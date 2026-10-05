<!-- doc: clean-code | chapter: 18 | part: VI. Xato bilan ishlash -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 18. Xato bilan ishlash qoidalari (Error Handling Rules)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

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
- [18.11 Amalda qo'llash](#1811-amalda-qollash)

</details>


Istisno dizayni, tekshiriladigan va tekshirilmaydigan istisnolar tanlovi [arxitektor hujjatidagi](../architect/README.md) istisnolar dizayni bo'limida, istisno orqali muloqot esa 4.6 da ko'rilgan. Bu bobda qolgan qoidalar: xato kodidan voz kechish, `try` blokini ajratish, normal oqimni aniqlash, `null` siyosati, va chegarada tez to'xtash.

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

## 18.11 Amalda qo'llash

- [ ] Xato kodi qaytaradigan metodlarni (`int` holat, `boolean` muvaffaqiyat) istisnoga yoki `Optional` ga o'tkazing.
- [ ] To'plam qaytaradigan barcha metodlarda `null` qaytarilmasligini tekshirib, `List.of()` ga o'tkazing.
- [ ] `null` parametr kutadigan public metodlarni overload yoki builder bilan almashtiring.
- [ ] Uchinchi tomon kutubxonasining istisnolarini wrapper ichida o'rab, chaqiruvchi uchun ma'noli turlar bering.
- [ ] `try` bloki ichida biznes mantiqi bor funksiyalarni ikkiga bo'lib, xato ishlovini ajratib bering.
- [ ] Oqim boshqarish uchun istisno ishlatilgan joylarni (`catch (ArrayIndexOutOfBounds)`) oddiy shartga aylantiring.
- [ ] "Yo'q" holati normal bo'lgan joylarni maxsus holat obyekti bilan ifodalab, `catch` bloklarini olib tashlang.
- [ ] Validatsiyani 5.11 taqsimoti bo'yicha chegaraga ko'chirib, ichki metodlardagi takroriy tekshiruvlarni o'chiring.

---

[&larr; 17. Vorislik, kompozitsiya va polimorfizm mexanikasi](17-vorislik-kompozitsiya-va-polimorfizm.md) · [Mundarija](README.md) · [19. Istisno mexanikasi va resurslar &rarr;](19-istisno-mexanikasi-va-resurslar.md)
