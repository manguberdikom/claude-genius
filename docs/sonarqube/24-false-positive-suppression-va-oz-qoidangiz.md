<!-- doc: sonarqube | chapter: 24 | part: VI. Amaliyot va jarayon -->

[SonarQube](../../README.md) / [SonarQube](README.md)

# 24. False positive, suppression va o'z qoidangiz (False Positives and Custom Rules)

<details>
<summary>Bu bobdagi 12 bo'lim</summary>

- [24.1 False positive nima va u qanchalik tez-tez uchraydi](#241-false-positive-nima-va-u-qanchalik-tez-tez-uchraydi)
- [24.2 Issue ni "false positive" yoki "won't fix" deb belgilash va farqi](#242-issue-ni-false-positive-yoki-wont-fix-deb-belgilash-va-farqi)
- [24.3 Belgilashni asoslash: izoh yozish majburiyati](#243-belgilashni-asoslash-izoh-yozish-majburiyati)
- [24.4 Kod ichida bostirish: `@SuppressWarnings` va uning ta'sir doirasi](#244-kod-ichida-bostirish-suppresswarnings-va-uning-tasir-doirasi)
- [24.5 Bostirishni ko'rib chiqish: ular to'planib qolmasligi uchun tartib](#245-bostirishni-korib-chiqish-ular-toplanib-qolmasligi-uchun-tartib)
- [24.6 Qoidani butunlay o'chirish qachon to'g'ri qaror](#246-qoidani-butunlay-ochirish-qachon-togri-qaror)
- [24.7 O'z qoidangizni yozish: qachon zarur bo'ladi](#247-oz-qoidangizni-yozish-qachon-zarur-boladi)
- [24.8 Qoida yozishning muqobillari: ArchUnit, linter, code review qoidasi](#248-qoida-yozishning-muqobillari-archunit-linter-code-review-qoidasi)
- [24.9 Jamoaviy kelishuv: kim belgilaydi, kim tasdiqlaydi](#249-jamoaviy-kelishuv-kim-belgilaydi-kim-tasdiqlaydi)
- [24.10 Suppression statistikasini kuzatish va ularni kamaytirish](#2410-suppression-statistikasini-kuzatish-va-ularni-kamaytirish)
- [24.11 Sonar charchog'i: belgilar ko'payib ketganda nima qilish](#2411-sonar-charchogi-belgilar-kopayib-ketganda-nima-qilish)
- [24.12 Amalda qo'llash](#2412-amalda-qollash)

</details>


Har bir jamoada bir kun shu savol tug'ilad: "Sonar xato qilyapti, buni qanday o'chiramiz?". Javob oson emas, chunki bostirishning to'rt xil yo'li bor va ularning har biri boshqa odamga boshqa narsani ko'rsatadi. Bu bobda haqiqiy false positive ni shunchaki noqulay qoidadan ajratishni, bostirishni qayerda va qanday qayd etishni, va qachon qoidani butunlay o'chirish eng halol qaror bo'lishini ko'rib chiqamiz. Oxirida bostirishlar sonini metrika sifatida kuzatish tartibi bor, chunki kuzatilmagan suppression bir yilda minglab bo'lib ketadi.

## 24.1 False positive nima va u qanchalik tez-tez uchraydi

False positive deganda qoida ishga tushdi, lekin kodda haqiqiy muammo yo'q holat tushuniladi. Uni uchta boshqa holatdan ajratish kerak. Birinchisi, qoida haq, lekin jamoa uni yoqtirmaydi. Ikkinchisi, qoida haq, lekin bu yerda tuzatish narxi foydadan katta. Uchinchisi, analizator kontekstni ko'rmagani uchun xato qilgan. Faqat uchinchisi false positive.

Tajribada eng ko'p sabab analizatorning klasspathni to'liq ko'rmasligi. Agar `sonar.java.binaries` yoki kutubxonalar ro'yxati to'liq bo'lmasa, analizator tiplarni yecha olmaydi va nullability haqidagi xulosalari buziladi. Shu sababdan paydo bo'lgan shovqinni bostirish eng katta xato, chunki konfiguratsiyani tuzatsa o'zi yo'qoladi.

Ikkinchi sabab framework semantikasi. Spring konteyner maydonga qiymat quyadi, Lombok konstruktor generatsiya qiladi, MapStruct implementatsiya yozadi, JPA proxy yaratadi. Analizator buni har doim bilmaydi. Uchinchi sabab reflection va dinamik chaqiruvlar.

Aniq raqam bermayman, chunki u profilga va loyihaga qarab o'zgaradi. Ishonchli qoida shu: agar jamoada issue larning o'ndan biridan ko'pi false positive deb belgilansa, muammo Sonar da emas, sozlamada yoki profil tanlashda.

```java
// Sonar shikoyat qiladi: "possible null dereference" (java:S2259 turkumi)
// Sabab: @Autowired maydon konstruktorda to'ldirilmagan deb ko'rinadi
@Service
public class TolovService {
    @Autowired
    private TolovRepository repository; // analizator uchun null bo'lishi mumkin

    public BigDecimal jami(Long buyurtmaId) {
        return repository.summaByBuyurtma(buyurtmaId); // ogohlantirish shu qatorda
    }
}

// Sonar o'tadigan variant: bostirish emas, dizaynni tuzatish
@Service
public class TolovServiceFixed {
    private final TolovRepository repository; // final, konstruktorda majburiy

    public TolovServiceFixed(TolovRepository repository) {
        this.repository = Objects.requireNonNull(repository);
    }

    public BigDecimal jami(Long buyurtmaId) {
        return repository.summaByBuyurtma(buyurtmaId);
    }
}
```

Bu misol muhim xulosani beradi. Ko'p "false positive" aslida kodning noaniqligi haqidagi signal. Konstruktor inyeksiyasiga o'tish ogohlantirishni ham, test yozishdagi qiyinchilikni ham bir vaqtda yo'q qiladi.

## 24.2 Issue ni "false positive" yoki "won't fix" deb belgilash va farqi

Serverda issue ni yopishning ikki ma'nosi bor va ular aralashtirilmasligi kerak. "False positive" degani: qoida xato ishladi, bu kodda muammo yo'q. "Won't fix" degani (yangi versiyalarda u "Accepted" deb nomlanadi): muammo bor, biz uni ongli ravishda qoldiramiz.

Status modeli versiyaga qarab farq qiladi. 9.9 LTA liniyasida issue "Resolved" holatiga o'tadi va sababi "False Positive" yoki "Won't Fix" bo'ladi. Keyingi liniyalarda, 2025 LTA ni ham qo'shib, "Accepted" alohida status sifatida ko'rinadi. Ikkala holatda ham natija bir xil: issue quality gate ning "new issues" shartiga ta'sir qilmay qoladi.

Farq hisobot uchun emas, qaror uchun muhim. False positive to'planib qolsa, demak profil yoki analiz sozlamasi noto'g'ri va uni tuzatish kerak. Accepted to'planib qolsa, demak jamoa texnik qarzni ongli to'playapti va uni reja bilan kamaytirish kerak. Bir xil belgi ostida ikkisini qo'shib yuborsangiz, hech qaysi muammoni ko'rmaysiz.

| Holat | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Qoida noqulay ko'rinsa | darhol false positive deb belgilanadi | avval qoida tavsifi va misoli o'qiladi, keyin qaror |
| Belgilash huquqi | hammada bor, hech kim kuzatmaydi | "Administer Issues" huquqi cheklangan guruhda |
| Izoh | bo'sh yoki "not relevant" | sabab, muqobil himoya va havola yozilgan |
| Bostirish joyi | tasodifiy: ba'zan UI, ba'zan NOSONAR | qaror daraxti bilan qat'iy belgilangan |
| Bir xil holat ko'p faylda | har safar qaytadan bostiriladi | profilda qoida parametri yoki exclusion bilan yechiladi |
| Klasspath muammosi | issue bostiriladi | `sonar.java.binaries` tuzatiladi, bostirish olib tashlanadi |
| Suppression soni | o'lchanmaydi | metrika sifatida kuzatiladi va chorakda ko'rib chiqiladi |
| Qoidani o'chirish | yashirincha, shaxsiy profilda | yozma asos bilan, umumiy profilda, sababi qayd etilgan |
| Yangi a'zo kelganda | bostirishlar sababini hech kim bilmaydi | har bir bostirishda izoh va muallif bor |
| Qarz holati | gate yashil, lekin kod yomonlashgan | accepted issue soni alohida grafikda ko'rinadi |

## 24.3 Belgilashni asoslash: izoh yozish majburiyati

Izohsiz bostirish eng zararli artefakt, chunki uni keyin hech kim tekshira olmaydi. Oradan bir yil o'tgandan keyin faqat "bu issue yopilgan" degani qoladi, "nega" degani yo'qoladi. Shuning uchun jamoa qoidasi oddiy bo'lishi kerak: izohsiz belgilash code review da rad etiladi.

Yaxshi izohning to'rt elementi bor. Birinchisi, qoida nimani nazarda tutgani va nega bu yerda u ishlamasligi. Ikkinchisi, muammoni boshqa qanday himoya qoplayotgani, masalan test, validatsiya yoki arxitektura cheklovi. Uchinchisi, havola: ticket raqami, ADR yoki pull request. To'rtinchisi, qayta ko'rib chiqish sharti, ya'ni qaysi o'zgarishdan keyin bu bostirish bekor bo'ladi.

```java
// Noto'g'ri izoh: "false positive" (hech narsa tushuntirmaydi)
// To'g'ri izoh namunasi (UI dagi comment maydoniga ham shu matn yoziladi):
//
// FP: qoida bu yerda callerning validatsiyasini ko'rmaydi.
// buyurtmaId OrderController da @Positive bilan tekshiriladi va
// TolovServiceTest#jami_manfiyIdBilan testi shu shartni qo'riqlaydi.
// Havola: PAY-1842. Agar controller validatsiyasi olib tashlansa,
// bu bostirish bekor bo'ladi va qayta ko'rib chiqilishi shart.
@SuppressWarnings("java:S3776") // cognitive complexity: legacy hisobot formulasi
public HisobotQatori qurish(TolovYozuvi yozuv) {
    // PAY-1842 doirasida bo'linadi, hozir formula to'liq ko'rinishda qolishi kerak
    return legacyFormula.apply(yozuv);
}
```

Izohni kod ichida ham, serverda ham bir xil yozish foydali. Serverdagi izoh audit uchun, koddagi izoh keyingi o'quvchi uchun. Ikkisi bir-biriga mos bo'lsa, bostirishni qayta ko'rib chiqish bir daqiqalik ish bo'ladi.

## 24.4 Kod ichida bostirish: `@SuppressWarnings` va uning ta'sir doirasi

Java da Sonar issue ini kod ichida bostirishning asosiy vositasi `@SuppressWarnings` annotatsiyasi va qoida kaliti. Kalit yangi formatda `java:S3776` ko'rinishida yoziladi, eski loyihalarda `squid:S3776` shakli ham uchraydi. Annotatsiyaning retention darajasi SOURCE, demak u bytecode ga tushmaydi va runtime da hech qanday narxi yo'q.

Ta'sir doirasi annotatsiya qo'yilgan element bilan cheklanadi. Klassga qo'yilsa, butun klass ichidagi mos issue lar bostiriladi. Metodga qo'yilsa, faqat shu metod. Lokal o'zgaruvchiga yoki parametrga qo'yilsa, eng tor doira. Qoida oddiy: doira imkon qadar tor bo'lsin, chunki keng doira kelgusida paydo bo'ladigan haqiqiy muammoni ham yashiradi.

```java
// YOMON: butun klassga qo'yilgan, kelgusi haqiqiy muammo ham yashiriladi
@SuppressWarnings({"java:S3776", "java:S1192", "java:S112"})
public class OmborXizmati { /* 600 qator */ }

// YAXSHI: bitta metod, bitta qoida, sabab izohi bilan
public class OmborXizmatiFixed {

    @SuppressWarnings("java:S1192") // SQL fragmentlari ataylab takrorlangan, OMB-77
    public List<Qoldiq> qoldiqHisoboti(Long omborId) {
        return jdbc.query(QOLDIQ_SQL, qoldiqMapper, omborId);
    }

    // Eng tor doira: faqat shu o'zgaruvchi
    public void yuklash(Fayl fayl) {
        @SuppressWarnings("java:S2095") // stream'ni Spring konteyner yopadi
        InputStream oqim = fayl.ochish();
        resurslar.register(oqim);
    }
}
```

`// NOSONAR` izohi ham bor. U qatordagi barcha issue ni bostiradi, kalit talab qilmaydi va shu sababdan ancha qo'pol vosita. Uni faqat annotatsiya qo'yish imkoni bo'lmagan joyda ishlatish kerak, masalan annotatsiya qo'yiladigan element yo'q bo'lsa. Sonar da NOSONAR izohlarini kuzatuvchi qoida bor, uni profilda yoqib qo'yish foydali, shunda bostirishlar o'zi ko'rinadigan bo'ladi.

Uchinchi yo'l skanerlash konfiguratsiyasi. U eng kuchli va eng xavfli, chunki issue serverga umuman kelmaydi va UI da hech qanday iz qoldirmaydi.

```properties
# sonar-project.properties yoki pom.xml ichidagi <properties>
# Generatsiya qilingan koddagi va legacy adapterdagi qoidalarni e'tiborsiz qoldirish
sonar.issue.ignore.multicriteria=e1,e2
sonar.issue.ignore.multicriteria.e1.ruleKey=java:S1192
sonar.issue.ignore.multicriteria.e1.resourceKey=**/generated/**/*.java
sonar.issue.ignore.multicriteria.e2.ruleKey=java:S106
sonar.issue.ignore.multicriteria.e2.resourceKey=**/tools/MigratsiyaCli.java

# Butun fayllarni analizdan chiqarish (eng kuchli, eng ehtiyotkor ishlatiladigan)
sonar.exclusions=**/generated/**,**/*MapperImpl.java
# Coverage hisobidan chiqarish: kod tahlil qilinadi, lekin coverage talab qilinmaydi
sonar.coverage.exclusions=**/config/**,**/*Application.java
# Nusxa-kod (duplication) hisobidan chiqarish
sonar.cpd.exclusions=**/dto/**
```

| Holat | To'g'ri bostirish | Noto'g'ri bostirish |
|---|---|---|
| Spring maydon inyeksiyasi tufayli null ogohlantirish | konstruktor inyeksiyasiga o'tish, bostirish kerak emas | klassga `@SuppressWarnings` qo'yish |
| MapStruct generatsiya qilgan `*MapperImpl` | `sonar.exclusions` bilan generatsiya papkasini chiqarish | har bir generatsiya qilingan faylda NOSONAR |
| CLI vositasida `System.out` ishlatish | shu bitta fayl uchun multicriteria exclusion, sababi yozilgan | butun loyihada konsol chiqishi qoidasini o'chirish |
| Hisobotdagi murakkab formula | metodga `java:S3776`, ticket havolasi bilan, refaktoring rejada | murakkablik qoidasining chegarasini 15 dan 50 ga ko'tarish |
| Resursni konteyner yopadi | lokal o'zgaruvchiga tor bostirish, izoh bilan | `java:S2095` ni profildan olib tashlash |
| Test koddagi assertion uslubi | test uchun alohida profil yoki aniq qoidani o'chirish | `sonar.exclusions` ga testlarni qo'shib yuborish |
| Takrorlangan string literal DTO da | `sonar.cpd.exclusions` yoki konstanta chiqarish | butun paketni analizdan chiqarish |
| Haqiqiy SQL injection ogohlantirishi | parametrlangan query ga o'tish | "won't fix" deb belgilash |
| Klasspath to'liq emasligidan shovqin | `sonar.java.binaries` ni tuzatish | yuzlab issue ni false positive deb yopish |

## 24.5 Bostirishni ko'rib chiqish: ular to'planib qolmasligi uchun tartib

Bostirish bir marta qo'yiladi va abadiy yashaydi, agar hech kim uni qayta ko'rmasa. Shuning uchun tartib kerak. Eng arzon tartib: har bir bostirish pull request da ikkinchi odam tomonidan tasdiqlanadi va izohi tekshiriladi. Bu bitta qoidaning o'zi bostirishlar sonini sezilarli kamaytiradi, chunki ko'pchilik dasturchi izoh yozishdan ko'ra kodni tuzatishni osonroq deb topadi.

Ikkinchi qatlam davriy ko'rib chiqish. Chorakda bir marta koddagi barcha `@SuppressWarnings` va NOSONAR ro'yxati chiqariladi va har biri uchun uch savol beriladi: sabab hali ham amal qiladimi, havolasi ochiqmi, doirasi tor-mi. Javobi yo'q bo'lganlari olib tashlanadi.

```bash
# Koddagi barcha bostirishlarni ro'yxatga olish va eng ko'p uchraydiganlarini sanash
grep -rn --include='*.java' -E '@SuppressWarnings|NOSONAR' src/ > /tmp/suppressions.txt
wc -l /tmp/suppressions.txt

# Qaysi qoida eng ko'p bostirilgan: shu qoida haqida jamoada suhbat kerak
grep -rhoE 'java:S[0-9]+' src/ | sort | uniq -c | sort -rn | head -10

# Izohsiz bostirishlar: ular birinchi navbatda tuzatiladi
grep -rn --include='*.java' -E '@SuppressWarnings\("[^"]+"\)\s*$' src/

# Skanerlash konfiguratsiyasidagi yashirin exclusion larni ko'rish
grep -rnE 'sonar\.(exclusions|issue\.ignore|coverage\.exclusions)' pom.xml *.properties
```

Uchinchi qatlam serverdagi hisobot. False positive va accepted issue lar ro'yxatini filtr bilan chiqarib, muallif va sana bo'yicha ko'rib chiqish mumkin. Eng muhim signal: bitta qoida bo'yicha ko'p false positive. Bu qoidani butunlay o'chirish yoki parametrini o'zgartirish vaqti kelganini bildiradi.

## 24.6 Qoidani butunlay o'chirish qachon to'g'ri qaror

Qoidani o'chirish ko'pincha eng halol yechim. Agar jamoa bir qoidani yuz marta bostirgan bo'lsa, demak jamoa u qoidaga qo'shilmaydi. Yuz joyda yashirin bostirish saqlashdan ko'ra, profilda bir marta o'chirib, sababini yozib qo'yish aniqroq va tekshirilishi oson.

O'chirish uchun uchta mezon. Birinchisi, qoida bo'yicha bostirishlar soni haqiqiy tuzatishlar sonidan ko'p. Ikkinchisi, qoida loyihaning ongli uslub qaroriga qarshi turadi, masalan jamoa ataylab boshqa naming konvensiyasini ishlatadi. Uchinchisi, qoida bir xil holatda muntazam xato ishlaydi va buni konfiguratsiya tuzatmaydi.

O'chirmaslik kerak bo'lgan holat ham aniq. Agar qoida security kategoriyasida bo'lsa va bostirishlar bitta dasturchidan kelayotgan bo'lsa, bu qoida muammosi emas, bilim muammosi. Bunday paytda qoida qoladi, o'qitish qo'shiladi.

Amalda o'chirish quality profile ichida qilinadi va u versiyalanadigan artefakt bo'lishi kerak. Profilni eksport qilib repozitoriyda saqlash qaror tarixini ko'rsatadi.

```xml
<!-- Eksport qilingan quality profile fragmenti: qaror tarixi repozitoriyda qoladi -->
<!-- config/sonar/profile-backend.xml -->
<profile>
  <name>Backend Java</name>
  <language>java</language>
  <rules>
    <!-- Cognitive complexity: chegara ko'tarilgan, o'chirilmagan.
         Sabab: hisobot modulidagi formulalar, ADR-014. -->
    <rule>
      <repositoryKey>java</repositoryKey>
      <key>S3776</key>
      <priority>MAJOR</priority>
      <parameters>
        <parameter>
          <key>threshold</key>
          <value>20</value>
        </parameter>
      </parameters>
    </rule>
    <!-- Ishlatilmagan metod parametri: o'chirilgan.
         Sabab: event handler imzolari framework tomonidan belgilanadi, ADR-019. -->
  </rules>
</profile>
```

Parametrni o'zgartirish ko'pincha o'chirishdan yaxshiroq. Qoida yashab qoladi, lekin chegarasi jamoa haqiqatiga mos bo'ladi. Chegarani 15 dan 20 ga ko'tarish mumkin, 50 ga ko'tarish esa qoidani o'chirishning yashirin shakli.

## 24.7 O'z qoidangizni yozish: qachon zarur bo'ladi

O'z qoidangiz kerak bo'ladigan holat bitta: loyihada takrorlanadigan va avtomatik tekshirilishi mumkin bo'lgan o'z konvensiyangiz bor, va uni code review da aytishdan charchagansiz. Masalan "to'lov summasi hech qachon `double` bo'lmaydi", yoki "tashqi API chaqiruvi albatta timeout bilan bo'ladi", yoki "domen klassida Spring annotatsiyasi bo'lmaydi".

Oddiy holatlarda qoida yozish kerak emas. Sonar da shablon qoidalar bor: ulardan nusxa olib, o'z regex yoki parametringizni berasiz va natijada o'z qoidangiz paydo bo'ladi. Masalan izohlar yoki nomlar ustidan regex bilan ishlaydigan shablonlar shu tarzda ishlatiladi. Bu yo'l bir soatlik ish, o'z plaginini yozish esa bir hafta va doimiy qo'llab-quvvatlash.

Chindan ham AST darajasida tekshiruv kerak bo'lsa, Java uchun custom plugin yoziladi. Unda `IssuableSubscriptionVisitor` dan meros olinadi va qaysi tugunlarni kuzatish aytiladi.

```java
// Custom Sonar Java qoidasi skeleti.
// API nomlari sonar-java versiyasiga qarab farq qiladi, misol repozitoriyasini tekshiring.
@Rule(key = "TolovSummasiDouble")
public class TolovSummasiDoubleRule extends IssuableSubscriptionVisitor {

    @Override
    public List<Tree.Kind> nodesToVisit() {
        return List.of(Tree.Kind.VARIABLE); // maydon va lokal o'zgaruvchilar
    }

    @Override
    public void visitNode(Tree tree) {
        VariableTree variable = (VariableTree) tree;
        String tip = variable.type().symbolType().fullyQualifiedName();
        String nom = variable.simpleName().name().toLowerCase(Locale.ROOT);

        boolean pulgaOxshash = nom.contains("summa") || nom.contains("narx");
        boolean suzuvchiTip = "double".equals(tip) || "float".equals(tip);

        if (pulgaOxshash && suzuvchiTip) {
            reportIssue(variable.simpleName(),
                "Pul miqdori uchun BigDecimal ishlatilsin, double aniqlikni yo'qotadi.");
        }
    }
}
```

Plaginni yozishdan oldin uchta narxni hisoblang. Birinchisi, plagin SonarQube versiyasiga bog'lanadi va har yangilanishda tekshirilishi kerak. Ikkinchisi, plaginni serverga admin o'rnatadi, demak deployment jarayoni paydo bo'ladi. Uchinchisi, qoidaga test yozish kerak, aks holda u o'zi false positive manbasiga aylanadi.

## 24.8 Qoida yozishning muqobillari: ArchUnit, linter, code review qoidasi

Ko'p holatda Sonar plagini eng qimmat yechim va eng arzon muqobil bor. Arxitektura cheklovlari uchun ArchUnit to'g'ri vosita: u oddiy test, repozitoriyda yashaydi, pull request da ishlaydi va buzilganda darhol qizil bo'ladi. Serverga hech narsa o'rnatilmaydi. ArchUnit ning batafsil mavzusi [testlash qo'llanmasidagi](../testing/README.md) ArchUnit bo'limida.

Formatlash va import tartibi uchun Spotless yoki Checkstyle arzonroq, chunki ular kodni o'zi tuzatadi. Bog'liqlik versiyalari uchun Maven Enforcer. Kutubxona ichidagi taqiqlangan API lar uchun ko'pincha oddiy arch test yetarli.

| Tuzoq | Yechim |
|---|---|
| Har bir konvensiya uchun Sonar plagini yozish | avval shablon qoida, keyin ArchUnit, plagin oxirgi chora |
| Plagin yozilgan, lekin unga test yozilmagan | qoidaga musbat va manfiy misollar bilan test majburiy |
| Plagin SonarQube yangilanishida sinadi | plagin versiyasi va server versiyasi CI da birga tekshiriladi |
| ArchUnit testi bor, lekin pipeline da ishlamaydi | arch testlar asosiy test fazasiga kiritiladi, alohida profilga yashirilmaydi |
| Bir xil tekshiruv Sonar da ham, linterda ham | bitta egasi tanlanadi, ikkinchisi o'chiriladi |
| Konvensiya faqat README da yozilgan | avtomatlashtirilmagan konvensiya buziladi, uni testga aylantirish kerak |
| Qoida juda keng yozilgan, shovqin beradi | qoida tor shartdan boshlanadi, keyin asta kengaytiriladi |
| Legacy kod yangi qoidani darhol buzadi | qoida faqat yangi kodga qo'llanadi yoki legacy paket vaqtincha chiqariladi |

## 24.9 Jamoaviy kelishuv: kim belgilaydi, kim tasdiqlaydi

Bostirish texnik emas, boshqaruv masalasi. Agar hamma hamma narsani bostira olsa, quality gate ma'nosini yo'qotadi. Shuning uchun huquqlarni ajratish kerak. SonarQube da issue ni false positive yoki accepted deb belgilash uchun maxsus huquq bor, u standart holatda keng tarqalgan, va uni cheklash birinchi qadam.

Ishlaydigan model quyidagicha. Dasturchi bostirishni taklif qiladi, ya'ni kodda annotatsiya va izoh bilan pull request ochadi. Reviewer izohni tekshiradi. Qoidani o'chirish yoki profil parametrini o'zgartirish esa boshqa darajada hal qilinadi: buni texnik yetakchi yoki arxitektor qiladi va qarorni ADR shaklida yozadi.

Muhim nuans: serverdagi UI orqali belgilash kod tarixida iz qoldirmaydi. Shu sababdan ko'p jamoa shunday kelishadi: doimiy bostirish koddagi annotatsiya bilan qilinadi, UI orqali belgilash esa faqat vaqtincha va faqat "Administer Issues" huquqi bor odamlar tomonidan. Shunda har bir bostirish git tarixida muallifi va sababi bilan qoladi.

```xml
<!-- pom.xml: skaner konfiguratsiyasi repozitoriyda, ya'ni review ostida -->
<properties>
  <sonar.projectKey>ombor-backend</sonar.projectKey>
  <!-- Versiyani qotirib qo'yish: skaner yangilanishi kutilmagan natija bermasligi uchun -->
  <sonar.maven.plugin.version><!-- joriy versiyani tekshirib yozing --></sonar.maven.plugin.version>
  <!-- Analiz uchun kompilyatsiya natijasi: to'liq bo'lmasa false positive ko'payadi -->
  <sonar.java.binaries>${project.build.outputDirectory}</sonar.java.binaries>
  <sonar.coverage.jacoco.xmlReportPaths>
    ${project.build.directory}/site/jacoco/jacoco.xml
  </sonar.coverage.jacoco.xmlReportPaths>
</properties>
```

## 24.10 Suppression statistikasini kuzatish va ularni kamaytirish

O'lchanmagan narsa boshqarilmaydi. Bostirishlar uchun uchta oddiy metrika yetarli. Birinchisi, koddagi `@SuppressWarnings` va NOSONAR larning umumiy soni. Ikkinchisi, serverdagi false positive va accepted issue lar soni. Uchinchisi, bir qoida bo'yicha bostirishlarning eng yuqori ulushi.

Bu uch raqamni har sprintda yozib borish kerak. O'sish tendensiyasi ikki xil ma'no beradi. Agar accepted o'sayotgan bo'lsa, texnik qarz to'planayapti. Agar false positive o'sayotgan bo'lsa, sozlama yoki profil muammosi bor va uni tuzatish bitta ishda yuzlab issue ni yopadi.

```sql
-- Bostirishlar sonini o'z metrika jadvalingizda kuzatish misoli.
-- Raqamlar CI dagi grep natijasidan va server hisobotidan yoziladi.
CREATE TABLE sifat_metrikasi (
    sana            DATE         NOT NULL,
    modul           VARCHAR(64)  NOT NULL,
    suppress_kod    INTEGER      NOT NULL, -- @SuppressWarnings va NOSONAR soni
    false_positive  INTEGER      NOT NULL, -- serverda FP deb belgilangan
    accepted        INTEGER      NOT NULL, -- ongli qoldirilgan issue lar
    PRIMARY KEY (sana, modul)
);

-- Oxirgi olti o'lchovda bostirishlar o'sganmi: tendensiyani ko'rish
SELECT modul,
       MIN(suppress_kod) AS eng_kam,
       MAX(suppress_kod) AS eng_ko_p,
       MAX(suppress_kod) - MIN(suppress_kod) AS o_sish
FROM sifat_metrikasi
WHERE sana > CURRENT_DATE - INTERVAL '6 months'
GROUP BY modul
ORDER BY o_sish DESC;
```

Kamaytirishning eng samarali usuli guruhlab ishlash. Eng ko'p bostirilgan bitta qoidani olasiz va uning hamma holatini bir sprintda hal qilasiz: qismi tuzatiladi, qismi uchun qoida parametri o'zgartiriladi, qolgani uchun qoida o'chiriladi. Bitta-bitta tuzatish bu ishni hech qachon tugatmaydi.

## 24.11 Sonar charchog'i: belgilar ko'payib ketganda nima qilish

Sonar charchog'i shunday ko'rinadi: dasturchi hisobotni ochmaydi, chunki unda yuzlab issue bor va ularning qaysi biri muhimligi tushunarsiz. Natija: gate ni o'tkazish uchun mexanik bostirish boshlanadi va vosita o'z ma'nosini yo'qotadi.

Davosi texnik emas, fokusni toraytirishda. Birinchi qadam: faqat yangi kodga qarash. Clean as You Code yondashuvi aynan shu uchun ishlab chiqilgan, legacy dagi minglab issue gate ni bloklamaydi. Ikkinchi qadam: profilni qisqartirish. Haqiqiy bug va security qoidalarini qoldirib, uslub qoidalarining bir qismini formatlovchi vositaga topshirish shovqinni keskin kamaytiradi.

Uchinchi qadam: bitta mavzuga fokus. Bu chorak faqat resurs yopilishi, keyingisi faqat null xavfsizligi. To'rtinchi qadam: kirish nuqtasi IDE bo'lishi. SonarLint yoki IDE plagini ogohlantirishni yozish paytida ko'rsatsa, issue CI ga yetib bormaydi va charchoq ham paydo bo'lmaydi.

Oxirgi va eng muhim qadam: bostirishni oson, tuzatishni qiyin qilib qo'ymaslik. Agar bostirish bir klik, tuzatish esa yarim kun bo'lsa, jamoa doim bostirishni tanlaydi. Izoh majburiyati va reviewer tasdig'i aynan shu balansni teskari tomonga buradi.

## 24.12 Amalda qo'llash

- [ ] `sonar.java.binaries` va kutubxona yo'llarini tekshirib, klasspathdan kelayotgan false positive larni bitta ishda yo'q qiling.
- [ ] Koddagi barcha `@SuppressWarnings` va NOSONAR ni `grep` bilan ro'yxatga oling, izohsiz bo'lganlariga sabab yozing yoki olib tashlang.
- [ ] Jamoada yozma qoida qabul qiling: false positive va accepted farqi, izohning to'rt elementi, va kim tasdiqlashi.
- [ ] "Administer Issues" huquqini cheklangan guruhga bering, doimiy bostirishlarni koddagi annotatsiyaga ko'chiring.
- [ ] Eng ko'p bostirilgan uchta qoidani aniqlang va har biri uchun qaror qabul qiling: tuzatish, parametrni o'zgartirish yoki o'chirish.
- [ ] Quality profile ni eksport qilib repozitoriyda saqlang, har bir o'chirilgan qoida yoniga sabab va ADR havolasini yozing.
- [ ] Yangi konvensiyani Sonar plagini bilan emas, avval shablon qoida yoki ArchUnit testi bilan avtomatlashtirishga harakat qiling.
- [ ] Har sprintda suppress, false positive va accepted sonlarini yozib boring va chorakda tendensiyani ko'rib chiqing.

---

[&larr; 23. Legacy loyihani 100% ga olib chiqish rejasi](23-legacy-loyihani-100-ga-olib-chiqish-rejasi.md) · [Mundarija](README.md) · [25. Xato katalogi: reliability &rarr;](25-xato-katalogi-reliability-bug-toifasi.md)
