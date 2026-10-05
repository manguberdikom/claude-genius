<!-- doc: architect | chapter: 4 | part: I. Fikrlash va qarorlar -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyyasi](README.md)

# 4. Kod - muloqot vositasi: nomlash, aniqlik, kognitiv yuk (Code as Communication)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

- [4.1 Kod yozishdan ko'ra o'qishga ko'p vaqt ketadi](#41-kod-yozishdan-kora-oqishga-kop-vaqt-ketadi)
- [4.2 Nomlash: domen tilidan nom olish](#42-nomlash-domen-tilidan-nom-olish)
- [4.3 Kognitiv yuk: bir metodni tushunish uchun nechta narsa](#43-kognitiv-yuk-bir-metodni-tushunish-uchun-nechta-narsa)
- [4.4 Metod uzunligi, ichma-ich shartlar va erta qaytish](#44-metod-uzunligi-ichma-ich-shartlar-va-erta-qaytish)
- [4.5 Izoh qachon kerak: "nima" emas, "nega"](#45-izoh-qachon-kerak-nima-emas-nega)
- [4.6 Xato va istisnolar orqali muloqot](#46-xato-va-istisnolar-orqali-muloqot)
- [4.7 Tur tizimidan foydalanish](#47-tur-tizimidan-foydalanish)
- [4.8 Paket tuzilishi: xususiyat bo'yicha bo'lish](#48-paket-tuzilishi-xususiyat-boyicha-bolish)
- [4.9 Kodda yashirin bilim](#49-kodda-yashirin-bilim)
- [4.10 O'zini hujjatlaydigan API](#410-ozini-hujjatlaydigan-api)
- [4.11 Amalda qo'llash](#411-amalda-qollash)

</details>



Kod ikki marta ishlatiladi: bir marta kompilyator uchun, qolgan yuz marta odam uchun. Kompilyator uchun ishlaydigan kod yozish past bar, chunki buni statik tahlil ham tekshiradi. Arxitektor uchun asosiy savol boshqa: ertaga bu metodga kelgan, domenni bilmaydigan odam uni to'g'ri o'zgartira oladimi. Shu bobda kod yozishni muloqot kanali sifatida ko'rib chiqamiz, va shu kanalning o'tkazuvchanligini oshiradigan aniq qarorlarni sanab o'tamiz.

## 4.1 Kod yozishdan ko'ra o'qishga ko'p vaqt ketadi

To'lov servisining hayot sikliga qarang. `PaymentAuthorizationService` bir hafta yozildi, keyin uch yil davomida o'qildi: incident vaqtida, audit vaqtida, yangi to'lov provayderi qo'shilganda, PCI tekshiruvida. Amaliyotda bitta metodni o'zgartirish uchun uni o'qiydigan odam o'zgartirishdan taxminan 5-10 barobar ko'p vaqt o'qishga sarflaydi. Bu nisbat qoida chiqaradi: yozishni qiyinlashtirib o'qishni osonlashtiradigan har qanday almashuv foydali.

Shundan kelib chiqadigan amaliy qoidalar qisqa. Birinchi, qisqa nom yozish vaqtini tejaydi, lekin o'qish vaqtini oshiradi, demak yutqazadi. Ikkinchi, "aqlli" bir qatorli ifoda yozuvchiga zavq beradi, o'quvchini sekinlashtiradi. Uchinchi, kodni tushunish uchun debugger ishga tushirish kerak bo'lsa, bu kod muloqotda muvaffaqiyatsiz bo'lgan.

```java
// yomon: nima qaytadi, qanday tartibda, nega filter shunday - hammasi yashirin
public List<Object[]> proc(Long id, int t) {
    return repo.find(id, t).stream()
        .filter(r -> r[3] != null && ((Integer) r[2]) > 0)
        .sorted((a, b) -> ((Date) b[1]).compareTo((Date) a[1]))
        .toList();
}

// yaxshi: tur, nom va tartib kodning o'zida aytilgan
public List<SettledPayment> findSettledPayments(OrderId orderId, Period period) {
    return paymentRepository.findByOrder(orderId, period).stream()
        .filter(Payment::isSettled)          // faqat bank tomonidan yopilganlar
        .sorted(comparing(Payment::settledAt).reversed())  // yangi birinchi
        .map(SettledPayment::from)
        .toList();
}
```

## 4.2 Nomlash: domen tilidan nom olish

Yaxshi nom domen mutaxassisi aytadigan so'z bo'ladi. Ombor bo'limi "qoldiq", "rezerv", "yo'lda" deb gapiradi, shuning uchun kodda `availableQuantity`, `reservedQuantity`, `inTransitQuantity` bo'lishi kerak, `qty1` va `qty2` emas. Agar domen eksperti bilan suhbatda ishlatilgan so'z kodda yo'q bo'lsa, demak tarjima qatlami bor, va har bir tarjima xato manbasi.

Qisqartma eng qimmat tejamkorlik. `calcAmt`, `pmtSts`, `ordHdr` kabi nomlar har o'qishda ongda qayta ochiladi. Faqat domenda rasman qabul qilingan qisqartmalar qoladi: `IBAN`, `VAT`, `SKU`, `TTL`. Qolgan hamma joyda to'liq so'z yoziladi, chunki IDE yozishni o'zi tugatadi.

`Manager`, `Helper`, `Util`, `Processor`, `Data`, `Info` qo'shimchalari alohida tuzoq. `OrderManager` nima qiladi degan savolga javob yo'q, shuning uchun unga hamma narsa to'planadi va u 2000 qatorga yetadi. Nom javobgarlikni cheklamasa, sinf ham cheklanmaydi. Yechim: nomni fe'ldan yoki aniq roldan chiqarish. `OrderManager` o'rniga `OrderPlacement`, `OrderCancellation`, `OrderPricing`. `PaymentHelper` o'rniga `PaymentRetryPolicy` va `CardNumberMasker`.

| Mavzu | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Sinf nomi | `OrderManager` hamma narsani yig'adi | `OrderPlacement`, `OrderCancellation` alohida |
| Metod nomi | `process(order)` | `reserveStockFor(order)` |
| Mantiqiy flag | `boolean flag` | `boolean stockAlreadyReserved` |
| Pul miqdori | `BigDecimal amount` | `Money amount` (valyuta bilan) |
| Xato belgisi | `return null` | `Optional<Invoice>` yoki domen xatosi |
| Izoh | kod nima qilishini takrorlaydi | nega shunday qilinganini yozadi |
| Metod imzosi | `save(Long, int, String)` | `save(OrderId, Quantity, WarehouseCode)` |
| Paket | `service`, `dto`, `util` | `order`, `payment`, `inventory` |
| Istisno | `throw new RuntimeException("err")` | `InsufficientStockException(sku, requested, available)` |
| Magic number | `if (status == 3)` | `if (status == OrderStatus.SHIPPED)` |

## 4.3 Kognitiv yuk: bir metodni tushunish uchun nechta narsa

Odamning ishchi xotirasi bir vaqtda taxminan 4-7 ta mustaqil elementni ushlab turadi. Metodni o'qiyotgan odam shu sig'imdan foydalanadi: har bir mahalliy o'zgaruvchi, har bir shart, har bir nomsiz shart bitta slot egallaydi. Metodda 12 ta o'zgaruvchi va 5 ta shart bo'lsa, o'quvchi sig'imdan chiqadi va qog'ozga yozib o'qishga o'tadi.

Shuning uchun amaliy o'lchov bor: metodga kirgandan keyin oxirigacha yodda tutish kerak bo'lgan narsalar sonini sanash. To'rtta yoki beshtadan ko'p bo'lsa, metodni bo'lish kerak. Bu "metod 20 qatordan oshmasin" qoidasidan aniqroq, chunki 40 qatorli to'g'ri chiziqli metod 10 qatorli ichma-ich shartlardan osonroq.

Kognitiv yukni kamaytiradigan uchta kuchli harakat bor. Shartni nomli mantiqiy o'zgaruvchiga chiqarish, chunki nom bir slotga joylashadi, ifoda esa uchta slotni oladi. Mahalliy o'zgaruvchi hayot muddatini qisqartirish, ideal holda e'lon qilingan joyda ishlatish. Metod ichida abstraksiya darajasini bir xil ushlash, ya'ni bir metodda ham SQL, ham narx hisoblash, ham audit log bo'lmasligi.

```java
// yomon: o'quvchi 6 ta shartni bir vaqtda yodda tutishi kerak
if (order.getStatus() == 2 && order.getItems().size() > 0
        && order.getCustomer().getBalance().compareTo(order.getTotal()) >= 0
        && !order.getCustomer().isBlocked()
        && order.getCreatedAt().isAfter(LocalDateTime.now().minusDays(30))) {
    ship(order);
}

// yaxshi: har bir shart nomlangan, o'quvchi 3 ta tushunchani ushlaydi
boolean paymentCovered = customer.hasBalanceFor(order.total());
boolean customerAllowed = !customer.isBlocked();
boolean withinShippingWindow = order.createdWithin(Duration.ofDays(30));

if (order.isConfirmed() && paymentCovered && customerAllowed && withinShippingWindow) {
    ship(order);
}
```

## 4.4 Metod uzunligi, ichma-ich shartlar va erta qaytish

Ichma-ich shartlar chuqurligi o'qish narxini chiziqli emas, ko'rsatkichli oshiradi. Uchinchi darajadagi `if` ichida turgan o'quvchi yuqoridagi ikki shartni ham yodda tutadi. Amaliy chegara: bitta metodda ikki darajadan chuqur bormaslik, uchinchi daraja paydo bo'lsa, ichkarini alohida metodga chiqarish.

Erta qaytish shu muammoni eng arzon yechadi. Metod boshida barcha yaroqsiz holatlarni tekshirib qaytarilsa, qolgan tana faqat "to'g'ri yo'l" bo'lib qoladi. Bu "guard clause" uslubi, va uning foydasi psixologik: o'quvchi tekshirilgan shartni xotiradan o'chirib yuboradi, chunki u boshqa qaytib kelmaydi.

```java
// yomon: 4 daraja chuqurlik, to'g'ri yo'l eng ichkarida yashiringan
public void refund(RefundRequest request) {
    if (request != null) {
        Payment payment = repo.find(request.paymentId());
        if (payment != null) {
            if (payment.isSettled()) {
                if (request.amount().compareTo(payment.amount()) <= 0) {
                    gateway.refund(payment, request.amount());
                }
            }
        }
    }
}

// yaxshi: yaroqsiz holatlar boshida tugaydi, oxirida faqat biznes amali qoladi
public void refund(RefundRequest request) {
    Payment payment = paymentRepository.findById(request.paymentId())
            .orElseThrow(() -> new PaymentNotFoundException(request.paymentId()));

    if (!payment.isSettled()) {
        throw new PaymentNotSettledException(payment.id(), payment.status());
    }
    if (request.amount().greaterThan(payment.refundableAmount())) {
        throw new RefundExceedsPaymentException(payment.id(), request.amount());
    }
    gateway.refund(payment, request.amount());
}
```

## 4.5 Izoh qachon kerak: "nima" emas, "nega"

Kod nima qilishini o'zi aytadi, shuning uchun uni takrorlagan izoh shovqin. Bundan yomoni, bu izoh kod o'zgarganda yangilanmaydi va yolg'onga aylanadi. Qoida oddiy: izoh kodda ko'rinmaydigan ma'lumot bersa qoladi, aks holda o'chiriladi.

Kodda ko'rinmaydigan to'rt xil ma'lumot bor. Birinchi, nega aynan shu yechim tanlangan va qaysi muqobil rad etilgan. Ikkinchi, tashqi dunyoning cheklovi, masalan provayder API si kunda 100 ta so'rovga ruxsat beradi. Uchinchi, matematik yoki huquqiy formulaning manbasi, masalan soliq hisoblash qoidasining rasmiy havolasi. To'rtinchi, vaqtinchalik yechim va uni olib tashlash sharti.

```java
// yomon: kod nima qilishini takrorlaydi
// pool kattaligini 20 ga o'rnatadi
hikariConfig.setMaximumPoolSize(20);

// yaxshi: qarorning asosi va chegarasi yozilgan
// PostgreSQL da max_connections = 100, bizda 4 ta instance ishlaydi.
// 4 x 20 = 80, qolgan 20 ta replikatsiya va admin ulanishlari uchun zaxira.
// Instance soni oshsa, bu qiymatni qayta hisoblash kerak.
hikariConfig.setMaximumPoolSize(20);

// yaxshi: tashqi cheklov kodda ko'rinmaydi, shuning uchun yoziladi
// Bank gateway bir IBAN uchun soatda 3 ta tekshiruvga ruxsat beradi (shartnoma 4.2).
// Shundan ortig'i 429 qaytaradi va 24 soat blok bo'ladi.
@RateLimiter(name = "ibanValidation")
public ValidationResult validate(Iban iban) { ... }
```

## 4.6 Xato va istisnolar orqali muloqot

Istisno xabari eng ko'p o'qiladigan matn, chunki uni production incidentida yarim tunda o'qiydilar. `RuntimeException("error")` kabi xabar muloqotni butunlay to'xtatadi. Yaxshi istisno uchta savolga javob beradi: nima bo'lmadi, qaysi obyekt bilan, va kutilgan holat qanday edi.

Arxitektura darajasida muhim qaror: domen xatolarini texnik xatolardan ajratish. "Omborda qoldiq yetmaydi" biznes holati, u kutilgan va uni foydalanuvchiga ko'rsatish kerak. "Ulanish uzildi" texnik holat, u retry va alert talab qiladi. Ikkisi bir xil tipda bo'lsa, chaqiruvchi ularni ajrata olmaydi va `catch (Exception e)` yozadi.

Xato kodlari API chegarasida alohida qiymat beradi. Kod mashina uchun, xabar odam uchun. Kodi bor xato mijoz tomonida ishlov berishni barqaror qiladi, chunki xabar matnini o'zgartirish mijozni buzmaydi.

```java
// yomon: kontekst yo'q, tip yo'q, log da faqat stack trace qoladi
if (stock < qty) {
    throw new RuntimeException("not enough");
}

// yaxshi: kontekst, domen tipi va mashina o'qiydigan kod
public final class InsufficientStockException extends BusinessException {
    private final Sku sku;
    public InsufficientStockException(Sku sku, int requested, int available) {
        super("INVENTORY_INSUFFICIENT_STOCK",
              "SKU %s uchun %d dona so'raldi, omborda %d dona bor"
                  .formatted(sku.value(), requested, available));
        this.sku = sku;
    }
}
// chaqiruvchi tomonda ajratish aniq bo'ladi
try {
    reservation.reserve(sku, quantity);
} catch (InsufficientStockException e) {
    return OrderResult.rejected(e.errorCode(), e.getMessage()); // biznes holati
} catch (DataAccessResourceFailureException e) {
    throw new RetryableInfrastructureException(e);              // texnik holat
}
```

## 4.7 Tur tizimidan foydalanish

Tur tizimi hujjatning kompilyator tekshiradigan qismi. Java 17 dan keyin bu kanalning kengligi sezilarli oshdi. `record` ma'lumot tashuvchini bir qatorda e'lon qiladi va `equals`, `hashCode`, `toString` ni o'zi beradi. `sealed interface` esa holatlar to'liq ro'yxatini e'lon qiladi, va `switch` da yangi holat qo'shilganda kompilyator xato beradi.

Value object primitiv obsessiyasini davolaydi. `String warehouseCode` va `String sku` o'rin almashsa kompilyator jim turadi, `WarehouseCode` va `Sku` bo'lsa esa kompilyatsiya buziladi. Bu xatoni runtime dan compile time ga ko'chiradi, ya'ni eng arzon joyga.

`Optional` qaytuvchi qiymat uchun, maydon yoki parametr uchun emas. Repository metodida `Optional<Order>` chaqiruvchiga "yo'q bo'lishi normal" degan xabarni beradi. `null` qaytarish esa hech narsa demaydi, shuning uchun chaqiruvchi tekshirishni esdan chiqaradi.

```java
// yomon: holatlar ro'yxati hech qayerda e'lon qilinmagan, string bilan ishlanadi
public String handle(String paymentResult, String code) {
    if ("OK".equals(paymentResult)) return "confirmed";
    if ("DECLINED".equals(paymentResult)) return "rejected:" + code;
    return "unknown";
}

// yaxshi: holatlar to'liq, switch da yangi holat qo'shilsa kompilyator ogohlantiradi
public sealed interface PaymentResult {
    record Authorized(TransactionId id, Money amount) implements PaymentResult {}
    record Declined(DeclineReason reason) implements PaymentResult {}
    record PendingReview(Duration expectedWait) implements PaymentResult {}
}

OrderDecision decide(PaymentResult result) {
    return switch (result) {
        case PaymentResult.Authorized a -> OrderDecision.confirm(a.id());
        case PaymentResult.Declined d -> OrderDecision.reject(d.reason());
        case PaymentResult.PendingReview p -> OrderDecision.hold(p.expectedWait());
    };
}
```

## 4.8 Paket tuzilishi: xususiyat bo'yicha bo'lish

Qatlam bo'yicha bo'lish, ya'ni `controller`, `service`, `repository`, `dto`, birinchi qarashda tartibli ko'rinadi. Amalda u eng muhim ma'lumotni yashiradi: tizim nima qiladi. `service` paketini ochgan odam 40 ta sinf ko'radi va ularning qaysi biri birga ishlashini bilmaydi. Bundan tashqari bitta funksiyani o'zgartirish 4 ta paketni ochishni talab qiladi.

Xususiyat bo'yicha bo'lishda yuqori daraja domenni aytadi: `order`, `payment`, `inventory`, `invoicing`. Har bir paket ichida o'z controller va repository si turadi. Buning ikki amaliy foydasi bor. Birinchi, `package-private` ko'rinishi haqiqatan ishlaydi, chunki bir xususiyatning ichki sinflari tashqariga chiqmaydi. Ikkinchi, modulni ajratish paytida paketni ko'chirish yetarli bo'ladi.

```bash
# yomon: qatlam bo'yicha, "tizim nima qiladi" ko'rinmaydi
com/shop/controller/{OrderController,PaymentController,StockController}.java
com/shop/service/{OrderService,PaymentService,StockService,...37 ta}.java
com/shop/repository/...
com/shop/dto/...

# yaxshi: xususiyat bo'yicha, chegaralar ko'rinadi
com/shop/order/{OrderController,OrderPlacement,OrderRepository,Order}.java
com/shop/payment/{PaymentController,PaymentAuthorization,PaymentGateway}.java
com/shop/inventory/{StockReservation,StockLevel,InventoryRepository}.java
com/shop/shared/money/{Money,Currency}.java   # faqat haqiqiy umumiy narsalar
```

Bu qarorni gap bilan emas, test bilan ushlab turish kerak. ArchUnit qoidasi `payment` paketidan `order` ning ichki sinflariga ulanishni taqiqlaydi, va shu bilan chegara hujjatdan kodga ko'chadi. Batafsil qoidalarni [testlash qo'llanmasidagi](../testing/README.md) arxitektura testlari bo'limida ko'rish mumkin.

## 4.9 Kodda yashirin bilim

Eng qimmat xatolar kodda yozilmagan bilim atrofida tug'iladi. Magic number buning eng ko'rinadigan shakli. `if (daysLate > 15)` ni o'qigan odam 15 ning qaydan kelganini bilmaydi, shuning uchun uni o'zgartirishga qo'rqadi yoki noto'g'ri o'zgartiradi. Nomli konstanta bu bilimni kodga qaytaradi: `MAX_GRACE_PERIOD_DAYS`.

Ikkinchi shakl yashirin tartib. Agar `validate()` ni `calculate()` dan oldin chaqirish kerak bo'lsa, lekin buni faqat muallif bilsa, bu bilim yo'qoladi. To'g'ri yechim tartibni imkonsiz qilish, masalan `calculate()` ni faqat `ValidatedOrder` tipidan qabul qiladigan qilish. Uchinchi shakl kutilmagan yon ta'sir: nomi `get` bilan boshlanadigan metod cache ni yangilasa yoki audit log yozsa, chaqiruvchi buni kutmaydi.

| Tuzoq | Nega xavfli | Yechim |
|---|---|---|
| `if (status == 3)` | 3 ning ma'nosi faqat SQL da yozilgan | `enum OrderStatus` va `@Enumerated(STRING)` |
| `Thread.sleep(500)` kutish | nega 500 ms, qanday sharoitda yetadi | nomli timeout konstanta va kommentda asos |
| `getBalance()` ichida yozish | tranzaksiyada kutilmagan UPDATE | `get` faqat o'qiydi, yozish `recalculate...()` |
| Yashirin chaqiruv tartibi | yangi developer tartibni buzadi | tipni o'zgartirish, `ValidatedOrder` kabi |
| `BigDecimal` da valyuta yo'q | USD va UZS qo'shilib ketadi | `Money(amount, currency)` value object |
| `List<String>` parametrlar | nima uchun ekani nomsiz | `record StockFilter(Set<Sku> skus, ...)` |
| Bo'sh `catch` bloki | xato yo'qoladi, incident ko'rinmaydi | log yoki qayta throw, albatta kontekst bilan |
| Statik util holat ushlaydi | test lar bir-biriga ta'sir qiladi | bean qilish, holatni argumentga ko'chirish |

## 4.10 O'zini hujjatlaydigan API

Public API uchun to'rtta kanal bor, va ularni birga ishlatish kerak. Birinchi kanal nom: metod nomi natijani va yon ta'sirni aytadi. Ikkinchi kanal imzo: parametr turlari noto'g'ri chaqiruvni imkonsiz qiladi. Uchinchi kanal Javadoc: faqat kod aytolmaydigan narsani yozadi, ya'ni shartnomani, tranzaksiya talabini, idempotentlikni va tashlanadigan istisnolarni. To'rtinchi kanal test nomlari: ular bajariladigan hujjat, chunki eskirsa qizil bo'ladi.

```java
// yomon: nom, imzo va hujjat hech narsa aytmaydi
/** Hisob-faktura yaratadi. */
public Invoice create(Long id, boolean b, int t) { ... }

// yaxshi: imzo chaqiruvni cheklaydi, Javadoc shartnomani aytadi
/**
 * Yopilgan buyurtma uchun hisob-faktura chiqaradi.
 * Idempotent: bir buyurtma uchun qayta chaqirilsa, mavjud fakturani qaytaradi.
 * Mavjud tranzaksiya talab qiladi (REQUIRED), o'zi tranzaksiya ochmaydi.
 *
 * @throws OrderNotClosedException buyurtma hali yopilmagan bo'lsa
 */
public Invoice issueInvoice(OrderId orderId, VatPolicy vatPolicy) { ... }
```

Test nomlari shu hujjatning davomi. `testCreate1` nomi hech kimga yordam bermaydi, `issueInvoice_returnsExistingInvoice_whenCalledTwiceForSameOrder` esa shartnomani takrorlaydi va buzilganda aynan qaysi kelishuv buzilganini aytadi. Arxitektor uchun amaliy o'lchov shu: public metod uchun yozilgan test nomlarini ketma-ket o'qib chiqqanda, u metodning shartnomasi tiklanishi kerak.

## 4.11 Amalda qo'llash

- [ ] Eng ko'p o'zgaradigan 5 ta sinfni tanlab, nomlaridan `Manager`, `Helper`, `Util`, `Processor` qo'shimchalarini olib tashlang va javobgarlik bo'yicha bo'ling.
- [ ] Domen eksperti ishlatadigan 15 ta atamani ro'yxat qilib, kodda ularning qanday yozilganini tekshiring; farq bo'lsa kodni domenga moslang.
- [ ] Eng murakkab 3 ta metodda ichma-ich shartlarni erta qaytishga aylantirib, chuqurlikni ikki darajadan oshmasligiga keltiring.
- [ ] Pul, SKU, ombor kodi va buyurtma identifikatori uchun value object joriy qiling, `String` va `BigDecimal` ni public imzolardan chiqaring.
- [ ] Barcha `throw new RuntimeException(...)` chaqiruvlarini topib, ularni kontekst va xato kodi bor domen yoki infratuzilma istisnolariga ajratib bering.
- [ ] Bitta xususiyatni (masalan to'lov) qatlam paketlaridan `payment` paketiga ko'chirib, ichki sinflarni `package-private` qiling va chegarani ArchUnit qoidasi bilan mahkamlang.
- [ ] Kodni magic number uchun skanerlang (timeout, retry soni, limit, kun soni) va har birini nomli konstanta va asosni aytuvchi izoh bilan almashtiring.
- [ ] Public API ning 10 ta metodida Javadoc ni "nima" dan "shartnoma" ga qayta yozing: idempotentlik, tranzaksiya talabi, tashlanadigan istisnolar.

---

[&larr; 3. Qaror qabul qilish va uni hujjatlashtirish](03-qaror-qabul-qilish-va-uni-hujjatlashtirish.md) · [Mundarija](README.md) · [5. Abstraksiya hissi, bog'liqlik va chegaralar &rarr;](05-abstraksiya-hissi-bogliqlik-va-chegaralar.md)
