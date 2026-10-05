<!-- doc: testing | chapter: 2 | part:  -->

[Barcha hujjatlar](../../README.md) / [Testlash qo'llanmasi](README.md)

# 2. Test piramidasi va test turlari xaritasi (Test Pyramid & the Map of Test Types)

<details>
<summary>Bu bobdagi 9 bo'lim</summary>

- [2.1 Klassik test piramidasi (Cohn)](#21-klassik-test-piramidasi-cohn)
- [2.2 Zamonaviy variantlar: Testing Trophy, Honeycomb, Test Diamond](#22-zamonaviy-variantlar-testing-trophy-honeycomb-test-diamond)
- [2.3 Teskari piramida (ice-cream cone) anti-patterni](#23-teskari-piramida-ice-cream-cone-anti-patterni)
- [2.4 Test turlari to'liq xaritasi](#24-test-turlari-toliq-xaritasi)
- [2.5 Qaysi mantiqni qaysi darajada testlash kerak](#25-qaysi-mantiqni-qaysi-darajada-testlash-kerak)
- [2.6 Test duplication: bir xil narsani ikki darajada testlash](#26-test-duplication-bir-xil-narsani-ikki-darajada-testlash)
- [2.7 Microservice va modular monolit uchun test taqsimoti namunasi](#27-microservice-va-modular-monolit-uchun-test-taqsimoti-namunasi)
- [2.8 Test nomlash va joylashtirish konvensiyasi](#28-test-nomlash-va-joylashtirish-konvensiyasi)
- [2.9 Arxitektor nazorat ro'yxati](#29-arxitektor-nazorat-royxati)

</details>



Test strategiyasi hujjat emas, byudjet taqsimotidir: har bir test darajasi pul, vaqt va ishonch o'rtasidagi muayyan kelishuvni ifodalaydi. Arxitektorning asosiy vazifasi - qaysi mantiq qaysi darajada tekshirilishini ongli ravishda belgilash va bu qarorni loyiha tuzilishi hamda build konfiguratsiyasida majburiy qilib qo'yish. Bu bobda klassik piramidadan zamonaviy shakllarga o'tish, test turlarining to'liq xaritasi, mantiq-daraja mosligi va Maven/Gradle darajasidagi amaliy konvensiyalar ko'rib chiqiladi. Maqsad - jamoada "bu testni qayerga yozaman?" savoliga bir xil javob beriladigan holatga erishish.

## 2.1 Klassik test piramidasi (Cohn)

Mike Cohn "Succeeding with Agile" (2009) kitobida test avtomatizatsiyasini uch qatlamli piramida sifatida tasvirlagan: keng asosda unit testlar, o'rtada service (integratsion) testlar, cho'qqida UI testlar. Shakl tasodifiy emas - u uchta o'zgaruvchining teskari proporsiyasini aks ettiradi: yuqoriga ko'tarilgan sari bitta testning ishga tushish vaqti, tiklash narxi va noaniqligi (flakiness) ortadi, lekin biznes ishonchi ham oshadi.

Keng asos kerakligining sababi matematik: Spring loyihasida bitta `@SpringBootTest` konteksti ko'tarilishi odatda bir necha soniya, oddiy unit test esa millisekundlar oladi. Agar 2000 ta holatni faqat yuqori darajada tekshirsangiz, suite soatlab ishlaydi va developer uni mahalliy mashinada ishga tushirmay qo'yadi - ya'ni test fikr-mulohaza (feedback) vositasi bo'lishdan to'xtaydi. Ikkinchi sabab - diagnostika aniqligi: unit test yiqilganda xato manzili bitta metod, E2E test yiqilganda esa o'ntacha servis ichida qolgan ehtimolliklar to'plami.

Piramidaning muhim, lekin ko'pincha e'tibordan chetda qolgan sharti: pastdagi testlar ustidagi testlarni *takrorlamasligi* kerak. Piramida qatlamlar qalinligi haqida emas, javobgarlik bo'linishi haqidagi shartnoma.

## 2.2 Zamonaviy variantlar: Testing Trophy, Honeycomb, Test Diamond

Klassik piramida 2009-yilda, DI konteynerlari sekin va konteynerlashtirish mavjud emas paytda shakllangan. Testcontainers, tez Spring kontekst keshi va kuchli statik analiz piramidani qayta muvozanatlashtirishga imkon berdi.

**Testing Trophy** (Kent C. Dodds) to'rt qatlamdan iborat: statik analiz (compiler, linter, null-check), unit, integration (eng keng qism), E2E. Asosiy g'oya - "integration" darajasi eng yaxshi ishonch/narx nisbatini beradi, chunki u real wiring'ni tekshiradi, lekin brauzer yoki to'liq muhitni talab qilmaydi. Java olamida bu Spring'ning slice testlari (`@WebMvcTest`, `@DataJpaTest`) va Testcontainers bilan ishlaydigan modul testlari.

**Testing Honeycomb** (Spotify, 2018) microservice'lar uchun taklif qilingan: o'rtada keng "integration test" qatlami, ikki tomonda tor "integrated test" (boshqa real servislar bilan) va "implementation detail test" qatlamlari. Mantiq - microservice'da murakkablik kodning ichida emas, servis chegarasida: HTTP contract, serializatsiya, DB mapping, message broker. Shuning uchun ko'p unit test yozishdan ko'ra, servisni chegaralari bilan birga, lekin tashqi real servislarsiz testlash foydali.

**Test Diamond** - yupqa unit, semiz integratsion va yupqa E2E qatlamlari. Bu shakl legacy modullarda yoki domain mantiqi kam bo'lgan, asosan orkestratsiya va mapping bilan shug'ullanadigan servislarda tabiiy yuzaga keladi.

| Loyiha turi | To'g'ri shakl | Nega |
|---|---|---|
| Boy domain mantiqli modular monolit | Piramida / Trophy | Qoidalar POJO darajasida testlanadi, modul chegaralari integratsiyada |
| CRUD-ga yaqin microservice | Honeycomb / Diamond | Risk chegarada: contract, mapping, DB, broker |
| Kutubxona yoki SDK | Qattiq piramida | Tashqi I/O yo'q, API yuzasi keng, mutation testing arzon |
| Legacy, testsiz tizim | Diamond (vaqtincha) | Avval xatti-harakatni integratsiyada "qotirish", keyin pastga tushirish |
| BFF / API gateway | Honeycomb | Deyarli butun qiymat serializatsiya va routing'da |

Shaklni tanlash qarori ADR (Architecture Decision Record) sifatida yozilishi kerak - aks holda har bir jamoa a'zosi o'z piramidasini quradi.

## 2.3 Teskari piramida (ice-cream cone) anti-patterni

Ice-cream cone - asosi yupqa unit testlardan, tanasi integratsion testlardan va keng cho'qqisi E2E/manual testlardan iborat teskari shakl (atama Alister Scott tomonidan ommalashtirilgan). U hech qachon ongli tanlov natijasi bo'lmaydi: u "release oldidan QA hammasini bosib ko'radi" degan jarayonning avtomatizatsiyaga ko'chirilishidan kelib chiqadi.

Narxi aniq o'lchanadi:

- **Feedback vaqti.** PR pipeline 10 daqiqadan 60-90 daqiqaga chiqadi, developer kontekstni yo'qotadi, batch'lar kattalashadi.
- **Flakiness.** E2E testlar zanjiridagi har bir bo'g'in ishonchliligi 99% bo'lsa ham, 40 bo'g'inli suite'ning barqarorligi ~67% ga tushadi. Natijada "qayta ishga tushir" madaniyati va yashil build'ga ishonchsizlik paydo bo'ladi.
- **Diagnostika narxi.** Bitta yiqilgan E2E test uchun o'rtacha tahlil vaqti unit testdan 10-30 barobar ko'p.
- **Refactoring to'xtaydi.** Ichki tuzilma testlar bilan qoplanmagani uchun har qanday o'zgarish regressiya qo'rquvini keltiradi.
- **Infrastruktura xarajati.** Har bir PR uchun to'liq muhit ko'tarish CI hisobining asosiy qismiga aylanadi.

Tuzatish yo'li - testni o'chirish emas, **pastga ko'chirish**: yiqilgan E2E testdagi har bir assertion uchun "bu holat eng past qaysi darajada tasdiqlanishi mumkin?" savolini berib, mos darajada test yozib, keyin E2E'dan o'sha assertion'ni olib tashlash.

## 2.4 Test turlari to'liq xaritasi

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

## 2.5 Qaysi mantiqni qaysi darajada testlash kerak

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

## 2.6 Test duplication: bir xil narsani ikki darajada testlash

Duplication piramidani ichdan buzadi: suite o'sadi, lekin ishonch o'smaydi. Tipik ko'rinishlari - bir xil hisob-kitob unit va E2E'da; validatsiyaning har bir qoidasi uchun alohida controller testi; `@SpringBootTest` ichida mapper'ni tekshirish.

Kesish uchun amaliy qoida - **har bir assertion uchun bitta "egasi" daraja**:

1. Har bir test holati uchun "eng past daraja, qaysiki bu xatoni tuta oladi" ni aniqlang va test shu yerda yashasin.
2. Yuqori daraja faqat *integratsiya faktini* tasdiqlasin: "controller to'g'ri servisni chaqirdi va natijani JSON qildi", "xabar broker'ga yetib bordi" - qiymatlar to'g'riligini emas.
3. E2E testlar uchun qattiq kvota belgilang (masalan, 15 ta) va yangi E2E qo'shish uchun eskisini olib tashlashni talab qiling.
4. Bug uchun regression test faqat bitta darajada yoziladi - bug qaysi darajada tutilishi mumkin bo'lsa, o'sha yerda.
5. Mutation testing bilan tekshiring: agar unit testni o'chirganda mutation score o'zgarmasa, u duplication.

## 2.7 Microservice va modular monolit uchun test taqsimoti namunasi

| Daraja | Microservice | Modular monolit | Kutubxona |
|---|---|---|---|
| Unit | 50-60% | 45-55% | 75-85% |
| Komponent / slice / modul | 20-25% | 25-30% | 5-10% |
| Integratsion (Testcontainers) | 10-15% | 10-15% | 10-15% |
| Contract | 3-5% | 1-2% (modullar orasida) | 0% |
| System / E2E | 1-3% | 3-5% | 0% |
| Nofunksional (perf, security, chaos) | ~1%, alohida pipeline | ~1% | kam |

Ishga tushish vaqti byudjeti - bu raqamlar CI'da gate sifatida majburlanishi kerak:

| Suite | Byudjet | Qachon ishlaydi |
|---|---|---|
| Unit (`*Test`, Spring konteksti yo'q) | < 60-90 s | Har commit, lokal watch |
| Slice + kontekst testlari | < 3 daqiqa | Har commit |
| Integratsion (`*IT`, Testcontainers) | < 8-10 daqiqa | Har PR |
| Contract verifikatsiya | < 2 daqiqa | Har PR |
| Smoke (deploy'dan keyin) | < 1 daqiqa | Har deploy |
| E2E + nofunksional | 20-60 daqiqa | Nightly va release oldidan |

Umumiy PR pipeline 15 daqiqadan oshmasligi maqsadli ko'rsatkich; oshsa, parallellashtirish yoki pastga ko'chirish talab qiladi.

## 2.8 Test nomlash va joylashtirish konvensiyasi

Konvensiya build vositasi tomonidan majburlansa ishlaydi. Maven Surefire sukut bo'yicha `**/Test*.java`, `**/*Test.java`, `**/*Tests.java`, `**/*TestCase.java` ni oladi; Failsafe esa `**/IT*.java`, `**/*IT.java`, `**/*ITCase.java` ni `integration-test` va `verify` fazalarida ishga tushiradi. Shuning uchun eng arzon ajratish - `*Test` = tez, `*IT` = sekin.

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

Maven konfiguratsiyasi - Surefire tezlarni, Failsafe sekinlarni oladi; `groups`/`excludedGroups` JUnit 5 tag ifodalariga o'tadi:

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

Tag'larni har testda qo'lda yozish o'rniga, kompozit annotatsiya yaratish kerak - shunda semantika bitta joyda saqlanadi:

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

## 2.9 Arxitektor nazorat ro'yxati

- [ ] Loyiha uchun test shakli (piramida / Trophy / Honeycomb / Diamond) tanlangan va ADR'da sababi bilan yozilgan.
- [ ] Har bir mantiq turi (domain, validatsiya, mapping, SQL, contract, security, event, tranzaksiya, resilience, konfiguratsiya) uchun "egasi" daraja hujjatlashtirilgan.
- [ ] `*Test` va `*IT` ajratilgan, Surefire/Failsafe yoki Gradle `JvmTestSuite` konfiguratsiyasi shu ajratishni majburlaydi.
- [ ] `@Tag` taksonomiyasi cheklangan (masalan `integration`, `slow`, `e2e`, `security`) va kompozit annotatsiyalar orqali qo'llanadi.
- [ ] Har bir suite uchun vaqt byudjeti belgilangan va CI'da oshib ketganda signal beradi (PR pipeline < 15 daqiqa).
- [ ] E2E testlar soni uchun qattiq kvota mavjud; yangisini qo'shish eskisini pastga ko'chirishni talab qiladi.
- [ ] Integratsion testlar real DB/broker (Testcontainers) bilan ishlaydi, in-memory o'rnini bosuvchilar prod dialektini yashirmaydi.
- [ ] Duplication davriy ravishda tekshiriladi (suite tarkibi `@Tag` bo'yicha hisoblanadi, kritik paketlarda mutation score o'lchanadi).

---

[&larr; 1. Sifat strategiyasi va arxitektorning roli](01-sifat-strategiyasi-va-arxitektorning-roli.md) · [Mundarija](README.md) · [3. Kim nima yozadi: rollar va mas'uliyat &rarr;](03-kim-nima-yozadi-rollar-va-masuliyat.md)
