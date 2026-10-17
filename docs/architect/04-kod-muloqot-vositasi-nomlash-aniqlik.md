<!-- doc: architect | chapter: 4 | part: I. Fikrlash va qarorlar -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

> Holat: tekshirilmoqda. Da'volar hali manbaga solishtirilmoqda.

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



Kod ikki manzilga yoziladi: kompilyator uchun va odam uchun. Kompilyator uchun ishlaydigan kod yozish past bar, chunki buni statik tahlil ham tekshiradi. Odam uchun yozishning mezonini *The Art of Readable Code* bitta gapda beradi va uni "o'qiluvchanlikning fundamental teoremasi" deb ataydi: kod shunday yozilishi kerakki, boshqa odam uni tushunishiga ketadigan vaqt eng kichik bo'lsin. Kitob "tushunish" so'ziga baland talab qo'yadi: o'quvchi kodni o'zgartira olishi, xatoni ko'ra olishi va uning qolgan kod bilan qanday ishlashini bilishi kerak. Arxitektor uchun savol shundan chiqadi: ertaga bu metodga kelgan, domenni bilmaydigan odam uni to'g'ri o'zgartira oladimi. Shu bobda kod yozishni muloqot kanali sifatida ko'rib chiqamiz, va shu kanalning o'tkazuvchanligini oshiradigan aniq qarorlarni sanab o'tamiz.

## 4.1 Kod yozishdan ko'ra o'qishga ko'p vaqt ketadi

To'lov servisining hayot sikliga qarang. `PaymentAuthorizationService` bir hafta yozildi, keyin uch yil davomida o'qildi: incident vaqtida, audit vaqtida, yangi to'lov provayderi qo'shilganda, PCI tekshiruvida. *Clean Code* bu nisbatni aytadi: o'qishga ketgan vaqtning yozishga ketgan vaqtga nisbati 10:1 dan ancha yuqori. Kitob shu nisbatdan to'g'ridan to'g'ri qoida chiqaradi: nisbat shunchalik katta bo'lgani uchun o'qishni osonlashtirish kerak, hatto bu yozishni qiyinlashtirsa ham. *Code Complete* xuddi shu almashuvni teskari tomondan aytadi: yozish qulayligini o'qish qulayligidan ustun qo'yish yolg'on tejamkorlik, chunki yaxshi kodni bir marta yozasiz, yomon kodni esa qayta-qayta o'qiysiz.

Shundan kelib chiqadigan amaliy qoidalar qisqa. Birinchi, qisqa nom yozish vaqtini tejaydi, lekin o'qish vaqtini oshiradi, demak yutqazadi. Ikkinchi, "aqlli" bir qatorli ifoda yozuvchiga zavq beradi, o'quvchini sekinlashtiradi: *The Art of Readable Code* buni aniq ko'rsatadi - qator soni kam bo'lishi maqsad emas, ikki qatorga yozilgan ifoda bir qatorga siqilgan ifodadan tezroq tushunilsa, ikki qator afzal. Uchinchi, kodni tushunish uchun debugger ishga tushirish kerak bo'lsa, bu kod muloqotda muvaffaqiyatsiz bo'lgan; bu uchinchi mezon shu korpusning amaliy qoidasi.

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

Yaxshi nom domen mutaxassisi aytadigan so'z bo'ladi. *Code Complete* buni "muammoga yo'naltirilganlik" deb ataydi: yaxshi nom yechimga emas, muammoga ishora qiladi, ya'ni "qanday" emas "nima" ni aytadi, va kitobdagi misol shu - `inputRec` hisoblash dunyosining so'zi, `employeeData` esa muammo sohasining so'zi. Kitob xuddi shu fikrni oxirgi qismida arxitektura darajasiga ko'taradi: yuqori darajadagi kod fayl, stek va massiv haqida emas, hal qilinayotgan muammo haqida gapirishi kerak. Ombor bo'limi "qoldiq", "rezerv", "yo'lda" deb gapiradi, shuning uchun kodda `availableQuantity`, `reservedQuantity`, `inTransitQuantity` bo'lishi kerak, `qty1` va `qty2` emas. Agar domen eksperti bilan suhbatda ishlatilgan so'z kodda yo'q bo'lsa, demak tarjima qatlami bor, va har bir tarjima xato manbasi.

