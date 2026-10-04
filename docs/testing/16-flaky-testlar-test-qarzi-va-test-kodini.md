<!-- doc: testing | chapter: 16 | part:  -->

[Java Spring loyihasida testlash](../../README.md) / [Testlash qo'llanmasi](README.md)

# 16. Flaky testlar, test qarzi va test kodini saqlash (Flaky Tests, Test Debt & Maintenance)

<details>
<summary>Bu bobdagi 13 bo'lim</summary>

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

</details>



Test suite'ning qiymati uning yashil rangiga emas, ishonchliligiga bog'liq: agar jamoa qizil build'ni ko'rib birinchi navbatda "qayta ishga tushir" tugmasini bossa, siz testlarni emas, faqat CI vaqtini sotib olgansiz. Flaky testlar, to'planib qolgan test qarzi va saqlanmaydigan test kodi eng yaxshi test strategiyasini ham yemirib tashlaydi. Bu bob flaky testni sabablari bo'yicha tasniflash, aniqlash, karantinga olish va yo'q qilish jarayonini, shuningdek test kodini production kodi darajasida saqlash amaliyotlarini qamrab oladi.

## 16.1 Flaky test nima va nega eng qimmat muammo

Flaky test - kod va muhit o'zgarmagan holda bir xil commit'da bir marta yashil, boshqa marta qizil bo'ladigan test. Texnik jihatdan bu determinizmning yo'qolishi: natija faqat tekshirilayotgan kodga emas, balki vaqt, tartib, parallelism yoki tashqi holatga ham bog'liq bo'lib qoladi.

Narxi uch qatlamdan iborat:

1. **CI xarajati.** 1500 testli suite, build 12 daqiqa, kuniga 60 build. Test darajasida 0.05% flake rate ham build'larning yarmida kamida bitta qizil test beradi. Kuniga 25 qayta ishga tushirish × 12 daqiqa ≈ 5 soat runner vaqti, oyiga ~110 soat.
2. **Insoniy xarajat.** Qizil build'ni tekshirish, log o'qish, "bu flaky ekan" xulosasiga kelish - o'rtacha 10-15 daqiqa. Kuniga 25 hodisa × 12 daqiqa ≈ 5 soat/kun, oyiga deyarli bitta FTE ekvivalenti.
3. **Ishonchning yo'qolishi - eng qimmati.** Flake rate 1-2% dan oshganda jamoa har bir qizilni "ehtimol flaky" deb taxmin qiladi. Shu daqiqadan boshlab suite regressiyani ushlash qobiliyatini yo'qotadi: haqiqiy xato ham xuddi shu "qayta ishga tushir" bilan yopilib, production'ga chiqib ketadi.

Arxitektor uchun xulosa: flaky test bitta test muammosi emas, butun suite'ning ishonch koeffitsiyentini pasaytiruvchi tizimli nuqson. Shuning uchun flake rate 1% dan oshsa, yangi feature testlarini yozishni to'xtatib barqarorlikni tiklash to'g'ri qaror bo'ladi.

## 16.2 Flaky testning asosiy sabablari, misollar va yechimlari

Quyidagi jadval - diagnostikada birinchi murojaat qiladigan ro'yxat. Amalda hodisalarning 80% i birinchi beshta qatorga to'g'ri keladi.

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

## 16.3 Flaky testni aniqlash

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

## 16.4 Karantin (quarantine) jarayoni

Karantin - flaky testni o'chirib yuborish emas, uni vaqtincha blocking bo'lishdan chiqarib, egasi va muddati bilan ro'yxatga olish. Qadamlar:

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

4. **Egasini belgilash.** Egasi yo'q karantin - abadiy karantin.
5. **SLA qo'yish.** Tavsiya: 2 sprint (14 kun), muddat test kodida va ticket'da yoziladi.
6. **Muddat o'tgach qaror.** Faqat ikki variant: tuzatildi va karantindan chiqdi, yoki o'chirildi. "Yana 2 sprint" taqiqlanadi, aks holda ro'yxat go'ristonga aylanadi.
7. **Kvota.** Karantinda bir vaqtda jami testlarning 0.5% dan ko'pi bo'lmasligi kerak. Kvota to'lsa, yangi feature ishi to'xtatiladi.

Zanjir: `flake aniqlandi → @Tag + ticket + egasi + SLA → PR gate'dan chiqarildi → nightly'da kuzatiladi → SLA ichida tuzatildi ? chiqdi : o'chirildi`.

## 16.5 Retry'ning o'rni

Retry - og'riq qoldiruvchi, davo emas. Qoida: retry faqat infratuzilma nosozligi uchun. Legitim holatlar - Docker image tortib olish, Testcontainers start, dependency yuklash, runner tarmog'ining uzilishi; bunday retry'lar pipeline step darajasida qo'yiladi, test darajasida emas.

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

Surefire bunday testlarni XML hisobotda `flakyFailure` elementi sifatida belgilaydi - bu aynan o'lchash uchun kerakli ma'lumot. Gradle'da `org.gradle.test-retry` plugin'i `maxRetries` va muhim `failOnPassedAfterRetry` opsiyasini beradi. JUnit 5'da standart retry API yo'q: `TestTemplateInvocationContextProvider` asosida custom extension yozish yoki tashqi kutubxona ishlatish kerak; `@RepeatedTest` retry emas, u boshqa maqsadga xizmat qiladi.

Qat'iy qoida: retry yoqilgan bo'lsa, `flakyFailure` soni dashboard'da ko'rsatiladi va u ham nolga intilishi kerak. Retry'ni global yoqib hisobotni o'qimaslik - flake'ni rasman qonuniylashtirish.

## 16.6 Test qarzi (test debt)

Test qarzi - suite'ning kelajakdagi o'zgarishlarni qo'llab-quvvatlash qobiliyatini kamaytiruvchi har qanday holat. Turlari: **eskirgan test** (o'zgargan talabni tekshiradi, lekin mock'lar shunchalik chuqur ki real xatti-harakat ko'rinmaydi); **assertion'siz test** (faqat metodni chaqiradi - mutation testing bunday testlarni darhol ochadi); **abadiy `@Disabled`** (sababi yozilmagan, hech kim tegishga qo'rqadi); **takrorlangan test** (bir scenariyni uch darajada tekshiradi, qo'shimcha xavf qoplamaydi); **tushunarsiz test** (80 qatorli setup, nomi `test1`).

Inventarizatsiya qilmasdan qarzni to'lash mumkin emas:

```bash
grep -rn "@Disabled" --include=*.java src/test | wc -l
grep -rn '@Disabled$' --include=*.java src/test        # sababsiz o'chirilganlar
grep -rLn -e "assertThat" -e "verify(" -e "assert" \
  --include=*Test.java src/test/java                   # assertion'siz nomzodlar
grep -rn '@Tag("flaky")' --include=*.java src/test | wc -l
```

Natijani bitta jadvalga yig'ib (test, tur, modul, egasi, qaror), har sprint'da belgilangan kvotani (masalan, 10 element) yopish kerak. "Bir hafta ichida hammasini tuzatamiz" rejasi deyarli har doim muvaffaqiyatsiz bo'ladi; o'lchanadigan kvota ishlaydi.

## 16.7 Testni o'chirish qoidalari

Test o'chirish tabu emas: noto'g'ri test salbiy qiymatga ega, chunki saqlashni talab qiladi, lekin xavfni qoplamaydi.

**O'chirish to'g'ri:** test boshqa test bilan to'liq dublikat; talab o'zgardi yoki feature olib tashlandi; test faqat implementatsiya detalini (private metod, getter) tekshiradi va refaktoringda har doim buziladi; xuddi shu xavf arzonroq va barqarorroq test bilan qoplangan; test flaky, karantin SLA o'tdi va qoplanayotgan xavf muhim emas.

**O'chirish noto'g'ri:** test qizil, chunki production kodda haqiqiy bug bor (eng xavfli holat); test sekin (bu tezlashtirish vazifasi); testni tushunish qiyin (bu refaktoring vazifasi); test har o'zgarishda buziladi, lekin biznes qoidasini himoya qiladi (buzilishi - signal, shovqin emas); muallifi noma'lum.

**Kim qaror qiladi.** Unit darajada - kod egasi jamoa, PR review'da. Integration va E2E darajada - jamoa va tech lead, chunki bu xavf qoplamasini o'zgartiradi. Compliance yoki audit testlari - faqat arxitektor va product owner roziligi bilan. Har bir o'chirishda PR description'da bitta savolga javob bo'lishi shart: "bu testni o'chirgach, qanday xavf endi qoplanmay qoladi?" Javob "hech qanday" bo'lsa, o'chirish xavfsiz; aks holda avval qoplamani boshqa joyga ko'chirish kerak.

## 16.8 Test kodini refaktoring qilish

Test kodi production kodidir: u kompilyatsiya qilinadi, CI'da ishlaydi, saqlanadi va buzilganda ish to'xtaydi. Lekin uning optimallashtirish maqsadi boshqacha - o'qiluvchanlik va xato sababini tez tushunish, DRY emas.

Balans qoidasi: testda bir oz takrorlanish yaxshi. Umumiy `setUp()` ga ko'chirilgan har bir qator testning lokal tushunarliligini kamaytiradi; agar testni o'qishda yuqoriga qarab uch metodni ochish kerak bo'lsa, abstraksiya juda uzoqqa ketgan. Shu bilan birga setup'ni qisqartirish zarur - abstraksiya orqali emas, test data builder orqali:

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

// KEYIN: builder - faqat scenariy uchun muhim qiymatlar ko'rinadi
@Test
void shouldRejectOrderOverCreditLimit() {
    var customer = aCustomer().withCreditLimit("1000").build();
    var order = anOrder().forCustomer(customer).withTotal("1500").build();
    assertThatThrownBy(() -> orderService.submit(order))
        .isInstanceOf(CreditLimitExceededException.class)
        .hasMessageContaining("credit limit");
}
```

Amaliy ro'yxat: nomlarni biznes tilida yozish (`shouldRejectOrderOverCreditLimit`, `testSubmit` emas); `@DisplayName` bilan scenariyni to'liq ifodalash; assertion'ni mazmunli qilish (`hasSize(3)` o'rniga `containsExactly(...)`); `assertTrue(x.equals(y))` ni AssertJ'ning tipga xos matcher'lariga o'tkazish - xato xabari ancha ma'lumotli bo'ladi; bir testda bir mantiqiy tasdiq, kerak bo'lsa `assertAll` yoki `SoftAssertions` bilan guruhlash. Test source'lariga ham code review va static analysis qo'llanadi.

## 16.9 Test smell'lar katalogi

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

## 16.10 Sekin testlarni tezlashtirish

Sekin suite - flake'ning yashirin sababi: muhandislar lokal ishga tushirishni tashlab faqat CI'ga tayanadi va fikr-mulohaza halqasi uzayadi. Eng sekin testlarni Surefire XML'dagi `time` atributidan topish mumkin:

```bash
find . -name 'TEST-*.xml' -path '*surefire-reports*' -print0 \
  | xargs -0 grep -ho '<testcase[^>]*>' \
  | sed -E 's/.*name="([^"]+)".*classname="([^"]+)".*time="([^"]+)".*/\3 \2#\1/' \
  | sort -rn | head -10
```

Gradle'da `build/reports/tests/test/index.html` sortlanadigan davomiylik ustuniga ega; Develocity test timeline'ni tarixiy taqqoslash bilan beradi.

Asosiy vositalar:

1. **Spring context sonini kamaytirish.** Har bir noyob konfiguratsiya - alohida yuklanish (5-20 s). `logging.level.org.springframework.test.context.cache=DEBUG` bilan kesh hit/miss statistikasini va `spring.test.context.cache.maxSize` (standart 32) chegarasini ko'rish mumkin. Maqsad: 3-5 ta standart test konfiguratsiyasi, mock bean'larni ad-hoc qo'shishdan voz kechish - har bir yangi kombinatsiya yangi context yaratadi.
2. **Konteynerni qayta ishlatish.** Testcontainers'da `@Container` ni `static` qilish, butun suite uchun singleton container pattern'i, lokal ishlab chiqishda `testcontainers.reuse.enable=true`. CI'da reuse o'chiriladi, chunki runner har safar toza.
3. **Testni past darajaga tushirish.** Eng samarali optimallashtirish - testni piramidaning pastki qatlamiga ko'chirish: E2E'dagi validatsiya scenariysi → `@WebMvcTest`; integration'dagi hisob-kitob mantiqi → toza unit test. Bitta E2E testni unit testga aylantirish odatda 30-60 sekundni millisekundlarga tushiradi.
4. **Parallelism.** `mode.default=same_thread` + `mode.classes.default=concurrent` eng xavfsiz boshlang'ich konfiguratsiya; Surefire `forkCount=1C` modul darajasida parallelism beradi. Parallelismni yoqishdan oldin tartib bog'liqligi tozalanishi shart, aks holda flake rate oshadi.

## 16.11 Testlar egaligi va madaniyat

Texnik yechimlar madaniyatsiz ishlamaydi. Minimal qoidalar: **buzgan tuzatadi** - buzilgan testni kodni o'zgartirgan muhandis tuzatadi, testni yozgan odam emas. **"Red build" qoidasi** - main qizil bo'lsa yangi merge yo'q; tiklash boshqa barcha ishdan ustun, SLA 30 daqiqa, aks holda revert (revert - jazo emas, standart operatsiya). **Egalik xaritasi** - har bir test paketi uchun mas'ul jamoa `CODEOWNERS` da yozilgan; egasiz test - tuzatilmaydigan test. **Haftalik test sog'ligi ko'rib chiqishi** - 20-30 daqiqa: flake rate trendi, karantin ro'yxati va SLA'lar, eng sekin 10 test, yangi `@Disabled` testlar; natija - nomlangan egali ticket'lar, umumiy xohish emas. **Yangi flake'ni darhol to'xtatish** - ikki hafta ichida ikki marta flake bo'lgan test avtomatik karantin nomzodi.

## 16.12 Anti-patternlar

- **Flaky testni `@Disabled` qilib unutish.** Sababsiz, egasiz, muddatsiz `@Disabled` - qarzni rasmiylashtirish; bir yildan keyin 200 ta o'chirilgan test va hech kim nega ekanini bilmaydi.
- **Retry'ni global yoqib qo'yish.** Butun suite'ga `rerunFailingTestsCount=3` flake rate'ni nolga tushirmaydi, uni ko'rinmas qiladi; haqiqiy race condition production'ga chiqadi.
- **"Mening mashinamda ishlaydi".** Bu diagnostika emas, muammoning tavsifi: test muhitga bog'liq, demak flaky. To'g'ri javob - timezone, locale, CPU soni, Docker versiyasi va test tartibini CI bilan tenglashtirib qayta sinash.
- **Testni o'zgartirib production xatosini yashirish.** Kutilgan qiymatni haqiqiy qiymatga moslashtirish bug'ni test suite ichida muzlatib qo'yadi. Qoida: avval "talab o'zgardimi?" savoliga PR'da yozma javob berish.
- **Assertion'ni yumshatib testni yashil qilish.** `isEqualTo(expected)` ni `isNotNull()` ga almashtirish: test yashil, qoplama yo'q. Mutation testing bunday yumshatishni aniq ko'rsatadi.
- **Flake'ni "normal shovqin" deb qabul qilish.** "Har build'da 2-3 test flake bo'ladi, bu normal" - suite'ning o'lim sertifikati.
- **Barcha flake'larni bir vaqtda tuzatishga urinish.** Flake rate bo'yicha reyting tuzib eng yuqori 20 tasidan boshlash kerak: odatda ular hodisalarning 70-80% ini beradi.

## 16.13 Arxitektor nazorat ro'yxati

- [ ] Flake rate o'lchanadi: barcha build'lardan test natijalari tarixi markaziy joyda saqlanadi va test darajasida flake rate hisoblanadi (maqsad < 1%).
- [ ] Karantin jarayoni rasmiylashtirilgan: `@Tag("flaky")` konvensiyasi, ticket, nomlangan egasi, SLA (≤ 2 sprint), muddat o'tganda o'chirish qoidasi va ≤ 0.5% kvota.
- [ ] Retry siyosati yozilgan: infratuzilma retry'i pipeline darajasida, test retry faqat vaqtinchalik va `flakyFailure` hisoboti bilan; global retry yoqilmagan.
- [ ] Nondeterminizm manbalari arxitektura darajasida yopilgan: `Clock` inject qilinadi, `Thread.sleep` taqiqlangan, timezone/locale CI'da qat'iy, random seed loglanadi.
- [ ] Suite tasodifiy tartibda va parallel rejimda kamida nightly sinaladi, shunda tartibga bog'liqlik PR gate'ga chiqmasdan aniqlanadi.
- [ ] Test qarzi inventarizatsiya qilingan: `@Disabled`, assertion'siz, dublikat va eskirgan testlar ro'yxati bor; har sprint'da kvota yopiladi.
- [ ] Test smell'lar katalogi PR review checklist'iga kiritilgan va test kodiga production kodi bilan bir xil review standarti qo'llanadi.
- [ ] Suite tezligi kuzatiladi: eng sekin 10 test haftalik ko'rib chiqiladi, Spring context soni cheklangan, "red build" tiklash ustuvorligi va `CODEOWNERS` egalik xaritasi kelishilgan.

---

[&larr; 15. CI/CD da test pipeline](15-ci-cd-da-test-pipeline.md) · [Mundarija](README.md) · [17. Metrikalar va test yetukligi modeli &rarr;](17-metrikalar-va-test-yetukligi-modeli.md)
