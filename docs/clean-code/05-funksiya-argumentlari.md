<!-- doc: clean-code | chapter: 5 | part: II. Funksiya va boshqaruv oqimi -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: AI yozgan, inson tekshirmagan.

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

## 5.12 Amalda qo'llash

- [ ] `boolean` parametri bor barcha public metodlarni grep qilib, har birini ikki metodga yoki enum parametriga aylantiring.
- [ ] To'rt va undan ko'p parametrli metodlarni ro'yxatlab, birga sayohat qiladigan parametr guruhlarini record ga yig'ing.
- [ ] Yonma-yon bir xil turdagi parametrlar bor imzolarni topib, value object joriy qiling (`AccountNumber`, `Money`).
- [ ] Chiqish argumenti ishlatilgan joylarni (`void f(StringBuilder out)`) qaytish qiymatiga o'tkazing.
- [ ] `null` uzatilishi kutilgan parametrlarni overload yoki builder bilan almashtiring.
- [ ] Overload qilingan metodlar ro'yxatini chiqarib, xatti-harakati farq qiladiganlarini qayta nomlang.
- [ ] Validatsiya 5.11 jadvalidagi darajalarga mos taqsimlanganini tekshirib, takrorlangan tekshiruvlarni olib tashlang.
- [ ] Yangi public API uchun "3 dan ko'p parametr review da asoslanadi" qoidasini kiritib, PR shabloniga qo'shing.

---

[&larr; 4. Funksiya: kichiklik va bitta ish](04-funksiya-kichiklik-va-bitta-ish.md) · [Mundarija](README.md) · [6. Shart, mantiq va boshqaruv oqimi &rarr;](06-shart-mantiq-va-boshqaruv-oqimi.md)
