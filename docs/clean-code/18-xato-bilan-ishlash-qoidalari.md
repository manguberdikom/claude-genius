<!-- doc: clean-code | chapter: 18 | part: VI. Xato bilan ishlash -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 18. Xato bilan ishlash qoidalari (Error Handling Rules)

<details>
<summary>Bu bobdagi 14 bo'lim</summary>

- [18.1 Xato kodi emas, istisno](#181-xato-kodi-emas-istisno)
- [18.2 `try-catch-finally` ni birinchi yozish](#182-try-catch-finally-ni-birinchi-yozish)
- [18.3 Istisnoni chaqiruvchi ehtiyojiga qarab aniqlash](#183-istisnoni-chaqiruvchi-ehtiyojiga-qarab-aniqlash)
- [18.4 `try` blokini alohida funksiyaga chiqarish](#184-try-blokini-alohida-funksiyaga-chiqarish)
- [18.5 Xato bilan ishlash ham bitta ish](#185-xato-bilan-ishlash-ham-bitta-ish)
- [18.6 Normal oqimni aniqlash va maxsus holat obyekti](#186-normal-oqimni-aniqlash-va-maxsus-holat-obyekti)
- [18.7 `null` qaytarmaslik va `null` uzatmaslik](#187-null-qaytarmaslik-va-null-uzatmaslik)
- [18.8 Bo'sh to'plam qaytarish qoidasi](#188-bosh-toplam-qaytarish-qoidasi)
- [18.9 Istisnoni oqim boshqarish uchun ishlatmaslik](#189-istisnoni-oqim-boshqarish-uchun-ishlatmaslik)
- [18.10 Tez to'xtash (fail fast) va chegarada tekshirish](#1810-tez-toxtash-fail-fast-va-chegarada-tekshirish)
- [18.11 Standart istisnolardan foydalanish](#1811-standart-istisnolardan-foydalanish)
- [18.12 To'g'rilik va mustahkamlik: javob bera olmaganda to'xtash yoki davom etish](#1812-togrilik-va-mustahkamlik-javob-bera-olmaganda-toxtash-yoki-davom-etish)
- [18.13 Himoya tekshiruvining qanchasi ishlab chiqarishda qoladi](#1813-himoya-tekshiruvining-qanchasi-ishlab-chiqarishda-qoladi)
- [18.14 Amalda qo'llash](#1814-amalda-qollash)

</details>


Istisno dizayni, tekshiriladigan va tekshirilmaydigan istisnolar tanlovi arxitektor hujjatidagi [istisnolar dizayni](../architect/13-zamonaviy-java-tili-va-api-dizayni.md#137-istisnolar-dizayni-tekshiriladigan-va-tekshirilmaydigan-oz-ierarxiyangiz) bo'limida, [istisno orqali muloqot](../architect/04-kod-muloqot-vositasi-nomlash-aniqlik.md#46-xato-va-istisnolar-orqali-muloqot) esa o'sha hujjatning nomlash bobida ko'rilgan. Bu bobda qolgan qoidalar: xato kodidan voz kechish, `try` blokini ajratish, normal oqimni aniqlash, `null` siyosati, va chegarada tez to'xtash.

## 18.1 Xato kodi emas, istisno

Xato kodini qaytarish chaqiruvchini darhol tekshirishga majbur qiladi va tekshiruv unutilsa, xato jim yo'qoladi. Bundan tashqari, xato kodi asosiy mantiqni shart bilan to'ldiradi va kodni chuqurlashtiradi.

```java
// yomon: xato kodi - tekshiruv unutilsa, xato yo'qoladi
public int deletePage(Page page) {
    if (page == null) return ERROR_NULL_PAGE;
    if (!registry.contains(page)) return ERROR_NOT_FOUND;
    registry.delete(page);
    return OK;
}
// chaqiruvchi:
if (deletePage(page) == OK) {
    if (registry.deleteReference(page.name) == OK) { ... }   // chuqurlashadi
}

// yaxshi: istisno - normal oqim toza qoladi
public void deletePage(Page page) {
    registry.delete(page);         // topilmasa PageNotFoundException tashlaydi
    references.delete(page.name());
}
```

Bitta istisno: **kutilayotgan** yo'qlik xato emas. `findById` topilmasa `Optional.empty()` qaytaradi, istisno tashlamaydi (2.11 dagi nomlash taqsimoti).

## 18.2 `try-catch-finally` ni birinchi yozish

Xato bilan ishlashni keyin qo'shish deyarli har doim yarim ishlaydi: resurslar yopilmagan, holat yarim o'zgargan bo'lib qoladi. To'g'ri tartib - `try` blokini birinchi yozish va u "qolgan kod uchun qamrov" yaratadi.

TDD kontekstida bu aniq qadamga aylanadi: oldin istisno kutadigan test yozish, keyin `try/catch` qo'shish, keyin ichini to'ldirish ([31-bob](31-tdd-intizomi-va-kod-dizayniga-tasiri.md)).

```java
// Birinchi qadam: xato yo'lini test bilan belgilash
@Test
void throwsWhenFileMissing() {
    assertThatThrownBy(() -> importer.importFile(Path.of("yo'q.csv")))
            .isInstanceOf(SettlementFileUnavailableException.class);
}

// Ikkinchi qadam: try/catch qamrovi, keyin ichi
public void importFile(Path file) {
    try (var lines = Files.lines(file, UTF_8)) {
        apply(parse(lines));
    } catch (NoSuchFileException e) {
        throw new SettlementFileUnavailableException(file, e);
    } catch (IOException e) {
        throw new SettlementFileUnreadableException(file, e);
    }
}
```

## 18.3 Istisnoni chaqiruvchi ehtiyojiga qarab aniqlash

Istisno sinflarini **manba** bo'yicha emas, **chaqiruvchi nima qilishi** bo'yicha ajratish kerak. Agar chaqiruvchi beshta istisno turini bir xil qayta ishlasa, beshta tur kerak emas.

```java
// yomon: chaqiruvchi uchta istisnoni bir xil qayta ishlaydi
try {
    port.open();
} catch (DeviceResponseException e) {
    log.error("qurilma javobi", e); throw new PortUnavailable(e);
} catch (ATM1212UnlockedException e) {
    log.error("qulf", e); throw new PortUnavailable(e);
} catch (GMXError e) {
    log.error("gmx", e); throw new PortUnavailable(e);
}

// yaxshi: past darajali API wrapper bilan o'ralgan, bitta ma'noli istisno
try {
    port.open();          // LocalPort ichida past darajali istisnolar o'raladi
} catch (PortDeviceFailure e) {
    log.error("port ochilmadi: {}", port.name(), e);
    throw e;
}
```

Shu uslub "o'rash" (wrapping) deb ataladi va u uchinchi tomon kutubxonasiga bog'liqlikni ham kamaytiradi: kutubxona almashtirilsa, faqat wrapper o'zgaradi.

O'rash ham bepul emas, shuning uchun uni **ortiqcha ishlatmaslik** kerak: har qatlamda qayta o'ralgan istisno stack trace ni uzaytiradi va sababni topishni qiyinlashtiradi. Qarorlar tartibi uch bosqichli va yuqoridan pastga qaraladi.

| Bosqich | Nima qilinadi | Qachon |
|---|---|---|
| 1. Oldini olish | yuqori metod parametrlarini past qatlamga uzatishdan **oldin** tekshirish | tekshirish mumkin bo'lganda: eng arzon yo'l, istisno umuman tug'ilmaydi |
| 2. Chetlab o'tish | past qatlam istisnosini yuqori qatlamda jimgina chetlab o'tib log qilish | holatni chaqiruvchidan yashirish mumkin bo'lganda va ish davom etishi kerak bo'lganda |
| 3. Tarjima | istisnoni abstraksiyaga mos istisnoga o'rash, sabab bilan | yuqori ikkisi mumkin bo'lmaganda |

Ya'ni tarjima oxirgi variant, birinchi emas. Ikkinchi bosqichda log yozish majburiy: istisno chaqiruvchidan yashirilgani uchun uning yagona izi log bo'lib qoladi ([log qilish yoki tashlash](19-istisno-mexanikasi-va-resurslar.md#197-log-qilish-yoki-tashlash-ikkisini-birga-qilmaslik)).

## 18.4 `try` blokini alohida funksiyaga chiqarish

`try/catch` bloki kodni chalkashtiradi, chunki u normal oqimni ham, xato oqimini ham bir funksiyada saqlaydi. Yechim: `try` blokining ichini alohida funksiyaga chiqarish, shunda tashqi funksiya faqat xato bilan ishlashni ko'rsatadi.

```java
// yaxshi: ikki funksiya, ikki javobgarlik
public void delete(Page page) {
    try {
        deletePageAndAllReferences(page);
    } catch (Exception e) {
        logError(e);
    }
}

private void deletePageAndAllReferences(Page page) throws Exception {
    page.delete();
    registry.deleteReference(page.name());
    configKeys.deleteKey(page.name().makeKey());
}

private void logError(Exception e) {
    log.error("sahifani o'chirishda xato", e);
}
```

## 18.5 Xato bilan ishlash ham bitta ish

Agar funksiyada `try` kalit so'zi bo'lsa, u `try` dan boshlanishi va `catch`/`finally` dan keyin tugashi kerak. Ya'ni xato bilan ishlash - funksiyaning **bitta** ishi va unga biznes mantiqi qo'shilmaydi (4.2 ning tatbiqi).

```java
// yomon: try bloki ichida ham biznes mantiqi, ham xato ishlovi
public void settle(Payment payment) {
    Money fee = feeFor(payment);              // try dan tashqarida biznes mantiqi
    try {
        gateway.settle(payment, fee);
        payment.markSettled();
        auditLog.record(payment);
    } catch (GatewayTimeout e) {
        payment.markPending();
        retryQueue.add(payment);
    }
}

// yaxshi: xato ishlovi alohida, normal oqim alohida
public void settle(Payment payment) {
    try {
        settleNow(payment);
    } catch (GatewayTimeout e) {
        scheduleRetry(payment, e);
    }
}
```

## 18.6 Normal oqimni aniqlash va maxsus holat obyekti

Ba'zan istisno umuman kerak emas: "yo'q" holati normal va uni obyekt bilan ifodalash mumkin (Special Case pattern). Shunda chaqiruvchida `try/catch` ham, `null` tekshiruvi ham qolmaydi.

```java
// yomon: istisno oqim boshqarish uchun ishlatilgan
try {
    MealExpenses expenses = expenseReport.getMeals(employeeId);
    total += expenses.getTotal();
} catch (MealExpensesNotFound e) {
    total += getMealPerDiem();      // "yo'q" holati - bu xato emas
}

// yaxshi: maxsus holat obyekti standart xatti-harakatni o'zida ushlaydi
MealExpenses expenses = expenseReport.getMeals(employeeId);   // har doim obyekt qaytadi
total += expenses.getTotal();

public final class PerDiemMealExpenses implements MealExpenses {
    @Override public Money getTotal() { return PER_DIEM; }
}
```

## 18.7 `null` qaytarmaslik va `null` uzatmaslik

`null` qaytarish chaqiruvchiga ish yuklaydi va bir joyda unutilsa `NullPointerException` beradi. `null` uzatish esa undan yomoni: metod ichida uni tekshirishning ishonchli usuli yo'q.

| Holat | `null` o'rniga |
|---|---|
| Topilmasligi mumkin | `Optional<T>` |
| Bo'sh to'plam | `List.of()` (18.8) |
| Standart xatti-harakat | maxsus holat obyekti (18.6) |
| Haqiqiy xato | istisno |
| Ixtiyoriy parametr | overload yoki builder (5.9) |
| Ixtiyoriy maydon | `Optional` getter, maydon `null` (24.1 chegarasi) |
| Tashqi ma'lumot (JSON) | validatsiya chegarada |

```java
// yomon
public List<Employee> getEmployees() {
    if (noEmployees) return null;       // chaqiruvchi tekshirishga majbur
}
for (Employee e : getEmployees()) { ... }   // NPE

// yaxshi
public List<Employee> getEmployees() {
    return employees == null ? List.of() : List.copyOf(employees);
}
```

## 18.8 Bo'sh to'plam qaytarish qoidasi

Metod to'plam qaytarsa, u hech qachon `null` qaytarmasligi kerak - bu Java da eng kam bahsli qoidalardan biri. `List.of()` va `Collections.emptyList()` ikkisi ham o'zgarmas va deyarli bepul (umumiy nusxa).

Shu qoidaning `Map`, `Set`, `Stream` va massiv uchun ekvivalentlari: `Map.of()`, `Set.of()`, `Stream.empty()`, `new String[0]`.

Massiv qaytarishda yonma-yon turadigan qoida ham bor: `toArray` ga uzatiladigan massivni ishlash uchun **oldindan ajratmang**. `list.toArray(new String[list.size()])` shakli tezroq ko'rinadi, lekin o'lchovlar bunday qilish zararli ekanini ko'rsatgan va zamonaviy JVM da nol uzunlikdagi massiv tezroq. Bundan tashqari o'lchamni oldin hisoblash ko'p threadli muhitda xato manbai: `size()` va `toArray` orasida to'plam o'sib ketsa, qaytgan massiv qisqartirilib qoladi. Shuning uchun yagona shakl - `new String[0]`, va u konstantaga chiqariladi.

```java
// yomon: oldindan ajratish - foydasi yo'q, poyga sharti bor
return names.toArray(new String[names.size()]);

// yaxshi: nol uzunlikdagi massiv, konstanta sifatida
private static final String[] EMPTY_NAMES = new String[0];

return names.toArray(EMPTY_NAMES);
```

## 18.9 Istisnoni oqim boshqarish uchun ishlatmaslik

Istisno **istisnoli** holat uchun. Normal oqimda istisno tashlash uch zarar keltiradi: stack trace yaratish qimmat (issiq yo'lda sezilarli), kod o'qilmaydi, va haqiqiy xatolar shovqin ichida ko'rinmay qoladi.

```java
// yomon: sikl oxirini istisno bilan aniqlash
try {
    int i = 0;
    while (true) {
        total += items[i++].price();
    }
} catch (ArrayIndexOutOfBoundsException e) {
    // sikl tugadi
}

// yaxshi
for (Item item : items) {
    total = total.add(item.price());
}
```

Shu qoidaning amaliy shakli: validatsiya uchun `try { Integer.parseInt(s) } catch` o'rniga oldindan tekshirish yoki `Optional` qaytaradigan parser ishlatish.

Shu yerda tekshiriladigan istisnoning narxi ham ko'rinadi: u chaqiruvchini `try-catch` ga majburlaydi va lambda ichida ishlatilmaydi ([tekshiriladigan istisno va lambda](24-lambda-oqim-va-funksional-uslub-tozaligi.md#247-tekshiriladigan-istisno-va-lambda)). Metodda yagona tekshiriladigan istisno qolgan bo'lsa, uni olib tashlashning ikki yo'li bor. Birinchisi: natijani `Optional` qilib qaytarish, shunda "bajarilmadi" holati qaytish turida ko'rinadi (kamchiligi: sabab haqida ma'lumot yo'qoladi). Ikkinchisi: metodni ikkiga bo'lish - holatni tekshiradigan metod va amalni bajaradigan metod, bajaruvchisi esa tekshirilmaydigan istisno tashlaydi (`hasNext` va `next` shakli). Ikkinchi yo'l ko'p threadli muhitda ehtiyot talab qiladi: tekshiruv va amal orasida holat o'zgarishi mumkin.

## 18.10 Tez to'xtash (fail fast) va chegarada tekshirish

Xato qanchalik manbaga yaqin aniqlansa, uni tuzatish shunchalik arzon. Shu sababli noto'g'ri ma'lumot tizimga kirishi bilan to'xtatilishi kerak, ichkariga tarqalib ketmasligi kerak.

Amalda bu 5.11 dagi validatsiya taqsimoti bilan amalga oshadi: tashqi chegarada format va majburiylik, value object konstruktorida invariant, domen metodida biznes qoidasi. Ichki metodlar esa tekshirmaydi - ular allaqachon to'g'ri ma'lumot oladi.

```java
// Chegarada: format, majburiylik, diapazon
@PostMapping("/refunds")
ResponseEntity<RefundResponse> refund(@Valid @RequestBody RefundRequest request) { ... }

// Value object: invariant - yaroqsiz obyekt tug'ilmaydi
public record Quantity(int value) {
    public Quantity {
        if (value <= 0) throw new IllegalArgumentException("quantity musbat: " + value);
    }
}

// Domen: biznes qoidasi
public void refund(Money amount) {
    if (amount.greaterThan(refundableAmount())) {
        throw new RefundExceedsPaymentException(id, amount, refundableAmount());
    }
}
```

## 18.11 Standart istisnolardan foydalanish

Har bir xato holati uchun yangi istisno sinfi yozish kod bazasini kattalashtiradi va o'quvchiga hech narsa qo'shmaydi: `InvalidOrderQuantityException` nomi `IllegalArgumentException` dan ko'proq ma'lumot bermaydi, chunki sabab xabarda yoziladi. Qoida: platformaning standart istisnosi ma'noga mos kelsa, shu ishlatiladi.

| Holat | Istisno |
|---|---|
| Argument qiymati noto'g'ri | `IllegalArgumentException` |
| Argument `null` bo'lmasligi kerak edi | `NullPointerException` |
| Indeks oraliqdan tashqarida | `IndexOutOfBoundsException` |
| Obyekt holati bu chaqiruvga tayyor emas | `IllegalStateException` |
| Operatsiya bu implementatsiyada yo'q | `UnsupportedOperationException` |
| Hisob arifmetik qoidani buzdi | `ArithmeticException` |
| Taqiqlangan joyda bir vaqtda o'zgartirish aniqlandi | `ConcurrentModificationException` |

```java
// yomon: standart istisnoni takrorlaydigan o'z sinfi
if (quantity <= 0) {
    throw new InvalidOrderQuantityException("quantity=" + quantity);
}

// yaxshi: standart istisno, xabarda kontekst bilan
if (quantity <= 0) {
    throw new IllegalArgumentException("quantity musbat bo'lishi kerak, berilgan: " + quantity);
}
```

`ConcurrentModificationException` ni ishlatganda bitta tafsilotni bilish kerak: u faqat **ishora**. Istisno bitta thread uchun mo'ljallangan obyekt bir vaqtda o'zgartirilayotganini aniqlaganda tashlanadi, lekin bir vaqtda o'zgartirishni ishonchli aniqlashning umuman yo'li yo'q: to'plamlar buni arzon hisoblagich bilan taxmin qiladi, shuning uchun istisno kelmasligi ham mumkin. Natijada `ConcurrentModificationException` ni **ushlab** mantiq qurish xato: u faqat xatoni erta ko'rsatadigan vosita, kafolat emas. To'g'ri yechim sinxronlash yoki `ConcurrentHashMap` kabi tur tanlash.

O'z istisno sinfi haqli bo'ladigan ikki holat bor. Birinchisi: chaqiruvchi shu xatoni **alohida** ushlab, boshqa yo'l tanlashi kerak (`InsufficientFundsException` ni ushlab, boshqa to'lov usuliga o'tish). Ikkinchisi: istisno xabarda sig'maydigan ma'lumot tashiydi (qolgan balans, kutish muddati, qayta urinish vaqti). Ikkisi ham yo'q bo'lsa, standart istisno yetadi. `IllegalArgumentException` va `IllegalStateException` orasidagi tanlov qoidasi: argument qiymatidan qat'i nazar chaqiruv noto'g'ri bo'lsa, bu holat xatosi; aks holda argument xatosi.

Uchinchi dalil ham bor va u o'z sinfini yozishdan tiyilish uchun yetarli: standart istisnoni voris olib tafsilot qo'shish mumkin, **lekin istisnolar seriyalanadi**. Seriyalanadigan sinf esa alohida yuk: uning seriyalash shakli de-fakto API ga aylanadi, versiyalar orasida mos kelishi kerak va har bir maydon shu shartnomaga qo'shiladi (25.4). Ya'ni "shunchaki bitta maydon qo'shdim" degan istisno sinfi aslida yangi seriyalash shartnomasini e'lon qiladi. Shuning uchun yaxshi sababsiz o'z istisno sinfi yozilmaydi.

Istisno sinfi haqli deb qaror qilingandan keyin ikkinchi savol keladi: u **tekshiriladigan** bo'ladimi. Mezon ikki shartning **birga** bajarilishi: holatni API ni to'g'ri ishlatish bilan oldini olish mumkin emas, VA programmist istisnoga duch kelganda foydali amal qila oladi. Ikkinchi shart ko'pincha e'tibordan qoladi: "foydali amal" degani qayta urinish, muqobil manbaga o'tish yoki foydalanuvchidan boshqa kiritish so'rash kabi aniq tiklanish yo'li. Chaqiruvchining qila oladigan yagona ishi log yozib yiqilish bo'lsa, tekshiriladigan istisno hech narsa bermaydi va faqat `try-catch` shovqinini keltiradi: bunda tekshirilmaydigan istisno to'g'ri tanlov. Dasturlash xatosi (yaroqsiz argument, noto'g'ri tartibdagi chaqiruv) va tiklanmaydigan holat esa har doim tekshirilmaydigan bo'ladi. To'liq qaror va iyerarxiya dizayni arxitektor hujjatidagi [istisnolar dizayni](../architect/13-zamonaviy-java-tili-va-api-dizayni.md#137-istisnolar-dizayni-tekshiriladigan-va-tekshirilmaydigan-oz-ierarxiyangiz) bo'limida.

Standart istisnoni ishlatish tanlovi API shartnomasining bir qismi: u `@throws` da yoziladi ([`@param`, `@return`, `@throws` to'liqligi](10-javadoc-va-api-hujjati.md#103-param-return-throws-toliqligi)) va keyin uni o'zgartirish buzuvchi o'zgarish bo'ladi.

## 18.12 To'g'rilik va mustahkamlik: javob bera olmaganda to'xtash yoki davom etish

Oldingi bo'limlar istisnoni qanday tashlash va tutishni yozdi, lekin ularning hech biri bitta savolga javob bermaydi: to'g'ri javob berish imkoni yo'q bo'lganda tizim **to'xtaydimi** yoki noto'g'ri javob bilan ishlashda davom etadimi. McConnell bu ikki yo'nalishni bitta o'qning ikki uchi deb qo'yadi (McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 8.3 (197-bet)):

- **To'g'rilik** (correctness) - noto'g'ri natijani hech qachon qaytarmaslik. Javob bermaslik noto'g'ri javob berishdan yaxshi.
- **Mustahkamlik** (robustness) - tizim ishlashda davom etishi uchun doim biror narsa qilishga urinish, natija ba'zan noto'g'ri bo'lishi hisobiga ham.

Ikkisi bir vaqtda maksimal bo'lmaydi: birini oshirish ikkinchisini pasaytiradi. Xavfsizlik uchun kritik va pul bilan ishlaydigan joy to'g'rilik tomonida turadi (radiatsiya dozasi, balans, limit, soliq), ko'rinish va ma'lumot beruvchi joy mustahkamlik tomonida (tavsiyalar, yetkazib berish prognozi). Diqqat: bu [Postel qonuni](../patterns/26-dizayn-printsiplari-solid-grasp-va-umumiy.md#2627-mustahkamlik-printsipi-robustness-principle-postels-law) EMAS. Postel qonuni kirishni qanday qabul qilish haqida, bu yerdagi qaror esa javob bera olmagan paytda nima qilish haqida.

Qaror arxitektura darajasida bir marta qabul qilinadi va izchil qo'llanadi: har bir ishlab chiquvchi o'z joyida o'zi tanlasa, tizimning umumiy xatti-harakati hech bir talabga mos kelmaydi, McConnell "qanday qulay bo'lsa shunday" variantini aynan shu sababdan tanqid qiladi. Tanlangan tomon esa kodda ko'rinadi va o'lchanadi ([arxitektor hujjatidagi degradatsiya rejasi](../architect/07-nosozlik-haqida-fikrlash.md#76-qisman-nosozlikda-nima-qilish-degradatsiya-rejasi-va-zaxira-javob), [patternlar hujjatidagi Fallback](../patterns/17-resilience-va-cloud-dizayn-patternlari.md#177-zaxira-yechim-fallback)).

```java
// To'g'rilik tomoni: javob bera olmasa, javob bermaydi
public Money balance(AccountId id) {
    return ledgerClient.balance(id);     // xato yuqoriga ketadi, "taxminiy balans" yo'q
}

// Mustahkamlik tomoni: past sifatli javob javobsizlikdan yaxshi
public List<Product> recommendations(CustomerId id) {
    try {
        return recommender.forCustomer(id);
    } catch (RecommenderUnavailableException e) {
        metrics.counter("recommendations.degraded").increment();
        return bestSellers.top(TOP_COUNT);   // sifati past, lekin belgilangan va o'lchangan
    }
}
```

Tomon tanlangandan keyin texnika tanlanadi. McConnell beradigan menyu har qatorning narxini ko'rsatadi (8.3 (194-196-bet)):

| Texnika | Nima qiladi | Qachon o'rinli |
|---|---|---|
| Neytral qiymat | zararsiz qiymat qaytaradi: nol, bo'sh satr, default rang | qiymat ko'rinishga ta'sir qiladi, qarorga emas |
| Keyingi yaroqli ma'lumot | buzilgan yozuvni o'tkazib yuboradi | oqim va paketli ishlovda, bitta yozuv hal qilmasa |
| Oldingi javob | oxirgi muvaffaqiyatli qiymatni qaytaradi | qiymat qisqa oraliqda deyarli o'zgarmasa |
| Eng yaqin yaroqli qiymat | diapazondan chiqqanini chegaraga tortadi | kalibrlangan o'lchov, chegarasi ma'lum qiymat |
| Ogohlantirishni log ga yozish | davom etadi, lekin iz qoldiradi | boshqa texnika bilan birga, yolg'iz emas |
| Xatoni yuqoriga uzatish | o'zi hal qilmaydi, xabar beradi | qaror yuqori qatlamda bo'lsa |
| Markaziy xato ishlovchisi | hamma xato bitta joyga boradi | yagona javob shakli kerak bo'lsa, bog'liqlik narxiga rozi bo'lsangiz |
| Xabarni shu joyda ko'rsatish | foydalanuvchiga darhol aytadi | UI matnini butun tizimga tarqatishga rozi bo'lsangiz |
| To'xtash | umuman javob bermaydi | noto'g'ri javobning zarari to'xtash zararidan katta bo'lsa |

Ikki qator Java da aniq shakl oladi. "Xatoni yuqoriga uzatish" `int` holat kodi emas, istisno: McConnell ning o'zi bu texnikaning uch mexanizmidan birini tilning istisno apparati deb sanaydi, shuning uchun [xato kodi emas, istisno](#181-xato-kodi-emas-istisno) qoidasi bilan ziddiyat yo'q - menyu qatori qaysi qatlam hal qilishi haqida, tashish mexanizmi haqida emas. "Neytral qiymat" esa [bo'sh to'plam qaytarish qoidasi](#188-bosh-toplam-qaytarish-qoidasi) ko'rinishida haqli, pul yoki ruxsat hisobida esa haqli emas: u yerda [tez to'xtash](#1810-tez-toxtash-fail-fast-va-chegarada-tekshirish) ishlaydi.

Mustahkamlik tomonining o'z chegarasi bor. Ousterhout buni haddan oshirish deb nomlaydi: istisnoni modul ichida yashirish faqat shu ma'lumot moduldan tashqarida kerak bo'lmaganda ma'noli. Uning misolida jamoa tarmoq moduli ichida hamma tarmoq istisnosini tutib tashlagan; natijada moduldan foydalanadigan ilova xabar yo'qolganini ham, qarshi tomondagi server yiqilganini ham bilib ololmagan, ya'ni mustahkam ilova yozish imkonsiz bo'lgan (Ousterhout, *A Philosophy of Software Design*, 1-nashr, Yaknyam Press, 2018, 10.10). Qoida shundan chiqadi: muhim bo'lmagan narsa yashiriladi, muhim narsa oshkor qilinadi. Jim yashirilgan xato mustahkamlik emas, bilib bo'lmaydigan noto'g'ri javob.

## 18.13 Himoya tekshiruvining qanchasi ishlab chiqarishda qoladi

Himoya kodining paradoksi: development da xato **ko'zga tashlanishi** kerak, hatto bezor bo'lsa ham, chunki sezilmagan xato tuzatilmaydi; production da esa shu xato iloji boricha sezilmasligi, tizim esa tiklanishi yoki chiroyli yiqilishi kerak. Shuning uchun "hamma tekshiruv qolsin" ham, "hammasi olinsin" ham javob emas: tekshiruvlar toifaga bo'linadi (McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 8.7 (209-210-bet)).

| Tekshiruv | Production da |
|---|---|
| Muhim xatoni ushlaydigani (hisob-kitob, pul, ruxsat) | **qoladi** |
| Oqibati chindan ham arzimas bo'lgani (ko'rinish, kosmetik nomuvofiqlik) | olinadi yoki jim log ga tushadi |
| Qattiq yiqilishga olib keladigani (ma'lumot yo'qolishi bilan) | **olinadi**: foydalanuvchi ishini saqlashga ulgursin |
| Chiroyli yiqilishga yordam beradigani | **qoladi** |
| Development da to'xtatadigan assertion | xatti-harakati o'zgaradi: log ga yozadi, to'xtatmaydi |

Ikki izoh shu jadvalga tegishli. Birinchisi: "olinadi" manba kodidan o'chirish degani emas, build yoki sozlama darajasida o'chirish degani - kod joyida qoladi, shunda keyingi tahrirda uni qaytarib yurish kerak bo'lmaydi. Ikkinchisi: chiroyli yiqilishga yordam beradigan tekshiruvni ataylab qoldirish real foyda bergan - Mars Pathfinder da injenerlar debug yordamchilarining bir qismini qasddan qoldirgan, qo'nishdan keyin yuzaga kelgan xatoni aynan shular bilan aniqlagan va tuzatilgan kodni yuklab, missiyani oxirigacha olib borgan.

Production da qoladigan tekshiruvning xabari esa foydalanuvchi ko'radigan matn bo'lib qoladi, shuning uchun u ichki jargon bilan emas, [uch xil adresat qoidasi](19-istisno-mexanikasi-va-resurslar.md#1910-xato-xabari-matni-uch-xil-adresat) bo'yicha yoziladi va yonida xatoni xabar qilish yo'li turadi.

Oxirgi va eng oson esdan chiqadigan qoida: himoya kodining o'zi ham kod. Har parametrni har joyda har tomondan tekshirish programmani sekin va semiz qiladi, lekin asosiy zarari boshqa - u murakkablikni oshiradi va himoya kodi xatodan xoli emas. Shoshib yozilgan tekshiruvda xato topilish ehtimoli oddiy koddan **kamroq emas**, ko'proq (McConnell, 8.8 (210-bet)). Shuning uchun himoya ham ustuvorlik bilan joylashtiriladi: u chegarada va invariant tug'ilish joyida zich bo'ladi ([tez to'xtash va chegarada tekshirish](#1810-tez-toxtash-fail-fast-va-chegarada-tekshirish)), chegaradan ichkarida esa siyraklashadi.

## 18.14 Amalda qo'llash

- [ ] Xato kodi qaytaradigan metodlarni (`int` holat, `boolean` muvaffaqiyat) istisnoga yoki `Optional` ga o'tkazing.
- [ ] To'plam qaytaradigan barcha metodlarda `null` qaytarilmasligini tekshirib, `List.of()` ga o'tkazing.
- [ ] `null` parametr kutadigan public metodlarni overload yoki builder bilan almashtiring.
- [ ] Uchinchi tomon kutubxonasining istisnolarini wrapper ichida o'rab, chaqiruvchi uchun ma'noli turlar bering.
- [ ] `try` bloki ichida biznes mantiqi bor funksiyalarni ikkiga bo'lib, xato ishlovini ajratib bering.
- [ ] Oqim boshqarish uchun istisno ishlatilgan joylarni (`catch (ArrayIndexOutOfBounds)`) oddiy shartga aylantiring.
- [ ] "Yo'q" holati normal bo'lgan joylarni maxsus holat obyekti bilan ifodalab, `catch` bloklarini olib tashlang.
- [ ] Validatsiyani 5.11 taqsimoti bo'yicha chegaraga ko'chirib, ichki metodlardagi takroriy tekshiruvlarni o'chiring.
- [ ] O'z istisno sinflarini sanab, har biri uchun savol bering: chaqiruvchi uni alohida ushlaydimi yoki qo'shimcha ma'lumot tashiydimi; ikkisi ham yo'q bo'lsa standart istisnoga o'tkazing.
- [ ] Har bir tashqi bog'liqlik uchun yozib qo'ying: javob bo'lmasa to'g'rilik tomonida to'xtaymizmi yoki mustahkamlik tomonida past sifatli javob beramizmi.
- [ ] Istisnoni tutib jim davom etadigan `catch` bloklarini topib, yashirilgan ma'lumot chaqiruvchiga kerakmi degan savolni bering.
- [ ] Production da qoladigan va olinadigan tekshiruvlarni ro'yxatlab, "olinadi" deganini build yoki sozlama bilan o'chiring, manbadan o'chirmang.

## Manbalar

- Joshua Bloch, *Effective Java* 3rd, Item 69 - istisno faqat istisno holat uchun
- Joshua Bloch, *Effective Java* 3rd, Item 70, 71 - tekshiriladigan va tekshirilmaydigan istisno tanlovi
- Joshua Bloch, *Effective Java* 3rd, Item 71 (298-bet) - tekshiriladigan istisno faqat ikki shart birga bajarilganda haqli bo'lishi: holatni API ni to'g'ri ishlatish bilan oldini olish mumkin emasligi va programmistning foydali amal qila olishi
- Joshua Bloch, *Effective Java* 3rd, Item 72 (300-bet) - `ConcurrentModificationException` ning faqat ishora bo'lishi: bir vaqtda o'zgartirishni ishonchli aniqlash mumkin emasligi
- Joshua Bloch, *Effective Java* 3rd, Item 72 (301-bet) - istisnolarning seriyalanishi va bu yukning o'z istisno sinfini yaxshi sababsiz yozmaslik uchun yetarli dalil bo'lishi
- Joshua Bloch, *Effective Java* 3rd, Item 73 (303-bet) - istisno tarjimasini ortiqcha ishlatmaslik: eng yaxshi yo'l past qatlam istisnosining oldini olish, keyingisi uni yuqori qatlamda chetlab o'tib log qilish
- Joshua Bloch, *Effective Java* 3rd, Item 54 (248-bet) - `toArray` ga uzatiladigan massivni ishlash uchun oldindan ajratmaslik va nol uzunlikdagi massiv uzatish
- ESLATMA: Liang (*Introduction to Java Programming*, 9-nashr, Pearson, 2013, 14-bob, 540-bet) o'z istisno sinfini `Exception` dan voris olib TEKSHIRILADIGAN qilishni talab qiladi; korpus esa tekshirilmaydiganni afzal ko'radi (arxitektor hujjatidagi istisnolar dizayni). Ikkisini ajratuvchi shart yuqorida yozilgan: tekshiriladigan istisno faqat chaqiruvchi uchun ma'noli tiklanish yo'li (qayta urinish, muqobil manba) bo'lganda tanlanadi, dasturlash xatosi va tiklanmaydigan holat esa tekshirilmaydigan bo'ladi
- Joshua Bloch, *Effective Java* 3rd, Item 72 - standart istisnolardan foydalanish
- Joshua Bloch, *Effective Java* 3rd, Item 73 - abstraksiyaga mos istisno tashlash
- Joshua Bloch, *Effective Java* 3rd, Item 54 - `null` emas, bo'sh to'plam qaytarish
- Robert C. Martin, *Clean Code*, 7-bob - xato kodi emas istisno, maxsus holat obyekti, `null` qaytarmaslik
- Joshua Bloch, *Effective Java* 3rd, Item 71 - yagona tekshiriladigan istisnoni olib tashlashning ikki yo'li: `Optional` va holat tekshiruvchi metod
- Robert C. Martin, *Clean Code*, 7-bob - `ACMEPort` namunasi: uchta past darajali istisnoni bitta ma'noli istisnoga o'rash
- Steve McConnell, *Code Complete*, 2-nashr, 8.3 (194-196-bet) - xato bilan ishlash texnikalari menyusi
- Steve McConnell, *Code Complete*, 2-nashr, 8.3 (197-bet) - to'g'rilik va mustahkamlik orasidagi tanlov, qaror arxitektura darajasida
- Steve McConnell, *Code Complete*, 2-nashr, 8.7 (209-210-bet) - qaysi himoya tekshiruvi ishlab chiqarishda qoladi, Mars Pathfinder misoli
- Steve McConnell, *Code Complete*, 2-nashr, 8.8 (210-bet) - ortiqcha himoya kodining o'zi xato manbai
- John Ousterhout, *A Philosophy of Software Design*, 1-nashr, 10.10 - xatoni yo'q qilishni haddan oshirish: muhim ma'lumot oshkor qilinadi

---

[&larr; 17. Vorislik, kompozitsiya va polimorfizm mexanikasi](17-vorislik-kompozitsiya-va-polimorfizm.md) · [Mundarija](README.md) · [19. Istisno mexanikasi va resurslar &rarr;](19-istisno-mexanikasi-va-resurslar.md)
