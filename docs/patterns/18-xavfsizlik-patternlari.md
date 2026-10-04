<!-- doc: patterns | chapter: 18 | part:  -->

[Java Spring arxitektori bilishi kerak bo'lgan barcha dizayn patternlar](../../README.md) / [Dizayn patternlar](README.md)

# 18. Xavfsizlik patternlari (Security Patterns)

<details>
<summary>Bu bo'limdagi 48 bo'lim</summary>

- [18.1 Autentifikatsiya va avtorizatsiya ajratilishi (Authentication vs Authorization)](#181-autentifikatsiya-va-avtorizatsiya-ajratilishi-authentication-vs-authorization)
- [18.2 Xavfsizlik filtrlar zanjiri (SecurityFilterChain - Chain of Responsibility)](#182-xavfsizlik-filtrlar-zanjiri-securityfilterchain---chain-of-responsibility)
- [18.3 Autentifikatsiya menejeri va delegatsiya (AuthenticationManager / ProviderManager)](#183-autentifikatsiya-menejeri-va-delegatsiya-authenticationmanager--providermanager)
- [18.4 Autentifikatsiya provayderi (AuthenticationProvider)](#184-autentifikatsiya-provayderi-authenticationprovider)
- [18.5 Foydalanuvchi ma'lumotlari manbasi (UserDetailsService)](#185-foydalanuvchi-malumotlari-manbasi-userdetailsservice)
- [18.6 Xavfsizlik konteksti egasi (SecurityContextHolder - Thread-Specific Storage)](#186-xavfsizlik-konteksti-egasi-securitycontextholder---thread-specific-storage)
- [18.7 Parol hash'lash va yangilanuvchan kodlash (Password hashing - DelegatingPasswordEncoder, upgradable encoding)](#187-parol-hashlash-va-yangilanuvchan-kodlash-password-hashing---delegatingpasswordencoder-upgradable-encoding)
- [18.8 Rolga asoslangan kirish nazorati (Role-Based Access Control - RBAC)](#188-rolga-asoslangan-kirish-nazorati-role-based-access-control---rbac)
- [18.9 Atribut va siyosatga asoslangan kirish nazorati (Attribute-Based / Policy-Based Access Control - ABAC)](#189-atribut-va-siyosatga-asoslangan-kirish-nazorati-attribute-based--policy-based-access-control---abac)
- [18.10 Metod darajasidagi xavfsizlik (Method Security - @PreAuthorize, @PostAuthorize)](#1810-metod-darajasidagi-xavfsizlik-method-security---preauthorize-postauthorize)
- [18.11 Ifodaga asoslangan xavfsizlik (Expression-based security - SpEL)](#1811-ifodaga-asoslangan-xavfsizlik-expression-based-security---spel)
- [18.12 Avtorizatsiya kodi + PKCE (OAuth2 Authorization Code + PKCE)](#1812-avtorizatsiya-kodi--pkce-oauth2-authorization-code--pkce)
- [18.13 Client Credentials oqimi (OAuth2 Client Credentials)](#1813-client-credentials-oqimi-oauth2-client-credentials)
- [18.14 Resource Server (OAuth2 Resource Server (JWT / opaque))](#1814-resource-server-oauth2-resource-server-jwt--opaque)
- [18.15 Token introspeksiyasi (Token Introspection)](#1815-token-introspeksiyasi-token-introspection)
- [18.16 Token uzatish (Token Relay)](#1816-token-uzatish-token-relay)
- [18.17 Refresh token aylanishi (Refresh Token Rotation)](#1817-refresh-token-aylanishi-refresh-token-rotation)
- [18.18 OpenID Connect (OpenID Connect)](#1818-openid-connect-openid-connect)
- [18.19 Spring Authorization Server (Spring Authorization Server)](#1819-spring-authorization-server-spring-authorization-server)
- [18.20 Federatsiyalangan identifikatsiya (Federated Identity)](#1820-federatsiyalangan-identifikatsiya-federated-identity)
- [18.21 Sessiyani boshqarish (Session Management (fixation protection, concurrent sessions))](#1821-sessiyani-boshqarish-session-management-fixation-protection-concurrent-sessions)
- [18.22 Remember-Me (Remember-Me)](#1822-remember-me-remember-me)
- [18.23 CSRF himoyasi (CSRF Protection - Synchronizer Token, Double Submit)](#1823-csrf-himoyasi-csrf-protection---synchronizer-token-double-submit)
- [18.24 CORS (Cross-Origin Resource Sharing)](#1824-cors-cross-origin-resource-sharing)
- [18.25 Xavfsizlik header'lari (Security Headers - CSP, HSTS)](#1825-xavfsizlik-headerlari-security-headers---csp-hsts)
- [18.26 Brute-force himoyasi / Akkaunt bloklash (Brute-force Protection / Account Lockout)](#1826-brute-force-himoyasi--akkaunt-bloklash-brute-force-protection--account-lockout)
- [18.27 Ko'p faktorli autentifikatsiya (Multi-Factor Authentication)](#1827-kop-faktorli-autentifikatsiya-multi-factor-authentication)
- [18.28 Passkey'lar / WebAuthn (Passkeys / WebAuthn)](#1828-passkeylar--webauthn-passkeys--webauthn)
- [18.29 Bir martalik token bilan kirish (One-Time Token Login / Magic Link)](#1829-bir-martalik-token-bilan-kirish-one-time-token-login--magic-link)
- [18.30 Sirlarni boshqarish (Secrets Management - Vault, Config Server Encryption)](#1830-sirlarni-boshqarish-secrets-management---vault-config-server-encryption)
- [18.31 Zero Trust (Zero Trust Architecture)](#1831-zero-trust-zero-trust-architecture)
- [18.32 mTLS (Mutual TLS)](#1832-mtls-mutual-tls)
- [18.33 API kaliti (API Key)](#1833-api-kaliti-api-key)
- [18.34 Audit log yuritish (Audit Logging)](#1834-audit-log-yuritish-audit-logging)
- [18.35 Kirish ma'lumotini tekshirish / chiqishni kodlash (Input Validation / Output Encoding)](#1835-kirish-malumotini-tekshirish--chiqishni-kodlash-input-validation--output-encoding)
- [18.36 Qatlamli himoya (Defense in Depth)](#1836-qatlamli-himoya-defense-in-depth)
- [18.37 Eng kam imtiyoz (Least Privilege)](#1837-eng-kam-imtiyoz-least-privilege)
- [18.38 Standart holatda xavfsiz (Secure by Default)](#1838-standart-holatda-xavfsiz-secure-by-default)
- [18.39 Xavfsiz tarzda yiqilish (Fail Securely)](#1839-xavfsiz-tarzda-yiqilish-fail-securely)
- [18.40 Vazifalarni ajratish (Separation of Duties)](#1840-vazifalarni-ajratish-separation-of-duties)
- [18.41 To'liq vositachilik (Complete Mediation)](#1841-toliq-vositachilik-complete-mediation)
- [18.42 Security kontekstini tarqatish (Security Context Propagation)](#1842-security-kontekstini-tarqatish-security-context-propagation)
- [18.43 Multi-tenant xavfsizlik (Multi-Tenant Security)](#1843-multi-tenant-xavfsizlik-multi-tenant-security)
- [18.44 Authorization Server yoki ichki auth tanlovi (Authorization Server vs Embedded Auth)](#1844-authorization-server-yoki-ichki-auth-tanlovi-authorization-server-vs-embedded-auth)
- [18.45 Yagona kirish (Single Sign-On (SSO))](#1845-yagona-kirish-single-sign-on-sso)
- [18.46 Munosabatga asoslangan kirish nazorati (Relationship-Based Access Control (ReBAC))](#1846-munosabatga-asoslangan-kirish-nazorati-relationship-based-access-control-rebac)
- [18.47 Tokenizatsiya (Tokenization)](#1847-tokenizatsiya-tokenization)
- [18.48 Ma'lumotni maskalash (Data Masking)](#1848-malumotni-maskalash-data-masking)

</details>



Xavfsizlik patternlari - ilovaga kim kirishi mumkin (authentication) va u nima qilishga haqli (authorization) degan ikki savolni tizimli, takrorlanuvchi va auditga yaroqli tarzda hal qiladigan dizayn yechimlari majmuasi. Spring Security aynan shu patternlar ustiga qurilgan: filter chain, delegatsiya qiluvchi manager'lar, pluggable provider'lar va thread'ga bog'langan security context - bularning har biri klassik GoF yoki enterprise pattern'ning aniq ko'rinishi. Arxitektor uchun bu bo'lim muhim, chunki xavfsizlik keyin "qo'shib qo'yiladigan" modul emas: u cross-cutting concern bo'lib, noto'g'ri joylashtirilgan bitta `permitAll()` yoki noto'g'ri tanlangan password encoder butun tizimni ochib qo'yadi. Bundan tashqari xavfsizlik qarorlari (RBAC yoki ABAC, filter darajasida yoki method darajasida tekshirish) keyinchalik o'zgartirish juda qimmat bo'ladigan arxitektura qarorlari hisoblanadi.

## 18.1 Autentifikatsiya va avtorizatsiya ajratilishi (Authentication vs Authorization)

**Tavsif:** Autentifikatsiya - "sen kimsan?" degan savolga javob berib, taqdim etilgan credential'lar (parol, token, sertifikat) asosida principal'ning identity'sini tasdiqlaydi. Avtorizatsiya - "senga ruxsat bormi?" degan savolga javob berib, allaqachon tasdiqlangan identity'ning ma'lum resursga yoki operatsiyaga huquqini tekshiradi. Bu ikki concern'ni qat'iy ajratish Spring Security'ning asosiy arxitektura prinsipi: identity bir marta aniqlanadi va keyin barcha access qarorlari uchun ishonchli manba bo'lib xizmat qiladi. Ajratish tufayli autentifikatsiya mexanizmini (form login → OIDC) avtorizatsiya qoidalariga tegmasdan almashtirish mumkin.

**Spring'da qayerda uchraydi:** Spring Security 6.x'da autentifikatsiya `AuthenticationManager`, `Authentication` va `AuthenticationException` iyerarxiyasi orqali; avtorizatsiya esa `AuthorizationManager<T>`, `AuthorizationDecision` va `AccessDeniedException` orqali ifodalanadi. Konfiguratsiyada ajratish ko'rinadi: `http.formLogin()` / `http.oauth2ResourceServer()` - autentifikatsiya, `http.authorizeHttpRequests()` - avtorizatsiya. Xatolarni ishlovchilar ham ajralgan: `AuthenticationEntryPoint` (401, kim ekanligi aniqlanmagan) va `AccessDeniedHandler` (403, aniqlangan lekin huquqi yo'q).

**Qo'llanish keyslari:**
- Mikroservislar: API gateway JWT'ni validate qilib identity'ni aniqlaydi, downstream servis faqat avtorizatsiya qiladi.
- Bitta ilovada bir nechta login usuli (LDAP, SAML, API key) bo'lsa, avtorizatsiya qoidalari o'zgarmasdan qoladi.
- 401 va 403 javoblarini to'g'ri qaytarish - frontend birinchisida login sahifasiga, ikkinchisida "ruxsat yo'q" ekraniga yo'naltiradi.
- Audit log'da "kim kirdi" va "nimaga urinib ko'rdi" hodisalarini alohida yozish (`AuthenticationSuccessEvent`, `AuthorizationDeniedEvent`).
- Service account'lar uchun autentifikatsiya mTLS orqali, avtorizatsiya esa oddiy RBAC orqali bo'lishi.

**Ehtiyot bo'ling:** Eng ko'p uchraydigan xato - autentifikatsiya qilingan foydalanuvchini avtomatik "ruxsat berilgan" deb hisoblash, ya'ni `authenticated()` bilan cheklanib qolish va resource ownership'ni tekshirmaslik (IDOR zaifligi). Shuningdek 403 o'rniga 401 qaytarish token'ni refresh qilish tsiklini cheksiz aylantirib yuborishi mumkin.

## 18.2 Xavfsizlik filtrlar zanjiri (SecurityFilterChain - Chain of Responsibility)

**Tavsif:** Har bir HTTP so'rov bir qancha mustaqil filter'dan iborat zanjir orqali o'tadi va har bir filter o'z vazifasini bajarib, so'rovni keyingisiga uzatadi yoki zanjirni to'xtatadi. Bu Chain of Responsibility pattern'ining toza ko'rinishi: CSRF tekshiruvi, header yozish, session boshqaruvi, autentifikatsiya va avtorizatsiya bir-biridan ajralgan, tartiblangan bosqichlar bo'ladi. Natijada xavfsizlik logikasi business kod'ga aralashmaydi va yangi concern qo'shish uchun zanjirga bitta filter qo'shish kifoya.

**Spring'da qayerda uchraydi:** Spring Security 6.x'da `SecurityFilterChain` bean'i `HttpSecurity` orqali yaratiladi; `DelegatingFilterProxy` → `FilterChainProxy` servlet container'dan so'rovni qabul qilib mos zanjirga yo'naltiradi. Standart filter'lar: `CsrfFilter`, `SecurityContextHolderFilter`, `UsernamePasswordAuthenticationFilter`, `BearerTokenAuthenticationFilter`, `ExceptionTranslationFilter`, `AuthorizationFilter`. Tartib `SecurityFilterChain` ichida `addFilterBefore` / `addFilterAfter` bilan boshqariladi; bir nechta zanjir `@Order` va `securityMatcher` bilan ajratiladi.

```java
@Bean
SecurityFilterChain api(HttpSecurity http) throws Exception {
    return http.securityMatcher("/api/**")
        .csrf(csrf -> csrf.disable())
        .sessionManagement(s -> s.sessionCreationPolicy(STATELESS))
        .oauth2ResourceServer(o -> o.jwt(Customizer.withDefaults()))
        .authorizeHttpRequests(a -> a.anyRequest().authenticated())
        .build();
}
```

**Qo'llanish keyslari:**
- Stateless REST API va stateful web UI uchun bitta ilovada ikki alohida zanjir qurish.
- Custom API-key filter'ni `UsernamePasswordAuthenticationFilter`'dan oldin joylashtirish.
- Rate limiting yoki tenant resolution'ni filter sifatida zanjirga qo'shish.
- `/actuator/**` uchun alohida, qattiqroq qoidali zanjir yaratish.
- Statik resurslarni zanjirdan butunlay chiqarib performance'ni yaxshilash.

**Ehtiyot bo'ling:** Zanjirlar tartibi qat'iy muhim - kengroq `securityMatcher`'li zanjir birinchi bo'lib kelsa, keyingilari hech qachon ishlamaydi va bu "jim" xavfsizlik teshigi hosil qiladi. Spring Boot 3.x'da `WebSecurityConfigurerAdapter` olib tashlangan, shuning uchun eski tutorial'lardan ko'chirilgan kod kompilyatsiya bo'lmaydi yoki noto'g'ri migratsiya qilinadi.

## 18.3 Autentifikatsiya menejeri va delegatsiya (AuthenticationManager / ProviderManager)

**Tavsif:** `AuthenticationManager` - autentifikatsiya uchun yagona kirish nuqtasi (facade), lekin o'zi hech qanday tekshiruv qilmaydi. Uning asosiy implementatsiyasi `ProviderManager` ro'yxatdagi provider'larni ketma-ket aylanib, so'rov turini qo'llab-quvvatlaydigan birinchi provider'ga ishni topshiradi (delegation + composite). Birinchi muvaffaqiyatli natija qaytariladi; hech biri ishlamasa, oxirgi xato yoki `ProviderNotFoundException` tashlanadi. Bu tuzilish bitta ilovada bir nechta credential turini parallel qo'llab-quvvatlashga imkon beradi.

**Spring'da qayerda uchraydi:** `org.springframework.security.authentication.AuthenticationManager` interfeysi va `ProviderManager` sinfi; `ProviderManager` ichida `List<AuthenticationProvider>` va ixtiyoriy `parent` manager bo'ladi. Konfiguratsiyada `AuthenticationManagerBuilder` yoki Spring Security 6.x'da to'g'ridan-to'g'ri `ProviderManager`'ni bean sifatida e'lon qilish keng tarqalgan. `AuthenticationManagerResolver<HttpServletRequest>` esa so'rovga qarab (masalan tenant yoki issuer bo'yicha) butunlay boshqa manager tanlashga xizmat qiladi.

**Qo'llanish keyslari:**
- DAO (ma'lumotlar bazasi) va LDAP provider'larini bitta manager'da birlashtirish.
- Multi-tenant SaaS'da `AuthenticationManagerResolver` bilan har bir tenant uchun o'z JWT issuer'ini tanlash.
- Programmatic re-authentication: xavfli operatsiya oldidan parolni qayta so'rab, `authenticate()`'ni qo'lda chaqirish.
- Test'larda mock `AuthenticationManager` berib, filter zanjirini izolyatsiyada tekshirish.
- Legacy va yangi identity store'lar o'rtasida bosqichma-bosqich migratsiya qilish.

**Ehtiyot bo'ling:** `eraseCredentials` standart holatda `true` - bu `Authentication` obyektidan parolni tozalaydi, shuning uchun uni keyinchalik downstream'da ishlatishga urinish `null` beradi. Provider'lar tartibi muhim: tezkor bazaviy tekshiruvni sekin tashqi tizimdan oldin qo'ymasa, har bir muvaffaqiyatsiz login tashqi servisga keraksiz yuklanish yaratadi.

## 18.4 Autentifikatsiya provayderi (AuthenticationProvider)

**Tavsif:** `AuthenticationProvider` - ma'lum bir credential turini tekshiruvchi plug-in nuqtasi: u `supports(Class<?>)` orqali o'zi ishlay oladigan `Authentication` turini e'lon qiladi va `authenticate()` ichida haqiqiy tekshiruvni amalga oshiradi. Bu Strategy pattern'ning namunasi - autentifikatsiya algoritmi (parol solishtirish, token verifikatsiya, tashqi IdP'ga murojaat) interfeys ortiga yashiriladi. Muvaffaqiyatda to'liq to'ldirilgan, authority'lari bilan `Authentication` obyekti qaytariladi.

**Spring'da qayerda uchraydi:** `AuthenticationProvider` interfeysi; tayyor implementatsiyalar: `DaoAuthenticationProvider` (`UserDetailsService` + `PasswordEncoder`), `JwtAuthenticationProvider`, `OidcAuthorizationCodeAuthenticationProvider`, `LdapAuthenticationProvider`, `RememberMeAuthenticationProvider`, `PreAuthenticatedAuthenticationProvider`. `AbstractUserDetailsAuthenticationProvider` esa `additionalAuthenticationChecks()` hook'ini ochib beradi - parol tekshiruvi mantig'ini kengaytirish uchun qulay.

**Qo'llanish keyslari:**
- Legacy tizimdagi nostandart hash algoritmi uchun custom provider yozish.
- Bir martalik parol (OTP / TOTP) ni ikkinchi faktor sifatida tekshiruvchi provider qurish.
- SMS yoki magic-link orqali passwordless login amalga oshirish.
- Tashqi HR tizimidan "xodim faolmi" degan qo'shimcha tekshiruvni `additionalAuthenticationChecks()`'ga qo'shish.
- Hardware token yoki mijoz sertifikati (mTLS) asosida identity aniqlash.

**Ehtiyot bo'ling:** `authenticate()` ichida `null` qaytarish "men bu turni qo'llab-quvvatlamayman, keyingisiga o't" degani, `AuthenticationException` tashlash esa "tekshirdim, muvaffaqiyatsiz" degani - bu ikkisini aralashtirib yuborish zanjirni kutilmagan tarzda davom ettiradi yoki to'xtatadi. Shuningdek custom provider'da timing-safe solishtirishdan voz kechish va `UsernameNotFoundException` bilan `BadCredentialsException`'ni tashqariga alohida chiqarish user enumeration zaifligini keltirib chiqaradi.

## 18.5 Foydalanuvchi ma'lumotlari manbasi (UserDetailsService)

**Tavsif:** `UserDetailsService` - username bo'yicha foydalanuvchi ma'lumotlarini (parol hash'i, authority'lar, akkaunt holati) yuklab beradigan yagona metodli abstraksiya. Bu Repository/Adapter pattern bo'lib, Spring Security'ni identity ma'lumotlari qayerda saqlanishidan (SQL, LDAP, NoSQL, tashqi API) butunlay ajratadi. Natijada autentifikatsiya logikasi o'zgarmasdan, ma'lumot manbasini almashtirish mumkin bo'ladi.

**Spring'da qayerda uchraydi:** `org.springframework.security.core.userdetails.UserDetailsService` va uning `loadUserByUsername(String)` metodi; qaytarilgan `UserDetails` (ko'pincha `User.builder()` yoki o'z entity'ingiz). Tayyor implementatsiyalar: `InMemoryUserDetailsManager`, `JdbcUserDetailsManager`, `LdapUserDetailsService`. Kengaytirilgan variantlar: `UserDetailsPasswordService` (parolni avtomatik re-hash qilish uchun) va `UserDetailsChecker` / `AccountStatusUserDetailsChecker` (akkaunt bloklangan yoki muddati o'tganini tekshirish).

**Qo'llanish keyslari:**
- JPA entity'dan foydalanuvchi va uning rollarini yuklab, `UserDetails`'ga map qilish.
- `@Transactional(readOnly = true)` bilan rollarni bitta `JOIN FETCH` so'rovida olish (N+1'dan qochish).
- OAuth2 Login'da tashqi IdP'dan kelgan foydalanuvchini lokal profil bilan birlashtirish (`OidcUserService` kengaytmasi).
- Faol bo'lmagan yoki muzlatilgan akkauntlarni `isEnabled()` / `isAccountNonLocked()` orqali bloklash.
- Test uchun `InMemoryUserDetailsManager` bilan tezkor fixture tayyorlash.

**Ehtiyot bo'ling:** Foydalanuvchi topilmasa `null` qaytarmaslik kerak - `UsernameNotFoundException` tashlang, aks holda `NullPointerException` yoki tushunarsiz xatolar chiqadi. `loadUserByUsername` har bir so'rovda chaqirilishi mumkin, shuning uchun og'ir so'rovlar yoki `LazyInitializationException` muammosiga aylanadigan lazy collection'lar bilan ehtiyot bo'ling; stateless JWT arxitekturasida esa bu servisni umuman chaqirish ortiqcha bo'lishi mumkin.

## 18.6 Xavfsizlik konteksti egasi (SecurityContextHolder - Thread-Specific Storage)

**Tavsif:** Hozirgi autentifikatsiyalangan principal'ni har bir metodga parametr sifatida uzatmaslik uchun u thread'ga bog'langan ambient holatda saqlanadi. `SecurityContextHolder` odatda `ThreadLocal` ichida `SecurityContext`'ni ushlab turadi va ilovaning har qanday qatlamidan "hozir kim ishlayapti" degan savolga javob beradi. Bu Thread-Specific Storage (Context Object) pattern - qulaylik beradi, lekin yashirin global holat hisoblanadi.

**Spring'da qayerda uchraydi:** `SecurityContextHolder`, `SecurityContext`, `Authentication`; strategiyalar: `MODE_THREADLOCAL` (standart), `MODE_INHERITABLETHREADLOCAL`, `MODE_GLOBAL`. Spring Security 6.x'da kontekstni so'rovlar orasida saqlash `SecurityContextRepository` (`HttpSessionSecurityContextRepository`, `RequestAttributeSecurityContextRepository`) va `SecurityContextHolderFilter` orqali boshqariladi. Async uchun `DelegatingSecurityContextExecutor`, `DelegatingSecurityContextAsyncTaskExecutor`, `@EnableAsync` bilan birga ishlatiladi; reactive stack'da esa o'rniga `ReactiveSecurityContextHolder` va Reactor Context ishlatiladi.

**Qo'llanish keyslari:**
- Audit maydonlarini (`createdBy`, `updatedBy`) `AuditorAware` orqali avtomatik to'ldirish.
- Service qatlamida hozirgi foydalanuvchi ID'si bo'yicha ma'lumotni filtrlash (multi-tenancy).
- `@AuthenticationPrincipal` bilan controller metodiga principal'ni to'g'ridan-to'g'ri inject qilish.
- `@Async` task'larga kontekstni ko'chirish uchun delegating executor sozlash.
- Log'larga MDC orqali username qo'shib, so'rovlarni kuzatish.

**Ehtiyot bo'ling:** `ThreadLocal` yangi thread'ga avtomatik ko'chmaydi - `@Async`, `CompletableFuture`, virtual thread'lar yoki o'z thread pool'ingizda kontekst `null` bo'lib chiqadi va tekshiruvlar jim o'tib ketadi. Bundan tashqari Spring Security 6.x'da kontekst endi avtomatik session'ga saqlanmaydi: `SecurityContextHolder.setContext()` dan keyin `SecurityContextRepository.saveContext()` chaqirilmasa, login keyingi so'rovda yo'qoladi.

## 18.7 Parol hash'lash va yangilanuvchan kodlash (Password hashing - DelegatingPasswordEncoder, upgradable encoding)

**Tavsif:** Parollar hech qachon ochiq yoki qaytariladigan shaklda saqlanmasligi kerak; ular sekin, salt'li, hisoblash jihatidan qimmat one-way funksiya bilan hash qilinadi. `DelegatingPasswordEncoder` hash qiymatining oldiga `{bcrypt}`, `{argon2}` kabi prefix qo'yib, bir vaqtning o'zida bir nechta algoritmni qo'llab-quvvatlaydi: tekshiruvda prefix bo'yicha mos encoder tanlanadi, yangi parollar esa faqat joriy standart bilan kodlanadi. Bu Strategy + Adapter kombinatsiyasi algoritmni to'xtatmasdan migratsiya qilishga imkon beradi.

**Spring'da qayerda uchraydi:** `PasswordEncoder` interfeysi; `PasswordEncoderFactories.createDelegatingPasswordEncoder()`; implementatsiyalar `BCryptPasswordEncoder`, `Argon2PasswordEncoder`, `Pbkdf2PasswordEncoder`, `SCryptPasswordEncoder`. Avtomatik yangilash uchun `PasswordEncoder.upgradeEncoding()` va `UserDetailsPasswordService` birgalikda ishlaydi: muvaffaqiyatli login paytida `DaoAuthenticationProvider` eski hash'ni yangi algoritm bilan qayta yozadi. Spring Security 6.x'da `NoOpPasswordEncoder` deprecated va faqat test uchun.

**Qo'llanish keyslari:**
- Legacy MD5/SHA-1 hash'lardan bcrypt yoki Argon2id'ga foydalanuvchini bezovta qilmasdan o'tish.
- `UserDetailsPasswordService` bilan login paytida hash'ni jim yangilash (upgradable encoding).
- Bcrypt strength'ni (masalan 10 → 12) server quvvati oshgani sayin ko'tarish.
- Parol tiklash va ro'yxatdan o'tish flow'larida bitta markaziy encoder bean'idan foydalanish.
- Test profilida tez, production'da qimmat parametrlarni ishlatib CI vaqtini qisqartirish.

**Ehtiyot bo'ling:** Hash'ni o'zingiz `equals()` bilan solishtirmang - faqat `matches()` ishlatilsin, aks holda timing attack va salt bilan ishlash xatolari paydo bo'ladi. Bcrypt 72 bayt'dan keyingi matnni jim kesib tashlaydi, shuning uchun uzun passphrase'lar yoki "pepper" qo'shish sxemalarida bu cheklovni hisobga olmaslik xavfsizlikni kutilganidan past qiladi.

## 18.8 Rolga asoslangan kirish nazorati (Role-Based Access Control - RBAC)

**Tavsif:** Ruxsatlar foydalanuvchiga to'g'ridan-to'g'ri emas, balki rol (yoki authority) orqali beriladi: foydalanuvchi → rol → ruxsatlar. Bu indirection ruxsatlarni boshqarishni soddalashtiradi, chunki yuzlab foydalanuvchi o'rniga bir nechta rolni tahrirlash kifoya. Spring Security'da rollar `GrantedAuthority` ro'yxati sifatida `Authentication` ichida tashiladi va avtorizatsiya qarorlari shu ro'yxat asosida qabul qilinadi.

**Spring'da qayerda uchraydi:** `GrantedAuthority`, `SimpleGrantedAuthority`, `AuthorityUtils`; konfiguratsiyada `authorizeHttpRequests(a -> a.requestMatchers("/admin/**").hasRole("ADMIN"))` yoki `hasAuthority("SCOPE_orders:read")`. `hasRole("X")` avtomatik `ROLE_` prefix qo'shadi - bu prefix `GrantedAuthorityDefaults` bean'i bilan o'zgartiriladi. Rol iyerarxiyasi uchun `RoleHierarchy` / `RoleHierarchyImpl` (6.3+ da `RoleHierarchyImpl.withDefaultRolePrefix()` builder'i) `AuthorizationManager`'ga ulanadi. JWT'dan authority ajratish `JwtGrantedAuthoritiesConverter` orqali.

**Qo'llanish keyslari:**
- Admin panelini `/admin/**` yo'llari uchun `ROLE_ADMIN` bilan yopish.
- `ROLE_ADMIN > ROLE_MANAGER > ROLE_USER` iyerarxiyasini `RoleHierarchy` bilan e'lon qilish.
- OAuth2 resource server'da scope'larni `SCOPE_` authority'lariga map qilish.
- Keycloak yoki Entra ID'dan kelgan group claim'larini lokal rollarga konvertatsiya qilish.
- Read-only auditor roli yaratib, barcha GET endpoint'larga ruxsat berish.

**Ehtiyot bo'ling:** `hasRole("ROLE_ADMIN")` yozish `ROLE_ROLE_ADMIN` degan mavjud bo'lmagan authority'ga aylanadi va tekshiruv doim `false` qaytaradi - bu klassik tuzoq. RBAC "role explosion"ga moyil: `ROLE_MANAGER_REGION_EU_READONLY` kabi nomlar paydo bo'lsa, bu ABAC'ga o'tish vaqti kelganining signali.

## 18.9 Atribut va siyosatga asoslangan kirish nazorati (Attribute-Based / Policy-Based Access Control - ABAC)

**Tavsif:** Qaror faqat rolga emas, balki subject (kim), resource (nima), action (qanday amal) va environment (qachon, qaysi IP) atributlariga asoslangan siyosat orqali qabul qilinadi. Bu RBAC'ning kombinatorik portlashini hal qiladi: "menejer faqat o'z bo'limi hujjatini ish vaqtida tahrirlashi mumkin" kabi qoida bitta policy bilan ifodalanadi. Spring Security 6.x'da bu Strategy pattern'ning umumlashtirilgan ko'rinishi - `AuthorizationManager` istalgan atributni hisobga oluvchi mantiq bilan almashtirilishi mumkin.

**Spring'da qayerda uchraydi:** `AuthorizationManager<T>` funksional interfeysi va `AuthorizationDecision`; `access(AuthorizationManager)` bilan `authorizeHttpRequests`'ga ulanadi, `AuthorizationManagers.allOf/anyOf` bilan kompozitsiya qilinadi. Ma'lumot darajasidagi ABAC uchun `@PreAuthorize` + `PermissionEvaluator` yoki Spring Security ACL moduli (`AclPermissionEvaluator`, `MutableAclService`). Tashqi policy engine'lar: Open Policy Agent (OPA) yoki Cerbos - ularni HTTP client bilan `AuthorizationManager` ichidan chaqirish keng tarqalgan yondashuv; Spring Data bilan birgalikda row-level filtrlash uchun Hibernate `@Filter` ishlatiladi.

**Qo'llanish keyslari:**
- Multi-tenant SaaS'da foydalanuvchi faqat o'z tenant'i ma'lumotini ko'rishini ta'minlash.
- Hujjat egasi (`document.ownerId == principal.id`) bo'lsa tahrirlashga ruxsat berish.
- Moliyaviy tranzaksiyani summa va foydalanuvchi limiti asosida tasdiqlash.
- Maxfiylik darajasi (`CONFIDENTIAL`) va xodim clearance darajasini solishtirish.
- IP range yoki ish vaqti bo'yicha admin operatsiyalarini cheklash.

**Ehtiyot bo'ling:** ABAC qarorlari ko'pincha ma'lumotni bazadan yuklashni talab qiladi - buni har bir obyekt uchun qilish N+1 so'rovga va sezilarli latency'ga olib keladi, shuning uchun collection'lar uchun post-filtering o'rniga query darajasida filtrlash afzal. Siyosatlar kod bo'ylab tarqalib ketsa, ularni audit qilish imkonsiz bo'ladi: policy'ni markazlashtirib, albatta test bilan qoplang.

## 18.10 Metod darajasidagi xavfsizlik (Method Security - @PreAuthorize, @PostAuthorize)

**Tavsif:** Xavfsizlik tekshiruvi HTTP yo'liga emas, balki business metodining o'ziga bog'lanadi: metod chaqirilishidan oldin (`@PreAuthorize`) yoki natija qaytarilgandan keyin (`@PostAuthorize`) qoida baholanadi. Bu Interceptor/Proxy pattern orqali ishlaydi - Spring AOP metod atrofida advice yaratib, ruxsat bo'lmasa `AccessDeniedException` tashlaydi. Natijada bitta servis metodi REST, scheduled job yoki message listener'dan chaqirilganda ham bir xil himoyalanadi (defence in depth).

**Spring'da qayerda uchraydi:** `@EnableMethodSecurity` (Spring Security 6.x; eski `@EnableGlobalMethodSecurity` deprecated) va annotatsiyalar `@PreAuthorize`, `@PostAuthorize`, `@PreFilter`, `@PostFilter`, hamda JSR-250 `@RolesAllowed` / `@Secured`. Ichki mexanizm: `AuthorizationManagerBeforeMethodInterceptor`, `PreAuthorizeAuthorizationManager`, `MethodSecurityExpressionHandler`. 6.3+ da `@AuthorizeReturnObject` va meta-annotatsiya shablonlari (`@PreAuthorize("hasRole('{role}')")`) qo'llab-quvvatlanadi.

```java
@PreAuthorize("hasRole('MANAGER') and #order.branchId == principal.branchId")
public void approve(Order order) { /* ... */ }

@PostAuthorize("returnObject.ownerId == authentication.name")
public Document findById(Long id) { /* ... */ }
```

**Qo'llanish keyslari:**
- Service qatlamidagi `deleteAccount()` kabi xavfli metodlarni rol bilan yopish.
- `@PostAuthorize` bilan qaytarilgan obyekt egasini tekshirib IDOR'dan himoyalanish.
- `@PostFilter` bilan ro'yxatdan ruxsatsiz elementlarni olib tashlash (kichik collection'lar uchun).
- Repository metodlariga annotatsiya qo'yib, barcha caller'lar uchun bir xil qoida o'rnatish.
- Meta-annotatsiya (`@IsTenantAdmin`) yaratib, SpEL takrorlanishini kamaytirish.

**Ehtiyot bo'ling:** Annotatsiyalar Spring AOP proxy orqali ishlaydi - xuddi shu bean ichidagi `this.method()` chaqiruvi proxy'ni chetlab o'tadi va tekshiruv umuman bajarilmaydi; shuningdek `private` yoki `final` metodlarda proxy ishlamaydi. `@PostAuthorize` metod allaqachon bajarilgandan keyin ishlaydi, demak yozuv operatsiyasi `@Transactional` ichida bo'lsa ham side-effect sodir bo'lib, faqat exception tufayli rollback'ga tayanadi - bu ishonchsiz pattern.

## 18.11 Ifodaga asoslangan xavfsizlik (Expression-based security - SpEL)

**Tavsif:** Ruxsat qoidalari imperativ `if` bloklari o'rniga deklarativ ifoda (Spring Expression Language) sifatida yoziladi va runtime'da maxsus kontekstda baholanadi. Bu Interpreter pattern: ifodalar bir marta parse qilinib, `authentication`, `principal`, metod argumentlari va qaytarilgan obyektga kirish huquqi bilan evaluate qilinadi. Natijada murakkab qoidalarni kompakt, o'qiydigan va konfiguratsiyaga chiqarish mumkin shaklda ifodalash imkoni paydo bo'ladi.

**Spring'da qayerda uchraydi:** `SecurityExpressionRoot` va `MethodSecurityExpressionOperations` taqdim etadigan funksiyalar: `hasRole`, `hasAnyAuthority`, `permitAll`, `denyAll`, `isAuthenticated`, `hasPermission`, `authentication`, `principal`, hamda `#argName` va `returnObject` o'zgaruvchilari. Kengaytirish nuqtalari: `DefaultMethodSecurityExpressionHandler` (custom root obyekt yoki `PermissionEvaluator` ulash uchun) va `DefaultHttpSecurityExpressionHandler`. Web tomonda `WebExpressionAuthorizationManager("hasRole('ADMIN') and hasIpAddress('10.0.0.0/8')")` ifodani `authorizeHttpRequests`'ga bog'laydi; `@bean.method(...)` sintaksisi orqali o'z bean'ingizdagi metodga ham murojaat qilish mumkin.

**Qo'llanish keyslari:**
- `@PreAuthorize("@documentGuard.canEdit(#id, authentication)")` bilan logikani oddiy, testlanadigan bean'ga ko'chirish.
- Metod argumenti bilan principal'ni solishtirib ownership tekshiruvi (`#userId == principal.id`).
- IP va rolni birlashtirgan qoidalarni `hasIpAddress` bilan yozish.
- ACL moduli bilan `hasPermission(#doc, 'WRITE')` chaqirig'ini ishlatish.
- Meta-annotatsiya shablonlari orqali takrorlanuvchi ifodalarni bitta joyda saqlash.

**Ehtiyot bo'ling:** SpEL string'lari kompilyatsiyada tekshirilmaydi - xato yozilgan property yoki rol nomi faqat runtime'da, ko'pincha production'da ma'lum bo'ladi, shuning uchun har bir ifoda integration test bilan qoplanishi shart. Ifodalarga hech qachon foydalanuvchi kiritgan matnni konkatenatsiya qilmang (expression injection) va murakkab mantiqni ifoda ichiga tiqishtirmasdan, `@bean.method()` yoki `PermissionEvaluator`'ga chiqaring; shuningdek metod argument nomlari uchun `-parameters` kompilyator flag'i yoqilganiga ishonch hosil qiling.

## 18.12 Avtorizatsiya kodi + PKCE (OAuth2 Authorization Code + PKCE)

**Tavsif:** Foydalanuvchi nomidan access token olishning eng xavfsiz oqimi: client foydalanuvchini authorization server'ga yuboradi, qaytib kelgan qisqa muddatli `code`ni token'ga almashtiradi. PKCE (Proof Key for Code Exchange) tasodifiy `code_verifier` yaratib, uning SHA-256 hash'ini (`code_challenge`) birinchi so'rovda yuboradi, token almashishda esa asl verifier'ni ko'rsatadi. Shu bilan o'g'irlangan authorization code boshqa tomonidan ishlatib bo'lmaydi. Bugungi kunda PKCE public client'lar (SPA, mobil) uchun majburiy, confidential client'lar uchun ham tavsiya etiladi.

**Spring'da qayerda uchraydi:** `spring-boot-starter-oauth2-client` moduli, `spring.security.oauth2.client.registration.*` konfiguratsiyasi va `ClientRegistration` / `ClientRegistrationRepository` abstraksiyalari. Oqimni `HttpSecurity.oauth2Login()` yoki `oauth2Client()` yoqadi; ichida `OAuth2AuthorizationRequestRedirectFilter`, `OAuth2LoginAuthenticationFilter` va `DefaultAuthorizationCodeTokenResponseClient` (Spring Security 6.4+ dan `RestClientAuthorizationCodeTokenResponseClient`) ishlaydi. Spring Security 6.x'da public client uchun PKCE avtomatik qo'shiladi, confidential client uchun esa `OAuth2AuthorizationRequestCustomizers.withPkce()`ni `DefaultOAuth2AuthorizationRequestResolver`ga ulash kerak.

**Qo'llanish keyslari:**
- Angular/React SPA foydalanuvchini Keycloak orqali login qilib, backend API'ga token bilan murojaat qiladi.
- Korporativ xodimlar portali Microsoft Entra ID (Azure AD) hisobi bilan tizimga kiradi.
- Mobil ilova native browser (AppAuth) orqali login qilib, client secret saqlashdan qutuladi.
- BFF (Backend-for-Frontend) Spring Boot ilovasi `oauth2Login()` bilan kodni token'ga almashtirib, token'ni session'da ushlab turadi.
- SaaS mahsulotda "Google bilan kirish" tugmasi orqali ro'yxatdan o'tish.

**Ehtiyot bo'ling:** `redirect-uri`ni wildcard yoki ochiq redirect qilib qo'yish eng katta xato - faqat aniq, oldindan ro'yxatga olingan URI ishlatiladi va `state` parametri CSRF uchun hamisha tekshirilishi shart. PKCE implicit flow'ni o'rnini bosadi; implicit va password grant'lardan butunlay voz kechish kerak, hamda access token'ni brauzerda `localStorage`da saqlash XSS orqali o'g'irlanish riskini keltiradi.

## 18.13 Client Credentials oqimi (OAuth2 Client Credentials)

**Tavsif:** Foydalanuvchi ishtirokisiz, xizmat o'z nomidan (machine-to-machine) token oladigan oqim: client o'z `client_id`/`client_secret` yoki JWT assertion bilan token endpoint'ga boradi va access token qaytaradi. Bu oqimda hech qanday resource owner yo'q, shuning uchun refresh token ham berilmaydi - token tugasa, yangisi so'raladi. Scope'lar orqali xizmatning imkoniyatlari toraytiriladi.

**Spring'da qayerda uchraydi:** `ClientRegistration` da `authorization-grant-type: client_credentials` ko'rsatiladi; token olishni `OAuth2AuthorizedClientManager` (`AuthorizedClientServiceOAuth2AuthorizedClientManager` - servlet, `AuthorizedClientServiceReactiveOAuth2AuthorizedClientManager` - reactive) boshqaradi. `RestClient` uchun `OAuth2ClientHttpRequestInterceptor`, `WebClient` uchun `ServletOAuth2AuthorizedClientExchangeFilterFunction` yoki `ServerOAuth2AuthorizedClientExchangeFilterFunction` token'ni `Authorization: Bearer` sarlavhasiga avtomatik qo'shadi. Spring Security 7.x / Boot 4.x'da `OAuth2ClientHttpRequestInterceptor` va deklarativ HTTP interface (`@HttpExchange`) bilan integratsiya soddalashgan.

**Qo'llanish keyslari:**
- Batch job kechasi hisobot xizmatining REST API'siga token bilan murojaat qiladi.
- Mikroservis ichki `payment-service`ga foydalanuvchi kontekstisiz texnik so'rov yuboradi.
- Kafka consumer qayta ishlangan event bo'yicha tashqi partner API'ga xabar beradi.
- CI/CD pipeline deploy tugagach monitoring tizimining API'siga marker yozadi.
- Legacy cron skript o'rniga Spring Boot scheduler SAP integratsiya API'siga ulanadi.

**Ehtiyot bo'ling:** Client credentials token'ida foydalanuvchi identifikatori yo'q - shuning uchun uni foydalanuvchi huquqlarini tekshirish uchun ishlatish (masalan, "admin xizmat token'i bor, demak hammasi mumkin") jiddiy avtorizatsiya teshigi. Secret'ni `application.yml`da ochiq saqlamang; Vault, Kubernetes Secret yoki mTLS/`private_key_jwt` client autentifikatsiyasini afzal ko'ring.

## 18.14 Resource Server (OAuth2 Resource Server (JWT / opaque))

**Tavsif:** API'ni kelgan access token asosida himoyalash patterni: har bir so'rovda `Authorization: Bearer` token tekshiriladi va natijada `Authentication` obyekti hosil bo'ladi. Ikki variant bor - JWT token'ni lokal ravishda imzo (JWK Set) bo'yicha tekshirish yoki opaque token'ni authorization server'ning introspection endpoint'iga yuborish. JWT variant tez va stateless, opaque variant esa darhol bekor qilish (revocation) imkonini beradi.

**Spring'da qayerda uchraydi:** `spring-boot-starter-oauth2-resource-server`, `HttpSecurity.oauth2ResourceServer(oauth2 -> oauth2.jwt(...))` yoki `.opaqueToken(...)`. JWT uchun `JwtDecoder` (`NimbusJwtDecoder`), `spring.security.oauth2.resourceserver.jwt.issuer-uri` yoki `jwk-set-uri`, scope'larni rolga o'girish uchun `JwtAuthenticationConverter` + `JwtGrantedAuthoritiesConverter`. Opaque uchun `OpaqueTokenIntrospector` (`SpringOpaqueTokenIntrospector`) va `...resourceserver.opaquetoken.introspection-uri`. Reactive tomonda `ReactiveJwtDecoder`, `BearerTokenAuthenticationFilter` esa token'ni ajratib oladi; `@AuthenticationPrincipal Jwt jwt` bilan claim'larga kirish mumkin.

**Qo'llanish keyslari:**
- Mikroservis arxitekturasida har bir service gateway'dan kelgan JWT'ni mustaqil tekshiradi.
- Mobil ilovaga xizmat qiluvchi public REST API `@PreAuthorize("hasAuthority('SCOPE_orders.read')")` bilan himoyalanadi.
- Ko'p tenant'li SaaS'da `issuer-uri` bo'yicha dinamik tenant aniqlash (`JwtIssuerAuthenticationManagerResolver`).
- Partner integratsiyasi uchun opaque token ishlatilib, shartnoma bekor qilinsa token darhol ishlamay qoladi.
- Gateway orqasidagi gRPC/REST service `audience` claim'ini tekshirib, boshqa API uchun berilgan token'ni rad etadi.

**Ehtiyot bo'ling:** Faqat imzoni tekshirish yetarli emas - `iss`, `aud`, `exp` va kerak bo'lsa `azp` claim'lari ham validator orqali tekshirilishi shart (`JwtValidators.createDefaultWithIssuer(...)` + `OAuth2TokenValidator` zanjiri). JWT'ni stateless tekshirish token'ni muddatidan oldin bekor qilishni imkonsiz qiladi, shuning uchun token amal qilish muddatini qisqa (5-15 daqiqa) tutish kerak.

## 18.15 Token introspeksiyasi (Token Introspection)

**Tavsif:** RFC 7662 bo'yicha resource server token'ning haqiqiyligi va metadata'sini authorization server'dan so'rab oladigan pattern. Introspection endpoint `active: true/false`, `scope`, `sub`, `exp`, `client_id` kabi maydonlarni qaytaradi va shu orqali opaque token'lar ham, kerak bo'lsa JWT'lar ham real vaqtda tekshiriladi. Bu bekor qilingan token'ni darhol bloklash imkonini beradi, lekin har so'rovda tashqi chaqiruv qo'shadi.

**Spring'da qayerda uchraydi:** `oauth2ResourceServer().opaqueToken()` va `OpaqueTokenIntrospector` interfeysi; standart amalga oshirish `SpringOpaqueTokenIntrospector` (reactive: `SpringReactiveOpaqueTokenIntrospector`), natijasi `BearerTokenAuthentication` + `OAuth2AuthenticatedPrincipal`. Konfiguratsiya: `spring.security.oauth2.resourceserver.opaquetoken.introspection-uri`, `client-id`, `client-secret`. O'z rol mapping'i yoki caching uchun `OpaqueTokenIntrospector`ni o'rab (delegate) `@Bean` qilib e'lon qilinadi; Spring Authorization Server tomonida esa `OAuth2TokenIntrospectionEndpointFilter` xizmat qiladi.

**Qo'llanish keyslari:**
- Bank API'si token bekor qilinganda (logout, firibgarlik shubhasi) ruxsatni bir zumda to'xtatishi kerak.
- Legacy authorization server faqat opaque token beradi, JWK Set yo'q.
- API gateway tokenni bir marta introspect qilib, orqadagi xizmatlarga ishonchli kontekst uzatadi.
- Compliance talabi bo'yicha har bir token ishlatilishi markazdan audit qilinishi kerak.
- Qisqa muddatli sessiyalarni darhol o'chirish zarur bo'lgan admin panel.

**Ehtiyot bo'ling:** Introspection har so'rovda tarmoq chaqiruvi qiladi - caching (Caffeine, Redis) qo'yilmasa, authorization server bottleneck va single point of failure bo'ladi; cache TTL'i token'ning qolgan `exp`idan oshmasligi kerak. Shuningdek introspection javobini log'ga to'liq yozish token metadata'si va `sub`ni sizdirib qo'yadi.

## 18.16 Token uzatish (Token Relay)

**Tavsif:** Foydalanuvchining access token'ini qabul qilgan xizmat uni pastdagi (downstream) xizmatlarga o'zgartirmasdan yoki almashtirib uzatish patterni. Shu orqali foydalanuvchi identifikatori va scope'lari butun chaqiruv zanjiri bo'ylab saqlanadi va har bir xizmat mustaqil avtorizatsiya qila oladi. Xavfsizroq varianti - RFC 8693 Token Exchange: har bir hop uchun `audience` toraytirilgan yangi token olinadi.

**Spring'da qayerda uchraydi:** Spring Cloud Gateway'da `TokenRelay` filtri (`spring.cloud.gateway.routes[].filters: - TokenRelay=`); ilova ichida `ServletOAuth2AuthorizedClientExchangeFilterFunction`/`ServerOAuth2AuthorizedClientExchangeFilterFunction` yoki `OAuth2ClientHttpRequestInterceptor` orqali `RestClient`/`WebClient`ga token qo'shiladi. Spring Security 6.3+ `token-exchange` grant type va `TokenExchangeOAuth2AuthorizedClientProvider`ni qo'llab-quvvatlaydi, shuningdek `JwtBearerOAuth2AuthorizedClientProvider` ham mavjud. Reactive zanjirda token kontekstini saqlash uchun `ReactiveSecurityContextHolder` ishlatiladi.

**Qo'llanish keyslari:**
- Gateway brauzerdan kelgan token'ni `order-service` va `billing-service`ga uzatadi.
- BFF session'dagi token'ni downstream API chaqiruvlarida qayta ishlatadi.
- Token Exchange bilan `api-gateway` token'ini `audience: internal-ledger` token'iga almashtiradi.
- Audit talabi bo'lgan tizimda har bir servis log'ida bir xil `sub` ko'rinishi uchun.
- Reactive WebFlux zanjirida foydalanuvchi kontekstini saqlab pastdagi xizmatni chaqirish.

**Ehtiyot bo'ling:** Token'ni "hamma joyga" uzatish eng keng tarqalgan xato - tashqi yoki kam ishonchli xizmatga uzatilgan token o'g'irlansa, butun foydalanuvchi huquqlari bilan ishlatiladi; `audience`ni toraytirish yoki Token Exchange afzal. Shuningdek `@Async` yoki yangi thread'da `SecurityContext` yo'qoladi - `DelegatingSecurityContextExecutor`siz token relay ishlamaydi.

## 18.17 Refresh token aylanishi (Refresh Token Rotation)

**Tavsif:** Refresh token har ishlatilganda yangisi berilib, oldingisi bekor qilinadi. Agar bekor qilingan (ishlatilgan) refresh token qayta kelsa, bu o'g'irlanish belgisi sanalib, butun token oilasi (token family) bekor qilinadi. Bu uzoq muddatli refresh token'ni saqlash riskini kamaytiradi va public client'lar uchun ayniqsa muhim.

**Spring'da qayerda uchraydi:** Spring Authorization Server tomonida `TokenSettings.builder().reuseRefreshTokens(false)` rotation'ni yoqadi; token'lar `OAuth2AuthorizationService` (`JdbcOAuth2AuthorizationService` yoki `InMemoryOAuth2AuthorizationService`) orqali saqlanadi va `OAuth2RefreshTokenAuthenticationProvider` almashishni bajaradi. Client tomonida `RefreshTokenOAuth2AuthorizedClientProvider` (`OAuth2AuthorizedClientProviderBuilder.builder().refreshToken()`) token muddati tugashidan oldin avtomatik yangilaydi; yangilangan client `OAuth2AuthorizedClientRepository`/`OAuth2AuthorizedClientService`ga saqlanadi.

```java
TokenSettings settings = TokenSettings.builder()
    .reuseRefreshTokens(false)
    .accessTokenTimeToLive(Duration.ofMinutes(10))
    .refreshTokenTimeToLive(Duration.ofDays(14))
    .build();
```

**Qo'llanish keyslari:**
- Mobil bank ilovasi foydalanuvchini har kuni login qilishga majburlamasdan xavfsizlikni saqlaydi.
- PKCE ishlatuvchi SPA refresh token'ni rotation bilan ishlatadi (cookie ichida).
- O'g'irlangan qurilma aniqlanganda token oilasini bekor qilib, barcha sessiyani uzish.
- Ko'p qurilmali hisobda har bir qurilma alohida token family'ga ega bo'ladi.
- Uzoq muddatli integratsiyalarda secret aylanishini avtomatlashtirish.

**Ehtiyot bo'ling:** Rotation'da race condition real muammo - bir vaqtda ikki so'rov bir refresh token'ni ishlatsa, biri "o'g'irlanish" deb qarab sessiyani uzadi; shuning uchun client tomonda refresh chaqiruvini serializatsiya qilish (lock/single-flight) kerak. Shuningdek refresh token'ni `localStorage`da saqlash rotation foydasini yo'qotadi - `HttpOnly`, `Secure`, `SameSite` cookie ishlatish kerak.

## 18.18 OpenID Connect (OpenID Connect)

**Tavsif:** OAuth2 ustiga qurilgan identifikatsiya qatlami: access token'dan tashqari `id_token` (imzolangan JWT) beriladi va unda foydalanuvchi haqidagi claim'lar (`sub`, `email`, `name`, `nonce`) bo'ladi. OAuth2 avtorizatsiya uchun, OIDC esa autentifikatsiya uchun - ya'ni "bu foydalanuvchi kim" savoliga standart javob. Qo'shimcha ma'lumotlar `UserInfo` endpoint'idan olinadi, provayder metadata'si `/.well-known/openid-configuration` orqali topiladi.

**Spring'da qayerda uchraydi:** `HttpSecurity.oauth2Login()` scope'da `openid` bo'lsa OIDC rejimida ishlaydi; natijada principal `OidcUser` (`DefaultOidcUser`), uning ichida `OidcIdToken` va `OidcUserInfo` bo'ladi. `OidcUserService`, `OidcIdTokenDecoderFactory`, `OidcAuthorizationCodeAuthenticationProvider` asosiy sinflar; logout uchun `OidcClientInitiatedLogoutSuccessHandler` (reactive: `OidcClientInitiatedServerLogoutSuccessHandler`) va back-channel logout uchun `OidcBackChannelLogoutFilter` (Spring Security 6.2+). Konfiguratsiya `spring.security.oauth2.client.provider.<id>.issuer-uri` bilan metadata'ni avtomatik yuklaydi.

**Qo'llanish keyslari:**
- Korporativ SSO: xodim bir marta Entra ID'ga kirib, barcha ichki ilovalarga kiradi.
- Kirish sahifasida "Google / Apple bilan davom etish" tugmalari.
- `OidcUser` claim'laridan foydalanuvchi profili (ism, avatar) olib UI'da ko'rsatish.
- Back-channel logout bilan IdP'dan chiqilganda barcha ilovalardagi sessiyani yopish.
- `groups` yoki `roles` claim'ini Spring Security authority'lariga o'girib RBAC qurish.

**Ehtiyot bo'ling:** `id_token` autentifikatsiya natijasi - uni API'ga access token sifatida yuborish noto'g'ri va keng tarqalgan xato; API uchun access token ishlatiladi. `nonce` tekshiruvi va `at_hash` validatsiyasini o'chirib qo'ymang, shuningdek `email` claim'ini yagona identifikator sifatida ishlatish xavfli - `sub` + `iss` juftligi barqaror kalit.

## 18.19 Spring Authorization Server (Spring Authorization Server)

**Tavsif:** Spring'ning o'z authorization server amalga oshirishi: OAuth2.1 va OIDC 1.0 spetsifikatsiyalarini qo'llab-quvvatlaydigan, Spring Security ustiga qurilgan mustaqil loyiha. U token endpoint, authorization endpoint, JWK Set, introspection, revocation, device authorization va OIDC discovery endpoint'larini beradi. Deprecated bo'lgan Spring Security OAuth loyihasining o'rnini bosadi va o'z client/token saqlashini to'liq moslashtirish mumkin.

**Spring'da qayerda uchraydi:** `spring-boot-starter-oauth2-authorization-server` (Spring Authorization Server 1.x/2.x). Asosiy konfiguratsiya `OAuth2AuthorizationServerConfiguration.applyDefaultSecurity(http)` yoki `OAuth2AuthorizationServerConfigurer`; asosiy bean'lar - `RegisteredClientRepository` (`JdbcRegisteredClientRepository`), `OAuth2AuthorizationService`, `OAuth2AuthorizationConsentService`, `JWKSource<SecurityContext>` va `AuthorizationServerSettings`. Token tarkibini `OAuth2TokenCustomizer<JwtEncodingContext>` bilan o'zgartiriladi; `RegisteredClient` ichida `ClientSettings` va `TokenSettings` sozlanadi.

**Qo'llanish keyslari:**
- Keycloak/Auth0'ga tashqi bog'liqlikni xohlamagan korporativ IdP qurish.
- Faqat ichki mikroservislar uchun yengil token server kerak bo'lgan platforma.
- Token claim'lariga tenant, branch yoki xodim ID'sini qo'shish talab qilinadi.
- On-premise, air-gapped muhitda litsenziyasiz OAuth2 server joylash.
- Legacy Spring Security OAuth (`AuthorizationServerConfigurerAdapter`) loyihasini migratsiya qilish.

**Ehtiyot bo'ling:** Authorization server - xavfsizlikning eng kritik komponenti: signing key'ni kodga qo'shib qo'yish yoki har restart'da yangi RSA kalit generatsiya qilish (in-memory `JWKSource`) production'da barcha token'larni buzadi - kalitni KMS/Vault/keystore'da saqlab, rotation qo'yish kerak. Shuningdek `InMemory*` repository va service'lar faqat demo uchun; klasterda JDBC yoki Redis asosidagi saqlash shart.

## 18.20 Federatsiyalangan identifikatsiya (Federated Identity)

**Tavsif:** Autentifikatsiyani tashqi identity provider'ga ishonib topshirish va bir nechta provayderni yagona ichki identifikatorga bog'lash patterni. Ilova parol saqlamaydi; o'rniga SAML, OIDC yoki LDAP orqali kelgan tasdiqni qabul qilib, local user yozuvi bilan bog'laydi (identity linking / just-in-time provisioning). Bu B2B SaaS'da har mijoz o'z IdP'si bilan kirishini ta'minlaydi.

**Spring'da qayerda uchraydi:** OIDC/OAuth2 uchun bir nechta `ClientRegistration` (`InMemoryClientRegistrationRepository`) va `/oauth2/authorization/{registrationId}` endpoint'lari; SAML 2.0 uchun `spring-security-saml2-service-provider`, `Saml2LoginConfigurer` (`http.saml2Login()`), `RelyingPartyRegistrationRepository`, `Saml2AuthenticatedPrincipal` va `OpenSaml5AuthenticationProvider` (Spring Security 6.5+). LDAP/Active Directory uchun `spring-security-ldap`, `LdapAuthenticationProvider` va `ActiveDirectoryLdapAuthenticationProvider`. Spring Authorization Server'da ham upstream IdP'ni `oauth2Login()` bilan federatsiya qilish mumkin, mapping uchun `GrantedAuthoritiesMapper` yoki custom `OAuth2UserService` ishlatiladi.

**Qo'llanish keyslari:**
- B2B SaaS har korporativ mijozga o'z Okta/Entra ID tenant'i bilan SSO beradi.
- Davlat portali eID/SAML provayderi orqali fuqaroni autentifikatsiya qiladi.
- Universitet tizimi Shibboleth federatsiyasiga qo'shiladi.
- Bitta foydalanuvchi ham Google, ham korporativ hisob bilan kirib, bir profilga bog'lanadi.
- Legacy LDAP katalogidan OIDC'ga bosqichma-bosqich migratsiya davrida ikkisi parallel ishlaydi.

**Ehtiyot bo'ling:** Hisoblarni `email` bo'yicha avtomatik bog'lash (account linking) hisob egallash (account takeover) zaifligiga olib keladi - email tasdiqlanganligini (`email_verified`) tekshirmasdan link qilmang. SAML'da metadata va imzolash sertifikatlarining muddati tugashi eng ko'p uchraydigan production incident'i, shuning uchun monitoring va rotation rejasi bo'lishi kerak.

## 18.21 Sessiyani boshqarish (Session Management (fixation protection, concurrent sessions))

**Tavsif:** Login paytida va undan keyin HTTP session hayotiy tsiklini nazorat qilish patterni. Session fixation himoyasi autentifikatsiyadan so'ng session ID'ni yangilaydi, shunda hujumchi oldin bergan ID bilan sessiyani egallab olmaydi. Concurrent session nazorati bir foydalanuvchi uchun faol sessiyalar sonini cheklaydi va ortiqchasini bekor qiladi yoki yangi login'ni rad etadi.

**Spring'da qayerda uchraydi:** `HttpSecurity.sessionManagement(...)` - `sessionFixation().changeSessionId()` (Servlet 3.1+ dagi standart), `maximumSessions(n)`, `maxSessionsPreventsLogin(true)`, `invalidSessionUrl(...)`, `sessionCreationPolicy(SessionCreationPolicy.STATELESS)`. Ichida `SessionManagementFilter`, `ConcurrentSessionFilter`, `SessionRegistry` (`SessionRegistryImpl`), `SessionAuthenticationStrategy` va `HttpSessionEventPublisher` bean'i ishlaydi. Klasterda sessiyani bo'lishish uchun Spring Session (`spring-session-data-redis`, `@EnableRedisHttpSession`, `SpringSessionBackedSessionRegistry`) va `spring.session.*` konfiguratsiyasi, hamda `CookieSerializer` orqali `SameSite`/`Secure` sozlanadi.

**Qo'llanish keyslari:**
- Internet-banking bitta hisob uchun faqat bitta faol sessiyaga ruxsat beradi.
- Admin panelda eski sessiyani majburan uzib, "boshqa joydan kirildi" xabarini ko'rsatish.
- Redis asosidagi Spring Session bilan bir nechta pod orasida sessiyani bo'lishish.
- Stateless REST API uchun session butunlay o'chiriladi (`STATELESS`) va JWT ishlatiladi.
- Logout'da session'ni invalidate qilib, cookie va `SecurityContext`ni tozalash.

**Ehtiyot bo'ling:** `SessionCreationPolicy.STATELESS` qo'ysangiz, `oauth2Login()`, CSRF token saqlash va `SessionRegistry` ishlamaydi - bu rejimni faqat haqiqiy stateless API'da ishlating. `maximumSessions` uchun `HttpSessionEventPublisher` bean'i e'lon qilinmasa, tugagan sessiyalar registry'dan o'chmaydi va foydalanuvchi vaqt o'tib login qila olmay qoladi.

## 18.22 Remember-Me (Remember-Me)

**Tavsif:** Foydalanuvchini session tugaganidan keyin ham eslab qolish mexanizmi: brauzerga uzoq muddatli cookie beriladi va keyingi tashrifda u asosida avtomatik autentifikatsiya qilinadi. Ikki amalga oshirish bor - faqat hash'langan token (foydalanuvchi nomi + parol hash + muddat + secret) va persistent token (bazada saqlangan, har ishlatilganda yangilanadigan series/token juftligi). Ikkinchisi o'g'irlanishni aniqlash imkonini beradi.

**Spring'da qayerda uchraydi:** `HttpSecurity.rememberMe(...)` konfiguratsiyasi; `RememberMeAuthenticationFilter`, `TokenBasedRememberMeServices` (hash variant) va `PersistentTokenBasedRememberMeServices` + `PersistentTokenRepository` (`JdbcTokenRepository`, `InMemoryTokenRepositoryImpl`). Natijada `RememberMeAuthenticationToken` hosil bo'ladi va `RememberMeAuthenticationProvider` uni tekshiradi; `AuthenticationTrustResolver` orqali `isRememberMe()` ni ajratish mumkin. Spring Security 6.x'da `TokenBasedRememberMeServices` SHA-256 algoritmini qo'llaydi va `rememberMe(r -> r.key("...").tokenValiditySeconds(...).useSecureCookie(true))` bilan sozlanadi.

**Qo'llanish keyslari:**
- Kontent sayti foydalanuvchisi "Meni eslab qol" belgisini qo'yib, har safar login qilmaydi.
- Ichki korporativ wiki'da uzoq sessiya qulaylik uchun yoqiladi.
- E-commerce savatini saqlab, foydalanuvchini qayta tanish.
- Persistent token bilan "bu qurilmani eslab qol" ro'yxatini boshqarish.
- Mobil web-view ilovada tez-tez login qilish talabini kamaytirish.

**Ehtiyot bo'ling:** Remember-me autentifikatsiyasi to'liq login'ga teng emas - parol o'zgartirish, to'lov yoki admin amallarini `isFullyAuthenticated()` yoki `fullyAuthenticated` bilan himoyalab, qayta login talab qilish kerak. `key`ni default qoldirish yoki muhitlar orasida bir xil ishlatish cookie'ni boshqa instance'da ishlatishga yo'l beradi; cookie `HttpOnly`, `Secure` va qisqa muddatli bo'lishi, parol o'zgarganda esa barcha remember-me token'lari bekor qilinishi shart.

## 18.23 CSRF himoyasi (CSRF Protection - Synchronizer Token, Double Submit)

**Tavsif:** Cross-Site Request Forgery hujumi autentifikatsiya qilingan foydalanuvchining browser'idagi cookie'sini ishlatib, uning nomidan so'rov yuboradi. Synchronizer token pattern'da server har bir session uchun tasodifiy token generatsiya qiladi va uni state-changing so'rovda (POST/PUT/DELETE) kutadi; token server tomonida saqlanadi va solishtiriladi. Double submit cookie pattern'da esa token cookie'da ham, request parametri yoki header'da ham yuboriladi va ularning tengligi tekshiriladi - bu stateless, chunki server token'ni saqlamaydi. Hujumchi cross-origin so'rovda cookie'ni yubora olsa ham, token qiymatini o'qib header'ga qo'ya olmaydi (Same-Origin Policy).

**Spring'da qayerda uchraydi:** Spring Security'da `CsrfFilter` va `HttpSecurity.csrf(...)` konfiguratsiyasi; `CsrfTokenRepository` interfeysi hamda uning implementatsiyalari `HttpSessionCsrfTokenRepository` (synchronizer token, default) va `CookieCsrfTokenRepository.withHttpOnlyFalse()` (double submit, SPA uchun). Token `CsrfToken` obyekti sifatida request attribute'ga qo'yiladi; Thymeleaf va Spring Form Taglib `_csrf` hidden input'ni avtomatik qo'shadi. Spring Security 6+ da token'ni dangal yuklash uchun `CsrfTokenRequestAttributeHandler` (`setCsrfRequestAttributeName(null)` bilan eager rendering) va BREACH himoyasi uchun `XorCsrfTokenRequestAttributeHandler` ishlatiladi; `CsrfFilter.DEFAULT_CSRF_MATCHER` GET/HEAD/OPTIONS/TRACE'ni e'tiborsiz qoldiradi. `requireCsrfProtectionMatcher` bilan qaysi endpoint'lar tekshirilishini o'zgartirish mumkin.

**Qo'llanish keyslari:**
- Thymeleaf/JSP asosidagi server-rendered admin panelda session cookie bilan ishlaganda forma yuborishni himoyalash.
- Angular yoki React SPA'da cookie-based session ishlatilganda `CookieCsrfTokenRepository` + `X-XSRF-TOKEN` header orqali double submit qo'llash.
- Spring Security 6 ga migratsiyada deferred token loading sababli buzilgan SPA login flow'ini `CsrfTokenRequestAttributeHandler` bilan tiklash.
- Bank internet-banking'ida pul o'tkazish formasini tashqi saytdan yuborilgan so'rovdan saqlash.
- OAuth2 login endpoint'larida `state` parametri yetarli bo'lmagan hollarda qo'shimcha CSRF qatlamini ta'minlash.

**Ehtiyot bo'ling:** Faqat Bearer token (`Authorization` header) bilan ishlaydigan toza stateless REST API'da CSRF himoyasi keraksiz - browser bu header'ni avtomatik yubormaydi; lekin cookie'da JWT saqlasangiz CSRF yana xavf tug'diradi, shuning uchun "REST = csrf disable" qoidasini ko'r-ko'rona qo'llamang. Double submit pattern subdomain'dan cookie yozish imkoniyati bo'lsa (session fixation / cookie tossing) zaiflashadi, shuning uchun `__Host-` prefiks, `SameSite=Lax` va HMAC-bog'langan token bilan mustahkamlang.

## 18.24 CORS (Cross-Origin Resource Sharing)

**Tavsif:** Browser'ning Same-Origin Policy'si boshqa origin'dagi JavaScript'ning javob tanasini o'qishiga to'sqinlik qiladi; CORS - serverga ruxsat berilgan origin, metod va header'larni e'lon qilish imkonini beradigan standart mexanizm. Server `Access-Control-Allow-Origin`, `-Methods`, `-Headers`, `-Credentials` javob header'lari bilan qoidalarni bildiradi, browser esa "non-simple" so'rovlardan avval `OPTIONS` preflight yuboradi. CORS - bu to'siq emas, balki boshqarilgan yumshatish: u autentifikatsiya yoki avtorizatsiya o'rnini bosmaydi, faqat browser'da kimga o'qishga ruxsat berilganini aytadi.

**Spring'da qayerda uchraydi:** Spring Framework'da `@CrossOrigin` annotatsiyasi (controller yoki metod darajasida), `WebMvcConfigurer.addCorsMappings(CorsRegistry)`, WebFlux'da `CorsWebFilter`; past darajada `CorsConfiguration`, `CorsConfigurationSource` va `UrlBasedCorsConfigurationSource`. Spring Security'da `HttpSecurity.cors(Customizer)` `CorsFilter`ni filter chain boshiga qo'yadi - bu autentifikatsiya filtrlaridan oldin ishlashi muhim, aks holda preflight 401 oladi. Spring Boot'da `spring.graphql.cors.*` va Actuator uchun `management.endpoints.web.cors.*` property'lari mavjud; Gateway'da `spring.cloud.gateway.globalcors` konfiguratsiyasi bor. `CorsConfiguration.setAllowedOriginPatterns` wildcard va credentials'ni birga ishlatish uchun qo'shilgan.

**Qo'llanish keyslari:**
- `app.example.com` dagi SPA'ning `api.example.com` dagi Spring Boot backend'iga murojaat qilishiga ruxsat berish.
- Lokal `localhost:5173` (Vite) dev-server'dan backend'ga so'rov yuborishni faqat `dev` profilda ochish.
- Spring Cloud Gateway darajasida markazlashtirilgan CORS siyosatini joriy qilib, har bir microservice'da takrorlamaslik.
- Uchinchi tomon hamkor domenlariga faqat `GET` ko'rinishdagi public katalog endpoint'ini ochish.
- Mobil ilova WebView yoki Electron ilovasi uchun custom `X-Tenant-Id` header'ini `allowedHeaders`ga qo'shish.

**Ehtiyot bo'ling:** `allowedOrigins("*")` ni `allowCredentials(true)` bilan birga ishlatish mumkin emas (Spring exception tashlaydi) va umuman `*` + cookie kombinatsiyasi o'zi xavfli - origin'larni aniq ro'yxatlang yoki `allowedOriginPatterns`da qattiq pattern bering. Agar `cors()` Spring Security chain'ida yoqilmasa yoki custom filter CORS'dan oldin ishlasa, preflight so'rovlar 401/403 bilan qaytib, "CORS xatosi" sifatida ko'rinadi - muammo aslida filter tartibida bo'ladi.

## 18.25 Xavfsizlik header'lari (Security Headers - CSP, HSTS)

**Tavsif:** Browser'ga uning o'zini qanday cheklashini aytadigan HTTP javob header'lari to'plami: `Content-Security-Policy` qaysi manbalardan skript, stil va frame yuklanishi mumkinligini belgilab XSS ta'sirini kamaytiradi, `Strict-Transport-Security` domenni faqat HTTPS orqali ochishga majbur qiladi va SSL-stripping'ni to'sadi. Bunga `X-Content-Type-Options: nosniff`, `X-Frame-Options`/`frame-ancestors` (clickjacking), `Referrer-Policy`, `Cross-Origin-Opener-Policy` va `Permissions-Policy` ham kiradi. Bu pattern - defense in depth: ilova kodidagi xatolik yuzaga chiqsa ham, uning zarari browser darajasida cheklanadi.

**Spring'da qayerda uchraydi:** Spring Security'ning `HeaderWriterFilter` va `HttpSecurity.headers(...)` DSL'i; `ContentSecurityPolicyHeaderWriter`, `HstsHeaderWriter`, `XContentTypeOptionsHeaderWriter`, `ReferrerPolicyHeaderWriter`, `XFrameOptionsHeaderWriter`, `PermissionsPolicyHeaderWriter`, `CrossOriginOpenerPolicyHeaderWriter`. Default holatda Spring Security `nosniff`, `X-Frame-Options: DENY`, `Cache-Control: no-store` va HTTPS so'rovlar uchun HSTS qo'shadi, CSP'ni esa siz o'zingiz yozishingiz kerak. CSP nonce'ni Thymeleaf shablonlariga uzatish uchun odatda custom `OncePerRequestFilter` + request attribute ishlatiladi; `requiresChannel().anyRequest().requiresSecure()` HTTPS'ga redirect qiladi.

**Qo'llanish keyslari:**
- Public SaaS portalida `script-src 'self' 'nonce-...'` bilan inline skriptlarni cheklab XSS ta'sirini kamaytirish.
- `includeSubDomains` va `preload` bilan HSTS qo'yib, butun `*.example.com` ni HTTPS'ga majburlash.
- Admin panelni iframe'ga joylashtirishni `frame-ancestors 'none'` orqali taqiqlab clickjacking'dan saqlash.
- H2 console yoki Swagger UI'ni ishlatish uchun faqat `dev` profilda `frameOptions().sameOrigin()` qilish.
- `Content-Security-Policy-Report-Only` + `report-to` bilan siyosatni ishlab chiqarishda sinovdan o'tkazib, keyin majburiy qilish.

**Ehtiyot bo'ling:** `preload` bilan HSTS'ni qo'yish deyarli qaytarib bo'lmaydigan qadam - sertifikat yoki subdomain muammosi butun domenni ishdan chiqarishi mumkin, shuning uchun avval kichik `max-age` bilan sinab ko'ring. CSP'ni `unsafe-inline`/`unsafe-eval` bilan yozish uni ma'nosiz qiladi; shuningdek reverse proxy (Nginx, API Gateway) ham xuddi shu header'ni qo'shsa, dublikat yoki ziddiyatli qiymatlar paydo bo'ladi.

## 18.26 Brute-force himoyasi / Akkaunt bloklash (Brute-force Protection / Account Lockout)

**Tavsif:** Parolni taxmin qilish hujumlariga qarshi muvaffaqiyatsiz login urinishlarini hisoblab, ma'lum chegaradan keyin akkauntni yoki IP'ni vaqtincha bloklash, kechiktirish (exponential backoff) yoki CAPTCHA talab qilish. Hisoblagich odatda akkaunt + IP kombinatsiyasi bo'yicha yuritiladi va TTL bilan avtomatik tozalanadi. Maqsad - hujum tezligini iqtisodiy jihatdan foydasiz darajaga tushirish, shu bilan birga haqiqiy foydalanuvchilarni butunlay qulflab qo'ymaslik.

**Spring'da qayerda uchraydi:** Spring Security'da `AuthenticationFailureBadCredentialsEvent` va `AuthenticationSuccessEvent`ni `@EventListener` bilan tinglab hisoblagich yuritish eng ko'p qo'llaniladigan yondashuv; blokni qo'llash uchun `UserDetails.isAccountNonLocked()` (`LockedException`) yoki custom `AuthenticationProvider`/`UserDetailsService`. Kalit saqlash uchun Redis (`RedisTemplate`, `spring-boot-starter-data-redis`) yoki Caffeine (`spring-boot-starter-cache`); rate limiting uchun Bucket4j, Resilience4j `RateLimiter`, yoki Spring Cloud Gateway'ning `RequestRateLimiterGatewayFilterFactory` (Redis token bucket). Spring Security `DelegatingPasswordEncoder` va `BCryptPasswordEncoder` work factor'i ham offline brute-force'ga qarshi ishlaydi. Credential stuffing uchun `CompromisedPasswordChecker` (Spring Security 6.3+, `HaveIBeenPwnedRestApiPasswordChecker`) mavjud.

**Qo'llanish keyslari:**
- B2C login formasida 5 ta xato urinishdan keyin akkauntni 15 daqiqaga bloklash.
- Bitta IP'dan ko'p akkauntga urilayotgan credential stuffing botini IP-bo'yicha rate limit bilan to'xtatish.
- OTP/SMS tasdiqlash kodini brute-force qilishga qarshi urinishlar sonini 3 ga cheklash.
- Gateway darajasida `/api/auth/**` yo'liga Redis token bucket qo'yib, barcha microservice'larni bir joyda himoyalash.
- Parol tiklash (forgot password) endpoint'ida enumeration va spam'ni kamaytirish uchun per-email throttling.

**Ehtiyot bo'ling:** Akkauntni faqat username bo'yicha bloklash o'zi DoS vektoriga aylanadi - hujumchi begonaning akkauntini ataylab qulflab qo'yishi mumkin, shuning uchun IP/qurilma reputatsiyasi, CAPTCHA yoki progressive delay bilan birlashtiring. Hisoblagichni lokal in-memory map'da saqlash bir nechta instance'li deploy'da ishlamaydi (har bir pod o'z limitini sanaydi) va login javoblarida "bu user bloklangan" deb aytish user enumeration'ga yo'l ochadi.

## 18.27 Ko'p faktorli autentifikatsiya (Multi-Factor Authentication)

**Tavsif:** Foydalanuvchini bir nechta mustaqil "faktor" bilan tekshirish: bilgan narsasi (parol), egalik qilgan narsasi (TOTP app, qurilma, security key) va o'zi bo'lgan narsasi (biometrika). Parol o'g'irlangan yoki qayta ishlatilgan holatda ham hujumchi ikkinchi faktorga ega bo'lmasa kira olmaydi. Amalda bu ko'p qadamli autentifikatsiya oqimi sifatida quriladi: birinchi faktordan keyin session "yarim autentifikatsiya qilingan" holatga o'tadi va faqat ikkinchi faktor tasdiqlangandan so'ng to'liq huquq beradi.

**Spring'da qayerda uchraydi:** Spring Security 6.x da ko'p qadamli oqim odatda `AuthenticationSuccessHandler` bilan foydalanuvchini `/mfa` sahifasiga yo'naltirib, `SecurityContext`ga vaqtinchalik cheklangan `GrantedAuthority` (masalan `ROLE_PRE_AUTH` yoki `MFA_REQUIRED`) berib amalga oshiriladi; so'ng custom `AuthenticationProvider`/filter TOTP kodini tekshirib to'liq `Authentication`ni almashtiradi. Metod darajasida `@PreAuthorize("hasAuthority('MFA_PASSED')")` yoki `AuthorizationManager` bilan step-up majburlanadi. TOTP uchun kutubxonalar: `com.warrenstrange:googleauth`, `dev.samstevens.totp`, Keycloak/Okta/Auth0 kabi IdP'larga `spring-boot-starter-oauth2-client` orqali delegatsiya. OAuth2/OIDC'da `acr`/`amr` claim'lari va `max_age` parametri step-up uchun ishlatiladi; Spring Authorization Server custom `AuthenticationProvider`lar bilan MFA oqimini qo'llab-quvvatlaydi.

**Qo'llanish keyslari:**
- Admin rolidagi foydalanuvchilar uchun TOTP (Google Authenticator) ni majburiy qilish.
- Pul o'tkazish yoki IBAN o'zgartirish amalida step-up MFA so'rash, oddiy ko'rishda esa so'ramaslik.
- Yangi qurilmadan yoki yangi davlatdan kirishda adaptiv ravishda ikkinchi faktorni yoqish.
- Korporativ SSO (Entra ID / Keycloak) orqali kelgan `amr` claim'ini tekshirib, MFA qilinmagan token'ni rad etish.
- Zaxira kodlar (recovery codes) bilan foydalanuvchining telefonini yo'qotgan holatini qoplash.

**Ehtiyot bo'ling:** SMS/email OTP eng zaif faktor - SIM swap va phishing'ga ochiq, shuning uchun yuqori qiymatli operatsiyalarda TOTP yoki WebAuthn'ni afzal ko'ring. Eng ko'p uchraydigan xato - birinchi faktordan keyin to'liq `Authentication`ni `SecurityContext`ga joylash: bu holda foydalanuvchi MFA sahifasini chetlab o'tib boshqa URL'ga to'g'ridan-to'g'ri kira oladi, shuning uchun MFA bajarilmaguncha huquqlar cheklangan bo'lishi shart.

## 18.28 Passkey'lar / WebAuthn (Passkeys / WebAuthn)

**Tavsif:** Parolsiz autentifikatsiya: foydalanuvchi qurilmasi public/private kalit juftligini generatsiya qiladi, private kalit qurilmada (TPM, Secure Enclave, security key) qoladi va serverga faqat public kalit yuboriladi. Login vaqtida server challenge yuboradi, qurilma uni private kalit bilan imzolaydi - shuning uchun o'g'irlanadigan umumiy sir (shared secret) yo'q. Imzo origin'ga bog'langani uchun passkey phishing'ga chidamli: soxta domen uchun browser imzo yaratmaydi.

**Spring'da qayerda uchraydi:** Spring Security 6.4+ da native WebAuthn/passkey qo'llab-quvvatlashi bor: `HttpSecurity.webAuthn(...)` bilan `rpId`, `rpName`, `allowedOrigins` sozlanadi; asosiy abstraksiyalar `WebAuthnRelyingPartyOperations` / `Webauthn4JRelyingPartyOperations`, `PublicKeyCredentialUserEntityRepository` va `UserCredentialRepository` (in-memory implementatsiyalar bor, production uchun o'zingiz JDBC/JPA variantini yozasiz). Avtomatik ravishda `/login/webauthn`, `/webauthn/register` endpoint'lari va default registratsiya sahifasi qo'shiladi; ichki qism `com.webauthn4j:webauthn4j-core` kutubxonasiga tayanadi. Spring Boot 3.4+/4.x bilan birga ishlaydi; eski versiyalarda Yubico `java-webauthn-server` yoki IdP (Keycloak, Okta) orqali amalga oshirilgan.

**Qo'llanish keyslari:**
- B2C ilovada parolni butunlay olib tashlab, platform passkey (Face ID / Windows Hello) bilan kirishga o'tish.
- Korporativ admin konsolga faqat FIDO2 security key (YubiKey) bilan kirishni talab qilish.
- Mavjud parol login'i ustiga passkey'ni ikkinchi faktor sifatida qo'shish va asta-sekin parolni so'ndirish.
- Phishing hujumlari ko'p bo'ladigan fintech ilovasida OTP o'rniga origin-bound passkey ishlatish.
- Bir akkauntga bir nechta passkey (telefon, laptop, security key) ro'yxatdan o'tkazib qurilma yo'qolishiga chidamlilik berish.

**Ehtiyot bo'ling:** `rpId` domenga qattiq bog'lanadi - uni keyinroq o'zgartirsangiz yoki `allowedOrigins`ni noto'g'ri sozlasangiz barcha mavjud passkey'lar ishlamay qoladi, shuning uchun domen strategiyasini boshida hal qiling. Qurilma yo'qolgan yoki sinxronizatsiya qilinmagan passkey holati uchun ishonchli account recovery oqimi bo'lishi shart, aks holda foydalanuvchi akkauntidan butunlay ayriladi - va recovery oqimi odatda eng zaif bo'g'inga aylanadi.

## 18.29 Bir martalik token bilan kirish (One-Time Token Login / Magic Link)

**Tavsif:** Foydalanuvchiga email yoki SMS orqali qisqa muddatli, bir marta ishlatiladigan token (magic link) yuborilib, u orqali parolsiz kirish yoki parolni tiklash amalga oshiriladi. Server token'ni xeshlangan holda qisqa TTL bilan saqlaydi, ishlatilgandan so'ng darhol bekor qiladi (single use). Bu pattern parol saqlash yukini kamaytiradi, lekin xavfsizlik email kanalining xavfsizligiga tenglashadi.

**Spring'da qayerda uchraydi:** Spring Security 6.4+ da `HttpSecurity.oneTimeTokenLogin(...)` DSL'i mavjud; asosiy komponentlar `OneTimeTokenService` (default `InMemoryOneTimeTokenService`, `JdbcOneTimeTokenService` ham bor), `OneTimeToken`, `GenerateOneTimeTokenRequest` va `OneTimeTokenGenerationSuccessHandler` - oxirgisini siz implementatsiya qilib token'ni email/SMS orqali yuborasiz. Avtomatik `/ott/generate` va `/login/ott` endpoint'lari qo'shiladi. Parol tiklash uchun klassik yo'l - `JdbcTokenRepository`-ga o'xshash o'z jadvalingiz, `SecureRandom`/`UUID` + `MessageDigest`/`BCrypt` xesh, `JavaMailSender` bilan yuborish; "remember me" uchun esa `PersistentTokenBasedRememberMeServices` alohida pattern.

**Qo'llanish keyslari:**
- Kamdan-kam kiradigan foydalanuvchilar uchun parolsiz magic link login (newsletter, portal).
- "Parolni esdan chiqardim" oqimida bir martalik tiklash havolasini yuborish.
- Yangi xodimni tizimga birinchi marta kiritishda invitation link orqali akkauntni aktivlashtirish.
- Mobil ilovadan web konsolga qurilmalararo (cross-device) kirishni osonlashtirish.
- Qo'llab-quvvatlash xizmati uchun vaqtincha, cheklangan huquqli kirish havolasini berish.

**Ehtiyot bo'ling:** Token'ning TTL'i qisqa (5-15 daqiqa) va qat'iy single-use bo'lishi, bazada esa faqat xeshi saqlanishi kerak; token'ni URL query parametrida yuborish uni browser history, Referer header va proxy log'lariga tushiradi. Email kompromis qilingan bo'lsa magic link to'liq akkaunt egaligini beradi, shuning uchun yuqori xavfli operatsiyalarda uni yakka autentifikatsiya vositasi sifatida ishlatmang va generate endpoint'ini albatta rate limit qiling.

## 18.30 Sirlarni boshqarish (Secrets Management - Vault, Config Server Encryption)

**Tavsif:** Parollar, API kalitlari, sertifikatlar va DB credential'larini kod, `application.yml` yoki Git repozitoriyda emas, markazlashtirilgan, audit qilinadigan va aylantirib (rotate) turiladigan secret store'da saqlash. Ilova ishga tushganda yoki ish vaqtida sirni autentifikatsiya qilingan kanal orqali oladi, kerak bo'lsa dinamik, qisqa muddatli credential generatsiya qiladi. Bu sirning yashash muddatini qisqartirib, kompromis oynasini kamaytiradi va rotatsiyani deploy'siz qilish imkonini beradi.

**Spring'da qayerda uchraydi:** Spring Cloud Vault (`spring-cloud-starter-vault-config`) - HashiCorp Vault'dan `PropertySource` sifatida sir o'qiydi, `VaultTemplate` bilan programmatik kirish, database secrets engine orqali dinamik DB credential va `spring.cloud.vault.*` konfiguratsiyasi; token aylanishi uchun `LeaseContainer`/`SecretLeaseContainer`. Spring Cloud Config Server `{cipher}` prefiksli shifrlangan qiymatlarni va `/encrypt`, `/decrypt` endpoint'larini qo'llab-quvvatlaydi (symmetric kalit yoki JKS keystore bilan). Kubernetes'da `spring-cloud-starter-kubernetes-client-config` Secret'larni mount yoki API orqali o'qiydi; AWS uchun Spring Cloud AWS `spring-cloud-aws-starter-secrets-manager` va `spring-cloud-aws-starter-parameter-store`. Rotatsiyadan keyin yangilash uchun `@RefreshScope` va Actuator'ning `/actuator/refresh` endpoint'i ishlatiladi.

**Qo'llanish keyslari:**
- Production DB parolini Git'dan olib tashlab, Vault database secrets engine orqali har bir pod uchun dinamik, 1 soatlik credential berish.
- Config Server'da `{cipher}` bilan shifrlangan integration API kalitlarini saqlash va faqat kerakli profilga ochish.
- Kubernetes'da Secret'ni env variable o'rniga projected volume sifatida mount qilib, pod loglariga tushmasligini ta'minlash.
- To'lov provayderi sertifikati (mTLS keystore) ni Vault PKI engine'dan avtomatik olib yangilash.
- Audit talabiga ko'ra "kim, qachon, qaysi sirni o'qidi" jurnalini markazlashtirish.

**Ehtiyot bo'ling:** Sirlarni Vault'ga ko'chirish "bootstrap secret" muammosini yo'q qilmaydi - Vault'ga kirish token'ining o'zi xavfsiz berilishi kerak (Kubernetes auth, AppRole, IAM), uni `application.yml`ga yozish butun g'oyani buzadi. Shuningdek sirlarni environment variable sifatida uzatish `/proc`, crash dump va `/actuator/env` orqali oqib ketishiga olib kelishi mumkin, shuning uchun Actuator endpoint'larini yopib, `@ConfigurationProperties`da sanitizatsiyani tekshirib turing.

## 18.31 Zero Trust (Zero Trust Architecture)

**Tavsif:** "Ichki tarmoq ishonchli" taxminidan voz kechib, har bir so'rovni - qayerdan kelganidan qat'i nazar - autentifikatsiya va avtorizatsiya qilish modeli. Har bir service-to-service chaqiruv o'z identifikatoriga ega bo'ladi, huquqlar minimal (least privilege) va qisqa muddatli beriladi, barcha trafik shifrlanadi hamda to'liq jurnallanadi. Ruxsat qarori statik tarmoq perimetriga emas, balki identity, qurilma holati va kontekstga asoslanadi.

**Spring'da qayerda uchraydi:** Resource server sifatida `spring-boot-starter-oauth2-resource-server` har bir chaqiruvda JWT/opaque token'ni tekshiradi (`JwtDecoder`, `JwtAuthenticationConverter`, `OpaqueTokenIntrospector`); service-to-service uchun `spring-boot-starter-oauth2-client` bilan client credentials grant va `OAuth2AuthorizedClientManager` + `ServletOAuth2AuthorizedClientExchangeFilterFunction` (`RestClient`/`WebClient` interceptor). Avtorizatsiya qarorlari `@PreAuthorize`, `AuthorizationManager`, `MethodSecurityExpressionHandler` orqali yoki tashqi policy engine (OPA/Cedar) bilan birlashtiriladi. Transport darajasida mTLS (`X509AuthenticationFilter`, `server.ssl.client-auth=need`) yoki Istio/Linkerd service mesh; `spring-boot-starter-actuator` + Micrometer Tracing kuzatuvchanlik beradi. Spring Authorization Server o'z token issuer'ingizni qurish imkonini beradi.

**Qo'llanish keyslari:**
- Microservice'lar o'rtasidagi har bir chaqiruvni JWT yoki mTLS identity bilan tekshirish, "VPN ichidasan - demak ishonchlisan" qoidasini olib tashlash.
- Multi-tenant SaaS'da har bir so'rovda tenant kontekstini tekshirib, cross-tenant ma'lumot oqishini to'sish.
- Ichki admin asboblarini faqat boshqariladigan qurilma + MFA sharti bilan ochish.
- Batch/cron job'lar uchun doimiy service parol o'rniga qisqa muddatli workload identity (client credentials) ishlatish.
- Legacy monolitni bo'lib chiqarishda har bir yangi service'ga alohida identity va aniq scope berish.

**Ehtiyot bo'ling:** Zero Trust - mahsulot emas, balki bosqichma-bosqich joriy etiladigan model; hammasini bir kunda yoqish latency, operatsion murakkablik va sertifikat boshqaruvi xarajatini keskin oshiradi. Eng ko'p uchraydigan yarim-yo'l xatosi: token'ni gateway'da bir marta tekshirib, keyin ichkarida "ishonchli" deb uzatish - bu aslida eski perimetr modelining yangi nomi.

## 18.32 mTLS (Mutual TLS)

**Tavsif:** Oddiy TLS'da faqat server o'z sertifikati bilan tanilsa, mutual TLS'da client ham X.509 sertifikat ko'rsatadi va ikki tomon bir-birini kriptografik tasdiqlaydi. Natijada transport darajasida kuchli, parolsiz identity paydo bo'ladi: sertifikat Subject/SAN qiymati principal sifatida ishlatiladi. Bu service-to-service aloqada bearer token o'g'irlanishi muammosini kamaytiradi, chunki sertifikatning private kaliti chaqiruvchida qoladi.

**Spring'da qayerda uchraydi:** Spring Boot'da `server.ssl.client-auth=need|want`, `server.ssl.trust-store`/`trust-store-password` yoki Boot 3.1+ dagi SSL bundle'lar (`spring.ssl.bundle.jks.*`, `spring.ssl.bundle.pem.*`) va `SslBundles` API; Spring Security tomonida `HttpSecurity.x509(...)`, `X509AuthenticationFilter`, `SubjectDnX509PrincipalExtractor` va `UserDetailsService` bilan sertifikat DN'ni rolga map qilish. Client tomonda `RestClient`/`WebClient` uchun `SslBundle` asosida Reactor Netty yoki Apache HttpClient `SSLContext` sozlanadi; `spring-boot-starter-webflux`da `HttpClient.secure(...)`. Spring Cloud Vault PKI engine yoki cert-manager sertifikatlarni avtomatik beradi; service mesh (Istio) mTLS'ni sidecar darajasida ilovadan tashqarida bajaradi. OAuth2'da sertifikatga bog'langan token uchun `tls_client_auth` va certificate-bound access token (RFC 8705) mavjud.

**Qo'llanish keyslari:**
- Bank yoki to'lov provayderi API'si bilan integratsiyada mTLS'ni majburiy talab sifatida bajarish.
- Kubernetes klasterida microservice'lar orasidagi barcha trafikni sidecar mTLS bilan shifrlash va autentifikatsiya qilish.
- IoT qurilmalarini parol o'rniga qurilmaga yuklangan sertifikat bilan tanish.
- Ichki admin/management portini faqat sertifikatga ega operator mashinalariga ochish.
- Hamkor B2B tizimidan keladigan webhook'larni client sertifikati bo'yicha tekshirish.

**Ehtiyot bo'ling:** Asosiy xarajat - sertifikat hayot sikli: muddati o'tgan yoki qo'lda almashtirilmagan sertifikat butun integratsiyani to'xtatadi, shuning uchun avtomatik rotatsiya va monitoring bo'lmasa mTLS ishlatmaslik yaxshiroq. Load balancer yoki ingress TLS'ni terminate qilsa, ilova client sertifikatini ko'rmaydi - bunday holda `X-Client-Cert`/`X-Forwarded-Client-Cert` header'iga ishonish faqat proxy'ga to'liq ishonch va bu header'ni tashqaridan tozalash sharti bilan mumkin.

## 18.33 API kaliti (API Key)

**Tavsif:** Chaqiruvchi tizimga beriladigan uzun, tasodifiy sir - har bir so'rovda header orqali yuborilib, mijozni identifikatsiya qiladi va kvota/rate limit hisobini yuritishga imkon beradi. API key - autentifikatsiyaning eng sodda shakli: u foydalanuvchini emas, balki chaqiruvchi ilovani (machine client) tanitadi va o'z-o'zidan hech qanday muddat yoki scope ma'lumotini olib yurmaydi. Shu sababli u odatda server-to-server, past riskli yoki public-read API'larda ishlatiladi.

**Spring'da qayerda uchraydi:** Spring Security'da custom `OncePerRequestFilter` yoki `AbstractPreAuthenticatedProcessingFilter` kengaytmasi (masalan `RequestHeaderAuthenticationFilter` `X-API-KEY` header'i uchun) bilan amalga oshiriladi; filter `PreAuthenticatedAuthenticationToken` yasab `AuthenticationManager`ga beradi, `PreAuthenticatedAuthenticationProvider` esa `AuthenticationUserDetailsService` orqali huquqlarni yuklaydi. Kalitlar bazada xeshlangan holda saqlanadi (`BCryptPasswordEncoder` yoki SHA-256 + prefiks lookup), taqqoslashda `MessageDigest.isEqual` bilan timing-safe tekshirish qilinadi. Rate limit uchun Bucket4j yoki Spring Cloud Gateway `RequestRateLimiter` key resolver'i API key bo'yicha sozlanadi; `spring-boot-starter-actuator` metrikalari kvotani kuzatadi.

```java
public class ApiKeyFilter extends AbstractPreAuthenticatedProcessingFilter {
    @Override protected Object getPreAuthenticatedPrincipal(HttpServletRequest req) {
        return req.getHeader("X-API-KEY"); // keyin provider xeshni tekshiradi
    }
    @Override protected Object getPreAuthenticatedCredentials(HttpServletRequest req) {
        return "N/A";
    }
}
```

**Qo'llanish keyslari:**
- Uchinchi tomon hamkorlariga public ma'lumot API'siga kirish va kvota hisobini berish.
- Internal cron/batch service'ning boshqa service'ga oddiy, past riskli chaqiruvlarini autentifikatsiya qilish.
- Webhook qabul qiluvchi endpoint'da yuboruvchini oldindan kelishilgan kalit bilan tekshirish (imzo bilan birga).
- Monitoring yoki scraping agentlariga faqat `GET /metrics` huquqi bilan cheklangan kalit berish.
- SDK foydalanuvchilariga sandbox va production muhitlari uchun alohida kalitlar tarqatish.

**Ehtiyot bo'ling:** API key - statik, muddatsiz bearer sir: u mobil ilova yoki frontend JavaScript'ga joylansa darhol ochiq deb hisoblanadi, shuning uchun foydalanuvchi autentifikatsiyasi yoki nozik operatsiyalar uchun OAuth2/OIDC token'ni tanlang. Kalitni plaintext saqlash, log'larga yozish yoki URL query parametrida uzatish keng tarqalgan xato - doimo header orqali yuboring, xeshlangan saqlang va rotatsiya hamda bekor qilish (revoke) mexanizmini boshidan rejalashtiring.

## 18.34 Audit log yuritish (Audit Logging)

**Tavsif:** Xavfsizlik nuqtai nazaridan audit logging "kim, nimani, qachon, qaysi natija bilan qildi" savoliga javob beradigan o'zgarmas (append-only) yozuvlar oqimini yaratadi. Oddiy application log'dan farqi - bu yozuvlar compliance va forensic tekshiruv uchun dalil bo'lib xizmat qiladi, shuning uchun ularda subject (foydalanuvchi yoki service account), resurs identifikatori, amal turi, natija (allow/deny) va korrelyatsiya ID'si bo'lishi shart. Muvaffaqiyatsiz authentication va authorization urinishlari ham, muvaffaqiyatli nozik amallar ham yozib boriladi. Log'lar o'zgartirilmasligi uchun alohida append-only store yoki WORM saqlashga yuboriladi.

**Spring'da qayerda uchraydi:** Spring Security `AuthenticationSuccessEvent`, `AuthenticationFailureBadCredentialsEvent`, `AuthorizationDeniedEvent`, `AuthorizationGrantedEvent` event'larini publish qiladi - ularni `@EventListener` bilan tutib olinadi; `AuthenticationEventPublisher` (standart implementatsiya `DefaultAuthenticationEventPublisher`) bu mexanizmni boshqaradi. Spring Data JPA'da `@EntityListeners(AuditingEntityListener.class)` + `@CreatedBy`/`@LastModifiedBy` va `AuditorAware<String>` bean domain-level audit maydonlarini to'ldiradi. Hibernate Envers (`@Audited`) entity versiyalarini alohida `_AUD` jadvallarda saqlaydi. Spring Boot 3.x'da `AuditEventRepository` bean bo'lsa, Actuator `/actuator/auditevents` endpoint'i ochiladi va `AuditApplicationEvent` orqali yoziladi. Strukturali JSON log uchun Boot 3.4+ `logging.structured.format.console=ecs` va MDC (`MDCInsertingServletFilter`, Micrometer Tracing'ning `traceId`) ishlatiladi.

**Qo'llanish keyslari:**
- Bank backend'ida har bir to'lov buyrug'ini kim yaratgani va kim tasdiqlaganini regulyator talab qilgan 7 yil davomida saqlash.
- Sog'liqni saqlash tizimida bemor kartasini ko'rgan har bir shifokorni HIPAA talablari bo'yicha yozib borish.
- Brute-force hujumini aniqlash uchun bir IP'dan kelgan `AuthenticationFailureBadCredentialsEvent` sonini Micrometer counter sifatida kuzatish.
- Admin panelidagi role o'zgartirish amallarini SIEM (Splunk, Elastic) tizimiga alohida kanal bilan yuborish.
- Incident'dan keyin `traceId` bo'yicha bitta foydalanuvchi sessiyasining butun amal zanjirini tiklash.

**Ehtiyot bo'ling:** Audit log'ga parol, token, PAN raqami yoki shaxsiy ma'lumotlarni to'liq yozib qo'yish eng ko'p uchraydigan xato - log'ning o'zi ma'lumot sizib chiqish kanaliga aylanadi, shuning uchun maskalash va `toString()` filtrlarini majburiy qiling. Audit yozuvini biznes tranzaksiyaning ichida sinxron yozsangiz, log store ishlamay qolganda biznes amali ham yiqiladi - bu qarorni (fail-open yoki fail-closed) ongli ravishda, compliance talabiga qarab tanlang.

## 18.35 Kirish ma'lumotini tekshirish / chiqishni kodlash (Input Validation / Output Encoding)

**Tavsif:** Bu juft pattern injection turkumidagi hujumlarning asosini yo'q qiladi: kirishda ma'lumot kutilgan shaklga mos kelishini allowlist asosida tekshiriladi, chiqishda esa ma'lumot borayotgan kontekstga (HTML, HTML atribut, JavaScript, URL, SQL, LDAP, shell) mos ravishda kodlanadi. Validation hujumni to'liq to'xtatmaydi - asosiy himoya kontekstga bog'liq encoding va parametrizatsiyadir, chunki bir xil satr HTML'da xavfsiz, JavaScript'da xavfli bo'lishi mumkin. Validation trust boundary'ning har bir chetida takrorlanadi: controller, service va persistence qatlamida.

**Spring'da qayerda uchraydi:** Jakarta Bean Validation (`jakarta.validation.constraints.*` - `@NotBlank`, `@Pattern`, `@Size`, `@Email`) `@Valid`/`@Validated` bilan controller parametrlarida va service metod argumentlarida ishlaydi; Hibernate Validator standart implementatsiya. `MethodArgumentNotValidException` va `ConstraintViolationException` `@ControllerAdvice` + `ProblemDetail` (RFC 9457) bilan boshqariladi. SQL injection'dan Spring Data JPA'ning derived query'lari, `@Query` ichidagi named parametrlar va `JdbcTemplate`/`JdbcClient`'ning `?` placeholder'lari himoya qiladi - satr konkatenatsiyasi emas. HTML chiqishda Thymeleaf `th:text` avtomatik escape qiladi (`th:utext` esa YO'Q), Spring Security'ning `HtmlUtils.htmlEscape` va OWASP Java Encoder (`Encode.forHtml`, `Encode.forJavaScript`) ishlatiladi. Rich-text uchun OWASP Java HTML Sanitizer yoki jsoup `Safelist`. `Content-Security-Policy` header'i `HeadersConfigurer#contentSecurityPolicy` bilan qo'yiladi.

**Qo'llanish keyslari:**
- Ommaviy REST API'da `@Pattern` bilan faqat `[A-Za-z0-9_-]` ruxsat etilgan tenant slug'ini qabul qilish.
- Foydalanuvchi yozgan izohni blog sahifasida ko'rsatishdan oldin HTML Sanitizer bilan faqat `<b>`, `<i>`, `<a>` tag'larini qoldirish.
- Dinamik `ORDER BY` ustunini foydalanuvchi kiritgan satrdan emas, server tomonidagi allowlist enum'idan tanlash.
- Fayl yuklashda nomni normalizatsiya qilib `../` path traversal'ni bloklash va kontent turini magic byte bo'yicha tekshirish.
- LDAP qidiruv filtriga uzatilayotgan login nomini `LdapEncoder.filterEncode` bilan kodlash.

**Ehtiyot bo'ling:** Faqat denylist (qora ro'yxat) bilan `<script>` kabi naqshlarni filtrlash deyarli har doim chetlab o'tiladi - allowlist va encoding'ni tanlang. Kirishda bir marta "sanitize" qilib ma'lumotni bazaga o'zgartirilgan holda saqlash ham xato: original ma'lumot buziladi va boshqa kontekstda (CSV, PDF, email) baribir xavfli bo'lib qoladi.

## 18.36 Qatlamli himoya (Defense in Depth)

**Tavsif:** Hech bir yagona nazorat mexanizmiga to'liq ishonmaslik printsipi: bir qatlam buzilganda keyingi qatlam hujumni to'xtatadi. Amalda bu edge (WAF, API gateway), transport (mTLS), application (authentication, authorization, validation), data (shifrlash, row-level security) va infratuzilma (network policy, container isolation) qatlamlarida bir-birini qoplaydigan nazoratlar o'rnatish degani. Har bir qatlam mustaqil ishlashi va boshqasining mavjudligiga tayanmasligi kerak.

**Spring'da qayerda uchraydi:** Gateway qatlamida Spring Cloud Gateway (`RouteLocator`, `RedisRateLimiter`) va u yerda birinchi JWT tekshiruvi; resource server ichida esa yana `oauth2ResourceServer().jwt()` orqali mustaqil tekshiruv. `SecurityFilterChain` ichida URL-level `authorizeHttpRequests` va metod-level `@PreAuthorize`/`@PostAuthorize` (`@EnableMethodSecurity`) birgalikda ishlaydi. Data qatlamida Hibernate `@Filter`/`@FilterDef` yoki PostgreSQL row-level security, ustun shifrlash uchun Spring Security Crypto `AesBytesEncryptor` yoki Hibernate `AttributeConverter`. Transport uchun `server.ssl.client-auth=need` bilan mTLS va `X509AuthenticationFilter`. Header'lar: HSTS, `X-Content-Type-Options`, CSP - barchasi `HttpSecurity#headers` orqali. Actuator endpoint'lari alohida port va alohida `SecurityFilterChain` bilan ajratiladi.

**Qo'llanish keyslari:**
- Gateway JWT'ni tekshirsa ham, har bir microservice o'z ichida token signature va audience'ni qayta tekshirishi (internal network buzilgan holatga qarshi).
- To'lov service'ida `@PreAuthorize` ustiga qo'shimcha ravishda DB'da row-level security bilan boshqa tenant yozuvlarini butunlay ko'rinmas qilish.
- Admin UI'ni ham role tekshiruvi, ham IP allowlist, ham majburiy MFA bilan uch qatlam himoya qilish.
- Secret'larni application'da shifrlash (envelope encryption) va ustiga disk-level shifrlash qo'llash.
- Rate limiting'ni gateway'da (global) va service'da (per-tenant) ikki darajada o'rnatish.

**Ehtiyot bo'ling:** Qatlamlarni ko'paytirish latency, operatsion murakkablik va noto'g'ri konfiguratsiya xavfini oshiradi - har bir qatlam qanday aniq tahdidni qoplashini yozib qo'ying, aks holda "xavfsizlik teatri" bo'ladi. Ayniqsa bir xil qarorni ikki joyda turli qoidalar bilan takrorlash (gateway bir xil, service boshqacha) eng xavfli holat: foydalanuvchi uchun kutilmagan deny yoki, yomoni, kutilmagan allow paydo bo'ladi.

## 18.37 Eng kam imtiyoz (Least Privilege)

**Tavsif:** Har bir subject (foydalanuvchi, service account, process, token) o'z vazifasini bajarish uchun zarur bo'lgan minimal huquqdan ko'p huquqqa ega bo'lmasligi kerak, va bu huquq faqat kerak bo'lgan vaqt oralig'ida amal qilishi lozim. Bu buzilish radiusini (blast radius) kamaytiradi: o'g'irlangan token yoki buzilgan pod butun tizimga emas, faqat kichik bir qismga kirish beradi. Amalda huquqlar coarse-grained role'lar emas, fine-grained permission'lar sifatida modellashtiriladi va muntazam qayta ko'rib chiqiladi.

**Spring'da qayerda uchraydi:** Spring Security'da OAuth2 scope'lar `SCOPE_` prefiksi bilan authority'ga aylanadi (`JwtGrantedAuthoritiesConverter`), shuning uchun `@PreAuthorize("hasAuthority('SCOPE_orders:read')")` bilan tor permission tekshiriladi. Client credentials token'lariga scope'ni Spring Authorization Server'da `RegisteredClient.withId(...).scope("orders:read")` bilan cheklanadi. Fine-grained qoidalar uchun `AuthorizationManager<T>` custom implementatsiyasi yoki `PermissionEvaluator` (`hasPermission(#id, 'Order', 'write')`) ishlatiladi; Spring Security ACL moduli domain-object-level huquqni beradi. DataSource darajasida read-only replica uchun alohida `DataSource` bean va faqat `SELECT` grant'i berilgan DB user. `spring.datasource.hikari.read-only=true` va `@Transactional(readOnly = true)` tasodifiy yozishni kamaytiradi.

**Qo'llanish keyslari:**
- Reporting service'ga faqat read-only DB user va faqat `reports:read` scope'li token berish.
- CI/CD pipeline'dagi service account'ga faqat bitta artifact repository'ga push huquqi berish.
- Qisqa muddatli (5 daqiqa) access token va uzoq muddatli refresh token'ni ajratish, refresh token'ni rotation bilan ishlatish.
- Support xodimiga mijoz ma'lumotini faqat maskalangan ko'rinishda va faqat ochiq ticket davomida ko'rsatish.
- Kubernetes'da har bir Spring Boot service uchun alohida ServiceAccount va faqat kerakli Secret'larni mount qilish.

**Ehtiyot bo'ling:** `ROLE_ADMIN` kabi keng role'ga asta-sekin hamma huquqni yopishtirish (privilege creep) - eng keng tarqalgan buzilish; permission'larni role'dan ajratib, muntazam access review o'tkazing. Boshqa chetga ketish ham zarar: haddan tashqari mayda permission'lar soni yuzlab bo'lsa, jamoa ularni tushunmay "hammasini bera qolaylik" deydi va natija teskari bo'ladi.

## 18.38 Standart holatda xavfsiz (Secure by Default)

**Tavsif:** Tizim hech qanday qo'shimcha konfiguratsiyasiz ham xavfsiz holatda ishga tushishi kerak: yopiq port, o'chirilgan debug, majburiy authentication, shifrlangan transport va ruxsat etilmagan amalga standart "deny". Xavfsizlikni yoqish uchun emas, kamaytirish uchun ongli qadam talab qilinadi - ya'ni xavfsizlikni o'chirish aniq, ko'rinadigan va review'dan o'tadigan o'zgarish bo'ladi. Bu pattern inson xatosini kamaytiradi, chunki "esdan chiqarib qo'yilgan" holat xavfsiz holat bo'ladi.

**Spring'da qayerda uchraydi:** Spring Boot `spring-boot-starter-security` dependency qo'shilishining o'zi barcha endpoint'larni himoyalaydi va CSRF, session fixation protection, xavfsizlik header'larini yoqadi. Spring Security 6.x/7.x'da `authorizeHttpRequests` ichida mos qoida topilmagan request `AuthorizationFilter` tomonidan rad etiladi, `anyRequest().denyAll()` esa buni ochiq yozish usuli. Spring Boot 3.x'da Actuator'dan faqat `health` web'ga ochiq, qolganlari `management.endpoints.web.exposure.include` bilan ongli qo'shiladi. Parollar uchun `PasswordEncoderFactories.createDelegatingPasswordEncoder()` standart sifatida bcrypt'ni tanlaydi va `{bcrypt}` prefiksi bilan migratsiyaga yo'l beradi. `server.error.include-stacktrace=never` va `include-message=never` Boot'ning standart qiymatlari. Spring Boot 4.x / Framework 7.x'da `@Nullable` va null-safety annotatsiyalari (JSpecify) standart sifatida non-null'ni nazarda tutadi.

**Qo'llanish keyslari:**
- Yangi microservice template'ida `anyRequest().authenticated()` bilan boshlab, ochiq endpoint'larni faqat aniq ro'yxat bilan qo'shish.
- Multi-tenant repository'da tenant filtri avtomatik yoqilgan bo'lishi, o'chirish faqat alohida `@AdminQuery` bilan mumkin bo'lishi.
- Yangi foydalanuvchi akkaunti hech qanday role'siz yaratilib, huquqlar faqat approval'dan keyin berilishi.
- `spring.jpa.open-in-view=false`, TLS majburiy, HTTP → HTTPS redirect kabi xavfsiz default'larni umumiy parent POM / shared starter'ga kiritish.
- Feature flag'larni standart holatda `off` qilib, yangi funksiyani ongli ravishda yoqish.

**Ehtiyot bo'ling:** Lokal ishlab chiqishni osonlashtirish uchun yozilgan `permitAll()`, `csrf().disable()` yoki self-signed sertifikatga ishonish kodi profile ajratilmasa production'ga chiqib ketadi - bunday sozlamalarni faqat `@Profile("dev")` ichida saqlang va CI'da production konfiguratsiyasini test bilan tekshiring. Shuningdek "secure default"ni global holda o'chiradigan bitta flag yaratmang, chunki u albatta bosiladi.

## 18.39 Xavfsiz tarzda yiqilish (Fail Securely)

**Tavsif:** Xato, timeout yoki tashqi tizim ishlamay qolgan holatda tizim xavfsiz holatga qaytishi kerak - ya'ni ruxsat bermaslik (fail-closed), ma'lumotni oshkor qilmaslik va yarim bajarilgan holatda qolmaslik. Ayniqsa authorization qarorlarida: policy service javob bermasa, javob "allow" emas, "deny" bo'lishi lozim. Shu bilan birga xato xabarlari ichki tuzilish, stack trace, SQL yoki foydalanuvchi mavjudligi haqida ma'lumot bermasligi kerak.

**Spring'da qayerda uchraydi:** Spring Security'da `AccessDeniedException` va `AuthenticationException` `ExceptionTranslationFilter` tomonidan tutilib, `AccessDeniedHandler` / `AuthenticationEntryPoint` orqali 403/401 ga aylantiriladi - qaror "allow" ga aylanib ketmaydi. `@ControllerAdvice` + `ResponseEntityExceptionHandler` va `ProblemDetail` bilan umumiy, detalsiz xato javobi beriladi; `@ExceptionHandler(Exception.class)` esa oxirgi to'siq. Resilience4j yoki Spring Retry bilan circuit breaker ishlatganda fallback metodi `deny` qaytarishi kerak - `@CircuitBreaker(name="policy", fallbackMethod="denyAll")`. Tranzaksiya butunligi uchun `@Transactional` default'da `RuntimeException`'da rollback qiladi; checked exception uchun `rollbackFor` ko'rsatiladi. Login'da foydalanuvchi mavjudligini oshkor qilmaslik uchun `DaoAuthenticationProvider`'ning `hideUserNotFoundExceptions=true` (standart holat) `BadCredentialsException` qaytaradi.

```java
@CircuitBreaker(name = "policy", fallbackMethod = "deny")
public boolean canApprove(String user, String orderId) {
    return policyClient.check(user, orderId);
}

private boolean deny(String user, String orderId, Throwable t) {
    log.warn("policy unavailable, denying for {}", user, t);
    return false; // fail-closed
}
```

**Qo'llanish keyslari:**
- Tashqi OPA yoki policy service timeout bo'lganda to'lov tasdiqlashni rad etish.
- JWKS endpoint ishlamay qolganda cache'dagi kalit muddati tugagan bo'lsa token'ni qabul qilmaslik.
- Parol tiklash formasida email mavjud yoki yo'qligini bir xil javob bilan yashirish.
- Fayl shifrlash kaliti yuklanmagan bo'lsa application ishga tushmasligi (fast fail at startup).
- Rate limiter uchun Redis yiqilganda ehtiyot choralari bilan konservativ limit qo'llash.

**Ehtiyot bo'ling:** Fail-closed har doim to'g'ri emas - hayot xavfi bor tizimlarda yoki read-only kontentda to'liq deny availability hujumiga aylanishi mumkin, shuning uchun qarorni resurs nozikligiga qarab tanlang va buni arxitektura qarorlari yozuvida (ADR) qayd qiling. Catch bloklarida exception'ni "yutib" yuborib davom etish (`catch (Exception e) { }`) fail-secure emas, fail-silently - eng xavfli anti-pattern.

## 18.40 Vazifalarni ajratish (Separation of Duties)

**Tavsif:** Bitta subject nozik amalni boshidan oxirigacha yolg'iz bajara olmasligi kerak: yaratish va tasdiqlash, kod yozish va deploy qilish, konfiguratsiyani o'zgartirish va audit qilish huquqlari turli shaxslar yoki turli role'lar orasida bo'linadi. Bu ichki firibgarlik va yagona buzilgan akkaunt orqali to'liq nazoratni qo'lga olish xavfini kamaytiradi. Texnik jihatdan bu maker-checker (four-eyes) workflow, dual control va mutually exclusive role'lar ko'rinishida amalga oshiriladi.

**Spring'da qayerda uchraydi:** Maker-checker domain modelda holat mashinasi sifatida yoziladi (`DRAFT → PENDING_APPROVAL → APPROVED`) va `@PreAuthorize` ichida SpEL bilan tasdiqlovchining yaratuvchi emasligi tekshiriladi: `@PreAuthorize("hasRole('APPROVER') and #order.createdBy != authentication.name")`. Spring Statemachine yoki Spring Boot bilan Camunda/Flowable workflow engine'i ko'p qadamli approval uchun ishlatiladi. Mutually exclusive role'lar `UserDetailsService` / custom `AuthorizationManager` ichida tekshiriladi. Audit tomoni Hibernate Envers yoki `AuditorAware` bilan ajratiladi, audit store'ga application faqat insert huquqiga ega bo'ladi. Konfiguratsiya tomonida Spring Cloud Config repo'siga o'zgartirish faqat PR orqali kiradi, deploy esa alohida pipeline role'i bilan bajariladi.

**Qo'llanish keyslari:**
- Bank o'tkazmasini bitta operator yaratadi, boshqa operator tasdiqlaydi, uchinchisi hech qaysi bosqichni o'zgartira olmaydi.
- Mijoz limitini oshirish so'rovini sotuv menejeri kiritadi, risk bo'limi tasdiqlaydi.
- Production DB'ga migration'ni developer yozadi, lekin faqat release menejeri apply qiladi.
- Audit log'ni ko'rish huquqi faqat compliance role'ida, uni o'zgartirish huquqi hech kimda bo'lmasligi.
- Shifrlash kalitini bir jamoa generatsiya qiladi, boshqasi rotation jadvalini boshqaradi (dual control).

**Ehtiyot bo'ling:** Kichik jamoada separation of duties operatsiyani butunlay to'xtatib qo'yishi mumkin - shuning uchun "break-glass" protsedurasi (vaqtinchalik kengaytirilgan huquq + majburiy audit + keyingi review) oldindan loyihalanishi kerak, aks holda jamoa hamma huquqni bitta akkauntga yig'adi. SpEL ichida tekshiruvni `createdBy` maydoniga tayanib yozsangiz, bu maydon foydalanuvchi kiritgan payload'dan emas, server tomonidan to'ldirilganiga ishonch hosil qiling.

## 18.41 To'liq vositachilik (Complete Mediation)

**Tavsif:** Himoyalangan resursga har bir murojaat, har safar, markazlashgan nazorat nuqtasidan o'tib tekshirilishi kerak - oldingi muvaffaqiyatli tekshiruv natijasini keyingi so'rov uchun qayta ishlatib bo'lmaydi. Buning sababi: huquqlar orada o'zgargan bo'lishi mumkin (role olib tashlangan, token revoke qilingan, obyekt egasi o'zgargan). Pattern amalda hamma kirish yo'llarini bitta authorization qatlamidan o'tkazish va "yon eshik"larni (direct object reference, internal endpoint, cache'dagi qaror) yopish demakdir.

**Spring'da qayerda uchraydi:** `DelegatingFilterProxy` → `FilterChainProxy` → `SecurityFilterChain` servlet model'da barcha HTTP so'rovlar uchun yagona nazorat nuqtasi; WebFlux'da `WebFilterChainProxy` va `AuthorizationWebFilter`. Metod darajasida `@EnableMethodSecurity` AOP proxy yaratadi - lekin proxy self-invocation'da ishlamaydi, bu to'liq vositachilikni buzadigan tipik tuzoq. Obyekt darajasidagi tekshiruv uchun `@PostAuthorize("returnObject.ownerId == authentication.name")`, `@PreFilter`/`@PostFilter` yoki `AuthorizationManager` + Spring Security ACL. IDOR'ga qarshi repository query'siga tenant/owner shartini majburiy qo'shish: `findByIdAndOwnerId(...)`. Token revocation uchun OAuth2 introspection (`oauth2ResourceServer().opaqueToken()`) har bir so'rovda holatni tekshiradi, JWT esa tekshirmaydi.

**Qo'llanish keyslari:**
- `/api/orders/{id}` endpoint'ida har safar order egasini tekshirish, faqat ID ni bilish yetarli bo'lmasligi (IDOR himoyasi).
- GraphQL'da har bir field resolver darajasida authorization qo'llash, faqat root query'da emas.
- Fayl yuklab olish uchun pre-signed URL berish o'rniga har so'rovda huquqni qayta tekshiradigan controller ishlatish.
- Admin foydalanuvchi role'i olib tashlanganda ochiq sessiyalarni darhol bekor qilish (`SessionRegistry#expireNow`).
- Batch job ichida har bir yozuv uchun emas, har bir tenant kontekstida authorization'ni qayta o'rnatish.

**Ehtiyot bo'ling:** Authorization qarorini cache'lash (masalan permission'lar ro'yxatini sessiyada uzoq saqlash) to'liq vositachilikni buzadi - qisqa TTL va invalidation strategiyasi bo'lmasa, huquq olib tashlangan foydalanuvchi uzoq vaqt kirishda davom etadi. Yana bir tuzoq: service metodini o'z sinfi ichidan chaqirish (`this.secureMethod()`) `@PreAuthorize`'ni butunlay chetlab o'tadi.

## 18.42 Security kontekstini tarqatish (Security Context Propagation)

**Tavsif:** `SecurityContext` standart holda `ThreadLocal`da saqlanadi, shuning uchun amal boshqa thread'ga (async, executor, reactive scheduler, scheduled job, messaging listener) o'tganda authentication ma'lumoti yo'qoladi va metod-level authorization ishlamay qoladi yoki `AuthenticationCredentialsNotFoundException` paydo bo'ladi. Pattern kontekstni thread chegaralari orqali ongli ravishda ko'chirishni (yoki reactive'da `Context`ga bog'lashni) va ishdan keyin majburiy tozalashni talab qiladi. Distributed tizimda bu service chegarasidan token yoki on-behalf-of token uzatishni ham qamrab oladi.

**Spring'da qayerda uchraydi:** Servlet/imperative tomonda `DelegatingSecurityContextExecutor`, `DelegatingSecurityContextExecutorService`, `DelegatingSecurityContextRunnable`/`Callable` va `DelegatingSecurityContextAsyncTaskExecutor` kontekstni ko'chiradi; `SecurityContextHolder.setStrategyName(MODE_INHERITABLETHREADLOCAL)` child thread'larga meros beradi (thread pool bilan xavfli). Spring Security 6.x'da `SecurityContextHolderStrategy` bean sifatida inject qilinadi. Java 21+ virtual thread'lar bilan `ScopedValue` yondashuvi ham ishlatiladi, lekin Spring Security hali `ThreadLocal`ga tayanadi - har bir task uchun kontekstni aniq o'rnatish zarur. Reactive tomonda `ReactiveSecurityContextHolder.getContext()` Reactor `Context`dan o'qiydi, `AuthorizationWebFilter` uni o'rnatadi; `.contextWrite(ReactiveSecurityContextHolder.withAuthentication(auth))` bilan qo'lda qo'yiladi va `@PreAuthorize` reactive metodlarda `Mono`/`Flux` qaytarganda ishlaydi. Micrometer Context Propagation (`ContextSnapshot`, `ContextRegistry`) imperative va reactive o'rtasida ko'chirishni soddalashtiradi; `Hooks.enableAutomaticContextPropagation()` Boot 3.x'da ko'p holatni hal qiladi. Service'lar orasida token uzatish uchun `ServletBearerExchangeFilterFunction` (WebClient) yoki `OAuth2AuthorizedClientManager` bilan token exchange.

**Qo'llanish keyslari:**
- `@Async` metodda audit yozuvini yozishda `@CreatedBy` maydonining bo'sh qolmasligini ta'minlash.
- WebFlux'da reactive repository chaqirig'i oldidan `@PreAuthorize` tekshiruvi ishlashi uchun kontekstni `contextWrite` bilan uzatish.
- Kafka listener'da tenant kontekstini message header'dan tiklab, so'ng tenant-aware repository ishlatish.
- `CompletableFuture.supplyAsync` bilan parallel chaqiriqlarda downstream service'ga foydalanuvchi token'ini uzatish.
- Scheduled job uchun foydalanuvchi emas, maxsus system `Authentication` o'rnatish (`RunAs` yoki aniq `SecurityContext`).

**Ehtiyot bo'ling:** Thread pool'da kontekstni tozalamaslik eng xavfli xato - keyingi task boshqa foydalanuvchining huquqi bilan ishlaydi (kontekst "oqib ketishi"), shuning uchun `try/finally` da `SecurityContextHolder.clearContext()` yoki Spring'ning delegating wrapper'laridan foydalaning. `MODE_INHERITABLETHREADLOCAL` ni pool bilan ishlatish ayni shu muammoni keltirib chiqaradi, chunki thread qayta ishlatiladi.

## 18.43 Multi-tenant xavfsizlik (Multi-Tenant Security)

**Tavsif:** Ko'p ijarachili (multi-tenant) tizimda eng katta xavf - tenant ma'lumotlarining bir-biriga oqib ketishi (cross-tenant leakage). Pattern tenant identifikatorini ishonchli manbadan (token'dagi claim yoki issuer) olishni, uni butun request davomida kontekstda saqlashni va ma'lumotga har bir murojaatda avtomatik qo'llashni talab qiladi. "Issuer per tenant" yondashuvida har bir tenant o'z identity provider'iga (o'z issuer URI va JWKS'iga) ega bo'ladi, shu bilan authentication ham tenant bo'yicha izolyatsiya qilinadi.

**Spring'da qayerda uchraydi:** Spring Security'da ko'p issuer uchun `JwtIssuerAuthenticationManagerResolver` (servlet) yoki `JwtIssuerReactiveAuthenticationManagerResolver` (WebFlux) issuer claim'iga qarab mos `AuthenticationManager`/`JwtDecoder` tanlaydi; `spring.security.oauth2.resourceserver.jwt.issuer-uri` bitta issuer uchun, ko'p issuer esa kod bilan `fromTrustedIssuers(...)` orqali. Ma'lumot izolyatsiyasi uchun Hibernate'ning multi-tenancy qo'llab-quvvatlashi: `CurrentTenantIdentifierResolver` + `MultiTenantConnectionProvider` (schema yoki database per tenant), yoki discriminator yondashuvi uchun `@TenantId` (Hibernate 6.x) va `@FilterDef`/`@Filter`. Umumiy DB'da PostgreSQL row-level security'ni `SET app.tenant_id` bilan birgalikda ishlatish mumkin. Tenant kontekstini uzatish uchun `OncePerRequestFilter` + `ThreadLocal` (yoki reactive'da Reactor `Context`), cache'da tenant'ni kalit qismiga kiritish (`@Cacheable(key = "#tenant + ':' + #id")`).

**Qo'llanish keyslari:**
- SaaS CRM'da har bir korporativ mijoz o'z Keycloak realm'i (o'z issuer URI) bilan login qilishi.
- Umumiy jadvalda `tenant_id` discriminator va Hibernate `@TenantId` bilan har bir query'ga avtomatik filtr qo'shilishi.
- Nozik tenant'lar uchun "database per tenant" rejimiga ko'chirish, boshqalar uchun shared schema qoldirish.
- Redis cache kalitlariga tenant prefiksi qo'shib, cache orqali ma'lumot oqishini oldini olish.
- Tenant bo'yicha alohida rate limit va kvota belgilash, bitta tenant boshqalarni "to'sib qo'yishini" oldini olish (noisy neighbour).

**Ehtiyot bo'ling:** Tenant ID ni HTTP header'dan yoki path parametridan olib ishonish - eng katta xato; u faqat tekshirilgan token claim'idan yoki issuer'dan kelishi kerak, aks holda foydalanuvchi header'ni o'zgartirib boshqa tenant'ga kiradi. Native query, batch job, migration va cache qatlamlari Hibernate filtrini chetlab o'tadi, shuning uchun izolyatsiyani DB darajasidagi row-level security bilan qoplash va cross-tenant integration test yozish zarur.

## 18.44 Authorization Server yoki ichki auth tanlovi (Authorization Server vs Embedded Auth)

**Tavsif:** Bu arxitektura qarori: authentication va token berish mas'uliyatini alohida Authorization Server (OAuth2/OIDC provider) ga ajratish yoki har bir application ichida parol tekshirish va sessiya boshqaruvini saqlash. Alohida AS ko'p client, SSO, federatsiya, token exchange va markazlashgan audit kerak bo'lganda to'g'ri tanlov; embedded auth esa bitta monolit, kam foydalanuvchi va oddiy talablar uchun ancha arzon va tushunarli. Qaror client turlari soni, SSO talabi, compliance, operatsion imkoniyat va kalit boshqaruvi (key rotation) bo'yicha baholanadi.

**Spring'da qayerda uchraydi:** Alohida AS uchun Spring Authorization Server (`spring-boot-starter-oauth2-authorization-server`, `OAuth2AuthorizationServerConfigurer`, `RegisteredClientRepository`, `JWKSource`) yoki tashqi provider (Keycloak, Auth0, Okta, Entra ID). Resource service tomonida `spring-boot-starter-oauth2-resource-server` va `oauth2ResourceServer(o -> o.jwt(...))`; browser client uchun `spring-boot-starter-oauth2-client` va `oauth2Login()` (`ClientRegistrationRepository`, `OAuth2AuthorizedClientManager`). Embedded auth uchun `formLogin()`, `UserDetailsService`/`JdbcUserDetailsManager`, `DaoAuthenticationProvider`, `DelegatingPasswordEncoder`, `rememberMe()` va `spring-session-data-redis` bilan distributed session. Service-to-service uchun client credentials grant yoki mTLS (`X509AuthenticationFilter`). Spring Security 6.x'dan `WebSecurityConfigurerAdapter` olib tashlangan - konfiguratsiya `SecurityFilterChain` bean'lari bilan yoziladi.

**Qo'llanish keyslari:**
- Web, mobil va partner API uchun yagona SSO kerak bo'lganda markazlashgan Authorization Server tanlash.
- Bitta ichki admin paneli uchun ortiqcha infratuzilmani oldini olib `formLogin` + `JdbcUserDetailsManager` qoldirish.
- Korporativ mijozlarning SAML/OIDC identity provider'lari bilan federatsiya talab qilinganda tashqi IdP'ga o'tish.
- Monolitdan microservice'larga migratsiyada sessiya asosidagi auth'dan JWT resource server modeliga bosqichma-bosqich ko'chish (strangler yondashuvi).
- Mashina-mashina integratsiyasida foydalanuvchi parolini saqlamaslik uchun client credentials grant ishlatish.

**Ehtiyot bo'ling:** O'zingizning OAuth2/OIDC server implementatsiyasini noldan yozish yoki JWT'ni qo'lda "tekshirish" (signature, `exp`, `aud`, `iss`, algoritm almashtirish hujumi) juda tez xatoga olib keladi - Spring Authorization Server yoki yetuk provider'dan foydalaning. Boshqa tomondan, 20 foydalanuvchili ichki tool uchun alohida AS o'rnatish operatsion yukni (HA, kalit rotation, upgrade) oqlamaydi; JWT tanlasangiz esa darhol revocation strategiyasini (qisqa TTL yoki introspection) belgilab oling.

## 18.45 Yagona kirish (Single Sign-On (SSO))

**Tavsif:** SSO foydalanuvchiga bir marta autentifikatsiyadan o'tib, bir nechta mustaqil ilova va domenga qayta parol kiritmasdan kirish imkonini beradi. Markazda ishonchli Identity Provider (IdP) turadi: ilova (Service Provider / Relying Party) foydalanuvchini IdP'ga yo'naltiradi, IdP uni tekshirib, imzolangan assertion yoki token (SAML Response, OIDC `id_token`) qaytaradi. Shu bilan parol faqat bitta joyda - IdP'da saqlanadi, ilovalar esa faqat tokenni verifikatsiya qiladi. Natijada parol tarqalish yuzasi kamayadi, markazlashgan MFA, session policy va audit qilish mumkin bo'ladi.

**Spring'da qayerda uchraydi:** Spring Security 6.x (Spring Boot 3.x) `spring-boot-starter-oauth2-client` moduli OIDC SSO'ni beradi: `HttpSecurity.oauth2Login()`, `ClientRegistrationRepository` / `InMemoryClientRegistrationRepository`, `spring.security.oauth2.client.registration.*` va `.provider.*` property'lari (Keycloak, Okta, Entra ID, Google). Resource server tomonida `spring-boot-starter-oauth2-resource-server`, `oauth2ResourceServer().jwt()`, `JwtDecoder` (`NimbusJwtDecoder.withJwkSetUri(...)`), `JwtAuthenticationConverter`, `OAuth2AuthenticatedPrincipal`. SAML 2.0 uchun `spring-security-saml2-service-provider`: `saml2Login()`, `RelyingPartyRegistrationRepository`, `Saml2AuthenticatedPrincipal`. Service-to-service tarafda `OAuth2AuthorizedClientManager` va `ServletOAuth2AuthorizedClientExchangeFilterFunction` (WebClient) tokenni uzatadi; o'z IdP'ingizni qurish kerak bo'lsa Spring Authorization Server 1.x (`spring-boot-starter-oauth2-authorization-server`) `OidcUserInfo` va JWK endpoint'lari bilan ishlaydi. Logout uchun `OidcClientInitiatedLogoutSuccessHandler` (RP-initiated logout).

**Qo'llanish keyslari:**
- Korporativ xodimlar Entra ID yoki Okta hisobi bilan o'nlab ichki Spring Boot ilovalariga qayta login qilmasdan kiradi.
- B2B SaaS mijozlari o'z IdP'si (SAML yoki OIDC) orqali tenant-ga ulanadi - "enterprise SSO" talabi.
- Mikroservislar klasterida API Gateway foydalanuvchini bir marta autentifikatsiya qilib, downstream servislarga JWT uzatadi.
- Universitet yoki davlat portali bir hisob bilan bir nechta subdomen-xizmatga kirishni ta'minlaydi.
- Xodim ishdan bo'shaganda IdP'da hisobni o'chirish barcha ilovalardagi kirishni darhol to'xtatadi (markazlashgan deprovisioning).

**Ehtiyot bo'ling:** SSO yagona nuqtada ishdan chiqish (IdP pasa - hamma ilova pasa) va yagona o'g'irlanish nuqtasi yaratadi, shuning uchun IdP uchun HA, MFA va qisqa token TTL shart; `id_token` ni resurs serverga access token sifatida yubormang va `iss`/`aud`/`nonce`/imzoni albatta tekshiring. Shuningdek SSO faqat autentifikatsiyani markazlashtiradi - avtorizatsiya hali ham har bir ilovada qoladi, va global logout (back-channel logout) ko'pincha nazardan chetda qolib, chiqib ketgan foydalanuvchining sessiyasi boshqa ilovada tirik qoladi.

## 18.46 Munosabatga asoslangan kirish nazorati (Relationship-Based Access Control (ReBAC))

**Tavsif:** ReBAC huquqni rol yoki atribut emas, subject va resurs orasidagi munosabat grafi orqali hisoblaydi: "Ali bu hujjat joylashgan papkaning egasi bo'lgan jamoaning a'zosi, demak u hujjatni ko'rishi mumkin". Qarorlar `(subject, relation, object)` ko'rinishidagi tuple'lar ustida graf bo'ylab o'tish (transitive closure) bilan olinadi, shuning uchun chuqur ierarxiya va meros tabiiy ifodalanadi. Google Zanzibar maqolasi bu modelning sanoat standarti bo'lib, OpenFGA, SpiceDB, Ory Keto shu asosda qurilgan. RBAC'dan farqi: ruxsat resursga bog'langan va har bir obyekt uchun individual bo'lishi mumkin.

**Spring'da qayerda uchraydi:** Spring Security'da ReBAC uchun maxsus modul yo'q - bu infratuzilma (tashqi authorization server) yoki ma'lumotlar bazasi darajasidagi pattern, Spring ilova esa unga PDP (Policy Decision Point) sifatida murojaat qiladi. Amalda `AuthorizationManager<T>` yoki `PermissionEvaluator` interfeysini o'zingiz implement qilib, ichida OpenFGA/SpiceDB Java SDK (`dev.openfga:openfga-sdk`, `authzed` gRPC client) ga `check(user, relation, object)` so'rovi yuboriladi; so'ng `@PreAuthorize("hasPermission(#docId, 'document', 'viewer')")` yoki `@PreAuthorize("@fga.check(authentication, #docId, 'viewer')")` orqali metod darajasida qo'llanadi. Spring Security ACL moduli (`spring-security-acl`, `AclPermissionEvaluator`, `MutableAclService`) obyekt-darajali ruxsatni RDBMS jadvallarida saqlaydigan eski, ancha sodda variant - ierarxik grafni emas, ota-bola ACL zanjirini qo'llab-quvvatlaydi. Ro'yxat so'rovlari uchun PDP'dan ruxsat etilgan ID'lar olinib, Spring Data JPA `Specification` yoki JPQL `IN` sharti bilan filtrlanadi; PostgreSQL Row-Level Security ham shu vazifaga ishlatiladi.

```java
@Bean
AuthorizationManager<RequestAuthorizationContext> docViewer(OpenFgaClient fga) {
    return (auth, ctx) -> {
        String docId = ctx.getVariables().get("id");
        boolean ok = fga.check("user:" + auth.get().getName(), "viewer", "document:" + docId);
        return new AuthorizationDecision(ok);
    };
}
```

**Qo'llanish keyslari:**
- Google Docs uslubidagi fayl almashish: har bir hujjatga alohida egalik, "editor", "commenter" huquqlari va papkadan meros olish.
- Ko'p-tenantli SaaS'da tashkilot → bo'lim → loyiha → task ierarxiyasi bo'ylab ruxsatning avtomatik tarqalishi.
- GitHub kabi platformada organization owner barcha repo'larga, team maintainer esa faqat o'z team repo'lariga kirishi.
- Sog'liqni saqlash tizimida shifokor faqat o'zi davolayotgan bemorning yozuvlarini ko'rishi (care-team munosabati).
- Marketplace'da sotuvchi faqat o'z do'koniga tegishli buyurtmalarni ko'rishi.

**Ehtiyot bo'ling:** Har bir so'rovga tashqi PDP'ga sinxron `check` qilish latency va ishonchlilik muammosi tug'diradi - batch `batch-check`, lokal cache va graceful degradation strategiyasini oldindan o'ylang, lekin ruxsat cache'ini uzoq TTL bilan saqlash revoke'ni kechiktirib xavfsizlik teshigi ochadi. "Ruxsat etilgan narsalar ro'yxatini ber" (list/filter) so'rovlari ReBAC'ning eng og'riqli joyi: minglab ID'ni PDP'dan tortib keyin `IN (...)` qilish N+1 va pagination'ni buzadi, shuning uchun oddiy RBAC yetarli bo'lgan joyda ReBAC'ni majburan kiritmang.

## 18.47 Tokenizatsiya (Tokenization)

**Tavsif:** Tokenizatsiya maxfiy ma'lumotni (karta raqami, JSHSHIR, pasport, telefon) matematik aloqasi bo'lmagan surrogat qiymat - token bilan almashtiradi, asl qiymat esa alohida himoyalangan token vault'da saqlanadi. Shifrlashdan farqi shundaki, tokenda kalit yoki algoritm orqali tiklanadigan ma'lumot yo'q: faqat vault'dagi xaritalash orqali qaytarish mumkin. Ko'pincha format-preserving bo'ladi (token ham 16 xonali va oxirgi 4 raqami saqlangan), shuning uchun mavjud sxema va biznes logikani o'zgartirmasdan joriy etiladi. Asosiy foydasi - compliance perimetrini (PCI DSS scope) qisqartirish: asl ma'lumot sizning asosiy ilovangizga umuman tushmaydi.

**Spring'da qayerda uchraydi:** Bu birinchi navbatda infratuzilma/provayder darajasidagi pattern - Spring'da "Tokenization" degan sinf yo'q. Amalda Stripe (`PaymentMethod`/`SetupIntent` orqali karta brauzerda tokenlashtiriladi), Adyen, Braintree, yoki HashiCorp Vault Transform Secrets Engine (FPE/masking) ishlatiladi; Spring ilova faqat tokenni saqlaydi. Spring Vault (`spring-vault-core`, `VaultTemplate`, `VaultOperations`) yoki Spring Cloud Vault bilan `vault/transform/encode/{role}` va `decode` endpoint'lariga murojaat qilinadi; AWS'da `AWSPaymentCryptography` yoki DynamoDB-backed vault. Ilova tomonida token/asl qiymat chegarasini JPA `AttributeConverter` (`@Convert`) yoki `@JsonSerialize` bilan ushlab turish, detokenizatsiyani alohida mikroservisga ajratib `@PreAuthorize("hasAuthority('SCOPE_pan:detokenize')")` bilan yopish keng tarqalgan. Log'ga tushib ketmasligi uchun Logback `MaskingPatternLayout` yoki domen tipida `toString()` ni override qilish qo'llanadi.

**Qo'llanish keyslari:**
- E-commerce'da takroriy to'lov (card-on-file) uchun karta tokeni saqlanadi, PAN esa PCI-sertifikatlangan provayderda qoladi.
- Bank mobil ilovasida hisob raqami o'rniga token bilan ishlash, detokenizatsiya faqat core-banking perimetrida.
- HR/insurance tizimida JSHSHIR tokenlashtirilib, analytics va reporting token ustida ishlaydi.
- Test va staging muhitiga productiondan ma'lumot ko'chirilganda maxfiy maydonlar tokenga almashtiriladi.
- Ko'p servisli arxitekturada faqat bitta "vault service" asl qiymatni ko'radi, qolgan 30 servis token bilan yashaydi.

**Ehtiyot bo'ling:** Token vault yangi yagona nuqta bo'lib qoladi - uning backup, HA va kalit boshqaruvi butun tizim xavfsizligini belgilaydi, va detokenizatsiya API'si yetarlicha qattiq avtorizatsiya qilinmasa tokenizatsiyadan hech qanday foyda qolmaydi. Deterministik tokenlarni (bir xil PAN → bir xil token) joining uchun ishlatish qulay, lekin bu korrelyatsiya va lug'at hujumiga yo'l ochadi; tokenizatsiyani shifrlash, TLS yoki access control o'rnini bosuvchi deb emas, ularga qo'shimcha qatlam deb qaraganingiz to'g'ri.

## 18.48 Ma'lumotni maskalash (Data Masking)

**Tavsif:** Data Masking maxfiy ma'lumotni ko'rsatish yoki nusxalash vaqtida qisman yoki to'liq yashiradi (`**** **** **** 4242`, `a***@mail.com`), shunda foydalanuvchi vazifasini bajarishga yetadigan minimal ma'lumotni ko'radi. Ikki asosiy turi bor: static masking - productiondan test muhitiga ma'lumot ko'chirilganda asl qiymat butunlay va qaytarib bo'lmas tarzda almashtiriladi; dynamic masking - ma'lumot bazada asl holida qoladi, lekin so'rov natijasi foydalanuvchi roliga qarab niqoblanadi. Tokenizatsiyadan farqi: masking odatda bir tomonlama va asl qiymatni tiklash ko'zda tutilmagan. Maqsad - "need to know" printsipi, GDPR data minimization va log'lar orqali ma'lumot oqib ketishini oldini olish.

**Spring'da qayerda uchraydi:** Spring'da tayyor "masking" moduli yo'q, lekin bir necha standart nuqtada amalga oshiriladi. API javobida: Jackson `@JsonSerialize(using = MaskingSerializer.class)`, `@JsonIgnore` yoki `@JsonView` bilan maydonni rolga qarab chiqarmaslik, hamda alohida DTO/projection (Spring Data `interface`-based projection) qaytarish. Log'larda: Logback `PatternLayout` dan meros olgan maskalovchi layout, `MessageConverter`, yoki Spring Boot 3.x Actuator'da `management.endpoint.env.show-values=WHEN_AUTHORIZED` va `@ConfigurationProperties` ustida `sanitize` qoidalari (`SanitizingFunction` bean). Micrometer tracing/`HttpTraceFilter`'da header'larni (`Authorization`, `Cookie`) olib tashlash. Persistence darajasida JPA `AttributeConverter`, Hibernate `@ColumnTransformer`. Dinamik masking ko'pincha ma'lumotlar bazasi funksiyasi: Oracle Data Redaction, SQL Server Dynamic Data Masking, PostgreSQL `anon` extension yoki `VIEW` + Row-Level Security - Spring ilova shunchaki niqoblangan natijani oladi. Spring Security `AuthorizationProxyFactory` (Spring Security 6.3+) `@AuthorizeReturnObject` bilan qaytarilgan obyekt maydonlarini rolga qarab yopishga imkon beradi.

```java
public class MaskingSerializer extends JsonSerializer<String> {
    @Override
    public void serialize(String v, JsonGenerator g, SerializerProvider p) throws IOException {
        g.writeString(v == null || v.length() < 4 ? "****" : "****" + v.substring(v.length() - 4));
    }
}
```

**Qo'llanish keyslari:**
- Call-center operatori mijoz kartasining faqat oxirgi 4 raqamini ko'radi, to'liq PAN hech kimga ko'rinmaydi.
- Productiondan olingan dump test muhitiga static masking bilan ko'chiriladi, ishlab chiquvchilar real shaxsiy ma'lumotni ko'rmaydi.
- Log va APM (Datadog, Elastic) ga `Authorization` header, parol va token tushmasligi uchun filtrlash.
- Tibbiy yoki HR hisobotlarida analitik faqat agregat va niqoblangan identifikatorlar bilan ishlaydi.
- Qo'llab-quvvatlash xodimi mijoz profilini ko'radi, lekin JSHSHIR va bank rekvizitlari niqoblangan holatda.

**Ehtiyot bo'ling:** Maskani faqat UI yoki DTO darajasida qo'yish mumkin emas - asl qiymat baribir API javobi, GraphQL, export (CSV/Excel), Actuator endpoint'lari yoki stack trace orqali chiqib ketishi odatiy xato; masking qoidasini mumkin bo'lgan eng chuqur qatlamda (DB view, repository projection) qo'llang. Yana bir tuzoq - qisman masking deanonimizatsiyaga yo'l qoldirishi: tug'ilgan sana + pochta indeksi + jins kabi bir nechta "zararsiz" niqoblangan maydon birlashtirilganda shaxsni aniqlash mumkin, shuning uchun masking'ni shifrlash va access control o'rnini bosuvchi chora deb hisoblamang.

---

[&larr; 17. Resilience va cloud dizayn patternlari](17-resilience-va-cloud-dizayn-patternlari.md) · [Mundarija](README.md) · [19. Reactive patternlar &rarr;](19-reactive-patternlar.md)
