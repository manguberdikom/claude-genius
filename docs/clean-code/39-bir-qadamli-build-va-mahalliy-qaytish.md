<!-- doc: clean-code | chapter: 39 | part: XI. Kod bazasi va jarayon gigiyenasi -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

# 39. Bir qadamli build va mahalliy qaytish halqasi (One-Step Build)

<details>
<summary>Bu bobdagi 9 bo'lim</summary>

- [39.1 Build bitta buyruq bo'lsin](#391-build-bitta-buyruq-bolsin)
- [39.2 Test bitta buyruq bo'lsin](#392-test-bitta-buyruq-bolsin)
- [39.3 Takrorlanadigan build: versiya qotirish va wrapper](#393-takrorlanadigan-build-versiya-qotirish-va-wrapper)
- [39.4 Bog'liqlik gigiyenasi: BOM, scope, keraksizni o'chirish](#394-bogliqlik-gigiyenasi-bom-scope-keraksizni-ochirish)
- [39.5 Build fayli o'qilishi](#395-build-fayli-oqilishi)
- [39.6 Generatsiya qilingan kodni ajratish](#396-generatsiya-qilingan-kodni-ajratish)
- [39.7 Mahalliy tez qaytish halqasi](#397-mahalliy-tez-qaytish-halqasi)
- [39.8 `.gitignore`, sir va konfiguratsiya fayllari](#398-gitignore-sir-va-konfiguratsiya-fayllari)
- [39.9 Amalda qo'llash](#399-amalda-qollash)

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

## 39.2 Test bitta buyruq bo'lsin

Evristika E2: testni ishga tushirish ham bir buyruq bo'lishi kerak va u hech qanday tashqi sozlama talab qilmasligi lozim. Testcontainers shu talabni bajaradi: baza va Kafka test paytida avtomatik ko'tariladi ([testlash qo'llanmasidagi](../testing/README.md) Testcontainers bo'limi).

```bash
./mvnw test              # unit testlar, soniyalar
./mvnw verify            # integratsion testlar ham, Testcontainers bilan
```

Agar testni ishga tushirish uchun mahalliy PostgreSQL o'rnatish yoki `application-local.yml` ni tahrirlash kerak bo'lsa, E2 buzilgan.

## 39.3 Takrorlanadigan build: versiya qotirish va wrapper

Build takrorlanadigan bo'lishi kerak: bir xil commit bir xil natija bersin. Buni buzadigan uch narsa bor va ularning hammasini yopish mumkin.

| Buzuvchi | Yechim |
|---|---|
| Vosita versiyasi mahalliy | Maven/Gradle wrapper repoda |
| JDK versiyasi mahalliy | `.sdkmanrc`, `maven.compiler.release` |
| Bog'liqlik versiyasi ochiq (`LATEST`, `+`) | aniq versiya yoki BOM |
| Snapshot bog'liqligi | reliz versiyasiga o'tish |
| Build vaqtidagi tashqi so'rov | kerakli fayllarni repoda saqlash |
| Plagin versiyasi ko'rsatilmagan | har bir plagin versiyasini yozish |

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

Qaytish halqasining uzunligi ishlab chiqish tezligini belgilaydi. Maqsad: kod yozilgandan keyin natijani 10 sekundda ko'rish.

| Halqa | Maqsad vaqt | Vositalar |
|---|---|---|
| Kompilyatsiya | < 5 s | incremental build, IDE |
| Unit testlar (bir modul) | < 10 s | tez testlar, mocksiz domen |
| Formatlash va lint | < 5 s | pre-commit hook (13.5) |
| Integratsion testlar | < 2 min | Testcontainers qayta ishlatish |
| Butun build | < 10 min | parallel modul, test teg |
| CI pipeline | < 15 min | keshlash, parallel job |

```properties
# ~/.testcontainers.properties - konteynerlarni qayta ishlatish (mahalliy ishda)
testcontainers.reuse.enable=true
```

```bash
# Faqat o'zgargan modul testlari
./mvnw -q -pl payment -am test

# Gradle: incremental va build kesh
./gradlew test --build-cache --parallel
```

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

## 39.9 Amalda qo'llash

- [ ] Yangi (yoki tozalangan) mashinada `git clone` + bitta buyruq bilan build ishlashini tekshirib, yetishmaganini README ga emas, build ga ko'chiring.
- [ ] Testni ishga tushirish uchun qo'lda sozlash kerak bo'lsa, uni Testcontainers yoki standart konfiguratsiya bilan yo'qoting.
- [ ] `dependency:analyze` ni ishga tushirib, ishlatilmaydigan bog'liqliklarni o'chiring va e'lon qilinmaganlarini qo'shing.
- [ ] Test kutubxonalarining `scope` i `test` ekanini tekshirib, production jar mazmunini ko'rib chiqing.
- [ ] Barcha bog'liqlik va plagin versiyalarini `<properties>` yoki BOM ga ko'chiring; snapshot va ochiq versiyalarni yo'qoting.
- [ ] Generatsiya qilingan kodni `git` dan chiqarib, formatlash va tahlildan istisno qiling.
- [ ] Mahalliy qaytish halqasini 39.7 jadvaliga qarab o'lchab, eng sekin bo'g'inni tezlashtiring.
- [ ] `.gitignore` ni sir fayllari bilan to'ldirib, CI ga sir skanerlashni qo'shing.

---

[&larr; 38. Refaktoringni xavfsiz bajarish](38-refaktoringni-xavfsiz-bajarish.md) · [Mundarija](README.md) · [40. Versiya nazorati gigiyenasi &rarr;](40-versiya-nazorati-gigiyenasi.md)
