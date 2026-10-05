<!-- doc: clean-code | chapter: 2 | part: I. Toza kodning asosi -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 2. Nomlash qoidalari: maqsadni ochib beruvchi nom (Naming: Intention-Revealing Names)

<details>
<summary>Bu bobdagi 16 bo'lim</summary>

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
- [2.16 Amalda qo'llash](#216-amalda-qollash)

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

## 2.16 Amalda qo'llash

- [ ] Kod bazasida `Info`, `Data`, `Object`, `temp`, `flag`, `result` so'zlarini grep qilib, har birini rolga qarab qayta nomlang.
- [ ] `IOrderRepository` turidagi interfeys prefikslarini olib tashlab, implementatsiyalarga mexanika nomini bering (`JdbcOrderRepository`).
- [ ] `get`/`find`/`fetch`/`load` so'zlarining joriy ishlatilishini sanab, 2.11 jadvalidagi bitta izchil taqsimotni kelishib oling va qolganini qayta nomlang.
- [ ] Bir harfli o'zgaruvchilarni qamrovi 5 qatordan oshganlarini topib, to'liq nomga o'tkazing.
- [ ] `m_`, `str`, `i`, `_` prefikslarini Checkstyle qoidasi bilan taqiqlang (13.4).
- [ ] Bir xil tushuncha uchun ikki nom ishlatilgan joylarni (`Product`/`ProductInfo`) birlashtiring yoki farqini bir gapda hujjatlashtiring.
- [ ] Har bir public konstanta nomida birlik borligini tekshiring (`...Ms`, `...Bytes`, `...Percent`).
- [ ] Jamoa lug'atini (glossary) fayl sifatida repoga qo'shib, har bir yangi domen atamasini shu yerda qayd eting (3.14).

---

[&larr; 1. Toza kod nima va nega qimmat](01-toza-kod-nima-va-nega-qimmat.md) · [Mundarija](README.md) · [3. Nom turlari bo'yicha aniq konvensiyalar &rarr;](03-nom-turlari-boyicha-aniq-konvensiyalar.md)
