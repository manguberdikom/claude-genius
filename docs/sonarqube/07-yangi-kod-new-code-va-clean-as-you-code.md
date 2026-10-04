<!-- doc: sonarqube | chapter: 7 | part: II. Quality gate -->

[SonarQube](../../README.md) / [SonarQube](README.md)

# 7. Yangi kod (new code) va "clean as you code" tamoyili (New Code and Clean as You Code)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

- [7.1 Yangi kod nima: ta'rifi va u nega alohida o'lchanadi](#71-yangi-kod-nima-tarifi-va-u-nega-alohida-olchanadi)
- [7.2 Yangi kod chegarasini belgilash usullari](#72-yangi-kod-chegarasini-belgilash-usullari)
- [7.3 Qaysi usul qaysi reliz jarayoniga mos keladi](#73-qaysi-usul-qaysi-reliz-jarayoniga-mos-keladi)
- [7.4 "Clean as you code" tamoyili: eski qarzni to'lamay turib oldinga siljish](#74-clean-as-you-code-tamoyili-eski-qarzni-tolamay-turib-oldinga-siljish)
- [7.5 Yangi kod ustidagi shartlar va umumiy kod ustidagi shartlar farqi](#75-yangi-kod-ustidagi-shartlar-va-umumiy-kod-ustidagi-shartlar-farqi)
- [7.6 Pull request tahlilida yangi kod qanday aniqlanadi](#76-pull-request-tahlilida-yangi-kod-qanday-aniqlanadi)
- [7.7 Faylni ko'chirish, formatlash va refaktoring yangi kodni qanday shishiradi](#77-faylni-kochirish-formatlash-va-refaktoring-yangi-kodni-qanday-shishiradi)
- [7.8 Blame ma'lumoti buzilganda nima bo'ladi va uni qanday tuzatish](#78-blame-malumoti-buzilganda-nima-boladi-va-uni-qanday-tuzatish)
- [7.9 Yangi kodda 100% talab qilishning amaliy oqibatlari](#79-yangi-kodda-100-talab-qilishning-amaliy-oqibatlari)
- [7.10 Eski kod reytingi va yangi kod reytingini bir vaqtda kuzatish](#710-eski-kod-reytingi-va-yangi-kod-reytingini-bir-vaqtda-kuzatish)
- [7.11 Amalda qo'llash](#711-amalda-qollash)

</details>



Sonar hisoblaydigan metrikalarning yarmi "yangi kod" ustida o'lchanadi. Bu bitta sozlama emas, balki butun bir ish uslubi: jamoa eski qarzni to'lamay turib ham sifatni oshira boradi. Lekin yangi kod chegarasi noto'g'ri qo'yilsa yoki git tarixi buzilgan bo'lsa, quality gate kutilmaganda qizil yonadi va hech kim nega qizil ekanini tushunmaydi. Bu bobda yangi kod qanday aniqlanishi, qaysi chegara usuli qaysi reliz jarayoniga mos kelishi va amalda eng ko'p uchraydigan tuzoqlar ko'rib chiqiladi.

## 7.1 Yangi kod nima: ta'rifi va u nega alohida o'lchanadi

Yangi kod deganda Sonar belgilangan chegaradan keyin o'zgargan yoki qo'shilgan kod qatorlarini tushunadi. Sonar buni fayl darajasida emas, qator darajasida hisoblaydi. Har bir qator uchun SCM blame ma'lumotidan oxirgi o'zgartirish sanasi va commit identifikatori olinadi. Agar shu sana chegaradan keyin bo'lsa, qator yangi kod to'plamiga kiradi.

Shundan keyin Sonar alohida metrikalar to'plamini hisoblaydi. Ular `new_` prefiksi bilan boshlanadi: yangi kodda qoplanganlik, yangi issue soni, yangi kodda takrorlangan qatorlar ulushi, yangi kodda qoplanishi kerak bo'lgan qatorlar soni. Bu metrikalar umumiy metrikalardan mustaqil.

Nega alohida o'lchanadi: umumiy metrikalar eski kodning massasi tufayli deyarli qimirlamaydi. Yetti yillik loyihada 200 ming qator bor va qoplanganlik 24 foiz bo'lsa, bitta sprintda yozilgan 800 qator mukammal test bilan ham umumiy raqamni 25 foizga ko'tarmaydi. Jamoa harakat qiladi, tablo o'zgarmaydi, metrikaga ishonch yo'qoladi.

Yangi kod metrikasi esa darhol javob beradi va shu sprintda yozilgan kodning sifatini ko'rsatadi. Bu mas'uliyat taqsimotiga ham to'g'ri keladi: pull request muallifi o'zi yozgan kod uchun javob beradi, 2019 yilda ketgan hamkasbining kodi uchun emas.

## 7.2 Yangi kod chegarasini belgilash usullari

Sonar bir nechta usulni taklif qiladi. Nomlanishi SonarQube versiyasiga qarab farq qiladi, lekin mohiyati bir xil qoladi. Eski liniyalarda bu "leak period" deb atalgan va `sonar.leak.period` xossasi bilan sozlangan. 9.9 LTA va 2025 LTA liniyalarida sozlama loyiha sozlamalarining "New Code" bo'limida turadi va global standart qiymat ham bor.

Birinchi usul: oldingi versiya. Sonar `sonar.projectVersion` qiymatining oxirgi o'zgarishini chegara deb oladi. Versiya `1.4.0` dan `1.5.0` ga o'tganda chegara avtomatik suriladi.

Ikkinchi usul: aniq sanadan boshlab. Chegara qo'lda qo'yilgan kalendar sanaga mixlanadi. Shu sanadan keyingi hamma narsa abadiy yangi kod bo'lib qoladi.

Uchinchi usul: kun soni. Suriluvchi oyna, masalan oxirgi 30 kun. Har kuni chegara bir kun oldinga suriladi.

To'rtinchi usul: aniq versiya yoki aniq tahlil. Siz ro'yxatdan bitta tahlilni tanlab, uni baseline qilib mixlaysiz. Bu "modernizatsiya shu nuqtadan boshlandi" degan ma'noni beradi.

Beshinchi usul, branch uchun eng muhimi: reference branch. Branchdagi yangi kod `main` bilan solishtirilib aniqlanadi. Bu `sonar.newCode.referenceBranch` xossasi bilan ham beriladi.

| Usul | Chegara qanday suriladi | Kuchli tomoni | Zaif tomoni | Kimga mos |
|---|---|---|---|---|
| Oldingi versiya | `sonar.projectVersion` o'zgarganda | Reliz bilan tabiiy mos | Versiya qo'lda o'zgarmasa chegara muzlaydi | Semantik versiyalangan kutubxona va servis |
| Aniq sana | Hech qachon, qo'lda o'zgartiriladi | Modernizatsiya boshlanishi aniq qolar | Vaqt o'tib yangi kod massasi o'sib ketadi | Qisqa muddatli tozalash kampaniyasi |
| Kun soni | Har kuni avtomatik | Sozlashni talab qilmaydi | Oyna ichidan chiqqan issue tabloni tark etadi | Tez-tez deploy qiladigan jamoa |
| Aniq tahlil / versiya | Faqat qo'lda | Baseline butunlay nazoratda | Unutilsa yillar davomida eskiradi | Legacy audit va shartnomaviy baseline |
| Reference branch | Har PR uchun avtomatik, diff asosida | PR uchun eng aniq natija | To'liq git tarixi majburiy | Trunk based va GitFlow jamoalari |

## 7.3 Qaysi usul qaysi reliz jarayoniga mos keladi

Agar siz har sprint oxirida versiya chiqarsangiz va Maven versiyasi haqiqatda o'zgarsa, "oldingi versiya" eng toza variant. Yangi kod "oxirgi relizdan keyin yozilgani" degan ma'noni oladi va buni biznes ham tushunadi. Shart: build versiyani Sonarga uzatishi kerak.

```xml
<!-- pom.xml: Sonar loyiha versiyasini Maven versiyasiga bog'lab qo'yamiz -->
<!-- shunda "oldingi versiya" chegarasi reliz bilan birga suriladi -->
<properties>
  <sonar.projectKey>warehouse-service</sonar.projectKey>
  <sonar.projectVersion>${project.version}</sonar.projectVersion>
  <!-- blame ishlashi uchun SCM provayderi aniq ko'rsatiladi -->
  <sonar.scm.provider>git</sonar.scm.provider>
  <!-- generatsiya qilingan kod yangi kodni shishirmasligi uchun chiqarib tashlanadi -->
  <sonar.exclusions>**/generated/**,**/*MapperImpl.java</sonar.exclusions>
  <sonar.coverage.exclusions>**/config/**,**/dto/**</sonar.coverage.exclusions>
</properties>
```

Agar siz kuniga bir necha marta deploy qilsangiz va versiya tushunchasi amalda yo'q bo'lsa, "kun soni" qulay. 30 kun ko'pchilik jamoa uchun muvozanatli. 7 kun juda qisqa, chunki ta'tilga ketgan odamning kodi tabloni tark etadi. 90 kun juda uzun, chunki chorak oxirida gate ostidagi qarz to'planib qoladi.

Uzoq yashaydigan `develop` branchi va reliz branchlari bo'lsa, reference branch eng aniq natija beradi. Bunda feature branch `develop` bilan, reliz branchi `main` bilan solishtiriladi. Monorepoda esa global standart qiymatga tayanmang. Har modulning reliz ritmi boshqacha, shuning uchun sozlama loyiha darajasida qo'yiladi.

Legacy modernizatsiya loyihasida "aniq tahlil" usuli ishlatiladi: birinchi tahlil baseline qilinadi va kelishuv shunday bo'ladi, bu nuqtadan keyingi hamma kod toza. Lekin kalendarga eslatma qo'ying, chunki ikki yildan keyin bu baseline ma'nosini yo'qotadi.

## 7.4 "Clean as you code" tamoyili: eski qarzni to'lamay turib oldinga siljish

"Clean as you code" uchta oddiy qoidadan iborat. Birinchi: tegmagan kodni tozalamaysiz. Ikkinchi: tekkan kodni standartga keltirasiz. Uchinchi: quality gate faqat yangi kodni ushlaydi.

Bu tamoyil iqtisodiy mantiqqa asoslanadi. Yillar davomida o'zgarmaydigan kod issue'li bo'lsa ham xarajat keltirmaydi. O'zgarayotgan qism esa o'zi haqida signal beradi: u yerda bug paydo bo'ladi va vaqt ketadi. Clean as you code aynan shu qizigan joylarni tozalaydi.

Misol: `PaymentService` 900 qator, cognitive complexity osmonda, qoplanganlik 11 foiz. Sizga refund funksiyasi kerak. Yomon yondashuv: butun klassni qayta yozish, 900 qatorli PR, hech kim review qilmaydi. To'g'ri yondashuv: refund logikasini alohida, test bilan qoplangan klassga chiqarish va unga delegatsiya qilish.

```java
// Yomon: yangi logika eski 900 qatorli klass ichiga tiqiladi.
// Sonar java:S3776 (cognitive complexity) bo'yicha shikoyat qiladi,
// chunki o'zgargan metod yangi kod sifatida qayta o'lchanadi.
public void process(Order order) {
    if (order.getType() == OrderType.REFUND) {
        if (order.getAmount().compareTo(BigDecimal.ZERO) > 0) {
            if (order.getPayment() != null) {
                if (order.getPayment().isSettled()) {
                    // ... yana besh qatlam ichma-ich shart
                }
            }
        }
    }
}
```

```java
// Sonar o'tadigan variant: yangi logika alohida klassda,
// complexity past, har bir tarmoq test bilan qoplanadi.
@Service
class RefundProcessor {

    private static final String NOT_SETTLED = "To'lov hali yakunlanmagan";

    RefundResult refund(Payment payment, BigDecimal amount) {
        // qo'riqchi shartlar: ichma-ich if o'rniga erta qaytish
        if (!payment.isSettled()) {
            return RefundResult.rejected(NOT_SETTLED);
        }
        if (amount.compareTo(payment.amount()) > 0) {
            return RefundResult.rejected("Summa to'lovdan katta");
        }
        return RefundResult.accepted(amount);
    }
}
```

Eski `process` metodiga faqat bitta delegatsiya qatori qo'shiladi. Yangi kod to'plami kichik, toza va to'liq qoplangan. Eski 900 qator o'z holida qoladi va gate'ni qizartirmaydi.

## 7.5 Yangi kod ustidagi shartlar va umumiy kod ustidagi shartlar farqi

Sonar'ning standart gate'i (Sonar way) faqat yangi kod shartlaridan tuzilgan. Bu tasodif emas, bu mahsulot falsafasi. Umumiy kod ustiga shart qo'yish texnik jihatdan mumkin, lekin ko'p hollarda bu xato.

Tasavvur qiling, umumiy qoplanganlik uchun 80 foiz sharti qo'yildi, hozirgi qiymat 22 foiz. Gate birinchi kundan qizil va yillar davomida qizil qoladi. Jamoa gate'ni o'chiradi yoki uni e'tiborsiz qoldiradi. Ikkinchisi yomonroq, chunki haqiqiy yangi muammo shu qizil fonda ko'rinmay ketadi.

Yangi kod shartlari esa bajarilishi mumkin. Yangi kodda 80 foiz qoplanganlik, yangi kodda yuqori og'irlikdagi issue bo'lmasligi, yangi kodda takrorlanish 3 foizdan oshmasligi: bularning hammasi bitta PR ichida hal qilinadi.

Umumiy metrikani butunlay tashlab yubormang. Uni gate shartiga emas, kuzatuv ko'rsatkichiga aylantiring. Bu haqda oxirgi bo'limda gaplashamiz.

| Savol | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Chegara usuli | Global standartni o'zgartirmaydi | Har loyihaning reliz ritmiga qarab tanlanadi |
| Umumiy coverage | Gate shartiga qo'yiladi, gate abadiy qizil | Trend sifatida kuzatiladi, gate yangi kodda |
| Legacy qarz | "Keling, hammasini tozalaymiz" sprinti rejalanadi | Tegilgan joy tozalanadi, qolgani kuzatuvda |
| Formatlash | Spotless butun repoga bir marta qo'llanadi | Alohida commitda, blame-ignore ro'yxati bilan |
| Fayl ko'chirish | Ko'chirish, formatlash, logika bitta commitda | Uch alohida commit, har biri tekshiriladi |
| CI klon | `fetch-depth: 1`, tez bo'lsin deb | `fetch-depth: 0`, blame to'g'ri bo'lsin deb |
| Yangi kod coverage talabi | 100 foiz, "sifat shunday bo'ladi" | 80 foiz, ustiga assertion sifati review'da |
| Kichik PR gate'da yiqilsa | Shart o'chiriladi yoki issue "won't fix" qilinadi | Istisno jurnalga yozilib, sababi bilan tasdiqlanadi |
| Generatsiya qilingan kod | Tahlilda qoladi va yangi kodni shishiradi | `sonar.exclusions` bilan chiqariladi |
| Baseline | Bir marta qo'yilib unutiladi | Chorakda qayta ko'rib chiqiladi |

## 7.6 Pull request tahlilida yangi kod qanday aniqlanadi

PR tahlilida Sonar loyihaning New Code sozlamasini ishlatmaydi. U PR diff'iga tayanadi. Aniqrog'i, PR branchi va base branch orasidagi merge base topiladi va shundan keyingi o'zgarishlar yangi kod deb olinadi. Shuning uchun PR tahlili uchun to'liq git tarixi majburiy.

Scanner'ga uchta xossa kerak: PR kaliti, PR branchi nomi va base branch nomi. CI integratsiyasi (GitHub Actions, GitLab CI, Bitbucket) ko'p hollarda bularni avtomatik aniqlaydi, lekin aniqlamagan holda qo'lda beriladi.

```yaml
# .github/workflows/sonar.yml
name: sonar
on: [pull_request]
jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          # 0 degani to'liq tarix: blame va merge base shunda ishlaydi
          fetch-depth: 0
      - uses: actions/setup-java@v4
        with:
          java-version: '21'
          distribution: temurin
      # test va JaCoCo hisoboti bitta buildda tayyorlanadi
      - name: Build va tahlil
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
        run: >
          ./mvnw -B verify
          org.sonarsource.scanner.maven:sonar-maven-plugin:sonar
          -Dsonar.host.url=${{ vars.SONAR_HOST_URL }}
          -Dsonar.pullrequest.key=${{ github.event.number }}
          -Dsonar.pullrequest.branch=${{ github.head_ref }}
          -Dsonar.pullrequest.base=${{ github.base_ref }}
```

Yana bir muhim nuqta: PR tahlilida qoplanganlik shu buildda ishlab chiqilgan JaCoCo hisobotidan olinadi. Agar testlar o'tkazib yuborilsa yoki `jacoco.exec` fayli yo'q bo'lsa, yangi kod qoplanganligi 0 foiz chiqadi va gate yiqiladi. Bu Sonar xatosi emas, bu build tartibi xatosi.

```properties
# sonar-project.properties: Maven ishlatilmaydigan loyihalar uchun
sonar.projectKey=order-api
sonar.sources=src/main/java
sonar.tests=src/test/java
sonar.java.binaries=target/classes
# JaCoCo XML hisoboti yo'li aniq ko'rsatiladi
sonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml
# branch tahlili uchun taqqoslash nuqtasi
sonar.newCode.referenceBranch=main
sonar.scm.provider=git
sonar.scm.forceReloadAll=false
```

## 7.7 Faylni ko'chirish, formatlash va refaktoring yangi kodni qanday shishiradi

Yangi kod blame sanasiga tayanadi, blame sanasi esa qatorning oxirgi o'zgarishiga qaraydi. Formatlash o'zgarishi ham o'zgarish hisoblanadi.

Agar siz Spotless yoki IDE formatlashini butun repoga bir marta qo'llasangiz, yuz minglab qator yangi blame sanasini oladi. Keyingi tahlilda yangi kod hajmi 200 ming qatorga chiqadi, qoplanganlik 20 foizga tushadi va gate qizil yonadi. Kod mazmunan bir zarra ham o'zgarmagan.

Fayl ko'chirish ham xuddi shunday xatarli. Git faylni ko'chirishni o'zi aniqlaydi, lekin faqat mazmun yetarlicha o'xshash bo'lsa. Faylni ko'chirib, shu commitda uni formatlab va ustiga logikani o'zgartirsangiz, git o'xshashlikni topolmaydi. Natijada butun fayl yangi fayl sifatida ko'rinadi.

Shuning uchun qoida oddiy: bitta commit bitta turdagi ishni qiladi. Avval ko'chirish commiti, keyin formatlash commiti, keyin logika commiti.

Flyway migratsiyalariga ham qaytib tegmang, chunki har tegish ularni yangi kodga qaytaradi.

```sql
-- V37__add_refund_table.sql
-- Yangi migratsiya: bu fayl yangi kod sifatida tahlil qilinadi.
-- Eski migratsiyalarni formatlash uchun ham qayta ochmang.
CREATE TABLE refund (
    id          BIGSERIAL PRIMARY KEY,
    payment_id  BIGINT        NOT NULL REFERENCES payment (id),
    amount      NUMERIC(19, 4) NOT NULL CHECK (amount > 0),
    status      VARCHAR(32)   NOT NULL,
    created_at  TIMESTAMPTZ   NOT NULL DEFAULT now()
);

-- qidiruv ko'p ishlatiladigan ustun bo'yicha indeks
CREATE INDEX idx_refund_payment ON refund (payment_id);
```

| Tuzoq | Nima bo'ladi | Yechim |
|---|---|---|
| Butun repoga formatlash bitta commitda | Hamma qator yangi kodga aylanadi, coverage quladi | Alohida commit, `.git-blame-ignore-revs` ga qo'shish |
| Ko'chirish va o'zgartirish bitta commitda | Git ko'chirishni aniqlamaydi, fayl to'liq yangi | Avval faqat `git mv` commiti, keyin logika |
| CI da `fetch-depth: 1` | Blame yo'q, yangi kod noto'g'ri hisoblanadi | `fetch-depth: 0` qilib qo'yish |
| Generatsiya qilingan kod tahlilda | Yangi kod shishadi, soxta issue oqimi | `sonar.exclusions` ga qo'shish |
| JaCoCo hisoboti buildda yo'q | Yangi kodda 0 foiz coverage, gate qizil | `verify` fazasidan keyin tahlil qilish |
| Kichik bugfix PR | Bitta qoplanmagan qator 0 foiz beradi | Absolut shart yoki tasdiqlangan istisno |
| Satr oxiri (CRLF/LF) o'zgarishi | Butun fayl o'zgargan ko'rinadi | `.gitattributes` bilan normalizatsiya |
| Baseline unutilgan | Ikki yillik kod "yangi" bo'lib qoladi | Chorakda New Code sozlamasini ko'rib chiqish |

## 7.8 Blame ma'lumoti buzilganda nima bo'ladi va uni qanday tuzatish

Blame buzilishining uchta asosiy sababi bor. Sayoz klon: CI `--depth 1` bilan klon qiladi va tarix yo'q. `.git` katalogi tahlil bosqichida mavjud emas, masalan artefakt boshqa job'ga ko'chirilganda. Loyiha boshqa VCS'dan import qilingan va butun tarix bitta "initial import" commitida.

Blame bo'lmaganda Sonar yangi kodni ishonchli aniqlay olmaydi. Ba'zi holatlarda yangi kod bo'sh chiqadi va gate hamma narsani o'tkazib yuboradi, bu yolg'on yashil. Boshqa holatlarda hamma fayl yangi deb olinadi va gate asossiz qizil yonadi. Ikkisi ham yomon, lekin yolg'on yashil xavfliroq.

Tekshirish va tuzatish bosqichlari:

```bash
# 1. Klon to'liqmi: natija "true" bo'lsa tarix sayoz
git rev-parse --is-shallow-repository

# 2. Sayoz bo'lsa to'liq tarixni tortib olish
git fetch --unshallow --tags

# 3. Muammoli faylda blame ishlayaptimi
git blame -L 1,20 --date=short src/main/java/.../PaymentService.java

# 4. Formatlash commitini blame hisobidan chiqarish (git tomonidagi chora)
echo "a1b2c3d4e5f6 # butun repoga spotless qo'llangan commit" >> .git-blame-ignore-revs
git config blame.ignoreRevsFile .git-blame-ignore-revs

# 5. Tahlilni SCM ma'lumotini qayta o'qishga majburlash
./mvnw sonar:sonar -Dsonar.scm.forceReloadAll=true
```

Bitta halol ogohlantirish: `.git-blame-ignore-revs` git buyruqlari uchun ishlaydi, lekin Sonar bu faylni o'qiydimi yoki yo'qmi, bu versiyaga va SCM plaginiga bog'liq. Shuning uchun unga yagona himoya sifatida tayanmang. Asosiy himoya hali ham formatlashni alohida commitda saqlash va formatlashdan keyin New Code chegarasini bilib turib surish.

## 7.9 Yangi kodda 100% talab qilishning amaliy oqibatlari

100 foiz talabi birinchi qarashda halol tuyuladi. Amalda u bir nechta nojo'ya ta'sir keltiradi.

Birinchi oqibat: assertion'siz testlar. Dasturchi qatorni "bosib o'tish" uchun test yozadi, lekin natijani tekshirmaydi. Sonar bunga `java:S2699` (test assertion'ni o'z ichiga olishi kerak) bilan javob berishi mumkin, lekin bu qoida hamma holatni tutmaydi.

```java
// Yomon: coverage bor, qiymat yo'q. Hech narsa tekshirilmaydi.
@Test
void refundWorks() {
    processor.refund(settledPayment(), new BigDecimal("10.00"));
}

// Sonar o'tadigan va haqiqatan foydali variant:
@Test
void settleQilinmaganTolovQaytarilmaydi() {
    RefundResult result = processor.refund(notSettledPayment(), BigDecimal.TEN);

    assertThat(result.accepted()).isFalse();
    assertThat(result.reason()).isEqualTo("To'lov hali yakunlanmagan");
}
```

Ikkinchi oqibat: kichik PR'da denominator muammosi. Bitta qatorli bugfix PR'da yangi kod 2 qator bo'lsa va bittasi qoplanmagan bo'lsa, qoplanganlik 50 foiz chiqadi va gate yiqiladi. Mantiqan PR yaxshi, mexanik ravishda qizil.

Uchinchi oqibat: odamlar tizimni aylanib o'tishni o'rganadi. Issue'lar "won't fix" deb belgilanadi va coverage exclusions ro'yxati asossiz o'sadi.

Amaliy tavsiya: yangi kodda 80 foiz qoplanganlik va yuqori og'irlikdagi yangi issue'ning nol bo'lishi ko'p jamoa uchun to'g'ri muvozanat. Qolgani review'ning ishi. Review'da ko'rilishi kerak bo'lgan savol "qoplanganlik qancha" emas, balki "bu test buzilsa, qanday bug ushlanadi".

Kichik PR muammosini hal qilish uchun absolut shartni ishlatish mumkin: yangi kodda qoplanmagan qatorlar soni ma'lum chegaradan oshmasligi. Bu foizga qaraganda kichik diff'larda barqarorroq ishlaydi.

## 7.10 Eski kod reytingi va yangi kod reytingini bir vaqtda kuzatish

Gate faqat yangi kodni ushlasa, eski kod ko'rinmay qolish xavfi bor. Shuning uchun ikkita qatlam kerak: gate yangi kod ustida, kuzatuv esa ikkisi ustida.

Gate shartlari faqat `new_` metrikalari bilan yoziladi. Umumiy metrikalar esa oylik trend sifatida o'qiladi: umumiy qoplanganlik o'syaptimi, issue soni kamayayaptimi. Muhimi raqamning qiymati emas, balki yo'nalishi.

Trendni API orqali olish va uni hisobotga qo'yish oson:

```bash
# Umumiy va yangi kod metrikalarining tarixi: yo'nalishni ko'rish uchun
curl -s -u "$SONAR_TOKEN:" \
  "$SONAR_URL/api/measures/search_history?component=warehouse-service\
&metrics=coverage,new_coverage,violations,new_violations,sqale_rating\
&from=2026-01-01" | jq '.measures[] | {metric, last: .history[-1]}'

# Gate holatini pipeline ichida tekshirish (PR uchun)
curl -s -u "$SONAR_TOKEN:" \
  "$SONAR_URL/api/qualitygates/project_status?projectKey=warehouse-service&pullRequest=482" \
  | jq '.projectStatus.status, .projectStatus.conditions[] | select(.status=="ERROR")'
```

Yana bir foydali amaliyot: "ratchet" yondashuvi. Umumiy qoplanganlik uchun gate sharti qo'yilmaydi, lekin CI da oddiy tekshiruv bo'ladi: umumiy qoplanganlik oldingi qiymatdan pastga tushmasligi kerak. Bu talab bajarilishi oson, chunki yangi kod yaxshi qoplangan bo'lsa umumiy raqam o'zidan o'sadi.

Reytinglar haqida bitta aniqlik: umumiy koddagi reliability yoki security reytingi eng og'ir bitta issue bilan belgilanadi. Shuning uchun 200 ming qatorli legacy loyihada umumiy reyting deyarli har doim pastki harf bo'ladi va u jamoaning joriy ishi haqida hech narsa aytmaydi. Yangi kod reytingi esa aytadi. Tabloda ikkisi yonma-yon turishi kerak, lekin qaror faqat yangi kod ustunidan chiqadi.

New Code sozlamasini o'zgartirganda jamoaga oldin xabar bering. Chegara surilishi bilan tabloda issue soni keskin o'zgaradi va sababini bilmagan odam buni buzilish deb o'ylaydi.

## 7.11 Amalda qo'llash

- [ ] Har bir loyiha uchun New Code chegarasini reliz ritmiga qarab tanlab, global standartga tayanishni to'xtating.
- [ ] CI checkout bosqichida `fetch-depth: 0` qo'ying va `git rev-parse --is-shallow-repository` natijasi `false` ekanini tekshiring.
- [ ] Quality gate'dan umumiy kod shartlarini olib tashlab, hammasini `new_` metrikalariga o'tkazing va eski shartlarni kuzatuv paneliga ko'chiring.
- [ ] Repoga formatlashni bir marta qo'llash kerak bo'lsa, buni alohida commitda bajarib, hash'ini `.git-blame-ignore-revs` ga yozing va jamoaga ogohlantirish yuboring.
- [ ] `sonar.exclusions` va `sonar.coverage.exclusions` ro'yxatini ko'rib chiqib, generatsiya qilingan kod va DTO'larni chiqarib tashlang.
- [ ] Yangi kod coverage sharti 100 foiz bo'lsa uni 80 foizga tushiring va ustiga "assertion yo'q test qabul qilinmaydi" degan review qoidasini kiriting.
- [ ] Kichik PR'lar uchun absolut shart (qoplanmagan qatorlar soni) qo'shib, foizli shart kelib chiqaradigan noto'g'ri qizil holatlarni kamaytiring.
- [ ] Oylik hisobotga `coverage`, `new_coverage`, `violations`, `new_violations` trendini `api/measures/search_history` orqali avtomatik yig'ib qo'ying.

---

[&larr; 6. Quality gate mexanikasi va shartlari](06-quality-gate-mexanikasi-va-shartlari.md) · [Mundarija](README.md) · [8. 100% ga sozlangan gate: har bir shart nimani talab qiladi &rarr;](08-100-ga-sozlangan-gate-har-bir-shart-nimani.md)
