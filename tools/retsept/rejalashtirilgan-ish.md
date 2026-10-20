# rejalashtirilgan ish

Minimal shakl (patterns 20.22, clean-code 22.3):

```java
@Configuration
@EnableScheduling
@EnableSchedulerLock(defaultLockAtMostFor = "PT30M")
class SchedulingConfig {
    @Bean LockProvider lockProvider(DataSource ds) {
        return new JdbcTemplateLockProvider(JdbcTemplateLockProvider.Configuration.builder()
            .withJdbcTemplate(new JdbcTemplate(ds)).usingDbTime().build());
    }
}

@Component
class OrderExpiryJob {
    private final OrderRepository orders;
    private final OrderProperties props;
    private final Clock clock;
    OrderExpiryJob(OrderRepository orders, OrderProperties props, Clock clock) {
        this.orders = orders; this.props = props; this.clock = clock;
    }

    @Scheduled(cron = "0 */5 * * * *")
    @SchedulerLock(name = "orderExpiry", lockAtLeastFor = "PT1M")
    void run() { orders.expireCreatedBefore(clock.instant().minus(props.ttl())); }
}
```

Allaqachon bor, yozmang:
- `sleep` sikli o'rniga `@Scheduled(cron, zone)` (patterns 20.21)
- O'z lock jadvali o'rniga ShedLock va `JdbcTemplateLockProvider` (patterns 20.22)
- `Instant.now()` o'rniga bor `Clock` bean; ikkinchi `clock()` start xatosi (code-review 18.7)

Tuzoqlar:
- `synchronized` faqat bitta JVM da, `@Scheduled` har podda: `@SchedulerLock` qo'ying (code-review 15.5)
- `lockAtMostFor` job eng uzun vaqtidan katta; lock bir martalikni kafolatlamaydi, job idempotent bo'lsin (patterns 20.22)
- Pool 1 thread, `fixedRate` navbat yig'adi: qo'lda scheduler bean emas `spring.task.scheduling.pool.size`, `fixedDelay` (patterns 4.14, 20.21)
- Davriy bulk `UPDATE ... WHERE status = 'NEW' AND created_at < ?` uchun `(created_at) WHERE status = 'NEW'` partial index; so'rovda status literal bo'lsin, bind parameter bilan planner uni olmaydi (architect 23.4)
