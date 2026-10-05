<!-- doc: sonarqube | chapter: 21 | part: VI. Amaliyot va jarayon -->

[Barcha hujjatlar](../../README.md) / [SonarQube](README.md)

# 21. CI/CD ga ulash, PR decoration va blokirovka (CI/CD Integration)

<details>
<summary>Bu bobdagi 12 bo'lim</summary>

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

</details>



SonarQube lokal kompyuterda ishga tushganda foyda beradi, lekin haqiqiy kuchi CI pipeline ichida ochiladi. Faqat o'sha joyda tahlil har bir commit uchun avtomatik bajariladi va quality gate natijasi merge qarorini boshqaradi. Bu bobda tahlilni pipeline ga qanday tartibda qo'yish, pull request natijasini qayerda ko'rish va qaysi texnik tuzoqlar eng ko'p vaqt yo'qotishini ko'rib chiqamiz. Test turlarini qanday yozish va CI da umuman qanday pipeline qurish masalasi [testlash qo'llanmasidagi](../testing/README.md) CI/CD test pipeline mavzusida, bu yerda faqat Sonar qismi.

## 21.1 Pipeline dagi to'g'ri tartib: qurish, test, coverage hisoboti, tahlil, gate kutish

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

## 21.2 GitHub Actions da sozlash: qadamlar, kesh, token saqlash

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

## 21.3 GitLab CI va Jenkins da sozlashning farqlari

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

## 21.4 Pull request tahlili: qanday ulanadi va natija qayerda ko'rinadi

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

## 21.5 PR decoration: izohlar, holat belgisi va merge ni bloklash

PR decoration server tomonda sozlanadi, CI da emas. Buning uchun SonarQube da ALM integration yoziladi: GitHub uchun GitHub App yoki token, GitLab uchun api scope li token. Keyin har bir loyiha o'sha integration ga va aniq repository ga bog'lanadi. Bog'lanish yo'q bo'lsa tahlil muvaffaqiyatli o'tadi, lekin PR da hech qanday izoh paydo bo'lmaydi.

Decoration uch ko'rinishda keladi. Birinchisi PR ga yoziladigan umumiy xulosa izohi: nechta yangi issue, new code coverage va duplication foizi. Ikkinchisi aniq qatorlarga qo'yiladigan inline izohlar. Uchinchisi PR check holati, ya'ni yashil yoki qizil belgi.

Merge ni Sonar o'zi bloklamaydi. Bu juda muhim nuqta. Sonar faqat check holatini yuboradi. Merge ni bloklash GitHub tomonda branch protection rule yoki ruleset bilan qilinadi: Sonar check ni "required status check" ro'yxatiga qo'shish kerak. GitLab da esa MR ni bloklash uchun pipeline muvaffaqiyatli bo'lishi talab qilinadi va Sonar job `allow_failure: false` bo'lishi shart.

Shundan kelib chiqadigan amaliy xulosa: gate ni qattiq qilish uchun ikkita mustaqil sozlama kerak. Bittasi Sonar tomonda quality gate shartlari. Ikkinchisi Git platformasi tomonda check ni majburiy qilish. Faqat bittasini qilish bloklash illyuziyasini beradi.

## 21.6 `sonar.qualitygate.wait` bilan build ni to'xtatish va timeout masalasi

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

## 21.7 Token va maxfiy ma'lumotni CI da saqlash

Token turini to'g'ri tanlash xavfni sezilarli kamaytiradi. SonarQube da bir nechta token turi bor va ularning imkoniyati farq qiladi. CI uchun eng tor variant loyiha darajasidagi analysis token, chunki u faqat bitta loyihani tahlil qilishga yetadi. User token esa o'sha foydalanuvchining barcha huquqlarini olib yuradi, ya'ni token oqib ketsa zarar kattaroq.

Tokenni hech qachon repository ichida saqlamang. Na `pom.xml` da, na `sonar-project.properties` da, na Dockerfile da. Uning joyi faqat CI secret store: GitHub Actions secrets, GitLab masked va protected variable, Jenkins credentials.

Tokenni `-Dsonar.token=` orqali buyruq qatorida uzatmang. Buyruq qatori jarayon ro'yxatida va ba'zan log da ko'rinadi. To'g'ri yo'l `SONAR_TOKEN` muhit o'zgaruvchisi, chunki scanner uni o'zi o'qiydi.

Token muddatini belgilang va aylantirish jadvalini yozib qo'ying. Muddatsiz token qulay, lekin u yillar davomida kimning qo'lida qolganini hech kim bilmaydi. Muddat tugashi build ni yiqitadi va bu yaxshi signal, chunki u aylantirish vaqti kelganini aytadi.

Huquq berishda eng kam imkoniyat qoidasiga amal qiling. CI foydalanuvchisiga faqat "Execute Analysis" huquqi kerak. Unga administrator huquqi berish keng tarqalgan xato, chunki keyin o'sha token quality gate shartlarini ham o'zgartira oladi.

## 21.8 Shallow clone muammosi va `fetch-depth` sozlash

Sonar git blame ma'lumotini ishlatadi. Blame orqali u har qatorning sanasi va muallifini biladi. Shu ma'lumot ustiga uchta narsa qurilgan: new code chegarasini aniqlash, issue ni mualliflarga biriktirish va yangi issue larni eski issue lardan ajratish.

CI tizimlari tezlik uchun default holda qisqartirilgan clone qiladi. GitHub Actions `actions/checkout` da bitta commit oladi. GitLab `GIT_DEPTH` ni kichik qiymatga qo'yadi. Jenkins da "shallow clone" opsiyasi tez tez yoqilgan bo'ladi.

Natija ko'pincha chalkash ko'rinadi. New code bo'limi bo'sh chiqadi, yoki aksincha butun fayl yangi deb hisoblanadi. Issue lar hech kimga biriktirilmaydi. Ba'zan log da blame ma'lumoti topilmagani haqida ogohlantirish chiqadi va u e'tibordan chetda qoladi.

Yechim bitta: tahlil qilinadigan job da to'liq tarix bo'lsin. GitHub Actions da `fetch-depth: 0`, GitLab da `GIT_DEPTH: "0"`, Jenkins da shallow clone ni o'chirish. Tarix og'ir bo'lsa, faqat Sonar job ida to'liq clone qiling, qolgan job larda qisqartirilgan qoldiring.

Yana bir nuance: `sonar.scm.disabled=true` parametri blame ni butunlay o'chiradi. Uni ba'zan tezlik uchun qo'yib yuboradilar va keyin new code nega ishlamayotganini tushunmaydilar. Bu parametr faqat git bo'lmagan muhitda o'rinli.

## 21.9 Fork dan kelgan PR va token yetishmasligi

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

## 21.10 Tahlil vaqtini qisqartirish: kesh, modul tanlash, parallel ish

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

Uchinchi qadam parallel ish. Testlarni parallel ishga tushirish foydali va bu [testlash qo'llanmasidagi](../testing/README.md) mavzu. Sonar qadamini esa parallel qilib bo'lmaydi: bitta projectKey uchun bir vaqtda ikki tahlil yuborish server navbatida ziddiyat tug'diradi. To'g'ri sxema: testlar parallel job larda ishlaydi, coverage hisobotlari artifact sifatida yig'iladi, keyin bitta yakuniy job ularni birlashtirib tahlil yuboradi.

To'rtinchi qadam PR da yengilroq tahlil. PR tahlili tabiatan kichikroq, chunki u faqat o'zgargan qatorlarga qaraydi. Lekin kompilyatsiya va test to'liq bajariladi. Shuning uchun PR pipeline da og'ir integratsion test to'plamini ajratib, Sonar uchun kerakli minimal coverage ni ta'minlash ko'p hollarda yetarli.

Agar scanner xotira yetmasligidan yiqilsa, `sonar.scanner.javaOpts` bilan heap ni oshirish vaqtinchalik yordam beradi. Asl yechim esa tahlil hajmini kamaytirish, chunki heap ni cheksiz oshirib bo'lmaydi.

## 21.11 Tahlil uzilganda nima qilish: qayta urinish yoki bloklashni yumshatish

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

## 21.12 Amalda qo'llash

- [ ] Pipeline da tartibni tekshirib chiqing: `verify` tugagandan keyin `jacoco.xml` mavjudligini aniq shart bilan tasdiqlang, keyingina `sonar:sonar` ishga tushsin.
- [ ] Barcha CI konfiguratsiyasida to'liq git tarixini yoqing: `fetch-depth: 0` yoki `GIT_DEPTH: "0"`, keyin Sonar UI da new code bo'limi to'lganini tekshiring.
- [ ] Har bir tahlil qadamiga `-Dsonar.qualitygate.wait=true` va aniq `sonar.qualitygate.timeout` qo'shing, so'ngra ataylab qoidani buzuvchi commit bilan build yiqilishini sinab ko'ring.
- [ ] Tokenni loyiha darajasidagi analysis token ga almashtiring, muddat belgilang, CI secret store ga ko'chiring va buyruq qatoridan olib tashlang.
- [ ] Git platformasi tomonda Sonar check ni required status check qilib qo'ying, chunki Sonar o'zi merge ni bloklamaydi.
- [ ] Fork dan kelgan PR uchun `if` sharti yozib, tahlilni ataylab o'tkazib yuboring va log da sababni yozdiring.
- [ ] `~/.m2` va `~/.sonar/cache` keshini yoqib, tahlil vaqtini o'lchang, keyin generatsiya qilingan kodni exclusions ga qo'shib qayta o'lchang.
- [ ] Mavjud barcha `continue-on-error` va `allow_failure: true` holatlarini ro'yxatlang, har biriga sana va sabab yozing, muddati o'tganini olib tashlang.

---

[&larr; 20. Mutation testing: 100% coverage qachon yolg'on](20-mutation-testing-100-coverage-qachon-yolgon.md) · [Mundarija](README.md) · [22. Lokal tekshirish: IDE, sonar-scanner va tez qaytish &rarr;](22-lokal-tekshirish-ide-sonar-scanner-va-tez.md)
