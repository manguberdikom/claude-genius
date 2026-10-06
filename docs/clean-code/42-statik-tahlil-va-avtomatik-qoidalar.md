<!-- doc: clean-code | chapter: 42 | part: XI. Kod bazasi va jarayon gigiyenasi -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: AI yozgan, inson tekshirmagan.

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

---

[&larr; 41. O'zgarishni kiritish jarayoni: kichik qadamlar](41-ozgarishni-kiritish-jarayoni-kichik-qadamlar.md) · [Mundarija](README.md) · [43. Professional mas'uliyat &rarr;](43-professional-masuliyat.md)
