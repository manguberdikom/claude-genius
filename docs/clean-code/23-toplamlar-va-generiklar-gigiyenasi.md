<!-- doc: clean-code | chapter: 23 | part: VII. Java tilining toza ishlatilishi -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 23. To'plamlar va generiklar gigiyenasi (Collections and Generics)

<details>
<summary>Bu bobdagi 14 bo'lim</summary>

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
- [23.12 `PriorityQueue` va `PriorityBlockingQueue` (Priority Queue)](#2312-priorityqueue-va-priorityblockingqueue-priority-queue)
- [23.13 Massiv bilan ishlash: chegara, qidiruv va `toArray`](#2313-massiv-bilan-ishlash-chegara-qidiruv-va-toarray)
- [23.14 Amalda qo'llash](#2314-amalda-qollash)

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
| Ustuvorlik bo'yicha chiqarish, keyingisini olish | [`PriorityQueue`](#2312-priorityqueue-va-priorityblockingqueue-priority-queue) |
| Kalit - enum | `EnumMap` (25.9) |
| O'zgarmas, kichik | `List.of`, `Map.of`, `Set.of` |
| Ko'p threadli | `ConcurrentHashMap`, `CopyOnWriteArrayList` |

Tanlov implementatsiya haqida, e'lon esa boshqa qaror: o'zgaruvchi, parametr, maydon va qaytish turi mos interfeys bilan e'lon qilinadi, implementatsiya sinfi faqat `new` yonida qoladi. Shunda keyinroq implementatsiyani almashtirish bitta qatorga tegadi.

```java
// yomon: implementatsiya turi imzoga chiqib ketgan
public ArrayList<Order> recent(HashMap<OrderId, Order> cache) { ... }

// yaxshi: interfeys turi, almashtirish bir qatorda
public List<Order> recent(Map<OrderId, Order> cache) { ... }
```

Istisno: interfeysda yo'q xatti-harakatga tayangan joy. `ArrayDeque` ning ikki tomonli navbat shartnomasi yoki `LinkedHashMap` ning qo'shilish tartibi kerak bo'lsa, shu tur e'lon qilinadi, lekin bu tanlov izohda yoki nomda ko'rinishi kerak.

Shu istisnoning ortida adabiyotdagi ikkinchi pozitsiya turadi va uni bilib qo'yish kerak. Ousterhout `private List<Message> incomingMessageList;` deb e'lon qilib, keyin uni `new ArrayList<Message>()` bilan yaratishni noravshan kod misoli sifatida keltiradi: e'lonni ko'rgan, lekin yaratilgan joyni ko'rmagan o'quvchi chalg'iydi, chunki haqiqiy tur o'zgaruvchining qanday ishlatilishiga ta'sir qiladi - `ArrayList` ning ishlash va thread-safety xususiyatlari `List` ning boshqa implementatsiyalaridan farq qiladi. Uning xulosasi: e'lonni yaratilgan tur bilan moslashtirish yaxshiroq (Ousterhout, *A Philosophy of Software Design*, 1-nashr, Yaknyam Press, 2018, 18.2).

Ikki qoida zid ko'rinadi, lekin ular boshqa joy haqida gapiradi. Ajratadigan shart - e'lon kimga ko'rinadi:

| E'lon qilinadigan joy | Tur | Nega |
|---|---|---|
| Public metod parametri, qaytish turi, moduldan tashqariga ko'rinadigan maydon | interfeys (`List`, `Map`, `Set`) | tur shartnomaning bir qismi; chaqiruvchi implementatsiyaga bog'lanmasligi kerak |
| Sinf ichidagi `private` maydon va lokal o'zgaruvchi, ayniqsa e'lon bilan `new` orasi uzoq | yaratilgan sinf yoki izoh bilan interfeys | bu yerda interfeys hech narsani yashirmaydi (tashqariga chiqmaydi), e'lon esa o'quvchi uchun yagona ma'lumot manbai |

Ya'ni interfeys bilan e'lon qilish qoidasi shartnomaga tegishli, Ousterhout ning ogohlantirishi esa o'qilishiga: yashiriladigan narsa bo'lmagan joyda abstrakt e'lon faqat ma'lumot yo'qotadi. Uchinchi yo'l ko'p holatda yetarli bo'ladi - e'lonni interfeysda qoldirib, tanlovni bitta qisqa izoh bilan aytish:

```java
// Qo'shilish tartibi kerak: hisobot ustunlari fayldagi tartibda chiqadi
private final Map<String, BigDecimal> totalsByColumn = new LinkedHashMap<>();
```

Interfeys bilan e'lon qilish qoidasining uch istisnosi bor va ularni
bilish kerak, aks holda qoida mutlaq ko'rinadi:

- **Mos interfeysi yo'q value sinf.** `String`, `BigDecimal`, `Duration`
  uchun "mos interfeys" degan narsa yo'q, demak tur sifatida sinfning
  o'zi yoziladi.
- **Asoslari sinf bo'lgan framework.** Ba'zi framework larning asosiy
  turi interfeys emas, abstrakt sinf (`OutputStream`); shunday holda
  ierarxiyaning umumiy SINFI tanlanadi.
- **Interfeysda yo'q qo'shimcha metodga tayanish.** `comparator()`
  metodi `Queue` da yo'q, demak u kerak bo'lsa `PriorityQueue` turi
  bilan e'lon qilinadi (23.12).

Uchalasida ham bitta zaxira qoida ishlaydi: mos interfeys yo'q bo'lsa,
kerakli funksionallikni beradigan **eng kam maxsus** sinf tanlanadi.
Ya'ni fayl oqimi `FileOutputStream` emas `OutputStream` deb e'lon
qilinadi; maxsusroq tur haqiqatan kerak bo'lmasa, u ortiqcha
bog'liqlikdan boshqa narsa bermaydi. Bu qoida yuqoridagi jadvalga zid
emas: jadval e'lon kimga ko'rinishini hal qiladi, bu qoida esa interfeys
bo'lmagan holatda qanchalik aniq sinf yozilishini.

`LinkedList` ni ishlatish uchun deyarli hech qanday sabab qolmagan: `ArrayDeque` navbat uchun tezroq, `ArrayList` ro'yxat uchun tezroq.

**Prefiks bo'yicha qidiruv saralangan tuzilmaga o'tadi.** `HashMap` to'liq moslik uchun ideal, lekin "shu prefiks bilan boshlanadigan hamma kalitni ber" so'rovi uchun yaramaydi: javob uchun hamma kalitni aylanib chiqish kerak bo'ladi va narx to'plam hajmi bilan chiziqli o'sadi. Shirazi ning bu masala uchun bergan yechimi - saralangan tuzilma va **diapazon qidiruvi**: prefiksdan boshlab prefiks hamda eng katta belgi bilan tugaydigan oraliqdagi kalitlar olinadi. Java da bu bugun `TreeMap.subMap` bilan bir chaqiruvda bajariladi.

```java
// Prefiks bo'yicha qidiruv: oraliq [prefix, prefix + max belgi)
NavigableMap<String, Integer> byKey = new TreeMap<>(Map.of(
        "hello", 1, "hell", 2, "alpha", 3, "bye", 4, "hi", 10));

SortedMap<String, Integer> startingWithH =
        byKey.subMap("h", true, "h" + Character.MAX_VALUE, false);
```

Ikki tafsilotni yozib qo'yish kerak. Birinchi: `TreeMap` yakka kalit bo'yicha o'qish va yozishda `HashMap` dan sezilarli sekinroq, shuning uchun almashtirish faqat prefiks qidiruvi haqiqatan kerak bo'lsa oqlanadi; ikki tuzilmani parallel ushlash esa (hash jadval tez kirish uchun, saralangan massiv diapazon uchun) ikki nusxaning mosligini ta'minlash muammosini keltiradi. Parallel kolleksiya tanlansa, hamma o'qish va yozish **bitta obyekt orqasiga** yashiriladi, shunda izchillikni bitta joy kafolatlaydi. Ikkinchi: parallel yechim asosan **kam o'zgaradigan** to'plam uchun mos, ya'ni bir marta yoki davriy quriladigan va ko'p o'qiladigan ma'lumot uchun.

ESLATMA: Shirazi ning kitobi 2003 yilda chiqqan va uning misoli saralangan massiv ustida binar qidiruvni qo'lda yozadi (`Character.MAX_VALUE` nayrangi ham shundan); zamonaviy shakl `TreeMap.subMap` yoki `NavigableSet.subSet`. PostgreSQL tomonidagi `LIKE 'prefiks%'` indeks masalasi [arxitektor hujjatida](../architect/README.md) alohida ko'rilgan.

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

Oxirgi tafsilot narxga tegishli va u `HashMap` ning `O(1)` da'vosini
aniqlashtiradi. Zanjirli hash jadvalida qidiruvning o'rtacha narxi
`Theta(1 + alfa)`, bunda `alfa = n/m` yuklanish koeffitsiyenti (`n` -
element soni, `m` - bucket soni). Ya'ni `alfa` bitta qidiruvda
ko'riladigan elementlar sonini bevosita belgilaydi va `O(1)` hech qanday
sehr emas. Shundan ikki amaliy xulosa chiqadi. Birinchi: hash funksiyasi
qiymatlarni bucket lar bo'ylab teng taqsimlamasa, ba'zi zanjirlar uzayadi
va o'rtacha narx o'rtacha bo'lib qolmaydi, shuning uchun `hashCode`
sifati to'plam narxining bir qismi (15.2). Ikkinchi: to'plam hajmi
oldindan ma'lum bo'lsa, boshlang'ich sig'imni konstruktorda berish
`alfa` ni past ushlaydi va qayta hashlashni (rehash) oldini oladi.

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

Uchinchi argument faqat dublikatdan qutqarish uchun emas, u siyosat
yoziladigan joy. Ikki shakl ko'p ishlatiladi. Birinchisi "oxirgi
yozuvchi g'alaba qozonadi": `(older, newer) -> newer`. Ikkinchisi
kalitdan **eng yaxshi** elementga xarita qurish:
`BinaryOperator.maxBy(comparing(...))` bilan har kalit uchun komparator
bo'yicha kattasi qoladi. Ikkalasining ham qiymati shunda: siyosat
imzoda ko'rinadi va review da muhokama qilinadi.

```java
// Har mahsulot uchun eng qimmat buyurtma
Map<Sku, Order> topBySku = orders.stream()
        .collect(toMap(Order::topSku, identity(),
                BinaryOperator.maxBy(comparing(Order::total))));

// "Oxirgi yozuvchi g'alaba qozonadi": kech kelgan narx eskisini bosadi
Map<Sku, Price> latest = ticks.stream()
        .collect(toMap(PriceTick::sku, PriceTick::price, (older, newer) -> newer));
```

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

Uchta o'xshash shaklni ajratish kerak, chunki ular bir xil emas. Xom `List` tur tekshiruvidan butunlay chiqadi. `List<Object>` esa tur xavfsiz: unga har qanday obyekt qo'yiladi, lekin u `List<String>` ni qabul qilmaydi (generiklar invariant). `List<?>` - chegarasiz wildcard: unga `null` dan boshqa narsa qo'shilmaydi, lekin har qanday `List<...>` ni qabul qiladi, shuning uchun "ichidagi tur menga ahamiyatsiz, faqat o'qiyman" degan joyda aynan shu yoziladi.

```java
void countAll(List raw) { }            // yomon: tur tekshiruvi yo'q
void countAll(List<Object> any) { }    // List<String> ni QABUL QILMAYDI
void countAll(List<?> any) { }         // yaxshi: har qanday ro'yxatni oladi, yozib bo'lmaydi
```

Xom tur haqli bo'lgan ikki joy bor va ikkisi ham tur ma'lumoti ish vaqtida yo'qolishidan kelib chiqadi: sinf literali (`List.class`, `List<String>.class` yo'q) va `instanceof` (`o instanceof Set` yoziladi, keyin `Set<?>` ga cast qilinadi).

Bu yo'qolishning nomi bor: **type erasure**. Kompilyatsiyadan keyin `Crate<T>`
ichidagi `T` ning hamma ishlatilishi `Object` ga aylanadi, ya'ni generiklar
faqat kompilyatsiya vaqtida bor; bitta `.class` fayl qoladi, har parametrlangan
tur uchun alohida nusxa yaratilmaydi, va kompilyator kerakli cast larni o'zi
qo'yadi (`Robot r = crate.lookInCrate();` chaqiruvi `Robot r = (Robot)
crate.lookInCrate();` ga aylanadi). Sababi moslik: erasure generikli kod
generiksiz eski Java bilan birga ishlashini ta'minlaydi (Boyarsky/Selikoff,
*OCP Java SE 17 Study Guide*, 9-bob (506-507-bet)).

Shundan uchta aniq oqibat chiqadi va ular yuqoridagi ikki istisnodan ko'proq:

- **Overload to'qnashuvi.** `chew(List<Object>)` va `chew(List<Double>)` bitta
  sinfda yashay olmaydi, chunki ikkisi ham `chew(List)` ga aylanadi. Shu sabab
  ota sinfdagi generik metodni overload qilish ham mumkin emas (shu yerda,
  507-bet).
- **`instanceof` va cast chegarasi.** `o instanceof List<String>` yoziladi, chunki
  ish vaqtida `String` haqida ma'lumot yo'q; faqat `o instanceof List<?>`
  mumkin. Shu sababli parametrlangan turga cast `unchecked` ogohlantirish
  beradi va u faqat yuqoridagi ikki shart bilan haqli.
- **Parametrlangan turni ish vaqtiga olib o'tish kerak bo'lganda qo'shimcha
  apparat.** Jackson bilan `List<Order>` ga deserializatsiya qilish uchun
  `Order.class` yetmaydi, `TypeReference` kabi tur tokeni beriladi; Spring ning
  `RestClient` va `WebClient` da xuddi shu rolni
  [`ParameterizedTypeReference`](../patterns/24-zamonaviy-java-va-funksional-patternlar.md#2419-tur-boyicha-xavfsiz-geterogen-konteyner-type-safe-heterogeneous-container)
  bajaradi.

```java
// yomon: erasure dan keyin ikkisi bir xil imzoga aylanadi - kompilyatsiya xatosi
void chew(List<Object> input) { }
void chew(List<Double> input) { }

// yomon: ish vaqtida String haqida ma'lumot yo'q - kompilyatsiya xatosi
if (payload instanceof List<String> orders) { ... }

// yaxshi: tur tokeni bilan parametrlangan tur ish vaqtiga olib o'tiladi
List<Order> orders = objectMapper.readValue(json, new TypeReference<List<Order>>() {});
```

Eski kod bilan chegarada xom tur orqali noto'g'ri element to'plamga
kirib qolishi mumkin, va u ancha keyin, cast paytida
`ClassCastException` bo'lib chiqadi. `Collections.checkedList`,
`checkedSet` va `checkedMap` shu masala uchun: ular tur mosligini **ish
vaqtida** tekshiradigan ko'rinish beradi, ya'ni xato elementni qo'shgan
joyda ushlaydi va stack trace haqiqiy aybdorni ko'rsatadi. Bu doimiy
yechim emas, debug asbobi: tekshiruv har qo'shishda narx qo'shadi.

```java
// Debug: noto'g'ri element qayerdan kelganini qo'shish joyida ushlash
List<Order> orders = Collections.checkedList(new ArrayList<>(), Order.class);
```

Generik turlarni to'g'ri berish lambda ishlatiladigan joyda ikki barobar
muhim, chunki kompilyator tur xulosasini aynan generik turlardan oladi.
Manbada xom tur bo'lsa element turi `Object` bo'lib qoladi va lambda
kompilyatsiyadan o'tmaydi: xato xabari lambdani ko'rsatadi, sababi esa
undan yuqorida, e'lon qatorida turadi.

```java
// yomon: xom tur - lambda ichida Order metodlari ko'rinmaydi
List rows = repository.findAll();
rows.stream().filter(row -> row.isSettled());    // kompilyatsiya xatosi

// yaxshi: tur parametri bor - tur xulosasi lambdaga yetib boradi
List<Order> rows = repository.findAll();
rows.stream().filter(Order::isSettled);
```

Qoida: `-Xlint:all` va `-Werror` bilan ogohlantirishlarni xatoga aylantirish (25.10).

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

Ikkinchi amaliy qoida imzoni soddalashtiradi: tur parametri metod e'lonida **faqat bir marta** uchrasa, uni wildcard bilan almashtiring. Bir marta uchragan `<E>` hech narsani bog'lamaydi, ya'ni u chaqiruvchiga ham, tanaga ham foyda bermaydi, faqat imzoni uzaytiradi.

```java
// ortiqcha: E bir marta uchraydi
static <E> void swapNothing(List<E> list) { }

// yaxshi: wildcard yetadi
static void swapNothing(List<?> list) { }
```

PECS ning eng ko'p kerak bo'ladigan amaliy holati solishtirishda chiqadi:
**barcha `Comparable` va `Comparator` iste'molchi**, chunki ularning
metodi qiymatni qabul qiladi va unga hech narsa qaytarmaydi. Shuning
uchun ularning parametri hamisha `? super` bilan yoziladi.

```java
// Comparable iste'molchi: super
static <T extends Comparable<? super T>> T max(List<? extends T> list) { ... }

// Comparator ham iste'molchi
static <T> void sort(List<T> list, Comparator<? super T> comparator) { ... }
```

Wildcard imzosining bitta mexanik chegarasi bor: `List<?>` ga `null` dan
boshqa qiymat qo'yilmaydi, shuning uchun elementlarni o'zgartiradigan
metodni wildcard imzo bilan to'g'ridan-to'g'ri yozib bo'lmaydi. Yechim -
turni "ushlaydigan" `private` generik yordamchi metod: ommaviy imzo
wildcard bilan qoladi, yordamchi metod esa tur parametrini oladi va shu
bilan yozish mumkin bo'ladi.

```java
// Ommaviy imzo wildcard: chaqiruvchi har qanday ro'yxatni beradi
public static void swap(List<?> list, int i, int j) {
    swapHelper(list, i, j);
}

// private yordamchi tur parametrini "ushlaydi" va yozish imkonini beradi
private static <E> void swapHelper(List<E> list, int i, int j) {
    list.set(i, list.set(j, list.get(i)));
}
```


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

Turlari bir-biridan farq qiladigan qiymatlarni bitta to'plamda, lekin tur xavfsizligini saqlab saqlash kerak bo'lsa, kalit sifatida `Class<T>` ishlatiladi: to'plamning o'zi `Map<Class<?>, Object>`, lekin kirish metodlari `Class<T>` orqali turni tiklaydi. Spring ning `getBean(Class<T>)` shakli ham shu.

```java
// yaxshi: kalit turni o'zida tashiydi, cast bitta joyda va xavfsiz
public final class Attributes {

    private final Map<Class<?>, Object> values = new HashMap<>();

    public <T> void put(Class<T> type, T value) {
        values.put(Objects.requireNonNull(type), type.cast(value));
    }

    public <T> Optional<T> get(Class<T> type) {
        return Optional.ofNullable(type.cast(values.get(type)));
    }
}
```

Chegarasi: generik tur kalit bo'la olmaydi (`List<String>.class` yo'q) va `type.cast` xom tur bilan chaqirilsa tur xavfsizligi buziladi, shu sababli `put` da `cast` bilan tekshirish qoldiriladi.

Generik metod yozishdan oldin bitta savol bor: tur parametrlari
bir-biriga bog'liqmi. JLS ning o'z so'zi bilan, bog'liq bo'lmagan tur
parametrlari bilan generik metod yozish yomon uslub: `<T, U> void
copy(List<T> from, List<U> to)` imzosida `T` va `U` bir-birini
cheklamaydi, demak tur parametri hech narsa kafolatlamaydi va faqat
imzoni uzaytiradi. Shunday holda wildcard yetadi (23.8).

Shu qarorning ikkinchi yarmi joylashuvga tegishli: **statik a'zo o'rab
turgan sinfning tur parametrini ishlatmaydi.** `class Box<T>` ichidagi
`static` metod `T` ni ko'rmaydi, chunki `T` nusxaga tegishli. Shuning
uchun statik yordamchi metod o'z tur parametrini o'zi e'lon qiladi, va bu
generik utility sinf yozishda darhol chiqadi.

```java
public final class Boxes {

    // yomon: Boxes<T> dagi T ni statik metod ko'rmaydi
    // static T firstOf(List<T> list) { ... }

    // yaxshi: statik generik metod o'z tur parametrini e'lon qiladi
    public static <T> Optional<T> firstOf(List<T> list) {
        return list.isEmpty() ? Optional.empty() : Optional.of(list.get(0));
    }
}
```

O'zgarmas, lekin ko'p turga yaroqli obyekt kerak bo'lsa **generik
singleton fabrikasi** yoziladi: erasure sababli bitta obyekt har
parametrlashtirish uchun qayta beriladi, ya'ni har tur uchun alohida
nusxa saqlash kerak emas. JDK da `Collections.reverseOrder()` va
`Function.identity()` aynan shu shakl.

```java
private static final Supplier<?> EMPTY = () -> null;

@SuppressWarnings("unchecked")   // obyektning holati yo'q: har tur uchun xavfsiz
public static <T> Supplier<T> emptySupplier() {
    return (Supplier<T>) EMPTY;
}
```

Ikki qisqa sintaktik qoida bo'limni yopadi. Birinchisi: yangi kodda
`unchecked conversion` ogohlantirishining ko'pi **diamond operatori**
(`<>`) bilan yo'qoladi, ya'ni o'ng tomondagi tur parametrini qo'lda
yozish shart emas va xom tur qoldirish uchun sabab qolmaydi. Ikkinchisi
`var` ga tegishli: e'lon qilinayotgan `var` o'zgaruvchi o'zining
initsializatorida ishlatilmaydi, va `var` bilan massiv initsializatori
yozilmaydi. Ikkisi ham kompilyator xatosi beradi, lekin diffda uchrab
turadi.

```java
List<Order> orders = new ArrayList<>();   // diamond: tur takrorlanmaydi
var count = count + 1;                    // kompilyatsiya xatosi: count hali e'lon qilinmagan
var nums = {1, 2, 3};                     // kompilyatsiya xatosi: initsializator turi yo'q
var nums = new int[] {1, 2, 3};           // yaxshi
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

Ko'rinish (view) qatorida bitta tafsilot bor va u keraksiz obyekt
yaratishni to'sadi: adapter yoki ko'rinish obyektida **backing obyektdan
boshqa holat yo'q**. `map.keySet()` har chaqiruvda yangi obyekt
qaytarsa ham, u bir xil xaritaga qaragan bir xil ko'rinish, shuning
uchun bitta backing obyekt uchun bir nechta adapter saqlash ham, ularni
keshlash ham ma'nosiz. Amaliy oqibat: ko'rinishni maydonda saqlashga
urinmaslik, kerak bo'lganda chaqirish.

Teskari tomondan, o'z turingiz element guruhini ifodalasa, u `Collection`
ni amalga oshirmasa ham **`Iterable` ni amalga oshirishi** kerak: shunda
mijoz uni `for-each` da ishlatadi va yangi metod o'rganishi kerak
bo'lmaydi. Narxi bitta `iterator()` metodi.

```java
public final class OrderBatch implements Iterable<Order> {

    private final List<Order> orders;

    @Override
    public Iterator<Order> iterator() { return orders.iterator(); }
}
```

## 23.12 `PriorityQueue` va `PriorityBlockingQueue` (Priority Queue)

Ustuvor navbat (priority queue) har bir elementga kalit biriktiradi va keyingi element shu kalit bo'yicha tanlanadi: `offer` qo'shadi, `peek` eng ustuvorini ko'rsatadi, `poll` esa uni olib chiqadi (CLRS, 6.5, 162-bet). Java'dagi ikki implementatsiya `PriorityQueue` va `PriorityBlockingQueue` heap ustiga qurilgan, shuning uchun narxi ham shu: heap `n` elementli to'plamda istalgan ustuvor navbat operatsiyasini `O(log n)` vaqtda bajaradi, eng ustuvorini o'qish esa `Theta(1)` (CLRS, 6.5, 163-165-betlar).

`PriorityQueue` dinamik: boshlang'ich sig'imi 11 va element qo'shilgan sayin sig'im avtomatik o'sadi. Komparator berilmasa tur uchun tabiiy tartib ishlatiladi va navbat boshida eng kichik qiymat turadi; boshqa tartib kerak bo'lsa u konstruktorda oshkor beriladi (Schildt, 19-bob).

Asosiy tuzoq esa tartibda. Navbatni iterator bilan aylanib chiqish mumkin, lekin o'sha iteratsiyaning tartibi aniqlanmagan; to'g'ri ishlatish `offer` va `poll` orqali boradi (Schildt, 19-bob). Ya'ni saralangan tartibni faqat `poll` ketma-ketligi beradi. `toString`, `forEach`, `stream` va `new ArrayList<>(queue)` saralanmagan tartibni beradi, va faqat birinchi element (`peek`) kafolatlangan. Bu xato ayniqsa log va testda uchraydi, chunki ikkalasi ham navbatni `toString` bilan ko'rsatadi.

```java
PriorityQueue<Job> queue = new PriorityQueue<>(comparingInt(Job::priority));
queue.addAll(jobs);

// yomon: iteratsiya tartibi aniqlanmagan, faqat peek() kafolatlangan
List<Job> wrong = new ArrayList<>(queue);
log.info("navbat: {}", queue);                 // toString ham saralanmagan

// yaxshi: tartib kerak bo'lsa poll() bilan bo'shatiladi
List<Job> order = new ArrayList<>(queue.size());
for (Job job = queue.poll(); job != null; job = queue.poll()) {
    order.add(job);
}

// yaxshi: navbat kerak bo'lmasa, saralangan ro'yxat oshkor quriladi
List<Job> sorted = jobs.stream().sorted(comparingInt(Job::priority)).toList();
```

Ikkinchi qoida: navbat tur sifatida faqat "keyingisini ol" namunasi uchun tanlanadi. Hamma element baribir kerak bo'lsa, oshkor `sorted()` yoki `TreeSet` aniqroq shartnoma beradi, chunki ularning iteratsiya tartibi saralangan.

`PriorityBlockingQueue` xuddi shu semantikaning thread-safe variantidir: u ustuvorlik bo'yicha tartiblangan navbat va elementlarni FIFO dan boshqa tartibda ishlash kerak bo'lganda ishlatiladi, boshqa saralangan to'plamlar kabi tabiiy tartib (`Comparable`) yoki `Comparator` bilan solishtiradi (Goetz, 5.3, 57-bet). Thread pool ga navbat sifatida berilsa, vazifalar kelish tartibida emas, ustuvorlik bo'yicha boshlanadi (Goetz, 8.3.2, 108-bet). Iteratsiya tartibi haqidagi tuzoq bu yerda ham o'zgarmaydi. Navbatni arxitektura darajasida ishlatish, broker prioriteti va starvation xavfi [prioritetli navbat](../patterns/17-resilience-va-cloud-dizayn-patternlari.md#1719-prioritetli-navbat-priority-queue) patternida.

```java
// Ustuvor vazifa navbati: tartibni faqat poll() beradi, log da esa size()
private final BlockingQueue<Job> inbox =
        new PriorityBlockingQueue<>(64, comparingInt(Job::priority));

@Scheduled(fixedDelay = 100)
void drain() throws InterruptedException {
    Job job = inbox.poll(50, TimeUnit.MILLISECONDS);   // ustuvorlik tartibida
    if (job != null) {
        handler.handle(job);
    }
    log.debug("navbat chuqurligi: {}", inbox.size());  // iteratsiya emas, size()
}
```

Uchinchi qoida sig'imga tegishli: ustuvor navbatning sig'imi avtomatik o'sadi, ya'ni konstruktordagi raqam chegara emas, boshlang'ich hajm. Iste'molchi yetib keladi deb navbatga chegara qo'ymaslik tizimni keyinroq qayta qurishga buyruq bo'ladi (Goetz, 5.3, 57-bet), shuning uchun chegara navbat turida emas, qabul qilish joyida yoziladi.

## 23.13 Massiv bilan ishlash: chegara, qidiruv va `toArray`

Massiv `List` dan arzonroq ko'rinadi va shu sababli yangi kodda ham
paydo bo'ladi. Uning to'rt chegarasi bor, va ularning hammasi
kompilyatorda emas, ish vaqtida yoki natijada ko'rinadi.

**Massiv yozuv emas.** Massiv tartibdagi **o'xshash** obyektlar to'plami
uchun: hamma element bir xil ma'noga ega bo'lishi kerak. Elementlar
boshqa-boshqa narsalarni bildirsa ("nol element - ism, birinchi element -
telefon"), bu joylashuv kelishuvi hech kimning esida qolmaydi. Obyekt
yoki `record` shu ma'lumotni maydon nomi bilan o'zi tashiydi.

```java
// yomon: joylashuv kelishuvi - [0] nima, [1] nima?
String[] customer = {"Aziza", "+998901234567"};
send(customer[1]);

// yaxshi: nom ma'lumotning o'zida
record Customer(String name, String phone) { }
send(customer.phone());
```

**Indeks `int`, chegara `2^31-1`.** Massiv indeksi `int` bo'lishi shart:
`long` indeks kompilyatsiya xatosi beradi, ya'ni Java massivi `2^31-1`
elementdan katta bo'la olmaydi. Har murojaat ish vaqtida tekshiriladi va
chegaradan chiqsa `ArrayIndexOutOfBoundsException` chiqadi. Amaliy
xulosa: katta ma'lumotni bitta massivda saqlash yo'li yo'q, uni
bo'laklash yoki off-heap tuzilmaga chiqarish kerak. `Collection` ning
`size()` chegarasi ham shu sababdan keladi (24.9).

**Ikkilik qidiruv saralanganlikni talab qiladi.** `Arrays.binarySearch`
ga saralanmagan massiv berilsa natija **aniqlanmagan** bo'ladi: istisno
chiqmaydi, metod shunchaki noto'g'ri indeks yoki "topilmadi" qaytaradi.
Bu nosozlikning eng yomon turi, chunki test ma'lumoti tasodifan
saralangan bo'lsa u ko'rinmaydi. Shuning uchun qidiruv shaklini tanlash
oshkor qaror bo'ladi: kichik yoki saralanmagan massivda chiziqli
qidiruv, saralangan massivda ikkilik qidiruv, saralash narxi esa
qidiruvlar soniga taqsimlanadi.

```java
// yomon: saralanmagan massivda binarySearch - natija aniqlanmagan
int[] codes = {30, 10, 20};
int index = Arrays.binarySearch(codes, 20);    // kafolat yo'q

// yaxshi: oldin saralash, keyin qidirish
int[] codes = {30, 10, 20};
Arrays.sort(codes);
int index = Arrays.binarySearch(codes, 20);
```

**`toArray` ga kichik massiv berilmaydi.** `Collection.toArray(T[])` ga
ro'yxatdan kichik massiv berilsa, metod istisno tashlamaydi: u kerakli
o'lchamda **yangi** massiv yaratadi va uzatilgan massiv o'zgarmagan
holda qoladi. Natijani qaytish qiymatidan emas, uzatilgan massivdan
o'qiydigan kod shu sababli jim bo'sh ma'lumot bilan ishlaydi. Qoida:
`toArray(new T[0])` yozish va natijani qaytish qiymatidan olish.

```java
// yomon: uzatilgan massiv to'ldirilmaydi, natija e'tiborsiz qoldirilgan
Order[] target = new Order[1];
orders.toArray(target);              // orders da 5 element bo'lsa target hamon bo'sh

// yaxshi: o'lchamni metod o'zi hal qiladi, natija qaytish qiymatida
Order[] all = orders.toArray(new Order[0]);
```

## 23.14 Amalda qo'llash

- [ ] `containsKey` + `get` + `put` namunalarini `computeIfAbsent`, `merge`, `getOrDefault` ga o'tkazing.
- [ ] `Collectors.toMap` ning ikki argumentli shakllarini topib, birlashtirish funksiyasini oshkor qo'shing.
- [ ] `HashMap`/`HashSet` tartibiga bog'langan mantiq va testlarni topib, `LinkedHashMap` yoki oshkor saralashga o'tkazing.
- [ ] `Arrays.asList` ishlatilgan joylarni niyatga qarab `List.of` yoki `new ArrayList<>` ga almashtiring.
- [ ] Xom generik turlarni (`List`, `Map` parametrsiz) topib, tur parametrlarini qo'shing.
- [ ] `@SuppressWarnings` larni ko'rib, qamrovini torroq qilib, sababini izohlang.
- [ ] Public API dagi massiv qaytaradigan metodlarni `List` ga o'tkazing.
- [ ] To'plam qaytaradigan getter larni 23.11 jadvaliga qarab bitta izchil shaklga keltiring.
- [ ] `PriorityQueue` va `PriorityBlockingQueue` ishlatilgan joylarni toping: iteratsiya, `toString`, `stream` yoki `new ArrayList<>(queue)` orqali tartibga bog'langan kod va testni `poll()` ga yoki oshkor `sorted()` ga o'tkazing.
- [ ] `Arrays.binarySearch` chaqiruvlarini topib, massivning saralanganligi kod yo'lida kafolatlanganini tekshiring.
- [ ] `toArray(T[])` chaqiruvlarini `toArray(new T[0])` shakliga keltirib, natijani qaytish qiymatidan o'qing.
- [ ] Joylashuv kelishuviga tayangan `String[]` va `Object[]` larni `record` ga o'tkazing.
- [ ] Bog'liq bo'lmagan tur parametrli generik metodlarni topib, wildcard imzoga keltiring.

## Manbalar

- Jack Shirazi, *Java Performance Tuning*, 2-nashr, O'Reilly, 2003, 11.9-bo'lim ("Finding the Index for Partially Matched Strings") - prefiks bo'yicha qidiruvda hash jadvalni to'liq aylanish narxi, saralangan tuzilma va diapazon qidiruvi (prefiksdan prefiks hamda eng katta belgigacha), `TreeMap` ning yakka kirishda sekinligi, parallel kolleksiyani bitta obyekt orqasiga yashirish va bu yechimning kam o'zgaradigan to'plam uchun mosligi. Bu nusxada barqaror bet raqami yo'q, shuning uchun bo'lim raqami va nomi ko'rsatilgan
- Joshua Bloch, *Effective Java* 3rd, Item 26, 27 - xom tur va `unchecked` ogohlantirish
- Joshua Bloch, *Effective Java* 3rd, Item 28 - massiv o'rniga `List`
- Joshua Bloch, *Effective Java* 3rd, Item 29, 30 - generik tur va generik metod
- Joshua Bloch, *Effective Java* 3rd, Item 31 - chegaralangan wildcard va PECS qoidasi
- Joshua Bloch, *Effective Java* 3rd, Item 33 - tur xavfsiz heterogen konteyner
- Joshua Bloch, *Effective Java* 3rd, Item 64 - obyektga interfeys turi bilan murojaat qilish
- Joshua Bloch, *Effective Java* 3rd, Item 26 - xom tur, `List<Object>` va `List<?>` farqi, sinf literali va `instanceof` dagi istisno
- Joshua Bloch, *Effective Java* 3rd, Item 31 - qaytish turida wildcard ishlatmaslik, bir marta uchragan tur parametrini wildcard bilan almashtirish
- Joshua Bloch, *Effective Java* 3rd, Item 28 - massiv kovariant va reified, generik invariant va o'chiriladigan
- Joshua Bloch, *Effective Java* 3rd, Item 32 - generik va varargs ni birga ishlatish, `@SafeVarargs`
- [Java API, `Collectors.toMap`](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/stream/Collectors.html#toMap(java.util.function.Function,java.util.function.Function)) - takrorlangan kalitda `IllegalStateException`
- Boyarsky/Selikoff, *OCP Java SE 17 Study Guide*, 9-bob (506-507-betlar) - type erasure: `T` ning `Object` ga aylanishi, bitta `.class` fayl qolishi, kompilyatorning cast qo'yishi, eski Java bilan moslik sababi va `chew(List<Object>)` bilan `chew(List<Double>)` ning to'qnashuvi
- Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, Clifford Stein, *Introduction to Algorithms*, 3-nashr, MIT Press, 2009, 6.5-bo'lim (162-165-betlar) - ustuvor navbatning operatsiyalari (`INSERT`, `MAXIMUM`, `EXTRACT-MAX`, `INCREASE-KEY`); heap `n` elementli to'plamda istalgan ustuvor navbat operatsiyasini `O(log n)` da bajarishi, eng ustuvorini o'qish `Theta(1)` bo'lishi
- Herbert Schildt, *Java The Complete Reference*, 11-nashr, McGraw-Hill, 2019, 19-bob (`PriorityQueue` bo'limi) - boshlang'ich sig'im 11 va sig'imning avtomatik o'sishi; komparator berilmasa tabiiy tartib va navbat boshida eng kichik qiymat; iterator bilan aylanish mumkin lekin iteratsiya tartibi aniqlanmagan, to'g'ri ishlatish `offer` va `poll` orqali
- Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley Professional, 5.3-bo'lim (57-bet) - `PriorityBlockingQueue` ustuvorlik bo'yicha tartiblangan navbat ekani, tabiiy tartib yoki `Comparator` bilan solishtirishi; navbatga chegara qo'ymaslikning narxi
- Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley Professional, 8.3.2-bo'lim (108-bet) - FIFO navbat vazifalarni kelish tartibida boshlashi, `PriorityBlockingQueue` esa ustuvorlik bo'yicha
- Joshua Bloch, *Effective Java* 3rd, Item 6 (23-bet) - adapter yoki ko'rinish obyektida backing obyektdan boshqa holat yo'qligi va shu sababli bir nechta adapter yaratishning keraksizligi
- Joshua Bloch, *Effective Java* 3rd, Item 27 (123-bet) - yangi kodda `unchecked conversion` ogohlantirishining ko'pi diamond operatori (`<>`) bilan yo'qolishi
- Joshua Bloch, *Effective Java* 3rd, Item 30 (136-bet) - generik singleton fabrikasi: erasure sababli bitta obyektning har parametrlashtirish uchun qayta berilishi, `Collections.reverseOrder` va `Function.identity` misollari
- Joshua Bloch, *Effective Java* 3rd, Item 31 (145-bet) - `List<?>` ga yozib bo'lmasligi sababli turni ushlaydigan `private` generik yordamchi metod (`swap`/`swapHelper`); barcha `Comparable` va `Comparator` ning iste'molchi ekani va `Comparable<? super T>` shakli
- Joshua Bloch, *Effective Java* 3rd, Item 42 (194-bet) - lambda ishlatiladigan joyda generik turlarni to'g'ri berish talabi: kompilyator tur xulosasini generiklardan oladi, xom turda lambda kompilyatsiya bo'lmaydi
- Joshua Bloch, *Effective Java* 3rd, Item 46 (213-bet) - uch argumentli `toMap` ni `BinaryOperator.maxBy(comparing(...))` bilan va "oxirgi yozuvchi g'alaba qozonadi" siyosati bilan ishlatish
- Joshua Bloch, *Effective Java* 3rd, Item 58 (266-bet) - element guruhini ifodalaydigan turning `Collection` ni amalga oshirmasa ham `Iterable` ni amalga oshirishi
- Joshua Bloch, *Effective Java* 3rd, Item 64 (281-bet) - sinf turi bilan e'lon qilish o'rinli bo'ladigan uch holat (mos interfeysi yo'q value sinf, asoslari sinf bo'lgan framework, interfeysda yo'q qo'shimcha metodga tayanish) va mos interfeys yo'qida eng kam maxsus sinfni tanlash
- *The Java Language Specification, Java SE 25 Edition* (Gosling, Joy, Steele, Bracha, Buckley, Smith, Bierman), 4-bob (78-bet) - tur parametrlari bir-biriga bog'liq bo'lmaganda generik metod yozishning yomon uslub ekani
- *The Java Language Specification, Java SE 25 Edition* (Gosling, Joy, Steele, Bracha, Buckley, Smith, Bierman), 10-bob (415-bet) - massiv indeksining `int` bo'lishi shartligi, `long` indeksning kompilyatsiya xatosi ekani, har murojaatning ish vaqtida tekshirilishi va massiv uzunligining `2^31-1` chegarasi
- Herbert Schildt, *Java The Complete Reference*, 12-nashr, McGraw-Hill, 2022, 3-bob (64-bet) - e'lon qilinayotgan `var` o'zgaruvchining o'z initsializatorida ishlatilmasligi va `var` bilan massiv initsializatori yozilmasligi
- Herbert Schildt, *Java The Complete Reference*, 12-nashr, McGraw-Hill, 2022, 14-bob (387-bet) - statik a'zoning o'rab turgan sinf tur parametrini ishlatmasligi va statik generik metod shakli
- Herbert Schildt, *Java The Complete Reference*, 12-nashr, McGraw-Hill, 2022, 20-bob (629-bet) - `Collections.checkedList` va `checkedMap` ning ish vaqtida tur mosligini tekshiradigan ko'rinish berishi
- Martin Fowler, *Refactoring*, 1-nashr, Addison-Wesley, 1999, 8-bob (150-bet) - Replace Array with Object: massiv tartibdagi o'xshash obyektlar to'plami uchun ekani va joylashuv kelishuvlarining esda qolmasligi
- Paul Deitel va Harvey Deitel, *Java How to Program*, 10-nashr, Pearson, 7-bob (287-bet) - `Arrays.binarySearch` ga saralanmagan massiv berilganda natijaning aniqlanmagan bo'lishi
- Paul Deitel va Harvey Deitel, *Java How to Program*, 10-nashr, Pearson, 16-bob (696-bet) - `toArray` ga ro'yxatdan kichik massiv berishning mantiq xatosi ekani
- Y. Daniel Liang, *Introduction to Java Programming*, 9-nashr, Pearson, 2013, 6-bob (248-bet) - chiziqli qidiruv kichik yoki saralanmagan massiv uchun, ikkilik qidiruv saralangan massiv talab qilishi
- Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, Clifford Stein, *Introduction to Algorithms*, 3-nashr, MIT Press, 2009, 11-bob (259-bet) - zanjirli hash jadvalida qidiruvning o'rtacha narxi `Theta(1 + alfa)` va `alfa = n/m` yuklanish koeffitsiyentining bitta qidiruvda ko'riladigan element sonini belgilashi
- John Ousterhout, *A Philosophy of Software Design*, 1-nashr, Yaknyam Press,
  2018, 18.2 - e'lon turi va yaratilgan tur farqining o'quvchini chalg'itishi;
  23.1 dagi ikki pozitsiyani ajratadigan shart shu manba bilan interfeys
  bilan e'lon qilish qoidasini yonma-yon qo'yadi

---

[&larr; 22. Sana, vaqt va mintaqa](22-sana-vaqt-va-mintaqa.md) · [Mundarija](README.md) · [24. Lambda, oqim va funksional uslub tozaligi &rarr;](24-lambda-oqim-va-funksional-uslub-tozaligi.md)
