<!-- doc: testing | chapter: 15 | part:  -->

[Barcha hujjatlar](../../README.md) / [Testlash qo'llanmasi](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 15. CI/CD da test pipeline (The Test Pipeline in CI/CD)

<details>
<summary>Bu bobdagi 18 bo'lim</summary>

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
- [15.16 Test ijarasi (tenancy) bilan production'da testlash](#1516-test-ijarasi-tenancy-bilan-productionda-testlash)
- [15.17 Integratsiya chastotasi va sakkizta integratsiya strategiyasi](#1517-integratsiya-chastotasi-va-sakkizta-integratsiya-strategiyasi)
- [15.18 Arxitektor nazorat ro'yxati](#1518-arxitektor-nazorat-royxati)

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

**Continuous delivery va continuous deployment bir narsa emas.** Newman ning ta'rifi: continuous delivery - har check-in ni release candidate deb baholash va uning production ga chiqishga tayyorligi haqida doimiy qaytarma aloqa olish; continuous deployment esa avtomatik tekshiruvdan o'tgan hamma narsani inson aralashuvisiz deploy qilish, ya'ni continuous delivery ning davomi. Continuous delivery siz continuous deployment bo'lmaydi, teskarisi esa mumkin va normal: ko'p jamoa deploy qarorini odam qabul qilishini xohlaydi va bu continuous delivery ga to'liq mos. Shuning uchun yuqoridagi 11-bosqichni avtomatlashtirmagan loyiha ham CD qilayotgan bo'ladi. Amaliy maslahat: CI vositasini CD ga moslab hack qilmang, pipeline ni birinchi darajali tushuncha sifatida modellaydigan vositani oling, aks holda qo'lda tasdiq bosqichini ham, manual UAT ni ham pipeline da ko'rsatib bo'lmaydi.

**Release candidate kod va konfiguratsiyani birga oladi va yashil commitdan kesiladi.** Google ning CD amaliyotida statik konfiguratsiya release candidate ga kod bilan birga qo'shiladi va shu kod bilan birga sinaladi; konfiguratsiya ham versiya nazoratida turadi va shu review jarayonidan o'tadi. Nomzod oxirgi tasdiqlangan (yashil) commitdan kesiladi, keyin muhitlar bo'ylab ko'tariladi va **qayta qurilmaydi**: artefakt yoki konteyner image i bir marta yasalib, test, staging va production da aynan shu nusxa ishlatiladi. Shu ikki qoida versiya nomuvofiqligini (version skew) nomzodni ko'tarish paytida ushlaydi, production da emas.

## 15.2 Feedback vaqti byudjeti

Feedback vaqti - arxitektura talabidir, SLA kabi o'lchanishi va kuzatilishi kerak. Amaliy byudjet: PR tekshiruvi 10 daqiqadan kam (ideal 7), merge pipeline 25-30 daqiqadan kam, nightly 2-3 soatdan kam. Sabab oddiy: 10 daqiqa - ishlab chiquvchi kontekstni yo'qotmasdan kutadigan oraliq. 20 daqiqadan oshsa, odam boshqa ishga o'tadi; 40 daqiqadan oshsa, jamoa pipeline'ni chetlab o'tish yo'llarini izlay boshlaydi.

| Pipeline | Maqsad (p50) | Qattiq chegara (p95) | Buzilganda |
|----------|--------------|----------------------|------------|
| PR gate | < 7 daq | < 10 daq | Suite'ni bo'lish, shard qo'shish |
| Merge | < 20 daq | < 30 daq | Og'ir testni nightly'ga ko'chirish |
| Nightly | < 90 daq | < 180 daq | Parallel runner, scope qisqartirish |
| Hotfix yo'li | < 5 daq | < 8 daq | Faqat smoke + critical unit |

Byudjet yonida **sekin o'sadigan xarajatlar** ham kuzatiladi. Google ning formulasi: tashkilot takrorlab bajaradigan har narsa o'sish bo'yicha o'lchanishi kerak. To'liq build qancha vaqt oladi, toza klon qancha davom etadi, til yoki framework versiyasini yangilash qancha turadi: bu uch raqam odatda hech kim tomonidan kuzatilmaydi va juda sekin yomonlashadi. Shuning uchun ular qaynatilayotgan baqa kabi: hech qachon inqiroz momenti bo'lib ko'rinmaydi, lekin bir kun "endi yangilay olmaymiz" holatiga olib keladi. Praktik yechim - bu uchtasini ham pipeline davomiyligi bilan bir xil metrika sifatida saqlash va choraklik ko'rib chiqish.

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

Eng katta tezlashtirish manbai - Spring kontekst keshini buzmaslik. Har xil `@MockitoBean`, har xil `@TestPropertySource`, har xil `@ActiveProfiles` kombinatsiyasi yangi ApplicationContext yaratadi, va har bir kontekst 2-10 sekund. [7-bobda](07-integratsion-test-spring-boot-slice-testlari.md) ko'rilgan kontekst keshlash qoidalariga rioya qilish ko'pincha parallellashtirishdan kattaroq samara beradi. Incremental build (Gradle'ning up-to-date checking, Maven'da `-o` offline rejim va `mvn -am` bilan cheklangan scope) bu rasmni to'ldiradi.

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

O'zgarishga ta'sir qilgan testlar rejimi build fayli (`build.gradle`, `settings.gradle`, `pom.xml`, versiya katalogi) o'zgarganda to'liq suite ga o'tadi: bog'liqlik versiyasi hamma testga tegadi, shuning uchun bu to'g'ri xatti-harakat. Oqibati kutilmagan: mashinada Docker ishlab tursa, to'liq suite ichidagi Testcontainers integratsion testlari ham yuradi va vaqt bir necha barobar oshadi. Docker siz yoki cheklangan muhitda (sandbox, kichik CI agent) sinalayotgan narsaga tegishli test fayllarini aniq yo'l bilan bering. Bu to'liq suite ni almashtirmaydi: merge pipeline va nightly da u baribir majburiy.

```bash
# build fayli o'zgargan, Docker kerak emas: faqat tegishli sinflar
./gradlew test --tests 'com.example.order.OrderServiceTest' --tests 'com.example.order.PriceCalculatorTest'
```

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

**CI ogohlantirish tizimi, mutlaq yashillik emas.** Winters ning qarashi CI ni production monitoringining "chapga surilgan" shakli deb oladi: ikkisi ham muammoni iloji boricha tez topish uchun ishlaydi va ikkisida ham sifat mezoni bir xil - signal faqat muhim invariant buzilganda chiqishi kerak. Har necha CI yurishida yiqiladigan flaky test har necha daqiqada navbatchini uyg'otadigan yolg'on alert bilan bir xil zararli. Shundan uch xulosa chiqadi, va ular korpusning "majburiy check deterministik bo'lsin" qoidasining asosi:

- 100 foiz yashil CI ni ta'minlash production uchun 100 foiz uptime ni ta'minlash kabi qimmat, va buni maqsad qilish test bilan commit orasida poyga holatiga olib keladi.
- Har nosozlikni teng darajada signal deb olish to'g'ri emas. Production da servisga ta'sir qilmayotgan alertni o'chirish to'g'ri qaror; sababi tushunarli va production ga ta'sir qilmaydigan test nosozligida ham testni o'chirishni ancha liberal qabul qilish mumkin.
- "CI yashil bo'lmasa hech kim commit qilmaydi" siyosati har holatda to'g'ri emas: nosozlik albatta tekshiriladi, lekin asosiy sabab aniq va production ga tegmasa, commitni bloklash asossiz.

Buning teskari tomoni ham bor: cause-based alert va mo'rt test butunlay qiymatsiz emas, ular nosozlikni tekshirishda qo'shimcha dalil beradi ("rasm pipeline i buzildi, unit testlardan biri JPEG siqishdan boshqa baytlar kelayotganini aytadi"). Ular faqat birlamchi signal bo'lishga yaramaydi.

Merge queue (GitHub merge queue yoki GitLab merge train) ikki muammoni yechadi: semantik konflikt (ikki PR alohida yashil, birga qizil) va "main doim yashil" kafolati. Merge queue'da pipeline PR branch'ida emas, PR'ning main bilan birlashgan natijasida ishlaydi. Narxi - qo'shimcha pipeline run; foydasi - buzilgan main va undan keluvchi barcha blokirovkalarning yo'qolishi. Katta jamoada (kuniga 20+ merge) merge queue praktik zarurat.

## 15.9 Test natijalari va hisobot

Pipeline natijasi tushunarli bo'lmasa, uning qiymati yarmiga tushadi. Minimal to'plam: JUnit XML (Surefire/Failsafe `target/surefire-reports/*.xml` va `failsafe-reports/*.xml`), ularni CI UI'da ko'rsatadigan reporter, va JaCoCo coverage hisoboti (`jacoco:report` → `target/site/jacoco/jacoco.xml`).

Boyroq hisobot uchun Allure (`allure-junit5` adapter, `allure-maven`/`allure-gradle` plugin) qadam-qadam ko'rinish, attachment (screenshot, request/response) va tarixiy trend beradi; ReportPortal esa natijalarni markazlashtirib, nosozlik klassifikatsiyasini taklif qiladi.

PR izohida nima bo'lishi kerak: o'tgan/yiqilgan test soni, coverage o'zgarishi (delta, mutlaq son emas), yangi flaky testlar va to'g'ridan-to'g'ri nosoz test log'iga havola. Nosozlik artefaktlari - bu debug qilish imkoniyati: failsafe report, application log, E2E uchun screenshot va video, OOM holatida heap dump (`-XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=target/`). Artefaktlarni faqat `if: failure()` da yuklash saqlash xarajatini keskin kamaytiradi.

Test asbobi chiqishini quvurga (`| tail`, `| tee`) ulaganda chiqish kodi quvurdagi oxirgi buyruqniki bo'ladi: asbob yiqilsa ham `tail` 0 qaytaradi va skript yoki CI "yashil" deb o'qiydi. Natijani kodga emas, asbobning yakuniy natija qatoriga va JUnit XML fayllariga qarab o'qing (`tests`, `failures`, `errors` atributlari). Kod kerak bo'lsa `set -o pipefail` yoki faylga yo'naltirish ishlatiladi.

```bash
# yomon: rc ni tail beradi, testlar yiqilsa ham 0
./gradlew test | tail -20; echo "rc=$?"

# yaxshi: quvur birinchi yiqilgan buyruqning kodini qaytaradi
set -o pipefail
./gradlew test | tail -20; echo "rc=$?"

# eng ishonchli: faylga yozish, kodni saqlash, keyin XML dan sanash
./gradlew test > build/test.log 2>&1; rc=$?
grep -ho 'tests="[0-9]*" skipped="[0-9]*" failures="[0-9]*" errors="[0-9]*"' build/test-results/test/*.xml
```

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

**Bitta to'plamni ham build ga, ham production ga qarshi yurgizish nosozlikni ajratadi.** Google ning Takeout jamoasi topgan arzon usul: postsubmit CI da yangi build bilan yurgan test to'plamining aynan o'zi production ga qarshi ham doimiy yurgiziladi. Shunda yangi qizil natija ikki manbaga ajraladi - o'zimizning so'nggi o'zgarishlarimizdan yoki production dagi boshqa mikroservisning relizidan. Bu usul ayniqsa ko'p servisga tayanadigan tizimda ishlaydi, chunki aks holda CI "butun tashkilotni" testlab, o'ziga tegishli bo'lmagan nosozlikni ko'rsatadi. Implementatsiyasi: bitta suite, ikki profil (`-Dtarget=rc` va `-Dtarget=prod`), natijalar bir hisobotda yonma-yon.

**Konfiguratsiyani ishga tushirish sinovi (deployment configuration test).** Google da katta nosozliklarning birinchi sababi kod emas, konfiguratsiya o'zgarishi. Sabab tuzilishda: konfiguratsiya production kodidan boshqa tilda yoziladi, binardan tezroq tarqaladi va testlash qiyinroq. Shuning uchun konfiguratsiya kod bilan bir qatorda versiya nazoratida turadi (shunda nosozlik sababi tasodifiy "flakiness" emas, aniq commit bo'ladi) va alohida katta test yoziladi: SUT production konfiguratsiyasi bilan ko'tariladi, qo'shimcha ma'lumot ham, assertion ham kerak emas - ko'tarilsa test o'tadi, ko'tarilmasa yiqiladi. Spring da buning eng yaqin shakli kontekst yuklanishini tekshiradigan smoke test:

```java
@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)
@ActiveProfiles("prod")
@TestPropertySource(properties = "spring.config.import=optional:configtree:/run/secrets/")
class ProdConfigurationSmokeTest {

    @Test
    void contextStartsWithProductionConfiguration(ApplicationContext context) {
        assertThat(context.isActive()).isTrue();
    }
}
```

Synthetic monitoring - bu production'da doimiy ishlaydigan smoke test: har 1-5 daqiqada muhim user journey'larni tashqaridan bajaradi va nosozlikni foydalanuvchi shikoyatidan oldin topadi. Amalda bu sizning E2E test kodingizning qayta ishlatilgan qismi bo'lishi mumkin, bu esa ikki marta yozishdan qutqaradi.

## 15.12 Production'da testlash

Production'da testlash - qoidalarni buzish emas, balki test muhiti hech qachon production'ga to'liq teng bo'lmasligini tan olish. To'rt asosiy texnika:

Feature flag bilan dark launch - yangi kod deploy qilinadi, lekin flag o'chiq; ichki foydalanuvchilar uchun yoqiladi, keyin bosqichma-bosqich kengaytiriladi. Spring'da bu oddiy `@ConditionalOnProperty` dan to'liq flag platformasiga (Unleash, LaunchDarkly, OpenFeature SDK) qadar bo'lishi mumkin. Shadow traffic - real so'rovlar nusxasi yangi versiyaga yuboriladi, lekin javobi foydalanuvchiga qaytmaydi; bu yangi implementatsiyani real yuklama va real ma'lumot shakli bilan sinashning eng halol usuli. A/B test - ikki variant o'rtasida business metrikani solishtirish, bu texnik emas, mahsulot qarori. Va barcha uchun asos - kuzatuvchanlik: distributed tracing, strukturalangan log, per-variant metrika.

Beshinchi texnika - **A/B diff regression test**, shadow traffic ning tekshiruv bilan to'ldirilgan shakli. Google da bu eng ko'p ishlatiladigan katta test turi: eski va yangi versiya ikki alohida muhitda ko'tariladi, ikkisiga bir xil trafik yuboriladi (ko'pincha production dan ko'chirilgan yoki tanlab olingan) va uchinchi binar javoblarni solishtiradi. Har farq ikki qatordan biriga tushadi: kutilgan o'zgarish yoki regressiya. Ikki variant ham foydali:

- **A-A taqqoslash** (tizimni o'zi bilan solishtirish) nondeterminizm, shovqin va flakiness manbalarini topadi va ularni keyingi A-B natijalaridan chiqarib tashlashga imkon beradi.
- **A-B-C taqqoslash** oxirgi production versiyasi, baseline build va kutilayotgan o'zgarishni birga qo'yadi: shunda bir qarashda ham shu o'zgarishning ta'siri, ham keyingi relizga yig'ilgan umumiy farq ko'rinadi.

Asosiy sababi Hyrum qonuni: tizimning haqiqiy public API si e'lon qilingani emas, foydalanuvchiga ko'rinadigan hamma narsa, shuning uchun nosozlik rejimlarining ko'pini oldindan test bilan qoplab bo'lmaydi. Kamchiliklari to'rtta va ular aniq: **tasdiqlash qo'lda** (farq yaxshimi yoki yomonmi, hatto baseline to'g'rimi - buni odam hal qiladi), **shovqin** (kutilmagan farq har safar qo'lda tekshirishni talab qiladi, shuning uchun shovqinni yo'qotish bunday testni qurishning asosiy murakkabligi), **qamrov** (burchak holatlarini ochadigan trafikni qo'lda yig'ish qiyin) va **sozlash** (bitta SUT ni ushlab turish ham qiyin, ikkitasi murakkablikni ikki baravar oshiradi, ayniqsa ular umumiy bog'liqliklarga ega bo'lsa).

Xavfsiz qilish shartlari: yozish operatsiyalarida yon ta'sir bo'lmasligini kafolatlash (shadow traffic'da yozishni mock qilish yoki alohida sxemaga yo'naltirish), test ma'lumotini real ma'lumotdan ajratish (test akkauntlarni belgilash va ularni analitikadan chiqarish), har bir flag uchun o'chirish mexanizmi va muddati (eskirgan flag - texnik qarz), va blast radius'ni cheklash. Agar siz canary metrikasini kuzatolmasangiz, production'da testlashga tayyor emassiz.

## 15.13 Monorepo va multi-modul loyihada test pipeline

Multi-modul Maven/Gradle loyihasida pipeline arxitekturasi modul grafigidan kelib chiqadi. Birinchi qadam - grafikni aniq va yuzaki (shallow) qilish: agar har bir modul `common` ga bog'liq bo'lsa, `common` dagi har o'zgarish butun suite'ni ishga tushiradi va selection'ning ma'nosi qolmaydi. Shuning uchun `common` ni mayda, barqaror modullarga bo'lish amaliy qiymat beradi.

Test util modullari (`test-support`, `testcontainers-fixtures`) `test-jar` yoki alohida artifact bo'lib chiqariladi, shunda har bir service uni `test` scope'da oladi - takroriy Testcontainers konfiguratsiyasi, umumiy fixture va assertion'lar bir joyda saqlanadi.

Versiyalash ikki modelda bo'ladi: bitta umumiy versiya (release train - barcha modullar birga chiqadi, oddiy, lekin bog'liq) yoki modul-bo'yicha mustaqil versiya (moslashuvchan, lekin matritsa testini talab qiladi). Release train monorepo'da ko'pincha to'g'ri tanlov: pipeline oddiy bo'ladi va contract test matritsasi kichik qoladi. Mustaqil versiyalashni tanlasangiz, contract test majburiy - aks holda modullar orasidagi moslik faqat production'da tekshiriladi.

Nashr qilinmagan lokal kutubxona versiyasini iste'molchida sinash uchun `mavenLocal()` ko'pincha init skript (`~/.gradle/init.d/`) orqali qo'shiladi. Iste'molchining repozitoriylari ichki guruhni `exclusiveContent` va guruh filtri (`includeGroup`) bilan faqat bitta registrdan olishga majburlasa, init skript qo'shgan `mavenLocal()` shu guruh uchun chetlab o'tiladi: Gradle guruhni faqat exclusive repoga yo'naltiradi, lokal versiya topilmaydi yoki registrdagi eski nusxa olinadi. Repo faylini tahrir qilmaslik yo'li: registr URL i xossadan o'qilsa (`providers.gradleProperty`), uni vaqtincha lokal repoga qaratish.

```bash
# 1. Kutubxonada: nashr qilinmagan versiyani lokal repoga chiqarish
./gradlew publishToMavenLocal

# 2. Iste'molchida: URL xossasini lokal repoga qaratish, build fayllariga tegmasdan
./gradlew test -PinternalRepoUrl="file://$HOME/.m2/repository" --refresh-dependencies

# 3. Kutubxona nashr qilingach: xossani olib tashlash va lokal nusxani o'chirish
rm -rf "$HOME/.m2/repository/com/example/internal/order-lib/1.4.0"
```

Tozalash majburiy qadam: `-P` ni `~/.gradle/gradle.properties` ga yozib qo'ymang, lokal nusxa qolib ketsa keyingi build jim holda registrdagisini emas, shuni oladi va CI da boshqacha natija chiqadi.

## 15.14 Pipeline'ni ishonchli qilish

Pipeline'ning ishonchliligi uning tezligidan muhimroq. Birinchi qoida - infratuzilma nosozligini test nosozligidan ajratish. Docker registry javob bermadi, runner diski to'ldi, network timeout - bular test nosozligi emas, lekin odatiy pipeline ularni bir xil "failed" sifatida ko'rsatadi. Yechim: infra bosqichlarini (image pull, dependency download, container startup) alohida step sifatida ajratish va ularning exit code'ini alohida ko'rish; keyin retry'ni faqat o'sha step'larga qo'llash.

**Main buzilganda birinchi harakat - rollback.** Google da har jamoada build uchun mas'ul navbatchi (Build Cop) bor: uning ishi testlarni kim buzganidan qat'i nazar yashil holatga qaytarish, va u xabar olganda qo'lidagi ishni qoldirib buni qiladi. Eng kuchli vositasi - rollback: aybdor o'zgarishni qaytarish tizimni ma'lum yaxshi holatga eng tez va eng xavfsiz tiklaydi, oldinga tuzatish esa xavfliroq taklif. Shu bilan birga **ma'lum yiqilgan test ustiga yangi ish commit qilinmaydi**: bu norma bo'lmasa, buzilgan main ustiga yangi o'zgarishlar yotib, sababni ajratish qiyinlashadi. Test va rollback bir-biriga tayanadi: testlar o'zgartirishga ishonch beradi, rollback qaytarishga; testsiz rollback xavfsiz emas, rollbacksiz buzilgan test tez tuzalmaydi.

**Aybdorni to'plamni bo'lib topish (culprit finding).** Bir necha o'zgarish birga sinalganda (bu tezlik uchun qilinadi) qizil natija to'plamning qaysi a'zosidan kelganini aytmaydi. Google da ikki yondashuv birga ishlaydi: tizim yiqilgan to'plamni alohida o'zgarishlarga bo'lib qayta yurgizadi, va muhandis qo'lida to'plam bo'ylab binar qidiruv qiladigan vosita bor. Muhim shart - avval nosozlikning haqiqiyligini tasdiqlash: flaky test va infratuzilma xatosi tufayli qizil bergan to'plamni bo'lib yurgizish bekor ish. Git da bu `git bisect run` bilan amalda bir xil ishlaydi.

```bash
# Yiqilgan to'plamda aybdor commitni topish
git bisect start HEAD <oxirgi-yashil-commit>
git bisect run ./mvnw -q -Dtest=OrderPaymentIT test
git bisect reset
```

Retry siyosati qat'iy bo'lishi kerak: `docker pull` va dependency download uchun retry - to'g'ri; test bajarilishi uchun retry - flaky testni yashirish, bu [16-bobda](16-flaky-testlar-test-qarzi-va-test-kodini.md) ko'rilgan jarayonni buzadi. Agar test retry kerak bo'lsa, u hodisa sifatida qayd etilsin va flaky sifatida belgilansin, jimgina yashil bo'lmasin.

Timeout har darajada: job uchun (`timeout-minutes: 25`), test uchun (`@Timeout` yoki `junit.jupiter.execution.timeout.testable.method.default=2 m`), container startup uchun (Testcontainers `withStartupTimeout`). Timeout bo'lmasa, osilgan test butun runner quotasini yeydi. Resurs tomoni: standart GitHub runner 2 vCPU / 7 GB RAM - bu Testcontainers bilan bir nechta container ko'targan integration suite uchun ko'pincha kam. Larger runner (4-8 vCPU) narxi bor, lekin 25 daqiqani 8 daqiqaga tushirsa, ishlab chiquvchi vaqti hisobida tez qaytadi. Nihoyat, Docker mavjudligini boshida tekshirish (`docker info`) va yo'q bo'lsa aniq xabar bilan tez yiqilish - 20 daqiqadan keyingi tushunarsiz `ContainerLaunchException` dan yaxshiroq.

"Could not complete execution for Gradle Test Executor N" xatosi test fork JVM o'lganini bildiradi: Gradle fork bilan aloqani yo'qotgan. Ko'pincha sabab heap `OutOfMemoryError`, konteyner killer (OOM killer) emas. Lokal mashinada fork ko'p, har biriga kam sinf tushadi va xato ko'rinmaydi. CI da fork kam, shuning uchun har fork ko'p sinf yuritadi va static maydonlar, context cache va katta fixture lar to'planib heap ni to'ldiradi.

Qayta chiqarish va dalil olish:

- Fork sonini bittaga tushiring (`-P<forks>=1` yoki `maxParallelForks = 1`) va test chiqish papkasini o'chiring, aks holda task up-to-date bo'lib yurmaydi.
- Dalilni doimiy qo'ying: heap dump va JVM xato fayli CI artefaktiga tushadi, taxmin kerak bo'lmaydi.
- Bitta forkda tartibga bog'liq testlar ham chiqadi: bir test JVM system property ga yozsa, keyingi test uni ko'radi.

```kotlin
import java.lang.management.ManagementFactory
import com.sun.management.OperatingSystemMXBean

tasks.withType<Test> {
    jvmArgs(
        "-XX:+HeapDumpOnOutOfMemoryError",
        "-XX:HeapDumpPath=build/test-crash",
        "-XX:ErrorFile=build/test-crash/hs_err_%p.log",
    )
    // fork sonini CPU dan tashqari konteyner xotirasi bilan ham cheklang
    val os = ManagementFactory.getOperatingSystemMXBean() as OperatingSystemMXBean
    val byMemory = (os.totalMemorySize / (1024L * 1024 * 1024) / 2).toInt().coerceAtLeast(1)
    maxParallelForks = minOf(Runtime.getRuntime().availableProcessors(), byMemory)
}
```

`OperatingSystemMXBean.getTotalMemorySize()` konteynerda cgroup chegarasini o'qiydi, host xotirasini emas. Kotlin DSL da `java.lang.management.ManagementFactory` ni to'liq nomi bilan yozib bo'lmaydi: `java` nomi `java {}` extension ga bog'lanadi, shuning uchun import qiling.

Odatiy sabablar:

- Static ArchUnit importlari: `static final JavaClasses` maydoni yuzlab MB lik grafni fork oxirigacha ushlaydi. Yechim: `SoftReference` bilan keshlangan umumiy yordamchi yoki `@AnalyzeClasses` keshi.
- Spring test context cache: sukut bo'yicha 32 ta context saqlanadi, har xil konfiguratsiyali testlar ko'p context ochadi.
- Katta fixture: har testda to'liq qayta yaratiladigan yoki static ushlanadigan ma'lumot.
- Test system property yoki environment ga yozishi: `StandardEnvironment.getSystemProperties()` haqiqiy JVM `System.getProperties()` ni qaytaradi, yozilgan qiymat shu fork dagi keyingi testlarga sizadi. Yechim: `environment.getPropertySources().addFirst(new MapPropertySource(..))`.

## 15.15 Anti-patternlar

Hamma testni har push'da ishga tushirish. Boshida to'g'ri ko'rinadi, loyiha o'sgach PR vaqti 45 daqiqaga chiqadi. To'g'ri yo'l - bosqichli strategiya va selection, nightly safety net bilan.

Qizil build bilan yashash. Main qizil bo'lib bir kundan ortiq turgan har bir soat - barcha signalning qiymatini nolga olib boradi. Qoida qattiq: buzilgan main eng yuqori prioritet, tuzatish yoki revert, uchinchi variant yo'q.

Flaky testni retry bilan yashirish. `retryFailedTests` qo'yib, qizil rangni yashilga aylantirish - eng qimmat qarz turi: endi siz real nosozlikni ham ko'rmaysiz.

Testni CI'da o'tkazib yuborish. `-DskipTests`, `@Disabled` kommentsiz, `@Ignore` "keyin tuzataman" bilan - bular hech qachon qaytib kelmaydi. Agar test o'chirilsa, muddat va ticket bilan o'chirilsin.

Faqat main'da test qilish. PR'da hech narsa ishlamasa, nosozlik main'ga tushgandan keyin aniqlanadi va kim buzganini topish qimmatlashadi.

Lokal va CI natijasining farqi. "Mening mashinamda ishlaydi" - bu pipeline dizayni muammosi: timezone, locale, Java versiyasi, Docker yoki fayl tizimi farqlari. Yechim - bir xil Java versiyasini wrapper/toolchain bilan qotirish, `-Duser.timezone=UTC` va `file.encoding=UTF-8` ni ikki joyda bir xil qo'yish, Testcontainers'ni lokalda ham ishlatish.

## 15.16 Test ijarasi (tenancy) bilan production'da testlash

15.12-bo'limdagi texnikalar test trafigini production'dan feature flag va shadow traffic bilan ajratadi. To'rtinchi yo'l boshqacha: so'rovga ijara (tenancy) konteksti qo'shiladi, u zanjir bo'ylab tarqaladi va har bir servis so'rov production, test yoki beta ijarasiga tegishli ekanini bilib, unga boshqacha ishlov beradi. Orosz buni Uber amaliyoti sifatida keltiradi: test ijarasidagi so'rovni olgan to'lov tizimi haqiqiy to'lovni amalga oshirmaydi, uni mock qiladi (Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 17-bob, 251-bet; shu kitob, 14-bob, 205-bet).

Kitobda g'oya nasrda berilgan, kod misoli yo'q; quyida u Spring MVC ga ko'chirilgan: ijara filter'da o'qiladi, adapter esa uni qaror nuqtasi sifatida ishlatadi.

```java
public enum Tenancy { PRODUCTION, TEST }

public final class TenancyContext {
    private static final ThreadLocal<Tenancy> CURRENT = new ThreadLocal<>();

    public static Tenancy current() {
        return CURRENT.get() == null ? Tenancy.PRODUCTION : CURRENT.get();
    }

    public static void set(Tenancy tenancy) { CURRENT.set(tenancy); }

    public static void clear() { CURRENT.remove(); }
}

@Component
public class TenancyFilter extends OncePerRequestFilter {

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain chain)
            throws ServletException, IOException {
        // ijara faqat ishonchli chegaradan keladi: tashqi so'rovda bu header o'chiriladi
        TenancyContext.set("test".equals(request.getHeader("X-Tenancy")) ? Tenancy.TEST : Tenancy.PRODUCTION);
        try {
            chain.doFilter(request, response);
        } finally {
            TenancyContext.clear();
        }
    }
}

@Service
public class PaymentGateway {

    private final PaymentClient real;
    private final PaymentClient stub;

    public PaymentGateway(PaymentClient real, PaymentClient stub) {
        this.real = real;
        this.stub = stub;
    }

    public PaymentResult charge(Order order) {
        return TenancyContext.current() == Tenancy.TEST ? stub.charge(order) : real.charge(order);
    }
}
```

Narxi kichik emas. Ijara kontekstini HTTP, Kafka va scheduler chegaralarida ham uzatish kerak (header propagatsiyasi, MDC yoki tracing baggage); `ThreadLocal` asinxron ishga o'tgan joyda yo'qoladi, shuning uchun uzatish nuqtalari testda qoplansin. Zanjirning bitta bo'g'ini ijarani bilmasa, test so'rovi real yon ta'sirga aylanadi. Test ma'lumoti analitikadan chiqariladi, PII qoidalari esa test ijarasi uchun ham kuchda qoladi.

Buning evaziga qatlamlar soni kamayadi: Orosz ko'p ijara qo'yilgan joyda bir nechta alohida test muhitini saqlashga ehtiyoj qolmasligini aytadi, ya'ni tekshiruv qatlamlari qo'shiladigan emas, bir-birini almashtiradigan tanlov (o'sha bob, 251-bet).

## 15.17 Integratsiya chastotasi va sakkizta integratsiya strategiyasi

Pipeline bosqichlari "qachon test ishlaydi" savoliga javob beradi, bu bo'lim esa undan oldingi savolga: bo'laklar bir-biriga **qanday tartibda** qo'shiladi. McConnell ikki chastota va olti tartib strategiyasini nomlaydi; tanlov integratsiya xatosini qidirish narxini belgilaydi, shuning uchun u CI sozlamasidan oldin turadigan qaror.

**Fazali integratsiya (phased).** Uch qadam: har bir sinf alohida yoziladi va testdan o'tadi, keyin hammasi bir vaqtda bitta tizimga qo'shiladi, keyin butun tizim debug qilinadi. Kitob uni "big bang integration" deb ham ataydi: sinflar birinchi marta birga ishlaganda muammolar bir vaqtda chiqadi, ayblanuvchi esa har qanday sinf, har qanday interfeys yoki ularning o'zaro ta'siri bo'lishi mumkin. Muammolar bir-birini niqoblaydi va integratsiya loyihaning oxirigacha boshlanmaydi. Kitob bu usulni faqat juda kichik, ikki-uch sinfli dasturga o'rinli deb beradi (McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 29.2 (691-692-bet)).

**Inkremental integratsiya.** Avval tizimning kichik, ishlaydigan qismi (skelet) yoziladi va to'liq testdan o'tkaziladi, keyin har bir yangi sinf shu skeletga bittalab qo'shiladi va har qo'shilishdan keyin kombinatsiya tekshiriladi. Birlik sinfdan kattaroq (yaxshi tekshirilgan komponent) bo'lishi ham mumkin. Kitob oltita foydani sanaydi: xatoni joylashtirish oson (yangi sinf aniq ayblanuvchi), tizim loyihaning boshida ishlay boshlaydi, taraqqiyotni kuzatish aniqlashadi, mijoz munosabati yaxshilanadi, birliklar butun tizim qismi sifatida ko'proq mashq qiladi va ish qismlarini parallel qilish hisobiga jadval qisqaradi. Interfeys xatosining ulushi sezilarli: bir loyiha hisobida xatolarning 39 foizi modullar orasidagi interfeys xatosi bo'lgan (o'sha joy, 29.2 (693-694-bet)).

Qolgan oltitasi inkremental integratsiyaning tartib strategiyalari (o'sha joy, 29.3 (694-701-bet)). Kitobning o'z ogohlantirishi: ularning hech biri hamma holat uchun eng yaxshi emas.

- **Yuqoridan-pastga (top-down).** Ierarxiyaning yuqorisidagi sinf birinchi yoziladi, pastdagilar o'rniga **stub** qo'yiladi va integratsiya davomida stublar haqiqiy sinflarga almashtiriladi. Foydasi: boshqaruv mantiqi va katta konseptual dizayn muammolari erta ochiladi, qisman ishlaydigan tizim erta paydo bo'ladi. Narxi: tizim interfeyslari oxirigacha sinalmay qoladi va juda ko'p stub kerak bo'ladi; stub test kodi bo'lgani uchun unda production koddan ko'proq xato bo'ladi, bu esa inkremental integratsiyaning maqsadini buzadi. Sof shaklda deyarli qo'llanmaydi: amalda tizim yuqoridan pastga, lekin bo'laklab (vertical slice) qilinadi.
- **Pastdan-yuqoriga (bottom-up).** Ierarxiyaning pastidagi sinflar birinchi yoziladi va ularni mashq qilish uchun **test driver** yoziladi; yuqori sinflar paydo bo'lgani sayin driverlar haqiqiy sinflarga almashtiriladi. Foydasi: xato manbasi bitta sinfga chegaralanadi va tizim interfeyslari erta sinaladi. Narxi: yuqori darajadagi interfeyslar oxirigacha qoladi, shuning uchun konseptual dizayn xatosi hamma mayda ish bitgandan keyin ochiladi; shu sababli kitob yuqori darajadagi dizaynni past darajadagi koddan oldin yakunlashni talab qiladi.
- **Sendvich (sandwich).** Myers tavsiyasi: avval yuqoridagi biznes-obyekt sinflari, keyin pastdagi qurilma interfeysi va keng ishlatiladigan utility sinflari integratsiya qilinadi, o'rta qatlam oxiriga qoldiriladi. Sof yuqoridan-pastga va sof pastdan-yuqoriga qattiqligidan qutqaradi va kerakli scaffolding ni kamaytiradi.
- **Xavf bo'yicha (risk-oriented).** Kitobning ikkinchi nomi - "hard part first". Har bir sinfga xavf darajasi qo'yiladi va eng qiyin qismlar birinchi integratsiya qilinadi. Natija sendvichga o'xshaydi (tepa va tag birinchi), lekin sababi boshqa: tepadagi interfeyslar va tizim interfeyslari tajribaga ko'ra xavfli, shu bilan birga o'rtadagi yomon tushunilgan algoritm yoki qattiq performance maqsadi bor sinf ham ro'yxat boshiga chiqishi mumkin.
- **Xususiyat bo'yicha (feature-oriented).** Bir vaqtda bitta xususiyat integratsiya qilinadi, ya'ni "inkrement" bitta sinfdan katta bo'ladi. Uch foydasi: past darajadagi umumiy kutubxonalardan boshqa joyda scaffolding yo'qoladi, chunki har bir xususiyat kerakli kodni o'zi bilan olib keladi; har bir integratsiya ko'rinadigan funksionallik qo'shadi; va u obyektga yo'naltirilgan dizayn bilan mos tushadi. Narxi: inkrement kattalashgani uchun yangi xatoning manbasi bitta sinfga chegaralanmaydi.
- **T shaklida (T-shaped).** Bitta vertikal bo'lak tanlanadi, u tizimni uchidan uchiga mashq qiladi va arxitektura taxminlaridagi katta muammolarni ochadi; vertikal bo'lak ishlagandan keyin tizimning kengligi qurib boriladi. Kitob uni ko'pincha xavf bo'yicha yoki xususiyat bo'yicha strategiya bilan birga ishlatishni aytadi.

Kitobdagi misollar C++ va ierarxiya diagrammasi shaklida; quyida ikki rolning Java dagi eng kichik ko'rinishi - stub bilan yuqoridan-pastga va driver bilan pastdan-yuqoriga.

```java
// Yuqoridan-pastga: PaymentClient hali yozilmagan, o'rnida stub turadi
private final PaymentClient stub = order -> PaymentResult.approved("stub-ref");

@Test
void marksOrderPaidWhenGatewayApproves() {
    CheckoutService service = new CheckoutService(stub, new InMemoryOrderRepository());

    assertThat(service.checkout(anOrder().withTotal("1500").build()).status())
            .isEqualTo(Status.PAID);
}

// Pastdan-yuqoriga: repository tayyor, uni mashq qiladigan driver test
@DataJpaTest
class OrderRepositoryBottomUpTest {

    @Autowired
    private OrderRepository repository;

    @Test
    void findsOpenOrdersByCustomer() {
        repository.save(anOrder().forCustomer(1L).withStatus(Status.NEW).build());

        assertThat(repository.findOpenByCustomerId(1L)).hasSize(1);
    }
}
```

| Strategiya | Nima kerak bo'ladi | Nimani erta ochadi |
|---|---|---|
| Fazali | Hech narsa | Hech narsa: hammasi oxirida chiqadi |
| Yuqoridan-pastga | Stub (ko'p) | Boshqaruv mantiqi, UI, konseptual dizayn |
| Pastdan-yuqoriga | Test driver | Tizim va infratuzilma interfeyslari |
| Sendvich | Ikkisi ham, lekin kamroq | Tepa va tagdagi muammolar |
| Xavf bo'yicha | Xavf ro'yxati | Eng qimmat noma'lumlik |
| Xususiyat bo'yicha | Skelet | Foydalanuvchiga ko'rinadigan funksionallik |
| T shaklida | Bitta uchidan uchiga yo'l | Arxitektura taxminlari |

Korpusda bitta strategiya allaqachon amalda tavsiya qilingan, lekin nomlanmagan: [review ni bo'lish: stacked PR texnikasi](../code-review/02-review-iqtisodi-xato-narxi-navbat-va-pr.md#26-review-ni-bolish-stacked-pr-texnikasi) katta ishni migratsiya, domen va controller tartibida uch PR ga bo'lishni aytadi. Bu aynan pastdan-yuqoriga integratsiya: sxema va entity pastda, domen o'rtada, tashqi API tepada, va har bosqich o'zidan pastdagisi yashil bo'lgandan keyin qo'shiladi. Shu nom bilan uning narxi ham ko'rinadi: tashqi API shakli oxirigacha sinalmaydi, shuning uchun uchinchi PR da kontrakt o'zgarsa, oldingi ikkitasi qayta ishlanadi. T shaklidagi variant bu narxni kamaytiradi - birinchi PR da bitta uchidan uchiga yupqa yo'l (bitta endpoint, bitta jadval, bitta domen qoidasi) chiqariladi, kenglik keyin qo'shiladi.

ESLATMA: Spring loyihasida stub va driver nomlari boshqacha ko'rinadi. Stub rolini `@MockitoBean` yoki qo'lda yozilgan fake bean bajaradi, driver rolini esa `@SpringBootTest` ko'tarmagan oddiy JUnit test sinfi yoki `@DataJpaTest` kabi slice bajaradi; kitobdagi "scaffolding ni kamaytirish" argumenti shu yerda "qancha mock bean kerak" savoliga aylanadi.

## 15.18 Arxitektor nazorat ro'yxati

- [ ] Pipeline bosqichlari fail fast printsipi bo'yicha tartiblangan, PR gate va merge pipeline aniq ajratilgan
- [ ] Feedback vaqti byudjeti yozilgan (PR < 10 daq), p95 metrika sifatida kuzatiladi va buzilganda aniq harakat rejasi bor
- [ ] Surefire (`*Test`) va Failsafe (`*IT`) ajratilgan, JUnit 5 parallel execution va sharding sozlangan hamda flaky bermasligi tasdiqlangan
- [ ] Dependency kesh, Gradle build cache, Testcontainers image pre-pull yoqilgan va Spring kontekst keshi buzilmasligi tekshirilgan; test selection faqat PR darajasida, to'liq suite nightly safety net sifatida majburiy
- [ ] Required check'lar ro'yxati ongli tanlangan (deterministik va tez), merge queue zarurati baholangan
- [ ] Nosozlik artefaktlari (JUnit XML, log, screenshot, heap dump) `if: failure()` da saqlanadi va PR'da xulosa ko'rinadi
- [ ] Deploy'dan keyin smoke test, canary metrikasi va avtomatik rollback sharti raqamlar bilan belgilangan
- [ ] Retry faqat infratuzilma step'larida; har bir nightly suite'ning nomlangan egasi va nosozlik marshruti bor

## Manbalar

- [JUnit 5.11, Running Tests](https://raw.githubusercontent.com/junit-team/junit5/r5.11.0/documentation/src/docs/asciidoc/user-guide/running-tests.adoc) - teg bo'yicha tanlash (`@Tag`, `includeTags`), `junit-platform.properties` va parallel bajarish sozlamalari, ya'ni pipeline da testni bosqichga bo'lish mexanizmi
- [maven-surefire, `TestSuiteXmlParser.java`](https://raw.githubusercontent.com/apache/maven-surefire/0c970adeb11e8a59b449be5b3be2a50c478c2a65/surefire-report-parser/src/main/java/org/apache/maven/plugins/surefire/report/TestSuiteXmlParser.java) - JUnit XML hisobotining tarkibi, CI da yig'iladigan maydonlar
- [Google, Speed of Code Reviews](https://raw.githubusercontent.com/google/eng-practices/3bb3ec25b3b0199f4940b1aa75f0ac5c5753301c/review/reviewer/speed.md) - javob tezligining jamoa oqimiga ta'siri, ya'ni pipeline vaqtining tashkiliy narxi
- [sonarqube 9.9 LTA, `ScanProperties.java`](https://raw.githubusercontent.com/SonarSource/sonarqube/9.9.8.100196/sonar-scanner-engine/src/main/java/org/sonar/scanner/scan/ScanProperties.java) - `sonar.qualitygate.wait` bilan pipeline ni bloklash va 300 sekundlik default timeout
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 23-bob ("Continuous Delivery", "CI Is Alerting", "Scenario #3: Debugging 'All of Google'") - release candidate ning kod va statik konfiguratsiyani birga olishi va muhitlar bo'ylab qayta qurilmasligi, CI ning ogohlantirish tizimi sifatida qarashi va 100 foiz yashillikning narxi, bitta to'plamni production ga qarshi ham yurgizib nosozlikni ajratish. Bu nashrning nusxasida barqaror bet raqami yo'q, shuning uchun bob va bo'lim nomi ko'rsatilgan
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 23-bob ("Culprit Finding", "Failure Management") - yiqilgan to'plamni alohida o'zgarishlarga bo'lib qayta yurgizish va binar qidiruv, Build Cop roli, rollback ning oldinga tuzatishdan xavfsizligi, ma'lum yiqilgan test ustiga commit qilmaslik normasi. Bu nashrning nusxasida barqaror bet raqami yo'q, shuning uchun bob va bo'lim nomi ko'rsatilgan
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 14-bob ("Configuration Issues", "Deployment Configuration Testing") - konfiguratsiya o'zgarishi katta nosozliklarning birinchi sababi ekani va konfiguratsiyani versiya nazoratida saqlab ishga tushirish sinovini katta test sifatida yurgizish. Bu nashrning nusxasida barqaror bet raqami yo'q, shuning uchun bob va bo'lim nomi ko'rsatilgan
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 1-bob ("Scale and Efficiency") - to'liq build vaqti, toza klon vaqti va til versiyasini yangilash narxi kabi sekin o'sadigan xarajatlarning kuzatilmasligi va ularning birdan inqirozga aylanmasligi. Bu nashrning nusxasida barqaror bet raqami yo'q, shuning uchun bob va bo'lim nomi ko'rsatilgan
- Sam Newman, *Building Microservices: Designing Fine-Grained Systems*, 2-nashr, O'Reilly, 2021, 7-bob ("Continuous Delivery Versus Continuous Deployment", "Tooling") - continuous delivery har check-in ni release candidate deb baholashi, continuous deployment uning davomi ekani va hamma uchun shart emasligi, qo'lda tasdiqning CD bilan mosligi, pipeline ni birinchi darajali tushuncha sifatida modellaydigan vosita tanlash. Bu nashrning nusxasida barqaror bet raqami yo'q, shuning uchun bob va bo'lim nomi ko'rsatilgan
- Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 17-bob "Shipping to Production" (251-bet) va 14-bob "Testing" (205-bet) - ijara konteksti so'rov bilan tarqaladi va servislar unga qarab boshqacha yo'naltiradi, test ijarasidagi to'lov mock qilinadi, ko'p ijara qo'yilganda alohida test muhitlariga ehtiyoj kamayadi
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 29.2-29.3 "Integration" (691-701-bet) - fazali va inkremental integratsiya farqi, inkremental integratsiyaning oltita foydasi va olti tartib strategiyasi: yuqoridan-pastga (stub), pastdan-yuqoriga (test driver), sendvich, xavf bo'yicha, xususiyat bo'yicha va T shaklida

---

[&larr; 14. Arxitektura testlari va kod sifati darvozalari](14-arxitektura-testlari-va-kod-sifati.md) · [Mundarija](README.md) · [16. Flaky testlar, test qarzi va test kodini saqlash &rarr;](16-flaky-testlar-test-qarzi-va-test-kodini.md)
