<!-- doc: sonarqube | chapter: 1 | part: I. SonarQube qanday ishlaydi -->

[Barcha hujjatlar](../../README.md) / [SonarQube](README.md)

# 1. SonarQube arxitekturasi va tahlil oqimi (Architecture and Analysis Flow)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

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

</details>



SonarQube ni "kodni tekshiradigan dastur" deb bilish yetarli emas. U bir nechta alohida jarayondan iborat tizim va ularning har biri boshqa joyda, boshqa vaqtda ishlaydi. Quality gate nega qizil bo'lganini yoki nega tahlil sekin ketganini tushunish uchun avval shu qismlar va ular orasidagi ma'lumot oqimini bilish kerak. Bu bob aynan shu mexanikani ochadi, keyingi boblardagi qoida va shartlar shu asosga tayanadi.

## 1.1 SonarQube qismlari: server, web interfeys, compute engine, ma'lumotlar bazasi, scanner

SonarQube Server bitta jarayon emas, balki bir nechta sub-jarayonni boshqaradigan konteyner. Birinchisi web server: REST API va brauzerdagi interfeysni beradi, autentifikatsiya va avtorizatsiya shu yerda hal bo'ladi. Ikkinchisi compute engine, qisqacha CE: scanner yuborgan hisobotni qabul qilib, uni haqiqiy natijaga aylantiradi. Uchinchisi search server, ya'ni ichki Elasticsearch: issue va komponentlar bo'yicha tez qidiruv va filtrlash uchun indeks saqlaydi.

Ma'lumotlar bazasi barcha doimiy ma'lumotni ushlab turadi: loyihalar, tahlil tarixi, metrika qiymatlari, issue lar, quality profile va quality gate sozlamalari. Production uchun PostgreSQL odatiy tanlov, Oracle va SQL Server ham qo'llanadi, ichki H2 esa faqat sinov uchun. Elasticsearch indeksi ikkilamchi: u bazadan qayta tiklanadi, shuning uchun backup strategiyasi bazaga va sozlama fayllariga qaratiladi.

Scanner esa serverda emas, sizning build muhitida ishlaydi. Java loyihada bu `sonar-maven-plugin` yoki Gradle `sonarqube` plugini, boshqa hollarda SonarScanner CLI. Scanner kodni o'qiydi, qoidalarni bajaradi va natijani hisobot sifatida serverga yuboradi. Ya'ni kodingiz serverga ko'tarilmaydi, ko'tariladigan narsa hisobot va unda keltirilgan kod parchalari.

## 1.2 SonarQube Server, SonarQube Cloud va IDE kengaytmasi o'rtasidagi farq

Uchta mahsulot bir xil qoida bazasiga tayanadi, lekin qaerda ishlashi va kimga javob berishi bilan farq qiladi. SonarQube Server o'zingiz joylashtirgan instansiya: versiyani, quality profile ni va saqlanish muddatini siz boshqarasiz. SonarQube Cloud (avvalgi nomi SonarCloud) xuddi shu modelning SaaS varianti: server va baza haqida qayg'urmaysiz, lekin versiya va ba'zi sozlamalar provayder qo'lida bo'ladi. Nomlar 2024 yildan beri o'zgargan, shuning uchun eski hujjatlarda SonarCloud va SonarLint atamalarini uchratasiz.

IDE kengaytmasi (avvalgi nomi SonarLint, hozir SonarQube for IDE) uchinchi turdagi vosita: u developer mashinasida, saqlash paytida ishlaydi va darhol ogohlantiradi. Muhim nuqta shu: kengaytma o'zi hech qanday natijani serverga yozmaydi va quality gate ga ta'sir qilmaydi. U faqat mahalliy fayllarni ko'radi, shuning uchun loyiha bo'yicha duplikatsiya yoki coverage kabi global metrikalarni hisoblay olmaydi.

Shu sababli kengaytmani serverga ulash (connected mode) amalda juda ko'p vaqtni tejaydi. Ulangan holatda kengaytma loyihaning quality profile ini va o'chirilgan qoidalarni serverdan oladi. Natijada IDE da ko'rgan ogohlantirish CI dagi natijaga mos keladi va "menda toza edi" vaziyati kamayadi.

## 1.3 Tahlilning to'liq yo'li: scanner dan compute engine gacha

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

## 1.4 Scanner kodni qanday o'qiydi: sintaksis daraxti, semantik model, bytecode

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

## 1.5 Nega kompilyatsiya qilingan klasslar kerak

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

## 1.6 Natija qayerda saqlanadi va loyiha tarixi qanday to'planadi

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

## 1.7 Branch va pull request tahlili

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

## 1.8 Tahlil davomiyligi va uni qisqartirish

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

## 1.9 Server versiyalari: LTA liniyasi va yangilanish siyosati

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

## 1.10 Kechikish sabablari: tahlil tugadi, natija hali yo'q

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

## 1.11 Amalda qo'llash

- [ ] CI log ida scanner ogohlantirishlarini o'qib chiqing va "binaries not found" turidagi xabar yo'qligiga ishonch hosil qiling.
- [ ] Tahlil qadamini `verify` dan keyinga ko'chiring, JaCoCo XML hisoboti haqiqatan yasalayotganini fayl mavjudligi bilan tekshiring.
- [ ] `sonar.qualitygate.wait=true` ni qo'shing va timeout ni o'zingizning o'rtacha CE vaqtidan ikki baravar katta qo'ying.
- [ ] Loyihaning new code ta'rifini ko'rib chiqing, trunk based ishlasa referens branch variantiga o'tkazing.
- [ ] CI checkout da to'liq git tarixi olinishini ta'minlang, aks holda new code metrikalariga ishonmang.
- [ ] Generatsiya qilingan kodni `sonar.exclusions` ga kiriting va bu o'zgarish coverage raqamiga qanday ta'sir qilganini yozib qo'ying.
- [ ] Jamoadagi IDE kengaytmalarini serverga connected mode da ulang, shunda mahalliy va CI natijalari mos keladi.
- [ ] Server versiyangiz LTA liniyasida ekanini tasdiqlang va yangilashni release oynasidan ajratib rejalashtiring.

---

[Mundarija](README.md) · [2. Scanner nimani yig'adi va qanday yuboradi &rarr;](02-scanner-nimani-yigadi-va-qanday-yuboradi.md)
