<!-- doc: sonarqube | chapter: 20 | part: V. Sonar o'tadigan test -->

[Barcha hujjatlar](../../README.md) / [SonarQube](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 20. Mutation testing: 100% coverage qachon yolg'on (Mutation Testing)

<details>
<summary>Bu bobdagi 12 bo'lim</summary>

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

</details>



Coverage raqami kodning bajarilganini o'lchaydi, tekshirilganini emas. JaCoCo
qatorga bayroq qo'yadi: bu qator test paytida ishga tushdi. Lekin natija to'g'rimi
yoki yo'qmi, JaCoCo buni bilmaydi. Mutation testing shu bo'shliqni yopadi: kodni
ataylab buzadi va testlar buzilganni sezadimi deb so'raydi.

## 20.1 100% coverage bilan hech narsani tekshirmaydigan test to'plami misoli

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

## 20.2 Mutation testing g'oyasi: kodga kichik o'zgarish kiritib, test sezadimi deb tekshirish

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

## 20.3 Mutant turlari: shart chegarasi, qaytish qiymati, matematik amal, chaqiruvni olib tashlash

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

## 20.4 O'ldirilgan va omon qolgan mutant, mutation score ma'nosi

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

## 20.5 PIT (pitest) ni Maven va Gradle da ishga tushirish

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

## 20.6 Hisobotni o'qish: qaysi mutant omon qolgan va bu nimani bildiradi

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

## 20.7 Omon qolgan mutantni test bilan yopish amaliyoti

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

## 20.8 Mutation testing narxi: vaqt va uni qisqartirish usullari

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

## 20.9 Qaysi modulga mutation testing qo'llash mantiqiy

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

## 20.10 Mutation score ni quality gate ga qo'shish masalasi

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

## 20.11 Coverage va mutation score ni birga o'qish

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
[testlash qo'llanmasidagi](../testing/README.md) unit test va test ma'lumotlari mavzularida.

## 20.12 Amalda qo'llash

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

---

[&larr; 19. Testning o'zidagi Sonar qoidalari va test sifati](19-testning-ozidagi-sonar-qoidalari-va-test.md) · [Mundarija](README.md) · [21. CI/CD ga ulash, PR decoration va blokirovka &rarr;](21-ci-cd-ga-ulash-pr-decoration-va-blokirovka.md)
