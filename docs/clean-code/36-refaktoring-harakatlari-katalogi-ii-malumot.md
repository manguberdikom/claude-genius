<!-- doc: clean-code | chapter: 36 | part: X. Hid katalogi va refaktoring harakatlari -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: tekshirilmoqda. Da'volar hali manbaga solishtirilmoqda.

# 36. Refaktoring harakatlari katalogi II: ma'lumot va inkapsulyatsiya (Refactoring Moves II)

<details>
<summary>Bu bobdagi 17 bo'lim</summary>

- [36.1 Sinf ajratish (Extract Class)](#361-sinf-ajratish-extract-class)
- [36.2 Sinfni ichkariga kiritish (Inline Class)](#362-sinfni-ichkariga-kiritish-inline-class)
- [36.3 Delegatni yashirish (Hide Delegate)](#363-delegatni-yashirish-hide-delegate)
- [36.4 Vositachini olib tashlash (Remove Middle Man)](#364-vositachini-olib-tashlash-remove-middle-man)
- [36.5 Maydonni ko'chirish (Move Field)](#365-maydonni-kochirish-move-field)
- [36.6 Yozuvni inkapsulyatsiya qilish (Encapsulate Record)](#366-yozuvni-inkapsulyatsiya-qilish-encapsulate-record)
- [36.7 To'plamni inkapsulyatsiya qilish (Encapsulate Collection)](#367-toplamni-inkapsulyatsiya-qilish-encapsulate-collection)
- [36.8 Primitivni obyektga almashtirish (Replace Primitive with Object)](#368-primitivni-obyektga-almashtirish-replace-primitive-with-object)
- [36.9 Vaqtinchalikni so'rovga almashtirish (Replace Temp with Query)](#369-vaqtinchalikni-sorovga-almashtirish-replace-temp-with-query)
- [36.10 Havolani qiymatga almashtirish (Change Reference to Value)](#3610-havolani-qiymatga-almashtirish-change-reference-to-value)
- [36.11 Qiymatni havolaga almashtirish (Change Value to Reference)](#3611-qiymatni-havolaga-almashtirish-change-value-to-reference)
- [36.12 Sozlash metodini olib tashlash (Remove Setting Method)](#3612-sozlash-metodini-olib-tashlash-remove-setting-method)
- [36.13 Konstruktorni fabrika funksiyasiga almashtirish](#3613-konstruktorni-fabrika-funksiyasiga-almashtirish)
- [36.14 Funksiyani buyruqqa va buyruqni funksiyaga almashtirish](#3614-funksiyani-buyruqqa-va-buyruqni-funksiyaga-almashtirish)
- [36.15 Maydon va metodni yuqoriga/pastga ko'chirish](#3615-maydon-va-metodni-yuqorigapastga-kochirish)
- [36.16 Testlash uchun ierarxiyadan foydalanish (Pull Up Feature, Push Down Dependency)](#3616-testlash-uchun-ierarxiyadan-foydalanish-pull-up-feature-push-down-dependency)
- [36.17 Amalda qo'llash](#3617-amalda-qollash)

</details>


Bu bob ma'lumot tuzilishini o'zgartiradigan harakatlarni qamrab oladi: sinf ajratish va birlashtirish, to'plamni inkapsulyatsiya qilish, primitivni obyektga aylantirish, havola va qiymat o'rtasida o'tish. Bu harakatlar 14-16 boblardagi qoidalarga olib boradigan mexanik yo'l.

## 36.1 Sinf ajratish (Extract Class)

**Nom**: ikki nashrda bir xil - 1-nashr Extract Class (122, 7-bob); 2-nashr Extract Class (182, 7-bob).

**Qachon**: sinf bir necha javobgarlikni oladi (tarqoq o'zgarish, 33.1); maydonlarning bir guruhi birga ishlatiladi; vaqtinchalik maydonlar bor (32.10).

**Mexanika (1-nashr, 122-124)**: sinf javobgarliklarini qanday bo'lish kerakligini hal qilish → ajratilgan javobgarlikni ifodalovchi yangi sinf yaratish → eski sinfdan yangisiga havola o'rnatish → ko'chirilishi kerak bo'lgan har bir maydonni Move Field bilan ko'chirish → har ko'chirishdan keyin kompilyatsiya va test → metodlarni Move Method bilan ko'chirish, quyi darajadagi metodlardan (chaqiriladigan, chaqirmaydigan) boshlab yuqoriga qarab → har ko'chirishdan keyin kompilyatsiya va test → ikki sinfning interfeyslarini ko'rib chiqib qisqartirish → yangi sinfni tashqariga ochish kerakmi, ochilsa havola obyekti sifatidami yoki o'zgarmas qiymat obyekti sifatidami - shuni hal qilish.

1-nashr nozikliklari (122): eski sinf javobgarliklari endi nomiga mos kelmasa, eski sinf qayta nomlanadi. Ikki tomonlama havola kerak bo'lishi mumkin, lekin teskari havola faqat haqiqatan kerak bo'lganda qo'yiladi va keyin uni bir tomonlama qilish mumkinmi deb tekshiriladi.

```java
// Oldin: Person ichida telefon ma'lumoti
class Person {
    private String name;
    private String officeAreaCode;
    private String officeNumber;
    String telephoneNumber() { return "(" + officeAreaCode + ") " + officeNumber; }
}

// Keyin: telefon o'z turida, invarianti bilan
record TelephoneNumber(String areaCode, String number) {
    @Override public String toString() { return "(%s) %s".formatted(areaCode, number); }
}

class Person {
    private String name;
    private TelephoneNumber officePhone;
}
```

## 36.2 Sinfni ichkariga kiritish (Inline Class)

**Nom**: ikki nashrda bir xil - 1-nashr Inline Class (125, 7-bob); 2-nashr Inline Class (186, 7-bob).

**Qachon**: sinf endi javobgarligini yo'qotgan (dangasa element, 32.9); yoki ikki sinf noo'rin yaqinlikda (33.3) va ularni birlashtirish aniqroq.

**Mexanika (1-nashr, 125)**: manba sinfning public protokolini yutib oluvchi sinfda e'lon qilish va bu metodlarning hammasini manba sinfga delegatsiya qilish → manba sinfga bo'lgan barcha murojaatlarni yutib oluvchi sinfga o'zgartirish → kompilyatsiya va test → Move Method va Move Field bilan manba sinfdan hech narsa qolmaguncha elementlarni ko'chirish → manba sinfni o'chirish.

1-nashr nozikliklari (125): manba sinf metodlari uchun alohida interfeys mazmunli bo'lsa, inline qilishdan oldin Extract Interface qo'llanadi. Qolib ketgan murojaatlarni kompilyator tutib olishi uchun manba sinfni `private` qilish yoki nomini o'zgartirish foydali.

## 36.3 Delegatni yashirish (Hide Delegate)

**Nom**: ikki nashrda bir xil - 1-nashr Hide Delegate (127, 7-bob); 2-nashr Hide Delegate (189, 7-bob).

**Qachon**: chaqiruvchi ikki darajali zanjir orqali murojaat qiladi (32.11).

**Mexanika (1-nashr, 127-128)**: delegatning har bir metodi uchun serverda oddiy delegatsiya metodi yaratish → mijozni serverni chaqirishga o'tkazish → har bir metodni o'tkazgandan keyin kompilyatsiya va test → agar endi hech bir mijoz delegatga murojaat qilmasa, serverning delegat uchun akssessorini o'chirish → kompilyatsiya va test.

```java
// Oldin: chaqiruvchi ikki turni biladi
Manager manager = person.department().manager();

// Keyin: Person delegatsiya qiladi, Department yashirin
Manager manager = person.manager();

class Person {
    private Department department;
    Manager manager() { return department.manager(); }
}
```

## 36.4 Vositachini olib tashlash (Remove Middle Man)

**Nom**: ikki nashrda bir xil - 1-nashr Remove Middle Man (130, 7-bob); 2-nashr Remove Middle Man (192, 7-bob).

**Qachon**: 36.3 ning teskarisi - delegatsiya metodlari ko'payib ketgan va sinf vositachiga aylangan (32.12).

**Mexanika (1-nashr, 130)**: delegat uchun akssessor yaratish → mijozning delegat metodidan har bir foydalanishi uchun shu metodni serverdan olib tashlash va mijozdagi chaqiruvni delegatning metodiga o'tkazish → har bir metoddan keyin kompilyatsiya va test.

## 36.5 Maydonni ko'chirish (Move Field)

**Nom**: ikki nashrda bir xil - 1-nashr Move Field (119, 7-bob); 2-nashr Move Field (207, 8-bob).

**Qachon**: maydon boshqa sinfda ko'proq ishlatiladi; maydonlar guruhi birga o'zgaradi; bitta maydonni o'zgartirish ikki sinfga tegadi.

**Mexanika (1-nashr, 119-120)**: maydon `public` bo'lsa, oldin Encapsulate Field (35.6) → kompilyatsiya va test → maqsad sinfda maydon va uning getter bilan setter metodlarini yaratish → maqsad sinfni kompilyatsiya qilish → manbadan maqsad obyektga qanday murojaat qilishni aniqlash → manba sinfdagi maydonni o'chirish → maydonga barcha murojaatlarni maqsad obyektning mos metodiga almashtirish: o'qish getter ga, tayinlash setter ga → kompilyatsiya va test.

1-nashr nozikliklari (119): maydonga murojaat qiluvchi metodlarni ham ko'chirish ehtimoli bor yoki murojaat qiluvchi metod ko'p bo'lsa, Self Encapsulate Field foydali bo'ladi. Maqsad obyektga yetish uchun mavjud maydon yoki metod bo'lmasa, manbada vaqtincha yangi maydon yaratish mumkin. Maydon `private` bo'lmasa, barcha voris sinflarda ham murojaat qidiriladi.

## 36.6 Yozuvni inkapsulyatsiya qilish (Encapsulate Record)

**Nom**: 2-nashr - Encapsulate Record (162, 7-bob). 1-nashrda bu nom yo'q; eng yaqin harakat Replace Record with Data Class (175, 8-bob).

**Qachon**: o'zgaradigan ma'lumot tuzilmasi (`Map<String, Object>`, ochiq maydonlar) kod bo'ylab tarqalgan.

**Mexanika (1-nashr, 175)**: yozuvni ifodalovchi sinf yaratish → har bir ma'lumot elementi uchun `private` maydon hamda uning getter va setter metodini berish. 1-nashr natijani ochiq nomlaydi: bu hali xatti-harakati yo'q "soqov" ma'lumot obyekti, va uning haqiqiy foydasi keyingi refaktoringlarda ochiladi.

**Qadamlar (shu korpus amaliyoti, kitobdan iqtibos emas)**: barcha murojaatlarni kirish metodlariga o'tkazish → ichki tuzilmani yashirish → endi turni xavfsiz o'zgartirish.

```java
// Oldin: shartnomasiz map - kalitlar hech qayerda hujjatlanmagan
Map<String, Object> organization = Map.of("name", "Shop", "country", "UZ");

// Keyin: tur shartnomani ushlaydi
record Organization(String name, CountryCode country) { }
```

## 36.7 To'plamni inkapsulyatsiya qilish (Encapsulate Collection)

**Nom**: ikki nashrda bir xil - 1-nashr Encapsulate Collection (168, 8-bob); 2-nashr Encapsulate Collection (170, 7-bob).

**Qachon**: getter ichki to'plamni qaytaradi va tashqi kod uni o'zgartiradi (14.7).

**Mexanika (1-nashr, 168-169)**: to'plam uchun qo'shish va o'chirish metodlarini qo'shish (`addLine`, `removeLine`) → maydonni bo'sh to'plam bilan initsializatsiya qilish → kompilyatsiya → setter chaqiruvchilarini topish va yo setter ni qo'shish bilan o'chirish amallari ustiga qurish, yoki mijozlarni to'g'ridan-to'g'ri shu amallarga o'tkazish → kompilyatsiya va test → getter dan olingan to'plamni o'zgartiradigan barcha joylarni qo'shish va o'chirish metodlariga o'tkazish, har o'zgarishdan keyin kompilyatsiya va test → shundan keyin getter ni o'zgartirilmas ko'rinish qaytaradigan qilish → oxirida getter foydalanuvchilarida egalik sinfiga tegishli kod bormi deb qarash va uni Extract Method bilan Move Method orqali egasiga ko'chirish.

**Tuzatish**: 1-nashr setter ni **o'chirishni** talab qilmaydi. U ikki yo'lni beradi: setter ni qo'shish va o'chirish amallari ustiga qurish, yoki uni Rename Method bilan `initialize` yoxud `replace` ga qayta nomlash. Sababi 1-nashrda aytilgan: setter ikki holatda ishlatiladi - to'plam bo'sh bo'lganda va bo'sh bo'lmagan to'plamni almashtirganda.

Java da o'zgartirilmas ko'rinish `Collections.unmodifiableList` va shunga o'xshash metodlar bilan olinadi; nusxa qaytarish ham shu maqsadga xizmat qiladi.

## 36.8 Primitivni obyektga almashtirish (Replace Primitive with Object)

**Nom**: 1-nashr - Replace Data Value with Object (141, 8-bob); 2-nashr - Replace Primitive with Object (174, 7-bob).

**Qachon**: primitiv qiymat atrofida mantiq paydo bo'ladi - validatsiya, formatlash, solishtirish (patternlar hujjatidagi [primitivlarga berilish anti-patterni](../patterns/25-anti-patternlar.md#2519-primitivlarga-berilish-primitive-obsession); [satr bilan tiplash o'rniga tur](21-satr-matn-va-regex.md#218-satr-bilan-tiplash-orniga-tur)).

**Mexanika (1-nashr, 141)**: qiymat uchun sinf yaratish; unga manba sinfdagi qiymat bilan bir xil turdagi `final` maydon, getter va shu maydonni argument sifatida oladigan konstruktor berish → kompilyatsiya → manba sinfdagi maydon turini yangi sinfga o'zgartirish → manba sinfdagi getter ni yangi sinfning getter ini chaqiradigan qilish → maydon manba sinf konstruktorida tilga olingan bo'lsa, uni yangi sinf konstruktori orqali tayinlash → setter ni yangi sinfning yangi nusxasini yaratadigan qilish → kompilyatsiya va test → kerak bo'lsa yangi obyektga Change Value to Reference (36.11) qo'llash.

Ya'ni 1-nashr yo'lida manba sinfning tashqi shartnomasi birinchi navbatda o'zgarmaydi: getter hamon primitivni qaytaradi va yangi turning getter iga delegatsiya qiladi. Shartnomani yangi turga ko'chirish keyingi, alohida qadam.

```java
// Oldin
private String priority;          // "high", "HIGH", "urgent"? - qoida yo'q

// Keyin: qiymat o'z turida, invarianti bilan
public record Priority(String code, int rank) {
    public Priority {
        if (rank < 0) throw new IllegalArgumentException("rank manfiy: " + rank);
    }

    public boolean isHigherThan(Priority other) { return rank > other.rank; }
}
```

Daraja alohida `rank` maydonida saqlanadi, chunki enum da `ordinal()` ga tayanish a'zolar tartibi o'zgarganda qiymatni jim buzadi (25.11).

## 36.9 Vaqtinchalikni so'rovga almashtirish (Replace Temp with Query)

**Nom**: ikki nashrda bir xil - 1-nashr Replace Temp with Query (97, 6-bob); 2-nashr Replace Temp with Query (178, 7-bob).

**Qachon**: mahalliy o'zgaruvchi ifodani ushlab turadi va shu ifoda boshqa joyda ham kerak.

**Mexanika (1-nashr, 97-98, oddiy holat)**: faqat bir marta tayinlangan vaqtinchalik o'zgaruvchini topish → uni `final` deb e'lon qilish → kompilyatsiya, bu uning bir marta tayinlanganini kafolatlaydi → tayinlashning o'ng tomonini metodga ajratish → kompilyatsiya va test → o'zgaruvchini ifoda bilan almashtirish (Inline Variable, 35.4).

1-nashr nozikliklari (97-98): ajratilgan metod boshida `private` deb belgilanadi, keyin kerak bo'lsa ko'rinish bo'shashtiriladi. Ajratilgan metod yon ta'sirsiz bo'lishi, ya'ni hech bir obyektni o'zgartirmasligi tekshiriladi; yon ta'siri bo'lsa, avval Separate Query from Modifier qo'llanadi. O'zgaruvchi bir martadan ko'p tayinlangan bo'lsa, avval Split Variable (35.19) ko'rib chiqiladi. Vaqtinchalik siklda natija yig'sa, mantiqning bir qismini so'rov metodiga ko'chirish kerak bo'ladi.

1-nashr motivatsiyasi (98) bu harakatni Extract Method dan oldingi muhim qadam deb ataydi: mahalliy o'zgaruvchilar ajratishni qiyinlashtiradi, shuning uchun imkon qadar ko'p o'zgaruvchi so'rovga almashtiriladi.

## 36.10 Havolani qiymatga almashtirish (Change Reference to Value)

**Nom**: ikki nashrda bir xil - 1-nashr Change Reference to Value (148, 8-bob); 2-nashr Change Reference to Value (252, 9-bob).

**Qachon**: havola obyekti kichik, o'zgarmas va uni boshqarish noqulay (15.5). 1-nashr (148) buni aniq aytadi: havola obyektini kimdir boshqarishi kerak, uni har safar nazoratchidan so'rab olinadi va xotira havolalari ham noqulay bo'ladi; qiymat obyektlari esa taqsimlangan va parallel tizimlarda ayniqsa foydali.

**Mexanika (1-nashr, 148)**: nomzod obyekt o'zgarmas ekanini yoki o'zgarmas bo'la olishini tekshirish → `equals` va `hashCode` metodlarini yozish → kompilyatsiya va test → fabrika metodini olib tashlab, konstruktorni `public` qilishni ko'rib chiqish.

**Chegara (1-nashr, 148)**: obyekt hozir o'zgarmas bo'lmasa, u o'zgarmas bo'lguncha Remove Setting Method (36.12) qo'llanadi. Obyekt o'zgarmas bo'la olmasa, bu refaktoring tashlab yuboriladi. Sababi shu yerda aytilgan: qiymat o'zgaradigan bo'lsa, bir obyektni o'zgartirganda shu narsani ifodalovchi barcha boshqa nusxalarni ham yangilash kerak bo'ladi.

```java
// Oldin: ichki obyekt havola bo'yicha, o'zgaradi
order.telephone().setAreaCode("71");

// Keyin: qiymat, almashtirish yangi nusxa bilan
order = order.withTelephone(new TelephoneNumber("71", "2001234"));
```

## 36.11 Qiymatni havolaga almashtirish (Change Value to Reference)

**Nom**: ikki nashrda bir xil - 1-nashr Change Value to Reference (144, 8-bob); 2-nashr Change Value to Reference (256, 9-bob).

**Qachon**: bir xil mantiqiy obyektning teng nusxalari ko'p va ularni bitta obyekt bilan almashtirish kerak. 1-nashr motivatsiyasi (145): oddiy, kichik va o'zgarmas ma'lumotli qiymatdan boshlanadi, keyin unga o'zgaradigan ma'lumot qo'shish va o'zgarish shu obyektga murojaat qiluvchilarning hammasiga yetib borishini ta'minlash kerak bo'ladi - shu nuqtada u havola obyektiga aylantiriladi.

**Mexanika (1-nashr, 145)**: Replace Constructor with Factory Method (36.13) → kompilyatsiya va test → obyektlarga kirishni ta'minlash uchun qaysi obyekt javobgar ekanini hal qilish; bu statik lug'at yoki registry obyekti bo'lishi mumkin → obyektlar oldindan yaratiladimi yoki talab bo'lganda yaratiladimi, shuni hal qilish → fabrika metodini havola obyektini qaytaradigan qilib o'zgartirish → kompilyatsiya va test.

1-nashr nozikliklari (145): bir nechta obyekt kirish nuqtasi bo'lishi mumkin; obyektlar oldindan yaratilsa, ular kerak bo'lishidan avval yuklangani kafolatlanadi va mavjud bo'lmagan obyekt so'ralganda xato qanday ishlashi hal qilinadi; fabrika mavjud obyektni qaytarishini nomida ko'rsatish uchun Rename Method foydali.

**Tuzatish**: bu harakat 36.10 ning teskarisi, lekin "kamdan-kam kerak bo'ladi" degan baho kitobga mos emas. 1-nashr (148) teskarisini aytadi: havola va qiymat o'rtasidagi qaror har doim ravshan emas va bu qaror ko'pincha teskariga o'zgartirilishi kerak bo'ladi.

## 36.12 Sozlash metodini olib tashlash (Remove Setting Method)

**Nom**: ikki nashrda bir xil - 1-nashr Remove Setting Method (242, 10-bob); 2-nashr Remove Setting Method (331, 11-bob).

**Qachon**: maydon yaratilish vaqtida o'rnatilib, keyin hech qachon o'zgarmasligi kerak (16.7). 1-nashr motivatsiyasi (242): setter ning mavjudligining o'zi maydon o'zgarishi mumkin degan ishora beradi; o'zgarmasligi kerak bo'lsa, setter berilmaydi va maydon `final` qilinadi, shunda niyat ravshan bo'ladi va o'zgarish imkoniyatining o'zi yo'qoladi.

**Mexanika (1-nashr, 242-243)**: kompilyatsiya va test → setter faqat konstruktorda yoki konstruktor chaqiradigan metodda chaqirilishini tekshirish → konstruktorni o'zgaruvchilarga to'g'ridan-to'g'ri murojaat qiladigan qilish → kompilyatsiya va test → setter ni o'chirish va maydonni `final` qilish → kompilyatsiya.

**Chegara (1-nashr, 243)**: voris sinf super sinfning `private` maydonlarini o'rnatayotgan bo'lsa, to'g'ridan-to'g'ri murojaatga o'tish bo'lmaydi. Bunda super sinfda shu qiymatlarni o'rnatadigan `protected` metod, eng yaxshisi konstruktor beriladi, va unga setter bilan chalkashtiradigan nom berilmaydi.

## 36.13 Konstruktorni fabrika funksiyasiga almashtirish

**Nom**: 1-nashr - Replace Constructor with Factory Method (246, 10-bob); 2-nashr - Replace Constructor with Factory Function (334, 11-bob).

**Qachon**: yaratish mantiqi oddiy `new` dan ko'proq; nom kerak (2.9); yaratish turi dinamik tanlanadi.

**Mexanika (1-nashr, 246)**: fabrika metodi yaratib, tanasini mavjud konstruktor chaqiruvi qilish → konstruktorga bo'lgan barcha chaqiruvlarni fabrika metodi chaqiruviga almashtirish → har almashtirishdan keyin kompilyatsiya va test → konstruktorni `private` deb e'lon qilish → kompilyatsiya.

**Tuzatish**: tartib muhim. Konstruktor `private` qilinishi chaqiruvchilar ko'chirilgandan **keyin** turadi, oldin emas: aks holda kod oraliq holatda kompilyatsiya bo'lmaydi.

```java
// Keyin: nom maqsadni aytadi, invariant tekshiriladi
public static Money ofMinorUnits(long minorUnits, Currency currency) { ... }
public static Money zero(Currency currency) { ... }
public static Money parse(String text) { ... }
```

## 36.14 Funksiyani buyruqqa va buyruqni funksiyaga almashtirish

**Nom**: 2-nashr - Replace Function with Command (337, 11-bob) va Replace Command with Function (344, 11-bob). 1-nashrda birinchisi boshqa nom bilan bor: Replace Method with Method Object (110, 6-bob). Ikkinchisi, Replace Command with Function, 1-nashrda yo'q - u 2-nashrda yangi.

**Replace Function with Command**: funksiya murakkab, ko'p mahalliy o'zgaruvchi va bosqichga ega → uni obyektga aylantirish, chunki maydonlar mahalliy o'zgaruvchilarni almashtirgandan keyin ichini Extract Function bilan bo'lish oson bo'ladi.

**Mexanika (1-nashr, 110-111, Replace Method with Method Object)**: metod nomi bilan yangi sinf yaratish → yangi sinfga asl metod turgan obyekt (manba obyekt) uchun `final` maydon, hamda metoddagi har bir vaqtinchalik o'zgaruvchi va har bir parametr uchun maydon berish → manba obyekt va har bir parametrni oladigan konstruktor berish → `compute` nomli metod berish → asl metod tanasini `compute` ga ko'chirish; asl obyektning metodlariga chaqiruvlarda manba obyekt maydonidan foydalanish → kompilyatsiya → eski metodni yangi obyektni yaratib `compute` ni chaqiradigan qilib almashtirish. 1-nashr natijani shunday izohlaydi: barcha mahalliy o'zgaruvchilar endi maydon bo'lgani uchun metodni parametr uzatmasdan erkin bo'lish mumkin. Mexanikaning o'zi Kent Beck dan olingan.

**Replace Command with Function**: teskari - buyruq obyekti faqat bitta `execute` metodidan iborat va holat saqlamaydi → oddiy funksiyaga qaytarish (32.9). Bu harakat 2-nashrda yangi, shuning uchun unga mexanika iqtibos qilinmaydi.

## 36.15 Maydon va metodni yuqoriga/pastga ko'chirish

Ierarxiya bilan ishlashning beshta harakati bor. Ikkitasi juft (metod va maydon uchun yuqoriga va pastga), Pull Up Constructor Body esa juftsiz: konstruktor tanasini pastga tushiradigan harakat ikki nashrning hech birida yo'q.

| Harakat | 1-nashr (bet) | 2-nashr (bet) | Qachon |
|---|---|---|---|
| Pull Up Method | 260, 11-bob | 350, 12-bob | bir xil metod bir necha vorisda (qardosh takrorlanish, 32.2) |
| Pull Up Field | 259, 11-bob | 353, 12-bob | bir xil maydon bir necha vorisda |
| Pull Up Constructor Body | 263, 11-bob | 355, 12-bob | konstruktorlar boshida bir xil kod |
| Push Down Method | 266, 11-bob | 359, 12-bob | metod faqat bir vorisga tegishli (rad etilgan meros, 33.5) |
| Push Down Field | 266, 11-bob | 361, 12-bob | maydon faqat bir vorisda ishlatiladi |

**Tuzatish**: beshovining mexanikasi bir xil emas. 1-nashr har biri uchun boshqa qadamlar beradi:

- **Pull Up Field (259)**: nomzod maydonlarning barcha ishlatilishlari bir xil ekanini tekshirish → nomlari boshqa bo'lsa, super sinfda qo'llanadigan nomga keltirish → kompilyatsiya va test → super sinfda yangi maydon yaratish → voris maydonlarini o'chirish → kompilyatsiya va test. Maydonlar `private` bo'lsa, super sinf maydonini voris murojaat qila oladigan darajaga chiqarish kerak bo'ladi; keyin yangi maydonga Self Encapsulate Field qo'llash ko'rib chiqiladi.
- **Pull Up Method (260)**: metodlar aynan bir xil ekanini tekshirish → signaturalari boshqa bo'lsa, super sinfda qo'llanadigan signaturaga keltirish → super sinfda yangi metod yaratib, biror vorisning tanasini ko'chirish va moslashtirish, keyin kompilyatsiya → bitta voris metodini o'chirish → kompilyatsiya va test → faqat super sinf metodi qolguncha o'chirib va test qilib davom etish → metod chaqiruvchilarida talab qilinadigan turni super sinfga o'zgartirish mumkinmi deb qarash. Metod ikki vorisda bor, super sinfda yo'q metodni chaqirsa, super sinfda abstrakt metod e'lon qilinadi; metod voris maydonini ishlatsa, Pull Up Field yoki Self Encapsulate Field va abstrakt getter kerak bo'ladi.
- **Pull Up Constructor Body (263)**: super sinf konstruktorini aniqlash → voris konstruktorlarining boshidagi umumiy kodni super sinf konstruktoriga ko'chirish → super sinf konstruktorini voris konstruktorining birinchi qadami sifatida chaqirish → kompilyatsiya va test. Keyinroq ham umumiy kod bo'lsa, u Extract Method bilan ajratilib Pull Up Method bilan yuqoriga ko'chiriladi.
- **Push Down Method (266)**: metodni barcha voris sinflarda e'lon qilib, tanasini har biriga nusxalash → metodni super sinfdan olib tashlash → kompilyatsiya va test → kerak bo'lmagan har bir vorisdan metodni o'chirish → kompilyatsiya va test. Metod maydonlarga yetishi uchun ularni `protected` qilish yoki super sinfda akssessor ishlatish kerak bo'ladi.
- **Push Down Field (266)**: maydonni barcha voris sinflarda e'lon qilish → maydonni super sinfdan olib tashlash → kompilyatsiya va test → kerak bo'lmagan vorislardan maydonni o'chirish → kompilyatsiya va test.

ESLATMA: yuqoriga ko'chirish vorislikni kuchaytiradi; natijada bazaviy sinf shishsa, kompozitsiyani ko'rib chiqish kerak (17.9) - bu shu korpusning tavsiyasi, kitobdan olingan emas.

## 36.16 Testlash uchun ierarxiyadan foydalanish (Pull Up Feature, Push Down Dependency)

36.15 dagi Pull Up va Push Down harakatlarining maqsadi - takrorlanishni yo'qotish va rad etilgan merosni tozalash. Feathers shu mexanikaning ikkinchi maqsadini beradi: sinfni test harness ichiga olish. Nomlari ham boshqa, shu sababli ularni alohida qidirish kerak bo'ladi.

**Pull Up Feature**

**Qachon** (Feathers, *Working Effectively with Legacy Code*, Prentice Hall PTR, 2004 (copyright 2005), 25-bob, 388-bet): sinfdagi metodlar klasteri bilan ishlash kerak, lekin sinfni instansiyalashga to'sqinlik qiladigan bog'liqliklar shu klasterga aloqasiz, ya'ni kerakli metodlar yomon bog'liqliklarga na to'g'ridan-to'g'ri, na bilvosita murojaat qiladi. Expose Static Method yoki Break Out Method Object ni qayta-qayta qo'llash mumkin, lekin Feathers bu bog'liqlikka eng to'g'ridan-to'g'ri javob emasligini aytadi.

**Mexanika (391-bet, besh qadam)**: ko'tariladigan metodlarni aniqlash → sinf uchun abstrakt super sinf yaratish → metodlarni super sinfga nusxalab kompilyatsiya qilish → kompilyator aytgan har bir yetishmayotgan murojaatni super sinfga ko'chirish, har qadamda imzoni butunligicha saqlab → ikki sinf ham muvaffaqiyatli kompilyatsiya qilgandan keyin abstrakt sinfga voris yaratib, unga testda sozlash uchun kerakli metodlarni qo'shish. Yomon bog'liqliklar eski sinfda qoladi va testga aralashmaydi.

Feathers natijani dizayn jihatidan ideal deb hisoblamaydi va buni oshkor yozadi (391-bet): bitta javobgarlik to'plami faqat testni osonlashtirish uchun ikki sinfga tarqaladi, va sinflar ichidagi aloqa kuchli bo'lmasa bu chalkashlik beradi. To'g'rirog'i - muammoli ishni biladigan alohida obyektga delegatsiya qilish; lekin bu qadam darhol xavfli ko'rinsa yoki boshqa yomon bog'liqliklar bo'lsa, feature ni ko'tarish yaxshi birinchi qadam bo'ladi. Preserve Signatures va Lean on the Compiler bilan birga bajarilsa xavf ancha kichik ([imzoni saqlash](38-refaktoringni-xavfsiz-bajarish.md#3811-imzoni-saqlash-preserve-signatures), [kompilyatorga tayanish](38-refaktoringni-xavfsiz-bajarish.md#3812-kompilyatorga-tayanish-lean-on-the-compiler)).

Super sinf nega abstrakt: Feathers ning sababi o'qiluvchanlik (391-bet) - ilovada har bir konkret sinf ishlatilayotganini bilish qulay, hech qayerda instansiyalanmagan konkret sinf esa "o'lik kod" ko'rinishini beradi.

**Push Down Dependency**

**Qachon** (392-bet): sinfdagi muammoli bog'liqlik bir necha metod chaqiruvi bilan chegaralanmagan, butun sinfga tarqalgan. Bir necha chaqiruv bo'lsa Subclass and Override Method yetardi; tarqalgan bo'lsa yetmaydi va Extract Interface ni bir necha bor qo'llash kerak bo'ladi.

**Mexanika (394-395-bet, olti qadam)**: muammoli sinfni test harness ichida build qilishga urinish → buildda muammo tug'dirayotgan bog'liqliklarni aniqlash → shu bog'liqliklarning aniq muhitini nomida aytadigan yangi voris yaratish → yomon bog'liqlik bor maydon va metodlarni, imzoni butunligicha saqlab, yangi vorisga nusxalash; asl sinfda shu metodlarni `protected abstract` qilish va asl sinfni abstrakt qilish → test uchun ikkinchi voris yaratib, testni shu vorisni instansiyalaydigan qilish → testlarni build qilib, yangi sinf instansiyalanayotganini tekshirish.

Kitobdagi misol C++ da va UI (MFC) dialoglari haqida. Java da shu g'oyaning eng ko'p uchraydigan shakli - metod ichida yaratiladigan yoki statik chaqiriladigan tashqi klient:

```java
// Keyin: sinf abstrakt, muammoli bog'liqlik vorisga tushdi
public abstract class OffMarketTradeValidator {

    protected abstract void notifyDesk(Trade trade);

    public boolean isValid(Trade trade) {
        return inRange(trade.date()) && inHours(trade);
    }
}

// Production vorisi: bog'liqlik faqat shu yerda
public class RestOffMarketTradeValidator extends OffMarketTradeValidator {

    private final RestClient deskClient;

    @Override
    protected void notifyDesk(Trade trade) {
        deskClient.post().uri("/desk/alerts").body(trade).retrieve().toBodilessEntity();
    }
}

// Test vorisi: bog'liqlik yo'q, isValid mantiqi test ostiga tushdi
class TestingOffMarketTradeValidator extends OffMarketTradeValidator {

    @Override
    protected void notifyDesk(Trade trade) {
    }
}
```

Feathers bu yerda ham vorislikni ideal deb atamaydi (395-bet): u sinf mantiqining bir qismini test ostiga olish uchun ishlatiladi. Abstrakt sinfga test qo'yilgandan keyin mantiqni vorisdan yuqoriga ko'tarib, pastda faqat tashqi bog'liqlik qoladigan holatga kelish, keyin esa uni alohida sinfga delegatsiya qilish mumkin bo'ladi; o'sha yangi sinf oxirida yagona bog'liqlik egasi bo'lib qoladi.

ESLATMA: Spring da bu harakatning birinchi alternativasi konstruktor inyeksiyasi va test dublyori - bog'liqlik konstruktor parametri bo'lsa, ierarxiyani umuman o'zgartirish kerak bo'lmaydi. Push Down Dependency ni konstruktorni o'zgartirish imkonsiz bo'lgan holatga qoldiring: chaqiruvchilar juda ko'p yoki obyektni framework yaratadi. Bu tanlov kitobda yo'q, korpusning qo'shimchasi.

## 36.17 Amalda qo'llash

- [ ] Bir necha javobgarlikka ega sinflarni Extract Class bilan bo'lib, har bir ko'chirishdan keyin test ishga tushiring; ko'chirishni quyi darajadagi metodlardan boshlang.
- [ ] Ichki to'plamni qaytaradigan getter larni Encapsulate Collection bilan yoping va setter ni `initialize` yoki `replace` ga qayta nomlang.
- [ ] `Map<String, Object>` tarqalgan joylarni Encapsulate Record bilan turga aylantiring.
- [ ] Atrofida mantiq to'plangan primitivlarni Replace Primitive with Object bilan value object ga o'tkazing; tashqi shartnomani alohida qadamda ko'chiring.
- [ ] Yaratilgandan keyin o'zgarmasligi kerak bo'lgan maydonlarning setter larini olib tashlab, maydonni `final` qiling.
- [ ] Murakkab konstruktorlarni nomlangan statik fabrikalarga o'tkazing, konstruktorni esa chaqiruvchilar ko'chgandan keyin `private` qiling.
- [ ] Ikki darajali chaqiruv zanjirlarini Hide Delegate bilan yopib, hech bir mijoz delegatga muhtoj bo'lmaganda delegat getter ini olib tashlang.
- [ ] Voris sinflardagi takrorlangan metod va maydonlarni Pull Up bilan birlashtiring, keyin bazaviy sinf hajmini tekshiring.
- [ ] Testga to'sqinlik qilayotgan bog'liqlik kerakli metodlar klasteriga aloqasiz bo'lsa, klasterni abstrakt super sinfga ko'tarib (Pull Up Feature) test vorisidan foydalaning; bog'liqlik butun sinfga tarqalgan bo'lsa uni yangi vorisga tushiring (Push Down Dependency).
- [ ] Ikki harakatni ham imzoni butunligicha saqlab va kompilyator xatolari bo'yicha bajaring; test qo'yilgandan keyin delegatsiyaga o'tishni alohida qadam qilib rejalashtiring.

## Manbalar

- Martin Fowler, *Refactoring: Improving the Design of Existing Code*, 1-nashr, Addison-Wesley, 1999, 7-bob (119-130) - Move Field, Extract Class, Inline Class, Hide Delegate va Remove Middle Man mexanikasi hamda nozikliklari
- Martin Fowler, *Refactoring: Improving the Design of Existing Code*, 1-nashr, Addison-Wesley, 1999, 8-bob (141-149, 168-169, 175) - Replace Data Value with Object, Change Value to Reference, Change Reference to Value, Encapsulate Collection va Replace Record with Data Class mexanikasi; havola va qiymat o'rtasidagi qaror ko'pincha teskariga o'zgartiriladi
- Martin Fowler, *Refactoring: Improving the Design of Existing Code*, 1-nashr, Addison-Wesley, 1999, 6-bob (97-98, 110-111) - Replace Temp with Query va Replace Method with Method Object mexanikasi, yon ta'sir tekshiruvi, `compute` metodi
- Martin Fowler, *Refactoring: Improving the Design of Existing Code*, 1-nashr, Addison-Wesley, 1999, 10-bob (242-243, 246) - Remove Setting Method va Replace Constructor with Factory Method mexanikasi, qadamlar tartibi, `protected` super sinf konstruktori chegarasi
- Martin Fowler, *Refactoring: Improving the Design of Existing Code*, 1-nashr, Addison-Wesley, 1999, 11-bob (259-266) - Pull Up Field, Pull Up Method, Pull Up Constructor Body, Push Down Method va Push Down Field ning bir-biridan farq qiladigan mexanikasi
- Martin Fowler, *Refactoring: Improving the Design of Existing Code*, 2-nashr, Addison-Wesley, 2019, "List of Refactorings" va 7, 8, 9, 11, 12-boblar mundarijasi - 2-nashrdagi nomlar va betlar: Encapsulate Record (162), Encapsulate Collection (170), Replace Primitive with Object (174), Replace Temp with Query (178), Extract Class (182), Inline Class (186), Hide Delegate (189), Remove Middle Man (192), Move Field (207), Change Reference to Value (252), Change Value to Reference (256), Remove Setting Method (331), Replace Constructor with Factory Function (334), Replace Function with Command (337), Replace Command with Function (344), Pull Up Method (350), Pull Up Field (353), Pull Up Constructor Body (355), Push Down Method (359), Push Down Field (361)
- Michael Feathers, *Working Effectively with Legacy Code*, Prentice Hall PTR, 2004 (copyright 2005), 25-bob (388-395) - Pull Up Feature: qachon qo'llanadi, besh qadamli mexanikasi, dizayn jihatidan ideal emasligi va super sinfning nega abstrakt bo'lishi; Push Down Dependency: tarqalgan bog'liqlik sharti, mexanikasi va test vorisining shakli
- ESLATMA: 1-nashr betlari shu korpusda ishlatilgan elektron nusxaning raqamlanishi bo'yicha va kitobning o'z mundarijasi bilan mos; qog'oz nashrining bet raqamlari boshqa bo'lishi mumkin
- ESLATMA: 36.16 oxiridagi Spring tanlovi (konstruktor inyeksiyasi va test dublyori birinchi alternativa) va shu bo'limdagi Java misoli korpusning qo'shimchasi; kitobdagi misol C++ da va UI dialoglari haqida
- ESLATMA: 36.6 dagi qadamlar ro'yxatining ikkinchi qismi (murojaatlarni kirish metodlariga o'tkazish, ichki tuzilmani yashirish) va 36.15 oxiridagi kompozitsiya tavsiyasi shu korpusning amaliy tavsiyasi, kitobdan olingan emas. Replace Command with Function (36.14) 2-nashrda yangi va uning matni bizda yo'q, shuning uchun unga mexanika berilmagan

---

[&larr; 35. Refaktoring harakatlari katalogi I: funksiya va o'zgaruvchi](35-refaktoring-harakatlari-katalogi-i-funksiya.md) · [Mundarija](README.md) · [37. Refaktoring harakatlari katalogi III: shart, API va ierarxiya &rarr;](37-refaktoring-harakatlari-katalogi-iii-shart.md)
