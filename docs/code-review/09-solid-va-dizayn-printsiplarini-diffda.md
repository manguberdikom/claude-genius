<!-- doc: code-review | chapter: 9 | part: II. Arxitektura, dizayn va clean code review -->

[Kod review](../../README.md) / [Kod review](README.md)

# 9. SOLID va dizayn printsiplarini diffda tekshirish (Principles, Not Slogans)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

- [9.1 SRP: o'zgarish sabablarini sanash](#91-srp-ozgarish-sabablarini-sanash)
- [9.2 OCP: yangi holat qo'shilganda nima o'zgaradi](#92-ocp-yangi-holat-qoshilganda-nima-ozgaradi)
- [9.3 LSP: shartnomani buzgan implementatsiya](#93-lsp-shartnomani-buzgan-implementatsiya)
- [9.4 ISP: semiz interfeys va majburiy bo'sh metodlar](#94-isp-semiz-interfeys-va-majburiy-bosh-metodlar)
- [9.5 DIP: interfeys kimga tegishli](#95-dip-interfeys-kimga-tegishli)
- [9.6 Demeter qonuni: zanjirli chaqiruv](#96-demeter-qonuni-zanjirli-chaqiruv)
- [9.7 Tell, don't ask va anemik model](#97-tell-dont-ask-va-anemik-model)
- [9.8 Kompozitsiya va meros](#98-kompozitsiya-va-meros)
- [9.9 Command-query separation: so'rov yon ta'sir qiladimi](#99-command-query-separation-sorov-yon-tasir-qiladimi)
- [9.10 Printsipni qurol sifatida ishlatmaslik](#910-printsipni-qurol-sifatida-ishlatmaslik)
- [9.11 Amalda qo'llash](#911-amalda-qollash)

</details>


SOLID review da ikki xil ishlatiladi. Birinchi usul - shior sifatida: "bu SRP ni buzadi". Bu izoh hech narsa bermaydi, chunki muallif nimani o'zgartirishni bilmaydi. Ikkinchi usul - diagnostika sifatida: har bir printsipning diffda ko'rinadigan aniq belgisi bor, va shu belgini ko'rsatish mumkin. Bu bob har bir printsip uchun belgini, oqibatni va review javobini beradi.

## 9.1 SRP: o'zgarish sabablarini sanash

Single responsibility "klass bitta ish qiladi" degani emas. U "klass bitta sababga ko'ra o'zgaradi" degani. Shu sababli SRP ni tekshirish usuli - o'zgarish sabablarini sanash, metodlarni sanash emas.

Amaliy savol: shu klassni o'zgartirishni kim so'raydi. Agar javobda ikki xil manfaatdor bo'lsa (buxgalteriya soliq qoidasini o'zgartiradi, marketing xabar matnini o'zgartiradi), klass bo'linishi kerak.

```java
// Ikki egasi bor klass: soliq qoidasi va hujjat shakli bir joyda.
@Service
public class InvoiceService {
    public Invoice create(Order order) {
        BigDecimal vat = order.total().multiply(new BigDecimal("0.12"));  // buxgalteriya
        Invoice inv = new Invoice(order.id(), order.total(), vat);
        String html = "<h1>Invoys #" + inv.number() + "</h1>"             // dizayn
                    + "<p>Jami: " + inv.total() + " so'm</p>";
        inv.setRenderedHtml(html);
        return inv;
    }
}
// Review izohi: soliq foizi o'zgarsa va hujjat shakli o'zgarsa - bitta
// faylga ikki xil jamoa tegadi. Shu fayl har ikki talabda konflikt beradi
// va har o'zgarishda ikki xil testni ishga tushirish kerak bo'ladi.
// Ajratish: VatCalculator (qoida) va InvoiceRenderer (shakl).
```

## 9.2 OCP: yangi holat qo'shilganda nima o'zgaradi

Open-closed ni tekshirishning aniq usuli bor: "ertaga yangi to'lov usuli (yoki yangi hujjat turi, yangi status) qo'shilsa, nechta faylga tegiladi" degan savol. Javob bitta fayl bo'lsa - yopiq. Besh fayl bo'lsa - har qo'shilishda beshta joyni esdan chiqarmaslik kerak.

```java
// Yopilmagan dizayn: yangi turi qo'shilsa, uch joy o'zgaradi.
switch (payment.type()) {
    case CARD -> cardFee(payment);
    case WALLET -> walletFee(payment);
}                                                  // 1-joy: komissiya
switch (payment.type()) { ... }                    // 2-joy: tekshiruv
switch (payment.type()) { ... }                    // 3-joy: hisobot

// Yopiq dizayn: yangi tur bitta klass qo'shish bilan keladi.
public interface PaymentMethod {
    PaymentType type();
    Money fee(Money amount);
    void validate(PaymentRequest request);
}
// Spring hamma implementatsiyani o'zi yig'adi.
@Service
public class PaymentMethods {
    private final Map<PaymentType, PaymentMethod> byType;

    public PaymentMethods(List<PaymentMethod> all) {       // konstruktorga ro'yxat
        this.byType = all.stream()
            .collect(toMap(PaymentMethod::type, identity()));
    }
    public PaymentMethod of(PaymentType type) {
        PaymentMethod m = byType.get(type);
        if (m == null) throw new UnsupportedPaymentType(type);
        return m;
    }
}
```

Diqqat: OCP ni oldindan qo'llash erta abstraksiyaga olib keladi. Mezon - haqiqatda yangi turlar qo'shilayotganini tarixda ko'rish. Agar tarixda ikki yil ichida uchta yangi to'lov usuli qo'shilgan bo'lsa, abstraksiya o'zini oqlaydi. Agar hech qachon qo'shilmagan bo'lsa, `switch` yetadi.

```bash
# Tarixdan OCP ni asoslash: shu enum ga qancha marta yangi qiymat qo'shilgan.
git log -p --follow -- '**/PaymentType.java' | grep -cE '^\+\s+[A-Z_]+,'
# Agar bu son yuqori bo'lsa, polimorfizm qo'shish dalil bilan asoslanadi.
```

## 9.3 LSP: shartnomani buzgan implementatsiya

Liskov buzilishi Java da ikki shaklda ko'rinadi: implementatsiya kutilmagan istisno tashlaydi, yoki kutilgan narsani qilmaydi (jim o'tkazib yuboradi).

```java
// Buzilish 1: implementatsiya shartnomani bajarmaydi.
public interface NotificationChannel {
    void send(Message message);        // shartnoma: xabarni yetkazadi
}
class NoopChannel implements NotificationChannel {
    @Override public void send(Message m) { }     // jim hech narsa qilmaydi
}
// Review izohi: bu implementatsiya chaqiruvchini aldaydi. Agar u test
// uchun kerak bo'lsa, test paketida bo'lishi kerak. Agar prodda
// "o'chirilgan kanal" ma'nosida bo'lsa, buni tur bilan ko'rsatish kerak:
// Optional<NotificationChannel> yoki isEnabled().

// Buzilish 2: shartnomada yo'q istisno.
class SmsChannel implements NotificationChannel {
    @Override public void send(Message m) {
        if (m.body().length() > 160) {
            throw new IllegalArgumentException("juda uzun");   // yangi shart
        }
    }
}
// Review izohi: chaqiruvchi kanal turini bilmaydi, lekin endi uzunlik
// cheklovini bilishi kerak. Shartnomaga `MessageTooLong` ni qo'shish yoki
// kanal imkoniyatlarini e'lon qilish kerak (maxLength()).
```

Spring kontekstida LSP buzilishining tipik joyi - `@Override` qilingan metod `super` ni chaqirmasligi, va `@Transactional` metodni vorisda qayta e'lon qilish (proxy xulqi o'zgaradi, [18-bob](18-bean-kontekst-va-proxy-mexanikasi-review.md)).

## 9.4 ISP: semiz interfeys va majburiy bo'sh metodlar

Interface segregation buzilishining belgisi aniq: implementatsiyada bo'sh metodlar yoki `UnsupportedOperationException` paydo bo'ladi.

```java
// Semiz interfeys: hamma implementatsiya hammasini qila olmaydi.
public interface FileStorage {
    void upload(String key, byte[] data);
    byte[] download(String key);
    void delete(String key);
    String presignedUrl(String key, Duration ttl);   // faqat S3 da bor
    void setAcl(String key, Acl acl);                // faqat S3 da bor
}
class LocalDiskStorage implements FileStorage {
    @Override public String presignedUrl(String k, Duration t) {
        throw new UnsupportedOperationException();   // ISP buzilishi belgisi
    }
}

// Ajratilgan interfeyslar: chaqiruvchi faqat kerakligiga bog'lanadi.
public interface FileStorage {
    void upload(String key, byte[] data);
    byte[] download(String key);
    void delete(String key);
}
public interface PresignedUrls {                     // qo'shimcha imkoniyat
    String presignedUrl(String key, Duration ttl);
}
// Review foydasi: lokal disk bilan ishlaydigan test muhitida presigned URL
// chaqiradigan kod kompilyatsiya paytida ko'rinadi.
```

## 9.5 DIP: interfeys kimga tegishli

Dependency inversion ko'pincha "interfeys ishlatish" deb tushuniladi, lekin uning mohiyati boshqa: interfeys foydalanuvchi tomonda e'lon qilinadi va implementatsiya unga moslashadi. Agar interfeys implementatsiya bilan bir paketda turgan bo'lsa va uning metodlari implementatsiya detallarini aks ettirsa, inversiya bo'lmagan.

| Belgi | Inversiya bormi |
| --- | --- |
| Interfeys domen paketida, implementatsiya infra da | Ha |
| Interfeys metodlari domen tilida (`shipped`, `authorize`) | Ha |
| Interfeys infra paketida, yonida `XxxImpl` | Yo'q |
| Interfeys metodlari vendor atamalarida (`callStripeApi`) | Yo'q |
| Domen `@Repository` annotatsiyasini biladi | Yo'q |

## 9.6 Demeter qonuni: zanjirli chaqiruv

`a.getB().getC().getD()` zanjiri ikki narsani bildiradi: chaqiruvchi uch darajali tuzilishni biladi, va o'rtadagi har qanday o'zgarish uni sindiradi. Bundan tashqari har bir `get` da null xavfi bor.

```java
// Zanjir: uch obyekt tuzilishiga bog'liqlik + uch null xavfi.
String city = order.getCustomer().getAddress().getCity().toUpperCase();

// Review javobi: so'rashni obyektning o'ziga topshirish.
String city = order.deliveryCity();     // Order o'z ichidagini biladi

// Order ichida:
public String deliveryCity() {
    return customer.address().city();    // bitta daraja, null konstruktorda yo'q
}
```

Istisno: fluent API va builder zanjirlari (`Stream`, `WebClient`, `builder()`) Demeter qonuniga kirmaydi, chunki ular har qadamda bir xil turni qaytaradi va tuzilish haqida bilim talab qilmaydi.

## 9.7 Tell, don't ask va anemik model

Anemik model - ma'lumot bir joyda (entity), qoidalar boshqa joyda (service) bo'lgan holat. Bu Spring loyihalarida eng keng tarqalgan dizayn. U har doim xato emas, lekin uning narxi bor: invariant hech kim tomonidan himoya qilinmaydi, chunki setterlar hammaga ochiq.

```java
// Anemik: har kim har qanday holatga o'tkaza oladi.
order.setStatus(SHIPPED);
order.setShippedAt(now());
// Qoida (faqat PAID dan SHIPPED ga o'tish mumkin) servisda, va u uch
// joyda takrorlanadi yoki bir joyda esdan chiqadi.

// Boy model: o'tish qoidasi obyekt ichida, noto'g'ri holat yaratilmaydi.
public class Order {
    private OrderStatus status;
    private Instant shippedAt;

    public void markShipped(Instant when, TrackingNumber tracking) {
        if (status != PAID) {
            throw new IllegalStateTransition(status, SHIPPED);
        }
        this.status = SHIPPED;
        this.shippedAt = when;
        this.tracking = tracking;
        registerEvent(new OrderShipped(id, tracking));   // domen eventi
    }
    // setStatus yo'q: tashqaridan holatni buzib bo'lmaydi.
}
```

Review mezoni: diffda `setX` ketma-ketligi ko'rinsa va ular birgalikda biznes holatini o'zgartirsa, bu operatsiya domen metodi bo'lishi kerak. Agar obyekt faqat ma'lumot tashuvchi bo'lsa (DTO, projection), setterlar normal.

## 9.8 Kompozitsiya va meros

Diffda yangi `extends` paydo bo'lsa, review savoli: bu "turi" munosabatimi yoki shunchaki kodni qayta ishlatishmi. Ikkinchi holda kompozitsiya to'g'ri.

```java
// Meros kodni qayta ishlatish uchun ishlatilgan: mo'rt bog'liqlik.
public class CachedOrderRepository extends JpaOrderRepositoryImpl {
    @Override public Optional<Order> findById(long id) {
        return cache.get(id, () -> super.findById(id));
    }
    // Muammo: boshqa findBy metodlar keshlanmaydi, va ota klassga yangi
    // metod qo'shilsa, u ham keshsiz o'tadi - jim nomuvofiqlik.
}

// Kompozitsiya: shartnoma aniq, qamrov to'liq ko'rinadi.
public class CachedOrderRepository implements OrderRepository {
    private final OrderRepository delegate;
    private final Cache cache;
    // Har metod ongli yoziladi: nima keshlanadi, nima o'tkaziladi.
}
```

Spring da bu masalaning yana bir tomoni bor: `@Transactional` yoki `@Cacheable` bo'lgan klassni meros qilish proxy xulqini o'zgartiradi va `super` chaqiruvi proxy orqali o'tmaydi. Shu sababli AOP ishtirok etadigan joyda meros qo'shimcha xavf keltiradi ([18-bob](18-bean-kontekst-va-proxy-mexanikasi-review.md)).

## 9.9 Command-query separation: so'rov yon ta'sir qiladimi

Nomi so'rovga o'xshagan metod holatni o'zgartirsa, bu eng jim xato manbalaridan biri: chaqiruvchi uni xavfsiz deb o'ylaydi va kerakli joyda ikki marta chaqiradi.

```java
// Yolg'on so'rov: getter yozadi.
public Token getToken() {
    if (token == null || token.isExpired()) {
        token = authClient.fetchNewToken();     // tashqi chaqiruv va holat o'zgarishi
    }
    return token;
}
// Review izohi: `getToken()` nomi bepul o'qishni bildiradi, lekin bu metod
// tarmoqqa chiqadi va umumiy holatni o'zgartiradi. Ikki thread bir vaqtda
// chaqirsa - ikki marta token olinadi. Nomi `currentToken()` yoki
// `refreshIfNeeded()` bo'lishi, va sinxronizatsiya qo'shilishi kerak.

// Aniq shakl: niyat nomda, poyga himoyalangan.
private final AtomicReference<Token> cached = new AtomicReference<>();

public Token currentToken() {
    Token t = cached.get();
    if (t != null && !t.isExpired()) return t;
    synchronized (this) {
        t = cached.get();
        if (t != null && !t.isExpired()) return t;
        Token fresh = authClient.fetchNewToken();
        cached.set(fresh);
        return fresh;
    }
}
```

## 9.10 Printsipni qurol sifatida ishlatmaslik

Printsip nomi bilan yozilgan izoh muallifni himoyasiz qoldiradi: u printsip nomini bilmasa, bahslashish imkoni yo'q. Bu review ni muhandislikdan ierarxiyaga aylantiradi.

Shu sababli qoida: printsip nomi izohda bo'lishi mumkin, lekin yolg'iz bo'lmasligi kerak. Har doim belgi, oqibat va o'zgarish hajmi bilan birga keladi.

```text
# Yomon: shior.
"SRP buzilgan, bo'lish kerak."

# Yaxshi: belgi -> oqibat -> taklif -> hajm.
suggest: InvoiceService ichida soliq hisobi va HTML shakli bir joyda.

Belgi: create() metodi ikki xil sababga ko'ra o'zgaradi - soliq foizi
(buxgalteriya) va hujjat ko'rinishi (dizayn).

Oqibati: shu fayl oxirgi 6 oyda 14 marta o'zgargan, 9 tasi shablon
uchun, 5 tasi soliq uchun. Konfliktlar shu faylda eng ko'p.

Taklif: VatCalculator va InvoiceRenderer ga ajratish. Hajmi: ikki klass,
taxminan 60 satr ko'chirish, mavjud testlar o'zgarmaydi.
```

## 9.11 Amalda qo'llash

- [ ] SRP uchun "o'zgarish sabablarini sanash" savolini checklistga qo'shing va eng ko'p o'zgargan 10 faylni `git log` bilan aniqlab, ularning sabablarini guruhlang.
- [ ] Loyihadagi barcha `switch`/`if` zinapoyalarini enum turi bo'yicha toping va ularning qanchasi uch joydan ko'proq takrorlanganini aniqlang.
- [ ] Enum larga tarixda qancha yangi qiymat qo'shilganini o'lchab, polimorfizm qo'shish kerak bo'lgan joylarni dalil bilan belgilang.
- [ ] `UnsupportedOperationException` tashlaydigan implementatsiyalarni toping - har biri ISP buzilishining belgisi.
- [ ] Domen paketidagi interfeyslarning metodlari domen tilida nomlanganini tekshiring, vendor atamalarini toping.
- [ ] Uch va undan ko'p bo'g'inli `get` zanjirlarini grep bilan topib, ularni obyekt metodiga ko'chirish ro'yxatini tuzing.
- [ ] Entity larda ketma-ket chaqiriladigan `setX` guruhlarini aniqlab, ularni domen metodlariga aylantirishni rejalashtiring.
- [ ] Nomi `get`/`is` bilan boshlanadigan, lekin holat o'zgartiradigan yoki tarmoqqa chiqadigan metodlarni toping va nomini tuzating.

---

[&larr; 8. Clean code review: nomlash, kognitiv yuk, metod shakli](08-clean-code-review-nomlash-kognitiv-yuk.md) · [Mundarija](README.md) · [10. Dizayn pattern review I: yo'q patternni ko'rish &rarr;](10-dizayn-pattern-review-i-yoq-patternni-korish.md)
