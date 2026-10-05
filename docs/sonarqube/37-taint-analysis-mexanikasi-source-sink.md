<!-- doc: sonarqube | chapter: 37 | part: IX. Kengaytirish va integratsiya -->

[Barcha hujjatlar](../../README.md) / [SonarQube](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 37. Taint analysis mexanikasi: source, sink, sanitizer (Taint Analysis Mechanics)

<details>
<summary>Bu bobdagi 13 bo'lim</summary>

- [37.1 Oddiy qoida va taint analysis farqi: bitta fayl va butun oqim](#371-oddiy-qoida-va-taint-analysis-farqi-bitta-fayl-va-butun-oqim)
- [37.2 Source nima: ishonchsiz ma'lumot kiradigan nuqtalar](#372-source-nima-ishonchsiz-malumot-kiradigan-nuqtalar)
- [37.3 Sink nima: ma'lumot xavfli joyga yetib boradigan nuqtalar](#373-sink-nima-malumot-xavfli-joyga-yetib-boradigan-nuqtalar)
- [37.4 Sanitizer va validator: oqimni to'xtatuvchi nuqtalar](#374-sanitizer-va-validator-oqimni-toxtatuvchi-nuqtalar)
- [37.5 Zanjir qanday quriladi: controller dan repository gacha misol](#375-zanjir-qanday-quriladi-controller-dan-repository-gacha-misol)
- [37.6 Nega taint analysis sekinroq va ko'proq resurs talab qiladi](#376-nega-taint-analysis-sekinroq-va-koproq-resurs-talab-qiladi)
- [37.7 Qaysi nashrda mavjud va Community nashrda nima qilish mumkin](#377-qaysi-nashrda-mavjud-va-community-nashrda-nima-qilish-mumkin)
- [37.8 Taint natijasini o'qish: Sonar ko'rsatadigan oqim qadamlari](#378-taint-natijasini-oqish-sonar-korsatadigan-oqim-qadamlari)
- [37.9 False positive sabablari: o'z validatoringizni Sonar tanimasligi](#379-false-positive-sabablari-oz-validatoringizni-sonar-tanimasligi)
- [37.10 Zanjirni uzish usullari: tur orqali, validatsiya orqali, repozitoriy chegarasida](#3710-zanjirni-uzish-usullari-tur-orqali-validatsiya-orqali-repozitoriy-chegarasida)
- [37.11 Spring loyihasida tipik oqimlar: so'rov parametri, header, fayl nomi, SQL](#3711-spring-loyihasida-tipik-oqimlar-sorov-parametri-header-fayl-nomi-sql)
- [37.12 Taint natijasini jamoada kim ko'rib chiqishi](#3712-taint-natijasini-jamoada-kim-korib-chiqishi)
- [37.13 Amalda qo'llash](#3713-amalda-qollash)

</details>



Sonar qoidalarining kattaroq qismi bitta metod yoki bitta fayl ichida qaror qabul qiladi. Xavfsizlik qoidalarining eng qimmatli qismi esa boshqacha ishlaydi: u ma'lumotning kirish nuqtasidan xavfli chaqiruvgacha bo'lgan butun yo'lini kuzatadi. Bu mexanizm taint analysis deb ataladi va uning uchta asosiy tushunchasi bor: source, sink va sanitizer. Bu bobda shu uch tushuncha qanday ishlashini, zanjir qanday qurilishini, natijani qanday o'qishni va qaysi nashrda bu imkoniyat borligini ko'rib chiqamiz.

## 37.1 Oddiy qoida va taint analysis farqi: bitta fayl va butun oqim

Oddiy qoida sintaktik daraxt va bitta metod doirasidagi oqim bilan ishlaydi. Masalan `null` tekshiruvi yoki kognitiv murakkablik hisobi uchun Sonar metoddan tashqariga chiqishi shart emas. Bunday tahlil arzon, tez va deyarli har doim aniq javob beradi.

Taint analysis boshqa masalani hal qiladi. U so'raydi: bu qiymat foydalanuvchidan keldimi, va u qayerga yetib bordi. Javob uchun metod chegarasidan oshib o'tish kerak, chunki controller qiymatni service ga, service repository ga uzatadi. Shuning uchun bu tahlil interprocedural, ya'ni bir nechta metod va bir nechta fayl bo'ylab ishlaydi.

Farqning amaliy natijasi shu: oddiy qoida buzilishini kod ko'rinishidan topish mumkin, taint issue esa faqat butun chaqiruv zanjirini ko'rib tushuniladi. Shuning uchun taint natijasini bitta qatorga qarab "bu yerda hammasi joyida" deb yopib tashlash eng ko'p uchraydigan xato.

## 37.2 Source nima: ishonchsiz ma'lumot kiradigan nuqtalar

Source bu dasturga tashqaridan nazoratsiz ma'lumot kiradigan joy. Sonar uchun source ro'yxati oldindan belgilangan va u freymvorkni biladi. Spring loyihasida eng tipik source lar quyidagilar.

`@RequestParam`, `@PathVariable`, `@RequestHeader`, `@CookieValue` bilan belgilangan metod argumentlari. `@RequestBody` orqali kelgan DTO ning maydonlari. `HttpServletRequest` dan o'qilgan parametr va header. `MultipartFile` ning `getOriginalFilename()` natijasi. Shuningdek message broker dan kelgan payload, tashqi HTTP javobi va ba'zi hollarda muhit o'zgaruvchilari ham source sifatida qaraladi.

Muhim nuqta: source bo'lishning o'zi muammo emas. Dastur tashqi ma'lumot qabul qilishi normal holat. Issue faqat o'sha ma'lumot sanitizatsiyasiz sink ga yetib borsa paydo bo'ladi. Shuning uchun controller dagi `@RequestParam` ustida hech qachon "bu xavfli" degan belgi turmaydi.

Amalda source ro'yxatini bilish diagnostika uchun kerak. Agar siz oqim qadamlarining birinchisini ko'rsangiz, Sonar sizga aynan qaysi kirish nuqtasini ishonchsiz deb hisoblaganini aytadi. Agar o'sha nuqta sizning arxitekturangizda allaqachon gateway darajasida tekshirilgan bo'lsa, buni Sonar bilmaydi va buni ayta olmaydi.

## 37.3 Sink nima: ma'lumot xavfli joyga yetib boradigan nuqtalar

Sink bu ishonchsiz qiymat zarar keltira oladigan chaqiruv. Har bir taint qoidasi aslida bitta source toifasi va bitta sink toifasi juftligi.

Java uchun ishonchim komil bo'lgan taint qoidalari va ularning sink lari quyidagicha. `java:S3649` SQL so'rovi qurilishini kuzatadi, sink bu konkatenatsiya bilan yasalgan native query yoki JDBC `Statement`. `java:S2076` OS buyrug'i chaqiruvini kuzatadi, sink bu `Runtime.exec` yoki `ProcessBuilder`. `java:S2083` fayl yo'li qurilishini kuzatadi, sink bu `new File(...)` yoki `Paths.get(...)`. `java:S5131` javobga yozilgan qiymatni kuzatadi, sink bu HTTP response ga eskaplanmagan matn chiqarish. `java:S5146` qayta yo'naltirishni kuzatadi, sink bu `sendRedirect` yoki `redirect:` prefiksi bilan qaytarilgan view nomi.

Bu ro'yxat to'liq emas va versiya bilan kengayadi. Shuning uchun amaliy tavsiya: sink ro'yxatini yodlab olish emas, balki o'z loyihangizdagi xavfli chaqiruvlarni bitta joyga yig'ish. Agar SQL faqat repository qatlamida yozilsa, fayl yo'li faqat bitta storage komponentida qurilsa, barcha taint oqimlari shu tor darvozadan o'tadi va ularni bir marta himoyalash yetarli bo'ladi.

## 37.4 Sanitizer va validator: oqimni to'xtatuvchi nuqtalar

Sanitizer bu Sonar "shu nuqtadan keyin qiymat xavfsiz" deb hisoblaydigan amal. Agar oqim yo'lida sanitizer bo'lsa, zanjir uziladi va issue yaratilmaydi.

Sonar bir nechta xil to'xtatuvchini taniydi. Birinchisi tur o'zgarishi: `Integer.parseInt`, `Long.valueOf`, `UUID.fromString` yoki `enum` ga aylantirish natijasi endi ixtiyoriy matn emas. Ikkinchisi bog'lanish mexanizmi: `PreparedStatement` parametri yoki JPA ning nomlangan parametri qiymatni so'rov matniga qo'shmaydi, shuning uchun SQL injection zanjiri shu yerda tugaydi. Uchinchisi ma'lum eskaplash va tozalash kutubxonalari, masalan OWASP encoder yoki HTML sanitizer.

Validatsiya esa murakkabroq holat. Agar siz qiymatni oq ro'yxat bilan tekshirib, mos kelmasa exception tashlasangiz, odam uchun bu yetarli dalil. Sonar buni faqat tekshiruv uning modeliga mos tushganda tan oladi. `equals` yoki `contains` bilan oq ro'yxatga solishtirish ko'p holatda tan olinadi, murakkab regex yoki boshqa klassdagi yordamchi metod esa ko'pincha tan olinmaydi.

## 37.5 Zanjir qanday quriladi: controller dan repository gacha misol

Quyida zaif zanjir. Oqim `@RequestParam` dan boshlanib, uch qatlam orqali native query ga yetib boradi.

```java
// 1-qadam: source. Sonar bu argumentni ishonchsiz deb belgilaydi.
@GetMapping("/hisobot")
public List<OrderRow> report(@RequestParam String sort) {
    return reportService.load(sort);
}

// 2-qadam: qiymat o'zgarmasdan keyingi qatlamga uzatiladi.
public List<OrderRow> load(String sort) {
    return reportRepository.findSorted(sort);
}

// 3-qadam: sink. Matn to'g'ridan to'g'ri so'rovga qo'shilgan.
public List<OrderRow> findSorted(String sort) {
    String sql = "select id, total from orders order by " + sort;
    return jdbcTemplate.query(sql, ROW_MAPPER);
}
```

Sonar bu holatda SQL injection oqimini ko'rsatadi, chunki source dan sink gacha hech qanday to'xtatuvchi yo'q. Endi uzilgan zanjir. Bu yerda matn umuman so'rovga yetib bormaydi, chunki u `enum` ga aylantirilgan.

```java
public enum OrderSort {
    ID("id"), TOTAL("total");
    private final String column;
    OrderSort(String column) { this.column = column; }
    public String column() { return column; }
}

@GetMapping("/hisobot")
public List<OrderRow> report(@RequestParam OrderSort sort) {
    // Spring noto'g'ri qiymatda 400 qaytaradi, service ga faqat enum keladi.
    return reportService.load(sort);
}

public List<OrderRow> findSorted(OrderSort sort) {
    // Sink ga faqat enum ichidagi oldindan belgilangan ustun nomi boradi.
    String sql = "select id, total from orders order by " + sort.column();
    return jdbcTemplate.query(sql, ROW_MAPPER);
}
```

Ikkinchi variantda zanjir ikki joyda uziladi: tur o'zgarishi va qiymatning oldindan belgilangan ro'yxatdan kelishi. Shuning uchun bu kod Sonar uchun ham, auditor uchun ham ishonchli.

## 37.6 Nega taint analysis sekinroq va ko'proq resurs talab qiladi

Oddiy qoida bitta metodni bir marta ko'rib chiqadi. Taint analysis esa chaqiruv grafini qurib, qiymatning mumkin bo'lgan barcha yo'llarini hisoblaydi. Yo'llar soni qatlamlar va shartlar soni bilan tez o'sadi, shuning uchun tahlil vaqti va xotira sarfi ham o'sadi.

Amaliy ko'rinishi shu: `mvn verify sonar:sonar` bosqichi katta monolitda bir necha daqiqadan o'nlab daqiqaga cho'zilishi mumkin, va skanner `OutOfMemoryError` bilan tushishi mumkin. Birinchi yechim xotira berish.

```bash
# Skanner JVM ga xotira berish. Aniq qiymat loyiha hajmiga qarab tanlanadi.
export SONAR_SCANNER_JAVA_OPTS="-Xmx4g"

# Tahlilni alohida bosqichda yurgizish, test bosqichidan keyin.
./mvnw -B clean verify
./mvnw -B sonar:sonar -Dsonar.projectKey=payments-api
```

Ikkinchi yechim tahlil doirasini tozalash. Generatsiya qilingan kod va migratsiya skriptlarini chiqarib tashlash tahlil vaqtini sezilarli qisqartiradi.

```properties
# sonar-project.properties yoki pom.xml dagi xossalar
sonar.sources=src/main/java
sonar.tests=src/test/java
# Generatsiya qilingan kodni tahlildan chiqarish.
sonar.exclusions=**/generated/**,**/target/**,**/*MapperImpl.java
# Coverage hisobotining joyi. Taint uchun emas, lekin bir joyda turadi.
sonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml
```

CI da taint tahlilini har bir push da emas, pull request va asosiy branch da yurgizish ham keng tarqalgan murosa.

```yaml
# .github/workflows/sonar.yml dagi tahlil bosqichi
name: sonar
on:
  pull_request:
  push:
    branches: [ main ]
jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0   # yangi kod hisobi uchun tarix kerak
      - uses: actions/setup-java@v4
        with:
          java-version: '21'
          distribution: temurin
      - name: Tahlil
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_SCANNER_JAVA_OPTS: -Xmx4g
        run: ./mvnw -B clean verify sonar:sonar
```

## 37.7 Qaysi nashrda mavjud va Community nashrda nima qilish mumkin

Bu eng muhim halol gap: taint analysis SonarQube ning Community nashrida yo'q. U Developer Edition va yuqori nashrlarda, shuningdek SonarCloud ning mos rejalarida ishlaydi. Shuning uchun injection toifasidagi qoidalar Community nashrda hech qachon ishga tushmaydi, hatto profilda yoqilgan ko'rinsa ham natija bermaydi.

Buning tashkiliy natijasi bor. Agar sizda Community nashr bo'lsa, SQL injection, path traversal va reflected XSS kabi muammolarni Sonar topib bermaydi. Bu "bizda bu muammolar yo'q" degani emas, "bizda bu tahlil yo'q" degani.

Community nashrda qolgan vositalar. Birinchisi security hotspot qoidalari, ular bitta fayl doirasida ishlaydi va xavfli chaqiruvni odam ko'rib chiqishi uchun belgilaydi. Ikkinchisi oddiy qoidalar, masalan `PreparedStatement` o'rniga konkatenatsiya ishlatilganini bevosita ko'rsatadigan tekshiruvlar. Uchinchisi arxitektura orqali himoya: SQL ni faqat bitta qatlamda yozish va bunga ArchUnit testi bilan majburlash, bu usul [testlash qo'llanmasidagi](../testing/README.md) ArchUnit mavzusida batafsil yoritilgan. To'rtinchisi tashqi vositalar, masalan OWASP dependency tekshiruvi.

## 37.8 Taint natijasini o'qish: Sonar ko'rsatadigan oqim qadamlari

Taint issue ni ochganda Sonar bitta qator emas, qadamlar ketma-ketligini ko'rsatadi. Birinchi qadam source, oxirgi qadam sink, oradagi qadamlar qiymatning uzatilish nuqtalari.

O'qish tartibi quyidagicha bo'lishi kerak. Avval oxirgi qadamga qarang va sink haqiqatan xavflimi deb so'rang. Keyin birinchi qadamga qarang va qiymat haqiqatan tashqaridan keladimi deb tekshiring. Shundan keyingina orada to'xtatuvchi bor yo'qligini ko'rib chiqing.

Ko'p jamoa xatosi shu: oqimning o'rtasidagi bitta qatorga qarab "bu metod ichida hech narsa yo'q" deb issue ni yopadi. Taint natijasida o'rta qadamlar odatda butunlay begunoh ko'rinadi, chunki ular shunchaki argumentni uzatadi.

Agar oqim haqiqatan yolg'on bo'lsa, uni issue sifatida "false positive" belgisi bilan yopish mumkin, lekin izoh yozish shart. Izohda nima uchun yolg'on ekani ko'rsatilsin, masalan qiymat gateway darajasida enum ga aylantirilgani. Izohsiz yopilgan xavfsizlik issue si keyingi auditda qayta ochiladi.

## 37.9 False positive sabablari: o'z validatoringizni Sonar tanimasligi

Eng ko'p uchraydigan sabab shu: siz validatsiyani o'z utilita klassingizda yozgansiz va Sonar uni sanitizer deb bilmaydi. Sonar faqat o'zi taniydigan to'xtatuvchilar ro'yxati bilan ishlaydi, sizning `SecurityUtils.checkColumn` metodingiz u ro'yxatda yo'q.

| Tuzoq | Nega yuzaga keladi | Yechim |
| --- | --- | --- |
| O'z validator metodi tan olinmaydi | Sonar modelida bu metod sanitizer emas | Tur o'zgarishi yoki oq ro'yxatdan qaytarilgan konstanta ishlatish |
| Regex bilan tekshirish yetarli deb o'ylash | Murakkab regex semantikasi hisoblanmaydi | Qiymatni emas, uning indeksini yoki enum ni uzatish |
| `@Valid` annotatsiyasi zanjirni uzadi deb o'ylash | Bean validation qiymatni o'zgartirmaydi | Validatsiyadan keyin tur xavfsiz obyektga map qilish |
| Issue izohsiz yopiladi | Keyingi analizda qayta ochiladi | Yopish izohida dalilni yozish |
| Butun fayl exclusion ga tushadi | Kelajakdagi haqiqiy muammolar ham yashiriladi | Exclusion emas, nuqtaviy suppress ishlatish |
| Sink ko'p joyda takrorlanadi | Har bir joyda alohida tekshiruv kerak bo'ladi | Sink ni bitta adapter klassga yig'ish |
| DTO maydoni butunlay ishonchsiz sanaladi | `@RequestBody` ichidagi barcha maydon source | Domen obyektiga o'tishda aniq konvertatsiya qilish |

Nuqtaviy bostirish kerak bo'lsa, qoida kaliti bilan yozing va yonida izoh qoldiring.

```java
public class ReportExport {

    // Ustun nomi faqat shu klass ichidagi konstantalardan keladi,
    // tashqi kirish yo'q. Shuning uchun oqim amalda uzilgan.
    @SuppressWarnings("java:S3649")
    public String buildOrderBy(ReportColumn column) {
        return "order by " + column.sqlName();
    }
}
```

Developer Edition da taint tahlilining o'z konfiguratsiyasini JSON fayl orqali kengaytirish, ya'ni o'z sanitizeringizni e'lon qilish imkoniyati bor. Konfiguratsiya xossasining aniq nomi va formati versiyaga qarab farq qiladi, shuning uchun uni o'z serveringiz versiyasining hujjatidan tekshiring. Men bu yerda xossa nomini aniq yozmayman, chunki yanglish nom butun sozlamani ishlamaydigan qiladi.

## 37.10 Zanjirni uzish usullari: tur orqali, validatsiya orqali, repozitoriy chegarasida

Birinchi usul eng ishonchli: turni o'zgartirish. Matnni `enum`, `long`, `UUID` yoki `LocalDate` ga aylantirsangiz, qiymatning erkinligi yo'qoladi. Bu usul Sonar uchun ham tushunarli, odam uchun ham dalil.

Ikkinchi usul validatsiya, lekin natijani qaytarish shaklida. Tekshirib `true` qaytargan metod zanjirni uzmaydi, chunki keyin yana o'sha ishonchsiz matn ishlatiladi. Tekshirib oq ro'yxatdagi konstantani qaytargan metod esa zanjirni uzadi, chunki sink ga sizning konstantangiz boradi.

Uchinchi usul repozitoriy chegarasida bog'lanish. SQL ni parametr bilan yozsangiz, qiymat so'rov matniga umuman qo'shilmaydi.

```sql
-- Zaif: qiymat so'rov matniga konkatenatsiya qilinadi.
-- select * from orders where customer_code = '<foydalanuvchi matni>'

-- Xavfsiz: qiymat parametr sifatida uzatiladi, so'rov matni o'zgarmaydi.
select id, total, status
from orders
where customer_code = ?
  and created_at >= ?
order by created_at desc
limit 100;
```

Spring Data tomonida xuddi shu printsip nomlangan parametr bilan ifodalanadi. Dinamik `order by` kerak bo'lsa, ustun nomini matn sifatida emas, `Sort` obyekti yoki oldindan belgilangan ro'yxat orqali bering.

```java
public interface OrderRepository extends Repository<Order, Long> {

    // Qiymat parametr sifatida bog'lanadi, so'rov matni statik.
    @Query("select o from Order o where o.customerCode = :code and o.total >= :min")
    List<Order> findByCustomer(@Param("code") String code,
                               @Param("min") BigDecimal min);
}

@Service
public class OrderQueryService {

    private static final Set<String> ALLOWED = Set.of("createdAt", "total");

    public Sort toSort(String raw) {
        // Oq ro'yxatdagi konstanta qaytariladi, foydalanuvchi matni emas.
        String column = ALLOWED.contains(raw) ? raw : "createdAt";
        return Sort.by(Sort.Direction.DESC, column);
    }
}
```

| Savol | Oddiy yondashuv | Arxitektor yondashuvi |
| --- | --- | --- |
| Taint issue kelganda | Qatorga qarab yopadi | Butun oqim qadamlarini o'qiydi |
| Zanjirni uzish | O'z utilita validatori yoziladi | Tur o'zgarishi va enum ishlatiladi |
| SQL yozish joyi | Istalgan qatlamda | Faqat repository da, ArchUnit bilan majburlanadi |
| Sink lar soni | Kod bo'ylab tarqalgan | Bitta adapter ichida to'plangan |
| Community nashr cheklovi | Sezilmaydi, "muammo yo'q" deb o'ylanadi | Ochiq tan olinadi, tashqi vosita qo'shiladi |
| Tahlil vaqti | Sekinlashsa e'tibor berilmaydi | Exclusion va xotira sozlanadi, vaqt kuzatiladi |
| False positive | Exclusion bilan butun fayl yashiriladi | Nuqtaviy suppress va izoh yoziladi |
| Mas'uliyat | Issue ni oxirgi tegingan odam yopadi | Xavfsizlik oqimlari uchun aniq egalik bor |
| Yangi sink paydo bo'lganda | Hech kim bilmaydi | Review checklist da tekshiriladi |

## 37.11 Spring loyihasida tipik oqimlar: so'rov parametri, header, fayl nomi, SQL

Birinchi tipik oqim so'rov parametridan SQL gacha. Buni yuqorida ko'rdik, u eng ko'p uchraydigan holat va `order by`, `like` hamda dinamik filtr qurishda paydo bo'ladi.

Ikkinchi oqim header dan log yoki javobga. `@RequestHeader` bilan olingan qiymat to'g'ridan to'g'ri javobga chiqsa, reflected XSS zanjiri hosil bo'ladi. Bu ayniqsa xato sahifalari va diagnostika endpointlarida uchraydi.

Uchinchi oqim yuklangan fayl nomidan fayl yo'ligacha. `MultipartFile.getOriginalFilename()` natijasi butunlay mijoz nazoratida va u yo'l ajratuvchi belgilarni o'z ichiga olishi mumkin. Shuning uchun uni to'g'ridan to'g'ri `Paths.get` ga bermaslik kerak.

```java
@PostMapping("/hujjat")
public String upload(@RequestParam MultipartFile file) throws IOException {
    // Mijozdan kelgan nom ishlatilmaydi, server o'zi nom generatsiya qiladi.
    String storedName = UUID.randomUUID() + ".bin";

    Path base = storageRoot.toAbsolutePath().normalize();
    Path target = base.resolve(storedName).normalize();

    // Qo'shimcha himoya: natija baza katalogidan chiqib ketmasligi.
    if (!target.startsWith(base)) {
        throw new IllegalStateException("Yo'l baza katalogidan tashqarida");
    }
    file.transferTo(target);
    return storedName;
}
```

To'rtinchi oqim tashqi HTTP javobidan ichki chaqiruvgacha. Hamkor servisning javobi ham ishonchsiz manba, ayniqsa u fayl nomi yoki URL qaytarsa. Bu holat ombor qoldig'ini tashqi tizimdan olib keladigan integratsiyalarda tez-tez uchraydi.

Taint tahlilini yoqish uchun maxsus plugin kerak emas, oddiy Sonar sozlamasi yetarli. Muhim shart faqat nashr va to'g'ri Java versiyasi.

```xml
<build>
  <plugins>
    <plugin>
      <groupId>org.sonarsource.scanner.maven</groupId>
      <artifactId>sonar-maven-plugin</artifactId>
      <!-- Versiyani o'z serveringiz talabiga qarab tanlang. -->
      <version>4.0.0.4121</version>
    </plugin>
    <plugin>
      <groupId>org.jacoco</groupId>
      <artifactId>jacoco-maven-plugin</artifactId>
      <version>0.8.12</version>
      <executions>
        <execution>
          <goals><goal>prepare-agent</goal></goals>
        </execution>
        <execution>
          <id>report</id>
          <phase>verify</phase>
          <goals><goal>report</goal></goals>
        </execution>
      </executions>
    </plugin>
  </plugins>
</build>
```

## 37.12 Taint natijasini jamoada kim ko'rib chiqishi

Taint issue oddiy code smell emas, shuning uchun uni ixtiyoriy dasturchi yopmasligi kerak. Amalda ishlaydigan model quyidagicha.

Kirish nuqtasining egasi birinchi javobgar. Agar oqim `OrderController` dan boshlangan bo'lsa, shu modulning jamoasi issue ni ko'rib chiqadi. Ular oqimni o'qiydi va uchta qarordan birini qabul qiladi: kodni tuzatish, zanjirni turga aylantirish bilan uzish, yoki dalil bilan false positive deb belgilash.

Ikkinchi javobgar sink egasi. Repository yoki storage komponentini yuritadigan odam o'z sink ini bir marta himoyalab, o'nlab kelajakdagi oqimni yopishi mumkin. Bu eng foydali investitsiya, chunki u takrorlanadigan ishni yo'q qiladi.

Uchinchi rol xavfsizlik yoki texnik yetakchi. U false positive deb yopilgan issue larni davriy ko'rib chiqadi va yopish izohlari haqiqatan dalil ekanini tekshiradi. Bu nazorat bo'lmasa, bir yil ichida barcha taint issue lar izohsiz yopilgan holatga keladi.

Quality gate tomonida qattiq qoida saqlash mantiqan to'g'ri. Yangi kodda ochiq xavfsizlik issue si bo'lmasligi sharti ko'p loyihada asosli, chunki bu toifa soni kam va har biri jiddiy. Eski kod uchun esa alohida reja tuzish kerak, aks holda gate doimiy qizil turadi va jamoa unga ishonishni to'xtatadi.

## 37.13 Amalda qo'llash

- [ ] O'z SonarQube nashringizni aniqlang va taint analysis mavjudligini tasdiqlang, Community bo'lsa bu cheklovni jamoaga ochiq ayting.
- [ ] Oxirgi tahlildagi barcha injection toifasidagi issue larni ochib, har birining oqim qadamlarini boshidan oxirigacha o'qib chiqing.
- [ ] Loyihada SQL yoziladigan va fayl yo'li quriladigan barcha joylarni sanab chiqing, ularni bitta qatlamga yig'ish rejasini tuzing.
- [ ] Dinamik `order by` va dinamik filtr ishlatilgan joylarda matn parametrini `enum` yoki oq ro'yxat konstantasiga almashtiring.
- [ ] Yuklangan fayl nomini bevosita ishlatadigan kodni toping va server tomonida generatsiya qilingan nomga o'tkazing.
- [ ] False positive deb yopilgan har bir xavfsizlik issue siga dalil izohi yozilganini tekshiring, izohsizlarini qayta oching.
- [ ] CI da tahlil bosqichi uchun xotira limitini va exclusion ro'yxatini sozlab, tahlil vaqtini o'lchab yozib qo'ying.
- [ ] Review checklist ga bitta band qo'shing: yangi xavfli chaqiruv qo'shilganda uning kirish nuqtasi qanday himoyalangani ko'rsatilsin.

---

[&larr; 36. Web API va avtomatlashtirish](36-web-api-va-avtomatlashtirish.md) · [Mundarija](README.md) · [38. Ko'p tilli loyiha: SQL, XML, YAML, Docker, Kubernetes, frontend &rarr;](38-kop-tilli-loyiha-sql-xml-yaml-docker.md)
