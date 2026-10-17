<!-- doc: clean-code | chapter: 19 | part: VI. Xato bilan ishlash -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: tekshirilmoqda. Da'volar hali manbaga solishtirilmoqda.

# 19. Istisno mexanikasi va resurslar (Exception Mechanics and Resources)

<details>
<summary>Bu bobdagi 15 bo'lim</summary>

- [19.1 Stack trace ni yo'qotmaslik: wrap va rethrow](#191-stack-trace-ni-yoqotmaslik-wrap-va-rethrow)
- [19.2 Ko'p turni tutish va tutish tartibi](#192-kop-turni-tutish-va-tutish-tartibi)
- [19.3 `finally` ichidagi `return` va bostirilgan istisno](#193-finally-ichidagi-return-va-bostirilgan-istisno)
- [19.4 `try-with-resources` va `AutoCloseable`](#194-try-with-resources-va-autocloseable)
- [19.5 `InterruptedException` ni to'g'ri qayta tiklash](#195-interruptedexception-ni-togri-qayta-tiklash)
- [19.6 `Throwable`, `Error` va `OutOfMemoryError` siyosati](#196-throwable-error-va-outofmemoryerror-siyosati)
- [19.7 Log qilish yoki tashlash: ikkisini birga qilmaslik](#197-log-qilish-yoki-tashlash-ikkisini-birga-qilmaslik)
- [19.8 Assertion va `-ea`: qachon haqli](#198-assertion-va--ea-qachon-haqli)
- [19.9 `Objects.requireNonNull`, Guava `Preconditions`, Bean Validation](#199-objectsrequirenonnull-guava-preconditions-bean-validation)
- [19.10 Xato xabari matni: uch xil adresat](#1910-xato-xabari-matni-uch-xil-adresat)
- [19.11 Xato kodi katalogi va uni barqaror ushlash](#1911-xato-kodi-katalogi-va-uni-barqaror-ushlash)
- [19.12 Xatolik atomarligi: yiqilgan metod obyektni buzib qoldirmasligi](#1912-xatolik-atomarligi-yiqilgan-metod-obyektni-buzib-qoldirmasligi)
- [19.13 Fayl va yo'l bilan ishlash: `Path`, `Files` va kodirovka](#1913-fayl-va-yol-bilan-ishlash-path-files-va-kodirovka)
- [19.14 Offensive programming: development da qattiq, production da yumshoq yiqilish](#1914-offensive-programming-development-da-qattiq-production-da-yumshoq-yiqilish)
- [19.15 Amalda qo'llash](#1915-amalda-qollash)

</details>


Oldingi bobda xato bilan ishlashning qoidalari berildi. Bu bobda Java dagi mexanika: stack trace ni saqlash, tutish tartibi, `finally` tuzoqlari, `try-with-resources`, `InterruptedException`, assertion, va xato xabarining uch xil adresati.

## 19.1 Stack trace ni yo'qotmaslik: wrap va rethrow

Istisnoni qayta tashlashning to'g'ri yo'li - asl istisnoni **sabab** (cause) sifatida uzatish. Buni unutish diagnostikani imkonsiz qiladi: log da yangi istisnoning stack trace i turadi, asl xato qayerda bo'lganini ko'rsatmaydi.

```java
// yomon: sabab yo'qoldi, asl xato qayerda bo'lgani ko'rinmaydi
catch (SQLException e) {
    throw new SettlementException("baza xatosi");
}

// yomon: faqat xabar ko'chirilgan, stack trace yo'q
catch (SQLException e) {
    throw new SettlementException(e.getMessage());
}

// yaxshi: sabab saqlangan, kontekst qo'shilgan
catch (SQLException e) {
    throw new SettlementException(
            "to'lov %s uchun hisob-kitob yozib bo'lmadi".formatted(paymentId), e);
}
```

Agar istisnoni o'zgartirmasdan qayta tashlasangiz, `throw e;` yozing - yangi istisno yaratish stack trace ni almashtiradi.

## 19.2 Ko'p turni tutish va tutish tartibi

`catch` bloklari **xususiydan umumiyga** tartibda yozilishi kerak; teskari tartib kompilyatsiya xatosi beradi (erishilmaydigan blok). Agar bir necha tur bir xil qayta ishlansa, multi-catch ishlatiladi va bu takrorlanishni yo'qotadi.

```java
// yaxshi: multi-catch, takrorlanish yo'q
try {
    gateway.settle(payment);
} catch (SocketTimeoutException | ConnectException e) {
    throw new GatewayUnavailableException(payment.id(), e);
} catch (IOException e) {
    throw new GatewayCommunicationException(payment.id(), e);
}
```

Qoida: `catch (Exception e)` faqat eng tashqi chegarada (controller advice, scheduler, konsumer) haqli. Ichki kodda u aniq istisnolarni yashiradi va `NullPointerException` kabi kodi xatolarini biznes xatosi deb qayta ishlaydi.

## 19.3 `finally` ichidagi `return` va bostirilgan istisno

`finally` blokidagi `return` yoki `throw` asl istisnoni **jimgina yo'qotadi**. Bu Java dagi eng yashirin xato shakllaridan biri: xato bo'lgan, lekin metod normal qaytgan.

```java
// yomon: istisno yo'qoladi, metod 0 qaytaradi
int count() {
    try {
        throw new IllegalStateException("baza yopilgan");
    } finally {
        return 0;          // istisno bostirildi
    }
}

// yaxshi: finally faqat tozalash qiladi, return va throw yo'q
int count() {
    try {
        return repository.count();
    } finally {
        meter.recordCallCompleted();
    }
}
```

Error Prone `Finally` qoidasi va IDE inspeksiyasi shu xatoni topadi; uni CI da bloklash kerak (42.2).

## 19.4 `try-with-resources` va `AutoCloseable`

Qo'lda `finally` ichida yopish uch xatoga olib keladi: yopishni unutish, `close()` ning o'zi istisno tashlashi (asl istisnoni bostiradi), va bir necha resursni noto'g'ri tartibda yopish. `try-with-resources` uchtasini ham hal qiladi: resurslar teskari tartibda yopiladi va `close()` istisnosi **bostirilgan** (suppressed) sifatida saqlanadi.

```java
// yomon: close() istisnosi asl istisnoni yo'qotadi
InputStream in = null;
try {
    in = Files.newInputStream(file);
    return read(in);
} finally {
    if (in != null) in.close();      // bu tashlasa, asl istisno yo'qoladi
}

// yaxshi: avtomatik yopish, bostirilgan istisno saqlanadi
try (InputStream in = Files.newInputStream(file);
     var reader = new BufferedReader(new InputStreamReader(in, UTF_8))) {
    return read(reader);
}
```

O'z resursingiz bo'lsa, `AutoCloseable` ni amalga oshirish kerak va `close()` idempotent bo'lishi lozim. `Stream` ham `AutoCloseable`: `Files.lines`, `Files.walk` va JDBC oqimlari `try-with-resources` ichida bo'lishi shart.

## 19.5 `InterruptedException` ni to'g'ri qayta tiklash

`InterruptedException` tutilganda thread ning uzilish (interrupt) belgisi tozalanadi. Agar u tiklanmasa, yuqoridagi kod uzilganini bilmaydi va to'xtatish (graceful shutdown) ishlamaydi.

```java
// yomon: uzilish belgisi yo'qoldi - executor to'xtamaydi
try {
    queue.poll(1, TimeUnit.SECONDS);
} catch (InterruptedException e) {
    log.warn("uzildi", e);
}

// yaxshi: belgi tiklandi va sikl to'xtadi
try {
    queue.poll(1, TimeUnit.SECONDS);
} catch (InterruptedException e) {
    Thread.currentThread().interrupt();     // belgini tiklash
    throw new SettlementInterruptedException("hisob-kitob uzildi", e);
}
```

## 19.6 `Throwable`, `Error` va `OutOfMemoryError` siyosati

`Error` ierarxiyasi (`OutOfMemoryError`, `StackOverflowError`, `NoClassDefFoundError`) JVM darajasidagi muammolarni bildiradi va ularni tutish deyarli har doim xato: tizim allaqachon ishonchsiz holatda.

```java
// yomon: Error ni tutish - JVM ishonchsiz holatda davom etadi
catch (Throwable t) {
    log.error("xato", t);
    return fallback();
}

// yaxshi: faqat Exception, Error yuqoriga o'tadi
catch (Exception e) {
    log.error("hisob-kitob muvaffaqiyatsiz: {}", paymentId, e);
    throw new SettlementFailedException(paymentId, e);
}
```

Yagona istisno: eng tashqi thread chegarasi (`UncaughtExceptionHandler`, scheduler) `Throwable` ni tutib log qilishi va keyin tizimni to'xtatishi mumkin - lekin davom ettirmasligi kerak.

## 19.7 Log qilish yoki tashlash: ikkisini birga qilmaslik

`catch` ichida ham log yozish, ham istisnoni qayta tashlash eng ko'p uchraydigan log shovqini manbai: bir xato log da uch-to'rt marta paydo bo'ladi va incident vaqtida haqiqiy sabab topilmaydi.

Qoida: istisnoni **qayta ishlagan** joy log yozadi; uzatib yuborgan joy log yozmaydi (29.5).

```java
// yomon: har bir qatlam log yozadi - bitta xato uch marta log'da
catch (IOException e) {
    log.error("fayl o'qilmadi", e);
    throw new ImportException(e);
}

// yaxshi: kontekst qo'shiladi, log yuqorida bir marta yoziladi
catch (IOException e) {
    throw new ImportException("fayl o'qilmadi: " + file, e);
}

// Eng tashqi chegarada bir marta:
@ExceptionHandler(ImportException.class)
ResponseEntity<ProblemDetail> handle(ImportException e) {
    log.error("import muvaffaqiyatsiz", e);         // bitta joyda
    return ResponseEntity.status(422).body(problem(e));
}
```

## 19.8 Assertion va `-ea`: qachon haqli

`assert` gapi standart holatda **o'chirilgan** (`-ea` flagi kerak), shuning uchun u hech qachon kirish ma'lumotini tekshirish uchun ishlatilmasligi kerak - production da u umuman bajarilmaydi.

Assertion faqat bitta holatda haqli: **ichki** taxminni hujjatlashtirish va test muhitida tekshirish. Public API validatsiyasi esa har doim oshkor tekshiruv bilan amalga oshadi.

```java
// yomon: kirish tekshiruvi assert bilan - production da o'chirilgan
public void refund(Money amount) {
    assert amount.isPositive();           // ishlamaydi!
}

// yaxshi: kirish tekshiruvi oshkor, ichki taxmin assert bilan
public void refund(Money amount) {
    if (!amount.isPositive()) {
        throw new IllegalArgumentException("summa musbat bo'lishi kerak: " + amount);
    }
    ...
    assert invariantHolds() : "refund dan keyin qoldiq manfiy bo'lib qoldi";
}
```

## 19.9 `Objects.requireNonNull`, Guava `Preconditions`, Bean Validation

Uch vosita, uch xil o'rin. Ularni aralashtirish kodni izchilsiz qiladi.

| Vosita | Qayerda | Nima tashlaydi |
|---|---|---|
| `Objects.requireNonNull` | konstruktor, public metod, `null` tekshiruvi | `NullPointerException` |
| Qo'lda `if` + istisno | biznes qoidasi, diapazon | domen yoki `IllegalArgumentException` |
| Guava `Preconditions` | kutubxona kodi, xabar formatlash | `IllegalArgumentException`/`State` |
| Bean Validation (`@Valid`) | HTTP va xabar chegarasi | `MethodArgumentNotValidException` |
| `record` compact konstruktori | value object invarianti | istalgan |
| `assert` | ichki taxmin, test muhiti | `AssertionError` |

```java
// yaxshi: har biri o'z o'rnida
public SettlementService(PaymentGateway gateway, Clock clock) {
    this.gateway = Objects.requireNonNull(gateway, "gateway");
    this.clock = Objects.requireNonNull(clock, "clock");
}
```

Qoida: xabar har doim **maydon nomini** ko'rsatishi kerak - `requireNonNull(gateway)` xabarsiz `NullPointerException` beradi va stack trace dan qaysi argument `null` bo'lganini aniqlash qiyin bo'ladi.

## 19.10 Xato xabari matni: uch xil adresat

Bitta xato uch joyga chiqadi va uchtasiga boshqa matn kerak. Ularni aralashtirish ikki muammo keltiradi: foydalanuvchi texnik matnni ko'radi, yoki injener foydasiz "Xatolik yuz berdi" xabarini o'qiydi.

| Adresat | Nima kerak | Nima kerak emas |
|---|---|---|
| Foydalanuvchi | nima bo'ldi, nima qilish kerak, o'z tilida | stack trace, SQL, identifikator |
| Log (injener) | obyekt identifikatori, kutilgan va haqiqiy holat, trace id | foydalanuvchi uchun xushmuomalalik |
| API klient | barqaror xato kodi, maydon nomi, qisqa izoh | ichki sinf nomi, stack trace |

```java
// Domen istisnosi: injener uchun to'liq kontekst
public class RefundExceedsPaymentException extends DomainException {
    public RefundExceedsPaymentException(PaymentId id, Money requested, Money refundable) {
        super("REFUND_EXCEEDS_PAYMENT",
              "to'lov %s uchun %s qaytarilmoqchi, lekin faqat %s qaytarish mumkin"
                      .formatted(id, requested, refundable));
    }
}

// Chegarada: API klient uchun barqaror kod, foydalanuvchi uchun xabar
@ExceptionHandler(RefundExceedsPaymentException.class)
ProblemDetail handle(RefundExceedsPaymentException e, Locale locale) {
    ProblemDetail problem = ProblemDetail.forStatus(HttpStatus.UNPROCESSABLE_ENTITY);
    problem.setProperty("code", e.code());                       // barqaror kod
    problem.setDetail(messages.getMessage(e.code(), locale));     // foydalanuvchi tili
    return problem;
}
```

## 19.11 Xato kodi katalogi va uni barqaror ushlash

API klientlari xato **kodiga** qarab shoxlanadi, matnga qarab emas. Shuning uchun kod barqaror bo'lishi kerak: bir marta e'lon qilingan kod ma'nosini o'zgartirmaydi va o'chirilmaydi.

Amalda bu enum yoki konstanta katalogi bilan amalga oshadi va u hujjatlashtiriladi.

```java
public enum SettlementErrorCode {
    REFUND_EXCEEDS_PAYMENT("qaytarish summasi to'lovdan oshdi"),
    PAYMENT_NOT_SETTLED("to'lov hali bank tomonidan yopilmagan"),
    GATEWAY_UNAVAILABLE("bank gateway javob bermadi"),
    IDEMPOTENCY_CONFLICT("bir xil kalit bilan boshqa so'rov yuborilgan");

    private final String description;
    SettlementErrorCode(String description) { this.description = description; }
}
```

## 19.12 Xatolik atomarligi: yiqilgan metod obyektni buzib qoldirmasligi

Metod istisno bilan tugasa, obyekt chaqiruvdan oldingi holatida qolishi kerak. Bu xatolik atomarligi (failure atomicity) deyiladi. Buzilganda oqibat yashirin bo'ladi: chaqiruvchi istisnoni ushlab, log yozib, ishini davom ettiradi, obyekt esa yarim o'zgargan holatda qoladi va xato ancha keyin, boshqa joyda chiqadi.

```java
// yomon: ikkinchi qator yiqilsa, hisob allaqachon kamaygan
public void transfer(Money amount, Account target) {
    this.balance = this.balance.minus(amount);   // o'zgardi
    target.credit(amount);                       // bu yerda yiqilsa, pul yo'qoladi
}

// yaxshi: avval tekshiriladi, keyin o'zgartiriladi
public void transfer(Money amount, Account target) {
    if (balance.isLessThan(amount)) {
        throw new InsufficientFundsException(id, balance, amount);
    }
    Money remaining = balance.minus(amount);     // vaqtinchalik qiymat
    target.credit(amount);                       // yiqilsa, balance hali tegilmagan
    this.balance = remaining;
}
```

To'rt yo'l bor va tartibi shunday: obyektni o'zgarmas qilish (o'zgarmas obyektda bu muammo tug'ilmaydi), hamma tekshiruvni o'zgartirishdan **oldin** bajarish, o'zgarishni vaqtinchalik nusxada qilib oxirida almashtirish, yoki xato chiqqanda holatni qaytaradigan qayta tiklash kodi yozish. Oxirgisi eng qimmat va eng ko'p xato qiladigan yo'l, u odatda disk va tashqi resurs bilan ishlashda qoladi.

Qoida mutlaq emas: bir nechta thread bir obyektni o'zgartirganda `ConcurrentModificationException` dan keyin obyekt holati noma'lum bo'lib qolishi mumkin va `Error` dan keyin tiklanishga urinmaydi. Lekin oddiy biznes kodida atomarlik erishiladigan narsa va uning yo'qligi hujjatlanishi kerak. Spring kontekstida tranzaksiya bazadagi holatni qaytaradi, lekin obyektning xotiradagi maydonlarini qaytarmaydi: rollback dan keyin keshda yoki singleton bean ichida qolgan o'zgarish shu qoidaga tegishli.

## 19.13 Fayl va yo'l bilan ishlash: `Path`, `Files` va kodirovka

Fayl bilan ishlashda eski (`java.io.File`) va yangi (`java.nio.file`) API lar yonma-yon yashaydi va eski API ning uchta kamchiligi bor: xato holatida `boolean` qaytaradi (sabab bilinmaydi), symlink va fayl atributlari bilan ishlamaydi, kodirovkani yashiradi. Qoida: yangi kodda `Path` va `Files` ishlatiladi, `File` faqat eski API bilan chegarada.

```java
// yomon: xato sababi yo'qoladi, kodirovka platformaga bog'liq
File f = new File(dir, name);
if (!f.delete()) {
    log.warn("o'chirilmadi");            // nega? ruxsat, band, yo'q?
}
List<String> lines = Files.readAllLines(f.toPath());   // JDK 18 gacha platforma kodirovkasi

// yaxshi: istisno sababni aytadi, kodirovka oshkor
Path path = dir.resolve(name);
Files.delete(path);                      // NoSuchFileException, AccessDeniedException
try (Stream<String> lines = Files.lines(path, StandardCharsets.UTF_8)) {
    lines.filter(not(String::isBlank)).forEach(this::handle);
}
```

Uchta tuzoq takrorlanadi. Birinchisi: `Files.lines`, `Files.list` va `Files.walk` oqim qaytaradi va ular ochiq fayl deskriptorini ushlab turadi, shuning uchun `try-with-resources` ichida ishlatiladi, aks holda deskriptor sizib ketadi va bu faqat yuk ostida ko'rinadi. Ikkinchisi: kodirovkani ko'rsatmaslik. JDK 18 dan beri sukut UTF-8, lekin eski JDK da va `FileReader` bilan u platformaga bog'liq, demak kod Windows da va konteynerda boshqa ishlaydi. Uchinchisi: yo'lni satr birlashtirish bilan qurish. `dir + "/" + name` ajratgichni qattiq yozadi va `..` bilan katalogdan chiqib ketishni to'smaydi; `resolve` esa `Path` semantikasini saqlaydi.

Tashqaridan kelgan nom bilan yo'l qurilganda xavfsizlik qoidasi qo'shiladi: yo'l normallashtiriladi va bazaviy katalog ichida qolganligi tekshiriladi.

```java
// yaxshi: katalogdan chiqib ketishni to'sadi
Path target = baseDir.resolve(userInput).normalize();
if (!target.startsWith(baseDir)) {
    throw new IllegalArgumentException("yo'l bazaviy katalogdan tashqarida");
}
```

Vaqtinchalik fayl uchun `Files.createTempFile` ishlatiladi: u nomni taxmin qilinmaydigan qiladi va ruxsatni tor qo'yadi, `new File(tmpdir, "x.tmp")` esa poyga sharti va boshqa jarayon tomonidan almashtirish uchun ochiq qoldiradi. Tozalash `deleteOnExit` ga qoldirilmaydi (u faqat JVM normal tugaganda ishlaydi va ro'yxatni xotirada o'stiradi), balki `try-with-resources` yoki `finally` da bajariladi.

## 19.14 Offensive programming: development da qattiq, production da yumshoq yiqilish

Himoya tekshiruvining qaysi qismi ishlab chiqarishga qolishi [xato bilan ishlash bobida](18-xato-bilan-ishlash-qoidalari.md#1813-himoya-tekshiruvining-qanchasi-ishlab-chiqarishda-qoladi) hal qilinadi; bu bo'lim shu qarorning mexanikasi haqida, ya'ni bitta tekshiruv development da **qattiq**, production da **yumshoq** ishlashini qanday ta'minlash haqida. McConnell bu yondashuvni Howard va LeBlanc dan olib offensive programming deb ataydi: kutilmagan holat development da ko'zdan qochmaydigan, production da esa tiklanadigan bo'lsin (McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 8.6 (206-bet)). Kitobda keltirilgan qisqa shakl eslab qolishga qulay: o'lgan programma shikastlangan programmadan kamroq zarar keltiradi (Andy Hunt va Dave Thomas).

Development da qattiqlik nimadan iborat:

- **Assertion chindan ham to'xtatsin.** Ma'lum muammoni Enter bosib o'tib ketish odati paydo bo'lmasligi kerak; muammo tuzatiladigan darajada og'riqli bo'lishi kerak. Java da bu `-ea` ni test va dev JVM da yoqish demakdir ([assertion va `-ea`: qachon haqli](#198-assertion-va--ea-qachon-haqli)).
- **Kutilmagan shox jim o'tmasin.** `default` yoki `else` tarmog'i qattiq yiqilsin yoki boshqa yo'l bilan ko'zga tashlanadigan bo'lsin.
- **"Toza" ma'lumot bilan cheklanmaslik.** McConnell ning C dagi tavsiyalari (ajratilgan xotirani va faylni axlat bilan to'ldirish, o'chirishdan oldin obyektni axlatga aylantirish) Java da ko'chmaydi, chunki xotira qo'lda ajratilmaydi. G'oyaning Java dagi shakli: testda chiroyli fixture emas, chetki va tasodifiy qiymat berish; yopilgan resursni qayta ishlatish jim o'tmasligi uchun `close()` dan keyin holat oshkor "yopilgan" deb belgilanadi va keyingi chaqiruv `IllegalStateException` tashlaydi.
- **Production dagi xato log i yig'ilib turadigan bo'lsin.** Chiqarilgan versiyada qanday xatolar bo'layotganini ko'rmasangiz, development dagi qattiqlikning foydasi yo'qoladi.

`default` tarmog'i haqidagi talab [`switch` ni toza ishlatish](06-shart-mantiq-va-boshqaruv-oqimi.md#66-switch-ni-toza-ishlatish-toliqlik-default-fallthrough) qoidasiga qarama-qarshi ko'rinadi, u yerda enum ustidagi `switch` da `default` yozilmaydi deyilgan. Ikkisini ajratadigan shart - to'liqlikni **kompilyator tekshira oladimi**. Enum yoki `sealed` tur ustidagi `switch` ifodasida tekshira oladi, shuning uchun `default` ni butunlay yozmaslik qattiqroq variant: xato run time dan compile time ga ko'chadi. `int`, `String` yoki tashqaridan kelgan qiymat ustidagi `switch` da esa kompilyator yordam bermaydi va o'shanda `default` majburiy, lekin u jim qiymat qaytarmaydi, yiqiladi.

```java
// Tashqi qiymat: to'liqlikni kompilyator tekshirmaydi, default yiqiladi
return switch (externalCode) {
    case "SETTLED" -> Status.SETTLED;
    case "REJECTED" -> Status.REJECTED;
    default -> throw new IllegalStateException("qo'llanmagan status kodi: " + externalCode);
};
```

Production dagi yumshoqlik esa kodni har safar qo'lda kiritib-chiqarib yurish bilan emas, **bir xil kodning ikki xatti-harakati** bilan ta'minlanadi: McConnell bu usulni debugging stub deb ataydi, ya'ni development da to'liq tekshiradigan, production da esa darhol qaytadigan ikki variant saqlanadi va ular build yoki sozlama bilan almashtiriladi (8.6 (207-208-bet)). Spring da buning tabiiy shakli profil bo'yicha ikki bean:

```java
public interface InvariantGuard {
    void require(boolean condition, String message);
}

@Component
@Profile("dev")
class FailHardGuard implements InvariantGuard {
    @Override
    public void require(boolean condition, String message) {
        if (!condition) {
            throw new IllegalStateException("invariant buzildi: " + message);
        }
    }
}

@Component
@Profile("!dev")
class LoggingGuard implements InvariantGuard {
    private static final Logger log = LoggerFactory.getLogger(LoggingGuard.class);

    @Override
    public void require(boolean condition, String message) {
        if (!condition) {
            log.error("invariant buzildi: {}", message);   // to'xtatmaydi, iz qoldiradi
        }
    }
}
```

Shu shaklning qiymati: chaqiruv joyi o'zgarmaydi, siyosat esa bitta joyda turadi. Debug yordamchisini kodga kiritib-chiqarib yuradigan usul har tahrirda diff shovqini va unutilgan tekshiruv qoldiradi.

## 19.15 Amalda qo'llash

- [ ] Barcha `catch` bloklarini ko'rib, sababni (`cause`) uzatmaydiganlarini tuzating.
- [ ] `catch (Throwable)` va `catch (Error)` ni topib, eng tashqi chegaradan tashqari joylarda olib tashlang.
- [ ] `finally` ichida `return` yoki `throw` bo'lgan joylarni tuzatib, Error Prone `Finally` qoidasini yoqing.
- [ ] Qo'lda `finally` da yopiladigan resurslarni `try-with-resources` ga o'tkazing.
- [ ] `InterruptedException` tutilgan barcha joylarda `Thread.currentThread().interrupt()` borligini tekshiring.
- [ ] "Log va qayta tashlash" namunalarini topib, log ni faqat qayta ishlagan joyda qoldiring.
- [ ] `assert` bilan kirish tekshiradigan joylarni oshkor tekshiruvga o'tkazing.
- [ ] API xato kodlari katalogini enum sifatida yozib, hujjatlashtiring va barqarorlik qoidasini kelishib oling.
- [ ] Holatni o'zgartiradigan metodlarni ko'rib chiqing: tekshiruvlar o'zgartirishdan oldin bajarilayotganini ta'minlang.
- [ ] Tranzaksiya rollback idan keyin xotirada qoladigan o'zgarishlarni (kesh, singleton maydon) ro'yxatlab, ularni tozalash yo'lini qo'ying.
- [ ] `Files.lines`, `Files.list` va `Files.walk` chaqiruvlarini toping va hammasi `try-with-resources` ichida ekanini tekshiring.
- [ ] `FileReader`, `FileWriter` va kodirovkasiz `readAllLines` chaqiruvlarini oshkor `StandardCharsets.UTF_8` ga o'tkazing.
- [ ] Tashqi kirishdan yo'l quradigan joylarda `normalize` va `startsWith` tekshiruvi borligini ta'minlang.
- [ ] Test va dev JVM da `-ea` yoqilganini tekshirib, assertion ning chindan ham to'xtatishini ta'minlang.
- [ ] Kompilyator to'liqligini tekshirmaydigan `switch` lardagi `default` tarmoqlarini ko'rib, jim qiymat qaytaradiganlarini yiqiladigan qiling.

## Manbalar

- Joshua Bloch, *Effective Java* 3rd, Item 76 - xatolik atomarligi va unga erishishning to'rt yo'li
- Joshua Bloch, *Effective Java* 3rd, Item 75 - istisno xabarida xatoni ushlash uchun ma'lumot
- Joshua Bloch, *Effective Java* 3rd, Item 77 - istisnoni e'tiborsiz qoldirmaslik
- Joshua Bloch, *Effective Java* 3rd, Item 9 - `try-finally` emas `try-with-resources`
- Joshua Bloch, *Effective Java* 3rd, Item 49 - parametr yaroqliligini tekshirish
- Herbert Schildt, *Java The Complete Reference*, 22, 23-boblar - `java.io` va NIO fayl API si
- [JEP 400: UTF-8 by Default](https://openjdk.org/jeps/400) - JDK 18 dan beri sukut kodirovka UTF-8
- Boyarsky/Selikoff, *OCP Java SE 17 Study Guide*, 14-bob - `Path`, `Files` va oqim bilan fayl o'qish
- Steve McConnell, *Code Complete*, 2-nashr, 8.6 (206-bet) - offensive programming: development da ko'zga tashlanadigan, production da tiklanadigan xato
- Steve McConnell, *Code Complete*, 2-nashr, 8.6 (207-208-bet) - debug yordamchilarini olib tashlashni rejalashtirish va debugging stub

---

[&larr; 18. Xato bilan ishlash qoidalari](18-xato-bilan-ishlash-qoidalari.md) · [Mundarija](README.md) · [20. Primitiv, son va pul &rarr;](20-primitiv-son-va-pul.md)
