<!-- doc: patterns | chapter: 26 | part:  -->

[Java Spring arxitektori bilishi kerak bo'lgan barcha dizayn patternlar](../../README.md) / [Dizayn patternlar](README.md)

# 26. Dizayn printsiplari: SOLID, GRASP va umumiy qoidalar (Design Principles: SOLID, GRASP & General Rules)

<details>
<summary>Bu bo'limdagi 30 bo'lim</summary>

- [26.1 Yagona javobgarlik printsipi (Single Responsibility Principle)](#261-yagona-javobgarlik-printsipi-single-responsibility-principle)
- [26.2 Ochiq/yopiq printsipi (Open/Closed Principle)](#262-ochiqyopiq-printsipi-openclosed-principle)
- [26.3 Liskov almashtirish printsipi (Liskov Substitution Principle)](#263-liskov-almashtirish-printsipi-liskov-substitution-principle)
- [26.4 Interfeys ajratish printsipi (Interface Segregation Principle)](#264-interfeys-ajratish-printsipi-interface-segregation-principle)
- [26.5 Bog'liqliklarni teskari aylantirish printsipi (Dependency Inversion Principle)](#265-bogliqliklarni-teskari-aylantirish-printsipi-dependency-inversion-principle)
- [26.6 Ma'lumot egasi (Information Expert (GRASP))](#266-malumot-egasi-information-expert-grasp)
- [26.7 Yaratuvchi (Creator (GRASP))](#267-yaratuvchi-creator-grasp)
- [26.8 Boshqaruvchi (Controller (GRASP))](#268-boshqaruvchi-controller-grasp)
- [26.9 Past bog'liqlik (Low Coupling (GRASP))](#269-past-bogliqlik-low-coupling-grasp)
- [26.10 Yuqori kogeziya (High Cohesion (GRASP))](#2610-yuqori-kogeziya-high-cohesion-grasp)
- [26.11 Polimorfizm (Polymorphism)](#2611-polimorfizm-polymorphism)
- [26.12 Sof Fabrikatsiya (Pure Fabrication)](#2612-sof-fabrikatsiya-pure-fabrication)
- [26.13 Vositachilik (Indirection)](#2613-vositachilik-indirection)
- [26.14 Himoyalangan O'zgarishlar (Protected Variations)](#2614-himoyalangan-ozgarishlar-protected-variations)
- [26.15 Demeter Qonuni (Law of Demeter)](#2615-demeter-qonuni-law-of-demeter)
- [26.16 Aytib Qo'y, So'ramay (Tell Don't Ask)](#2616-aytib-qoy-soramay-tell-dont-ask)
- [26.17 Vorislikdan Ustun Kompozitsiya (Composition over Inheritance)](#2617-vorislikdan-ustun-kompozitsiya-composition-over-inheritance)
- [26.18 Mas'uliyatlarni Ajratish (Separation of Concerns)](#2618-masuliyatlarni-ajratish-separation-of-concerns)
- [26.19 O'zini Takrorlamaslik (Don't Repeat Yourself (DRY))](#2619-ozini-takrorlamaslik-dont-repeat-yourself-dry)
- [26.20 Oddiy Tut (Keep It Simple (KISS))](#2620-oddiy-tut-keep-it-simple-kiss)
- [26.21 Kerak Bo'lmaydi Printsipi (You Aren't Gonna Need It (YAGNI))](#2621-kerak-bolmaydi-printsipi-you-arent-gonna-need-it-yagni)
- [26.22 Eng Kam Hayratlanish Printsipi (Principle of Least Astonishment)](#2622-eng-kam-hayratlanish-printsipi-principle-of-least-astonishment)
- [26.23 Buyruq-So'rov Ajratilishi (Command-Query Separation)](#2623-buyruq-sorov-ajratilishi-command-query-separation)
- [26.24 O'zgaruvchan Qismni Inkapsulyatsiya Qilish (Encapsulate What Varies)](#2624-ozgaruvchan-qismni-inkapsulyatsiya-qilish-encapsulate-what-varies)
- [26.25 Interfeysga Qarab Programmalash (Program to an Interface)](#2625-interfeysga-qarab-programmalash-program-to-an-interface)
- [26.26 Gollivud Printsipi (Hollywood Principle (Inversion of Control))](#2626-gollivud-printsipi-hollywood-principle-inversion-of-control)
- [26.27 Mustahkamlik Printsipi (Robustness Principle (Postel's Law))](#2627-mustahkamlik-printsipi-robustness-principle-postels-law)
- [26.28 Yagona Abstraksiya Darajasi (Single Level of Abstraction)](#2628-yagona-abstraksiya-darajasi-single-level-of-abstraction)
- [26.29 Barqaror Bog'liqliklar va Barqaror Abstraksiyalar (Stable Dependencies & Stable Abstractions)](#2629-barqaror-bogliqliklar-va-barqaror-abstraksiyalar-stable-dependencies--stable-abstractions)
- [26.30 Amalda qo'llash](#2630-amalda-qollash)

</details>



Dizayn printsiplari - bu aniq sinf tuzilmasi beruvchi pattern emas, balki pattern tanlashda qaror mezoni bo'lib xizmat qiladigan qoidalar to'plami. SOLID javobgarlikni taqsimlash va abstraksiya chegaralarini belgilashga, GRASP (General Responsibility Assignment Software Patterns) esa "bu mas'uliyatni qaysi obyektga bersam?" degan kundalik savolga javob beradi. Arxitektor uchun bu printsiplar kod review'da, modul chegaralarini chizishda va texnik qarz hisobini yuritishda umumiy til vazifasini bajaradi: Strategy, Adapter yoki Outbox kabi patternlarning aksariyati aslida shu printsiplarning amaliy ko'rinishidir. Spring Framework 6.x / Spring Boot 3.x arxitekturasining o'zi ham - stereotype annotatsiyalar, interfeysga asoslangan injection, auto-configuration'ning `@ConditionalOnMissingBean` mexanizmi - bu qoidalarning freymvork darajasidagi tatbiqidir.

## 26.1 Yagona javobgarlik printsipi (Single Responsibility Principle)

**Tavsif:** Har bir sinf yoki modul faqat bitta o'zgarish sababiga ega bo'lishi kerak - uni faqat bitta manfaatdor tomonning talabi o'zgarganda tahrirlash lozim. Amalda bu biznes qoidalarini, ma'lumotlarga kirishni, transport qatlamini (HTTP, messaging) va konfiguratsiyani alohida sinslarga ajratishni bildiradi. Natijada unit test yozish osonlashadi, regressiya radiusi qisqaradi va bir faylga tegadigan jamoalar soni kamayadi. Printsip "sinf kichik bo'lsin" degani emas - "sinfning auditoriyasi bitta bo'lsin" degani.

**Spring'da qayerda uchraydi:** Spring stereotype annotatsiyalari shu bo'linishni to'g'ridan-to'g'ri qo'llab-quvvatlaydi: `@RestController` faqat HTTP kontrakti va validatsiyani, `@Service` use case orkestratsiyasini, `@Repository` persistence'ni, `@ConfigurationProperties` esa faqat konfiguratsiya binding va validatsiyasini olib boradi. Spring Batch 5.x'da bitta step ataylab uchta interfeysga ajratilgan - `ItemReader`, `ItemProcessor`, `ItemWriter`; Spring Boot 3.x auto-configuration ham texnologiya bo'yicha mayda `@AutoConfiguration` sinflariga bo'lingan (`DataSourceAutoConfiguration`, `JacksonAutoConfiguration`, `TaskExecutionAutoConfiguration`). Cross-cutting mas'uliyatlar sinfdan tashqariga chiqariladi: logging va metrikalar `@Aspect` yoki `io.micrometer.observation.ObservationHandler` ichiga, xato formatlash `@ControllerAdvice` va `ProblemDetail`ga, header manipulyatsiyasi `HandlerInterceptor` yoki `WebFilter`ga.

**Qo'llanish keyslari:**
- 2000 qatorli `OrderService`ni `OrderPricingService`, `OrderValidator` va `OrderRepository`ga ajratib, narx qoidasi o'zgarganda faqat bitta sinfga tegish.
- DTO va JPA `@Entity`ni ajratish: REST kontrakti o'zgarishi ma'lumotlar bazasi sxemasini o'zgartirishga majbur qilmasligi uchun.
- Hisobot generatsiyasini (PDF/Excel) biznes xizmatdan ajratib, Spring Batch step'iga ko'chirish.
- Audit yozuvini `@EntityListeners(AuditingEntityListener.class)` va `@EnableJpaAuditing` orqali domain kodidan chiqarib tashlash.
- Konfiguratsiya kalitlarini `@ConfigurationProperties(prefix = "billing")` record'iga yig'ib, `@Value` ni o'nlab sinf bo'ylab tarqatmaslik.

**Ehtiyot bo'ling:** Printsipni haddan ortiq qo'llash "anemic" sinflar okeanini keltiradi - har biri bitta metodli 50 ta sinf orasida biznes mantiqni kuzatish qiyinlashadi. Javobgarlikni texnik qatlam emas, o'zgarish sababi bo'yicha o'lchang: bir use case'ning ikki qismi doim birga o'zgarsa, ularni ajratish kogeziyani buzadi.

## 26.2 Ochiq/yopiq printsipi (Open/Closed Principle)

**Tavsif:** Modul kengaytirish uchun ochiq, lekin modifikatsiya uchun yopiq bo'lishi kerak: yangi xulq-atvorni mavjud, sinovdan o'tgan kodga tegmasdan qo'shish mumkin bo'lsin. Buning odatiy yo'li - o'zgaruvchan qismni abstraksiya (interfeys, strategiya, hook) ortiga olib, yangi variantni yangi sinf sifatida registratsiya qilish. Bu `if/else` va `switch` zanjirlarining cheksiz o'sishini to'xtatadi va binar moslik (binary compatibility) saqlanishiga yordam beradi.

**Spring'da qayerda uchraydi:** Freymvorkning deyarli butun extension modeli shu printsipga asoslangan: `BeanPostProcessor` va `BeanFactoryPostProcessor` konteyner xulqini o'zgartirmasdan kengaytiradi, `WebMvcConfigurer` va `HttpMessageConverter` registratsiyasi MVC pipeline'ini, `SecurityFilterChain` bean'lari (Spring Security 6.x, `HttpSecurity` lambda DSL) esa xavfsizlik qoidalarini kengaytiradi. Spring Boot auto-configuration'da `@ConditionalOnMissingBean` tufayli siz o'z bean'ingizni e'lon qilib default'ni almashtirasiz - starter kodini o'zgartirish kerak emas. Spring AI 1.x'da `ChatClient.builder(chatModel)` ga `MessageChatMemoryAdvisor`, `QuestionAnswerAdvisor` kabi Advisor'larni qo'shish ham shu model; Spring Data'da esa `@Query` yoki custom fragment interfeys bilan repository'ni kengaytirasiz.

**Qo'llanish keyslari:**
- To'lov provayderlari: `PaymentProvider` interfeysini yaratib, yangi provayder uchun faqat yangi `@Component` qo'shish va `Map<String, PaymentProvider>` injection bilan tanlash.
- Chegirma qoidalari: har bir aksiya alohida `DiscountRule` bean'i, `List<DiscountRule>` sifatida `@Order` bilan tartiblanib injekt qilinadi.
- Xato javoblarini `@ControllerAdvice` ichida kengaytirish - controller'lar kodiga tegmasdan yangi exception turini qo'shish.
- Spring Boot starter'dagi default `ObjectMapper`ni o'z `Jackson2ObjectMapperBuilderCustomizer` bean'ingiz bilan sozlash.
- Spring AI'da RAG kontekstini qo'shish uchun yangi Advisor registratsiyasi, prompt yuborish kodini o'zgartirmasdan.

**Ehtiyot bo'ling:** Har bir ehtimoliy o'zgarish uchun oldindan abstraksiya qurish - bu speculative generality: ishlatilmaydigan interfeyslar va plugin nuqtalari kodni o'qishni qiyinlashtiradi. Ikkinchi real variant paydo bo'lgandan keyin abstraksiya kiritish (rule of three) ko'pincha to'g'riroq qaror.

## 26.3 Liskov almashtirish printsipi (Liskov Substitution Principle)

**Tavsif:** Bazaviy tur ishlatilgan har qanday joyda uning subtipi, chaqiruvchi kod uchun ko'rinadigan farq bo'lmasdan, almashtirilishi mumkin bo'lishi kerak. Bu nafaqat signatura mosligi, balki kontrakt mosligini talab qiladi: subtip precondition'larni kuchaytirmasligi, postcondition'larni zaiflashtirmasligi va invariantlarni buzmasligi lozim. Buzilish odatda kutilmagan `UnsupportedOperationException`, yashirin `null` qaytarish yoki yangi checked exception shaklida namoyon bo'ladi.

**Spring'da qayerda uchraydi:** Spring'da ko'p narsa interfeys orqali injekt qilinadi, shuning uchun LSP amaliy ahamiyatga ega: `PlatformTransactionManager` o'rniga `JpaTransactionManager`, `DataSourceTransactionManager` yoki `JtaTransactionManager` qo'yilganda `@Transactional` semantikasi saqlanadi; `CacheManager` o'rniga `CaffeineCacheManager`, `RedisCacheManager` yoki test uchun `NoOpCacheManager` almashtiriladi. Spring Data ierarxiyasi (`CrudRepository` → `PagingAndSortingRepository` → `JpaRepository`) ham shu asosda ishlaydi, lekin e'tibor bering: `JpaRepository.save()` merge semantikasi bilan, `MongoRepository.save()` esa boshqa tranzaksion kafolatlar bilan ishlaydi - ya'ni store'ni almashtirish har doim shaffof emas. Klassik buzilish misoli - `Collections.unmodifiableList()` qaytargan `List` yoki `Arrays.asList()` natijasiga `add()` chaqirilganda `UnsupportedOperationException` olish; Java 17+ `sealed` interfeyslar esa ruxsat etilgan subtiplar to'plamini kompilyatsiya vaqtida cheklab, kontraktni nazorat qilishga yordam beradi.

**Qo'llanish keyslari:**
- Test muhitida real `JavaMailSender` o'rniga fake implementatsiya qo'yish va biznes kod o'zgarmasligiga ishonch hosil qilish.
- `@Primary` bilan default implementatsiyani almashtirganda integratsion testlar hali ham o'tishini talab qilish.
- Hexagonal arxitekturada bitta port uchun ikkita adapter (REST va Kafka) yozib, ularning xato kontraktini bir xil qilish.
- Read-only replika uchun `DataSource` almashtirganda yozish operatsiyalarini chaqirmaslik - aks holda kontrakt buziladi.
- Domain ierarxiyasini `sealed interface` + `record` bilan modellab, `switch` pattern matching orqali barcha holatlarni to'liq qamrab olish.

**Ehtiyot bo'ling:** Eng ko'p uchraydigan tuzoq - meros orqali kodni qayta ishlatish uchun mos kelmaydigan ierarxiya qurish (`Square extends Rectangle` klassikasi); bunda kompozitsiya yoki delegatsiya xavfsizroq. Subtipda metodni `UnsupportedOperationException` bilan "o'chirish" interfeys juda keng ekanining belgisi - bu ISP muammosiga ishora qiladi.

## 26.4 Interfeys ajratish printsipi (Interface Segregation Principle)

**Tavsif:** Mijoz o'ziga kerak bo'lmagan metodlarga bog'lanishga majbur bo'lmasligi kerak - bitta "yirik" interfeys o'rniga bir nechta tor, rolga mo'ljallangan interfeys yaxshiroq. Bu mock yozishni soddalashtiradi, kompilyatsiya bog'liqliklarini kamaytiradi va implementatsiyalarda bo'sh (stub) metodlar paydo bo'lishini oldini oladi. Tor interfeyslar, qo'shimcha sifatida, LSP buzilishlarini ham kamaytiradi.

**Spring'da qayerda uchraydi:** Spring lifecycle callback'lari ataylab mayda interfeyslarga bo'lingan: `InitializingBean`, `DisposableBean`, `BeanNameAware`, `ApplicationContextAware`, `SmartLifecycle` - bean faqat kerakligini implement qiladi. Spring Data'da `Repository` bo'sh marker interfeys, ustiga `CrudRepository`, `ListCrudRepository` (Spring Data 3.0+, `List` qaytaradi), `PagingAndSortingRepository` va custom fragment interfeyslar tanlab qo'yiladi - ya'ni siz faqat kerakli operatsiyalarni e'lon qilasiz. Spring MVC'da `WebMvcConfigurerAdapter` Java 8 `default` metodlari paydo bo'lgandan keyin deprecate qilinib, `WebMvcConfigurer` ning o'ziga o'tilgan; Spring Security 6.x'da esa `WebSecurityConfigurerAdapter` olib tashlanib, komponent bo'yicha bean'lar (`SecurityFilterChain`, `UserDetailsService`, `PasswordEncoder`) qoldirilgan.

**Qo'llanish keyslari:**
- Repository'ni `OrderReader` va `OrderWriter` interfeyslariga ajratib, CQRS'da read modeliga faqat o'qish portini berish.
- Spring Data'da `JpaRepository` o'rniga faqat `findById` va `save` e'lon qilgan tor interfeys yozib, tasodifiy `deleteAll()` chaqiruvini imkonsiz qilish.
- Katta `NotificationService` o'rniga `EmailSender`, `SmsSender`, `PushSender` portlarini ajratish.
- Testlarda tor port uchun bir necha qatorli fake yozib, Mockito'siz ishlash.
- Modul chegaralarida faqat kerakli metodlarni ko'rsatuvchi "client-owned" interfeys e'lon qilish (interface segregation by consumer).

**Ehtiyot bo'ling:** Har bir metod uchun alohida interfeys yaratish navigatsiyani buzadi va "interface explosion" ga olib keladi - interfeysni rol bo'yicha, ya'ni mijoz guruhi bo'yicha ajratish kerak. Shuningdek, tor interfeyslarni keyinroq birlashtirish qiyin, shuning uchun public API'da ularni e'lon qilishdan oldin iste'molchi senariylarini aniqlang.

## 26.5 Bog'liqliklarni teskari aylantirish printsipi (Dependency Inversion Principle)

**Tavsif:** Yuqori darajali biznes mantiq quyi darajali detallarga emas, ikkisi ham abstraksiyaga bog'lanishi kerak; abstraksiya esa detalga emas, detal abstraksiyaga bog'liq bo'lsin. Amalda domain qatlami port interfeyslarini o'zi e'lon qiladi, infratuzilma esa ularni implement qiladi va bog'lanish yo'nalishi "ichkariga" qaratiladi. Bu ma'lumotlar bazasi, broker yoki tashqi API ni almashtirishni lokal o'zgarishga aylantiradi.

**Spring'da qayerda uchraydi:** Spring IoC konteyneri (`ApplicationContext`) shu printsipni ishga soladi: konstruktor injection orqali bean interfeys tipida olinadi, konkret implementatsiyani esa konteyner `@Component`, `@Bean`, `@Qualifier`, `@Primary` va `@Profile` asosida tanlaydi. Ixtiyoriy yoki ko'p implementatsiyali holatlar uchun `ObjectProvider<T>` va `List<T>`/`Map<String, T>` injection ishlatiladi; `@ConditionalOnMissingBean` esa Spring Boot 3.x starter'larida default detalni almashtirish imkonini beradi. Spring Boot'ning `JavaMailSender`, `MessageSource`, `TaskExecutor`, `RestClient` (Spring Framework 6.1+) kabi abstraksiyalari ham xuddi shu maqsadda - ilova kodi SMTP yoki HTTP kutubxonasi detallarini bilmaydi.

```java
// domain (port) - infratuzilmaga bog'liqlik yo'q
public interface OrderNotifier { void orderShipped(OrderId id); }

@Service
class ShipOrderUseCase {
    private final OrderNotifier notifier;           // abstraksiyaga bog'liq
    ShipOrderUseCase(OrderNotifier notifier) { this.notifier = notifier; }
}

@Component // infratuzilma (adapter) - portga bog'liq, teskari emas
class KafkaOrderNotifier implements OrderNotifier { /* ... */ }
```

**Qo'llanish keyslari:**
- Hexagonal/Clean arxitekturada `domain` moduli `spring-context`dan boshqa hech narsaga (hatto JPA'ga ham) bog'lanmasligini ta'minlash.
- Tashqi kredit-skoring API ni `CreditScorePort` ortiga olib, testlarda WireMock yoki in-memory fake bilan almashtirish.
- Monolitdan ajratishda bitta portni saqlab, implementatsiyani lokal bean'dan HTTP adapter'ga ko'chirish.
- `@Profile("test")` bilan e-mail yuboruvchi adapterni log'ga yozuvchi versiyaga almashtirish.
- Legacy `JdbcTemplate` kodini asta-sekin `JpaOrderRepository`ga o'tkazish - biznes qatlamiga tegmasdan.

**Ehtiyot bo'ling:** Faqat bitta implementatsiyasi bo'lgan va hech qachon almashmaydigan har bir sinf uchun interfeys yaratish - bu sun'iy indirection, kodni o'qishni qiyinlashtiradi va foyda bermaydi. Shuningdek, port interfeysiga infratuzilma tiplari (`ResultSet`, `KafkaRecord`, JPA `Entity`) sizib kirsa, teskari aylantirish faqat nominal bo'lib qoladi.

## 26.6 Ma'lumot egasi (Information Expert (GRASP))

**Tavsif:** Mas'uliyatni uni bajarish uchun kerakli ma'lumotga ega bo'lgan obyektga bering. Bu qoida hisob-kitob va qaror qabul qilishni ma'lumot bilan bir joyda saqlab, obyektlar orasidagi getter orqali "ma'lumot so'rab yurish" (feature envy) holatini yo'q qiladi. Natijada kogeziya oshadi, bog'liqlik kamayadi va domain mantiq bitta joyda testlanadi.

**Spring'da qayerda uchraydi:** Bu birinchi navbatda domain modellashtirish qoidasi: JPA `@Entity` yoki `@Embeddable` value object ichida xulq-atvor saqlanadi (masalan `Order.addLine()`, `Money.add()`), `@Service` esa faqat tranzaksiya va orkestratsiyani boshqaradi. Spring Data `org.springframework.data.domain.AbstractAggregateRoot` sinfi, `@DomainEvents` va `@AfterDomainEventPublication` annotatsiyalari bilan birgalikda, aggregate'ning o'zi hodisa chiqarishi uchun to'g'ridan-to'g'ri qo'llab-quvvatlash beradi. Ma'lumotning "egasi" ma'lumotlar bazasi bo'lgan holatlarda (agregat hisob-kitoblar, katta hajmli filtrlar) mas'uliyat repository'ga va `@Query` / projection'larga o'tadi - bu ham shu printsipning amaliy ko'rinishi.

```java
@Entity
class Order extends AbstractAggregateRoot<Order> {
    @Embedded private Money total;
    void ship() {                      // qaror - ma'lumot egasida
        if (total.isZero()) throw new IllegalStateException("bo'sh buyurtma");
        this.status = SHIPPED;
        registerEvent(new OrderShipped(id));   // hodisa aggregate ichida
    }
}
```

**Qo'llanish keyslari:**
- Buyurtma summasini `OrderService` ichida emas, `Order.total()` metodida hisoblash.
- Status o'tishlari qoidasini (`NEW → PAID → SHIPPED`) aggregate ichida saqlab, `setStatus()` setter'ini olib tashlash.
- Pul va valyuta mantiqini `Money` record/value object ichiga joylashtirib, dumaloqlash xatolarini bir joyda boshqarish.
- Hisobot uchun 10 million qatorni ilovaga tortmasdan, repository'da `@Query` yoki native SQL agregatidan foydalanish.
- `AbstractAggregateRoot` + `@TransactionalEventListener` bilan "buyurtma yuborildi" hodisasini aggregate o'zi e'lon qilishi.

**Ehtiyot bo'ling:** Printsipni ko'r-ko'rona qo'llash aggregate'ni "god object" ga aylantiradi - tashqi tizim, narx jadvali yoki boshqa aggregate ma'lumoti kerak bo'lsa, mas'uliyatni domain service'ga berish to'g'riroq. Lazy loading'ga tayangan entity ichida murakkab hisob-kitob yozish esa `LazyInitializationException` va N+1 so'rovlarga olib keladi.

## 26.7 Yaratuvchi (Creator (GRASP))

**Tavsif:** B obyektini yaratish mas'uliyatini B ni o'zida saqlaydigan, B dan foydalanadigan yoki uni inisializatsiya qilish uchun ma'lumotga ega bo'lgan A obyektiga bering. Bu "kim kimni yaratadi" savoliga javob berib, bog'liqlik grafigini tabiiy va bir yo'nalishli qiladi. Yaratish mantiqi bir joyda bo'lgani uchun invariantlar obyekt tug'ilishida darhol tekshiriladi va yarim-inisializatsiya qilingan holat paydo bo'lmaydi.

**Spring'da qayerda uchraydi:** Konteyner darajasida yaratuvchi - `BeanFactory`/`ApplicationContext`: `@Configuration` ichidagi `@Bean` metodlari aniq factory metod rolini bajaradi, murakkab holatlar uchun `FactoryBean<T>` va `@Lookup` yoki `ObjectProvider.getObject()` (prototype scope uchun) ishlatiladi. Kutubxona API'larida builder shaklidagi creator keng tarqalgan: `RestClient.builder()`, `WebClient.builder()`, `RestTemplateBuilder`, `JobBuilder`/`StepBuilder` (Spring Batch 5.x) va `ChatClient.builder(chatModel)` (Spring AI 1.x). Domain darajasida esa aggregate root o'z child'larini yaratadi (`order.addLine(...)`), yoki static factory metod (`Order.place(...)`) orqali tug'iladi - Spring bunga xalaqit bermaydi, chunki domain obyektlari bean emas.

**Qo'llanish keyslari:**
- `Order` aggregate'i `OrderLine` obyektlarini `addLine()` ichida yaratib, `List<OrderLine>` ni tashqaridan to'ldirishni taqiqlash.
- Murakkab tashqi klientni `@Bean` metodida `RestClient.builder()` bilan qurib, timeout va interceptor'larni bir joyda belgilash.
- Request-scoped yoki prototype bean'ni singleton ichidan `ObjectProvider` yoki `@Lookup` orqali olish.
- Static factory (`Money.of("UZS", 1000)`) bilan validatsiyani konstruktorga ko'tarish va noto'g'ri valyutani konstruksiya vaqtida rad etish.
- Test ma'lumotlarini Object Mother / Test Data Builder sinflarida yaratib, testlar bo'ylab takrorlanishni kamaytirish.

**Ehtiyot bo'ling:** Hamma narsani Spring bean'iga aylantirish tuzoqqa olib keladi - qisqa umrli domain obyektlari (`Order`, `Money`) `new` yoki factory metod bilan yaratilishi kerak, aks holda ularga holat yoziladigan singleton paydo bo'lib, thread-safety buziladi. Builder'ni har bir mayda DTO uchun yozish esa foydasiz boilerplate; Java `record` ko'pincha yetarli.

## 26.8 Boshqaruvchi (Controller (GRASP))

**Tavsif:** Tizimga tushadigan har bir hodisa (HTTP so'rov, xabar, timer) uchun uni qabul qilib, keyingi ishni delegatsiya qiladigan birinchi obyektni aniqlang. Controller biznes mantiqni o'zi bajarmaydi - u faqat kirishni tarjima qiladi, tranzaksiya chegarasini belgilaydigan use case xizmatini chaqiradi va natijani protokol formatiga o'giradi. Shu tufayli bitta biznes senariy bir nechta transport orqali (REST, Kafka, CLI) ishlatilishi mumkin.

**Spring'da qayerda uchraydi:** Spring MVC'da `DispatcherServlet` front controller rolini bajaradi, undan keyin `@RestController`/`@Controller` metodlari use case controller bo'ladi; WebFlux'da `@Controller` yoki funksional `RouterFunction` ishlatiladi. Boshqa transportlar uchun ekvivalentlar mavjud: `@KafkaListener` (Spring for Apache Kafka), `@RabbitListener`, `@JmsListener`, `@MessageMapping` (STOMP/RSocket), `@SqsListener` (Spring Cloud AWS), `@Scheduled` va `@EventListener`. Haqiqiy use case esa odatda `@Service` + `@Transactional` sinfida yashaydi; umumiy xato ishlovi `@ControllerAdvice` va `ProblemDetail` (RFC 9457, Spring Framework 6.x) orqali markazlashtiriladi.

**Qo'llanish keyslari:**
- `@RestController` ni ingichka saqlab, barcha mantiqni `PlaceOrderUseCase` sinfiga ko'chirish va shu use case'ni `@KafkaListener` dan ham qayta ishlatish.
- Tranzaksiya chegarasini controller'da emas, application service'da `@Transactional` bilan belgilash.
- `@Valid` va DTO validatsiyasini controller qatlamida qoldirib, domain'ni HTTP detallaridan tozalash.
- Idempotentlik kalitini (`Idempotency-Key` header) controller'da o'qib, use case'ga oddiy parametr sifatida uzatish.
- CLI yoki admin vazifalari uchun `@ShellComponent` (Spring Shell) yoki `ApplicationRunner` ni xuddi shu use case ustiga qo'yish.

**Ehtiyot bo'ling:** "Fat controller" - biznes qoidalari, SQL va tashqi chaqiruvlar controller ichida to'planishi eng keng tarqalgan anti-pattern; u testlarni sekinlashtiradi va mantiqni qayta ishlatishni imkonsiz qiladi. Teskari chekka holat ham bor: butun ilova uchun bitta "umumiy" controller/facade yaratish kogeziyani buzadi - har bir use case guruhi uchun alohida kirish nuqtasi yaxshiroq.

## 26.9 Past bog'liqlik (Low Coupling (GRASP))

**Tavsif:** Modullar orasidagi bog'liqlik sonini va kuchini minimal darajada ushlang, shunda bitta joydagi o'zgarish boshqalarga tarqalmaydi. Bog'liqlikni kamaytirish usullari - interfeys/port orqali muloqot, hodisalar bilan aloqani asinxronlashtirish, umumiy ma'lumotlar bazasi jadvallarini bo'lishmaslik va paket chegaralarini majburlash. Bu deployability va mustaqil jamoa ishini ta'minlaydigan asosiy mezon.

**Spring'da qayerda uchraydi:** `ApplicationEventPublisher` bilan `@EventListener` / `@TransactionalEventListener` modul ichida sinflarni, Spring Cloud Stream yoki Kafka esa xizmatlar orasini bo'shashtirib bog'laydi. Spring Modulith 1.x (`spring-modulith-core`) paket darajasidagi modullarni `ApplicationModules.of(App.class).verify()` testi bilan nazorat qiladi, `@ApplicationModuleListener` esa modullar orasidagi tranzaksion hodisalarni, `spring-modulith-events-jpa` bilan birga, event publication registry orqali ishonchli yetkazadi (Outbox'ga yaqin mexanizm). Qo'shimcha vositalar: `@ConfigurationProperties` konfiguratsiyani markazlashtiradi, ArchUnit testlari esa "domain paketi infratuzilmaga import qilmasin" qoidasini CI'da majburlaydi.

**Qo'llanish keyslari:**
- `OrderService` to'g'ridan-to'g'ri `InvoiceService`ni chaqirish o'rniga `OrderPlaced` hodisasini e'lon qilishi.
- Spring Modulith `verify()` testini CI'ga qo'shib, modullar orasidagi ruxsatsiz bog'liqlikni build'da to'xtatish.
- Har bir modulga o'z sxemasini berib, boshqa modul jadvalini to'g'ridan-to'g'ri `JOIN` qilishni taqiqlash.
- Tashqi API bilan ishlashni bitta adapter paketiga yopib, DTO'larni domain'ga sizdirmaslik.
- Monolitdan microservice ajratishdan oldin modul chegaralarini hodisalar bilan bo'shashtirib, keyin jismoniy ajratish.

**Ehtiyot bo'ling:** Bog'liqlikni kamaytirish uchun hamma joyda hodisa ishlatish kuzatuvchanlikni yo'qotadi - chaqiruv zanjirini kuzatish qiyinlashadi va `@EventListener` ichidagi xatolar jim qoladi (`@TransactionalEventListener(phase = AFTER_COMMIT)` da tranzaksiya allaqachon commit bo'lgan). Shuningdek, bo'shashgan bog'liqlik "eventual consistency" ni keltiradi: biznes buni qabul qila olishini oldindan tasdiqlang.

## 26.10 Yuqori kogeziya (High Cohesion (GRASP))

**Tavsif:** Bitta modul ichidagi elementlar bir maqsadga xizmat qilishi va birga o'zgarishi kerak; o'zaro bog'liq mantiq tarqalib ketmasligi lozim. Yuqori kogeziya past bog'liqlikning tabiiy natijasidir: tegishli hamma narsa bir joyda bo'lsa, modullar orasidagi muloqot kamayadi. Bu kodni o'qish, nomlash va mas'uliyatni jamoalar bo'yicha taqsimlashni osonlashtiradi.

**Spring'da qayerda uchraydi:** Spring hech qanday paket tuzilmasini majburlamaydi, shuning uchun bu arxitektor qarori: `com.acme.order` ichida controller, service, repository va domain'ni birga saqlash (package-by-feature) `com.acme.controller`/`com.acme.service` (package-by-layer) dan ko'ra kogeziyali bo'ladi. Spring Modulith shu yondashuvni rasmiylashtiradi - har bir top-level paket modul, uning `internal` quyi paketlari esa tashqaridan yopiq hisoblanadi; Spring Boot starter'lari ham xuddi shu printsip bilan texnologiya bo'yicha guruhlangan. Konfiguratsiyada kogeziya `@ConfigurationProperties(prefix = "...")` record'lari va `@Configuration` sinflarini funksiya bo'yicha ajratish bilan ta'minlanadi.

**Qo'llanish keyslari:**
- Loyihani `order`, `billing`, `shipping` modullariga bo'lib, har birida o'z controller/service/repository to'plamini saqlash.
- Modul ichki sinflarini `internal` paketga yashirib, faqat port interfeyslarini public qilish.
- Konfiguratsiya kalitlarini bitta `BillingProperties` record'ida guruhlab, 20 ta tarqoq `@Value` ni yo'q qilish.
- 30 metodli `UtilService` yoki `CommonService` ni mavzular bo'yicha bo'lib tashlash.
- Microservice chegarasini texnik qatlam emas, bounded context bo'yicha belgilash, shunda bitta talab bitta xizmatda bajariladi.

**Ehtiyot bo'ling:** Kogeziyani faqat "nomi o'xshash sinflarni bir paketga yig'ish" deb tushunish xato - `util`, `common`, `helper` paketlari odatda past kogeziyaning belgisidir va vaqt o'tib hamma narsaga bog'lanadi. Ikkinchi tomondan, modullarni haddan tashqari mayda bo'lish ham zarar: bitta oddiy talab uchun besh modulni o'zgartirish kerak bo'lsa, chegaralar noto'g'ri chizilgan.

## 26.11 Polimorfizm (Polymorphism)

**Tavsif:** GRASP'ning bu printsipi aytadi: turga qarab xatti-harakat o'zgarishi kerak bo'lsa, `if/else` yoki `switch` shoxlari o'rniga mas'uliyatni polimorf operatsiyalarga taqsimla. Har bir variant o'z sinfida umumiy interfeysni amalga oshiradi, chaqiruvchi esa faqat abstraksiyaga bog'lanadi. Natijada yangi variant qo'shish mavjud kodni o'zgartirishni talab qilmaydi - bu Open/Closed printsipining amaliy ko'rinishi. Shartli mantiq yo'qolmaydi, balki bitta joyga (factory yoki registry'ga) ko'chadi.

**Spring'da qayerda uchraydi:** Spring Framework'ning o'zi polimorfizm ustiga qurilgan: `org.springframework.core.convert.converter.Converter<S,T>`, `HandlerMethodArgumentResolver`, `HttpMessageConverter`, `AuthenticationProvider`, `HealthIndicator` - barchasi strategiya interfeyslari va Spring ularning barcha implementatsiyalarini `List<T>` yoki `Map<String, T>` sifatida inject qiladi. Java 17+ da `sealed interface` va `record` bilan variantlar to'plamini yopib, `switch` pattern matching bilan ekspresivlik olish mumkin - lekin yangi variantlar tez-tez qo'shilsa, baribir interfeys + `@Component` ro'yxati afzal. `@Qualifier`, `@Primary` va `ObjectProvider<T>` to'g'ri implementatsiyani tanlashga yordam beradi; `Ordered`/`@Order` esa chain tartibini belgilaydi.

```java
public interface PaymentHandler {
    boolean supports(PaymentType type);
    Receipt pay(PaymentRequest req);
}

@Service
class PaymentRouter {
    private final List<PaymentHandler> handlers;
    PaymentRouter(List<PaymentHandler> handlers) { this.handlers = handlers; }

    Receipt route(PaymentRequest req) {
        return handlers.stream().filter(h -> h.supports(req.type())).findFirst()
            .orElseThrow(() -> new UnsupportedPaymentException(req.type()))
            .pay(req);
    }
}
```

**Qo'llanish keyslari:**
- To'lov turlari (karta, bank o'tkazmasi, wallet) uchun alohida `PaymentHandler` implementatsiyalari va router bean.
- Hujjat formatlari (PDF, XLSX, CSV) eksporti uchun `DocumentExporter` interfeysi va format bo'yicha `Map<String, DocumentExporter>`.
- Multi-tenant narx hisoblash: har bir tarif rejasi uchun o'z `PricingStrategy` bean'i.
- Spring Security'da LDAP, DB va OAuth2 uchun bir nechta `AuthenticationProvider` ro'yxatda ishlaydi.
- Notification kanallari (email, SMS, push) uchun bitta `NotificationSender` abstraksiyasi.

**Ehtiyot bo'ling:** Ikki-uch variantli va o'zgarmaydigan shart uchun to'liq sinflar ierarxiyasini qurish ortiqcha murakkablik - bunday holda oddiy `switch` o'qilishi oson. Shuningdek implementatsiyalar bir-biridan juda farq qilsa, umumiy interfeys "quyi umumiy bo'luvchi"ga aylanib, har bir metod uchun `UnsupportedOperationException` tashlanadigan holatga olib keladi.

## 26.12 Sof Fabrikatsiya (Pure Fabrication)

**Tavsif:** Domen modelida tabiiy egasi yo'q mas'uliyat paydo bo'lganda (persistence, mapping, transaction boundary, tashqi tizim bilan aloqa), uni sun'iy, domenda mavjud bo'lmagan sinfga beramiz. Bu domen obyektlarini infratuzilma tashvishlaridan tozalaydi va past coupling bilan yuqori cohesion'ni saqlaydi. "Sof" degani - bu sinf real dunyo tushunchasi emas, balki toza dizayn uchun o'ylab topilgan konstruksiya.

**Spring'da qayerda uchraydi:** `@Repository` bilan belgilangan Spring Data interfeyslari (`JpaRepository`, `CrudRepository`) klassik Pure Fabrication: `Order` entity o'zini saqlashni bilmaydi, `OrderRepository` biladi. Shunga o'xshash `@Service` qatlamidagi application service'lar, MapStruct yoki qo'lda yozilgan mapper sinflari, `JdbcClient` (Spring Framework 6.1+) va `RestClient` wrapper'lari, Spring Batch'dagi `ItemReader`/`ItemWriter`, `@Component` sifatidagi `EventPublisherAdapter` - barchasi shu printsip mahsuli. DDD atamalarida bu Repository, Factory va Domain Service naqshlariga to'g'ri keladi.

**Qo'llanish keyslari:**
- `OrderRepository` yaratish, shunda `Order` aggregate'i JPA yoki JDBC haqida hech narsa bilmaydi.
- `OrderMapper` sinfi entity va DTO orasida konvertatsiya qiladi, domen obyektiga `toDto()` metodini qo'shmaslik uchun.
- `PricingCalculator` domen service'i bir nechta aggregate ustida hisob-kitob qiladi, chunki mas'uliyat bitta entity'ga sig'maydi.
- `IdempotencyKeyStore` komponenti takroriy so'rovlarni kuzatadi - bu biznes tushunchasi emas, texnik ehtiyoj.
- `OutboxPublisher` scheduled bean domen eventlarini broker'ga uzatadi.

**Ehtiyot bo'ling:** Har bir mas'uliyat uchun yangi `...Manager`, `...Helper`, `...Util` sinfi yaratish anemik domen modeliga olib keladi - biznes qoidalari entity'larda emas, prosedural service'larda tarqalib ketadi. Fabrikatsiyani faqat domenga tegishli bo'lmagan mas'uliyatlar uchun ishlatinglar; qoida obyektning o'z holatiga tegishli bo'lsa, u entity ichida qolishi kerak.

## 26.13 Vositachilik (Indirection)

**Tavsif:** Ikki komponent o'rtasidagi to'g'ridan-to'g'ri bog'liqlikni oraliq obyekt orqali almashtirib, ularni bir-biridan ajratish. Vositachi coupling'ni kamaytiradi, o'zgarishlarni bir joyda ushlab turadi va qayta ishlatishni osonlashtiradi. Bu Protected Variations'ni amalga oshirishning asosiy mexanizmi va Adapter, Facade, Mediator, Proxy naqshlarining umumiy ildizi.

**Spring'da qayerda uchraydi:** Spring'ning butun arxitekturasi vositachilikka tayanadi: `ApplicationContext` bean'lar orasidagi bog'liqlikni boshqaradi, `@Transactional` va `@Cacheable` CGLIB/JDK proxy orqali ishlaydi (`AbstractAutoProxyCreator`), `ApplicationEventPublisher` publisher va listener'ni bir-biridan ajratadi. `DispatcherServlet` HTTP so'rov bilan controller o'rtasidagi vositachi; `PlatformTransactionManager` kod bilan tranzaksiya API orasidagi vositachi; `Environment` va `@ConfigurationProperties` kod bilan konfiguratsiya manbasi orasidagi vositachi. Hexagonal arxitekturada port interfeyslari (`PaymentGateway`) adapter implementatsiyalari (`StripePaymentGateway`) uchun indirection nuqtasi bo'ladi.

**Qo'llanish keyslari:**
- Tashqi REST API uchun `PaymentGateway` port interfeysi, shunda provayderni almashtirish bitta adapter'ni o'zgartirish bilan tugaydi.
- `@Transactional` proxy orqali biznes kodini `EntityManager` tranzaksiya API'sidan ajratish.
- Modullar orasida `ApplicationEventPublisher` ishlatish (Spring Modulith `@ApplicationModuleListener`) - modullar bir-birini import qilmaydi.
- `@ConfigurationProperties` record'i orqali kodni `application.yml` kalitlari nomlaridan izolyatsiya qilish.
- Legacy SOAP tizimini yangi domenga `LegacyCustomerAdapter` orqali ulash.

**Ehtiyot bo'ling:** Har bir qatlam uchun ortiqcha vositachi qo'shish "lasagna arxitekturasi" - stack trace o'qilmaydi, debug qiyinlashadi, lekin hech qanday real moslashuvchanlik olinmaydi. Vositachini faqat real o'zgarish ehtimoli yoki testlash ehtiyoji bo'lganda qo'sh; bir implementatsiyali interfeys, hech qachon almashmaydigan bo'lsa, faqat shovqin.

## 26.14 Himoyalangan O'zgarishlar (Protected Variations)

**Tavsif:** Tizimdagi o'zgarishi mumkin bo'lgan yoki beqaror nuqtalarni aniqlab, ular atrofida barqaror interfeys qo'yish va qolgan kodni shu interfeysga bog'lash. Shunda o'zgarish sodir bo'lganda ta'sir faqat bitta adapter yoki implementatsiya bilan cheklanadi. Bu GRASP printsiplarining eng umumiysi - Information Hiding, Open/Closed va Dependency Inversion shuning turli ko'rinishlari.

**Spring'da qayerda uchraydi:** Spring'ning abstraksiya qatlamlari aniq shu maqsadda yozilgan: `PlatformTransactionManager` JTA, JDBC va JPA tranzaksiya farqlarini yashiradi; `CacheManager` Redis, Caffeine va Hazelcast orasidagi farqni; `Resource` fayl tizimi, classpath va S3 farqini; `DataAccessException` ierarxiyasi vendor-spetsifik `SQLException` kodlarini barqaror istisnolarga tarjima qiladi (`SQLExceptionTranslator`). `spring-cloud-config`, `@Profile`, `Environment` abstraksiyasi muhit o'zgarishlaridan himoya qiladi; Spring AI 1.x'dagi `ChatModel` va `EmbeddingModel` interfeyslari esa model provayderini (OpenAI, Anthropic, Azure, Bedrock) almashtirishni bir bog'liqlik va bir nechta property o'zgarishiga qisqartiradi.

**Qo'llanish keyslari:**
- Barcha tashqi integratsiyalarni port interfeyslari ortiga yashirib, provayder almashganda domen kodini tegmaslik.
- Spring AI `ChatClient` ishlatib, LLM provayderini almashtirish imkonini saqlab qolish.
- `CacheManager` abstraksiyasi orqali local Caffeine'dan Redis'ga o'tish, service kodini o'zgartirmasdan.
- Public REST API'ni DTO'lar bilan versiyalash, shunda ichki entity sxemasi o'zgarishi mijozlarni buzmaydi.
- `DataAccessException` ishlatib, PostgreSQL'dan boshqa bazaga migratsiya paytida exception handling'ni saqlab qolish.

**Ehtiyot bo'ling:** Hamma narsani "kelajakda o'zgaradi" deb abstraktlash spekulyativ umumlashtirish bo'lib, murakkablikni haqiqiy foyda bermasdan oshiradi. Faqat tasdiqlangan yoki yuqori ehtimolli o'zgarish nuqtalarini himoya qil - qolganini YAGNI tamoyili bo'yicha kerak bo'lganda refactoring qilish arzonroq.

## 26.15 Demeter Qonuni (Law of Demeter)

**Tavsif:** "Faqat eng yaqin do'stlaring bilan gaplash" - obyekt metodi faqat o'zining maydonlari, parametrlari, o'zi yaratgan obyektlar va o'zining metodlari bilan ishlashi kerak. `order.getCustomer().getAddress().getCity().getName()` ko'rinishidagi zanjirlar chaqiruvchini butun obyekt grafigi tuzilishiga bog'laydi, natijada har qanday oraliq o'zgarish uzoqdagi kodni buzadi. Printsip coupling'ni kamaytiradi va ma'lumot egasiga mas'uliyatni qaytaradi.

**Spring'da qayerda uchraydi:** JPA entity'larida bu printsip ayniqsa muhim: uzun getter zanjirlari `LazyInitializationException` va N+1 select muammolarini keltiradi, chunki har bir qadam yangi proxy'ni initsializatsiya qiladi. Yechim - Spring Data'ning projection interfeyslari yoki `record` DTO'lari bilan `@Query` konstruktor ifodalari, shuningdek `EntityGraph` orqali kerakli grafikni oldindan yuklash. Spring'ning `Environment.getProperty()` va `@ConfigurationProperties` record'lari ham tuzilmani yashiradi. Statik tahlilda PMD'ning `LawOfDemeter` qoidasi va Checkstyle buzilishlarni ko'rsatadi, ArchUnit testlari esa qatlamlar orasidagi noto'g'ri navigatsiyani bloklaydi.

**Qo'llanish keyslari:**
- `order.getCustomer().getAddress().getCity()` o'rniga `order.shippingCity()` metodini aggregate ichiga qo'shish.
- Spring Data projection interfeysi bilan controller'ga faqat kerakli maydonlarni qaytarish, entity grafigini ochmasdan.
- `Customer` ichida `isEligibleForDiscount()` metodi, service'da `customer.getLoyalty().getTier().getLevel() > 3` tekshiruvi o'rniga.
- Test kodida chuqur mock zanjirlari (`RETURNS_DEEP_STUBS`) o'rniga aggregate metodini mock qilish.
- ArchUnit qoidasi: controller qatlami repository yoki entity ichki tuzilmasiga to'g'ridan-to'g'ri murojaat qilmasligini majburlash.

**Ehtiyot bo'ling:** Printsipni so'zma-so'z qo'llash har bir qatlam uchun delegatsiya metodlarini ko'paytirib, "wrapper" shovqinini yaratadi - ayniqsa Builder, Stream va fluent API'larda (`RestClient.get().uri(...).retrieve()`) zanjir mutlaqo normal, chunki har bir qadam bir xil obyekt turini qaytaradi. Qoida ma'lumot tuzilmasi bo'ylab navigatsiyaga tegishli, fluent interfeyslarga emas.

## 26.16 Aytib Qo'y, So'ramay (Tell Don't Ask)

**Tavsif:** Obyektdan holatini so'rab olib, tashqarida qaror qabul qilish o'rniga, obyektga nima qilish kerakligini aytish va qarorni u o'z ichida qabul qilishiga ruxsat berish. Bu invariantlarni obyekt ichida ushlab turadi, ma'lumot va xatti-harakatni birga saqlaydi hamda anemik modelni oldini oladi. Natijada biznes qoidalari service'larda tarqalib ketmaydi, balki aggregate ichida bitta joyda yashaydi.

**Spring'da qayerda uchraydi:** Spring'ning o'zi bu printsipni tashqi API'larida ko'rsatadi: `TransactionTemplate.execute(callback)` yoki `JdbcClient.sql(...).query(...)` ichida nazoratni o'zida ushlaydi, holatini tashqariga bermaydi. Domen qatlamida DDD uslubidagi aggregate'lar - `order.cancel(reason)`, `account.withdraw(amount)` - `@Entity` ichida biznes metodlari sifatida yoziladi, setter'lar esa `protected` qilinadi. Spring Data JPA bunga qarshilik qilmaydi: entity'da `@Version` optimistic lock, `AbstractAggregateRoot.registerEvent()` (Spring Data Commons) orqali domen eventlarini e'lon qilish va `@DomainEvents`/`@AfterDomainEventPublication` bilan ularni `save()` vaqtida chiqarish mumkin.

**Qo'llanish keyslari:**
- `if (order.getStatus() == NEW) order.setStatus(CANCELLED)` o'rniga `order.cancel(reason)` metodini chaqirish.
- Balans tekshiruvini `Account.withdraw()` ichiga ko'chirib, `InsufficientFundsException`ni o'sha joyda tashlash.
- `AbstractAggregateRoot` orqali `OrderCancelled` eventini aggregate ichida ro'yxatga olish.
- Validatsiya qoidalarini konstruktorda yoki factory metodda bajarib, yaroqsiz obyekt yaratilishini imkonsiz qilish.
- `Optional.map/ifPresent` ishlatish, `isPresent()` + `get()` juftligi o'rniga.

**Ehtiyot bo'ling:** Har bir so'rov (query) uchun ham printsipni majburlash xato - reporting, DTO mapping va serializatsiya uchun getter'lar zarur, CQRS'da read model aniq "ask" uslubida ishlaydi. Shuningdek bir nechta aggregate ustidagi koordinatsiya qoidalari bitta entity'ga sig'maydi; ularni domen service'ga chiqarish to'g'riroq.

## 26.17 Vorislikdan Ustun Kompozitsiya (Composition over Inheritance)

**Tavsif:** Xatti-harakatni qayta ishlatish uchun sinfni kengaytirish o'rniga, kerakli funksionallikni ta'minlovchi obyektni ichiga joylab, unga delegatsiya qilish. Voris chuqur ierarxiyada ota-sinfning implementatsiya detallariga qattiq bog'lanadi (fragile base class muammosi) va Java'da faqat bitta sinfdan voris olish mumkin. Kompozitsiya esa bog'liqlikni runtime'da almashtirishga, testda mock qo'yishga va bir nechta xatti-harakatni erkin birlashtirishga imkon beradi.

**Spring'da qayerda uchraydi:** Spring Boot 3.x/4.x konfiguratsiyasida idiomatik yo'l - `@Component` bean'larni konstruktor orqali inject qilish, abstract bazoviy service'lardan voris olish emas. `RestClient`, `WebClient`, `JdbcClient` barchasi builder + interceptor kompozitsiyasiga qurilgan; Spring Security 6.x'dagi `SecurityFilterChain` filtrlar kompozitsiyasi; `HandlerInterceptor` va `@Aspect` AOP esa vorislik ishlatmasdan xatti-harakat qo'shadi. Java 17+ `record` sinflari voris olishni mutlaqo taqiqlaydi, shuning uchun DTO va value object'lar faqat kompozitsiya orqali tuziladi; `sealed interface` esa kengaytirishni boshqarilgan tarzda ochadi. `default` metodli interfeyslar bilan mixin uslubida qayta ishlatish ham vorislikka alternativa bo'ladi.

**Qo'llanish keyslari:**
- `AbstractBaseService` dan voris olish o'rniga `AuditLogger` va `MetricsRecorder` bean'larini inject qilish.
- Retry, circuit breaker va timeout'ni Resilience4j dekoratorlari sifatida qatlamma-qatlam qo'shish.
- `RestClient.Builder` ga `ClientHttpRequestInterceptor` qo'shib, auth header'ni barcha chaqiruvlarga ulash.
- Validatsiya qoidalarini `List<OrderValidator>` sifatida inject qilib, yangi qoidani yangi bean bilan qo'shish.
- Testda real bog'liqlik o'rniga fake implementatsiya berish, `@SpyBean` yoki protected metodlarni override qilmasdan.

**Ehtiyot bo'ling:** Kompozitsiya ham ortiqcha ishlatilsa, ko'p mayda bean va uzun konstruktorlarga olib keladi - konstruktorda 6-7 dan ortiq parametr paydo bo'lsa, bu sinf juda ko'p mas'uliyatni olgan degan signal. Vorislik haqiqiy "is-a" munosabati va barqaror, hujjatlashtirilgan kengaytirish nuqtalari bo'lganda (masalan Spring'ning `OncePerRequestFilter`) hamon to'g'ri tanlov.

## 26.18 Mas'uliyatlarni Ajratish (Separation of Concerns)

**Tavsif:** Tizimni har biri bitta aniq tashvish bilan shug'ullanadigan qismlarga ajratish: biznes mantiqi, persistence, transport, xavfsizlik, kuzatuv, konfiguratsiya. Har bir qism alohida tushuniladi, alohida testlanadi va alohida o'zgaradi, shuning uchun bir sohadagi o'zgarish boshqalarini buzmaydi. Bu Single Responsibility Principle'ning tizim darajasidagi ko'rinishi va qatlamli, hexagonal hamda modulli monolit arxitekturalarining asosi.

**Spring'da qayerda uchraydi:** Spring'ning stereotip annotatsiyalari aynan shu ajratishni ifodalaydi: `@RestController` transport, `@Service` biznes mantiqi, `@Repository` ma'lumotlarga kirish, `@Configuration` esa tashqi bog'lanish uchun. Cross-cutting concern'lar deklarativ tarzda ajratiladi - `@Transactional`, `@Cacheable`, `@PreAuthorize`, `@Observed` (Micrometer Observation API, Spring Boot 3.x), `@ControllerAdvice` bilan markazlashgan xato ishlash. Spring Modulith 1.x `@ApplicationModule` va `ApplicationModules.verify()` orqali modullar orasidagi chegaralarni build vaqtida majburlaydi; ArchUnit testlari qatlam qoidalarini tekshiradi; `@ConfigurationProperties` konfiguratsiyani kod mantiqidan ajratadi.

**Qo'llanish keyslari:**
- Controller'da faqat DTO validatsiyasi va mapping, barcha biznes qoidalari service yoki domen qatlamida.
- `@ControllerAdvice` bilan `ProblemDetail` (RFC 9457) javoblarini markazlashtirib, har bir controller'dagi try/catch'ni olib tashlash.
- Spring Modulith bilan `order`, `billing`, `shipping` modullarini ajratib, `verify()` testi bilan noto'g'ri import'ni bloklash.
- Audit va metrikalarni `@Aspect` yoki `ObservationHandler` orqali qo'shib, biznes metodlarini toza saqlash.
- Domen qatlamini JPA annotatsiyalaridan xoli tutib, persistence modelini alohida adapter paketda saqlash.

**Ehtiyot bo'ling:** Ajratishni ortiqcha qilish - har bir CRUD operatsiya uchun entity, DTO, mapper, port, adapter yaratish - kichik servislarda sof boilerplate'ga aylanadi. Chegaralarni biznes imkoniyatlari bo'yicha chiz, texnik qatlamlar bo'yicha emas: anemik `UserService` + `UserRepository` + `UserMapper` uchligi mas'uliyat ajratilgandek ko'rinsa ham, aslida bitta tashvish uch faylga bo'linganidan boshqa narsa emas.

## 26.19 O'zini Takrorlamaslik (Don't Repeat Yourself (DRY))

**Tavsif:** Har bir bilim yoki qaror tizimda bitta aniq, vakolatli joyda ifodalanishi kerak. Takrorlangan mantiq o'zgarish paytida bir joyda tuzatilib, boshqasida qolib ketishi mumkin - bu xatolarning klassik manbai. DRY kod satrlarini emas, balki *bilimni* takrorlamaslik haqida: bir xil ko'rinadigan, lekin turli sabablarga ko'ra o'zgaradigan ikki blok takrorlanish emas.

**Spring'da qayerda uchraydi:** Spring Boot'ning butun falsafasi DRY: `@SpringBootApplication` va auto-configuration (`spring.factories` o'rnini olgan `AutoConfiguration.imports`) takroriy bean deklaratsiyalarini yo'qotadi; Spring Data derived query metodlari (`findByStatusAndCreatedAtAfter`) boilerplate DAO kodini olib tashlaydi; `@ControllerAdvice` xato ishlashni markazlashtiradi; `@Aspect` va `@Around` advice cross-cutting takrorlanishni kesadi. Konfiguratsiyada parent POM va `dependencyManagement` (yoki Spring Boot BOM) versiyalarni bitta joyda saqlaydi; `@ConfigurationProperties` record'i esa property kalitlarini kod bo'ylab takrorlamaslikka yordam beradi. Testlarda `@TestConfiguration` va Testcontainers uchun umumiy abstract bazoviy sinf takroriy setup'ni kamaytiradi.

**Qo'llanish keyslari:**
- Validatsiya qoidalarini `@Valid` + maxsus `ConstraintValidator` sifatida yozib, har bir controller'da qayta yozmaslik.
- Umumiy `@Transactional(readOnly = true)` sozlamalarini `@Service` darajasida bir marta e'lon qilish.
- Mikroservislar orasida umumiy DTO va client kodini OpenAPI generator orqali yaratish, qo'lda ko'chirmasdan.
- `spring-boot-starter-parent` yoki BOM import bilan kutubxona versiyalarini bitta joyda boshqarish.
- Testcontainers konfiguratsiyasini `@ServiceConnection` bilan bitta abstract integration-test bazoviy sinfiga chiqarish.

**Ehtiyot bo'ling:** DRY'ni ko'r-ko'rona qo'llash eng xavfli natija - mikroservislar orasida umumiy "shared-kernel" kutubxonasi yaratish ularni qattiq bog'lab, mustaqil deploy afzalligini yo'q qiladi. Tasodifiy o'xshashlikni (coincidental duplication) birlashtirishdan ko'ra, uchinchi marta takrorlanishni kutish (Rule of Three) ko'pincha arzonroq.

## 26.20 Oddiy Tut (Keep It Simple (KISS))

**Tavsif:** Eng sodda, ishlaydigan yechimni tanlash va murakkablikni faqat o'lchanadigan ehtiyoj paydo bo'lganda qo'shish. Murakkablik to'g'ridan-to'g'ri xarajat: ko'proq kod, ko'proq xato, uzoqroq onboarding, sekinroq o'zgarish. KISS YAGNI bilan birga ishlaydi - kelajakda kerak bo'lishi mumkin degan taxmin asosida abstraksiya qurmaslik.

**Spring'da qayerda uchraydi:** Spring Boot 3.x/4.x ko'p hollarda eng sodda yo'lni taklif qiladi: `JdbcClient` yoki Spring Data JDBC murakkab JPA mapping o'rniga; `@ConfigurationProperties` record'i murakkab konfiguratsiya sinflari o'rniga; `RestClient` (Spring Framework 6.1+) oddiy bloklovchi chaqiruvlar uchun reaktiv `WebClient` o'rniga; modulli monolit (Spring Modulith) mikroservislardan oldingi qadam sifatida. Java 17-25 xususiyatlari - `record`, `sealed`, pattern matching, virtual threads (`spring.threads.virtual.enabled=true`) - murakkab reaktiv zanjirlarsiz yuqori concurrency berishi mumkin, bu esa stack'ni sezilarli soddalashtiradi.

**Qo'llanish keyslari:**
- Yangi loyihani modulli monolit sifatida boshlab, haqiqiy masshtab ehtiyoji paydo bo'lganda modulni ajratish.
- Yuqori concurrency uchun virtual thread'larni yoqib, butun kodni reaktiv stack'ga ko'chirmaslik.
- Oddiy hisobotlar uchun `JdbcClient` bilan to'g'ridan-to'g'ri SQL yozish, JPA criteria API o'rniga.
- Bitta implementatsiyali interfeyslarni olib tashlab, konkret sinfni to'g'ridan-to'g'ri inject qilish.
- Oddiy kalit-qiymat kesh uchun `@Cacheable` + Caffeine ishlatish, distributed cache infratuzilmasini qurmasdan.

**Ehtiyot bo'ling:** KISS "o'ylamay yozish" degani emas - xavfsizlik, idempotentlik, tranzaksiya chegaralari va xato ishlashni "sodda" deb tashlab ketish keyinroq ancha qimmatga tushadi. Shuningdek haqiqatan murakkab domen uchun sun'iy soddalashtirish (hamma narsani bitta katta service'ga yig'ish) soddalik emas, balki murakkablikni ko'rinmas joyga surish.

## 26.21 Kerak Bo'lmaydi Printsipi (You Aren't Gonna Need It (YAGNI))

**Tavsif:** YAGNI hozir talab qilinmagan funksionallikni "kelajakda kerak bo'lar" degan taxmin bilan yozmaslikni talab qiladi. Har bir ortiqcha abstraksiya qatlami qo'shimcha test, dokumentatsiya va migratsiya yuki keltiradi, lekin haqiqiy talab kelganda u odatda noto'g'ri shaklda bo'lib chiqadi. Printsip kodni o'chirishni emas, balki qarorni haqiqiy ma'lumot paydo bo'lgunga qadar kechiktirishni (defer) targ'ib qiladi. Bu YAGNI'ni rejalashtirishdan voz kechish deb tushunmaslik kerak - gap faqat spekulyativ implementatsiya haqida.

**Spring'da qayerda uchraydi:** Spring Boot 3.x auto-configuration o'zi YAGNI'ning amaliy ko'rinishi: `@ConditionalOnMissingBean` va `@ConditionalOnClass` orqali siz faqat `spring-boot-starter-data-jpa` yoki `spring-boot-starter-web` qo'shsangiz kerakli infratuzilma bean'lari yaratiladi, qolgani umuman yuklanmaydi. Loyiha darajasida YAGNI buzilishining klassik ko'rinishi - har bir `JpaRepository` ustiga hech narsa qo'shmaydigan `XxxRepositoryImpl` yoki `XxxDao` wrapper'i, yoki bitta implementatsiyasi bor interfeyslar to'plami. Spring Modulith 1.x (`spring-modulith-core`) monolit ichida modul chegaralarini saqlab turishga imkon beradi, shuning uchun mikroservislarga ajratishni haqiqiy masshtab muammosi paydo bo'lganda qilish mumkin. `@ConfigurationProperties` ham shu ruhda: konfiguratsiya kaliti faqat real ehtiyoj bo'lganda qo'shiladi.

**Qo'llanish keyslari:**
- Yangi CRUD modulni bitta `@Service` + `JpaRepository` bilan boshlash, hozircha kerak bo'lmagan DAO va mapper qatlamlarini qo'shmaslik.
- Monolitni Spring Modulith bilan modullarga bo'lib, mikroservis ajratishni trafik o'sishiga qadar kechiktirish.
- Faqat bitta provayder ishlatilayotganda "plugin arxitekturasi" o'rniga oddiy konkret sinf qoldirish.
- Hozircha bitta ma'lumotlar bazasi yetarli bo'lsa, multi-tenant routing datasource'ni rejaga olib, lekin implementatsiya qilmasdan qoldirish.
- Kesh, batch va event stream'ni profiling natijasi muammoni ko'rsatgandan keyin kiritish.

**Ehtiyot bo'ling:** YAGNI arxitektura darajasidagi qaytarib bo'lmaydigan qarorlarga (ma'lumotlar bazasi tanlovi, API kontrakt shakli, xavfsizlik modeli, audit va multi-tenancy) tegishli emas - bularni keyin qo'shish juda qimmat. Shuningdek YAGNI'ni test yozmaslik yoki xatolarni boshqarishni tashlab ketish uchun bahona qilib ishlatish printsipni butunlay buzadi.

## 26.22 Eng Kam Hayratlanish Printsipi (Principle of Least Astonishment)

**Tavsif:** Tizim o'zini foydalanuvchi va chaqiruvchi kod kutgandek tutishi kerak: nom nimani aytsa, aynan shuni qilishi, odatiy konvensiyalardan asossiz chetga chiqmasligi lozim. Printsip API dizayni, konfiguratsiya nomlari, standart qiymatlar va xato xabarlariga birdek tegishli. Maqsad - jamoadagi yangi injener kodni o'qiganda "bu qanday ishlaydi?" degan savol tug'ilmasligi. Hayratlanish narxi juda baland: u odatda production incident shaklida to'lanadi.

**Spring'da qayerda uchraydi:** Spring'ning "convention over configuration" yondashuvi shu printsipga tayanadi: `application.yml` dagi relaxed binding (`my-prop`, `myProp`, `MY_PROP` bir xil `@ConfigurationProperties` maydoniga tushadi), Spring Data JPA'ning `findByLastNameOrderByFirstNameAsc` kabi derived query method nomlari, `@RestController` uchun standart JSON serializatsiya. Klassik "hayratlanish" manbai - `@Transactional`ning standart rollback siyosati: faqat `RuntimeException` va `Error` da rollback bo'ladi, checked exception'da esa transaksiya commit qilinadi, agar `rollbackFor` berilmasa. Yana biri - bir xil bean ichidagi metodni `this.method()` orqali chaqirganda proxy chetlab o'tilishi, shuning uchun `@Transactional`, `@Cacheable` va `@Async` ishlamaydi. Spring Framework 6.x dagi `ProblemDetail` (RFC 9457) xato javoblarini standart, kutilgan shaklda qaytarish uchun xizmat qiladi.

**Qo'llanish keyslari:**
- REST API'da HTTP status kodlarini semantikasiga mos qaytarish: 201 + `Location` yaratishda, 404 topilmaganda, 409 konfliktda.
- `@ConfigurationProperties` prefikslarini modul nomiga mos qo'yish va standart qiymatlarni xavfsiz tomonga (masalan, feature flag `false`) sozlash.
- `getXxx()` metodi hech narsani o'zgartirmasligi, `findXxx()` esa `Optional` qaytarishi kabi nomlash konvensiyalarini butun kod bazasida saqlash.
- Checked exception ishlatiladigan servislarda `@Transactional(rollbackFor = Exception.class)` ni ochiq yozib, kutilmagan commit'dan saqlanish.
- Jamoa uchun ArchUnit yoki Checkstyle qoidalari bilan nomlash va paket konvensiyalarini majburlash.

**Ehtiyot bo'ling:** Eng ko'p hayratlanish Spring'ning "sehrli" imkoniyatlarini aralash ishlatganda tug'iladi - masalan `@Async` metodga `@Transactional` qo'yish yoki bir nechta `AOP` aspektlarini noma'lum tartibda stacking qilish; `@Order` ni ochiq belgilang. Shuningdek "biz uchun qulay" deb o'ylab o'ylab chiqarilgan maxsus konvensiya (`findUser()` ichida yozish operatsiyasi) kutilmagan nojo'ya ta'sirlar manbaiga aylanadi.

## 26.23 Buyruq-So'rov Ajratilishi (Command-Query Separation)

**Tavsif:** Bertrand Meyer taklif qilgan bu printsipga ko'ra metod yoki holatni o'zgartiradi (command, hech narsa qaytarmaydi), yoki ma'lumot qaytaradi (query, holatni o'zgartirmaydi) - ikkisini bitta metodda aralashtirmaydi. Bu kodni mulohaza qilish, keshlash, qayta urinish (retry) va test qilishni ancha osonlashtiradi, chunki query'lar nojo'ya ta'sirsiz bo'lib, ularni xohlagancha chaqirish mumkin. CQRS esa shu g'oyani butun arxitektura darajasiga - alohida read va write modellarga - ko'chirishdir.

**Spring'da qayerda uchraydi:** Spring'ning data API'lari bu ajratishni signatura darajasida ko'rsatadi: `JdbcTemplate` va Spring Framework 6.1 dagi `JdbcClient` da `query()` ma'lumot o'qiydi, `update()` esa o'zgartiradi va ta'sirlangan qatorlar sonini qaytaradi. Spring Data JPA'da o'zgartiruvchi so'rov `@Modifying @Query` bilan ochiq belgilanishi shart, aks holda `EntityManager` xato beradi; o'qish metodlarini esa `@Transactional(readOnly = true)` bilan belgilash Hibernate'ga flush'ni o'tkazib yuborish imkonini beradi. Kesh abstraksiyasida `@Cacheable` faqat query metodlarda ma'noga ega, holatni o'zgartiruvchi metod uchun `@CacheEvict` yoki `@CachePut` ishlatiladi. Retry (`spring-retry`) va `@Transactional` propagation'ni to'g'ri qo'llash ham metod command yoki query ekanini bilishga tayanadi. CQRS darajasida Spring ilovalari `ApplicationEventPublisher`, Spring Modulith event publication registry yoki Axon Framework bilan read modelni alohida quradi.

```java
@Transactional(readOnly = true)
public Optional<OrderView> findOrder(UUID id) { ... }   // query

@Transactional
@CacheEvict(cacheNames = "orders", key = "#id")
public void cancelOrder(UUID id) { ... }                // command
```

**Qo'llanish keyslari:**
- Read-only servis metodlarini `@Transactional(readOnly = true)` bilan belgilab, replica datasource'ga yo'naltirish.
- `@Cacheable` ni faqat nojo'ya ta'sirsiz query metodlarga qo'yib, noto'g'ri keshlangan yozuvlardan saqlanish.
- `@Modifying(clearAutomatically = true)` bilan bulk update so'rovlarini aniq ajratib, stale entity holatidan qutulish.
- GET endpoint'lar hech qachon holatni o'zgartirmasligini majburlash, shunda retry va CDN keshlash xavfsiz bo'ladi.
- Hisobot va dashboard uchun alohida read model (projection) qurib, yozuv modelidan ajratish.

**Ehtiyot bo'ling:** Printsipni mutlaqlashtirish amaliy muammolar tug'diradi - `Stack.pop()`, `Queue.poll()` yoki `save()` metodining generated ID bilan entity qaytarishi atomiklik uchun zarur istisnolardir. CQRS'ni esa eventual consistency talablarini jamoa tushunmaydigan joyda kiritish ko'pincha YAGNI buzilishi va murakkablik o'sishiga olib keladi.

## 26.24 O'zgaruvchan Qismni Inkapsulyatsiya Qilish (Encapsulate What Varies)

**Tavsif:** Tizimda o'zgarish ehtimoli yuqori bo'lgan qismni aniqlab, uni interfeys yoki alohida modul orqasiga yashirish kerak, shunda o'zgarish barqaror kodga tarqalmaydi. Bu Strategy, Adapter va Factory kabi patternlarning umumiy asosidir. Amalda bu "o'zgarish o'qlarini" izlash degani: to'lov provayderi, soliq qoidalari, narx siyosati, tashqi API versiyasi. To'g'ri chegara qo'yilganda yangi variant qo'shish mavjud kodni o'zgartirmasdan amalga oshadi.

**Spring'da qayerda uchraydi:** Spring Framework'ning o'zi shu printsip ustiga qurilgan: `PlatformTransactionManager` tranzaksiya texnologiyasini, `CacheManager` kesh provayderini (Caffeine, Redis), `PasswordEncoder` esa hashing algoritmini yashiradi - Spring Security 6.x dagi `DelegatingPasswordEncoder` `{bcrypt}`, `{argon2}` prefikslari bilan algoritm migratsiyasini kod o'zgartirmasdan bajaradi. Spring AI 1.x dagi `ChatModel` va `EmbeddingModel` abstraksiyalari model provayderini (OpenAI, Anthropic, Ollama) starter almashtirish bilan o'zgartirish imkonini beradi, `VectorStore` esa vektor bazasini yashiradi. Ilova kodida bu `Map<String, PaymentStrategy>` injection, `ObjectProvider<T>`, `@ConditionalOnProperty` va Spring profillari orqali amalga oshiriladi; `@ConfigurationProperties` esa o'zgaruvchan sozlamalarni bitta typed obyektga to'playdi.

**Qo'llanish keyslari:**
- To'lov provayderlarini `PaymentGateway` interfeysi orqasiga olib, Stripe va mahalliy provayderni bitta kod bazasida saqlash.
- Soliq yoki chegirma hisoblash qoidalarini mamlakat bo'yicha alohida strategy bean'larga ajratish.
- Fayl saqlashni `StorageClient` abstraksiyasi bilan yashirib, lokalda disk, production'da S3 ishlatish.
- Spring AI'da `ChatModel` orqali LLM provayderini A/B test qilish yoki fallback qo'yish.
- Notification kanallarini (email, SMS, push) bitta interfeys va `@ConditionalOnProperty` bilan yoqib-o'chirish.

**Ehtiyot bo'ling:** Noto'g'ri o'q bo'yicha abstraksiya qurish eng qimmat xato: bitta implementatsiyasi bor "universal" interfeys faqat shovqin qo'shadi, keyin esa ikkinchi provayder kelganda u mos kelmaydi (leaky abstraction). Ikkinchi real variant paydo bo'lgandan keyin refaktor qilish ko'pincha arzonroq bo'ladi.

## 26.25 Interfeysga Qarab Programmalash (Program to an Interface)

**Tavsif:** Kod konkret sinfga emas, kontraktga (interfeys yoki abstrakt tur) bog'lanishi kerak, shunda implementatsiyani almashtirish, test uchun stub qo'yish va proxy bilan o'rash mumkin bo'ladi. Bu "Program to an interface, not an implementation" - GoF kitobining asosiy tavsiyalaridan biri. Natijada komponentlar o'rtasidagi bog'liqlik kompilyatsiya vaqtida minimallashadi va modul chegaralari aniq bo'ladi.

**Spring'da qayerda uchraydi:** Spring Data'da repozitoriy odatda faqat interfeys bo'ladi (`extends JpaRepository<Order, UUID>`), implementatsiyani esa runtime'da proxy generatsiya qiladi. Spring Framework 6.x dagi declarative HTTP client ham xuddi shunday: `@HttpExchange`/`@GetExchange` bilan belgilangan interfeys `HttpServiceProxyFactory` orqali `RestClient` yoki `WebClient` ustida implementatsiyalanadi. Ilova kodida `List`, `Map`, `Collection` kabi JDK interfeyslarini maydon va signatura turi qilib ishlatish, `ApplicationContext`/`BeanFactory` ga tayanish ham shu printsip. AOP nuqtai nazaridan ham muhim: interfeysi bor bean uchun Spring JDK dynamic proxy, bo'lmasa CGLIB subclass proxy yasaydi - CGLIB `final` sinf va `final` metodlarni proxy qila olmaydi, shuning uchun `@Transactional` yoki `@Cacheable` ishlatiladigan sinflarni `final` qilmaslik kerak.

```java
@HttpExchange("/api/v1")
public interface BillingClient {
    @GetExchange("/invoices/{id}")
    Invoice byId(@PathVariable String id);
}
```

**Qo'llanish keyslari:**
- Domen servisini interfeys sifatida e'lon qilib, integratsiya testlarida `@TestConfiguration` orqali fake implementatsiya qo'yish.
- Tashqi tizim mijozlarini `@HttpExchange` interfeyslari bilan e'lon qilib, kontraktni bitta joyda saqlash.
- Spring Modulith modullarida faqat interfeys va DTO'ni public API qilib chiqarish, implementatsiyani `internal` paketda yashirish.
- Collection turlarini signaturada `List`/`Set` sifatida qaytarib, chaqiruvchini `ArrayList`ga bog'lamaslik.
- Bir nechta implementatsiyani `@Qualifier` yoki `Map<String, Handler>` injection bilan tanlash.

**Ehtiyot bo'ling:** Har bir sinf uchun avtomatik interfeys yasash anti-pattern - bitta implementatsiyali, o'zgarmaydigan servislar uchun bu faqat navigatsiyani qiyinlashtiradi. Shuningdek interfeysga JPA entity yoki Hibernate turlari oqib chiqsa, abstraksiya ma'nosini yo'qotadi.

## 26.26 Gollivud Printsipi (Hollywood Principle (Inversion of Control))

**Tavsif:** "Bizga qo'ng'iroq qilmang, biz o'zimiz chaqiramiz" - komponent framework'ni chaqirmaydi, framework komponentning callback'larini kerakli vaqtda chaqiradi. Bu nazoratni ilova kodidan konteynerga o'tkazish (Inversion of Control) degani; natijada lifecycle, resurs boshqaruvi va xatolarni qayta ishlash framework zimmasida qoladi. Dependency Injection - IoC'ning eng keng tarqalgan ko'rinishi, Template Method esa uning sinf darajasidagi variantidir.

**Spring'da qayerda uchraydi:** Bu Spring'ning mavjudlik asosi: `ApplicationContext` bean'larni yaratadi, bog'laydi va lifecycle callback'larini chaqiradi - `@PostConstruct`/`@PreDestroy` (Jakarta annotatsiyalari), `InitializingBean`, `DisposableBean`, `SmartLifecycle`, `BeanPostProcessor`. Startup'da `ApplicationRunner` va `CommandLineRunner`, event'larda `@EventListener` va `ApplicationListener` sizning metodingizni framework chaqiradi. Template Method ko'rinishi: `JdbcTemplate.query(sql, rowMapper)` resurs boshqaruvini o'ziga oladi va faqat `RowMapper` callback'ingizni chaqiradi, `TransactionTemplate.execute(callback)` esa commit/rollback'ni o'zi hal qiladi. Xuddi shunday `@Scheduled`, `@KafkaListener`, `@RabbitListener`, `@JmsListener`, `HandlerInterceptor` va Spring Security'ning `OncePerRequestFilter` ham callback modelida ishlaydi.

**Qo'llanish keyslari:**
- Startup migratsiya yoki warm-up ishini `ApplicationRunner` bean'ida bajarish.
- Domen hodisalarini `@EventListener` va `@TransactionalEventListener(phase = AFTER_COMMIT)` bilan qayta ishlash.
- Rejali ishlarni `@Scheduled(cron = "...")` bilan e'lon qilib, thread va timer boshqaruvini Spring'ga qoldirish.
- JDBC resurslarini `JdbcClient`/`JdbcTemplate` callback'lari orqali ishlatib, `try-finally` boilerplate'dan qutulish.
- Graceful shutdown uchun `SmartLifecycle` implementatsiya qilib, consumer'larni tartibli to'xtatish.

**Ehtiyot bo'ling:** Konteyner nazoratni o'zi boshqarganda bean yaratilish tartibi va callback fazalari muhim bo'lib qoladi: `@PostConstruct` ichida boshqa bean'ning hali tayyor bo'lmagan holatiga tayanish yoki konstruktorda uzoq I/O qilish startup'ni sindiradi. Shuningdek ko'p sonli yashirin callback'lar debug qilishni qiyinlashtiradi - ularning tartibini `@Order` bilan aniq belgilang.

## 26.27 Mustahkamlik Printsipi (Robustness Principle (Postel's Law))

**Tavsif:** Jon Postel ta'rifiga ko'ra: "yuborayotganingizda qat'iy, qabul qilayotganingizda bag'rikeng bo'l". Ya'ni chiqish ma'lumotlari kontraktga aniq mos bo'lishi, kiruvchi ma'lumotlarda esa ahamiyatsiz chetlanishlar (notanish maydonlar, qo'shimcha bo'sh joy, yangi enum qiymatlari) tizimni yiqitmasligi kerak. Bu "tolerant reader" yondashuvi distributed tizimlarda servislarni bir-biridan mustaqil deploy qilish imkonini beradi. Aks holda provayder tomonidagi har bir kichik qo'shimcha barcha iste'molchilarni sindiradi.

**Spring'da qayerda uchraydi:** Spring Boot 3.x Jackson'ni aynan shu printsip bilan sozlaydi: `FAIL_ON_UNKNOWN_PROPERTIES` standart holda o'chirilgan, ya'ni notanish JSON maydonlari xato bermaydi; buni `spring.jackson.deserialization.fail-on-unknown-properties` yoki sinf ustida `@JsonIgnoreProperties(ignoreUnknown = true)` bilan boshqarish mumkin. Chiqish tomonida qat'iylik `@JsonInclude(NON_NULL)`, aniq DTO/record turlari va `ProblemDetail` (RFC 9457) orqali ta'minlanadi. Kafka va gRPC integratsiyalarida bu schema evolution darajasida ishlaydi: Avro va Protobuf backward/forward mosligi, Confluent Schema Registry qoidalari - bu Spring'ning emas, infratuzilmaning mas'uliyati, Spring ilovasi esa `spring-kafka` serializer konfiguratsiyasi orqali shunga tayanadi. Kiruvchi so'rovlarning haqiqiy biznes talablarini esa Jakarta Bean Validation (`@Valid`, `@NotNull`) qat'iy tekshiradi.

**Qo'llanish keyslari:**
- Upstream servis javobiga yangi maydon qo'shganda iste'molchi deployini talab qilmaslik uchun tolerant reader DTO'lar ishlatish.
- Kafka topic sxemasini backward-compatible evolutsiya qilib, consumer'larni producer'dan mustaqil deploy qilish.
- Notanish enum qiymatini `UNKNOWN` ga map qilib (`@JsonEnumDefaultValue`), yangi tur kelganda consumer'ni yiqitmaslik.
- REST API versiyalashda eski mijozlar uchun qo'shimcha maydonlarni ignore qiladigan o'qish mantiqi qoldirish.
- Tashqi webhook payload'larini bo'sh joy, sana formati va katta-kichik harf farqlariga chidamli parse qilish.

**Ehtiyot bo'ling:** Bag'rikenglikni xavfsizlik va to'lov kabi joylarda qo'llash xato - autentifikatsiya, avtorizatsiya va pul bilan bog'liq input qat'iy validatsiya va allow-list talab qiladi, aks holda injection va mass assignment xavfi tug'iladi. Shuningdek doimiy "jimgina kechirish" xatolarni yashirib, ma'lumot buzilishini keyinroq, tuzatish qiyin bo'lgan paytda oshkor qiladi - chetlanishlarni hech bo'lmasa metrika va log'ga yozib boring.

## 26.28 Yagona Abstraksiya Darajasi (Single Level of Abstraction)

**Tavsif:** Bitta metod ichidagi barcha ifodalar taxminan bir xil mavhumlik darajasida bo'lishi kerak: yuqori darajadagi biznes qadamlari bilan past darajadagi string manipulyatsiyasi yoki SQL tafsilotlari aralashmasligi lozim. Bu SLAP (Single Level of Abstraction Principle) deb ham ataladi va metodni "o'qiladigan hikoya" ga aylantiradi. Amalda bu past darajadagi tafsilotlarni alohida xususiy metodga yoki alohida sinfga ko'chirish bilan erishiladi. Natija - kod review'da niyat tezda ko'rinadi va xatolar tez topiladi.

**Spring'da qayerda uchraydi:** Spring'ning qatlamli arxitekturasi bu printsipni tabiiy ravishda qo'llaydi: `@RestController` faqat HTTP tafsilotlari (status, header, DTO mapping) bilan ishlaydi, `@Service` biznes orkestratsiyasi va `@Transactional` chegarasini belgilaydi, repozitoriy esa persistence tafsilotini o'ziga oladi. Buzilish ko'rinishi - controller ichida `EntityManager` yoki `RestClient` chaqiruvi, yoki servis metodida JSON parsing va SQL stringlari aralashuvi. `JdbcClient` va `RestClient` kabi fluent API'lar past darajadagi ishni bitta ifodaga yig'ib, chaqiruvchi metodni bir darajada saqlashga yordam beradi. Spring Modulith `ApplicationModules.of(App.class).verify()` va ArchUnit testlari esa qatlam va modul chegaralarini CI'da avtomatik majburlash uchun ishlatiladi.

**Qo'llanish keyslari:**
- Controller metodini 5-10 qatorga qisqartirib, barcha biznes qadamlarini servis metodiga ko'chirish.
- Uzun `processOrder()` metodini `validate()`, `reserveStock()`, `charge()`, `publishEvent()` qadamlariga ajratish.
- Mapping mantiqini alohida mapper komponentga (MapStruct yoki qo'lda yozilgan) chiqarib, servisni toza qoldirish.
- Retry, timeout va circuit breaker tafsilotlarini `@Retryable` yoki Resilience4j dekoratoriga ko'chirib, biznes metodidan olib tashlash.
- ArchUnit testi bilan controller'dan repozitoriyga to'g'ridan-to'g'ri murojaatni taqiqlash.

**Ehtiyot bo'ling:** Printsipni haddan oshirib, har 3 qatorni alohida metodga ajratish "metod chakanalashuvi" ga olib keladi va o'qishni aksincha qiyinlashtiradi - faqat o'zi mustaqil ma'noga ega va yaxshi nomlanadigan bo'laklarni ajratish kerak. Shuningdek har bir qatlam uchun yangi DTO yasash mexanik majburiyatga aylansa, bu faqat boilerplate o'stiradi.

## 26.29 Barqaror Bog'liqliklar va Barqaror Abstraksiyalar (Stable Dependencies & Stable Abstractions)

**Tavsif:** Robert Martin'ning SDP qoidasi: bog'liqlik yo'nalishi barqarorlik tomon bo'lishi kerak - tez o'zgaradigan modul barqaror modulga tayanishi mumkin, teskarisi esa yo'q. SAP qoidasi esa buni to'ldiradi: barqaror modul abstrakt bo'lishi kerak, aks holda uni o'zgartirish imkonsiz bo'lib qoladi. Barqarorlik bu yerda "yaxshi" degani emas, balki "o'zgartirish qiyinligi" - unga ko'p modul tayanadi. Bu ikki qoida birgalikda arxitekturada bog'liqlik grafining yo'nalishini belgilaydi va aylanali (cyclic) bog'liqliklardan saqlaydi.

**Spring'da qayerda uchraydi:** Spring ekotizimining o'zi shu modelda qurilgan: `spring-core` va Jakarta API paketlari (`jakarta.persistence`, `jakarta.servlet`) juda barqaror va asosan abstraksiyalardan iborat, ularga butun dunyo tayanadi; konkret, tez o'zgaradigan kod esa chekkada turadi. Spring Framework 6.x/7.x va Spring Boot 3.x/4.x deprecation siyosati, `@Deprecated(since, forRemoval)` belgilashlari ham barqaror API kontraktini saqlash vositasidir. Loyiha darajasida bu Maven/Gradle multi-module tuzilmada `api` va `impl` modullarini ajratish, Gradle'da `api` va `implementation` konfiguratsiyalarini to'g'ri ishlatish bilan amalga oshiriladi. Spring Modulith `ApplicationModules.of(Application.class).verify()` modullar orasidagi aylanali bog'liqlik va yashirin paketlarga murojaatni aniqlaydi; ArchUnit esa `noClasses().that().resideInAPackage("..domain..").should().dependOnClassesThat().resideInAPackage("..infrastructure..")` kabi qoidalar bilan yo'nalishni majburlaydi. Dependency Inversion bu yerda amaliy vosita: domen port interfeysini e'lon qiladi, infratuzilma adapter uni implementatsiya qiladi.

**Qo'llanish keyslari:**
- Hexagonal arxitekturada domen modulini barqaror va abstrakt qilib, JPA va Kafka adapterlarini unga tayantirish.
- Umumiy kontrakt kutubxonasini (`order-api` DTO va interfeyslar) alohida artifact qilib, servislar o'rtasida ulashish.
- Spring Modulith `verify()` testini CI'ga qo'shib, modullar orasida aylanali bog'liqlik paydo bo'lishini bloklash.
- Gradle'da tranzitiv oqishni kamaytirish uchun `implementation` ni standart qilib, faqat kontraktni `api` orqali ochish.
- Ko'p jamoa foydalanadigan umumiy modulni semantik versiyalash va deprecation davri bilan boshqarish.

**Ehtiyot bo'ling:** Eng keng tarqalgan buzilish - "shared-common" yoki "utils" moduli: unga hamma tayanadi (ya'ni u barqaror), lekin ichida konkret, tez o'zgaradigan kod va entity'lar bo'ladi, natijada har bir o'zgarish butun tizimni qayta deploy qilishni talab qiladi. Ikkinchi tuzoq - metrikalarni (instability, abstractness) maqsadga aylantirib, haqiqiy ehtiyojsiz interfeyslar o'rmonini yaratish.

## 26.30 Amalda qo'llash

- [ ] Eng katta 10 sinfni topib, har biri uchun savolga javob yozing: uning o'zgarish sababi nechta.
- [ ] `instanceof` yoki tur bo'yicha `switch` ishlatadigan joylarni qidirib, polimorfizm bilan almashtirish nomzodlarini belgilang.
- [ ] Interfeyslarni ko'rib chiqing: mijozlar ishlatmaydigan metodlar borligini tekshiring (interface segregation).
- [ ] Konkret sinfga bog'langan konstruktor parametrlarini toping va ularni abstraksiyaga o'tkazish foydasini qaror qiling.
- [ ] Vorislik ishlatilgan har bir joyni tekshirib, subclass bazaning shartnomasini buzmayotganini tasdiqlang.
- [ ] Zanjir shaklidagi chaqiruvlarni (`a.getB().getC().getD()`) qidirib, Demeter qonunini buzadigan joylarni ro'yxat qiling.
- [ ] DRY nomi bilan yaratilgan umumiy kodni tekshiring: u haqiqatan bir xil qoidami yoki tasodifan o'xshash ikki qoidami.
- [ ] YAGNI bo'yicha ishlatilmaydigan abstraksiya va konfiguratsiya nuqtalarini topib, olib tashlash ro'yxatini tuzing.

---

[&larr; 25. Anti-patternlar](25-anti-patternlar.md) · [Mundarija](README.md) · [27. Monolitdan microservice'ga migratsiya patternlari &rarr;](27-monolitdan-microservicega-migratsiya.md)
