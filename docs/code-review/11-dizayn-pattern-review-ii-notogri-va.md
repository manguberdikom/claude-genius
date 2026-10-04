<!-- doc: code-review | chapter: 11 | part: II. Arxitektura, dizayn va clean code review -->

[Kod review](../../README.md) / [Kod review](README.md)

# 11. Dizayn pattern review II: noto'g'ri va ortiqcha qo'llangan pattern (Misapplied and Over-Applied Patterns)

<details>
<summary>Bu bobdagi 12 bo'lim</summary>

- [11.1 Noto'g'ri qo'llangan patternning umumiy belgilari](#111-notogri-qollangan-patternning-umumiy-belgilari)
- [11.2 Strategy nomi bor, shoxlanish ham bor](#112-strategy-nomi-bor-shoxlanish-ham-bor)
- [11.3 Fabrika yoki yashirin service locator](#113-fabrika-yoki-yashirin-service-locator)
- [11.4 Repository patternining buzilgan shakllari](#114-repository-patternining-buzilgan-shakllari)
- [11.5 Event noto'g'ri qo'llanganda](#115-event-notogri-qollanganda)
- [11.6 Dekorator zanjiri va kuzatib bo'lmaydigan oqim](#116-dekorator-zanjiri-va-kuzatib-bolmaydigan-oqim)
- [11.7 Singleton, statik holat va Spring](#117-singleton-statik-holat-va-spring)
- [11.8 CQRS, event sourcing va saga: ortiqcha qo'llanish](#118-cqrs-event-sourcing-va-saga-ortiqcha-qollanish)
- [11.9 Mapper va DTO qatlamlarining haddan oshishi](#119-mapper-va-dto-qatlamlarining-haddan-oshishi)
- [11.10 Pattern teatri: nom bilan yashirilgan murakkablik](#1110-pattern-teatri-nom-bilan-yashirilgan-murakkablik)
- [11.11 Pattern review jadvali: belgi, savol, javob](#1111-pattern-review-jadvali-belgi-savol-javob)
- [11.12 Amalda qo'llash](#1112-amalda-qollash)

</details>


Pattern bo'shlig'idan ko'ra xavfliroq holat bor: pattern qo'llangan, nomi to'g'ri, lekin mexanikasi buzilgan. Bunday kod review dan osongina o'tadi, chunki u tanish nomlar bilan bezatilgan. Reviewer `Strategy`, `Factory`, `Repository` so'zini ko'radi va ishonadi. Bu bob shu ishonchni tekshirishni o'rgatadi: pattern nomi ostida nima ishlayotganini ko'rish.

## 11.1 Noto'g'ri qo'llangan patternning umumiy belgilari

| Belgi | Nimani bildiradi |
| --- | --- |
| Pattern nomi klass nomida, lekin mexanikasi yo'q | Nom bezak sifatida ishlatilgan |
| Strategy bor, lekin tanlash `if` bilan | Shoxlanish ko'chmagan, faqat ko'paygan |
| Factory ichida `switch` va `new` | Yaratish markazlashgan, lekin yopiq emas |
| Interfeys bor, bitta implementatsiya | Soxta abstraksiya ([7-bob](07-bogliqlik-koheziya-va-abstraksiya-review.md)) |
| Builder majburiy maydonlarni tekshirmaydi | Xato kompilyatsiyadan ish vaqtiga ko'chgan |
| Repository ichida biznes qoidasi | Qatlam aralashgan |
| Event yuborilgan, lekin tranzaksiya bilan bog'lanmagan | Yetkazish kafolati yo'q |
| Observer tartibga tayanadi | Yashirin vaqt bog'liqligi |
| Singleton `getInstance()` Spring loyihasida | Ikki xil hayot sikli, test qiyin |
| Decorator zanjiri uch darajadan chuqur | Nosozlikni kuzatish imkonsiz |
| Abstract base class bitta vorisi bilan | Meros kodni qayta ishlatish uchun |
| Generic parametr hech qayerda almashmaydi | Ortiqcha ceremony |

## 11.2 Strategy nomi bor, shoxlanish ham bor

Eng ko'p uchraydigan yarim qo'llanish: interfeys va implementatsiyalar yozilgan, lekin ularni tanlash joyida yana `switch` turadi. Natijada kod hajmi oshdi, lekin OCP qo'lga kirmadi - yangi tur qo'shilganda yana shu `switch` ni topish kerak.

```java
// Yarim qo'llanish: Strategy bor, lekin tanlash qo'lda.
@Service
public class FeeService {
    private final CardFee cardFee;
    private final WalletFee walletFee;
    private final CryptoFee cryptoFee;

    public Money fee(Payment p) {
        switch (p.type()) {                       // yangi tur = shu joyni tuzatish
            case CARD -> { return cardFee.of(p); }
            case WALLET -> { return walletFee.of(p); }
            case CRYPTO -> { return cryptoFee.of(p); }
            default -> throw new IllegalStateException();
        }
    }
}

// To'liq qo'llanish: tanlash ham ko'chgan, yangi tur faqat yangi klass.
public interface FeePolicy {
    PaymentType appliesTo();
    Money of(Payment payment);
}

@Service
public class FeeService {
    private final Map<PaymentType, FeePolicy> policies;

    public FeeService(List<FeePolicy> all) {
        this.policies = all.stream().collect(toMap(FeePolicy::appliesTo, identity()));
        // Ishga tushishda to'liqlikni tekshirish: har enum qiymatiga policy bormi.
        EnumSet<PaymentType> missing = EnumSet.allOf(PaymentType.class);
        missing.removeAll(policies.keySet());
        if (!missing.isEmpty()) {
            throw new IllegalStateException("FeePolicy yo'q: " + missing);
        }
    }
    public Money fee(Payment p) { return policies.get(p.type()).of(p); }
}
// Review foydasi: yangi PaymentType qo'shilsa va policy yozilmasa, ilova
// ishga tushishda yiqiladi - prodda jim xato bo'lmaydi. Bu "fail fast"
// yondashuvi Strategy ni polimorfizmdan ham ishonchli qiladi.
```

## 11.3 Fabrika yoki yashirin service locator

`Factory` nomi ostida ko'pincha service locator yashiringan bo'ladi: klass o'z bog'liqliklarini kontekstdan o'zi oladi. Bu bog'liqlikni yashiradi, testni qiyinlashtiradi va ishga tushish vaqtidagi xatoni ish vaqtiga ko'chiradi.

```java
// Service locator: bog'liqlik konstruktorda ko'rinmaydi.
@Component
public class HandlerFactory {
    private final ApplicationContext ctx;          // hamma narsaga kirish

    public Handler forType(String type) {
        return ctx.getBean(type + "Handler", Handler.class);   // satr bo'yicha!
    }
}
// Muammolar: (1) bog'liqlik grafigi ko'rinmaydi, (2) yo'q bean faqat
// chaqiruv paytida xato beradi, (3) bean nomi satr konkatenatsiyasi bilan
// qurilgan - refactoring uni buzadi va kompilyator sezmaydi,
// (4) testda butun kontekst kerak.

// To'g'ri: bog'liqliklar aniq, xato ishga tushishda chiqadi.
@Component
public class Handlers {
    private final Map<EventType, Handler> byType;
    public Handlers(List<Handler> handlers) {
        this.byType = handlers.stream().collect(toMap(Handler::handles, identity()));
    }
    public Handler forType(EventType type) {
        Handler h = byType.get(type);
        if (h == null) throw new NoHandlerFor(type);
        return h;
    }
}
```

## 11.4 Repository patternining buzilgan shakllari

`Repository` eng ko'p noto'g'ri ishlatiladigan nom. Uning mohiyati - domen obyektlari to'plamiga kirish, ma'lumotlar bazasi API si emas. Review da uch xil buzilish uchraydi.

```java
// Buzilish 1: repository ichida biznes qoidasi.
public interface OrderRepository extends JpaRepository<Order, Long> {
    @Query("""
        select o from Order o
        where o.status = 'PAID'
          and o.total > 1000000
          and o.customer.tier = 'GOLD'
        """)
    List<Order> findEligibleForBonus();      // "bonus huquqi" - biznes qoidasi
}
// Review izohi: bonus shartlari JPQL satrida yashiringan. Qoida o'zgarsa,
// uni domen testida emas, repository testida tekshirish kerak bo'ladi, va
// shart kodda qidirilmaydi. Shartni domen (yoki spetsifikatsiya) ga
// ko'chirish, repository ga esa faqat kerakli ma'lumotni olish qoldirish.

// Buzilish 2: repository ichida N+1 keltiradigan qulay metod.
List<Order> findAll();                        // 200 000 qator - keyin filtr Java da

// Buzilish 3: repository tashqariga JPA turlarini chiqaradi.
Page<Order> search(Specification<Order> spec, Pageable page);
// Domen Spring Data turlarini bilib qoladi - port oqib chiqdi (7.6).

// To'g'ri shakl: domen tilida so'rovlar va aniq qaytish turlari.
public interface Orders {                     // domen porti
    Optional<Order> byNumber(OrderNumber number);
    List<Order> awaitingShipment(ShippingWindow window, int limit);
    void save(Order order);
}
```

## 11.5 Event noto'g'ri qo'llanganda

Spring `ApplicationEvent` lari bilan ishlash osonligi tufayli eng ko'p xato shu yerda bo'ladi. Uch xil xato uchraydi va ularning hammasi jim ishlaydi.

```java
// Xato 1: event tranzaksiya ichida sinxron ishlanadi va uni buzadi.
@EventListener
public void on(OrderPlaced e) {
    mailer.send(...);           // tranzaksiya ichida, sekin tashqi chaqiruv
}
// Standart @EventListener sinxron: publish chaqirilgan thread da ishlaydi,
// ya'ni tranzaksiya ichida. Mail serveri sekin bo'lsa, DB tranzaksiyasi
// shuncha uzoq turadi.

// Xato 2: AFTER_COMMIT ishlatilgan, lekin xato yutiladi.
@TransactionalEventListener(phase = AFTER_COMMIT)
public void on(OrderPlaced e) {
    inventory.reserve(e.orderId());   // bu yiqilsa - hech kim bilmaydi,
}                                     // tranzaksiya allaqachon commit bo'lgan

// Xato 3: event ichida entity uzatilgan.
events.publish(new OrderPlaced(order));   // detached entity, lazy maydonlar
// Listener boshqa thread da bo'lsa - LazyInitializationException yoki
// eskirgan holat. Eventda identifikator va immutable qiymatlar bo'lishi kerak.

// To'g'ri shakllar:
// (a) Ichki, muhim bo'lmagan ish - AFTER_COMMIT + xato ishlash.
@TransactionalEventListener(phase = AFTER_COMMIT)
public void sendConfirmation(OrderPlaced e) {
    try { mailer.send(e.orderId()); }
    catch (Exception ex) { log.warn("tasdiq xati yuborilmadi: {}", e.orderId(), ex);
                           meter.counter("mail.failed").increment(); }
}
// (b) Muhim ish (inventar, to'lov) - event emas, outbox (10.8).
// (c) Eventda faqat identifikator va qiymat obyektlari.
public record OrderPlaced(OrderId orderId, Money total, Instant at) { }
```

Review savoli har doim bitta: bu event yo'qolsa, tizim nomuvofiq holatda qoladimi. Javob "ha" bo'lsa, event yetarli emas - kafolatli mexanizm kerak.

## 11.6 Dekorator zanjiri va kuzatib bo'lmaydigan oqim

Dekorator foydali, lekin uch darajadan chuqur zanjir nosozlikni tushunishni imkonsiz qiladi: stack trace da o'nta `invoke` ko'rinadi va qaysi daraja qaror qabul qilganini bilib bo'lmaydi.

```java
// Juda chuqur: beshta o'ram, har biri xulqni o'zgartiradi.
new LoggingRepo(new CachingRepo(new RetryingRepo(new MetricsRepo(new JpaRepo()))));
// Review savollari: kesh retry dan oldinmi yoki keyinmi? Retry keshlangan
// xatoni qaytaradimi? Metrika qaysi darajada o'lchanadi - keshdan oldin
// yoki keyin? Bu savollarning javobi tartibga bog'liq, lekin tartib hech
// qayerda hujjatlashtirilmagan.

// Yaxshiroq: kesishgan vazifalarni framework mexanizmiga topshirish
// (@Cacheable, @Retryable, @Timed) va zanjirni ikki darajada ushlab turish.
// Yoki tartibni aniq e'lon qilish va sabab bilan izohlash:
@Bean
Orders orders(JpaOrders jpa, CacheManager cm, RetryTemplate rt) {
    // Tartib ahamiyatli: retry keshdan ICHKARIDA - keshlangan natija
    // uchun qayta urinish bo'lmaydi, faqat haqiqiy DB xatosi uchun.
    return new CachingOrders(cm, new RetryingOrders(rt, jpa));
}
```

## 11.7 Singleton, statik holat va Spring

Spring loyihasida `getInstance()` ko'rilsa, bu ikki xil hayot sikli degani: Spring bean lari va qo'lda boshqarilgan statik holat. Oqibatlari: testlar bir-biriga ta'sir qiladi, konfiguratsiya ikki joydan keladi, va ishga tushish tartibi aniqlanmaydi.

```java
// Muammo: statik singleton va Spring bean aralashgan.
public class RateCache {
    private static final RateCache INSTANCE = new RateCache();
    public static RateCache getInstance() { return INSTANCE; }
    private final Map<String, BigDecimal> rates = new HashMap<>();  // thread-safe emas
    public void put(String c, BigDecimal r) { rates.put(c, r); }
}
// Review izohlari: (1) HashMap bir vaqtda o'qilib va yozilsa - buzilish
// yoki cheksiz sikl; (2) testlar orasida holat saqlanadi, test tartibi
// natijaga ta'sir qiladi; (3) kesh hajmi cheklanmagan - xotira o'sadi.

// To'g'ri: bean, aniq kesh, cheklangan hajm va TTL.
@Configuration
class CacheConfig {
    @Bean
    Cache<String, BigDecimal> rateCache() {
        return Caffeine.newBuilder()
                       .maximumSize(1_000)            // hajm cheklangan
                       .expireAfterWrite(Duration.ofMinutes(10))   // yangilik oynasi
                       .recordStats()                 // metrikaga ulanadi
                       .build();
    }
}
```

## 11.8 CQRS, event sourcing va saga: ortiqcha qo'llanish

Bu uchlik eng qimmat patternlar va eng ko'p asossiz qo'llanadigan patternlar. Review da ularning har biri uchun aniq shart bor; shart bajarilmasa, narx foydadan katta.

| Pattern | Qo'llashga asos bo'ladigan shart | Shart yo'q bo'lsa narxi |
| --- | --- | --- |
| CQRS (alohida o'qish modeli) | O'qish yuki yozuvdan bir necha baravar katta, yoki o'qish shakli yozuvdan tubdan farq qiladi | Ikki model sinxronizatsiyasi, eventual consistency bilan bog'liq xatolar, ikki baravar kod |
| Event sourcing | Tarix va auditning o'zi biznes talabi; holatni qayta hisoblash kerak | Migratsiya murakkabligi, so'rovlar uchun proyeksiya, yangi odam uchun yuqori yuk |
| Saga | Bir operatsiya uch va ko'p mustaqil tizimga tegadi | Holat jadvali, worker, kompensatsiya, kuzatish - oddiy tranzaksiya yetadigan joyda |
| Microservice ajratish | Mustaqil deploy va mustaqil masshtablash kerak | Tarmoq, kuzatish, taqsimlangan tranzaksiya muammolari |
| Hexagonal to'liq shakli | Bir nechta tashqi adapter real almashtiriladi | Har oddiy maydon uchun to'rt klass |

```text
# Review izohi: ortiqcha patternni rad etishning to'g'ri shakli.
question: Bu PR da buyurtma o'qish uchun alohida proyeksiya jadvali va
uni to'ldiradigan listener qo'shilgan (CQRS). Uch savol:

1) Hozirgi o'qish yuki qancha? Metrikada buyurtma o'qish p99 = 40 ms,
   kuniga 12 ming so'rov - bu bitta jadval uchun katta yuk emas.
2) Proyeksiya kechikishi biznes uchun qabul qilinadimi? Foydalanuvchi
   buyurtma yaratib, darhol ro'yxatda ko'rmasligi mumkin.
3) Proyeksiya buzilsa (listener xatosi), uni qanday qayta quramiz?

Agar maqsad faqat so'rovni tezlashtirish bo'lsa, avval indeks va
projection interfeysi bilan o'lchab ko'rsak - narxi nol. CQRS ga o'tish
uchun o'lchangan dalil bo'lsa, qaytib kelamiz va ADR yozamiz.
```

## 11.9 Mapper va DTO qatlamlarining haddan oshishi

Har qatlam uchun alohida model yaratish qoidasi mexanik qo'llanganda, bitta maydon qo'shish uchun olti faylga tegish kerak bo'ladi.

```text
Request DTO -> Command -> Domain -> Entity -> Projection -> Response DTO
```

Review mezoni - har bir model alohida sababga ko'ra o'zgaradimi. Agar `Command` va `Request DTO` har doim birga o'zgarsa va maydonlari bir xil bo'lsa, ular bitta model. Teskarisi ham to'g'ri: tashqi API shakli va jadval sxemasi mustaqil o'zgarsa, ularni ajratish zarur.

| Chegara | Ajratish kerakmi | Sabab |
| --- | --- | --- |
| Tashqi API va domen | Ha | API shartnomasi, versiyalash, orqaga moslik |
| Domen va jadval | Odatda ha | Sxema migratsiyasi, ORM talablari |
| Request DTO va Command | Odatda yo'q | Bir xil sababga ko'ra o'zgaradi |
| O'qish javobi va entity | Ha | Projection samaraliroq, ortiqcha maydon chiqmaydi |
| Ichki servislar orasida | Yo'q | Bir xil deploy birligi |

## 11.10 Pattern teatri: nom bilan yashirilgan murakkablik

Eng qiyin holat - kod pattern nomlari bilan to'lgan, lekin hech bir pattern o'z vazifasini bajarmaydi. Belgilari: `AbstractBaseServiceFactoryProvider` tipidagi nomlar, uch daraja meros, har bir interfeysga bitta implementatsiya, va eng oddiy operatsiya uchun o'n faylga sakrash.

Bunday PR ni review qilishning to'g'ri usuli - bitta oddiy ssenariyni oxirigacha kuzatish va necha faylga sakrash kerakligini sanash. Keyin shu sonni izohda ko'rsatish: "bitta buyurtma yaratish yo'lini tushunish uchun 11 fayl ochish kerak bo'ldi". Bu raqam did bahsidan ko'ra ishonchliroq dalil.

```bash
# Murakkablikni raqamda ko'rsatish: bitta operatsiya yo'lidagi fayllar.
# Chaqiruv zanjirini kuzatish (IDE bo'lmaganda ham ishlaydi).
start='placeOrder'
for i in 1 2 3 4 5; do
  echo "--- daraja $i: $start"
  grep -rn --include='*.java' "$start(" src/main/java | head -5
  # keyingi darajaga qo'lda o'tiladi; maqsad - sakrash sonini sanash
done

# Meros chuqurligi: uch darajadan chuqur ierarxiyalar.
grep -rn --include='*.java' 'extends Abstract' src/main/java | wc -l
```

## 11.11 Pattern review jadvali: belgi, savol, javob

| Ko'rilgan narsa | Review savoli | Yaxshi javob bo'lmasa |
| --- | --- | --- |
| Yangi interfeys | Ikkinchi implementatsiya bormi yoki rejadami | Interfeysni olib tashlash |
| Yangi `Abstract` klass | Nechta vorisi bo'ladi, umumiy kod shartnomaga tegishlimi | Kompozitsiya |
| Strategy + `switch` | Tanlash nega ko'chmagan | Registr yoki enum xulqi |
| Factory + `ApplicationContext` | Bog'liqliklar nega ko'rinmaydi | Konstruktor inyeksiyasi |
| Builder | Majburiy maydonlar qayerda tekshiriladi | `build()` da tekshirish yoki record |
| Event | Yo'qolsa nima bo'ladi | Outbox yoki sinxron chaqiruv |
| `@Async` | Xato qayerga boradi, pool qaysi | `AsyncUncaughtExceptionHandler` va aniq pool |
| Kesh | Invalidatsiya qachon, hajmi cheklanganmi | TTL, maksimal hajm, metrika |
| Yangi proyeksiya jadvali | Qayta qurish yo'li bormi | Oddiy indeks bilan boshlash |
| Saga | Har qadam idempotentmi | Holatni jadvalga yozish |
| Decorator zanjiri | Tartib nega shunday | Framework mexanizmiga o'tkazish |
| Generic parametr | Qayerda almashadi | Konkret turga tushirish |

## 11.12 Amalda qo'llash

- [ ] Loyihada `Strategy`, `Factory`, `Provider`, `Manager` nomli klasslarni toping va har birida pattern mexanikasi haqiqatda ishlayotganini tekshiring.
- [ ] `ApplicationContext` yoki `BeanFactory` inyeksiya qilingan joylarni toping - har biri yashirin service locator.
- [ ] `getBean("..." + suffix)` shaklidagi satr bilan bean izlashni butunlay olib tashlang.
- [ ] Strategy registrlariga ishga tushish vaqtidagi to'liqlik tekshiruvini qo'shing (har enum qiymatiga implementatsiya bormi).
- [ ] Repository interfeyslarini ko'rib chiqing: JPQL ichida biznes sharti bor metodlarni aniqlab, qoidani domenga ko'chirishni rejalashtiring.
- [ ] Barcha `@EventListener` larni sanab, qaysilari `@TransactionalEventListener` bo'lishi kerakligini va qaysilari outbox ga o'tishi kerakligini belgilang.
- [ ] Eventlarda entity uzatilgan joylarni toping va ularni identifikator va qiymat obyektlariga o'tkazing.
- [ ] `getInstance()` va statik mutable holatni grep bilan topib, bean ga o'tkazish ro'yxatini tuzing.
- [ ] Hajmi va TTL si cheklanmagan keshlarni toping - har biri potensial xotira muammosi.

---

[&larr; 10. Dizayn pattern review I: yo'q patternni ko'rish](10-dizayn-pattern-review-i-yoq-patternni-korish.md) · [Mundarija](README.md) · [12. Code smell va anti-pattern katalogi diffda &rarr;](12-code-smell-va-anti-pattern-katalogi-diffda.md)
