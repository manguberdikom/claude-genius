<!-- doc: testing | chapter: 14 | part:  -->

[Barcha hujjatlar](../../README.md) / [Testlash qo'llanmasi](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 14. Arxitektura testlari va kod sifati darvozalari (Architecture Tests & Code Quality Gates)

<details>
<summary>Bu bobdagi 14 bo'lim</summary>

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

</details>



Arxitektura faqat hujjatda yashasa, u birinchi muddat siqig'ida o'ladi: diagramma wiki'da qoladi, kod esa boshqa yo'ldan ketadi. Arxitektorning eng arzon va eng ta'sirli vositalaridan biri - qoidani matn sifatida emas, bajariladigan test sifatida yozish va uni kod sifati darvozalari qatoriga qo'yish. Bu bobda ArchUnit va Spring Modulith bilan chegaralarni mustahkamlash, JaCoCo, PIT, statik tahlil va SonarQube darvozalarini sozlash ko'rib chiqiladi. Oxirida esa eng qiyin qism: bu darvozalarni mavjud loyihaga jamoani sindirmasdan joriy qilish.

## 14.1 Qoidani hujjat emas, test qilib yozish

Arxitektura qoidasi uch joyda yashashi mumkin: kimningdir boshida, hujjatda yoki testda. Birinchisi jamoa o'zgarishi bilan yo'qoladi, ikkinchisi oyiga bir marta o'qiladi, uchinchisi har commit'da tekshiriladi. "Controller repository'ni chaqirmaydi" degan jumla wiki'da turganda maslahat, `ArchRule` sifatida yozilganda esa shartnoma.

Code review nega yetarli emas? Reviewer - odam: charchaydi va 900 qatorli PR'da import blokidagi bitta yangi paketni ko'rmaydi. Qoida bilimi notekis taqsimlangan: yangi dasturchi "domain paketi Spring'ga bog'lanmaydi" shartini bilmaydi, tajribali reviewer esa buni har safar qo'lda tushuntiradi. "Faqat bu safar" istisnolari hech qayerda qayd etilmaydi va olti oydan keyin normaga aylanadi. Va qoida shaxsiy mavzuga aylanadi: "men shunday yozdim, u esa yoqtirmadi". Test shaxssiz - build qizil bo'ldi, muhokama tugadi.

Shu bilan birga test review'ni almashtirmaydi, uni tozalaydi: test mexanik invariantlarni (bog'liqlik yo'nalishi, annotatsiya joyi, nomlanish, cycle) oladi, review esa dizaynning maqsadga mosligini. Istisno ham kodda yashashi kerak: qoidani buzish zarur bo'lsa, bu `@ArchIgnore`, freeze store yozuvi yoki `because(...)` izohi orqali ko'rinadigan va audit qilinadigan bo'lishi lozim.

## 14.2 ArchUnit asoslari

ArchUnit - oddiy Java kutubxonasi: bayt-kodni o'qiydi, `JavaClasses` modelini quradi va unga qoidalarni qo'llaydi. Alohida agent yoki maxsus runner kerak emas, qoida oddiy JUnit 5 testi sifatida ishlaydi (`archunit-junit5` artifact'i). ArchUnit 1.x'da asosiy elementlar quyidagilar: `ArchRuleDefinition.classes()`, `noClasses()`, `methods()`, `noMethods()`, `fields()` subyektni tanlaydi; `.that(...)` uni filtrlaydi; `.should(...)` talabni bildiradi; `.because(...)` xato matniga sababni qo'shadi. `@AnalyzeClasses` import qilingan klasslarni keshlaydi, `@ArchTest` esa `static final ArchRule` maydoni yoki `void method(JavaClasses)` metodi bo'lishi mumkin.

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

Mavjud loyihada yangi qoidani yoqsangiz, yuzlab buzilish chiqadi va jamoa qoidani emas, testni o'chiradi. `FreezingArchRule` buni hal qiladi: birinchi ishga tushishda mavjud buzilishlarni violation store'ga yozib testni yashil qiladi, keyin faqat yangi buzilishlar xato beradi. Buzilish tuzatilsa store qisqaradi - ratchet bir tomonga aylanadi.

```java
@ArchTest
static final ArchRule domain_toza = FreezingArchRule.freeze(
        noClasses().that().resideInAPackage("..domain..")
                .should().dependOnClassesThat()
                .resideInAnyPackage("org.springframework..", "jakarta.persistence..")
                .because("domain model framework'dan mustaqil bo'ladi"));
```

Store yo'li `archunit.properties` da `freeze.store.default.path` va `freeze.store.default.allowStoreCreation=true` bilan boshqariladi. Store'ni git'ga qo'shing: u texnik qarzning ko'rinadigan ro'yxatiga aylanadi.

## 14.3 Amaliy ArchUnit qoidalari to'plami

Qatlamlarni o'nlab `noClasses()` qoidasi bilan emas, `Architectures.layeredArchitecture()` bilan tasvirlash qulay - xato xabari ham tushunarli chiqadi.

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

Keyingi to'plam - kundalik xatolarni ushlaydigan qoidalar. `GeneralCodingRules` ichida tayyori bor: `NO_CLASSES_SHOULD_USE_FIELD_INJECTION` (konstruktor injection majburiy), `NO_CLASSES_SHOULD_ACCESS_STANDARD_STREAMS` (`System.out.println` ta'qiqi).

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

Oxirgi ikkisi - aylanma bog'liqlik va test nomlash konvensiyasi. Cycle tekshiruvi `SlicesRuleDefinition` orqali bajariladi va amalda eng foydali qoidalardan biri: aylanma bog'liqlik modullashtirishni imkonsiz qiladi.

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

## 14.4 Spring Modulith bilan modul chegaralarini tekshirish

Spring Modulith 1.x paketni modul deb qabul qiladi: application klassining to'g'ridan-to'g'ri ost-paketlari - modullar, ularning ichki ost-paketlari esa modulning yopiq qismi. Boshqa moduldan faqat modulning yuqori darajadagi tipiga yoki `@NamedInterface` bilan belgilangan paketga murojaat qilish mumkin. Bu modular monolitni saqlashning eng arzon yo'li: paket qoidalarini qo'lda yozish o'rniga bitta `verify()` barcha chegarani tekshiradi.

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

`Documenter` PlantUML (C4 uslubidagi) diagrammalarini va har bir modul uchun "canvas" (ochiq API, event'lar, konfiguratsiya xossalari) hujjatini `target/spring-modulith-docs` ichiga yozadi. Bu hujjat qo'lda yangilanmaydi - har build'da kodan qayta tug'iladi va eskirmaydi.

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

## 14.5 Test coverage: JaCoCo

JaCoCo Java agent sifatida ulanadi va bajarilgan bayt-kodni hisoblaydi. Muhim farq - counter turlari: `LINE` qator bajarildimi deb so'raydi, `BRANCH` esa shart ifodasining har ikki tarmog'i sinalganini tekshiradi. `if (a && b)` bitta qator, lekin to'rt tarmoq: line coverage 100%, branch coverage 25% bo'lishi mumkin. Shuning uchun chegara `BRANCH` ustiga qo'yiladi.

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

Generatsiya qilingan kodni chiqarib tashlash shart: MapStruct `*MapperImpl`, jOOQ/OpenAPI generatori, protobuf. Lombok uchun `lombok.config` ga `lombok.addLombokGeneratedAnnotation = true` qo'ying - JaCoCo nomi `Generated` bo'lgan annotatsiyali kodni o'zi e'tiborsiz qoldiradi. DTO va record'larda tekshirishga arziydigan logika yo'q.

Eng muhim qaror - chegarani belgilash. Umumiy foiz ("80% bo'lsin") yaroqsiz: eski loyihada erishilmas, yangisida ma'nosiz oson. To'g'ri yondashuv - o'zgargan kod uchun chegara (diff coverage): "bu PR'da qo'shilgan yoki o'zgargan qatorlarning kamida 80% qoplangan bo'lsin". SonarQube buni New Code ustidan o'zi hisoblaydi, Sonar bo'lmasa `diff-cover` kabi vositalar JaCoCo XML hisobotini git diff bilan birlashtiradi. Umumiy foiz esa faqat trend sifatida kuzatiladi: tushib ketmasin, shu kifoya.

Coverage nimaga yaraydi: qoplanmagan joyni topishga. "Bu `catch` bloki bajarilmagan", "bu `else` sinalmagan" - real signal. Nimaga yaramaydi: sifat ko'rsatkichi bo'lishga, chunki u kod bajarilganini aytadi, natija tekshirilganini aytmaydi.

## 14.6 Coverage anti-patternlari

Birinchi anti-pattern - 100% quvish. Oxirgi 15% eng qimmat va eng kam foydali qism: `toString`, getter, `equals`, config klasslari, erishilmaydigan `default` branch'lar. Shu vaqt integration testlarga sarflansa, foyda bir necha barobar ko'p bo'ladi.

Ikkinchisi - assertion'siz test. Metodni chaqirib hech narsa tekshirmaydigan test coverage'ni ko'taradi, lekin bitta xatoni ham ushlamaydi. Bundan yomoni - `assertThat(result).isNotNull()` bilan tugaydigan testlar: ular tekshirayotgandek ko'rinadi va coverage KPI bo'lgan jamoalarda o'z-o'zidan paydo bo'ladi.

Uchinchi va eng xatarli - coverage'ni KPI yoki bonus mezoni qilish. Goodhart qonuni aniq ishlaydi: ko'rsatkich maqsadga aylansa, u ko'rsatkich bo'lishdan to'xtaydi. Jamoa foizni ko'taradi, test suite esa sifatsiz qoladi. Arxitektor pozitsiyasi aniq bo'lsin: foizga emas, coverage pasayishi sababiga qaraymiz, test sifatini esa mutation testing o'lchaydi.

## 14.7 Mutation testing: PIT

PIT (pitest) bayt-kodga kichik o'zgartirishlar - mutatsiyalar - kiritadi va testlarni qayta ishga tushiradi. Mutatsiyadan keyin ham barcha test yashil bo'lsa, mutatsiya "tirik qoldi" (survived): test suite o'sha xatti-harakatni tekshirmaydi. Mutation score = o'ldirilgan mutatsiyalar / jami mutatsiyalar. Coverage "bu qator bajarildimi?" deb so'raydi, PIT "bu qatorni buzsam, testlar sezadimi?" deb - bu ancha qimmatli savol.

`pitest-maven` va `pitest-junit5-plugin` ni ulash, `targetClasses`, `mutationThreshold` va Gradle varianti [SonarQube hujjatidagi PIT ni Maven va Gradle da ishga tushirish](../sonarqube/20-mutation-testing-100-coverage-qachon-yolgon.md#205-pit-pitest-ni-maven-va-gradle-da-ishga-tushirish) bo'limida yozilgan, bu yerda faqat mutator tanlovi va CI darvozasidagi o'rni ko'riladi.

Mutator guruhlari: `DEFAULTS` (shart inkori, matematik amallar, `void` chaqiruvni o'chirish, return qiymatini almashtirish), `STRONGER` (ustiga `REMOVE_CONDITIONALS` va `EXPERIMENTAL_*` qismi) va `ALL`. Boshlash uchun `DEFAULTS` yetarli, domain yadrosi uchun `STRONGER` oqlanadi.

PIT sekin: har mutatsiya uchun testlar qayta ishlaydi. Uni cheklashning uch yo'li bor. Birinchisi - `targetClasses`'ni faqat biznes logikasi bilan cheklash: controller, config va DTO uchun mutation testing ma'nosiz. Ikkinchisi - `withHistory` va faqat o'zgargan sinflar: `org.pitest:pitest-maven:scmMutationCoverage` goal'i SCM holatiga qarab (`ADDED`, `MODIFIED`) faqat o'zgargan fayllarni tahlil qiladi, bu PR darvozasi uchun mos. Uchinchisi - to'liq tahlilni nightly'ga olib chiqish. Mutation score'ni bloklovchi qilishdan oldin kamida bir oy trend sifatida kuzating.

## 14.8 Statik tahlil: qaysi vositani tanlash

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

Amaliy tanlov: minimal to'plam - Spotless (format), Error Prone + NullAway (kompilyatsiyada), ArchUnit (chegaralar) va SonarQube (jamlovchi darvoza). Checkstyle'ning formatlash qismini Spotless bajargani uchun uni faqat qoida uchun qoldiring. PMD va SpotBugs Sonar bilan qisman takrorlanadi, lekin `findsecbugs` plugin'i bilan SpotBugs xavfsizlik uchun qiymat beradi.

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

## 14.9 SonarQube quality gate

Sonar'ning asosiy g'oyasi - New Code: baseline (oldingi versiya, N kun yoki reference branch) belgilanadi va darvoza shartlari faqat shundan keyin o'zgargan kodga qo'llaniladi. Standart "Sonar way" gate'i yangi kod uchun coverage kamida 80%, duplikatsiya 3% dan oshmasligi, Maintainability/Reliability/Security reytinglari A va security hotspot'larning 100% ko'rib chiqilganini talab qiladi. Eski kodda minglab muammo bo'lsa ham gate yashil bo'ladi - shuning uchun u mavjud loyihada ishlaydi.

```yaml
      - name: Sonar tahlili
        run: >
          ./mvnw -B verify sonar:sonar
          -Dsonar.projectKey=shop
          -Dsonar.qualitygate.wait=true
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

`sonar.qualitygate.wait=true` bo'lmasa, scanner natijani yuborib darhol muvaffaqiyat bilan tugaydi va gate amalda hech narsani bloklamaydi - bu eng ko'p uchraydigan xato. Gate buzilganda PR status check qizil bo'ladi, izohlar esa PR decoration orqali diff ustiga tushadi. Texnik qarzda ikki qoida muhim: muammolarni ommaviy "Won't fix" qilib yopmang va eski kodni rejalashtirilgan tarzda, eng ko'p o'zgaradigan fayllardan boshlab tozalang.

## 14.10 Bog'liqliklarni nazorat qilish

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

`dependencyConvergence` bitta kutubxonaning turli versiyalari transitiv kelib qolgan holatlarni ushlaydi - bu `NoSuchMethodError` kabi runtime xatolarining asosiy manbai. Ruxsat etilgan kutubxonalar ro'yxatini BOM orqali yuritish qulay: barcha versiyalar `dependencyManagement`da, `bannedDependencies` esa eski variantlarni to'sadi (JUnit 4, Joda-Time, `commons-logging`). Gradle'da shu vazifani `resolutionStrategy.failOnVersionConflict()` va platform/BOM bajaradi.

Litsenziya uchun `license-maven-plugin` (MojoHaus) `aggregate-add-third-party` goal'i va `failOnBlacklist` sozlamasi ishlatiladi: GPL yoki noma'lum litsenziya paydo bo'lsa build to'xtaydi. Zaxiralanmagan kutubxonani ushlashning avtomatik qoidasi yo'q, lekin ikki signal ishlaydi: `versions-maven-plugin` ko'rsatadigan so'nggi reliz sanasi (ikki yildan oshgan bo'lsa ko'rib chiqiladi) va yangi bog'liqlik qo'shilganda arxitektura review'i. Ma'lum zaifliklarni skanerlash (OWASP Dependency-Check, SCA) [13-bobda](13-nofunksional-testlar-performance-resilience.md) ko'rilgan; bu bobdagi darvoza sifat va moslik uchun.

## 14.11 Formatlash va pre-commit

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

## 14.12 Darvozalarni joylashtirish

Barcha tekshiruvni bitta joyga yig'ish - eng ko'p uchraydigan xato: PR 40 daqiqa kutadi va jamoa darvozani yoqtirmay qoladi. To'g'ri yondashuv - tekshiruvlarni tezligi bo'yicha bosqichlarga taqsimlash.

| Bosqich | Nima ishlaydi | Vaqt budjeti | Buzilganda |
| --- | --- | --- | --- |
| Lokal (IDE) | Error Prone kompilyatsiyada, IDE inspection, `.editorconfig` | darhol | dasturchi o'zi ko'radi |
| pre-commit | `spotless:apply`, ArchUnit tez qoidalari | 10 sekundgacha | commit to'xtaydi |
| PR (har push) | unit testlar, ArchUnit, `modules.verify()`, Spotless check, enforcer, Sonar PR tahlili | 10 daqiqagacha | PR qizil, merge bloklangan |
| Merge (main) | to'liq integration testlar, JaCoCo check, Sonar quality gate, litsenziya tekshiruvi | 30 daqiqagacha | main qizil, release bloklangan |
| Nightly | to'liq PIT, SpotBugs + findsecbugs, Dependency-Check, PMD/CPD | cheklanmagan | ticket ochiladi, release bloklanmaydi |

Qoida sodda: PR'da faqat tez va deterministik tekshiruvlar, sekin tahlillar nightly'ga. Har bir qizil nightly uchun javobgar va muddat belgilanadi.

## 14.13 Darvozalarni joriy qilish strategiyasi

Mavjud loyihada hamma darvozani birdan yoqish kafolatlangan muvaffaqiyatsizlik: birinchi hafta hamma PR qizil bo'ladi, keyingi haftada jamoa tekshiruvlarni `continue-on-error` qilib qo'yadi.

| Bosqich | Qadam | Talab darajasi |
| --- | --- | --- |
| 1 | Spotless + `.editorconfig`, `ratchetFrom` bilan | majburiy, lekin avtomatik tuzatiladi |
| 2 | ArchUnit, barcha qoida `freeze` bilan | yangi buzilish taqiqlangan |
| 3 | JaCoCo report + Sonar New Code gate | faqat o'zgargan kodga |
| 4 | Error Prone/NullAway, enforcer, litsenziya | bitta moduldan boshlab |
| 5 | PIT nightly, keyin kritik paketlarda PR gate | trend, keyin chegara |

Har bir bosqichda uch narsa qilinadi: baseline olinadi (freeze store, Sonar New Code sanasi, ogohlantirishlar soni), talab faqat yangi kodga qo'yiladi va istisno so'rash yo'li aniq bo'ladi. Jamoani ishontirishning eng yaxshi usuli - darvozani "jazolash" emas, "review'dan mexanik ishni olib tashlash" sifatida taqdim etish. Ikkinchisi - har bir qoidaning `because(...)` izohida sababni yozish: sababni biladigan dasturchi qoidani aylanib o'tmaydi.

Darvozalar ro'yxatini ham kod kabi yuriting: har chorakda ko'rib chiqing, bitta ham real xato ushlamagan qoidani o'chiring, soxta signal beradigan tekshiruvni tuzating. Hech kim ishonmaydigan qizil darvoza - darvoza emas.

## 14.14 Arxitektor nazorat ro'yxati

- [ ] Har bir muhim arxitektura qoidasi uchun buzilganda build'ni qizil qiladigan test bor (ArchUnit yoki `modules.verify()`), qoida wiki'da emas, repo'da yashaydi.
- [ ] Mavjud buzilishlar `FreezingArchRule` store'iga olingan, store git'da saqlanadi va uning o'sishi PR'da ko'rinadi.
- [ ] JaCoCo'da umumiy foiz emas, o'zgargan kod uchun chegara qo'yilgan; generatsiya qilingan kod, DTO va config `excludes`da.
- [ ] Coverage KPI yoki bonus mezoni emas; test suite sifati kritik paketlarda PIT mutation score bilan o'lchanadi.
- [ ] Sonar quality gate New Code uchun sozlangan va `sonar.qualitygate.wait=true` bilan PR'ni haqiqatan bloklaydi.
- [ ] Statik tahlil bosqichma-bosqich joriy qilingan: baseline olingan, yangi kodga qattiq, eski kodga yumshoq talab.
- [ ] Bog'liqlik darvozasi bor: `dependencyConvergence`, ban ro'yxati, litsenziya tekshiruvi va zaxiralanmagan kutubxona signali.
- [ ] Har bir darvoza uchun "qizil bo'lsa kim nima qiladi" qoidasi va istisno so'rash yo'li hujjatlashtirilgan.

---

[&larr; 13. Nofunksional testlar: performance, resilience, xavfsizlik](13-nofunksional-testlar-performance-resilience.md) · [Mundarija](README.md) · [15. CI/CD da test pipeline &rarr;](15-ci-cd-da-test-pipeline.md)
