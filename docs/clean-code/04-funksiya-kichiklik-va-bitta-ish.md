<!-- doc: clean-code | chapter: 4 | part: II. Funksiya va boshqaruv oqimi -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 4. Funksiya: kichiklik va bitta ish (Functions: Small and Doing One Thing)

<details>
<summary>Bu bobdagi 14 bo'lim</summary>

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
- [4.11 Pseudokod yozish qoidalari: niyat darajasidagi bayon](#411-pseudokod-yozish-qoidalari-niyat-darajasidagi-bayon)
- [4.12 PPP: pseudokodni izohga, izohni kodga aylantirish](#412-ppp-pseudokodni-izohga-izohni-kodga-aylantirish)
- [4.13 Mantiqni avval sodda tilda bayon qilish](#413-mantiqni-avval-sodda-tilda-bayon-qilish)
- [4.14 Amalda qo'llash](#414-amalda-qollash)

</details>


Metod uzunligi, ichma-ich shartlar va erta qaytish [arxitektor hujjatidagi](../architect/README.md) metod uzunligi va erta qaytish bo'limida ko'rib chiqilgan. Bu bobda funksiya qoidalarining qolgan qismi: "bitta ish qiladi" ni qanday tekshirish, pastga tushish qoidasi, ajratib olish mexanikasi va funksiyani toza holatga keltirish tartibi.

## 4.1 Birinchi qoida: kichik; ikkinchi qoida: yana kichikroq

Qoidaning manbasi bu yerda tadqiqot emas, tajriba: Martin uni o'zi ham shunday beradi va "buni tadqiqotga havola bilan asoslab bo'lmaydi" deb yozadi. Lekin u bergan chegaralar aniq va ular yuqori chegara shaklida: funksiya 100 qator **bo'lmasligi** kerak, 20 qator esa deyarli hech qachon bo'lmasligi kerak. Pastki chegara yo'q: u Kent Beck ning kodida har bir funksiya ikki, uch yoki to'rt qatordan iborat bo'lganini namuna qilib keltiradi.

Uzunlik bilan birga ikkita tuzilma qoidasi yuradi va amalda ular uzunlikdan ko'ra ko'proq ish qiladi. Birinchisi: `if`, `else`, `while` ichidagi blok bir qatordan iborat bo'lsin, va u qator odatda funksiya chaqiruvi bo'ladi - shunda blok nomlangan bo'ladi. Ikkinchisi: funksiyaning indentatsiya darajasi birdan yoki ikkidan oshmasin, ya'ni funksiya ichiga ichma-ich tuzilma sig'maydi.

```java
// yomon: uch daraja indentatsiya, blok nomlanmagan
for (Order order : orders) {
    if (order.isPaid()) {
        for (OrderItem item : order.items()) {
            if (item.isBackordered()) { reserve(item); }
        }
    }
}

// yaxshi: bir daraja, har blok nomlangan funksiya chaqiruvi
for (Order order : paidOrders(orders)) {
    reserveBackorderedItems(order);
}
```

Shu hajmda funksiya nomi uning butun mazmunini qamrab oladi, test yozish oson bo'ladi va qayta ishlatish imkoniyati paydo bo'ladi.

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

Ajratishning uchinchi sababi bor va u ko'pincha e'tibordan chetda qoladi:
**takrorlanadigan kodni bir xil shaklga keltirish**. Boswell va Foucher
misolida to'rtta tekshiruv bir xil narsani qiladi, lekin har biri boshqa
uzunlikda, qatorlari ko'chib ketgan va foydali qism (`"Doug Adams"`,
`"Mr. Douglas Adams"`) `database_connection` va `error` kabi takroriy
tokenlar orasida ko'milgan. Yordamchi metod chiqarilgandan keyin to'rt chaqiruv
to'rt qatorga sig'adi va to'rtta test borligi, har birining parametrlari bilan,
bir qarashda ko'rinadi (Boswell/Foucher, *The Art of Readable Code*, 1-nashr,
O'Reilly, 2011, 4-bob (37-38-bet)).

```java
// Oldin: shakl tartibsiz, muhim qism takroriy tokenlar orasida
assertThat(expander.expandFullName(connection, "Doug Adams", errors))
        .isEqualTo("Mr. Douglas Adams");
assertThat(errors.message()).isEmpty();
assertThat(expander.expandFullName(connection, " Jake Brown ", errors))
        .isEqualTo("Mr. Jacob Brown III");
assertThat(errors.message()).isEmpty();
assertThat(expander.expandFullName(connection, "No Such Guy", errors)).isEmpty();
assertThat(errors.message()).isEqualTo("no match found");

// Keyin: shakl bir xil, har qatorda faqat o'zgaradigan qism qoldi
checkFullName("Doug Adams", "Mr. Douglas Adams", "");
checkFullName(" Jake Brown ", "Mr. Jacob Brown III", "");
checkFullName("No Such Guy", "", "no match found");
checkFullName("John", "", "more than one result");
```

Kitob bu harakatni "kodni chiroyli qilish" bo'limida beradi va natijasini oshkor
aytadi: maqsad estetik bo'lsa ham, foydasi estetik emas - takrorlanish
yo'qoladi, har holatning muhim qismi ko'zga tashlanadi va yangi holat qo'shish
arzonlashadi (shu yerda, 38-bet). Shaklni bir xillashtirish, demak, ajratishni
boshlash uchun yetarli sabab: tana uzun bo'lishi shart emas.

**Bog'liq bo'lmagan quyi masalani ajratish.** Uzunlik va izoh ehtiyoji ajratish uchun yetarli sabab, lekin eng ishonchli mezon boshqa: **qator funksiyaning maqsadiga ishlayaptimi**. Boswell va Foucher uch qadamli tartib beradi:

1. Funksiya yoki blokka qarab "bu kodning yuqori darajadagi maqsadi nima?" deb so'rang.
2. Har qator uchun "bu qator shu maqsadga bevosita ishlaydimi, yoki maqsadga erishish uchun kerak bo'lgan **bog'liq bo'lmagan quyi masalani** yechayaptimi?" deb so'rang.
3. Yetarlicha qator quyi masalaga tegishli bo'lsa, o'sha kod alohida funksiyaga chiqadi.

Ajralgan funksiyaning asosiy xususiyati - u **nima uchun chaqirilayotganini bilmaydi**: `sphericalDistance`, `makeUrlFriendly`, `urlSafeEncrypt` o'z chaqiruvchisidan butunlay mustaqil. Kitobdagi misol: eng yaqin joyni topadigan funksiya ichida sferik masofa formulasi turgan edi; formula alohida funksiyaga chiqarilgandan keyin asosiy funksiya o'z maqsadiga qaytdi va o'quvchi geometriyaga chalg'imaydigan bo'ldi.

Foydasi uch tomonli va u estetik emas: ajralgan kod **alohida testlanadi**, chegara holatlarini yaxshilash osonlashadi (chunki o'zgartirish chaqiruvchiga ta'sir qilmaydi), va u qayta ishlatiladigan bo'ladi.

```java
// Maqsad: eng yaqin joyni topish. Geometriya - bog'liq bo'lmagan quyi masala.
Location findClosest(double lat, double lng, List<Location> locations) {
    return locations.stream()
            .min(comparingDouble(l -> sphericalDistance(lat, lng, l.lat(), l.lng())))
            .orElse(null);
}

// Chaqiruvchidan bexabar, alohida testlanadi
static double sphericalDistance(double lat1, double lng1, double lat2, double lng2) {
    double phi1 = toRadians(lat1);
    double phi2 = toRadians(lat2);
    return acos(sin(phi1) * sin(phi2)
            + cos(phi1) * cos(phi2) * cos(toRadians(lng2) - toRadians(lng1)));
}
```

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

## 4.11 Pseudokod yozish qoidalari: niyat darajasidagi bayon

Metodni qurishning nomlangan tartibi bor: *Code Complete* uni "Pseudocode Programming Process" (PPP) deb ataydi. Tartibning birinchi yarmi shu bo'limda, ya'ni metodni kodda emas, tabiiy tilda loyihalash. Kitob to'rt harakatni belgilaydi va kerak bo'lsa takrorlashni aytadi: metodni loyihalash, loyihani tekshirish, kodni yozish, kodni tekshirish (9-bob, 217-bet).

Pseudokod bu algoritm yoki metod qanday ishlashini tasvirlaydigan norasmiy, tabiiy tilga yaqin yozuv. Tabiiy tilga o'xshash har qanday matn bir xil foyda bermaydi, shuning uchun kitob to'rt qoida beradi (9-bob, 218-bet):

- Aniq amalni aniq tasvirlaydigan tabiiy til gaplari yozilsin.
- Maqsad tilining sintaksisi ishlatilmasin. Bayonga `Optional`, `throw` yoki qaytish qiymati kirsa, u kod darajasiga tushadi va yuqori darajada loyihalashning butun foydasi yo'qoladi.
- Pseudokod **niyat darajasida** yozilsin: yondashuv nimani bildiradi, maqsad tilida qanday amalga oshiriladi emas.
- Lekin shu darajadan past ham bo'lsin: har qatoridan kod yozish deyarli mexanik bo'lsin. Juda yuqori daraja muammoli tafsilotni yashiradi, shuning uchun "pseudokod yozgandan ko'ra kodni yozish osonroq" deb tuyulguncha aniqlashtiriladi.

Kitobdagi yaxshi va yomon pseudokod misollari C da yozilgan; quyida shu farq Java kontekstiga o'tkazilgan. Birinchi variant allaqachon kod, demak pseudokod emas:

```java
// yomon pseudokod: Java sintaksisi va qaytish qiymati tafsiloti kirib kelgan
// repository.findById(id) ni chaqir, natija Optional bo'sh bo'lsa null qaytar
// status != PENDING bo'lsa IllegalStateException tashla
// entity.setStatus(CONFIRMED) qil, repository.save(entity) chaqir, true qaytar
```

```java
// yaxshi pseudokod: faqat niyat, maqsad tiliga bog'liqlik yo'q
// Buyurtmani raqami bo'yicha top
// Topilmasa, chaqiruvchiga buyurtma yo'qligini bildir
// Buyurtma hali kutish holatida bo'lsa, uni tasdiqlangan holatga o'tkaz
// Boshqa holatda bo'lsa, bu o'tish mumkin emasligini bildir
// Tasdiqlash natijasini qaytar
```

Ikkinchi variantni Java, Kotlin yoki boshqa tilda bajarish mumkin, birinchisi esa faqat bitta yo'lni ochiq qoldiradi. Shu uslubning foydasi kitobda sanab o'tilgan (9-bob, 219-220-bet): past darajadagi loyihani kodni ochmasdan review qilish mumkin bo'ladi; aniqlashtirish kichik qadamlar bilan boradi, shuning uchun yuqori darajadagi xato yuqori darajada ushlanadi; bir necha qator pseudokodni o'zgartirish bir bet kodni o'zgartirishdan arzon, ya'ni xato "eng arzon bosqichda" topiladi; va pseudokod keyinchalik izohga aylangani uchun izoh yozish ishi deyarli qolmaydi.

## 4.12 PPP: pseudokodni izohga, izohni kodga aylantirish

Pseudokod yozishdan oldin bajariladigan ishlar ro'yxati bor va ularning hammasi matn qoldirmaydi: ularning maqsadi yozishdan oldingi fikriy tayyorgarlik (9-bob, 220-223-bet). Metodning vazifasi umumiy dizaynga mos tushishini tekshirish; metod nimani yashirishini, kirish va chiqishini, oldingi va keyingi shartlarini aytib qo'yish; metodga nom berish; uni qanday test qilishni hozir hal qilish; standart kutubxonada tayyor yechim bormi deb qarash; xato bilan ishlash yo'lini tanlash. Nom topilmasa, bu ogohlantirish belgisi: McConnell buni "noaniq nom noaniq dizayndan chiqadi, orqaga qaytib dizaynni yaxshilang" deb yozadi.

Keyin pseudokod yoziladi, tekshiriladi va bir necha variant sinaladi. Tekshirishning eng arzon usuli boshqa odamga tushuntirish: 11 qator pseudokodni review qilishga odam 35 qator kodga qaraganda osonroq ko'nadi va pseudokodda yuqori darajadagi xato ko'rinib qoladi (9-bob, 224-bet). Shu bilan bir qatorda bir nechta variantni pseudokodda sinab ko'rish kerak, chunki kod yozilgandan keyin unga hissiy bog'lanish paydo bo'ladi va yomon dizaynni tashlash qiyinlashadi.

Kod yozish qadamlari aniq: metod e'lonini yozish, sarlavha izohini joyida qoldirish, pseudokod qatorlarini izohga aylantirish, keyin har bir izoh ostiga kod to'ldirish. Kitob kutilgan nisbatni beradi: har bir izoh odatda 2 dan 10 qatorgacha kodga aylanadi (9-bob, 228-bet).

```java
/** Buyurtmani tasdiqlaydi; buyurtma topilmasa yoki holat mos kelmasa, sababini qaytaradi. */
ConfirmResult confirm(OrderId id) {
    // Buyurtmani raqami bo'yicha top
    Order order = orders.findById(id).orElse(null);

    // Topilmasa, chaqiruvchiga buyurtma yo'qligini bildir
    if (order == null) {
        return ConfirmResult.notFound(id);
    }

    // Boshqa holatda bo'lsa, bu o'tish mumkin emasligini bildir
    if (order.status() != OrderStatus.PENDING) {
        return ConfirmResult.wrongStatus(order.status());
    }

    // Buyurtma hali kutish holatida bo'lsa, uni tasdiqlangan holatga o'tkaz
    orders.save(order.confirmed());
    return ConfirmResult.confirmed(id);
}
```

Bitta izoh ostida kod kutilganidan ko'p bo'lib ketsa, ikki yo'l bor: o'sha bo'lakni yangi metodga chiqarish (nom pseudokod qatoridan o'zi chiqadi, [funksiyadan funksiya chiqarish mexanikasi](#45-funksiyadan-funksiya-chiqarish-mexanikasi)) yoki PPP ni shu qatorga rekursiv qo'llab, uni bir necha pseudokod qatoriga yoyib yuborish. Oxirida tozalash bosqichi keladi va u izohlarga ham tegadi: PPP rekursiv qo'llangan joyda izoh ostida yaxshi nomlangan metod chaqiruvi turib qolsa, izoh ortiqcha bo'ladi va o'chiriladi ([ortiqcha izoh](09-yomon-izohlar-katalogi.md#92-ortiqcha-izoh-kodni-sozma-soz-takrorlash)).

PPP TDD ga qarshi qo'yilmaydi. McConnell ning o'zi bobning oxirida PPP ga uchta alternativani sanaydi: test-first, refactoring va design by contract (9-bob, 232-233-bet). Shu uchligining birinchisi bu korpusda [TDD intizomi](31-tdd-intizomi-va-kod-dizayniga-tasiri.md) sifatida alohida bob bo'lib yozilgan, ikkinchisi esa [funksiyani birinchi urinishda toza yozish mumkin emas](#410-funksiyani-birinchi-urinishda-toza-yozish-mumkin-emas) bo'limining mazmuni. Tanlov mavzuga qarab: metodning mantiqi chigal bo'lsa pseudokod arzon, kutilgan xulq chigal bo'lsa test arzon.

## 4.13 Mantiqni avval sodda tilda bayon qilish

*The Art of Readable Code* uchta qadamli usul beradi va uni kod yozishdan oldin qo'llashni taklif qiladi (12-bob, 131-bet): kod nima qilishi kerakligini hamkasbingizga aytganday sodda tilda bayon qilish; bayondagi kalit so'z va iboralarga diqqat qilish; keyin kodni shu bayonga moslab yozish. Usulning kuchi shundaki, bayon kodni soddalashtirish yo'lini o'zi ko'rsatib beradi.

Kitobdagi misol PHP da; quyida g'oya Java ga o'tkazilgan. Dastlabki shartda uchta inkor va ikki daraja ichma-ichlik bor:

```java
// yomon: uch inkor, ikki daraja, qoida ko'rinmaydi
boolean authorized;
if (document != null) {
    authorized = isAdmin(request) || document.ownerId().equals(session.userId());
} else {
    authorized = isAdmin(request);
}
if (!authorized) {
    return Rendered.notAuthorized();
}
```

Endi mantiq sodda tilda aytiladi: "ruxsat olishning ikki yo'li bor, admin bo'lish yoki shu hujjatning egasi bo'lish (hujjat bo'lsa); boshqa holatda ruxsat yo'q". Shu bayon kodga qaytarilsa, inkorlar yo'qoladi:

```java
// yaxshi: bayondagi ikki yo'l ikki shart bo'lib turadi
if (isAdmin(request)) {
    return Rendered.page();  // birinchi yo'l: admin
}
if (document != null && document.ownerId().equals(session.userId())) {
    return Rendered.page();  // ikkinchi yo'l: hujjat egasi
}
return Rendered.notAuthorized();
```

Usul katta metodda boshqa foyda beradi: bayonning eng chigal gapi aynan ajratib olinadigan bo'lakni ko'rsatadi. Kitobdagi uchta iteratorni moslash misolida bayonning "qatorlarning vaqtlari mos kelmasa, mos kelguncha surish" qismi `advanceToMatchingTime` nomli alohida metodga chiqariladi va asosiy metod o'qiladigan holatga keladi (12-bob, 135-136-bet). Usulni o'sha yangi metodga rekursiv qo'llaganda yana bir narsa chiqadi: bayon masalaga xos nomlarni (`stock_iter` va shu kabi) tilga olmaydi, demak metod ichidagi o'zgaruvchi nomlari ham umumiyroq va qisqaroq bo'lishi mumkin.

Bu usulning nomlangan shakli "rubber ducking": kitob bir universitet laboratoriyasining qoidasini keltiradi, unda talaba yordam so'rashdan oldin muammoni xonadagi o'yinchoq ayiqchaga tushuntirishi kerak bo'lgan, va ovoz chiqarib bayon qilishning o'zi ko'pincha yechimni ochib bergan (12-bob, 137-bet). Shu korpusda bu usulning debug tomoni [ko'r yo'lak va botqoqdan chiqish](46-vaqt-diqqat-va-mashq.md#465-kor-yolak-va-botqoqdan-chiqish) bo'limida yozilgan. Teskari xulosasi esa yozishdan oldin kerak: muammoni yoki dizaynni so'z bilan ayta olmasangiz, unda biror narsa aniqlanmagan yoki tushib qolgan.

## 4.14 Amalda qo'llash

- [ ] Kod bazasidagi eng uzun 20 ta metodni topib (`awk` yoki IDE metrikasi), har birida 4.3 dagi "bo'lim izohi" signalini qidiring.
- [ ] Har bir topilgan bo'limni alohida private metodga chiqarib, izohni metod nomiga aylantiring.
- [ ] Sinflarda metodlar tartibini pastga tushish qoidasiga keltiring: chaqiruvchi yuqorida, chaqiriladigan pastda.
- [ ] `if`/`for`/`while` bloklarida qavs yo'q joylarni Checkstyle `NeedBraces` bilan taqiqlang va mavjudlarini tuzating.
- [ ] Nomida `And`, `Or`, `Then` bor metodlarni grep qilib, ularni ikki metodga bo'ling.
- [ ] 15 dan ko'p private metodi bor sinflarni ro'yxatlab, ichida yashiringan sinfni ajratish variantini ko'rib chiqing.
- [ ] Bir funksiya ichida SQL, HTTP va biznes qoidasi birga turgan joylarni topib, darajalarni ajratib bering.
- [ ] Yangi kod uchun "bir funksiya bir ekranga sig'adi" qoidasini review checklistiga kiritib, istisnolarni izohlashni talab qiling.

## Manbalar

- Dustin Boswell, Trevor Foucher, *The Art of Readable Code*, 1-nashr, O'Reilly, 2011 (copyright 2012), 10-bob (109-111-betlar) - funksiyaning yuqori darajadagi maqsadini so'rash, har qatorni shu maqsadga ishlayotgani bo'yicha tekshirish va bog'liq bo'lmagan quyi masalani chaqiruvchidan bexabar alohida funksiyaga chiqarish; ajratilgan kodning alohida testlanishi va qayta ishlatilishi
- Robert C. Martin, *Clean Code*, 3-bob - funksiya 100 qator bo'lmasligi, 20 qator deyarli hech qachon bo'lmasligi; qoida tadqiqotga emas tajribaga tayanishi
- Robert C. Martin, *Clean Code*, 3-bob ("Blocks and Indenting") - blok bir qator bo'lishi, indentatsiya darajasi birdan yoki ikkidan oshmasligi
- Robert C. Martin, *Clean Code*, 3-bob ("Do One Thing", "One Level of Abstraction per Function") - bitta ish qilish sinovi va pastga tushish qoidasi
- Robert C. Martin, *Clean Code*, 17-bob, G30, G34 - funksiya bitta ish qilsin, bir darajadan pastga tushish
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 9-bob (217-bet) - metod qurishning to'rt harakati va ularning takrorlanishi (4.11)
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 9-bob (218-220-bet) - pseudokod yozishning to'rt qoidasi, niyat darajasi, maqsad tili sintaksisidan voz kechish va uslubning sanab o'tilgan foydalari (4.11)
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 9-bob (220-224-bet) - pseudokoddan oldingi tayyorgarlik ro'yxati, nom topilmasligi dizayn ogohlantirishi ekani, pseudokodni boshqa odamga tushuntirib tekshirish va variantlarni sinash (4.12)
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 9-bob (226-230-bet) - pseudokodni izohga aylantirish va har izoh ostiga kod to'ldirish tartibi, bir izohga 2 dan 10 qatorgacha kod, bo'lakni yangi metodga chiqarish yoki PPP ni rekursiv qo'llash (4.12)
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 9-bob (232-233-bet) - ortiqcha bo'lib qolgan pseudokod izohini o'chirish; PPP ga uch alternativa: test-first, refactoring va design by contract (4.12)
- Dustin Boswell, Trevor Foucher, *The Art of Readable Code*, 1-nashr, O'Reilly, 2011 (copyright 2012), 12-bob (131-133-bet) - mantiqni sodda tilda bayon qilib keyin kodga aylantirishning uch qadami va ruxsat tekshiruvi misolida inkorlarning yo'qolishi (4.13)
- Dustin Boswell, Trevor Foucher, *The Art of Readable Code*, 1-nashr, O'Reilly, 2011 (copyright 2012), 12-bob (135-138-bet) - bayonning chigal gapi ajratiladigan bo'limni ko'rsatishi, usulni rekursiv qo'llaganda nomlarning umumiylashishi, "rubber ducking" va so'z bilan aytilmagan dizayn tugallanmagani (4.13)
- Dustin Boswell, Trevor Foucher, *The Art of Readable Code*, 1-nashr, O'Reilly, 2011 (copyright 2012), 4-bob (37-38-bet) - `CheckFullName` misolida tartibsiz takrorlanadigan kodni yordamchi metod bilan bir xil shaklga keltirish va uning uch foydasi (takrorlanish yo'qolishi, muhim qismning ko'rinishi, yangi holat qo'shish arzonligi)

---

[&larr; 3. Nom turlari bo'yicha aniq konvensiyalar](03-nom-turlari-boyicha-aniq-konvensiyalar.md) · [Mundarija](README.md) · [5. Funksiya argumentlari &rarr;](05-funksiya-argumentlari.md)
