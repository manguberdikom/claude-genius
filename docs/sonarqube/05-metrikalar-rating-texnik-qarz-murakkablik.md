<!-- doc: sonarqube | chapter: 5 | part: I. SonarQube qanday ishlaydi -->

[Barcha hujjatlar](../../README.md) / [SonarQube](README.md)

# 5. Metrikalar: rating, texnik qarz, murakkablik, takrorlanish (Metrics and Ratings)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

- [5.1 Reliability, security va maintainability reytinglari qanday hisoblanadi](#51-reliability-security-va-maintainability-reytinglari-qanday-hisoblanadi)
- [5.2 Texnik qarz (technical debt) va debt ratio: formulasi va ma'nosi](#52-texnik-qarz-technical-debt-va-debt-ratio-formulasi-va-manosi)
- [5.3 Remediation effort: har bir issue ga qo'yilgan vaqt bahosi qayerdan keladi](#53-remediation-effort-har-bir-issue-ga-qoyilgan-vaqt-bahosi-qayerdan-keladi)
- [5.4 Cyclomatic complexity va cognitive complexity farqi](#54-cyclomatic-complexity-va-cognitive-complexity-farqi)
- [5.5 Takrorlanish (duplication): blok qanday aniqlanadi va foiz qanday hisoblanadi](#55-takrorlanish-duplication-blok-qanday-aniqlanadi-va-foiz-qanday-hisoblanadi)
- [5.6 Hajm metrikalari: qatorlar, bayonotlar, funksiyalar, klasslar](#56-hajm-metrikalari-qatorlar-bayonotlar-funksiyalar-klasslar)
- [5.7 Qamrov metrikalari: line, branch va umumiy coverage](#57-qamrov-metrikalari-line-branch-va-umumiy-coverage)
- [5.8 Metrikalarning cheklovi: raqam yaxshi, kod yomon bo'lishi mumkin](#58-metrikalarning-cheklovi-raqam-yaxshi-kod-yomon-bolishi-mumkin)
- [5.9 Qaysi metrikaga ishonish mumkin, qaysi biri faqat signal](#59-qaysi-metrikaga-ishonish-mumkin-qaysi-biri-faqat-signal)
- [5.10 Metrikani vaqt bo'ylab kuzatish va trend o'qish](#510-metrikani-vaqt-boylab-kuzatish-va-trend-oqish)
- [5.11 Amalda qo'llash](#511-amalda-qollash)

</details>



Sonar hisobotidagi harf va foizlar sehrli emas. Ularning ortida juda oddiy arifmetika turadi: qoida topgan har bir issue ga daqiqa bahosi qo'yiladi, bahalar qo'shiladi, keyin kod hajmiga bo'linadi. Shu mexanikani bilgan developer reytingni ko'rib darhol tushunadi: bu yerda bitta blocker bugmi, yoki minglab mayda smell to'planganmi. Quyida har bir metrika qanday hisoblanadi, qaysi biriga qaror uchun tayanish mumkin va qaysi biri faqat tekshirishga chaqiruvchi signal ekani ko'rsatiladi.

## 5.1 Reliability, security va maintainability reytinglari qanday hisoblanadi

Uchta reyting uchta butunlay boshqa mantiq ishlatadi, va buni aralashtirish eng keng tarqalgan xato. Reliability va security reytingi eng og'ir bitta issue bo'yicha aniqlanadi: minglab mayda bug A dan C ga tushirmaydi, lekin bitta blocker bug darhol E beradi. Maintainability reytingi esa aksincha, jamlanma: u texnik qarzning kod hajmiga nisbatidan chiqadi, shuning uchun bitta smell hech narsani o'zgartirmaydi, minglab smell esa harfni pastga suradi.

Shuning uchun reliability E ni tuzatish uchun bitta joyni tuzatish kifoya qiladi, maintainability D ni tuzatish esa oylik ish bo'lishi mumkin. Security review reytingi to'rtinchi, alohida o'lchov: u security hotspot larning qanchasini odam ko'rib chiqqaniga qaraydi, ya'ni kod sifatini emas, jarayon bajarilganini o'lchaydi.

| Reyting | Reliability va security sharti | Maintainability sharti (debt ratio) | Security review sharti (ko'rilgan hotspot) |
|---|---|---|---|
| A | bironta bug yoki vulnerability yo'q | 5% va undan kam | 80% va undan ko'p |
| B | kamida bitta past ta'sirli issue bor | 6% dan 10% gacha | 70% dan 80% gacha |
| C | kamida bitta o'rta ta'sirli issue bor | 11% dan 20% gacha | 50% dan 70% gacha |
| D | kamida bitta yuqori ta'sirli issue bor | 21% dan 50% gacha | 30% dan 50% gacha |
| E | kamida bitta blocker darajali issue bor | 50% dan ko'p | 30% dan kam |

Jadvaldagi chegaralar SonarQube ning standart sozlamasi, va ularni administrator o'zgartirishi mumkin. Og'irlik atamasi versiyaga qarab farq qiladi: eski liniyada bu Blocker, Critical, Major, Minor, Info severity, 10.x dan boshlangan Clean Code taksonomiyasida esa har bir issue software quality (reliability, security, maintainability) va impact darajasi orqali tavsiflanadi. Mexanika o'zgarmadi: eng og'ir ta'sir harfni belgilaydi.

## 5.2 Texnik qarz (technical debt) va debt ratio: formulasi va ma'nosi

Texnik qarz Sonar da aniq o'lchov birligiga ega: daqiqa. Bu SQALE index deb ataladi va barcha maintainability issue larning remediation effort yig'indisiga teng. Hisobotda u "5d 4h" ko'rinishida chiqadi, lekin ichida baribir butun son daqiqa yotadi. Kun hisobiga o'tkazishda standart ish kuni 8 soat deb olinadi, shuning uchun 480 daqiqa qarz "1d" bo'lib ko'rinadi.

Debt ratio esa nisbat: qarzni shu kodni noldan yozish uchun ketadigan taxminiy vaqtga bo'ladi. Rivojlantirish narxi standart holatda har bir kod qatori uchun 30 daqiqa deb olinadi, bu `sonar.technicalDebt.developmentCost` sozlamasi bilan boshqariladi. Formula: debt ratio = remediation cost / (ncloc * cost per line). 10 000 qatorli modulda rivojlantirish narxi 300 000 daqiqa, ya'ni A reyting uchun qarz 15 000 daqiqadan oshmasligi kerak.

Bu formuladan bitta nozik xulosa chiqadi: debt ratio ni kod yozib ham yaxshilash mumkin. Agar modulga toza 5000 qator qo'shsangiz, maxraj o'sadi va foiz tushadi, qarzning o'zi esa joyida qoladi. Shuning uchun absolyut qarz daqiqasi va foiz birga o'qilishi kerak.

```properties
# sonar-project.properties: qarz hisobini loyihaga moslash
sonar.projectKey=payments-service
sonar.sources=src/main/java
sonar.tests=src/test/java
sonar.java.binaries=target/classes

# Bitta kod qatorini yozish narxi daqiqada.
# Standart 30. Pasaytirsang debt ratio oshadi, ya'ni talab qattiqlashadi.
sonar.technicalDebt.developmentCost=30

# Generatsiya qilingan kod qarzga kirmasligi uchun chiqarib tashlanadi.
sonar.exclusions=**/generated/**,**/*MapperImpl.java,**/dto/openapi/**

# Coverage hisobidan test yordamchilarini chiqarish.
sonar.coverage.exclusions=**/config/**,**/*Application.java
```

Yangi kod uchun alohida qarz o'lchovi bor, va amalda aynan shu muhim. Quality gate da ko'pincha "new code maintainability rating A dan past bo'lmasin" sharti turadi, bu esa yangi kod qarz nisbati 5% dan oshmasin degani. Eski qarz esa gate ni buzmaydi, u faqat hisobotda yashab turadi.

## 5.3 Remediation effort: har bir issue ga qo'yilgan vaqt bahosi qayerdan keladi

Vaqt bahosi kodni tahlil qilishdan emas, qoidaning ta'rifidan keladi. Har bir rule o'zining remediation funksiyasiga ega va u uch shakldan biri bo'ladi. Constant: qoida ishga tushgan har bir joy uchun bir xil vaqt, masalan 5 daqiqa. Linear: o'lchangan birlik soniga ko'paytiriladi, masalan har bir takrorlangan blok uchun 10 daqiqa. Linear with offset: boshlang'ich vaqt plus birlik bahosi, masalan 30 daqiqa plus ortiqcha har bir shoxlanish uchun 1 daqiqa.

Shuning uchun cognitive complexity 40 bo'lgan metod cognitive complexity 16 bo'lgan metoddan ko'proq qarz keltiradi, chunki offset ustiga ortiqcha birliklar qo'shiladi. Va shuning uchun bitta katta God class o'nta kichik smell dan ko'proq daqiqa bera oladi.

Bu bahalarni administrator Quality Profile da o'zgartirishi mumkin, lekin buni kamdan kam qilish kerak. Agar siz bahani pasaytirib debt ratio ni A ga chiqarsangiz, siz muammoni tuzatmadingiz, faqat o'lchov asbobini sozladingiz. To'g'ri yo'l: loyihaga mos kelmaydigan qoidani profildan butunlay o'chirish va buni yozib qo'yish, bahani qalbakilashtirmaslik.

```bash
# Qarzni qaysi fayl va qaysi qoida keltirganini aniqlash.
# facets effort bo'yicha jamlanmani qaytaradi.
curl -s -u "$SONAR_TOKEN:" \
  "$SONAR_URL/api/issues/search?componentKeys=payments-service\
&impactSoftwareQualities=MAINTAINABILITY&ps=1&facets=rules,files" \
  | jq '.facets[] | {property, values: (.values[0:5])}'

# Eng qimmat 10 ta issue: effort bo'yicha saralash.
curl -s -u "$SONAR_TOKEN:" \
  "$SONAR_URL/api/issues/search?componentKeys=payments-service\
&s=EFFORT&asc=false&ps=10" \
  | jq -r '.issues[] | "\(.effort)\t\(.rule)\t\(.component):\(.line)"'
```

Ikkinchi so'rov amalda eng foydali: u 1000 ta mayda smell o'rniga qarzning yarmini keltirgan uchta metodni ko'rsatadi. Qarz kamaytirishni shu uchtadan boshlash kerak.

## 5.4 Cyclomatic complexity va cognitive complexity farqi

Cyclomatic complexity mustaqil ijro yo'llari sonini sanaydi. Har bir shoxlanish nuqtasi bittaga oshiradi: `if`, `for`, `while`, `do`, `case`, `catch`, shuningdek `&&` va `||` qisqa tutashuv operatorlari va uchlik operator. `else` qo'shmaydi, chunki u yangi shart kiritmaydi. Bu metrika test uchun qulay: u taxminan nechta test holati kerakligini ko'rsatadi.

Cognitive complexity esa kodni odam o'qiganda qancha kuch ketishini modellashtiradi va bu `java:S3776` qoidasining asosi. Uning uchta farqi muhim. Birinchi: ichma ich joylashuv jarima oladi, ikkinchi qavat ichidagi `if` bittaga emas, uchga oshiradi. Ikkinchi: butun `switch` bloki nechta `case` borligidan qat'i nazar bittaga oshiradi, chunki o'qishga bitta qaror sifatida tushadi. Uchinchi: bir xil mantiqiy operatorlar ketma ketligi bitta deb sanaladi, ya'ni `a && b && c` bitta, `a && b || c` esa ikkita.

Natijada bir xil cyclomatic qiymatiga ega ikki metod butunlay boshqa cognitive qiymat olishi mumkin. Bu bejiz emas: tekis `switch` o'qishga oson, uch qavatli `if` esa qiyin. Standart chegara 15, u sozlanadi.

```java
// Sonar shikoyati: java:S3776, cognitive complexity 15 chegarasidan oshdi.
// Sabab: uch qavat ichma ich shart, har bir qavat jarima qo'shadi.
BigDecimal hisobla(Buyurtma b) {
    BigDecimal jami = BigDecimal.ZERO;
    if (b != null) {                                   // +1
        if (b.getQatorlar() != null) {                 // +2 (joylashuv)
            for (Qator q : b.getQatorlar()) {          // +3
                if (q.getSoni() > 0) {                 // +4
                    if (q.getChegirma() != null) {     // +5
                        jami = jami.add(q.narxChegirmali());
                    } else {                           // +1
                        jami = jami.add(q.narx());
                    }
                }
            }
        }
    }
    return jami;
}
```

```java
// Sonar o'tadigan variant: guard clause va stream bilan qavat yo'qoldi.
// Cognitive complexity 1 ga tushdi, cyclomatic ham pasaydi.
BigDecimal hisobla(Buyurtma b) {
    if (b == null || b.getQatorlar() == null) {   // +1, ketma ket || bitta sanaladi
        return BigDecimal.ZERO;
    }
    return b.getQatorlar().stream()
            .filter(q -> q.getSoni() > 0)
            .map(Qator::narxYakuniy)              // chegirma mantiqi Qator ichida
            .reduce(BigDecimal.ZERO, BigDecimal::add);
}
```

Ikkinchi variantda chegirma shartini `Qator` ga ko'chirish tasodifiy emas. Murakkablikni kamaytirishning ishonchli yo'li uni bo'lish emas, balki qarorni ma'lumot egasiga berish. Shunchaki metodni ikkiga bo'lsangiz, umumiy cognitive yig'indisi saqlanib qolishi mumkin, faqat chegaradan o'tib ketadi.

## 5.5 Takrorlanish (duplication): blok qanday aniqlanadi va foiz qanday hisoblanadi

Sonar takrorlanishni o'zining CPD (copy paste detector) mexanizmi bilan topadi va Java uchun chegara ketma ket 10 ta bayonot (statement). Ya'ni o'ntadan kam qatorli bir xil nusxa hisobga olinmaydi. Taqqoslash tokenlar darajasida ketadi, shuning uchun o'zgaruvchi nomini almashtirish takrorlanishni yashirmaydi, formatlash va izohlar esa ahamiyatsiz.

Foiz juda sodda: duplicated_lines_density = duplicated_lines / lines * 100. Diqqat qiling, maxrajda `lines`, ya'ni fayldagi barcha qatorlar, `ncloc` emas. Va takrorlangan blokning har ikki nusxasi ham duplicated_lines ga kiradi, shuning uchun 50 qatorli blokni bir joyga ko'chirish foizni 100 qatorga kamaytiradi. Standart quality gate sharti: yangi kodda takrorlanish 3% dan oshmasin.

Eng ko'p tortishuv test kodi va DTO ustida boshlanadi. Testlarda o'xshash arrange bloklari tabiiy, generatsiya qilingan DTO larda esa takrorlanish ma'nosiz. To'g'ri javob ikkisi uchun boshqa: testdagi takrorlanishni odatda builder yoki object mother bilan yo'qotish kerak (bu mavzu [testlash qo'llanmasidagi](../testing/README.md) test ma'lumotlari bo'limida ochilgan), generatsiya qilingan kodni esa tahlildan chiqarish kerak.

```properties
# Takrorlanish hisobini halol saqlash.
# Generatsiya qilingan kod CPD dan chiqariladi, chunki uni tuzatish mumkin emas.
sonar.cpd.exclusions=**/generated/**,**/*Request.java,**/*Response.java

# DIQQAT: testlarni bu yerga qo'shish vasvasa, lekin bu qarzni yashiradi.
# Testdagi takrorlanishni object mother bilan yo'qotish afzal.
# sonar.cpd.exclusions=**/test/** <- buni qilmaslik tavsiya etiladi

# Java uchun blok chegarasi tilga qattiq bog'langan: 10 bayonot.
# Uni property bilan o'zgartirib bo'lmaydi, faqat istisno qo'shish mumkin.
```

## 5.6 Hajm metrikalari: qatorlar, bayonotlar, funksiyalar, klasslar

Hajm metrikalari o'zi bo'yicha sifat haqida gapirmaydi, lekin ular boshqa hamma formulaning maxraji bo'lgani uchun muhim. `lines` fayldagi jismoniy qatorlar, bo'sh qatorlar ham kiradi. `ncloc` esa izoh va bo'sh qatorsiz kod qatorlari, va aynan u debt ratio hisobida ishlatiladi. Ikkisi orasidagi farq odatda 25 dan 40 foizga yetadi.

`statements` bayonotlar sonini sanaydi va u qatorlardan mustaqil, chunki bitta qatorga uchta bayonot sig'adi. `functions` metodlar va konstruktorlar soni, `classes` esa klass, interface, enum va record larni birga oladi. `comment_lines_density` izohlar ulushini ko'rsatadi, lekin bu metrikani maqsadga aylantirish deyarli har doim zarar: natijada har bir getter ustida ma'nosiz Javadoc paydo bo'ladi.

Amalda hajm metrikalaridan eng foydali ikkita nisbat chiqadi. Birinchi: ncloc bo'lingan functions, ya'ni o'rtacha metod uzunligi. Ikkinchi: functions bo'lingan classes, ya'ni o'rtacha klass to'ldirilganligi. Ikkinchisi keskin o'sgan paytda modulda God class o'sayotgan bo'ladi.

```bash
# Modul kesimida hajm va murakkablik nisbatlarini chiqarish.
curl -s -u "$SONAR_TOKEN:" \
  "$SONAR_URL/api/measures/component_tree?component=payments-service\
&metricKeys=ncloc,statements,functions,classes,complexity,cognitive_complexity\
&qualifiers=DIR&ps=100" \
  | jq -r '.components[] |
      [ .path,
        (.measures[] | select(.metric=="ncloc") | .value),
        (.measures[] | select(.metric=="functions") | .value),
        (.measures[] | select(.metric=="cognitive_complexity") | .value)
      ] | @tsv' \
  | awk -F'\t' '{printf "%-40s ncloc=%s fn=%s cog=%s avg_cog=%.1f\n", \
      $1,$2,$3,$4,($3>0?$4/$3:0)}' \
  | sort -t= -k5 -nr | head -15
```

## 5.7 Qamrov metrikalari: line, branch va umumiy coverage

Uchta raqam bor va ular turlicha hisoblanadi. Line coverage bajarilishi mumkin bo'lgan qatorlarning qanchasi hech bo'lmasa bir marta ishga tushganini ko'rsatadi. Branch coverage (Sonar da condition coverage) har bir shartning ham true, ham false yo'li sinalganini talab qiladi, shuning uchun u deyarli har doim pastroq chiqadi. Umumiy `coverage` metrikasi esa ikkisining qo'shilgan nisbati: qoplangan shartlar plus qoplangan qatorlar bo'lingan barcha shartlar plus barcha bajariladigan qatorlar.

Shu formuladan muhim narsa kelib chiqadi: shoxlanishlar maxrajga ikki marta kiradi, chunki har bir shart ikkita yo'l beradi. Shuning uchun murakkab metodni test qilmaslik umumiy coverage ni oddiy metodni test qilmaslikdan ko'ra qattiqroq tushiradi. Bu ham tasodifiy emas, bu metrikaga ataylab kiritilgan og'irlik.

Sonar o'zi coverage o'lchamaydi. Uni JaCoCo 0.8.x o'lchaydi va XML hisobotini beradi, Sonar esa faqat o'qiydi. Shuning uchun eng keng tarqalgan nosozlik tahlil xatosi emas, hisobot yo'lining noto'g'ri ko'rsatilishi yoki hisobot Sonar ishga tushgandan keyin yaratilishi.

```xml
<!-- JaCoCo: XML hisobot Sonar uchun majburiy, HTML faqat odam uchun -->
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <version>0.8.12</version>
  <executions>
    <execution>
      <id>prepare-agent</id>
      <goals><goal>prepare-agent</goal></goals>
    </execution>
    <execution>
      <!-- report verify dan oldin bo'lsin, aks holda Sonar bo'sh fayl ko'radi -->
      <id>report</id>
      <phase>test</phase>
      <goals><goal>report</goal></goals>
    </execution>
  </executions>
</plugin>
```

```yaml
# CI: tartib muhim. test -> jacoco report -> sonar.
# sonar ni alohida ishga tushirsang, target/ tozalanib ketmasligi kerak.
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }   # new code farqi uchun butun tarix kerak
      - uses: actions/setup-java@v4
        with: { distribution: temurin, java-version: '21' }
      - name: Test va coverage
        run: mvn -B verify
      - name: Sonar tahlili
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
        run: >
          mvn -B sonar:sonar
          -Dsonar.host.url=${{ vars.SONAR_URL }}
          -Dsonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml
      - name: Quality gate natijasini kutish
        run: mvn -B sonar:sonar -Dsonar.qualitygate.wait=true
```

## 5.8 Metrikalarning cheklovi: raqam yaxshi, kod yomon bo'lishi mumkin

Har bir metrikani aldash mumkin, va ko'pincha bu ataylab emas, bilmaslikdan sodir bo'ladi. Coverage assert siz test bilan ko'tariladi, chunki JaCoCo qator bajarildimi degan savolga javob beradi, natija to'g'rimi degan savolga emas. Cognitive complexity metodni ikkiga bo'lib pasayadi, holbuki umumiy mantiq xuddi shunday chalkash qoladi. Duplication foizi maxrajni kattalashtirib tushadi. Debt ratio yangi kod qo'shib yaxshilanadi.

| Tuzoq | Nima bo'ladi | Yechim |
|---|---|---|
| Assert siz test | coverage 90%, xato ushlanmaydi | mutation testing yoki kod review da assert talab qilish |
| Katta metodni mexanik bo'lish | S3776 yo'qoladi, chalkashlik qoladi | qarorni ma'lumot egasi klassga ko'chirish |
| `sonar.cpd.exclusions` ga testni qo'shish | duplication 0%, test bazasi chirkin | object mother va builder joriy qilish |
| Getter ustiga Javadoc | comment density o'sadi, foyda yo'q | izohni faqat sabab tushuntirishga ishlatish |
| Debt ratio ni yangi kod bilan suyultirish | foiz A, qarz daqiqasi o'sgan | absolyut `sqale_index` ni ham kuzatish |
| `@SuppressWarnings` va NOSONAR tarqalishi | issue yo'q, muammo bor | NOSONAR ni gate da sanash, sababini talab qilish |
| 100% coverage ni maqsad qilish | trivial test lavinasi | yangi kod uchun 80% chegara, murakkab joyga branch talab |
| Integration test ni coverage dan chiqarish | past foiz, haqiqiy qamrov ko'rinmaydi | hisobotlarni birlashtirib bitta XML bermoq |

Asosiy xulosa: metrika kodni emas, kodning kuzatiladigan shaklini o'lchaydi. Shakl to'g'ri bo'lib, mazmun buzuq bo'lishi mumkin. Shuning uchun Sonar kod review ni almashtirmaydi, u review qilinadigan joyni ko'rsatadi.

## 5.9 Qaysi metrikaga ishonish mumkin, qaysi biri faqat signal

Metrikalarni ikki toifaga ajratish kerak: qaror qabul qilish mumkin bo'lganlar va tekshirishga chaqiradiganlar. Birinchi toifada aniq, bir ma'noli o'lchovlar: yangi kodda bug yoki vulnerability bormi, yangi kod coverage foizi, takrorlangan yangi bloklar. Ikkinchi toifada jamlanma va baholovchi raqamlar: umumiy debt daqiqasi, maintainability harfi, umumiy coverage, comment density.

| Mavzu | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Asosiy ko'rsatkich | umumiy coverage foizini kuzatadi | new code coverage va new code bug ni kuzatadi |
| Reyting harfi | A ni maqsad qilib qo'yadi | harf ortidagi eng qimmat 10 issue ni ochadi |
| Debt | daqiqa yig'indisini hisobotda qoldiradi | qarzni modul kesimiga bo'lib egasini belgilaydi |
| Murakkablik | chegaradan o'tish uchun metodni bo'ladi | mas'uliyatni klasslar orasida qayta taqsimlaydi |
| Duplication | exclusions bilan foizni tushiradi | takrorlangan blokni umumiy abstraksiyaga chiqaradi |
| Coverage chegarasi | butun loyihaga 80% qo'yadi | murakkab paketga branch coverage shartini qo'shadi |
| NOSONAR | kerak bo'lsa yozadi, izohsiz | sababli izoh talab qiladi va sonini trend qiladi |
| Gate buzilishi | kechiktiradi, keyin ko'radi | PR ni bloklaydi va shu kuni tuzatadi |
| Metrika manbasi | UI dagi raqamga qaraydi | API dan tarix yig'ib trend o'qiydi |
| Istisno | global exclusions yozadi | istisnoni sabab bilan hujjatlashtiradi va muddat qo'yadi |

Qoida sifatida: qaror metrikalarini quality gate ga qo'ying, signal metrikalarini esa faqat kuzatuvda qoldiring. Signal metrikasini gate ga qo'yish eng tez yo'l bilan uni aldashga olib keladi, chunki jamoada shu raqamni ko'tarish rag'bati paydo bo'ladi.

## 5.10 Metrikani vaqt bo'ylab kuzatish va trend o'qish

Bitta tahlil natijasi deyarli hech narsa aytmaydi. Ma'no yo'nalishda: qarz o'sayotganmi yoki kamayayotganmi, coverage qaysi sprintdan keyin tushdi, murakkablik qaysi modulda to'planmoqda. Sonar bu uchun `api/measures/search_history` endpointini beradi, va uni haftada bir marta o'z bazangizga yozib qo'yish eng arzon kuzatuv usuli.

Trendni o'qishda uchta naqshni ajratish kerak. Birinchi: coverage ning pog'onali tushishi, bu odatda yangi modul test siz qo'shilganini bildiradi. Ikkinchi: qarzning tekis o'sishi, bu normal, agar ratio barqaror bo'lsa. Uchinchi: issue sonining keskin o'zgarishi quality profile almashganini bildiradi, kod o'zgarganini emas, va bu ikkisini aralashtirmaslik muhim.

```sql
-- O'z bazangizda saqlangan trend jadvali (API dan haftada bir yozib boriladi).
-- Maqsad: foiz va absolyut qarzni birga ko'rish.
SELECT
    o_sana,
    ncloc,
    sqale_index                                   AS qarz_daqiqa,
    ROUND(sqale_debt_ratio, 2)                    AS qarz_foiz,
    ROUND(coverage, 1)                            AS qamrov,
    sqale_index - LAG(sqale_index) OVER (ORDER BY o_sana) AS qarz_ozgarish,
    ROUND(coverage - LAG(coverage) OVER (ORDER BY o_sana), 1) AS qamrov_ozgarish
FROM sifat_trend
WHERE loyiha_kaliti = 'payments-service'
  AND o_sana >= CURRENT_DATE - INTERVAL '180 days'
ORDER BY o_sana DESC;
```

Bu so'rovda `qarz_ozgarish` musbat, `qarz_foiz` esa tushgan hafta eng xavfli holat: kod ko'p yozilgan, qarz ham o'sgan, lekin foiz suyulgani uchun hech kim sezmagan. Aynan shu holatni trend ko'rsatadi, bitta hisobot esa yashiradi.

Oxirgi maslahat: trendni odamga ko'rsatganda foizni emas, yo'nalishni ko'rsating. "Qarz uch sprintda 12 kundan 19 kunga o'sdi" gapi "maintainability C" gapidan ko'ra ko'proq qaror keltiradi, chunki unda vaqt va miqdor bor.

## 5.11 Amalda qo'llash

- [ ] Loyihangizda `sqale_index` (daqiqa) va `sqale_debt_ratio` (foiz) qiymatlarini birga chiqarib, oxirgi uch oyda ikkisi bir yo'nalishda harakat qilganini tekshiring.
- [ ] `api/issues/search` ni `s=EFFORT&asc=false` bilan chaqirib, qarzning eng qimmat 10 ta manbasini aniqlang va ularni mas'ul jamoalarga taqsimlang.
- [ ] Cognitive complexity bo'yicha chegaradan o'tgan uchta metodni tanlab, ularni bo'lish emas, mas'uliyatni ko'chirish bilan qayta yozing va oldingi hamda keyingi qiymatni yozib qo'ying.
- [ ] `sonar.cpd.exclusions` va `sonar.coverage.exclusions` ro'yxatini ochib, har bir qator uchun sababni izohda yozing, sababsizlarini olib tashlang.
- [ ] JaCoCo XML hisoboti Sonar tahlilidan oldin yaratilayotganini CI logidan tasdiqlang, `xmlReportPaths` yo'li mavjud faylga ko'rsatayotganini tekshiring.
- [ ] Quality gate ni ko'rib chiqing: unda faqat new code bo'yicha qaror metrikalari turganiga, umumiy coverage kabi signal metrikalari turmaganiga ishonch hosil qiling.
- [ ] Kod bazasida `NOSONAR` va `@SuppressWarnings("java:S...")` sonini sanab, trend jadvaliga ustun qilib qo'shing va har bir yangisiga sabab izohini talab qiling.
- [ ] Haftalik cron bilan `api/measures/search_history` natijasini o'z jadvalingizga yozib boradigan skript qo'shing, keyin 6 oylik trendni jamoaga ko'rsating.

---

[&larr; 4. Rule, quality profile va severity](04-rule-quality-profile-va-severity.md) · [Mundarija](README.md) · [6. Quality gate mexanikasi va shartlari &rarr;](06-quality-gate-mexanikasi-va-shartlari.md)
