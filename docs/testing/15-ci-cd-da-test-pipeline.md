<!-- doc: testing | chapter: 15 | part:  -->

[Barcha hujjatlar](../../README.md) / [Testlash qo'llanmasi](README.md)

# 15. CI/CD da test pipeline (The Test Pipeline in CI/CD)

<details>
<summary>Bu bobdagi 16 bo'lim</summary>

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

</details>



Test suite qanchalik yaxshi yozilgan bo'lsa ham, uni ishga tushiradigan pipeline sekin, ishonchsiz yoki tartibsiz bo'lsa, jamoa testlarga ishonishni to'xtatadi. CI/CD - bu testlarning haqiqiy yashash muhiti: aynan shu yerda test suite'ning arxitekturasi iqtisodiy qiymatga aylanadi yoki yo'qoladi. Bu bobda biz pipeline bosqichlarini tartiblash, feedback vaqtini byudjet sifatida boshqarish, testlarni parallellashtirish va tanlab ishga tushirish, GitHub Actions'da to'liq workflow qurish, deploy'dan keyingi tekshirish va production'da testlash masalalarini arxitektor nuqtai nazaridan ko'rib chiqamiz. Maqsad - har bir o'zgarish uchun qancha ishonch kerakligini ongli ravishda tanlash va buni pipeline tuzilishida aks ettirish.

## 15.1 Pipeline bosqichlari va tartibi

Pipeline tartibini belgilovchi yagona printsip - fail fast: eng tez va eng arzon tekshiruv birinchi bo'lib ishlaydi, eng qimmat va eng sekin tekshiruv oxirida. Agar kod kompilyatsiya qilinmasa, 20 daqiqalik E2E suite'ni ishga tushirishning ma'nosi yo'q. Shu bilan birga, "tez narsa oldinga" printsipini mutlaqlashtirmang: statik tahlil unit testdan tezroq bo'lishi mumkin, lekin unit test nosozligi odatda muhimroq signal beradi, shuning uchun ularni bir xil bosqichda parallel job sifatida ishga tushirish ko'p hollarda to'g'ri yechim.

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

## 15.2 Feedback vaqti byudjeti

Feedback vaqti - arxitektura talabidir, SLA kabi o'lchanishi va kuzatilishi kerak. Amaliy byudjet: PR tekshiruvi 10 daqiqadan kam (ideal 7), merge pipeline 25-30 daqiqadan kam, nightly 2-3 soatdan kam. Sabab oddiy: 10 daqiqa - ishlab chiquvchi kontekstni yo'qotmasdan kutadigan oraliq. 20 daqiqadan oshsa, odam boshqa ishga o'tadi; 40 daqiqadan oshsa, jamoa pipeline'ni chetlab o'tish yo'llarini izlay boshlaydi.

| Pipeline | Maqsad (p50) | Qattiq chegara (p95) | Buzilganda |
|----------|--------------|----------------------|------------|
| PR gate | < 7 daq | < 10 daq | Suite'ni bo'lish, shard qo'shish |
| Merge | < 20 daq | < 30 daq | Og'ir testni nightly'ga ko'chirish |
| Nightly | < 90 daq | < 180 daq | Parallel runner, scope qisqartirish |
| Hotfix yo'li | < 5 daq | < 8 daq | Faqat smoke + critical unit |

Byudjetni ushlab turish uchun pipeline davomiyligini metrika sifatida saqlang va p95 ni haftalik ko'rib chiqing. Byudjet buzilganda uchta vosita bor: parallellashtirish (resurs qo'shish), scope'ni ko'chirish (testni keyingi bosqichga olib o'tish), va testni tezlashtirish (Spring kontekstini kamaytirish, Testcontainers reuse). To'rtinchi "vosita" - testni o'chirish - faqat o'sha test haqiqatan qiymat bermasa qo'llanadi va bu qaror ongli, hujjatlashtirilgan bo'lishi kerak.

## 15.3 Testlarni ajratish va parallel bajarish

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

`forkCount=1C` - CPU yadrosi soniga teng JVM fork. Bu JVM darajasidagi parallellik. JUnit 5 esa bir JVM ichida thread darajasida parallellikni beradi, `junit-platform.properties` orqali:

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

Muhim ogohlantirish: parallel execution faqat testlar haqiqatan izolyatsiya qilingan bo'lsa ishlaydi. Umumiy statik state, bitta jadvalga yozadigan integration testlar, `@DirtiesContext` - bularning barchasi parallellikda flaky natija beradi. Shuning uchun amaliy strategiya: unit testlarda `concurrent`, Spring kontekstli integration testlarda `classes.default=concurrent` + metodlar `same_thread`, va konfliktli testlarga `@ResourceLock` yoki `@Execution(SAME_THREAD)`.

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

CI matrix va sharding - bu testlarni bir nechta runner'ga bo'lib tarqatish. GitHub Actions'da `strategy.matrix` bilan 4 shard ishga tushiriladi, har biri test ro'yxatining o'z qismini oladi. Sharding'ni amalga oshirishning ikki yo'li: test fayllari ro'yxatini deterministik bo'lish (hash yoki index bo'yicha) yoki oldingi run'lardagi davomiylik ma'lumotiga qarab balanslash (ikkinchisi ancha samarali, lekin tarixiy ma'lumot saqlashni talab qiladi).

## 15.4 Keshlash va tezlashtirish

Keshlash - pipeline tezlashtirishning eng arzon vositasi. Maven uchun `~/.m2/repository`, Gradle uchun `~/.gradle/caches` keshlanadi; `actions/setup-java` da `cache: maven` yoki `cache: gradle` buni avtomatik qiladi. Gradle build cache (`org.gradle.caching=true`) bundan kuchliroq: u task natijalarini (compile, test) keshlaydi, ya'ni o'zgarmagan modul testi umuman qayta ishlamaydi. Remote build cache bilan bu kesh butun jamoa va CI o'rtasida bo'linadi.

Docker layer cache image build vaqtini qisqartiradi, lekin Spring loyihalarida Jib yoki Buildpacks ishlatilsa, layer ajratish allaqachon optimal (dependency layer alohida, application class'lar alohida). Testcontainers uchun ikkita muhim optimizatsiya: image'larni oldindan pull qilish (pipeline boshida `docker pull postgres:16-alpine`, bu test timeout'ini oldini oladi) va container reuse (`testcontainers.reuse.enable=true` - lokalda juda foydali, CI'da ephemeral runner'da ma'nosi kam).

Eng katta tezlashtirish manbai - Spring kontekst keshini buzmaslik. Har xil `@MockBean`, har xil `@TestPropertySource`, har xil `@ActiveProfiles` kombinatsiyasi yangi ApplicationContext yaratadi, va har bir kontekst 2-10 sekund. [7-bobda](07-integratsion-test-spring-boot-slice-testlari.md) ko'rilgan kontekst keshlash qoidalariga rioya qilish ko'pincha parallellashtirishdan kattaroq samara beradi. Incremental build (Gradle'ning up-to-date checking, Maven'da `-o` offline rejim va `mvn -am` bilan cheklangan scope) bu rasmni to'ldiradi.

## 15.5 Testni tanlab ishga tushirish

Katta monorepo'da har push'da butun suite'ni ishga tushirish byudjetni buzadi. Test selection - faqat o'zgarishga aloqador testlarni ishga tushirish.

Eng ishonchli daraja - modul darajasi. Maven'da `mvn test -pl payment-service -am` o'sha modul va uning upstream dependency'larini quradi; `-amd` esa downstream'larni ham oladi, bu esa o'zgarish ta'sirini to'liqroq qamrab oladi. Gradle'da `./gradlew :payment-service:test` plus dependency grafigini `./gradlew :payment-service:dependencies` orqali tahlil qilish mumkin. Git diff'dan o'zgargan fayllarni olib, ularni modul yo'llariga map qilish - amaliy va tushunarli yondashuv:

```bash
# O'zgargan modullarni aniqlash (merge-base'ga nisbatan)
BASE=$(git merge-base origin/main HEAD)
CHANGED=$(git diff --name-only "$BASE"...HEAD \
  | awk -F/ '/\// {print $1}' | sort -u | grep -v '^\.' )
if [ -z "$CHANGED" ]; then echo "no module changes"; exit 0; fi
# Umumiy modul o'zgarsa - hammasini ishga tushiramiz
if echo "$CHANGED" | grep -qE '^(common|test-support|platform-bom)$'; then
  echo "ALL" > affected.txt
else
  echo "$CHANGED" | paste -sd, - > affected.txt
fi
# Maven: mvn -pl "$(cat affected.txt)" -am verify
```

Predictive test selection (Gradle Develocity, Launchable kabi tijorat yechimlari) bundan bir qadam uzoqlashadi: tarixiy ma'lumot va ML modeli asosida qaysi test o'zgarishdan ta'sirlanishi ehtimolini bashorat qiladi va faqat yuqori ehtimolli testlarni ishga tushiradi. Bu PR vaqtini sezilarli qisqartiradi.

Xavfi va chegarasi aniq bo'lishi kerak. Test selection har qanday holatda ham evristika: reflection, Spring profile, konfiguratsiya fayli, SQL migratsiya yoki resource orqali keladigan bog'liqlikni statik tahlil ko'rmaydi. Shuning uchun qoida: selection faqat PR darajasida, merge pipeline va nightly'da esa to'liq suite majburiy. Agar selection noto'g'ri ishlasa, nightly uni tutadi - bu "safety net" bo'lmasa, selection'ni kiritmang.

## 15.6 GitHub Actions bilan to'liq namuna workflow

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

Coverage va PR izohi alohida job sifatida: JaCoCo report'ni yig'ib, `madrapps/jacoco-report` yoki o'z `gh pr comment` buyruqlaringiz bilan PR'ga xulosa yoziladi. Testcontainers ishlatganda `services:` bloki kerak emas - Docker'ni test o'zi boshqaradi; `services:` ni faqat Testcontainers ishlatilmagan, oddiy TCP service kerak bo'lgan holatda tanlang (tezroq, lekin lokalda takrorlanmaydi).

## 15.7 GitLab CI va Jenkins uchun eslatma

GitLab CI'da ekvivalent tushunchalar: `stages` bosqichlarni, `parallel: 4` sharding'ni, `cache:key` dependency keshini, `artifacts:reports:junit` esa test natijalarini merge request'da ko'rsatishni beradi. Eng katta farq - Testcontainers uchun Docker: GitLab runner'da `docker:dind` service yoki privileged runner kerak, va `DOCKER_HOST` to'g'ri sozlanishi lozim. `rules:changes` bilan modul bo'yicha selection tabiiy ifodalanadi.

Jenkins'da declarative pipeline `stage` va `parallel` bloklaridan iborat; `junit '**/target/surefire-reports/*.xml'` natijalarni oladi, `publishHTML` yoki Allure plugin hisobotni chiqaradi. Farqlar: Jenkins agent'lari odatda uzoq yashaydigan (persistent) mashinalar, shuning uchun workspace tozalash (`cleanWs()`) va Testcontainers'dan qolgan container'larni tozalash (Ryuk) muhim; kesh esa agent diskida tabiiy ravishda saqlanadi, bu tez, lekin "ishlaydi mening agentimda" muammosini keltirib chiqaradi.

## 15.8 Majburiy tekshiruvlar va branch protection

Required check sifatida nimani belgilash - arxitektura qarori. Majburiy: build, unit test, slice/integration test, contract test, coverage darvozasi ([14-bobda](14-arxitektura-testlari-va-kod-sifati.md) belgilangan chegaralar bo'yicha), critical security scan. Ogohlantirish sifatida qoldirish mumkin: yangi statik tahlil qoidalari (grace period bilan), performance trend, informational dependency advisory'lar. Qoida: majburiy check faqat deterministik va tez bo'lishi kerak - flaky check majburiy bo'lsa, jamoa uni chetlab o'tishni o'rganadi.

Merge queue (GitHub merge queue yoki GitLab merge train) ikki muammoni yechadi: semantik konflikt (ikki PR alohida yashil, birga qizil) va "main doim yashil" kafolati. Merge queue'da pipeline PR branch'ida emas, PR'ning main bilan birlashgan natijasida ishlaydi. Narxi - qo'shimcha pipeline run; foydasi - buzilgan main va undan keluvchi barcha blokirovkalarning yo'qolishi. Katta jamoada (kuniga 20+ merge) merge queue praktik zarurat.

## 15.9 Test natijalari va hisobot

Pipeline natijasi tushunarli bo'lmasa, uning qiymati yarmiga tushadi. Minimal to'plam: JUnit XML (Surefire/Failsafe `target/surefire-reports/*.xml` va `failsafe-reports/*.xml`), ularni CI UI'da ko'rsatadigan reporter, va JaCoCo coverage hisoboti (`jacoco:report` → `target/site/jacoco/jacoco.xml`).

Boyroq hisobot uchun Allure (`allure-junit5` adapter, `allure-maven`/`allure-gradle` plugin) qadam-qadam ko'rinish, attachment (screenshot, request/response) va tarixiy trend beradi; ReportPortal esa natijalarni markazlashtirib, nosozlik klassifikatsiyasini taklif qiladi.

PR izohida nima bo'lishi kerak: o'tgan/yiqilgan test soni, coverage o'zgarishi (delta, mutlaq son emas), yangi flaky testlar va to'g'ridan-to'g'ri nosoz test log'iga havola. Nosozlik artefaktlari - bu debug qilish imkoniyati: failsafe report, application log, E2E uchun screenshot va video, OOM holatida heap dump (`-XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=target/`). Artefaktlarni faqat `if: failure()` da yuklash saqlash xarajatini keskin kamaytiradi.

## 15.10 Nightly va haftalik suite'lar

| Suite | Chastota | Tarkib | Egasi |
|-------|----------|--------|-------|
| To'liq regression | Nightly | Barcha IT + E2E, selection'siz | Dev jamoa (rotatsiya) |
| Performance | Nightly | Load profil, baseline bilan solishtirish | Platform/SRE |
| Mutation testing | Haftalik | PIT, o'zgargan paketlarda | Dev jamoa |
| Dependency + image scan | Nightly | CVE, litsenziya, SBOM diff | Security |
| Soak test | Haftalik | 8-24 soat uzluksiz yuklama | Platform/SRE |

Nightly'ning asosiy xatosi - natijani hech kim ko'rmasligi. Shuning uchun uchta tashkiliy qoida: har bir nightly suite'ning nomlangan egasi bo'lsin (jamoa, shaxs emas - shaxs ta'tilga chiqadi); nosozlik avtomatik ravishda ticket yoki Slack kanaliga tushsin, email'ga emas; va ertalab birinchi ish - nightly natijasini ko'rib chiqish, bu standup'ning doimiy bandi bo'lsin. Agar nightly uch kun ketma-ket qizil bo'lsa va hech narsa o'zgarmasa, u suite o'lgan - uni tuzat yoki o'chir.

## 15.11 Deploy'dan keyingi tekshirish

Deploy tugadi degani ishlayapti degani emas. Post-deploy verification zanjirida: readiness probe (`/actuator/health/readiness`) pod trafik qabul qilishga tayyormi; liveness probe (`/actuator/health/liveness`) jarayon tirikmi; keyin smoke test - real muhitga qarshi 5-15 ta eng muhim yo'l (login, asosiy o'qish, asosiy yozish), bir-ikki daqiqada tugaydigan.

Canary release'da yangi versiya trafikning 5-10% ini oladi va metrikalar solishtiriladi: error rate, p99 latency, business metrika (masalan, muvaffaqiyatli to'lov ulushi). Avtomatik rollback sharti aniq raqamlar bilan ifodalanishi kerak: "5 daqiqa oynada canary error rate baseline'dan 2x yuqori bo'lsa" yoki "p99 baseline'dan 50% yuqori". Argo Rollouts yoki Flagger bu analizni deklarativ ravishda bajaradi. Shartlarni noaniq qoldirmang - "agar yomon ko'rinsa" degan shart hech qachon avtomatik ishlamaydi.

Synthetic monitoring - bu production'da doimiy ishlaydigan smoke test: har 1-5 daqiqada muhim user journey'larni tashqaridan bajaradi va nosozlikni foydalanuvchi shikoyatidan oldin topadi. Amalda bu sizning E2E test kodingizning qayta ishlatilgan qismi bo'lishi mumkin, bu esa ikki marta yozishdan qutqaradi.

## 15.12 Production'da testlash

Production'da testlash - qoidalarni buzish emas, balki test muhiti hech qachon production'ga to'liq teng bo'lmasligini tan olish. To'rt asosiy texnika:

Feature flag bilan dark launch - yangi kod deploy qilinadi, lekin flag o'chiq; ichki foydalanuvchilar uchun yoqiladi, keyin bosqichma-bosqich kengaytiriladi. Spring'da bu oddiy `@ConditionalOnProperty` dan to'liq flag platformasiga (Unleash, LaunchDarkly, OpenFeature SDK) qadar bo'lishi mumkin. Shadow traffic - real so'rovlar nusxasi yangi versiyaga yuboriladi, lekin javobi foydalanuvchiga qaytmaydi; bu yangi implementatsiyani real yuklama va real ma'lumot shakli bilan sinashning eng halol usuli. A/B test - ikki variant o'rtasida business metrikani solishtirish, bu texnik emas, mahsulot qarori. Va barcha uchun asos - kuzatuvchanlik: distributed tracing, strukturalangan log, per-variant metrika.

Xavfsiz qilish shartlari: yozish operatsiyalarida yon ta'sir bo'lmasligini kafolatlash (shadow traffic'da yozishni mock qilish yoki alohida sxemaga yo'naltirish), test ma'lumotini real ma'lumotdan ajratish (test akkauntlarni belgilash va ularni analitikadan chiqarish), har bir flag uchun o'chirish mexanizmi va muddati (eskirgan flag - texnik qarz), va blast radius'ni cheklash. Agar siz canary metrikasini kuzatolmasangiz, production'da testlashga tayyor emassiz.

## 15.13 Monorepo va multi-modul loyihada test pipeline

Multi-modul Maven/Gradle loyihasida pipeline arxitekturasi modul grafigidan kelib chiqadi. Birinchi qadam - grafikni aniq va yuzaki (shallow) qilish: agar har bir modul `common` ga bog'liq bo'lsa, `common` dagi har o'zgarish butun suite'ni ishga tushiradi va selection'ning ma'nosi qolmaydi. Shuning uchun `common` ni mayda, barqaror modullarga bo'lish amaliy qiymat beradi.

Test util modullari (`test-support`, `testcontainers-fixtures`) `test-jar` yoki alohida artifact bo'lib chiqariladi, shunda har bir service uni `test` scope'da oladi - takroriy Testcontainers konfiguratsiyasi, umumiy fixture va assertion'lar bir joyda saqlanadi.

Versiyalash ikki modelda bo'ladi: bitta umumiy versiya (release train - barcha modullar birga chiqadi, oddiy, lekin bog'liq) yoki modul-bo'yicha mustaqil versiya (moslashuvchan, lekin matritsa testini talab qiladi). Release train monorepo'da ko'pincha to'g'ri tanlov: pipeline oddiy bo'ladi va contract test matritsasi kichik qoladi. Mustaqil versiyalashni tanlasangiz, contract test majburiy - aks holda modullar orasidagi moslik faqat production'da tekshiriladi.

## 15.14 Pipeline'ni ishonchli qilish

Pipeline'ning ishonchliligi uning tezligidan muhimroq. Birinchi qoida - infratuzilma nosozligini test nosozligidan ajratish. Docker registry javob bermadi, runner diski to'ldi, network timeout - bular test nosozligi emas, lekin odatiy pipeline ularni bir xil "failed" sifatida ko'rsatadi. Yechim: infra bosqichlarini (image pull, dependency download, container startup) alohida step sifatida ajratish va ularning exit code'ini alohida ko'rish; keyin retry'ni faqat o'sha step'larga qo'llash.

Retry siyosati qat'iy bo'lishi kerak: `docker pull` va dependency download uchun retry - to'g'ri; test bajarilishi uchun retry - flaky testni yashirish, bu [16-bobda](16-flaky-testlar-test-qarzi-va-test-kodini.md) ko'rilgan jarayonni buzadi. Agar test retry kerak bo'lsa, u hodisa sifatida qayd etilsin va flaky sifatida belgilansin, jimgina yashil bo'lmasin.

Timeout har darajada: job uchun (`timeout-minutes: 25`), test uchun (`@Timeout` yoki `junit.jupiter.execution.timeout.testable.method.default=2 m`), container startup uchun (Testcontainers `withStartupTimeout`). Timeout bo'lmasa, osilgan test butun runner quotasini yeydi. Resurs tomoni: standart GitHub runner 2 vCPU / 7 GB RAM - bu Testcontainers bilan bir nechta container ko'targan integration suite uchun ko'pincha kam. Larger runner (4-8 vCPU) narxi bor, lekin 25 daqiqani 8 daqiqaga tushirsa, ishlab chiquvchi vaqti hisobida tez qaytadi. Nihoyat, Docker mavjudligini boshida tekshirish (`docker info`) va yo'q bo'lsa aniq xabar bilan tez yiqilish - 20 daqiqadan keyingi tushunarsiz `ContainerLaunchException` dan yaxshiroq.

## 15.15 Anti-patternlar

Hamma testni har push'da ishga tushirish. Boshida to'g'ri ko'rinadi, loyiha o'sgach PR vaqti 45 daqiqaga chiqadi. To'g'ri yo'l - bosqichli strategiya va selection, nightly safety net bilan.

Qizil build bilan yashash. Main qizil bo'lib bir kundan ortiq turgan har bir soat - barcha signalning qiymatini nolga olib boradi. Qoida qattiq: buzilgan main eng yuqori prioritet, tuzatish yoki revert, uchinchi variant yo'q.

Flaky testni retry bilan yashirish. `retryFailedTests` qo'yib, qizil rangni yashilga aylantirish - eng qimmat qarz turi: endi siz real nosozlikni ham ko'rmaysiz.

Testni CI'da o'tkazib yuborish. `-DskipTests`, `@Disabled` kommentsiz, `@Ignore` "keyin tuzataman" bilan - bular hech qachon qaytib kelmaydi. Agar test o'chirilsa, muddat va ticket bilan o'chirilsin.

Faqat main'da test qilish. PR'da hech narsa ishlamasa, nosozlik main'ga tushgandan keyin aniqlanadi va kim buzganini topish qimmatlashadi.

Lokal va CI natijasining farqi. "Mening mashinamda ishlaydi" - bu pipeline dizayni muammosi: timezone, locale, Java versiyasi, Docker yoki fayl tizimi farqlari. Yechim - bir xil Java versiyasini wrapper/toolchain bilan qotirish, `-Duser.timezone=UTC` va `file.encoding=UTF-8` ni ikki joyda bir xil qo'yish, Testcontainers'ni lokalda ham ishlatish.

## 15.16 Arxitektor nazorat ro'yxati

- [ ] Pipeline bosqichlari fail fast printsipi bo'yicha tartiblangan, PR gate va merge pipeline aniq ajratilgan
- [ ] Feedback vaqti byudjeti yozilgan (PR < 10 daq), p95 metrika sifatida kuzatiladi va buzilganda aniq harakat rejasi bor
- [ ] Surefire (`*Test`) va Failsafe (`*IT`) ajratilgan, JUnit 5 parallel execution va sharding sozlangan hamda flaky bermasligi tasdiqlangan
- [ ] Dependency kesh, Gradle build cache, Testcontainers image pre-pull yoqilgan va Spring kontekst keshi buzilmasligi tekshirilgan; test selection faqat PR darajasida, to'liq suite nightly safety net sifatida majburiy
- [ ] Required check'lar ro'yxati ongli tanlangan (deterministik va tez), merge queue zarurati baholangan
- [ ] Nosozlik artefaktlari (JUnit XML, log, screenshot, heap dump) `if: failure()` da saqlanadi va PR'da xulosa ko'rinadi
- [ ] Deploy'dan keyin smoke test, canary metrikasi va avtomatik rollback sharti raqamlar bilan belgilangan
- [ ] Retry faqat infratuzilma step'larida; har bir nightly suite'ning nomlangan egasi va nosozlik marshruti bor

---

[&larr; 14. Arxitektura testlari va kod sifati darvozalari](14-arxitektura-testlari-va-kod-sifati.md) · [Mundarija](README.md) · [16. Flaky testlar, test qarzi va test kodini saqlash &rarr;](16-flaky-testlar-test-qarzi-va-test-kodini.md)
