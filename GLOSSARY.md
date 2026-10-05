# Atamalar lug'ati

Oltita hujjat bo'ylab ishlatiladigan atamalar. Maqsad: inglizcha manbadan
kelgan o'quvchi o'zbekcha bo'limni topa olsin, va aksincha.

Sohaviy ma'lumotnomalar:

- [SonarQube glossariysi](docs/sonarqube/43-tezkor-malumotnoma-parametrlar-buyruqlar.md#4314-glossariy)
- [Pattern nomlari alifbo indeksi](docs/patterns/99-alifbo-boyicha-indeks.md)
- [Toza kod qoidalari jadvallari](docs/clean-code/48-tezkor-malumotnoma-qoidalar-va-tekshiruv.md)
- [Review izohlari uchun tayyor iboralar](docs/code-review/44-shablonlar-checklistlar-va-reviewer.md#443-review-izohlari-uchun-tayyor-iboralar)

## Inglizcha qoladigan atamalar

Bu so'zlar yangi matnda inglizcha yoziladi, chunki jamoada va kod ichida
shunday ishlatiladi, tarjimasi esa noaniqlik tug'diradi:

`bean`, `proxy`, `thread`, `cache`, `latency`, `throughput`, `heap`, `stack`,
`lock`, `deadlock`, `commit`, `rollback`, `branch`, `build`, `deploy`,
`pipeline`, `container`, `pod`, `scanner`, `quality gate`, `coverage`,
`issue`, `bug`, `code smell`, `vulnerability`, `security hotspot`, `rule`,
`severity`, `mock`, `stub`, `fake`, `spy`, `fixture`, `flaky`, `slice`,
`endpoint`, `payload`, `timeout`, `retry`, `backoff`, `jitter`,
`circuit breaker`, `idempotent`, `partition`, `offset`, `lag`, `rebalance`,
`vacuum`, `bloat`, `planner`, `index`, `trace`, `span`, `metric`, `log`,
`probe`, `sidecar`, `anti-pattern`, `record`, `sealed`, `virtual thread`.

Ulardan ba'zilarining o'zbekcha shakli mavjud sarlavha va matnda ham uchraydi
(`kesh`, `indeks`, `metrika`, `qamrov`, `qayta urinish`). Pastdagi jadval bu
shakllarni faqat qidirish uchun beradi. Mavjud sarlavhalar o'zgartirilmaydi.

Qo'shimcha qoida: annotatsiya, sinf, metod, parametr va konfiguratsiya
kalitlari hech qachon tarjima qilinmaydi - `@Transactional`, `HikariCP`,
`spring.datasource.url` har doim asl holida.

## O'zbekcha - inglizcha

| O'zbekcha | Inglizcha |
|---|---|
| abstraksiya | abstraction |
| alohida ajratish | isolation |
| arxitektura uslubi | architectural style |
| baho (A-E) | rating |
| bo'lim | section |
| bob | chapter |
| bog'liqlik | coupling, dependency |
| bostirish | suppression |
| buyruq | command |
| chegara | boundary, limit |
| cheklov | constraint |
| chiqarib tashlash | exclusion |
| darvoza | gate |
| dublyor (test) | test double |
| fabrika | factory |
| hodisa | event |
| holat | state |
| hayot tsikli | lifecycle |
| in'ektsiya | injection |
| indeks | index |
| izchillik | consistency |
| izolyatsiya darajasi | isolation level |
| jadval | table |
| jiddiylik | severity |
| jurnal | log |
| kechiktirilgan yuklash | lazy loading |
| kesh, keshlash | cache, caching |
| koheziya | cohesion |
| kompozitsiya | composition |
| kognitiv yuk | cognitive load |
| kuzatuvchi | observer |
| kuzatuvchanlik | observability |
| meros | inheritance |
| metrika | metric |
| migratsiya | migration |
| murakkablik | complexity |
| navbat | queue |
| nosozlik | failure |
| obyekt | object |
| oqim | stream, flow |
| o'zgarmas | immutable |
| o'zgaruvchan | mutable |
| qamrov | coverage, scope |
| qaror yozuvi | ADR, decision record |
| qator | row (jadval), line (kod) |
| qayta urinish | retry |
| qoida | rule |
| quruvchi | builder |
| replikatsiya | replication |
| reyestr | registry |
| rejalashtiruvchi | planner, scheduler |
| sahifalash | pagination |
| shablon | template |
| shishish | bloat |
| sig'im | capacity |
| sinf | class |
| so'rov | query (DB), request (HTTP) |
| strukturaviy | structural |
| sxema | schema |
| takrorlanish | duplication |
| taqsimlangan | distributed |
| tekshiruv | check, validation |
| texnik qarz | technical debt |
| tranzaksiya | transaction |
| tur | type |
| ulanish | connection |
| ulanishlar hovuzi | connection pool |
| uzilish | outage, breaking change |
| vositachi | mediator |
| xato | error, bug, issue |
| xotira | memory |
| xulq-atvor | behavioral |
| yagona nusxa | singleton |
| yakuniy izchillik | eventual consistency |
| yaratuvchi | creational |
| yuk | load |
| hid (kod) | code smell |
| refaktoring harakati | refactoring move |
| diff | diff |
| nit | nit, minor comment |
| to'xtatuvchi izoh | blocking comment |
| xavf yuzasi | risk surface |
| invariant | invariant |
| majburiyat tili | language of commitment |
| zaiflik | vulnerability |
| zanjir | chain |

## Inglizcha - o'zbekcha (eng ko'p qidiriladiganlar)

| Inglizcha | O'zbekcha bo'lim nomi |
|---|---|
| behavioral patterns | [Xulq-atvor patternlari](docs/patterns/03-xulq-atvor-patternlari.md) |
| caching | [Keshlash patternlari](docs/patterns/11-keshlash-patternlari.md) |
| cognitive complexity | [Cognitive complexity va takrorlanish](docs/sonarqube/15-cognitive-complexity-va-takrorlanishni.md) |
| coverage | [Coverage qanday o'lchanadi](docs/sonarqube/09-coverage-qanday-olchanadi-jacoco-mexanikasi.md) |
| creational patterns | [Yaratuvchi patternlar](docs/patterns/01-yaratuvchi-patternlar.md) |
| garbage collection | [Garbage collection va xotira sozlash](docs/architect/10-garbage-collection-va-xotira-sozlash.md) |
| indexes | [Indekslar: B-tree, GIN, GiST, BRIN](docs/architect/23-indekslar-b-tree-gin-gist-brin-va-tanlov.md) |
| isolation levels | [MVCC, izolyatsiya darajalari, lock](docs/architect/22-mvcc-izolyatsiya-darajalari-lock-va-deadlock.md) |
| mutation testing | [Mutation testing](docs/sonarqube/20-mutation-testing-100-coverage-qachon-yolgon.md) |
| observability | [Kuzatuvchanlik amaliyoti](docs/architect/30-kuzatuvchanlik-amaliyoti-log-metrika-trace.md) |
| quality gate | [Quality gate mexanikasi](docs/sonarqube/06-quality-gate-mexanikasi-va-shartlari.md) |
| resilience | [Resilience va cloud dizayn patternlari](docs/patterns/17-resilience-va-cloud-dizayn-patternlari.md) |
| structural patterns | [Strukturaviy patternlar](docs/patterns/02-strukturaviy-patternlar.md) |
| code smells | [Kod hidlari katalogi I](docs/clean-code/32-kod-hidlari-katalogi-i-nom-funksiya-malumot.md), [II](docs/clean-code/33-kod-hidlari-katalogi-ii-sinf-ierarxiya.md) |
| naming | [Nomlash qoidalari](docs/clean-code/02-nomlash-qoidalari-maqsadni-ochib-beruvchi.md) |
| reading a diff | [Diffni o'qish mexanikasi](docs/code-review/04-diffni-oqish-mexanikasi.md) |
| refactoring moves | [Refaktoring harakatlari katalogi I](docs/clean-code/35-refaktoring-harakatlari-katalogi-i-funksiya.md) |
| reviewing AI code | [AI yozgan kodni review qilish](docs/code-review/43-ai-yozgan-kodni-review-qilish-va-ai-bilan.md) |
| security review | [Xavfsizlik review metodikasi](docs/code-review/28-xavfsizlik-review-metodikasi.md) |
| test pyramid | [Test piramidasi](docs/testing/02-test-piramidasi-va-test-turlari-xaritasi.md) |
| Testcontainers | [Testcontainers bilan test](docs/testing/08-testcontainers-bilan-real-infratuzilmada.md) |
| transactions | [Spring tranzaksiyalari](docs/architect/19-spring-tranzaksiyalari-va-ularning.md) |
| virtual threads | [Virtual threads, structured concurrency](docs/architect/12-virtual-threads-structured-concurrency-va.md) |
