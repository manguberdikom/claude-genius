<!-- doc: sonarqube | chapter: 43 | part: X. Amaliy ma'lumotnoma -->

[Barcha hujjatlar](../../README.md) / [SonarQube](README.md)

# 43. Tezkor ma'lumotnoma: parametrlar, buyruqlar, glossariy (Quick Reference and Glossary)

<details>
<summary>Bu bobdagi 15 bo'lim</summary>

- [43.1 Eng ko'p ishlatiladigan `sonar.*` parametrlari](#431-eng-kop-ishlatiladigan-sonar-parametrlari)
- [43.2 Qamrov va hisobot yo'llari uchun parametrlar](#432-qamrov-va-hisobot-yollari-uchun-parametrlar)
- [43.3 Exclusion parametrlari va ularning farqi](#433-exclusion-parametrlari-va-ularning-farqi)
- [43.4 Pull request va branch parametrlari](#434-pull-request-va-branch-parametrlari)
- [43.5 Maven buyruqlari to'plami](#435-maven-buyruqlari-toplami)
- [43.6 Gradle buyruqlari to'plami](#436-gradle-buyruqlari-toplami)
- [43.7 Mustaqil scanner va Docker orqali ishga tushirish](#437-mustaqil-scanner-va-docker-orqali-ishga-tushirish)
- [43.8 Foydali `curl` so'rovlari](#438-foydali-curl-sorovlari)
- [43.9 Metrika kalitlari](#439-metrika-kalitlari)
- [43.10 Quality gate uchun boshlang'ich shartlar namunasi](#4310-quality-gate-uchun-boshlangich-shartlar-namunasi)
- [43.11 Yangi loyihani boshlash uchun qadamlar](#4311-yangi-loyihani-boshlash-uchun-qadamlar)
- [43.12 Oddiy yondashuv va arxitektor yondashuvi](#4312-oddiy-yondashuv-va-arxitektor-yondashuvi)
- [43.13 Tuzoq va yechim](#4313-tuzoq-va-yechim)
- [43.14 Glossariy](#4314-glossariy)
- [43.15 Amalda qo'llash](#4315-amalda-qollash)

</details>



Bu bob tushuntirish uchun emas, qarash uchun yozilgan. Unda eng ko'p ishlatiladigan parametrlar, buyruqlar, metrika kalitlari va atamalar bir joyda to'plangan. Har bir jadvalda faqat amalda tasdiqlangan nomlar bor, shubhali nom esa umuman kiritilmagan. Shuning uchun bu ro'yxatni to'liq deb hisoblamang va aniq versiyangizdagi to'liq ro'yxatni serverdagi `/web_api` sahifasidan oling.

## 43.1 Eng ko'p ishlatiladigan `sonar.*` parametrlari

| Parametr | Ma'nosi | Namuna qiymati |
|---|---|---|
| `sonar.projectKey` | Loyihaning server ichidagi yagona kaliti | `com.example:orders-service` |
| `sonar.projectName` | Interfeysda ko'rinadigan nom | `Orders Service` |
| `sonar.projectVersion` | Tahlilga yoziladigan versiya belgisi | `1.4.0` |
| `sonar.sources` | Asosiy manba kataloglari | `src/main/java` |
| `sonar.tests` | Test manbalari katalogi | `src/test/java` |
| `sonar.sourceEncoding` | Fayllarning kodlashi | `UTF-8` |
| `sonar.projectBaseDir` | Tahlil boshlanadigan ildiz katalog | `.` |
| `sonar.host.url` | SonarQube server manzili | `https://sonar.example.com` |
| `sonar.token` | Autentifikatsiya tokeni | `${SONAR_TOKEN}` |
| `sonar.java.binaries` | Kompilyatsiya qilingan asosiy klasslar | `target/classes` |
| `sonar.java.test.binaries` | Kompilyatsiya qilingan test klasslari | `target/test-classes` |
| `sonar.java.libraries` | Bog'liqlik jar fayllari | `target/dependency/*.jar` |
| `sonar.java.source` | Java til darajasi | `17` |
| `sonar.java.jdkHome` | Tahlil uchun JDK yo'li | `/usr/lib/jvm/jdk-21` |
| `sonar.qualitygate.wait` | Scanner gate natijasini kutadi | `true` |
| `sonar.qualitygate.timeout` | Kutish chegarasi, sekund | `300` |
| `sonar.scm.provider` | SCM turi, blame uchun | `git` |
| `sonar.scm.disabled` | SCM o'qishini o'chirish | `false` |
| `sonar.verbose` | Batafsil log | `true` |

Token uchun eski `sonar.login` va `sonar.password` juftligi hali ishlashi mumkin, lekin yangi liniyalarda `sonar.token` tavsiya qilinadi. To'liq ro'yxatni serverdagi `/web_api` sahifasidan oling.

## 43.2 Qamrov va hisobot yo'llari uchun parametrlar

| Parametr | Ma'nosi | Namuna qiymati |
|---|---|---|
| `sonar.coverage.jacoco.xmlReportPaths` | JaCoCo XML hisobot yo'li yoki yo'llari | `target/site/jacoco/jacoco.xml` |
| `sonar.junit.reportPaths` | Test natijalari XML katalogi | `target/surefire-reports` |
| `sonar.coverage.exclusions` | Qamrov talabidan chiqariladigan fayllar | `**/config/**,**/dto/**` |

Multi module loyihada har bir modulning XML hisobotini vergul bilan sanash yoki birlashtirilgan hisobot yaratish kerak. Sonar faqat XML ni o'qiydi, HTML va `exec` fayl unga yaramaydi.

```properties
# Loyiha identifikatori: server ichida yagona bo'lishi shart
sonar.projectKey=com.example:orders-service
sonar.projectName=Orders Service
# Manba va test kataloglari
sonar.sources=src/main/java
sonar.tests=src/test/java
# Java tahlili uchun kompilyatsiya natijasi majburiy
sonar.java.binaries=target/classes
sonar.java.test.binaries=target/test-classes
sonar.java.source=17
# Kodlash: aks holda o'zbek matni buzilib ko'rinadi
sonar.sourceEncoding=UTF-8
# Qamrov: faqat XML hisobot qabul qilinadi
sonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml
sonar.junit.reportPaths=target/surefire-reports
# Generatsiya qilingan kod tahlildan chiqariladi
sonar.exclusions=**/generated/**,**/*MapperImpl.java
```

## 43.3 Exclusion parametrlari va ularning farqi

| Parametr | Nimaga ta'sir qiladi | Qachon ishlatiladi |
|---|---|---|
| `sonar.exclusions` | Fayl umuman tahlil qilinmaydi, metrikaga kirmaydi | Generatsiya qilingan va migratsiya kodi |
| `sonar.inclusions` | Faqat sanalgan fayllar tahlil qilinadi | Katta repozitoriyning bir qismini olish |
| `sonar.test.exclusions` | Test fayllari tahlildan chiqariladi | Katta avtogeneratsiya test to'plami |
| `sonar.test.inclusions` | Faqat sanalgan test fayllari olinadi | Test papkasining bir qismini tahlil qilish |
| `sonar.coverage.exclusions` | Fayl tahlil qilinadi, lekin qamrov talab qilinmaydi | DTO, konfiguratsiya, `main` klassi |
| `sonar.cpd.exclusions` | Fayl dublikat tekshiruvidan chiqariladi | Takrorlanishi tabiiy bo'lgan sxema klasslari |
| `sonar.issue.ignore.multicriteria` | Tanlangan qoida tanlangan faylda o'chiriladi | Bitta qoida bitta qatlamga mos kelmaganda |

Eng ko'p uchraydigan xato `sonar.exclusions` ni qamrov uchun ishlatish. Agar maqsad faqat qamrov talabini yumshatish bo'lsa, `sonar.coverage.exclusions` ishlatiladi.

```java
// JaCoCo 0.8.x nomi "Generated" so'zini o'z ichiga olgan annotatsiyani
// ko'rsa, o'sha klass yoki metodni qamrov hisobidan chiqarib tashlaydi.
// Shart: annotatsiya retention CLASS yoki RUNTIME bo'lishi kerak.
@Retention(RetentionPolicy.CLASS)
@Target({ElementType.TYPE, ElementType.METHOD})
public @interface GeneratedByBuild {
}

// Shu annotatsiya qo'yilgan klass qamrov raqamini pasaytirmaydi,
// lekin Sonar qoidalari unga baribir qo'llanadi.
@GeneratedByBuild
public final class OrderRowMapperImpl {
    // ombor qatorini obyektga o'girish uchun generatsiya qilingan kod
}
```

## 43.4 Pull request va branch parametrlari

| Parametr | Ma'nosi | Namuna qiymati |
|---|---|---|
| `sonar.branch.name` | Tahlil qilinayotgan branch nomi | `feature/payment-retry` |
| `sonar.pullrequest.key` | Pull request raqami yoki identifikatori | `1428` |
| `sonar.pullrequest.branch` | Manba branch nomi | `feature/payment-retry` |
| `sonar.pullrequest.base` | Nishon branch nomi | `main` |
| `sonar.newCode.referenceBranch` | New code uchun taqqoslash branchi | `main` |

Ko'p CI integratsiyalarida bu parametrlar avtomatik aniqlanadi va ularni qo'lda berish shart emas. Qo'lda berish kerak bo'lgan holat: o'z skriptingiz yoki standart bo'lmagan CI. `sonar.branch.name` va pull request parametrlarini bir vaqtda berish xato hisoblanadi.

```yaml
# CI da tahlil: avval test va qamrov, keyin Sonar, keyin gate kutish
analyze:
  stage: verify
  variables:
    # shallow clone blame ma'lumotini buzadi, shuning uchun to'liq tarix
    GIT_DEPTH: "0"
  script:
    - mvn -B clean verify
    - >
      mvn -B sonar:sonar
      -Dsonar.host.url=$SONAR_HOST_URL
      -Dsonar.token=$SONAR_TOKEN
      -Dsonar.qualitygate.wait=true
      -Dsonar.qualitygate.timeout=600
  # gate yiqilsa quvur ham yiqiladi
  allow_failure: false
```

## 43.5 Maven buyruqlari to'plami

```bash
# To'liq zanjir: test, qamrov hisoboti, keyin tahlil
mvn -B clean verify sonar:sonar

# Plugin versiyasini qat'iy ko'rsatib chaqirish
mvn -B org.sonarsource.scanner.maven:sonar-maven-plugin:sonar

# Parametrlarni buyruq satridan berish
mvn -B sonar:sonar -Dsonar.host.url=https://sonar.example.com \
  -Dsonar.token="$SONAR_TOKEN" -Dsonar.projectKey=com.example:orders

# Gate natijasini kutish: CI uchun asosiy shart
mvn -B sonar:sonar -Dsonar.qualitygate.wait=true

# Faqat qamrov hisobotini yangilash
mvn -B test jacoco:report

# Tahlilni muhokama qilish uchun batafsil log
mvn -B sonar:sonar -Dsonar.verbose=true

# Testni o'tkazib yuborish: qamrov nolga tushadi, ehtiyot bo'ling
mvn -B clean install -DskipTests sonar:sonar
```

```xml
<build>
  <plugins>
    <plugin>
      <groupId>org.jacoco</groupId>
      <artifactId>jacoco-maven-plugin</artifactId>
      <version>0.8.12</version>
      <executions>
        <!-- agent testdan oldin ulanadi -->
        <execution>
          <goals><goal>prepare-agent</goal></goals>
        </execution>
        <!-- XML hisobot verify fazasida yoziladi -->
        <execution>
          <id>jacoco-report</id>
          <phase>verify</phase>
          <goals><goal>report</goal></goals>
        </execution>
      </executions>
    </plugin>
    <plugin>
      <groupId>org.sonarsource.scanner.maven</groupId>
      <artifactId>sonar-maven-plugin</artifactId>
      <!-- aniq versiyani Maven Central dan tanlang -->
      <version>${sonar-maven-plugin.version}</version>
    </plugin>
  </plugins>
</build>
```

## 43.6 Gradle buyruqlari to'plami

```bash
# Plugin 4.x va yuqorisida vazifa nomi "sonar"
./gradlew test jacocoTestReport sonar

# Eski plugin liniyasida vazifa nomi "sonarqube"
./gradlew test jacocoTestReport sonarqube

# Parametrlarni buyruq satridan berish
./gradlew sonar -Dsonar.host.url=https://sonar.example.com \
  -Dsonar.token="$SONAR_TOKEN"

# Gate natijasini kutish
./gradlew sonar -Dsonar.qualitygate.wait=true

# Ko'p modulli qurilmada bitta modulni tahlil qilish
./gradlew :orders-service:test :orders-service:sonar

# Nima bajarilishini oldin ko'rish
./gradlew sonar --dry-run
```

Gradle da qamrov hisoboti XML ko'rinishida yoqilgan bo'lishi kerak. `jacocoTestReport` vazifasining `reports` blokida `xml.required` ni `true` qilish shart.

## 43.7 Mustaqil scanner va Docker orqali ishga tushirish

```bash
# Mustaqil scanner: sonar-project.properties fayliga tayanadi
sonar-scanner -Dsonar.host.url="$SONAR_HOST_URL" -Dsonar.token="$SONAR_TOKEN"

# Scanner ni Docker ichida yuritish: joriy katalog ulanadi
docker run --rm \
  -e SONAR_HOST_URL="$SONAR_HOST_URL" \
  -e SONAR_TOKEN="$SONAR_TOKEN" \
  -v "$(pwd):/usr/src" \
  sonarsource/sonar-scanner-cli

# Mahalliy tajriba uchun server ko'tarish
docker run -d --name sonarqube -p 9000:9000 sonarqube:community

# Server tayyor bo'lganini tekshirish
curl -s http://localhost:9000/api/system/status
```

Mahalliy serverda dastlabki kirish `admin` va `admin` juftligi bilan bo'ladi va parolni darhol almashtirish talab qilinadi. Docker da ko'tarilgan server ma'lumotlarini saqlash uchun `data`, `extensions` va `logs` kataloglarini volume qilish kerak.

## 43.8 Foydali `curl` so'rovlari

```bash
# Token bilan autentifikatsiya: token foydalanuvchi nomi o'rnida
AUTH="-u $SONAR_TOKEN:"

# Server versiyasi
curl -s "$SONAR_HOST_URL/api/server/version"

# Token haqiqiyligini tekshirish
curl -s $AUTH "$SONAR_HOST_URL/api/authentication/validate"

# Quality gate natijasi: CI uchun eng kerakli so'rov
curl -s $AUTH "$SONAR_HOST_URL/api/qualitygates/project_status?projectKey=com.example:orders"

# Bir nechta metrikani birdan olish
curl -s $AUTH "$SONAR_HOST_URL/api/measures/component?component=com.example:orders&metricKeys=coverage,ncloc,bugs"

# Ochiq issue larni qidirish
curl -s $AUTH "$SONAR_HOST_URL/api/issues/search?componentKeys=com.example:orders&severities=BLOCKER,CRITICAL"

# Security hotspot ro'yxati
curl -s $AUTH "$SONAR_HOST_URL/api/hotspots/search?projectKey=com.example:orders"

# Tahlil vazifasi holati
curl -s $AUTH "$SONAR_HOST_URL/api/ce/activity?component=com.example:orders"
```

Yangi liniyalarda `Authorization: Bearer <token>` sarlavhasi ham qabul qilinadi. Qaysi endpoint qanday parametr olishini aniq bilish uchun serverdagi `/web_api` sahifasini oching, chunki u aynan sizning versiyangiz uchun generatsiya qilinadi.

## 43.9 Metrika kalitlari

| Kalit | Ma'nosi |
|---|---|
| `ncloc` | Izoh va bo'sh qatorsiz kod qatorlari soni |
| `lines` | Fayldagi barcha qatorlar soni |
| `complexity` | Siklomatik murakkablik yig'indisi |
| `cognitive_complexity` | Kognitiv murakkablik yig'indisi |
| `coverage` | Umumiy qamrov, qator va shart birgalikda |
| `line_coverage` | Qator qamrovi, foiz |
| `branch_coverage` | Shart qamrovi, foiz |
| `lines_to_cover` | Qamrashga tegishli qatorlar soni |
| `uncovered_lines` | Qamrab olinmagan qatorlar soni |
| `conditions_to_cover` | Qamrashga tegishli shartlar soni |
| `uncovered_conditions` | Qamrab olinmagan shartlar soni |
| `duplicated_lines` | Takrorlangan qatorlar soni |
| `duplicated_lines_density` | Takrorlanish ulushi, foiz |
| `duplicated_blocks` | Takrorlangan bloklar soni |
| `violations` | Barcha issue soni |
| `bugs` | Reliability toifasidagi issue soni |
| `vulnerabilities` | Security toifasidagi issue soni |
| `code_smells` | Maintainability toifasidagi issue soni |
| `security_hotspots` | Qo'lda ko'rib chiqishga muhtoj joylar soni |
| `sqale_index` | Technical debt, daqiqa hisobida |
| `sqale_debt_ratio` | Debt ning taxminiy ishlab chiqish narxiga nisbati |
| `sqale_rating` | Maintainability bahosi, A dan E gacha |
| `reliability_rating` | Reliability bahosi |
| `security_rating` | Security bahosi |
| `security_review_rating` | Hotspot ko'rib chiqilganlik bahosi |
| `alert_status` | Quality gate natijasi: `OK` yoki `ERROR` |
| `tests` | Bajarilgan test soni |
| `test_failures` | Muvaffaqiyatsiz test soni |

Hajm metrikalari qatorida `files`, `classes`, `functions` va `statements` kalitlari ham bor. Test tomonida `test_errors`, `skipped_tests` va `test_execution_time` kalitlari ishlatiladi.

New code uchun ko'p metrikaning `new_` prefiksli juftligi bor: `new_coverage`, `new_lines`, `new_bugs`, `new_vulnerabilities`, `new_code_smells`, `new_duplicated_lines_density`, `new_lines_to_cover`, `new_technical_debt`. To'liq ro'yxatni serverdagi `/web_api` sahifasidan, `api/metrics/search` bo'limidan oling.

```sql
-- Metrikani SonarQube ma'lumotlar bazasidan to'g'ridan to'g'ri o'qish
-- qo'llab quvvatlanmaydi: jadval sxemasi versiyada ogohlantirishsiz o'zgaradi.
-- Shuning uchun hisobotni Web API orqali oling va o'z bazangizga yozing.
CREATE TABLE quality_snapshot (
    project_key   VARCHAR(255) NOT NULL,
    taken_at      TIMESTAMP    NOT NULL,
    coverage      NUMERIC(5,2),
    new_coverage  NUMERIC(5,2),
    gate_status   VARCHAR(16)  NOT NULL,
    CONSTRAINT pk_quality_snapshot PRIMARY KEY (project_key, taken_at)
);

-- Oxirgi o'n kunda gate necha marta yiqilgani
SELECT project_key, COUNT(*) AS failures
FROM quality_snapshot
WHERE gate_status = 'ERROR'
  AND taken_at >= now() - INTERVAL '10 days'
GROUP BY project_key
ORDER BY failures DESC;
```

## 43.10 Quality gate uchun boshlang'ich shartlar namunasi

| Shart | Taklif qilinadigan chegara | Izoh |
|---|---|---|
| `new_coverage` | 80 foizdan kam bo'lsa yiqiladi | Yangi kodga nisbatan, eski kodga emas |
| `new_duplicated_lines_density` | 3 foizdan oshsa yiqiladi | Nusxa ko'chirishni darhol ushlaydi |
| `new_blocker_violations` yoki yangi issue soni | Noldan oshsa yiqiladi | Versiyaga qarab nom va shakl farq qiladi |
| `new_security_hotspots_reviewed` | 100 foizdan kam bo'lsa yiqiladi | Hotspot ko'rib chiqilishi majburiy bo'ladi |
| `new_reliability_rating` | A dan yomon bo'lsa yiqiladi | Yangi bug ga nol tolerantlik |
| `new_security_rating` | A dan yomon bo'lsa yiqiladi | Yangi vulnerability ga nol tolerantlik |
| `new_maintainability_rating` | A dan yomon bo'lsa yiqiladi | Yangi code smell ni cheklaydi |

Standart `Sonar way` gate shu ruhda tuzilgan va u faqat new code ni tekshiradi. SonarQube 10 liniyasidan boshlab clean code taksonomiyasi joriy etilgani uchun ayrim shart nomlari o'zgargan, shuning uchun aniq nomni o'z serveringizdagi gate tahrirlash sahifasida tasdiqlang.

## 43.11 Yangi loyihani boshlash uchun qadamlar

1. Serverda loyiha yaratish va `projectKey` ni belgilash.
2. CI uchun alohida token generatsiya qilish va uni secret sifatida saqlash.
3. JaCoCo plugin ni qo'shish va XML hisobotni yoqish.
4. `sonar.coverage.jacoco.xmlReportPaths` ni hisobot yo'liga moslash.
5. Birinchi tahlilni mahalliy mashinada yuritib natijani ko'rish.
6. Generatsiya qilingan kod va migratsiyalarni `sonar.exclusions` ga kiritish.
7. DTO va konfiguratsiya klasslarini `sonar.coverage.exclusions` ga kiritish.
8. New code definition ni tanlash: referens branch yoki oldingi versiya.
9. Quality gate ni new code ga moslab sozlash.
10. CI da `sonar.qualitygate.wait=true` ni yoqish, quvurni gate ga bog'lash va pull request tahlilini yoqish.

## 43.12 Oddiy yondashuv va arxitektor yondashuvi

| Mavzu | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Gate sozlash | Umumiy qamrovga 80 foiz qo'yiladi | Faqat new code ga chegara qo'yiladi |
| Exclusion | `sonar.exclusions` ga hammasi tashlanadi | Qamrov, dublikat va tahlil exclusion lari ajratiladi |
| Token | Shaxsiy token CI ga yoziladi | CI uchun alohida texnik hisob tokeni ishlatiladi |
| Qamrov hisoboti | `exec` fayl qoldiriladi va qamrov nol chiqadi | XML hisobot generatsiyasi qurilish qismiga kiritiladi |
| CI xatti harakati | Tahlil yuboriladi va natija kutilmaydi | `qualitygate.wait` yoqiladi, quvur gate ga bog'lanadi |
| Issue bilan ishlash | Qoidalar o'chiriladi | Qoida profilda muhokama qilinib moslanadi |
| Dublikat | Nusxa ko'chirib qo'yiladi va exclusion yoziladi | Umumiy abstraksiya ajratiladi |
| Hotspot | Hammasi `safe` deb yopiladi | Har biri sabab bilan hujjatlashtiriladi |
| New code definition | Standart holda qoldiriladi | Relizlash modeliga mos tanlanadi |
| Metrika kuzatuvi | Faqat gate rangiga qaraladi | `sqale_index` va `new_coverage` trendi kuzatiladi |
| Multi module | Har bir modul alohida loyiha qilinadi | Bitta loyiha ichida modul tuzilmasi saqlanadi |

## 43.13 Tuzoq va yechim

| Tuzoq | Nima bo'ladi | Yechim |
|---|---|---|
| Qamrov nol ko'rsatadi | XML hisobot yo'li topilmadi | `xmlReportPaths` ni tekshirish va `jacoco:report` ni verify ga bog'lash |
| Yangi kod butun loyiha deb ko'rinadi | Shallow clone, blame yo'q | CI da to'liq git tarixini olish |
| Java qoidalari ishlamaydi | `sonar.java.binaries` berilmagan | Tahlildan oldin kompilyatsiya qilish |
| Pull request tahlili xato beradi | Branch va PR parametrlari bir vaqtda berilgan | Faqat bittasini qoldirish |
| Gate yashil, lekin xato ko'p | Shart faqat new code ga qo'yilgan | Eski debt uchun alohida reja tuzish |
| Dublikat keskin oshdi | Generatsiya qilingan kod tahlilga kirdi | `sonar.cpd.exclusions` yoki `sonar.exclusions` qo'shish |
| Tahlil juda sekin | Katta binar va resurs fayllar skanerlanadi | `sonar.exclusions` bilan ularni chiqarish |
| Token ishlamay qoldi | Token muddati tugagan yoki bekor qilingan | Yangi token olish va secret ni yangilash |
| Quvur gate ni kutmaydi | `qualitygate.wait` yoqilmagan | Parametrni yoqish va timeout berish |

## 43.14 Glossariy

- **issue**: Sonar topgan muammo yozuvi. Har bir issue bitta qoidaga va bitta joyga bog'langan.
- **bug**: Reliability toifasidagi issue. Kodning kutilmagan natija berishi ehtimoli bor degan ma'noni beradi.
- **vulnerability**: Security toifasidagi issue. Zaiflik mavjud deb baholangan joy.
- **code smell**: Maintainability toifasidagi issue. Ishlaydi, lekin keyinchalik qimmatga tushadi.
- **security hotspot**: Avtomatik hukm chiqarilmaydigan, qo'lda ko'rib chiqishni talab qiladigan joy. Natijasi `safe` yoki tasdiqlangan zaiflik bo'ladi.
- **rule**: Bitta tekshiruv. Har bir qoida kalitga ega, masalan `java:S2259`.
- **quality profile**: Tilga tegishli qoidalar to'plami. Loyihaga shu to'plam qo'llanadi.
- **quality gate**: Tahlil natijasi uchun shartlar to'plami. Natija `OK` yoki `ERROR` bo'ladi.
- **new code**: Taqqoslash nuqtasidan keyin o'zgargan kod. Gate shartlari asosan shunga qo'llanadi.
- **new code definition**: New code ni qanday aniqlash qoidasi. Referens branch, versiya yoki kun soni bo'lishi mumkin.
- **clean as you code**: Eski debt ni bir yo'la tozalamasdan, faqat yangi kodni toza saqlash yondashuvi.
- **technical debt**: Issue larni tuzatishga ketadigan taxminiy vaqt. `sqale_index` metrikasi orqali o'lchanadi.
- **SQALE**: Debt ni vaqt sifatida hisoblash va A dan E gacha baho berish modeli.
- **severity**: Issue ning jiddiyligi. Profilga qarab o'zgaradi, shuning uchun uni mutlaq haqiqat deb olmaslik kerak.
- **taint analysis**: Ishonchsiz manbadan kelgan ma'lumot xavfli joyga qanday yetib borishini kuzatuvchi tahlil. SQL injection va shunga o'xshash zaifliklarni topishda ishlatiladi.
- **cyclomatic complexity**: Koddagi mustaqil yo'llar soni.
- **cognitive complexity**: Kodni o'qib tushunish qiyinligini o'lchaydigan metrika. Ichma ich joylashish uni keskin oshiradi.
- **coverage**: Testlar qamrab olgan kod ulushi. Sonar uni qamrov vositasining hisobotidan oladi.
- **condition coverage**: Shart ifodalarining har bir natijasi sinalganlik ulushi.
- **scanner**: Kodni o'qib ma'lumot yuboradigan mijoz. Maven plugin, Gradle plugin yoki mustaqil CLI shaklida bo'ladi.
- **compute engine**: Serverda yuborilgan ma'lumotni qayta ishlab metrika va gate natijasini hisoblaydigan qism.
- **false positive**: Noto'g'ri topilgan issue. Shu holatda issue sabab bilan yopiladi.
- **accepted yoki won't fix**: Issue haqiqiy, lekin tuzatilmasligi qabul qilingan holat. Nom versiyaga qarab farq qiladi.
- **exclusion**: Fayl yoki qoidani tahlilning bir qismidan chiqarib tashlash sozlamasi.
- **SCM blame**: Har bir qatorni kim va qachon o'zgartirganini ko'rsatuvchi git ma'lumoti. New code aniqlash shunga tayanadi.
- **ncloc**: Izohsiz va bo'sh qatorsiz kod qatorlari soni. Loyiha hajmini o'lchashda asosiy raqam.
- **LTA**: Uzoq muddat qo'llab quvvatlanadigan reliz liniyasi. Ishlab chiqarish serveri uchun shu liniya tanlanadi.

## 43.15 Amalda qo'llash

- [ ] Loyihangizdagi barcha `sonar.*` sozlamalarini bitta `sonar-project.properties` yoki `pom.xml` bo'limiga yig'ib, tarqoq joylarni o'chiring.
- [ ] `sonar.exclusions` ro'yxatini ko'rib chiqing va faqat qamrov uchun kerak bo'lgan yozuvlarni `sonar.coverage.exclusions` ga ko'chiring.
- [ ] CI da `sonar.qualitygate.wait=true` ni yoqib, quvurni gate natijasiga bog'langanini bitta ataylab buzilgan commit bilan tekshiring.
- [ ] `api/qualitygates/project_status` so'rovini CI log ida chop etadigan qadam qo'shib, yiqilish sababi darhol ko'rinadigan qiling.
- [ ] Serveringizdagi `/web_api` sahifasini ochib, shu bobdagi parametr va metrika nomlarini o'z versiyangizda tasdiqlang.
- [ ] New code definition ni relizlash modelingizga moslab tanlang va tanlov sababini repozitoriyda qisqa yozib qoldiring.
- [ ] Glossariy atamalarini jamoa bilan bir marta ko'rib chiqing, chunki `bug`, `hotspot` va `debt` so'zlarini har kim boshqacha tushunadi.
- [ ] Oyda bir marta `ncloc`, `new_coverage` va `sqale_index` qiymatlarini yozib boradigan oddiy jadval yuritib, trendni kuzating.

---

[&larr; 42. Diagnostika: tahlil ishlamaganda nima qilish](42-diagnostika-tahlil-ishlamaganda-nima-qilish.md) · [Mundarija](README.md)
