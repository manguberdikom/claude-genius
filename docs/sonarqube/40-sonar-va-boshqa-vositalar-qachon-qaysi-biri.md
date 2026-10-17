<!-- doc: sonarqube | chapter: 40 | part: IX. Kengaytirish va integratsiya -->

[Barcha hujjatlar](../../README.md) / [SonarQube](README.md)

> Holat: tekshirilmoqda. Da'volar hali manbaga solishtirilmoqda.

# 40. Sonar va boshqa vositalar: qachon qaysi biri (Sonar and Other Tools)

<details>
<summary>Bu bobdagi 12 bo'lim</summary>

- [40.1 Sonar nimani yaxshi qiladi va nimani umuman qilmaydi](#401-sonar-nimani-yaxshi-qiladi-va-nimani-umuman-qilmaydi)
- [40.2 SpotBugs: bytecode darajasidagi tahlil va u qachon qo'shimcha qiymat beradi](#402-spotbugs-bytecode-darajasidagi-tahlil-va-u-qachon-qoshimcha-qiymat-beradi)
- [40.3 PMD va Checkstyle: uslub va qoidalar, Sonar bilan takrorlanishi](#403-pmd-va-checkstyle-uslub-va-qoidalar-sonar-bilan-takrorlanishi)
- [40.4 Error Prone va NullAway: kompilyatsiya paytida xato topish](#404-error-prone-va-nullaway-kompilyatsiya-paytida-xato-topish)
- [40.5 ArchUnit: arxitektura qoidalarini test sifatida yozish](#405-archunit-arxitektura-qoidalarini-test-sifatida-yozish)
- [40.6 Semgrep va shunga o'xshash qoida yozish vositalari](#406-semgrep-va-shunga-oxshash-qoida-yozish-vositalari)
- [40.7 Formatlash vositalari (Spotless kabi) va ularni bahsdan chiqarish](#407-formatlash-vositalari-spotless-kabi-va-ularni-bahsdan-chiqarish)
- [40.8 Vositalarni birlashtirish: qaysi biri bloklaydi, qaysi biri ogohlantiradi](#408-vositalarni-birlashtirish-qaysi-biri-bloklaydi-qaysi-biri-ogohlantiradi)
- [40.9 Takroriy ogohlantirishlarni kamaytirish: qoidalarni bo'lish](#409-takroriy-ogohlantirishlarni-kamaytirish-qoidalarni-bolish)
- [40.10 Pipeline da tartib va umumiy vaqt byudjeti](#4010-pipeline-da-tartib-va-umumiy-vaqt-byudjeti)
- [40.11 Kam vosita bilan ko'p foyda: minimal to'plam tavsiyasi](#4011-kam-vosita-bilan-kop-foyda-minimal-toplam-tavsiyasi)
- [40.12 Amalda qo'llash](#4012-amalda-qollash)

</details>



Sonar bitta vosita, u hamma narsani topmaydi. Ko'p jamoa shu yerda ikki xatodan birini qiladi: yoki Sonar dan boshqa hech narsani ishlatmaydi, yoki beshta vositani yoqib, bir xil ogohlantirishni uch joydan oladi. Bu bobda Sonar ning chegarasini chizib, qolgan vositalarni faqat ochiq qolgan bo'shliqqa qo'yamiz. Maqsad: eng kam vosita bilan eng ko'p haqiqiy xatoni topish, pipeline vaqtini esa o'stirmaslik.

## 40.1 Sonar nimani yaxshi qiladi va nimani umuman qilmaydi

Sonar ning asosiy kuchi uchta narsada. Birinchisi, markazlashgan tarix: issue, coverage, duplication va rating bir serverda saqlanadi. Ikkinchisi, "Clean as You Code" modeli: quality gate asosan new code ga qaraydi, shuning uchun eski loyihada ham joriy qilish mumkin. Uchinchisi, issue hayot sikli: false positive, won't fix, assignee, PR decoration.

Sonar yaxshi topadigan narsalar: haddan tashqari murakkab metod (`java:S3776`), takrorlangan string literal (`java:S1192`), o'lik kod, noto'g'ri `equals` va `hashCode` juftligi (`java:S1206`), SQL injection yo'li, va xavfli joyni security hotspot sifatida belgilash.

Null dereference (`java:S2259`) va yopilmagan resurs (`java:S2095`) ham shu ro'yxatda, lekin ular bitta muhim shart bilan keladi: bu qoidalar sonar-java ning o'zida emas, alohida symbolic execution pluginida yashaydi. Shuning uchun ular faqat o'sha plugin o'rnatilgan bo'lsa ishlaydi. Ikkisining holati ham bir xil emas: `java:S2095` symbolic execution pluginining `Sonar way` profilida bor, `java:S2259` esa ochiq manbalardagi hech bir `Sonar way` profilida yo'q, ya'ni uni profilda qo'lda yoqish kerak. "Sonar null ni o'zi topadi" degan taxmin shu ikki shartni o'tkazib yuboradi.

Sonar umuman qilmaydigan narsalar esa shu ro'yxat:

- Arxitektura qoidalaringizni bilmaydi. `web` paketidan to'g'ridan to'g'ri `repository` ga murojaat qilish Sonar uchun oddiy kod.
- Domen qoidasini tekshirmaydi. "Pul `BigDecimal` da bo'lsin" degan qoida tayyor emas.
- Bytecode ni ko'rmaydi. Lombok yoki mapper generator yaratgan kodda nima borligini bilmaydi.
- Kompilyatsiya paytida to'xtatmaydi. Siz xato kodni local da erkin kompilyatsiya qilasiz, Sonar faqat scanner ishlaganda gapiradi.
- Formatlashni tuzatmaydi. U ba'zi uslub buzilishini aytadi, lekin faylni o'zi to'g'rilamaydi.
- O'z qoidangizni oson qo'shib bo'lmaydi. Custom qoida uchun Java plugin va alohida release sikli kerak.

Quyidagi jadval butun bobning xaritasi.

| Vosita | Nimani topadi | Qachon ishlaydi | Narxi (vaqt va qo'llab-quvvatlash) |
| --- | --- | --- | --- |
| SonarQube / SonarCloud | Bug, code smell, vulnerability, hotspot, coverage, duplication, tarix | Scanner bosqichida, test va JaCoCo dan keyin | Server yoki obuna, profil boshqarish doimiy ish |
| SpotBugs (+ find-sec-bugs) | Bytecode darajasidagi bug naqshlari, generated kod ichidagi muammo | `compile` dan keyin, class fayllar ustida | Noise ko'p, filter fayli kerak; `effort=max` sezilarli sekinlashtiradi |
| PMD | Kod naqshlari, ortiqcha murakkablik, ishlatilmagan element | Source ustida, istalgan bosqichda | Tez, lekin Sonar bilan kuchli takrorlanadi |
| Checkstyle | Uslub, nomlash, import tartibi, Javadoc | Source ustida, odatda `validate` | Juda tez, formatter bo'lsa ko'p qoidasi keraksiz |
| Error Prone | Kompilyatsiya paytidagi xato naqshlari, tip bilan bog'liq xatolar | Aynan `javac` ichida | Kompilyatsiya sekinlashadi (ulushi loyihaga bog'liq, CI da o'lchab ko'r), flag sozlash kerak |
| NullAway | Null bilan bog'liq xatolar, annotatsiyaga asoslangan | Error Prone ichida | Boshlanishida annotatsiya qo'yish mehnati, keyin arzon |
| ArchUnit | Arxitektura va paket qoidalari | Oddiy test sifatida, test bosqichida | Juda arzon, qoidani o'zingiz yozasiz |
| Semgrep | Loyihaga xos naqsh, ko'p tilli, YAML qoida | Alohida qadam, source ustida | Tez, qoida yozish oson, qoida bazasini saqlash kerak |
| Spotless | Formatlash va litsenziya sarlavhasi | `validate` da check, local da apply | Deyarli bepul, bir martalik katta diff |

## 40.2 SpotBugs: bytecode darajasidagi tahlil va u qachon qo'shimcha qiymat beradi

SpotBugs source ni emas, `.class` fayllarni o'qiydi. Shuning uchun u Sonar ko'rmaydigan qatlamga qaraydi: Lombok yaratgan `equals`, MapStruct yozgan mapper, record ning sintetik metodlari, kompilyator qo'shgan bridge metodlar. Agar loyihada kod generatsiyasi ko'p bo'lsa, SpotBugs haqiqiy qo'shimcha qiymat beradi.

Amalda eng ko'p foyda beradigan detektorlar: `EI_EXPOSE_REP` (ichki massivni tashqariga berish), `RV_RETURN_VALUE_IGNORED`, `DM_DEFAULT_ENCODING` (platforma encoding iga ishonish), `NP_NULL_ON_SOME_PATH`. Bulardan ba'zilari Sonar da ham bor, lekin SpotBugs ularni generated kodda topadi.

Bu yerda bitta sabab tez-tez noto'g'ri aytiladi. Pastdagi misolda Sonar jim qolsa, bu Lombok tufayli emas: Sonar da shu muammo uchun qoida bor, `java:S2384` ("Private mutable members should not be stored or returned directly"), lekin u default `Sonar way` profilida yoqilmagan. Ya'ni sabab generatsiya emas, profil tanlovi. SpotBugs ning haqiqiy qo'shimcha qiymati esa boshqa joyda: u konstruktorda ham, Lombok yozgan getter da ham bir xil ko'radi, chunki ikkisi ham bytecode da turadi.

```java
// Ombor qoldig'i servisi. Sonar bu yerda jim qolishi mumkin, lekin
// sababi `java:S2384` ning Sonar way da yoqilmagani.
@Getter
public class StockSnapshot {
    private final String warehouseCode;
    // Massiv to'g'ridan to'g'ri qaytariladi: chaqiruvchi uni o'zgartira oladi.
    private final int[] quantities;

    public StockSnapshot(String warehouseCode, int[] quantities) {
        this.warehouseCode = warehouseCode;
        this.quantities = quantities; // EI_EXPOSE_REP2
    }
}
```

Tuzatilgan variant nusxa oladi: `this.quantities = quantities.clone()`, getter ham `clone()` qaytaradi. Yanada yaxshisi massiv o'rniga `List.copyOf` ishlatish.

SpotBugs ni Maven ga qo'shish:

```xml
<plugin>
  <groupId>com.github.spotbugs</groupId>
  <artifactId>spotbugs-maven-plugin</artifactId>
  <configuration>
    <!-- Low ni yoqsangiz noise portlaydi, Medium dan boshlang -->
    <threshold>Medium</threshold>
    <effort>Max</effort>
    <xmlOutput>true</xmlOutput>
    <!-- Bilib turib qoldirilgan holatlar shu faylda -->
    <excludeFilterFile>config/spotbugs-exclude.xml</excludeFilterFile>
    <plugins>
      <plugin>
        <groupId>com.h3xstream.findsecbugs</groupId>
        <artifactId>findsecbugs-plugin</artifactId>
        <version>1.13.0</version>
      </plugin>
    </plugins>
  </configuration>
</plugin>
```

Ikki ogohlantirish. Birinchisi: SpotBugs yangi bytecode versiyasini o'qishi uchun o'zi ham yangi bo'lishi kerak. Java 21 dan yuqori maqsadga o'tganda uning versiyasini ko'tarmasangiz tahlil xato bilan to'xtaydi. Ikkinchisi: `excludeFilterFile` ni kod bilan birga review qiling, aks holda u sekin asta hamma narsani o'chiradigan faylga aylanadi.

## 40.3 PMD va Checkstyle: uslub va qoidalar, Sonar bilan takrorlanishi

Sonar ning o'z Java analizatori bu uchlikning ko'p mavzusini qamrab oladi, shuning uchun uchalasini to'liq yoqish eng ko'p takrorlanish beradigan konfiguratsiya. Lekin takrorlanishni tekshirganda ikki narsani ajratish kerak: qoida MAVJUDMI va u DEFAULT PROFILDA yoqilganmi.

| Mavzu | Sonar | Sonar way da | PMD 7 | Checkstyle |
|---|---|---|---|---|
| Ishlatilmagan lokal o'zgaruvchi | `java:S1481` | Ha | `UnusedLocalVariable` | `UnusedLocalVariable` |
| Bo'sh `catch` | `java:S108` | Ha | `EmptyCatchBlock` | - |
| Ichma ich shartni birlashtirish | `java:S1066` | Ha | `CollapsibleIfStatements` | - |
| Metod juda uzun | `java:S138` | **Yo'q** | `NcssCount` | `MethodLength` |
| Shart chuqurligi chegarasi | - | - | - | `NestedIfDepth` |

Jadvaldan ikkita aniq xulosa chiqadi. Birinchi: "metod juda uzun" uchun default sozlamada takrorlanish YO'Q, chunki `java:S138` Sonar way da yoqilmagan; agar bu sizga kerak bo'lsa, uni Sonar profilida yoqish PMD yoki Checkstyle qo'shishdan arzon. Ikkinchi: Checkstyle ning `NestedIfDepth` i chuqurlik chegarasini qo'yadi, Sonar ning `java:S1066` i esa birlashtirish mumkin bo'lgan shartni ko'rsatadi; bu ikkisi ekvivalent emas va ikkisini bir xil deb hisoblash noto'g'ri taqsimotga olib keladi.

Tavsiya: PMD ni yoqmang, uning o'rnini Sonar egallagan. Checkstyle ni faqat Sonar da yo'q yoki Sonar way da yoqilmagan narsa uchun qoldiring, va ro'yxatni taxminga emas, tekshiruvga tayanib tuzing. Masalan package nomining katalogga mosligi Sonar da BOR va u Sonar way da yoqilgan (`java:S1598`), ya'ni buni Checkstyle ga qoldirish ortiqcha takrorlanish. Litsenziya sarlavhasi uchun esa Sonar da qoida bor (`java:S1451`), lekin u Sonar way da yoqilmagan, shuning uchun bu yerda tanlov bor: Sonar profilida yoqish yoki Checkstyle ga qoldirish. Import tartibini esa formatter hal qiladi.

Agar qoldirsangiz, hisobotni Sonar ga import qiling, shunda developer bitta joydan o'qiydi:

```properties
# sonar-project.properties: tashqi analizator hisobotlari
sonar.java.checkstyle.reportPaths=target/checkstyle-result.xml
sonar.java.spotbugs.reportPaths=target/spotbugsXml.xml
# Umumiy format (Semgrep, o'z skriptingiz) shu kalit orqali keladi
sonar.externalIssuesReportPaths=target/semgrep-sonar.json
# Qoidani faqat ayrim fayllarda o'chirish
sonar.issue.ignore.multicriteria=e1,e2
sonar.issue.ignore.multicriteria.e1.ruleKey=java:S3776
sonar.issue.ignore.multicriteria.e1.resourceKey=**/generated/**/*.java
sonar.issue.ignore.multicriteria.e2.ruleKey=java:S1192
sonar.issue.ignore.multicriteria.e2.resourceKey=**/*MigrationTest.java
```

Muhim halol nuqta: import qilingan tashqi issue lar Sonar ichida to'liq boshqarilmaydi. Severity ni o'zgartirish yoki false positive belgilash har doim ishlamaydi, va ularning quality gate shartiga qo'shilishi SonarQube versiyasiga qarab farq qiladi. Buni o'z serveringizda sinov PR bilan tekshirib ko'ring.

## 40.4 Error Prone va NullAway: kompilyatsiya paytida xato topish

Error Prone ning yutug'i joylashuvida: u `javac` ichida ishlaydi va xatoni kompilyatsiya paytida beradi. Ya'ni dasturchi javobni PR ochilishini kutmasdan, o'z kompilyatoridan oladi. Sonar PR da gapirsa, Error Prone kod yozilayotganda gapiradi.

NullAway esa Error Prone ustida ishlaydigan tekshiruv. U `@Nullable` annotatsiyasiga tayanadi va "annotatsiya qilingan paketda hamma narsa non-null" deb qabul qiladi. Sonar ning null tahlili bitta metod ichida kuchli, NullAway esa metodlar orasidagi shartnomani tekshiradi. Ikkisi bir birini almashtirmaydi.

```xml
<plugin>
  <artifactId>maven-compiler-plugin</artifactId>
  <configuration>
    <compilerArgs>
      <arg>-XDcompilePolicy=simple</arg>
      <!-- Flag to'plami Error Prone va JDK versiyasiga qarab farq qiladi -->
      <arg>--should-stop=ifError=FLOW</arg>
      <!-- Har bir flag ALOHIDA <arg> ichida. XML da satr oxiridagi
           `\` oddiy belgi bo'lib qoladi va javac uni alohida token
           deb oladi, keyin Error Prone uni tanimaydi va javac ga
           uzatadi: natijada kompilyatsiya tushunarsiz xato beradi. -->
      <arg>-Xplugin:ErrorProne</arg>
      <arg>-Xep:NullAway:ERROR</arg>
      <arg>-XepOpt:NullAway:AnnotatedPackages=uz.shop.payment</arg>
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
        <version>0.12.1</version>
      </path>
    </annotationProcessorPaths>
  </configuration>
</plugin>
```

JDK 16+ da bu blokning o'zi yetmaydi: Error Prone `jdk.compiler` ning yopiq ichki paketlariga murojaat qiladi va `.mvn/jvm.config` dagi `--add-exports`/`--add-opens` qatorlarisiz build `IllegalAccessError` bilan yiqiladi. Qatorlar ro'yxati, fork rejimidagi `-J` varianti va Error Prone ning JDK talabi [toza kod hujjatidagi kompilyator ogohlantirishlari va Error Prone bo'limida](../clean-code/25-java-kodidagi-umumiy-tuzoqlar.md#2510-kompilyator-ogohlantirishlari--xlint--werror-error-prone-nullaway).

To'lov servisidagi tipik holat: repository `Optional` emas, `null` qaytaradi, chaqiruvchi esa darhol metod chaqiradi. Sonar bunda ba'zan jim qoladi, chunki `null` boshqa klassdan keladi. NullAway uchun bu kompilyatsiya xatosi, chunki `@Nullable` qaytish tipi tekshirilmagan. Tuzatish: `Optional<Payment>` ga o'tish yoki `null` ni tekshirib, domen xatosini tashlash.

Joriy qilish strategiyasi muhim. Hamma tekshiruvni darhol `ERROR` qilsangiz loyiha kompilyatsiya bo'lmaydi. Avval hamma o'chirilgan tekshiruvni ogohlantirish sifatida yoqib ko'ring, keyin eng qimmat besh-o'n tekshiruvni `ERROR` ga ko'taring. Flag nomi ko'pincha xato yoziladi: `AllChecks` degan tekshiruv yo'q, demak `-Xep:AllChecks:WARN` hech narsa qilmaydi. To'g'ri flag boshqa shaklda:

```xml
<arg>-XepAllDisabledChecksAsWarnings</arg>
```

## 40.5 ArchUnit: arxitektura qoidalarini test sifatida yozish

ArchUnit shu bobda bitta sababdan turadi: u Sonar ning eng katta bo'shlig'ini yopadi. Sonar paket bog'liqligi haqidagi sizning qoidangizni bilmaydi, ArchUnit esa uni test sifatida yozib, build ni to'xtatadi. ArchUnit sintaksisi [testlash qo'llanmasidagi](../testing/README.md) ArchUnit mavzusida, bu yerda faqat ikkisining birga ishlashi.

Birinchi masala keng tarqalgan, lekin u aslida masala emas: "Sonar `@ArchTest` maydonlariga assertion yo'q deb shikoyat qiladi" degan gap tekshiruvga dosh bermaydi. `java:S2699` qoidasi faqat METODlarni ko'radi, maydonni emas, shuning uchun `@ArchTest` maydoni uni ishga tushirmaydi. Metod ko'rinishida yozilgan qoida ham shikoyat chiqarmaydi, chunki qoidaning default assertion naqshi `check.*` bilan boshlanadigan chaqiruvni assertion deb hisoblaydi, ya'ni `rule.check(classes)` yetarli. Demak bu yerda `sonar.issue.ignore.multicriteria` yozish shart emas.

Haqiqiy masala boshqa va u ArchUnit tomonida. `@AnalyzeClasses` annotatsiyasini faqat ArchUnit ning o'z JUnit 5 engine i o'qiydi, va u faqat `@ArchTest` maydonlari va metodlari uchun ishlaydi. Agar sinf ustida `@AnalyzeClasses` yozib, ichida oddiy `@Test` metodlar bo'lsa, annotatsiya umuman ta'sir qilmaydi: `importOptions` ham qo'llanmaydi, ya'ni `DoNotIncludeTests` e'tiborsiz qoladi va qoida test klasslariga ham tegib ketishi mumkin. Ikki to'g'ri shakl bor, ularni aralashtirmaslik kerak.

```java
// 1-shakl: ArchUnit engine i. @AnalyzeClasses sinflarni o'zi import
// qiladi va importOptions aynan shu yerda ishlaydi.
@AnalyzeClasses(packages = "uz.shop",
                importOptions = ImportOption.DoNotIncludeTests.class)
class ArchitectureRulesTest {

    // Web qatlami faqat application qatlami orqali ishlaydi
    @ArchTest
    static final ArchRule webRepositoryGaTegmasin =
        noClasses().that().resideInAPackage("..web..")
            .should().dependOnClassesThat().resideInAPackage("..repository..");

    // Domen qoidasi: Sonar da bunday qoida yo'q
    @ArchTest
    static final ArchRule pulDoubleDaSaqlanmasin =
        noFields().that().haveNameMatching(".*[Aa]mount.*")
            .should().haveRawType(Double.class);
}
```

```java
// 2-shakl: oddiy JUnit. @AnalyzeClasses YO'Q, chunki u ishlamaydi;
// import opsiyasi importer ga qo'lda beriladi.
class ArchitectureRulesManualTest {

    private static final JavaClasses CLASSES = new ClassFileImporter()
        .withImportOption(ImportOption.DoNotIncludeTests.INSTANCE)
        .importPackages("uz.shop");

    @Test
    void webRepositoryGaTegmasin() {
        noClasses().that().resideInAPackage("..web..")
            .should().dependOnClassesThat().resideInAPackage("..repository..")
            .check(CLASSES);
    }
}
```

Ikkinchi masala: takrorlanish. ArchUnit bilan "`System.out` ishlatilmasin" degan qoidani yozish mumkin, lekin bu Sonar da allaqachon bor. Ikki joyda bir xil qoida bo'lsa, bittasi eskiradi va ikkisi bir biriga zid gapiradi. Taqsimot aniq bo'lsin: paket bog'liqligi, qatlam, nomlash va annotatsiya mavjudligi ArchUnit da; kod ichidagi mantiq va xavfsizlik Sonar da.

Uchinchi masala: coverage. Bu yerda ham gap aniqlashtirishni talab qiladi. ArchUnit importer klass fayllarni bytecode sifatida o'qiydi va klasslarni YUKLAMAYDI, ya'ni production kod ishga tushmaydi va JaCoCo uni bajarilgan deb hisoblamaydi. Demak ArchUnit testi coverage raqamini o'z-o'zidan ko'tarmaydi. Haqiqiy xavf boshqa shaklda: ArchUnit testi qo'shilganda "test yozdik" degan taassurot paydo bo'ladi, test soni va build vaqti o'sadi, biznes mantiq esa qoplanmagan qoladi. Shuning uchun coverage pastligini arxitektura testi bilan yopishga urinish o'lchov emas, o'zini chalg'itish.

Mavzuning to'liq yozuvi testlash qo'llanmasidagi [arxitektura testlari va kod sifati darvozalari](../testing/14-arxitektura-testlari-va-kod-sifati.md#142-archunit-asoslari) bo'limida; bu yerda faqat Sonar qoidasi nuqtai nazari.

## 40.6 Semgrep va shunga o'xshash qoida yozish vositalari

Semgrep ning qiymati bitta: o'z qoidangizni Java plugin yozmasdan, YAML da besh daqiqada yozasiz. Sonar da custom qoida uchun plugin loyihasi, versiyalash va deploy kerak. Semgrep da qoida repository dagi fayl bo'ladi va PR da review qilinadi.

```yaml
rules:
  - id: hisobot-service-da-native-query
    languages: [java]
    severity: WARNING
    message: >
      Hisobot servisida native query ishlatilgan. Buyruq va o'qish
      qatlamini aralashtirmang, read-model repository ga ko'chiring.
    patterns:
      - pattern: |
          @Query(value = "...", nativeQuery = true)
          $RET $METHOD(...);
      - pattern-inside: |
          interface $REPO { ... }
    paths:
      include:
        - "**/report/**"
  - id: tolov-logida-karta-raqami
    languages: [java]
    severity: ERROR
    message: "Karta raqamini log ga yozish taqiqlangan."
    pattern-either:
      - pattern: $LOG.info(..., $X.getCardNumber(), ...)
      - pattern: $LOG.debug(..., $X.getCardNumber(), ...)
```

Semgrep ni Sonar ning o'rniga qo'ymang. Uning data flow tahlili kuchsizroq va u tarix saqlamaydi. To'g'ri ishlatish: loyihaga xos uchta-o'nta qoida, natijani Sonar ga generic issue formatida import qilish. Shunga o'xshash vositalar: `jqassistant` (grafda so'rov) va OpenRewrite recipe lari, oxirgisi topish bilan birga tuzatib ham beradi.

## 40.7 Formatlash vositalari (Spotless kabi) va ularni bahsdan chiqarish

Formatlash haqidagi bahs eng arzon va eng ko'p vaqt yeydigan bahs. Uni kelishuv bilan emas, avtomatika bilan yo'q qilish kerak. Spotless google-java-format yoki palantir-java-format ni qo'llaydi, `apply` bilan tuzatadi, `check` bilan build ni to'xtatadi.

```bash
# Local da bir marta hammasini formatlash
./mvnw spotless:apply

# CI da faqat tekshirish, tuzatmaslik
./mvnw -q spotless:check

# Katta loyihada hamma faylni emas, faqat yangi o'zgarishni formatlash.
# DIQQAT: `ratchetFrom` buyruq qatorida ishlamaydi, plugin uni Maven
# property sifatida ochmagan. `-Dspotless.ratchetFrom=...` jimgina
# e'tiborsiz qoladi: xato ham chiqmaydi, ta'sir ham qilmaydi.
# U faqat pom.xml ichida beriladi:
#   <configuration><ratchetFrom>origin/main</ratchetFrom></configuration>
./mvnw spotless:apply

# Pre-commit hook: kommitdan oldin formatlash
printf '%s\n' '#!/bin/sh' './mvnw -q spotless:apply' > .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

Formatter yoqilgandan keyin Sonar profilidan va Checkstyle dan uslub qoidalarini o'chiring. Qavs joyi, qator uzunligi va import tartibi haqidagi qoidalar endi keraksiz, chunki kod formatter chiqargan ko'rinishda. Birinchi `apply` bitta katta commit beradi, uni `git blame` uchun `.git-blame-ignore-revs` fayliga qo'shing.

## 40.8 Vositalarni birlashtirish: qaysi biri bloklaydi, qaysi biri ogohlantiradi

Eng ko'p uchraydigan xato: hamma vosita build ni to'xtatadi. Natijada developer formatlash xatosi, uslub xatosi va haqiqiy bug ni bir xil qizil rang sifatida ko'radi, va uchalasiga bir xil e'tibor beradi, ya'ni e'tibor bermaydi.

Qoida oddiy: tez, aniq va o'z o'zidan tuzatiladigan narsa bloklaydi. Sekin, taxminga asoslangan va muhokama talab qiladigan narsa ogohlantiradi. Bloklaydi: Spotless check, kompilyatsiya xatolari va Error Prone ning `ERROR` darajasi, ArchUnit testlari, Sonar quality gate ning new code shartlari. Ogohlantiradi: SpotBugs ning `Medium` topilmalari, Semgrep ning `WARNING` qoidalari, eski koddagi issue lar, coverage ning umumiy raqami.

```yaml
name: ci
on: [pull_request]
jobs:
  fast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }   # Sonar new code uchun to'liq tarix kerak
      - uses: actions/setup-java@v4
        with: { java-version: '21', distribution: 'temurin', cache: 'maven' }
      # 1-qadam: eng tez va eng aniq tekshiruv, darhol to'xtatadi
      - run: ./mvnw -q spotless:check
      # 2-qadam: kompilyatsiya + Error Prone + NullAway
      - run: ./mvnw -q -DskipTests compile
      # 3-qadam: testlar, ArchUnit ham shu yerda, JaCoCo hisoboti bilan
      - run: ./mvnw -q verify
      # 4-qadam: bloklamaydigan tahlil
      - run: ./mvnw -q spotbugs:spotbugs || echo "SpotBugs: ogohlantirish"
      # 5-qadam: Sonar, test va coverage dan keyin
      - run: ./mvnw -q sonar:sonar -Dsonar.qualitygate.wait=true
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

## 40.9 Takroriy ogohlantirishlarni kamaytirish: qoidalarni bo'lish

Yagona ishonchli usul bor: har bir qoida turi uchun bitta egani tanlash va qolganlarida o'chirish. Buni yozib qo'yish kerak, aks holda har yangi developer yana bitta vosita qo'shadi.

Ishlaydigan taqsimot shunday. Formatlash: Spotless. Uslub va nomlash: Checkstyle, faqat Spotless qamramaydigan qism. Null shartnomasi: NullAway. Bytecode va generated kod: SpotBugs. Arxitektura: ArchUnit. Loyihaga xos naqsh: Semgrep. Qolgan hammasi, ya'ni kod mantiqi, xavfsizlik, murakkablik, duplication va coverage: Sonar.

Takrorlanishni o'lchash mumkin. Bitta PR da hamma vositani yoqib, topilmalarni fayl va qator bo'yicha taqqoslang. Bir xil qator ikki vositada chiqsa, bittasi o'chirishga nomzod.

| Tuzoq | Nima bo'ladi | Yechim |
| --- | --- | --- |
| Sonar, PMD va Checkstyle to'liq yoqilgan | Bir xil issue uch marta, developer uchalasiga ishonmaydi | PMD ni o'chirish, Checkstyle ni uchta modulga qisqartirish |
| SpotBugs `Low` threshold | Minglab topilma, hech kim ko'rmaydi | `Medium` dan boshlash, exclude faylini review qilish |
| Hamma vosita build ni to'xtatadi | Formatlash xatosi bug bilan bir darajada | Bloklash huquqini faqat tez va aniq tekshiruvga berish |
| Error Prone darhol `ERROR` | Loyiha kompilyatsiya bo'lmaydi, rollback | Avval `WARN`, keyin tanlab `ERROR` ga ko'tarish |
| ArchUnit qoidasi Sonar qoidasini takrorlaydi | Ikki joy bir biriga zid gapiradi | Qoida egasini aniq taqsimlash va hujjatlashtirish |
| `@AnalyzeClasses` oddiy `@Test` metodlari bilan yozilgan | Annotatsiya ta'sirsiz, `importOptions` qo'llanmaydi | `@ArchTest` ga o'tish yoki importer opsiyasini qo'lda berish |
| Tashqi hisobot Sonar ga import qilingan, lekin gate ga qo'shilmagan | Topilma ko'rinadi, hech narsani to'xtatmaydi | Sinov PR bilan tekshirish, kerak bo'lsa alohida CI qadami bilan bloklash |
| SpotBugs eski versiya, yangi bytecode | Tahlil xato bilan to'xtaydi, CI qizil | Java versiyasi ko'tarilganda SpotBugs ni ham ko'tarish |

## 40.10 Pipeline da tartib va umumiy vaqt byudjeti

Prinsip: eng arzon va eng ko'p xato topadigan tekshiruv birinchi bo'ladi. Spotless bir soniyada ishlaydi va diff ni darhol ko'rsatadi, uni oxirida qo'yish ma'nosiz.

Vaqt byudjetini oldindan belgilang. Masalan PR pipeline uchun 12 daqiqa: formatlash va kompilyatsiya 2 daqiqa, unit test va ArchUnit 3 daqiqa, integratsion test 4 daqiqa, Sonar scanner 2 daqiqa, zahira 1 daqiqa. SpotBugs va Semgrep shu byudjetga sig'masa, ularni kechki `nightly` build ga ko'chiring.

Sonar har doim test va JaCoCo dan keyin ishlashi kerak, aks holda coverage nol bo'lib keladi va quality gate yolg'on sababdan buziladi. Bu eng ko'p uchraydigan konfiguratsiya xatosi.

```sql
-- CI metrikasi uchun oddiy jadval: har bir qadam qancha vaqt oldi
-- Vaqt byudjetini his bilan emas, raqam bilan boshqarish uchun
SELECT step_name,
       count(*)                                  AS yurishlar,
       round(avg(duration_seconds))              AS ortacha_sek,
       round(percentile_cont(0.95)
             WITHIN GROUP (ORDER BY duration_seconds)) AS p95_sek,
       sum(CASE WHEN status = 'FAILED' THEN 1 ELSE 0 END) AS xatolar
FROM ci_step_run
WHERE started_at > now() - interval '30 days'
  AND branch_kind = 'pull_request'
GROUP BY step_name
ORDER BY p95_sek DESC;
```

Natija odatda bitta narsani ko'rsatadi: vaqtning yarmini bitta qadam yeydi. Ko'pincha bu integratsion testlar, ba'zan SpotBugs ning `effort=Max` sozlamasi. Qisqartirish shu qadamdan boshlanadi.

## 40.11 Kam vosita bilan ko'p foyda: minimal to'plam tavsiyasi

Nol dan boshlasangiz, to'rtta vosita yetarli: Spotless, Sonar, ArchUnit, va Error Prone bilan NullAway. Bu to'plam formatlash bahsini o'ldiradi, kod mantiqi va xavfsizlikni qoplaydi, arxitekturani qulflaydi, va null xatolarini kompilyatsiya paytida tutadi.

SpotBugs ni faqat kod generatsiyasi ko'p bo'lsa qo'shing. Semgrep ni Sonar da yo'q, aniq nomlangan qoidaga ehtiyoj paydo bo'lganda qo'shing. PMD ni qo'shmang. Checkstyle ni Spotless qamramaydigan uch-to'rt qoida uchun qoldiring yoki undan ham voz keching.

| Savol | Oddiy yondashuv | Arxitektor yondashuvi |
| --- | --- | --- |
| Qancha vosita yoqamiz | Topilgan hamma vositani yoqamiz | Har bir bo'shliq uchun bittasi, takrorlanish nolga yaqin |
| Kim bloklaydi | Hammasi bloklaydi | Tez va aniq tekshiruv bloklaydi, taxminiy narsa ogohlantiradi |
| Takroriy issue | "Ikki joydan ko'rish yaxshi" | Qoida egasini belgilab, boshqasida o'chiramiz |
| Formatlash | Code review da muhokama qilamiz | Spotless `apply`, review da gapirmaymiz |
| Arxitektura qoidasi | Hujjatga yozamiz va eslatamiz | ArchUnit testi, build ni to'xtatadi |
| O'z qoidamiz kerak | Sonar plugin yozamiz | Semgrep YAML, repository da review qilinadi |
| Null xatolari | Sonar PR da aytadi | NullAway kompilyatsiyada aytadi, Sonar zahira bo'ladi |
| Pipeline vaqti | O'sib ketsa chidaymiz | Oldindan byudjet, p95 ni o'lchab qisqartiramiz |
| Yangi vosita qo'shish | Qiziq ko'rinsa qo'shamiz | Qaysi bo'shliqni yopadi, qaysi vositani o'chiramiz, deb so'raymiz |
| Noise ko'paysa | Hamma narsani exclude qilamiz | Qoida profilini qisqartiramiz, exclude ni review qilamiz |

Eslatma, bu to'plam ham sifatni kafolatlamaydi. Vositalar faqat ma'lum naqshlarni topadi. Noto'g'ri domen mantiqi, yomon ma'lumot modeli va kerakmas murakkablik hech bir statik tahlilda ko'rinmaydi. Ular review va dizayn ishi bilan topiladi.

## 40.12 Amalda qo'llash

- [ ] Loyihadagi hamma statik tahlil vositasi uchun "qaysi bo'shliqni yopadi" degan bitta gap yozing. Javobi bo'lmagan vositani o'chiring.
- [ ] Bitta sinov PR da hamma vositani yoqib, topilmalarni fayl va qator bo'yicha taqqoslang, ikki joyda chiqqan qoidalarning bittasini o'chiring.
- [ ] Spotless ni qo'shib, `spotless:apply` ni alohida commit qiling va uni `.git-blame-ignore-revs` ga yozing. Keyin Sonar profilidan uslub qoidalarini olib tashlang.
- [ ] Error Prone ni `-XepAllDisabledChecksAsWarnings` bilan yoqing, eng ko'p takrorlangan beshta ogohlantirishni tuzatib, ularni `ERROR` ga ko'taring.
- [ ] NullAway ni bitta modulda, masalan to'lov modulida yoqing. `AnnotatedPackages` ni faqat shu paketga bering va kompilyatsiya tozalanmaguncha kengaytirmang.
- [ ] ArchUnit testlariga Sonar shikoyat qilayotganini tekshiring. Kerak bo'lsa `sonar.issue.ignore.multicriteria` bilan shu fayllarda qoidani o'chiring.
- [ ] CI qadamlari vaqtini o'lchaydigan dashboard tuzing va PR pipeline uchun aniq daqiqa byudjetini yozib qo'ying. Byudjetdan chiqqan qadamni `nightly` ga ko'chiring.
- [ ] Qaysi vosita bloklaydi va qaysi biri ogohlantiradi degan qarorni repository dagi bitta faylga yozing, yangi vosita qo'shishda shu faylni yangilash shart bo'lsin.

## Manbalar

- SonarSource, `sonar-java` ning qoida metadatasi va `Sonar way` profili
  ([https://github.com/SonarSource/sonar-java/tree/8.44.0.48651/sonar-java-plugin/src/main/resources/profiles/Sonar_way](https://github.com/SonarSource/sonar-java/tree/8.44.0.48651/sonar-java-plugin/src/main/resources/profiles/Sonar_way),
  tag `8.44.0.48651`, SONAR Source-Available License v1.0) - 40.2 dagi
  `java:S2384` ning profilda yo'qligi va 40.3 dagi `java:S138`,
  `java:S1598`, `java:S1451` ning holati.
- SonarSource, `AssertionsInTestsCheck` va `UnitTestUtils`
  ([https://github.com/SonarSource/sonar-java/blob/8.44.0.48651/java-checks/src/main/java/org/sonar/java/checks/tests/AssertionsInTestsCheck.java](https://github.com/SonarSource/sonar-java/blob/8.44.0.48651/java-checks/src/main/java/org/sonar/java/checks/tests/AssertionsInTestsCheck.java),
  tag `8.44.0.48651`) - 40.5 dagi `java:S2699` faqat metodlarni ko'rishi
  va `check.*` ni assertion deb hisoblashi.
- SonarSource, `sonar-java-symbolic-execution`
  ([https://github.com/SonarSource/sonar-java-symbolic-execution/tree/4450911/java-symbolic-execution/java-symbolic-execution-plugin/src/main/java/org/sonar/java/se/checks](https://github.com/SonarSource/sonar-java-symbolic-execution/tree/4450911/java-symbolic-execution/java-symbolic-execution-plugin/src/main/java/org/sonar/java/se/checks),
  commit `4450911`, SONAR Source-Available License v1.0) - 40.1 dagi
  `java:S2259` va `java:S2095` ning alohida pluginda turishi.
- Error Prone, `ErrorProneOptions`
  ([https://github.com/google/error-prone/blob/v2.36.0/check_api/src/main/java/com/google/errorprone/ErrorProneOptions.java](https://github.com/google/error-prone/blob/v2.36.0/check_api/src/main/java/com/google/errorprone/ErrorProneOptions.java),
  tag `v2.36.0`, Apache-2.0) - 40.4 dagi
  `-XepAllDisabledChecksAsWarnings` flagi va tanilmagan tokenning
  javac ga uzatilishi.
- ArchUnit, `ArchUnitTestEngine` va `Locations`
  ([https://github.com/TNG/ArchUnit/blob/v1.4.1/archunit-junit/junit5/engine/src/main/java/com/tngtech/archunit/junit/internal/ArchUnitTestEngine.java](https://github.com/TNG/ArchUnit/blob/v1.4.1/archunit-junit/junit5/engine/src/main/java/com/tngtech/archunit/junit/internal/ArchUnitTestEngine.java),
  tag `v1.4.1`, Apache-2.0) - 40.5 dagi `@AnalyzeClasses` ning faqat
  `@ArchTest` bilan ishlashi va importer ning klasslarni yuklamasligi.
- Spotless Maven plugini, `AbstractSpotlessMojo`
  ([https://github.com/diffplug/spotless/blob/plugin-maven/2.30.0/plugin-maven/src/main/java/com/diffplug/spotless/maven/AbstractSpotlessMojo.java](https://github.com/diffplug/spotless/blob/plugin-maven/2.30.0/plugin-maven/src/main/java/com/diffplug/spotless/maven/AbstractSpotlessMojo.java),
  tag `plugin-maven/2.30.0`, Apache-2.0) - 40.7 dagi `ratchetFrom`
  parametrining Maven property sifatida ochilmagani.
- PMD, Java qoida to'plamlari
  ([https://github.com/pmd/pmd/tree/pmd_releases/7.28.0/pmd-java/src/main/resources/category/java](https://github.com/pmd/pmd/tree/pmd_releases/7.28.0/pmd-java/src/main/resources/category/java),
  tag `pmd_releases/7.28.0`, BSD-style) - 40.3 dagi `NcssCount`,
  `UnusedLocalVariable`, `EmptyCatchBlock`, `CollapsibleIfStatements`.
- Checkstyle, tekshiruv sinflari
  ([https://github.com/checkstyle/checkstyle/tree/checkstyle-14.3.0/src/main/java/com/puppycrawl/tools/checkstyle/checks](https://github.com/checkstyle/checkstyle/tree/checkstyle-14.3.0/src/main/java/com/puppycrawl/tools/checkstyle/checks),
  tag `checkstyle-14.3.0`, LGPL-2.1) - 40.3 dagi `MethodLength`,
  `UnusedLocalVariable`, `NestedIfDepth` va `PackageDeclaration`.
- SpotBugs, `messages.xml` va Maven plugini
  ([https://github.com/spotbugs/spotbugs/blob/4.10.5/spotbugs/etc/messages.xml](https://github.com/spotbugs/spotbugs/blob/4.10.5/spotbugs/etc/messages.xml),
  tag `4.10.5`, LGPL-2.1) - 40.2 dagi `EI_EXPOSE_REP`,
  `RV_RETURN_VALUE_IGNORED`, `DM_DEFAULT_ENCODING`,
  `NP_NULL_ON_SOME_PATH` detektorlari.

---

[&larr; 39. Bog'liqlik zaifliklari va litsenziya tekshiruvi](39-bogliqlik-zaifliklari-va-litsenziya.md) · [Mundarija](README.md) · [41. Lombok, record va generatsiya qilingan kod &rarr;](41-lombok-record-va-generatsiya-qilingan-kod.md)
