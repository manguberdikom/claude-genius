<!-- doc: code-review | chapter: 34 | part: VII. Test review -->

[Barcha hujjatlar](../../README.md) / [Kod review](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 34. Test to'liqligini review qilish (Test Case Completeness)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

- [34.1 To'g'ri savol: qaysi holat qamralmagan](#341-togri-savol-qaysi-holat-qamralmagan)
- [34.2 Chegaraviy qiymatlar: eng ko'p qaytim beradigan test holatlari](#342-chegaraviy-qiymatlar-eng-kop-qaytim-beradigan-test-holatlari)
- [34.3 Shartlar kombinatsiyasi: qaror jadvali](#343-shartlar-kombinatsiyasi-qaror-jadvali)
- [34.4 Holat o'tish matritsasi](#344-holat-otish-matritsasi)
- [34.5 Xato yo'llari: eng ko'p qamralmay qoladigan qism](#345-xato-yollari-eng-kop-qamralmay-qoladigan-qism)
- [34.6 Konkurentlik va idempotentlik testlari](#346-konkurentlik-va-idempotentlik-testlari)
- [34.7 Mutatsion fikrlash: testni aldab o'tish mumkinmi](#347-mutatsion-fikrlash-testni-aldab-otish-mumkinmi)
- [34.8 Ma'lumotga bog'liq holatlar](#348-malumotga-bogliq-holatlar)
- [34.9 Yetishmayotgan holatni review izohida ko'rsatish](#349-yetishmayotgan-holatni-review-izohida-korsatish)
- [34.10 Review checklisti: test to'liqligi](#3410-review-checklisti-test-toliqligi)
- [34.11 Amalda qo'llash](#3411-amalda-qollash)

</details>


Review ning eng kam bajariladigan qismi - testlarni jiddiy o'qish. Ko'pincha reviewer "test bor" degan faktga qaraydi va mazmunini o'qimaydi. Natijada yolg'on ishonch paydo bo'ladi: coverage 85 foiz, lekin eng xavfli holatlar qamralmagan. Bu bob testlar to'liqligini tizimli baholashni beradi - qamrov foizini emas, holatlar to'plamini tekshirish. Test yozish texnikasi va test piramidasi [Testlash qo'llanmasi](../testing/README.md) da; bu yerda faqat review nuqtai nazari.

## 34.1 To'g'ri savol: qaysi holat qamralmagan

Coverage "bu satr bajarildimi" degan savolga javob beradi. Review esa boshqa savolni beradi: "qaysi kirish uchun bu kod noto'g'ri ishlaydi va test buni tutadimi". Ikkinchi savolga javob berish uchun tizimli usul kerak, aks holda reviewer faqat o'zi o'ylab topgan holatlarni so'raydi.

Usul to'rt qadamdan iborat:

1. Kirishlarni ekvivalentlik sinflariga bo'lish.
2. Har sinf uchun chegaralarni topish.
3. Shartlar kombinatsiyasini jadvalga yozish.
4. Xato yo'llari va holat o'tishlarini sanash.

```java
// Review qilinayotgan kod: chegirma hisobi.
public Money discountFor(Order order, Customer customer, LocalDate on) {
    if (order.total().isLessThan(MIN_TOTAL)) return Money.ZERO;      // 1
    BigDecimal rate = customer.tier().discountRate();                 // 2
    if (customer.registeredBefore(on.minusYears(1))) {                // 3
        rate = rate.add(LOYALTY_BONUS);
    }
    if (rate.compareTo(MAX_RATE) > 0) rate = MAX_RATE;                // 4
    return order.total().multiply(rate);
}
```

Shu 6 satr uchun holatlar to'plami:

| Sinf | Holatlar |
| --- | --- |
| `order.total` | `MIN_TOTAL` dan past, aynan `MIN_TOTAL`, yuqori, nol, manfiy(?), juda katta |
| `customer.tier` | Har bir enum qiymati (hammasi) |
| Ro'yxatdan o'tish sanasi | Bir yildan kam, aynan bir yil, ko'p, kelasi sana(?) |
| Natija chegarasi | `MAX_RATE` dan past, aynan, undan yuqori (kesiladi) |
| `on` | Bugun, o'tgan, kelasi |
| Null lar | `order`, `customer`, `on` null bo'lsa |

Bu 6 ta `if` uchun kamida 12-15 ta test holati. Agar PR da 2 ta test bo'lsa, review izohi aniq bo'ladi: "aynan `MIN_TOTAL` chegarasi va `MAX_RATE` kesilishi qamralmagan - ikkisi ham bitta `>` yoki `>=` xatosi bilan buziladi".

## 34.2 Chegaraviy qiymatlar: eng ko'p qaytim beradigan test holatlari

Xatolarning katta qismi chegaralarda yashaydi, chunki `<` va `<=` farqi eng ko'p qilinadigan xato. Shu sababli har bir sonli yoki tartibli shart uchun uch nuqta tekshiriladi: chegaradan bir past, aynan chegara, bir yuqori.

| Kirish turi | Tekshirilishi kerak bo'lgan qiymatlar |
| --- | --- |
| Butun son | 0, 1, -1, chegara, chegara ± 1, `MIN_VALUE`, `MAX_VALUE` |
| Pul | 0, eng kichik birlik (0.01), chegara, manfiy, juda katta |
| Satr | bo'sh, bitta belgi, maksimal uzunlik, maksimal + 1, bo'sh joy, unicode, emoji |
| Ro'yxat | bo'sh, bitta element, maksimal, maksimal + 1 |
| Sana | bugun, kecha, ertaga, chegara sana, 29-fevral, yil oxiri, yozgi vaqt o'tishi |
| Vaqt oralig'i | nol davomiylik, teskari (oxiri boshidan oldin), bir xil |
| Enum | har bir qiymat, va "yangi qiymat qo'shilsa" holati |
| Optional/null | mavjud, bo'sh, null |

```java
// To'g'ri shakl: chegaralar jadval sifatida, o'qiladigan nomlar bilan.
@ParameterizedTest(name = "{0} so'm, {1} -> {2} so'm chegirma")
@CsvSource({
    //  summa,     daraja,  kutilgan
    "  99999.99,  GOLD,     0.00",     // chegaradan bir tiyin past
    " 100000.00,  GOLD, 15000.00",     // AYNAN chegara
    " 100000.01,  GOLD, 15000.00",     // chegaradan bir tiyin yuqori
    "      0.00,  GOLD,     0.00",     // nol
    " 100000.00,  BRONZE,   0.00",     // chegirmasiz daraja
    "1000000.00,  GOLD, 150000.00"     // katta summa
})
void discountAtBoundaries(BigDecimal total, CustomerTier tier, BigDecimal expected) {
    Order order = order(total);
    Customer customer = customer(tier, registeredAt(LAST_MONTH));
    assertThat(calculator.discountFor(order, customer, TODAY))
        .isEqualByComparingTo(expected);
}

// Enum to'liqligi: yangi qiymat qo'shilsa test yiqiladi.
@ParameterizedTest
@EnumSource(CustomerTier.class)
void everyTierHasDefinedDiscount(CustomerTier tier) {
    Money result = calculator.discountFor(order(BIG_TOTAL), customer(tier), TODAY);
    assertThat(result).isNotNull();
    assertThat(result.amount()).isBetween(ZERO, BIG_TOTAL.amount());
}
```

## 34.3 Shartlar kombinatsiyasi: qaror jadvali

Ikki yoki uchdan ko'p shart birgalikda qarorga ta'sir qilsa, holatlarni bitta-bitta sanash xato: kombinatsiyalar o'tkazib yuboriladi. Qaror jadvali bu muammoni yechadi.

```text
Qoida: buyurtma bekor qilinishi mumkinmi?
Shartlar: (A) status NEW yoki PAID, (B) jo'natilmagan, (C) 24 soat ichida

| A | B | C | Natija        | Test bormi |
|---|---|---|---------------|------------|
| T | T | T | Bekor qilinadi| ha         |
| T | T | F | Rad etiladi   | YO'Q       |  <- review topilmasi
| T | F | T | Rad etiladi   | ha         |
| T | F | F | Rad etiladi   | yo'q (A=T,B=F allaqachon qamralgan) |
| F | T | T | Rad etiladi   | YO'Q       |  <- review topilmasi
| F | * | * | Rad etiladi   | -          |
```

Review izohining shakli: "Bekor qilish uchun uch shart bor, testlarda ulardan ikkitasining kombinatsiyasi yo'q: (status PAID, jo'natilmagan, lekin 24 soatdan keyin) va (status SHIPPED, 24 soat ichida). Ikkinchisi ayniqsa muhim - u mijoz jo'natilgan buyurtmani bekor qilishiga yo'l qo'ymaslik kerakligini tekshiradi."

```java
// Qaror jadvalini testda ifodalash.
@ParameterizedTest(name = "status={0}, shipped={1}, hours={2} -> {3}")
@CsvSource({
    "NEW,       false,  1, true",
    "PAID,      false,  1, true",
    "PAID,      false, 25, false",      // vaqt o'tgan
    "PAID,      true,   1, false",      // jo'natilgan
    "SHIPPED,   true,   1, false",
    "DELIVERED, true,   1, false",
    "CANCELLED, false,  1, false"       // allaqachon bekor
})
void cancellationRules(OrderStatus status, boolean shipped, int hoursAgo, boolean expected) {
    Order order = orderWith(status, shipped, clock.instant().minus(hoursAgo, HOURS));
    assertThat(order.isCancellable(clock.instant())).isEqualTo(expected);
}
```

## 34.4 Holat o'tish matritsasi

Holat mashinasi bo'lgan domen (buyurtma, to'lov, obuna) uchun to'liqlik mezoni aniq: har bir o'tish ruxsat etilgan yoki taqiqlangan ekani tekshiriladi. N holatda N x N kombinatsiya bor, va ularning hammasini bitta test bilan qoplash mumkin.

```java
// Butun matritsani bitta testda qoplash: 36 kombinatsiya (6x6).
@ParameterizedTest
@MethodSource("allTransitions")
void transitionMatrix(OrderStatus from, OrderStatus to) {
    Order order = orderInStatus(from);
    boolean allowed = ALLOWED.contains(entry(from, to));   // kutilgan jadval

    if (allowed) {
        assertThatCode(() -> order.transitionTo(to)).doesNotThrowAnyException();
        assertThat(order.status()).isEqualTo(to);
    } else {
        assertThatThrownBy(() -> order.transitionTo(to))
            .isInstanceOf(IllegalStateTransition.class);
        assertThat(order.status()).as("rad etilgan o'tishda holat o'zgarmasin")
                                  .isEqualTo(from);
    }
}

static Stream<Arguments> allTransitions() {
    return Arrays.stream(OrderStatus.values())
        .flatMap(f -> Arrays.stream(OrderStatus.values()).map(t -> arguments(f, t)));
}
// Review foydasi: yangi status qo'shilganda test avtomatik 13 yangi
// kombinatsiyani tekshiradi va `ALLOWED` jadvalini to'ldirishni talab qiladi.
```

## 34.5 Xato yo'llari: eng ko'p qamralmay qoladigan qism

Testlar odatda muvaffaqiyatli yo'lni qoplaydi. Xato yo'llari esa prodda tez-tez bajariladi va ularda xato qilish osonroq, chunki ular kamroq sinaladi.

| Xato yo'li | Tekshirilishi kerak |
| --- | --- |
| Tashqi servis timeout | Qanday istisno, retry, foydalanuvchiga javob |
| Tashqi servis 500 | Fallback ishlaydimi, holat to'g'rimi |
| Tashqi servis noto'g'ri javob | Validatsiya, istisno |
| DB constraint buzilishi | Istisno aylantirilganmi (409) |
| Optimistik qulf konflikti | Foydalanuvchiga tushunarli javob |
| Tranzaksiya rollback | Holat qaytdimi, yon ta'sir qolmadimi |
| Yarim bajarilgan jarayon | Kompensatsiya yoki qayta boshlash |
| Validatsiya xatosi | To'g'ri status va xabar |
| Avtorizatsiya rad etishi | 403/404 va ma'lumot oqmasligi |
| Bo'sh natija | Bo'sh ro'yxat, `Optional.empty()`, 404 |

```java
// Xato yo'lini test qilish: tashqi servis nosozligi.
@Test
void paymentTimeoutLeavesOrderInPendingAndSchedulesRetry() {
    when(gateway.capture(any())).thenThrow(new GatewayTimeout());

    assertThatThrownBy(() -> service.confirm(orderId))
        .isInstanceOf(PaymentPending.class);

    // Eng muhimi: holat nima bo'ldi?
    Order order = orders.findById(orderId).orElseThrow();
    assertThat(order.status()).isEqualTo(CONFIRMING);        // oraliq holat
    assertThat(outbox.pendingFor(orderId)).hasSize(1);       // qayta urinish rejalashtirilgan
    assertThat(order.paidAt()).isNull();                     // to'lanmagan deb belgilanmagan
}
// Review izohi: timeout testi bor, lekin "gateway 500 qaytardi" va
// "gateway noto'g'ri formatda javob berdi" holatlari yo'q. Uchinchisi
// ayniqsa muhim: provayder o'tgan oy `amount` ni satr sifatida
// yuborishni boshlagan edi.
```

## 34.6 Konkurentlik va idempotentlik testlari

Bu holatlar deyarli hech qachon test qilinmaydi, lekin ularni test qilish mumkin va review da so'rash kerak.

```java
// Idempotentlik testi: aniq va oson.
@Test
void sameIdempotencyKeyChargesOnce() {
    PaymentRequest req = request(Money.of(100_000));

    PaymentResponse first = service.charge("key-1", req);
    PaymentResponse second = service.charge("key-1", req);   // takroriy

    assertThat(second).isEqualTo(first);                     // bir xil natija
    verify(gateway, times(1)).charge(any());                 // bir marta chaqirilgan
    assertThat(payments.countByOrder(req.orderId())).isEqualTo(1);
}

// Poyga testi: ikki parallel so'rov.
@Test
void concurrentRegistrationCreatesSingleCustomer() throws Exception {
    String email = "ali@example.com";
    int threads = 8;
    var latch = new CountDownLatch(1);
    var pool = Executors.newFixedThreadPool(threads);
    var results = new ArrayList<Future<?>>();

    for (int i = 0; i < threads; i++) {
        results.add(pool.submit(() -> {
            latch.await();                       // hammasi bir vaqtda boshlansin
            return service.register(email);
        }));
    }
    latch.countDown();

    long ok = 0, conflicts = 0;
    for (Future<?> f : results) {
        try { f.get(); ok++; }
        catch (ExecutionException e) {
            assertThat(e.getCause()).isInstanceOf(EmailAlreadyUsed.class);
            conflicts++;
        }
    }
    assertThat(ok).as("faqat bitta muvaffaqiyat").isEqualTo(1);
    assertThat(conflicts).isEqualTo(threads - 1);
    assertThat(customers.countByEmail(email)).isEqualTo(1);
    pool.shutdown();
}
// Diqqat: bu test haqiqiy PostgreSQL bilan (Testcontainers) ishlashi kerak -
// H2 da unique constraint xulqi farq qiladi ([36-bob](36-test-turi-va-integratsion-test-review.md)).
```

## 34.7 Mutatsion fikrlash: testni aldab o'tish mumkinmi

Eng kuchli review texnikasi: "bu kodni qanday buzsam, testlar hali ham o'tadi" degan savol. Agar javob topilsa, test yetarli emas.

| Mutatsiya | Test tutadimi |
| --- | --- |
| `<` ni `<=` ga almashtirish | Faqat chegara testi bo'lsa |
| Shartni teskari qilish | Ikki tomon testi bo'lsa |
| Qaytish qiymatini `null` qilish | Assertion qiymatni tekshirsa |
| `if` blokini o'chirish | Shart bajarilgan holat testi bo'lsa |
| Arifmetik amalni almashtirish (`+` -> `-`) | Aniq qiymat tekshirilsa |
| Metod chaqiruvini o'chirish | Natija yoki yon ta'sir tekshirilsa |
| Konstantani o'zgartirish (15% -> 25%) | Aniq qiymat tekshirilsa |
| Istisno turini almashtirish | Tur tekshirilsa |

```java
// Review da shu savolni qo'llash: testlar quyidagi mutatsiyalarni tutadimi?
// Kod: if (order.total().isLessThan(MIN_TOTAL)) return Money.ZERO;
//
// Mutatsiya 1: isLessThan -> isLessThanOrEqual
//   Tutish uchun: total = MIN_TOTAL aynan bo'lgan test kerak.
// Mutatsiya 2: return Money.ZERO -> return null
//   Tutish uchun: natija qiymati tekshirilishi kerak (isNotNull yetarli emas,
//   lekin isEqualByComparingTo(ZERO) tutadi).
// Mutatsiya 3: butun `if` ni o'chirish
//   Tutish uchun: MIN_TOTAL dan past summa testi kerak.

// Avtomatlashtirish: PIT (pitest) mutatsion testlashni o'lchaydi.
// mvn org.pitest:pitest-maven:mutationCoverage
// Natija: "mutation score 62%" - ya'ni mutatsiyalarning 38 foizini
// testlar tutmaydi. Bu coverage dan ancha ishonchli ko'rsatkich.
```

PIT butun loyihaga emas, faqat domen va narxlash kabi muhim paketlarga yo'naltiriladi, chunki u sekin ishlaydi, domen uchun `mutationThreshold` esa boshqa paketlardan yuqoriroq qo'yiladi. Plugin sozlamasi [SonarQube hujjatidagi PIT ni Maven va Gradle da ishga tushirish](../sonarqube/20-mutation-testing-100-coverage-qachon-yolgon.md#205-pit-pitest-ni-maven-va-gradle-da-ishga-tushirish) bo'limida.

## 34.8 Ma'lumotga bog'liq holatlar

```java
// Review da so'raladigan ma'lumot holatlari.
// 1) Bo'sh to'plam: ro'yxat bo'sh bo'lsa hisob to'g'rimi?
@Test void totalOfEmptyOrderIsZero() { ... }
// Ko'pincha bu yerda 0 ga bo'lish yoki `get(0)` xatosi chiqadi.

// 2) Bitta element: o'rtacha, mediana, birinchi/oxirgi.
@Test void singleLineOrderTotal() { ... }

// 3) Dublikatlar: bir xil mahsulot ikki marta.
@Test void duplicateProductLinesAreMerged() { ... }

// 4) Katta hajm: chegaralar ishlaydimi.
@Test void orderWithMaxLinesIsRejected() { ... }

// 5) Eski ma'lumot: migratsiyadan oldin yaratilgan qatorlar.
@Test void handlesLegacyRowsWithNullRiskScore() { ... }
// Bu eng ko'p o'tkazib yuboriladigan holat: yangi kod toza ma'lumotda
// ishlaydi, lekin prodda eski shakldagi qatorlar bor (25.3).

// 6) Unicode va maxsus belgilar.
@Test void customerNameWithApostropheAndCyrillic() { ... }
// O'zbek tilidagi ismlar (G'ayrat, O'ktam) apostrof bilan - SQL, JSON,
// CSV va URL da alohida tekshirish talab qiladi.
```

## 34.9 Yetishmayotgan holatni review izohida ko'rsatish

Review izohi "testlar yetarli emas" shaklida bo'lsa, muallif nima qilishni bilmaydi. To'g'ri shakl - aniq holatni va nega muhimligini aytish.

```text
# Yomon shakl.
"Test coverage past, ko'proq test kerak."

# Yaxshi shakl: aniq holat, sabab, kutilgan natija.
suggest (test): discountFor uchun uch holat qamralmagan.

1. total = MIN_TOTAL aynan (100000.00).
   Nega: hozir `isLessThan` ishlatilgan. Agar u `isLessThanOrEqual` ga
   o'zgarsa (yoki teskari), hech bir test buni tutmaydi. Chegirma
   chegarasi biznes uchun aniq raqam - uni qulflash kerak.
   Kutilgan: 15000.00 chegirma.

2. rate MAX_RATE dan oshadigan holat: GOLD (15%) + loyalty (10%) = 25%,
   MAX_RATE = 20%.
   Nega: 4-satrdagi kesish mantiqi hech qachon bajarilmaydi hozirgi
   testlarda. Kutilgan: 20% ga kesiladi.

3. customer.registeredAt aynan bir yil oldin.
   Nega: `registeredBefore` da `<` yoki `<=` farqi. Biznes bilan
   aniqlashtirish kerak: aynan bir yil - bonus beriladimi?

Birinchi ikkisi @CsvSource ga ikki qator qo'shish bilan hal bo'ladi.
```

## 34.10 Review checklisti: test to'liqligi

| Savol | Nega |
| --- | --- |
| Har sonli shart uchun uch chegara testi bormi | `<` va `<=` xatosi |
| Enum ning hamma qiymati qamralganmi | Yangi qiymat |
| Shartlar kombinatsiyasi jadval bilan tekshirilganmi | O'tkazib yuborilgan kombinatsiya |
| Holat o'tish matritsasi to'liqmi | Taqiqlangan o'tish |
| Bo'sh to'plam va bitta element holati bormi | 0 ga bo'lish, `get(0)` |
| Null va bo'sh kirish testlari bormi | NPE |
| Xato yo'llari (timeout, 500, noto'g'ri javob) qamralganmi | Prodda tez-tez bajariladi |
| Idempotentlik testi bormi | Dublikat |
| Poyga testi bormi (kritik joylarda) | Konkurentlik xatosi |
| Eski shakldagi ma'lumot bilan test bormi | Migratsiyadan keyingi holat |
| Mutatsiya bilan testni aldab o'tish mumkinmi | Yolg'on ishonch |
| Unicode va apostrof bilan test bormi | Mahalliy ma'lumot |

## 34.11 Amalda qo'llash

- [ ] Eng muhim uchta domen klassi uchun holatlar jadvalini tuzib, mavjud testlar bilan taqqoslang va bo'shliqlarni ro'yxatga oling.
- [ ] Barcha sonli chegaralar uchun "chegaradan past / aynan / yuqori" testlarini qo'shing.
- [ ] Holat mashinasi bo'lgan domen obyektlari uchun to'liq o'tish matritsasi testini yozing.
- [ ] `@EnumSource` bilan har bir enum qiymati qamralganini ta'minlang.
- [ ] Ikki va undan ko'p shartli qarorlar uchun qaror jadvalini `@CsvSource` ga aylantiring.
- [ ] Har bir tashqi integratsiya uchun kamida uch xato yo'li testini qo'shing: timeout, 5xx, noto'g'ri javob.
- [ ] Idempotentlik talab qiladigan har bir operatsiya uchun "ikki marta chaqirish" testini yozing.
- [ ] Kritik poyga holatlari uchun parallel test yozing (haqiqiy PostgreSQL bilan).
- [ ] PIT ni domen paketlariga sozlab, mutatsiya ballini o'lchang va 80 foizdan past bo'lsa bo'shliqlarni to'ldiring.

---

[&larr; 33. Bog'liqlik va supply chain review](33-bogliqlik-va-supply-chain-review.md) · [Mundarija](README.md) · [35. Test sifati review: assertion, izolyatsiya, beqarorlik &rarr;](35-test-sifati-review-assertion-izolyatsiya.md)
