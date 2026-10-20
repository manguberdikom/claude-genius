---
name: postgres-tuning
description: Diagnose or tune PostgreSQL behaviour behind a Java/Spring application - slow query, EXPLAIN ANALYZE reading, planner and statistics, index choice (B-tree, GIN, GiST, BRIN, partial, covering), MVCC and isolation levels, lock contention and deadlock, vacuum and bloat, schema and data-type design, constraints, partitioning, replication, server parameters (shared_buffers, work_mem, effective_cache_size), connection pooling with HikariCP, statement and lock timeouts, and monitoring via pg_stat_* views. Use when a query is slow, a lock or deadlock appears, an index decision is needed, table size or bloat grows, connections run out, or a migration must run without downtime.
---

# PostgreSQL: diagnostika va sozlash

`docs/architect/` hujjatining IV qismi (21-27 boblar).

## Qoida

O'lchamasdan sozlamang. Tartib (`architect 24.12`):

0. **Rostdan sekinmi yoki kutyaptimi** - `pg_stat_activity.wait_event_type`:
   lock kutishi (`architect 22.10`) yoki pool (`architect 27.5`) indeks
   bilan tuzalmaydi.
1. **Qaysi so'rov** - `pg_stat_statements` dan eng qimmati (`architect 24.10`,
   yoqish `27.10`).
2. **Nega qimmat** - `EXPLAIN (ANALYZE, BUFFERS)`, taxmin qilmang
   (`architect 24.6`, `24.7`). `rows` va `actual rows` farqi katta bo'lsa,
   muammo statistikada.
3. **Indeks yoki sxema** - `architect 23`, `architect 25`.
4. Faqat shundan keyin parametr (`architect 27.2`, `27.3`, `27.8`).

0-2 ma'lumoti jonli serverdan: avval foydalanuvchidan so'rang (sekin
so'rov logi: `architect 27.11`). Lokal kichik bazadagi reja boshqacha.

`shared_buffers` ni oshirish sekin so'rovni tezlashtirmaydi. Noto'g'ri
indeks `work_mem` bilan tuzalmaydi.

`/manguberdi` shu sessiyada chaqirilgan bo'lsa kod yoki migratsiya
o'zgarishi aktyorga beriladi (`dasturchi`, sxema qarori
`rejalashtiruvchi`); bu skill o'shanda faqat bob jadvali.

## Vazifa - bob jadvali

| Vazifa | Fayl |
|---|---|
| Process model, WAL, checkpoint, vacuum mexanikasi, bloat | `docs/architect/21-postgresql-arxitekturasi-process-model-wal.md` |
| MVCC, izolyatsiya darajalari, lock turlari, deadlock, `pg_locks` | `docs/architect/22-mvcc-izolyatsiya-darajalari-lock-va-deadlock.md` |
| Indeks tanlash: B-tree, GIN, GiST, BRIN, qisman, qamrab oluvchi, `CONCURRENTLY`, keraksiz indeksni topish | `docs/architect/23-indekslar-b-tree-gin-gist-brin-va-tanlov.md` |
| Planner, `ANALYZE`, statistika, narx parametrlari, `EXPLAIN ANALYZE` o'qish, generic plan muammosi | `docs/architect/24-planner-statistika-va-explain-analyze-oqish.md` |
| Sxema dizayni, ma'lumot turlari, cheklovlar, `enum` vs lug'at jadvali | `docs/architect/25-sxema-dizayni-malumot-turlari-va-cheklovlar.md` |
| Partitioning, replikatsiya, katta hajm | `docs/architect/26-partitioning-replikatsiya-va-katta-hajm.md` |
| `shared_buffers`, `work_mem`, HikariCP pool kattaligi, `statement_timeout`, `pg_stat_*` monitoring | `docs/architect/27-sozlash-connection-pool-va-monitoring.md` |
| To'xtashsiz sxema migratsiyasi, expand/contract, Flyway | `docs/architect/33-sxema-migratsiyasi-va-toxtashsiz-reliz.md` |

## Spring tomoni

PostgreSQL muammosi ko'pincha Java tomonda tug'iladi:

| Belgi | Qarang |
|---|---|
| N+1 so'rov, lazy load exception, flush tartibi | `docs/architect/18-spring-data-jpa-va-hibernate-chuqur.md` |
| Uzun tranzaksiya, `readOnly`, propagation, `idle in transaction` | `docs/architect/19-spring-tranzaksiyalari-va-ularning.md` |
| JDBC pool tugadi (`Connection is not available, request timed out`), `connection-timeout`, thread hisobi | `docs/architect/27-sozlash-connection-pool-va-monitoring.md`, `docs/architect/08-ishlash-va-resurs-hissi-napkin-math.md` |
| Repository/Specification/ID generatsiyasi patternlari | `docs/patterns/09-malumotlarga-kirish-va-orm-patternlari.md` |
| Testda H2 emas, real PostgreSQL konteyner | `docs/testing/08-testcontainers-bilan-real-infratuzilmada.md` |
| PostgreSQL ga xos Sonar issue'lari | `docs/sonarqube/29-xato-katalogi-spring-jpa-va-postgresql-ga.md` |

## Asboblar

```bash
python3 tools/rules_for.py --vazifa="<vazifa>" <entity, repository, migratsiya .sql>  # kod yoki migratsiya yozishdan OLDIN
python3 tools/schema_from_entities.py <src>  # jadval, ustun, FK, indeks
python3 tools/schema_from_entities.py <src> --only-findings  # EAGER, indekssiz
                                                   # FK, ORDINAL enum, precision
tools/doc.sh find -f "pg_stat_statements"    # matn ichidan qidirish
tools/doc.sh outline architect <bob>         # bobdagi bo'limlar
tools/doc.sh show architect <raqam>          # butun bob emas, faqat o'sha bo'lim
```
