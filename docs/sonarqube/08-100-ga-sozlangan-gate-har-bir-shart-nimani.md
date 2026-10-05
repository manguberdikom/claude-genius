<!-- doc: sonarqube | chapter: 8 | part: II. Quality gate -->

[Barcha hujjatlar](../../README.md) / [SonarQube](README.md)

# 8. 100% ga sozlangan gate: har bir shart nimani talab qiladi (A Gate Set to 100 Percent)

<details>
<summary>Bu bobdagi 12 bo'lim</summary>

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

</details>



Jamoalar "gate ni 100% ga sozlaymiz" deganda ko'pincha bitta raqamni, ya'ni coverage ni nazarda tutadi. Amalda esa quality gate bir nechta mustaqil shartning mantiqiy VA birikmasi, va ularning har biri boshqa narsani o'lchaydi. Shuning uchun "100% gate" ni qondirish bitta ish emas, balki besh-olti xil ishning jamlanmasi. Bu bob har bir shartni alohida ochadi, ularning o'zaro ziddiyatini ko'rsatadi va qondirish tartibini aniq ketma-ketlikda beradi.

## 8.1 "100% gate" aslida nimani anglatadi: bu bitta raqam emas, bir nechta shart

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

## 8.2 Shart: yangi kodda coverage 100 foiz, nimani talab qiladi va qanchaga tushadi

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

## 8.3 Shart: yangi kodda takrorlanish 0 foiz, qanday qondiriladi

Sonar takrorlanishni token ketma-ketligi bo'yicha topadi, matn bo'yicha emas. Java uchun chegara odatda kamida 10 ta ketma-ket bayonot atrofida, aniq qiymat tilga va versiyaga qarab farq qiladi. O'zgaruvchi nomini almashtirish takrorni yashirmaydi.

0 foiz talabi eng og'ir uriladigan joy integratsion testlar. Ikki `@SpringBootTest` sinfida bir xil `given` bloki bo'lsa, u darhol duplication bo'lib chiqadi. To'g'ri yechim testdan takrorni olib tashlash, ya'ni umumiy fixture ni `@TestConfiguration` yoki builder ga ko'chirish. Noto'g'ri yechim esa `sonar.cpd.exclusions` ga butun test papkasini yozib qo'yish, chunki shunda haqiqiy nusxa-ko'chirma ham ko'rinmay qoladi.

Produktsion kodda eng ko'p takrorlanadigan uchta joy: DTO dan entity ga o'girish, validatsiya bloklari, va `try/catch` bilan o'ralgan tashqi chaqiruvlar. Birinchisini mapper ga, ikkinchisini Bean Validation annotatsiyalariga, uchinchisini bitta `execute(Supplier<T>)` yordamchisiga yig'ish takrorlanishni ildizdan yo'qotadi.

## 8.4 Shart: yangi issue 0 ta, har bir toifa bo'yicha nima qilish kerak

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

## 8.5 Shart: security hotspot 100 foiz ko'rib chiqilgan, jarayoni

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

Bu so'rovni qoplash uchun haqiqiy baza kerak, mock emas. Testcontainers bilan qanday ishlash [testlash qo'llanmasidagi](../testing/README.md) Testcontainers mavzusida batafsil yozilgan, shuning uchun bu yerda takrorlanmaydi.

## 8.6 Shart: reytinglar A darajada, nima buzadi

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

## 8.7 Shartlar birga qo'yilganda yuzaga keladigan qarama-qarshiliklar

Birinchi ziddiyat: coverage 100 foiz va issue 0 ta bir-biriga qarshi ishlaydi. Qoplanmagan tarmoqni yopish uchun test yozasan, test kodida esa Sonar o'z qoidalarini qo'llaydi. Natijada test yozish yangi issue keltiradi, uni tuzatish yana vaqt oladi. Yechim: test kodi uchun alohida quality profile, lekin bu profil bo'sh bo'lmasin, chunki test kodi ham kod.

Ikkinchi ziddiyat: duplication 0 foiz va coverage 100 foiz. Takrorni yo'qotish uchun abstraksiya chiqarasan, abstraksiya esa yangi tarmoqlar keltiradi, ular yana test talab qiladi. Ba'zan ozgina takror abstraksiyadan arzonroq, lekin 0 foiz shart bunga yo'l bermaydi.

