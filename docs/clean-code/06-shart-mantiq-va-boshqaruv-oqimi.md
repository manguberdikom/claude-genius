<!-- doc: clean-code | chapter: 6 | part: II. Funksiya va boshqaruv oqimi -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 6. Shart, mantiq va boshqaruv oqimi (Conditionals and Control Flow)

<details>
<summary>Bu bobdagi 13 bo'lim</summary>

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
- [6.11 Jadvalga asoslangan kirish: indeks jadvali va pog'onali jadval](#611-jadvalga-asoslangan-kirish-indeks-jadvali-va-pogonali-jadval)
- [6.12 O'qish tartibi: taqqoslash, shox va oqimni yashiradigan konstruksiyalar](#612-oqish-tartibi-taqqoslash-shox-va-oqimni-yashiradigan-konstruksiyalar)
- [6.13 Amalda qo'llash](#613-amalda-qollash)

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

Ifoda qisqargandan keyin ham bir savol qoladi: operatorlar qaysi tartibda bajariladi. Bu yerda qoida qat'iy - **tilning ustunlik jadvaliga tayanmang, qavs qo'ying**. Qavs o'quvchidan `&&` ning `||` dan yuqori turishini, `<` ning `==` dan oldin bajarilishini yoddan bilishni talab qilmaydi; ikki tilda parallel ishlaydigan odam uchun esa bu yod umuman ishonchsiz. McConnell buni shunday ifodalaydi: qavs qo'yish telegramma yuborish emas, har belgi uchun pul to'lamaysiz (McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 19.1 (437-bet)). Shubha bo'lsa, qavs qo'yiladi.

```java
// yomon: && ning ustunligi || dan yuqori - o'quvchi buni eslab turishi kerak
if (order.isPaid() || order.isPending() && !order.isExpired()) { ... }

// yaxshi: qavs maqsadni ifodaning o'zida aytadi
if (order.isPaid() || (order.isPending() && !order.isExpired())) { ... }
```

Qavslar balansini ko'z bilan tekshirishning oson yo'li ham bor: ifoda bo'ylab chapdan o'ngga yurib, ochuvchi qavsda sanoqni bittaga oshirasiz, yopuvchida bittaga kamaytirasiz; oxirida nol chiqsa, qavslar juft.

Qavs ifodani tushunarli qiladi, lekin uni **qisqartirmaydi**. Uchinchi xato shakl
aynan qisqartirish istagidan tug'iladi: `&&` va `||` ning qisqa tutashuv
(short-circuit) xulqidan foydalanib, tayinlash va shartni bitta ifodaga siqish.
Boswell va Foucher o'z kodlaridan misol keltiradi - `assert((!(bucket =
FindBucket(key))) || !bucket->IsOccupied());` qatori "kalit uchun bucket ni ol;
`null` bo'lmasa, band emasligini tekshir" degani, lekin bir qator bo'lsa ham
ko'pchilik programmistni to'xtatib o'ylantiradi; ikki qatorga yoyilgan shakl
aynan shu ishni qiladi va o'qiladi. Mualliflar sababini ham aytadi: mantiqni
qisqa "nugget" ga siqishda zavq bor, u kichik jumboqni yechishga o'xshaydi,
lekin natija keyin o'qiydigan odam uchun tezlik to'siqi bo'ladi
(Boswell/Foucher, *The Art of Readable Code*, 1-nashr, O'Reilly, 2011, 8-bob
(86-bet)).

```java
// yomon: tayinlash shart ichiga siqilgan
if ((bucket = findBucket(key)) == null || !bucket.isOccupied()) { ... }

