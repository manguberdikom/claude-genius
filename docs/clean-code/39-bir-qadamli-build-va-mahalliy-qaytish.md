<!-- doc: clean-code | chapter: 39 | part: XI. Kod bazasi va jarayon gigiyenasi -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 39. Bir qadamli build va mahalliy qaytish halqasi (One-Step Build)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

- [39.1 Build bitta buyruq bo'lsin](#391-build-bitta-buyruq-bolsin)
- [39.2 Test bitta buyruq bo'lsin](#392-test-bitta-buyruq-bolsin)
- [39.3 Takrorlanadigan build: versiya qotirish va wrapper](#393-takrorlanadigan-build-versiya-qotirish-va-wrapper)
- [39.4 Bog'liqlik gigiyenasi: BOM, scope, keraksizni o'chirish](#394-bogliqlik-gigiyenasi-bom-scope-keraksizni-ochirish)
- [39.5 Build fayli o'qilishi](#395-build-fayli-oqilishi)
- [39.6 Generatsiya qilingan kodni ajratish](#396-generatsiya-qilingan-kodni-ajratish)
- [39.7 Mahalliy tez qaytish halqasi](#397-mahalliy-tez-qaytish-halqasi)
- [39.8 `.gitignore`, sir va konfiguratsiya fayllari](#398-gitignore-sir-va-konfiguratsiya-fayllari)
- [39.9 IDE qobiliyatlari: bir tugmali ishga tushirish, test va debug](#399-ide-qobiliyatlari-bir-tugmali-ishga-tushirish-test-va-debug)
- [39.10 Debug yordamchilarini rejali olib tashlash](#3910-debug-yordamchilarini-rejali-olib-tashlash)
- [39.11 Amalda qo'llash](#3911-amalda-qollash)

</details>


Toza kod faqat fayllar ichida emas: kod bazasining atrofidagi mexanika ham o'qilishi va ishonchli bo'lishi kerak. Bu bobda build, bog'liqliklar va mahalliy qaytish halqasining gigiyenasi. CI/CD test pipeline i [testlash qo'llanmasidagi](../testing/README.md) CI/CD test pipeline bo'limida, Sonar ulanishi [SonarQube hujjatidagi](../sonarqube/README.md) JaCoCo ni ulash bo'limida.

## 39.1 Build bitta buyruq bo'lsin

Evristika E1 (34.2) aniq talab qo'yadi: `git clone` dan keyin bitta buyruq butun loyihani qurishi kerak. Har bir qo'shimcha qadam - qo'lda o'rnatiladigan vosita, tahrirlanishi kerak bo'lgan fayl, maxfiy bilim - yangi odamning birinchi kunini yo'qotadi va avtomatlashtirishni to'sadi.

```bash
# Maqsad: shu uchta buyruq yetarli bo'lsin
git clone git@github.com:shop/payment.git
cd payment
./mvnw verify          # yoki ./gradlew build
```

Buni ta'minlash uchun: wrapper (`mvnw`, `gradlew`) repoda, JDK versiyasi `.sdkmanrc` yoki `.tool-versions` da, Docker kerak bo'lsa `compose.yml` repoda, va hech qanday qo'lda sozlash yo'q.

**Har build oldidan `clean` qilish odati alomat.** Google ning build tizimlari bo'yicha tahlilida bu aniq tashxis bilan ko'rsatilgan: muhandislar odat sifatida har buildan oldin `clean` ni bajara boshlasa, demak inkremental build ishonchsiz va ular bunga ishonmay qo'ygan. Sabab topshiriqqa asoslangan (task-based) build tizimlarining tuzilishida: topshiriq istalgan ishni bajarishi mumkin, shuning uchun tizim uning allaqachon bajarilganini umumiy holda tekshira olmaydi. Muhandis qayta ishga tushirish shartini qo'lda yozganda esa qisqa yo'l tanlanadi (masalan C++ da `#include` grafini parse qilmasdan faylni kuzatish ro'yxatini taxmin qilish), va natijada ba'zan natija qayta ishlatilmasligi kerak joyda ishlatiladi.

Qoida: **qaysi qadam qayta ishlashi kerakligini build tizimi o'zi aniqlashi kerak**, odam emas; bu ish mashinaga mos va odamga kutilganidan ancha nozik. Shuning uchun `./mvnw clean verify` ni standart buyruq qilib qo'yish qisqa muddatda qulay, uzoq muddatda esa inkremental build ning butun ma'nosini yo'qotadi. Muqobili: Gradle ning input va output e'lonlari bilan task larni to'g'ri yozish, `--build-cache` yoqish va `clean` ni faqat build tizimi xatosi tasdiqlanganda ishlatish.

```bash
# Alomat: odat bo'lgan clean
./mvnw clean verify          # har marta nolidan

# Maqsad: inkremental ishonchli, clean istisno
./mvnw verify
./gradlew build --build-cache
```

## 39.2 Test bitta buyruq bo'lsin

Evristika E2: testni ishga tushirish ham bir buyruq bo'lishi kerak va u hech qanday tashqi sozlama talab qilmasligi lozim. Testcontainers shu talabni bajaradi: baza va Kafka test paytida avtomatik ko'tariladi ([testlash qo'llanmasidagi](../testing/README.md) Testcontainers bo'limi).

```bash
./mvnw test              # unit testlar, soniyalar
./mvnw verify            # integratsion testlar ham, Testcontainers bilan
```

Agar testni ishga tushirish uchun mahalliy PostgreSQL o'rnatish yoki `application-local.yml` ni tahrirlash kerak bo'lsa, E2 buzilgan.

## 39.3 Takrorlanadigan build: versiya qotirish va wrapper

Build takrorlanadigan bo'lishi kerak: bir xil commit bir xil natija bersin. Buni buzadigan narsalarni jadvalga yig'dik, va ularning hammasini yopish mumkin.

**Repozitoriylar orasidagi bog'liqlik esa qotirilmaydi.** Ichki bog'liqlikni versiyaga qotirish bitta repozitoriy ichida to'g'ri, lekin tashkilot bir nechta repozitoriyga bo'lingan bo'lsa, ular orasidagi bog'liqlikni qotirish boshqa muammo keltiradi: har repozitoriy qaysi versiyaga tayanishini o'zi tanlaydi va shunda bitta komponentning bir nechta versiyasi bir vaqtda yashaydi. Google ning tavsiyasi: repozitoriylarni ajratish qarori qabul qilingan bo'lsa ham, **repozitoriylar orasidagi bog'liqlik qotirilmagan, ya'ni trunk bo'yicha ("at head") bo'lishi ma'qul**, va tashkilot bo'yicha yagona virtual trunk tushunchasi saqlanadi. VCS va build tizimlarida bunga imkon beradigan vositalar ko'payib bormoqda (Google ning o'zi bu sohada hali hech narsa silliq ishlayotganini ko'rmaganini aytadi).

Amaliy tarjimasi: ichki kutubxonalarning reliz versiyasini har iste'molchi alohida tanlaydigan model qarz yig'adi, chunki yangilanish har iste'molchi uchun alohida ish bo'lib qoladi. Muqobili - ichki kutubxonani SNAPSHOT emas, lekin **markaziy BOM** orqali bitta joydan boshqarish va BOM ni muntazam oldinga surish, yoki Gradle ning composite build (`includeBuild`) mexanizmi bilan manbadan qurish.

"Bir xil natija" iborasining ikki darajasi bor va ularni ajratish kerak. Birinchi daraja: build bir xil ishlaydi va bir xil testlardan o'tadi. Pastdagi jadval shu darajani ta'minlaydi. Ikkinchi daraja kuchliroq: chiqqan artifact BAYTGA BAYT bir xil bo'ladi (reproducible build). Ikkinchisi birinchisidan o'z-o'zidan kelib chiqmaydi, chunki JAR ichidagi yozuvlarning vaqt belgisi har build da o'zgaradi.

| Buzuvchi | Yechim |
|---|---|
| Vosita versiyasi mahalliy | Maven/Gradle wrapper repoda |
| JDK versiyasi mahalliy | `.sdkmanrc`, `maven.compiler.release` |
| Bog'liqlik versiyasi ochiq (`LATEST`, `+`) | aniq versiya yoki BOM |
| Snapshot bog'liqligi | reliz versiyasiga o'tish |
| Build vaqtidagi tashqi so'rov | kerakli fayllarni repoda saqlash |
| Plagin versiyasi ko'rsatilmagan | har bir plagin versiyasini yozish |
| Artifact ichidagi vaqt belgisi har build da boshqa | `project.build.outputTimestamp` |

Baytga bayt takrorlanishni yoqish uchun Maven da bitta property yetarli. Maven hujjati tartibni shunday beradi: avval `mvn artifact:check-buildplan` bilan plaginlarni ko'tarish kerakligini tekshirish, keyin property ni qo'yish.

```xml
<properties>
  <!-- Reproducible Builds rejimi: JAR ichidagi yozuvlar shu vaqt
       belgisini oladi, demak ikki build bayt-baytga teng chiqadi.
       Maven 3.10.0 va 4.0.0-beta-5 dan boshlab bu rejim default
       yoqilgan, lekin property ni yozish default qiymatni
       almashtirish uchun foydali qoladi. -->
  <project.build.outputTimestamp>2026-01-01T00:00:00Z</project.build.outputTimestamp>
</properties>
```

Takrorlanishni tekshirish ham bitta buyruq bilan bo'ladi:

```bash
# 1) Loyihani build qilib lokal repoga o'rnatish
mvn clean install

# 2) Qayta build qilib, oldingi natija bilan solishtirish
mvn clean verify artifact:compare
```

Bu lokal tekshiruv to'liq dalil emas: u muhit oqishini (foydalanuvchi nomi, joriy katalog) ushlamaydi, shuning uchun haqiqiy takrorlanishni butunlay boshqa muhitda qayta build qilib tekshirish kerak. Lekin u arzon va vaqt belgisi kabi oddiy sabablarni darhol topadi.

```xml
<!-- Versiyalar bir joyda, BOM bilan boshqariladi -->
<dependencyManagement>
  <dependencies>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-dependencies</artifactId>
      <version>${spring-boot.version}</version>
      <type>pom</type>
      <scope>import</scope>
    </dependency>
  </dependencies>
</dependencyManagement>
```

## 39.4 Bog'liqlik gigiyenasi: BOM, scope, keraksizni o'chirish

Bog'liqlik qo'shishning yashirin narxi [arxitektor hujjatidagi](../architect/README.md) bog'liqlik qo'shishning yashirin narxi bo'limida. Bu yerda kod bazasi darajasidagi qoidalar: versiyalar bir joyda, `scope` to'g'ri, va ishlatilmaydigan bog'liqliklar o'chirilgan.

```bash
# Ishlatilmaydigan va e'lon qilinmagan bog'liqliklarni topish
./mvnw dependency:analyze

# Bog'liqlik daraxti: takrorlangan va konflikt versiyalar
./mvnw dependency:tree -Dverbose | grep -E 'omitted|conflict'

# Gradle da
./gradlew dependencies --configuration runtimeClasspath
```

| `scope` | Qachon |
|---|---|
| `compile` (standart) | kodda ishlatiladi |
| `runtime` | faqat ish vaqtida kerak (JDBC drayveri) |
| `provided` | konteyner beradi |
| `test` | faqat testda |
| `import` | BOM |

Eng ko'p uchraydigan xato: test kutubxonasini (`assertj`, `mockito`) `compile` scope da qoldirish - u production jar ga tushadi.

**Umumiy kutubxonaning nomini o'zgartirmagan forki taqiqlanadi.** Jamoa umumiy infratuzilma kutubxonasida (masalan Guava yoki ichki `commons`) xato topib, uni joyida tuzatish o'rniga fork qilsa va kutubxona hamda uning simvollari nomini o'zgartirmasa, kod bazasiga ko'rinmaydigan bo'linish kiradi: istalgan maqsadning tranzitiv bog'liqlik to'plamida shu kutubxonaning **aniq bitta** nusxasi bo'lishi shart. Ikki tomon birlashganda eng yaxshi holatda build yiqiladi, eng yomon holatda mos kelmagan ikki versiya bir binar ichida linklanib tushunib bo'lmaydigan runtime xatolari beradi. Oqibati masshtab bo'yicha yomon: "yangi bog'liqlik qo'shish" kabi oddiy amal shu bo'linish buzilmaganini tekshirish uchun butun kod bazasi testlarini yurgizishni talab qilib qoladi.

**Shading muammoni yashiradi.** Java da shading - kutubxonaning ichki bog'liqliklari nomini o'zgartirib ularni ilovaning qolgan qismidan yashirish - standartga yaqin amaliyot. Funksiyalar uchun bu texnik jihatdan asosli, garchi nazariy jihatdan hiyla bo'lsa ham. Lekin bir paketdan ikkinchisiga uzatiladigan **turlar** uchun shading na nazariyada, na amalda ishlaydi: lug'at turi (vocabulary type) yoki undan yuqori konstruksiya beradigan kutubxonaning bir nechta versiyasi yiqiladi. Shading va shunga o'xshash yondashuvlar asosiy muammoni, ya'ni bitta bog'liqlikning bir nechta versiyasi kerak bo'lib qolganini, yamaydi.

Amaliy qoida:

- Xatoni **joyida tuzatish** va yuqoriga (upstream) yuborish birinchi tanlov.
- Fork zarur bo'lsa, u **qayta nomlanadi**: `groupId`, paket nomi va simvollar o'zgaradi, shunda ikki nusxa bir binarda tinch yashaydi.
- `maven-shade-plugin` bilan relocation faqat funksiyalar uchun ishlaydigan vaqtinchalik chora deb qaraladi va uning muddati yoziladi.

```xml
<!-- Fork qayta nomlanadi, shunda ikki nusxa to'qnashmaydi -->
<groupId>uz.shop.forked.guava</groupId>
<artifactId>guava-shop</artifactId>
```

## 39.5 Build fayli o'qilishi

`pom.xml` va `build.gradle` ham kod va ular ham o'qilishi kerak. Qoidalar: xususiyatlar (`<properties>`) yuqorida va versiyalar shu yerda, bog'liqliklar guruhlangan va saralangan, plaginlar sozlamalari izohlangan.

```xml
<properties>
  <java.version>21</java.version>
  <!-- Versiyalar bir joyda: yangilash uchun bitta fayl tahrirlanadi -->
  <spring-boot.version>3.5.6</spring-boot.version>
  <testcontainers.version>1.21.3</testcontainers.version>
  <spotless.version>2.46.1</spotless.version>
</properties>
```

Spotless `sortPom` (13.3) `pom.xml` ni avtomatik tartiblaydi va diff shovqinini yo'qotadi.

**Build tizimini almashtirish qarori: og'riq bormi.** Build fayli o'qilmaydigan bo'lsa birinchi savol "boshqa build tizimiga ko'chamizmi" bo'lmasligi kerak. Google ning xulosasi aniq: mavjud build tizimidan boshqasiga ko'chish katta loyihada qimmat, va loyiha allaqachon **tezlik yoki to'g'rilik** muammosini ko'rsatmayotgan bo'lsa, ko'chish o'zini oqlamaydi. Qo'lda yozilgan skriptlar faqat eng kichik loyihalarga va uzoq vaqt o'zgarmaydigan kodga yaraydi; topshiriqqa asoslangan tizim (Maven, Gradle) masshtablanishni sezilarli yaxshilaydi, narxi - build tuzilishi haqida o'ylash va build fayllarini yozish; artefaktga asoslangan tizim (Bazel) buildni ko'p mashinaga taqsimlash va takrorlanuvchanlikni beradi, narxi - moslashuvchanlikning yo'qolishi, chunki tizim chegarasida ishlash shart.

Shundan ikki amaliy qoida:

- **Yangi loyihada** build tizimi boshidan ongli tanlanadi, chunki keyin ko'chish qimmat.
- **Mavjud loyihada** ko'chish faqat o'lchangan og'riq bilan asoslanadi: build vaqti byudjetdan chiqdi (39.7), yoki inkremental build ishonchsiz bo'lib `clean` odatga aylandi (39.1). Aks holda to'g'ri ish - mavjud build faylini tartibga keltirish va keshni yoqish.

## 39.6 Generatsiya qilingan kodni ajratish

Generatsiya qilingan kod `target/generated-sources` yoki `build/generated` ichida turadi, `src/` da emas, va `git` ga tushmaydi. Sababi: u har build da qayta yaratiladi, uni tahrirlash ma'nosiz, va u diff ni to'ldiradi.

```gitignore
target/
build/
*.class
# Generatsiya qilingan kod git ga tushmaydi
src/main/generated/
```

Agar generator vositasi `src/` ga yozsa, uning sozlamasini o'zgartirish kerak; imkonsiz bo'lsa, shu papkani formatlash, statik tahlil va coverage dan chiqarish lozim (13.8 va [SonarQube hujjatidagi](../sonarqube/README.md) Lombok va generatsiya qilingan kod bo'limi).

## 39.7 Mahalliy tez qaytish halqasi

Qaytish halqasining uzunligi ishlab chiqish tezligini belgilaydi. Pastdagi jadvaldagi vaqtlar o'lchov emas, JAMOA BYUDJETI: ular loyiha hajmiga, apparatga va test turiga qarab o'zgaradi. Jadvalning foydasi aniq raqamda emas, tartibda: kompilyatsiya sekundlarda, bir modul testlari sekundlar ichida, integratsion testlar daqiqalarda, butun build esa diqqatni yo'qotmaslik uchun o'n daqiqalar oralig'ida qolishi kerak. O'z byudjetingizni o'lchab yozing va buzilganda sababini qidiring.

| Halqa | Byudjet (jamoa kelishuvi) | Vositalar |
|---|---|---|
| Kompilyatsiya | < 5 s | incremental build, IDE |
| Unit testlar (bir modul) | < 10 s | tez testlar, mocksiz domen |
| Formatlash va lint | < 5 s | pre-commit hook (13.5) |
| Masofaviy kesh urishi | < 1 s/artefakt | `--build-cache`, Gradle yoki Bazel remote cache |
| Integratsion testlar | < 2 min | Testcontainers qayta ishlatish |
| Butun build | < 10 min | parallel modul, test teg |
| CI pipeline | < 15 min | keshlash, parallel job |

Konteynerni qayta ishlatish integratsion test halqasini sezilarli qisqartiradi, lekin uni yoqish bitta qatordan iborat emas va bu yerda jimgina ishlamay qolish oson. Testcontainers hujjati uchta shartni talab qiladi: bayroq, konteynerda `withReuse(true)`, va konteynerni QO'LDA `start()` bilan ishga tushirish (`stop()` chaqirilmaydi, ya'ni `try-with-resources` ham, JUnit integratsiyasi ham ishlatilmaydi). Shartlardan bittasi bajarilmasa konteyner oddiy tartibda ko'tariladi va o'chadi, hech qanday xato chiqmaydi.

```properties
# ~/.testcontainers.properties - FOYDALANUVCHI fayli.
# Diqqat: bu sozlamani classpath dagi properties fayli orqali berish
# ISHLAMAYDI, hujjat buni alohida aytadi. Muqobil yo'l muhit
# o'zgaruvchisi: TESTCONTAINERS_REUSE_ENABLE=true
testcontainers.reuse.enable=true
```

```java
// Konteyner konfiguratsiyasi BIR XIL bo'lishi shart, aks holda qayta
// ishlatilmaydi va yangisi ko'tariladi.
static final PostgreSQLContainer<?> DB =
    new PostgreSQLContainer<>("postgres:16-alpine")
        .withReuse(true);

static {
    DB.start();   // qo'lda; stop() chaqirilmaydi
}
```

Uch ogohlantirishni ham yozib qo'yish kerak, chunki ular hujjatda bor. Birinchi: bu imkoniyat EKSPERIMENTAL va xulqi o'zgarishi mumkin. Ikkinchi: konteynerlar testlar tugagandan keyin TO'XTAMAYDI, ya'ni ularni o'zingiz kuzatasiz va o'chirasiz. Uchinchi: bu rejim CI uchun mos emas, chunki resurs tozalash va tarmoq kabi ba'zi imkoniyatlar to'liq ishlamaydi. Shuning uchun u faqat mahalliy ishda yoqiladi.

```bash
# Faqat o'zgargan modul testlari
./mvnw -q -pl payment -am test

# Gradle: incremental va build kesh
./gradlew test --build-cache --parallel
```

**Masofaviy build kesh ikki shart bajarilganda ishlaydi.** Birinchi shart - build **to'liq takrorlanadigan** bo'lishi (39.3): har maqsad uchun kirishlar to'plamini aniqlash mumkin bo'lishi va bir xil kirish istalgan mashinada bir xil chiqish berishi kerak. Aks holda keshdan yuklab olingan artefakt o'zi qurganidan farq qilishi mumkin va kesh ishonchsiz bo'ladi. Shuning uchun keshdagi har artefakt ikki narsa bilan kalitlanadi: maqsad va **kirishlar hashi**; shunda ikki muhandis bir maqsadni boshqa o'zgarish bilan qursa, kesh ikkala natijani ham to'qnashuvsiz saqlaydi.

Ikkinchi shart - artefaktni **yuklab olish uni qurishdan tezroq** bo'lishi. Bu o'z-o'zidan ro'y bermaydi, ayniqsa kesh serveri build qilayotgan mashinadan uzoq bo'lsa. Shuning uchun masofaviy keshni sozlashda tarmoq kechikishi hisobga olinadi va kesh haqiqatda yordam berayotgani **tajriba bilan o'lchanadi**.

Shu yerda bitta muqobil yo'lni ham chetlab o'tish kerak. Sekin qurilayotgan o'z modullarini artefakt sifatida relizga chiqarib, ularga tashqi bog'liqlik kabi tayanish nazariy jihatdan buildni tezlashtiradi (artefakt sekin qurilib, tez yuklab olinsa). Amalda esa bu ortiqcha mehnat va murakkablik kiritadi: kimdir har artefaktni qurib yuklashga mas'ul bo'ladi, iste'molchilar oxirgi versiyada qolishni ta'minlashi kerak, va nosozlikni tekshirish qiyinlashadi, chunki tizimning har qismi manba daraxtining boshqa nuqtasidan qurilgan bo'ladi va yagona manzara qolmaydi. To'g'ri yechim - masofaviy keshni ishlatish: u artefaktga bevosita tayanishning tezlik foydasini beradi, lekin buildlar har doim bir manbadan qurilgandek izchil qoladi.

## 39.8 `.gitignore`, sir va konfiguratsiya fayllari

Sir kod bazasiga tushsa, uni tarixdan olib tashlash qiyin va u allaqachon oqib ketgan hisoblanadi (40.8). Himoya ikki qatlamli: `.gitignore` va avtomatik skanerlash.

```gitignore
# Mahalliy sozlamalar va sirlar hech qachon commit qilinmaydi
.env
*.local.yml
application-local.yml
*.p12
*.jks
*.pem
secrets/
# IDE va OS
.idea/
*.iml
.vscode/
.DS_Store
```

Qoida: `application.yml` da sir bo'lmaydi - faqat `${ENV_VAR}` havolasi (26.4). Sirlar muhit o'zgaruvchisi, Kubernetes Secret yoki secret manager dan keladi.

```yaml
# CI da sir skanerlash: tarixga tushishini to'sadi
- name: Sir skanerlash
  run: |
    docker run --rm -v "$PWD:/repo" zricethezav/gitleaks:latest \
      detect --source=/repo --no-git -v
```

## 39.9 IDE qobiliyatlari: bir tugmali ishga tushirish, test va debug

Bir qadamli build ning IDE dagi aksi ham bor: kuniga o'nlab marta takrorlanadigan harakat bitta tugma bo'lishi kerak. Orosz bu bo'shliqni alohida ta'kidlaydi: kimyo laboratoriyasida asbobni ishlatish o'rgatiladi, dasturiy ta'minotda esa bunday o'qitish kam uchraydi va muhandis tooling, build va deploy qanday ishlashini ko'pincha o'zi topib olishga majbur (Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 10-bob, 133-bet).

Quyidagi ro'yxat kitobning zamonaviy IDE dan kutiladigan qobiliyatlar ro'yxati; o'ng ustun shu qobiliyat Java va Spring loyihasida qayerda kerak bo'lishini ko'rsatadi (shu yerda, 133-134-bet).

| Qobiliyat | Tekshiruv savoli | Java va Spring da qayerda |
|---|---|---|
| Refaktoring | nom o'zgartirish va metod ajratish tugmasi bormi | 38.3 chegarasi ichida |
| Kompilyatsiya | bitta qisqartma bilan, saqlashda avtomatik bo'ladimi | ko'p modulli Maven loyihasi |
| Ishga tushirish | ilovani bitta tugma bilan ko'tarish | `spring-boot:run` konfiguratsiyasi |
| Qayta yuklash | kod o'zgarsa kontekst qayta ko'tariladimi | mahalliy profil |
| Debug | breakpoint, qadamlash, stack trace, lokal o'zgaruvchilar | 46.9 |
| Kengaytirilgan debug | shartli breakpoint, N marta o'tkazib yuborish | sikl ichidagi bitta yozuv |
| Testni ishga tushirish | bitta test metodini alohida yurgizish | `@Test` metod darajasida |
| Testni debug qilish | aynan shu testga breakpoint qo'yish | yiqilgan integratsion test |
| PR ochish | IDE dan chiqmasdan | 40.6 hajmi bilan birga |

Ikkinchi talab siklning uzunligiga tegishli: tahrirdan natijani ko'rishgacha bir necha sekunddan ko'p ketsa, vaqt kontekstni almashtirishga sarflanadi va zamonaviy asbobda bunchalik kutishning sababi yo'q. Sekin siklni normal deb qabul qilmaslik kerak: jamoadoshlardan so'rab, mashinasini kutmaydigan odamning sozlamasini ko'chirish eng tez yo'l (shu yerda, 134-bet).

```bash
# IDE dagi har tugma ortida shu buyruqlar turadi. Ikkisi bir xil
# natija bermasa, IDE konfiguratsiyasi build dan ajrab ketgan:
# odatda sabab IDE ning o'z kompilyatori, faol profil yoki
# muhit o'zgaruvchisi bo'ladi.
./mvnw -q -pl payment -am test -Dtest=SettlementImporterTest#rejectsMixedCurrency
./mvnw -q -pl payment spring-boot:run -Dspring-boot.run.profiles=local
```

ESLATMA: jadvalning o'ng ustuni va IDE bilan buyruq natijasini solishtirish tavsiyasi shu korpusning amaliy qo'shimchasi, kitobdan olingan emas.

## 39.10 Debug yordamchilarini rejali olib tashlash

Debug yordamchisi - invariant tekshiruvi, qo'shimcha diagnostika, soxta ma'lumot generatori, yordamchi endpoint - ishlab chiqish paytida arzon, production da esa hajm va tezlik bo'yicha qimmat tushadi. Qaysi tekshiruv production da qoladi degan savol [xato bilan ishlash bobida](18-xato-bilan-ishlash-qoidalari.md#1813-himoya-tekshiruvining-qanchasi-ishlab-chiqarishda-qoladi) hal qilinadi; bu bo'lim esa qolmaydiganini qanday olib tashlash haqida, ya'ni build darajasidagi qarori haqida. McConnell bu yerda ikki qoida beradi va ikkisi ham vaqt bilan bog'liq.

Birinchisi: yordamchi iloji boricha ertaroq kiritiladi. Odatda programmist yordamchi yozishga muammo bir necha marta tishlaganidan keyin kirishadi; birinchi holatdan keyin yozilsa, u butun loyiha davomida foyda beradi (McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 8.6 (206-bet)).

Ikkinchisi: olib tashlash yo'li yordamchi KIRITILAYOTGANDA hal qilinadi. Maqsad - debug kodini programmaga qo'lda kiritib, keyin qo'lda chiqarib yurishdan qutulish; kitob buning uchun uch yo'lni sanaydi (shu yerda, 8.6 (206-208-bet)):

- **Versiya nazorati va build asbobi.** Bir xil manbadan ikki xil build yasaladi: development rejimida debug kodi kiradi, production rejimida chiqib qoladi.
- **Preprotsessor.** C++ da `#if defined(DEBUG)` bilan bo'lak kompilyator kalitida yoqiladi yoki o'chiriladi; tilda preprotsessor bo'lmasa, kitob o'z konvensiyasi bilan precompiler yozishni ham ko'rib chiqadi (misoli Java uchun `//#BEGIN DEBUG` va `//#END DEBUG` belgilari).
- **Debug stub.** Tekshiruv alohida rutinaga chiqariladi: development versiyasi to'liq tekshiradi, production versiyasi darhol qaytadi; ikki versiya ham saqlanadi. Buning Spring dagi shakli (profil bo'yicha ikki bean) [offensive programming bo'limida](19-istisno-mexanikasi-va-resurslar.md#1914-offensive-programming-development-da-qattiq-production-da-yumshoq-yiqilish).

Java da birinchi va uchinchi yo'l ishlaydi, ikkinchisi yo'q: tilda preprotsessor va shartli kompilyatsiya yo'q, shuning uchun uning o'rnini build profili, konfiguratsiya kaliti va `assert` oladi.

Til spetsifikatsiyasida bu yerda bitta kichik teshik ataylab qoldirilgan va uni bilish kerak: erishilmaydigan gap kompilyatsiya xatosi, lekin `if (false) { ... }` erishilmaydigan hisoblanmaydi. Teshik aynan shartli kompilyatsiyaga o'xshash narsa uchun ochiq qoldirilgan: `static final boolean DEBUG = false` bilan o'ralgan bo'lak kompilyatsiyadan o'tadi va keyin optimizatsiyada tushib qoladi. Shunga qaramay bu yo'l yordamchini olib tashlash rejasi hisoblanmaydi, chunki bayroq manba kodda qotib qoladi: build profili yoki konfiguratsiya kaliti bilan boshqarilmaydi va kim qachon yoqishini hech qayerda ko'rsatmaydi.

| Yordamchi | Java va Spring mexanizmi | Nimaga e'tibor berish |
|---|---|---|
| Invariant tekshiruvi | `assert` va faqat test ishga tushirishida `-ea` ([assertion va `-ea`](19-istisno-mexanikasi-va-resurslar.md#198-assertion-va--ea-qachon-haqli)) | `assert` ichida yon ta'sir bo'lmasligi shart: production da u bajarilmaydi |
| Qimmat diagnostika | `log.debug` va `isDebugEnabled` | `System.out` emas (29-bob); log darajasi deploydan keyin ham o'zgartiriladi |
| Yordamchi endpoint yoki sahifa | `@Profile("local")`, `@ConditionalOnProperty` | production profilida ko'tarilmasligini test bilan qulflash |
| Soxta ma'lumot generatori | `test` scope yoki alohida Maven profili | asosiy artefaktga tushmasligi (39.4) |
| Qattiq tekshiruv rejimi | bayroq bilan yoqiladigan validator (debug stub ning Java shakli) | o'chirilganda xatti-harakat o'zgarmasligi |

```java
// Invariant: faqat `-ea` bilan yoqiladi, shuning uchun ichida yon ta'sir yo'q
assert rows.stream().noneMatch(SettlementRow::isNegative)
        : "validatsiyadan keyin manfiy qator qoldi";

// Qimmat diagnostika: daraja bilan o'chadi, kodda qolib ketmaydi
if (log.isDebugEnabled()) {
    log.debug("batch={} accepted={} rejected={}",
            batch.id(), accepted.size(), rejected.size());
}
```

```java
// Yordamchi endpoint: production profilida kontekstga umuman kirmaydi
@Profile("local")
@RestController
@RequestMapping("/internal/settlement")
class SettlementDebugController {

    private final SettlementImporter importer;

    SettlementDebugController(SettlementImporter importer) {
        this.importer = importer;
    }

    @PostMapping("/replay")
    ImportReport replay(@RequestBody ReplayRequest request) {
        return importer.replay(request.batchId());
    }
}
```

Qoidaning bitta amaliy shakli bor: yordamchining o'chirilgan holati xatti-harakatni o'zgartirmasin. `assert` ichida hisob yoki o'zgartirish bo'lsa, `-ea` siz production boshqacha ishlaydi va bu eng qiyin topiladigan xato turi bo'ladi. Olib tashlash rejasi esa izoh emas: u build profili, konfiguratsiya kaliti yoki feature flag shaklida bo'ladi. `TODO: keyin o'chiriladi` reja hisoblanmaydi (8.7).

ESLATMA: jadvalning Java va Spring ustuni shu korpusning moslashtirishi; kitob til sifatida C++ va umumiy build asboblari (ant, make) misolida gapiradi. `assert` ning `-ea` siz bajarilmasligi va `@Profile` xatti-harakati esa Java va Spring ning hujjatlashtirilgan xatti-harakati.

## 39.11 Amalda qo'llash

- [ ] Yangi (yoki tozalangan) mashinada `git clone` + bitta buyruq bilan build ishlashini tekshirib, yetishmaganini README ga emas, build ga ko'chiring.
- [ ] Testni ishga tushirish uchun qo'lda sozlash kerak bo'lsa, uni Testcontainers yoki standart konfiguratsiya bilan yo'qoting.
- [ ] `dependency:analyze` ni ishga tushirib, ishlatilmaydigan bog'liqliklarni o'chiring va e'lon qilinmaganlarini qo'shing.
- [ ] Test kutubxonalarining `scope` i `test` ekanini tekshirib, production jar mazmunini ko'rib chiqing.
- [ ] Barcha bog'liqlik va plagin versiyalarini `<properties>` yoki BOM ga ko'chiring; snapshot va ochiq versiyalarni yo'qoting.
- [ ] Generatsiya qilingan kodni `git` dan chiqarib, formatlash va tahlildan istisno qiling.
- [ ] Mahalliy qaytish halqasini 39.7 jadvaliga qarab o'lchab, eng sekin bo'g'inni tezlashtiring.
- [ ] `.gitignore` ni sir fayllari bilan to'ldirib, CI ga sir skanerlashni qo'shing.
- [ ] Har bir debug yordamchisi uchun olib tashlash mexanizmini (profil, sozlama kaliti, `-ea`) yozib qo'ying va `TODO` bilan qolganlarini tuzating (39.10).

## Manbalar

- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 18-bob ("Difficulty performing incremental builds", "Time, Scale, Trade-Offs") - har build oldidan `clean` qilish odati inkremental buildning ishonchsizligi alomati ekani va qaysi qadam qayta ishlashini build tizimi o'zi aniqlashi kerakligi; build tizimini almashtirish tezlik yoki to'g'rilik muammosi ko'rinmasa o'zini oqlamasligi. Bu nashrning nusxasida barqaror bet raqami yo'q, shuning uchun bob va bo'lim nomi ko'rsatilgan
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 18-bob ("Remote Caching", "Caching build results using external dependencies") - masofaviy keshning ikki sharti (build to'liq takrorlanadigan bo'lishi va artefakt kalitining kirishlar hashi bo'lishi; yuklab olish qurishdan tezroq bo'lishi va buni tajriba bilan o'lchash), hamda o'z artefaktlarini tashqi bog'liqlik sifatida chiqarish o'rniga keshni ishlatish. Bu nashrning nusxasida barqaror bet raqami yo'q, shuning uchun bob va bo'lim nomi ko'rsatilgan
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 16-bob ("Scenario: Multiple Available Versions", "TL;DRs") - umumiy kutubxonaning qayta nomlanmagan forki kodbazani bo'lishi va runtime xatolariga olib kelishi, shadingning funksiyalar uchun ishlab turlar uchun ishlamasligi va asosiy muammoni yashirishi, repozitoriylar orasidagi bog'liqlikning qotirilmagan (trunk bo'yicha) bo'lishi afzalligi. Bu nashrning nusxasida barqaror bet raqami yo'q, shuning uchun bob va bo'lim nomi ko'rsatilgan
- Apache Maven, *Configuring for Reproducible Builds*
  ([https://github.com/apache/maven-site/blob/eb827a7/content/markdown/guides/mini/guide-reproducible-builds.md](https://github.com/apache/maven-site/blob/eb827a7/content/markdown/guides/mini/guide-reproducible-builds.md),
  commit `eb827a7`, Apache-2.0) - 39.3 dagi
  `project.build.outputTimestamp`, `artifact:check-buildplan` va
  `artifact:compare` bilan tekshirish, hamda Maven 3.10.0 dan boshlab
  rejimning default yoqilishi.
- *The Java Language Specification, Java SE 25 Edition* (Gosling, Joy, Steele,
  Bracha, Buckley, Smith, Bierman), 14-bob (556-bet) - erishilmaydigan gap
  kompilyatsiya xatosi ekani, lekin `if (false) { ... }` erishilmaydigan
  hisoblanmasligi va bu teshikning shartli kompilyatsiyaga o'xshash
  foydalanish uchun ataylab qoldirilgani.
- Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr,
  Pragmatic Engineer, 2023, 10-bob (133-134) - 39.9 dagi IDE dan
  kutiladigan qobiliyatlar ro'yxati, tooling bo'yicha rasmiy
  o'qitishning kamligi va tahrirdan natijagacha bo'lgan siklni qisqa
  ushlash talabi.
- Testcontainers, *Reusable Containers*
  ([https://github.com/testcontainers/testcontainers-java/blob/1.21.4/docs/features/reuse.md](https://github.com/testcontainers/testcontainers-java/blob/1.21.4/docs/features/reuse.md),
  tag `1.21.4`, MIT) - 39.7 dagi uch shart (bayroq, `withReuse(true)`,
  qo'lda `start()`), classpath properties fayli orqali yoqilmasligi,
  imkoniyatning eksperimental ekani, konteynerlarning to'xtamasligi va
  CI uchun mos emasligi.
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 8.6
  (206-208) - 39.10 dagi ikki qoida: debug yordamchisini ertaroq kiritish,
  olib tashlash yo'lini oldindan hal qilish; versiya nazorati va build
  asbobi, preprotsessor va debug stub mexanizmlari

---

[&larr; 38. Refaktoringni xavfsiz bajarish](38-refaktoringni-xavfsiz-bajarish.md) · [Mundarija](README.md) · [40. Versiya nazorati gigiyenasi &rarr;](40-versiya-nazorati-gigiyenasi.md)
