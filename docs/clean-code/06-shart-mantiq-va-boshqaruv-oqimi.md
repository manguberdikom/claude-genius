<!-- doc: clean-code | chapter: 6 | part: II. Funksiya va boshqaruv oqimi -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 6. Shart, mantiq va boshqaruv oqimi (Conditionals and Control Flow)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

- [6.1 Shartni nomlash va inkapsulyatsiya qilish](#61-shartni-nomlash-va-inkapsulyatsiya-qilish)
- [6.2 Inkor shartdan qochish va De Morgan qoidasi](#62-inkor-shartdan-qochish-va-de-morgan-qoidasi)
- [6.3 Murakkab mantiqni soddalashtirish](#63-murakkab-mantiqni-soddalashtirish)
- [6.4 `else` ni yo'q qilish usullari](#64-else-ni-yoq-qilish-usullari)
- [6.5 Ternar operatori: qachon o'qiladi](#65-ternar-operatori-qachon-oqiladi)
- [6.6 `switch` ni toza ishlatish: to'liqlik, `default`, fallthrough](#66-switch-ni-toza-ishlatish-toliqlik-default-fallthrough)
- [6.7 Chegaraviy shartlarni inkapsulyatsiya qilish](#67-chegaraviy-shartlarni-inkapsulyatsiya-qilish)
- [6.8 `null` tekshiruvi zinapoyasi va undan chiqish](#68-null-tekshiruvi-zinapoyasi-va-undan-chiqish)
- [6.9 Yashirin vaqt bog'liqligini ko'rinadigan qilish](#69-yashirin-vaqt-bogliqligini-korinadigan-qilish)
- [6.10 Takrorlangan `switch` va turga qarab shoxlanish](#610-takrorlangan-switch-va-turga-qarab-shoxlanish)
- [6.11 Amalda qo'llash](#611-amalda-qollash)

</details>


Erta qaytish va ichma-ich chuqurlik [arxitektor hujjatidagi](../architect/README.md) metod uzunligi va erta qaytish bo'limida berilgan. Bu bobda shartlarning qolgan qoidalari: inkor, mantiqiy soddalashtirish, `else` ni yo'qotish, `switch` ni to'g'ri ishlatish, chegaraviy shartlarni inkapsulyatsiya qilish va yashirin vaqt bog'liqligi.

## 6.1 Shartni nomlash va inkapsulyatsiya qilish

Shart ifodasi uch va undan ko'p operandga yetganda uni nomlash kerak. Nomlash ikki shaklda bo'ladi: mahalliy `boolean` o'zgaruvchi (eng arzon) yoki metod (qayta ishlatiladigan va testlanadigan). Agar shart domen qoidasini ifodalasa, u domen obyektiga ko'chishi kerak.

```java
// yomon: shart o'quvchidan to'rtta narsani ushlab turishni talab qiladi
if (payment.getStatus() == 1 && payment.getAmount().compareTo(BigDecimal.ZERO) > 0
        && payment.getSettledAt() != null
        && !payment.getCurrency().equals("UZS")) { ... }

// yaxshi: qoida domen obyektida nomlangan va testlanadi
if (payment.isForeignSettled()) { ... }

// Payment ichida:
public boolean isForeignSettled() {
    return status == SETTLED && amount.isPositive() && !currency.equals(Currency.UZS);
}
```

## 6.2 Inkor shartdan qochish va De Morgan qoidasi

Ijobiy shart inkordan tez o'qiladi, chunki ongda qo'shimcha amal talab qilmaydi. Shu sababli `if (!isNotEmpty(list))` kabi ifodalar yo'qotilishi kerak. De Morgan qoidasi bu ishni mexanik qiladi: `!(a && b)` → `!a || !b`, `!(a || b)` → `!a && !b`.

```java
// yomon: ikki inkor va bitta murakkab ifoda
if (!(order.isPaid() && order.isInStock())) {
    reject(order);
}

// yaxshi: ijobiy shart va erta qaytish
if (order.isPaid() && order.isInStock()) {
    accept(order);
    return;
}
reject(order);

// yoki: inkorni domen nomiga aylantirish
if (order.isNotReadyToShip()) { reject(order); }   // nom ijobiy o'qiladi
```

Istisno: guard clause da inkor tabiiy va to'g'ri (`if (order == null) throw ...`), chunki u erta chiqish uchun ishlatiladi.

## 6.3 Murakkab mantiqni soddalashtirish

Mantiqiy ifodalarni qisqartirish ko'pincha mexanik ish. Amaldagi uch harakat: bir xil shart ikki shoxda takrorlansa, uni tashqariga chiqarish; `if (a) return true; else return false;` ni `return a;` ga aylantirish; va bir xil natijaga olib boradigan shartlarni `||` bilan birlashtirish (Consolidate Conditional Expression, [37-bob](37-refaktoring-harakatlari-katalogi-iii-shart.md)).

```java
// yomon
if (customer.isBlocked()) {
    return true;
} else if (customer.hasOverdueInvoice()) {
    return true;
} else {
    return false;
}

// yaxshi
return customer.isBlocked() || customer.hasOverdueInvoice();

// yana yaxshiroq: nomlangan domen qoidasi
return customer.isCreditSuspended();
```

## 6.4 `else` ni yo'q qilish usullari

`else` bloki ko'pincha keraksiz va uni yo'qotish kodni tekislaydi. To'rt usul bor: guard clause bilan erta qaytish, standart qiymatni oldin belgilash, `switch` ifodasiga o'tish, va polimorfizm ([patternlar hujjatidagi](../patterns/README.md) polimorfizm printsipi).

```java
// yomon: ichma-ich if/else zinapoyasi
String label;
if (status == PENDING) {
    label = "Kutilmoqda";
} else if (status == SETTLED) {
    label = "Yopilgan";
} else {
    label = "Noma'lum";
}

// yaxshi: switch ifodasi, to'liqligi kompilyator tomonidan tekshiriladi
String label = switch (status) {
    case PENDING -> "Kutilmoqda";
    case SETTLED -> "Yopilgan";
    case REJECTED, PARTIALLY_REFUNDED -> "Muammoli";
};

// eng yaxshi: label enum ning o'zida yashaydi
String label = status.displayName();
```

## 6.5 Ternar operatori: qachon o'qiladi

Ternar operator bitta oddiy tanlovda `if/else` dan qisqa va o'qiladi. Uch holatda esa zarar qiladi: ichma-ich ishlatilganda, operandlari uzun bo'lganda, va yon ta'siri bo'lganda.

```java
// yaxshi: qisqa va bir tanlov
Money fee = order.isExpress() ? EXPRESS_FEE : STANDARD_FEE;

// yomon: ichma-ich ternar - o'qilmaydi
String tier = total > 1000 ? "GOLD" : total > 500 ? "SILVER" : total > 100 ? "BRONZE" : "NONE";

// yaxshi: tanlov domen metodiga ko'chdi
CustomerTier tier = CustomerTier.forAnnualSpend(total);
```

## 6.6 `switch` ni toza ishlatish: to'liqlik, `default`, fallthrough

Zamonaviy Java da `switch` **ifodasi** (`->` shakli) eski `switch` gapidan ustun, chunki fallthrough xatosi yo'q, har bir shox qiymat qaytaradi va `sealed` tur ustida to'liqligi kompilyator tomonidan tekshiriladi ([arxitektor hujjatidagi](../architect/README.md) sealed interfeys va pattern matching bo'limlari).

Qolgan qoidalar: enum ustida `switch` da `default` yozmaslik (shunda yangi enum a'zosi qo'shilganda kompilyator xato beradi), eski `switch` gapida har bir `case` ni `break` bilan tugatish yoki `->` shakliga o'tish, va `switch` ni past darajali kodda ushlab turish ([patternlar hujjatidagi](../patterns/README.md) polimorfizm bilan almashtirish qoidasi).

```java
// yomon: default bor - yangi enum a'zosi jimgina "Noma'lum" ga tushadi
switch (status) {
    case PENDING: return "Kutilmoqda";
    default: return "Noma'lum";
}

// yaxshi: default yo'q, yangi a'zo kompilyatsiyani buzadi va eslatadi
return switch (status) {
    case PENDING -> "Kutilmoqda";
    case SETTLED -> "Yopilgan";
    case REJECTED -> "Rad etilgan";
    case PARTIALLY_REFUNDED -> "Qisman qaytarilgan";
};
```

## 6.7 Chegaraviy shartlarni inkapsulyatsiya qilish

`i + 1`, `level - 1`, `<=` va `<` farqlari kod bo'ylab tarqalsa, off-by-one xatolari paydo bo'ladi va ularni topish qiyin. Yechim: chegara hisobini bir joyda nomlab qo'yish.

```java
// yomon: level + 1 uch joyda takrorlangan
if (level + 1 < tags.length) {
    parts = new Parse(body, tags, level + 1, offset + endTag);
}

// yaxshi: chegara nomlangan
int nextLevel = level + 1;
if (nextLevel < tags.length) {
    parts = new Parse(body, tags, nextLevel, offset + endTag);
}

// yaxshi: oraliq o'z turiga olingan, inklyuzivlik turda hujjatlangan
record DateRange(LocalDate fromInclusive, LocalDate toExclusive) {
    boolean includes(LocalDate day) {
        return !day.isBefore(fromInclusive) && day.isBefore(toExclusive);
    }
}
```

## 6.8 `null` tekshiruvi zinapoyasi va undan chiqish

Ichma-ich `null` tekshiruvlari eng ko'p uchraydigan chuqurlik manbai. To'rtta chiqish yo'li bor va tartibi shunday: `null` ni manbada yo'qotish (18.7), `Optional` zanjiri (24.6), maxsus holat obyekti (18.6), va faqat chegarada `Objects.requireNonNull`.

```java
// yomon: zanjir bo'ylab null tekshiruvi
if (order != null) {
    Customer c = order.getCustomer();
    if (c != null) {
        Address a = c.getAddress();
        if (a != null && a.getCity() != null) {
            return a.getCity().toUpperCase();
        }
    }
}
return "NOMA'LUM";

// yaxshi: null manbada yo'q, Optional faqat haqiqiy yo'qlik uchun
return order.customer().address()
        .map(Address::city)
        .map(String::toUpperCase)
        .orElse(UNKNOWN_CITY);
```

## 6.9 Yashirin vaqt bog'liqligini ko'rinadigan qilish

Agar metodlarni faqat ma'lum tartibda chaqirish mumkin bo'lsa va bu tartib kodda ko'rinmasa, bu yashirin vaqt bog'liqligi (hidden temporal coupling; [patternlar hujjatida](../patterns/README.md) Sequential Coupling anti-patterni, 25.17). Clean code darajasidagi yechimi: tartibni imzoga olib chiqish.

```java
// yomon: tartib faqat izohda va xotirada
public void run() {
    openConnection();
    authenticate();     // openConnection dan keyin bo'lishi shart
    sendPayload();      // authenticate dan keyin bo'lishi shart
}

// yaxshi: har bir qadam keyingisi uchun kerakli natijani qaytaradi
public void run() {
    Connection connection = openConnection();
    Session session = authenticate(connection);
    sendPayload(session);
}
```

Shu uslub "o'tkazish" (passing a baton) deb ataladi: tartibni buzish kompilyatsiyadan o'tmaydi.

## 6.10 Takrorlangan `switch` va turga qarab shoxlanish

Bir xil `switch` yoki `if/else` zanjiri uch-to'rt joyda takrorlansa, bu hid ([32-bob](32-kod-hidlari-katalogi-i-nom-funksiya-malumot.md), Repeated Switches). Har bir yangi enum a'zosi barcha takrorlarni topishni talab qiladi va bittasi doim esdan chiqadi.

Yechim darajalari: xatti-harakatni enum ichiga ko'chirish (eng arzon), `sealed` interfeys va pattern matching, yoki polimorfizm. Enum ichiga ko'chirish Java da ko'pincha yetarli.

```java
// yaxshi: har bir shox enum a'zosining o'zida
public enum ShippingMethod {
    STANDARD { public Money fee(Weight w) { return Money.of(10_000); } },
    EXPRESS   { public Money fee(Weight w) { return Money.of(25_000); } },
    FREIGHT   { public Money fee(Weight w) { return Money.of(w.kg() * 3_000); } };

    public abstract Money fee(Weight weight);
}
```

## 6.11 Amalda qo'llash

- [ ] Uch va undan ko'p operandli shart ifodalarini topib, har birini nomlangan `boolean` yoki domen metodiga chiqaring.
- [ ] `!(...)` shaklidagi inkor ifodalarni De Morgan bilan soddalashtirib, ijobiy shartga aylantiring.
- [ ] `if (x) return true; else return false;` namunalarini grep qilib, `return x;` ga qisqartiring.
- [ ] Enum ustidagi barcha `switch` lardan `default` ni olib tashlab, to'liqlikni kompilyatorga topshiring.
- [ ] Eski `switch` gaplarini `->` ifodasiga o'tkazib, fallthrough xavfini yo'qoting.
- [ ] Ichma-ich ternar operatorlarni topib, domen metodi yoki `switch` ifodasiga aylantiring.
- [ ] `null` tekshiruvi zanjirlari bor joylarni `Optional` yoki manbadagi `null` ni yo'qotish bilan tekislang.
- [ ] Ma'lum tartibda chaqirilishi shart bo'lgan metod guruhlarini topib, tartibni qaytish turlari orqali majburiy qiling.

---

[&larr; 5. Funksiya argumentlari](05-funksiya-argumentlari.md) · [Mundarija](README.md) · [7. Sikl, iteratsiya va to'plam bilan ishlash &rarr;](07-sikl-iteratsiya-va-toplam-bilan-ishlash.md)