// yaxshi: ikki qator, bir ish bir joyda
Bucket bucket = findBucket(key);
if (bucket == null || !bucket.isOccupied()) { ... }
```

Chegara: qisqa tutashuvning o'zi taqiqlanmaydi. `if (bucket != null &&
bucket.isOccupied())` yoki `if (order != null && order.isPaid())` toza shakl,
chunki ikkinchi operand faqat tekshiruv, yon ta'siri yo'q (shu yerda, 86-bet).
Ajratuvchi shart ham shu: `&&` va `||` operandlarida tayinlash, `remove`,
`next()` kabi holatni o'zgartiradigan chaqiruv bo'lmasin. Yon ta'sir bo'lsa,
operandning bajarilishi shartga bog'liq bo'lib qoladi va bu kodni o'qib
bilinmaydi; shu sabab [shartli ifodalarni birlashtirish](37-refaktoring-harakatlari-katalogi-iii-shart.md#372-shartli-ifodalarni-birlashtirish-consolidate-conditional-expression)
refaktoringi ham yon ta'sir bor joyda taqiqlanadi.

**Chalkashgan mantiqda teskari masalani yeching.** Shartni chegara tuzatmalari bilan ketma-ket yamash - `<=` ni `<` ga almashtirish, keyin uchinchi holat qo'shish - murakkablikning aniq belgisi. Boswell va Foucher ning misoli: ikki oraliq kesishishini tekshiradigan `overlapsWith` har ikki uchning qarshi oraliq ichiga tushishini tekshirgan, ikki marta tuzatilgan va har tuzatmadan keyin yangi xato chiqqan; uchinchi urinishda shart uch qismli va o'qilmaydigan bo'lib qolgan.

Yechim - to'xtab **teskari masalani** yechish. "Kesishadi" ning teskarisi "kesishmaydi" va u ikki holatdan iborat: qarshi oraliq biz boshlashimizdan oldin tugaydi, yoki biz tugaganimizdan keyin boshlanadi. Har shartda ikki qiymat qoladi, shuning uchun `<=` to'g'rimi degan savolga diqqat yetadi.

```java
public record DateRange(LocalDate begin, LocalDate end) {   // [begin, end)

    // Yomon: chegara tuzatmalari bilan yamalgan shart
    boolean overlapsWithTangled(DateRange other) {
        return (!begin.isBefore(other.begin) && begin.isBefore(other.end))
                || (end.isAfter(other.begin) && !end.isAfter(other.end))
                || (!begin.isAfter(other.begin) && !end.isBefore(other.end));
    }

    // Yaxshi: teskari masala, har qatorda bitta taqqoslash
    boolean overlapsWith(DateRange other) {
        if (!other.end().isAfter(begin)) return false;   // bizdan oldin tugadi
        if (!other.begin().isBefore(end)) return false;  // bizdan keyin boshlandi
        return true;
    }
}
```

Teskari masalaga o'tishning boshqa shakllari ham bor: massivni teskari tartibda aylanish yoki ma'lumot tuzilmasini oxiridan boshlab to'ldirish. Umumiy signal bitta: shart uchinchi marta tuzatilayotgan bo'lsa, yechim shartni tuzatishda emas, masalani boshqa tomondan qo'yishda.

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

To'rtinchi holat Java ga xos va o'qilishdan emas, semantikadan keladi: ternarning
ikki shoxi har xil numeric turda bo'lsa, ifodaning turi **ko'tariladi**.
Spetsifikatsiya qoidasi: shoxlar bir xil turda bo'lmasa va maxsus holatlarga
(primitiv va uning boxed jufti, `byte`/`short` jufti, `int` konstantasi) tushmasa,
ikki operandga umumiy numeric promotion qo'llanadi va ifoda turi shu ko'tarilgan
tur bo'ladi; promotion esa unboxing ni ham o'z ichiga oladi (*The Java Language
Specification, Java SE 25 Edition*, 15.25.2 (711-712-bet)).

Bundan ikki tuzoq chiqadi. Birinchisi jim tur o'zgarishi: bir shoxi `int`,
ikkinchisi `double` bo'lsa, butun ifoda `double` bo'ladi, shuning uchun `int`
kutgan joyda kasr paydo bo'ladi. Ikkinchisi va qimmatlisi: bir shoxi primitiv
`int`, ikkinchisi `Integer` bo'lsa, qoida bo'yicha ifoda turi `int` bo'ladi,
demak `Integer` unboxing qilinadi - va u `null` bo'lsa chaqiruv
`NullPointerException` bilan yiqiladi, hatto shu shox tanlanmagan bo'lsa ham
tanlanishi mumkin bo'lgani uchun tur shunday hisoblanadi.

```java
// yomon: ifoda turi double bo'lib ketdi
double discount = isMember ? 1 : 0.5;          // 1 emas, 1.0

