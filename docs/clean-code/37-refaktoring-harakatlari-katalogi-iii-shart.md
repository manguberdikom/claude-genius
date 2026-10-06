<!-- doc: clean-code | chapter: 37 | part: X. Hid katalogi va refaktoring harakatlari -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 37. Refaktoring harakatlari katalogi III: shart, API va ierarxiya (Refactoring Moves III)

<details>
<summary>Bu bobdagi 17 bo'lim</summary>

- [37.1 Shartni parchalash (Decompose Conditional)](#371-shartni-parchalash-decompose-conditional)
- [37.2 Shartli ifodalarni birlashtirish (Consolidate Conditional Expression)](#372-shartli-ifodalarni-birlashtirish-consolidate-conditional-expression)
- [37.3 Ichma-ich shartni guard clause ga almashtirish](#373-ichma-ich-shartni-guard-clause-ga-almashtirish)
- [37.4 Shartni polimorfizmga almashtirish (Replace Conditional with Polymorphism)](#374-shartni-polimorfizmga-almashtirish-replace-conditional-with-polymorphism)
- [37.5 Maxsus holatni kiritish (Introduce Special Case)](#375-maxsus-holatni-kiritish-introduce-special-case)
- [37.6 Assertion kiritish (Introduce Assertion)](#376-assertion-kiritish-introduce-assertion)
- [37.7 So'rovni o'zgartirishdan ajratish (Separate Query from Modifier)](#377-sorovni-ozgartirishdan-ajratish-separate-query-from-modifier)
- [37.8 Funksiyani parametrlash (Parameterize Function)](#378-funksiyani-parametrlash-parameterize-function)
- [37.9 Flag argumentini olib tashlash (Remove Flag Argument)](#379-flag-argumentini-olib-tashlash-remove-flag-argument)
- [37.10 Butun obyektni saqlash (Preserve Whole Object)](#3710-butun-obyektni-saqlash-preserve-whole-object)
- [37.11 Parametrni so'rovga va so'rovni parametrga almashtirish](#3711-parametrni-sorovga-va-sorovni-parametrga-almashtirish)
- [37.12 Algoritmni almashtirish (Substitute Algorithm)](#3712-algoritmni-almashtirish-substitute-algorithm)
- [37.13 Turni kodlashdan voris sinflarga almashtirish](#3713-turni-kodlashdan-voris-sinflarga-almashtirish)
- [37.14 Voris sinfni delegatsiyaga almashtirish](#3714-voris-sinfni-delegatsiyaga-almashtirish)
- [37.15 Voris sinfni va ierarxiyani yo'qotish](#3715-voris-sinfni-va-ierarxiyani-yoqotish)
- [37.16 Refaktoring harakatini tanlash jadvali](#3716-refaktoring-harakatini-tanlash-jadvali)
- [37.17 Amalda qo'llash](#3717-amalda-qollash)

</details>


Bu bob shartli mantiqni, API shaklini va vorislik ierarxiyasini o'zgartiradigan harakatlarni qamrab oladi. Ular 6, 17 va 5 boblardagi qoidalarga olib boradigan mexanik yo'l.

## 37.1 Shartni parchalash (Decompose Conditional)

**Qachon**: `if` sharti yoki shoxlari murakkab (6.1).

**Mexanika**: shartni Extract Function bilan nomlangan metodga chiqarish → har bir shoxni ham alohida metodga chiqarish → natijada uch qatorli `if/else` qoladi.

```java
// Keyin
if (isSummerPeriod(date)) {
    charge = summerCharge(quantity);
} else {
    charge = winterCharge(quantity);
}
```

## 37.2 Shartli ifodalarni birlashtirish (Consolidate Conditional Expression)

**Qachon**: bir necha shart bir xil natijaga olib boradi (6.3).

**Mexanika**: shartlarni `||` yoki `&&` bilan birlashtirish → birlashgan shartni Extract Function bilan nomlash → test.

```java
// Oldin
if (employee.seniority() < 2) return 0;
if (employee.monthsDisabled() > 12) return 0;
if (employee.isPartTime()) return 0;

// Keyin
if (isNotEligibleForDisability(employee)) return 0;
```

## 37.3 Ichma-ich shartni guard clause ga almashtirish

Erta qaytish [arxitektor hujjatidagi](../architect/README.md) metod uzunligi va erta qaytish bo'limida ko'rilgan; bu yerda mexanikasi: eng tashqi shartni olib, uni teskari aylantirish va darhol qaytarish → qolgan shartlarni ketma-ket shu tarzda chiqarish → har qadamdan keyin test.

Qoida: guard clause **istisnoli** holatlar uchun, `if/else` esa teng huquqli shoxlar uchun. Ikki shox ham normal bo'lsa, guard clause ishlatilmaydi.

## 37.4 Shartni polimorfizmga almashtirish (Replace Conditional with Polymorphism)

**Qachon**: `switch` yoki `if/else` turga qarab shoxlanadi va u takrorlanadi (32.7, G23).

**Mexanika**: ierarxiya yoki enum yaratish → har bir shoxni mos turga ko'chirish → bazaviy metodni abstrakt qilish → `switch` ni polimorf chaqiruv bilan almashtirish.

Java da uch variant bor va ularning tanlovi aniq:

| Variant | Qachon |
|---|---|
| Enum ichida xatti-harakat | variantlar soni barqaror, mantiq kichik (6.10) |
| `sealed` interfeys + pattern matching | variantlar har xil ma'lumotga ega (25.3) |
| Ierarxiya va polimorfizm | variantlar o'z holatiga ega |

## 37.5 Maxsus holatni kiritish (Introduce Special Case)

**Qachon**: bir xil `null` yoki maxsus qiymat tekshiruvi kod bo'ylab takrorlanadi (18.6).

**Mexanika**: maxsus holat uchun sinf yaratish → u standart xatti-harakatni beradi → `null` qaytaradigan joyni maxsus holat obyekti qaytaradigan qilish → tekshiruvlarni bittadan o'chirish.

```java
// Maxsus holat: noma'lum mijoz
final class UnknownCustomer implements Customer {
    public String name() { return "noma'lum"; }
    public BillingPlan billingPlan() { return BillingPlan.basic(); }
    public boolean isUnknown() { return true; }
}
```

## 37.6 Assertion kiritish (Introduce Assertion)

**Qachon**: kod ma'lum taxminga asoslangan, lekin taxmin hech qayerda yozilmagan (G22).

**Mexanika**: taxminni oshkor tekshiruvga aylantirish - public chegarada istisno (18.10), ichki kodda `assert` yoki `Objects.requireNonNull` (19.8-19.9).

Qoida: assertion **hujjat** vazifasini bajaradi va u bajarilmasligi kerak - agar u ishga tushsa, kod xato.

## 37.7 So'rovni o'zgartirishdan ajratish (Separate Query from Modifier)

**Qachon**: metod ham qiymat qaytaradi, ham holatni o'zgartiradi ([patternlar hujjatidagi](../patterns/README.md) buyruq-so'rov ajratilishi printsipi).

**Mexanika**: faqat so'rov qiladigan yangi metod yaratish → asl metodni so'rov metodini chaqiradigan qilish → chaqiruvchilarni ikki chaqiruvga ajratish → asl metoddan qaytish qiymatini olib tashlash.

```java
// Oldin
String alertForMiscreant(List<String> people);   // topadi va signal yuboradi

// Keyin
Optional<String> findMiscreant(List<String> people);   // faqat so'rov
void alertFor(String miscreant);                        // faqat amal
```

## 37.8 Funksiyani parametrlash (Parameterize Function)

**Qachon**: bir necha funksiya bir xil tuzilishga ega, faqat qiymatlar farq qiladi (shaklli takrorlanish, 32.2).

**Mexanika**: eng umumiy funksiyani tanlash → farq qiladigan qiymatni parametrga aylantirish → boshqa funksiyalarni yangi funksiyaga delegatsiya qilish → chaqiruvchilarni ko'chirish → eski funksiyalarni o'chirish.

```java
// Oldin
void tenPercentRaise(Employee e) { e.raiseBy(0.10); }
void fivePercentRaise(Employee e) { e.raiseBy(0.05); }

// Keyin
void raise(Employee employee, BigDecimal factor) { employee.raiseBy(factor); }
```

## 37.9 Flag argumentini olib tashlash (Remove Flag Argument)

[Flag argumenti va uni ikki funksiyaga bo'lish](05-funksiya-argumentlari.md#53-flag-argumenti-va-uni-ikki-funksiyaga-bolish) bo'limida ko'rilgan. Mexanikasi: har bir flag qiymati uchun aniq nomlangan metod yaratish → asl metodni `private` qilish → chaqiruvchilarni yangi metodlarga ko'chirish.

## 37.10 Butun obyektni saqlash (Preserve Whole Object)

**Qachon**: chaqiruvchi obyektdan bir necha qiymat ajratib olib, ularni parametr sifatida uzatadi (5.7).

**Mexanika**: butun obyektni oladigan yangi parametr qo'shish → ichida eski parametrlardan foydalanishni obyekt metodlariga o'tkazish → eski parametrlarni olib tashlash.

## 37.11 Parametrni so'rovga va so'rovni parametrga almashtirish

**Replace Parameter with Query**: parametr qiymatini funksiya o'zi aniqlay oladi (obyekt holatidan) → parametrni olib tashlash va ichida hisoblash. Bog'liqlikni kamaytiradi, lekin funksiyani holatga bog'laydi.

**Replace Query with Parameter**: teskari - funksiya global yoki tashqi holatga murojaat qiladi → shu qiymatni parametrga chiqarish. Funksiyani sof qiladi va test qilishni osonlashtiradi (31.3).

Ikkinchisi ko'pincha afzal, chunki sof funksiya testlanadi va keshlanadi.

## 37.12 Algoritmni almashtirish (Substitute Algorithm)

**Qachon**: mavjud algoritmdan ravshanroq yoki samaraliroq variant bor.

**Mexanika**: mavjud xatti-harakatni to'liq qamrab oladigan testlar yozish → yangi algoritmni yozish → testlarni ishga tushirish → eski kodni o'chirish.

Bu harakatni test qamrovisiz bajarish mumkin emas: u xatti-harakatni saqlashi kerak, lekin ichini to'liq o'zgartiradi ([arxitektor hujjatidagi](../architect/README.md) xavfsizlik to'ri va xatti-harakatni qayd etuvchi test bo'limi xavfsizlik to'ri haqida).

## 37.13 Turni kodlashdan voris sinflarga almashtirish

**Qachon**: tur kodi (`String type`, `int kind`) xatti-harakatni belgilaydi va u bo'yicha shoxlanish bor.

**Mexanika**: tur kodini inkapsulyatsiya qilish → har bir qiymat uchun voris sinf yaratish (yoki enum a'zosi) → shoxli metodlarni Push Down bilan tarqatish → tur kodini o'chirish.

## 37.14 Voris sinfni delegatsiyaga almashtirish

[Delegatsiya bilan vorislikni almashtirish](17-vorislik-kompozitsiya-va-polimorfizm.md#179-delegatsiya-bilan-vorislikni-almashtirish) bo'limida ko'rilgan. Mexanikasi: delegat maydon qo'shish → `extends` ni olib tashlash → kompilyator ko'rsatgan metodlarni delegatsiyaga aylantirish → keraksizlarini o'chirish → test.

**Replace Superclass with Delegate** - xuddi shu harakatning bazaviy sinf tomoni: `extends HashMap` kabi noto'g'ri vorislikni yo'qotadi.

## 37.15 Voris sinfni va ierarxiyani yo'qotish

**Remove Subclass**: voris sinf endi farq qilmaydi (bazaviy sinf bilan bir xil xatti-harakat) → maydonni bazaviy sinfga ko'chirish, voris sinfni o'chirish.

**Collapse Hierarchy**: bazaviy va voris sinf bir-biridan deyarli farq qilmaydi → birlashtirish (32.9).

**Extract Superclass**: ikki sinfda umumiy qism bor → bazaviy sinf ajratish. Eslatma: avval interfeys yoki kompozitsiya variantini ko'rib chiqish kerak (17.7).

## 37.16 Refaktoring harakatini tanlash jadvali

Hid topilganda qaysi harakatni qo'llash kerakligini tez aniqlash uchun jadval.

| Hid | Birinchi harakat | Keyingi |
|---|---|---|
| Uzun funksiya | Extract Function | Replace Temp with Query |
| Sirli nom | Rename | Change Function Declaration |
| Takrorlangan kod | Extract Function | Pull Up Method |
| Uzun parametr ro'yxati | Introduce Parameter Object | Preserve Whole Object |
| Ma'lumot to'dasi | Extract Class | Introduce Parameter Object |
| Primitivlarga berilish | Replace Primitive with Object | Extract Class |
| Takrorlangan `switch` | Replace Conditional with Polymorphism | Move Function |
| Sikllar | Replace Loop with Pipeline | Split Loop |
| Global ma'lumot | Encapsulate Variable | inyeksiya |
| O'zgaradigan ma'lumot | Remove Setting Method | Change Reference to Value |
| Tarqoq o'zgarish | Split Phase | Extract Class |
| Feature envy | Move Function | Extract Function |
| Xabar zanjiri | Hide Delegate | Move Function |
| Vositachi | Remove Middle Man | Inline Function |
| Ma'lumot sinfi | Move Function | Encapsulate Record |
| Rad etilgan meros | Push Down Method | Replace Superclass with Delegate |
| Vaqtinchalik maydon | Extract Class | Introduce Special Case |
| Dangasa element | Inline Function | Collapse Hierarchy |
| Flag argumenti | Remove Flag Argument | Parameterize Function |
| `null` tekshiruvi zanjiri | Introduce Special Case | Encapsulate Variable |

## 37.17 Amalda qo'llash

- [ ] Murakkab shartlarni Decompose Conditional va Consolidate Conditional bilan soddalashtiring.
- [ ] Takrorlangan turga qarab shoxlanishni enum, `sealed` yoki ierarxiyaga o'tkazing (37.4 jadvali).
- [ ] Takrorlangan `null` tekshiruvlarini Introduce Special Case bilan yo'qoting.
- [ ] Ham qiymat qaytaradigan, ham holatni o'zgartiradigan metodlarni ikkiga ajrating.
- [ ] Bir xil tuzilishli funksiya guruhlarini Parameterize Function bilan birlashtiring.
- [ ] Obyektdan maydon ajratib uzatadigan chaqiruvlarni Preserve Whole Object bilan soddalashtiring.
- [ ] To'plamlardan voris olgan sinflarni Replace Superclass with Delegate bilan tuzating.
- [ ] 37.16 jadvalini jamoa bilan ko'rib chiqib, review izohlarida harakat nomini ishlatishni odat qiling.

---

[&larr; 36. Refaktoring harakatlari katalogi II: ma'lumot va inkapsulyatsiya](36-refaktoring-harakatlari-katalogi-ii-malumot.md) · [Mundarija](README.md) · [38. Refaktoringni xavfsiz bajarish &rarr;](38-refaktoringni-xavfsiz-bajarish.md)
