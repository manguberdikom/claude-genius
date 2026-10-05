<!-- doc: code-review | chapter: 30 | part: VI. Xavfsizlik review -->

[Barcha hujjatlar](../../README.md) / [Kod review](README.md)

# 30. Autentifikatsiya va avtorizatsiya review (Authentication and Authorization)

<details>
<summary>Bu bobdagi 10 bo'lim</summary>

- [30.1 IDOR: eng ko'p uchraydigan va eng oson o'tib ketadigan xato](#301-idor-eng-kop-uchraydigan-va-eng-oson-otib-ketadigan-xato)
- [30.2 Foydalanuvchi identifikatori qayerdan keladi](#302-foydalanuvchi-identifikatori-qayerdan-keladi)
- [30.3 Spring Security konfiguratsiyasi review](#303-spring-security-konfiguratsiyasi-review)
- [30.4 Metod darajasidagi xavfsizlik](#304-metod-darajasidagi-xavfsizlik)
- [30.5 Himoyasiz qolgan endpointlarni topish](#305-himoyasiz-qolgan-endpointlarni-topish)
- [30.6 JWT va token review](#306-jwt-va-token-review)
- [30.7 Ko'p tenantlik (multi-tenancy)](#307-kop-tenantlik-multi-tenancy)
- [30.8 Biznes mantiqini chetlab o'tish](#308-biznes-mantiqini-chetlab-otish)
- [30.9 Review checklisti: kirish nazorati](#309-review-checklisti-kirish-nazorati)
- [30.10 Amalda qo'llash](#3010-amalda-qollash)

</details>


Kirish nazorati xatolari zaifliklarning eng ko'p uchraydigan sinfi, va avtomatik instrumentlar ularni deyarli topmaydi. Sababi: "bu foydalanuvchi shu ma'lumotni ko'rishi kerakmi" degan savolga javob faqat domen bilimida bor. Shu sababli bu bob reviewer ning eng muhim xavfsizlik vazifasi haqida.

## 30.1 IDOR: eng ko'p uchraydigan va eng oson o'tib ketadigan xato

```java
// Zaiflik: ID so'rovdan keladi, egalik tekshirilmaydi.
@GetMapping("/orders/{id}")
public OrderResponse get(@PathVariable UUID id) {
    return OrderResponse.from(orders.findById(id).orElseThrow());
}
// Har qanday autentifikatsiya qilingan foydalanuvchi boshqa odamning
// buyurtmasini ko'radi. `@PreAuthorize("isAuthenticated()")` bu yerda
// hech narsa bermaydi - u faqat "kirgan" ekanini tekshiradi.

// Yechim 1 (eng ishonchli): so'rovda egalik sharti.
@GetMapping("/orders/{id}")
public OrderResponse get(@PathVariable UUID id, @AuthenticationPrincipal AppUser user) {
    return orders.findByIdAndCustomerId(id, user.customerId())
                 .map(OrderResponse::from)
                 .orElseThrow(OrderNotFound::new);     // 404, 403 emas
}
// Nega 404: 403 "bu buyurtma bor, lekin sizga tegishli emas" degan
// ma'lumot beradi - bu enumeratsiya uchun foydali signal.

// Yechim 2: aniq avtorizatsiya tekshiruvi (murakkab qoidalar uchun).
@PreAuthorize("@orderAccess.canRead(#id, authentication)")
@GetMapping("/orders/{id}")
public OrderResponse get(@PathVariable UUID id) { ... }

@Component("orderAccess")
public class OrderAccessPolicy {
    public boolean canRead(UUID orderId, Authentication auth) {
        AppUser user = (AppUser) auth.getPrincipal();
        if (user.hasRole("SUPPORT")) return true;              // qo'llab-quvvatlash
        return orders.existsByIdAndCustomerId(orderId, user.customerId());
    }
}
```

Review usuli: har bir endpoint uchun "bu resursni kim ko'rishi kerak" va "kod shuni qanday ta'minlaydi" savollari. Javob "`isAuthenticated()`" bo'lsa va resurs foydalanuvchiga tegishli bo'lsa - zaiflik.

## 30.2 Foydalanuvchi identifikatori qayerdan keladi

```java
// Blocker: foydalanuvchi o'z identifikatorini aytadi.
@PostMapping("/transfers")
public void transfer(@RequestBody TransferRequest req) {
    accounts.transfer(req.fromAccountId(), req.toAccountId(), req.amount());
}
// Hujumchi `fromAccountId` ga boshqa odamning hisobini qo'yadi.

// To'g'ri: identifikator autentifikatsiya kontekstidan, so'rovdan emas.
@PostMapping("/transfers")
public void transfer(@RequestBody @Valid TransferRequest req,
                     @AuthenticationPrincipal AppUser user) {
    // Hisob foydalanuvchiga tegishliligi tekshiriladi.
    Account from = accounts.findByIdAndOwner(req.fromAccountId(), user.id())
                           .orElseThrow(AccountNotFound::new);
    accounts.transfer(from.id(), req.toAccountId(), req.amount());
}
```

| So'rovdan olinmasligi kerak | Qayerdan olinadi |
| --- | --- |
| `userId`, `customerId` | `Authentication` principal |
| `tenantId` | Token claim yoki domen (subdomen) |
| Rol va huquqlar | Token yoki bazadan |
| Narx va chegirma | Serverda hisoblanadi |
| Buyurtma summasi | Serverda qatorlardan hisoblanadi |
| Status va holat | Server qoidasi bilan |
| `isAdmin` kabi bayroqlar | Hech qachon mijozdan |

## 30.3 Spring Security konfiguratsiyasi review

```java
// Review da diqqat bilan o'qiladigan kod: qoidalar tartibi muhim.
@Bean
SecurityFilterChain api(HttpSecurity http) throws Exception {
    return http
        .securityMatcher("/api/**")
        .authorizeHttpRequests(a -> a
            // DIQQAT: tartib muhim - birinchi mos kelgan qoida ishlaydi.
            .requestMatchers("/api/public/**").permitAll()
            .requestMatchers(HttpMethod.GET, "/api/orders/**").hasRole("USER")
            .requestMatchers("/api/admin/**").hasRole("ADMIN")
            .anyRequest().authenticated())          // standart: yopiq
        .csrf(csrf -> csrf.disable())               // nega? (quyida)
        .sessionManagement(s -> s.sessionCreationPolicy(STATELESS))
        .oauth2ResourceServer(o -> o.jwt(Customizer.withDefaults()))
        .build();
}
```

Review savollari shu konfiguratsiya uchun:

| Savol | Xavf |
| --- | --- |
| `anyRequest().authenticated()` oxirida bormi | Yangi endpoint himoyasiz ochiladi |
| `permitAll` naqshlari tor emasmi | `/api/**` ochiq qolishi |
| Qoidalar tartibi to'g'rimi | Keng qoida torini soya qiladi |
| `csrf.disable()` asoslanganmi | Sessiya bilan ishlasa - CSRF xavfi |
| Metod bo'yicha farq hisobga olinganmi | `GET` ochiq, `POST` yopiq |
| `permitAll` da `/actuator` yo'qmi | Diagnostika oshkor (21.7) |
| JWT tekshiruvi to'liqmi | Imzo, muddat, issuer, audience |
| Standart `anonymous` xulqi tushunilganmi | Autentifikatsiyasiz kirish |

```java
// CSRF: qachon o'chirish mumkin.
// - Agar autentifikatsiya FAQAT `Authorization` header orqali bo'lsa
//   (JWT, Bearer) - CSRF xavfi yo'q, o'chirish mumkin.
// - Agar cookie da sessiya yoki token bo'lsa - CSRF KERAK.
// Review izohi: "csrf disabled" bilan "cookie da token" birga bo'lsa -
// bu blocker. Cookie ni `SameSite=Strict` qilish qo'shimcha himoya,
// lekin yetarli emas.
```

## 30.4 Metod darajasidagi xavfsizlik

```java
// @PreAuthorize ning tipik xatolari.

// Xato 1: faqat autentifikatsiya tekshirilgan.
@PreAuthorize("isAuthenticated()")              // IDOR dan himoya qilmaydi

// Xato 2: rol tekshirilgan, egalik emas.
@PreAuthorize("hasRole('USER')")                // har qanday USER kira oladi

// Xato 3: `hasAuthority` va `hasRole` chalkashtirilgan.
@PreAuthorize("hasAuthority('ADMIN')")          // "ROLE_ADMIN" ni topmaydi
@PreAuthorize("hasRole('ADMIN')")               // "ROLE_" prefiksini o'zi qo'shadi

// Xato 4: annotatsiya proxy orqali o'tmaydigan joyda (18.1).
// private metod yoki shu klass ichidan chaqiruv - tekshiruv ishlamaydi.

// Xato 5: `@PostAuthorize` bilan ma'lumot allaqachon o'qilgan.
@PostAuthorize("returnObject.customerId == authentication.principal.customerId")
public Order find(UUID id) { ... }
// Ishlaydi, lekin: (1) ma'lumot bazadan o'qilgan va loglarda bo'lishi
// mumkin; (2) yon ta'sirli metodda kech bo'ladi; (3) ro'yxatlar uchun
// ishlamaydi. Afzal: so'rovda filtrlash.

// To'g'ri shakl: domen policy bean i, test bilan qoplangan.
@PreAuthorize("@orderAccess.canModify(#id, authentication)")
public void cancel(UUID id, String reason) { ... }
```

```java
// Avtorizatsiya qoidalarini test bilan qoplash: review ning talabi.
@SpringBootTest
@AutoConfigureMockMvc
class OrderAuthorizationTest {

    @Test
    @WithMockUser(username = "ali", roles = "USER")
    void userCannotReadAnotherCustomersOrder() throws Exception {
        UUID otherOrder = seedOrderFor("vali");
        mvc.perform(get("/api/orders/{id}", otherOrder))
           .andExpect(status().isNotFound());      // 404, 403 emas
    }

    @Test
    void anonymousIsRejected() throws Exception {
        mvc.perform(get("/api/orders/{id}", UUID.randomUUID()))
           .andExpect(status().isUnauthorized());
    }

    @Test
    @WithMockUser(roles = "USER")
    void userCannotAccessAdminEndpoints() throws Exception {
        mvc.perform(post("/api/admin/refunds"))
           .andExpect(status().isForbidden());
    }
}
```

## 30.5 Himoyasiz qolgan endpointlarni topish

```java
// Eng foydali test: har bir endpoint himoyalanganini tekshirish.
// Yangi endpoint qo'shilib, avtorizatsiya yozilmasa - CI gapiradi.
@SpringBootTest
class EndpointSecurityCoverageTest {

    @Autowired RequestMappingHandlerMapping mappings;

    // Ongli ravishda ochiq qoldirilgan yo'llar - aniq ro'yxat.
    private static final Set<String> PUBLIC = Set.of(
        "/api/public/health", "/api/public/version", "/api/auth/login");

    @Test
    void everyEndpointIsEitherPublicOrSecured() {
        List<String> unprotected = new ArrayList<>();
        mappings.getHandlerMethods().forEach((info, method) -> {
            String path = info.getPathPatternsCondition().getPatternValues()
                              .stream().findFirst().orElse("?");
            if (PUBLIC.contains(path)) return;
            boolean hasMethodSecurity =
                method.hasMethodAnnotation(PreAuthorize.class)
                || method.hasMethodAnnotation(PostAuthorize.class)
                || method.getBeanType().isAnnotationPresent(PreAuthorize.class);
            // Agar metod darajasida ham, filter chain da ham qoida bo'lmasa:
            if (!hasMethodSecurity && !coveredByFilterChain(path)) {
                unprotected.add(method.getMethod().getName() + " -> " + path);
            }
        });
        assertThat(unprotected)
            .as("himoyalanmagan endpointlar")
            .isEmpty();
    }
}
```

```bash
# Review paytida tez tekshirish: yangi endpointlar va ularning himoyasi.
git diff origin/main...HEAD -- '*.java' \
  | grep -E '^\+.*@(Get|Post|Put|Delete|Patch)Mapping' -A6 \
  | grep -E '^\+' \
  | grep -B6 -E 'public .*\(' \
  | grep -cE '@PreAuthorize|@Secured|@RolesAllowed' \
  || echo "OGOHLANTIRISH: yangi endpointlarda avtorizatsiya annotatsiyasi topilmadi"
```

## 30.6 JWT va token review

```java
// Review savollari har bir token tekshiruvi uchun.
@Bean
JwtDecoder jwtDecoder(@Value("${auth.issuer}") String issuer,
                      @Value("${auth.audience}") String audience) {
    NimbusJwtDecoder decoder = JwtDecoders.fromIssuerLocation(issuer);
    decoder.setJwtValidator(new DelegatingOAuth2TokenValidator<>(
        new JwtTimestampValidator(Duration.ofSeconds(30)),   // muddat + clock skew
        new JwtIssuerValidator(issuer),                      // kim bergan
        new JwtClaimValidator<List<String>>("aud",           // kimga berilgan
            aud -> aud != null && aud.contains(audience)),
        new JwtClaimValidator<String>("scope",               // qanday huquq
            scope -> scope != null)
    ));
    return decoder;
}
```

| Tekshiriladigan | Nega |
| --- | --- |
| Imzo va algoritm | `alg: none` yoki `HS256` bilan `RS256` almashtirish hujumi |
| `exp` va `nbf` | Muddati o'tgan token |
| `iss` | Boshqa provayder tokeni |
| `aud` | Boshqa servis uchun berilgan token |
| `scope`/`roles` | Huquqlar |
| Bekor qilish | Chiqib ketgan foydalanuvchi tokeni hali amal qiladi |
| Muddat uzunligi | 24 soatlik access token - juda uzun |
| Saqlash joyi | `localStorage` da XSS bilan o'g'irlanadi |

```java
// Token dagi ma'lumotga ishonish chegarasi.
// Token imzolangan, ya'ni tarkibi o'zgartirilmagan. LEKIN:
// - undagi rol eskirgan bo'lishi mumkin (foydalanuvchi huquqi olib tashlangan);
// - undagi `customerId` boshqa tizimdan kelgan va tekshirilmagan bo'lishi mumkin.
// Review savoli: kritik huquqlar (to'lov, admin) har safar bazadan
// tekshiriladimi yoki tokenga ishonamizmi?
```

## 30.7 Ko'p tenantlik (multi-tenancy)

```java
// Eng xavfli xato sinfi: tenant filtri bitta joyda esdan chiqadi.
// Natijada bir mijoz boshqa mijozning ma'lumotini ko'radi.

// Zaif: tenant filtri qo'lda, har so'rovda.
List<Order> orders = repository.findByStatus(OPEN);   // tenant filtri YO'Q!

// Himoya 1: PostgreSQL Row Level Security - eng ishonchli.
```

```sql
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
CREATE POLICY orders_tenant_isolation ON orders
    USING (tenant_id = current_setting('app.tenant_id')::uuid);
-- Ilova har tranzaksiya boshida tenant ni o'rnatadi:
--   SET LOCAL app.tenant_id = '...';
-- Filtr esdan chiqsa ham, baza ma'lumot bermaydi. Bu "fail closed" dizayn.
```

```java
// Tenant ni tranzaksiya boshida o'rnatish.
@Component
public class TenantConnectionInitializer {
    @EventListener
    public void onTransactionStart(TransactionStartedEvent e) {
        jdbc.update("SET LOCAL app.tenant_id = ?", TenantContext.require().value());
    }
}
// Review savollari: (1) tenant qayerdan keladi (token, subdomen - so'rov
// tanasidan EMAS); (2) o'rnatilmagan bo'lsa nima bo'ladi (so'rov yiqilishi
// kerak, hamma ma'lumot qaytmasligi); (3) `SET LOCAL` pool da oqib
// ketmaydimi (LOCAL tranzaksiya oxirida tozalanadi - shuning uchun LOCAL);
// (4) keshlar tenant bo'yicha ajratilganmi (16.4);
// (5) batch va worker ishlar tenant kontekstini to'g'ri o'rnatadimi.
```

## 30.8 Biznes mantiqini chetlab o'tish

Bu zaiflik sinfi avtomatik instrumentlar uchun ko'rinmas, chunki kodda hech qanday "xavfli funksiya" yo'q.

```java
// Naqsh 1: narx mijozdan keladi.
public record CheckoutRequest(List<LineRequest> lines, BigDecimal totalPrice) { }
// Hujumchi `totalPrice = 0.01` yuboradi. Review: narx serverda hisoblanadi.

// Naqsh 2: holat o'tishi tekshirilmaydi.
@PostMapping("/orders/{id}/ship")
public void ship(@PathVariable UUID id) {
    orders.markShipped(id);                     // to'lanmagan buyurtmani jo'natish
}
// Review: holat o'tish qoidasi domen ichida (10.6).

// Naqsh 3: qadamlar tartibi majburlanmaydi.
// Ko'p qadamli jarayonda (ro'yxatdan o'tish, buyurtma) hujumchi oraliq
// qadamni o'tkazib yuborishi mumkin: /checkout/confirm ni to'lovdan oldin.
// Review savoli: har qadam oldingi qadam bajarilganini tekshiradimi?

// Naqsh 4: chegara va kvota tekshirilmaydi.
// Chegirma kodini 1000 marta ishlatish, bitta aksiyadan 500 marta foyda olish.
// Review savoli: ishlatish soni qayerda hisoblanadi va u poygaga chidamlimi
// (27.2)?

// Naqsh 5: salbiy va chegaraviy qiymatlar.
public void refund(OrderId id, Money amount) { ... }
// amount manfiy bo'lsa - pul olish. amount buyurtma summasidan katta
// bo'lsa - ortiqcha qaytarish. Review: ikkisi ham tekshirilishi kerak.
```

## 30.9 Review checklisti: kirish nazorati

| Savol | Nega |
| --- | --- |
| Har endpoint avtorizatsiya qoidasiga egami | Himoyasiz endpoint |
| Resurs egaligi tekshiriladimi | IDOR |
| Foydalanuvchi ID si so'rovdan olinmaydimi | O'zgalar nomidan harakat |
| Ro'yxatlar foydalanuvchi bo'yicha filtrlanganmi | Ommaviy ma'lumot oqishi |
| `404` yoki `403` tanlovi ongli qilinganmi | Enumeratsiya |
| `anyRequest().authenticated()` oxirida bormi | Yangi endpoint ochiq |
| `permitAll` naqshlari tormi | Ortiqcha ochiqlik |
| CSRF holati autentifikatsiya shakliga mosmi | CSRF hujumi |
| JWT da `iss`, `aud`, `exp` tekshiriladimi | Boshqa tokenni qabul qilish |
| Kritik huquqlar bazadan tekshiriladimi | Eskirgan token |
| Tenant izolyatsiyasi majburlanganmi (RLS) | Tenant orasida oqish |
| Narx, summa, status serverda hisoblanadimi | Biznes mantiqini chetlab o'tish |
| Manfiy va chegaraviy qiymatlar tekshirilganmi | Pul yo'nalishini teskari qilish |
| Avtorizatsiya qoidalari test bilan qoplanganmi | Regressiya |

## 30.10 Amalda qo'llash

- [ ] Barcha endpointlarni ro'yxatga olib, har biri uchun "kim kira oladi" va "kod buni qanday ta'minlaydi" ustunlarini to'ldiring.
- [ ] `isAuthenticated()` yoki faqat rol bilan himoyalangan, lekin foydalanuvchi resursiga tegadigan endpointlarni toping - har biri IDOR.
- [ ] So'rov tanasidan yoki parametrdan `userId`, `customerId`, `tenantId` oladigan joylarni toping va autentifikatsiya kontekstiga o'tkazing.
- [ ] Himoyalanmagan endpointlarni aniqlaydigan testni (30.5) qo'shib, CI ga kiriting.
- [ ] JWT dekoder sozlamalarida `iss`, `aud`, `exp` va algoritm tekshiruvi borligini tasdiqlang.
- [ ] Ko'p tenantli bo'lsa, PostgreSQL RLS ni yoqib, tenant filtri esdan chiqishiga chidamli dizayn qiling.
- [ ] Narx, chegirma va summa mijozdan keladigan joylarni toping va serverda hisoblashga o'tkazing.
- [ ] Har bir holat o'tishi va ko'p qadamli jarayon uchun oldingi qadam tekshiruvini qo'shing.
- [ ] Avtorizatsiya uchun kamida uchta test yozing: egasi ko'radi, boshqa foydalanuvchi ko'rmaydi, anonim rad etiladi.

---

[&larr; 29. Injection review: SQL va boshqalar](29-injection-review-sql-va-boshqalar.md) · [Mundarija](README.md) · [31. Kirish va chiqish xavfsizligi: SSRF, deserializatsiya, fayllar &rarr;](31-kirish-va-chiqish-xavfsizligi-ssrf.md)
