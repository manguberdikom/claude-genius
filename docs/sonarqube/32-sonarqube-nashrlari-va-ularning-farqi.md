<!-- doc: sonarqube | chapter: 32 | part: VIII. Server va tashkilot -->

[Barcha hujjatlar](../../README.md) / [SonarQube](README.md)

> Holat: tekshirilmoqda. Da'volar hali manbaga solishtirilmoqda.

# 32. SonarQube nashrlari va ularning farqi (Editions)

<details>
<summary>Bu bobdagi 12 bo'lim</summary>

- [32.1 Nashrlar qatori: Community, Developer, Enterprise va Data Center yo'nalishi](#321-nashrlar-qatori-community-developer-enterprise-va-data-center-yonalishi)
- [32.2 Community nashrda nima bor va nima yo'q](#322-community-nashrda-nima-bor-va-nima-yoq)
- [32.3 Branch tahlili va pull request decoration qaysi nashrdan boshlab mavjud](#323-branch-tahlili-va-pull-request-decoration-qaysi-nashrdan-boshlab-mavjud)
- [32.4 Taint analysis (chuqur xavfsizlik tahlili) qaysi nashrda ishlaydi](#324-taint-analysis-chuqur-xavfsizlik-tahlili-qaysi-nashrda-ishlaydi)
- [32.5 Portfolio, umumiy hisobot va ko'p loyihali ko'rinish](#325-portfolio-umumiy-hisobot-va-kop-loyihali-korinish)
- [32.6 Qo'llab-quvvatlanadigan tillar soni nashrga qanday bog'liq](#326-qollab-quvvatlanadigan-tillar-soni-nashrga-qanday-bogliq)
- [32.7 SonarQube Cloud va o'zingizda joylashtirilgan server tanlovi](#327-sonarqube-cloud-va-ozingizda-joylashtirilgan-server-tanlovi)
- [32.8 Litsenziya qanday hisoblanadi va xarajat nimaga bog'liq](#328-litsenziya-qanday-hisoblanadi-va-xarajat-nimaga-bogliq)
- [32.9 Community nashrda chegaralarni qanday chetlab o'tish mumkin va buning narxi](#329-community-nashrda-chegaralarni-qanday-chetlab-otish-mumkin-va-buning-narxi)
- [32.10 Qaysi jamoaga qaysi nashr mos keladi: hajm va ehtiyojga qarab tavsiya](#3210-qaysi-jamoaga-qaysi-nashr-mos-keladi-hajm-va-ehtiyojga-qarab-tavsiya)
- [32.11 Nashrni tanlashdan oldin beriladigan savollar](#3211-nashrni-tanlashdan-oldin-beriladigan-savollar)
- [32.12 Amalda qo'llash](#3212-amalda-qollash)

</details>



SonarQube bitta mahsulot emas, balki bir nechta nashrdan iborat qator. Siz CI da ko'rgan xatti-harakat ko'p hollarda kod sifatiga emas, balki qaysi nashr litsenziyasi o'rnatilganiga bog'liq bo'ladi. Shu sababli "nega mening PR da Sonar hech narsa yozmadi" yoki "nega taint analysis topilmadi" degan savollarning javobi texnik emas, tijoriy bo'lishi mumkin. Bu bobda nashrlar farqi, ularning amaliy natijasi va tanlash mantiqini ko'rib chiqamiz, lekin nomlar va narx siyosati vaqt o'tishi bilan o'zgarganini doim yodda tutamiz.

## 32.1 Nashrlar qatori: Community, Developer, Enterprise va Data Center yo'nalishi

Nashrlar ro'yxati mahsulotning o'z kodida qattiq yozilgan: `EditionProvider.Edition` enum i to'rt qiymatdan iborat - `COMMUNITY` ("Community"), `DEVELOPER` ("Developer"), `ENTERPRISE` ("Enterprise") va `DATACENTER` ("Data Center"). Community bepul va ochiq manbali nashr: SonarQube ning ochiq repozitoriysi aynan shu nashrning kodini saqlaydi va LGPL v3 ostida tarqatiladi, qolgan uchtasi esa tijoriy litsenziya bilan beriladi.

Nashrlar orasidagi imkoniyat taqsimotini esa kod to'liq ko'rsatmaydi: ochiq kodda faqat Community da NIMA YO'Q ekani ko'rinadi, u yoki bu imkoniyat qaysi pullik bosqichdan boshlanishini sotuvchining joriy matritsasi belgilaydi. Shu sababli bu bobda Community chegaralari kodga tayangan holda, pullik bosqichlar farqi esa tasdiqlashni talab qiladigan ma'lumot sifatida beriladi.

Nomlar bilan ehtiyot bo'lish kerak. Ochiq nashrning hozirgi rasmiy nomi "SonarQube Community Build": repozitoriyning o'z README fayli shu nomni ishlatadi. Avvalroq "SonarQube" va "SonarCloud" atamalari yurgan, bugun esa "SonarQube Server" va "SonarQube Cloud" ishlatiladi.

Versiya raqamlari ham ikki qatorga bo'lingan va buni Docker image teglarida ko'rish mumkin: Community Build teglari `26.10.0.133078-community` shaklida (ya'ni 26.x qatori), pullik nashrlar esa `2026.5.2-developer`, `2026.5.2-enterprise`, `2026.5.2-datacenter-app` shaklida (2026.x qatori). Uzoq muddat qo'llab-quvvatlanadigan qator LTA (Long-Term Active) deb ataladi va uning teglari `2026.5-lta-developer` kabi yoziladi. "LTS" eski atama, yangi teglarda u uchramaydi.

## 32.2 Community nashrda nima bor va nima yo'q

Community nashrda tahlil yadrosi to'liq ishlaydi. Siz quality profile sozlaysiz, quality gate yaratasiz, issue va code smell ko'rasiz, coverage hisobotini yuklaysiz va Web API orqali hammasini avtomatlashtirasiz.

Yo'q narsalar esa aniq. Ularning bir qismi to'g'ridan-to'g'ri kodda ko'rinadi:

- branch va pull request tahlili yo'q: tahlil metama'lumotida branch yoki PR berilsa, kod `Branches and Pull Requests are not supported in Community Edition` deb to'xtatadi (`AnalysisMetadataHolderImpl`), Web API parametrlari esa "Branch key. Not available in the community edition" izohi bilan belgilangan;
- moslashtirilgan dashboard yo'q: "Community Edition does not support custom dashboards" (`DefaultDashboardCountService`);
- taint analysis va bir qancha til analizatori birga kelmaydi (32.4 va 32.6).

Teskari misol ham bor: loyihani eksport qilish imkoniyati 9.2 versiyada Enterprise dan Community ga ko'chirilgan (`ExportAction` changelog i). Ya'ni chegara qotib qolgan narsa emas, versiyadan versiyaga siljiydi va har versiyada qayta tekshirilishi kerak.

```bash
# Community nashrni mahalliy sinash uchun eng tez yo'l
# Diqqat: tashqi baza va hajm sozlamalari yo'q, faqat tajriba uchun
# Teg shakli: Community uchun `community` yoki `<versiya>-community`,
# pullik nashrlar uchun `<versiya>-developer`, `-enterprise`,
# `-datacenter-app`, `-datacenter-search`
docker run -d --name sonar-local \
  -p 9000:9000 \
  -e SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true \
  sonarqube:community

# Konteyner tayyor bo'lganini kutish
until curl -sf http://localhost:9000/api/system/status | grep -q '"UP"'; do
  echo "Sonar hali ko'tarilmoqda..."
  sleep 5
done

# Qaysi nashr va qaysi versiya ishlayotganini tekshirish
curl -su admin:admin http://localhost:9000/api/server/version
curl -su admin:admin http://localhost:9000/api/navigation/global \
  | head -c 400
```

## 32.3 Branch tahlili va pull request decoration qaysi nashrdan boshlab mavjud

Branch tahlili va PR decoration Community Build da yo'q: bu kodda aniq to'sib qo'yilgan (32.2). Pullik nashrlarda bu imkoniyat bor, aniq bosqichni esa sotuvchi matritsasidan tasdiqlang. Buning amaliy ma'nosi katta. Branch tahlili bor nashrda har bir feature branch va har bir pull request alohida tahlil qilinadi, "new code" faqat shu PR o'zgartirgan qatorlar bo'yicha hisoblanadi va quality gate natijasi GitHub yoki GitLab PR sahifasida ko'rinadi. Community nashrida esa bitta asosiy branch tahlil qilinadi va dasturchi fikr-mulohazani merge dan keyin oladi, ya'ni eng qimmat paytda.

```yaml
# GitHub Actions: branch va PR parametrlari
# Bu parametrlar branch tahlili bor nashrda kutilgan natija beradi,
# Community Build da esa tahlil xato bilan to'xtaydi
name: sonar
on:
  push:
    branches: [ main ]
  pull_request:
    types: [ opened, synchronize, reopened ]
jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0   # new code aniqlanishi uchun to'liq tarix kerak
      - uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: '21'
      # PR konteksti avtomatik aniqlanadi, lekin token majburiy
      - run: ./mvnw -B verify sonar:sonar
        env:
          SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## 32.4 Taint analysis (chuqur xavfsizlik tahlili) qaysi nashrda ishlaydi

Taint analysis ishonchsiz manbadan (masalan HTTP parametri) xavfli nuqtaga (masalan SQL so'rovi) qadar ma'lumot yo'lini kuzatadi. Bu oddiy pattern tekshiruvidan farq qiladi, chunki u metodlar orasidan o'tib yo'lni quradi. Bu imkoniyat Community Build ga kirmaydi: uni bajaradigan plaginlar tijoriy `com.sonarsource.security` guruhida turadi (`sonar-security-plugin` va til bo'yicha frontendlari: java, php, python, kotlin, go, csharp, vbnet), Community Build ning birga keladigan plaginlar ro'yxatida esa ular yo'q. Natijada bir xil kod Community Build da "toza", taint analysis bor nashrda esa vulnerability sifatida ko'rinadi.

```java
// SHIKOYAT QILINADIGAN kod: so'rov HTTP parametridan to'g'ridan-to'g'ri yig'iladi
@RestController
class HisobotController {

    private final JdbcTemplate jdbc;

    HisobotController(JdbcTemplate jdbc) { this.jdbc = jdbc; }

    @GetMapping("/hisobot")
    List<Map<String, Object>> hisobot(@RequestParam String omborKodi) {
        // Taint analysis bu yo'lni topadi: param -> konkatenatsiya -> SQL
        String sql = "select * from qoldiq where ombor = '" + omborKodi + "'";
        return jdbc.queryForList(sql);
    }
}

// TUZATILGAN kod: parametr qiymat sifatida uzatiladi, SQL matni o'zgarmas
@GetMapping("/hisobot-v2")
List<Map<String, Object>> hisobotV2(@RequestParam String omborKodi) {
    String sql = "select mahsulot, qoldiq from qoldiq where ombor = ?";
    return jdbc.queryForList(sql, omborKodi);
}
```

```sql
-- Yuqoridagi konkatenatsiya nima hosil qilishini ko'rsatadigan misol
-- Oddiy holat:
select * from qoldiq where ombor = 'TOSHKENT-1';

-- Hujum kiritilganda hosil bo'ladigan matn:
select * from qoldiq where ombor = '' or '1'='1';

-- Kerakli shakl: matn qat'iy, qiymat alohida uzatiladi
-- PreparedStatement bilan plan ham qayta ishlatiladi
select mahsulot, qoldiq from qoldiq where ombor = ?;
```

## 32.5 Portfolio, umumiy hisobot va ko'p loyihali ko'rinish

Bitta loyiha sahifasi dasturchiga yetarli, lekin yetakchiga va arxitektorga yetmaydi. Enterprise yo'nalishida portfolio va application tushunchalari paydo bo'ladi, ya'ni o'nlab loyihani bitta ierarxiyaga yig'ib, umumiy reyting va tendentsiyani ko'rish mumkin. Bu, masalan, 40 ta mikroservisdan qaysi biri texnik qarzni tez to'playotganini bitta ekranda ko'rsatadi.

Community yoki Developer nashrida ham bu savolga javob topish mumkin, lekin o'z kuchingiz bilan. Web API dan loyihalar ro'yxati va o'lchovlarni olib, o'zingizning jadvalingizni qurasiz. Bu ish bir kunlik, ammo uni saqlab turish uzoq muddatli majburiyat.

```bash
# Web API orqali o'z "mini portfolio" hisobotini yig'ish
HOST="https://sonar.ichki.example"
TOKEN="$SONAR_TOKEN"

# Barcha loyihalar kalitini olish
curl -su "$TOKEN:" "$HOST/api/projects/search?ps=500" \
  | jq -r '.components[].key' > /tmp/loyihalar.txt

# Har bir loyiha uchun asosiy o'lchovlar
while read -r KEY; do
  curl -su "$TOKEN:" \
    "$HOST/api/measures/component?component=$KEY&metricKeys=ncloc,coverage,bugs,vulnerabilities,sqale_index" \
    | jq -r --arg k "$KEY" \
      '[$k, (.component.measures[] | .value)] | @tsv'
done < /tmp/loyihalar.txt | sort -k2 -n -r
```

## 32.6 Qo'llab-quvvatlanadigan tillar soni nashrga qanday bog'liq

Community Build bilan qaysi analizator birga kelishini taxmin qilish shart emas: u paketlash faylida qatorma-qator sanab o'tilgan. 26.11 kodida ro'yxat shunday: Java (va Java symbolic execution), C#, VB.NET, JavaScript (TypeScript va CSS bilan bir paketda), PHP, Python, Kotlin, Ruby, Scala, Go, Rust, Flex, HTML, XML, IaC va Text (sir qidirish), ustiga JaCoCo hisobotini o'qiydigan plagin.

Tijoriy guruhda (`com.sonarsource.*`) qoladigan analizatorlar esa boshqalar: ABAP, COBOL, CFamily (C, C++, Objective-C), Dart, PL/I, PL/SQL, VB6, RPG, Apex, shuningdek dataflow bug detection (DBD) va xavfsizlik (taint) plaginlari. Ya'ni keng tarqalgan zamonaviy tillar bilan ishlaydigan Spring jamoasi uchun Community Build ning til qamrovi yetadi; C yoki C++ komponenti, mainframe merosi yoki Dart bo'lsa, pullik nashr kerak bo'ladi.

Ro'yxat har relizda o'zgaradi: o'z versiyangizdagi aniq holatni server UI sidagi plaginlar ro'yxatidan yoki shu versiya kodining paketlash faylidan tekshirib oling.

Quyidagi jadval faqat Community Build chegarasini ko'rsatadi, chunki aynan shu chegara ochiq kodda tasdiqlanadi. Pullik bosqichlar orasidagi farqni (nima Developer da, nima Enterprise da) bu yerdan izlamang: uni sotuvchining joriy matritsasi belgilaydi va shartnomadan oldin shu matritsa bilan solishtirish kerak.

| Imkoniyat | Community Build da | Tasdiq |
| --- | --- | --- |
| Asosiy branch tahlili, issue, code smell | bor | ochiq kod va paketlangan analizatorlar |
| Quality gate va quality profile | bor | ochiq kodda |
| Coverage hisobotini qabul qilish | bor | JaCoCo plagini birga keladi |
| Loyihani eksport qilish | bor | 9.2 da Enterprise dan ko'chirilgan |
| Feature branch tahlili | yo'q | kod xato bilan to'xtatadi |
| Pull request tahlili va decoration | yo'q | kod xato bilan to'xtatadi |
| Moslashtirilgan dashboard | yo'q | kodda shunday yozilgan |
| Taint analysis | yo'q | plagin tijoriy guruhda |
| Native va meros tillari (C, C++, COBOL, ABAP, PL/SQL, RPG, Dart) | yo'q | analizatorlar tijoriy guruhda |
| Portfolio va application ko'rinishi | yo'q | ochiq kodda yo'q |
| Klaster (Data Center) | yo'q | ochiq kodda yo'q |

## 32.7 SonarQube Cloud va o'zingizda joylashtirilgan server tanlovi

Cloud variantida server, baza, yangilanish va zaxira nusxa Sonar tomonida bo'ladi, siz faqat CI dan tahlil yuborasiz. O'zingizda joylashtirilgan server esa to'liq nazorat beradi, lekin unga PostgreSQL, Elasticsearch xotirasi, disk, yangilanish oynasi va monitoring kerak. Tanlov ko'pincha texnik emas, tashkiliy: kod tashqariga chiqishi mumkinmi va kimda operatsion resurs bor.

Yana bir farq ish oqimida. Cloud variantida PR integratsiyasi va branch tahlili odatda tarifga kiritilgan bo'ladi, ya'ni Community nashrining cheklovi bu yerda boshqacha ko'rinadi. O'z serveringizda esa bu imkoniyatlar nashr litsenziyasiga bog'liq.

```properties
# sonar-project.properties: ikki muhit uchun bitta fayl
sonar.projectKey=tolov-servisi
sonar.projectName=Tolov Servisi
sonar.sources=src/main/java
sonar.tests=src/test/java
sonar.java.binaries=target/classes

# Coverage: JaCoCo 0.8.x hisobot yo'li
sonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml

# Generatsiya qilingan kodni chiqarib tashlash
# Bu LOC hisobini ham, shovqinni ham kamaytiradi
sonar.exclusions=**/generated/**,**/*MapperImpl.java,**/db/migration/**

# Branch nomi: Developer va yuqorisida ma'noga ega
# Community nashrida bu parametr inkor qilinishi mumkin
sonar.branch.name=${env.BRANCH_NAME}
```

## 32.8 Litsenziya qanday hisoblanadi va xarajat nimaga bog'liq

Litsenziya hisobi va narx siyosati ochiq kodda emas, shuning uchun bu yerda hisoblash qoidasi tasdiqlangan ma'lumot sifatida berilmaydi: uni sotuvchining joriy shartlaridan oling. Shu sababli xarajatni kamaytirishning eng halol yo'li keraksiz kodni tahlildan chiqarib tashlash, ya'ni generatsiya qilingan sinflar va migratsiya skriptlarini exclusions ga kiritish.

Aniq narx yozmaymiz va u haqda taxmin qilmaymiz, chunki narx siyosati, bosqichlar va hisoblash qoidalari o'zgaradi. Hozirgi holatni rasmiy saytdan tekshiring va o'z LOC raqamingiz bilan hisoblang. LOC ni oldindan bilish uchun Community nashrida bir marta tahlil qilib, `ncloc` o'lchovini o'qib olish eng ishonchli usul.

```xml
<!-- Maven: tahlil va coverage uchun minimal, lekin to'g'ri sozlama -->
<properties>
  <!-- Versiyalarni o'zingizdagi joriy relizga moslang -->
  <sonar.maven.plugin.version>4.0.0.4121</sonar.maven.plugin.version>
  <jacoco.version>0.8.12</jacoco.version>
  <!-- LOC hisobini va shovqinni kamaytirish -->
  <sonar.exclusions>**/generated/**,**/config/OpenApiConfig.java</sonar.exclusions>
</properties>

<build>
  <plugins>
    <plugin>
      <groupId>org.jacoco</groupId>
      <artifactId>jacoco-maven-plugin</artifactId>
      <version>${jacoco.version}</version>
      <executions>
        <execution><goals><goal>prepare-agent</goal></goals></execution>
        <!-- XML hisobot majburiy: Sonar faqat uni o'qiydi -->
        <execution>
          <id>report</id><phase>verify</phase>
          <goals><goal>report</goal></goals>
        </execution>
      </executions>
    </plugin>
  </plugins>
</build>
```

## 32.9 Community nashrda chegaralarni qanday chetlab o'tish mumkin va buning narxi

Birinchi usul: har bir branch uchun alohida loyiha kaliti yaratish. Bu ishlaydi, lekin tarix bo'linadi, loyihalar ro'yxati axlatga aylanadi va "new code" davri noto'g'ri hisoblanadi. Ikkinchi usul: PR da Sonar ko'rinishini emas, balki o'zingizning darvozangizni qurish. CI da tahlilni ishga tushirasiz, quality gate natijasini API dan o'qiysiz va build ni yiqitasiz.

Uchinchi usul: PR ga izohni o'zingiz yozish. `git diff` dan o'zgargan qatorlarni olasiz, Sonar issue larini API dan so'raysiz va faqat tegishli qatorlarga tushganini chiqarasiz. Bu Developer nashrining PR decoration natijasiga uzoqdan o'xshaydi, ammo aniqligi pastroq.

```bash
#!/usr/bin/env bash
# Community nashrda "o'z qo'lim bilan PR darvozasi"
set -euo pipefail
HOST="$SONAR_HOST_URL"; KEY="tolov-servisi"

# 1) Tahlilni ishga tushirish va report-task faylini saqlash
./mvnw -B verify sonar:sonar -Dsonar.host.url="$HOST"

# 2) Tahlil navbatda tugashini kutish
CE_URL=$(grep '^ceTaskUrl=' target/sonar/report-task.txt | cut -d= -f2-)
until curl -su "$SONAR_TOKEN:" "$CE_URL" | grep -q '"status":"SUCCESS"'; do
  echo "Tahlil hali hisoblanmoqda..."
  sleep 5
done

# 3) Quality gate holatini o'qish va build ni shu asosda yiqitish
STATUS=$(curl -su "$SONAR_TOKEN:" \
  "$HOST/api/qualitygates/project_status?projectKey=$KEY" \
  | jq -r '.projectStatus.status')
echo "Quality gate: $STATUS"
[ "$STATUS" = "OK" ] || { echo "Darvoza yopiq, PR to'xtatiladi"; exit 1; }
```

Bu yo'llarning umumiy narxi bor. Siz skript saqlashga, API o'zgarishini kuzatishga va yangi odamga buni tushuntirishga vaqt sarflaysiz. Taint analysis va portfolio kabi imkoniyatlarni esa hech qanaqa skript bilan qaytarib bo'lmaydi.

| Tuzoq | Nega yuzaga keladi | Yechim |
| --- | --- | --- |
| PR da Sonar izohi yo'q | nashr branch tahlilini qo'llamaydi | nashrni tekshirish yoki API asosida o'z darvozani qurish |
| Har branch alohida loyiha | Community cheklovini aylanib o'tish | vaqtinchalik kalitlarni avtomatik tozalash va faqat main ni saqlash |
| Coverage 0 ko'rinadi | JaCoCo XML hisobot yaratilmagan | `verify` fazasida `report` goal ni yoqish |
| New code noto'g'ri hisoblanadi | sayoz klon, tarix yo'q | CI da to'liq tarixni olish |
| Xavfsizlik yo'li topilmaydi | taint analysis nashrda yo'q | sinkni parametrlashtirish va ko'rib chiqishni majburiy qilish |
| Litsenziya kutilganidan qimmat | generatsiya qilingan kod ham hisoblangan | exclusions bilan haqiqiy kodni ajratish |
| Sonar ishdan chiqsa CI to'xtaydi | bitta nusxa, zaxira yo'q | kritik bo'lsa klaster yo'nalishini baholash |
| Nashr imkoniyati haqida bahs | eski hujjat va eski nomlar | joriy rasmiy matritsani manba qilib olish |

## 32.10 Qaysi jamoaga qaysi nashr mos keladi: hajm va ehtiyojga qarab tavsiya

Bitta yoki ikkita dasturchi va ichki loyiha uchun Community nashri yetarli. Siz quality gate ni o'rganasiz, coverage ni yig'asiz va kodni toza saqlash odatini shakllantirasiz. Kundalik PR oqimi bor 5 dan 50 gacha dasturchili jamoa uchun branch tahlili amalda majburiy bo'ladi, chunki fikr-mulohaza merge dan keyin kelsa hech kim uni tuzatmaydi. Moliyaviy yoki shaxsiy ma'lumot bilan ishlaydigan jamoa uchun taint analysis alohida qiymat beradi.

Ko'p jamoali tashkilot uchun asosiy ehtiyoj ko'rinish bo'ladi, ya'ni o'nlab loyihani bitta ierarxiyada kuzatish. Sonar CI ning majburiy bo'g'iniga aylangan va to'xtashi qimmatga tushadigan tashkilotlar uchun esa klaster yo'nalishi muhokama qilinadi.

| Savol | Oddiy yondashuv | Arxitektor yondashuvi |
| --- | --- | --- |
| Nashr tanlash | "bepulini olamiz, keyin ko'ramiz" | kerakli imkoniyatlar ro'yxatidan boshlanadi |
| PR fikr-mulohazasi | merge dan keyin tekshiriladi | PR da bloklanadi, aks holda qiymat yo'qoladi |
| Xavfsizlik | pattern tekshiruvga ishonadi | manba va nuqta yo'lini kuzatish talab qiladi |
| LOC va xarajat | tahlildan keyin hayron bo'ladi | exclusions va `ncloc` oldindan o'lchanadi |
| Cloud yoki o'z serveri | "o'zimizda ishonchliroq" | operatsion yuk va ma'lumot siyosati hisoblanadi |
| Imkoniyat bahsi | eski blog postiga tayanadi | joriy rasmiy matritsani manba qiladi |
| Community cheklovi | har branch uchun yangi loyiha ochadi | ongli ravishda API asosida darvoza quradi |
| Ishonchlilik | bitta nusxa, zaxirasiz | to'xtash narxini hisoblab, klasterni baholaydi |
| Yangilanish | tasodifan versiya oshiradi | LTA liniyasida qoladi va reja bilan ko'chadi |
| Qaror hujjati | og'zaki kelishuv | tanlov sababi yozib qoldiriladi |

## 32.11 Nashrni tanlashdan oldin beriladigan savollar

Birinchi savol: fikr-mulohaza qachon kerak. Agar javob "PR da" bo'lsa, branch tahlili bo'lmagan nashr sizga mos kelmaydi. Ikkinchi savol: kodda ishonchsiz kiritma xavfli nuqtaga yetib boradigan joy bormi. Agar bor bo'lsa, taint analysis ni alohida baholang.

Uchinchi savol: nechta loyiha va kim umumiy manzarani ko'rishi kerak. Agar javob "o'nlab loyiha va texnik direktor" bo'lsa, portfolio yo'nalishi muhokamaga kiradi. To'rtinchi savol: Sonar to'xtasa nima bo'ladi. Agar relizga chiqa olmasangiz, bu ishonchlilik masalasi va u pul bilan hal qilinadi. Beshinchi savol: haqiqiy LOC qancha va undan qancha qismi generatsiya qilingan. Bu raqamni oldindan o'lchash mumkin va u tahlil hajmini ham, shovqinni ham belgilaydi.

Oltinchi savol: yangilanish qatori qaysi. Kodning o'z sozlamalarida har reliz uchun amal qilish muddati (EOL) yozib qo'yiladi: LTA bo'lmagan versiya uchun u keyingi relizgacha, LTA versiya uchun esa reliz sanasidan 12 oy (premium qo'llab-quvvatlash bilan 18 oy). Ya'ni oddiy qatorda qolsangiz, har reliz bilan ko'chishga majbursiz.

Alohida eslatma: coverage, quality gate va yangi kod tamoyili bo'yicha kundalik ish uslubi barcha nashrlarda bir xil, bu masalalar bu hujjatning quality gate va yangi kod mavzularida yoritilgan. Test yozish uslubi esa [testlash qo'llanmasiga](../testing/README.md) tegishli.

## 32.12 Amalda qo'llash

- [ ] Hozirgi serveringizda qaysi nashr va qaysi versiya ishlayotganini `api/server/version` va UI orqali aniqlab, hujjatga yozib qo'ying.
- [ ] Jamoaga kerakli imkoniyatlar ro'yxatini tuzing va uni joriy rasmiy nashr matritsasi bilan qator-qator solishtiring.
- [ ] Bitta tahlil ishga tushirib `ncloc` qiymatini o'lchang va generatsiya qilingan kodni `sonar.exclusions` bilan chiqarib tashlagandan keyin qayta o'lchang.
- [ ] Agar PR fikr-mulohazasi hozir yo'q bo'lsa, API asosidagi quality gate skriptini CI ga qo'shib, kamida bloklash mexanizmini yo'lga qo'ying.
- [ ] CI da `fetch-depth: 0` o'rnatilganini tekshirib, new code hisobining to'g'riligini tasdiqlang.
- [ ] Kodda ishonchsiz kiritmadan SQL yoki buyruq nuqtasiga boradigan yo'llarni qo'lda ro'yxatlab, taint analysis qancha qiymat berishini baholang.
- [ ] Cloud va o'z serveri variantlarini operatsion yuk, ma'lumot siyosati va to'xtash narxi bo'yicha bitta sahifada taqqoslang.
- [ ] Yakuniy tanlovni sababi bilan qaror hujjatiga yozib, narx va nashr nomlarini rasmiy saytdan tasdiqlangan sana bilan belgilang.

## Manbalar

- SonarQube Community Build manbasi, `c9f52e4d6e4a34a0d8ba4df9de9c093b6e077707` commit (26.11, 2026-10-16): [`sonar-core/src/main/java/org/sonar/core/platform/EditionProvider.java`](https://github.com/SonarSource/sonarqube/blob/c9f52e4d6e4a34a0d8ba4df9de9c093b6e077707/sonar-core/src/main/java/org/sonar/core/platform/EditionProvider.java) - `Edition` enum i to'rt qiymat: COMMUNITY, DEVELOPER, ENTERPRISE, DATACENTER va ularning yorliqlari
- [`README.md`](https://github.com/SonarSource/sonarqube/blob/c9f52e4d6e4a34a0d8ba4df9de9c093b6e077707/README.md) - ochiq nashrning rasmiy nomi "SonarQube Community Build", litsenziya LGPL v3
- [`server/sonar-ce-task-projectanalysis/src/main/java/org/sonar/ce/task/projectanalysis/analysis/AnalysisMetadataHolderImpl.java`](https://github.com/SonarSource/sonarqube/blob/c9f52e4d6e4a34a0d8ba4df9de9c093b6e077707/server/sonar-ce-task-projectanalysis/src/main/java/org/sonar/ce/task/projectanalysis/analysis/AnalysisMetadataHolderImpl.java) - "Branches and Pull Requests are not supported in Community Edition"
- [`server/sonar-webserver-webapi/src/main/java/org/sonar/server/issue/ws/SearchAction.java`](https://github.com/SonarSource/sonarqube/blob/c9f52e4d6e4a34a0d8ba4df9de9c093b6e077707/server/sonar-webserver-webapi/src/main/java/org/sonar/server/issue/ws/SearchAction.java) - `branch` va `pullRequest` parametrlari izohi: "Not available in the community edition"
- [`server/sonar-webserver-webapi/src/main/java/org/sonar/server/projectdump/ws/ExportAction.java`](https://github.com/SonarSource/sonarqube/blob/c9f52e4d6e4a34a0d8ba4df9de9c093b6e077707/server/sonar-webserver-webapi/src/main/java/org/sonar/server/projectdump/ws/ExportAction.java) - changelog: loyiha eksporti 9.2 da Enterprise dan Community ga ko'chirilgan
- [`server/sonar-webserver/src/main/java/org/sonar/server/platform/telemetry/DefaultDashboardCountService.java`](https://github.com/SonarSource/sonarqube/blob/c9f52e4d6e4a34a0d8ba4df9de9c093b6e077707/server/sonar-webserver/src/main/java/org/sonar/server/platform/telemetry/DefaultDashboardCountService.java) - "Community Edition does not support custom dashboards"
- [`sonar-application/bundled_plugins.gradle`](https://github.com/SonarSource/sonarqube/blob/c9f52e4d6e4a34a0d8ba4df9de9c093b6e077707/sonar-application/bundled_plugins.gradle) - Community Build bilan birga keladigan analizatorlar ro'yxati (32.6)
- [`build.gradle`](https://github.com/SonarSource/sonarqube/blob/c9f52e4d6e4a34a0d8ba4df9de9c093b6e077707/build.gradle) - tijoriy `com.sonarsource.*` guruhidagi analizatorlar va xavfsizlik (taint) plaginlari (32.4, 32.6)
- [`gradle.properties`](https://github.com/SonarSource/sonarqube/blob/c9f52e4d6e4a34a0d8ba4df9de9c093b6e077707/gradle.properties) - versiya 26.11 va EOL qoidasi: LTA bo'lmagan versiya keyingi relizgacha, LTA versiya 12 oy, premium qo'llab-quvvatlash bilan 18 oy
- [`server/sonar-webserver-webapi/src/main/java/org/sonar/server/platform/ws/UpgradesAction.java`](https://github.com/SonarSource/sonarqube/blob/c9f52e4d6e4a34a0d8ba4df9de9c093b6e077707/server/sonar-webserver-webapi/src/main/java/org/sonar/server/platform/ws/UpgradesAction.java) - 2026.5 da `lta` maydoni qo'shilgan, atama Long-Term Active
- Docker Hub `library/sonarqube` teglar ro'yxati, 2026-10-17 da olingan - teg shakllari `community`, `26.10.0.133078-community`, `2026.5.2-developer`, `2026.5.2-enterprise`, `2026.5.2-datacenter-app`, `2026.5-lta-developer`; `lts-community` degan teg yo'q
- ESLATMA: pullik bosqichlar orasidagi imkoniyat taqsimoti (nima Developer da, nima Enterprise da), litsenziya hisobi va narx ochiq manbada yo'q. Ular shu bobda tasdiqlangan ma'lumot sifatida berilmaydi, sotuvchining joriy matritsasidan tekshirilishi kerak
- ESLATMA: 32.5, 32.7, 32.9, 32.10, 32.11 va 32.12 dagi tavsiyalar, jamoa hajmi bo'yicha maslahat va API asosida darvoza qurish usullari shu korpusning amaliy tavsiyasi, birlamchi manbadan olingan emas

---

[&larr; 31. Xatolarga tushmaslik uchun yakuniy tavsiyalar](31-xatolarga-tushmaslik-uchun-yakuniy.md) · [Mundarija](README.md) · [33. Serverni o'rnatish, sozlash va resurs rejalashtirish &rarr;](33-serverni-ornatish-sozlash-va-resurs.md)
