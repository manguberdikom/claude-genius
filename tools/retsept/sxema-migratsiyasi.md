# sxema migratsiyasi

Minimal shakl (code-review 25.2, 25.4, 15.5, patterns 22.10, architect 23.4):

```java
// V42: SET lock_timeout = '3s'; ALTER TABLE orders ADD COLUMN risk_score numeric(5,2);
// V43 yolg'iz: CREATE INDEX CONCURRENTLY risk_todo ON orders (id)
//   WHERE risk_score IS NULL; -- keyin DROP INDEX CONCURRENTLY
@Component
@ConditionalOnProperty("backfill.risk-score.enabled")
class RiskScoreBackfill {
    private final JdbcTemplate jdbc;
    private final Counter filled;
    RiskScoreBackfill(JdbcTemplate jdbc, MeterRegistry meters) {
        this.jdbc = jdbc;
        this.filled = meters.counter("backfill.filled");
    }
    @Scheduled(fixedDelay = 1_000)
    @SchedulerLock(name = "riskScoreBackfill", lockAtMostFor = "PT5M")
    void fillNextBatch() {
        filled.increment(jdbc.update("""
            UPDATE orders SET risk_score = least(amount / 1000, 999) WHERE id IN (
            SELECT id FROM orders WHERE risk_score IS NULL ORDER BY id LIMIT 5000)"""));
    }
}
```

Allaqachon bor, yozmang:
- `ddl-auto: update` o'rniga Flyway tarixi va `ddl-auto: none` (architect 33.2)
- Podlararo migratsiya qulfi o'rniga Flyway advisory lock (architect 33.10)

Tuzoqlar:
- `RENAME COLUMN`, o'qilayotgan ustun `DROP` i eski podni sindiradi, `ALTER COLUMN TYPE` jadvalni qayta yozadi: expand and contract (code-review 25.1, 25.3, architect 33.4)
- `CONCURRENTLY` uzilsa `indisvalid = false` indeks qoladi: `DROP INDEX CONCURRENTLY`, qayta (architect 33.8)
- `ADD COLUMN ... NOT NULL` qiymatsiz yiqiladi: konstant `DEFAULT` yoki nullable, backfill, `CHECK ... NOT VALID`, `VALIDATE`, `SET NOT NULL` (code-review 25.1, architect 33.6, 33.7)
- Butun jadval `UPDATE` migratsiya ichida: ulkan tranzaksiya, WAL, replika lag; bo'lakli idempotent job (code-review 25.4, architect 33.9)
- Migratsiya faqat statement timeout li pooler orqali yursa (to'g'ridan ulanish yo'q), katta jadvalni ko'chirishda oy yoki sana bo'lagi timeout dan oshadi va changeSet har yurishda qayta yiqiladi. Yo'l: id kursori bo'yicha `LIMIT` li paketlar (`WHERE id > (SELECT max(id) FROM yangi) ORDER BY id LIMIT N`), bir nechta bir xil `runAlways` changeSet; almashtirish qulfi ostida faqat oxirgi o'tishdan keyingi qatorlar (architect 26.5)
- Liquibase `listUnrunChangeSets` `runAlways` changeSet ni har yurishda yurmagan deb qaytaradi: pending metrikasi va "pending bo'sh" IT si `isAlwaysRun()` ni chiqarib tashlashi kerak, aks holda ish tugagach ham har yurishda ogohlantirish chiqadi
