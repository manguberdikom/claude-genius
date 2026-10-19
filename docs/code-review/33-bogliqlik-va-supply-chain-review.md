<!-- doc: code-review | chapter: 33 | part: VI. Xavfsizlik review -->

[Barcha hujjatlar](../../README.md) / [Kod review](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 33. Bog'liqlik va supply chain review (Dependencies and Supply Chain)

<details>
<summary>Bu bobdagi 8 bo'lim</summary>

- [33.1 Yangi bog'liqlik uchun savollar](#331-yangi-bogliqlik-uchun-savollar)
- [33.2 Transitive bog'liqliklar va versiya konflikti](#332-transitive-bogliqliklar-va-versiya-konflikti)
- [33.3 Skanerlashni CI ga qo'yish](#333-skanerlashni-ci-ga-qoyish)
- [33.4 Versiya yangilash PR larini review qilish](#334-versiya-yangilash-pr-larini-review-qilish)
- [33.5 Build va CI ning o'zi](#335-build-va-ci-ning-ozi)
- [33.6 Review checklisti: bog'liqliklar](#336-review-checklisti-bogliqliklar)
- [33.7 Bog'liqlik shartnomasi: va'da, qadam va egalik](#337-bogliqlik-shartnomasi-vada-qadam-va-egalik)
- [33.8 Amalda qo'llash](#338-amalda-qollash)

</details>


`pom.xml` dagi bitta qator butun ilovaga kod qo'shadi - sizning kodingizdan ko'p bo'lishi mumkin. Shu sababli bog'liqlik o'zgarishi review da alohida e'tibor talab qiladi, lekin amalda u eng tez "LGTM" oladigan diff turi.

## 33.1 Yangi bog'liqlik uchun savollar

6.4 da arxitektura nuqtai nazaridan savollar berilgan; bu yerda xavfsizlik va yangilanish nuqtai nazari.

| Savol | Qanday tekshirish |
| --- | --- |
| Oxirgi reliz qachon | Maven Central yoki GitHub |
| Ma'lum CVE bormi | `dependency-check`, `osv-scanner` |
| Litsenziya mosmi | `license-maven-plugin` |
| Nechta transitive olib keladi | `dependency:tree` |
| Ishlab chiqaruvchisi kim | Jamoa yoki bitta odam |
| Nomi tanish paketga o'xshashmi | Typosquatting |
| Qancha kod uchun olinadi | 20 satr uchun kutubxona - savol |
| Alternativa JDK yoki Spring da bormi | Ko'pincha bor |

```bash
# Yangi bog'liqlik haqida ma'lumot to'plash: review izohi uchun dalil.
GROUP=com.example; ART=some-lib; VER=1.2.3

# 1) Oxirgi versiyalar va relizlar oralig'i.
curl -s "https://search.maven.org/solrsearch/select?q=g:$GROUP+AND+a:$ART&core=gav&rows=10&wt=json" \
  | jq -r '.response.docs[] | "\(.v)  \(.timestamp/1000 | todate)"'

# 2) Ma'lum zaifliklar (OSV - Google ning ochiq bazasi).
curl -s -X POST https://api.osv.dev/v1/query \
  -d "{\"package\":{\"ecosystem\":\"Maven\",\"name\":\"$GROUP:$ART\"},\"version\":\"$VER\"}" \
  | jq -r '.vulns[]? | "\(.id): \(.summary)"'

# 3) Nimani olib keladi.
./mvnw dependency:tree -Dincludes="$GROUP:$ART" -Dverbose

# 4) Haqiqiy o'zgarish: butun daraxt farqi (6.4 dagi usul).
```

## 33.2 Transitive bog'liqliklar va versiya konflikti

```bash
# Versiya konfliktlarini topish: Maven "eng yaqin g'olib" qoidasini
# ishlatadi, bu kutilmagan versiyaga olib kelishi mumkin.
./mvnw dependency:tree -Dverbose | grep -E 'omitted for conflict' | head -20

# Yakuniy versiyalarni ko'rish (haqiqatda nima ishlatiladi).
./mvnw dependency:list | grep -E 'jackson|netty|guava|commons' | sort -u

# Review diqqati: Spring Boot BOM versiyalarni boshqaradi. Qo'lda
# versiya ko'rsatish BOM ni chetlab o'tadi va mos kelmaslikka olib keladi.
```

```xml
<!-- Yomon: versiya qo'lda, BOM chetlab o'tilgan. -->
<dependency>
  <groupId>com.fasterxml.jackson.core</groupId>
  <artifactId>jackson-databind</artifactId>
  <version>2.15.0</version>            <!-- Boot boshqa versiya kutadi -->
</dependency>

<!-- Yaxshi: BOM boshqaradi. -->
<dependency>
  <groupId>com.fasterxml.jackson.core</groupId>
  <artifactId>jackson-databind</artifactId>
</dependency>

<!-- Agar aniq versiya kerak bo'lsa: sabab izoh bilan va BOM property orqali. -->
<properties>
  <!-- Izohda ikki narsa aniq bo'lishi kerak: SABAB va BOM dagi
       hozirgi qiymat. Ikkinchisini taxmin qilmaslik kerak, aks holda
       "ko'tarish" amalda PASAYTIRISH bo'lib chiqadi: masalan Boot 3.3
       Jackson 2.17.x ni, Boot 3.4 esa 2.18.x ni boshqaradi, demak
       Boot 3.4 da 2.17.1 yozish versiyani orqaga suradi. To'g'ri
       qiymatni Boot ning o'z BOM idan tekshirish kerak:
       `mvn help:evaluate -Dexpression=jackson-bom.version`.
       Boot keyingi minor ga o'tganda bu propertyni olib tashlash shart. -->
  <jackson-bom.version>2.18.2</jackson-bom.version>
</properties>
```

Ikki BOM import qilingan loyihada review da yana bitta savol paydo
bo'ladi: bir xil artifact ikkisida ham bo'lsa, qaysi biri g'olib. Maven
ning javobi "oxirgi so'z emas, birinchi so'z": import lar tartib bilan
o'qiladi va kalit allaqachon kiritilgan bo'lsa, keyingi import uni
ALMASHTIRMAYDI. Shuning uchun BOM lar tartibi ahamiyatli va uni
tasodifga qoldirmaslik kerak. To'g'ridan-to'g'ri yozilgan
`<dependencyManagement>` yozuvi esa import lardan oldin qo'yiladi, ya'ni
u har qanday BOM dan ustun turadi. Diffda yangi BOM import qilinganda
review savoli shu: u mavjud BOM dan oldin turadimi va qaysi versiyalarga
tegadi.

Uchinchi nozik joy scope da. `optional` deb belgilangan bog'liqlik
chuqur tranzitiv darajada umuman tortilmaydi, shuning uchun "tranzitiv
bog'liqlik hammasi keladi" degan taxmin to'g'ri emas. Shunga o'xshab
`provided` va `test` scope lari ham transitiv emas. Bu zaiflik
hisobotini o'qishda muhim: hisobotda ko'rinmagan artifact yo'q degani
emas, u boshqa scope da bo'lishi mumkin.

Maven Enforcer ning `requireUpperBoundDeps` qoidasi shu sohada eng
arzon himoya: u tanlangan versiya tranzitiv talab qilingan eng yuqori
versiyadan past bo'lsa build ni yiqitadi. Lekin uning qamrovini bilish
kerak: `test` va `provided` scope lari default bo'yicha chetlab
o'tiladi.

## 33.3 Skanerlashni CI ga qo'yish

```xml
<!-- OWASP Dependency-Check: ma'lum CVE larni topadi. -->
<plugin>
  <groupId>org.owasp</groupId>
  <artifactId>dependency-check-maven</artifactId>
  <configuration>
    <!-- DIQQAT: bu chegara "yangi" zaiflikni emas, MAVJUD har qanday
         zaiflikni tekshiradi. Default qiymat 11, ya'ni build hech
         qachon yiqilmaydi. 7.0 ga tushirish legacy loyihada birinchi
         yurishda darhol qizil beradi, shuning uchun avval suppression
         ro'yxatini tayyorlash kerak. -->
    <failBuildOnCVSS>7.0</failBuildOnCVSS>
    <suppressionFiles>
      <suppressionFile>.dependency-check-suppressions.xml</suppressionFile>
    </suppressionFiles>
    <!-- `<nvdApiKey>${env.NVD_API_KEY}</nvdApiKey>` YOZMANG: plugin
         javadoc i buni ogohlantiradi, chunki `mvn -X` bilan kalit
         standart chiqishga tushadi. To'g'ri shakl kalitni emas,
         o'zgaruvchi NOMINI beradi. -->
    <nvdApiKeyEnvironmentVariable>NVD_API_KEY</nvdApiKeyEnvironmentVariable>
  </configuration>
</plugin>
```

```xml
<!-- Suppression fayli - review ning muhim obyekti.
     Har bir suppression sabab va muddat bilan bo'lishi kerak. -->
<suppressions xmlns="https://jeremylong.github.io/DependencyCheck/dependency-suppression.1.4.xsd">
  <suppress until="2026-12-31Z">
    <notes>
      CVE-2026-1234: faqat XML parsing yo'lida, biz faqat JSON ishlatamiz.
      Muddat tugaganda topilma QAYTA PAYDO BO'LADI va build yiqilishi
      mumkin, shuning uchun bu sana taqvimga ham yozilgan.
      Tekshirilgan: 2026-10-04, PR #1423. Keyingi ko'rib chiqish: 2026-12-31.
    </notes>
    <packageUrl regex="true">^pkg:maven/com\.example/some-lib@.*$</packageUrl>
    <cve>CVE-2026-1234</cve>
  </suppress>
</suppressions>
<!-- Review qoidasi: izohsiz yoki `until` siz suppression qabul qilinmaydi.
     Aks holda suppression fayli "hammasini o'chirish" vositasiga aylanadi. -->
```

```bash
# Alternativa: osv-scanner. `--lockfile` hali ishlaydi, lekin v2 da
# kanonik shakl subcommand bilan.
osv-scanner scan source -r .

# SBOM yaratish: nima ishlatilayotganini hujjatlashtirish.
./mvnw org.cyclonedx:cyclonedx-maven-plugin:makeAggregateBom
# Natija: target/bom.json - incident paytida "bizda shu kutubxona bormi"
# savoliga tez javob beradi.
```

## 33.4 Versiya yangilash PR larini review qilish

Dependabot yoki Renovate yuborgan PR lar ko'pincha e'tiborsiz merge qilinadi. Ular uchun ham qoidalar kerak.

| Yangilanish turi | Review talabi |
| --- | --- |
| Patch (3.4.1 -> 3.4.2) | CI yashil bo'lsa yetarli |
| Minor (3.4 -> 3.5) | Reliz izohini o'qish, deprecation larni ko'rish |
| Major (3.x -> 4.x) | Migratsiya qo'llanmasi, alohida reja |
| Xavfsizlik yangilanishi | Tezkor, lekin CI majburiy |
| Transitive versiya o'zgarishi | `dependency:tree` farqini ko'rish |
| Build plugin yangilanishi | Lokalda `verify` o'tkazish |
| Paket nomi o'zgargan (masalan OpenPDF 2.4 dan 3.0 ga: `com.lowagie` -> `org.openpdf`) | Import larni almashtirish mexanik, lekin kompilyatsiya xatosi butun modulga tarqaladi; reliz izohini o'qib, alohida PR qilish |
| Kutubxona sinflari `AutoCloseable` bo'lib qolgan | Ishlatiladigan sinflarni `javap -cp <jar> <sinf>` bilan tekshirish: Sonar `java:S2093` va `java:S2095` shu sinf bilan ishlagan joylarni ko'rsatadi ([resurslarni yopish](../sonarqube/13-sonar-otadigan-kod-yozish-qoidalari.md#136-resurslarni-yopish-try-with-resources-va-yopilmagan-oqim)) |

```yaml
# Renovate konfiguratsiyasi: shovqinni kamaytirish va muhimini ajratish.
{
  "extends": ["config:recommended"],
  "packageRules": [
    {
      "description": "Patch yangilanishlarni avtomatik birlashtirish",
      "matchUpdateTypes": ["patch"],
      "automerge": true,
      "automergeType": "branch"
    },
    {
      "description": "Spring Boot va Java ni alohida ko'rish",
      "matchPackageNames": ["/^org\\.springframework/", "/^java/"],
      "automerge": false,
      "labels": ["needs-careful-review"]
    }
  ],
  "vulnerabilityAlerts": {
    "labels": ["security"],
    "automerge": false
  },
  "prConcurrentLimit": 5
}
```

Shu konfiguratsiyada ikkita tuzatish bor va ikkisi ham jimgina
ishlamaydigan sozlamalar edi.

Birinchi: `vulnerabilityAlerts` YUQORI DARAJADAGI obyekt, u
`packageRules` ichiga yozilmaydi. Renovate update larni tekislaganda
bu kalitni har bir update dan olib tashlaydi, shuning uchun qoida
ichida yozilgan `labels` va `automerge` hech qachon qo'llanmaydi.
Ya'ni xavfsizlik PR lari yorliqsiz kelib turadi va buni sezish qiyin.

Ikkinchi: `matchPackagePatterns` eskirgan. Renovate uni
`matchPackageNames` ga avtomatik ko'chiradi va naqshni `/.../` ichiga
o'raydi, lekin migratsiyaga tayanmaslik kerak: yangi yozuvda naqsh
aniq `/regex/` shaklida beriladi.

## 33.5 Build va CI ning o'zi

Supply chain xavfi faqat kutubxonalarda emas - build jarayonining o'zida ham.

| Xavf | Himoya |
| --- | --- |
| Pin qilinmagan GitHub Action | SHA bilan pin qilish (`uses: actions/checkout@<sha>`) |
| `curl | bash` build ichida | Tekshirilgan artefakt, checksum |
| Ishonchsiz Maven repozitoriy | Faqat Central va ichki Nexus |
| Secret ni CI logida chop etish | Masking, `echo` dan saqlanish |
| Fork dan kelgan PR da secret | `pull_request` (emas `pull_request_target`) |
| Build artefaktining imzosi yo'q | Sigstore, checksum |
| Konteyner bazasi tag bilan | Digest bilan pin qilish |
| `latest` tag | Aniq versiya |

Gradle da `gradle/verification-metadata.xml` bu himoyaning bir qismi, va u diffda to'rt joyda buziladi.

- `mavenLocal()` birinchi repo bo'lsa, lokal `~/.m2` dagi ichki kutubxona nusxasi registrdagidan farq qiladi: metadata lokal nusxaga qarab yoziladi, CI da esa registr nusxasi chiqib verification yiqiladi. Diffda `mavenLocal()` ni toraytirilgan holda talab qiling: `mavenLocal { content { includeModule("uz.mbabm", "internal-lib") } }`.
- `./gradlew --write-verification-metadata sha256 build` keshdan o'qilgan parent POM larni yozmaydi, metadata to'liq bo'lmay qoladi. Qayta yozish `--refresh-dependencies` bilan va ishlaydigan registr tokeni bilan bajariladi.
- `~/.gradle/gradle.properties` proyektdagi `gradle.properties` dan ustun. U yerdagi eskirgan registr tokeni 401 beradi, sababi esa proyekt fayliga qarab topilmaydi.
- Ichki kutubxonani bir xil versiya bilan qayta publish qilish checksum ni o'zgartiradi va verification ni buzadi. Tuzatish yangi versiya raqami, metadata ni qo'lda to'g'rilash emas.

Metadata fayli diffda o'zgargan bo'lsa, o'zgargan checksum uchun sabab so'raladi: yangi versiya, yoki o'sha versiyaning o'zgargan artefakti. Ikkinchisi bilan merge qilinmaydi.

```yaml
# GitHub Actions: xavfsizroq shakl.
jobs:
  build:
    permissions:
      # Default huquq enterprise, tashkilot yoki repozitoriya
      # sozlamasidan keladi, shuning uchun "standart: write" deb
      # taxmin qilmaslik kerak. Bu qator default nima bo'lishidan
      # qat'i nazar minimumni qo'yadi.
      contents: read
    steps:
      # SHA bilan pin: tag o'zgartirilishi mumkin, SHA - yo'q.
      - uses: actions/checkout@08eba0b27e820071cde6df949e0beb9ba4906955  # v4.3.0
      - uses: actions/setup-java@c5195efecf7bdfc987ee8bae7a71cb8b11521c00  # v4.7.1
        with:
          java-version: '21'
          distribution: 'temurin'
          cache: 'maven'
      - run: ./mvnw -B verify
```

```dockerfile
# Konteyner bazasini digest bilan pin qilish.
FROM eclipse-temurin:21-jre-alpine@sha256:abc123...
# Tag (`21-jre-alpine`) o'zgarishi mumkin - digest o'zgarmaydi.
# Review savoli: bu digest qachon yangilanadi va kim yangilaydi?

# Qo'shimcha review bandlari:
USER 10001                      # root emas
COPY --chown=10001:10001 target/app.jar /app/app.jar
# Ko'p qatlamli build: build vositalari yakuniy obrazda qolmaydi.
```

## 33.6 Review checklisti: bog'liqliklar

| Savol | Nega |
| --- | --- |
| Yangi bog'liqlik haqiqatan kerakmi | Hujum yuzasi va yangilanish yuki |
| CVE holati tekshirilganmi | Ma'lum zaiflik |
| Litsenziya mosmi | Huquqiy xavf |
| Versiya BOM orqali boshqariladimi | Mos kelmaslik |
| Qo'lda versiya ko'rsatilsa, sabab yozilganmi | Keyinchalik eskirib qoladi |
| Transitive o'zgarishlar ko'rilganmi | Yashirin yangilanish |
| Suppression lar sabab va muddat bilanmi | "Hammasini o'chirish" |
| GitHub Action lar SHA bilan pin qilinganmi | Supply chain |
| Konteyner bazasi digest bilanmi | Takrorlanuvchanlik |
| CI huquqlari minimalmi | Token o'g'irlanishi |
| SBOM yaratiladimi | Incidentda tez javob |

## 33.7 Bog'liqlik shartnomasi: va'da, qadam va egalik

33.2 va 33.4 mexanikani beradi: konfliktni topish, yangilash PR ini
qanday o'qish. Bu bo'lim jarayonning o'zi haqida, ya'ni versiya
raqamiga qancha ishonish mumkin va yangilash ishini kim bajaradi.

- **SemVer kafolat emas, baho.** Winters/Manshreck/Wright SemVer ni
  "odam bu o'zgarishni qanchalik xavfli deb biladi" degan yo'qotishli
  (lossy) qisqartma deb ataydi. Ikki tomondan noto'g'ri chiqadi.
  Kam himoya: patch va minor ham kuzatiladigan xulq orqali
  sindiradi, chunki Hyrum qonuni API sintaksisi bilan cheklanmaydi
  (log chiqishi formati, bog'liqlik import tartibi, "tartiblanmagan"
  oqimning tartibi). Ortiqcha cheklov: kutubxona ichidagi siz
  ishlatmaydigan funksiya buzilgani uchun major ko'tarilsa, SemVer
  yechuvchisi (SAT-solver) sizga yangilanishni man etadi, holbuki
  kod birga ishlar edi. Shuning uchun mosligning yagona haqiqiy
  dalili versiya raqami emas, iste'molchi testlari va CI natijasi.
  Review da bundan amaliy savol chiqadi: "patch, CI yashil" degan
  izoh yetarlimi, yoki bu kutubxonaning kuzatiladigan xulqiga
  tayanadigan joyimiz bormi.
- **Eng kichik qadam bilan ko'tarilish (minimum version selection).**
  Kitob Go ekotizimidan kelgan MVS yondashuvini ko'rsatadi: `liba`
  `libbase >= 1.7` desa, 1.8 mavjud bo'lsa ham avval aynan 1.7 ga
  o'tiladi. Sababi oddiy: `>= 1.7` deb yozilgan bo'lsa, `liba`
  muallifi aynan 1.7 bilan ishlagan, demak kamida shu juftlik bir
  marta birga sinalgan. Umumiy qoida: kelajakni aniq bilmaganda eng
  kichik qadamni tashlang va har qadamda testlarni yurgizing. Katta
  sakrash bir yillik ishni bir commitga yig'ishga o'xshaydi: xato
  chiqsa, uni qaysi qadam keltirganini ajratib bo'lmaydi. Java da
  bu Maven ning standart xulqi emas, shuning uchun Renovate yoki
  Dependabot da bir necha minor ni bitta PR ga qo'shmaslik va
  `separateMinorPatch` kabi sozlama bilan qadamni mayda ushlash
  kerak (ESLATMA: MVS Maven da o'rnatilgan qoida emas, kitob uni Go
  misolida tushuntiradi).
- **Diamond konflikti: oldinga, orqaga, keyin lokal patch.** 33.2
  konfliktni topishni beradi, yechish tartibi esa shunday. Birinchi
  va eng oson yo'l: konflikt keltirgan bog'liqliklarning birini
  oldinga yoki orqaga surib, mos keladigan juftlikni topish.
  Orqaga surish xavfsizlik yangilanishi majburlagan holatda yopiq
  yo'l, chunki zaif versiyaga qaytib bo'lmaydi. Ikkinchi yo'l:
  bog'liqlikni lokal patch qilish. Bu qiyin, chunki mos kelmaslik
  sababini na provayder, na iste'molchi biladi: `liba` muallifi
  hamon `libbase` v1 bilan to'g'ri ishlaydi, `libb` esa allaqachon
  v2 ga o'tgan, muammoni faqat ikkisini birga tortgan odam ko'radi.
  Java da shading (Maven Shade bilan paketni qayta nomlash) qisman
  yordam beradi: ikki versiyani yonma-yon joylashtirish mumkin,
  lekin ikki versiya o'rtasida tur uzatilsa (v1 dagi `Map` v2 ning
  API siga tushsa) yechim yo'q.
- **Ta'minotchi nimani va'da qilganini ochiq yozadi.** Bog'liqlik
  shartnoma: ikki tomonning ham huquqi va majburiyati bor. Kitob
  ta'minotchidan to'rt savolga ochiq javob talab qiladi: qancha
  moslik ko'zda tutilgan, qanday evolyutsiya kutiladi, o'zgarish
  qanday boshqariladi va reliz qancha vaqt qo'llab-quvvatlanadi.
  Kitobdagi qiyoslash: C++ standart kutubxonasi va Java deyarli
  cheksiz orqaga moslik (Java da eski JAR yangi versiyada ishlaydi),
  Go faqat manba mosligi, binar moslik yo'q, Abseil ABI ni
  va'da qilmaydi lekin buzuvchi API o'zgarishi bilan birga avtomatik
  refaktoring asbobini beradi, Boost esa versiyalar orasida umuman
  moslik va'da qilmaydi. Mashhur, lekin moslik va'dasi yo'q
  kutubxonani uzoq yashaydigan kodning tanasiga kiritish eng katta
  xavf. Review savoli: bu bog'liqlikning qo'llab-quvvatlash siyosati
  qayerda yozilgan va biz unga tayanamizmi.
- **Yetim va kritik bir vaqtda bo'lmasin.** Kitobning keysi: biror
  paket demo uchun kiritiladi, egasi uni yengil narsa deb biladi,
  keyin boshqa jamoa uni tizimning markaziga tortadi. To'g'ridan
  to'g'ri ishlatish o'smaydi, tranzitiv ishlatish o'sadi, egasi esa
  buni ko'rmaydi. Oradan vaqt o'tib zaiflik e'lon qilinadi: `OWNERS`
  faylini hech kim yangilamagan, asl ikki odam boshqa jamoada,
  minglab loyiha tranzitiv tayangan, va yangilash paketning butun
  tarixini bir sakrashda bosib o'tishi kerak. Qoida: egalik darajasi
  pastki chegarasini ko'tarish, muntazam yangilashni arzon qilish va
  paketning yetim hamda kritik bo'lishiga yo'l qo'ymaslik. Review da
  bu `CODEOWNERS` savoli: bu bog'liqlikni ko'targan PR da uni
  keyin kim ko'taradi degan javob bormi.
- **Kutubxonani qo'llab-quvvatlash rejasisiz chiqarmang.** Teskari
  tomon: siz bog'liqlik ishlab chiqarsangiz. Google ning 2006
  yildagi flags kutubxonasini ochiq chiqarishi kitobda nomuvaffaqiyat
  sifatida keltiriladi: ichki va tashqi nusxa asta-sekin ajralib
  ketdi, tashqi nusxaga mas'ul jamoa qolmadi va u qarovsiz qoldi.
  Kitobning xulosasi aniq: uzoq muddat qo'llab-quvvatlash rejasi va
  vakolati bo'lmasa, chiqarmang. Yana bir oqibat: "vaqt o'tgach
  hamma fork eskiradi", ya'ni ichki va tashqi nusxa ajralib ketishi
  injiniring samaradorligiga soliq bo'lib tushadi.

Shu yerdagi ikki qoida boshqa boblarga tegishli. Eskirish oynasini
kutubxona o'zgarish tezligiga qarab belgilash va eskirishni
majburlash jarayoni
[37.9](37-api-moslik-va-breaking-change-review.md#379-eskirish-jarayoni-advisory-compulsory-va-qaytmaslik)
da; versiya raqamini BOM bilan boshqarish mexanikasi
[patterns 22.32](../patterns/22-deployment-va-operatsion-patternlar.md#2232-semantik-versiyalash-va-bom-bilan-dependency-boshqarish-semantic-versioning--bom-dependency-management)
da.

## 33.8 Amalda qo'llash

- [ ] `dependency-check` yoki `osv-scanner` ni CI ga qo'shib, `failBuildOnCVSS` ni 7.0 ga qo'ying.
- [ ] Mavjud suppression larni ko'rib chiqib, izohi va `until` sanasi yo'qlarini tuzating yoki olib tashlang.
- [ ] CycloneDX bilan SBOM yaratishni build ga qo'shing va natijani artefakt sifatida saqlang.
- [ ] Qo'lda versiya ko'rsatilgan bog'liqliklarni toping va har biriga sabab izohini qo'shing yoki BOM ga qaytaring.
- [ ] `dependency:tree -Dverbose` bilan versiya konfliktlarini aniqlab, ro'yxat tuzing.
- [ ] Renovate yoki Dependabot ni sozlab, patch yangilanishlarni avtomatik, major larni alohida yorliq bilan qiling.
- [ ] Barcha GitHub Action larni SHA bilan pin qiling va workflow huquqlarini `contents: read` ga tushiring.
- [ ] Konteyner bazasini digest bilan pin qilib, uni yangilash jarayonini belgilang.
- [ ] Yangi bog'liqlik qo'shadigan PR lar uchun shablonga 8 savolli ro'yxatni kiriting.
- [ ] Har kritik bog'liqlik uchun `CODEOWNERS` da egani belgilang, shunda u yetim va kritik bir vaqtda bo'lmaydi.
- [ ] Yangilashni bir necha minor ni bitta PR ga yig'maydigan qilib sozlab, qadamni mayda ushlang.
- [ ] Asosiy bog'liqliklarning qo'llab-quvvatlash siyosatini (moslik turi va reliz muddati) bitta jadvalga yozib qo'ying.
- [ ] O'z kutubxonangizni chiqarishdan oldin uni kim va qancha vaqt qo'llab-quvvatlashini yozma qayd qiling.

## Manbalar

- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at
  Google*, O'Reilly, 2020, 21-bob ("Conflicting Requirements and
  Diamond Dependencies", "Compatibility Promises", "The Limitations of
  SemVer", "Minimum Version Selection", "Exporting Dependencies",
  "Dependency Management, In Theory") - 33.7 dagi SemVer ning
  yo'qotishli baho ekani va ikki tomonlama xatosi, eng kichik qadam
  bilan ko'tarilish asosi, diamond konfliktini yechish tartibi hamda
  shading ning chegarasi, ta'minotchidan talab qilinadigan to'rt
  savol va C++/Java, Go, Abseil, Boost qiyosi, paketning yetim va
  kritik bir vaqtda bo'lishi keysi, flags kutubxonasi misolidan
  chiqqan "qo'llab-quvvatlash rejasisiz chiqarmang" qoidasi. Bu
  nashrning qo'limizdagi nusxasida chop etilgan bet raqami yo'q,
  shuning uchun bob va bo'lim nomi ko'rsatilgan
- Apache Maven, `DefaultDependencyManagementImporter` va
  `DefaultDependencyManagementInjector`
  ([https://github.com/apache/maven/blob/maven-3.9.16/maven-model-builder/src/main/java/org/apache/maven/model/composition/DefaultDependencyManagementImporter.java](https://github.com/apache/maven/blob/maven-3.9.16/maven-model-builder/src/main/java/org/apache/maven/model/composition/DefaultDependencyManagementImporter.java),
  tag `maven-3.9.16`, Apache-2.0) - 33.2 dagi BOM import tartibi:
  birinchi import g'olib, to'g'ridan-to'g'ri yozuv import lardan ustun.
- Apache Maven Resolver, `NearestVersionSelector` va
  `OptionalDependencySelector`
  ([https://github.com/apache/maven-resolver/blob/maven-resolver-2.0.24/maven-resolver-util/src/main/java/org/eclipse/aether/util/graph/transformer/NearestVersionSelector.java](https://github.com/apache/maven-resolver/blob/maven-resolver-2.0.24/maven-resolver-util/src/main/java/org/eclipse/aether/util/graph/transformer/NearestVersionSelector.java),
  tag `maven-resolver-2.0.24`, Apache-2.0) - 33.2 dagi "eng yaqin
  g'olib" qoidasi va `optional` bog'liqlikning chuqur darajada
  tortilmasligi.
- Apache Maven Dependency Plugin va Dependency Tree
  ([https://github.com/apache/maven-dependency-tree/blob/maven-dependency-tree-3.3.0/src/main/java/org/apache/maven/shared/dependency/graph/internal/VerboseDependencyNode.java](https://github.com/apache/maven-dependency-tree/blob/maven-dependency-tree-3.3.0/src/main/java/org/apache/maven/shared/dependency/graph/internal/VerboseDependencyNode.java),
  tag `maven-dependency-tree-3.3.0`, Apache-2.0) - 33.2 dagi
  "omitted for conflict" matni va `tree`, `list` goal nomlari.
- Apache Maven Enforcer, `requireUpperBoundDeps`
  ([https://github.com/apache/maven-enforcer/blob/enforcer-3.6.3/enforcer-rules/src/site/apt/requireUpperBoundDeps.apt.vm](https://github.com/apache/maven-enforcer/blob/enforcer-3.6.3/enforcer-rules/src/site/apt/requireUpperBoundDeps.apt.vm),
  tag `enforcer-3.6.3`, Apache-2.0) - 33.2 dagi qoida va uning
  `test` bilan `provided` ni chetlab o'tishi.
- OWASP Dependency-Check Maven plugini
  ([https://github.com/dependency-check/DependencyCheck/blob/v13.0.0/maven/src/main/java/org/owasp/dependencycheck/maven/BaseDependencyCheckMojo.java](https://github.com/dependency-check/DependencyCheck/blob/v13.0.0/maven/src/main/java/org/owasp/dependencycheck/maven/BaseDependencyCheckMojo.java),
  tag `v13.0.0`, Apache-2.0) - 33.3 dagi `failBuildOnCVSS` ning mavjud
  zaiflikni tekshirishi va 11 lik default i, hamda `nvdApiKey` ni
  POM ga yozishning sir oqishi xavfi va
  `nvdApiKeyEnvironmentVariable` tavsiyasi.
- OWASP Dependency-Check, suppression sxemasi
  ([https://github.com/dependency-check/DependencyCheck/blob/v13.0.0/core/src/main/resources/schema/dependency-suppression.1.4.xsd](https://github.com/dependency-check/DependencyCheck/blob/v13.0.0/core/src/main/resources/schema/dependency-suppression.1.4.xsd),
  tag `v13.0.0`, Apache-2.0) - 33.3 dagi 1.4 namespace i va `until`
  semantikasi.
- Renovate
  ([https://github.com/renovatebot/renovate/blob/08cb221/docs/usage/configuration-options.md](https://github.com/renovatebot/renovate/blob/08cb221/docs/usage/configuration-options.md)
  va [`flatten.ts`](https://github.com/renovatebot/renovate/blob/08cb221/lib/workers/repository/updates/flatten.ts),
  commit `08cb221`, AGPL-3.0) - 33.4 dagi `vulnerabilityAlerts` ning
  yuqori darajadagi obyekt bo'lishi va `matchPackagePatterns` ning
  `matchPackageNames` ga migratsiyasi.
- OpenPDF, 3.0.0 changelog i
  ([https://github.com/LibrePDF/OpenPDF/blob/3.0.5/changelogs/3.0.0.md](https://github.com/LibrePDF/OpenPDF/blob/3.0.5/changelogs/3.0.0.md),
  tag `3.0.5`, MPL-2.0 yoki LGPL-2.1) - 33.4 dagi `com.lowagie` dan
  `org.openpdf` ga paket nomi o'zgarishi.
- GitHub Docs, workflow sintaksisi va `pull_request_target`
  ([https://github.com/github/docs/blob/53aac26/content/actions/reference/workflows-and-actions/workflow-syntax.md](https://github.com/github/docs/blob/53aac26/content/actions/reference/workflows-and-actions/workflow-syntax.md),
  commit `53aac26`, CC BY 4.0) - 33.5 dagi `GITHUB_TOKEN` default
  huquqining sozlamaga bog'liqligi va fork PR da `pull_request` ning
  read-only token berishi.
- Gradle, bog'liqlik verifikatsiyasi
  ([https://github.com/gradle/gradle/blob/v9.8.1/platforms/documentation/docs/src/docs/userguide/securing-builds/dependency_verification.adoc](https://github.com/gradle/gradle/blob/v9.8.1/platforms/documentation/docs/src/docs/userguide/securing-builds/dependency_verification.adoc),
  tag `v9.8.1`, Apache-2.0) - 33.5 dagi
  `--write-verification-metadata` va repozitoriya kontentini
  cheklash.
- CycloneDX Maven plugini va OSV Scanner
  ([https://github.com/CycloneDX/cyclonedx-maven-plugin/blob/2.4.1/src/main/java/org/cyclonedx/maven/CycloneDxAggregateMojo.java](https://github.com/CycloneDX/cyclonedx-maven-plugin/blob/2.4.1/src/main/java/org/cyclonedx/maven/CycloneDxAggregateMojo.java),
  tag `2.4.1`, Apache-2.0; va
  [osv-scanner README](https://github.com/google/osv-scanner/blob/v2.7.0/README.md),
  tag `v2.7.0`, Apache-2.0) - 33.3 dagi `makeAggregateBom` va
  `target/bom.json`, hamda `osv-scanner scan source` shakli.

---

[&larr; 32. Secret, maxfiy ma'lumot va kriptografiya review](32-secret-maxfiy-malumot-va-kriptografiya.md) · [Mundarija](README.md) · [34. Test to'liqligini review qilish &rarr;](34-test-toliqligini-review-qilish.md)
