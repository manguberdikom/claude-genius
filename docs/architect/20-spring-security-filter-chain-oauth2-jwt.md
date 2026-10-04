<!-- doc: architect | chapter: 20 | part: III. Spring chuqur bilim -->

[Kod yozadigan arxitektorning miyyasi](../../README.md) / [Arxitektor miyyasi](README.md)

# 20. Spring Security: filter chain, OAuth2, JWT (Spring Security)

<details>
<summary>Bu bobdagi 13 bo'lim</summary>

- [20.1 `SecurityFilterChain` tuzilishi va filtrlar tartibi](#201-securityfilterchain-tuzilishi-va-filtrlar-tartibi)
- [20.2 Autentifikatsiya va avtorizatsiya: `Authentication`, `SecurityContext`, `GrantedAuthority`](#202-autentifikatsiya-va-avtorizatsiya-authentication-securitycontext-grantedauthority)
- [20.3 Spring Security 6 konfiguratsiyasi: lambda uslubi va eski uslubdan farqi](#203-spring-security-6-konfiguratsiyasi-lambda-uslubi-va-eski-uslubdan-farqi)
- [20.4 Sessiya va token: qachon qaysi biri mantiqli](#204-sessiya-va-token-qachon-qaysi-biri-mantiqli)
- [20.5 OAuth2 rollari: resource server, client, authorization server](#205-oauth2-rollari-resource-server-client-authorization-server)
- [20.6 JWT ni tekshirish: imzo, `iss`, `aud`, `exp`, kalit aylanishi (JWKS)](#206-jwt-ni-tekshirish-imzo-iss-aud-exp-kalit-aylanishi-jwks)
- [20.7 Token muddati, yangilash (refresh) va bekor qilish muammosi](#207-token-muddati-yangilash-refresh-va-bekor-qilish-muammosi)
- [20.8 Metod darajasidagi xavfsizlik: `@PreAuthorize` va uning proxy chegarasi](#208-metod-darajasidagi-xavfsizlik-preauthorize-va-uning-proxy-chegarasi)
- [20.9 Ko'p ijarachi (multi-tenant) va qator darajasidagi kirish nazorati](#209-kop-ijarachi-multi-tenant-va-qator-darajasidagi-kirish-nazorati)
- [20.10 CORS, CSRF va ular qachon kerak](#2010-cors-csrf-va-ular-qachon-kerak)
- [20.11 Parol saqlash, maxfiy ma'lumot va audit izlari](#2011-parol-saqlash-maxfiy-malumot-va-audit-izlari)
- [20.12 Keng tarqalgan xatolar: ochiq qolgan endpoint, tekshirilmagan token, ortiqcha huquq](#2012-keng-tarqalgan-xatolar-ochiq-qolgan-endpoint-tekshirilmagan-token-ortiqcha-huquq)
- [20.13 Amalda qo'llash](#2013-amalda-qollash)

</details>



Spring Security ko'pchilik uchun "sehrli qora quti" bo'lib qoladi: konfiguratsiya ishlaydi, lekin nega ishlaydi degan savolga javob yo'q. Aslida u oddiy servlet filter zanjiri ustiga qurilgan, va deyarli har bir xatolik shu zanjirdagi tartib, SecurityContext ning umri yoki token tekshiruvining to'liq bo'lmagani bilan izohlanadi. Bu bobda to'lov va buyurtma servislari misolida mexanikaga qaraymiz: so'rov qaysi filtrdan o'tadi, JWT qanday tekshiriladi, va arxitektor qayerda qaror qabul qiladi.

## 20.1 `SecurityFilterChain` tuzilishi va filtrlar tartibi

Spring Boot servlet konteynerga bitta `DelegatingFilterProxy` ni ro'yxatdan o'tkazadi, u `springSecurityFilterChain` nomli beanga, ya'ni `FilterChainProxy` ga delegat qiladi. `FilterChainProxy` ichida `SecurityFilterChain` beanlar ro'yxati bor. Har bir so'rov uchun u ro'yxatni yuqoridan pastga aylanib chiqadi va BIRINCHI mos kelgan zanjirni ishlatadi, qolganlarini umuman ko'rmaydi. Shuning uchun `@Order` va `securityMatcher` qiymatlari funksional emas, xavfsizlik qarori hisoblanadi.

Bitta zanjir ichidagi filtrlar tartibi qattiq belgilangan. Amalda muhim ketma-ketlik: `SecurityContextHolderFilter` (kontekstni o'qiydi), `HeaderWriterFilter`, `CorsFilter`, `CsrfFilter`, `LogoutFilter`, keyin autentifikatsiya filtrlari (`BearerTokenAuthenticationFilter`, `UsernamePasswordAuthenticationFilter`, `BasicAuthenticationFilter`), so'ng `AnonymousAuthenticationFilter`, `ExceptionTranslationFilter` va eng oxirida `AuthorizationFilter`. Ikki xulosa chiqadi. Birinchi: CORS preflight CSRF dan oldin ishlanadi, shuning uchun `OPTIONS` so'rovi token talab qilmaydi. Ikkinchi: avtorizatsiya qarori zanjirning OXIRIDA chiqadi, ya'ni undan oldin turgan filtrlar allaqachon ishlab bo'lgan va ular ichida qilingan I/O (masalan foydalanuvchini bazadan o'qish) hali ruxsat tekshirilmagan holda bajarilgan.

`ExceptionTranslationFilter` `AuthorizationFilter` dan oldin turadi, chunki u pastdan ko'tarilgan `AccessDeniedException` ni tutib 401 yoki 403 ga aylantiradi. Agar sizning `@RestControllerAdvice` ingiz 403 ni ushlamayotgan bo'lsa, sabab shu: exception controller ga yetib bormaydi, filtr darajasida hal bo'ladi.

```java
// Ikkita alohida zanjir: API uchun stateless, admin UI uchun sessiyali.
@Bean
@Order(1)
SecurityFilterChain apiChain(HttpSecurity http) throws Exception {
    return http
        .securityMatcher("/api/**")                 // faqat shu prefiks
        .csrf(csrf -> csrf.disable())               // stateless API, cookie ishlatilmaydi
        .sessionManagement(s -> s.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
        .authorizeHttpRequests(a -> a
            .requestMatchers(HttpMethod.GET, "/api/payments/**").hasAuthority("SCOPE_payments.read")
            .requestMatchers(HttpMethod.POST, "/api/payments/**").hasAuthority("SCOPE_payments.write")
            .anyRequest().authenticated())          // oxirgi qoida har doim yopiq
        .oauth2ResourceServer(o -> o.jwt(Customizer.withDefaults()))
        .build();
}

@Bean
@Order(2)
SecurityFilterChain adminChain(HttpSecurity http) throws Exception {
    return http
        .authorizeHttpRequests(a -> a
            .requestMatchers("/login", "/css/**").permitAll()
            .anyRequest().hasRole("ADMIN"))
        .formLogin(Customizer.withDefaults())
        .build();
}
```

## 20.2 Autentifikatsiya va avtorizatsiya: `Authentication`, `SecurityContext`, `GrantedAuthority`

`Authentication` uchta narsani saqlaydi: `getPrincipal()` (kim), `getCredentials()` (nima bilan isbotlandi) va `getAuthorities()` (nimaga haqli). JWT resource server holatida principal `Jwt` obyekti bo'ladi, authority lar esa `scope` yoki `scp` claim idan `JwtGrantedAuthoritiesConverter` tomonidan `SCOPE_` prefiksi bilan yasaladi. Bu yerda birinchi tuzoq: `hasRole("ADMIN")` avtomatik `ROLE_ADMIN` authority ini qidiradi, `hasAuthority("ADMIN")` esa aynan `ADMIN` ni. JWT dagi rollar odatda `realm_access.roles` yoki `roles` claim ida keladi va `ROLE_` prefiksi yo'q, shuning uchun `hasRole` jim turib ishlamaydi.

`SecurityContextHolder` ichida `ThreadLocal` turadi. Demak kontekst so'rovni ishlayotgan thread ga bog'langan. `@Async` metod yoki qo'lda yaratilgan `ExecutorService` ichida kontekst bo'lmaydi, va `@PreAuthorize` u yerda "anonymous" ni ko'radi. Yechim: executor ni `DelegatingSecurityContextExecutorService` bilan o'rash, yoki `SecurityContextHolder.setStrategyName(MODE_INHERITABLETHREADLOCAL)` (lekin pool da qayta ishlatilgan thread da eski kontekst qolib ketishi mumkin, bu xavfli).

```java
// Keycloak uslubidagi rollarni ROLE_ prefiksi bilan authority ga aylantirish.
@Bean
JwtAuthenticationConverter jwtAuthenticationConverter() {
    JwtGrantedAuthoritiesConverter scopes = new JwtGrantedAuthoritiesConverter();
    scopes.setAuthorityPrefix("SCOPE_");
    scopes.setAuthoritiesClaimName("scope");

    JwtAuthenticationConverter converter = new JwtAuthenticationConverter();
    converter.setJwtGrantedAuthoritiesConverter(jwt -> {
        Collection<GrantedAuthority> all = new ArrayList<>(scopes.convert(jwt));
        Map<String, Object> realm = jwt.getClaimAsMap("realm_access");
        if (realm != null && realm.get("roles") instanceof Collection<?> roles) {
            roles.forEach(r -> all.add(new SimpleGrantedAuthority("ROLE_" + r)));
        }
        return all;
    });
    // principal nomi sub emas, preferred_username bo'lsin: audit log uchun qulay
    converter.setPrincipalClaimName("preferred_username");
    return converter;
}
```

## 20.3 Spring Security 6 konfiguratsiyasi: lambda uslubi va eski uslubdan farqi

Spring Security 6 da `WebSecurityConfigurerAdapter` butunlay olib tashlangan, konfiguratsiya faqat `SecurityFilterChain` bean orqali yoziladi. `antMatchers` va `mvcMatchers` o'rniga bitta `requestMatchers` qolgan. `authorizeRequests` o'rniga `authorizeHttpRequests`, u ichkarida `AuthorizationManager` ishlatadi va eski `FilterSecurityInterceptor` emas, `AuthorizationFilter` bilan ishlaydi. Zanjirni yozishda `and()` deprecated, 7.x da esa lambda bo'lmagan uslub umuman yo'q.

Eng ko'p yo'qotish keltiradigan o'zgarish ko'rinmaydigan joyda: `SecurityContextPersistenceFilter` o'rniga `SecurityContextHolderFilter` keldi. Eski filtr har so'rov oxirida kontekstni sessiyaga AVTOMATIK saqlar edi, yangisi saqlamaydi. Agar siz o'z filtringizda `SecurityContextHolder.getContext().setAuthentication(...)` qilib qo'ysangiz, Spring Security 6 da bu sessiyada qolmaydi va keyingi so'rov yana anonim bo'ladi. To'g'ri yo'li: `SecurityContextRepository` ga ochiq yozish.

```java
// Spring Security 6: kontekstni sessiyaga saqlash endi QO'LDA bo'ladi.
public class OtpVerificationFilter extends OncePerRequestFilter {

    private final SecurityContextRepository repository =
            new HttpSessionSecurityContextRepository();

    @Override
    protected void doFilterInternal(HttpServletRequest req, HttpServletResponse res,
                                    FilterChain chain) throws ServletException, IOException {
        Authentication auth = verifyOtp(req);          // ikkinchi faktor tekshirildi
        if (auth != null) {
            SecurityContext ctx = SecurityContextHolder.createEmptyContext();
            ctx.setAuthentication(auth);
            SecurityContextHolder.setContext(ctx);
            repository.saveContext(ctx, req, res);     // bu qator bo'lmasa kontekst yo'qoladi
        }
        chain.doFilter(req, res);
    }
}
```

## 20.4 Sessiya va token: qachon qaysi biri mantiqli

Sessiya serverda holat saqlaydi, demak logout va bekor qilish darhol ishlaydi, lekin horizontal skalalashda yopishqoq (sticky) sessiya yoki Spring Session orqali Redis/JDBC ga ko'chirish kerak bo'ladi. Token, xususan JWT, holatsiz: tekshirish uchun bazaga borish shart emas, lekin chiqarilgan tokenni muddatidan oldin to'xtatish deyarli imkonsiz. Qaror oddiy mezonga tayanadi: agar bir brauzer ichida ishlaydigan ichki admin paneli bo'lsa, sessiya arzonroq va xavfsizroq. Agar mobil ilova, SPA va servis orasidagi chaqiruvlar bo'lsa, token kerak.

Amalda eng barqaror kombinatsiya: brauzer uchun `HttpOnly`, `Secure`, `SameSite=Lax` cookie dagi sessiya yoki opaque token, servislar orasida esa JWT. Oraliq variant: BFF (backend for frontend) sessiyani ushlab turadi va downstream ga JWT uzatadi, shunda JavaScript tokenni hech qachon ko'rmaydi. Sessiya hajmi uchun raqam: bitta oddiy autentifikatsiyalangan sessiya taxminan 2 dan 10 KB gacha joy oladi, 50 ming parallel foydalanuvchi Redis da taxminan 100 dan 500 MB gacha degani.

## 20.5 OAuth2 rollari: resource server, client, authorization server

Uchta rol uchta mutlaqo boshqa starter va boshqa mas'uliyat. Resource server kiruvchi tokenni TEKSHIRADI va hech qachon chiqarmaydi: `spring-boot-starter-oauth2-resource-server`. Client foydalanuvchi nomidan token OLADI va downstream chaqiruvga qo'yadi: `spring-boot-starter-oauth2-client`, ichida `OAuth2AuthorizedClientManager`. Authorization server tokenni CHIQARADI: alohida `spring-authorization-server` proyekti, va uni o'z qo'lingiz bilan yozishga urinish deyarli har doim xato qaror.

Arxitektor eng ko'p xato qiladigan joy: buyurtma servisi ham API ni himoyalaydi, ham to'lov servisiga chaqiruv qiladi. Bu bitta ilovada resource server va client rollarining birgaligi. Ikkisi bir zanjirda yashashi mumkin, lekin token olish uchun `client_credentials` grant kerak, foydalanuvchi tokenini shunchaki uzatish (token passthrough) esa audience ni buzadi.

```yaml
# Buyurtma servisi: ham resource server (kiruvchi), ham client (chiquvchi).
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: https://id.example.com/realms/orders
          # jwk-set-uri ni ko'rsatmasak, issuer metadata dan topiladi
          audiences: orders-api          # aud tekshiruvi YOQILADI
      client:
        registration:
          payments:
            provider: internal-idp
            client-id: orders-service
            client-secret: ${ORDERS_CLIENT_SECRET}
            authorization-grant-type: client_credentials
            scope: payments.write
        provider:
          internal-idp:
            token-uri: https://id.example.com/realms/orders/protocol/openid-connect/token
```

## 20.6 JWT ni tekshirish: imzo, `iss`, `aud`, `exp`, kalit aylanishi (JWKS)

`NimbusJwtDecoder` ishi ikki qadamdan iborat: avval imzoni tekshiradi, keyin `OAuth2TokenValidator` zanjirini ishlatadi. `JwtDecoders.fromIssuerLocation(...)` ishlatilganda standart validator `JwtTimestampValidator` (`exp` va `nbf`, standart clock skew taxminan 60 sekund) va `JwtIssuerValidator` dan iborat. Diqqat qiling: `aud` AVTOMATIK tekshirilmaydi. Agar siz uni qo'shmasangiz, bitta IdP dan olingan va boshqa servis uchun chiqarilgan token sizning API ga ham kiradi. Bu real audit topilmasi, nafaqat nazariya.

Kalit aylanishi (rotation) JWKS orqali ishlaydi. Decoder `jwk-set-uri` ni o'qiydi va natijani cache qiladi (Nimbus da standart TTL taxminan 5 daqiqa, oldindan yangilash bilan). Noma'lum `kid` kelganda JWKS qayta o'qiladi, lekin bu masofaviy HTTP chaqiruv: IdP javob bermasa, butun API 401 qaytara boshlaydi. Shuning uchun JWKS endpoint ga timeout (connect taxminan 2 sekund, read taxminan 3 sekund) va retry qo'yish kerak, hamda IdP ni mavjudlik nuqtai nazaridan kritik bog'liqlik deb hisoblash kerak.

```java
// aud va iss ni ochiq tekshirish, qo'shimcha claim bilan.
@Bean
JwtDecoder jwtDecoder(@Value("${idp.issuer}") String issuer) {
    NimbusJwtDecoder decoder = JwtDecoders.fromIssuerLocation(issuer);

    OAuth2TokenValidator<Jwt> audience = new JwtClaimValidator<List<String>>(
            JwtClaimNames.AUD,
            aud -> aud != null && aud.contains("payments-api"));

    // to'lov servisi faqat kuchli autentifikatsiyadan o'tgan tokenni qabul qiladi
    OAuth2TokenValidator<Jwt> acr = new JwtClaimValidator<String>(
            "acr", v -> "mfa".equals(v));

    decoder.setJwtValidator(new DelegatingOAuth2TokenValidator<>(
            JwtValidators.createDefaultWithIssuer(issuer), audience, acr));
    return decoder;
}
```

| Tuzoq | Nima sodir bo'ladi | Yechim |
|---|---|---|
| `aud` tekshirilmagan | Boshqa servis uchun chiqarilgan token qabul qilinadi | `audiences` property yoki `JwtClaimValidator` |
| `alg: none` yoki tokenni qo'lda parse qilish | Imzosiz token ishonchli deb qabul qilinadi | Faqat `JwtDecoder`, hech qachon qo'lda base64 decode emas |
| JWKS cache ga timeout yo'q | IdP sekinlashsa butun API bloklanadi | Connect/read timeout va circuit breaker |
| `exp` ga ortiqcha clock skew | Muddati o'tgan token yana ishlaydi | Skew ni taxminan 30 sekundda ushlab turish, NTP sozlash |
| Scope va rol aralashtirilgan | `hasRole` jim turib ishlamaydi | Authority prefikslarini bitta konvensiyaga keltirish |
| Har zanjirda alohida `JwtDecoder` | Validator qoidalari bo'linib ketadi | Bitta `JwtDecoder` bean, zanjirlarga inject qilish |
| Token ichida ko'p ma'lumot | Header 8 KB limitiga uriladi, proxy 431 qaytaradi | Faqat `sub`, `scope`, `tenant` kabi minimal claim lar |

## 20.7 Token muddati, yangilash (refresh) va bekor qilish muammosi

JWT ni bekor qilish mumkin emas, bu uning dizayni. Demak qaror savol qo'yilishi bilan boshlanadi: "foydalanuvchi huquqi olingandan keyin qancha vaqt eski huquq bilan ishlashi mumkin?" Javob access token TTL ini belgilaydi. Ichki servislar uchun taxminan 5 dan 15 daqiqa, to'lov yoki admin amallari uchun taxminan 2 dan 5 daqiqa oqilona. Refresh token uzoqroq yashaydi (taxminan 8 soatdan 30 kungacha) va u IdP tomonida saqlanadi, demak uni bekor qilish mumkin.

Darhol bekor qilish kerak bo'lsa uch yo'l bor. Birinchi: opaque token va `OpaqueTokenIntrospector` (RFC 7662), har so'rov IdP ga boradi, latency taxminan 5 dan 30 ms oshadi, lekin introspection natijasini 10 dan 30 sekundga cache qilish kelishuvni yumshatadi. Ikkinchi: `jti` bo'yicha denylist, Redis da token TTL muddatiga teng yashaydi, xotira kichik. Uchinchi: foydalanuvchi uchun `tokensValidAfter` vaqt belgisi, token `iat` undan oldin bo'lsa rad etiladi, bu "barcha qurilmalardan chiqish" funksiyasiga aynan to'g'ri keladi.

## 20.8 Metod darajasidagi xavfsizlik: `@PreAuthorize` va uning proxy chegarasi

`@EnableMethodSecurity` AOP proxy orqali ishlaydi. Shundan kelib chiqadigan chegaralar aniq. Birinchi: o'z-o'ziga chaqiruv (self-invocation) tekshiruvdan o'tmaydi, chunki chaqiruv proxy dan emas, `this` dan ketadi. Ikkinchi: `private` va `final` metod JDK dinamik proxy yoki CGLIB da ushlanmaydi. Uchinchi: faqat Spring bean ichidagi metodlar himoyalanadi, `new` bilan yaratilgan obyekt ustida annotatsiya hech narsa qilmaydi.

Tartib ham muhim. Metod xavfsizligi advice i tranzaksiya advice idan oldin ishlashi kerak, aks holda ruxsatsiz chaqiruv uchun ham tranzaksiya ochiladi. Standart tartibda shunday, lekin o'z `@Aspect` ingizga `@Order` qo'yganda buzilishi mumkin. `@PostAuthorize` esa alohida tuzoq: metod allaqachon bajarilgan, demak yon effekt sodir bo'lgan, faqat natija qaytarilmaydi. Yozish amallarida `@PostAuthorize` ishlatmaslik kerak.

```java
@Service
public class PaymentService {

    @PreAuthorize("hasAuthority('SCOPE_payments.write') and #cmd.amount <= 1000000")
    public PaymentId create(CreatePayment cmd) {
        return store(cmd);
    }

    // TUZOQ: bu chaqiruv proxy dan o'tmaydi, @PreAuthorize ishlamaydi
    public void createBatch(List<CreatePayment> cmds) {
        cmds.forEach(this::create);
    }

    // natijani filtrlash: faqat o'z filiali hisobotlari qoladi
    @PostFilter("filterObject.branchId == authentication.name")
    public List<Report> reports() { return allReports(); }
}
```

`@PostFilter` ro'yxatni xotirada filtrlaydi. 100 ming qatorni bazadan olib keyin 12 tasini qoldirish arxitektura xatosi. Filtrlash `WHERE` ga tushishi kerak.

## 20.9 Ko'p ijarachi (multi-tenant) va qator darajasidagi kirish nazorati

Bir nechta issuer bo'lsa, `JwtIssuerAuthenticationManagerResolver` har token uchun `iss` ga qarab mos `AuthenticationManager` ni tanlaydi va har biri o'z JWKS ini ishlatadi. Ro'yxat qattiq belgilangan bo'lishi shart, aks holda hujumchi o'z issuer ini ko'rsatib o'z tokenini yasaydi.

Qator darajasidagi nazorat uchun ikki yo'l bor. Birinchi: har `WHERE` ga `tenant_id` qo'shish, bu bitta esdan chiqqan query da sizib chiqishni beradi. Ikkinchi: PostgreSQL Row Level Security, tekshiruv bazada qoladi va ilova xatosiga bog'liq bo'lmaydi.

```sql
-- Ijarachi bo'yicha izolyatsiya bazada, ilovada emas.
ALTER TABLE payments ENABLE ROW LEVEL SECURITY;
ALTER TABLE payments FORCE ROW LEVEL SECURITY;  -- jadval egasiga ham tegsin

CREATE POLICY payments_tenant_isolation ON payments
  USING (tenant_id = current_setting('app.tenant_id', true)::uuid);

-- Har tranzaksiya boshida, pool dagi connection ga yopishib qolmasligi uchun LOCAL
SET LOCAL app.tenant_id = '9f1c...';
```

`SET LOCAL` tanlovi qasddan: u tranzaksiya oxirida avtomatik bekor bo'ladi. `SET` (LOCAL siz) ishlatilsa qiymat connection da qoladi va HikariCP uni keyingi foydalanuvchiga beradi, bu esa to'g'ridan to'g'ri ma'lumot sizishi. `current_setting('app.tenant_id', true)` dagi `true` sozlama yo'q bo'lsa `NULL` qaytaradi, `NULL = tenant_id` esa hech qanday qator bermaydi, ya'ni xato holatda tizim yopiq bo'ladi. Bu "fail closed" xatti-harakati, aynan shu kerak.

## 20.10 CORS, CSRF va ular qachon kerak

CSRF faqat brauzer so'rovga avtomatik credential (cookie yoki basic auth) qo'shadigan holatda kerak. `Authorization: Bearer` header ni brauzer o'zi qo'shmaydi, demak to'liq stateless JWT API da CSRF himoyasi ma'nosiz. Lekin tokenni cookie da saqlasangiz, CSRF yana kerak bo'ladi. Ko'pchilik `csrf().disable()` ni cookie sessiyali ilovada ham yozib qo'yadi, bu esa ochiq teshik.

CORS Spring Security da `CorsFilter` orqali ishlaydi va u CSRF dan oldin turadi. Ikki qoida esda tursin: `allowCredentials(true)` bilan `allowedOrigins("*")` birga ishlamaydi, `allowedOriginPatterns` kerak bo'ladi. Ikkinchisi: CORS brauzer himoyasi, server himoyasi emas, `curl` uni e'tiborsiz qoldiradi.

```java
@Bean
CorsConfigurationSource corsConfigurationSource() {
    CorsConfiguration cfg = new CorsConfiguration();
    cfg.setAllowedOriginPatterns(List.of("https://*.example.com"));  // * emas
    cfg.setAllowedMethods(List.of("GET", "POST", "PUT", "DELETE"));
    cfg.setAllowedHeaders(List.of("Authorization", "Content-Type"));
    cfg.setAllowCredentials(true);
    cfg.setMaxAge(1800L);   // preflight natijasi 30 daqiqa cache lanadi
    UrlBasedCorsConfigurationSource src = new UrlBasedCorsConfigurationSource();
    src.registerCorsConfiguration("/api/**", cfg);
    return src;
}
```

## 20.11 Parol saqlash, maxfiy ma'lumot va audit izlari

`DelegatingPasswordEncoder` (ya'ni `PasswordEncoderFactories.createDelegatingPasswordEncoder()`) hash ni `{bcrypt}$2a$10$...` ko'rinishida saqlaydi. Prefiks tufayli algoritmni migratsiyasiz almashtirish mumkin: yangi parollar `{argon2}` bilan yoziladi, eskilari hali `{bcrypt}` bilan tekshiriladi. BCrypt strength 10 taxminan 50 dan 100 ms gacha hisoblanadi, 12 esa taxminan 200 dan 400 ms. Bu login endpoint ning throughput ini to'g'ridan to'g'ri cheklaydi, demak brute force dan himoya bo'lib ham xizmat qiladi. BCrypt kiruvchi parolni 72 baytdan keyin kesib tashlaydi, uzun passphrase lar uchun Argon2 to'g'riroq tanlov.

Audit izi uchun `AuditorAware` ni `SecurityContextHolder` ga bog'lash eng qisqa yo'l. Lekin bu `@Async` va batch job larda bo'sh qaytadi, shuning uchun tizim foydalanuvchisi uchun zaxira qiymat kerak. Audit yozuvi hech qachon `Authentication#getCredentials()` ni, token ni yoki parolni saqlamasligi kerak. Log da token ko'rinib qolishi eng ko'p takrorlanadigan sizish kanali, odatda `DEBUG` darajadagi HTTP client logger orqali.

```java
@Bean
AuditorAware<String> auditorAware() {
    return () -> Optional.ofNullable(SecurityContextHolder.getContext().getAuthentication())
            .filter(Authentication::isAuthenticated)
            .map(Authentication::getName)
            .filter(name -> !"anonymousUser".equals(name))
            .or(() -> Optional.of("system"));   // batch job uchun zaxira
}
```

## 20.12 Keng tarqalgan xatolar: ochiq qolgan endpoint, tekshirilmagan token, ortiqcha huquq

Ochiq qolgan endpoint deyarli har doim `requestMatchers` tartibidan kelib chiqadi: birinchi mos kelgan qoida ishlaydi, shuning uchun `anyRequest().permitAll()` ni yuqoriga qo'yish keyingi qoidalarni o'ldiradi. Ikkinchi manba: `/actuator/**` uchun alohida zanjir yozilib, unda autentifikatsiya qo'yilmagani. `/actuator/env` va `/actuator/heapdump` maxfiy ma'lumot beradi, ularni ochiq qoldirish kritik xato. Uchinchi manba: `/api/v2/**` qo'shilgan, lekin konfiguratsiyada faqat `/api/v1/**` bor.

```bash
# Chiqishdan oldin minimal tekshiruv: tokensiz qancha endpoint javob beradi?
BASE=https://orders.example.com
for p in /api/payments /api/orders /actuator /actuator/env /actuator/heapdump \
         /api/v2/orders /swagger-ui/index.html /v3/api-docs; do
  code=$(curl -s -o /dev/null -w '%{http_code}' "$BASE$p")
  echo "$code $p"       # 401 yoki 403 kutiladi, 200 bo'lsa darhol tekshir
done
```

| Mezon | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Zanjir soni | Bitta `SecurityFilterChain` hamma yo'l uchun | Yo'l bo'yicha ajratilgan zanjirlar, `securityMatcher` bilan |
| Standart qoida | `permitAll` dan boshlash, keyin yopish | `anyRequest().authenticated()` dan boshlash, keyin ochish |
| JWT tekshiruvi | `issuer-uri` yozib qo'yish bilan cheklanish | `iss`, `aud`, `exp`, `acr` ni ochiq validator bilan tekshirish |
| Authority | String rol nomlari kodga sochilgan | Konstanta va bitta prefiks konvensiyasi, scope va rol ajratilgan |
| Token umri | 24 soatlik access token, qulay bo'lgani uchun | 5 dan 15 daqiqa, refresh rotation va `jti` denylist |
| Bekor qilish | "JWT ni bekor qilib bo'lmaydi" deb qo'yib yuborish | `tokensValidAfter` yoki introspection, SLA raqami bilan |
| Ijarachi izolyatsiyasi | Har `WHERE` ga `tenant_id` qo'lda qo'shish | PostgreSQL RLS, `SET LOCAL` va fail closed xatti-harakat |
| CSRF | Hamma joyda `disable()` | Cookie sessiyali zanjirda yoqilgan, stateless zanjirda o'chirilgan |
| Metod xavfsizligi | `@PostFilter` bilan xotirada filtrlash | Filtrni `WHERE` ga tushirish, `@PreAuthorize` ni chegarada ishlatish |
| Nazorat | Konfiguratsiyani ko'z bilan o'qish | Avtomatlashtirilgan tekshiruv, [testlash qo'llanmasidagi](../testing/README.md) xavfsizlik testlari bo'limi |

Ortiqcha huquq eng sekin seziladigan xato. Odatda `SCOPE_orders.read` yetarli bo'lgan joyda `ROLE_ADMIN` talab qilinadi, chunki shunday yozish osonroq. Natijada har servis admin huquqi bilan ishlaydi va bitta buzilgan servis butun tizimni ochadi. Minimal scope ni yozib chiqish zerikarli ish, lekin uni qilmaslik narxi incident paytida bilinadi.

## 20.13 Amalda qo'llash

- [ ] Barcha `SecurityFilterChain` beanlarni ro'yxatga oling, `@Order` va `securityMatcher` qiymatlarini yozib, har bir yo'l qaysi zanjirga tushishini jadvalda tasdiqlang.
- [ ] Har bir zanjirda oxirgi qoida `anyRequest().authenticated()` yoki undan qattiqroq ekanini tekshiring, `permitAll` ni faqat aniq ro'yxat uchun qoldiring.
- [ ] `JwtDecoder` ga `aud` validatorini qo'shing yoki `spring.security.oauth2.resourceserver.jwt.audiences` ni to'ldiring, so'ng boshqa audience li token bilan 401 kelishini tasdiqlang.
- [ ] JWKS chaqiruviga connect taxminan 2 sekund va read taxminan 3 sekund timeout o'rnatib, IdP ni mavjudlik bog'liqligi sifatida monitoringga qo'shing.
- [ ] Access token TTL ini 15 daqiqadan oshmaydigan qilib kelishib oling va huquq olingandan keyin eski token qancha yashashini SLA sifatida hujjatlashtiring.
- [ ] `@Async` va batch kodda `DelegatingSecurityContextExecutorService` ishlatilayotganini tekshiring, aks holda `@PreAuthorize` va audit nomlari bo'sh qoladi.
- [ ] Ko'p ijarachi jadvallarda RLS ni yoqib, `SET LOCAL` ishlatilayotganini va sozlama yo'q holatda hech qanday qator qaytmasligini tekshiring.
- [ ] Chiqishdan oldin tokensiz `curl` skriptini CI ga qo'shib, `/actuator/env`, `/actuator/heapdump` va yangi versiya prefikslarini har deploy da sinab turing.

---

[&larr; 19. Spring tranzaksiyalari va ularning chegaralari](19-spring-tranzaksiyalari-va-ularning.md) · [Mundarija](README.md) · [21. PostgreSQL arxitekturasi: process model, WAL, checkpoint, vacuum &rarr;](21-postgresql-arxitekturasi-process-model-wal.md)
