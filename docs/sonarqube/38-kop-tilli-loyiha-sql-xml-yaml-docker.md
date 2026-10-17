<!-- doc: sonarqube | chapter: 38 | part: IX. Kengaytirish va integratsiya -->

[Barcha hujjatlar](../../README.md) / [SonarQube](README.md)

> Holat: tekshirilmoqda. Da'volar hali manbaga solishtirilmoqda.

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

Ko'p jamoa shu yerda ikkinchi marta yanglishadi: "mayli, hech bo'lmaganda `.sql` dagi parolni topadi" deb o'ylaydi. Default holatda topmaydi, va buning sababi analizatorning fayl tanlash mantiqida. Matn va secret analizatori (`sonar-text`) ikki to'plamni ko'radi: tili aniqlangan fayllar, va `sonar.text.inclusions` naqshiga tushgan fayllar. Shu ikkinchi naqshning default qiymati aniq:

```properties
# sonar-text ning default inclusions ro'yxati
sonar.text.inclusions=**/*.sh,**/*.bash,**/*.zsh,**/*.ksh,**/*.ps1,\
  **/*.properties,**/*.conf,**/*.pem,**/*.config,.env,.aws/config
```

Ro'yxatda `**/*.sql` yo'q. Bepul nashrda `.sql` ning tili ham yo'q, chunki SQL analizatorlari tijorat nashriga tegishli. Ikkisi birlashganda natija shu: Flyway migratsiyasidagi parolni hech kim ko'rmaydi. Yechim bitta qator:

```properties
# .sql va boshqa kerakli kengaytmalarni secret skaneriga qo'shish
sonar.text.inclusions=**/*.sh,**/*.properties,**/*.conf,**/*.pem,\
  **/*.config,.env,**/*.sql
```

Bu yerda yana bitta shart bor va u CI da jimgina ishdan chiqaradi: `sonar.text.inclusions` orqali qo'shilgan fayllar faqat git kuzatuvidagi bo'lsa tahlil qilinadi. Agar tahlil git repozitoriysi ichida yurgizilmasa (arxivdan ochilgan manba, `.git` siz konteyner), analizator faqat tili aniqlangan fayllarga qaytadi va log ga ogohlantirish yozadi. Ya'ni lokal mashinada ishlagan sozlama CI da jim qolishi mumkin, va buni faqat log ni o'qib bilasan.

Ikkinchi haqiqiy foyda Java tomonida: satrlarni ulab so'rov yasash. Bu Java qoidasi bo'lib, injection xavfini ko'rsatadi va u hech qanday qo'shimcha sozlamasiz ishlaydi.

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

XML analizatori bepul nashrda bor va u `pom.xml`, `logback-spring.xml`, `web.xml` kabi fayllarni o'qiydi. Lekin bu yerda keng tarqalgan bitta kutish borki, u bajarilmaydi: **`pom.xml` da `LATEST` yoki `RELEASE` versiya ishlatilgani uchun Sonar shikoyat qilmaydi**. Analizatorning qoida ro'yxatida bunday qoida yo'q, versiyasi umuman yozilmagan bog'liqlik uchun ham yo'q. Agar bu kerak bo'lsa, uni Maven Enforcer plugini bajaradi, Sonar emas.

Maven ga tegishli haqiqiy qoidalar boshqa narsani tekshiradi va ularning bir qismi default profilda yoqilmagan:

| Qoida | Nimani tekshiradi | Turi | Sonar way da |
|---|---|---|---|
| `xml:S3422` | Bog'liqlikda `system` scope | BUG | Ha |
| `xml:S3421` | Eskirgan `${pom}` prefiksli property | CODE_SMELL | Ha |
| `xml:S3417` | Taqiqlangan bog'liqlik ro'yxati (sozlanadi) | CODE_SMELL | Yo'q |
| `xml:S3423` | `pom.xml` elementlari tavsiya etilgan tartibda | CODE_SMELL | Yo'q |
| `xml:S3419`, `xml:S3420` | `groupId` va `artifactId` nom qoidasi | CODE_SMELL | Yo'q |

Shu jadvaldagi `xml:S3417` amalda eng foydalisi: taqiqlangan bog'liqlik ro'yxatini o'zing yozasan (masalan `commons-logging` yoki ichki eskirgan kutubxona) va u PR da yiqitadi. Lekin u default profilda o'chiq turadi, shuning uchun uni quality profile da qo'lda yoqib, parametrini to'ldirish kerak.

