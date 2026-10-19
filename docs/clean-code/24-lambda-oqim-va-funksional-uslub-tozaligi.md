<!-- doc: clean-code | chapter: 24 | part: VII. Java tilining toza ishlatilishi -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

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


Oqim va sikl tanlovi arxitektor hujjatidagi [Stream API](../architect/13-zamonaviy-java-tili-va-api-dizayni.md#136-stream-api-qachon-foyda-qachon-oddiy-sikl-tushunarliroq) bo'limida, `Optional` ning to'g'ri ishlatilishi esa o'sha bobdagi [Optional ni to'g'ri ishlatish](../architect/13-zamonaviy-java-tili-va-api-dizayni.md#135-optional-ni-togri-ishlatish-qaytish-qiymati-maydon-emas) bo'limida berilgan. Bu bobda funksional kodning tozalik qoidalari: lambda uzunligi, metod havolasi, yon ta'sir, `Collectors` ni o'qiladigan ushlash va istisnolar.

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

Lambda tanasi tashqi qamrovdagi lokal o'zgaruvchini faqat **effectively
final** bo'lsa oladi: o'zgaruvchi e'londan keyin bir marta ham
o'zgartirilmagan bo'lishi kerak, va bu talab lambda ichida ham,
tashqarisida ham amal qiladi. Shuning uchun "lambda ichida hisoblagichni
oshirish" namunasi kompilyatsiyadan o'tmaydi. Kompilyatorni mamnun qilish
uchun hisoblagichni maydonga ko'chirish esa muammoni yechmaydi, yashiradi
(24.4).

```java
// yomon: total effectively final emas - kompilyatsiya xatosi
int total = 0;
rows.forEach(row -> total += row.amount());

// yaxshi: hisob oqimning o'zida qoladi
int total = rows.stream().mapToInt(SettlementRow::amount).sum();
```

Qolgan ikki qoida lambdaning o'qilishiga tegishli. Birinchisi: **lambda
parametrlarining turlari yozilmaydi**, agar ularning borligi kodni
aniqroq qilmasa; kompilyator turni tur xulosasi bilan topadi, yozilgan
tur esa faqat qatorni uzaytiradi. Ikkinchisi shundan kelib chiqadi:
turlar ko'rinmaganidan keyin o'qilish butunlay **nomga** tayanadi,
shuning uchun oqim quvurida lambda parametrini ehtiyotkorlik bilan
nomlash majburiy, `x`, `a`, `t` kabi harflar bilan emas.

```java
// yomon: tur ortiqcha, nom hech narsa aytmaydi
.filter((Payment p) -> p.isSettled())
.map((Payment x) -> x.amount())

// yaxshi: tur xulosa qilinadi, nom domen nomi
.filter(payment -> payment.isSettled())
.map(Payment::amount)
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

Metod havolasining besh turi bor va ularni nom bilan bilish review da
foyda beradi, chunki noaniqlik ko'pincha turlarni aralashtirishdan
chiqadi.

| Tur | Shakl | Misol |
|---|---|---|
| Statik | `Sinf::statikMetod` | `Integer::parseInt` |
| Bog'langan (bound) nusxa | `obyekt::metod` | `payment::amount` |
| Bog'lanmagan (unbound) nusxa | `Sinf::nusxaMetodi` | `Payment::amount` |
| Sinf konstruktori | `Sinf::new` | `ArrayList::new` |
| Massiv konstruktori | `Tur[]::new` | `String[]::new` |

Bog'langan va bog'lanmagan shakl bir xil ko'rinadi, lekin birinchisida
obyekt allaqachon tanlangan, ikkinchisida obyekt birinchi argument bo'lib
keladi. Aynan shu farq `map(Payment::amount)` ni ishlatadi va
`map(payment::amount)` ni xato qiladi.

Teskari tomoni ham bor: metod havolasi har doim qisqaroq degani emas.
`Function.identity()` o'rniga `x -> x` yoziladi, chunki u qisqaroq va
tozaroq; `identity()` nomi qo'shimcha ma'no bermaydi.

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

Standart turlardan foydalanishning ikki qoidasi bor. Birinchisi: **boxed
primitiv bilan asosiy funksional interfeysni ishlatmaslik**, primitiv
variantini olish. `Function<Integer, Integer>` emas `IntUnaryOperator`,
`Predicate<Long>` emas `LongPredicate`. Ommaviy amalda har element uchun
boxing va unboxing qilinadi, va bu narx jadvaldagi "primitiv variantlar"
qatorining butun sababi (20.6).

Ikkinchisi o'z interfeysingizga tegishli: **hamisha
`@FunctionalInterface` qo'yiladi.** U uch ish qiladi: o'quvchiga interfeys
lambda uchun mo'ljallanganini aytadi, bitta abstrakt metod shartini
kompilyatorga majburlatadi, va keyinchalik kimdir tasodifan ikkinchi
abstrakt metod qo'shishini to'sadi.

```java
@FunctionalInterface
public interface TaxPolicy {
    Money taxFor(Region region, Money net);
}
```

Lambdaning o'zi haqida bitta mexanik chegara: **lambda generic bo'la
olmaydi**, ya'ni unga tur parametri yozilmaydi. Generiklik lambdada emas,
u amalga oshiradigan funksional interfeysda beriladi, shuning uchun o'z
funksional interfeysingizni yozganda tur parametri interfeys e'lonida
turadi.

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

**Oqim manbasini quvur qurilgandan keyin o'zgartirish natijaga ta'sir qiladi.** Yon ta'sirning ikkinchi, kamroq tanilgan shakli - manbaga tegish. Stream kechiktirib bajariladi: `collection.stream()` chaqiruvi hech narsa o'qimaydi, faqat ma'lumotni kerak bo'lganda qayerdan izlashni biladigan obyekt yaratadi. Shuning uchun manba kolleksiya `stream()` dan **keyin**, lekin terminal operatsiyadan **oldin** o'zgartirilsa, o'zgarish natijaga kiradi.

```java
var cats = new ArrayList<String>();
cats.add("Annie");
cats.add("Ripley");
var stream = cats.stream();      // hech narsa o'qilmaydi
cats.add("KC");                  // quvur qurilgandan keyin qo'shildi
System.out.println(stream.count());   // 3, 2 emas
```

Bu xatti-harakat JDK hujjatida **non-interference** talabi sifatida yozilgan: quvur bajarilayotganda manbani o'zgartirish `ConcurrentModificationException` yoki yanada yomoni jim noto'g'ri natija beradi. Yuqoridagi misol qonuniy, chunki o'zgarish terminal operatsiyadan oldin sodir bo'lgan, lekin kodni o'qigan odam buni kutmaydi. Qoida: **`stream()` chaqiruvi va terminal operatsiya bitta ifodada tursin**, oraliq `Stream` o'zgaruvchiga saqlanmasin. Saqlash kerak bo'lgan hollarda (quvurni bosqichma-bosqich qurish) manba o'zgarmas bo'lsin: `List.copyOf(cats).stream()`.

Yon ta'sirning uchinchi shakli lambdaning capture qoidasidan chiqadi va u
ayniqsa jim. Lambda tashqi qamrovdagi lokal o'zgaruvchini faqat
effectively final bo'lsa oladi (24.1), lekin tashqi sinfning **nusxa va
statik maydonini** o'qiy ham, o'zgartira ham oladi: maydonga capture
cheklovi qo'yilmagan. Natijada "hisoblagich lokal o'zgaruvchi bo'lganda
kompilyatsiya bo'lmadi, maydon qilib qo'ydim" degan tuzatish kompilyatorni
mamnun qiladi va muammoni kattalashtiradi. Lokal o'zgaruvchi bitta metod
ichida qolardi, maydon esa butun obyekt bo'ylab umumiy o'zgaradigan
holat: parallel oqimda poyga holati, ketma-ket oqimda esa oldingi
chaqiruvdan qolgan qiymat.

```java
// yomon: capture cheklovini maydon bilan chetlab o'tish - jim umumiy holat
private int processed;

void run(List<Order> orders) {
    orders.forEach(order -> processed++);   // kompilyatsiya bo'ladi, thread-safe emas
}

// yaxshi: hisob natija bo'lib qaytadi
long processed = orders.stream().filter(this::process).count();
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

Parallel oqim foyda beradigan shart ham aniq va u manbaga bog'liq: `ArrayList`, `HashMap`, `HashSet`, `ConcurrentHashMap`, massiv, `int` va `long` oraliqlari. Ularning umumiy xususiyati ikkita: ular kerakli o'lchamdagi bo'laklarga arzon va aniq bo'linadi (buni `spliterator` bajaradi) va ketma-ket o'qilganda havolalar xotirada yonma-yon yotadi. Teskari tomoni: `Stream.iterate` va `limit` bilan qurilgan oqim parallelda yomon ishlaydi, chunki uni bo'lib bo'lmaydi.

Terminal amal ham ahamiyatli: parallel uchun eng mos amallar reduksiyalar (`reduce`, `min`, `max`, `count`, `sum`). `collect` esa to'plamni qo'shib yurishni talab qiladi, shuning uchun parallelda qimmat. Ya'ni parallel oqim qarori uch savolga javob bo'ladi: manba bo'linadimi, terminal amal reduksiyami, va o'lchov haqiqatda foyda ko'rsatdimi.

Oraliq amallarning ikki toifasi ham shu qarorga kiradi. Holatsiz oraliq
amal (`filter`, `map`) har elementni mustaqil ko'radi, shuning uchun uni
bo'laklarga bo'lish bepul. Holatli oraliq amal (`sorted`, `distinct`)
esa oldingi barcha oraliq amal tugashini talab qiladi va parallel oqimda
butun oqimni buferlaydi: quvurning o'rtasidagi bitta `sorted`
parallellashtirishning foydasini yo'qotishi mumkin.

Parallellashtirishning narxi faqat tezlikda emas, **to'g'rilikda** ham:
noto'g'ri funksiya berilgan parallel oqim sekin ishlamaydi, noto'g'ri
natija beradi, va bu natija har ishga tushishda boshqacha bo'ladi. Shuning
uchun `reduce` ga uzatilgan akkumulyator va birlashtirgich uchta shartni
qanoatlantirishi shart:

- **holatsiz (stateless)** - natija faqat argumentlarga bog'liq, hech
  qanday tashqi holatni o'qimaydi va yozmaydi;
- **aralashmaydigan (non-interfering)** - quvur bajarilayotganda manbani
  o'zgartirmaydi (24.4);
- **assotsiativ** - `(a op b) op c` va `a op (b op c)` bir xil natija
  beradi, chunki bo'laklarning birlashtirilish tartibi aniqlanmagan.

Uchta shart ketma-ket oqim uchun ham yozilgan, lekin ketma-ket oqimda
ularning buzilishi ko'pincha ko'rinmaydi: assotsiativ bo'lmagan
akkumulyator bitta threadda barqaror natija berib turadi va faqat
`parallel()` qo'shilganda sinadi.

```java
// yomon: ayirish assotsiativ emas - parallelda natija har xil chiqadi
int result = numbers.parallelStream().reduce(0, (a, b) -> a - b);

// yomon: holatli akkumulyator - tashqi obyektni o'zgartiradi
StringBuilder all = new StringBuilder();
String joined = words.parallelStream()
        .reduce("", (acc, word) -> { all.append(word); return acc + word; });

// yaxshi: assotsiativ va holatsiz
int result = numbers.parallelStream().reduce(0, Integer::sum);
```

Oxirgi qoida o'z turlaringizga tegishli: `Stream`, `Iterable` yoki
`Collection` ning o'z implementatsiyasi parallelda yaxshi ishlashi kerak
bo'lsa, `spliterator` metodini override qilish va parallel ishlashni
**o'lchash** shart. Standart `spliterator` sizning manbangiz qanday
bo'linishini bilmaydi, shuning uchun u bo'laklarni teng qilmaydi va
parallellashtirish foyda bermaydi.

Parallel oqim ichida tasodifiy son kerak bo'lsa, generator tanlovi
alohida qaror: bitta thread uchun `ThreadLocalRandom`, bo'linadigan
parallel oqim yoki fork-join uchun `SplittableRandom`; `Random` faqat
eski kodda qoladi ([tasodifiy son
generatsiyasi](20-primitiv-son-va-pul.md#208-tasodifiy-son-uuid-va-identifikator-generatsiyasi)).

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

`Optional` ni nega umuman tanlash kerak, degan savol ham shu yerga
tegishli, chunki u `null` bilan taqqoslashni hal qiladi: `Optional`
**tekshiriladigan istisnoga ruhan o'xshaydi**. U API foydalanuvchisini
qiymat qaytmasligi ehtimoliga qarashga majbur qiladi, chunki qiymatga
yetish uchun o'ramni ochish kerak. `null` qaytarish va tekshirilmaydigan
istisno tashlash esa buni e'tiborsiz qoldirishga yo'l qoldiradi va
nosozlik chaqiruv joyidan uzoqda chiqadi.

Ikki mexanik qoida zanjirni qisqartiradi. Birinchisi: **boxed primitivni
o'ragan `Optional` hech qachon qaytarilmaydi**, chunki u ikki qatlam
o'ram beradi (`Optional` ning o'zi va boxing); `OptionalInt`,
`OptionalLong`, `OptionalDouble` ishlatiladi. Ikkinchisi: Java 9 dan
`Optional.stream()` bor, ya'ni `Stream<Optional<T>>` ni `Stream<T>` ga
aylantirish uchun ikki bosqichli filtr kerak emas.

```java
// yomon: ikki bosqich va get()
Stream<Order> found = ids.stream()
        .map(repository::findById)
        .filter(Optional::isPresent)
        .map(Optional::get);

// yaxshi: bitta flatMap
Stream<Order> found = ids.stream()
        .map(repository::findById)
        .flatMap(Optional::stream);
```

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

`groupingBy` ning jim xulqi haqida ikki tafsilot bor va ikkisi ham enum
kalit bilan chiqadi. Birinchisi: `groupingBy` qaytaradigan xarita
implementatsiyasini **o'zi tanlaydi** va u `EnumMap` bo'lmaydi; `EnumMap`
kerak bo'lsa uch parametrli shakl ishlatiladi, bunda ikkinchi argument
xarita fabrikasi (`mapFactory`). Ikkinchisi: `groupingBy` faqat **mavjud
kalitlar** uchun yozuv yaratadi, qo'lda to'ldirilgan `EnumMap` esa barcha
kalitlar uchun. Ya'ni ikki shakl bir xil ko'rinadi, lekin elementi
bo'lmagan guruh so'ralganda biri `null`, ikkinchisi bo'sh ro'yxat beradi.

```java
// yaxshi: xarita fabrikasi oshkor - natija EnumMap, tartib enum e'loni bo'yicha
Map<Status, List<Payment>> byStatus = payments.stream()
        .collect(groupingBy(Payment::status,
                () -> new EnumMap<>(Status.class),
                toList()));
```

Oraliq tur haqidagi yuqoridagi qoidaning chegarasi ham bor va u
adabiyotda qarama-qarshi aytilgan: Bloch quvur ichida juft obyekt
yasashni qoniqarsiz deb ataydi va buning o'rniga **mappingni teskari
aylantirishni** tavsiya qiladi. Ikkisini ajratadigan shart oraliq turning
roliga qaraydi.

| Holat | Yechim |
|---|---|
| Oraliq tur agregatsiya KALITI bo'ladi (region va valyuta juftligi bo'yicha guruhlash) | oraliq `record`: kalit nom oladi, `equals` va `hashCode` ni tekin beradi |
| Quvurning oldingi bosqichidagi QIYMATGA qaytish kerak (eng ko'p sotilgan mahsulot nomi, lekin solishtirish soni bo'yicha) | mappingni teskari aylantirish: kalit va qiymat almashtiriladi, natija `Collectors.maxBy` yoki `toMap` ning merge funksiyasi bilan olinadi |

Ya'ni oraliq tur yangi kalit yaratganda haqli. U faqat yo'qolgan qiymatni
quvur bo'ylab tashib yurish uchun yasalsa, teskari mapping qisqaroq va
qo'shimcha tur qoldirmaydi.

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

Jadvalning `Iterable<T>` qatori bitta tafsilotni yashiradi: JDK `Stream`
ni `for-each` da ishlatish yo'lini bermaydi. `Stream` da `iterator()`
metodi bor, lekin `Stream` `Iterable` ni amalga oshirmaydi, shuning uchun
`for-each` uchun adapter metod yoziladi. Metod havolasini `Iterable` ga
cast qilish shakli ham ishlaydi (`(Iterable<Payment>)
payments::iterator`), lekin u amalda o'qilmaydi va review da savol
tug'diradi.

```java
// Adapter: Stream ni for-each da ishlatish uchun
public static <T> Iterable<T> iterableOf(Stream<T> stream) {
    return stream::iterator;
}

for (Payment payment : iterableOf(service.streamSettledIn(range))) { ... }
```

`Collection` ni qaytish turi qilishning chegarasi katta ketma-ketlikda
chiqadi: `Collection.size()` `int` qaytaradi, demak qaytarilgan
ketma-ketlik uzunligi `Integer.MAX_VALUE` dan oshmaydi. Shundan kattasi
kerak bo'lsa yoki hajm oldindan noma'lum bo'lsa, `Stream` va `Iterable`
qoladi.

## 24.10 Amalda qo'llash

- [ ] Uch qatordan uzun lambdalarni topib, nomlangan metodlarga chiqaring.
- [ ] Oqim ichida tashqi to'plamga yozadigan `forEach` larni `map`/`collect` ga o'tkazing.
- [ ] `peek` ishlatilgan joylarni mantiqdan olib tashlang yoki log uchun oshkor metodga aylantiring.
- [ ] `parallelStream` chaqiruvlarini ko'rib, I/O bo'lsa oshkor executor ga, o'lchovsiz bo'lsa ketma-ket oqimga qaytaring.
- [ ] `isPresent()` + `get()` namunalarini `map`/`orElseGet`/`orElseThrow` zanjiriga aylantiring.
- [ ] `orElse(<qimmat chaqiruv>)` holatlarini `orElseGet` ga o'tkazing.
- [ ] `@SneakyThrows` ishlatilgan joylarni oshkor o'rashga almashtirib, annotatsiyani taqiqlang.
- [ ] Ikki darajadan chuqur `groupingBy` zanjirlarini oraliq record bilan tekislang.
- [ ] Enum kalit bo'yicha `groupingBy` chaqiruvlarini topib, `EnumMap` kerak bo'lsa `mapFactory` shaklini qo'ying.
- [ ] O'z funksional interfeyslaringizga `@FunctionalInterface` qo'yib, boxed primitiv parametrlarini primitiv variantga o'tkazing.
- [ ] `parallelStream` ichidagi `reduce` va `collect` funksiyalarini uch shart bo'yicha tekshiring: holatsiz, aralashmaydigan, assotsiativ.
- [ ] `filter(Optional::isPresent).map(Optional::get)` namunalarini `flatMap(Optional::stream)` ga almashtiring.

## Manbalar

- Boyarsky/Selikoff, *OCP Java SE 17 Study Guide*, 10-bob (565-bet) - stream ning kechiktirib bajarilishi: `stream()` chaqiruvi ma'lumotni o'qimasligi, manba kolleksiya quvur qurilgandan keyin va terminal operatsiyadan oldin o'zgartirilsa o'zgarish natijaga kirishi
- Joshua Bloch, *Effective Java* 3rd, Item 42 - anonim sinf o'rniga lambda, lambdaning uzunligi
- Joshua Bloch, *Effective Java* 3rd, Item 43 - metod havolasi qachon o'qiladi
- Joshua Bloch, *Effective Java* 3rd, Item 44 - standart funksional interfeyslardan foydalanish
- Joshua Bloch, *Effective Java* 3rd, Item 45, 46 - oqimni o'lchov bilan ishlatish, yon ta'sirsiz funksiyalar
- Joshua Bloch, *Effective Java* 3rd, Item 47 - qaytish turi sifatida `Stream` emas `Collection`
- Joshua Bloch, *Effective Java* 3rd, Item 48 - parallel oqim: qaysi manba bo'linadi, qaysi terminal amal mos keladi
- Joshua Bloch, *Effective Java* 3rd, Item 55 - `Optional` ni o'rinli qaytarish
- Joshua Bloch, *Effective Java* 3rd, Item 42 (194-bet) - lambda parametrlarining turlarini yozmaslik
- Joshua Bloch, *Effective Java* 3rd, Item 43 (198-bet) - metod havolasining besh turi (statik, bog'langan nusxa, bog'lanmagan nusxa, sinf konstruktori, massiv konstruktori); `Function.identity()` o'rniga `x -> x`
- Joshua Bloch, *Effective Java* 3rd, Item 44 (201-202-betlar) - boxed primitiv bilan asosiy funksional interfeysni ishlatmaslik; `@FunctionalInterface` ning uch vazifasi
- Joshua Bloch, *Effective Java* 3rd, Item 45 (206-207-betlar) - oqim quvurida lambda parametrlarini ehtiyotkorlik bilan nomlash; oldingi bosqich qiymatiga qaytish uchun mappingni teskari aylantirish
- Joshua Bloch, *Effective Java* 3rd, Item 37 (173-bet) - `groupingBy` ning xarita implementatsiyasini o'zi tanlashi va `mapFactory` shakli; `groupingBy` faqat mavjud kalitlar uchun yozuv yaratishi
- Joshua Bloch, *Effective Java* 3rd, Item 47 (217, 219-betlar) - `Stream` ni `for-each` da ishlatish uchun adapter metod; `Collection.size()` ning `int` qaytarishi va `Integer.MAX_VALUE` chegarasi
- Joshua Bloch, *Effective Java* 3rd, Item 48 (223-224-betlar) - parallellashtirishning xavfsizlik nosozligi va `reduce` funksiyalariga qo'yilgan uch talab; o'z `Stream`, `Iterable` yoki `Collection` implementatsiyasida `spliterator` ni override qilish va o'lchash
- Joshua Bloch, *Effective Java* 3rd, Item 55 (250, 252-253-betlar) - `Optional` ning tekshiriladigan istisnoga ruhan o'xshashligi; `Optional.stream()` va `flatMap` ko'prigi; boxed primitiv o'rniga `OptionalInt`, `OptionalLong`, `OptionalDouble`
- Herbert Schildt, *Java The Complete Reference*, 12-nashr, McGraw-Hill, 2022, 15-bob (399, 405-406-betlar) - lambda faqat effectively final lokal o'zgaruvchini olishi; lambdaning tashqi sinf nusxa va statik maydonini o'qib ham, o'zgartira ham olishi; lambdaning o'zi generic bo'la olmasligi
- Herbert Schildt, *Java The Complete Reference*, 12-nashr, McGraw-Hill, 2022, 30-bob (1014-bet) - `reduce` akkumulyatori uchun holatsiz, aralashmaydigan va assotsiativ bo'lish talabi
- Paul Deitel va Harvey Deitel, *Java How to Program*, 10-nashr, Pearson, 17-bob (742-bet) - holatli oraliq amalning oldingi oraliq amallar tugashini talab qilishi va parallel oqimda butun oqimni buferlashi
- [Java API, `Stream.peek`](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/stream/Stream.html#peek(java.util.function.Consumer)) - debug uchun mo'ljallangani va chaqirilmasligi mumkinligi

---

[&larr; 23. To'plamlar va generiklar gigiyenasi](23-toplamlar-va-generiklar-gigiyenasi.md) · [Mundarija](README.md) · [25. Java kodidagi umumiy tuzoqlar &rarr;](25-java-kodidagi-umumiy-tuzoqlar.md)
