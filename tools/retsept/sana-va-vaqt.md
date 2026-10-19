# sana va vaqt

Minimal shakl (clean-code 22.3, 22.5, 26.3):

```java
@Configuration
class TimeConfig {
    @Bean Clock clock() { return Clock.systemUTC(); }
}

@ConfigurationProperties("shop.order")
record OrderProperties(Duration ttl) { }

@Service
class OrderExpiryService {
    private final Clock clock;
    private final OrderProperties props;
    OrderExpiryService(Clock clock, OrderProperties props) { this.clock = clock; this.props = props; }

    boolean isExpired(Order order) {
        return order.createdAt().plus(props.ttl()).isBefore(clock.instant());
    }
}
```

Allaqachon bor, yozmang:
- `Instant.now()` o'rniga `Clock` bean, testda `Clock.fixed(...)` (clean-code 22.3)
- `30 * 24 * 60 * 60 * 1000L`, takror `static final` TTL o'rniga bitta `@ConfigurationProperties` record da `Duration` ("30d", deploysiz), `@ConfigurationPropertiesScan` bilan (clean-code 22.5, patterns 25.8)
- statik `SimpleDateFormat` o'rniga `static final DateTimeFormatter.ofPattern(..., Locale.ROOT)`, API da `ISO_INSTANT` (clean-code 22.1, 22.7)

Tuzoqlar:
- `LocalDate.now()` yoki `ZoneId.systemDefault()` server mintaqasiga bog'lanadi; `LocalDate.now(clock)`, mintaqa oshkor (clean-code 22.4)
- hodisa vaqtini `LocalDateTime` yoki `timestamp without time zone` da saqlash qiymatni siljitadi; `Instant` va `timestamptz` (clean-code 22.2, 22.9)
- kunlik oraliqni `23:59:59` bilan yopish soniyalarni yo'qotadi; yarim ochiq `[from, to)`, SQL da `>=` va `<` (clean-code 22.6)
- entity maydonida `createdAt = Instant.now()` initsializatori testda qotirilmaydi; konstruktorga `clock.instant()` yoki `@CreatedDate` + `@EntityListeners(AuditingEntityListener.class)` + `@EnableJpaAuditing(dateTimeProviderRef = ...)` (`Clock` dan `DateTimeProvider`) (clean-code 22.3, code-review 14.5, patterns 10.2, 23.30)
