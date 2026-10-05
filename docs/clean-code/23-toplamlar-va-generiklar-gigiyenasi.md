<!-- doc: clean-code | chapter: 23 | part: VII. Java tilining toza ishlatilishi -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

# 23. To'plamlar va generiklar gigiyenasi (Collections and Generics)

<details>
<summary>Bu bobdagi 12 bo'lim</summary>

- [23.1 To'g'ri to'plam turini tanlash](#231-togri-toplam-turini-tanlash)
- [23.2 `Map` ni toza ishlatish](#232-map-ni-toza-ishlatish)
- [23.3 `Collectors.toMap` va takrorlangan kalit](#233-collectorstomap-va-takrorlangan-kalit)
- [23.4 Iteratsiya tartibi](#234-iteratsiya-tartibi)
- [23.5 `Arrays.asList`, `List.of` va o'zgartirilmaslik farqi](#235-arraysaslist-listof-va-ozgartirilmaslik-farqi)
- [23.6 `null` kalit va qiymat siyosati](#236-null-kalit-va-qiymat-siyosati)
- [23.7 Xom tur va `unchecked` ogohlantirish](#237-xom-tur-va-unchecked-ogohlantirish)
- [23.8 Wildcard qoidalari: PECS](#238-wildcard-qoidalari-pecs)
- [23.9 Generik metod, tur xulosasi va `var`](#239-generik-metod-tur-xulosasi-va-var)
- [23.10 Massiv va generikni aralashtirmaslik](#2310-massiv-va-generikni-aralashtirmaslik)
- [23.11 To'plamni qaytarish: nusxa, ko'rinish, oqim](#2311-toplamni-qaytarish-nusxa-korinish-oqim)
- [23.12 Amalda qo'llash](#2312-amalda-qollash)

</details>


To'plam tanlovi va generik turlar bilan ishlash Java kodining kundalik qismi, va shu sababli kichik xatolar ko'p takrorlanadi. Bu bobda to'plam turini tanlash, `Map` ni toza ishlatish, iteratsiya tartibi, o'zgartirilmaslik darajalari (16.3 ni to'ldiradi) va generiklar qoidalari.

## 23.1 To'g'ri to'plam turini tanlash

To'plam tanlovi xatti-harakatni belgilaydi: tartib, dublikat, qidiruv tezligi, `null` siyosati. Noto'g'ri tanlov kodni ishlaydigan, lekin sekin yoki nozik xato bilan qoldiradi.

| Ehtiyoj | Tur |
|---|---|
| Tartibli ro'yxat, indeks bo'yicha kirish | `ArrayList` |
| Boshidan/oxiridan qo'shish, navbat | `ArrayDeque` |
| Dublikatsiz, tartib muhim emas | `HashSet` |
| Dublikatsiz, qo'shilish tartibida | `LinkedHashSet` |
| Dublikatsiz, saralangan | `TreeSet` |
| Kalit-qiymat, tartib muhim emas | `HashMap` |
| Kalit-qiymat, qo'shilish tartibida | `LinkedHashMap` |
| Kalit-qiymat, saralangan | `TreeMap` |
| Kalit - enum | `EnumMap` (25.9) |
| O'zgarmas, kichik | `List.of`, `Map.of`, `Set.of` |
| Ko'p threadli | `ConcurrentHashMap`, `CopyOnWriteArrayList` |

`LinkedList` ni ishlatish uchun deyarli hech qanday sabab qolmagan: `ArrayDeque` navbat uchun tezroq, `ArrayList` ro'yxat uchun tezroq.

## 23.2 `Map` ni toza ishlatish

`Map` bilan ishlashda eski shakllar (`containsKey` + `get` + `put`) uzun, ikki marta qidiradi va xatoga moyil. Zamonaviy metodlar bir chaqiruvda ishlaydi va niyatni aytadi.

```java
// yomon: uch chaqiruv, uch marta hash hisoblanadi
if (!index.containsKey(sku)) {
    index.put(sku, new ArrayList<>());
}
index.get(sku).add(order);

// yaxshi
index.computeIfAbsent(sku, k -> new ArrayList<>()).add(order);

// yomon: null tekshiruvi va NPE xavfi (20.6)
Integer count = counters.get(sku);
counters.put(sku, count == null ? 1 : count + 1);

// yaxshi
counters.merge(sku, 1, Integer::sum);

// yaxshi: standart qiymat
int available = stock.getOrDefault(sku, 0);
```

| Niyat | Metod |
|---|---|
| Yo'q bo'lsa yaratish | `computeIfAbsent` |
| Bor bo'lsa yangilash | `computeIfPresent` |
| Qiymatni yig'ish | `merge` |
| Standart qiymat o'qish | `getOrDefault` |
| Faqat yo'q bo'lsa qo'yish | `putIfAbsent` |
| Shart bo'yicha o'chirish | `entrySet().removeIf` |
| Hamma qiymatni o'zgartirish | `replaceAll` |

## 23.3 `Collectors.toMap` va takrorlangan kalit

`Collectors.toMap` ikki argumentli shakli takrorlangan kalit uchrasa `IllegalStateException` tashlaydi. Bu ko'pincha testda ko'rinmaydi va production ma'lumotida chiqadi.

```java
// yomon: dublikat kalit bo'lsa IllegalStateException
Map<Sku, Order> byTopSku = orders.stream()
        .collect(toMap(Order::topSku, identity()));

// yaxshi: birlashtirish funksiyasi oshkor - qaror kodda ko'rinadi
Map<Sku, Order> byTopSku = orders.stream()
        .collect(toMap(Order::topSku, identity(), (first, second) -> first));

// yaxshi: dublikat normal bo'lsa, guruhlash
Map<Sku, List<Order>> bySku = orders.stream().collect(groupingBy(Order::topSku));
```

Ikkinchi tuzoq: `toMap` `null` qiymatni qabul qilmaydi (`merge` ichida NPE beradi), `groupingBy` esa qabul qiladi.

## 23.4 Iteratsiya tartibi

`HashMap` va `HashSet` tartibi **kafolatlanmaydi** va JVM versiyasi yoki element soni o'zgarganda o'zgaradi. Shu sababli ularning tartibiga bog'lanish yashirin xato: kod bugun ishlaydi, keyingi reliz da boshqa tartib beradi.

```java
// yomon: tartibga bog'langan test va mantiq
Map<String, Integer> counts = new HashMap<>();
String report = counts.keySet().stream().collect(joining(", "));   // tartib tasodifiy

// yaxshi: tartib kerak bo'lsa, u oshkor tanlanadi
Map<String, Integer> counts = new LinkedHashMap<>();    // qo'shilish tartibi
Map<String, Integer> counts = new TreeMap<>();          // alifbo tartibi
String report = counts.keySet().stream().sorted().collect(joining(", "));
```

## 23.5 `Arrays.asList`, `List.of` va o'zgartirilmaslik farqi

Uch shakl o'xshash ko'rinadi, lekin uch xil xatti-harakat beradi va ularni aralashtirish `UnsupportedOperationException` ga olib keladi.

```java
List<String> a = Arrays.asList("x", "y");   // fiksirlangan hajm; set() ishlaydi, add() yo'q
List<String> b = List.of("x", "y");         // to'liq o'zgarmas; null taqiqlangan
List<String> c = new ArrayList<>(List.of("x", "y"));   // to'liq o'zgaradi

a.set(0, "z");    // ishlaydi
a.add("z");       // UnsupportedOperationException
b.set(0, "z");    // UnsupportedOperationException
```

Qoida: o'zgarmas kerak bo'lsa `List.of`/`List.copyOf`; o'zgaradigan kerak bo'lsa oshkor `new ArrayList<>(...)`. `Arrays.asList` faqat massivni ro'yxat sifatida o'qish uchun.

## 23.6 `null` kalit va qiymat siyosati

`null` ga munosabat to'plam turiga qarab farq qiladi va bu farq hujjatlanmagan xatolarning manbai.

| Tur | `null` kalit | `null` qiymat |
|---|---|---|
| `HashMap` | 1 ta ruxsat | ruxsat |
| `TreeMap` | taqiqlangan (NPE) | ruxsat |
| `ConcurrentHashMap` | taqiqlangan | taqiqlangan |
| `Map.of` | taqiqlangan | taqiqlangan |
| `HashSet` | 1 ta ruxsat | - |
| `List.of` | taqiqlangan | - |
| `ArrayList` | ruxsat | - |

Eng ko'p uchraydigan tuzoq: `HashMap` dan `ConcurrentHashMap` ga o'tish mavjud kodni buzadi, chunki `null` qiymat endi taqiqlangan. Qoida: to'plamlarda `null` ni umuman ishlatmaslik (18.7).

## 23.7 Xom tur va `unchecked` ogohlantirish

Xom tur (`List` generik parametrsiz) tur xavfsizligini butunlay o'chiradi va faqat eski kod bilan moslik uchun qolgan. `@SuppressWarnings("unchecked")` esa faqat ikki shart bilan haqli: boshqa yo'l yo'q, va sabab izohda yozilgan.

```java
// yomon: xom tur - tur tekshiruvi yo'q
List orders = repository.findAll();
orders.add("satr");           // kompilyatsiyadan o'tadi, ClassCastException keyin chiqadi

// yaxshi: generik tur
List<Order> orders = repository.findAll();

// yaxshi: bostirish eng kichik qamrovda va izohlangan
@SuppressWarnings("unchecked")   // JPA native query Object[] qaytaradi, mapping qo'lda
List<SettlementRow> rows = (List<SettlementRow>) query.getResultList();
```

Qoida: `-Xlint:all` va `-Werror` bilan ogohlantirishlarni xatoga aylantirish (25.11).

## 23.8 Wildcard qoidalari: PECS

Generik parametrlarda `? extends` va `? super` tanlovi uchun oddiy qoida bor: **PECS** - Producer Extends, Consumer Super. Agar parametr ma'lumot **beradi** (o'qiladi), `? extends`; agar ma'lumot **oladi** (yoziladi), `? super`.

```java
// Ishlab chiqaruvchi (o'qiymiz): extends
Money totalOf(List<? extends Payment> payments) {
    return payments.stream().map(Payment::amount).reduce(Money.ZERO, Money::add);
}
// Shunda List<CardPayment> ham, List<BankPayment> ham qabul qilinadi

// Iste'molchi (yozamiz): super
void collectInto(List<? super SettlementRow> target) {
    target.add(new SettlementRow(...));
}

// Ikkisi ham kerak bo'lsa: wildcard yo'q, aniq tur
void copy(List<? extends T> source, List<? super T> target) { ... }
```

Amaliy qoida: **qaytish turida** wildcard ishlatmaslik - u chaqiruvchini wildcard bilan ishlashga majbur qiladi va kod tarqaladi.

## 23.9 Generik metod, tur xulosasi va `var`

Generik metod turni argumentdan xulosa qiladi va bu kodni qisqartiradi. `var` bilan birga ishlatilganda esa tur umuman ko'rinmay qolishi mumkin - bunda o'qilish buziladi ([arxitektor hujjatidagi](../architect/README.md) matn bloki va `var` bo'limi).

```java
// yaxshi: generik metod, tur xulosa qilinadi
static <T> List<T> firstN(List<T> source, int n) { ... }
List<Order> first10 = firstN(orders, 10);

// yomon: var + generik metod - tur hech qayerda ko'rinmaydi
var result = process(input);

// yaxshi: var faqat o'ng tomonda tur ko'rinsa
var orders = new ArrayList<Order>();
var byId = new HashMap<OrderId, Order>();
```

## 23.10 Massiv va generikni aralashtirmaslik

Massivlar kovariant (`Object[] = String[]` ruxsat) va ish vaqtida tur tekshiradi; generiklar invariant va ish vaqtida turni o'chiradi. Ikkisini aralashtirish `ArrayStoreException` yoki kompilyator ogohlantirishiga olib keladi.

```java
// yomon: massiv kovariantligi ish vaqtida xato beradi
Object[] objects = new String[1];
objects[0] = 42;              // ArrayStoreException

// yomon: generik massiv yaratib bo'lmaydi
List<String>[] lists = new List<String>[10];    // kompilyatsiya xatosi

// yaxshi: to'plam ishlatish
List<List<String>> lists = new ArrayList<>();
```

Qoida: public API da massiv qaytarmaslik (u o'zgaradi va nusxa talab qiladi, 14.7); `List` qaytarish.

## 23.11 To'plamni qaytarish: nusxa, ko'rinish, oqim

Metod to'plam qaytarganda uchta tanlov bor va ularning har biri boshqa shartnoma beradi.

| Shakl | Shartnoma | Qachon |
|---|---|---|
| `List.copyOf(internal)` | o'zgarmas nusxa | standart tanlov |
| `Collections.unmodifiableList(internal)` | o'zgarmas ko'rinish, manba o'zgarsa o'zgaradi | katta to'plam, ichki ishlatish |
| `new ArrayList<>(internal)` | chaqiruvchi o'zgartira oladi | kamdan-kam, oshkor hujjatlanadi |
| `Stream<T>` | bir marta o'qiladi | katta natija, lazy |
| `Iterable<T>` | faqat iteratsiya | API ni torroq qilish |

Hech qachon ichki to'plamni to'g'ridan-to'g'ri qaytarmaslik kerak (14.7). Qaytish turi nomda va hujjatda aniq bo'lishi kerak: `List` tartibni kafolatlaydi, `Collection` yo'q.

## 23.12 Amalda qo'llash

- [ ] `containsKey` + `get` + `put` namunalarini `computeIfAbsent`, `merge`, `getOrDefault` ga o'tkazing.
- [ ] `Collectors.toMap` ning ikki argumentli shakllarini topib, birlashtirish funksiyasini oshkor qo'shing.
- [ ] `HashMap`/`HashSet` tartibiga bog'langan mantiq va testlarni topib, `LinkedHashMap` yoki oshkor saralashga o'tkazing.
- [ ] `Arrays.asList` ishlatilgan joylarni niyatga qarab `List.of` yoki `new ArrayList<>` ga almashtiring.
- [ ] Xom generik turlarni (`List`, `Map` parametrsiz) topib, tur parametrlarini qo'shing.
- [ ] `@SuppressWarnings` larni ko'rib, qamrovini torroq qilib, sababini izohlang.
- [ ] Public API dagi massiv qaytaradigan metodlarni `List` ga o'tkazing.
- [ ] To'plam qaytaradigan getter larni 23.11 jadvaliga qarab bitta izchil shaklga keltiring.

---

[&larr; 22. Sana, vaqt va mintaqa](22-sana-vaqt-va-mintaqa.md) · [Mundarija](README.md) · [24. Lambda, oqim va funksional uslub tozaligi &rarr;](24-lambda-oqim-va-funksional-uslub-tozaligi.md)