Qisqartma eng qimmat tejamkorlik. `calcAmt`, `pmtSts`, `ordHdr` kabi nomlar har o'qishda ongda qayta ochiladi. *The Art of Readable Code* bu yerda ishlaydigan sinov beradi: loyihaga xos qisqartma yomon g'oya, chunki u yangi kelgan odamga shifr kabi ko'rinadi, va qisqartmani qoldirish mumkin bo'ladigan yagona holat - yangi jamoadoshi uning ma'nosini o'zi tushunsa. Shu kitob "uzun nom yozish qiyin" degan bahonani ham yopadi: har qanday zamonaviy muharrirda so'zni avtomatik tugatish bor. *Code Complete* esa qisqartmalarni jamoa darajasida boshqarishni taklif qiladi - loyihada qisqartmalarning yozib qo'yilgan ro'yxati bo'lsin, shunda har kim o'ziga yangi qisqartma o'ylab topmaydi. Shu sababli faqat domenda rasman qabul qilingan qisqartmalar qoladi: `IBAN`, `VAT`, `SKU`, `TTL`.

`Manager`, `Helper`, `Util`, `Processor`, `Data`, `Info` qo'shimchalari alohida tuzoq, va bu ro'yxat o'ylab topilgan emas: *Clean Code* sinf nomida `Manager`, `Processor`, `Data` va `Info` so'zlaridan qochishni aytadi, `Info` va `Data` ni esa "shovqin so'zlar" deb ataydi - `Product` va `ProductInfo` nomlari bir-biridan farq qiladi, lekin ma'nosi farq qilmaydi. Shu kitobning ikkinchi qoidasi bu yerda muhim: sinf nomi ot yoki ot iborasi bo'ladi, fe'l bo'lmaydi. `OrderManager` nima qiladi degan savolga javob yo'q, shuning uchun unga hamma narsa to'planadi va u cheksiz o'sadi. Nom javobgarlikni cheklamasa, sinf ham cheklanmaydi. Yechim: nomni aniq roldan chiqarish. `OrderManager` o'rniga `OrderPlacement`, `OrderCancellation`, `OrderPricing`. `PaymentHelper` o'rniga `PaymentRetryPolicy` va `CardNumberMasker`.

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

