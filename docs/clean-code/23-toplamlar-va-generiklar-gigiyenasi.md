<!-- doc: clean-code | chapter: 23 | part: VII. Java tilining toza ishlatilishi -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: tekshirilmoqda. Da'volar hali manbaga solishtirilmoqda.

# 23. To'plamlar va generiklar gigiyenasi (Collections and Generics)

<details>
<summary>Bu bobdagi 13 bo'lim</summary>

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
- [23.13 Amalda qo'llash](#2313-amalda-qollash)

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

Uchta o'xshash shaklni ajratish kerak, chunki ular bir xil emas. Xom `List` tur tekshiruvidan butunlay chiqadi. `List<Object>` esa tur xavfsiz: unga har qanday obyekt qo'yiladi, lekin u `List<String>` ni qabul qilmaydi (generiklar invariant). `List<?>` - chegarasiz wildcard: unga `null` dan boshqa narsa qo'shilmaydi, lekin har qanday `List<...>` ni qabul qiladi, shuning uchun "ichidagi tur menga ahamiyatsiz, faqat o'qiyman" degan joyda aynan shu yoziladi.

```java
void countAll(List raw) { }            // yomon: tur tekshiruvi yo'q
void countAll(List<Object> any) { }    // List<String> ni QABUL QILMAYDI
void countAll(List<?> any) { }         // yaxshi: har qanday ro'yxatni oladi, yozib bo'lmaydi
```

Xom tur haqli bo'lgan ikki joy bor va ikkisi ham tur ma'lumoti ish vaqtida yo'qolishidan kelib chiqadi: sinf literali (`List.class`, `List<String>.class` yo'q) va `instanceof` (`o instanceof Set` yoziladi, keyin `Set<?>` ga cast qilinadi).

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

Ikkinchi amaliy qoida imzoni soddalashtiradi: tur parametri metod e'lonida **faqat bir marta** uchrasa, uni wildcard bilan almashtiring. Bir marta uchragan `<E>` hech narsani bog'lamaydi, ya'ni u chaqiruvchiga ham, tanaga ham foyda bermaydi, faqat imzoni uzaytiradi.

```java
// ortiqcha: E bir marta uchraydi
static <E> void swapNothing(List<E> list) { }

// yaxshi: wildcard yetadi
static void swapNothing(List<?> list) { }
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

## 23.13 Amalda qo'llash

- [ ] `containsKey` + `get` + `put` namunalarini `computeIfAbsent`, `merge`, `getOrDefault` ga o'tkazing.
- [ ] `Collectors.toMap` ning ikki argumentli shakllarini topib, birlashtirish funksiyasini oshkor qo'shing.
- [ ] `HashMap`/`HashSet` tartibiga bog'langan mantiq va testlarni topib, `LinkedHashMap` yoki oshkor saralashga o'tkazing.
- [ ] `Arrays.asList` ishlatilgan joylarni niyatga qarab `List.of` yoki `new ArrayList<>` ga almashtiring.
- [ ] Xom generik turlarni (`List`, `Map` parametrsiz) topib, tur parametrlarini qo'shing.
- [ ] `@SuppressWarnings` larni ko'rib, qamrovini torroq qilib, sababini izohlang.
- [ ] Public API dagi massiv qaytaradigan metodlarni `List` ga o'tkazing.
- [ ] To'plam qaytaradigan getter larni 23.11 jadvaliga qarab bitta izchil shaklga keltiring.
- [ ] `PriorityQueue` va `PriorityBlockingQueue` ishlatilgan joylarni toping: iteratsiya, `toString`, `stream` yoki `new ArrayList<>(queue)` orqali tartibga bog'langan kod va testni `poll()` ga yoki oshkor `sorted()` ga o'tkazing.

## Manbalar

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
- Thomas H. Cormen, Charles E. Leiserson, Ronald L. Rivest, Clifford Stein, *Introduction to Algorithms*, 3-nashr, MIT Press, 2009, 6.5-bo'lim (162-165-betlar) - ustuvor navbatning operatsiyalari (`INSERT`, `MAXIMUM`, `EXTRACT-MAX`, `INCREASE-KEY`); heap `n` elementli to'plamda istalgan ustuvor navbat operatsiyasini `O(log n)` da bajarishi, eng ustuvorini o'qish `Theta(1)` bo'lishi
- Herbert Schildt, *Java The Complete Reference*, 11-nashr, McGraw-Hill, 2019, 19-bob (`PriorityQueue` bo'limi) - boshlang'ich sig'im 11 va sig'imning avtomatik o'sishi; komparator berilmasa tabiiy tartib va navbat boshida eng kichik qiymat; iterator bilan aylanish mumkin lekin iteratsiya tartibi aniqlanmagan, to'g'ri ishlatish `offer` va `poll` orqali
- Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley Professional, 5.3-bo'lim (57-bet) - `PriorityBlockingQueue` ustuvorlik bo'yicha tartiblangan navbat ekani, tabiiy tartib yoki `Comparator` bilan solishtirishi; navbatga chegara qo'ymaslikning narxi
- Brian Goetz va boshqalar, *Java Concurrency in Practice*, Addison-Wesley Professional, 8.3.2-bo'lim (108-bet) - FIFO navbat vazifalarni kelish tartibida boshlashi, `PriorityBlockingQueue` esa ustuvorlik bo'yicha
- John Ousterhout, *A Philosophy of Software Design*, 1-nashr, Yaknyam Press,
  2018, 18.2 - e'lon turi va yaratilgan tur farqining o'quvchini chalg'itishi;
  23.1 dagi ikki pozitsiyani ajratadigan shart shu manba bilan interfeys
  bilan e'lon qilish qoidasini yonma-yon qo'yadi

---

[&larr; 22. Sana, vaqt va mintaqa](22-sana-vaqt-va-mintaqa.md) · [Mundarija](README.md) · [24. Lambda, oqim va funksional uslub tozaligi &rarr;](24-lambda-oqim-va-funksional-uslub-tozaligi.md)
