<!-- doc: clean-code | chapter: 37 | part: X. Hid katalogi va refaktoring harakatlari -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 37. Refaktoring harakatlari katalogi III: shart, API va ierarxiya (Refactoring Moves III)

<details>
<summary>Bu bobdagi 19 bo'lim</summary>

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
- [37.17 Takrorlangan shart bo'laklarini birlashtirish (Consolidate Duplicate Conditional Fragments)](#3717-takrorlangan-shart-bolaklarini-birlashtirish-consolidate-duplicate-conditional-fragments)
- [37.18 Nazorat flagini olib tashlash (Remove Control Flag)](#3718-nazorat-flagini-olib-tashlash-remove-control-flag)
- [37.19 Amalda qo'llash](#3719-amalda-qollash)

</details>


Bu bob shartli mantiqni, API shaklini va vorislik ierarxiyasini
o'zgartiradigan harakatlarni qamrab oladi. Ular 6, 17 va 5 boblardagi
qoidalarga olib boradigan mexanik yo'l.

Harakat nomlari ikki nashrda farq qiladi: 1-nashrda (Fowler 1999) `Introduce
Null Object`, 2-nashrda `Introduce Special Case`. Har bo'limda ikki nom ham,
betlari bilan beriladi. Mexanika qadamlari 1-nashr matnidan olingan, chunki
bu korpusda 2-nashrning faqat mundarijasi bor. Qadamlar orasidagi "compile
and test" 1-nashrning asosiy intizomi: u har bir bo'limda takrorlanadi, 38-bob
esa shuning nega shunday ekanini tushuntiradi.

## 37.1 Shartni parchalash (Decompose Conditional)

Kitob: 1-nashr *Decompose Conditional* (192), 2-nashr *Decompose Conditional* (260).

**Qachon**: murakkab `if-then-else` ifodasi bor (6.1). Fowler buni shunday
izohlaydi: kod ham shart tekshiruvida, ham amallarda *nima* bo'layotganini
aytadi, lekin *nega* bo'layotganini yashiradi (1-nashr, 192-bet).

**Mexanika** (1-nashr, 193-bet):

1. Shartni o'z metodiga chiqarish (Extract Method).
2. `then` qismini va `else` qismini o'z metodlariga chiqarish.

Har bir chiqarish alohida bajariladi, har biridan keyin kompilyatsiya va test;
kitobda natija faqat qisqalik uchun bir qadamda ko'rsatiladi. Ichma-ich shart
bo'lsa, Fowler avval 37.3 ni ko'rib chiqadi, u mos kelmasa har bir shartni
parchalaydi.

```java
// Oldin
if (date.before(SUMMER_START) || date.after(SUMMER_END))
    charge = quantity * winterRate + winterServiceCharge;
else
    charge = quantity * summerRate;

// Keyin
if (notSummer(date))
    charge = winterCharge(quantity);
else
    charge = summerCharge(quantity);
```

Kitobdagi izoh: shart qisqa bo'lsa ham chiqarishga arziydi, chunki
`notSummer(date)` o'qiganda niyat ko'rinadi, asl ifodani esa o'qib chiqib
nimani tekshirayotganini aniqlash kerak. Chiqarilgan metod izohday o'qiladi.

## 37.2 Shartli ifodalarni birlashtirish (Consolidate Conditional Expression)

Kitob: 1-nashr *Consolidate Conditional Expression* (194), 2-nashr
*Consolidate Conditional Expression* (263).

**Qachon**: ketma-ket shart tekshiruvlari bor, tekshiruvlar har xil, lekin
natija bir xil (6.3).

**Mexanika** (1-nashr, 194-bet):

1. Shartlarning hech birida yon ta'sir yo'qligini tekshirish. Yon ta'sir bo'lsa,
   bu refaktoringni bajarish mumkin emas.
2. Shartlar zanjirini mantiqiy operator bilan bitta shartga aylantirish.
3. Kompilyatsiya va test.
4. Shartga Extract Method qo'llashni ko'rib chiqish.

Chegara: agar tekshiruvlar haqiqatan mustaqil bo'lsa va ularni bitta tekshiruv
deb o'ylash to'g'ri bo'lmasa, birlashtirmaslik kerak. Kitob buni oshkor aytadi:
birlashtirish sabablari ayni paytda birlashtirmaslik sabablari ham.

```java
// Oldin
double disabilityAmount() {
    if (seniority < 2) return 0;
    if (monthsDisabled > 12) return 0;
    if (isPartTime) return 0;
    // nafaqa summasini hisoblash
}

// Keyin
double disabilityAmount() {
    if (isNotEligibleForDisability()) return 0;
    // nafaqa summasini hisoblash
}
```

Fowler `&&` variantini ham keltiradi va metod faqat shartni tekshirib qiymat
qaytarsa, uni ternar operatorli bitta `return` ga aylantirishni ko'rsatadi
(1-nashr, 196-bet).

## 37.3 Ichma-ich shartni guard clause ga almashtirish

Kitob: 1-nashr *Replace Nested Conditional with Guard Clauses* (201), 2-nashr
*Replace Nested Conditional with Guard Clauses* (266).

**Qachon**: metodning shartli xatti-harakati normal bajarilish yo'lini
ko'rsatmaydi. Erta qaytish [arxitektor hujjatidagi](../architect/README.md)
metod uzunligi va erta qaytish bo'limida ko'rilgan.

**Mexanika** (1-nashr, 202-bet):

1. Har bir tekshiruv uchun guard clause qo'yish. Guard clause yo qaytaradi, yo
   istisno tashlaydi.
2. Har bir tekshiruv guard clause ga aylangandan keyin kompilyatsiya va test.
3. Hamma guard clause bir xil natija bersa, 37.2 ni qo'llash.

Qoida kitobdan (1-nashr, 202-bet): shartli ifoda ikki shaklda keladi.
Birinchisida ikki shox ham normal xatti-harakatning qismi: `if/else`
ishlatiladi. Ikkinchisida bir javob normal, ikkinchisi g'ayrioddiy holat: shart
tekshirilib darhol qaytiladi, bu guard clause. Atama Beck dan olingan. Fowler
"bitta chiqish nuqtasi" qoidasini foydali deb hisoblamaydi: asosiy printsip
ravshanlik, metod bitta chiqish nuqtasi bilan ravshanroq bo'lsa shunday
qilinadi, aks holda qilinmaydi.

```java
// Keyin
double getPayAmount() {
    if (isDead) return deadAmount();
    if (isSeparated) return separatedAmount();
    if (isRetired) return retiredAmount();
    return normalPayAmount();
}
```

Kitobdagi qo'shimcha (1-nashr, 205-bet): guard qaytaradigan qiymat oshkor
yozilsin (`return 0.0;`), vaqtinchalik o'zgaruvchi orqali emas, shunda guard
ishga tushgandagi natija darhol ko'rinadi.

**Ichma-ichlik qo'shimcha tahrirlardan jim yig'iladi.** Guard kerakligini sezish uchun sabab bor: ichma-ichlik bitta katta qadamda emas, bir nechta kichik qadamda paydo bo'ladi. Boswell va Foucher ning kuzatuvi: yangi shartni mavjud blok ichiga qo'yish eng oson yo'l, chunki muallif uchun o'sha payt yangi kod diqqat markazida turadi, va **diff toza ko'rinadi** - bir necha qator qo'shilgan, boshqa hech narsa tegilmagan. Keyin kodga kelgan odam esa butun ichma-ichlikni birdan qabul qilishi kerak bo'ladi va avvalgi kontekst yo'q.

Shuning uchun refaktoring harakatining o'zidan oldin bitta odat turadi: **o'zgartirishdan keyin kodga yangi o'quvchi nigohi bilan, butunligicha qarash**. Faqat diffga qarash bu holatda yetmaydi, chunki muammo qo'shilgan qatorlarda emas, umumiy shaklda. Review da shu signalning ishlashi uchun reviewer o'zgargan metodni to'liq, diff kontekstidan tashqari o'qiydi.

```java
// Tahrirlar jim yig'ildi: har biri alohida toza ko'rinardi
if (userResult == SUCCESS) {
    if (permissionResult != SUCCESS) {      // ikkinchi tahrirda qo'shildi
        reply.writeErrors(permissionResult);
        reply.done();
        return;
    }
    reply.writeErrors("");
} else {
    reply.writeErrors(userResult);
}
reply.done();

// Butunligicha qaragandan keyin: guard, bitta daraja
if (userResult != SUCCESS) {
    reply.writeErrors(userResult);
    reply.done();
    return;
}
if (permissionResult != SUCCESS) {
    reply.writeErrors(permissionResult);
    reply.done();
    return;
}
reply.writeErrors("");
reply.done();
```

## 37.4 Shartni polimorfizmga almashtirish (Replace Conditional with Polymorphism)

Kitob: 1-nashr *Replace Conditional with Polymorphism* (205), 2-nashr
*Replace Conditional with Polymorphism* (272).

**Qachon**: shart obyektning turiga qarab har xil xatti-harakat tanlaydi
(32.7, G23). Eng katta foyda shu shartlar to'plami programmada bir necha joyda
takrorlanganda: yangi tur qo'shilganda hamma shartni topib tuzatish kerak,
polimorfizmda esa yangi voris sinf yoziladi (1-nashr, 206-bet).

**Mexanika** (1-nashr, 206-207-bet):

1. Avval vorislik tuzilishi kerak. U yo'q bo'lsa, uni 37.13 (Replace Type Code
   with Subclasses) yoki Replace Type Code with State/Strategy bilan yaratish.
2. Shart katta metodning bir qismi bo'lsa, Extract Method bilan ajratish.
3. Kerak bo'lsa Move Method bilan shartni ierarxiyaning tepasiga ko'chirish.
4. Bitta voris sinfni tanlab, shart metodini override qiluvchi metod yaratish;
   shartning shu shoxi tanasini ko'chirib moslash.
5. Kompilyatsiya va test. Ko'chirilgan shoxni asl shartdan o'chirish.
   Kompilyatsiya va test.
6. Hamma shox voris sinf metodiga aylanmaguncha takrorlash.
7. Bazaviy sinf metodini abstrakt qilish.

Ikki tuzilish variantining tanlovi kitobda aniq: voris sinflar eng oddiy
variant, shuning uchun imkon bo'lsa shu olinadi. Lekin tur kodi obyekt
yaratilgandan keyin o'zgarsa, yoki sinf boshqa sabab bilan allaqachon voris
olingan bo'lsa, voris sinf ishlamaydi va State/Strategy kerak bo'ladi
(1-nashr, 206-bet).

| Variant | Qachon (1-nashr, 206-bet) |
|---|---|
| Replace Type Code with Subclasses | tur kodi o'zgarmas, sinf hali voris olinmagan |
| Replace Type Code with State/Strategy | tur kodi obyekt yaratilgandan keyin o'zgaradi, yoki sinf boshqa sabab bilan voris olingan |

Java da bu ikki variantning o'rnini enum ichidagi xatti-harakat (6.10) va
`sealed` interfeys plyus pattern matching (25.3) ham bosa oladi; bu korpusning
tavsiyasi, kitobda bu til imkoniyatlari yo'q.

Oraliq qadamda Fowler hali ko'chirilmagan `switch` shoxiga tuzoq qo'yadi:
`throw new RuntimeException("Should be being overridden")`, shunda override
ishlamasa darhol ko'rinadi (1-nashr, 209-bet).

## 37.5 Maxsus holatni kiritish (Introduce Special Case)

Kitob: 1-nashr *Introduce Null Object* (209), 2-nashr *Introduce Special Case*
(289).

**Qachon**: `null` qiymat tekshiruvi kod bo'ylab takrorlanadi (18.6).

**Mexanika** (1-nashr, 211-212-bet):

1. Asl sinfning `null` versiyasi bo'lgan voris sinf yaratish. Ikki sinfda ham
   `isNull` operatsiyasi: asl sinfda `false`, null sinfda `true`.
2. Kompilyatsiya.
3. Asl obyekt o'rniga `null` qaytarishi mumkin bo'lgan hamma joyni topib, null
   obyekt qaytaradigan qilish.
4. O'zgaruvchini `null` bilan taqqoslaydigan hamma joyni `isNull` chaqiruviga
   almashtirish. Buni manbalarni bittadan olib, orasida kompilyatsiya va test
   bilan qilish mumkin; endi `null` ko'rinmasligi kerak bo'lgan joyga bir necha
   assertion qo'yish foydali.
5. Kompilyatsiya va test.
6. Mijoz `null` bo'lmasa bitta amalni, `null` bo'lsa boshqasini bajaradigan
   joylarni topish; shu amalni null sinfda alternativ xatti-harakat bilan
   override qilish; tekshiruvni o'chirib, kompilyatsiya va test.

Nomning o'zgarishi sababi kitobda aytilgan: `null` obyekt kattaroq pattern -
*special case* - ning xususiy holi; `UnknownCustomer` va `NoCustomer` ikkisi
ham `Customer` ning maxsus holatlari, va ularni ajratish mumkin (1-nashr,
216-bet). 2-nashr shu kattaroq nomni oladi.

```java
// Maxsus holat: noma'lum mijoz
final class UnknownCustomer implements Customer {
    public String name() { return "noma'lum"; }
    public BillingPlan billingPlan() { return BillingPlan.basic(); }
    public boolean isUnknown() { return true; }
}
```

Alternativ variant (1-nashr, 216-bet): `isNull` metodi o'rniga bo'sh
interfeys (`interface Null {}`) va `instanceof` tekshiruvi. Fowler odatda
`instanceof` dan qochadi, lekin bu yerda uni maqbul deb hisoblaydi, chunki asl
sinfni o'zgartirish kerak emas - manbasi yo'q sinf uchun ham ishlaydi.

Xavf, kitobdan: null obyekt hamma xabarga javob bergani uchun tizim hech
qachon yiqilmaydi, va shu sababli muammoni sezish yoki topish qiyinlashadi
(Ron Jeffries, 1-nashr, 211-bet). Null obyektlar o'zgarmas, shu sababli ular
Singleton [Gang of Four] sifatida bajariladi.

## 37.6 Assertion kiritish (Introduce Assertion)

Kitob: 1-nashr *Introduce Assertion* (216), 2-nashr *Introduce Assertion* (302).

**Qachon**: kod programma holati haqida biror taxminga tayanadi, taxmin esa
hech qayerda yozilmagan, faqat algoritmni o'qib aniqlanadi yoki izohda aytilgan
(G22).

**Mexanika** (1-nashr, 217-bet): shart rost deb hisoblangan joyni ko'rsangiz,
shuni aytadigan assertion qo'shish. Assertion tizimning ishlashiga ta'sir
qilmasligi kerak, shuning uchun uni qo'shish har doim xatti-harakatni
saqlaydi.

Kitobdagi qoidalar (1-nashr, 217-bet):

- Assertion - har doim rost deb hisoblangan shart. Uning yiqilishi
  programmist xatosini bildiradi, shu sababli u tekshirilmaydigan istisnoga
  olib kelishi kerak.
- Assertion ni tizimning boshqa qismlari ishlatmaydi; u ishlab chiqarish
  kodidan odatda olib tashlanadi, shuning uchun bu assertion ekanini
  belgilash muhim.
- Assertion ikki vazifani bajaradi: muloqot (o'quvchiga kod qanday taxminga
  tayanganini aytadi) va debug (xatoni manbasiga yaqin tutadi). O'zini
  tekshiruvchi kod yozilganda debug foydasi kamayadi, muloqot foydasi qoladi.
- Assertion ni haddan oshirib ishlatmaslik: rost deb o'ylagan hamma narsani
  emas, faqat rost *bo'lishi kerak* bo'lgan narsani tekshirish. Ortiqcha
  assertion takrorlangan mantiqqa va qiyin qo'llab-quvvatlashga olib keladi.
  Kod assertion siz ham ishlayotgan bo'lsa, u yordam bermaydi, chalkashtiradi.

Java da bu korpus assertion ni public chegarada istisno (18.10), ichki kodda
`assert` yoki `Objects.requireNonNull` (19.8-19.9) bilan ifodalashni tavsiya
qiladi; kitob faqat "tekshirilmaydigan istisno" deydi va aniq mexanizmni
belgilamaydi.

## 37.7 So'rovni o'zgartirishdan ajratish (Separate Query from Modifier)

Kitob: 1-nashr *Separate Query from Modifier* (225), 2-nashr *Separate Query
from Modifier* (306).

**Qachon**: metod qiymat qaytaradi va ayni paytda obyekt holatini
o'zgartiradi.

Qoida kitobdan (1-nashr, 225-bet): qiymat qaytaradigan har qanday metodda
ko'rinadigan yon ta'sir bo'lmasligi kerak. Fowler buni Meyer ga havola bilan
beradi (Meyer buni mutlaq qoida deb hisoblaydi) va o'zi ko'p holda shunga amal
qilganini aytadi. "Ko'rinadigan" so'zi muhim: so'rov natijasini maydonda
keshlash obyekt holatini o'zgartiradi, lekin o'zgarish ko'rinmaydi - so'rovlar
ketma-ketligi har doim bir xil natija beradi.

**Mexanika** (1-nashr, 225-226-bet):

1. Asl metod qaytaradigan qiymatni qaytaradigan so'rov metodi yaratish.
2. Asl metodni shu so'rov chaqiruvining natijasini qaytaradigan qilish: asl
   metoddagi har bir `return` endi `return newQuery()` deydi.
3. Kompilyatsiya va test.
4. Har bir chaqiruvda asl metod chaqiruvini so'rov chaqiruviga almashtirish va
   undan oldingi qatorga asl metod chaqiruvini qo'yish. Har bir chaqiruvchini
   o'zgartirgandan keyin kompilyatsiya va test.
5. Asl metodni `void` qilish va `return` ifodalarini olib tashlash.

```java
// Oldin
String foundMiscreant(List<String> people);   // topadi va signal yuboradi

// Keyin
String foundPerson(List<String> people);      // faqat so'rov
void sendAlert(List<String> people);          // faqat amal
```

Ko'p oqimli kod (1-nashr, 228-bet): test-and-set ni bitta amal sifatida
bajarish muhim idioma va bu refaktoringga zid kelmaydi. Fowler Doug Lea bilan
muhokama qilib shunday xulosaga keladi: so'rov va o'zgartirish metodlari
alohida qoladi, lekin uchinchi, ikkisini ham bajaradigan `synchronized` metod
saqlanadi. U ichida alohida so'rov va o'zgartirish metodlarini chaqiradi; agar
ular `synchronized` bo'lmasa, ko'rinishini package yoki private darajasiga
toraytirish mumkin.

## 37.8 Funksiyani parametrlash (Parameterize Function)

Kitob: 1-nashr *Parameterize Method* (228), 2-nashr *Parameterize Function*
(310).

**Qachon**: bir necha metod o'xshash ish qiladi, farq faqat tanadagi
qiymatlarda (shaklli takrorlanish, 32.2).

**Mexanika** (1-nashr, 229-bet):

1. Har bir takrorlanuvchi metod o'rnini bosa oladigan parametrli metod
   yaratish.
2. Kompilyatsiya.
3. Bitta eski metodni yangi metod chaqiruvi bilan almashtirish.
4. Kompilyatsiya va test.
5. Qolgan metodlar uchun takrorlash, har biridan keyin test.

Butun metodni parametrlash imkoni bo'lmasa, avval metodning bir bo'lagini
chiqarib, keyin shu bo'lakni parametrlash kerak.

```java
// Oldin
void tenPercentRaise()  { salary *= 1.1; }
void fivePercentRaise() { salary *= 1.05; }

// Keyin
void raise(double factor) { salary *= (1 + factor); }
```

Kitobdagi ikkinchi, kamroq ko'rinadigan misol: bosqichli tarif hisobi uchta
qattiq yozilgan oraliq bilan yozilgan edi, oraliq chegaralari parametrga
chiqarilib bitta `usageInRange(start, end)` metodiga aylantirildi. Qiyinligi -
bir necha qiymat asosida takrorlanuvchi kodni payqash (1-nashr, 229-230-bet).

## 37.9 Flag argumentini olib tashlash (Remove Flag Argument)

Kitob: 1-nashr *Replace Parameter with Explicit Methods* (230), 2-nashr
*Remove Flag Argument* (314).

**Qachon**: metod sanab o'tilgan parametr qiymatiga qarab boshqa-boshqa kod
bajaradi. [Flag argumenti va uni ikki funksiyaga
bo'lish](05-funksiya-argumentlari.md#53-flag-argumenti-va-uni-ikki-funksiyaga-bolish)
bo'limida ko'rilgan.

**Mexanika** (1-nashr, 231-bet):

1. Parametrning har bir qiymati uchun oshkor metod yaratish.
2. Shartning har bir shoxida mos yangi metodni chaqirish.
3. Har bir shoxni o'zgartirgandan keyin kompilyatsiya va test.
4. Shartli metodning har bir chaqiruvchisini mos yangi metod chaqiruviga
   almashtirish.
5. Kompilyatsiya va test.
6. Hamma chaqiruvchi o'zgargandan keyin shartli metodni o'chirish.

Nega: chaqiruvchi parametrni belgilash bilan nima qilishini allaqachon
tanlagan, demak unga alohida metodlar berib shartdan voz kechish mumkin. Bunda
shart yo'qoladi, kompilyatsiya vaqtidagi tekshiruv paydo bo'ladi va interfeys
ravshanlashadi: `Switch.beOn()` `Switch.setState(true)` dan ancha tushunarli
(1-nashr, 230-bet).

Chegara (1-nashr, 231-bet): parametr qiymatlari tez-tez o'zgaradigan bo'lsa bu
harakatni qo'llamaslik kerak. Agar metod faqat parametrni maydonga yozsa,
oddiy setter yetadi; shartli xatti-harakat kerak bo'lsa 37.4 kerak.

## 37.10 Butun obyektni saqlash (Preserve Whole Object)

Kitob: 1-nashr *Preserve Whole Object* (232), 2-nashr *Preserve Whole Object*
(319).

**Qachon**: chaqiruvchi bitta obyektdan bir necha qiymat olib, ularni
parametr sifatida uzatadi (5.7). Kitobdagi muammo: chaqirilgan obyektga
keyinchalik yangi qiymat kerak bo'lsa, shu metodning hamma chaqiruvini topib
o'zgartirish kerak.

**Mexanika** (1-nashr, 233-234-bet):

1. Ma'lumot keladigan butun obyekt uchun yangi parametr qo'shish.
2. Kompilyatsiya va test.
3. Qaysi parametrlar butun obyektdan olinishi kerakligini aniqlash.
4. Bitta parametrni olib, metod tanasidagi murojaatlarni butun obyekt
   parametrining mos metodi chaqiruviga almashtirish.
5. Parametrni o'chirish. Kompilyatsiya va test.
6. Butun obyektdan olinishi mumkin bo'lgan har bir parametr uchun takrorlash.
7. Chaqiruvchi metoddagi o'chirilgan parametrlarni tayyorlaydigan kodni olib
   tashlash (agar u kod boshqa joyda ishlatilmasa). Kompilyatsiya va test.

Narxi, kitobdan (1-nashr, 233-bet): alohida qiymat uzatilganda chaqirilgan
obyekt faqat qiymatga bog'lanadi, qiymatlar kelgan obyektga bog'lanmaydi.
Butun obyektni uzatish esa shu ikki obyekt orasida bog'liqlik yaratadi. Agar
bu bog'liqlik tuzilishini buzsa, bu harakat qo'llanmaydi. Fowler yana bir
narsani aytadi: chaqirilgan metod boshqa obyektdan ko'p qiymat ishlatayotgani
metod aslida shu obyektda bo'lishi kerakligining signali, shu sababli bu
harakat bilan birga Move Method ni ham ko'rib chiqish kerak. Butun obyekt
hali mavjud bo'lmasa, oldin Introduce Parameter Object kerak.

```java
// Oldin
int low = daysTempRange().getLow();
int high = daysTempRange().getHigh();
withinPlan = plan.withinRange(low, high);

// Keyin
withinPlan = plan.withinRange(daysTempRange());
```

## 37.11 Parametrni so'rovga va so'rovni parametrga almashtirish

Kitob: 1-nashr *Replace Parameter with Method* (235), 2-nashr *Replace
Parameter with Query* (324) va *Replace Query with Parameter* (327).

**Replace Parameter with Query**: obyekt bir metodni chaqirib, natijani
boshqa metodga parametr qilib uzatadi, qabul qiluvchi esa shu metodni o'zi
ham chaqira oladi. Parametr olib tashlanadi va hisob qabul qiluvchi ichiga
ko'chadi.

**Mexanika** (1-nashr, 236-bet):

1. Kerak bo'lsa, parametr hisobini metodga chiqarish.
2. Metod tanasidagi parametr murojaatlarini shu metod chaqiruviga
   almashtirish.
3. Har bir almashtirishdan keyin kompilyatsiya va test.
4. Parametrni Remove Parameter bilan olib tashlash.

Qachon bajarilmaydi (1-nashr, 236-bet): hisob chaqiruvchi metodning
parametriga tayansa (u har chaqiruvda o'zgarishi mumkin), yoki qabul qiluvchida
yuboruvchiga havola bo'lmasa va unga havola berish niyati bo'lmasa.

**Replace Query with Parameter** teskari yo'nalish: funksiya ichida tashqi
holatga murojaat qilish o'rniga shu qiymat parametrga chiqariladi. Bu harakat
2-nashrda paydo bo'lgan (327-bet); 1-nashrda unga mos yozuv yo'q, shu sababli
bu korpusda uning mexanikasi kitob matniga tayanmaydi.

1-nashr ikki yo'nalishni teng qo'ymaydi: u parametrni olib tashlash tomonda
turadi, chunki uzun parametr ro'yxatini tushunish qiyin va "agar metod
parametrda kelgan qiymatni boshqa yo'l bilan ola olsa, olishi kerak"
(1-nashr, 236-bet). 2-nashrdagi teskari harakatni qaysi holatda afzal ko'rish
kerakligi bu korpusda manbaga tayanmagani uchun aytilmaydi.

## 37.12 Algoritmni almashtirish (Substitute Algorithm)

Kitob: 1-nashr *Substitute Algorithm* (113, 6-bob), 2-nashr *Substitute
Algorithm* (195, 7-bob).

**Qachon**: mavjud algoritmdan ravshanroq variant bor. Kitobda ikki tipik
sabab: muammo yaxshiroq tushunilgani, yoki kodingizni takrorlaydigan imkoniyat
beradigan kutubxona ishlatila boshlangani (1-nashr, 114-bet).

**Mexanika** (1-nashr, 114-bet):

1. Yangi algoritmni tayyorlash va kompilyatsiya qilish.
2. Yangi algoritmni mavjud testlarda yurgizish. Natijalar bir xil bo'lsa, ish
   tugadi.
3. Natijalar farq qilsa, eski algoritmni test va debug uchun taqqoslash
   mezoni sifatida ishlatish: har bir test holatini eski va yangi algoritmda
   yurgizib, ikki natijani birga kuzatish. Shu qaysi test holati muammo
   berayotganini va qanday berayotganini ko'rsatadi.

Oldingi shart (1-nashr, 114-bet): bu qadamdan oldin metod imkon qadar
parchalangan bo'lishi kerak. Katta, murakkab algoritmni almashtirish juda
qiyin; uni faqat soddalashtirish orqali bajarsa bo'ladigan ishga aylantirish
mumkin.

Shunga ko'ra bu harakat test qamrovisiz bajarilmaydi: mexanikaning o'zi
natijalarni taqqoslashga tayanadi
([arxitektor hujjatidagi](../architect/README.md) xavfsizlik to'ri va
xatti-harakatni qayd etuvchi test bo'limi xavfsizlik to'ri haqida).

## 37.13 Turni kodlashdan voris sinflarga almashtirish

Kitob: 1-nashr *Replace Type Code with Subclasses* (181, 8-bob), 2-nashr
*Replace Type Code with Subclasses* (362, 12-bob).

**Qachon**: o'zgarmas tur kodi sinf xatti-harakatiga ta'sir qiladi. Belgisi -
tur kodi qiymatini tekshirib har xil kod bajaradigan `switch` yoki
`if-then-else` (1-nashr, 181-bet).

**Mexanika** (1-nashr, 182-bet):

1. Tur kodini self-encapsulate qilish (faqat accessor orqali o'qish). Tur kodi
   konstruktorga uzatilsa, konstruktorni factory metodga almashtirish kerak.
2. Tur kodining har bir qiymati uchun voris sinf yaratish va unda tur kodi
   getteri ni mos qiymat qaytaradigan qilib override qilish. Qiymat
   vaqtincha qattiq yoziladi; bu hamma `switch` almashtirilgunicha turadigan
   vaqtinchalik holat.
3. Har bir tur kodi qiymati voris sinfga aylangandan keyin kompilyatsiya va
   test.
4. Bazaviy sinfdan tur kodi maydonini o'chirish va accessorlarni abstrakt deb
   e'lon qilish.
5. Kompilyatsiya va test.

O'rni kitobda aniq aytilgan (1-nashr, 182-bet): bu asosan 37.4 ni imkonli
qiladigan iskala harakat. Uni qo'llashga signal - shartli ifodalarning
borligi. Shart yo'q bo'lsa, Replace Type Code with Class to'g'riroq va kamroq
muhim harakat. Ikkinchi sabab - faqat ayrim tur kodlariga tegishli
xususiyatlar: refaktoringdan keyin ularni Push Down Method va Push Down Field
bilan o'z joyiga tushirish mumkin.

Qachon ishlamaydi (1-nashr, 181-182-bet): tur kodi obyekt yaratilgandan keyin
o'zgarsa, yoki sinf boshqa sabab bilan allaqachon voris olingan bo'lsa.
Bunda Replace Type Code with State/Strategy ishlatiladi.

## 37.14 Voris sinfni delegatsiyaga almashtirish

Kitob: 1-nashr *Replace Inheritance with Delegation* (287), 2-nashr *Replace
Subclass with Delegate* (381) va *Replace Superclass with Delegate* (399).

**Qachon**: voris sinf bazaviy sinf interfeysining faqat bir qismini
ishlatadi, yoki unga tegishli bo'lmagan ma'lumotni meros qilib olmoqchi emas
(1-nashr, 287-bet). [Delegatsiya bilan vorislikni
almashtirish](17-vorislik-kompozitsiya-va-polimorfizm.md#179-delegatsiya-bilan-vorislikni-almashtirish)
bo'limida ko'rilgan.

**Mexanika** (1-nashr, 288-bet):

1. Voris sinfda bazaviy sinf instansiyasiga havola qiladigan maydon yaratish va
   uni `this` ga tenglashtirish.
2. Voris sinfda aniqlangan har bir metodni shu delegat maydon orqali
   ishlaydigan qilish; har bir metoddan keyin kompilyatsiya va test. `super`
   orqali voris sinfda aniqlangan metodni chaqiradigan metodlarni hozir
   almashtirish mumkin emas - cheksiz rekursiya bo'ladi; ular vorislik
   uzilgandan keyin almashtiriladi.
3. `extends` ni olib tashlash va delegat maydonga yangi obyekt berish.
4. Mijoz ishlatadigan har bir bazaviy sinf metodi uchun oddiy delegatsiya
   metodi qo'shish.
5. Kompilyatsiya va test.

Narxi, kitobdan: qo'shimcha delegatsiya metodlari - yozish zerikarli, lekin
xato qilish uchun juda oddiy (1-nashr, 288-bet).

Kitobdagi klassik misol: `Stack` ni `Vector` dan voris qilish. Fowler Java 1.1
ning o'zi shunday qilganini aytadi. Mijozlar stackdan faqat `push`, `pop`,
`size` va `isEmpty` ni ishlatadi, oxirgi ikkisi `Vector` dan meros bo'lib
kelgan - demak interfeys sinf nima qilayotganini aytmaydi.

**Replace Superclass with Delegate** (2-nashr, 399-bet) shu harakatning
bazaviy sinf tomoni; 1-nashrda ikki tomon bitta yozuv ostida turadi.

**Teskari yo'nalish va uning sharti** (1-nashr, 289-bet): *Replace Delegation
with Inheritance* delegatsiyani qaytib vorislikka aylantiradi, lekin u faqat
bitta shartda haqli - siz delegatning **barcha** metodini ishlatayotgan
bo'lsangiz. Sabab voris sinfning majburiyatida: voris sinf super sinf
interfeysiga to'liq rioya qilishi kerak, shuning uchun delegatning metodlaridan
bir qismi ishlatilmasa, vorislik mijozga ishlatilmaydigan interfeysni ham ochib
beradi va 37.14 ning o'zi yana kerak bo'lib qoladi ([rad etilgan
meros](17-vorislik-kompozitsiya-va-polimorfizm.md#176-rad-etilgan-meros-va-interfeysni-bolish)).
Shart bajarilmasa ikki boshqa yo'l qoladi: mijozni delegatga to'g'ridan-to'g'ri
yuborish, yoki Remove Middle Man (36.4).

Korpus kompozitsiyani vorislikdan ustun qo'yadi (17-bob), bu esa yuqoridagi
qoidani rad qilmaydi, chunki ikkisi boshqa savolga javob beradi. Ustunlik
**standart tanlov** haqida: yangi kod yozilayotganda kompozitsiya olinadi.
Fowler ning sharti esa **mavjud delegatsiyani qaytarish** haqida: delegatsiya
allaqachon bor va uning hamma metodi ishlatiladigan bo'lsa, delegatsiya metodlari
shunchaki shovqin bo'lib qoladi va vorislik soddaroq chiqadi. Ajratuvchi shart
shu ikki holatni bir-biridan ajratadi.

## 37.15 Voris sinfni va ierarxiyani yo'qotish

**Remove Subclass**. Kitob: 1-nashr *Replace Subclass with Fields* (188),
2-nashr *Remove Subclass* (369).

Qachon (1-nashr, 188-bet): voris sinflar faqat o'zgarmas ma'lumot qaytaradigan
metodlarda farq qiladi (constant method, Beck). Bunday metodlar o'zi foydali,
lekin faqat shulardan iborat voris sinf yashashga arzimaydi.

Mexanika (1-nashr, 189-bet): voris sinflarga Replace Constructor with Factory
Method → voris sinfga murojaat qiladigan kodni bazaviy sinfga o'tkazish →
bazaviy sinfda har bir constant metod uchun `final` maydon e'lon qilish →
maydonlarni to'ldiradigan `protected` konstruktor → voris konstruktorlarini
uni chaqiradigan qilish → kompilyatsiya va test → har bir constant metodni
bazaviy sinfda maydon qaytaradigan qilib bajarish va voris sinfdan o'chirish,
har bir o'chirishdan keyin test → hamma metod ketganda konstruktorni factory
metodga Inline Method bilan ko'chirish → voris sinfni o'chirish →
kompilyatsiya va test → qolgan voris sinflar uchun takrorlash.

**Collapse Hierarchy**. Kitob: 1-nashr *Collapse Hierarchy* (279), 2-nashr
*Collapse Hierarchy* (380).

Qachon (1-nashr, 279-bet): bazaviy va voris sinf bir-biridan juda farq
qilmaydi (32.9). Kitob sababini aytadi: ierarxiya bo'ylab metod va maydonlarni
yuqoriga va pastga surgandan keyin qiymat qo'shmaydigan voris sinf qolishi
mumkin.

Mexanika (1-nashr, 279-280-bet): qaysi sinf o'chirilishini tanlash →
o'chiriladigan sinfning hamma xatti-harakati va ma'lumotini ikkinchisiga Pull
Up Field/Pull Up Method yoki Push Down Method/Push Down Field bilan ko'chirish
→ har bir ko'chirishdan keyin kompilyatsiya va test → o'chiriladigan sinfga
murojaatlarni (o'zgaruvchi e'lonlari, parametr turlari, konstruktorlar)
tuzatish → bo'sh sinfni o'chirish → kompilyatsiya va test.

**Tease Apart Inheritance**. Kitob: 1-nashr *Tease Apart Inheritance* (295).

Qachon (1-nashr, 295-bet): bitta ierarxiya bir vaqtda ikki ishni bajaradi.
Aniqlash belgisi arzon va mexanik: ma'lum darajadagi har bir sinfning voris
sinflari bir xil sifatlovchi bilan boshlanadi, ya'ni bir xil prefiks
ierarxiyaning har bir shoxida qaytariladi. Takrorlangan sifatlovchining o'zi
ikkinchi o'qning nomi, shuning uchun tashxis uchun nom prefikslarini sanash
yetarli.

Yechim: ikki ierarxiya yasash va ular orasiga delegatsiya qo'yish - bitta o'q
ierarxiyada qoladi, ikkinchisi alohida ierarxiyaga chiqadi va birinchisi uni
delegat sifatida ishlatadi. Bu kombinatorik portlashning (33.16) ierarxiya
shakli; uni parallel ierarxiyalar hidi (33.6) bilan aralashtirmaslik kerak -
u yerda ikki alohida ierarxiya bir-biriga ergashadi, bu yerda esa bitta
ierarxiya ichida ikki o'q yashiringan.

**Extract Superclass**. Kitob: 1-nashr *Extract Superclass* (272), 2-nashr
*Extract Superclass* (375).

Qachon (1-nashr, 272-bet): ikki sinfda o'xshash xususiyatlar bor. Bu
takrorlangan kodning bir shakli.

Mexanika (1-nashr, 273-274-bet): bo'sh abstrakt bazaviy sinf yaratish va ikki
sinfni undan voris qilish → bittadan Pull Up Field, Pull Up Method va Pull Up
Constructor Body qo'llash, odatda maydonlardan boshlash → har bir ko'tarishdan
keyin kompilyatsiya va test → voris sinflarda qolgan metodlarda umumiy qism
bo'lsa, Extract Method va keyin Pull Up Method; umumiy oqim o'xshash bo'lsa
Form Template Method → mijozlarni ko'rib chiqish: faqat umumiy interfeysni
ishlatsa, e'lon qilingan turni bazaviy sinfga o'zgartirish.

Imzolari har xil, maqsadi bir xil metodlar uchun avval Rename Method; imzosi
bir xil, tanasi har xil bo'lsa, umumiy imzoni bazaviy sinfda abstrakt deb
e'lon qilish; tanasi har xil, ishi bir xil bo'lsa, 37.12 bilan bitta tanani
ikkinchisiga ko'chirib ko'rish (1-nashr, 273-bet).

Vorislikmi yoki delegatsiyami: kitob tanlov mezonini beradi - alternativa
Extract Class, va tanlov aslida vorislik bilan delegatsiya orasida. Ikki sinf
interfeysni ham, xatti-harakatni ham bo'lishsa, vorislik oddiyroq variant.
Noto'g'ri tanlangan bo'lsa, keyinchalik 37.14 bilan tuzatish mumkin (1-nashr,
273-bet). Bu korpusning 17.7 dagi tavsiyasi shu mezonning Java uchun
qattiqroq shakli.

## 37.16 Refaktoring harakatini tanlash jadvali

Hid topilganda qaysi harakatni qo'llash kerakligini tez aniqlash uchun
jadval. Hid nomlari 1-nashr 3-bobidan (63-72-bet), harakat nomlari 2-nashr
mundarijasidan, har bir juftlik 1-nashr matnida aytilgan.

| Hid (1-nashr) | Birinchi harakat | Keyingi | 1-nashr beti |
|---|---|---|---|
| Duplicated Code | Extract Function | Pull Up Method yoki Form Template Method | 63 |
| Long Function | Extract Function | Replace Temp with Query, Decompose Conditional | 64-65 |
| Large Class | Extract Class | Extract Superclass | 65 |
| Long Parameter List | Introduce Parameter Object | Preserve Whole Object, Replace Parameter with Query | 65-66 |
| Divergent Change | Extract Class | - | 66 |
| Shotgun Surgery | Move Function | Move Field, Inline Class | 66 |
| Feature Envy | Move Function | Extract Function | 66 |
| Data Clumps | Extract Class | Introduce Parameter Object, Preserve Whole Object | 67 |
| Primitive Obsession | Replace Primitive with Object | Extract Class, Introduce Parameter Object | 67-68 |
| Repeated Switches | Replace Conditional with Polymorphism | Introduce Special Case | 68 |
| Lazy Element | Collapse Hierarchy | Inline Class | 68 |
| Temporary Field | Extract Class | Introduce Special Case | 69 |
| Message Chains | Hide Delegate | Extract Function, Move Function | 69 |
| Middle Man | Remove Middle Man | Inline Function | 70 |
| Alternative Classes with Different Interfaces | Change Function Declaration | Extract Superclass | 70 |
| Data Class | Remove Setting Method | Move Function, Encapsulate Record | 71 |
| Refused Bequest | Push Down Method | Replace Subclass with Delegate | 71 |
| Comments | Extract Function | Change Function Declaration, Introduce Assertion | 71 |

Kitobda shu jadvalning o'zi orqa muqovada turadi va Fowler uni hid bilan
harakat orasidagi ko'rsatma deb ataydi, qat'iy mezon deb emas: bob boshida u
"refaktoring qachon kechikkanini aniq mezon bilan aytmaymiz" deb oshkor
yozadi (1-nashr, 63-bet).

## 37.17 Takrorlangan shart bo'laklarini birlashtirish (Consolidate Duplicate Conditional Fragments)

Kitob: 1-nashr *Consolidate Duplicate Conditional Fragments* (196). 2-nashrning
"List of Refactorings" ro'yxatida bu yozuv yo'q, shuning uchun bu yerda faqat
1-nashr mexanikasi beriladi.

**Qachon**: shartning barcha shoxlarida bir xil kod bo'lagi bajariladi. Bunda
shart nimani o'zgartirayotgani ko'rinmaydi, chunki o'zgaradigan va o'zgarmaydigan
qism aralashgan.

**Mexanika** (1-nashr, 196-bet):

1. Shartdan qat'i nazar bir xil bajarilgan kodni aniqlash.
2. Umumiy kod boshida bo'lsa, uni shartdan OLDINGA ko'chirish.
3. Umumiy kod oxirida bo'lsa, uni shartdan KEYINGA ko'chirish.
4. Umumiy kod o'rtada bo'lsa, undan oldingi yoki keyingi kod biror narsani
   o'zgartirayotganini tekshirish. O'zgartirsa, umumiy kodni oldinga yoki
   orqaga surib chetiga chiqarish, keyin 2 yoki 3-qadamni qo'llash.
5. Bitta ifodadan ko'p bo'lsa, uni Extract Method bilan metodga chiqarish.

```java
// Oldin: send() ikki shoxda ham bor, shart nimani o'zgartirayotgani ko'rinmaydi
if (isSpecialDeal()) {
    total = price.multiply(new BigDecimal("0.95"));
    notifier.send(order);
} else {
    total = price.multiply(new BigDecimal("0.98"));
    notifier.send(order);
}

// Keyin: shart faqat farqni ushlaydi
if (isSpecialDeal()) {
    total = price.multiply(new BigDecimal("0.95"));
} else {
    total = price.multiply(new BigDecimal("0.98"));
}
notifier.send(order);
```

Fowler alohida aytadigan ikkinchi holat istisnolar bilan: `try` blokida istisno
tashlashi mumkin bo'lgan ifodadan keyingi kod `catch` bloklarida ham
takrorlansa, u `finally` ga ko'chiriladi (shu yerda, 197-bet). Java da bu
shakl eng ko'p resursni bo'shatish va metrikani yozishda uchraydi.

```java
// Oldin: timer.stop() uch joyda takrorlangan
try {
    gateway.settle(batch);
    timer.stop();
} catch (GatewayTimeoutException e) {
    audit.timeout(batch);
    timer.stop();
} catch (GatewayRejectedException e) {
    audit.rejected(batch, e.reason());
    timer.stop();
}

// Keyin: takroriy qism finally ga ko'chdi
try {
    gateway.settle(batch);
} catch (GatewayTimeoutException e) {
    audit.timeout(batch);
} catch (GatewayRejectedException e) {
    audit.rejected(batch, e.reason());
} finally {
    timer.stop();
}
```

Chegara: `finally` ichida `return` yoki istisno bo'lmasligi kerak, aks holda
asl istisno bostiriladi; bu tuzoq [`finally` ichidagi `return` va bostirilgan
istisno](19-istisno-mexanikasi-va-resurslar.md#193-finally-ichidagi-return-va-bostirilgan-istisno)
bo'limida ko'rilgan. Shartning har shoxida bir xil ko'rinadigan, lekin
aslida boshqa obyekt ustida ishlaydigan kod bu refaktoringga kirmaydi:
birlashtirishdan oldin bo'laklar haqiqatan bir xil ekani tekshiriladi.

## 37.18 Nazorat flagini olib tashlash (Remove Control Flag)

Kitob: 1-nashr *Remove Control Flag* (197). 2-nashrning "List of Refactorings"
ro'yxatida bu yozuv ham yo'q.

**Qachon**: bir qator shart tekshiruvi bor va qachon to'xtashni belgilash uchun
`boolean done` kabi o'zgaruvchi ishlatiladi.

Fowler sababni oshkor aytadi: bunday flaglar foydasidan ko'p tashvish keltiradi
va ular strukturali programmalashning "bitta kirish, bitta chiqish nuqtasi"
qoidasidan qolgan. U bitta kirish nuqtasi bilan qo'shiladi (zamonaviy tillar
buni o'zi majburlaydi), lekin bitta chiqish nuqtasi talabi chalkash shartlarga
va shu noqulay flaglarga olib kelishini aytadi; tillarda `break` va `continue`
aynan murakkab shartdan chiqish uchun bor. Flagni yo'qotgandan keyin shartning
haqiqiy maqsadi ko'rinib qoladi (1-nashr, 197-bet).

**Mexanika** (1-nashr, 198-bet). Birinchi variant, `break` yoki `continue`
bilan:

1. Flagning qaysi qiymati mantiqdan chiqarishini aniqlash.
2. Shu chiqish qiymatini tayinlashlarni `break` yoki `continue` bilan
   almashtirish.
3. Har bir almashtirishdan keyin kompilyatsiya va test.

Ikkinchi variant, `break` va `continue` yo'q tillarda ham ishlaydi:

1. Mantiqni metodga chiqarish.
2. Flagning chiqish qiymatini aniqlash.
3. Chiqish qiymatini tayinlashlarni `return` bilan almashtirish.
4. Har bir almashtirishdan keyin kompilyatsiya va test.

Fowler `break` bor tilda ham ikkinchi variantni afzal ko'radi: `return` metodda
boshqa kod bajarilmasligini aniq aytadi, va bunday kodni baribir ajratish kerak
bo'ladi (shu yerda, 198-bet).

```java
// Oldin: found flagi ham to'xtatadi, ham tanani o'raydi
void checkSecurity(List<String> people) {
    boolean found = false;
    for (String person : people) {
        if (!found) {
            if (person.equals("Don")) {
                sendAlert();
                found = true;
            }
            if (person.equals("John")) {
                sendAlert();
                found = true;
            }
        }
    }
}

// Keyin: flag yo'q, to'xtash nuqtasi ko'rinadi
void checkSecurity(List<String> people) {
    for (String person : people) {
        if (person.equals("Don") || person.equals("John")) {
            sendAlert();
            break;
        }
    }
}
```

Alohida qaraladigan holat: flag ayni paytda natija ma'lumotini ham tashiyotgan
bo'lsa (`String found` kabi). Fowler qoidasi: `break` ishlatilsa flag qoladi,
metodga ajratilsa esa qiymat `return` bilan qaytariladi, shuning uchun ajratish
afzal (shu yerda, 197-bet va 199-200-bet). Ajratilgan metod ayni paytda
`sendAlert()` ni ham chaqirsa, keyingi qadam
[so'rovni o'zgartirishdan ajratish](#377-sorovni-ozgartirishdan-ajratish-separate-query-from-modifier)
bo'ladi: Fowler misolni aynan shu refaktoringda davom ettiradi.

```java
// Keyin: flag natija ham bo'lsa, metodga ajratib return qilinadi
void checkSecurity(List<String> people) {
    someLaterCode(findMiscreant(people));
}

Optional<String> findMiscreant(List<String> people) {
    for (String person : people) {
        if (person.equals("Don") || person.equals("John")) {
            return Optional.of(person);
        }
    }
    return Optional.empty();
}
```

Boswell va Foucher xuddi shu qoidaga nomlash tomonidan keladi: ular
programma ma'lumotini saqlamaydigan, faqat bajarilish yo'nalishini boshqaradigan
o'zgaruvchini "nazorat flagi" deb ataydi va "sikl o'rtasidan chiqmaslik kerak"
degan aytilmagan qoida yo'qligini ta'kidlaydi; ichma-ich sikl bo'lib oddiy
`break` yetmasa, yechim siklni yoki tanasini yangi funksiyaga ko'chirish
(Boswell/Foucher, *The Art of Readable Code*, 1-nashr, O'Reilly, 2011, 9-bob
(96-bet)). Qoidaning sikl tomonidagi bayoni
[shartni sikl boshiga chiqarish](07-sikl-iteratsiya-va-toplam-bilan-ishlash.md#711-shartni-sikl-boshiga-chiqarish-dowhile-va-nazorat-flagi)
bo'limida.

## 37.19 Amalda qo'llash

- [ ] Murakkab shartlarni 37.1 va 37.2 bilan soddalashtiring, har bir
      chiqarishdan keyin test yurgizing.
- [ ] Guard clause ni faqat g'ayrioddiy holatlar uchun ishlatib, teng huquqli
      ikki shoxni `if/else` da qoldiring (37.3).
- [ ] Takrorlangan turga qarab shoxlanishda avval vorislik tuzilishini
      yarating (37.13), keyin shartni polimorfizmga o'tkazing (37.4).
- [ ] Tur kodi obyekt yaratilgandan keyin o'zgaradigan joylarda voris sinf
      emas, State/Strategy variantini tanlang.
- [ ] Takrorlangan `null` tekshiruvlarini 37.5 bilan yo'qotib, null obyekt
      xatoni yashirib qo'ymaganini tekshiradigan assertion qoldiring.
- [ ] Ham qiymat qaytaradigan, ham holatni o'zgartiradigan metodlarni ikkiga
      ajratib, ko'p oqimli joyda `synchronized` uchinchi metodni saqlang
      (37.7).
- [ ] Bir xil tuzilishli funksiya guruhlarini 37.8 bilan birlashtiring.
- [ ] Obyektdan maydon ajratib uzatadigan chaqiruvlarni 37.10 bilan
      soddalashtirishdan oldin yangi bog'liqlik tuzilishni buzmaganini
      tekshiring.
- [ ] To'plamlardan voris olgan sinflarni 37.14 bilan tuzating.
- [ ] 37.16 jadvalini jamoa bilan ko'rib chiqib, review izohlarida harakat
      nomini ishlatishni odat qiling.
- [ ] Shartning barcha shoxlarida takrorlangan chaqiruvlarni topib, shartdan
      oldinga yoki keyinga chiqaring; `catch` bloklarida takrorlanganini
      `finally` ga ko'chiring (37.17).
- [ ] Sikl va shartlardagi `done`, `found`, `finished` nomli `boolean`
      o'zgaruvchilarni sanab, `break` yoki ajratish va `return` bilan
      yo'qoting; flag natija ham tashisa, ajratishni tanlang (37.18).

## Manbalar

- Dustin Boswell, Trevor Foucher, *The Art of Readable Code*, 1-nashr, O'Reilly, 2011 (copyright 2012), 7-bob (78-bet) - yangi shartni mavjud blok ichiga qo'yish diffda toza ko'rinsa ham ichma-ichlikni yig'ishi, o'zgartirishdan keyin kodga yangi o'quvchi nigohi bilan butunligicha qarash va kerak bo'lsa erta qaytishga o'tkazish
- Martin Fowler, *Refactoring: Improving the Design of Existing Code*,
  1-nashr, Addison-Wesley, 1999, 9-bob "Simplifying Conditional Expressions"
  (192-219) - 37.1-37.6 dagi mexanika qadamlari, guard clause ning ikki shakl
  mezoni, null obyekt va special case pattern, assertion qoidalari
- Martin Fowler, *Refactoring: Improving the Design of Existing Code*,
  1-nashr, Addison-Wesley, 1999, 10-bob "Making Method Calls Simpler"
  (220-258) - 37.7-37.11 dagi mexanika, buyruq-so'rov ajratilishi qoidasi
  (Meyer ga havola, 225), ko'p oqimli kod uchun uchinchi `synchronized`
  metod (Doug Lea, 228), `Switch.beOn()` misoli (230), butun obyektni
  uzatishning bog'liqlik narxi (233)
- Martin Fowler, *Refactoring: Improving the Design of Existing Code*,
  1-nashr, Addison-Wesley, 1999, 11-bob "Dealing with Generalization"
  (259-292) - 37.15 dagi Extract Superclass va Collapse Hierarchy mexanikasi,
  37.14 dagi `Stack extends Vector` misoli va delegatsiya qadamlari,
  vorislik bilan delegatsiya orasidagi tanlov mezoni (273)
- Martin Fowler, *Refactoring: Improving the Design of Existing Code*,
  1-nashr, Addison-Wesley, 1999, 6-bob (113-114) va 8-bob (181-191) -
  37.12 Substitute Algorithm mexanikasi va oldingi sharti, 37.13 Replace Type
  Code with Subclasses mexanikasi va uning iskala roli, 37.15 dagi Replace
  Subclass with Fields qadamlari
- Martin Fowler, *Refactoring: Improving the Design of Existing Code*,
  1-nashr, Addison-Wesley, 1999, 11-bob (289-bet) - Replace Delegation with
  Inheritance ning sharti: delegatning barcha metodi ishlatilayotgan bo'lishi,
  chunki voris sinf super sinf interfeysiga to'liq rioya qilishi kerak; shart
  bajarilmasa mijozni delegatga yuborish yoki Remove Middle Man
- Martin Fowler, *Refactoring: Improving the Design of Existing Code*,
  1-nashr, Addison-Wesley, 1999, 12-bob (295-bet) - Tease Apart Inheritance:
  bitta ierarxiya ikki ishni bajarayotganining belgisi (ma'lum darajadagi har
  sinfning voris sinflari bir xil sifatlovchi bilan boshlanishi) va yechim
  sifatida ikki ierarxiya hamda ular orasida delegatsiya
- Martin Fowler, *Refactoring: Improving the Design of Existing Code*,
  1-nashr, Addison-Wesley, 1999, 3-bob "Bad Smells in Code" (63-72) -
  37.16 jadvalidagi hid va harakat juftliklari
- Martin Fowler, *Refactoring: Improving the Design of Existing Code*,
  2-nashr, Addison-Wesley, 2019, mundarija va "List of Refactorings" -
  harakatlarning 2-nashrdagi nomi va beti: 10-bob "Simplifying Conditional
  Logic" (259-304), 11-bob "Refactoring APIs" (305-348), 12-bob "Dealing
  with Inheritance" (349-404), Substitute Algorithm (195)
- ESLATMA: 37.4 dagi enum va `sealed` interfeys varianti, 37.6 dagi `assert`
  va `Objects.requireNonNull` taqsimoti, 37.15 oxiridagi 17.7 ga havola shu
  korpusning Java uchun amaliy tavsiyasi, kitobdan olingan emas
- ESLATMA: vorislik bilan delegatsiya o'rtasidagi ziddiyatning ajratuvchi
  sharti ("standart tanlov" va "mavjud delegatsiyani qaytarish" holatlarini
  ajratish) korpus qarori: Fowler shartni delegatning hamma metodi ishlatiladimi
  degan savol bilan beradi, korpus esa kompozitsiyani standart tanlov sifatida
  saqlab, shartni faqat qaytarish holatiga qo'llaydi
- ESLATMA: 37.11 dagi Replace Query with Parameter faqat 2-nashrda bor, shu
  sababli uning mexanikasi bu bobda berilmaydi
- Martin Fowler, *Refactoring: Improving the Design of Existing Code*,
  1-nashr, Addison-Wesley, 1999, 9-bob (196-200) - 37.17 dagi besh qadamli
  mexanika va `try/catch` dan `finally` ga ko'chirish holati; 37.18 dagi ikki
  variant mexanikasi, bitta chiqish nuqtasi qoidasining tanqidi, `return`
  variantining afzalligi va flag natija ma'lumotini ham tashiydigan holat
- Dustin Boswell, Trevor Foucher, *The Art of Readable Code*, 1-nashr,
  O'Reilly, 2011 (copyright 2012), 9-bob (96-bet) - 37.18 ning ikkinchi
  manbasi: nazorat flagi ta'rifi va ichma-ich siklda funksiyaga ko'chirish
  yechimi
- ESLATMA: 37.17 va 37.18 ning 2-nashrdagi nomi va beti yozilmagan, chunki
  2-nashrning "List of Refactorings" ro'yxatida bu ikki yozuv yo'q
- ESLATMA: 37.18 dagi `Optional` bilan qaytaruvchi variant shu korpusning
  Java uchun amaliy shakli; kitob misoli bo'sh satr qaytaradi

---

[&larr; 36. Refaktoring harakatlari katalogi II: ma'lumot va inkapsulyatsiya](36-refaktoring-harakatlari-katalogi-ii-malumot.md) · [Mundarija](README.md) · [38. Refaktoringni xavfsiz bajarish &rarr;](38-refaktoringni-xavfsiz-bajarish.md)
