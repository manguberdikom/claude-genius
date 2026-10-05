<!-- doc: code-review | chapter: 12 | part: II. Arxitektura, dizayn va clean code review -->

[Barcha hujjatlar](../../README.md) / [Kod review](README.md)

# 12. Code smell va anti-pattern katalogi diffda (Smells in a Diff)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

- [12.1 Boshqaruv oqimi smell lari](#121-boshqaruv-oqimi-smell-lari)
- [12.2 Ma'lumot va holat smell lari](#122-malumot-va-holat-smell-lari)
- [12.3 Spring ga xos anti-patternlar](#123-spring-ga-xos-anti-patternlar)
- [12.4 Ma'lumotlar bazasiga tegishli smell lar](#124-malumotlar-bazasiga-tegishli-smell-lar)
- [12.5 Test smell lari](#125-test-smell-lari)
- [12.6 Konkurentlik smell lari](#126-konkurentlik-smell-lari)
- [12.7 Xavfsizlik smell lari (tez ro'yxat)](#127-xavfsizlik-smell-lari-tez-royxat)
- [12.8 Operatsion smell lar](#128-operatsion-smell-lar)
- [12.9 Smell ni oqibat tilida aytish](#129-smell-ni-oqibat-tilida-aytish)
- [12.10 Katalogni loyihaga moslashtirish](#1210-katalogni-loyihaga-moslashtirish)
- [12.11 Amalda qo'llash](#1211-amalda-qollash)

</details>


Bu bob review ning tez ishlatiladigan ma'lumotnomasi: belgi, oqibat va javob. Maqsad - diffda ko'rinadigan naqshni tanib olish va uni oqibat tilida aytish. Smell o'zi xato emas, u xato ehtimolini oshiradigan shakl, shu sababli har bandda "qachon qabul qilinadi" ustuni ham bor.

## 12.1 Boshqaruv oqimi smell lari

| Smell | Diffdagi belgisi | Oqibati | Qachon qabul qilinadi |
| --- | --- | --- | --- |
| Ichma-ich shartlar | Uch va ko'p daraja `if` | Chegaraviy holat ko'rinmaydi | Qisqa va chiziqli bo'lsa |
| Bo'sh `catch` | `catch (Exception e) { }` | Xato yo'qoladi, incident ko'r bo'ladi | Deyarli hech qachon |
| `catch (Exception)` keng | Barcha xatolar bir xil ishlanadi | Dasturlash xatosi biznes xatosi kabi ko'rinadi | Chegara qatlamida, log bilan |
| Bayroq parametr | `process(order, true)` | Chaqiruv joyi o'qilmaydi | Ichki private metodda |
| `null` qaytarish | `return null;` | Chaqiruvchida NPE xavfi | Ichki, tez yo'lda (hujjatlangan) |
| Istisno bilan boshqaruv | `try { parse() } catch { default }` | Sekin va niyat yashirin | Tashqi API shunday bo'lsa |
| Mantiqsiz standart | `default -> {}` jim o'tkazish | Yangi enum qiymati jim yo'qoladi | Hech qachon |
| Takroriy shart | Bir xil `if` ikki joyda | Bittasi o'zgarmay qoladi | Qisqa va ochiq bo'lsa |

```java
// Eng xavfli naqsh: jim yutilgan xato va jim o'tkazilgan enum.
try {
    inventory.reserve(order);
} catch (Exception e) {              // nima bo'lsa ham davom etadi
    // keyinroq tuzatamiz
}

switch (event.type()) {
    case CREATED -> handleCreated(event);
    case UPDATED -> handleUpdated(event);
    default -> { }                   // DELETED qo'shilsa - jim yo'qoladi
}

// Review javobi: ikkisi ham oqibat bilan aytiladi.
// blocker: inventar band qilish xatosi yutilgan. Buyurtma yaratiladi,
//          lekin tovar band qilinmaydi - ikki mijoz bir mahsulotni oladi.
//          Hech qanday log yoki metrika yo'q, shuning uchun bu holatni
//          mijoz shikoyat qilgandan keyin bilamiz.
// blocker: default -> {} yangi hodisa turini jim yutadi. sealed interface
//          yoki default -> throw qo'yilsa, yangi tur kompilyatsiyada yoki
//          birinchi testda ko'rinadi.
```

## 12.2 Ma'lumot va holat smell lari

| Smell | Belgisi | Oqibati |
| --- | --- | --- |
| Mutable umumiy holat | `static Map`, `static List` | Poyga, buzilgan ma'lumot, test ta'siri |
| Mutable obyekt kalit sifatida | `HashMap<Order,...>` o'zgaruvchan `Order` | Yo'qolgan yozuvlar |
| `equals` bor, `hashCode` yo'q | Faqat bittasi override qilingan | `HashSet` da dublikatlar |
| JPA entity da `equals` ID bo'yicha, ID generated | Yangi obyekt `hashCode` i o'zgaradi | `Set` da g'alati xulq |
| Ochiq setterlar domenda | `setStatus`, `setTotal` public | Invariant himoyasiz |
| Kolleksiyani tashqariga qaytarish | `return this.lines;` | Tashqaridan o'zgartirish |
| Primitiv obsessiya | Hamma narsa `String`/`long` | Almashtirib qo'yish, validatsiya tarqalishi |
| `Optional` maydon sifatida | `private Optional<X> x;` | Serializatsiya muammosi, ortiqcha o'ram |
| Nullable bo'lgan boolean | `Boolean active` | Uch holatli mantiq |
| Pul `double` da | `double amount` | Yig'ilgan aniqlik xatosi |
| Zonasiz vaqt | `LocalDateTime` saqlashda | Yozgi vaqt va server zonasi muammolari |

```java
// Kolleksiyani himoyalash: eng ko'p o'tkazib yuboriladigan joy.
public class Order {
    private final List<OrderLine> lines = new ArrayList<>();

    // Yomon: tashqaridan o'zgartirish mumkin, invariant buziladi.
    public List<OrderLine> getLines() { return lines; }

    // Yaxshi: o'qish uchun himoyalangan ko'rinish, o'zgartirish metod orqali.
    public List<OrderLine> lines() { return List.copyOf(lines); }

    public void addLine(ProductId product, Quantity qty, Money price) {
        if (status != NEW) throw new IllegalStateException("tasdiqlangan buyurtma");
        if (lines.size() >= MAX_LINES) throw new TooManyLines(MAX_LINES);
        lines.add(new OrderLine(product, qty, price));
        recalculateTotal();                  // invariant: total = qatorlar summasi
    }
}
```

## 12.3 Spring ga xos anti-patternlar

| Anti-pattern | Belgisi | Oqibati |
| --- | --- | --- |
| Maydon inyeksiyasi | `@Autowired` maydonda | Testda konteksttsiz qurilmaydi, immutable emas |
| `@Autowired` bilan setter | Setter orqali bog'liqlik | Yarim qurilgan bean |
| `ApplicationContext` inyeksiyasi | Service locator | Yashirin bog'liqlik |
| Katta `@Configuration` | Yuzlab satrli bean e'lonlari | O'qilmaydi, sinov qiyin |
| `@Transactional` controller da | Tranzaksiya web qatlamida | Uzoq tranzaksiya, OSIV |
| `@Transactional` private metodda | Proxy ishlamaydi | Tranzaksiya yo'q, jim |
| Shu klass ichidan `this.method()` | Proxy chetlab o'tilgan | `@Cacheable`, `@Async` ishlamaydi |
| `@Value` ko'p joyda | Konfiguratsiya tarqalgan | Tipli tekshiruv yo'q |
| Profil bo'yicha biznes mantiqi | `@Profile("prod")` servisda | Prod va test xulqi boshqacha |
| `@ComponentScan` juda keng | Butun paket daraxti | Ishga tushish sekin, kutilmagan beanlar |
| `JpaRepository` controller da | Qatlam o'tkazib yuborilgan | Avtorizatsiya va tranzaksiya yo'q |
| Entity DTO sifatida | Entity controller javobida | Sxema API ga yopishadi, lazy xatolar |
| `@Async` natijasi tashlab ketilgan | `void` qaytaradi, xato yo'qoladi | Jim nosozlik |
| `CommandLineRunner` da migratsiya | Ishga tushishda ma'lumot o'zgartirish | Ikki instansda poyga |

```java
// Eng jim xato: shu klass ichidan chaqiruv proxy ni chetlab o'tadi.
@Service
public class OrderService {

    @Transactional
    public void placeAll(List<PlaceOrder> commands) {
        for (PlaceOrder cmd : commands) {
            place(cmd);          // this.place(...) - proxy ishlamaydi!
        }
    }

    @Transactional(propagation = REQUIRES_NEW)   // e'lon qilingan, lekin ishlamaydi
    public void place(PlaceOrder cmd) { ... }
}
// Review izohi (blocker): place() ichki chaqiruv orqali ishga tushadi,
// shuning uchun REQUIRES_NEW qo'llanmaydi - hammasi bitta tranzaksiyada
// ketadi. Bitta buyurtma xatosi butun paketni qaytaradi, niyat esa teskari
// bo'lgan. Yechim: ikki bean ga ajratish (OrderBatch -> OrderService) yoki
// TransactionTemplate ni aniq chaqirish.
```

## 12.4 Ma'lumotlar bazasiga tegishli smell lar

| Smell | Belgisi | Oqibati |
| --- | --- | --- |
| Siklda so'rov | `for` ichida `repository.findById` | N+1, p99 portlashi |
| `findAll()` keyin Java da filtr | Butun jadval tortiladi | Xotira va kechikish |
| Pagination yo'q | Ro'yxat endpointi limitsiz | Katta javob, OOM |
| `ORDER BY` indekssiz | Yangi tartiblash ustuni | Disk sort, sekin so'rov |
| Dinamik SQL konkatenatsiyasi | `"... WHERE " + field` | SQL injection |
| Tranzaksiya ichida tashqi chaqiruv | HTTP yoki Kafka `@Transactional` ichida | Qulf uzoq, ulanish band |
| `@Transactional` juda keng | Butun servis metodida | Qulflar to'planadi |
| Qulf tartibi turlicha | Ikki joyda teskari tartibda `FOR UPDATE` | Deadlock |
| Migratsiyada `UPDATE` butun jadvalga | Katta jadvalda bir `UPDATE` | Uzoq qulf, replikatsiya lag |
| `SELECT *` | Yangi ustun qo'shilsa ham tortiladi | Tarmoq va xotira |
| Vaqt filtri funksiya bilan | `WHERE date(created_at) = ?` | Indeks ishlatilmaydi |

```sql
-- Review da tez tanib olinadigan ikki naqsh.

-- 1) Indeks ishlatilmaydigan filtr: ustun funksiya ichida.
SELECT * FROM orders WHERE date(created_at) = '2026-10-01';   -- seq scan
-- To'g'risi: oraliq bilan, indeks ishlaydi.
SELECT id, total FROM orders
 WHERE created_at >= '2026-10-01' AND created_at < '2026-10-02';

-- 2) Katta jadvalga "bitta" UPDATE: 12 mln qator, uzoq qulf va WAL to'lishi.
UPDATE orders SET tier = 'BRONZE' WHERE tier IS NULL;
-- To'g'risi: bo'laklab, har bo'lak alohida tranzaksiyada ([25-bob](25-migratsiya-review-qulf-backfill-orqaga.md)).
```

## 12.5 Test smell lari

| Smell | Belgisi | Oqibati |
| --- | --- | --- |
| Assertion yo'q | Faqat chaqiruv va `assertNotNull` | Hech narsa tekshirilmaydi |
| Mock ni tekshirish | `verify(repo).save(any())` yolg'iz | Implementatsiya tekshirilgan, xulq emas |
| `Thread.sleep` test ichida | Vaqtga tayanish | Beqaror test, sekin pipeline |
| Testlar o'zaro bog'liq | Tartibga tayanish, umumiy holat | Jim buziladi |
| Haqiqiy vaqt ishlatilishi | `LocalDate.now()` | Oyning oxirida yiqiladi |
| Haqiqiy tashqi servis | Tarmoqqa chiqish | Beqaror, sekin |
| Bitta testda o'nta assertion | Har xil holatlar birga | Xato joyi noaniq |
| Test nomi ma'nosiz | `test1`, `shouldWork` | Nosozlikda nima buzilganini bilmaslik |
| Faqat happy path | Chegaraviy holat yo'q | Regressiya tutilmaydi |
| Hamma narsa `@SpringBootTest` | Butun kontekst har testda | Sekin, xatoni lokalizatsiya qilish qiyin |

Test review ning to'liq metodikasi VII bo'limda (34-36-boblar), chunki test to'liqligi alohida tahlil apparatini talab qiladi.

## 12.6 Konkurentlik smell lari

| Smell | Belgisi | Oqibati |
| --- | --- | --- |
| Tekshir-keyin-yoz | `if (!exists) save()` | Ikki parallel so'rov ikki yozuv |
| `synchronized` bitta instansda | Qulf faqat shu JVM da | Ikki instansda ishlamaydi |
| `ConcurrentHashMap` ichida murakkab yangilash | `get` keyin `put` | Atomik emas |
| `volatile` bilan hisoblash | `volatile int counter; counter++` | Yo'qolgan yangilanishlar |
| Yangi `ExecutorService` har chaqiruvda | `newFixedThreadPool` metod ichida | Thread portlashi |
| Pool yopilmaydi | `shutdown()` yo'q | Thread oqishi |
| `ThreadLocal` tozalanmaydi | `remove()` yo'q | Xotira oqishi, ma'lumot aralashuvi |
| Cheksiz navbat | `new LinkedBlockingQueue<>()` | OOM, orqaga bosim yo'q |
| `CompletableFuture` xatosi tashlab ketilgan | `exceptionally` yo'q | Jim nosozlik |
| Virtual thread ichida `synchronized` bilan uzoq blok | Pinning | Carrier thread band |

## 12.7 Xavfsizlik smell lari (tez ro'yxat)

| Smell | Belgisi |
| --- | --- |
| Koddagi secret | Parol, token satr sifatida |
| Logda maxfiy ma'lumot | `log.info("req={}", request)` to'liq obyekt |
| Avtorizatsiya ID bo'yicha emas | `@PreAuthorize("isAuthenticated()")` yolg'iz |
| Foydalanuvchi ID so'rovdan olinadi | `@RequestParam userId` |
| So'rovdan kelgan ustun nomi | Dinamik `ORDER BY` |
| Fayl yo'li kirishdan quriladi | Path traversal |
| URL kirishdan quriladi | SSRF |
| Deserializatsiya ishonilmagan ma'lumotdan | `ObjectInputStream`, polimorfik Jackson |
| `permitAll` keng naqsh bilan | `/api/**` ochiq |
| CSRF o'chirilgan sababsiz | `csrf().disable()` |
| Xato javobida stack trace | Ichki detallar tashqariga |
| Zaif tasodif | `Math.random()`, `new Random()` token uchun |

Xavfsizlik review ning to'liq metodikasi VI bo'limda (28-33-boblar).

## 12.8 Operatsion smell lar

| Smell | Belgisi | Oqibati |
| --- | --- | --- |
| Timeout yo'q | `RestClient` yoki `WebClient` sozlamasiz | Thread va pool to'lishi |
| Retry chegarasiz | `while(true)` qayta urinish | Retry bo'roni |
| Log in sikl ichida | Har qator uchun `log.info` | Disk va kechikish |
| Metrika yo'q | Yangi tashqi integratsiya o'lchovsiz | Ko'r incident |
| Health check yuzaki | Faqat "UP" qaytaradi | Yiqilgan bog'liqlik ko'rinmaydi |
| Konfiguratsiya kodda | Qattiq yozilgan URL va chegara | Deploy kerak bo'ladi |
| Feature flag o'chirish sanasi yo'q | Flag doimiy bo'lib qoladi | Shoxlar to'planadi |
| Migratsiya qaytarish rejasi yo'q | Faqat `up` skripti | Reliz qaytarilmaydi |
| Batch ish qulf olmaydi | Ikki instansda bir vaqtda | Ikki marta bajarish |
| Graceful shutdown yo'q | Pod o'ldirilganda ish yarim qoladi | Yo'qolgan xabarlar |

## 12.9 Smell ni oqibat tilida aytish

Katalogdan foydalanishning to'g'ri usuli - nomini aytmaslik, oqibatini aytish. "Bu feature envy" degan izoh muallifni lug'at qidirishga majbur qiladi. "Bu metod Order ning uch darajali ichki tuzilishini biladi, shuning uchun Order o'zgarsa shu hisob sinadi" degan izoh darhol tushunarli.

| Smell nomi (ichki fikr) | Izohda aytiladigan gap |
| --- | --- |
| Feature envy | "Bu hisob Order ning ichki tuzilishiga tayanadi" |
| Shotgun surgery | "Bu o'zgarish 9 faylga bittadan satr qo'shdi" |
| Primitive obsession | "Ikki `long` ni almashtirib qo'ysa, kompilyator sezmaydi" |
| Temporal coupling | "`render()` ni `load()` dan oldin chaqirish NPE beradi" |
| God class | "Bu klass to'rt xil sababga ko'ra o'zgaradi" |
| Anemic model | "Status o'tish qoidasi uch joyda takrorlangan" |
| Leaky abstraction | "Port `HttpClientErrorException` tashlaydi" |

## 12.10 Katalogni loyihaga moslashtirish

Umumiy katalog boshlanish nuqtasi, lekin eng foydali katalog - loyihaning o'z incidentlaridan yozilgani. Har bir incidentdan keyin bitta satr qo'shiladi: belgi, oqibat, qanday topish.

```markdown
<!-- REVIEW-SMELLS.md - loyihaning o'z katalogi, incidentlardan o'sadi. -->
| Sana | Incident | Diffda qanday ko'rinardi | Qanday qidiramiz |
|---|---|---|---|
| 2026-03-11 | To'lov ikki marta o'tdi | `findByKey` keyin `save`, unique yo'q | `grep -rn "findBy.*Key"` + migratsiyada unique |
| 2026-05-02 | Hisobot 40 daqiqa ishladi | Siklda `rateFor()` chaqiruvi | `for` ichida client chaqiruvi |
| 2026-06-19 | Prod qotib qoldi | Tranzaksiya ichida HTTP, timeout yo'q | `@Transactional` + client chaqiruvi |
| 2026-08-07 | Mijoz boshqa buyurtmani ko'rdi | `@PreAuthorize("isAuthenticated()")` | ID bo'yicha tekshiruvsiz endpointlar |
```

Shu jadval review checklistining eng ishonchli qismiga aylanadi, chunki uning har bir bandi loyihada haqiqatan sodir bo'lgan.

## 12.11 Amalda qo'llash

- [ ] `REVIEW-SMELLS.md` faylini yarating va oxirgi beshta incidentni "belgi / oqibat / qanday qidiramiz" shaklida yozing.
- [ ] Bo'sh `catch` va `catch (Exception e)` bloklarini loyihada sanab, ularning har biri uchun log yoki qayta tashlash qo'shing.
- [ ] `default -> { }` va `default: break;` holatlarini toping va ularni istisno tashlashga yoki `sealed` ga o'tkazing.
- [ ] Domen klasslarida tashqariga qaytarilgan mutable kolleksiyalarni toping (`return this.list`) va himoyalangan ko'rinishga o'tkazing.
- [ ] Shu klass ichidan chaqiriladigan `@Transactional`, `@Cacheable`, `@Async` metodlarni toping - ularning hammasi ishlamaydi.
- [ ] `static` mutable maydonlarni (`static Map`, `static List`, `SimpleDateFormat`) grep bilan topib ro'yxat tuzing.
- [ ] Timeout sozlanmagan HTTP mijozlarini aniqlang va har biriga ulanish va o'qish timeout i qo'ying.
- [ ] Smell nomlarini izohda ishlatishni to'xtatib, oqibat tilidagi iboralar jadvalini jamoaga tarqating.

---

[&larr; 11. Dizayn pattern review II: noto'g'ri va ortiqcha qo'llangan pattern](11-dizayn-pattern-review-ii-notogri-va.md) · [Mundarija](README.md) · [13. Domen modeli review: invariant, agregat, chegara &rarr;](13-domen-modeli-review-invariant-agregat.md)
