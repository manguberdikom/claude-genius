<!-- doc: sonarqube | chapter: 32 | part: VIII. Server va tashkilot -->

[Barcha hujjatlar](../../README.md) / [SonarQube](README.md)

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

Qator to'rt bosqichdan iborat va har bir yuqori bosqich pastdagini to'liq o'z ichiga oladi. Community bepul va ochiq asosdagi nashr, u yakka dasturchi yoki kichik jamoa uchun yetarli. Developer nashri branch tahlili va chuqur xavfsizlik tahlilini qo'shadi, ya'ni kundalik PR ish oqimi shu yerdan boshlanadi. Enterprise nashri portfolio, umumiy boshqaruv hisobotlari va ko'p loyihali tashkilot ehtiyojlarini qo'shadi. Data Center yo'nalishi esa klaster, yuqori ishonchlilik va gorizontal masshtab uchun, ya'ni Sonar ishdan chiqsa butun CI to'xtab qolishi mumkin bo'lgan tashkilotlar uchun.

Nomlar bilan ehtiyot bo'lish kerak. Sonar brendi bir necha marta qayta nomlangan va bugungi hujjatlarda "SonarQube Server", "SonarQube Cloud" va "SonarQube Community Build" kabi atamalar uchraydi, avvalroq esa "SonarQube" va "SonarCloud" ishlatilgan. Agar sizning jamoada eski atamalar yursa, bu qo'shimcha chalkashlik manbai bo'ladi. Hozirgi rasmiy nomlanishni va nashrlar ro'yxatini rasmiy saytdan tekshiring.

## 32.2 Community nashrda nima bor va nima yo'q

Community nashrda tahlil yadrosi to'liq ishlaydi. Siz quality profile sozlaysiz, quality gate yaratasiz, issue va code smell ko'rasiz, coverage hisobotini yuklaysiz va Web API orqali hammasini avtomatlashtirasiz. Ya'ni "Sonar o'tadigan kod yozish" mashqining 80 foizini bepul nashrda ham bajarish mumkin.

Yo'q narsalar esa aniq va sezilarli. Odatda Community nashrda faqat bitta asosiy branch tahlil qilinadi, pull request uchun alohida tahlil va PR decoration bo'lmaydi, taint analysis ishlamaydi, portfolio darajasidagi ko'rinish yo'q va ba'zi tillar qo'llanmaydi. Bu taqsimot versiyaga qarab o'zgarishi mumkin, shuning uchun o'z versiyangiz hujjatiga qarab tasdiqlang.

```bash
# Community nashrni mahalliy sinash uchun eng tez yo'l
# Diqqat: tashqi baza va hajm sozlamalari yo'q, faqat tajriba uchun
docker run -d --name sonar-local \
  -p 9000:9000 \
  -e SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true \
  sonarqube:lts-community

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

Branch tahlili va PR decoration odatda Developer nashridan boshlab mavjud bo'ladi. Buning amaliy ma'nosi katta. Developer nashrida har bir feature branch va har bir pull request alohida tahlil qilinadi, "new code" faqat shu PR o'zgartirgan qatorlar bo'yicha hisoblanadi va quality gate natijasi to'g'ridan-to'g'ri GitHub yoki GitLab PR sahifasida ko'rinadi. Community nashrida esa bitta asosiy branch tahlil qilinadi va dasturchi fikr-mulohazani merge dan keyin oladi, ya'ni eng qimmat paytda.

```yaml
# GitHub Actions: branch va PR parametrlari
# Bu parametrlar Developer nashri va yuqorisida kutilgan natija beradi
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

