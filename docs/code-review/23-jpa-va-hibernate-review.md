<!-- doc: code-review | chapter: 23 | part: V. PostgreSQL va ma'lumot qatlami review -->

[Barcha hujjatlar](../../README.md) / [Kod review](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 23. JPA va Hibernate review (JPA and Hibernate)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

- [23.1 N+1: diffdan ko'rish](#231-n1-diffdan-korish)
- [23.2 So'rovlar sonini test bilan qulflash](#232-sorovlar-sonini-test-bilan-qulflash)
- [23.3 Fetch strategiyasi](#233-fetch-strategiyasi)
- [23.4 Cascade va orphan removal](#234-cascade-va-orphan-removal)
- [23.5 Dirty checking va ortiqcha UPDATE](#235-dirty-checking-va-ortiqcha-update)
- [23.6 Batch yozuv](#236-batch-yozuv)
- [23.7 Projection: entity kerak bo'lmaganda](#237-projection-entity-kerak-bolmaganda)
- [23.8 Hibernate xulqini o'zgartiradigan nozik annotatsiyalar](#238-hibernate-xulqini-ozgartiradigan-nozik-annotatsiyalar)
- [23.9 Entity hayot sikli va detached holat](#239-entity-hayot-sikli-va-detached-holat)
- [23.10 Review checklisti: JPA](#2310-review-checklisti-jpa)
- [23.11 Amalda qo'llash](#2311-amalda-qollash)

</details>


JPA ning xavfi shundaki, u yozgan SQL ni ko'rsatmaydi. Diffda bitta annotatsiya o'zgaradi, prodda esa so'rovlar soni yuzga ko'payadi. Shu sababli JPA kodini review qilish bitta malakani talab qiladi: annotatsiyadan SQL ni tiklab ko'rish. Hibernate ichki mexanikasi (dirty checking, flush tartibi, ikkinchi daraja kesh) [Arxitektor miyasi](../architect/README.md) da; bu yerda diffdan so'rovlar sonini baholash.

## 23.1 N+1: diffdan ko'rish

N+1 ning belgisi diffda uchta shaklda ko'rinadi: yangi lazy maydonga sikl ichida tegish, DTO mapping ichida bog'liq obyektni o'qish, va `toString`/serializatsiya orqali tasodifiy yuklash.

```java
// Belgi 1: sikl ichida lazy kolleksiyaga tegish.
List<Order> orders = repository.findByStatus(OPEN);        // 1 so'rov
for (Order o : orders) {
    total = total.add(o.getLines().stream()                // har buyurtmaga 1 so'rov
                       .map(OrderLine::getAmount).reduce(ZERO, Money::plus));
}
// 500 buyurtma = 501 so'rov. Har biri 1 ms bo'lsa ham, 500 ms.

// Yechim 1: JOIN FETCH - bitta so'rov.
@Query("select distinct o from Order o join fetch o.lines where o.status = :s")
List<Order> findByStatusWithLines(@Param("s") OrderStatus status);
// Diqqat: JOIN FETCH va pagination birga ishlamaydi - Hibernate hamma
// qatorni xotiraga olib, keyin sahifalaydi (HHH000104 ogohlantirishi).

// Yechim 2: @EntityGraph - deklarativ, pagination bilan ham ishlaydi
// (lekin Hibernate ikkinchi so'rov bilan to'ldiradi).
@EntityGraph(attributePaths = { "lines", "customer" })
List<Order> findByStatus(OrderStatus status);

// Yechim 3 (eng tezi): agregatni SQL da hisoblash, entity yuklamaslik.
@Query("""
    select new com.acme.order.OrderTotal(o.id, sum(l.amount))
      from Order o join o.lines l
     where o.status = :s
     group by o.id
    """)
List<OrderTotal> totalsByStatus(@Param("s") OrderStatus status);
```

```yaml
# N+1 ni test va lokal ishga tushirishda ko'rinadigan qilish.
spring:
  jpa:
    properties:
      hibernate:
        generate_statistics: true           # so'rovlar soni logga chiqadi
    open-in-view: false                     # lazy xatolari darhol ko'rinadi
logging:
  level:
    org.hibernate.SQL: debug
    org.hibernate.orm.jdbc.bind: trace      # parametr qiymatlari
```

## 23.2 So'rovlar sonini test bilan qulflash

Review izohida "N+1 bor" degan gapni dalil bilan quvvatlash va kelajakda regressiyani oldini olish usuli - so'rovlar sonini test bilan belgilash.

```java
// So'rov sonini tekshiradigan test: review ning eng kuchli argumenti.
@SpringBootTest
@AutoConfigureTestDatabase(replace = NONE)
class OrderQueryCountTest {

    @Autowired OrderService service;
    @Autowired EntityManagerFactory emf;

    @Test
    void listingOrdersUsesConstantQueryCount() {
        Statistics stats = emf.unwrap(SessionFactory.class).getStatistics();
        stats.clear();

        service.openOrdersWithTotals();      // 500 buyurtma bor

        // Niyat: so'rovlar soni ma'lumot hajmiga bog'liq bo'lmasin.
        assertThat(stats.getPrepareStatementCount())
            .as("so'rovlar soni")
            .isLessThanOrEqualTo(3);
    }
}
// Alternativa: datasource-proxy yoki QuickPerf kutubxonasi
// (@ExpectSelect(3) annotatsiyasi bilan).
```

## 23.3 Fetch strategiyasi

| Annotatsiya | Standart fetch | Review talabi |
| --- | --- | --- |
| `@ManyToOne` | EAGER | Deyarli har doim `LAZY` qilish kerak |
| `@OneToOne` | EAGER | `LAZY` + `optional = false` |
| `@OneToMany` | LAZY | To'g'ri standart, `JOIN FETCH` bilan ishlatish |
| `@ManyToMany` | LAZY | Ko'pincha alohida entity ga ajratish kerak |
| `@ElementCollection` | LAZY | Kichik to'plamlar uchun |

```java
// Eng ko'p uchraydigan muammo: @ManyToOne standart EAGER.
@Entity
public class OrderLine {
    @ManyToOne                               // EAGER: har OrderLine bilan Product yuklanadi
    private Product product;

    @ManyToOne(fetch = FetchType.LAZY)       // to'g'ri
    @JoinColumn(name = "product_id", nullable = false)
    private Product product;
}
// Oqibati: 1000 qatorli buyurtma yuklanganda 1000 Product ham yuklanadi,
// ularning har birida yana EAGER bog'liqlik bo'lsa - zanjir bo'ylab
// butun baza xotiraga tortiladi.

// Diqqat: LAZY @ManyToOne bilan `line.getProduct().getId()` ham so'rov
// yuboradi (agar proxy bo'lmasa). ID kerak bo'lsa, uni alohida ustun
// sifatida saqlash foydali:
@Column(name = "product_id", insertable = false, updatable = false)
private UUID productId;                      // so'rovsiz ID
```

## 23.4 Cascade va orphan removal

```java
// Xavfli: cascade = ALL mijozdan buyurtmaga.
@OneToMany(mappedBy = "customer", cascade = CascadeType.ALL, orphanRemoval = true)
private List<Order> orders;
// Oqibati: customers.delete(customer) butun buyurtma tarixini o'chiradi.
// Buxgalteriya va audit nuqtai nazaridan bu deyarli har doim xato.
// Bundan tashqari kolleksiyadan element olib tashlash uni DB dan o'chiradi -
// bu kutilmagan xulq bo'lishi mumkin.

// Review savollari har bir cascade uchun:
// 1) Ota obyekt o'chirilganda bola haqiqatan o'chirilishi kerakmi?
// 2) Yoki bu agregat chegarasi xato qo'yilganmi (13.3)?
// 3) `ON DELETE` qoidasi DB da ham mosmi (FK)?

// Mos shakl: haqiqiy agregat ichidagi qatorlar uchun.
@Entity
public class Order {
    @OneToMany(mappedBy = "order", cascade = CascadeType.ALL, orphanRemoval = true)
    private List<OrderLine> lines;           // qatorlar buyurtmasiz mavjud emas
}
```

## 23.5 Dirty checking va ortiqcha UPDATE

```java
// Naqsh: o'qish metodida tasodifiy yozuv.
@Transactional                               // readOnly yo'q!
public List<OrderView> list() {
    List<Order> orders = repository.findAll();
    orders.forEach(o -> o.setLastViewedAt(now()));    // har o'qishda UPDATE!
    return orders.stream().map(OrderView::from).toList();
}
// Oqibati: ro'yxatni ochish 500 UPDATE yuboradi, replikatsiya lag o'sadi,
// va `updated_at` triggerlari ishga tushadi.

// Naqsh: entity ni o'zgartirmasdan ham UPDATE chiqishi.
// Sabab: mutable tur (Date, kolleksiya) yoki noto'g'ri equals/hashCode,
// yoki AttributeConverter har flush da boshqa natija berishi.
// Tekshirish: hibernate.generate_statistics va EntityUpdateCount.

// Review qoidasi: o'qish metodlari @Transactional(readOnly = true) bilan -
// Hibernate dirty checking qilmaydi va tasodifiy UPDATE chiqmaydi.
```

## 23.6 Batch yozuv

```java
// Naqsh: 10 000 qatorni bitta-bitta saqlash.
for (Row row : rows) { repository.save(toEntity(row)); }     // 10 000 INSERT

// To'g'ri: batch yozuv sozlangan va tartib buzilmagan.
```

```yaml
spring:
  jpa:
    properties:
      hibernate:
        jdbc.batch_size: 50
        order_inserts: true              # bir xil jadval INSERT lari guruhlanadi
        order_updates: true
        batch_versioned_data: true       # @Version bilan ham batch ishlaydi
  datasource:
    hikari:
      data-source-properties:
        reWriteBatchedInserts: true      # PostgreSQL JDBC: multi-row INSERT
```

```java
// Diqqat: batch IDENTITY generatsiyasi bilan ISHLAMAYDI - Hibernate har
// INSERT dan keyin ID ni olishi kerak.
@Id @GeneratedValue(strategy = GenerationType.IDENTITY)      // batch o'chadi
private Long id;

// Batch ishlashi uchun: SEQUENCE + allocationSize yoki UUID.
@Id
@GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "order_seq")
@SequenceGenerator(name = "order_seq", sequenceName = "order_seq", allocationSize = 50)
private Long id;
// Review izohi: allocationSize DB sequence ning INCREMENT BY bilan mos
// bo'lishi shart, aks holda ID konfliktlari bo'ladi.

// Katta import uchun esa Hibernate umuman kerak emas:
jdbcTemplate.batchUpdate(
    "INSERT INTO import_row (id, payload) VALUES (?, ?::jsonb)",
    rows, 500, (ps, row) -> { ps.setObject(1, row.id()); ps.setString(2, row.json()); });
// Yoki eng tez yo'l - PostgreSQL COPY (millionlab qator uchun).
```

## 23.7 Projection: entity kerak bo'lmaganda

```java
// Naqsh: ro'yxat uchun to'liq entity yuklanadi.
List<Order> orders = repository.findByStatus(OPEN);   // 40 ustun, lazy proxy lar
return orders.stream().map(o -> new OrderRow(o.getId(), o.getNumber())).toList();

// To'g'ri: faqat kerakli ustunlar o'qiladi.
// Variant 1: interfeys projection (Spring Data o'zi amalga oshiradi).
public interface OrderRow {
    UUID getId();
    String getNumber();
    BigDecimal getTotal();
}
List<OrderRow> findByStatus(OrderStatus status);

// Variant 2: record + konstruktor ifodasi (aniqroq va tipli).
@Query("select new com.acme.order.OrderRow(o.id, o.number, o.total) from Order o where o.status = :s")
List<OrderRow> rowsByStatus(@Param("s") OrderStatus status);

// Variant 3: murakkab hisob uchun - JdbcClient, entity umuman yo'q.
List<OrderRow> rows = jdbcClient.sql("""
        SELECT o.id, o.number, o.total,
               count(l.id) AS line_count
          FROM orders o LEFT JOIN order_line l ON l.order_id = o.id
         WHERE o.status = :status
         GROUP BY o.id, o.number, o.total
         ORDER BY o.created_at DESC
         LIMIT 100
        """)
    .param("status", status.name())
    .query(OrderRow.class)
    .list();
```

Review qoidasi: ma'lumot o'zgartirilmasa, entity kerak emas. Projection kamroq ustun o'qiydi, dirty checking qilmaydi, birinchi daraja keshni to'ldirmaydi va lazy xatolaridan xoli.

## 23.8 Hibernate xulqini o'zgartiradigan nozik annotatsiyalar

| Annotatsiya | Ta'siri | Review diqqati |
| --- | --- | --- |
| `@DynamicUpdate` | Faqat o'zgargan ustunlar yangilanadi | Har flush da SQL qayta quriladi (narx); keng jadvalda foydali |
| `@Immutable` | O'zgarishlar e'tiborsiz qoldiriladi | Jim ishlamaydigan `set` lar |
| `@NaturalId` | Tabiiy kalit bo'yicha kesh | Kalit o'zgarmasligi kafolatlanganmi |
| `@BatchSize` | Lazy yuklashni guruhlash | N+1 ni N/batch ga kamaytiradi |
| `@Formula` | Hisoblangan maydon SQL da | Har o'qishda hisob, indekssiz |
| `@Where` | Global filtr | Jim yashirin shart - juda xavfli |
| `@SQLDelete` | Yumshoq o'chirish | O'chirilgan qatorlar hamma joyda filtrlanadimi |
| `@Cacheable` (2-daraja) | Klaster bo'ylab kesh | Invalidatsiya, klasterda mos kelish |
| `@LazyCollection(EXTRA)` | `size()` uchun alohida so'rov | Ko'pincha noto'g'ri qo'llanadi |
| `@OrderBy` vs `@OrderColumn` | SQL tartibi vs saqlangan indeks | `@OrderColumn` qo'shimcha UPDATE lar beradi |

```java
// @Where - eng xavfli: shart hamma so'rovga jim qo'shiladi.
@Entity
@Where(clause = "deleted = false")
public class Customer { }
// Oqibati: (1) o'chirilgan mijozni hech qanday so'rov bilan ola olmaysiz
// (hatto admin paneldan ham); (2) native so'rovlarga bu shart qo'shilmaydi,
// shuning uchun JPQL va SQL natijalari farq qiladi; (3) JOIN larda
// kutilmagan natija. Review tavsiyasi: shartni aniq so'rovlarda yozish.
```

## 23.9 Entity hayot sikli va detached holat

```java
// Naqsh: detached entity ni saqlash - jim ustun yo'qotilishi.
public void update(OrderDto dto) {
    Order order = new Order();               // detached, hamma maydon null
    order.setId(dto.id());
    order.setComment(dto.comment());
    repository.save(order);                  // merge: boshqa maydonlar null bo'ladi!
}
// Oqibati: `total`, `status`, `created_at` null ga yoziladi yoki NOT NULL
// xatosi chiqadi. Bu ma'lumot yo'qotishning klassik yo'li.

// To'g'ri: yuklash, o'zgartirish, tranzaksiya commit i bilan saqlash.
@Transactional
public void update(OrderDto dto) {
    Order order = repository.findById(dto.id()).orElseThrow(OrderNotFound::new);
    order.changeComment(dto.comment());      // domen metodi
    // save() chaqirish shart emas: boshqarilayotgan entity avtomatik flush bo'ladi.
}
```

## 23.10 Review checklisti: JPA

| Savol | Nega |
| --- | --- |
| Yangi lazy maydonga sikl ichida tegilmaydimi | N+1 |
| `@ManyToOne` LAZY qilinganmi | Yashirin EAGER zanjiri |
| `JOIN FETCH` pagination bilan ishlatilmaganmi | Xotirada sahifalash |
| O'qish metodlari `readOnly` mi | Tasodifiy UPDATE |
| `cascade = ALL` oqibati baholanganmi | Ma'lumot yo'qolishi |
| Batch sozlangan va IDENTITY ishlatilmaganmi | Sekin import |
| Ro'yxat uchun projection ishlatilganmi | Ortiqcha ustun va xotira |
| Detached entity `save` qilinmaydimi | Maydon yo'qolishi |
| `@Where`, `@SQLDelete` kabi global filtrlar bormi | Jim yashirin shart |
| Katta natijalar oqim yoki bo'lak bilan o'qiladimi | OOM |
| `@Version` kerakli joyda bormi | Yo'qolgan yangilanish |
| So'rov soni test bilan qulflangangmi | Regressiya |

## 23.11 Amalda qo'llash

- [ ] `hibernate.generate_statistics` ni test profilida yoqib, asosiy endpointlar uchun so'rov sonini o'lchang.
- [ ] Eng muhim uchta ro'yxat endpointi uchun so'rov sonini qulflaydigan test yozing.
- [ ] Barcha `@ManyToOne` va `@OneToOne` larni toping va `fetch = LAZY` qo'yilganini tasdiqlang.
- [ ] `spring.jpa.open-in-view=false` qilib, chiqadigan `LazyInitializationException` larni DTO yoki `JOIN FETCH` bilan tuzating.
- [ ] `cascade = ALL` va `orphanRemoval = true` ishlatilgan joylarni ko'rib, agregat chegarasini qayta baholang.
- [ ] Batch sozlamalarini (`batch_size`, `order_inserts`, `reWriteBatchedInserts`) qo'shing va `IDENTITY` ishlatadigan entity larni sequence ga o'tkazishni rejalashtiring.
- [ ] Ro'yxat qaytaradigan so'rovlarni projection ga o'tkazib, o'qilayotgan ustun sonini kamaytiring.
- [ ] `@Where` va `@SQLDelete` ishlatilgan joylarni aniq so'rov shartlariga o'tkazishni ko'rib chiqing.
- [ ] `new Entity()` + `setId()` + `save()` naqshini grep bilan topib, barchasini tuzating.

---

[&larr; 22. Tashqi integratsiya review: timeout, retry, broker](22-tashqi-integratsiya-review-timeout-retry.md) · [Mundarija](README.md) · [24. SQL, so'rov rejasi va indeks review &rarr;](24-sql-sorov-rejasi-va-indeks-review.md)