// yomon: ifoda turi int, shuning uchun bonus unboxing qilinadi
Integer bonus = repository.findBonus(userId);  // null bo'lishi mumkin
int total = base + (isMember ? bonus : 0);     // bonus == null -> NPE

// yaxshi: shoxlar bir turda, null oshkor hal qilingan
int total = base + (isMember ? Objects.requireNonNullElse(bonus, 0) : 0);

// yaxshi: boxed natija kerak bo'lsa, ikki shox ham boxed
Integer applied = isMember ? bonus : Integer.valueOf(0);
```

Qoida: ternarning ikki shoxi bir xil turda bo'lsin. Aralashsa, turni oshkor
yozish yoki `if/else` ga o'tish kerak; boxed qiymat qatnashsa esa `null` ni
ternardan oldin hal qilish kerak. Shu tuzoqning boshqa shakllari
[avtoboxing narxi va `null` unboxing](20-primitiv-son-va-pul.md#206-avtoboxing-narxi-va-null-unboxing)
bo'limida.

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

Uchta-to'rtta shoxli `switch` da `case` lar tartibi ahamiyatsiz, lekin o'nlab hodisa turini qayta ishlaydigan `switch` da tartib o'qilishni belgilaydi. McConnell uchta tartiblash qoidasini beradi va ular bir-biriga alternativa, birga ishlatilmaydi (McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 15.2 (361-bet)):

- **Alifbo yoki raqam bo'yicha.** Shoxlar bir xil ahamiyatga ega bo'lsa shu tartib eng yaxshisi: kerakli `case` ni ro'yxatdan ko'z bilan topish oson. Enum ustidagi `switch` da bu enum e'lon tartibiga ergashish bilan bir xil natija beradi va IDE ning "add remaining cases" harakati ham shuni yozadi.
- **Normal holat birinchi.** Bitta normal va bir nechta istisno shox bo'lsa, normali yuqoriga chiqadi; qolganlari pastda turadi. Qaysi biri normal ekani kodda ko'rinmasa, bir qatorlik izoh buni aytadi.
- **Chastota bo'yicha.** Eng ko'p bajariladigan shox yuqorida: o'quvchi ro'yxatni ko'pincha aynan shu shoxni izlab ochadi.

Tanlangan tartibni buzadigan yangi `case` ni "oxiriga qo'shib qo'yish" vaqt o'tishi bilan tartibni yo'qotadi, shuning uchun tartib qaysi ekani bir marta kelishiladi va code review da tekshiriladi.

Boshqaruv ifodasining **turi** ham tanlov: satr ustida `switch` faqat ma'lumot allaqachon satr shaklida kelganda yoziladi. Satr `switch` i kompilyatorda hash hisobi va `equals` solishtirishlari zanjiriga aylanadi, `enum` yoki `int` ustidagi `switch` esa to'g'ridan-to'g'ri jadval bo'yicha o'tadi. Shuning uchun domen holati satr sifatida tashib yurilgan bo'lsa, `switch` dan oldin uni `enum` ga aylantirish ikki foyda beradi: to'liqlik tekshiruvi qaytadi va noto'g'ri qiymat chegarada ushlanadi.

Eski `switch` ni yangi shaklga ko'chirayotgan diffda yana bitta cheklov esga tushadi: bitta `switch` da `->` shoxi bilan `:` shoxini aralashtirib bo'lmaydi, ikkisidan bittasi tanlanadi. Shuning uchun ko'chirish qisman qilinmaydi: `switch` butunlay yangi shaklga o'tadi yoki butunlay eski shaklda qoladi.

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

Chegara shartining o'zi ham ma'lum shaklda yoziladi: **son o'qi tartibida**, ya'ni kichikdan kattaga chapdan o'ngga. Oraliq ichida ekanini tekshirganda chegaralar ikki tomonda, tekshirilayotgan qiymat o'rtada turadi; oraliqdan tashqarida ekanini tekshirganda esa teskarisi - qiymat ikki chetda, chegaralar o'rtada. Shunda shart matni tekshirilayotgan rasmni takrorlaydi va `<` bilan `<=` ni almashtirib yuborish ko'zga tashlanadi (McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 19.1 (440-bet)).

```java
// yomon: chegaralar bir xil tomonda, rasm ko'rinmaydi
if (page >= MIN_PAGE && page <= MAX_PAGE) { ... }
if (page < MIN_PAGE || page > MAX_PAGE) { ... }

