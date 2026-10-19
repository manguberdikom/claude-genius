# test: asinxron

Minimal shakl (testing 11.9):

```java
@SpringBootTest
class WelcomeMailTest {
    @Autowired UserService users;
    @Autowired MailOutbox outbox;

    @Test
    void sendsWelcomeMail() {
        users.register(new RegisterCommand("ali@example.com"));

        await().atMost(Duration.ofSeconds(5))
               .untilAsserted(() -> assertThat(outbox.count()).isEqualTo(1));
    }
}
```

Allaqachon bor, yozmang:
- `Thread.sleep` yoki qo'lda polling sikli o'rniga Awaitility `await().atMost(...).untilAsserted(...)` (testing 16.2)
- event'ni ushlovchi qo'lda listener o'rniga test klassida `@RecordApplicationEvents` + `ApplicationEvents` (testing 11.10)
- natijani kutish o'rniga testda `SyncTaskExecutor` bean: `@Async` kod sinxron va deterministik ishlaydi (patterns 5.31)

Tuzoqlar:
- `Thread.sleep` bilan kutish sekin CI'da yiqiladi, tezida ortiqcha kutadi; shart bajarilguncha `await()`, timeout faqat yuqori chegara (testing 16.2)
- `AFTER_COMMIT` listener'ni `@Transactional` test metodida tekshirsangiz commit bo'lmaydi va listener chaqirilmaydi; test metodi tranzaksiyasiz bo'lsin (testing 11.9)
- `latch.await()` yoki `future.get()` ni timeout'siz chaqirish testni osiltiradi; sahiy, lekin chekli timeout bering (testing 11.12)
