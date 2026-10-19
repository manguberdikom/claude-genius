# sxema migratsiyasi

Minimal shakl (code-review 25.2, 25.4, 15.5, patterns 22.10):

```java
// V42__add_risk_score.sql
//   SET lock_timeout = '3s';
//   ALTER TABLE orders ADD COLUMN risk_score numeric(5,2);
@Component
@ConditionalOnProperty("backfill.risk-score.enabled")
class RiskScoreBackfill {
    private final JdbcTemplate jdbc;
    private boolean done;

    RiskScoreBackfill(JdbcTemplate jdbc, MeterRegistry meters) {
        this.jdbc = jdbc;
        Gauge.builder("backfill.remaining", jdbc, j -> j.queryForObject(
                "SELECT count(*) FROM orders WHERE risk_score IS NULL", Long.class))
            .register(meters);
    }

    @Scheduled(fixedDelay = 1_000)
    @SchedulerLock(name = "riskScoreBackfill", lockAtMostFor = "PT5M")
    void fillNextBatch() {
        if (done) return;
        done = jdbc.update("""
            UPDATE orders SET risk_score = 0 WHERE id IN (SELECT id FROM orders
            WHERE risk_score IS NULL ORDER BY id LIMIT 5000)""") == 0;
    }
}
```

Allaqachon bor, yozmang:
- `ddl-auto: update` o'rniga Flyway tarixi va `ddl-auto: none` (architect 33.1, 33.2)
- Podlar orasida migratsiya qulfi o'rniga Flyway advisory lock (architect 33.10)
- `CONCURRENTLY` uchun tranzaksiyani qo'lda o'chirish o'rniga Flyway parseri, fayl yolg'iz (architect 33.8)

Tuzoqlar:
- `RENAME COLUMN` yoki o'qilayotgan ustunni `DROP` eski podlarni sindiradi: expand and contract (code-review 25.3, architect 33.4)
- `ADD COLUMN ... NOT NULL` qiymatsiz yiqiladi: konstant `DEFAULT` yoki nullable va backfill, keyin `CHECK ... NOT VALID`, `VALIDATE`, `SET NOT NULL` (code-review 25.1, architect 33.6, 33.7)
- Butun jadval `UPDATE` migratsiya ichida: ulkan tranzaksiya, WAL, replika lag; bo'lakli, idempotent job (code-review 25.4, architect 33.9)