Spring loyihada XML analizatoridan olinadigan eng qimmat ikki qoida esa Maven ga umuman tegishli emas:

```xml
<!-- xml:S3822 (Sonar way da yoqilgan): hbm2ddl.auto "validate" dan boshqa
     qiymatda bo'lsa, sxema o'zgarishi, o'chishi yoki tozalanishi mumkin -->
<session-factory>
  <property name="hibernate.hbm2ddl.auto">update</property>  <!-- shikoyat -->
</session-factory>

<!-- xml:S2068: parol XML ichida ochiq yozilgan -->
<bean id="dataSource" class="...DriverManagerDataSource">
  <property name="password" value="Pr0d-P@ssw0rd"/>           <!-- shikoyat -->
</bean>
```

Bu yerda nozik joy bor: `xml:S3822` faqat XML ni o'qiydi. Spring Boot loyihasida `ddl-auto` odatda `application.yaml` da turadi, va o'sha yerda bu qoida ishga tushmaydi. Ya'ni "Sonar meni `ddl-auto: update` dan himoya qiladi" degan taxmin faqat eski XML konfiguratsiyali loyihada to'g'ri.

Umumiy XML gigiyenasi qoidalari ham bor, lekin ular kutilganidan torroq: uzun qator (`S103`), tabulyatsiya (`S105`), bir xil bo'lmagan otstup (`S1120`), izohga olingan kod (`S125`), prolog `<?xml` bilan boshlanishi (`S1778`), parser xatosi (`S2260`), va o'z XPath ifodangni qoida sifatida yozish imkoni (`S140`). Birinchi beshtasining to'rttasi default profilda yo'q. XXE, ya'ni tashqi DTD obyektini yuklash xavfi esa XML qoidasi emas, u Java tomonidagi parser sozlamasi bo'yicha tekshiriladi.

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

Dockerfile tahlili infratuzilma analizatori orqali keladi va bepul nashrda mavjud. Qoida kalitlari `docker:` prefiksi bilan boshlanadi. Amalda eng ko'p ishlaydiganlari:

