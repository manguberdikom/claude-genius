<!-- doc: clean-code | chapter: 24 | part: VII. Java tilining toza ishlatilishi -->

[Toza kod yozuvchining qoidalari](../../README.md) / [Toza kod qoidalari](README.md)

# 24. Lambda, oqim va funksional uslub tozaligi (Lambdas and Streams)

<details>
<summary>Bu bobdagi 10 bo'lim</summary>

- [24.1 Lambda uzunligi va uni metodga chiqarish](#241-lambda-uzunligi-va-uni-metodga-chiqarish)
- [24.2 Metod havolasi qachon o'qiladi](#242-metod-havolasi-qachon-oqiladi)
- [24.3 Standart funksional interfeyslar va o'zingiznikini yozmaslik](#243-standart-funksional-interfeyslar-va-ozingiznikini-yozmaslik)
- [24.4 Oqim ichida yon ta'sir va `forEach` tuzog'i](#244-oqim-ichida-yon-tasir-va-foreach-tuzogi)
- [24.5 `peek`, `parallelStream` va tartib](#245-peek-parallelstream-va-tartib)
- [24.6 `Optional` ni zanjirda toza ishlatish](#246-optional-ni-zanjirda-toza-ishlatish)
- [24.7 Tekshiriladigan istisno va lambda](#247-tekshiriladigan-istisno-va-lambda)
- [24.8 `Collectors` ni o'qiladigan ushlash](#248-collectors-ni-oqiladigan-ushlash)
- [24.9 Oqimni qaytarish yoki to'plam qaytarish](#249-oqimni-qaytarish-yoki-toplam-qaytarish)
- [24.10 Amalda qo'llash](#2410-amalda-qollash)

</details>


Oqim va sikl tanlovi [arxitektor hujjatidagi](../architect/README.md) Stream API bo'limida, `Optional` ning to'g'ri ishlatilishi 13.5 da berilgan. Bu bobda funksional kodning tozalik qoidalari: lambda uzunligi, metod havolasi, yon ta'sir, `Collectors` ni o'qiladigan ushlash va istisnolar.

## 24.1 Lambda uzunligi va uni metodga chiqarish

Lambda bir ifoda bo'lsa o'qiladi; blokka aylansa (qavs va `return` paydo bo'lsa) o'qilishi tushadi. Amaliy chegara: lambda uch qatordan oshsa, uni nomlangan metodga chiqarish kerak - shunda nom niyatni aytadi va metod alohida testlanadi.

```java
// yomon: oqim ichida 8 qatorli lambda
List<SettlementRow> valid = rows.stream()
        .filter(row -> {
            if (row.amount() == null) return false;
            if (row.amount().signum() <= 0) return false;
            if (row.currency() == null) return false;
            if (!SUPPORTED.contains(row.currency())) return false;
            return row.settledAt() != null;
        })
        .toList();

// yaxshi: qoida nomlangan va testlanadi
List<SettlementRow> valid = rows.stream()
        .filter(this::isValid)
        .toList();

private boolean isValid(SettlementRow row) { ... }
```

## 24.2 Metod havolasi qachon o'qiladi

Metod havolasi (`Payment::isSettled`) lambdadan qisqa va nom ma'noni aytadi, shuning uchun mavjud bo'lsa afzal. Lekin u har doim o'qiladi degani emas: argumentlar tartibi ko'rinmasa yoki konstruktor havolasi noaniq bo'lsa, lambda aniqroq.

```java
// yaxshi: metod havolasi nomni beradi
.filter(Payment::isSettled)
.map(Payment::amount)
.sorted(comparing(Payment::settledAt))

// yomon: argumentlar tartibi ko'rinmaydi
.reduce(Money::add)            // qaysi qiymat qaysi pozitsiyada?
// yaxshi: aniq
.reduce(Money.ZERO, (sum, next) -> sum.plus(next))

// yomon: konstruktor havolasi noaniq (bir nechta konstruktor bor)
.map(SettlementRow::new)
// yaxshi
.map(line -> SettlementRow.parse(line))
```

## 24.3 Standart funksional interfeyslar va o'zingiznikini yozmaslik

`java.util.function` paketi 43 ta interfeys beradi va ularning hammasi uchun o'z interfeysingizni yozish keraksiz: standart turlar bilan sizning kodingiz boshqa kutubxonalar bilan birga ishlaydi.

| Shakl | Interfeys |
|---|---|
| `T → R` | `Function<T,R>` |
| `T → boolean` | `Predicate<T>` |
| `T → void` | `Consumer<T>` |
| `() → T` | `Supplier<T>` |
| `(T,U) → R` | `BiFunction<T,U,R>` |
| `T → T` | `UnaryOperator<T>` |
| `(T,T) → T` | `BinaryOperator<T>` |
| primitiv variantlar | `IntPredicate`, `ToLongFunction` va h.k. |

O'z interfeysingizni yozish faqat ikki holatda haqli: nom domen ma'nosini beradi (`interface TaxPolicy { Money taxFor(Region r, Money net); }`), yoki tekshiriladigan istisno tashlanishi kerak (24.7).

## 24.4 Oqim ichida yon ta'sir va `forEach` tuzog'i

Oqim transformatsiya uchun mo'ljallangan; uning ichida tashqi holatni o'zgartirish ikki muammo keltiradi: parallel oqimda poyga holati, va o'qilishi - oqim nima qaytarayotgani ko'rinmaydi.

```java
// yomon: oqim ichida tashqi holat o'zgaradi
List<String> codes = new ArrayList<>();
orders.stream().forEach(order -> codes.add(order.code()));   // yon ta'sir

// yaxshi: oqim natija qaytaradi
List<String> codes = orders.stream().map(Order::code).toList();

// yomon: forEach ichida biznes amali va tranzaksiya
orders.stream().forEach(order -> {
    order.markShipped();
    repository.save(order);        // har bir element uchun alohida so'rov (7.9)
});

// yaxshi: oqim tanlaydi, sikl yoki paket amali o'zgartiradi
List<OrderId> toShip = orders.stream().filter(Order::isReadyToShip).map(Order::id).toList();
repository.markShipped(toShip);
```

## 24.5 `peek`, `parallelStream` va tartib

`peek` faqat **debug** uchun mo'ljallangan va uni mantiqda ishlatish xato: terminal amal bo'lmasa oqim umuman bajarilmaydi, va ba'zi optimizatsiyalarda `peek` chaqirilmaydi.

`parallelStream` esa deyarli har doim noto'g'ri tanlov: u umumiy `ForkJoinPool.commonPool` ni ishlatadi (butun ilova bilan birga), kichik to'plamlarda sekinroq, va yon ta'sirli kod bilan buziladi. Qoida: `parallelStream` faqat o'lchov natijasi asosida, CPU ga bog'liq, katta va mustaqil hisob uchun.

```java
// yomon: tartibni buzadi va umumiy pool ni egallaydi
orders.parallelStream().forEach(repository::save);     // I/O - parallel oqim uchun emas

// yaxshi: I/O uchun oshkor executor
try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
    orders.forEach(order -> executor.submit(() -> gateway.notify(order)));
}
```

`forEachOrdered` tartibni saqlaydi, lekin parallel oqimning foydasini yo'qotadi - bu ikkisining birga kerak bo'lishi parallel oqim noto'g'ri tanlov ekanini bildiradi.

## 24.6 `Optional` ni zanjirda toza ishlatish

`Optional` ning asosiy qoidalari [arxitektor hujjatidagi](../architect/README.md) `Optional` bo'limida: qaytish qiymati sifatida ishlatiladi, maydon va parametr sifatida emas. Bu yerda zanjirni toza ushlash qoidalari.

```java
// yomon: isPresent + get - Optional ning ma'nosi yo'qoladi
if (maybeOrder.isPresent()) {
    return maybeOrder.get().total();
}
return Money.ZERO;

// yaxshi: zanjir
return maybeOrder.map(Order::total).orElse(Money.ZERO);

// yomon: orElse ichida qimmat chaqiruv - har doim bajariladi
return findCached(id).orElse(loadFromDatabase(id));    // baza har doim o'qiladi!

// yaxshi: orElseGet lazy
return findCached(id).orElseGet(() -> loadFromDatabase(id));

// yaxshi: topilmasa istisno, xabar bilan
return repository.findById(id)
        .orElseThrow(() -> new OrderNotFoundException(id));
```

Qo'shimcha qoidalar: `Optional.get()` ni hech qachon tekshiruvsiz chaqirmaslik, `Optional` ni `null` qilmaslik, va `Optional<List<T>>` o'rniga bo'sh ro'yxat qaytarish (18.8).

## 24.7 Tekshiriladigan istisno va lambda

Standart funksional interfeyslar tekshiriladigan istisno tashlamaydi, shuning uchun oqim ichida `IOException` tashlaydigan kod kompilyatsiyadan o'tmaydi. Uch yechim bor va ularning tartibi shunday.

```java
// 1) Eng yaxshi: oqim o'rniga sikl ishlatish
List<String> contents = new ArrayList<>();
for (Path file : files) {
    contents.add(Files.readString(file, UTF_8));     // istisno tabiiy o'tadi
}

// 2) O'rash uchun yordamchi metod (istisno turini saqlab)
private String readOrThrow(Path file) {
    try {
        return Files.readString(file, UTF_8);
    } catch (IOException e) {
        throw new UncheckedIOException("fayl o'qilmadi: " + file, e);
    }
}
List<String> contents = files.stream().map(this::readOrThrow).toList();

// 3) Yomon: lambda ichida try/catch - oqim o'qilmaydi
files.stream().map(f -> { try { ... } catch (IOException e) { ... } });
```

`@SneakyThrows` (Lombok) bu muammoni yashiradi, lekin istisnoni imzodan olib tashlaydi va chaqiruvchi uni ko'rmaydi - shu sababli taqiqlanishi kerak (26.10).

## 24.8 `Collectors` ni o'qiladigan ushlash

`Collectors` zanjirlari tez murakkablashadi va ichma-ich `groupingBy` o'qilmaydigan kod beradi. Qoida: ikki darajadan chuqur guruhlashni oraliq turga chiqarish.

```java
// yomon: uch darajali ichma-ich collector - o'qilmaydi
Map<Region, Map<Currency, List<Money>>> result = payments.stream()
        .collect(groupingBy(Payment::region,
                groupingBy(Payment::currency,
                        mapping(Payment::amount, toList()))));

// yaxshi: oraliq tur ma'no beradi
record RegionCurrency(Region region, Currency currency) { }

Map<RegionCurrency, Money> totals = payments.stream()
        .collect(groupingBy(p -> new RegionCurrency(p.region(), p.currency()),
                reducing(Money.ZERO, Payment::amount, Money::plus)));
```

Statik import (`groupingBy` emas `Collectors.groupingBy`) shu kodni ancha o'qiladigan qiladi va bu `Collectors` uchun qabul qilingan istisno (12.7).

## 24.9 Oqimni qaytarish yoki to'plam qaytarish

Public metod `Stream` qaytarishi mumkin, lekin bu shartnomani o'zgartiradi: oqim bir marta o'qiladi va yopilishi kerak bo'lishi mumkin. Shuning uchun standart tanlov - `List` qaytarish; `Stream` faqat ikki holatda.

| Holat | Qaytish turi |
|---|---|
| Kichik yoki o'rta natija | `List<T>` |
| Katta natija, lazy o'qish kerak | `Stream<T>` (`@MustBeClosed` bilan) |
| Bazadan oqim (kursor) | `Stream<T>`, `try-with-resources` majburiy |
| Faqat iteratsiya kerak | `Iterable<T>` |
| Chaqiruvchi filtrlaydi | `List<T>`, keyin `.stream()` |

```java
// Bazadan oqim: yopilishi majburiy va bu hujjatlanadi
/**
 * Hisobot uchun to'lovlar oqimi. Oqim <b>yopilishi kerak</b>:
 * {@code try (var stream = ...)} ichida ishlatiladi, aks holda
 * ulanish qaytarilmaydi.
 */
@Transactional(readOnly = true)
Stream<Payment> streamSettledIn(DateRange range);
```

## 24.10 Amalda qo'llash

- [ ] Uch qatordan uzun lambdalarni topib, nomlangan metodlarga chiqaring.
- [ ] Oqim ichida tashqi to'plamga yozadigan `forEach` larni `map`/`collect` ga o'tkazing.
- [ ] `peek` ishlatilgan joylarni mantiqdan olib tashlang yoki log uchun oshkor metodga aylantiring.
- [ ] `parallelStream` chaqiruvlarini ko'rib, I/O bo'lsa oshkor executor ga, o'lchovsiz bo'lsa ketma-ket oqimga qaytaring.
- [ ] `isPresent()` + `get()` namunalarini `map`/`orElseGet`/`orElseThrow` zanjiriga aylantiring.
- [ ] `orElse(<qimmat chaqiruv>)` holatlarini `orElseGet` ga o'tkazing.
- [ ] `@SneakyThrows` ishlatilgan joylarni oshkor o'rashga almashtirib, annotatsiyani taqiqlang.
- [ ] Ikki darajadan chuqur `groupingBy` zanjirlarini oraliq record bilan tekislang.

---

[&larr; 23. To'plamlar va generiklar gigiyenasi](23-toplamlar-va-generiklar-gigiyenasi.md) · [Mundarija](README.md) · [25. Java kodidagi umumiy tuzoqlar &rarr;](25-java-kodidagi-umumiy-tuzoqlar.md)
