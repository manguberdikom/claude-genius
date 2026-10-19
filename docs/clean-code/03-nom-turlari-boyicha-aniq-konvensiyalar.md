<!-- doc: clean-code | chapter: 3 | part: I. Toza kodning asosi -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 3. Nom turlari bo'yicha aniq konvensiyalar (Naming Conventions by Kind)

<details>
<summary>Bu bobdagi 18 bo'lim</summary>

- [3.1 Mantiqiy nomlar: `is`, `has`, `can`, `should` va inkor tuzog'i](#31-mantiqiy-nomlar-is-has-can-should-va-inkor-tuzogi)
- [3.2 To'plam, massiv va oqim nomlari](#32-toplam-massiv-va-oqim-nomlari)
- [3.3 Birlik nomda: `timeoutMs`, `sizeBytes`, `priceMinor`](#33-birlik-nomda-timeoutms-sizebytes-priceminor)
- [3.4 Konstanta, `static final` va enum a'zolari](#34-konstanta-static-final-va-enum-azolari)
- [3.5 Enum turi va holat nomlari](#35-enum-turi-va-holat-nomlari)
- [3.6 Interfeys va implementatsiya nomlari: `Impl` qachon haqli](#36-interfeys-va-implementatsiya-nomlari-impl-qachon-haqli)
- [3.7 Abstrakt sinf va `Abstract` prefiksi](#37-abstrakt-sinf-va-abstract-prefiksi)
- [3.8 Generik tur parametrlari](#38-generik-tur-parametrlari)
- [3.9 Metod nomi va qaytish turi muvofiqligi](#39-metod-nomi-va-qaytish-turi-muvofiqligi)
- [3.10 Istisno sinflari nomlari](#310-istisno-sinflari-nomlari)
- [3.11 Paket, modul va artefakt nomlari](#311-paket-modul-va-artefakt-nomlari)
- [3.12 Test metodi va test sinfi nomlari](#312-test-metodi-va-test-sinfi-nomlari)
- [3.13 Fayl, resurs va konfiguratsiya kaliti nomlari](#313-fayl-resurs-va-konfiguratsiya-kaliti-nomlari)
- [3.14 Jamoa lug'ati va uni majburlash](#314-jamoa-lugati-va-uni-majburlash)
- [3.15 Nomni o'zgartirish intizomi](#315-nomni-ozgartirish-intizomi)
- [3.16 Hisoblangan qiymat qo'shimchasi va juft nomlar](#316-hisoblangan-qiymat-qoshimchasi-va-juft-nomlar)
- [3.17 Registr, akronim va grammatik shakl](#317-registr-akronim-va-grammatik-shakl)
- [3.18 Amalda qo'llash](#318-amalda-qollash)

</details>


Oldingi bob nomning umumiy sifatini tekshirdi. Bu bobda har bir nom turi uchun alohida konvensiya beriladi: mantiqiy qiymat, to'plam, konstanta, enum, interfeys, generik parametr, istisno, paket, fayl. Konvensiya bo'lmasa, har bir ishlab chiquvchi o'z uslubini kiritadi va kod bazasi bir necha dialektga bo'linadi.

## 3.1 Mantiqiy nomlar: `is`, `has`, `can`, `should` va inkor tuzog'i

Mantiqiy qiymat nomi gap bo'lishi kerak, shunda `if` ichida o'qilishi tabiiy chiqadi. To'rtta prefiks yetarli: `is` (holat), `has` (egalik), `can` (ruxsat yoki imkoniyat), `should` (siyosat qarori). `was`, `will` va `requires` ham qo'shiladi, lekin faqat ma'nosi aniq bo'lganda.

Eng qimmat xato - inkor nom. `isNotValid`, `disableCache`, `notFound` nomlari `if (!isNotValid)` kabi ikki marta inkorga olib keladi va o'quvchi xato o'qiydi. Qoida: nom har doim ijobiy shaklda, inkor `!` operatorida qoladi.

```java
// yomon
boolean isNotEligible;
boolean disableRetry;
if (!isNotEligible && !disableRetry) { ... }   // ikki inkor

// yaxshi
boolean eligible;
boolean retryEnabled;
if (eligible && retryEnabled) { ... }
```

| Prefiks | Ma'nosi | Misol |
|---|---|---|
| `is` | hozirgi holat | `isSettled`, `isExpired` |
| `has` | egalik, mavjudlik | `hasActiveSubscription` |
| `can` | imkoniyat, ruxsat | `canBeCancelled` |
| `should` | siyosat qarori | `shouldRetry` |
| `was` | o'tgan holat | `wasDelivered` |
| `requires` | talab | `requiresManualReview` |
| sifat | holat sifati | `empty`, `blank`, `stale` |

## 3.2 To'plam, massiv va oqim nomlari

To'plam nomi ko'plikda bo'ladi va tur nomini takrorlamaydi. `orders` yetarli; `orderList` esa `List` dan `Set` ga o'tganda yolg'onga aylanadi (2.2). Map uchun esa kalit va qiymat munosabatini nomda ko'rsatish kerak, chunki `Map<A,B>` o'zi yetarli emas.

```java
List<Order> orders;                       // yaxshi
Set<Sku> reservedSkus;                    // yaxshi
Map<CustomerId, List<Order>> ordersByCustomer;   // kalit → qiymat nomda
Map<Sku, Integer> availableQuantityBySku;        // qiymat ma'nosi nomda
Stream<Payment> settledPayments;          // oqim ham ko'plikda
```

Agar to'plamning roli alohida bo'lsa, rol nomi ko'plikdan ustun: `shippingQueue`, `auditTrail`, `priceHistory`.

## 3.3 Birlik nomda: `timeoutMs`, `sizeBytes`, `priceMinor`

Birlik nomda bo'lmasa, uni ongda saqlash kerak bo'ladi va bu eng ko'p uchraydigan production xatolarining manbai: sekundni millisekund deb berish, so'mni tiyin deb hisoblash, bayt va kilobaytni aralashtirish.

```java
// yomon: birlik yashirin
void setTimeout(long timeout);
long size;
BigDecimal price;

// yaxshi: birlik nomda yoki turda
void setReadTimeout(Duration readTimeout);     // eng yaxshi: tur birlikni ushlaydi
void setReadTimeoutMs(long readTimeoutMs);     // ikkinchi yaxshi: nomda
long sizeBytes;
long priceMinorUnits;                          // tiyin
Money price;                                   // eng yaxshi: value object
```

Qoida tartibi: birlikni turga ko'chirish (`Duration`, `Money`, `Percentage`) eng yaxshi; nomga yozish ikkinchi; hech qayerda yozmaslik xato.

Birlik qoidasining umumlashmasi bor: nomga **xavfli yoki kutilmagan har qanday xususiyat** yoziladi, nafaqat o'lchov birligi. Boswell va Foucher buni xavfsizlik tomonidan ko'rsatadi: ko'p ekspluatatsiya programma olgan ma'lumot hali xavfsiz holatda emasligini payqamaslikdan chiqadi, shuning uchun `untrustedUrl` va `unsafeMessageBody` nomlari tozalashdan keyin `trustedUrl` va `safeMessageBody` ga aylanadi (Boswell/Foucher, *The Art of Readable Code*, 1-nashr, O'Reilly, 2011, 2-bob (16-17-bet)). Kitob jadvali to'rt holatni beradi: shifrlanmagan parol `plaintextPassword`, ekranlanmagan foydalanuvchi matni `unescapedComment`, UTF-8 ga o'tkazilgan HTML `htmlUtf8`, URL kodlangan kirish `dataUrlenc`.

```java
// yomon: nom bir xil, holat esa har xil - almashtirib yuborish jim o'tadi
String password = request.password();
String comment = request.comment();
render(comment);                              // XSS: ekranlanmagan

// yaxshi: xavfli holat nomda, tozalanganidan keyin nom o'zgaradi
String plaintextPassword = request.password();
String passwordHash = encoder.encode(plaintextPassword);
String unescapedComment = request.comment();
String safeComment = HtmlUtils.htmlEscape(unescapedComment);
render(safeComment);
```

Chegara muhim: bu prefikslar har o'zgaruvchiga yopishtirilmaydi, aks holda ular shovqinga aylanadi va [shovqin so'zlar](02-nomlash-qoidalari-maqsadni-ochib-beruvchi.md#24-shovqin-sozlar-info-data-object-variable-the) qoidasiga tushadi. Mezon aniq: o'quvchi o'zgaruvchining holatini xato tushunsa xato oson sizib kiradigan va oqibati og'ir bo'ladigan joyda yoziladi, ya'ni avvalo xavfsizlik chegarasida. Shu bilan bu Hungarian notation emas: Hungarian turni kodlaydi va rasmiy tizim, bu yerda esa faqat muhim xususiyat va faqat kerak bo'lganda kodlanadi (shu yerda, 17-bet).

## 3.4 Konstanta, `static final` va enum a'zolari

Java konvensiyasi: `UPPER_SNAKE_CASE` faqat haqiqiy konstantalar uchun, ya'ni kompilyatsiya vaqtida ma'lum va o'zgarmas qiymatlar. O'zgarmas, lekin ish vaqtida hisoblanadigan maydon (`private final Clock clock`) oddiy `camelCase` oladi.

Konstanta nomi uning ma'nosini, qiymatini emas, aytishi kerak. `THREE = 3` foydasiz; `MAX_RETRY_ATTEMPTS = 3` foydali. Qiymatni nomda takrorlash (`TIMEOUT_30 = 30`) qiymat o'zgarganda nomni yolg'onga aylantiradi.

```java
// yomon
static final int THREE = 3;
static final int TIMEOUT_30 = 30;
static final String S = "ERROR";

// yaxshi: ma'no, birlik va asos
static final int MAX_RETRY_ATTEMPTS = 3;
static final Duration GATEWAY_READ_TIMEOUT = Duration.ofSeconds(30);
static final String SETTLEMENT_FAILED_CODE = "SETTLEMENT_FAILED";
```

Konstantani interfeysga qo'yib voris olish (constant interface) qoldirilgan amaliyot (17.8). Konstantalar `enum` ga yoki `final` utility sinfga yoki eng yaxshisi tegishli domen sinfiga joylashadi.

Bitta istisno nomlashdan kattaroq: `public static final` massiv maydoni konstanta emas. Uzunligi noldan katta massivning elementi hamisha almashtirilishi mumkin, shuning uchun bunday maydon va shu maydonni qaytaruvchi accessor inkapsulyatsiyada tuynuk qoldiradi. Ikki yechim bor: massivni `private` qilib o'zgarmas `List` ko'rinishini ochish, yoki har chaqiruvda nusxa qaytarish (14.6).

```java
// yomon: klient PERMITTED_CODES[0] = "ANY" deb yozib qo'yadi
public static final String[] PERMITTED_CODES = { "OK", "RETRY" };

// yaxshi: o'zgarmas ko'rinish
private static final String[] CODES = { "OK", "RETRY" };
public static final List<String> PERMITTED_CODES = List.of(CODES);
```

Konstantaning yana bir oqibati binar moslikda ko'rinadi: `static final int` qiymati klient kodiga kompilyatsiya vaqtida ko'chiriladi. Shuning uchun kutubxonada qiymat o'zgartirilsa va klient qayta kompilyatsiya qilinmasa, klient eski qiymat bilan jim ishlashda davom etadi. `enum` da bu muammo yo'q: yangi a'zo qo'shish yoki a'zolar tartibini o'zgartirish klientni qayta kompilyatsiya qilishga majburlamaydi, chunki a'zoga havola ish vaqtida yechiladi (3.5, 25.9).

## 3.5 Enum turi va holat nomlari

Enum turi birlikda nomlanadi, chunki u bitta qiymatning turini bildiradi: `OrderStatus`, `PaymentMethod`, `Currency` - `OrderStatuses` emas. A'zolari esa `UPPER_SNAKE_CASE` va ma'nosi domen tilida: `PENDING`, `AWAITING_SETTLEMENT`, `PARTIALLY_REFUNDED`.

Enum a'zosi nomida qisqartma va texnik kod yashirmaslik kerak. `S1`, `S2` ma'nosiz; agar bazada raqamli kod saqlanishi kerak bo'lsa, kodni enum ichidagi maydonga olib, nomni o'qiladigan qoldirish kerak.

```java
public enum SettlementStatus {
    PENDING(0),
    SETTLED(1),
    REJECTED(2),
    PARTIALLY_REFUNDED(3);

    private final int legacyCode;   // bazadagi raqam alohida maydonda

    SettlementStatus(int legacyCode) { this.legacyCode = legacyCode; }

    public int legacyCode() { return legacyCode; }
}
```

## 3.6 Interfeys va implementatsiya nomlari: `Impl` qachon haqli

Interfeys domen rolini oladi, implementatsiya esa shu rolni **qanday** bajarishini aytadi. Shunday bo'lsa, `Impl` qo'shimchasi o'z-o'zidan keraksiz bo'lib qoladi: `OrderRepository` / `JdbcOrderRepository`, `PriceCalculator` / `TieredPriceCalculator`, `NotificationSender` / `SmtpNotificationSender`.

`Impl` faqat bitta holatda haqli: implementatsiya bitta va uning mexanikasini ayta olmaydigan darajada oddiy (masalan interfeys faqat test uchun ajratilgan). Bunda ham ko'pincha yaxshiroq yechim bor: interfeysni umuman yozmaslik va sinfning o'zini ishlatish ([arxitektor hujjatidagi](../architect/README.md) interfeysni foydalanuvchi tomonda e'lon qilish bo'limi).

| Interfeys | Yaxshi implementatsiya nomi | Yomon |
|---|---|---|
| `OrderRepository` | `JdbcOrderRepository` | `OrderRepositoryImpl` |
| `PaymentGateway` | `StripePaymentGateway` | `PaymentGatewayImpl` |
| `ExchangeRateProvider` | `CachingExchangeRateProvider` | `DefaultExchangeRateProvider` |
| `AuditLog` | `DatabaseAuditLog` | `AuditLogImpl` |
| `Clock` | `FixedClock`, `SystemClock` | `ClockImpl` |

`Default` prefiksi ham shu toifada: u mexanikani emas, mualliflik tartibini aytadi.

## 3.7 Abstrakt sinf va `Abstract` prefiksi

`AbstractOrderProcessor` nomi o'quvchiga texnik ma'lumot beradi (bu sinfni instantiate qilib bo'lmaydi) va bu ba'zan foydali, chunki voris yozmoqchi odam darhol tushunadi. Shuning uchun Java ekotizimida `Abstract` prefiksi qabul qilingan va undan voz kechish kerak emas.

Lekin ikki qoida bor. Birinchi, `Abstract` prefiksi faqat haqiqatan voris olish uchun mo'ljallangan sinfda bo'ladi; "umumiy kodni qo'yish uchun" yaratilgan bazaviy sinf esa odatda kompozitsiyaga aylantirilishi kerak (17.9). Ikkinchi, nomning qolgan qismi hali ham rolni aytishi kerak: `AbstractTemplate` ma'nosiz.

## 3.8 Generik tur parametrlari

Bir harfli generik nomlar an'ana bo'lib qolgan va ularni saqlash kerak: `T` (type), `E` (element), `K`/`V` (key/value), `R` (result), `U` (ikkinchi tur), `N` (number). Bitta yoki ikkita parametrda bu yetarli.

Parametr soni ikkitadan oshsa yoki ma'nosi noaniq bo'lsa, to'liq nom yozish kerak. Konvensiya: bitta katta harf bilan boshlanadigan so'z yoki so'z + `T`.

```java
// an'anaviy va yetarli
public interface Repository<T, ID> { Optional<T> findById(ID id); }

// parametr soni ko'p: ma'noli nom o'qilishni saqlaydi
public interface Pipeline<InputT, OutputT, ContextT> {
    OutputT run(InputT input, ContextT context);
}

// istisno turi uchun an'anaviy harf X
public interface ThrowingSupplier<T, X extends Exception> {
    T get() throws X;
}
```

Bu yerda til spetsifikatsiyasining o'z konvensiyasi bilan ziddiyat chiqadi: JLS tur parametri nomini qisqa, afzal bitta harf va kichik harf bo'lmagan shaklda talab qiladi, shunda u oddiy sinf nomidan ko'zga darhol ajralib turadi; istisno turi uchun an'anaviy harf `X`. Ajratuvchi shart - **parametr soni**. Bir yoki ikki parametrda JLS shakli amal qiladi (`T`, `E`, `K`/`V`, `X`), uchta va undan ko'pida o'qilish ustun turadi; JLS ning o'zi bu yo'lni ochiq qoldiradi, chunki konvensiya ko'r-ko'rona qo'llanmaydi (3.14). Uzun nomga o'tganda ikki shart saqlanadi: nom bosh harf bilan boshlanadi va `T` suffiksi qoladi, shunda tur parametri sinf nomi bilan aralashmaydi.

## 3.9 Metod nomi va qaytish turi muvofiqligi

Nom qaytish turiga mos bo'lmasa, o'quvchi chalg'iydi. `getOrders()` bitta `Order` qaytarsa, `isValid()` `String` qaytarsa, `save()` `void` emas `Long` qaytarsa - har birida yashirin shartnoma bor va u nomda ko'rinmaydi.

| Qaytish turi | Nom shakli | Misol |
|---|---|---|
| `boolean` | `is`/`has`/`can` | `isSettled()` |
| `Optional<T>` | `find` | `findByEmail()` |
| `T` (kafolatlangan) | `get`/`require` | `getById()`, `requireActive()` |
| `List<T>` | ko'plik | `findAllPending()` |
| `void` (o'zgartiradi) | buyruq fe'li | `cancel()`, `markShipped()` |
| `long`/`int` (son) | `count`/`size` | `countPending()` |
| yangi obyekt | `to`/`as`/`with` | `toDto()`, `withDiscount()` |
| yon ta'sirli va qiymatli | ikkiga bo'lish | `reserve()` + `reservationId()` |

Oxirgi qator buyruq-so'rov ajratilishiga ([patternlar hujjatidagi](../patterns/README.md) buyruq-so'rov ajratilishi printsipi) ishora qiladi: bir metod ham o'zgartirsa, ham qiymat qaytarsa, nomi ikkisini ham aytolmaydi.

Jadvalning `to`/`as` qatori amalda uch aniq naqshga bo'linadi va ularni aralashtirish tez-tez uchraydi. `toType` turni o'zgartirib **mustaqil** obyekt qaytaradi (`toString`, `toArray`): manba keyin o'zgarsa, natija o'zgarmaydi. `asType` bir xil ma'lumotning boshqa turdagi **ko'rinishini** qaytaradi (`asList`): manba o'zgarsa, ko'rinish ham o'zgaradi. `typeValue` esa qiymati bir xil primitivni qaytaradi (`intValue`, `longValue`). Nomni to'g'ri tanlash klientga nusxa oldimi yoki ko'rinish oldimi degan savolga imzoning o'zida javob beradi.

O'zgarmas sinfda metod nomining shakli ham boshqacha: amal obyektni o'zgartirmaydi, yangi obyekt qaytaradi, shuning uchun nom buyruq fe'li emas predlog bo'ladi: `plus`, `minus`, `times`, `dividedBy`. `add` nomi obyektni joyida o'zgartirayotgandek o'qiladi. `BigInteger` va `BigDecimal` shu konvensiyani buzgani uchun ularning natijasini o'zlashtirmasdan tashlab yuborish klassik xatoga aylandi (16.4).

## 3.10 Istisno sinflari nomlari

Istisno nomi `Exception` bilan tugaydi va muammoni aytadi, sababini emas. `OrderException` nima bo'lganini aytmaydi; `OrderAlreadyShippedException` aytadi. Nom shunday aniq bo'lsa, `catch` bloki ham aniq bo'ladi va xato bilan ishlash shartlari kodda ko'rinadi.

```java
// yomon: bir istisno hamma holat uchun
throw new OrderException("xato");

// yaxshi: har bir holat o'z turida, kontekst konstruktorda
throw new OrderAlreadyShippedException(orderId, shippedAt);
throw new InsufficientStockException(sku, requested, available);
throw new PaymentDeclinedException(paymentId, gatewayCode);
```

Texnik istisnolarda `Failure` yoki `Error` emas, `Exception` qo'shimchasi qolaveradi; `Error` nomi JVM `java.lang.Error` ierarxiyasini anglatadi va chalkashtiradi.

## 3.11 Paket, modul va artefakt nomlari

Paket nomi kichik harflarda, ko'plik yoki birlikda izchil, va xususiyatni anglatadi ([arxitektor hujjatidagi](../architect/README.md) paketni xususiyat bo'yicha bo'lish bo'limi paketni xususiyat bo'yicha bo'lishni ko'rib chiqadi). Bu yerda qolgan konvensiyalar: qisqartma yo'q, kamalak (`com.company.project.service.impl.v2`) yo'q, `util` paketiga hamma narsani tashlash yo'q.

| Daraja | Konvensiya | Misol |
|---|---|---|
| Guruh | teskari domen | `uz.shop` |
| Modul | xususiyat yoki kontekst | `uz.shop.payment` |
| Ichki qatlam | rol | `uz.shop.payment.api`, `...payment.internal` |
| Artefakt (Maven) | modul nomi bilan bir xil | `shop-payment` |
| Jar/image nomi | artefakt + versiya | `shop-payment:1.4.2` |
| Test paketi | ishlab chiqarish bilan bir xil | `uz.shop.payment` |
| Konfiguratsiya prefiksi | modul nomi | `shop.payment.gateway.*` |

Jadvalga til tomonidan qo'yilgan uch cheklov qo'shiladi. Birinchi: paket yoki modul nomi `java` identifikatori bilan boshlanmaydi, chunki u Java SE platformasining o'zi uchun ajratilgan. Ikkinchi: modul nomi uning asosiy eksport qilinadigan paketi nomiga mos keladi, ya'ni `uz.shop.payment` moduli `uz.shop.payment` paketini eksport qiladi; aks holda `module-info.java` va `import` qatorlari bir-biriga ishora qilmaydi va bog'liqlikni o'qish qiyinlashadi. Uchinchi: nomsiz paket, ya'ni `package` e'lonisiz fayl, faqat kichik yoki vaqtinchalik ilova uchun qoldirilgan - ishlab chiqarish kodida har bir fayl o'z paketiga joylanadi, chunki nomsiz paketdagi sinfni nomlangan paketdan `import` qilib bo'lmaydi.

## 3.12 Test metodi va test sinfi nomlari

Test nomlash konvensiyalari [testlash qo'llanmasidagi](../testing/README.md) test nomlash va AAA bo'limida berilgan. Bu yerda faqat nomlash nuqtai nazaridan ikki qo'shimcha qoida bor. Birinchi, test nomi texnik emas, xatti-harakat tilida bo'lishi kerak: `shouldRejectRefundExceedingSettledAmount`, `test1` emas. Ikkinchi, test sinfi nomi sinab ko'rilayotgan sinfga bog'lanadi: `OrderPricingTest`, `OrderPricingIT` (integratsion).

## 3.13 Fayl, resurs va konfiguratsiya kaliti nomlari

Kod tashqarisidagi nomlar ham o'sha qoidalarga bo'ysunadi, lekin o'z konvensiyasi bor.

| Narsa | Konvensiya | Misol |
|---|---|---|
| Java fayl | public sinf nomi | `OrderPricing.java` |
| Flyway migratsiya | `V<versiya>__<fe'l>_<obyekt>` | `V12__add_settled_at_to_payment.sql` |
| Property kaliti | `kebab-case`, modul prefiksi | `shop.payment.read-timeout` |
| Env o'zgaruvchi | `UPPER_SNAKE` | `SHOP_PAYMENT_READ_TIMEOUT` |
| Jadval, ustun | `snake_case`, birlikda jadval | `payment`, `settled_at` |
| Indeks | `ix_<jadval>_<ustunlar>` | `ix_payment_order_id` |
| Cheklov | `ck_`, `fk_`, `uq_` prefiks | `uq_payment_idempotency_key` |
| Metrika | `<domen>_<obyekt>_<birlik>` | `payment_settlement_seconds` |
| Log kaliti | `camelCase` yoki `snake_case`, izchil | `orderId` |
| Feature flag | `<modul>.<xususiyat>.enabled` | `payment.instant-refund.enabled` |

## 3.14 Jamoa lug'ati va uni majburlash

Nomlash qoidalari lug'at bo'lmasa, har bir ishlab chiquvchining xotirasiga tayanadi. Shuning uchun repoda `docs/glossary.md` fayli turishi kerak: har bir domen atamasi, uning ingliz tilidagi kod shakli, va nima **emasligi**.

```markdown
| Atama (biznes) | Kodda | Ma'nosi | Aralashtirmaslik kerak |
|---|---|---|---|
| Qoldiq | `availableQuantity` | sotishga tayyor miqdor | `onHandQuantity` bilan |
| Rezerv | `reservedQuantity` | buyurtmaga ajratilgan | `availableQuantity` bilan |
| Hisob-kitob | `settlement` | bank bilan yopilishi | `payment` bilan |
| Qaytarish | `refund` | pulni qaytarish | `cancellation` bilan |
```

Majburlash uchun ikki vosita bor: review paytida lug'atga havola qilish, va ArchUnit yoki custom lint qoidasi bilan taqiqlangan nomlarni bloklash (42.4).

Lug'at konvensiyaning chegarasini ham yozadi, chunki konvensiya ko'r-ko'rona qo'llanmaydi: uzoq vaqt qaror topgan an'anaviy nom konvensiyadan ustun turadi. `Math.sin` va `Math.cos` metod nomi uchun to'liq so'z talabini buzadi, lekin ularni `sine` va `cosine` ga o'zgartirish matematika tilidan kelgan o'quvchini chalg'itadi. Shuning uchun lug'atda "istisno" ustuni bo'ladi va har bir istisno sababi bilan yoziladi; aks holda bir xil istisno har review da qaytadan bahsga aylanadi.

## 3.15 Nomni o'zgartirish intizomi

Nomni yaxshilash eng arzon refaktoring, lekin faqat to'g'ri bajarilganda. Uch qoida: IDE refaktoringi bilan qilish (qo'lda almashtirish satr literallarini ham o'zgartirib qo'yadi), alohida commit qilish (mantiq o'zgarishi bilan aralashmasin, 40.1), va public API bo'lsa deprecate siklidan o'tish ([arxitektor hujjatidagi](../architect/README.md) orqaga moslik bo'limi).

```bash
# Nomni o'zgartirish commiti faqat nom o'zgarishini o'z ichiga oladi.
# Diff ni tekshirish: mantiq o'zgarmaganiga ishonch
git show --stat HEAD
git diff HEAD~1 -- '*.java' | grep -E '^\+' | grep -vE 'rename|Rename' | head

# Satr literallari va reflektiv havolalarni alohida tekshirish
grep -rn "orderManager" --include=*.java --include=*.yml --include=*.sql src/
```

## 3.16 Hisoblangan qiymat qo'shimchasi va juft nomlar

Ikki kichik konvensiya nomlarni bir-biriga moslaydi: hisoblangan qiymatning qo'shimchasi qayerda turadi va qarama-qarshi tushunchalar qanday juftlikda nomlanadi. Ikkisi ham o'zicha arzimas, lekin jamoada izchil bo'lmasa, bir xil narsa uchun ikki nom paydo bo'ladi.

**Hisob qo'shimchasi nom oxirida turadi.** `Total`, `Sum`, `Average`, `Max`, `Min`, `Count`, `Index` kabi qo'shimcha nomning oxiriga qo'yiladi: `revenueTotal`, `expenseTotal`, `revenueAverage`, `expenseAverage`. Buning uchta sababi bor (McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 11.1 (263-264-bet)). Birinchisi: nomning eng ma'noli qismi oldinda turadi va birinchi o'qiladi. Ikkinchisi: konvensiya `totalRevenue` va `revenueTotal` ni bitta programmada yonma-yon ishlatishga yo'l qoldirmaydi, holbuki ikkisi bir xil narsa va o'quvchi ularni ikki narsa deb o'ylaydi. Uchinchisi: `revenueTotal`, `expenseTotal`, `revenueAverage` to'plami simmetrik, `totalRevenue`, `expenseTotal`, `averageExpense` esa tartibsiz.

Istisno `Num` bilan bog'liq: boshida turganda u jamini (`numCustomers`), oxirida turganda indeksni (`customerNum`) anglatadi. Shu ikkilik chalkashtirgani uchun McConnell `Num` dan butunlay voz kechishni tavsiya qiladi: jami uchun `Count` yoki `Total`, aniq element uchun `Index` (shu yerda, 11.1 (264-bet)). Ya'ni `customerCount` va `customerIndex`.

Qo'shimcha faqat hisoblangan qiymatga tegishli, tur nomiga emas: `orderList`, `nameString` yoki `priceData` shaklidagi nomlar bu konvensiya bilan oqlanmaydi, ular 2.4 dagi shovqin so'z va 3.2 dagi tur nomini takrorlash qoidalariga tushadi.

**Qarama-qarshi tushunchalar juftlikda nomlanadi.** Juftlikni aniq ishlatish izchillikni, izchillik esa o'qilishni beradi; tabiiy tildagi juftlikdan chiqib ketgan nom esa eslab qolinmaydi. Kitob quyidagi juftliklarni beradi (shu yerda, 11.1 (264-bet)):

| Juftlik | Java da tipik joy |
|---|---|
| `begin` / `end` | oraliq, sahifa chegarasi |
| `first` / `last` | tartiblangan to'plam elementi |
| `min` / `max` | chegara va validatsiya |
| `next` / `previous` | iterator, sahifalash |
| `old` / `new` | audit va o'zgarish tarixi |
| `opened` / `closed` | resurs va hisob holati |
| `locked` / `unlocked` | qulf holati |
| `visible` / `invisible` | UI va eksport maydonlari |
| `source` / `target`, `source` / `destination` | ko'chirish va migratsiya |
| `up` / `down` | tartib va yo'nalish |

Qoida: bitta juftlik tanlanadi va aralashtirilmaydi. `startDate` bilan `endDate` to'g'ri, `startDate` bilan `finishDate` esa ikki juftlikdan yarmini oladi va o'quvchini to'xtatadi.

```java
// yomon: qo'shimcha oldinda, juftlik aralash, Num ikki ma'noda
BigDecimal totalRevenue;
BigDecimal revenueSum;
LocalDate startDate;
LocalDate finishDate;
int numOrders;
int orderNum;

// yaxshi: qo'shimcha oxirida, bitta juftlik, Num yo'q
BigDecimal revenueTotal;
BigDecimal revenueAverage;
LocalDate beginDate;
LocalDate endDate;
int orderCount;
int orderIndex;
```

**Chegara nomi `max_` yoki `min_` bilan boshlanadi va inklyuzivlikni hal qiladi.** Yuqoridagi jadval juftliklarni sanadi, lekin chegaraning o'zi qiymatga kiradimi yoki yo'qmi degan savolga javob bermaydi, va aynan shu joyda off-by-one xatosi tug'iladi. Boswell va Foucher ning misoli: savatda 10 dan ortiq element bo'lmasligi kerak va doimiy `CART_TOO_BIG_LIMIT = 10` deb nomlangan. Nom "shu qiymatgacha" yoki "shu qiymat ham kiradi" degan savolga javob bermaydi, shuning uchun tekshiruvda `>=` va `>` orasidagi tanlov tasodifiy bo'ladi va kod klassik bir-birlik xato beradi.

Yechim nomda: chegaralanayotgan narsaning oldiga `max` yoki `min` qo'yiladi, ya'ni `MAX_ITEMS_IN_CART = 10`. Shunda `max` so'zining o'zi chegara **inklyuziv** ekanini aytadi va tekshiruv o'z-o'zidan to'g'ri chiqadi.

```java
// yomon: nom inklyuzivlikni aytmaydi, tekshiruv tasodifiy
private static final int CART_TOO_BIG_LIMIT = 10;
if (cart.itemCount() >= CART_TOO_BIG_LIMIT) {   // 10 ta ham taqiqlandi
    throw new CartTooLargeException();
}

// yaxshi: max_ inklyuziv chegarani aytadi, tekshiruv aniq
private static final int MAX_ITEMS_IN_CART = 10;
if (cart.itemCount() > MAX_ITEMS_IN_CART) {     // 10 ta ruxsat
    throw new CartTooLargeException();
}
```

Shu ikki konvensiya 2.11 dagi "bitta tushunchaga bitta so'z" qoidasining nom qismiga tegishli aniqlashtirishi: jamoa lug'ati qo'shimcha va juftlik ro'yxatini ham o'z ichiga oladi (3.14).

Ajratilgan funksiya ichidagi qaytish o'zgaruvchisi bu qoidadan chetda qoladi: unga har safar yangi tavsifiy nom o'ylab topish o'rniga jamoada bitta kelishilgan nom beriladi, Fowler ning ikkinchi nashri `result` ni ishlatadi. Sabab shunda: qiymatning ma'nosi funksiya nomida allaqachon aytilgan, o'zgaruvchi nomi esa faqat "bu qaytariladigan qiymat" degan rolni belgilaydi, shuning uchun bu yerda izchillik tavsifiylikdan ustun turadi. Shu konvensiya funksiya ajratish mexanikasini (35.1) hamma joyda bir xil ko'rinishda ushlab turadi va diff ni o'qishni osonlashtiradi.

## 3.17 Registr, akronim va grammatik shakl

O'zgaruvchini kichik, turni bosh harf bilan yozish shunchaki uslub emas: u nomga murojaat qilish imkonini saqlab turadi. Bitta oddiy nom bir vaqtda o'zgaruvchi, tur va paket bo'lishi mumkin, shunday to'qnashuvda til o'zgaruvchini turdan, turni paketdan ustun tanlaydi (obscuring). Ya'ni tur `payment` deb nomlansa va shu nomli o'zgaruvchi qamrovda bo'lsa, turga oddiy nom bilan murojaat qilish imkoni yo'qoladi va har joyda to'liq nom yozishga to'g'ri keladi.

Identifikatorda `$` belgisi tilda ruxsat etilgan, lekin u mashina generatsiya qilgan nomlar (ichki sinf, proxy, kompilyator yasagan ko'prik metod) uchun qoldirilgan: qo'lda yozilgan kodda `$` ishlatilmaydi.

Akronim registri alohida kelishuvni talab qiladi, chunki ikki shakl ham uchraydi: faqat birinchi harfni katta yozish (`HttpUrl`, `XmlParser`) yoki butun akronimni katta yozish (`HTTPURL`). Birinchisi tanlanadi, chunki ikkinchi shaklda ketma-ket kelgan ikki akronimning chegarasi ko'rinmaydi. Metod yoki maydon nomi akronim bilan boshlansa, akronim butunlay kichik yoziladi: `httpUrl`, `xmlParser`.

Grammatik shakl ham nom turiga bog'lanadi: instansiyalanadigan sinf birlikdagi ot (`Order`, `PaymentGateway`), instansiyalanmaydigan utility sinf ko'plikdagi ot (`Collections`, `Files`, 14.8), interfeys esa sinf kabi ot yoki `-able` va `-ible` bilan tugaydigan sifat (`Runnable`, `Comparable`).

```java
// yomon: tur kichik harf bilan, akronim butunlay katta, utility sinf birlikda
class payment { }
class HTTPURLBuilder { }
final class StringUtil { private StringUtil() { } }

// yaxshi
class Payment { }
class HttpUrlBuilder { }
final class Strings { private Strings() { } }
interface Retryable { void retry(); }
```

## 3.18 Amalda qo'llash

- [ ] Barcha mantiqiy maydon va metodlarni ko'rib, inkor nomlarni (`isNot...`, `disable...`) ijobiy shaklga o'tkazing.
- [ ] Vaqt, hajm va pul bilan ishlaydigan public imzolarda birlikni turga ko'chiring: `Duration`, `Money`, `Percentage`.
- [ ] `...Impl` va `Default...` nomli sinflarni topib, har biriga mexanikasini aytuvchi nom bering.
- [ ] Enum a'zolari ichida raqamli yoki qisqartma nomlar bo'lsa, kodni ichki maydonga ko'chirib nomni o'qiladigan qiling.
- [ ] `docs/glossary.md` yaratib, domen eksperti ishlatadigan 20 atamani kod shakli bilan yozib qo'ying.
- [ ] Metod nomlari va qaytish turlari muvofiqligini 3.9 jadvali bo'yicha tekshirib, mos kelmaganlarini qayta nomlang.
- [ ] Flyway, property, jadval va metrika nomlanishini 3.13 jadvaliga moslab, farqlarni bitta migratsiyada tuzating.
- [ ] Nom o'zgartirish uchun alohida commit qoidasini jamoa kelishuviga kiritib, PR shabloniga eslatma qo'shing.
- [ ] `total...`, `avg...` shaklidagi nomlarni qo'shimchasi oxirida turadigan shaklga o'tkazib, `Num` ni `Count` va `Index` ga ajratib yozing (3.16).

## Manbalar

- Dustin Boswell, Trevor Foucher, *The Art of Readable Code*, 1-nashr, O'Reilly, 2011 (copyright 2012), 3-bob (25-bet) - chegara nomini `max_` yoki `min_` bilan boshlash, `CART_TOO_BIG_LIMIT` ning inklyuzivlikni aytmasligi va shundan kelib chiqadigan off-by-one xatosi
- Robert C. Martin, *Clean Code*, 2-bob ("Class Names", "Method Names") - sinf nomi ot, metod nomi fe'l, getter konvensiyasi
- Joshua Bloch, *Effective Java* 3rd, Item 68 - umumiy qabul qilingan nomlash konvensiyalari (tipografik va grammatik)
- Joshua Bloch, *Effective Java* 3rd, Item 34 - `int` konstanta o'rniga enum va enum a'zolari nomi
- Robert C. Martin, *Clean Code*, 17-bob, N7 - nom yon ta'sirni aytsin
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 11.1
  (263-264) - hisoblangan qiymat qo'shimchasining nom oxirida turishi va uning
  uch sababi, `Num` qo'shimchasining ikki ma'nosi va `Count`/`Index` ga
  o'tish tavsiyasi, qarama-qarshi nom juftliklari ro'yxati
- Dustin Boswell, Trevor Foucher, *The Art of Readable Code*, 1-nashr, O'Reilly, 2011 (copyright 2012), 2-bob (16-17-betlar) - birlik qoidasining umumlashmasi: xavfli yoki kutilmagan xususiyatni nomga yozish (`plaintext_password`, `unescaped_comment`, `html_utf8`, `data_urlenc`), chegarasi va Hungarian notation dan farqi
- Joshua Bloch, *Effective Java* 3rd, Item 15 (76-bet) - `public static final` massiv maydonining xavfsizlik tuynugi: uzunligi noldan katta massiv hamisha o'zgaradi, yechim `private` massiv va o'zgarmas `List` yoki nusxa qaytaruvchi metod
- Joshua Bloch, *Effective Java* 3rd, Item 34 (158-bet) - `int` enum qiymatlarining klientga kompilyatsiya vaqtida ko'chirilishi va qiymat o'zgarganda klientning qayta kompilyatsiyasiz jim xato ishlashi; `enum` da a'zo qo'shish yoki tartibini o'zgartirish klientni buzmasligi
- Joshua Bloch, *Effective Java* 3rd, Item 17 (82-bet) - o'zgarmas sinfda amal yangi obyekt qaytarishi va metod nomining fe'l emas predlog bo'lishi (`plus`, `minus`), `BigInteger` ning shu konvensiyani buzgani
- Joshua Bloch, *Effective Java* 3rd, Item 68 (290-bet) - akronimda faqat birinchi harfni katta yozish (`HttpUrl`, `HTTPURL` emas) va metod yoki maydon nomining boshidagi akronimning butunlay kichik yozilishi
- Joshua Bloch, *Effective Java* 3rd, Item 68 (291-bet) - grammatik konvensiya: instansiyalanadigan sinf birlikda ot, utility sinf ko'plikda ot (`Collections`), interfeys sinf kabi yoki `-able`/`-ible` bilan tugaydigan sifat
- Joshua Bloch, *Effective Java* 3rd, Item 68 (292-bet) - `toType`, `asType` va `typeValue` metod nomlarining uch xil ma'nosi: mustaqil obyekt, boshqa turdagi ko'rinish, bir xil qiymatli primitiv
- *The Java Language Specification, Java SE 25 Edition* (Gosling, Joy, Steele, Bracha, Buckley, Smith, Bierman), 6-bob (155-bet) - tur parametri nomi qisqa, afzal bitta harf va kichik harf bo'lmasligi, istisno turi uchun `X`, va konvensiyaning ko'r-ko'rona qo'llanmasligi ("should not be followed slavishly")
- *The Java Language Specification, Java SE 25 Edition* (Gosling, Joy, Steele, Bracha, Buckley, Smith, Bierman), 6-bob (156-157-betlar) - paket va modul nomi `java` identifikatori bilan boshlanmasligi, modul nomining asosiy eksport qilinadigan paket nomiga mos kelishi
- *The Java Language Specification, Java SE 25 Edition* (Gosling, Joy, Steele, Bracha, Buckley, Smith, Bierman), 6-bob (180-bet) - obscuring: bir xil oddiy nomda o'zgaruvchining turdan, turning paketdan ustun tanlanishi va shundan kelib chiqadigan registr konvensiyasining sababi
- *The Java Language Specification, Java SE 25 Edition* (Gosling, Joy, Steele, Bracha, Buckley, Smith, Bierman), 7-bob (422-bet) - nomsiz paketning faqat kichik yoki vaqtinchalik ilova uchun qoldirilgani
- Y. Daniel Liang, *Introduction to Java Programming*, 9-nashr, Pearson, 2013, 2-bob (40-bet) - identifikatorda `$` belgisining mashina generatsiya qilgan kod uchun qoldirilgani
- Martin Fowler, *Refactoring*, 2-nashr, Addison-Wesley, 2019, 1-bob (22-bet) - ajratilgan funksiyadagi qaytish o'zgaruvchisini bitta kelishilgan nom (`result`) bilan atash konvensiyasi
- ESLATMA: `PERMITTED_CODES` va registr konvensiyasining kod misollari korpus qo'shimchasi; kitoblar qoidani nasr bilan beradi, bu misollar uni Java shaklida ko'rsatish uchun yozilgan

---

[&larr; 2. Nomlash qoidalari: maqsadni ochib beruvchi nom](02-nomlash-qoidalari-maqsadni-ochib-beruvchi.md) · [Mundarija](README.md) · [4. Funksiya: kichiklik va bitta ish &rarr;](04-funksiya-kichiklik-va-bitta-ish.md)