| Qoida | Nimani tekshiradi |
|---|---|
| `docker:S6471` | Konteyner imtiyozli foydalanuvchi sifatida ishlaydi |
| `docker:S6596` | Base image tegi aniq emas (`latest` va shunga o'xshash) |
| `docker:S6587` | Paket o'rnatilgandan keyin kesh tozalanmagan |
| `docker:S6472` | Sir qiymati `ENV` yoki `ARG` orqali berilgan |
| `docker:S6437` | Hisob ma'lumoti kodda qotirilgan |
| `docker:S6589` | Faylda bittadan ko'p `ENTRYPOINT` yoki `CMD` |
| `docker:S7019` | `ENTRYPOINT` va `CMD` uchun exec shakli afzal |
| `docker:S7029` | Lokal faylni ko'chirishda `ADD` emas, `COPY` |

Oxirgi qatorda ko'p takrorlanadigan sodda qoidaning aslida ikki tomoni borligi ko'rinadi. `docker:S7029` lokal fayl uchun `COPY` ni talab qiladi, lekin `docker:S7026` teskari yo'nalishda ishlaydi: masofaviy resursni olishda `ADD` ni so'raydi. Ya'ni "`ADD` yomon, `COPY` yaxshi" degan qisqa qoida yarim haqiqat.

Ikki tuzoq esa alohida aytishga arziydi.

Birinchisi, "`apt-get install` da versiyani qotirish" qoidasi mavjud deb o'ylash. Bunday qoida yo'q. Paket menejeri bilan bog'liq qoidalar boshqa narsani ko'radi: keshni tozalash (`S6587`), `update` ni `install` siz bajarish (`S6595`), tavsiya etilgan paketlarni avtomatik o'rnatish (`S6500`), rozilik bayrog'ini qo'ymaslik (`S6584`). Paket versiyasini qotirishni xohlasang, bu Dockerfile review qoidasi bo'ladi, Sonar qoidasi emas.

Ikkinchisi, digest masalasidagi ichki ziddiyat. `docker:S7023` base image ni digest bilan mixlashni so'raydi, `docker:S6497` esa digest bilan image tortishni xavfsizlik nuqtai nazaridan shubhali deb belgilaydi, chunki digest ga mixlangan image xavfsizlik yangilanishini olmaydi. SonarSource bu ziddiyatni oddiy yo'l bilan hal qilgan: ikkalasi ham default `Sonar way` profilida yo'q. Agar o'z profilingda ikkalasini yoqsang, har bir `FROM` qatori ikkita qarama-qarshi shikoyat oladi.

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

Uch eslatma. Birinchi: faylni Sonar ko'rishi uchun u `sonar.sources` ichida bo'lishi kerak, aks holda ildizdagi Dockerfile tahlilga kirmaydi.

Ikkinchi va ko'proq jimgina ishlaydigani: fayl nomi ham mos kelishi kerak. `sonar.docker.file.patterns` ning default qiymati `Dockerfile,*.dockerfile`. Demak `Dockerfile.prod`, `Dockerfile-builder` yoki `docker/app.build` nomli fayl indekslanmaydi va hech qanday xato chiqmaydi, u shunchaki yo'q bo'ladi. Ko'p modulli loyihada bu odatiy holat, shuning uchun naqshni kengaytirish kerak:

```properties
sonar.docker.file.patterns=Dockerfile,*.dockerfile,Dockerfile.*
```

Uchinchi: Sonar image ichidagi CVE larni skanerlamaydi, bu boshqa vositaning ishi.

## 38.7 Kubernetes manifesti: resurs limiti, probe, imtiyozli konteyner

Kubernetes manifestlari ham infratuzilma analizatori hududiga kiradi, qoida kalitlari `kubernetes:` prefiksi bilan boshlanadi. Lekin bu yerda kutish bilan haqiqat orasida ikkita aniq farq bor va ikkalasi ham xavfsizlik rejasiga ta'sir qiladi.

Birinchi farq: **readiness va liveness probe yo'qligi uchun qoida mavjud emas**. Analizator qoidalari orasida probe ni tekshiradigani yo'q. Bu real bo'shliq, chunki probe yo'q Deployment ishlab chiqarishda jimgina buzilgan podga trafik yuboradi. Uni `kubeconform`, `kube-score` yoki OPA/Conftest siyosati bilan yopish kerak.

Ikkinchi farq: resurs chegarasi qoidalari uchta va ularning hammasi default profilda emas.

| Qoida | Nimani tekshiradi | Turi | Sonar way da |
|---|---|---|---|
| `kubernetes:S6864` | Memory limit qo'yilgan | VULNERABILITY | Ha |
| `kubernetes:S6870` | Storage limit qo'yilgan | VULNERABILITY | Ha |
| `kubernetes:S6869` | CPU limit qo'yilgan | VULNERABILITY | **Yo'q** |
| `kubernetes:S6873`, `S6892`, `S6897` | Memory, CPU va storage uchun `requests` | CODE_SMELL | Ha |

Ya'ni default sozlamada CPU limiti yo'q konteyner shikoyat chiqarmaydi, memory limiti yo'q konteyner esa chiqaradi. Agar CPU limiti sening siyosating bo'lsa, `kubernetes:S6869` ni profilda qo'lda yoqish kerak. (CPU limiti har doim ham to'g'ri siyosat emas, bu alohida bahs, lekin qaror ongli bo'lishi kerak, default tanlab bermasin.)

Qolgan qoidalar kutilgandek ishlaydi: `privileged: true` uchun `kubernetes:S6428`, `allowPrivilegeEscalation` uchun `S6430`, host namespace uchun `S6431`, nozik yo'lni mount qilish uchun `S6433` (bu ham Sonar way da emas), `latest` tegi uchun `S6596`, Docker socket uchun `S6429`, RBAC da wildcard uchun `S6867`. Manifest ichida ochiq yozilgan parolni esa Kubernetes qoidasi emas, secret analizatori topadi.

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

Helm bo'yicha eski maslahat endi kerak emas. Analizator ichida Go template evaluatori bor: u `Chart.yaml` turgan papkani topadi, shablonni o'zi hisoblab chiqadi va natijani Kubernetes qoidalari bilan tekshiradi. Ya'ni `helm template` natijasini alohida papkaga chiqarib berish shart emas. Ikkita istisno bor va ular log da ko'rinadi: chart ildizidagi `values.yaml` va `.tpl` fayllari parse qilinmaydi, chunki ular manifest emas. Helm shablonining o'z gigiyenasi uchun esa alohida qoida bor: `kubernetes:S6893` qavslar ichidagi probelni tekshiradi (`{{ .Values.x }}`, `{{.Values.x}}` emas).

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

