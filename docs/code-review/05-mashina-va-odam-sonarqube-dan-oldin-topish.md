<!-- doc: code-review | chapter: 5 | part: I. Review ning mohiyati va iqtisodi -->

[Barcha hujjatlar](../../README.md) / [Kod review](README.md)

# 5. Mashina va odam: SonarQube dan oldin topish (Beating the Tools)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

- [5.1 Nega Sonar dan oldin topish kerak](#51-nega-sonar-dan-oldin-topish-kerak)
- [5.2 Mashina deterministik tutadigan narsalar](#52-mashina-deterministik-tutadigan-narsalar)
- [5.3 Mashina tuta olmaydigan narsalar](#53-mashina-tuta-olmaydigan-narsalar)
- [5.4 Qo'lda statik tahlil o'tishi: o'n to'rt savol](#54-qolda-statik-tahlil-otishi-on-tort-savol)
- [5.5 Cognitive complexity ni ko'zda hisoblash](#55-cognitive-complexity-ni-kozda-hisoblash)
- [5.6 Null yo'lini qo'lda kuzatish](#56-null-yolini-qolda-kuzatish)
- [5.7 Resurs oqishini ko'rish](#57-resurs-oqishini-korish)
- [5.8 Security hotspot: mashina belgilaydi, qarorni odam qabul qiladi](#58-security-hotspot-mashina-belgilaydi-qarorni-odam-qabul-qiladi)
- [5.9 Coverage raqami aldaganda](#59-coverage-raqami-aldaganda)
- [5.10 Shovqinni kamaytirish va izohni qoidaga aylantirish](#510-shovqinni-kamaytirish-va-izohni-qoidaga-aylantirish)
- [5.11 Amalda qo'llash](#511-amalda-qollash)

</details>


Reviewer uchun eng past hurmat keltiradigan holat - Sonar topgan narsani review ham topmaganligi. Eng yuqori qiymat keltiradigan holat - Sonar hech qachon topa olmaydigan narsani topish. Shu ikki qutb orasida reviewer ning haqiqiy darajasi aniqlanadi. Bu bob ikki narsani beradi: mashinadan oldinda yurish uchun qo'lda bajariladigan statik tahlil o'tishi, va mashina tuta olmaydigan sinflarning aniq ro'yxati. SonarQube ning ichki mexanikasi va qoidalar katalogi [SonarQube](../sonarqube/README.md) da, bu yerda faqat review stoli nuqtai nazari.

## 5.1 Nega Sonar dan oldin topish kerak

Birinchi sabab - vaqt. Sonar natijasi PR ochilgandan keyin 3-15 daqiqada keladi, ba'zi loyihalarda yarim soatdan keyin. Agar reviewer shu vaqtni kutsa, u kontekstni yo'qotadi. Agar kutmasa va keyin Sonar 12 ta issue chiqarsa, muallif ikkinchi davraga kiradi.

Ikkinchi sabab - signal sifati. Sonar `S2095` (resurs yopilmagan) deb aytadi, lekin "bu resurs yuk ostida 200 ta ulanishni egallaydi va pool ni to'ldiradi" demaydi. Qoida raqami xatoni ko'rsatadi, oqibatni ko'rsatmaydi. Muallif oqibatni bilmasa, u xatoni tuzatadi, lekin shu sinf xatoni qaytarmaslikni o'rganmaydi.

Uchinchi sabab - ishonch. Agar reviewer Sonar dan keyin hech narsa qo'shmasa, jamoa review ni kerak emas deb hisoblashni boshlaydi, va bu to'g'ri xulosa bo'ladi.

## 5.2 Mashina deterministik tutadigan narsalar

Bu ro'yxatni reviewer bilishi kerak, chunki unga vaqt sarflash - isrof. Bu narsalar PR ochilishidan oldin lokal `verify` da tutilishi kerak.

| Sinf | Misol | Instrument |
| --- | --- | --- |
| Uslub va format | Qavs joyi, import tartibi, satr uzunligi | spotless, checkstyle |
| Ishlatilmaydigan kod | O'qilmagan o'zgaruvchi, yetib bo'lmaydigan kod | kompilyator, Sonar |
| Aniq null yo'li | `null` qaytaradigan metod natijasi tekshirilmagan | Sonar, ErrorProne, SpotBugs |
| Resurs yopilmaganligi | `InputStream`, `Stream`, `Connection` | Sonar S2095 |
| Shubhali taqqoslash | `==` bilan `String`, `equals` bilan turli tur | ErrorProne |
| Mantiqiy doimiy shart | Har doim rost bo'lgan `if` | Sonar |
| Takroriy kod bloklari | Copy-paste bloklar | Sonar CPD |
| Murakkablik chegarasi | Cognitive complexity > 15 | Sonar |
| Ma'lum CVE | Zaif kutubxona versiyasi | dependency-check, Dependabot |
| Oddiy injection naqshlari | SQL satriga konkatenatsiya | Sonar, Semgrep |
| Qattiq yozilgan secret | Koddagi parol satri | gitleaks, Sonar |
| Standart API noto'g'ri ishlatilishi | `Optional.get()` tekshirmasdan | Sonar, ErrorProne |

Xulosa: bu jadvaldagi hech narsa review izohiga aylanmasligi kerak. Agar aylansa, muammo instrumentda, odamda emas. To'g'ri javob - qoidani CI ga qo'yish, izoh yozmaslik.

## 5.3 Mashina tuta olmaydigan narsalar

Bu reviewer ning haqiqiy ish maydoni. Hamma bandning umumiy xususiyati bor: ularni topish uchun niyat, domen yoki tizim konteksti kerak, ya'ni koddan tashqaridagi bilim.

| Sinf | Misol | Nega mashina ko'rmaydi |
| --- | --- | --- |
| Noto'g'ri biznes qoidasi | Chegirma 10% emas, 15% bo'lishi kerak | Talab kodda yo'q |
| Buzilgan invariant | Qoldiq manfiyga tushishi mumkin | Invariant e'lon qilinmagan |
| Yo'q kod | Avtorizatsiya tekshiruvi qo'yilmagan | Yo'q narsani ko'rsatish uchun model kerak |
| Poyga holati | Tekshir-keyin-yoz ikki instansda | Ish vaqti xulqi, statik emas |
| Noto'g'ri abstraksiya | Interfeysning bitta implementatsiyasi va soxta moslashuvchanlik | Dizayn qarori |
| Pattern noto'g'ri qo'llanishi | Strategy o'rniga `if` zinapoyasi, yoki teskarisi | Kontekstga bog'liq |
| Tranzaksiya chegarasi noto'g'ri | Tashqi chaqiruv tranzaksiya ichida | Semantika, qoida emas |
| Ma'lumot modeli xatosi | Pul `double` da, vaqt `LocalDateTime` da | Domen bilimi |
| Yetarsiz test holati | Test bor, lekin chegaraviy qiymat yo'q | Qamrov o'lchanadi, to'g'rilik o'lchanmaydi |
| Yolg'on test | Assertion yo'q yoki `assertNotNull` bilan tugaydi | Test kompilyatsiya bo'ladi va o'tadi |
| Avtorizatsiya mantiqi teshigi | Foydalanuvchi boshqa ID ni so'rasa | Faqat domen bilan aniqlanadi |
| Migratsiya operatsion xavfi | `ALTER` 12 mln qatorni qulflaydi | Jadval hajmi kodda yo'q |
| Observability bo'shlig'i | Xato bo'lsa, bilib bo'lmaydi | O'lchov talabi kodda yo'q |
| Orqaga moslik buzilishi | Maydon nomi o'zgargan, eski mijoz bor | Mijozlar kodda yo'q |
| Performance regressiyasi | Siklda tashqi chaqiruv | Yuk va hajmga bog'liq |

## 5.4 Qo'lda statik tahlil o'tishi: o'n to'rt savol

Bu ro'yxat Sonar dan oldin bajariladi va taxminan 10 daqiqa oladi. Maqsad - Sonar chiqaradigan issue larning katta qismini oldin ko'rish va ularni oqibat bilan birga aytish.

1. Har bir yangi `public` metod kirishini tekshiradimi, yoki tekshirish chaqiruvchida qoldirilganmi.
2. Qaytarilgan `null` bormi, va u `Optional` bilan almashtirilishi kerakmi.
3. Tashqi manbadan kelgan qiymat `Optional.get()`, `orElseThrow()` yoki `charAt(0)` bilan to'g'ridan-to'g'ri ishlatilganmi.
4. Yangi ochilgan resurs (`Stream`, `InputStream`, `Connection`, `ExecutorService`) `try-with-resources` ichida yoki `close` yo'li borligi ko'rinadimi.
5. `catch` bloklari qanday: `Exception` ni yutib yuborgan yoki kontekstsiz qayta tashlagan joy bormi.
6. Siklda tashqi chaqiruv (DB, HTTP, kesh) bormi.
7. Shartlar soni: eng katta metodda nechta shoxlanish bor, 15 dan oshadimi.
8. Takrorlangan blok bormi: xuddi shu 10 satr boshqa faylda ham turganmi.
9. `String` konkatenatsiyasi bilan quriladigan so'rov yoki buyruq bormi.
10. Sanab o'tiladigan holatlar to'liqmi: `switch` da `default` bormi, yangi enum qiymati qo'shilsa nima bo'ladi.
11. Taqqoslashlar: `equals`/`hashCode` juftligi buzilmaganmi, `compareTo` bilan `equals` mos keladimi.
12. Sonlar: butun sonlar bo'linishi, `int` ga sig'may qolish, pul uchun `double` ishlatilishi bormi.
13. Vaqt: `new Date()`, `LocalDateTime.now()` to'g'ridan-to'g'ri ishlatilganmi (test qilinmaydigan va zonasiz).
14. Mutable holat: statik o'zgaruvchi, umumiy `HashMap`, `SimpleDateFormat` bean sifatida bormi.

```java
// Shu o'n to'rt savolni bitta misolda ko'rish. Sonar bu kodda 6-7 issue
// topadi, lekin reviewer ularni oqibat bilan aytadi.
@Service
public class ReportService {

    // (14) Mutable umumiy holat: SimpleDateFormat thread-safe emas.
    //      Ikki parallel so'rov buzilgan sana beradi yoki istisno tashlaydi.
    private static final SimpleDateFormat FMT = new SimpleDateFormat("yyyy-MM-dd");

    private final JdbcTemplate jdbc;
    private final RateClient rates;

    public ReportService(JdbcTemplate jdbc, RateClient rates) {
        this.jdbc = jdbc;
        this.rates = rates;
    }

    public List<Row> build(String from, String to, String sortBy) {
        // (1) Kirish tekshirilmagan, (9) so'rov konkatenatsiya bilan qurilgan.
        //     sortBy foydalanuvchidan kelsa - SQL injection.
        String sql = "SELECT id, amount, currency, created_at FROM payments "
                   + "WHERE created_at BETWEEN '" + from + "' AND '" + to + "' "
                   + "ORDER BY " + sortBy;

        List<Map<String, Object>> raw = jdbc.queryForList(sql);
        List<Row> out = new ArrayList<>();

        for (Map<String, Object> r : raw) {
            // (6) Siklda tashqi HTTP chaqiruvi: 10 000 qator = 10 000 so'rov.
            //     p99 30 ms bo'lsa ham, bu 5 daqiqa.
            BigDecimal rate = rates.rateFor((String) r.get("currency"));

            // (12) Pul hisobi double orqali o'tyapti: aniqlik yo'qoladi.
            double amount = ((Number) r.get("amount")).doubleValue()
                          * rate.doubleValue();

            // (13) Zona yo'q: server zonasiga bog'liq natija.
            out.add(new Row(FMT.format(r.get("created_at")), amount));
        }
        return out;
    }
}
```

Shu kodga review izohi Sonar tilida emas, oqibat tilida yoziladi:

```text
blocker: sortBy to'g'ridan-to'g'ri ORDER BY ga qo'yilgan. Agar u so'rov
         parametridan kelsa, bu SQL injection: `1; DROP TABLE ...` emas,
         lekin `(SELECT ...)` bilan ma'lumot chiqarib olish mumkin.
         Yechim: ruxsat etilgan ustunlar ro'yxati (whitelist) + enum.

blocker: rates.rateFor sikl ichida chaqirilgan. 10 000 qatorli hisobotda bu
         10 000 HTTP so'rov. Valyutalar soni 10 tadan oshmaydi - oldin bir
         marta olib, Map ga joylash kerak.

blocker: pul hisobi double da. 0.1 + 0.2 muammosi hisobotda markazlashgan
         xatoga olib keladi. BigDecimal va aniq scale kerak.

suggest: SimpleDateFormat static - thread-safe emas. DateTimeFormatter
         (immutable) ga o'tkazish kerak.

question: created_at BETWEEN ikki satr bilan solishtirilgan. Ustun turi
          timestamptz bo'lsa, zona qanday hisobga olinadi?
```

## 5.5 Cognitive complexity ni ko'zda hisoblash

Sonar `cognitive complexity` ni hisoblaydi, lekin reviewer uni chamalab bilishi kerak. Hisob oddiy: har bir shoxlanish bir ball, ichma-ich joylashgan shoxlanish chuqurligicha ko'p ball, `else if` zanjiri har bir bo'g'in uchun ball, `catch` bir ball, uzilish operatorlari (`break`, `continue` yorliq bilan) ball.

Amaliy mezon: bitta ekranga sig'maydigan va uch darajadan chuqur ichma-ich shartga ega metod allaqachon chegaradan o'tgan. Sonar aytishini kutish shart emas.

Muhim nuans: murakkablikni kamaytirish uchun metodni ikkiga bo'lish ko'rsatkichni yaxshilaydi, lekin tushunarlilikni yaxshilamasligi mumkin. Agar ajratilgan metod `part1`, `part2` deb nomlangan bo'lsa, bu ko'rsatkichni aldash. To'g'ri yechim - domen tilidagi nom bilan ajratish yoki shoxlanishni polimorfizm bilan almashtirish ([10-bobga](10-dizayn-pattern-review-i-yoq-patternni-korish.md) qarang).

## 5.6 Null yo'lini qo'lda kuzatish

Statik tahlil null ni faqat bitta metod ichida ishonchli kuzatadi. Metoddan metodga o'tgan null uchun annotatsiya kerak. Shu sababli reviewer null ni chegaralarda kuzatadi.

```java
// Null chegaralarini aniq qilish: review da shu uch naqsh talab qilinadi.

// 1) Paket darajasida standart: hamma narsa null bo'lmaydi, istisno belgilanadi.
//    package-info.java
@NullMarked
package com.acme.order.domain;   // JSpecify (yoki @NonNullApi - Spring)

// 2) Qaytish turida null yo'q: Optional yoki bo'sh to'plam.
public interface OrderRepository {
    Optional<Order> findByNumber(String number);   // yaxshi
    List<Order> findOpen();                        // bo'sh ro'yxat, null emas
    // Order findByNumber(String n);               // yomon: null qaytarishi mumkin
}

// 3) Kirishda tekshiruv chegarada bir marta, keyin ishonch.
public Receipt charge(ChargeCommand cmd) {
    Objects.requireNonNull(cmd, "cmd");
    // Domen obyekti ichida null bo'lmasligi konstruktorda kafolatlanadi,
    // shuning uchun quyidagi kodda null tekshiruvi takrorlanmaydi.
    return gateway.charge(cmd.amount(), cmd.card());
}

// Review savoli: tashqi JSON dan kelgan DTO da @NotNull bormi, yoki null
// domenga kirib ketadimi? Jackson bo'sh maydonni null qilib qoldiradi.
public record ChargeRequest(
        @NotNull @Positive BigDecimal amount,
        @NotBlank String currency,
        @NotNull @Valid CardRequest card) { }
```

## 5.7 Resurs oqishini ko'rish

Sonar yopilmagan `Stream` ni topadi, lekin "yopildi, lekin kech yopildi" holatini topmaydi. Review da uch savol beriladi: resurs kim tomonidan ochildi, kim yopadi, va yopilish istisno bo'lganda ham kafolatlanganmi.

```java
// PostgreSQL bilan oqimli o'qish: resurs oqishining klassik joyi.

// Yomon: Stream yopilmaydi, kursor va ulanish ushlab qolinadi.
@Transactional(readOnly = true)
public void exportAll(Writer out) {
    orders.streamAllByStatus(OPEN)        // Stream<Order> qaytaradi
          .forEach(o -> write(out, o));   // istisno bo'lsa - oqim ochiq qoladi
}

// Yaxshi: try-with-resources + fetch size + statelessSession/clear.
@Transactional(readOnly = true)
public void exportAll(Writer out) {
    try (Stream<Order> rows = orders.streamAllByStatus(OPEN)) {
        rows.forEach(o -> {
            write(out, o);
            // Hibernate birinchi darajali keshi o'smasligi uchun: aks holda
            // 2 mln qator heap ga to'planadi va OOM bo'ladi.
            em.detach(o);
        });
    }
}
// Review izohi: @Transactional(readOnly = true) va fetchSize birga kerak.
// PostgreSQL JDBC kursor rejimiga faqat autoCommit=false da o'tadi,
// aks holda butun natija klientga tortiladi (hujjat: architect, JDBC bo'limi).
```

## 5.8 Security hotspot: mashina belgilaydi, qarorni odam qabul qiladi

Sonar da "security hotspot" degan toifa bor: bu xato emas, qaror talab qiladigan joy. Masalan `Random` ishlatilishi, HTTP header o'qilishi, fayl yo'li qurilishi. Mashina ularni belgilaydi, lekin xavfli yoki xavfsiz ekanini kontekst hal qiladi.

Reviewer uchun qoida: hotspot ko'rsatilganda "bu yerda tashqi, ishonilmaydigan ma'lumot bormi" degan savolga javob yozib qoldirish kerak. Javob izohda qolsa, keyingi reviewer o'sha ishni qaytadan qilmaydi. Xavfsizlik review ning to'liq metodikasi VI bo'limda.

## 5.9 Coverage raqami aldaganda

Coverage - kod bajarildimi degan savolga javob beradi, to'g'ri ishladimi degan savolga javob bermaydi. Shu sababli reviewer coverage foiziga qaramaydi, assertion larga qaraydi.

```java
// 100% line coverage beradigan, lekin hech narsani tekshirmaydigan test.
@Test
void calculatesDiscount() {
    Order order = new Order(BigDecimal.valueOf(1000), CustomerTier.GOLD);
    BigDecimal result = calculator.discountFor(order);
    assertThat(result).isNotNull();          // yolg'on ishonch
}

// Review izohi (blocker): assertion qiymatni tekshirmaydi. Bu test
// discountFor ichidagi har qanday o'zgarishda ham o'tadi. Kutilgan qiymat
// yozilishi kerak, va GOLD/SILVER/chegaraviy summalar uchun alohida holat.

// To'g'ri shakl: aniq qiymat va chegaralar.
@ParameterizedTest
@CsvSource({
    "999.99, GOLD,   0.00",   // chegaradan past: chegirma yo'q
    "1000.00, GOLD, 150.00",  // chegara aynan: 15%
    "1000.00, SILVER, 50.00", // boshqa daraja
    "0.00,   GOLD,   0.00"    // nol summa
})
void discountMatchesTable(BigDecimal total, CustomerTier tier, BigDecimal expected) {
    assertThat(calculator.discountFor(new Order(total, tier)))
        .isEqualByComparingTo(expected);
}
```

Coverage raqami foydali bo'ladigan bitta holat bor: yangi kod uchun coverage nolga teng bo'lsa, demak test umuman yozilmagan. Qolgan hamma holatda raqam emas, test holatlarining to'liqligi muhim. Test to'liqligini review qilish VII bo'limda batafsil.

## 5.10 Shovqinni kamaytirish va izohni qoidaga aylantirish

Reviewer bir xil izohni uchinchi marta yozayotgan bo'lsa, u noto'g'ri ish qilyapti. To'g'ri harakat - izohni avtomatik qoidaga aylantirish. Bu review ning eng yuqori qaytimli ishi: bir marta sarflangan vaqt keyingi barcha PR larda tejaladi.

```java
// Takrorlanadigan arxitektura izohini ArchUnit qoidasiga aylantirish.
// "Controller to'g'ridan-to'g'ri repository ga murojaat qilmasligi kerak"
// izohini uchinchi marta yozish o'rniga:
@AnalyzeClasses(packages = "com.acme", importOptions = DoNotIncludeTests.class)
class ArchitectureRulesTest {

    @ArchTest
    static final ArchRule controllers_do_not_touch_repositories =
        noClasses().that().resideInAPackage("..web..")
                   .should().dependOnClassesThat().resideInAPackage("..repository..")
                   .because("web qatlami application servis orqali o'tishi kerak");

    @ArchTest
    static final ArchRule domain_is_framework_free =
        noClasses().that().resideInAPackage("..domain..")
                   .should().dependOnClassesThat()
                   .resideInAnyPackage("org.springframework..", "jakarta.persistence..")
                   .because("domen frameworkdan mustaqil bo'lsin");

    @ArchTest
    static final ArchRule no_field_injection =
        noFields().should().beAnnotatedWith(Autowired.class)
                  .because("konstruktor orqali inyeksiya: testlanadigan va immutable");

    @ArchTest
    static final ArchRule transactional_only_in_application_layer =
        methodsThat(are(annotatedWith(Transactional.class)))
            .should().beDeclaredInClassesThat().resideInAPackage("..application..")
            .because("tranzaksiya chegarasi bitta qatlamda turishi kerak");
}
```

```xml
<!-- Takrorlanadigan Java darajasidagi izohni kompilyatsiya xatosiga aylantirish.
     ErrorProne review dan oldin, kompilyatsiya paytida gapiradi. -->
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-compiler-plugin</artifactId>
  <configuration>
    <compilerArgs>
      <arg>-XDcompilePolicy=simple</arg>
      <arg>--should-stop=ifError=FLOW</arg>
      <!-- Pul double da, Date ishlatilishi, == bilan String taqqoslash -->
      <arg>-Xplugin:ErrorProne
           -Xep:MissingOverride:ERROR
           -Xep:ReferenceEquality:ERROR
           -Xep:FallThrough:ERROR
           -Xep:OptionalGetWithoutIsPresent:ERROR
           -Xep:StreamResourceLeak:ERROR</arg>
    </compilerArgs>
  </configuration>
</plugin>
```

Qoidaga aylantirishning chegarasi ham bor: kontekstga bog'liq qarorni qoida qilib qo'yish shovqin keltiradi va jamoa qoidani o'chirib tashlaydi. Mezon oddiy - agar istisno 10 foizdan ko'p holatda kerak bo'lsa, bu qoida emas, muhokama mavzusi.

## 5.11 Amalda qo'llash

- [ ] Oxirgi 20 PR dagi Sonar issue larini sanab, ularning qanchasi review izohida ham aytilganini tekshiring. Nisbat past bo'lsa, 14 savolli o'tishni joriy qiling.
- [ ] 14 savolli qo'lda statik tahlil ro'yxatini `REVIEW.md` ga qo'shing va uni yuqori xavfli PR larda majburiy qiling.
- [ ] ErrorProne ni `maven-compiler-plugin` ga ulab, kamida `ReferenceEquality`, `OptionalGetWithoutIsPresent`, `StreamResourceLeak` ni `ERROR` darajasiga qo'ying.
- [ ] Takrorlanadigan uchta arxitektura izohini ArchUnit testiga aylantirib, CI ga qo'shing.
- [ ] Loyihadagi `SimpleDateFormat`, `new Date()`, `double` bilan pul hisobini grep bilan topib, ro'yxat tuzing va qoidaga aylantiring.
- [ ] `package-info.java` ga `@NullMarked` (yoki `@NonNullApi`) qo'yib, null chegarasini e'lon qiling.
- [ ] Yangi kod coverage i emas, yangi testlardagi assertion sifatini tekshirishni review bandiga aylantiring: `assertNotNull` bilan tugaydigan testlarni toping.
- [ ] Sonar hotspot lari uchun "tashqi ma'lumot bormi" javobini izohda yozib qoldirish qoidasini joriy qiling.

---

[&larr; 4. Diffni o'qish mexanikasi](04-diffni-oqish-mexanikasi.md) · [Mundarija](README.md) · [6. Arxitektura review: qatlam, chegara, bog'liqlik yo'nalishi &rarr;](06-arxitektura-review-qatlam-chegara-bogliqlik.md)