Uchinchi ziddiyat: mudofaa kodi va coverage. "Bu hech qachon bo'lmaydi" deb yozilgan `else` bloki testda qo'zg'atilishi qiyin. Jamoa ikki yo'ldan birini tanlashga majbur: mudofaa kodini olib tashlash yoki uni sun'iy test bilan qoplash. Birinchisi odatda to'g'riroq, chunki o'lmas kod texnik qarz.

To'rtinchi ziddiyat: reyting A va amaliy muddat. Reytingni ko'tarish uchun refaktoring kerak, refaktoring esa diff ni kattalashtiradi, katta diff esa yana ko'proq yangi kod va ko'proq coverage talabi degani. Bu halqadan chiqish uchun refaktoringni alohida PR qilish kerak, funksional o'zgarishdan ajratib.

## 8.8 Gate ni qondirish uchun kerakli ish tartibi: aniq ketma-ketlik

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

## 8.9 foiz gate ning haqiqiy narxi: vaqt, jamoa charchog'i, chetlab o'tish xavfi

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

## 8.10 Qachon 100 foiz o'rinli, qachon 80-90 aqlliroq qaror

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

## 8.11 Gate ni bosqichma-bosqich qattiqlashtirish rejasi

Birdan 100 foizga o'tish deyarli har doim chetlab o'tish bilan tugaydi. Shuning uchun gate to'rt bosqichda qattiqlashtiriladi, har bosqich kamida ikki sprint turadi.

Birinchi bosqich: yangi kod ta'rifini to'g'rilash va gate ni faqat kuzatuv rejimida ishlatish. Hech narsa bloklanmaydi, lekin har PR da raqam ko'rinadi.

Ikkinchi bosqich: yangi kodda blocker va critical darajadagi issue larni bloklash, coverage chegarasini 60 ga qo'yish. Shu bosqichda SonarLint ni IDE ga majburiy qilish kerak, aks holda feedback juda kech keladi.

Uchinchi bosqich: coverage ni 80 ga, duplication ni 3 foizga, hotspot review ni 100 foizga ko'tarish. Bu aslida standart `Sonar way` darajasi va aksariyat jamoa uchun oqilona nuqta.

To'rtinchi bosqich: faqat yadro modullarda coverage 100 va issue 0. Bu bosqich butun monorepoga emas, nomlangan modullarga qo'llanadi. Shu paytda gate ro'yxati, exclusion ro'yxati va chetlab o'tish jurnali bitta hujjatda bo'lishi kerak, aks holda uch oydan keyin hech kim nega shunday qilinganini eslay olmaydi.

## 8.12 Amalda qo'llash

- [ ] `api/qualitygates/show` dan mavjud shart nomlarini o'qib, o'z versiyangizdagi aniq metrika kalitlarini yozib qo'ying.
- [ ] `sonar.coverage.jacoco.xmlReportPaths` va `verify` dan keyin `sonar:sonar` tartibini tekshirib, coverage 0 bo'lmasligiga ishonch hosil qiling.
- [ ] Loyiha ildiziga `lombok.config` qo'shib `lombok.addLombokGeneratedAnnotation = true` yozing va coverage o'zgarishini o'lchang.
- [ ] Yangi kod ta'rifini `referenceBranch=main` ga o'tkazib, PR analizini `sonar.pullrequest.*` parametrlari bilan ulang.
- [ ] CI da `sonar.qualitygate.wait=true` qo'yib, gate buzilishi merge ni to'xtatishini tasdiqlang.
- [ ] Har bir exclusion va `Won't fix` qaroriga sabab yozadigan jurnal fayli yuritishni boshlang.
- [ ] Qaysi modulda 100 foiz, qaysi modulda 80 foiz talab qilinishini risk bo'yicha ajratib, ikkita alohida gate yarating.
- [ ] Bitta yadro modulda mutation testing ishlatib, 100 foiz coverage haqiqatan xatoni ushlayotganini tekshirib ko'ring.

---

[&larr; 7. Yangi kod (new code) va "clean as you code" tamoyili](07-yangi-kod-new-code-va-clean-as-you-code.md) · [Mundarija](README.md) · [9. Coverage qanday o'lchanadi: JaCoCo mexanikasi &rarr;](09-coverage-qanday-olchanadi-jacoco-mexanikasi.md)
