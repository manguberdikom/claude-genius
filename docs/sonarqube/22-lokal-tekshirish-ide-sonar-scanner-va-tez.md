<!-- doc: sonarqube | chapter: 22 | part: VI. Amaliyot va jarayon -->

[Barcha hujjatlar](../../README.md) / [SonarQube](README.md)

# 22. Lokal tekshirish: IDE, sonar-scanner va tez qaytish (Local Feedback Loop)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

- [22.1 Nega xatoni CI da emas, yozayotganda ko'rish arzonroq](#221-nega-xatoni-ci-da-emas-yozayotganda-korish-arzonroq)
- [22.2 SonarLint ni IDE ga o'rnatish va ishlatish](#222-sonarlint-ni-ide-ga-ornatish-va-ishlatish)
- [22.3 Connected mode: server profilini IDE ga tortib olish](#223-connected-mode-server-profilini-ide-ga-tortib-olish)
- [22.4 Lokal to'liq tahlilni ishga tushirish va natijani ko'rish](#224-lokal-toliq-tahlilni-ishga-tushirish-va-natijani-korish)
- [22.5 JaCoCo hisobotini lokal ochib, qaysi qator qamralmaganini ko'rish](#225-jacoco-hisobotini-lokal-ochib-qaysi-qator-qamralmaganini-korish)
- [22.6 Commit oldidan tekshirish: pre-commit hook va uning chegarasi](#226-commit-oldidan-tekshirish-pre-commit-hook-va-uning-chegarasi)
- [22.7 IDE ogohlantirishlari va Sonar natijasi mos kelmasligi sabablari](#227-ide-ogohlantirishlari-va-sonar-natijasi-mos-kelmasligi-sabablari)
- [22.8 Tez qaytish uchun tekshiruvlarni bosqichlarga bo'lish](#228-tez-qaytish-uchun-tekshiruvlarni-bosqichlarga-bolish)
- [22.9 Jamoada bir xil sozlama: formatlash, linter, IDE konfiguratsiyasi](#229-jamoada-bir-xil-sozlama-formatlash-linter-ide-konfiguratsiyasi)
- [22.10 Lokal tahlilni tezlashtirish: faqat o'zgargan modulni tekshirish](#2210-lokal-tahlilni-tezlashtirish-faqat-ozgargan-modulni-tekshirish)
- [22.11 Amalda qo'llash](#2211-amalda-qollash)

</details>



Sonar natijasini faqat CI da ko'rish eng qimmat yo'l. Kod yozilgan payt bilan xato ko'rilgan payt orasida qancha vaqt o'tsa, tuzatish shuncha qimmatga tushadi. Bu bobda xatoni IDE da, keyin lokal `sonar-scanner` da, keyin pre-commit hookda tutib olish yo'li ko'rsatiladi. Maqsad bitta: CI ga faqat allaqachon toza bo'lgan kod borishi.

## 22.1 Nega xatoni CI da emas, yozayotganda ko'rish arzonroq

Tuzatish narxi vaqt bilan o'sadi, chunki kontekst yo'qoladi. Kod yozayotganda metodning nega shunday yozilganini yodda tutasan. Yarim kundan keyin CI qizil bo'lganda esa qaytib kirib, kontekstni boshidan tiklash kerak. Bu tiklash ishi kodni tuzatishning o'zidan ko'proq vaqt oladi.

CI orqali qaytish halqasi uzun. Push qilasan, runner navbatda turadi, build ketadi, test ketadi, keyin Sonar tahlil qiladi. Oddiy Spring loyihada bu 6 dan 20 daqiqagacha. Agar bitta cognitive complexity ogohlantirishi uchun shu halqani uch marta aylantirsan, bir soat yo'qoladi.

Yana bir narxi bor: PR dagi review. Reviewer Sonar ogohlantirishini o'qib, komment yozadi, sen tuzatasan, u yana qaraydi. Bu ikki kishining vaqti. IDE da ko'rilgan ogohlantirish esa hech kimning vaqtini olmaydi.

Shu sababli tekshiruvni uch bosqichga tarqatish kerak. IDE bir necha sekundda javob beradi. Lokal to'liq tahlil bir necha daqiqada. CI esa oxirgi to'siq bo'lib, quality gate ni hal qiladi. CI ni birinchi tekshirish joyi sifatida ishlatish, bu kompilyatorni server orqali chaqirishga o'xshaydi.

## 22.2 SonarLint ni IDE ga o'rnatish va ishlatish

SonarLint 2024 yildan beri "SonarQube for IDE" nomi bilan ham tarqatiladi. Ikki nom bir mahsulotni anglatadi, versiyaga qarab plugin katalogida biri yoki ikkinchisi ko'rinadi. IntelliJ IDEA da `Settings > Plugins > Marketplace` ichidan `SonarQube for IDE` deb qidiriladi va o'rnatiladi. VS Code va Eclipse uchun ham xuddi shu plugin bor.

O'rnatilgandan keyin u standalone rejimda ishlaydi. Ya'ni serverga ulanmasdan, o'zida bor qoidalar to'plami bilan faylni tekshiradi. Bu rejimda ko'p narsa topiladi: null dereference ehtimoli, ishlatilmagan o'zgaruvchi, noto'g'ri `equals`, murakkab metod. Lekin bu to'plam sening serveringdagi profil bilan bir xil emas.

Muhim sozlama: tahlil qachon ishlashi. Standart holatda u faqat ochilgan fayl uchun ishlaydi. Butun loyihani IDE ichidan tekshirish uchun `Analyze All Project Files` buyrug'i bor, lekin katta loyihada u sekin. Amalda to'g'ri odat: ochilgan fayl uchun avtomatik, modul uchun esa lokal `sonar-scanner`.

IDE da tahlil uchun kerakli JVM ni ham belgilash kerak. Plugin o'z Java jarayonini ishga tushiradi, va u loyihaning Java versiyasidan farq qilishi mumkin.

```properties
# .idea/sonarlint/ ichidagi sozlama IDE orqali yoziladi, qo'lda tahrirlanmaydi.
# Loyiha darajasida muhim bo'lgan narsa: tahlildan chiqarilgan fayllar.
# Generatsiya qilingan kodni IDE tahlilidan ham chiqarib tashlash kerak.
sonar.exclusions=**/generated/**,**/target/generated-sources/**,**/*_.java
# Test fayllari alohida toifaga kiradi, ularga boshqa qoidalar qo'llanadi.
sonar.test.inclusions=**/src/test/java/**
# Coverage hisoboti yo'li IDE uchun kerak emas, lekin scanner uchun shart.
sonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml
```

## 22.3 Connected mode: server profilini IDE ga tortib olish

Standalone rejimning asosiy muammosi shu: IDE sening serveringdagi quality profile ni bilmaydi. Agar jamoa ba'zi qoidalarni o'chirgan yoki jiddiylikni o'zgartirgan bo'lsa, IDE buni ko'rmaydi. Natijada ikki xil haqiqat paydo bo'ladi.

Connected mode shu farqni yo'qotadi. Plugin serverga ulanadi, loyihaning quality profile ini, o'chirilgan qoidalarni va `New Code` chegarasini tortib oladi. Shundan keyin IDE da ko'ringan narsa server aytadigan narsaga yaqin bo'ladi.

Ulanish uchun token kerak. Token foydalanuvchi nomidan beriladi va parol o'rnini bosadi. Uni IDE ga qo'lda kiritasan, repozitoriyga hech qachon yozmaysan.

```bash
# 1. Serverda token yaratish: My Account > Security > Generate Tokens.
# Token turi "User Token" bo'lsin, "Project Analysis Token" faqat scanner uchun.

# 2. Ulanish ishlayotganini terminalda tekshirish:
curl -s -u "$SONAR_TOKEN:" \
  "https://sonar.company.uz/api/authentication/validate"
# Kutilgan javob: {"valid":true}

# 3. Loyihaning amaldagi quality profile ini ko'rish:
curl -s -u "$SONAR_TOKEN:" \
  "https://sonar.company.uz/api/qualityprofiles/search?project=payment-service" \
  | python3 -m json.tool

# 4. New Code chegarasi qanday sozlanganini bilish:
curl -s -u "$SONAR_TOKEN:" \
  "https://sonar.company.uz/api/new_code_periods/show?project=payment-service"
```

Connected mode yana bitta foyda beradi: serverda `Won't Fix` yoki `False Positive` deb belgilangan issue lar IDE da ham ko'rinmaydi. Bu shovqinni sezilarli kamaytiradi. Taxminan hafta davomida jamoa IDE ga ishonishni boshlaydi, chunki u yolg'on ogohlantirish bermaydi.

Connected mode ni butun jamoa uchun bir xil qilish kerak. Agar yarim jamoa standalone ishlasa, "menda ko'rinmayapti" bahsi qaytib keladi.

## 22.4 Lokal to'liq tahlilni ishga tushirish va natijani ko'rish

IDE hamma narsani topmaydi. Duplicated blocks, coverage, va butun loyiha bo'ylab hisoblanadigan metrikalar faqat to'liq tahlilda chiqadi. Shuning uchun PR ochishdan oldin bir marta lokal to'liq tahlil qilish foydali.

Maven loyihada tartib shunday: avval test va JaCoCo, keyin scanner. Tartibni buzish eng ko'p uchraydigan xato, chunki `sonar:sonar` ni alohida chaqirsang, JaCoCo hisoboti hali yo'q bo'ladi va coverage nol ko'rinadi.

```bash
# To'liq lokal tahlil: test, coverage, keyin scanner. Bitta zanjirda.
export SONAR_TOKEN='squ_xxxxxxxxxxxxxxxx'
export SONAR_HOST_URL='https://sonar.company.uz'

mvn -B clean verify \
    org.sonarsource.scanner.maven:sonar-maven-plugin:sonar \
    -Dsonar.projectKey=payment-service \
    -Dsonar.host.url="$SONAR_HOST_URL" \
    -Dsonar.token="$SONAR_TOKEN"

# Natija serverga yuboriladi, lekin quality gate javobini kutmaydi.
# Javobni kutish uchun alohida flag kerak:
mvn -B sonar:sonar -Dsonar.qualitygate.wait=true -Dsonar.qualitygate.timeout=300

# Gradle da xuddi shu ish:
./gradlew clean test jacocoTestReport sonar \
    -Dsonar.token="$SONAR_TOKEN" -Dsonar.host.url="$SONAR_HOST_URL"
```

Natijani ko'rishning ikki yo'li bor. Birinchisi brauzerda loyiha sahifasi, bu eng aniq. Ikkinchisi terminalda qaytgan `ANALYSIS SUCCESSFUL, you can find the results at ...` qatori, u to'g'ridan to'g'ri havola beradi.

Diqqat qiladigan narsa: lokal tahlil ham serverdagi natijani almashtiradi. Agar sen branch nomini bermasang, tahlil asosiy branch ustiga yozilib qolishi mumkin. Shu sababli lokal tahlilda `sonar.branch.name` ni albatta ko'rsatish kerak, yoki alohida `-local` suffiksli projectKey ishlatish kerak.

## 22.5 JaCoCo hisobotini lokal ochib, qaysi qator qamralmaganini ko'rish

Sonar coverage ni o'zi o'lchamaydi. U JaCoCo bergan XML ni o'qiydi. Ya'ni "coverage past" muammosini hal qilish uchun Sonar kerak emas, JaCoCo ning o'z HTML hisoboti yetarli va u tezroq.

JaCoCo HTML hisoboti qator darajasida rang beradi. Yashil qator bajarilgan, qizil bajarilmagan, sariq esa shart qisman qamralgan. Sariq eng muhim signal, chunki u `if (a && b)` dagi bitta shox tekshirilmaganini ko'rsatadi. Sonar buni `Conditions to cover` deb hisoblaydi.

```xml
<!-- pom.xml: JaCoCo XML va HTML hisobotini birga chiqarish. -->
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <version>0.8.12</version>
  <executions>
    <execution>
      <id>jacoco-prepare</id>
      <goals><goal>prepare-agent</goal></goals>
    </execution>
    <execution>
      <!-- report goal ni verify ga bog'lash kerak, aks holda XML yozilmaydi. -->
      <id>jacoco-report</id>
      <phase>verify</phase>
      <goals><goal>report</goal></goals>
    </execution>
  </executions>
</plugin>
```

Hisobotni ochish juda oddiy, lekin ko'pchilik buni bilmaydi va to'g'ridan to'g'ri Sonar sahifasiga qaraydi.

```bash
# Faqat test va hisobot, scanner yo'q. Eng tez halqa.
mvn -B -q clean verify -DskipITs

# HTML hisobotni brauzerda ochish:
xdg-open target/site/jacoco/index.html   # Linux
# open target/site/jacoco/index.html     # macOS

# Qamralmagan qatorlarni terminalda sanash, XML dan to'g'ridan to'g'ri:
python3 - <<'PY'
import xml.etree.ElementTree as ET
t = ET.parse('target/site/jacoco/jacoco.xml')
for cls in t.iter('class'):
    missed = [l.get('nr') for l in cls.iter('line') if l.get('mi') != '0']
    if missed:
        print(cls.get('name'), '->', ','.join(missed[:15]))
PY
```

Bu skript qaysi klassning qaysi qatori qamralmaganini chiqaradi. Shundan keyin test yozish aniq ishga aylanadi. Qamrovni qanday test bilan to'ldirish kerakligi [testlash qo'llanmasidagi](../testing/README.md) unit test mavzusida batafsil.

Bitta ogohlantirish: `mi` atributi "missed instructions" degani, qator umuman bajarilmaganini bildirmaydi. Lekin amaliy maqsad uchun bu yetarli signal.

## 22.6 Commit oldidan tekshirish: pre-commit hook va uning chegarasi

Pre-commit hook arzon tekshiruvlar uchun yaxshi. Formatlash, oddiy statik tahlil, kompilyatsiya. Lekin unga to'liq Sonar tahlilini qo'yish xato, chunki har commit da bir necha daqiqa kutish jamoani hookni o'chirishga majbur qiladi.

```bash
#!/usr/bin/env bash
# .githooks/pre-commit  -  faqat tez tekshiruvlar.
set -euo pipefail

# O'zgargan Java fayllarni olish, o'chirilganlarni tashlab.
FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.java$' || true)
[ -z "$FILES" ] && exit 0

# 1. Formatlash: avtomatik tuzatadi va qaytib stage ga qo'yadi.
mvn -B -q spotless:apply
echo "$FILES" | xargs git add

# 2. Kompilyatsiya: sintaksis xatosi commit ga tushmasin.
mvn -B -q compile -o || { echo "Kompilyatsiya buzilgan, commit to'xtatildi."; exit 1; }

# 3. Secret tekshiruvi: token yoki parol qo'shilmaganini ko'rish.
if git diff --cached | grep -nE '(squ_|AKIA[0-9A-Z]{16}|password\s*=\s*"[^"]{4,})'; then
  echo "Diff da sir bo'lishi mumkin. Tekshirib, keyin commit qil."
  exit 1
fi
echo "Pre-commit tekshiruvlari o'tdi."
```

Hookni jamoaga tarqatish uchun `core.hooksPath` ishlatiladi, chunki `.git/hooks` repozitoriyga tushmaydi.

```bash
# Bir marta sozlash, keyin hamma uchun ishlaydi.
git config core.hooksPath .githooks
chmod +x .githooks/pre-commit

# Tekshirish:
git config --get core.hooksPath

# Zudlik bo'lsa hookni chetlab o'tish mumkin, bu ataylab qoldirilgan:
git commit --no-verify -m "hotfix: to'lov statusi"
```

Hookning chegarasi aniq: u majburiy emas. `--no-verify` har doim bor, va u bo'lishi ham kerak. Shu sababli hook sifat kafolati emas, balki qulaylik. Majburiy qoidalar faqat CI da va quality gate da yashashi mumkin.

| Tuzoq | Nega yuz beradi | Yechim |
|---|---|---|
| Lokal coverage 0%, serverda 80% | `sonar:sonar` `verify` dan oldin ishladi, XML hali yo'q | `clean verify` va `sonar` ni bitta zanjirda chaqir |
| IDE da ogohlantirish yo'q, CI da bor | standalone rejim, server profili tortilmagan | connected mode ni yoq |
| Lokal tahlil asosiy branch natijasini buzdi | `sonar.branch.name` berilmagan | lokal uchun alohida projectKey yoki branch nomi ber |
| Pre-commit hook 4 daqiqa ishlaydi | hookka to'liq test yoki scanner qo'yilgan | hookda faqat format va compile qoldir |
| Duplicated blocks faqat CI da chiqadi | IDE butun loyihani ko'rmaydi | PR oldidan bir marta to'liq lokal tahlil |
| Sariq qatorlar e'tibordan chetda | faqat line coverage raqamiga qaralgan | JaCoCo HTML da branch ranglarini ko'r |
| Hook `--no-verify` bilan chetlab o'tiladi | hook majburiy emas | majburiy shartni quality gate ga ko'chir |
| Jamoada har xil format diff keltiradi | IDE sozlamalari sinxron emas | Spotless va EditorConfig ni repoga qo'y |

## 22.7 IDE ogohlantirishlari va Sonar natijasi mos kelmasligi sabablari

Bu savol har jamoada chiqadi va javobi odatda beshta sababdan bittasi. Birinchisi rejim: standalone IDE o'z qoidalar to'plamini ishlatadi, server esa quality profile ni. Ikkinchisi versiya: IDE plugin ichidagi analyzer versiyasi serverdagidan yangi yoki eski bo'lishi mumkin, va yangi qoidalar faqat bir tarafda bor.

Uchinchisi qamrov doirasi. IDE bitta faylni ko'radi, server butun loyihani. Shu sababli cross-file muammolar, duplicated code va `New Code` hisobi faqat serverda chiqadi. To'rtinchisi scope: fayl `sonar.exclusions` ga tushgan bo'lsa serverda umuman tahlil qilinmaydi, IDE esa uni ko'rib turadi.

Beshinchisi va eng chalkashi: `New Code` chegarasi. Serverdagi quality gate ko'p shartni faqat yangi kod uchun o'lchaydi. IDE esa butun faylni tekshiradi. Shu sababli IDE 20 ta ogohlantirish ko'rsatganda, quality gate faqat ikkitasini hisoblashi mumkin.

```bash
# Farqni aniqlash: serverdagi aniq issue ro'yxatini olib, IDE bilan solishtirish.
curl -s -u "$SONAR_TOKEN:" \
  "$SONAR_HOST_URL/api/issues/search?componentKeys=payment-service:src/main/java/uz/pay/PaymentService.java&resolved=false" \
  | python3 -c 'import json,sys; d=json.load(sys.stdin); [print(i["rule"], i.get("line"), i["message"][:60]) for i in d["issues"]]'

# Serverdagi analyzer versiyalarini ko'rish, IDE plugin versiyasi bilan solishtirish uchun:
curl -s -u "$SONAR_TOKEN:" "$SONAR_HOST_URL/api/plugins/installed" \
  | python3 -c 'import json,sys; [print(p["key"], p["version"]) for p in json.load(sys.stdin)["plugins"]]'
```

Agar farq topilsa, javob bitta: serverni haqiqat manbasi deb hisobla. IDE tezkor yordamchi, hakam emas.

## 22.8 Tez qaytish uchun tekshiruvlarni bosqichlarga bo'lish

Barcha tekshiruvni bitta buyruqqa yig'ish jozibali, lekin sekin. To'g'ri yondashuv bosqichlash: har bosqich oldingisidan qimmatroq va kamroq ishga tushadi.

| Bosqich | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Sintaksis | kompilyatsiyani CI kutadi | IDE da darhol, incremental compile |
| Formatlash | review da qo'lda aytiladi | Spotless pre-commit da avtomatik tuzatadi |
| Oddiy code smell | CI dagi Sonar aytadi | IDE connected mode da yozayotganda |
| Unit test | push dan keyin runner ishlaydi | lokal `verify -DskipITs`, 1 daqiqa |
| Coverage | Sonar sahifasida ko'riladi | JaCoCo HTML lokal ochiladi |
| Integratsion test | har push da to'liq | lokal faqat o'zgargan modulda, CI da to'liq |
| Duplicated code | hech kim qaramaydi | PR oldidan bir marta to'liq lokal tahlil |
| Quality gate | PR qizil bo'lganda bilinadi | lokal `qualitygate.wait` bilan oldindan |
| Secret | review da tasodifan topiladi | pre-commit grep va CI scanner, ikki qavat |
| Arxitektura qoidasi | og'zaki kelishuv | ArchUnit testi, lokal ham ishlaydi |

CI tomonida ham shu bosqichlash kerak. Tez ishlar oldin, qimmatlari keyin. Agar `fast` job yiqilsa, Sonar jobini umuman ishga tushirmaslik kerak.

```yaml
# .github/workflows/ci.yml  -  bosqichli pipeline.
name: ci
on: [pull_request]
jobs:
  fast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with: { java-version: '21', distribution: 'temurin', cache: 'maven' }
      # Format va kompilyatsiya: 1-2 daqiqa, darhol javob beradi.
      - run: mvn -B -q spotless:check compile

  analysis:
    needs: fast          # fast yiqilsa, bu job umuman ishlamaydi
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }   # New Code hisobi uchun to'liq tarix shart
      - uses: actions/setup-java@v4
        with: { java-version: '21', distribution: 'temurin', cache: 'maven' }
      - run: mvn -B clean verify sonar:sonar -Dsonar.qualitygate.wait=true
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
```

`fetch-depth: 0` ni yozib qo'yish muhim. Sayoz clone da Sonar New Code ni to'g'ri aniqlay olmaydi va yangi kod o'rniga butun faylni yangi deb hisoblashi mumkin.

## 22.9 Jamoada bir xil sozlama: formatlash, linter, IDE konfiguratsiyasi

Agar har kim o'z IDE sozlamasi bilan ishlasa, diff lar formatlash o'zgarishlari bilan to'ladi. Sonar bunda ikki marta zarar ko'radi: birinchidan New Code hajmi sun'iy o'sadi, ikkinchidan review da haqiqiy o'zgarish ko'rinmay qoladi.

Yechim sozlamani repozitoriyga ko'chirish. Formatlash qoidasi `pom.xml` da yashaydi va Spotless orqali majburlanadi. Tahrirlovchi xulqi `.editorconfig` da yashaydi va deyarli hamma IDE uni o'qiydi.

```xml
<!-- pom.xml: Spotless. Formatlash qoidasi kodda yashaydi, IDE da emas. -->
<plugin>
  <groupId>com.diffplug.spotless</groupId>
  <artifactId>spotless-maven-plugin</artifactId>
  <version>2.44.0</version>
  <configuration>
    <java>
      <googleJavaFormat><style>AOSP</style></googleJavaFormat>
      <removeUnusedImports/>
      <!-- Ishlatilmagan import Sonar da ham code smell, shu yerda yo'qoladi. -->
      <trimTrailingWhitespace/>
      <endWithNewline/>
    </java>
  </configuration>
  <executions>
    <execution>
      <!-- check ni verify ga bog'lash: CI da ham, lokal da ham bir xil. -->
      <goals><goal>check</goal></goals>
      <phase>verify</phase>
    </execution>
  </executions>
</plugin>
```

Connected mode sozlamasini ham umumiy qilish mumkin. IntelliJ `.idea/sonarlint` papkasini yozadi va unda server ulanishi nomi hamda projectKey bog'lanishi saqlanadi. Bu fayllarni repozitoriyga qo'shish mumkin, lekin token hech qachon unda bo'lmaydi: token har bir developerning o'z IDE kalit saqlovchisida qoladi.

Yana bitta amaliy qoida: Java versiyasi bir xil bo'lsin. Agar birov Java 17 da, boshqasi Java 25 da kompilyatsiya qilsa, ba'zi Sonar qoidalari boshqacha ishlaydi. `maven.compiler.release` ni `pom.xml` da qattiq belgilash kerak, va `.sdkmanrc` yoki shunga o'xshash fayl bilan JDK ni ham qayd qilish kerak.

## 22.10 Lokal tahlilni tezlashtirish: faqat o'zgargan modulni tekshirish

Ko'p modulli loyihada butun reaktorni tahlil qilish uzoq ketadi. Maven da `-pl` va `-am` flaglari shuni hal qiladi. `-pl` qaysi modul, `-am` esa uning bog'liqliklarini ham qurishni bildiradi.

```bash
# 1. Diff dan o'zgargan modullarni topish.
BASE=${1:-origin/main}
MODULES=$(git diff --name-only "$BASE"...HEAD \
  | awk -F/ '/^[a-z0-9-]+\/src\//{print $1}' | sort -u | paste -sd, -)

if [ -z "$MODULES" ]; then
  echo "Java modullarda o'zgarish yo'q, tahlil kerak emas."
  exit 0
fi
echo "O'zgargan modullar: $MODULES"

# 2. Faqat shu modullarni va ularning bog'liqliklarini qurish va testlash.
mvn -B -T 1C clean verify -pl "$MODULES" -am -DskipITs

# 3. Shu modullar uchun lokal Sonar tahlili, alohida branch nomi bilan.
mvn -B sonar:sonar -pl "$MODULES" \
  -Dsonar.branch.name="local-$(git rev-parse --abbrev-ref HEAD)" \
  -Dsonar.token="$SONAR_TOKEN"
```

Tezlikni oshiradigan boshqa vositalar ham bor. `-T 1C` har protsessor yadrosiga bitta thread beradi va ko'p modulli build ni sezilarli tezlashtiradi. `-o` offline rejim, bog'liqliklar allaqachon yuklangan bo'lsa tarmoqqa chiqmaydi. `-DskipITs` integratsion testlarni tashlab ketadi, ular odatda eng sekin qismi.

Lekin bitta ogohlantirish bor va u muhim. Qisman tahlil Sonar da to'liq rasmni bermaydi. Agar sen faqat bitta modulni tahlil qilib yuborsan, qolgan modullarning oldingi natijasi serverda eski holida qoladi. Shu sababli qisman tahlil lokal ishchi vositasi, CI da esa har doim to'liq tahlil bo'lishi kerak.

Duplicated code ayniqsa shunday. U modullar orasida ham topiladi, shuning uchun bitta modulni tahlil qilib "takrorlanish yo'q" degan xulosa chiqarish xato. Quality gate hisobini faqat CI dagi to'liq tahlil beradi.

## 22.11 Amalda qo'llash

- [ ] IDE ga SonarQube for IDE pluginini o'rnat va server bilan connected mode ni yoq, shundan keyin IDE profili server profiliga mos keladi.
- [ ] `curl -s -u "$SONAR_TOKEN:" "$SONAR_HOST_URL/api/authentication/validate"` bilan tokenni tekshir va uni faqat IDE kalit saqlovchisida qoldir.
- [ ] JaCoCo `report` goal ini `verify` fazasiga bog'la, keyin `mvn clean verify -DskipITs` ishlatib `target/site/jacoco/index.html` ni ochib qizil va sariq qatorlarni ko'r.
- [ ] `.githooks/pre-commit` yoz: Spotless apply, offline compile va secret grep, keyin `git config core.hooksPath .githooks` ni bajar.
- [ ] Spotless va `.editorconfig` ni repozitoriyga qo'shib, `spotless:check` ni `verify` fazasiga bog'la, shunda formatlash diff lari yo'qoladi.
- [ ] CI da `fast` va `analysis` joblarini ajrat, `analysis` ga `needs: fast` qo'y va checkout da `fetch-depth: 0` ber.
- [ ] Ko'p modulli loyihada diff dan modul nomini topib `mvn verify -pl <modullar> -am -T 1C` bilan lokal halqani qisqartir, lekin CI da to'liq tahlil qoldir.
- [ ] PR ochishdan oldin bir marta `mvn clean verify sonar:sonar -Dsonar.qualitygate.wait=true` ni lokal branch nomi bilan ishlatib, gate javobini oldindan ko'r.

---

[&larr; 21. CI/CD ga ulash, PR decoration va blokirovka](21-ci-cd-ga-ulash-pr-decoration-va-blokirovka.md) · [Mundarija](README.md) · [23. Legacy loyihani 100% ga olib chiqish rejasi &rarr;](23-legacy-loyihani-100-ga-olib-chiqish-rejasi.md)
