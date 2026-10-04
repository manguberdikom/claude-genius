<!-- doc: sonarqube | chapter: 34 | part: VIII. Server va tashkilot -->

[SonarQube](../../README.md) / [SonarQube](README.md)

# 34. Yangilash, LTA migratsiyasi, zaxira va housekeeping (Upgrades, Backup and Housekeeping)

<details>
<summary>Bu bobdagi 12 bo'lim</summary>

- [34.1 LTA (uzoq muddatli) liniya va oraliq versiyalar farqi](#341-lta-uzoq-muddatli-liniya-va-oraliq-versiyalar-farqi)
- [34.2 Yangilash yo'li: qaysi versiyadan qaysi versiyaga sakrash mumkin](#342-yangilash-yoli-qaysi-versiyadan-qaysi-versiyaga-sakrash-mumkin)
- [34.3 Yangilashdan oldin zaxira: ma'lumotlar bazasi va sozlamalar](#343-yangilashdan-oldin-zaxira-malumotlar-bazasi-va-sozlamalar)
- [34.4 Yangilash jarayoni va migratsiya sahifasi](#344-yangilash-jarayoni-va-migratsiya-sahifasi)
- [34.5 Yangilashdan keyin yangi qoidalar yuzlab issue chiqarishi va unga tayyorgarlik](#345-yangilashdan-keyin-yangi-qoidalar-yuzlab-issue-chiqarishi-va-unga-tayyorgarlik)
- [34.6 Qoida o'zgarishi natijalarni qanday siljitadi va qayta bazaviylashtirish (re-baseline)](#346-qoida-ozgarishi-natijalarni-qanday-siljitadi-va-qayta-bazaviylashtirish-re-baseline)
- [34.7 Plugin moslik masalasi va ularni tekshirish](#347-plugin-moslik-masalasi-va-ularni-tekshirish)
- [34.8 Housekeeping sozlamalari: eski tahlil, branch va PR ma'lumotlarini tozalash](#348-housekeeping-sozlamalari-eski-tahlil-branch-va-pr-malumotlarini-tozalash)
- [34.9 Ma'lumotlar bazasi hajmi o'sishi va uni jilovlash](#349-malumotlar-bazasi-hajmi-osishi-va-uni-jilovlash)
- [34.10 Yangilashni avval sinov muhitida o'tkazish tartibi](#3410-yangilashni-avval-sinov-muhitida-otkazish-tartibi)
- [34.11 Orqaga qaytarish rejasi: nega zaxirasiz yangilash xavfli](#3411-orqaga-qaytarish-rejasi-nega-zaxirasiz-yangilash-xavfli)
- [34.12 Amalda qo'llash](#3412-amalda-qollash)

</details>


SonarQube serverni yangilash oddiy `docker pull` emas. Yangilash ma'lumotlar bazasi sxemasini migratsiya qiladi, qoida to'plamini almashtiradi va shu bilan birga butun jamoaning quality gate natijasini siljitadi. Shuning uchun yangilash texnik ish emas, balki rejalashtirilgan o'zgarish boshqaruvi hodisasi. Bu bo'limda yangilash yo'li, zaxira, migratsiya, qoida o'zgarishining ta'siri, housekeeping va orqaga qaytarish rejasi ko'rib chiqiladi.

## 34.1 LTA (uzoq muddatli) liniya va oraliq versiyalar farqi

SonarQube ikki xil relizni chiqaradi. Oraliq (interim) versiyalar tez-tez chiqadi, yangi qoida olib keladi, lekin qisqa muddat qo'llab-quvvatlanadi. LTA, ya'ni uzoq muddatli faol liniya, kamdan-kam chiqadi va uzoq vaqt xavfsizlik hamda bug tuzatishlarini oladi.

Amaliy qoida oddiy. Agar sizda ichki jamoa serveri bo'lsa va uni har oyda yangilashga odam ajratmagan bo'lsangiz, LTA liniyasida turish kerak. Oraliq versiyadan keyingi yangilash yo'li uzoqroq va sinovdan kamroq o'tgan bo'ladi.

9.9 LTA liniyasi va undan keyingi 2025 LTA liniyasi mavjud. Aniq nuqtali versiya raqamini bu yerda yozmayman, chunki ular reliz jadvaliga qarab o'zgaradi. Har bir yangilashdan oldin rasmiy upgrade guide sahifasini va o'sha versiyaning release notes faylini o'qib, qo'llab-quvvatlanadigan Java va ma'lumotlar bazasi versiyalarini tekshiring.

## 34.2 Yangilash yo'li: qaysi versiyadan qaysi versiyaga sakrash mumkin

Asosiy tamoyil shunday: bir LTA liniyasidan keyingisiga to'g'ridan-to'g'ri o'tish qo'llab-quvvatlanadi, lekin ikki LTA ni oshirib tashlab o'tish mumkin emas. Ikki liniya ortda qolgan bo'lsangiz, o'rtadagi LTA ga ko'tarilib migratsiyani tugatasiz, keyin yana yangilaysiz.

Yangilash yo'li faqat server versiyasi bilan cheklanmaydi. Uch narsa birga ko'tariladi: server, scanner (sonar-maven-plugin yoki Gradle sonarqube plugin), hamda ma'lumotlar bazasi va JVM.

| Holat | Qanday yo'l tutish |
|---|---|
| Bir LTA liniyasidan keyingisiga | To'g'ridan-to'g'ri yangilash, bir martalik migratsiya |
| Ikki yoki undan ko'p liniya ortda | O'rtadagi LTA da to'xtab, migratsiyani tugatib, keyin davom etish |
| Oraliq versiyadan LTA ga | Avval release notes dagi breaking changes ro'yxatini o'qish |
| Faqat patch (oxirgi raqam) | Odatda sxema o'zgarmaydi, lekin zaxira baribir olinadi |
| Scanner eski, server yangi | Scanner ni ham ko'tarish, chunki eski scanner yangi qoidani bilmaydi |
| JVM yoki PostgreSQL qo'llab-quvvatlanmaydigan versiyada | Avval platformani ko'tarish, keyin Sonar ni |

Maven tomonida scanner versiyasini aniq qotirib qo'yish yangilashni oldindan aytib beradigan qiladi.

```xml
<!-- Scanner versiyasini aniq qotiramiz, LATEST ishlatmaymiz -->
<properties>
  <sonar.plugin.version>4.0.0.4121</sonar.plugin.version>
</properties>
<build>
  <pluginManagement>
    <plugins>
      <plugin>
        <groupId>org.sonarsource.scanner.maven</groupId>
        <artifactId>sonar-maven-plugin</artifactId>
        <!-- Versiyani bitta joyda boshqaramiz, barcha modul shundan oladi -->
        <version>${sonar.plugin.version}</version>
      </plugin>
    </plugins>
  </pluginManagement>
</build>
```

Bu misoldagi raqam shunchaki namuna. Haqiqiy loyihada serveringiz qo'llab-quvvatlaydigan scanner versiyasini hujjatdan tekshirib yozing.

## 34.3 Yangilashdan oldin zaxira: ma'lumotlar bazasi va sozlamalar

SonarQube holati ikki joyda yashaydi. Birinchisi ma'lumotlar bazasi: loyihalar, issue tarixi, quality profile, quality gate, foydalanuvchi va token. Ikkinchisi data katalogi: qidiruv indeksi va yuklangan plugin fayllari. Qidiruv indeksi qayta qurilishi mumkin, lekin ma'lumotlar bazasi qayta qurilmaydi. Shuning uchun zaxiraning yuragi bu ma'lumotlar bazasi dump fayli.

```bash
#!/usr/bin/env bash
set -euo pipefail

TS=$(date +%Y%m%d-%H%M)
OUT="/backup/sonar/${TS}"
mkdir -p "${OUT}"

# 1) Ma'lumotlar bazasi dump: custom format, keyin tiklash osonroq
PGPASSWORD="${SONAR_DB_PASSWORD}" pg_dump \
  --host="${SONAR_DB_HOST}" --username=sonar --dbname=sonarqube \
  --format=custom --compress=6 --file="${OUT}/sonarqube.dump"

# 2) Sozlama fayllari va plugin katalogi
tar czf "${OUT}/conf-extensions.tgz" \
  /opt/sonarqube/conf /opt/sonarqube/extensions

# 3) Dump ni darhol tekshiramiz: ro'yxat chiqmasa zaxira yaroqsiz
pg_restore --list "${OUT}/sonarqube.dump" > "${OUT}/manifest.txt"
wc -l "${OUT}/manifest.txt"

# 4) Checksum, chunki keyin "shu fayl o'shami" savoli chiqadi
sha256sum "${OUT}"/* > "${OUT}/SHA256SUMS"
echo "Zaxira tayyor: ${OUT}"
```

Dump ni olish bilan ish tugamaydi. Tiklashni sinab ko'rmagan zaxira zaxira emas, u faqat umid. Yangilashdan oldingi haftada dump ni bo'sh bazaga tiklab, Sonar ni o'sha bazaga ulab ko'ring. Quality profile va quality gate konfiguratsiyasini alohida eksport qilib git ga qo'yish ham foydali, chunki migratsiyadan keyin profil farqini ko'rish mumkin bo'ladi.

## 34.4 Yangilash jarayoni va migratsiya sahifasi

Yangilash tartibi qat'iy. Avval tahlil jo'natuvchi CI job larini to'xtatasiz, keyin serverni o'chirasiz, zaxira olasiz, so'ng yangi versiyani ishga tushirasiz. Yangi server darhol ishlashga tayyor bo'lmaydi. U migratsiya kutish holatiga o'tadi va web interfeys `/setup` sahifasiga yo'naltiradi, shu yerda migratsiyani boshlash tugmasi bosiladi.

```bash
# Yangilashdan keyin serverning holatini API orqali kuzatamiz
# Status qiymatlari: STARTING, DB_MIGRATION_NEEDED, DB_MIGRATION_RUNNING, UP
curl -s http://sonar.internal:9000/api/system/status

# Migratsiyani boshlash (faqat DB_MIGRATION_NEEDED holatida)
curl -s -X POST -u "${SONAR_ADMIN_TOKEN}:" \
  http://sonar.internal:9000/api/system/migrate_db

# Migratsiya tugashini kutamiz, loglarni parallel kuzatamiz
until curl -s http://sonar.internal:9000/api/system/status | grep -q '"status":"UP"'; do
  echo "migratsiya davom etmoqda..."
  sleep 15
done

# Log ichida muvaffaqiyatsiz migratsiya qadami bormi
grep -iE "migration|ERROR" /opt/sonarqube/logs/web.log | tail -n 40
```

Migratsiya davomida serverga tahlil jo'natish kerak emas. Katta bazada u o'n daqiqadan bir necha soatgacha davom etishi mumkin, chunki ba'zi qadamlar jadvallarga yangi ustun va indeks qo'shadi. Bu vaqtni oldindan bilishning yagona yo'li sinov muhitida haqiqiy hajmli dump bilan o'tkazib ko'rish.

```yaml
# docker-compose: versiya tegini aniq qotiramiz, latest emas
services:
  sonarqube:
    image: sonarqube:${SONAR_IMAGE_TAG}   # masalan LTA community tegi
    environment:
      SONAR_JDBC_URL: jdbc:postgresql://db:5432/sonarqube
      SONAR_JDBC_USERNAME: sonar
      SONAR_JDBC_PASSWORD: ${SONAR_DB_PASSWORD}
    volumes:
      # Data va extensions nomli volume da, konteyner ichida emas
      - sonar_data:/opt/sonarqube/data
      - sonar_extensions:/opt/sonarqube/extensions
      - sonar_logs:/opt/sonarqube/logs
    ulimits:
      nofile: { soft: 65536, hard: 65536 }
volumes:
  sonar_data:
  sonar_extensions:
  sonar_logs:
```

`latest` tegi yangilashni tasodifiy qiladi. Konteyner qayta ishga tushganda siz bilmagan versiya ko'tarilsa, migratsiya ham sizning ruxsatingizsiz boshlanadi.

## 34.5 Yangilashdan keyin yangi qoidalar yuzlab issue chiqarishi va unga tayyorgarlik

Yangi versiya yangi qoidalarni va yaxshilangan analizatorni olib keladi. Natijada ertalab quality gate qizil bo'lib turadi, garchi hech kim kodga tegmagan bo'lsa ham. Bu nosozlik emas. Yangi qoida eski kodni ham ko'radi, va eski kodda ilgari ko'rinmagan issue lar paydo bo'ladi.

Muhim nuqta shu: yangi issue lar ko'pincha eski kodda topiladi, lekin ularning "yangi kod" sifatida hisoblanishi new code period qanday aniqlanganiga bog'liq. Agar new code period "oldingi versiyadan beri" deb sozlangan bo'lsa, yangilashdan keyin birinchi tahlil yuzlab issue ni yangi kod ustuniga qo'yib yuborishi mumkin. Shuning uchun yangilashni reliz oynasining o'rtasiga emas, oxiriga yoki boshiga rejalashtiring.

Tayyorgarlik ikki qadamdan iborat. Birinchisi, yangilashni avval bitta vakil loyihada o'tkazib, qancha yangi issue chiqishini sanash. Ikkinchisi, gate ni o'chirish o'rniga jamoaga aniq muddat berish, chunki o'chirilgan gate keyin qayta yoqilmaydi.

```java
// Yomon: yangi qoida shikoyat qiladigan tipik joy.
// Hisobot summasini qurganda null bo'lishi mumkin qiymat tekshirilmagan,
// va Optional dan qiymat shartsiz olinyapti.
public BigDecimal hisoblaJami(Buyurtma buyurtma) {
    return buyurtma.getChegirma().get().qiymat()   // Optional shartsiz ochilgan
            .add(buyurtma.getYetkazish().summa()); // null bo'lishi mumkin
}

// Sonar o'tadigan variant: null va bo'sh holat ochiq ifodalangan
public BigDecimal hisoblaJami(Buyurtma buyurtma) {
    BigDecimal chegirma = buyurtma.getChegirma()
            .map(Chegirma::qiymat)
            .orElse(BigDecimal.ZERO);
    BigDecimal yetkazish = Optional.ofNullable(buyurtma.getYetkazish())
            .map(Yetkazish::summa)
            .orElse(BigDecimal.ZERO);
    return chegirma.add(yetkazish);
}
```

Birinchi variant eski versiyada e'tibordan chetda qolib, yangi versiyada belgilanishi mumkin. Tuzatish kodni ham xavfsizroq qiladi, ya'ni ish behuda ketmaydi.

## 34.6 Qoida o'zgarishi natijalarni qanday siljitadi va qayta bazaviylashtirish (re-baseline)

Yangi versiyada uch xil o'zgarish bo'ladi: qoida qo'shiladi, qoida olib tashlanadi yoki birlashtiriladi, va qoidaning jiddiyligi yoki toifasi o'zgaradi. Har uchi ham o'lchovni siljitadi. Qoida olib tashlanganda avvalgi issue lar yopiladi va texnik qarz raqami kamayadi, qoida qo'shilganda teskarisi bo'ladi.

Baholash modeli ham versiyalar orasida o'zgarishi mumkin. Yangi liniyalarda issue lar bitta jiddiylik o'rniga sifat o'lchoviga bog'langan ko'p o'lchovli baholash bilan ko'rsatiladi. Bu gate shartlarining mazmunini o'zgartiradi, shuning uchun ularni yangilashdan keyin qaytadan o'qib chiqish kerak.

Qayta bazaviylashtirish amaliy qadamlardan iborat. Yangilashdan keyin barcha asosiy branch larni bir marta to'liq qayta tahlil qilasiz. Keyin new code period ni yangi reference nuqtaga qo'yasiz, masalan yangilashdan keyingi birinchi reliz versiyasiga. Shundan keyin "yangi kod" o'lchovi yana ma'noli bo'ladi, chunki u yangilash shovqinini o'z ichiga olmaydi.

```properties
# Yangilashdan keyin referens nuqtani ataylab siljitamiz.
# Shunda "yangi kod" yangilash shovqinini emas, haqiqiy yangi ishni o'lchaydi.
sonar.projectKey=ombor-servis
sonar.projectVersion=2026.10.0-post-upgrade

# Scanner CI da gate natijasini kutsin, shunda qizil gate pipeline ni to'xtatadi
sonar.qualitygate.wait=true
sonar.qualitygate.timeout=600

# JaCoCo hisobotining joyi, agregatsiya moduli ishlatilgan holat
sonar.coverage.jacoco.xmlReportPaths=coverage-report/target/site/jacoco-aggregate/jacoco.xml

# Yangilashdan keyin generatsiya qilingan kodni qaytadan chiqaramiz,
# aks holda yangi qoidalar unga ham shikoyat qiladi
sonar.exclusions=**/generated/**,**/*MapperImpl.java,**/target/**
```

Eski issue larni ommaviy "won't fix" qilib yopish yo'li ham bor, lekin u oxirgi chora. Ommaviy yopish odatga aylansa, Sonar natijasiga ishonch yo'qoladi.

## 34.7 Plugin moslik masalasi va ularni tekshirish

Har bir plugin ma'lum server versiya oralig'i bilan ishlaydi. Yangi serverga eski plugin mos kelmasa, server ishga tushmaydi yoki plugin yuklanmay qoladi. Eng ko'p muammo chiqaradigan toifalar: autentifikatsiya pluginlari, qo'shimcha til analizatorlari, va o'zingiz yozgan maxsus qoida pluginlari.

```bash
# O'rnatilgan pluginlar ro'yxati va versiyasi
curl -s -u "${SONAR_ADMIN_TOKEN}:" \
  http://sonar.internal:9000/api/plugins/installed | python3 -m json.tool

# Yangilanishi kerak bo'lgan pluginlar
curl -s -u "${SONAR_ADMIN_TOKEN}:" \
  http://sonar.internal:9000/api/plugins/updates

# Fayl darajasida: extensions katalogidagi jar lar
ls -1 /opt/sonarqube/extensions/plugins/*.jar

# Har bir jar ichidagi manifest qaysi server versiyasini talab qiladi
for j in /opt/sonarqube/extensions/plugins/*.jar; do
  echo "== ${j}"
  unzip -p "${j}" META-INF/MANIFEST.MF | grep -iE "Plugin-Key|Plugin-Version|Sonar-Version"
done
```

O'z maxsus qoida pluginingiz bo'lsa, u eng zaif nuqta. Plugin API versiyalar orasida o'zgaradi va deprecated API olib tashlanishi mumkin. Shu sababli rejada pluginni qayta kompilyatsiya qilish uchun alohida vaqt ajratiladi. Yangilashdan oldin har bir plugin uchun moslik holatini hujjatdan tekshirib jadvalga yozing. Mos kelmaydigan plugin topilsa, ikki variant qoladi: uni olib tashlash yoki yangilashni kutish.

## 34.8 Housekeeping sozlamalari: eski tahlil, branch va PR ma'lumotlarini tozalash

Housekeeping bu Sonar ning ichki tozalash siyosati. U tahlil tarixini qancha saqlashni, snapshot larni qanday birlashtirishni va o'lgan branch bilan yopilgan PR ma'lumotlarini qachon o'chirishni belgilaydi. Standart sozlamalar ko'p branch li loyihada tez yetmaydi.

Eng foydali uchta sozlama shular. Birinchisi, yopilgan PR ma'lumotlarini bir necha kundan keyin o'chirish. Ikkinchisi, faol bo'lmagan feature branch ma'lumotlarini bir necha haftadan keyin o'chirish. Uchinchisi, kunlik snapshot larni haftalik va oylik darajaga birlashtirish. Housekeeping yangilashning bir qismi, chunki migratsiya vaqti baza hajmiga bog'liq. Yangilashdan bir hafta oldin uni qattiqlashtirib bir necha tozalash siklini o'tkazsangiz, migratsiya tezroq o'tadi.

| Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|
| `latest` konteyner tegi bilan ishlash | LTA tegini aniq qotirib, yangilashni ataylab boshlash |
| Zaxirani "ehtimol kerak bo'lmaydi" deb o'tkazib yuborish | Dump olish va uni bo'sh bazaga tiklab sinab ko'rish |
| To'g'ridan-to'g'ri produktsiyada yangilash | Haqiqiy dump nusxasi bilan sinov muhitida avval o'tkazish |
| Yangi issue to'lqinini ko'rib gate ni o'chirib qo'yish | New code period ni qayta bazaviylashtirib, gate ni saqlash |
| Pluginlarni yangilashdan keyin tekshirish | Yangilashdan oldin moslik matritsasini yozib chiqish |
| Housekeeping ni standart holida qoldirish | Branch va PR saqlash muddatini loyiha oqimiga moslash |
| Baza hajmini faqat disk to'lganda ko'rish | Jadval hajmini oyda bir marta o'lchab, trendni kuzatish |
| Scanner versiyasini har modulda alohida yozish | Scanner versiyasini bitta `pluginManagement` da boshqarish |
| Orqaga qaytarishni "serverni qaytaramiz" deb o'ylash | Baza dump ni tiklashni ham o'z ichiga olgan rollback rejasi |

## 34.9 Ma'lumotlar bazasi hajmi o'sishi va uni jilovlash

Sonar bazasi uch yo'nalishda o'sadi: issue jadvali, o'lchov va snapshot jadvallari, hamda fayl manbalari bilan duplikat ma'lumotlari. Eng tez o'sish sababi odatda bitta, ya'ni o'chirilmayotgan qisqa umrli branch va PR tahlillari.

Hajmni o'lchash uchun faqat o'qish so'rovlari ishlatiladi. Sonar sxemasi ichki hisoblanadi va unga qo'lda yozish tavsiya etilmaydi, chunki migratsiya aynan shu sxemaga tayanadi. Jadval nomlari versiyalar orasida o'zgaradi, shuning uchun so'rovdan oldin jadval mavjudligini tekshiring.

```sql
-- Eng katta jadvallar: hajm o'sishining asosiy manbasini topish uchun
SELECT relname AS jadval,
       pg_size_pretty(pg_total_relation_size(c.oid)) AS umumiy_hajm,
       pg_total_relation_size(c.oid) AS bayt
FROM pg_class c
JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname = 'public' AND c.relkind = 'r'
ORDER BY bayt DESC
LIMIT 15;

-- Butun bazaning hajmi, trendni oyda bir marta yozib borish uchun
SELECT pg_size_pretty(pg_database_size(current_database())) AS baza_hajmi;
```

Keyingi qadam sababni aniqlashtirish. Agar branch soni o'nlab emas, yuzlab bo'lsa, housekeeping sozlamasi ishlamayotganini ko'rsatadi.

```sql
-- Loyiha bo'yicha branch va PR soni: housekeeping ishlayaptimi
-- Diqqat: jadval va ustun nomlari versiyaga qarab farq qiladi,
-- shuning uchun avval \d project_branches bilan tekshirib oling.
SELECT p.kee AS loyiha_kaliti,
       b.branch_type AS turi,
       count(*) AS soni
FROM project_branches b
JOIN projects p ON p.uuid = b.project_uuid
GROUP BY p.kee, b.branch_type
HAVING count(*) > 20
ORDER BY soni DESC;
```

Hajmni jilovlashning uchta yo'li bor. Birinchisi housekeeping muddatini qisqartirish. Ikkinchisi tahlil qilinadigan fayllar doirasini `sonar.exclusions` bilan toraytirish, ayniqsa generatsiya qilingan kodni chiqarib tashlash. Uchinchisi keraksiz loyihalarni butunlay o'chirish, chunki arxivlangan loyiha ham joy egallab turadi. PostgreSQL darajasidagi `VACUUM` va indeks holati masalalari arxitektor mindset hujjatidagi PostgreSQL mavzusida yoritilgan.

## 34.10 Yangilashni avval sinov muhitida o'tkazish tartibi

Sinov muhitidagi yangilash bu repetisiya. Maqsadi uchta savolga javob olish: migratsiya qancha vaqt oladi, qaysi plugin sinadi, va qancha yangi issue paydo bo'ladi. Bu savollarga faqat produktsiya bazasining haqiqiy nusxasi javob beradi.

```bash
#!/usr/bin/env bash
set -euo pipefail

# 1) Produktsiya dump ini sinov bazasiga tiklaymiz
createdb -h stage-db -U postgres sonarqube_stage
pg_restore -h stage-db -U postgres -d sonarqube_stage \
  --no-owner --no-privileges /backup/sonar/latest/sonarqube.dump

# 2) Yangilashdan OLDIN o'lchovni yozib olamiz (keyin taqqoslaymiz)
curl -s -u "${TOKEN}:" \
  "http://sonar-stage:9000/api/measures/component?component=ombor-servis&metricKeys=violations,coverage,duplicated_lines_density" \
  > /tmp/oldin.json

# 3) Yangi versiyani ko'taramiz va migratsiya vaqtini o'lchaymiz
START=$(date +%s)
docker compose -f docker-compose.stage.yml up -d
# ... status UP bo'lishini kutish ...
echo "migratsiya sekund: $(( $(date +%s) - START ))"

# 4) Vakil loyihani qayta tahlil qilib, yangi o'lchovni olamiz
./mvnw -B clean verify sonar:sonar -Dsonar.host.url=http://sonar-stage:9000
```

Oldin va keyin o'lchovlarini yonma-yon qo'yib, yangi issue sonini sanaydigan hisobotni jamoaga tarqatish eng foydali qadam. Shunda yangilash kuni hech kim kutilmagan qizil gate dan hayratga tushmaydi. Pipeline ning o'zini tuzish [testlash qo'llanmasidagi](../testing/README.md) CI/CD test pipeline mavzusida bor.

```yaml
# CI da yangilashdan keyin birinchi ishga tushirish: gate ni kutadi,
# lekin natijani bloklovchi emas, ogohlantiruvchi sifatida yozib boradi.
name: sonar-post-upgrade-check
on: { workflow_dispatch: {} }
jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }   # blame uchun to'liq tarix kerak
      - uses: actions/setup-java@v4
        with: { distribution: temurin, java-version: '21' }
      - name: Server versiyasini yozib olamiz
        run: curl -sf "${SONAR_HOST_URL}/api/server/version" | tee server-version.txt
      - name: Tahlil
        continue-on-error: true    # birinchi yugurishda pipeline ni yiqitmaymiz
        run: ./mvnw -B clean verify sonar:sonar -Dsonar.qualitygate.wait=true
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
```

## 34.11 Orqaga qaytarish rejasi: nega zaxirasiz yangilash xavfli

Sonar yangilashida orqaga qaytarish oddiy emas, chunki migratsiya bir tomonlama. Yangi versiya ma'lumotlar bazasi sxemasini o'zgartiradi, va eski versiya o'zgargan sxemani o'qishni bilmaydi. Shuning uchun konteynerni eski tegga qaytarish yetarli emas: eski server yangi sxemaga ulansa ishga tushmaydi.

Demak haqiqiy rollback faqat bitta: eski server versiyasini qaytarish va bazani yangilashdan oldingi dump dan tiklash. Bu migratsiyadan keyin kirgan barcha tahlillarni yo'qotishni bildiradi. Shuning uchun yangilash oynasida CI tahlillari to'xtatiladi.

| Tuzoq | Yechim |
|---|---|
| `latest` teg bilan konteyner qayta ishga tushib, migratsiya o'z-o'zidan boshlanishi | Teg va versiyani aniq qotirish, avtomatik restart siyosatini nazorat qilish |
| Zaxira olingan, lekin tiklash sinovdan o'tmagan | `pg_restore --list` va bo'sh bazaga to'liq tiklash mashqi |
| Eski serverni qaytarib, baza yangi sxemada qolishi | Rollback ni server va baza juftligi sifatida bajarish |
| Migratsiya vaqtida CI tahlil jo'natib turishi | Yangilash oynasida sonar bosqichini CI da o'chirish |
| Yangi issue to'lqini uchun gate ni butunlay o'chirish | New code period ni qayta bazaviylashtirish va muddat belgilash |
| Maxsus qoida plugini yangi API da kompilyatsiya qilinmasligi | Plugin ni yangilashdan oldin yangi API ga qarshi qurib ko'rish |
| Housekeeping sozlanmaganidan baza o'sib, migratsiya cho'zilishi | Yangilashdan oldin tozalash siklini o'tkazish |
| Data katalogi konteyner ichida qolib, plugin va indeks yo'qolishi | `data` va `extensions` ni nomli volume ga chiqarish |
| Scanner eski qolib, yangi qoidalar ishlamasligi | Scanner versiyasini server bilan birga ko'tarish |
| Yangilash reliz oynasining o'rtasida o'tkazilishi | Yangilashni reliz boshiga yoki tugaganiga rejalashtirish |

Oxirgi gap eng muhimi: bu bo'limdagi tartib umumiy prinsip darajasida yozilgan. Aniq versiya raqamlari, qo'llab-quvvatlanadigan JVM va PostgreSQL oralig'i, hamda migratsiya qadamlari har bir reliz bilan o'zgaradi. Yangilashdan oldin o'sha versiyaning rasmiy upgrade guide sahifasini va release notes faylini o'qib, shu rejani unga solishtiring.

## 34.12 Amalda qo'llash

- [ ] Hozirgi server versiyasini `api/server/version` orqali aniqlang va u LTA liniyasidami yoki oraliq versiyadami degan savolga yozma javob bering.
- [ ] Yangilash yo'lini rasmiy upgrade guide bo'yicha tekshirib, oraliq to'xtashlar kerakmi yoki yo'qmi degan qarorni hujjatlashtiring.
- [ ] `pg_dump` zaxira skriptini yozib, uni bo'sh bazaga tiklash mashqini bir marta bajarib ko'ring va ketgan vaqtni yozib qo'ying.
- [ ] O'rnatilgan pluginlar ro'yxatini `api/plugins/installed` dan chiqarib, har biri uchun moslik holatini jadvalga yozing.
- [ ] Produktsiya dump nusxasi bilan sinov muhitida yangilashni o'tkazib, migratsiya vaqtini va yangi issue sonini o'lchab oling.
- [ ] Housekeeping sozlamalarini loyiha branch oqimiga moslab qisqartiring va bir necha tozalash siklidan keyin baza hajmini qayta o'lchang.
- [ ] Yangilashdan keyin new code period ni yangi referens versiyaga qo'yib, barcha asosiy branch larni bir marta to'liq qayta tahlil qiling.
- [ ] Rollback rejasini bitta sahifada yozing: kim bajaradi, qaysi dump ishlatiladi, qancha ma'lumot yo'qoladi va qaror qanday mezon bilan qabul qilinadi.

---

[&larr; 33. Serverni o'rnatish, sozlash va resurs rejalashtirish](33-serverni-ornatish-sozlash-va-resurs.md) · [Mundarija](README.md) · [35. Foydalanuvchi, guruh, huquqlar, token va SSO &rarr;](35-foydalanuvchi-guruh-huquqlar-token-va-sso.md)
