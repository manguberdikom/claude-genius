<!-- doc: code-review | chapter: 11 | part: II. Arxitektura, dizayn va clean code review -->

[Barcha hujjatlar](../../README.md) / [Kod review](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

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

Bobning ikki o'lchovi ikki kitobdagi ogohlantirishdan keladi. Birinchisi -
patternning narxi. GoF patternlarni qanday ishlatish bo'limini shu gap bilan
yopadi: patternlar tanlab ishlatilmasdan qo'llanmasligi kerak, chunki ular
moslashuvchanlikka ko'pincha qo'shimcha bilvosita qatlamlar kiritib erishadi, bu
dizaynni murakkablashtiradi va unumdorlikka tushadi; pattern faqat bergan
moslashuvchanlik haqiqatda kerak bo'lganda qo'llanadi, va uni baholashda
patternning Consequences bo'limi eng foydali (GoF, 1.8-bo'lim, 31-bet).
Head First xuddi shu fikrni ochiq ogohlantirish qilib qo'yadi: patternni
ortiqcha ishlatish overengineered kodga olib keladi, shuning uchun har doim
ishni bajaradigan eng oddiy yechim tanlanadi va pattern ehtiyoj paydo bo'lganda
kiritiladi; pattern ba'zan butunlay overkill bo'ladi va dizayn printsiplariga
qaytib ancha oddiy yechim topish mumkin (Freeman/Robson, 584-bet). Kitob
patternlarni "shunchaki ishlatish uchun" boshlashni ham alohida rad etadi:
patternlar ma'noli bo'lgan joyda qo'llanadi (Freeman/Robson, 516-bet).

Ikkinchi o'lchov - niyat. Patternning tanib olinadigan belgisi strukturasi emas,
niyati. GoF strukturaviy patternlar muhokamasida shuni ko'rsatadi: Decorator va
Proxy, Decorator va Composite, Adapter va Bridge strukturasi o'xshash, lekin
o'xshashlik niyatlardagi farqni yashiradi va shu farq amaliy ahamiyatga ega (GoF,
219-220-bet). Head First ham Strategy va State uchun shu xulosaga keladi:
struktura bir xil, niyat butunlay boshqa (Freeman/Robson, 381 va 414-415-bet).
Review da savol shundan tug'iladi: nom qo'yilgan, lekin shu nomning niyati bu
kodda bajarilayaptimi.

## 11.1 Noto'g'ri qo'llangan patternning umumiy belgilari

| Belgi | Nimani bildiradi |
| --- | --- |
| Pattern nomi klass nomida, lekin mexanikasi yo'q | Nom bezak sifatida ishlatilgan |
| Strategy bor, lekin tanlash `if` bilan | Shoxlanish ko'chmagan, faqat ko'paygan |
| Factory ichida `switch` va `new` | Yaratish markazlashgan, lekin yopiq emas |
| Repository ichida JPA turlari tashqariga chiqadi | Domen ma'lumot qatlamiga bog'lanib qoldi |
| Interfeys bor, bitta implementatsiya | Soxta abstraksiya ([7-bob](07-bogliqlik-koheziya-va-abstraksiya-review.md)) |
| Builder majburiy maydonlarni tekshirmaydi | Xato kompilyatsiyadan ish vaqtiga ko'chgan |
| Repository ichida biznes qoidasi | Qatlam aralashgan |
| Event yuborilgan, lekin tranzaksiya bilan bog'lanmagan | Yetkazish kafolati yo'q |
| Observer lar bir-birining tartibiga tayanadi | Kutilmagan yangilanish: kuzatuvchilar bir-birini bilmaydi (GoF, 296-bet) |
| Singleton `getInstance()` Spring loyihasida | Ikki xil hayot sikli, test qiyin |
| Statik mutable holat | Global ma'lumot: "aybsizligi isbotlanmagan" (Fowler, PoEAA, 483-bet) |
| Decorator zanjiri chuqur | Ko'p kichik klass, API ni tushunish qiyinlashadi (Freeman/Robson, 101-bet) |
| Abstract base class bitta vorisi bilan | Meros kodni qayta ishlatish uchun |
| Generic parametr hech qayerda almashmaydi | Ortiqcha ceremony |

