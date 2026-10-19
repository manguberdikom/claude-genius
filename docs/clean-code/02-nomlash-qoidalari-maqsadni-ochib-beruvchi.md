<!-- doc: clean-code | chapter: 2 | part: I. Toza kodning asosi -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 2. Nomlash qoidalari: maqsadni ochib beruvchi nom (Naming: Intention-Revealing Names)

<details>
<summary>Bu bobdagi 19 bo'lim</summary>

- [2.1 Nom javob berishi kerak bo'lgan uchta savol](#21-nom-javob-berishi-kerak-bolgan-uchta-savol)
- [2.2 Yolg'on ma'lumot beradigan nom](#22-yolgon-malumot-beradigan-nom)
- [2.3 Ma'noli farq: `a1`, `a2`, `Info` va `Data`](#23-manoli-farq-a1-a2-info-va-data)
- [2.4 Shovqin so'zlar: `Info`, `Data`, `Object`, `Variable`, `The`](#24-shovqin-sozlar-info-data-object-variable-the)
- [2.5 Talaffuz qilinadigan nom](#25-talaffuz-qilinadigan-nom)
- [2.6 Qidiriladigan nom va bir harfli o'zgaruvchi chegarasi](#26-qidiriladigan-nom-va-bir-harfli-ozgaruvchi-chegarasi)
- [2.7 Kodlash va prefikslar: Hungarian notation, `m_`, `I` prefiksi](#27-kodlash-va-prefikslar-hungarian-notation-m_-i-prefiksi)
- [2.8 Aqliy tarjimani talab qiladigan nom](#28-aqliy-tarjimani-talab-qiladigan-nom)
- [2.9 Sinf nomi ot, metod nomi fe'l, getter konvensiyasi](#29-sinf-nomi-ot-metod-nomi-fel-getter-konvensiyasi)
- [2.10 Hazil, jargon va madaniy havolalar](#210-hazil-jargon-va-madaniy-havolalar)
- [2.11 Bitta tushunchaga bitta so'z](#211-bitta-tushunchaga-bitta-soz)
- [2.12 So'z o'yini qilmaslik](#212-soz-oyini-qilmaslik)
- [2.13 Yechim domeni va muammo domeni nomlari](#213-yechim-domeni-va-muammo-domeni-nomlari)
- [2.14 Kontekst qo'shish va ortiqcha kontekst qo'shmaslik](#214-kontekst-qoshish-va-ortiqcha-kontekst-qoshmaslik)
- [2.15 Nom uzunligi qamrovga mutanosib](#215-nom-uzunligi-qamrovga-mutanosib)
- [2.16 Qisqartma qoidalari va psixologik masofa](#216-qisqartma-qoidalari-va-psixologik-masofa)
- [2.17 Nomga ma'lumot zichlash: aniq so'z va aniq nom](#217-nomga-malumot-zichlash-aniq-soz-va-aniq-nom)
- [2.18 Nomni xato talqinlarga sinash](#218-nomni-xato-talqinlarga-sinash)
- [2.19 Amalda qo'llash](#219-amalda-qollash)

</details>


Nomni domen tilidan olish qoidasi [arxitektor hujjatidagi](../architect/README.md) nomlashni domen tilidan olish bo'limida yoritilgan. Bu bobda qolgan qism: nomning o'zini tekshirish uchun aniq qoidalar to'plami. Har bir qoida bitta aniq xatoni to'sadi va ularning hammasini review paytida bir daqiqada qo'llash mumkin.

## 2.1 Nom javob berishi kerak bo'lgan uchta savol

Yaxshi nom uchta savolga javob beradi: bu nima, nega mavjud, qanday ishlatiladi. Agar nomni ko'rib izoh yozish ehtiyoji tug'ilsa, nom shu uchta savoldan birini javobsiz qoldirgan. Izoh yozish o'rniga nomni o'zgartirish kerak.

```java
// yomon: uchta savolning hammasi javobsiz
int d;          // kunlar
List<int[]> l;  // nima?
boolean f;

// yaxshi: nom o'zi javob beradi, izoh kerak emas
int daysSinceLastPayment;
List<Cell> flaggedCells;
boolean shipmentAlreadyDispatched;
```

Tekshiruv usuli oddiy: nomni ovoz chiqarib o'qib, keyin "bu nima?" deb so'rang. Javob nomning o'zidan kelmasa, nom ishlamaydi.

## 2.2 Yolg'on ma'lumot beradigan nom

Nom noto'g'ri ma'lumot bersa, u yo'q nomdan ham yomon, chunki o'quvchi ishonadi va xato qiladi. Eng ko'p uchraydigan to'rt shakl bor: tur haqida yolg'on (`accountList` aslida `Set`), hajm haqida yolg'on (`cache` aslida bitta qiymat), xatti-harakat haqida yolg'on (`getUser` ichida yozadi), va vaqt haqida yolg'on (`currentBalance` aslida kechagi qoldiq).

```java
// yomon: nom tur haqida yolg'on gapiradi
Map<String, Customer> customerList;
// yomon: nom o'zgartirishni yashiradi
public Order getOrder(Long id) { order.touch(); return order; }

// yaxshi: nom haqiqatni aytadi
Map<CustomerId, Customer> customersById;
public Order findOrder(OrderId id);        // faqat o'qiydi
public Order markOrderSeen(OrderId id);   // o'zgartirishi nomda ko'rinadi
```

Shunga yaqin tuzoq: `l`, `O`, `I` harflari. Ular `1` va `0` bilan aralashadi va hech qanday shriftda ishonchli farqlanmaydi.

Yolg'onning eng qimmat shakli esa standart kutubxona sinfi nomini takrorlash: o'z sinfingizga `System`, `List`, `Date` yoki `Timer` deb nom bermang. Kompilyator bunga ruxsat beradi, lekin shundan keyin bir faylda `java.util.List` ishlab turadi, boshqasida o'z `List` ingiz, va o'quvchi qaysi biri nazarda tutilganini `import` qatoridan izlab topishga majbur bo'ladi. Xato esa `import` o'zgarganda, masalan IDE avtomatik `import` qo'shganda, jim paydo bo'ladi.

## 2.3 Ma'noli farq: `a1`, `a2`, `Info` va `Data`

Kompilyatorni qondirish uchun qo'shilgan farq odam uchun ma'lumot bermaydi. `source` va `destination` farq beradi; `a1` va `a2` bermaydi. `Product`, `ProductInfo` va `ProductData` uchligi esa eng zararli, chunki uchtasi bir xil narsani anglatadi va o'quvchi qaysi birini ishlatishni bilmaydi.

```java
// yomon: farq bor, ma'no yo'q
void copyChars(char[] a1, char[] a2) { ... }
class Product { } class ProductInfo { } class ProductData { }

// yaxshi: farq ma'noli
void copyChars(char[] source, char[] destination) { ... }
class Product { }             // domen entiteti
class ProductSummary { }      // ro'yxat uchun qisqa ko'rinish
class ProductCatalogEntry { } // tashqi katalogdagi yozuv
```

Agar ikkita nom orasidagi farqni bir gapda aytib bera olmasangiz, ikkitasidan biri keraksiz.

## 2.4 Shovqin so'zlar: `Info`, `Data`, `Object`, `Variable`, `The`

Shovqin so'z nomga uzunlik qo'shadi, ma'no qo'shmaydi. `theCustomer` va `customer`, `CustomerObject` va `Customer`, `nameString` va `name` juftliklarida ikkinchisi har doim yaxshiroq. `Manager`, `Helper`, `Util`, `Processor` qo'shimchalari [arxitektor hujjatidagi](../architect/README.md) nomlashni domen tilidan olish bo'limida ko'rilgan; bu yerdagi ro'yxat ularning qolgani.

| Shovqin | Nega keraksiz | Almashtirish |
|---|---|---|
| `Info`, `Data` | hamma narsa ma'lumot | `Summary`, `Snapshot`, `Request` |
| `Object` | tur allaqachon ma'lum | olib tashlash |
| `the`, `a`, `an` | artikl ma'no bermaydi | olib tashlash |
| `nameString` | tur imzoda ko'rinadi | `name` |
| `moneyAmount` | takrorlash | `price`, `fee`, `total` |
| `doSomething` | ma'nosi yo'q | aniq fe'l |
| `temp`, `tmp` | umri yashirin | `scaledPrice` |
| `result`, `value`, `item` | kontekstsiz | `taxedTotal`, `orderLine` |
| `flag` | nimani belgilaydi? | `stockReserved` |
| `list2`, `map2` | farq ma'nosiz | rolga qarab nom |

## 2.5 Talaffuz qilinadigan nom

Nomni ovoz chiqarib aytib bo'lmasa, u haqida gaplasha olmaysiz. `genymdhms` nomi code review da "gen-y-m-d-h-m-s" ga aylanadi va suhbat buziladi. Talaffuz qilinadigan nom esa jamoa lug'atiga qo'shiladi: "generationTimestamp ni tekshirdingmi?" degan savol bir urinishda tushuniladi.

```java
// yomon: ovoz chiqarib aytish mumkin emas
private Date genymdhms;
private String pszqint;

// yaxshi: suhbatda ishlatiladi
private Instant generatedAt;
private String quarterlyIntervalCode;
```

## 2.6 Qidiriladigan nom va bir harfli o'zgaruvchi chegarasi

Nomning qiymati uni grep bilan topish mumkinligida ham. `e` harfini qidirib bo'lmaydi; `MAX_CLASSES_PER_STUDENT` ni esa bir urinishda topasiz. Shu sababli raqamli literal va bir harfli nomlar katta qamrovda yaramaydi.

Bir harfli nom faqat bitta holatda haqli: qamrov juda kichik va ma'nosi an'anaviy. Sikl hisoblagichi `i`, `j`; lambda ichidagi bitta argument; `catch` blokidagi `e`. Qamrov bir necha qatordan oshsa, nom to'liq yoziladi (3.15 va 2.15).

```java
// yomon: qidirib bo'lmaydi, ma'no yashirin
for (int j = 0; j < 34; j++) { s += (t[j] * 4) / 5; }

// yaxshi: har bir element qidiriladi va nomlangan
static final int WORK_DAYS_PER_WEEK = 5;
static final int REAL_DAYS_PER_IDEAL_DAY = 4;
int sum = 0;
for (int task = 0; task < NUMBER_OF_TASKS; task++) {
    int realTaskDays = taskEstimate[task] * REAL_DAYS_PER_IDEAL_DAY;
    sum += (realTaskDays / WORK_DAYS_PER_WEEK);
}
```

## 2.7 Kodlash va prefikslar: Hungarian notation, `m_`, `I` prefiksi

Nomga tur yoki qamrov haqidagi ma'lumotni kodlab yozish zamonaviy IDE da keraksiz va zararli: tur o'zgarsa prefiks yolg'onga aylanadi. `strName`, `iCount`, `m_description`, `_field` shakllari shu sababli chiqib ketdi.

Interfeys prefiksi alohida holat. `IOrderRepository` nomi o'quvchiga keraksiz ma'lumot beradi (bu interfeys ekani muhim emas) va implementatsiyani nomsiz qoldiradi. To'g'ri yechim: interfeys sof domen nomini oladi, implementatsiya mexanika nomini oladi.

```java
// yomon
public interface IOrderRepository { }
public class OrderRepositoryImpl implements IOrderRepository { }

// yaxshi: interfeys domen nomini oladi, implementatsiya mexanikani aytadi
public interface OrderRepository { }
public class JdbcOrderRepository implements OrderRepository { }
public class InMemoryOrderRepository implements OrderRepository { }  // test uchun
```

`Impl` qo'shimchasi faqat bitta implementatsiya bo'lib, uning mexanikasini ayta olmaydigan kam holatda haqli (3.6).

## 2.8 Aqliy tarjimani talab qiladigan nom

Agar o'quvchi nomni o'qib, ongda boshqa nomga aylantirishi kerak bo'lsa, nom ishlamaydi. Klassik misol: `for (int i...)` ichida `i` aslida "mijoz indeksi" ekanini eslab turish. Professional farqi shu: o'quvchi uchun aniq yozadi, o'zi uchun qisqa yozmaydi.

```java
// yomon: o'quvchi r nima ekanini eslab turadi
for (var r : rows) { if (r[2] != null) process(r); }

// yaxshi: tarjima kerak emas
for (PaymentRow payment : paymentRows) {
    if (payment.settledAt() != null) {
        process(payment);
    }
}
```

## 2.9 Sinf nomi ot, metod nomi fe'l, getter konvensiyasi

Konvensiya oddiy va istisnosi kam: sinf va record nomi ot yoki ot iborasi (`Invoice`, `PaymentGateway`, `OrderLine`), metod nomi fe'l yoki fe'l iborasi (`postPayment`, `deletePage`, `save`). Fe'l bo'lmagan metod nomi (`data()`, `info()`) nima qilishini aytmaydi.

Aksessor, mutator va predikat uchun JavaBean konvensiyasi: `getName`, `setName`, `isPosted`. Record va domen obyektlarida esa `get` prefiksini tashlab, maydon nomini ishlatish qabul qilingan: `order.total()`, `payment.settledAt()`. Muhimi - bitta kod bazasida bitta uslub.

```java
// konstruktor overload o'rniga nomlangan statik fabrika (nom maqsadni aytadi)
Complex fulcrumPoint = Complex.fromRealNumber(23.0);   // yaxshi
Complex fulcrumPoint = new Complex(23.0);              // yomon: 23.0 nima?
```

## 2.10 Hazil, jargon va madaniy havolalar

Hazilli nom bir kishiga tushunarli, qolganlarga yo'q. `whack()` o'rniga `kill()`, `eatMyShorts()` o'rniga `abort()` yozish kerak. Mahalliy jargon va qisqartmalar ham shu toifada: ular jamoadan chiqqach ma'nosini yo'qotadi.

Qoida: nom ikki yildan keyin, boshqa jamoada, boshqa tilda gaplashadigan odam uchun ham ishlashi kerak. Hazil shu sinovdan o'tmaydi.

## 2.11 Bitta tushunchaga bitta so'z

`get`, `fetch`, `retrieve`, `find`, `load`, `lookup` so'zlari bir xil narsani anglatsa, kod bazasida faqat bittasi qolishi kerak. Aks holda o'quvchi har safar "farq bormi?" deb o'ylaydi va IDE avtotoldirishi foydasiz bo'lib qoladi.

Shu bilan birga, agar farq bor bo'lsa, u izchil bo'lishi kerak. Keng tarqalgan izchil taqsimot quyidagicha.

| So'z | Ma'nosi | Topilmasa |
|---|---|---|
| `findX` | izlaydi, bo'lmasligi normal | `Optional.empty()` |
| `getX` | mavjudligi kafolatlangan | istisno |
| `loadX` | tashqi manbadan oladi | istisno |
| `fetchX` | tarmoq orqali oladi | istisno yoki `Optional` |
| `listX` | ko'p natija | bo'sh ro'yxat |
| `searchX` | mezon bo'yicha, sahifalangan | bo'sh sahifa |
| `createX` | yangi yaratadi | konflikt istisnosi |
| `ensureX` | yo'q bo'lsa yaratadi | idempotent |

## 2.12 So'z o'yini qilmaslik

Bitta so'zni ikki xil ma'noda ishlatish 2.11 ning teskarisi va xatosi ham shunchalik qimmat. `add` metodi bir joyda arifmetik qo'shishni, boshqa joyda to'plamga element qo'shishni bildirsa, o'quvchi har safar kodni o'qib tekshiradi.

```java
// yomon: add ikki xil ma'noda
Money add(Money other);                 // arifmetik
void add(OrderLine line);               // to'plamga qo'shish

// yaxshi: har bir amal o'z nomini oladi
Money plus(Money other);
void appendLine(OrderLine line);
```

## 2.13 Yechim domeni va muammo domeni nomlari

Ikki xil lug'at bor va ikkisi ham o'z o'rnida to'g'ri. Yechim domeni (informatika, pattern, texnologiya) nomlari texnik kodda yaxshi ishlaydi: `JobQueue`, `RetryPolicy`, `AccountVisitor`, `ConnectionPool`. Muammo domeni (biznes) nomlari domen kodida ishlaydi: `Invoice`, `SettlementBatch`, `CreditLimit`.

Xato ikki yo'nalishda bo'ladi. Domen sinfiga texnik nom berish (`OrderStrategyFactoryBean`) biznes ma'nosini yo'qotadi. Texnik sinfga biznes nomi berish (`OrderHelper` aslida HTTP klient) o'quvchini chalg'itadi. Qoida: nomni o'quvchining kim bo'lishiga qarab tanlang.

## 2.14 Kontekst qo'shish va ortiqcha kontekst qo'shmaslik

Nom o'z-o'zidan yetarli kontekst bermasa, uni qo'shish kerak - lekin prefiks bilan emas, tur yoki paket bilan. `state` o'zi noaniq; `Address` sinfi ichidagi `state` esa aniq.

```java
// yomon: har bir maydonga prefiks qo'yilgan
class Address {
    private String addrFirstName;
    private String addrState;
}

// yaxshi: kontekst sinfdan keladi
class Address {
    private String firstName;
    private String state;
}
```

Teskari xato ham bor: ortiqcha kontekst. `GasStationDeluxe` ilovasida har bir sinfni `GSD` prefiksi bilan boshlash avtotoldirishni buzadi va hech narsa qo'shmaydi. Paket nomi allaqachon kontekst beradi.

## 2.15 Nom uzunligi qamrovga mutanosib

Amaliy qoida: nom uzunligi uning qamrovi (scope) ga mutanosib bo'lishi kerak. Uch qatorli blok ichidagi o'zgaruvchi qisqa nom ola oladi; `public static final` maydon yoki public API metodi to'liq va aniq nom talab qiladi.

| Qamrov | Nom uzunligi | Misol |
|---|---|---|
| Lambda argumenti, 1 qator | 1-2 harf | `p -> p.isSettled()` |
| Sikl hisoblagichi | 1 harf | `i`, `j` |
| Metod ichidagi mahalliy, 3-10 qator | bir so'z | `total`, `draft` |
| Metod ichidagi mahalliy, uzun | ikki-uch so'z | `taxedOrderTotal` |
| Maydon | ikki-uch so'z | `paymentRetryPolicy` |
| Public metod | to'liq ibora | `reserveStockForOrder` |
| Public konstanta | to'liq, birlik bilan | `DEFAULT_READ_TIMEOUT_MS` |
| Sinf | ot iborasi | `SettlementBatchImporter` |

## 2.16 Qisqartma qoidalari va psixologik masofa

Qisqartma yozuvni tezlashtiradi va o'qishni sekinlashtiradi. Programmist kod bazasining hayoti davomida yozishdan ko'ra ko'proq o'qiydi, shuning uchun tanlov o'qish foydasiga qilinadi: qisqartma faqat jamoada kelishilgan va hujjatlashtirilgan bo'lsa haqli, qolgan holatda so'z to'liq yoziladi (McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 11.6 (285-bet)).

**Fonetik qisqartma yozilmaydi.** So'zning imlosi emas, tovushi bo'yicha qisqartirish (`skating` dan `sk8ing`, `highlight` dan `hilite`, `before` dan `b4`, `execute` dan `xqt`) nomni jumboqqa aylantiradi; McConnell bu usulni shaxsiy avtomobil raqamini o'qishga qiyoslaydi va tavsiya qilmaydi (shu yerda, 11.6 (283-bet)).

**Bitta harf tashlash qisqartma emas.** Bitta belgi yozish mehnati arzimas, yo'qotilgan o'qilish esa arzimas emas; keyin o'zingiz ham harf tashlagan yoki tashlamaganingizni eslamaysiz. Yo bir necha harf tashlanadi, yo so'z to'liq yoziladi.

**Bitta so'zga bitta qisqartma.** `Num` yoki `No` dan biri tanlanadi va hamma joyda shu ishlatiladi; bir joyda `Number`, boshqa joyda `Num` bo'lmaydi. Bu 2.11 dagi "bitta tushunchaga bitta so'z" qoidasining qisqartmaga tegishli shakli.

**Telefon testi.** Kodni telefonda boshqa odamga o'qib bera olmasangiz, nom o'zgaradi: `xPstn` emas `xPos`, `ndsCmptg` emas `needsComputing` (shu yerda, 11.6 (283-bet)). Bu [talaffuz qilinadigan nom](#25-talaffuz-qilinadigan-nom) qoidasining qisqartmaga tegishli tekshiruvi.

**Psixologik masofa** - ikki nomni bir-biridan ajratishning qanchalik osonligi. Masofa kichik bo'lsa, o'quvchi ikki nomni bitta deb o'qiydi va xato ko'rinmas bo'lib qoladi:

| Birinchi nom | Ikkinchi nom | Masofa |
|---|---|---|
| `stoppt` | `stcppt` | deyarli ko'rinmaydi |
| `shiftrn` | `shiftrm` | deyarli yo'q |
| `dcount` | `bcount` | kichik |
| `claims1` | `claims2` | kichik |
| `product` | `sum` | katta |

Jadval McConnell dan (shu yerda, 23.4 (556-bet)). Undan ikkita amaliy qoida chiqadi. Birinchisi: ikki nom orasida kamida ikki harf farq bo'lsin yoki farq nomning boshida yoki oxirida tursin, chunki so'z o'rtasidagi harf eng kam ko'rinadi (shu yerda, 11.7 (285-bet)). Ikkinchisi: ma'nosi yaqin nomlar ham xavfli - `input` va `inputValue`, `recordNum` va `numRecords`, `fileNumber` va `fileIndex` juftlarini bir qarashda ajratib bo'lmaydi; ikki o'zgaruvchining nomini almashtirib qo'yganda programma buzilmasa, ikkisi ham qayta nomlanishi kerak (shu yerda, 11.7 (285-bet) va bu bobdagi [ma'noli farq](#23-manoli-farq-a1-a2-info-va-data) qoidasi).

```java
// yomon: farq bitta harfda va u so'z o'rtasida
int clientRecs = repository.countRecords(clientId);
int clientReps = repository.countReports(clientId);

// yaxshi: farq oxirida va bir necha harfda
int clientRecordCount = repository.countRecords(clientId);
int clientReportCount = repository.countReports(clientId);
```

Qoida nega debug paytida qimmat: odam kutgan narsasini ko'radi, shuning uchun masofasi kichik juft nomlar xatoni o'qish paytida ko'rinmas qiladi. Shu mexanizm va uning debugdagi oqibati [xatoni topish va tuzatish tartibida](46-vaqt-diqqat-va-mashq.md#4610-xatoni-topish-va-tuzatish-tartibi) ko'rilgan.

## 2.17 Nomga ma'lumot zichlash: aniq so'z va aniq nom

Nom kichik izoh: joyi oz, lekin o'quvchi uni o'zgaruvchi har ko'ringanda o'qiydi. Shuning uchun nomga ma'lumot zichlanadi, ya'ni bo'sh so'z aniq so'z bilan almashtiriladi (Boswell/Foucher, *The Art of Readable Code*, 1-nashr, O'Reilly, 2011, 2-bob (8-bet)).

**Bo'sh fe'l o'rniga aniq fe'l.** `get` manbani ajratmaydi: keshdanmi, bazadanmi, tarmoqdanmi. Tarmoqdan olsa `fetch` yoki `download` aniqroq. `size()` ham shunday bo'sh: daraxt balandligimi, tugun sonimi, bayt hajmimi. `stop()` qaytarib bo'lmaydigan amal bo'lsa `kill()`, `resume()` juftligi bor bo'lsa `pause()`. Chegara ham bor: aniqlik maqsad, chiroylilik emas. PHP dagi `explode` jonli nom, lekin uning `split` dan farqini nom aytmaydi, demak u ma'lumot bermaydi (shu yerda, 9-bet).

```java
// yomon: fe'l manbani ham, o'lchovni ham aytmaydi
Page getPage(URI uri);
int size();

// yaxshi: manba va o'lchov nomda
Page downloadPage(URI uri);
int nodeCount();
```

**Mavhum nom o'rniga aniq nom.** Nom predmetni mavhum emas, aniq tasvirlasin. Kitob misoli: TCP portni tinglash mumkinligini tekshiradigan metod `serverCanStart()` deb nomlangan, aniq shakli `canListenOnPort()` - u metod nima qilishini to'g'ridan-to'g'ri aytadi (shu yerda, 13-bet). Ikkinchi misol bayroq nomi haqida: `--run_locally` nom ishlatilish holatidan olingan, shuning uchun yangi jamoadosh u nima qilishini bilmaydi va masofadagi serverda log kerak bo'lganda nom kulgili ko'rinadi; to'g'ri shakl `--extra_logging`, ya'ni bayroq nima qilishini aytadi. Bayroq ikki ishni boshqarsa, nomni mavhumlashtirish emas, ikkinchi bayroq (`--use_local_database`) qo'shish to'g'ri: ikki ortogonal g'oyani bitta nomga siqish nomni ataylab noaniq qilishdir (shu yerda, 14-15-bet).

```java
// yomon: nom ishlatilish holatidan olingan, xatti-harakatdan emas
@Value("${app.run-locally:false}")
private boolean runLocally;

// yaxshi: har bayroq o'z xatti-harakatini aytadi
@Value("${app.extra-logging:false}")
private boolean extraLogging;
@Value("${app.use-local-database:false}")
private boolean useLocalDatabase;
```

Bu ikki harakat [bitta tushunchaga bitta so'z](#211-bitta-tushunchaga-bitta-soz) qoidasi bilan birga ishlaydi: avval har tushuncha uchun aniq so'z tanlanadi, keyin shu so'z kod bazasida izchil ishlatiladi.

## 2.18 Nomni xato talqinlarga sinash

2.1 nom javob berishi kerak savollarni berdi, 2.2 esa yolg'on ma'lumot beradigan nomni ko'rsatdi. Bu bo'lim jarayon haqida: nomni yozib qo'ygandan keyin uni **ataylab noto'g'ri o'qishga urinib ko'rish**. Boswell va Foucher ning asosiy g'oyasi shu: nomni tanqid qilish uchun "bu nomdan boshqa qanday ma'no o'qilishi mumkin?" savoli beriladi va javob izlanadi.

**Ikki qarama-qarshi ma'noga ega so'z nom qilinmaydi.** `filter` buning klassik misoli: `Database.allObjects.filter("year <= 2011")` natijasida sharti to'g'ri chiqqan obyektlar qoladimi yoki olib tashlanadimi - nom aytmaydi. Tanlab qoldirish uchun `select`, olib tashlash uchun `exclude` yoziladi. Shu guruhdagi ikkinchi misol - `clip(text, length)`: u oxiridan `length` ni kesadimi yoki matnni `length` uzunligigacha qisqartiradimi? Niyat ikkinchisi bo'lsa, nom `truncate(text, maxChars)` bo'ladi, chunki `max` chegarani aytadi ([chegara nomlari](03-nom-turlari-boyicha-aniq-konvensiyalar.md#316-hisoblangan-qiymat-qoshimchasi-va-juft-nomlar)) va `chars` birlikni aytadi: `length` baytmi, belgimi yoki so'zmi noaniq edi. Uchinchi shakl - ot ham, fe'l ham bo'la oladigan metod nomi: `count()` "sanani qaytaradi" ham, "sanab chiq" ham bo'lib o'qiladi.

| Shubhali nom | Ikki talqin | Aniq shakl |
|---|---|---|
| `filter(predicate)` | tanlab qoldirish yoki olib tashlash | `select` yoki `exclude` |
| `clip(text, length)` | oxiridan kesish yoki chegaraga qisqartirish | `truncate(text, maxChars)` |
| `count()` | sonni qaytaradi yoki sanashni boshlaydi | `itemCount()` yoki `recountItems()` |
| `check(order)` | tekshirib natija qaytaradi yoki istisno tashlaydi | `isValid(order)` yoki `validate(order)` |

**Baho beruvchi va hissiy so'z nomga qo'yilmaydi.** Google ning C++ kodida nusxa konstruktori va `operator=` ni taqiqlovchi makro uzoq vaqt `DISALLOW_EVIL_CONSTRUCTORS` deb nomlangan. Ikki muammo bor edi. Birinchisi: "evil" so'zi bahsli pozitsiyani juda qattiq ifodalaydi, ya'ni nom texnik faktni emas, muallifning fikrini aytadi. Ikkinchisi va amaliyroq: nom nimani taqiqlayotganini aytmaydi, va aslida u konstruktorni emas, nusxa olish va tayinlashni taqiqlardi (`operator=` konstruktor ham emas). Makro keyinchalik `DISALLOW_COPY_AND_ASSIGN` deb qayta nomlangan. Java da bu `UglyHackUtil`, `StupidLegacyMapper` yoki `TemporaryBadFix` kabi nomlar: ular o'quvchiga nima qilinayotganini emas, muallifning kayfiyatini aytadi.

**Nomzodlar bittadan sinaladi.** Nom tanlashda bir nechta variant bo'lsa, har biri alohida tekshiriladi: bu nom nimani anglatmasligi mumkin? Boswell va Foucher ning misoli - bir tajribaning sozlamalarini boshqasidan qayta ishlatish uchun kalit nomi. `template` noaniq ("men shablonmanmi yoki shablonni ishlatayapmanmi?") va shablon ko'pincha to'ldirilmagan narsa deb tushuniladi. `reuse: 100` "bu tajriba 100 martagacha qayta ishlatiladi" deb o'qilishi mumkin. `copy: 100` "100 marta nusxa ol" yoki "bu 100-nusxa" deb o'qiladi. `inherit` esa programmistga tanish va undan keyin o'zgartirish kiritilishi kutilishini aytadi. Yechim ikki qadamli: aniqroq so'z tanlanadi va **nom qaysi obyektga ishora qilishini ham aytadi**, ya'ni `copyExperiment` yoki `inheritFromExperimentId`.

Oxirgi va eng arzon tekshiruv - **hamkasbdan so'rash**: nom yoki izoh nimani anglatishini so'rang va uning birinchi taassurotini kelajakdagi o'quvchining taassuroti deb oling. Tushuntirib bergandan keyin "ha, endi tushunarli" degan javob natija emas: o'quvchi yonida siz turmaysiz.

## 2.19 Amalda qo'llash

- [ ] Kod bazasida `Info`, `Data`, `Object`, `temp`, `flag`, `result` so'zlarini grep qilib, har birini rolga qarab qayta nomlang.
- [ ] `IOrderRepository` turidagi interfeys prefikslarini olib tashlab, implementatsiyalarga mexanika nomini bering (`JdbcOrderRepository`).
- [ ] `get`/`find`/`fetch`/`load` so'zlarining joriy ishlatilishini sanab, 2.11 jadvalidagi bitta izchil taqsimotni kelishib oling va qolganini qayta nomlang.
- [ ] Bir harfli o'zgaruvchilarni qamrovi 5 qatordan oshganlarini topib, to'liq nomga o'tkazing.
- [ ] `m_`, `str`, `i`, `_` prefikslarini Checkstyle qoidasi bilan taqiqlang (13.4).
- [ ] Bir xil tushuncha uchun ikki nom ishlatilgan joylarni (`Product`/`ProductInfo`) birlashtiring yoki farqini bir gapda hujjatlashtiring.
- [ ] Har bir public konstanta nomida birlik borligini tekshiring (`...Ms`, `...Bytes`, `...Percent`).
- [ ] Jamoa lug'atini (glossary) fayl sifatida repoga qo'shib, har bir yangi domen atamasini shu yerda qayd eting (3.14).
- [ ] Jamoa lug'atiga qisqartmalar ro'yxatini qo'shib, fonetik qisqartmalarni (`hilite`, `xqt`) taqiqlang va bir harf bilan farq qiladigan nom juftlarini topib qayta nomlang (2.16).

## Manbalar

- Dustin Boswell, Trevor Foucher, *The Art of Readable Code*, 1-nashr, O'Reilly, 2011 (copyright 2012), 2-bob (14-bet) va 3-bob (24, 29-31-betlar) - nomga baho beruvchi so'z qo'ymaslik va `DISALLOW_EVIL_CONSTRUCTORS` ning `DISALLOW_COPY_AND_ASSIGN` ga qayta nomlanishi; ikki qarama-qarshi ma'noli so'z (`filter`, `clip`); nom nomzodlarini bittadan xato talqinlarga sinash (`template`, `reuse`, `copy`, `inherit`) va nomning qaysi obyektga ishora qilishini aytishi
- Robert C. Martin, *Clean Code*, 2-bob - maqsadni ochib beruvchi nom, yolg'on ma'lumot, ma'noli farq, talaffuz qilinadigan va qidiriladigan nom
- Robert C. Martin, *Clean Code*, 2-bob ("Avoid Encodings") - Hungarian notation, a'zo prefiksi, interfeys va implementatsiya nomlari
- Robert C. Martin, *Clean Code*, 2-bob ("Add Meaningful Context") - kontekst qo'shish va ortiqcha kontekst qo'shmaslik
- Robert C. Martin, *Clean Code*, 17-bob, N1-N7 - nomlash evristikalari, uzun qamrov uchun uzun nom
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 11.6
  (283, 285) - fonetik qisqartma, bitta harf tashlamaslik, izchil
  qisqartirish, telefon testi va qisqartma to'qnashuvini sinonim bilan
  yechish; yozish qulayligi va o'qish qulayligi farqi
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 11.7
  (285) - o'xshash ma'noli va bir harf bilan farq qiladigan nomlar, kamida
  ikki harf farq talabi
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 23.4
  (556) - psixologik masofa ta'rifi va nomlar jadvali
- Dustin Boswell, Trevor Foucher, *The Art of Readable Code*, 1-nashr, O'Reilly, 2011 (copyright 2012), 2-bob (8-9-betlar) - `get` va `size` bo'sh so'zligi, `fetch`/`download` va `nodeCount` aniq shakllari, `stop`/`kill`/`pause` tanlovi, `explode` va `split` misolida "aniq va to'g'ri, chiroyli emas" mezoni
- Dustin Boswell, Trevor Foucher, *The Art of Readable Code*, 1-nashr, O'Reilly, 2011 (copyright 2012), 2-bob (13-15-betlar) - `ServerCanStart` o'rniga `CanListenOnPort`, `--run_locally` nomining uch muammosi va `--extra_logging` bilan `--use_local_database` ga bo'linishi
- Y. Daniel Liang, *Introduction to Java Programming*, 9-nashr, Pearson, 2013, 2-bob (44-bet) - Java kutubxonasida mavjud sinf nomini (`System`, `List`) o'z sinfiga bermaslik

---

[&larr; 1. Toza kod nima va nega qimmat](01-toza-kod-nima-va-nega-qimmat.md) · [Mundarija](README.md) · [3. Nom turlari bo'yicha aniq konvensiyalar &rarr;](03-nom-turlari-boyicha-aniq-konvensiyalar.md)
