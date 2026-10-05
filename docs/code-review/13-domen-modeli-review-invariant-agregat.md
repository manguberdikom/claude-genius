<!-- doc: code-review | chapter: 13 | part: II. Arxitektura, dizayn va clean code review -->

[Barcha hujjatlar](../../README.md) / [Kod review](README.md)

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


Domen modeli - tizimning eng uzoq yashaydigan qismi. Controller qayta yoziladi, ORM almashtiriladi, lekin "buyurtma nima" degan savolning javobi yillar davomida qoladi. Shu sababli domen modeliga tegadigan PR boshqa PR lardan chuqurroq o'qiladi: bu yerdagi xato keyinchalik yuzta joyda ko'rinadi. DDD atamalarining ta'rifi [Dizayn patternlar](../patterns/README.md) va [Arxitektor miyyasi](../architect/README.md) da; bu yerda faqat review savollari.

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

## 13.2 Anemik modelni ongli tanlash

Anemik model har doim xato emas. CRUD ustun bo'lgan modulda (ma'lumotnoma jadvallar, sozlamalar, admin panel) boy model ortiqcha. Xato - tanlovning ongsizligi: biznes qoidalari ko'p bo'lgan modulda anemik modeldan foydalanish.

| Modul turi | Mos model | Review kutilmasi |
| --- | --- | --- |
| Ma'lumotnoma, sozlama | Anemik + validation | Setterlar normal, DTO = entity bo'lishi mumkin |
| Hisobot va o'qish | Projection, DTO | Entity umuman kerak emas |
| Biznes jarayoni (buyurtma, to'lov) | Boy model | Setterlar yo'q, holat metodlari bor |
| Integratsiya (adapter) | Oddiy struktura | Mapping va tashqi shakl |

Xavfli belgi: bitta modulda ikki yondashuv aralashgan - qoidalarning yarmi entity da, yarmi servisda. Shu holatda invariantni hech kim to'liq himoya qilmaydi.

## 13.3 Agregat chegarasi: nima birga saqlanadi

Agregat - birga o'zgaradigan va birga tekshiriladigan obyektlar guruhi. Chegara review da ikki savol bilan tekshiriladi: qaysi invariant tranzaksiya ichida kafolatlanishi kerak, va agregat qanchalik katta bo'ladi.

```java
// Juda katta agregat: buyurtmaga 50 000 qator ilashishi mumkin.
@Entity
public class Customer {
    @OneToMany(mappedBy = "customer", cascade = ALL, fetch = EAGER)
    private List<Order> orders = new ArrayList<>();      // yillar davomida o'sadi
}
// Review izohlari: (1) EAGER - mijozni yuklash barcha buyurtmalarni
// tortadi; (2) cascade ALL - mijozni o'chirish barcha buyurtmalarni
// o'chiradi, bu biznes qoidasimi?; (3) yangi buyurtma qo'shish uchun butun
// kolleksiya yuklanadi - xotira va qulf.
// Yechim: Order alohida agregat, Customer faqat CustomerId bilan bog'lanadi.

// To'g'ri chegara: agregatlar ID orqali bog'lanadi.
@Entity
public class Order {
    @Id @GeneratedValue private Long id;
    @Embedded private CustomerId customerId;        // boshqa agregatga havola
    @ElementCollection                              // buyurtma qatorlari esa ichida
    private List<OrderLine> lines = new ArrayList<>();
}
```

Chegara mezoni: invariant tranzaksiya ichida kafolatlanishi kerakmi. "Buyurtma summasi qatorlar summasiga teng" - ha, demak qatorlar agregat ichida. "Mijozning umumiy xaridi 10 mln dan oshmaydi" - bu boshqa agregatga tegadi, uni tranzaksiya emas, jarayon bilan ta'minlash kerak (yoki ongli ravishda eventual consistency qabul qilinadi).

## 13.4 Value object va entity farqi diffda

Value object qiymati bilan aniqlanadi va o'zgarmaydi (`Money`, `Address`, `DateRange`, `Email`). Entity identifikatori bilan aniqlanadi va holati o'zgaradi. Review da aralashtirish belgisi: value object da `id` paydo bo'lishi yoki setterlar qo'shilishi.

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
// Review diqqati: record da `equals` avtomatik, lekin BigDecimal da
// 10.00 va 10.0 teng EMAS (scale farqi). Shu sababli konstruktorda
// setScale qilinmasa, teng summalar teng emas deb chiqadi - jadvalda
// va Set da jim xato beradi.
```

## 13.5 Identifikator dizayni

ID turini tanlash qaytarib bo'lmaydigan qarorlar qatoriga kiradi: u API ga, indekslarga va tashqi tizimlarga tarqaydi.

| Variant | Foydasi | Narxi | Review savoli |
| --- | --- | --- | --- |
| `bigserial` (ketma-ket) | Kichik indeks, tabiiy tartib | Raqamni taxmin qilish mumkin, merge qiyin | ID tashqariga chiqadimi |
| `uuid` v4 | Taxmin qilinmaydi, taqsimlangan yaratish | Indeks katta va tasodifiy, insert sekinroq | Hajm va insert tezligi muhimmi |
| UUID v7 / ULID | Vaqt bo'yicha tartibli, taqsimlangan | Yangi, kutubxona kerak | Indeks lokalligi kerakmi |
| Tabiiy kalit (`order_number`) | Biznes uchun ma'noli | O'zgarishi mumkin, formati qotib qoladi | Qiymat o'zgarishi mumkinmi |

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

Review da alohida savol: ichki ID tashqi API da ko'rinadimi. Ketma-ket ID tashqariga chiqsa, raqobatchi buyurtmalar sonini biladi va mijozlar bir-birining resursini taxmin qila oladi (IDOR xavfi, [30-bob](30-autentifikatsiya-va-avtorizatsiya-review.md)).

## 13.6 Domen eventlari: nima e'lon qilinadi

Domen eventi o'tgan zamonda nomlanadi va o'zgarmas faktni bildiradi: `OrderPlaced`, `PaymentCaptured`. Review da uch xato uchraydi: event buyruq kabi nomlangan (`SendEmail`), eventda mutable obyekt uzatilgan, va event tranzaksiyadan oldin e'lon qilingan.

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

## 13.7 Domen tili: kod va suhbat bir xil so'z bilan

Agar biznes "aktivatsiya" deyotgan bo'lsa, kodda `enable`, `turnOn` va `activate` aralash ishlatilsa, har suhbatda tarjima qilish kerak bo'ladi. Review da bu arzon tuzatiladi, keyinroq esa qimmat.

```bash
# Domen tilining izchilligini tekshirish: bitta tushuncha necha xil nom bilan.
for term in activate enable turnOn start; do
  printf '%-10s %s\n' "$term" "$(grep -rn --include='*.java' -c "$term" src/main/java | wc -l)"
done
# Natijada bir tushuncha uchun to'rt nom chiqsa, lug'atni kelishib olish kerak.
```

Foydali amal: `GLOSSARY.md` faylida 20-40 asosiy tushuncha va ularning yagona kodli nomi. Review da yangi nom paydo bo'lganda shu faylga qarash kifoya.

## 13.8 Domen servisi qachon kerak

Qoida mavjud obyektga sig'maydigan holatlar uchun domen servisi ishlatiladi: qoida ikki agregatga tegadi, yoki tashqi ma'lumot kerak. Review da belgisi: servis nomi "nima qilishi" bilan nomlangan va holatsiz.

| Qoida qayerda turadi | Misol |
| --- | --- |
| Agregat ichida | "Buyurtma summasi qatorlar summasiga teng" |
| Value object ichida | "Email shakli to'g'ri" |
| Domen servisida | "Mijozning kredit limiti yetadimi" (hisob + mijoz) |
| Application servisida | Tranzaksiya, avtorizatsiya, chaqiruvlar ketma-ketligi |
| Infra da | SQL, HTTP, serializatsiya |

Belgi: application servis ichida 50 satrli biznes hisobi paydo bo'lsa, u domenga tushishi kerak. Teskari belgi: domen servisi `@Transactional` yoki repository bilan ishlasa, u aslida application servis.

## 13.9 ORM domen modelini buzganda

JPA talablari domen modeliga ta'sir qiladi: no-arg konstruktor, mutable maydonlar, `@Id`. Review savoli - qaysi murosaga ongli kelingan.

| JPA talabi | Domen uchun oqibati | Murosa |
| --- | --- | --- |
| No-arg konstruktor | To'liq bo'lmagan obyekt yaratilishi mumkin | `protected` qilish |
| Maydonlar `final` bo'lmaydi | Immutable emas | Setterlarni olib tashlash |
| Kolleksiyalar mutable | Tashqaridan o'zgartirish | Himoyalangan ko'rinish qaytarish |
| Lazy proxy | Domen tashqarisida istisno | Agregat chegarasida yuklash |
| `@Id` generated | `equals`/`hashCode` muammosi | Biznes kalit yoki oldindan yaratilgan UUID |
| Dirty checking | Har `set` yozuvga aylanadi | Domen metodlari orqali o'zgartirish |

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
// Shu obyekt HashSet ga qo'yilgandan keyin saqlangan bo'lsa, u Set ichida
// "yo'qoladi" - hashCode o'zgargan. Review da bu holat alohida tekshiriladi.
```

## 13.10 Modelga tegadigan PR uchun qo'shimcha talablar

Domen modeli o'zgarishi boshqa o'zgarishlardan ko'proq narsani talab qiladi, chunki u ma'lumotga va API ga tarqaydi.

| Talab | Nega |
| --- | --- |
| Migratsiya bilan birga keladi | Model va sxema bir-biriga mos bo'lishi kerak |
| Invariant testi bor | Noto'g'ri holat yaratilmasligini tekshirish |
| Holat o'tish matritsasi testi | Taqiqlangan o'tishlar rad etilishi |
| Mavjud ma'lumot bilan moslik | Eski qatorlar yangi qoidani buzmaydimi |
| API ta'siri baholangan | Yangi majburiy maydon mijozni sindiradimi |
| Terminologiya `GLOSSARY.md` da | Nom izchil |

Ayniqsa beshinchi band: yangi `NOT NULL` maydon qo'shilsa, mavjud 4 mln qator uchun qiymat qayerdan keladi. Bu savolga javob migratsiya review da emas, model review da berilishi kerak ([25-bob](25-migratsiya-review-qulf-backfill-orqaga.md)).

## 13.11 Amalda qo'llash

- [ ] Domen entity larida `public` setterlar sonini sanang va biznes jarayoni modullarida ularni domen metodlariga aylantirish ro'yxatini tuzing.
- [ ] Har bir agregat uchun "qaysi invariant tranzaksiya ichida kafolatlanadi" degan javobni bir satrda yozing.
- [ ] `EAGER` va `cascade = ALL` ishlatilgan `@OneToMany` larni toping va agregat chegarasini qayta ko'rib chiqing.
- [ ] `BigDecimal` ishlatadigan value object larda `setScale` normalizatsiyasi borligini tekshiring.
- [ ] `@GeneratedValue` bilan ishlaydigan entity larning `equals`/`hashCode` ini ko'rib chiqing va UUID ga o'tish variantini baholang.
- [ ] Ichki ketma-ket ID lar tashqi API da ko'rinadigan joylarni aniqlab, IDOR xavfini baholang.
- [ ] `GLOSSARY.md` yaratib, 20 asosiy tushuncha uchun yagona kodli nomni kelishib oling.
- [ ] Domen modeliga tegadigan PR lar uchun qo'shimcha talablar jadvalini PR shabloniga kiriting.

---

[&larr; 12. Code smell va anti-pattern katalogi diffda](12-code-smell-va-anti-pattern-katalogi-diffda.md) · [Mundarija](README.md) · [14. Java tili darajasidagi xatolar katalogi &rarr;](14-java-tili-darajasidagi-xatolar-katalogi.md)
