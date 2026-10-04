<!-- doc: sonarqube | chapter: 2 | part: I. SonarQube qanday ishlaydi -->

[SonarQube](../../README.md) / [SonarQube](README.md)

# 2. Scanner nimani yig'adi va qanday yuboradi (What the Scanner Collects)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

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

</details>



Sonar serverdagi quality gate qanchalik aqlli sozlangan bo'lsa ham, u faqat scanner yuborgan ma'lumot ustida ishlaydi. Scanner esa sizning konfiguratsiyangizga so'zsiz bo'ysunadi: siz ko'rsatmagan papkani o'qimaydi, siz ulamagan coverage hisobotini o'ylab topmaydi, kompilyatsiya natijasini topmasa esa qoidalarning yarmini jimgina o'chiradi. Shuning uchun "nega mening testlarim bor, lekin coverage 0%" degan savolning javobi deyarli har doim serverda emas, `sonar-project.properties` faylida yoki build loginida yotadi. Bu bobda scanner nimani yig'adi, nimani ko'rmaydi va yuborishdan oldin buni qanday tekshirish mumkinligini ko'rib chiqamiz.

## 2.1 `sonar-project.properties` va asosiy parametrlar

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

## 2.2 Manba va test papkalarini to'g'ri ko'rsatish

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

## 2.3 `sonar.java.binaries` va `sonar.java.libraries`: nega majburiy

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

## 2.4 Tashqi hisobotlarni ulash

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

Integratsion testlar coverage ga qanday qo'shilishi [testlash qo'llanmasidagi](../testing/README.md) "integratsion test va Testcontainers" mavzusiga tegishli. Bu yerda muhimi shu: agar `failsafe` bosqichi `verify` dan oldin tugamasa, uning coverage ma'lumoti XML ga tushmaydi.

## 2.5 Maven, Gradle va mustaqil scanner

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

## 2.6 Scanner qaysi fayllarni umuman ko'rmaydi

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

## 2.7 Tahlilni lokal tekshirish va ogohlantirishlarni o'qish

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

## 2.8 SCM ma'lumoti: blame nega kerak

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

## 2.9 Monorepo va ko'p modulli loyiha

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

## 2.10 Scanner keshi, vaqt va takroriy tahlil

Scanner ishga tushganda loyiha ildizida `.scannerwork` papkasini yaratadi va u yerga ichki holat bilan birga `report-task.txt` ni yozadi. Shu fayl ichida tahlil natijasi joylashgan URL va task id bo'ladi, shuning uchun pipeline ning keyingi qadamida natijaga havola berish uchun undan foydalanish mumkin. Bu papkani build artifact sifatida saqlash diagnostikani ancha osonlashtiradi.

Tahlil vaqti asosan ikki narsaga ketadi: fayllarni indekslash va semantik tahlil. Shuning uchun vaqtni qisqartirishning real yo'llari ham shu ikki joyda. Generatsiya qilingan kodni exclusion ga olish indekslashni kamaytiradi. Monorepo da faqat o'zgargan modulni tahlil qilish eng katta foyda beradi. Gradle da `sonar.gradle.skipCompile` kabi parametrlar bilan qayta kompilyatsiyani o'tkazib yuborish mumkin, lekin bunda binaries allaqachon mavjud bo'lishi shart.

Takroriy tahlil haqida muhim fakt: bir xil kodni ikki marta yuborish issue larni ikkilantirmaydi. Sonar har tahlilda loyihaning yangi holatini quradi va eski issue larni fayl, qoida va kod konteksti bo'yicha moslaydi. Shu sababli kod qatorlarini ko'chirish issue ni "yangi" qilib qo'yishi mumkin, holbuki mazmunan u o'sha eski muammo. Katta refaktoring dan keyin new code bo'yicha gate kutilmaganda qizil bo'lishining sababi odatda shu.

Nihoyat, CI keshi bilan ehtiyot bo'lish kerak. Maven repository keshini saqlash foydali. Lekin `target` papkasini keshlash xavfli: eski `.class` fayllar yangi manba kod bilan birga yuborilsa, semantik tahlil mos kelmaydigan model quradi va tushunarsiz natija beradi. Har tahlil oldidan `clean` ishlatish bu sinfdagi muammolarni butunlay yo'q qiladi.

## 2.11 Amalda qo'llash

- [ ] `sonar-project.properties` yoki POM da `sonar.sources` va `sonar.tests` aniq ajratilganini tekshiring, test papkasi manba ro'yxatida bo'lmasin.
- [ ] JaCoCo `report` goal ni `verify` fazasiga ulab, `target/site/jacoco/jacoco.xml` faylining build dan keyin haqiqatan mavjudligini tasdiqlang.
- [ ] Scanner log ini `grep "bytecode of dependencies"` bilan tekshirib, klasspath bo'sh emasligiga ishonch qiling.
- [ ] CI checkout qadamiga `fetch-depth: 0` qo'shing va blame ishlayotganini `git log -1` bilan tasdiqlang.
- [ ] Barcha mavjud `sonar.exclusions` qatorlarini qayta ko'rib chiqing: har biriga izoh yozing va coverage ni ko'tarish uchun qo'yilganlarini `sonar.coverage.exclusions` ga ko'chiring yoki olib tashlang.
- [ ] Monorepo bo'lsa har deploylanadigan servisga alohida `sonar.projectKey` ajratib, faqat o'zgargan servisni tahlil qiladigan qilib pipeline ni sozlang.
- [ ] `sonar.qualitygate.wait=true` ni yoqib, gate yiqilganda pipeline ning to'xtashini tekshirib ko'ring.
- [ ] CI da `target` papkasi keshlanmayotganini va har tahlil `clean` bilan boshlanishini tasdiqlang.

---

[&larr; 1. SonarQube arxitekturasi va tahlil oqimi](01-sonarqube-arxitekturasi-va-tahlil-oqimi.md) · [Mundarija](README.md) · [3. Issue turlari: bug, vulnerability, code smell, security hotspot &rarr;](03-issue-turlari-bug-vulnerability-code-smell.md)
