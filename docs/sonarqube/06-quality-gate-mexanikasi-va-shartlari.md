<!-- doc: sonarqube | chapter: 6 | part: II. Quality gate -->

[Barcha hujjatlar](../../README.md) / [SonarQube](README.md)

# 6. Quality gate mexanikasi va shartlari (Quality Gate Mechanics)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

- [6.1 Quality gate nima: shartlar to'plami va ularning tekshirilishi](#61-quality-gate-nima-shartlar-toplami-va-ularning-tekshirilishi)
- [6.2 Standart gate va uning shartlari](#62-standart-gate-va-uning-shartlari)
- [6.3 Shart tuzilishi: metrika, operator, chegara qiymati](#63-shart-tuzilishi-metrika-operator-chegara-qiymati)
- [6.4 Gate holati: passed va failed, va u qachon hisoblanadi](#64-gate-holati-passed-va-failed-va-u-qachon-hisoblanadi)
- [6.5 Gate ni loyihaga tayinlash va bir nechta gate ni boshqarish](#65-gate-ni-loyihaga-tayinlash-va-bir-nechta-gate-ni-boshqarish)
- [6.6 Gate natijasini CI da olish: `sonar.qualitygate.wait` va uning ta'siri](#66-gate-natijasini-ci-da-olish-sonarqualitygatewait-va-uning-tasiri)
- [6.7 Gate failed bo'lganda build ni to'xtatish yoki ogohlantirish bilan cheklanish](#67-gate-failed-bolganda-build-ni-toxtatish-yoki-ogohlantirish-bilan-cheklanish)
- [6.8 Gate shartlarini tanlash mantiqi: nimani bloklash kerak, nimani kerak emas](#68-gate-shartlarini-tanlash-mantiqi-nimani-bloklash-kerak-nimani-kerak-emas)
- [6.9 Juda qattiq gate ning ta'siri: chetlab o'tish yo'llari va jamoa xatti-harakati](#69-juda-qattiq-gate-ning-tasiri-chetlab-otish-yollari-va-jamoa-xatti-harakati)
- [6.10 Gate o'zgarganda tarixiy loyihalarga ta'siri](#610-gate-ozgarganda-tarixiy-loyihalarga-tasiri)
- [6.11 Amalda qo'llash](#611-amalda-qollash)

</details>



Quality gate Sonar tahlilining yakuniy hukmi. Analiz minglab issue va o'nlab metrikani hisoblaydi, lekin CI ga faqat bitta javob kerak: o'tdi yoki o'tmadi. Quality gate aynan shu javobni beradigan mexanizm, va u sehrli emas: bir nechta oddiy shartning mantiqiy VA (AND) birlashmasi. Shu bobda shart qanday tuzilishini, holat qachon hisoblanishini, CI uni qanday kutib olishini va qattiq sozlangan gate jamoani qanday buzishini ko'ramiz.

## 6.1 Quality gate nima: shartlar to'plami va ularning tekshirilishi

Quality gate nomlangan shartlar ro'yxati. Har bir shart bitta metrikaga tegishli. Shart "coverage 80% dan kam bo'lsa failed" yoki "yangi duplikatsiya 3% dan ko'p bo'lsa failed" ko'rinishida yoziladi. Gate holati barcha shartlarning birlashmasi: hech bo'lmasa bitta shart buzilsa, gate failed bo'ladi. Shartlar orasida OR yo'q, ularni "yoki" bilan birlashtirib bo'lmaydi.

Muhim nuqta: gate shartni o'zi hisoblamaydi. Metrikani scanner va server tomoni hisoblaydi, gate esa tayyor raqamni chegara bilan solishtiradi. Shuning uchun gate natijasi analiz tugab, Compute Engine vazifasi `SUCCESS` bo'lgandan keyingina mavjud bo'ladi. Scanner tugashi gate tugashini bildirmaydi.

Shartlar odatda "New Code" (yangi kod) va "Overall Code" (butun kod) ko'rinishida ikkiga bo'linadi. Zamonaviy sozlamada deyarli barcha bloklovchi shart New Code ustida turadi. Buning sababi oddiy: eski texnik qarzni bir kechada to'lash mumkin emas, lekin yangi kod sifatini bugundan nazorat qilish mumkin.

## 6.2 Standart gate va uning shartlari

SonarQube o'rnatilganda `Sonar way` nomli gate built-in bo'lib keladi va yangi loyihalarga standart sifatida tayinlanadi. Uni tahrirlab bo'lmaydi, chunki u built-in. O'zgartirish kerak bo'lsa, nusxa olinadi va nusxa tahrirlanadi.

`Sonar way` tarkibi SonarQube liniyasiga qarab farq qiladi, buni e'tiborsiz qoldirmang. 9.9 LTA davrida u asosan reyting va foiz shartlaridan iborat edi: New Code uchun coverage kamida 80%, duplikatsiya 3% dan oshmasin, Reliability, Security va Maintainability reytingi A bo'lsin, Security Hotspots 100% ko'rib chiqilgan bo'lsin. Clean Code taksonomiyasi kirgandan keyin, 10.x va 2025 LTA liniyasida reyting shartlari o'rnini "yangi issue bo'lmasin" turidagi to'g'ridan to'g'ri shart egalladi. Aniq ro'yxatni har doim o'z serveringizdagi Quality Gates sahifasidan tekshirib oling, yodda saqlangan ro'yxatga ishonmang.

Amalda eng ko'p adashtiradigan shart coverage. 80% raqami butun loyiha uchun emas, New Code uchun qo'yiladi. Agar PR da 10 qator yangi kod bo'lsa va ulardan 2 qator test bilan qoplanmagan bo'lsa, New Code coverage 80% chiqadi va shart arang o'tadi. Yana bitta qoplanmagan qator PR ni failed qiladi. Kichik PR da coverage juda sezgir bo'ladi, bu normal hol.

## 6.3 Shart tuzilishi: metrika, operator, chegara qiymati

Har bir shart uchta elementdan yig'iladi. Birinchisi metrika kaliti, masalan `new_coverage` yoki `new_duplicated_lines_density`. Ikkinchisi operator: kichik, katta yoki teng emas. Uchinchisi chegara (threshold), ya'ni raqam yoki reyting darajasi.

Metrikaning yo'nalishi operatorni belgilaydi. Coverage uchun "yaxshi" yo'nalish yuqoriga, shuning uchun shart "chegaradan kichik bo'lsa failed" shaklida yoziladi. Duplikatsiya uchun yo'nalish pastga, shuning uchun shart "chegaradan katta bo'lsa failed" bo'ladi. UI da operator ko'pincha avtomatik tanlanadi, API orqali yozganda esa qo'lda beriladi.

```bash
# Gate shartlarini API orqali ko'rish va yangi shart qo'shish.
# Token bilan autentifikatsiya, parol bo'sh qoldiriladi.
export SONAR_HOST=https://sonar.company.uz
export SONAR_TOKEN=squ_xxxxxxxx

# 1) Mavjud gate va uning shartlari ro'yxati
curl -s -u "$SONAR_TOKEN:" \
  "$SONAR_HOST/api/qualitygates/show?name=Payment%20Gate" | jq '.conditions'

# 2) Yangi shart: New Code coverage 85% dan kam bo'lsa failed
curl -s -u "$SONAR_TOKEN:" -X POST \
  "$SONAR_HOST/api/qualitygates/create_condition" \
  -d "gateName=Payment Gate" \
  -d "metric=new_coverage" \
  -d "op=LT" \
  -d "error=85"

# 3) Shartni o'chirish uchun avval uning id sini olish kerak
# (show javobidagi conditions[].id qiymati ishlatiladi)
```

Reyting metrikalari raqam bilan kodlanadi: A uchun 1, B uchun 2 va shu tartibda. API ga `error=1` yuborilsa, bu "A dan yomon bo'lsa failed" degani. UI da buni harf ko'rinishida ko'rasiz, API da raqam sifatida. Shu nomuvofiqlik ko'p chalkashtiradi.

| Metrika turi | Yo'nalish | Odatiy operator | Chegara ko'rinishi |
|---|---|---|---|
| Coverage, condition coverage | Yuqoriga yaxshi | LT (kichik bo'lsa failed) | Foiz, masalan 80 |
| Duplikatsiya foizi | Pastga yaxshi | GT (katta bo'lsa failed) | Foiz, masalan 3 |
| Issue soni | Pastga yaxshi | GT | Butun son, masalan 0 |
| Reyting (A..E) | A eng yaxshi | GT | Raqam kodi, A uchun 1 |
| Security Hotspots Reviewed | Yuqoriga yaxshi | LT | Foiz, odatda 100 |

## 6.4 Gate holati: passed va failed, va u qachon hisoblanadi

Gate holati uch qiymatdan biri bo'ladi: `OK`, `ERROR` yoki `NONE`. `NONE` holati gate da hech qanday shart yo'qligini bildiradi, bu sozlash xatosi. Ko'pchilik UI da `Passed` va `Failed` so'zlarini ko'radi, API esa `OK` va `ERROR` qaytaradi. Skriptlarda API qiymatiga tayanish kerak.

Hisoblash ketma-ketligi quyidagicha. Scanner kodni analiz qiladi va natijani serverga yuboradi. Server navbatga Compute Engine vazifasini qo'yadi. Vazifa bajarilganda metrikalar saqlanadi va shundan keyin gate hisoblanadi. Ya'ni gate asinxron, scanner tugaganda hali javob yo'q.

```java
// Gate natijasini analizdan keyin olish uchun minimal klient.
// Bu kod CI yordamchi utilitasida ishlatiladi, ilova kodida emas.
public final class QualityGateClient {
    private static final HttpClient HTTP = HttpClient.newHttpClient();
    private final String baseUrl;
    private final String authHeader;

    public QualityGateClient(String baseUrl, String token) {
        this.baseUrl = Objects.requireNonNull(baseUrl, "baseUrl");
        // Token parol o'rnida keladi, parol qismi bo'sh qoldiriladi
        this.authHeader = "Basic " + Base64.getEncoder()
                .encodeToString((token + ":").getBytes(StandardCharsets.UTF_8));
    }

    /** Loyiha oxirgi analizi bo'yicha gate holati: OK yoki ERROR. */
    public String fetchStatus(String projectKey) throws IOException, InterruptedException {
        String url = baseUrl + "/api/qualitygates/project_status?projectKey="
                + URLEncoder.encode(projectKey, StandardCharsets.UTF_8);
        HttpRequest request = HttpRequest.newBuilder(URI.create(url))
                .header("Authorization", authHeader).GET().build();
        HttpResponse<String> response = HTTP.send(request, BodyHandlers.ofString());
        if (response.statusCode() != 200) {
            throw new IOException("Sonar API xatosi: " + response.statusCode());
        }
        return JsonPath.read(response.body(), "$.projectStatus.status");
    }
}
```

Bu klientni yozishdan oldin bitta savol bering: menga haqiqatan kerakmi. Ko'pincha kerak emas, chunki plugin buni o'zi qila oladi. Klient faqat natijani o'z dashboardingizga yozmoqchi bo'lsangiz asos bo'ladi.

## 6.5 Gate ni loyihaga tayinlash va bir nechta gate ni boshqarish

Har bir loyihada aynan bitta quality gate bo'ladi. Ikki gate ni bir loyihaga biriktirib bo'lmaydi. Agar ikki xil talab kerak bo'lsa, ikki gate ni birlashtirgan uchinchi gate yasaladi yoki loyiha ikkiga bo'linadi.

Tayinlash UI da loyiha sozlamalaridan yoki API orqali qilinadi. Yangi loyihalar standart deb belgilangan gate ni oladi. Katta tashkilotda eng barqaror yondashuv quyidagicha: 2 yoki 3 ta gate, har biri ma'lum sinfdagi servis uchun. Masalan to'lov va auth servislari uchun qattiqroq gate, ichki admin paneli uchun yumshoqroq gate, legacy monolit uchun faqat "yangi issue qo'shilmasin" turidagi minimal gate.

```bash
# Gate ni loyihaga tayinlash va standart gate ni o'rnatish.
# Ko'p loyihaga bir xil gate ni biriktirish uchun oddiy tsikl yetarli.

for KEY in uz.company:payment-api uz.company:billing-worker; do
  curl -s -u "$SONAR_TOKEN:" -X POST \
    "$SONAR_HOST/api/qualitygates/select" \
    -d "gateName=Critical Services Gate" \
    -d "projectKey=$KEY"
  echo "tayinlandi: $KEY"
done

# Yangi loyihalar uchun standart gate (ehtiyot bo'ling, global ta'sir qiladi)
curl -s -u "$SONAR_TOKEN:" -X POST \
  "$SONAR_HOST/api/qualitygates/set_as_default" \
  -d "name=Default Service Gate"
```

Gate sonini ko'paytirmang. Har bir qo'shimcha gate alohida kelishuv, alohida tarix va alohida tushunmovchilik manbasi. O'n beshta gate bo'lgan serverda hech kim qaysi loyihada qanday talab borligini bilmaydi.

## 6.6 Gate natijasini CI da olish: `sonar.qualitygate.wait` va uning ta'siri

Standart holatda scanner natijani yuboradi va darhol muvaffaqiyat bilan tugaydi. Gate failed bo'lsa ham build yashil qoladi. Bu eng ko'p uchraydigan yolg'on xavfsizlik hissi: pipeline da Sonar bosqichi bor, lekin u hech narsani bloklamaydi.

Buni `sonar.qualitygate.wait=true` parametri hal qiladi. U yoqilganda scanner Compute Engine vazifasi tugashini kutadi, gate holatini oladi va `ERROR` bo'lsa nolga teng bo'lmagan exit kod bilan tugaydi. Kutish vaqti `sonar.qualitygate.timeout` bilan boshqariladi va soniyada beriladi, standart qiymati 300 soniya atrofida.

```properties
# sonar-project.properties yoki CI dagi -D parametrlari
sonar.projectKey=uz.company:payment-api
sonar.projectName=Payment API

# Gate natijasini kutish: build gate failed bo'lsa yiqiladi
sonar.qualitygate.wait=true
# Kutish chegarasi soniyada; sekin serverda oshirish kerak bo'ladi
sonar.qualitygate.timeout=600

# Coverage hisoboti yo'li (JaCoCo 0.8.x XML hisoboti)
sonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml

# Generatsiya qilingan kodni analizdan chiqarish
sonar.exclusions=**/generated/**,**/*MapperImpl.java
# Coverage talabidan chiqarish, lekin issue tekshiruvini qoldirish
sonar.coverage.exclusions=**/config/**,**/*Application.java
```

`wait` ni yoqishning narxi bor. Build endi server navbatiga bog'liq bo'ladi. Navbat uzun bo'lsa pipeline kutadi, timeout urilsa build texnik sabab bilan yiqiladi, kod aybsiz bo'lsa ham. Shuning uchun `wait` ni PR pipeline da yoqish, tungi to'liq analizda esa o'chirish ko'pincha to'g'ri yechim.

```yaml
# GitHub Actions: PR da gate ni kutadi, main da esa kutmaydi.
name: build
on: [pull_request, push]
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0   # New Code hisoblash uchun to'liq tarix kerak
      - uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: '21'
      - name: Test va coverage
        run: ./mvnw -B clean verify
      - name: Sonar analiz
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
        run: >
          ./mvnw -B sonar:sonar
          -Dsonar.qualitygate.wait=${{ github.event_name == 'pull_request' }}
          -Dsonar.qualitygate.timeout=600
```

Maven da plugin versiyasini qo'lda qadab qo'yish kerak. Versiyasiz `sonar:sonar` chaqirish har safar boshqa plugin tortib kelishi mumkin va bu build ni takrorlanmas qiladi.

```xml
<!-- pom.xml: scanner va JaCoCo versiyalari qat'iy qadalgan -->
<build>
  <plugins>
    <plugin>
      <groupId>org.sonarsource.scanner.maven</groupId>
      <artifactId>sonar-maven-plugin</artifactId>
      <version>4.0.0.4121</version>
    </plugin>
    <plugin>
      <groupId>org.jacoco</groupId>
      <artifactId>jacoco-maven-plugin</artifactId>
      <version>0.8.12</version>
      <executions>
        <execution>
          <id>prepare</id>
          <goals><goal>prepare-agent</goal></goals>
        </execution>
        <execution>
          <!-- XML hisobot Sonar uchun majburiy, HTML faqat odam uchun -->
          <id>report</id>
          <phase>verify</phase>
          <goals><goal>report</goal></goals>
        </execution>
      </executions>
    </plugin>
  </plugins>
</build>
```

## 6.7 Gate failed bo'lganda build ni to'xtatish yoki ogohlantirish bilan cheklanish

Ikki siyosat bor va ikkisining ham o'z o'rni bor. Qattiq siyosat: gate failed bo'lsa PR merge qilinmaydi. Yumshoq siyosat: gate failed bo'lsa izoh yoziladi, lekin merge mumkin.

Qattiq siyosatni yoqishdan oldin bitta shart bajarilishi kerak: gate shartlari jamoa bilan kelishilgan va ular New Code ustida turgan bo'lishi kerak. Butun kod ustida qattiq shart bilan legacy loyihaga qattiq gate qo'yish ishni to'xtatadi, chunki birinchi PR muallifi 40 ming qatorlik qarzni to'lashi kerak bo'ladi.

Oraliq yondashuv ancha amaliy. Avval 4 yoki 6 hafta faqat ogohlantirish rejimida ishlatiladi. Shu davrda gate qancha PR ni yiqitgani o'lchanadi. Agar ko'rsatkich sabab bilan tushuntirilsa, siyosat qattiqlashtiriladi.

```sql
-- O'z CI metrikalar bazangizda gate natijalarini kuzatish.
-- Sonar bazasiga to'g'ridan to'g'ri SQL yozish qo'llanmaydi, shuning uchun
-- natija API orqali o'qilib, o'z jadvalingizga yoziladi.
CREATE TABLE ci_quality_gate_run (
    id            BIGSERIAL PRIMARY KEY,
    project_key   TEXT        NOT NULL,
    branch        TEXT        NOT NULL,
    status        TEXT        NOT NULL,   -- OK yoki ERROR
    failed_metric TEXT,                   -- birinchi buzilgan shart metrikasi
    analyzed_at   TIMESTAMPTZ NOT NULL
);

-- So'nggi 30 kunda qaysi shart eng ko'p bloklagan
SELECT failed_metric,
       COUNT(*) AS fail_count
FROM   ci_quality_gate_run
WHERE  status = 'ERROR'
  AND  analyzed_at >= now() - INTERVAL '30 days'
GROUP  BY failed_metric
ORDER  BY fail_count DESC;
```

Bu so'rovning javobi siyosatni tuzatish uchun asos beradi. Agar 90% yiqilish bitta shart sababli bo'lsa, demak o'sha shart noto'g'ri sozlangan yoki jamoada bilim bo'shlig'i bor.

## 6.8 Gate shartlarini tanlash mantiqi: nimani bloklash kerak, nimani kerak emas

Bloklash mezoni oddiy: shart buzilganda muallif nima qilishini bilsa, shart bloklovchi bo'lishi mumkin. Agar muallif "bu raqamni qanday tuzatishni bilmayman" desa, shart bloklamasligi kerak.

Bloklashga munosib bo'lgan narsalar: yangi kodda ishonchlilik va xavfsizlik muammolari, yangi kodda ko'rib chiqilmagan Security Hotspot, yangi kodda juda past coverage, yangi kodda ko'p nusxalangan blok. Bularning hammasi aniq va lokal: muallif o'z diff ida tuzatadi.

Bloklashga yaramaydigan narsalar: butun loyiha coverage i, butun loyiha texnik qarz vaqti, kod qatorlari soni, butun loyiha reytingi. Bular jamoa uchun ko'rsatkich, individual PR uchun jazo emas. Ularni gate ga qo'ysangiz, aybsiz odam jazolanadi.

| Shart | Bloklash | Sabab |
|---|---|---|
| New Code da yangi bug turidagi issue | Ha | Lokal, aniq, muallif tuzatadi |
| New Code coverage 80% dan past | Ha | Diff ga test yozish mumkin |
| New Code duplikatsiya 3% dan ko'p | Ha | Metodga ajratish yetarli |
| Ko'rib chiqilmagan Security Hotspot | Ha | Ko'rib chiqish bir necha daqiqa |
| Butun loyiha coverage 80% dan past | Yo'q | Eski qarz, PR muallifi aybdor emas |
| Butun loyihadagi code smell soni | Yo'q | Cheksiz katta, tuzatish chegarasi yo'q |
| Texnik qarz koeffitsiyenti (overall) | Yo'q | Taxminiy baho, aniq harakat bermaydi |
| Kod qatorlari soni | Yo'q | Sifat bilan bog'liq emas |

## 6.9 Juda qattiq gate ning ta'siri: chetlab o'tish yo'llari va jamoa xatti-harakati

Qattiqlik chegarasidan oshganda jamoa gate ni yengishni boshlaydi, sifatni oshirishni emas. Bu axloqiy muammo emas, tizim dizayni muammosi. Odamlar eng kam qarshilik yo'lidan boradi, va qattiq gate ko'pincha eng kam qarshilikni chetlab o'tishga qo'yadi.

Eng ko'p uchraydigan chetlab o'tish usullari quyidagilar. Birinchisi coverage ni soxta test bilan ko'tarish: metod chaqiriladi, lekin hech qanday assert yo'q. Ikkinchisi `sonar.coverage.exclusions` ga paket qo'shish. Uchinchisi issue ni "Won't fix" yoki "False positive" deb yopish, sababini o'ylab topib. To'rtinchisi kodga `@SuppressWarnings` yoki `// NOSONAR` yozish. Beshinchisi PR ni katta qilish: 10 qatorli PR da coverage shart juda sezgir, 2000 qatorli PR da o'rtacha raqam osonroq chiqadi.

```java
// Yomon kod: coverage ni ko'taradi, xatoni topmaydi.
@Test
void calculateTotal_works() {
    OrderService service = new OrderService(new InMemoryPriceRepo());
    service.calculateTotal(new Order("A-1", List.of(new Item("SKU-1", 2))));
    // Hech qanday assert yo'q: JaCoCo qatorni qoplangan deb belgilaydi,
    // lekin natija xato bo'lsa ham test yashil qoladi.
}

// Sonar o'tadigan va haqiqatan tekshiradigan variant.
@Test
void calculateTotal_appliesQuantityAndRoundsToTwoDecimals() {
    PriceRepo prices = sku -> new BigDecimal("19.99");
    OrderService service = new OrderService(prices);

    BigDecimal total = service.calculateTotal(
            new Order("A-1", List.of(new Item("SKU-1", 2))));

    // 19.99 * 2 = 39.98, yarim yuqoriga yaxlitlash bilan
    assertThat(total).isEqualByComparingTo(new BigDecimal("39.98"));
}
```

Assert siz testni Sonar ham ushlaydi: "test assertion ichida bo'lishi kerak" turidagi qoida mavjud. Lekin bu qoidani chetlab o'tish ham qiyin emas, masalan ma'nosiz `assertNotNull` yozib. Shuning uchun gate ni code review bilan juftlash kerak. Gate raqamni tekshiradi, odam ma'noni tekshiradi. Test sifatining o'zi alohida mavzu va u [testlash qo'llanmasidagi](../testing/README.md) test sifati va mutatsion test mavzularida ochiladi.

| Tuzoq | Nimaga olib keladi | Yechim |
|---|---|---|
| Overall coverage ni gate ga qo'yish | Legacy loyihada hamma PR yiqiladi | Faqat New Code coverage shartini qoldirish |
| `wait` ni yoqmaslik | Gate failed bo'lsa ham build yashil | PR pipeline da `sonar.qualitygate.wait=true` |
| `wait` ni yoqib timeout ni oshirmaslik | Navbat uzunda build sababsiz yiqiladi | `sonar.qualitygate.timeout` ni 600 ga ko'tarish |
| `fetch-depth: 1` bilan checkout | New Code chegarasi noto'g'ri, diff katta ko'rinadi | `fetch-depth: 0` va to'g'ri `newCodePeriod` |
| Coverage ni assert siz test bilan ko'tarish | Raqam yaxshi, xato ushlanmaydi | Review da assert talab qilish, mutatsion test |
| `// NOSONAR` ni erkin ishlatish | Qoida o'lik, sabab hech qayerda yozilmagan | `NOSONAR` ni review da sabab bilan talab qilish |
| Keng `coverage.exclusions` | Butun domen qatlami o'lchovdan chiqadi | Exclusion ni faqat DTO va config ga cheklash |
| 100% coverage shartini qo'yish | Trivial test ko'payadi, PR kattalashadi | Chegarani 80 yoki 85 da qoldirish |

Mana so'ralgan taqqoslash: standart shart va 100% ga sozlangan shart bir xil metrikada qanday boshqacha xulq berishini ko'rsatadi.

| Jihat | Standart gate sharti (New Code coverage < 80%) | 100% ga sozlangan gate sharti (New Code coverage < 100%) |
|---|---|---|
| Kichik PR da xulq | 10 qatorda 2 qator qoplanmasa ham o'tadi | Bitta qoplanmagan qator PR ni yiqitadi |
| Getter va DTO | Ularga test yozmaslik mumkin | Yoki test yoziladi, yoki exclusion qo'shiladi |
| Exception yo'llari | Asosiy yo'l qoplansa yetarli | Har bir catch bloki uchun test kerak |
| Jamoa xatti-harakati | Test mazmuniga e'tibor qoladi | Exclusion va assert siz test ko'payadi |
| Review yuklamasi | O'rtacha | Yuqori, chunki soxta testlarni ushlash kerak |
| Haqiqiy xato topish qobiliyati | Barqaror | Oshmaydi, ba'zan tushadi |
| Legacy kodga tegish | Mumkin, qarz sekin to'lanadi | Qo'rqinchli, shuning uchun refactoring to'xtaydi |
| Tavsiya | Standart holat sifatida qoldirish | Faqat kichik va kritik modulda, ongli ravishda |

## 6.10 Gate o'zgarganda tarixiy loyihalarga ta'siri

Gate shartini o'zgartirish retroaktiv emas. Eski analizlarning saqlangan holati qayta yozilmaydi. Lekin loyihaning hozirgi holati keyingi analizda darhol yangi shart bo'yicha baholanadi.

Shuning uchun gate ni qattiqlashtirishning real ta'siri shunday ko'rinadi: o'zgarishdan keyin birinchi PR yuborgan odam yangi shartni birinchi bo'lib yeb qoladi, garchi uning diff i avvalgi kundagidek bo'lsa ham. Bu jamoada adolatsizlik hissi tug'diradi va Sonar ga ishonchni buzadi.

To'g'ri tartib quyidagicha. Avval o'zgarishni e'lon qilish va kuchga kirish sanasini aytish. Keyin yangi shart bilan bir necha loyihada sinov o'tkazish, masalan nusxa gate da. Shundan keyingina real gate ni almashtirish. Va o'zgarishni gate tarixida qayd qilish, chunki metrika grafigidagi keskin sakrashni keyin tushuntirish kerak bo'ladi.

New Code chegarasini o'zgartirish ham shunga o'xshash ta'sir beradi. Agar chegara "oldingi versiya" dan "oxirgi 30 kun" ga ko'chirilsa, New Code hajmi keskin o'zgaradi va coverage foizi ham siljiydi. Kod o'zgarmagan bo'lsa ham gate holati o'zgarishi mumkin.

| Jihat | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Gate tanlash | Built-in `Sonar way` ni shundayligicha qoldirish | Servis sinfiga mos 2-3 gate, har birida sabab yozilgan |
| Shart chegarasi | "Qattiqroq bo'lsa yaxshiroq" deb 100% qo'yish | Chegarani jamoa real bajara oladigan darajada qo'yish |
| Shart doirasi | Overall Code ustiga shart qo'yish | Bloklovchi shartlarni faqat New Code ustida qoldirish |
| CI integratsiyasi | `sonar:sonar` chaqirib natijani o'qimaslik | `wait` va `timeout` ni muhitga qarab sozlash |
| Gate failed bo'lganda | Issue ni "Won't fix" qilib yopish | Sababni tahlil qilish, kod yoki shartni tuzatish |
| Coverage ni ko'tarish | Assert siz test yozib raqamni bo'yash | Xulqni tekshiradigan test, mutatsion test bilan nazorat |
| Exclusion siyosati | Yiqilgan paketni exclusions ga qo'shish | Exclusion ro'yxatini review qilinadigan artefakt deb qarash |
| Gate o'zgarishi | Kechqurun jim o'zgartirish | E'lon, sinov davri, kuchga kirish sanasi, qayd |
| Natijani kuzatish | Faqat UI ga qarash | Gate natijalarini o'z bazasiga yozib trend o'lchash |
| Muvaffaqiyat mezoni | Gate yashil | Production da incident soni va o'rtacha tuzatish vaqti |

## 6.11 Amalda qo'llash

- [ ] Serveringizdagi `Sonar way` gate shartlarini `api/qualitygates/show` orqali eksport qiling va haqiqiy ro'yxatni hujjatlashtirib qo'ying.
- [ ] Gate dagi barcha bloklovchi shartni tekshirib, Overall Code ustida turganlarini New Code ga ko'chiring.
- [ ] PR pipeline ga `sonar.qualitygate.wait=true` va `sonar.qualitygate.timeout=600` qo'shing, main branch da `wait` ni o'chirib qoldiring.
- [ ] CI checkout ini `fetch-depth: 0` ga o'tkazing va New Code chegarasi to'g'ri hisoblanayotganini bitta PR da tekshirib ko'ring.
- [ ] `sonar-maven-plugin` va `jacoco-maven-plugin` versiyalarini `pom.xml` da qat'iy qadab, build takrorlanadigan bo'lishini ta'minlang.
- [ ] Oxirgi 30 kundagi gate yiqilishlarini metrika bo'yicha guruhlab, eng ko'p bloklagan shartni aniqlang va u asoslimi degan savolga javob yozing.
- [ ] `sonar.coverage.exclusions` ro'yxatini qayta ko'rib chiqing va domen yoki servis qatlamiga tegadigan har bir qatorni olib tashlang.
- [ ] Gate ni qattiqlashtirish rejasini e'lon sanasi, sinov davri va kuchga kirish sanasi bilan yozib, jamoaga oldindan tarqating.

---

[&larr; 5. Metrikalar: rating, texnik qarz, murakkablik, takrorlanish](05-metrikalar-rating-texnik-qarz-murakkablik.md) · [Mundarija](README.md) · [7. Yangi kod (new code) va "clean as you code" tamoyili &rarr;](07-yangi-kod-new-code-va-clean-as-you-code.md)
