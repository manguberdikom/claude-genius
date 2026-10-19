# test

Minimal shakl (testing 5.3, testing 5.10):

```java
class SubscriptionServiceTest {
    private final Instant now = Instant.parse("2026-01-01T00:00:00Z");
    private final SubscriptionService service =
            new SubscriptionService(Clock.fixed(now, ZoneOffset.UTC));

    @Test
    void expiresRightAfterEndInstant() {
        boolean expired = service.isExpired(new Subscription(now.minusMillis(1)));

        assertThat(expired).isTrue();
    }
}
```

Allaqachon bor, yozmang:
- `Thread.sleep` kutuvi o'rniga Awaitility `await().atMost(...).untilAsserted(...)` (sonarqube 19.4)
- `Instant.now()` va `UUID.randomUUID()` o'rniga inject qilingan `Clock.fixed(...)` va `Supplier<UUID>` (testing 5.10)
- H2 yoki qo'lda URL sozlash o'rniga `@ServiceConnection` bilan `PostgreSQLContainer` bean (code-review 36.2)
- To'liq `@SpringBootTest` o'rniga `@WebMvcTest` + `MockMvcTester` + `@MockitoBean` yoki `@DataJpaTest` slice (code-review 36.3)

Tuzoqlar:
- Assertion yo'q yoki faqat `isNotNull()`: natijani aniq qiymat bilan tekshiring, faqat xato yo'qligi kerak bo'lsa `assertThatCode(...).doesNotThrowAnyException()` (sonarqube 19.2, code-review 35.1)
- Mock zanjiri va faqat `verify` dan iborat test: in-memory fake bilan holatni tekshiring, `verify` faqat ko'rinmaydigan yon ta'sir uchun (testing 5.8)
- `@DataJpaTest` har testni rollback qiladi: poyga va qulf testlarini u bilan yozmang (code-review 36.3)
