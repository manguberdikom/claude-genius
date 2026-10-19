<!-- doc: testing | chapter: 2 | part:  -->

[Barcha hujjatlar](../../README.md) / [Testlash qo'llanmasi](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

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

Quyidagi uch shakl sanoat amaliyotidan kelib chiqqan taklif: ularning manbasi kitob emas, muallif blogi va konferensiya materiallari. Shuning uchun ularni "kanonik model" deb emas, kontekstga qarab tanlanadigan variant deb qarang.

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

Ice-cream cone - teskari shakl: E2E va qo'lda testlar ko'p, integratsion va unit testlar esa ikkisi ham kam. Ta'rifni aniq ushlang: bu yerda o'rta qatlam ham semiz emas, aynan pastki ikki qatlam birga yupqa.

Yonidagi ikkinchi anti-pattern - **soat qumi (hourglass)**: unit testlar ko'p, E2E testlar ko'p, o'rtadagi integratsion qatlam esa bo'sh. Bu ice-cream cone dan ham chalg'ituvchi, chunki suite tashqaridan sog'lom ko'rinadi - pastda minglab unit test bor - lekin qatlamlar o'rtasidagi wiring hech qayerda tekshirilmaydi, shuning uchun har bir regressiya to'g'ridan-to'g'ri E2E da, ya'ni eng qimmat va eng sekin joyda ushlanadi. U hech qachon ongli tanlov natijasi bo'lmaydi: u "release oldidan QA hammasini bosib ko'radi" degan jarayonning avtomatizatsiyaga ko'chirilishidan kelib chiqadi.

Narxi aniq o'lchanadi:

- **Feedback vaqti.** PR pipeline 10 daqiqadan 60-90 daqiqaga chiqadi, developer kontekstni yo'qotadi, batch'lar kattalashadi.
- **Flakiness.** E2E testlar zanjiridagi har bir bo'g'in ishonchliligi 99% bo'lsa ham, 40 bo'g'inli suite'ning barqarorligi ~67% ga tushadi. Natijada "qayta ishga tushir" madaniyati va yashil build'ga ishonchsizlik paydo bo'ladi.
- **Diagnostika narxi.** Bitta yiqilgan E2E test uchun tahlil vaqti unit testdan ancha ko'p, chunki yiqilish sababi butun zanjirda bo'lishi mumkin (brauzer, tarmoq, ma'lumot, boshqa servis). Nisbatni o'z suite ingizda o'lchash kerak: yiqilgan testdan to sababni topishgacha ketgan vaqtni bir oy yozib yuring.
- **Refactoring to'xtaydi.** Ichki tuzilma testlar bilan qoplanmagani uchun har qanday o'zgarish regressiya qo'rquvini keltiradi.
- **Infrastruktura xarajati.** Har bir PR uchun to'liq muhit ko'tarish CI hisobining asosiy qismiga aylanadi.

Tuzatish yo'li - testni o'chirish emas, **pastga ko'chirish**: yiqilgan E2E testdagi har bir assertion uchun "bu holat eng past qaysi darajada tasdiqlanishi mumkin?" savolini berib, mos darajada test yozib, keyin E2E'dan o'sha assertion'ni olib tashlash.

**Shakl qanday paydo bo'ladi: prototip bir necha kunda legacy ga aylanadi.** Google ning izohi ice-cream cone ning kelib chiqishini vaqt o'lchoviga bog'laydi. Kod bir necha daqiqa yashaydi deb o'ylanganda qo'lda sinash to'g'ri tanlov: skript yoziladi, ishga tushirib ko'riladi, funksiya qo'shiladi, yana ishga tushirib ko'riladi. Keyin skript ishlay boshlaydi, boshqalarga beriladi, lekin avtomatik testi yo'q. Eng yomon holat esa kodning o'zi unit test yozishga qulay bo'lmagan shaklda yozilgani: shunda yozish mumkin bo'lgan yagona avtomatik test E2E bo'lib qoladi va **bir necha kun ichida legacy kod** paydo bo'ladi.

Shundan amaliy qoida: prototip bo'lsa ham, **rivojlanishning birinchi kunlarida** piramidaga o'tish kerak, ya'ni unit testlar yoziladi va shundan keyin ustiga avtomatik integratsion testlar qo'shiladi, qo'lda E2E dan esa chiqib ketiladi. Google buni submit sharti qilib qo'ygan: unit test bo'lmasa o'zgarish qabul qilinmaydi. Qolgan bo'shliq - unit test va qo'lda test orasidagi oraliq qatlam - alohida ish talab qiladi va u uzoq muddatli sog'liq uchun zarur.

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

Jadvaldagi "qancha" ustuni mutlaq raqam emas, nisbat haqida: Spring loyihasida suite tarkibini `@Tag` bo'yicha hisoblab, bu nisbatlardan chetlanishni metrika sifatida kuzatish mumkin. Ustundagi foizlar shu korpusning amaliy mo'ljali, biror kitobdan ko'chirilgan emas. Manbaga tayangan yagona nisbat Google ning o'z taqsimoti: test soni bo'yicha taxminan 80% kichik (unit), 15% o'rta qamrovli integratsion va 5% uchidan-uchiga test, va kitobning o'zi buni "juda qo'pol mo'ljal" deb ataydi. Tez-tez keltiriladigan 70/20/10 nisbatining esa aniq birlamchi manbasi yo'q, uni iqtibos sifatida ishlatmang.

Xaritaning o'zi haqida bitta shart ham bor va uni yozib qo'yish kerak: xarita universal emas. Orosz integratsion va UI test atamalarining chegarasi haqida tortishishni foydasiz deb hisoblaydi va muhim narsa boshqa deydi: jamoa qaysi atamada nimani nazarda tutishini kelishib olishi (Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 14-bob, 198-bet). Amaliy natija: yuqoridagi jadval korpus ichidagi atama kelishuvi bo'lib qoladi, lekin boshqa jamoada "integratsion test" boshqa narsani bildirishi mumkin, shuning uchun test strategiyasi hujjatining birinchi bo'limi atamalar ta'rifi bo'ladi. Atama kelishilmagan joyda qamrov raqamlari ham taqqoslanmaydi.

Google ning modelida yana bir ajratish bor va u bu jadvalda yo'q: har bir test ikki MUSTAQIL o'lchov bilan tavsiflanadi. Birinchisi hajm (size): kichik test bitta process ichida ishlaydi, o'rta test bitta mashinada, katta test esa istalgan joyda (Google da to'rtinchi daraja ham bor: enormous). Ikkinchisi qamrov (scope): test kodning qancha qismini tekshiradi - bitta metodmi, bir necha sinf wiring'imi, butun tizimmi. Bu ikkisi bir-biriga bog'lanmagan: kichik hajmli test keng qamrovli bo'lishi mumkin va teskarisi. Yuqoridagi jadvalning "Tezlik" ustuni aslida hajm xususiyati, qatorlar esa qamrov bo'yicha ajratilgan - shuning uchun uni o'qiyotganda ikki o'lchovni aralashtirmang. Amalda hajmni belgilash foydali, chunki parallellik va izolyatsiya aynan hajmga bog'liq: faqat kichik testlar cheklovsiz parallel ishlaydi.

**Hajm cheklovlari asbob bilan majburlanadi, kelishuv bilan emas.** Google da hajm ta'riflari test infratuzilmasida kodlangan: kichik test bitta processda (ko'p tilda bitta threadda) ishlaydi, uxlamaydi, I/O bajarmaydi va bloklanadigan chaqiruv qilmaydi, ya'ni tarmoq va diskka chiqmaydi. Bu ta'rif hujjatda qolmaydi: Java testlari maxsus security manager ostida yurgiziladi va `small` deb belgilangan test taqiqlangan amalni bajarsa (masalan tarmoq ulanishi ochsa) **yiqiladi**. Sabab aniq: cheklovlar kichik testni sekinlik va nondeterminizmning asosiy manbalaridan uzadigan qum qutisi (sandbox) yasaydi. O'rta testga bitta mashina ichida qolish sharti bilan ko'proq erkinlik beriladi, lekin tarmoq murojaati faqat `localhost` ga ruxsat etiladi; katta test esa istalgan joyda ishlaydi va E2E hamda legacy tizim uchun saqlanadi. Katta testlar kichiklaridan ajratilib, har push da emas, build va reliz bosqichida yurgiziladi.

