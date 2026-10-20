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
- `Instant.now()` o'rniga `Clock` bean (clean-code 22.3)
- `30 * 24 * 60 * 60 * 1000L`, takror `static final` TTL o'rniga `@ConfigurationProperties` record da `Duration`, `@ConfigurationPropertiesScan` bilan (clean-code 22.5, patterns 25.8)
- statik `SimpleDateFormat` o'rniga `static final DateTimeFormatter.ofPattern("yyyy-MM-dd", Locale.ROOT)` (`YYYY` hafta yili, `DD` yil kuni), API da `ISO_INSTANT` (clean-code 22.1, 22.7)

Tuzoqlar:
- `LocalDate.now()` yoki `ZoneId.systemDefault()` server zonasiga bog'lanadi; `LocalDate.now(clock)`, zona oshkor (clean-code 22.4)
- hodisa vaqti `LocalDateTime` yoki `timestamp without time zone` da siljiydi: `Instant`, `timestamptz` (clean-code 22.2, 22.9)
- kun oxirini `23:59:59` bilan yopish soniya yo'qotadi: yarim ochiq `[from, to)`, SQL da `>=` va `<` (clean-code 22.6)
- entity vaqti: `@CreatedDate` + `@EnableJpaAuditing(dateTimeProviderRef = ...)`, `DateTimeProvider` `Clock` dan (patterns 10.2, 23.30)
- kun soni `Duration.between(..).toDays()` emas `ChronoUnit.DAYS.between(fromDate, toDate)` (code-review 14.5)
- `@Primary Clock.fixed` butun test kontekstiga emas, domen bean ga: `@Scheduled`, kesh TTL, lock muzlaydi (patterns 23.30)
