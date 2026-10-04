<!-- doc: sonarqube | chapter: 4 | part: I. SonarQube qanday ishlaydi -->

[SonarQube](../../README.md) / [SonarQube](README.md)

# 4. Rule, quality profile va severity (Rules, Profiles and Severity)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

- [4.1 Qoida nima: tavsif, misol, tuzatish yo'li, kalit](#41-qoida-nima-tavsif-misol-tuzatish-yoli-kalit)
- [4.2 Standart profil (Sonar way) va u nimani o'z ichiga oladi](#42-standart-profil-sonar-way-va-u-nimani-oz-ichiga-oladi)
- [4.3 O'z profilingizni yaratish: nasl olish, qoida qo'shish va o'chirish](#43-oz-profilingizni-yaratish-nasl-olish-qoida-qoshish-va-ochirish)
- [4.4 Qoidani o'chirish qachon to'g'ri qaror, qachon o'zini aldash](#44-qoidani-ochirish-qachon-togri-qaror-qachon-ozini-aldash)
- [4.5 Qoida parametrlari: chegaralarni loyihaga moslash](#45-qoida-parametrlari-chegaralarni-loyihaga-moslash)
- [4.6 Profil tayinlash: til bo'yicha, loyiha bo'yicha, tashkilot bo'yicha](#46-profil-tayinlash-til-boyicha-loyiha-boyicha-tashkilot-boyicha)
- [4.7 Profil o'zgarishi va uning eski natijalarga ta'siri](#47-profil-ozgarishi-va-uning-eski-natijalarga-tasiri)
- [4.8 Tashqi vositalar qoidalari: SpotBugs, PMD, Checkstyle bilan birga ishlash](#48-tashqi-vositalar-qoidalari-spotbugs-pmd-checkstyle-bilan-birga-ishlash)
- [4.9 Qoidalar to'plamini jamoada kelishish va hujjatlashtirish](#49-qoidalar-toplamini-jamoada-kelishish-va-hujjatlashtirish)
- [4.10 Profil versiyasini kuzatish va yangi qoidalar kelganda nima qilish](#410-profil-versiyasini-kuzatish-va-yangi-qoidalar-kelganda-nima-qilish)
- [4.11 Amalda qo'llash](#411-amalda-qollash)

</details>



Sonar hech qachon "kod yomon" degan umumiy hukm chiqarmaydi. U faqat o'ziga berilgan qoidalar ro'yxatini bajaradi, va bu ro'yxat quality profile deb ataladi. Shuning uchun bitta kodni ikki xil profil bilan tekshirsangiz, natija ham ikki xil chiqadi. Bu bobda qoida nima, profil qanday boshqariladi, qoidani o'chirish qachon mantiqiy qaror va qachon o'zini aldash ekanini ko'rib chiqamiz.

## 4.1 Qoida nima: tavsif, misol, tuzatish yo'li, kalit

Qoida bu kod ustidagi bitta aniq tekshiruv. Har bir qoidaning kaliti bor va u `til:Sraqam` ko'rinishida yoziladi, masalan `java:S1192`. Kalit o'zgarmaydi, qoida nomi esa versiyadan versiyaga tahrirlanishi mumkin, shuning uchun jamoa yozishmalarida har doim kalitga tayanish kerak. Sonar UI da har bir qoidaning sahifasida uchta narsa bo'ladi: nega bu muammo, qanday kod buzadi va qanday kod to'g'ri.

Qoidalar bir necha turga bo'linadi. Bug turi ishlashda xato beradigan kodni ko'rsatadi. Vulnerability xavfsizlik teshigi. Security hotspot esa avtomatik hukm emas, inson ko'rib chiqishi kerak bo'lgan joy. Code smell ishlaydi, lekin keyinchalik qimmatga tushadigan kod. 2025 LTA liniyasida bu turlar yonida "clean code attribute" va software quality bo'yicha tasnif ham chiqadi, lekin ostidagi tekshiruv mantiqi o'sha qoidaning o'zi bo'lib qoladi.

Eng ko'p uchraydigan misol cognitive complexity. `java:S3776` metod ichidagi shart va tsikl shoxlarini sanaydi, standart chegara 15. Quyida ombor qoldig'ini tekshiruvchi metod shu chegaradan oshadi.

```java
// Sonar shikoyati: java:S3776, cognitive complexity chegaradan oshdi
public String reserve(Order order) {
    if (order != null) {
        if (order.getItems() != null) {
            for (OrderItem item : order.getItems()) {
                if (item.getQty() > 0) {
                    Stock stock = stockRepo.find(item.getSku());
                    if (stock != null) {
                        if (stock.getQty() >= item.getQty()) {
                            stock.setQty(stock.getQty() - item.getQty());
                        } else {
                            return "YETMAYDI";
                        }
                    } else {
                        return "TOPILMADI";
                    }
                }
            }
        }
    }
    return "OK";
}
```

Tuzatish yo'li chegarani ko'tarish emas, shoxlarni kamaytirish. Tekshiruvlarni alohida metodga chiqarsak, murakkablik har bir metodda chegaradan past bo'ladi va test yozish ham osonlashadi.

```java
// Sonar o'tadigan variant: har bir metodda bitta mas'uliyat
public ReservationResult reserve(Order order) {
    for (OrderItem item : order.items()) {
        ReservationResult result = reserveOne(item);
        if (result.failed()) {
            return result; // birinchi xatoda to'xtaymiz
        }
    }
    return ReservationResult.ok();
}

private ReservationResult reserveOne(OrderItem item) {
    Stock stock = stockRepo.findBySku(item.sku())
            .orElseThrow(() -> new SkuNotFoundException(item.sku()));
    if (stock.qty() < item.qty()) {
        return ReservationResult.insufficient(item.sku());
    }
    stock.decrease(item.qty());
    return ReservationResult.ok();
}
```

Qoidalar faqat Java uchun emas. SQL, XML, YAML va Dockerfile uchun ham o'z qoida to'plami bor. Masalan hisobot so'rovida ustunlarni aniq sanab chiqish qoidasi migratsiyadan keyin kutilmagan natijadan saqlaydi.

```sql
-- Sonar shikoyati: ustunlar aniq sanalmagan, jadval o'zgarsa kod buziladi
SELECT * FROM payments WHERE status = 'PENDING';

-- Sonar o'tadigan variant: aniq ustunlar va aniq tartib
SELECT p.id, p.order_id, p.amount, p.currency, p.created_at
FROM payments p
WHERE p.status = 'PENDING'
ORDER BY p.created_at;
```

## 4.2 Standart profil (Sonar way) va u nimani o'z ichiga oladi

Har bir til uchun Sonar o'zining "Sonar way" profilini beradi va yangi loyiha avtomatik shu profilga ulanadi. Bu profil ichidagi qoidalar tanlangan mezon bilan tanlangan: false positive ehtimoli past, muammosi tushunarli, tuzatish yo'li aniq. Java uchun Sonar way da minglab mavjud qoidadan taxminan yarmidan kamrog'i yoqilgan bo'ladi, aniq son versiyaga qarab farq qiladi.

Sonar way ichida nima bor va nima yo'q ekanini tushunish muhim. Ichida: null dereference, resurs yopilmaganligi, bo'sh catch bloki, takrorlangan string literal, dead code, murakkablik chegaralari, keng tarqalgan xavfsizlik naqshlari. Ichida yo'q: ko'p stilistik talablar, qattiq nomlash konvensiyalari, kontekstga juda bog'liq arxitektura qoidalari. Stil masalasini Sonar emas, formatter hal qilishi kerak.

Yana bir "Sonar way Recommended" nomli variant ham uchraydi, unda qo'shimcha qoidalar bor. Ikkala standart profil ham read-only, ya'ni ularni tahrirlay olmaysiz. O'zgartirish uchun nasl olish kerak.

## 4.3 O'z profilingizni yaratish: nasl olish, qoida qo'shish va o'chirish

Jarayon oddiy: Quality Profiles sahifasida Sonar way ni tanlaysiz, Copy yoki Extend qilasiz, keyin o'z profilingizda qoidalarni sozlaysiz. Copy va Extend o'rtasidagi farq muhim. Copy nusxa oladi va keyin ota profil yangilansa, sizga hech narsa o'tmaydi. Extend esa nasl bog'lanishini saqlaydi: ota profilga yangi qoida qo'shilsa, u sizning profilingizda ham paydo bo'ladi.

Amalda tavsiya: Extend tanlang. Shunda Sonar jamoasi yangi foydali qoida qo'shganda siz uni bepul olasiz, o'zingizning farqlaringiz esa alohida qatlamda qoladi. Nasl olingan profilda ota qoidasini o'chira olmaysiz, faqat o'zingiz qo'shganini boshqarasiz. Agar otaning bitta qoidasi sizga umuman mos kelmasa, o'sha holatda Copy yoki qoida darajasida boshqa yechim kerak bo'ladi.

Profilni qo'lda sozlashning xavfi shuki, u serverda yashaydi va git da izi qolmaydi. Shuning uchun profilni backup qilib repoda saqlash kerak. Web API buni oson qiladi.

```bash
# Profilni XML ga eksport qilish va repoda saqlash
SONAR_URL="https://sonar.example.com"
curl -sS -u "$SONAR_TOKEN:" \
  "$SONAR_URL/api/qualityprofiles/backup?language=java&qualityProfile=Payments%20Java" \
  -o quality/payments-java-profile.xml

# Yoqilgan qoidalar sonini tekshirish (git diff da ko'rinadi)
grep -c "<rule>" quality/payments-java-profile.xml

# Boshqa muhitga tiklash
curl -sS -u "$SONAR_TOKEN:" -X POST \
  -F "backup=@quality/payments-java-profile.xml" \
  "$SONAR_URL/api/qualityprofiles/restore"
```

Bu bitta harakat profilni "serverdagi sirli sozlama" dan "code review dan o'tadigan fayl" ga aylantiradi. Profilni kim, qachon va nega o'zgartirganini pull request tarixidan ko'rasiz.

## 4.4 Qoidani o'chirish qachon to'g'ri qaror, qachon o'zini aldash

Bu bobning eng muhim qismi. Qoidani o'chirish o'zi yomon emas, lekin sabab muhim. To'g'ri sabab: qoida sizning texnologiyangizda haqiqatan ham noto'g'ri ishlaydi. Noto'g'ri sabab: qoida ko'p issue chiqardi va biz tuzatishni xohlamaymiz.

| Holat | Qoidani o'chirish o'rinli | Qoidani o'chirish o'rinsiz |
| --- | --- | --- |
| Qoida framework naqshini tushunmaydi | Lombok yoki MapStruct generatsiyasi noto'g'ri belgilansa | Lombok ishlatmasdan shunchaki getter yozishni xohlamasangiz |
| Issue soni juda ko'p | Qoida butun loyihada 100% false positive bo'lsa | Qoida haqiqiy qarzni ko'rsatsa, raqam esa noqulay bo'lsa |
| Test kodi | Test uchun mos kelmaydigan qoidani faqat test papkasida o'chirish | Testlardagi assertion yo'qligini aytuvchi qoidani o'chirish |
| Chegara qoidalari | Generatsiya qilingan kod uchun chegarani istisno qilish | Metod murakkabligini 15 dan 60 ga ko'tarish |
| Xavfsizlik | Boshqa qatlamda himoya borligi hujjatlashtirilgan bo'lsa | "Bizning ichki tizim, hujum bo'lmaydi" deganda |
| Deprecated API | Migratsiya rejasi va muddati yozilgan bo'lsa | Migratsiya hech qachon boshlanmasa |
| Legacy modul | Modul o'chirilish rejasida va faqat o'sha modulda | Butun monolitda global o'chirish |
| Quality gate qizil | Hech qachon: gate shartini ko'rib chiqish kerak | Gate o'tishi uchun qoidani o'chirish |

Uchinchi yo'l ham bor va u ko'pincha eng to'g'risi: qoidani o'chirmasdan, aniq bitta joyda istisno qilish. Java da bu `@SuppressWarnings` izohi, va unda sabab yozilishi shart.

```java
@Service
public class LegacyPaymentGateway {

    // Qoida global o'chirilmadi, faqat shu metodda istisno qilindi.
    // Sabab: tashqi SOAP client o'zini yopadi, biz yopsak session uziladi.
    // Jira: PAY-4412, 2026 Q1 da yangi REST client ga o'tamiz.
    @SuppressWarnings("java:S2095")
    public PaymentStatus charge(ChargeCommand command) {
        GatewaySession session = vendorClient.openSession();
        return session.charge(command.amount(), command.currency());
    }
}
```

Bu yondashuvning afzalligi: istisno kodning yonida turadi, sababi o'qiladi, va grep bilan hamma istisnoni bir ko'rishda sanab chiqasiz. Serverda "Won't fix" bosish esa koddan ko'rinmaydi va yangi developer hech narsa bilmaydi.

## 4.5 Qoida parametrlari: chegaralarni loyihaga moslash

Ko'p qoidaning parametri bor va bu o'chirishdan ancha yumshoq vosita. `java:S3776` da murakkablik chegarasi, `java:S1192` da bir xil string necha marta takrorlanishi, metod parametrlari sonini cheklovchi qoidada maksimal son. Parametr nomlari versiyaga qarab farq qiladi, shuning uchun aniq nomni UI dan yoki eksport qilingan XML dan oling.

Parametrni o'zgartirishda bitta qoida bor: chegarani kod darajasiga emas, jamoa kelishgan maqsadga qarab qo'ying. Agar kodda murakkablik 40 bo'lsa va siz chegarani 40 qilsangiz, qoida o'lgan bo'ladi. To'g'ri yo'l: chegarani 15 da qoldirib, yangi kodga qo'llash, eski kodni asta tuzatish. Sonar ning "new code" mantiqi aynan shu uchun bor.

```xml
<!-- quality/payments-java-profile.xml, parametr bilan qoida -->
<profile>
  <name>Payments Java</name>
  <language>java</language>
  <rules>
    <rule>
      <repositoryKey>java</repositoryKey>
      <key>S3776</key>
      <priority>CRITICAL</priority>
      <parameters>
        <!-- standart 15, biz 12 ga tushirdik: domen kodi sodda bo'lishi kerak -->
        <parameter>
          <key>Threshold</key>
          <value>12</value>
        </parameter>
      </parameters>
    </rule>
  </rules>
</profile>
```

Severity ham xuddi parametr kabi profil ichida o'zgaradi. Bu muhim, chunki quality gate sharti ko'pincha severity ga bog'lanadi. Agar gate "Blocker va Critical issue bo'lmasin" desa, siz bitta qoidaning severity sini Major dan Critical ga ko'tarib, uni amalda majburiy qilib qo'yasiz. Teskari harakat ham ishlaydi va aynan shu joyda o'zini aldash boshlanadi: severity ni Info ga tushirish qoidani o'chirishning yashirin shakli.

| Tuzoq | Nima bo'ladi | Yechim |
| --- | --- | --- |
| Chegarani kodga moslash | Qoida hech qachon ishga tushmaydi | Chegarani qoldirib, new code shartini ishlatish |
| Severity ni Info ga tushirish | Gate o'tadi, muammo qoladi | Severity ni saqlab, issue ni rejaga kiritish |
| Profilni faqat UI da sozlash | O'zgarish tarixi yo'q, audit yo'q | Profilni XML backup bilan repoda saqlash |
| Copy bilan nasl uzish | Yangi qoidalar hech qachon kelmaydi | Extend ishlatish |
| Global `@SuppressWarnings` | Butun sinf nazoratdan chiqadi | Istisno aniq metodda va sabab bilan |
| Tashqi report ulanmagan | SpotBugs natijasi Sonar da ko'rinmaydi | Report yo'lini `sonar.java.*ReportPaths` ga berish |
| Har modulda boshqa profil | Natijalarni solishtirib bo'lmaydi | Tashkilot darajasida bitta asos profil |
| Test papkasi ajratilmagan | Test kodi domen qoidalari bilan tekshiriladi | `sonar.tests` ni aniq ko'rsatish |

## 4.6 Profil tayinlash: til bo'yicha, loyiha bo'yicha, tashkilot bo'yicha

Profil har doim bitta tilga tegishli. Ya'ni bitta loyihada Java, XML va YAML uchun uchta alohida profil faol bo'ladi. Shuning uchun "loyihaning profili" degan narsa yo'q, "loyihaning har bir til uchun profili" bor.

Tayinlashning uch darajasi mavjud. Birinchisi default: har bir til uchun bitta profil default deb belgilanadi va yangi loyihalar shuni oladi. Ikkinchisi loyiha darajasi: aniq bitta loyihaga boshqa profil biriktirasiz. Uchinchisi tashkilot amaliyoti: default ni o'z korporativ profilingizga almashtirasiz va shundan keyin barcha yangi loyihalar avtomatik to'g'ri profilni oladi.

Amalda eng barqaror sxema ikki qatlamli: tashkilot bo'ylab bitta "Company Java" profili Sonar way dan nasl oladi, va faqat juda alohida loyihalar undan nasl olgan o'z profilini qiladi. Uchdan ko'p qatlam qilsangiz, qaysi qoida qaysi profildan kelganini hech kim tushunmay qoladi.

Diqqat qiling: profilni skaner tomonidan, ya'ni `sonar-project.properties` ichidan tanlay olmaysiz. Bu ataylab shunday, chunki aks holda har bir developer o'z mashinasida qoidalarni yumshatib yuborishi mumkin edi. Profil faqat serverda, ruxsati bor odam tomonidan tayinlanadi.

## 4.7 Profil o'zgarishi va uning eski natijalarga ta'siri

Bu joy ko'p chalkashlik keltiradi, shuning uchun aniq aytamiz. Profilni o'zgartirganingizda Sonar eski analiz natijalarini qayta hisoblamaydi. Yangi qoida faqat keyingi analizdan boshlab issue chiqaradi. Shuning uchun profil o'zgargandan keyin darhol bitta analiz ishga tushirmaguningizcha, dashboard eski manzarani ko'rsatib turadi.

Ikkinchi nozik nuqta: yangi qoida yoqilsa, u eski kodda ham issue topadi. Agar quality gate sharti faqat new code ga qarasa, bu issue lar gate ni buzmaydi va ro'yxatda texnik qarz sifatida turadi. Agar gate overall code ga qarasa, bitta profil o'zgarishi ertasi kuni butun pipeline ni qizartirib qo'yishi mumkin. Shuning uchun profilga yangi qoida qo'shishni relizdan oldingi kunga qo'ymang.

Uchinchisi: qoidani o'chirsangiz, undan kelgan issue lar yopiladi va "closed" holatga o'tadi. Keyin o'sha qoidani qaytarsangiz, issue lar yangi deb hisoblanishi mumkin, ya'ni ularning "created" sanasi o'zgarib, new code oynasiga tushib qolishi mumkin. Buni tekshirmasdan katta profil o'zgarishini relizga olib bormang.

Xavfsiz tartib: profilni staging Sonar serverida yoki alohida loyiha kaliti bilan sinab ko'rish, natijadagi issue sonini solishtirish, keyin asosiy serverga restore qilish.

```properties
# sonar-project.properties: profil o'zgarishini sinash uchun vaqtincha loyiha kaliti
sonar.projectKey=payments-service-profile-trial
sonar.projectName=Payments Service (profil sinovi)
sonar.sources=src/main/java
sonar.tests=src/test/java
sonar.java.binaries=target/classes
# Sinov loyihasi gate ni buzmasligi uchun alohida gate biriktirilgan
sonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml
# Generatsiya qilingan kodni tahlildan chiqaramiz
sonar.exclusions=**/generated/**,**/*MapperImpl.java
```

## 4.8 Tashqi vositalar qoidalari: SpotBugs, PMD, Checkstyle bilan birga ishlash

Sonar o'zining Java analizatoriga ega va u ko'p narsani qoplaydi. Shunga qaramay SpotBugs ba'zi bytecode darajasidagi muammolarni yaxshi topadi, Checkstyle esa stilistik talablarni qattiq ushlaydi. Ikki yo'l bor: bu vositalarning natijasini Sonar ga import qilish, yoki ularni mustaqil ravishda build da ishlatish.

Import qilsangiz, natija Sonar da issue sifatida ko'rinadi va quality gate ga ta'sir qiladi. Buning uchun report fayl yo'lini skanerga berish kerak.

```xml
<build>
  <plugins>
    <plugin>
      <groupId>com.github.spotbugs</groupId>
      <artifactId>spotbugs-maven-plugin</artifactId>
      <configuration>
        <!-- Sonar o'qiy oladigan XML report -->
        <xmlOutput>true</xmlOutput>
        <xmlOutputDirectory>${project.build.directory}/spotbugs</xmlOutputDirectory>
        <!-- build ni to'xtatmaydi, hukm Sonar gate da chiqadi -->
        <failOnError>false</failOnError>
      </configuration>
      <executions>
        <execution>
          <phase>verify</phase>
          <goals><goal>spotbugs</goal></goals>
        </execution>
      </executions>
    </plugin>
  </plugins>
</build>
```

Report yo'llari `sonar.java.spotbugs.reportPaths`, `sonar.java.pmd.reportPaths` va `sonar.java.checkstyle.reportPaths` kabi parametrlar bilan beriladi. Aniq nom SonarQube versiyasiga qarab farq qiladi, shuning uchun o'z versiyangizning hujjatidan tasdiqlang. Import qilingan qoidalar alohida repository ga tushadi va ularning kaliti `squid` yoki `java` emas, o'sha vositaning kaliti bo'ladi.

Eng katta xato ikki vositani bir xil narsa uchun yonma yon ishlatish. Agar SpotBugs ham, Sonar ham null dereference ni topsa, bitta muammo ikki marta sanaladi va metrikalar buziladi. To'g'ri taqsimot: Sonar asosiy analizator, SpotBugs faqat Sonar da yo'q bo'lgan tekshiruvlar uchun, Checkstyle faqat formatlash uchun va u Sonar ga import qilinmaydi.

```yaml
# .github/workflows/quality.yml, tartib muhim: verify keyin sonar
- name: Build va static analiz
  run: mvn -B clean verify   # jacoco va spotbugs report shu yerda yaratiladi

- name: Sonar analiz
  env:
    SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
  run: >
    mvn -B sonar:sonar
    -Dsonar.projectKey=payments-service
    -Dsonar.qualitygate.wait=true

- name: Profil backup o'zgarmaganini tekshirish
  run: |
    curl -sS -u "$SONAR_TOKEN:" \
      "$SONAR_HOST/api/qualityprofiles/backup?language=java&qualityProfile=Company%20Java" \
      -o /tmp/live.xml
    diff -q quality/company-java-profile.xml /tmp/live.xml \
      || echo "OGOHLANTIRISH: serverdagi profil repodagidan farq qiladi"
```

## 4.9 Qoidalar to'plamini jamoada kelishish va hujjatlashtirish

Profil texnik fayl emas, u jamoa kelishuvi. Shuning uchun uni bitta odam bir kechada o'zgartirmasligi kerak. Ishlaydigan tartib quyidagicha: har bir o'chirilgan yoki qo'shilgan qoida uchun repoda bitta qator yoziladi, unda qoida kaliti, qaror, sabab va qarorni qabul qilgan odam bo'ladi.

Bu ro'yxatni `quality/rules-decisions.md` kabi faylda saqlash kifoya. Yangi developer kelganda u "nega bu qoida o'chirilgan" savoliga javobni bir joydan topadi. Audit paytida ham xuddi shu fayl ishlaydi.

Sabab yozishda aniq bo'ling. "Bizga mos emas" sabab emas. "MapStruct generatsiya qilgan `*MapperImpl` sinflarida bu qoida 100% false positive, generatsiya shabloni o'zgarmaguncha o'chirib qo'yildi" sabab. Ikkinchi yozuvni olti oydan keyin ham qayta ko'rib chiqa olasiz.

Qoida qo'shishni ham xuddi shu tartibda qiling. Yangi qoida yoqishdan oldin uning hozirgi kodda qancha issue topishini bilib oling. Agar 400 ta chiqsa, qoidani darhol Blocker qilib qo'yish o'rniga, uni yoqib, gate ni faqat new code ga bog'lab qo'ying. Shunda yangi kod toza bo'ladi, eski kod esa reja bilan tozalanadi. Quality gate va new code mexanikasi haqida shu hujjatning quality gate bobida batafsil yozilgan.

## 4.10 Profil versiyasini kuzatish va yangi qoidalar kelganda nima qilish

SonarQube yangilanganda analizator pluginlari ham yangilanadi va Sonar way ga yangi qoidalar qo'shiladi. Agar siz Extend qilgan bo'lsangiz, bu qoidalar sizga avtomatik keladi. Bu yaxshi, lekin kutilmagan bo'lsa yoqimsiz: ertalab pipeline qizil bo'lib turadi.

Shuning uchun yangilanishni jarayon sifatida rasmiylashtirish kerak. Avval staging serverda yangilang. Keyin bir necha vakil loyihani qayta analiz qiling va yangi issue larni ko'rib chiqing. Yangi qoidalardan qaysi biri haqiqiy muammo topganini va qaysi biri shovqin ekanini belgilang. Shovqin bo'lganini o'z profilingizda o'chirib, sababini hujjatga yozing. Shundan keyin prod serverni yangilang.

| Mavzu | Oddiy yondashuv | Arxitektor yondashuvi |
| --- | --- | --- |
| Profil tanlash | Sonar way ni o'zi yetadi | Sonar way dan Extend qilib korporativ asos profil yaratiladi |
| Profilni saqlash | Serverda UI orqali sozlanadi | XML backup repoda, o'zgarish pull request orqali |
| Qoida yoqmasa | Qoida o'chiriladi | Avval false positive tekshiriladi, keyin parametr, oxirida o'chirish |
| Istisno berish | Serverda "Won't fix" bosiladi | Kodda `@SuppressWarnings` va sabab izohi |
| Chegaralar | Kodga moslab ko'tariladi | Standart saqlanadi, new code shartiga tayaniladi |
| Severity | Gate o'tishi uchun tushiriladi | Severity haqiqiy ta'sirni aks ettiradi |
| Tashqi vositalar | SpotBugs va Sonar ikkisi ham hammasini tekshiradi | Mas'uliyat taqsimlangan, takrorlanish yo'q |
| Yangilanish | Prod da to'g'ridan to'g'ri yangilanadi | Staging da sinaladi, yangi qoidalar baholanadi |
| Qarorlar tarixi | Odamlar xotirasida | `rules-decisions.md` faylida kalit, sabab va muallif bilan |
| Profil soni | Har jamoa o'zini qiladi | Ikki qatlam: tashkilot asosi va zarur istisnolar |

Oxirgi maslahat: profilni kichik tuting. 600 ta yoqilgan qoida 200 tasidan yaxshi degani emas. Jamoa tushunadigan, sababi hujjatlashtirilgan va haqiqatan ham tuzatiladigan qoidalar to'plami eng foydali profil bo'ladi.

## 4.11 Amalda qo'llash

- [ ] Hozirgi loyihangizda har bir til uchun qaysi profil faol ekanini Sonar UI dan aniqlang va ro'yxat tuzing.
- [ ] Sonar way dan Extend qilib bitta korporativ `Company Java` profilini yarating, Copy ishlatmang.
- [ ] `api/qualityprofiles/backup` orqali profil XML ini eksport qilib, uni `quality/` papkasida git ga qo'shing.
- [ ] `quality/rules-decisions.md` fayl yaratib, har bir o'chirilgan qoida uchun kalit, sabab, muallif va qayta ko'rish sanasini yozing.
- [ ] Serverdagi "Won't fix" va "False positive" belgilarini ko'rib chiqing, mos keladiganlarini koddagi `@SuppressWarnings` va izohga o'tkazing.
- [ ] `java:S3776` chegarasini loyihangizda sinab ko'ring: standart 15 da qoldirib, yangi kodda qancha issue chiqishini o'lchang.
- [ ] CI ga serverdagi profil repodagi XML dan farq qilsa ogohlantirish beradigan qadam qo'shing.
- [ ] Keyingi SonarQube yangilanishini avval staging da bajarib, yangi qoidalardan kelgan issue larni jamoa bilan bir o'tirishda baholang.

---

[&larr; 3. Issue turlari: bug, vulnerability, code smell, security hotspot](03-issue-turlari-bug-vulnerability-code-smell.md) · [Mundarija](README.md) · [5. Metrikalar: rating, texnik qarz, murakkablik, takrorlanish &rarr;](05-metrikalar-rating-texnik-qarz-murakkablik.md)
