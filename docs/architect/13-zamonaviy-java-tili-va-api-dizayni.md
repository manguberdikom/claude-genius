<!-- doc: architect | chapter: 13 | part: II. Java chuqur bilim -->

[Kod yozadigan arxitektorning miyyasi](../../README.md) / [Arxitektor miyyasi](README.md)

# 13. Zamonaviy Java tili va API dizayni (Modern Java and API Design)

<details>
<summary>Bu bobdagi 12 bo'lim</summary>

- [13.1 Record: qachon ishlatish, qachon oddiy sinf kerak](#131-record-qachon-ishlatish-qachon-oddiy-sinf-kerak)
- [13.2 Sealed interface va pattern matching bilan to'liq qamrovli tanlov](#132-sealed-interface-va-pattern-matching-bilan-toliq-qamrovli-tanlov)
- [13.3 `switch` ifodasi va deconstruction pattern](#133-switch-ifodasi-va-deconstruction-pattern)
- [13.4 Text block, `var` va o'qilishi: foyda va chegara](#134-text-block-var-va-oqilishi-foyda-va-chegara)
- [13.5 Optional ni to'g'ri ishlatish: qaytish qiymati, maydon emas](#135-optional-ni-togri-ishlatish-qaytish-qiymati-maydon-emas)
- [13.6 Stream API: qachon foyda, qachon oddiy sikl tushunarliroq](#136-stream-api-qachon-foyda-qachon-oddiy-sikl-tushunarliroq)
- [13.7 Istisnolar dizayni: tekshiriladigan va tekshirilmaydigan, o'z ierarxiyangiz](#137-istisnolar-dizayni-tekshiriladigan-va-tekshirilmaydigan-oz-ierarxiyangiz)
- [13.8 Kutubxona API si dizayni: kirish nuqtasi kam, nom aniq, standart qiymat xavfsiz](#138-kutubxona-api-si-dizayni-kirish-nuqtasi-kam-nom-aniq-standart-qiymat-xavfsiz)
- [13.9 Orqaga moslik: metod qo'shish, nomini o'zgartirish, deprecate qilish siyosati](#139-orqaga-moslik-metod-qoshish-nomini-ozgartirish-deprecate-qilish-siyosati)
- [13.10 Null xavfsizligi: annotatsiyalar va chegaraviy tekshiruv](#1310-null-xavfsizligi-annotatsiyalar-va-chegaraviy-tekshiruv)
- [13.11 Java versiyalari: LTS tanlash va yangilanish strategiyasi](#1311-java-versiyalari-lts-tanlash-va-yangilanish-strategiyasi)
- [13.12 Amalda qo'llash](#1312-amalda-qollash)

</details>



Java 17 dan 25 gacha til shunchalik o'zgardi ki, eski uslubda yozilgan kod endi texnik qarz bo'lib qoldi. Record, sealed interface va pattern matching birgalikda ma'lumot modelini kompilyator tekshiradigan shaklga keltiradi. Arxitektor uchun bu yerdagi savol "yangi sintaksis chiroylimi" emas, balki "qaysi xato kompilyatsiya vaqtida tutiladi va qaysi biri production da tutiladi". Bu bobda til imkoniyatlari va API dizayni qarorlari aynan shu mezon bilan ko'rib chiqiladi.

## 13.1 Record: qachon ishlatish, qachon oddiy sinf kerak

Record o'zgarmas ma'lumot tashuvchisi uchun mo'ljallangan. Kompilyator unga konstruktor, `equals`, `hashCode`, `toString` va komponent accessor larini o'zi yozadi. `equals` barcha komponentlar ustidan hisoblanadi, shuning uchun record ni `HashMap` kaliti qilib ishlatish xavfsiz. Record yashirin tarzda `final`, boshqa sinfdan meros olmaydi, maydonlari `final`.

Validatsiyani compact konstruktorda qilish kerak. Bu yagona joy, chunki record o'zgarmas, demak yaroqsiz holat hech qachon yuzaga kelmaydi.

```java
public record PaymentRequest(
        String orderId,
        BigDecimal amount,
        Currency currency,
        Instant requestedAt) {

    public PaymentRequest {
        // compact konstruktor: validatsiya shu yerda, boshqa joyda emas
        Objects.requireNonNull(orderId, "orderId null bo'lmaydi");
        Objects.requireNonNull(currency, "currency null bo'lmaydi");
        if (amount == null || amount.signum() <= 0) {
            throw new IllegalArgumentException("summa musbat bo'lishi kerak: " + amount);
        }
        // BigDecimal scale ni normallashtiramiz, aks holda equals yolg'on ishlaydi:
        // 10.0 va 10.00 BigDecimal da teng emas
        amount = amount.setScale(currency.getDefaultFractionDigits(), RoundingMode.UNNECESSARY);
    }

    public boolean isLargePayment() {
        return amount.compareTo(new BigDecimal("10000")) >= 0;
    }
}
```

Oddiy sinf quyidagi hollarda kerak. Birinchi, JPA entity: Hibernate argumentsiz konstruktor, o'zgaruvchan maydon va proxy uchun ochiq sinf talab qiladi, record bunga yaramaydi. Ikkinchi, identity semantikasi kerak bo'lsa: buyurtma entity si ID bo'yicha teng bo'lishi kerak, barcha maydonlari bo'yicha emas. Uchinchi, komponentlar soni oltitadan oshsa va ularning yarmi ixtiyoriy bo'lsa: bu yerda builder li oddiy sinf o'qilishi yaxshiroq. To'rtinchi, keyinchalik maydon qo'shilishi kutilayotgan ommaviy API da record komponentlari tartibi konstruktor imzosining bir qismi, shuning uchun har bir qo'shimcha binary moslikni buzadi.

Record DTO va read model uchun ideal. Spring Data JPA interface va sinf asosidagi projection larda record ni to'g'ridan to'g'ri qabul qiladi, JPQL da `select new` konstruktor ifodasi ham ishlaydi. Jackson record ni 2.12 dan beri komponent nomlari bo'yicha serialize va deserialize qiladi, qo'shimcha annotatsiya shart emas.

## 13.2 Sealed interface va pattern matching bilan to'liq qamrovli tanlov

Sealed ierarxiya kompilyatorga "bu turning variantlari aynan shular" deb aytadi. Natijada `switch` da `default` shoxi kerak emas, va yangi variant qo'shilganda uni unutgan har bir `switch` kompilyatsiya xatosi beradi. Bu to'lov natijasi, buyurtma holati, hisobot formati kabi yopiq to'plamlar uchun eng kuchli vositalardan biri.

```java
public sealed interface PaymentResult {

    record Captured(String providerRef, BigDecimal amount) implements PaymentResult {}
    record Pending(String providerRef, Duration retryAfter) implements PaymentResult {}
    record Declined(DeclineReason reason, String providerMessage) implements PaymentResult {}
    record ProviderUnavailable(Duration retryAfter) implements PaymentResult {}
}

// Yangi variant qo'shilsa, bu switch kompilyatsiya qilinmaydi: default yo'q
String auditLine(PaymentResult result) {
    return switch (result) {
        case Captured(var ref, var amount) ->
                "olindi ref=" + ref + " summa=" + amount;
        case Pending(var ref, var retryAfter) ->
                "kutilmoqda ref=" + ref + " qayta=" + retryAfter.toSeconds() + "s";
        case Declined(DeclineReason.INSUFFICIENT_FUNDS, var msg) ->
                "mablag' yetmadi: " + msg;
        case Declined(var reason, var msg) ->
                "rad etildi " + reason + ": " + msg;
        case ProviderUnavailable(var retryAfter) ->
                "provayder ishlamaydi, qayta=" + retryAfter.toSeconds() + "s";
    };
}
```

`permits` ro'yxatini yozmasa ham bo'ladi, agar barcha implementatsiya bir faylda yoki bir paketda bo'lsa. Nested record lar shu sababli ko'p qulay: butun ierarxiya bitta faylda ko'rinadi.

Muhim chegara: sealed ierarxiya sizning kodingizda bo'lishi kerak. Agar siz kutubxona chiqarayotgan bo'lsangiz, sealed interface mijozga yangi variant qo'shishga ruxsat bermaydi. Bu ataylab qilinadigan qaror. Agar kengaytirish nuqtasi kerak bo'lsa, oddiy interface qoldiring va visitor o'rnini saqlang. Agar variantlar sizda to'liq nazoratda bo'lsa, sealed ni tanlang, chunki u har bir yangi holatni qamrab olishga majbur qiladi.

## 13.3 `switch` ifodasi va deconstruction pattern

`switch` endi ifoda, ya'ni qiymat qaytaradi. Bu uch narsani beradi. Birinchi, `->` shoxlari fall through qilmaydi, shuning uchun unutilgan `break` dan kelib chiqadigan xatolar yo'qoladi. Ikkinchi, har bir shox qiymat qaytarishi shart, demak kompilyator to'liqlikni tekshiradi. Uchinchi, record pattern bilan ma'lumotni darhol ochib olish mumkin, alohida cast va getter chaqiruvlari kerak emas.

`when` guard shart ni pattern ustiga qo'yadi. Guard tartibi muhim: aniqroq shart avval yozilishi kerak, aks holda kompilyator "pattern dominated" xatosini beradi.

```java
// Ombor qoldig'i bo'yicha qaror: pattern + guard, hech qanday if-else zinapoyasi yo'q
sealed interface StockEvent {
    record Reserved(String sku, int qty) implements StockEvent {}
    record Released(String sku, int qty) implements StockEvent {}
    record Recounted(String sku, int counted, int expected) implements StockEvent {}
}

int delta(StockEvent event) {
    return switch (event) {
        case null -> 0;                                  // pattern switch da null ni aniq yozish mumkin
        case Reserved(_, int qty) when qty > 1000 -> -qty; // katta rezerv, alohida audit
        case Reserved(_, int qty) -> -qty;
        case Released(_, int qty) -> qty;
        case Recounted(_, int counted, int expected) -> counted - expected;
    };
}
```

Ikki tuzoqni bilib turish kerak. Birinchi, `case null` yozilmasa pattern switch `NullPointerException` tashlaydi. Eski `switch` ham shunday qilardi, lekin endi `case null` ni ochiq yozish imkoni bor va u niyatni ko'rsatadi. Ikkinchi, sealed ierarxiya alohida kompilyatsiya qilingan modul da o'zgarsa, eski `switch` runtime da `MatchException` beradi. Shuning uchun sealed ierarxiya va uni ishlatuvchi kod bir deploy birligida bo'lishi afzal. Nomsiz pattern `_` Java 22 dan boshlab to'liq qo'llanadi va ishlatilmaydigan komponentni ko'rsatishga xizmat qiladi.

## 13.4 Text block, `var` va o'qilishi: foyda va chegara

Text block SQL va JSON ni kodda o'qiladigan qiladi. Kompilyator chap tomondagi umumiy bo'shliqni o'zi olib tashlaydi, chegarani yopuvchi `"""` ning joylashuvi belgilaydi. Satr oxiridagi `\` yangi qatorni bosadi, `\s` esa kerakli bo'shliqni saqlab qoladi.

```java
// Hisobot so'rovi: text block bilan SQL diff da o'qiladi va DBA bilan muhokama qilinadi
private static final String MONTHLY_REVENUE = """
        select date_trunc('month', p.captured_at) as month,
               p.currency,
               sum(p.amount)                      as total,
               count(*)                           as payments
        from payment p
        where p.status = 'CAPTURED'
          and p.captured_at >= ?
          and p.captured_at <  ?
        group by 1, 2
        order by 1 desc
        """;

// var: o'ng tomon turni aytib turganda foydali
var byCurrency = new HashMap<Currency, BigDecimal>();      // tur bir marta yozildi
var rows = jdbcTemplate.query(MONTHLY_REVENUE, mapper, from, to);

// var: bu yerda zarar, chunki o'qiyotgan odam turni bilmaydi
var result = service.process(request);                     // nima qaytadi, noma'lum
```

`var` qoidasi oddiy. O'ng tomonda konstruktor yoki fabrika chaqiruvi bo'lib, tur nomi ko'rinib turgan bo'lsa `var` ishlatiladi. Metod chaqiruvining natijasi bo'lsa va tur nomi ko'rinmasa, turni ochiq yozish kerak. `var` ommaviy API imzosida ishlatilmaydi, u faqat lokal o'zgaruvchi. Diamond operator bilan birga `var x = new ArrayList<>()` yozsangiz `ArrayList<Object>` chiqadi, bu deyarli har doim xato.

Text block ning chegarasi: u shablon mexanizmi emas. Ichida o'zgaruvchi almashtirish uchun `formatted` ishlating. Foydalanuvchi kiritgan qiymatni SQL text block ichiga string sifatida ulamang, bu SQL injection. Parametr placeholder ishlating.

## 13.5 Optional ni to'g'ri ishlatish: qaytish qiymati, maydon emas

`Optional` bitta masalani hal qilish uchun yaratilgan: metod qiymat qaytarmasligi mumkinligini imzoda bildirish. U maydon turi emas, konstruktor parametri emas, kolleksiya elementi emas. `Optional` `Serializable` ni implement qilmaydi, shuning uchun entity maydoni yoki cache ga yoziladigan DTO maydoni sifatida ishlatilmaydi.

```java
// To'g'ri: repository topilmaslikni imzoda bildiradi
Optional<Payment> findByProviderRef(String providerRef);

// To'g'ri: orElseThrow domen istisnosi bilan
Payment payment = payments.findByProviderRef(ref)
        .orElseThrow(() -> new PaymentNotFoundException(ref));

// To'g'ri: zanjir, hech qanday isPresent yo'q
String country = payments.findByProviderRef(ref)
        .map(Payment::payer)
        .flatMap(Payer::billingAddress)
        .map(Address::countryCode)
        .orElse("UZ");

// Xato: Optional maydon. Serializable emas, JPA uni map qilmaydi, xotira ortadi
// private Optional<String> note;

// Xato: get() tekshiruvsiz. NoSuchElementException stack trace si foydasiz
// Payment p = payments.findByProviderRef(ref).get();

// Xato: Optional parametr. Chaqiruvchi Optional.of qurishga majbur
// void notify(Optional<String> email) { ... }
```

Bo'sh kolleksiya qaytarish kerak bo'lganda `Optional<List<T>>` yozmang. Bo'sh `List` o'zi "yo'q" ni anglatadi. `orElse` va `orElseGet` farqi muhim: `orElse` argumentini har doim hisoblaydi, hatto qiymat bor bo'lsa ham. Agar standart qiymat hisoblanishi arzon bo'lmasa, `orElseGet` ishlating. Oqimda ishlaganda `stream().flatMap(Optional::stream)` bo'sh qiymatlarni toza filtrlaydi.

## 13.6 Stream API: qachon foyda, qachon oddiy sikl tushunarliroq

Stream deklarativ transformatsiya uchun yaxshi: filtrlash, map qilish, guruhlash, jamlash. U bitta ifodada niyatni ko'rsatadi va oraliq o'zgaruvchilarni yo'q qiladi. Lekin stream ning uchta aniq zaifligi bor: debug qilish qiyin, `break` ekvivalenti yo'q, va stack trace o'qilmas holga keladi.

```java
// Stream foydali: guruhlash va jamlash bir ifodada
Map<Currency, BigDecimal> totalByCurrency = payments.stream()
        .filter(p -> p.status() == CAPTURED)
        .collect(Collectors.groupingBy(
                Payment::currency,
                Collectors.reducing(BigDecimal.ZERO, Payment::amount, BigDecimal::add)));

// Sikl tushunarliroq: bir nechta o'zgaruvchi, erta chiqish va xatolar yig'ilishi
List<String> rejected = new ArrayList<>();
BigDecimal running = BigDecimal.ZERO;
for (Payment p : payments) {
    if (running.compareTo(dailyLimit) >= 0) {
        break;                                  // stream da bunga toza ekvivalent yo'q
    }
    try {
        running = running.add(provider.capture(p));   // checked exception stream ichida og'riq
    } catch (ProviderException e) {
        rejected.add(p.orderId());
    }
}
```

Qoida: agar lambda ichida `try/catch` paydo bo'lsa yoki tashqi o'zgaruvchi o'zgarishi kerak bo'lsa, sikl yozing. Agar transformatsiya toza bo'lsa, stream yozing.

`parallelStream` ni ehtiyotkorlik bilan ishlating. U umumiy `ForkJoinPool.commonPool` da ishlaydi va butun JVM uchun umumiy. Bloklanadigan I/O ni parallel stream ga bermang. Foyda odatda element soni o'n minglardan oshganda va amal sof CPU bo'lganda ko'rinadi. Virtual thread davrida I/O ni parallellashtirish uchun to'g'ri vosita executor, parallel stream emas. Java 24 da `Stream.gather` va `Gatherers` to'liq qo'shildi, u oynali va holatli transformatsiyalarni standart usulda yozish imkonini beradi.

## 13.7 Istisnolar dizayni: tekshiriladigan va tekshirilmaydigan, o'z ierarxiyangiz

Tekshiriladigan istisno chaqiruvchi haqiqatan ham tiklanish harakati qila oladigan holat uchun. Tekshirilmaydigan istisno programma xatosi yoki tiklanmaydigan infratuzilma nosozligi uchun. Spring ning o'zi bu tanlovni allaqachon qilgan: `DataAccessException` ierarxiyasi butunlay `RuntimeException` dan meros oladi, chunki SQL xatosidan chaqiruvchi deyarli hech narsa qila olmaydi.

```java
// Domen ierarxiyasi: bitta ildiz, barqaror xato kodi, kontekst maydonlari
public abstract class PaymentException extends RuntimeException {
    private final String code;          // API javobiga chiqadigan barqaror kod
    private final String orderId;

    protected PaymentException(String code, String orderId, String message, Throwable cause) {
        super(message, cause);
        this.code = code;
        this.orderId = orderId;
    }
    public String code() { return code; }
    public String orderId() { return orderId; }
}

public final class InsufficientFundsException extends PaymentException {
    public InsufficientFundsException(String orderId) {
        super("PAYMENT_INSUFFICIENT_FUNDS", orderId, "mablag' yetarli emas: " + orderId, null);
    }
}

// Qayta urinish mumkinligini tur bilan bildirish: resilience qatlami shu belgiga qaraydi
public interface Retryable { Duration retryAfter(); }
```

Uch amaliy qoida. Birinchi, xato kodini `enum` yoki konstanta sifatida saqlang va uni API kontraktining bir qismi deb bilib, hech qachon o'zgartirmang. Xato matni o'zgarishi mumkin, kod o'zgarmasligi kerak. Ikkinchi, `cause` ni hech qachon yo'qotmang: `throw new MyException(msg)` yozib asl istisnoni tashlab ketish eng ko'p uchraydigan diagnostika yo'qotishi. Uchinchi, boshqaruv oqimi uchun istisno ishlatmang. Agar holat kutilgan bo'lsa, sealed natija turi qaytaring, yuqoridagi `PaymentResult` kabi.

Yuqori chastotali kodda stack trace yig'ish qimmat. Kutilgan, soniyada minglab marta yuz beradigan holat uchun `super(message, cause, false, false)` konstruktori bilan suppression va writableStackTrace ni o'chirish mumkin. Bu optimizatsiyani faqat o'lchov ko'rsatganda qiling.

## 13.8 Kutubxona API si dizayni: kirish nuqtasi kam, nom aniq, standart qiymat xavfsiz

Ichki kutubxona chiqarayotganda eng muhim qaror nimani ommaviy qilish emas, nimani ommaviy qilmaslik. Har bir `public` tur kelajakdagi majburiyat. Bir kirish nuqtasi, bir nechta `sealed` yoki `final` qiymat turi, qolgani `package private`.

```java
// Bitta kirish nuqtasi, qolgan hammasi paket ichida yashiringan
public final class ReportExporter {

    public static Builder builder() { return new Builder(); }

    public static final class Builder {
        // Standart qiymatlar xavfsiz tomonga qaragan: kichik sahifa, qisqa timeout
        private int pageSize = 1_000;
        private Duration timeout = Duration.ofSeconds(30);
        private boolean includePii = false;        // standart: PII yo'q

        public Builder pageSize(int pageSize) {
            if (pageSize < 1 || pageSize > 50_000) {
                throw new IllegalArgumentException("pageSize 1..50000 oralig'ida");
            }
            this.pageSize = pageSize;
            return this;
        }
        public Builder timeout(Duration timeout) { this.timeout = timeout; return this; }
        public Builder includePii(boolean includePii) { this.includePii = includePii; return this; }
        public ReportExporter build() { return new ReportExporter(this); }
    }
}
```

Nom berishda uch qoida. Birinchi, `get` prefiksi faqat haqiqiy accessor uchun. Hisoblash qiladigan metod `calculateMonthlyTotal` deb nomlanadi, chunki chaqiruvchi uning qimmatligini bilishi kerak. Ikkinchi, bool parametr o'rniga `enum` bering. `export(true, false)` chaqiruvni o'qib bo'lmaydi, `export(Format.CSV, Pii.EXCLUDE)` o'qiladi. Uchinchi, vaqt birligini nomga yozmang, `Duration` qabul qiling. `timeoutMs` xato birlik berish xatosini ochiq qoldiradi.

Standart qiymat har doim xavfsiz tomonga qarashi kerak. PII standart holda o'chirilgan, retry standart holda o'chirilgan yoki chegaralangan, timeout standart holda cheksiz emas. Mijoz xavfli rejimni ongli ravishda yoqadi.

| Mezon | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Ma'lumot modeli | Hamma joyda mutable POJO, setter bilan | Record, compact konstruktorda validatsiya, yaroqsiz holat mavjud emas |
| Variantlar to'plami | `String type` maydoni va `if-else` zinapoyasi | Sealed interface va to'liq qamrovli `switch` ifodasi |
| Yo'qlik | Null qaytarish va Javadoc da eslatma | `Optional` qaytish qiymati, maydon emas, parametr emas |
| Istisnolar | Hamma joyda `RuntimeException` yoki `Exception` | Bitta domen ildizi, barqaror xato kodi, `cause` saqlanadi |
| API sirti | Hamma sinf `public`, "kerak bo'lar" | Bir kirish nuqtasi, qolgani paket ichida |
| Standart qiymatlar | Cheksiz timeout, cheksiz sahifa | Chegaralangan va xavfsiz standart, xavfli rejim ongli yoqiladi |
| Null kontrakti | Hech qanday annotatsiya, har joyda tekshiruv | `@NullMarked` paket, chegarada tekshiruv, build da statik tahlil |
| Metod o'chirish | To'g'ridan to'g'ri o'chirish, minor versiyada | `@Deprecated(since, forRemoval)`, ikki relizlik oyna, `japicmp` darvozasi |
| Java versiyasi | "Ishlayapti, tegmaymiz" | LTS da turish, har oraliq relizni CI da sinash |
| Stream va sikl | Hamma narsa stream, lambda ichida `try/catch` | Toza transformatsiya stream, holatli va erta chiqadigan mantiq sikl |

## 13.9 Orqaga moslik: metod qo'shish, nomini o'zgartirish, deprecate qilish siyosati

Binary moslik va source moslik ikki xil narsa. Interface ga metod qo'shsangiz, source moslik buziladi, chunki implementatsiya qiluvchilar kompilyatsiya qilinmaydi. `default` metod qo'shsangiz ikkisi ham saqlanadi. Record ga komponent qo'shsangiz konstruktor imzosi o'zgaradi va eski kompilyatsiya qilingan mijoz `NoSuchMethodError` oladi.

Metod nomini "o'zgartirish" degan amal yo'q. Yangi nom bilan metod qo'shiladi, eskisi eski nomda qoladi va `@Deprecated(since = "...", forRemoval = true)` bilan belgilanadi. Eski metod yangisiga delegatsiya qiladi. Olib tashlash faqat major versiyada bo'ladi.

```bash
# Build da moslikni darvoza qilib qo'yish
# japicmp: oldingi reliz bilan binary farqni tekshiradi, buzilish bo'lsa build yiqiladi
mvn -q com.github.siom79.japicmp:japicmp-maven-plugin:cmp

# jdeprscan: kodingiz JDK ning deprecated API sidan foydalanayotganini ko'rsatadi
jdeprscan --release 25 --for-removal target/report-exporter-2.4.0.jar

# jdeps: tasodifiy ichki paket bog'liqligini topadi
jdeps --multi-release 25 -summary target/report-exporter-2.4.0.jar
```

Deprecate siyosatini yozib qo'ying va unga rioya qiling. Amaliy shakl: belgilangan metod kamida ikki minor reliz yoki taxminan oltita oy yashaydi. Javadoc da `@deprecated` tegi o'rnini aniq ko'rsatadi, ya'ni "`exportCsv(Pii)` ni ishlating". Metrika qo'ying: eski metod chaqirilganda counter oshadi, shunda olib tashlashdan oldin uni hali kim ishlatayotganini bilasiz.

| Tuzoq | Nima bo'ladi | Yechim |
|---|---|---|
| Record ga yangi komponent qo'shish | Eski mijozda `NoSuchMethodError` | Yangi record turi chiqarish yoki builder li sinfga o'tish |
| Interface ga abstrakt metod qo'shish | Mijoz implementatsiyasi kompilyatsiya qilinmaydi | `default` metod qo'shish yoki yangi interface ajratish |
| `Optional` ni entity maydoni qilish | JPA map qilmaydi, serializatsiya yiqiladi | Maydon nullable, accessor `Optional` qaytaradi |
| `parallelStream` ichida bloklanadigan I/O | `commonPool` to'lib qoladi, butun JVM sekinlashadi | Alohida executor yoki virtual thread ishlatish |
| Sealed ierarxiyani alohida modulda o'zgartirish | Runtime da `MatchException` | Ierarxiya va iste'molchini bir deploy birligida saqlash |
| Pattern `switch` da `case null` yo'q | Kutilmagan `NullPointerException` | `case null` ni ochiq yozish yoki chegarada tekshirish |
| `var new ArrayList<>()` | Tur `ArrayList<Object>` bo'lib ketadi | Generic parametrni ochiq yozish |
| `orElse` ichida qimmat chaqiruv | Qiymat bor bo'lsa ham hisoblanadi | `orElseGet` ishlatish |
| Istisno `cause` sini tashlab ketish | Asl sabab log da yo'q, diagnostika imkonsiz | `cause` ni har doim konstruktorga uzatish |
| Xato matniga qarab mijoz mantiq yozishi | Matn o'zgarsa integratsiya yiqiladi | Barqaror xato kodi, matn faqat odam uchun |

## 13.10 Null xavfsizligi: annotatsiyalar va chegaraviy tekshiruv

Java da null xavfsizligini til bermaydi, shuning uchun uni annotatsiya va build darvozasi bilan quramiz. JSpecify 1.0 bugungi standart tanlov. `@NullMarked` ni paket yoki modul darajasida qo'ysangiz, o'sha doiradagi barcha tur ishlatilishi standart holda non null deb qabul qilinadi. Shundan keyin faqat istisnolarni, ya'ni `@Nullable` ni belgilash kifoya. Spring Framework 7 va Spring Boot 4 o'z API sida JSpecify ga o'tdi, shuning uchun ekosistemaga mos tanlov shu.

```java
// package-info.java: butun paket uchun non null standart
@NullMarked
package com.shop.payment.api;

import org.jspecify.annotations.NullMarked;
```

```java
@NullMarked
public final class PaymentFacade {

    // Parametr va qaytish qiymati standart holda non null
    public PaymentResult pay(PaymentRequest request, @Nullable String idempotencyKey) {
        // Chegaraviy tekshiruv: tashqi dunyodan kelgan qiymat faqat shu yerda tekshiriladi
        Objects.requireNonNull(request, "request");
        String key = idempotencyKey != null ? idempotencyKey : UUID.randomUUID().toString();
        return engine.execute(request, key);   // ichkarida endi null tekshiruvi yo'q
    }
}
```

Arxitektura qoidasi: null tekshiruvi tizim chegarasida bo'ladi. Chegara deganda controller, message listener, tashqi klient adapter va ommaviy facade tushuniladi. Chegaradan o'tgandan keyin ichki qatlamlar non null deb ishonadi va takroriy tekshiruv yozmaydi. Bu minglab keraksiz `if (x != null)` ni yo'q qiladi.

Annotatsiya o'z o'zidan hech narsa tekshirmaydi. Build ga statik tahlil qo'shish kerak. Error Prone ustidagi NullAway annotatsiyalarni o'qiydi va qoida buzilishini kompilyatsiya xatosiga aylantiradi. IDE inspeksiyasi ham shu annotatsiyalarni tushunadi, lekin IDE CI emas. Qoidani CI da majburlash kerak, aks holda u tavsiya bo'lib qoladi.

## 13.11 Java versiyalari: LTS tanlash va yangilanish strategiyasi

Java olti oyda bir reliz chiqaradi va Java 21 dan boshlab LTS har ikki yilda keladi. Amaldagi LTS lar: 17 (2021), 21 (2023), 25 (2025). Production da LTS da turish to'g'ri qaror, chunki oraliq relizlar faqat oltita oy yamoq oladi. Lekin "LTS da turish" degani oraliq relizlarni ko'rmaslik degani emas.

Praktik strategiya ikki trekli. Production trek LTS da. Ikkinchi trek CI da: nightly build eng yangi JDK da ham kompilyatsiya qilib, testlarni o'tkazadi. Shunda keyingi LTS ga o'tish ikki yillik katta loyiha emas, balki bir necha kunlik ish bo'ladi.

```yaml
# CI: production LTS plus kelgusi relizni kuzatuvchi trek
strategy:
  fail-fast: false
  matrix:
    java: [ 21, 25, 26-ea ]   # 21 production, 25 maqsad, 26-ea ogohlantirish uchun
steps:
  - uses: actions/setup-java@v4
    with:
      distribution: temurin
      java-version: ${{ matrix.java }}
  - run: mvn -B verify
```

```properties
# Maven: bytecode maqsadi va manba sintaksisi alohida boshqariladi
maven.compiler.release=21
# Kutubxona chiqarayotganda eng past qo'llanadigan versiyaga release qiling,
# chunki --release eski API dan tashqariga chiqishni kompilyatsiyada bloklaydi
maven.compiler.parameters=true
```

Yangilanish paytida uchta narsa ko'p muammo beradi. Birinchi, bytecode manipulyatsiya qiladigan kutubxonalar: ByteBuddy, ASM asosidagi agentlar va eski mock kutubxonalari yangi class file versiyasini tanimasligi mumkin, shuning uchun ularni avval ko'taring. Ikkinchi, JDK ichki API siga kirish: yangi relizlarda u qattiqroq yopiladi va `--add-opens` flaglari tobora kamroq ishlaydi. Uchinchi, GC standartining o'zgarishi: heap va pauza o'lchovlarini yangilanishdan keyin qaytadan oling, chunki eski tuning parametrlari yangi kollektorda ma'noni o'zgartiradi.

Qaror mezoni oddiy. Agar Spring Boot 3.x da bo'lsangiz, Java 17 minimal, lekin Java 21 virtual thread uchun amalda majburiy. Spring Boot 4.x va Spring Framework 7.x ham Java 17 ni minimal baseline deb oladi, shunga qaramay yangi loyihani Java 25 da boshlash to'g'ri, chunki keyingi ikki yil davomida yangilanish talab qilinmaydi.

## 13.12 Amalda qo'llash

- [ ] Loyihadagi barcha DTO va read model sinflarini ko'rib chiqing, mutable POJO larni record ga o'tkazing va validatsiyani compact konstruktorga yig'ing.
- [ ] `String type` yoki `int status` maydoni bilan boshqarilayotgan eng katta `if-else` zinapoyasini toping va uni sealed interface plus `switch` ifodasiga aylantiring.
- [ ] Barcha `Optional` maydonlarini va `Optional` parametrlarini grep bilan topib olib tashlang, `Optional` ni faqat qaytish qiymati sifatida qoldiring.
- [ ] `.get()` va `orElse` ichidagi qimmat chaqiruvlarni audit qiling, birinchisini `orElseThrow` ga, ikkinchisini `orElseGet` ga o'zgartiring.
- [ ] Domen istisnolari uchun bitta ildiz sinf va barqaror xato kodlari `enum` ini joriy qiling, `cause` yo'qotilayotgan joylarni tuzatib chiqing.
- [ ] Ommaviy paketlarga `package-info.java` da `@NullMarked` qo'ying va NullAway ni build darvozasi qilib yoqing.
- [ ] Kutubxona modullariga `japicmp` ni ulang va binary moslik buzilishini build yiqilishiga aylantiring, deprecate oynasini yozib hujjatlashtiring.
- [ ] CI matritsasiga production LTS dan tashqari keyingi JDK ni qo'shing va nightly build da uni ham sinaydigan qilib qo'ying.

---

[&larr; 12. Virtual threads, structured concurrency va scoped values](12-virtual-threads-structured-concurrency-va.md) · [Mundarija](README.md) · [14. JVM profiling va diagnostika: JFR, async-profiler, heap dump &rarr;](14-jvm-profiling-va-diagnostika-jfr-async.md)
