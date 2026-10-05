<!-- doc: clean-code | chapter: 19 | part: VI. Xato bilan ishlash -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

# 19. Istisno mexanikasi va resurslar (Exception Mechanics and Resources)

<details>
<summary>Bu bobdagi 12 bo'lim</summary>

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
- [19.12 Amalda qo'llash](#1912-amalda-qollash)

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

## 19.12 Amalda qo'llash

- [ ] Barcha `catch` bloklarini ko'rib, sababni (`cause`) uzatmaydiganlarini tuzating.
- [ ] `catch (Throwable)` va `catch (Error)` ni topib, eng tashqi chegaradan tashqari joylarda olib tashlang.
- [ ] `finally` ichida `return` yoki `throw` bo'lgan joylarni tuzatib, Error Prone `Finally` qoidasini yoqing.
- [ ] Qo'lda `finally` da yopiladigan resurslarni `try-with-resources` ga o'tkazing.
- [ ] `InterruptedException` tutilgan barcha joylarda `Thread.currentThread().interrupt()` borligini tekshiring.
- [ ] "Log va qayta tashlash" namunalarini topib, log ni faqat qayta ishlagan joyda qoldiring.
- [ ] `assert` bilan kirish tekshiradigan joylarni oshkor tekshiruvga o'tkazing.
- [ ] API xato kodlari katalogini enum sifatida yozib, hujjatlashtiring va barqarorlik qoidasini kelishib oling.

---

[&larr; 18. Xato bilan ishlash qoidalari](18-xato-bilan-ishlash-qoidalari.md) · [Mundarija](README.md) · [20. Primitiv, son va pul &rarr;](20-primitiv-son-va-pul.md)