// yaxshi: oraliq ichida - chegaralar chetda, qiymat o'rtada
if (MIN_PAGE <= page && page <= MAX_PAGE) { ... }

// yaxshi: oraliqdan tashqarida - qiymat chetda, chegaralar o'rtada
if (page < MIN_PAGE || MAX_PAGE < page) { ... }
```

Bir tomonli tekshiruvda ham shu mantiq saqlanadi: qiymat kichik bo'lishi kutilsa `while (i < MIN_PAGE)`, katta bo'lishi kutilsa `while (MIN_PAGE < i)`. Qiymatni doim chapga qo'yish odati ikkinchi holatni `while (i > MIN_PAGE)` ga aylantiradi va rasm yo'qoladi.

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

Agar metodlarni faqat ma'lum tartibda chaqirish mumkin bo'lsa va bu tartib kodda ko'rinmasa, bu yashirin vaqt bog'liqligi (hidden temporal coupling; patternlar hujjatida [Sequential Coupling anti-patterni](../patterns/25-anti-patternlar.md#2517-ketma-ket-bogliqlik-sequential-coupling)). Clean code darajasidagi yechimi: tartibni imzoga olib chiqish.

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

Qoidaning chegarasi ham bor va ajratuvchi shart oddiy: **enum kimga tegishli**. Enum sizning kodingizda bo'lsa, xatti-harakat enum ichiga kiradi. Enum sizga tegishli bo'lmasa (kutubxona yoki boshqa modulning enumi), unga metod qo'sholmaysiz, shuning uchun konstantaga xos xatti-harakatni tashqarida, shu enum ustidagi `switch` da yozish o'rinli bo'ladi. Bunday `switch` hid emas: u yagona joyda turadi va enum egasi o'zgarganda kompilyator (to'liqlik tekshiruvi orqali) sizni ogohlantiradi.

## 6.11 Jadvalga asoslangan kirish: indeks jadvali va pog'onali jadval

Oldingi bo'lim shoxlanishni enum yoki polimorfizmga ko'chirdi. Uchinchi yo'l ham bor: shoxlanishni **ma'lumotga** ko'chirish. Shart zanjiri qiymatni toifaga bog'lashdan boshqa ish qilmasa, bu bog'lanish jadvalda saqlanadi, kod esa faqat qidirish qiladi. Kalitni to'g'ridan-to'g'ri jadval indeksiga aylantirish mumkin bo'lmaganda ikki sxema qoladi (McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 18.3-18.4 (425-426-bet)).

**Indeks jadvali.** Birlamchi ma'lumot bilan avval indeksdan kalit topiladi, keyin shu kalit bilan asosiy jadvaldan yozuv olinadi. Kalit maydoni siyrak bo'lganda shu sxema yutadi: to'rt raqamli artikul `0000`-`9999` oralig'ida bo'lsa-yu omborda yuzta mahsulot bo'lsa, o'n ming elementli asosiy jadval o'rniga o'n ming elementli yengil indeks va yuz elementli asosiy jadval tutiladi. Ikkinchi foydasi: bitta jadval ustiga bir nechta indeks qurish mumkin (nom bo'yicha, sana bo'yicha, summa bo'yicha) va indeksni ko'chirish asosiy yozuvni ko'chirishdan arzon. Java da indeks `Map<String, Integer>` yoki `Map<Sku, ProductRow>` bo'ladi, ya'ni til bu sxemani o'zi beradi.

**Pog'onali jadval.** Bu yerda jadval yozuvi bitta nuqta uchun emas, **oraliq** uchun amal qiladi: chegirma darajalari, tarif pog'onalari, baho shkalasi. Oraliqlar notekis bo'lsa yoki chegaralar kasr son bo'lsa, kalitni indeksga aylantiradigan funksiya topilmaydi, shuning uchun har oraliqning cheti jadvalga yoziladi va qiymat tushgan pog'ona qidiriladi. McConnell buni massiv va sikl bilan yozadi; Java da buning tayyor shakli `NavigableMap` va uning `floorEntry` metodi, quyida shu ishlatilgan.

```java
// Chegirma darajalari: chegaralar kodda emas, ma'lumotda
public final class DiscountTable {