Frontend tomonida yana bitta jim chegara bor: `sonar.javascript.maxFileSize` ning default qiymati 1000 KB. Undan katta fayl tahlil qilinmaydi. Generatordan chiqqan API klienti yoki bitta katta bundle shu chegaradan oshib, hisobotda umuman ko'rinmasligi mumkin. Agar bunday fayl haqiqatan tahlil qilinishi kerak bo'lsa, chegarani ko'tarish mumkin; ko'pincha esa to'g'ri javob uni `sonar.exclusions` ga ataylab yozib qo'yish, shunda u "tahlil qilindi" deb o'ylanmaydi.

## 38.10 Shell skriptlari va CI konfiguratsiyasi

Shell skriptlari uchun Sonar da to'liq analizator yo'q. Buni aytib qo'yish kerak, chunki ko'p jamoa `scripts/deploy.sh` ni Sonar tekshirishini kutadi. Bash uchun to'g'ri vosita ShellCheck, va uni CI da alohida bosqich sifatida ushlab turish mumkin. Hamma narsa bitta joyda ko'rinishi talab bo'lsa, tashqi vosita natijasini SARIF formatida `sonar.sarifReportPaths` orqali yuklash yo'li bor, lekin issue lar tashqi qoida sifatida ko'rinadi va gate shartlariga ta'siri cheklangan.

Dockerfile uchun esa umumiy SARIF yo'lidan ko'ra yaxshiroq variant bor: infratuzilma analizatori hadolint hisobotini to'g'ridan-to'g'ri qabul qiladi.

```properties
# hadolint natijasini Sonar ga import qilish
sonar.docker.hadolint.reportPaths=target/hadolint-report.json
```

