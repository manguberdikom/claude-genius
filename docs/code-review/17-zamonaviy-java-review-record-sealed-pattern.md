<!-- doc: code-review | chapter: 17 | part: III. Java kodini chuqur tahlil -->

[Kod review](../../README.md) / [Kod review](README.md)

# 17. Zamonaviy Java review: record, sealed, pattern matching, virtual thread (Modern Java)

<details>
<summary>Bu bobdagi 8 bo'lim</summary>

- [17.1 record: qachon to'g'ri, qachon noto'g'ri](#171-record-qachon-togri-qachon-notogri)
- [17.2 sealed: to'liqlikni kompilyatorga topshirish](#172-sealed-toliqlikni-kompilyatorga-topshirish)
- [17.3 Pattern matching: shoxlanishni qisqartirish, lekin yashirmaslik](#173-pattern-matching-shoxlanishni-qisqartirish-lekin-yashirmaslik)
- [17.4 Virtual threadlar: diffdagi bitta qator, tizimdagi katta o'zgarish](#174-virtual-threadlar-diffdagi-bitta-qator-tizimdagi-katta-ozgarish)
- [17.5 Text block va SQL](#175-text-block-va-sql)
- [17.6 `var`: qachon o'qishni osonlashtiradi](#176-var-qachon-oqishni-osonlashtiradi)
- [17.7 Yangi imkoniyatlarni qabul qilish siyosati](#177-yangi-imkoniyatlarni-qabul-qilish-siyosati)
- [17.8 Amalda qo'llash](#178-amalda-qollash)

</details>


Yangi til imkoniyatlari review ga ikki xil ta'sir qiladi. Biri foydali: `record` va `sealed` xatolarni kompilyatsiyaga ko'chiradi, ya'ni reviewer ularni tekshirishdan ozod bo'ladi. Ikkinchisi xavfli: yangi imkoniyat noto'g'ri joyda ishlatilsa, muammo ko'rinmas bo'ladi. Bu bob har ikki tomonni ko'radi.

## 17.1 record: qachon to'g'ri, qachon noto'g'ri

```java
// To'g'ri ishlatilish: immutable qiymat, tenglik qiymat bo'yicha.
public record Money(BigDecimal amount, Currency currency) { }        // value object
public record PlaceOrder(CustomerId customer, List<LineItem> lines) { }  // command
public record OrderView(UUID id, String number, String total) { }    // o'qish modeli

// Noto'g'ri: JPA entity. Record maydonlari final, no-arg konstruktor yo'q,
// proxy yaratilmaydi - Hibernate buni boshqara olmaydi.
public record Order(Long id, String number) { }                      // entity emas

// Diqqat 1: record "sayoz" immutable. Kolleksiya ichi o'zgarishi mumkin.
public record Basket(List<Item> items) {
    public Basket {
        items = List.copyOf(items);          // nusxa olish majburiy
    }
    // Aks holda: tashqaridagi ro'yxatga element qo'shilsa, Basket o'zgaradi.
}

// Diqqat 2: record ichida validatsiya - kompakt konstruktor.
public record Quantity(int value) {
    public Quantity {
        if (value <= 0) throw new IllegalArgumentException("qiymat musbat bo'lsin");
    }
}

// Diqqat 3: record ning equals i hamma maydonni oladi. Agar maydonlardan
// biri array bo'lsa - havola taqqoslanadi (14.2).
public record Payload(byte[] data) { }       // equals ishlamaydi, review da e'tibor
```

## 17.2 sealed: to'liqlikni kompilyatorga topshirish

`sealed` review ning ishini kamaytiradigan eng foydali imkoniyat: yangi holat qo'shilganda barcha `switch` lar kompilyatsiyada xato beradi, ya'ni reviewer "hamma joy yangilandimi" savolini bermasa ham bo'ladi.

```java
// Natija turini sealed qilish: chaqiruvchi hamma holatni ko'rishga majbur.
public sealed interface TransferResult {
    record Completed(TransactionId id, Instant at) implements TransferResult { }
    record Rejected(RejectReason reason) implements TransferResult { }
    record RequiresApproval(ApprovalId id, Money threshold) implements TransferResult { }
}

// Chaqiruvchi tomonda: default yo'q, kompilyator to'liqlikni ta'minlaydi.
ResponseEntity<?> response = switch (transfers.execute(cmd)) {
    case Completed c -> ResponseEntity.ok(new TransferResponse(c.id(), c.at()));
    case Rejected r  -> ResponseEntity.unprocessableEntity().body(problem(r.reason()));
    case RequiresApproval a -> ResponseEntity.accepted()
            .body(new ApprovalRequired(a.id(), a.threshold()));
};
// Review foydasi: yangi holat (masalan Pending) qo'shilsa, bu switch
// kompilyatsiya bo'lmaydi. Istisnolar bilan qilingan dizaynda bu
// kafolat yo'q - yangi istisno turini hech kim ushlamasligi mumkin.
```

Review savoli: natija "muvaffaqiyat yoki istisno" shaklida yetarli ifodalanadimi. Biznes rad etishi (karta rad etildi, limit oshdi) istisno emas - bu normal natija, va `sealed` bilan ifodalanishi yaxshiroq. Istisno esa kutilmagan holatlar uchun qoladi.

## 17.3 Pattern matching: shoxlanishni qisqartirish, lekin yashirmaslik

```java
// Foydali: tur tekshiruvi va ajratish bir qadamda.
if (event instanceof OrderPaid paid && paid.total().isGreaterThan(LIMIT)) {
    review.flag(paid.orderId());
}

// Record pattern bilan ichki qiymatni olish.
switch (command) {
    case PlaceOrder(CustomerId customer, List<LineItem> lines) when lines.isEmpty() ->
        throw new EmptyOrder();
    case PlaceOrder(CustomerId customer, List<LineItem> lines) ->
        orders.place(customer, lines);
    case CancelOrder(OrderId id, String reason) ->
        orders.cancel(id, reason);
}

// Review diqqati: `when` shartlari ko'payib ketsa, bu yashirin biznes
// qoidalari to'planishi. Uch-to'rtdan ko'p `when` bo'lsa, qoidalar
// domen obyektiga ko'chirilishi kerak - aks holda qoida `switch` ichida
// yashiringan bo'ladi va test qilish qiyin.
```

## 17.4 Virtual threadlar: diffdagi bitta qator, tizimdagi katta o'zgarish

```properties
# Bitta qator butun ijro modelini o'zgartiradi.
spring.threads.virtual.enabled=true
```

Review da shu qator uchun to'rt savol beriladi:

1. DB pool qayta hisoblanganmi. Virtual threadlar cheksiz, lekin Hikari pool emas: 10 000 so'rov 20 ta ulanishni kutadi. Navbat va `connection-timeout` yangi sharoitda qayta ko'riladi.
2. `synchronized` bilan uzoq bloklanish bormi (15.10 dagi pinning).
3. `ThreadLocal` ga tayangan kesh bormi - endi foyda bermaydi.
4. Tashqi servislar bu yukni ko'taradimi. Virtual threadlar sizning ilovangizni tez qiladi, keyingi servisni esa yuk bilan ko'madi - rate limit va bulkhead kerak.

```java
// Strukturali konkurentlik (Java 21+ preview/22+): parallel chaqiruvlarni
// bitta hayot sikli bilan boshqarish. Review da afzal ko'riladi, chunki
// xato va bekor qilish aniq.
public OrderPage load(OrderId id) throws InterruptedException {
    try (var scope = new StructuredTaskScope.ShutdownOnFailure()) {
        Subtask<Order> order = scope.fork(() -> orders.byId(id));
        Subtask<List<Shipment>> ships = scope.fork(() -> shipments.forOrder(id));
        Subtask<Invoice> invoice = scope.fork(() -> invoices.forOrder(id));

        scope.joinUntil(Instant.now().plusSeconds(2));   // umumiy deadline
        scope.throwIfFailed(OrderPageFailed::new);        // biri yiqilsa - hammasi

        return new OrderPage(order.get(), ships.get(), invoice.get());
    }
}
// Qiyoslash: uchta CompletableFuture bilan yozilganda timeout har biriga
// alohida, bekor qilish qo'lda, va bitta xato qolganlarini to'xtatmaydi.
```

## 17.5 Text block va SQL

```java
// Text block SQL ni o'qiladigan qiladi, lekin injection xavfini
// o'zgartirmaydi. Review da shu farq muhim.
String sql = """
    SELECT o.id, o.number, o.total
      FROM orders o
     WHERE o.customer_id = ?
       AND o.created_at >= ?
     ORDER BY o.created_at DESC
     LIMIT 100
    """;                                    // parametrlar bilan - xavfsiz

// Xavfli variant text block da ham xuddi shunday xavfli:
String sql = """
    SELECT * FROM orders ORDER BY %s
    """.formatted(sortBy);                  // injection ([29-bob](29-injection-review-sql-va-boshqalar.md))
```

## 17.6 `var`: qachon o'qishni osonlashtiradi

```java
// Foydali: tur o'ng tomondan aniq ko'rinadi.
var orders = new ArrayList<Order>();
var entry = Map.entry(key, value);

// Zararli: tur ko'rinmaydi va o'qiyotgan odam IDE siz tushunmaydi.
var result = service.process(input);        // nima qaytdi?
var x = compute();                          // Optional? List? int?

// Review mezoni: diffni brauzerda o'qiyotgan odam turni bila oladimi.
// Bila olmasa - aniq tur yoziladi.
```

## 17.7 Yangi imkoniyatlarni qabul qilish siyosati

Review da takrorlanadigan bahsni oldini olish uchun jamoa yangi imkoniyatlar bo'yicha pozitsiyani yozib qo'yishi kerak.

```markdown
<!-- REVIEW.md ichida: til imkoniyatlari bo'yicha pozitsiya -->
## Til imkoniyatlari

| Imkoniyat | Pozitsiya |
|---|---|
| `record` | DTO, command, event, value object uchun standart. Entity uchun emas. |
| `sealed` | Natija turlari va domen holatlari uchun afzal. |
| Pattern matching `switch` | `instanceof` zanjiri o'rniga afzal. 4+ `when` bo'lsa - domenga ko'chirish. |
| `var` | Tur o'ng tomonda ko'rinsa - ha. Metod natijasida - yo'q. |
| Text block | SQL va JSON uchun standart. |
| Virtual threads | Yoqilgan. `synchronized` uzoq bloklash taqiqlanadi. |
| `Optional` | Qaytish turi sifatida. Maydon va parametr sifatida emas. |
| Stream `parallel()` | Faqat o'lchangan dalil bilan, bloklanmaydigan ish uchun. |
```

## 17.8 Amalda qo'llash

- [ ] `REVIEW.md` ga til imkoniyatlari pozitsiyasi jadvalini qo'shib, takrorlanadigan bahslarni to'xtating.
- [ ] Kolleksiya maydoni bo'lgan `record` larni toping va kompakt konstruktorda `List.copyOf` qilinganini tekshiring.
- [ ] Istisno bilan ifodalangan biznes rad etishlarini aniqlab, ularni `sealed` natija turiga o'tkazish variantini baholang.
- [ ] `default` bilan tugaydigan enum `switch` larini `sealed` yoki to'liq `switch` ga o'tkazing.
- [ ] `spring.threads.virtual.enabled=true` yoqilgan bo'lsa, Hikari pool va timeout qiymatlarini yuk sinovi bilan qayta tekshiring.
- [ ] `var` ishlatilgan joylarni ko'rib, metod natijasida turi ko'rinmaydiganlarni aniq turga o'tkazing.
- [ ] Parallel tashqi chaqiruvlarni `StructuredTaskScope` yoki umumiy deadline bilan qayta yozishni rejalashtiring.

---

[&larr; 16. Resurs, xotira va GC bosimi review](16-resurs-xotira-va-gc-bosimi-review.md) · [Mundarija](README.md) · [18. Bean, kontekst va proxy mexanikasi review &rarr;](18-bean-kontekst-va-proxy-mexanikasi-review.md)
