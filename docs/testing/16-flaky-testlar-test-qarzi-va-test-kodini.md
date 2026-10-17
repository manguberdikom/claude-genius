<!-- doc: testing | chapter: 16 | part:  -->

[Barcha hujjatlar](../../README.md) / [Testlash qo'llanmasi](README.md)

> Holat: tekshirilmoqda. Da'volar hali manbaga solishtirilmoqda.

# 16. Flaky testlar, test qarzi va test kodini saqlash (Flaky Tests, Test Debt & Maintenance)

<details>
<summary>Bu bobdagi 30 bo'lim</summary>

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
- [16.13 Smell lar uch qatlami: code, behavior va project smell](#1613-smell-lar-uch-qatlami-code-behavior-va-project-smell)
- [16.14 Erratic Test: tartib va holat orqali o'zaro ta'sir](#1614-erratic-test-tartib-va-holat-orqali-ozaro-tasir)
- [16.15 Test Run War, Resource Leakage va Resource Optimism](#1615-test-run-war-resource-leakage-va-resource-optimism)
- [16.16 Fragile Test va to'rt sezgirlik](#1616-fragile-test-va-tort-sezgirlik)
- [16.17 Overspecified Software, Sensitive Equality va Fragile Fixture](#1617-overspecified-software-sensitive-equality-va-fragile-fixture)
- [16.18 Slow Tests ning to'rt nomlangan sababi](#1618-slow-tests-ning-tort-nomlangan-sababi)
- [16.19 Frequent Debugging: defekt lokalizatsiyasining yo'qligi](#1619-frequent-debugging-defekt-lokalizatsiyasining-yoqligi)
- [16.20 Manual Intervention: testni odam ushlab turadigan joylar](#1620-manual-intervention-testni-odam-ushlab-turadigan-joylar)
- [16.21 Assertion Roulette va Missing Assertion Message](#1621-assertion-roulette-va-missing-assertion-message)
- [16.22 Conditional Test Logic ning besh sababi](#1622-conditional-test-logic-ning-besh-sababi)
- [16.23 Obscure Test ning olti sababi](#1623-obscure-test-ning-olti-sababi)
- [16.24 Hard-to-Test Code: testlash qiyinligi dizayn muammosi](#1624-hard-to-test-code-testlash-qiyinligi-dizayn-muammosi)
- [16.25 Test Code Duplication: ko'chirish va g'ildirakni qayta ixtiro qilish](#1625-test-code-duplication-kochirish-va-gildirakni-qayta-ixtiro-qilish)
- [16.26 Test Logic in Production: test mantiqining production ga oqib o'tishi](#1626-test-logic-in-production-test-mantiqining-production-ga-oqib-otishi)
- [16.27 Buggy Tests va High Test Maintenance Cost](#1627-buggy-tests-va-high-test-maintenance-cost)
- [16.28 Production Bugs: to'plamdagi bo'shliqlarning olti nomi](#1628-production-bugs-toplamdagi-boshliqlarning-olti-nomi)
- [16.29 Mystery Guest ning tashqi resurs shakli: In-line Resource va Setup External Resource](#1629-mystery-guest-ning-tashqi-resurs-shakli-in-line-resource-va-setup-external-resource)
- [16.30 Arxitektor nazorat ro'yxati](#1630-arxitektor-nazorat-royxati)

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
| Coverage agenti | Reflektsiya bilan a'zo sanash: `getDeclaredMethods()`, `getDeclaredFields()` | JaCoCo agenti sintetik `$jacocoInit` va `$jacocoData` qo'shadi: tor yurish (agentsiz) yashil, to'liq suite qizil | `isSynthetic()` filtri ([JaCoCo agenti](../sonarqube/09-coverage-qanday-olchanadi-jacoco-mexanikasi.md#92-java-agent-va-offline-instrumentatsiya-farqi)) |

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

```text
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

Surefire bunday testlarni XML hisobotda `flakyFailure` elementi sifatida belgilaydi va bu aynan o'lchash uchun kerakli ma'lumot. Surefire manbasidagi XML parser ikkita shunday elementni biladi, `flakyFailure` va `flakyError`, hamda ular uchun alohida hisoblagich yuritadi (`incrementNumberOfFlakes`). Ya'ni flaky test soni hisobotda tayyor ko'rinishda keladi va uni qo'lda sanash kerak emas: `grep -c flakyFailure` yoki XML ni parse qilish yetadi. Gradle'da `org.gradle.test-retry` plugin'i `maxRetries` va muhim `failOnPassedAfterRetry` opsiyasini beradi. JUnit 5'da standart retry API yo'q: `TestTemplateInvocationContextProvider` asosida custom extension yozish yoki tashqi kutubxona ishlatish kerak; `@RepeatedTest` retry emas, u boshqa maqsadga xizmat qiladi.

Qat'iy qoida: retry yoqilgan bo'lsa, `flakyFailure` soni dashboard'da ko'rsatiladi va u ham nolga intilishi kerak. Retry'ni global yoqib hisobotni o'qimaslik - flake'ni rasman qonuniylashtirish.

## 16.6 Test qarzi (test debt)

Test qarzi - suite'ning kelajakdagi o'zgarishlarni qo'llab-quvvatlash qobiliyatini kamaytiruvchi har qanday holat. Turlari: **eskirgan test** (o'zgargan talabni tekshiradi, lekin mock'lar shunchalik chuqur ki real xatti-harakat ko'rinmaydi); **assertion'siz test** (faqat metodni chaqiradi - mutation testing bunday testlarni darhol ochadi); **abadiy `@Disabled`** (sababi yozilmagan, hech kim tegishga qo'rqadi); **takrorlangan test** (bir ssenariyni uch darajada tekshiradi, qo'shimcha xavf qoplamaydi); **tushunarsiz test** (80 qatorli setup, nomi `test1`).

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

Amaliy ro'yxat: nomlarni biznes tilida yozish (`shouldRejectOrderOverCreditLimit`, `testSubmit` emas); `@DisplayName` bilan ssenariyni to'liq ifodalash; assertion'ni mazmunli qilish (`hasSize(3)` o'rniga `containsExactly(...)`); `assertTrue(x.equals(y))` ni AssertJ'ning tipga xos matcher'lariga o'tkazish - xato xabari ancha ma'lumotli bo'ladi; bir testda bir mantiqiy tasdiq, kerak bo'lsa `assertAll` yoki `SoftAssertions` bilan guruhlash. Test source'lariga ham code review va static analysis qo'llanadi.

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
| General Fixture | Bitta katta umumiy fixture hammaga xizmat qiladi, har biri 10% ini ishlatadi | Ssenariy bo'yicha kichik fixture'lar; `@Nested` ichida lokal setup |

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
3. **Testni past darajaga tushirish.** Eng samarali optimallashtirish - testni piramidaning pastki qatlamiga ko'chirish: E2E'dagi validatsiya ssenariysi → `@WebMvcTest`; integration'dagi hisob-kitob mantiqi → toza unit test. Bitta E2E testni unit testga aylantirish odatda 30-60 sekundni millisekundlarga tushiradi.
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

## 16.13 Smell lar uch qatlami: code, behavior va project smell

Meszaros test smell larini uch qatlamga ajratadi va bu bo'linish tuzatish tartibini belgilaydi. **Code smell** - test kodini o'qiyotgan odam sezadigan narsa: kod to'g'ri ishlaydi, lekin niyatini aytmaydi; uni avval tanib olish kerak va zarurligi hammaga baravar ko'rinmaydi. **Behavior smell** ni e'tiborsiz qoldirish qiyin, chunki u testni eng noqulay paytda yiqitadi yoki kompilyatsiya qilmaydi. **Project smell** ni esa test kodini o'qimaydigan va testlarni yurgizmaydigan odam, ya'ni menejer yoki mijoz sezadi: u loyihaning umumiy sog'ligi ko'rsatkichi (Gerard Meszaros, *xUnit Test Patterns: Refactoring Test Code*, Addison-Wesley, 2007, 2-bob, 10-11-bet).

Muhim nuqta: bu uch qatlam bir vaqtda ko'rinadi. Project smell odatda biror behavior smell ning loyiha darajasidagi alomati, uning ostida esa haqiqiy sabab bo'lgan code smell turadi. Kitob shu sababli ildiz sababini topish uchun "Besh nega" usulini maslahat beradi va ogohlantiradi: bitta qatlamdagi alomatni to'g'ridan-to'g'ri davolashga urinish eng tipik xato (o'sha joy, 11-bet). Shuningdek kitob "sniffability" mezonini kiritadi: narsa smell bo'lishi uchun u o'zini bildirib turishi kerak, aks holda u shunchaki sabab (cause) deb belgilanadi va alohida nom bilan ota-smell ichida yashaydi.

| Qatlam | Kim sezadi | Qachon sezadi | Namuna |
|---|---|---|---|
| Code smell | Dasturchi, review'chi | Test kodini o'qiganda yoki yozganda | Obscure Test, Conditional Test Logic, Test Code Duplication |
| Behavior smell | Dasturchi, CI | Test yurganda yoki kompilyatsiyada | Erratic Test, Fragile Test, Slow Tests, Assertion Roulette |
| Project smell | Menejer, mijoz | Reja va production hodisalaridan | Buggy Tests, High Test Maintenance Cost, Production Bugs |

Amaliy natija: PR review code smell larni ushlaydi, CI dashboard behavior smell larni o'lchaydi, choraklik ko'rib chiqish esa project smell larni ko'radi. Uchtasidan bittasi ham yetarli emas: faqat review bo'lsa flake ko'rinmaydi, faqat dashboard bo'lsa sababi topilmaydi. Shu bobdagi [test smell lar katalogi](#169-test-smelllar-katalogi) qisqa jadval, keyingi bo'limlar esa har ota-smell ning nomlangan sabablarini ochadi.

## 16.14 Erratic Test: tartib va holat orqali o'zaro ta'sir

Erratic Test - behavior smell, uning ta'rifi oddiy: bitta yoki bir nechta test o'zini beqaror tutadi, ba'zan o'tadi, ba'zan yiqiladi. Kitob uni sakkizta nomlangan sababga ajratadi va shu sabablardan beshtasi testlarning o'zaro ta'siriga tegishli (Gerard Meszaros, *xUnit Test Patterns: Refactoring Test Code*, Addison-Wesley, 2007, 16-bob, 228-238-bet).

**Interacting Tests** (229-bet) - yolg'iz ishlaydigan test to'plamga yangi test qo'shilganda, boshqa test yiqilganda yoki test qayta nomlanib tartibi o'zgarganda yiqiladi. Sabab odatda Shared Fixture: testning hayotidan uzoq yashaydigan har qanday narsa o'zaro ta'sirga olib keladi, shu sababli kitob static maydonlardan ham SUT da, ham test infratuzilmasida voz kechishni, Singleton va Registry dan iloji boricha qochishni talab qiladi; ulardan voz kecholmasa, har test boshida static holatni qayta tiklash mexanizmi qo'yiladi (229-230-bet).

**Interacting Test Suites** (231-bet) - testlar alohida to'plamda yashil, birga yurganda qizil: ikki to'plam bir xil resursni yaratmoqchi bo'ladi, birinchisi muvaffaqiyat qozonadi, ikkinchisi yiqiladi.

**Lonely Test** (232-bet) - teskari holat: test to'plam ichida ishlaydi, lekin yolg'iz yurganda ishlamaydi, chunki u boshqa test yoki to'plam darajasidagi setup qoldirgan holatga tayanadi. Yechim - Fresh Fixture ga o'tish yoki testga o'z lazy setup ini qo'shish.

**Unrepeatable Test** (234-bet) - test birinchi yugurishda o'tadi, keyingilarida yiqiladi (yoki teskarisi): u o'zi bilan yugurishlar oralig'ida ta'sirlashadi. Kitob ogohlantiradi: bir nechta bunday test bo'lsa, har yugurishda boshqa test qizil bo'lgandek ko'rinadi va naqsh ko'rinmay qoladi.

**Nondeterministic Test** (237-bet) - faqat bitta runner ishlayotganda ham natija har safar boshqacha: sabab har yugurishda boshqa qiymat ishlatilishi. Kitob buni debug qilish eng ko'p vaqt oladigan holat deb belgilaydi, lekin sabab aniqlangandan keyin tasodifiy qiymatni muammo keltirgan qiymat bilan almashtirish oson ekanini aytadi.

```java
@Test
@Order(0) // tartibni ataylab e'lon qilish: Lonely Test ni ko'rinadigan qiladi
void failsWhenRunAlone() {
    // Agar bu test yolg'iz yurganda yiqilsa, u Shared Fixture ga tayanadi
    assertThat(orderRepository.count()).isPositive();
}
```

Diagnostika qoidasi: `MethodOrderer.Random` va `ClassOrderer.Random` bilan nightly yugurish, keyin har bir qizil testni yolg'iz yurgizish. To'plamda qizil, yolg'iz yashil - Interacting Tests; to'plamda yashil, yolg'iz qizil - Lonely Test. Mexanik sabablar va ularning Java/Spring ko'rinishlari [flaky testning asosiy sabablari](#162-flaky-testning-asosiy-sabablari-misollar-va-yechimlari) jadvalida.

Interacting Tests ning printsipial yechimi umumiy fixture dan voz kechish emas, uni ataylab o'zgarmas qilish. Meszaros Shared Fixture ning shu variantini Immutable Shared Fixture deb ataydi: fixture ikki mantiqiy qismga bo'linadi - har bir testga kerak, lekin hech bir test o'zgartirmaydigan qism (odatda reference ma'lumot) va har bir test o'zi quradigan, o'zgartiradigan yoki o'chiradigan qism (Fresh Fixture). Eng qiyin joyi nimani "o'zgarish" deb hisoblash: kitobning kalit mezoni - agar biror test boshqa test qilgan ishni o'zgarmas fixture dagi obyektning o'zgarishi deb sezsa, o'sha o'zgarish fixture ni baham ko'radigan hech bir testda ruxsat etilmaydi (Meszaros, *xUnit Test Patterns*, Addison-Wesley, 2007, 18-bob, 323-bet). Spring da bu mezon to'g'ridan-to'g'ri `TestContext` cache i va `static` Testcontainers konteyneriga tegishli: ikkisi ham umumiy fixture, shuning uchun ularda yashaydigan ma'lumot faqat o'qish uchun bo'lsa, testlarning bir-biriga ta'siri printsipial ravishda imkonsiz bo'ladi. To'rt strategiyaning tanlov jadvali [fixture strategiyalari](10-test-malumotlarini-boshqarish.md#102-fixture-strategiyalari) bo'limida.

## 16.15 Test Run War, Resource Leakage va Resource Optimism

Erratic Test ning qolgan uch sababi muhit va resurslarga tegishli, shuning uchun ular arxitektura qarori bilan yopiladi, test kodini tuzatish bilan emas (Gerard Meszaros, *xUnit Test Patterns: Refactoring Test Code*, Addison-Wesley, 2007, 16-bob, 233-bet va 235-236-bet).

**Test Run War** (235-bet) - bir necha odam bir vaqtda testlarni yurgizganda xatolar tasodifiy chiqadi. Alomat aniq: bitta odam nuqtai nazaridan test "ba'zan" yiqiladi, lekin sabab umumiy tashqi resurs, odatda umumiy baza. Bu eng oson tanib olinadigan smell, chunki u kun ichida, release oldidan va jamoa kattalashganda kuchayadi. Yechim test kodida emas: har dasturchi va har CI yugurishi uchun alohida [baza qumloqi](../patterns/23-testing-patternlari.md#2378-baza-qumloqi-database-sandbox) beriladi, ya'ni umumiy dev yoki staging bazasi test maqsadida ishlatilmaydi.

**Resource Leakage** (233-bet) - testlar yoki SUT cheklangan resursni (ulanish, fayl deskriptori, thread, konteyner) olib qo'yib yubormaydi. Alomat xarakterli: to'plam asta-sekin sekinlashadi yoki birdan yiqila boshlaydi, runner yoki bazani qayta ishga tushirish muammoni vaqtincha hal qiladi, keyin u qaytadi. Kitob juda amaliy maslahat beradi: barcha resurs pool larining hajmini 1 ga tushirib qo'ying, shunda oqishni qiladigan test ancha tez yiqiladi va topish osonlashadi (233-bet).

**Resource Optimism** (233-bet) - test o'z muhitida mavjud bo'lgan tashqi resursga tayanadi va boshqa muhitda u yo'q. Alomat: test bir muhitda o'tadi, boshqasida yiqiladi. Bu Context Sensitivity ning yaqin qarindoshi va germetik test talabini buzishdir.

```properties
# Oqishni tez ushlash uchun test profilida pool ni 1 ga tushirish
spring.datasource.hikari.maximum-pool-size=1
spring.datasource.hikari.leak-detection-threshold=2000
```

HikariCP ning `leakDetectionThreshold` sozlamasi ochilib qolgan ulanishni log ga yozadi, `maximum-pool-size=1` esa oqishni darhol ko'rinadigan qiladi: keyingi test ulanish kuta boshlaydi va timeout bilan yiqiladi. Konteyner va fayl resurslari uchun bu rolni [tozalashning uch shakli](../patterns/23-testing-patternlari.md#2371-tozalashning-uch-shakli-garbage-collected--in-line--implicit-teardown) bo'limidagi avtomatik tozalash mexanizmlari bajaradi.

## 16.16 Fragile Test va to'rt sezgirlik

Fragile Test - test SUT ning u tekshirmaydigan qismi o'zgarganda kompilyatsiya qilmaydi yoki yiqiladi. Kitob uning sabablarini "to'rt sezgirlik" deb nomlaydi (Gerard Meszaros, *xUnit Test Patterns: Refactoring Test Code*, Addison-Wesley, 2007, 16-bob, 239-247-bet).

**Interface Sensitivity** (241-bet) - SUT interfeysining test ishlatadigan qismi o'zgarganda test kompilyatsiya qilmaydi. Java kabi statik tipli tilda bu kompilyatsiya xatosi bo'lib chiqadi, ya'ni eng arzon sezgirlik: xato joyi darhol ko'rinadi. Kitob interfeys faqat tashkilot ichida va testlar tomonidan ishlatilsa eng yaxshi yechim SUT API ni test utility metod ortiga yashirish deb yozadi.

**Behavior Sensitivity** (242-bet) - SUT xatti-harakati o'zgarganda boshqa testlar yiqiladi. Bu avtomatik ravishda smell emas: regressiya testining butun maqsadi shu. U smell bo'ladi faqat uch holatda: testlar fixture qurish uchun ishlatadigan funksionallik o'zgarsa, natijani tekshirish uchun ishlatadigan funksionallik o'zgarsa, yoki tozalash kodi o'zgarsa. Yechim - fixture haqidagi taxminlarni Creation Method ortiga, natija haqidagi taxminlarni custom assertion ortiga yashirish.

**Data Sensitivity** (243-bet) - test ishlatadigan ma'lumot o'zgarganda test yiqiladi: bazaga yozuv qo'shildi, yozuv o'zgartirildi yoki o'chirildi, Standard Fixture ni quradigan kod tuzatildi. Kitob aniq aytadi: bu holat faqat Standard Fixture ishlatilganda yuzaga keladi.

**Context Sensitivity** (245-bet) - SUT ishlayotgan kontekstning holati yoki xatti-harakati o'zgarganda test yiqiladi: vaqt va sanaga bog'liqlik yoki SUT tayanadigan boshqa tizim xatti-harakatining o'zgarishi. Kitob asosiy sababni dizaynda ko'radi: qaysi SUT tekshirilayotgani aniq bo'lmasa, unit test juda ko'p kodni qamrab oladi va kontekstga sezgir bo'lib qoladi.

| Sezgirlik | Alomat | Birinchi chora |
|---|---|---|
| Interface | Kompilyatsiya xatosi | SUT API ni test utility metod ortiga yashirish |
| Behavior | Fixture yoki tekshirish mantiqi buzildi | Creation Method va custom assertion |
| Data | Baza ma'lumoti o'zgardi | Standard Fixture dan [minimal fixture](../patterns/23-testing-patternlari.md#2370-minimal-va-standart-fixture-minimal-fixture--standard-fixture) ga o'tish |
| Context | Vaqt, tashqi tizim yoki qo'shni kod | [Clock injection](../patterns/23-testing-patternlari.md#2330-clock-injection-clock-injection), SUT chegarasini kichraytirish |

## 16.17 Overspecified Software, Sensitive Equality va Fragile Fixture

Fragile Test ning qolgan uch sababi mocking va taqqoslash uslubidan kelib chiqadi (Gerard Meszaros, *xUnit Test Patterns: Refactoring Test Code*, Addison-Wesley, 2007, 16-bob, 246-bet).

**Overspecified Software** (246-bet, taxallusi Overcoupled Test) - test dasturiy ta'minot qanday tuzilishi yoki qanday ishlashi haqida juda ko'p narsa aytadi. Kitob uni Behavior Sensitivity ning bir shakli deb belgilaydi va behavior verification uslubi bilan, ya'ni mock obyektlarni qatlam kesib o'tuvchi testlar qurish uchun keng ishlatish bilan bog'laydi. Asosiy muammo: test nima erishilishi kerakligini emas, qanday qilinishi kerakligini tasvirlaydi, shuning uchun u faqat ma'lum bir implementatsiya bilan o'tadi. Kitobning yechimi - "Use the Front Door First" principi, ya'ni iloji boricha SUT ning asosiy interfeysi orqali ishlash.

**Sensitive Equality** (246-bet) - tekshiriladigan obyektlar satrga aylantirilib, kutilgan satr bilan taqqoslanadi. Kitob buni ikki tomondan izohlaydi: bu Behavior Sensitivity, chunki test o'zi tekshirmayotgan xatti-harakatga (ya'ni `toString` ga) sezgir; shu bilan birga bu Interface Sensitivity ham, chunki interfeys semantikasi o'zgargan. Xulosa qat'iy: obyektni tekshirish uchun uning satr ko'rinishini ishlatish muammo chaqirishdan boshqa narsa emas.

**Fragile Fixture** (246-bet) - Standard Fixture yangi test uchun o'zgartirilganda bir nechta boshqa test yiqiladi. Kitob buni mustaqil sabab emas, Data Sensitivity yoki Context Sensitivity ning taxallusi deb belgilaydi.

```java
// Sensitive Equality: toString formatiga bog'langan test
assertThat(order.toString()).isEqualTo("Order[id=1, total=1500.00 UZS]");

// Maydon bo'yicha taqqoslash: toString o'zgarsa test yiqilmaydi
assertThat(order)
        .extracting(Order::id, Order::total)
        .containsExactly(1L, Money.of("1500.00", "UZS"));
```

Mock ni qancha ishlatish kerakligi va holat bilan xulqni tekshirish o'rtasidagi tanlov [holatni va xulqni tekshirish](../patterns/23-testing-patternlari.md#2367-holatni-va-xulqni-tekshirish-state-verification--behavior-verification) bo'limida; tashqi servisni almashtirish variantlari ierarxiyasi esa [tashqi servislarni taqlid qilish](09-tashqi-servislarni-taqlid-qilish-va.md#91-muammo-va-yechim-variantlari-ierarxiyasi) bobida.

## 16.18 Slow Tests ning to'rt nomlangan sababi

Slow Tests ning o'zi behavior smell, lekin kitob uni to'rt nomlangan sababga ajratadi va har biri boshqa chora talab qiladi (Gerard Meszaros, *xUnit Test Patterns: Refactoring Test Code*, Addison-Wesley, 2007, 16-bob, 253-257-bet).

**Slow Component Usage** (254-bet) - SUT ning biror komponenti sekin. Kitob eng keng tarqalgan sababni aniq ko'rsatadi: ko'p testda baza bilan ishlash. Chora - sekin komponentni deyarli bir zumda javob beradigan test dublyori bilan almashtirish, baza holatida esa fake baza bilan.

**General Fixture** (255-bet) - har test bir xil ortiqcha qurilgan fixture ni qayta quradi. Fresh Fixture har test uchun yangi nusxa yaratgani uchun sekinlashish test soniga ko'paytiriladi. Kitob birinchi o'ylanadigan yechimni (General Fixture ni Shared Fixture qilish) ataylab rad etadi: agar uni o'zgarmas qilib bo'lmasa, bu Erratic Test ga olib keladi; to'g'ri yechim - har testning fixture hajmini kamaytirish.

**Asynchronous Test** (255-bet) - bir nechta test nomutanosib uzoq yuradi, chunki ularda oshkora kutish bor. Sabab: SUT thread yoki process ochadi, test esa ularning ishga tushib tugashini kutishi kerak; vaqt o'zgaruvchan bo'lgani uchun test "har holda" uzun kutish qo'yadi.

**Too Many Tests** (256-bet) - testlar shunchalik ko'p, qanchalik tez bajarilsa ham umumiy vaqt uzun. Kitobning yechimi: hamma testni har doim yurgizish shart emas, lekin hamma test muntazam yurishi shart. Mos ko'ndalang kesim bilan kichik to'plam yasalib, u har commit oldidan yuriladi, qolgani esa tunda yoki boshqa qulay vaqtda; kitob buni ba'zilar "build pipeline" deb atashini qayd etadi.

| Sabab | Alomat | Chora |
|---|---|---|
| Slow Component Usage | Ko'p test bazaga yoki tashqi tizimga uriladi | Test dublyori, in-memory fake, pastki qatlamga ko'chirish |
| General Fixture | Hamma test sekin, fixture qurish uzun | Fixture hajmini kamaytirish, Shared Fixture ga qochmaslik |
| Asynchronous Test | Bir nechta test nomutanosib uzun | `Awaitility`, deterministik `TaskExecutor`, Humble Object |
| Too Many Tests | Umumiy vaqt uzun, har test tez | Commit oldi kichik to'plam, qolgani nightly |

Java va Spring tomonidagi aniq o'lchov va optimallashtirish usullari [sekin testlarni tezlashtirish](#1610-sekin-testlarni-tezlashtirish) bo'limida; bosqichlash siyosati esa CI pipeline bobida.

## 16.19 Frequent Debugging: defekt lokalizatsiyasining yo'qligi

Frequent Debugging (taxallusi Manual Debugging) - test yiqilishlarining ko'pchiligida sababni topish uchun debugger ishga solinadi yoki kodga print qo'yiladi. Kitob buni bitta holat uchun muammo deb hisoblamaydi: smell faqat bu odat bo'lganda paydo bo'ladi (Gerard Meszaros, *xUnit Test Patterns: Refactoring Test Code*, Addison-Wesley, 2007, 16-bob, 248-249-bet).

Sabab - to'plamda defekt lokalizatsiyasi yo'q: yiqilgan testlar nima buzilganini o'z xabari yoki yiqilishlar naqshi bilan aytishi kerak. Kitob ikki bo'shliqni ko'rsatadi. Birinchisi - alohida sinf ichidagi mantiq xatosini ko'rsatadigan batafsil unit testlarning yo'qligi. Ikkinchisi - bir guruh sinf orasidagi integratsiya xatosini ko'rsatadigan component testlarning yo'qligi; bu aynan mock obyektlar keng ishlatilib, ammo mock programlangan xatti-harakat bilan real bog'liqlikning unit testlari mos kelmaganda yuzaga keladi. Uchinchi sabab ham bor: kam yurgizilgan testlar. Testlar har kichik o'zgarishdan keyin yurgizilsa, nimani o'zgartirganingiz yodda bo'ladi va qizil test sababini qidirish kerak bo'lmaydi.

```java
// Defekt lokalizatsiyasi: xabar nima buzilganini aytadi
assertThat(invoice.vat())
        .as("QQS summasi net dan 12 foiz hisoblanadi")
        .isEqualByComparingTo("54.00");
```

Amaliy diagnostika: bir sprint davomida har debug sessiyasidan keyin "qanday avtomatik test bu sessiyani keraksiz qilardi" degan savolga yozma javob bering va shu testni yozing. Agar javob doimo "unit test" bo'lsa, piramida yuqoriga og'gan; javob doimo "component test" bo'lsa, mock lar real xatti-harakatdan chetga chiqqan va kontrakt testi kerak. Assertion xabarining mexanikasi [assertion metodi va assertion xabari](../patterns/23-testing-patternlari.md#2365-assertion-metodi-va-assertion-xabari-assertion-method--assertion-message) bo'limida.

## 16.20 Manual Intervention: testni odam ushlab turadigan joylar

Manual Intervention - test har yugurishda odamning qo'l aralashuvini talab qiladi. Kitob uch nomlangan sababni ajratadi (Gerard Meszaros, *xUnit Test Patterns: Refactoring Test Code*, Addison-Wesley, 2007, 16-bob, 250-252-bet).

**Manual Fixture Setup** (250-bet) - odam testlardan oldin muhitni qo'lda tayyorlaydi: serverni sozlaydi, process ishga tushiradi yoki fixture yasash skriptini yurgizadi. Sabab ikki xil: fixture qurishni avtomatlashtirishga e'tibor berilmagan, yoki SUT komponentlari shunchalik qattiq bog'langan ki, tizimning katta qismini ishlab chiqish muhitida yurgizib bo'lmaydi. Ikkinchi holda yechim test emas, dizayn: SUT ni qo'lda qilinadigan qadamlardan ajratish kerak.

**Manual Result Verification** (251-bet) - testlar yuriladi, lekin deyarli har doim yashil, hatto SUT noto'g'ri natija qaytarayotganini bilganda ham. Sabab: test o'zini o'zi tekshirmaydi, shuning uchun u faqat istisno chiqqanda yiqiladi. Bu eng xavfli shakl, chunki u yolg'on xotirjamlik beradi.

**Manual Event Injection** (251-bet) - test bajarilishi davomida odam biror harakat qilishi kerak: tarmoq kabelini uzish, baza ulanishini tushirish, interfeysdagi tugmani bosish. Kitob ta'sirini aniq yozadi: bu testni yurgizish kuchini oshiradi va testni nazoratsiz yurgizishni imkonsiz qiladi, ya'ni to'liq avtomatik build va test tsiklini yo'q qiladi.

```java
// Manual Event Injection o'rniga: nosozlikni kod bilan yasash
@Test
void opensCircuitAfterRepeatedTimeouts() {
    wireMock.stubFor(get("/rates").willReturn(aResponse().withFixedDelay(5_000)));
    for (int i = 0; i < 5; i++) {
        assertThatThrownBy(() -> rateClient.fetch("USD")).isInstanceOf(CallNotPermittedException.class);
    }
}
```

Nosozlikni qo'lda yasash o'rniga uni dublyor darajasida programlash kerak: kechikish, 500 javob, ulanishni yopish WireMock va Testcontainers imkoniyatlari bilan kod ichidan beriladi. Konteynerni to'xtatib va qayta ko'tarib tarmoq nosozligini ham avtomatlashtirish mumkin. Qo'lda bajariladigan qadam qolsa, u test emas, qo'llanma: uni test to'plamidan chiqarib, alohida hujjatlashtirish to'g'ri.

## 16.21 Assertion Roulette va Missing Assertion Message

Assertion Roulette - bitta test metodidagi bir nechta tasdiqdan qaysi biri yiqilganini aytish qiyin. Kitob ikki nomlangan sababni ajratadi (Gerard Meszaros, *xUnit Test Patterns: Refactoring Test Code*, Addison-Wesley, 2007, 16-bob, 224-227-bet).

**Eager Test** (224-bet) - bitta test juda ko'p funksionallikni tekshiradi: SUT ning bir nechta metodi chaqiriladi yoki bir metod fixture qurish va tasdiqlar bilan aralashtirilib bir necha marta chaqiriladi. Natijada qizil bo'lganda testning qaysi qismi buzilgani ko'rinmaydi.

**Missing Assertion Message** (226-bet) - test yiqiladi, runner chiqishidan esa qaysi tasdiq yiqilganini aniqlab bo'lmaydi. Sabab: bir xil yoki umuman yo'q xabar bilan chaqirilgan tasdiq metodlari. Kitob buni ayniqsa komandalar satri runner i yoki tahrirlovchiga integratsiyalanmagan runner bilan ishlaganda keskin deb belgilaydi va amaliy qoida beradi: bir xil turdagi tasdiq metodidan birdan ko'p chaqiruv bo'lsa, hech bo'lmaganda minimal xabar qo'shiladi (226-bet).

```java
// Assertion Roulette: uch bir xil tasdiq, xabarsiz
assertEquals(expected.customerId(), actual.customerId());
assertEquals(expected.productId(), actual.productId());
assertEquals(expected.quantity(), actual.quantity());

// AssertJ bilan: bitta tasdiq, maydon nomlari xabarda
assertThat(actual)
        .usingRecursiveComparison()
        .comparingOnlyFields("customerId", "productId", "quantity")
        .isEqualTo(expected);
```

Modern IDE va `assertAll` bu smell ni yumshatadi, lekin yo'q qilmaydi: CI log ida IDE integratsiyasi yo'q va stack trace qatori odatda yetarli emas. Shuning uchun qoida ikki qismli: tasdiq sonini kamaytirish (Eager Test ga qarshi) va qolganlariga `as("...")` qo'yish (Missing Assertion Message ga qarshi).

## 16.22 Conditional Test Logic ning besh sababi

Conditional Test Logic (taxallusi Indented Test Code) - testda bajarilishi ham, bajarilmasligi ham mumkin bo'lgan kod bor. Kitob besh nomlangan sababni ajratadi (Gerard Meszaros, *xUnit Test Patterns: Refactoring Test Code*, Addison-Wesley, 2007, 15-bob, 200-208-bet).

**Flexible Test** (202-bet) - test qachon yoki qayerda yurganiga qarab boshqa funksionallikni tekshiradi: odatda u tashqi omilga qarab kutilgan natijaning turli variantlarini quradi. Tipik namuna - joriy vaqtni olib, SUT chiqishi qanday bo'lishi kerakligini hisoblash.

**Conditional Verification Logic** (203-bet) - shart va tsikl natijani tekshirish uchun ishlatiladi: SUT kerakli obyektni qaytarmasa tasdiqlar bajarilmasligi uchun shart qo'yiladi, yoki kolleksiya ichidagini tekshirish uchun tsikl yoziladi. Natijada SUT hech narsa qaytarmasa test jim o'tadi.

**Production Logic in Test** (204-bet) - testning natijani tekshirish qismida kutilgan qiymat SUT ning mantiqini takrorlab hisoblanadi: test endi hech narsa tekshirmaydi, chunki ikki tomon bir xil formuladan chiqadi.

**Complex Teardown** (206-bet) - murakkab tozalash kodi o'zidan keyin to'g'ri tozalamay, muhitni buzib qoldirish ehtimoli yuqori; bunday kodning to'g'ri yozilganini tekshirish qiyin va u keyinchalik sababsiz yiqiladigan testlarga olib keladigan "ma'lumot oqishi" yasaydi.

**Multiple Test Conditions** (207-bet) - test bir xil mantiqni ko'p kirish to'plamiga qo'llashga urinadi va buni tsikl bilan qiladi; natijada birinchi yiqilish qolganlarini to'sadi.

```java
// Multiple Test Conditions: tsikl o'rniga parametrlangan test
@ParameterizedTest
@CsvSource({"1, 2, 3", "2, 3, 5", "3, 4, 7"})
void addsTwoNumbers(int a, int b, int expected) {
    assertThat(calculator.add(a, b)).isEqualTo(expected);
}
```

Spring va JUnit 5 kontekstida chora aniq: tsikl o'rniga `@ParameterizedTest` va [ma'lumotga asoslangan test](../patterns/23-testing-patternlari.md#2383-malumotga-asoslangan-test-data-driven-test); shart o'rniga guard assertion yoki shoxni alohida testga ajratish; murakkab tozalash o'rniga tranzaksiya rollback i yoki `@TempDir`; vaqtga qarab shoxlanish o'rniga [Clock injection](../patterns/23-testing-patternlari.md#2330-clock-injection-clock-injection). Kutilgan qiymat esa SUT formulasidan mustaqil yo'l bilan olinadi, bu [test qiymatlari](../patterns/23-testing-patternlari.md#2381-test-qiymatlari-literal-hosila-va-generatsiya-literal-value--derived-value--generated-value) bo'limida ko'rsatilgan.

## 16.23 Obscure Test ning olti sababi

Obscure Test taxalluslari Verbose Test, Complex Test va Long Test; ta'rifi - testni bir qarashda tushunish qiyin. Kitob olti nomlangan sababni sanaydi (Gerard Meszaros, *xUnit Test Patterns: Refactoring Test Code*, Addison-Wesley, 2007, 15-bob, 186-199-bet).

**Mystery Guest** (188-bet) - o'quvchi fixture va tekshirish mantiqi orasidagi sabab-natija aloqasini ko'rmaydi, chunki uning bir qismi test metodidan tashqarida bajarilgan. Fixture qurish yoki natijani tekshirish testda ko'rinmaydigan ma'lumotga tayansa, o'quvchi avval tashqi ma'lumotni topib o'qishi kerak bo'ladi.

**General Fixture** (190-bet) - test kerakli funksionallikni tekshirish uchun zarur bo'lganidan kattaroq fixture quradi yoki unga murojaat qiladi; natijada fixture, SUT ning ishlatilgan qismi va kutilgan natija orasidagi aloqa tushunarsiz bo'ladi.

**Irrelevant Information** (192-bet) - test fixture haqida ko'p keraksiz tafsilot ochadi va o'quvchi qaysi qiymat natijaga ta'sir qilishini ajratib ololmaydi.

**Hard-Coded Test Data** (194-bet) - fixture, tasdiqlar yoki SUT argumentlaridagi qiymatlar test metodiga qattiq yozilgan va kirish bilan kutilgan chiqish orasidagi aloqa ko'rinmaydi. Kitob bu sababning Erratic Test ga ham olib kelishini qayd etadi.

**Indirect Testing** (196-bet) - test metodi SUT bilan boshqa obyekt orqali ishlaydi va o'zaro ta'sir murakkablashadi; biznes mantiqini taqdimot qatlami orqali tekshirish eng keng tarqalgan namuna.

**Eager Test** (186-bet, bu smell ichida ham sabab) - bitta test metodida juda ko'p funksionallik tekshiriladi va qaysi qism fixture qurish, qaysi qism SUT ni ishlatish ekani ko'rinmaydi.

| Sabab | Birinchi chora |
|---|---|
| Mystery Guest | Fixture ni test ichida yaratish, builder bilan |
| General Fixture | Ssenariy bo'yicha kichik fixture, `@Nested` ichida lokal setup |
| Irrelevant Information | Faqat natijaga ta'sir qiladigan qiymatni ko'rsatish |
| Hard-Coded Test Data | Nomlangan doimiy yoki hosila qiymat |
| Indirect Testing | SUT ni to'g'ridan-to'g'ri test qilish, qatlamni pastga tushirish |
| Eager Test | Har xatti-harakatga alohida test |

Sozlash mantiqini qayerga qo'yish bo'yicha tanlov mezoni [fixture sozlashning uch shakli](../patterns/23-testing-patternlari.md#2368-fixture-sozlashning-uch-shakli-in-line-setup--delegated-setup--implicit-setup) bo'limida; qayta ishlatiladigan yordamchi kod uchun [test utility metodi va test helper](../patterns/23-testing-patternlari.md#2375-test-utility-metodi-va-test-helper-test-utility-method--test-helper).

## 16.24 Hard-to-Test Code: testlash qiyinligi dizayn muammosi

Hard-to-Test Code - code smell, lekin uning ildizi test kodida emas, SUT dizaynida. Taxallusi Hard-Coded Dependency. Kitob to'rt nomlangan sababni ajratadi (Gerard Meszaros, *xUnit Test Patterns: Refactoring Test Code*, Addison-Wesley, 2007, 15-bob, 209-212-bet).

**Highly Coupled Code** (210-bet) - sinfni bir necha boshqa sinfni ham test qilmasdan test qilib bo'lmaydi, chunki u yakka holda bajarilmaydi. Kitob sabablar ro'yxatini beradi: yomon dizayn, obyektga yo'naltirilgan dizayn tajribasining yetishmasligi va bog'liqlikni kamaytirishni rag'batlantirmaydigan mukofot tizimi. Yechim - bog'lanishni uzish; test dublyori, aniqrog'i test stub yoki mock obyekt bunda asosiy vosita.

**Asynchronous Code** (210-bet) - sinfni to'g'ridan-to'g'ri metod chaqiruvi bilan test qilib bo'lmaydi: test thread, process yoki ilovani ishga tushirib, start tugashini kutishi kerak. Ta'siri ikki qirrali: testlar murakkablashadi va ancha uzoq yuradi, bu esa tez yurishi shart bo'lgan unit testlar uchun asosiy muammo. Ildiz sabab - algoritm kodi u bajariladigan aktiv obyektga qattiq bog'langan; yechim esa mantiqni asinxron murojaat mexanizmidan ajratish, ya'ni Humble Object.

**Untestable Test Code** (211-bet) - test metodining tanasi shunchalik tushunarsiz yoki shunchalik ko'p shart mantiqiga ega ki, testning o'zi to'g'rimi degan savol paydo bo'ladi. Kitob ta'sirini aniq yozadi: test metodidagi har qanday shart mantiqi Buggy Tests ehtimolini oshiradi va yuqori test saqlash narxiga olib keladi.

**Hard-Coded Dependency** (210-bet) - taxallus sifatida belgilangan: bog'liqlik sinf nomi bilan kodga yozilgan va almashtirilmaydi.

```java
// Hard-Coded Dependency: almashtirilmaydi
public class OrderService {
    private final RateClient rates = new HttpRateClient("https://rates.example.com");
}

// Konstruktor injection: bog'liqlik testda almashtiriladi
public class OrderService {
    private final RateClient rates;
    public OrderService(RateClient rates) { this.rates = rates; }
}
```

Legacy kodga test qo'shish alohida mavzu va kitob bu yerda Michael Feathers ning kitobiga havola qiladi. Qiyin test qilinadigan kodni ochishning vositalari bu hujjatda [testga xos subklass](../patterns/23-testing-patternlari.md#2374-testga-xos-subklass-test-specific-subclass) va Humble Object bo'limlarida; rollar bo'yicha javobgarlik esa [rollar ta'rifi va farqi](03-kim-nima-yozadi-rollar-va-masuliyat.md#31-rollar-tarifi-va-farqi) bo'limida.

## 16.25 Test Code Duplication: ko'chirish va g'ildirakni qayta ixtiro qilish

Test Code Duplication - bir xil test kodi ko'p marta takrorlangan. Kitob ikki nomlangan sababni ajratadi va ularning texnik yechimi bir xil, jarayon yechimi esa boshqa (Gerard Meszaros, *xUnit Test Patterns: Refactoring Test Code*, Addison-Wesley, 2007, 15-bob, 213-216-bet).

**Cut-and-Paste Code Reuse** (214-bet) - nusxa ko'chirish kodni tez yozishning kuchli vositasi, lekin natijada bir xil kodning ko'p nusxasi paydo bo'ladi va har biri parallel ravishda saqlanishi kerak. Kitob sababni dasturchining fokusida ko'radi: "qanday qilish" tafsilotiga qaragan odam bir xil kodni ko'p marta yozadi, chunki umumiy manzarani, ya'ni testning niyatini ko'rmaydi yoki ko'rishga vaqt ajratmaydi. Qo'shimcha omil - refaktoring ko'nikmasi va tajribasining yetishmasligi.

**Reinventing the Wheel** (215-bet) - Cut-and-Paste ataylab nusxa yasasa, bu sabab tasodifan bir xil operatorlar ketma-ketligini turli testlarda yozishdan kelib chiqadi. Ildiz sabab - qaysi test utility metodlar mavjudligini bilmaslik; qo'shimcha omil - boshqalar yozgan kodni qayta ishlatishdan ko'ra o'zi yozishga moyillik. Texnik yechim bir xil, lekin jarayon yechimi boshqacha: test avtomatlashtiruvchi yangi kod yozishdan oldin mavjud utility metodlarni ko'proq joydan qidirishi kerak.

```java
// Takrorlangan tekshiruv maxsus AssertJ assertion ga ko'chiriladi
public final class OrderAssert extends AbstractAssert<OrderAssert, Order> {
    private OrderAssert(Order actual) { super(actual, OrderAssert.class); }

    public static OrderAssert assertThatOrder(Order actual) { return new OrderAssert(actual); }

    public OrderAssert isPaidWithTotal(String total) {
        isNotNull();
        assertThat(actual.status()).as("status").isEqualTo(OrderStatus.PAID);
        assertThat(actual.total()).as("total").isEqualByComparingTo(total);
        return this;
    }
}
```

Jarayon tomoni review da hal qiladi: "bu tekshiruvni qayerda ko'rgandik" savolini review checklist iga kiritish va test helper larni mavzu bo'yicha nomlab, topilishi oson joyda saqlash. Takrorlanishga qarshi vositalar ro'yxati va balans qoidasi [test kodini refaktoring qilish](#168-test-kodini-refaktoring-qilish) bo'limida: testda bir oz takrorlanish aytilgan sabablarga ko'ra foydali.

## 16.26 Test Logic in Production: test mantiqining production ga oqib o'tishi

Test Logic in Production - production ga chiqadigan kodda faqat test paytida bajarilishi kerak bo'lgan mantiq bor. Kitob to'rt nomlangan sababni ajratadi (Gerard Meszaros, *xUnit Test Patterns: Refactoring Test Code*, Addison-Wesley, 2007, 15-bob, 217-222-bet).

**Test Hook** (217-bet) - SUT ichidagi shart "haqiqiy" kod yoki test uchun maxsus mantiq bajarilishini belgilaydi, ya'ni kodda `if (testing) { ... } else { ... }` shaklidagi bo'laklar paydo bo'ladi. Kitob alomatini ehtiyotkorlik bilan yozadi: xulqiy alomat umuman bo'lmasligi ham mumkin, yoki muammo production da chiqadi.

**For Tests Only** (219-bet) - SUT da kod faqat testlar uchun mavjud: ayrim metodlar faqat testdan chaqiriladi, ayrim maydonlar `private` bo'lishi kerakligida `public` qilingan. Ta'siri: SUT murakkablashadi, interfeysning potensial iste'molchilari chalg'iydi, bu metodlar esa faqat juda tor sharoitda tekshirilgani uchun odatiy ishlatishda ishlamasligi mumkin.

**Test Dependency in Production** (220-bet) - production bajariladigan artefakt test artefaktiga bog'liq: production kodini yolg'iz build qilib bo'lmaydi yoki test artefaktlari bo'lmasa u ishlamaydi.

**Equality Pollution** (221-bet) - testga xos tenglik SUT ning `equals` metodiga yoziladi. Kitob alomatini aniq ko'rsatadi: diqqatga sazovor narsa shundaki, SUT ga `equals` umuman kerak emas edi; keyinchalik `equals` yangi talab bilan o'zgarganda testlar yiqiladi yoki biznes talabiga zid tenglik qolib ketadi. Ildiz sabab - testga xos tenglik tushunchasini bilmaslik.

```java
// For Tests Only o'rniga: tekshirish uchun domen metodi
public class Order {
    // public void setStatusForTest(OrderStatus s) { ... }  // test uchun ochilgan setter
    public boolean isPayable() { return status == OrderStatus.NEW && total.isPositive(); }
}
```

Spring kontekstida eng tipik ko'rinishlar: production profilida ham o'qiladigan `app.test-mode` flag i, `src/main` ichida qolgan mock implementatsiya, `src/main` dagi sinfning `spring-boot-starter-test` ga bog'liqligi. Chora: test uchun kerakli kirish nuqtalarini [testga xos subklass](../patterns/23-testing-patternlari.md#2374-testga-xos-subklass-test-specific-subclass) yoki test dublyori orqali berish, `equals` ni esa domen talabiga ko'ra yozib, taqqoslashni AssertJ ning maydon bo'yicha taqqoslashiga qoldirish. Build darajasida tekshirish oson: `src/main` dan test kutubxonalariga bog'liqlikni arxitektura testi bilan taqiqlash.

## 16.27 Buggy Tests va High Test Maintenance Cost

Bu ikki project smell bir xil ildizlarga ega va ularni menejer sezadi, kodni o'qimay (Gerard Meszaros, *xUnit Test Patterns: Refactoring Test Code*, Addison-Wesley, 2007, 17-bob, 260-267-bet).

**Buggy Tests** (260-bet) - avtomatik testlarda muntazam bug topiladi. Alomatlari ikki tomonli: build yiqiladi, aybdor test deb ko'rsatiladi, lekin tekshirganda test qilinayotgan kod to'g'ri ishlaydi; yoki production da bug chiqadi, garchi aynan shu ssenariyni tekshiradigan test bor edi, va sabab tahlili testda bug borligini ko'rsatadi. Kitob ta'sirini keskin yozadi: yolg'on natija beradigan testlar xavfli. Kerak bo'lmaganda o'tadigan test yolg'on xotirjamlik beradi, kerak bo'lmaganda yiqiladigan test esa testlarga ishonchni yo'q qiladi - bir necha marta shunday bo'lgandan keyin jamoa ularni e'tiborsiz qoldiradi.

**High Test Maintenance Cost** (265-bet) - mavjud testlarni saqlashga juda ko'p kuch ketadi. Alomati ijtimoiy: jamoa unumdorligi sezilarli pasayadi va dasturchilar testlarni to'plamdan olib tashlashni talab qila boshlaydi. Kitob muhim kuzatuvni yozadi: production kodini yozish majburiy, testlarni saqlash esa bilmagan odam uchun butunlay ixtiyoriy ko'rinadi; agar bu muammo bilan hech narsa qilinmasa, jamoa yoki rahbariyat "test avtomatlashtirish ishlamaydi" degan qarorga keladi va butun ish behuda ketadi.

Ikkisining ham sabablari bir xil uchlik: Fragile Test (to'rt sezgirlik orqali), Obscure Test va Hard-to-Test Code. Kitob High Test Maintenance Cost ning ildiz sababini esa test avtomatlashtirish principlariga e'tibor bermaslikda, yaqin sababini ortiqcha Test Code Duplication va SUT API ga juda qattiq bog'langan testlarda ko'radi (266-bet).

| Project smell | Qaysi savol bilan o'lchanadi |
|---|---|
| Buggy Tests | Qizil build larning necha foizi test xatosi bo'lib chiqdi? |
| High Test Maintenance Cost | PR larda test fayllaridagi o'zgarish ulushi qancha va u o'smoqdami? |

Shu bobdagi [test qarzi](#166-test-qarzi-test-debt) va [testlar egaligi va madaniyat](#1611-testlar-egaligi-va-madaniyat) bo'limlari bu ikki smell ni boshqarishning jarayon tomonini beradi.

## 16.28 Production Bugs: to'plamdagi bo'shliqlarning olti nomi

Production Bugs - rasmiy test bosqichida yoki production da juda ko'p bug topiladi. Bu project smell va kitob uni olti nomlangan sababga ajratadi (Gerard Meszaros, *xUnit Test Patterns: Refactoring Test Code*, Addison-Wesley, 2007, 17-bob, 268-274-bet).

**Infrequently Run Tests** (268-bet) - dasturchilar testlarni kam yurgizadi; savol berilsa sabab chiqadi: yurgizish uzoq (Slow Tests) yoki keraksiz yiqilishlar ko'p (Buggy Tests). Kitob kuzatuvi: avtomatik testlarning foydasini ko'rgan dasturchi, biror narsa yo'lni to'smaguncha, ularni yurgizishda davom etadi; eng ko'p to'sqinlik qiladigan narsalar sekin testlar va qayta yurgizib bo'lmaydigan testlar.

**Lost Test** (269-bet) - to'plamda bajarilayotgan test soni kamaydi yoki kutilganidek o'smadi. Kitob sabablarini sanaydi: test metodi yoki test sinfi o'chirilgan, hech qachon to'plamga qo'shilmagan, annotatsiya qo'yilmagan yoki metod nomi discovery konvensiyasiga mos kelmagan.

**Missing Unit Test** (271-bet) - barcha unit testlar yashil, lekin customer test yiqilib turadi: bir vaqtda u o'tgan edi, lekin alohida sinflarning xatti-harakatini tekshiradigan unit testlar yozilmagan va keyingi o'zgarish ularning birini buzgan.

**Untested Code** (271-bet) - SUT da hech bir test ishlatmaydigan kod yo'li bor. Kitob eng keng tarqalgan sababni ko'rsatadi: SUT bog'liq komponentning ma'lum xatti-harakatiga javob beradigan yo'llarga ega va bu yo'llarni ishlatish usuli topilmagan; odatda komponent sinxron chaqiriladi va ayrim qiymatlar qaytaradi yoki istisno tashlaydi, oddiy testlashda esa bilvosita kirishlarning faqat bir qismi uchraydi. Yechim - test stub bilan kerakli bilvosita kirishlarni berib, hamma yo'lni qamrash.

**Untested Requirement** (272-bet) - funksionallik test qilinmaganini "bilamiz", lekin uni dasturiy ta'minotning ochiq interfeysi orqali ko'rinadigan qilib tekshirishning yo'li topilmaydi, hamma yozilgan test esa o'tadi.

**Neverfail Test** (274-bet) - funksionallik ishlamayotganini bilamiz, ammo uning testlari o'tadi; TDD da esa hali yozilmagan funksionallik testini yiqitib bo'lmaydi. Kitob ikki sababni beradi: noto'g'ri yozilgan tasdiq (`assertTrue(aVariable, true)` shaklida) va ancha yomoni, asinxron testlarda boshqa thread yoki process da tashlangan xato runner ga yetib bormasligi. Yechim - thread lar orasida xato aniqlashni ta'minlash yoki kodni Humble Executable shaklida refaktoring qilish.

```java
// Untested Code: istisno yo'lini test stub bilan qamrash
@Test
void returnsCachedRateWhenProviderFails() {
    given(rateProvider.rateFor("USD")).willThrow(new RateProviderException("502"));
    assertThat(rateService.rateFor("USD")).isEqualByComparingTo("12500.00");
}
```

Lost Test ga qarshi amaliy chora: CI da test sonini o'lchab, u kutilgan chegaradan pastga tushsa build ni yiqitish; `@Disabled` testlar ro'yxatini esa [testni o'chirish qoidalari](#167-testni-ochirish-qoidalari) bo'limidagi siyosat bilan boshqarish. Neverfail Test ga qarshi eng kuchli vosita mutation testing: u tasdiq yumshoq bo'lsa darhol ko'rsatadi.

## 16.29 Mystery Guest ning tashqi resurs shakli: In-line Resource va Setup External Resource

Obscure Test ro'yxatidagi Mystery Guest ikki shaklda keladi. Birinchisi obyekt fixture i: sozlash test metodidan tashqarida, `setUp` yoki helper ichida bajarilgan. Ikkinchisi tashqi resurs: test fayl, katalog yoki bazadagi oldindan tayyorlangan ma'lumotga tayanadi va o'quvchi testning boshlang'ich shartini ko'rmaydi. Meszaros ikkinchi shakl uchun ikkita alohida refaktoring beradi.

**In-line Resource** (Meszaros, *xUnit Test Patterns*, Addison-Wesley, 2007, A ilovasi, 736-737-bet). Qoida: tashqi resursning mazmunini testning fixture sozlash mantiqiga ko'chirish. Eng oddiy shakli - ishlatilayotgan faylning mazmunini test kodidagi satrga olib kirish; shundan keyin test o'qigan ma'lumot o'quvchiga ko'rinadi. Kitob uch yo'lni sanaydi: resursni testning o'zi yaratadi (masalan faylni oldindan tayyorlab qo'yish o'rniga test uni yozadi); resurs o'rniga test ichida initsializatsiya qilinadigan Test Stub qo'yiladi; yoki resursni o'qiydigan qism SUT dan ajratiladi va testga mazmun to'g'ridan-to'g'ri uzatiladi. Ikki ogohlantirish: resurs mazmuni katta bo'lsa, ehtimol siz Eager Test dan ham aziyat chekayotgansiz, shuning uchun avval ma'lumotni kamaytirish kerak; va faylni test boshida yaratib oxirida o'chirish Prebuilt Fixture dan Fresh Fixture ga o'tish bo'ladi, ya'ni testlar bir oz sekinlashadi.

**Setup External Resource** (o'sha joy, A ilovasi, 740-bet). Bu variant resursni test kodiga olib kirish imkonsiz bo'lganda ishlatiladi: SUT ning resursga murojaat mexanizmini Test Stub yoki Fake Object bilan almashtira olmaymiz. Shunda qoida - resursni oldindan tayyorlangan holda ishlatish o'rniga, testning o'zi uni yaratadi yoki ajratadi va ish tugagandan keyin bo'shatadi, hamda **test yiqilganda ham** bo'shatilishini kafolatlaydi. Nimani hal qiladi: Mystery Guest va Resource Optimism, chunki resurs har yugurishda yaratilgani uchun uning mavjudligi va mazmuni kafolatlangan. Nimani hal qilmaydi: bir xil nomdagi resursni talashadigan parallel yugurishlar, ya'ni Test Run War va Interacting Tests; buning uchun resurs nomini yugurishga xos qilish kerak.

Java da ikkinchi qoidaning tayyor mexanizmi `@TempDir`: katalogni JUnit yaratadi va test natijasidan qat'i nazar tozalaydi, nom esa har yugurishda boshqacha bo'ladi.

```java
class InvoiceExportTest {

    @TempDir
    Path tempDir; // nomi yugurishga xos: Test Run War ehtimoli yo'qoladi

    @Test
    void writesInvoiceLinesAsCsv() throws IOException {
        // Setup External Resource: kirish faylini test O'ZI yaratadi
        Path source = Files.writeString(tempDir.resolve("orders.csv"), """
                id,total
                1,1500
                """);

        Path report = new InvoiceExporter().export(source, tempDir.resolve("out.csv"));

        // In-line Resource: kutilgan mazmun ham testda, tashqi "expected" faylida emas
        assertThat(Files.readString(report)).isEqualTo("1,1500.00\n");
    }
}
```

Tanlov mezoni qisqa: resurs mazmunini testga sig'dira olsangiz In-line Resource, resursning o'zi shart bo'lsa Setup External Resource. Ikkisi ham [Obscure Test ning olti sababi](#1623-obscure-test-ning-olti-sababi) jadvalidagi Mystery Guest qatorining tashqi resurs uchun aniqlashtirilgan shakli; resurs yo'qolib yoki talashib qolish holatlari esa [Test Run War, Resource Leakage va Resource Optimism](#1615-test-run-war-resource-leakage-va-resource-optimism) bo'limida.

## 16.30 Arxitektor nazorat ro'yxati

- [ ] Flake rate o'lchanadi: barcha build'lardan test natijalari tarixi markaziy joyda saqlanadi va test darajasida flake rate hisoblanadi (maqsad < 1%).
- [ ] Karantin jarayoni rasmiylashtirilgan: `@Tag("flaky")` konvensiyasi, ticket, nomlangan egasi, SLA (≤ 2 sprint), muddat o'tganda o'chirish qoidasi va ≤ 0.5% kvota.
- [ ] Retry siyosati yozilgan: infratuzilma retry'i pipeline darajasida, test retry faqat vaqtinchalik va `flakyFailure` hisoboti bilan; global retry yoqilmagan.
- [ ] Nondeterminizm manbalari arxitektura darajasida yopilgan: `Clock` inject qilinadi, `Thread.sleep` taqiqlangan, timezone/locale CI'da qat'iy, random seed loglanadi.
- [ ] Suite tasodifiy tartibda va parallel rejimda kamida nightly sinaladi, shunda tartibga bog'liqlik PR gate'ga chiqmasdan aniqlanadi.
- [ ] Test qarzi inventarizatsiya qilingan: `@Disabled`, assertion'siz, dublikat va eskirgan testlar ro'yxati bor; har sprint'da kvota yopiladi.
- [ ] Test smell'lar katalogi PR review checklist'iga kiritilgan va test kodiga production kodi bilan bir xil review standarti qo'llanadi.
- [ ] Suite tezligi kuzatiladi: eng sekin 10 test haftalik ko'rib chiqiladi, Spring context soni cheklangan, "red build" tiklash ustuvorligi va `CODEOWNERS` egalik xaritasi kelishilgan.

## Manbalar

- Gerard Meszaros, *xUnit Test Patterns: Refactoring Test Code*, Addison-Wesley, 2007, 2-bob "Test Smells" (9-17-bet) - code, behavior va project smell bo'linishi, "sniffability" mezoni va ildiz sababni "Besh nega" bilan topish
- Gerard Meszaros, *xUnit Test Patterns: Refactoring Test Code*, Addison-Wesley, 2007, 15-bob "Code Smells" (185-222-bet) - Obscure Test (186), Conditional Test Logic (200), Hard-to-Test Code (209), Test Code Duplication (213) va Test Logic in Production (217) hamda ularning nomlangan sabablari
- Gerard Meszaros, *xUnit Test Patterns: Refactoring Test Code*, Addison-Wesley, 2007, 16-bob "Behavior Smells" (223-257-bet) - Assertion Roulette (224), Erratic Test (228), Fragile Test (239), Frequent Debugging (248), Manual Intervention (250) va Slow Tests (253)
- Gerard Meszaros, *xUnit Test Patterns: Refactoring Test Code*, Addison-Wesley, 2007, 17-bob "Project Smells" (259-274-bet) - Buggy Tests (260), High Test Maintenance Cost (265) va Production Bugs (268) hamda ularning sabablari
- Gerard Meszaros, *xUnit Test Patterns: Refactoring Test Code*, Addison-Wesley, 2007, F ilovasi "Smells, Aliases, and Causes" (761-765-bet) - har smell, taxallus va sababning bet raqami va ota-smell i
- [maven-surefire, `TestSuiteXmlParser.java`](https://raw.githubusercontent.com/apache/maven-surefire/0c970adeb11e8a59b449be5b3be2a50c478c2a65/surefire-report-parser/src/main/java/org/apache/maven/plugins/surefire/report/TestSuiteXmlParser.java) - `flakyFailure` va `flakyError` elementlari va `incrementNumberOfFlakes` hisoblagichi
- [JUnit 5.11, Writing Tests](https://raw.githubusercontent.com/junit-team/junit5/r5.11.0/documentation/src/docs/asciidoc/user-guide/writing-tests.adoc) - `@RepeatedTest` ning maqsadi (retry emas), test tartibi uchun `MethodOrderer` va `ClassOrderer`
- [JUnit 5.11, Extensions](https://raw.githubusercontent.com/junit-team/junit5/r5.11.0/documentation/src/docs/asciidoc/user-guide/extensions.adoc) - `TestTemplateInvocationContextProvider`, ya'ni retry ni qo'lda yozish yo'li
- [JUnit 5.11, Running Tests](https://raw.githubusercontent.com/junit-team/junit5/r5.11.0/documentation/src/docs/asciidoc/user-guide/running-tests.adoc) - `junit-platform.properties` dagi parallellik sozlamalari
- Gerard Meszaros, *xUnit Test Patterns: Refactoring Test Code*, Addison-Wesley, 2007, A ilovasi "Test Refactorings" (736-737 va 740-bet) - In-line Resource va Setup External Resource refaktoringlari, ya'ni Mystery Guest ning tashqi resurs shakli
- Gerard Meszaros, *xUnit Test Patterns: Refactoring Test Code*, Addison-Wesley, 2007, 18-bob "Test Strategy Patterns" (323-bet) - Immutable Shared Fixture varianti va "nima o'zgarish hisoblanadi" mezoni

---

[&larr; 15. CI/CD da test pipeline](15-ci-cd-da-test-pipeline.md) · [Mundarija](README.md) · [17. Metrikalar va test yetukligi modeli &rarr;](17-metrikalar-va-test-yetukligi-modeli.md)
