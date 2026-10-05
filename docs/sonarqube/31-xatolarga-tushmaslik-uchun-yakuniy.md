<!-- doc: sonarqube | chapter: 31 | part: VII. Xato katalogi: qanday kod qanday xato hisoblanadi -->

[Barcha hujjatlar](../../README.md) / [SonarQube](README.md)

# 31. Xatolarga tushmaslik uchun yakuniy tavsiyalar (Preventive Checklist)

<details>
<summary>Bu bobdagi 12 bo'lim</summary>

- [31.1 Kod yozishdan oldin: metod kichik, nom aniq, shart sodda bo'lsin degan odat](#311-kod-yozishdan-oldin-metod-kichik-nom-aniq-shart-sodda-bolsin-degan-odat)
- [31.2 Reliability toifasiga tushmaslik uchun kundalik qoidalar ro'yxati](#312-reliability-toifasiga-tushmaslik-uchun-kundalik-qoidalar-royxati)
- [31.3 Security toifasiga tushmaslik uchun kundalik qoidalar ro'yxati](#313-security-toifasiga-tushmaslik-uchun-kundalik-qoidalar-royxati)
- [31.4 Maintainability toifasiga tushmaslik uchun kundalik qoidalar ro'yxati](#314-maintainability-toifasiga-tushmaslik-uchun-kundalik-qoidalar-royxati)
- [31.5 Test yozishda doimo bajariladigan minimal to'plam](#315-test-yozishda-doimo-bajariladigan-minimal-toplam)
- [31.6 Commit qilishdan oldingi shaxsiy tekshiruv ro'yxati](#316-commit-qilishdan-oldingi-shaxsiy-tekshiruv-royxati)
- [31.7 Pull request ochishdan oldingi tekshiruv ro'yxati](#317-pull-request-ochishdan-oldingi-tekshiruv-royxati)
- [31.8 Jamoaviy kelishuv: nimani bloklash, nimani ogohlantirish darajasida qoldirish](#318-jamoaviy-kelishuv-nimani-bloklash-nimani-ogohlantirish-darajasida-qoldirish)
- [31.9 Yangi loyihani birinchi kundan toza boshlash uchun sozlamalar to'plami](#319-yangi-loyihani-birinchi-kundan-toza-boshlash-uchun-sozlamalar-toplami)
- [31.10 Eng ko'p uchraydigan o'nta xatoni oldini oluvchi o'nta odat](#3110-eng-kop-uchraydigan-onta-xatoni-oldini-oluvchi-onta-odat)
- [31.11 Sonar ni dushman emas, vosita sifatida ishlatish](#3111-sonar-ni-dushman-emas-vosita-sifatida-ishlatish)
- [31.12 Amalda qo'llash](#3112-amalda-qollash)

</details>



Bu hujjatning oxirgi bobi. Undan oldingi boblarda Sonar nimani qanday hisoblashini, qaysi qoida qachon ishga tushishini va quality gate shartlari qanday tekshirilishini ko'rdik. Shu bilimdan amaliy natija chiqarish vaqti keldi: quyida tushuntirish emas, qoida bor. Har bir band kundalik ishda bajariladigan harakat, uni jamoa kelishuvi yoki shaxsiy odat sifatida qabul qilish mumkin.

## 31.1 Kod yozishdan oldin: metod kichik, nom aniq, shart sodda bo'lsin degan odat

Sonar hisoblaydigan ko'pchilik metrika bitta sababdan o'sadi: metod o'z hajmidan kattalashib ketadi. Shuning uchun eng arzon profilaktika kod yozilgandan keyin emas, yozilishidan oldin boshlanadi. Uchta odat deyarli barcha maintainability shikoyatini kelib chiqishidan to'xtatadi.

Birinchi odat: metod bitta ish qilsin. Metod nomini aytganda "va" so'zi kerak bo'lsa, u ikkita metod. `validateAndSaveAndNotify` nomining o'zi cognitive complexity o'sishini oldindan e'lon qiladi.

Ikkinchi odat: nom izohni almashtirsin. `if (s == 2)` qatorini izoh bilan tushuntirish o'rniga `if (status == OrderStatus.PAID)` deb yozish kerak. Sonar sehrli sonlar va noaniq nomlar uchun alohida shikoyat qiladi, lekin asosiy foyda Sonar emas, o'qiydigan odam.

Uchinchi odat: shart yassi bo'lsin. Ichma-ich joylashgan `if` lar cognitive complexity ni ko'paytiradi, chunki o'quvchi bir vaqtda bir nechta shartni boshida ushlab turishi kerak. Yechim guard clause, ya'ni erta `return`.

```java
// Yomon: ichma-ich shartlar, cognitive complexity tez o'sadi
public BigDecimal hisobla(Order order) {
    if (order != null) {
        if (order.getItems() != null) {
            if (!order.getItems().isEmpty()) {
                return order.getItems().stream()
                    .map(OrderItem::getSum)
                    .reduce(BigDecimal.ZERO, BigDecimal::add);
            }
        }
    }
    return BigDecimal.ZERO;
}

// Sonar o'tadigan variant: guard clause bilan yassi tuzilma
public BigDecimal hisobla(Order order) {
    if (order == null) {
        return BigDecimal.ZERO;          // erta chiqish
    }
    List<OrderItem> items = order.getItems();
    if (items == null || items.isEmpty()) {
        return BigDecimal.ZERO;          // bo'sh holat ham erta chiqadi
    }
    return items.stream()
        .map(OrderItem::getSum)
        .reduce(BigDecimal.ZERO, BigDecimal::add);
}
```

Qoida sifatida: yangi metod yozganingizda IDE da uning qatorlarini sanang. Yigirma qatordan oshsa, ajratish uchun sabab izlang. Ellik qatordan oshsa, ajratmaslik uchun sabab izlang.

## 31.2 Reliability toifasiga tushmaslik uchun kundalik qoidalar ro'yxati

Reliability toifasi, ya'ni bug turidagi issue lar, kodning ishlamay qolishi ehtimolini bildiradi. Bu toifa quality gate da eng qattiq bloklanadigan toifa bo'lishi kerak, chunki uning narxi production da to'lanadi.

| Kundalik qoida | Nega shunday (Sonar nuqtai nazaridan) |
| --- | --- |
| `Optional` ni `get()` bilan ochmang, `orElseThrow` yoki `orElse` ishlatilsin | Sonar tekshirilmagan `get()` ni potensial exception manbasi deb belgilaydi |
| Tashqi manbadan kelgan obyektni ishlatishdan oldin null holati aniqlansin | Null ga murojaat qilish ehtimoli bor yo'l topilsa, bug ochiladi |
| `BigDecimal` ni `equals` bilan emas, `compareTo` bilan solishtiring | `equals` scale ni ham hisobga oladi, `2.0` va `2.00` teng chiqmaydi |
| `catch` bloki bo'sh qolmasin, hech bo'lmasa log yozilsin | Yutilgan exception xatoni yashiradi, bu alohida bug qoidasi |
| Resursni `try-with-resources` bilan oching | Yopilmagan stream va connection resurs oqishi deb baholanadi |
| Thread va vaqt bilan ishlaganda o'zgaruvchan umumiy holatdan voz kechilsin | Sinxronlanmagan umumiy holat Sonar uchun yuqori jiddiylikdagi bug |
| Shart ichida qiymat o'zgartirmang | Yon effektli shart tekshirib bo'lmaydigan kod hosil qiladi |
| `switch` da `default` yoki enum ning barcha holati qoplansin | Qoplanmagan holat kutilmagan oqimga olib keladi |
| Taqqoslashda har doim ma'lum qiymat chapda turmasin degan odatni tashlang, `Objects.equals` ishlatilsin | Ikki tomoni ham null bo'lishi mumkin bo'lgan taqqoslash xavfli |

Eng muhim amaliy maslahat: yangi bug issue paydo bo'lsa, uni "keyin" ro'yxatiga qo'shmang. Bug toifasidagi issue odatda bir necha qatorlik tuzatish, lekin bir hafta o'tgach uning konteksti esdan chiqadi.

## 31.3 Security toifasiga tushmaslik uchun kundalik qoidalar ro'yxati

Security toifasi ikkiga bo'linadi: vulnerability, ya'ni Sonar o'zi xavf deb hisoblagan kod, va security hotspot, ya'ni odam ko'rib qarorini aytishi kerak bo'lgan joy. Hotspot ni "xato" deb emas, "ko'rikdan o'tishi shart" deb qabul qilish kerak.

| Kundalik qoida | Nega shunday |
| --- | --- |
| SQL ni satr qo'shish bilan yasamang, parametr ishlatilsin | Satr konkatenatsiyasi SQL injection sifatida belgilanadi |
| Parol, token va kalit kodda turmasin, konfiguratsiya yoki secret store dan kelsin | Kodga yozilgan sir yuqori jiddiylikdagi vulnerability |
| Log ga foydalanuvchi kiritgan ma'lumotni tozalamasdan yozmang | Log injection va shaxsiy ma'lumot oqishi xavfi |
| Kriptografiyada zamonaviy algoritm va kuchli tasodif manbasi ishlatilsin | Eskirgan algoritm va `Random` xavfli deb baholanadi |
| Fayl yo'lini tashqi kiritmadan to'g'ridan to'g'ri yasamang | Path traversal xavfi hotspot sifatida ochiladi |
| Exception matnini foydalanuvchiga to'liq qaytarmang | Ichki tuzilma oshkor bo'lishi xavf deb hisoblanadi |
| Hotspot ni "safe" deb yopganda izoh yozilsin | Izohsiz yopilgan hotspot keyingi ko'rikda qayta ochiladi |
| Avtorizatsiya tekshiruvi kontrollerda emas, servis chegarasida bo'lsin | Chetlab o'tiladigan tekshiruv Sonar e'tiboridan tashqarida ham xavfli |

```sql
-- Yomon: satr qo'shish, Sonar SQL injection deb belgilaydi
-- "SELECT * FROM payments WHERE client_id = " + clientId

-- Sonar o'tadigan variant: nomli parametr
SELECT p.id, p.amount, p.status
FROM payments p
WHERE p.client_id = :clientId      -- parametr sifatida uzatiladi
  AND p.created_at >= :fromDate
ORDER BY p.created_at DESC;
```

Alohida eslatma: `@Query` ichida ham parametr ishlatilsin. JPQL satrini Java tomonida yig'ish Sonar uchun oddiy konkatenatsiya bilan bir xil darajada xavfli.

## 31.4 Maintainability toifasiga tushmaslik uchun kundalik qoidalar ro'yxati

Maintainability, ya'ni code smell, hujjatdagi issue larning aksariyatini tashkil qiladi. Bu toifa kodni buzmaydi, lekin keyingi o'zgarishning narxini oshiradi. Shuning uchun uni bloklash emas, chegara qo'yish orqali boshqarish to'g'ri.

| Kundalik qoida | Nega shunday |
| --- | --- |
| Cognitive complexity chegarasini metod darajasida kuzatib turing | Eng tez o'sadigan va eng ko'p shikoyat tug'diradigan metrika |
| Takrorlangan blokni uchinchi marta ko'rganda ajratib oling | Duplication foizi quality gate shartiga kiradi |
| Ishlatilmagan parametr, o'zgaruvchi va import darhol o'chirilsin | Arzon tuzatish, lekin issue soni sezilarli kamayadi |
| Sehrli son nomli konstantaga chiqarilsin | Nomsiz son ma'nosini yo'qotadi va xato manbasi bo'ladi |
| `TODO` va `FIXME` ga issue havolasi qo'shilsin yoki o'chirilsin | Izohsiz `TODO` doimiy smell sifatida qoladi |
| Izohga olingan kod saqlanmasin, git tarixi bor | Kommentdagi kod alohida qoida bilan belgilanadi |
| Metod parametri soni ettitadan oshmasin, obyektga yig'ilsin | Ko'p parametr chaqiruv joyida xatoga olib keladi |
| Deprecated API ishlatilganda almashtirish rejasi yozilsin | Eskirgan API keyingi versiya yangilashini bloklaydi |

## 31.5 Test yozishda doimo bajariladigan minimal to'plam

Test tafsilotlari [testlash qo'llanmasida](../testing/README.md) bor, bu yerda faqat Sonar o'lchoviga tegishli minimal to'plam. Sonar coverage ni o'zi hisoblamaydi, JaCoCo hisoblotini o'qiydi. Shuning uchun birinchi qoida: hisobot haqiqatan ham yaratilib, Sonar ga uzatilsin.

Har bir yangi public metod uchun minimal to'plam uchta testdan iborat. Birinchisi oddiy muvaffaqiyatli yo'l. Ikkinchisi chegara holati, ya'ni bo'sh ro'yxat, nol qiymat, eng katta qiymat. Uchinchisi xato yo'li, ya'ni exception yoki rad etilgan natija.

```java
// Minimal to'plam: muvaffaqiyat, chegara, xato
@Test
void toliq_tolov_statusni_PAID_ga_otkazadi() {
    Order order = order(BigDecimal.valueOf(100));
    PaymentResult natija = service.pay(order, BigDecimal.valueOf(100));
    assertThat(natija.status()).isEqualTo(OrderStatus.PAID);
}

@Test
void nol_summa_rad_etiladi() {                 // chegara holati
    Order order = order(BigDecimal.valueOf(100));
    assertThatThrownBy(() -> service.pay(order, BigDecimal.ZERO))
        .isInstanceOf(InvalidAmountException.class);
}

@Test
void qoldiq_yetmasa_xato_qaytaradi() {         // xato yo'li
    Order order = order(BigDecimal.valueOf(100));
    assertThatThrownBy(() -> service.pay(order, BigDecimal.valueOf(40)))
        .isInstanceOf(PartialPaymentException.class)
        .hasMessageContaining("qoldiq");
}
```

Ikkinchi qoida: assertion bo'lmagan test yozmang. Sonar assertion siz test metodini alohida belgilaydi, va bu to'g'ri, chunki bunday test faqat coverage raqamini ko'taradi. Uchinchi qoida: `@Disabled` testni uzoq saqlamang. O'chirilgan test ham smell, ham yolg'on xotirjamlik.

To'rtinchi qoida: shartli tarmoqni test qilgan bo'lsangiz, natijani ham tekshiring. Metod chaqirilgani coverage uchun yetarli, lekin xatoni ushlash uchun yetarli emas. Aynan shu joyda 100% coverage aldaydi: barcha qator qoplangan bo'lishi mumkin, lekin hech bir natija tekshirilmagan.

## 31.6 Commit qilishdan oldingi shaxsiy tekshiruv ro'yxati

Commit oldidagi tekshiruv ikki daqiqa oladi va PR dagi munozarani sezilarli qisqartiradi. Eng foydali qadam, lokal tahlilni ishga tushirish, ya'ni serverga yubormasdan natijani ko'rish.

```bash
# 1. Formatlash va kompilyatsiya
./mvnw -q clean verify -DskipITs

# 2. JaCoCo hisoboti yaratilganini tekshirish
test -f target/site/jacoco/jacoco.xml && echo "coverage hisoboti bor"

# 3. Faqat o'zgargan kodni ko'rish, ortiqcha narsa kirmaganiga ishonch
git diff --stat
git diff --cached

# 4. Lokal Sonar tahlili (server manzili va token muhit o'zgaruvchisida)
./mvnw -q sonar:sonar -Dsonar.host.url="$SONAR_HOST" \
  -Dsonar.token="$SONAR_TOKEN"
```

Shaxsiy ro'yxat quyidagicha: yangi sehrli son yo'q, yangi `System.out` yo'q, yangi bo'sh `catch` yo'q, yangi `TODO` havolasiz emas, debug uchun qo'yilgan vaqtinchalik kod olib tashlangan, test nomi nimani tekshirayotganini aytadi.

## 31.7 Pull request ochishdan oldingi tekshiruv ro'yxati

PR darajasida asosiy savol boshqa: bu o'zgarish quality gate ni o'tadimi va ko'rikchi uni tushunadimi. Sonar PR tahlilida odatda faqat yangi kod baholanadi, shuning uchun PR ni kichik ushlash eng samarali vosita.

Birinchi band: PR bitta mavzuga tegishli bo'lsin. Refaktoring va yangi funksiya bitta PR da aralashsa, Sonar natijasini ham, ko'rikni ham o'qish qiyinlashadi.

Ikkinchi band: PR tavsifida nima o'zgarganini va nega o'zgarganini yozing. Uchinchi band: agar quality gate yangi kod coverage sababli qizil bo'lsa, test qo'shing yoki coverage dan chiqarilishi kerak bo'lgan kodni to'g'ri belgilang. To'rtinchi band: hotspot paydo bo'lsa, uni PR da izohlab bering, ko'rikchi qaroringizni ko'rishi kerak.

| Tuzoq | Yechim |
| --- | --- |
| PR katta, Sonar yuzlab issue ko'rsatadi | PR ni mavzuga bo'lib yuboring, har biri alohida ko'rikdan o'tsin |
| Yangi kod coverage past, chunki getter va DTO sanaladi | Yaratilgan va oddiy kodni tahlildan chiqarish qoidasini loyihada bir marta sozlang |
| Gate qizil, lekin sabab eski kodda | Yangi kod shartlariga tayanadigan gate ni tanlang, eski qarzni alohida reja bilan yoping |
| Hotspot har PR da qayta ochiladi | Yopishda sabab yozilsin, izohsiz yopish keyin bekor qiladi |
| Coverage hisoboti yo'q, Sonar nolni ko'rsatadi | Hisobot yo'li konfiguratsiyada aniq ko'rsatilsin, CI da fayl mavjudligi tekshirilsin |
| Test kodi o'zi issue to'playdi | Test uchun alohida profil va alohida chegara kelishilsin |
| Tahlil sekun, ishlab chiquvchi kutadi | Tahlilni alohida qadamga chiqaring, keshni saqlang |
| Issue "false positive" deb ko'p yopiladi | Qoidani profil darajasida muhokama qiling, har joyda alohida yopish emas |

## 31.8 Jamoaviy kelishuv: nimani bloklash, nimani ogohlantirish darajasida qoldirish

Eng ko'p uchraydigan boshqaruv xatosi, hammasini bloklash. Natijada jamoa gate ni chetlab o'tish yo'lini izlaydi. To'g'ri yondashuv darajalarni ajratishdir: ba'zi narsa merge ni to'xtatadi, ba'zisi faqat ko'rinadi.

Bloklash uchun nomzodlar: yangi kodda bug toifasidagi issue, yangi kodda vulnerability, ko'rikdan o'tmagan security hotspot, yangi kod coverage belgilangan foizdan past, yangi kodda duplication belgilangan foizdan yuqori.

Ogohlantirish uchun nomzodlar: maintainability issue lar umumiy soni, eski koddagi technical debt, past jiddiylikdagi uslub shikoyatlari, metod uzunligi bo'yicha chegaradan ozgina oshish.

| Mavzu | Oddiy yondashuv | Arxitektor yondashuvi |
| --- | --- | --- |
| Quality gate shartlari | Hammasini qizil qilish, keyin chetlab o'tish | Yangi kodga qattiq, eski kodga reja bilan yondashish |
| Coverage | Butun loyiha uchun bitta katta foiz talab qilish | Yangi kod coverage va shartli tarmoq sifatiga qarash |
| Yangi qoida qo'shish | Darhol bloklovchi qilib yoqish | Avval ogohlantirish, statistikani ko'rib keyin bloklash |
| False positive | Har joyda alohida yopish | Profil darajasida qoidani muhokama qilib sozlash |
| Technical debt | Katta refaktoring sprinti rejalashtirish | Tegilgan faylni tozalash qoidasi, bosqichma bosqich |
| Sonar vaqti | Har commit da to'liq tahlil | PR da yangi kod tahlili, asosiy branch da to'liq tahlil |
| Hotspot | Hammasini "safe" deb yopish | Har birini izohlab, qarorni tarixda saqlash |
| Test kodi tahlili | Umuman tahlildan chiqarish | Alohida profil, assertion va duplication qoidalari saqlanadi |
| Issue mas'uliyati | Kimdir keyin tuzatadi | Issue muallifi, ya'ni PR egasi tuzatadi |
| Natijani o'qish | Faqat yashil yoki qizil rangga qarash | Trendga qarash, issue zichligi kamayayotganini kuzatish |

Kelishuvni og'zaki emas, yozma qiling. Repozitoriyadagi qisqa hujjat, ya'ni "bizda nima bloklanadi" ro'yxati, har yangi a'zoga vaqt tejaydi.

## 31.9 Yangi loyihani birinchi kundan toza boshlash uchun sozlamalar to'plami

Yangi loyihada eng katta imkoniyat shu: hali qarz yo'q. Birinchi kunda sozlangan uchta narsa keyinchalik oylab vaqt tejaydi.

Birinchisi, loyiha kaliti va manba kodlash. Ikkinchisi, coverage hisoboti yo'li. Uchinchisi, tahlildan chiqariladigan yaratilgan kod.

```properties
# sonar-project.properties yoki pom.xml xossalari
sonar.projectKey=ombor-servisi
sonar.projectName=Ombor servisi
sonar.sourceEncoding=UTF-8
sonar.java.source=21

# Coverage hisoboti yo'li: JaCoCo XML, aggregate modul uchun ham
sonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml

# Yaratilgan va tahlilga aloqasi yo'q kodni chiqarish
sonar.exclusions=**/generated/**,**/dto/**Mapper*.java
sonar.coverage.exclusions=**/config/**,**/*Application.java
```

Maven tomonida JaCoCo ni to'g'ri bog'lash muhim: `prepare-agent` test fazasidan oldin, `report` esa `verify` dan oldin ishlashi kerak. Aks holda hisobot bo'sh bo'ladi va Sonar coverage ni nol deb ko'rsatadi.

```xml
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <version>0.8.12</version>
  <executions>
    <execution>
      <id>agent</id>
      <goals><goal>prepare-agent</goal></goals>
    </execution>
    <execution>
      <id>report</id>
      <phase>verify</phase>              <!-- hisobot verify da yaratiladi -->
      <goals><goal>report</goal></goals>
    </execution>
  </executions>
</plugin>
```

CI tomonida tahlilni alohida qadam qiling va gate natijasini kuting. Kutmasangiz, qizil gate merge ni to'xtatmaydi.

```yaml
# CI da tahlil va gate natijasini kutish
- name: Test va coverage
  run: ./mvnw -B clean verify

- name: Sonar tahlili
  env:
    SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
  run: >
    ./mvnw -B sonar:sonar
    -Dsonar.projectKey=ombor-servisi
    -Dsonar.qualitygate.wait=true      # gate natijasi kutiladi
```

Shuni ham eslatib o'tish kerak: `sonar.qualitygate.wait` xulq-atvori va mavjudligi versiyaga qarab farq qiladi, shuning uchun o'z serveringiz versiyasi hujjatida tasdiqlang.

## 31.10 Eng ko'p uchraydigan o'nta xatoni oldini oluvchi o'nta odat

Birinchi odat: metodni yozib bo'lgach, uning eng chuqur `if` darajasini sanash. Ikkinchi odat: `Optional` qaytargan metodni chaqirganda darhol natija yo'q holatini hal qilish. Uchinchi odat: pul miqdorini faqat `BigDecimal` da saqlash va `compareTo` bilan solishtirish.

To'rtinchi odat: har bir `catch` ichida nima bo'layotganini bir qatorda tushuntirish. Beshinchi odat: SQL va JPQL ni hech qachon satr qo'shish bilan yasamaslik. Oltinchi odat: sirni konfiguratsiyadan olish, kodga yozmaslik.

Yettinchi odat: uchinchi takrorlanishda umumiy metod ajratish. Sakkizinchi odat: yangi test yozganda assertion ni testdan oldin o'ylab qo'yish. To'qqizinchi odat: `TODO` yozganda unga issue raqami qo'shish. O'ninchi odat: PR ni yuborishdan oldin o'z diff ini boshqa odam ko'zi bilan bir marta o'qish.

Bu o'nta odatning hammasi birgalikda kuniga besh daqiqa vaqt oladi. Ularning o'rnini bosadigan vosita yo'q, chunki Sonar xatoni topadi, lekin odatni yarata olmaydi.

## 31.11 Sonar ni dushman emas, vosita sifatida ishlatish

Sonar ni dushman sifatida ko'rish ikki ko'rinishda bo'ladi. Birinchisi, raqamni ko'tarish uchun mazmunsiz test yozish. Ikkinchisi, issue ni tuzatish o'rniga qoidani o'chirish. Ikkalasi ham o'lchovni buzadi, muammoni esa joyida qoldiradi.

Vosita sifatida ishlatish boshqacha ko'rinadi. Issue ro'yxati vazifa ro'yxati emas, balki signal. Agar bitta modulda cognitive complexity doim oshsa, bu modulning mas'uliyati noto'g'ri taqsimlangan degani. Agar duplication bir nechta servis o'rtasida takrorlansa, umumiy kutubxona yoki umumiy abstraksiya kerak degani. Sonar bu xulosani aytmaydi, lekin uni ko'rishga yetarli ma'lumot beradi.

Shuni ham ochiq aytish kerak: yashil quality gate kodning to'g'riligini kafolatlamaydi. U faqat belgilangan shartlar bajarilganini aytadi. Mantiq xatosi, noto'g'ri talab va yomon arxitektura yashil gate bilan ham mavjud bo'la oladi. Shuning uchun Sonar ko'rikni almashtirmaydi, uni arzonlashtiradi: ko'rikchi uslub va aniq xatolar bilan emas, mantiq va qaror bilan shug'ullanadi.

Oxirgi fikr: o'lchovni maqsadga aylantirmang. Maqsad, o'zgartirish oson va buzilishi qiyin kod. Sonar shu maqsadga qanchalik yaqinlashayotganingizni ko'rsatadigan asboblar panelidan biri.

## 31.12 Amalda qo'llash

- [ ] Jamoada bitta sahifali kelishuv yozing: nima merge ni bloklaydi, nima faqat ogohlantiradi.
- [ ] Yangi loyihada birinchi kuni `sonar.coverage.jacoco.xmlReportPaths` va exclusions qiymatlarini sozlang.
- [ ] CI da tahlil qadamini qo'shib, gate natijasini kutishni yoqing va qizil gate da merge to'xtashini tekshirib ko'ring.
- [ ] Commit oldidan ishlatiladigan shaxsiy tekshiruv ro'yxatini repozitoriyaga qo'ying va bir hafta amal qilib ko'ring.
- [ ] Bitta eng ko'p shikoyat to'playdigan modulni tanlab, undagi uchta eng yuqori cognitive complexity metodini ajratib yozing.
- [ ] Barcha ochiq security hotspot larni ko'rib chiqing va har biriga qarorni izoh bilan yozing.
- [ ] Assertion siz va `@Disabled` holatidagi testlarni toping, har biriga qaror qabul qiling: to'ldirish yoki o'chirish.
- [ ] Oylik bir marta trendga qarang: yangi kod issue zichligi kamayayotganini yoki o'sayotganini yozib boring.

---

[&larr; 30. Xato katalogi: test kodidagi xatolar](30-xato-katalogi-test-kodidagi-xatolar.md) · [Mundarija](README.md) · [32. SonarQube nashrlari va ularning farqi &rarr;](32-sonarqube-nashrlari-va-ularning-farqi.md)