Jadvaldagi har qator bir xil savolga olib keladi: nomning niyati bajarilayaptimi.
Masalan `Strategy` nomi bor, lekin tanlash `if` da qolgan bo'lsa, GoF ning Strategy
niyati - algoritmlar oilasini qamrab olib ularni almashtirib ishlatiladigan qilish va
algoritmni uni ishlatadigan klientlardan mustaqil o'zgartirish (GoF, 315-bet) -
bajarilmaydi, chunki klient hali ham har algoritmni biladi.

## 11.2 Strategy nomi bor, shoxlanish ham bor

Eng ko'p uchraydigan yarim qo'llanish: interfeys va implementatsiyalar yozilgan, lekin ularni tanlash joyida yana `switch` turadi. Natijada kod hajmi oshdi, lekin OCP qo'lga kirmadi - yangi tur qo'shilganda yana shu `switch` ni topish kerak.

Nega bu yarim qo'llanish, kitobdan ko'rinadi. GoF da Strategy ning niyati -
algoritmlar oilasini qamrab olish, har birini alohida inkapsulyatsiya qilish va
ularni almashtirib ishlatiladigan qilish, shunda algoritm uni ishlatadigan
klientlardan mustaqil o'zgaradi (GoF, 315-bet). GoF ning Collaborations bo'limi
mexanikani ham aytadi: klient odatda bitta ConcreteStrategy obyektini yaratib
Context ga beradi va shundan keyin faqat Context bilan ishlaydi (GoF, 318-bet).
Yuqoridagi `switch` da esa `FeeService` uch implementatsiyaning hammasini biladi:
algoritm klientdan mustaqil o'zgarmadi, faqat uch sinfga ko'chdi. Diffdan qolgan
`switch` ning kitobdagi nomi ham bor - uni yo'qotadigan refaktoring Fowler da
*Replace Conditional with Polymorphism* deb ataladi (1999, 205-bet).

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
// ishga tushishda yiqiladi - prodda jim xato bo'lmaydi.
```

Registrni ishga tushishda to'liqlikka tekshirish - shu korpusning amaliy qo'shimchasi,
kitoblardagi Strategy tavsifida bunday qadam yo'q. Kitobdan keladigan talab boshqa:
klient algoritmlarni emas, faqat Context ni bilsin (GoF, 318-bet).

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

Bu yerda ikki nom aralashtirilmasin. Yuqoridagi `HandlerFactory` GoF ning Factory
Method i emas: GoF da Factory Method obyekt yaratish uchun interfeys e'lon qiladi
va qaysi sinf yaratilishini subclasslar hal qiladi (GoF, 107-bet), bu yerda esa
hech qanday subclass yo'q - kontekstdan nom bo'yicha bean olinadi. Uning aslidagi
shakli - Fowler ning Registry i: bir obyekt boshqa obyektlarni topish uchun
murojaat qiladigan ma'lum joy (Fowler, *Patterns of Enterprise Application
Architecture*, 480-bet). Fowler Registry ni ishlatishga ruxsat beradi, lekin
ikki shartni qo'yadi, va ikkisi ham yuqoridagi kodda buzilgan: yalang'och map
inkapsulyatsiya qilinmagan va statik tipli tilda tur xavfsizligini saqlamaydi,
shuning uchun aniq klass afzal; va umumiy xulosasi - har qanday global ma'lumot
aybsizligi isbotlanmaguncha aybdor (PoEAA, 482-483-bet). Satr konkatenatsiyasi
bilan bean izlash aynan tur xavfsizligini yo'qotadigan shakl.

## 11.4 Repository patternining buzilgan shakllari

`Repository` eng ko'p noto'g'ri ishlatiladigan nom, chunki uning ta'rifi
ma'lumotlar bazasi API si emas. Patternni kiritgan kitobda Repository domen va
ma'lumotlarni moslashtirish qatlamlari orasida vositachi bo'ladi va xotiradagi
domen obyektlari to'plami kabi o'zini tutadi: klient so'rov shartini deklarativ
ravishda tuzib unga beradi, obyekt oddiy to'plamga qo'shilgani va undan
olingani kabi qo'shiladi va olinadi, kerakli baza operatsiyalarini esa
inkapsulyatsiya qilingan moslashtirish kodi orqa planda bajaradi; patternning
maqsadlaridan biri - domen va ma'lumotlarni moslashtirish qatlamlari orasida
toza ajratish va bir tomonlama bog'liqlik (Fowler, *Patterns of Enterprise
Application Architecture*, 322-323-bet). Review da shu ta'rifning uch xil
buzilishi uchraydi.

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

Uch buzilishning hammasi bitta ta'rifga urinadi. Birinchisi domen qoidasini
moslashtirish qatlamiga tushiradi, ya'ni bir tomonlama bog'liqlikni teskari
qiladi. Ikkinchisi "xotiradagi to'plam" taassurotini haqiqatan xotiraga
ko'chiradi. Uchinchisi inkapsulyatsiyani buzadi: Repository ning vazifasi baza
operatsiyalarini orqa planda ushlab turish edi (PoEAA, 322-323-bet), JPA turlari
interfeysda ko'rinsa esa ular ushlanmaydi va port oqib chiqadi (7.6).

## 11.5 Event noto'g'ri qo'llanganda

Spring `ApplicationEvent` lari bilan ishlash osonligi tufayli eng ko'p xato shu yerda bo'ladi. Uch xil xato uchraydi va ularning hammasi jim ishlaydi.

Patternning o'zi bu xatolarni oldindan aytib qo'ygan. GoF da Observer ning niyati
obyektlar orasida bir-ko'p bog'liqlikni aniqlash: bir obyekt holatini o'zgartirsa,
unga tobelar avtomatik xabardor qilinadi va yangilanadi (GoF, 293-bet). GoF
sanaydigan foyda - subyekt va kuzatuvchi orasidagi bog'liqlikning abstrakt
bo'lishi va translyatsiya shaklida xabar berish; uchinchi oqibati esa aynan
ogohlantirish: kuzatuvchilar bir-birining borligini bilmagani uchun subyektni
o'zgartirishning haqiqiy narxini ko'rmaydi, zararsiz ko'rinadigan operatsiya
kuzatuvchilar va ularga tobe obyektlar bo'ylab yangilanish kaskadini keltirib
chiqaradi, va aniq belgilanmagan bog'liqlik shartlari izlash qiyin bo'lgan
bekorchi yangilanishlarga olib keladi (GoF, 296-bet). Tranzaksiya ichida mail
yuborish - shu kaskadning narxi.

GoF Notify ni kim chaqirishini ham alohida masala qilib qo'yadi: holatni
o'zgartiradigan operatsiya o'zi chaqirsa klient eslab turishi kerak emas, lekin
ketma-ket bir necha operatsiya ketma-ket bir necha yangilanish beradi; klient
chaqirsa esa bir qator o'zgarishdan keyin bir marta xabar berish mumkin, lekin
klient uni chaqirishni esdan chiqarishi mumkin (GoF, 297-bet). Spring da bu
tanlov `@EventListener` va `@TransactionalEventListener` orasidagi tanlovga
aylanadi.

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

Review savoli har doim bitta: bu event yo'qolsa, tizim nomuvofiq holatda qoladimi. Javob "ha" bo'lsa, event yetarli emas - kafolatli mexanizm kerak. Kafolatli mexanizmning
nomi va shakli Richardson da: xabar ma'lumotlar bazasi tranzaksiyasining bir qismi
sifatida OUTBOX jadvaliga yoziladi, shuning uchun atomiklik bitta lokal ACID
tranzaksiyadan keladi (Richardson, 3-bob, 98-bet).

## 11.6 Dekorator zanjiri va kuzatib bo'lmaydigan oqim

Dekorator foydali, lekin zanjir chuqurlashgani sari nosozlikni tushunish
qiyinlashadi: stack trace o'ramlarning `invoke` chaqiruvlari bilan to'ladi va
qaysi daraja qaror qabul qilganini bilib bo'lmaydi.

Buning kitobdagi asosi bor. GoF Decorator ning kuchini rekursiv kompozitsiyada
ko'radi: komponent funksiyaning faqat bir qismini beradi, qolganini bir yoki bir
nechta dekorator qo'shadi, va obyektning to'liq funksiyasi kompilyatsiya paytida
aniqlanmagani uchun rekursiv kompozitsiya Decorator ning ajralmas qismi bo'ladi
(GoF, 220-bet). Narxi ham shu yerdan: Head First Java I/O ni misol qilib
Decorator ning kamchiligini aytadi - bu pattern bilan qurilgan dizaynlar
ko'pincha juda ko'p kichik klass beradi, va bu Decorator ga asoslangan API ni
ishlatmoqchi bo'lgan dasturchi uchun og'ir bo'ladi (Freeman/Robson, 101-bet).

Shuni ham ajratish kerak: pastdagi zanjirning ba'zi darajalari aslida Decorator
emas. Kesh va retry mas'uliyat qo'shadi, ya'ni Decorator; kirishni tekshiradigan
yoki real obyektni kechiktirib yaratadigan o'ram esa Proxy, chunki GoF da asosiy
funksiyani subyekt beradi va proxy unga kirishga ruxsat beradi yoki rad etadi
(GoF, 207 va 220-bet).

```java
// Juda chuqur: beshta o'ram, har biri xulqni o'zgartiradi.
new LoggingRepo(new CachingRepo(new RetryingRepo(new MetricsRepo(new JpaRepo()))));
// Review savollari: kesh retry dan oldinmi yoki keyinmi? Retry keshlangan
// xatoni qaytaradimi? Metrika qaysi darajada o'lchanadi - keshdan oldin
// yoki keyin? Bu savollarning javobi tartibga bog'liq, lekin tartib hech
// qayerda hujjatlashtirilmagan.

