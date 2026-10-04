<!-- doc: sonarqube | chapter: 23 | part: VI. Amaliyot va jarayon -->

[SonarQube](../../README.md) / [SonarQube](README.md)

# 23. Legacy loyihani 100% ga olib chiqish rejasi (Bringing a Legacy Project to 100)

<details>
<summary>Bu bobdagi 13 bo'lim</summary>

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

</details>


Legacy loyihani Sonar ko'rsatkichlari bo'yicha "100% ga olib chiqish" degan gap ko'pincha noto'g'ri tushuniladi. Maqsad barcha issue ni nolga tushirish emas, balki quality gate ni barqaror yashil holatda tutib turish va yangi kodni toza yozish. Bu bob o'n ikki yillik kod bazasiga Sonar ni kiritishdan boshlab, bir yil ichida o'lchanadigan natijaga chiqishgacha bo'lgan rejani beradi. Refaktoring usullari [arxitektor hujjatida](../architect/README.md), bu yerda faqat ko'rsatkichlar va jarayon.

## 23.1 Birinchi tahlil: minglab issue chiqqanda vahimaga tushmaslik

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

## 23.2 Boshlang'ich holatni qayd etish va uni taqqoslash nuqtasi qilish

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

## 23.3 "Clean as you code" ni birinchi kundan yoqish

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

## 23.4 Yangi kod shartlarini darhol qattiq qo'yish, eski kodni bosqichma-bosqich tuzatish

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

## 23.5 Eski issue larni toifalash: tuzatish, qoldirish, qoidani o'chirish

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

## 23.6 Qaysi modulni birinchi tozalash: xavf va o'zgarish tezligiga qarab

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

## 23.7 Qamrovni bosqichma-bosqich oshirish rejasi va oraliq maqsadlar

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

## 23.8 Testsiz kodga test yozish tartibi: avval xatti-harakatni qayd etish

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

## 23.9 Jamoani jarayonga qo'shish va vaqt ajratish masalasi

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

## 23.10 Rahbarga rejani va kutilayotgan natijani tushuntirish

Rahbarga "texnik qarz" deb tushuntirish deyarli hech qachon ishlamaydi. Ishlaydigan til: xatolar narxi va yetkazib berish tezligi.

Uchta raqamni oldinga chiqaring: oxirgi olti oydagi production incident soni va ularning qanchasi test bilan tutilishi mumkin edi, bitta release tayyorlash vaqti, yangi developer ning birinchi PR ga chiqish vaqti.

So'rash kerak bo'lgan narsa ham aniq bo'lsin: sprint sig'imining 15 foizi, 12 oy muddat, har chorakda hisobot. Cheksiz "tozalash loyihasi" so'ramang, u birinchi muddat siqilishida bekor qilinadi.

Va'da berishda ehtiyot bo'ling. "Bir yildan keyin 100% o'tadi" deb aytmang. To'g'ri formula: bir yildan keyin har bir PR gate dan o'tadi, yangi kodning 80 foizi qoplangan bo'ladi, umumiy coverage 25 foiz atrofida bo'ladi. Bu kam ko'rinadi, lekin bu bajariladigan va'da.

## 23.11 Muvaffaqiyat o'lchovi: issue soni emas, nimani o'lchash kerak

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

## 23.12 Bir yillik real jadval namunasi

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

## 23.13 Amalda qo'llash

- [ ] Birinchi skanni `fetch-depth: 0` bilan oling va hech qanday gate shartisiz baseline raqamlarini o'z jadvalingizga yozib qo'ying.
- [ ] `sonar.exclusions` va `sonar.coverage.exclusions` ni sozlab, generatsiya qilingan kod va konfiguratsiya klasslarini skandan chiqaring, keyin skanni qayta yuritib raqamlar farqini qayd eting.
- [ ] Yangi kod chegarasini `previous_version` ga qo'ying va release jarayoni `projectVersion` ni haqiqatan oshirayotganini tekshiring.
- [ ] Quality gate da faqat new code shartlarini yoqing: coverage 80%, duplication 3%, yangi blocker va critical nol.
- [ ] Jamoa bilan bir majlis o'tkazib, eng ko'p chiqqan 30 qoida uchun tuzatish, `Accept` yoki profildan o'chirish qarorini birga qabul qiling.
- [ ] Git tarixidan eng tez o'zgaradigan 15 paketni chiqarib, biznes xavfi bilan kesishtiring va birinchi tozalanadigan modulni tanlang.
- [ ] Tanlangan modulga JaCoCo `check` chegarasini qo'ying va uni har chorakda qo'lda ko'tarishni kalendarga yozing.
- [ ] Oylik hisobot uchun gate o'tish foizi, new code coverage medianasi va production incident sonini birga ko'rsatadigan bitta jadval tayyorlang.

---

[&larr; 22. Lokal tekshirish: IDE, sonar-scanner va tez qaytish](22-lokal-tekshirish-ide-sonar-scanner-va-tez.md) · [Mundarija](README.md) · [24. False positive, suppression va o'z qoidangiz &rarr;](24-false-positive-suppression-va-oz-qoidangiz.md)
