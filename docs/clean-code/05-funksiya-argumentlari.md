<!-- doc: clean-code | chapter: 5 | part: II. Funksiya va boshqaruv oqimi -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 5. Funksiya argumentlari (Function Arguments)

<details>
<summary>Bu bobdagi 12 bo'lim</summary>

- [5.1 Argument soni: nol, bir, ikki, uch va undan keyin](#51-argument-soni-nol-bir-ikki-uch-va-undan-keyin)
- [5.2 Monadik shakllar: so'rov, o'zgartirish, hodisa](#52-monadik-shakllar-sorov-ozgartirish-hodisa)
- [5.3 Flag argumenti va uni ikki funksiyaga bo'lish](#53-flag-argumenti-va-uni-ikki-funksiyaga-bolish)
- [5.4 Tanlov (selector) argumenti va `enum` bilan almashtirish](#54-tanlov-selector-argumenti-va-enum-bilan-almashtirish)
- [5.5 Chiqish argumenti va `void` dan qaytishga o'tish](#55-chiqish-argumenti-va-void-dan-qaytishga-otish)
- [5.6 Argument obyekti va parametr guruhlari](#56-argument-obyekti-va-parametr-guruhlari)
- [5.7 Butun obyektni berish yoki maydonini berish](#57-butun-obyektni-berish-yoki-maydonini-berish)
- [5.8 Argument tartibi va bir xil turdagi qo'shni argumentlar](#58-argument-tartibi-va-bir-xil-turdagi-qoshni-argumentlar)
- [5.9 Varargs, `null` argument va ixtiyoriy parametrlar](#59-varargs-null-argument-va-ixtiyoriy-parametrlar)
- [5.10 Overload qilish tuzoqlari va nomni aniqlashtirish](#510-overload-qilish-tuzoqlari-va-nomni-aniqlashtirish)
- [5.11 Argumentni tekshirish joyi: chegara, konstruktor, domen](#511-argumentni-tekshirish-joyi-chegara-konstruktor-domen)
- [5.12 Amalda qo'llash](#512-amalda-qollash)

</details>


Uzun parametr ro'yxati patternlar hujjatida [uzun parametrlar ro'yxati anti-patterni](../patterns/25-anti-patternlar.md#2522-uzun-parametrlar-royxati-long-parameter-list) sifatida sanalgan. Bu bobda argumentlarning **shakli** ko'rib chiqiladi: nechta argument haqli, flag va selector argument nega zararli, chiqish argumenti nima uchun qoldirilgan, va argument obyekti qachon kerak.

## 5.1 Argument soni: nol, bir, ikki, uch va undan keyin

Argument soni funksiyani tushunish narxini belgilaydi, chunki har bir argument o'quvchidan savol so'raydi: bu nima, qanday tartibda, `null` bo'lishi mumkinmi. Shu sababli tartib aniq: nol argument eng yaxshi, bitta yaxshi, ikkita qabul qilinadi, uchta asoslanishi kerak, to'rtta va undan ko'pi deyarli har doim xato.

| Argument soni | Nomi | Holati |
|---|---|---|
| 0 | niladik | eng yaxshi: obyekt holatidan ishlaydi |
| 1 | monadik | yaxshi: so'rov, o'zgartirish yoki hodisa |
| 2 | diadik | qabul qilinadi, tartib xavfi bor |
| 3 | triadik | asoslanishi kerak, tartib xavfi yuqori |
| 4+ | poliadik | argument obyekti kerak (5.6) |

Diadik funksiyada tabiiy tartib bo'lsa, u xavfsiz: `new Point(x, y)`, `assertEquals(expected, actual)`. Tabiiy tartib bo'lmasa, nomlangan parametr yo'qligi Java da muammo tug'diradi va yechim turni kuchaytirishda (`Money` va `Quantity` ni aralashtirib bo'lmaydi).

## 5.2 Monadik shakllar: so'rov, o'zgartirish, hodisa

Bitta argumentli funksiyalar uch shaklga bo'linadi va har birining o'z konvensiyasi bor. **So'rov**: argument haqida savol beradi va javob qaytaradi (`boolean fileExists(String path)`). **O'zgartirish**: argumentni boshqa narsaga aylantiradi va natijani **qaytaradi** (`InputStream fileOpen(String path)`). **Hodisa**: argumentni qabul qilib tizim holatini o'zgartiradi va hech narsa qaytarmaydi (`void passwordAttemptFailedNTimes(int attempts)`).

Eng ko'p uchraydigan xato - o'zgartirish shaklida argumentni o'zgartirib, uni qaytarmaslik. Bu chiqish argumentiga aylanadi (5.5) va o'quvchi natijani qayerdan olishini bilmaydi.

## 5.3 Flag argumenti va uni ikki funksiyaga bo'lish

`boolean` argument funksiyaning ikki xil ish qilishini ochiq e'lon qiladi, ya'ni "bitta ish" qoidasini buzadi (4.2). Undan ham yomoni: chaqiruv joyida `render(true)` o'qilganda `true` nimani anglatishi ko'rinmaydi va o'quvchi funksiya imzosini ochadi.

```java
// yomon: chaqiruv joyi o'qilmaydi
report.render(true);
payment.process(order, false, true);

// yaxshi: har bir xatti-harakat o'z nomida
report.renderForSuite();
report.renderForSingleTest();
payment.processWithoutRetry(order);
```

Agar flag argumenti tashqi API dan kelgan bo'lsa va olib tashlab bo'lmasa, uni enum ga aylantirish ikkinchi yaxshi yechim: `render(RenderMode.SUITE)` hech bo'lmasa chaqiruv joyida o'qiladi.

**Tushunarsiz literalning nomi chaqiruv joyida ko'rinadi.** Enum ga aylantirish ham, imzoni o'zgartirish ham imkonsiz bo'lsa (uchinchi tomon kutubxonasi, generatsiya qilingan klient), oxirgi chora - literal yoniga nom izohi qo'yish. Python va Kotlin da nomlangan argument bor, Java da yo'q, shuning uchun Boswell va Foucher taklif qilgan shakl inline izoh bo'ladi va uning joyi muhim: izoh **qiymatdan oldin** turadi.

```java
void connect(int timeoutMs, boolean useEncryption) { ... }

// Tushunarsiz: 10 nima, false nima
connect(10, false);

// Yaxshi: izoh qiymatdan OLDIN, birlik nomda
connect(/* timeoutMs = */ 10, /* useEncryption = */ false);

// Yomon: qiymatdan keyingi izoh false ning ma'nosini ochmaydi
connect(10, false /* useEncryption */);
connect(10, false /* = useEncryption */);
```

Ikki tafsilot muhim. Birinchi: `boolean` argumentda izohning oldinda turishi ayniqsa zarur, chunki keyingi izoh "shifrlashni ishlat" yoki "shifrlashni ishlatma" degan savolga javob bermaydi. Ikkinchi: izoh parametrning haqiqiy nomini emas, **yaxshiroq nomni** ham yozishi mumkin - yuqoridagi misolda parametr `timeout` deb nomlangan bo'lsa ham izohda `timeoutMs` yozilgan, ya'ni izoh birlikni qo'shib nomni "tuzatadi". Eng yaxshi yechim esa hamon imzoni o'zgartirish: parametr nomining o'zi birlikni aytsa, izoh kerak bo'lmaydi.

## 5.4 Tanlov (selector) argumenti va `enum` bilan almashtirish

Selector argumenti - flag argumentining umumlashgan shakli: funksiya ichida `switch` yoki `if` bilan xatti-harakatni tanlaydi. U funksiyani bir necha vazifaga birlashtirib, har bir chaqiruvchini keraksiz kontekst bilan yuklaydi.

```java
// yomon: selector argumenti funksiyani ikki vazifaga birlashtirgan
public BigDecimal calculateWeeklyPay(boolean overtime) {
    int tenthRate = getTenthRate();
    int tenthsWorked = getTenthsWorked();
    int straightTime = Math.min(400, tenthsWorked);
    int overTime = Math.max(0, tenthsWorked - straightTime);
    int straightPay = straightTime * tenthRate;
    double overtimeRate = overtime ? 1.5 : 1.0 * tenthRate;
    int overtimePay = (int) Math.round(overTime * overtimeRate);
    return BigDecimal.valueOf(straightPay + overtimePay);
}

// yaxshi: siyosat alohida turda, funksiya bitta ish qiladi
public Money weeklyPay(OvertimePolicy policy) {
    Money straight = straightTimePay();
    return straight.add(policy.overtimePay(overtimeTenths(), tenthRate()));
}
```

## 5.5 Chiqish argumenti va `void` dan qaytishga o'tish

Chiqish argumenti - funksiyaga uzatilgan obyektni funksiya o'zgartirib, natijani shu obyekt orqali qaytarishi. Bu shakl o'quvchidan imzoni tekshirishni talab qiladi, chunki argument odatda **kirish** deb o'qiladi.

```java
// yomon: s ni kim o'zgartiradi, nimaga aylanadi - imzodan ko'rinmaydi
public void appendFooter(StringBuffer report) { report.append("..."); }
appendFooter(report);

// yaxshi: obyektning o'z holati o'zgaradi yoki yangi qiymat qaytadi
report.appendFooter();
String withFooter = report.withFooter();
```

Xuddi shu qoida to'plamlarga ham tegishli: metodga `List` berib, uni to'ldirib qaytarish o'rniga yangi `List` qaytarish kerak (23.11).

Buning ostida tilning semantikasi turadi va u tez-tez chalkashtiriladi: Java argumentni hamisha **qiymat bo'yicha** uzatadi, ya'ni metod o'zgaruvchining nusxasini oladi. Shuning uchun parametrni metod ichida qayta tayinlash chaqiruvchidagi o'zgaruvchiga hech qanday ta'sir qilmaydi. Havola nusxasi orqali **obyekt holatini** o'zgartirish esa ta'sir qiladi, chunki nusxa ham xuddi shu obyektga ishora qiladi. Chiqish argumenti aynan shu ikkinchi yo'ldan foydalanadi, shuning uchun uni imzodan sezish qiyin.

Shundan parametr bilan ishlashning ikkinchi qoidasi chiqadi: parametrga metod ichida qiymat tayinlanmaydi. Tayinlash chaqiruvchiga ko'rinmaydi, lekin pass-by-reference ga o'rgangan o'quvchi uni chiqish argumenti deb o'qiydi; bundan tashqari bitta nom metod boshida bir ma'noni, o'rtasida boshqa ma'noni tashiydi. O'rniga lokal o'zgaruvchi kiritiladi va parametr faqat "nima uzatilgan" degan ma'noda qoladi (Fowler da bu Remove Assignments to Parameters harakati; u ham temp uchun `result` nomini ishlatadi, 3.16).

```java
// yomon: parametr metod o'rtasida boshqa ma'noga o'tadi
int discount(int inputVal, int quantity) {
    if (inputVal > 50) {
        inputVal -= 2;        // chaqiruvchida o'zgarmaydi, o'quvchi esa o'zgaradi deb o'ylaydi
    }
    return inputVal;
}

// yaxshi: kirish o'zgarmaydi, natija alohida nomda
int discount(int inputVal, int quantity) {
    int result = inputVal;
    if (inputVal > 50) {
        result -= 2;
    }
    return result;
}
```

Jamoa buni kompilyatorga topshirishi ham mumkin: parametrni `final` qilib e'lon qilish tayinlashni umuman taqiqlaydi va Checkstyle ning `FinalParameters` qoidasi buni butun kod bazasida majburlaydi (42.3). Qoida boshqa tillarga ko'chmaydi: chiqish parametri bor tillarda tayinlash qonuniy vosita bo'lib qolaveradi.

## 5.6 Argument obyekti va parametr guruhlari

Uch yoki undan ko'p argument birga sayohat qilsa (data clump), ular aslida bir tushuncha. Ularni obyektga yig'ish argument sonini kamaytirmaydi - u tushunchaga nom beradi, va shu nom kod bazasida qayta ishlatiladi.

```java
// yomon: beshta argument, tartibi yodda saqlanadi
void createReservation(Long customerId, String sku, int quantity,
                       LocalDate from, LocalDate to) { ... }

// yaxshi: ikki tushuncha nomlangan
void createReservation(ReservationRequest request) { ... }

record ReservationRequest(CustomerId customer, Sku sku, Quantity quantity,
                          DateRange period) {
    ReservationRequest {
        if (quantity.isZeroOrLess()) throw new IllegalArgumentException("quantity");
        Objects.requireNonNull(period, "period");
    }
}
```

Qo'shimcha foyda: validatsiya bir joyga to'planadi (5.11) va `DateRange` o'z invariantini (`from <= to`) o'zi himoya qiladi.

## 5.7 Butun obyektni berish yoki maydonini berish

Ikki yo'nalishdagi qarorning oddiy mezoni bor. Agar funksiya obyektning uch yoki undan ko'p maydonini olsa, butun obyektni berish kerak (Preserve Whole Object, [37-bob](37-refaktoring-harakatlari-katalogi-iii-shart.md)). Agar funksiya obyektning faqat bitta maydonini olsa va obyekt haqida hech narsa bilishi shart bo'lmasa, maydonni berish bog'liqlikni kamaytiradi.

```java
// yomon: uchta maydon ajratib olingan, bog'liqlik yashirin
boolean within = range.includes(order.getCreatedAt(), order.getTimezone(), order.getRegion());

// yaxshi: butun obyekt
boolean within = range.includes(order);

// yaxshi (teskari holat): faqat bitta qiymat kerak, obyekt kerak emas
boolean expired = clock.isAfter(order.expiresAt());
```

## 5.8 Argument tartibi va bir xil turdagi qo'shni argumentlar

Eng xavfli imzo - yonma-yon turgan bir xil turdagi argumentlar, chunki ularni almashtirib yuborish kompilyatsiyadan o'tadi va faqat production da ko'rinadi.

```java
// yomon: ikki String va ikki int - almashtirsa kompilyator jim turadi
void transfer(String from, String to, int amount, int fee);
transfer(toAccount, fromAccount, fee, amount);   // xato, kompilyator sezmaydi

// yaxshi: tur o'zi xatoni to'sadi
void transfer(AccountNumber from, AccountNumber to, Money amount, Money fee);
// eng yaxshi: tushuncha obyektga yig'ilgan
void execute(TransferInstruction instruction);
```

Tartib bo'yicha konvensiya: muhimdan kam muhimga, obyekt birinchi, sozlama oxirida, `callback` eng oxirida (lambda ni chaqiruv joyida o'qiladigan qiladi).

Shu konvensiyaning eski va aniqroq shakli **kirish-o'zgartirish-chiqish** tartibi: faqat o'qiladigan parametrlar birinchi, o'qilib ham o'zgartiriladigani ikkinchi, faqat yoziladigani uchinchi. Tartib shu bilan metod ichidagi amal ketma-ketligini takrorlaydi: ma'lumotni ol, o'zgartir, natijani qaytar. Tartibni tasodifiy yoki alifbo bo'yicha qo'yish shu ma'noni yo'qotadi (McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 7.5 (174-bet)). McConnell bu konvensiya C kutubxonasining "o'zgaradigan parametr birinchi" an'anasiga zid ekanini ham aytadi va ikkisidan qaysi birini tanlasang ham **izchil** qo'llashni talab qiladi; Java standart kutubxonasining o'zi ikki tomonda turadi (`System.arraycopy(src, srcPos, dest, destPos, length)` kirishni oldinga, `Collections.copy(dest, src)` esa chiqishni oldinga qo'yadi).

Java da chiqish argumenti baribir tavsiya qilinmaydi ([chiqish argumenti va `void` dan qaytishga o'tish](#55-chiqish-argumenti-va-void-dan-qaytishga-otish)), shuning uchun qoida amalda ikki qismga qisqaradi: faqat o'qiladigan parametrlar oldinda, to'ldiriladigan yoki o'zgartiriladigan yagona nishon esa oxirida.

```java
// yomon: nishon oldinda, kirish keyinda - o'qilishi teskari
void render(StringBuilder out, Invoice invoice, Locale locale);

// yaxshi: kirish -> o'zgartiriladigan nishon
void render(Invoice invoice, Locale locale, StringBuilder out);

// eng yaxshi: nishon umuman yo'q, natija qaytadi
String render(Invoice invoice, Locale locale);
```

Tartibni eslab qolish muammosini **tur** bilan hal qilish (yuqoridagi
`AccountNumber`, `Money`) eng ishonchli yo'l, lekin yagona emas. Ikkinchi yo'l
nom bilan ishlaydi: argument nomlari funksiya nomining o'ziga kodlanadi.
Martin bu shaklni "keyword" deb ataydi va `assertEquals` ni
`assertExpectedEqualsActual(expected, actual)` deb yozish mumkinligini
ko'rsatadi; bu argument tartibini yodda saqlash muammosini keskin
yumshatadi (Martin, *Clean Code*, 3-bob (43-bet)). Shu yerda bir argumentli
funksiya uchun qoida ham turadi: funksiya nomi va argumenti fe'l/ot juftini
tashkil qilsin - `write(name)` yaxshi, `writeField(name)` yanada yaxshi,
chunki `name` ning nima ekani ham aytiladi.

Ikki yo'lni solishtirish qiyin emas: tur bilan hal qilish kompilyatorni ishga
soladi va chaqiruv joyini qisqa qoldiradi, nom bilan hal qilish esa hech narsa
talab qilmaydi, lekin nom uzayadi va kompilyator baribir jim turadi. Shuning
uchun tartib quyidagicha: bir xil turdagi qo'shni argumentlar bo'lsa, avval
turni ajratish; tur ajratib bo'lmaydigan joyda (ikki `Money`, ikki `Instant`)
keyword shakli yoki argument obyekti qoladi.

```java
// yomon: ikki Instant yonma-yon, tartib faqat hujjatda
Report build(Instant from, Instant to);

// yaxshi: nom tartibni imzoda aytadi (keyword shakli)
Report buildFromUntil(Instant from, Instant until);

// eng yaxshi: oraliq tushuncha bo'lib, tartib ichiga ko'chdi
Report build(DateRange range);
```

## 5.9 Varargs, `null` argument va ixtiyoriy parametrlar

`varargs` o'qilishi uchun foydali, lekin uch tuzog'i bor: nol argument bilan chaqirish mumkin (kutilmagan bo'sh holat), avtomatik massiv yaratiladi (issiq yo'lda narx), va overload bilan birga ishlatilsa tanlov qoidalari chalkash bo'ladi. Qoida: `varargs` dan oldin kamida bitta majburiy parametr qo'yish.

`null` ni argument sifatida uzatish deyarli har doim xato (18.7). Ixtiyoriy parametr kerak bo'lsa, uch yechim bor va tartibi shunday: overload qilingan metod, builder, yoki `Optional` parametr (eng kam afzal, chunki chaqiruv joyi shovqinli bo'ladi).

```java
// yaxshi: overload bilan ixtiyoriylik
public Page<Order> search(OrderCriteria criteria) { return search(criteria, Pageable.unpaged()); }
public Page<Order> search(OrderCriteria criteria, Pageable pageable) { ... }

// yaxshi: varargs oldida majburiy parametr bor
public void audit(AuditEvent event, Tag... tags) { ... }
```

To'rtinchi tuzoq generik bilan birga chiqadi: `List<String>...` kabi parametr ichida generik massiv yaratiladi, Java da esa generik massiv tur xavfsiz emas. Kompilyator shu sababli ogohlantirish beradi. Metod massivni tashqariga bermasa va unga faqat o'qish uchun tegsa, ogohlantirish `@SafeVarargs` bilan yopiladi; metod massivni qaytarsa yoki saqlasa, `@SafeVarargs` yolg'on bo'ladi va o'rniga `List<List<String>>` parametri yoziladi.

```java
// yaxshi: massiv tashqariga chiqmaydi, shuning uchun xavfsiz
@SafeVarargs
static <T> List<T> concat(List<T>... lists) {
    return Arrays.stream(lists).flatMap(List::stream).toList();
}
```

Shartning kengroq shakli shunday: generik `varargs` massivini boshqa metodga **berish** xavfli, va faqat ikki istisno xavfsiz. Birinchi: to'g'ri `@SafeVarargs` qo'yilgan boshqa `varargs` metodiga berish. Ikkinchi: massiv tarkibidan funksiya hisoblaydigan, `varargs` bo'lmagan metodga berish (masalan `Arrays.stream`). Qolgan hollarda massiv tashqariga chiqadi va xato chaqiruv joyidan ikki qavat uzoqda, `ClassCastException` shaklida chiqadi.

`@SafeVarargs` ni qo'yish joyi ham cheklangan: u faqat override qilinmaydigan metodda qonuniy, ya'ni `static`, `final` va Java 9 dan boshlab `private` metodda. Sababi oddiy: annotatsiya metod tanasining xavfsizligi haqidagi va'da, har qanday override ning tanasi uchun esa bu va'dani berib bo'lmaydi.

## 5.10 Overload qilish tuzoqlari va nomni aniqlashtirish

Overload qilish bir xil tushunchaning turli kirish shakllari uchun yaxshi (`of(int)`, `of(String)`). Lekin **xatti-harakat** farq qilsa, overload o'quvchini chalg'itadi: qaysi metod chaqirilayotganini tur xulosasi hal qiladi va bu kodda ko'rinmaydi.

```java
// yomon: ikkisi boshqa ish qiladi, tanlov tur orqali yashiringan
void remove(int index);        // indeks bo'yicha
void remove(Integer element);  // qiymat bo'yicha - klassik tuzoq

// yaxshi: nom farqni aytadi
void removeAt(int index);
void removeValue(Integer element);
```

Qo'shimcha qoida: overload qilingan metodlar bir xil sonli argument bilan turlicha ishlamasligi, va `null` uzatilganda qaysi biri tanlanishi aniq bo'lishi kerak.

Tuzoqning sababi kompilyatorning tanlov tartibida. Spetsifikatsiya nomzodlarni
avval nom, ko'rinish va **arity** bo'yicha yig'adi, keyin tanlovni uch bosqichda
qiladi: birinchi bosqich boxing, unboxing va varargs siz (strict invocation);
ikkinchisi boxing va unboxing bilan, lekin varargs siz (loose invocation);
uchinchisi varargs bilan. Har bosqichda nomzod topilmasa keyingisiga o'tiladi,
bir bosqichda bir nechtasi mos kelsa esa eng aniqi (most specific) tanlanadi
(*The Java Language Specification, Java SE 25 Edition*, 15.12.2 (631-632-bet) va
15.12.2.1 (637-bet)).

Shundan ikki amaliy natija chiqadi. Birinchi: tanlov **statik** turlar bilan,
kompilyatsiya vaqtida qilinadi; obyektning ish vaqtidagi haqiqiy turi hech
narsani o'zgartirmaydi, shuning uchun `Object o = "satr"; print(o);` chaqiruvi
`print(Object)` ni oladi. Ikkinchi va xavflisi: yangi overload qo'shilishi
mavjud chaqiruvni jim boshqa metodga yo'naltirishi mumkin. Spetsifikatsiya
misolini beradi: sinfda `m(Object)` bor bo'lsa va unga `m(Object...)` qo'shilsa,
`m(null)` chaqiruvi endi `m(Object[])` ni oladi, chunki u aniqroq (shu yerda,
15.12.2 (632-bet)).

```java
// yomon: ikkinchi overload qo'shilishi m(null) ning ma'nosini o'zgartiradi
void audit(Object payload);
void audit(Object... payloads);        // qo'shilgandan keyin audit(null) bu yerga tushadi

// yomon: statik tur hal qiladi, ish vaqtidagi tur emas
Object value = "satr";
format(value);                         // format(Object), format(String) emas

// yaxshi: nom farqni aytadi, tanlov kompilyatorga qoldirilmaydi
void auditOne(Object payload);
void auditAll(List<Object> payloads);
```

Qoida: public API ga yangi overload qo'shish binar moslikni saqlasa ham xulqni
o'zgartirishi mumkin, shuning uchun u yangi metod nomi qo'shishdan qimmatroq
qaror. `null` bilan chaqiriladigan joyda esa tur oshkor cast bilan yoziladi
(`audit((Object) null)`) yoki chaqiruv umuman boshqa nomli metodga o'tkaziladi.

Overload qachon haqli ekanini bitta mezon aniqlaydi: bir xil arity li overload lar faqat kamida bitta mos pozitsiyadagi parametr **radikal farqli** turda bo'lsa xavfsiz. Ikki tur radikal farqli deyiladi, agar `null` bo'lmagan hech bir ifodani ikkalasiga ham cast qilib bo'lmasa (`int` va `Collection`, `String` va `int[]`). Shunday bo'lsa chaqiruv joyida qaysi metod tanlanishi argumentning e'lon qilingan turidan ko'rinadi va tanlov kompilyator ichida yashirinmaydi.

Funksional interfeyslar bu mezonni buzadi va alohida tilga olinadi: bir xil argument pozitsiyasida turli funksional interfeyslarni oladigan overload lar yozilmaydi. Lambda va metod havolasining turi kontekstdan chiqadi, shuning uchun klientda noaniqlik tug'iladi va chaqiruv joyi cast yozishga majbur bo'ladi. `ExecutorService.submit` ning `Callable<T>` va `Runnable` overload lari shu holatning kutubxonadagi misoli.

```java
// yomon: ikki funksional interfeys bir pozitsiyada
void schedule(Runnable task);
void schedule(Callable<Void> task);     // klient cast yozishga majbur

// yaxshi: nom farqni aytadi, radikal farqli turlar esa overload bo'lib qolaveradi
void scheduleTask(Runnable task);
void scheduleCall(Callable<Void> task);
```

## 5.11 Argumentni tekshirish joyi: chegara, konstruktor, domen

Validatsiyani har bir metodda takrorlash kodni shishiradi; umuman tekshirmaslik xatoni chuqurga suradi. To'g'ri yechim - tekshirishni joy bo'yicha taqsimlash.

| Daraja | Nima tekshiriladi | Vosita |
|---|---|---|
| Tashqi chegara (controller) | format, majburiylik, diapazon | Bean Validation `@Valid` |
| Value object konstruktori | invariant (`from <= to`) | `record` compact konstruktori |
| Domen metodi | biznes qoidasi, holat | domen istisnosi |
| Public kutubxona API | `null` va shartnoma | `Objects.requireNonNull` |
| Private metod | hech narsa (ishonadi) | assertion, ixtiyoriy |
| Repository | hech narsa | domen allaqachon tekshirgan |

Shu taqsimot "fail fast" ni ta'minlaydi (18.10) va ichki metodlarni toza qoldiradi: ular allaqachon to'g'ri ma'lumot oladi.

Jadvalga bitta istisno qo'shiladi: tekshiruv qimmat yoki amalda bajarilmas bo'lsa va hisob jarayonining o'zi uni bilvosita bajarsa, oshkor tekshiruv shart emas. `Collections.sort` elementlarning bir-biri bilan solishtirilishini saralash paytida o'zi tekshiradi, shuning uchun oldin ro'yxatni aylanib `Comparable` ekanini tasdiqlash ortiqcha ish. Lekin bu istisnoning narxi bor: bilvosita tekshiruvda xato ish o'rtasida chiqadi, ya'ni amal atomarligini yo'qotishi mumkin, shuning uchun u faqat qisman bajarilgan ish zarar qilmaydigan joyda qo'llanadi.

Teskari tomondan ogohlantirish ham bor: parametrga o'zboshimchalik bilan cheklov qo'yish yaxshi narsa emas. Metod amaliy darajada qanchalik umumiy bo'lsa, shuncha yaxshi: "faqat musbat son" yoki "faqat 100 tagacha element" kabi shart amalda kerak bo'lmasa, u faqat chaqiruvchini cheklaydi va keyinroq olib tashlanganda API o'zgarishiga aylanadi. Shuning uchun tekshiruv invariantni himoya qiladi, dasturchining ehtiyotkorligini emas.

## 5.12 Amalda qo'llash

- [ ] `boolean` parametri bor barcha public metodlarni grep qilib, har birini ikki metodga yoki enum parametriga aylantiring.
- [ ] To'rt va undan ko'p parametrli metodlarni ro'yxatlab, birga sayohat qiladigan parametr guruhlarini record ga yig'ing.
- [ ] Yonma-yon bir xil turdagi parametrlar bor imzolarni topib, value object joriy qiling (`AccountNumber`, `Money`).
- [ ] Chiqish argumenti ishlatilgan joylarni (`void f(StringBuilder out)`) qaytish qiymatiga o'tkazing.
- [ ] `null` uzatilishi kutilgan parametrlarni overload yoki builder bilan almashtiring.
- [ ] Overload qilingan metodlar ro'yxatini chiqarib, xatti-harakati farq qiladiganlarini qayta nomlang.
- [ ] Validatsiya 5.11 jadvalidagi darajalarga mos taqsimlanganini tekshirib, takrorlangan tekshiruvlarni olib tashlang.
- [ ] Yangi public API uchun "3 dan ko'p parametr review da asoslanadi" qoidasini kiritib, PR shabloniga qo'shing.

## Manbalar

- Dustin Boswell, Trevor Foucher, *The Art of Readable Code*, 1-nashr, O'Reilly, 2011 (copyright 2012), 6-bob (63-64-betlar) - chaqiruvdagi tushunarsiz literal uchun nom izohi, izohning qiymatdan OLDIN turishi, `boolean` argumentda bu tartibning zarurati va izohda parametr nomiga birlik qo'shish
- Robert C. Martin, *Clean Code*, 3-bob ("Function Arguments") - nol, bir, ikki, uch argument tartibi va poliadik funksiya
- Robert C. Martin, *Clean Code*, 3-bob ("Flag Arguments", "Output Arguments") - flag argumenti funksiyani ikkiga bo'ladi, chiqish argumenti o'rniga qaytish qiymati
- Joshua Bloch, *Effective Java* 3rd, Item 51 - metod imzosini ehtiyotkorlik bilan loyihalash, to'rtta yoki undan kam parametr
- Joshua Bloch, *Effective Java* 3rd, Item 52, 53 - overload va varargs ni o'rinli ishlatish
- Joshua Bloch, *Effective Java* 3rd, Item 49 - parametr yaroqliligini tekshirish joyi
- Robert C. Martin, *Clean Code*, 17-bob, F1-F3 - ko'p argument, chiqish argumenti, flag argumenti
- Steve McConnell, *Code Complete*, 2-nashr, 7.5 (174-bet) - parametrlarni kirish-o'zgartirish-chiqish tartibida qo'yish va C an'anasi bilan ziddiyat
- [Java API, `java.util.Collections`](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Collections.html) - `copy(dest, src)` imzosi: nishon birinchi
- Robert C. Martin, *Clean Code*, 3-bob ("Verbs and Keywords") (43-bet) - fe'l/ot jufti (`write(name)`, `writeField(name)`) va keyword shakli: argument nomlarini funksiya nomiga kodlash, `assertExpectedEqualsActual(expected, actual)`
- *The Java Language Specification, Java SE 25 Edition* (Gosling, Joy, Steele, Bracha, Buckley, Smith, Bierman), 15.12.2 (631-632-betlar) - overload tanlashning uch bosqichi (strict, loose, variable arity), eng aniq nomzodning tanlanishi va `m(Object...)` qo'shilishi `m(null)` ni boshqa metodga yo'naltirishi
- *The Java Language Specification, Java SE 25 Edition* (Gosling, Joy, Steele, Bracha, Buckley, Smith, Bierman), 15.12.2.1 (637-bet) - nomzodlarni nom, ko'rinish va arity bo'yicha yig'ish sharti
- Jeanne Boyarsky, Scott Selikoff, *OCP Oracle Certified Professional Java SE 17 Developer Study Guide*, Sybex, 5-bob (253-bet) - Java ning faqat qiymat bo'yicha uzatishi: metod o'zgaruvchining nusxasini olishi, parametrni qayta tayinlash chaqiruvchiga ta'sir qilmasligi, havola nusxasi orqali obyekt holatini o'zgartirish esa ta'sir qilishi
- Martin Fowler, *Refactoring*, 1-nashr, Addison-Wesley, 1999, 6-bob (107-bet) - Remove Assignments to Parameters: parametrga tayinlamaslik, o'rniga temp (`result`) kiritish, sabab sifatida pass-by-value va pass-by-reference chalkashligi, qoidaning chiqish parametri bor tillarga ko'chmasligi
- Joshua Bloch, *Effective Java* 3rd, Item 32 (148-bet) - generik `varargs` massivini boshqa metodga berishning ikki xavfsiz istisnosi: to'g'ri `@SafeVarargs` qo'yilgan `varargs` metodi va massiv tarkibidan funksiya hisoblaydigan `varargs` bo'lmagan metod
- Joshua Bloch, *Effective Java* 3rd, Item 32 (149-bet) - `@SafeVarargs` faqat override qilinmaydigan metodda (`static`, `final`, Java 9 dan `private`) qonuniy ekani
- Joshua Bloch, *Effective Java* 3rd, Item 52 (241-bet) - bir xil arity li overload lar uchun "radikal farqli tur" mezoni: `null` bo'lmagan hech bir ifodani ikkala turga ham cast qilib bo'lmasligi
- Joshua Bloch, *Effective Java* 3rd, Item 44 (202-bet) - bir xil argument pozitsiyasida turli funksional interfeyslarni oladigan overload lar klientda noaniqlik tug'dirishi va cast talab qilishi (`ExecutorService.submit`)
- Joshua Bloch, *Effective Java* 3rd, Item 49 (230-bet) - hisob jarayonida bilvosita bajariladigan tekshiruv uchun oshkor tekshiruvning shart emasligi (`Collections.sort`) va bunga tayanishning atomarlikka ta'siri; parametrga o'zboshimchalik bilan cheklov qo'ymaslik
- ESLATMA: `scheduleTask`/`scheduleCall` va `discount` kod misollari korpus qo'shimchasi; `discount` misolining shakli Fowler ning 107-betdagi misoliga tayanadi, Spring va Checkstyle ko'rinishi (`FinalParameters`) esa korpus qo'shimchasi

---

[&larr; 4. Funksiya: kichiklik va bitta ish](04-funksiya-kichiklik-va-bitta-ish.md) · [Mundarija](README.md) · [6. Shart, mantiq va boshqaruv oqimi &rarr;](06-shart-mantiq-va-boshqaruv-oqimi.md)
