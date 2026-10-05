<!-- doc: sonarqube | chapter: 9 | part: III. Qamrov (coverage) -->

[Barcha hujjatlar](../../README.md) / [SonarQube](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 9. Coverage qanday o'lchanadi: JaCoCo mexanikasi (How Coverage Is Measured)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

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

</details>



SonarQube coverage raqamini o'zi hisoblamaydi. U faqat tashqi vositadan kelgan hisobotni o'qiydi, Java dunyosida bu deyarli har doim JaCoCo. Shuning uchun "coverage 68% chiqdi" degan savolning javobi Sonar da emas, JaCoCo ning bytecode bilan ishlash mexanikasida yotadi. Bu bobda probe qanday qo'yiladi, `jacoco.exec` ichida nima bor, qaysi ko'rsatkich Sonar ga boradi va nega ba'zi qator yashil bo'lsa ham branch sariq qolishini ko'rib chiqamiz.

## 9.1 JaCoCo qanday ishlaydi: bytecode ga instrumentatsiya qo'shish

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

## 9.2 Java agent va offline instrumentatsiya farqi

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

## 9.3 `jacoco.exec` fayli: nima yoziladi va qanday hisobotga aylanadi

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

## 9.4 Instruction, line, branch, complexity va method qamrovi farqi

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

## 9.5 SonarQube qaysi ko'rsatkichni oladi va `coverage` qanday hisoblanadi

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

## 9.6 Lambda, switch ifodasi va string konkatenatsiyasi bytecode da qanday ko'rinadi

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

## 9.7 Bytecode dagi yashirin shartlar: nega qator yashil, lekin branch sariq

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

## 9.8 Unit test va integratsion test qamrovini birlashtirish

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

## 9.9 Ko'p modulli loyihada umumiy hisobot yig'ish

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

## 9.10 Qamrov o'lchovining chegarasi: bajarilgan kod tekshirilgan degani emas

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

Qamrovning ikkinchi chegarasi ma'lumot bo'yicha. Branch qamrovi "ikki yo'nalish sinaldi" deydi, lekin `BigDecimal` yaxlitlash rejimi xato bo'lsa buni ko'rsatmaydi. `null`, bo'sh ro'yxat, manfiy miqdor va integer overflow kabi holatlar qamrov 100% bo'lganda ham sinalmagan bo'lishi mumkin. Shuning uchun qamrov yagona o'lchov bo'lmasligi kerak. Mutation testing, masalan PIT, kodni ataylab buzib testning sezgirligini o'lchaydi va qamrov ko'rsatmagan bo'shliqni topadi. Test sifatini oshirish usullari [testlash qo'llanmasidagi](../testing/README.md) test ma'lumotlari va metrikalar mavzularida batafsil berilgan.

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

## 9.11 Amalda qo'llash

- [ ] `mvn help:effective-pom | grep -A3 '<debug'` bilan debug ma'lumoti yoqilganini tasdiqlang, aks holda line coverage 0 bo'ladi.
- [ ] JaCoCo versiyasini 0.8.12 yoki undan yangisiga ko'taring va `lombok.config` ga `lombok.addLombokGeneratedAnnotation = true` qo'shing.
- [ ] `prepare-agent` va `prepare-agent-integration` ni ikki alohida `destFile` bilan sozlang, keyin `merge` va `report` goal larini `verify` fazasiga ulang.
- [ ] `sonar.coverage.jacoco.xmlReportPaths` ni XML hisobotga yo'naltiring va `.exec` yo'li qolmaganini tekshiring.
- [ ] Ko'p modulli loyihada kodsiz `coverage` modulini `report-aggregate` bilan yaratib, reactor da oxirgi qilib qo'ying.
- [ ] HTML hisobotdagi eng past branch qamrovi bo'lgan beshta metodni oching va har bir sariq rombcha uchun qaysi shart sinalmaganini yozib chiqing.
- [ ] Har bir `orElseThrow` va `Optional` lambda si uchun uni bajaradigan alohida test holati borligini tasdiqlang.
- [ ] PIT mutation testing ni eng muhim ikki paketga ulab, mutation score bilan line coverage o'rtasidagi farqni o'lchang.

---

[&larr; 8. 100% ga sozlangan gate: har bir shart nimani talab qiladi](08-100-ga-sozlangan-gate-har-bir-shart-nimani.md) · [Mundarija](README.md) · [10. JaCoCo va SonarQube ulanishi: Maven va Gradle sozlash &rarr;](10-jacoco-va-sonarqube-ulanishi-maven-va.md)
