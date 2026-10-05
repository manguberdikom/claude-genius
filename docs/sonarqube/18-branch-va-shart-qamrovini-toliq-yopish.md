<!-- doc: sonarqube | chapter: 18 | part: V. Sonar o'tadigan test -->

[Barcha hujjatlar](../../README.md) / [SonarQube](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 18. Branch va shart qamrovini to'liq yopish usullari (Covering Every Branch)

<details>
<summary>Bu bobdagi 15 bo'lim</summary>

- [18.1 Line coverage va branch coverage farqi aniq misolda](#181-line-coverage-va-branch-coverage-farqi-aniq-misolda)
- [18.2 Murakkab shart (`&&`, `||`) bytecode da nechta tarmoq hosil qiladi](#182-murakkab-shart---bytecode-da-nechta-tarmoq-hosil-qiladi)
- [18.3 Qisqa tutashuv (short-circuit) va u qamrovga qanday ta'sir qiladi](#183-qisqa-tutashuv-short-circuit-va-u-qamrovga-qanday-tasir-qiladi)
- [18.4 Har bir tarmoqni yopish uchun kerakli test holatlari jadvali](#184-har-bir-tarmoqni-yopish-uchun-kerakli-test-holatlari-jadvali)
- [18.5 `switch` va yangi `switch` ifodasini to'liq qoplash](#185-switch-va-yangi-switch-ifodasini-toliq-qoplash)
- [18.6 Ternar operator va `Optional` zanjiri](#186-ternar-operator-va-optional-zanjiri)
- [18.7 Sikl ichidagi shartlar va chegaraviy qiymatlar](#187-sikl-ichidagi-shartlar-va-chegaraviy-qiymatlar)
- [18.8 Istisno tarmog'ini yopish: mock orqali xato yuzaga keltirish](#188-istisno-tarmogini-yopish-mock-orqali-xato-yuzaga-keltirish)
- [18.9 `finally` bloki va resurs yopilishi](#189-finally-bloki-va-resurs-yopilishi)
- [18.10 Null tekshiruvlari: haqiqatan kerakmi yoki olib tashlash mumkinmi](#1810-null-tekshiruvlari-haqiqatan-kerakmi-yoki-olib-tashlash-mumkinmi)
- [18.11 Shartni soddalashtirib tarmoqlar sonini kamaytirish](#1811-shartni-soddalashtirib-tarmoqlar-sonini-kamaytirish)
- [18.12 Tuzoq va yechim](#1812-tuzoq-va-yechim)
- [18.13 Oddiy yondashuv va arxitektor yondashuvi](#1813-oddiy-yondashuv-va-arxitektor-yondashuvi)
- [18.14 Sonar ga tarmoq ma'lumotini uzatish](#1814-sonar-ga-tarmoq-malumotini-uzatish)
- [18.15 Amalda qo'llash](#1815-amalda-qollash)

</details>



Quality gate `coverage` raqamiga qaraydi, lekin bu raqam ikki xil o'lchovdan yasalgan: qator qamrovi va shart qamrovi. Ko'p jamoa faqat birinchisini quvadi va keyin gate nega qizil bo'lganini tushunmaydi. Bu bobda Sonar shart qamrovini qanday hisoblashini, bytecode da nechta tarmoq paydo bo'lishini va har bir tarmoqni yopish uchun qanday test kerakligini ko'rib chiqamiz.

## 18.1 Line coverage va branch coverage farqi aniq misolda

Sonar ikkita alohida raqam saqlaydi. `line_coverage` bajarilishi mumkin bo'lgan qatorlardan qanchasi ishga tushganini aytadi. `branch_coverage`, UI da "Condition Coverage" deb nomlanadi, shartli o'tish nuqtalarining nechta yo'nalishi bosib o'tilganini aytadi. Umumiy `coverage` ikkisining birlashmasi: qoplangan shartlar va qatorlar yig'indisini barcha shartlar va qatorlar yig'indisiga bo'lish.

Ombor qoldig'ini zahiralash metodini olaylik. Bitta test bilan hamma qator bajariladi, lekin shartning ikkinchi yo'nalishi hech qachon sinalmaydi.

```java
// Zahiralash: bitta test bilan qatorlar 100% bo'ladi
public ReservationResult reserve(String sku, int qty) {
    Stock stock = stockRepository.findBySku(sku);   // 1-qator
    if (stock.available() < qty) {                  // 2-qator: shart
        return ReservationResult.rejected(sku);     // 3-qator
    }
    stock.decrease(qty);                            // 4-qator
    return ReservationResult.accepted(sku, qty);    // 5-qator
}
```

Faqat teskari holatni test qilsak, 3-qator qizil qoladi va JaCoCo 2-qatorni qisman qoplangan deb belgilaydi. Ya'ni qator qamrovi "kod ishga tushdimi" degan savolga javob beradi, tarmoq qamrovi "qaror qanday qabul qilindi" degan savolga. Biznes xatolari deyarli har doim ikkinchi savolda yashiradi.

## 18.2 Murakkab shart (`&&`, `||`) bytecode da nechta tarmoq hosil qiladi

JaCoCo manba kodni emas, bytecode ni o'qiydi. Har bir shartli o'tish buyrug'i, masalan `IFEQ` yoki `IF_ICMPLT`, ikkita natija beradi. Demak `if (a)` ikkita tarmoq, `if (a && b)` esa to'rtta tarmoq hosil qiladi, chunki kompilyator ikkita alohida o'tish yozadi. Uchta atomar shart oltita, to'rttasi sakkizta tarmoq beradi.

Muhim nuqta: JaCoCo har bir atomar shartni alohida sanaydi, kombinatsiyasini sanamaydi. Ya'ni bu MC/DC emas, oddiy branch coverage. To'rtta shart uchun 16 kombinatsiya bor, ammo 100% tarmoq qamrovi uchun odatda 4 yoki 5 test yetadi. Raqam yashil bo'lishi mumkin, holbuki kombinatsiyalarning yarmi sinalmagan.

Yana bir nozik joy: kompilyator va kod generatorlari yozgan sintetik kod ham tarmoq yasaydi. `String` ustidan `switch` `hashCode()` va `equals()` zanjirini yozadi. Lombok ning `@EqualsAndHashCode` generatsiyasi ham tarmoq qo'shadi, shuning uchun generatsiya qilingan kodni qamrovdan chiqarish kerak.

```xml
<!-- JaCoCo: branch qamrovini CLASS darajasida majburiy qilish -->
<plugin>
  <groupId>org.jacoco</groupId>
  <artifactId>jacoco-maven-plugin</artifactId>
  <version>0.8.12</version>
  <executions>
    <execution>
      <id>check-branches</id>
      <goals><goal>check</goal></goals>
      <configuration>
        <rules>
          <rule>
            <element>CLASS</element>
            <!-- generatsiya qilingan kod exclusions da chiqariladi -->
            <limits>
              <limit>
                <counter>BRANCH</counter>
                <value>COVEREDRATIO</value>
                <minimum>0.80</minimum>
              </limit>
            </limits>
          </rule>
        </rules>
      </configuration>
    </execution>
  </executions>
</plugin>
```

## 18.3 Qisqa tutashuv (short-circuit) va u qamrovga qanday ta'sir qiladi

`&&` chap tomon `false` bo'lsa o'ng tomonni bajarmaydi, `||` chap tomon `true` bo'lsa o'ng tomonga o'tmaydi. Qamrov uchun oqibat bitta: bajarilmagan shart tarmog'i ochiq qoladi. Agar `a` har doim `false` bo'ladigan testlar yozsak, JaCoCo "2 of 4 branches missed" deb ko'rsatadi.

Aksincha vaziyat ham bor: ba'zan `b` ni hech qanday test bilan bajarish imkoni yo'q, chunki `a` uni istisno qiladi. `java:S2589` keraksiz boolean ifodani, `java:S2583` natijasi har doim bir xil bo'ladigan shartni belgilaydi. Bunday holatda yechim test yozish emas, ortiqcha shartni o'chirish.

Amaliy qoida: eng arzon va eng ko'p rad etadigan shartni chapga qo'ying. Ammo esda tuting, chap shart juda tez rad etsa, o'ng tomonni yopish uchun maxsus test ma'lumotlari tayyorlash kerak bo'ladi.

## 18.4 Har bir tarmoqni yopish uchun kerakli test holatlari jadvali

To'lovni ushlab qolish (capture) qarorini olaylik. To'rtta atomar shart bor, demak JaCoCo sakkizta tarmoq sanaydi.

```java
// Capture sharti: 4 atomar shart, 8 tarmoq
public boolean canCapture(Payment payment, Merchant merchant) {
    return payment.isAuthorized()                       // A
            && !payment.isExpired(clock.instant())      // B
            && (payment.amount().compareTo(merchant.dailyLimit()) <= 0  // C
                || payment.isManuallyApproved());       // D
}
```

Short-circuit ni hisobga olib minimal test to'plamini tuzamiz. `-` belgisi shart umuman bajarilmaganini bildiradi.

| # | A: authorized | B: expired emas | C: limit ichida | D: qo'lda tasdiq | Yangi yopilgan tarmoq | Natija |
|---|---|---|---|---|---|---|
| 1 | false | - | - | - | A=false | false |
| 2 | true | false | - | - | A=true, B=false | false |
| 3 | true | true | true | - | B=true, C=true | true |
| 4 | true | true | false | true | C=false, D=true | true |
| 5 | true | true | false | false | D=false | false |

Besh test sakkizta tarmoqni yopadi. Jadvalni parametrli testga ko'chiramiz, shunda qamrov va hujjat bitta joyda turadi. Yangi shart qo'shilsa jadvalga yangi qator qo'shiladi va test to'plami avtomatik o'sadi. Shu usul review paytida ham foydali: tekshiruvchi jadvalga qarab qaysi kombinatsiya tushib qolganini darhol ko'radi.

```java
@ParameterizedTest(name = "[{index}] A={0} B={1} C={2} D={3} -> {4}")
@CsvSource({
    // A,     expired, limitIchida, qolda, kutilgan
    "false,   false,   true,        false, false",  // 1: A=false
    "true,    true,    true,        false, false",  // 2: B=false
    "true,    false,   true,        false, true",   // 3: C=true
    "true,    false,   false,       true,  true",   // 4: C=false, D=true
    "true,    false,   false,       false, false"   // 5: D=false
})
void canCapture_barchaTarmoq(boolean authorized, boolean expired,
                             boolean limitIchida, boolean qolda, boolean kutilgan) {
    Payment payment = PaymentFixture.builder()
            .authorized(authorized)
            .expiresAt(expired ? SOATDAN_OLDIN : SOATDAN_KEYIN)
            .amount(limitIchida ? new BigDecimal("50.00") : new BigDecimal("5000.00"))
            .manuallyApproved(qolda)
            .build();

    assertThat(service.canCapture(payment, MERCHANT_LIMIT_100)).isEqualTo(kutilgan);
}
```

## 18.5 `switch` va yangi `switch` ifodasini to'liq qoplash

Klassik `switch` har bir `case` uchun bitta tarmoq yasaydi va `default` ham tarmoq hisoblanadi. `default` yozilmagan bo'lsa, Sonar `java:S131` qoidasi bilan shikoyat qiladi, JaCoCo esa baribir yashirin "hech qaysi case mos kelmadi" yo'nalishini sanaydi.

Java 17 dan keyingi `switch` ifodasi `enum` ustida ishlatilganda holat o'zgaradi. Barcha konstanta sanab o'tilgan bo'lsa, kompilyator to'liqlikni (exhaustiveness) o'zi tekshiradi va `default` shart emas. Lekin kompilyator sinf alohida qayta kompilyatsiya qilinishi ehtimoliga qarshi yashirin tarmoq yozadi, u xato tashlaydi va JaCoCo da qoplanmagan qoladi. Shuning uchun `enum` ustidagi `switch` ifodasi ko'pincha "1 of N branches missed" deb ko'rsatiladi va bu normal holat.

```java
// Komissiya: switch ifodasi, enum to'liq sanalgan
BigDecimal commission(OrderStatus status, BigDecimal amount) {
    return switch (status) {
        case NEW, PENDING -> BigDecimal.ZERO;              // 1-tarmoq
        case PAID -> amount.multiply(new BigDecimal("0.02"));  // 2-tarmoq
        case SHIPPED -> amount.multiply(new BigDecimal("0.03")); // 3-tarmoq
        case CANCELLED -> amount.negate();                 // 4-tarmoq
    };
}

// Test: enum ning hamma qiymati bo'ylab yuramiz
@ParameterizedTest
@EnumSource(OrderStatus.class)
void commission_hammaHolatUchunAniqlangan(OrderStatus status) {
    assertThatNoException()
            .isThrownBy(() -> service.commission(status, new BigDecimal("100")));
}
```

`@EnumSource` ning qiymati shundaki, `enum` ga yangi konstanta qo'shilganda test avtomatik o'sadi va `switch` da unutilgan holat darhol yiqiladi.

## 18.6 Ternar operator va `Optional` zanjiri

Ternar operator `?:` ham ikkita tarmoq yasaydi, lekin u bitta qatorda yozilgani uchun qator qamrovi uni yashiradi. `return qty > 0 ? qty : 0;` qatori bitta test bilan yashil bo'ladi, holbuki tarmoqlarning yarmi ochiq. Ichma ich joylashgan ternar tarmoqlarni ko'paytiradi va o'qilishga oid qoidani ishga tushiradi.

`Optional` zanjirida `orElse` tarmoq yasamaydi, chunki u har doim argumentni hisoblaydi. `orElseGet`, `orElseThrow`, `filter` va `map` esa ichida shart saqlaydi: har bir oraliq qadam uchun qiymat bor va qiymat yo'q holatlari kerak.

```java
// Chegirma: har bir Optional qadami 2 holat talab qiladi
public BigDecimal discountFor(Long customerId, String couponCode) {
    return couponRepository.findByCode(couponCode)          // bor / yo'q
            .filter(Coupon::isActive)                        // aktiv / aktiv emas
            .filter(c -> c.appliesTo(customerId))            // tegishli / tegishli emas
            .map(Coupon::percent)                            // map ishga tushdi / tushmadi
            .orElse(BigDecimal.ZERO);
}
// Testlar: kupon yo'q; aktiv emas; mijozga tegishli emas; to'liq mos.
```

To'rtta test to'rtta tarmoq juftligini yopadi. Agar uchinchi testni yozmasak, `appliesTo` ning `false` yo'nalishi ochiq qoladi va eng xavfli biznes xatosi, ya'ni boshqa mijozning chegirmasini qo'llash, test bilan himoyalanmagan bo'ladi.

## 18.7 Sikl ichidagi shartlar va chegaraviy qiymatlar

Sikl o'zi ham shart: `for` va `while` ning sikl sharti ikkita tarmoq beradi. Birinchisi "yana bitta iteratsiya", ikkinchisi "sikl tugadi". Bo'sh kolleksiya bilan chaqirilmagan metodda bu ikkinchi tarmoq yopilsa ham, sikl ichidagi `if` ning tarmoqlari ochiq qolishi mumkin. Shuning uchun sikl uchun uch xil kirish ma'lumoti kerak: bo'sh, bitta element, bir nechta element.

`break` va `continue` yana tarmoq qo'shadi: "sikl shartidan chiqdi" va "break orqali chiqdi" yo'llari alohida sanaladi.

```java
// Birinchi mos tranzaksiyani topish
Optional<Transaction> firstOverLimit(List<Transaction> txs, BigDecimal limit) {
    for (Transaction tx : txs) {            // sikl sharti: 2 tarmoq
        if (tx.amount().compareTo(limit) > 0) {  // if: 2 tarmoq
            return Optional.of(tx);              // break yo'li
        }
    }
    return Optional.empty();                // sikl oxirigacha yetdi
}
// Kerakli kirish: [] ; [kichik] ; [kichik, katta] ; [katta, kichik]
```

Chegaraviy qiymatlar alohida masala. `compareTo(limit) > 0` uchun `amount` ning `limit` ga aniq teng holati muhim, chunki `>` va `>=` xatosi eng ko'p uchraydi. Tarmoq qamrovi bu xatoni ushlamaydi: teng holat `false` tarmog'ini yopadi va qamrov yashil ko'rinadi. Har bir solishtirishga uchta qiymat bering: past, teng, baland.

## 18.8 Istisno tarmog'ini yopish: mock orqali xato yuzaga keltirish

`try` va `catch` juftligi ham tarmoq yasaydi, lekin uni oddiy ma'lumot bilan yopish qiyin. Tashqi tizim xatosini yuzaga keltirish uchun mock dan foydalanamiz. Bu bobda mock mexanikasi tushuntirilmaydi, u [testlash qo'llanmasidagi](../testing/README.md) test duble mavzusida bor. Bu yerda muhimi: `catch` bloki ichidagi har bir qator va har bir qayta tashlash yo'li alohida tarmoq.

Ko'p jamoa `catch` ichida faqat `log.error` yozib qo'yadi. Natijada Sonar ikki marta shikoyat qiladi: qamrov yetmaydi va istisnoni yutib yuborish turkumidagi qoida ishga tushadi. To'g'ri yechim: `catch` da aniq xatti harakat bo'lsin va test shuni tekshirsin.

```java
@Test
void capture_gatewayXatosidaRetryGaQoyiladi() {
    // mock tashqi gateway ni xato tashlashga majburlaymiz
    when(gateway.capture(any())).thenThrow(new GatewayTimeoutException("504"));

    CaptureResult result = service.capture(PAYMENT_ID);

    // catch xatti harakati: PENDING_RETRY va outbox yozuvi
    assertThat(result.status()).isEqualTo(Status.PENDING_RETRY);
    verify(outbox).enqueue(argThat(e -> e.type().equals("CAPTURE_RETRY")));
    verify(paymentRepository).save(argThat(p -> p.attempts() == 1));
}

@Test
void capture_boshqaXatolarQaytaTashlanadi() {
    when(gateway.capture(any())).thenThrow(new IllegalStateException("buzilgan holat"));

    // ikkinchi catch tarmog'i: qayta tashlash yo'li
    assertThatThrownBy(() -> service.capture(PAYMENT_ID))
            .isInstanceOf(IllegalStateException.class);
    verify(outbox, never()).enqueue(any());
}
```

## 18.9 `finally` bloki va resurs yopilishi

`finally` bloki bytecode da ikki marta yoziladi: normal oqim uchun va istisno oqimi uchun. Shu sababli faqat muvaffaqiyatli yo'lni test qilsangiz, JaCoCo `finally` qatorlarini qisman qoplangan deb ko'rsatadi.

`try-with-resources` da kompilyator `close()` ni `null` tekshiruvi va bosiq istisno (suppressed exception) mantig'i bilan o'raydi. Hosil bo'lgan tarmoqlarning ba'zilarini Java kodidan turib yopish mumkin emas. Amaliy javob: ularni ta'qib qilmang, lekin `try` blokidan istisno chiqadigan testni albatta yozing.

```java
// Yomon: qo'lda finally, qo'shimcha null tarmog'i
Connection conn = null;
try {
    conn = dataSource.getConnection();
    return read(conn);
} finally {
    if (conn != null) {        // test qilish qiyin tarmoq
        conn.close();
    }
}

// Sonar o'tadigan variant: tarmoq kodda ko'rinmaydi
try (Connection conn = dataSource.getConnection()) {
    return read(conn);
}
```

## 18.10 Null tekshiruvlari: haqiqatan kerakmi yoki olib tashlash mumkinmi

Har bir `if (x != null)` ikkita tarmoq qo'shadi. Agar `x` hech qachon `null` bo'lmasa, siz yopilmaydigan tarmoq yaratib qamrovni o'zingiz pasaytirdingiz. Sonar ning oqim tahlili metod chegarasidan tashqariga har doim chiqmaydi, shuning uchun qarorni siz qabul qilasiz.

Mezon oddiy. Tashqi chegarada, ya'ni HTTP controller, Kafka consumer va tashqi API javobida null mumkin, demak tekshiruv kerak va u uchun test yoziladi. Ichki domen metodlarida null kelmasligi shartnoma bo'lishi kerak: konstruktorda bir marta `Objects.requireNonNull` qo'yib, ichki tekshiruvlarni olib tashlang.

`null` qaytaradigan metod ham har bir chaqiruv joyida ikkita tarmoq yasaydi. Bo'sh `List` yoki `Optional` qaytarsa, bu tarmoqlar yo'qoladi.

## 18.11 Shartni soddalashtirib tarmoqlar sonini kamaytirish

Eng tez qamrov yutug'i test yozishdan emas, tarmoq sonini kamaytirishdan keladi. Uchta usul bor: shartni nomlangan predikatga ajratish, `if` zanjirini `Map` ga aylantirish, shartni ma'lumotlar bazasiga ko'chirish.

Birinchi usul tarmoq sonini kamaytirmaydi, lekin ularni kichik testlanadigan bo'laklarga taqsimlaydi va `java:S3776` cognitive complexity qoidasini qondiradi. Ikkinchi usul tarmoqlarni butunlay yo'q qiladi: `Map` dagi izlash shartli o'tish emas. Uchinchi usul filtrlash siklini `WHERE` shartiga aylantiradi.

```sql
-- Oldin: Java da sikl va if bilan filtrlangan edi.
-- Keyin: shart SQL ga ko'chdi, Java da tarmoq qolmadi.
SELECT o.id, o.total_amount, o.status
FROM orders o
JOIN merchants m ON m.id = o.merchant_id
WHERE o.status = 'PAID'
  AND o.created_at >= :fromDate
  AND (o.total_amount <= m.daily_limit OR o.manually_approved = true)
ORDER BY o.created_at DESC;
```

```java
// Oldin: 3 ta if, 6 tarmoq, har biri uchun test kerak
BigDecimal fee(OrderStatus s) {
    if (s == OrderStatus.PAID) return new BigDecimal("0.02");
    if (s == OrderStatus.SHIPPED) return new BigDecimal("0.03");
    if (s == OrderStatus.CANCELLED) return BigDecimal.ZERO;
    return BigDecimal.ZERO;
}

// Keyin: 0 tarmoq, bitta parametrli test hammasini qoplaydi
private static final Map<OrderStatus, BigDecimal> FEES = Map.of(
        OrderStatus.PAID, new BigDecimal("0.02"),
        OrderStatus.SHIPPED, new BigDecimal("0.03"),
        OrderStatus.CANCELLED, BigDecimal.ZERO);

BigDecimal fee(OrderStatus s) {
    return FEES.getOrDefault(s, BigDecimal.ZERO);
}
```

## 18.12 Tuzoq va yechim

| Tuzoq | Nima bo'ladi | Yechim |
|---|---|---|
| Faqat `line_coverage` ni kuzatish | Gate `coverage` da yiqiladi, sabab tushunarsiz | `branch_coverage` va `uncovered_conditions` metrikasini ham panelga qo'yish |
| `enum` `switch` ifodasida "1 branch missed" | Yopilmaydigan tarmoqni quvib vaqt ketadi | Yashirin `default` ni qabul qilish, qamrov chegarasini CLASS darajasida belgilash |
| Qo'lda `finally` va `null` tekshiruvi | Qoplanmaydigan tarmoqlar ko'payadi | `try-with-resources` ga o'tish |
| Keraksiz null tekshiruvi ichki metodda | Tarmoq hech qachon yopilmaydi | Konstruktorda `requireNonNull`, ichkarida tekshiruvni o'chirish |
| Lombok va MapStruct generatsiyasi | Begona tarmoqlar foizni pasaytiradi | `sonar.coverage.exclusions` va JaCoCo `excludes` da chiqarish |
| 100% tarmoq, 0 ta assertion | Yashil raqam, himoya yo'q | Mutation testing yoki assertion sifatini review da tekshirish |
| Chegara qiymati sinalmagan | `>` va `>=` xatosi ushlanmaydi | Har bir solishtirishga past, teng, baland uchligini berish |
| `catch` da faqat log | Istisno tarmog'i ochiq, qoida ham buziladi | `catch` ga aniq xatti harakat berish va uni `verify` bilan tekshirish |

## 18.13 Oddiy yondashuv va arxitektor yondashuvi

| Savol | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Qamrov maqsadi | Umumiy foizni 80 ga ko'tarish | Yangi kod uchun tarmoq qamrovini majburiy qilish, eski kodni qoldirish |
| Murakkab shart | Bitta test yozib yashil qatorga qanoat qilish | Haqiqat jadvalini tuzib, har bir tarmoqqa qator ajratish |
| Test yozish tartibi | Kod bitgandan keyin qamrovni to'ldirish | Jadvalni kod bilan birga tuzib, `@CsvSource` ga ko'chirish |
| Yopilmaydigan tarmoq | Soxta test yozib yoki `@Generated` qo'yib yashirish | Shartni o'chirish yoki kompilyator yasagan tarmoq ekanini hujjatlash |
| `if` zanjiri | Har bir shoxga alohida test | Zanjirni `Map` yoki strategiyaga aylantirib tarmoqni yo'qotish |
| Null | Ehtiyot uchun hamma joyda tekshirish | Chegarada bir marta tekshirish, ichkarida shartnomaga tayanish |
| Istisno yo'llari | Test qilish qiyin deb o'tkazib yuborish | Mock bilan har bir `catch` ning xatti harakatini tekshirish |
| Sikl | Bitta ro'yxat bilan test | Bo'sh, bitta, ko'p va chegara qiymatlari to'rtligi |
| Gate buzilganda | Chegarani pasaytirish | Tarmoq sonini kamaytirib kodni soddalashtirish |
| Qamrov ishonchi | Foiz yetarli dalil | Mutation testing bilan assertion sifatini alohida o'lchash |

## 18.14 Sonar ga tarmoq ma'lumotini uzatish

Sonar o'zi qamrov o'lchamaydi, u JaCoCo ning XML hisobotini o'qiydi. Shuning uchun XML generatsiyasi yoqilgan va yo'l to'g'ri ko'rsatilgan bo'lishi kerak.

```properties
# sonar-project.properties: tarmoq ma'lumoti JaCoCo XML dan keladi
sonar.projectKey=payments-service
sonar.java.source=21
sonar.coverage.jacoco.xmlReportPaths=target/site/jacoco-aggregate/jacoco.xml,\
  target/site/jacoco/jacoco.xml
sonar.junit.reportPaths=target/surefire-reports,target/failsafe-reports
# generatsiya qilingan kod qamrovsiz
sonar.coverage.exclusions=**/config/**,**/dto/**,**/*Application.java
# lekin code smell tekshiruvida qoladi
sonar.exclusions=**/generated/**
```

```bash
# Avval hisobot, keyin tahlil
./mvnw clean verify -Pcoverage

# Yopilmagan tarmoqlarni terminalda ko'rish
grep -o 'missedb="[1-9][0-9]*"[^>]*' target/site/jacoco/jacoco.xml | head -20

# Sonar ga yuborish: XML mavjud bo'lishi shart
./mvnw sonar:sonar -Dsonar.host.url="$SONAR_URL" -Dsonar.token="$SONAR_TOKEN"

# Gate natijasini kutish
./mvnw sonar:sonar -Dsonar.qualitygate.wait=true -Dsonar.qualitygate.timeout=600
```

```yaml
# CI: test va tahlil bitta job da
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0   # new code aniqlash uchun butun tarix kerak
      - uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: '21'
      - name: Test va JaCoCo
        run: ./mvnw -B clean verify
      - name: Branch chegarasi
        run: ./mvnw -B jacoco:check@check-branches
      - name: Sonar tahlili
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
        run: ./mvnw -B sonar:sonar -Dsonar.qualitygate.wait=true
```

Halol xulosa: 100% tarmoq qamrovi xatosiz kodni kafolatlamaydi. JaCoCo kombinatsiyalarni emas, alohida natijalarni sanaydi va assertion sifatini o'lchamaydi. Tarmoq qamrovi faqat "bu qaror hech qachon sinalmagan" holatini ushlaydigan quyi chegara. Shartni soddalashtirib tarmoq sonini kamaytirish, qolganini jadval orqali ataylab yopish eng barqaror strategiya.

## 18.15 Amalda qo'llash

- [ ] Sonar loyiha panelida `branch_coverage` va `uncovered_conditions` metrikalarini qo'shib, eng ko'p yopilmagan shart saqlagan 10 ta sinfni ro'yxatga oling.
- [ ] Shu ro'yxatdagi eng murakkab shartni oling, uning atomar shartlarini sanab haqiqat jadvalini tuzing va `@CsvSource` parametrli testga ko'chiring.
- [ ] `jacoco-maven-plugin` ga `BRANCH` va `COVEREDRATIO` chegarasi bilan `check` qoidasini qo'shib, generatsiya qilingan sinflarni `excludes` ga kiriting.
- [ ] Barcha qo'lda yozilgan `finally` bloklarini `try-with-resources` ga o'tkazing va `java:S2095` ogohlantirishlari yo'qolganini tekshiring.
- [ ] Ichki domen metodlaridagi null tekshiruvlarini ko'rib chiqing: konstruktorda bir marta `requireNonNull` qoldirib, qolganini o'chiring.
- [ ] Har bir `catch` bloki uchun mock bilan xato yuzaga keltiruvchi test yozing va `catch` ichidagi xatti harakatni `verify` bilan tasdiqlang.
- [ ] Kamida bitta uzun `if` zanjirini `Map` yoki strategiyaga aylantirib, tarmoq soni va cognitive complexity qanchaga kamayganini o'lchab yozib qo'ying.
- [ ] CI da `fetch-depth: 0` va `sonar.qualitygate.wait=true` yoqilganini tekshirib, gate qizil bo'lganda pipeline haqiqatan yiqilishiga ishonch hosil qiling.

---

[&larr; 17. Sonar talablarini qondiradigan test yozish](17-sonar-talablarini-qondiradigan-test-yozish.md) · [Mundarija](README.md) · [19. Testning o'zidagi Sonar qoidalari va test sifati &rarr;](19-testning-ozidagi-sonar-qoidalari-va-test.md)