// Yaxshiroq: kesishgan vazifalarni framework mexanizmiga topshirish
// (@Cacheable, @Retryable, @Timed) va zanjirni qisqa ushlab turish.
// Yoki tartibni aniq e'lon qilish va sabab bilan izohlash:
@Bean
Orders orders(JpaOrders jpa, CacheManager cm, RetryTemplate rt) {
    // Tartib ahamiyatli: retry keshdan ICHKARIDA - keshlangan natija
    // uchun qayta urinish bo'lmaydi, faqat haqiqiy DB xatosi uchun.
    return new CachingOrders(cm, new RetryingOrders(rt, jpa));
}
```

Zanjir uchun aniq chuqurlik chegarasi (ikki daraja, uch daraja) kitoblarda yo'q.
Kitobdan keladigan talab sifat talabi: zanjirning har darajasi niyati bo'yicha
oqlanishi va tartibi sabab bilan izohlanishi kerak, chunki tartib natijani
o'zgartiradi. Review izohi shuning uchun "zanjir chuqur" emas, "kesh retry dan
oldinmi yoki keyinmi va nega" shaklida yoziladi.

## 11.7 Singleton, statik holat va Spring

Spring loyihasida `getInstance()` ko'rilsa, bu ikki xil hayot sikli degani: Spring bean lari va qo'lda boshqarilgan statik holat. Oqibatlari: testlar bir-biriga ta'sir qiladi, konfiguratsiya ikki joydan keladi, va ishga tushish tartibi aniqlanmaydi.

GoF da Singleton ning niyati - sinfda faqat bitta instans borligini ta'minlash va
unga global kirish nuqtasini berish (GoF, 127-bet). Diqqat qiladigan joy shu:
GoF ning o'zi singletonni statik metodlar orqali qurishni afzal shakl deb
hisoblamaydi. Uning beshinchi oqibati - Singleton sinf operatsiyalaridan
moslashuvchanroq, chunki statik metodlar bilan qurilgan shaklda dizaynni bir
instansdan ko'proq instansga ruxsat beradigan holga o'zgartirish qiyin bo'ladi
(GoF, 128-bet). Spring bean i aynan shu moslashuvchanlikni beradi: bir xil sinfdan
ikki bean, test uchun boshqa instans, profil bo'yicha boshqa konfiguratsiya.

Fowler statik holatni umumiy qoida bilan baholaydi: har qanday global ma'lumot
aybsizligi isbotlanmaguncha aybdor (PoEAA, 483-bet). Review da shu shaklda
ishlatiladi - `getInstance()` o'z-o'zidan xato emas, lekin oqlanishi so'raladi.

```java
// Muammo: statik singleton va Spring bean aralashgan.
public class RateCache {
    private static final RateCache INSTANCE = new RateCache();
    public static RateCache getInstance() { return INSTANCE; }
    private final Map<String, BigDecimal> rates = new HashMap<>();  // thread-safe emas
    public void put(String c, BigDecimal r) { rates.put(c, r); }
}
// Review izohlari: (1) HashMap thread-safe emas, bir vaqtda o'qilib va
// yozilsa holat buziladi ([15-bob](15-holat-mutability-va-concurrency-review.md));
// (2) testlar orasida holat saqlanadi, test tartibi natijaga ta'sir qiladi;
// (3) kesh hajmi cheklanmagan - xotira o'sadi.

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

