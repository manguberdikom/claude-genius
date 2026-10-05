<!-- doc: testing | chapter: 11 | part:  -->

[Barcha hujjatlar](../../README.md) / [Testlash qo'llanmasi](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 11. Xavfsizlik, tranzaksiya, asinxron va konkurentlik testlari (Testing Security, Transactions, Async & Concurrency)

<details>
<summary>Bu bobdagi 15 bo'lim</summary>

- [11.1 Spring Security'ni testlash asoslari](#111-spring-securityni-testlash-asoslari)
- [11.2 Avtorizatsiya qoidalarini testlash](#112-avtorizatsiya-qoidalarini-testlash)
- [11.3 Method security'ni testlash](#113-method-securityni-testlash)
- [11.4 OAuth2 va JWT: Resource Server'ni testlash](#114-oauth2-va-jwt-resource-serverni-testlash)
- [11.5 CSRF, CORS, security header va sessiya](#115-csrf-cors-security-header-va-sessiya)
- [11.6 Xavfsizlik testining chegarasi](#116-xavfsizlik-testining-chegarasi)
- [11.7 Tranzaksiya chegaralarini testlash](#117-tranzaksiya-chegaralarini-testlash)
- [11.8 Optimistik va pessimistik lock'ni testlash](#118-optimistik-va-pessimistik-lockni-testlash)
- [11.9 Asinxron kodni testlash](#119-asinxron-kodni-testlash)
- [11.10 Spring event'larni testlash](#1110-spring-eventlarni-testlash)
- [11.11 Scheduled task va job'larni testlash](#1111-scheduled-task-va-joblarni-testlash)
- [11.12 Konkurentlik va poyga holatini testlash](#1112-konkurentlik-va-poyga-holatini-testlash)
- [11.13 Retry, timeout va circuit breaker'ni testlash](#1113-retry-timeout-va-circuit-breakerni-testlash)
- [11.14 Anti-patternlar](#1114-anti-patternlar)
- [11.15 Arxitektor nazorat ro'yxati](#1115-arxitektor-nazorat-royxati)

</details>



Xavfsizlik, tranzaksiya, asinxronlik va konkurentlik - Spring ilovalarining eng ko'p buziladigan, ammo eng kam testlanadigan to'rt sohasi. Bu yerdagi xatolar kompilyatsiya vaqtida ko'rinmaydi: ular production'da noto'g'ri ruxsat, yarim commit bo'lgan ma'lumot yoki ikki marta yechilgan to'lov ko'rinishida chiqadi. Bobda har bir sohani Spring Security 6.x, Spring Boot 3.x/4.x, JUnit 5, Awaitility, Spring Retry va Resilience4j vositalari bilan deterministik testga qanday aylantirish mumkinligini ko'ramiz. Arxitektor uchun asosiy savol - qaysi qoida testga majburan qoplanishi kerak va qaysi chegaradan keyin test emas, boshqa vosita turi kerak.

## 11.1 Spring Security'ni testlash asoslari

`spring-security-test` moduli (`testImplementation 'org.springframework.security:spring-security-test'`) ikki xil mexanizm beradi. Birinchisi - annotatsiyalar: `@WithMockUser` soxta `Authentication` yaratadi, `@WithAnonymousUser` kontekstni anonim holatga qo'yadi, `@WithUserDetails` esa haqiqiy `UserDetailsService` bean'idan foydalanuvchini yuklaydi (shuning uchun u rol xaritalashdagi xatoni ham ushlaydi). Ikkinchisi - `SecurityMockMvcRequestPostProcessors`: `user()`, `jwt()`, `opaqueToken()`, `csrf()`. Post-processor'lar afzal, chunki ularni parametrlashtirilgan testga uzatish mumkin. `@WebMvcTest` sizning `SecurityFilterChain` konfiguratsiyangizni skan qilmaydi - uni `@Import` bilan qo'shish shart, aks holda test real qoidalarni emas, Boot'ning default himoyasini tekshiradi.

```java
@WebMvcTest(OrderController.class)
@Import(SecurityConfig.class)   // SecurityFilterChain avtomatik skan QILINMAYDI
class OrderControllerSecurityTest {

    @Autowired MockMvc mvc;
    @MockitoBean OrderService orderService;   // Boot 3.4+; oldin @MockBean

    @Test @WithMockUser(username = "ali", roles = "USER")
    void userSeesOwnOrders() throws Exception {
        mvc.perform(get("/api/orders")).andExpect(status().isOk());
    }

    @Test @WithAnonymousUser
    void anonymousGetsUnauthorized() throws Exception {
        mvc.perform(get("/api/orders")).andExpect(status().isUnauthorized());
    }

    @Test @WithUserDetails("manager@acme.io")
    void managerCanDeleteWithCsrf() throws Exception {
        mvc.perform(delete("/api/orders/1").with(csrf()))
           .andExpect(status().isNoContent());
    }

    @Test @WithMockUser(roles = "MANAGER")
    void missingCsrfTokenIsForbidden() throws Exception {
        mvc.perform(delete("/api/orders/1")).andExpect(status().isForbidden());
    }
}
```

Reaktiv stack'da ekvivalenti `WebTestClient` va `SecurityMockServerConfigurers` (`mockUser()`, `mockJwt()`, `mockOpaqueToken()`) bo'ladi; ular `mutateWith()` orqali bitta so'rovga qo'llanadi.

```java
@SpringBootTest(webEnvironment = WebEnvironment.RANDOM_PORT)   // WebFlux
@AutoConfigureWebTestClient
class ReportApiSecurityTest {

    @Autowired WebTestClient client;

    @Test
    void scopeReportsReadIsAllowed() {
        client.mutateWith(mockJwt().jwt(j -> j.claim("scope", "reports:read")))
              .get().uri("/api/reports")
              .exchange().expectStatus().isOk();
    }
}
```

## 11.2 Avtorizatsiya qoidalarini testlash

Avtorizatsiya - bu matritsa, demak uni matritsa sifatida testlash kerak: rol x endpoint x kutilgan HTTP status. Bu jadval arxitektura artefakti bo'lib, kodda bitta joyda (test `@MethodSource`'ida yoki CSV faylda) yashashi va yangi endpoint qo'shilganda majburan to'ldirilishi lozim. Eng muhim qatorlar - ruxsat berilganlar emas, **rad etilganlar**: `403` kutilgan hollar regressiyani birinchi ushlaydi. `401` va `403` ni aralashtirib yubormang: autentifikatsiya yo'q - `401`, bor-u huquq yo'q - `403`.

| Endpoint | Metod | ANONYMOUS | ROLE_USER | ROLE_MANAGER | ROLE_ADMIN |
|---|---|---|---|---|---|
| /api/orders | GET | 401 | 200 | 200 | 200 |
| /api/orders | POST | 401 | 201 | 201 | 201 |
| /api/orders/{id} | DELETE | 401 | 403 | 204 | 204 |
| /api/orders/{id}/refund | POST | 401 | 403 | 403 | 200 |
| /api/admin/users | GET | 401 | 403 | 403 | 200 |
| /actuator/health | GET | 200 | 200 | 200 | 200 |
| /actuator/env | GET | 401 | 403 | 403 | 200 |

```java
@SpringBootTest
@AutoConfigureMockMvc
class AuthorizationMatrixTest {

    @Autowired MockMvc mvc;

    record Rule(String role, HttpMethod method, String path, int expected) {}

    static Stream<Rule> matrix() {
        return Stream.of(
            new Rule("ANON",    HttpMethod.GET,    "/api/orders",          401),
            new Rule("USER",    HttpMethod.GET,    "/api/orders",          200),
            new Rule("USER",    HttpMethod.DELETE, "/api/orders/1",        403),
            new Rule("MANAGER", HttpMethod.DELETE, "/api/orders/1",        204),
            new Rule("MANAGER", HttpMethod.POST,   "/api/orders/1/refund", 403),
            new Rule("ADMIN",   HttpMethod.POST,   "/api/orders/1/refund", 200));
    }

    @ParameterizedTest(name = "{0}")
    @MethodSource("matrix")
    void endpointFollowsMatrix(Rule r) throws Exception {
        var req = request(r.method(), r.path()).with(csrf());
        if (!"ANON".equals(r.role())) req = req.with(user("t").roles(r.role()));
        mvc.perform(req).andExpect(status().is(r.expected()));
    }
}
```

Qo'shimcha nazorat: `RequestMappingHandlerMapping` bean'idan barcha mapping'larni olib, ularning har biri matritsada borligini tasdiqlaydigan test yozing. Shunda "yangi endpoint qo'shdim, security qoidasini yozishni esdan chiqardim" holati CI'da qulaydi.

## 11.3 Method security'ni testlash

`@EnableMethodSecurity` bilan `@PreAuthorize`/`@PostAuthorize` AOP proxy orqali ishlaydi, demak testda bean kontekstdan olinishi shart - `new AccountService()` hech narsani tekshirmaydi. `@WithMockUser` ishlaydi, chunki u `TestSecurityContextHolder` orqali `SecurityContextHolder`'ni to'ldiradi. Ba'zan rolni dinamik yasash kerak bo'ladi - o'shanda `SecurityContext`'ni qo'lda to'ldirib, `finally` blokida tozalash kerak. `@PostAuthorize` uchun yodda tuting: metod allaqachon bajarilib bo'lgan, shuning uchun test yon ta'sir (yozuv) rollback bo'lganini ham tekshirishi lozim.

```java
@SpringBootTest
class AccountServiceSecurityTest {

    @Autowired AccountService service;   // @PreAuthorize("hasRole('ADMIN')")

    @Test
    @WithMockUser(roles = "SUPPORT")
    void supportCannotCloseAccount() {
        assertThatThrownBy(() -> service.close(42L))
            .isInstanceOf(AccessDeniedException.class);
    }

    @Test
    void manualSecurityContextIsHonoured() {
        var ctx = SecurityContextHolder.createEmptyContext();
        ctx.setAuthentication(new UsernamePasswordAuthenticationToken(
                "ops", "n/a", List.of(new SimpleGrantedAuthority("ROLE_ADMIN"))));
        SecurityContextHolder.setContext(ctx);
        try {
            assertThat(service.close(42L)).isTrue();
        } finally {
            SecurityContextHolder.clearContext();
        }
    }
}
```

Spring Security 6.3+ da method security `AuthorizationDeniedException` tashlaydi - u `AccessDeniedException`'ning merosxo'ri, shuning uchun yuqoridagi assertion ikkala versiyada ham o'tadi.

## 11.4 OAuth2 va JWT: Resource Server'ni testlash

Resource Server'da asosiy xavf - claim'dan authority'ga xaritalash. Default `JwtGrantedAuthoritiesConverter` `scope`/`scp` claim'ini `SCOPE_` prefiksi bilan authority'ga aylantiradi. `jwt()` post-processor'iga `.jwt(...)` bilan claim bersangiz, shu konverter ishga tushadi va siz real xaritalashni testlaysiz; `.authorities(...)` bersangiz esa konverterni chetlab o'tasiz va buzuq Keycloak `realm_access` parser'i testda ko'rinmay qoladi. Shuning uchun maxsus konverter uchun doim claim darajasidan boshlang.

```java
@Test
void scopeClaimBecomesScopeAuthority() throws Exception {
    mvc.perform(get("/api/reports").with(jwt()
            .jwt(j -> j.subject("svc-1").claim("scope", "reports:read"))))
       .andExpect(status().isOk());
}

@Test
void customAuthorityConverterIsExercised() throws Exception {
    mvc.perform(get("/api/admin/metrics").with(jwt().jwt(j -> j
            .claim("realm_access", Map.of("roles", List.of("admin"))))))
       .andExpect(status().isOk());   // realm_access -> ROLE_admin
}

@Test
void opaqueTokenWithoutScopeIsForbidden() throws Exception {
    mvc.perform(get("/api/reports").with(opaqueToken()
            .attributes(a -> a.put("sub", "svc-1"))))
       .andExpect(status().isForbidden());
}
```

`jwt()` imzo, `iss`, `aud` va `exp` tekshiruvini butunlay o'tkazib yuboradi. Shu sababli kamida bitta test real token oqimini bosib o'tishi kerak: RSA kalit juftini testda generatsiya qilib, JWKS'ni mock HTTP server orqali uzatish va `spring.security.oauth2.resourceserver.jwt.jwk-set-uri` ni unga yo'naltirish, yoki Keycloak Testcontainer'dan haqiqiy `access_token` olish ([8-bobga](08-testcontainers-bilan-real-infratuzilmada.md) qarang). Issuer validatsiyasining buzilishi aynan shu testda ushlanadi.

## 11.5 CSRF, CORS, security header va sessiya

`csrf()` post-processor'i to'g'ri token qo'shadi; `csrf().useInvalidToken()` esa himoya haqiqatan ishlayotganini tasdiqlaydi. Stateless JWT API'da CSRF'ni o'chirish o'rinli, lekin bu qaror testda yozilgan bo'lishi kerak. Security header'lar bo'yicha diqqat: HSTS faqat `secure` so'rovda yuboriladi, shuning uchun MockMvc'da `.secure(true)` kerak. CORS preflight noto'g'ri origin'dan kelganda Spring Security `403` qaytaradi.

```java
@SpringBootTest
@AutoConfigureMockMvc
class HttpSecurityContractTest {

    @Autowired MockMvc mvc;

    @Test @WithMockUser
    void defaultSecurityHeadersAreSent() throws Exception {
        mvc.perform(get("/api/orders").secure(true))   // HSTS faqat HTTPS'da
           .andExpect(header().string("X-Content-Type-Options", "nosniff"))
           .andExpect(header().string("X-Frame-Options", "DENY"))
           .andExpect(header().exists("Strict-Transport-Security"));
    }

    @Test
    void preflightFromUnknownOriginIsRejected() throws Exception {
        mvc.perform(options("/api/orders")
                .header(HttpHeaders.ORIGIN, "https://evil.example")
                .header(HttpHeaders.ACCESS_CONTROL_REQUEST_METHOD, "GET"))
           .andExpect(status().isForbidden());
    }

    @Test
    void statelessApiCreatesNoHttpSession() throws Exception {
        var result = mvc.perform(get("/api/orders").with(jwt())).andReturn();
        assertThat(result.getRequest().getSession(false)).isNull();
    }
}
```

Sessiya boshqaruvi uchun ikki testni unutmang. Session fixation: `MockHttpSession` bilan login qilib, `result.getRequest().getSession(false).getId()` login oldidagi id'dan farq qilishini tasdiqlang (default strategiya `changeSessionId`). Concurrent session: `maximumSessions(1)` qo'yilganda ikkinchi login'dan keyin `SessionRegistry.getAllSessions(principal, false)` bitta yozuv qoldirishini va birinchi sessiya `isExpired()` bo'lishini tekshiring.

## 11.6 Xavfsizlik testining chegarasi

Unit va integration testlar faqat **siz yozgan qoidalarni** tekshiradi: matritsa bo'yicha endpoint himoyalanganmi, claim to'g'ri xaritalanganmi, CSRF yoqilganmi. Ular noma'lum zaifliklarni, dependency CVE'larini, noto'g'ri sozlangan infrastrukturani, SQL injection yoki IDOR'ni tizimli qidirmaydi. Bu ishlar uchun alohida qatlam kerak: SAST (kod tahlili), dependency scanning, DAST va qo'lda penetration test - ular [13-bobda](13-nofunksional-testlar-performance-resilience.md) ko'rilgan. Test strategiyasida bu chegarani yozib qo'ying, aks holda "100% security test qoplangan" degan yolg'on xotirjamlik paydo bo'ladi.

## 11.7 Tranzaksiya chegaralarini testlash

Tranzaksiya testida birinchi qoida: **test metodining o'ziga `@Transactional` qo'ymang**. Aks holda hamma narsa bitta tranzaksiyada bo'lib, oxirida rollback qilinadi - propagation va commit xatti-harakatini ko'rish imkonsiz. Haqiqiy baza (Testcontainers, [8-bob](08-testcontainers-bilan-real-infratuzilmada.md)) va yozuvlarni tashqaridan sanash kerak. `REQUIRES_NEW` yangi connection oladi, shuning uchun test profilida pool hajmi kamida 2 bo'lsin. `NESTED` savepoint talab qiladi: `JpaTransactionManager` uni faqat `setNestedTransactionAllowed(true)` bilan va dialekt qo'llab-quvvatlasa bajaradi. Eng ko'p uchraydigan tuzoq - checked exception default holda rollback qilmaydi.

```java
@SpringBootTest                       // DIQQAT: test metodida @Transactional YO'Q
class TransactionBoundaryTest {

    @Autowired OrderFacade facade;    // REQUIRED, ichida audit REQUIRES_NEW
    @Autowired OrderRepository orders;
    @Autowired AuditRepository audits;
    @Autowired JdbcTemplate jdbc;

    @AfterEach void cleanUp() { jdbc.execute("truncate orders, audit_log"); }

    @Test
    void requiresNewCommitsEvenIfOuterRollsBack() {
        assertThatThrownBy(() -> facade.placeAndFail("SKU-1"))
            .isInstanceOf(IllegalStateException.class);

        assertThat(orders.count()).isZero();   // tashqi REQUIRED rollback
        assertThat(audits.count()).isOne();    // ichki REQUIRES_NEW commit
    }

    @Test
    void checkedExceptionCommitsUnlessRollbackForIsSet() {
        assertThatThrownBy(() -> facade.placeAndThrowChecked("SKU-2"))
            .isInstanceOf(QuotaExceededException.class);

        assertThat(orders.count()).isOne();    // klassik tuzoq: rollback bo'lmadi
    }
}
```

Self-invocation muammosini ham test bilan ushlash mumkin: proxy chetlab o'tilganda tranzaksiya umuman boshlanmaydi.

```java
@Service
public class ReportService {

    @Transactional
    public boolean proxied() {
        return TransactionSynchronizationManager.isActualTransactionActive();
    }

    public boolean viaSelfCall() { return proxied(); }   // proxy chetlab o'tiladi
}

// Test (service bean kontekstdan olinadi):
assertThat(service.proxied()).isTrue();
assertThat(service.viaSelfCall()).isFalse();   // self-invocation fosh bo'ldi
```

Oraliq holatni tekshirish uchun `TestTransaction.flagForCommit()` va `TestTransaction.end()` yordam beradi: testning o'rtasida commit qilib, keyin yangi tranzaksiyada natijani o'qish mumkin.

## 11.8 Optimistik va pessimistik lock'ni testlash

`@Version` bilan to'qnashuvni thread'lar bilan yasash mumkin, lekin bu beqaror chiqadi. Deterministik yo'l - bitta thread'da ikkita `EntityManager` ochib, ikkisi ham bir xil versiyani o'qib, birin-ketin commit qilish: ikkinchi commit kafolatli yiqiladi.

```java
@SpringBootTest
class OptimisticLockTest {

    @Autowired EntityManagerFactory emf;
    @Autowired ProductRepository repo;

    @Test
    void staleVersionIsRejectedOnCommit() {
        Long id = repo.save(new Product("A", 100)).getId();
        var em1 = emf.createEntityManager();
        var em2 = emf.createEntityManager();
        try {
            em1.getTransaction().begin();
            em2.getTransaction().begin();
            Product p1 = em1.find(Product.class, id);   // version = 0
            Product p2 = em2.find(Product.class, id);   // version = 0

            p1.setPrice(110);
            em1.getTransaction().commit();              // version -> 1

            p2.setPrice(120);
            assertThatThrownBy(() -> em2.getTransaction().commit())
                .isInstanceOf(RollbackException.class)
                .hasCauseInstanceOf(OptimisticLockException.class);
        } finally { em1.close(); em2.close(); }
    }
}
```

Service qatlami orqali kelganda Spring bu xatoni `ObjectOptimisticLockingFailureException`'ga o'raydi - retry logikasi borligini ham shu turdagi assertion bilan tekshiring. Pessimistik lock uchun esa lock'ni ushlab turuvchi ikkinchi tranzaksiya kerak; `Thread.sleep` emas, `CountDownLatch` bilan koordinatsiya qiling. Lock timeout hint'i DB'ga bog'liq: PostgreSQL'da `0` qiymati `FOR UPDATE NOWAIT`ga aylanadi.

```java
public interface SeatRepository extends JpaRepository<Seat, Long> {
    @Lock(LockModeType.PESSIMISTIC_WRITE)
    @QueryHints(@QueryHint(name = "jakarta.persistence.lock.timeout", value = "0"))
    @Query("select s from Seat s where s.id = :id")
    Optional<Seat> findByIdForUpdate(@Param("id") Long id);
}

@Test
void secondTransactionCannotTakeTheSameRowLock() throws Exception {
    var locked = new CountDownLatch(1);
    var release = new CountDownLatch(1);
    var pool = Executors.newFixedThreadPool(1);

    pool.submit(() -> tx.executeWithoutResult(s -> {
        seats.findByIdForUpdate(1L);
        locked.countDown();
        awaitQuietly(release);                 // lock'ni ushlab turish
    }));
    assertThat(locked.await(5, TimeUnit.SECONDS)).isTrue();

    assertThatThrownBy(() -> tx.executeWithoutResult(
            s -> seats.findByIdForUpdate(1L)))
        .isInstanceOf(PessimisticLockingFailureException.class);

    release.countDown();
    pool.shutdown();
}
```

## 11.9 Asinxron kodni testlash

`@Async` metod, `@EventListener` va `@TransactionalEventListener(phase = AFTER_COMMIT)` natijasini `Thread.sleep` bilan kutish - eng tez beqarorlashadigan naqsh. O'rniga Awaitility: `await().atMost(...).pollInterval(...).untilAsserted(...)` shart bajarilishi bilanoq davom etadi, bajarilmasa aniq xabar bilan yiqiladi. `AFTER_COMMIT` listener'i uchun yana bir shart bor: test metodi `@Transactional` bo'lmasligi kerak, aks holda commit umuman bo'lmaydi va listener hech qachon chaqirilmaydi. Determinizm kerak bo'lsa, `CountDownLatch` bilan aniq signal kutish eng ishonchli variant.

```java
@SpringBootTest
@RecordApplicationEvents
class OrderEventFlowTest {

    @Autowired OrderService orders;
    @Autowired ApplicationEvents events;
    @Autowired MailProbe mailProbe;   // @TransactionalEventListener(AFTER_COMMIT)

    @Test
    void eventIsPublishedAndHandledAfterCommit() {
        orders.place(new PlaceOrder("SKU-7", 2));

        assertThat(events.stream(OrderPlaced.class)).hasSize(1);

        await().atMost(Duration.ofSeconds(5))
               .pollInterval(Duration.ofMillis(50))
               .untilAsserted(() ->
                   assertThat(mailProbe.sent()).containsExactly("SKU-7"));
    }

    @Test
    void latchVariantForAsyncHandler() throws Exception {
        var latch = mailProbe.resetLatch(1);
        orders.place(new PlaceOrder("SKU-8", 1));
        assertThat(latch.await(5, TimeUnit.SECONDS)).isTrue();
    }
}
```

## 11.10 Spring event'larni testlash

`@RecordApplicationEvents` test klassiga qo'yilsa, `ApplicationEvents` bean'ini inject qilib publish qilingan event'larni to'g'ridan-to'g'ri tasdiqlash mumkin - har bir test metodi uchun yozuv alohida. Bu modul chegarasini tekshirishning eng arzon usuli: service listener'ni emas, faqat event'ni publish qilganini tasdiqlaydi. Spring Modulith'da esa `Scenario` API modullar orasidagi oqimni to'liq kuzatadi - stimulni beradi, event kelishini kutadi va keyin yon modul holatini tekshiradi.

```java
@ApplicationModuleTest
class OrderModuleTest {

    @Test
    void completingOrderReleasesInventory(Scenario scenario) {
        scenario.stimulate(() -> orders.complete(42L))
                .andWaitForEventOfType(OrderCompleted.class)
                .matchingMappedValue(OrderCompleted::orderId, 42L)
                .toArriveAndVerify(evt ->
                    assertThat(inventory.reserved(42L)).isZero());
    }
}
```

## 11.11 Scheduled task va job'larni testlash

Scheduler'da "qachon" va "nima" ni ajratish kerak. "Nima" - oddiy service metodi, u odatdagicha testlanadi; `@Scheduled` metod esa to'g'ridan-to'g'ri chaqirilib tekshiriladi. "Qachon" - cron ifodasi, uni `CronExpression.parse(...).next(...)` bilan alohida testlash kerak, chunki `MON-FRI` yoki yil oxiri xatosi faqat shunda ko'rinadi. Testda scheduler umuman ishga tushmasligi uchun cron'ni property'dan oling va test profilida `Scheduled.CRON_DISABLED` (`"-"`) qiymatini bering yoki `@EnableScheduling`'ni `@Profile("!test")` konfiguratsiyaga chiqaring. ShedLock'li cluster xatti-harakati uchun real DB lock jadvali bilan `LockProvider`'ni ikki marta chaqirib, ikkinchi urinish `Optional.empty()` qaytarishini tasdiqlang.

```java
@SpringBootTest
@SpringBatchTest
class NightlyReportJobTest {

    @Autowired JobLauncherTestUtils jobLauncherTestUtils;
    @Autowired JobRepositoryTestUtils jobRepositoryTestUtils;

    @AfterEach void clean() { jobRepositoryTestUtils.removeJobExecutions(); }

    @Test
    void jobCompletesAndWritesEveryRow() throws Exception {
        var params = new JobParametersBuilder()
                .addLocalDate("runDate", LocalDate.of(2026, 1, 31))
                .toJobParameters();

        JobExecution exec = jobLauncherTestUtils.launchJob(params);

        assertThat(exec.getExitStatus()).isEqualTo(ExitStatus.COMPLETED);
        assertThat(exec.getStepExecutions())
            .anySatisfy(s -> assertThat(s.getWriteCount()).isEqualTo(100L));
    }

    @Test
    void cronFiresOnWorkdayMornings() {
        var cron = CronExpression.parse("0 0 6 * * MON-FRI");
        assertThat(cron.next(LocalDateTime.of(2026, 1, 30, 7, 0)))   // juma
            .isEqualTo(LocalDateTime.of(2026, 2, 2, 6, 0));          // dushanba
    }
}
```

`JobLauncherTestUtils.launchStep("stepName")` bitta step'ni izolyatsiyada ishga tushiradi - katta job'ning bir bosqichidagi reader/processor/writer mantiqini tez tekshirish uchun qulay.

## 11.12 Konkurentlik va poyga holatini testlash

Race condition testi ikkita narsani talab qiladi: yetarlicha parallellik va bir vaqtda urish. `ExecutorService` birinchisini, `CyclicBarrier` ikkinchisini beradi - barcha thread'lar barrier'da to'planib, keyin bir paytda kirishadi. Tekshiriladigan xossa odatda idempotentlik: bir xil idempotency key bilan N marta urilganda bazada aynan bitta yozuv qolishi kerak. Unique constraint bu yerda oxirgi himoya chizig'i, shuning uchun test uning haqiqatan ishlayotganini (va `DataIntegrityViolationException` to'g'ri ushlanayotganini) ham tasdiqlashi lozim.

```java
@SpringBootTest
class PaymentIdempotencyTest {

    @Autowired PaymentService payments;
    @Autowired PaymentRepository repo;

    @RepeatedTest(5)
    void sameIdempotencyKeyCreatesExactlyOneCharge() throws Exception {
        int threads = 16;
        var key = "key-" + UUID.randomUUID();
        var barrier = new CyclicBarrier(threads);
        var pool = Executors.newFixedThreadPool(threads);
        var cmd = new Charge(key, BigDecimal.TEN);

        var futures = IntStream.range(0, threads).mapToObj(i -> pool.submit(() -> {
            barrier.await(10, TimeUnit.SECONDS);
            try { payments.charge(cmd); } catch (DuplicateChargeException ok) { }
            return null;
        })).toList();

        for (var f : futures) f.get(15, TimeUnit.SECONDS);
        pool.shutdown();

        assertThat(repo.countByIdempotencyKey(key)).isOne();
    }
}
```

Bunday testlar tabiatan beqarorlikka moyil. Beqarorlikni kamaytirish uchun: har bir takrorlashda yangi kalit/ID ishlating, hech qachon `Thread.sleep` bilan sinxronlashtirmang, timeout'larni sahiy (lekin cheksiz emas) qo'ying, thread sonini CI mashinasining yadrolaridan kelib chiqib belgilang va bu testlarni `@Tag("concurrency")` bilan ajratib alohida CI job'da yurgizing. Beqaror testni "retry until green" bilan ko'mish - xatoni ko'mish; bu mavzu [16-bobda](16-flaky-testlar-test-qarzi-va-test-kodini.md) batafsil.

## 11.13 Retry, timeout va circuit breaker'ni testlash

`@Retryable` da eng muhim tekshiruv - urinishlar **soni**: mock gateway'ga `verify(gateway, times(3))` qo'ying, aks holda `maxAttempts` qiymatini o'zgartirgan refactoring sezilmay o'tadi. Test tezligi uchun backoff'ni property orqali kichraytiring. Resilience4j'da circuit breaker holatini kutib o'tirmasdan `transitionToOpenState()` bilan majburan oching va `@BeforeEach` da `reset()` qiling - aks holda testlar bir-biriga ta'sir qiladi. Kechikish va 5xx simulyatsiyasi uchun WireMock ([9-bob](09-tashqi-servislarni-taqlid-qilish-va.md)) ishlatiladi: `withFixedDelay` timeout'ni, `withFault` esa connection reset holatini tekshiradi.

```java
@SpringBootTest
class ResilienceTest {

    @Autowired RatesClient client;    // @Retryable(retryFor = ..., maxAttempts = 3)
    @MockitoBean RatesGateway gateway;
    @Autowired CircuitBreakerRegistry registry;

    @BeforeEach void resetCircuit() { registry.circuitBreaker("rates").reset(); }

    @Test
    void retryStopsAfterThreeAttempts() {
        when(gateway.fetch()).thenThrow(new RemoteException("503"));

        assertThatThrownBy(client::rates).isInstanceOf(RemoteException.class);
        verify(gateway, times(3)).fetch();
    }

    @Test
    void openCircuitFailsFastWithoutRemoteCall() {
        registry.circuitBreaker("rates").transitionToOpenState();

        assertThatThrownBy(client::rates)
            .isInstanceOf(CallNotPermittedException.class);
        verifyNoInteractions(gateway);
    }
}
```

Fallback'ni ham testlang: circuit ochiqligida ilova cache'dagi qiymatni qaytarishi kerakmi yoki `503` berishi kerakmi - bu mahsulot qarori va u test bilan muhrlanishi shart.

## 11.14 Anti-patternlar

- Xavfsizlikni faqat qo'lda, brauzerda "ishladi" deb tekshirish; rad etilish (`403`) holatlari uchun bitta ham avtomatik test yo'q.
- Hamma joyda `@WithMockUser` ishlatib, haqiqiy token oqimini (imzo, `iss`, `aud`, `exp`, claim-to-authority konverteri) hech qachon bosib o'tmaslik.
- Test metodiga `@Transactional` qo'yib, keyin commit, `AFTER_COMMIT` listener va propagation xatti-harakatini "tekshirgan" deb hisoblash.
- Asinxron natijani `Thread.sleep(2000)` bilan kutish; CI sekinlashganda test yiqiladi, tezlashganda esa yolg'on yashil bo'ladi.
- `@MockBean`/`@MockitoBean` bilan security filter chain'ni butunlay chetlab o'tib, faqat controller mantiqini test qilib "endpoint himoyalangan" degan xulosa chiqarish.
- Checked exception'da rollback bo'lishini taxmin qilish va `rollbackFor` yo'qligini test bilan tasdiqlamaslik.
- Race condition testini yozib, beqarorligi uchun `@Disabled` qo'yish yoki CI'da retry bilan yashirish.

## 11.15 Arxitektor nazorat ro'yxati

- [ ] Har bir himoyalangan endpoint uchun rol x metod x status matritsasi mavjud va parametrlashtirilgan test bilan to'liq qoplangan (401 va 403 ajratilgan).
- [ ] Kamida bitta test real JWT oqimini (imzo va issuer validatsiyasi bilan) bosib o'tadi, qolganlari `jwt()`/`opaqueToken()` post-processor'laridan foydalanadi.
- [ ] CSRF, CORS va security header qoidalari hamda sessiya strategiyasi (stateless yoki fixation/concurrent session) test bilan muhrlangan.
- [ ] Tranzaksiya testlari haqiqiy bazada ishlaydi, test metodida `@Transactional` yo'q; `REQUIRES_NEW`, rollback va checked exception xatti-harakati tasdiqlangan.
- [ ] Self-invocation va lock konflikti (optimistik, kerak bo'lsa pessimistik) uchun aniq testlar bor.
- [ ] Asinxron natijalar faqat Awaitility yoki `CountDownLatch` bilan kutiladi; kodbazada `Thread.sleep` ishlatilgan test yo'q.
- [ ] Idempotentlik va race condition testlari `@Tag` bilan ajratilgan, alohida CI job'da yurgiziladi va beqaror holda qoldirilmagan.
- [ ] Retry urinishlari soni, circuit breaker holati va fallback xatti-harakati test bilan tasdiqlangan; penetration test, SAST va DAST alohida reja sifatida yozilgan ([13-bob](13-nofunksional-testlar-performance-resilience.md)).

---

[&larr; 10. Test ma'lumotlarini boshqarish](10-test-malumotlarini-boshqarish.md) · [Mundarija](README.md) · [12. End-to-end va UI testlar &rarr;](12-end-to-end-va-ui-testlar.md)