    private static final NavigableMap<Long, BigDecimal> RATE_BY_MIN_AMOUNT = new TreeMap<>(Map.of(
            0L, new BigDecimal("0.00"),
            1_000_000L, new BigDecimal("0.03"),
            5_000_000L, new BigDecimal("0.05"),
            20_000_000L, new BigDecimal("0.08")));

    public BigDecimal rateFor(long amount) {
        // floorEntry: kalitlardan amount dan katta bo'lmagan eng kattasi
        return RATE_BY_MIN_AMOUNT.floorEntry(amount).getValue();
    }
}
```

Pog'onali jadvalning uchta tuzog'i bor va ularning hammasi chegarada. Birinchisi: eng yuqori va eng past pog'ona yopilgan bo'lishi kerak, aks holda chetdagi qiymat hech bir oraliqqa tushmaydi (yuqoridagi kodda `0L` pog'onasi shu uchun turadi, bo'lmasa `floorEntry` `null` qaytaradi). Ikkinchisi: `<` va `<=` ni almashtirib yuborish; qidirishni `floorEntry` ga topshirish shu savolni ma'lumot tuzilmasi darajasida bir marta hal qiladi, qo'lda yozilgan siklda esa u har tahrirda qaytadi ([chegaraviy shartlarni inkapsulyatsiya qilish](#67-chegaraviy-shartlarni-inkapsulyatsiya-qilish)). Uchinchisi: jadval uzun bo'lsa ketma-ket qidirish qimmatga tushadi, shuning uchun binar qidirish yoki indeks sxemasiga o'tiladi - `NavigableMap` da bu allaqachon logarifmik. Qidirishning o'zi esa har doim alohida metodda turadi: jadval sxemasi keyin o'zgarsa, chaqiruvchilar o'zgarmaydi.

## 6.12 O'qish tartibi: taqqoslash, shox va oqimni yashiradigan konstruksiyalar

6.1-6.11 shartning **mazmuni** haqida: nomlash, soddalashtirish, jadvalga ko'chirish. Bu bo'lim esa bir xil mantiqning qaysi **tartibda** yozilishi haqida. Mantiq o'zgarmaydi, o'qish tezligi o'zgaradi.

**Taqqoslashda o'zgaruvchan ifoda chapda, barqaror qiymat o'ngda.** `length >= 10` va `10 <= length` bir narsa, lekin birinchisi tez o'qiladi. Qoida: chap tomonga **tekshirilayotgan**, qiymati o'zgarib turadigan ifoda, o'ng tomonga esa unga qarshi solishtirilayotgan, qiymati barqarorroq ifoda yoziladi. Bu tabiiy gap tuzilishiga mos keladi: "yiliga kamida 100 ming ishlasa" deyiladi, "18 yil sizning yoshingizdan kichik yoki tengmi" deyilmaydi. Shuning uchun `while (bytesReceived < bytesExpected)` to'g'ri shakl: `bytesReceived` sikl davomida o'sadi, `bytesExpected` esa barqaror.

Eski "Yoda notation" (`if (NULL == obj)`) `==` ni tasodifan `=` deb yozishdan saqlash uchun ishlatilgan. Java da bu muammo yo'q: `if (obj = null)` kompilyatsiya qilinmaydi, chunki shart `boolean` talab qiladi; `boolean` o'zgaruvchida esa (`if (flag = true)`) kompilyator ogohlantiradi va statik tahlil xato beradi (42.1). Ya'ni teskari tartibni Java da ishlatish uchun sabab qolmagan.

**`if`/`else` shoxlari tartibi tanlanadi.** Uch mezon bor va ular odatda bir yo'nalishni ko'rsatadi:

1. **Avval ijobiy shart**, inkor emas: `if (debug)`, `if (!debug)` emas (6.2).
2. **Avval oddiy shox** - uni yo'ldan chiqarish uchun; shu bilan `if` ham, `else` ham bitta ekranga sig'ishi mumkin bo'ladi.
3. **Avval qiziq yoki xavfli shox.**

Mezonlar to'qnashsa, qaror o'ylab qabul qilinadi, lekin ko'p holatda g'olib aniq. Boswell va Foucher ning misoli: `if (!url.hasQueryParameter("expand_all"))` bilan boshlangan blok o'quvchining diqqatini darhol `expand_all` holatiga qaratadi, chunki inkor "pushti fil haqida o'ylama" kabi ishlaydi - inkorning o'zi e'tibordan chiqadi, nomlangan narsa esa qoladi. Shunda `expand_all` ham qiziq, ham ijobiy shox, demak u oldinga qo'yiladi.

```java
// Yomon: inkor shart oldinda, lekin diqqat ikkinchi shoxda
if (!url.hasQueryParameter("expand_all")) {
    response.render(items);
} else {
    items.forEach(Item::expand);
    response.render(items);
}

