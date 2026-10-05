<!-- doc: sonarqube | chapter: 42 | part: X. Amaliy ma'lumotnoma -->

[Barcha hujjatlar](../../README.md) / [SonarQube](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 42. Diagnostika: tahlil ishlamaganda nima qilish (Troubleshooting)

<details>
<summary>Bu bobdagi 17 bo'lim</summary>

- [42.1 Diagnostika tartibi](#421-diagnostika-tartibi)
- [42.2 Belgi va sabab: umumiy jadval](#422-belgi-va-sabab-umumiy-jadval)
- [42.3 Coverage 0% ko'rinadi](#423-coverage-0-korinadi)
- [42.4 Yangi kod bo'sh yoki noto'g'ri aniqlanadi](#424-yangi-kod-bosh-yoki-notogri-aniqlanadi)
- [42.5 Tahlil "project not found" yoki kalit mos kelmasligi bilan tushadi](#425-tahlil-project-not-found-yoki-kalit-mos-kelmasligi-bilan-tushadi)
- [42.6 Scanner xotira yetishmasligidan tushadi](#426-scanner-xotira-yetishmasligidan-tushadi)
- [42.7 Tahlil juda uzoq davom etadi](#427-tahlil-juda-uzoq-davom-etadi)
- [42.8 Java versiyasi mos kelmasligi va kompilyatsiya qilingan klass topilmasligi](#428-java-versiyasi-mos-kelmasligi-va-kompilyatsiya-qilingan-klass-topilmasligi)
- [42.9 Pull request tahlili ko'rinmaydi yoki izohlar qo'yilmaydi](#429-pull-request-tahlili-korinmaydi-yoki-izohlar-qoyilmaydi)
- [42.10 Gate natijasi CI da kutilmaydi yoki noto'g'ri o'qiladi](#4210-gate-natijasi-ci-da-kutilmaydi-yoki-notogri-oqiladi)
- [42.11 Issue lar kutilmaganda ko'payib ketdi](#4211-issue-lar-kutilmaganda-kopayib-ketdi)
- [42.12 Fayllar tahlilga umuman kirmagan](#4212-fayllar-tahlilga-umuman-kirmagan)
- [42.13 Test fayllari manba sifatida hisoblangan](#4213-test-fayllari-manba-sifatida-hisoblangan)
- [42.14 Server javob bermaydi yoki navbat to'lib qolgan](#4214-server-javob-bermaydi-yoki-navbat-tolib-qolgan)
- [42.15 Tuzoq va yechim](#4215-tuzoq-va-yechim)
- [42.16 Oddiy yondashuv va arxitektor yondashuvi](#4216-oddiy-yondashuv-va-arxitektor-yondashuvi)
- [42.17 Amalda qo'llash](#4217-amalda-qollash)

</details>



Sonar tahlili buzilganda ko'pchilik birinchi navbatda quality gate shartini o'zgartirishga urinadi. Bu xato yo'l, chunki aksariyat hollarda muammo gate da emas, balki scanner ga berilgan ma'lumotda yoki loyiha kalitida bo'ladi. Bu bob diagnostikani aniq tartibda olib borishni o'rgatadi: avval belgi, keyin sabab farazi, keyin tekshirish buyrug'i, keyin yechim. Har bir bo'limda log da nimani izlash kerakligi ko'rsatilgan, chunki scanner o'z ishini batafsil yozib boradi va javob deyarli har doim log ichida turadi.

## 42.1 Diagnostika tartibi

Tahlil natijasi kutilganidan farq qilganda tekshirishni pastdan yuqoriga olib boring. Pastda build turadi, yuqorida quality gate turadi. Agar build noto'g'ri bo'lsa, gate ni sozlash hech narsani tuzatmaydi.

Tartib shunday bo'ladi. Birinchi qadam: build o'zi muvaffaqiyatli tugadimi va test lar haqiqatan ishga tushdimi. Ikkinchi qadam: coverage hisoboti fayl sifatida diskda mavjudmi va uning ichi bo'sh emasmi. Uchinchi qadam: scanner shu faylni ko'rdimi va o'qidimi. To'rtinchi qadam: scanner qaysi loyiha kalitiga va qaysi branch ga yozdi. Beshinchi qadam: server shu tahlilni qabul qildimi va navbatda qayta ishladimi. Oltinchi qadam: new code davri to'g'ri aniqlandimi. Yettinchi qadam: quality gate qaysi shartda qulab tushdi.

Har bir qadamda bitta buyruq va bitta log so'zini izlang. Birinchi uchta qadamni mahalliy mashinada tekshirish mumkin, server kerak emas. Shuning uchun ularga ko'proq vaqt bering.

```bash
# Diagnostikaning birinchi uch qadami, serversiz
# 1-qadam: test lar ishladimi va qancha test bajarildi
mvn -q clean verify | tail -40
ls -1 target/surefire-reports/*.xml | wc -l

# 2-qadam: JaCoCo XML hisoboti bormi va bo'sh emasmi
ls -la target/site/jacoco/jacoco.xml
grep -c "<counter" target/site/jacoco/jacoco.xml

# 3-qadam: scanner shu faylni ko'rdimi (batafsil log bilan)
mvn sonar:sonar -Dsonar.verbose=true 2>&1 | tee /tmp/sonar.log
grep -i -E "jacoco|coverage|report path" /tmp/sonar.log
```

## 42.2 Belgi va sabab: umumiy jadval

Bu jadval diagnostikaning xaritasi. Belgini topib, eng ehtimolli sabablar ro'yxatini birinchi ustundan o'qing va shu tartibda tekshiring.

| Belgi | Eng ehtimolli sabab | Birinchi tekshiruv | Qayerda hal qilinadi |
|---|---|---|---|
| Coverage 0% | XML hisobot yo'q yoki yo'li noto'g'ri | `ls target/site/jacoco/jacoco.xml` | build konfiguratsiyasi |
| Coverage 0%, hisobot bor | scanner hisobot yo'lini bilmaydi | `grep -i jacoco` scanner log da | scanner xossasi |
| Coverage past, lekin test bor | test lar skip bo'lgan yoki module boshqa | `mvn verify` chiqishidagi test soni | build buyrug'i |
| New code bo'sh | reference branch server da topilmagan | loyiha New Code sozlamasi | server sozlamasi |
| New code butun loyiha | SCM ma'lumoti yo'q, shallow clone | `git log --oneline -5` | CI checkout qadami |
| "project not found" turidagi xato | `sonar.projectKey` mos emas | `grep projectKey` log da | scanner xossasi |
| Avtorizatsiya rad etildi | token eskirgan yoki huquqi yetmaydi | token bilan `curl` tekshiruvi | server huquqlari |
| Scanner OutOfMemory | heap kichik, loyiha katta | `SONAR_SCANNER_OPTS` qiymati | CI muhit o'zgaruvchisi |
| Tahlil juda uzoq | ortiqcha fayl va generated kod kiritilgan | `sonar.exclusions` ro'yxati | scanner xossasi |
| Klass topilmadi turidagi ogohlantirish | `verify` dan oldin tahlil ishga tushgan | build qadamlar ketma-ketligi | CI pipeline |
| Java versiyasi mos emas | bytecode va `sonar.java.source` farqi | `java -version` va `mvn -v` | muhit va build |
| PR tahlili ko'rinmaydi | PR xossalari berilmagan | `grep pullrequest` log da | CI pipeline |
| Gate natijasi CI da o'qilmaydi | `sonar.qualitygate.wait` yoqilmagan | pipeline qadami chiqishi | CI pipeline |
| Issue lar keskin ko'paydi | quality profile yoki Sonar versiyasi yangilangan | loyiha tarixidagi sana | server sozlamasi |
| Fayllar tahlilga kirmagan | `sonar.sources` yoki exclusion xato | indekslangan fayl soni log da | scanner xossasi |
| Test kodi manba sifatida | `sonar.tests` ko'rsatilmagan | log dagi indekslash bo'limi | scanner xossasi |
| Server javob bermaydi | navbat to'lgan yoki resurs tugagan | server sog'ligi so'rovi | server infratuzilmasi |

## 42.3 Coverage 0% ko'rinadi

Belgi: tahlil muvaffaqiyatli tugaydi, issue lar ko'rinadi, lekin coverage ustuni 0.0% yoki bo'sh turadi. Bu eng ko'p uchraydigan muammo va uning sababi deyarli hamisha bitta: Sonar o'zi coverage ni o'lchamaydi, uni JaCoCo o'lchaydi, Sonar esa faqat tayyor XML hisobotni o'qiydi. Shuning uchun sabablarni shu zanjir bo'ylab ketma-ket tekshirish kerak.

Sabablar ketma-ketligi shunday. Birinchi: JaCoCo agent umuman ulanmagan, ya'ni `prepare-agent` goal build da yo'q. Ikkinchi: agent ulangan, lekin `report` goal yo'q, shuning uchun `jacoco.exec` bor, XML yo'q. Uchinchi: XML bor, lekin scanner boshqa yo'lga qaraydi. To'rtinchi: test lar `-DskipTests` bilan o'tkazib yuborilgan, shuning uchun XML bo'sh counter lar bilan yozilgan. Beshinchi: multi module loyihada har bir module o'z hisobotini yozadi, scanner esa faqat bittasini ko'radi. Oltinchi: tahlil `verify` dan oldin, alohida buyruqda ishga tushgan va o'sha paytda hisobot hali yo'q edi. Yettinchi: coverage exclusion ro'yxati shunchalik keng ki, hisoblanadigan kod qolmagan.

Tekshirish usuli oddiy. Avval faylning o'zi borligini va ichida haqiqiy raqamlar borligini ko'ring, keyin scanner log ida shu fayl yo'li aytilganini toping. Log da JaCoCo sensor ishga tushganini va hisobot yo'lini bildiradigan qatorlar bo'ladi, shunga o'xshash xabarni kalit so'z bilan izlang.

```bash
# JaCoCo exec va XML ikkisi ham bormi
find . -name "jacoco.exec" -o -name "jacoco.xml" | head -20

# XML ichida nol bo'lmagan qoplama bormi (covered atributi)
grep -o 'covered="[0-9]*"' target/site/jacoco/jacoco.xml | sort -u | head

# scanner log ida JaCoCo sensori va yo'l haqidagi qatorlarni izlash
grep -n -i -E "jacoco|xmlReportPaths|no coverage" /tmp/sonar.log

# test lar chindan ishladimi yoki skip bo'ldimi
grep -n -i -E "Tests run|skipTests|No tests to run" /tmp/sonar.log
```

Yechim: `prepare-agent` va `report` goal larini bitta plugin ichida bog'lang, XML yo'lini scanner ga aniq aytib qo'ying va tahlilni `verify` fazasidan keyin ishga tushiring. Multi module loyihada barcha module hisobotlarini bitta ro'yxatda, vergul bilan sanab bering yoki aggregate hisobot yarating.

```xml
<!-- JaCoCo: agent va XML hisobot. Versiyani loyihangiz talabiga moslang -->
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <version>0.8.12</version>
  <executions>
    <execution>
      <!-- test lardan oldin agentni ulash -->
      <id>agent</id>
      <goals><goal>prepare-agent</goal></goals>
    </execution>
    <execution>
      <!-- test lardan keyin XML hisobot yozish -->
      <id>report</id>
      <phase>verify</phase>
      <goals><goal>report</goal></goals>
    </execution>
  </executions>
</plugin>
```

```properties
# Coverage hisobot yo'llari. Multi module da vergul bilan sanaladi
sonar.coverage.jacoco.xmlReportPaths=\
  payment-service/target/site/jacoco/jacoco.xml,\
  order-service/target/site/jacoco/jacoco.xml
# Generated kod coverage hisobidan chiqariladi, lekin issue lar qoladi
sonar.coverage.exclusions=**/dto/**,**/config/**,**/*Application.java
```

Alohida holat: test lar bor, o'tadi, lekin coverage deyarli oshmaydi. Bunda tahlil buzilmagan, test haqiqiy kodni ishga tushirmayotgan bo'ladi.

```java
// Muammo: hamma narsa mock, shuning uchun haqiqiy kod bajarilmaydi
@Test
void limitTekshiruvi_mockBilan() {
    PaymentService service = mock(PaymentService.class);   // tekshirilayotgan klass mock
    when(service.pay(any())).thenReturn(Result.REJECTED);
    assertEquals(Result.REJECTED, service.pay(request));   // mock ni tekshiradi
}

// Yechim: tekshirilayotgan klass haqiqiy, faqat tashqi bog'liqlik mock
@Test
void limitTekshiruvi_haqiqiyKodBilan() {
    PaymentService service = new PaymentService(gatewayMock, limitPolicy);
    Result result = service.pay(new PaymentRequest("ORD-1", new BigDecimal("1200")));
    assertEquals(Result.REJECTED, result);                 // haqiqiy mantiq bajarildi
}
```

## 42.4 Yangi kod bo'sh yoki noto'g'ri aniqlanadi

Belgi: quality gate "New Code" shartlarini tekshiradi, lekin yangi kod qatorlari nol ko'rinadi yoki aksincha butun loyiha yangi deb hisoblanadi. Ikkinchi holatda gate butun tarixiy qarz uchun qulab tushadi va jamoa tahlilga ishonchini yo'qotadi.

Sabab uchta joydan keladi. Birinchi: new code davri loyiha sozlamasida noto'g'ri tanlangan, masalan reference branch sifatida server da mavjud bo'lmagan branch ko'rsatilgan. Ikkinchi: CI shallow clone qiladi, shuning uchun git tarixi yo'q va Sonar qaysi qator qachon o'zgarganini aniqlay olmaydi. Uchinchi: SCM provider aniqlanmagan, masalan ishchi katalog git repository emas yoki `.git` papkasi konteynerga tushmagan.

Tekshirish usuli: mahalliy git tarixi chuqurligini va scanner log idagi SCM bo'limini ko'ring. Log da blame ma'lumoti to'planayotgani yoki SCM ma'lumoti yo'qligi haqida shunga o'xshash ogohlantirish bo'ladi.

```bash
# Tarix chuqurligi: shallow clone bo'lsa bu fayl mavjud bo'ladi
test -f .git/shallow && echo "SHALLOW clone, tarix to'liq emas"
git rev-list --count HEAD

# Reference branch mahalliy va remote da bormi
git branch -r | grep -E "origin/(main|develop|release)"

# scanner log ida SCM va blame bo'limi
grep -n -i -E "scm|blame|shallow" /tmp/sonar.log
```

Yechim: CI da to'liq tarixni oling va reference branch ni server da mavjud branch ga qaratib qo'ying. Reference branch ni belgilash usuli Sonar versiyasiga qarab farq qiladi, shuning uchun avval loyihaning New Code sozlamalarini interfeysdan tasdiqlang.

```yaml
# GitHub Actions: Sonar uchun to'liq tarix shart
- uses: actions/checkout@v4
  with:
    # 0 degani butun tarix, shallow clone o'chiriladi
    fetch-depth: 0
- name: Build va tahlil
  run: mvn -B clean verify sonar:sonar
  env:
    SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

## 42.5 Tahlil "project not found" yoki kalit mos kelmasligi bilan tushadi

Belgi: scanner serverga ulanadi, lekin loyihani topa olmaydi yoki huquq yetmasligini aytadi. Xabar matni versiyaga qarab farq qiladi, shunga o'xshash "project not found" yoki "insufficient privileges" mazmunidagi qator bo'ladi.

Sabab to'rtta. Birinchi: `sonar.projectKey` qiymati server dagi kalitdan farq qiladi, masalan `com.shop:payment` va `shop-payment` adashtirilgan. Ikkinchi: loyiha hali yaratilmagan va server da avtomatik yaratish o'chirilgan. Uchinchi: token boshqa loyihaga bog'langan project token. To'rtinchi: `sonar.host.url` noto'g'ri, masalan reverse proxy orqasidagi kontekst yo'li tushib qolgan.

Tekshirish usuli: avval kalitni log dan o'qing, keyin shu kalitni server API orqali so'rang. Agar API javobi bo'sh bo'lsa, kalit mos emas. Agar javob huquq xatosi bo'lsa, muammo token da.

```bash
# scanner qaysi kalit va qaysi URL bilan ishlaganini log dan o'qish
grep -n -E "projectKey|host.url|Project key" /tmp/sonar.log

# server dagi loyiha haqiqatan shu kalit bilan mavjudmi
curl -s -u "$SONAR_TOKEN:" \
  "$SONAR_HOST/api/projects/search?projects=com.shop:payment-service" | head -c 400

# token umuman ishlayaptimi (autentifikatsiya tekshiruvi)
curl -s -o /dev/null -w "%{http_code}\n" -u "$SONAR_TOKEN:" \
  "$SONAR_HOST/api/authentication/validate"
```

Yechim: kalitni bitta joyda, `pom.xml` yoki `sonar-project.properties` ichida saqlang va CI dan qayta bermang. Kalitni hech qachon branch nomi yoki build raqami bilan aralashtirmang, aks holda har build yangi loyiha yaratadi va new code tarixi yo'qoladi.

## 42.6 Scanner xotira yetishmasligidan tushadi

Belgi: tahlil o'rtasida jarayon `OutOfMemoryError` bilan to'xtaydi yoki CI konteyneri jarayonni o'ldiradi. Ko'pincha bu katta monolit loyihalarda, generated kod ko'p bo'lganda yoki juda uzun fayllar mavjud bo'lganda yuz beradi.

Sabab ikkitadir. Birinchi: scanner JVM heap i kichik, chunki hech kim uni sozlamagan. Ikkinchi: konteynerning umumiy xotira limiti heap dan kichik, shuning uchun OS jarayonni o'ldiradi va log da hatto xato ham qolmaydi.

Tekshirish usuli: log oxiridagi qatorni ko'ring. Agar `OutOfMemoryError` bo'lsa, heap kichik. Agar log hech qanday xatosiz kesilgan bo'lsa va exit kod 137 bo'lsa, konteyner limiti sabab.

```bash
# Oxirgi build ning chiqish kodi: 137 konteyner o'ldirganini bildiradi
echo "exit code: $?"

# log da xotira haqidagi qatorlar
grep -n -E "OutOfMemory|GC overhead|Killed" /tmp/sonar.log

# scanner uchun heap ni oshirish (Maven plugin orqali ishlaganda MAVEN_OPTS)
export SONAR_SCANNER_OPTS="-Xmx4g"
export MAVEN_OPTS="-Xmx4g"
mvn -B clean verify sonar:sonar
```

Yechim: heap ni oshirish birinchi qadam, lekin yakuniy yechim emas. Tahlilga kiradigan fayl hajmini kamaytirish ko'proq foyda beradi, chunki generated kod va minifikatsiya qilingan resurslar tahlilga hech qanday qiymat qo'shmaydi. Konteyner limitini heap dan kamida 25 foiz kattaroq qilib qo'ying.

## 42.7 Tahlil juda uzoq davom etadi

Belgi: Sonar qadami butun pipeline vaqtining yarmidan ko'pini oladi. Jamoa buni sezadi va tahlilni faqat kechasi ishlaydigan qadamga ko'chirishni so'raydi, bu esa fikr qaytishini sekinlashtiradi.

Sabab bir nechta. Birinchi: `node_modules`, `target`, `build` va generated manbalar indekslanmoqda. Ikkinchi: juda katta bitta fayl tahlilga kirgan, masalan SQL dump yoki minifikatsiya qilingan JS. Uchinchi: har build da butun tarix bo'yicha blame qayta o'qilmoqda, chunki SCM cache ishlamaydi. To'rtinchi: server navbati band va scanner javobni kutib turadi, ya'ni sekinlik scanner da emas.

Tekshirish usuli: log dagi sensor vaqtlarini o'qing. Scanner har bir sensor uchun ketgan vaqtni yozadi, shuning uchun eng qimmat qadamni topish mumkin.

```bash
# Eng uzoq ishlagan sensorlarni topish
grep -E "Sensor .* \(done\)" /tmp/sonar.log | sort -t= -k2 -rn | head -15

# Indekslangan fayl soni: kutilganidan katta bo'lsa exclusion kerak
grep -n -E "files indexed|indexing" /tmp/sonar.log

# Eng katta manba fayllarni topish
find src -type f -name "*.java" -size +200k -exec ls -lh {} \;
```

```properties
# Tahlil hajmini kamaytirish: generated va qurilgan kod chiqariladi
sonar.sources=src/main/java,src/main/resources
sonar.exclusions=**/target/**,**/build/**,**/node_modules/**,\
  **/generated/**,**/*.min.js,**/db/migration/**
# Katta binar va dump fayllar
sonar.exclusions=${sonar.exclusions},**/*.sql.gz,**/*.pdf
```

## 42.8 Java versiyasi mos kelmasligi va kompilyatsiya qilingan klass topilmasligi

Belgi: tahlil tugaydi, lekin issue lar soni kutilganidan ancha kam. Log da bytecode topilmagani yoki tilning versiyasi mos emasligi haqida shunga o'xshash ogohlantirish bo'ladi. Bu holat xavfli, chunki tahlil "yashil" ko'rinadi, lekin aslida yarim ishlagan.

Sabab uchta. Birinchi: tahlil `compile` dan oldin ishga tushgan, shuning uchun `target/classes` bo'sh. Ikkinchi: CI dagi JDK versiyasi loyiha talabidan past, masalan kod Java 21 xususiyatlaridan foydalanadi, JDK 17 bilan parsing xato beradi. Uchinchi: `sonar.java.source` qiymati haqiqiy kompilyatsiya versiyasiga mos emas. Sonar ning qaysi JDK versiyasida ishlashi va qaysi til versiyasini tahlil qila olishi server versiyasiga qarab farq qiladi, shuning uchun yangilanishdan oldin moslik jadvalini tekshirish kerak.

Tekshirish usuli: JDK versiyalarini va `target/classes` ichidagi klass sonini ko'ring, keyin log dagi bytecode haqidagi ogohlantirishni izlang.

```bash
# Scanner qaysi JDK da ishlayapti va Maven qaysi JDK ni ko'radi
java -version 2>&1 | head -2
mvn -v | head -3

# Kompilyatsiya qilingan klasslar bormi
find . -path "*/target/classes" -name "*.class" | wc -l

# log da bytecode va til versiyasi haqidagi ogohlantirishlar
grep -n -i -E "bytecode|binaries|not compiled|source version|preview" /tmp/sonar.log
```

Yechim: tahlilni har doim `verify` yoki kamida `test-compile` dan keyin ishga tushiring va `sonar.java.binaries` ni aniq ko'rsating. Java versiyasini build fayli va CI muhitida bir xil qiymatda saqlang.

```properties
# Bytecode yo'llari: bularsiz ko'p qoida ishga tushmaydi
sonar.java.binaries=target/classes
sonar.java.test.binaries=target/test-classes
sonar.java.libraries=target/dependency/*.jar
# Til versiyasi kompilyatsiya versiyasiga teng bo'lishi kerak
sonar.java.source=21
```

## 42.9 Pull request tahlili ko'rinmaydi yoki izohlar qo'yilmaydi

Belgi: PR ochilgan, CI o'tgan, lekin Sonar da PR alohida ko'rinmaydi. Yoki PR ko'rinadi, ammo GitHub yoki GitLab ichida izoh va status yo'q.

Sabab to'rtta. Birinchi: PR xossalari scanner ga berilmagan, shuning uchun tahlil branch tahlili sifatida yozilgan. Ikkinchi: CI "detached HEAD" holatida ishlaydi va branch nomi aniqlanmagan. Uchinchi: DevOps platforma integratsiyasi server da sozlanmagan yoki uning token i eskirgan. To'rtinchi: branch va PR tahlili litsenziya yoki edition cheklovi ostida, bu imkoniyat barcha edition larda mavjud emas.

Tekshirish usuli: log da PR kaliti, source va target branch qiymatlari borligini ko'ring. Agar ular bo'sh bo'lsa, scanner PR ekanini bilmagan.

```bash
# PR xossalari scanner ga yetib bordimi
grep -n -E "pullrequest|branch.name|Branch name" /tmp/sonar.log

# Server da shu PR ro'yxatga olindimi
curl -s -u "$SONAR_TOKEN:" \
  "$SONAR_HOST/api/project_pull_requests/list?project=com.shop:payment-service" \
  | head -c 400
```

```yaml
# PR tahlili: kalit va branch nomlari aniq beriladi
- name: Sonar PR tahlili
  if: github.event_name == 'pull_request'
  run: |
    mvn -B clean verify sonar:sonar \
      -Dsonar.pullrequest.key=${{ github.event.number }} \
      -Dsonar.pullrequest.branch=${{ github.head_ref }} \
      -Dsonar.pullrequest.base=${{ github.base_ref }}
  env:
    SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

## 42.10 Gate natijasi CI da kutilmaydi yoki noto'g'ri o'qiladi

Belgi: Sonar interfeysida quality gate qizil, lekin CI yashil tugaydi. Yoki aksincha, CI xato qaytaradi, lekin sababi tushunarsiz.

Sabab ikkitadir. Birinchi: scanner tahlilni serverga yuborib, javobni kutmasdan chiqib ketadi, chunki kutish rejimi yoqilmagan. Tahlil server navbatida asinxron qayta ishlanadi, shuning uchun scanner ning muvaffaqiyatli chiqishi gate o'tganini bildirmaydi. Ikkinchi: pipeline gate natijasini o'qiydi, lekin branch yoki PR ni noto'g'ri ko'rsatadi, shuning uchun eski tahlil natijasini ko'radi.

Tekshirish usuli: kutish rejimini yoqing va natijani alohida qadamda API dan o'qib ko'ring. Tahlil vazifasining holati `report-task.txt` faylida yozilgan bo'ladi.

```bash
# Scanner yozgan vazifa ma'lumoti
cat target/sonar/report-task.txt

# Vazifa holatini so'rash: SUCCESS bo'lgandan keyingina gate ni o'qish mantiqiy
TASK_ID=$(grep '^ceTaskId=' target/sonar/report-task.txt | cut -d= -f2)
curl -s -u "$SONAR_TOKEN:" "$SONAR_HOST/api/ce/task?id=$TASK_ID"

# Gate holatini o'qish
curl -s -u "$SONAR_TOKEN:" \
  "$SONAR_HOST/api/qualitygates/project_status?projectKey=com.shop:payment-service"
```

Yechim: `sonar.qualitygate.wait=true` ni yoqing va timeout qiymatini CI qadami uchun aniq belgilang. Gate natijasini o'qiyotgan skript branch yoki PR parametrini scanner bilan bir xil berishi kerak.

## 42.11 Issue lar kutilmaganda ko'payib ketdi

Belgi: kod o'zgarmagan, lekin bir kunda issue soni yuzlab oshdi. Jamoa buni "Sonar buzildi" deb qabul qiladi, aslida sabab boshqa.

Sabab uchta. Birinchi: quality profile yangilangan yoki yangi qoidalar yoqilgan. Ikkinchi: server yoki Java analyzer plugini yangi versiyaga o'tgan va mavjud qoidalar aniqroq ishlay boshlagan. Uchinchi: exclusion ro'yxati o'zgargan va ilgari tahlildan tashqarida bo'lgan katta modul ichkariga kirgan.

Tekshirish usuli: loyiha tarixida sakrash sodir bo'lgan sanani toping, keyin shu sanadagi profile o'zgarishini va server yangilanishini solishtiring. Sonar profile o'zgarishlari tarixini saqlaydi, shuning uchun bu taqqoslash aniq javob beradi.

```bash
# Loyihada ishlatilgan profile va uning oxirgi o'zgarishi
curl -s -u "$SONAR_TOKEN:" \
  "$SONAR_HOST/api/qualityprofiles/search?project=com.shop:payment-service"

# Issue larni yaratilgan sanaga ko'ra guruhlab ko'rish
curl -s -u "$SONAR_TOKEN:" \
  "$SONAR_HOST/api/issues/search?componentKeys=com.shop:payment-service&facets=createdAt&ps=1"
```

Yechim: profile o'zgarishini alohida, rejalashtirilgan ish sifatida qabul qiling. Yangi qoidalarni butun tarixga emas, new code ga qarshi qo'llang. Eski kod uchun qarzni alohida backlog da yuritish jamoani blok qilmaydi.

## 42.12 Fayllar tahlilga umuman kirmagan

Belgi: Sonar da loyiha bor, lekin fayl soni haqiqiy kodga mos kelmaydi. Masalan 400 ta Java faylli loyiha uchun 12 ta fayl ko'rsatiladi.

Sabab to'rtta. Birinchi: `sonar.sources` noto'g'ri katalogga qaratilgan. Ikkinchi: exclusion pattern juda keng, masalan `**/*Service*` kabi ehtiyotsiz qoida. Uchinchi: multi module loyihada faqat ildiz module tahlil qilingan, chunki `mvn` buyrug'i submodule ichida ishga tushgan. To'rtinchi: fayl kodlash muammosi tufayli ba'zi fayllar o'qilmagan.

Tekshirish usuli: scanner log ida indekslangan fayl sonini va ko'rib chiqilgan katalog ro'yxatini o'qing. Bu raqamni `find` natijasi bilan solishtiring.

```bash
# Haqiqiy fayl soni
find src/main/java -name "*.java" | wc -l

# Scanner nechta fayl indeksladi va qaysi katalogdan
grep -n -E "indexed|Base dir|Source paths|Excluded" /tmp/sonar.log

# Kodlash muammosi bo'lgan fayllarni qidirish
grep -n -i -E "encoding|unsupported character" /tmp/sonar.log
```

## 42.13 Test fayllari manba sifatida hisoblangan

Belgi: issue lar ichida test klasslari ko'rinadi, coverage past hisoblanadi va duplikatsiya ko'rsatkichi sun'iy ravishda oshib ketadi. Sababi oddiy: Sonar test kodini manba kod deb qabul qilgan.

Sabab ikkitadir. Birinchi: `sonar.tests` ko'rsatilmagan, shuning uchun `src/test/java` ham manba sifatida indekslangan. Ikkinchi: test kodi manba katalogi ichida yotadi, masalan integratsion test lar `src/main` ostida qolib ketgan.

Tekshirish usuli: Sonar interfeysida bitta test faylni oching va uning turini ko'ring. Log da manba va test katalogi ro'yxati alohida yoziladi, shuni solishtiring.

```properties
# Manba va test kodi aniq ajratiladi
sonar.sources=src/main/java
sonar.tests=src/test/java,src/integrationTest/java
sonar.test.inclusions=**/*Test.java,**/*Tests.java,**/*IT.java
# Test kodidagi duplikatsiya ko'pincha normal, shuning uchun chiqariladi
sonar.cpd.exclusions=**/*Test.java,**/*IT.java
```

Yechim: test kodini alohida source set ga chiqaring va `sonar.tests` ni doim to'ldiring. Testlash qo'llanmasidagi integratsion test larni ajratish mavzusi bu ajratishni build darajasida qanday qilishni tushuntiradi.

## 42.14 Server javob bermaydi yoki navbat to'lib qolgan

Belgi: scanner tahlilni yuboradi, lekin natija interfeysda paydo bo'lmaydi. Yoki tahlil "pending" holatida uzoq turadi. Bu holat scanner muammosi emas, server muammosi.

Sabab to'rtta. Birinchi: Compute Engine navbati band, chunki bir vaqtda juda ko'p katta tahlil kelgan. Ikkinchi: ma'lumotlar bazasi sekin yoki disk joy tugagan. Uchinchi: Elasticsearch indeksi buzilgan va server read-only rejimga o'tgan. To'rtinchi: reverse proxy so'rov hajmi limiti tufayli katta tahlil hisobotini o'tkazmagan.

Tekshirish usuli: avval server sog'ligini va navbat holatini so'rang, keyin server log ini ko'ring. Javobda navbatdagi vazifalar soni va ularning kutish vaqti bo'ladi.

```bash
# Server sog'ligi va tizim holati
curl -s -u "$SONAR_TOKEN:" "$SONAR_HOST/api/system/health"
curl -s -u "$SONAR_TOKEN:" "$SONAR_HOST/api/system/status"

# Navbatdagi va ishlayotgan tahlil vazifalari
curl -s -u "$SONAR_TOKEN:" "$SONAR_HOST/api/ce/activity_status"

# Server log larida xato darajasidagi qatorlar
grep -n -E "ERROR|WARN" /opt/sonarqube/logs/ce.log | tail -30
grep -n -E "ERROR|read-only|disk" /opt/sonarqube/logs/es.log | tail -20
```

Yechim: navbat muntazam to'lib turadigan bo'lsa, Compute Engine worker sonini va server resurslarini oshirish kerak. Tahlil hajmini kamaytirish ham yordam beradi, chunki kichik hisobot tezroq qayta ishlanadi. Ma'lumotlar bazasidagi eski tahlil snapshot larini tozalash siyosatini yoqib qo'ying.

Ba'zan muammo ma'lumotlar bazasi darajasida bo'ladi. Bunda jadval hajmini ko'rish qaysi ma'lumot o'sib ketganini aytadi.

```sql
-- Eng katta jadvallarni topish: issue va snapshot tarixi odatda birinchi o'rinda
SELECT relname AS jadval,
       pg_size_pretty(pg_total_relation_size(relid)) AS hajm
FROM pg_catalog.pg_statio_user_tables
ORDER BY pg_total_relation_size(relid) DESC
LIMIT 10;
```

## 42.15 Tuzoq va yechim

| Tuzoq | Nima uchun xato | Yechim |
|---|---|---|
| Coverage 0% ni ko'rib gate chegarasini pasaytirish | sabab o'lchovda, chegarada emas | XML hisobot zanjirini tuzatish |
| Tahlilni `verify` dan oldin ishga tushirish | bytecode va hisobot hali yo'q | tahlilni `verify` dan keyinga qo'yish |
| Har branch uchun yangi projectKey | new code tarixi yo'qoladi | kalitni bitta joyda qotirish |
| Shallow clone ni qoldirish | blame va new code ishlamaydi | `fetch-depth: 0` qo'yish |
| Heap ni cheksiz oshirish | konteyner jarayonni o'ldiradi | exclusion bilan hajmni kamaytirish |
| Issue ko'payganda qoidalarni o'chirish | real muammolar yashiriladi | new code ga qarshi qo'llash |
| Test kodini exclusion bilan butunlay yashirish | test sifati ko'rinmay qoladi | `sonar.tests` bilan ajratish |
| Gate natijasini kutmasdan CI ni yashil deb hisoblash | qizil gate sezilmay qoladi | `qualitygate.wait` yoqish |

## 42.16 Oddiy yondashuv va arxitektor yondashuvi

| Holat | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Coverage 0% | gate shartini olib tashlash | hisobot zanjirini qadam bo'yicha tekshirish |
| Diagnostika | log ni ko'zdan kechirish | aniq kalit so'z bilan grep qilish |
| New code bo'sh | butun loyiha shartiga o'tish | reference branch va git tarixini tuzatish |
| Sekin tahlil | tahlilni kechaga ko'chirish | exclusion bilan indeks hajmini kamaytirish |
| Xotira xatosi | heap ni ikki barobar oshirish | konteyner limiti va fayl hajmini birga sozlash |
| Issue portlashi | qoidalarni o'chirish | profile o'zgarishi sanasini aniqlash |
| PR tahlili yo'q | qo'lda branch tahliliga qaytish | PR xossalarini pipeline da shartli berish |
| Gate CI da o'qilmaydi | qadamni `continue-on-error` qilish | vazifa holatini API dan kutib o'qish |
| Takrorlanuvchi muammo | har safar qo'lda tuzatish | diagnostika skriptini repository ga qo'shish |

## 42.17 Amalda qo'llash

- [ ] Loyihada `mvn clean verify sonar:sonar -Dsonar.verbose=true` ni ishga tushirib, log ni faylga saqlang va JaCoCo sensori qatorini toping.
- [ ] `target/site/jacoco/jacoco.xml` faylida nol bo'lmagan `covered` qiymatlari borligini tasdiqlang.
- [ ] CI checkout qadamida to'liq git tarixi olinayotganini tekshirib, shallow clone ni o'chiring.
- [ ] `sonar.projectKey`, `sonar.sources`, `sonar.tests` va `sonar.java.binaries` qiymatlarini bitta konfiguratsiya faylida qotirib qo'ying.
- [ ] `sonar.qualitygate.wait` ni yoqib, qizil gate da pipeline chindan ham to'xtashini atayin buzilgan commit bilan sinab ko'ring.
- [ ] Indekslangan fayl sonini haqiqiy fayl soni bilan solishtirib, exclusion ro'yxatini qayta ko'rib chiqing.
- [ ] Server sog'ligi va Compute Engine navbati holatini tekshiradigan kichik skript yozib, uni jamoa wiki siga qo'shing.
- [ ] Shu bobdagi tekshiruv buyruqlarini `scripts/sonar-diagnose.sh` fayliga yig'ib, repository ga commit qiling.

---

[&larr; 41. Lombok, record va generatsiya qilingan kod](41-lombok-record-va-generatsiya-qilingan-kod.md) · [Mundarija](README.md) · [43. Tezkor ma'lumotnoma: parametrlar, buyruqlar, glossariy &rarr;](43-tezkor-malumotnoma-parametrlar-buyruqlar.md)