"Kognitiv yuk" atamasining o'zi Ousterhout dan keladi: u murakkablikning uch belgisidan biri bo'lib, dasturchi o'zgartirish kiritish uchun yig'ib olishi kerak bo'lgan ma'lumot hajmini bildiradi (murakkablikning to'liq yozuvi [architect 6](06-murakkablikni-boshqarish.md#61-muhim-murakkablik-va-tasodifiy-murakkablik-farqi) da). Sig'imning o'zi bo'yicha *Code Complete* Miller ning 1956 yildagi ishiga tayanadi: odam bir vaqtda taxminan yettita ma'lumot bo'lagini ushlab turadi, va kitob boshqa bobda shu chegarani "besh-to'qqizta fikriy birlik" shaklida takrorlaydi. Metodni o'qiyotgan odam ayni shu sig'imdan foydalanadi: har bir mahalliy o'zgaruvchi, har bir nomsiz shart undan bitta joy oladi.

*Code Complete* shu sig'imni bitta aniq joyda qoidaga aylantiradi: metod parametrlari soni taxminan yettitadan oshmasin, chunki odam shundan ko'pini bir vaqtda ushlab turolmaydi. Bu bobda ishlatiladigan o'lchov shu qoidaning kengaytmasi va shu korpusning amaliy tavsiyasi: metodga kirgandan keyin oxirigacha yodda tutish kerak bo'lgan narsalar sonini sanash, sanoq sig'imga yaqinlashsa metodni bo'lish. Bu "metod N qatordan oshmasin" qoidasidan aniqroq, va Ousterhout bu qoidaning o'ziga qarshi chiqadi: "N qatordan uzun har qanday metod bo'linishi kerak" degan yondashuv ko'p sonli yuzaki metod va sinf tug'diradi, ya'ni tizimning umumiy murakkabligini oshiradi. 40 qatorli to'g'ri chiziqli metod 10 qatorli ichma-ich shartlardan osonroq.

Kognitiv yukni kamaytiradigan uchta harakat kitoblarda aniq nomlangan. Birinchi, shartni nomli mantiqiy o'zgaruvchiga chiqarish: *The Art of Readable Code* buni "xulosa o'zgaruvchi" deb ataydi va beshta o'zgaruvchidan tuzilgan shartni `user_owns_document` kabi bitta nomga aylantirishni ko'rsatadi, shunda o'quvchi shart o'rniga tushunchani o'qiydi. Ikkinchi, mahalliy o'zgaruvchining qamrovini qisqartirish, ya'ni uni ishlatiladigan joyga yaqin e'lon qilish - shu kitobning alohida bo'limi. Uchinchi, metod ichida abstraksiya darajasini bir xil ushlash: Ousterhout da bu "har qatlam boshqa abstraksiya" qoidasi, ya'ni bir metodda ham SQL, ham narx hisoblash, ham audit log bo'lmasligi.

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

Ichma-ich shartlarning mexanizmini *The Art of Readable Code* aniq tasvirlaydi: har bir chuqurlik darajasi o'quvchining "fikriy stekiga" yana bitta shart qo'yadi, va yopiluvchi qavsni ko'rganda o'quvchi shu stekdan nimani olib tashlashni eslashi kerak bo'ladi. Chegara haqida *Code Complete* raqam beradi: tadqiqotlar ko'rsatishicha, kam odam uchdan ortiq ichma-ich `if` ni tushunadi, va bir qancha tadqiqotchi uch yoki to'rt darajadan oshmaslikni tavsiya qiladi. Shuning uchun uchinchi daraja paydo bo'lganda ichkarini alohida metodga chiqarish kerak.

Erta qaytish shu muammoni eng arzon yechadi, va uslubning nomi ham, foydasining tushuntirishi ham kitobdan: *The Art of Readable Code* da u "guard clause" deb ataladi va nega ishlashi aytiladi - har bir `if` bloki `return` bilan tugaganda o'quvchi fikriy stekdan hech narsani olib tashlashi kerak bo'lmaydi. Metod boshida barcha yaroqsiz holatlarni tekshirib qaytarilsa, qolgan tana faqat "to'g'ri yo'l" bo'lib qoladi. *Code Complete* ning chuqur ichma-ichlikni yumshatish bo'limi xuddi shu yo'nalishni beradi: shartlarni qayta tekshirish yoki ichki kodni alohida metodga ajratish.

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

Kod nima qilishini o'zi aytadi, shuning uchun uni takrorlagan izoh shovqin: Ousterhout da bu alohida qizil bayroq ("izoh kodni takrorlaydi"), *The Art of Readable Code* da esa qoida shunday yozilgan - kodning o'zidan tez chiqadigan faktga izoh yozilmaydi. Shu kitob yana bir narsani aytadi: izoh yomon nomning o'rnini bosmaydi, nomni tuzatish kerak. Bundan tashqari takrorlovchi izoh kod o'zgarganda yangilanmaydi va yolg'onga aylanadi. Qoida oddiy: izoh kodda ko'rinmaydigan ma'lumot bersa qoladi, aks holda o'chiriladi.

Sarlavhadagi "nima emas, nega" formulasini Ousterhout aniqlashtiradi, va bu aniqlik muhim: metod ichidagi izohning vazifasi kod NIMA qilayotganini kodning o'zidan yuqori abstraksiya darajasida aytish va kerak bo'lsa NEGA shundayligini qo'shish, aytilmasligi kerak bo'lgan narsa esa QANDAY, chunki buni kodning o'zi aytadi.

Kodda ko'rinmaydigan ma'lumot turlari kitoblarda sanab o'tilgan. *The Art of Readable Code* ularni "fikrni qayd qilish" bo'limida beradi: nega shu yechim tanlangani va o'lchov natijasi, kodning ma'lum kamchiligi hamda uni `TODO`, `FIXME`, `HACK` belgilari bilan qayd qilish, va konstanta qiymatining tarixi. Ousterhout yana bir turni qo'shadi: modullar o'rtasida tarqalgan dizayn qarori, chunki u bitta faylga tegishli bo'lmagani uchun hech qayerda yozilmay qoladi. Bizning kontekstda ro'yxat shunday turadi: tanlov asosi va rad etilgan muqobil, tashqi dunyoning cheklovi, huquqiy yoki matematik formulaning rasmiy manbasi, va vaqtinchalik yechim bilan uni olib tashlash sharti.

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

Istisno xabari eng ko'p o'qiladigan matn, chunki uni production incidentida yarim tunda o'qiydilar. `RuntimeException("error")` kabi xabar muloqotni butunlay to'xtatadi. *Clean Code* talabni aniq qo'yadi: har bir tashlangan istisno xatoning manbasi va joyini aniqlash uchun yetarli kontekst bersin, chunki stack trace muvaffaqiyatsiz bo'lgan amalning niyatini aytmaydi, shu sababli xabarda qaysi amal bajarilmagani va qanday nosozlik bo'lgani yozilishi kerak. Amalda bu uchta savolga javob berish bilan bir xil: nima bo'lmadi, qaysi obyekt bilan, va kutilgan holat qanday edi.

Arxitektura darajasida muhim qaror: domen xatolarini texnik xatolardan ajratish. *Clean Code* bu tasnifning mezonini beradi - istisno sinflarini manbasi yoki texnik turi bo'yicha emas, chaqiruvchining ehtiyoji bo'yicha, ya'ni ular QANDAY tutilishiga qarab ajratish kerak. "Omborda qoldiq yetmaydi" biznes holati, u kutilgan va uni foydalanuvchiga ko'rsatish kerak. "Ulanish uzildi" texnik holat, u retry va alert talab qiladi. Ikkisi boshqacha tutiladi, demak ikkisi boshqa tipda bo'lishi kerak; bir xil tipda bo'lsa, chaqiruvchi ularni ajrata olmaydi va `catch (Exception e)` yozadi.

Xato kodlari API chegarasida alohida qiymat beradi: kod mashina uchun, xabar odam uchun, va kodi bor xato mijoz tomonida ishlov berishni barqaror qiladi, chunki xabar matnini o'zgartirish mijozni buzmaydi. Bu uchinchi qoida shu korpusning amaliy tavsiyasi, yuqoridagi kitoblardan olingan emas.

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

Value object primitiv obsessiyasini davolaydi, va atama o'ylab topilgan emas: Fowler *Refactoring* da "primitive obsession" ni alohida kod hidi sifatida yozadi va aynan shu misollarni keltiradi - sonni valyuta bilan birlashtirgan pul sinfi, telefon raqami va pochta indeksi kabi maxsus satrlar. `String warehouseCode` va `String sku` o'rin almashsa kompilyator jim turadi, `WarehouseCode` va `Sku` bo'lsa esa kompilyatsiya buziladi. Bu xatoni runtime dan compile time ga ko'chiradi, ya'ni eng arzon joyga.

`Optional` qaytuvchi qiymat uchun, maydon yoki parametr uchun emas. Repository metodida `Optional<Order>` chaqiruvchiga "yo'q bo'lishi normal" degan xabarni beradi. `null` qaytarish esa hech narsa demaydi, shuning uchun chaqiruvchi tekshirishni esdan chiqaradi; *Clean Code* da bu alohida qoida sifatida turadi - `null` qaytarmaslik kerak.

`record`, `sealed interface` va `Optional` ning Java mexanikasi [architect 13](13-zamonaviy-java-tili-va-api-dizayni.md#131-record-qachon-ishlatish-qachon-oddiy-sinf-kerak) da to'liq yozilgan; bu bo'lim faqat ularning muloqot kanali sifatidagi rolini oladi.

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

Bu tanlovni *Clean Architecture* ning oxirgi bobi (Simon Brown yozgan "The Missing Chapter") to'rtta nomlangan variant sifatida qo'yadi: qatlam bo'yicha, xususiyat bo'yicha, port va adapter, komponent bo'yicha. Qatlam bo'yicha bo'lish, ya'ni `controller`, `service`, `repository`, `dto`, birinchi qarashda tartibli ko'rinadi. Amalda u eng muhim ma'lumotni yashiradi: tizim nima qiladi. `service` paketini ochgan odam 40 ta sinf ko'radi va ularning qaysi biri birga ishlashini bilmaydi. Bundan tashqari bitta funksiyani o'zgartirish 4 ta paketni ochishni talab qiladi.

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

Bu qarorni gap bilan emas, test bilan ushlab turish kerak. ArchUnit qoidasi `payment` paketidan `order` ning ichki sinflariga ulanishni taqiqlaydi, va shu bilan chegara hujjatdan kodga ko'chadi. Batafsil qoidalarni [testing 14.2](../testing/14-arxitektura-testlari-va-kod-sifati.md#142-archunit-asoslari) bo'limida ko'rish mumkin.

## 4.9 Kodda yashirin bilim

Eng qimmat xatolar kodda yozilmagan bilim atrofida tug'iladi. Ousterhout bu holatni "obscurity" deb ataydi va uni murakkablikning ikki sababidan biri qilib qo'yadi: muhim ma'lumot ko'rinmay qolganda kod o'zini oson ko'rsatadi, lekin aslida oson emas (murakkablikning to'liq yozuvi [architect 6](06-murakkablikni-boshqarish.md#61-muhim-murakkablik-va-tasodifiy-murakkablik-farqi) da). Magic number buning eng ko'rinadigan shakli, katalog yozuvi [patterns 25.8](../patterns/25-anti-patternlar.md#258-sehrli-sonlar-va-satrlar-magic-numbers--strings) da. `if (daysLate > 15)` ni o'qigan odam 15 ning qaydan kelganini bilmaydi, shuning uchun uni o'zgartirishga qo'rqadi yoki noto'g'ri o'zgartiradi. Nomli konstanta bu bilimni kodga qaytaradi: `MAX_GRACE_PERIOD_DAYS`. *The Art of Readable Code* bu yerda ikkinchi qadamni ham talab qiladi: konstantaning qiymati ortida deyarli doim "hikoya" turadi, va shu hikoya izohda qolishi kerak, aks holda keyingi odam qiymatni qanday o'zgartirishni bilmaydi.

Ikkinchi shakl yashirin tartib, va uning rasmiy nomi bor: *Fundamentals of Software Architecture* Page-Jones ning taksonomiyasidan "bajarilish tartibi bo'yicha connascence" (connascence of execution) ni keltiradi - bir necha komponentning bajarilish tartibi muhim bo'lsa, ular shu tartib bilan bog'langan bo'ladi, va kitobdagi misol aynan shunday: `send()` dan keyin `setSubject()` chaqirilgan kod ishlamaydi. Agar `validate()` ni `calculate()` dan oldin chaqirish kerak bo'lsa, lekin buni faqat muallif bilsa, bu bilim yo'qoladi. To'g'ri yechim tartibni imkonsiz qilish, masalan `calculate()` ni faqat `ValidatedOrder` tipidan qabul qiladigan qilish. Uchinchi shakl kutilmagan yon ta'sir: *Clean Code* ning "yon ta'siri bo'lmasin" qoidasi shu haqda - nomi bir narsani aytib, yana boshqasini qiladigan metod chaqiruvchini chalg'itadi, shuning uchun nomi `get` bilan boshlanadigan metod cache ni yangilamasligi va audit log yozmasligi kerak.

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

Public API uchun to'rtta kanal bor, va ularni birga ishlatish kerak. Birinchi kanal nom: *Code Complete* ning "o'zini hujjatlaydigan kod" bobi hujjatlashning birinchi joyi kodning o'zi ekanini aytadi, va shu kitobning izoh bo'limi foydali mezon beradi - izohni yozishdan oldin "shu kodni bajaradigan metodni qanday nomlagan bo'lardim" deb so'rash kerak, javob ko'pincha niyat darajasidagi izohning o'zi bo'lib chiqadi. Ikkinchi kanal imzo: parametr turlari noto'g'ri chaqiruvni imkonsiz qiladi. Uchinchi kanal interfeys hujjati, Java da Javadoc: Ousterhout unda nima bo'lishini sanab beradi - chaqiruvchi ko'zi bilan ko'rilgan xatti-harakat, har bir argument va qaytuvchi qiymat chegaralari bilan, yon ta'sirlar, tashlanadigan istisnolar va bajarilishi kerak bo'lgan oldingi shartlar; shu bilan birga interfeys hujjatiga ichki tafsilot tushsa, bu alohida qizil bayroq. To'rtinchi kanal test nomlari: *The Art of Readable Code* da test nomi uchta narsani aytishi kerak - qaysi sinf, qaysi metod va qanday holat tekshirilayotgani.

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

Test nomlari shu hujjatning davomi. `testCreate1` nomi hech kimga yordam bermaydi, `issueInvoice_returnsExistingInvoice_whenCalledTwiceForSameOrder` esa shartnomani takrorlaydi va buzilganda aynan qaysi kelishuv buzilganini aytadi. Arxitektor uchun amaliy o'lchov shu (shu korpusning tavsiyasi): public metod uchun yozilgan test nomlarini ketma-ket o'qib chiqqanda, u metodning shartnomasi tiklanishi kerak.

## 4.11 Amalda qo'llash

- [ ] Eng ko'p o'zgaradigan 5 ta sinfni tanlab, nomlaridan `Manager`, `Helper`, `Util`, `Processor` qo'shimchalarini olib tashlang va javobgarlik bo'yicha bo'ling.
- [ ] Domen eksperti ishlatadigan 15 ta atamani ro'yxat qilib, kodda ularning qanday yozilganini tekshiring; farq bo'lsa kodni domenga moslang.
- [ ] Eng murakkab 3 ta metodda ichma-ich shartlarni erta qaytishga aylantirib, chuqurlikni ikki darajadan oshmasligiga keltiring.
- [ ] Pul, SKU, ombor kodi va buyurtma identifikatori uchun value object joriy qiling, `String` va `BigDecimal` ni public imzolardan chiqaring.
- [ ] Barcha `throw new RuntimeException(...)` chaqiruvlarini topib, ularni kontekst va xato kodi bor domen yoki infratuzilma istisnolariga ajratib bering.
- [ ] Bitta xususiyatni (masalan to'lov) qatlam paketlaridan `payment` paketiga ko'chirib, ichki sinflarni `package-private` qiling va chegarani ArchUnit qoidasi bilan mahkamlang.
- [ ] Kodni magic number uchun skanerlang (timeout, retry soni, limit, kun soni) va har birini nomli konstanta va asosni aytuvchi izoh bilan almashtiring.
- [ ] Public API ning 10 ta metodida Javadoc ni "nima" dan "shartnoma" ga qayta yozing: idempotentlik, tranzaksiya talabi, tashlanadigan istisnolar.

## Manbalar

- Dustin Boswell, Trevor Foucher, *The Art of Readable Code*, 1-nashr, O'Reilly, 2011, 1-bob (2-4-betlar) - "kod tushunishga oson bo'lishi kerak" va o'qiluvchanlikning fundamental teoremasi; qator sonini kamaytirish maqsad emasligi
- Dustin Boswell, Trevor Foucher, *The Art of Readable Code*, 1-nashr, O'Reilly, 2011 (copyright 2012), 2-bob (18-19-betlar) - loyihaga xos qisqartma va "yangi jamoadoshi tushunadimi" sinovi, uzun nomni muharrir o'zi tugatishi
- Dustin Boswell, Trevor Foucher, *The Art of Readable Code*, 1-nashr, O'Reilly, 2011 (copyright 2012), 5-bob (47-51-betlar) - kodning o'zidan chiqadigan faktga izoh yozmaslik, yomon nomni izoh bilan yopmaslik, fikrni qayd qilish (o'lchov natijasi, TODO/FIXME/HACK, konstanta tarixi)
- Dustin Boswell, Trevor Foucher, *The Art of Readable Code*, 1-nashr, O'Reilly, 2011 (copyright 2012), 7-bob (75-78-betlar) - erta qaytish va guard clause, ichma-ichlikning "fikriy stek" mexanizmi
- Dustin Boswell, Trevor Foucher, *The Art of Readable Code*, 1-nashr, O'Reilly, 2011 (copyright 2012), 8-bob (84-bet) va 9-bob (97-bet) - xulosa o'zgaruvchi, o'zgaruvchi qamrovini qisqartirish
- Dustin Boswell, Trevor Foucher, *The Art of Readable Code*, 1-nashr, O'Reilly, 2011 (copyright 2012), 14-bob (157-158-betlar) - test nomi sinf, metod va tekshirilayotgan holatni aytishi
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 11.1 (259-261-betlar) - nom obyektni to'liq va aniq tasvirlashi, "muammoga yo'naltirilganlik"; 11.6 (282-285-betlar) - qisqartmalar ro'yxati va yozish/o'qish qulayligi almashuvi
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 7-bob (178-bet) va 19.6 (457-bet) - Miller 1956 ga tayangan sig'im: taxminan yettita ma'lumot bo'lagi, "besh-to'qqizta fikriy birlik", metod parametrlari chegarasi
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 19.4 (445-bet) - uchdan ortiq ichma-ich `if` ni kam odam tushunadi, uch yoki to'rt daraja chegarasi va uni yumshatish yo'llari
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 32.5 (795-797-betlar) - niyat darajasidagi izoh va "metodni qanday nomlagan bo'lardim" mezoni; 34.3 (841-842-betlar) - o'qish qulayligidan yozish qulayligini ustun qo'yish yolg'on tejamkorlik; 34.6 (845-846-betlar) - muammo sohasi atamalarida dasturlash
- Robert C. Martin, *Clean Code*, 1-bob (14-bet) - o'qish va yozish vaqti nisbati 10:1 dan yuqori, shundan "o'qishni osonlashtir" qoidasi
- Robert C. Martin, *Clean Code*, 2-bob (21 va 25-betlar) - shovqin so'zlar (`Info`, `Data`), sinf nomida `Manager`, `Processor`, `Data`, `Info` dan qochish, sinf nomi fe'l bo'lmasligi
- Robert C. Martin, *Clean Code*, 3-bob - yon ta'siri bo'lmasin; 7-bob (107-109-betlar) - istisnoga kontekst berish va istisno sinflarini chaqiruvchining ehtiyoji (qanday tutilishi) bo'yicha ajratish, `null` qaytarmaslik
- Robert C. Martin, *Clean Architecture*, 34-bob - paketni qatlam, xususiyat, port va adapter yoki komponent bo'yicha bo'lish
- John Ousterhout, *A Philosophy of Software Design*, 1-nashr (v1.0), Yaknyam Press, 2018, 2.2-2.3 - kognitiv yuk va obscurity; 4.6 - "N qatordan uzun metod bo'linsin" qoidasi tanqidi (classitis); 7-bob - har qatlam boshqa abstraksiya
- John Ousterhout, *A Philosophy of Software Design*, 1-nashr, Yaknyam Press, 2018, 13.2, 13.5-13.7 - izoh kodni takrorlamasligi, interfeys hujjati tarkibi (argument, yon ta'sir, istisno, oldingi shart), interfeys hujjatiga ichki tafsilot tushishi qizil bayroq, modullar orasidagi dizayn qarori
- Martin Fowler, *Refactoring*, Addison-Wesley, 1999, 3-bob - "primitive obsession" kod hidi, pul sinfi va maxsus satrlar misoli
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, O'Reilly, 2020, 3-bob - Page-Jones ning connascence taksonomiyasi, bajarilish tartibi bo'yicha connascence
- Herbert Schildt, *Java The Complete Reference*, 9-bob - paket va interfeys, ko'rinish qoidalari
- ESLATMA: 4.1 dagi debugger mezoni, 4.3 dagi "yodda tutish kerak bo'lgan narsalarni sanash" o'lchovi, 4.6 dagi xato kodi qoidasi, 4.10 dagi test nomlarini ketma-ket o'qish mezoni va 4.11 dagi checklist shu korpusning amaliy tavsiyasi, kitobdan olingan emas

---

[&larr; 3. Qaror qabul qilish va uni hujjatlashtirish](03-qaror-qabul-qilish-va-uni-hujjatlashtirish.md) · [Mundarija](README.md) · [5. Abstraksiya hissi, bog'liqlik va chegaralar &rarr;](05-abstraksiya-hissi-bogliqlik-va-chegaralar.md)