Taint analysis ishonchsiz manbadan (masalan HTTP parametri) xavfli nuqtaga (masalan SQL so'rovi) qadar ma'lumot yo'lini kuzatadi. Bu oddiy pattern tekshiruvidan farq qiladi, chunki u metodlar orasidan o'tib yo'lni quradi. Odatda bu imkoniyat Developer nashridan boshlab ishlaydi va Community nashrida mavjud emas. Natijada bir xil kod Community da "toza", Developer da esa vulnerability sifatida ko'rinadi.

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

Tillar ro'yxati nashrga bog'liq va bu ko'pchilik uchun kutilmagan cheklov bo'ladi. Umumiy qoida shunday: keng tarqalgan zamonaviy tillar Community nashrida ham bor, kompilyatsiya talab qiladigan mahalliy tillar va korporativ meros tillari esa yuqori nashrlarda paydo bo'ladi. Java, Kotlin, JavaScript, TypeScript, Python va shunga o'xshash tillar bilan ishlaydigan Spring jamoasi uchun Community nashrining til qamrovi odatda muammo emas.

Agar sizda C yoki C++ komponenti, mobil native kod yoki mainframe merosi bo'lsa, tekshirish majburiy. Aniq taqsimot versiyadan versiyaga o'zgaradi, shuning uchun til ro'yxatini rasmiy saytdagi joriy matritsadan tasdiqlang va uni arxitektura qaroriga asos qilib olmang.

| Imkoniyat | Community | Developer | Enterprise | Data Center |
| --- | --- | --- | --- | --- |
| Asosiy branch tahlili, issue, code smell | bor | bor | bor | bor |
| Quality gate va quality profile | bor | bor | bor | bor |
| Coverage hisobotini qabul qilish | bor | bor | bor | bor |
| Feature branch tahlili | yo'q | bor | bor | bor |
| Pull request tahlili va decoration | yo'q | bor | bor | bor |
| Taint analysis (manba va nuqta yo'li) | yo'q | bor | bor | bor |
| Xavfsizlik hisobotlari (OWASP kabi) | cheklangan | bor | bor | bor |
| Portfolio va application ko'rinishi | yo'q | yo'q | bor | bor |
| Tashkiliy boshqaruv hisobotlari | yo'q | yo'q | bor | bor |
| Qo'shimcha tillar (native, meros) | cheklangan | kengayadi | yana kengayadi | yana kengayadi |
| Klaster va yuqori ishonchlilik | yo'q | yo'q | yo'q | bor |

Yuqoridagi taqsimot umumiy manzara uchun va versiyaga qarab o'zgarishi mumkin. Shartnoma yoki arxitektura qaroridan oldin joriy rasmiy jadval bilan solishtiring.

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

Sonar litsenziyasi an'anaviy ravishda tahlil qilinadigan kod qatorlari soniga, ya'ni LOC ga bog'lanadi va yillik obuna shaklida sotiladi. Dasturchilar soni emas, kod hajmi asosiy o'lchov bo'lishi odatiy holat. Shu sababli xarajatni kamaytirishning eng halol yo'li keraksiz kodni tahlildan chiqarib tashlash, ya'ni generatsiya qilingan sinflar va migratsiya skriptlarini exclusions ga kiritish.

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

Uchinchi savol: nechta loyiha va kim umumiy manzarani ko'rishi kerak. Agar javob "o'nlab loyiha va texnik direktor" bo'lsa, portfolio yo'nalishi muhokamaga kiradi. To'rtinchi savol: Sonar to'xtasa nima bo'ladi. Agar relizga chiqa olmasangiz, bu ishonchlilik masalasi va u pul bilan hal qilinadi. Beshinchi savol: haqiqiy LOC qancha va undan qancha qismi generatsiya qilingan. Bu raqam bevosita xarajatga ta'sir qiladi va uni oldindan o'lchash mumkin.

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

---

[&larr; 31. Xatolarga tushmaslik uchun yakuniy tavsiyalar](31-xatolarga-tushmaslik-uchun-yakuniy.md) · [Mundarija](README.md) · [33. Serverni o'rnatish, sozlash va resurs rejalashtirish &rarr;](33-serverni-ornatish-sozlash-va-resurs.md)
