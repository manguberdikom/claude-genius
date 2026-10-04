<!-- doc: testing | chapter: 17 | part:  -->

[Java Spring loyihasida testlash](../../README.md) / [Testlash qo'llanmasi](README.md)

# 17. Metrikalar va test yetukligi modeli (Metrics & Testing Maturity)

<details>
<summary>Bu bobdagi 14 bo'lim</summary>

- [17.1 Nimani o'lchash kerak va nega](#171-nimani-olchash-kerak-va-nega)
- [17.2 Sifat natijasi metrikalari (outcome)](#172-sifat-natijasi-metrikalari-outcome)
- [17.3 Jarayon metrikalari](#173-jarayon-metrikalari)
- [17.4 Test suite sog'ligi metrikalari](#174-test-suite-sogligi-metrikalari)
- [17.5 Coverage'ni to'g'ri ishlatish](#175-coverageni-togri-ishlatish)
- [17.6 Metrikalarni yig'ish va ko'rsatish](#176-metrikalarni-yigish-va-korsatish)
- [17.7 Ogohlantiruvchi belgilar (leading indicators)](#177-ogohlantiruvchi-belgilar-leading-indicators)
- [17.8 Test yetukligi modeli: besh daraja](#178-test-yetukligi-modeli-besh-daraja)
- [17.9 Nolga yaqin holatdan boshlash: 30/60/90 kunlik reja](#179-nolga-yaqin-holatdan-boshlash-306090-kunlik-reja)
- [17.10 Legacy kodga test yozish strategiyasi](#1710-legacy-kodga-test-yozish-strategiyasi)
- [17.11 Jamoani ishontirish va o'rgatish](#1711-jamoani-ishontirish-va-orgatish)
- [17.12 Byudjet va vaqt](#1712-byudjet-va-vaqt)
- [17.13 Anti-patternlar](#1713-anti-patternlar)
- [17.14 Arxitektor nazorat ro'yxati](#1714-arxitektor-nazorat-royxati)

</details>



Metrikalar testlash strategiyasining ko'zi: ular xavf qayerda to'planganini va qayerda biz shunchaki o'zimizni xotirjam qilayotganimizni ko'rsatadi. Bu bobda qaysi metrikalarni yig'ish, ularni qanday o'qish va ularni KPI'ga aylantirib buzib qo'ymaslik yo'llari ko'rib chiqiladi. Keyin testlash yetukligining besh darajali modeli beriladi: har bir daraja uchun belgilari, odatiy muammolari va yuqoriga chiqish qadamlari. Bobning so'nggi qismi amaliy: testlash deyarli yo'q loyihada 30, 60 va 90 kun ichida ishonchli asos qurish va legacy kodni testga ochish tartibi.

## 17.1 Nimani o'lchash kerak va nega

Metrika qaror qabul qilish uchun yig'iladi. Agar biror raqamga qarab hech qanday harakat qilmasak, uni yig'ish ortiqcha mehnat. Shuning uchun har bir metrikani kiritishdan oldin ikki savolga javob yozib qo'yish kerak: "bu raqam qanday o'zgarganda nima qilamiz?" va "qarorni kim qabul qiladi?". Masalan flake rate 2% dan oshsa, keyingi sprintda barqarorlashtirishga sig'im ajratiladi; change failure rate ikki hafta ketma-ket o'ssa, release jarayoni qayta ko'riladi.

Goodhart qonuni: metrika maqsadga aylansa, u metrika sifatida ishlashdan to'xtaydi. Coverage'ni jamoa KPI qilish o'rniga assertion'siz testlar, getter/setter testlari va `toString()` tekshiruvlari paydo bo'ladi - raqam o'sadi, xavf o'zgarmaydi. Bug soni bo'yicha baholash QA'ni mayda-chuyda defekt yozishga undaydi. Shu sababli arxitektor uchun amaliy qoida: outcome metrikalari (production'dagi sifat) maqsad bo'lishi mumkin, process va suite metrikalari esa faqat diagnostika - ularni shaxs yoki jamoa bahosiga bog'lamaslik kerak.

Ikkinchi qoida - metrikalar juftlikda o'qiladi: deploy chastotasi change failure rate bilan, coverage mutation score bilan. Yolg'iz raqam manipulyatsiyaga ochiq.

## 17.2 Sifat natijasi metrikalari (outcome)

Bular foydalanuvchi his qiladigan natijani o'lchaydi va boshqaruv bilan suhbatning asosiy tili bo'lishi kerak.

| Metrika | Ta'rifi | Yig'ish manbasi |
|---|---|---|
| Escaped defect | Production'ga chiqib ketgan va foydalanuvchi/monitoring topgan xato | Jira'da `found-in: production` maydoni yoki `escaped` label'i majburiy qilinadi |
| Defect escape rate | Escaped defect / (escaped + release oldidan topilgan) | Jira JQL hisoboti, release bo'yicha guruhlab |
| Production incident soni va og'irligi | Sev1/Sev2/Sev3 kesimida oylik soni | Incident tracker (PagerDuty, Opsgenie) yoki postmortem ro'yxati |
| Change failure rate | Deploy'larning qanchasi rollback/hotfix talab qilgani | CD quvuri yozuvlari + hotfix branch nomlash konvensiyasi |
| Failed deployment recovery time (MTTR) | Buzilgan deploy'dan tiklanishgacha o'tgan vaqt | Incident boshlanish/yopilish vaqtlari, deploy log'lari |
| Mijoz shikoyatlari | Support ticket'larning defektga tegishli ulushi | Support tizimi (Zendesk/Jira Service Management) kategoriyasi |
| SLO buzilishi | Error budget'ning sarflangan ulushi | Prometheus/Grafana SLO burn-rate panellari |

Eng muhim amaliy nuqta: escaped defect'ni to'g'ri yig'ish uchun "qaysi test darajasi bu xatoni tutishi kerak edi?" degan maydon kiritiladi (unit / integration / contract / e2e / umuman testlanmaydi). Shu bitta maydon chorakda bir marta tahlil qilinsa, test strategiyasini raqamga asoslab o'zgartirish mumkin bo'ladi: masalan escaped defect'larning yarmi integratsion chegarada bo'lsa, unit test yozishni ko'paytirish befoyda.

## 17.3 Jarayon metrikalari

Jarayon metrikalari jamoaning ishlash tezligi va qaytar aloqa sifatini ko'rsatadi. DORA to'rtligi (deployment frequency, lead time for changes, change failure rate, failed deployment recovery time) shu guruhning yadrosi: birinchi ikkitasi tezlik, qolgan ikkitasi barqarorlik. Ularni faqat birga o'qish kerak - tezlikni barqarorlik hisobiga oshirish hech narsa yutqazmagandek ko'rinadi, lekin escaped defect o'sadi.

Qo'shimcha jarayon metrikalari:

- **Lead time for changes** - commit'dan production'gacha; Git API va deploy yozuvlari bog'lab hisoblanadi.
- **PR feedback vaqti** - PR ochilishidan birinchi CI natijasigacha va birinchi review izohigacha. 10 daqiqadan oshsa, developer kontekstni yo'qotadi.
- **Test ishga tushish vaqti** - bosqichlar bo'yicha: unit, integratsion (Testcontainers), e2e. Har bir bosqich uchun p50 va p95.
- **Build muvaffaqiyat foizi** - asosiy branch'da yashil build ulushi. 90% dan past bo'lsa, quvur ishonchni yo'qotgan.
- **Flake rate** - qayta ishga tushirishda natijasi o'zgargan test ishga tushishlari ulushi.
- **Karantindagi testlar soni** - vaqtincha o'chirilgan testlar ro'yxatining uzunligi va o'rtacha yoshi.
- **Texnik qarz hajmi** - SonarQube'dagi remediation effort yoki `@Disabled` va `TODO: test` belgilarining soni.

## 17.4 Test suite sog'ligi metrikalari

Suite ham mahsulot: u eskiradi, sekinlashadi va ishonchni yo'qotadi. Shuning uchun uni alohida kuzatish kerak.

- Testlar soni darajalar bo'yicha (unit / slice / integration / contract / e2e) - piramida shakli buzilganini birinchi bo'lib shu ko'rsatadi.
- Eng sekin 20 test - JUnit 5 XML hisobotlaridan (`target/surefire-reports`) avtomatik ajratiladi, har haftada qayta hisoblanadi.
- Coverage: umumiy emas, **diff coverage** (yangi/o'zgargan qatorlar) va kritik modullar kesimidagi line/branch coverage.
- Mutation score - PIT (pitest) orqali, o'zgargan fayllarga cheklab.
- Assertion zichligi - test metodiga o'rtacha assertion soni; 0 ga yaqin testlar "ishga tushdi, demak ishlaydi" tipidagi bo'sh testlar.
- `@Disabled` / `@Ignore` testlar soni va ularning yoshi.
- Test kodining production kodiga nisbati - odatda 0.5-1.5 oralig'ida; 0.2 dan past bo'lsa testlash yetishmaydi, 3 dan yuqori bo'lsa takrorlanish yoki haddan ziyod e2e bor.

## 17.5 Coverage'ni to'g'ri ishlatish

"80% coverage" maqsadi ma'nosiz, chunki u xavfni emas, kod hajmini o'lchaydi: avtogeneratsiya qilingan DTO'lar va MapStruct mapper'lar raqamni oson ko'taradi, to'lov hisoblash yoki retry logikasi esa qoplanmagan qolishi mumkin. To'g'ri yondashuv uchta qoidadan iborat. Birinchi: darvoza butun loyihaga emas, **o'zgargan kodga** (diff/new code) qo'yiladi - SonarQube'da "new code" quality gate, JaCoCo + diff-cover bilan esa patch coverage. Ikkinchi: kritik modullar ro'yxati alohida ajratiladi va ular uchun branch coverage talab qilinadi. Uchinchi: coverage mutation score bilan birga o'qiladi - yuqori coverage va past mutation score aniq signal: testlar kodni ishga tushiradi, lekin hech narsa tekshirmaydi.

| Metrika | Nimani ko'rsatadi | Nimani ko'rsatmaydi |
|---|---|---|
| Line coverage | Qaysi qatorlar umuman ishga tushgani | Natija tekshirilganini, chegara holatlarini |
| Branch coverage | Shart tarmoqlarining bosilganini | Tarmoq ichidagi mantiq to'g'riligini |
| Diff coverage | Yangi kod testlanganini | Legacy qismdagi xavfni |
| Mutation score | Testlarning xatoni tuta olishini | Talab to'g'ri tushunilganini, performance'ni |
| Testlar soni | Suite hajmini | Sifatni, takrorlanishni |
| Test ishga tushish vaqti | Qaytar aloqa tezligini | Testlar nimani qoplaganini |
| Flake rate | Suite ishonchliligini | Production barqarorligini |

Qoplanmagan kritik yo'lni topish uchun amaliy usul: JaCoCo XML hisobotini incident/escaped defect ro'yxati bilan solishtirish. Oxirgi chorakda defekt chiqqan sinflar ro'yxatini olib, ularning branch coverage va mutation score'ini tekshirish - eng foydali test yozish joylari deyarli har doim shu kesishmada bo'ladi.

## 17.6 Metrikalarni yig'ish va ko'rsatish

Birinchi qadam - CI'dan chiqadigan artefaktlarni standartlashtirish: JUnit XML, JaCoCo XML, PIT hisoboti, test davomiyligi va build metadatasi (commit, branch, davomiylik, natija). Keyin eng arzon variant: CI job'i hisobotlarni parse qilib Prometheus Pushgateway'ga yozadi, Grafana esa dashboard sifatida ko'rsatadi. Test natijalarini odam o'qiydigan shaklda ko'rsatish uchun Allure yoki ReportPortal ishlatiladi: ikkisi ham test tarixini saqlaydi, ReportPortal qo'shimcha ravishda nosozliklarni avtomatik kategoriyalashga yordam beradi. Production tomondan Spring Boot Actuator va Micrometer orqali Prometheus'ga chiqadigan metrikalar SLO panellarini to'ldiradi.

Dashboard'da ko'pi bilan ikki ekran bo'lishi kerak: biri **tezlik va barqarorlik** (DORA to'rtligi), ikkinchisi **suite sog'ligi** (davomiylik trendi, flake rate, karantin, diff coverage, mutation score).

Haftalik sifat hisobotining namunasi (bir sahifadan oshmasligi kerak):

1. Oxirgi hafta: deploy soni, change failure rate, eng og'ir incident va uning sababi.
2. Escaped defect'lar: soni, qaysi modulda, qaysi test darajasi tutishi kerak edi.
3. Suite holati: build muvaffaqiyat foizi, p95 davomiylik, flake rate, karantindagi testlar o'zgarishi.
4. Diff coverage va mutation score o'rtachasi; darvoza buzilgan PR'lar soni.
5. Keyingi hafta uchun uchta aniq harakat va javobgar shaxslar.

## 17.7 Ogohlantiruvchi belgilar (leading indicators)

Outcome metrikalari kechikib keladi: escaped defect allaqachon mijozga tegib ketgan bo'ladi. Shu sababli oldindan ogohlantiruvchi belgilarni kuzatish kerak:

- **PR'larda test yo'qligi** - production kodi o'zgargan, test fayllari o'zgarmagan PR'lar ulushi o'sadi.
- **Kontekst sonining o'sishi** - har xil `@MockBean` va `@TestPropertySource` kombinatsiyalari ko'paysa, Spring kontekst cache ishlamay qoladi va build sekinlashadi.
- **Build vaqtining sekin o'sishi** - haftada 2-3% o'sish bir chorakda ikki barobarga aylanadi; trend chizig'i absolyut qiymatdan muhimroq.
- **Flake rate o'sishi** - jamoa "qayta ishga tushir" madaniyatiga o'tishdan oldingi oxirgi signal.
- **`@Disabled` sonining o'sishi** - qarz jim to'planayotganini ko'rsatadi.
- **Bitta modulda defektlarning to'planishi** - defektlarning katta qismi kichik modullar to'plamidan keladi; test va refaktoring sig'imi shu joyga yo'naltiriladi.

## 17.8 Test yetukligi modeli: besh daraja

| Daraja | Belgilari | Odatiy muammolar | Asosiy vositalar |
|---|---|---|---|
| 1. Tartibsiz qo'lda testlash | Testlar deyarli yo'q, release oldidan qo'lda tekshiruv, bilim bir-ikki odamda | Regressiya doimiy, release qo'rquvi, hotfix'lar ko'p | Qo'lda checklist, Jira |
| 2. Asosiy unit testlar va CI | CI har PR'da build va unit testlarni ishga tushiradi, coverage o'lchanadi | Testlar faqat oson joylarda, ko'p mock, integratsion xavf ochiq | JUnit 5, Mockito, Maven/Gradle, GitHub Actions |
| 3. Piramida va integratsion testlar | Darajalar ajratilgan, Testcontainers bilan real baza/broker, slice testlar | Suite sekinlashadi, flaky testlar paydo bo'ladi, kontekst ko'payadi | Testcontainers, `@SpringBootTest`, `@DataJpaTest`, WireMock |
| 4. Contract, performance va sifat darvozalari | Servislar orasida contract testlar, yuklama testlari CI'da, diff coverage va mutation darvozalari | Darvozalar bypass qilinadi, performance natijalari shovqinli | Spring Cloud Contract yoki Pact, Gatling/k6, JaCoCo, PIT, SonarQube |
| 5. Production'da testlash va uzluksiz tajriba | Feature flag, canary, SLO va error budget, chaos tajribalari, synthetic monitoring | Kuzatuvchanlik xarajati, tajribalarni boshqarish murakkabligi | Prometheus/Grafana, OpenTelemetry, feature flag platformasi, canary deploy |

Keyingi darajaga o'tish qadamlari:

**1 → 2:** CI quvurini o'rnatish va asosiy branch'ni himoyalash; build'ni 10 daqiqadan qisqa qilish; eng ko'p defekt chiqadigan 3 sinfga unit test yozish; coverage'ni o'lchashni yoqish (darvozasiz); har bug-fix bilan test talab qilish qoidasini kiritish.

**2 → 3:** test darajalarini Maven/Gradle profillariga ajratish; Testcontainers bilan real PostgreSQL/Kafka'ga o'tish; Spring test kontekstlarini birlashtirib cache'dan foydalanish; tashqi HTTP'ni WireMock bilan izolyatsiya qilish; eng sekin 20 testni har hafta ko'rib chiqish.

**3 → 4:** consumer-driven contract testlarni kiritish; diff coverage darvozasini yoqish; o'zgargan fayllar uchun mutation testlashni (PIT `scmMutationCoverage`) qo'shish; asosiy ikki-uch scenariyga yuklama testi va baseline; flaky testlar uchun karantin va SLA jarayoni.

**4 → 5:** feature flag bilan deploy va release'ni ajratish; canary va avtomatik rollback; SLO va error budget joriy qilish; muhim foydalanuvchi yo'llariga synthetic test; nazorat ostidagi fault injection tajribalari.

## 17.9 Nolga yaqin holatdan boshlash: 30/60/90 kunlik reja

| Davr | Maqsad | Aniq qadamlar | O'lchanadigan natija |
|---|---|---|---|
| 0-30 kun | Qaytar aloqani yoqish | CI quvuri (build + mavjud testlar), asosiy branch himoyasi, 5-10 smoke/e2e test eng muhim foydalanuvchi yo'llariga, JaCoCo hisobotini yoqish (darvozasiz), escaped defect yozuvini standartlashtirish | Har PR'da yashil build; build vaqti < 10 daqiqa; smoke testlar har deploy'da ishlaydi |
| 31-60 kun | Xavf joylarini qoplash | Git tarixi bo'yicha eng ko'p o'zgaradigan va defekt chiqadigan 3-5 modulni aniqlash va ularga unit + slice test yozish, Testcontainers bilan repository/integratsion testlar, WireMock bilan tashqi integratsiyalar, diff coverage darvozasini ogohlantirish rejimida yoqish | Kritik modullarda branch coverage o'sishi; diff coverage hisoboti har PR'da |
| 61-90 kun | Darvoza va barqarorlik | Diff coverage darvozasini majburiy qilish (masalan yangi kod uchun 70-80%), o'zgargan fayllarga PIT mutation tekshiruvi, contract testlar eng muhim servis chegarasida, flaky karantin jarayoni, haftalik sifat hisoboti | Change failure rate va escaped defect trendi pasayishi; flake rate < 1%; karantin ro'yxati qisqaruvi |

Muhim tartib: darvozani birinchi kuni majburiy qilish - eng tez-tez uchraydigan xato. Avval o'lchash, keyin ogohlantirish, oxirida bloklash.

Diff coverage va mutation darvozasining minimal konfiguratsiyasi:

```xml
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <version>0.8.12</version>
  <executions>
    <execution>
      <goals><goal>prepare-agent</goal></goals>
    </execution>
    <execution>
      <id>report</id>
      <phase>verify</phase>
      <goals><goal>report</goal></goals>
    </execution>
  </executions>
</plugin>
<plugin>
  <groupId>org.pitest</groupId>
  <artifactId>pitest-maven</artifactId>
  <version>1.17.0</version>
  <configuration>
    <targetClasses><param>com.acme.billing.*</param></targetClasses>
    <mutationThreshold>60</mutationThreshold>
    <withHistory>true</withHistory>
  </configuration>
</plugin>
```

```yaml
jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Build and test
        run: ./mvnw -B verify
      - name: Diff coverage gate
        run: |
          pip install diff-cover
          diff-cover target/site/jacoco/jacoco.xml \
            --compare-branch=origin/main \
            --fail-under=80 \
            --html-report diff-coverage.html
      - name: Mutation testing on changed files
        run: ./mvnw -B org.pitest:pitest-maven:scmMutationCoverage
```

## 17.10 Legacy kodga test yozish strategiyasi

Legacy kod - testlari yo'q kod. Michael Feathers'ning yondashuvi: avval mavjud xulq-atvorni **characterization test** bilan "muzlatish", keyin refaktoring qilish. Tartib qat'iy: (1) kodni o'zgartirmasdan test yozishga urinish; (2) agar iloji bo'lmasa, eng kam xavfli seam'ni ochish; (3) characterization test; (4) refaktoring; (5) yangi mantiqni testdan boshlab yozish.

Seam - xulqni kodni tahrir qilmasdan almashtirish mumkin bo'lgan nuqta. Spring loyihalarida eng ko'p ishlatiladigan uchta usul: **parameterize constructor** (`new` chaqiruvini konstruktorga chiqarish), **extract interface** (tashqi tizimga interfeys qo'yish) va **sprout method** (yangi mantiqni alohida, testlanadigan metodga chiqarish).

```java
// OLDIN: bog'liqlik ichida yaratilgan, test yozish imkonsiz
public class InvoiceService {
    private final SmtpMailer mailer = new SmtpMailer();
    private final TaxApiClient taxApi = new TaxApiClient("https://tax.prod");

    public BigDecimal finalize(Invoice invoice) {
        BigDecimal tax = taxApi.calculate(invoice.getTotal(), invoice.getCountry());
        mailer.send(invoice.getCustomerEmail(), "Invoice", tax.toString());
        return invoice.getTotal().add(tax);
    }
}

// KEYIN: extract interface + parameterize constructor
public class InvoiceService {
    private final Mailer mailer;
    private final TaxCalculator taxCalculator;

    public InvoiceService(Mailer mailer, TaxCalculator taxCalculator) {
        this.mailer = mailer;
        this.taxCalculator = taxCalculator;
    }

    public BigDecimal finalize(Invoice invoice) {
        BigDecimal tax = taxCalculator.calculate(invoice.getTotal(), invoice.getCountry());
        notifyCustomer(invoice, tax); // sprout method
        return invoice.getTotal().add(tax);
    }

    void notifyCustomer(Invoice invoice, BigDecimal tax) {
        mailer.send(invoice.getCustomerEmail(), "Invoice", tax.toString());
    }
}
```

Characterization test mavjud xulqni, hatto u g'alati bo'lsa ham, yozib oladi:

```java
@Test
void finalize_qaysi_summani_qaytarishini_yozib_olamiz() {
    TaxCalculator tax = (total, country) -> new BigDecimal("12.50");
    List<String> sent = new ArrayList<>();
    InvoiceService service = new InvoiceService(
            (to, subject, body) -> sent.add(to), tax);

    BigDecimal result = service.finalize(invoiceOf("100.00", "UZ", "a@b.uz"));

    assertThat(result).isEqualByComparingTo("112.50");
    assertThat(sent).containsExactly("a@b.uz");
}
```

Agar natija kutilganidan farq qilsa, testni "to'g'ri" qiymatga emas, **haqiqiy** qiymatga moslang va farqni alohida defekt sifatida yozib qo'ying: shu bosqichda maqsad xulqni saqlash, tuzatish emas.

## 17.11 Jamoani ishontirish va o'rgatish

Eng kuchli argument - incident bilan bog'lanish. Oxirgi uch-besh incidentni olib, har biri uchun "qanday test buni oldini olardi va u qancha vaqt oladi?" degan tahlil yozilsa, testlash mavhum qiymatdan konkret summaga aylanadi. Shundan keyin ichki standart yoziladi: qaysi kodga qanday daraja test majburiy, nima mock qilinadi, nima real (Testcontainers), test nomlash konvensiyasi, flaky test bilan nima qilinadi.

Madaniyat tomoni: PR review'da test ham ko'rib chiqiladi (assertion bormi, test nima deyilishini tushuntiradimi), haftada bir soat pair testing seansi o'tkaziladi, yangi a'zo onboarding'ida birinchi vazifa sifatida bitta kichik test yozib PR qiladi. Arxitektor uchun muhim: standartni hujjat sifatida emas, shablon va ishlaydigan misollar sifatida berish - jamoa o'qiganini emas, ko'chirganini takrorlaydi.

## 17.12 Byudjet va vaqt

Amaliy mo'ljal: feature ishlab chiqish vaqtining 20-30% testga ketadi va bu alohida "task" emas, Definition of Done qismi. Bundan tashqari test infratuzilmasiga (quvur, Testcontainers, hisobotlar, flaky bilan ishlash) har sprintda sig'imning 5-10% ajratish kerak - aks holda suite asta-sekin ishonchni yo'qotadi.

"Test uchun vaqt yo'q" argumentiga javob raqam bilan beriladi: bitta production incident'ning narxi (tekshirish + hotfix + release + mijoz ta'siri) odatda shu funksiyaga test yozish vaqtidan bir necha barobar yuqori. Investitsiya qaytimini ko'rsatish uchun eng yaxshi ko'rsatkichlar: change failure rate, MTTR va PR feedback vaqti - ularning yaxshilanishi to'g'ridan-to'g'ri ishlab chiqish tezligiga aylanadi.

## 17.13 Anti-patternlar

- **Coverage foizini jamoa KPI qilish** - assertion'siz testlar va sun'iy raqam o'sishi; o'rniga diff coverage + mutation score darvozasi.
- **QA'ni topilgan bug soni bo'yicha baholash** - mayda defektlar oqimi va jamoalar orasida qarama-qarshilik; o'rniga escaped defect va risk qoplanishi.
- **Test sonini maqsad qilish** - takrorlanuvchi, sekin va mo'rt suite; o'rniga xavf kesimida qoplanish.
- **Metrikani faqat boshqaruvga ko'rsatish uchun yig'ish** - dashboard chiroyli, qaror yo'q; har metrikaga javobgar va harakat chegarasi biriktirilishi kerak.
- **Darvozani darhol majburiy qilish** - bypass madaniyati tug'iladi; o'lchash → ko'rsatish → ogohlantirish → bloklash ketma-ketligiga rioya qiling.
- **Yolg'iz metrikaga qarab qaror qabul qilish** - tezlik va barqarorlikni, coverage va mutation'ni har doim juftlikda o'qing.

## 17.14 Arxitektor nazorat ro'yxati

- [ ] Har bir yig'ilayotgan metrika uchun "qanday o'zgarsa, nima qilamiz" qarori va javobgar shaxs yozilgan.
- [ ] Outcome metrikalari (escaped defect, change failure rate, MTTR, SLO buzilishi) muntazam yig'iladi va escaped defect'ga "qaysi test darajasi tutishi kerak edi" maydoni biriktirilgan.
- [ ] Coverage darvozasi butun loyihaga emas, diff/new code'ga qo'yilgan va mutation score bilan birga o'qiladi.
- [ ] Suite sog'ligi kuzatiladi: p95 davomiylik, flake rate, karantin ro'yxati, `@Disabled` soni, eng sekin 20 test.
- [ ] Leading indicator'lar (testsiz PR ulushi, build vaqti trendi, kontekst soni) dashboard'da bor va chegaralari belgilangan.
- [ ] Jamoaning hozirgi yetuklik darajasi aniqlangan va keyingi darajaga 3-5 ta konkret qadam rejaga kiritilgan.
- [ ] Legacy modullar uchun characterization test va seam ochish tartibi standart sifatida hujjatlangan.
- [ ] Test infratuzilmasiga har sprintda aniq sig'im (5-10%) ajratilgan va hech bir metrika shaxsiy KPI qilib qo'yilmagan.

---

[&larr; 16. Flaky testlar, test qarzi va test kodini saqlash](16-flaky-testlar-test-qarzi-va-test-kodini.md) · [Mundarija](README.md) · [18. Shablonlar, checklistlar va ma'lumotnoma &rarr;](18-shablonlar-checklistlar-va-malumotnoma.md)
