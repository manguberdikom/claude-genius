<!-- doc: sonarqube | chapter: 10 | part: III. Qamrov (coverage) -->

[Barcha hujjatlar](../../README.md) / [SonarQube](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 10. JaCoCo va SonarQube ulanishi: Maven va Gradle sozlash (Wiring JaCoCo to SonarQube)

<details>
<summary>Bu bobdagi 12 bo'lim</summary>

- [10.1 Maven da JaCoCo plugin: `prepare-agent` va `report` bosqichlari](#101-maven-da-jacoco-plugin-prepare-agent-va-report-bosqichlari)
- [10.2 Hisobot yo'lini Sonar ga ko'rsatish: `sonar.coverage.jacoco.xmlReportPaths`](#102-hisobot-yolini-sonar-ga-korsatish-sonarcoveragejacocoxmlreportpaths)
- [10.3 Nega XML hisobot kerak va binar `exec` fayl yetarli emas](#103-nega-xml-hisobot-kerak-va-binar-exec-fayl-yetarli-emas)
- [10.4 Gradle da JaCoCo: `jacocoTestReport` va XML chiqishini yoqish](#104-gradle-da-jacoco-jacocotestreport-va-xml-chiqishini-yoqish)
- [10.5 Ko'p modulli Maven loyihasida yig'ma hisobot tayyorlash](#105-kop-modulli-maven-loyihasida-yigma-hisobot-tayyorlash)
- [10.6 Integratsion test qamrovini alohida yig'ib, keyin birlashtirish](#106-integratsion-test-qamrovini-alohida-yigib-keyin-birlashtirish)
- [10.7 Surefire va Failsafe bilan ishlash tartibi](#107-surefire-va-failsafe-bilan-ishlash-tartibi)
- [10.8 Coverage 0% ko'rinishi va uning sabablari](#108-coverage-0-korinishi-va-uning-sabablari)
- [10.9 Sozlashni tekshirish: qaysi faylga qarash, qaysi log qatorini izlash](#109-sozlashni-tekshirish-qaysi-faylga-qarash-qaysi-log-qatorini-izlash)
- [10.10 CI da tartib: test, hisobot, tahlil ketma-ketligi](#1010-ci-da-tartib-test-hisobot-tahlil-ketma-ketligi)
- [10.11 Oddiy yondashuv va arxitektor yondashuvi](#1011-oddiy-yondashuv-va-arxitektor-yondashuvi)
- [10.12 Amalda qo'llash](#1012-amalda-qollash)

</details>



Sonar coverage ni o'zi o'lchamaydi. U faqat JaCoCo tayyorlagan XML hisobotni o'qiydi va undagi raqamlarni quality gate shartlari bilan solishtiradi. Shuning uchun "coverage 0%" muammosining deyarli hammasi Sonar da emas, balki build sozlamasida: agent ulanmagan, XML yaratilmagan yoki yo'l noto'g'ri ko'rsatilgan. Bu bobda Maven va Gradle uchun to'liq ishlaydigan ulanish zanjiri va uni tekshirish tartibi beriladi.

## 10.1 Maven da JaCoCo plugin: `prepare-agent` va `report` bosqichlari

Zanjir ikki goal dan iborat. `prepare-agent` test JVM ga `-javaagent` argumentini qo'shadi, bu argument `argLine` nomli Maven property ga yoziladi. Testlar ishlaganda agent bayt kodni uchishda instrumentatsiya qiladi va natijani binar `jacoco.exec` fayliga yozadi. `report` goal shu binar fayl va `target/classes` dagi klasslarni solishtirib HTML, CSV va XML hisobot chiqaradi.

Muhim nuqta: `prepare-agent` odatda `initialize` fazasiga, `report` esa `verify` fazasiga bog'lanadi. Agar siz `mvn test` bilan to'xtasangiz, XML hali yaratilmagan bo'ladi. Shuning uchun `report` ni ataylab `test` fazasiga ko'chirish yoki build ni `verify` gacha olib borish kerak.

```xml
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <version>0.8.12</version>
  <executions>
    <execution>
      <id>jacoco-agentni-ulash</id>
      <goals>
        <goal>prepare-agent</goal>
      </goals>
    </execution>
    <execution>
      <!-- report ni test dan keyin darhol chiqaramiz -->
      <id>jacoco-xml-hisobot</id>
      <phase>test</phase>
      <goals>
        <goal>report</goal>
      </goals>
      <configuration>
        <!-- XML Sonar uchun, HTML odam uchun -->
        <formats>
          <format>XML</format>
          <format>HTML</format>
        </formats>
      </configuration>
    </execution>
  </executions>
</plugin>
```

JaCoCo versiyasini Java versiyasiga qarab tanlang. Yangi JDK chiqqanda JaCoCo ning eski versiyasi yangi class file major version ni tanimaydi va `Unsupported class file major version` xatosini beradi. Rasmiy qo'llab-quvvatlash shu versiyalardan boshlanadi ([JaCoCo changelog, v0.8.14](https://github.com/jacoco/jacoco/blob/v0.8.14/org.jacoco.doc/docroot/doc/changes.html)):

| Java | Eng past JaCoCo |
|---|---|
| 17 | 0.8.8 |
| 21 | 0.8.11 |
| 22 | 0.8.12 |
| 23, 24 | 0.8.13 |
| 25 | 0.8.14 |

Bu hujjat misollaridagi 0.8.12 Java 21 bazasi uchun yetarli. Java 25 da u class faylni tanimaydi, versiyani 0.8.14 ga ko'taring.

## 10.2 Hisobot yo'lini Sonar ga ko'rsatish: `sonar.coverage.jacoco.xmlReportPaths`

Sonar da coverage ni import qiladigan sensor nomi JaCoCo XML Report Importer. U faqat bitta parametrga qaraydi: `sonar.coverage.jacoco.xmlReportPaths`. Bu parametr vergul bilan ajratilgan ro'yxatni qabul qiladi, nisbiy yo'llar modul bazasiga nisbatan hisoblanadi.

`sonar-maven-plugin` ishlatilganda ko'p parametr pom dan avtomatik olinadi. Standalone scanner ishlatilganda esa hammasini qo'lda yozish kerak.

```properties
# Bitta modulli loyiha uchun root dagi sonar-project.properties
sonar.projectKey=shop-payment
sonar.projectName=Shop Payment Service
sonar.sources=src/main/java
sonar.tests=src/test/java
sonar.java.binaries=target/classes
sonar.java.test.binaries=target/test-classes
sonar.java.libraries=target/dependency/*.jar

# Coverage ning YAGONA manbasi
sonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml

# Test natijalari alohida parametr, coverage bilan aralashtirmaslik kerak
sonar.junit.reportPaths=target/surefire-reports,target/failsafe-reports

# Coverage talab qilinmaydigan joylar
sonar.coverage.exclusions=**/config/**,**/dto/**,**/*Application.java
```

`sonar.coverage.exclusions` va `sonar.exclusions` ni aralashtirib yubormang. Birinchisi faylni tahlilda qoldiradi, lekin coverage hisobidan chiqaradi. Ikkinchisi faylni butunlay tahlildan olib tashlaydi, ya'ni code smell va bug ham topilmaydi. Generated kod uchun ikkinchisi, konfiguratsiya klasslari uchun birinchisi to'g'ri keladi.

## 10.3 Nega XML hisobot kerak va binar `exec` fayl yetarli emas

Binar `jacoco.exec` fayli ichida faqat probe massivlari bor. Unda klass nomi bor, lekin qator raqamlari va shart tarmoqlari yo'q. Bu ma'lumotni olish uchun `exec` ni `target/classes` dagi haqiqiy bayt kod bilan birga o'qish shart. Shu birlashtirish ishini `jacoco:report` goal bajaradi.

Eski Sonar versiyalarida `sonar.jacoco.reportPaths` parametri bor edi va u binar faylni o'qiy olardi. Bu yondashuv SonarQube 8.x liniyasida olib tashlandi, sababi scanner ning class path ga bog'liq bo'lib qolishi va natijaning beqarorligi. Bugungi 9.9 LTA va 2025 LTA liniyasida yagona qo'llanadigan yo'l XML hisobot.

```bash
# Agent ishlagan bo'lsa binar fayl paydo bo'ladi
ls -l target/jacoco.exec

# Sonar bu faylni o'qimaydi, XML ni alohida chiqaramiz
mvn -q jacoco:report
ls -l target/site/jacoco/jacoco.xml

# XML ichida nechta klass borligini sanaymiz, 0 bo'lsa muammo bor
grep -c '<class name=' target/site/jacoco/jacoco.xml

# Umumiy LINE counter ni ko'ramiz: missed va covered qiymatlari
grep -o 'type="LINE" missed="[0-9]*" covered="[0-9]*"' \
  target/site/jacoco/jacoco.xml | tail -1
```

Agar `covered="0"` chiqsa, muammo Sonar da emas. Demak agent testlar paytida ulanmagan yoki testlar umuman ishlamagan. Sonar ga borishdan oldin shu joyda to'xtab sababini topish kerak.

## 10.4 Gradle da JaCoCo: `jacocoTestReport` va XML chiqishini yoqish

Gradle da `jacoco` plugin `test` task ga agent ni o'zi ulaydi. Lekin `jacocoTestReport` task XML ni odatiy holda chiqarmaydi, faqat HTML beradi. Shuning uchun XML ni ataylab yoqish kerak. Yana bir tuzoq: `jacocoTestReport` `test` dan keyin avtomatik ishlamaydi, uni `finalizedBy` bilan bog'lash kerak.

```groovy
plugins {
    id 'java'
    id 'jacoco'
    id 'org.sonarqube' version '5.1.0.4882'
}

jacoco { toolVersion = '0.8.12' }

test {
    useJUnitPlatform()
    // Test tugagach hisobot avtomatik chiqsin
    finalizedBy jacocoTestReport
}

jacocoTestReport {
    dependsOn test
    reports {
        // Gradle 7 dan boshlab required, undan oldin enabled edi
        xml.required = true
        html.required = true
        csv.required = false
    }
}
```

Sonar property larini alohida blokda beramiz. Yo'l Maven dagidan butunlay boshqacha, shuning uchun uni ko'chirishdan oldin tekshirish kerak.

```groovy
sonar {
    properties {
        property 'sonar.projectKey', 'shop-payment'
        // Gradle dagi odatiy yo'l: build/reports/jacoco/test/
        property 'sonar.coverage.jacoco.xmlReportPaths',
                "${layout.buildDirectory.get()}/reports/jacoco/test/jacocoTestReport.xml"
    }
}
```

Gradle dagi odatiy XML yo'li `build/reports/jacoco/test/jacocoTestReport.xml`. Bu Maven dagi yo'ldan butunlay boshqacha, shuning uchun hujjatdan ko'chirgan sozlamani tekshirmasdan ishlatish eng ko'p uchraydigan xato. Yangi `org.sonarqube` plugin versiyalari `jacocoTestReport` chiqishini o'zi topa oladi, lekin property ni aniq yozish hamma versiyada ishlaydi.

## 10.5 Ko'p modulli Maven loyihasida yig'ma hisobot tayyorlash

Ko'p modulli loyihada har bir modul o'z `jacoco.exec` faylini yozadi. Muammo shunda: `order-service` dagi test `shared-domain` modulidagi klassni ishlatsa, bu qamrov `shared-domain` ning o'z hisobotida ko'rinmaydi. Natijada umumiy foiz haqiqatdan past chiqadi va quality gate behuda yiqiladi.

Yechim `report-aggregate` goal. Buning uchun alohida modul yaratiladi va unga barcha hisoblanadigan modullar dependency sifatida qo'shiladi. Aggregate goal faqat shu modul dependency larini yig'adi, shuning uchun dependency ro'yxati to'liq bo'lishi shart.

```xml
<!-- coverage-report/pom.xml: faqat hisobot yig'ish uchun modul -->
<dependencies>
  <dependency>
    <groupId>com.shop</groupId>
    <artifactId>shared-domain</artifactId>
    <version>${project.version}</version>
  </dependency>
  <dependency>
    <groupId>com.shop</groupId>
    <artifactId>order-service</artifactId>
    <version>${project.version}</version>
  </dependency>
</dependencies>
<build>
  <plugins>
    <plugin>
      <groupId>org.jacoco</groupId>
      <artifactId>jacoco-maven-plugin</artifactId>
      <executions>
        <execution>
          <id>yigma-hisobot</id>
          <phase>verify</phase>
          <goals><goal>report-aggregate</goal></goals>
        </execution>
      </executions>
    </plugin>
  </plugins>
</build>
```

Bu modul `verify` fazasida `coverage-report/target/site/jacoco-aggregate/jacoco.xml` faylini yaratadi. Modul reactor da oxirgi bo'lishi kerak, aks holda yig'ilmagan natijani o'qiydi. Keyin root pom da yo'lni barcha modullar uchun bir xil property qilib beramiz.

```xml
<!-- root pom.xml properties: har bir modul shu yo'lni ko'radi -->
<properties>
  <sonar.coverage.jacoco.xmlReportPaths>
    ${maven.multiModuleProjectDirectory}/coverage-report/target/site/jacoco-aggregate/jacoco.xml
  </sonar.coverage.jacoco.xmlReportPaths>
  <!-- Hisobot moduli o'zida kod yo'q, tahlildan chiqaramiz -->
  <sonar.skip>false</sonar.skip>
</properties>
```

Bu yerda `${maven.multiModuleProjectDirectory}` ishlatilgani muhim. `${project.basedir}` har modulda boshqa qiymat beradi va nisbiy `../` zanjiri modul chuqurligi o'zgarganda buziladi. Agar aggregate ishlatmasangiz, muqobil yo'l barcha modul hisobotlarini vergul bilan sanash, lekin bu ro'yxat yangi modul qo'shilganda eskiradi.

## 10.6 Integratsion test qamrovini alohida yig'ib, keyin birlashtirish

Integratsion testlar Failsafe orqali `integration-test` fazasida ishlaydi. Agar ikki xil test uchun bitta `jacoco.exec` fayliga yozsak, keyingi agent oldingi natijani ustiga yozib ketishi mumkin. Toza yechim: ikki alohida `exec` fayl, keyin `merge` goal bilan birlashtirish va bitta XML chiqarish.

```xml
<executions>
  <execution>
    <id>unit-agent</id>
    <goals><goal>prepare-agent</goal></goals>
    <configuration>
      <destFile>${project.build.directory}/jacoco-ut.exec</destFile>
      <!-- Surefire shu property ni o'qiydi -->
      <propertyName>surefireArgLine</propertyName>
    </configuration>
  </execution>
  <execution>
    <id>it-agent</id>
    <phase>pre-integration-test</phase>
    <goals><goal>prepare-agent-integration</goal></goals>
    <configuration>
      <destFile>${project.build.directory}/jacoco-it.exec</destFile>
      <propertyName>failsafeArgLine</propertyName>
    </configuration>
  </execution>
</executions>
```

Integratsion agent goal i `prepare-agent-integration` deb ataladi, uning standart fazasi ham `pre-integration-test` ([jacoco v0.8.12, AgentITMojo](https://github.com/jacoco/jacoco/blob/v0.8.12/jacoco-maven-plugin/src/org/jacoco/maven/AgentITMojo.java)); `-test` qo'shimchali goal yo'q va build "Could not find goal" bilan yiqiladi.

Birlashtirish va yakuniy hisobot `verify` fazasida bajariladi. `merge` goal `fileSets` ichidagi barcha `exec` fayllarni bitta faylga qo'shadi, keyin `report` shu birlashgan fayldan XML chiqaradi.

```xml
<execution>
  <id>exec-fayllarni-birlashtirish</id>
  <phase>verify</phase>
  <goals><goal>merge</goal></goals>
  <configuration>
    <fileSets>
      <fileSet>
        <directory>${project.build.directory}</directory>
        <includes><include>jacoco-*.exec</include></includes>
      </fileSet>
    </fileSets>
    <destFile>${project.build.directory}/jacoco-merged.exec</destFile>
  </configuration>
</execution>
<execution>
  <id>birlashgan-hisobot</id>
  <phase>verify</phase>
  <goals><goal>report</goal></goals>
  <configuration>
    <dataFile>${project.build.directory}/jacoco-merged.exec</dataFile>
    <outputDirectory>${project.build.directory}/site/jacoco</outputDirectory>
  </configuration>
</execution>
```

Execution lar bir xil fazada ketma-ket pom dagi tartibda ishlaydi, shuning uchun `merge` ni `report` dan yuqoriga yozish shart. Testcontainers bilan ishlaydigan integratsion testlar bu zanjirda hech qanday qo'shimcha sozlama talab qilmaydi, chunki agent ilova JVM ida turadi, konteynerda emas. Testcontainers ni qanday tashkil qilish esa [testlash qo'llanmasidagi](../testing/README.md) Testcontainers mavzusida yoritilgan.

## 10.7 Surefire va Failsafe bilan ishlash tartibi

Eng tez-tez uchraydigan buzilish sababi: kimdir Surefire ga `<argLine>` yozadi va JaCoCo qo'ygan qiymatni almashtiradi. `@{argLine}` sintaksisi late property evaluation ni yoqadi va avvalgi qiymatni saqlaydi. `${argLine}` esa build boshida bo'sh bo'lishi mumkin va xato beradi.

```xml
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-surefire-plugin</artifactId>
  <version>3.2.5</version>
  <configuration>
    <!-- @{...} JaCoCo argumentini saqlaydi, ${...} buzadi -->
    <argLine>@{surefireArgLine} -Xmx1g -Duser.timezone=UTC</argLine>
    <!-- forkCount 0 bo'lsa agent ulanmaydi va coverage 0% chiqadi -->
    <forkCount>1</forkCount>
    <reuseForks>true</reuseForks>
  </configuration>
</plugin>
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-failsafe-plugin</artifactId>
  <version>3.2.5</version>
  <configuration>
    <argLine>@{failsafeArgLine}</argLine>
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

Failsafe ning `verify` goal ini qo'shishni unutmang. Uni yozmasangiz, integratsion test yiqilsa ham build yashil qoladi, Sonar esa buzuq kod uchun coverage qabul qiladi. Bu eng xavfli holat, chunki quality gate o'tadi va xato ishlab chiqarishga ketadi.

## 10.8 Coverage 0% ko'rinishi va uning sabablari

0% deyarli hech qachon "test yo'q" degani emas. Quyida haqiqiy sabablar va ularning belgilari.

| Tuzoq | Belgisi | Yechim |
|---|---|---|
| XML hisobot yaratilmagan | `target/site/jacoco/jacoco.xml` yo'q | `report` goal ni `test` yoki `verify` fazasiga bog'lash |
| Sonar `clean` dan keyin alohida ishlagan | log da `No coverage report can be found` | `mvn clean verify sonar:sonar` bir zanjirda |
| Surefire `argLine` ni almashtirgan | `jacoco.exec` fayli umuman yo'q | `@{argLine}` yoki alohida `propertyName` ishlatish |
| `forkCount` nolga teng | exec bo'sh yoki yo'q | `forkCount` ni 1 yoki undan ko'p qilish |
| Yo'l noto'g'ri yozilgan | log da `0 report(s)` | XML ni `ls` bilan topib, yo'lni aynan ko'chirish |
| Ko'p modulda aggregate yo'q | foiz past, modullar nol | `report-aggregate` moduli qo'shish |
| `sonar.sources` boshqa papkaga qaragan | coverage bor, fayllar mos emas | `sonar.sources` va paket tuzilmasini solishtirish |
| Tekshirilayotgan klass mock qilingan | test yashil, qator qizil | haqiqiy obyekt, faqat bog'liqlik mock |
| Lombok generated kod | model klasslar 0% | `lombok.addLombokGeneratedAnnotation=true` |
| `sonar.exclusions` ga tushgan | fayl Sonar da ko'rinmaydi | `coverage.exclusions` ga ko'chirish |
| CI da test step o'tkazib yuborilgan | `-DskipTests` build log da | tahlildan oldin testni majburiy qilish |
| Yangi kod uchun 0% | umumiy foiz yaxshi, gate qizil | yangi qatorlar uchun test yozish |

Oxirgi uchta qatordan biri amalda tushuntirishni talab qiladi. Tekshirilayotgan servisning o'zini mock qilish test yashil chiqishiga olib keladi, lekin JaCoCo mock ning dinamik klassini hisoblamaydi.

```java
// TUZOQ: tekshirilayotgan klassning o'zi mock, coverage 0% qoladi
@Test
void mockQilinganServisQamrovBermaydi() {
    PaymentService service = mock(PaymentService.class);
    when(service.charge(any())).thenReturn(Receipt.ok("R-1"));
    assertThat(service.charge(new ChargeRequest(100)).status()).isEqualTo("OK");
}

// TO'G'RI: haqiqiy obyekt, faqat tashqi bog'liqlik mock qilinadi
@Test
void haqiqiyServisQamrovBeradi() {
    PaymentGateway gateway = mock(PaymentGateway.class);
    when(gateway.send(any())).thenReturn(GatewayResult.approved("R-1"));
    PaymentService service = new PaymentService(gateway, new InMemoryLedger());
    Receipt receipt = service.charge(new ChargeRequest(100));
    assertThat(receipt.status()).isEqualTo("OK");
}
```

Lombok uchun loyiha root ida `lombok.config` fayli yaratiladi va unga `lombok.addLombokGeneratedAnnotation = true` yoziladi. Bundan keyin JaCoCo generated getter va `equals` metodlarini hisobdan chiqaradi. Bu haqiqiy yechim, chunki generated kodni test qilish hech qanday xatodan himoya qilmaydi.

## 10.9 Sozlashni tekshirish: qaysi faylga qarash, qaysi log qatorini izlash

Tekshirishni har doim pastdan yuqoriga olib boring. Birinchi savol: `jacoco.exec` fayli bormi. Yo'q bo'lsa muammo agent da. Bor bo'lsa ikkinchi savol: `jacoco.xml` bormi va ichida `covered` qiymati noldan kattami. Faqat shundan keyin Sonar log ini o'qishga arziydi.

Sonar scanner log ida JaCoCo sensor nomini izlang. Hisobot topilsa, scanner import qilgan fayl sonini yozadi. Topilmasa, ogohlantirish ichida u qaragan yo'lni aynan ko'rsatadi, shu yo'lni fayl tizimidagi haqiqiy yo'l bilan solishtirish kifoya. Batafsil ro'yxat uchun scanner ni `-X` yoki debug rejimida ishlatish mumkin.

```bash
# 1-qadam: agent ishlaganmi
find . -name 'jacoco*.exec' -size +0 -printf '%p %s bayt\n'

# 2-qadam: XML bormi va bo'sh emasmi
find . -name 'jacoco*.xml' -path '*site*' -printf '%p %s bayt\n'

# 3-qadam: scanner nimani import qilgan
mvn -B sonar:sonar | tee sonar.log
grep -iE 'jacoco|coverage|report\(s\)' sonar.log

# 4-qadam: hech narsa topilmasa, qaysi yo'lga qaraganini ko'ramiz
grep -i 'xmlReportPaths' sonar.log

# 5-qadam: fayllar mos kelmasa, source yo'lini tekshiramiz
grep -iE 'Source|indexing|Base dir' sonar.log | head -20
```

Agar coverage import bo'lgan, lekin Sonar da baribir past ko'rinsa, muammo fayl moslashtirishda. JaCoCo XML da yo'l paket nomi bilan beriladi, Sonar esa `sonar.sources` ostidagi fayllar bilan solishtiradi. Paket nomi papka tuzilmasiga mos bo'lmasa moslik topilmaydi va qamrov yo'qoladi.

## 10.10 CI da tartib: test, hisobot, tahlil ketma-ketligi

CI da tartib qat'iy: avval test va hisobot, keyin tahlil, keyin quality gate natijasini kutish. Tahlilni test bilan bir job ichida qoldirish kerak, chunki boshqa job da `target` papkasi bo'lmaydi. Agar jobs ni ajratish zarur bo'lsa, `target` ni artifact qilib uzatish kerak.

Yana bir shart: `fetch-depth: 0`. Sonar yangi kodni aniqlash uchun git tarixini o'qiydi. Shallow clone da blame ma'lumoti yo'q va yangi kod chegarasi noto'g'ri hisoblanadi.

```yaml
name: ci
on: [push, pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          # Yangi kodni aniqlash uchun butun tarix kerak
          fetch-depth: 0
      - uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: '21'
          cache: maven
      # 1. Test va hisobot: XML shu qadamda tug'iladi
      - name: Test va coverage
        run: mvn -B clean verify
      # 2. Tahlil: clean YO'Q, aks holda hisobot o'chadi
      - name: Sonar tahlili
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
        run: mvn -B sonar:sonar -Dsonar.host.url=${{ secrets.SONAR_HOST_URL }}
```

`clean` ni faqat birinchi qadamda ishlatish eng muhim qoida. Ikki buyruqni bitta qatorga qo'shib yozish ham mumkin, lekin alohida step da xatoning qaysi bosqichda bo'lganini log dan darhol ko'rish osonroq.

```bash
# TO'G'RI tartib
mvn -B clean verify            # test, exec, XML
mvn -B sonar:sonar             # tahlil, XML ni o'qiydi

# NOTO'G'RI: clean hisobotni tahlildan oldin o'chiradi
mvn -B clean sonar:sonar

# NOTO'G'RI: testlar o'tkazib yuborilgan, coverage 0%
mvn -B clean verify -DskipTests
mvn -B sonar:sonar

# Bir buyruqda ham ishlaydi
mvn -B clean verify sonar:sonar -Dsonar.token=$SONAR_TOKEN
```

## 10.11 Oddiy yondashuv va arxitektor yondashuvi

| Savol | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Hisobot formati | HTML yetadi deb o'ylaydi | XML ni majburiy formatga qo'yadi, HTML qo'shimcha |
| `report` fazasi | odatiy holatga ishonadi | `test` yoki `verify` ga aniq bog'laydi |
| Surefire `argLine` | `${argLine}` yozadi va buzadi | alohida `propertyName` va `@{...}` ishlatadi |
| Ko'p modul | har modul foizini alohida ko'radi | `report-aggregate` moduli bilan yig'adi |
| Integratsion test | bitta `exec` ga yozadi | ikki `exec` va `merge` goal |
| Yo'l ko'rsatish | hujjatdan yo'lni ko'chiradi | fayl tizimidan topib tekshiradi |
| CI tartibi | `clean sonar:sonar` ishlatadi | test va tahlilni ikki qadamga ajratadi |
| Git tarixi | shallow clone bilan qoladi | `fetch-depth: 0` qo'yadi |
| Generated kod | 0% ni ko'rib test yozadi | `lombok.config` va exclusion bilan hisobdan chiqaradi |
| 0% debug | Sonar sozlamasini o'zgartiradi | `exec`, `xml`, log zanjirini pastdan yuqoriga tekshiradi |
| Failsafe `verify` | goal ni yozmay qoldiradi | `verify` goal ni qo'shib build ni qizil qiladi |
| Maqsad | foizni ko'tarish | yangi kod uchun ishonchli o'lchov qurish |

Oxirgi qator eng muhim. To'g'ri ulangan JaCoCo faqat raqamni ko'rsatadi, u sifatni o'lchamaydi. 100% qamrov assertion siz testlar bilan ham olinadi, bunda har qator ishga tushadi, lekin hech narsa tekshirilmaydi. Shuning uchun ulanishni tugatgach, keyingi ish foizni ko'tarish emas, balki mavjud testlarning assertion sifatini ko'rib chiqish.

Shuni ham aniq ayting: quality gate shartlari har loyihada boshqacha sozlanadi. Bir joyda yangi kod uchun 80% talab qilinadi, boshqa joyda 60%. "Har doim o'tadigan" universal sozlama yo'q, bor narsa aniq shartni bilish va unga mos ishlash.

## 10.12 Amalda qo'llash

- [ ] Loyihada `jacoco.exec` va `jacoco.xml` fayllari haqiqatda yaratilayotganini `find` bilan tekshiring, natijani yozib qo'ying.
- [ ] `report` goal ni `test` yoki `verify` fazasiga aniq bog'lang va XML formatini majburiy qiling.
- [ ] Surefire va Failsafe konfiguratsiyasidagi barcha `argLine` yozuvlarini `@{...}` sintaksisiga o'tkazing va `forkCount` ni nol emasligini tasdiqlang.
- [ ] `sonar.coverage.jacoco.xmlReportPaths` qiymatini fayl tizimidagi haqiqiy yo'l bilan solishtirib tekshiring, hujjatdan ko'chirgan qiymatga ishonmang.
- [ ] Ko'p modulli loyihada `report-aggregate` moduli yaratib, uni reactor da oxirgi qilib qo'ying va root pom da yo'lni bitta property ga chiqaring.
- [ ] Integratsion testlar uchun alohida `exec` fayl va `merge` goal sozlang, Failsafe ning `verify` goal ini qo'shing.
- [ ] CI da test va tahlilni ikki alohida qadamga ajratib, `clean` ni faqat birinchi qadamda qoldiring va `fetch-depth: 0` qo'ying.
- [ ] Lombok ishlatilsa `lombok.config` ga `addLombokGeneratedAnnotation` qo'shing, konfiguratsiya klasslarini `coverage.exclusions` ga kiriting.

---

[&larr; 9. Coverage qanday o'lchanadi: JaCoCo mexanikasi](09-coverage-qanday-olchanadi-jacoco-mexanikasi.md) · [Mundarija](README.md) · [11. Qamralmay qoladigan kod va unga test yozish &rarr;](11-qamralmay-qoladigan-kod-va-unga-test-yozish.md)
