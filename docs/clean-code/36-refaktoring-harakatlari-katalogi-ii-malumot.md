<!-- doc: clean-code | chapter: 36 | part: X. Hid katalogi va refaktoring harakatlari -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 36. Refaktoring harakatlari katalogi II: ma'lumot va inkapsulyatsiya (Refactoring Moves II)

<details>
<summary>Bu bobdagi 16 bo'lim</summary>

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
- [36.16 Amalda qo'llash](#3616-amalda-qollash)

</details>


Bu bob ma'lumot tuzilishini o'zgartiradigan harakatlarni qamrab oladi: sinf ajratish va birlashtirish, to'plamni inkapsulyatsiya qilish, primitivni obyektga aylantirish, havola va qiymat o'rtasida o'tish. Bu harakatlar 14-16 boblardagi qoidalarga olib boradigan mexanik yo'l.

## 36.1 Sinf ajratish (Extract Class)

**Qachon**: sinf bir necha javobgarlikni oladi (tarqoq o'zgarish, 33.1); maydonlarning bir guruhi birga ishlatiladi; vaqtinchalik maydonlar bor (32.10).

**Mexanika**: yangi sinf yaratish → bog'liqlikni asl sinfdan yangisiga o'rnatish → maydonlarni bittadan Move Field bilan ko'chirish → har bir ko'chirishdan keyin test → metodlarni Move Function bilan ko'chirish → interfeysni ko'rib chiqib keraksizni yopish.

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

**Qachon**: sinf endi javobgarligini yo'qotgan (dangasa element, 32.9); yoki ikki sinf noo'rin yaqinlikda (33.3) va ularni birlashtirish aniqroq.

**Mexanika**: maqsad sinfda manba sinfning public metodlariga mos delegatsiya metodlari yaratish → chaqiruvchilarni maqsad sinfga o'tkazish → maydon va metodlarni ko'chirish → manba sinfni o'chirish.

## 36.3 Delegatni yashirish (Hide Delegate)

**Qachon**: chaqiruvchi ikki darajali zanjir orqali murojaat qiladi (32.11).

**Mexanika**: serverga delegatsiya metodi qo'shish → chaqiruvchilarni shu metodga o'tkazish → delegatga kirishni (getter) olib tashlash.

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

**Qachon**: 36.3 ning teskarisi - delegatsiya metodlari ko'payib ketgan va sinf vositachiga aylangan (32.12).

**Mexanika**: delegatga kirish metodi (getter) qo'shish → chaqiruvchilarni delegatga to'g'ridan-to'g'ri murojaatga o'tkazish → keraksiz delegatsiya metodlarini o'chirish.

## 36.5 Maydonni ko'chirish (Move Field)

**Qachon**: maydon boshqa sinfda ko'proq ishlatiladi; maydonlar guruhi birga o'zgaradi; bitta maydonni o'zgartirish ikki sinfga tegadi.

**Mexanika**: maydonni inkapsulyatsiya qilish (35.6) → maqsad sinfda maydon va kirish metodlarini yaratish → asl sinfni maqsad sinfga delegatsiya qilish → chaqiruvchilarni ko'chirish → asl maydonni o'chirish.

## 36.6 Yozuvni inkapsulyatsiya qilish (Encapsulate Record)

**Qachon**: o'zgaradigan ma'lumot tuzilmasi (`Map<String, Object>`, ochiq maydonlar) kod bo'ylab tarqalgan.

**Mexanika**: ma'lumotni ushlaydigan sinf yaratish → kirish metodlari qo'shish → barcha murojaatlarni metodlarga o'tkazish → ichki tuzilmani yashirish → endi turni o'zgartirish xavfsiz.

```java
// Oldin: shartnomasiz map - kalitlar hech qayerda hujjatlanmagan
Map<String, Object> organization = Map.of("name", "Shop", "country", "UZ");

// Keyin: tur shartnomani ushlaydi
record Organization(String name, CountryCode country) { }
```

## 36.7 To'plamni inkapsulyatsiya qilish (Encapsulate Collection)

**Qachon**: getter ichki to'plamni qaytaradi va tashqi kod uni o'zgartiradi (14.7).

**Mexanika**: to'plamga element qo'shish va o'chirish uchun metodlar qo'shish (`addLine`, `removeLine`) → getter ni o'zgartirilmas nusxa yoki ko'rinish qaytaradigan qilish → setter ni o'chirish → to'g'ridan-to'g'ri o'zgartirgan chaqiruvchilarni yangi metodlarga ko'chirish.

## 36.8 Primitivni obyektga almashtirish (Replace Primitive with Object)

**Qachon**: primitiv qiymat atrofida mantiq paydo bo'ladi - validatsiya, formatlash, solishtirish ([patternlar hujjatidagi](../patterns/README.md) primitivlarga berilish anti-patterni ; 21.8).

**Mexanika**: yangi `record` yaratish → maydon turini almashtirish → getter ni yangi tur qaytaradigan qilish → chaqiruvchilarni bosqichma-bosqich ko'chirish → mantiqni yangi turga ko'chirish.

```java
// Oldin
private String priority;          // "high", "HIGH", "urgent"? - qoida yo'q

// Keyin
private Priority priority;        // enum yoki record, invariant bilan

public enum Priority {
    LOW, NORMAL, HIGH, URGENT;

    public boolean isHigherThan(Priority other) { return ordinal() > other.ordinal(); }
}
```

## 36.9 Vaqtinchalikni so'rovga almashtirish (Replace Temp with Query)

**Qachon**: mahalliy o'zgaruvchi ifodani ushlab turadi va shu ifoda boshqa joyda ham kerak.

**Mexanika**: o'zgaruvchi `final` va bir marta tayinlanganini tekshirish → o'ng tomonni metodga chiqarish → o'zgaruvchi ishlatilishlarini metod chaqiruvi bilan almashtirish → o'zgaruvchini o'chirish.

Bu harakat Extract Function dan oldin bajariladi va uni osonlashtiradi: parametrlar soni kamayadi.

## 36.10 Havolani qiymatga almashtirish (Change Reference to Value)

**Qachon**: ichki obyekt o'zgarmas bo'lishi mumkin va u o'zi mustaqil identifikatorga ega bo'lishi shart emas (15.5).

**Mexanika**: ichki obyektni o'zgarmas qilish (barcha setter larni yo'qotish) → `equals` va `hashCode` ni qiymat bo'yicha yozish (yoki `record` ga aylantirish) → ichki obyektni almashtirishni yangi nusxa yaratishga o'tkazish.

```java
// Oldin: ichki obyekt havola bo'yicha, o'zgaradi
order.telephone().setAreaCode("71");

// Keyin: qiymat, almashtirish yangi nusxa bilan
order = order.withTelephone(new TelephoneNumber("71", "2001234"));
```

## 36.11 Qiymatni havolaga almashtirish (Change Value to Reference)

**Qachon**: bir xil mantiqiy obyektning nusxalari ko'p va ularni bir vaqtda o'zgartirish kerak (mijoz ma'lumoti har bir buyurtmada nusxalangan).

**Mexanika**: obyektlar uchun repository yoki registry yaratish → yaratish joyini repository ga o'tkazish → nusxa o'rniga havola saqlash.

Bu harakat 36.10 ning teskarisi va u kamdan-kam kerak bo'ladi: nusxani havolaga aylantirish bog'liqlik qo'shadi.

## 36.12 Sozlash metodini olib tashlash (Remove Setting Method)

**Qachon**: maydon yaratilgandan keyin o'zgarmasligi kerak (16.7).

**Mexanika**: maydonni konstruktor parametriga aylantirish → barcha setter chaqiruvchilarini konstruktorga o'tkazish → setter ni o'chirish → maydonni `final` qilish.

## 36.13 Konstruktorni fabrika funksiyasiga almashtirish

**Qachon**: yaratish mantiqi oddiy `new` dan ko'proq; nom kerak (2.9); yaratish turi dinamik tanlanadi.

**Mexanika**: statik fabrika metodi yaratish → konstruktorni chaqirish → konstruktorni `private` qilish → chaqiruvchilarni fabrikaga o'tkazish.

```java
// Keyin: nom maqsadni aytadi, invariant tekshiriladi
public static Money ofMinorUnits(long minorUnits, Currency currency) { ... }
public static Money zero(Currency currency) { ... }
public static Money parse(String text) { ... }
```

## 36.14 Funksiyani buyruqqa va buyruqni funksiyaga almashtirish

**Replace Function with Command**: funksiya murakkab, ko'p mahalliy o'zgaruvchi va bosqichga ega → uni obyektga aylantirish (maydonlar mahalliy o'zgaruvchilarni almashtiradi), keyin ichini Extract Function bilan bo'lish oson bo'ladi.

**Replace Command with Function**: teskari - buyruq obyekti faqat bitta `execute` metodidan iborat va holat saqlamaydi → oddiy funksiyaga qaytarish (32.9).

## 36.15 Maydon va metodni yuqoriga/pastga ko'chirish

Ierarxiya bilan ishlashning to'rt juft harakati bor va ularning hammasi bir xil mexanikaga ega: tekshirish, ko'chirish, test.

| Harakat | Qachon |
|---|---|
| Pull Up Method | bir xil metod bir necha vorisda (qardosh takrorlanish, 32.2) |
| Pull Up Field | bir xil maydon bir necha vorisda |
| Pull Up Constructor Body | konstruktorlar boshida bir xil kod |
| Push Down Method | metod faqat bir vorisga tegishli (rad etilgan meros, 33.5) |
| Push Down Field | maydon faqat bir vorisda ishlatiladi |

Eslatma: yuqoriga ko'chirish vorislikni kuchaytiradi; agar natijada bazaviy sinf shishsa, kompozitsiyani ko'rib chiqish kerak (17.9).

## 36.16 Amalda qo'llash

- [ ] Bir necha javobgarlikka ega sinflarni Extract Class bilan bo'lib, har bir ko'chirishdan keyin test ishga tushiring.
- [ ] Ichki to'plamni qaytaradigan getter larni Encapsulate Collection bilan yoping.
- [ ] `Map<String, Object>` tarqalgan joylarni Encapsulate Record bilan turga aylantiring.
- [ ] Atrofida mantiq to'plangan primitivlarni Replace Primitive with Object bilan value object ga o'tkazing.
- [ ] Yaratilgandan keyin o'zgarmasligi kerak bo'lgan maydonlarning setter larini olib tashlang.
- [ ] Murakkab konstruktorlarni nomlangan statik fabrikalarga o'tkazing.
- [ ] Ikki darajali chaqiruv zanjirlarini Hide Delegate bilan yopib, delegat getter larini olib tashlang.
- [ ] Voris sinflardagi takrorlangan metod va maydonlarni Pull Up bilan birlashtiring, keyin bazaviy sinf hajmini tekshiring.

---

[&larr; 35. Refaktoring harakatlari katalogi I: funksiya va o'zgaruvchi](35-refaktoring-harakatlari-katalogi-i-funksiya.md) · [Mundarija](README.md) · [37. Refaktoring harakatlari katalogi III: shart, API va ierarxiya &rarr;](37-refaktoring-harakatlari-katalogi-iii-shart.md)
