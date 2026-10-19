<!-- doc: patterns | chapter: 3 | part:  -->

[Barcha hujjatlar](../../README.md) / [Dizayn patternlar](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 3. Xulq-atvor patternlari (Behavioral Patterns)

<details>
<summary>Bu bobdagi 29 bo'lim</summary>

- [3.1 Mas'uliyat zanjiri (Chain of Responsibility)](#31-masuliyat-zanjiri-chain-of-responsibility)
- [3.2 Buyruq (Command)](#32-buyruq-command)
- [3.3 Interpretator (Interpreter)](#33-interpretator-interpreter)
- [3.4 Iterator (Iterator)](#34-iterator-iterator)
- [3.5 Vositachi (Mediator)](#35-vositachi-mediator)
- [3.6 Memento (Memento)](#36-memento-memento)
- [3.7 Kuzatuvchi (Observer)](#37-kuzatuvchi-observer)
- [3.8 Holat (State)](#38-holat-state)
- [3.9 Strategiya (Strategy)](#39-strategiya-strategy)
- [3.10 Shablon metodi (Template Method)](#310-shablon-metodi-template-method)
- [3.11 Tashrifchi (Visitor)](#311-tashrifchi-visitor)
- [3.12 Bo'sh obyekt (Null Object)](#312-bosh-obyekt-null-object)
- [3.13 Spetsifikatsiya (Specification)](#313-spetsifikatsiya-specification)
- [3.14 Xizmatkor (Servant)](#314-xizmatkor-servant)
- [3.15 Ravon interfeys (Fluent Interface)](#315-ravon-interfeys-fluent-interface)
- [3.16 Callback (Callback)](#316-callback-callback)
- [3.17 Pipeline (obyekt darajasida) (Pipeline (object-level))](#317-pipeline-obyekt-darajasida-pipeline-object-level)
- [3.18 Ikki tomonlama dispatch (Double Dispatch)](#318-ikki-tomonlama-dispatch-double-dispatch)
- [3.19 Event agregatori (Event Aggregator)](#319-event-agregatori-event-aggregator)
- [3.20 O'rab bajarish (Execute Around)](#320-orab-bajarish-execute-around)
- [3.21 Chekli holatlar mashinasi (Finite State Machine (Spring Statemachine))](#321-chekli-holatlar-mashinasi-finite-state-machine-spring-statemachine)
- [3.22 Qoidalar dvigateli / Siyosat (Rules Engine / Policy)](#322-qoidalar-dvigateli--siyosat-rules-engine--policy)
- [3.23 Qora taxta (Blackboard)](#323-qora-taxta-blackboard)
- [3.24 O'zgarish uchun dizayn: qayta dizayn sabablari (Designing for Change: Causes of Redesign)](#324-ozgarish-uchun-dizayn-qayta-dizayn-sabablari-designing-for-change-causes-of-redesign)
- [3.25 Patternni tanlash va qo'llash tartibi (How to Select and Use a Design Pattern)](#325-patternni-tanlash-va-qollash-tartibi-how-to-select-and-use-a-design-pattern)
- [3.26 Patternlar orasidagi munosabatlar (Pattern Relationships and Related Patterns)](#326-patternlar-orasidagi-munosabatlar-pattern-relationships-and-related-patterns)
- [3.27 Kompozit patternlar: patternlardan yasalgan pattern (Compound Patterns)](#327-kompozit-patternlar-patternlardan-yasalgan-pattern-compound-patterns)
- [3.28 Har pattern nimani o'zgaruvchan qiladi (What Each Pattern Lets You Vary)](#328-har-pattern-nimani-ozgaruvchan-qiladi-what-each-pattern-lets-you-vary)
- [3.29 Amalda qo'llash](#329-amalda-qollash)

</details>



Xulq-atvor patternlari obyektlar orasidagi mas'uliyat taqsimoti va o'zaro muloqot algoritmlarini tartibga soladi - ya'ni "kim kim bilan gaplashadi va qaysi qarorni kim qabul qiladi" degan savolga javob beradi. Yaratuvchi patternlar obyekt qanday paydo bo'lishini, strukturaviy patternlar ularning qanday bog'lanishini hal qilsa, xulq-atvor patternlari tizimning dinamikasini - oqimlarni, hodisalarni, holat o'tishlarini va kengaytirish nuqtalarini belgilaydi. Spring Framework'ning o'zi aslida bu patternlarning sanoat miqyosidagi katalogi: `JdbcTemplate`, `PasswordEncoder`, `@EventListener`, `SecurityFilterChain` - bularning hammasi shu bo'limdagi g'oyalarning amaliy ko'rinishi. Arxitektor uchun ularni bilish ikki tomonlama foydali: birinchidan, Spring'ning ichki mexanizmlarini (nega aynan shu extension point bor) tushunadi, ikkinchidan, o'z domen kodida `if/else` va `switch` daraxtlarini polimorfizm bilan almashtirib, o'zgarishga ochiq dizayn qura oladi.

## 3.1 Mas'uliyat zanjiri (Chain of Responsibility)

**Tavsif:** So'rovni bir nechta handler'dan iborat zanjir orqali o'tkazadi: har bir handler yoki so'rovni o'zi qayta ishlaydi, yoki keyingisiga uzatadi. Yuboruvchi qaysi handler javob berishini bilmaydi, shuning uchun zanjir tarkibi va tartibi runtime'da erkin o'zgartiriladi. Bu cross-cutting mantiqni (autentifikatsiya, logging, validatsiya, rate limiting) asosiy biznes kodidan ajratib, mustaqil bo'laklarga bo'lish imkonini beradi. Zanjir odatda dekorativ emas, balki "to'xtatish huquqi" bilan ishlaydi - har qanday bo'g'in oqimni uzib, javob qaytarishi mumkin.

**Spring'da qayerda uchraydi:** Eng toza misol - Spring Security'dagi `FilterChainProxy` va u boshqaradigan `SecurityFilterChain` (Spring Security 6.x'da `SecurityFilterChain` bean'lari `HttpSecurity` orqali yig'iladi), unda `OncePerRequestFilter` merosxo'rlari `FilterChain.doFilter()` ni chaqirib zanjirni davom ettiradi. Jakarta Servlet spetsifikatsiyasidagi `jakarta.servlet.Filter`/`FilterChain`, Spring MVC'dagi `HandlerInterceptor` ketma-ketligi (`HandlerExecutionChain`), WebFlux'dagi `WebFilter`/`WebFilterChain` ham xuddi shu pattern. Spring AOP ichida `ReflectiveMethodInvocation` `MethodInterceptor` ro'yxatini birin-ketin chaqiradi - ya'ni har bir `@Transactional`/`@Cacheable` interceptor zanjirning bir bo'g'ini. `RestClient` va `RestTemplate` uchun `ClientHttpRequestInterceptor`, WebClient uchun `ExchangeFilterFunction` ham shu modelda.

**Qo'llanish keyslari:**
- HTTP so'rov uchun autentifikatsiya, CORS, CSRF, rate limiting va audit bosqichlarini mustaqil filter'larga ajratish.
- Kiruvchi hujjat yoki to'lov buyrug'ini ketma-ket validatsiya qoidalaridan o'tkazish, birinchi xatolikda to'xtatish.
- Kelgan event'ni bir necha ixtisoslashgan handler orasidan "kim tanidi, o'sha ishlaydi" printsipida tarqatish.
- Legacy integratsiyada xabarni normalizatsiya → boyitish → yo'naltirish bosqichlariga bo'lish (Spring Integration pipeline).
- Multi-tenant tizimda tenant aniqlash va kontekst to'ldirishni biznes mantiqdan oldin bajarish.

**Ehtiyot bo'ling:** Zanjir uzun bo'lsa, debug qilish og'irlashadi va handler'lar tartibiga yashirin bog'liqlik paydo bo'ladi - shuning uchun `@Order`/`OrderComparator` bilan tartibni oshkora belgilang va zanjirni Actuator yoki log orqali ko'rinadigan qiling. Agar so'rovni albatta kimdir qayta ishlashi shart bo'lsa, zanjir oxirida default handler qo'ying; aks holda "jim yo'qolgan" so'rovlar paydo bo'ladi.

```java
// Chain of Responsibility: har bo'g'in o'ziga tegishlisini hal qiladi yoki uzatadi
public interface DiscountRule {
    Optional<Discount> apply(Cart cart);        // bo'sh = men emas, keyingisi
}

@Service
public class DiscountChain {
    private final List<DiscountRule> rules;     // tartib @Order bilan belgilanadi

    public DiscountChain(List<DiscountRule> rules) { this.rules = rules; }

    public Discount resolve(Cart cart) {
        return rules.stream()
                .flatMap(r -> r.apply(cart).stream())
                .findFirst()
                .orElse(Discount.none());
    }
}
```

**Qurish qarorlari:** Zanjirni ikki yo'l bilan qurish mumkin. Birinchi yo'l - mavjud havolalar ustida: butun-qism ierarxiyasidagi ota havolasi allaqachon zanjir bo'lib turadi, shuning uchun alohida `successor` maydoni e'lon qilmaslik joy tejaydi (qarang: [Kompozitni qurish qarorlari](02-strukturaviy-patternlar.md#222-kompozitni-qurish-qarorlari-implementing-composite)). Ikkinchi yo'l - oshkora zanjir, va u mavjud tuzilma kerakli ketma-ketlikka mos kelmaganda majburiy bo'lib qoladi. Qaror mezoni sodda: zanjir tartibi daraxt shakliga teng bo'lsa mavjud havolalarni ishlating, aks holda ortiqcha havola yozishdan qochmang - noto'g'ri tuzilmani zanjir sifatida ishlatish keyinchalik tartibni o'zgartirishni imkonsiz qiladi.

Ikkinchi qaror handler bazasiga tegishli: baza sinf successor'ni saqlab, so'rovni shartsiz uzatadigan default implementatsiya bersin. Shunda so'rovga qiziqmagan konkret handler hech narsa qayta yozmaydi va yangi handler yozish "faqat men hal qiladigan holatni yoz" degan ishga aylanadi; uzatishni har handlerga takrorlash esa bir kuni bitta joyda esdan chiqadi va so'rov jim yo'qoladi.

Uchinchi qaror - so'rovni qanday ifodalash, va bu tanlov zanjirning kengaytiriluvchanligini belgilaydi. Qattiq yozilgan metod chaqiruvi xavfsiz, lekin faqat qat'iy to'plamdagi so'rovni uzatadi. Kod parametri bilan bitta metod to'plamni ochiq qiladi, lekin dispatch uchun shart operatori kerak bo'ladi va parametrlar tur-xavfsiz uzatilmaydi. Alohida so'rov obyekti parametrlarni birga olib yuradi va subclass bilan kengayadi, narxi esa handler so'rov turini aniqlashi kerakligi. ESLATMA: Java 17+ da uchinchi variantning narxi yo'qoladi - `sealed interface Request` va pattern matching'li `switch` dispatch'ni tur-xavfsiz qiladi va to'liqlikni kompilyator tekshiradi.
## 3.2 Buyruq (Command)

**Tavsif:** Amalni obyekt sifatida inkapsulyatsiya qiladi: bajariladigan ish, uning parametrlari va receiver bitta sinfga joylanadi. Shu sababli amalni navbatga qo'yish, kechiktirish, qayta urinish, jurnalga yozish yoki bekor qilish (undo) mumkin bo'ladi. Chaqiruvchi (invoker) amal nima qilishini bilmaydi - faqat `execute()` ni biladi, bu esa chaqiruvchini mantiqdan to'liq ajratadi.

**Spring'da qayerda uchraydi:** `java.lang.Runnable` va `java.util.concurrent.Callable` - til darajasidagi Command; Spring ularni `TaskExecutor`, `@Async` va `ThreadPoolTaskExecutor` orqali bajaradi, Java 21+ virtual thread'lar bilan esa `SimpleAsyncTaskExecutor.setVirtualThreads(true)` yoki `spring.threads.virtual.enabled=true` sozlamasi ishlatiladi. Spring Framework'ning callback interfeyslari - `TransactionCallback`, `JdbcTemplate` ichidagi `StatementCallback`, `ConnectionCallback` - resursga nisbatan bajariladigan buyruqlar. Spring Batch'dagi `Tasklet` va `Step` bajarilishi, Spring Shell'dagi `@ShellMethod`, CQRS uchun Axon Framework'ning `@CommandHandler`/`CommandGateway` ham shu patternga asoslanadi.

**Qo'llanish keyslari:**
- Uzoq davom etadigan ishni (hisobot generatsiyasi, export) command obyekti ko'rinishida navbatga qo'yib, worker'da bajarish.
- CQRS arxitekturasida `CreateOrderCommand` kabi oshkora buyruqlar bilan yozish oqimini modellashtirish.
- Audit talabi bor tizimda har bir foydalanuvchi amalini seriyalashtirib saqlash va kerak bo'lsa qayta ijro etish (replay).
- Undo/redo zarur bo'lgan hujjat yoki konfiguratsiya tahrirlash oqimlari.
- Outbox pattern bilan tranzaksiya oxirida bajarilishi kerak bo'lgan tashqi chaqiruvlarni buyruq sifatida saqlash.

**Ehtiyot bo'ling:** Har bir kichik amal uchun alohida command sinfi yozish kodni portlatib yuboradi - buni faqat navbat, retry, audit yoki undo kerak bo'lganda qo'llang. Seriyalanadigan buyruqlar API shartnomasiga aylanadi: maydon qo'shish/olib tashlashda versiyalashni oldindan o'ylamasa, navbatda yotgan eski buyruqlar deserializatsiyada sinadi.

```java
// Command: harakat obyekt sifatida - navbatga qo'yish, log, qayta bajarish mumkin
public sealed interface AccountCommand permits Freeze, Close {
    long accountId();
}
public record Freeze(long accountId, String reason) implements AccountCommand {}
public record Close(long accountId) implements AccountCommand {}

@Service
public class AccountCommandHandler {
    private final Map<Class<?>, Consumer<AccountCommand>> handlers = Map.of(
            Freeze.class, c -> freeze((Freeze) c),
            Close.class,  c -> close((Close) c));

    public void handle(AccountCommand cmd) {
        handlers.get(cmd.getClass()).accept(cmd);
    }
    private void freeze(Freeze c) { /* ... */ }
    private void close(Close c) { /* ... */ }
}
```

**Qurish qarorlari:** Birinchi qaror - buyruq qanchalik aqlli bo'lishi, va bu spektr, ikki holatli tanlov emas. Bir chekkada buyruq faqat receiver bilan amalni bog'laydi va o'zi hech narsa qilmaydi. Ikkinchi chekkada buyruq hech kimga delegatsiya qilmasdan hammasini o'zi bajaradi - mustaqil receiver mavjud bo'lmaganda shunday bo'ladi. Orada receiver'ni ish vaqtida topadigan buyruq turadi. Chekka tanlovlar aniq, oraliq variant esa eng ko'p xatoga olib keladi: buyruq receiver'ni o'zi izlasa, u konteyner yoki reyestrga bog'lanadi va testda alohida yurmaydi.

Ikkinchi qaror undo ni qo'llab-quvvatlashga tegishli va u uch narsani saqlashni talab qiladi: receiver, amal argumentlari, hamda receiver'ning o'zgarishi mumkin asl qiymatlari. Bir daraja undo uchun oxirgi bajarilgan buyruqni saqlash yetadi; ko'p daraja undo va redo uchun tarix ro'yxati kerak bo'ladi va ro'yxat uzunligi mavjud daraja sonini belgilaydi. Shu yerdan uchinchi qaror chiqadi: bajarilgandan keyin holati o'zgaradigan buyruq tarix ro'yxatiga qo'yilishdan OLDIN nusxalanishi shart, aks holda bir xil buyruq obyektining ikki chaqirig'i tarixda farqlanmaydi va undo noto'g'ri qiymatni tiklaydi; holati o'zgarmaydigan buyruqqa esa havola yetadi. ESLATMA: Java'da buyruqni immutable `record` qilib yozish bu nusxalashni butunlay keraksiz qiladi, shuning uchun tarix ro'yxati bilan ishlaydigan kodda `record` default tanlov.

To'rtinchi tafsilot uzoq undo va redo ketma-ketligida chiqadi: amallarni teskari hisoblash bilan tiklaganda xato to'planadi va ilova holati asl qiymatlardan uzoqlashadi. Shuning uchun aniq tiklash kerak bo'lsa buyruqqa [Memento](#36-memento-memento) orqali qo'shimcha ma'lumot beriladi - u boshqa obyektlarning ichini ochmasdan asl holatni olib yuradi.
## 3.3 Interpretator (Interpreter)

**Tavsif:** Ma'lum bir tilning grammatikasini obyekt daraxti (AST) sifatida ifodalab, shu daraxtni aylanib chiqib ifodani hisoblaydi. Har bir grammatik qoida alohida sinfga mos keladi, shuning uchun til yangi konstruksiyalar bilan kengaytiriladi. Natijada biznes qoidalari yoki filtrlar kompilyatsiya qilinmagan, matn ko'rinishida saqlanib, runtime'da bajariladi.

**Spring'da qayerda uchraydi:** Spring Expression Language (SpEL) - `org.springframework.expression.spel.standard.SpelExpressionParser`, `Expression`, `StandardEvaluationContext` - klassik Interpreter implementatsiyasi; `@Value("#{...}")`, `@Cacheable(key = "...")`, `@PreAuthorize("hasRole('ADMIN')')")` kabi annotatsiyalar shu interpretator ustida ishlaydi. Spring Data'dagi `PartTree` metod nomini (`findByLastNameAndAgeGreaterThan`) grammatik tahlil qilib query'ga aylantiradi, Hibernate 6 esa HQL/JPQL uchun Antlr asosidagi parser va semantik daraxt (SQM) ishlatadi. Spring Boot'ning `@ConditionalOnExpression` va Actuator'ning filtr ifodalari ham SpEL'ga tayanadi.

**Qo'llanish keyslari:**
- Bitta deploy ichida o'zgaradigan narx yoki chegirma qoidalarini matn ifoda sifatida bazada saqlash.
- Foydalanuvchi yozadigan hisobot filtrlari uchun xavfsiz, cheklangan DSL berish.
- Feature flag va routing shartlarini konfiguratsiyada ifoda bilan belgilash.
- Low-code forma validatsiyasi: maydonlar orasidagi shartlarni deklarativ yozish.
- Risk yoki fraud skoringda analitiklar tahrirlaydigan qoidalar to'plamini bajarish.

**Ehtiyot bo'ling:** Tashqi foydalanuvchi kiritgan SpEL'ni to'g'ridan-to'g'ri hisoblash jiddiy RCE xavfi - `SimpleEvaluationContext` yoki o'zingiz yozgan cheklangan grammatikadan foydalaning, `StandardEvaluationContext` ni ishonchsiz matn bilan ishlatmang. To'laqonli til yozishga kirishishdan oldin o'ylab ko'ring: ko'p holatda Strategy yoki tayyor rule engine (Drools, OpenPolicyAgent) arzonga tushadi.

```java
// Interpreter: qoida matn sifatida saqlanadi va bajarilyapti
@Service
public class SpelRuleEngine {
    private final SpelExpressionParser parser = new SpelExpressionParser();
    private final Map<String, Expression> cache = new ConcurrentHashMap<>();

    public boolean matches(String rule, Order order) {
        Expression e = cache.computeIfAbsent(rule, parser::parseExpression);
        // Ishonchsiz manbadan kelgan ifodani bajarmang: SpEL to'liq Java chaqiradi
        return Boolean.TRUE.equals(e.getValue(new StandardEvaluationContext(order), Boolean.class));
    }
}
// matches("total > 1000000 and customer.vip", order)
```

**Qurish qarorlari:** Patternni tanlashdan oldin bitta shart tekshiriladi: u faqat unumdorlik tanqid bo'lmagan joyda ishlatiladi. Daraxtni to'g'ridan-to'g'ri hisoblash eng sodda, lekin eng sekin yo'l; tez interpretatorlar daraxtni hisoblamaydi, avval uni boshqa shaklga o'giradi (masalan regulyar ifodani holat mashinasiga). Demak qoida matn ko'rinishida saqlanishi talab bo'lsa, lekin u issiq yo'lda millionlab marta bajarilsa, yechim interpretatsiya emas, kompilyatsiya yoki keshlangan o'tkazish bo'ladi.

Ikkinchi qaror - AST ni kim yasaydi. Pattern parsing'ni o'z ichiga OLMAYDI va bu alohida qaror: daraxt jadval asosidagi parser bilan, qo'lda yozilgan recursive descent parser bilan yoki to'g'ridan-to'g'ri klient tomonidan (fluent qurish orqali) yasaladi. Patternni tanlab, parsing qarorini qoldirib qo'yish keng tarqalgan xato: grammatika o'sgandan keyin parser ni almashtirish daraxt sinflarini ham qayta yozishga olib keladi.

Uchinchi qaror amallarni qayerda ushlashga tegishli. `interpret` amalini grammatika sinflarining o'zida ushlash faqat bitta amal bo'lganda qulay; ifoda ustida tur tekshiruvi, optimizatsiya va kod generatsiyasi ham kerak bo'lsa, ularni [Tashrifchi](#311-tashrifchi-visitor) ga chiqarish kerak, aks holda har yangi amal barcha grammatika sinfini o'zgartiradi. To'rtinchi qaror xotiraga tegishli: terminal simvollar daraxtda juda ko'p takrorlanadi va ularni [Flyweight](02-strukturaviy-patternlar.md#26-flyweight-flyweight) bilan bo'lishish mumkin, chunki terminal tugun o'z o'rnini saqlamaydi va kontekstni ota tugundan parametr sifatida oladi - bu intrinsic va extrinsic holat ajratishning toza namunasi.
## 3.4 Iterator (Iterator)

**Tavsif:** To'plam elementlarini uning ichki tuzilishini oshkor qilmasdan ketma-ket aylanib chiqish usulini beradi. Aylanish holati (kursor) alohida obyektda saqlanadi, shuning uchun bir to'plam ustida bir nechta mustaqil obxod bo'lishi mumkin. Katta ma'lumotlar bilan ishlaganda esa butun to'plamni xotiraga olmasdan, bo'lak-bo'lak o'qishga yo'l ochadi.

**Spring'da qayerda uchraydi:** Platforma darajasida `java.util.Iterator`, `Iterable`, `Spliterator` va `Stream`; Spring Data'da `Streamable`, `Page`/`Slice`/`Pageable` (pagination asosida kursor), MongoDB va JPA repository'laridagi `Stream<T>` qaytaruvchi metodlar va `CloseableIterator`. Spring Batch'da `ItemReader` - eng aniq ko'rinishdagi Iterator: `JdbcCursorItemReader`, `JdbcPagingItemReader`, `FlatFileItemReader` `read()` chaqirig'i bilan birin-ketin element qaytaradi va oxirida `null` beradi. Reaktiv dunyoda Project Reactor'ning `Flux` push-asosidagi, `JdbcTemplate` ning `RowCallbackHandler` esa callback-asosidagi obxodni ta'minlaydi.

**Qo'llanish keyslari:**
- Millionlab qatorli jadvalni ETL jarayonida kursor bilan oqim sifatida o'qish.
- REST API'da katta natijani `Page` yoki keyset pagination orqali qismlarga bo'lib qaytarish.
- Tashqi API'ning sahifalangan javobini bitta `Iterator`/`Stream` ortiga yashirish.
- Fayl yoki Kafka topic'ini xotiraga sig'maydigan hajmda ketma-ket qayta ishlash.
- Domen agregatida ichki kolleksiyani faqat o'qish uchun ochib berish (incapsulyatsiyani buzmasdan).

**Ehtiyot bo'ling:** Repository'dan qaytgan `Stream` yoki `CloseableIterator` ochiq DB kursorini ushlab turadi - uni `try-with-resources` ichida yoping va tranzaksiya doirasida ishlating, aks holda connection pool tez tugaydi. `Iterator` bilan aylanib turib to'plamni o'zgartirish `ConcurrentModificationException` beradi; offset-asosidagi pagination esa chuqur sahifalarda sekinlashadi va yozuvlar siljishi sababli element tashlab ketadi.

```java
// Iterator: katta natijani xotiraga yig'masdan aylanib chiqish
public interface OrderRepository extends JpaRepository<Order, Long> {
    @QueryHints(@QueryHint(name = HINT_FETCH_SIZE, value = "500"))
    Stream<Order> findByStatus(OrderStatus status);     // kursor asosida
}

@Service
public class OrderExport {
    @Transactional(readOnly = true)                     // stream uchun shart
    public void exportPending(Writer out) {
        try (Stream<Order> orders = repo.findByStatus(PENDING)) {
            orders.forEach(o -> write(out, o));         // bir vaqtda bitta qator
        }
    }
}
```

**Qurish qarorlari:** Birinchi qaror - obxod algoritmini kim belgilaydi. Iterator belgilasa, bitta kolleksiya ustida turli obxod algoritmini (oldindan, keyin, filtrlangan) ishlatish oson bo'ladi; narxi esa inkapsulyatsiyada - algoritm kolleksiyaning yopiq maydonlariga murojaat qilsa, kolleksiya o'z ichini iteratorga ochishga majbur bo'ladi. Kolleksiya belgilasa, iterator faqat joriy pozitsiyani saqlaydi va bunday yengil iterator kursor deb ataladi; shunda inkapsulyatsiya saqlanadi, lekin obxod shakli bitta bo'lib qoladi. ESLATMA: Java'da ikki variant ham tilda bor - `Iterator` kursor shaklini, `Spliterator` va `Stream` esa obxod algoritmini tashqariga chiqargan shaklni beradi.

Ikkinchi qaror [Kompozit](02-strukturaviy-patternlar.md#23-kompozit-composite) ustida ishlaganda chiqadi va u yerda tashqi iterator qiyin: pozitsiya bitta indeks emas, ko'p qatlamni qamragan yo'l, shuning uchun uni stack'da saqlash kerak bo'ladi. Uch variantning narxi turlicha: ichki rekursiv obxod yo'lni chaqiruv stack'ida saqlab kodni soddalashtiradi, lekin obxodni to'xtatib turish qiyin; tashqi iterator stack'ni o'zi boshqarib to'xtatishga ruxsat beradi, lekin kodi og'ir; tugunlar aka-uka va ota havolasiga ega bo'lsa esa kursor-asosidagi iterator eng yengil chiqadi, chunki pozitsiya bitta tugun havolasidan iborat bo'ladi.
## 3.5 Vositachi (Mediator)

**Tavsif:** Ko'p komponentni bir-biri bilan to'g'ridan-to'g'ri gaplashtirish o'rniga, muloqotni bitta vositachi obyektga yuklaydi. Natijada N×N bog'liqlik to'ri N ta bog'liqlikka aylanadi va komponentlar bir-birini bilmasdan ishlaydi. Koordinatsiya mantiqi bir joyda to'planadi, bu uni test qilish va o'zgartirishni osonlashtiradi.

**Spring'da qayerda uchraydi:** `ApplicationEventPublisher` va uning ortidagi `ApplicationEventMulticaster` (`SimpleApplicationEventMulticaster`) - ilovadagi markaziy vositachi: publisher listener'larni, listener'lar publisher'ni bilmaydi. Spring Integration'da `MessageChannel`, `MessageRouter` va `IntegrationFlow`'lar endpoint'lar orasidagi muloqotni to'liq vositachiga topshiradi; Spring Cloud Stream `Binder` orqali shu rolni broker ustida bajaradi. Spring Modulith'da modullar orasidagi aloqa atayin event'lar (`@ApplicationModuleListener`) orqali, to'g'ridan-to'g'ri bean injection'siz qurilishi tavsiya etiladi. Spring MVC'dagi `DispatcherServlet` ham `HandlerMapping`, `HandlerAdapter` va `ViewResolver` orasidagi muvofiqlashtiruvchi sifatida xuddi shu vazifani bajaradi.

**Qo'llanish keyslari:**
- Modulli monolitda bounded context'lar orasidagi aloqani event bus orqali qurish va kompilyatsiya bog'liqligini uzish.
- Bir nechta tashqi servisni (to'lov, ombor, bildirishnoma) chaqiruvchi buyurtma oqimini bitta orchestrator'ga yig'ish.
- Murakkab UI/forma holatida maydonlar orasidagi o'zaro ta'sirni markazlashtirish (masalan Vaadin yoki JavaFX view controller).
- Chat yoki WebSocket xonalarida xabarlarni `SimpMessagingTemplate` orqali tarqatish.
- Legacy integratsiyada turli protokollardagi tizimlarni ESB/Spring Integration vositachisi ostida ulash.

**Ehtiyot bo'ling:** Vositachi o'sib ketsa, u "god object" ga aylanadi - barcha biznes qoidalari bitta sinfga yig'ilib, uni o'zgartirish xavfli bo'ladi; mantiqni domen servislariga qaytarib, vositachida faqat yo'naltirishni qoldiring. Event'lar orqali qurilgan vositachilik oqimni ko'rinmas qiladi: tracing (Micrometer Tracing) va oshkora event katalogi bo'lmasa, nosozlikni topish qiyinlashadi.

```java
// Mediator: modullar bir-birini bilmaydi, vositachi orqali gaplashadi
@Service
public class OrderService {
    private final ApplicationEventPublisher events;     // vositachi

    public OrderService(ApplicationEventPublisher events) { this.events = events; }

    @Transactional
    public void place(Order order) {
        repo.save(order);
        events.publishEvent(new OrderPlaced(order.id()));   // kim tinglaydi - bilmaymiz
    }
}

@Component
class StockReservation {
    @TransactionalEventListener            // commit'dan keyin ishlaydi
    void on(OrderPlaced e) { /* zaxirani band qilish */ }
}
```

**Qurish qarorlari:** Abstrakt Mediator sinfi har doim kerak emas: kolleague'lar faqat bitta vositachi bilan ishlasa, abstraksiya hech narsa qo'shmaydi va u faqat bir kolleague turi turli vositachilar bilan ishlashi kerak bo'lganda qiymat beradi. Ikkinchi qaror muhimroq - kolleague vositachi bilan qanday gaplashadi. Ikki yo'l bor. Birinchi: vositachini kuzatuvchi qilib qo'yish - kolleague Subject bo'lib holat o'zgarganda xabar beradi va yuboruvchi haqida hech narsa aytmaydi (qarang: [Kuzatuvchi](#37-kuzatuvchi-observer)). Ikkinchi: vositachida maxsus bildirish interfeysi bo'lib, kolleague o'zini argument sifatida uzatadi; shunda vositachi yuboruvchini taniydi va aniqroq yo'naltiradi, lekin ikki tomon kuchliroq bog'lanadi. ESLATMA: Spring'da birinchi yo'l `ApplicationEventPublisher` bilan default, ikkinchi yo'l esa hodisa sinfiga yuboruvchi identifikatorini kiritish yoki aniq interfeysli `@Service` vositachi yozish ko'rinishida qoladi.

Fasad bilan vositachini aralashtirmaslik uchun ajratuvchi chiziq protokol yo'nalishida: [Fasad](02-strukturaviy-patternlar.md#25-fasad-facade) bir yo'nalishli, ya'ni fasad quyi tizim obyektlariga so'rov qiladi, teskarisi emas, va yangi xulq qo'shmaydi; vositachi esa ko'p yo'nalishli va kolleague'lar o'zi bera olmaydigan hamkorlikni yuzaga keltiradi. Shuning uchun "quyi tizim menga javob qaytarmaydi, faqat chaqiriladi" bo'lsa fasad, "ikki tomon bir-biriga reaksiya qiladi" bo'lsa vositachi. Biznes qarori kimda turishi bo'yicha ajratish esa alohida yozilgan (qarang: [Orkestrator vs fasad](08-biznes-logika-va-service-qatlam-patternlari.md#825-orkestrator-vs-fasad-orchestrator-vs-facade)).
## 3.6 Memento (Memento)

**Tavsif:** Obyektning ichki holatini inkapsulyatsiyani buzmasdan tashqi "snapshot" sifatida saqlaydi va keyin shu holatga qaytarish imkonini beradi. Snapshot ichini faqat egasi tushunadi, boshqalar uni shunchaki saqlovchi (caretaker) sifatida ushlab turadi. Shu tufayli undo, checkpoint va davom ettirish (resume) imkoniyatlari paydo bo'ladi.

**Spring'da qayerda uchraydi:** Spring Batch'dagi `ExecutionContext` - klassik Memento: `ItemStream.update()` orqali o'qish pozitsiyasi `JobRepository` ga yoziladi va restart'da aynan shu joydan davom etiladi. Spring Statemachine'da `StateMachineContext` va `StateMachinePersister` mashina holatini tashqi omborga saqlaydi/tiklaydi. Tranzaksiya darajasida `SavepointManager` va `TransactionStatus.createSavepoint()` (`PROPAGATION_NESTED`) qisman rollback uchun checkpoint beradi; Hibernate'ning dirty checking mexanizmi esa yuklangan entity'ning snapshot'ini persistence context'da saqlaydi. HTTP sohasida `HttpSession` va Spring Session (`spring-session-data-redis`) foydalanuvchi holatining saqlangan nusxasi sifatida ishlaydi.

**Qo'llanish keyslari:**
- Uzoq batch job'ni uzilishdan keyin oxirgi checkpoint'dan qayta ishga tushirish.
- Hujjat yoki konfiguratsiya tahririda undo/redo va versiya tarixini qo'llab-quvvatlash.
- Ko'p qadamli wizard formasida har qadam holatini saqlab, orqaga qaytish imkonini berish.
- Saga yoki state machine instance'ini bazada saqlab, boshqa node'da davom ettirish.
- Domen agregatining "oldingi qiymatlari" ni audit uchun snapshot ko'rinishida yozish.

**Ehtiyot bo'ling:** Katta obyektlarning snapshot'lari xotira va I/O ni tez yeb qo'yadi - faqat zarur maydonlarni saqlang yoki event sourcing + davriy snapshot kombinatsiyasiga o'tishni ko'rib chiqing. Snapshot'ni oddiy DTO sifatida ochib qo'ysangiz, inkapsulyatsiya yo'qoladi va saqlangan formatning har bir o'zgarishi migratsiya muammosiga aylanadi.

```java
// Memento: holat tashqariga chiqariladi va keyin tiklanadi
public record ImportCheckpoint(long lastId, int processed) {}

@Component
public class ImportJob {
    public ImportCheckpoint snapshot() {            // memento yaratish
        return new ImportCheckpoint(lastId, processed);
    }
    public void restore(ImportCheckpoint c) {       // memento'dan tiklash
        this.lastId = c.lastId();
        this.processed = c.processed();
    }
}
// Spring Batch da bir xil g'oya: ExecutionContext ni JobRepository saqlaydi
```

**Qurish qarorlari:** Patternning kam aytiladigan foydasi Originator tomonida: memento Originator'ni soddalashtiradi. Versiyalarni klient saqlagani uchun Originator saqlashni boshqarmaydi, eski versiyalarni hisoblab yurmaydi va klient "men tugatdim" deb xabar berishi kerak bo'lmaydi; holat egasi faqat snapshot yasash va undan tiklashni biladi. Shu qulaylikning narxi esa saqlovchi tomonida va u yashirin: caretaker memento ichida qancha holat borligini bilmaydi, chunki memento ataylab qora quti. Yengil ko'rinadigan caretaker shu sababli kutilmagan xotira narxini ko'tarib qolishi mumkin, demak memento'ni o'z vaqtida bo'shatish - caretaker'ning oshkora mas'uliyati bo'lishi kerak: necha snapshot saqlanadi, qancha vaqt yashaydi va kim o'chiradi degan savollarga javob kodda turishi lozim. ESLATMA: Spring Batch'da bu javob framework tomonidan berilgan - `ExecutionContext` hajmi `JobRepository` jadvalidagi ustun uzunligi bilan cheklangan, shuning uchun u checkpoint uchun kichik qiymatlar saqlashga majburlaydi.
## 3.7 Kuzatuvchi (Observer)

**Tavsif:** Bitta subyekt holati o'zgarganda unga obuna bo'lgan barcha kuzatuvchilarga avtomatik xabar beradi. Subyekt kuzatuvchilarning konkret turini bilmaydi, shuning uchun yangi reaksiyalarni mavjud kodga tegmasdan qo'shish mumkin. Bu "ochiq-yopiq" printsipini amalda ta'minlaydigan eng keng tarqalgan mexanizm.

**Spring'da qayerda uchraydi:** `ApplicationEventPublisher.publishEvent()`, `ApplicationListener<E>`, `@EventListener` va `@TransactionalEventListener` (`AFTER_COMMIT` fazasi bilan) - Spring'ning o'zidagi asosiy Observer apparati; Spring Boot ichki hodisalari (`ApplicationReadyEvent`, `ContextRefreshedEvent`, Security'dagi `AuthenticationSuccessEvent`) ham shu orqali tarqaladi. Spring Data'da `@DomainEvents` va `AbstractAggregateRoot.registerEvent()` agregat saqlanganda domen hodisalarini avtomatik e'lon qiladi. Reaktiv stack'da `Publisher`/`Subscriber` (Reactive Streams, Project Reactor) backpressure bilan ishlaydigan Observer varianti; `java.beans.PropertyChangeListener` esa platformadagi tarixiy misol.

```java
@Component
class OrderPaidListener {
    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
    void on(OrderPaidEvent e) {
        // commit'dan keyin: xabarnoma, outbox, integratsiya
    }
}
```

**Qo'llanish keyslari:**
- Buyurtma to'langandan so'ng xabarnoma, hisob-faktura va analitikani bir-biridan mustaqil ishga tushirish.
- Cache'ni ma'lumot o'zgarishi hodisasi bilan invalidatsiya qilish.
- Audit va metrikalarni biznes kodga tegmasdan hodisalar orqali yig'ish.
- Modulli monolitda modullar orasidagi "nozik" aloqa (Spring Modulith).
- WebSocket/SSE orqali frontend'ga real vaqt yangilanishlarini uzatish.

**Ehtiyot bo'ling:** Standart `@EventListener` chaqiruvi sinxron va bir xil thread'da bajariladi - og'ir listener publisher tranzaksiyasini uzaytiradi yoki uni sindiradi; shuning uchun `AFTER_COMMIT` yoki `@Async` dan foydalaning, lekin `@Async` bilan hodisa yo'qolishi mumkinligini hisobga olib outbox qo'llang. Listener'lar soni ko'paygach, oqim "yashirin" bo'lib qoladi: bir hodisa boshqa hodisani chaqiradigan kaskadlar va ro'yxatdan yechilmagan listener'lar (memory leak) ni nazorat qilish kerak.

**Qurish qarorlari:** Subject va Observer orasidagi abstrakt bog'lanish arxitektura darajasida bitta aniq ish qiladi: u qatlamlashni saqlaydi. Past qatlamdagi subject yuqori qatlamdagi observer'ga xabar berishi mumkin va bog'liqlik yo'nalishi buzilmaydi, chunki subject observer'ning turini bilmaydi - u faqat obuna interfeysini biladi. Shuning uchun domen moduli infratuzilma moduliga hodisa yuborishi mumkin bo'lib qoladi, teskari yo'naltirilgan import esa paydo bo'lmaydi (qarang: [Bog'liqliklarni teskari aylantirish printsipi](26-dizayn-printsiplari-solid-grasp-va-umumiy.md#265-bogliqliklarni-teskari-aylantirish-printsipi-dependency-inversion-principle)). Teskari holat ham qoidani ko'rsatadi: Subject va Observer rollarini bitta obyektga qo'shsangiz, u obyekt ikki qatlamni qamraydi yoki ikkisidan bittasiga tiqilib qoladi va qatlam chegarasi yo'qoladi.

Ikkinchi qaror xabar shakliga tegishli va u bitta observer bir nechta subject'ni kuzatganda majburiy bo'ladi: `update` chaqirig'ida subject o'zini uzatishi kerak, aks holda observer qaysi subject xabar berganini bilmaydi va reaksiyani to'g'ri manbaga bog'lay olmaydi. ESLATMA: Spring'da bu talab hodisa sinfining o'zi bilan bajariladi - hodisa payloadi manbani (agregat identifikatorini yoki `ApplicationEvent.getSource()` ni) olib yurgani uchun alohida `update(subject)` imzosi kerak bo'lmaydi; lekin bir xil hodisa sinfini ikki manba uchun ishlatsangiz, manba maydonini payloadga kiritish shart bo'lib qoladi.

## 3.8 Holat (State)

**Tavsif:** Obyektning xulqi uning ichki holatiga qarab o'zgarishini alohida holat sinflariga chiqaradi: har bir holat o'zining ruxsat etilgan amallarini va keyingi o'tishlarini biladi. Shu tariqa katta `switch (status)` daraxtlari polimorfizm bilan almashtiriladi. O'tishlar oshkora bo'lgani uchun noto'g'ri holat kombinatsiyalari kompilyatsiya yoki konfiguratsiya darajasida bloklanadi.

**Spring'da qayerda uchraydi:** Spring Statemachine (`spring-statemachine-core`) - holatlar, o'tishlar, guard va action'larni deklarativ e'lon qilish uchun maxsus proyekt; `StateMachineBuilder`, `@WithStateMachine`, `@OnTransition` annotatsiyalari bilan ishlatiladi. Spring Batch'da `BatchStatus`/`ExitStatus` va step oqimining shartli o'tishlari (`on("FAILED").to(...)`) holat mashinasini konfiguratsiya bilan ifodalaydi. Oddiy Java'da `sealed interface` + `record` (Java 17+) va `switch` pattern matching (Java 21+) holat modelini tilning o'zida xavfsiz yozish imkonini beradi; Spring Security'dagi autentifikatsiya oqimi (anonymous → authenticated → fully authenticated) ham holatga asoslangan xulqqa misol.

**Qo'llanish keyslari:**
- Buyurtma yoki to'lov lifecycle'ini (`NEW → PAID → SHIPPED → RETURNED`) qat'iy o'tishlar bilan modellashtirish.
- Hujjat tasdiqlash workflow'i: har bir holatda kim nima qila olishini aniq cheklash.
- Qurilma yoki IoT sessiyasining ulanish holatlarini boshqarish.
- Saga/long-running jarayonning qadamlarini holat mashinasi sifatida saqlash va tiklash.
- Subscription billing holatlari (trial, active, past due, canceled) va ularga mos ruxsatlar.

**Ehtiyot bo'ling:** To'laqonli state machine framework'ini uch-to'rt holatli oddiy oqim uchun kiritish ortiqcha murakkablik - avval enum + o'tish jadvali yoki `sealed` ierarxiyani sinab ko'ring. Holatni bazada faqat satr (`String status`) sifatida saqlab, o'tish qoidalarini kodda tarqatib yuborish eng keng tarqalgan xato: tekshiruvni bitta joyda markazlashtiring, aks holda ma'lumot bazasida "imkonsiz" holatlar paydo bo'ladi.

```java
// State: xulq holatga qarab o'zgaradi, if zanjiri yo'q
public enum OrderState {
    NEW      { @Override public OrderState pay()    { return PAID; } },
    PAID     { @Override public OrderState ship()   { return SHIPPED; } },
    SHIPPED  { @Override public OrderState deliver(){ return DELIVERED; } },
    DELIVERED;

    public OrderState pay()     { throw illegal("pay"); }
    public OrderState ship()    { throw illegal("ship"); }
    public OrderState deliver() { throw illegal("deliver"); }

    private IllegalStateException illegal(String op) {
        return new IllegalStateException(op + " holatda mumkin emas: " + name());
    }
}
```

**Qurish qarorlari:** Birinchi qaror - o'tish mezonini kim belgilaydi. Mezon qat'iy va kam o'zgaradigan bo'lsa, u Context'da turadi: o'tish jadvali bitta joyda va holat sinflari bir-birini bilmaydi. Moslashuvchanroq yo'l - State sinfining o'zi keyingi holatini va qachon o'tishni aytishi; narxi esa bog'lanishda, chunki shunda bir State kamida bitta boshqa State'ni bilib qoladi va o'tish grafigi sinflar bo'ylab tarqaladi. Yuqoridagi `enum` misoli ikkinchi yo'lni ko'rsatadi; o'tishlar soni o'sganda jadvalni Context'ga yoki konfiguratsiyaga ko'chirish arzonroq tushadi.

Ikkinchi qaror holat obyektlarining umriga tegishli: ularni oldindan yaratib saqlash yoki kerak bo'lganda yaratib tashlash. Holat tez-tez o'zgarsa oldindan yaratish afzal, chunki yaratish narxi bir marta to'lanadi; holat kamdan-kam o'zgarsa va holat obyekti ko'p ma'lumot saqlasa, kerak bo'lganda yaratish xotirani tejaydi. Bu qaror uchinchisi bilan bog'langan: State obyektlari maydonsiz bo'lsa, holat ularning turida kodlangan bo'lgani uchun turli kontekstlar ularni bo'lishishi mumkin, ya'ni ular amalda intrinsic holatsiz flyweight (qarang: [Flyweight](02-strukturaviy-patternlar.md#26-flyweight-flyweight)). ESLATMA: Java'da bo'lishiladigan holat obyektining tabiiy shakli `enum`, Spring'da esa maydonsiz singleton bean; holat obyektiga maydon qo'shilishi bilan bo'lishish taqiqlanadi va bu o'zgarish jim o'tib ketadi, shuning uchun holat sinflarini maydonsiz saqlash qoida bo'lishi kerak.

To'rtinchi tafsilot patternning yashirin kafolati: o'tishlar Context nuqtai nazaridan atomar, chunki o'tishda bitta o'zgaruvchi qayta bog'lanadi, bir nechta emas. Shuning uchun yarim o'tgan, nomuvofiq ichki holat yuzaga kelmaydi - `if` zanjiri bilan yozilgan holat mantiqida esa ikki-uch maydon ketma-ket o'zgargani uchun aynan shunday nomuvofiq oraliq holatlar paydo bo'ladi.
## 3.9 Strategiya (Strategy)

**Tavsif:** Bir vazifani bajarishning bir nechta algoritmini alohida sinflarga ajratib, umumiy interfeys ortida almashtiriladigan qiladi. Mijoz kodi qaysi algoritm ishlayotganini bilmaydi va shart operatorlari o'rniga shunchaki interfeysga tayanadi. Yangi variant qo'shish mavjud kodni o'zgartirishni talab qilmaydi - bu DI konteynerlari bilan eng tabiiy birlashadigan pattern.

**Spring'da qayerda uchraydi:** Spring'ning yarmi Strategy ustida qurilgan: `PasswordEncoder` (`BCryptPasswordEncoder`, `Argon2PasswordEncoder`, `DelegatingPasswordEncoder`), `AuthenticationProvider`, `CacheManager`/`Cache`, `TaskExecutor`, `HttpMessageConverter`, `ClientHttpRequestFactory` (`JdkClientHttpRequestFactory`, `ApacheHttpClient...`), `PlatformTransactionManager`, Spring Retry'dagi `RetryPolicy`/`BackOffPolicy`, Spring Cloud LoadBalancer'dagi `ReactorServiceInstanceLoadBalancer`. Amaliy loyihada esa strategiyalarni `Map<String, PricingStrategy>` yoki `List<Validator>` ko'rinishida inject qilish standart yondashuv; `ObjectProvider` va `@Qualifier` tanlashni nozik boshqarish uchun ishlatiladi.

```java
@Service
class PaymentRouter {
    private final Map<String, PaymentStrategy> strategies; // bean nomi -> strategiya
    PaymentRouter(Map<String, PaymentStrategy> strategies) { this.strategies = strategies; }
    Receipt pay(String provider, Money amount) {
        return strategies.get(provider).charge(amount);
    }
}
```

**Qo'llanish keyslari:**
- To'lov provayderlari (Click, Payme, Stripe) uchun bitta interfeys va provayderga qarab tanlanadigan implementatsiya.
- Narx/chegirma hisoblash algoritmlarini mijoz segmentiga qarab almashtirish.
- Fayl export formatlari (CSV, XLSX, PDF) uchun bir xil shartnoma.
- Retry va backoff siyosatlarini integratsiya turiga qarab sozlash.
- Multi-tenant tizimda tenant'ga xos biznes qoidalarini alohida strategiya bean'lari bilan berish.

**Ehtiyot bo'ling:** Faqat bitta implementatsiya bo'lgan joyda interfeys yaratish - bu "spekulyativ generallik", keraksiz qatlam; ikkinchi variant real paydo bo'lganda ajratish arzonroq. Strategiyalar orasida umumiy mutable state ulashmang va `Map` orqali tanlashda kalitni (bean nomini) oshkora `enum` yoki annotatsiya bilan bog'lang, aks holda noto'g'ri kalit runtime'da `NullPointerException` beradi.

**Qurish qarorlari:** Asosiy qaror - Strategy va Context orasida ma'lumot qanday almashadi, va ikki yo'lning ikkisi ham narx bilan keladi. Birinchi yo'l: Context kerakli ma'lumotni parametr sifatida uzatadi. Ikkisi ajratilgan qoladi va strategiya Context turini bilmaydi, lekin Context sodda strategiyaga ham kerak bo'lmagan ma'lumotni tayyorlab uzatadi. Ikkinchi yo'l: Context o'zini uzatadi va strategiya kerakligini o'zi so'raydi. Strategiya aniq kerakligini oladi, lekin Context o'z ma'lumotiga kengroq interfeys ochishga majbur bo'ladi va ikkisi kuchliroq bog'lanadi.

Shu yerdan o'lchanadigan oqibat chiqadi: Strategy interfeysi barcha konkret strategiyalar uchun umumiy bo'lgani uchun sodda strategiya unga uzatilgan ma'lumotning hammasini ishlatmaydi va Context behuda parametr tayyorlaydi. Agar tayyorlash qimmat bo'lsa (so'rov, hisoblash, tashqi chaqiruv), bog'lanishni ataylab kuchaytirish to'g'ri qaror bo'ladi - masalan ma'lumotni `Supplier` sifatida uzatib, faqat so'ragan strategiya uchun hisoblash. ESLATMA: Java'da oraliq yo'l ham bor va u ko'pincha eng yaxshisi - Context o'zini emas, faqat o'ziga kerakli tor ko'rinishni (`record` yoki kichik interfeys) uzatadi; shunda parametr ro'yxati ham o'smaydi, Context ham ichini ochmaydi.

## 3.10 Shablon metodi (Template Method)

**Tavsif:** Algoritmning umumiy skeletini bazaviy sinfda belgilab, o'zgaradigan qadamlarini abstrakt yoki hook metodlarga chiqaradi. Merosxo'r faqat kerakli qadamni amalga oshiradi, qadamlarning tartibi va invariantlari (resurs ochish/yopish, xatolikni o'girish) baza sinf nazoratida qoladi. Bu takrorlanuvchi infratuzilma kodini bir joyda markazlashtirishning eng tezkor usuli.

**Spring'da qayerda uchraydi:** `JdbcTemplate`, `JmsTemplate`, `RedisTemplate`, `TransactionTemplate`, `RestTemplate` - nomidan ko'rinib turgani kabi, resursni ochish, xatolikni `DataAccessException` ierarxiyasiga o'girish va yopishni o'z ustiga olib, faqat callback qismini sizga qoldiradi (Template Method + Callback birgalikda). `AbstractApplicationContext.refresh()` konteyner ishga tushish skeletini belgilaydi va `postProcessBeanFactory()`, `onRefresh()` kabi hook'larni qoldiradi. Spring Security'dagi `AbstractAuthenticationProcessingFilter.attemptAuthentication()`, Spring MVC'dagi `OncePerRequestFilter.doFilterInternal()`, Spring Batch'dagi `AbstractItemCountingItemStreamItemReader.doRead()` ham shu pattern; platformadagi klassik misol - `HttpServlet.service()` → `doGet()/doPost()`.

**Qo'llanish keyslari:**
- Tashqi integratsiya chaqiruvlari uchun umumiy skelet: logging, timeout, retry, metrika - faqat "so'rovni tuzish" qadami o'zgaradi.
- Import/export pipeline'ida o'qish → validatsiya → transformatsiya → yozish bosqichlarini qat'iy tartibda ushlab turish.
- Custom filter yoki interceptor yozishda Spring'ning `OncePerRequestFilter` kabi baza sinflarini kengaytirish.
- Testlarda umumiy setup/teardown skeletini bazaviy test sinfiga chiqarish.
- Hisobot generatsiyasining umumiy oqimi bilan formatga xos render qadamini ajratish.

**Ehtiyot bo'ling:** Meros qattiq bog'liqlik yaratadi - baza sinf o'zgarganda barcha merosxo'rlar sinishi mumkin va Java'da bitta sinfdan ko'p meros yo'q; shuning uchun ko'p holatda Strategy yoki funksional interfeys (lambda-callback) moslashuvchanroq. Hook metodlarni `public` qilib qo'ymang va konstruktordan chaqirilgan overridable metodlardan voz keching: subclass hali to'liq initsializatsiya bo'lmagan holatda ishlab ketadi.

```java
// Template Method: qat'iy skelet, o'zgaradigan qadamlar subclass'da
public abstract class ImportTemplate<T> {

    public final ImportResult run(Path file) {       // final: skelet o'zgarmaydi
        List<T> rows = parse(file);
        List<T> valid = rows.stream().filter(this::isValid).toList();
        save(valid);
        return new ImportResult(rows.size(), valid.size());
    }

    protected abstract List<T> parse(Path file);     // o'zgaradigan qadam
    protected abstract boolean isValid(T row);
    protected abstract void save(List<T> rows);
}
```

**Qurish qarorlari:** Birinchi va eng ko'p unutiladigan talab hujjatlashtirishga tegishli: qaysi amal hook (qayta yozish MUMKIN) va qaysi biri abstrakt (qayta yozish SHART) ekanini oshkora aytish kerak. Subclass yozuvchi buni bilmasa abstrakt sinfni samarali qayta ishlatolmaydi - u yo ortiqcha metod qayta yozadi, yo kerakli qadamni tashlab ketadi. ESLATMA: Java'da ajratishning yarmi tilda bor (`abstract` metod qayta yozishni majburlaydi), qolgan yarmi esa Javadoc zimmasida: hook metodning Javadoc i default xulqni va qayta yozilganda nima o'zgarishini aytishi kerak.

Ikkinchi qaror miqdorga tegishli: subclass qayta yozishi kerak primitiv amallar sonini minimallashtiring. Qancha ko'p amal qayta yozilishi shart bo'lsa, shuncha og'ir va xatoga moyil kengaytirish chiqadi; uchta majburiy metod o'rniga bitta parametr obyekti yoki bitta strategiya ko'pincha yetadi. Uchinchi qaror esa o'qiluvchanlikka tegishli va arzon: qayta yozilishi kerak amalni nomlash konventsiyasi bilan belgilab qo'yish. Spring'ning `doFilterInternal`, `doRead` va `doInBackground` nomlaridagi `do` prefiksi aynan shu vazifani bajaradi - template metod va kengaytirish nuqtasi koddan bir qarashda ajraladi.

To'rtinchi qaror merosning eng tez-tez uchraydigan xatosini yo'q qiladi: ota amalini qayta yozib `super` ni chaqirishni esdan chiqarish oson va bu xato jim o'tadi, chunki kod kompilyatsiya qilinadi. Yechim strukturaviy: shu amalni template metodga aylantirib, uning o'zgaradigan qismini hook'ka chiqarsangiz, ota nazoratni o'z qo'lida ushlaydi va chaqirishni esdan chiqarish imkoniyati yo'qoladi. Bu meros ierarxiyasida nazoratning yuqoriga va pastga sakrashi muammosidan farq qiladi (qarang: [Yo-Yo muammosi](25-anti-patternlar.md#2512-yo-yo-muammosi-yo-yo-problem)): bu yerda gap bitta metodning shartnomasida.
## 3.11 Tashrifchi (Visitor)

**Tavsif:** Obyekt tuzilmasi (masalan AST yoki hujjat daraxti) ustida bajariladigan amalni alohida "tashrifchi" sinfga chiqaradi, shunda yangi amal qo'shish uchun element sinflarini o'zgartirish kerak bo'lmaydi. Double dispatch orqali har bir element tashrifchining o'ziga mos `visitXxx()` metodini chaqiradi. Natijada tuzilma barqaror, amallar esa erkin kengayadigan bo'ladi.

**Spring'da qayerda uchraydi:** Spring Core ichida `BeanDefinitionVisitor` bean definition'lardagi qiymatlarni aylanib chiqib placeholder'larni almashtiradi (`PropertySourcesPlaceholderConfigurer` shu orqali ishlaydi). Spring o'z ichiga repackage qilgan ASM'da `ClassVisitor`/`AnnotationVisitor` (`SimpleAnnotationMetadataReadingVisitor`) class fayllarini yuklamasdan skanerlaydi - `@ComponentScan` va `@ConditionalOn...` shartlari aynan shunga tayanadi. Platformada `java.nio.file.FileVisitor`/`SimpleFileVisitor` daraxt bo'ylab yurish uchun, `javax.lang.model.element.ElementVisitor` esa annotation processor'lar (MapStruct, Lombok) uchun; Hibernate 6 va Querydsl query daraxtlarini visitor bilan SQL'ga o'giradi, Jackson'ning `JsonNode` ustidagi obxodlari ham shu uslubda yoziladi.

**Qo'llanish keyslari:**
- Query DSL yoki filtr daraxtini turli backend'larga (SQL, Elasticsearch, Mongo) o'girish.
- Konfiguratsiya yoki hujjat daraxti bo'ylab validatsiya, statistika va transformatsiya amallarini mustaqil qo'shish.
- Annotation processing yoki kod generatsiyasida AST tahlili.
- Hisob-kitob daraxtlari (narx formulalari, soliq qoidalari) ustida bir nechta hisoblash amalini bajarish.
- Statik tahlil/lint vositalarida bir xil daraxt ustida ko'p tekshiruvni ishlatish.

**Ehtiyot bo'ling:** Visitor element turlari barqaror bo'lganda foydali: yangi element turi qo'shilsa, barcha visitor'larni o'zgartirishga majbur bo'lasiz - bu teskari yo'nalishdagi qattiqlik. Java 21'dagi `sealed` ierarxiya + `switch` pattern matching aksariyat holatda visitor boilerplate'ini butunlay o'rnini bosadi, shuning uchun yangi kodda avval shuni ko'rib chiqing.

```java
// Visitor: yopiq ierarxiya ustida yangi amal, sinflarga tegmasdan
public sealed interface Node permits Literal, Add, Mul {}
public record Literal(BigDecimal value) implements Node {}
public record Add(Node left, Node right) implements Node {}
public record Mul(Node left, Node right) implements Node {}

// Pattern matching bilan visitor: yangi amal = yangi metod, sealed to'liqlikni majburlaydi
public static BigDecimal eval(Node n) {
    return switch (n) {
        case Literal l -> l.value();
        case Add a -> eval(a.left()).add(eval(a.right()));
        case Mul m -> eval(m.left()).multiply(eval(m.right()));
    };
}
```

**Qurish qarorlari:** Birinchi qaror - obyekt tuzilmasini kim aylanib chiqadi, va uch variant bor. Tuzilmaning o'zi aylansa (kolleksiya elementlar bo'ylab yurib `accept` ni chaqiradi, kompozit o'zini rekursiv aylanadi) obxod kodi bitta joyda qoladi va bu eng ko'p ishlatiladigan yo'l. Alohida [iterator](#34-iterator-iterator) ishlatish obxod tartibini almashtirish imkonini beradi. Uchinchi variant - obxodni visitor'ning o'ziga yuklash: u obxod kodini har visitor'da takrorlaydi, shuning uchun faqat obxod tartibi amal natijasiga bog'liq bo'lganda (masalan ildizdan pastga qarab kontekst to'planganda) asosli bo'ladi.

Ikkinchi qaror patternning kam nomlanadigan foydasiga tegishli: visitor obxod paytida holat to'playdi. Visitor bo'lmasa shu holat obxod metodlariga qo'shimcha argument bo'lib o'tar yoki global o'zgaruvchi bo'lib qolar edi; visitor esa uni o'z maydonida saqlaydi va obxod imzosini toza qoldiradi. Uchinchi - to'lanadigan narx: visitor inkapsulyatsiyani buzadi, chunki element ichki holatini visitor'ga yetarli qilish uchun sinflarga ochiq amallar qo'shishga majbur bo'lasiz. Bu element turi qo'shish qiyinligidan alohida narx va u patternni tanlashdan oldin hisobga olinadi.

Visitor'ni iteratordan ustun qiladigan bitta xususiyat bor va u tanlovni ko'pincha hal qiladi: visitor bir-biriga aloqasi yo'q, umumiy ota turi bo'lmagan sinflarni ham aylanadi, iterator esa faqat umumiy turga ega elementlar ustida ishlaydi. ESLATMA: Java'da shu ustunlik `sealed` ierarxiya bilan yo'qoladi - umumiy ota tur majburiy bo'lgani uchun pattern matching'li `switch` yetadi; aralash, umumiy turga keltirilmaydigan sinflar ustida esa visitor hali ham yagona yo'l.
## 3.12 Bo'sh obyekt (Null Object)

**Tavsif:** `null` qaytarish o'rniga interfeysni amalga oshiruvchi, lekin "hech nima qilmaydigan" neytral obyekt qaytaradi. Mijoz kodi `if (x != null)` tekshiruvlaridan xoli bo'ladi va xulq bir xil polimorf yo'l bilan davom etadi. Bu, ayniqsa, optional hamkor komponentlar (logger, metrika, cache, notifier) uchun kodni ancha toza qiladi.

**Spring'da qayerda uchraydi:** Spring Framework'da `NoOpCacheManager`/`NoOpCache` (cache'ni o'chirish uchun), Spring Security'da `NullRequestCache`, `NullRememberMeServices`, `NullSecurityContextRepository` va WebFlux uchun `NoOpServerSecurityContextRepository`, shuningdek `ProviderManager` ichidagi null event publisher. spring-jcl modulidagi `NoOpLog`, Micrometer'dagi `Tracer.NOOP` va noop meter'lar, SLF4J'dagi `NOPLogger` ham shu g'oyaning tayyor implementatsiyalari. Java'da `Collections.emptyList()`, `Optional.empty()` va `Function.identity()` neytral qiymatlar sifatida xizmat qiladi; Spring Data repository'lari esa `null` o'rniga `Optional<T>` qaytarishni standart qilib qo'ygan.

**Qo'llanish keyslari:**
- Test va dev profilida haqiqiy xabarnoma yoki to'lov gateway'i o'rniga no-op implementatsiya ulash.
- Cache yoki metrika ixtiyoriy bo'lgan modulda `@ConditionalOnMissingBean` bilan no-op fallback berish.
- Domenda "mehmon foydalanuvchi" yoki "chegirmasiz siyosat" kabi neytral qiymatlarni obyekt sifatida ifodalash.
- Kolleksiya qaytaruvchi metodlarda hamisha bo'sh kolleksiya qaytarib, chaqiruvchini NPE'dan saqlash.
- Feature flag o'chirilganda butun strategiyani no-op variantga almashtirish.

**Ehtiyot bo'ling:** Null Object xatoni yashirib qo'yishi mumkin - konfiguratsiya yo'qolgani sababli hamma joyda jim ishlaydigan no-op bean ulanib qolsa, muammo production'da ancha keyin ma'lum bo'ladi; shuning uchun ishga tushishda ogohlantirish logi yoki Actuator'da ko'rinadigan belgi qoldiring. Shuningdek, "hech nima qilmaslik" domen uchun to'g'ri javob bo'lmagan joyda (masalan to'lovni o'tkazish) no-op emas, oshkora xatolik kerak.

```java
// Null Object: null tekshiruvi o'rniga hech nima qilmaydigan implementatsiya
public interface AuditLog {
    void record(String event);

    AuditLog NONE = event -> { };            // bo'sh obyekt
}

@Configuration
class AuditConfig {
    @Bean
    @ConditionalOnProperty(name = "audit.enabled", havingValue = "false")
    AuditLog disabledAuditLog() { return AuditLog.NONE; }   // chaqiruvchi kod o'zgarmaydi
}
```

## 3.13 Spetsifikatsiya (Specification)

**Tavsif:** Biznes qoidasini (predikatni) alohida obyekt sifatida kapsulalaydi va ularni `and`, `or`, `not` operatorlari bilan kompozitsiya qilish imkonini beradi. Natijada murakkab filtrlash shartlari qayta ishlatiladigan, mustaqil testlanadigan bloklarga ajraladi va service qatlamidagi uzun `if` zanjirlari yo'qoladi. Ko'pincha ikki qiyofada bo'ladi: in-memory kolleksiyani tekshirish va ma'lumotlar bazasiga query sifatida tarjima qilish.

**Spring'da qayerda uchraydi:** Spring Data JPA'ning `org.springframework.data.jpa.domain.Specification<T>` interfeysi aynan shu pattern: `JpaSpecificationExecutor<T>` repository'ga `findAll(Specification)`, `count(Specification)`, `findBy(Specification, Function)` metodlarini qo'shadi, `Specification.where(...).and(...).or(...).not()` esa kompozitsiya beradi. Spring Data MongoDB'da `Criteria` va `Query`, Querydsl integratsiyasida `QuerydslPredicateExecutor` va `BooleanExpression` xuddi shu rolni bajaradi; sof domenda esa `java.util.function.Predicate<T>` va uning `and/or/negate` metodlari yetarli.

**Qo'llanish keyslari:**
- Admin panelidagi dinamik qidiruv: foydalanuvchi to'ldirgan filter maydonlaridan runtime'da `Specification` yig'ish.
- Murakkab biznes qoidasini ("faol, KYC o'tgan va limitdan oshmagan mijoz") bitta nomli obyektga chiqarib, bir necha service'da qayta ishlatish.
- Multi-tenant yoki soft-delete kabi doimiy shartlarni baza `Specification` sifatida har bir query'ga qo'shish.
- Buyurtma chegirmaga loyiqligini aniqlash qoidalarini alohida testlanadigan sinflarga ajratish.
- Querydsl `BooleanExpression`lari orqali type-safe hisobot filtrlarini qurish.

**Ehtiyot bo'ling:** `Specification` ichida JPA Criteria API bilan ishlash tezda o'qishga qiyin kodga aylanadi, shuning uchun uni factory metodlar bilan nomlab yashirish kerak; shuningdek in-memory `Predicate` va baza `Specification` versiyalarini bir sinfda aralashtirish semantik farq (null, `LIKE` case-sensitivity, collation) tufayli xatolarga olib keladi.

```java
// Specification: so'rov sharti qayta ishlatiladigan obyekt
public final class OrderSpecs {
    public static Specification<Order> status(OrderStatus s) {
        return (root, q, cb) -> cb.equal(root.get("status"), s);
    }
    public static Specification<Order> createdAfter(Instant t) {
        return (root, q, cb) -> cb.greaterThan(root.get("createdAt"), t);
    }
}

// Shartlar birlashtiriladi, repository metodlari ko'paymaydi
Page<Order> page = orderRepository.findAll(
        OrderSpecs.status(PENDING).and(OrderSpecs.createdAfter(yesterday)),
        PageRequest.of(0, 50));
```

## 3.14 Xizmatkor (Servant)

**Tavsif:** Bir guruh o'xshash obyektlarga xos bo'lgan xatti-harakatni ularning har biriga metod qo'shish orqali emas, balki tashqi "servant" sinfiga chiqarish patterni. Obyektlar faqat servant'ga kerak bo'lgan minimal interfeysni taqdim etadi, logika esa bitta joyda yashaydi. Bu Visitor'dan soddaroq: hech qanday double dispatch yo'q, servant shunchaki parametr sifatida obyektni oladi.

**Spring'da qayerda uchraydi:** Spring ekosistemida bu odatda `@Service` yoki `@Component` bo'lgan stateless helper bean ko'rinishida amalga oshiriladi: masalan `PasswordEncoder` (`BCryptPasswordEncoder`) `UserDetails` obyektlariga xizmat qiladi, `ConversionService`/`Converter<S,T>` turli DTO'larga, `Validator` (`org.springframework.validation.Validator` yoki Jakarta Bean Validation `jakarta.validation.Validator`) esa model obyektlariga xizmat qiladi. JDK'dagi `java.util.Collections` va `java.util.Arrays` ham klassik servant misollari.

**Qo'llanish keyslari:**
- Bir nechta entity uchun umumiy audit maydonlarini to'ldiruvchi `AuditStampService`.
- DTO va entity o'rtasida mapping qiluvchi stateless mapper bean (MapStruct generatsiya qilgan sinflar).
- Turli hisobot obyektlarini formatlovchi `ReportFormatter` beani.
- Domain obyektlariga tashqi API uchun imzo (signature) hisoblab beruvchi `SignatureCalculator`.
- Legacy entity'larni o'zgartirmasdan ularga yangi validatsiya qo'shish.

**Ehtiyot bo'ling:** Servant'ga juda ko'p mas'uliyat yuklasa, u anemik domen modeli va "god service" ga olib keladi - obyektning o'ziga tegishli invariantlar entity ichida qolishi kerak. Servant stateless bo'lishi shart, aks holda singleton bean sifatida thread-safety muammolari paydo bo'ladi.

```java
// Servant: bir nechta turga xizmat qiladigan stateless yordamchi
@Service
public class ShippingCostCalculator {              // xizmatkor: holati yo'q

    public Money cost(Shippable item, Destination to) {
        BigDecimal base = item.weightKg().multiply(to.ratePerKg());
        return Money.of(base.add(to.fixedFee()), to.currency());
    }
}
// Order, Parcel va Pallet - hammasi Shippable, lekin hisob mantiqini saqlamaydi
```

## 3.15 Ravon interfeys (Fluent Interface)

**Tavsif:** Metodlar `this` yoki yangi obyekt qaytarib, chaqiruvlarni zanjir shaklida yozish imkonini beradigan API dizayni. Maqsad - kodni domen tiliga yaqin, o'qishga oson qilish va ko'p parametrli konstruktorlar yoki setter to'dasidan qutulish. Ko'pincha Builder bilan birga keladi, ammo fluent interface konfiguratsiya va query qurishda ham mustaqil ishlatiladi.

**Spring'da qayerda uchraydi:** Spring Framework 6.x bunga to'la: `RestClient.create().get().uri(...).retrieve().body(X.class)`, `WebClient`, `RestTemplateBuilder`, `MockMvcRequestBuilders.get("/x").param(...)`, `UriComponentsBuilder.fromUriString(...).queryParam(...).build()`. Spring Security 6.x'dagi lambda DSL (`http.authorizeHttpRequests(a -> a.requestMatchers("/admin/**").hasRole("ADMIN")).csrf(Customizer::withDefaults)`) va Spring Data'ning `Criteria`/`Query`, hamda Java Stream API ham shu uslubda.

**Qo'llanish keyslari:**
- Tashqi HTTP integratsiyalarini `RestClient` yoki `WebClient` zanjiri bilan o'qishga oson yozish.
- `SecurityFilterChain` konfiguratsiyasini lambda DSL orqali deklarativ tasvirlash.
- Test fixture'larini `OrderTestBuilder.anOrder().paid().withItems(3).build()` ko'rinishida yaratish.
- Murakkab URI va query parametrlarini `UriComponentsBuilder` bilan xavfsiz qurish.
- Domain-specific til ko'rinishidagi validatsiya yoki hisobot konfiguratsiyasi API'si.

**Ehtiyot bo'ling:** Mutable `this` qaytaradigan fluent obyekt shared holatda xavfli - har bir qadamda yangi immutable obyekt qaytarish ishonchliroq; shuningdek zanjir yarmida qolgan obyekt (`build()` chaqirilmagan) va noto'g'ri tartibda chaqirish mumkin bo'lgan API xatolarni compile-time'da emas, runtime'da yuzaga chiqaradi.

```java
// Fluent interface: qurish qadamlari o'qiladigan zanjirga aylanadi
public final class QueryBuilder {
    private final StringBuilder where = new StringBuilder();

    public static QueryBuilder orders() { return new QueryBuilder(); }

    public QueryBuilder status(OrderStatus s) { return add("status = '" + s + "'"); }
    public QueryBuilder after(LocalDate d)    { return add("created_at > '" + d + "'"); }

    private QueryBuilder add(String cond) {
        if (!where.isEmpty()) where.append(" AND ");
        where.append(cond);
        return this;                                 // zanjir uchun o'zini qaytaradi
    }
    public String build() { return "SELECT * FROM orders WHERE " + where; }
}

// Spring'dagi tanish zanjir
Order o = restClient.get().uri("/orders/{id}", id).retrieve().body(Order.class);
```

## 3.16 Callback (Callback)

**Tavsif:** Chaqiruvchi tomon o'z kodining bir qismini funksiya yoki interfeys implementatsiyasi sifatida boshqa komponentga uzatadi, u esa kerakli paytda uni chaqiradi. Bu nazoratni teskari aylantiradi (inversion of control): infratuzilma hayotiy siklni boshqaradi, biznes logikasi faqat "foydali ish"ni beradi. Sinxron (template metod ichida) yoki asinxron (natija kelganda chaqiriladigan handler) bo'lishi mumkin.

**Spring'da qayerda uchraydi:** `JdbcTemplate` ning `RowMapper`, `ResultSetExtractor`, `PreparedStatementSetter`, `ConnectionCallback` interfeyslari; `TransactionTemplate.execute(TransactionCallback)`; `RedisTemplate`/`RabbitTemplate` callback'lari; `KafkaTemplate.send(...).whenComplete(...)` (`CompletableFuture`); Spring Boot'ning `ApplicationRunner`/`CommandLineRunner`; lifecycle callback'lari sifatida `InitializingBean`, `DisposableBean`, `BeanPostProcessor`, `@PostConstruct`. Java tomonida `java.util.function.*` interfeyslari va `CompletableFuture.thenApply/exceptionally`.

**Qo'llanish keyslari:**
- `JdbcTemplate.query(sql, rowMapper)` bilan `ResultSet` ni domen obyektiga aylantirish.
- `TransactionTemplate` orqali faqat kerakli kod blokini programmatik transaksiyaga o'rash.
- Asinxron Kafka yoki HTTP so'rov natijasini `whenComplete` callback'ida qayta ishlash.
- Retry kutubxonasiga (`RetryTemplate.execute(RetryCallback)`) qayta bajarilishi kerak bo'lgan operatsiyani berish.
- Bean yaratilgandan keyin cache'ni oldindan to'ldirish uchun lifecycle callback.

**Ehtiyot bo'ling:** Asinxron callback'larni ketma-ket ulash "callback hell" va kuzatib bo'lmaydigan stack trace'larga olib keladi - reactive operator'lar yoki `CompletableFuture` kompozitsiyasi afzal. Callback ichida `ThreadLocal`ga tayanmang: transaksiya, `SecurityContext` va MDC asinxron thread'ga avtomatik ko'chmaydi.

```java
// Callback: nima qilishni chaqiruvchi beradi, qachon qilishni kutubxona
@Repository
public class OrderJdbc {
    private final JdbcClient db;

    public List<OrderRow> recent(int limit) {
        return db.sql("SELECT id, status, total FROM orders ORDER BY id DESC LIMIT :n")
                 .param("n", limit)
                 // RowMapper - callback: qator qanday o'qilishini biz aytamiz
                 .query((rs, i) -> new OrderRow(rs.getLong("id"),
                                                rs.getString("status"),
                                                rs.getBigDecimal("total")))
                 .list();
    }
}
```

## 3.17 Pipeline (obyekt darajasida) (Pipeline (object-level))

**Tavsif:** Ishlov berishni ketma-ket bosqichlarga (stage) ajratadi, har bir bosqich kirishni qabul qilib, chiqishni keyingisiga uzatadi. Chain of Responsibility'dan farqi - bu yerda maqsad so'rovni "kimga tegishli" ekanini aniqlash emas, balki ma'lumotni bosqichma-bosqich transformatsiya qilish. Bosqichlar mustaqil, almashtiriladigan va alohida testlanadigan bo'ladi.

**Spring'da qayerda uchraydi:** Spring Integration'ning `IntegrationFlow` DSL'i (`IntegrationFlow.from(...).transform(...).filter(...).handle(...)`) to'g'ridan-to'g'ri pipeline; Spring Batch'da `Step` ketma-ketligi va `CompositeItemProcessor`; Spring Cloud Stream'da `Function` kompozitsiyasi (`spring.cloud.function.definition=a|b|c`); `FilterChain`/`SecurityFilterChain` ham pipeline ko'rinishida. Sof Java'da `Function.andThen`/`compose`, Stream API va `Flux`/`Mono` operator zanjirlari.

**Qo'llanish keyslari:**
- ETL: faylni o'qish → validatsiya → boyitish (enrichment) → normalizatsiya → bazaga yozish.
- Spring Batch `CompositeItemProcessor` bilan har bir yozuvga bir nechta transformatsiya ketma-ket qo'llash.
- Kiruvchi webhook payload'ini dekodlash, imzoni tekshirish va kanonik eventga aylantirish.
- Hisobot generatsiyasi: ma'lumot yig'ish → agregatsiya → formatlash → eksport.
- Spring Cloud Stream'da bir nechta `Function` beanini `|` bilan birlashtirib stream pipeline qurish.

**Ehtiyot bo'ling:** Pipeline bosqichlari orasida mutable shared kontekst obyektini uzatish yashirin bog'lanish (coupling) yaratadi va bosqich tartibiga sezgir qiladi - immutable natija obyektlari afzal. Xatolik boshqaruvi va partial failure strategiyasini oldindan belgilang, aks holda pipeline o'rtasida uzilgan ish qayerda qolganini aniqlash qiyin bo'ladi.

```java
// Pipeline: bosqichlar bir xil shakl, tartib aniq va o'zgartirilishi oson
public interface Stage<T> extends UnaryOperator<T> {}

@Service
public class InvoicePipeline {
    private final List<Stage<Invoice>> stages;   // validate -> enrich -> price -> round

    public InvoicePipeline(List<Stage<Invoice>> stages) { this.stages = stages; }

    public Invoice process(Invoice in) {
        Invoice out = in;
        for (Stage<Invoice> s : stages) out = s.apply(out);
        return out;
    }
}
```

## 3.18 Ikki tomonlama dispatch (Double Dispatch)

**Tavsif:** Chaqiriladigan metodni bitta emas, ikkita obyektning runtime turiga qarab tanlash mexanizmi. Java faqat bitta argument bo'yicha (receiver) virtual dispatch qiladi, shuning uchun ikkinchi dispatch odatda `accept(visitor)` → `visitor.visit(this)` ko'rinishidagi ikki bosqichli chaqiruv bilan erishiladi. Bu `instanceof` zanjirlari va qo'lda tur tekshiruvini yo'q qiladi.

**Spring'da qayerda uchraydi:** Spring'ning `BeanDefinitionVisitor`, `org.springframework.asm` va `MethodVisitor` asosidagi bytecode tahlili, hamda `org.springframework.expression`/SpEL AST ichidagi node'lar shu uslubda ishlaydi; `ApplicationListener<E extends ApplicationEvent>` va `@EventListener` esa event turi bo'yicha dispatchni `GenericApplicationListener`/`ResolvableType` orqali amalga oshiradi. Java 21+ dagi `sealed` interfeyslar va pattern matching `switch` ko'pincha klassik double dispatch o'rniga zamonaviy alternativa bo'lib xizmat qiladi.

**Qo'llanish keyslari:**
- To'lov usuli va valyuta kombinatsiyasiga qarab har xil komissiya hisoblash strategiyasini tanlash.
- Hujjat turi va eksport formati (PDF/XLSX/CSV) juftligiga mos renderer tanlash.
- AST yoki query daraxti node'lari ustida bir nechta xil "tashrifchi" (optimizator, validator, printer) ishlatish.
- Domain event turi va kanal (email/SMS/push) juftligi bo'yicha xabar shablonini aniqlash.
- Collision/interaksiya qoidalari: ikki xil obyekt turi uchrashganda nima bo'lishini aniqlash.

**Ehtiyot bo'ling:** Double dispatch tur kombinatsiyalari ko'paygan sayin N×M metodga o'sadi va yangi tur qo'shilganda barcha visitor'larni o'zgartirishga majbur qiladi; Java 21+ loyihalarda `sealed` iyerarxiya ustida pattern matching `switch` ko'pincha soddaroq va compile-time to'liqlik tekshiruvini (exhaustiveness) beradi.

```java
// Double dispatch: natija ikki argumentning turiga bog'liq
public BigDecimal fee(Instrument instrument, Account account) {
    return switch (instrument) {
        case Stock s -> switch (account) {
            case Retail r -> s.price().multiply(new BigDecimal("0.003"));
            case Institutional i -> s.price().multiply(new BigDecimal("0.0005"));
        };
        case Bond b -> switch (account) {
            case Retail r -> b.nominal().multiply(new BigDecimal("0.001"));
            case Institutional i -> BigDecimal.ZERO;
        };
    };
}
// Ikki sealed ierarxiya: kompilyator barcha juftlikni qamrab olishga majbur qiladi
```

## 3.19 Event agregatori (Event Aggregator)

**Tavsif:** Ko'p sonli publisher va subscriber o'rtasida bitta markaziy vositachi (hub) turadi; komponentlar bir-biriga emas, faqat agregatorga bog'lanadi. Bu N×M bog'lanishni N+M ga kamaytiradi va yangi tinglovchini mavjud kodga tegmasdan qo'shish imkonini beradi. Observer'dan farqi - subscription manbasi har bir publisher emas, yagona nuqta.

**Spring'da qayerda uchraydi:** Spring Framework'ning ichki event mexanizmi aynan shu: `ApplicationEventPublisher.publishEvent(...)`, `@EventListener`, `@TransactionalEventListener(phase = AFTER_COMMIT)`, `ApplicationEventMulticaster` (standart `SimpleApplicationEventMulticaster`, `taskExecutor` bilan asinxron qilish mumkin) va `@Async` bilan birga ishlatish. Tashqi masshtabda Spring Integration'ning `PublishSubscribeChannel`, Spring Cloud Bus, hamda Kafka/RabbitMQ topic'lari shu rolni bajaradi.

**Qo'llanish keyslari:**
- `OrderPlacedEvent` ni e'lon qilib, email yuborish, ombor zahirasini kamaytirish va analitikaga yozishni mustaqil listener'larga ajratish.
- Modulith arxitekturasida modullar o'rtasida to'g'ridan-to'g'ri bean injection o'rniga event orqali aloqa.
- `@TransactionalEventListener(AFTER_COMMIT)` bilan faqat transaksiya muvaffaqiyatli tugaganda tashqi tizimga xabar yuborish.
- Cache invalidatsiyasi: ma'lumot o'zgargani haqidagi eventni bir nechta cache egasi tinglashi.
- Domain audit log'ini biznes kodga aralashmasdan event tinglash orqali to'ldirish.

**Ehtiyot bo'ling:** Event oqimi oshgach tizim "kim nimani chaqirdi" ni kuzatish qiyin bo'lgan yashirin bog'lanishga aylanadi - muhim biznes oqimini faqat eventga tayanib qurmang. Standart `ApplicationEventMulticaster` sinxron va bir xil thread'da ishlaydi, shuning uchun listener ichidagi sekin yoki exception tashlagan kod publisher'ni ham bloklaydi yoki buzadi; asinxron qilganda transaksiya va `SecurityContext` propagatsiyasini alohida sozlash kerak.

```java
// Event aggregator: ko'p manba, bitta nuqta, iste'molchilar manbani bilmaydi
public record DomainEvent(String type, String aggregateId, Instant at) {}

@Component
public class DomainEventBus {
    private final ApplicationEventPublisher publisher;

    public DomainEventBus(ApplicationEventPublisher publisher) { this.publisher = publisher; }

    public void publish(DomainEvent e) { publisher.publishEvent(e); }
}

@Component
class AuditListener {
    @Async                                        // tinglovchi chaqiruvchini kutmaydi
    @EventListener
    void on(DomainEvent e) { /* audit yozuvi */ }
}
```

## 3.20 O'rab bajarish (Execute Around)

**Tavsif:** Takrorlanadigan "oldin/keyin" kodni (resurs olish va yopish, transaksiya boshlash va yakunlash, vaqt o'lchash) bitta metodga yashirib, foydali ishni callback sifatida uning ichida bajaradi. Mijoz faqat o'zining logikasini yozadi, resurs boshqaruvi va xatolik tozalashi kafolatlangan holda markazda qoladi. Bu Template Method'ning kompozitsiyaga asoslangan, moslashuvchan varianti.

**Spring'da qayerda uchraydi:** `TransactionTemplate.execute(TransactionCallback)`, `JdbcTemplate.execute(ConnectionCallback)`, `JdbcClient` (Spring Framework 6.1+), `RetryTemplate.execute(...)`, `RedisTemplate.execute(SessionCallback)`, `TransactionalOperator.transactional(...)` (reactive). Deklarativ ko'rinishi - `@Transactional`, `@Cacheable`, `@Retryable`, `@Timed` annotatsiyalari, ular ostida Spring AOP `MethodInterceptor`/`@Around` advice ishlaydi. Java'da `try-with-resources` ham shu g'oyaning tilga kiritilgan shakli.

**Qo'llanish keyslari:**
- Programmatik transaksiya chegarasini aniq belgilash uchun `TransactionTemplate` ishlatish.
- Tashqi API chaqiruvini retry va timeout siyosati bilan o'rash.
- Metod bajarilish vaqtini va metrikalarni Micrometer `Timer` orqali o'lchash.
- Distributed lock olish, ish bajarish va lock'ni har qanday holatda bo'shatish.
- MDC'ga correlation ID qo'yib, blok tugagach uni tozalash.

**Ehtiyot bo'ling:** Callback ichida checked exception va natija turlarini to'g'ri uzatish (generic `<T>` bilan) oldindan o'ylanmasa, API noqulay bo'lib qoladi; shuningdek `@Transactional` kabi annotatsiya proxy orqali ishlaydi, shuning uchun bir sinf ichidagi self-invocation advice'ni butunlay chetlab o'tadi.

```java
// Execute Around: ochish va yopish kutubxonada, o'rtasi chaqiruvchida
@Component
public class WithAdvisoryLock {
    private final JdbcClient db;

    public <T> T run(long key, Supplier<T> body) {
        db.sql("SELECT pg_advisory_lock(:k)").param("k", key).update();
        try {
            return body.get();                    // faqat bu qism o'zgaradi
        } finally {
            db.sql("SELECT pg_advisory_unlock(:k)").param("k", key).update();
        }
    }
}

// Chaqiruvchi lock olish va bo'shatishni eslab qolmaydi
Receipt r = withAdvisoryLock.run(accountId, () -> transfer(from, to, amount));
```

## 3.21 Chekli holatlar mashinasi (Finite State Machine (Spring Statemachine))

**Tavsif:** Obyektning mumkin bo'lgan holatlari, ular orasidagi o'tishlar va o'tishni qo'zg'atuvchi eventlarni aniq modellashtiradi. Biznes jarayoni (buyurtma, to'lov, ariza) `if/else` va boolean flag'lar o'rniga deklarativ holat diagrammasiga aylanadi, noto'g'ri o'tishlar esa markazda bloklanadi. Har bir o'tishga guard (shart) va action (yon ta'sir) bog'lash mumkin.

**Spring'da qayerda uchraydi:** Spring Statemachine (`org.springframework.statemachine`) moduli: `@EnableStateMachine`, `StateMachineConfigurerAdapter`, `StateMachine<S,E>`, `@WithStateMachine`, `@OnTransition`, guard va action uchun `Guard<S,E>`/`Action<S,E>`, hamda holatni saqlash uchun `StateMachinePersister` (JPA, Redis). Soddaroq holatlarda `enum`ga asoslangan o'z FSM'ingiz (`enum OrderState { ... abstract boolean canTransitionTo(OrderState) }`) yoki Spring Batch/Spring Integration oqimlari yetarli bo'ladi; `@Transactional` bilan birga holat o'zgarishi atomar saqlanadi.

**Qo'llanish keyslari:**
- Buyurtma hayotiy sikli: `CREATED → PAID → SHIPPED → DELIVERED`, qaytarish va bekor qilish tarmoqlari bilan.
- Kredit arizasini ko'p bosqichli tasdiqlash workflow'i (hujjat tekshiruvi, skoring, qo'lda tasdiq).
- To'lov tranzaksiyasi holatlari: authorized, captured, refunded, chargeback.
- KYC/onboarding jarayonini bosqichlar va har bosqichdagi ruxsat etilgan amallar bilan boshqarish.
- IoT yoki qurilma sessiyasining ulanish holatlarini kuzatish.

**Ehtiyot bo'ling:** Spring Statemachine qo'shimcha infratuzilma va o'rganish narxini keltiradi - oddiy 3-4 holatli oqim uchun `enum` asosidagi o'tish jadvali yetarli va osonroq. Holat mashinasi instance'i stateful, shuning uchun uni singleton bean sifatida bir necha request orasida ulashish xato: har bir biznes obyekt uchun alohida instance oling yoki `StateMachinePersister` bilan holatni bazadan tiklang.

```java
// FSM: ruxsat etilgan o'tishlar deklarativ, kodda if zanjiri yo'q
@Configuration
@EnableStateMachineFactory
class OrderStateMachineConfig extends StateMachineConfigurerAdapter<OrderState, OrderEvent> {

    @Override
    public void configure(StateMachineStateConfigurer<OrderState, OrderEvent> states)
            throws Exception {
        states.withStates().initial(OrderState.NEW).states(EnumSet.allOf(OrderState.class));
    }

    @Override
    public void configure(StateMachineTransitionConfigurer<OrderState, OrderEvent> t)
            throws Exception {
        t.withExternal().source(OrderState.NEW).target(OrderState.PAID).event(OrderEvent.PAY)
         .and()
         .withExternal().source(OrderState.PAID).target(OrderState.SHIPPED).event(OrderEvent.SHIP);
    }
}
```

## 3.22 Qoidalar dvigateli / Siyosat (Rules Engine / Policy)

**Tavsif:** Biznes qoidalarini kod shoxlari o'rniga deklarativ "shart → harakat" to'plami sifatida tashqariga chiqaradi va ularni dvigatel (engine) baholaydi. Qoidalar ko'p, tez-tez o'zgaradigan va biznes tomonidan boshqariladigan domenlarda deploy qilmasdan yoki minimal o'zgartirish bilan yangilash imkonini beradi. Policy varianti esa bitta qarorni (masalan, kim nimaga ruxsatli) almashtiriladigan obyektga kapsulalaydi.

**Spring'da qayerda uchraydi:** Spring'ning o'z SpEL mexanizmi (`org.springframework.expression.spel.standard.SpelExpressionParser`) oddiy qoidalarni matn sifatida baholash uchun ishlatiladi; Spring Security'da policy aniq ko'rinadi - `AuthorizationManager<T>`, `@PreAuthorize("hasRole('ADMIN') and #order.ownerId == authentication.name")`, `PermissionEvaluator`, `AccessDecisionManager` (legacy). Tashqi kutubxonalar: Drools (KIE `KieContainer`, `KieSession`), Easy Rules (`io.github.j-easy:easy-rules`), yoki Open Policy Agent'ga tashqi chaqiruv. Oddiy holatlarda `List<Rule>` bean kolleksiyasi va `@Order` bilan tartiblangan Spring bean'lar yetarli.

**Qo'llanish keyslari:**
- Chegirma va loyalty qoidalari: marketing tez-tez o'zgartiradigan shartlar to'plami.
- Firibgarlikka qarshi skoring: har bir qoida ball qo'shadi, yig'indi bo'yicha qaror qabul qilinadi.
- Kredit so'rovini avtomatik tasdiqlash/rad etish mezonlari.
- Spring Security `@PreAuthorize` va `AuthorizationManager` bilan murakkab ruxsat siyosatlari.
- Sug'urta tarifini mijoz profiliga qarab hisoblash qoidalari.

**Ehtiyot bo'ling:** To'laqonli rules engine (Drools) katta operatsion va bilim narxiga ega - qoidalar soni o'nlab bo'lsa, oddiy `Specification`/strategy bean'lar ancha tushunarli va tez. Qoidalarni matn (SpEL, skript) sifatida tashqi manbadan olish compile-time xavfsizlikni yo'qotadi va foydalanuvchi kiritgan ifodani baholash code injection xavfini tug'diradi, shuning uchun ishonchsiz kirishni hech qachon `SpelExpressionParser`ga bermang.

```java
// Rules engine: qoidalar ma'lumot, kod o'zgarmaydi
public record Rule(String name, Predicate<Claim> when, Decision then) {}

@Service
public class ClaimPolicy {
    private final List<Rule> rules = List.of(
            new Rule("limit", c -> c.amount().compareTo(LIMIT) > 0, Decision.MANUAL),
            new Rule("blacklist", c -> blacklist.contains(c.customerId()), Decision.REJECT));

    public Decision decide(Claim claim) {
        return rules.stream()
                .filter(r -> r.when().test(claim))
                .findFirst()
                .map(Rule::then)
                .orElse(Decision.AUTO_APPROVE);
    }
}
```

## 3.23 Qora taxta (Blackboard)

**Tavsif:** Aniq algoritmi yo'q murakkab masalalarni hal qilish uchun umumiy "qora taxta" (shared knowledge base) yaratiladi; mustaqil ekspert komponentlar (knowledge source) taxtadagi hozirgi holatni o'qib, o'z hissasini qo'shadi, nazoratchi (control) esa qaysi ekspertni qachon ishlatishni belgilaydi. Yechim bir yo'lda emas, bosqichma-bosqich, qisman natijalar to'planishi orqali shakllanadi. Nutq tanish, OCR, diagnostika va murakkab skoring tizimlarida qo'llanadi.

**Spring'da qayerda uchraydi:** Spring'da maxsus modul yo'q, lekin pattern tipik tarzda quriladi: umumiy holat uchun shared store (`RedisTemplate`, `CacheManager` yoki JPA entity), ekspertlar sifatida umumiy interfeysni implementatsiya qiluvchi bean'lar (`List<KnowledgeSource>` injection va `@Order`), nazoratchi sifatida orkestrator `@Service`, hamda qadamlar o'rtasidagi muvofiqlashtirish uchun `ApplicationEventPublisher` yoki Spring Integration `MessageChannel`. Spring Batch'ning `ExecutionContext` ham bosqichlar orasida qisman natijalarni ulashuvchi kichik "blackboard" sifatida xizmat qiladi.

**Qo'llanish keyslari:**
- Firibgarlikni aniqlash: qurilma, geolokatsiya, xatti-harakat va to'lov tarixi ekspertlari umumiy risk profilini to'ldiradi.
- Hujjatni qayta ishlash: OCR, til aniqlash, maydon ajratish va validatsiya bosqichlari natijalarini umumiy kontekstga yozish.
- Ko'p manbadan kelgan ma'lumotlarni (CRM, billing, support) birlashtirib mijozning yagona profilini shakllantirish.
- Monitoring/diagnostika tizimi: turli analizatorlar umumiy taxtaga gipotezalarni yozib, root cause ni aniqlash.
- Logistikada marshrutni bir nechta evristika yordamida bosqichma-bosqich yaxshilash.

**Ehtiyot bo'ling:** Blackboard mutable shared holatga asoslangani uchun concurrency, versiyalash va "qaysi ekspert nimani o'zgartirdi" muammolari darhol paydo bo'ladi - yozishni atomar qiling va har bir hissani kim qo'shganini qayd eting. Bu pattern faqat haqiqatan determinant algoritmi yo'q masalalar uchun; aniq ketma-ketlik ma'lum bo'lsa, oddiy Pipeline yoki orkestrlangan service ancha arzon va tushunarli.

```java
// Blackboard: ekspertlar umumiy holatga hissa qo'shadi, tartib oldindan ma'lum emas
public interface Expert {
    boolean contribute(Blackboard board);        // true = yangi narsa qo'shdim
}

@Service
public class DiagnosisEngine {
    private final List<Expert> experts;

    public Blackboard solve(Blackboard board, int maxRounds) {
        for (int round = 0; round < maxRounds; round++) {
            boolean progress = false;
            for (Expert e : experts) progress |= e.contribute(board);
            if (!progress) break;                 // hech kim yangi narsa qo'shmadi
        }
        return board;
    }
}
```

## 3.24 O'zgarish uchun dizayn: qayta dizayn sabablari (Designing for Change: Causes of Redesign)

**Tavsif:** Patternlarning asosiy qiymati bugungi masalani hal qilishda emas, ertangi o'zgarishni arzonlashtirishda. Har pattern tizim tuzilishining qaysidir qismini qolganidan mustaqil o'zgartirishga imkon beradi, ya'ni tizimni aniq bir turdagi o'zgarishga chidamli qiladi. GoF buni teskari tomondan beradi: avval qayta dizaynni majburlaydigan sakkizta sabab sanaladi, keyin har sababga qarshi turadigan patternlar ko'rsatiladi. Birinchi sabab - obyektni sinf nomini aniq yozib yaratish: bu sizni interfeysga emas, implementatsiyaga bog'laydi, va yechim yaratishni bilvosita qilish (Abstract Factory, Factory Method, Prototype). Ikkinchisi - aniq amalga bog'liqlik, ya'ni qattiq yozilgan chaqiruv (Chain of Responsibility, Command). Uchinchisi - apparat va platformaga bog'liqlik (Abstract Factory, Bridge). To'rtinchisi - obyektning ichki tasviri yoki implementatsiyasiga bog'liqlik (Abstract Factory, Bridge, Memento, Proxy). Beshinchisi - algoritmga bog'liqlik: algoritm ishlab chiqish davomida kengayadi va almashadi, demak uni ajratish kerak (Builder, Iterator, Strategy, Template Method, Visitor). Oltinchisi - qattiq bog'lanish: bir-biriga chambarchas bog'langan sinflar alohida qayta ishlatilmaydi (Abstract Factory, Bridge, Chain of Responsibility, Command, Facade, Mediator, Observer). Yettinchisi - funksionallikni subclass orqali kengaytirish: har yangi sinf o'z yuki bilan keladi va ierarxiya portlaydi (Bridge, Chain of Responsibility, Composite, Decorator, Observer, Strategy). Sakkizinchisi - sinfni qulay o'zgartirib bo'lmasligi, masalan manba kodi yo'q kutubxona sinfi (Adapter, Decorator, Visitor). Shu ro'yxat pattern tanlashning eng amaliy kirish nuqtasi: avval nima o'zgarishini aniqlang, keyin shu sabab qatoridagi patternlarni o'qing.

**Spring'da qayerda uchraydi:** Spring'ning o'zi shu sakkiz sababga qarshi qurilgan va buni konfiguratsiya darajasida beradi. Sinf nomini qattiq yozishga qarshi `@Bean`, `@ConditionalOnMissingBean` va `ObjectProvider`; platformaga bog'liqlikka qarshi `ServletWebServerFactory` oilasi va `ClientHttpRequestFactory`; ichki tasvirga bog'liqlikka qarshi `Repository` abstraksiyasi va `LazyConnectionDataSourceProxy`; algoritmga bog'liqlikka qarshi `Converter`, `RowMapper` va `AuthorizationManager`; qattiq bog'lanishga qarshi `ApplicationEventPublisher` va Spring Modulith modul event'lari; subclass orqali kengaytirishga qarshi `BeanPostProcessor` va AOP; o'zgartirib bo'lmaydigan sinfga qarshi `@ConfigurationPropertiesBinding` va Jackson mix-in. Shu sabablarning har biri uchun GoF tavsiya qiladigan pattern korpusda alohida yozuv sifatida bor.

**Qo'llanish keyslari:**
- Yangi funksiya loyihalashda "nima o'zgarishi ehtimoli bor" savoliga javob yozib, shundan keyin pattern tanlash.
- Legacy modulni rejalashtirishda qayta dizaynni majburlagan sababni aniqlab, aynan shu o'qni ajratish.
- ADR da tanlangan patternni qaysi sababga qarshi kiritilgani bilan asoslash.
- Review paytida "bu pattern qanday o'zgarishni arzonlashtiradi" savolini berish va javob bo'lmasa patternni olib tashlash.
- Uchinchi tomon kutubxonasini o'rab, uning almashtirilishini bitta adapter nuqtasiga qamab qo'yish.

**Ehtiyot bo'ling:** Ro'yxatni "hamma sababni oldindan yopish kerak" degan ma'noda o'qish eng qimmat xato: har mustaqil o'q qo'shimcha bilvosita qatlam va narx. O'zgarish ehtimoli bo'lmagan joyda moslashuvchanlik ortiqcha murakkablik va u YAGNI ga zid. Ilova, kutubxona (toolkit) va framework uchun bu narx bir xil emas: ilovada ichki qayta ishlatish va qo'llab-quvvatlash muhim, kutubxona ko'p ilovada ishlashi kerak, framework esa ilova arxitekturasini belgilab beradi va uning interfeysidagi kichik o'zgarish ham barcha foydalanuvchilarga uriladi. Shu sababli moslashuvchanlik byudjeti framework'da eng katta, ichki ilova kodida eng kichik. Pattern taklif qilishning narxi review nuqtasidan ham yozilgan (qarang: [code-review 10-bo'lim](../code-review/10-dizayn-pattern-review-i-yoq-patternni-korish.md#1011-pattern-taklif-qilishning-narxi), Pattern taklif qilishning narxi).

```text
Qayta dizayn sababi -> qarshi turadigan pattern (GoF 1.6, 24-25-bet)

  1. Sinf nomini yozib yaratish    Abstract Factory, Factory Method, Prototype
  2. Aniq amalga bog'liqlik        Chain of Responsibility, Command
  3. Platformaga bog'liqlik        Abstract Factory, Bridge
  4. Ichki tasvirga bog'liqlik     Abstract Factory, Bridge, Memento, Proxy
  5. Algoritmga bog'liqlik         Builder, Iterator, Strategy,
                                   Template Method, Visitor
  6. Qattiq bog'lanish             Abstract Factory, Bridge, Chain of
                                   Responsibility, Command, Facade,
                                   Mediator, Observer
  7. Subclass bilan kengaytirish   Bridge, Chain of Responsibility, Composite,
                                   Decorator, Observer, Strategy
  8. Sinfni o'zgartirib bo'lmaslik Adapter, Decorator, Visitor

Ishlatish tartibi: sababni toping, keyin qatorni o'qing. Teskarisi emas.
```

## 3.25 Patternni tanlash va qo'llash tartibi (How to Select and Use a Design Pattern)

**Tavsif:** Yigirma uchta pattern orasidan to'g'risini topish alohida ko'nikma, va GoF buning uchun oltita kirish yo'lini beradi. Birinchisi - patternlar qanday dizayn muammolarini hal qilishini ko'rib chiqish: obyektlarni topish, granularlik, interfeys spetsifikatsiyasi va qolgan mavzular (qarang: [1-bo'lim](01-yaratuvchi-patternlar.md#120-obyektlarni-topish-va-obyekt-granularligi-finding-appropriate-objects-and-object-granularity), Obyektlarni topish va obyekt granularligi). Ikkinchisi - barcha patternlarning Intent qatorlarini ketma-ket o'qib chiqish va tasnif bilan izlash maydonini qisqartirish (qarang: [1-bo'lim](01-yaratuvchi-patternlar.md#119-katalogni-tashkil-etish-maqsad-va-qamrov-organizing-the-catalog-purpose-and-scope), Katalogni tashkil etish). Uchinchisi - patternlarning o'zaro munosabatlarini o'rganish. To'rtinchisi - bir maqsadli patternlarni birga o'qish, chunki ularning farqi aynan solishtirganda ko'rinadi. Beshinchisi - qayta dizayn sabablaridan kirish. Oltinchisi - teskari savol: nima o'zgarishi mumkinligi emas, nimani qayta dizayn qilmasdan o'zgartirishni xohlaysiz. Pattern tanlangandan keyin uni qo'llash ham tartibli ish. GoF yetti qadam beradi: yozuvni bir o'qib chiqish va ayniqsa Applicability bilan Consequences ga e'tibor berish; Structure, Participants va Collaborations ni o'rganish; kod misolini ko'rish; ishtirokchilarga o'z domeniga mos nom berish, lekin pattern rolini nomda saqlash (`TeXLayoutStrategy` uslubida); sinflarni e'lon qilish va mavjud sinflarga ta'sirni aniqlash; metodlarga ilovaga xos nom berish va nomlash konvensiyasini izchil saqlash; so'ngra mas'uliyat va aloqalarni amalga oshirish.

**Spring'da qayerda uchraydi:** To'rtinchi qadam Spring kodida ochiq ko'rinadi: rol nomda saqlanadi va shu tufayli sinf nima qilishini nomidan bilib olish mumkin - `SimpleAsyncTaskExecutor`, `DelegatingFilterProxy`, `CompositeHealthContributor`, `AbstractRoutingDataSource`, `BeanFactoryPostProcessor`, `TransactionAwareDataSourceProxy`. Oltinchi qadam ham izchil: fabrika metodlari Spring'da `create` prefiksi bilan boshlanadi (`createRequest`, `createBeanFactory`, `createApplicationContext`), kengaytirish nuqtalari `postProcess` bilan. Spring hujjatining har moduli xuddi GoF yozuvi kabi tuzilgan: nima uchun kerak, qachon qo'llanadi, cheklovlari nima.

**Qo'llanish keyslari:**
- Yangi masalada pattern qidirishni "qaysi sababdan qayta dizayn kelishi mumkin" savolidan boshlash, nom ro'yxatini varaqlashdan emas.
- Ikki o'xshash pattern orasida tanlash: ikkisining Consequences qismini yonma-yon qo'yib solishtirish.
- Pattern qo'llashdan oldin uning narxini ADR da yozib, jamoa bilan kelishish.
- Sinf va metod nomlariga pattern rolini kiritish, shunda keyingi o'quvchi niyatni koddan o'qiydi.
- Klassik tuzilishdan chetlashish bo'lsa, farqni javadoc yoki modul README da aniq yozish.

**Ehtiyot bo'ling:** Patternni tanlab emas, ko'rinib qolgani uchun qo'llash eng keng tarqalgan xato. Patternlar moslashuvchanlikni ko'pincha qo'shimcha bilvosita qatlam kiritish bilan oladi, bu esa dizaynni murakkablashtiradi va unumdorlikka ta'sir qiladi; shuning uchun pattern faqat u beradigan moslashuvchanlik haqiqatan kerak bo'lganda qo'llanadi. Baholash paytida eng foydali bo'lim Consequences: foydani emas, narxni o'qing. Yetti qadamni ketma-ketlikdan chiqarib, to'g'ridan-to'g'ri kod misolidan ko'chirib yozish ham tipik xato: Applicability o'qilmagani uchun pattern noto'g'ri kontekstda paydo bo'ladi.

```text
Tanlash: oltita kirish yo'li (GoF 1.7, 28-29-bet)
  1. Patternlar qanday dizayn muammosini hal qiladi
  2. Intent qatorlarini o'qish + tasnif bilan filtrlash
  3. Patternlar munosabatlari grafigini o'rganish
  4. Bir maqsadli patternlarni solishtirish
  5. Qayta dizayn sabablaridan kirish
  6. Nimani o'zgaruvchan qoldirmoqchiligingizdan kirish

Qo'llash: yetti qadam (GoF 1.8, 29 va 31-bet)
  1. Yozuvni bir o'qish (Applicability + Consequences)
  2. Structure, Participants, Collaborations
  3. Kod misoli
  4. Ishtirokchilarga domen nomi, rol nomda qolsin
  5. Sinflarni e'lon qilish, mavjud sinflarga ta'sirni aniqlash
  6. Metodlarga ilovaga xos izchil nom
  7. Mas'uliyat va aloqalarni amalga oshirish
```

## 3.26 Patternlar orasidagi munosabatlar (Pattern Relationships and Related Patterns)

**Tavsif:** Pattern yolg'iz yashamaydi. GoF katalogidagi har yozuvning oxirgi bo'limi "Related Patterns" deb ataladi va u uch xil savolga javob beradi: qaysi patternlar bunga yaqin, ular orasidagi muhim farq nima, va bu pattern qaysi patternlar bilan birga ishlatiladi. Butun katalogni shu bo'limlar bo'yicha bitta grafikka yig'ish ham mumkin va GoF buni alohida rasmda beradi. Munosabatlar bir necha turga bo'linadi. Birga ishlatiladiganlar: Composite ko'pincha Iterator yoki Visitor bilan keladi, Command zanjiri Composite bilan makro-buyruqqa aylanadi, Flyweight bo'lishiladigan obyektlarni Factory orqali tarqatadi. Muqobillar: Prototype ko'pincha Abstract Factory o'rnini bosadi, Strategy sinf qamrovidagi Template Method ning obyekt qamrovidagi javobi, State va Strategy bir xil tuzilishga ega lekin maqsadi boshqa. Tuzilishi o'xshash, maqsadi boshqalar: Composite va Decorator diagrammasi deyarli bir xil, lekin biri butun-qism ierarxiyasi uchun, ikkinchisi mas'uliyat qo'shish uchun; Proxy ham Decorator ga o'xshaydi, ammo u kirishni boshqaradi, xulq qo'shmaydi. Amalda shu farqlarni bilish patternni to'g'ri tanlashdan ko'ra ko'proq foyda beradi: review paytida eng ko'p uchraydigan savol "bu Decorator mi yoki Proxy mi" va javob maqsaddan chiqadi, tuzilishdan emas.

**Spring'da qayerda uchraydi:** Spring'da patternlar deyarli har doim guruhda keladi. `DispatcherServlet` Front Controller bo'lib, `HandlerMapping` strategiyalarini, `HandlerAdapter` adapterlarini va `HandlerInterceptor` zanjirini birga ishlatadi. `SecurityFilterChain` Chain of Responsibility bo'lib, har filtri ichida Strategy (`AuthenticationProvider`, `AuthorizationManager`) ishlaydi. `CacheInterceptor` Proxy ichida Template Method yuritadi va `CacheResolver` strategiyasini chaqiradi. `JdbcTemplate` Template Method va Strategy (`RowMapper`) ni birga beradi. `BeanFactory` Abstract Factory, `@Bean` Factory Method, singleton scope Singleton va `BeanDefinitionRegistry` Registry: to'rttasi bitta mexanizmning qismi.

**Qo'llanish keyslari:**
- Patternni tanlashdan oldin yaqin patternlar bilan solishtirish: Decorator, Proxy va Adapter uchligi eng ko'p aralashtiriladi.
- Mavjud kodga nom berishda maqsadni aniqlab olish: kirishni boshqarsa Proxy, xulq qo'shsa Decorator, interfeysni moslashtirsa Adapter.
- Composite ierarxiyasiga yangi amal qo'shish kerak bo'lganda Visitor ni, elementlarni kezish kerak bo'lganda Iterator ni ulash.
- Bir patterndan ikkinchisiga o'tish yo'lini rejalashtirish: Template Method ierarxiyasini Strategy ga ko'chirish.
- Modul hujjatida ishlatilgan patternlar ro'yxatini va ularning bir-biriga ulanishini yozib qo'yish.

**Ehtiyot bo'ling:** Tuzilish o'xshashligini pattern aynanligi deb o'qish eng ko'p uchraydigan xato: UML diagrammasi bir xil bo'lishi mumkin, lekin niyat boshqa bo'lsa nom ham boshqa bo'ladi va noto'g'ri nom keyingi o'quvchini chalg'itadi. Ikkinchi tuzoq - patternlarni zanjirga ulab, oqimni kuzatib bo'lmaydigan qilish: Proxy ichida Decorator, uning ichida Chain of Responsibility bo'lsa, stack trace o'qilmaydi va xatolik qaysi qatlamdan kelganini aniqlash qiyin. Uchinchisi - munosabatlar grafigini "pattern qancha ko'p bo'lsa shuncha yaxshi" deb tushunish.

```text
Eng ko'p aralashtiriladigan uchlik: maqsad bo'yicha ajratish

  Adapter    interfeysni MOSLASHTIRADI
             mijoz kutgan tur boshqa, asl tur o'zgarmaydi
             -> interfeys boshqa, xulq o'sha

  Decorator  mas'uliyat QO'SHADI
             bir xil interfeys, zanjir bo'lib ketma-ket ulanadi
             -> interfeys o'sha, xulq boshqa

  Proxy      kirishni BOSHQARADI
             bir xil interfeys, lekin kechiktirish, kesh, huquq,
             masofaviy chaqiruv
             -> interfeys o'sha, xulq o'sha, kirish shartli

Savol tartibi: interfeys o'zgardimi? xulq o'zgardimi? kirish
cheklandimi? Uchinchi savolga "ha" bo'lsa, bu Proxy.
```

## 3.27 Kompozit patternlar: patternlardan yasalgan pattern (Compound Patterns)

**Tavsif:** Patternlar birga ishlatilganda ko'pincha barqaror guruh hosil qiladi, va agar o'sha guruh ko'p masalada qayta ishlatilsa, u kompozit pattern (compound pattern) deb ataladi. Ta'rif aniq: bir nechta patternni birga qo'yish o'zi hali kompozit pattern emas, u faqat bitta yechim; kompozit pattern bo'lishi uchun guruh ko'p masalada qo'llanadigan umumiy yechim bo'lishi kerak. Eng mashhur misoli MVC. MVC uch roldan iborat: Model ma'lumot, holat va ilova mantiqini saqlaydi; View modelni foydalanuvchiga ko'rsatadi; Controller kirishni qabul qilib, uni model ustidagi amalga tarjima qiladi. Lekin MVC ni rollar orqali o'rganish qiyin, patternlar orqali esa oson, chunki u uchta patternning birikmasi. Model View va Controller'ni Observer orqali xabardor qiladi: model o'zgarganda obunachilarga xabar beradi va modelning o'zi View yoki Controller'ga bog'liq emas, shuning uchun bitta modelga bir nechta View ulash mumkin. View va Controller esa Strategy munosabatida: Controller View uchun strategiya bo'lib, interfeys xulqini belgilaydi va boshqasiga almashtirilishi mumkin; View faqat tasvir bilan shug'ullanadi. View ning o'z ichida Composite ishlaydi: yuqori darajadagi komponent boshqa komponentlarni, ular yana boshqalarini saqlaydi. MVC yana Factory Method (View uchun standart Controller sinfini belgilash) va Decorator (View ga scroll qo'shish) dan foydalanadi, lekin asosiy uchligi Observer, Composite va Strategy. MVC ning web va Spring'dagi shakli alohida yozilgan (qarang: [6-bo'lim](06-web-va-taqdimot-qatlami-patternlari.md#61-model-korinish-boshqaruvchi-model-view-controller-mvc), Model-Ko'rinish-Boshqaruvchi).

**Spring'da qayerda uchraydi:** Spring'da ham barqaror pattern guruhlari bor va ularni shu nuqtadan ko'rish osonlashtiradi. `DispatcherServlet` atrofidagi guruh: Front Controller + Strategy (`HandlerMapping`, `ViewResolver`) + Adapter (`HandlerAdapter`) + Chain of Responsibility (`HandlerInterceptor`). Spring Modulith'dagi guruh: Observer (`@ApplicationModuleListener`) + Transactional Outbox (`EventPublicationRegistry`) + Retry. Resilience guruhi: Decorator (`@CircuitBreaker` proxy) + Strategy (fallback) + Observer (holat o'zgarishi event'lari). Spring Batch'dagi guruh: Template Method (`Tasklet`, `Step`) + Strategy (`ItemReader`, `ItemProcessor`, `ItemWriter`) + Composite (`CompositeItemWriter`). Har guruh bitta masala turi uchun qayta-qayta ishlatiladi, demak ular kompozit pattern mezoniga javob beradi.

**Qo'llanish keyslari:**
- Yangi modul loyihalashda bitta pattern emas, mos guruhni tanlash: masalan event + outbox + retry uchligi.
- MVC ni o'rgatishda yoki hujjatlashtirishda uni rollar orqali emas, uchta pattern orqali tushuntirish.
- Mavjud tizimdagi barqaror guruhni aniqlab, uni ichki pattern sifatida nomlash va qayta ishlatish.
- Ichki framework qurishda guruhni bitta API ortiga yashirish va foydalanuvchiga faqat kengaytirish nuqtalarini ochish.
- Review paytida guruhning to'liqligini tekshirish: Observer bor, lekin outbox yo'q bo'lsa xabar yo'qolishi mumkin.

**Ehtiyot bo'ling:** Bir nechta patternni bitta yechimda ishlatganda darhol "kompozit pattern yasadim" deb o'ylash xato: u umumiy, ko'p masalada qayta ishlatiladigan bo'lmaguncha oddiy dizayn qarori. Guruhlar narxi qo'shiladi, foydasi esa qo'shilmaydi: to'rt patterndan iborat guruh to'rt barobar moslashuvchanlik bermaydi, lekin to'rt barobar bilvosita qatlam beradi. MVC'da eng tipik buzilish - Controller ichiga biznes mantiq va ma'lumotlarga kirishni joylash: shunda Strategy munosabati yo'qoladi va View model bilan qattiq bog'lanadi. Yana bir buzilish - Model'ni View va Controller'dan xabardor qilish: Observer'ning butun ma'nosi modelning ulardan mustaqil bo'lishida.

```text
MVC uchta patterndan yasalgan (HFDP 12-bob, 526-527-bet)

  Model  --(Observer)-->  View, Controller
         model holati o'zgarsa obunachilarga xabar beradi.
         Model View va Controller'ni bilmaydi.

  View   --(Strategy)-->  Controller
         Controller View uchun strategiya: interfeys xulqini
         belgilaydi va almashtirilishi mumkin.

  View   --(Composite)--> View, View, ...
         ko'rinish komponentlar daraxti: yuqori daraja ichkilarini
         saqlaydi va ularga bir xil munosabatda bo'ladi.

Web'da shakl o'zgaradi (so'rov asosidagi "Model 2"), lekin
uchta munosabat saqlanadi.
```

## 3.28 Har pattern nimani o'zgaruvchan qiladi (What Each Pattern Lets You Vary)

**Tavsif:** Pattern tanlashning eng qisqa yo'li - savolni teskari qo'yish: nima o'zgarishi mumkin deb emas, nimani qayta dizayn qilmasdan o'zgartirishni xohlayman deb so'rash. GoF butun katalogni aynan shu kesimda bitta jadvalga sig'diradi: har pattern yonida u mustaqil o'zgartirishga imkon beradigan aspekt yozilgan. Yaratuvchi patternlar yaratishning turli qirralarini ochadi: Abstract Factory mahsulot obyektlari oilasini, Builder kompozit obyekt qanday qurilishini, Factory Method yaratiladigan obyektning subclass'ini, Prototype yaratiladigan obyektning sinfini, Singleton esa sinfning yagona nusxasini. Strukturaviy patternlar tuzilish va kirishni ochadi: Adapter obyektning interfeysini, Bridge implementatsiyasini, Composite tuzilishi va kompozitsiyasini, Decorator subclass yasamasdan mas'uliyatini, Facade subsystem interfeysini, Flyweight saqlash narxini, Proxy esa obyektga qanday va qayerdan murojaat qilinishini. Xulq-atvor patternlari aloqa va algoritmni ochadi: Chain of Responsibility so'rovni bajaradigan obyektni, Command so'rov qachon va qanday bajarilishini, Interpreter tilning grammatikasi va talqinini, Iterator elementlarga qanday murojaat qilinishi va kezilishini, Mediator kim kim bilan qanday aloqa qilishini, Memento obyektdan tashqarida qanday va qachon yopiq ma'lumot saqlanishini, Observer bog'liq obyektlar soni va ularning qanday yangilanishini, State obyektning holatlarini, Strategy algoritmni, Template Method algoritm qadamlarini, Visitor esa element sinflarini o'zgartirmasdan ularga qo'llanadigan amallarni. Shu jadval "o'zgaruvchan qismni inkapsulyatsiya qilish" printsipining patternlar bo'yicha yoyilgan shakli (qarang: [26-bo'lim](26-dizayn-printsiplari-solid-grasp-va-umumiy.md#2624-ozgaruvchan-qismni-inkapsulyatsiya-qilish-encapsulate-what-varies), O'zgaruvchan qismni inkapsulyatsiya qilish).

**Spring'da qayerda uchraydi:** Spring shu jadvalni konfiguratsiya darajasiga chiqaradi, shuning uchun "nimani o'zgartirmoqchiman" savoliga javob ko'pincha tayyor kengaytirish nuqtasi bo'lib chiqadi. Algoritmni almashtirish kerak bo'lsa `Converter`, `RowMapper`, `AuthorizationManager` yoki `CacheResolver` bean'i; mas'uliyat qo'shish kerak bo'lsa AOP aspekti yoki `BeanPostProcessor`; obyektga kirishni boshqarish kerak bo'lsa `@Cacheable`, `@Transactional`, `LazyConnectionDataSourceProxy`; mahsulot oilasini almashtirish kerak bo'lsa `@Profile` bilan `@Configuration` sinfi; so'rovni kim bajarishini o'zgartirish kerak bo'lsa `SecurityFilterChain` yoki `HandlerInterceptor` tartibi; holatlar to'plamini o'zgartirish kerak bo'lsa Spring Statemachine konfiguratsiyasi.

**Qo'llanish keyslari:**
- Masalani "nimani almashtirmoqchiman" shaklida yozib, shu aspekt bo'yicha patternni topish.
- Review'da taklif qilinayotgan patterndan "bu nimani mustaqil o'zgartirishga imkon beradi" deb so'rash.
- Bir nechta pattern mos kelganda ularning o'zgaruvchan aspektini solishtirib tanlash: Strategy algoritmni, Template Method esa qadamlarni ochadi.
- Kutubxona API'sini loyihalashda ochiladigan aspektlarni ongli sanab chiqish va qolganini yopiq qoldirish.
- Kodda pattern bor, lekin hech narsa o'zgarmayotgan joylarni topib, ortiqcha qatlamni olib tashlash.

**Ehtiyot bo'ling:** Jadvaldan "har aspektni ochib qo'yish kerak" degan xulosa chiqarmang: ochilgan har aspekt bilvosita qatlam, konfiguratsiya va test yuki. Ikkinchi xato - aspektni noto'g'ri tanlash: algoritmning butunini almashtirish kerak bo'lsa Strategy, faqat ayrim qadamlarini almashtirish kerak bo'lsa Template Method, va ikkisini aralashtirish keraksiz ierarxiya beradi. Uchinchisi - o'zgaruvchan aspekt deklaratsiya darajasida qolib, amalda bitta implementatsiya bilan yashashi: interfeysning bitta implementatsiyasi yillar davomida o'zgarmasa, u abstraksiya emas, ortiqcha fayl.

```text
"Nimani o'zgartirmoqchiman" -> pattern (GoF Table 1.2, 30-bet)

  mahsulot obyektlari oilasi        Abstract Factory
  kompozit obyekt qanday qurilishi  Builder
  yaratiladigan obyekt subclass'i   Factory Method
  yaratiladigan obyekt sinfi        Prototype
  sinfning yagona nusxasi           Singleton
  obyekt interfeysi                 Adapter
  obyekt implementatsiyasi          Bridge
  obyekt tuzilishi va kompozitsiyasi Composite
  mas'uliyat (subclass yasamasdan)  Decorator
  subsystem interfeysi              Facade
  obyektlarni saqlash narxi         Flyweight
  obyektga kirish va joylashuvi     Proxy
  so'rovni bajaradigan obyekt       Chain of Responsibility
  so'rov qachon va qanday bajariladi Command
  grammatika va talqin              Interpreter
  elementlarga murojaat va kezish   Iterator
  kim kim bilan qanday aloqa qiladi Mediator
  tashqarida saqlanadigan yopiq holat Memento
  bog'liq obyektlar soni va yangilanishi Observer
  obyekt holatlari                  State
  algoritm                          Strategy
  algoritm qadamlari                Template Method
  sinfni o'zgartirmasdan qo'shiladigan amal Visitor
```

## 3.29 Amalda qo'llash

- [ ] `switch` yoki `if/else if` zanjiri bilan algoritm tanlaydigan metodlarni toping va har birini Strategy yoki `Map<Enum, Handler>` registriga o'tkazish rejasini yozing.
- [ ] Domen holatini `String` yoki `int` bilan saqlaydigan maydonlarni `enum` ga o'tkazing va ruxsat etilgan o'tishlarni aniq ro'yxat qilib yozing.
- [ ] `ApplicationEventPublisher` chaqiruvlarini sanab chiqing va har biri tranzaksiya ichida yoki tashqarisida bo'lishi kerakligini qaror qiling.
- [ ] `null` qaytaradigan public metodlarni toping va `Optional`, bo'sh kolleksiya yoki Null Object ga o'tkazing.
- [ ] Takrorlanadigan so'rov shartlarini (`findByStatusAndTypeAndDate...`) Specification ga chiqarish rejasini tuzing.
- [ ] Resursni ochib-yopadigan takrorlanuvchi `try` bloklarini qidirib, Execute Around yoki `Template` sinfiga ajratish nomzodlarini belgilang.
- [ ] Zanjir shaklidagi ishlov (validatsiya, boyitish, transformatsiya) joylarini toping va ularni aniq nomli bosqichlarga ajratilgan Pipeline qilib yozing.
- [ ] Har bir Observer yoki listener uchun savolga javob yozing: u sinxronmi, xato bersa chaqiruvchi nima qiladi.

## Manbalar

- Freeman/Robson, *Head First Design Patterns* 2nd, 1-bob - Strategy va o'zgaruvchan qismni inkapsulyatsiya qilish
- Freeman/Robson, *Head First Design Patterns* 2nd, 2-bob - Observer
- Freeman/Robson, *Head First Design Patterns* 2nd, 6-bob - Command
- Freeman/Robson, *Head First Design Patterns* 2nd, 8-bob - Template Method
- Freeman/Robson, *Head First Design Patterns* 2nd, 9-bob - Iterator
- Freeman/Robson, *Head First Design Patterns* 2nd, 10-bob - State va uning Strategy dan farqi
- Freeman/Robson, *Head First Design Patterns* 2nd, 14-bob - qolgan patternlar: Bridge, Chain of Responsibility, Flyweight, Interpreter, Mediator, Memento, Prototype, Visitor
- [Spring Framework, Spring Expression Language (SpEL)](https://raw.githubusercontent.com/spring-projects/spring-framework/v7.0.0/spring-expression/src/main/java/org/springframework/expression/spel/support/SimpleEvaluationContext.java) - ishonchsiz ifoda uchun cheklangan kontekst
- [Java API, `Iterator`](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/Iterator.html) - iteratsiya vaqtida o'zgartirishda `ConcurrentModificationException`
- [JEP 441: Pattern Matching for switch](https://openjdk.org/jeps/441) - `sealed` ierarxiya ustida to'liqlik tekshiruvi
- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns: Elements of Reusable Object-Oriented Software*, Addison-Wesley, 1995, 1.6-bo'lim (23-25-bet) - qayta dizaynni majburlaydigan sakkizta sabab va har sababga qarshi turadigan patternlar ro'yxati
- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns*, Addison-Wesley, 1995, 1.6-bo'lim (25-28-bet) - ilova, kutubxona (toolkit) va framework uchun moslashuvchanlik narxining farqi
- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns*, Addison-Wesley, 1995, 1.7-bo'lim (28-29-bet) - patternni tanlashning oltita kirish yo'li
- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns*, Addison-Wesley, 1995, 1.8-bo'lim (29 va 31-bet) - patternni qo'llashning yetti qadami va patternni tanlab ishlatish ogohlantirishi
- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns*, Addison-Wesley, 1995, Table 1.2 (30-bet) - har pattern mustaqil o'zgartirishga imkon beradigan aspekt
- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns*, Addison-Wesley, 1995, 1.5-bo'lim va Figure 1.1 (10 va 12-bet) - patternlar birga ishlatilishi, muqobilligi va o'xshash tuzilishi; `Related Patterns` bo'limlari asosidagi munosabatlar grafigi
- Freeman/Robson, *Head First Design Patterns* 2nd, 12-bob (494-bet) - compound pattern ta'rifi: bir nechta patternni ko'p masalada qayta ishlatiladigan umumiy yechimga birlashtirish
- Freeman/Robson, *Head First Design Patterns* 2nd, 12-bob (526-527-bet) - MVC compound pattern sifatida: Observer, Strategy va Composite munosabatlari
- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns*, Addison-Wesley, 1995, 1.2-bo'lim (4-6-bet) - MVC ichidagi Observer, Composite va Strategy, hamda Factory Method bilan Decorator ning qo'shimcha roli
- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns*, Addison-Wesley, 1995, Chain of Responsibility, Implementation (226-228-bet) - zanjirni mavjud havolalar ustida qurish, baza handler'ning shartsiz uzatuvchi default i va so'rovni ifodalashning uch yo'li
- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns*, Addison-Wesley, 1995, Command, Implementation (238-239-bet) - buyruq aqlliligi spektri, undo uchun saqlanadigan uch narsa, tarix ro'yxati, nusxalash talabi va xato to'planishiga qarshi Memento
- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns*, Addison-Wesley, 1995, Interpreter, Applicability va Implementation (245 va 247-248-bet) - unumdorlik sharti, parsing patternga kirmasligi, amalni Visitor'ga chiqarish va terminal simvollarni Flyweight bilan bo'lishish
- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns*, Addison-Wesley, 1995, Iterator, Implementation (260-261 va 263-bet) - obxod algoritmini kim belgilashi, kursor shakli va kompozit ustidagi iteratorning uch varianti
- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns*, Addison-Wesley, 1995, Mediator, Implementation (277-bet) - abstrakt Mediator qachon kerak emasligi va kolleague bilan vositachi orasidagi muloqotning ikki shakli
- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns*, Addison-Wesley, 1995, Mediator, Related Patterns (282-bet) - Facade bir yo'nalishli, Mediator ko'p yo'nalishli protokol beradi
- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns*, Addison-Wesley, 1995, Memento, Consequences (286-287-bet) - Originator'ni soddalashtirishi va caretaker'ning yashirin xotira narxi
- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns*, Addison-Wesley, 1995, Observer, Consequences va Implementation (295 va 297-bet) - abstrakt bog'lanish qatlamlashni saqlashi va bir nechta subject kuzatilganda `update` ga subject uzatilishi
- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns*, Addison-Wesley, 1995, State, Consequences va Implementation (307 va 309-bet) - o'tishlarning atomarligi, maydonsiz State obyektlarini bo'lishish va holat obyektlarini oldindan yaratish yoki talabga ko'ra yaratish
- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns*, Addison-Wesley, 1995, State, Implementation (308-bet) - o'tish mezonini Context yoki State sinfining o'zi belgilashi
- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns*, Addison-Wesley, 1995, Strategy, Implementation va Consequences (318-320-bet) - Strategy va Context orasidagi ma'lumot almashinuvining ikki yo'li va umumiy interfeysdan kelib chiqadigan ortiqcha parametr narxi
- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns*, Addison-Wesley, 1995, Template Method, Implementation (326-328 va 330-bet) - hook va abstrakt amalni ajratib hujjatlashtirish, primitiv amallar sonini minimallashtirish, nomlash konventsiyasi va `super` ni chaqirishni esdan chiqarish muammosi
- Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides, *Design Patterns*, Addison-Wesley, 1995, Visitor, Consequences va Implementation (336-337 va 339-340-bet) - umumiy ota turi bo'lmagan sinflarni aylanish, holat to'plash, inkapsulyatsiyani buzish narxi va obxod mas'uliyatining uch varianti
- ESLATMA: kitoblarda yo'q, korpus qo'shgan qism - so'rov obyekti uchun `sealed` va pattern matching javobi; buyruqni immutable `record` qilish nusxalash talabini yo'q qilishi; `Iterator` va `Spliterator`/`Stream` ni GoF ning ikki variantiga xaritalash; vositachilikning `ApplicationEventPublisher` ko'rinishi; Spring Batch `ExecutionContext` hajmi caretaker mas'uliyatiga misol sifatida; hodisa payloadida manbani olib yurish; maydonsiz holat uchun `enum` va singleton bean; Strategy ga tor ko'rinish (`record`) uzatish; hook metod uchun Javadoc talabi; visitor ustunligining `sealed` bilan yo'qolishi

---

[&larr; 2. Strukturaviy patternlar](02-strukturaviy-patternlar.md) · [Mundarija](README.md) · [4. Concurrency patternlari &rarr;](04-concurrency-patternlari.md)
