<!-- doc: clean-code | chapter: 19 | part: VI. Xato bilan ishlash -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 19. Istisno mexanikasi va resurslar (Exception Mechanics and Resources)

<details>
<summary>Bu bobdagi 16 bo'lim</summary>

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
- [19.15 `catch` parametri va resurs o'zgaruvchisi: yashirin `final` va aniqroq qayta tashlash](#1915-catch-parametri-va-resurs-ozgaruvchisi-yashirin-final-va-aniqroq-qayta-tashlash)
- [19.16 Amalda qo'llash](#1916-amalda-qollash)

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

Kompilyator bu yerda bitta yordam beradi va keng `catch` shu yordamni o'chiradi. `try` bloki tashlay **olmaydigan** tekshiriladigan istisnoni tutish kompilyatsiya xatosi: ya'ni `catch (ParseException e)` yozsangiz va blok ichida uni tashlaydigan hech narsa bo'lmasa, kod kompilyatsiya bo'lmaydi va siz ortiqcha bandni darhol ko'rasiz. `catch (Exception e)` esa har doim kompilyatsiya qilinadi, chunki `RuntimeException` har joydan kelishi mumkin. Natijada keng `catch` nafaqat aniq istisnolarni yashiradi, balki "bu blokdan umuman hech narsa tashlanmaydi" holatini ham yashiradi: tozalashdan keyin ortiqcha bo'lib qolgan `try-catch` yillar davomida turib qoladi.

Shu yerda tekshiriladigan istisnoning maydon initsializatoriga tegishli qoidasi ham bor va u kam ma'lum: instans maydoni initsializatori tekshiriladigan istisno tashlashi mumkin, lekin faqat sinfning **har bir** oshkor konstruktori shu istisnoni `throws` da e'lon qilgan bo'lsa. Oshkor konstruktor umuman bo'lmasa, initsializatorda tekshiriladigan istisno tashlab bo'lmaydi. Amaliy natija: resurs ochadigan yoki parse qiladigan ishni maydon initsializatoriga qo'yish kompilyatsiya qarzini keltiradi, shuning uchun u statik fabrikaga yoki konstruktor tanasiga ko'chiriladi.

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

`try-with-resources` ga `catch` va `finally` bandlarini ham qo'yish mumkin, ya'ni istisnoni qayta ishlash uchun qo'shimcha ichma-ich `try` kerak emas. Lekin `finally` ning **tartibi** tuzoq: u yashirin `close()` dan KEYIN bajariladi. Shuning uchun `finally` ichida resursga tegadigan o'lchov, log yoki tekshiruv yozilsa, u allaqachon yopilgan resursni ko'radi.

```java
// yaxshi: catch shu yerda, qo'shimcha ichma-ich try kerak emas
try (var reader = Files.newBufferedReader(file, UTF_8)) {
    return parse(reader);
} catch (NoSuchFileException e) {
    throw new ImportException("import fayli yo'q: " + file, e);
} finally {
    meter.recordCallCompleted();        // reader allaqachon yopilgan
}
```

O'z resursingiz bo'lsa, `AutoCloseable` ni amalga oshirish kerak va `close()` idempotent bo'lishi lozim. Bundan tashqari `close()` obyektni **yaroqsiz** deb belgilashi kerak: oddiy shakl - `closed` maydonini `true` qilish, qolgan metodlarning birinchi qatorida shu maydonni tekshirish va yopilgandan keyingi chaqiruvda `IllegalStateException` tashlash. Shunday qilmasa, yopilgan resursni qayta ishlatish jim o'tadi va xato uzoqda, boshqa alomat bilan chiqadi ([offensive programming](#1914-offensive-programming-development-da-qattiq-production-da-yumshoq-yiqilish) shu qoidaning umumiy shakli).

```java
public final class SettlementLedger implements AutoCloseable {

    private boolean closed;

    public void append(SettlementRow row) {
        requireOpen();
        ...
    }

    @Override
    public void close() {
        if (closed) { return; }        // idempotent
        closed = true;
        flush();
    }

    private void requireOpen() {
        if (closed) {
            throw new IllegalStateException("ledger yopilgan, yozib bo'lmaydi");
        }
    }
}
```

`Stream` ham `AutoCloseable`: `Files.lines`, `Files.walk` va JDBC oqimlari `try-with-resources` ichida bo'lishi shart.

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

Yuqoridagi shaklda belgi darhol tiklanadi va bu to'g'ri, chunki metod shu zahoti qaytadi. Lekin bekor qilishni **qo'llab-quvvatlamaydigan**, ya'ni uzilgandan keyin ham ishini oxirigacha qilishi kerak bo'lgan faoliyat uchun tartib boshqa: uzilish holati lokal o'zgaruvchida saqlanadi va qaytishdan sal **oldin** tiklanadi. Sabab mexanik: bloklovchi metodlarning ko'pi kirishda uzilish holatini tekshiradi va u o'rnatilgan bo'lsa darhol `InterruptedException` bilan qaytadi. Belgini `catch` ichida darhol tiklab, keyin yana bloklovchi chaqiruvga kirsangiz, siklning har aylanishi darhol istisno bilan tugaydi va qayta urinish tsikli cheksiz aylanadi.

```java
// yaxshi: uzilish lokal saqlandi, ish bajarildi, belgi oxirida tiklandi
public SettlementRow takeUninterruptibly(BlockingQueue<SettlementRow> queue) {
    boolean interrupted = false;
    try {
        while (true) {
            try {
                return queue.take();
            } catch (InterruptedException e) {
                interrupted = true;      // darhol tiklanmaydi: tsikl cheksiz bo'lib qolardi
            }
        }
    } finally {
        if (interrupted) {
            Thread.currentThread().interrupt();
        }
    }
}
```

Tanlov mezoni: faoliyat bekor qilishni qo'llab-quvvatlasa, belgi tiklanadi va ish to'xtatiladi; qo'llab-quvvatlamasa, belgi lokal saqlanib chiqishdan oldin tiklanadi, chunki uzilish ma'lumotini butunlay yo'qotish ham xato ([arxitektor hujjatidagi](../architect/11-concurrency-thread-lock-atomic-happens.md#1114-bekor-qilish-interrupt-siyosati-va-thread-starvation-deadlock) bekor qilish va interrupt siyosati).

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

Siyosatning yozish tomoni ham bor: `Exception`, `RuntimeException` yoki `Error` ning vorisi bo'lmagan throwable (ya'ni to'g'ridan-to'g'ri `Throwable` dan voris olgan sinf) yozilmaydi. Java bunga ruxsat beradi, lekin natija hech qanday foyda bermaydi: bunday sinf oddiy tekshiriladigan istisno kabi ishlaydi, shu bilan birga API foydalanuvchisini chalkashtiradi, chunki uni `catch (Exception e)` tutmaydi va `catch (Error e)` ham tutmaydi. Amalda u faqat eng tashqi `catch (Throwable t)` ga tushadi, ya'ni ishlovchisi yo'q istisno bo'lib qoladi. Qoida: o'z istisno sinfi `RuntimeException` (tekshirilmaydigan) yoki `Exception` (tekshiriladigan) dan voris oladi va uchinchi variant yo'q.

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

Uchinchi variant ham bor va u kam, lekin haqli: istisnoni **e'tiborsiz qoldirish**. Masalan faqat o'qish uchun ochilgan `InputStream` ni yopishda chiqqan istisno hech narsani o'zgartirmaydi, chunki ma'lumot allaqachon o'qilgan va amalni qaytarishning ma'nosi yo'q. Bo'sh `catch` bloki esa review da har doim xato deb o'qiladi, shuning uchun haqli holatning oshkor shakli bor va u ikki qismdan iborat: blok ichida **nega** e'tiborsiz qoldirilayotganini aytuvchi izoh, va o'zgaruvchining `ignored` deb nomlanishi. Nom konvensiyasi muhim, chunki u statik tahlil vositalariga ham, review qiluvchiga ham "bu ataylab" degan signal beradi.

```java
// yaxshi: sababi izohda, nomi konvensiya bo'yicha
int numColors = 4;
try {
    numColors = processor.optimalColorCount();
} catch (TimeoutException | ExecutionException ignored) {
    // Standart qiymat yetarli: optimaldan past bo'lsa ham ishlaydi
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

Shundan ikkinchi, qat'iy qoida kelib chiqadi: **assertion ifodasi yon ta'sirsiz bo'lishi kerak**. `assert` o'chirilganda ifoda umuman bajarilmaydi, demak ifoda ichidagi tayinlash, inkrement yoki holat o'zgartiruvchi chaqiruv `-ea` yoqilgan va yoqilmagan muhitda dasturni **boshqacha** ishlatadi. Bu xatoning eng yomon shakli: nosozlik faqat production da chiqadi va dev da takrorlanmaydi, chunki dev da ifoda bajarilib turgan.

```java
// yomon: assert o'chirilsa getNext() umuman chaqirilmaydi va mantiq o'chadi
assert (row = reader.getNext()) != null;

// yomon: hisoblagich faqat -ea bilan o'sadi
assert counter.incrementAndGet() > 0;

// yaxshi: ifoda faqat o'qiydi va hukm chiqaradi
SettlementRow row = reader.getNext();
assert row != null : "reader hasNext dan keyin null qaytardi";
```

Mezon bitta: `assert` dan keyingi kod `assert` qatorini butunlay o'chirib tashlasa ham xuddi shunday ishlashi kerak.

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

Java 9 da `Objects` ga oraliq tekshiruvi uchun uchta metod qo'shilgan va ularning o'z o'rni bor: `Objects.checkIndex(index, length)`, `Objects.checkFromToIndex(from, to, length)` va `Objects.checkFromIndexSize(from, size, length)`. Ikki chegara bilish kerak. Birinchi: ular faqat **ro'yxat va massiv indeksi** uchun mo'ljallangan, umumiy diapazon tekshiruvi (`amount` 0 dan 1000 gacha) uchun emas. Ikkinchi: ular o'z xato xabarini qabul qilmaydi, ya'ni kontekst qo'shib bo'lmaydi. Shuning uchun ular o'z to'plam yoki bufer sinfingizni yozganda qulay, biznes qoidasi uchun esa qo'lda `if` qoladi.

```java
// yaxshi: o'z to'plam sinfida indeks tekshiruvi
public SettlementRow get(int index) {
    Objects.checkIndex(index, size);     // IndexOutOfBoundsException, standart xabar
    return rows[index];
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

Uchinchi adresat jadvaldagi taqiqning bir sababini ochadi: istisnoning **satr ko'rinishini parslab** qo'shimcha ma'lumot olish juda yomon amaliyot. `Throwable` sinflari `toString` va `getMessage` formatini spetsifikatsiyalamaydi, demak format reliz bilan o'zgaradi va parslaydigan kod jim buziladi; ba'zan esa buzilmaydi, lekin noto'g'ri qiymat chiqaradi, bu yomonroq. Agar chaqiruvchiga xatodan ma'lumot kerak bo'lsa, u xabarda emas, **accessor** da berilishi kerak: istisno sinfi maydon saqlaydi va getter beradi (`e.refundable()`, `e.retryAfter()`). Shu qoida `toString` ning umumiy qoidasining istisnoga tegishli shakli ([`toString`: foydali, xavfsiz, mantiqda ishlatilmaydigan](15-tenglik-hash-va-obyekt-shartnomalari.md#157-tostring-foydali-xavfsiz-mantiqda-ishlatilmaydigan)).

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

Katalogning narxi ham bor va u e'tibordan qolmasligi kerak. Xato kodi `enum` i bog'liqlik magnitiga aylanadi: uni hamma modul import qiladi, demak enum ga bitta konstanta qo'shilsa yoki o'zgartirilsa, importchilarning hammasi qayta kompilyatsiya va qayta deploy qilinadi. Natija dasturchi xulqida ko'rinadi: qayta deploy qiyin bo'lgani uchun odamlar yangi kod qo'shmay, mavjud kodni "yaqin ma'noda" qayta ishlatadi va katalog ma'nosini yo'qotadi. Istisno sinflari bu muammodan xoli, chunki yangi istisno mavjud istisnoning vorisi sifatida qo'shiladi va importchilar tegilmaydi.

Ikki da'vo bir-biriga qarshi ko'rinadi, lekin ularni ajratuvchi shart aniq: kod **qayerda** ishlatiladi.

| Kod qayerda | To'g'ri shakl | Nega |
|---|---|---|
| Tashqi API chegarasida: klient kodga qarab shoxlanadi | barqaror kod katalogi | kod mijozning shartnomasi, u o'zgarmasligi kerak va hujjatlashtiriladi |
| Ichki qaytish qiymati sifatida: chaqiruvchi o'zi tekshiradi | istisno | katalog bog'liqlik magniti bo'ladi, tekshiruvni unutish esa jim o'tadi |

Ya'ni katalog **chegarada** yashaydi va faqat chegarada: HTTP javobi, xabar sarlavhasi, tashqi shartnoma. Ichki qatlamlarda esa domen istisnolari ishlatiladi va kod faqat chegarada, istisnodan ko'chiriladi (19.10 dagi `ProblemDetail` namunasi shu shakl). Ichki kodda xato kodini qaytarish taqiqi [xato kodi emas, istisno](18-xato-bilan-ishlash-qoidalari.md#181-xato-kodi-emas-istisno) da yoziladi; bu bo'lim chegaradagi istisnoni belgilaydi.

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

Tekshiruv olib tashlanganda **ikki** qoida bir vaqtda buziladi va bu platformadagi klassik namunada ko'rinadi: hajmni tekshirmaydigan `pop` metodi. Birinchi buzilish, atomarlik: hisoblagich allaqachon kamaygan, shuning uchun obyekt manfiy `size` bilan nomuvofiq holatda qoladi va keyingi har bir chaqiruv kutilmagan natija beradi. Ikkinchi buzilish, abstraksiya darajasi: chaqiruvchi `ArrayIndexOutOfBoundsException` oladi, holbuki u stack bilan ishlayotganini biladi va `EmptyStackException` yoki `IllegalStateException` kutadi (18.3). Bitta yetishmagan `if` ikki bobdagi qoidani birga buzadi, shuning uchun tekshiruvni "ortiqcha" deb olib tashlash qarori hamisha shu ikki tomondan baholanadi.

```java
// yomon: tekshiruv yo'q - holat ham buziladi, istisno ham mos kelmaydi
public Object pop() {
    size--;                              // allaqachon kamaydi
    return elements[size];               // ArrayIndexOutOfBoundsException
}

// yaxshi: tekshiruv o'zgartirishdan oldin, istisno abstraksiyaga mos
public Object pop() {
    if (size == 0) {
        throw new EmptyStackException();
    }
    Object result = elements[--size];
    elements[size] = null;               // eskirgan havolani tozalash
    return result;
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

Fayl bilan ishlashda poyga sharti faqat vaqtinchalik faylda emas. **Fayl mavjudligini tekshirish hech narsa kafolatlamaydi**: `Files.exists(path)` `true` qaytargandan keyin ham keyingi qator `NoSuchFileException` tashlashi mumkin, chunki fayl oradagi vaqtda boshqa jarayon yoki boshqa thread tomonidan o'chirilgan bo'lishi mumkin. Shuning uchun to'g'ri shakl "tekshir, keyin bajar" emas, "bajar, istisnoni ushla": `exists` tekshiruvi faqat foydalanuvchiga xabar berish uchun ishlatiladi va amalni `try-catch` siz qoldirmaydi.

```java
// yomon: tekshiruv va amal orasida oyna bor
if (Files.exists(path)) {
    return Files.readString(path, UTF_8);      // NoSuchFileException baribir mumkin
}

// yaxshi: amal bajariladi, yo'qlik holati istisno bilan hal qilinadi
try {
    return Files.readString(path, UTF_8);
} catch (NoSuchFileException e) {
    throw new ImportException("import fayli yo'q: " + path, e);
}
```

Oqimni qo'lda o'qiganda ikki tuzoq qo'shiladi. Birinchi: `available()` **oqim oxirini aniqlash uchun ishlamaydi**. U faqat "bloklanmasdan hozir qancha bayt o'qish mumkin" degan taxminni qaytaradi, shuning uchun `while (in.available() > 0)` sikli tarmoq va `ObjectInputStream` da ma'lumotning yarmini o'qib to'xtaydi. Oqim oxiri `read()` ning `-1` qaytarishi, `EOFException`, yoki element sonini oldin yozib qo'yish bilan aniqlanadi. Ikkinchi, `ByteBuffer` bilan ishlaganda: bufer o'qish va yozish orasida **qayta tiklanishi** shart. `flip()` yozish rejimidan o'qish rejimiga o'tkazadi (limit ni joriy pozitsiyaga qo'yib pozitsiyani nolga qaytaradi), `clear()` yoki `rewind()` esa teskarisini qiladi. Chaqirilmasa keyingi amal noto'g'ri pozitsiyadan boshlanadi va odatda hech narsa o'qimaydi, hech qanday istisno ham bermaydi: NIO ni qo'lda yozganda birinchi uchraydigan xato shu.

```java
// yomon: flip yo'q - pozitsiya oxirida, read hech narsa bermaydi
channel.read(buffer);
while (buffer.hasRemaining()) { handle(buffer.get()); }   // sikl umuman kirmaydi

// yaxshi: yozishdan keyin flip, qayta ishlatishdan oldin clear
channel.read(buffer);
buffer.flip();
while (buffer.hasRemaining()) { handle(buffer.get()); }
buffer.clear();
```

Vaqtinchalik fayl uchun `Files.createTempFile` ishlatiladi: u nomni taxmin qilinmaydigan qiladi va ruxsatni tor qo'yadi, `new File(tmpdir, "x.tmp")` esa poyga sharti va boshqa jarayon tomonidan almashtirish uchun ochiq qoldiradi. Tozalash `deleteOnExit` ga qoldirilmaydi (u faqat JVM normal tugaganda ishlaydi va ro'yxatni xotirada o'stiradi), balki `try-with-resources` yoki `finally` da bajariladi.

To'rtinchi tuzoq oqimning o'ziga tegadi: **buferlanmagan o'qish va yozish**.
`FileInputStream` dan to'g'ridan-to'g'ri baytma-bayt o'qish har bayt uchun
tizim chaqiruviga tushadi va jarayon butunlay I/O ga bog'lanib qoladi. Shirazi
buni o'lchagan: `FileInputStream` ni `BufferedInputStream` ga o'rash vaqtni
bir tartibga (order of magnitude) qisqartirgan. Shu bilan birga buferni
kattalashtirish avtomatik yaxshilanish bermaydi: uning o'lchovida default
bufer o'rniga 8 KB bufer sezilarli farq ko'rsatmagan, demak bufer hajmi
taxmin bilan emas, o'lchov bilan tanlanadi (Shirazi, *Java Performance
Tuning*, 2-nashr, O'Reilly, 2003, 8.3-bo'lim "From Raw I/O to Smokin' I/O").

```java
// yomon: har bayt uchun tizim chaqiruvi
try (InputStream in = Files.newInputStream(path)) {
    int b;
    while ((b = in.read()) != -1) {
        handle((byte) b);
    }
}

// yaxshi: buferlangan o'qish, qator darajasida ishlov
try (BufferedReader reader = Files.newBufferedReader(path, StandardCharsets.UTF_8)) {
    String line;
    while ((line = reader.readLine()) != null) {
        handle(line);
    }
}
```

ESLATMA: kitobning o'lchovi JDK 1.1-1.4 davrida va `DataInputStream.readLine`
bilan qilingan, shuning uchun uning aniq raqamlari bugunga ko'chmaydi;
buferlash qoidasining o'zi amal qiladi. Zamonaviy shakl: `Files.newBufferedReader`
va `Files.newBufferedWriter`, yoki `Files.lines` (u ham buferlangan oqim
ustida ishlaydi) va ikkisi ham kodirovkani oshkor oladi.

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

## 19.15 `catch` parametri va resurs o'zgaruvchisi: yashirin `final` va aniqroq qayta tashlash

Java ba'zi o'zgaruvchilarni siz `final` deb yozmasangiz ham `final` qiladi, ba'zilaridan esa "effectively final" bo'lishni talab qiladi. Istisno va resurs bilan ishlaydigan kodda bu uch joyda chiqadi va uchi ham amaliy natijaga olib keladi.

**Multi-catch parametri yashirin `final`.** `catch (A | B e)` shaklida `e` ga blok ichida yangi qiymat berib bo'lmaydi va bu kompilyatsiya xatosi. Bitta turni tutadigan oddiy `catch` da esa tayinlash qonuniy, lekin ma'nosi yo'q va keyingi qoidani buzadi. Xuddi shu yashirin `final` interfeys maydonida va `try-with-resources` ning resurs o'zgaruvchisida ham amal qiladi: resursni blok ichida boshqa obyektga almashtirib, yashirin `close()` ni chetlab o'tish mumkin emas.

**Aniqroq qayta tashlash (more precise rethrow) effectively final ni talab qiladi.** Java 7 dan `catch (Exception e) { throw e; }` yozilganda kompilyator `e` ning haqiqiy mumkin bo'lgan turlarini hisoblaydi va metodning `throws` ro'yxatida faqat shularni talab qiladi. Ya'ni keng tutib aniq qayta tashlash mumkin. Lekin bu faqat `catch` parametri effectively final bo'lganda ishlaydi: parametrga blok ichida yangi qiymat berilsa, kompilyator uning turi haqidagi bilimni yo'qotadi va `throws Exception` ga qaytadi. Shuning uchun o'ramchi metodda `throws` ni toraytirish qarori parametrga tegmaslikka bog'liq.

```java
// yaxshi: throws ro'yxati aniq, chunki e effectively final
void copyLedger(Path from, Path to) throws NoSuchFileException, AccessDeniedException {
    try {
        Files.copy(from, to);
    } catch (Exception e) {
        audit.record("copy failed", from, to);
        throw e;                  // kompilyator aniq ikki turni ko'radi
    }
}

// yomon: parametrga tayinlash - aniqroq qayta tashlash yo'qoldi
void copyLedgerYomon(Path from, Path to) throws Exception {   // toraytirib bo'lmaydi
    try {
        Files.copy(from, to);
    } catch (Exception e) {
        e = new IOException("copy failed", e);   // endi tur noma'lum
        throw e;
    }
}
```

**Resurs spetsifikatsiyasida avval e'lon qilingan o'zgaruvchi.** JDK 9 dan `try (resource)` ichida yangi o'zgaruvchi e'lon qilish shart emas: avval e'lon qilingan o'zgaruvchining nomini yozish ham mumkin. Sharti bitta va u qat'iy: o'zgaruvchi effectively final bo'lishi kerak, ya'ni e'londan keyin unga qayta tayinlanmaydi. Bu shakl resursni boshqa joyda (masalan fabrika metodida) olib, yopishni `try` ga topshirish kerak bo'lganda qulay.

```java
// JDK 9+: resurs avval e'lon qilingan, try faqat yopadi
BufferedReader reader = openLedger(file);    // boshqa joyda ochildi, qayta tayinlanmaydi
try (reader) {
    return parse(reader);
}
```

Qoida sifatida: `catch` parametriga va resurs o'zgaruvchisiga hech qachon qayta tayinlamang. Yangi qiymat kerak bo'lsa yangi lokal o'zgaruvchi e'lon qilinadi, shunda `throws` ni toraytirish imkoni ham, yashirin `close()` ning kafolati ham saqlanadi.

## 19.16 Amalda qo'llash

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
- [ ] Bo'sh `catch` bloklarini toping: haqli bo'lsa izoh qo'shib o'zgaruvchini `ignored` deb nomlang, aks holda ishlovchi yozing.
- [ ] `assert` ifodalarida tayinlash va holat o'zgartiruvchi chaqiruv borligini tekshirib, ularni `assert` dan tashqariga chiqaring.
- [ ] Istisno xabarini yoki `toString` ini parslaydigan kodni toping va istisnoga accessor qo'shib almashtiring.
- [ ] `Files.exists` dan keyin amal bajaradigan joylarni "bajar va istisnoni ushla" shakliga o'tkazing.
- [ ] `available()` bilan oqim oxirini aniqlaydigan siklni toping va `-1` yoki `EOFException` ga o'tkazing.
- [ ] O'z `AutoCloseable` sinflaringizda `close()` dan keyingi chaqiruv `IllegalStateException` tashlashini ta'minlang.
- [ ] `catch` parametriga yoki resurs o'zgaruvchisiga qayta tayinlaydigan joylarni toping va yangi lokal o'zgaruvchiga o'tkazing.

## Manbalar

- Joshua Bloch, *Effective Java* 3rd, Item 76 - xatolik atomarligi va unga erishishning to'rt yo'li
- Joshua Bloch, *Effective Java* 3rd, Item 75 - istisno xabarida xatoni ushlash uchun ma'lumot
- Joshua Bloch, *Effective Java* 3rd, Item 77 - istisnoni e'tiborsiz qoldirmaslik
- Joshua Bloch, *Effective Java* 3rd, Item 9 - `try-finally` emas `try-with-resources`
- Joshua Bloch, *Effective Java* 3rd, Item 8 (31-bet) - resursni tugatish kerak bo'lganda `AutoCloseable` ni amalga oshirish, `close()` da obyektni yaroqsiz deb belgilash va keyingi chaqiruvda `IllegalStateException` tashlash
- Joshua Bloch, *Effective Java* 3rd, Item 9 (36-bet) - `try-with-resources` ga `catch` bandi qo'yish mumkinligi va shunda ichma-ich `try` kerak bo'lmasligi
- Joshua Bloch, *Effective Java* 3rd, Item 49 (229-bet) - Java 9 dagi `Objects.checkIndex`, `checkFromToIndex` va `checkFromIndexSize` metodlari faqat ro'yxat va massiv indeksi uchun bo'lishi va o'z xabarini qabul qilmasligi
- Joshua Bloch, *Effective Java* 3rd, Item 70 (297-bet) - `Exception`, `RuntimeException` yoki `Error` ning vorisi bo'lmagan throwable yozmaslik
- Joshua Bloch, *Effective Java* 3rd, Item 70 (297-bet) - istisnoning satr ko'rinishini parslab qo'shimcha ma'lumot olmaslik: `Throwable` sinflari satr ko'rinishini spetsifikatsiyalamaydi
- Joshua Bloch, *Effective Java* 3rd, Item 77 (310-bet) - istisnoni e'tiborsiz qoldirish haqli bo'lganda `catch` blokida sababni tushuntiruvchi izoh bo'lishi va o'zgaruvchi `ignored` deb nomlanishi
- Joshua Bloch, *Effective Java* 3rd, Item 76 (308-bet) - tekshiruv olib tashlansa obyektning nomuvofiq (manfiy `size`) holatda qolishi va tashlanadigan istisnoning abstraksiyaga mos kelmasligi: ikki qoidaning birga buzilishi
- Robert C. Martin, *Clean Code*, 3-bob ("Prefer Exceptions to Returning Error Codes", 47-48-bet) - xato kodi `enum` ining bog'liqlik magniti bo'lishi: uni hamma import qilishi, o'zgarganda qayta kompilyatsiya va qayta deploy talab qilishi, natijada programmistlarning yangi kod qo'shmay eskisini qayta ishlatishi; istisnoning esa voris sinf sifatida qayta deploy talab qilmay qo'shilishi
- ESLATMA: Clean Code xato kodi `enum` ini bog'liqlik magniti deb ataydi, korpus esa tashqi API uchun barqaror xato kodi katalogini talab qiladi. Ikkisini ajratuvchi shart (kod TASHQI API chegarasida bo'lsa katalog haqli, ICHKI qaytish qiymati sifatida ishlatilsa istisno afzal) va uning jadvali korpus qo'shimchasi, kitobda bu ajratish yo'q
- Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley, 2006, 7-bob (90-bet) - bekor qilishni qo'llab-quvvatlamaydigan, lekin bloklovchi metod chaqiradigan faoliyatning uzilish holatini lokal saqlab qaytishdan oldin tiklashi va holatni darhol tiklashning cheksiz tsiklga olib kelishi
- *The Java Language Specification, Java SE 25 Edition* (Gosling, Joy, Steele, Bracha, Buckley, Smith, Bierman), 4.12.4 (104-bet) - interfeys maydoni, `try-with-resources` resursi va ko'p turni tutadigan `catch` parametrining yashirin `final` bo'lishi
- *The Java Language Specification, Java SE 25 Edition* (Gosling, Joy, Steele, Bracha, Buckley, Smith, Bierman), 11.2.3 (430-bet) - `try` bloki tashlay olmaydigan tekshiriladigan istisnoni `catch` qilish kompilyatsiya xatosi bo'lishi, `catch (Exception e)` esa har doim kompilyatsiya qilinishi
- *The Java Language Specification, Java SE 25 Edition* (Gosling, Joy, Steele, Bracha, Buckley, Smith, Bierman), 11.2.2 (429-bet) - instans maydoni initsializatori tekshiriladigan istisno tashlashi faqat har bir oshkor konstruktor uni `throws` da e'lon qilganda mumkinligi
- *The Java Language Specification, Java SE 25 Edition* (Gosling, Joy, Steele, Bracha, Buckley, Smith, Bierman), 14.10 (512-bet) - assertion ifodasi yon ta'sirsiz bo'lishi talabi: aks holda dastur xulqi `-ea` yoqilganiga qarab o'zgaradi
- Herbert Schildt, *Java The Complete Reference*, 12-nashr, McGraw Hill, 2022, 10-bob (245-246-bet) - multi-catch parametrining yashirin `final` bo'lishi va aniqroq qayta tashlashning `catch` parametri effectively final bo'lishini talab qilishi
- Herbert Schildt, *Java The Complete Reference*, 12-nashr, McGraw Hill, 2022, 13-bob (330-bet) - JDK 9 dan resurs spetsifikatsiyasida avval e'lon qilingan, effectively final o'zgaruvchining turishi mumkinligi
- Herbert Schildt, *Java The Complete Reference*, 12-nashr, McGraw Hill, 2022, 13-bob (339-bet) - `assert (n = getnum()) > 0` kabi yon ta'sirli assertion ning assertion o'chirilganda mantiqni o'chirishi
- Herbert Schildt, *Java The Complete Reference*, 12-nashr, McGraw Hill, 2022, 23-bob (782-bet) - `ByteBuffer` ning o'qish va yozish orasida `flip`/`rewind` bilan qayta tiklanishi sharti
- Boyarsky/Selikoff, *OCP Java SE 17 Study Guide*, 11-bob (622-bet) - `try-with-resources` ga qo'lda yozilgan `finally` ning yashirin `close()` dan keyin bajarilishi
- Boyarsky/Selikoff, *OCP Java SE 17 Study Guide*, 14-bob ("Introducing I/O Streams") - `ObjectInputStream` ning `available()` metodi oqim oxirini aniqlash uchun ishlamasligi, oxirning `EOFException` bilan yoki sanoqni oldin yozib qo'yish bilan aniqlanishi
- Paul Deitel va Harvey Deitel, *Java How to Program*, 10-nashr, Pearson, 15-bob (650-bet) - fayl mavjudligini tekshirgandan keyin ham amalning `IOException` tashlashi mumkinligi, chunki fayl oradagi vaqtda o'chirilishi mumkin
- Joshua Bloch, *Effective Java* 3rd, Item 49 - parametr yaroqliligini tekshirish
- Herbert Schildt, *Java The Complete Reference*, 22, 23-boblar - `java.io` va NIO fayl API si
- [JEP 400: UTF-8 by Default](https://openjdk.org/jeps/400) - JDK 18 dan beri sukut kodirovka UTF-8
- Boyarsky/Selikoff, *OCP Java SE 17 Study Guide*, 14-bob - `Path`, `Files` va oqim bilan fayl o'qish
- Steve McConnell, *Code Complete*, 2-nashr, 8.6 (206-bet) - offensive programming: development da ko'zga tashlanadigan, production da tiklanadigan xato
- Steve McConnell, *Code Complete*, 2-nashr, 8.6 (207-208-bet) - debug yordamchilarini olib tashlashni rejalashtirish va debugging stub
- Jack Shirazi, *Java Performance Tuning*, 2-nashr, O'Reilly, 2003, 8.3-bo'lim "From Raw I/O to Smokin' I/O" - buferlanmagan `FileInputStream` ning jarayonni I/O ga bog'lab qo'yishi, `BufferedInputStream` bilan o'rash vaqtni bir tartibga qisqartirishi va default bufer o'rniga 8 KB bufer sezilarli farq bermasligi
- ESLATMA: Shirazi ning o'lchovi JDK 1.1-1.4 davrida va `DataInputStream.readLine` bilan qilingan; uning raqamlari eskirgan, zamonaviy shakl (`Files.newBufferedReader`, `Files.lines`) shu korpusning tavsiyasi

---

[&larr; 18. Xato bilan ishlash qoidalari](18-xato-bilan-ishlash-qoidalari.md) · [Mundarija](README.md) · [20. Primitiv, son va pul &rarr;](20-primitiv-son-va-pul.md)
