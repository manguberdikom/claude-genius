<!-- doc: sonarqube | chapter: 39 | part: IX. Kengaytirish va integratsiya -->

[SonarQube](../../README.md) / [SonarQube](README.md)

# 39. Bog'liqlik zaifliklari va litsenziya tekshiruvi (Dependency Risk and Licences)

<details>
<summary>Bu bobdagi 13 bo'lim</summary>

- [39.1 Sonar kodingizni tekshiradi, bog'liqliklaringizni esa to'liq tekshirmaydi](#391-sonar-kodingizni-tekshiradi-bogliqliklaringizni-esa-toliq-tekshirmaydi)
- [39.2 Bog'liqlik zaifligi nima va u qanday aniqlanadi (ma'lum zaifliklar bazasi)](#392-bogliqlik-zaifligi-nima-va-u-qanday-aniqlanadi-malum-zaifliklar-bazasi)
- [39.3 Tranzitiv bog'liqlik: siz qo'shmagan kutubxona ham sizniki](#393-tranzitiv-bogliqlik-siz-qoshmagan-kutubxona-ham-sizniki)
- [39.4 Maven va Gradle da bog'liqlik daraxtini ko'rish](#394-maven-va-gradle-da-bogliqlik-daraxtini-korish)
- [39.5 Zaiflikni tekshiruvchi vositalar: OWASP Dependency-Check, Trivy, Grype, Dependabot](#395-zaiflikni-tekshiruvchi-vositalar-owasp-dependency-check-trivy-grype-dependabot)
- [39.6 Natijani CI ga ulash va qaysi daraja build ni bloklashi](#396-natijani-ci-ga-ulash-va-qaysi-daraja-build-ni-bloklashi)
- [39.7 False positive va zaiflikni asosli ravishda e'tiborsiz qoldirish](#397-false-positive-va-zaiflikni-asosli-ravishda-etiborsiz-qoldirish)
- [39.8 Yangilash siyosati: qachon darhol, qachon rejali](#398-yangilash-siyosati-qachon-darhol-qachon-rejali)
- [39.9 SBOM nima va u nimaga kerak](#399-sbom-nima-va-u-nimaga-kerak)
- [39.10 Litsenziya tekshiruvi: qaysi litsenziya xavfli bo'lishi mumkin](#3910-litsenziya-tekshiruvi-qaysi-litsenziya-xavfli-bolishi-mumkin)
- [39.11 Bog'liqliklarni kamaytirish: eng yaxshi himoya](#3911-bogliqliklarni-kamaytirish-eng-yaxshi-himoya)
- [39.12 Sonar natijasi bilan bog'liqlik hisobotini birga o'qish](#3912-sonar-natijasi-bilan-bogliqlik-hisobotini-birga-oqish)
- [39.13 Amalda qo'llash](#3913-amalda-qollash)

</details>


Quality gate yashil bo'lishi loyihada xavf yo'q degani emas. Zamonaviy Spring Boot ilovasida yozilgan kod umumiy bayt hajmining juda kichik qismini tashkil qiladi, qolgani esa `pom.xml` yoki `build.gradle` orqali kelgan kutubxonalar. Shu bobda bog'liqlik zaifliklari qanday aniqlanishi, tranzitiv bog'liqlik nima uchun eng xavfli joy bo'lishi, zaiflik tekshiruvini CI ga qanday ulash va litsenziya masalasiga qanday qarash kerakligini ko'rib chiqamiz. Maqsad bitta: Sonar hisoboti bilan bog'liqlik hisobotini bir stolda o'qishni o'rganish.

## 39.1 Sonar kodingizni tekshiradi, bog'liqliklaringizni esa to'liq tekshirmaydi

SonarQube ning asosiy ishi statik analiz: sizning manba kodingizni parse qiladi, qoidalarni qo'llaydi, issue chiqaradi. U `OrderService.java` ichidagi null dereference yoki SQL konkatenatsiyasini ko'radi. Lekin `spring-boot-starter-web` orqali kelgan bironta JAR ichidagi ma'lum zaiflik Sonar ning klassik qoidalar to'plamida issue sifatida paydo bo'lmaydi.

Bu yerda halol bo'lish kerak. SonarQube va SonarCloud oilasida bog'liqliklarni tekshirish imkoniyati vaqt o'tishi bilan qo'shilgan va o'zgargan. Qaysi nashrda (Community, Developer, Enterprise) va qaysi versiyada bu nima deb nomlanishi, nimani qamrab olishi va litsenziya tahlili bor-yo'qligi farq qiladi. Shuning uchun bu yerda aniq funksiya nomlarini sanab chiqarmaymiz. O'z o'rnatmangiz uchun rasmiy hujjatdan tekshiring: nashr, versiya va ulangan plugin ro'yxatiga qarab javob boshqacha chiqadi.

Amaliy xulosa shu: bog'liqlik zaifligini alohida vosita bilan tekshirishni rejalashtiring. Agar Sonar o'rnatmangiz buni qamrab olsa, ikkinchi vosita ortiqcha ishonch bo'ladi. Agar qamrab olmasa, siz yagona himoyasiz qolmaysiz.

## 39.2 Bog'liqlik zaifligi nima va u qanday aniqlanadi (ma'lum zaifliklar bazasi)

Bog'liqlik zaifligi deganda ishlatayotgan kutubxonangizning ma'lum versiyasida topilgan va ommaga e'lon qilingan xavfsizlik nuqsoni tushuniladi. Har bir bunday nuqsonga CVE identifikatori beriladi, masalan `CVE-2021-44228`. Uning jiddiyligi CVSS ball bilan o'lchanadi, 0 dan 10 gacha.

Aniqlash mexanizmi tasavvur qilgandan ancha soddaroq. Vosita sizning bog'liqliklar ro'yxatini yig'adi, har bir artifact uchun uning koordinatasini aniqlaydi (`groupId:artifactId:version`), keyin bu koordinatani ma'lum zaifliklar bazasidagi yozuvlar bilan solishtiradi. Baza sifatida ko'pincha NVD, GitHub Advisory Database yoki OSV ishlatiladi.

Demak bu statik analiz emas, balki ro'yxatni ro'yxat bilan taqqoslash. Shundan ikkita muhim natija kelib chiqadi. Birinchisi: vosita kutubxona ichidagi kodni o'qimaydi, faqat versiya raqamiga qaraydi. Ikkinchisi: baza yangilanmasa, tekshiruv ham eskiradi. Offline rejimda ishlayotgan CI da baza keshini muntazam yangilash alohida vazifa bo'ladi.

Yana bir nozik joy: vosita zaif funksiya sizning kodda chaqirilishini bilmaydi. Zaiflik bor, lekin siz unga tegadigan yo'ldan foydalanmasligingiz mumkin. Buni reachability tahlili deyiladi va u hamma vositada yo'q.

## 39.3 Tranzitiv bog'liqlik: siz qo'shmagan kutubxona ham sizniki

Siz `pom.xml` ga o'n qator qo'shasiz, natijada classpath da yuz ellik JAR paydo bo'ladi. Qolganlari tranzitiv bog'liqlik: sizning bog'liqliklaringizning bog'liqliklari. Xavfning katta qismi aynan shu yerda yashaydi, chunki bu artifactlarni siz tanlamadingiz va ularning versiyasini bilmaysiz.

Log4Shell voqeasi buni yaxshi ko'rsatdi. Ko'p jamoalar `log4j-core` ni hech qachon o'z qo'li bilan qo'shmagan edi, u boshqa kutubxona orqali kelgan. Shuning uchun birinchi savol har doim bitta: bu artifact classpath ga kim orqali kirdi.

Maven da versiya tanlash qoidasi "nearest definition wins", ya'ni daraxtda ildizga eng yaqin e'lon g'olib bo'ladi. Gradle da esa odatiy xulq boshqacha, u konflikt bo'lganda eng yuqori versiyani tanlaydi. Bu farqni bilish kerak, aks holda "nega men qo'ygan versiya qo'llanmadi" degan savol javobsiz qoladi.

Spring Boot da eng toza yechim BOM orqali versiyani boshqarish. `spring-boot-dependencies` allaqachon yuzlab artifact versiyasini muvofiqlashtirib beradi. Bitta tranzitiv artifactni ko'tarish kerak bo'lsa, uni property orqali yoki `dependencyManagement` bo'limida bir joyda bosh.

```xml
<!-- Tranzitiv artifactni bir joyda boshqarish -->
<dependencyManagement>
  <dependencies>
    <dependency>
      <!-- Spring Boot BOM: yuzlab versiyani muvofiqlashtiradi -->
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-dependencies</artifactId>
      <version>${spring-boot.version}</version>
      <type>pom</type>
      <scope>import</scope>
    </dependency>
    <dependency>
      <!-- Zaif tranzitiv versiyani majburan ko'tarish -->
      <groupId>com.example.lib</groupId>
      <artifactId>json-utils</artifactId>
      <version>2.14.3</version>
    </dependency>
  </dependencies>
</dependencyManagement>
```

## 39.4 Maven va Gradle da bog'liqlik daraxtini ko'rish

Har qanday muhokama shu buyruqdan boshlanadi. Hisobotda noma'lum artifact chiqdi, siz esa uning kelib chiqishini bilmaysiz. Daraxtni chiqarib, zanjirni ko'rasiz.

```bash
# Maven: butun daraxt faylga
mvn -q dependency:tree -DoutputFile=target/deps.txt

# Faqat kerakli artifact va uning ota-onasi
mvn dependency:tree -Dincludes=com.fasterxml.jackson.core:jackson-databind

# Yakuniy tanlangan versiyalar va konfliktlar
mvn dependency:tree -Dverbose

# Gradle: runtime classpath uchun daraxt
./gradlew dependencies --configuration runtimeClasspath

# Gradle: bitta artifact qaysi yo'l bilan kelgani
./gradlew dependencyInsight \
  --dependency jackson-databind \
  --configuration runtimeClasspath
```

Ikkita maslahat. Birinchisi: `runtimeClasspath` ni tekshiring, `compileClasspath` ni emas. Ishlab turgan ilovaga nima yuklansa, xavf shundan keladi. Ikkinchisi: test uchun ishlatiladigan artifact prod ga chiqmaydi, shuning uchun uni ajratib qarang. `test` scope dagi zaiflik ham muhim, lekin ustuvorligi boshqacha.

Daraxtni CI artifact sifatida saqlab qo'yish ham foydali. Keyinchalik "o'sha hafta qaysi versiya edi" degan savolga javob topish osonlashadi.

## 39.5 Zaiflikni tekshiruvchi vositalar: OWASP Dependency-Check, Trivy, Grype, Dependabot

To'rtta vosita to'rt xil o'rinda turadi va ular bir-birini almashtirmaydi.

OWASP Dependency-Check build ichida ishlaydi, Maven va Gradle plugini bor, NVD ma'lumotlariga tayanadi va HTML yoki JSON hisobot beradi. Kuchli tomoni: build ga chuqur integratsiya. Og'ir tomoni: NVD bazasini yuklab olish va keshlash vaqt oladi, API kalit va kesh katalogini oldindan sozlash kerak.

Trivy container image, filesystem va repository ni skanerlaydi. Agar siz Spring Boot ni Docker image sifatida chiqarsangiz, Trivy bitta o'tishda ham JAR larni, ham base image dagi OS paketlarni ko'radi. Grype shunga yaqin vazifani bajaradi va SBOM fayl bilan yaxshi ishlaydi, uning hamkori Syft SBOM yaratadi.

Dependabot boshqa darajada ishlaydi. U sizning repository ni kuzatadi va zaiflik yoki yangi versiya chiqqanda avtomatik pull request ochadi. Ya'ni bu skaner emas, bu yangilash oqimi. Ikkisi birga eng yaxshi natija beradi: skaner xavfni ko'rsatadi, Dependabot uni yopadigan PR tayyorlaydi.

```yaml
# .github/dependabot.yml - haftalik yangilash PR lari
version: 2
updates:
  - package-ecosystem: "maven"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
    # Mayda patch larni bitta PR ga yig'ish
    groups:
      spring-patches:
        patterns:
          - "org.springframework*"
        update-types:
          - "patch"
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "monthly"
```

## 39.6 Natijani CI ga ulash va qaysi daraja build ni bloklashi

Birinchi kundan boshlab build ni yiqitish eng tez-tez uchraydigan xato. Katta legacy loyihada skanerni yoqishingiz bilan yuzlab topilma chiqadi, pipeline qizil bo'ladi, jamoa esa bir hafta ichida tekshiruvni butunlay o'chirib tashlaydi.

To'g'ri yo'l bosqichli. Avval skanerni hisobot rejimida ishlatasiz, build yiqilmaydi. Ikki hafta ichida mavjud topilmalarni ro'yxatga olasiz va baseline qilasiz. Keyin faqat yangi topilmalar uchun blok qo'yasiz. Bu Sonar ning "new code" falsafasiga aynan mos keladi va shu mantiqni bog'liqliklarga ham ko'chirish mumkin.

Blok chegarasi haqida aniq qaror yozib qo'yilsin. Amaliyotda keng tarqalgan taqsimot: Critical darajasidagi topilma prod release ni bloklaydi, High darajasi asosli izoh talab qiladi, Medium va pastrog'i backlog ga tushadi. Raqam emas, qaror muhim: kim va qancha vaqt ichida javob beradi.

```yaml
# GitHub Actions: avval hisobot, keyin blok
name: dependency-scan
on: [pull_request]
jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: "21"
      # 1-bosqich: har qanday holatda hisobot yig'iladi
      - name: Skaner
        run: ./gradlew dependencyCheckAnalyze || true
      - name: Hisobotni saqlash
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: dependency-report
          path: build/reports/
      # 2-bosqich: baseline tayyor bo'lgandan keyin yoqiladi
      - name: Yangi topilmalar uchun blok
        run: ./gradlew dependencyCheckAnalyze
```

## 39.7 False positive va zaiflikni asosli ravishda e'tiborsiz qoldirish

Versiya taqqoslashga asoslangan tekshiruv noto'g'ri signal berishi tabiiy. Ikki xil loyiha bir xil nom bilan chiqishi mumkin, artifact ichidagi metadata chalg'itishi mumkin, yoki CVE sizning ishlatish rejimingizga tegishli bo'lmasligi mumkin.

Bu yerda ikkita so'z aralashib ketadi. False positive: zaiflik umuman bu artifactga tegishli emas. Not applicable: zaiflik haqiqiy, lekin sizning kontekstingizda ekspluatatsiya qilinmaydi, masalan zaif komponent faqat test scope da yoki tashqi kirish yo'li yo'q.

Ikkala holatda ham javob bitta: suppress qiling, lekin izoh va muddat bilan. Izohsiz suppress eng yomon qarz turi, chunki bir yildan keyin uni kim va nega yozganini hech kim bilmaydi.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!-- dependency-check-suppressions.xml -->
<suppressions xmlns="https://jeremylong.github.io/DependencyCheck/dependency-suppression.1.3.xsd">
  <suppress until="2026-01-31Z">
    <notes><![CDATA[
      Sabab: bu CVE faqat SSL server rejimida ta'sir qiladi.
      Bizda kutubxona faqat client sifatida ishlatiladi.
      Tekshirgan: platform-team, ticket PLAT-4412.
      Muddatdan keyin qayta ko'rib chiqilsin.
    ]]></notes>
    <packageUrl regex="true">^pkg:maven/com\.example/net\-client@.*$</packageUrl>
    <cve>CVE-2024-11111</cve>
  </suppress>
</suppressions>
```

`until` atributi muhim. U suppress ni avtomatik eskiradigan qiladi, shuning uchun ro'yxat yildan yilga shishib ketmaydi.

## 39.8 Yangilash siyosati: qachon darhol, qachon rejali

Har bir zaiflikni o'sha kuni yopish real emas, hammasini keyinga qoldirish esa xavfli. Shuning uchun yozma siyosat kerak va u ikki o'qqa tayanadi: zaiflikning jiddiyligi va komponentning kirish yo'liga yaqinligi.

Darhol yangilash talab qiladigan holat: tashqi trafik qabul qiluvchi komponentda remote code execution yoki autentifikatsiyani chetlab o'tish. Bunday holatda release jadvali kutilmaydi, hotfix branch ochiladi.

Rejali yangilash: kutubxonaning minor versiyasi, test infratuzilmasidagi zaiflik, ichki tarmoqdan boshqa kirish yo'li bo'lmagan komponent. Bunday ishlar sprint ichidagi texnik ulushga kiradi.

Alohida eslatma Spring Boot haqida. Boot ning patch versiyasini ko'tarish ko'pincha o'nlab tranzitiv artifactni bir yo'la yangilaydi. Shuning uchun "Boot ni oyda bir marta patch darajasida ko'tarish" odati alohida CVE lar bilan kurashishdan ko'ra arzonga tushadi. Java ning LTS versiyasi va JaCoCo 0.8.x kabi build vositalari uchun ham xuddi shu mantiq amal qiladi.

Yangilashdan keyin regressiya testi majburiy. Bu yerda [testlash qo'llanmasidagi](../testing/README.md) Testcontainers va integratsion test mavzulari kerak bo'ladi, chunki kutubxona yangilanishini unit test yolg'iz qo'lga ilmaydi.

## 39.9 SBOM nima va u nimaga kerak

SBOM (Software Bill of Materials) ilovangiz ichida nima borligining mashina o'qiy oladigan ro'yxati. Har bir komponent nomi, versiyasi, koordinatasi va ko'pincha litsenziyasi yoziladi. Ikki keng tarqalgan format bor: CycloneDX va SPDX.

Nima uchun kerak. Yangi CVE e'lon qilinganda savol bitta bo'ladi: bizda bormi va qaysi release da bor. SBOM bo'lsa, javobni daqiqalarda topasiz. SBOM bo'lmasa, har bir release ni qayta build qilib tekshirishga to'g'ri keladi.

Shuning uchun SBOM ni release artifact qatorida saqlash kerak, build papkasida qoldirmaslik kerak. Har bir versiya uchun o'z SBOM fayli bo'lsin.

```bash
# CycloneDX plugin bilan SBOM yaratish (Maven)
mvn org.cyclonedx:cyclonedx-maven-plugin:makeAggregateBom

# Syft bilan image dan SBOM
syft packages registry:myrepo/orders:1.4.2 -o cyclonedx-json > sbom.json

# SBOM faylini zaiflikka tekshirish
grype sbom:sbom.json

# Container image ni to'g'ridan-to'g'ri skanerlash
trivy image myrepo/orders:1.4.2
```

## 39.10 Litsenziya tekshiruvi: qaysi litsenziya xavfli bo'lishi mumkin

Litsenziya xavfi texnik emas, huquqiy. Kod ishlaydi, test o'tadi, lekin kompaniya ustida majburiyat paydo bo'ladi. Shuning uchun bu masalani muhandis yolg'iz hal qilmaydi.

Umumiy manzara shunday. Permissive litsenziyalar (Apache-2.0, MIT, BSD) tijorat mahsulotida odatda muammosiz ishlatiladi. Weak copyleft (LGPL, MPL, EPL) kutubxona sifatida ishlatishga ruxsat beradi, lekin o'zgartirish va bog'lash shartlari bor. Strong copyleft (GPL, AGPL) esa sizning mahsulotingizga ham o'z shartini yoyishi mumkin, AGPL bunda tarmoq orqali xizmat ko'rsatishni ham qamrab oladi.

Eng xavfli holat: litsenziyasi noma'lum yoki ko'rsatilmagan artifact. Uni "ehtimol muammo yo'q" deb o'tkazib yuborish xato, chunki huquqiy maydonda sukut ruxsat degani emas.

Amaliy yondashuv: yozma ruxsat ro'yxati tuzing, build vaqtida tekshiring. Yangi litsenziya chiqsa, build ogohlantirish beradi va qaror yuridik javobgar odam bilan birga qabul qilinadi. Bu yerda ham aniq huquqiy maslahat bermayman, bu kompaniyangiz yuristi ishi. Vositaning ishi faqat bitta: ro'yxatni ko'rinadigan qilish.

## 39.11 Bog'liqliklarni kamaytirish: eng yaxshi himoya

Skanerlash muhim, lekin eng arzon himoya kutubxonani umuman qo'shmaslik. Har bir yangi artifact uchta xarajat keltiradi: zaiflik maydoni kengayadi, yangilash yuki ortadi, litsenziya xavfi qo'shiladi.

Shuning uchun yangi bog'liqlik qo'shishdan oldin uchta savol bering. Birinchisi: bu ishni standart kutubxona yoki Spring ning o'zi bajara oladimi. Ikkinchisi: biz uning necha foiz imkoniyatidan foydalanamiz. Uchinchisi: bu kutubxona faol qo'llab-quvvatlanadimi, oxirgi release qachon chiqqan.

Amalda eng ko'p uchraydigan ortiqcha narsalar: faqat bitta yordamchi metod uchun qo'shilgan katta utility kutubxona, Java 17 dan keyin keraksiz bo'lib qolgan collection yoki date kutubxonalari, va ikki xil JSON kutubxonasini bir vaqtda ushlab turish.

Bir nozik joy bor. Kutubxonani olib tashlab, o'rniga uning mantiqini o'zingiz yozsangiz, xavf statik analizga ko'chadi. Ya'ni Sonar sizdan kattaroq hisob so'raydi: cyclomatic complexity, coverage, duplication. Shuning uchun qaror "har doim o'zimiz yozamiz" emas, balki "kichik va tushunarli narsani o'zimiz, murakkab va xavfsizlikka tegishli narsani sinovdan o'tgan kutubxona bilan".

| Masala | Oddiy yondashuv | Arxitektor yondashuvi |
| --- | --- | --- |
| Zaiflik tekshiruvi | Hujum bo'lgandan keyin qo'lda qarash | Har PR da avtomatik skaner, baseline bilan |
| Tranzitiv artifact | Classpath da nima borligi noma'lum | Daraxt CI artifact sifatida saqlanadi |
| Versiya boshqaruvi | Har modulda alohida versiya yozilgan | BOM va bitta `dependencyManagement` joyi |
| Build ni bloklash | Birinchi kundan hammasini bloklash | Bosqichli: hisobot, baseline, yangi topilma |
| False positive | Skanerni butunlay o'chirish | Izoh va `until` muddati bilan suppress |
| Yangilash | Faqat majbur bo'lganda ko'tarish | Oylik patch oqimi, Dependabot PR lari |
| Release tarkibi | Build qayta tiklanib tekshiriladi | Har release uchun saqlangan SBOM |
| Litsenziya | Hech kim qaramaydi | Ruxsat ro'yxati build da tekshiriladi |
| Yangi kutubxona | Birinchi topilgani qo'shiladi | Uchta savol va qo'llab-quvvatlanish tekshiruvi |
| Javobgarlik | "Xavfsizlik jamoasi ko'radi" | Egasi va SLA yozma belgilangan |

## 39.12 Sonar natijasi bilan bog'liqlik hisobotini birga o'qish

Ikki hisobot ikki xil savolga javob beradi. Sonar: "men yozgan kodda qanday nuqson bor". Bog'liqlik skaneri: "men ishlatayotgan kodda qanday ma'lum nuqson bor". Qaror qabul qilish uchun ikkisini bir vaqtda ko'rish kerak.

Eng foydali kesishma nuqtasi Sonar ning security hotspot tushunchasi. Hotspot o'zi xato emas, u insoniy ko'rikni talab qiladigan joy. Agar hotspot aynan zaif kutubxona ishlatiladigan joyda chiqsa, bu ikki signalning ustma-ust tushishi va u eng yuqori ustuvorlikka chiqadi.

Teskari holat ham bor. Zaiflik hisobotida artifact qizil, lekin Sonar ko'rsatgan kod yo'llari u bilan hech qanday aloqada emas. Bu suppress uchun asos emas, lekin ustuvorlikni pasaytirish uchun argument bo'ladi.

Bitta dashboard tuzish amalda yaxshi natija beradi: Sonar quality gate holati, yangi issue soni, coverage foizi, hamda Critical va High zaiflik soni va eng eski ochiq zaiflikning yoshi. Oxirgi raqam eng gapiradigan metrika, chunki u jamoaning javob tezligini ko'rsatadi.

| Tuzoq | Yechim |
| --- | --- |
| Quality gate yashil, lekin classpath da zaif JAR bor | Zaiflik skanerini alohida pipeline bosqichi qilish |
| Skaner `compileClasspath` ni tekshiradi | `runtimeClasspath` ni, ya'ni haqiqiy ishga tushadiganini tekshirish |
| NVD bazasi CI da har safar qaytadan yuklanadi | Kesh katalogini saqlash va API kalitini sozlash |
| Suppress ro'yxati yildan yilga o'sib boradi | Har yozuvga izoh va `until` muddati, choraklik ko'rik |
| Zaiflik yopildi, lekin regressiya tekshirilmadi | Yangilash PR ida integratsion testlarni majburiy qilish |
| Faqat JAR lar skanerlanadi, base image e'tibordan chetda | Container image ni ham skanerlash, SBOM ni image dan olish |
| Litsenziyasi noma'lum artifact jimgina o'tib ketadi | Noma'lum litsenziyani build da ogohlantirish sifatida belgilash |
| Zaiflik hisoboti hech kimga tegishli emas | Har komponentga egasi va javob muddati biriktirilgan |

## 39.13 Amalda qo'llash

- [ ] `mvn dependency:tree -DoutputFile=target/deps.txt` yoki `./gradlew dependencies --configuration runtimeClasspath` ni ishga tushirib, hozirgi classpath ro'yxatini faylga saqlang va repository ga qo'ying.
- [ ] O'z SonarQube nashri va versiyasi bog'liqlik tahlilini qamrab oladimi degan savolni rasmiy hujjatdan tekshirib, javobni jamoa wiki siga bir paragraf qilib yozib qo'ying.
- [ ] Bitta skanerni (OWASP Dependency-Check, Trivy yoki Grype) CI ga hisobot rejimida ulang, hozircha build ni bloklamasin, hisobot artifact sifatida saqlansin.
- [ ] Ikki hafta ichida chiqqan topilmalardan baseline tuzing va shundan keyin faqat yangi Critical topilma uchun blok qoidasini yoqing.
- [ ] Mavjud suppress yozuvlarini ko'rib chiqing, har biriga sabab izohi, mas'ul va `until` muddatini qo'shing, muddati o'tganini o'chiring.
- [ ] CycloneDX yoki Syft bilan SBOM yaratishni release pipeline ga qo'shing va faylni har versiya uchun alohida saqlanadigan artifactga aylantiring.
- [ ] Ruxsat berilgan litsenziyalar ro'yxatini yozma hujjat qilib tasdiqlang va noma'lum litsenziyali artifact chiqqanda ogohlantirish beradigan tekshiruv qo'shing.
- [ ] Dependabot yoki shunga o'xshash yangilash oqimini yoqing, Spring Boot patch versiyasini oylik ko'tarish odatini sprint rejasiga kiritib, har yangilash PR ida integratsion testlar majburiy bo'lsin.

---

[&larr; 38. Ko'p tilli loyiha: SQL, XML, YAML, Docker, Kubernetes, frontend](38-kop-tilli-loyiha-sql-xml-yaml-docker.md) · [Mundarija](README.md) · [40. Sonar va boshqa vositalar: qachon qaysi biri &rarr;](40-sonar-va-boshqa-vositalar-qachon-qaysi-biri.md)
