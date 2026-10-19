<!-- doc: clean-code | chapter: 7 | part: II. Funksiya va boshqaruv oqimi -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 7. Sikl, iteratsiya va to'plam bilan ishlash (Loops and Iteration)

<details>
<summary>Bu bobdagi 12 bo'lim</summary>

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
- [7.11 Shartni sikl boshiga chiqarish: `do/while` va nazorat flagi](#711-shartni-sikl-boshiga-chiqarish-dowhile-va-nazorat-flagi)
- [7.12 Amalda qo'llash](#712-amalda-qollash)

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

Indeks nomi uchun alohida qoida bor va u ichma-ich siklda ishlaydi. `i`, `j`, `k` tushunarli, lekin uch sikl ichma-ich kelganda qaysi indeks qaysi massivga tegishli ekani ko'rinmaydi va `clubs[i].members[k] == users[j]` kabi qator alohida qaraganda to'g'ri ko'rinadi, aslida ikki indeks almashib ketgan. Boswell va Foucher yechimi: indeks nomini kolleksiya nomining bosh harfiga bog'lash (`ci`, `mi`, `ui`), shunda xato ko'zga tashlanadi, chunki indeksning bosh harfi massivning bosh harfiga mos kelmay qoladi (Boswell/Foucher, *The Art of Readable Code*, 1-nashr, O'Reilly, 2011, 2-bob (12-bet)).

```java
// yomon: xato alohida qatorda to'g'ri ko'rinadi
for (int i = 0; i < clubs.size(); i++) {
    for (int j = 0; j < clubs.get(i).members().size(); j++) {
        for (int k = 0; k < users.size(); k++) {
            if (clubs.get(i).members().get(k).equals(users.get(j))) { ... }
        }
    }
}

// yaxshi: bosh harf mos kelmasligi xatoni ko'rsatadi
for (int ci = 0; ci < clubs.size(); ci++) {
    for (int mi = 0; mi < clubs.get(ci).members().size(); mi++) {
        for (int ui = 0; ui < users.size(); ui++) {
            if (clubs.get(ci).members().get(mi).equals(users.get(ui))) { ... }
        }
    }
}
```

Java da bu holatning arzonroq yechimi ham bor: uch darajali indeksli sikl o'rniga `for-each` va ichki siklni metodga chiqarish indeksni butunlay yo'qotadi. Indeks nomlash qoidasi indeksning o'zi kerak bo'lgan joyda qoladi.

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

Oshkor `Iterator` ichma-ich siklda ishlatilsa, klassik xato chiqadi: tashqi to'plam iteratorining `next()` i ichki sikl ichida chaqiriladi. Natijada tashqi iterator ichki sikl tezligida suriladi va element tugaganda `NoSuchElementException` chiqadi; to'plam o'lchamlari karrali bo'lsa istisno ham chiqmaydi va natija jim noto'g'ri bo'ladi. Shuning uchun ichma-ich o'tishda jadvalning birinchi qatori ayniqsa muhim: ichma-ich `for-each` da har bir sikl o'z iteratorini oladi va xato umuman yuzaga kelmaydi.

```java
// yomon: tashqi iteratorning next() i ichki siklda chaqiriladi
for (Iterator<Suit> i = suits.iterator(); i.hasNext(); ) {
    for (Iterator<Rank> j = ranks.iterator(); j.hasNext(); ) {
        deck.add(new Card(i.next(), j.next()));     // i.next() har kartada suriladi
    }
}

// yaxshi: har bir sikl o'z elementini oladi
for (Suit suit : suits) {
    for (Rank rank : ranks) {
        deck.add(new Card(suit, rank));
    }
}
```

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

`Inclusive` va `Exclusive` qo'shimchasi aniq, lekin uzun. Boswell va Foucher qisqa muqobilni beradi va u **idioma** bo'lgani uchun ishlaydi:

- **Ikki uchi ham kiradigan (inklyuziv) oraliq uchun `first` va `last`.** `integerRange(start, stop)` da `stop` noaniq (`[2,3]` mi, `[2,3,4]` mi), `last` esa aniq inklyuziv: `printKeys(first, last)`. Shu holatda `min`/`max` juftligi ham ishlaydi, agar kontekstda tabiiy eshitilsa.
- **Oxiri kirmaydigan (yarim ochiq) oraliq uchun `begin` va `end`.** Programmalashda bu eng keng qabul qilingan konvensiya, shuning uchun `end` ning o'zi bir oz noaniq bo'lsa ham (tabiiy tilda "kitobning oxirida" inklyuziv) idioma uni hal qiladi. Yarim ochiq oraliq amalda qulayroq: 16-oktyabrdagi hodisalarni `("OCT 16 00:00", "OCT 17 00:00")` deb yozish `("OCT 16 00:00", "OCT 16 23:59:59.9999")` dan tozaroq.

| Oraliq turi | Nom juftligi | Java da |
|---|---|---|
| `[a, b]` ikki uchi kiradi | `first` / `last` | `firstDay`, `lastDay` |
| `[a, b)` oxiri kirmaydi | `begin` / `end` | `beginDate`, `endDate` |
| Chegara qiymati kiradi | `min` / `max` | `maxItemsInCart` |

ESLATMA: Java ning o'z API si yarim ochiq oraliqni ishlatadi (`List.subList(int fromIndex, int toIndex)`, `String.substring`), shuning uchun `begin`/`end` shakli ekotizim bilan izchil; `fromInclusive`/`toExclusive` esa `NavigableMap.subMap` imzosidan kelgan va u ham birlamchi manba. Ikkisini bitta kod bazasida aralashtirmang.

Chegara nomidan tashqari sikl **shartining** ikki tuzog'i bor va ikkisi ham off-by-one ning qo'shnisi. Birinchi: sikl boshqaruvchi o'zgaruvchisi sifatida suzuvchi nuqtali qiymat ishlatilmaydi. `double` va `float` qiymatlar aniq saqlanmaydi, shuning uchun `rate != 1.0` sharti kutilgan iteratsiyada rost bo'lmasligi mumkin va sikl cheksiz aylanadi; sanagich butun son bo'ladi, kasr qiymat esa sikl ichida butun sanagichdan hisoblanadi (20.1). Ikkinchi: qadami 1 dan katta bo'lgan siklning shartida tenglik emas, munosabat operatori (`<`, `<=`) yoziladi. Qadam chegaraga aniq tushmasa, tenglik sharti ustidan sakrab o'tib ketadi va sikl yana to'xtamaydi.

```java
// yomon: suzuvchi sanagich va tenglik sharti
for (double rate = 0.1; rate != 1.0; rate += 0.1) { ... }
for (int i = 1; i != 10; i += 2) { ... }       // 1, 3, 5, 7, 9, 11 ... to'xtamaydi

// yaxshi: butun sanagich, munosabat operatori, kasr qiymat hisoblanadi
for (int step = 1; step <= 10; step++) {
    double rate = step / 10.0;
}
for (int i = 1; i < 10; i += 2) { ... }
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

To'rtinchi qoida sikl tanasiga tegishli: natijasi iteratsiyadan iteratsiyaga o'zgarmaydigan hisob sikl ichidan sikl oldiga chiqariladi va nom oladi. Birinchi foyda o'qilishda: sikl tanasida faqat haqiqatan o'zgaradigan narsa qoladi, shuning uchun o'quvchi nima iteratsiyaga bog'liqligini bir qarashda ko'radi. Ikkinchi foyda ishda: hisob metod chaqiruvi bo'lsa, uni sikl ichida qoldirish har iteratsiyada qayta bajarilishini bildiradi. Bu [sikl o'zgaruvchisi va cheksiz sikl xavfi](../sonarqube/25-xato-katalogi-reliability-bug-toifasi.md#2515-sikl-ozgaruvchisini-ichkarida-ozgartirish-yoki-cheksiz-sikl-xavfi) qoidasining tana tomonidagi juftligi: u sikl **shartining** qayta hisoblanishini qamraydi, bu yerdagi qoida sikl **tanasini**.

```java
// yomon: chegara har iteratsiyada qaytadan hisoblanadi
for (Order order : orders) {
    if (order.total().compareTo(policy.limitFor(customer)) > 0) {
        flagged.add(order);
    }
}

// yaxshi: o'zgarmas qiymat sikl oldida nomlanadi
Money limit = policy.limitFor(customer);
for (Order order : orders) {
    if (order.total().compareTo(limit) > 0) {
        flagged.add(order);
    }
}
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

## 7.11 Shartni sikl boshiga chiqarish: `do/while` va nazorat flagi

Siklni bir qarashda o'qish uchun uning to'xtash sharti ko'z tushadigan joyda, ya'ni tanadan yuqorida turishi kerak. Ikki keng tarqalgan shakl buni buzadi: `do/while` shartni tanadan pastga tushiradi, nazorat flagi esa shartni tanaga sochib tashlaydi.

**`do/while` dan `while` ga yoki erta qaytishga o'tish.** `if`, `while` va `for` da shart himoyalayotgan koddan yuqorida turadi, `do/while` da esa pastda; kod yuqoridan pastga o'qilgani uchun bu tabiiy emas va ko'p o'quvchi blokni ikki marta o'qiydi. Boswell va Foucher amalda ko'rilgan `do/while` sikllarining ko'pchiligi boshidan `while` bo'lib yozilishi mumkin ekanini aytadi; shuningdek `do/while` ichidagi `continue` chalkash, chunki `do { continue; } while (false)` bir marta aylanadimi yoki cheksizmi degan savol ko'pchilikni to'xtatib o'ylantiradi (javobi: bir marta). Shu yerda kitob Stroustrup ni keltiradi: u `do` ni xato va chalkashlik manbai deb hisoblaydi va shartni "oldinda, ko'rinadigan joyda" ko'rishni afzal ko'radi (Boswell/Foucher, *The Art of Readable Code*, 1-nashr, O'Reilly, 2011, 7-bob (74-75-bet)).

```java
// yomon: shart pastda, bundan tashqari node == null bo'lsa NPE
public boolean containsNode(Node node, String name, int maxLength) {
    do {
        if (node.name().equals(name)) {
            return true;
        }
        node = node.next();
    } while (node != null && --maxLength > 0);
    return false;
}

// yaxshi: shart yuqorida, maxLength == 0 va node == null holatlari o'zi ishlaydi
public boolean containsNode(Node node, String name, int maxLength) {
    while (node != null && maxLength-- > 0) {
        if (node.name().equals(name)) {
            return true;
        }
        node = node.next();
    }
    return false;
}
```

Kitob `do/while` ni takrorlangan tana bilan (tanani sikl oldidan bir marta yozib, keyin `while` ga kirish) almashtirishni oshkor taqiqlaydi: bu `do/while` dan ham yomon, chunki kod ikkilanadi (shu yerda, 75-bet). Qoidaning joyi [indeksli sikl, `for-each` va iterator tanlovi](#72-indeksli-sikl-for-each-va-iterator-tanlovi) jadvalidagi "kamida bir marta bajarish" qatorini aniqlashtiradi: `do/while` shu holatda ham oxirgi variant, birinchisi emas.

**Nazorat flagini `break` yoki `return` bilan yo'qotish.** `boolean done = false` turidagi o'zgaruvchining birgina vazifasi bajarilish yo'nalishini boshqarish: u programmaning ma'lumotini saqlamaydi. Bunday o'zgaruvchi "sikl o'rtasidan chiqmaslik kerak" degan aytilmagan qoidadan tug'iladi; bunday qoida yo'q va flagni olib tashlash sharti shundan: `break` yoki `continue` bilan almashtirish, ichma-ich sikl bo'lsa esa siklni yoki tanasini metodga chiqarib `return` ishlatish (shu yerda, 9-bob (96-bet)).

```java
// yomon: done flagi tanaga sochilgan, shart ikki joyda
boolean done = false;
while (iterator.hasNext() && !done) {
    SettlementRow row = iterator.next();
    if (row.isRejected()) {
        audit.record(row);
        done = true;
        continue;
    }
    process(row);
}

// yaxshi: flag yo'q, to'xtash nuqtasi ko'rinadi
while (iterator.hasNext()) {
    SettlementRow row = iterator.next();
    if (row.isRejected()) {
        audit.record(row);
        break;
    }
    process(row);
}
```

Bu Fowler ning [Remove Control Flag](37-refaktoring-harakatlari-katalogi-iii-shart.md#3718-nazorat-flagini-olib-tashlash-remove-control-flag) refaktoringi bilan aynan bir xil qoida: ikki manba bir xil sababni (bitta chiqish nuqtasi talabi) va bir xil yechimni (`break`, `continue`, ajratish va `return`) beradi. Mexanika, flag ayni paytda natija qiymatini ham tashiydigan holat va `try/finally` bilan tozalash varianti shu katalog yozuvida.

## 7.12 Amalda qo'llash

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
- [ ] `do/while` ishlatilgan joylarni sanab, har birini `while` yoki erta qaytishga o'tkazib ko'ring; tana haqiqatan kamida bir marta kerak bo'lgan holatni izohda yozib qoldiring.
- [ ] Sikl ichidagi `done`, `found`, `finished` nomli `boolean` o'zgaruvchilarni topib, `break`/`return` bilan yo'qoting.
- [ ] Ichma-ich indeksli sikllarda indeks nomini kolleksiya bosh harfiga bog'lang (`ci`, `mi`, `ui`) yoki ichki siklni metodga chiqarib indeksni butunlay olib tashlang.

## Manbalar

- Dustin Boswell, Trevor Foucher, *The Art of Readable Code*, 1-nashr, O'Reilly, 2011 (copyright 2012), 3-bob (26-bet) - ikki uchi ham kiradigan oraliq uchun `first`/`last` (`stop` ning noaniqligi), oxiri kirmaydigan yarim ochiq oraliq uchun `begin`/`end` idiomasi va yarim ochiq oraliqning amaliy qulayligi
- Joshua Bloch, *Effective Java* 3rd, Item 58 - an'anaviy `for` o'rniga `for-each`
- Joshua Bloch, *Effective Java* 3rd, Item 57 - lokal o'zgaruvchi qamrovini kichik ushlash, sikl o'zgaruvchisi
- Joshua Bloch, *Effective Java* 3rd, Item 46 - oqimda yon ta'sirsiz funksiyalar
- [Java API, `ConcurrentModificationException`](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/ConcurrentModificationException.html) - iteratsiya vaqtida to'plamni o'zgartirish
- Steve McConnell, *Code Complete*, 2-nashr, 16.3 (385-bet) - siklni ichdan tashqariga qurish texnikasi
- Steve McConnell, *Code Complete*, 2-nashr, 17.2 (393, 396-398-bet) - rekursiyaning tugashi, xavfsizlik hisoblagichi, stek chuqurligi va sikl bilan almashtirish
- [Java API, `StackOverflowError`](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/StackOverflowError.html) - rekursiya juda chuqur bo'lganda tashlanadi
- Dustin Boswell, Trevor Foucher, *The Art of Readable Code*, 1-nashr, O'Reilly, 2011 (copyright 2012), 2-bob (12-bet) - ichma-ich siklda indeks nomini kolleksiya bosh harfiga bog'lash (`ci`, `mi`, `ui`) va xatoning ko'rinib qolishi
- Dustin Boswell, Trevor Foucher, *The Art of Readable Code*, 1-nashr, O'Reilly, 2011 (copyright 2012), 7-bob (74-75-betlar) - `do/while` da shartning pastda turishi, `continue` ning chalkashligi, tanani takrorlab almashtirish taqiqi va Stroustrup ning `do` dan qochish pozitsiyasi
- Dustin Boswell, Trevor Foucher, *The Art of Readable Code*, 1-nashr, O'Reilly, 2011 (copyright 2012), 9-bob (96-bet) - nazorat flagi ta'rifi (programma ma'lumotini saqlamaydigan o'zgaruvchi), "sikl o'rtasidan chiqmaslik" qoidasining yo'qligi va ichma-ich siklda metodga chiqarish yechimi
- Paul Deitel va Harvey Deitel, *Java How to Program*, 10-nashr, Early Objects, Pearson, 5-bob (154-bet) - sikl boshqaruvida suzuvchi nuqtali o'zgaruvchi ishlatmaslik, sanagich uchun butun son olish
- Y. Daniel Liang, *Introduction to Java Programming*, 9-nashr, Pearson, 2013, 4-bob (142-bet) - sikl boshqaruvida suzuvchi nuqtali qiymat bilan tenglik tekshirmaslik (ikkinchi mustaqil manba)
- Paul Deitel va Harvey Deitel, *Java How to Program*, 10-nashr, Early Objects, Pearson, 5-bob (159-bet) - qadami 1 dan katta siklning shartida `==` va `!=` o'rniga munosabat operatorini ishlatish
- Paul Deitel va Harvey Deitel, *Java How to Program*, 10-nashr, Early Objects, Pearson, 5-bob (162-bet) - natijasi o'zgarmaydigan hisobni sikl ichidan sikl oldiga chiqarish
- Joshua Bloch, *Effective Java* 3rd, Item 58 (265-bet) - ichma-ich iteratsiyada tashqi iteratorning `next()` ini ichki siklda chaqirish xatosi: `NoSuchElementException` yoki o'lchamlar karrali bo'lganda jim noto'g'ri natija
- ESLATMA: `policy.limitFor` va `Card` kod misollari korpus qo'shimchasi; kitoblar qoidani boshqa misollarda beradi, `sonarqube` bilan bog'lanish ham korpus qo'shimchasi

---

[&larr; 6. Shart, mantiq va boshqaruv oqimi](06-shart-mantiq-va-boshqaruv-oqimi.md) · [Mundarija](README.md) · [8. Izoh qoidalari: yaxshi izohlar &rarr;](08-izoh-qoidalari-yaxshi-izohlar.md)
