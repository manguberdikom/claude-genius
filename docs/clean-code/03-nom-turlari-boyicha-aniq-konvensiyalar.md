<!-- doc: clean-code | chapter: 3 | part: I. Toza kodning asosi -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

# 3. Nom turlari bo'yicha aniq konvensiyalar (Naming Conventions by Kind)

<details>
<summary>Bu bobdagi 16 bo'lim</summary>

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
- [3.16 Amalda qo'llash](#316-amalda-qollash)

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
```

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

## 3.16 Amalda qo'llash

- [ ] Barcha mantiqiy maydon va metodlarni ko'rib, inkor nomlarni (`isNot...`, `disable...`) ijobiy shaklga o'tkazing.
- [ ] Vaqt, hajm va pul bilan ishlaydigan public imzolarda birlikni turga ko'chiring: `Duration`, `Money`, `Percentage`.
- [ ] `...Impl` va `Default...` nomli sinflarni topib, har biriga mexanikasini aytuvchi nom bering.
- [ ] Enum a'zolari ichida raqamli yoki qisqartma nomlar bo'lsa, kodni ichki maydonga ko'chirib nomni o'qiladigan qiling.
- [ ] `docs/glossary.md` yaratib, domen eksperti ishlatadigan 20 atamani kod shakli bilan yozib qo'ying.
- [ ] Metod nomlari va qaytish turlari muvofiqligini 3.9 jadvali bo'yicha tekshirib, mos kelmaganlarini qayta nomlang.
- [ ] Flyway, property, jadval va metrika nomlanishini 3.13 jadvaliga moslab, farqlarni bitta migratsiyada tuzating.
- [ ] Nom o'zgartirish uchun alohida commit qoidasini jamoa kelishuviga kiritib, PR shabloniga eslatma qo'shing.

---

[&larr; 2. Nomlash qoidalari: maqsadni ochib beruvchi nom](02-nomlash-qoidalari-maqsadni-ochib-beruvchi.md) · [Mundarija](README.md) · [4. Funksiya: kichiklik va bitta ish &rarr;](04-funksiya-kichiklik-va-bitta-ish.md)
