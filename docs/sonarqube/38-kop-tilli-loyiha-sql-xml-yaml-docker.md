<!-- doc: sonarqube | chapter: 38 | part: IX. Kengaytirish va integratsiya -->

[Barcha hujjatlar](../../README.md) / [SonarQube](README.md)

# 38. Ko'p tilli loyiha: SQL, XML, YAML, Docker, Kubernetes, frontend (Multi-language Projects)

<details>
<summary>Bu bobdagi 13 bo'lim</summary>

- [38.1 Java loyihada aslida nechta til bor: manba, konfiguratsiya, migratsiya, skript](#381-java-loyihada-aslida-nechta-til-bor-manba-konfiguratsiya-migratsiya-skript)
- [38.2 Tahlilga qo'shiladigan fayl turlarini sozlash](#382-tahlilga-qoshiladigan-fayl-turlarini-sozlash)
- [38.3 SQL va migratsiya fayllari: nimaga e'tibor beriladi](#383-sql-va-migratsiya-fayllari-nimaga-etibor-beriladi)
- [38.4 XML va `pom.xml`: bog'liqlik va konfiguratsiya qoidalari](#384-xml-va-pomxml-bogliqlik-va-konfiguratsiya-qoidalari)
- [38.5 YAML va `application.yaml`: maxfiy ma'lumot va sozlama xatolari](#385-yaml-va-applicationyaml-maxfiy-malumot-va-sozlama-xatolari)
- [38.6 Dockerfile qoidalari: root foydalanuvchi, aniq versiya, keraksiz paket](#386-dockerfile-qoidalari-root-foydalanuvchi-aniq-versiya-keraksiz-paket)
- [38.7 Kubernetes manifesti: resurs limiti, probe, imtiyozli konteyner](#387-kubernetes-manifesti-resurs-limiti-probe-imtiyozli-konteyner)
- [38.8 Frontend (TypeScript va JavaScript) ni shu loyihaga qo'shish yoki ajratish](#388-frontend-typescript-va-javascript-ni-shu-loyihaga-qoshish-yoki-ajratish)
- [38.9 Frontend qamrovini ulash va alohida hisobot berish](#389-frontend-qamrovini-ulash-va-alohida-hisobot-berish)
- [38.10 Shell skriptlari va CI konfiguratsiyasi](#3810-shell-skriptlari-va-ci-konfiguratsiyasi)
- [38.11 Ko'p tilli loyihada quality gate ni adolatli qo'yish](#3811-kop-tilli-loyihada-quality-gate-ni-adolatli-qoyish)
- [38.12 Qaysi tilni tahlilga qo'shmaslik mantiqiy](#3812-qaysi-tilni-tahlilga-qoshmaslik-mantiqiy)
- [38.13 Amalda qo'llash](#3813-amalda-qollash)

</details>



Ko'pchilik Java loyihani "Java loyiha" deb ataydi, lekin repozitoriyni ochib sanab chiqsang, odatda sakkiztadan o'n ikkitagacha til topiladi. Sonar bu tillarning hammasini birdan ko'rmaydi: bir qismini standart holatda tahlil qiladi, bir qismini sozlash kerak, bir qismi esa faqat tijorat nashrida mavjud. Bu bobda qaysi til qanday yo'l bilan tahlilga kiradi, qamrov va quality gate ko'p tilli loyihada qanday hisoblanadi, va nimani ataylab tahlildan chiqarib qo'yish mantiqiy ekanini ko'rib chiqamiz. Maqsad bitta: Sonar hisoboti loyihaning haqiqiy holatini ko'rsatsin, Java fayllarining yarmini emas.

## 38.1 Java loyihada aslida nechta til bor: manba, konfiguratsiya, migratsiya, skript

Oddiy Spring Boot monolitini oling. `src/main/java` da Java, `src/main/resources` da `application.yaml`, `logback-spring.xml` va `messages.properties`, `db/migration` da Flyway SQL migratsiyalari turadi. Ildizda `pom.xml`, `Dockerfile` va `docker-compose.yaml` bor. `deploy/` da Kubernetes manifestlari, `.github/workflows/ci.yaml` da CI, `scripts/` da bash skriptlar yotadi. Admin paneli shu repozitoriyda bo'lsa, `frontend/` da TypeScript, HTML va CSS ham bor.

Bu fayllarning har biri ishlab chiqarishga ta'sir qiladi, va eng qimmat hodisalarning katta qismi Java kodidan emas, konfiguratsiyadan kelib chiqadi. Noto'g'ri connection pool o'lchami, `latest` tegi bilan qotib qolgan image, resurs limiti yo'q pod. Agar Sonar faqat Java ni ko'rsa, u loyihaning eng xatarli qismini tekshirmaydi.

Shu sababli ko'p tilli tahlil bu "qo'shimcha imkoniyat" emas, balki asosiy ehtiyoj. Lekin halol gap shu: qo'llab-quvvatlash nashrga bog'liq. Java, XML, YAML, JSON, HTML, CSS, JavaScript, TypeScript, Python, Go, PHP, Kotlin, Ruby, Scala, shuningdek Docker, Kubernetes va Terraform kabi infratuzilma tillari bepul nashrda ham bor. Bir qator til esa faqat pullik nashrda ishlaydi: PL/SQL va T-SQL kabi maxsus SQL dialektlari, C va C++, Objective-C, Swift, Apex, ABAP, COBOL shu qatorga kiradi. Ro'yxat versiya bilan o'zgaradi va yangi tillar qo'shilib turadi, shuning uchun aniq ro'yxatni o'z versiyangiz hujjatidan yoki server UI dagi Rules bo'limidan tekshirish kerak. Men bu yerda ro'yxatni oxirgi haqiqat deb bermayman.

## 38.2 Tahlilga qo'shiladigan fayl turlarini sozlash

Sonar scanner ikki savolga javob izlaydi: qaysi fayllarni o'qiyman va ularni qaysi tilga tegishli deb hisoblayman. Birinchi savolga `sonar.sources` va `sonar.tests` javob beradi. Maven plugini bu ikkisini `pom.xml` dan avtomatik oladi, shu sababli Maven loyihada ularni qo'lda yozish ko'pincha kerak emas va hatto zarar keltiradi. Ikkinchi savolga har tilning fayl kengaytmasi va shu til uchun mavjud analizator javob beradi.

Muammo odatda shu joyda tug'iladi: Maven avtomatik `sonar.sources` ni `src/main/java` ga tenglashtiradi, natijada ildizdagi `Dockerfile`, `deploy/` va `.github/` tahlilga kirmaydi. Yechim `sonar.sources` ni kengaytirish va shu bilan birga Java kompilyatsiya natijasi joyida qolishiga ishonch hosil qilish.

```properties
# Ildizdagi sonar-project.properties: ko'p tilli loyiha uchun asos
sonar.projectKey=shop-backend
sonar.projectName=Shop Backend
sonar.sourceEncoding=UTF-8

# Java manbasiga qo'shimcha ravishda infratuzilma va migratsiya papkalari
sonar.sources=src/main/java,src/main/resources,deploy,scripts,Dockerfile,.github
sonar.tests=src/test/java

# Generatsiya qilingan va uchinchi tomon fayllari tahlilga kirmasin
sonar.exclusions=**/generated/**,**/target/**,**/node_modules/**,**/*.min.js

# Qamrov hisobidan chiqariladigan fayllar: konfiguratsiya va DTO
sonar.coverage.exclusions=**/config/**,**/*Application.java,**/dto/**

# Takroriylik tekshiruvidan migratsiyalarni chiqaramiz: ular ataylab o'xshash
sonar.cpd.exclusions=src/main/resources/db/migration/**

# JaCoCo XML hisobotining yo'li, agregator modulda birlashtirilgan fayl
sonar.coverage.jacoco.xmlReportPaths=report/target/site/jacoco-aggregate/jacoco.xml
```

Bu yerda muhim nuqta bor: `sonar.exclusions` faylni butunlay tahlildan chiqaradi, `sonar.coverage.exclusions` esa faylni tahlilda qoldiradi, lekin qamrov hisobiga kiritmaydi. Ikkisini aralashtirib yuborish eng keng tarqalgan xato. Konfiguratsiya klassini `sonar.exclusions` ga yozsang, undagi maxfiy ma'lumot ham tekshirilmay qoladi.

| Tuzoq | Nima sodir bo'ladi | Yechim |
|---|---|---|
| `sonar.sources` faqat `src/main/java` | Dockerfile va manifestlar hech qachon tekshirilmaydi | Sources ro'yxatiga infratuzilma papkalarini qo'shish |
| Maven loyihada `sonar.sources` ni qo'lda qayta yozish | Java kompilyatsiya natijasi topilmaydi, Java tahlili buziladi | Maven da sources ni plugin hisoblashiga qoldirish yoki `sonar.java.binaries` ni aniq ko'rsatish |
| `node_modules` exclusion ga kirmagan | Tahlil soatlab davom etadi, minglab soxta issue chiqadi | `sonar.exclusions` ga `**/node_modules/**` qo'shish |
| Migratsiyalar takroriylik hisobiga kirgan | Duplication foizi sun'iy o'sadi, gate yiqiladi | `sonar.cpd.exclusions` ga migratsiya papkasini yozish |
| Qamrov hisoboti yo'li noto'g'ri | Coverage nol ko'rinadi, gate "new code 0%" deb yiqitadi | Hisobot faylini scanner dan oldin generatsiya qilish va yo'lni tekshirish |
| Frontend `lcov` fayli yuklanmagan | TypeScript kodi tahlil qilinadi, lekin qamrovsiz ko'rinadi | `sonar.javascript.lcov.reportPaths` ni ko'rsatish |

## 38.3 SQL va migratsiya fayllari: nimaga e'tibor beriladi

Bu yerda eng ko'p noto'g'ri tushuniladigan joy. Flyway migratsiyalaridagi `.sql` fayllari uchun chuqur tahlil, ya'ni so'rov mantiqini tekshiruvchi qoidalar, standart bepul nashrda mavjud emas. PL/SQL va T-SQL analizatorlari tijorat nashriga tegishli, va ular ham PostgreSQL dialektini emas, Oracle va SQL Server dialektini nazarda tutadi. Shuning uchun "Sonar mening PostgreSQL migratsiyamni tekshiradi" degan kutish ko'pincha asossiz.

Amalda ikkita haqiqiy foyda bor. Birinchisi, `.sql` fayllaridagi maxfiy ma'lumot: parol, token, connection string. Maxfiy ma'lumotni aniqlash qoidalari matn analizatori orqali ishlaydi va u bepul nashrda ham mavjud. Ikkinchisi, Java tomondan SQL ga bo'lgan munosabat: satrlarni ulab so'rov yasash. Bu Java qoidasi bo'lib, injection xavfini ko'rsatadi.

```sql
-- Shikoyat chiqaradigan migratsiya: ishlab chiqarishda bloklanish xavfi
-- V12__add_status_to_orders.sql
ALTER TABLE orders ADD COLUMN status VARCHAR(32) NOT NULL DEFAULT 'NEW';

-- Parol migratsiyada yozilgan: maxfiy ma'lumot qoidasi shikoyat qiladi
CREATE USER report_reader WITH PASSWORD 'Sup3rSecret!';

-- Tuzatilgan variant: ustun avval nullable qo'shiladi, keyin to'ldiriladi
-- V12__add_status_to_orders.sql
ALTER TABLE orders ADD COLUMN status VARCHAR(32);
UPDATE orders SET status = 'NEW' WHERE status IS NULL;
ALTER TABLE orders ALTER COLUMN status SET DEFAULT 'NEW';

-- Parol o'rniga rol beriladi, parol tashqi secret store dan o'rnatiladi
CREATE ROLE report_reader;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO report_reader;
```

Yuqoridagi bloklanish xavfi haqidagi mulohaza Sonar qoidasi emas, bu PostgreSQL mexanikasi, va uni arxitektor mindset hujjatidagi migratsiya va qulf mavzusida ko'rish kerak. Java tomonidagi SQL muammosi esa aniq Sonar hududi.

```java
// Shikoyat chiqaradigan kod: so'rov satr ulash bilan yasalgan
public List<Order> findByStatus(String status) {
    String sql = "SELECT * FROM orders WHERE status = '" + status + "'";
    return jdbcTemplate.query(sql, orderRowMapper);
}

// Tuzatilgan variant: parametr bilan bog'langan so'rov
private static final String FIND_BY_STATUS =
        "SELECT id, status, total FROM orders WHERE status = ?";

public List<Order> findByStatus(String status) {
    // Parametr alohida uzatiladi, injection yo'li yopiladi
    return jdbcTemplate.query(FIND_BY_STATUS, orderRowMapper, status);
}
```

## 38.4 XML va `pom.xml`: bog'liqlik va konfiguratsiya qoidalari

XML analizatori bepul nashrda bor va u `pom.xml`, `logback-spring.xml`, `web.xml` kabi fayllarni o'qiydi. Uning qoidalari ikki guruhga bo'linadi: umumiy XML gigiyenasi va Maven ga xos tekshiruvlar. Umumiy guruhda bo'sh element, takroriy atribut, kodlanish e'loni yo'qligi, DTD tashqi obyektini yuklash xavfi bor. Maven guruhida bog'liqlik versiyasi ko'rsatilmagani yoki `LATEST` va `RELEASE` kabi aniq bo'lmagan versiya ishlatilgani tekshiriladi.

Aniq versiya masalasi real: versiyasi qotirilmagan build takrorlanmaydi, va bugun o'tgan test ertaga boshqa artefakt bilan ishga tushadi.

```xml
<!-- Shikoyat chiqaradigan qism: versiya aniq emas, scope yozilmagan -->
<dependency>
  <groupId>org.apache.commons</groupId>
  <artifactId>commons-lang3</artifactId>
  <version>RELEASE</version>
</dependency>

<!-- Tuzatilgan variant: versiya property orqali qotirilgan -->
<properties>
  <commons-lang3.version>3.17.0</commons-lang3.version>
</properties>

<dependency>
  <groupId>org.apache.commons</groupId>
  <artifactId>commons-lang3</artifactId>
  <version>${commons-lang3.version}</version>
</dependency>

<!-- Qamrov hisobotini Sonar o'qiydigan XML formatda chiqarish -->
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <version>0.8.12</version>
  <executions>
    <execution><id>report</id><goals><goal>report</goal></goals></execution>
  </executions>
</plugin>
```

JaCoCo 0.8.x liniyasida patch versiyasini Java versiyangizga qarab tanlang: yangi bytecode bilan eski patch sinishi mumkin, shuning uchun uni Java yangilanishi bilan birga ko'tarib borish kerak.

## 38.5 YAML va `application.yaml`: maxfiy ma'lumot va sozlama xatolari

YAML uchun ikki xil tahlil bor va ularni ajratish muhim. Birinchisi YAML ning o'zi sifatida tahlil: sintaksis, takroriy kalit, juda uzun qator. Ikkinchisi faylning mazmuniga qarab maxsus tahlil: agar fayl Kubernetes manifesti bo'lsa, infratuzilma qoidalari ishga tushadi, agar oddiy Spring konfiguratsiyasi bo'lsa, ishga tushmaydi. Sonar `application.yaml` ni Spring semantikasi bilan tushunmaydi, ya'ni `spring.datasource.hikari.maximum-pool-size` qiymati to'g'rimi yoki yo'qmi deb hukm chiqarmaydi.

Shunga qaramay, bu faylda eng muhim tekshiruv ishlaydi: maxfiy ma'lumotni aniqlash. Parol, API kalit, bulut hisob ma'lumoti kodga tushib qolsa, u security kategoriyasida, odatda blocker yoki critical darajasida chiqadi.

```yaml
# Shikoyat chiqaradigan konfiguratsiya: parol va kalit kodda
spring:
  datasource:
    url: jdbc:postgresql://db.prod.internal:5432/shop
    username: shop_app
    password: Pr0d-P@ssw0rd-2025   # maxfiy ma'lumot qoidasi shikoyat qiladi
  jpa:
    show-sql: true                 # ishlab chiqarishda log ni to'ldiradi
payment:
  api-key: sk_live_51Hx9kQ2eZvKYlo

# Tuzatilgan variant: qiymatlar muhit o'zgaruvchisidan olinadi
spring:
  datasource:
    url: ${DB_URL}
    username: ${DB_USERNAME}
    password: ${DB_PASSWORD}       # qiymat secret store dan keladi
  jpa:
    show-sql: false
payment:
  api-key: ${PAYMENT_API_KEY}
```

Bir ogohlantirish: maxfiy ma'lumotni aniqlash qoidalari naqsh asosida ishlaydi. Ular keng tarqalgan formatdagi kalitlarni topadi, lekin ichki tizimingning o'ziga xos tokenini topmasligi mumkin. Sonar bu yerda qo'shimcha to'r, asosiy to'siq esa secret store va pre-commit hook.

## 38.6 Dockerfile qoidalari: root foydalanuvchi, aniq versiya, keraksiz paket

Dockerfile tahlili infratuzilma analizatori orqali keladi va bepul nashrda mavjud. Qoidalar mazmunan quyidagi masalalarni qamrab oladi: konteyner root sifatida ishga tushishi, base image tegining aniq bo'lmasligi, paket menejerining keshini tozalamaslik, `apt-get install` da versiya qotirilmagani, `COPY` o'rniga `ADD` ishlatilishi, sir qiymatini `ENV` orqali image ichiga joylash, va `RUN` ichida parol yozish. Qoida kalitlari `docker:` prefiksi bilan boshlanadi va aniq raqamni server UI dagi Rules bo'limidan ko'rish kerak, chunki ular versiya bilan qo'shilib boradi.

```bash
# Shikoyat chiqaradigan Dockerfile
FROM eclipse-temurin:latest
COPY target/shop.jar /app/shop.jar
RUN apt-get update && apt-get install -y curl
ENV PAYMENT_API_KEY=sk_live_51Hx9kQ2eZvKYlo
ENTRYPOINT ["java","-jar","/app/shop.jar"]

# Tuzatilgan Dockerfile: aniq teg, root dan voz kechish, kesh tozalash
FROM eclipse-temurin:21.0.5_11-jre-alpine AS runtime

# Alohida foydalanuvchi yaratamiz, konteyner root bo'lib ishlamaydi
RUN addgroup -S app && adduser -S -G app app

WORKDIR /app
COPY --chown=app:app target/shop.jar /app/shop.jar

# Sir qiymati image ichiga yozilmaydi, runtime da beriladi
USER app
EXPOSE 8080
ENTRYPOINT ["java","-XX:MaxRAMPercentage=75","-jar","/app/shop.jar"]
```

Ikki eslatma. Faylni Sonar ko'rishi uchun u `sonar.sources` ichida bo'lishi kerak, aks holda ildizdagi Dockerfile tahlilga kirmaydi. Va Sonar image ichidagi CVE larni skanerlamaydi: bu boshqa vositaning ishi.

## 38.7 Kubernetes manifesti: resurs limiti, probe, imtiyozli konteyner

Kubernetes manifestlari ham infratuzilma analizatori hududiga kiradi. Qoidalar mazmuni: konteynerda CPU va memory limiti yo'qligi, readiness va liveness probe yo'qligi, `privileged: true` qo'yilgani, `allowPrivilegeEscalation` ni yopmaslik, host tarmog'i yoki host papkasini mount qilish, `latest` tegi bilan image ishlatish, `Secret` qiymatini manifest ichida ochiq yozish. Qoida kalitlari `kubernetes:` prefiksi bilan boshlanadi.

Bu yerda Sonar ning kuchli tomoni shu: manifest odatda hech qanday testdan o'tmaydi, shuning uchun avtomatik tekshiruv bo'lmasa, xato faqat hodisadan keyin topiladi.

```yaml
# Tuzatilgan Deployment: limit, probe va xavfsizlik konteksti bor
apiVersion: apps/v1
kind: Deployment
metadata:
  name: shop-backend
spec:
  replicas: 3
  template:
    spec:
      containers:
        - name: app
          image: registry.internal/shop-backend:1.42.0  # latest emas
          resources:
            requests: { cpu: "250m", memory: "512Mi" }
            limits: { cpu: "1", memory: "1Gi" }
          readinessProbe:
            httpGet: { path: /actuator/health/readiness, port: 8080 }
            initialDelaySeconds: 10
          livenessProbe:
            httpGet: { path: /actuator/health/liveness, port: 8080 }
            initialDelaySeconds: 30
          securityContext:
            runAsNonRoot: true
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
          envFrom:
            - secretRef: { name: shop-db-credentials }
```

Helm chart da qiyinchilik bor: shablon ichidagi `{{ }}` ifodalari YAML ni yaroqsiz qiladi va analizator ba'zi fayllarni o'qiy olmaydi. Yechim: `helm template` natijasini alohida papkaga chiqarib, shu papkani Sonar ga berish.

## 38.8 Frontend (TypeScript va JavaScript) ni shu loyihaga qo'shish yoki ajratish

Monorepo da backend va frontend bir repozitoriyda yotsa, savol tug'iladi: bitta Sonar loyihasi bo'lsinmi yoki ikkita. Javob jamoa tuzilishiga bog'liq.

Bitta loyiha qulay, chunki bitta quality gate, bitta hisobot va pull request da bitta tekshiruv bo'ladi. Lekin kamchiligi jiddiy: coverage bitta umumiy foizga aylanadi. Backend da 85 foiz, frontend da 20 foiz bo'lsa, umumiy raqam 60 atrofida chiqadi va u hech kimga haqiqatni aytmaydi. Bundan tashqari gate yiqilganda kim javobgar ekani darhol tushunarsiz bo'ladi.

Ikkita loyiha ajratish aniqlik beradi: har jamoa o'z raqamiga, o'z gate iga va o'z profiliga ega bo'ladi. Narxi shu: CI da ikkita scanner ishlaydi va pull request da ikkita status chiqadi. Katta jamoada bu to'g'ri tanlov, kichik admin panel uchun bitta loyiha ham yetarli.

Eslatma: eski versiyalardagi `sonar.modules` yondashuvi endi tavsiya etilmaydi, monorepo da ajratish har papkani alohida loyiha kaliti bilan skanerlash orqali qilinadi. Bu nuqtada versiyaga qarab farq bor.

## 38.9 Frontend qamrovini ulash va alohida hisobot berish

Frontend qamrovi Sonar ga LCOV formatida beriladi: Jest yoki Vitest `lcov` reporter ni yoqib, hisobotni `coverage/lcov.info` ga yozadi. TypeScript tahlili sifatli bo'lishi uchun `tsconfig` yo'lini ham berish kerak, aks holda tur ma'lumotisiz tahlil qilinadi va bir qancha qoida ishga tushmaydi.

```bash
# 1-qadam: backend testi va JaCoCo XML hisoboti
./mvnw clean verify

# 2-qadam: frontend testi va LCOV hisoboti
npm --prefix frontend ci
npm --prefix frontend run test -- --coverage --coverageReporters=lcov

# 3-qadam: backend loyihasini skanerlash
./mvnw sonar:sonar -Dsonar.projectKey=shop-backend -Dsonar.qualitygate.wait=true

# 4-qadam: frontend loyihasini alohida kalit bilan skanerlash
npx sonarqube-scanner \
  -Dsonar.projectKey=shop-frontend \
  -Dsonar.sources=frontend/src \
  -Dsonar.tests=frontend/src \
  -Dsonar.test.inclusions=**/*.test.ts,**/*.test.tsx \
  -Dsonar.javascript.lcov.reportPaths=frontend/coverage/lcov.info \
  -Dsonar.typescript.tsconfigPaths=frontend/tsconfig.json \
  -Dsonar.exclusions=**/node_modules/**,**/*.min.js,**/dist/** \
  -Dsonar.qualitygate.wait=true
```

`sonar.qualitygate.wait=true` ni ikkala skanerlashda ham qo'yish muhim. Aks holda CI yashil bo'ladi, gate esa keyin yiqiladi va hech kim buni ko'rmaydi.

## 38.10 Shell skriptlari va CI konfiguratsiyasi

Shell skriptlari uchun Sonar da to'liq analizator yo'q. Buni aytib qo'yish kerak, chunki ko'p jamoa `scripts/deploy.sh` ni Sonar tekshirishini kutadi. Bash uchun to'g'ri vosita ShellCheck, va uni CI da alohida bosqich sifatida ushlab turish mumkin. Hamma narsa bitta joyda ko'rinishi talab bo'lsa, tashqi vosita natijasini SARIF formatida `sonar.sarifReportPaths` orqali yuklash yo'li bor, lekin issue lar tashqi qoida sifatida ko'rinadi va gate shartlariga ta'siri cheklangan.

CI konfiguratsiyasi, masalan `.github/workflows/ci.yaml`, YAML sifatida tekshiriladi va undagi maxfiy ma'lumot aniqlanadi. Lekin workflow mantiqi, masalan action ni commit hash bilan pinlamaslik, Sonar qoidalari bilan to'liq qamrab olinmaydi.

## 38.11 Ko'p tilli loyihada quality gate ni adolatli qo'yish

Eng muhim qoida bitta: gate ni "new code" asosida qo'y. Ko'p tilli eski loyihada umumiy kod bo'yicha shart qo'yish amalda ishlamaydi, chunki o'n yillik qarz bir kechada to'lanmaydi. Yangi kod bo'yicha shart esa adolatli: bugun yozilgan har qanday tilga bir xil talab qo'yiladi.

| Mavzu | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Qamrab olinadigan tillar | Faqat Java tahlil qilinadi | Java, XML, YAML, Docker, Kubernetes, frontend birgalikda qamraladi |
| `sonar.sources` | Maven avtomatik qiymatiga tashlab qo'yiladi | Infratuzilma papkalari ataylab qo'shiladi va tekshiriladi |
| Coverage ko'rsatkichi | Backend va frontend bitta foizga qo'shiladi | Har til yoki har loyiha o'z qamrov raqamiga ega |
| Gate shartlari | Umumiy kod bo'yicha 80 foiz talab qilinadi | New code bo'yicha shart, eski qarz alohida reja bilan kamaytiriladi |
| Maxfiy ma'lumot | Faqat code review ga ishoniladi | Secret qoidasi gate da blocker, qo'shimcha pre-commit hook bor |
| Dockerfile va manifest | Hech kim tekshirmaydi, hodisadan keyin tuzatiladi | Infratuzilma qoidalari CI da yiqitadi, PR o'tmaydi |
| Shell skript | Sonar tekshiradi deb o'ylanadi | ShellCheck alohida bosqich, kerak bo'lsa SARIF orqali yuklanadi |
| Exclusion siyosati | Gate yiqilganda shoshilib exclusion yoziladi | Exclusion lar ro'yxati sabab izohi bilan reviewdan o'tadi |
| Nashr imkoniyatlari | "Sonar hammasini biladi" deb taxmin qilinadi | Qaysi til qaysi nashrda borligi oldin tekshiriladi, reja shunga moslanadi |
| Hisobot egasi | Gate yiqilsa kim tuzatishi noma'lum | Har loyiha va har tilga egalik biriktirilgan |

Amaliy taqsimot shunday bo'lishi mumkin: backend uchun new code coverage 80 foiz, frontend uchun 60 foizdan boshlab har chorakda ko'tarish, infratuzilma loyihasiga coverage sharti umuman yo'q, chunki Dockerfile ga test yozilmaydi. Uning o'rniga security rating va yangi issue soni sharti qo'yiladi. Qamrov sharti ma'nosiz bo'lgan tilga qamrov talab qilish gate ni soxta yiqitadi va jamoani uni chetlab o'tishga o'rgatadi.

Qamrovni integratsion test bilan oshirish yo'llari [testlash qo'llanmasidagi](../testing/README.md) Testcontainers va CI test pipeline mavzularida yozilgan. Bu yerda faqat Sonar bu raqamni qanday o'qishi muhim.

## 38.12 Qaysi tilni tahlilga qo'shmaslik mantiqiy

Hammasini qo'shish to'g'ri strategiya emas. Quyidagilarni ataylab chiqarib qo'yish mantiqiy.

Generatsiya qilingan kod: OpenAPI yoki Protobuf dan yasalgan klasslar, MapStruct chiqargan fayllar. Ularni sen tuzatmaysin, generator tuzatadi. Tahlilda qolsa, minglab issue paydo bo'ladi va haqiqiy muammolar shovqin ichida ko'rinmaydi.

Minifikatsiya qilingan va vendor fayllar: `*.min.js`, `node_modules`, `dist`, `vendor`. Tahlilning qiymati nolga teng, sarflangan vaqt esa katta.

Katta ma'lumot fayllari, masalan test fixture sifatidagi uzun JSON va CSV. Natija foydasiz, vaqt esa sarflanadi.

Eski, muzlatilgan modul. Modul o'zgarmasa va o'chirilishi rejalashtirilgan bo'lsa, uni tahlilda ushlash faqat raqamni buzadi. Lekin "muzlatilgan" degani "xavfsiz" degani emas: security qoidalari uchun uni qoldirish to'g'riroq.

Chiqarib qo'yishning har bir qatori sabab izohi bilan birga yozilishi kerak. Exclusion ro'yxati izohsiz o'sa boshlasa, bir yildan keyin Sonar hisoboti loyihaning uchdan birini ko'rsatadigan bezakka aylanadi.

## 38.13 Amalda qo'llash

- [ ] Repozitoriyni ochib, undagi barcha til va fayl turlarini sanab, ro'yxat tuz: qaysi biri hozir tahlilga kiradi va qaysi biri kirmaydi.
- [ ] Server UI dagi Rules bo'limida til bo'yicha filtr qo'yib, o'z nashringizda qaysi til uchun qoida mavjudligini aniq tekshir, taxminga tayanma.
- [ ] `sonar.sources` ga `Dockerfile`, `deploy` va `.github` papkalarini qo'shib, birinchi tahlildan keyin chiqqan infratuzilma issue larini ko'rib chiq.
- [ ] `sonar.exclusions` va `sonar.coverage.exclusions` ni ajrat: generatsiya qilingan kodni birinchisiga, konfiguratsiya klasslarini ikkinchisiga yoz.
- [ ] Frontend uchun alohida loyiha kaliti yaratib, LCOV va `tsconfig` yo'llarini ulab, backend bilan aralashtirmagan holda qamrovni o'lchang.
- [ ] Quality gate ni new code asosiga o'tkaz va infratuzilma loyihasiga coverage sharti qo'ymasdan security rating sharti qo'y.
- [ ] Shell skriptlar uchun CI ga ShellCheck bosqichini qo'shib, natijani majburiy qil, uni Sonar dan kutib o'tirma.
- [ ] Exclusion faylidagi har bir qatorga bir qatorli izoh yozib, uni har chorakda qayta ko'rib chiqadigan vazifa yarat.

---

[&larr; 37. Taint analysis mexanikasi: source, sink, sanitizer](37-taint-analysis-mexanikasi-source-sink.md) · [Mundarija](README.md) · [39. Bog'liqlik zaifliklari va litsenziya tekshiruvi &rarr;](39-bogliqlik-zaifliklari-va-litsenziya.md)
