<!-- doc: architect | chapter: 20 | part: III. Spring chuqur bilim -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 20. Spring Security: filter chain, OAuth2, JWT (Spring Security)

<details>
<summary>Bu bobdagi 19 bo'lim</summary>

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
- [20.13 Request matcher tuzog'i: Ant va MVC, `*` va `**`, regex](#2013-request-matcher-tuzogi-ant-va-mvc--va--regex)
- [20.14 JWT imzo kaliti: simmetrik, assimmetrik, JWS va JWE](#2014-jwt-imzo-kaliti-simmetrik-assimmetrik-jws-va-jwe)
- [20.15 HTTP Basic: har so'rovda credential, `realmName` va xato javobi](#2015-http-basic-har-sorovda-credential-realmname-va-xato-javobi)
- [20.16 Form login: maxsus sahifa, handler lar va HTTP Basic bilan birga](#2016-form-login-maxsus-sahifa-handler-lar-va-http-basic-bilan-birga)
- [20.17 Xavfsizlikning besh funksiyasi: faqat himoya emas](#2017-xavfsizlikning-besh-funksiyasi-faqat-himoya-emas)
- [20.18 Avtorizatsiya qarori qayerda turadi: gateway da qo'pol, servis ichida ingichka](#2018-avtorizatsiya-qarori-qayerda-turadi-gateway-da-qopol-servis-ichida-ingichka)
- [20.19 Amalda qo'llash](#2019-amalda-qollash)

</details>



Spring Security ko'pchilik uchun "sehrli qora quti" bo'lib qoladi: konfiguratsiya ishlaydi, lekin nega ishlaydi degan savolga javob yo'q. Aslida u oddiy servlet filter zanjiri ustiga qurilgan, va deyarli har bir xatolik shu zanjirdagi tartib, SecurityContext ning umri yoki token tekshiruvining to'liq bo'lmagani bilan izohlanadi. Bu bobda to'lov va buyurtma servislari misolida mexanikaga qaraymiz: so'rov qaysi filtrdan o'tadi, JWT qanday tekshiriladi, va arxitektor qayerda qaror qabul qiladi.

## 20.1 `SecurityFilterChain` tuzilishi va filtrlar tartibi

Spring Boot servlet konteynerga bitta `DelegatingFilterProxy` ni ro'yxatdan o'tkazadi, u `springSecurityFilterChain` nomli beanga, ya'ni `FilterChainProxy` ga delegat qiladi. `FilterChainProxy` ichida `SecurityFilterChain` beanlar ro'yxati bor. Har bir so'rov uchun u ro'yxatni yuqoridan pastga aylanib chiqadi va BIRINCHI mos kelgan zanjirni ishlatadi, qolganlarini umuman ko'rmaydi. Shuning uchun `@Order` va `securityMatcher` qiymatlari funksional emas, xavfsizlik qarori hisoblanadi.

Bitta zanjir ichidagi filtrlar tartibi qattiq belgilangan. Amalda muhim ketma-ketlik: `SecurityContextHolderFilter` (kontekstni o'qiydi), `HeaderWriterFilter`, `CorsFilter`, `CsrfFilter`, `LogoutFilter`, keyin autentifikatsiya filtrlari (`BearerTokenAuthenticationFilter`, `UsernamePasswordAuthenticationFilter`, `BasicAuthenticationFilter`), so'ng `AnonymousAuthenticationFilter`, `ExceptionTranslationFilter` va eng oxirida `AuthorizationFilter`. Ikki xulosa chiqadi. Birinchi: CORS preflight CSRF dan oldin ishlanadi, shuning uchun `OPTIONS` so'rovi token talab qilmaydi. Ikkinchi: avtorizatsiya qarori zanjirning OXIRIDA chiqadi, ya'ni undan oldin turgan filtrlar allaqachon ishlab bo'lgan va ular ichida qilingan I/O (masalan foydalanuvchini bazadan o'qish) hali ruxsat tekshirilmagan holda bajarilgan.

`ExceptionTranslationFilter` `AuthorizationFilter` dan oldin turadi, chunki u pastdan ko'tarilgan `AccessDeniedException` ni tutib 401 yoki 403 ga aylantiradi. Agar sizning `@RestControllerAdvice` ingiz 403 ni ushlamayotgan bo'lsa, sabab shu: exception controller ga yetib bormaydi, filtr darajasida hal bo'ladi.

Zanjirdagi tartib qat'iy deganda framework o'z filtrlariga bergan pozitsiya raqamlari tushuniladi: kitob ularni `CorsFilter` 100, `CsrfFilter` 200, `BasicAuthenticationFilter` 300 ko'rinishida ko'rsatadi va o'z filtringizni shu raqamlarga nisbatan oldin, keyin yoki aynan o'sha pozitsiyada qo'yish mumkin (Spilca, 9-bob, 199-bet). Shundan ikki amaliy qoida chiqadi. Birinchi: bitta pozitsiyaga ikki filtr qo'yilsa, ular qaysi tartibda chaqirilishi ANIQLANMAGAN, demak `addFilterAt` bilan qo'yilgan ikki filtrning bir-biriga bog'liqligiga tayanib bo'lmaydi. Ikkinchi: framework filtr har so'rovda faqat bir marta chaqirilishini kafolatlamaydi, shuning uchun log yozadigan yoki hisoblagichni oshiradigan filtr `OncePerRequestFilter` dan meros oladi (Spilca, 9-bob, 210-bet).

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

Konfiguratsiya USLUBI bilan birga uning TUZILISHI ham qaror. Bitta katta security konfiguratsiya sinfi tez o'sadi, shuning uchun mas'uliyatni ajratish kerak: foydalanuvchi va parol boshqaruvi (`UserDetailsService`, `PasswordEncoder`) bir sinfda, web avtorizatsiya (`HttpSecurity` va `SecurityFilterChain`) boshqa sinfda (Spilca, 2-bob, 56-57-bet). Bu ko'p `SecurityFilterChain` bean yozish bilan adashtirilmasin: zanjirlar SO'ROVLARNI ajratadi ([20.1](#201-securityfilterchain-tuzilishi-va-filtrlar-tartibi)), bu yerda esa konfiguratsiya ajratiladi. Teskari holat ham bor: ilovada foydalanuvchi tushunchasi umuman bo'lmasa (masalan faqat statik API kalitini tekshiradigan filtr), Boot baribir standart `UserDetailsService` ni avtomatik sozlaydi va konsolga parol chiqaradi; buni `@SpringBootApplication(exclude = UserDetailsServiceAutoConfiguration.class)` bilan o'chirish kerak, aks holda hech kim ishlatmaydigan, lekin mavjud bo'lgan foydalanuvchi qolib ketadi (Spilca, 9-bob, 210-bet).

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

Jadvaldagi oxirgi ikki qator uchun Newman amaliy yo'l beradi va ular JWT ning uchta qiyinchiligi sifatida sanalgan (11-bob, "Challenges").

**Ochiq kalitni yetkazish va almashtirish.** Imzolangan tokenni tekshirish uchun qabul qiluvchi tomonga kanal tashqarisidan ma'lumot, odatda ochiq kalit, yetib borishi kerak, ya'ni kalitni boshqarishning hamma muammosi shu yerda paydo bo'ladi: mikroservis ochiq kalitni qanday oladi va kalit almashishi kerak bo'lsa nima bo'ladi. Kitob Vault ni misol qiladi, chunki u kalitni olish va aylanishini qo'llab-quvvatlaydi va taqsimlangan muhit uchun loyihalangan. Ochiq kalitni konfiguratsiya fayliga qattiq yozish mumkin, lekin keyin kalit o'zgarishi muammosi qoladi. Spring da bu muammoning standart yechimi JWKS endpoint i va yuqoridagi `JwtDecoder` sozlamasi, lekin JWKS ga ulanish ham tashqi bog'liqlik, shuning uchun jadvaldagi timeout va circuit breaker qatori bilan birga ishlaydi.

**Uzoq asinxron jarayon uchun token muddati.** Mijoz buyurtma bergandan keyin boshlanadigan asinxron jarayonlar zanjiri (to'lovni olish, xabar yuborish, yig'ish va jo'natish) soatlar yoki kunlar davom etishi mumkin va mijozning keyingi aralashuvi bo'lmaydi. Savol shunda: shu muddatga teng amal qilish davri bo'lgan token yasash kerakmi. Kitob savolni ochiq qoldiradi, lekin uni to'g'ri qo'yadi: qaysi nuqtada uzoq muddatli token tokensiz ishlashdan ko'proq muammo bo'ladi. Amalda ko'rilgan ikki yo'l: faqat shu kontekstda ishlaydigan, doirasi cheklangan alohida uzoq muddatli token yasash, yoki oqimning ma'lum nuqtasidan keyin tokendan umuman voz kechish.

**Token juda kattalashsa.** Kamdan kam, lekin uchraydi: tokenga shunchalik ko'p ma'lumot kerak bo'lib qoladi, token hajmining o'zi muammoga aylanadi. Newman ning mijozi musiqa huquqlarini boshqarish domenida bitta trek uchun tokenda 10 minggacha yozuv kerak bo'lishi mumkinligini hisoblab chiqqan. Yechim esa butun tizimni emas, bitta holatni ajratishdan chiqdi: tizimning asosiy qismi kam maydonli oddiy token bilan ishlay oladi, shuning uchun murakkab huquq avtorizatsiyasi boshqacha hal qilindi, ya'ni JWT dastlabki "oddiy" avtorizatsiya uchun ishlatildi, qo'shimcha maydonlar esa kerak bo'lganda ma'lumotlar omboridan qidirib olindi. Bu jadvaldagi "faqat minimal claim lar" qatorining amaliy shakli: tokenga nima sig'masa, u avtorizatsiya qaroriga kirish kaliti bo'ladi, qarorning o'zi emas.
## 20.7 Token muddati, yangilash (refresh) va bekor qilish muammosi

JWT ni bekor qilish mumkin emas, bu uning dizayni. Demak qaror savol qo'yilishi bilan boshlanadi: "foydalanuvchi huquqi olingandan keyin qancha vaqt eski huquq bilan ishlashi mumkin?" Javob access token TTL ini belgilaydi. Ichki servislar uchun taxminan 5 dan 15 daqiqa, to'lov yoki admin amallari uchun taxminan 2 dan 5 daqiqa oqilona. Refresh token uzoqroq yashaydi (taxminan 8 soatdan 30 kungacha) va u IdP tomonida saqlanadi, demak uni bekor qilish mumkin.

Darhol bekor qilish kerak bo'lsa uch yo'l bor. Birinchi: opaque token va `OpaqueTokenIntrospector` (RFC 7662), har so'rov IdP ga boradi, latency taxminan 5 dan 30 ms oshadi, lekin introspection natijasini 10 dan 30 sekundga cache qilish kelishuvni yumshatadi. Ikkinchi: `jti` bo'yicha denylist, Redis da token TTL muddatiga teng yashaydi, xotira kichik. Uchinchi: foydalanuvchi uchun `tokensValidAfter` vaqt belgisi, token `iat` undan oldin bo'lsa rad etiladi, bu "barcha qurilmalardan chiqish" funksiyasiga aynan to'g'ri keladi.

Bekor qilish nega shuncha muhim ekanini hujum nomi bilan aytish qulay. Kitob OAuth 2 ning zaif nuqtalarini sanaganda to'rtta nomni beradi: klientdagi CSRF, klient credential ini o'g'irlash, token replay va token hijacking (Spilca, 12-bob, 299-bet). Replay eng oddiysi: token tarmoqda sarlavha sifatida ketadi va ushlab olinsa, hujumchi uni xohlagancha qayta ishlatadi, xuddi yo'qolgan uy kaliti bilan eshikni necha marta xohlasa ochish mumkin bo'lgani kabi. Token muddati va bekor qilish mexanizmi aynan shu replay oynasini qisqartirish uchun bor. Refresh token ham xuddi shu nishon: u ushlab olinsa, undan yangi access token olinadi, shuning uchun refresh token rotation va uni bir marta ishlatish qoidasi majburiy.

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

Parol hash lanishidan oldin xotirada qancha turishi ham qaror. `String` o'zgarmas va u GC ga qolguncha heap da yashaydi, demak heap dump parolni oshkor qiladi; shu sababli standart kutubxona parol o'qishni `char[]` bilan beradi va uning massivi ishlatilgandan keyin nolga to'ldirilishi kerak (Herbert Schildt, *Java The Complete Reference*, 12-nashr, McGraw-Hill, 2022, 22-bob, 753-bet). Qoida CLI va batch ilovasida amaliy qiymat beradi, chunki web oqimida parol allaqachon HTTP tanasida `String` bo'lib keladi va u yerda bu himoya ishlamaydi.

```java
// CLI yoki batch: parol xotirada qolmasligi uchun massiv tozalanadi
Console console = System.console();
char[] password = console.readPassword("Parol: ");
try {
    if (!encoder.matches(CharBuffer.wrap(password), storedHash)) {
        throw new BadCredentialsException("parol mos kelmadi");
    }
} finally {
    Arrays.fill(password, '\0');   // `String` da bu imkoniyat yo'q
}
```

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

Avval umumiy sababni aytish kerak, chunki u ro'yxatdagi har bir xatodan oldin turadi: Spring Security ilovani o'zi himoyalamaydi. Kitob buni ochiq yozadi, u sehrli panatseya emas va zaiflik yo'qligini kafolatlamaydi; dasturchi uni ilovaning talabiga qarab sozlashi va moslashtirishi shart (Spilca, 1-bob, 5-bet). Kitobning o'xshatishi qisqa: signalizatsiyani o'rnatganda uni derazalarga ham ulash sizning ishingiz, va derazadan kirilganda signalizatsiya ishlamagani uning aybi emas (Spilca, 1-bob, 6-bet). Review uchun amaliy xulosa: classpath da `spring-boot-starter-security` turgani himoya dalili emas; dalil faqat yozib chiqilgan yo'l, zanjir va qoida matritsasi, hamda uni tasdiqlaydigan test.

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

## 20.13 Request matcher tuzog'i: Ant va MVC, `*` va `**`, regex

Qoidaning bitta g'oyasi bor: matcher yo'lni framework qanday talqin qilsa, AYNAN shunday tushunishi kerak. Matcher ning tushunchasi routing ning tushunchasidan farq qilsa, orada ochiq qolgan yo'l paydo bo'ladi, ya'ni jim turadigan authorization bypass: hech narsa buzilmaydi, log da xato yo'q, faqat himoyalangan deb o'ylangan endpoint himoyalanmagan.

Kanonik misol trailing slash. Spring MVC `@GetMapping("/hello")` ni `/hello` va `/hello/` uchun bir xil metodga xaritalaydi. MVC matcher `/hello` ni himoyalaganda `/hello/` ni ham o'z-o'zidan himoyalaydi, Ant matcher esa faqat berilgan ifodani so'zma-so'z qo'llaydi va Spring MVC ning bu xususiyatidan bexabar: `antMatchers("/hello").authenticated()` da `/hello` 401 qaytaradi, `/hello/` esa autentifikatsiyasiz `Hello!` beradi (Spilca, 8-bob, 189-bet). Kitob buni "jiddiy xavfsizlik teshigi" deb ataydi va shu sababli MVC matcher ni Ant matcher dan ustun qo'yishni tavsiya qiladi (Spilca, 8-bob, 186-bet).

Ifoda sintaksisi ikkala matcher da bir xil, va undagi birinchi xato `*` bilan `**` ni aralashtirish: `*` BITTA segment o'rnini bosadi, `**` esa KO'P segment (pastdagi jadval). Yo'l o'zgaruvchisiga shart qo'yish kerak bo'lsa `{param:regex}` ishlaydi, lekin nom, ikki nuqta va regex orasida bo'sh joy qolmasligi shart (Spilca, 8-bob, 184-185-bet). Shart bir nechta yo'l o'zgaruvchisini birga qamrasa (masalan `/video/{country}/{language}` da mamlakat va til kombinatsiyasi), Ant va MVC ifodalari yetmaydi va regex matcher kerak bo'ladi; regex o'qishga qiyin, shuning uchun u oxirgi chora (Spilca, 8-bob, 190-191-bet).

Qoidalar tartibi aniqdan umumiyga: `anyRequest()` dan keyin yozilgan aniq matcher ishlamaydi, shuning uchun `anyRequest()` har doim oxirgi qator (Spilca, 8-bob, 176-bet). Va yana bir chalkashlik: `permitAll` FAQAT avtorizatsiya haqida gapiradi. Autentifikatsiya avtorizatsiyadan oldin ishlaydi, demak `permitAll` endpointga noto'g'ri credential yuborilsa javob 401 bo'ladi, chaqiruv endpointga umuman yetib bormaydi (Spilca, 8-bob, 177-178-bet). Bu "autentifikatsiyasiz" emas, "muvaffaqiyatsiz autentifikatsiya": credential yuborilsa, framework uni baholaydi.

```java
// Spring Security 6: bitta `requestMatchers`, lekin semantika hali ham muhim.
@Bean
SecurityFilterChain catalogChain(HttpSecurity http) throws Exception {
    return http
        .httpBasic(Customizer.withDefaults())
        .authorizeHttpRequests(a -> a
            .requestMatchers("/product/{code:^[0-9]+$}").permitAll()
            .requestMatchers("/a/*").hasRole("MANAGER")   // faqat bitta segment
            .requestMatchers("/a/**").hasRole("ADMIN")    // /a va undan keyingi hammasi
            .requestMatchers(new RegexRequestMatcher(
                    "^/video/(US|CA|UK)/[a-z]{2}$", "GET")).authenticated()
            .anyRequest().denyAll())                      // umumiy qoida oxirida
        .build();
}
```

| Ifoda | Nimaga mos keladi |
|---|---|
| `/a` | faqat `/a` (MVC semantikasida `/a/` ham) |
| `/a/*` | `/a/b`, `/a/c`; `/a/b/c` ga mos emas |
| `/a/**` | `/a`, `/a/b`, `/a/b/c` |
| `/a/**/c` | `/a/b/c`, `/a/b/d/e/c` |
| `/a/{param}` | `/a` va bitta yo'l o'zgaruvchisi |
| `/a/{param:regex}` | o'zgaruvchi qiymati regex ga mos kelganda |

ESLATMA: kitob Spring Security 5.x ga tayanadi va `antMatchers`, `mvcMatchers`, `regexMatchers` ni alohida metod sifatida ishlatadi. Spring Security 6 da ularning o'rnida bitta `requestMatchers` qoldi, lekin qoidaning mohiyati o'zgarmadi, chunki tanlov endi yashirin: `requestMatchers(String...)` Spring MVC bor kontekstda MVC semantikasini, MVC bo'lmaganda Ant semantikasini oladi. `AntPathRequestMatcher` yoki `RegexRequestMatcher` ochiq yozilganda trailing slash tuzog'i qaytib keladi, shuning uchun yo'l, zanjir va qoida matritsasi [test bilan tasdiqlanadi](../testing/11-xavfsizlik-tranzaksiya-asinxron-va.md#112-avtorizatsiya-qoidalarini-testlash).

## 20.14 JWT imzo kaliti: simmetrik, assimmetrik, JWS va JWE

Imzo kalitini tanlash kriptografiya emas, ishonch chegarasi haqidagi qaror. Simmetrik kalitda bitta kalit tokenni ham imzolaydi, ham tekshiradi: eng sodda va eng tez yo'l (Spilca, 15-bob, 361-bet). Lekin bu kalitni har bir resource server bilan bo'lishish kerak, va kalitni qo'lida tutgan resource server tokenni tekshirishdan tashqari IMZOLAY ham oladi, ya'ni o'ziga istalgan huquqni yozib bera oladi (Spilca, 15-bob, 370-bet). Kitobning qoidasi shu joyda juda qisqa: kalitni tizimingizdan tashqariga berish kerak bo'lsa, u simmetrik bo'lmasligi kerak. Simmetrik kalitni pochta yoki boshqa himoyalanmagan kanal bilan uzatish taqiqlanadi.

Authorization server va resource server bir tashkilot tomonidan ishlab chiqilmagan bo'lsa, ishonch yo'q va assimmetrik kalit juftligi kerak: yopiq (private) kalit authorization server da turadi va faqat u imzolaydi, ochiq (public) kalit resource server da turadi va faqat tekshiradi. O'g'irlangan ochiq kalit hujumchiga hech narsa bermaydi, chunki u bilan token imzolab bo'lmaydi (Spilca, 15-bob, 371-372-bet). Amaliy xulosa: ichki monolit atrofida simmetrik kalit yetarli, ikkinchi jamoa yoki tashqi hamkor tokenni tekshiradigan joyda esa faqat assimmetrik.

Imzolangan JWT ni JWS, shifrlangan JWT ni JWE deb atashadi. JWS ning tanasi kalitsiz ham o'qiladi: hujumchi uni ko'radi, lekin o'zgartira olmaydi, chunki o'zgartirilgan tana imzoni buzadi; JWE ning tanasini esa kalitsiz umuman o'qib bo'lmaydi (Spilca, 15-bob, 361, 363-bet). Qoida shundan chiqadi: JWS tanasiga maxfiy hech narsa yozilmaydi, u amalda ochiq matn.

Kalitni foydalanuvchiga bog'lash alohida qarorni ochadi. Kitobning hands-on misolida JWT biznes-mantiq serverining o'zi biladigan simmetrik kalit bilan imzolanadi va soddalik uchun barcha foydalanuvchiga bitta kalit ishlatiladi; har foydalanuvchiga alohida kalit berishning foydasi esa aniq, chunki o'sha foydalanuvchining BARCHA tokenini bekor qilish uchun shunchaki uning kalitini o'zgartirish yetarli (Spilca, 11-bob, 278-bet). Bu [20.7](#207-token-muddati-yangilash-refresh-va-bekor-qilish-muammosi) dagi bekor qilish uchragan uch yo'lga to'rtinchi variantni qo'shadi.

```bash
# Kalit juftligi: yopiq kalit keyin ochiq kalit (Spilca, 15-bob, 372-373-bet).
keytool -genkeypair -alias ssia -keyalg RSA -keypass ssia123 \
        -keystore ssia.jks -storepass ssia123

keytool -list -rfc --keystore ssia.jks | openssl x509 -inform pem -pubkey
```

```java
// Assimmetrik: resource server faqat tekshiradi, imzolay olmaydi.
@Bean
JwtDecoder jwtDecoder(@Value("${jwt.public-key}") RSAPublicKey publicKey) {
    return NimbusJwtDecoder.withPublicKey(publicKey).build();
}

// Simmetrik: faqat bitta ishonch chegarasi ichida qoladigan kalit.
@Bean
JwtDecoder internalJwtDecoder(@Value("${jwt.key}") String key) {
    SecretKey secret = new SecretKeySpec(
            key.getBytes(StandardCharsets.UTF_8), "HmacSHA256");
    return NimbusJwtDecoder.withSecretKey(secret).build();
}
```

ESLATMA: kitob bu ishni `JwtTokenStore` va `JwtAccessTokenConverter` (Spring Security OAuth) bilan qiladi, bu sinflar zamonaviy Spring Security da yo'q; yuqoridagi misol `NimbusJwtDecoder` shaklida. Kalit aylanishi va JWKS uchun [20.6](#206-jwt-ni-tekshirish-imzo-iss-aud-exp-kalit-aylanishi-jwks) ga qaraladi. Yana bir nuqta ziddiyatga o'xshaydi: kitob 11-bobda JJWT bilan tokenni QO'LDA yasaydi va parse qiladi, korpus esa qo'lda parse qilishni taqiqlaydi. Ikkisi ziddiyat emas, shart boshqa: JJWT tokenni O'ZI chiqaradigan komponent uchun to'g'ri vosita, `JwtDecoder` esa tashqi IdP chiqargan tokenni qabul qiladigan resource server uchun yagona yo'l.

## 20.15 HTTP Basic: har so'rovda credential, `realmName` va xato javobi

HTTP Basic ni kitob to'rt joyda qaytarib tanqid qiladi va sababi bitta: u credential ni HAR so'rovda yuboradi. `Authorization` sarlavhasiga `Basic` prefiksi va `username:password` ning Base64 kodi tushadi. Base64 shifrlash ham, hashlash ham emas, u faqat uzatish qulayligi uchun kodlash; yo'lda ushlab olingan sarlavhadan credential to'g'ridan to'g'ri o'qiladi, shuning uchun HTTP Basic kamida HTTPS siz ishlatilmaydi (Spilca, 2-bob, 41-bet). Ikkinchi narx arxitektura darajasida: credential tarmoqda tez-tez aylanadi va klient uni qayergadir saqlashi kerak bo'ladi, hamda har ilova o'z credential ombori bilan yashaydi (Spilca, 12-bob, 285-286-bet).

Token aynan shu ikki narxni to'laydi: credential faqat birinchi so'rovda yuboriladi, keyin token ishlaydi; token qisqa umrli bo'lishi mumkin; tokenni credential ni bekor qilmasdan bekor qilish mumkin; token huquqlarni o'zi tashiydi; va autentifikatsiya mas'uliyati boshqa komponentga chiqariladi (Spilca, 11-bob, 251-bet). Shuning uchun HTTP Basic ni ichki, odam bormaydigan, tarmoqda himoyalangan servis-servis chaqiruvidan tashqarida tanlamaslik kerak, va [20.4](#204-sessiya-va-token-qachon-qaysi-biri-mantiqli) dagi tanlov HTTP Basic ni odatda chiqarib tashlaydi.

Qolgan holatda uni sozlash kerak bo'ladi. `realmName` realm nomini o'zgartiradi; realm ni ma'lum autentifikatsiya metodi bilan himoyalangan maydon deb o'qish mumkin. Diqqat qiladigan tafsilot: `WWW-Authenticate` sarlavhasi javobda FAQAT 401 holatida ko'rinadi, 200 da ko'rinmaydi, shuning uchun uni 200 javobda qidirish vaqt yo'qotish (Spilca, 5-bob, 125-bet). Muvaffaqiyatsiz autentifikatsiya javobining shaklini `AuthenticationEntryPoint#commence` belgilaydi: u `HttpServletRequest`, `HttpServletResponse` va sababchi `AuthenticationException` ni oladi, demak sarlavha qo'shish, holatni belgilash va tanani tozalash shu yerda bo'ladi. Kitobning ogohlantirishi shu joyda: muvaffaqiyatsiz autentifikatsiya javobi maxfiy ma'lumot sizdirishning odatiy nuqtasi, shuning uchun tanaga sabab yozilmaydi (Spilca, 5-bob, 126-bet).

```java
@Bean
SecurityFilterChain internalBasicChain(HttpSecurity http) throws Exception {
    return http
        .securityMatcher("/internal/**")      // faqat servis-servis yo'li
        .httpBasic(b -> {
            b.realmName("payments-internal");
            b.authenticationEntryPoint((req, res, ex) -> {
                res.setHeader("WWW-Authenticate", "Basic realm=\"payments-internal\"");
                res.setHeader("X-Request-Id", MDC.get("requestId"));
                res.sendError(HttpStatus.UNAUTHORIZED.value());   // tana bo'sh
            });
        })
        .authorizeHttpRequests(a -> a.anyRequest().hasRole("SERVICE"))
        .build();
}
```

ESLATMA: kitob `AuthenticationEntryPoint` ni ishlatadigan komponentni `ExceptionTranslationManager` deb ataydi; zanjirdagi haqiqiy sinf nomi `ExceptionTranslationFilter` ([20.1](#201-securityfilterchain-tuzilishi-va-filtrlar-tartibi)). Kitobning misoli `WebSecurityConfigurerAdapter` ichidagi `configure(HttpSecurity)` da yozilgan, yuqoridagi shakl esa `SecurityFilterChain` bean.

## 20.16 Form login: maxsus sahifa, handler lar va HTTP Basic bilan birga

`formLogin()` ni yoqish bilan Spring Security standart login va logout sahifasini o'zi beradi. O'z sahifangizga o'tish ikki qadam: `loginPage("/login")` bilan yo'lni aytish va o'sha yo'l uchun controller hamda view berish, aks holda autentifikatsiyasiz foydalanuvchi mavjud bo'lmagan sahifaga yo'naltiriladi (Walls, 5-bob, 128-bet). POST manzili va maydon nomlari standart holatda `/login`, `username` va `password`; ularni `loginProcessingUrl`, `usernameParameter` va `passwordParameter` o'zgartiradi va forma HTML i bilan mos bo'lishi shart (Walls, 5-bob, 130-bet).

Muvaffaqiyatli login dan keyingi manzil ham tuzoq tug'diradi. Standart xulq: foydalanuvchini u borishni xohlagan sahifaga qaytarish, login sahifasiga o'zi kelgan bo'lsa esa ildizga yuborish. `defaultSuccessUrl("/design")` faqat shu ikkinchi holatni o'zgartiradi; har holatda majburan bitta sahifaga yuborish kerak bo'lsa ikkinchi parametr `true` beriladi (Walls, 5-bob, 130-bet). Logout esa POST `/logout` ni tutadigan filtr qo'yadi, shuning uchun view da havola emas, forma kerak (Walls, 5-bob, 133-bet).

Qaror shartga bog'liq bo'lganda `defaultSuccessUrl` yetmaydi va `AuthenticationSuccessHandler` kerak: `onAuthenticationSuccess` so'rov, javob va `Authentication` ni oladi, demak huquqqa qarab boshqa-boshqa manzilga yo'naltirish mumkin. Uning jufti `AuthenticationFailureHandler`: u javobga sarlavha qo'shadi, so'rov identifikatorini qaytaradi yoki hodisani log ga yozadi. Kitob ikkisini klient javobning aniq shaklini kutgan holat uchun tavsiya qiladi va javobni tozalab, maxfiy ma'lumot chiqmasligini eslatadi (Spilca, 5-bob, 130-132-bet).

Oxirgi nuqta amalda ko'p vaqt yo'qotadi: faqat `formLogin()` yozilgan zanjirda to'g'ri HTTP Basic credential bilan kelgan so'rov ham 302 oladi va login formasiga yo'naltiriladi. Ikkala metod kerak bo'lsa ikkisini ochiq yozish shart (Spilca, 5-bob, 133-bet). Arxitektor qarori shu yerda: ikkisini bitta zanjirda birga ushlash faqat o'tish davri uchun mantiqli, barqaror holatda brauzer yo'li va API yo'li `securityMatcher` bilan alohida zanjirga ajratiladi ([20.1](#201-securityfilterchain-tuzilishi-va-filtrlar-tartibi)).

```java
@Bean
SecurityFilterChain uiChain(HttpSecurity http,
                            AuthenticationSuccessHandler successHandler,
                            AuthenticationFailureHandler failureHandler) throws Exception {
    return http
        .formLogin(f -> f
            .loginPage("/login")                  // o'z sahifasi: controller va view kerak
            .loginProcessingUrl("/authenticate")  // forma POST manzili
            .usernameParameter("user")
            .passwordParameter("pwd")
            .successHandler(successHandler)       // huquqqa qarab yo'naltirish
            .failureHandler(failureHandler))      // javob shakli va log
        .httpBasic(Customizer.withDefaults())     // o'tish davri uchun ikkisi birga
        .logout(l -> l.logoutUrl("/logout"))      // faqat POST
        .authorizeHttpRequests(a -> a
            .requestMatchers("/login", "/css/**").permitAll()
            .anyRequest().authenticated())
        .build();
}
```

ESLATMA: kitoblarning ikkisi ham `and()` bilan zanjirlangan uslubni ishlatadi (Walls `SecurityFilterChain` bean ichida, Spilca `WebSecurityConfigurerAdapter` ichida); Spring Security 6 da `and()` deprecated va yuqoridagi lambda shakli yagona yo'l ([20.3](#203-spring-security-6-konfiguratsiyasi-lambda-uslubi-va-eski-uslubdan-farqi)).

## 20.17 Xavfsizlikning besh funksiyasi: faqat himoya emas

Bu bob boshdan oxirigacha bitta funksiya haqida: himoya. Filter chain, token tekshiruvi, matcher va metod darajasidagi qoidalar hammasi hujumni to'sish uchun. Newman shu tor qarashning xavfini ko'rsatadi va ilova xavfsizligini butun holda tavsiflash uchun AQSh NIST (National Institute of Standards and Technology) ning besh qismli modelini tanlaydi; uning so'zlari bilan model aynan shu holistik tabiati bilan foydali, chunki qanday tahdidga duch kelishingizni o'ylab ko'rmasdan butun kuchni himoyaga sarflash juda oson, aqlli hujumchi himoyadan o'tib ketganda nima qilishni o'ylash esa undan ham kechikadi (Sam Newman, *Building Microservices: Designing Fine-Grained Systems*, 2-nashr, O'Reilly, 2021, 11-bob, "The Five Functions of Cybersecurity" bo'limi).

| Funksiya | Nima qiladi | Korpusda qayerda |
| --- | --- | --- |
| Identify | hujumchi kim, u nimani olmoqchi va siz qayerda eng zaifsiz | tahdid modellashtirish; jamoa bilan birga qilinadigan shakli [risk-storming](07-nosozlik-haqida-fikrlash.md#711-risk-storming-xavfni-jamoa-bilan-diagramma-ustida-topish) |
| Protect | asosiy aktivlarni himoyalash | shu bobning qolgan hamma bo'limi |
| Detect | barcha urinishga qaramay hujum bo'lganini aniqlash | [audit izlari](#2011-parol-saqlash-maxfiy-malumot-va-audit-izlari) va [alert dizayni](30-kuzatuvchanlik-amaliyoti-log-metrika-trace.md#3010-ogohlantirish-alert-dizayni-belgiga-emas-foydalanuvchi-tasiriga-qarab) |
| Respond | yomon narsa yuz bergani aniqlangandan keyin harakat qilish | [birinchi qadam: tiklash](35-incident-on-call-va-post-mortem.md#353-birinchi-qadam-tiklash-sabab-qidirish-emas) |
| Recover | incidentdan keyin tiklanish | [tiklanish vaqti](07-nosozlik-haqida-fikrlash.md#79-tiklanish-vaqti-rto-va-rpo-raqamlarini-kelishib-olish) va post-mortem |

Birinchi funksiya eng ko'p tashlab ketiladigani va Newman uning sababini dasturchi psixologiyasida ko'radi: mikroservis arxitekturasidagi xavfsizlik xavflari haqida gaplashganda dasturchilar darhol JWT va mutual TLS haqida gapira boshlaydi, ya'ni ko'rinadigan texnik muammolarga texnik yechim izlaydi (11-bob, "Identify"). Uning hikoyasi shu xatoni yaxshi ko'rsatadi: bir kompaniyada ruxsatsiz odam qabulxonaga, keyin korporativ tarmoqqa kirgandan keyin ofislarga videokuzatuv o'rnatish bo'yicha uzoq bahs ketgan, bahs esa xodimni kuzatish va buzg'unchiga ruxsat berish o'rtasidagi qarama-qarshilikka aylangan; shu paytda bir xodim asosiy ofislardan birining eshigi qulfi buzuq ekanini va yillar davomida odamlar ertalab kelib eshikni qulflanmagan holda topganini aytgan (11-bob, "Identify"). Darsi aniq: eng katta xavf qayerda ekanini tushunmasdan, vaqtni noto'g'ri joyga sarflash mumkin.

Tahdid modellashtirishning natijasi hujjat emas, ro'yxat bo'ladi: qanday xavfsizlik nazoratlari qo'yilishi kerakligi haqidagi tavsiyalar, va ular jarayon o'zgarishi, texnologiya almashishi yoki arxitektura o'zgarishi shaklida bo'lishi mumkin; bir qismi ko'ndalang bo'lib bir nechta jamoaga tegadi, bir qismi esa tor ishga aylanadi (11-bob, "Identify"). Newman bitta majburiy shartni qo'yadi: modellashtirish butun holda qilinishi kerak, tahlilni bir-ikki mikroservisga qisqartirish yolg'on xavfsizlik hissi beradi, ya'ni ajoyib mustahkam kirish eshigi qurib, derazani ochiq qoldirish bilan tugaydi.

Detect funksiyasi Spring tomonida odatda bo'sh qoladi, chunki autentifikatsiya xatolari faqat log ga tushadi va ularni hech kim o'qimaydi. Spring Security hodisalarini metrikaga chiqarish shu bo'shliqni arzon yopadi.

```java
// Detect: parol xatosi va ruxsat rad etilishi metrikaga chiqadi.
// Shundan keyin alert qoidasi yozish mumkin bo'ladi, log o'qishni kutmasdan.
@Component
public class SecurityEventMetrics {

    private final Counter badCredentials;
    private final Counter accessDenied;

    public SecurityEventMetrics(MeterRegistry registry) {
        this.badCredentials = Counter.builder("security.authentication.failure")
                .tag("reason", "bad_credentials")   // foydalanuvchi nomi teg bo'lmaydi
                .register(registry);
        this.accessDenied = Counter.builder("security.authorization.denied")
                .register(registry);
    }

    @EventListener
    public void onBadCredentials(AuthenticationFailureBadCredentialsEvent event) {
        badCredentials.increment();
    }

    @EventListener
    public void onAccessDenied(AuthorizationDeniedEvent<?> event) {
        accessDenied.increment();
    }
}
```

Teg tanlashda ehtiyot bo'lish kerak: foydalanuvchi nomini yoki token subject ini metrika tegiga qo'yish kardinallikni portlatadi va maxfiy ma'lumotni metrika tizimiga chiqaradi ([kardinallik portlashi](30-kuzatuvchanlik-amaliyoti-log-metrika-trace.md#306-kardinallik-portlashi-metrika-tegiga-foydalanuvchi-id-qoyish-xatosi)). Respond va recover funksiyalari esa bu bobda emas, [incident](35-incident-on-call-va-post-mortem.md#353-birinchi-qadam-tiklash-sabab-qidirish-emas) bobida yashaydi, va bu to'g'ri taqsimot: xavfsizlik incidenti ham incident, faqat uning aloqa va huquqiy qismi qo'shimcha bo'ladi.

Identify funksiyasining ikkinchi, rasmiyroq shakli ham bor. Fairbanks xavfsizlik tahlilini modellashtirish masalasi deb qo'yadi: tizim ma'lumot oqimi diagrammasi (data flow diagram) sifatida modellashtiriladi va manba kodining shu modeldan chetga chiqmagani tekshiriladi, ya'ni hujum yo'llari diagramma ustida qidiriladi. Spring loyihasida bu amalda shunday ko'rinadi: maxfiy ma'lumot qaysi endpoint dan kirib, qaysi bean orqali o'tib, qaysi jadvalga yoki tashqi chaqiruvga chiqishi chiziladi, keyin kodda shu chiziqdan tashqari yo'l (masalan log ga yozish yoki hisobot so'rovi) bor-yo'qligi qidiriladi. Diagrammaning chegarasi ham ochiq: u faqat oqimni ko'rsatadi, qaroring to'g'riligini emas.

Ikkinchi va noqulayroq savol: qancha nazorat qo'yish kerak. Fairbanks ning kuzatuvi aniq, xavfsizlikni har doim yana bir qadam oshirish mumkin, har qo'shimcha chora esa narx bilan keladi, va manfaatdorlar qaysi choralar to'plami ular uchun optimal bo'lishini bilmaydi. Shuning uchun jarayon manfaatdorlarni o'z ehtiyojini tushunishga olib boradi va tanlov shu tushunchadan chiqadi, ya'ni "hammasini yoqamiz" ham, "keyin qo'shamiz" ham javob emas.

Shu bilan bog'liq uchinchi savol xavfsizlikning arxitektura atributi sifatidagi o'rniga tegishli. *Fundamentals of Software Architecture* chegarani aniq qo'yadi: xavfsizlik arxitektura xarakteristikasi bo'ladigan nuqta uning tizim strukturasiga talab qo'yishi. Agar to'lovni uchinchi tomon qayta ishlasa, oddiy gigiena yetadi, ya'ni ma'lumotni shifrlash va parolni hash qilish; bu ishlar dizayn tanlovini o'zgartirmaydi. Agar ilovaning o'zi to'lovni qayta ishlasa, kritik xavfsizlik qismlari alohida modul yoki komponent bilan izolyatsiya qilinadi, ya'ni xavfsizlik endi strukturaga ta'sir qiladi va arxitektura xarakteristikasiga aylanadi. Amaliy foydasi: "xavfsizlik muhim" degan gap talabga aylantirilishi kerak, va mezon shu, u chegara chizadimi yoki yo'q.

ESLATMA: yuqoridagi `SecurityEventMetrics` sinfi va jadvalning "Korpusda qayerda" ustuni shu korpusning qo'shimchasi. Newman besh funksiyani sanaydi va har birini mikroservis kontekstida izohlaydi, Spring kodini bermaydi. Data flow diagrammasining Spring dagi ko'rinishi haqidagi paragraf ham shu korpusning qo'shimchasi.

## 20.18 Avtorizatsiya qarori qayerda turadi: gateway da qo'pol, servis ichida ingichka

Bu savol korpus ichida qarama-qarshi javob olgan, shuning uchun u alohida bo'limda hal qilinadi. [patterns 18.37](../patterns/18-xavfsizlik-patternlari.md#1837-eng-kam-imtiyoz-least-privilege) eng kam imtiyoz patternida huquqlarni qo'pol (coarse-grained) rol lar emas, ingichka (fine-grained) permission lar sifatida modellashtirishni aytadi. Newman esa 11-bobda teskari ko'rinadigan gap aytadi: qo'pol rol larni afzal ko'r. Ikki gap bir-biriga zid emas, chunki ular turli savolga javob beradi. Ajratuvchi shart bitta: **huquq qayerda saqlanadi va qayerda baholanadi**.

| Savol | Javob | Qayerda |
|---|---|---|
| Foydalanuvchi tizimga kirganmi | autentifikatsiya | gateway yoki SSO |
| Foydalanuvchi bu ilovaga umuman kira oladimi | qo'pol rol (`STAFF`, `CALL_CENTER`) | gateway yoki SSO, identity provider dagi atribut |
| Foydalanuvchi mijozning to'lov ma'lumotini ko'ra oladimi | ingichka qoida | o'sha ma'lumotga egalik qiladigan servis |
| Foydalanuvchi qancha summagacha qaytarim bera oladi | ingichka qoida | qaytarim funksionalligi yashaydigan servis |

Newman ning ogohlantirishi aynan birinchi ustunning oxirgi ikki qatorini uchinchi qatordan tashqariga chiqarishga qarshi. Gateway autentifikatsiyadan keyin principal ning atributlarini ajratib olsa, qo'polroq qaror qabul qila oladi, masalan `STAFF` rolisiz hech kim helpdesk ilovasiga kira olmasligi. Lekin undan keyingi qarorlar servisning o'ziga qoldirilishi kerak, chunki aniq amallarga ruxsat berishni servis hal qiladi. Teskari yo'lning natijasi kitobda nomlangan: `CALL_CENTER_50_DOLLAR_REFUND` kabi haddan tashqari ingichka rol lar yaratilib, bitta servis funksionalligiga xos ma'lumot directory servisiga tiqilib qoladi. Natijasi ikki qatorda: bunday tizimni yuritish koshmar, va servisning mustaqil hayot sikli yo'qoladi, chunki servis o'zini qanday tutishi haqidagi ma'lumotning bir qismi endi boshqa joyda, ehtimol tashkilotning boshqa qismi boshqaradigan tizimda yashaydi. Shuning uchun Newman ning tavsiyasi "ingichka huquq yomon" degani emas: u identity provider da tashkilot ishlashiga mos qo'pol rol larni ushlashni, ingichka qarorni esa funksionallik yashaydigan joyga qoldirishni aytadi.

Markazda hamma avtorizatsiyani bajarish yo'li ham bor va Newman uni confused deputy muammosining yechimlaridan biri sifatida sanaydi: so'rov tizimga kirgan zahoti, SSO gateway da yoki chetki ilovada, hamma kerakli avtorizatsiya bajariladi va quyi servislar so'rov allaqachon ruxsat etilgan deb qabul qiladi. Narxi esa uch qatorda yozilgan. Birinchisi, bu yashirin ishonchni (implicit trust) qabul qilish, ya'ni zero trust dan voz kechish. Ikkinchisi, yuqoridagi birlik quyi servislar qanday funksionallik berishini va unga kirishni qanday cheklashni bilishi kerak bo'ladi. Uchinchisi va eng amaliysi, mustaqil deploy yo'qoladi: yangi funksionallikni chiqarish endi servisni deploy qilish bilan birga gateway ga avtorizatsiya konfiguratsiyasini qo'llashni ham talab qiladi. Shu sababli Newman qarorni funksionallik yashaydigan servisga surishni afzal ko'radi, chunki bu servisni o'z ichiga yopiq qiladi va kerak bo'lsa zero trust ni amalga oshirish imkonini beradi.

Shunda servisga qaror uchun kerakli ma'lumotni yetkazish muammosi qoladi va uning yechimi JWT: so'rovni kim yuborganini va uning qaysi guruhlarga tegishli ekanini ishonchli uzatish kerak, chunki foydalanuvchi nomini oddiy HTTP sarlavhasiga yozish uni istalgan odam almashtirib qo'yishiga ochiq qoldiradi. Tekshiruv mexanikasi [20.6](#206-jwt-ni-tekshirish-imzo-iss-aud-exp-kalit-aylanishi-jwks) da.

Spring da bu taqsimot shunday ko'rinadi: gateway yoki chetki filter chain qo'pol darajada to'sadi, servis ichida esa `@PreAuthorize` va `AuthorizationManager` ingichka qarorni token dagi atributlar asosida chiqaradi.

```java
// Chetki daraja: qo'pol. Token dagi rol bo'yicha butun hududni yopadi.
@Bean
SecurityFilterChain helpdeskChain(HttpSecurity http) throws Exception {
    return http.securityMatcher("/helpdesk/**")
            .authorizeHttpRequests(a -> a
                    .anyRequest().hasAuthority("ROLE_CALL_CENTER"))  // tashkiliy rol
            .oauth2ResourceServer(o -> o.jwt(Customizer.withDefaults()))
            .build();
}
```

```java
// Servis ichi: ingichka. Qoida va chegara shu servisning kodida va bazasida.
@Service
class RefundService {

    private final RefundLimitPolicy limits;   // chegara shu servisda, IdP da emas

    // Rol gateway dan keldi; summaning chegarasi esa shu yerda hal bo'ladi.
    @PreAuthorize("hasAuthority('ROLE_CALL_CENTER')")
    @Transactional
    public Refund issue(OrderId orderId, Money amount, Jwt principal) {
        Money cap = limits.capFor(principal.getClaimAsStringList("groups"));
        if (amount.compareTo(cap) > 0) {
            throw new RefundLimitExceeded(amount, cap);   // 403, audit ga tushadi
        }
        return refunds.create(orderId, amount, principal.getSubject());
    }
}
```

Shundan patterns 18.37 bilan kelishuv chiqadi va u bitta jumlada: eng kam imtiyoz talabi ingichka permission ni **qayerda ishlatish** haqida, Newman ning ogohlantirishi esa uni **qayerda saqlash** haqida. Ingichka permission servisning o'z kodida, o'z bazasida va o'z testida yashaydi; markaziy directory da esa faqat tashkilot tuzilmasiga mos qo'pol rol lar qoladi. Patterns 18.37 ning oxiridagi ogohlantirish ham shu yo'nalishda ishlaydi: yuzlab mayda permission tushunarsiz bo'lib qolsa, jamoa "hammasini bera qolaylik" deydi va natija teskari bo'ladi, ya'ni ikki manba bitta xatoni, ingichka huquqni noto'g'ri joyga chiqarishni, turli so'z bilan qoralaydi.

## 20.19 Amalda qo'llash

- [ ] Barcha `SecurityFilterChain` beanlarni ro'yxatga oling, `@Order` va `securityMatcher` qiymatlarini yozib, har bir yo'l qaysi zanjirga tushishini jadvalda tasdiqlang.
- [ ] Har bir zanjirda oxirgi qoida `anyRequest().authenticated()` yoki undan qattiqroq ekanini tekshiring, `permitAll` ni faqat aniq ro'yxat uchun qoldiring.
- [ ] `JwtDecoder` ga `aud` validatorini qo'shing yoki `spring.security.oauth2.resourceserver.jwt.audiences` ni to'ldiring, so'ng boshqa audience li token bilan 401 kelishini tasdiqlang.
- [ ] JWKS chaqiruviga connect taxminan 2 sekund va read taxminan 3 sekund timeout o'rnatib, IdP ni mavjudlik bog'liqligi sifatida monitoringga qo'shing.
- [ ] Access token TTL ini 15 daqiqadan oshmaydigan qilib kelishib oling va huquq olingandan keyin eski token qancha yashashini SLA sifatida hujjatlashtiring.
- [ ] `@Async` va batch kodda `DelegatingSecurityContextExecutorService` ishlatilayotganini tekshiring, aks holda `@PreAuthorize` va audit nomlari bo'sh qoladi.
- [ ] Ko'p ijarachi jadvallarda RLS ni yoqib, `SET LOCAL` ishlatilayotganini va sozlama yo'q holatda hech qanday qator qaytmasligini tekshiring.
- [ ] Chiqishdan oldin tokensiz `curl` skriptini CI ga qo'shib, `/actuator/env`, `/actuator/heapdump` va yangi versiya prefikslarini har deploy da sinab turing.

## Manbalar

- Laurentiu Spilca, *Spring Security in Action*, 1-bob - Spring Security nima qiladi va nimani dasturchiga qoldiradi
- Laurentiu Spilca, *Spring Security in Action*, 2-bob - Spring Security ning birinchi sozlamalari
- Laurentiu Spilca, *Spring Security in Action*, 5-bob - HTTP Basic sozlamalari, form login va autentifikatsiya handler lari
- Laurentiu Spilca, *Spring Security in Action*, 8-bob - avtorizatsiya uchun request matcher turlari: MVC, Ant va regex
- Laurentiu Spilca, *Spring Security in Action*, 11-bob - token nima beradi, JWT tuzilishi va imzo kaliti
- Laurentiu Spilca, *Spring Security in Action*, 9-bob - filtrlar va filter chain mexanikasi
- Laurentiu Spilca, *Spring Security in Action*, 12-15-boblar - OAuth 2 oqimlari, resource server va JWT
- Craig Walls, *Spring in Action* 6th, 5, 8-boblar - Spring Security va REST ni himoyalash
- John Carnell, *Spring Microservices in Action*, 7-bob - mikroservisni himoyalash
- Sam Newman, *Building Microservices: Designing Fine-Grained Systems*, 2-nashr, O'Reilly, 2021, 11-bob ("The Five Functions of Cybersecurity", "Identify", "Protect" bo'limlari) - NIST ning besh qismli modeli (identify, protect, detect, respond, recover) va uning holistik tabiati; butun kuchni himoyaga sarflash xatosi; dasturchilarning darhol JWT va mutual TLS ga o'tishi; videokuzatuv bahsi va buzuq eshik qulfi hikoyasi; tahdid modellashtirishning natijasi xavfsizlik nazoratlari ro'yxati ekani va tahlilni bir-ikki mikroservisga qisqartirish yolg'on xavfsizlik hissi berishi; mikroservisning hujum sathini kengaytirishi va shu bilan chuqur himoya imkonini ham berishi. Bu nashrning qo'limizdagi elektron nusxasida barqaror bet raqami yo'q, shuning uchun faqat bob va bo'lim nomi ko'rsatilgan
- [Spring Security 6.3, CSRF](https://raw.githubusercontent.com/spring-projects/spring-security/6.3.0/docs/modules/ROOT/pages/features/exploits/csrf.adoc) - CSRF himoyasi, token repository va SPA holati
- [OWASP, CSRF Prevention Cheat Sheet](https://raw.githubusercontent.com/OWASP/CheatSheetSeries/72865b1e3b5754246a101778dc00b37f9c233373/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.md) - himoya usullari va ularning chegaralari
- Sam Newman, *Building Microservices: Designing Fine-Grained Systems*, 2-nashr, O'Reilly, 2021, 11-bob ("Fine-Grained Authorization", "Centralized, Upstream Authorization", "Decentralizing Authorization" bo'limlari) - gateway ning qo'pol darajada to'sishi, keyingi qarorlarni servisning o'ziga qoldirish, `CALL_CENTER_50_DOLLAR_REFUND` kabi ingichka rol larni directory ga tiqishning narxi (yuritish qiyinligi va servisning mustaqil hayot siklini yo'qotishi), markaziy avtorizatsiyaning yashirin ishonch, gateway ning quyi funksionallikni bilishi va mustaqil deploy yo'qolishi narxi, hamda foydalanuvchi nomini oddiy sarlavhada uzatishning xavfi
- Sam Newman, *Building Microservices: Designing Fine-Grained Systems*, 2-nashr, O'Reilly, 2021, 11-bob ("Challenges" bo'limi, JSON Web Tokens) - imzo tekshirish uchun ochiq kalitni yetkazish va almashtirish muammosi hamda Vault, uzoq asinxron jarayon uchun token muddati va ikki ko'rilgan yo'l (doirasi cheklangan uzoq muddatli token yoki oqimning ma'lum nuqtasidan keyin tokendan voz kechish), token juda kattalashganda (bitta trek uchun 10 minggacha yozuv) oddiy token bilan boshlang'ich avtorizatsiya qilib qolganini ma'lumotlar omboridan qidirish. Bu nashrning qo'limizdagi elektron nusxasida barqaror bet raqami yo'q, shuning uchun faqat bob va bo'lim nomi ko'rsatilgan
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, O'Reilly, 2020, 4-bob ("Architecture Characteristics Defined") - xavfsizlik maxsus struktura talab qilgandagina arxitektura xarakteristikasi bo'lishi: to'lovni uchinchi tomon qayta ishlasa oddiy gigiena (shifrlash, hash) yetadi, ilovaning o'zi qayta ishlasa kritik xavfsizlik alohida modul yoki komponent bilan izolyatsiya qilinadi. Qo'limizdagi nusxada chop etilgan bet raqami yo'q, shuning uchun faqat bob nomi ko'rsatilgan
- George Fairbanks, *Just Enough Software Architecture*, 1-nashr, 2010, 15.6.3 - xavfsizlik tahlilini ma'lumot oqimi diagrammasi (DFD) bilan modellashtirish va manba kodining modeldan chetga chiqmaganini tekshirish, hamda har qo'shimcha xavfsizlik chorasining narxi va manfaatdorlarning optimal to'plamni bilmasligi
- Herbert Schildt, *Java The Complete Reference*, 12-nashr, McGraw-Hill, 2022, 22-bob (753-bet) - `Console.readPassword` ning `char[]` qaytarishi va massivni ishlatilgandan keyin nolga to'ldirish talabi, `String` esa xotirada qolishi
- ESLATMA: 20.18 dagi `helpdeskChain` va `RefundService` kod misollari hamda qaror joylashuvi jadvali shu korpusning qo'shimchasi; `patterns 18.37` bilan kelishuv shartining ("qayerda ishlatish" va "qayerda saqlash") ifodasi ham shu korpusning xulosasi

---

[&larr; 19. Spring tranzaksiyalari va ularning chegaralari](19-spring-tranzaksiyalari-va-ularning.md) · [Mundarija](README.md) · [21. PostgreSQL arxitekturasi: process model, WAL, checkpoint, vacuum &rarr;](21-postgresql-arxitekturasi-process-model-wal.md)