JVM da security manager Java 17 dan beri o'chirilgan ([JEP 411](https://openjdk.org/jeps/411)), shuning uchun zamonaviy shakli boshqa: cheklov `@Tag` va build konfiguratsiyasi bilan ajratiladi, taqiqni esa ArchUnit qoidasi (`noClasses().that().haveSimpleNameEndingWith("Test")...`) va Testcontainers/HTTP client importini bloklash bilan majburlanadi.

```java
@Test
void smallTestsDoNotTouchNetworkOrDisk() {
    ArchRuleDefinition.noClasses()
            .that().haveSimpleNameEndingWith("Test")
            .and().areAnnotatedWith(Tag.class)
            .should().dependOnClassesThat()
            .resideInAnyPackage("java.net..", "org.testcontainers..", "java.nio.file..")
            .check(new ClassFileImporter().importPackages("com.example"));
}
```

ESLATMA: Google ning security manager yechimi JDK 17+ da ishlamaydi; yuqoridagi ArchUnit shakli korpus qo'shimchasi, kitobda bu variant yo'q.

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

Duplication'ni kesishdan oldin teskari chegarani ham belgilab oling. Google da bu "Beyonce qoidasi" deb ataladi: buzilishini xohlamagan har bir narsani test bilan qoplang. Ya'ni duplication'ni kamaytirish hech narsani qoplamay qoldirish degani emas - har bir xatti-harakat kamida BITTA darajada tekshirilsin, lekin birdan ortiq darajada qiymat tekshirilmasin.

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

