<!-- doc: clean-code | chapter: 7 | part: II. Funksiya va boshqaruv oqimi -->

[Toza kod yozuvchining qoidalari](../../README.md) / [Toza kod qoidalari](README.md)

# 7. Sikl, iteratsiya va to'plam bilan ishlash (Loops and Iteration)

<details>
<summary>Bu bobdagi 10 bo'lim</summary>

- [7.1 Sikl tanasini chiqarish va sikl o'zgaruvchisi nomi](#71-sikl-tanasini-chiqarish-va-sikl-ozgaruvchisi-nomi)
- [7.2 Indeksli sikl, `for-each` va iterator tanlovi](#72-indeksli-sikl-for-each-va-iterator-tanlovi)
- [7.3 Bitta siklda bir necha ish: siklni bo'lish](#73-bitta-siklda-bir-necha-ish-siklni-bolish)
- [7.4 `break`, `continue`, label va ulardan chiqish](#74-break-continue-label-va-ulardan-chiqish)
- [7.5 Birdan ko'p shartli siklni qayta yozish](#75-birdan-kop-shartli-siklni-qayta-yozish)
- [7.6 Iteratsiya vaqtida to'plamni o'zgartirish](#76-iteratsiya-vaqtida-toplamni-ozgartirish)
- [7.7 Sikldan quvurga o'tish mezoni](#77-sikldan-quvurga-otish-mezoni)
- [7.8 Off-by-one va chegarani hujjatlashtirish](#78-off-by-one-va-chegarani-hujjatlashtirish)
- [7.9 Katta siklda resurs va xotira xatti-harakati](#79-katta-siklda-resurs-va-xotira-xatti-harakati)
- [7.10 Amalda qo'llash](#710-amalda-qollash)

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

## 7.10 Amalda qo'llash

- [ ] Tanasi uch qatordan uzun bo'lgan sikllarni topib, tanani nomlangan metodga chiqaring.
- [ ] Sikl o'zgaruvchilari nomlarini (`e`, `o`, `item`) elementning roliga qarab qayta nomlang.
- [ ] Bir siklda bir necha mustaqil hisob qilinadigan joylarni ikki siklga yoki quvurga bo'ling.
- [ ] `break <label>` ishlatilgan joylarni ichki siklni metodga chiqarib yo'qoting.
- [ ] `for-each` ichida `remove`/`put` chaqirilgan joylarni `removeIf` yoki `Iterator` ga o'tkazing.
- [ ] Chegara parametrlari nomiga inklyuzivlikni yozing yoki oraliqni `record` ga oling.
- [ ] Siklda ulanish ochadigan yoki so'rov yuboradigan joylarni paketli amalga aylantiring.
- [ ] Har bir chegaraviy shart uchun uch holatli test (oldin, chegarada, keyin) yozilganini tekshiring.

---

[&larr; 6. Shart, mantiq va boshqaruv oqimi](06-shart-mantiq-va-boshqaruv-oqimi.md) · [Mundarija](README.md) · [8. Izoh qoidalari: yaxshi izohlar &rarr;](08-izoh-qoidalari-yaxshi-izohlar.md)
