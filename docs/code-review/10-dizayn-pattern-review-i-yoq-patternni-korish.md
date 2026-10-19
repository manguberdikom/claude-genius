<!-- doc: code-review | chapter: 10 | part: II. Arxitektura, dizayn va clean code review -->

[Barcha hujjatlar](../../README.md) / [Kod review](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 10. Dizayn pattern review I: yo'q patternni ko'rish (Missing Patterns)

<details>
<summary>Bu bobdagi 12 bo'lim</summary>

- [10.1 Pattern bo'shlig'ining umumiy belgilari](#101-pattern-boshligining-umumiy-belgilari)
- [10.2 Shoxlanishdan polimorfizmga: eng ko'p uchraydigan bo'shliq](#102-shoxlanishdan-polimorfizmga-eng-kop-uchraydigan-boshliq)
- [10.3 Yaratish mantiqi tarqalganda: fabrika](#103-yaratish-mantiqi-tarqalganda-fabrika)
- [10.4 Parametrlar portlashi: builder yoki parametr obyekti](#104-parametrlar-portlashi-builder-yoki-parametr-obyekti)
- [10.5 Kesishgan vazifalar qo'lda yozilganda: decorator yoki AOP](#105-kesishgan-vazifalar-qolda-yozilganda-decorator-yoki-aop)
- [10.6 Holat shoxlari: yashiringan holat mashinasi](#106-holat-shoxlari-yashiringan-holat-mashinasi)
- [10.7 Tashqi tizim domen ichida: adapter va port](#107-tashqi-tizim-domen-ichida-adapter-va-port)
- [10.8 Yozuv va xabar birga bo'lishi kerak bo'lganda: outbox](#108-yozuv-va-xabar-birga-bolishi-kerak-bolganda-outbox)
- [10.9 Ikki marta kelgan so'rov: idempotentlik](#109-ikki-marta-kelgan-sorov-idempotentlik)
- [10.10 Ko'p bosqichli jarayon: saga va kompensatsiya](#1010-kop-bosqichli-jarayon-saga-va-kompensatsiya)
- [10.11 Pattern taklif qilishning narxi](#1011-pattern-taklif-qilishning-narxi)
- [10.12 Amalda qo'llash](#1012-amalda-qollash)

</details>


Review ning eng yuqori qiymatli qismi - kodda pattern o'rni bo'sh qolganini ko'rish. Bu "pattern ishlatish kerak" degan talab emas: pattern o'zi maqsad emas. Mohiyat boshqa - takrorlanadigan muammoning ma'lum yechimi bor, va muallif uni qo'lda, yarim holda, xatolari bilan qayta yozyapti. Reviewer ning ishi shu holatni belgi orqali tanib olish va tayyor yechimni ko'rsatish. Patternlarning to'liq katalogi [Dizayn patternlar](../patterns/README.md) da, bu yerda faqat diffdagi belgilar va review javoblari.

## 10.1 Pattern bo'shlig'ining umumiy belgilari

| Diffdagi belgi | Nimani bildiradi | Qaysi yechim |
| --- | --- | --- |
| Enum bo'yicha `switch` uch va ko'p joyda | Xulq ma'lumot bilan birga turmaydi | Fowler: Replace Conditional with Polymorphism; enum ichida xulq |
| `if (type == A) ... else if (type == B)` o'sib boryapti | Yangi tur har joyda eslanishi kerak | Fowler: Replace Type Code with Subclasses yoki State/Strategy |
| Obyekt yaratish mantiqi uch joyda takrorlangan | Yaratish qoidasi tarqalgan | Fowler: Replace Constructor with Factory Method |
| Konstruktorda 6+ parametr, ko'pi bir xil turda | Argumentni almashtirib qo'yish tutilmaydi | Fowler: Introduce Parameter Object |
| Konstruktorda ko'p ixtiyoriy maydon, qurilish bosqichli | Bir chaqiruvda qurish noqulay | GoF: Builder |
| Har metodda bir xil `try/catch/log/metric` o'rami | Kesishgan vazifa qo'lda yozilgan | GoF: Decorator (mas'uliyat qo'shish); AOP, `@Retryable` |
| Tashqi obyektga kirishni boshqarish kerak (masofaviy, kech yuklanadigan, huquq tekshiriladigan) | Kirish nazorati tarqalgan | GoF: Proxy (kirishni boshqarish) |
| `status` bo'yicha `if` lar va qo'lda o'tishlar | Holat mashinasi yashiringan | Aniq o'tish jadvali; xulq holatga bog'liq bo'lsa Fowler: Replace Type Code with State/Strategy |
| Tashqi API chaqiruvi domen ichida | Chegara yo'q | GoF: Adapter; port |
| DB yozuvi va keyin xabar yuborish | Atomiklik yo'q | Richardson: Transactional outbox |
| Bir xil so'rov yoki xabar ikki marta kelsa dublikat | Idempotentlik yo'q | Idempotent ishlovchi + bazada yagonalik |
| Ko'p bosqichli jarayon bitta metodda, qaytarish yo'q | Mustaqil tizimlar nomuvofiq qoladi | Richardson: Saga va kompensatsiya |
| Har joyda `new RestClient(...)` | Konfiguratsiya tarqalgan | Bitta sozlangan bean |
| Katta `Map<String,Object>` konfiguratsiya | Shartnoma yo'q | `@ConfigurationProperties` tipli obyekt |

Jadvalda ikki nom qasddan ajratilgan. Birinchisi - Decorator va Proxy. GoF ikkisining
niyatini aniq farqlaydi: Decorator obyektga dinamik ravishda qo'shimcha mas'uliyat
qo'shadi, Proxy esa obyektning o'rnini bosib unga kirishni boshqaradi (GoF, 175 va
207-bet). GoF ning strukturaviy patternlar muhokamasida bu farq yana bir marta
ta'kidlanadi: Proxy da asosiy funksiyani subyektning o'zi beradi, proxy esa unga
kirishga ruxsat beradi yoki rad etadi; Decorator da komponent funksiyaning faqat bir
qismini beradi, qolganini dekoratorlar qo'shadi (GoF, 220-bet).

Ikkinchisi - Chain of Responsibility. U ko'p bosqichli jarayon uchun emas: GoF da uning
vazifasi so'rovni bir necha nomzoddan biri bajarishi, va GoF ning o'zi uning uchinchi
oqibatini "qabul qilinishi kafolatlanmagan" deb yozadi - so'rov zanjir oxiriga yetib,
umuman bajarilmasligi mumkin (GoF, 223 va 226-bet). Har bosqichi bajarilishi shart
bo'lgan jarayon uchun bu noto'g'ri nom; 10.10 dagi saga shakli ishlatiladi.

## 10.2 Shoxlanishdan polimorfizmga: eng ko'p uchraydigan bo'shliq

Belgi aniq: bir xil `switch` ikki yoki uch joyda takrorlangan. Oqibati ham aniq: yangi qiymat qo'shilganda uchinchi joy esdan chiqadi, va xato prodda chiqadi.

```java
// Belgi: bir xil enum bo'yicha uch joyda shoxlanish.
// DiscountService.java
switch (tier) { case GOLD -> 0.15; case SILVER -> 0.05; case BRONZE -> 0.0; }
// ShippingService.java
switch (tier) { case GOLD -> Money.ZERO; case SILVER -> fee(50); ... }
// SupportService.java
switch (tier) { case GOLD -> Priority.HIGH; ... }

// Review javobi 1: xulqni enum ichiga olish (eng oddiy, Java da tabiiy).
public enum CustomerTier {
    GOLD(new BigDecimal("0.15"), Money.ZERO, Priority.HIGH),
    SILVER(new BigDecimal("0.05"), Money.of(50), Priority.NORMAL),
    BRONZE(BigDecimal.ZERO, Money.of(100), Priority.LOW);

    private final BigDecimal discountRate;
    private final Money shippingFee;
    private final Priority supportPriority;
    // konstruktor va getterlar

    public Money discountOn(Money total) { return total.multiply(discountRate); }
}
// Foydasi: yangi daraja qo'shilganda kompilyator uch joyni emas, bir joyni
// talab qiladi va hech narsa esdan chiqmaydi.

// Review javobi 2: tur qiymati obyekt yaratilgandan keyin o'zgarsa, yoki sinf
// boshqa sabab bilan allaqachon subclass qilingan bo'lsa - Strategy/State obyekti.
public interface TierPolicy {
    CustomerTier tier();
    Money discountOn(Money total);
    Money shippingFee(Weight weight);
}
@Component
class GoldPolicy implements TierPolicy { /* ... */ }
// Spring List<TierPolicy> ni o'zi yig'adi; registr 9.2 da ko'rsatilgan.
```

Bu refaktoringning kitobdagi nomi - Fowler, *Replace Conditional with Polymorphism*
(1999, 205-206-bet; 2-nashrda, 2019, 272-bet). Fowler ning asosiy dalili aynan yuqoridagi
belgi bilan bir xil: polimorfizmdan eng katta foyda bir xil shartlar to'plami
programmaning ko'p joyida takrorlanganda olinadi, chunki yangi tur qo'shilganda
shartlarning hammasini topib tuzatish kerak bo'ladi, subclass bilan esa faqat yangi
subclass yoziladi (1999, 205-bet).

Polimorfizm uchun kerakli ierarxiyani qurishning ikki yo'li bor va tanlash sharti
kitobda aniq: odatda *Replace Type Code with Subclasses* ishlatiladi, lekin tur
qiymati obyekt yaratilgandan keyin o'zgarsa yoki sinf boshqa sabab bilan allaqachon
subclass qilingan bo'lsa, subclass qilish mumkin emas va *Replace Type Code with
State/Strategy* ishlatiladi (Fowler 1999, 181 va 205-bet). Yuqoridagi ikkinchi javob
shu holat uchun.

Qachon `switch` qoldiriladi: bitta joyda, kichik va barqaror to'plam uchun. `sealed interface` bilan birga ishlatilsa, kompilyator to'liqligini tekshiradi - bu holat polimorfizmdan ham yaxshiroq bo'lishi mumkin ([17-bob](17-zamonaviy-java-review-record-sealed-pattern.md)).

## 10.3 Yaratish mantiqi tarqalganda: fabrika

Belgi: bir xil obyektni qurish uchun kerak bo'lgan to'rt qator uch joyda takrorlangan, va ularning biri boshqalaridan farq qiladi (xato shu farqda).

```java
// Belgi: audit yozuvini qurish uch joyda takrorlangan, biri zonani
// boshqacha qo'ygan - hisobotlarda bir soatlik siljish.
AuditEvent e = new AuditEvent();
e.setUserId(currentUser.getId());
e.setAt(LocalDateTime.now());                 // boshqa joyda Instant.now()
e.setAction("ORDER_CANCELLED");
e.setDetails(objectMapper.writeValueAsString(order));

// Review javobi: yaratish qoidasi bitta joyda, nomlangan fabrika metodi bilan.
public record AuditEvent(UserId userId, Instant at, AuditAction action, String payloadJson) {

    public static AuditEvent of(UserId user, AuditAction action, Object payload, Clock clock) {
        return new AuditEvent(user, clock.instant(), action, Json.write(payload));
    }
}
// Foydasi: vaqt manbasi bitta (Clock - testlanadi), serializatsiya bitta,
// va yangi majburiy maydon qo'shilsa kompilyator hamma joyni ko'rsatadi.
```

Nomlashda diqqat: bu yerdagi `AuditEvent.of(...)` - GoF ning Factory Method i emas.
GoF Factory Method ining niyati boshqa: obyekt yaratish uchun interfeys e'lon
qilinadi, lekin qaysi sinf yaratilishini subclasslar hal qiladi (GoF, 107-bet).
Yuqoridagi statik metodda hech qanday subclass yo'q. Uning kitobdagi nomi - Fowler,
*Replace Constructor with Factory Method* (1999, 246-bet; 2-nashrda, 2019, *Replace
Constructor with Factory Function*, 334-bet): oddiy qurishdan ko'proq ish qilish
kerak bo'lganda konstruktor fabrika metodi bilan almashtiriladi. Review izohida
shu nom ishlatilsa, muallif noto'g'ri patternni izlab ketmaydi.

GoF ning o'zi bu yerda ortiqcha ish qilmaslikni ham eslatadi: Factory Method
dizaynni moslashuvchan qiladi, lekin yaratilayotgan sinf hech qachon o'zgarmasa
yoki yaratish subclass oson override qila oladigan operatsiyada bo'lsa, u shart
emas (GoF, 136-bet).

## 10.4 Parametrlar portlashi: builder yoki parametr obyekti

Belgi: konstruktor yoki metodda 6+ parametr, ularning bir nechtasi bir xil turda. Oqibati: parametrlarni almashtirib qo'yish kompilyatsiyada tutilmaydi.

```java
// Xavfli: besh String ketma-ket. Almashtirilsa, kompilyator jim.
new ShipmentRequest(orderId, address, city, region, postalCode, phone, note);

// Yechim 1: domen turlari (eng ishonchli).
new ShipmentRequest(new OrderId(id), new Address(city, region, postalCode), new Phone(phone), note);

// Yechim 2: builder (ixtiyoriy maydonlar ko'p bo'lsa).
ShipmentRequest.builder()
    .orderId(orderId)
    .address(address)
    .phone(phone)
    .note(note)                     // ixtiyoriy
    .build();                       // build() ichida majburiy maydonlar tekshiriladi

// Review diqqati: builder ishlatilsa, majburiy maydonlar tekshirilishi
// shart. Aks holda builder konstruktordan xavfsizroq emas - u faqat
// xatoni kompilyatsiyadan ish vaqtiga ko'chiradi.
```

Ikki yechimni almashtirib yubormaslik kerak, chunki ular turli muammolarni hal
qiladi.

Birinchi yechim - argument tartibi muammosi. Birga yuradigan parametrlar guruhi
bitta obyektga aylantiriladi; Fowler bu refaktoringni *Introduce Parameter Object*
deb ataydi (1999, 238-bet; 2-nashrda, 2019, 140-bet) va sababini shunday beradi: bunday
guruh data clump, uzun parametr ro'yxatini tushunish qiyin, obyekt esa ro'yxatni
qisqartiradi va keyinchalik parametrlar ustidagi takroriy mantiqni ham o'ziga
tortadi. Argumentni almashtirib qo'yishdan himoya shu yechimdan keladi, chunki
turlar boshqacha bo'ladi.

Ikkinchi yechim - Builder. GoF da uning niyati argument xavfsizligi emas:
murakkab obyektning qurilishini uning tasvirlanishidan ajratish, shunda bir xil
qurish jarayoni turli tasvirlar yaratishi mumkin bo'ladi (GoF, 97-bet). GoF
sanab o'tgan foydalar ham shu haqda: mahsulotning ichki tasvirini almashtirish,
qurish kodini tasvirlashdan ajratish va qurish jarayonini qadamlab boshqarish
(GoF, 100-bet). Shuning uchun review izohida "argumentlar almashib ketmasligi
uchun builder" emas, "bu besh parametr bitta obyekt" deyiladi.

## 10.5 Kesishgan vazifalar qo'lda yozilganda: decorator yoki AOP

Belgi: o'nta metodda bir xil `try { ... } catch { log; metric }` o'rami. Oqibati: o'n birinchi metodda o'ram esdan chiqadi va xato ko'rinmay qoladi.

```java
// Belgi: har metodda qo'lda retry va o'lchov.
public PaymentResult charge(ChargeCommand cmd) {
    int attempt = 0;
    while (true) {
        long start = System.nanoTime();
        try {
            PaymentResult r = gateway.charge(cmd);
            meter.timer("gateway.charge").record(System.nanoTime() - start, NANOSECONDS);
            return r;
        } catch (GatewayTimeout e) {
            if (++attempt >= 3) throw e;
            sleep(100L * attempt);            // qo'lda backoff, jitter yo'q
        }
    }
}

// Review javobi: tayyor mexanizmlardan foydalanish. Retry siyosati
// deklarativ, o'lchov avtomatik, kod faqat biznes qismini saqlaydi.
@Service
public class PaymentService {

    @Retry(name = "gateway")                  // Resilience4j: backoff + jitter
    @CircuitBreaker(name = "gateway", fallbackMethod = "queueForLater")
    @Timed(value = "gateway.charge")          // Micrometer
    public PaymentResult charge(ChargeCommand cmd) {
        return gateway.charge(cmd);
    }

    private PaymentResult queueForLater(ChargeCommand cmd, CallNotPermittedException e) {
        outbox.enqueue(cmd);
        return PaymentResult.pending();
    }
}
```

```yaml
# Siyosat konfiguratsiyada: review da raqamlar muhokama qilinadi, kod emas.
resilience4j:
  retry:
    instances:
      gateway:
        max-attempts: 3
        wait-duration: 200ms
        enable-exponential-backoff: true
        exponential-backoff-multiplier: 2
        enable-randomized-wait: true          # jitter: retry bo'ronini oldini oladi
        retry-exceptions:
          - java.net.SocketTimeoutException   # faqat qayta urinishga arziydiganlar
        ignore-exceptions:
          - com.acme.payment.CardDeclined     # biznes rad etishi - retry qilinmaydi
  circuitbreaker:
    instances:
      gateway:
        sliding-window-size: 50
        failure-rate-threshold: 50
        wait-duration-in-open-state: 30s
```

Review da asosiy savol konfiguratsiyaga qaratiladi: qaysi istisnolar retry qilinadi. `retry-exceptions` ga biznes xatolari (karta rad etildi, yetarli mablag' yo'q) kirib qolsa, tizim bir xil rad etishni uch marta takrorlaydi va foydalanuvchiga uch marta SMS keladi.

Nomlashda ikkinchi diqqat: Spring ning `@Retryable` va `@Transactional` mexanizmi
proxy orqali ishlaydi, lekin bu yerda taklif qilinayotgan yechimning niyati
Decorator ga tegishli. GoF ikki patternni niyati bo'yicha ajratadi. Decorator
obyektga dinamik ravishda qo'shimcha mas'uliyat qo'shadi va subclass qilishga
moslashuvchan alternativa beradi (GoF, 175-bet); Proxy esa boshqa obyektning
o'rnini bosib unga kirishni boshqaradi (GoF, 207-bet). GoF ning strukturaviy
patternlar muhokamasi farqni amaliy shaklga keltiradi: Proxy da asosiy funksiyani
subyekt beradi, proxy esa unga kirishga ruxsat beradi yoki rad etadi, va proxy
dinamik ravishda xususiyat qo'shish yoki olib tashlash uchun mo'ljallanmagan;
Decorator da esa komponent funksiyaning faqat bir qismini beradi, qolganini bir
yoki bir nechta dekorator qo'shadi, shuning uchun rekursiv kompozitsiya
Decorator ning ajralmas qismi (GoF, 220-bet).

Review uchun bu farq amaliy: o'ram retry, o'lchov yoki kesh qo'shsa - bu
Decorator, va review savoli "zanjir tartibi qanday" bo'ladi (11.6). O'ram
kirishni tekshirsa yoki real obyektni kechiktirib yaratsa - bu Proxy, va review
savoli "kirish rad etilganda nima qaytadi" bo'ladi.

## 10.6 Holat shoxlari: yashiringan holat mashinasi

Belgi: `status` maydoni bo'yicha `if` lar turli joylarda, va holat o'tishlari `setStatus` bilan qo'lda qilinadi. Oqibati: taqiqlangan o'tish (bekor qilingan buyurtmani jo'natish) hech narsa bilan to'xtatilmaydi.

Quyidagi yechim - o'tish jadvali, va uni GoF ning State pattern i deb atash xato.
GoF State da xulq holat sinflariga ko'chiriladi: har holat alohida sinf bo'ladi,
Context joriy holat obyektiga so'rovni delegat qiladi va holat o'zgarganda
ishlatayotgan obyektini almashtiradi; GoF shartning har tarmog'i alohida sinfga
tushishini aynan shunday ta'riflaydi (GoF, 305-306-bet). O'tish jadvali esa hech
qanday xulqni ko'chirmaydi - u faqat ruxsat etilgan o'tishlarni e'lon qiladi.
Agar xulqning o'zi holatga qarab o'zgarsa, kerakli refaktoringning kitobdagi nomi
- Fowler, *Replace Type Code with State/Strategy* (1999, 184-bet): tur kodi holat
obyekti bilan almashtiriladi va bu GoF ning state yoki strategy pattern iga
tayanadi. Fowler shu yerda ikkisidan birini tanlash mexanikani o'zgartirmasligini
ham aytadi: bitta algoritmni soddalashtirsa strategy, holatga xos ma'lumot
ko'chirilsa va obyekt holat almashtiradi deb qaralsa state (1999, 184-bet).

```java
// Review javobi: o'tishlarni aniq e'lon qilish. Oddiy va o'qiladigan shakl.
public enum OrderStatus {
    NEW(EnumSet.of(PAID, CANCELLED)),
    PAID(EnumSet.of(SHIPPED, REFUNDED)),
    SHIPPED(EnumSet.of(DELIVERED)),
    DELIVERED(EnumSet.noneOf(OrderStatus.class)),   // terminal
    CANCELLED(EnumSet.noneOf(OrderStatus.class)),
    REFUNDED(EnumSet.noneOf(OrderStatus.class));

    private final Set<OrderStatus> allowed;
    OrderStatus(Set<OrderStatus> allowed) { this.allowed = allowed; }

    public void checkTransitionTo(OrderStatus next) {
        if (!allowed.contains(next)) {
            throw new IllegalStateTransition(this, next);
        }
    }
}
// Order ichida:
public void transitionTo(OrderStatus next) {
    status.checkTransitionTo(next);
    this.status = next;
}
// Foydasi: taqiqlangan o'tish bitta joyda to'xtatiladi, va o'tishlar
// jadvali kodda hujjat sifatida turadi. Testda ham o'tish matritsasini
// to'liq tekshirish mumkin ([34-bob](34-test-toliqligini-review-qilish.md)).
```

Head First ham shu ikkisini ajratishni ta'kidlaydi: Strategy va State strukturasi
deyarli bir xil, lekin niyatlari butunlay boshqa (Freeman/Robson, 381-bet). Farqni
kitob shunday beradi: Strategy da klient odatda obyektga qaysi strategiyani
berishni o'zi boshqaradi, State da esa Context vaqt o'tishi bilan o'z holatini
aniq belgilangan o'tishlar bo'yicha o'zi almashtiradi, ya'ni xulqni o'zgartirish
patternning ishlash usuliga kiritilgan (Freeman/Robson, 414-415-bet). Diffda
`setStatus` ko'rinsa, mavzu State ga tegishli; `setPolicy` ko'rinsa - Strategy ga.

Qo'shimcha review savoli: holat o'tishi ma'lumotlar bazasida ham himoyalanganmi. Ikki parallel so'rov bir vaqtda `PAID` dan `SHIPPED` va `REFUNDED` ga o'tkazishi mumkin. Shu sababli o'tish `UPDATE ... WHERE status = 'PAID'` shaklida yoki optimistik versiya bilan bajarilishi kerak ([27-bob](27-izolyatsiya-poyga-holatlari-va-xabar.md)).

## 10.7 Tashqi tizim domen ichida: adapter va port

Belgi: domen yoki servis kodida `RestClient`, `WebClient`, SDK klassi yoki `HttpHeaders` ko'rinadi. Oqibati: domen testi tarmoqqa bog'liq bo'ladi, vendor almashtirilsa biznes kodi o'zgaradi, va vendor xato formatlari biznes mantiqiga tarqaydi.

```java
// Belgi: biznes metodi HTTP detallarini biladi.
public Order place(PlaceOrder cmd) {
    HttpHeaders h = new HttpHeaders();
    h.setBearerAuth(tokenStore.get());
    ResponseEntity<Map> resp = restTemplate.exchange(
        "https://fraud.vendor.io/v2/score", POST, new HttpEntity<>(body, h), Map.class);
    if (((Number) resp.getBody().get("score")).intValue() > 80) {   // "magic" 80
        throw new FraudSuspected();
    }
    ...
}

// Review javobi: port domen tilida, adapter detallarni yashiradi.
public interface FraudScoring {                      // domen porti
    FraudVerdict score(OrderDraft draft);
}
public enum FraudVerdict { ALLOW, REVIEW, BLOCK }

@Component
class VendorFraudScoring implements FraudScoring {   // infra adapteri
    @Override public FraudVerdict score(OrderDraft draft) {
        ScoreResponse r = client.post()... .body(ScoreResponse.class);
        return r.score() > blockThreshold ? BLOCK
             : r.score() > reviewThreshold ? REVIEW : ALLOW;
    }
}
// Foydasi: chegara raqamlari bitta joyda va konfiguratsiyada; domen
// faqat uch holatni biladi; test uchun tarmoq kerak emas.
```

Nom kitobdan keladi: GoF da Adapter ning niyati sinfning interfeysini klient
kutgan boshqa interfeysga o'girish, shunda interfeyslari mos kelmagani uchun
birga ishlay olmaydigan sinflar birga ishlay oladi (GoF, 139-bet). Yuqoridagi
`VendorFraudScoring` aynan shuni qiladi: vendor javobini domen kutgan uch
qiymatli verdiktga o'giradi. GoF Adapter ni Facade dan ham ajratadi - facade
yangi interfeys e'lon qiladi, adapter esa mavjud interfeysni qayta ishlatadi
(GoF, 219-bet), shuning uchun port domen tilida bo'lishi muhim: u yangi emas,
domenning allaqachon mavjud tili.

## 10.8 Yozuv va xabar birga bo'lishi kerak bo'lganda: outbox

Belgi: bitta metodda `repository.save(...)` va keyin `kafkaTemplate.send(...)` yoki tashqi HTTP chaqiruvi. Oqibati: ikkisidan biri bajarilib, ikkinchisi bajarilmasligi mumkin, va tizim holatlari ajralib ketadi.

```java
// Belgi: ikki tizimga yozuv, atomiklik yo'q.
@Transactional
public void place(PlaceOrder cmd) {
    Order order = orders.save(Order.from(cmd));
    kafka.send("orders", new OrderPlaced(order.id()));   // commit dan oldin!
}
// Uch xil nosozlik: (1) kafka o'tdi, commit yiqildi - xabar bor, buyurtma
// yo'q; (2) commit o'tdi, kafka yiqildi - buyurtma bor, xabar yo'q;
// (3) kafka sekin - DB tranzaksiyasi va qulf uzoq ushlanadi.

// Review javobi: xabar bir xil tranzaksiyada jadvalga yoziladi.
@Transactional
public void place(PlaceOrder cmd) {
    Order order = orders.save(Order.from(cmd));
    outbox.save(OutboxMessage.of("orders", new OrderPlaced(order.id())));  // atomik
}
```

```sql
-- Outbox jadvali va uning indeksi: workerlar bir-birini kutmaydi.
CREATE TABLE outbox_message (
    id           bigserial PRIMARY KEY,
    topic        text        NOT NULL,
    payload      jsonb       NOT NULL,
    created_at   timestamptz NOT NULL DEFAULT now(),
    published_at timestamptz,
    attempts     int         NOT NULL DEFAULT 0
);
-- Faqat yuborilmaganlar uchun partial indeks: jadval o'sganda ham kichik.
CREATE INDEX outbox_pending_idx ON outbox_message (created_at)
    WHERE published_at IS NULL;
```

Patternning nomi va mohiyati Richardson da yozilgan: xabar ma'lumotlar bazasi
tranzaksiyasining bir qismi sifatida bazadagi OUTBOX jadvaliga saqlanib
e'lon qilinadi; atomiklik shu yerdan keladi, chunki bu bitta lokal ACID
tranzaksiya, jadval vaqtinchalik navbat vazifasini bajaradi va alohida komponent
uni o'qib brokerga chiqaradi (Richardson, 3-bob, 98-bet).

Review ning qo'shimcha savollari: outbox tozalanadimi (aks holda jadval cheksiz o'sadi), xabar tartibi muhimmi (bo'lsa, agregat bo'yicha ketma-ketlik kerak), va iste'molchi dublikatga tayyormi (outbox "kamida bir marta" yetkazadi).

Mavzuning to'liq yozuvi [transactional outbox](../patterns/10-malumotlarni-boshqarish-va-taqsimlash.md#1014-tranzaksion-outbox-transactional-outbox) bo'limida; bu yerda faqat shu bo'limning nuqtai nazari.

## 10.9 Ikki marta kelgan so'rov: idempotentlik

Belgi: tashqaridan keladigan yozuv operatsiyasida (to'lov, buyurtma, xabar iste'moli) takrorlanishga qarshi himoya yo'q. Oqibati: foydalanuvchi ikki marta bosganida ikki to'lov, retry dan keyin ikki buyurtma, Kafka qayta yetkazganida ikki yozuv.

```java
// Review javobi: kalit tashqaridan keladi, yagonalik bazada majburlanadi.
@PostMapping("/payments")
public ResponseEntity<PaymentResponse> pay(
        @RequestHeader("Idempotency-Key") @NotBlank String idemKey,
        @Valid @RequestBody PaymentRequest req) {
    return ResponseEntity.ok(payments.charge(idemKey, req));
}

@Transactional
public PaymentResponse charge(String idemKey, PaymentRequest req) {
    // 1) Avval kalitni band qilish: DB unique constraint - yagona ishonchli
    //    himoya (ikki instans, ikki thread, retry - hammasi uchun).
    try {
        idempotency.save(new IdempotencyRecord(idemKey, hash(req)));
        em.flush();                       // konfliktni shu yerda bilish uchun
    } catch (DataIntegrityViolationException dup) {
        // 2) Takroriy so'rov: oldingi natijani qaytaramiz, ikki marta
        //    to'lamaymiz. So'rov tanasi boshqacha bo'lsa - 409.
        IdempotencyRecord prev = idempotency.getByKey(idemKey);
        if (!prev.requestHash().equals(hash(req))) {
            throw new IdempotencyKeyReused(idemKey);
        }
        return prev.storedResponse();
    }
    PaymentResponse resp = gateway.charge(req);
    idempotency.storeResponse(idemKey, resp);
    return resp;
}
```

```sql
CREATE TABLE idempotency_record (
    key           text        PRIMARY KEY,          -- yagonalik kafolati
    request_hash  text        NOT NULL,
    response      jsonb,
    created_at    timestamptz NOT NULL DEFAULT now()
);
-- Oyna: eski kalitlar tozalanadi, aks holda jadval cheksiz o'sadi.
CREATE INDEX idempotency_created_idx ON idempotency_record (created_at);
```

Mexanizmning kitobdagi shakli xabar iste'moli uchun tasvirlangan va u yuqoridagi
koddagi bilan bir xil: ishlovchi agar bir xil xabar bilan bir necha marta
chaqirilishi xavfsiz bo'lsa idempotent hisoblanadi, va buni ta'minlashning
amaliy yo'li - ishlangan xabarlarning identifikatorlarini biznes mantiqi
ishlatadigan lokal ACID tranzaksiyaning o'zida alohida jadvalga yozib qo'yish,
keyin shu jadvalda bor identifikatorni dublikat deb tashlab yuborish
(Richardson, 6-bob, 196-bet). Yuqorida `idempotency_record` shu jadval, va
`Idempotency-Key` uning kaliti.

Review ning asosiy diqqati: kalit qayerda tekshiriladi. Agar `findByKey` keyin `save` qilinsa, bu poyga - ikki parallel so'rov ikkisi ham "topilmadi" deb o'tadi. Faqat unique constraint ishonchli.

Mavzuning to'liq yozuvi [idempotency](../patterns/07-api-dizayn-patternlari.md#79-idempotentlik-kaliti-idempotency-key) bo'limida; bu yerda faqat shu bo'limning nuqtai nazari.

## 10.10 Ko'p bosqichli jarayon: saga va kompensatsiya

Belgi: bitta metodda uch-to'rt tashqi tizim ketma-ket chaqiriladi. Oqibati: uchinchisi yiqilganda birinchi ikkisi bajarilgan holda qoladi, va tizim nomuvofiq holatda.

```java
// Belgi: to'rt qadam, qaytarish yo'q.
public void checkout(Cart cart) {
    inventory.reserve(cart);          // 1
    Payment p = payments.charge(cart);// 2  - bu yiqilsa, 1 qaytarilmaydi
    shipping.schedule(cart);          // 3  - bu yiqilsa, 1 va 2 qoladi
    notifications.send(cart);         // 4
}

// Review javobi: har qadamning kompensatsiyasi aniq, holat saqlanadi.
// Oddiy shakl: holat jadvalida qadamlarni belgilash va worker bilan davom
// ettirish (to'liq saga freymvorki kerak emas).
public enum CheckoutStep { RESERVED, PAID, SCHEDULED, NOTIFIED }

@Transactional
public void advance(CheckoutId id) {
    Checkout c = checkouts.lockById(id);          // SELECT ... FOR UPDATE
    switch (c.nextStep()) {
        case RESERVED  -> { inventory.reserve(c); c.mark(RESERVED); }
        case PAID      -> { payments.charge(c);   c.mark(PAID); }
        case SCHEDULED -> { shipping.schedule(c); c.mark(SCHEDULED); }
        case NOTIFIED  -> { notifications.send(c); c.complete(); }
    }
}
// Kompensatsiya: PAID dan keyin SCHEDULED uch marta yiqilsa,
// payments.refund(c) chaqiriladi va inventory.release(c) bajariladi.
```

Nom Richardson dan: saga - bir necha servisdagi ma'lumotni yangilashi kerak
bo'lgan har bir tizim buyrug'i uchun aniqlanadigan lokal tranzaksiyalar
ketma-ketligi; har lokal tranzaksiya bitta servis ichida oddiy ACID tranzaksiya
bilan bajariladi, va saga ACID tranzaksiyadan ikki jihatda farq qiladi: unda
izolyatsiya xususiyati yo'q, va har lokal tranzaksiya o'z o'zgarishini commit
qilgani uchun sagani qaytarish faqat kompensatsiya tranzaksiyalari bilan
mumkin (Richardson, 4-bob, 114-bet). Yuqoridagi `advance` shaklida qadamlar va
kompensatsiya aynan shu sababdan aniq yozilgan.

Review da saga uchun uch savol: har qadam idempotentmi (worker qayta urinadi), kompensatsiya ham yiqilishi mumkinmi (ikkinchi darajali himoya kerak), va jarayon qotib qolganini qanday bilamiz (eng muhim savol - metrika va alert, [39-bob](39-observability-review.md)).

## 10.11 Pattern taklif qilishning narxi

Pattern taklif qilgan reviewer uning narxini ham aytishi kerak. Har bir pattern kod hajmini oshiradi, navigatsiyani uzaytiradi va yangi odam uchun o'rganish yuki qo'shadi.

Bu talab kitoblardan keladi. GoF patternlarni qanday ishlatish bo'limini aynan
shu ogohlantirish bilan yopadi: patternlar tanlab ishlatilmasdan qo'llanmasligi
kerak, chunki ular moslashuvchanlikka ko'pincha qo'shimcha bilvosita qatlamlar
kiritib erishadi, bu dizaynni murakkablashtiradi va unumdorlikka tushadi;
pattern faqat bergan moslashuvchanlik haqiqatda kerak bo'lganda qo'llanadi (GoF,
1.8-bo'lim, 31-bet). Head First xuddi shu fikrni ogohlantirish shaklida beradi:
patternlarni ortiqcha ishlatish overengineered kodga olib keladi, shuning uchun
har doim ishni bajaradigan eng oddiy yechim tanlanadi va pattern faqat ehtiyoj
paydo bo'lganda kiritiladi (Freeman/Robson, 584-bet).

Narx nimadan iborat bo'lishini jadval ko'rsatadi. Aniq satr soni loyihaga qarab
o'zgaradi, shuning uchun bu yerda faqat qo'shiladigan qismlar sanaladi.

| Pattern | Narxi nimadan iborat | Qachon arzimaydi |
| --- | --- | --- |
| Strategy | 1 interfeys + har tur uchun 1 klass + registr | Ikki holat, o'zgarmaydi |
| Builder | Builder klassi yoki kutubxona + `build()` tekshiruvi | Record va bir necha majburiy parametr yetadi |
| Outbox | Jadval, worker, tozalash, monitoring | Xabar yo'qolishi muhim emas |
| Saga | Holat jadvali, worker, kompensatsiya | Bir tizimli tranzaksiya yetadi |
| CQRS | Ikki model, sinxronizatsiya | O'qish yuki kichik |
| Event sourcing | Event do'koni, proyeksiya, migratsiya | Tarix talab qilinmaydi |
| Adapter/port | 1 interfeys + 1 klass | Vendor almashtirilmaydi va test oson |

GoF ning o'zi bir misolda bu hisobni qanday qilishni ko'rsatadi: Factory Method
dizaynni moslashuvchan qiladi va boshqa patternlardan kam joy oladi, chunki yangi
klass emas, faqat yangi operatsiya talab qiladi; lekin yaratilayotgan sinf hech
qachon o'zgarmasa u shart emas (GoF, 136-bet).

Shu sababli review izohining to'g'ri shakli: "bu yerda Strategy kerak" emas, balki
"shu `switch` uchinchi joyda takrorlandi, yangi tur qo'shilganda uchtasini eslash
kerak; enum ichiga xulqni olsak, bitta joy qoladi". Birinchi shakl buyruq,
ikkinchisi muhandislik taklifi: u belgini, oqibatni va narxni birga qo'yadi.

## 10.12 Amalda qo'llash

- [ ] Loyihadagi barcha enum larni sanab, har biri bo'yicha nechta joyda `switch`/`if` borligini aniqlang; uchdan ko'p joy bo'lsa, xulqni enum ga yoki Strategy ga ko'chirishni rejalashtiring.
- [ ] `repository.save` va `kafka.send` (yoki tashqi HTTP) bir metodda uchraydigan joylarni grep bilan topib, har biri uchun outbox kerakligini baholang.
- [ ] Tashqaridan kelgan barcha yozuv endpointlarini sanab, ularning qanchasida idempotentlik kaliti borligini jadvalga yozing.
- [ ] Idempotentlik `findBy` + `save` orqali qilingan joylarni toping - ularni unique constraint ga o'tkazish majburiy.
- [ ] Qo'lda yozilgan retry sikllarini toping va ularni Resilience4j yoki Spring Retry ga o'tkazing; `retry-exceptions` ro'yxatida biznes xatolari yo'qligini tasdiqlang.
- [ ] `status` bo'yicha shoxlanishlarni toping va o'tish matritsasini enum ichida e'lon qiling.
- [ ] Domen va servis paketlarida `RestClient`, `WebClient`, SDK importlarini qidirib, ularni adapter ortiga ko'chirish ro'yxatini tuzing.
- [ ] Ko'p qadamli jarayonlarni (uchdan ko'p tashqi chaqiruv) aniqlab, har biri uchun "uchinchi qadam yiqilsa nima bo'ladi" savoliga yozma javob oling.

## Manbalar

- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns: Elements of Reusable Object-Oriented Software*, Addison-Wesley, 1995, 1.8-bo'lim (29-31-bet) - patternni qanday ishlatish tartibi va ogohlantirish: pattern tanlab ishlatilmasdan qo'llanmaydi, u qo'shimcha bilvosita qatlam kiritadi
- GoF, *Design Patterns*, 1995, 3-bob (87, 97, 100, 107, 127, 136-bet) - Abstract Factory, Builder, Factory Method va Singleton niyatlari; Builder ning oqibatlari; Factory Method qachon shart emasligi
- GoF, *Design Patterns*, 1995, 4-bob (139, 175, 207, 219-220-bet) - Adapter, Decorator va Proxy niyatlari; strukturaviy patternlar muhokamasida Adapter/Facade va Decorator/Proxy farqi
- GoF, *Design Patterns*, 1995, 5-bob (223, 226, 293, 305-307, 315, 318-bet) - Chain of Responsibility niyati va "qabul qilinishi kafolatlanmagan" oqibati; Observer, State va Strategy niyatlari; State da shart tarmoqlarining alohida sinflarga tushishi
- Martin Fowler, *Refactoring: Improving the Design of Existing Code*, 1-nashr, Addison-Wesley, 1999, 8-bob (181, 184, 238, 246-bet) - Replace Type Code with Subclasses va State/Strategy tanlash sharti; Introduce Parameter Object; Replace Constructor with Factory Method
- Martin Fowler, *Refactoring*, 1-nashr, 1999, 9-bob (205-206-bet) - Replace Conditional with Polymorphism va uning sababi: bir xil shartlar to'plami ko'p joyda takrorlanganda eng katta foyda
- Martin Fowler, *Refactoring*, 2-nashr, Addison-Wesley, 2019, refaktoringlar ro'yxati (140, 272, 334, 362-bet) - shu refaktoringlarning ikkinchi nashrdagi nomlari va o'rni: Introduce Parameter Object, Replace Conditional with Polymorphism, Replace Constructor with Factory Function, Replace Type Code with Subclasses
- Eric Freeman, Elisabeth Robson, *Head First Design Patterns*, 2-nashr, O'Reilly, 2021, 10-bob (381, 414-415-bet) - Strategy va State strukturasi o'xshash, niyati butunlay boshqa; klient strategiyani beradi, Context esa o'z holatini o'zi almashtiradi
- Freeman/Robson, *Head First Design Patterns*, 2-nashr, 2021, 13-bob (584-bet) - patternni ortiqcha ishlatish overengineered kodga olib keladi; eng oddiy yechim tanlanadi va pattern ehtiyoj paydo bo'lganda kiritiladi
- Chris Richardson, *Microservices Patterns*, Manning, 2019, 3-bob (98-bet) - Transactional outbox: xabar baza tranzaksiyasining bir qismi sifatida OUTBOX jadvaliga yoziladi
- Chris Richardson, *Microservices Patterns*, 2019, 4-bob (114-bet) - Saga: lokal tranzaksiyalar ketma-ketligi, izolyatsiya yo'q, qaytarish faqat kompensatsiya bilan
- Chris Richardson, *Microservices Patterns*, 2019, 6-bob (196-bet) - idempotent ishlovchi: ishlangan xabar identifikatori bir xil lokal tranzaksiyada jadvalga yoziladi va dublikat tashlanadi
- ESLATMA: 10.5 dagi Resilience4j va Micrometer annotatsiyalari, 10.6 dagi `EnumSet` o'tish jadvali, 10.9 dagi `Idempotency-Key` HTTP sarlavhasi va 10.12 dagi checklist shu korpusning amaliy tavsiyasi, yuqoridagi kitoblardan olingan emas
- ESLATMA: 10.8, 10.9 va 10.10 ning to'liq yozuvi patterns hujjatida (outbox 10.14, idempotentlik 7.9, saga 14.9); bu bobda faqat diffdan ko'rish nuqtai nazari

---

[&larr; 9. SOLID va dizayn printsiplarini diffda tekshirish](09-solid-va-dizayn-printsiplarini-diffda.md) · [Mundarija](README.md) · [11. Dizayn pattern review II: noto'g'ri va ortiqcha qo'llangan pattern &rarr;](11-dizayn-pattern-review-ii-notogri-va.md)
