<!-- doc: sonarqube | chapter: 27 | part: VII. Xato katalogi: qanday kod qanday xato hisoblanadi -->

[Barcha hujjatlar](../../README.md) / [SonarQube](README.md)

# 27. Xato katalogi: maintainability, tuzilish va murakkablik (Catalog: Maintainability, Structure)

<details>
<summary>Bu bobdagi 17 bo'lim</summary>

- [27.1 Cognitive complexity chegarasidan oshgan metod](#271-cognitive-complexity-chegarasidan-oshgan-metod)
- [27.2 Juda uzun metod va juda uzun klass](#272-juda-uzun-metod-va-juda-uzun-klass)
- [27.3 Parametrlar soni ko'p metod](#273-parametrlar-soni-kop-metod)
- [27.4 Ichma-ich joylashgan shartlar va chuqur bloklar](#274-ichma-ich-joylashgan-shartlar-va-chuqur-bloklar)
- [27.5 Birlashtirish mumkin bo'lgan ketma-ket `if` lar](#275-birlashtirish-mumkin-bolgan-ketma-ket-if-lar)
- [27.6 Bo'sh blok va bo'sh `catch`](#276-bosh-blok-va-bosh-catch)
- [27.7 Takrorlangan kod bloki](#277-takrorlangan-kod-bloki)
- [27.8 Takrorlangan satr literali](#278-takrorlangan-satr-literali)
- [27.9 Magic number va uni konstantaga chiqarish](#279-magic-number-va-uni-konstantaga-chiqarish)
- [27.10 Ortiqcha mahalliy o'zgaruvchi va darhol qaytariladigan qiymat](#2710-ortiqcha-mahalliy-ozgaruvchi-va-darhol-qaytariladigan-qiymat)
- [27.11 Keraksiz `else` va erta qaytish bilan soddalashtirish](#2711-keraksiz-else-va-erta-qaytish-bilan-soddalashtirish)
- [27.12 Ternar operatorlarni ichma-ich joylash](#2712-ternar-operatorlarni-ichma-ich-joylash)
- [27.13 `switch` da `default` yo'qligi va qamrab olinmagan holat](#2713-switch-da-default-yoqligi-va-qamrab-olinmagan-holat)
- [27.14 Umumiy `Exception` ni ushlash yoki tashlash](#2714-umumiy-exception-ni-ushlash-yoki-tashlash)
- [27.15 Oddiy yondashuv va arxitektor yondashuvi](#2715-oddiy-yondashuv-va-arxitektor-yondashuvi)
- [27.16 Tuzoq va yechim](#2716-tuzoq-va-yechim)
- [27.17 Amalda qo'llash](#2717-amalda-qollash)

</details>



Bu bob maintainability toifasidagi eng ko'p uchraydigan code smell larni katalog ko'rinishida yig'adi. Har bir holat uchun avval Sonar shikoyat qiladigan kod, keyin shikoyat sababi, keyin tuzatilgan variant beriladi. Misollar to'lov, buyurtma va hisobot servislari ustida qurilgan. Jiddiylik ustuni "taxminan", chunki uni quality profile belgilaydi.

| Kod holati | Sonar nima deydi | Toifa | Jiddiylik (taxminan) | Ta'siri |
| --- | --- | --- | --- | --- |
| Metodda cognitive complexity chegaradan oshdi (`java:S3776`) | "Refactor this method to reduce its Cognitive Complexity" | maintainability (code smell) | Critical | Metodni o'qish va test bilan qamrash qiyinlashadi |
| Metod juda uzun (`java:S138`) | "Metod ruxsat etilgan qatordan uzun" | maintainability (code smell) | Major | Bitta metod bir nechta mas'uliyatni ushlab turadi |
| Klass yoki fayl juda uzun | "Fayl ruxsat etilgan qatordan uzun" (fayl uzunligi qoidasi) | maintainability (code smell) | Major | Klass God Object ga aylanadi |
| Parametrlar soni ko'p (`java:S107`) | "Metodda 7 dan ko'p parametr bor" | maintainability (code smell) | Major | Chaqiruv joyida argument almashib ketadi |
| Nazorat strukturalari chuqur ichma-ich (`java:S134`) | "Uch darajadan chuqur joylashtirma" | maintainability (code smell) | Critical | Shart kombinatsiyalari ko'rinmay qoladi |
| Birlashtirilishi mumkin bo'lgan `if` lar (`java:S1066`) | "Merge this if statement with the enclosing one" | maintainability (code smell) | Major | Ortiqcha ichma-ich daraja, keraksiz murakkablik |
| Bo'sh blok (`java:S108`) | "Either remove or fill this block of code" | maintainability (code smell) | Major | Yozilmagan mantiq yo'q bo'lib ketadi |
| Bo'sh `catch` va yo'q qilingan exception | "Handle this exception or rethrow it" | maintainability (code smell) | Major | Xato jim yutiladi, incident tahlili imkonsiz |
| Takrorlangan kod bloki (duplication metrikasi) | "Duplicated Blocks" o'sadi, quality gate shartiga tegadi | maintainability (o'lchov) | Quality gate sharti | Tuzatish bir joyda qilinadi, boshqasida qolib ketadi |
| Takrorlangan satr literali (`java:S1192`) | "Literal takrorlanmasin, konstanta kirit" | maintainability (code smell) | Critical | Matn yoki kalit bir joyda o'zgaradi, boshqasida yo'q |
| Magic number (`java:S109`) | "Assign this magic number to a well-named constant" | maintainability (code smell) | Major | Raqamning ma'nosi faqat muallif xotirasida qoladi |
| Darhol qaytariladigan mahalliy o'zgaruvchi (`java:S1488`) | "Ifodani darhol qaytar" | maintainability (code smell) | Minor | Shovqin, o'qishga qo'shimcha qadam |
| Ishlatilmaydigan qiymat berish (`java:S1854`) | "Remove this useless assignment to local variable" | maintainability (code smell) | Major | O'quvchini chalg'itadi, bug ni yashiradi |
| Boolean ifodani `if/else` bilan qaytarish (`java:S1126`) | "Bitta return bilan almashtir" | maintainability (code smell) | Minor | Oddiy mantiq uch barobar uzun yoziladi |
| Ichma-ich ternar operator (`java:S3358`) | "Ichma-ich ternarni ajratib ol" | maintainability (code smell) | Major | Ifoda bir qarashda noto'g'ri o'qiladi |
| `switch` da `default` yo'q | "Add a default case to this switch" (default branch qoidasi) | maintainability (code smell) | Critical | Yangi enum qiymati jim o'tib ketadi |
| Umumiy `Exception` ni tashlash (`java:S112`) | "Maxsus exception tashla" | maintainability (code smell) | Major | Chaqiruvchi xato turini ajrata olmaydi |

## 27.1 Cognitive complexity chegarasidan oshgan metod

Sonar cyclomatic complexity dan tashqari cognitive complexity ni ham hisoblaydi. Har bir shart, tsikl va `catch` ball qo'shadi, ichma-ich joylashuv esa ballni ko'paytirib yuboradi. Java uchun standart chegara metodga 15 ball, bu profile da o'zgartiriladi.

```java
// Sonar shikoyati: Cognitive Complexity 19, ruxsat etilgani 15
public PaymentResult charge(Order order, Card card) {
    if (order != null) {
        if (order.isPaid()) {
            return PaymentResult.alreadyPaid();
        } else {
            if (card.isExpired()) {
                return PaymentResult.rejected("CARD_EXPIRED");
            } else {
                if (order.total().compareTo(card.limit()) > 0) {
                    return PaymentResult.rejected("LIMIT");
                } else {
                    for (Fee fee : order.fees()) {
                        if (fee.isRefundable() && !fee.isApplied()) {
                            applyFee(order, fee);
                        }
                    }
                    return gateway.charge(order, card);
                }
            }
        }
    }
    return PaymentResult.rejected("NO_ORDER");
}
```

Tuzatish yo'li: guard clause bilan darajani yo'qotish va tsiklni metodga chiqarish.

```java
// Cognitive Complexity 4 ga tushdi, har bir qism alohida test qilinadi
public PaymentResult charge(Order order, Card card) {
    if (order == null) return PaymentResult.rejected("NO_ORDER");
    if (order.isPaid()) return PaymentResult.alreadyPaid();
    if (card.isExpired()) return PaymentResult.rejected("CARD_EXPIRED");
    if (exceedsLimit(order, card)) return PaymentResult.rejected("LIMIT");
    applyRefundableFees(order);
    return gateway.charge(order, card);
}

private void applyRefundableFees(Order order) {
    order.fees().stream()
        .filter(fee -> fee.isRefundable() && !fee.isApplied())
        .forEach(fee -> applyFee(order, fee));
}
```

Issue ni lokal ko'rish uchun bitta modulni skanerlash yetadi.

```bash
# faqat to'lov modulini skanerlab, cognitive complexity issue larini ko'rish
./mvnw -pl payment-service -am clean verify sonar:sonar \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login="$SONAR_TOKEN"
```

Tavsiya: cognitive complexity ni refactoring uchun signal deb qabul qil, chegarani ko'tarib issue ni o'chirma.

## 27.2 Juda uzun metod va juda uzun klass

Uzunlik qoidasi faqat qator sanaydi, lekin ko'pincha to'g'ri joyni ko'rsatadi. Hisobot servisidagi uzun metod odatda yig'ish, hisoblash va formatlashni bir joyda bajaradi.

```java
// Sonar shikoyati: metod 140 qator, ruxsat etilgani odatda 75
public byte[] buildMonthlyReport(int year, int month) {
    List<Order> orders = jdbc.query("select ...", rowMapper); // SQL kod ichida
    BigDecimal revenue = BigDecimal.ZERO;
    // ... 40 qator agregatsiya
    // ... 50 qator Excel yacheykalarini to'ldirish
    // ... 30 qator fayl nomini yasash va log yozish
    return bytes;
}
```

Yechim: so'rovni repository ga, agregatsiyani domain klassga, formatlashni alohida writer ga ko'chirish.

```java
// har bir qadam alohida tiplangan, metod 6 qator
public byte[] buildMonthlyReport(ReportPeriod period) {
    List<OrderRow> rows = reportRepository.findOrderRows(period);
    RevenueSummary summary = RevenueSummary.from(rows);
    return excelWriter.write(summary);
}
```

So'rov repository ga chiqqach, SQL ni optimallashtirish osonlashadi.

```sql
-- hisobot uchun agregatsiya bazada bajariladi, Java da emas
select o.status, count(*) as order_count, sum(o.total_amount) as revenue
from orders o
where o.created_at >= :period_start and o.created_at < :period_end
group by o.status;
```

Tavsiya: uzunlik issue sini qator kesib emas, mas'uliyatni ajratib yo'q qil.

## 27.3 Parametrlar soni ko'p metod

Standart chegara 7 parametr. Bunday metodda argumentlar joyi almashsa, kompilyator ham ushlamaydi.

```java
// Sonar shikoyati: 9 parametr, ruxsat etilgani 7
public Payment create(Long orderId, String currency, BigDecimal amount,
                      String cardToken, String payerEmail, String ip,
                      boolean threeDs, String idempotencyKey, String note) {
    // ...
}
```

Parametrlarni ma'noli record ga yig'ish kerak.

```java
// chaqiruv joyi o'qiladigan bo'ldi, yangi maydon qo'shish signaturani buzmaydi
public record PaymentRequest(Long orderId, Money amount, CardData card,
                             PayerContext payer, String idempotencyKey) {}

public Payment create(PaymentRequest request) {
    // ...
}
```

Tavsiya: uchdan ortiq parametr paydo bo'lsa, ularni domain tushunchasi sifatida nomlab record ga yig'.

## 27.4 Ichma-ich joylashgan shartlar va chuqur bloklar

Sonar nazorat strukturalari chuqurligini alohida sanaydi, standart chegara uch daraja. Chuqur blok cognitive complexity ni ham oshiradi, ya'ni bitta joy ikki issue beradi.

```java
// Sonar shikoyati: 4 daraja ichma-ich nazorat strukturasi
for (OrderLine line : order.lines()) {
    if (line.quantity() > 0) {
        if (stock.has(line.sku())) {
            if (!line.isReserved()) {
                reserve(line);
            }
        }
    }
}
```

Shartlarni teskari o'girib `continue` bilan chiqib ketish darajani bitta qoldiradi.

```java
// bitta daraja, har bir shart o'z nomini oldi
for (OrderLine line : order.lines()) {
    if (!isReservable(line)) continue;
    reserve(line);
}

private boolean isReservable(OrderLine line) {
    return line.quantity() > 0 && stock.has(line.sku()) && !line.isReserved();
}
```

Tavsiya: tsikl ichidagi shartlar zanjirini nomlangan predikat metodga chiqar.

## 27.5 Birlashtirish mumkin bo'lgan ketma-ket `if` lar

Agar ichki `if` da `else` bo'lmasa va u tashqi blokdagi yakka operator bo'lsa, Sonar ikki shartni birlashtirishni talab qiladi.

```java
// Sonar shikoyati: bu if ni tashqi if bilan birlashtir
if (order.isConfirmed()) {
    if (order.total().signum() > 0) {
        invoiceService.issue(order);
    }
}
```

```java
// bitta shart, o'qish uchun bir daraja kamaydi
if (order.isConfirmed() && order.total().signum() > 0) {
    invoiceService.issue(order);
}
```

Tavsiya: birlashtirilgan shart uzayib ketsa, uni `&&` bilan qoldirmay nomlangan metodga ol.

## 27.6 Bo'sh blok va bo'sh `catch`

Bo'sh blok qoidasi `if`, `for`, `while` bloklariga tegadi. Bo'sh `catch` alohida qoida bilan ushlanadi va incident tahliliga ham zarar beradi.

```java
// Sonar shikoyati: bo'sh blok va yutilgan exception
try {
    gateway.charge(order);
} catch (GatewayException e) {
}
if (order.isPaid()) {
}
```

Har bir exception uchun qaror kerak: qayta tashlash, kompensatsiya yoki hech bo'lmasa log.

```java
// xato kontekst bilan qayta tashlanadi, blok esa butunlay olib tashlandi
try {
    gateway.charge(order);
} catch (GatewayException e) {
    throw new PaymentFailedException(order.id(), e);
}
```

Tavsiya: exception ni atay yutish kerak bo'lsa, sababini izohda yozib `log.debug` qoldir.

## 27.7 Takrorlangan kod bloki

Duplication qoida emas, metrika. Sonar o'xshash token ketma-ketligini topib `Duplicated Lines (%)` ni hisoblaydi, quality gate esa odatda yangi kod uchun 3 foiz chegara qo'yadi.

```java
// Sonar shikoyati: bu ikki metodda takrorlangan blok bor
public void payOrder(Order o) {
    if (o == null) throw new IllegalArgumentException("order is null");
    if (o.isCancelled()) throw new IllegalStateException("cancelled");
    audit.log("PAY", o.id());
    gateway.charge(o);
}

public void refundOrder(Order o) {
    if (o == null) throw new IllegalArgumentException("order is null");
    if (o.isCancelled()) throw new IllegalStateException("cancelled");
    audit.log("REFUND", o.id());
    gateway.refund(o);
}
```

Umumiy qismni template metodga chiqaramiz.

```java
// tekshirish va audit bir joyda, farq faqat harakatda
private void withValidOrder(Order o, String action, Consumer<Order> op) {
    if (o == null) throw new IllegalArgumentException("order is null");
    if (o.isCancelled()) throw new IllegalStateException("cancelled");
    audit.log(action, o.id());
    op.accept(o);
}
```

Generatsiya qilingan kodni duplication hisobidan chiqarib tashla.

```properties
# generatsiya qilingan va migratsiya fayllari duplication hisobiga kirmasin
sonar.cpd.exclusions=**/generated/**,**/*MapperImpl.java
sonar.exclusions=**/db/migration/**
sonar.java.source=21
```

Tavsiya: duplication ni exclusion bilan yashirishdan avval, blok haqiqatan umumiy mantiq emasligiga ishonch hosil qil.

## 27.8 Takrorlangan satr literali

Bir xil satr literali uch martadan ko'p takrorlansa, Sonar konstanta talab qiladi. Chegara qoida parametri bilan sozlanadi.

```java
// Sonar shikoyati: "PAYMENT_FAILED" literali 4 marta takrorlangan
if (status.equals("PAYMENT_FAILED")) metrics.inc("PAYMENT_FAILED");
if (prev.equals("PAYMENT_FAILED")) audit.log("PAYMENT_FAILED", id);
```

```java
// bitta manba, nomi o'z ma'nosini aytib turadi
private static final String PAYMENT_FAILED = "PAYMENT_FAILED";

if (PAYMENT_FAILED.equals(status)) metrics.inc(PAYMENT_FAILED);
```

Tavsiya: status va xato kodlari uchun satr emas, enum ishlat, shunda qoida ham, kompilyator ham yordam beradi.

## 27.9 Magic number va uni konstantaga chiqarish

Kod ichidagi tushuntirilmagan raqam uchun Sonar nomlangan konstanta so'raydi. `-1`, `0`, `1` kabi qiymatlar odatda istisno qilinadi.

```java
// Sonar shikoyati: 0.02 va 86400 nimani bildiradi, tushunarsiz
BigDecimal fee = amount.multiply(new BigDecimal("0.02"));
if (secondsSincePayment > 86400) markAsSettled(payment);
```

```java
// raqam nomini oldi, biznes qoidasi o'qiladigan bo'ldi
private static final BigDecimal GATEWAY_FEE_RATE = new BigDecimal("0.02");
private static final Duration SETTLEMENT_WINDOW = Duration.ofDays(1);

BigDecimal fee = amount.multiply(GATEWAY_FEE_RATE);
if (sincePayment.compareTo(SETTLEMENT_WINDOW) > 0) markAsSettled(payment);
```

Tavsiya: konstanta nomida qiymatni emas, biznes ma'nosini yoz, masalan `GATEWAY_FEE_RATE`.

## 27.10 Ortiqcha mahalliy o'zgaruvchi va darhol qaytariladigan qiymat

Ikki qoida bor: darhol qaytariladigan o'zgaruvchi va hech qachon o'qilmaydigan qiymat berish. Ikkinchisi xavfliroq, chunki u ko'pincha haqiqiy bug ni yashiradi.

```java
// Sonar shikoyati: natija darhol qaytariladi, total esa hech qachon o'qilmaydi
public BigDecimal total(Order order) {
    BigDecimal total = BigDecimal.ZERO;
    BigDecimal result = order.lines().stream()
        .map(OrderLine::amount).reduce(BigDecimal.ZERO, BigDecimal::add);
    return result;
}
```

```java
// ortiqcha o'zgaruvchilar yo'q, ifoda to'g'ridan to'g'ri qaytariladi
public BigDecimal total(Order order) {
    return order.lines().stream()
        .map(OrderLine::amount)
        .reduce(BigDecimal.ZERO, BigDecimal::add);
}
```

Tavsiya: ishlatilmaydigan qiymat berish issue sini o'chirishdan oldin, u yerda yo'qolgan mantiq yo'qligini tekshir.

## 27.11 Keraksiz `else` va erta qaytish bilan soddalashtirish

`return` dan keyingi `else` va boolean ifodani `if/else` bilan qaytarish alohida qoidalar bilan belgilanadi.

```java
// Sonar shikoyati: bu if-then-else ni bitta return bilan almashtir
public boolean isRefundable(Payment p) {
    if (p.isSettled() && !p.isDisputed()) {
        return true;
    } else {
        return false;
    }
}
```

```java
// shart o'zi javob, qo'shimcha shoxlanish yo'q
public boolean isRefundable(Payment p) {
    return p.isSettled() && !p.isDisputed();
}
```

Tavsiya: validatsiya qadamlarini guard clause bilan boshida qaytar, asosiy mantiqni `else` ichida saqlama.

## 27.12 Ternar operatorlarni ichma-ich joylash

Ichma-ich ternar ifodani o'qishda xato qilish ehtimoli yuqori, shuning uchun Sonar alohida qoida beradi.

```java
// Sonar shikoyati: ichma-ich ternar operatorni alohida ifodaga chiqar
String label = p.isPaid() ? "PAID"
    : p.isPending() ? (p.isDisputed() ? "DISPUTED" : "PENDING")
    : "FAILED";
```

```java
// qarorlar switch da ko'rinadi, har bir shoxni test qilish oson
String label = switch (p.state()) {
    case PAID -> "PAID";
    case PENDING -> p.isDisputed() ? "DISPUTED" : "PENDING";
    case FAILED -> "FAILED";
};
```

Tavsiya: bitta daraja ternar qoldir, ikkinchi darajaga ehtiyoj tug'ilsa `switch` yoki metodga o't.

## 27.13 `switch` da `default` yo'qligi va qamrab olinmagan holat

Sonar `switch` barcha holatni qamrab olishini talab qiladi. Eski uslubdagi `switch` da `default` yetishmasa issue tushadi, `switch` expression da esa kompilyator o'zi talab qiladi.

```java
// Sonar shikoyati: default branch yo'q, yangi enum qiymati jim o'tadi
switch (order.status()) {
    case NEW: reserveStock(order); break;
    case PAID: ship(order); break;
    case CANCELLED: releaseStock(order); break;
}
```

```java
// barcha holat qamrab olingan, kutilmagan qiymat aniq xato beradi
switch (order.status()) {
    case NEW -> reserveStock(order);
    case PAID -> ship(order);
    case CANCELLED -> releaseStock(order);
    default -> throw new IllegalStateException("Noma'lum status: " + order.status());
}
```

Tavsiya: enum ustidagi `switch` ni expression shaklida yoz, shunda yangi qiymat qo'shilganda build buziladi.

## 27.14 Umumiy `Exception` ni ushlash yoki tashlash

`Exception` yoki `Throwable` ni tashlash uchun bitta qoida, ularni ushlash uchun boshqasi ishlaydi. Ikkisi ham chaqiruvchidan xatoni ajratish imkonini tortib oladi.

```java
// Sonar shikoyati: umumiy exception tashlanadi va umumiy exception ushlanadi
public void settle(Payment p) throws Exception {
    try {
        gateway.settle(p);
    } catch (Exception e) {
        log.error("xato", e);
    }
}
```

```java
// aniq tip tashlanadi, faqat kutilgan xato ushlanadi
public void settle(Payment p) throws SettlementException {
    try {
        gateway.settle(p);
    } catch (GatewayTimeoutException e) {
        throw new SettlementException(p.id(), e);
    }
}
```

Tavsiya: har bir texnik xatoni domain xatosiga o'rab tashla, `catch (Exception e)` ni faqat eng tashqi chegarada qoldir.

## 27.15 Oddiy yondashuv va arxitektor yondashuvi

| Holat | Oddiy yondashuv | Arxitektor yondashuvi |
| --- | --- | --- |
| Cognitive complexity issue | Chegarani profile da 25 ga ko'taradi | Metodni bo'lib, chegarani tegmasdan qoldiradi |
| Uzun metod | Qatorlarni qisqartirib bir satrga yig'adi | Mas'uliyatni ajratib alohida klassga chiqaradi |
| Ko'p parametr | Oxirgi parametrlarni `Map` ga tiqadi | Domain record kiritadi va tiplashni kuchaytiradi |
| Duplication | `sonar.cpd.exclusions` ga qo'shadi | Umumiy mantiqni ajratadi, exclusion faqat generatsiya uchun |
| Takrorlangan literal | `NOSONAR` izohi qo'yadi | Enum yoki konstanta kiritadi |
| Magic number | Izoh yozib qoldiradi | Nomlangan konstanta va birlik tipini kiritadi |
| Bo'sh `catch` | `e.printStackTrace()` qo'shib issue ni yopadi | Xatoni domain exception ga o'rab qayta tashlaydi |
| `switch` da `default` yo'q | `default: break;` yozadi | `switch` expression ga o'tib, kutilmagan holatni xato qiladi |
| Issue oqimi | Oyda bir marta ko'p issue ni yopadi | Yangi kod shartini CI da majburiy qiladi, qarz o'smaydi |

## 27.16 Tuzoq va yechim

| Tuzoq | Nega xavfli | Yechim |
| --- | --- | --- |
| `// NOSONAR` ni ommaviy ishlatish | Issue yo'qoladi, muammo qoladi | Faqat sababi izohlangan yakka holatda, review bilan |
| Chegaralarni issue yo'qolgunicha ko'tarish | Quality gate ma'nosini yo'qotadi | Chegarani qattiq qoldirib, yangi kodga shart qo'yish |
| Butun modulni `sonar.exclusions` ga kiritish | Modul o'lchovsiz qoladi | Faqat generatsiya qilingan kodni chiqarish |
| Code smell larni bug bilan bir navbatda ko'rish | Reliability issue lari kechikadi | Toifa bo'yicha ajratib, bug va vulnerability ni oldin yopish |
| Refactoring ni testsiz boshlash | Xulq o'zgarib ketadi, Sonar sezmaydi | Avval mavjud xulqni test bilan qulflash, keyin bo'lish |
| Faqat lokal scan ga ishonish | Branch va quality gate holati ko'rinmaydi | CI da scan va gate natijasini majburiy qadam qilish |

Chegaralarni loyihada bir marta mahkamlab qo'y, shunda hamma bir xil natija oladi.

```xml
<!-- scan konfiguratsiyasi pom.xml da turadi, lokal va CI bir xil ishlaydi -->
<properties>
  <sonar.projectKey>payment-service</sonar.projectKey>
  <sonar.java.source>21</sonar.java.source>
  <sonar.cpd.exclusions>**/generated/**</sonar.cpd.exclusions>
  <sonar.coverage.jacoco.xmlReportPaths>
    ${project.build.directory}/site/jacoco/jacoco.xml
  </sonar.coverage.jacoco.xmlReportPaths>
</properties>
```

CI da gate natijasini kutish kerak, aks holda build yashil, gate esa qizil qoladi.

```yaml
# gate natijasini kutmasa, CI yashil bo'lib code smell o'tib ketadi
- name: Sonar scan va gate
  run: |
    ./mvnw -B clean verify sonar:sonar \
      -Dsonar.qualitygate.wait=true
  env:
    SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

## 27.17 Amalda qo'llash

- [ ] To'lov, buyurtma va hisobot servislaridagi cognitive complexity issue larini ro'yxatga olib, eng yuqori ballli uchta metodni guard clause bilan bo'l.
- [ ] Yetti va undan ko'p parametrli metodlarni topib, har birini domain record ga aylantir.
- [ ] Barcha bo'sh `catch` bloklarini ko'rib chiq va har birini domain exception ga o'rab qayta tashla.
- [ ] Uch martadan ko'p takrorlangan status literallarini enum ga ko'chir, konstantani bitta joyda qoldir.
- [ ] `sonar.cpd.exclusions` va `sonar.exclusions` ro'yxatini tozalab, faqat generatsiya qilingan kodni qoldir.
- [ ] Eski uslubdagi enum `switch` larni `switch` expression ga o'tkaz va kutilmagan qiymatga xato tashla.
- [ ] CI pipeline ga `-Dsonar.qualitygate.wait=true` qo'shib, gate qizil bo'lsa build yiqilishini ta'minla.
- [ ] Refactoring dan oldin mavjud xulqni test bilan qulfla, [testlash qo'llanmasidagi](../testing/README.md) xulq-markazli test mavzusiga tayan.

---

[&larr; 26. Xato katalogi: security](26-xato-katalogi-security-vulnerability-va.md) · [Mundarija](README.md) · [28. Xato katalogi: maintainability, nomlash, o'lik kod va uslub &rarr;](28-xato-katalogi-maintainability-nomlash-olik.md)
