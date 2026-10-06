<!-- doc: clean-code | chapter: 28 | part: VIII. Spring va ma'lumot qatlamida toza kod -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 28. JPA va SQL kodining tozaligi (Clean JPA and SQL)

<details>
<summary>Bu bobdagi 10 bo'lim</summary>

- [28.1 Entitet gigiyenasi: `equals`, `hashCode`, `toString`](#281-entitet-gigiyenasi-equals-hashcode-tostring)
- [28.2 Lombok va entitet: nimani ishlatmaslik](#282-lombok-va-entitet-nimani-ishlatmaslik)
- [28.3 Assotsiatsiya yordamchi metodlari va ikki tomonlilik](#283-assotsiatsiya-yordamchi-metodlari-va-ikki-tomonlilik)
- [28.4 `fetch`, `cascade`, `orphanRemoval` ni oshkor yozish](#284-fetch-cascade-orphanremoval-ni-oshkor-yozish)
- [28.5 Repository metod nomlari: derived query chegarasi](#285-repository-metod-nomlari-derived-query-chegarasi)
- [28.6 `@Query`, native query va ularni o'qiladigan ushlash](#286-query-native-query-va-ularni-oqiladigan-ushlash)
- [28.7 Projeksiya va DTO qaytarish](#287-projeksiya-va-dto-qaytarish)
- [28.8 SQL yozish uslubi](#288-sql-yozish-uslubi)
- [28.9 Migratsiya fayli nomlanishi va mazmuni](#289-migratsiya-fayli-nomlanishi-va-mazmuni)
- [28.10 Amalda qo'llash](#2810-amalda-qollash)

</details>


Hibernate mexanikasi va PostgreSQL chuqur bilimi [arxitektor hujjatidagi](../architect/README.md) Spring Data JPA va Hibernate bo'limida, ORM patternlari [patternlar hujjatidagi](../patterns/README.md) ma'lumotlarga kirish va ORM patternlari bo'limida. Bu bobda ma'lumot qatlami **kodining** tozaligi: entitet gigiyenasi, assotsiatsiyalar, repository metodlari, SQL yozish uslubi.

## 28.1 Entitet gigiyenasi: `equals`, `hashCode`, `toString`

JPA entiteti uchun tenglik qoidalari oddiy obyektdan farq qiladi (15.4-15.5): identifikator bo'yicha tenglik, barqaror `hashCode`, va proxy bilan ishlaydigan `instanceof`.

```java
@Entity
@Table(name = "payment")
public class Payment {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        // Hibernate proxy uchun instanceof kerak, getClass() emas
        if (!(o instanceof Payment other)) return false;
        // id null bo'lsa (hali saqlanmagan) obyektlar faqat o'ziga teng
        return id != null && id.equals(other.id);
    }

    @Override
    public int hashCode() {
        // Barqaror: id tayinlanganda ham hash o'zgarmaydi (15.9)
        return Payment.class.hashCode();
    }

    @Override
    public String toString() {
        // Faqat skalyar maydonlar: lazy assotsiatsiya yuklanmaydi (15.7)
        return "Payment{id=%s, amount=%s, status=%s}".formatted(id, amount, status);
    }
}
```

## 28.2 Lombok va entitet: nimani ishlatmaslik

Lombok ning ba'zi annotatsiyalari entitetda nozik xato beradi va ularning hammasi 26.10 siyosatida taqiqlangan. Sabablarini bilish muhim, chunki xato jim o'tadi.

| Annotatsiya | Entitetda nima bo'ladi |
|---|---|
| `@Data` | setter + `equals`/`hashCode` barcha maydonlardan: lazy yuklash va noto'g'ri tenglik |
| `@EqualsAndHashCode` | assotsiatsiyalarni `equals` ga qo'shadi: butun grafni yuklaydi |
| `@ToString` | lazy kolleksiyalarni yuklaydi yoki `LazyInitializationException` beradi |
| `@Builder` | `@NoArgsConstructor` ni yo'qotadi: Hibernate entitetni yarata olmaydi |
| `@AllArgsConstructor` | maydon tartibi o'zgarsa jim xato |
| `@Setter` | invariantni buzadi (16.7) |
| `@Getter` | xavfsiz |
| `@NoArgsConstructor(access = PROTECTED)` | xavfsiz va kerakli |

## 28.3 Assotsiatsiya yordamchi metodlari va ikki tomonlilik

Ikki tomonli assotsiatsiyada ikki tomonni qo'lda sinxron ushlash kerak, aks holda xotiradagi obyekt grafi bazadagi holatga mos kelmaydi. Yechim: yordamchi metod va to'g'ridan-to'g'ri kolleksiyaga kirishni yopish (14.7).

```java
@Entity
public class Order {

    @OneToMany(mappedBy = "order", cascade = CascadeType.ALL, orphanRemoval = true)
    private final List<OrderLine> lines = new ArrayList<>();

    // Yordamchi metod ikki tomonni birga ushlaydi
    public void addLine(OrderLine line) {
        lines.add(line);
        line.setOrder(this);
    }

    public void removeLine(OrderLine line) {
        lines.remove(line);
        line.setOrder(null);
    }

    // Tashqariga o'zgartirilmas ko'rinish
    public List<OrderLine> lines() { return Collections.unmodifiableList(lines); }
}
```

Qo'shimcha qoida: ikki tomonli assotsiatsiya faqat haqiqatan kerak bo'lganda qo'yiladi. Bir tomonli `@ManyToOne` ko'pincha yetarli va ancha kam muammo beradi.

## 28.4 `fetch`, `cascade`, `orphanRemoval` ni oshkor yozish

Standart `fetch` qiymatlari xavfli: `@ManyToOne` va `@OneToOne` standart holatda `EAGER`, ya'ni har bir so'rov butun grafni tortadi. Qoida: har bir assotsiatsiyada `fetch` oshkor yoziladi va u deyarli har doim `LAZY`.

```java
// yomon: standart EAGER - har bir Payment o'qilganda Order ham yuklanadi
@ManyToOne
private Order order;

// yaxshi: oshkor LAZY; kerak bo'lganda join fetch bilan olinadi
@ManyToOne(fetch = FetchType.LAZY, optional = false)
@JoinColumn(name = "order_id", nullable = false)
private Order order;
```

`cascade` ham oshkor bo'lishi kerak: `CascadeType.ALL` `REMOVE` ni ham o'z ichiga oladi va bu kutilmagan o'chirishlarga olib keladi. Agregat ildizi va uning qismlari orasida `ALL` + `orphanRemoval` to'g'ri; mustaqil entitetlar orasida esa `cascade` umuman bo'lmasligi kerak.

| Munosabat | `cascade` | `orphanRemoval` |
|---|---|---|
| Agregat ildizi → qismi (`Order` → `OrderLine`) | `ALL` | `true` |
| Mustaqil entitetlar (`Payment` → `Customer`) | yo'q | `false` |
| Ko'pdan-ko'pga | `PERSIST`, `MERGE` | `false` |
| Audit yozuvi | yo'q | `false` |

## 28.5 Repository metod nomlari: derived query chegarasi

Spring Data derived query lari qisqa va o'qiladi, lekin faqat ma'lum uzunlikka qadar. `findByCustomerIdAndStatusInAndCreatedAtBetweenOrderByCreatedAtDesc` nomi chegarani oshib ketgan: uni o'qish SQL o'qishdan qiyin.

Qoida: metod nomi uch shartdan oshsa, `@Query` yoki Specification ga o'tish kerak.

```java
public interface PaymentRepository extends JpaRepository<Payment, Long> {

    // yaxshi: qisqa va o'qiladi
    Optional<Payment> findByIdempotencyKey(IdempotencyKey key);
    List<Payment> findByOrderId(Long orderId);

    // yomon: nom chegaradan oshgan
    // List<Payment> findByCustomerIdAndStatusInAndCreatedAtBetweenOrderByCreatedAtDesc(...)

    // yaxshi: @Query bilan oshkor, nomi niyatni aytadi
    @Query("""
            select p from Payment p
            where p.customerId = :customerId
              and p.status in :statuses
              and p.createdAt >= :from and p.createdAt < :toExclusive
            order by p.createdAt desc
            """)
    List<Payment> findRecentByCustomerAndStatus(
            @Param("customerId") CustomerId customerId,
            @Param("statuses") Set<SettlementStatus> statuses,
            @Param("from") Instant from,
            @Param("toExclusive") Instant toExclusive);
}
```

## 28.6 `@Query`, native query va ularni o'qiladigan ushlash

JPQL va native query uchun uch qoida bor. Birinchi, matn bloki ishlatish (12.9) - satr birlashtirish SQL ni o'qilmaydigan qiladi. Ikkinchi, nomlangan parametrlar (`:customerId`), pozitsion emas (`?1`). Uchinchi, parametrlarni **hech qachon** satr birlashtirish bilan qo'ymaslik (SQL injection).

```java
// yomon: SQL injection va o'qilmaydigan matn
@Query(value = "select * from payment where status = '" + status + "'", nativeQuery = true)

// yaxshi: parametr bog'langan, matn bloki, ustunlar sanalgan
@Query(value = """
        select p.id, p.amount, p.currency, p.settled_at
        from payment p
        where p.status = :status
          and p.settled_at >= :from
        """, nativeQuery = true)
List<PaymentRow> findSettledSince(@Param("status") String status, @Param("from") Instant from);
```

## 28.7 Projeksiya va DTO qaytarish

Butun entitetni o'qish kerak bo'lmasa, uni o'qimaslik kerak: projeksiya kamroq ustun oladi, lazy muammolarini yo'qotadi va entitetni tranzaksiyadan tashqariga chiqarmaydi ([patternlar hujjatidagi](../patterns/README.md) API da JPA entitetlarini fosh qilish anti-patterni).

```java
// yaxshi: interfeys projeksiyasi - Spring Data o'zi amalga oshiradi
public interface PaymentSummary {
    Long getId();
    Money getAmount();
    Instant getSettledAt();
}

List<PaymentSummary> findByOrderId(Long orderId);

// yaxshi: konstruktor projeksiyasi - record ga to'g'ridan-to'g'ri
@Query("""
        select new uz.shop.payment.PaymentSummary(p.id, p.amount, p.settledAt)
        from Payment p where p.orderId = :orderId
        """)
List<PaymentSummary> summariesFor(@Param("orderId") Long orderId);
```

## 28.8 SQL yozish uslubi

Migratsiya va native query dagi SQL ham kod va u ham o'qilishi kerak. Qoidalar qisqa va ularni formatter majburlay oladi (13.3 dagi Spotless `sql` bloki).

| Qoida | Sabab |
|---|---|
| Kalit so'zlar kichik harfda (yoki izchil katta) | izchillik |
| `select *` emas, ustunlar sanaladi | sxema o'zgarsa kod buzilmaydi |
| Har bir ustun/shart alohida qatorda | diff o'qiladi |
| `join ... on` oshkor, vergulli join yo'q | shart ko'rinadi |
| Ichma-ich subquery o'rniga CTE (`with`) | o'qiladi |
| Jadval aliaslari ma'noli (`p`, `o`), bir harfli emas-chi | qisqa va aniq |
| `where` da funksiya yo'q (`lower(col) = ?`) | indeks ishlaydi |
| Sanada yarim ochiq oraliq (`>=`, `<`) | 22.6 |

```sql
-- yaxshi: o'qiladi, ustunlar sanalgan, CTE bilan tekis
with settled as (
    select p.order_id,
           sum(p.amount) as settled_amount
    from payment p
    where p.settled_at >= :from
      and p.settled_at < :to_exclusive
    group by p.order_id
)
select o.id,
       o.customer_id,
       o.total_amount,
       coalesce(s.settled_amount, 0) as settled_amount
from orders o
left join settled s on s.order_id = o.id
where o.status = 'CONFIRMED'
order by o.created_at desc;
```

## 28.9 Migratsiya fayli nomlanishi va mazmuni

Migratsiya strategiyasi va to'xtashsiz reliz arxitektor hujjatidagi [sxema migratsiyasi va to'xtashsiz reliz](../architect/33-sxema-migratsiyasi-va-toxtashsiz-reliz.md) bobida. Bu yerda fayl darajasidagi qoidalar: [nomlanish](03-nom-turlari-boyicha-aniq-konvensiyalar.md#313-fayl-resurs-va-konfiguratsiya-kaliti-nomlari), bir migratsiya bir maqsad, va orqaga qaytarish imkoni.

```sql
-- V12__add_settled_at_to_payment.sql
-- Maqsad: hisob-kitob vaqtini saqlash. To'xtashsiz: avval ustun qo'shiladi (nullable),
-- keyingi relizda kod yozadi, V14 da not null qo'yiladi.

alter table payment
    add column settled_at timestamptz;

-- Indeks concurrently: jadval bloklanmaydi (katta jadval uchun majburiy)
create index concurrently if not exists ix_payment_settled_at
    on payment (settled_at)
    where settled_at is not null;
```

Qoidalar: bir faylda bir mantiqiy o'zgarish, migratsiyani qo'lda tahrirlamaslik (checksum buziladi), va ma'lumot migratsiyasini sxema migratsiyasidan ajratish.

## 28.10 Amalda qo'llash

- [ ] Barcha entitetlarda `equals`/`hashCode` ni identifikator bo'yicha yozib, `hashCode` ni barqaror qiling.
- [ ] Entitetlardagi `@Data`, `@EqualsAndHashCode`, `@ToString` annotatsiyalarini olib tashlang.
- [ ] Barcha `@ManyToOne` va `@OneToOne` ga oshkor `fetch = LAZY` qo'shing.
- [ ] `cascade = ALL` ishlatilgan joylarni 28.4 jadvaliga qarab ko'rib chiqing.
- [ ] Ikki tomonli assotsiatsiyalarga yordamchi metodlar qo'shib, kolleksiya getter larini o'zgartirilmas qiling.
- [ ] Uch shartdan uzun derived query nomlarini `@Query` ga o'tkazib, matn bloki bilan yozing.
- [ ] Entitet qaytaradigan API metodlarini projeksiya yoki DTO ga o'tkazing.
- [ ] SQL fayllarini 28.8 qoidalariga keltirib, `select *` ni ustun ro'yxatiga almashtiring.

---

[&larr; 27. REST API kodining o'qilishi](27-rest-api-kodining-oqilishi.md) · [Mundarija](README.md) · [29. Log kodining tozaligi &rarr;](29-log-kodining-tozaligi.md)
