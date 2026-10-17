<!-- doc: clean-code | chapter: 7 | part: II. Funksiya va boshqaruv oqimi -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: tekshirilmoqda. Da'volar hali manbaga solishtirilmoqda.

# 7. Sikl, iteratsiya va to'plam bilan ishlash (Loops and Iteration)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

- [7.1 Sikl tanasini chiqarish va sikl o'zgaruvchisi nomi](#71-sikl-tanasini-chiqarish-va-sikl-ozgaruvchisi-nomi)
- [7.2 Indeksli sikl, `for-each` va iterator tanlovi](#72-indeksli-sikl-for-each-va-iterator-tanlovi)
- [7.3 Bitta siklda bir necha ish: siklni bo'lish](#73-bitta-siklda-bir-necha-ish-siklni-bolish)
- [7.4 `break`, `continue`, label va ulardan chiqish](#74-break-continue-label-va-ulardan-chiqish)
- [7.5 Birdan ko'p shartli siklni qayta yozish](#75-birdan-kop-shartli-siklni-qayta-yozish)
- [7.6 Iteratsiya vaqtida to'plamni o'zgartirish](#76-iteratsiya-vaqtida-toplamni-ozgartirish)
- [7.7 Sikldan quvurga o'tish mezoni](#77-sikldan-quvurga-otish-mezoni)
- [7.8 Off-by-one va chegarani hujjatlashtirish](#78-off-by-one-va-chegarani-hujjatlashtirish)
- [7.9 Katta siklda resurs va xotira xatti-harakati](#79-katta-siklda-resurs-va-xotira-xatti-harakati)
- [7.10 Rekursiya: tugashini kafolatlash, stek va sikl bilan almashtirish](#710-rekursiya-tugashini-kafolatlash-stek-va-sikl-bilan-almashtirish)
- [7.11 Amalda qo'llash](#711-amalda-qollash)

</details>


Sikl o'qish narxi jihatidan shartdan qimmat, chunki o'quvchi nafaqat tanani, balki holatning vaqt bo'yicha o'zgarishini ham ushlab turishi kerak. Bu bobda siklni o'qiladigan ushlashning aniq qoidalari: tana uzunligi, o'zgaruvchi nomi, chiqish nuqtalari, siklni bo'lish va quvurga o'tish mezoni.

## 7.1 Sikl tanasini chiqarish va sikl o'zgaruvchisi nomi

Sikl tanasi uch qatordan oshsa, uni metodga chiqarish kerak. Shundan keyin sikl bir qarashda o'qiladi: "har bir element uchun shuni qil". Sikl o'zgaruvchisi nomi esa elementning rolini aytishi kerak, `item` yoki `e` emas.

```java
// yomon: tana uzun, nom ma'nosiz
for (Object[] e : rows) {
    if (e[3] != null) {
        BigDecimal amt = (BigDecimal) e[2];
        if (amt.compareTo(BigDecimal.ZERO) > 0) {
            total = total.add(amt);
            count++;
        }
    }
}

// yaxshi: tana bitta chaqiruv, nom rolni aytadi
for (SettlementRow settlement : settlements) {
    accumulate(settlement);
}
```

Murakkab siklni birinchi urinishda to'g'ri yozishning oddiy texnikasi bor: **ichdan tashqariga** qurish. Avval bitta aniq holat uchun kod yoziladi, indekslar o'rniga literal qiymat bilan; keyin shu kod ichkariga suriladi va atrofiga sikl o'raladi, literal esa sikl o'zgaruvchisi bilan almashtiriladi; kerak bo'lsa yana bitta sikl o'raladi va yana bitta literal almashtiriladi; oxirida ishga tushirishlar qo'shiladi (McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 16.3 (385-bet)). Foydasi psixologik: har qadamda bitta narsa o'ylanadi va ko'rsatkichni, chegarani va tanani bir vaqtda boshda ushlab turish kerak bo'lmaydi.

```java
// 1-qadam: bitta aniq holat, literal bilan
Money premium = rateTable.rateFor(42, Gender.FEMALE);
Money total = premium;

// 2-qadam: atrofiga sikl, literal sikl o'zgaruvchisidan keladi
Money total = Money.ZERO;
for (Person person : group) {
    Money premium = rateTable.rateFor(person.age(), person.gender());
    total = total.plus(premium);
}
```

Qadamlarni qat'iy ketma-ketlikda bajarish shart emas; muhimi aniq holatdan boshlash va umumlashtirishni kichik, tekshirib boriladigan qadamlarga bo'lish. Sikl tayyor bo'lgandan keyin tanasi uch qatordan uzun bo'lib chiqsa, yuqoridagi qoida bo'yicha u metodga chiqadi.

## 7.2 Indeksli sikl, `for-each` va iterator tanlovi

Tanlov qoidasi oddiy: indeks kerak bo'lmasa, `for-each`. Indeksli `for` faqat indeksning o'zi ma'noga ega bo'lganda yoki massiv bilan ishlaganda haqli. `Iterator` ni oshkor ishlatish faqat iteratsiya vaqtida o'chirish kerak bo'lganda qoladi (7.6).

| Holat | To'g'ri tanlov |
|---|---|
| Elementlar ustida o'tish | `for (X x : xs)` |
| Indeks ma'noga ega (qator raqami) | `for (int i = 0; ...)` |
| Ikki to'plamni parallel o'tish | indeksli `for` yoki `zip` yordamchisi |
| Iteratsiya vaqtida o'chirish | `Iterator.remove()` yoki `removeIf` |
| Transformatsiya va filtr | `stream()` (7.7) |
| Cheksiz yoki shartli | `while` |
| Kamida bir marta bajarish | `do/while` (kamdan-kam) |

## 7.3 Bitta siklda bir necha ish: siklni bo'lish

Bir sikl ichida ikki mustaqil hisob qilinsa, u ikki siklga bo'linishi kerak (Split Loop, [35-bob](35-refaktoring-harakatlari-katalogi-i-funksiya.md)). "Tezlik uchun bitta siklda qilaman" argumenti deyarli har doim o'lchanmagan: ikki marta o'tish narxi minglab element uchun sezilmaydi, o'qish foydasi esa darhol keladi.

```java
// yomon: bir siklda ikki mustaqil hisob
Money total = Money.ZERO;
LocalDate earliest = null;
for (Order order : orders) {
    total = total.add(order.total());
    if (earliest == null || order.createdAt().isBefore(earliest)) {
        earliest = order.createdAt();
    }
}

// yaxshi: har bir hisob o'z nomi bilan, mustaqil testlanadi
Money total = totalOf(orders);
LocalDate earliest = earliestCreatedAt(orders);
```

Bo'lgandan keyin har bir sikl ko'pincha quvurga aylanadi va yo'qoladi (7.7).

## 7.4 `break`, `continue`, label va ulardan chiqish

`continue` guard clause ning sikl ichidagi shakli va u foydali: yaroqsiz elementni o'tkazib yuboradi, keyingi tana esa chuqurlikka tushmaydi. `break` esa qidiruvni to'xtatish uchun to'g'ri. Label bilan `break` (`break outer;`) deyarli har doim ichki siklni metodga chiqarish zarurligini bildiradi.

```java
// yomon: labelli break - ichma-ich sikl metodga chiqishi kerak
outer:
for (Warehouse warehouse : warehouses) {
    for (Stock stock : warehouse.stocks()) {
        if (stock.sku().equals(sku)) { found = stock; break outer; }
    }
}

// yaxshi: ichki qidiruv alohida metodda, chiqish return bilan
Optional<Stock> found = findStock(warehouses, sku);

private Optional<Stock> findStock(List<Warehouse> warehouses, Sku sku) {
    for (Warehouse warehouse : warehouses) {
        for (Stock stock : warehouse.stocks()) {
            if (stock.sku().equals(sku)) return Optional.of(stock);
        }
    }
    return Optional.empty();
}
```

## 7.5 Birdan ko'p shartli siklni qayta yozish

`while (a && b && !c)` shaklidagi sikl sharti o'quvchidan uch holatni bir vaqtda ushlashni talab qiladi. Yechim: shartni nomlash (6.1) yoki siklni ikki bosqichga bo'lish.

```java
// yomon
while (retries < MAX && !succeeded && clock.instant().isBefore(deadline)) { ... }

// yaxshi: shart nomlangan
while (shouldRetry(retries, succeeded, deadline)) { ... }

// yaxshi (ko'p holatda): qayta urinish siyosati alohida obyektda
retryPolicy.execute(() -> gateway.settle(payment));
```

## 7.6 Iteratsiya vaqtida to'plamni o'zgartirish

`for-each` ichida to'plamdan element o'chirish `ConcurrentModificationException` beradi va bu xato ko'pincha faqat ma'lum ma'lumotda chiqadi. Uchta to'g'ri yo'l bor: `removeIf`, `Iterator.remove()`, yoki yangi to'plam yig'ish.

```java
// yomon: ConcurrentModificationException
for (Order order : orders) {
    if (order.isExpired()) orders.remove(order);
}

// yaxshi: maqsad aniq, bir qator
orders.removeIf(Order::isExpired);

// yaxshi: manbani o'zgartirmaslik kerak bo'lsa
List<Order> active = orders.stream().filter(not(Order::isExpired)).toList();
```

Xuddi shu qoida `Map` ga tegishli: iteratsiya vaqtida `put` qilish taqiqlangan; `entrySet().removeIf` yoki `compute*` metodlari ishlatiladi (23.2).

## 7.7 Sikldan quvurga o'tish mezoni

Oqim va sikl tanlovi [arxitektor hujjatidagi](../architect/README.md) Stream API bo'limida ko'rib chiqilgan. Bu yerda amaliy mezon: quvur (`stream`) **transformatsiya va filtr** zanjirida o'qiladi; sikl esa **holat yig'ish, erta chiqish va yon ta'sir** da o'qiladi.

| Vazifa | O'qiladigan shakl |
|---|---|
| Filtr + mapping + yig'ish | `stream()` |
| Erta chiqish bilan qidiruv | `stream().filter().findFirst()` yoki sikl |
| Indeksga bog'liq hisob | sikl |
| Tashqi holatni o'zgartirish | sikl (oqimda yon ta'sir - 24.4) |
| Istisno tashlashi mumkin bo'lgan amal | sikl (24.7) |
| Ikki to'plamni birga o'tish | sikl |
| Guruhlash va agregatsiya | `Collectors.groupingBy` |
| Cheksiz ketma-ketlik | `Stream.iterate` |

## 7.8 Off-by-one va chegarani hujjatlashtirish

Off-by-one xatolarining asosiy sababi - chegaraning inklyuzivligi hech qayerda yozilmagani. Yechim ikki qatlamli: nomda yozish (`fromInclusive`, `toExclusive`) va turga olish (6.7 dagi `DateRange`).

```java
// yomon: oxirgi element kiradimi - kodni o'qib chiqarish kerak
List<Order> page(int offset, int limit);

// yaxshi: nom va tur chegarani aytadi
List<Order> page(Pageable pageable);                 // Spring konvensiyasi
List<Order> inRange(LocalDate fromInclusive, LocalDate toExclusive);
```

Test tomonida qoida: har bir chegara uchun uchta holat yozish - chegaradan oldin, chegarada, chegaradan keyin.

## 7.9 Katta siklda resurs va xotira xatti-harakati

Toza kod katta hajmda ham toza qolishi kerak. Uch qoida bor va ularning hammasi o'qilishini buzmaydi. Birinchi, siklda butun natijani xotiraga yig'maslik: `Stream` yoki kursor bilan oqim sifatida ishlash. Ikkinchi, siklda resurs ochmaslik (ulanish, fayl) - resurs sikldan tashqarida ochiladi. Uchinchi, siklda bitta-bitta so'rov yuborish o'rniga paket (batch) ishlatish; bu N+1 ning umumiy shakli ([patternlar hujjatidagi](../patterns/README.md) N+1 so'rovlar anti-patterni).

```java
// yomon: siklda bitta-bitta so'rov va ulanish
for (OrderId id : ids) {
    try (Connection c = dataSource.getConnection()) {      // har iteratsiyada yangi ulanish
        orderRepository.markShipped(c, id);
    }
}

// yaxshi: bitta tranzaksiya, paketli yangilash
orderRepository.markShipped(ids);     // ichida: update ... where id = any(?)
```

## 7.10 Rekursiya: tugashini kafolatlash, stek va sikl bilan almashtirish

Rekursiya masalaning kichik bir qismini o'zi hal qiladi, qolganini maydalab, har bo'lagi uchun o'zini chaqiradi. U kam hollarda kerak bo'ladi, lekin o'rinli ishlatilganda yechim chindan ham chiroyli chiqadi: daraxt bo'ylab yurish, ichma-ich JSON ni yoyish, katalog daraxtini aylanib chiqish, [Kompozit](../patterns/02-strukturaviy-patternlar.md#23-kompozit-composite) tuzilmasini hisoblash (McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 17.2 (393-bet)). Shu bilan birga rekursiya siklning "chiroyliroq" varianti emas: oddiy takrorlanishni rekursiya bilan yozish sekinroq ishlaydi, xotira sarfini oldindan aytib bo'lmaydigan qiladi va o'qilishini yomonlashtiradi. Faktorial va Fibonachchi shunga klassik misol: ikkisi ham siklda yoziladi.

Rekursiv metodga to'rt talab qo'yiladi (McConnell, 17.2 (396-397-bet)):

- **Tugashi kafolatlangan bo'lsin.** Metodda rekursiv bo'lmagan yo'l, ya'ni chaqiruvni to'xtatadigan shart bo'lishi shart. Bu shart kirish ma'lumotining har qanday shaklida ishga tushishi tekshiriladi, faqat "normal" ma'lumotda emas.
- **To'xtatish sharti yo'q joyda xavfsizlik hisoblagichi bo'lsin.** Oddiy to'xtash shartini yozish mumkin bo'lmasa (masalan tuzilma halqa bo'lib chiqishi mumkin bo'lsa), chuqurlik hisoblagichi parametr yoki maydon sifatida uzatiladi va chegaradan oshganda metod to'xtaydi. Hisoblagich har chaqiruvda qaytadan yaratilmasligi kerak, aks holda u hech narsani sanamaydi.
- **Rekursiya bitta metod ichida qolsin.** `A` `B` ni, `B` `C` ni, `C` esa yana `A` ni chaqiradigan halqali rekursiyani kod o'qib aniqlash deyarli imkonsiz. Bitta metod ichidagi rekursiyani boshda ushlab turishning o'zi qiyin.
- **Stekni ko'zdan qochirmang.** Rekursiya qancha stek yeyishini oldindan aytib bo'lmaydi. Ikki natija bundan chiqadi: xavfsizlik chegarasi stek sig'imidan kelib chiqib tanlanadi, va rekursiv metod ichida og'ir obyektlarni lokal o'zgaruvchiga yig'ib ketmaslik kerak.

Java da bu talablarning oxirgisi eng qattiq, chunki JVM da tail call optimizatsiyasi kafolatlanmagan: chuqurlik `-Xss` bilan belgilangan stek hajmiga urilganda `StackOverflowError` keladi va u `Error`, ya'ni tutib davom etiladigan narsa emas ([`Throwable`, `Error` va `OutOfMemoryError` siyosati](19-istisno-mexanikasi-va-resurslar.md#196-throwable-error-va-outofmemoryerror-siyosati)). Shuning uchun chuqurligi tashqi ma'lumotdan kelgan joyda (foydalanuvchi yuborgan JSON, tashqi katalog daraxti) rekursiya o'rniga o'z stekida yuradigan sikl yoziladi: rekursiya bilan qilinadigan har qanday ishni stek va sikl bilan ham qilish mumkin.

```java
// yomon: chuqurlik tashqi ma'lumotdan keladi, to'xtash chegarasi yo'q
long countNodes(Node node) {
    long count = 1;
    for (Node child : node.children()) {
        count += countNodes(child);
    }
    return count;
}

// yaxshi: o'z steki bilan sikl - stek chuqurligi JVM ga bog'liq emas
long countNodes(Node root) {
    Deque<Node> pending = new ArrayDeque<>();
    pending.push(root);
    long count = 0;
    while (!pending.isEmpty()) {
        Node node = pending.pop();
        count++;
        node.children().forEach(pending::push);
    }
    return count;
}
```

Chuqurligi kod bilan chegaralangan joyda (ikki-uch darajali domen tuzilmasi) rekursiya o'qilishi uchun afzal qoladi. Qaror mezoni shunday: chuqurlikni kim belgilaydi. Kod belgilasa rekursiya mumkin, tashqi ma'lumot belgilasa sikl.

## 7.11 Amalda qo'llash

- [ ] Tanasi uch qatordan uzun bo'lgan sikllarni topib, tanani nomlangan metodga chiqaring.
- [ ] Sikl o'zgaruvchilari nomlarini (`e`, `o`, `item`) elementning roliga qarab qayta nomlang.
- [ ] Bir siklda bir necha mustaqil hisob qilinadigan joylarni ikki siklga yoki quvurga bo'ling.
- [ ] `break <label>` ishlatilgan joylarni ichki siklni metodga chiqarib yo'qoting.
- [ ] `for-each` ichida `remove`/`put` chaqirilgan joylarni `removeIf` yoki `Iterator` ga o'tkazing.
- [ ] Chegara parametrlari nomiga inklyuzivlikni yozing yoki oraliqni `record` ga oling.
- [ ] Siklda ulanish ochadigan yoki so'rov yuboradigan joylarni paketli amalga aylantiring.
- [ ] Har bir chegaraviy shart uchun uch holatli test (oldin, chegarada, keyin) yozilganini tekshiring.
- [ ] Rekursiv metodlarni sanab, har birida to'xtash sharti yoki chuqurlik chegarasi borligini tekshiring.
- [ ] Chuqurligi tashqi ma'lumotdan keladigan rekursiyalarni o'z steki bilan yurgan siklga o'tkazing.

## Manbalar

- Joshua Bloch, *Effective Java* 3rd, Item 58 - an'anaviy `for` o'rniga `for-each`
- Joshua Bloch, *Effective Java* 3rd, Item 57 - lokal o'zgaruvchi qamrovini kichik ushlash, sikl o'zgaruvchisi
- Joshua Bloch, *Effective Java* 3rd, Item 46 - oqimda yon ta'sirsiz funksiyalar
- [Java API, `ConcurrentModificationException`](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/ConcurrentModificationException.html) - iteratsiya vaqtida to'plamni o'zgartirish
- Steve McConnell, *Code Complete*, 2-nashr, 16.3 (385-bet) - siklni ichdan tashqariga qurish texnikasi
- Steve McConnell, *Code Complete*, 2-nashr, 17.2 (393, 396-398-bet) - rekursiyaning tugashi, xavfsizlik hisoblagichi, stek chuqurligi va sikl bilan almashtirish
- [Java API, `StackOverflowError`](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/StackOverflowError.html) - rekursiya juda chuqur bo'lganda tashlanadi

---

[&larr; 6. Shart, mantiq va boshqaruv oqimi](06-shart-mantiq-va-boshqaruv-oqimi.md) · [Mundarija](README.md) · [8. Izoh qoidalari: yaxshi izohlar &rarr;](08-izoh-qoidalari-yaxshi-izohlar.md)
