<!-- doc: clean-code | chapter: 42 | part: XI. Kod bazasi va jarayon gigiyenasi -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 42. Statik tahlil va avtomatik qoidalar (Static Analysis and Automated Rules)

<details>
<summary>Bu bobdagi 8 bo'lim</summary>

- [42.1 Kompilyator birinchi tekshiruvchi](#421-kompilyator-birinchi-tekshiruvchi)
- [42.2 Error Prone va NullAway](#422-error-prone-va-nullaway)
- [42.3 SpotBugs, PMD va Checkstyle rollari](#423-spotbugs-pmd-va-checkstyle-rollari)
- [42.4 ArchUnit bilan qoidani kodga aylantirish](#424-archunit-bilan-qoidani-kodga-aylantirish)
- [42.5 Maxsus lint qoidasi yozish](#425-maxsus-lint-qoidasi-yozish)
- [42.6 Qoidani joriy qilish tartibi: ogohlantirish, keyin xato](#426-qoidani-joriy-qilish-tartibi-ogohlantirish-keyin-xato)
- [42.7 False positive va bostirishni hujjatlashtirish](#427-false-positive-va-bostirishni-hujjatlashtirish)
- [42.8 Amalda qo'llash](#428-amalda-qollash)

</details>


Toza kod qoidasi odam xotirasida yashasa, u buziladi. Shu sababli har bir qoidaning oxirgi manzili - mashina. SonarQube ning mexanikasi, quality gate va xato katalogi alohida hujjatda; bu bobda qolgan vositalar va qoidani joriy qilish tartibi.

## 42.1 Kompilyator birinchi tekshiruvchi

Kompilyator eng tez va eng arzon statik tahlilchi, lekin uning ogohlantirishlari odatda o'chirilgan holda qoldiriladi. `-Xlint:all -Werror` bir martalik sozlama va u darhol o'nlab muammoni topadi (25.10).

| Vosita | Nima topadi | Narxi |
|---|---|---|
| Kompilyator `-Xlint` | xom tur, deprecation, unchecked | bepul |
| Error Prone | xatolik namunalari (300+ qoida) | kompilyatsiyaga +20% |
| NullAway | `null` xavfi | kam |
| Checkstyle | uslub va nomlash | kam |
| SpotBugs | bytecode darajasidagi xatolar | o'rtacha |
| PMD | murakkablik, o'lik kod | o'rtacha |
| ArchUnit | arxitektura qoidalari | test sifatida |
| SonarQube | hammasi + tarix va gate | server |

**Kompilyator darajasida nimani xato qilish mumkin.** Google ning statik tahlil siyosati kompilyatorda xato qilinadigan tekshiruvlarga uch shart qo'yadi, va u `-Xlint:all -Werror` dan ko'ra tanlanganroq:

1. **Bajarilishi mumkin va oson tuzatiladi** - iloji bo'lsa xato mexanik qo'llanadigan tuzatma taklif qiladi.
2. **Amalda yolg'on pozitiv bermaydi** (no effective false positives) - to'g'ri kod uchun build hech qachon to'xtamaydi.
3. **Faqat to'g'rilikka ta'sir qiladi** - uslub yoki yaxshi amaliyot emas. Uslub qoidasi review ga yoki alohida linterga qoladi.

Shuning uchun Error Prone ning `ERROR` darajasidagi qoidalari Google ning Java kompilyatorida yoqilgan: ular aynan shu uchta shartni qondiradi. Yangi tekshiruvni yoqishdan oldin kod bazasidagi hamma mavjud buzilish tozalanadi, aks holda kompilyator rivojlangani uchun mavjud loyihalarning buildi qiziladi; ya'ni yangi tekshiruvning qiymati hamma mavjud holatni tuzatishga arzishi kerak.

Ikkinchi qoida qattiqroq: **kompilyator ogohlantirishi chiqarilmaydi**. Google ning tajribasi - muhandislar kompilyator ogohlantirishini e'tiborsiz qoldiradi, shuning uchun tekshiruv yoki xato darajasida yoqiladi (build to'xtaydi), yoki kompilyator chiqishida umuman ko'rsatilmaydi. Build ni to'xtata olmaydigan tekshiruv yo bostiriladi, yo review vositasida ko'rsatiladi. Java va C++ kompilyatorlari aynan shunday sozlangan, Go esa buni chegaraga olib boradi: boshqa tillarda ogohlantirish bo'lgan narsa (ishlatilmagan o'zgaruvchi yoki import) Go da xato.

Shundan amaliy xulosa: `-Xlint:all -Werror` ni butun loyihaga bir zarb bilan yoqish 42.6 dagi bosqichli tartibdan o'tadi, lekin oxirgi holat **ogohlantirish qolmaslik** bo'lishi kerak - "ogohlantirishlar bor, lekin ularga qaramaydi" holati Google ning pozitsiyasida eng yomon variant.

## 42.2 Error Prone va NullAway

Error Prone kompilyatsiya paytida ishlaydi va **xatolik namunalarini** topadi - uslub emas, haqiqiy xatolar. Bu hujjatdagi ko'p qoidalar uning qoidalariga bevosita mos keladi.

| Bu hujjatdagi qoida | Error Prone qoidasi |
|---|---|
| `equals` bor, `hashCode` yo'q (15.2) | `EqualsHashCode` |
| `finally` da `return` (19.3) | `Finally` |
| Nostatik ichki sinf (25.7) | `ClassCanBeStatic` |
| `split` regex tuzog'i (21.5) | `StringSplitter` |
| Kodirovka berilmagan (21.3) | `DefaultCharset` |
| `java.util.Date` (22.1) | `JavaUtilDate` |
| `BigDecimal.equals` (20.2) | `BigDecimalEquals` |
| Natija e'tiborsiz qoldirilgan | `ReturnValueIgnored` |
| `Optional.get` tekshiruvsiz (24.6) | `OptionalGetWithoutIsPresent` |
| Immutable obyektga yozish (16.1) | `Immutable` |
| Ishlatilmaydigan o'zgaruvchi (33.10) | `UnusedVariable` |

NullAway esa `null` xavfini kompilyatsiya vaqtida topadi va u JSpecify annotatsiyalari bilan ishlaydi ([arxitektor hujjatidagi](../architect/README.md) null xavfsizligi bo'limi): paketga `@NullMarked` qo'yilsa, barcha turlar standart holatda `null` bo'lmaydi va istisnolar `@Nullable` bilan belgilanadi.

```java
// package-info.java (10.7)
@NullMarked
package uz.shop.payment;

// Endi null qaytarish kompilyatsiya xatosi
Payment find(PaymentId id) { return null; }        // NullAway: ERROR

// Oshkor nullable
@Nullable Payment findOrNull(PaymentId id) { return null; }   // ruxsat
```

## 42.3 SpotBugs, PMD va Checkstyle rollari

Uch vositaning rollari qo'shilmasligi kerak, aks holda bir xil muammo uch marta xabar qilinadi va jamoa hisobotlarni o'qishni to'xtatadi.

| Vosita | Roli | Qoidalar soni |
|---|---|---|
| Checkstyle | uslub, nomlash, tuzilish chegaralari | 20-30 (tanlangan) |
| SpotBugs | bytecode darajasidagi xatolar, thread xavfi | standart to'plam |
| PMD | murakkablik, o'lik kod, takrorlanish | tanlangan |
| Error Prone | xatolik namunalari | standart + tanlangan |

Amaliy tavsiya: Checkstyle (uslub) + Error Prone (xatolar) + Sonar (umumiy) kombinatsiyasi ko'p loyihada yetarli; SpotBugs va PMD ni faqat aniq ehtiyoj bo'lganda qo'shish.

## 42.4 ArchUnit bilan qoidani kodga aylantirish

ArchUnit arxitektura va kod qoidalarini **test** sifatida yozadi va bu eng moslashuvchan usul: qoida kod bazasiga xos bo'lsa, uni hech qanday linter bilmaydi. Arxitektor hujjati 36.9 da qatlam qoidalari misoli berilgan; bu yerda shu hujjatdagi qoidalarni majburlash.

```java
@AnalyzeClasses(packages = "uz.shop", importOptions = ImportOption.DoNotIncludeTests.class)
class CleanCodeRulesTest {

    // 22.1: eski sana API si taqiqlangan
    @ArchTest
    static final ArchRule eski_sana_api_taqiqlangan =
            noClasses().should().dependOnClassesThat()
                    .haveFullyQualifiedName("java.util.Date")
                    .orShould().dependOnClassesThat()
                    .haveFullyQualifiedName("java.text.SimpleDateFormat");

    // 20.1: pul maydonlarida double bo'lmasin
    @ArchTest
    static final ArchRule pul_double_bilan_saqlanmaydi =
            noFields().that().haveNameMatching(".*(amount|price|total|fee|balance).*")
                    .should().haveRawType(double.class)
                    .orShould().haveRawType(Double.class);

    // 25.1: Optional maydon bo'lmasin
    @ArchTest
    static final ArchRule optional_maydon_bolmaydi =
            noFields().should().haveRawType(Optional.class);

    // 26.10: Lombok @Data taqiqlangan
    @ArchTest
    static final ArchRule lombok_data_taqiqlangan =
            noClasses().should().beAnnotatedWith("lombok.Data");

    // 2.4 va arxitektor 4.2: ma'nosiz sinf qo'shimchalari
    @ArchTest
    static final ArchRule manosiz_sinf_nomlari =
            noClasses().should().haveSimpleNameEndingWith("Manager")
                    .orShould().haveSimpleNameEndingWith("Helper")
                    .orShould().haveSimpleNameEndingWith("Info");

    // 26.1: field injection taqiqlangan
    @ArchTest
    static final ArchRule maydon_inyeksiyasi_taqiqlangan =
            noFields().should().beAnnotatedWith("org.springframework.beans.factory.annotation.Autowired");

    // 22.3: Instant.now() biznes kodida chaqirilmaydi, Clock ishlatiladi
    @ArchTest
    static final ArchRule vaqt_clock_orqali_olinadi =
            noClasses().that().resideInAPackage("..domain..")
                    .should().callMethod(Instant.class, "now");
}
```

Mavzuning to'liq yozuvi testlash qo'llanmasidagi [arxitektura testlari va kod sifati darvozalari](../testing/14-arxitektura-testlari-va-kod-sifati.md#142-archunit-asoslari) bo'limida; bu yerda faqat kod shakli nuqtai nazari.

## 42.5 Maxsus lint qoidasi yozish

Review da bir xil izoh har haftada qaytsa, u qoidaga aylanishi kerak ([arxitektor hujjatidagi](../architect/README.md) standart o'rnatish bo'limi). ArchUnit ko'p holatni qoplaydi, lekin ba'zi qoidalar AST darajasini talab qiladi - bunda Error Prone ning maxsus tekshiruvi yoziladi.

```java
// Error Prone maxsus qoidasi: log'da satr birlashtirish taqiqlangan (29.1)
@BugPattern(
        summary = "SLF4J xabarida satr birlashtirish: {} placeholder ishlatilsin",
        severity = ERROR,
        link = "docs/clean-code.md#291")
public class NoStringConcatInLog extends BugChecker implements MethodInvocationTreeMatcher {

    private static final Matcher<ExpressionTree> LOG_CALL =
            instanceMethod().onDescendantOf("org.slf4j.Logger")
                    .namedAnyOf("trace", "debug", "info", "warn", "error");

    @Override
    public Description matchMethodInvocation(MethodInvocationTree tree, VisitorState state) {
        if (!LOG_CALL.matches(tree, state)) return NO_MATCH;
        ExpressionTree first = tree.getArguments().isEmpty() ? null : tree.getArguments().get(0);
        if (first instanceof BinaryTree binary && binary.getKind() == Kind.PLUS) {
            return describeMatch(tree);
        }
        return NO_MATCH;
    }
}
```

Shu yo'lning ikkinchi ishlatilishi annotatsiyalarga tegishli. Annotatsiya o'zining qo'llanish shartini to'liq ifodalay olmaydi: `@Target(ElementType.METHOD)` annotatsiyani metodga cheklaydi, lekin "faqat parametrsiz statik metodda" kabi shartni kompilyator majburlay olmaydi, chunki bunday shartni annotatsiya e'lonida yozib bo'lmaydi. Natijada annotatsiya noto'g'ri joyga qo'yilsa, xato kompilyatsiyada emas, ish vaqtida yoki umuman chiqmaydi.

Yechim shu bo'limdagi bilan bir xil: shartni asbobga yozish. Ikki variant bor va tanlov shartning qayerda ko'rinishiga qarab qilinadi. Shart faqat annotatsiya e'lonidan kelib chiqsa va annotatsiyani kutubxona sifatida tarqatayotgan bo'lsangiz, `javax.annotation.processing` API si bilan annotation processor yoziladi: u kompilyatsiya vaqtida ishlaydi va shartni buzgan ishlatishga kompilyator xatosi beradi, ya'ni annotatsiya bilan birga tarqaladi. Shart kod bazasining o'z konvensiyasi bo'lsa, Error Prone tekshiruvi yoki ArchUnit qoidasi (42.4) arzonroq chiqadi, chunki u annotatsiya egasi bo'lishni talab qilmaydi.

## 42.6 Qoidani joriy qilish tartibi: ogohlantirish, keyin xato

Yangi qoidani darhol xato darajasida yoqish mavjud kod bazasida yuzlab xato beradi va jamoa uni o'chiradi. Ishlaydigan tartib bosqichli.

| Bosqich | Harakat |
|---|---|
| 1 | Qoidani ogohlantirish darajasida yoqib, sonini o'lchash |
| 2 | Yangi kod uchun xato, mavjud kod uchun ogohlantirish ("clean as you code") |
| 3 | Mavjud buzilishlarni bosqichma-bosqich tuzatish, sonini kuzatish |
| 4 | Son nolga yetganda qoidani xato darajasiga ko'tarish |
| 5 | Qoida sababini hujjatda yozib qo'yish ([48-bob](48-tezkor-malumotnoma-qoidalar-va-tekshiruv.md)) |

Ikkinchi bosqich eng muhim: Sonar ning "new code" tushunchasi ([SonarQube hujjatidagi](../sonarqube/README.md) "clean as you code" va yangi kod bo'limi) shu yondashuvni to'g'ridan-to'g'ri qo'llab-quvvatlaydi.

**Qoida sonining o'zi narx.** Bosqichli tartib "qoidani qanday yoqish" ga javob beradi; undan oldin turadigan savol - **bu qoida umuman kerakmi**. Google ning uslub ko'rsatmasidagi birinchi printsipi: qoida o'z vaznini tortishi kerak. Har yangi qoida tashkilotdagi barcha muhandisga o'rganish va unga moslashish xarajati qo'shadi. Qoidalar ko'paygan sari ularning hammasini yozish paytida esda tutish qiyinlashadi, yangi odamni o'rgatish ham qiyinlashadi, qoidalar to'plamini saqlash ham qimmatlashadi.

Shundan ikki amaliy qoida chiqadi:

- **O'z-o'zidan ravshan narsa uchun qoida yozilmaydi.** Google ning C++ ko'rsatmasida `goto` ni taqiqlovchi qoida yo'q, chunki C++ muhandislari uni o'zi ishlatmaydi va qoida qo'shish ortiqcha yuk bo'lardi. Uslub ko'rsatmasi yuridik hujjat emas: aniq taqiqlanmagan narsa ruxsat etilgan degani emas.
- **Bir-ikki odam xato qilayotgan narsa uchun qoida yozilmaydi.** Hammaning esida tutishi kerak narsalar ro'yxatini uzaytirish bu holatda o'zini oqlamaydi; to'g'ri yo'l - o'sha ikki odam bilan gaplashish.

Jamoa ro'yxatini tekshirish usuli oddiy: har qoida uchun "bu qoidani bilmagan odam qanday xato qiladi va bu xato oxirgi bir yilda nechta marta sodir bo'ldi" savoliga javob yozib ko'rish. Javob yo'q bo'lsa, qoida ro'yxatdan chiqadi.

## 42.7 False positive va bostirishni hujjatlashtirish

Har bir statik tahlil vositasi noto'g'ri xabar beradi va bostirish (`@SuppressWarnings`) kerak bo'ladi. Qoida: bostirish har doim **izoh bilan** va eng kichik qamrovda bo'ladi (23.7).

```java
// yaxshi: qamrov torroq, sabab yozilgan, qoida nomi aniq
@SuppressWarnings("unchecked")   // JPA native query Object[] qaytaradi, mapping qo'lda tekshirilgan
private List<SettlementRow> mapRows(Query query) { ... }

// yomon: butun sinf uchun, sababsiz
@SuppressWarnings("all")
class SettlementImporter { ... }
```

Bostirishlar sonini CI da o'lchash kerak: u o'sib borsa, qoida noto'g'ri sozlangan yoki jamoa unga ishonmaydi.

```bash
# Bostirishlar ro'yxati va soni: o'sishini kuzatish
grep -rn "@SuppressWarnings" src/main/java | wc -l
grep -rn "@SuppressWarnings" src/main/java | grep -v "//" | head    # izohsizlarni topish
```

## 42.8 Amalda qo'llash

- [ ] `-Xlint:all -Werror` ni yoqib, chiqqan ogohlantirishlarni ro'yxatlab bosqichma-bosqich tuzating.
- [ ] Error Prone ni build ga qo'shib, 42.2 jadvalidagi qoidalarni `ERROR` darajasiga ko'taring.
- [ ] NullAway ni yoqib, paketlarga `@NullMarked` qo'shishni bosqichma-bosqich boshlang.
- [ ] Checkstyle, SpotBugs va PMD rollarini ajratib, takrorlangan qoidalarni o'chiring.
- [ ] 42.4 dagi ArchUnit qoidalarini loyihaga moslab qo'shing va CI da ishga tushiring.
- [ ] Review da takrorlanadigan uch izohni tanlab, ularni ArchUnit yoki maxsus qoidaga aylantiring.
- [ ] Yangi qoidalarni 42.6 dagi besh bosqichli tartib bo'yicha joriy qiling.
- [ ] `@SuppressWarnings` sonini o'lchab, izohsizlarini tuzatib, o'sishini CI da kuzatib turing.

## Manbalar

- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 20-bob ("Compiler Integration") - kompilyator darajasida faqat bajarilishi mumkin, amalda yolg'on pozitiv bermaydigan va to'g'rilikka tegishli tekshiruvlarni xato qilib yoqish, yangi tekshiruvdan oldin mavjud buzilishlarni tozalash, hamda kompilyator ogohlantirishi chiqarilmasligi (yo xato, yo ko'rsatilmaydi). Bu nashrning nusxasida barqaror bet raqami yo'q, shuning uchun bob va bo'lim nomi ko'rsatilgan
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 8-bob ("Rules Must Pull Their Weight") - har yangi qoidaning barcha muhandisga o'rganish xarajati qo'shishi, o'z-o'zidan ravshan narsa uchun qoida yozilmasligi (`goto` misoli) va bir-ikki odam xato qilayotgan narsa uchun qoida qo'shish masshtablanmasligi. Bu nashrning nusxasida barqaror bet raqami yo'q, shuning uchun bob va bo'lim nomi ko'rsatilgan
- [SpotBugs, hujjat](https://raw.githubusercontent.com/spotbugs/spotbugs/6fc14ff38f4ebfbb4457caaa6df9a0ddd23a18c6/docs/index.rst) - bytecode asosidagi tahlil va qoida toifalari
- [PIT, README](https://raw.githubusercontent.com/hcoles/pitest/f7fe5adfa5fb6e727c12d2403a48f5e4e9dd2fc6/README.md) - mutatsiya testlash va qamrov bilan farqi
- [ArchUnit, README](https://raw.githubusercontent.com/TNG/ArchUnit/a0640ffa3ea5806c4fbab0dfbd29e363646d0fa3/README.md) - arxitektura qoidasini test sifatida yozish
- Joshua Bloch, *Effective Java* 3rd, Item 39 (181-bet) - annotatsiya bilan ifodalanmaydigan shartni ("faqat parametrsiz statik metodda") kompilyator majburlay olmasligi va buning uchun annotation processor yozish kerakligi
- ESLATMA: annotation processor bilan Error Prone yoki ArchUnit o'rtasidagi tanlov sharti (shart annotatsiya e'lonidanmi yoki kod bazasining konvensiyasidanmi kelib chiqadi) korpus qo'shimchasi

---

[&larr; 41. O'zgarishni kiritish jarayoni: kichik qadamlar](41-ozgarishni-kiritish-jarayoni-kichik-qadamlar.md) · [Mundarija](README.md) · [43. Professional mas'uliyat &rarr;](43-professional-masuliyat.md)
