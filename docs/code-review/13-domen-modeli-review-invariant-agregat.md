<!-- doc: code-review | chapter: 13 | part: II. Arxitektura, dizayn va clean code review -->

[Barcha hujjatlar](../../README.md) / [Kod review](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 13. Domen modeli review: invariant, agregat, chegara (Reviewing the Domain Model)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

- [13.1 Modelning asosiy savoli: invariant kim tomonidan himoyalangan](#131-modelning-asosiy-savoli-invariant-kim-tomonidan-himoyalangan)
- [13.2 Anemik modelni ongli tanlash](#132-anemik-modelni-ongli-tanlash)
- [13.3 Agregat chegarasi: nima birga saqlanadi](#133-agregat-chegarasi-nima-birga-saqlanadi)
- [13.4 Value object va entity farqi diffda](#134-value-object-va-entity-farqi-diffda)
- [13.5 Identifikator dizayni](#135-identifikator-dizayni)
- [13.6 Domen eventlari: nima e'lon qilinadi](#136-domen-eventlari-nima-elon-qilinadi)
- [13.7 Domen tili: kod va suhbat bir xil so'z bilan](#137-domen-tili-kod-va-suhbat-bir-xil-soz-bilan)
- [13.8 Domen servisi qachon kerak](#138-domen-servisi-qachon-kerak)
- [13.9 ORM domen modelini buzganda](#139-orm-domen-modelini-buzganda)
- [13.10 Modelga tegadigan PR uchun qo'shimcha talablar](#1310-modelga-tegadigan-pr-uchun-qoshimcha-talablar)
- [13.11 Amalda qo'llash](#1311-amalda-qollash)

</details>


Domen modeli - tizimning eng uzoq yashaydigan qismi. Controller qayta yoziladi, ORM almashtiriladi, lekin "buyurtma nima" degan savolning javobi yillar davomida qoladi. Shu sababli domen modeliga tegadigan PR boshqa PR lardan chuqurroq o'qiladi: bu yerdagi xato keyinchalik yuzta joyda ko'rinadi. DDD atamalarining ta'rifi [Dizayn patternlar](../patterns/README.md) va [Arxitektor miyasi](../architect/README.md) da: entity [patterns 13.13](../patterns/13-domain-driven-design-patternlari.md#1313-entity-entity), value object [patterns 13.14](../patterns/13-domain-driven-design-patternlari.md#1314-qiymat-obyekti-value-object), agregat [patterns 13.15](../patterns/13-domain-driven-design-patternlari.md#1315-agregat-va-agregat-ildizi-aggregate--aggregate-root), invariant [patterns 13.24](../patterns/13-domain-driven-design-patternlari.md#1324-invariantlar-invariants). Bu yerda pattern qaytadan tushuntirilmaydi, faqat review savollari.

## 13.1 Modelning asosiy savoli: invariant kim tomonidan himoyalangan

Domen modelini review qilish bitta savoldan boshlanadi: bu obyektni noto'g'ri holatda yaratish yoki noto'g'ri holatga o'tkazish mumkinmi. Agar mumkin bo'lsa, qayerda bo'lsa ham bir kun shunday bo'ladi.

```java
// Himoyasiz model: har qanday holat yaratilishi mumkin.
@Entity
public class Subscription {
    @Id @GeneratedValue private Long id;
    private LocalDate startsAt;
    private LocalDate endsAt;
    private BigDecimal monthlyPrice;
    private SubscriptionStatus status;
    // setterlar hammasi public, no-arg konstruktor public
}
// Shu model bilan quyidagilar hammasi mumkin:
//  - endsAt < startsAt (manfiy davr)
//  - monthlyPrice manfiy
//  - status = ACTIVE, lekin endsAt o'tgan
//  - startsAt null

// Himoyalangan model: noto'g'ri holat tuzilmaydi.
@Entity
public class Subscription {
    @Id @GeneratedValue private Long id;
    @Embedded private DateRange period;         // o'z invariantini saqlaydi
    @Embedded private Money monthlyPrice;       // valyuta va manfiylik tekshirilgan
    @Enumerated(STRING) private SubscriptionStatus status;

    protected Subscription() { }                // JPA uchun, protected

    public Subscription(DateRange period, Money monthlyPrice) {
        this.period = Objects.requireNonNull(period);
        this.monthlyPrice = monthlyPrice.requirePositive();
        this.status = PENDING;
    }

    public void activate(LocalDate on) {
        if (status != PENDING) throw new IllegalStateTransition(status, ACTIVE);
        if (!period.contains(on)) throw new OutsideSubscriptionPeriod(on, period);
        this.status = ACTIVE;
    }
}

public record DateRange(LocalDate from, LocalDate to) {
    public DateRange {
        if (from == null || to == null) throw new IllegalArgumentException("sana null");
        if (to.isBefore(from)) throw new IllegalArgumentException("to < from");
    }
    public boolean contains(LocalDate d) {
        return !d.isBefore(from) && !d.isAfter(to);
    }
}
```

Review savollari ketma-ketligi: konstruktor to'liq holat talab qiladimi, setterlar qanchasi `public`, va holat o'tishlari metod orqali o'tadimi.

Birinchi savolning mezoni kitobda aniq: Evans public konstruktor fabrika bilan bir xil qoidaga bo'ysunadi deydi - u atomar amal bo'lishi va yaratilgan obyektning BARCHA invariantlarini qanoatlantirishi shart; interfeys noto'g'ri obyekt so'rashga yo'l qo'ysa, istisno otilishi kerak, nosoz qiymat qaytmasligi kerak (*Domain-Driven Design*, 6-bob, 100 va 102-bet). Ikkinchi mezon agregat ildizi bilan bog'liq: ildiz entity invariantlarni tekshirish uchun oxirgi javobgar, va agregat ichidagi har qanday o'zgarish commit bo'lganda butun agregatning invariantlari bajarilgan bo'lishi shart (shu kitob, 92-bet). Shu sababli review da "kim himoyalaydi" savoli konkret: javob konstruktor va ildiz metodlari bo'lishi kerak, chaqiruvchi emas.

## 13.2 Anemik modelni ongli tanlash

Xulqsiz (anemik) model har doim xato emas: xato - tanlovning ongsizligi.

Avval atribut haqida. "Anemic Domain Model" atamasi Fowler ning alohida yozuvidan keladi, *Patterns of Enterprise Application Architecture* kitobida bu so'z umuman uchramaydi; shu sababli review izohida uni kitobga yoki Evans ga tiqishtirish xato. Kitobda boshqa narsa bor - tanlov mezoni. Fowler uchta uslubni (Transaction Script, Table Module, Domain Model) solishtirib, tanlov faqat domen mantiqining murakkabligiga bog'liq deydi: oddiy "null emas" tekshiruvlari va bir-ikki yig'indi bo'lsa Transaction Script yaxshiroq, o'zgarib turadigan murakkab validatsiya, hisob va keltirib chiqarish qoidalari bo'lsa obyekt modeli kerak (*PoEAA*, 9-bob, 119-bet). Eng muhimi, u o'lchov berishdan ochiq bosh tortadi: domen mantiqining murakkabligini hech kim o'lchashni bilmaydi, shuning uchun amalda tajribali odamlar talabni ko'rib qarorni o'zlari qabul qiladi (shu kitob, 2-bob, 30-bet). Richardson ham shu tanlovni takrorlaydi: protsedurali Transaction Script oddiy mantiq uchun yaxshi ishlaydi, murakkab mantiq uchun esa Domain model kerak, chunki transaction script lar monolit kabi to'xtovsiz o'sadi (*Microservices Patterns*, 5-bob, 149-150-bet).

Review uchun amaliy oqibati: diffda "setter bor" o'zi xato emas, xato - modulning mantiq murakkabligi bilan tanlangan uslub mos emasligi. Shu sababli izoh "anemik model anti-pattern" deb emas, "bu modulda qoida necha joyda va kim tekshiradi" deb yoziladi.

Xavfli belgi: bitta modulda ikki yondashuv aralashgan - qoidalarning yarmi entity da, yarmi servisda. Shu holatda invariantni hech kim to'liq himoya qilmaydi (13.1 dagi "kim himoyalaydi" savoli). Anemik modelning anti-pattern sifatidagi yozuvi [patterns 13.31](../patterns/13-domain-driven-design-patternlari.md#1331-anemik-domen-modeli-anti-anemic-domain-model-anti) da.

## 13.3 Agregat chegarasi: nima birga saqlanadi

Chegara review da ikki savol bilan tekshiriladi: qaysi invariant tranzaksiya ichida kafolatlanishi kerak, va agregat qanchalik kichik bo'la oladi.

Kitobdagi mezon aniq. Evans da agregat ichidagi invariantlar har tranzaksiya tugashida bajariladi, agregatlar orasidagi qoida esa har doim yangi bo'lishi kutilmaydi - u event yoki batch bilan kelishilgan muddat ichida yopiladi (*Domain-Driven Design*, 6-bob, 91-bet). Khononov buni bir gapda beradi: agregat chegarasiga faqat biznes mantiqi uchun qat'iy izchil bo'lishi SHART bo'lgan ma'lumot kiradi, yakuniy izchillik yetarli bo'lgan hamma narsa tashqarida qoladi, va qoida - agregatni iloji boricha kichik tutish (*Learning Domain-Driven Design*, 6-bob, 89-bet). Richardson xuddi shu xulosaga boshqa tomondan keladi: katta agregat atomar yangilashni osonlashtiradi, lekin bir mijozning turli buyurtmalarini yangilash tranzaksiyalari ketma-ket turib qoladi, shuning uchun imkon qadar mayda agregat yaxshiroq (*Microservices Patterns*, 5-bob, 158-bet).

```java
// Juda katta agregat: kolleksiyaga chegara yo'q.
@Entity
public class Customer {
    @OneToMany(mappedBy = "customer", cascade = ALL, fetch = EAGER)
    private List<Order> orders = new ArrayList<>();      // yillar davomida o'sadi
}
// Review izohlari: (1) EAGER - mijozni yuklash barcha buyurtmalarni
// tortadi; (2) cascade ALL - mijozni o'chirish barcha buyurtmalarni
// o'chiradi: Evans da o'chirish amali agregat chegarasidagi hamma narsani
// birdan olib tashlaydi, demak savol - Order Customer chegarasi ichidami;
// (3) yangi buyurtma qo'shish uchun butun kolleksiya yuklanadi.
// Yechim: Order alohida agregat, Customer faqat CustomerId bilan bog'lanadi -
// Richardson ning 2-qoidasi: agregatlar orasidagi havola obyekt havolasi
// emas, birlamchi kalit (ID) orqali bo'ladi.

// To'g'ri chegara: agregatlar ID orqali bog'lanadi.
@Entity
public class Order {
    @Id @GeneratedValue private Long id;
    @Embedded private CustomerId customerId;        // boshqa agregatga havola
    @ElementCollection                              // buyurtma qatorlari esa ichida
    private List<OrderLine> lines = new ArrayList<>();
}
```

Chegara mezoni: invariant tranzaksiya ichida kafolatlanishi kerakmi. "Buyurtma summasi qatorlar summasiga teng" - ha, demak qatorlar agregat ichida. "Mijozning umumiy xarid limiti oshmaydi" - bu boshqa agregatga tegadi, uni tranzaksiya emas, jarayon bilan ta'minlash kerak (yoki ongli ravishda eventual consistency qabul qilinadi).

Uchinchi review savoli - bitta tranzaksiyada nechta agregat o'zgaradi. Richardson ning 3-qoidasi: bitta tranzaksiya faqat bitta agregatni yaratadi yoki yangilaydi; ko'p agregatni o'zgartirish kerak bo'lsa, buning uchun saga bor, uning har qadami aniq bitta agregatni o'zgartiradi (*Microservices Patterns*, 5-bob, 157-bet). Bir servis ichida RDBMS bilan ishlayotganda bu qoidadan ongli chekinish mumkin, lekin diffda bu chekinish ko'rinib turishi kerak (shu bet). Shuningdek Evans da agregat ichidagi obyektni to'g'ridan-to'g'ri so'rov bilan olish taqiqlangan: bazadan faqat agregat ildizi so'raladi, qolganlariga ildizdan o'tib boriladi (*Domain-Driven Design*, 6-bob, 92-bet). Review da bu konkret belgi beradi - ichki entity uchun alohida repository paydo bo'lgan diff chegarani buzadi.

## 13.4 Value object va entity farqi diffda

Farqning kitobdagi ta'rifi qisqa: entity atributlari bilan emas, vaqt bo'yicha davom etadigan ayniyat (identity) bilan aniqlanadi, value object esa faqat o'zi nima ekani bilan - kim ekani bilan emas (Evans, *Domain-Driven Design*, 5-bob, 65 va 71-bet). Evans ning tavsiyasi ham qat'iy: elementda faqat atributlari muhim bo'lsa, uni value object deb belgilang, O'ZGARMAS tutingiz va unga ayniyat BERMANG (shu kitob, 71-bet). Sababi texnik: obyekt xavfsiz ulashilishi uchun o'zgarmas bo'lishi shart, aks holda bir egadagi o'zgarish ikkinchi egasining invariantini buzadi (shu kitob, 72-bet). Shu sababli review da aralashtirish belgisi bitta: value object da `id` paydo bo'lishi yoki setter qo'shilishi.

Java tomonidan o'zgarmaslikning tekshiruv punktlari Bloch da beshta qoida bilan berilgan: holatni o'zgartiradigan metod bo'lmasin, sinf meros olinmaydigan bo'lsin, barcha maydon `final`, barcha maydon `private`, va mutable komponentga tashqaridan havola chiqmasin (konstruktor va getter da himoya nusxasi) - *Effective Java* 3-nashr, Item 17, 80-bet. Diffda value object ni shu beshlik bo'yicha o'qish eng arzon yo'l.

Khononov value object ning review uchun muhim foydasini qo'shadi: validatsiya mantig'i value object ichida turgani uchun u takrorlanmaydi va uni chaqirishni unutib bo'lmaydi, primitive obsession esa shu bilan yopiladi (*Learning Domain-Driven Design*, 6-bob, 78-80-bet); tenglik qiymat bo'yicha bo'lgani uchun `equals` va `hashCode` ni to'g'ri yozish majburiy (shu kitob, 81-bet).

```java
// Value object: immutable, equals qiymat bo'yicha, validatsiya ichida.
public record Money(BigDecimal amount, Currency currency) implements Comparable<Money> {
    public Money {
        Objects.requireNonNull(amount); Objects.requireNonNull(currency);
        // Scale ni normalizatsiya qilish: 10.00 va 10.0 teng bo'lishi uchun.
        amount = amount.setScale(currency.getDefaultFractionDigits(), HALF_UP);
    }
    public Money plus(Money other) { requireSameCurrency(other);
        return new Money(amount.add(other.amount), currency); }
    public Money times(int n) { return new Money(amount.multiply(valueOf(n)), currency); }
    @Override public int compareTo(Money o) { requireSameCurrency(o);
        return amount.compareTo(o.amount); }
}
// Review diqqati: record da `equals` avtomatik, lekin BigDecimal ning
// `compareTo` si `equals` bilan izchil emas. Bloch ning misoli: bo'sh
// HashSet ga new BigDecimal("1.0") va new BigDecimal("1.00") qo'shilsa,
// to'plamda IKKI element qoladi (equals teng emas deydi), xuddi shu amal
// TreeSet da bitta element beradi (compareTo teng deydi) - Effective Java
// 3-nashr, Item 14, 68-69-bet. Shu sababli konstruktorda setScale
// qilinmasa, teng summalar HashSet va Map kaliti sifatida jim ikkiga
// bo'linadi.
```

Entitet va value object tengligining to'liq yozuvi [clean-code 15.5](../clean-code/15-tenglik-hash-va-obyekt-shartnomalari.md#155-entitet-va-value-object-tengligi-farqi) da; bu yerda faqat diffda ko'rinadigan belgi.

## 13.5 Identifikator dizayni

ID turini tanlash qaytarib bo'lmaydigan qarorlar qatoriga kiradi: u API ga, indekslarga va tashqi tizimlarga tarqaydi.

Kitob bu yerda texnologiya tanlamaydi, lekin uchta qat'iy talab beradi. Evans da: ID atributi olingandan keyin O'ZGARMAS deb belgilanadi va hech qachon o'zgarmaydi, hatto tizim buni majburlay olmasa ham; tizim o'zi yaratadigan ID uchun esa yaratish algoritmi tizim ichida yagonalikni kafolatlashi shart, va bu parallel ishlov hamda taqsimlangan tizimda alohida qiyinchilik (*Domain-Driven Design*, 5-bob, 69-bet). Uchinchisi - tabiiy kalit haqida: Evans tashqi ID lar ishonchsizligini misol bilan ko'rsatadi (telefon raqami o'zgaradi, davlat bergan raqam hammada bo'lmaydi), shuning uchun ko'pincha maxsus tayinlangan identifikator ishlatiladi (shu bet). To'rtinchi nuqta review uchun muhim: Evans ID ning tizim ichkarisida qolishini va foydalanuvchiga ko'rinishini alohida hollar deb ajratadi (shu bet).

Shu uch talabdan review savollari kelib chiqadi:

| Review savoli | Nega (kitobdan) |
| --- | --- |
| ID yaratilgandan keyin o'zgarishi mumkinmi | Evans: ID immutable deb belgilanadi, hech qachon o'zgarmaydi |
| Yagonalik kim tomonidan kafolatlanadi | Evans: generator tizim ichida yagonalikni kafolatlashi shart, concurrency va taqsimlanganlik bu yerda qiyinchilik tug'diradi |
| Tabiiy kalit tanlangan bo'lsa, u o'zgara oladimi | Evans: tashqi/tabiiy identifikatorlar o'zgaradi va to'liq emas |
| ID tashqi API da ko'rinadimi | Evans: ichki ID va foydalanuvchiga ko'rinadigan ID alohida hollar |

```java
// Tipli ID: almashtirib qo'yish kompilyatsiyada tutiladi (8.5).
public record OrderId(UUID value) {
    public static OrderId newId() { return new OrderId(UuidCreator.getTimeOrderedEpoch()); }
    @Override public String toString() { return value.toString(); }
}

// JPA bilan ishlatish uchun converter (yoki @Embedded).
@Converter(autoApply = true)
class OrderIdConverter implements AttributeConverter<OrderId, UUID> {
    @Override public UUID convertToDatabaseColumn(OrderId id) {
        return id == null ? null : id.value();
    }
    @Override public OrderId convertToEntityAttribute(UUID db) {
        return db == null ? null : new OrderId(db);
    }
}
```

Oxirgi savolning review izohi: ketma-ket ichki ID tashqariga chiqsa, qiymat taxmin qilinadigan bo'ladi va avtorizatsiya tekshiruvi yo'q endpoint da boshqa mijozning resursi ochiladi. Bu domen modeli emas, avtorizatsiya kamchiligi, shuning uchun uning yozuvi [30-bob](30-autentifikatsiya-va-avtorizatsiya-review.md) da: model review da faqat "bu ID tashqariga chiqadimi" savoli beriladi va javob 30-bobga uzatiladi.

ESLATMA: `bigserial`, UUID v4 va UUID v7 orasidagi indeks hajmi va insert tezligi solishtirmasi bu bobdan olib tashlangan, chunki quyidagi manbalarning hech birida bunday o'lchov yo'q. Baza tomonidagi tanlov `postgres-tuning` doirasida, o'z o'lchovi bilan hal qilinadi.

## 13.6 Domen eventlari: nima e'lon qilinadi

Uchta review xatosi bor va uchtasi ham Richardson da aniq qoida bilan yopiladi.

Birinchisi - nom. Domen eventi - o'tgan zamon sifatdoshi bilan nomlangan sinf, u agregatga yuz bergan narsani bildiradi, odatda holat o'zgarishini: `Order Created`, `Order Cancelled`, `Order Shipped` (*Microservices Patterns*, 5-bob, 160-161-bet). Demak `SendEmail` event emas, buyruq: review da nom o'zgartiriladi yoki tur boshqa joyga ko'chiriladi.

Ikkinchisi - yuk. Richardson da eventning har bir xossasi yo primitiv qiymat, yo value object bo'ladi; qo'shimcha ma'lumot (event ID, vaqt, o'zgartirgan foydalanuvchi) metadata yoki konvert obyektida turadi (shu kitob, 161-bet). Eventga o'zgaruvchan entity yoki lazy proxy solingan diff shu qoidani buzadi.

Uchinchisi - vaqt. Richardson: servis eventlarni tranzaksion messaging bilan e'lon qilishi shart, ya'ni event agregatni yangilagan tranzaksiyaning o'zi bilan birga chiqadi - amalda event ACID tranzaksiya ichida OUTBOX jadvaliga yoziladi, commit dan keyin esa broker ga uzatiladi (shu kitob, 166-bet). Demak tranzaksiyadan oldin publish qilish ham, commit dan keyin alohida publish qilish ham kafolatsiz: review da outbox borligi so'raladi ([patterns 10.14](../patterns/10-malumotlarni-boshqarish-va-taqsimlash.md#1014-tranzaksion-outbox-transactional-outbox)).

```java
// Agregat ichida event yig'ish, publish qilish - saqlashdan keyin.
@Entity
public class Order extends AbstractAggregateRoot<Order> {   // Spring Data
    public void markPaid(PaymentId paymentId, Instant when) {
        if (status != NEW) throw new IllegalStateTransition(status, PAID);
        this.status = PAID;
        this.paidAt = when;
        registerEvent(new OrderPaid(new OrderId(id), paymentId, total, when));
    }
}
// Spring Data repository.save() dan keyin eventlar e'lon qiladi, ya'ni
// agregat holati bilan birga. Qabul qiluvchi tomonda:
@TransactionalEventListener(phase = AFTER_COMMIT)
void on(OrderPaid e) { /* commit dan keyin, yetkazish kafolati kerak bo'lsa outbox */ }
```

Shu shaklning kitobdagi asosi: Richardson da eventni tushuncha jihatidan agregat e'lon qiladi, chunki holat o'zgarishini faqat agregat biladi; agregat messaging API ni to'g'ridan-to'g'ri chaqirsa, u dependency injection ishlatmagani uchun API metod argumenti sifatida yurishga to'g'ri keladi va infratuzilma biznes mantiqqa chirmashadi (*Microservices Patterns*, 5-bob, 164-bet). Spring Data dagi `AbstractAggregateRoot` aynan shu muammoni yopadi. Mexanizmning o'z yozuvi [patterns 13.33](../patterns/13-domain-driven-design-patternlari.md#1333-spring-data-bilan-domen-hodisalari-domain-events-with-spring-data-abstractaggregateroot-domainevents) da.

## 13.7 Domen tili: kod va suhbat bir xil so'z bilan

Agar biznes "aktivatsiya" deyotgan bo'lsa, kodda `enable`, `turnOn` va `activate` aralash ishlatilsa, har suhbatda tarjima qilish kerak bo'ladi.

Evans da talab ikki qismdan iborat. Birinchisi - modelni tilning asosi qilib olish va shu tildan guruh ichidagi BARCHA muloqotda hamda KODDA foydalanish; bir tushuncha uchun bir nom diagrammada, yozuvda va ayniqsa og'zaki suhbatda ishlatiladi (*Domain-Driven Design*, 2-bob, 26-bet). Ikkinchisi - til o'zgarganda kodni ergashtirish: iborani muhokama bilan tanlab, keyin kodni refactor qilib sinf, metod va modul nomlari yangi modelga moslanadi (shu bet). Shu sababli nom haqidagi review izohi "uslub" emas: kod bilan suhbat orasidagi tarjimani yo'q qilish modelning o'zi uchun ishlaydi.

Evans tarjimaning narxini ham aytadi: umumiy til bo'lmasa, tarjima har doim noaniq bo'ladi, tushunmovchilikni yashiradi va kodning buzuvchi refactoring ga uchrashiga olib keladi (shu kitob, 25-bet).

```bash
# Domen tilining izchilligini tekshirish: bitta tushuncha necha xil nom bilan.
# -o har uchrashni alohida qatorga chiqaradi, ya'ni wc -l uchrashlar sonini
# beradi. -w qo'yilmaydi: u activateAccount kabi camelCase nomni o'tkazib yuboradi.
for term in activate enable turnOn start; do
  printf '%-10s %s\n' "$term" "$(grep -rhoi --include='*.java' "$term" src/main/java | wc -l)"
done
# Nechta faylda uchrashini bilish kerak bo'lsa: grep -rli --include='*.java' "$term" src/main/java | wc -l
# Natijada bir tushuncha uchun to'rt nom chiqsa, lug'atni kelishib olish kerak.
```

ESLATMA: `GLOSSARY.md` faylida asosiy tushunchalar va ularning yagona kodli nomini saqlash - shu korpusning amaliy tavsiyasi, kitobdan olingan talab emas (Evans da lug'at fayli emas, tilning o'zi talab qilinadi). Tushunchalar soni ham kitobdan emas, shuning uchun bu yerda raqam berilmaydi. Review da yangi nom paydo bo'lganda shu faylga qarash kifoya.

## 13.8 Domen servisi qachon kerak

Qoida mavjud obyektga sig'maydigan holatlar uchun domen servisi ishlatiladi.

Evans da yaxshi servisning uchta belgisi sanalgan: amal entity yoki value object ning tabiiy qismi bo'lmagan domen tushunchasiga tegishli, interfeys domen modelining boshqa elementlari bilan ta'riflanadi, va amal HOLATSIZ (*Domain-Driven Design*, 5-bob, 76-bet). Holatsizlik bu yerda aniq ma'noga ega: har qanday chaqiruvchi servisning har qanday nusxasidan uning o'tmishiga qaramay foydalana oladi (shu bet). Nomlash ham shundan kelib chiqadi - servis entity emas, faoliyat nomi bilan, ya'ni fe'l bilan nomlanadi (shu bet).

Evans ning o'z misoli chegarani ko'rsatadi: pul o'tkazish domen servisi, chunki "funds transfer" bank tilidagi tushuncha va u muhim biznes qoidalarini (to'g'ri hisoblarga debet va kredit) o'z ichiga oladi; tranzaksiyalarni jadvalga eksport qilish esa application servis, chunki bank domenida "fayl formati" degan tushuncha yo'q va biznes qoidasi qatnashmaydi (shu kitob, 76-77-bet).

| Qoida qayerda turadi | Misol |
| --- | --- |
| Agregat ichida | "Buyurtma summasi qatorlar summasiga teng" |
| Value object ichida | "Email shakli to'g'ri" |
| Domen servisida | "Mijozning kredit limiti yetadimi" (hisob + mijoz) |
| Application servisida | Tranzaksiya, avtorizatsiya, chaqiruvlar ketma-ketligi |
| Infra da | SQL, HTTP, serializatsiya |

Review belgisi: application servis ichida biznes hisobi paydo bo'lsa (biznes tilida nomi bor qoida), u domenga tushishi kerak. Teskari belgi ham shu qatlamlar bo'linishidan kelib chiqadi: Evans ning qatlam jadvalida kiruvchi so'rovni hazm qilish, domen servisiga murojaat qilish, javobni kutish va xabarnoma yuborish qarorini qabul qilish - application servisning ishi (shu kitob, 77-bet), Richardson da esa repository dan agregatni olib kelish va saqlash aynan servis (application) vazifasi (*Microservices Patterns*, 5-bob, 159-bet). Demak `@Transactional` va repository ko'rinib turgan sinf domen servisi emas. Domen servisining to'liq yozuvi [patterns 13.18](../patterns/13-domain-driven-design-patternlari.md#1318-domen-servisi-domain-service) da.

## 13.9 ORM domen modelini buzganda

JPA talablari domen modeliga ta'sir qiladi: no-arg konstruktor, mutable maydonlar, `@Id`. Review savoli - qaysi murosaga ongli kelingan.

Evans bu murosani kitobda alohida ko'rib chiqadi va yo'nalishni aniq beradi: baza obyekt ombori sifatida ishlatilsa, mapping qurolining kuchidan qat'i nazar ma'lumot modeli bilan obyekt modelini bir-biridan uzoqlashtirmaslik kerak, hatto obyekt munosabatlarining boyligidan qurbon berib (*Domain-Driven Design*, 6-bob, 114-bet). Shu bet da ikkita review uchun tayyor mezon bor: mapping lar SHAFFOF bo'lishi, ya'ni koddan yoki mapping yozuvidan ko'rinib turishi shart; va obyekt tizimidan tashqaridagi process lar shu omborga tegmasligi kerak, chunki ular obyektlar himoyalagan invariantlarni buzadi. Uchinchi mezon nomlashga tegishli: obyektdagi va jadvaldagi mos elementlar sinchkovlik bilan BIR XIL nomlanishi kerak, aks holda shaffoflik tez yo'qoladi (shu bet).

Quyidagi jadval shu mezonlarni JPA tilida ochadi.

| JPA talabi | Domen uchun oqibati | Murosa |
| --- | --- | --- |
| No-arg konstruktor | To'liq bo'lmagan obyekt yaratilishi mumkin | `protected` qilish |
| Maydonlar `final` bo'lmaydi | Immutable emas | Setterlarni olib tashlash |
| Kolleksiyalar mutable | Tashqaridan o'zgartirish | Himoyalangan ko'rinish qaytarish |
| Lazy proxy | Domen tashqarisida istisno | Agregat chegarasida yuklash |
| `@Id` generated | `equals`/`hashCode` muammosi | Biznes kalit yoki oldindan yaratilgan UUID |
| Dirty checking | Har `set` yozuvga aylanadi | Domen metodlari orqali o'zgartirish |

Jadvalning ikkinchi va uchinchi qatori Bloch ning o'zgarmaslik qoidalariga tegadi: barcha maydon `final` bo'lishi (3-qoida) va mutable komponentga tashqaridan havola chiqmasligi, ya'ni getter da himoya nusxasi (5-qoida) - *Effective Java* 3-nashr, Item 17, 80-bet. JPA bu ikkisini to'liq bajarishga yo'l qo'ymaydi, shuning uchun review da savol "bajarilganmi" emas, "qancha chekinilgan va nega" bo'ladi.

```java
// JPA entity uchun equals/hashCode: eng ko'p xato qilinadigan joy.
@Entity
public class Order {
    @Id private UUID id = UUID.randomUUID();   // oldindan yaratilgan: generated emas

    // ID oldindan ma'lum bo'lgani uchun equals barqaror: obyekt saqlanishdan
    // oldin ham keyin ham bir xil hashCode beradi.
    @Override public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Order other)) return false;
        return id.equals(other.id);
    }
    @Override public int hashCode() { return id.hashCode(); }
}
// Agar @GeneratedValue ishlatilsa: saqlashdan oldin id = null, keyin 42.
// Bu to'g'ridan-to'g'ri hashCode shartnomasini buzadi: Bloch da hashCode
// bitta ishga tushishi davomida bir obyektda qayta-qayta chaqirilganda
// DOIM bir xil qiymat qaytarishi shart, agar equals da ishlatiladigan
// ma'lumot o'zgarmagan bo'lsa (Effective Java 3-nashr, Item 11, 50-bet).
// Shu obyekt HashSet ga qo'yilgandan keyin saqlansa, hashCode o'zgaradi va
// u Set ichida "yo'qoladi". Review da bu holat alohida tekshiriladi.
```

## 13.10 Modelga tegadigan PR uchun qo'shimcha talablar

Domen modeli o'zgarishi boshqa o'zgarishlardan ko'proq narsani talab qiladi, chunki u ma'lumotga va API ga tarqaydi. Quyidagi jadval shu korpusning review talablari ro'yxati: uning birinchi bandi (model va sxema bir-biriga mos turishi) Evans ning 114-betdagi talabiga tayanadi, qolganlari esa kitobdan emas, amaliyotdan.

| Talab | Nega |
| --- | --- |
| Migratsiya bilan birga keladi | Model va sxema bir-biriga mos bo'lishi kerak |
| Invariant testi bor | Noto'g'ri holat yaratilmasligini tekshirish |
| Holat o'tish matritsasi testi | Taqiqlangan o'tishlar rad etilishi |
| Mavjud ma'lumot bilan moslik | Eski qatorlar yangi qoidani buzmaydimi |
| API ta'siri baholangan | Yangi majburiy maydon mijozni sindiradimi |
| Terminologiya `GLOSSARY.md` da | Nom izchil |

Ayniqsa beshinchi band: yangi `NOT NULL` maydon qo'shilsa, mavjud qatorlar uchun qiymat qayerdan keladi. Bu savolga javob migratsiya review da emas, model review da berilishi kerak ([25-bob](25-migratsiya-review-qulf-backfill-orqaga.md)).

## 13.11 Amalda qo'llash

- [ ] Domen entity larida `public` setterlar sonini sanang va biznes jarayoni modullarida ularni domen metodlariga aylantirish ro'yxatini tuzing.
- [ ] Har bir agregat uchun "qaysi invariant tranzaksiya ichida kafolatlanadi" degan javobni bir satrda yozing.
- [ ] `EAGER` va `cascade = ALL` ishlatilgan `@OneToMany` larni toping va agregat chegarasini qayta ko'rib chiqing.
- [ ] `BigDecimal` ishlatadigan value object larda `setScale` normalizatsiyasi borligini tekshiring.
- [ ] `@GeneratedValue` bilan ishlaydigan entity larning `equals`/`hashCode` ini ko'rib chiqing va UUID ga o'tish variantini baholang.
- [ ] Ichki ketma-ket ID lar tashqi API da ko'rinadigan joylarni aniqlab, IDOR xavfini baholang.
- [ ] `GLOSSARY.md` yaratib, takrorlanayotgan tushunchalar uchun yagona kodli nomni kelishib oling.
- [ ] Bitta tranzaksiyada bir nechta agregat o'zgaradigan joylarni toping va har biri uchun chekinish ongli qilinganini tekshiring.
- [ ] Domen modeliga tegadigan PR lar uchun qo'shimcha talablar jadvalini PR shabloniga kiriting.

## Manbalar

- Eric Evans, *Domain-Driven Design*, Addison-Wesley, 2004, 2-bob (25-31-bet) - umumiy til: modelni tilning asosi qilish, bir tushunchaga bir nom, til o'zgarganda kodni refactor bilan ergashtirish, tarjimaning narxi (13.7)
- Eric Evans, *Domain-Driven Design*, Addison-Wesley, 2004, 5-bob (65-78-bet) - entity ayniyat bilan, value object esa faqat qiymati bilan aniqlanadi; value object o'zgarmas tutiladi va unga ayniyat berilmaydi; ID immutable deb belgilanadi va generator yagonalikni kafolatlashi shart; domen servisining uchta belgisi (76-bet) va domen/application/infra bo'linishi (76-77-bet) (13.4, 13.5, 13.8)
- Eric Evans, *Domain-Driven Design*, Addison-Wesley, 2004, 6-bob (89-103 va 113-115-bet) - agregat chegarasi va ildizi, invariantlar commit da bajarilishi, agregat qoidalari (tashqaridan faqat ildizga havola, bazadan faqat ildiz so'raladi, o'chirish chegarani butun oladi), public konstruktor fabrika qoidasiga bo'ysunishi, obyekt modeli bilan sxemani uzoqlashtirmaslik va mapping shaffofligi (13.1, 13.3, 13.9)
- Martin Fowler, *Patterns of Enterprise Application Architecture*, Addison-Wesley, 2003, 2-bob (29-30-bet) va 9-bob (116-120-bet) - Transaction Script, Table Module va Domain Model orasidagi tanlov faqat domen mantiqining murakkabligiga bog'liq, va bu murakkablikni o'lchash usuli yo'q (13.2)
- Chris Richardson, *Microservices Patterns*, Manning, 2019, 5-bob (149-166-bet) - Transaction Script va Domain model tanlovi, agregatning uch qoidasi (faqat ildizga havola, agregatlar orasida birlamchi kalit, bitta tranzaksiya bitta agregat), agregatni mayda tutish, domen eventining o'tgan zamon nomi va xossalari, eventni outbox bilan tranzaksion e'lon qilish (13.2, 13.3, 13.6)
- Vlad Khononov, *Learning Domain-Driven Design*, O'Reilly, 2021, 6-bob (78-81 va 87-90-bet) - value object validatsiyani o'z ichida saqlashi va primitive obsession ni yopishi, o'zgarmaslik va qiymat bo'yicha tenglik, agregat tranzaksiya chegarasi hamda uni iloji boricha kichik tutish (13.3, 13.4)
- Joshua Bloch, *Effective Java*, 3-nashr, Addison-Wesley, 2018, Item 17 (80-bet) - o'zgarmaslikning besh qoidasi; Item 11 (50-bet) - hashCode ning bir ishga tushish ichida barqaror qolish shartnomasi; Item 14 (68-69-bet) - `BigDecimal` ning `compareTo` si `equals` bilan izchil emasligi va HashSet / TreeSet dagi oqibati (13.4, 13.9)
- ESLATMA: "Anemic Domain Model" atamasi *PoEAA* da umuman uchramaydi (kitob matni bo'yicha tekshirildi), u Fowler ning alohida yozuvidan keladi. 13.2 da atama kitobga yoki Evans ga tegishli deb ko'rsatilmaydi, kitobdan faqat tanlov mezoni olingan
- ESLATMA: Evans ga berilgan bet raqamlari 2003 yil aprel "Final Manuscript" nusxasiga tegishli (uning mundarijasi va bet pastidagi raqamlar bir-biriga mos), chop etilgan 2004 nashrda siljish bo'lishi mumkin; bob raqamlari ikkisida bir xil
- ESLATMA: 13.9 dagi JPA talabi va murosa jadvali, 13.10 dagi PR talablari jadvali, 13.11 checklisti va 13.7 dagi `GLOSSARY.md` tavsiyasi shu korpusning amaliy tekshiruv ro'yxati, kitobdan olingan emas; ulardagi alohida bandlarga qo'yilgan iqtiboslar bundan mustasno
- ESLATMA: 13.5 dan ID turlarini indeks hajmi va insert tezligi bo'yicha solishtirgan jadval, 13.2 dan esa "modul turi - mos model" taksonomiyasi o'chirildi, chunki yuqoridagi manbalarda bunday o'lchov ham, bunday tasnif ham yo'q

---

[&larr; 12. Code smell va anti-pattern katalogi diffda](12-code-smell-va-anti-pattern-katalogi-diffda.md) · [Mundarija](README.md) · [14. Java tili darajasidagi xatolar katalogi &rarr;](14-java-tili-darajasidagi-xatolar-katalogi.md)
