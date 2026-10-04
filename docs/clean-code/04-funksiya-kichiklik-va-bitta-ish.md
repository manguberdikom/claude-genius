<!-- doc: clean-code | chapter: 4 | part: II. Funksiya va boshqaruv oqimi -->

[Toza kod yozuvchining qoidalari](../../README.md) / [Toza kod qoidalari](README.md)

# 4. Funksiya: kichiklik va bitta ish (Functions: Small and Doing One Thing)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

- [4.1 Birinchi qoida: kichik; ikkinchi qoida: yana kichikroq](#41-birinchi-qoida-kichik-ikkinchi-qoida-yana-kichikroq)
- [4.2 "Bitta ish qiladi" ni qanday tekshirish](#42-bitta-ish-qiladi-ni-qanday-tekshirish)
- [4.3 Bo'limlari bor funksiya bitta ish qilmaydi](#43-bolimlari-bor-funksiya-bitta-ish-qilmaydi)
- [4.4 Pastga tushish qoidasi va gazeta metaforasi](#44-pastga-tushish-qoidasi-va-gazeta-metaforasi)
- [4.5 Funksiyadan funksiya chiqarish mexanikasi](#45-funksiyadan-funksiya-chiqarish-mexanikasi)
- [4.6 Funksiya nomi uzunligi va aniqligi](#46-funksiya-nomi-uzunligi-va-aniqligi)
- [4.7 Funksiya qaytish nuqtalari: bitta `return` afsonasi](#47-funksiya-qaytish-nuqtalari-bitta-return-afsonasi)
- [4.8 Funksiya ichidagi bo'sh joy, blok va qavs](#48-funksiya-ichidagi-bosh-joy-blok-va-qavs)
- [4.9 Yordamchi funksiyalar soni va joylashuvi](#49-yordamchi-funksiyalar-soni-va-joylashuvi)
- [4.10 Funksiyani birinchi urinishda toza yozish mumkin emas](#410-funksiyani-birinchi-urinishda-toza-yozish-mumkin-emas)
- [4.11 Amalda qo'llash](#411-amalda-qollash)

</details>


Metod uzunligi, ichma-ich shartlar va erta qaytish [arxitektor hujjatidagi](../architect/README.md) metod uzunligi va erta qaytish bo'limida ko'rib chiqilgan. Bu bobda funksiya qoidalarining qolgan qismi: "bitta ish qiladi" ni qanday tekshirish, pastga tushish qoidasi, ajratib olish mexanikasi va funksiyani toza holatga keltirish tartibi.

## 4.1 Birinchi qoida: kichik; ikkinchi qoida: yana kichikroq

Funksiyaning to'g'ri uzunligi haqida aniq son berish qiyin, lekin kuzatish bor: toza kod bazalarida funksiyalarning katta qismi 4-12 qator oralig'ida bo'ladi va har biri bir ekranga sig'adi. Shu hajmda funksiya nomi uning butun mazmunini qamrab oladi, test yozish oson bo'ladi va qayta ishlatish imkoniyati paydo bo'ladi.

Kichik funksiyadan qo'rqishning odatiy sababi - "juda ko'p metod bo'lib ketadi". Amalda esa teskari natija chiqadi: metodlar soni oshadi, lekin har birining o'qish narxi tushadi va jami o'qish vaqti qisqaradi. Bundan tashqari, nomlangan kichik funksiya izohni almashtiradi (8.2).

```java
// yomon: bitta funksiya to'rt ishni bajaradi, 30+ qator
public void processOrder(Order order) {
    if (order.getItems().isEmpty()) throw new IllegalArgumentException();
    BigDecimal total = BigDecimal.ZERO;
    for (OrderItem item : order.getItems()) {
        total = total.add(item.getPrice().multiply(BigDecimal.valueOf(item.getQty())));
    }
    if (order.getCustomer().getTier().equals("GOLD")) {
        total = total.multiply(new BigDecimal("0.9"));
    }
    order.setTotal(total);
    jdbc.update("update orders set total = ? where id = ?", total, order.getId());
    mailSender.send(order.getCustomer().getEmail(), "Buyurtma qabul qilindi", "...");
}

// yaxshi: har bir qadam nomlangan, asosiy funksiya hikoyani aytadi
public void placeOrder(Order order) {
    requireNonEmpty(order);
    Money total = pricing.totalFor(order);
    order.applyTotal(total);
    orderRepository.save(order);
    notifications.orderAccepted(order);
}
```

## 4.2 "Bitta ish qiladi" ni qanday tekshirish

"Bitta ish" ta'rifi noaniq ko'rinadi, lekin aniq sinovi bor: funksiyadan ma'noli nom bilan boshqa funksiya ajratib olish mumkin bo'lsa va u shunchaki asl funksiyaning qayta ifodasi bo'lmasa, demak funksiya bir necha ish qilayotgan edi.

Ikkinchi sinov abstraksiya darajasida: funksiya ichidagi barcha gaplar nom aytgan abstraksiyadan **bir daraja pastda** bo'lishi kerak ([patternlar hujjatidagi](../patterns/README.md) yagona abstraksiya darajasi printsipi shu printsipni ta'riflaydi). `placeOrder` ichida `jdbc.update(...)` turishi ikki darajani buzadi, chunki SQL "buyurtma berish" dan ikki daraja past.

```java
// yomon: uchta daraja bir funksiyada (siyosat, mapping, SQL)
public Money priceFor(OrderDraft draft) {
    var rate = jdbcTemplate.queryForObject(
            "select rate from tax_rate where region = ?", BigDecimal.class, draft.region());
    Money net = draft.lines().stream().map(this::lineTotal).reduce(Money.ZERO, Money::add);
    return net.add(net.multiply(rate));
}

// yaxshi: bir funksiya - bir daraja
public Money priceFor(OrderDraft draft) {
    Money net = netAmountOf(draft);
    return net.add(taxPolicy.taxFor(draft.region(), net));
}
```

## 4.3 Bo'limlari bor funksiya bitta ish qilmaydi

Agar funksiya ichida `// --- validatsiya ---`, `// --- hisoblash ---`, `// --- saqlash ---` kabi izohli bo'limlar paydo bo'lsa, bu eng ishonchli signal: bo'limlar aslida alohida funksiyalar bo'lishi kerak va izohlar ularning nomi bo'ladi. Shu almashtirish izohni ham, uzunlikni ham bir vaqtda yo'qotadi.

Shu signalning boshqa shakllari: funksiya ichida bo'sh qatorlar bilan ajratilgan guruhlar, `region` yoki `#region` belgilari (9.7), va funksiya boshida "bu funksiya quyidagini qiladi: 1) ... 2) ..." izohi.

## 4.4 Pastga tushish qoidasi va gazeta metaforasi

Kod gazeta kabi o'qilishi kerak: sarlavha eng umumiy, keyin asosiy mazmun, oxirida mayda tafsilot. Funksiyalar uchun bu "pastga tushish qoidasi" (stepdown rule) deb ataladi: har bir funksiya o'zidan keyin keladigan funksiyalarni chaqiradi va har bir qadamda abstraksiya darajasi bir pog'ona tushadi.

```java
public final class SettlementImporter {

    // 1-daraja: butun jarayon
    public void importDailyFile(Path file) {
        List<SettlementRow> rows = parse(file);
        List<SettlementRow> valid = rejectInvalid(rows);
        apply(valid);
    }

    // 2-daraja: har bir qadamning mazmuni
    private List<SettlementRow> parse(Path file) { ... }
    private List<SettlementRow> rejectInvalid(List<SettlementRow> rows) { ... }
    private void apply(List<SettlementRow> rows) { ... }

    // 3-daraja: mayda tafsilot
    private boolean hasKnownCurrency(SettlementRow row) { ... }
}
```

Shu tartib buzilsa, o'quvchi faylni yuqoriga-pastga aylantirib o'qiydi va kontekstni yo'qotadi.

## 4.5 Funksiyadan funksiya chiqarish mexanikasi

Ajratish (extract) eng ko'p ishlatiladigan refaktoring va uning xavfsiz tartibi bor. Birinchi, ajratilayotgan qatorlarni belgilab, ular ishlatadigan mahalliy o'zgaruvchilarni aniqlash. Ikkinchi, ulardan nechtasi o'zgartirilayotganini sanash: bittasi bo'lsa qaytish qiymatiga aylanadi, bir nechtasi bo'lsa oldin o'zgaruvchilarni bo'lish kerak ([35-bob](35-refaktoring-harakatlari-katalogi-i-funksiya.md)). Uchinchi, IDE refaktoringi bilan bajarish. To'rtinchi, nomni mazmunga qarab emas, **maqsadga** qarab tanlash.

```java
// Ajratishdan oldin: nima qilayotgani kodda, nega qilayotgani yo'q
if (order.createdAt().isBefore(now.minusDays(30))
        && order.status() == OrderStatus.PENDING) {
    order.expire();
}

// Ajratishdan keyin: nom maqsadni aytadi
if (isStalePending(order)) {
    order.expire();
}

private boolean isStalePending(Order order) {
    return order.status() == OrderStatus.PENDING
            && order.createdAt().isBefore(clock.instant().minus(STALE_AFTER));
}
```

Ajratishdan keyin darhol tekshirish: yangi funksiya nomi `And`, `Or`, `Then` so'zlarini o'z ichiga olmasligi kerak. Olsa, u bitta ish qilmaydi.

## 4.6 Funksiya nomi uzunligi va aniqligi

Private funksiya nomi uzun bo'lishi mumkin va bo'lishi kerak, chunki u faqat bir joyda chaqiriladi va uning vazifasi izohni almashtirish. `includeSetupAndTeardownPages` nomi uzun, lekin izohdan arzon.

Nomni tanlashning amaliy usuli: funksiyani izoh bilan tasvirlab ko'ring, keyin shu izohni nomga aylantiring. Izoh "yaroqsiz qatorlarni olib tashlaydi va qolganini qaytaradi" bo'lsa, nom `rejectInvalidRows` bo'ladi.

## 4.7 Funksiya qaytish nuqtalari: bitta `return` afsonasi

"Funksiyada bitta `return` bo'lishi kerak" qoidasi strukturali dasturlash davridan qolgan va kichik funksiyalarda zarar qiladi: u guard clause ni ([arxitektor hujjatidagi](../architect/README.md) metod uzunligi va erta qaytish bo'limi) imkonsiz qiladi va ichma-ich shartlarni ko'paytiradi.

Haqiqiy qoida boshqa: funksiya kichik bo'lsa, bir necha `return` muammo emas. Muammo faqat katta funksiyada paydo bo'ladi, chunki o'quvchi chiqish nuqtalarini sanab chiqolmaydi. Shu sababli yechim `return` sonini kamaytirish emas, funksiyani kichraytirish.

```java
// yaxshi: uchta return, lekin funksiya kichik va har biri aniq
Optional<Discount> bestDiscount(Customer customer, Money total) {
    if (customer.isBlocked()) return Optional.empty();
    if (total.isLessThan(MIN_DISCOUNTABLE)) return Optional.empty();
    return discounts.stream().filter(d -> d.appliesTo(customer)).max(byAmount());
}
```

## 4.8 Funksiya ichidagi bo'sh joy, blok va qavs

`if`, `else`, `while` bloklari bir qatordan oshmasligi kerak, va o'sha bir qator ko'pincha funksiya chaqiruvi bo'ladi. Bu qoida ichma-ich chuqurlikni avtomatik ravishda bir darajada ushlab turadi.

Qavslarni tashlab yuborish (`if (x) doIt();`) esa alohida xato manbasi: keyingi o'zgartirishda ikkinchi qator qo'shiladi va shart faqat birinchisiga tegib qoladi. Qoida: har doim qavs, hatto bir qator uchun ham. Buni Checkstyle `NeedBraces` qoidasi majburlaydi.

```java
// yomon: qavssiz, keyingi o'zgartirishda xato tug'ilgan
if (!order.isPaid())
    log.warn("to'lanmagan buyurtma {}", order.id());
    reject(order);              // har doim bajariladi!

// yaxshi
if (!order.isPaid()) {
    log.warn("to'lanmagan buyurtma {}", order.id());
    reject(order);
}
```

## 4.9 Yordamchi funksiyalar soni va joylashuvi

Private yordamchi funksiyalar ko'payishi muammo emas; ularning joylashuvi muammo bo'ladi. Qoida: har bir private funksiya o'zini chaqiradigan funksiyadan **keyin**, iloji boricha yaqin turadi (11.7). Shunda o'quvchi yuqoridan pastga bir yo'nalishda o'qiydi.

Ikkinchi qoida: agar private funksiyalar guruhi o'z holicha mantiqiy butunlik hosil qilsa va sinfning asosiy vazifasiga tegishli bo'lmasa, ular alohida sinfga chiqishi kerak. Sinfda 15 ta private metod bo'lsa, ehtimol ichida yashiringan sinf bor.

## 4.10 Funksiyani birinchi urinishda toza yozish mumkin emas

Toza funksiya birdan yozilmaydi va bunga urinish vaqtni yo'qotadi. Ishlaydigan tartib: oldin ishlaydigan, chuqur va chirkin versiyani yozish; testlar bilan qotirish; keyin nomlarni aniqlashtirish, ajratish, tartiblash. Testlar bo'lmasa, bu tozalash xavfli bo'ladi.

Shu tartib TDD da tabiiy chiqadi ([31-bob](31-tdd-intizomi-va-kod-dizayniga-tasiri.md)): yashil holatda refaktoring bepul, chunki har qadamdan keyin test tasdiqlaydi.

## 4.11 Amalda qo'llash

- [ ] Kod bazasidagi eng uzun 20 ta metodni topib (`awk` yoki IDE metrikasi), har birida 4.3 dagi "bo'lim izohi" signalini qidiring.
- [ ] Har bir topilgan bo'limni alohida private metodga chiqarib, izohni metod nomiga aylantiring.
- [ ] Sinflarda metodlar tartibini pastga tushish qoidasiga keltiring: chaqiruvchi yuqorida, chaqiriladigan pastda.
- [ ] `if`/`for`/`while` bloklarida qavs yo'q joylarni Checkstyle `NeedBraces` bilan taqiqlang va mavjudlarini tuzating.
- [ ] Nomida `And`, `Or`, `Then` bor metodlarni grep qilib, ularni ikki metodga bo'ling.
- [ ] 15 dan ko'p private metodi bor sinflarni ro'yxatlab, ichida yashiringan sinfni ajratish variantini ko'rib chiqing.
- [ ] Bir funksiya ichida SQL, HTTP va biznes qoidasi birga turgan joylarni topib, darajalarni ajratib bering.
- [ ] Yangi kod uchun "bir funksiya bir ekranga sig'adi" qoidasini review checklistiga kiritib, istisnolarni izohlashni talab qiling.

---

[&larr; 3. Nom turlari bo'yicha aniq konvensiyalar](03-nom-turlari-boyicha-aniq-konvensiyalar.md) · [Mundarija](README.md) · [5. Funksiya argumentlari &rarr;](05-funksiya-argumentlari.md)