// Yaxshi: qiziq va ijobiy shox oldinda
if (url.hasQueryParameter("expand_all")) {
    items.forEach(Item::expand);
}
response.render(items);
```

**Bajarilish yo'lini yashiradigan konstruksiyalar kodning katta ulushiga tarqatilmaydi.** O'quvchi ideal holatda `main` dan boshlab qadamma-qadam kuzatib chiqa olishi kerak. Quyidagi konstruksiyalar bu kuzatishni buzadi va shu sababli nuqtali ishlatiladi:

| Konstruksiya | Nima yashiradi |
|---|---|
| Thread (`ExecutorService`, `@Async`) | kod qachon bajarilishi noaniq |
| Signal va interrupt ishlovchisi, shutdown hook | istalgan paytda bajarilishi mumkin |
| Istisno | bajarilish bir necha chaqiruv orqali yuqoriga ko'tariladi |
| Funksiya ko'rsatkichi va anonim funksiya (lambda, callback) | qaysi kod yurishini kompilyatsiya paytida bilib bo'lmaydi |
| Virtual metod (`object.virtualMethod()`) | noma'lum voris sinfning kodi chaqiriladi |

Bu konstruksiyalarning har biri foydali va ba'zilari kodni o'qiladigan va kamroq takrorlanadigan qiladi: Spring ning o'zi proxy, `@Transactional` va `@EventListener` orqali shu mexanizmlarga tayanadi. Qoida miqdor haqida: kodning juda katta ulushi shu konstruksiyalarga tayanmasligi kerak, aks holda xatoni kuzatish keskin qiyinlashadi. Praktik chegara - **bitta oqimda ikkitadan ko'p yashirin sakrash bo'lmasin**: controller dan `@Async` metodga, u yerdan event listener ga, u yerdan yana lambda callback ga o'tgan oqimni hech kim kuzata olmaydi.

ESLATMA: "bitta oqimda ikkitadan ko'p emas" chegarasi korpus qo'shimchasi; kitob aniq son bermaydi, faqat "katta ulush" deydi.

## 6.13 Amalda qo'llash

- [ ] Uch va undan ko'p operandli shart ifodalarini topib, har birini nomlangan `boolean` yoki domen metodiga chiqaring.
- [ ] `!(...)` shaklidagi inkor ifodalarni De Morgan bilan soddalashtirib, ijobiy shartga aylantiring.
- [ ] `if (x) return true; else return false;` namunalarini grep qilib, `return x;` ga qisqartiring.
- [ ] Enum ustidagi barcha `switch` lardan `default` ni olib tashlab, to'liqlikni kompilyatorga topshiring.
- [ ] Eski `switch` gaplarini `->` ifodasiga o'tkazib, fallthrough xavfini yo'qoting.
- [ ] Ichma-ich ternar operatorlarni topib, domen metodi yoki `switch` ifodasiga aylantiring.
- [ ] `null` tekshiruvi zanjirlari bor joylarni `Optional` yoki manbadagi `null` ni yo'qotish bilan tekislang.
- [ ] Ma'lum tartibda chaqirilishi shart bo'lgan metod guruhlarini topib, tartibni qaytish turlari orqali majburiy qiling.
- [ ] `&&` va `||` aralashgan shartlarni topib, ustunlikni qavs bilan oshkor qiling.
- [ ] Oraliq tekshiruvlarini son o'qi tartibiga keltiring: chegaralar chetda, qiymat o'rtada.
- [ ] Qiymatni toifaga bog'lashdan boshqa ish qilmaydigan shart zanjirlarini jadvalga (`Map`, `NavigableMap`) ko'chiring.

## Manbalar

- Dustin Boswell, Trevor Foucher, *The Art of Readable Code*, 1-nashr, O'Reilly, 2011 (copyright 2012), 7-bob (70-72, 79-80-betlar) - taqqoslashda o'zgaruvchan ifodani chapga va barqaror qiymatni o'ngga qo'yish, `if`/`else` shoxlari tartibining uch mezoni va inkor shartning diqqatni aynan shu holatga qaratishi, bajarilish yo'lini yashiradigan konstruksiyalarni kodning katta ulushiga tarqatmaslik
- Dustin Boswell, Trevor Foucher, *The Art of Readable Code*, 1-nashr, O'Reilly, 2011 (copyright 2012), 8-bob (87-88-betlar) - shartni chegara tuzatmalari bilan ketma-ket yamash murakkablik belgisi ekani va teskari masalani yechish texnikasi (oraliqlar kesishmasligi ikki holatdan iborat)
- Robert C. Martin, *Clean Code*, 3-bob ("Switch Statements") - `switch` ni past darajali sinfga ko'chirish va polimorfizm bilan almashtirish
- Robert C. Martin, *Clean Code*, 17-bob, G23, G28, G29, G33 - `if/else` o'rniga polimorfizm, shartni inkapsulyatsiya qilish, inkor shartdan qochish, chegaraviy shartni inkapsulyatsiya
- Herbert Schildt, *Java The Complete Reference*, 5-bob - boshqaruv gaplari, `switch` va fallthrough semantikasi
- Boyarsky/Selikoff, *OCP Java SE 17 Study Guide*, 3-bob - `switch` ifodasi, pattern matching va to'liqlik talabi
- Steve McConnell, *Code Complete*, 2-nashr, 15.2 (361-bet) - `case` larni tartiblashning uch yo'li: alifbo, normal holat birinchi, chastota
- Steve McConnell, *Code Complete*, 2-nashr, 18.3-18.4 (425-426-bet) - indeks jadvali va pog'onali jadval orqali kirish
- Steve McConnell, *Code Complete*, 2-nashr, 19.1 (437-bet) - ustunlikka tayanmasdan qavs qo'yish
- Steve McConnell, *Code Complete*, 2-nashr, 19.1 (440-bet) - sonli ifodani son o'qi tartibida yozish
- [Java API, `java.util.NavigableMap`](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/NavigableMap.html) - `floorEntry`: berilgan kalitdan katta bo'lmagan eng katta kalit
- Herbert Schildt, *Java The Complete Reference*, 12-nashr, McGraw Hill, 2022, 5-bob (94-bet) - satr ustida `switch` ni faqat ma'lumot allaqachon satr shaklida bo'lganda ishlatish va satr `switch` ining hash bilan `equals` solishtirishlari zanjiriga aylanishi
- Herbert Schildt, *Java The Complete Reference*, 12-nashr, McGraw Hill, 2022, 17-bob (458-bet) - bitta `switch` da `->` shoxi bilan `:` shoxini aralashtirib bo'lmasligi
- Joshua Bloch, *Effective Java* 3rd, Item 34 (167-bet) - enum ustidagi `switch` sizga tegishli bo'lmagan enum ga konstantaga xos xatti-harakat qo'shish uchun o'rinli ekani
- Dustin Boswell, Trevor Foucher, *The Art of Readable Code*, 1-nashr, O'Reilly, 2011 (copyright 2012), 8-bob (86-bet) - qisqa tutashuv mantiqini suiiste'mol qilish, `assert((!(bucket = FindBucket(key))) || !bucket->IsOccupied())` misoli, "aqlli nugget" ogohlantirishi va `if (object && object->method())` toza shakli
- *The Java Language Specification, Java SE 25 Edition* (Gosling, Joy, Steele, Bracha, Buckley, Smith, Bierman), 15.25.2 (711-712-betlar) - numeric ternarning tur qoidalari: primitiv va boxed juft uchun natija primitiv tur bo'lishi, aks holda umumiy numeric promotion va promotion ning unboxing ni o'z ichiga olishi

---

[&larr; 5. Funksiya argumentlari](05-funksiya-argumentlari.md) · [Mundarija](README.md) · [7. Sikl, iteratsiya va to'plam bilan ishlash &rarr;](07-sikl-iteratsiya-va-toplam-bilan-ishlash.md)
