<!-- doc: patterns | chapter: 6 | part:  -->

[Java Spring arxitektori bilishi kerak bo'lgan barcha dizayn patternlar](../../README.md) / [Dizayn patternlar](README.md)

# 6. Web va taqdimot qatlami patternlari (Web & Presentation Patterns)

<details>
<summary>Bu bo'limdagi 35 bo'lim</summary>

- [6.1 Model-Ko'rinish-Boshqaruvchi (Model-View-Controller, MVC)](#61-model-korinish-boshqaruvchi-model-view-controller-mvc)
- [6.2 Old boshqaruvchi (Front Controller - DispatcherServlet)](#62-old-boshqaruvchi-front-controller---dispatcherservlet)
- [6.3 Sahifa boshqaruvchisi (Page Controller)](#63-sahifa-boshqaruvchisi-page-controller)
- [6.4 Ilova boshqaruvchisi (Application Controller - HandlerMapping + HandlerAdapter)](#64-ilova-boshqaruvchisi-application-controller---handlermapping--handleradapter)
- [6.5 Tutib qoluvchi filtr (Intercepting Filter - Filter, HandlerInterceptor)](#65-tutib-qoluvchi-filtr-intercepting-filter---filter-handlerinterceptor)
- [6.6 Kontekst ob'ekti (Context Object)](#66-kontekst-obekti-context-object)
- [6.7 Ko'rinish yordamchisi (View Helper)](#67-korinish-yordamchisi-view-helper)
- [6.8 Kompozit ko'rinish (Composite View)](#68-kompozit-korinish-composite-view)
- [6.9 Dispetcher ko'rinish (Dispatcher View)](#69-dispetcher-korinish-dispatcher-view)
- [6.10 Xizmatdan ishchiga (Service to Worker)](#610-xizmatdan-ishchiga-service-to-worker)
- [6.11 Shablon ko'rinish (Template View - Thymeleaf)](#611-shablon-korinish-template-view---thymeleaf)
- [6.12 Transformatsiya ko'rinishi (Transform View)](#612-transformatsiya-korinishi-transform-view)
- [6.13 Ikki bosqichli ko'rinish (Two Step View - layouts)](#613-ikki-bosqichli-korinish-two-step-view---layouts)
- [6.14 Model-Ko'rinish-Taqdimotchi (Model-View-Presenter, MVP)](#614-model-korinish-taqdimotchi-model-view-presenter-mvp)
- [6.15 Model-Ko'rinish-Ko'rinishModeli (Model-View-ViewModel, MVVM)](#615-model-korinish-korinishmodeli-model-view-viewmodel-mvvm)
- [6.16 Post/Redirect/Get (Post/Redirect/Get, PRG)](#616-postredirectget-postredirectget-prg)
- [6.17 Flash atributlar / Flash doirasi (Flash Attributes / Flash Scope)](#617-flash-atributlar--flash-doirasi-flash-attributes--flash-scope)
- [6.18 Istisnolarni qayta ishlovchi (Exception Handler - @ControllerAdvice, @ExceptionHandler)](#618-istisnolarni-qayta-ishlovchi-exception-handler---controlleradvice-exceptionhandler)
- [6.19 Kontent muzokarasi (Content Negotiation)](#619-kontent-muzokarasi-content-negotiation)
- [6.20 HTTP xabar konvertori (HttpMessageConverter)](#620-http-xabar-konvertori-httpmessageconverter)
- [6.21 Argument va qaytish qiymati ishlovchilari (HandlerMethodArgumentResolver / HandlerMethodReturnValueHandler)](#621-argument-va-qaytish-qiymati-ishlovchilari-handlermethodargumentresolver--handlermethodreturnvaluehandler)
- [6.22 Funksional endpointlar (Functional Endpoints - RouterFunction)](#622-funksional-endpointlar-functional-endpoints---routerfunction)
- [6.23 Server tomonidan yuboriladigan hodisalar (Server-Sent Events, SSE)](#623-server-tomonidan-yuboriladigan-hodisalar-server-sent-events-sse)
- [6.24 WebSocket va STOMP (WebSocket / STOMP)](#624-websocket-va-stomp-websocket--stomp)
- [6.25 Mijoz tomonidagi sessiya holati (Client Session State)](#625-mijoz-tomonidagi-sessiya-holati-client-session-state)
- [6.26 Server tomonidagi sessiya holati (Server Session State)](#626-server-tomonidagi-sessiya-holati-server-session-state)
- [6.27 Ma'lumotlar bazasidagi sessiya holati (Database Session State)](#627-malumotlar-bazasidagi-sessiya-holati-database-session-state)
- [6.28 Ma'lumotlarni bog'lash va forma ob'ekti (Data Binding / Form Backing Object)](#628-malumotlarni-boglash-va-forma-obekti-data-binding--form-backing-object)
- [6.29 Lokal va tema aniqlovchilar (LocaleResolver / ThemeResolver)](#629-lokal-va-tema-aniqlovchilar-localeresolver--themeresolver)
- [6.30 Statik resurslarni xizmat qilish (Static Resource Handling)](#630-statik-resurslarni-xizmat-qilish-static-resource-handling)
- [6.31 Multipart (fayl yuklash) ishlovi (Multipart Handling)](#631-multipart-fayl-yuklash-ishlovi-multipart-handling)
- [6.32 Ko'rinish aniqlovchi (View Resolver)](#632-korinish-aniqlovchi-view-resolver)
- [6.33 Asinxron so'rovlarni qayta ishlash (Async Request Processing - Callable, DeferredResult, StreamingResponseBody)](#633-asinxron-sorovlarni-qayta-ishlash-async-request-processing---callable-deferredresult-streamingresponsebody)
- [6.34 Server tomonida renderlash, SPA va gipermedia ilovalar (Server-Side Rendering vs SPA vs Hypermedia-Driven Application)](#634-server-tomonida-renderlash-spa-va-gipermedia-ilovalar-server-side-rendering-vs-spa-vs-hypermedia-driven-application)
- [6.35 Amalda qo'llash](#635-amalda-qollash)

</details>



Web va taqdimot qatlami - bu HTTP so'rovi tizimga kirib, biznes mantiqqa yetib boradigan va javob (HTML, JSON, oqim yoki WebSocket xabari) sifatida mijozga qaytadigan butun yo'l. Bu bo'lim Core J2EE va Fowler'ning klassik web patternlarini (Front Controller, Application Controller, Intercepting Filter, Template View, Two Step View, sessiya holati patternlari) hamda ularning Spring MVC va WebFlux'dagi aniq timsollarini (`DispatcherServlet`, `HandlerMapping`, `HandlerInterceptor`, `HttpMessageConverter`, `RouterFunction`, `SseEmitter`, STOMP) qamrab oladi. Arxitektor bu qatlamni puxta bilishi shart, chunki aynan shu yerda xavfsizlik, kuzatuv, kontent muzokarasi, xatolarni yagona formatda qaytarish va gorizontal masshtablash (sessiya holatini qayerda saqlash) kabi kesishuvchi qarorlar qabul qilinadi - va noto'g'ri qaror biznes mantiqqa emas, balki har bir so'rovga ta'sir qiladi. Spring'ning web stack'i aslida shu patternlarning tayyor, kengaytiriladigan amalga oshirilishidir: ularni nomi bilan bilish framework'ni "sehr" sifatida emas, ongli ravishda kengaytirish imkonini beradi.

## 6.1 Model-Ko'rinish-Boshqaruvchi (Model-View-Controller, MVC)

**Tavsif:** Muammo - foydalanuvchi interfeysi kodi ma'lumot, taqdimot va kirish ishlovini bir joyga aralashtirib yuborsa, uni sinash, qayta ishlatish va parallel ishlab chiqish qiyinlashadi. MVC taqdimotni uch rolga ajratadi: Model - ko'rsatiladigan holat va domen ma'lumotlari; View - modelni foydalanuvchiga chiqaradigan tasvir; Controller - kirishni (HTTP so'rovini) qabul qilib, modelni tayyorlab, qaysi View renderlanishini hal qiladigan komponent. Web'da bu "Model 2" (so'rov asosidagi) varianti: har bir so'rov controller orqali o'tadi, controller modelni to'ldiradi, view esa faqat o'qiydi. Natijada view mantiqdan, controller esa HTML'dan xoli bo'ladi.

**Spring'da qayerda uchraydi:** Spring MVC modulining o'zi (`spring-webmvc`): `@Controller` / `@RestController`, `Model`, `ModelMap`, `ModelAndView`, `View` va `ViewResolver` interfeyslari, `DispatcherServlet` (Front Controller sifatida), `spring-boot-starter-web`. REST holatida "View" rolini `HttpMessageConverter` orqali JSON serializatsiya bajaradi (`@ResponseBody`). WebFlux'da xuddi shu rollar `DispatcherHandler`, `@Controller`, `Rendering` va reaktiv `View` orqali ifodalanadi.

**Qo'llanish keyslari:**
- Thymeleaf bilan server tomonida renderlanadigan klassik korporativ web-ilova (admin panel, back-office).
- SPA yoki mobil mijoz uchun JSON qaytaradigan REST API - bu yerda View "tasvir" bo'lib, converter orqali hosil bo'ladi.
- Bir xil controller'dan bir nechta tasvir chiqarish (HTML sahifa va JSON) - kontent muzokarasi bilan birgalikda.
- Katta jamoalarda frontend va backend ishini ajratish: shablonlar dizaynerlar tomonidan, controller'lar backend tomonidan yoziladi.
- Server tomonida renderlanadigan SEO-talab marketing va kontent sahifalari.

**Ehtiyot bo'ling:** Controller'ga biznes mantiq va ma'lumotlarga kirish kodini joylash "Fat Controller" anti-patterniga olib keladi (qarang: [25-bo'lim](25-anti-patternlar.md), Fat Controller) - controller faqat HTTP'ni domen chaqiruviga tarjima qilishi kerak. JPA entity'larni model sifatida to'g'ridan-to'g'ri view'ga yoki JSON'ga chiqarish ichki modelni tashqi kontraktga aylantiradi (qarang: [25-bo'lim](25-anti-patternlar.md), Exposing JPA entities in API). MVC - taqdimot qatlami patterni; u Service va Domain qatlamlarini ([8-bo'lim](08-biznes-logika-va-service-qatlam-patternlari.md)) o'rnini bosmaydi.

## 6.2 Old boshqaruvchi (Front Controller - DispatcherServlet)

**Tavsif:** Muammo - har bir sahifa yoki endpoint o'z servlet'iga ega bo'lsa, autentifikatsiya, lokalizatsiya, xato ishlovi va kuzatuv kabi kesishuvchi vazifalar har joyda takrorlanadi va izchilligini yo'qotadi. Front Controller barcha kiruvchi so'rovlarni yagona kirish nuqtasidan o'tkazadi: u so'rovni tahlil qiladi, umumiy ishlovni bajaradi, so'ngra uni tegishli ishlovchiga (handler) yo'naltiradi va javobni renderlash jarayonini boshqaradi. Kesishuvchi mantiq bir joyda jamlanadi, handler'lar esa faqat o'z vazifasiga e'tibor qaratadi.

**Spring'da qayerda uchraydi:** `org.springframework.web.servlet.DispatcherServlet` (`FrameworkServlet` vorisi) - Spring MVC'ning yuragi; uning `doDispatch` siklida `getHandler` → `getHandlerAdapter` → `handle` → `processDispatchResult` → `render` bosqichlari bor. Spring Boot uni `DispatcherServletAutoConfiguration` orqali `/` ga ro'yxatdan o'tkazadi (`DispatcherServletRegistrationBean`, `spring.mvc.servlet.path`). WebFlux'dagi muqobili - `DispatcherHandler` (`WebHandler` amalga oshirilishi) va uni o'rab turgan `HttpHandler`/`WebHttpHandlerBuilder`. Bir ilovada bir nechta `DispatcherServlet` (masalan, `/api/*` va `/admin/*` uchun alohida kontekstlar bilan) ro'yxatdan o'tkazish mumkin.

**Qo'llanish keyslari:**
- Har qanday Spring MVC ilovasi - pattern avtomatik qo'llaniladi, lekin uni bilish `DispatcherServlet` xususiyatlarini (`throwExceptionIfNoHandlerFound`, `enableLoggingRequestDetails`) ongli sozlash imkonini beradi.
- Monolit ichida API va admin UI'ni alohida `DispatcherServlet` + alohida `WebApplicationContext` bilan izolyatsiya qilish.
- Legacy servlet ilovasini bosqichma-bosqich Spring MVC'ga ko'chirish: avval `DispatcherServlet` ni bitta prefiksga ulash, keyin yo'llarni ko'chirish.
- Yagona kirish nuqtasida kuzatuv (`ServerHttpObservationFilter`) va xatolarni yagona formatga keltirish.

**Ehtiyot bo'ling:** Front Controller'ning o'zini `extends DispatcherServlet` qilib o'zgartirish deyarli hech qachon kerak emas - kengaytirish nuqtalari `HandlerInterceptor`, `HandlerExceptionResolver`, `HandlerMethodArgumentResolver` va `WebMvcConfigurer` orqali beriladi. `DispatcherServlet` servlet konteyner `Filter` zanjiridan keyin ishlaydi, shuning uchun Security filtrlarida yuzaga kelgan istisnolar `@ControllerAdvice` ga yetib bormaydi.

## 6.3 Sahifa boshqaruvchisi (Page Controller)

**Tavsif:** Fowler tasniflagan Page Controller - har bir mantiqiy sahifa yoki amal uchun alohida ishlovchi ob'ekt (yoki metod) bo'lib, u shu sahifaga tegishli kirishni qabul qiladi, modelni tayyorlaydi va view'ni tanlaydi. Front Controller "qayerga yo'naltirish" ni hal qilsa, Page Controller "shu sahifa uchun nima qilish" ni hal qiladi; ikkalasi birgalikda ishlaydi. Pattern oddiy: har bir URL - bir controller metodi, mantiq lokal va tushunarli.

**Spring'da qayerda uchraydi:** `@Controller` klassining har bir `@GetMapping`/`@PostMapping` metodi - bu Page Controller; `HandlerMethod` abstraksiyasi aynan shu birlikni ifodalaydi. Interfeys asosidagi eski uslub: `org.springframework.web.servlet.mvc.Controller` (`handleRequest`), `AbstractController`, `ParameterizableViewController`, `HttpRequestHandler` (`HttpRequestHandlerAdapter` orqali). JSF (JoinFaces orqali Spring Boot bilan) dagi backing bean ham Page Controller'ning timsoli. WebMvc.fn da `HandlerFunction<ServerResponse>` - bitta sahifa/endpoint uchun funksional Page Controller.

**Qo'llanish keyslari:**
- Shakl ko'rsatish (GET) va shaklni qabul qilish (POST) juftligini bitta `@Controller` klassida jamlash.
- Mahsulot sahifasi, buyurtma tafsiloti kabi har bir "ekran" uchun alohida controller metodi.
- Sodda, kam mantiqli statik sahifalar uchun `ViewControllerRegistry` orqali kodsiz Page Controller.
- Health yoki "about" kabi yakka endpointlarni `HttpRequestHandler` sifatida yengil amalga oshirish.

**Ehtiyot bo'ling:** Bir controller klassiga o'nlab sahifani joylash uni God Object'ga aylantiradi - controller'larni domen bo'yicha (buyurtmalar, to'lovlar) guruhlang. Har bir metodda takrorlanadigan "umumiy model atributlari" ni `@ModelAttribute` metodlar yoki `@ControllerAdvice` ga ko'chiring, aks holda Page Controller'lar nusxa-ko'chirma kodga to'ladi.

## 6.4 Ilova boshqaruvchisi (Application Controller - HandlerMapping + HandlerAdapter)

**Tavsif:** Front Controller kattalashgach, "qaysi so'rov qaysi ishlovchiga boradi" va "ishlovchini qanday chaqirish kerak" mantig'i uni og'irlashtiradi. Application Controller bu ikki javobgarlikni ajratib oladi: amal (action) ni aniqlash va view'ni tanlash markazlashgan, konfiguratsiya qilinadigan komponentga topshiriladi. Front Controller "darvoza", Application Controller esa "yo'l xaritasi": u so'rov atributlari (yo'l, metod, header, media type) asosida ishlovchini tanlaydi va uni yagona kontrakt orqali bajaradi.

**Spring'da qayerda uchraydi:** `HandlerMapping` (amalni aniqlash): `RequestMappingHandlerMapping` (`@RequestMapping` uchun), `SimpleUrlHandlerMapping`, `BeanNameUrlHandlerMapping`, `RouterFunctionMapping`, Boot'ning `WelcomePageHandlerMapping`; natija - `HandlerExecutionChain` (handler + interceptor'lar). `HandlerAdapter` (ishlovchini chaqirish): `RequestMappingHandlerAdapter`, `HandlerFunctionAdapter`, `HttpRequestHandlerAdapter`, `SimpleControllerHandlerAdapter`. Moslashtirish: `RequestMappingInfo`, `RequestCondition` (shaxsiy shartlar uchun `RequestMappingHandlerMapping#getCustomMethodCondition`), `PathPatternParser` (6.0'dan sukut bo'yicha, `AntPathMatcher` o'rniga), `WebMvcConfigurer#configurePathMatch`, `@RequestMapping(params=, headers=, consumes=, produces=)`. Spring Framework 7 API versiyalash ham shu mexanizmga `ApiVersionStrategy` orqali ulanadi - qarang: [7-bo'lim](07-api-dizayn-patternlari.md) (API Versioning). WebFlux: `RequestMappingHandlerMapping`/`HandlerAdapter` ning reaktiv variantlari va `HandlerResultHandler`.

**Qo'llanish keyslari:**
- Shaxsiy marshrutlash sharti: `X-Tenant` header'i yoki feature flag asosida bir xil URL'ni turli handler'larga yo'naltirish (`RequestCondition`).
- Annotatsiyali controller'lar va funksional `RouterFunction` larni bir ilovada birga ishlatish - ikkala `HandlerMapping` tartib bilan so'raladi.
- Legacy `HttpRequestHandler` lar (masalan, eski SOAP endpointlari) va zamonaviy `@RestController` larni yagona `DispatcherServlet` ostida birlashtirish.
- URL namunalarini `PathPattern` bilan tez va xavfsiz moslashtirish (`{*path}`, `{id:\d+}`).
- Yangi protokol yoki handler turi uchun shaxsiy `HandlerAdapter` yozish (kamdan-kam, lekin plugin arxitekturalarida uchraydi).

**Ehtiyot bo'ling:** `HandlerMapping` tartibi (`Ordered`) muhim - xato tartib "noto'g'ri handler topildi" yoki 404 ko'rinishida namoyon bo'ladi. `AntPathMatcher` ga qaytish (`spring.mvc.pathmatch.matching-strategy=ant_path_matcher`) faqat legacy suffix-pattern'lar uchun va vaqtinchalik bo'lishi kerak. `@RequestMapping` larda bir xil yo'l uchun ikkilamchi (ambiguous) mapping ishga tushirishda istisno beradi - buni testlar bilan ushlang.

## 6.5 Tutib qoluvchi filtr (Intercepting Filter - Filter, HandlerInterceptor)

**Tavsif:** Muammo - autentifikatsiya, kodlashni o'rnatish, so'rovni qayd etish, siqish, korrelyatsiya ID'si kabi so'rovdan oldin va keyin bajariladigan vazifalarni har bir ishlovchi takrorlamasligi kerak. Intercepting Filter bu vazifalarni almashtiriladigan, zanjirga tiziladigan komponentlarga ajratadi; har biri so'rovni o'tkazadi, o'zgartiradi yoki to'xtatadi. Bu Chain of Responsibility'ning web-qatlamdagi ixtisoslashgan ko'rinishi (qarang: [3-bo'lim](03-xulq-atvor-patternlari.md), Chain of Responsibility). Filtrlar servlet darajasida (handler'dan bexabar), interceptor'lar esa Front Controller ichida (handler va modeldan xabardor) ishlaydi.

**Spring'da qayerda uchraydi:** Servlet darajasi: `jakarta.servlet.Filter`, `OncePerRequestFilter`, `GenericFilterBean`, `FilterRegistrationBean` (tartib, URL namunalari), `@Component` filtr avtomatik `/*` ga ro'yxatdan o'tadi, `@Order`; tayyor filtrlar - `CharacterEncodingFilter`, `FormContentFilter`, `HiddenHttpMethodFilter`, `ForwardedHeaderFilter`, `ShallowEtagHeaderFilter`, `CommonsRequestLoggingFilter`, `RequestContextFilter`, `ServerHttpObservationFilter`, `DelegatingFilterProxy` orqali `springSecurityFilterChain` (qarang: [18-bo'lim](18-xavfsizlik-patternlari.md), SecurityFilterChain). MVC darajasi: `HandlerInterceptor` (`preHandle`, `postHandle`, `afterCompletion`), `AsyncHandlerInterceptor#afterConcurrentHandlingStarted`, `MappedInterceptor`, `WebMvcConfigurer#addInterceptors` (`InterceptorRegistry#addPathPatterns/excludePathPatterns`), `WebRequestInterceptor`. WebFlux: `WebFilter` va `WebFilterChain`. Javob tanasini o'zgartirish uchun - `ResponseBodyAdvice`.

**Qo'llanish keyslari:**
- Korrelyatsiya/trace ID'ni header'dan olib MDC'ga joylash va javobga qaytarish (qarang: [21-bo'lim](21-observability-patternlari.md)).
- Tenant'ni subdomen yoki header'dan aniqlab, so'rov davomida kontekstga saqlash.
- So'rov va javob tanasini audit uchun qayd etish (`ContentCachingRequestWrapper`/`ContentCachingResponseWrapper` bilan).
- Admin yo'llari uchun qo'shimcha IP cheklovi yoki maintenance rejimida 503 qaytarish.
- Handler metodining annotatsiyasi (`HandlerMethod#getMethodAnnotation`) asosida rate limit yoki feature flag tekshiruvi.

**Ehtiyot bo'ling:** `InputStream` ni filtrda bir marta o'qisangiz, controller unga ega bo'lmaydi - o'rash (wrapper) ishlating. `postHandle` `@ResponseBody` javobi uchun juda kech (javob allaqachon yozilgan), unda `ResponseBodyAdvice` yoki filtr kerak. Filtrdan tashlangan istisnolar `@ControllerAdvice` ga yetmaydi; filtr tartibini `Ordered.HIGHEST_PRECEDENCE` bilan ko'r-ko'rona o'rnatish Security zanjiri bilan ziddiyat tug'diradi.

```java
@Component
public class TenantInterceptor implements HandlerInterceptor {
    @Override
    public boolean preHandle(HttpServletRequest req, HttpServletResponse res, Object handler) {
        String tenant = req.getHeader("X-Tenant-Id");
        if (tenant == null) { res.setStatus(HttpStatus.BAD_REQUEST.value()); return false; }
        TenantContext.set(tenant);
        return true;
    }
    @Override
    public void afterCompletion(HttpServletRequest req, HttpServletResponse res, Object h, Exception ex) {
        TenantContext.clear();
    }
}
```

## 6.6 Kontekst ob'ekti (Context Object)

**Tavsif:** Muammo - `HttpServletRequest`, `HttpSession`, header'lar va cookie'lar kabi protokolga bog'liq ob'ektlar servis va domen qatlamiga "sizib" kirsa, kod servlet API'ga bog'lanib qoladi, testlash va qayta ishlatish qiyinlashadi. Context Object protokolga xos holatni protokoldan mustaqil ob'ektga o'rab beradi: foydalanuvchi, tenant, lokal, trace ID, so'rov atributlari - hammasi yagona kontekst orqali olinadi. Shu bilan birga, kontekst so'rov davomida (yoki thread/scope davomida) hamma joydan erishiladigan bo'ladi.

**Spring'da qayerda uchraydi:** `WebRequest` va `NativeWebRequest` (servlet API'dan abstraksiya, `@ModelAttribute`/`@InitBinder` metodlarida parametr sifatida), `RequestAttributes`/`ServletRequestAttributes` va `RequestContextHolder.currentRequestAttributes()`, `RequestContextUtils`, `LocaleContextHolder`, `ServerWebExchange` (WebFlux'da so'rov+javob+sessiya+atributlar konteksti - eslatma: bu yerda `exchange.getAttributes()` orqali handler'lar o'rtasida ma'lumot uzatiladi), funksional uslubda `ServerRequest#attributes()`, Spring Security'dagi `SecurityContextHolder` (qarang: [18-bo'lim](18-xavfsizlik-patternlari.md)) va `RequestContextFilter`. Thread'ga bog'langan tashuvchilar `ThreadLocal` va `ScopedValue` asosida qurilgan - qarang: [4-bo'lim](04-concurrency-patternlari.md) (Thread-Specific Storage, Scoped Values). Request scope bean'lar (`@RequestScope`) - qarang: [5-bo'lim](05-spring-core-ichidagi-patternlar-xaritasi.md) (Bean scopes).

**Qo'llanish keyslari:**
- `TenantContext` yoki `RequestContext` orqali ko'p ijarachili (multi-tenant) ilovada joriy tenant'ni servis qatlamiga uzatmasdan olish.
- Joriy foydalanuvchi va uning rollarini domen xizmatlariga `HttpServletRequest` bermasdan etkazish.
- So'rov lokal va vaqt zonasini formatlash va i18n uchun `LocaleContextHolder` dan olish.
- Audit uchun so'rov ID, IP va user-agent'ni yagona `RequestInfo` record'ida yig'ish.
- Validatsiya yoki data binding metodlarida servlet API o'rniga `WebRequest` ishlatib, birlik testlarni soddalashtirish.

**Ehtiyot bo'ling:** `RequestContextHolder` `ThreadLocal`ga asoslangan - `@Async`, `CompletableFuture` yoki reaktiv zanjirda kontekst yo'qoladi; tarqatish uchun `TaskDecorator` yoki Micrometer `ContextPropagation` kerak. Kontekstni "global o'zgaruvchi" sifatida suiiste'mol qilish yashirin bog'liqlik yaratadi: domen qatlamiga kerakli qiymatlarni aniq parametr sifatida uzatish afzal, kontekst - faqat web-qatlam chegarasida.

## 6.7 Ko'rinish yordamchisi (View Helper)

**Tavsif:** Muammo - shablon ichida formatlash, hisoblash, lokalizatsiya va shartli ko'rsatish mantig'i to'planib, view'ni sinab bo'lmaydigan va dizaynerlar uchun tushunarsiz qiladi. View Helper bu mantiqni alohida yordamchi komponentlarga (teglar, utility ob'ektlar, formatlovchilar, model tayyorlovchilar) ko'chiradi; shablon faqat ularni chaqiradi. Natijada view "yupqa", yordamchilar esa birlik testlar bilan qoplangan bo'ladi.

**Spring'da qayerda uchraydi:** Thymeleaf'da ifoda utility ob'ektlari (`#dates`, `#temporals`, `#numbers`, `#strings`, `#fields`, `#messages`), `#{...}` xabar ifodalari (`MessageSource` orqali - qarang: [5-bo'lim](05-spring-core-ichidagi-patternlar-xaritasi.md)), SpEL orqali bean'ga murojaat (`${@priceFormatter.format(order.total)}`), shaxsiy dialect va `IProcessor` lar; JSP'da `spring:message`, `spring:url`, `form:input` teg kutubxonalari; FreeMarker'da `spring.ftl` makrolari. Model tomonida - `@ControllerAdvice` ichidagi `@ModelAttribute` metodlar (barcha view'lar uchun umumiy atributlar), `Formatter`/`Printer` (qarang: [5-bo'lim](05-spring-core-ichidagi-patternlar-xaritasi.md), ConversionService) va `RequestContext` (`spring.ftl`/JSP'da `requestContext`).

**Qo'llanish keyslari:**
- Pul, sana va foizlarni lokalga mos formatlash - shablonda emas, `Formatter` yoki Thymeleaf utility'da.
- Sahifa sarlavhasi, joriy foydalanuvchi ismi, menyu bandlari kabi umumiy atributlarni `@ControllerAdvice` + `@ModelAttribute` orqali barcha view'larga berish.
- Murakkab ruxsat tekshiruvini (`sec:authorize` kabi) shablon dialect'i ko'rinishida ta'minlash.
- Markdown'ni HTML'ga aylantirish yoki matnni qisqartirish kabi takrorlanuvchi tasvir mantig'ini yordamchi bean'da jamlash.
- Statik resurs URL'lariga versiya qo'shishni `ResourceUrlProvider` yordamchisi orqali bajarish.

**Ehtiyot bo'ling:** Yordamchidan servis yoki repository chaqirish (shablon ichidan `${@orderService.findAll()}`) taqdimot qatlamida yashirin ma'lumot kirishini tug'diradi va N+1 muammolarini view'ga olib keladi - yordamchi faqat tayyor modelni bezaydi. `@ControllerAdvice` dagi `@ModelAttribute` metodlar har bir so'rovda, shu jumladan JSON endpointlarida ham ishlaydi; ularni `assignableTypes`/`basePackages` bilan cheklang.

## 6.8 Kompozit ko'rinish (Composite View)

**Tavsif:** Muammo - header, navigatsiya, footer, yon panel kabi bo'laklar har bir sahifada takrorlanadi; o'zgarish barcha sahifalarga tegadi. Composite View sahifani kichik, qayta ishlatiladigan sub-view'lardan (fragmentlardan) yig'adi; har bir fragment mustaqil, sahifa esa ularning kompozitsiyasi. Bu GoF Composite'ning (qarang: [2-bo'lim](02-strukturaviy-patternlar.md)) taqdimot qatlamidagi ko'rinishi: barg (fragment) va konteyner (sahifa) bir xil "render" kontraktiga ega.

**Spring'da qayerda uchraydi:** Thymeleaf fragmentlari - `th:fragment`, `th:insert`, `th:replace`, parametrli fragmentlar (`~{header :: nav(active='orders')}`) va fragment ifodalari; Thymeleaf Layout Dialect (`layout:fragment`); FreeMarker `#include`/`#import` makrolari; JSP `<jsp:include>`/`<%@ include %>`. Apache Tiles qo'llab-quvvatlashi Spring Framework 6.0 da olib tashlangan - yangi loyihalarda Thymeleaf fragmentlari yoki Layout Dialect ishlatiladi. Bitta fragmentni mustaqil endpoint sifatida qaytarish (`return "orders :: table"`) htmx uslubidagi qismiy yangilanishlarga asos bo'ladi. Mikroservislar darajasida sahifani server tomonida fragmentlardan yig'ish - qarang: [14-bo'lim](14-microservices-patternlari.md) (Server-Side Page Fragment Composition).

**Qo'llanish keyslari:**
- Umumiy header/footer/navigatsiyani bitta fragmentda saqlab, barcha sahifalarda qayta ishlatish.
- Dashboard'ni mustaqil vidjet-fragmentlarga bo'lish, har biri o'z modelini oladi.
- Forma maydonlari (input + label + xato xabari) uchun parametrli fragment - izchil dizayn va validatsiya ko'rinishi.
- htmx yoki fetch orqali faqat jadval fragmentini qayta yuklash (qismiy renderlash).
- Email shablonlarini (sarlavha, tana, imzo) fragmentlardan yig'ish.

**Ehtiyot bo'ling:** Fragmentlar chuqur ichma-ich bo'lsa, ma'lumot oqimini kuzatish qiyinlashadi va "qaysi controller qaysi fragment uchun model beradi" chalkashadi - har bir fragmentning kirish kontraktini (parametrlarni) aniq hujjatlang. Fragment ichida ma'lumot yuklash (View Helper'dan servis chaqirish) kompozitsiyani sekin va kuzatib bo'lmaydigan qiladi.

## 6.9 Dispetcher ko'rinish (Dispatcher View)

**Tavsif:** Core J2EE'dagi Dispatcher View - Front Controller so'rovni minimal yoki hech qanday ishlovsiz bevosita view'ga yo'naltiradigan variant; ma'lumotni olish va tayyorlash view renderlash paytida (yoki View Helper'lar orqali) bajariladi. Bu Service to Worker'ning "teskari" tomoni: u yerda ishlov controller'da, bu yerda - view yoki yordamchilarda. Pattern statik yoki deyarli statik sahifalar, hamda modelni allaqachon tayyor holda olgan hollar uchun mos.

**Spring'da qayerda uchraydi:** `WebMvcConfigurer#addViewControllers` → `ViewControllerRegistry#addViewController("/about").setViewName("about")`, `ParameterizableViewController`, `UrlFilenameViewController` (URL'dan view nomini chiqaradi), `RequestToViewNameTranslator` (`DefaultRequestToViewNameTranslator` - handler `void` yoki `null` qaytarsa view nomi URL'dan olinadi), `ViewControllerRegistry#addRedirectViewController` va `addStatusController`. WebFlux'da `ViewResolverRegistry` va `Rendering.view("about")`. Spring Boot'ning `index.html` uchun `WelcomePageHandlerMapping` va `BasicErrorController` ning `error` view'i ham amalda Dispatcher View'dir.

**Qo'llanish keyslari:**
- "Biz haqimizda", "Maxfiylik siyosati" kabi statik sahifalarni controller yozmasdan ulash.
- Eski URL'larni yangisiga qayta yo'naltirish (`addRedirectViewController`) - SEO migratsiyalarida.
- SPA uchun barcha noma'lum yo'llarni `index.html` ga yo'naltirish (client-side routing).
- Faqat `@ControllerAdvice` dan kelgan umumiy model atributlari bilan renderlanadigan sahifalar.
- Maintenance yoki "tez orada" sahifasini `addStatusController` bilan 503 statusda ko'rsatish.

**Ehtiyot bo'ling:** Dispatcher View'ni dinamik ma'lumotli sahifalarga tatbiq etish view ichida ma'lumot yuklashni rag'batlantiradi - bu testlab bo'lmaydigan shablonlarga olib keladi. `RequestToViewNameTranslator` ga tayanib view nomini yashirin qoldirish o'qilishini pasaytiradi; aniq `return "about"` afzal.

## 6.10 Xizmatdan ishchiga (Service to Worker)

**Tavsif:** Core J2EE'dagi Service to Worker - Front Controller (yoki Application Controller) so'rovni qabul qiladi, ishlovchi ("worker", ya'ni controller/action) biznes xizmatini chaqirib modelni to'liq tayyorlaydi, keyin view faqat tayyor modelni renderlaydi. Barcha ishlov renderlashdan oldin bajariladi, view "aqlsiz" qoladi. Bu zamonaviy Spring MVC ilovasining standart oqimi va Dispatcher View'ga qarshi qo'yiladi.

**Spring'da qayerda uchraydi:** Standart `@Controller` metodi: `Model` ga atributlarni joylash, servis qatlamini chaqirish, view nomini (yoki `ModelAndView`) qaytarish; `DispatcherServlet` → `HandlerAdapter` → handler → `ViewResolver` → `View#render` zanjiri. REST uchun xuddi shu oqim `@ResponseBody` + `HttpMessageConverter` bilan tugaydi. Servis qatlami kontrakti - qarang: [8-bo'lim](08-biznes-logika-va-service-qatlam-patternlari.md) (Service Layer, DTO, Mapper). `@ModelAttribute` metodlar modelni so'rovdan oldin to'ldiradigan "worker" yordamchilari sifatida ishlaydi.

**Qo'llanish keyslari:**
- Buyurtma tafsiloti sahifasi: controller `OrderQueryService` dan DTO oladi, modelga joylaydi, Thymeleaf renderlaydi.
- Qidiruv natijalari sahifasi: parametrlarni bog'lash, validatsiya, servis chaqiruvi, sahifalangan model.
- Forma yuborish: bog'lash → validatsiya → servis → PRG redirect (qarang 6.16).
- JSON API'da controller DTO qaytaradi, "view" vazifasini converter bajaradi.
- Server tomonida renderlanadigan hisobot sahifalari, bunda barcha ma'lumot bitta transaksiyada tayyorlanadi.

**Ehtiyot bo'ling:** Worker'ga biznes mantiqni joylash controller'ni semirtiradi - worker faqat orkestratsiya va HTTP tarjimasi. Lazy JPA assotsiatsiyalarini view renderlash paytida yuklashga tayanish Open Session in View ga bog'liqlik yaratadi (qarang: [9-bo'lim](09-malumotlarga-kirish-va-orm-patternlari.md)) - modelni controller'da to'liq DTO ko'rinishida tayyorlang.

## 6.11 Shablon ko'rinish (Template View - Thymeleaf)

**Tavsif:** Fowler'ning Template View'i - HTML sahifasida belgilar (markers) joylashtirilib, renderlash paytida ular model qiymatlari bilan to'ldiriladi. Shablon statik tuzilmani (dizayn) saqlaydi, dinamik qismlar esa ifoda tili orqali kiritiladi. Bu web'dagi eng keng tarqalgan view strategiyasi: dizaynerlar HTML bilan ishlaydi, dasturchilar modelni beradi. "Natural templating" (brauzerda statik fayl sifatida ham ochiladigan shablon) Thymeleaf'ning asosiy ustunligi.

**Spring'da qayerda uchraydi:** `spring-boot-starter-thymeleaf` (`thymeleaf-spring6` moduli Spring 6/7 bilan ishlaydi): `SpringTemplateEngine`, `SpringResourceTemplateResolver`, `ThymeleafViewResolver`, `spring.thymeleaf.cache`, `spring.thymeleaf.prefix/suffix`; standart dialect (`th:text`, `th:each`, `th:if`, `th:object`, `th:field`, `th:href="@{...}"`), Spring Security dialect (`thymeleaf-extras-springsecurity6`). Muqobillar: FreeMarker (`spring-boot-starter-freemarker`, `FreeMarkerViewResolver`), Mustache (`spring-boot-starter-mustache`), Groovy Markup, JSP (`InternalResourceViewResolver`, lekin executable jar'da cheklovlar bilan), JTE (uchinchi tomon starter'i, kompilyatsiya qilinadigan shablonlar). Email uchun `TemplateEngine#process` ni to'g'ridan-to'g'ri chaqirish.

**Qo'llanish keyslari:**
- Admin panel va back-office ilovalari, bunda SEO va tez ishga tushirish SPA murakkabligidan muhimroq.
- Marketing/kontent sahifalari - server renderlash va keshlash bilan yuqori unumdorlik.
- Transaksion email'lar (tasdiq, hisob-faktura) HTML'ini shablon orqali yaratish.
- PDF generatsiyasi uchun HTML tayyorlab, keyin OpenHTMLtoPDF kabi vosita bilan PDF'ga aylantirish.
- htmx bilan birgalikda interaktiv, lekin serverda renderlanadigan "gipermedia" ilovalar.

**Ehtiyot bo'ling:** Shablonda mantiq (murakkab shartlar, hisoblashlar, servis chaqiruvlari) to'planishi - Template View'ning asosiy kasalligi; View Helper ga ko'chiring. Ishlab chiqish rejimida `spring.thymeleaf.cache=false`, ishlab chiqarishda `true` bo'lishi shart. `th:utext` bilan foydalanuvchi kiritgan matnni chiqarish XSS'ga yo'l ochadi - sukutdagi `th:text` escape'ini saqlang (qarang: [18-bo'lim](18-xavfsizlik-patternlari.md), Output Encoding).

## 6.12 Transformatsiya ko'rinishi (Transform View)

**Tavsif:** Fowler'ning Transform View'i - modelni element-element aylanib chiqib, uni chiqish formatiga transformatsiya qiladigan view; shablonda belgilarni to'ldirish o'rniga, dastur modelning har bir qismi uchun chiqish bo'lagini hosil qiladi. Klassik misol XSLT: domen XML'i stylesheet orqali HTML'ga aylanadi. Zamonaviy ko'rinishi - modelni JSON, XML, CSV, PDF yoki Excel'ga seriyalashtiruvchi view'lar: tuzilma modeldan kelib chiqadi, shablon esa yo'q.

**Spring'da qayerda uchraydi:** `org.springframework.web.servlet.view.xslt.XsltView` va `XsltViewResolver`; JSON/XML view'lar - `MappingJackson2JsonView`, `MappingJackson2XmlView` (Spring Framework 7 da Jackson 3 asosidagi `JacksonJsonView`/`JacksonXmlView` qo'shilgan), `MarshallingView` (JAXB/`Marshaller`); hujjat view'lari - `AbstractPdfView` (OpenPDF), `AbstractXlsxView`/`AbstractXlsxStreamingView` (Apache POI); `ContentNegotiatingViewResolver` bir xil modelni formatga qarab turli Transform View'ga yo'naltiradi. Keng ma'noda `@ResponseBody` + `HttpMessageConverter` (6.20) ham Transform View'dir - model to'g'ridan-to'g'ri baytlarga aylanadi.

**Qo'llanish keyslari:**
- Hisobotni bitta modeldan HTML, PDF va XLSX ko'rinishlarida eksport qilish.
- Legacy XML ma'lumotlarini XSLT orqali HTML yoki boshqa XML sxemasiga aylantirish.
- Katta jadvallarni `AbstractXlsxStreamingView` bilan xotirani to'ldirmasdan Excel'ga chiqarish.
- RSS/Atom lentalari yoki sitemap.xml ni modeldan generatsiya qilish.
- Bir xil controller'dan `Accept` header'iga qarab JSON yoki XML qaytarish.

**Ehtiyot bo'ling:** XSLT bugun kam ishlatiladi va mutaxassis topish qiyin - yangi loyihada uni faqat XML-markaziy integratsiyalar talab qilsa tanlang. Transform View'da tasvir mantiqi Java kodida bo'ladi, shuning uchun dizayn o'zgarishlari dasturchi ishtirokini talab qiladi; HTML uchun Template View odatda afzal. PDF/Excel generatsiyasi CPU va xotira talab qiladi - katta hajmlarda asinxron (6.33) yoki batch ([20-bo'lim](20-batch-va-scheduling-patternlari.md)) yondashuvga o'ting.

## 6.13 Ikki bosqichli ko'rinish (Two Step View - layouts)

**Tavsif:** Fowler'ning Two Step View'i renderlashni ikki bosqichga ajratadi: birinchi bosqichda domen modeli mantiqiy sahifaga (sarlavha, kontent bloki, yon panel - hali HTML'siz tuzilma) aylanadi, ikkinchi bosqichda bu mantiqiy sahifa yagona layout orqali konkret HTML'ga renderlanadi. Natijada saytning umumiy ko'rinishini (layout, tema) bir joyda o'zgartirish mumkin va barcha sahifalar izchil bo'ladi. Amaliyotda bu "layout + kontent fragmenti" (decorator) modelidir.

**Spring'da qayerda uchraydi:** Thymeleaf'ning o'z fragment ifodalari bilan layout: `th:replace="~{layouts/main :: page(~{::title}, ~{::content})}"` - layout parametr sifatida kontent fragmentini oladi; Thymeleaf Layout Dialect (`layout:decorate="~{layouts/main}"`, `layout:fragment="content"`) - eng ko'p ishlatiladigan dekorator yondashuvi; FreeMarker makro-layoutlar; SiteMesh (servlet filtr sifatida, Spring MVC'dan mustaqil). Apache Tiles (klassik Two Step View amalga oshirilishi) Spring Framework 6.0 da olib tashlangan. Tema (theme) almashish - ilgari `ThemeResolver`, hozir CSS o'zgaruvchilari va layout tanlovi orqali (qarang 6.29).

**Qo'llanish keyslari:**
- Butun sayt uchun yagona `main` layout (head, header, footer, skriptlar) va har bir sahifa faqat kontent fragmentini beradi.
- Ko'p ijarachili SaaS'da tenant'ga qarab turli layout/brending tanlash (`layouts/{tenant}/main`).
- Autentifikatsiya qilingan va mehmon foydalanuvchilar uchun ikki alohida layout.
- Mobil va desktop uchun turli layout, lekin bir xil kontent fragmentlari.
- Email shablonlari uchun umumiy "chrome" (logo, footer) va o'zgaruvchan tana.

**Ehtiyot bo'ling:** Chuqur layout ierarxiyasi (layout → sub-layout → sahifa → fragment) kuzatishni qiyinlashtiradi - ikki-uch darajadan oshmang. Layout Dialect uchinchi tomon kutubxonasi bo'lib, Thymeleaf versiyalari bilan moslik oynasini tekshirish kerak; sof Thymeleaf fragment ifodalari bilan ham xuddi shu natijaga erishish mumkin. htmx uslubidagi qismiy javoblarda layout'ni chetlab o'tishni (`HX-Request` header'i bo'lsa faqat fragmentni qaytarish) oldindan loyihalashtiring.

## 6.14 Model-Ko'rinish-Taqdimotchi (Model-View-Presenter, MVP)

**Tavsif:** MVP - MVC'ning view'ni passiv qiladigan varianti: Presenter view interfeysi orqali view'ni to'liq boshqaradi (nima ko'rsatish, qaysi tugma faol), view esa foydalanuvchi hodisalarini presenter'ga uzatadi va o'zi hech qanday qaror qabul qilmaydi ("Passive View"). View interfeys orqali abstraksiyalangani uchun presenter UI framework'siz birlik test qilinadi. Bu pattern asosan holatli (stateful), komponentga asoslangan UI'lar uchun (desktop, Vaadin, Android) tabiiy, so'rov-javob web MVC'da kamroq.

**Spring'da qayerda uchraydi:** Vaadin Flow + Spring Boot (`vaadin-spring-boot-starter`): `@Route` view'lar va Spring bean sifatida presenter'lar, `@UIScope`/`@RouteScope` bean scope'lari; JavaFX + Spring Boot (FXML controller'lari view, Spring bean'lar presenter rolida); Spring MVC'da MVP to'g'ridan-to'g'ri yo'q, lekin "Humble Object" g'oyasi (qarang: [23-bo'lim](23-testing-patternlari.md)) controller'ni iloji boricha yupqa qilib, qaror mantig'ini test qilinadigan "presenter/use case" klassiga ko'chirishda qo'llanadi. Spring'ning o'zi MVP uchun maxsus API bermaydi - bu arxitektura tanlovi, framework imkoniyati emas.

**Qo'llanish keyslari:**
- Vaadin asosidagi ichki korporativ ilovada ekran mantig'ini presenter'ga ajratib, UI komponentlarisiz test qilish.
- JavaFX desktop vositasi Spring Boot konteyneri bilan - presenter servislarni inject qiladi, view FXML'da.
- Murakkab, holatli forma oqimlari (wizard) bo'lgan ekranlar, bunda tugma holatlari va validatsiya ko'p shartli.
- Android/KMP mijozlar uchun Spring backend bilan ishlaydigan jamoada umumiy terminologiya.

**Ehtiyot bo'ling:** So'rov-javob Spring MVC'ga "sun'iy" MVP qatlamini qo'shish (view interfeyslari, presenter'lar) ortiqcha abstraksiya tug'diradi - u yerda controller + servis yetarli. Vaadin'da presenter'ni session scope'da saqlash xotira iste'molini oshiradi va gorizontal masshtablashni (sticky session) talab qiladi.

## 6.15 Model-Ko'rinish-Ko'rinishModeli (Model-View-ViewModel, MVVM)

**Tavsif:** MVVM - view va model orasiga ViewModel joylashtiradi: ViewModel view uchun tayyor, bog'lanadigan (bindable) holat va buyruqlarni beradi, view esa deklarativ data binding orqali avtomatik yangilanadi (ikki tomonlama bog'lanish). Presenter'dan farqi - ViewModel view'ni bilmaydi, u shunchaki kuzatiladigan holat; bog'lanishni framework bajaradi. Bu reaktiv frontend framework'lari (Vue, Angular, Knockout), WPF, JavaFX properties va Android ViewModel asosidagi pattern.

**Spring'da qayerda uchraydi:** Spring backend'da MVVM'ning o'zi emas, uning "serverdagi yarmi" uchraydi: ViewModel'ga mos keladigan ekran-markaziy DTO'lar (`OrderPageViewModel` record'i - faqat shu ekran uchun kerak maydonlar), ularni tayyorlovchi BFF endpointlari (qarang: [7-bo'lim](07-api-dizayn-patternlari.md), Backend for Frontend) va Transfer Object Assembler (qarang: [8-bo'lim](08-biznes-logika-va-service-qatlam-patternlari.md)). Server tomonidagi "yaqin qarindoshlar": Thymeleaf `th:object`/`th:field` bilan forma ob'ektiga bog'lanish (6.28), Vaadin `Binder<T>` (ikki tomonlama binding), Hilla (Vaadin) - Spring `@BrowserCallable` servislarini TypeScript tiplari bilan React/Lit'ga ulaydi, JavaFX `Property` lar Spring Boot ichida.

**Qo'llanish keyslari:**
- SPA (Angular/Vue/React) frontend uchun ekran-markaziy DTO'lar beradigan Spring BFF.
- Vaadin `Binder` orqali forma holatini bean'ga ikki tomonlama bog'lash va validatsiya xatolarini avtomatik ko'rsatish.
- Hilla bilan backend servis metodlarini frontend'da tiplangan funksiya sifatida chaqirish.
- JavaFX desktop ilovasida `ObjectProperty`/`StringProperty` asosidagi ViewModel, servislar Spring'dan inject qilinadi.
- Real vaqt dashboard: WebSocket/SSE orqali keluvchi hodisalar frontend ViewModel'ini yangilaydi (6.23, 6.24).

**Ehtiyot bo'ling:** Backend DTO'ni frontend ViewModel'i bilan 1:1 tenglashtirish API'ni bitta ekranga qattiq bog'laydi - bu BFF uchun maqbul, umumiy (public) API uchun emas. Ikki tomonlama binding katta holatlarda kuzatib bo'lmaydigan yangilanish zanjirlarini tug'diradi; bir tomonlama oqimni (unidirectional data flow) afzal ko'ring.

## 6.16 Post/Redirect/Get (Post/Redirect/Get, PRG)

**Tavsif:** Muammo - forma POST bilan yuborilgach, foydalanuvchi sahifani yangilasa (F5) brauzer POST'ni takrorlaydi va buyurtma ikki marta yaratiladi; "Orqaga" tugmasi ham "formani qayta yuborasizmi?" dialogini chiqaradi. PRG yechimi: POST so'rovini qayta ishlagach, HTML qaytarmasdan natija sahifasiga redirect (302/303) qaytariladi; brauzer GET bajaradi va tarixda faqat GET qoladi. Yangilash xavfsiz, URL ulashish mumkin, ikkilangan yuborish oldini olinadi.

**Spring'da qayerda uchraydi:** `return "redirect:/orders/{id}"` prefiksi (`UrlBasedViewResolver`, `RedirectView`), URI shablon o'zgaruvchilari `RedirectAttributes#addAttribute` orqali to'ldiriladi; `RedirectAttributes#addFlashAttribute` (6.17) bir martalik xabar uchun; `ResponseEntity.status(HttpStatus.SEE_OTHER).location(uri).build()` - REST uslubida 303; `ServletUriComponentsBuilder.fromCurrentContextPath()` - to'liq URL yaratish; Spring Framework 6.0 dan `RequestMappingHandlerAdapter#ignoreDefaultModelOnRedirect` sukut bo'yicha `true` - model atributlari endi redirect URL'iga query parametr sifatida avtomatik qo'shilmaydi. WebFlux: `Rendering.redirectTo("/orders/" + id)`. Proxy ortida to'g'ri sxema/host uchun `ForwardedHeaderFilter` yoki `server.forward-headers-strategy`.

**Qo'llanish keyslari:**
- Buyurtma yaratish formasi: POST → 303 → GET `/orders/{id}` tasdiqlash sahifasi.
- Profilni tahrirlash: muvaffaqiyatdan so'ng profil sahifasiga redirect va flash xabar.
- Login/logout oqimlari: amal bajarilgach bosh sahifaga yoki saqlangan URL'ga redirect.
- Fayl yuklash: katta multipart POST'ni qayta yuborishning oldini olish.
- Ko'p qadamli wizard: har bir qadam POST'dan keyin navbatdagi qadam GET'iga redirect.

**Ehtiyot bo'ling:** PRG brauzerdagi takroriy yuborishni to'xtatadi, lekin ikki marta bosish (double click) yoki tarmoq takrorlashlaridan himoya qilmaydi - bu uchun idempotentlik tokeni yoki unikal cheklov kerak (qarang: [7-bo'lim](07-api-dizayn-patternlari.md), Idempotency Key). Validatsiya xatosida redirect qilish xatolar va kiritilgan qiymatlarni yo'qotadi - xato bo'lsa formani qayta render qiling, redirect faqat muvaffaqiyatda. Foydalanuvchi kiritgan URL'ga redirect "open redirect" zaifligiga olib keladi - faqat nisbiy yoki oq ro'yxatdagi manzillarga yo'naltiring.

```java
@PostMapping("/orders")
public String create(@Valid @ModelAttribute OrderForm form, BindingResult errors,
                     RedirectAttributes redirect) {
    if (errors.hasErrors()) {
        return "orders/new";               // xato: formani qayta ko'rsatish, redirect yo'q
    }
    OrderId id = orderService.create(form.toCommand());
    redirect.addAttribute("id", id.value());
    redirect.addFlashAttribute("message", "Buyurtma yaratildi");
    return "redirect:/orders/{id}";       // PRG: 302 -> GET /orders/{id}
}
```

## 6.17 Flash atributlar / Flash doirasi (Flash Attributes / Flash Scope)

**Tavsif:** Muammo - PRG'dan keyin "Buyurtma saqlandi" kabi bir martalik xabarni redirect orqali keyingi GET'ga etkazish kerak, lekin URL parametri xunuk va qayta yuklashda saqlanib qoladi, sessiya atributi esa tozalashni talab qiladi. Flash scope - faqat keyingi so'rov davomida mavjud bo'lib, o'qilgach avtomatik o'chiriladigan vaqtinchalik saqlash. Atribut redirect'dan oldin saqlanadi, redirect'dan keyingi so'rovda modelga qo'shiladi va yo'q bo'ladi.

**Spring'da qayerda uchraydi:** `RedirectAttributes#addFlashAttribute`, `FlashMap`, `FlashMapManager` (`SessionFlashMapManager` - sukut bo'yicha `HttpSession` da saqlaydi), `RequestContextUtils.getInputFlashMap(request)` va `getOutputFlashMap(request)`; `DispatcherServlet` so'rov boshida input flash map'ni modelga birlashtiradi; flash map maqsadli URL va parametrlarga bog'lanishi mumkin (`FlashMap#setTargetRequestPath`). Bog'liq mexanizmlar: `@SessionAttributes` + `SessionStatus#setComplete()` (ko'p qadamli shakl uchun sessiya doirasi) va `@SessionAttribute` (mavjud sessiya atributini o'qish). WebFlux'da flash scope qo'llab-quvvatlanmaydi - `WebSession` yoki query parametr orqali amalga oshiriladi.

**Qo'llanish keyslari:**
- PRG'dan keyin "muvaffaqiyat/xato" bildirishnomasini bir marta ko'rsatish.
- Shaklni qayta ishlashda yuzaga kelgan tashqi xizmat xatosini redirect orqali forma sahifasiga qaytarish.
- Yaratilgan ob'ekt identifikatorini keyingi sahifada "yangi" sifatida ajratib ko'rsatish.
- Ko'p qadamli wizard'da keyingi qadamga kichik kontekst (tanlangan tarif) uzatish.
- Login'dan keyin bir martalik "xush kelibsiz" yoki parol muddati haqida ogohlantirish.

**Ehtiyot bo'ling:** Flash atributlar sessiyaga tayanadi - stateless REST API'da yoki sessiya yo'q muhitda ishlamaydi va bir nechta instance bo'lsa Spring Session kabi tarqatilgan sessiya saqlash kerak. Katta ob'ektlarni (butun entity) flash'ga joylash sessiyani shishiradi va seriyalashtirish muammolariga olib keladi - faqat kichik, `Serializable` qiymatlar. Parallel tab'lar flash xabarni "noto'g'ri" sahifada ko'rsatishi mumkin; `FlashMap` ni maqsadli yo'lga bog'lang.

## 6.18 Istisnolarni qayta ishlovchi (Exception Handler - @ControllerAdvice, @ExceptionHandler)

**Tavsif:** Muammo - har bir controller o'z try/catch'ini yozsa, xato javoblari formati, status kodlari va log'lash tarqoq va nomuvofiq bo'ladi. Pattern istisnolarni web-qatlam chegarasida markazlashgan ishlovchiga yo'naltiradi: istisno turi → HTTP status + yagona xato tanasi (va log darajasi) xaritasi bir joyda. Domen qatlami o'z istisnolarini tashlaydi, HTTP'ga tarjima faqat web-qatlamda bo'ladi; controller'lar xato kodidan xoli qoladi.

**Spring'da qayerda uchraydi:** `@ExceptionHandler` (controller ichida - lokal, `@ControllerAdvice`/`@RestControllerAdvice` ichida - global; `basePackages`, `assignableTypes`, `annotations` bilan cheklash, `@Order` bilan tartib); `ResponseEntityExceptionHandler` (Spring MVC'ning standart istisnolarini `ProblemDetail` ga tarjima qiladigan bazaviy klass, `spring.mvc.problemdetails.enabled=true` bilan Boot'da yoqiladi); `HandlerExceptionResolver` zanjiri - `ExceptionHandlerExceptionResolver`, `ResponseStatusExceptionResolver` (`@ResponseStatus`, `ResponseStatusException`), `DefaultHandlerExceptionResolver`, `HandlerExceptionResolverComposite`; `ErrorResponse`/`ErrorResponseException` va `ProblemDetail` (RFC 9457 - qarang: [7-bo'lim](07-api-dizayn-patternlari.md), Problem Details); Spring Boot: `BasicErrorController`, `ErrorAttributes`/`DefaultErrorAttributes`, `ErrorViewResolver`, `server.error.include-message/include-stacktrace/include-binding-errors`, `/error` yo'li. WebFlux: `@ExceptionHandler` ham ishlaydi, pastki daraja - `WebExceptionHandler`, `ErrorWebExceptionHandler`.

**Qo'llanish keyslari:**
- Domen istisnolarini (`OrderNotFoundException` → 404, `InsufficientStockException` → 409) `ProblemDetail` ga xaritalash.
- `MethodArgumentNotValidException`/`HandlerMethodValidationException` ni maydon-xato ro'yxati bilan 400 ga aylantirish.
- Kutilmagan istisnolar uchun 500 + korrelyatsiya ID va stack trace'ni faqat log'ga yozish.
- HTML ilovada xato turiga qarab foydalanuvchiga mos sahifa (`error/404.html`, `error/5xx.html`) ko'rsatish.
- Legacy mijozlar uchun eski xato formati va yangi mijozlar uchun Problem Details ni `@ControllerAdvice` ni paket bo'yicha ajratib berish.

**Ehtiyot bo'ling:** `@ExceptionHandler(Exception.class)` bilan hamma narsani 500 ga yutib yuborish diagnostikani o'ldiradi (qarang: [25-bo'lim](25-anti-patternlar.md), Catch-all exception handler, Exception Swallowing) - aniq turlarni xaritalang, qolganini log'lang. Security filtrlarida (`AuthenticationException`, `AccessDeniedException` filtr darajasida) yuzaga kelgan istisnolar `@ControllerAdvice` ga yetmaydi - ular uchun `AuthenticationEntryPoint`/`AccessDeniedHandler` kerak (qarang: [18-bo'lim](18-xavfsizlik-patternlari.md)). Istisno xabarini to'g'ridan-to'g'ri mijozga qaytarish ichki ma'lumot (SQL, klass nomi) sizib chiqishiga olib keladi.

```java
@RestControllerAdvice
class ApiExceptionHandler extends ResponseEntityExceptionHandler {

    @ExceptionHandler(OrderNotFoundException.class)
    ProblemDetail notFound(OrderNotFoundException ex) {
        ProblemDetail pd = ProblemDetail.forStatusAndDetail(HttpStatus.NOT_FOUND, ex.getMessage());
        pd.setType(URI.create("https://api.example.com/problems/order-not-found"));
        pd.setProperty("orderId", ex.orderId());
        return pd;
    }
}
```

## 6.19 Kontent muzokarasi (Content Negotiation)

**Tavsif:** Muammo - bir xil resurs turli mijozlarga turli formatda (JSON, XML, HTML, CSV) va turli tilda kerak, lekin har bir format uchun alohida URL yaratish API'ni ko'paytiradi. Content Negotiation'da mijoz nimani qabul qila olishini e'lon qiladi (`Accept`, `Accept-Language`, `Accept-Encoding`), server esa mos tasvirni tanlaydi yoki 406 Not Acceptable qaytaradi; so'rov tanasining formati `Content-Type` bilan e'lon qilinadi, server uni o'qiy olmasa 415 qaytaradi. Resurs identifikatori (URL) formatdan mustaqil qoladi.

**Spring'da qayerda uchraydi:** `ContentNegotiationManager` va `ContentNegotiationStrategy` lari: `HeaderContentNegotiationStrategy` (sukut, `Accept` header), `ParameterContentNegotiationStrategy` (`?format=json`), `FixedContentNegotiationStrategy`; `WebMvcConfigurer#configureContentNegotiation` (`ContentNegotiationConfigurer#favorParameter`, `mediaType("csv", ...)`, `defaultContentType`), Boot xususiyatlari `spring.mvc.contentnegotiation.*`; `@RequestMapping(produces = "application/json", consumes = "application/json")` - mapping darajasida muzokara; `ContentNegotiatingViewResolver` - view darajasida (HTML vs JSON view); `HttpMessageConverter#canWrite(type, mediaType)` tanlovi (6.20); `MediaType`, `HttpMediaTypeNotAcceptableException` (406), `HttpMediaTypeNotSupportedException` (415). URL kengaytmasi (`.json`) asosidagi strategiya 5.2 dan boshlab deprecated qilingan va yangi loyihalarda ishlatilmaydi. WebFlux: `RequestedContentTypeResolver`. Media type orqali API versiyalash - qarang: [7-bo'lim](07-api-dizayn-patternlari.md) (API Versioning).

**Qo'llanish keyslari:**
- Bitta `/reports/{id}` endpointidan `Accept` ga qarab JSON, CSV yoki PDF qaytarish.
- Brauzer uchun HTML, API mijozi uchun JSON - bir controller, `ContentNegotiatingViewResolver`.
- `Accept-Language` asosida lokalizatsiya qilingan xato xabarlari (6.29 bilan birgalikda).
- `consumes` bilan bir URL'da JSON va `multipart/form-data` so'rovlarini alohida handler'larga ajratish.
- Eski mijozlar uchun `application/vnd.company.v1+json` kabi vendor media type'larni qo'llab-quvvatlash.

**Ehtiyot bo'ling:** `?format=` parametri keshlash va proxy'lar bilan yomon chiqishadi va URL'ni formatga bog'laydi - faqat brauzerdan test qilish qulayligi uchun yoqing. Sukutdagi `Accept: */*` yoki yo'q header holatida qaytariladigan format aniq belgilanmasa, converter tartibiga bog'liq "tasodifiy" natija chiqadi - `defaultContentType` ni o'rnating. Juda ko'p format qo'llab-quvvatlash test matritsasini ko'paytiradi; haqiqatan ishlatiladiganlarini qoldiring.

## 6.20 HTTP xabar konvertori (HttpMessageConverter)

**Tavsif:** Muammo - controller HTTP tanasini baytlardan Java ob'ektiga va aksincha o'zi aylantirsa, format mantiqi hamma joyga tarqaladi. HttpMessageConverter - Strategy patternining (qarang: [3-bo'lim](03-xulq-atvor-patternlari.md)) web ko'rinishi: har bir converter "men ushbu Java turini ushbu media type'da o'qiy/yoza olaman" deb e'lon qiladi, framework esa tur + media type juftligi uchun mos converter'ni tanlaydi. Controller faqat tiplangan ob'ektlar bilan ishlaydi; serializatsiya to'liq almashtiriladigan komponentda.

**Spring'da qayerda uchraydi:** `HttpMessageConverter<T>` (`canRead/canWrite/read/write`), `GenericHttpMessageConverter`; tayyorlari - `MappingJackson2HttpMessageConverter` (Jackson 2; Spring Framework 7 / Boot 4 da Jackson 3 asosidagi `JacksonJsonHttpMessageConverter` birlamchi), `MappingJackson2XmlHttpMessageConverter`, `StringHttpMessageConverter`, `ByteArrayHttpMessageConverter`, `FormHttpMessageConverter` (`application/x-www-form-urlencoded` va multipart), `ResourceHttpMessageConverter`, `ResourceRegionHttpMessageConverter` (Range so'rovlari), `ProtobufHttpMessageConverter`, `GsonHttpMessageConverter`, `JsonbHttpMessageConverter`, `KotlinSerializationJsonHttpMessageConverter`, `Jaxb2RootElementHttpMessageConverter`. Ulanish nuqtalari: `@RequestBody`/`@ResponseBody`/`@RestController`, `HttpEntity`/`ResponseEntity`, `RequestResponseBodyMethodProcessor`; sozlash - `WebMvcConfigurer#extendMessageConverters` (mavjudlarini saqlab qo'shish) va `configureMessageConverters` (to'liq almashtirish), Boot'ning `HttpMessageConverters` bean'i, `Jackson2ObjectMapperBuilderCustomizer` (Boot 3) / Jackson 3 uchun `JsonMapper` customizer'lari (Boot 4); `RequestBodyAdvice`/`ResponseBodyAdvice` (`@JsonView`, `MappingJacksonValue`, javobni o'rash). Mijoz tomonida xuddi shu converter'lar `RestTemplate`/`RestClient` da ishlaydi. WebFlux: `Encoder`/`Decoder`, `HttpMessageReader`/`HttpMessageWriter`, `ServerCodecConfigurer`.

**Qo'llanish keyslari:**
- Barcha JSON javoblarda `ObjectMapper` ni bir xil sozlash (sana formati, `null` ni yashirish, noma'lum maydonlarga toqat).
- Protobuf yoki CBOR kabi ixcham formatni ichki servislar o'rtasida qo'llab-quvvatlash.
- CSV eksport uchun shaxsiy `HttpMessageConverter<List<Row>>` yozish.
- `ResponseBodyAdvice` orqali barcha javoblarni konvert (`{data, meta}`) ichiga o'rash (qarang: [7-bo'lim](07-api-dizayn-patternlari.md), Envelope vs bare response).
- Fayl yuklab berishda `Resource` + `ResourceRegionHttpMessageConverter` bilan `Range` so'rovlarini qo'llash (video streaming).

**Ehtiyot bo'ling:** `configureMessageConverters` sukutdagi ro'yxatni butunlay o'chiradi - ko'pincha `extendMessageConverters` kerak. Bir nechta `ObjectMapper` (Boot'niki va qo'lda yaratilgani) bo'lsa, converter qaysi birini ishlatayotgani chalkashadi - Boot'ning `ObjectMapper` bean'ini customizer orqali sozlang. JPA entity'larni to'g'ridan-to'g'ri seriyalashtirish lazy yuklash, siklik havolalar va ichki maydonlarning sizib chiqishiga olib keladi (qarang: [25-bo'lim](25-anti-patternlar.md), Exposing JPA entities in API).

## 6.21 Argument va qaytish qiymati ishlovchilari (HandlerMethodArgumentResolver / HandlerMethodReturnValueHandler)

**Tavsif:** Muammo - controller metodlari `HttpServletRequest` dan header, cookie, sessiya yoki Security kontekstidan qiymatlarni qo'lda ajratib olishi takrorlanuvchi, test qilinmaydigan kod tug'diradi. Pattern metod parametrini (annotatsiya yoki tur bo'yicha) tanib, uning qiymatini so'rovdan avtomatik hal qiluvchi (resolver) va metod qaytargan qiymatni javobga aylantiruvchi (handler) kengaytiriladigan strategiyalar zanjirini beradi. Controller imzosi deklarativ bo'ladi: `@CurrentUser User user, @RequestId String id`.

**Spring'da qayerda uchraydi:** `HandlerMethodArgumentResolver` (`supportsParameter`, `resolveArgument`) va `HandlerMethodReturnValueHandler` (`supportsReturnType`, `handleReturnValue`); ro'yxatdan o'tkazish - `WebMvcConfigurer#addArgumentResolvers`/`addReturnValueHandlers` (standartlardan keyin), `RequestMappingHandlerAdapter#setCustomArgumentResolvers`; o'rnatilganlari - `RequestParamMethodArgumentResolver`, `PathVariableMethodArgumentResolver`, `RequestHeaderMethodArgumentResolver`, `ServletCookieValueMethodArgumentResolver`, `RequestResponseBodyMethodProcessor` (ham resolver, ham handler), `ServletModelAttributeMethodProcessor`, `PrincipalMethodArgumentResolver`, `SessionAttributeMethodArgumentResolver`; `HandlerMethodArgumentResolverComposite`. Mashhur kengaytmalar: Spring Security `@AuthenticationPrincipal` (`AuthenticationPrincipalArgumentResolver`), `@CurrentSecurityContext`; Spring Data `Pageable`/`Sort` (`PageableHandlerMethodArgumentResolver`, `SortHandlerMethodArgumentResolver`); Spring HATEOAS `PagedResourcesAssembler`. WebFlux'da `org.springframework.web.reactive.result.method.HandlerMethodArgumentResolver` va `HandlerResultHandler`.

**Qo'llanish keyslari:**
- `@CurrentTenant TenantId tenant` - header yoki subdomen asosida tenant'ni hal qilish.
- `@CurrentUser UserProfile user` - Security principal'dan domen foydalanuvchisini yuklab berish.
- `@ClientInfo ClientInfo info` - IP, user-agent, trace ID ni record'ga yig'ish.
- Shaxsiy query parametr sintaksisini (`?filter=status:eq:ACTIVE`) `Specification`/`Filter` ob'ektiga aylantirish.
- Shaxsiy return handler: `Result<T>` yoki `Either<Error, T>` qaytargan controller'ni avtomatik `ResponseEntity`/`ProblemDetail` ga xaritalash.

**Ehtiyot bo'ling:** Shaxsiy resolver'lar standartlardan keyin tekshiriladi - `@RequestParam` kabi o'rnatilgan annotatsiya bilan to'qnashsa sizniki ishlamaydi; shaxsiy annotatsiya yoki noyob tur ishlating. Resolver ichida ma'lumotlar bazasiga murojaat (har so'rovda foydalanuvchini yuklash) yashirin I/O va N+1 ga olib keladi - natijani so'rov atributida keshlang yoki yengil identifikator qaytaring. Resolver'larning tartibi va `supportsParameter` shartlari testlar bilan qoplanishi kerak.

```java
public class CurrentTenantArgumentResolver implements HandlerMethodArgumentResolver {
    @Override
    public boolean supportsParameter(MethodParameter p) {
        return p.hasParameterAnnotation(CurrentTenant.class)
            && TenantId.class.isAssignableFrom(p.getParameterType());
    }
    @Override
    public Object resolveArgument(MethodParameter p, ModelAndViewContainer mav,
                                  NativeWebRequest req, WebDataBinderFactory f) {
        String header = req.getHeader("X-Tenant-Id");
        if (header == null) throw new MissingRequestHeaderException("X-Tenant-Id", p);
        return new TenantId(header);
    }
}
```

## 6.22 Funksional endpointlar (Functional Endpoints - RouterFunction)

**Tavsif:** Muammo - annotatsiyalar asosidagi marshrutlash "sehrli" va dinamik emas: yo'llar kompilyatsiya vaqtida annotatsiyalarda qotib qoladi, ularni konfiguratsiya yoki plugin asosida yig'ish qiyin. Funksional uslubda marshrutlash - bu oddiy kod: `RouterFunction` so'rov predikatlarini (`GET("/orders/{id}")`, `accept(JSON)`) `HandlerFunction` larga (so'rovni javobga aylantiruvchi funksiya) xaritalaydi, filtrlar esa funksiya kompozitsiyasi orqali qo'shiladi. Natija aniq, test qilinadigan, dinamik yig'iladigan marshrutlar jadvali.

**Spring'da qayerda uchraydi:** WebMvc.fn - `org.springframework.web.servlet.function`: `RouterFunction<ServerResponse>`, `RouterFunctions.route()` builder'i (`.GET(...)`, `.POST(...)`, `.nest(...)`, `.filter(...)`, `.onError(...)`, `.build()`), `RequestPredicates` (`path`, `accept`, `contentType`, `queryParam`), `HandlerFunction<ServerResponse>`, `ServerRequest`/`ServerResponse`, `HandlerFilterFunction`; `DispatcherServlet` ga `RouterFunctionMapping` + `HandlerFunctionAdapter` orqali ulanadi va annotatsiyali controller'lar bilan yonma-yon ishlaydi - `RouterFunction` bean'i sifatida e'lon qilinadi. Kotlin uchun `router { }` DSL. Reaktiv WebFlux.fn (`org.springframework.web.reactive.function.server`, `coRouter`) - qarang: [19-bo'lim](19-reactive-patternlar.md) (WebFlux functional endpoints). Spring Cloud Gateway MVC ham `RouterFunction` asosida qurilgan.

**Qo'llanish keyslari:**
- Konfiguratsiya yoki plugin ro'yxati asosida ishga tushishda dinamik yig'iladigan marshrutlar (ko'p ijarachili yo'llar, feature flag bilan yoqiladigan endpointlar).
- Kichik, yengil servislar yoki sidecar'lar - annotatsiya skanerisiz, aniq funksiya kompozitsiyasi.
- Bir guruh endpoint uchun umumiy filtr (autentifikatsiya, log) ni `nest` + `filter` bilan qo'llash.
- Marshrutlash jadvalini `RouterFunction` birlik testi bilan `MockMvc`/servlet'siz tekshirish.
- Spring Cloud Gateway MVC bilan proxy marshrutlarini kod sifatida tavsiflash.

**Ehtiyot bo'ling:** Funksional va annotatsiyali uslublarni bir modulda aralashtirish jamoani chalg'itadi - modul darajasida bitta uslubni tanlang. `@Valid`, `@RequestBody` kabi deklarativ qulayliklar `ServerRequest` da yo'q (`request.body(Class)` va qo'lda validatsiya kerak) - qisqa kod kutmang. `RouterFunction` da handler'lar lambda bo'lgani uchun stack trace va kuzatuv nomlari kamroq ma'noli; `HandlerFunction` larni nomlangan metodlarga ajrating.

```java
@Configuration
class OrderRoutes {
    @Bean
    RouterFunction<ServerResponse> orderRouter(OrderHandler handler) {
        return RouterFunctions.route()
            .nest(RequestPredicates.path("/api/orders"), b -> b
                .GET("/{id}", RequestPredicates.accept(MediaType.APPLICATION_JSON), handler::get)
                .POST("", RequestPredicates.contentType(MediaType.APPLICATION_JSON), handler::create))
            .filter((req, next) -> req.headers().firstHeader("X-Tenant-Id") == null
                ? ServerResponse.badRequest().build()
                : next.handle(req))
            .build();
    }
}
```

## 6.23 Server tomonidan yuboriladigan hodisalar (Server-Sent Events, SSE)

**Tavsif:** Muammo - brauzerga serverdan bir tomonlama, real vaqt yangilanishlarini (bildirishnoma, progress, ticker) etkazish kerak, lekin WebSocket to'liq ikki tomonlama kanal uchun ortiqcha, polling esa isrofgarchilik. SSE - oddiy HTTP javobi (`text/event-stream`) ni ochiq qoldirib, matnli hodisalarni ketma-ket yozish; brauzerdagi `EventSource` avtomatik qayta ulanadi va `Last-Event-ID` bilan davom ettiradi. Proxy'lar va HTTP infratuzilmasi bilan tabiiy ishlaydi, HTTP/2 da ulanishlar cheklovi ham yumshaydi.

**Spring'da qayerda uchraydi:** Spring MVC - `SseEmitter` (`send`, `complete`, `completeWithError`, `onTimeout`, `onCompletion`, `onError`), `SseEmitter.event().id(...).name(...).data(...).reconnectTime(...)`, umumiyroq `ResponseBodyEmitter`; asinxron servlet ishlovi va `spring.mvc.async.request-timeout`, `WebMvcConfigurer#configureAsyncSupport` (6.33). WebFlux - `Flux<ServerSentEvent<T>>` yoki `produces = MediaType.TEXT_EVENT_STREAM_VALUE` bilan `Flux<T>` (qarang: [19-bo'lim](19-reactive-patternlar.md), Streaming responses). Mijoz tomonida `WebClient` (`bodyToFlux(ServerSentEvent.class)`); Spring AI'ning stream'li chat javoblari ham SSE orqali. Emitter'larni saqlash uchun `CopyOnWriteArrayList`/`ConcurrentHashMap` va hodisa manbai sifatida `ApplicationEvent` yoki Kafka consumer (qarang: 5- va 16-bo'limlar).

**Qo'llanish keyslari:**
- Uzoq davom etadigan vazifaning (import, hisobot) progress foizini jonli ko'rsatish.
- Foydalanuvchi bildirishnomalari lentasi (yangi xabar, buyurtma holati o'zgardi).
- Dashboard'da metrikalar va narxlar ticker'ini jonli yangilash.
- LLM javobini token-token stream'lash (Spring AI bilan).
- Admin panelda log yoki audit hodisalarini jonli kuzatish.

**Ehtiyot bo'ling:** Har bir ochiq SSE ulanishi Servlet stack'da thread egallamaydi (asinxron), lekin emitter'lar xotirada qoladi - uzilgan mijozlarni `onCompletion`/`onTimeout` da tozalang, aks holda sizish bo'ladi. Load balancer, Nginx yoki Spring Cloud Gateway javobni buferlashi mumkin (`X-Accel-Buffering: no`, `proxy_buffering off`) va idle timeout'lar ulanishni uzadi - heartbeat (`:ping` comment) yuboring. SSE faqat matn va bir tomonlama; ikki tomonlama yoki binar oqim kerak bo'lsa WebSocket (6.24). Ko'p instance'li muhitda hodisani barcha emitter'larga etkazish uchun Redis pub/sub yoki broker kerak.

## 6.24 WebSocket va STOMP (WebSocket / STOMP)

**Tavsif:** Muammo - chat, hamkorlikda tahrirlash, o'yin yoki savdo terminali kabi ilovalar past kechikishli, ikki tomonlama, doimiy kanalni talab qiladi; HTTP so'rov-javob modeli bunga mos emas. WebSocket bitta TCP ulanish ustida ikki tomonlama freym oqimini beradi; STOMP esa uning ustida xabar semantikasi (destination, subscribe, send, ack) qo'shib, pub/sub modelini va broker bilan integratsiyani standartlashtiradi. Natijada "mavzuga obuna bo'l, xabar yubor" - xom freymlar emas.

**Spring'da qayerda uchraydi:** `spring-boot-starter-websocket`. Past daraja: `@EnableWebSocket`, `WebSocketConfigurer#registerWebSocketHandlers`, `WebSocketHandler`/`TextWebSocketHandler`/`BinaryWebSocketHandler`, `WebSocketSession`, `HandshakeInterceptor`, `ConcurrentWebSocketSessionDecorator` (parallel yozishdan himoya). STOMP: `@EnableWebSocketMessageBroker`, `WebSocketMessageBrokerConfigurer` (`registerStompEndpoints`, `configureMessageBroker` - `enableSimpleBroker` yoki `enableStompBrokerRelay` RabbitMQ/ActiveMQ ga, `setApplicationDestinationPrefixes`, `setUserDestinationPrefix`), `@MessageMapping`, `@SendTo`, `@SendToUser`, `@SubscribeMapping`, `@Payload`, `@DestinationVariable`, `@MessageExceptionHandler`, `SimpMessagingTemplate` (`convertAndSend`, `convertAndSendToUser`), `ChannelInterceptor`, SockJS fallback (`withSockJS()`), `SimpUserRegistry`. Xavfsizlik: `AuthorizationManager<Message<?>>` / `MessageMatcherDelegatingAuthorizationManager` (qarang: [18-bo'lim](18-xavfsizlik-patternlari.md)). WebFlux: reaktiv `WebSocketHandler` va `HandlerMapping`. Muqobil binar protokol - RSocket (`spring-boot-starter-rsocket`, `@MessageMapping`). Xabar modellari - qarang: [15-bo'lim](15-enterprise-integration-patterns-i-xabarlar.md) (Publish-Subscribe Channel).

**Qo'llanish keyslari:**
- Ko'p foydalanuvchili chat yoki qo'llab-quvvatlash kanali (`/topic/room.{id}`, `/user/queue/replies`).
- Hamkorlikda tahrirlash va kursor holatini sinxronlash.
- Savdo terminali yoki auksion: narxlar oqimi va buyurtma tasdiqlari past kechikish bilan.
- IoT boshqaruv paneli: qurilma holatini olish va buyruq yuborish bir kanalda.
- Server tomonidan boshlanadigan amaliyot: foydalanuvchini aniq sessiyadan chiqarish yoki pop-up ko'rsatish.

**Ehtiyot bo'ling:** `SimpleBroker` bitta JVM ichida ishlaydi - ikki va undan ortiq instance'da obunalar bo'linib ketadi; ishlab chiqarishda `StompBrokerRelay` (RabbitMQ/ActiveMQ) yoki Redis orqali tarqatish shart. WebSocket ulanishi uzoq umr ko'radi: autentifikatsiya handshake'da bir marta bo'ladi, token muddati tugaganini alohida tekshirish kerak; CSRF va `Origin` tekshiruvini (`setAllowedOriginPatterns`) o'chirmang. Load balancer idle timeout'lari va korporativ proxy'lar ulanishni uzadi - heartbeat'larni sozlang va SockJS fallback'ni baholang. Faqat server→mijoz oqimi kerak bo'lsa SSE (6.23) ancha sodda.

## 6.25 Mijoz tomonidagi sessiya holati (Client Session State)

**Tavsif:** Fowler'ning uch sessiya holati patternidan birinchisi: so'rovlar orasidagi holat mijozda saqlanadi - cookie, yashirin forma maydoni, URL parametri, brauzer `localStorage` yoki imzolangan token ichida; server har so'rovda holatni mijozdan qabul qiladi va o'zida hech narsa saqlamaydi. Server stateless bo'lgani uchun gorizontal masshtablash va instance almashtirish ahamiyatsiz bo'ladi, lekin holat hajmi, xavfsizligi (o'zgartirish, o'qish) va har so'rovda uzatilishi mijoz zimmasiga tushadi.

**Spring'da qayerda uchraydi:** `@CookieValue`, `ResponseCookie` builder'i (`httpOnly`, `secure`, `sameSite`, `maxAge`) va `HttpServletResponse#addCookie`; `CookieLocaleResolver` (lokalni cookie'da saqlash); yashirin maydonlar `th:field` bilan (`<input type="hidden">`); URL'dagi holat (`?page=2&sort=name`) - `@RequestParam` + `Pageable`; stateless autentifikatsiya - JWT/opaque token'lar `Authorization` header'ida yoki `HttpOnly` cookie'da (qarang: [18-bo'lim](18-xavfsizlik-patternlari.md), OAuth2 Resource Server, Session Management), Remember-Me token'i (qarang: [18-bo'lim](18-xavfsizlik-patternlari.md)); CSRF double-submit cookie (qarang: [18-bo'lim](18-xavfsizlik-patternlari.md)). SPA'larda holat brauzer xotirasida bo'lib, Spring tomoni faqat `SessionCreationPolicy.STATELESS` bo'ladi. Spring Session `DefaultCookieSerializer` - hatto server holati bo'lsa ham, uning identifikatori mijoz cookie'sida.

**Qo'llanish keyslari:**
- Stateless REST API: JWT access token mijozda, server sessiya saqlamaydi.
- Foydalanuvchi afzalliklari (til, tema, jadval sahifa o'lchami) ni cookie'da saqlash.
- Qidiruv filtrlari va sahifalashni URL'da saqlash - ulashiladigan, bookmark qilinadigan havolalar.
- Ko'p qadamli forma holatini imzolangan yashirin maydonda yoki mijoz xotirasida tashib yurish (CDN ortidagi statik frontend).
- Mehmon savatchasini (anonymous cart) cookie identifikatori yoki `localStorage` da saqlash.

**Ehtiyot bo'ling:** Mijozdagi har qanday holat o'zgartirilishi mumkin deb hisoblang - narx, rol, chegirma kabi qiymatlarni hech qachon mijozdan qabul qilmang, imzolang (HMAC) yoki serverda qayta hisoblang. Cookie'lar har so'rov bilan ketadi (4 KB chegara, trafik yuki) va `HttpOnly`/`Secure`/`SameSite` bo'lmasa XSS/CSRF'ga ochiq. JWT'ni "sessiya o'rnini bosuvchi" sifatida ishlatish bekor qilish (revocation) muammosini tug'diradi - qisqa muddat + refresh rotation (qarang: [18-bo'lim](18-xavfsizlik-patternlari.md)).

## 6.26 Server tomonidagi sessiya holati (Server Session State)

**Tavsif:** Holat server xotirasida (yoki serverga yaqin saqlashda) ushlanadi, mijoz faqat sessiya identifikatorini (cookie) tashiydi. Dasturlash eng sodda - ob'ektni sessiyaga joylash kifoya - va mijozga ishonish shart emas. Narxi: server endi stateful; instance ishdan chiqsa holat yo'qoladi, gorizontal masshtablash sticky session yoki sessiya replikatsiyasini talab qiladi, xotira iste'moli faol foydalanuvchilar soniga proporsional o'sadi.

**Spring'da qayerda uchraydi:** `HttpSession` (`@SessionAttribute` o'qish, `@SessionAttributes` + `SessionStatus` - controller darajasidagi "conversation" scope), `@SessionScope` bean'lar (qarang: [5-bo'lim](05-spring-core-ichidagi-patternlar-xaritasi.md), Bean scopes & scoped proxy), `HttpSessionListener`, `server.servlet.session.timeout`, `server.servlet.session.cookie.*` (`name`, `http-only`, `secure`, `same-site`), `server.servlet.session.tracking-modes=cookie` (URL rewriting'ni o'chirish); Spring Security - `SecurityContext` sukut bo'yicha sessiyada (`HttpSessionSecurityContextRepository`), sessiya fiksatsiyasi himoyasi va parallel sessiyalarni cheklash (qarang: [18-bo'lim](18-xavfsizlik-patternlari.md), Session Management). Tarqatilgan sessiya: Spring Session (`spring-session-data-redis`, `@EnableRedisHttpSession`, `SessionRepository`, `SessionRepositoryFilter`, `FindByIndexNameSessionRepository` - foydalanuvchi bo'yicha sessiyalarni topish), Hazelcast, Tomcat `DeltaManager` (kam ishlatiladi). WebFlux: `WebSession`, `WebSessionManager`, `WebSessionStore` (`InMemoryWebSessionStore` sukut, Spring Session reaktiv Redis). Flash scope (6.17) ham sessiyaga tayanadi.

**Qo'llanish keyslari:**
- Thymeleaf asosidagi klassik web-ilovada autentifikatsiya qilingan foydalanuvchi sessiyasi.
- Ko'p qadamli wizard'da yarim to'ldirilgan shaklni `@SessionAttributes` da ushlab turish.
- Savatcha yoki draft ma'lumotini kirgan foydalanuvchi uchun Redis-asoslangan sessiyada saqlash.
- OAuth2 login oqimida `state`/PKCE verifier'ini sessiyada saqlash (`spring-security-oauth2-client`).
- Server tomonidagi UI framework'lar (Vaadin) - komponent daraxti to'liq sessiyada yashaydi.

**Ehtiyot bo'ling:** Sessiyaga katta ob'ektlar (entity grafigi, hisobot natijalari) joylash xotirani to'ldiradi va Redis'ga seriyalashtirish narxini oshiradi - faqat identifikator va kichik DTO. Sessiyadagi ob'ektlar `Serializable` bo'lishi va versiya o'zgarishida (deploy) deseriyalanishi kerak - JSON seriyalashtirish (`GenericJackson2JsonRedisSerializer`) klass versiyasiga kamroq bog'liq. Sticky session'ga tayanish nol-uzilishli deploy va autoscaling'ni murakkablashtiradi; API uchun stateless (6.25), UI uchun Spring Session afzal. `@SessionAttributes` ni `setComplete()` siz qoldirish sessiyada "eskirgan" holat qoldiradi.

## 6.27 Ma'lumotlar bazasidagi sessiya holati (Database Session State)

**Tavsif:** Sessiya holati server xotirasida emas, ma'lumotlar bazasida (yoki shunga o'xshash bardoshli saqlashda) ushlanadi; server stateless qoladi, mijoz identifikatorni tashiydi, har so'rovda holat bazadan o'qiladi va yoziladi. Instance ishdan chiqsa yoki almashtirilsa holat saqlanib qoladi, barcha instance'lar bir xil holatni ko'radi, sessiya umri va auditi bazaning vositalariga bo'ysunadi. Narxi - har so'rovda qo'shimcha I/O va "yetim" (tugallanmagan) holatlarni tozalash zarurati.

**Spring'da qayerda uchraydi:** Spring Session JDBC: `spring-session-jdbc`, `@EnableJdbcHttpSession`, `JdbcIndexedSessionRepository`, `SPRING_SESSION` va `SPRING_SESSION_ATTRIBUTES` jadvallari (sxema skriptlari `org/springframework/session/jdbc/schema-*.sql`), `spring.session.jdbc.initialize-schema`, `spring.session.jdbc.cleanup-cron`, `spring.session.timeout` - Boot 3+ da `spring.session.store-type` olib tashlangan, saqlash turi classpath'dan aniqlanadi. Spring Session MongoDB (`spring-session-data-mongodb`). Domen darajasida: "Work-in-progress" / draft entity'lar - `ShoppingCart`, `ApplicationDraft` jadvallari, foydalanuvchi yoki anonim token bo'yicha kalitlangan, Spring Data repository orqali (qarang: [9-bo'lim](09-malumotlarga-kirish-va-orm-patternlari.md)); uzoq biznes jarayonlar uchun Process Manager/Saga holati (qarang: 15- va 14-bo'limlar). Sessiya jadvalini tozalash - `@Scheduled` yoki ShedLock bilan (qarang: [20-bo'lim](20-batch-va-scheduling-patternlari.md)).

**Qo'llanish keyslari:**
- Redis'siz infratuzilmada ko'p instance'li UI ilovasi uchun Spring Session JDBC.
- Savatcha, murojaat anketasi yoki hujjat draft'ini kunlar davomida, qurilmalar aro saqlash.
- Audit talabi bo'lgan sohalarda (bank, davlat) foydalanuvchi sessiyalarini bazada kuzatish.
- Uzoq davom etadigan, qayta tiklanadigan (resumable) ko'p qadamli jarayon holati.
- Anonim savatchani ro'yxatdan o'tgach foydalanuvchiga biriktirish (token → user_id migratsiyasi).

**Ehtiyot bo'ling:** Har so'rovda sessiyani bazadan o'qish/yozish asosiy bazaga yuk va kechikish qo'shadi - yuqori trafikli tizimlarda Redis (6.26) yoki stateless (6.25) afzal; JDBC sessiya kichik/o'rta ilovalar uchun. Sessiya atributlarini bazaga BLOB sifatida seriyalashtirish so'rovlab bo'lmaydigan, versiyaga bog'liq ma'lumot yaratadi - biznes ma'noli holatni (savatcha) alohida, normal jadvallarda saqlang, sessiyada faqat identifikatorlar. Tozalash ishini unutish jadvalni cheksiz o'stiradi (qarang: [10-bo'lim](10-malumotlarni-boshqarish-va-taqsimlash.md), Archive / Purge).

## 6.28 Ma'lumotlarni bog'lash va forma ob'ekti (Data Binding / Form Backing Object)

**Tavsif:** Muammo - HTTP so'rov parametrlari matn ko'rinishida keladi; ularni tiplangan ob'ektga aylantirish, konvertatsiya xatolarini yig'ish va validatsiya qilish qo'lda yozilsa zerikarli va xatoga moyil. Data Binding so'rov parametrlarini nomlari bo'yicha ob'ekt xususiyatlariga avtomatik bog'laydi, konvertatsiya va validatsiya xatolarini `Errors` ob'ektida to'playdi; Form Backing Object - shu bog'lanish uchun maxsus yaratilgan, faqat formani ifodalovchi ob'ekt (domen entity'si emas). Shablon (`th:object`/`th:field`) ham ayni ob'ektdan qiymat va xatolarni o'qiydi - ikki tomonlama forma bog'lanishi.

**Spring'da qayerda uchraydi:** `WebDataBinder`/`DataBinder`, `@ModelAttribute` (parametr - bog'lash, metod - model tayyorlash), `@InitBinder` (`setAllowedFields`, `setDisallowedFields`, `registerCustomEditor`, `addValidators`), `BindingResult`/`Errors`/`FieldError`, `@Valid`/`@Validated` (Bean Validation), `BindException`, `MethodArgumentNotValidException`, Spring 6.1+ o'rnatilgan metod validatsiyasi `HandlerMethodValidationException`; record va konstruktor asosida bog'lash (Spring 6.1+, `@BindParam` bilan parametr nomini o'zgartirish); `ConversionService`/`Formatter`/`@DateTimeFormat`/`@NumberFormat` (qarang: [5-bo'lim](05-spring-core-ichidagi-patternlar-xaritasi.md), ConversionService); Thymeleaf `th:object`, `th:field`, `#fields.hasErrors('email')`, `th:errors`; `@RequestBody` uchun bog'lash `HttpMessageConverter` orqali bo'lib, `WebDataBinder` qatnashmaydi (lekin `@Valid` ishlaydi). `@ConfigurationProperties` ham xuddi shu `Binder` g'oyasining konfiguratsiya varianti (qarang: [5-bo'lim](05-spring-core-ichidagi-patternlar-xaritasi.md)). WebFlux: `WebExchangeDataBinder`, `WebExchangeBindException`.

**Qo'llanish keyslari:**
- Ro'yxatdan o'tish shakli: `RegistrationForm` record'i, `@Valid`, xatolar `th:errors` bilan maydon yonida.
- Qidiruv filtrlari (`?status=ACTIVE&from=2026-01-01`) ni `SearchCriteria` ob'ektiga bog'lash, `@DateTimeFormat` bilan.
- Ichki ob'ektlar va ro'yxatlar (`items[0].quantity`, `address.city`) bilan murakkab shakllar.
- Admin panelda tahrirlash shakli: entity → form DTO → bog'lash → validatsiya → servis orqali yangilash.
- `@InitBinder` bilan kirish matnlarini trim qilish (`StringTrimmerEditor`) va sana formatini jamoa standartiga keltirish.

**Ehtiyot bo'ling:** JPA entity'ni to'g'ridan-to'g'ri `@ModelAttribute` qilish mass-assignment zaifligini tug'diradi - foydalanuvchi `role=ADMIN` yoki `balance=...` yubora oladi; alohida form ob'ekti yoki `setAllowedFields` shart (qarang: [25-bo'lim](25-anti-patternlar.md), Exposing JPA entities in API). Bog'lash xatolarini `BindingResult` siz qoldirish 400 o'rniga istisno beradi - forma handler'larida `BindingResult` ni darhol `@ModelAttribute` dan keyin qo'ying. Validatsiya annotatsiyalari biznes qoidalarini (unikal email) o'rnini bosmaydi - ularni servis qatlamida tekshirib, `errors.rejectValue` bilan formaga qaytaring.

## 6.29 Lokal va tema aniqlovchilar (LocaleResolver / ThemeResolver)

**Tavsif:** Muammo - foydalanuvchining tili, mintaqasi, vaqt zonasi va ko'rinish temasi har so'rovda aniqlanishi va barcha formatlash/xabar mexanizmlariga tarqalishi kerak, lekin bu qaror (header? cookie? sessiya? profil?) joylashuvga qarab o'zgaradi. Pattern "qaysi lokal/tema" qarorini almashtiriladigan strategiyaga ajratadi: Front Controller so'rov boshida resolver'dan lokalni oladi, kontekstga joylaydi, va qolgan barcha komponentlar (xabar manbai, formatlovchilar, view) shu kontekstni o'qiydi.

**Spring'da qayerda uchraydi:** `LocaleResolver` va `LocaleContextResolver` (vaqt zonasi bilan): `AcceptHeaderLocaleResolver` (sukut; `Accept-Language`), `CookieLocaleResolver`, `SessionLocaleResolver`, `FixedLocaleResolver`; `LocaleChangeInterceptor` (`?lang=uz` bilan o'zgartirish), `LocaleContextHolder`, `RequestContextUtils.getLocale(request)`, `TimeZoneAwareLocaleContext`; Boot: `spring.web.locale`, `spring.web.locale-resolver=fixed|accept-header`; iste'molchilar - `MessageSource` (qarang: [5-bo'lim](05-spring-core-ichidagi-patternlar-xaritasi.md), MessageSource), Thymeleaf `#{...}`, `@DateTimeFormat`/`@NumberFormat` lokalga bog'liq formatlash, Bean Validation xabarlari (`LocalValidatorFactoryBean#setValidationMessageSource`). WebFlux: `LocaleContextResolver`, `AcceptHeaderLocaleContextResolver`. Tema: `ThemeResolver` (`FixedThemeResolver`, `CookieThemeResolver`, `SessionThemeResolver`), `ThemeChangeInterceptor`, `ThemeSource` - Spring Framework 6.0 da deprecated va 7.0 da olib tashlangan; zamonaviy yondashuv - CSS o'zgaruvchilari, `prefers-color-scheme` va foydalanuvchi profilidagi tema qiymatini modelga/cookie'ga berish (6.13, 6.25).

**Qo'llanish keyslari:**
- O'zbek/rus/ingliz tilli davlat xizmati portali: `CookieLocaleResolver` + `LocaleChangeInterceptor`, til tanlagich.
- API xato xabarlarini `Accept-Language` bo'yicha lokalizatsiya qilish (`AcceptHeaderLocaleResolver` + `MessageSource`).
- Kirgan foydalanuvchi profilidagi tilni ustuvor qilib, shaxsiy `LocaleResolver` yozish (profil → cookie → header).
- Vaqt zonasiga mos sana ko'rsatish uchun `TimeZoneAwareLocaleContext` dan `ZoneId` olish.
- Ko'p ijarachili SaaS'da tenant brendingi (logo, ranglar) uchun tema qiymatini `@ControllerAdvice` orqali modelga berish.

**Ehtiyot bo'ling:** `AcceptHeaderLocaleResolver` lokalni o'zgartirishni qo'llab-quvvatlamaydi - `LocaleChangeInterceptor` bilan ishlatganda `UnsupportedOperationException` olinadi; cookie yoki sessiya resolver'i kerak. `LocaleContextHolder` thread'ga bog'langan: `@Async` yoki reaktiv kodda lokal yo'qoladi, aniq parametr sifatida uzating. Sana/valyuta formatlashni frontend'ga va backend'ga ikki marta amalga oshirish nomuvofiqlik tug'diradi - formatlash qayerda bo'lishini bitta joyda hal qiling.

## 6.30 Statik resurslarni xizmat qilish (Static Resource Handling)

**Tavsif:** Muammo - CSS, JS, rasm, shrift va SPA bundle'lari kabi statik fayllar `DispatcherServlet` orqali o'tsa ham, ular uchun controller yozish ma'nosiz; ayni paytda ularga keshlash sarlavhalari, versiyalash (cache busting), siqish va xavfsiz yo'l tekshiruvi kerak. Pattern statik resurslarni alohida, deklarativ sozlanadigan handler orqali xizmat qiladi: resurs joylashuvlari, URL namunalari, kesh siyosati va resolver/transformer zanjiri (versiya, siqish, URL qayta yozish) konfiguratsiyada e'lon qilinadi.

**Spring'da qayerda uchraydi:** `ResourceHttpRequestHandler`, `WebMvcConfigurer#addResourceHandlers` → `ResourceHandlerRegistry` (`addResourceHandler("/assets/**").addResourceLocations("classpath:/static/").setCacheControl(...)`), `ResourceChainRegistration` (`resourceChain(true)`), `ResourceResolver` lar - `PathResourceResolver` (xavfsiz yo'l tekshiruvi), `VersionResourceResolver` (`ContentVersionStrategy` - fayl hash'i, `FixedVersionStrategy`), `EncodedResourceResolver` (oldindan siqilgan `.gz`/`.br`), `LiteWebJarsResourceResolver` (Spring 6.2+, `webjars-locator-lite`), `CachingResourceResolver`; `ResourceTransformer` lar - `CssLinkResourceTransformer`; `ResourceUrlProvider` va `ResourceUrlEncodingFilter` (shablonlarda versiyalangan URL yaratish). Boot: `spring.web.resources.static-locations` (sukut `classpath:/META-INF/resources/`, `/resources/`, `/static/`, `/public/`), `spring.mvc.static-path-pattern`, `spring.web.resources.cache.cachecontrol.*`, `spring.web.resources.chain.strategy.content.enabled`, `spring.web.resources.add-mappings=false` (o'chirish), `WelcomePageHandlerMapping` (`index.html`). WebFlux: `ResourceWebHandler`, `spring.webflux.static-path-pattern`. CDN va bulutli joylashtirish - qarang: [17-bo'lim](17-resilience-va-cloud-dizayn-patternlari.md) (Static Content Hosting); HTTP keshlash sarlavhalari - qarang: [11-bo'lim](11-keshlash-patternlari.md) (HTTP caching).

**Qo'llanish keyslari:**
- Thymeleaf ilovasi uchun CSS/JS'ni kontent hash'li URL (`/css/app-9f8e7d.css`) bilan va bir yillik `Cache-Control: max-age` bilan xizmat qilish.
- SPA bundle'ini (React/Angular) `classpath:/static/` dan xizmat qilish va noma'lum yo'llarni `index.html` ga yo'naltirish (`PathResourceResolver#getResource` ni override qilish).
- WebJars orqali frontend kutubxonalarini Maven bog'liqliklar sifatida boshqarish.
- Oldindan brotli/gzip siqilgan assetlarni `EncodedResourceResolver` bilan `Accept-Encoding` ga qarab qaytarish.
- Foydalanuvchi yuklagan rasmlarni fayl tizimidan (`file:/var/app/uploads/`) alohida handler bilan, qisqa kesh muddati bilan xizmat qilish.

**Ehtiyot bo'ling:** Katta trafikli statik kontentni JVM'dan xizmat qilish CPU va ulanishlarni isrof qiladi - ishlab chiqarishda CDN yoki reverse proxy (Nginx) oldinga qo'yiladi, Spring faqat fallback. Versiyalash yoqilganda shablonlardagi URL'lar `ResourceUrlProvider`/`@{...}` orqali yaratilishi kerak, aks holda eski (keshdagi) nomlar 404 beradi. `addResourceLocations("file:" + userPath)` da yo'l tekshiruvisiz (`PathResourceResolver` saqlab qolinmasa) directory traversal xavfi bor. `index.html` fallback'ini `/api/**` ga ham qo'llash API 404'larini HTML'ga aylantiradi - namunalarni ajrating.

## 6.31 Multipart (fayl yuklash) ishlovi (Multipart Handling)

**Tavsif:** Muammo - fayl yuklash (`multipart/form-data`) oddiy forma parametrlaridan farq qiladi: tana katta, bir nechta qism (part) dan iborat, har biri o'z `Content-Type` va nomiga ega, xotiraga to'liq yuklab bo'lmaydi. Pattern multipart tahlilini almashtiriladigan resolver'ga topshiradi: u so'rovni qismlarga ajratadi, kichik qismlarni xotirada, kattalarini vaqtinchalik faylda saqlaydi (yoki stream qiladi), hajm chegaralarini tekshiradi va controller'ga tiplangan `MultipartFile`/`Part` ob'ektlarini beradi.

**Spring'da qayerda uchraydi:** `MultipartResolver` - `StandardServletMultipartResolver` (Servlet 3.0+ API asosida, sukut; `CommonsMultipartResolver` Spring Framework 6.0 da olib tashlangan), `MultipartHttpServletRequest`, `MultipartFile` (`getInputStream`, `transferTo(Path)`, `getOriginalFilename`, `getContentType`), `@RequestParam MultipartFile file`, `@RequestPart` (JSON qism + fayl qism birgalikda, `HttpMessageConverter` orqali), `jakarta.servlet.http.Part`, `MultipartConfigElement`; Boot: `spring.servlet.multipart.enabled`, `max-file-size`, `max-request-size`, `file-size-threshold`, `location`, `resolve-lazily`; `MaxUploadSizeExceededException` (odatda 413 ga xaritalanadi); mijoz tomonida `MultipartBodyBuilder`, `RestClient`/`RestTemplate` + `MultiValueMap<String, Object>` va `FileSystemResource`/`ByteArrayResource`. WebFlux: `FilePart`, `Part`, `Flux<DataBuffer>`, `PartEvent` (Spring 6.0+, to'liq stream'li ishlov), `DefaultPartHttpMessageReader`, `spring.webflux.multipart.*`. Fayllarni yuklab berish uchun `Resource`/`StreamingResponseBody` va `Content-Disposition` (`ContentDisposition.attachment().filename(...)`).

**Qo'llanish keyslari:**
- Foydalanuvchi avatarini yuklash: hajm va MIME tekshiruvi, qayta o'lchash, obyekt saqlashga (S3/MinIO) yozish.
- Hujjat + metadata'ni bitta so'rovda yuborish: `@RequestPart("meta") DocumentMeta` va `@RequestPart("file") MultipartFile`.
- Ko'p faylli yuklash (`MultipartFile[]` yoki `List<MultipartFile>`) va har biri uchun natija ro'yxati.
- Katta CSV import: `resolve-lazily` yoki WebFlux `PartEvent` bilan faylni to'liq xotiraga olmasdan qatorma-qator qayta ishlash.
- Chunked/resumable yuklash protokoli (tus kabi) uchun qismlarni vaqtinchalik saqlab, oxirida birlashtirish.

**Ehtiyot bo'ling:** Hajm chegaralari ikki darajada ishlaydi - Spring/Boot xususiyatlari va oldingi proxy (Nginx `client_max_body_size`, Gateway) - ikkalasini muvofiqlashtiring, aks holda foydalanuvchi tushunarsiz 413/502 oladi. `getOriginalFilename()` va `getContentType()` mijozdan keladi - ularga ishonmang: fayl nomini qayta nomlang (UUID), MIME'ni tarkib bo'yicha aniqlang (Apache Tika), zarur bo'lsa antivirus tekshiruvi. Faylni bazaga BLOB sifatida saqlash o'rniga obyekt saqlash + Valet Key (qarang: [17-bo'lim](17-resilience-va-cloud-dizayn-patternlari.md)) orqali to'g'ridan-to'g'ri yuklashni ko'rib chiqing. Vaqtinchalik `location` katalogi konteynerda to'lib ketmasligi uchun diskni kuzating.

## 6.32 Ko'rinish aniqlovchi (View Resolver)

**Tavsif:** Muammo - controller qaysi shablon texnologiyasi (Thymeleaf, FreeMarker, PDF, JSON) ishlatilishini bilmasligi kerak; u faqat mantiqiy view nomini qaytaradi. View Resolver mantiqiy nomni (va lokalni) konkret `View` ob'ektiga aylantiradigan strategiya: bir nechta resolver tartib bilan so'raladi, birinchi topgani g'olib. Shu tufayli shablon dvigatelini almashtirish, lokalga xos view'lar, bean nomi bo'yicha maxsus view'lar va kontent muzokarasi controller'ga tegmasdan amalga oshiriladi. Bu GoF Strategy + Chain of Responsibility'ning taqdimot qatlamidagi kombinatsiyasi.

**Spring'da qayerda uchraydi:** `ViewResolver#resolveViewName(name, locale)` va `View#render(model, request, response)`; amalga oshirishlar - `ThymeleafViewResolver`, `FreeMarkerViewResolver`, `GroovyMarkupViewResolver`, `MustacheViewResolver`, `InternalResourceViewResolver` (JSP), `XsltViewResolver`, `BeanNameViewResolver` (view nomi = bean nomi; PDF/Excel view'lar uchun qulay), `ContentNegotiatingViewResolver` (6.19), `ViewResolverComposite`; `UrlBasedViewResolver` ning `redirect:` va `forward:` prefikslari, `setViewNames`/`setOrder` bilan cheklash va tartib; `WebMvcConfigurer#configureViewResolvers` → `ViewResolverRegistry`; `ModelAndView`, `SmartView` (`isRedirectView`), `RequestToViewNameTranslator`; `AbstractCachingViewResolver` - hal qilingan view'larni keshlaydi. Boot har shablon dvigateli uchun resolver'ni avtomatik sozlaydi (`spring.thymeleaf.*`, `spring.freemarker.*`). WebFlux: reaktiv `ViewResolver`, `ViewResolutionResultHandler`, `Rendering`.

**Qo'llanish keyslari:**
- Thymeleaf HTML sahifalari va `BeanNameViewResolver` orqali `pdfReportView`/`xlsxExportView` ni bir ilovada birga ishlatish.
- Legacy JSP'dan Thymeleaf'ga bosqichma-bosqich ko'chish: ikkala resolver, `setViewNames("legacy/*")` bilan ajratish.
- Mobil va desktop uchun turli shablon papkalarini `User-Agent` yoki tenant bo'yicha tanlovchi shaxsiy `ViewResolver`.
- `redirect:`/`forward:` prefikslari orqali PRG (6.16) va ichki forward'larni view nomi bilan ifodalash.
- Testlarda `MockMvc` + `view().name("orders/list")` bilan controller'ni shablonsiz tekshirish (qarang: [23-bo'lim](23-testing-patternlari.md), @WebMvcTest).

**Ehtiyot bo'ling:** `InternalResourceViewResolver` har doim `View` qaytaradi (mavjudligini tekshirmaydi), shuning uchun zanjirda oxirgi bo'lishi kerak - aks holda keyingi resolver'lar hech qachon so'ralmaydi. Ishlab chiqarishda view keshi (`setCache(true)`, `spring.thymeleaf.cache=true`) yoqilgan bo'lishi shart. Controller'da view yo'lini (`"templates/orders/list.html"`) to'liq yozish resolver g'oyasini buzadi - faqat mantiqiy nom.

## 6.33 Asinxron so'rovlarni qayta ishlash (Async Request Processing - Callable, DeferredResult, StreamingResponseBody)

**Tavsif:** Muammo - sekin tashqi chaqiruv yoki hodisa kutilayotganda servlet konteyner thread'ini band qilish thread pool'ni tez tugatadi va boshqa so'rovlarni to'xtatib qo'yadi. Servlet 3.0 asinxron ishlovi so'rovni konteyner thread'idan ajratadi: so'rov "to'xtatiladi", ish boshqa thread'da yoki hodisa kelganda bajariladi, natija tayyor bo'lganda konteyner javobni yozish uchun so'rovni qayta dispetcherlaydi. Shu asosda uzoq polling, oqimli javoblar va SSE quriladi.

**Spring'da qayerda uchraydi:** Controller qaytish turlari - `Callable<T>` (Spring boshqaradigan `AsyncTaskExecutor` da bajariladi), `WebAsyncTask<T>` (timeout va executor bilan), `DeferredResult<T>` (natija tashqi thread/hodisa tomonidan `setResult` qilinadi), `CompletableFuture<T>`/`CompletionStage<T>`, `ListenableFuture` (deprecated), `StreamingResponseBody` (`OutputStream` ga asinxron yozish), `ResponseBodyEmitter`/`SseEmitter` (6.23); ichki mexanizm - `WebAsyncManager`, `WebAsyncUtils`, `AsyncHandlerInterceptor`, `CallableProcessingInterceptor`, `DeferredResultProcessingInterceptor`; sozlash - `WebMvcConfigurer#configureAsyncSupport` (`AsyncSupportConfigurer#setTaskExecutor`, `setDefaultTimeout`), `spring.mvc.async.request-timeout`; Spring 6.1+ `Callable` uchun aniq `AsyncTaskExecutor` sozlanmagan bo'lsa ogohlantiradi (Boot `applicationTaskExecutor` ni beradi); `spring.threads.virtual.enabled=true` bilan virtual thread'lar (qarang: [4-bo'lim](04-concurrency-patternlari.md), Virtual Threads, Thread Pool). `AsyncRequestTimeoutException` → 503. Reaktiv muqobil - WebFlux (qarang: [19-bo'lim](19-reactive-patternlar.md)); API darajasidagi 202 + status resursi - qarang: [7-bo'lim](07-api-dizayn-patternlari.md) (Asynchronous Request-Reply).

**Qo'llanish keyslari:**
- Uzoq polling (long polling) endpointi: `DeferredResult` hodisa kelganda yoki timeout'da to'ldiriladi.
- Katta fayl/hisobotni `StreamingResponseBody` bilan xotiraga to'liq yuklamasdan oqim sifatida qaytarish.
- Bir nechta sekin downstream chaqiruvni `CompletableFuture.allOf` bilan parallel bajarib, natijani birlashtirish.
- Tashqi to'lov provayderi javobini kutish - konteyner thread'ini band qilmay `DeferredResult` + callback.
- SSE/progress oqimlari (6.23) uchun asosiy infratuzilma.

**Ehtiyot bo'ling:** Asinxron ishlov umumiy ish hajmini kamaytirmaydi - faqat konteyner thread'larini bo'shatadi; agar ish o'zi bloklovchi bo'lsa, boshqa pool to'ladi. Virtual thread'lar (Java 21+) ko'p hollarda `Callable`/`DeferredResult` murakkabligisiz xuddi shu samarani beradi - avval `spring.threads.virtual.enabled` ni baholang. Asinxron dispetcherlashda `ThreadLocal` kontekstlar (Security, MDC, lokal) yo'qoladi - `TaskDecorator` yoki `DelegatingSecurityContextAsyncTaskExecutor` kerak; filtrlar `asyncSupported=true` bo'lishi shart. Timeout'ni belgilamaslik "osilib qolgan" so'rovlarga olib keladi.

## 6.34 Server tomonida renderlash, SPA va gipermedia ilovalar (Server-Side Rendering vs SPA vs Hypermedia-Driven Application)

**Tavsif:** Bu arxitektura tanlovi patterni: foydalanuvchi interfeysi qayerda yig'iladi? SSR - HTML to'liq serverda shablon orqali renderlanadi (Template View), brauzer minimal JS bilan ishlaydi; SPA - server faqat JSON API beradi, interfeys brauzerda JavaScript framework'i tomonidan yig'iladi; HDA (Hypermedia-Driven Application, htmx uslubi) - server HTML fragmentlari qaytaradi, brauzerdagi yengil kutubxona ularni sahifaga joylaydi, holat serverda qoladi. Har biri kechikish, SEO, jamoa ko'nikmalari, autentifikatsiya modeli va murakkablikda turli kelishuvlarni beradi; arxitektor bu tanlovni ongli qilishi kerak.

**Spring'da qayerda uchraydi:** SSR - Spring MVC + Thymeleaf/JTE/FreeMarker (6.11, 6.13), sessiya cookie autentifikatsiyasi; SPA - `@RestController` + statik bundle (6.30) yoki alohida frontend joylashtirish, Spring Security OAuth2/JWT yoki BFF uslubidagi sessiya (qarang: [7-bo'lim](07-api-dizayn-patternlari.md), Backend for Frontend; [18-bo'lim](18-xavfsizlik-patternlari.md), CORS, CSRF); HDA - Thymeleaf fragmentlari (6.8) + htmx, `HX-Request`/`HX-Trigger` header'lari bilan ishlash uchun jamoa kutubxonasi `htmx-spring-boot` (uchinchi tomon, `@HxRequest`); Java'da to'liq komponentli UI - Vaadin Flow (server tomonida holat, WebSocket push) va Hilla (Spring servislari + React); Spring Boot DevTools LiveReload SSR tsiklini tezlashtiradi. Mikro-frontend va fragment kompozitsiyasi - qarang: 12- va 14-bo'limlar.

**Qo'llanish keyslari:**
- Ichki admin/back-office: kichik jamoa, SEO kerak emas, tez yetkazish - SSR yoki HDA (Thymeleaf + htmx).
- Ommaviy mobil + web mijozlar bir API'dan foydalanadi, boy interaktivlik - SPA + REST/GraphQL + BFF.
- Kontent sayti yoki marketing: SEO va birinchi renderlash tezligi hal qiluvchi - SSR, CDN keshlash bilan.
- Murakkab ish stoli uslubidagi korporativ ilova Java jamoasi tomonidan - Vaadin Flow.
- Mavjud SSR ilovaga bosqichma-bosqich interaktivlik qo'shish - htmx fragmentlari, to'liq SPA qayta yozishsiz.

**Ehtiyot bo'ling:** "Hamma SPA qilyapti" degan tanlov ikki jamoa, ikki build, CORS/CSRF/token boshqaruvi va BFF kabi murakkablikni olib keladi - faqat interaktivlik va mijoz xilma-xilligi buni oqlasa tanlang (qarang: [25-bo'lim](25-anti-patternlar.md), Resume-Driven Development). SSR ilovada JSON API'ni "keyinroq qo'shamiz" deyish controller'larni HTML'ga qattiq bog'laydi - servis qatlamini boshidan DTO asosida loyihalang. Vaadin kabi server-holatli UI'lar sessiya xotirasi va sticky session talab qiladi (6.26) - autoscaling rejasiga kiriting.

## 6.35 Amalda qo'llash

- [ ] Controller metodlarining uzunligini o'lchab, 20 qatordan oshganlarini ro'yxatga oling - ularda biznes logika bor.
- [ ] Controller ichidan repository yoki `EntityManager` chaqirilgan joylarni qidirib, har birini servis qatlamiga ko'chirish rejasini yozing.
- [ ] Barcha `Filter` va `HandlerInterceptor` larni tartibi bilan ro'yxatga olib, har birining nega shu tartibda turganini yozib qo'ying.
- [ ] `@ControllerAdvice` borligini va u barcha istisnolarni Problem Details (RFC 9457) formatida qaytarayotganini tasdiqlang.
- [ ] Entity to'g'ridan-to'g'ri HTTP javobida qaytarilgan joylarni toping va har biri uchun DTO yoki projection kiriting.
- [ ] Forma yuborgandan keyin redirect qilinmaydigan POST endpointlarni toping va ularga Post/Redirect/Get qo'llang.
- [ ] Sessiyada saqlanadigan ma'lumotni sanab chiqing va har biri uchun savolga javob yozing: bu stateless deploy'ni buzadimi.
- [ ] Uzoq ishlaydigan so'rovlarni toping va ularni `DeferredResult`, SSE yoki navbatga o'tkazish nomzodi sifatida belgilang.

---

[&larr; 5. Spring Core ichidagi patternlar xaritasi](05-spring-core-ichidagi-patternlar-xaritasi.md) · [Mundarija](README.md) · [7. API dizayn patternlari &rarr;](07-api-dizayn-patternlari.md)