```text
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

## Manbalar

- Robert C. Martin, *Clean Architecture*, 28-bob - test chegarasi, testlar tizimning qismi ekani va mo'rt test muammosi
- Titus Winters, Tom Manshreck, Hyrum Wright (tahr.), *Software Engineering at Google*, O'Reilly, 2020, 11-bob "Testing Overview" - Google ning piramida versiyasi va taqsimoti (~80% kichik, ~15% o'rta qamrovli, ~5% uchidan-uchiga, kitobning o'zi "juda qo'pol mo'ljal" deb ataydi); hajm (size) va qamrov (scope) ikki mustaqil o'lchov; kichik/o'rta/katta test ta'riflari; ice-cream cone va soat qumi anti-patternlari; "buzilishini xohlamagan narsani qopla" qoidasi
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 11-bob ("Test Size", "Test sizes in practice") - kichik testning cheklovlari (bitta process, sleep yo'q, I/O va bloklanadigan chaqiruv yo'q) va ularning test infratuzilmasi orqali majburlanishi, taqiqlangan amal qilgan kichik testning yiqilishi, o'rta testga `localhost` ruxsati va katta testning qolgan hollar uchun saqlanishi. Bu nashrning nusxasida barqaror bet raqami yo'q, shuning uchun bob va bo'lim nomi ko'rsatilgan
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 14-bob ("Larger Tests and Time") - qo'lda sinalgan prototipning bir necha kunda legacy ga aylanishi, unit test yozish qiyin bo'lsa faqat E2E qolishi va rivojlanishning birinchi kunlarida piramidaga o'tish zarurati. Bu nashrning nusxasida barqaror bet raqami yo'q, shuning uchun bob va bo'lim nomi ko'rsatilgan
- [JEP 411, Deprecate the Security Manager for Removal](https://openjdk.org/jeps/411) - Java 17 dan security manager eskirgan, shuning uchun Google ning hajm cheklovini majburlash yechimi zamonaviy JDK da ishlamaydi
- Mike Cohn, *Succeeding with Agile*, 2009 - klassik test piramidasining asl manbasi (Google kitobidagi havola orqali)
- Gerard Meszaros, *xUnit Test Patterns: Refactoring Test Code*, Addison-Wesley, 2007, 6-bob, 51-53-betlar - test turlari taksonomiyasi va "component test" atamasi; "integration" va "subsystem" atamalarining turli ma'nolari haqida ogohlantirish
- ESLATMA: 2.2 dagi Testing Trophy, Honeycomb va Test Diamond shakllari muallif blogi va konferensiya materiallaridan, kitob manbasi emas; 2.4 va 2.7 dagi foizlar va vaqt chegaralari shu korpusning amaliy mo'ljali
- Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 14-bob (198-bet) - integratsion va UI test atamalarining chegarasi muhim emasligi, jamoa qaysi atamada nimani nazarda tutishini kelishib olishi muhim bo'lishi

---

[&larr; 1. Sifat strategiyasi va arxitektorning roli](01-sifat-strategiyasi-va-arxitektorning-roli.md) · [Mundarija](README.md) · [3. Kim nima yozadi: rollar va mas'uliyat &rarr;](03-kim-nima-yozadi-rollar-va-masuliyat.md)