Analizator o'z ichida hadolint qoidalari katalogini (`DL1001`, `DL3000` va hokazo) nom va og'irlik bilan olib yuradi, shuning uchun import qilingan issue lar "noma'lum tashqi qoida" bo'lib emas, tushunarli nom bilan ko'rinadi. Bu Dockerfile ni ikki qatlamda tekshirish imkonini beradi: Sonar ning o'z qoidalari va hadolint ning o'zi.

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
| Default profil | Qoida bor ekan, demak ishlaydi deb o'ylanadi | `Sonar way` da yo'q qoidalar ajratib yoqiladi (CPU limit, taqiqlangan bog'liqlik) |
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
- [ ] Shu filtrda qoidaning `Sonar way` da yoqilganini ham tekshir: `kubernetes:S6869` (CPU limit) va `xml:S3417` (taqiqlangan bog'liqlik) default da o'chiq.
- [ ] `sonar.text.inclusions` ga `**/*.sql` qo'shib, migratsiyadagi parol topilishini bitta soxta parol bilan sinab ko'r; tahlil git repozitoriysi ichida yurgizilayotganini ham tasdiqla.
- [ ] `sonar.docker.file.patterns` ni repozitoriyadagi haqiqiy Dockerfile nomlariga solishtir: `Dockerfile.prod` kabi nomlar default naqshga tushmaydi.
- [ ] Probe yo'qligini tekshiradigan qoida Sonar da yo'q: `kube-score`, `kubeconform` yoki Conftest siyosati bilan shu bo'shliqni yop.
- [ ] `sonar.sources` ga `Dockerfile`, `deploy` va `.github` papkalarini qo'shib, birinchi tahlildan keyin chiqqan infratuzilma issue larini ko'rib chiq.
- [ ] `sonar.exclusions` va `sonar.coverage.exclusions` ni ajrat: generatsiya qilingan kodni birinchisiga, konfiguratsiya klasslarini ikkinchisiga yoz.
- [ ] Frontend uchun alohida loyiha kaliti yaratib, LCOV va `tsconfig` yo'llarini ulab, backend bilan aralashtirmagan holda qamrovni o'lchang.
- [ ] Quality gate ni new code asosiga o'tkaz va infratuzilma loyihasiga coverage sharti qo'ymasdan security rating sharti qo'y.
- [ ] Shell skriptlar uchun CI ga ShellCheck bosqichini qo'shib, natijani majburiy qil, uni Sonar dan kutib o'tirma.
- [ ] Exclusion faylidagi har bir qatorga bir qatorli izoh yozib, uni har chorakda qayta ko'rib chiqadigan vazifa yarat.

## Manbalar

- SonarSource, `sonar-iac` ning Kubernetes qoidalari metadatasi
  ([https://github.com/SonarSource/sonar-iac/tree/1.42.0.14460/iac-extensions/kubernetes/src/main/resources/org/sonar/l10n/kubernetes/rules/kubernetes](https://github.com/SonarSource/sonar-iac/tree/1.42.0.14460/iac-extensions/kubernetes/src/main/resources/org/sonar/l10n/kubernetes/rules/kubernetes),
  tag `1.42.0.14460`, SONAR Source-Available License v1.0) - 38.7 dagi
  qoida ro'yxati, turlari va `Sonar way` profiliga kirmaganlari; probe
  qoidasining yo'qligi shu ro'yxatdan ko'rinadi.
- SonarSource, `sonar-iac` ning Docker qoidalari metadatasi
  ([https://github.com/SonarSource/sonar-iac/tree/1.42.0.14460/iac-extensions/docker/src/main/resources/org/sonar/l10n/docker/rules/docker](https://github.com/SonarSource/sonar-iac/tree/1.42.0.14460/iac-extensions/docker/src/main/resources/org/sonar/l10n/docker/rules/docker),
  tag `1.42.0.14460`, SONAR Source-Available License v1.0) - 38.6 dagi
  qoidalar, `S7023` va `S6497` ziddiyati, paket versiyasi qoidasining
  yo'qligi.
- SonarSource, `DockerSettings`
  ([https://github.com/SonarSource/sonar-iac/blob/1.42.0.14460/iac-extensions/docker/src/main/java/org/sonar/iac/docker/plugin/DockerSettings.java](https://github.com/SonarSource/sonar-iac/blob/1.42.0.14460/iac-extensions/docker/src/main/java/org/sonar/iac/docker/plugin/DockerSettings.java),
  tag `1.42.0.14460`) - 38.6 dagi `sonar.docker.file.patterns` default
  qiymati va 38.10 dagi `sonar.docker.hadolint.reportPaths`.
- SonarSource, `sonar-iac` ning Helm evaluatori
  ([https://github.com/SonarSource/sonar-iac/tree/1.42.0.14460/iac-extensions/kubernetes/src/main/java/org/sonar/iac/helm](https://github.com/SonarSource/sonar-iac/tree/1.42.0.14460/iac-extensions/kubernetes/src/main/java/org/sonar/iac/helm),
  tag `1.42.0.14460`) - 38.7 dagi Helm shablonini analizatorning o'zi
  hisoblashi, `values.yaml` va `.tpl` istisnolari.
- SonarSource, `TextAndSecretsSensor`
  ([https://github.com/SonarSource/sonar-text/blob/2.21.0.5225/sonar-text-plugin/src/main/java/org/sonar/plugins/common/TextAndSecretsSensor.java](https://github.com/SonarSource/sonar-text/blob/2.21.0.5225/sonar-text-plugin/src/main/java/org/sonar/plugins/common/TextAndSecretsSensor.java),
  tag `2.21.0.5225`) - 38.3 dagi `sonar.text.inclusions` default qiymati
  va git kuzatuvi sharti.
- SonarSource, `sonar-xml` qoidalari metadatasi
  ([https://github.com/SonarSource/sonar-xml/tree/2.19.0.8138/sonar-xml-plugin/src/main/resources/org/sonar/l10n/xml/rules/xml](https://github.com/SonarSource/sonar-xml/tree/2.19.0.8138/sonar-xml-plugin/src/main/resources/org/sonar/l10n/xml/rules/xml),
  tag `2.19.0.8138`) - 38.4 dagi Maven qoidalari, `S3822` ning XML bilan
  cheklanishi va `LATEST`/`RELEASE` qoidasining yo'qligi.
- SonarSource, `JavaScriptPlugin`
  ([https://github.com/SonarSource/sonar-javascript/blob/14.1.0.46226/sonar-plugin/sonar-javascript-plugin/src/main/java/org/sonar/plugins/javascript/JavaScriptPlugin.java](https://github.com/SonarSource/sonar-javascript/blob/14.1.0.46226/sonar-plugin/sonar-javascript-plugin/src/main/java/org/sonar/plugins/javascript/JavaScriptPlugin.java),
  tag `14.1.0.46226`) - 38.9 dagi `sonar.typescript.tsconfigPaths`,
  `sonar.javascript.lcov.reportPaths` va `sonar.javascript.maxFileSize`
  default qiymati.

---

[&larr; 37. Taint analysis mexanikasi: source, sink, sanitizer](37-taint-analysis-mexanikasi-source-sink.md) · [Mundarija](README.md) · [39. Bog'liqlik zaifliklari va litsenziya tekshiruvi &rarr;](39-bogliqlik-zaifliklari-va-litsenziya.md)