Bu uchlik qimmat, va shart bajarilmasa narx foydadan katta bo'ladi. Shartlar
jadvalidagi qatorlarning bir qismi kitobdan keladi.

CQRS uchun Richardson ikki kamchilikni sanaydi: arxitektura murakkablashadi,
chunki so'rov tomonidagi servislarni yozish, qo'shimcha ma'lumot omborlarini
boshqarish va ishlatish kerak bo'ladi; va replikatsiya kechikishi bilan ishlash
kerak, chunki buyruq tomoni event e'lon qilishi va so'rov tomoni uni ishlab
ko'rinishni yangilashi orasida kechikish bor, shuning uchun agregatni yangilab
darhol so'rov yuborgan klient oldingi versiyani ko'rishi mumkin. Richardson ning
tavsiyasi ham aniq: imkon bo'lgan joyda API kompozitsiyasi ishlatiladi va CQRS
faqat majbur bo'lganda qo'llanadi (Richardson, 7.2.4-bo'lim, 236-bet).

Event sourcing uchun Richardson beshta kamchilikni sanaydi: o'rganish egri
chizig'i bor boshqa programmalash modeli (mavjud ilovada biznes mantiqini qayta
yozish kerak), xabarga asoslangan ilovaning murakkabligi, eventlarni rivojlantirish
qiyinligi (eventlar abadiy saqlanadi, shuning uchun agregat bir necha sxema
versiyasini qayta ishlashga majbur bo'lishi mumkin), ma'lumotni o'chirish
qiyinligi va event omborini so'rov qilishning qiyinligi (Richardson,
6.1.9-bo'lim, 200-202-bet).

Saga uchun shart patternning ta'rifidan kelib chiqadi: saga bir necha servisdagi
ma'lumotni yangilashi kerak bo'lgan tizim buyrug'i uchun aniqlanadi, va unda
ACID tranzaksiyaning izolyatsiya xususiyati yo'q, qaytarish esa faqat
kompensatsiya tranzaksiyalari bilan mumkin (Richardson, 4-bob, 114-bet). Bitta
servis va bitta baza bo'lsa shart bajarilmaydi.

| Pattern | Qo'llashga asos bo'ladigan shart | Shart yo'q bo'lsa narxi |
| --- | --- | --- |
| CQRS (alohida o'qish modeli) | API kompozitsiyasi yetmaydi: so'rov shakli yozuv modelidan tubdan farq qiladi | Murakkabroq arxitektura, qo'shimcha ombor, replikatsiya kechikishi (Richardson, 236-bet) |
| Event sourcing | Agregatlar tarixining o'zi talab | Boshqa programmalash modeli, event sxemasini rivojlantirish, o'chirish va so'rov qilish qiyinligi (Richardson, 200-202-bet) |
| Saga | Bir operatsiya bir necha servisdagi ma'lumotni yangilaydi | Izolyatsiya yo'qligi va kompensatsiya tranzaksiyalari (Richardson, 114-bet) |
| Microservice ajratish | Mustaqil deploy va mustaqil masshtablash kerak | Tarmoq, kuzatish, taqsimlangan ma'lumot muvofiqligi muammolari |
| Qo'shimcha bilvosita qatlam (port, adapter, generik interfeys) | Bergan moslashuvchanlik haqiqatda kerak | Murakkablashgan dizayn va unumdorlik yo'qotishi (GoF, 31-bet) |

Rad etishning to'g'ri shakli - shartni o'lchab ko'rsatishni so'rash, nomni rad
etish emas. Quyidagi izoh namunasi; undagi raqamlar o'rniga PR ning o'z
metrikasi qo'yiladi.

```text
# Review izohi: ortiqcha patternni rad etishning to'g'ri shakli (raqamlar namuna).
question: Bu PR da buyurtma o'qish uchun alohida proyeksiya jadvali va
uni to'ldiradigan listener qo'shilgan (CQRS). Uch savol:

1) Hozirgi o'qish yuki qancha? Metrikada buyurtma o'qish p99 = 40 ms,
   kuniga 12 ming so'rov - bu bitta jadval uchun katta yuk emas.
2) Proyeksiya kechikishi biznes uchun qabul qilinadimi? Foydalanuvchi
   buyurtma yaratib, darhol ro'yxatda ko'rmasligi mumkin.
3) Proyeksiya buzilsa (listener xatosi), uni qanday qayta quramiz?

Agar maqsad faqat so'rovni tezlashtirish bo'lsa, avval indeks va
projection interfeysi bilan o'lchab ko'rsak. CQRS ga o'tish uchun
o'lchangan dalil bo'lsa, qaytib kelamiz va ADR yozamiz.
```

## 11.9 Mapper va DTO qatlamlarining haddan oshishi

Har qatlam uchun alohida model yaratish qoidasi mexanik qo'llanganda, bitta maydon qo'shish uchun olti faylga tegish kerak bo'ladi.

Nomning kelib chiqishi bu qoidani oqlamaydi. Fowler da Data Transfer Object ning
ta'rifi - metod chaqiruvlari sonini kamaytirish uchun ma'lumotni processlar
orasida olib yuradigan obyekt, va u masofaviy interfeys bilan ishlaganda har
chaqiruv qimmat bo'lgani uchun paydo bo'ladi (PoEAA, 401-bet). Qachon ishlatish
sharti ham shunga mos: DTO bitta metod chaqiruvida ikki process orasida bir
nechta ma'lumotni uzatish kerak bo'lganda ishlatiladi (PoEAA, 406-bet). Bitta
process ichidagi har qatlam uchun alohida model yaratish bu shartdan kelib
chiqmaydi.

```text
Request DTO -> Command -> Domain -> Entity -> Projection -> Response DTO
```

Review mezoni - har bir model alohida sababga ko'ra o'zgaradimi. Agar `Command` va `Request DTO` har doim birga o'zgarsa va maydonlari bir xil bo'lsa, ular bitta model. Teskarisi ham to'g'ri: tashqi API shakli va jadval sxemasi mustaqil o'zgarsa, ularni ajratish zarur. Quyidagi jadval shu mezonning shu korpusdagi
amaliy qo'llanishi, kitobdan ko'chirilgan taksonomiya emas.

| Chegara | Ajratish kerakmi | Sabab |
| --- | --- | --- |
| Tashqi API va domen | Ha | API shartnomasi, versiyalash, orqaga moslik |
| Domen va jadval | Odatda ha | Sxema migratsiyasi, ORM talablari |
| Request DTO va Command | Odatda yo'q | Bir xil sababga ko'ra o'zgaradi |
| O'qish javobi va entity | Ha | Projection samaraliroq, ortiqcha maydon chiqmaydi |
| Ichki servislar orasida | Yo'q | Bir xil deploy birligi |

## 11.10 Pattern teatri: nom bilan yashirilgan murakkablik

Eng qiyin holat - kod pattern nomlari bilan to'lgan, lekin hech bir pattern o'z vazifasini bajarmaydi. Belgilari: `AbstractBaseServiceFactoryProvider` tipidagi nomlar, uch daraja meros, har bir interfeysga bitta implementatsiya, va eng oddiy operatsiya uchun o'n faylga sakrash.

Bunday PR ni review qilishning to'g'ri usuli - bitta oddiy ssenariyni oxirigacha kuzatish va necha faylga sakrash kerakligini sanash. Keyin shu sonni izohda ko'rsatish: "bitta buyurtma yaratish yo'lini tushunish uchun 11 fayl ochish kerak bo'ldi" (son o'lchangan bo'lishi kerak, taxmin emas). Bu raqam did bahsidan ko'ra ishonchliroq dalil.

Ikki kitob ham shu holatni oldindan nomlab qo'ygan. GoF patternlar
moslashuvchanlikka qo'shimcha bilvosita qatlamlar kiritib erishishini va bu
dizaynni murakkablashtirishini aytadi, shuning uchun pattern faqat bergan
moslashuvchanlik haqiqatda kerak bo'lganda qo'llanadi (GoF, 31-bet). Head First
esa buni to'g'ridan-to'g'ri ogohlantirish qilib qo'yadi: patternni ortiqcha
ishlatish overengineered kodga olib keladi, har doim ishni bajaradigan eng oddiy
yechim tanlanadi va pattern ehtiyoj paydo bo'lganda kiritiladi (Freeman/Robson,
584-bet). Pattern teatri - shu ikki ogohlantirishning bir vaqtda buzilishi:
bilvosita qatlamlar bor, lekin ular bergan moslashuvchanlikdan foydalanilmaydi
(har interfeysga bitta implementatsiya).

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

## Manbalar

- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns: Elements of Reusable Object-Oriented Software*, Addison-Wesley, 1995, 1.8-bo'lim (31-bet) - pattern tanlab ishlatilmasdan qo'llanmaydi: bilvosita qatlam dizaynni murakkablashtiradi va unumdorlikka tushadi; baholashda Consequences bo'limi ishlatiladi
- GoF, *Design Patterns*, 1995, 3-bob (107, 127-128-bet) - Factory Method niyati (subclass qaysi sinf yaratilishini hal qiladi); Singleton niyati va uning beshinchi oqibati: statik sinf operatsiyalari bilan qurilgan shaklda bir instansdan ko'proqqa o'tish qiyin
- GoF, *Design Patterns*, 1995, 4-bob (207, 219-220-bet) - Proxy niyati; strukturaviy patternlar muhokamasi: o'xshash struktura niyatlardagi farqni yashiradi, Decorator da rekursiv kompozitsiya ajralmas, Proxy da subyekt asosiy funksiyani beradi
- GoF, *Design Patterns*, 1995, 5-bob (293, 296, 297, 315, 318-bet) - Observer niyati va uchinchi oqibati "kutilmagan yangilanish"; Notify ni kim chaqirishi masalasi; Strategy niyati va klient Context bilan ishlashi
- Martin Fowler, *Refactoring: Improving the Design of Existing Code*, 1-nashr, Addison-Wesley, 1999, 9-bob (205-bet) - Replace Conditional with Polymorphism: Strategy yonida qolgan `switch` ni yo'qotadigan refaktoringning nomi
- Martin Fowler, *Patterns of Enterprise Application Architecture*, Addison-Wesley, 2003, 13-bob (322-323-bet) - Repository: domen va ma'lumotlarni moslashtirish qatlamlari orasidagi vositachi, xotiradagi domen obyektlari to'plami kabi, baza operatsiyalari inkapsulyatsiya qilinadi
- Fowler, *Patterns of Enterprise Application Architecture*, 2003, 15-bob (401 va 406-bet) - Data Transfer Object: processlar orasida ma'lumot uzatib chaqiruv sonini kamaytiradi; bir metod chaqiruvida ikki process orasida ko'p ma'lumot uzatish kerak bo'lganda ishlatiladi
- Fowler, *Patterns of Enterprise Application Architecture*, 2003, 18-bob (480 va 482-483-bet) - Registry: obyektlarni topishning ma'lum joyi; yalang'och map inkapsulyatsiya qilinmaydi va tur xavfsizligini bermaydi; har qanday global ma'lumot aybsizligi isbotlanmaguncha aybdor
- Eric Freeman, Elisabeth Robson, *Head First Design Patterns*, 2-nashr, O'Reilly, 2021, 3-bob (101-bet) - Decorator ning kamchiligi: dizayn ko'pincha juda ko'p kichik klass beradi va API ni ishlatish qiyinlashadi
- Freeman/Robson, *Head First Design Patterns*, 2-nashr, 2021, 10-bob (381, 414-415-bet) - Strategy va State strukturasi o'xshash, niyati butunlay boshqa
- Freeman/Robson, *Head First Design Patterns*, 2-nashr, 2021, 12-bob (516-bet) - patternlar ma'noli bo'lgan joyda qo'llanadi; "shunchaki ishlatish uchun" boshlanmaydi
- Freeman/Robson, *Head First Design Patterns*, 2-nashr, 2021, 13-bob (584-bet) - ogohlantirish: ortiqcha ishlatish overengineered kodga olib keladi; eng oddiy yechim tanlanadi, pattern ehtiyoj paydo bo'lganda kiritiladi
- Chris Richardson, *Microservices Patterns*, Manning, 2019, 3-bob (98-bet) - Transactional outbox: event yo'qolmasligi kerak bo'lganda kafolatli mexanizm
- Chris Richardson, *Microservices Patterns*, 2019, 4-bob (114-bet) - Saga ning qo'llash sharti, izolyatsiya yo'qligi va kompensatsiya tranzaksiyalari
- Chris Richardson, *Microservices Patterns*, 2019, 6.1.9-bo'lim (200-202-bet) - event sourcing ning beshta kamchiligi
- Chris Richardson, *Microservices Patterns*, 2019, 7.2.4-bo'lim (236-bet) - CQRS ning kamchiliklari va tavsiya: imkon bo'lsa API kompozitsiyasi, CQRS faqat majbur bo'lganda
- ESLATMA: 11.2 dagi registrning ishga tushish vaqtidagi to'liqlik tekshiruvi, 11.6 dagi zanjir tartibini `@Bean` da izohlash, 11.7 dagi Caffeine konfiguratsiyasi, 11.9 dagi chegaralar jadvali, 11.10 dagi fayl sanash usuli, 11.11 jadvali va 11.12 dagi checklist shu korpusning amaliy tavsiyasi, yuqoridagi kitoblardan olingan emas
- ESLATMA: 11.5 va 11.7 dagi Spring mexanikasi (`@EventListener`, `@TransactionalEventListener`, bean hayot sikli) va 11.4 dagi Spring Data turlari freymvork hujjatiga tegishli; patternning kitobdagi ta'rifi bilan taqqoslash uchun keltirilgan

---

[&larr; 10. Dizayn pattern review I: yo'q patternni ko'rish](10-dizayn-pattern-review-i-yoq-patternni-korish.md) · [Mundarija](README.md) · [12. Code smell va anti-pattern katalogi diffda &rarr;](12-code-smell-va-anti-pattern-katalogi-diffda.md)
