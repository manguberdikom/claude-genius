<!-- doc: architect | chapter: 15 | part: III. Spring chuqur bilim -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 15. Spring Core mexanikasi: IoC konteyner, bean lifecycle, AOP proxy (Spring Core Mechanics)

<details>
<summary>Bu bobdagi 12 bo'lim</summary>

- [15.1 `ApplicationContext` ishga tushish bosqichlari: bean definition, post-processor, instantiation](#151-applicationcontext-ishga-tushish-bosqichlari-bean-definition-post-processor-instantiation)
- [15.2 `BeanFactoryPostProcessor` va `BeanPostProcessor` farqi va ularning tartibi](#152-beanfactorypostprocessor-va-beanpostprocessor-farqi-va-ularning-tartibi)
- [15.3 Bean lifecycle: konstruktor, inject, `@PostConstruct`, `@PreDestroy`](#153-bean-lifecycle-konstruktor-inject-postconstruct-predestroy)
- [15.4 Scope lar: singleton, prototype, request va ularning amaliy oqibati](#154-scope-lar-singleton-prototype-request-va-ularning-amaliy-oqibati)
- [15.5 Bog'liqlikni kiritish usullari va nega konstruktor orqali kiritish afzal](#155-bogliqlikni-kiritish-usullari-va-nega-konstruktor-orqali-kiritish-afzal)
- [15.6 Aylanma bog'liqlik: nega paydo bo'ladi, Spring Boot 3 da nega xato beradi](#156-aylanma-bogliqlik-nega-paydo-boladi-spring-boot-3-da-nega-xato-beradi)
- [15.7 `@Lazy`, `@Primary`, `@Qualifier`, `@Conditional` qachon kerak](#157-lazy-primary-qualifier-conditional-qachon-kerak)
- [15.8 AOP mexanikasi: JDK dinamik proxy va CGLIB farqi](#158-aop-mexanikasi-jdk-dinamik-proxy-va-cglib-farqi)
- [15.9 Proxy tuzog'i: ichki metod chaqiruvida `@Transactional` va `@Cacheable` ishlamasligi](#159-proxy-tuzogi-ichki-metod-chaqiruvida-transactional-va-cacheable-ishlamasligi)
- [15.10 `ApplicationEvent` va `@EventListener`: sinxron tabiati va tranzaksiya bilan bog'liqligi](#1510-applicationevent-va-eventlistener-sinxron-tabiati-va-tranzaksiya-bilan-bogliqligi)
- [15.11 Ishga tushish vaqtini qisqartirish: ortiqcha bean va komponent skanerlash](#1511-ishga-tushish-vaqtini-qisqartirish-ortiqcha-bean-va-komponent-skanerlash)
- [15.12 Amalda qo'llash](#1512-amalda-qollash)

</details>



Spring konteyneri sehr emas, u aniq tartibda ishlaydigan mexanizm. Arxitektor uchun bu mexanizmni bilish zarurati amaliy: ishga tushish vaqti, aylanma bog'liqlik xatosi, `@Transactional` ning jim turib ishlamasligi va event larning tranzaksiya bilan noto'g'ri bog'lanishi hammasi shu mexanizmdan kelib chiqadi. Quyida konteyner ichida nima sodir bo'lishini bosqichma-bosqich ko'rib chiqamiz va har bosqichga bog'langan tuzoqlarni ajratamiz. Misollar to'lov servisi, buyurtma va ombor qoldig'i domenidan olingan.

## 15.1 `ApplicationContext` ishga tushish bosqichlari: bean definition, post-processor, instantiation

`AbstractApplicationContext.refresh()` ketma-ketligi Spring Framework 6.x da deterministik. Avval `obtainFreshBeanFactory()` bo'sh `DefaultListableBeanFactory` yaratadi. Keyin `invokeBeanFactoryPostProcessors()` chaqiriladi va aynan shu nuqtada `ConfigurationClassPostProcessor` komponent skanerlashni bajaradi, `@Configuration` sinflarini o'qiydi, `@Bean` metodlaridan bean definition lar yasaydi. Bu bosqichda hech bir business bean yaratilmagan, faqat metadata bor.

Keyin `registerBeanPostProcessors()` `BeanPostProcessor` larni topadi va ularni ro'yxatga oladi. Faqat shundan keyin `finishBeanFactoryInitialization()` barcha singleton larni haqiqatan instantiate qiladi. Oxirida `finishRefresh()` `ContextRefreshedEvent` ni yuboradi va `SmartLifecycle` bean larini ishga tushiradi.

```java
// Bean definition bosqichida qancha bean ro'yxatga olinganini ko'rish.
// Bu metadata, hali hech narsa yaratilmagan.
@Component
class DefinitionAudit implements BeanFactoryPostProcessor {

    @Override
    public void postProcessBeanFactory(ConfigurableListableBeanFactory bf) {
        // Bu yerda getBean() chaqirmaymiz: bean ni muddatidan oldin
        // yaratib, uni proxy lanmay qolishiga olib kelamiz.
        System.out.println("definition soni: " + bf.getBeanDefinitionCount());
        BeanDefinition bd = bf.getBeanDefinition("paymentService");
        System.out.println("scope: " + bd.getScope()
                + ", lazy: " + bd.isLazyInit());
    }
}
```

Amaliy xulosa: definition bosqichida bean ni `getBean()` bilan tortib olish eng tipik xato. Bean `BeanPostProcessor` lar ro'yxatga olinishidan oldin yaratiladi va na `@Transactional`, na `@Async` proxy ni oladi. Log dagi "is not eligible for getting processed by all BeanPostProcessors" ogohlantirishi aynan shuni bildiradi.

## 15.2 `BeanFactoryPostProcessor` va `BeanPostProcessor` farqi va ularning tartibi

Ikkisi nomi o'xshash, lekin ular butunlay boshqa bosqichda ishlaydi. `BeanFactoryPostProcessor` bean definition ni, ya'ni retseptni o'zgartiradi. `BeanPostProcessor` esa allaqachon yaratilgan obyektni, ya'ni tayyor taomni o'zgartiradi yoki uni proxy bilan o'raydi.

| Jihat | `BeanFactoryPostProcessor` | `BeanPostProcessor` |
|---|---|---|
| Nima bilan ishlaydi | `BeanDefinition` (metadata) | instance (obyekt) |
| Chaqirilish vaqti | singleton lar yaratilishidan oldin, bir marta | har bir bean yaratilganda |
| Tipik vazifa | property qiymatini almashtirish, definition qo'shish | AOP proxy o'rash, `@Autowired` ni bajarish |
| Platforma misoli | `ConfigurationClassPostProcessor`, `PropertySourcesPlaceholderConfigurer` | `AutowiredAnnotationBeanPostProcessor`, `AnnotationAwareAspectJAutoProxyCreator` |
| Tartib mexanizmi | `PriorityOrdered`, keyin `Ordered`, keyin qolganlar | xuddi shu uch guruh |
| Xato narxi | kontekst ko'tarilmaydi | bean proxy siz qoladi, xato jim o'tadi |

`BeanDefinitionRegistryPostProcessor` esa `BeanFactoryPostProcessor` ning kengaytmasi va u yangi definition qo'shish imkonini beradi. Spring uni birinchi chaqiradi, chunki definition qo'shish definition o'zgartirishdan oldin bo'lishi shart.

```java
// To'lov provayderlarini konfiguratsiyadan dinamik ro'yxatga olish.
// Har bir provayder uchun alohida bean definition yasaymiz.
class ProviderRegistrar implements BeanDefinitionRegistryPostProcessor {

    @Override
    public void postProcessBeanDefinitionRegistry(BeanDefinitionRegistry reg) {
        for (String code : List.of("uzcard", "humo", "visa")) {
            AbstractBeanDefinition bd = BeanDefinitionBuilder
                    .genericBeanDefinition(HttpPaymentGateway.class)
                    .addConstructorArgValue(code)
                    .setLazyInit(true)   // kerak bo'lmasa yaratilmaydi
                    .getBeanDefinition();
            reg.registerBeanDefinition("gateway_" + code, bd);
        }
    }
}
```

`BeanPostProcessor` yozganda bitta qoida bor: u imkon qadar kam dependency ga ega bo'lsin. Post-processor boshqa bean ga muhtoj bo'lsa, o'sha bean ham muddatidan oldin yaratiladi va proxy siz qoladi. Shu sababli kerakli bean ni `ObjectProvider` orqali kechiktirib olish to'g'ri usul.

## 15.3 Bean lifecycle: konstruktor, inject, `@PostConstruct`, `@PreDestroy`

Bitta singleton bean uchun tartib qat'iy: konstruktor ishlaydi, keyin field va setter inject qilinadi, keyin `Aware` interfeyslari chaqiriladi, keyin `BeanPostProcessor.postProcessBeforeInitialization()`, keyin `@PostConstruct`, keyin `InitializingBean.afterPropertiesSet()`, keyin `@Bean(initMethod)`, va oxirida `postProcessAfterInitialization()`. Proxy aynan oxirgi qadamda yasaladi.

```java
@Service
public class PaymentService {

    private final PaymentGateway gateway;
    private final MeterRegistry meters;
    private Counter failures;

    // 1-qadam: konstruktor. Dependency lar shu yerda yetib keladi.
    public PaymentService(PaymentGateway gateway, MeterRegistry meters) {
        this.gateway = gateway;
        this.meters = meters;
        // Bu yerda gateway ni ISHLATMAYMIZ: u hali proxy lanmagan
        // bo'lishi mumkin va tranzaksiya ishlamaydi.
    }

    // 2-qadam: barcha dependency tayyor, og'ir ish shu yerda.
    @PostConstruct
    void init() {
        this.failures = meters.counter("payment.failures");
    }

    // Faqat singleton uchun chaqiriladi va faqat graceful shutdown da.
    @PreDestroy
    void drain() {
        gateway.closeIdleConnections();
    }
}
```

Eng ko'p uchraydigan tuzoq: konstruktor ichida inject qilingan bean ning metodini chaqirish. O'sha payt proxy hali yo'q, demak `@Transactional` ishlamaydi. Og'ir initializatsiya va cache warm-up `@PostConstruct` yoki `ApplicationReadyEvent` ga tegishli.

`@PreDestroy` ishonchliligi cheklangan: u faqat kontekst normal yopilganda ishlaydi. `kill -9`, OOM killer yoki `terminationGracePeriodSeconds` tugaganda bajarilmaydi, shuning uchun unga majburiy business logika qo'yish xato. Kubernetes da `server.shutdown=graceful` va `spring.lifecycle.timeout-per-shutdown-phase=30s` kerak, pod grace period esa taxminan 45 sekund bo'lsin.

## 15.4 Scope lar: singleton, prototype, request va ularning amaliy oqibati

Default scope singleton va u konteyner darajasidagi yakka nusxa. Bu degani singleton bean da o'zgaradigan holat saqlash thread safety buzilishiga olib keladi. Prototype har `getBean()` da yangi obyekt beradi, lekin Spring uni kuzatmaydi va `@PreDestroy` ni chaqirmaydi. Shu sababli prototype ichida resurs ochish xotira sizishiga olib keladi.

Eng nozik joy: prototype yoki request scope bean ni singleton ga to'g'ridan to'g'ri inject qilish. Singleton bir marta yaratilganda bir marta inject oladi, demak prototype bir martagina olinadi va amalda singleton ga aylanadi.

```java
@Service
public class ReportService {

    // Noto'g'ri: prototype faqat bir marta olinadi.
    // @Autowired private ReportBuffer buffer;

    // To'g'ri: har chaqiruvda yangi nusxa.
    private final ObjectProvider<ReportBuffer> bufferProvider;

    ReportService(ObjectProvider<ReportBuffer> bufferProvider) {
        this.bufferProvider = bufferProvider;
    }

    public byte[] build(long orderId) {
        ReportBuffer buffer = bufferProvider.getObject();
        try {
            return buffer.render(orderId);
        } finally {
            buffer.close();   // prototype ni O'ZIMIZ yopamiz
        }
    }
}

// Request scope ni singleton ga inject qilish uchun proxy shart.
@Component
@RequestScope   // ichida proxyMode = TARGET_CLASS
class CurrentUserContext { }
```

Request scope da yana bir tuzoq bor: `@Async` yoki `CompletableFuture` ichida request scope bean ga murojaat qilish `BeanCreationException` beradi, chunki yangi thread da request yo'q. Kerakli qiymatni asinxron ishga uzatishdan oldin oddiy obyektga ko'chirib olish kerak.

## 15.5 Bog'liqlikni kiritish usullari va nega konstruktor orqali kiritish afzal

Uch usul bor: konstruktor, setter va field. Konstruktor orqali kiritish yagona to'g'ri default. Sababi mexanik, estetik emas.

Konstruktor `final` field ga ruxsat beradi, demak dependency o'zgarmaydi va thread safe publication kafolatlanadi. Obyekt hamisha to'liq holatda tug'iladi. Parametrlar sonining o'sishi dizayn muammosini ko'rsatadigan ochiq signal, field inject esa buni yashiradi. Va konstruktor aylanma bog'liqlikni yashirmay, darhol oshkor qiladi.

| Vazifa | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Dependency kiritish | `@Autowired` field ga | konstruktor, `final` field |
| Dependency soni 8 ta bo'lsa | hammasini inject qilish | sinfni bo'lish, facade ajratish |
| Bir interfeys, ikki implementatsiya | `@Primary` bilan tezda yopish | `@Qualifier` yoki alohida tip bilan aniq ko'rsatish |
| Aylanma bog'liqlik | `allow-circular-references=true` | mas'uliyatni ajratish yoki event bilan uzish |
| Ishga tushish sekin | `lazy-initialization=true` yoqish | `/actuator/startup` bilan o'lchash, bean larni kamaytirish |
| Kesh ishlamayapti | `@Cacheable` ni ko'chirish | self-invocation ekanini tekshirish, chaqiruvni tashqariga olish |
| Event bilan ish | `@EventListener` da DB yozish | `@TransactionalEventListener(AFTER_COMMIT)` |
| Komponent skanerlash | ildiz paketdan hammasini | aniq paketlar va `@ConditionalOnProperty` |
| Prototype resursi | GC ga ishonish | `ObjectProvider` va qo'lda yopish |
| Shutdown | `@PreDestroy` ga tayanish | idempotent qayta ishlash, outbox orqali kafolat |

Setter inject faqat ixtiyoriy bog'liqlik uchun o'rinli. Field inject esa testda reflection talab qiladi va sinfni konteynerga mahkamlab qo'yadi.

## 15.6 Aylanma bog'liqlik: nega paydo bo'ladi, Spring Boot 3 da nega xato beradi

`OrderService` `PaymentService` ga, `PaymentService` esa `OrderService` ga muhtoj bo'lsa aylanma bog'liqlik paydo bo'ladi. Konstruktor orqali kiritishda Spring bu halqani uza olmaydi, chunki ikkisidan birini yaratish uchun ikkinchisi tayyor bo'lishi kerak. Field inject da Spring yarim yaratilgan obyektni "early reference" sifatida berib, halqani yashiradi va shu bilan muammoni ertaga suradi.

Spring Boot 2.6 dan boshlab `spring.main.allow-circular-references` default `false`, Spring Boot 3.x da ham shunday. Natijada kontekst `BeanCurrentlyInCreationException` bilan ko'tarilmaydi. Bu to'g'ri qaror: halqa doim mas'uliyat chegarasi noto'g'ri chizilganini ko'rsatadi.

```properties
# Bu flag ni yoqish muammoni yashiradi, yechmaydi.
# Faqat legacy kodni vaqtincha ishga tushirish uchun.
spring.main.allow-circular-references=false

# Ishga tushishni tezlashtirish, lekin xatolar runtime ga suriladi.
spring.main.lazy-initialization=false

# Spring Boot da default allaqachon true: hamma joyda CGLIB.
spring.aop.proxy-target-class=true

# Graceful shutdown: @PreDestroy ga real imkon beradi.
server.shutdown=graceful
spring.lifecycle.timeout-per-shutdown-phase=30s
```

Halqani uzishning uch yo'li bor: umumiy logikani uchinchi bean ga ajratish (narx hisobini `PricingCalculator` ga chiqarish), yo'nalishni event bilan teskari qilish (`PaymentService` `PaymentCompletedEvent` yuboradi), yoki kichik interfeys ajratib faqat kerakli shartnomani inject qilish. `@Lazy` bilan yopish ishlaydi lekin dizayn qarzini qoldiradi.

## 15.7 `@Lazy`, `@Primary`, `@Qualifier`, `@Conditional` qachon kerak

`@Lazy` bean ni birinchi murojaatga qadar yaratmaydi. U og'ir, kamdan kam ishlatiladigan bean uchun foydali, masalan yiliga bir marta ishlaydigan hisobot eksporteri. Lekin `@Lazy` xatoni ishga tushish vaqtidan birinchi so'rov vaqtiga suradi, ya'ni fail-fast ni yo'qotadi. Shuning uchun uni global yoqish emas, nuqtali qo'llash to'g'ri.

`@Primary` bir nechta nomzod bo'lganda default ni belgilaydi. `@Qualifier` esa chaqiruv joyida aniq tanlaydi. Qoida sodda: agar tanlov kontekstga bog'liq bo'lsa `@Qualifier`, agar haqiqatan bitta "asosiy" implementatsiya bo'lsa `@Primary`. Ikkisini aralashtirib ishlatish eng qiyin topiladigan konfiguratsiya xatolariga olib keladi.

```java
@Configuration
class GatewayConfig {

    // Asosiy provayder: boshqa joyda qualifier yozilmasa shu olinadi.
    @Bean
    @Primary
    PaymentGateway uzcardGateway(GatewayProperties props) {
        return new HttpPaymentGateway(props.uzcard());
    }

    // Faqat property yoqilgan bo'lsa yaratiladi: ortiqcha bean bo'lmaydi.
    @Bean
    @Qualifier("fallback")
    @ConditionalOnProperty(name = "payment.visa.enabled", havingValue = "true")
    PaymentGateway visaGateway(GatewayProperties props) {
        return new HttpPaymentGateway(props.visa());
    }

    // Test profilida haqiqiy HTTP ga chiqmaydigan stub.
    @Bean
    @ConditionalOnMissingBean(PaymentGateway.class)
    PaymentGateway noopGateway() {
        return new NoopPaymentGateway();
    }
}
```

`@Conditional` va uning Boot dagi shakllari (`@ConditionalOnProperty`, `@ConditionalOnMissingBean`, `@ConditionalOnClass`) definition bosqichida ishlaydi: shart bajarilmasa bean umuman ro'yxatga olinmaydi. Bu startup ni qisqartirishning eng arzon usuli. `@ConditionalOnMissingBean` tartibga sezgir, uni faqat auto-configuration ichida ishlatish kerak.

## 15.8 AOP mexanikasi: JDK dinamik proxy va CGLIB farqi

Spring AOP byte code ni o'zgartirmaydi, u proxy yasaydi. Ikki mexanizm bor. JDK dinamik proxy interfeys asosida ishlaydi va faqat interfeysda e'lon qilingan metodlarni ushlaydi. CGLIB esa sinfdan subclass yasaydi va metodlarni override qiladi.

| Jihat | JDK dinamik proxy | CGLIB |
|---|---|---|
| Talab | kamida bitta interfeys | nofinal sinf, nofinal metod |
| Nimani ushlaydi | interfeys metodlari | barcha public va protected metodlar |
| `final` sinf | muammo yo'q | proxy yasalmaydi, xato |
| `private` metod | ushlanmaydi | ushlanmaydi |
| Konstruktor | chaqirilmaydi | subclass konstruktori chaqiriladi |
| Tipga cast | faqat interfeysga | konkret sinfga ham |

Spring Boot da `spring.aop.proxy-target-class` default `true`, ya'ni CGLIB ishlatiladi hatto interfeys bo'lsa ham. Bu bilimsiz holda tuzoqqa aylanadi: agar kod `@Autowired` bilan interfeysni emas, konkret sinfni kutsa va boshqa joyda JDK proxy yasalgan bo'lsa, `BeanNotOfRequiredTypeException` chiqadi. Shuning uchun injection nuqtalarida interfeysga tayanish ishonchliroq.

Spring Framework 6.x da CGLIB qayta paketlangan holda ichida keladi. Lekin u `final` metodni override qila olmaydi, demak `@Transactional` qo'yilgan `final` metod jim tranzaksiyasiz ishlaydi. Kotlin da sinflar default `final` bo'lgani uchun bu muammo tez yuzaga keladi.

## 15.9 Proxy tuzog'i: ichki metod chaqiruvida `@Transactional` va `@Cacheable` ishlamasligi

Bu eng ko'p takrorlanadigan va eng jim o'tadigan xato. Proxy faqat tashqaridan kelgan chaqiruvni ushlaydi. Bir sinf ichida `this.method()` chaqirilsa, chaqiruv proxy dan o'tmaydi va annotatsiya butunlay e'tiborsiz qoladi. Kompilyator ogohlantirmaydi, test ham ko'pincha o'tadi.

```java
@Service
public class StockService {

    private final StockRepository repo;
    private final StockService self;   // o'ziga proxy orqali havola

    StockService(StockRepository repo, @Lazy StockService self) {
        this.repo = repo;
        this.self = self;
    }

    public void importBatch(List<StockRow> rows) {
        for (StockRow row : rows) {
            // NOTO'G'RI: this orqali, proxy chetlab o'tiladi,
            // REQUIRES_NEW ishlamaydi, hamma narsa bitta tranzaksiyada.
            // applyRow(row);

            // TO'G'RI: proxy orqali o'tadi, har qator alohida tranzaksiya.
            self.applyRow(row);
        }
    }

    @Transactional(propagation = Propagation.REQUIRES_NEW)
    public void applyRow(StockRow row) {
        repo.decrease(row.sku(), row.qty());
    }
}
```

Uch yechim bor va ularning narxi farq qiladi. Eng toza yechim mas'uliyatni ikki bean ga ajratish, chunki `importBatch` orkestratsiya, `applyRow` esa tranzaksional birlik va ular bir sinfda turishi majburiy emas. Ikkinchisi yuqoridagidek `@Lazy` self-injection, u ishlaydi lekin niyatni yashiradi. Uchinchisi `TransactionTemplate` ni to'g'ridan to'g'ri ishlatish, bu annotatsiyadan ko'ra ochiqroq va test qilish osonroq.

| Tuzoq | Nima sodir bo'ladi | Yechim |
|---|---|---|
| `this.method()` ichki chaqiruvi | annotatsiya e'tiborsiz, tranzaksiya yo'q | bean ni bo'lish yoki `TransactionTemplate` |
| `@Transactional` `private` metodda | proxy ushlamaydi, jim o'tadi | `public` qilish va tashqaridan chaqirish |
| `@Transactional` `final` metodda | CGLIB override qila olmaydi | `final` ni olib tashlash |
| `@PostConstruct` ichida `@Transactional` chaqiruvi | proxy hali tayyor emas | `ApplicationReadyEvent` da bajarish |
| `@Cacheable` o'sha sinf ichidan | kesh hamisha bo'sh, DB yuklanadi | chaqiruvni tashqi bean ga chiqarish |
| `@Async` metod `void` va exception | xato yo'qoladi | `CompletableFuture` qaytarish |
| Prototype singleton ichida | bir marta olinadi | `ObjectProvider` |
| Request scope `@Async` ichida | `BeanCreationException` | qiymatni oldin DTO ga ko'chirish |

Mavzuning to'liq yozuvi [transactional self-invocation](19-spring-tranzaksiyalari-va-ularning.md#196-ichki-metod-chaqiruvi-tuzogi-va-undan-chiqish-yollari) bo'limida; bu yerda faqat shu bo'limning nuqtai nazari.

## 15.10 `ApplicationEvent` va `@EventListener`: sinxron tabiati va tranzaksiya bilan bog'liqligi

`ApplicationEventPublisher.publishEvent()` default holda SINXRON. `SimpleApplicationEventMulticaster` listener larni chaqiruvchi thread da ketma-ket ishga tushiradi. Demak event yuborish "fire and forget" emas: listener sekin bo'lsa publisher kutadi, listener exception tashlasa publisher ham yiqiladi. Bu ko'pincha noto'g'ri tushuniladi va event lar yengil deb o'ylanadi.

Ikkinchi muhim nuqta tranzaksiya. Oddiy `@EventListener` hali ochiq tranzaksiya ichida ishlaydi. Agar listener email yuborsa yoki tashqi API ga chiqsa, keyin esa tranzaksiya rollback bo'lsa, email yuborilgan, lekin buyurtma yo'q. Bu klassik nomuvofiqlik.

```java
@Component
class PaymentNotifier {

    // Commit dan KEYIN ishlaydi: rollback bo'lsa umuman chaqirilmaydi.
    @TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
    public void onPaid(PaymentCompletedEvent e) {
        // Diqqat: bu yerdagi DB yozish yangi tranzaksiya talab qiladi.
        notifier.send(e.orderId());
    }

    // Asinxron: alohida thread, publisher kutmaydi.
    // Lekin xato publisher ga qaytmaydi, log qilish MAJBURIY.
    @Async
    @EventListener
    public void onAudit(PaymentCompletedEvent e) {
        auditLog.append(e);
    }
}
```

`AFTER_COMMIT` fazasida DB ga yozmoqchi bo'lsangiz, u avtomatik yangi tranzaksiyaga tushmaydi, shuning uchun `REQUIRES_NEW` ni aniq ko'rsatish kerak. Yuborish kafolati talab qilinsa, event emas, dizayn [patternlar hujjatidagi](../patterns/README.md) outbox yondashuvi to'g'ri, chunki `AFTER_COMMIT` dan keyin JVM o'lsa xabar yo'qoladi.

## 15.11 Ishga tushish vaqtini qisqartirish: ortiqcha bean va komponent skanerlash

Oddiy monolitda 3000 dan 8000 gacha bean bo'lishi mumkin va ishga tushish 15 sekunddan 60 sekundgacha cho'ziladi. Kubernetes da bu readiness probe va rolling update tezligiga to'g'ridan to'g'ri ta'sir qiladi. Birinchi qadam taxmin qilmaslik, o'lchash.

```bash
# 1. Startup qadamlarini yozib olish uchun actuator endpoint.
#    Config: BufferingApplicationStartup bean sifatida ro'yxatga olinadi.
curl -s localhost:8080/actuator/startup | jq \
  '.timeline.events | sort_by(-.duration) | .[0:15]
   | map({name: .startupStep.name, ms: (.duration | ltrimstr("PT"))})'

# 2. Auto-configuration hisobotini ko'rish: nima yoqilgan, nima yo'q.
java -jar app.jar --debug 2>&1 | sed -n '/Positive matches/,/Exclusions/p'

# 3. AOT bosqichini oldindan bajarish (Spring Boot 3.x).
./mvnw -Pnative spring-boot:process-aot

# 4. CDS arxivi: Spring Boot 3.3+ da ishga tushishni taxminan
#    30-40 foizga qisqartiradi.
java -XX:ArchiveClassesAtExit=app.jsa -Dspring.context.exit=onRefresh -jar app.jar
java -XX:SharedArchiveFile=app.jsa -jar app.jar
```

Eng katta g'oliblar quyidagilar. Komponent skanerlash doirasini toraytirish, ya'ni `@SpringBootApplication(scanBasePackages = ...)` bilan aniq paketlarni ko'rsatish, chunki ildiz paketdan skanerlash kutubxona paketlariga ham kirib ketadi. Keraksiz auto-configuration larni `spring.autoconfigure.exclude` bilan o'chirish. Ishlatilmaydigan starter larni `pom.xml` dan olib tashlash, ayniqsa bir nechta template engine yoki ikkita HTTP client qolgan loyihalarda.

Connection pool ham ta'sir qiladi: HikariCP da `minimum-idle` ni `maximum-pool-size` ga teng qo'yish start paytida barcha connection ni ochadi. Odatiy web servis uchun pool 10 dan 20 gacha yetarli, undan kattasi PostgreSQL tomonda zarar keltiradi.

`spring.main.lazy-initialization=true` ishga tushishni taxminan ikki baravar tezlashtiradi, lekin konfiguratsiya xatolari birinchi so'rovga suriladi. Shuning uchun uni faqat lokal development profilida yoqish mantiqiy, production da esa fail-fast qimmatliroq. Spring Framework 6.2 dan boshlab sekin bean larni fonda initsializatsiya qilish imkoni bor va u asosan tashqi ulanish kutadigan bean lar uchun foyda beradi.

## 15.12 Amalda qo'llash

- [ ] `/actuator/startup` ni `BufferingApplicationStartup` bilan yoqib, eng sekin 15 ta qadamni yozib ol va ishga tushish vaqtini bazaviy raqam sifatida qayd qil.
- [ ] Kod bazasida `@Transactional` va `@Cacheable` qo'yilgan barcha metodlarni tekshirib, ichki `this.` chaqiruvi orqali chaqirilayotganlarini top va chaqiruvni tashqariga chiqar.
- [ ] `final` yoki `private` metodda turgan `@Transactional`, `@Async`, `@Cacheable` annotatsiyalarini grep bilan izla va ularni tuzat, chunki ular jim ishlamayapti.
- [ ] `spring.main.allow-circular-references` ni `false` holatida qoldirib kontekstni ko'tar, chiqqan halqalarni `@Lazy` bilan yopmay, mas'uliyatni ajratib yech.
- [ ] Tashqi effekt beradigan (email, SMS, tashqi API) barcha `@EventListener` larni ko'rib chiq va ularni `@TransactionalEventListener(AFTER_COMMIT)` ga o'tkaz.
- [ ] `--debug` bilan auto-configuration hisobotini olib, ishlatilmaydigan starter larni va auto-configuration larni `spring.autoconfigure.exclude` bilan o'chir.
- [ ] `scanBasePackages` ni aniq paketlar ro'yxatiga qisqartirib, bean definition sonining oldin va keyingi farqini o'lchab yoz.
- [ ] `server.shutdown=graceful` va `spring.lifecycle.timeout-per-shutdown-phase` ni sozlab, Kubernetes grace period ini undan kattaroq qilib qo'y.

---

[&larr; 14. JVM profiling va diagnostika: JFR, async-profiler, heap dump](14-jvm-profiling-va-diagnostika-jfr-async.md) · [Mundarija](README.md) · [16. Spring Boot mexanikasi: auto-configuration, starter, Actuator &rarr;](16-spring-boot-mexanikasi-auto-configuration.md)
