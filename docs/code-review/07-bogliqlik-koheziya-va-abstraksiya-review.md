<!-- doc: code-review | chapter: 7 | part: II. Arxitektura, dizayn va clean code review -->

[Barcha hujjatlar](../../README.md) / [Kod review](README.md)

# 7. Bog'liqlik, koheziya va abstraksiya review (Coupling, Cohesion, Abstraction)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

- [7.1 Bog'liqlik turlarini diffda aniqlash](#71-bogliqlik-turlarini-diffda-aniqlash)
- [7.2 Vaqt bog'liqligi: eng jim xato manbasi](#72-vaqt-bogliqligi-eng-jim-xato-manbasi)
- [7.3 Koheziya: nima birga o'zgarsa, birga tursin](#73-koheziya-nima-birga-ozgarsa-birga-tursin)
- [7.4 Soxta abstraksiya: bitta implementatsiyali interfeys](#74-soxta-abstraksiya-bitta-implementatsiyali-interfeys)
- [7.5 DRY ning noto'g'ri qo'llanishi](#75-dry-ning-notogri-qollanishi)
- [7.6 Oqib chiqadigan abstraksiya (leaky abstraction)](#76-oqib-chiqadigan-abstraksiya-leaky-abstraction)
- [7.7 Feature envy va shotgun surgery](#77-feature-envy-va-shotgun-surgery)
- [7.8 Abstraksiya darajalarining aralashuvi](#78-abstraksiya-darajalarining-aralashuvi)
- [7.9 Konstruktor parametrlari soni - eng oson o'lchov](#79-konstruktor-parametrlari-soni---eng-oson-olchov)
- [7.10 Abstraksiyani olib tashlash ham yaxshilanish](#710-abstraksiyani-olib-tashlash-ham-yaxshilanish)
- [7.11 Amalda qo'llash](#711-amalda-qollash)

</details>


Arxitektura buzilishi odatda bitta klassning ichida boshlanadi: klass o'ziga tegishli bo'lmagan narsani bilib qoladi, yoki bir-biriga aloqasi yo'q ikki narsa bir joyga tushadi. Bu bob shu ikki kuchni - bog'liqlik va koheziyani - diffdan o'qishni beradi. Nazariy ta'rif [Arxitektor miyasi](../architect/README.md) da, bu yerda faqat ko'rinadigan belgilar va review javoblari.

## 7.1 Bog'liqlik turlarini diffda aniqlash

Bog'liqlik bir xil emas. Uning har bir turi boshqa belgi qoldiradi va boshqa narx keltiradi.

| Tur | Diffdagi belgisi | Narxi | Review javobi |
| --- | --- | --- | --- |
| Ma'lumot (parametr orqali) | Oddiy parametr | Eng arzon, normal | Qabul qilinadi |
| Shakl (DTO strukturasi) | Boshqa modulning DTO si import qilingan | O'rtacha | O'z turiga aylantirish |
| Boshqaruv (boolean flag) | `doWork(true, false)` | Yuqori | Ikki alohida metod |
| Vaqt (chaqiruv tartibi) | `init()` keyin `run()` majburiy | Yuqori | Konstruktor yoki bitta metod |
| Joylashuv (URL, yo'l) | Qattiq yozilgan manzil | O'rtacha | Konfiguratsiya |
| Sxema (umumiy jadval) | Boshqa modul jadvaliga `JOIN` | Juda yuqori | API yoki o'qish modeli |
| Umumiy mutable holat | `static` to'plam, singleton kesh | Juda yuqori | Holatni egasiga berish |
| Implementatsiya (ichki detal) | Boshqa modulning `internal` klassi | Juda yuqori | Chegara orqali o'tish |

## 7.2 Vaqt bog'liqligi: eng jim xato manbasi

Vaqt bog'liqligi - obyektdan foydalanish uchun metodlarni ma'lum tartibda chaqirish kerak bo'lgan holat. Kompilyator buni tekshirmaydi, test odatda to'g'ri tartibda yozilgan bo'ladi, va xato faqat yangi chaqiruv joyi paydo bo'lganda chiqadi.

```java
// Vaqt bog'liqligi: ikki qadam majburiy, lekin hech narsa buni majburlamaydi.
public class ReportBuilder {
    private List<Row> rows;

    public void load(LocalDate from, LocalDate to) {   // birinchi chaqirilishi shart
        this.rows = repository.rows(from, to);
    }

    public byte[] render() {                           // ikkinchi
        return pdf.render(rows);                       // load chaqirilmasa - NPE
    }
}
// Review izohi: render() ni load() dan oldin chaqirish kompilyatsiyada
// tutilmaydi. Yangi chaqiruvchi shu tartibni bilmasligi mumkin.
// Yechim: holatni konstruktorga olib kirish yoki bitta metod qilish.

// To'g'ri: obyekt yaratilgan paytdan to'liq ishga tayyor (immutable).
public record ReportRequest(LocalDate from, LocalDate to) { }

public class ReportService {
    public byte[] render(ReportRequest request) {      // bitta kirish nuqtasi
        List<Row> rows = repository.rows(request.from(), request.to());
        return pdf.render(rows);
    }
}
```

Spring kodida bu naqsh ko'p uchraydi: `@PostConstruct` da bir narsa to'ldiriladi, keyin metodlar unga tayanadi. Review savoli - bean to'liq qurilgandan keyin ishlatilishi kafolatlanganmi, va `@PostConstruct` ichida tashqi chaqiruv bo'lsa, ishga tushish buzilmaydimi.

## 7.3 Koheziya: nima birga o'zgarsa, birga tursin

Past koheziya belgisi - bitta klassda bir-biriga aloqasi yo'q bo'lgan metodlar to'plami. Uning eng aniq ko'rsatkichi: klass maydonlarining qanchasi har bir metodda ishlatiladi. Agar klassda 8 maydon bo'lsa va har metod ulardan ikkitasini ishlatsa, bu aslida to'rt xil klass.

```java
// Past koheziya: "OrderService" ichida to'rt xil mas'uliyat.
@Service
public class OrderService {
    private final OrderRepository orders;      // 1-guruh
    private final PaymentClient payments;      // 2-guruh
    private final PdfRenderer pdf;             // 3-guruh
    private final SmsSender sms;               // 4-guruh
    private final ExcelExporter excel;         // 3-guruh
    private final FraudScoreClient fraud;      // 2-guruh

    public Order place(PlaceOrder cmd) { /* orders, payments, fraud */ }
    public byte[] invoicePdf(long id) { /* orders, pdf */ }
    public byte[] monthlyExcel(int m) { /* orders, excel */ }
    public void remind(long id) { /* orders, sms */ }
}
// Review izohi: konstruktorda 6 bog'liqlik, lekin hech bir metod uchtadan
// ko'pini ishlatmaydi. Bu klass to'rt sababga ko'ra o'zgaradi: buyurtma
// qoidasi, hujjat shakli, hisobot formati, xabar matni.
// Natijasi: PDF shablonini o'zgartirish uchun to'lov mantiqi bor faylga
// tegiladi, va shu fayl har sprintda konflikt beradi.
// Yechim: OrderPlacement, OrderDocuments, OrderReports, OrderReminders.
```

```bash
# Koheziyani o'lchash: tarixda birga o'zgargan fayllar (change coupling).
# Agar ikki fayl har doim birga o'zgarsa, ular bitta modul bo'lishi kerak.
# Agar bitta fayl turli sabablar bilan o'zgarsa, u bo'linishi kerak.
git log --format='%H' --since='12 months ago' \
  | while read -r c; do git show --name-only --format= "$c"; echo "---"; done \
  | awk '/^---$/{for(i in f) for(j in f) if(i<j) print i" + "j; delete f; next}
         /\.java$/{f[$0]=1}' \
  | sort | uniq -c | sort -rn | head -20

# Bitta faylning o'zgarish sabablarini ko'rish: commit sarlavhalari.
git log --oneline --since='6 months ago' -- src/main/java/.../OrderService.java | head -30
```

Ikkinchi buyruq review da juda foydali: agar bitta faylning oxirgi 30 commit sarlavhasi to'rt xil mavzuda bo'lsa (to'lov, PDF, hisobot, SMS), klassni bo'lish kerakligi dalil bilan ko'rsatiladi.

## 7.4 Soxta abstraksiya: bitta implementatsiyali interfeys

Loyihalarda eng ko'p uchraydigan ortiqcha abstraksiya - har bir servis uchun interfeys yozish odati. `OrderService` va `OrderServiceImpl` juftligi hech qanday moslashuvchanlik bermaydi: almashtirish nuqtasi yo'q, test uchun ham kerak emas (Mockito klasslarni ham mock qiladi).

```java
// Soxta abstraksiya: faqat nom takrorlanishi, foyda nol.
public interface OrderService {                 // bitta implementatsiya
    Order place(PlaceOrder cmd);
}
@Service
public class OrderServiceImpl implements OrderService { /* ... */ }

// Review savoli: ikkinchi implementatsiya qachon paydo bo'ladi?
// Javob "hech qachon" bo'lsa - interfeys olib tashlanadi.

// Haqiqiy abstraksiya: almashtirish nuqtasi real.
public interface PaymentGateway {               // Stripe, Payme, test uchun soxta
    AuthResult authorize(Money amount, Card card);
}
// Bu yerda interfeys kerak, chunki:
// 1) ikki provayder ham prodda ishlaydi (marshrutlash bor);
// 2) testda tarmoqqa chiqmaydigan implementatsiya kerak;
// 3) domen vendor turlarini bilmasligi kerak.
```

Mezon uchta savolda: hozir ikkinchi implementatsiya bormi, testda almashtirish zarurmi (integratsion test bilan yopib bo'lmaydimi), va bu chegarada bog'liqlik yo'nalishini teskari qilish kerakmi. Uchiga ham "yo'q" bo'lsa, interfeys ortiqcha.

## 7.5 DRY ning noto'g'ri qo'llanishi

Takrorlanishni olib tashlash har doim yaxshi emas. Ikki kod bloki bir xil ko'rinishi mumkin, lekin turli sabablarga ko'ra o'zgaradi. Ularni birlashtirish - ikki mustaqil narsani bir-biriga qulflash.

```java
// Tasodifiy o'xshashlik: ikki validatsiya bir xil ko'rinadi.
void validateCustomerPhone(String phone) {
    if (phone == null || !phone.matches("\\+998\\d{9}")) throw new Invalid();
}
void validateCourierPhone(String phone) {
    if (phone == null || !phone.matches("\\+998\\d{9}")) throw new Invalid();
}

// Noto'g'ri "yaxshilash": birlashtirish.
void validatePhone(String phone) { ... }        // ikkisi ham shuni chaqiradi

// Nega noto'g'ri: kuryer telefoni kelasi oyda xalqaro raqam bo'lishi mumkin
// (chet el kuryerlari), mijoz telefoni esa faqat mahalliy qoladi. Shunda
// umumiy metodga flag qo'shiladi - va boshqaruv bog'liqligi paydo bo'ladi.

// To'g'ri yondashuv: tur bilan ajratish, umumiy qism primitiv darajada qoladi.
public record PhoneNumber(String value) {
    public PhoneNumber {
        if (value == null || !value.matches("\\+\\d{7,15}")) throw new Invalid();
    }
}
public record UzPhoneNumber(String value) { /* +998 qoidasi */ }
```

Review mezoni: takrorlangan kod bir xil sababga ko'ra o'zgaradimi. Javob "ha" bo'lsa - birlashtirish. "Yo'q" yoki "bilmayman" bo'lsa - takrorlanish arzonroq. Uchinchi marta takrorlanganda qaytib ko'rish qoidasi amalda yaxshi ishlaydi.

## 7.6 Oqib chiqadigan abstraksiya (leaky abstraction)

Abstraksiya ichidagi detal tashqariga chiqib qolsa, u foyda bermaydi, lekin narx keltiradi: foydalanuvchi ikki narsani - abstraksiyani va uning ichini - bilishi kerak bo'ladi.

| Oqish belgisi | Misol | Oqibati |
| --- | --- | --- |
| Istisno turi implementatsiyadan | `PaymentGateway` `HttpClientErrorException` tashlaydi | Chaqiruvchi HTTP ni biladi |
| Qaytish turida vendor klassi | `StripeCharge` qaytariladi | Vendor almashtirilmaydi |
| Konfiguratsiya nomlari oqib chiqqan | `setStripeApiVersion` port interfeysida | Abstraksiya soxta |
| Tartiblash/pagination detali | `Pageable` domen portida | Spring domenga kirgan |
| `null` ning maxsus ma'nosi | "null = topilmadi, bo'sh = xato" | Hujjatsiz shartnoma |
| Ketma-ketlikka bog'liqlik | "avval `prepare` chaqiring" | Vaqt bog'liqligi |

```java
// Oqadigan port: domen HTTP va Stripe ni biladi.
public interface PaymentGateway {
    StripeChargeResponse charge(String json) throws HttpClientErrorException;
}

// Yopiq port: faqat domen tillari.
public interface PaymentGateway {
    /** Xato holatlari: DECLINED, NETWORK, INVALID_CARD. */
    AuthResult authorize(Money amount, Card card);
}
public sealed interface AuthResult {
    record Approved(String authCode) implements AuthResult { }
    record Declined(DeclineReason reason) implements AuthResult { }
    record Failed(FailureKind kind, String detail) implements AuthResult { }
}
// Review foydasi: chaqiruvchi hamma holatni hisobga olishga majbur
// (sealed + switch), va vendor istisnolari adapter ichida qoladi.
```

## 7.7 Feature envy va shotgun surgery

Feature envy - metod o'z klassining maydonlaridan ko'ra boshqa obyektning maydonlari bilan ko'proq ishlaydigan holat. Diffda belgisi: yangi metodda `other.getX()`, `other.getY()`, `other.getZ()` ketma-ketligi.

```java
// Feature envy: hisob Order ning ichki ma'lumotidan quriladi, lekin
// Order dan tashqarida bajariladi.
public class ShippingCalculator {
    public Money cost(Order order) {
        BigDecimal weight = BigDecimal.ZERO;
        for (OrderLine line : order.getLines()) {          // ichkiga kirish
            weight = weight.add(line.getProduct().getWeight()
                                    .multiply(BigDecimal.valueOf(line.getQty())));
        }
        if (order.getCustomer().getTier() == GOLD) { ... } // yana ichkiga
        return ...;
    }
}
// Review izohi: bu metod Order ning uch darajali ichki tuzilishini biladi.
// Order o'zgarsa, shu hisob ham sinadi. Og'irlik hisobini Order ga
// ko'chirish kerak: order.totalWeight(). Qoidaning o'zi (narx jadvali)
// kalkulyatorda qolishi mumkin.
```

Shotgun surgery - bitta mantiqiy o'zgarish uchun ko'p faylga tegish kerak bo'lgan holat. Diffda belgisi: 12 faylda bittadan satr o'zgargan va hammasi bir xil o'zgarish.

```bash
# Shotgun surgery belgisini o'lchash: bir xil o'zgarish necha faylda.
git diff --numstat origin/main...HEAD \
  | awk '$1<=3 && $2<=3 {n++} END {print n" ta faylda uchdan kam satr tegilgan"}'

# Agar bu son 8 dan oshsa va o'zgarishlar bir xil bo'lsa, abstraksiya yo'q:
git diff origin/main...HEAD | grep -E '^\+' | sort | uniq -c | sort -rn | head
```

Birinchi buyruq "bir xil satr ko'p joyda takrorlangan" holatini ko'rsatadi. Review javobi - bu o'zgarish bitta joyda bo'lishi uchun nima kerak degan savol.

## 7.8 Abstraksiya darajalarining aralashuvi

Bir metod ichida turli darajadagi gaplar bo'lsa, o'qish qiyinlashadi: biznes qoidasi bilan bayt bufferi yoki satr formatlash bir qatorda turadi.

```java
// Aralash darajalar: "nima" va "qanday" bir joyda.
public void publishDailyReport(LocalDate date) {
    List<Row> rows = repository.rows(date);                    // yuqori daraja
    ByteArrayOutputStream bos = new ByteArrayOutputStream();   // past daraja
    try (ZipOutputStream zip = new ZipOutputStream(bos)) {     // past daraja
        zip.putNextEntry(new ZipEntry("report.csv"));
        for (Row r : rows) {
            zip.write((r.id() + ";" + r.amount() + "\n").getBytes(UTF_8));
        }
    } catch (IOException e) { throw new UncheckedIOException(e); }
    mailer.send(recipients(), "Kunlik hisobot", bos.toByteArray());  // yuqori
}

// Bir darajada o'qiladigan shakl: har qatori bir xil balandlikda.
public void publishDailyReport(LocalDate date) {
    List<Row> rows = repository.rows(date);
    byte[] archive = csvArchive(rows);
    mailer.send(recipients(), "Kunlik hisobot", archive);
}
// Review mezoni: metodni o'qiganda "nima bo'layotgani" bir o'qishda
// tushunarli bo'lsa, daraja to'g'ri. Zip va baytlar pastki metodda.
```

## 7.9 Konstruktor parametrlari soni - eng oson o'lchov

Bog'liqlikni o'lchashning eng tez usuli - konstruktorga qarash. Besh-oltidan ko'p bog'liqlik klassning juda ko'p narsani bilishini bildiradi. Bu qoida qattiq emas, lekin savol berish uchun yetarli sabab.

```bash
# Konstruktor parametrlari ko'p bo'lgan klasslarni topish.
grep -rn --include='*.java' -A4 'public [A-Z][A-Za-z]*(' src/main/java \
  | grep -oE '\(([^)]*,){5,}[^)]*\)' | wc -l

# Diffda yangi qo'shilgan konstruktor parametrlarini ko'rish.
git diff origin/main...HEAD -- '*.java' | grep -E '^\+.*private final '
```

Diffda yangi `private final` maydon qo'shilishi - har doim savol: bu klassning mas'uliyati o'sdimi, yoki yangi mas'uliyat boshqa joyga tegishlimi.

## 7.10 Abstraksiyani olib tashlash ham yaxshilanish

Review izohlari odatda abstraksiya qo'shishni so'raydi. Teskari yo'nalish ham xuddi shunday qimmatli: ortiqcha qatlamni olib tashlash.

| Olib tashlashga arziydigan narsa | Belgisi |
| --- | --- |
| Bitta implementatsiyali interfeys | `XxxImpl` nomlash |
| Hech narsa qo'shmaydigan mapper | DTO va entity maydonlari bir xil, mapping 1:1 |
| O'tkazib yuboruvchi servis | Metod faqat repository ga delegatsiya qiladi |
| Hech kim tashlamaydigan custom istisno | Faqat e'lon qilingan |
| Ishlatilmaydigan konfiguratsiya flag i | Har doim bir qiymatda |
| Generics ortiqcha | `<T extends Object>` real polimorfizm yo'q |
| Abstract base class | Bitta vorisi bor |

```bash
# Bitta implementatsiyali interfeyslarni topish.
for i in $(grep -rl --include='*.java' 'public interface' src/main/java); do
  name=$(basename "$i" .java)
  impl=$(grep -rl --include='*.java' "implements .*$name" src/main/java | wc -l)
  [ "$impl" = "1" ] && echo "$name: 1 implementatsiya"
done | head -20

# Faqat delegatsiya qiladigan metodlarni topish (bir satrli servis metodlari).
grep -rn --include='*.java' -A2 'public .* [a-z].*(' src/main/java/**/service \
  | grep -B1 'return [a-z]*\.[a-z]*(' | head -20
```

## 7.11 Amalda qo'llash

- [ ] Bog'liqlik turlari jadvalini review checklistiga qo'shib, har PR da "qaysi tur qo'shildi" savolini bering.
- [ ] Vaqt bog'liqligi bor klasslarni toping (`init`/`load` keyin ishlatiladigan) va ularni immutable konstruktorga o'tkazish tiketini ochingg.
- [ ] Change coupling skriptini ishga tushirib, har doim birga o'zgaradigan 10 juft faylni aniqlang va ularni bitta moduldami yoki yo'qligini tekshiring.
- [ ] Oxirgi 6 oyda bitta faylga kelgan commit sarlavhalarini mavzu bo'yicha guruhlab, to'rtdan ko'p mavzuli klasslarni bo'lishni rejalashtiring.
- [ ] Bitta implementatsiyali interfeyslar ro'yxatini chiqarib, real almashtirish nuqtasi yo'qlarini olib tashlang.
- [ ] Portlardan oqib chiqadigan detallarni toping: `HttpClientErrorException`, `Pageable`, vendor turlari domen interfeyslarida.
- [ ] Konstruktorida 6 dan ko'p bog'liqlik bo'lgan klasslarni sanab, ularning har bir metodi nechta maydonni ishlatishini tekshiring.
- [ ] Faqat delegatsiya qiladigan servis qatlamlari va 1:1 mapperlarni toping va olib tashlash taklifini kiritiladigan PR ga qo'shing.

---

[&larr; 6. Arxitektura review: qatlam, chegara, bog'liqlik yo'nalishi](06-arxitektura-review-qatlam-chegara-bogliqlik.md) · [Mundarija](README.md) · [8. Clean code review: nomlash, kognitiv yuk, metod shakli &rarr;](08-clean-code-review-nomlash-kognitiv-yuk.md)
