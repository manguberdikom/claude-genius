<!-- doc: patterns | chapter: 5 | part:  -->

[Barcha hujjatlar](../../README.md) / [Dizayn patternlar](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 5. Spring Core ichidagi patternlar xaritasi (Patterns inside Spring Core)

<details>
<summary>Bu bo'limdagi 42 bo'lim</summary>

- [5.1 IoC konteyner (IoC Container - BeanFactory / ApplicationContext)](#51-ioc-konteyner-ioc-container---beanfactory--applicationcontext)
- [5.2 Bean definition va registry (Bean Definition & BeanDefinitionRegistry - Registry Pattern)](#52-bean-definition-va-registry-bean-definition--beandefinitionregistry---registry-pattern)
- [5.3 FactoryBean (FactoryBean - Abstract Factory)](#53-factorybean-factorybean---abstract-factory)
- [5.4 ObjectProvider va lazy lookup (ObjectProvider / Lazy Lookup)](#54-objectprovider-va-lazy-lookup-objectprovider--lazy-lookup)
- [5.5 @Lookup metod injeksiyasi (@Lookup Method Injection)](#55-lookup-metod-injeksiyasi-lookup-method-injection)
- [5.6 Bean scope'lari va scoped proxy (Bean Scopes & Scoped Proxy)](#56-bean-scopelari-va-scoped-proxy-bean-scopes--scoped-proxy)
- [5.7 @Lazy orqali kechiktirilgan initsializatsiya (@Lazy - Lazy Initialization / Virtual Proxy)](#57-lazy-orqali-kechiktirilgan-initsializatsiya-lazy---lazy-initialization--virtual-proxy)
- [5.8 @Primary / @Qualifier bilan noaniqlikni yechish (@Primary / @Qualifier Disambiguation)](#58-primary--qualifier-bilan-noaniqlikni-yechish-primary--qualifier-disambiguation)
- [5.9 Bean lifecycle callback'lari (Bean Lifecycle Callbacks - Template Method)](#59-bean-lifecycle-callbacklari-bean-lifecycle-callbacks---template-method)
- [5.10 BeanPostProcessor (BeanPostProcessor - Decorator / Interceptor)](#510-beanpostprocessor-beanpostprocessor---decorator--interceptor)
- [5.11 BeanFactoryPostProcessor va BeanDefinitionRegistryPostProcessor (BeanFactoryPostProcessor / BeanDefinitionRegistryPostProcessor)](#511-beanfactorypostprocessor-va-beandefinitionregistrypostprocessor-beanfactorypostprocessor--beandefinitionregistrypostprocessor)
- [5.12 Aware interfeyslari (Aware Interfaces - Callback Injection)](#512-aware-interfeyslari-aware-interfaces---callback-injection)
- [5.13 Lifecycle va SmartLifecycle (Lifecycle / SmartLifecycle)](#513-lifecycle-va-smartlifecycle-lifecycle--smartlifecycle)
- [5.14 SmartInitializingSingleton (SmartInitializingSingleton)](#514-smartinitializingsingleton-smartinitializingsingleton)
- [5.15 Tartiblash va ustuvorlik (Ordered / @Order)](#515-tartiblash-va-ustuvorlik-ordered--order)
- [5.16 Spring AOP: proxy asosidagi kesishuv (Spring AOP - Advice, Pointcut, Advisor, Interceptor)](#516-spring-aop-proxy-asosidagi-kesishuv-spring-aop---advice-pointcut-advisor-interceptor)
- [5.17 Tranzaksiya proxy'si va TransactionTemplate (@Transactional Proxy & TransactionTemplate)](#517-tranzaksiya-proxysi-va-transactiontemplate-transactional-proxy--transactiontemplate)
- [5.18 Template sinflari (Template Classes)](#518-template-sinflari-template-classes)
- [5.19 Callback interfeyslari (Callback Interfaces)](#519-callback-interfeyslari-callback-interfaces)
- [5.20 Ilova hodisalari (ApplicationEvent / @EventListener / @TransactionalEventListener)](#520-ilova-hodisalari-applicationevent--eventlistener--transactionaleventlistener)
- [5.21 Environment va PropertySource zanjiri (Environment & PropertySource Chain)](#521-environment-va-propertysource-zanjiri-environment--propertysource-chain)
- [5.22 Konfiguratsiya xossalarini bog'lash (@ConfigurationProperties Binding)](#522-konfiguratsiya-xossalarini-boglash-configurationproperties-binding)
- [5.23 Profillar (Profiles)](#523-profillar-profiles)
- [5.24 Shartli bean'lar va auto-konfiguratsiya (@Conditional & Auto-configuration)](#524-shartli-beanlar-va-auto-konfiguratsiya-conditional--auto-configuration)
- [5.25 Starter'lar (Starters)](#525-starterlar-starters)
- [5.26 Auto-konfiguratsiya SPI ro'yxati (AutoConfiguration.imports / spring.factories SPI)](#526-auto-konfiguratsiya-spi-royxati-autoconfigurationimports--springfactories-spi)
- [5.27 Resurs abstraksiyasi (Resource Abstraction)](#527-resurs-abstraksiyasi-resource-abstraction)
- [5.28 Konvertatsiya xizmati (ConversionService / Converter / Formatter)](#528-konvertatsiya-xizmati-conversionservice--converter--formatter)
- [5.29 Validator abstraksiyasi (Validator Abstraction)](#529-validator-abstraksiyasi-validator-abstraction)
- [5.30 Xabar manbasi va xalqarolashtirish (MessageSource / i18n)](#530-xabar-manbasi-va-xalqarolashtirish-messagesource--i18n)
- [5.31 Vazifa bajaruvchi va rejalashtiruvchi (TaskExecutor / TaskScheduler)](#531-vazifa-bajaruvchi-va-rejalashtiruvchi-taskexecutor--taskscheduler)
- [5.32 Tranzaksiya sinxronizatsiyasi (TransactionSynchronization)](#532-tranzaksiya-sinxronizatsiyasi-transactionsynchronization)
- [5.33 DataAccessException iyerarxiyasi va exception tarjimasi (DataAccessException Hierarchy / Exception Translation)](#533-dataaccessexception-iyerarxiyasi-va-exception-tarjimasi-dataaccessexception-hierarchy--exception-translation)
- [5.34 Cache abstraksiyasi (Cache Abstraction / @Cacheable Proxy)](#534-cache-abstraksiyasi-cache-abstraction--cacheable-proxy)
- [5.35 Spring Retry va @Retryable (Spring Retry / @Retryable)](#535-spring-retry-va-retryable-spring-retry--retryable)
- [5.36 Spring ifoda tili (Spring Expression Language / SpEL)](#536-spring-ifoda-tili-spring-expression-language--spel)
- [5.37 @Import, ImportSelector va registrar (@Import / ImportSelector / ImportBeanDefinitionRegistrar)](#537-import-importselector-va-registrar-import--importselector--importbeandefinitionregistrar)
- [5.38 Meta-annotatsiyalar va kompozit annotatsiyalar (Meta-annotations / Composed Annotations)](#538-meta-annotatsiyalar-va-kompozit-annotatsiyalar-meta-annotations--composed-annotations)
- [5.39 Konfiguratsiyadan ustun konvensiya (Convention over Configuration)](#539-konfiguratsiyadan-ustun-konvensiya-convention-over-configuration)
- [5.40 Spring'da Null Object qo'llanishi (Null Object Usage in Spring)](#540-springda-null-object-qollanishi-null-object-usage-in-spring)
- [5.41 Spring'dagi fluent DSL builder'lar (Fluent DSL Builders in Spring)](#541-springdagi-fluent-dsl-builderlar-fluent-dsl-builders-in-spring)
- [5.42 Amalda qo'llash](#542-amalda-qollash)

</details>



Spring Framework'ning o'zi - klassik dizayn patternlar katalogining ishlab chiqarishga tayyor, jangovar sinovdan o'tgan amaliy ko'rinishi: IoC konteyner Factory, Registry, Proxy, Template va Observer patternlarini bir necha qatlamda birlashtirib ishlatadi. Arxitektor uchun bu xarita muhim, chunki Spring'da "sehrli" ko'ringan har bir xususiyat ortida aniq nomlangan pattern va aniq extension point turadi. Shu xaritani bilgan injener bean yaratilish tartibini, startup muammolarini, circular dependency va proxy bilan bog'liq nozik xatolarni taxmin qilmasdan diagnostika qiladi. Eng muhimi - framework'ni "hack" qilmasdan, uning o'z kengaytirish nuqtalari orqali to'g'ri qatlamga ulanishni bilib oladi.

## 5.1 IoC konteyner (IoC Container - BeanFactory / ApplicationContext)

**Tavsif:** Obyektlarni kim yaratadi va kim ularning bog'liqliklarini uzatadi - bu mas'uliyatni ilova kodidan tashqi konteynerga ko'chiradi (Inversion of Control). Konteyner bean definition'lar katalogini o'qiydi, har bir bean'ning tip va bog'liqlik grafigini quradi, so'ng to'g'ri tartibda instantiate qilib, dependency'larni inject qiladi. `BeanFactory` - minimal lookup va lifecycle kontrakti, `ApplicationContext` esa uning ustiga event publishing, i18n, resource loading va annotation-based konfiguratsiyani qo'shadi. Natijada komponentlar bir-biriga emas, abstraksiyaga va konteyner kontraktiga bog'lanadi.

**Spring'da qayerda uchraydi:** `org.springframework.beans.factory.BeanFactory`, `ListableBeanFactory`, `HierarchicalBeanFactory`, `ConfigurableListableBeanFactory` va asosiy implementatsiya `DefaultListableBeanFactory`. Yuqori qatlamda `ApplicationContext` / `ConfigurableApplicationContext`, amalda `GenericApplicationContext`, `AnnotationConfigApplicationContext`, `ClassPathXmlApplicationContext`; Spring Boot 3.x/4.x web ilovada `AnnotationConfigServletWebServerApplicationContext` yoki reactive uchun `AnnotationConfigReactiveWebServerApplicationContext` (`SpringApplication.run()` tanlaydi). Parent-child context ierarxiyasi Spring MVC'da (root context + `DispatcherServlet` context) va Spring Cloud'da ishlatiladi; `@Configuration`, `@Bean`, `@ComponentScan`, `@Import` - konfiguratsiya metadatasi uchun asosiy annotatsiyalar.

**Qo'llanish keyslari:**
- Monolit Spring Boot ilovada barcha service, repository va infrastruktura bean'larini bitta `ApplicationContext` orqali boshqarish.
- Test'da `@SpringBootTest` yoki qo'lda `AnnotationConfigApplicationContext` bilan faqat kerakli slice'ni ko'tarish.
- Parent-child ierarxiya bilan umumiy infrastruktura bean'larini bir nechta izolyatsiyalangan modul context'lari orasida ulashish.
- Plugin arxitekturasida har bir plugin uchun alohida child context yaratib, uni to'liq `close()` qilib tashlash.
- CLI yoki batch jobda `SpringApplication` orqali context ko'tarib, ish tugagach graceful shutdown qilish.

**Ehtiyot bo'ling:** `ApplicationContext`'ni kod ichida `getBean()` uchun aylantirib yurish Service Locator anti-patterniga olib keladi - o'rniga constructor injection ishlatilsin. Katta ilovada bir nechta context ko'tarish (ayniqsa testlarda har xil konfiguratsiya bilan) context cache'ni buzadi va startup vaqtini ko'paytiradi.

```java
// Konteyner bean'ni qidiradi, yaratadi va bog'laydi - kod `new` ishlatmaydi
@SpringBootApplication
public class App {
    public static void main(String[] args) {
        ConfigurableApplicationContext ctx = SpringApplication.run(App.class, args);
        // getBean biznes kodda emas, faqat diagnostika uchun
        System.out.println(ctx.getBeanDefinitionCount() + " ta bean definition");
    }
}
```

## 5.2 Bean definition va registry (Bean Definition & BeanDefinitionRegistry - Registry Pattern)

**Tavsif:** Bean obyektning o'zi emas, balki uning "retsepti" - class nomi, scope, constructor argumentlari, property qiymatlari, init/destroy method nomlari, lazy va primary flag'lari - alohida metadata obyektida saqlanadi. Bu metadata markaziy registry'da nom bo'yicha saqlanadi va instantiate qilishdan oldin o'zgartirilishi mumkin. Shu ajratish tufayli konfiguratsiya manbasi (annotation, XML, Groovy, programmatik kod, AOT metadata) bean yaratish mexanizmidan mustaqil bo'ladi. Registry - nom bo'yicha retseptni qidirish va ro'yxatga olish uchun yagona kontrakt.

**Spring'da qayerda uchraydi:** `BeanDefinition` interfeysi va implementatsiyalari: `GenericBeanDefinition`, `RootBeanDefinition`, `ChildBeanDefinition`, `AnnotatedGenericBeanDefinition`, `ScannedGenericBeanDefinition`. Registry tomoni: `BeanDefinitionRegistry` (uni `DefaultListableBeanFactory` va `GenericApplicationContext` implement qiladi), yordamchilar `BeanDefinitionBuilder`, `BeanDefinitionReaderUtils`, `AbstractBeanDefinitionReader`, `ClassPathBeanDefinitionScanner`. Dinamik ro'yxatga olish uchun `ImportBeanDefinitionRegistrar` (masalan `@EnableJpaRepositories`, `@MapperScan`) va `BeanDefinitionRegistryPostProcessor`; Spring Framework 7.0'da programmatik ro'yxatga olish uchun `BeanRegistrar` API, Spring Boot 3.x AOT'da esa `BeanRegistrationAotProcessor` definition'larni compile-time kodga aylantiradi.

**Qo'llanish keyslari:**
- Spring Data'ga o'xshash starter yozib, interfeyslarni skanerlab har biri uchun proxy bean definition ro'yxatga olish.
- `@ConditionalOnProperty` asosida bir xil tipdagi bean'larni (masalan ko'p tenant uchun `DataSource`) dinamik generatsiya qilish.
- Legacy XML konfiguratsiyasini annotation'ga ko'chirishda ikkalasini bitta registry'da birlashtirish.
- Definition darajasida `setPrimary(true)` yoki `setLazyInit(true)` qo'yib, mavjud auto-configuration xatti-harakatini o'zgartirish.
- Testda bean definition'ni almashtirib (`@MockitoBean` yoki qo'lda `registerBeanDefinition`) real infrastrukturani stub bilan almashtirish.

**Ehtiyot bo'ling:** Registry'ni context `refresh()` tugagandan keyin o'zgartirish xavfli - singleton'lar allaqachon yaratilgan bo'lishi mumkin va metadata bilan real holat farq qiladi. Bir xil bean nomi bilan qayta ro'yxatga olish jim turib override qilishi mumkin; Spring Boot'da `spring.main.allow-bean-definition-overriding` standart holda `false` - buni yoqish o'rniga nomlarni aniq boshqarish kerak.

```java
// Bean definition - retsept, bean - natija. Retseptni programmatik qo'shish:
@Component
class DynamicHandlers implements BeanDefinitionRegistryPostProcessor {
    @Override
    public void postProcessBeanDefinitionRegistry(BeanDefinitionRegistry registry) {
        for (String channel : List.of("sms", "email")) {
            registry.registerBeanDefinition("notifier-" + channel,
                    BeanDefinitionBuilder.genericBeanDefinition(Notifier.class)
                            .addConstructorArgValue(channel)
                            .getBeanDefinition());
        }
    }
}
```

## 5.3 FactoryBean (FactoryBean - Abstract Factory)

**Tavsif:** Ba'zi obyektlarni oddiy constructor bilan yaratish mumkin emas: ular murakkab builder, JNDI lookup yoki proxy generatsiyasini talab qiladi. `FactoryBean` - konteyner ichida yashovchi fabrika bean: konteyner uni o'zini yaratadi, lekin boshqa bean'larga uning `getObject()` natijasini inject qiladi. Shu bilan murakkab yaratish logikasi konfiguratsiyadan va iste'molchi koddan to'liq yashiriladi. Haqiqiy fabrika obyektining o'ziga kerak bo'lsa, bean nomi oldiga `&` prefiksi qo'yiladi.

**Spring'da qayerda uchraydi:** `org.springframework.beans.factory.FactoryBean<T>` (`getObject()`, `getObjectType()`, `isSingleton()`), `SmartFactoryBean`, qulaylik uchun `AbstractFactoryBean<T>`. Keng tarqalgan implementatsiyalar: JPA uchun `LocalContainerEntityManagerFactoryBean`, Hibernate uchun `LocalSessionFactoryBean`, AOP'da `ProxyFactoryBean`, `JndiObjectFactoryBean`, `MethodInvokingFactoryBean`, `ServiceLocatorFactoryBean`, MyBatis'dagi `SqlSessionFactoryBean` va `MapperFactoryBean`. Spring Boot JPA auto-configuration (`HibernateJpaConfiguration`) aynan `LocalContainerEntityManagerFactoryBean`ni bean sifatida e'lon qiladi, shuning uchun `EntityManagerFactory` inject qilinadi.

**Qo'llanish keyslari:**
- Tashqi kutubxonaning builder-only client'ini (masalan gRPC yoki SDK client) Spring bean sifatida taqdim etish.
- Konfiguratsiyaga qarab bir necha implementatsiyadan birini tanlab qaytaruvchi yagona bean nuqtasi yaratish.
- Interfeys asosida dinamik proxy generatsiya qilib, uni repository yoki client bean sifatida registratsiya qilish.
- Legacy JNDI yoki tashqi resursni lookup qilib, qolgan kodga oddiy tip sifatida ko'rsatish.
- Og'ir, bir marta yaratiladigan obyekt (connection pool, `EntityManagerFactory`) uchun yaratish va validatsiya logikasini bir joyga yig'ish.

**Ehtiyot bo'ling:** `getObjectType()` `null` qaytarsa yoki noto'g'ri tip bersa, by-type autowiring buziladi va `FactoryBean` erta instantiate qilinib startup tartibini o'zgartiradi. Oddiy holatlarda `@Bean` metodi ancha sodda va o'qishga qulay - `FactoryBean` faqat tip dinamik yoki proxy generatsiya kerak bo'lganda oqlanadi.

```java
// FactoryBean: bean yaratish mantig'i murakkab bo'lganda
@Component("pspClient")
class PspClientFactoryBean implements FactoryBean<PspClient> {
    private final PspProperties props;
    PspClientFactoryBean(PspProperties props) { this.props = props; }

    @Override public PspClient getObject() { return PspClient.connect(props.url()); }
    @Override public Class<?> getObjectType() { return PspClient.class; }
}
// Inject qilinganda PspClient keladi, FactoryBean emas.
// FactoryBean'ning o'zi kerak bo'lsa: ctx.getBean("&pspClient")
// Zamonaviy alternativa: oddiy @Bean metodi
```

## 5.4 ObjectProvider va lazy lookup (ObjectProvider / Lazy Lookup)

**Tavsif:** Bean'ni darhol emas, kerak bo'lgan paytda olish, yoki umuman bo'lmasa ham ishlashga chidash kerak bo'ladi. `ObjectProvider` injection point'ga obyektning o'zi emas, unga indirection beruvchi handle uzatadi: mavjudligini tekshirish, bir nechtasini stream sifatida olish yoki argument bilan prototype yaratish mumkin. Bu optional dependency'ni `null` bilan emas, tipli API bilan ifodalaydi. Qo'shimcha foyda - singleton ichida har safar yangi prototype olish va circular dependency'ni uzish.

**Spring'da qayerda uchraydi:** `org.springframework.beans.factory.ObjectProvider<T>` (`ObjectFactory<T>` kengaytmasi): `getIfAvailable()`, `getIfUnique()`, `getObject(Object... args)`, `stream()`, `orderedStream()`; programmatik olish `BeanFactory.getBeanProvider(Class)`. Standart alternativa - `jakarta.inject.Provider<T>` (Spring Framework 6.x `jakarta` namespace'ida). Spring Boot auto-configuration'larida bu idiomatik usul: ko'p `*AutoConfiguration` klasslari customizer va optional komponentlarni `ObjectProvider` orqali qabul qiladi (masalan `ObjectProvider<HttpMessageConverters>`, `ObjectProvider<RestClientCustomizer>`), `orderedStream()` esa `@Order`/`Ordered` bo'yicha tartiblangan ro'yxat beradi.

**Qo'llanish keyslari:**
- Starter yozishda optional customizer'larni qabul qilish: bor bo'lsa qo'llanadi, yo'q bo'lsa default ishlaydi.
- Singleton service ichida har murojaatda yangi prototype bean (masalan stateful command obyekt) olish.
- Bir nechta strategiya implementatsiyasini `orderedStream()` bilan tartiblangan pipeline sifatida yig'ish.
- Og'ir bean'ni faqat tegishli kod yo'li ishga tushganda yaratish, startup vaqtini qisqartirish.
- Ikki bean orasidagi circular dependency'ni to'g'ridan-to'g'ri injection o'rniga provider bilan uzish.

**Ehtiyot bo'ling:** `ObjectProvider`ni hamma joyda ishlatish kodni Spring API'siga bog'laydi va dependency grafigini yashirin qiladi - majburiy bog'liqlik uchun oddiy constructor injection qolsin. `getIfAvailable()` bilan jim `null` qaytarish, konfiguratsiya xatosini startup'da emas, runtime'da yuzaga chiqarish xavfini tug'diradi.

```java
// ObjectProvider: bean bor-yo'qligi noma'lum yoki har chaqiruvda yangi kerak
@Service
public class ReportService {
    private final ObjectProvider<PdfRenderer> renderers;   // prototype bean

    public ReportService(ObjectProvider<PdfRenderer> renderers) { this.renderers = renderers; }

    public byte[] render(Report r) {
        PdfRenderer renderer = renderers.getObject();      // har chaqiruvda yangi nusxa
        return renderer.render(r);
    }
}
// getIfAvailable() - bean yo'q bo'lsa null; getIfUnique() - bir nechta bo'lsa null
```

## 5.5 @Lookup metod injeksiyasi (@Lookup Method Injection)

**Tavsif:** Singleton bean ichida har safar yangi prototype instance kerak bo'lganda, oddiy field injection ishlamaydi - u faqat bir marta inject qilinadi. `@Lookup` konteynerga aytadi: bu metodni CGLIB subclass orqali override qilib, har chaqiruvda `getBean()` natijasini qaytar. Natijada iste'molchi kod `BeanFactory`ga bog'lanmaydi, abstrakt metodning o'zi factory rolini bajaradi. Bu klassik Service Locator'ning deklarativ, konteyner tomonidan amalga oshiriladigan varianti.

**Spring'da qayerda uchraydi:** `org.springframework.beans.factory.annotation.Lookup`, uni `AutowiredAnnotationBeanPostProcessor` qayta ishlaydi va CGLIB subclass generatsiya qiladi. XML dunyosidagi ekvivalenti - `<lookup-method>` (`LookupOverride`) va yaqin qarindoshi `<replaced-method>` (`MethodReplacer`, `ReplaceOverride`). Amalda bu yondashuv `ObjectProvider` bilan almashtirilishi mumkin, Spring'ning o'z kodida esa prototype-ga bog'liq singleton'lar uchun tarixiy mexanizm sifatida qoladi.

```java
@Component
public abstract class ReportRunner {
    public String run(ReportRequest req) {
        return createTask().execute(req); // har chaqiruvda yangi instance
    }
    @Lookup
    protected abstract ReportTask createTask(); // @Scope("prototype") bean
}
```

**Qo'llanish keyslari:**
- Singleton orchestrator ichida har request uchun yangi stateful task obyektini olish.
- Legacy abstract factory metodini `BeanFactory`ni inject qilmasdan Spring bean'ga aylantirish.
- Har safar yangi `StringBuilder`-ga o'xshash mutable helper yoki yangi connection wrapper olish.
- Testda abstract metodni oddiy override qilib, konteynersiz ham sinovdan o'tkazish.
- XML'dan annotation'ga migratsiyada `<lookup-method>` konfiguratsiyasini kodga ko'chirish.

**Ehtiyot bo'ling:** Metod `final` yoki `private` bo'lsa, class `final` bo'lsa yoki bean `new` bilan yaratilib qo'lda registratsiya qilinsa, CGLIB override ishlamaydi va metod jim turib asl holatida qoladi. Zamonaviy kodda `ObjectProvider<T>` yoki oddiy `@Bean` factory metodi aniqroq va GraalVM native image'da kamroq muammo keltiradi.

## 5.6 Bean scope'lari va scoped proxy (Bean Scopes & Scoped Proxy)

**Tavsif:** Bean definition bitta bo'lsa ham, uning nechta instance'i va qancha yashashi ortogonal masala - scope aynan shu hayot muddatini belgilaydi. Singleton context bilan, prototype har murojaatda, request/session esa web so'rovi yoki foydalanuvchi sessiyasi bilan bog'lanadi. Qisqa umrli bean'ni uzoq umrli bean'ga to'g'ridan-to'g'ri inject qilish mumkin emas, shuning uchun konteyner o'rtaga scoped proxy qo'yadi: proxy singleton sifatida inject qilinadi, lekin har chaqiruvda joriy scope'dagi haqiqiy instance'ni topib, unga delegate qiladi.

**Spring'da qayerda uchraydi:** `@Scope` annotatsiyasi va konstantalar `ConfigurableBeanFactory.SCOPE_SINGLETON` / `SCOPE_PROTOTYPE`, web scope'lar `WebApplicationContext.SCOPE_REQUEST` / `SCOPE_SESSION` / `SCOPE_APPLICATION`; qulay meta-annotatsiyalar `@RequestScope`, `@SessionScope`, `@ApplicationScope`. Proxy tomoni: `@Scope(proxyMode = ScopedProxyMode.TARGET_CLASS | INTERFACES)`, `ScopedProxyFactoryBean`, `ScopedProxyUtils`. Custom scope uchun `org.springframework.beans.factory.config.Scope` interfeysi va `CustomScopeConfigurer`; mavjud misollar `SimpleThreadScope`, Spring Cloud Context'dagi `@RefreshScope`. Web scope'lar ishlashi uchun `RequestContextFilter`/`RequestContextListener` yoki `DispatcherServlet` kerak (Spring Boot buni avtomatik sozlaydi).

**Qo'llanish keyslari:**
- Joriy foydalanuvchi yoki tenant kontekstini `@RequestScope` bean'ga yig'ib, scoped proxy orqali singleton service'larga inject qilish.
- Checkout savatchasi kabi foydalanuvchiga xos holatni `@SessionScope` bean'da saqlash.
- Spring Cloud Config yangilanganda `@RefreshScope` bilan konfiguratsiyaga bog'liq bean'larni qayta yaratish.
- Prototype scope bilan har safar toza stateful validator yoki parser instance'ini olish.
- Batch yoki messaging pipeline uchun custom scope yozib, har job ichida resurs izolyatsiyasini ta'minlash.

**Ehtiyot bo'ling:** Request/session scoped bean'ga proxy orqali `@Async` thread yoki `@Scheduled` job ichida murojaat qilish `No thread-bound request found` xatosini beradi - scope kontekstini thread'lar o'rtasida o'zi ko'chirmaydi. Prototype bean'lar uchun konteyner destroy callback'larini chaqirmaydi, shuning uchun ularda resurs ochib qoldirish memory leak'ka olib keladi.

```java
// Request scope'dagi bean singleton ichiga inject qilinsa, proxy shart
@Bean
@RequestScope                       // = @Scope(value = "request", proxyMode = TARGET_CLASS)
RequestContext requestContext() {
    return new RequestContext();
}

@Service
class AuditService {
    private final RequestContext ctx;    // proxy inject qilinadi
    AuditService(RequestContext ctx) { this.ctx = ctx; }
    // Har chaqiruvda proxy joriy so'rovning haqiqiy nusxasini topadi
}
```

## 5.7 @Lazy orqali kechiktirilgan initsializatsiya (@Lazy - Lazy Initialization / Virtual Proxy)

**Tavsif:** Standart holda singleton bean'lar context refresh paytida darhol yaratiladi; bu startup'da barcha konfiguratsiya xatolarini ochadi, lekin og'ir bean'lar uchun qimmat. `@Lazy` bean yaratilishini birinchi real murojaatgacha kechiktiradi. Injection point'da qo'yilganda esa Spring o'rtaga lazy resolution proxy qo'yadi: proxy darhol inject qilinadi, haqiqiy bean esa ilk metod chaqirilganda yaratiladi. Bu Virtual Proxy patterning konteyner darajasidagi ko'rinishi.

**Spring'da qayerda uchraydi:** `org.springframework.context.annotation.Lazy` - `@Component`, `@Bean`, `@Configuration` klassida yoki injection point'da (constructor parametri, field, `@Autowired` metodi) ishlatiladi; proxy generatsiyasini `ContextAnnotationAutowireCandidateResolver` boshqaradi. Butun ilova darajasida Spring Boot 3.x/4.x'da `spring.main.lazy-initialization=true`, undan ayrim bean'larni ajratib olish uchun `LazyInitializationExcludeFilter` bean'i. `@ComponentScan(lazyInit = true)` ham mavjud; `@Lazy(false)` esa global lazy rejimda aniq bean'ni eager qilib qaytaradi.

**Qo'llanish keyslari:**
- Lokal development va test'da `spring.main.lazy-initialization=true` bilan startup vaqtini keskin qisqartirish.
- Faqat kamdan-kam ishlatiladigan admin yoki migration yo'lida kerak bo'ladigan og'ir client'ni kechiktirish.
- Tashqi tizimga ulanish startup'da mavjud bo'lmasligi mumkin bo'lgan integratsiya bean'ini lazy qilish.
- Ikki bean orasidagi konstruktor circular dependency'ni injection point'da `@Lazy` bilan uzish.
- Ko'p profilli monolitda faqat ayrim profilda ishlatiladigan modul bean'larini talab bo'yicha ko'tarish.

**Ehtiyot bo'ling:** Lazy rejim konfiguratsiya xatolarini startup'dan birinchi so'rovga ko'chiradi - production'da bu "healthy" ko'ringan, lekin ilk trafikda yiqiladigan ilova degani. `@Scheduled`, `@EventListener`, `Lifecycle` va metrikalarni ro'yxatga oluvchi bean'lar lazy bo'lsa, ular hech qachon ishga tushmay qolishi mumkin.

```java
@Service
public class SearchService {
    private final SearchIndex index;

    // @Lazy: bean faqat birinchi chaqiruvda yaratiladi, bu yerda proxy keladi
    public SearchService(@Lazy SearchIndex index) { this.index = index; }
}

// Butun ilova uchun (faqat dev profilda):
// spring.main.lazy-initialization=true
// Production'da u konfiguratsiya xatosini startup'dan birinchi so'rovga ko'chiradi.
```

## 5.8 @Primary / @Qualifier bilan noaniqlikni yechish (@Primary / @Qualifier Disambiguation)

**Tavsif:** Bir tipdan bir nechta bean bo'lsa, by-type autowiring noaniq bo'lib qoladi va konteyner xato beradi. `@Primary` "teng bo'lsa, standart sifatida shuni ol" deydi, `@Qualifier` esa injection point'da aniq nomli yoki meta-annotatsiyali kandidatni tanlaydi. Bu Strategy patternni konfiguratsiya darajasida boshqarish usuli: implementatsiyalar ko'p, tanlov esa deklarativ. To'g'ri qo'llanganda kod `if/else` va factory switch'lardan xoli bo'ladi.

**Spring'da qayerda uchraydi:** `@Primary`, `@Qualifier` (`org.springframework.beans.factory.annotation`), `@Qualifier` bilan meta-annotatsiyalangan custom annotatsiyalar (masalan o'zingizning `@Fast`, `@Audit`), ro'yxat injeksiyasida tartib uchun `@Order` / `Ordered` / `@Priority`. Spring Framework 6.2'dan: `@Fallback` (faqat boshqa kandidat bo'lmasa tanlanadi) va `@Bean(defaultCandidate = false)` - bean'ni by-type tanlovdan chiqarib, faqat qualifier bilan olish mumkin. Noaniqlik xatosi `NoUniqueBeanDefinitionException`, bean yo'qligi `NoSuchBeanDefinitionException`; Spring Boot auto-configuration'lari esa `@ConditionalOnMissingBean` va `@Primary` kombinatsiyasi bilan foydalanuvchi bean'iga yo'l beradi.

**Qo'llanish keyslari:**
- Bir nechta `DataSource` bo'lganda asosiysini `@Primary` qilib, qolganlarini `@Qualifier("reporting")` bilan olish.
- `ObjectMapper`ning umumiy va maxsus (snake_case, legacy) variantlarini bir contextda yashashi.
- Custom qualifier annotatsiya yozib, payment provider strategiyalarini tip-xavfsiz tanlash.
- Starter yozishda default bean'ni `@Fallback` yoki `@ConditionalOnMissingBean` bilan berib, foydalanuvchiga override imkonini qoldirish.
- Bir nechta `TaskExecutor` yoki `TransactionManager` bo'lganda har bir qo'llanish joyini aniq qualifier bilan bog'lash.

**Ehtiyot bo'ling:** Bir tipdan ikkita `@Primary` bo'lishi startup'da xato beradi, `@Primary`ga ortiqcha tayanish esa noto'g'ri bean jim turib inject qilinishiga olib keladi - kritik joylarda aniq `@Qualifier` yozish xavfsizroq. `@Qualifier` qiymati sifatida bean nomini string ko'rinishida tarqatish refactoring'da sinadi; meta-annotatsiya yoki konstanta ishlatish ma'qul.

```java
public interface PaymentGateway { Receipt charge(Payment p); }

@Component("psp") @Primary          // default tanlov
class PspGateway implements PaymentGateway { /* ... */ }

@Component("mock")
class MockGateway implements PaymentGateway { /* ... */ }

@Service
class Checkout {
    private final PaymentGateway gateway;
    // @Qualifier @Primary dan ustun turadi
    Checkout(@Qualifier("mock") PaymentGateway gateway) { this.gateway = gateway; }
}
```

## 5.9 Bean lifecycle callback'lari (Bean Lifecycle Callbacks - Template Method)

**Tavsif:** Bean to'liq inject qilingandan keyin ba'zan validatsiya, cache isitish yoki resurs ochish kerak; context yopilganda esa ularni toza yopish lozim. Konteyner shu uchun belgilangan nuqtalarda bean'ning o'z metodlarini chaqiradi - bu Template Method patterning lifecycle versiyasi: skeletni konteyner boshqaradi, "bo'shliqni" bean to'ldiradi. Chaqirilish tartibi qat'iy: `@PostConstruct` → `InitializingBean.afterPropertiesSet()` → `@Bean(initMethod)`, destroy tomonda esa `@PreDestroy` → `DisposableBean.destroy()` → `@Bean(destroyMethod)`.

**Spring'da qayerda uchraydi:** `InitializingBean`, `DisposableBean`, `jakarta.annotation.PostConstruct` / `jakarta.annotation.PreDestroy` (Spring Framework 6.x'da `javax` emas, `jakarta`), `@Bean(initMethod = "...", destroyMethod = "...")`. Annotatsiyalarni `CommonAnnotationBeanPostProcessor` qayta ishlaydi, destroy tomonini `DestructionAwareBeanPostProcessor` va `DisposableBeanAdapter` boshqaradi. `@Bean` uchun `destroyMethod` standart holda inferred: bean `AutoCloseable` yoki `close()`/`shutdown()` metodiga ega bo'lsa avtomatik chaqiriladi (`destroyMethod = ""` bilan o'chiriladi). Spring Boot'da context yopilishi `SpringApplication` registratsiya qilgan shutdown hook orqali sodir bo'ladi.

**Qo'llanish keyslari:**
- Startup'da konfiguratsiya qiymatlarini validatsiya qilib, noto'g'ri bo'lsa darhol fail-fast qilish.
- Connection pool, file channel yoki native resursni ochish va context yopilganda yopish.
- In-memory cache yoki lookup jadvalini birinchi so'rovdan oldin to'ldirish.
- Tashqi registry'ga (service discovery, JMX) o'zini ro'yxatdan o'tkazish va chiqishda o'chirish.
- Legacy komponentning `init()` / `cleanup()` metodlarini kodga qo'l tekizmasdan `@Bean` orqali ulash.

**Ehtiyot bo'ling:** Prototype scope bean'larda destroy callback'lari umuman chaqirilmaydi - ularni yopish mas'uliyati chaqiruvchida qoladi. `@PostConstruct` ichida og'ir I/O yoki boshqa bean'ga murojaat qilish startup'ni sekinlashtiradi va initsializatsiya tartibiga yashirin bog'liqlik yaratadi; proxy bilan o'ralgan bean'da bu callback target obyektda ishlaydi, shuning uchun u yerdan o'z-o'ziga chaqiruv AOP'ni chetlab o'tadi.

```java
@Component
public class IndexWarmer {

    @PostConstruct                  // inject tugagandan keyin
    void warmUp() {
        // TUZOQ: bu yerda tashqi chaqiruv startup'ni va readiness probe'ni ushlaydi
        cache.preload();
    }

    @PreDestroy                     // kontekst yopilishidan oldin
    void flush() {
        cache.flushToDisk();
    }
}
// Ketma-ketlik: konstruktor -> @Autowired setter -> Aware -> @PostConstruct
//              -> InitializingBean.afterPropertiesSet -> @Bean(initMethod)
```

## 5.10 BeanPostProcessor (BeanPostProcessor - Decorator / Interceptor)

**Tavsif:** Konteyner yaratgan har bir bean'ni, uning kodini o'zgartirmasdan, yaratilish paytida ushlab turib boyitish yoki proxy bilan o'rash mumkin. `BeanPostProcessor` initsializatsiyadan oldin va keyin chaqiriladi va `postProcessAfterInitialization()` butunlay boshqa obyekt - masalan proxy - qaytarishi mumkin. Spring'ning annotation'ga asoslangan deyarli barcha sehri shu nuqtada tug'iladi: `@Transactional`, `@Async`, `@Cacheable` proxy'lari aynan shu yerda o'raladi. Bu Decorator patterning konteyner darajasida, global va deklarativ ko'rinishi.

**Spring'da qayerda uchraydi:** `BeanPostProcessor` va kengaytmalari `InstantiationAwareBeanPostProcessor`, `SmartInstantiationAwareBeanPostProcessor`, `MergedBeanDefinitionPostProcessor`, `DestructionAwareBeanPostProcessor`. Framework'ning o'z implementatsiyalari: `AutowiredAnnotationBeanPostProcessor`, `CommonAnnotationBeanPostProcessor`, `ApplicationContextAwareProcessor`, `AbstractAutoProxyCreator` / `AnnotationAwareAspectJAutoProxyCreator`, `AsyncAnnotationBeanPostProcessor`, `ScheduledAnnotationBeanPostProcessor`, `PersistenceAnnotationBeanPostProcessor`; Spring Boot'da `ConfigurationPropertiesBindingPostProcessor`. Tartib `PriorityOrdered` / `Ordered` bilan boshqariladi, ro'yxatga olish `ConfigurableBeanFactory.addBeanPostProcessor()` yoki oddiy bean e'loni orqali bo'ladi.

**Qo'llanish keyslari:**
- Custom annotatsiya yozib (masalan `@Retryable` yoki `@Audited`), unga mos bean'larni proxy bilan o'rash.
- Barcha bean'larni skanerlab, metrika yoki tracing instrumentatsiyasini avtomatik qo'shish.
- Ma'lum tipdagi bean'larga startup'da qo'shimcha konfiguratsiya yoki validatsiya qo'llash.
- Uchinchi tomon kutubxonasi bean'ini kodini o'zgartirmasdan decorator bilan o'rab, xatti-harakatini moslashtirish.
- `@ConfigurationProperties` bean'lariga qo'shimcha dekripsiya yoki normalizatsiya qadamini ulash.

**Ehtiyot bo'ling:** `BeanPostProcessor`'ning o'zi boshqa bean'larni inject qilsa, ular juda erta instantiate qilinadi va boshqa post-processor'lardan (masalan AOP proxy'dan) chetda qolib ketadi - bog'liqliklarni `ObjectProvider` yoki `BeanFactoryAware` orqali kechiktirib olish kerak. Shuningdek har bir bean uchun chaqirilgani sababli, ichida sekin logika yozish butun startup'ni sezilarli sekinlashtiradi.

```java
// BeanPostProcessor: har bean yaratilganda aralashish imkoni
@Component
class TimingBeanPostProcessor implements BeanPostProcessor {
    @Override
    public Object postProcessAfterInitialization(Object bean, String name) {
        if (!(bean instanceof PaymentGateway g)) return bean;
        // bean'ni proxy bilan o'rab qaytarish - Spring AOP ham shunday ishlaydi
        return (PaymentGateway) p -> {
            long t0 = System.nanoTime();
            try { return g.charge(p); }
            finally { log.info("{} {} ns", name, System.nanoTime() - t0); }
        };
    }
}
```

## 5.11 BeanFactoryPostProcessor va BeanDefinitionRegistryPostProcessor (BeanFactoryPostProcessor / BeanDefinitionRegistryPostProcessor)

**Tavsif:** Ba'zi o'zgarishlarni bean yaratilgandan keyin emas, undan oldin - metadata darajasida qilish kerak. `BeanFactoryPostProcessor` barcha definition'lar o'qilgandan, lekin birorta singleton yaratilmasdan oldin chaqiriladi va definition'larni erkin o'zgartirishga ruxsat beradi. `BeanDefinitionRegistryPostProcessor` undan ham ilgari ishlaydi va yangi definition'lar qo'shish imkonini beradi. Shu ikkita nuqta Spring'ning plugin va starter ekotizimining asosiy kirish eshigi hisoblanadi.

**Spring'da qayerda uchraydi:** `BeanFactoryPostProcessor.postProcessBeanFactory(ConfigurableListableBeanFactory)` va `BeanDefinitionRegistryPostProcessor.postProcessBeanDefinitionRegistry(BeanDefinitionRegistry)`. Eng muhim implementatsiya - `ConfigurationClassPostProcessor`, ya'ni `@Configuration`/`@Bean`/`@Import`/`@ComponentScan` ni qayta ishlovchi dvigatel. Boshqalari: `PropertySourcesPlaceholderConfigurer` (`${...}` placeholder'lar), `PropertyOverrideConfigurer`, `CustomScopeConfigurer`, `EventListenerMethodProcessor`; ekotizimda MyBatis'ning `MapperScannerConfigurer`, Spring Data'ning repository registrar infratuzilmasi. `@Configuration` klassi ichida e'lon qilinsa, metod albatta `static @Bean` bo'lishi kerak.

**Qo'llanish keyslari:**
- Interfeyslarni skanerlab, har biri uchun client yoki repository bean definition'ini generatsiya qiluvchi starter yozish.
- Mavjud auto-configuration bean'ining definition'iga `setPrimary`, `setLazyInit` yoki qo'shimcha property qo'yib moslashtirish.
- Property manbasini (Vault, KMS, tashqi config server) placeholder resolution'dan oldin ulash.
- Custom scope'ni `CustomScopeConfigurer` orqali ro'yxatga olish.
- Ko'p tenant arxitekturasida tenant ro'yxatiga qarab har biri uchun bir to'plam bean definition yaratish.

**Ehtiyot bo'ling:** Bu processor'lar ichida `getBean()` chaqirish bean'larni muddatidan oldin yaratadi va boshqa post-processing qadamlarini chetlab o'tadi - faqat metadata bilan ishlash kerak. `@Configuration` klassida `static` bo'lmagan `@Bean` metodi sifatida e'lon qilinsa, butun konfiguratsiya klassi juda erta instantiate qilinadi va `@Autowired` hamda placeholder resolution ishlamay qolishi mumkin.

```java
// BeanFactoryPostProcessor: bean'lar yaratilishidan OLDIN definition'ni o'zgartirish
@Component
class ForceLazyRepositories implements BeanFactoryPostProcessor {
    @Override
    public void postProcessBeanFactory(ConfigurableListableBeanFactory bf) {
        for (String name : bf.getBeanDefinitionNames()) {
            if (name.endsWith("Repository")) {
                bf.getBeanDefinition(name).setLazyInit(true);
            }
        }
    }
}
// Bu bosqichda bean'ni getBean qilmang: u muddatidan oldin yaratiladi
```

## 5.12 Aware interfeyslari (Aware Interfaces - Callback Injection)

**Tavsif:** Ba'zi infratuzilma komponentlariga konteynerning o'zi - uning nomi, factory'si, environment'i yoki event publisher'i - kerak bo'ladi. Spring bu ehtiyojni bir to'plam tor, bitta setter'li interfeys bilan qondiradi: bean kerakli `Aware` interfeysini implement qilsa, konteyner initsializatsiyadan oldin tegishli obyektni uzatadi. Bu push-based callback injection: bean hech narsani qidirmaydi, konteyner o'zi beradi. Interfeyslarning torligi tufayli bean faqat o'ziga kerak bo'lgan infratuzilma qismiga bog'lanadi.

**Spring'da qayerda uchraydi:** `BeanNameAware`, `BeanFactoryAware`, `BeanClassLoaderAware` (beans moduli); `ApplicationContextAware`, `EnvironmentAware`, `ResourceLoaderAware`, `ApplicationEventPublisherAware`, `MessageSourceAware`, `EmbeddedValueResolverAware`, `ImportAware`, `ApplicationStartupAware` (context moduli); web tomonda `ServletContextAware`, `ServletConfigAware`. Ko'pchiligini `ApplicationContextAwareProcessor` (ichki `BeanPostProcessor`) uzatadi, `BeanNameAware`/`BeanFactoryAware` esa `AbstractAutowireCapableBeanFactory.invokeAwareMethods()` ichida bevosita chaqiriladi - shu sababli ular `@PostConstruct` va `afterPropertiesSet()` dan oldin ishlaydi.

**Qo'llanish keyslari:**
- Infratuzilma bean'i (custom post-processor, registrar) uchun `BeanFactory`ga erta kirish.
- `ApplicationEventPublisherAware` bilan domen event'larini `ApplicationContext`ni to'liq inject qilmasdan publish qilish.
- `EnvironmentAware` orqali profil va property'larga qarab o'zini sozlovchi komponent yozish.
- `ImportAware` bilan `@Enable*` annotatsiyasining atributlarini konfiguratsiya klassida o'qish.
- `ResourceLoaderAware` bilan classpath yoki tashqi resurslarni yuklovchi umumiy utility yozish.

**Ehtiyot bo'ling:** Oddiy business bean'da `Aware` interfeyslarini ishlatish kodni Spring'ga qattiq bog'laydi va testlashni qiyinlashtiradi - ularning o'rni faqat framework va infratuzilma qatlamida. `ApplicationContextAware` orqali `getBean()` chaqirish esa to'g'ridan-to'g'ri Service Locator anti-patterniga aylanadi; kerakli bog'liqlikni constructor'da yoki `ObjectProvider` bilan olish ma'qul.

```java
// Aware: konteyner infratuzilmasini callback orqali beradi
@Component
class ContextReporter implements ApplicationContextAware, EnvironmentAware {
    private ApplicationContext ctx;

    @Override public void setApplicationContext(ApplicationContext ctx) { this.ctx = ctx; }
    @Override public void setEnvironment(Environment env) {
        log.info("profillar: {}", Arrays.toString(env.getActiveProfiles()));
    }
}
// Biznes kodda Aware ishlatish - konteynerga bog'lanish. Oddiy injeksiya afzal.
```

## 5.13 Lifecycle va SmartLifecycle (Lifecycle / SmartLifecycle)

**Tavsif:** Bean yaratilishi va uning ichidagi fon aktivligini boshlash - ikki xil narsa: listener, poller, scheduler yoki server socket'ni context to'liq tayyor bo'lgandan keyin, belgilangan tartibda ishga tushirish kerak. `Lifecycle` `start()`/`stop()`/`isRunning()` kontraktini beradi, `SmartLifecycle` esa unga avtomatik ishga tushish, faza (phase) bo'yicha tartib va asinxron, callback bilan to'xtash imkonini qo'shadi. Start fazalar o'sish tartibida, stop esa teskari tartibda bajariladi - bu graceful shutdown'ning asosi.

**Spring'da qayerda uchraydi:** `org.springframework.context.Lifecycle`, `SmartLifecycle` (`isAutoStartup()`, `getPhase()`, `stop(Runnable)`, `DEFAULT_PHASE = Integer.MAX_VALUE`), `Phased`, boshqaruvchi `LifecycleProcessor` / `DefaultLifecycleProcessor`. Spring Boot 3.x/4.x'da web server aynan shu mexanizm orqali boshqariladi (`WebServerStartStopLifecycle`, graceful shutdown uchun `WebServerGracefulShutdownLifecycle`, `server.shutdown=graceful`), timeout `spring.lifecycle.timeout-per-shutdown-phase` bilan sozlanadi. Messaging dunyosida Spring Kafka'ning `MessageListenerContainer` va Spring AMQP'ning `SimpleMessageListenerContainer` `SmartLifecycle` implementatsiyalari; CRaC checkpoint/restore (`spring.context.checkpoint=onRefresh`) ham `Lifecycle` orqali ishlaydi.

```java
@Component
class OutboxPoller implements SmartLifecycle {
    private volatile boolean running;
    @Override public void start() { running = true; /* scheduler'ni yoqish */ }
    @Override public void stop() { running = false; /* in-flight ishni tugatish */ }
    @Override public boolean isRunning() { return running; }
    @Override public int getPhase() { return Integer.MAX_VALUE - 1024; } // web'dan oldin to'xtaydi
}
```

**Qo'llanish keyslari:**
- Kafka yoki RabbitMQ consumer'ini web server tayyor bo'lgandan keyin ishga tushirish va shutdown'da undan oldin to'xtatish.
- Graceful shutdown'da in-flight so'rovlar va messagelar tugashini kutib, keyin connection'larni yopish.
- Blue-green deploy yoki leader election'da fon ishini runtime'da `start()`/`stop()` bilan boshqarish.
- Faza raqamlari bilan "avval cache isisin, keyin trafik qabul qilinsin" tartibini kafolatlash.
- Testda tashqi tizimga ulanadigan listener'larni `isAutoStartup() == false` qilib o'chirib qo'yish.

**Ehtiyot bo'ling:** `stop()` bloklovchi va uzoq bo'lsa, shutdown timeout'i urib ketadi va ish yarim yo'lda uzilib qoladi - uzoq to'xtash uchun `stop(Runnable)` variantini ishlatish kerak. `Lifecycle` (`SmartLifecycle` emas) implementatsiyasi avtomatik ishga tushmaydi, lazy bean esa umuman start qilinmaydi - bu jim turib ishlamaydigan consumer'ga olib keladi.

## 5.14 SmartInitializingSingleton (SmartInitializingSingleton)

**Tavsif:** Ba'zi ishlarni bean o'zi tayyor bo'lgandan keyin emas, barcha singleton'lar tayyor bo'lgandan keyin qilish kerak - masalan butun context'ni skanerlab, annotatsiyalangan metodlarni ro'yxatga olish. `SmartInitializingSingleton` aynan shu "hammasi tayyor" nuqtasiga ilinadi: `afterSingletonsInstantiated()` eager singleton'lar pre-instantiation bosqichi tugagach chaqiriladi. Bu `@PostConstruct`dan kechroq, lekin `ContextRefreshedEvent`dan oldinroq ishlaydigan oraliq hook. Shu tufayli boshqa bean'larni erta instantiate qilib qo'yish xavfisiz global ro'yxat yig'ish mumkin.

**Spring'da qayerda uchraydi:** `org.springframework.beans.factory.SmartInitializingSingleton`, uni `DefaultListableBeanFactory.preInstantiateSingletons()` oxirida chaqiradi. Framework'dagi real implementatsiyalar: `EventListenerMethodProcessor` (`@EventListener` metodlarini topib ro'yxatga oladi), `ScheduledAnnotationBeanPostProcessor` (`@Scheduled` task'larni context tayyor bo'lgach ishga tushiradi), JMX'dagi `MBeanExporter`, Spring Kafka'dagi `KafkaListenerAnnotationBeanPostProcessor`. Muqobil hook'lar: `@EventListener(ContextRefreshedEvent.class)`, `ApplicationListener<ApplicationReadyEvent>` hamda Spring Boot'ning `ApplicationRunner` / `CommandLineRunner`.

**Qo'llanish keyslari:**
- Custom annotatsiyali metodlarni butun context bo'ylab topib, handler registry'ga yig'ish.
- Barcha strategiya bean'larini bir marta skanerlab, tip yoki kalit bo'yicha lookup jadvalini qurish.
- Startup validatsiyasi: barcha kerakli bean'lar, converter'lar yoki mapping'lar mavjudligini tekshirish.
- Metrika va health indicator'larni context to'liq shakllangandan keyin ro'yxatga olish.
- `BeanPostProcessor` bilan juftlikda ishlatib, yig'ilgan ma'lumotni oxirida bir marta yakuniy holatga keltirish.

**Ehtiyot bo'ling:** Bu callback faqat eager singleton'lar uchun kafolatlangan - lazy yoki scoped bean'lar hali yaratilmagan bo'ladi, shuning uchun `getBeanNamesForType()` bilan definition darajasida ishlash xavfsizroq. Ilova trafik qabul qilishga tayyor bo'lgandan keyin bajarilishi kerak bo'lgan ish uchun u mos emas - bunday holatda `ApplicationReadyEvent` yoki `ApplicationRunner` ishlatilsin.

```java
// SmartInitializingSingleton: BARCHA singleton'lar tayyor bo'lgandan keyin
@Component
class HandlerRegistryInitializer implements SmartInitializingSingleton {
    private final ApplicationContext ctx;
    HandlerRegistryInitializer(ApplicationContext ctx) { this.ctx = ctx; }

    @Override
    public void afterSingletonsInstantiated() {
        // @PostConstruct dan farqi: bu yerda hamma bean mavjud, aylanma bog'liqlik yo'q
        ctx.getBeansOfType(CommandHandler.class).values().forEach(registry::register);
    }
}
```

## 5.15 Tartiblash va ustuvorlik (Ordered / @Order)

**Tavsif:** Bir xil tipdagi bir nechta komponent (filter, interceptor, advice, post-processor) ketma-ket ishlaganda ularning ijro tartibi muhim bo'ladi, lekin bean'larni yaratish tartibi bunga kafolat bermaydi. Bu pattern tartibni alohida metadata - butun son ko'rinishidagi "order" qiymati - sifatida ajratib oladi va framework bu qiymat bo'yicha ro'yxatni saralaydi. Kichik qiymat yuqori ustuvorlikni bildiradi (`Ordered.HIGHEST_PRECEDENCE` = `Integer.MIN_VALUE`). Natijada komponentlar bir-biri haqida bilmagan holda ham bashorat qilinadigan zanjir hosil qiladi.

**Spring'da qayerda uchraydi:** `org.springframework.core.Ordered` va undan oldin ishlaydigan `PriorityOrdered` interfeyslari, `@Order` annotatsiyasi (`org.springframework.core.annotation.Order`), `jakarta.annotation.Priority`, saralash mantiqini bajaradigan `OrderComparator` va `AnnotationAwareOrderComparator`, `OrderUtils`. Amalda: `FilterRegistrationBean#setOrder`, Spring Security'da bir nechta `SecurityFilterChain` bean'ini `@Order` bilan tartiblash, `HandlerInterceptor` zanjiri, `@ControllerAdvice` sinflari, `HandlerMapping` va `HandlerExceptionResolver` ro'yxatlari, `@EventListener` metodlari, `List<T>` ko'rinishida inject qilinadigan strategiya to'plamlari. Spring Boot 3.x auto-konfiguratsiyada `@AutoConfigureOrder`, `@AutoConfigureBefore`, `@AutoConfigureAfter` ishlatiladi; `BeanPostProcessor` esa `PriorityOrdered` → `Ordered` → tartibsiz guruhlariga bo'lib qo'llanadi.

**Qo'llanish keyslari:**
- `OncePerRequestFilter` asosidagi correlation-ID filter'ini autentifikatsiya filter'idan oldin ishga tushirish.
- Spring Security'da `/api/**` va qolgan URL'lar uchun ikki `SecurityFilterChain`ni to'g'ri tartibda joylashtirish.
- `@ControllerAdvice` ichida umumiy exception handler'ni maxsus handler'dan keyin qo'yish.
- `List<ValidationRule>` sifatida inject qilingan validatsiya qoidalarini aniq ketma-ketlikda bajarish.
- Kutubxona beradigan auto-konfiguratsiyani mijoz loyihasining konfiguratsiyasidan keyin qo'llash.

**Ehtiyot bo'ling:** `@Order` faqat kolleksiya sifatida yig'ilgan yoki zanjirga qo'shilgan komponentlarni saralaydi - u bean'larning yaratilish (instantiation) tartibini yoki `@Bean` metodlari chaqiriluvini boshqarmaydi; bunga `@DependsOn` yoki haqiqiy dependency kerak. Qo'lda yozilgan "1, 2, 3" qiymatlari o'rniga `Ordered.LOWEST_PRECEDENCE - 10` kabi nisbiy konstantalardan foydalaning, aks holda kutubxona order'lari bilan to'qnashuv chiqadi.

```java
// Tartib: kichik qiymat oldin ishlaydi
@Component
@Order(1)                                    // avval ishga tushadi
class BlacklistFraudCheck implements FraudCheck { /* ... */ }

@Component
@Order(100)
class VelocityFraudCheck implements FraudCheck { /* ... */ }

// List<FraudCheck> inject qilinganda Spring @Order bo'yicha saralab beradi.
// Tartib muhim bo'lsa, uni aniq belgilang: scanning tartibiga tayanmang.
```

## 5.16 Spring AOP: proxy asosidagi kesishuv (Spring AOP - Advice, Pointcut, Advisor, Interceptor)

**Tavsif:** Logging, audit, metrika, retry, tranzaksiya kabi cross-cutting masalalar o'nlab sinfga tarqalib ketsa, biznes kodi shovqinga ko'miladi. AOP bu masalalarni uch mustaqil tushunchaga ajratadi: *advice* - nima qilish kerak, *pointcut* - qayerda qo'llash kerak, *advisor* - ularni birlashtirgan juftlik. Spring buni runtime'da proxy yaratib amalga oshiradi: target bean o'rniga kontekstga uning proxy'si joylashtiriladi va har bir chaqiruv interceptor zanjiri orqali o'tadi. Bu Proxy, Decorator va Chain of Responsibility patternlarining amaliy birikmasi.

**Spring'da qayerda uchraydi:** `org.aopalliance.intercept.MethodInterceptor` va `MethodInvocation`, `org.springframework.aop.Pointcut`, `Advisor`, `PointcutAdvisor`, `DefaultPointcutAdvisor`, `AspectJExpressionPointcut`, `NameMatchMethodPointcut`. Deklarativ uslub: `@Aspect`, `@Around`, `@Before`, `@AfterReturning`, `@AfterThrowing`, `ProceedingJoinPoint`, `@EnableAspectJAutoProxy` va uning ortidagi `AnnotationAwareAspectJAutoProxyCreator`. Programmatik uslub: `ProxyFactory`, `ProxyFactoryBean`. Proxy mexanizmlari - interfeys uchun `JdkDynamicAopProxy`, sinf uchun `CglibAopProxy` (Spring Framework 6.x'da CGLIB Spring ichiga "repackage" qilingan, Spring Boot 3.x esa `spring.aop.proxy-target-class=true` bilan odatda CGLIB ishlatadi). Yordamchilar: `AopUtils`, `AopProxyUtils.ultimateTargetClass`, `AopContext.currentProxy()` (faqat `exposeProxy=true` bo'lsa).

**Qo'llanish keyslari:**
- `@Timed` yoki o'z annotatsiyangiz bo'yicha metod bajarilish vaqtini Micrometer'ga yozish.
- Tashqi integratsiya adapter'lariga retry va circuit-breaker mantiqini qo'shish.
- Multi-tenant ilovada har bir service chaqiruvidan oldin tenant kontekstini o'rnatish va keyin tozalash.
- Sezgir metodlar uchun audit log yozib, kim qanday argument bilan chaqirganini saqlash.
- Legacy sinflarga kod tegmasdan kirish nazoratini (`@PreAuthorize`ga o'xshash) qo'llash.

**Ehtiyot bo'ling:** Eng ko'p uchraydigan tuzoq - self-invocation: bir xil bean ichidan `this.method()` chaqirilsa proxy chetlab o'tiladi va advice ishlamaydi; shuningdek `private`, `static` va `final` metodlar, `final` sinflar advise qilinmaydi. Proxy'lar qo'shimcha chaqiruv qatlamini va `getClass()` natijasining o'zgarishini keltirib chiqaradi, shuning uchun tip tekshiruvi va reflection'ga tayangan kod `AopProxyUtils`dan foydalanishi kerak.

```java
@Aspect
@Component
public class AuditAspect {

    @Pointcut("@annotation(com.example.Audited)")
    void audited() {}

    @Around("audited()")
    public Object around(ProceedingJoinPoint pjp) throws Throwable {
        String method = pjp.getSignature().toShortString();
        try {
            Object result = pjp.proceed();
            auditLog.success(method);
            return result;
        } catch (Throwable t) {
            auditLog.failure(method, t);
            throw t;                      // istisnoni yutmang
        }
    }
}
```

## 5.17 Tranzaksiya proxy'si va TransactionTemplate (@Transactional Proxy & TransactionTemplate)

**Tavsif:** Tranzaksiyani qo'lda boshqarish (`begin`, `commit`, `rollback`, `finally close`) takrorlanuvchi va xatoga moyil kod. Spring buni ikki yo'l bilan hal qiladi: deklarativ - `@Transactional` annotatsiyasi AOP proxy orqali metod atrofiga tranzaksiya chegarasini o'raydi; programmatik - `TransactionTemplate` callback ichidagi kodni tranzaksiya ichida bajaradi. Ikkisi ham bir xil `PlatformTransactionManager` abstraksiyasiga tayanadi, shuning uchun JDBC, JPA yoki JTA ostida kod o'zgarmaydi.

**Spring'da qayerda uchraydi:** `@Transactional`, `@EnableTransactionManagement`, ichki ishni bajaruvchi `TransactionInterceptor` va `TransactionAspectSupport`, metadata o'quvchi `AnnotationTransactionAttributeSource`. Manager'lar: `PlatformTransactionManager`, `DataSourceTransactionManager`, `JpaTransactionManager`, `JtaTransactionManager`, reaktiv tomonda `ReactiveTransactionManager` va `TransactionalOperator`. Programmatik: `TransactionTemplate`, `TransactionCallback`, `TransactionCallbackWithoutResult`, `TransactionStatus`, `TransactionDefinition`, `Propagation` va `Isolation` enum'lari, `TransactionSynchronizationManager`. Spring Boot 3.x `DataSourceTransactionManagerAutoConfiguration` va `JpaBaseConfiguration` orqali manager'ni avtomatik yaratadi.

**Qo'llanish keyslari:**
- Service qatlamidagi use-case metodini bitta atomar tranzaksiyaga o'rash.
- Hisobot o'qish metodlarini `@Transactional(readOnly = true)` bilan belgilash - flush'ni o'chiradi va replica'ga yo'naltirishga imkon beradi.
- `Propagation.REQUIRES_NEW` bilan audit yozuvini asosiy tranzaksiya rollback bo'lsa ham saqlab qolish.
- Uzun batch jobda `TransactionTemplate` yordamida har 500 yozuvni alohida tranzaksiyada commit qilish.
- `TransactionSynchronizationManager.registerSynchronization` bilan commit'dan keyin cache'ni tozalash.

**Ehtiyot bo'ling:** Standart sozlamada rollback faqat `RuntimeException` va `Error`da sodir bo'ladi - checked exception uchun `rollbackFor` ni aniq ko'rsatish shart; `catch` bilan "yutilgan" exception esa tranzaksiyani allaqachon rollback-only holatga o'tkazib, commit paytida `UnexpectedRollbackException` beradi. `@Transactional`ni `private` metodga yoki bir sinf ichidagi o'z-o'zini chaqiruvga qo'yish hech qanday ta'sir bermaydi, hamda `@Transactional` metod ichida tashqi HTTP chaqiruv qilish tranzaksiyani va connection'ni keraksiz uzoq ushlab turadi.

```java
// Deklarativ chegara: proxy orqali, self-invocation ishlamaydi
@Transactional(timeout = 5, readOnly = false)
public void transfer(long from, long to, Money amount) { /* ... */ }

// Programmatik chegara: aniq va proxy'ga bog'liq emas
@Service
public class LedgerService {
    private final TransactionTemplate tx;

    public LedgerService(PlatformTransactionManager tm) {
        this.tx = new TransactionTemplate(tm);
        this.tx.setTimeout(5);
    }

    public Receipt post(Entry entry) {
        return tx.execute(status -> ledger.append(entry));   // chegara aniq ko'rinadi
    }
}
```

## 5.18 Template sinflari (Template Classes)

**Tavsif:** Har qanday infratuzilma bilan ishlashda bir xil "skelet" takrorlanadi: resurs olish, ishni bajarish, xatoni tarjima qilish, resursni qaytarish. Template Method pattern bu o'zgarmas skeletni framework ichida qoldirib, faqat o'zgaradigan qismni foydalanuvchiga beradi. Shu sababli Spring'dagi `*Template` sinflari resource management va exception translation'ni o'ziga oladi, siz esa bir necha qator biznes mantig'ini yozasiz.

**Spring'da qayerda uchraydi:** `JdbcTemplate`, `NamedParameterJdbcTemplate` va Spring Framework 6.1+ dagi fluent `JdbcClient`; HTTP tomonda `RestTemplate` (6.x'da maintenance holatida), yangi `RestClient` (6.1+) va reaktiv `WebClient`; messaging'da `JmsTemplate`, `KafkaTemplate` (Spring for Apache Kafka), `RabbitTemplate` (Spring AMQP); `TransactionTemplate`; ma'lumotlar omborlari uchun `RedisTemplate`/`StringRedisTemplate`, `MongoTemplate`, `ElasticsearchTemplate`. Xato tarjimasi `SQLExceptionTranslator` va `SQLErrorCodeSQLExceptionTranslator` orqali `DataAccessException` ierarxiyasiga aylanadi; Spring Boot 3.x bu template'larning ko'pini (`JdbcTemplate`, `KafkaTemplate`, `RestClient.Builder`) auto-konfiguratsiya qiladi.

**Qo'llanish keyslari:**
- JPA mos kelmaydigan murakkab reporting SQL'ini `JdbcClient` yoki `JdbcTemplate` bilan yozish.
- Batch `INSERT`ni `jdbcTemplate.batchUpdate` orqali bitta round-trip'da bajarish.
- Tashqi REST API ga `RestClient` bilan timeout va interceptor sozlangan chaqiruv qilish.
- `KafkaTemplate` orqali transactional producer'da event yuborish.
- `RedisTemplate` yordamida distributed lock yoki rate-limit counter'ini boshqarish.

**Ehtiyot bo'ling:** Template'lar konfiguratsiya tugagandan keyin thread-safe deb hisoblanadi, lekin runtime'da `setInterceptors`, `setMessageConverters` kabi setter'larni chaqirish yashirin race condition yaratadi - har bir maqsad uchun alohida bean yasang. Yangi kodda `RestTemplate` o'rniga `RestClient` yoki `WebClient` ni tanlang va timeout'ni albatta aniq belgilang, chunki standart `RestTemplate` cheksiz kutishi mumkin.

```java
// Template sinfi: resurs va xato boshqaruvi kutubxonada
@Repository
public class AccountDao {
    private final JdbcClient db;
    public AccountDao(JdbcClient db) { this.db = db; }

    public Optional<Account> find(long id) {
        return db.sql("SELECT id, balance FROM accounts WHERE id = :id")
                 .param("id", id)
                 .query(Account.class)
                 .optional();
    }
}
// Connection olish, yopish va SQLException ni DataAccessException ga
// aylantirish - hammasi template ichida.
```

## 5.19 Callback interfeyslari (Callback Interfaces)

**Tavsif:** Template sinfi skeletni boshqaradi, ammo "har bir qatorni qanday obyektga aylantirish kerak" degan qismni faqat chaqiruvchi biladi. Callback - bu template ichiga uzatiladigan kichik strategiya: framework resursni ochadi, callback'ga beradi va undan keyin tozalaydi. Bu Strategy va Inversion of Control birikmasi bo'lib, resurs oqib ketishini (resource leak) tuzilmaviy darajada imkonsiz qiladi.

**Spring'da qayerda uchraydi:** JDBC tomonida `RowMapper<T>`, `ResultSetExtractor<T>`, `RowCallbackHandler`, `PreparedStatementSetter`, `PreparedStatementCreator`, `ConnectionCallback`, `StatementCallback`, `CallableStatementCallback`, `BatchPreparedStatementSetter`; tayyor implementatsiyalar `BeanPropertyRowMapper`, `DataClassRowMapper` (Java record va immutable sinflar uchun), `SingleColumnRowMapper`, `RowMapperResultSetExtractor`. Boshqa modullarda: `TransactionCallback`, `JmsTemplate`ning `MessageCreator` va `SessionCallback`, `RedisCallback` va `SessionCallback` (Spring Data Redis), `CollectionCallback` (Spring Data MongoDB). Java 17+ da bu interfeyslarning deyarli barchasi funksional, shuning uchun lambda yoki method reference sifatida yoziladi.

**Qo'llanish keyslari:**
- `RowMapper`ni record konstruktoriga bog'lab, DTO'ni to'g'ridan-to'g'ri SQL natijasidan yasash.
- `JOIN` natijasidagi bir-ko'p (one-to-many) strukturani `ResultSetExtractor` bilan agregatsiyalab yig'ish.
- Millionlab qatorli eksportni `RowCallbackHandler` orqali stream qilib, xotirada ushlamaslik.
- `PreparedStatementSetter` bilan dinamik filtr parametrlarini xavfsiz bog'lash.
- `ConnectionCallback` orqali vendor-specific JDBC API (masalan PostgreSQL `COPY`) ga tushish.

**Ehtiyot bo'ling:** `ResultSet`, `Connection` yoki `Statement` obyektini callback'dan tashqariga chiqarib yubormang - template qaytgandan keyin ular yopilgan bo'ladi va `SQLException` yoki yashirin leak chiqadi. `RowCallbackHandler` holat saqlaydi, demak u thread-safe emas va bean sifatida bir marta yaratib qayta ishlatilmasligi kerak; `BeanPropertyRowMapper` esa reflection'ga tayangani uchun eng issiq (hot) query'larda qo'lda yozilgan mapper'dan sekinroq ishlaydi.

```java
// Callback: "nima" ni biz beramiz, "qachon" ni kutubxona hal qiladi
List<OrderRow> rows = jdbcTemplate.query(
        "SELECT id, status FROM orders WHERE created_at > ?",
        ps -> ps.setTimestamp(1, Timestamp.from(since)),   // PreparedStatementSetter
        (rs, i) -> new OrderRow(rs.getLong(1), rs.getString(2)));  // RowMapper

// Katta natija uchun qator-qator ishlov: xotirada hammasi yig'ilmaydi
jdbcTemplate.query("SELECT id FROM orders", (RowCallbackHandler) rs ->
        export(rs.getLong("id")));
```

## 5.20 Ilova hodisalari (ApplicationEvent / @EventListener / @TransactionalEventListener)

**Tavsif:** Modullar bir-birini to'g'ridan-to'g'ri chaqirsa, ular qattiq bog'lanib qoladi va har bir yangi "yon ta'sir" mavjud service'ni o'zgartirishni talab qiladi. Observer pattern buni teskari aylantiradi: publisher faqat "nima bo'ldi" degan faktni e'lon qiladi, qiziqqan listener'lar esa mustaqil ravishda reaksiya bildiradi. Spring bunga multicaster, deklarativ listener va tranzaksiya fazalariga bog'lanish imkonini qo'shadi, shu bilan "commit bo'lgandan keyin yubor" kabi real talablarni qoplaydi.

**Spring'da qayerda uchraydi:** `ApplicationEventPublisher`, `ApplicationEventPublisherAware`, `ApplicationEvent`, `ApplicationListener<E>`, `@EventListener` (shart uchun `condition` SpEL atributi), `@TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)`, asinxronlik uchun `@Async` va `SimpleApplicationEventMulticaster`ga berilgan `TaskExecutor`, POJO event'lar uchun `PayloadApplicationEvent`. Framework o'zi ham shu mexanizmdan foydalanadi: `ContextRefreshedEvent`, `ContextClosedEvent`, Spring Boot 3.x'da `ApplicationStartedEvent`, `ApplicationReadyEvent`, `AvailabilityChangeEvent`; Spring Security `AuthenticationSuccessEvent` yuboradi. Spring Modulith `@ApplicationModuleListener` bilan "async + yangi tranzaksiya + after-commit" kombinatsiyasini bitta annotatsiyaga yig'adi.

**Qo'llanish keyslari:**
- Buyurtma yaratilgandan keyin email/SMS yuborishni asosiy use-case'dan ajratish.
- `AFTER_COMMIT` fazasida Kafka'ga event yuborib, "DB rollback bo'ldi, lekin xabar ketdi" muammosini yo'qotish.
- Domen o'zgarishi natijasida read-model yoki cache'ni invalidatsiya qilish.
- `ApplicationReadyEvent`da warm-up query va health probe'larni ishga tushirish.
- Modulli monolitda modullar orasidagi aloqani event bilan kuchsizlantirish (loose coupling).

**Ehtiyot bo'ling:** Standart holatda event'lar sinxron - publisher thread'ida va ayni tranzaksiyada bajariladi, demak listener ichidagi exception publisher'ga qaytib, uning tranzaksiyasini rollback qiladi. `AFTER_COMMIT` listener esa tranzaksiyadan tashqarida ishlaydi: unda DB yozishni xohlasangiz `Propagation.REQUIRES_NEW` kerak, aks holda yozuv jim saqlanmay qolishi mumkin; shuningdek event oqimi juda ko'payib ketsa, mantiq "ko'rinmas" bo'lib, debug qilish og'irlashadi.

```java
@Transactional
public void place(Order order) {
    repo.save(order);
    events.publishEvent(new OrderPlaced(order.id()));
}

@Component
class OrderPlacedHandlers {

    @EventListener                       // sinxron, tranzaksiya ICHIDA
    void updateMetrics(OrderPlaced e) { counter.increment(); }

    @TransactionalEventListener(phase = AFTER_COMMIT)   // commit'dan KEYIN
    void notifyWarehouse(OrderPlaced e) { warehouse.send(e); }
}
// Xabar yuborish AFTER_COMMIT da bo'lishi kerak: rollback bo'lsa xabar ketmaydi
```

## 5.21 Environment va PropertySource zanjiri (Environment & PropertySource Chain)

**Tavsif:** Konfiguratsiya qiymatlari bir nechta manbadan keladi: command-line, environment variable, `application.yml`, Kubernetes ConfigMap, Vault. Spring bu manbalarni bir xil `PropertySource` abstraksiyasiga keltirib, ularni ustuvorligi bo'yicha tartiblangan zanjirga joylaydi. Qiymat so'ralganda zanjir boshidan yurib, birinchi topilgan javob qaytadi - bu Chain of Responsibility pattern bo'lib, "override qilish" semantikasini tabiiy beradi.

**Spring'da qayerda uchraydi:** `Environment`, `ConfigurableEnvironment`, `StandardEnvironment`, `PropertyResolver`, `MutablePropertySources` (`addFirst`, `addLast`, `addBefore`), `PropertySource` va uning implementatsiyalari `SystemEnvironmentPropertySource`, `MapPropertySource`, `OriginTrackedMapPropertySource`, `RandomValuePropertySource`. Placeholder'ni ochish `PropertySourcesPlaceholderConfigurer` va `@Value` orqali, qo'shimcha fayl `@PropertySource` bilan qo'shiladi. Spring Boot 3.x konfiguratsiya yuklashni `ConfigDataEnvironmentPostProcessor` va `EnvironmentPostProcessor` SPI orqali bajaradi, `spring.config.import` (masalan `optional:configtree:/etc/secrets/`) tashqi manbalarni ulaydi; ustuvorlik tartibi hujjatlashtirilgan - command-line argumentlar `SPRING_APPLICATION_JSON`, keyin OS environment, so'ngra profil fayllari va oxirida `application.properties`.

**Qo'llanish keyslari:**
- Bir xil image'ni dev/stage/prod'da faqat environment variable almashtirib ishlatish.
- Kubernetes'dagi mounted secret'larni `configtree:` orqali property sifatida o'qish.
- Vault yoki AWS Parameter Store'ni `EnvironmentPostProcessor` bilan zanjir boshiga qo'shish.
- `Environment.getProperty` bilan feature flag'ni runtime'da emas, startup'da o'qib bean tanlash.
- `OriginTrackedValue` ma'lumotidan foydalanib, "bu qiymat qaysi fayldan keldi" degan diagnostika chiqarish.

**Ehtiyot bo'ling:** `@Value` qiymati bean yaratilganda bir marta hal qilinadi - Spring Cloud `@RefreshScope` bo'lmasa, property o'zgarishi ilovaga ta'sir qilmaydi. Zanjirga manba qo'shayotganda `addFirst`/`addLast` tanlovini aniq o'ylab ko'ring, aks holda prod'da kutilmaganda default qiymat ustun chiqib ketadi; sirlarni esa `/actuator/env` orqali oshkor qilmaslik uchun sanitize sozlamalarini tekshirib qo'ying.

```java
// PropertySource zanjiri: yuqoridagi pastdagini bosadi
// 1) buyruq qatori argumentlari
// 2) OS muhit o'zgaruvchilari (SPRING_DATASOURCE_URL)
// 3) application-{profile}.yml
// 4) application.yml
// 5) @PropertySource
@Component
class ConfigAudit {
    ConfigAudit(ConfigurableEnvironment env) {
        // Qiymat qaysi manbadan kelganini aniqlash
        env.getPropertySources().forEach(ps ->
                log.info("{} -> {}", ps.getName(), ps.getProperty("psp.url")));
    }
}
```

## 5.22 Konfiguratsiya xossalarini bog'lash (@ConfigurationProperties Binding)

**Tavsif:** O'nlab `@Value` o'rniga konfiguratsiyani tipli, validatsiyalanadigan va guruhlangan obyektga bog'lash ancha xavfsiz. `@ConfigurationProperties` prefiks ostidagi barcha kalitlarni POJO yoki record'ga map qiladi, kerakli konvertatsiyani (String → `Duration`, `DataSize`, enum, `List`, `Map`) bajaradi va relaxed binding orqali `my-prop`, `my_prop`, `MY_PROP` shakllarini bir xil deb qabul qiladi. Bu Builder/Data Transfer Object va Strategy (conversion) patternlarining konfiguratsiyaga moslashtirilgan ko'rinishi.

**Spring'da qayerda uchraydi:** `@ConfigurationProperties`, `@EnableConfigurationProperties`, `@ConfigurationPropertiesScan`, ichkarida ishlovchi `ConfigurationPropertiesBindingPostProcessor` va umumiy `Binder`/`Bindable` API. Spring Boot 3.x'da yagona konstruktorli sinf uchun constructor binding avtomatik (eski `@ConstructorBinding` faqat bir nechta konstruktor bo'lsa kerak), `@DefaultValue` standart qiymat beradi. Validatsiya `@Validated` va `jakarta.validation` annotatsiyalari bilan, birlik ko'rsatish `@DurationUnit` va `@DataSizeUnit` bilan, ichki obyekt `@NestedConfigurationProperty` bilan. IDE autocomplete uchun `spring-boot-configuration-processor`, maxsus tiplar uchun `@ConfigurationPropertiesBinding` converter'lari ishlatiladi.

```java
@ConfigurationProperties("billing.gateway")
@Validated
public record GatewayProps(
        @NotBlank String baseUrl,
        @DefaultValue("3s") Duration timeout,
        @Min(1) int maxRetries,
        Map<String, String> headers) {}
```

**Qo'llanish keyslari:**
- Tashqi integratsiya sozlamalarini (URL, timeout, retry, API kalit nomi) bitta record'da jamlash.
- Noto'g'ri konfiguratsiyada ilovani startup'da yiqitib, prod'da kech aniqlanishini oldini olish.
- Kutubxona yoki starter uchun hujjatlashtirilgan, autocomplete'li sozlama modeli berish.
- `Map<String, TenantConfig>` ko'rinishida ko'p tenant sozlamalarini dinamik o'qish.
- Testda `@ConfigurationProperties` bean'ini `ApplicationContextRunner` bilan izolyatsiyada tekshirish.

**Ehtiyot bo'ling:** Constructor/record binding immutable bo'lgani uchun `@RefreshScope` bilan yangilanmaydi va setter binding kutgan kod ishlamay qoladi - bitta sinfda ikki uslubni aralashtirmang. Shuningdek `@Value` ichidagi SpEL `@ConfigurationProperties` bog'lanishida qo'llanmaydi, binding esa relaxed nomlashga tayanadi, shuning uchun YAML'da kalitni kamelCase emas, kebab-case bilan yozish eng bashoratli variant.

## 5.23 Profillar (Profiles)

**Tavsif:** Bir xil kod bazasi turli muhitlarda turli bean'lar va sozlamalar bilan ishlashi kerak: lokalda in-memory queue, prod'da Kafka. Profile - bu nomlangan shart bo'lib, bean definition yoki konfiguratsiya blokini faqat ma'lum muhitda aktiv qiladi. Bu `@Conditional`ning maxsus, odam o'qiy oladigan ko'rinishi va muhit bo'yicha variantlarni bitta joydan boshqarish imkonini beradi.

**Spring'da qayerda uchraydi:** `@Profile` annotatsiyasi (shart ifodalari bilan: `@Profile("!prod & cloud")`), `Environment.getActiveProfiles()` va `acceptsProfiles(Profiles.of(...))`, `spring.profiles.active`, `spring.profiles.default`, `spring.profiles.group` (Spring Boot 2.4+ da eski `spring.profiles.include` o'rniga tavsiya etiladi), profil fayllari `application-{profile}.yml`, YAML dokumenti darajasidagi `spring.config.activate.on-profile`. Testlarda `@ActiveProfiles`, shuningdek Spring Boot 3.x `ApplicationContextRunner#withSystemProperties` bilan profil xatti-harakatini tekshirish mumkin.

**Qo'llanish keyslari:**
- `dev` profilda H2 va mock to'lov gateway'ini, `prod` da real PostgreSQL va gateway'ni ulash.
- `prod` profilda audit va rate-limit filter'larini qo'shimcha ravishda yoqish.
- `spring.profiles.group.prod=prod,cloud,metrics` bilan bir nechta profilni bitta nom ostida birlashtirish.
- Integration testda `@ActiveProfiles("test")` orqali Testcontainers konfiguratsiyasini tanlash.
- Local demo uchun seed data yuklovchi `CommandLineRunner`ni faqat `demo` profilda ishga tushirish.

**Ehtiyot bo'ling:** Profile'ni biznes feature-flag sifatida ishlatish anti-pattern: profillar startup'da qotib qoladi, runtime'da o'zgarmaydi va kombinatsiyalari tez portlab ketadi - buning uchun `@ConfigurationProperties` yoki haqiqiy flag tizimidan foydalaning. Profil ostidagi bean yo'q bo'lsa, unga bog'langan inject nuqtalari startup'da yiqiladi, shuning uchun har bir profilni CI'da kamida bir marta kontekst yuklab sinab ko'rish kerak.

```java
@Configuration(proxyBeanMethods = false)
class PaymentConfig {

    @Bean
    @Profile("!prod")                    // prod'dan boshqa hamma joyda
    PaymentGateway mockGateway() { return new MockGateway(); }

    @Bean
    @Profile("prod")
    PaymentGateway pspGateway(PspProperties p) { return new PspGateway(p); }
}
// Profil soni o'sib ketsa, @ConditionalOnProperty aniqroq bo'ladi:
// profil "qanday muhit", property "qaysi imkoniyat yoqilgan" degani.
```

## 5.24 Shartli bean'lar va auto-konfiguratsiya (@Conditional & Auto-configuration)

**Tavsif:** Framework "aqlli default" bera olishi uchun atrof-muhitni o'zi tekshirishi kerak: kerakli sinf classpath'da bormi, foydalanuvchi o'z bean'ini bergan-bermaganmi, qaysi property yoqilgan. `@Conditional` bu tekshiruvni `Condition` strategiyasiga ajratadi va bean definition ro'yxatga olinishidan oldin baholaydi. Spring Boot auto-konfiguratsiyasi butunlay shunga qurilgan: har bir auto-config sinfi shartlar to'plami ortida turadi va faqat mos holatda qo'llanadi.

**Spring'da qayerda uchraydi:** `Condition` interfeysi, `ConditionContext`, `AnnotatedTypeMetadata`, `@Conditional`. Spring Boot 3.x tayyor shartlari: `@ConditionalOnClass`, `@ConditionalOnMissingClass`, `@ConditionalOnBean`, `@ConditionalOnMissingBean`, `@ConditionalOnProperty`, `@ConditionalOnResource`, `@ConditionalOnExpression`, `@ConditionalOnWebApplication`, `@ConditionalOnAvailableEndpoint`, `@ConditionalOnThreading` (virtual thread'lar uchun, Boot 3.2+). Auto-konfiguratsiya sinfi `@AutoConfiguration` bilan belgilanadi, tartibi `@AutoConfigureBefore`/`@AutoConfigureAfter` bilan boshqariladi, ro'yxat `AutoConfigurationImportSelector` orqali yuklanadi, natijani `ConditionEvaluationReport` (`--debug` yoki `/actuator/conditions`) ko'rsatadi.

```java
@AutoConfiguration
@ConditionalOnClass(AuditSink.class)
@ConditionalOnProperty(prefix = "audit", name = "enabled", matchIfMissing = true)
@EnableConfigurationProperties(AuditProps.class)
public class AuditAutoConfiguration {
    @Bean
    @ConditionalOnMissingBean
    AuditSink auditSink(AuditProps props) {
        return new HttpAuditSink(props);
    }
}
```

**Qo'llanish keyslari:**
- Ichki platforma kutubxonasiga "o'zi sozlanadigan, lekin override qilinadigan" default bean'lar berish.
- `management.metrics.export.*` kabi property bilan ixtiyoriy integratsiyani yoqish/o'chirish.
- Classpath'da Redis bo'lsa distributed cache, bo'lmasa in-memory cache tanlash.
- Servlet va reactive stack uchun bir xil funksiyaning ikki xil implementatsiyasini ro'yxatga olish.
- Startup muammosini `/actuator/conditions` hisoboti bilan "nega bu bean yaratilmadi" savoliga javob topish.

**Ehtiyot bo'ling:** `@ConditionalOnBean` va `@ConditionalOnMissingBean` baholash paytida faqat o'sha vaqtgacha ro'yxatga olingan bean definition'larni ko'radi, shuning uchun ular tartibga sezgir va faqat auto-konfiguratsiya sinflarida ishlatilishi kerak - oddiy `@Configuration`da ular jim, takrorlanmaydigan xatolarga olib keladi. Shartlarni haddan tashqari ko'paytirish esa kontekstni "sehrli" qilib qo'yadi, shuning uchun har bir auto-config uchun `ApplicationContextRunner` bilan test yozish amalda majburiy.

## 5.25 Starter'lar (Starters)

**Tavsif:** Yangi loyihada "qaysi kutubxonaning qaysi versiyasi qaysi biri bilan mos keladi" muammosi ko'p vaqt oladi. Starter - bu o'z kodi bo'lmagan, faqat bir-biriga mos dependency to'plamini va kerakli auto-konfiguratsiyani olib keladigan "ruxsatnoma" artifact. Mohiyatan bu dependency darajasidagi Facade: bitta koordinatani qo'shib, butun ishlaydigan stack'ni olasiz.

**Spring'da qayerda uchraydi:** `spring-boot-starter-web`, `spring-boot-starter-webflux`, `spring-boot-starter-data-jpa`, `spring-boot-starter-security`, `spring-boot-starter-validation`, `spring-boot-starter-actuator`, `spring-boot-starter-test` va boshqalar; versiyalarni boshqaruvchi `spring-boot-dependencies` BOM hamda `spring-boot-starter-parent`. Uchinchi tomon uchun rasmiy nomlash konvensiyasi `xxx-spring-boot-starter` (Spring o'z nomini `spring-boot-starter-xxx` prefiksiga saqlab qo'ygan) va tavsiya etilgan struktura: alohida `xxx-spring-boot-autoconfigure` moduli + bo'sh `xxx-spring-boot-starter` moduli. Gradle'da BOM `platform(SpringBootPlugin.BOM_COORDINATES)` orqali ulanadi.

**Qo'llanish keyslari:**
- Kompaniya ichidagi umumiy observability, security va messaging sozlamalarini bitta internal starter'da tarqatish.
- Mikroservislar orasida kutubxona versiyalarini BOM orqali markazlashtirib boshqarish.
- Tomcat o'rniga Undertow yoki Jetty'ga o'tish uchun starter ichidagi exclusion'dan foydalanish.
- `spring-boot-starter-test` bilan JUnit 5, AssertJ, Mockito va Testcontainers integratsiyasini bir zarbada olish.
- SDK'ni mijoz jamoalarga "qo'sh va ishlat" shaklida yetkazish.

**Ehtiyot bo'ling:** Starter'ga biznes kodi yoki `@Component` sinflarini joylashtirmang - kod `autoconfigure` modulida, starter faqat POM/dependency bo'lib qolishi kerak, aks holda majburiy classpath bog'liqliklari paydo bo'ladi. BOM boshqargan versiyani qo'lda override qilish (`<spring-boot.version>` tashqarisida) runtime'da `NoSuchMethodError` kabi mos kelmaslik xatolarini keltiradi.

```java
// Starter: bog'liqliklar to'plami + auto-konfiguratsiya
// payments-spring-boot-starter/pom.xml - faqat bog'liqliklar, kod yo'q
// payments-spring-boot-autoconfigure/.../PaymentsAutoConfiguration.java:
@AutoConfiguration
@ConditionalOnClass(PspClient.class)
@EnableConfigurationProperties(PspProperties.class)
public class PaymentsAutoConfiguration {

    @Bean
    @ConditionalOnMissingBean            // foydalanuvchi o'zini bersa, biz tegmaymiz
    PaymentGateway paymentGateway(PspProperties props) {
        return new PspGateway(props);
    }
}
```

## 5.26 Auto-konfiguratsiya SPI ro'yxati (AutoConfiguration.imports / spring.factories SPI)

**Tavsif:** Spring Boot classpath'dagi barcha sinflarni skanerlab auto-konfiguratsiyalarni topmaydi - buning uchun har bir jar o'zining kirish nuqtalarini matnli ro'yxatda e'lon qiladi. Bu klassik Service Provider Interface (SPI) pattern: kontrakt framework'da, implementatsiya ro'yxati esa resurs faylida, natijada kengaytirish uchun kodga tegish kerak emas va startup tez qoladi. Spring buni Java'ning `ServiceLoader` mexanizmidan ilhomlanib, lekin o'z yuklovchisi bilan amalga oshiradi.

**Spring'da qayerda uchraydi:** Spring Boot 3.x'da auto-konfiguratsiyalar `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` faylida - har qatorda bitta to'liq sinf nomi (bu format 2.7'da kiritilib, 3.0'dan majburiy bo'ldi). Eski `META-INF/spring.factories` fayli esa boshqa kengaytirish nuqtalari uchun saqlanib qolgan: `EnvironmentPostProcessor`, `ApplicationContextInitializer`, `ApplicationListener`, `SpringApplicationRunListener`, `FailureAnalyzer`, `TemplateAvailabilityProvider`. Yuklovchi sinflar: `SpringFactoriesLoader`, `ImportCandidates`, `AutoConfigurationImportSelector`; metadata generatsiyasi uchun `spring-boot-autoconfigure-processor`.

**Qo'llanish keyslari:**
- O'z kutubxonangizning `@AutoConfiguration` sinfini imports fayliga yozib, mijoz loyihasida avtomatik faollashtirish.
- `EnvironmentPostProcessor` ni `spring.factories` orqali ro'yxatga olib, Vault yoki maxsus secret manbasini qo'shish.
- `FailureAnalyzer` bilan noto'g'ri konfiguratsiyaga tushunarli xato xabari berish.
- `ApplicationContextInitializer` orqali kontekst ko'tarilishidan oldin dinamik property qo'shish.
- Testda `AutoConfigurations.of(...)` bilan ro'yxatdan mustaqil ravishda auto-config'ni sinab ko'rish.

**Ehtiyot bo'ling:** Bu fayllardagi sinf nomlari oddiy matn - refactoring yoki paketni ko'chirish ularni jim buzadi va auto-konfiguratsiya shunchaki "yo'qoladi", hech qanday compile xatosi bermaydi; shuning uchun imports faylini `ApplicationContextRunner`siz emas, `@SpringBootTest` yoki `AutoConfigurations` testi bilan qoplang. Spring Boot 3.x'da auto-konfiguratsiyani faqat `spring.factories`da qoldirgan eski kutubxonalar umuman yuklanmaydi - migratsiyada shuni birinchi tekshiring.

```properties
# META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports
com.example.payments.PaymentsAutoConfiguration
com.example.payments.PaymentsMetricsAutoConfiguration

# Boot 2.7 gacha: META-INF/spring.factories ichida
# org.springframework.boot.autoconfigure.EnableAutoConfiguration=\
#   com.example.payments.PaymentsAutoConfiguration
```

## 5.27 Resurs abstraksiyasi (Resource Abstraction)

**Tavsif:** Fayl classpath'da, diskda, URL ortida yoki xotirada bo'lishi mumkin, lekin o'quvchi kodga faqat `InputStream` kerak. `Resource` interfeysi barcha bu manbalarni bitta kontraktga keltiradi (`getInputStream`, `exists`, `getFilename`, `getURL`), `ResourceLoader` esa prefiks (`classpath:`, `file:`, `http:`) bo'yicha mos implementatsiyani tanlaydi. Bu Strategy va Adapter patternlarining birikmasi bo'lib, kodni deploy modeliga bog'liqlikdan ozod qiladi.

**Spring'da qayerda uchraydi:** `org.springframework.core.io.Resource` va implementatsiyalari `ClassPathResource`, `FileSystemResource`, `UrlResource`, `ByteArrayResource`, `InputStreamResource`, `WritableResource`, web muhitida `ServletContextResource`. Yuklovchilar: `ResourceLoader`, `DefaultResourceLoader`, `FileSystemResourceLoader`, pattern qo'llab-quvvatlovchi `ResourcePatternResolver` va `PathMatchingResourcePatternResolver` (`classpath*:config/**/*.yml`), shuningdek `ResourceLoaderAware`, `ResourceUtils`. `@Value("classpath:schema.sql") Resource` ko'rinishidagi inject `ResourceEditor`/`ConversionService` orqali ishlaydi; Spring MVC statik fayllarni `ResourceHttpRequestHandler` va `spring.web.resources.*` sozlamalari bilan beradi.

**Qo'llanish keyslari:**
- Migratsiya yoki seed SQL fayllarini classpath'dan o'qib `ScriptUtils` bilan bajarish.
- Email yoki hujjat shablonlarini jar ichidan `ClassPathResource` orqali yuklash.
- `classpath*:` pattern bilan bir nechta modulning konfiguratsiya fragmentlarini topish.
- JWT public key yoki sertifikatni `file:` prefiksi bilan tashqi mount'dan olish.
- Test fiksturalarini bir xil kod bilan ham IDE'da, ham jar ichida o'qiydigan util yozish.

**Ehtiyot bo'ling:** Fat jar ichidagi classpath resursi haqiqiy fayl emas - `getFile()` yoki `resource.getFile().toPath()` lokalda ishlab, prod'da `FileNotFoundException` beradi; har doim `getInputStream()` dan foydalaning va uni try-with-resources bilan yoping. `classpath*:` bilan nested jar'larni skanerlash cheklangan va sekin, shuning uchun uni startup'da bir marta, hot path'da esa umuman ishlatmang.

```java
// Resource: fayl, classpath, URL va S3 bitta abstraksiya ortida
@Service
public class TemplateLoader {
    private final ResourceLoader loader;
    public TemplateLoader(ResourceLoader loader) { this.loader = loader; }

    public String load(String location) throws IOException {
        // "classpath:templates/x.html", "file:/etc/app/x.html", "https://..."
        Resource r = loader.getResource(location);
        if (!r.exists()) throw new FileNotFoundException(location);
        try (InputStream in = r.getInputStream()) {
            return new String(in.readAllBytes(), StandardCharsets.UTF_8);
        }
    }
}
```

## 5.28 Konvertatsiya xizmati (ConversionService / Converter / Formatter)

**Tavsif:** HTTP parametr, property fayl va UI form'dan kelgan ma'lumot ko'pincha `String`, ilova esa tipli obyekt kutadi. `Converter<S,T>` har bir yo'nalish uchun kichik, stateless strategiya beradi, `ConversionService` esa barcha converter'larni registry sifatida saqlab, kerakli juftlikni runtime'da tanlaydi; `Formatter<T>` bunga lokalizatsiya bilan "chop etish va o'qish" juftligini qo'shadi. Bu Strategy va Registry patternlarining birikmasi bo'lib, eski `PropertyEditor` mexanizmining thread-safe o'rnini bosgan.

**Spring'da qayerda uchraydi:** `Converter<S,T>`, `ConverterFactory`, `GenericConverter`, `ConditionalGenericConverter`; registry va servis tomonida `ConversionService`, `ConfigurableConversionService`, `DefaultConversionService`, `DefaultFormattingConversionService`, `ConversionServiceFactoryBean`, `FormattingConversionServiceFactoryBean`. Formatlash: `Formatter<T>`, `Printer`, `Parser`, `AnnotationFormatterFactory`, `@DateTimeFormat`, `@NumberFormat`. Web qatlamida `WebMvcConfigurer#addFormatters(FormatterRegistry)` va `WebDataBinder`, konfiguratsiya binding'ida maxsus converter'ni `@ConfigurationPropertiesBinding` bilan belgilash kerak; Spring Boot 3.x `ApplicationConversionService` orqali `Duration`, `DataSize`, `Period` kabi tiplarni qo'shadi.

**Qo'llanish keyslari:**
- URL path'dagi slug yoki ID'ni to'g'ridan-to'g'ri domen obyektiga aylantirish.
- Legacy API'dan kelgan maxsus sana formatini `Formatter` bilan ikki yo'nalishda o'qish va yozish.
- `@ConfigurationProperties` ichida `Money`, `Email` kabi value object'larni property satridan yasash.
- Enum'ning tashqi kodlarini (`"A1"`, `"B2"`) `ConverterFactory` bilan umumiy tarzda bog'lash.
- Thymeleaf form'larida lokalga mos son va sana ko'rinishini `@NumberFormat` orqali boshqarish.

**Ehtiyot bo'ling:** Web MVC ishlatadigan conversion service va property binding'dagi service alohida - faqat `@Component` sifatida ro'yxatga olingan converter avtomatik hamma joyda ishlamaydi, konfiguratsiya binding uchun `@ConfigurationPropertiesBinding` shart. Converter'lar singleton va ko'p thread'dan chaqiriladi, shuning uchun ularni mutable holat yoki thread-safe bo'lmagan `SimpleDateFormat` bilan yozmang; `java.time` va immutable mantiqdan foydalaning.

```java
// Converter: satr va domen turi orasidagi aylantirish bitta joyda
@Component
class StringToTenantIdConverter implements Converter<String, TenantId> {
    @Override public TenantId convert(String source) { return TenantId.of(source); }
}

// Ro'yxatga olinsa, @RequestParam, @PathVariable, @Value va
// @ConfigurationProperties binding'ida avtomatik ishlaydi:
@GetMapping("/tenants/{id}/orders")
List<Order> list(@PathVariable TenantId id) { return service.byTenant(id); }
```

## 5.29 Validator abstraksiyasi (Validator Abstraction)

**Tavsif:** Obyektni tekshirish mantiqini obyektning o'zidan va web qatlamidan ajratib, alohida strategiya sinfiga chiqaradi. `Validator` interfeysi `supports(Class<?>)` va `validate(Object, Errors)` metodlaridan iborat bo'lib, xatolar domain obyektiga emas, balki `Errors`/`BindingResult` kontekstiga yoziladi. Bu Strategy pattern'ining klassik ko'rinishi: bitta model uchun bir nechta kontekstga xos validator bo'lishi mumkin (create vs update). Spring shuningdek Jakarta Bean Validation (JSR-380) ni shu abstraksiya ustiga adapter orqali ulaydi.

**Spring'da qayerda uchraydi:** `org.springframework.validation.Validator`, `Errors`, `BeanPropertyBindingResult`, `ValidationUtils`, `SmartValidator`. Bean Validation ko'prigi - `LocalValidatorFactoryBean` va `SpringValidatorAdapter` (Hibernate Validator 8.x ustida). Web qatlamida `@Valid`/`@Validated` + `@InitBinder` ichidagi `WebDataBinder.addValidators(...)`, global holda `WebMvcConfigurer#getValidator()`. Service qatlamida metod darajasidagi tekshirish `MethodValidationPostProcessor` orqali; Spring Framework 6.1+ da bu `MethodValidationResult` bilan boyitilgan va Spring Boot 3.2+ da controller metodlari uchun ham ishlaydi. `@ConfigurationProperties` + `@Validated` esa konfiguratsiyani ishga tushishda tekshiradi.

**Qo'llanish keyslari:**
- Bir xil DTO uchun "yaratish" va "tahrirlash" senariylarida turlicha qoidalar qo'llash.
- Bean Validation annotatsiyalari bilan ifodalanmaydigan cross-field qoidalar (masalan `startDate < endDate`).
- Repository'ga murojaat qiladigan tekshiruvlar, masalan email unikalligi, buning uchun validator'ga bean inject qilinadi.
- `@ConfigurationProperties` orqali kelgan noto'g'ri sozlamada ilovani fail-fast holatda to'xtatish.
- Service qatlamida metod argumentlarini tekshirish, controller'dan tashqari chaqiruvlar uchun ham.

**Ehtiyot bo'ling:** Validator ichida tranzaksion yoki tashqi I/O chaqiruvlar qilish uni sekin va nozik qiladi - og'ir business qoidalarni domain service'ga qoldiring. `Errors` obyektiga xato qo'shish exception tashlamaydi, shuning uchun `BindingResult` ni controller'da tekshirmasang, noto'g'ri ma'lumot jimgina o'tib ketadi.

```java
// Bean Validation deklarativ, murakkab qoida uchun alohida Validator
public record TransferRequest(
        @NotNull Long from,
        @NotNull Long to,
        @NotNull @DecimalMin("0.01") BigDecimal amount) {}

@Component
class TransferValidator implements Validator {
    @Override public boolean supports(Class<?> c) { return TransferRequest.class == c; }

    @Override public void validate(Object target, Errors errors) {
        TransferRequest r = (TransferRequest) target;
        if (Objects.equals(r.from(), r.to())) {
            errors.reject("transfer.sameAccount", "O'zidan o'ziga o'tkazish mumkin emas");
        }
    }
}
```

## 5.30 Xabar manbasi va xalqarolashtirish (MessageSource / i18n)

**Tavsif:** Matnli xabarlarni kod ichidan chiqarib, kalit + locale juftligi bo'yicha tashqi manbadan oladigan yagona nuqta beradi. `MessageSource` interfeysi kalitni, argumentlarni va `Locale` ni qabul qilib, formatlangan satrni qaytaradi; yechilmagan kalit uchun default qiymat yoki `NoSuchMessageException`. Ichida `MessageFormat` va parent-child iyerarxiya (Chain of Responsibility ko'rinishi) ishlaydi: bola topmasa, ota manbadan izlanadi. Bu Service Locator va Strategy aralashmasi - xabar manbasini properties, DB yoki boshqa joyga almashtirish mumkin.

**Spring'da qayerda uchraydi:** `org.springframework.context.MessageSource`, `ResourceBundleMessageSource`, `ReloadableResourceBundleMessageSource`, `StaticMessageSource`, `MessageSourceAccessor`. `ApplicationContext` o'zi `MessageSource` ni extend qiladi, shuning uchun `applicationContext.getMessage(...)` ishlaydi. Spring Boot `messages.properties` ni avtomatik ulaydi (`spring.messages.basename`, `spring.messages.fallback-to-system-locale`). Locale aniqlash - `LocaleResolver` implementatsiyalari: `AcceptHeaderLocaleResolver`, `SessionLocaleResolver`, `CookieLocaleResolver` va `LocaleChangeInterceptor`. Validation xatolari `MessageCodesResolver` (`DefaultMessageCodesResolver`) orqali kalitlarga aylanadi; Thymeleaf'da `#{...}`, `ProblemDetail` matnlari uchun esa `ErrorResponse` + `MessageSource` birgalikda ishlaydi.

**Qo'llanish keyslari:**
- Ko'p tilli web UI yoki email template'larida foydalanuvchiga ko'rinadigan matnlarni locale bo'yicha berish.
- Validation xato matnlarini `messages.properties` da markazlashtirish va kodni o'zgartirmasdan tahrirlash.
- REST API'da `Accept-Language` header'iga qarab `ProblemDetail.detail` ni tarjima qilish.
- Pul, sana va son formatlarini locale'ga mos ravishda `MessageFormat` argumentlari bilan chiqarish.
- Xabar matnini DB yoki admin paneldan boshqarish uchun maxsus `AbstractMessageSource` yozish.

**Ehtiyot bo'ling:** `ResourceBundleMessageSource` fayllarni cache qiladi va JVM ishlab turganda qayta o'qimaydi - dev muhitda `ReloadableResourceBundleMessageSource` + `cacheSeconds` ishlatilsin. `fallback-to-system-locale=true` holati production'da serverning locale'iga qarab kutilmagan tilni qaytaradi; odatda uni `false` qilib, aniq default bundle qo'yish to'g'ri.

```java
@Bean
MessageSource messageSource() {
    ReloadableResourceBundleMessageSource ms = new ReloadableResourceBundleMessageSource();
    ms.setBasename("classpath:messages");      // messages_uz.properties, messages_ru...
    ms.setDefaultEncoding("UTF-8");
    ms.setFallbackToSystemLocale(false);       // kutilmagan tilga tushib qolmaslik
    return ms;
}

// Ishlatish: xabar matni kodda emas, resursda
String text = messageSource.getMessage("order.created",
        new Object[]{order.id()}, LocaleContextHolder.getLocale());
```

## 5.31 Vazifa bajaruvchi va rejalashtiruvchi (TaskExecutor / TaskScheduler)

**Tavsif:** "Nimani bajarish" va "qanday/qachon bajarish" masalalarini ajratadi: kod `Runnable`/`Callable` beradi, infrastruktura esa thread pool, virtual thread yoki sinxron bajarishni tanlaydi. `TaskExecutor` - `java.util.concurrent.Executor` ning Spring varianti (Strategy), `TaskScheduler` esa cron va fixed-rate rejalashtirishni abstraksiya qiladi. Buning foydasi: bir xil business kod test'da sinxron, production'da pool orqali ishlaydi - faqat bean almashtiriladi. `@Async` va `@Scheduled` esa bu abstraksiyani proxy orqali deklarativ qiladi.

**Spring'da qayerda uchraydi:** `org.springframework.core.task.TaskExecutor`, `SimpleAsyncTaskExecutor`, `SyncTaskExecutor`, `ThreadPoolTaskExecutor`, `VirtualThreadTaskExecutor` (Spring 6.1+), `ConcurrentTaskExecutor`. Rejalashtirish - `TaskScheduler`, `ThreadPoolTaskScheduler`, `SimpleTriggerContext`, `CronTrigger`, `PeriodicTrigger`. Deklarativ qatlam: `@EnableAsync` + `@Async` (`AsyncAnnotationBeanPostProcessor`), `@EnableScheduling` + `@Scheduled` (`ScheduledAnnotationBeanPostProcessor`), xatolar uchun `AsyncUncaughtExceptionHandler`. Spring Boot 3.2+ da `spring.threads.virtual.enabled=true` bilan `applicationTaskExecutor` va Tomcat virtual thread'larga o'tadi; `spring.task.execution.*` va `spring.task.scheduling.*` pool'larni sozlaydi. MVC'da `AsyncTaskExecutor` `Callable` qaytaruvchi controller'lar uchun ishlatiladi.

**Qo'llanish keyslari:**
- Email yuborish yoki audit yozish kabi javobni kutmaydigan ishlarni `@Async` bilan background'ga chiqarish.
- Kechasi ishlaydigan reconciliation yoki tozalash job'ini `@Scheduled(cron = ...)` bilan rejalashtirish.
- Bir nechta tashqi API chaqiruvini parallel bajarib, `CompletableFuture` orqali yig'ish.
- I/O og'ir workload uchun platform pool'dan virtual thread executor'ga o'tish.
- Testda `SyncTaskExecutor` ni inject qilib, asinxron kodni determinizmli sinash.

**Ehtiyot bo'ling:** `@Async` metodni o'sha sinf ichidan chaqirsang proxy aylanib o'tiladi va kod sinxron ishlaydi; shuningdek thread almashgani uchun `SecurityContext`, `RequestContext` va tranzaksiya avtomatik ko'chmaydi (`DelegatingSecurityContextAsyncTaskExecutor` kerak). Default `ThreadPoolTaskScheduler` pool size 1 - bir job cho'zilsa qolganlari kutib qoladi va bir nechta instansda `@Scheduled` har bir node'da takrorlanadi (ShedLock yoki Quartz kerak).

```java
@Configuration
@EnableAsync
@EnableScheduling
class AsyncConfig implements AsyncConfigurer {

    @Override
    public Executor getAsyncExecutor() {
        ThreadPoolTaskExecutor ex = new ThreadPoolTaskExecutor();
        ex.setCorePoolSize(8); ex.setMaxPoolSize(8); ex.setQueueCapacity(500);
        ex.setThreadNamePrefix("async-");
        ex.initialize();
        return ex;
    }

    @Override
    public AsyncUncaughtExceptionHandler getAsyncUncaughtExceptionHandler() {
        return (ex, method, params) -> log.error("async xato: {}", method, ex);
    }
}
```

## 5.32 Tranzaksiya sinxronizatsiyasi (TransactionSynchronization)

**Tavsif:** Tranzaksiyaning hayot tsikliga - commit oldidan, commit keyin, rollback'da va yopilishda - o'z kodini ulash imkonini beradi. Bu Observer/callback pattern'i: ishtirokchilar `TransactionSynchronizationManager` ga ro'yxatdan o'tadi va tranzaksiya menejeri mos momentda ularni chaqiradi. Asosiy maqsad - tranzaksiyadan tashqaridagi ta'sirlarni (xabar yuborish, cache tozalash) faqat commit muvaffaqiyatli bo'lganda bajarish, ya'ni dual-write muammosini kamaytirish. U shuningdek resurslarni (Connection, EntityManager) thread'ga bog'lab, bir tranzaksiya ichida qayta ishlatish uchun ham ishlatiladi.

**Spring'da qayerda uchraydi:** `org.springframework.transaction.support.TransactionSynchronization`, `TransactionSynchronizationAdapter`, `TransactionSynchronizationManager`, `TransactionTemplate`, `PlatformTransactionManager`. Deklarativ varianti - `@TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)` va `ApplicationEventPublisher`; Spring Data domain event'lari `@DomainEvents` + `AbstractAggregateRoot` orqali shu mexanizmdan foydalanadi. JPA integratsiyasida `EntityManagerHolder`, JDBC'da `DataSourceUtils.getConnection(...)` ayni shu resource binding'ga tayanadi. Spring Modulith esa `@ApplicationModuleListener` ni transaction-after-commit semantikasi bilan beradi.

**Qo'llanish keyslari:**
- Entity saqlangandan keyin, faqat commit bo'lsa Kafka yoki RabbitMQ'ga event yuborish.
- Commit'dan keyin Redis cache yoki search index'ni invalidate qilish.
- Rollback bo'lganda yuklangan vaqtinchalik faylni o'chirish yoki tashqi rezervatsiyani bekor qilish.
- Audit yozuvini `beforeCommit` da qo'shib, u ham bir xil tranzaksiyaga tushishini ta'minlash.
- Outbox jadvaliga yozib, publisher'ni `afterCommit` da trigger qilish.

**Ehtiyot bo'ling:** `afterCommit` callback'i tranzaksiyadan tashqarida ishlaydi - u yerda DB'ga yozsang yangi tranzaksiya kerak (`REQUIRES_NEW`), aks holda o'zgarish yo'qoladi; callback ichidagi exception esa commit'ni ortga qaytarmaydi. Qo'lda `registerSynchronization` chaqirishdan oldin `isSynchronizationActive()` ni tekshir, aks holda `IllegalStateException` olasan.

```java
// Tranzaksiya commit'idan keyin ish bajarish (resurs yopish, xabar yuborish)
@Service
public class OutboxPublisher {

    @Transactional
    public void save(Order order) {
        repo.save(order);
        TransactionSynchronizationManager.registerSynchronization(
                new TransactionSynchronization() {
                    @Override public void afterCommit() {
                        broker.send(new OrderPlaced(order.id()));   // faqat commit bo'lsa
                    }
                });
    }
}
// Odatda @TransactionalEventListener(AFTER_COMMIT) toza va o'qilishi oson
```

## 5.33 DataAccessException iyerarxiyasi va exception tarjimasi (DataAccessException Hierarchy / Exception Translation)

**Tavsif:** Har bir ma'lumot manbasining o'ziga xos xatolarini (JDBC `SQLException` va vendor error code'lari, JPA `PersistenceException`, Mongo xatolari) yagona, texnologiyadan mustaqil runtime exception daraxtiga aylantiradi. Bu Adapter va Translator pattern'i: business kod `SQLState` yoki vendor kodini bilmasdan `DuplicateKeyException` yoki `OptimisticLockingFailureException` ni tutadi. Barchasi unchecked bo'lgani uchun DAO imzolari `throws` bilan ifloslanmaydi va qatlamlar o'rtasida almashish osonlashadi.

**Spring'da qayerda uchraydi:** `org.springframework.dao.DataAccessException` va uning avlodlari: `DataIntegrityViolationException`, `DuplicateKeyException`, `EmptyResultDataAccessException`, `OptimisticLockingFailureException`, `CannotAcquireLockException`, `QueryTimeoutException`, `DeadlockLoserDataAccessException`. Tarjimonlar - `SQLExceptionTranslator`, `SQLErrorCodeSQLExceptionTranslator` (`sql-error-codes.xml`), `SQLStateSQLExceptionTranslator`, `SQLExceptionSubclassTranslator`, `PersistenceExceptionTranslator`. Avtomatik ulash: `@Repository` + `PersistenceExceptionTranslationPostProcessor` (Spring Boot'da avtomatik), `JdbcTemplate`, `JdbcClient` (Spring 6.1+), `NamedParameterJdbcTemplate` va Spring Data repository'lari ham shu iyerarxiyani qaytaradi.

**Qo'llanish keyslari:**
- Unique constraint buzilishini `DuplicateKeyException` orqali tutib, 409 Conflict qaytarish.
- `@Version` bilan optimistic lock konfliktida `OptimisticLockingFailureException` ni ushlab, operatsiyani qayta urinish.
- Deadlock yoki lock timeout'ni `TransientDataAccessException` bo'yicha ajratib, faqat shu holatda retry qilish.
- JDBC'dan JPA'ga yoki aksincha ko'chganda catch bloklarini o'zgartirmaslik.
- `@RestControllerAdvice` da `DataAccessException` ni yagona `ProblemDetail` javobga aylantirish.

**Ehtiyot bo'ling:** Tarjima avtomatik emas - oddiy POJO DAO'da `EntityManager` ni to'g'ridan-to'g'ri ishlatsang, `@Repository` yoki translation post-processor bo'lmasa, native `PersistenceException` chiqadi. Shuningdek `DataIntegrityViolationException` ni "duplicate" deb taxmin qilish xato: u foreign key, not-null va check constraint'lar uchun ham keladi, shuning uchun sabab bo'yicha aniqlashtirish kerak.

```java
// Exception tarjimasi: SQLException emas, ma'noli tur
@Service
public class AccountService {

    public void create(Account a) {
        try {
            dao.insert(a);
        } catch (DuplicateKeyException e) {          // DataAccessException ierarxiyasi
            throw new AccountAlreadyExistsException(a.email(), e);
        } catch (CannotAcquireLockException e) {     // deadlock yoki lock timeout
            throw new RetryableAccountException(e);
        }
    }
}
// Tarjimani Spring bajaradi: tashqi kod JDBC vendor kodlarini bilmaydi
```

## 5.34 Cache abstraksiyasi (Cache Abstraction / @Cacheable Proxy)

**Tavsif:** Caching mantiqini business kodga aralashtirmasdan, metod chaqiruvini AOP proxy bilan o'rab, natijani kalit bo'yicha saqlaydi va keyingi chaqiruvda qaytaradi. `Cache` va `CacheManager` interfeyslari Strategy sifatida ishlaydi: Caffeine, Redis, Hazelcast yoki oddiy `ConcurrentHashMap` kodga ta'sir qilmasdan almashtiriladi. Kalit `KeyGenerator` yoki SpEL ifodasi bilan hosil qilinadi, shartlar `condition` va `unless` bilan beriladi. Bu klassik Proxy + Decorator kombinatsiyasi.

**Spring'da qayerda uchraydi:** `@EnableCaching`, `@Cacheable`, `@CachePut`, `@CacheEvict`, `@Caching`, `@CacheConfig`; infrastruktura - `CacheManager`, `Cache`, `CacheInterceptor`, `CacheAspectSupport`, `KeyGenerator`, `SimpleKeyGenerator`, `CacheResolver`, `CacheErrorHandler`. Implementatsiyalar: `ConcurrentMapCacheManager`, `CaffeineCacheManager`, `RedisCacheManager` (`RedisCacheConfiguration` bilan TTL), `JCacheCacheManager`, `CompositeCacheManager`. Spring Boot `spring.cache.type` va `spring.cache.cache-names` bilan auto-konfiguratsiya qiladi; `CacheManagerCustomizer` sozlashga imkon beradi. Spring Framework 6.2+ da `@Cacheable` reactive `Mono`/`Flux` bilan ham ishlay oladi.

**Qo'llanish keyslari:**
- Kam o'zgaradigan reference ma'lumot (davlatlar, tariflar) uchun DB yuklamasini kamaytirish.
- Sekin tashqi API javoblarini TTL bilan Redis'da saqlash.
- Og'ir hisob-kitob natijasini (report aggregate) metod darajasida memoize qilish.
- Ma'lumot yangilanganda `@CacheEvict(allEntries = true)` bilan bog'liq cache'ni tozalash.
- `@CachePut` orqali yozish operatsiyasi natijasini cache'ga darhol yozib qo'yish.

**Ehtiyot bo'ling:** Proxy orqali ishlagani uchun self-invocation va `private`/`final` metodlar cache'lanmaydi; mutable obyektni local cache'da saqlash esa chaqiruvchi uni o'zgartirsa, cache'ni ham buzadi. Distributed cache'da serializatsiya sxemasi va TTL'ni aniq belgilash kerak, aks holda `null` yoki eski ma'lumot uzoq yashaydi; `sync = true` bo'lmasa cache stampede yuz beradi.

```java
@Service
public class RateService {

    @Cacheable(cacheNames = "rates", key = "#from + '-' + #to", sync = true)
    public BigDecimal rate(String from, String to) {
        return cbuClient.fetchRate(from, to);       // sync = true: stampede himoyasi
    }

    @CacheEvict(cacheNames = "rates", allEntries = true)
    @Scheduled(cron = "0 5 9 * * *")
    public void refreshDaily() { }
}
// @Cacheable proxy orqali: o'z sinfi ichidan chaqirilsa kesh ishlamaydi
```

## 5.35 Spring Retry va @Retryable (Spring Retry / @Retryable)

**Tavsif:** Vaqtinchalik xatolarda operatsiyani belgilangan siyosat bo'yicha qayta urinishni deklarativ qiladi. Retry siyosati (necha marta, qaysi exception'larda) va backoff siyosati (fixed, exponential, jitter) alohida Strategy sifatida ajratilgan, urinishlar tugaganda `@Recover` metodi fallback beradi. Shuningdek Circuit Breaker ko'rinishi ham bor: ketma-ket xatolardan keyin chaqiruvlar ma'lum vaqt to'xtatiladi. Bu Retry va Circuit Breaker pattern'larining AOP proxy orqali ifodasi.

**Spring'da qayerda uchraydi:** `spring-retry` kutubxonasi - `@EnableRetry`, `@Retryable`, `@Recover`, `@Backoff`, `@CircuitBreaker`; imperativ API: `RetryTemplate`, `RetryPolicy` (`SimpleRetryPolicy`, `ExceptionClassifierRetryPolicy`), `BackOffPolicy` (`ExponentialBackOffPolicy`, `ExponentialRandomBackOffPolicy`), `RetryCallback`, `RecoveryCallback`, `RetryListener`. Spring Framework 7.0 core'ga `org.springframework.core.retry.RetryTemplate`/`RetryPolicy` va `@Retryable` qo'shildi, shuning uchun yangi loyihalarda tashqi kutubxonaga ehtiyoj kamayadi. Shuningdek `@Retryable` Spring Boot 3.x da `spring-retry` dependency qo'shilganda ishlaydi; Resilience4j (`@CircuitBreaker`, `@RateLimiter`) muqobil yechim, Spring Kafka va Spring AMQP esa `RetryTemplate` ni ichida ishlatadi.

**Qo'llanish keyslari:**
- Tashqi HTTP API'dagi 503 yoki timeout'da exponential backoff bilan qayta urinish.
- DB deadlock yoki optimistic lock konfliktida tranzaksiyani qaytadan bajarish.
- Kafka consumer'da xabarni bir necha marta urinib, keyin DLT'ga yuborish.
- Ishga tushishda bog'liq servisning hozir bo'lishini kutib, ulanishni qayta sinash.
- `@Recover` bilan cache'dagi eski qiymatni yoki default javobni fallback qilib berish.

**Ehtiyot bo'ling:** Idempotent bo'lmagan operatsiyani retry qilish dublikat to'lov yoki ikki marta yozuv hosil qiladi - avval idempotentlikni ta'minlang. `@Retryable` ni `@Transactional` metodga qo'yish tartibi muhim: retry tranzaksiyadan tashqarida bo'lmasa, allaqachon rollback-only belgilangan tranzaksiya ichida qayta urinish foydasiz, shuningdek uzun backoff thread'ni va HTTP timeout budjetini yeb qo'yadi.

```java
@Service
public class PspClient {

    @Retryable(retryFor = {ConnectException.class, SocketTimeoutException.class},
               maxAttempts = 3,
               backoff = @Backoff(delay = 200, multiplier = 2, random = true))
    public Receipt charge(Payment p) {
        return rest.post().uri("/charge").body(p).retrieve().body(Receipt.class);
    }

    @Recover
    public Receipt fallback(ConnectException e, Payment p) {
        return Receipt.pending(p.id());     // retry tugagach chaqiriladi
    }
}
// Faqat idempotent operatsiyaga retry qo'ying. random = true - jitter.
```

## 5.36 Spring ifoda tili (Spring Expression Language / SpEL)

**Tavsif:** Runtime'da obyekt grafini so'rash va ifoda hisoblash uchun kichik til beradi: property navigatsiyasi, metod chaqirish, arifmetika, kolleksiya proyeksiya/selection va bean murojaatlari. Arxitektura jihatidan bu Interpreter pattern'i - ifoda `Expression` AST'ga parse qilinadi, so'ngra `EvaluationContext` ustida hisoblanadi. Shu sababli bir marta parse qilib, ko'p marta turli kontekstlarda ishlatish mumkin. Spring uni annotatsiya qiymatlari, security qoidalari va cache kalitlari uchun ichki "plugin" tili sifatida ishlatadi.

**Spring'da qayerda uchraydi:** `org.springframework.expression.spel.standard.SpelExpressionParser`, `Expression`, `EvaluationContext`, `StandardEvaluationContext`, `SimpleEvaluationContext`, `BeanFactoryResolver`. Ishlatilish joylari: `@Value("#{...}")` va `${...}` property placeholder'lari, `@Cacheable(key = "#id")`, `@Cacheable(condition/unless)`, `@PreAuthorize("hasRole('ADMIN') and #id == authentication.name")` (Spring Security), `@ConditionalOnExpression`, `@EventListener(condition = "#event.important")`, `@Scheduled(cron = "${...}")` bilan birga, Spring Data `@Query` ichida `?#{...}` va `SpEL` kengaytmalari, Spring Integration router/filter ifodalari. Spring Framework 6.2+ da `SpelCompilerMode` va ifoda uzunligi/chuqurligi bo'yicha himoya limitlari mavjud.

**Qo'llanish keyslari:**
- `@Value` orqali property qiymatini hisoblash yoki default berish, masalan ro'yxatni ajratish.
- Cache kalitini bir nechta argumentdan tuzish va `unless` bilan `null` natijani cache'lamaslik.
- Method security'da resurs egasini `#id` va `authentication` orqali tekshirish.
- Event listener'ni faqat ma'lum shartli event'larda ishga tushirish.
- Spring Data query'siga joriy foydalanuvchi yoki tenant id'sini ifoda bilan uzatish.

**Ehtiyot bo'ling:** Foydalanuvchi kiritgan matnni SpEL ifodasi sifatida hisoblash - jiddiy RCE xavfi; bunday holatda `SimpleEvaluationContext` (reflection va bean access cheklangan) ishlating yoki butunlay voz keching. Murakkab biznes mantiqni annotatsiya satriga yozish compile-time tekshiruvdan va refactoring'dan chetda qoladi, shuning uchun ifodalarni qisqa tutib, mantiqni Java metodiga chiqarish ma'qul.

```java
// SpEL: konfiguratsiya va annotatsiya ichida ifoda
@Value("#{systemEnvironment['PSP_URL'] ?: 'http://localhost:8080'}")
private String pspUrl;

@Scheduled(cron = "#{@schedulingProperties.settlementCron}")
public void settle() { }

@PreAuthorize("hasRole('ADMIN') or #order.customerId == authentication.name")
public void cancel(Order order) { }

// Ishonchsiz manbadan kelgan satrni SpEL da bajarmang: u ixtiyoriy Java chaqiradi
```

## 5.37 @Import, ImportSelector va registrar (@Import / ImportSelector / ImportBeanDefinitionRegistrar)

**Tavsif:** Konfiguratsiyani kompozitsiya qilish va bean definition'larni programmatik ravishda ro'yxatdan o'tkazish mexanizmi. `@Import` boshqa `@Configuration` sinflarini qo'shadi, `ImportSelector` esa metadata va muhitga qarab qaysi konfiguratsiya sinflari yuklanishini runtime'da tanlaydi, `ImportBeanDefinitionRegistrar` to'g'ridan-to'g'ri `BeanDefinition` yaratadi. Bu Builder va Factory pattern'larining konfiguratsiya darajasidagi ko'rinishi: yakuniy kontekst "tarkibi" qoidalar bo'yicha yig'iladi. `DeferredImportSelector` esa tanlovni foydalanuvchi konfiguratsiyasidan keyinga suradi.

**Spring'da qayerda uchraydi:** `@Import`, `ImportSelector`, `DeferredImportSelector`, `ImportBeanDefinitionRegistrar`, `ImportAware`, `AnnotationMetadata`, `BeanDefinitionRegistry`, `BeanDefinitionBuilder`. Spring Boot'ning butun auto-configuration mexanizmi `AutoConfigurationImportSelector` (`DeferredImportSelector`) va `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` fayliga tayanadi. `@EnableCaching`, `@EnableAsync`, `@EnableTransactionManagement`, `@EnableWebSecurity` kabi `@Enable*` annotatsiyalar `@Import` ustida qurilgan (`AdviceModeImportSelector`, `*ConfigurationSelector`). `@MapperScan` (MyBatis) va `@EnableFeignClients` registrar orqali dinamik proxy bean'larni ro'yxatdan o'tkazadi.

**Qo'llanish keyslari:**
- Kompaniya ichidagi starter yozish: bitta `@Enable*` annotatsiya ortida bir nechta konfiguratsiyani yuklash.
- Muhit yoki property qiymatiga qarab turli implementatsiya konfiguratsiyasini tanlash.
- Interfeys skanerlab, har biri uchun dinamik proxy bean definition yaratish.
- Legacy XML yoki uchinchi tomon konfiguratsiyasini `@Import` bilan modulga biriktirish.
- Test uchun faqat kerakli slice konfiguratsiyalarini `@Import` bilan yig'ish.

**Ehtiyot bo'ling:** `ImportSelector` va registrar lifecycle'ning juda erta fazasida ishlaydi - ularga oddiy bean inject qilinmaydi, faqat `Environment`, `ResourceLoader`, `BeanFactory`, `BeanClassLoader` aware interfeyslari orqali resurs olinadi. Registrar'da qo'lda yaratilgan bean definition'lar `@ConditionalOn*` va ordering qoidalarini chetlab o'tishi mumkin, shu sababli odatdagi holatlarda `@Bean` + `@Conditional` yetarli bo'lsa, bu mexanizmdan foydalanmaslik soddaroq.

```java
// ImportSelector: qaysi konfiguratsiya yuklanishini runtime'da tanlash
public class StorageSelector implements ImportSelector {
    @Override
    public String[] selectImports(AnnotationMetadata meta) {
        boolean s3 = Boolean.parseBoolean(System.getProperty("storage.s3", "false"));
        return new String[]{ s3 ? S3StorageConfig.class.getName()
                                : LocalStorageConfig.class.getName() };
    }
}

@Configuration
@Import(StorageSelector.class)
class StorageConfig { }
```

## 5.38 Meta-annotatsiyalar va kompozit annotatsiyalar (Meta-annotations / Composed Annotations)

**Tavsif:** Bir nechta annotatsiyani bitta yangi annotatsiya ortiga yashirib, takrorlanuvchi konfiguratsiyani nomlangan, bir joyda boshqariladigan abstraksiyaga aylantiradi. Spring annotatsiyalarni "merged" ko'rinishda o'qiydi: meta-annotatsiya atributlari `@AliasFor` orqali ustki annotatsiyaga chiqariladi, shuning uchun o'z annotatsiyangiz standart annotatsiya bilan bir xil kuchga ega bo'ladi. Bu Facade va Decorator'ning deklarativ varianti - semantikani kengaytirmay, uni qulay nom ostida qayta ishlatish.

**Spring'da qayerda uchraydi:** `org.springframework.core.annotation.AnnotatedElementUtils`, `MergedAnnotations`, `AnnotationUtils`, `@AliasFor`. Spring o'zida ko'p: `@RestController` = `@Controller` + `@ResponseBody`, `@GetMapping` = `@RequestMapping(method = GET)`, `@SpringBootApplication` = `@SpringBootConfiguration` + `@EnableAutoConfiguration` + `@ComponentScan`, `@Service`/`@Repository` = `@Component`, `@SpringBootTest` slice'lari (`@WebMvcTest`, `@DataJpaTest`), Spring Security'da `@PreAuthorize` ustida qurilgan maxsus annotatsiyalar. `@Transactional` ni meta-annotatsiya qilib `@ReadOnlyTransaction` yaratish ham odatiy amaliyot.

**Qo'llanish keyslari:**
- `@ReadOnlyTx` kabi annotatsiya yozib, `@Transactional(readOnly = true, timeout = 5)` ni bir joyda standartlashtirish.
- Security qoidalarini `@IsAdmin` yoki `@IsResourceOwner` sifatida nomlab, SpEL ifodalarini takrorlamaslik.
- Test slice'larini kompaniya standartlariga mos `@IntegrationTest` annotatsiyasi ostida birlashtirish.
- API versiyalash uchun `@V1GetMapping` kabi path prefiksi bilan kompozit mapping yaratish.
- Observability annotatsiyalarini (`@Observed`, `@Timed`) biznes semantikasi bilan birlashtirish.

**Ehtiyot bo'ling:** Chuqur annotatsiya iyerarxiyasi kodni "sehrli" qiladi - o'quvchi haqiqiy xatti-harakatni ko'rish uchun bir necha fayl ochishga majbur bo'ladi, shuning uchun 2-3 ta annotatsiyani birlashtirishdan nariga ketmaslik ma'qul. Atributni ustki annotatsiyaga chiqarish uchun `@AliasFor` shart; `@Retention(RUNTIME)` ni unutsang annotatsiya umuman ko'rinmaydi va standart `java.lang.reflect` chaqiruvlari merged semantikani bilmaydi - `AnnotatedElementUtils` ishlatilsin.

```java
// Meta-annotatsiya: takrorlanuvchi annotatsiya to'plamini bitta nom ostiga yig'ish
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@Transactional(readOnly = true, timeout = 10)
@Service
public @interface QueryService { }

// Ishlatish: niyat bitta nomda ko'rinadi
@QueryService
public class OrderQueryService {
    public List<OrderSummary> recent() { /* ... */ }
}
```

## 5.39 Konfiguratsiyadan ustun konvensiya (Convention over Configuration)

**Tavsif:** Eng ko'p uchraydigan holat uchun aniq konfiguratsiyani umuman talab qilmaslik, faqat chetga chiqishni e'lon qilishni so'rash printsipi. Framework oqilona default'lar beradi, nomlash qoidalari va classpath tarkibidan xulosa chiqaradi, foydalanuvchi esa faqat kerakli joyini override qiladi. Bu Template Method va Strategy'ning konfiguratsiya darajasidagi natijasi: "boilerplate nolga yaqin, lekin escape hatch bor". Natijada loyihalar bir-biriga o'xshaydi va yangi injenerning kirish narxi tushadi.

**Spring'da qayerda uchraydi:** Spring Boot auto-configuration (`@ConditionalOnClass`, `@ConditionalOnMissingBean`, `@ConditionalOnProperty`), `application.yml`/`application.properties` va `spring.config.import`, standart papkalar `src/main/resources/static`, `templates`, `META-INF/resources`. Qo'shimcha: `@SpringBootApplication` joylashgan paketdan boshlab component scan, `schema.sql`/`data.sql` va Flyway'ning `db/migration` jildi, `messages.properties` basename, Spring Data'da metod nomidan query hosil qilish (`findByEmailAndActiveTrue`), JPA'da sinf nomidan jadval nomi, `application-{profile}.yml` profil fayllari, `banner.txt`. Spring Boot 3.x da `spring-configuration-metadata.json` IDE autocomplete uchun shu konvensiyalarni ta'minlaydi.

**Qo'llanish keyslari:**
- Yangi mikroservisni minimal konfiguratsiya bilan ishga tushirib, faqat datasource URL'ni berish.
- `@ConditionalOnMissingBean` yordamida default bean berib, foydalanuvchiga uni almashtirish imkonini qoldirish.
- Profil fayllari bilan dev/stage/prod sozlamalarini kod o'zgartirmasdan ajratish.
- Spring Data derived query'lar bilan oddiy CRUD repository'larni SQL yozmasdan olish.
- Ichki starter yaratib, jamoadagi barcha servislarga bir xil observability va security default'larini berish.

**Ehtiyot bo'ling:** Default'lar ko'rinmas bo'lgani uchun muammo chiqqanda sabab noma'lum tuyuladi - `--debug` yoki `ConditionEvaluationReport` bilan nima yuklanganini tekshirishni o'rganish kerak. Production uchun muhim parametrlarni (pool size, timeout, `open-in-view`, `ddl-auto`) default holatida qoldirmang: ular qulaylik uchun tanlangan, yuklama uchun emas.

```java
// Konvensiya: nom to'g'ri bo'lsa, konfiguratsiya kerak emas
// application.yml (nom bo'yicha topiladi), schema.sql, data.sql,
// src/main/resources/templates/ (Thymeleaf), static/ (statik fayllar)

public interface OrderRepository extends JpaRepository<Order, Long> {
    // Metod nomidan so'rov tuziladi: @Query yozish kerak emas
    List<Order> findByStatusAndCreatedAtAfter(OrderStatus status, Instant since);
}
// Konvensiya buzilgan joyda esa aniq konfiguratsiya yozing: yashirin sehr emas
```

## 5.40 Spring'da Null Object qo'llanishi (Null Object Usage in Spring)

**Tavsif:** `null` yoki shart tekshirishlar o'rniga interfeysni "hech nima qilmaydigan" xatti-harakat bilan amalga oshiruvchi obyekt beradi. Chaqiruvchi kod har joyda `if (x != null)` yozmaydi, chunki no-op implementatsiya kutilgan shartnomani bajaradi, lekin hech qanday ta'sir qoldirmaydi. Spring bundan ko'pincha xususiyatni o'chirish yoki test/dev muhiti uchun placeholder sifatida foydalanadi. Bu Strategy pattern'ining degenerativ, lekin juda foydali holati.

**Spring'da qayerda uchraydi:** `org.springframework.cache.support.NoOpCacheManager` va `NoOpCache` (`spring.cache.type=none`), `org.springframework.security.crypto.password.NoOpPasswordEncoder` (deprecated, faqat legacy uchun), `org.springframework.core.task.SyncTaskExecutor` (asinxronlikni yo'q qiladigan variant), Micrometer'dagi `NoopMeterRegistry` va `SimpleMeterRegistry`, `io.micrometer.tracing.otel`/`brave` o'rniga `Tracer.NOOP`, `org.springframework.validation.beanvalidation` o'rniga validator'siz konfiguratsiya, `MethodInterceptor` zanjirlaridagi bo'sh advice. Shuningdek `ResourceLoader` uchun `DefaultResourceLoader` va `StaticMessageSource` bo'sh default sifatida ishlatiladi; Spring Boot `spring.main.banner-mode=off` kabi sozlamalar ham shu g'oyaga yaqin.

**Qo'llanish keyslari:**
- Lokal profil yoki testda caching'ni `NoOpCacheManager` bilan o'chirib, kodni o'zgartirmaslik.
- Metrikalar yoqilmagan muhitda `Tracer.NOOP` berib, instrumentatsiya kodini saqlab qolish.
- Feature flag o'chirilganda interfeysning no-op implementatsiyasini inject qilish.
- Xabar yuborish servisining dev muhitdagi "log-only" yoki "do-nothing" variantini berish.
- Test'da notifikatsiya yoki audit yon ta'sirlarini butunlay neytrallash.

**Ehtiyot bo'ling:** `NoOpPasswordEncoder` ni production'da ishlatish parolni ochiq matnda saqlash bilan teng - u faqat migratsiya davrida, `DelegatingPasswordEncoder` ortida va muddatli reja bilan ishlatilishi mumkin. No-op implementatsiya xatolarni jimgina yutib, muammoni yashirishi mumkin, shuning uchun uni kutilgan joyda ekanini log yoki startup xabari bilan ko'rsatish foydali.

```java
// Spring'dagi tayyor Null Object'lar: imkoniyatni o'chirish uchun
@Bean
@ConditionalOnProperty(name = "cache.enabled", havingValue = "false")
CacheManager noOpCacheManager() {
    return new NoOpCacheManager();     // @Cacheable ishlaydi, lekin keshlamaydi
}

// Shu yondashuv tufayli chaqiruvchi kodda `if (cacheEnabled)` yozilmaydi.
```

## 5.41 Spring'dagi fluent DSL builder'lar (Fluent DSL Builders in Spring)

**Tavsif:** Murakkab obyektni yoki konfiguratsiyani bosqichma-bosqich, zanjirli metod chaqiruvlari bilan yig'ishga imkon beradi: har bir chaqiruv `this` yoki yangi bosqichni qaytaradi, oxirida `build()` yoki terminal operatsiya natija beradi. Bu Builder pattern'ining o'qiladigan DSL ko'rinishi; ko'p argumentli konstruktorlar va mutable setter'lar o'rnini bosadi, shuningdek IDE autocomplete orqali konfiguratsiya "yo'l xaritasini" ko'rsatadi. Immutable natija qaytaradigan builder'lar thread-safe qayta ishlatishni ham osonlashtiradi.

**Spring'da qayerda uchraydi:** HTTP klientlari - `RestClient.builder()` (Spring 6.1+), `WebClient.builder()`, `RestTemplateBuilder` (Spring Boot), `RestClient.Builder#requestInterceptor`, `HttpRequest`/`RequestEntity.method(...).headers(...).body(...)`, `UriComponentsBuilder`. Security - `HttpSecurity` DSL (`http.authorizeHttpRequests(a -> a.requestMatchers(...).hasRole(...)).oauth2ResourceServer(...)`) va `SecurityFilterChain` bean'lari, `AuthenticationManagerBuilder`. Boshqalar: `SpringApplicationBuilder`, `MockMvcRequestBuilders` / `MockMvcResultMatchers` va `WebTestClient`, `BeanDefinitionBuilder`, `ProblemDetail.forStatusAndDetail(...)`, `RouterFunctions.route()` (WebFlux/WebMvc.fn), `IntegrationFlow` DSL (Spring Integration), `JdbcClient.sql(...).param(...).query(...)`, `ChatClient.create(model).prompt()...` (Spring AI).

```java
SecurityFilterChain chain(HttpSecurity http) throws Exception {
    return http
        .authorizeHttpRequests(a -> a
            .requestMatchers("/actuator/health").permitAll()
            .anyRequest().authenticated())
        .oauth2ResourceServer(o -> o.jwt(Customizer.withDefaults()))
        .csrf(CsrfConfigurer::disable)
        .build();
}
```

**Qo'llanish keyslari:**
- Har bir tashqi servis uchun alohida `RestClient` ni base URL, header va timeout bilan tuzish.
- Lambda DSL yordamida o'qiladigan `SecurityFilterChain` konfiguratsiyasini yozish.
- `MockMvc` yoki `WebTestClient` bilan integratsion testlarni zanjirli assertion'lar orqali ifodalash.
- `UriComponentsBuilder` bilan query parametrlarini to'g'ri encode qilib URL yig'ish.
- `SpringApplicationBuilder` bilan parent-child kontekst yoki banner/profil sozlamalarini programmatik berish.

**Ehtiyot bo'ling:** Builder'ni chaqiruvlar orasida qayta ishlatishda mutable/immutable semantikasini aniq bilish kerak - `RestClient.Builder` ni `clone()` qilmasdan bir nechta joyda o'zgartirsang, sozlamalar bir-biriga oqib ketadi. `HttpSecurity` DSL'da tartib va matcher'lar aniqligi muhim: kengroq `requestMatchers` ni oldin yozib qo'ysang, keyingi qat'iyroq qoidalar hech qachon ishlamaydi, shuning uchun eng aniq matcher'lar yuqorida turishi lozim.

## 5.42 Amalda qo'llash

- [ ] `applicationContext.getBean(...)` va `BeanFactoryAware` ishlatadigan joylarni qidirib, har birini injeksiyaga aylantirish rejasini yozing.
- [ ] Bir interfeysga bir nechta implementatsiya bo'lgan joylarni toping va `@Primary` yoki `@Qualifier` aniq qo'yilganini tasdiqlang.
- [ ] `@PostConstruct` ichida tashqi chaqiruv yoki uzoq ish bajaradigan bean'larni toping; ular startup'ni va readiness probe'ni buzadi.
- [ ] `BeanPostProcessor` va `BeanFactoryPostProcessor` implementatsiyalarini sanab chiqing va har birining `@Order` qiymatini yozib qo'ying.
- [ ] Request yoki session scope'dagi bean'lar singleton ichiga inject qilingan joylarni tekshirib, scoped proxy ishlatilganini tasdiqlang.
- [ ] `@ConfigurationProperties` sinflarini `@Validated` bilan qoplab, noto'g'ri konfiguratsiya startup'da yiqitishini ta'minlang.
- [ ] `@EventListener` larni ko'rib chiqing va tranzaksiya commit'idan keyin ishlashi kerak bo'lganlarini `@TransactionalEventListener` ga o'tkazing.
- [ ] Auto-konfiguratsiya qaroriga ta'sir qilgan shartlarni `--debug` rejimidagi `ConditionEvaluationReport` dan eksport qilib, hujjatlashtirib qo'ying.

---

[&larr; 4. Concurrency patternlari](04-concurrency-patternlari.md) · [Mundarija](README.md) · [6. Web va taqdimot qatlami patternlari &rarr;](06-web-va-taqdimot-qatlami-patternlari.md)
