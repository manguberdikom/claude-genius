<!-- doc: patterns | chapter: 20 | part:  -->

[Barcha hujjatlar](../../README.md) / [Dizayn patternlar](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 20. Batch va scheduling patternlari (Batch & Scheduling Patterns)

<details>
<summary>Bu bobdagi 31 bo'lim</summary>

- [20.1 Chunk'ga asoslangan ishlov (Chunk-Oriented Processing)](#201-chunkga-asoslangan-ishlov-chunk-oriented-processing)
- [20.2 Tasklet (Tasklet)](#202-tasklet-tasklet)
- [20.3 ItemReader / ItemProcessor / ItemWriter (ItemReader / ItemProcessor / ItemWriter)](#203-itemreader--itemprocessor--itemwriter-itemreader--itemprocessor--itemwriter)
- [20.4 Job / Step / Flow (Job / Step / Flow)](#204-job--step--flow-job--step--flow)
- [20.5 JobRepository va restart imkoniyati (JobRepository & Restartability)](#205-jobrepository-va-restart-imkoniyati-jobrepository--restartability)
- [20.6 Skip va retry siyosatlari (Skip / Retry Policies)](#206-skip-va-retry-siyosatlari-skip--retry-policies)
- [20.7 Partitsiyalash (Partitioning - local, remote)](#207-partitsiyalash-partitioning---local-remote)
- [20.8 Masofaviy chunking (Remote Chunking)](#208-masofaviy-chunking-remote-chunking)
- [20.9 Parallel qadamlar va ko'p-thread'li qadam (Parallel Steps / Multi-threaded Step)](#209-parallel-qadamlar-va-kop-threadli-qadam-parallel-steps--multi-threaded-step)
- [20.10 Job parametrlari va job identifikatori (Job Parameters & Job Identity)](#2010-job-parametrlari-va-job-identifikatori-job-parameters--job-identity)
- [20.11 Step scope va kechiktirilgan binding (Step Scope / Late Binding)](#2011-step-scope-va-kechiktirilgan-binding-step-scope--late-binding)
- [20.12 Listener'lar (Listeners - JobExecutionListener, StepExecutionListener)](#2012-listenerlar-listeners---jobexecutionlistener-stepexecutionlistener)
- [20.13 Kompozit ItemProcessor / ItemWriter (Composite ItemProcessor / ItemWriter)](#2013-kompozit-itemprocessor--itemwriter-composite-itemprocessor--itemwriter)
- [20.14 Classifier bilan kompozit writer (Classifier Composite Writer)](#2014-classifier-bilan-kompozit-writer-classifier-composite-writer)
- [20.15 Paging reader va cursor reader (Paging Reader vs Cursor Reader)](#2015-paging-reader-va-cursor-reader-paging-reader-vs-cursor-reader)
- [20.16 Staging jadval (Staging Table)](#2016-staging-jadval-staging-table)
- [20.17 Boshqaruvchi so'rov (Driving Query)](#2017-boshqaruvchi-sorov-driving-query)
- [20.18 Process indikatori (Process Indicator)](#2018-process-indikatori-process-indicator)
- [20.19 Extract-Transform-Load (Extract-Transform-Load - ETL)](#2019-extract-transform-load-extract-transform-load---etl)
- [20.20 Backfill (Backfill)](#2020-backfill-backfill)
- [20.21 Rejalashtirilgan vazifalar (Scheduled Tasks)](#2021-rejalashtirilgan-vazifalar-scheduled-tasks)
- [20.22 Taqsimlangan scheduler lock (Distributed Scheduler Lock, ShedLock)](#2022-taqsimlangan-scheduler-lock-distributed-scheduler-lock-shedlock)
- [20.23 Quartz klasterlash (Quartz Clustering)](#2023-quartz-klasterlash-quartz-clustering)
- [20.24 Joblar uchun leader election (Leader Election for Jobs)](#2024-joblar-uchun-leader-election-leader-election-for-jobs)
- [20.25 Spring Cloud Task](#2025-spring-cloud-task)
- [20.26 Solishtirish (reconciliation) joblari (Reconciliation Jobs)](#2026-solishtirish-reconciliation-joblari-reconciliation-jobs)
- [20.27 Arxivlash va tozalash joblari (Archive / Purge Jobs)](#2027-arxivlash-va-tozalash-joblari-archive--purge-jobs)
- [20.28 Batch oynasi va SLA (Batch Window & SLA)](#2028-batch-oynasi-va-sla-batch-window--sla)
- [20.29 Idempotent batch (Idempotent Batch)](#2029-idempotent-batch-idempotent-batch)
- [20.30 Batch'da dead-letter boshqaruvi (Dead-Letter Handling in Batch)](#2030-batchda-dead-letter-boshqaruvi-dead-letter-handling-in-batch)
- [20.31 Amalda qo'llash](#2031-amalda-qollash)

</details>



Batch va scheduling patternlari - bu katta hajmli, uzoq davom etadigan va vaqt bo'yicha ishga tushadigan ishlovlarni ishonchli bajarish uchun shakllangan yechimlar to'plami. Onlayn (request-response) dunyoda bir so'rov sekundlarda tugaydi, batch dunyosida esa bitta ish millionlab yozuvni soatlab qayta ishlaydi - shu sababli xotira sarfi, transaction chegaralari, restart (qayta ishga tushirish), idempotentlik va gorizontal masshtablash arxitektura darajasidagi qarorlarga aylanadi. Arxitektor uchun bu patternlar muhim, chunki ular "tungi hisob-kitob" yoki "ERP integratsiyasi" kabi biznes-kritik oqimlarning SLA'sini, xatolarga chidamliligini va kuzatiluvchanligini (observability) belgilaydi. Spring Batch bu patternlarni domen tilida kodlashtirgan: Job, Step, chunk, ItemReader/Writer, JobRepository - bular shunchaki API emas, balki umumiy so'zlashuv lug'ati.

## 20.1 Chunk'ga asoslangan ishlov (Chunk-Oriented Processing)

**Tavsif:** Katta hajmli ma'lumotni bittadan o'qib, bittadan qayta ishlab, lekin N dona yozuvdan iborat to'plam (chunk) sifatida yozish va har bir chunk oxirida transaction'ni commit qilish patterni. Bu yondashuv xotirani chegaralangan ushlab turadi (butun dataset RAM'ga yuklanmaydi) va commit interval orqali throughput bilan xatolik narxi o'rtasida muvozanat beradi. Agar 7-chunk'da xato bo'lsa, undan oldingi 6 chunk allaqachon commit qilingan va restart shu joydan davom etadi. Amalda bu "read-process-write + periodic commit" halqasidan iborat.

**Spring'da qayerda uchraydi:** Spring Batch 5.x (Spring Boot 3.x) va 6.x (Spring Boot 4.x) da `StepBuilder.chunk(int, PlatformTransactionManager)` orqali quriladi; ichida `SimpleStepBuilder`, `ChunkOrientedTasklet`, `SimpleChunkProvider` va `SimpleChunkProcessor` ishlaydi. Commit interval o'rniga dinamik chegara kerak bo'lsa `CompletionPolicy` (`SimpleCompletionPolicy`, `TimeoutTerminationPolicy`) ishlatiladi, progress kuzatish uchun `ChunkListener` va `StepExecutionListener` mavjud.

```java
@Bean
Step importStep(JobRepository repo, PlatformTransactionManager tx,
                ItemReader<Row> reader, ItemWriter<Row> writer) {
    return new StepBuilder("importStep", repo)
            .<Row, Row>chunk(500, tx)
            .reader(reader).writer(writer)
            .build();
}
```

**Qo'llanish keyslari:**
- Tungi hisob-kitob: 20 mln bank tranzaksiyasini o'qib, komissiya hisoblab, natijani jadvalga yozish.
- CSV/fixed-length fayldan kelgan narx ro'yxatini validatsiya qilib katalogga yuklash.
- Legacy Oracle bazasidan yangi PostgreSQL sxemasiga bosqichma-bosqich migratsiya.
- Oylik billing: har bir abonent uchun invoice generatsiya qilish va PDF navbatiga qo'yish.
- Data warehouse uchun kunlik ETL: staging jadvallaridan fakt jadvallariga yuklash.

**Ehtiyot bo'ling:** Chunk size'ni juda katta qilish (masalan 100 000) transaction'ni uzaytiradi, lock contention va undo/redo o'sishiga olib keladi; juda kichik qilish esa commit overhead'ini oshiradi - 100-1000 oralig'idan boshlab o'lchab tanlang. Bir chunk ichida tashqi REST chaqiruvlari qilish transaction'ni tashqi tizim latency'siga bog'lab qo'yadi, buni alohida qadamga yoki asinxron ishlovga chiqarish kerak.

## 20.2 Tasklet (Tasklet)

**Tavsif:** Qadamning (step) butun mantig'i bitta metodda bajariladigan, read-process-write tuzilishiga tushmaydigan oddiy pattern. `execute()` metodi `RepeatStatus.FINISHED` qaytarsa qadam tugaydi, `CONTINUABLE` qaytarsa yangi transaction bilan qayta chaqiriladi. Bu "atomik vazifa" uchun mo'ljallangan: fayl ko'chirish, jadvalni tozalash, stored procedure chaqirish, flag qo'yish.

**Spring'da qayerda uchraydi:** `org.springframework.batch.core.step.tasklet.Tasklet` interfeysi va `StepBuilder.tasklet(Tasklet, PlatformTransactionManager)`; tayyor implementatsiyalar - `MethodInvokingTaskletAdapter` (mavjud bean metodini qadamga aylantirish), `SystemCommandTasklet` (OS buyrug'ini chaqirish) va `spring-batch-integration` dagi `JobStepBuilder` orqali boshqa Job'ni chaqirish. Tasklet ichida `ChunkContext` va `StepContribution` orqali `ExecutionContext` bilan ishlanadi.

**Qo'llanish keyslari:**
- Asosiy ishlovdan oldin staging jadvalini `TRUNCATE` qilish yoki indekslarni o'chirish.
- Ishlov tugagach SFTP'ga chiqish faylini yuklash yoki arxiv papkaga ko'chirish.
- Kunlik agregatsiyani bajaruvchi DB stored procedure'ni chaqirish.
- Tashqi tizimga "batch yakunlandi" signalini (webhook yoki JMS xabari) yuborish.
- Fayl mavjudligini va kutilgan hajmini tekshiruvchi pre-validation qadami.

**Ehtiyot bo'ling:** Tasklet ichiga millionlab yozuvni o'qiydigan halqa yozish eng keng tarqalgan xato - bunda restartability, skip/retry va metrikalar yo'qoladi, xotira esa portlaydi. Agar vazifada "har bir element uchun" mantiq bo'lsa, bu chunk-oriented qadam bo'lishi kerak, Tasklet emas.

## 20.3 ItemReader / ItemProcessor / ItemWriter (ItemReader / ItemProcessor / ItemWriter)

**Tavsif:** Ishlov mantig'ini uch mas'uliyatga ajratuvchi pattern: manbadan bittadan o'qish (reader), transformatsiya yoki filtrlash (processor), to'plamni yozish (writer). Processor `null` qaytarsa element filtrlanadi va writer'ga yetib bormaydi. Bu ajratish har bir bo'lakni alohida unit-test qilish, qayta ishlatish va manba/maqsadni almashtirish imkonini beradi - masalan CSV reader'ni JDBC reader'ga o'zgartirish qolgan kodga ta'sir qilmaydi.

**Spring'da qayerda uchraydi:** `ItemReader`, `ItemProcessor`, `ItemWriter` interfeyslari va holatni saqlash uchun `ItemStream` (`ItemStreamReader`/`ItemStreamWriter`). Tayyor implementatsiyalar: `FlatFileItemReader` + `DefaultLineMapper`/`DelimitedLineTokenizer`, `JsonItemReader`, `StaxEventItemReader`, `JdbcCursorItemReader`, `JdbcPagingItemReader`, `JpaPagingItemReader`, `MongoPagingItemReader`, `KafkaItemReader`; yozuvchilar - `FlatFileItemWriter`, `JdbcBatchItemWriter`, `JpaItemWriter`, `CompositeItemWriter`, `ClassifierCompositeItemWriter`. Processor tarafida `ValidatingItemProcessor` (Bean Validation bilan `BeanValidatingItemProcessor`), `CompositeItemProcessor`, `ClassifierCompositeItemProcessor`, `FunctionItemProcessor` va builder'lar (`FlatFileItemReaderBuilder` va h.k.).

**Qo'llanish keyslari:**
- To'lov provayderidan kelgan kunlik settlement faylini o'qib, ichki formatga map qilib bazaga yozish.
- Bazadagi mijoz yozuvlarini anonimlashtirib (PII masking) test muhiti uchun dump chiqarish.
- Kafka topic'dan hodisalarni o'qib, agregatsiya qilib analytics jadvaliga yozish.
- Bir nechta turdagi yozuvni turli jadvallarga yo'naltirish (`ClassifierCompositeItemWriter`).
- Validatsiyadan o'tmagan qatorlarni filtrlab, qolganini yuklash va rad etilganlarni alohida faylga chiqarish.

**Ehtiyot bo'ling:** `JdbcCursorItemReader` bitta ochiq cursor va bitta connection ushlaydi - ko'p thread yoki uzoq ishlov uchun `JdbcPagingItemReader` ma'qul, lekin paging'da `ORDER BY` barqaror va unique bo'lishi shart, aks holda yozuvlar takrorlanadi yoki tushib qoladi. JPA reader'larda `EntityManager` cache'i o'sib ketadi, shuning uchun chunk oxirida flush/clear va `saveState` sozlamalariga e'tibor bering.

## 20.4 Job / Step / Flow (Job / Step / Flow)

**Tavsif:** Batch ishini ierarxik modellashtirish patterni: Job - bitta biznes-ishning yuqori darajadagi birligi, Step - uning mustaqil, o'z transaction va metadata chegarasiga ega bosqichi, Flow - qadamlar o'rtasidagi o'tish grafigi (ketma-ketlik, shart, shoxlanish, parallel split). Qadamlar orasidagi o'tish exit status asosida aniqlanadi, shu sababli "xato bo'lsa tozalash qadamiga o't" yoki "fayl bo'sh bo'lsa o'tkazib yubor" kabi mantiqni deklarativ yozish mumkin.

**Spring'da qayerda uchraydi:** `JobBuilder` va `StepBuilder` (Spring Batch 5+ da `JobBuilderFactory`/`StepBuilderFactory` olib tashlangan - `JobRepository` to'g'ridan-to'g'ri konstruktorga beriladi), `FlowBuilder` va `SimpleFlow`, `JobExecutionDecider` shartli o'tishlar uchun, `FlowBuilder.SplitBuilder` parallel shoxlar uchun, `JobStep` ichma-ich job'lar uchun. Ishga tushirish `JobLauncher`/`JobOperator` yoki Spring Boot'ning `JobLauncherApplicationRunner` orqali (`spring.batch.job.name` property bilan), konfiguratsiya esa `@EnableBatchProcessing` yoki `DefaultBatchConfiguration` subclass'i bilan qilinadi.

**Qo'llanish keyslari:**
- Kechki oqim: "faylni yuklab ol → validatsiya → yuklash → hisobot → arxivlash" ketma-ketligi.
- Xatolik yuz berganda `on("FAILED").to(cleanupStep)` orqali kompensatsiya qadamiga o'tish.
- Bir-biriga bog'liq bo'lmagan uchta hisobotni `split()` bilan parallel generatsiya qilish.
- `JobExecutionDecider` yordamida oy oxirida qo'shimcha yopish qadamini bajarish.
- Umumiy "reusable" qadamlarni bir nechta job'da qayta ishlatish (masalan arxivlash qadami).

**Ehtiyot bo'ling:** Juda ko'p shartli o'tish va decider ishlatilgan flow'lar tezda o'qilmas "spagetti"ga aylanadi - murakkablik oshsa orkestratsiyani Job'dan tashqariga (Airflow, Argo Workflows, Spring Cloud Data Flow) chiqarish ma'qul. Shuningdek Step'lar orasida ma'lumotni `ExecutionContext` orqali uzatish vasvasasiga berilmang: u metadata uchun, katta payload uchun emas.

## 20.5 JobRepository va restart imkoniyati (JobRepository & Restartability)

**Tavsif:** Har bir job va step bajarilishining holatini turg'un omborga (odatda RDBMS) yozib borish patterni: qaysi chunk commit bo'lgan, reader qaysi qatorda to'xtagan, nechta yozuv o'qilgan/yozilgan/skip qilingan. Shu metadata hisobiga muvaffaqiyatsiz tugagan job qayta ishga tushirilganda noldan emas, oxirgi muvaffaqiyatli checkpoint'dan davom etadi. Checkpoint ma'lumoti `ExecutionContext` sifatida chunk commit'i bilan bitta transaction'da saqlanadi - shuning uchun holat va ma'lumot bir-biriga mos qoladi.

**Spring'da qayerda uchraydi:** `JobRepository` interfeysi va `JdbcJobRepositoryFactoryBean`/`JobRepositoryFactoryBean` orqali quriladigan `SimpleJobRepository`; metadata jadvallari `BATCH_JOB_INSTANCE`, `BATCH_JOB_EXECUTION`, `BATCH_JOB_EXECUTION_PARAMS`, `BATCH_STEP_EXECUTION`, `BATCH_*_EXECUTION_CONTEXT` (DDL `org/springframework/batch/core/schema-*.sql` da, Spring Boot `spring.batch.jdbc.initialize-schema` bilan yaratadi). O'qish uchun `JobExplorer`, boshqarish uchun `JobOperator` (restart/stop/abandon), qadam darajasida `allowStartIfComplete(true)` va `startLimit(n)`; reader'lar `ItemStream.update()` orqali o'z pozitsiyasini shu kontekstga yozadi.

**Qo'llanish keyslari:**
- 8 soat ishlagan job 7-soatda uzilganda, restart bilan faqat qolgan qismni qayta ishlash.
- Operatsion jamoaga "qaysi job qachon ishladi, nechta yozuv skip bo'ldi" degan audit ko'rinishini berish.
- Pod qayta ishga tushganda (Kubernetes) to'xtab qolgan execution'ni `JobOperator.restart()` bilan tiklash.
- `BATCH_STEP_EXECUTION` metrikalarini Grafana'ga chiqarib SLA monitoringi qurish.
- Idempotent bo'lmagan qadamni `allowStartIfComplete(false)` bilan ikki marta bajarilishidan saqlash.

**Ehtiyot bo'ling:** In-memory yoki `ResourcelessJobRepository` tipidagi repository'da restart va audit umuman yo'q - productionda har doim turg'un JDBC repository ishlatilsin, sxema versiyasi esa Spring Batch versiyasiga mos migratsiya qilinsin. Restart faqat reader'ingiz holatini to'g'ri saqlasa ishlaydi: tartibsiz query, `saveState(false)` yoki tashqi navbatdan o'qish holatni buzadi va "qayta ishlov" dublikatlarga olib keladi.

## 20.6 Skip va retry siyosatlari (Skip / Retry Policies)

**Tavsif:** Xatolarni ikki xil tabiatga ajratib ishlov berish patterni: vaqtinchalik (transient) xatolar qayta urinishga arziydi, "yomon ma'lumot" (deterministik) xatolar esa o'tkazib yuborilishi (skip) va alohida qayd etilishi kerak. Spring Batch bu ikkisini chunk darajasida birlashtiradi: retry tugamagach element skip qilinadi, skip limiti oshsa qadam fail bo'ladi. Skip paytida chunk "scan" rejimiga o'tib, elementlarni bittadan qayta ishlab aybdorni topadi - bu xatti-harakatni bilish performance uchun muhim.

**Spring'da qayerda uchraydi:** `SimpleStepBuilder.faultTolerant()` dan keyin `skip(Class)`, `noSkip(Class)`, `skipLimit(int)`, `skipPolicy(SkipPolicy)` (`LimitCheckingItemSkipPolicy`, `AlwaysSkipItemSkipPolicy`, `NeverSkipItemSkipPolicy`) va `retry(Class)`, `retryLimit(int)`, `retryPolicy(...)`, `backOffPolicy(...)`, `noRollback(Class)`. Ostida `spring-retry` (`RetryTemplate`, `SimpleRetryPolicy`, `ExponentialBackOffPolicy`) yotadi; kuzatish uchun `SkipListener`, `RetryListener`, `ItemReadListener`/`ItemWriteListener`. Batch tashqarisida xuddi shu g'oya `@Retryable`/`@Recover` (Spring Retry) yoki Resilience4j bilan qo'llanadi.

**Qo'llanish keyslari:**
- Fayldagi buzuq qatorlarni (parse xatosi) skip qilib, ularni "rejected" jadvaliga yozish.
- Deadlock yoki `CannotAcquireLockException` holatida chunk'ni exponential backoff bilan qayta urinish.
- Tashqi API'ning 503/timeout javoblarida retry, 400 javobida esa darhol skip qilish.
- Kunlik yuklamada skip hisoblagichi chegaradan oshsa job'ni to'xtatib, operatorga alert yuborish.
- Validatsiya xatolaridagi yozuvlarni `SkipListener` orqali dead-letter topic'ga yuborish.

**Ehtiyot bo'ling:** Deterministik xatoni (masalan `NullPointerException` yoki unique constraint buzilishi) retry qilish faqat vaqt sarflaydi va retry limiti tugagach baribir fail bo'ladi - qaysi exception transient ekanini aniq ro'yxat bilan belgilang, `Exception.class` ni ko'r-ko'rona skip qilmang. Cheksiz yoki juda katta `skipLimit` esa "muvaffaqiyatli" tugagan, lekin yarmi yo'qolgan ishlovni yashiradi.

## 20.7 Partitsiyalash (Partitioning - local, remote)

**Tavsif:** Katta ma'lumot to'plamini mustaqil bo'laklarga (partition) ajratib, har birini alohida step execution sifatida parallel bajarish patterni. Manager qadam `Partitioner` yordamida partition'lar va ularning `ExecutionContext` parametrlarini (masalan ID oralig'i yoki fayl nomi) yaratadi, `PartitionHandler` esa ularni thread'larga yoki boshqa JVM'larga tarqatadi. Har bir worker o'z partition'ini to'liq o'qiydi va yozadi - ya'ni faqat metadata tarmoq orqali ketadi, ma'lumotning o'zi emas.

**Spring'da qayerda uchraydi:** `PartitionStep`, `Partitioner` (`SimplePartitioner`, `MultiResourcePartitioner`), `StepExecutionSplitter`, `PartitionHandler` implementatsiyalari: lokal uchun `TaskExecutorPartitionHandler` (`StepBuilder.partitioner(...).gridSize(n).taskExecutor(...)`), remote uchun `spring-batch-integration` dagi `MessageChannelPartitionHandler`, `RemotePartitioningManagerStepBuilder` va `RemotePartitioningWorkerStepBuilder` (`@EnableBatchIntegration` bilan, Kafka/RabbitMQ/JMS kanallari ustida). Worker tarafida partition parametrlari `@StepScope` bean'larga `#{stepExecutionContext['minId']}` ko'rinishida inyeksiya qilinadi.

**Qo'llanish keyslari:**
- 50 mln qatorli jadvalni ID oralig'i bo'yicha 32 partition'ga bo'lib parallel qayta ishlash.
- SFTP'dan kelgan 200 ta faylni `MultiResourcePartitioner` bilan har fayl - bitta partition qilib yuklash.
- Ko'p-ijarachi (multi-tenant) tizimda har bir tenant uchun alohida partition ishga tushirish.
- Kubernetes'da worker pod'larini remote partitioning bilan avtomatik masshtablash.
- Mintaqa yoki filial bo'yicha bo'lingan oylik hisob-kitobni parallel bajarish.

**Ehtiyot bo'ling:** Partitsiyalash faqat ma'lumot tabiiy ravishda bir-biriga bog'liq bo'lmagan bo'laklarga ajralsa ishlaydi; umumiy jadvalga yozadigan partition'lar lock contention va deadlock keltiradi, DB connection pool'i esa gridSize'dan kichik bo'lsa hamma worker navbatda qotib qoladi. Partition'lar notekis bo'lsa (bitta bo'lakda 90% ma'lumot) parallelizmdan foyda yo'q - kalit taqsimotini oldin o'lchang.

## 20.8 Masofaviy chunking (Remote Chunking)

**Tavsif:** Qadamning o'qish qismini manager node'da qoldirib, processing va yozishni masofadagi worker'larga uzatish patterni. Manager `ItemReader` bilan o'qigan chunk'larni xabar navbatiga (middleware) yuboradi, worker'lar ularni qabul qilib `ItemProcessor`/`ItemWriter` bilan qayta ishlaydi va natijani qaytaradi. Partitioning'dan farqi: bu yerda ma'lumotning o'zi tarmoq orqali uzatiladi, shuning uchun u faqat CPU-og'ir processing I/O xarajatidan ustun bo'lganda foyda beradi.

**Spring'da qayerda uchraydi:** `spring-batch-integration` moduli: manager tarafda `RemoteChunkingManagerStepBuilderFactory`/`RemoteChunkingManagerStepBuilder` va `ChunkMessageChannelItemWriter`, worker tarafda `RemoteChunkingWorkerBuilder` va `ChunkProcessorChunkHandler`, ikkisi ham `@EnableBatchIntegration` bilan yoqiladi. Transport sifatida Spring Integration kanallari ishlatiladi - `spring-boot-starter-amqp` (RabbitMQ), Kafka yoki JMS; chunk'lar serializatsiya qilinadi, shuning uchun item'lar `Serializable` yoki JSON converter bilan mos bo'lishi kerak.

**Qo'llanish keyslari:**
- Har bir yozuv uchun og'ir skoring yoki ML inference hisoblanadigan risk-baholash ishlovi.
- Hujjatlarni OCR yoki rasm transformatsiyasi bilan parallel qayta ishlash.
- Shifrlash/deshifrlash yoki PDF generatsiyasi kabi CPU-bound transformatsiyalar.
- Yagona markaziy manbadan (bitta fayl yoki cursor) o'qib, ishlovni ko'p worker'ga yoyish.
- Mavjud navbat infratuzilmasi bor tizimda worker'larni elastik masshtablash.

**Ehtiyot bo'ling:** Ko'p holatda partitioning yaxshiroq tanlov - remote chunking serializatsiya, tarmoq va middleware ishonchliligi (at-least-once yetkazish, dublikatlar) muammolarini qo'shadi va manager'dagi reader bitta bo'g'iz (bottleneck) bo'lib qoladi. Agar worker'lar o'z ma'lumotini mustaqil o'qiy olsa, remote chunking'ni tanlamang.

## 20.9 Parallel qadamlar va ko'p-thread'li qadam (Parallel Steps / Multi-threaded Step)

**Tavsif:** Bitta JVM ichida parallelizmga erishishning ikki usuli: `split` bilan bir-biriga bog'liq bo'lmagan qadamlarni bir vaqtda bajarish, yoki bitta qadam ichida chunk'larni `TaskExecutor` orqali bir nechta thread'da qayta ishlash. Split qadam darajasida izolyatsiya beradi (har bir shox o'z `StepExecution`iga ega), multi-threaded step esa bitta reader/writer instance'ini thread'lar o'rtasida bo'lishadi - shu sababli ular thread-safe bo'lishi shart.

**Spring'da qayerda uchraydi:** Flow darajasida `FlowBuilder.split(TaskExecutor)` va `SplitBuilder.add(Flow...)`; qadam darajasida `SimpleStepBuilder.taskExecutor(TaskExecutor)` (`ThreadPoolTaskExecutor`, `SimpleAsyncTaskExecutor`; Java 21+ da virtual thread'lar bilan `SimpleAsyncTaskExecutor.setVirtualThreads(true)`). Thread-safety uchun `SynchronizedItemStreamReader` va `SynchronizedItemStreamWriter` wrapper'lari, asinxron processing uchun `spring-batch-integration` dagi `AsyncItemProcessor` + `AsyncItemWriter`. Eski `throttleLimit(...)` Spring Batch 5 dan boshlab deprecated - parallelizm endi executor pool o'lchami bilan boshqariladi.

**Qo'llanish keyslari:**
- Bir-biridan mustaqil uchta fayl eksportini `split()` bilan bir vaqtda generatsiya qilish.
- I/O-bound yozuvni (tashqi API yoki uzoq DB) ko'p thread bilan tezlashtirish.
- `AsyncItemProcessor` bilan har bir element uchun qilinadigan tarmoq chaqiruvlarini overlap qilish.
- Virtual thread'lar yordamida minglab bir vaqtli HTTP chaqiruvi bo'lgan boyitish (enrichment) qadami.
- Mustaqil hisobot va arxivlash qadamlarini parallel bajarib tungi oynani qisqartirish.

**Ehtiyot bo'ling:** Ko'p-thread'li qadamda restartability odatda yo'qoladi - chunk'lar tartibsiz commit bo'lgani uchun reader pozitsiyasi ishonchli checkpoint bermaydi, shuning uchun `saveState(false)` qo'yib, restart strategiyasini (masalan to'liq qayta ishlov yoki partitioning) ongli tanlang. Shuningdek `FlatFileItemReader` kabi stateful reader'lar sinxronlashtirilmasa yozuvlar yo'qoladi yoki takrorlanadi, DB connection pool esa thread soniga mos kattalashtirilishi kerak.

## 20.10 Job parametrlari va job identifikatori (Job Parameters & Job Identity)

**Tavsif:** Job bajarilishini tashqi kirish qiymatlari bilan parametrlash va shu parametrlarning bir qismi orqali `JobInstance`ning yakkayu-yagona identifikatorini aniqlash patterni. Identifying parametrlar to'plami bir xil bo'lsa - bu bir xil mantiqiy ish, ya'ni muvaffaqiyatli tugagan instance'ni qaytadan ishga tushirish mumkin emas, muvaffaqiyatsiz tugagani esa restart qilinadi. Bu "bir kunlik ishlov kuniga faqat bir marta bajariladi" kafolatini infratuzilma darajasida beradi va tasodifiy ikki marta ishga tushirishdan saqlaydi.

**Spring'da qayerda uchraydi:** `JobParameters`, `JobParametersBuilder` va Spring Batch 5 dan boshlab tiplangan `JobParameter<T>` (`identifying` flag bilan); identifikator hisobi `JobKeyGenerator`/`DefaultJobKeyGenerator` orqali, takrorlanadigan ishlar uchun `JobParametersIncrementer` (`RunIdIncrementer`), tekshirish uchun `JobParametersValidator`/`DefaultJobParametersValidator`. Qiymatlarni bean'larga olish uchun `@StepScope`/`@JobScope` va `@Value("#{jobParameters['runDate']}")`; CLI'dan uzatish Spring Boot'da `java -jar app.jar --spring.batch.job.name=dailyJob runDate=2026-10-04` ko'rinishida (`JobLauncherApplicationRunner` orqali). Qayta urinish holatida `JobInstanceAlreadyCompleteException` va `JobExecutionAlreadyRunningException` aynan shu patternning signalidir.

**Qo'llanish keyslari:**
- `runDate` parametri bilan har kun uchun alohida job instance yaratish va idempotentlikni ta'minlash.
- Kelgan fayl yo'lini (`inputFile`) parametr qilib bir job'ni ko'p fayl uchun qayta ishlatish.
- Tenant ID yoki filial kodini parametr qilib bir xil mantiqni turli kontekstlarda bajarish.
- `RunIdIncrementer` bilan test yoki ad-hoc qayta ishga tushirishlarni cheklovsiz bajarish.
- Chunk size yoki grid size kabi sozlamalarni non-identifying parametr sifatida uzatib, identifikatorga ta'sir qilmaslik.

**Ehtiyot bo'ling:** `RunIdIncrementer` ni productionda ko'r-ko'rona qo'shish job identity'ning asosiy foydasini yo'q qiladi - har safar yangi instance yaratilib, bir xil kun ikki marta qayta ishlanishi va dublikat ma'lumot paydo bo'lishi mumkin. Parametr qiymatlari metadata jadvaliga yoziladi, shuning uchun parol, token yoki boshqa maxfiy ma'lumotni job parametri sifatida uzatmang.

## 20.11 Step scope va kechiktirilgan binding (Step Scope / Late Binding)

**Tavsif:** Batch job parametrlari (masalan, fayl nomi, sana oralig'i) faqat job ishga tushgan paytda ma'lum bo'ladi, lekin reader/writer bean'lari Spring context ko'tarilayotganda yaratiladi. Step scope bean'ni singleton emas, balki har bir step execution uchun alohida yaratadi va SpEL ifodalarini step boshlanganda hal qiladi (late binding). Shu tarzda `JobParameters` yoki `ExecutionContext` qiymatlarini to'g'ridan-to'g'ri bean konfiguratsiyasiga inyeksiya qilish mumkin bo'ladi. Qo'shimcha foyda - bean har safar yangi holatda yaratilganligi uchun restart va parallel step'lar xavfsiz ishlaydi.

**Spring'da qayerda uchraydi:** Spring Batch (`spring-boot-starter-batch`, Spring Batch 5.x/6.x) `@StepScope` va `@JobScope` annotatsiyalari; `org.springframework.batch.core.scope.StepScope` va `JobScope` scope implementatsiyalari; SpEL orqali `@Value("#{jobParameters['inputFile']}")`, `#{stepExecutionContext['partitionStart']}`, `#{jobExecutionContext['runId']}`. Konfiguratsiyada `@Bean @StepScope public FlatFileItemReader<Trade> reader(@Value("#{jobParameters['path']}") String path)` ko'rinishida yoziladi; Spring proxy orqali (`ScopedProxyMode.TARGET_CLASS`) singleton step'ga inyeksiya qilinadi. `JobParametersIncrementer` (`RunIdIncrementer`) bilan birga tez-tez qo'llaniladi.

**Qo'llanish keyslari:**
- Har kecha keladigan CSV faylni nomidagi sana bo'yicha o'qish: `#{jobParameters['businessDate']}`.
- Partition qilingan step'da har bir worker o'z `minId`/`maxId` oralig'ini `stepExecutionContext`dan olishi.
- Reporting job'da hisobot davri (`fromDate`, `toDate`) ni `JdbcPagingItemReader` so'rov parametrlariga uzatish.
- Bir xil job'ni turli mijoz (tenant) uchun `tenantId` parametri bilan qayta ishga tushirish.
- Faylga yozuvchi `FlatFileItemWriter` uchun chiqish yo'lini run vaqtida aniqlash.

**Ehtiyot bo'ling:** `@StepScope` bean'ni step kontekstidan tashqarida (masalan, oddiy `@Service` ichida yoki test'da step'siz) chaqirsangiz `ScopeNotActiveException` olasiz; shuningdek step-scoped bean'ni qo'lda `new` bilan yaratish late binding'ni butunlay o'chiradi. `@StepScope` ni `ItemReader` interfeysini qaytaruvchi metodda e'lon qilsangiz, Spring `ItemStream` metodlarini ko'rmay qolishi mumkin - qaytish turini aniq sinf (`FlatFileItemReader`) qilib yozing.

## 20.12 Listener'lar (Listeners - JobExecutionListener, StepExecutionListener)

**Tavsif:** Batch job'ning hayot tsiklidagi muhim nuqtalariga (job boshlanishi/tugashi, step boshlanishi/tugashi, chunk, har bir item o'qilishi/ishlanishi/yozilishi, xato) biznes mantiqdan ajratilgan callback'lar ulash patterni. Bu cross-cutting vazifalarni - audit, metrika, xabarnoma, resurs tozalash, xato hisobotini - reader/processor/writer kodiga aralashtirmasdan bajarishga imkon beradi. Listener'lar `ExecutionContext` orqali holatni o'qiydi va yozadi, shuning uchun restart mantiqi uchun ham qulay. Bir nechta listener zanjir bo'lib ro'yxatga olinadi va e'lon qilingan tartibda chaqiriladi.

**Spring'da qayerda uchraydi:** Spring Batch interfeyslari `JobExecutionListener`, `StepExecutionListener`, `ChunkListener`, `ItemReadListener`, `ItemProcessListener`, `ItemWriteListener`, `SkipListener`, `RetryListener`; annotatsiya variantlari `@BeforeJob`, `@AfterJob`, `@BeforeStep`, `@AfterStep`, `@AfterChunkError`, `@OnSkipInRead`, `@OnWriteError`. Ro'yxatga olish `JobBuilder.listener(...)` va `StepBuilder.listener(...)` orqali; `ExecutionContextPromotionListener` step context'dagi kalitlarni job context'ga ko'taradi. Spring Boot 3.x da `BatchMetrics`/Micrometer `spring.batch.*` metrikalarini avtomatik chiqaradi, `JobExecutionListener` esa Micrometer `Counter` yoki `MeterRegistry` bilan birga qo'llaniladi.

**Qo'llanish keyslari:**
- Job tugaganda natija (o'qilgan/yozilgan/skip soni) bo'yicha email yoki Slack xabarnoma yuborish.
- `@BeforeJob` da kirish faylining mavjudligini va checksum'ini tekshirib, yo'q bo'lsa job'ni darhol to'xtatish.
- `SkipListener` bilan tashlab ketilgan yozuvlarni "rejected" jadvaliga yoki dead-letter faylga yozish.
- `StepExecutionListener` da staging jadvalni step boshida tozalash, oxirida indeks qayta qurish.
- `ExecutionContextPromotionListener` orqali birinchi step hisoblagan `batchId` ni keyingi step'larga uzatish.

**Ehtiyot bo'ling:** `@AfterStep` yoki `afterStep` ichida `ExitStatus` ni qaytarib step natijasini jimgina o'zgartirish flow mantiqini kutilmaganda buzadi - bu yerda faqat ataylab va hujjatlashtirilgan holda `ExitStatus` qaytaring. Item-level listener'lar (`ItemReadListener`) millionlab marta chaqiriladi, shuning uchun ularda log yozish yoki DB chaqirig'i qilish job'ni bir necha barobar sekinlashtiradi.

## 20.13 Kompozit ItemProcessor / ItemWriter (Composite ItemProcessor / ItemWriter)

**Tavsif:** Bir nechta mayda, bir vazifani bajaruvchi processor yoki writer'ni ketma-ket zanjirga yig'ib, step'ga yagona komponent sifatida berish patterni. Processor zanjirida birinchisining chiqishi ikkinchisiga kirish bo'ladi (validatsiya → boyitish → mapping), writer kompozitida esa bir xil item to'plami har bir writer'ga navbat bilan yoziladi (DB + fayl + event). Bu Single Responsibility va qayta ishlatishni ta'minlaydi, chunki har bir bo'lak alohida test qilinadi. Chunk transaction chegarasi o'zgarmaydi - butun zanjir bitta chunk ichida bajariladi.

**Spring'da qayerda uchraydi:** `org.springframework.batch.item.support.CompositeItemProcessor` (`setDelegates(List)`) va `CompositeItemWriter` (`setDelegates(List)`); Spring Batch 5.x da builder'lar `CompositeItemProcessorBuilder` va `CompositeItemWriterBuilder`. Hamkor sinflar: `ValidatingItemProcessor`/`BeanValidatingItemProcessor` (Jakarta Bean Validation), `ScriptItemProcessor`, `FunctionItemProcessor` (Java `Function` ni o'rash), `ItemProcessorAdapter`. Writer tomonida `JdbcBatchItemWriter`, `JpaItemWriter`, `FlatFileItemWriter`, `KafkaItemWriter`, `MongoItemWriter` delegate sifatida ishlatiladi; `CompositeItemWriter` `ItemStream` bo'lgan delegate'larni avtomatik `open/update/close` qiladi.

**Qo'llanish keyslari:**
- Kirish yozuvini avval Bean Validation bilan tekshirib, so'ng referens ma'lumot bilan boyitib, oxirida DTO dan entity'ga o'girish.
- Bitta chunk'ni ham `JdbcBatchItemWriter` bilan DB ga, ham `FlatFileItemWriter` bilan audit faylga yozish.
- Yozuv saqlangandan keyin `KafkaItemWriter` orqali downstream tizimlarga event chiqarish.
- Legacy va yangi jadvalga parallel yozish (dual-write) migratsiya davrida.
- Umumiy maskalash/PII tozalash processor'ini bir nechta job'da qayta ishlatish.

**Ehtiyot bo'ling:** `CompositeItemProcessor` da oraliq processor `null` qaytarsa, item filtrlanadi va zanjirning qolgan qismi umuman chaqirilmaydi - filtrlash qadamini ataylab oxirgi yoki birinchi o'ringa qo'ying. `CompositeItemWriter` atomar emas: ikkinchi writer xato bersa birinchisining yozgani (ayniqsa Kafka yoki tashqi API) qaytmaydi, shuning uchun non-transactional resurslarni oxiriga qo'yib, idempotentlikni ta'minlang.

## 20.14 Classifier bilan kompozit writer (Classifier Composite Writer)

**Tavsif:** Bir step'dan chiqayotgan heterogen item'larni turiga yoki biror atributiga qarab turli writer'larga yo'naltirish patterni. `Classifier` har bir item uchun mos writer'ni tanlaydi, shuning uchun bitta job ichida bir nechta chiqish kanalini (jadval, fayl, queue) saqlab qolish mumkin bo'ladi. Bu `if/else` ni writer ichiga yashirishdan ko'ra toza, chunki marshrutlash mantiqi deklarativ va alohida test qilinadi. Xuddi shu yondashuv reader va processor uchun ham mavjud.

**Spring'da qayerda uchraydi:** `org.springframework.batch.item.support.ClassifierCompositeItemWriter` va `ClassifierCompositeItemProcessor`; klassifikatorlar `org.springframework.classify.Classifier`, `SubclassClassifier`, `PatternMatchingClassifier`, `BackToBackPatternClassifier` (`spring-retry` ichidagi `org.springframework.classify` paketi). Builder: `ClassifierCompositeItemWriterBuilder`. Delegate'lar odatda `JdbcBatchItemWriter`, `FlatFileItemWriter`, `KafkaItemWriter` bo'ladi.

```java
@Bean
ClassifierCompositeItemWriter<Txn> writer(ItemWriter<Txn> ok, ItemWriter<Txn> rejected) {
    return new ClassifierCompositeItemWriterBuilder<Txn>()
        .classifier(t -> t.isValid() ? ok : rejected)
        .build();
}
```

**Qo'llanish keyslari:**
- Valid yozuvlarni asosiy jadvalga, xato yozuvlarni "rejected" faylga yo'naltirish.
- Bitta multi-format faylidan o'qilgan header/detail/trailer yozuvlarini turli jadvallarga yozish.
- To'lov turiga qarab (card, transfer, cash) har birini o'z jadvaliga yozish.
- Mijoz segmentiga qarab item'ni turli Kafka topic'larga chiqarish.
- Multi-tenant job'da tenant bo'yicha turli datasource writer'larini tanlash.

**Ehtiyot bo'ling:** `ClassifierCompositeItemWriter` delegate'larining `ItemStream` metodlarini o'zi chaqirmaydi - har bir stateful writer'ni step'ga `StepBuilder.stream(writer)` orqali alohida ro'yxatdan o'tkazmasangiz, fayl ochilmaydi yoki restart holati yo'qoladi. Classifier hech qachon `null` qaytarmasligi kerak, aks holda item jimgina tushib qolishi yoki `NullPointerException` chiqishi mumkin.

## 20.15 Paging reader va cursor reader (Paging Reader vs Cursor Reader)

**Tavsif:** Katta hajmli DB natijalarini o'qishning ikki asosiy strategiyasi. Cursor reader bitta ochiq `ResultSet`/cursor ustida qatorlarni stream qilib oladi - bitta so'rov, kam overhead, lekin uzoq ochiq connection va non-restartable pozitsiya muammosi. Paging reader esa natijani `LIMIT/OFFSET` yoki keyset shartlari bilan bo'lib, har sahifa uchun yangi so'rov yuboradi - connection qisqa muddat ushlanadi, restart va multithreaded step uchun xavfsiz. Tanlov hajm, tranzaksiya davomiyligi va thread-safety talablaridan kelib chiqadi.

**Spring'da qayerda uchraydi:** Cursor tomoni: `JdbcCursorItemReader`, `StoredProcedureItemReader`, `HibernateCursorItemReader` (`spring-batch-infrastructure`). Paging tomoni: `JdbcPagingItemReader` + `SqlPagingQueryProviderFactoryBean` (yoki `PostgresPagingQueryProvider`, `OraclePagingQueryProvider`), `JpaPagingItemReader`, `HibernatePagingItemReader`, `RepositoryItemReader` (Spring Data `PagingAndSortingRepository` ustida), `MongoPagingItemReader`. Builder'lar: `JdbcPagingItemReaderBuilder`, `JpaPagingItemReaderBuilder`. Paging reader'da `setSortKeys()` majburiy, keyset-style pagination esa `SqlPagingQueryProvider` orqali `sortKey > :lastValue` shaklida generatsiya qilinadi.

**Qo'llanish keyslari:**
- 50 million qatorli jadvalni tungi ETL da o'qish - `JdbcPagingItemReader` bilan restartable qilish.
- Multithreaded step yoki partitioning'da thread-safe reader kerak bo'lganda paging reader tanlash.
- Kichik-o'rta (bir necha yuz ming) va bir martalik o'qishda tezlik uchun `JdbcCursorItemReader` ishlatish.
- Stored procedure natijasini stream qilib o'qish uchun `StoredProcedureItemReader`.
- Spring Data entity'lari ustida tayyor repository metodidan `RepositoryItemReader` bilan o'qish.

**Ehtiyot bo'ling:** `OFFSET` asosidagi paging chuqur sahifalarda kvadratik sekinlashadi va o'qish davomida ma'lumot o'zgarsa qatorlar takrorlanadi yoki tushib qoladi - barqaror, unikal `sortKey` (odatda primary key) ishlatib keyset pagination'ga o'ting. `JdbcCursorItemReader` va `HibernateCursorItemReader` thread-safe emas: ularni multithreaded step yoki parallel flow'da ishlatish ma'lumotni buzadi.

## 20.16 Staging jadval (Staging Table)

**Tavsif:** Tashqi manbadan kelgan xom ma'lumotni avval oraliq (staging) jadvalga minimal validatsiya bilan yuklab, keyin alohida step'larda tozalash, boyitish va asosiy jadvallarga ko'chirish patterni. Bu kirish bilan biznes mantiqni ajratadi: fayl o'qish xatosi va biznes xatosi turli step'larda aniqlanadi, qayta ishlash esa faylni emas, DB ni manba qilib oladi. Staging jadval shuningdek audit izi, qayta tiklash (replay) va set-based SQL transformatsiyalari uchun imkon beradi. Odatda `batch_id`, `status`, `loaded_at` ustunlari bilan birga keladi.

**Spring'da qayerda uchraydi:** Spring Batch'ning ko'p step'li job'i: birinchi step `FlatFileItemReader` + `JdbcBatchItemWriter` bilan staging jadvalga yuklaydi; keyingi step `JdbcPagingItemReader` bilan staging'dan o'qiydi. Katta set-based o'tkazish uchun `TaskletStep` (`org.springframework.batch.core.step.tasklet.Tasklet`) ichida `JdbcTemplate`/`NamedParameterJdbcTemplate` bilan `INSERT ... SELECT`/`MERGE` bajariladi. Spring Batch'ning o'zida `org.springframework.batch.item.database.JdbcBatchItemWriter`, sxema boshqaruvi uchun Flyway yoki Liquibase, tezkor yuklash uchun PostgreSQL `COPY` yoki Oracle external table ishlatiladi.

**Qo'llanish keyslari:**
- Bank fayl almashinuvida (SWIFT, ISO 20022) kelgan faylni avval staging'ga yuklab, keyin reconciliation qilish.
- Kunlik mijoz eksportini staging'da deduplikatsiya qilib, so'ng `MERGE` bilan master jadvalga qo'shish.
- Xato yozuvlarni staging'da `status='REJECTED'` deb belgilab, biznes foydalanuvchisiga hisobot berish.
- Legacy tizimdan migratsiyada xom ma'lumotni saqlab, transformatsiyani bir necha marta qayta ishga tushirish.
- Juda katta hajmda row-by-row processing o'rniga set-based SQL transformatsiyaga o'tish.

**Ehtiyot bo'ling:** Staging jadvalni tozalash siyosatini (partition drop yoki `TRUNCATE`) boshidan belgilamasang, jadval o'sib ketib DB ni bo'g'adi va indeks'lar yuklash tezligini keskin pasaytiradi. Bir vaqtda bir nechta job instansiyasi bir xil staging jadvalga yozishi mumkin bo'lsa, `batch_id` bo'yicha izolyatsiya qiling - aks holda bir job boshqasining ma'lumotini ko'chirib yuboradi.

## 20.17 Boshqaruvchi so'rov (Driving Query)

**Tavsif:** Butun og'ir obyektni emas, faqat kalitlar (ID) ro'yxatini o'qib olib, har bir kalit uchun detallarni processor ichida alohida yuklash patterni. Reader yengil va kam xotira ishlatadigan bo'lib qoladi, cursor uzoq ushlanmaydi, ORM esa bitta katta join natijasi o'rniga aniq navigatsiya qiladi. Bu klassik "ID list + per-item fetch" yondashuvi bo'lib, murakkab obyekt graflarini batch qilishda ishlatiladi. Kamchiligi - N+1 so'rov, shuning uchun u ko'pincha chunk-level batch fetch bilan birlashtiriladi.

**Spring'da qayerda uchraydi:** Reader sifatida `JdbcPagingItemReader` yoki `JdbcCursorItemReader` faqat `SELECT id FROM ...` qaytaradi (`SingleColumnRowMapper`); processor esa `ItemProcessor` ichida `JdbcTemplate`, Spring Data repository (`findById`, `findAllById`) yoki JPA `EntityManager` bilan to'liq obyektni yuklaydi. Chunk darajasida samaradorlik uchun `ItemProcessor` o'rniga `ItemWriter`/`ItemProcessor` ni `findAllById(ids)` bilan to'plab chaqirish, yoki Spring Batch 5.x `ItemProcessor` zanjiriga `RepositoryItemReader` qo'shish mumkin. `@StepScope` bilan birga ko'p ishlatiladi.

**Qo'llanish keyslari:**
- Faqat o'zgargan buyurtmalar ID'larini olib, keyin har biri uchun to'liq agregatni yuklab qayta hisoblash.
- ORM lazy-loading'li chuqur obyekt graflarini (order → items → shipments) batch qilishda.
- Partitioning uchun ID oraliqlarini aniqlashda boshqaruvchi so'rovdan `min/max` olish.
- Tashqi API dan boyitish kerak bo'lgan hollarda avval kalitlar ro'yxatini olish.
- Katta jadvalda murakkab join'ni cursor'da uzoq ushlab turmaslik uchun.

**Ehtiyot bo'ling:** Har bir item uchun alohida so'rov yuborish N+1 muammosini keltiradi va millionlab yozuvda job'ni soatlarga uzaytiradi - iloji bo'lsa chunk ichida `findAllById` yoki `IN (:ids)` bilan to'plab yuklang. Shuningdek kalitlar ro'yxati o'qilgandan keyin ma'lumot o'zgarishi mumkin, shuning uchun processor topilmagan ID larni (o'chirilgan yozuv) jimgina `null` qaytarib filtrlashi yoki aniq xato berishi kerakligini oldindan hal qiling.

## 20.18 Process indikatori (Process Indicator)

**Tavsif:** Qayta ishlanishi kerak bo'lgan har bir yozuvga holat ustuni (`status`, `processed`, `claimed_by`) qo'shib, kim nimani olganini va nima tugaganini DB ning o'zida belgilash patterni. Shu tufayli job restart bo'lganda yoki bir nechta worker parallel ishlaganda hech bir yozuv ikki marta ishlanmaydi va hech biri tushib qolmaydi. Ishlash sxemasi: `SELECT ... WHERE status='NEW'` → ishlash → `UPDATE ... SET status='DONE'` bir tranzaksiyada. Parallel ishlashda yozuvlar odatda `UPDATE ... SET claimed_by=:worker WHERE status='NEW'` bilan "band qilinadi".

**Spring'da qayerda uchraydi:** Spring Batch da reader `JdbcPagingItemReader` status filtri bilan, holatni yangilash esa `CompositeItemWriter` ning ikkinchi delegate'i (`JdbcBatchItemWriter` bilan `UPDATE`) yoki `ItemWriteListener`/`ChunkListener` orqali amalga oshiriladi. Partitioning'da `org.springframework.batch.core.partition.support.Partitioner` (masalan `ColumnRangePartitioner` ko'rinishidagi o'z implementatsiyangiz) va `TaskExecutorPartitionHandler` bilan birga ishlatiladi. DB tomonida PostgreSQL `SELECT ... FOR UPDATE SKIP LOCKED` yoki Oracle `SKIP LOCKED` orqali band qilish; `@Transactional` va `PlatformTransactionManager` chunk tranzaksiyasini ta'minlaydi.

**Qo'llanish keyslari:**
- Outbox jadvalidagi yuborilmagan event'larni bir nechta pod parallel ishlashi.
- To'lov so'rovlarini qayta ishlashda exactly-once semantikasini DB holati bilan ta'minlash.
- Yarim yo'lda to'xtagan job'ni restart qilganda faqat `NEW` yozuvlardan davom etish.
- Uzoq davom etadigan migratsiyada progressni kuzatish va to'xtatib-davom ettirish.
- Xato bergan yozuvlarni `status='ERROR'` qilib belgilab, alohida retry job'i bilan qayta urinish.

**Ehtiyot bo'ling:** Holat yangilanishi biznes yozuvi bilan bitta tranzaksiyada bo'lmasa (masalan avtokommit yoki boshqa datasource), crash paytida ikki marta ishlash yoki tushib qolish yuzaga keladi. Oddiy `WHERE status='NEW'` ni `SKIP LOCKED` yoki optimistik versiyalashsiz parallel worker'larda ishlatish lock kutish va duplikatlarga olib keladi; shuningdek holat ustuniga indeks qo'ymasang, jadval o'sgani sari har sahifa so'rovi sekinlashadi.

## 20.19 Extract-Transform-Load (Extract-Transform-Load - ETL)

**Tavsif:** Ma'lumotni manbadan ajratib olish (extract), biznes qoidalari bo'yicha o'zgartirish (transform) va maqsadli tizimga yuklash (load) bosqichlarini aniq ajratilgan fazalarga bo'lish patterni. Har bir faza alohida kuzatiladi, qayta ishga tushiriladi va masshtablanadi, shuning uchun xato qaysi bosqichda bo'lganini aniqlash oson. Spring Batch'ning chunk-oriented modeli aynan shu patternning to'g'ridan-to'g'ri ifodasi: reader = extract, processor = transform, writer = load. Zamonaviy variantda tartib ELT ga o'zgaradi - xom ma'lumot avval ombor'ga yuklanib, transformatsiya SQL da bajariladi.

**Spring'da qayerda uchraydi:** Chunk-oriented step: `StepBuilder.chunk(size, txManager).reader(...).processor(...).writer(...)` (Spring Batch 5.x/6.x da `StepBuilder` konstruktorga `JobRepository` oladi). Reader/writer implementatsiyalari: `FlatFileItemReader`, `StaxEventItemReader`, `JsonItemReader`, `JdbcPagingItemReader`, `KafkaItemReader`; `JdbcBatchItemWriter`, `JpaItemWriter`, `FlatFileItemWriter`, `AvroItemWriter`. Orkestratsiya uchun `JobLauncher`, `JobOperator`, `@EnableBatchProcessing` (yoki Spring Boot 3.x avtokonfiguratsiyasi), uzoq pipeline'lar uchun Spring Cloud Data Flow va Spring Cloud Task. Fayl yoki queue orqali kelgan oqim uchun Spring Integration (`spring-integration-file`) bilan birlashtiriladi.

**Qo'llanish keyslari:**
- Kunlik operatsion DB dan data warehouse'ga fakt va o'lchov jadvallarini yuklash.
- Bir nechta hamkor tizimdan kelgan turli formatli fayllarni yagona kanonik modelga keltirish.
- Legacy mainframe fixed-length faylini relyatsion sxemaga ko'chirish.
- Moliyaviy hisobot uchun kunlik agregatlarni hisoblab, reporting jadvaliga yozish.
- CRM va billing tizimlari o'rtasida tungi sinxronizatsiya.

**Ehtiyot bo'ling:** Transformatsiyani writer yoki reader ichiga yashirish fazalar ajratilishini buzadi va job'ni test qilishni deyarli imkonsiz qiladi - biznes mantiqni `ItemProcessor` da saqlang. Juda katta hajmda row-by-row ETL tabiiy chegaraga uriladi: bunda set-based SQL (ELT) yoki partitioning'ga o'tishni oldindan rejalashtiring, va qayta yuklashda idempotentlikni (`MERGE`/upsert) ta'minlamasang duplikatlar paydo bo'ladi.

## 20.20 Backfill (Backfill)

**Tavsif:** Mavjud, ko'pincha juda katta hajmli tarixiy ma'lumotni yangi sxema, yangi hisoblangan maydon yoki yangi tizimga bir martalik (yoki takrorlanadigan) to'ldirish patterni. Asosiy talablar: ishlab turgan production yukini bo'g'maslik, to'xtatib-davom ettirish imkoniyati, idempotentlik va progressni kuzatish. Odatda ma'lumot kalit oralig'i yoki sana bo'yicha bo'laklarga (chunk/partition) bo'linadi, har bo'lak alohida tranzaksiyada ishlanadi va tezlik throttling bilan boshqariladi. Natija oxirida tekshirish (reconciliation) so'rovi bilan tasdiqlanadi.

**Spring'da qayerda uchraydi:** Spring Batch job'i `Partitioner` + `TaskExecutorPartitionHandler` (bitta JVM da) yoki `MessageChannelPartitionHandler` (`spring-batch-integration`, remote partitioning) bilan; har bir partition `@StepScope` reader'ga `minId`/`maxId` oladi. Progress `JobRepository` jadvallarida (`BATCH_STEP_EXECUTION`) va `ExecutionContext` da saqlanadi, qayta ishga tushirish `JobOperator.restart(...)` yoki `RunIdIncrementer` bilan. Throttling uchun `TaskExecutor` pool o'lchami va chunk size, Kubernetes muhitida Spring Cloud Task / Spring Batch'ning `--spring.batch.job.name` bilan ishlatiladigan Job resurslari; sxema o'zgarishi Flyway/Liquibase migratsiyalari bilan muvofiqlashtiriladi.

**Qo'llanish keyslari:**
- Yangi qo'shilgan ustunni (masalan normallashtirilgan telefon raqami) 200 million qatorda to'ldirish.
- Yangi search index yoki read-model'ni tarixiy event'lar asosida qayta qurish (CQRS projection rebuild).
- Xato deploy sababli noto'g'ri hisoblangan qiymatlarni ma'lum sana oralig'ida qayta hisoblash.
- Yangi mikroservis DB siga legacy monolitdan tarixni ko'chirish (dual-write davrida).
- Yangi joriy qilingan audit/compliance maydonlarini eski yozuvlar uchun to'ldirish.

**Ehtiyot bo'ling:** Throttling'siz backfill DB ni, replication lag'ni va connection pool'ni to'ldirib production'ni yiqitadi - chunk o'lchami, parallel worker soni va ish vaqti oynasini (off-peak) aniq cheklang. Backfill idempotent bo'lishi shart (`WHERE col IS NULL` yoki versiya tekshiruvi): aks holda qayta ishga tushirish qiymatlarni ikki marta o'zgartiradi, shuningdek bir vaqtda ishlayotgan ilova yozuvlari bilan yozish poygasiga tushib, yangi ma'lumotni eski qiymat bilan ustiga yozishi mumkin.

## 20.21 Rejalashtirilgan vazifalar (Scheduled Tasks)

**Tavsif:** Ilova ichida vaqt bo'yicha takrorlanadigan ishlarni (hisobot yig'ish, cache yangilash, holat tekshirish) tashqi cron demoniga bog'lanmasdan bajarish patterni. Metod darajasida deklarativ jadval beriladi: fixed rate, fixed delay yoki cron ifodasi. Scheduler alohida thread pool'da ishlaydi va har bir trigger uchun metodni chaqiradi, shuning uchun vazifa kodi qisqa va bloklanmaydigan bo'lishi kerak.

**Spring'da qayerda uchraydi:** `@EnableScheduling` (Spring Boot'da `spring-boot-starter`dagi auto-configuration orqali avtomatik) va `@Scheduled(cron = "...", fixedDelay = ..., fixedRate = ..., initialDelay = ...)`; infratuzilma sifatida `TaskScheduler`, `ThreadPoolTaskScheduler` va Spring Framework 6.1+ dagi `SimpleAsyncTaskScheduler` (virtual thread'lar uchun, `spring.threads.virtual.enabled=true`). Nozik sozlash uchun `SchedulingConfigurer` interfeysi, dinamik trigger uchun `CronTrigger`/`PeriodicTrigger`, ifodani tekshirish uchun `org.springframework.scheduling.support.CronExpression`. Boot 3.x da pool o'lchami `spring.task.scheduling.pool.size`, Spring Framework 6.1+ da `@Scheduled(scheduler = "myScheduler")` bilan alohida scheduler tanlanadi; `@Scheduled(cron = "...", zone = "Asia/Tashkent")` vaqt mintaqasini belgilaydi.

**Qo'llanish keyslari:**
- Har kuni ertalab 02:00 da kunlik moliyaviy hisobotni generatsiya qilish.
- Har 30 sekundda tashqi hamkor API'sidan valyuta kurslarini olib cache'ni yangilash.
- Har 5 minutda outbox jadvalidagi yuborilmagan event'larni broker'ga uzatish.
- Har soatda sessiya jadvalidagi muddati o'tgan token'larni bekor qilish.
- Har hafta dushanba kuni mijozlarga obuna muddati haqida eslatma tayyorlash.

**Ehtiyot bo'ling:** Standart `ThreadPoolTaskScheduler` pool o'lchami birga teng, shuning uchun bitta sekin vazifa boshqa barcha jadvallarni kechiktiradi - pool'ni kattalashtiring yoki og'ir ishni `@Async`/alohida executor'ga chiqaring. Bir nechta instance'da deploy qilinganda `@Scheduled` har bir node'da mustaqil ishga tushadi, ya'ni bu pattern o'zi klaster uchun xavfsiz emas: lock yoki leader election bilan birga ishlatilishi shart.

## 20.22 Taqsimlangan scheduler lock (Distributed Scheduler Lock, ShedLock)

**Tavsif:** Bir xil `@Scheduled` vazifa bir nechta instance'da bir vaqtda ishga tushib, ishni ikki marta bajarishini oldini oladi. Yechim - umumiy tashqi store'dagi (DB jadvali, Redis, Mongo, ZooKeeper) nomlangan lock: trigger vaqti kelganda faqat lock'ni egallagan node ishni bajaradi, qolganlari jimgina chiqib ketadi. Lock muddat bilan beriladi, shuning uchun node o'lsa ham lock avtomatik bo'shaydi.

**Spring'da qayerda uchraydi:** Eng keng tarqalgani ShedLock (`net.javacrumbs.shedlock:shedlock-spring`): `@EnableSchedulerLock(defaultLockAtMostFor = "PT10M")` va metod ustida `@SchedulerLock(name = "...", lockAtMostFor = "...", lockAtLeastFor = "...")`; store uchun `LockProvider` implementatsiyalari - `JdbcTemplateLockProvider` (`shedlock` jadvali), Redis, MongoDB, ZooKeeper, DynamoDB variantlari. Spring'ning o'z stack'ida muqobil sifatida Spring Integration `LockRegistry` (`JdbcLockRegistry`, `RedisLockRegistry`) yoki Redisson `RLock` ishlatiladi.

```java
@Scheduled(cron = "0 0 2 * * *")
@SchedulerLock(name = "dailySettlement", lockAtMostFor = "PT30M", lockAtLeastFor = "PT1M")
public void runDailySettlement() {
    settlementService.settleForDate(LocalDate.now().minusDays(1));
}
```

**Qo'llanish keyslari:**
- Multi-instance Boot ilovasida kunlik hisob-kitob (settlement) jobini aynan bir marta ishga tushirish.
- Outbox publisher'ni faqat bitta node'da aylantirib, event dublikatlarini kamaytirish.
- Tashqi provayderga kvota bilan cheklangan sinxronizatsiya chaqiruvlarini bir nusxada bajarish.
- Kubernetes'da `replicas: 3` bo'lgan servisdagi cache warm-up vazifasini koordinatsiya qilish.
- Blue-green deploy paytida eski va yangi versiya bir vaqtda ishlayotganda ikki marta bajarilishni to'sish.

**Ehtiyot bo'ling:** `lockAtMostFor` vazifaning real maksimal davomiyligidan katta bo'lishi kerak, aks holda lock muddati tugab boshqa node ishni parallel boshlab yuboradi - bu eng ko'p uchraydigan xato. Lock "at most once" kafolatini bermaydi (node to'xtab qolsa ish yarim bajarilgan bo'lishi mumkin), shuning uchun vazifaning o'zi ham idempotent bo'lsin.

## 20.23 Quartz klasterlash (Quartz Clustering)

**Tavsif:** Quartz - persistent job store'ga ega to'laqonli scheduler: trigger'lar va job detail'lar bazada saqlanadi, shuning uchun ilova qayta ishga tushsa ham jadval yo'qolmaydi. Klaster rejimida bir nechta node bitta jadval to'plamini `SELECT ... FOR UPDATE` asosidagi lock bilan bo'lishadi va har bir trigger'ni faqat bitta node bajaradi. Misfire siyosati node o'lgan yoki kechikkan holatda nima qilishni belgilaydi.

**Spring'da qayerda uchraydi:** `spring-boot-starter-quartz`, `SchedulerFactoryBean` auto-configuration, `JobDetail`/`Trigger` bean'lari (`JobBuilder`, `TriggerBuilder`, `CronScheduleBuilder`), Spring bean'larini inject qilish uchun `SpringBeanJobFactory`. Boot property'lari: `spring.quartz.job-store-type=jdbc`, `spring.quartz.jdbc.initialize-schema`, `spring.quartz.properties.org.quartz.jobStore.isClustered=true`, `...clusterCheckinInterval`, `...org.quartz.scheduler.instanceId=AUTO`. Job sinflari `QuartzJobBean`dan meros oladi yoki `org.quartz.Job`ni amalga oshiradi; konkurensiyani cheklash uchun `@DisallowConcurrentExecution` va `@PersistJobDataAfterExecution`. Bazada `QRTZ_*` jadvallari yaratiladi.

**Qo'llanish keyslari:**
- Foydalanuvchi tomonidan runtime'da yaratiladigan eslatma va bildirishnoma jadvallari (har bir mijozga o'z cron'i).
- SaaS platformasida har bir tenant uchun alohida hisobot jadvalini dinamik ro'yxatga olish.
- Node restart'idan keyin ham yo'qolmasligi kerak bo'lgan kechiktirilgan bir martalik vazifalar (masalan, 24 soatdan keyin buyurtmani bekor qilish).
- HA talab qiladigan integratsiya jadvallarini klasterda avtomatik failover bilan ishlatish.
- Admin UI'dan jadvalni to'xtatish, pauza qilish va qayta ishga tushirish imkonini berish.

**Ehtiyot bo'ling:** Klaster rejimida barcha node'lar bir xil `org.quartz.jobStore` sozlamalari, bir xil DB va sinxronlashgan tizim vaqtiga ega bo'lishi shart - clock drift trigger'larni ikki marta ishga tushirishga olib keladi. Oddiy "har 5 minutda bitta ish" uchun Quartz juda og'ir: `QRTZ_*` jadvallari, migratsiya va misfire semantikasini qo'shimcha yuk sifatida olib kelmaslik uchun bunday holatda `@Scheduled` + ShedLock yetarli.

## 20.24 Joblar uchun leader election (Leader Election for Jobs)

**Tavsif:** Har bir vazifaga alohida lock olish o'rniga, klasterdagi node'lardan biri "leader" sifatida tanlanadi va barcha scheduled ishlarni faqat shu node bajaradi. Leader'lik umumiy lock registry yoki konsensus store orqali ushlab turiladi va muntazam yangilanadi; leader yo'qolsa, qolganlardan biri uning o'rnini oladi. Bu scheduler holatini bir joyda markazlashtiradi va vazifalar orasidagi tartibni saqlashni osonlashtiradi.

**Spring'da qayerda uchraydi:** Spring Integration'dagi `org.springframework.integration.support.leader.LockRegistryLeaderInitiator` + `DefaultCandidate`, hamda `LockRegistry` implementatsiyalari (`JdbcLockRegistry`, `RedisLockRegistry`, `ZookeeperLockRegistry`); leader'lik o'zgarishi `OnGrantedEvent`/`OnRevokedEvent` application event'lari bilan e'lon qilinadi va ularga `@EventListener` orqali reaksiya qilib scheduler'ni yoqish/o'chirish mumkin. Kubernetes muhitida `spring-cloud-kubernetes-fabric8-leader` ConfigMap asosida leader tanlaydi; past darajada Apache Curator `LeaderSelector`/`LeaderLatch` ishlatiladi. Ko'pincha leader flag'i `SmartLifecycle` yoki `ScheduledTaskRegistrar` bilan birga, vazifalarni dinamik ravishda ro'yxatga olish uchun qo'llanadi.

**Qo'llanish keyslari:**
- Klasterda o'nlab `@Scheduled` vazifa bor va ularning har biriga alohida lock qo'yish noqulay bo'lganda.
- Ketma-ketligi muhim bo'lgan job'lar zanjirini (ETL step'lari) bir node'da tartib bilan bajarish.
- Kafka consumer bo'lmagan, lekin bitta nusxada ishlashi kerak bo'lgan background aggregator'ni boshqarish.
- Legacy fayl integratsiyasida umumiy katalogni faqat bitta node'ning poll qilishi.
- In-memory holat (masalan, hisoblangan hisobot buffer'i) saqlaydigan komponentni faqat leader'da yoqish.

**Ehtiyot bo'ling:** Split-brain real xavf: tarmoq uzilishida eski leader o'zini hali ham leader deb hisoblab ishni davom ettirishi mumkin, shuning uchun vazifalar idempotent bo'lishi va lock TTL qisqa bo'lishi kerak. Barcha yuklamani bitta node'ga yig'ish resurs nomutanosibligini keltiradi - CPU-og'ir batch uchun leader'ni faqat koordinator qilib, haqiqiy ishni worker'larga tarqatish to'g'riroq.

## 20.25 Spring Cloud Task

**Tavsif:** Qisqa muddat ishlaydigan, boshlanib tugaydigan (short-lived) mikroservislar uchun hayot sikli va audit patterni. Ilova ishga tushganda ish boshlanish yozuvi, tugaganda tugash vaqti va exit kod bazaga yoziladi, so'ng JVM to'xtaydi. Bu uzluksiz ishlab turadigan servis emas, balki konteyner sifatida ishga tushirilib tugaydigan vazifa modelini Spring Boot ichida standartlashtiradi.

**Spring'da qayerda uchraydi:** `spring-cloud-task-core` va `@EnableTask`; audit uchun `TaskRepository`, `TaskExplorer`, `TaskExecution` modeli va `TASK_EXECUTION`/`TASK_EXECUTION_PARAMS` jadvallari; hayot siklini boshqaruvchi `TaskLifecycleListener`, natijani belgilash uchun `ExitCodeGenerator`/`ExitCodeExceptionMapper`. Spring Batch bilan integratsiya `spring-cloud-task-batch` modulida: `TaskBatchExecutionListener` job execution'ni task execution'ga bog'laydi, remote partitioning uchun `DeployerPartitionHandler` va `DeployerStepExecutionHandler` worker'larni platformada (Kubernetes, Cloud Foundry) ishga tushiradi. Orkestratsiya va UI qatlami - Spring Cloud Data Flow.

**Qo'llanish keyslari:**
- Kubernetes `CronJob` sifatida ishga tushirilib tugaydigan kechki ETL vazifasini auditi bilan yuritish.
- Spring Batch job'ini mustaqil konteyner sifatida ishga tushirib, natijani markazlashgan jadvalda kuzatish.
- Remote partitioning bilan katta faylni o'nlab vaqtinchalik worker pod'larga bo'lib ishlash.
- Ma'lumotlar migratsiyasi yoki bir martalik backfill skriptini kuzatiladigan task sifatida rasmiylashtirish.
- Spring Cloud Data Flow'da task'lar zanjirini (job A tugagach job B) qurish.

**Ehtiyot bo'ling:** Task modeli doimiy ishlaydigan ilova uchun emas: `@EnableTask`ni web servisga qo'shib qo'ysangiz, ilova startup'dan keyin darhol tugash yozuvini yozib, kutilmagan holatga tushadi. Shuningdek `TASK_EXECUTION` jadvali vaqt o'tishi bilan o'sib boradi - retention/purge rejasi va DataSource izolyatsiyasini oldindan o'ylab qo'ying.

## 20.26 Solishtirish (reconciliation) joblari (Reconciliation Jobs)

**Tavsif:** Ikki yoki undan ortiq tizimdagi ma'lumot holatini davriy solishtirib, nomuvofiqliklarni (yetishmayotgan, ortiqcha, qiymati farq qiladigan yozuvlarni) topadi va avtomatik tuzatadi yoki hisobot qiladi. Eventual consistency sharoitida xabar yo'qolishi, retry dublikatlari va qo'lda tuzatishlar sababli drift muqarrar - reconciliation shu drift uchun "oxirgi himoya chizig'i". Odatda ikki tomonni kalit bo'yicha saralangan holda stream qilib, merge-join algoritmi bilan farqlar aniqlanadi.

**Spring'da qayerda uchraydi:** Spring Batch (`spring-boot-starter-batch`) bilan: `JobRepository`, `StepBuilder`, `ItemStreamReader` implementatsiyalari (`JdbcCursorItemReader`, `JdbcPagingItemReader`, `FlatFileItemReader`), ikki manbani birga o'qish uchun o'z `ItemReader` wrapper'i, natijalarni ikki yo'nalishga yozish uchun `ClassifierCompositeItemWriter`. Tashqi tizimni so'rash uchun `RestClient`/`WebClient`, tuzatish event'larini yuborish uchun `KafkaTemplate`. Nomuvofiqlik metrikalari uchun Micrometer `Counter`/`Gauge` va `JobExecutionListener` ichida alert yuborish; kichik hajmlarda `@Scheduled` + `JdbcTemplate` ham yetarli.

**Qo'llanish keyslari:**
- To'lov provayderi (PSP) hisobotini ichki buyurtma/tranzaksiya jadvali bilan har kuni solishtirish.
- Ombor tizimidagi qoldiq bilan e-commerce katalogidagi stock qiymatini tenglashtirish.
- Outbox jadvalida "yuborilgan" deb belgilangan, lekin broker'da yo'q bo'lgan event'larni topib qayta yuborish.
- Buxgalteriya ledger'i va bank ko'chirmasi o'rtasidagi farqlarni kunlik aniqlash.
- Microservice'lar o'rtasida replikatsiya qilingan read-model'ni manba jadvali bilan tekshirish.

**Ehtiyot bo'ling:** Tuzatishni ko'r-ko'rona avtomatlashtirish xavfli - ikki tomonning kesish vaqti (cut-off) bir xil bo'lmasa, "yetishmayotgan" deb topilgan yozuvlar aslida yo'lda bo'lgan tranzaksiyalar bo'lib chiqadi va job to'g'ri ma'lumotni buzadi. Avval faqat hisobot rejimida (dry-run) ishlatib, farq hajmi uchun chegara (threshold) qo'ying; chegaradan oshsa avtomatik tuzatishni to'xtatib, odamga eskalatsiya qiling.

## 20.27 Arxivlash va tozalash joblari (Archive / Purge Jobs)

**Tavsif:** Operatsion bazadagi eski ma'lumotni retention siyosatiga muvofiq arzon saqlash joyiga ko'chiradi yoki butunlay o'chiradi. Maqsad - jadval va indeks hajmini, shu orqali so'rov vaqtini va zaxira (backup) oynasini nazoratda tutish, hamda yuridik saqlash muddati talablariga rioya qilish. To'g'ri amalga oshirilganda ish kichik chunk'larga bo'linadi: har bir tranzaksiyada ma'lum sondagi qator ko'chiriladi/o'chiriladi va keyin pauza beriladi.

**Spring'da qayerda uchraydi:** Spring Batch step'i `JdbcPagingItemReader` + `JdbcBatchItemWriter` yoki `FlatFileItemWriter` (CSV/JSONL eksport) bilan; `chunk(1000, transactionManager)` va `taskExecutor` orqali throttling. Arxivni obyekt saqlashga yuborish uchun Spring Cloud AWS `S3Template`/`S3Client`, yoki `spring-integration-sftp`. Oddiy holatlar uchun `@Scheduled` + `JdbcTemplate.update()` ni `LIMIT` bilan tsiklda chaqirish; jadval partition'larini DB darajasida drop qilish (PostgreSQL/Oracle partitioning) eng tez variant. Soft delete uchun Hibernate 6 `@SoftDelete` (Spring Boot 3.3+ da mavjud), `@SQLRestriction` (6.3 dan, eski `@Where` o'rnida) va `@Filter`; `@Where` Hibernate 7.0 da olib tashlangan ([hibernate-orm 7.0.0, migration guide](https://github.com/hibernate/hibernate-orm/blob/7.0.0/migration-guide.adoc)).

**Qo'llanish keyslari:**
- 90 kundan oshgan audit log yozuvlarini S3'ga Parquet/CSV sifatida chiqarib, bazadan o'chirish.
- Yetkazib berilgan bildirishnoma (notification) jadvalini har kecha tozalash.
- GDPR talabiga ko'ra bekor qilingan akkauntlarning shaxsiy ma'lumotini belgilangan muddatdan keyin o'chirish.
- `TASK_EXECUTION`, `BATCH_STEP_EXECUTION_CONTEXT` kabi metadata jadvallarini qisqartirish.
- Vaqtinchalik fayl yuklash (upload staging) katalogini va unga mos DB yozuvlarini tozalash.

**Ehtiyot bo'ling:** Bitta katta `DELETE` operatsiyasi million qatorni bir tranzaksiyada o'chirib, lock eskalatsiyasi, replikatsiya lag'i va WAL/undo portlashiga olib keladi - har doim chunk bilan va past yuklama oynasida ishlang. O'chirishdan oldin arxiv muvaffaqiyatli yozilganini tasdiqlang (avval yoz, keyin o'chir), aks holda tiklab bo'lmaydigan ma'lumot yo'qotiladi; yuridik saqlash (legal hold) ostidagi yozuvlar uchun istisno filtri bo'lishi shart.

## 20.28 Batch oynasi va SLA (Batch Window & SLA)

**Tavsif:** Batch ishlari uchun ruxsat etilgan vaqt oynasi (masalan, 01:00-05:00) va har bir job uchun tugash muddati shartnoma sifatida belgilanadi, so'ng real bajarilish vaqti kuzatilib, oynadan chiqish xavfi oldindan aniqlanadi. Oyna ichida joblar o'zaro bog'liqlik (dependency) grafi bo'yicha tartiblanadi, kritik yo'l (critical path) hisoblanadi va kechikish signal beradi. Oynadan oshib ketgan job operatsion yuklamaga va mijoz SLA'siga ta'sir qilgani uchun uni to'xtatish yoki qisqartirilgan rejimda davom etish qoidalari ham qismi hisoblanadi.

**Spring'da qayerda uchraydi:** Spring Batch'da `JobExecutionListener`/`StepExecutionListener` bilan boshlanish-tugash vaqtini o'lchash, `JobExplorer` va `JobOperator` (`stop(executionId)`) bilan ishlayotgan execution'larni kuzatish va to'xtatish, `StepExecution#setTerminateOnly()` bilan muloyim uzish. Micrometer avtomatik `spring.batch.job` va `spring.batch.step` timer metrikalarini chiqaradi (tag'lar: `name`, `status`), ularni Prometheus alert'lari bilan bog'lash mumkin; `management.endpoint.health` va Actuator orqali holat ko'rsatiladi. Tashqi orkestratsiyada Spring Cloud Data Flow yoki Airflow/Control-M oynani va dependency'ni boshqaradi, Boot ilovasi esa faqat o'z SLA metrikasini e'lon qiladi.

**Qo'llanish keyslari:**
- Kunlik yopish (day-close) zanjiri ertalab 06:00 dagi filial ochilishiga qadar tugashi kerak bo'lgan bank tizimi.
- Hisob-faktura generatsiyasi mijoz portalida 08:00 da ko'rinishi shart bo'lgan telekom billing'i.
- Kechki ETL oynasida DWH yuklanishi tugamasa, ertalabki BI hisobotlarini eski ma'lumot bilan ko'rsatish qaroriga asos bo'lishi.
- Job o'rtacha davomiyligi oshib borayotganini trend sifatida kuzatib, hajm o'sishiga oldindan tayyorlanish.
- Oyna ichida bir vaqtda ishlaydigan joblar sonini cheklab, OLTP bazaga tushadigan yuklamani boshqarish.

**Ehtiyot bo'ling:** Faqat "job muvaffaqiyatli tugadi" signalini kuzatish yetarli emas - oynadan chiqqan, lekin "SUCCESS" bilan tugagan job SLA buzilishini yashiradi, shuning uchun davomiylik va tugash vaqti bo'yicha alohida alert kerak. Oyna yetmay qolganda birinchi reaksiya parallelizmni oshirish bo'lmasin: parallel step'lar bir xil DB'ga urilib umumiy throughput'ni pasaytirishi mumkin, avval kritik yo'lni va eng sekin step'ni o'lchang.

## 20.29 Idempotent batch (Idempotent Batch)

**Tavsif:** Job yoki uning bir qismi qayta ishga tushirilganda natija bir marta ishlagandagiday bo'lishini kafolatlaydi. Bu ikki mexanizmga tayanadi: bajarilgan ishni eslab qolish (qayerdan davom etish kerakligi) va yozish operatsiyalarining qayta bajarilsa ham holatni o'zgartirmasligi (upsert, natural key bo'yicha unikal cheklov, dedup jadvali). Idempotentlik bo'lmasa, restart yoki qisman xatolik dublikat to'lov, ikki marta yuborilgan email yoki buzilgan agregatlar bilan yakunlanadi.

**Spring'da qayerda uchraydi:** Spring Batch'ning `JobRepository` metadata'si job instance'ni `JobParameters` to'plami bilan identifikatsiya qiladi, shu sababli bir xil parametr bilan tugagan job qayta ishga tushmaydi (`JobInstanceAlreadyCompleteException`); yangi instance kerak bo'lganda `JobParametersIncrementer`/`RunIdIncrementer` ishlatiladi. Restart'da `StepExecution`ning `ExecutionContext`i (`ItemStream#update`) o'qish pozitsiyasini saqlaydi; `allowStartIfComplete(true)` va `startLimit` qayta ishlash siyosatini belgilaydi. Yozish tomonida `JdbcBatchItemWriter` bilan `INSERT ... ON CONFLICT DO UPDATE`, JPA'da `@Version` optimistic locking, Kafka tomonida `KafkaTemplate` + transactional producer yoki xabarga biznes kaliti qo'yib iste'molchida dedup qilish.

**Qo'llanish keyslari:**
- Yarim yo'lda node o'lgan import jobini xuddi shu faylni boshidan o'qimasdan davom ettirish.
- Hisob-kitob (settlement) jobini xatolikdan keyin qayta ishga tushirganda ikki marta pul o'tkazmaslik.
- Faylni hamkor ikki marta yuborganda (bir xil fayl nomi/hash) ikkinchisini e'tiborsiz qoldirish.
- Kunlik agregatni `MERGE`/upsert bilan qayta hisoblab, eski qiymat ustiga yozish.
- Bildirishnoma yuborish step'ida `notification_sent` dedup jadvali bilan takroriy email'ni to'sish.

**Ehtiyot bo'ling:** `ExecutionContext`ga tayangan restart faqat reader deterministik tartibda o'qiganda to'g'ri ishlaydi - `ORDER BY` bo'lmagan paging reader restart'da qatorlarni tashlab ketadi yoki takrorlaydi. Chunk ichidagi tashqi side-effect'lar (email, tashqi API chaqiruvi) DB tranzaksiyasiga kirmaydi, shuning uchun ularni alohida idempotentlik kaliti bilan himoyalang va "retry = xavfsiz" degan taxminni har bir writer uchun alohida tekshirib chiqing.

Mavzuning to'liq yozuvi [idempotency](07-api-dizayn-patternlari.md#79-idempotentlik-kaliti-idempotency-key) bo'limida; bu yerda faqat shu bo'limning nuqtai nazari.

## 20.30 Batch'da dead-letter boshqaruvi (Dead-Letter Handling in Batch)

**Tavsif:** Bitta buzuq yozuv butun jobni to'xtatib qo'yishining oldini oladi: qayta urinib bo'lmaydigan (non-transient) xatolikka uchragan element asosiy oqimdan chiqarilib, sababi bilan alohida "rad etilganlar" joyiga (error jadvali, reject fayli, DLQ topic) yoziladi, job esa qolgan ma'lumot bilan davom etadi. Keyin shu rad etilganlar alohida tahlil qilinadi, tuzatiladi va qayta ishlash jobi bilan oqimga qaytariladi. Bu xatolik tasnifiga tayanadi: transient xato uchun retry, doimiy xato uchun skip va dead-letter.

**Spring'da qayerda uchraydi:** Spring Batch step'ida `.faultTolerant()` bilan `retry(...)`/`retryLimit(...)`, `skip(...)`/`skipLimit(...)`, maxsus mantiq uchun `SkipPolicy`; rad etilganlarni yozib qolish uchun `SkipListener` (`onSkipInRead`, `onSkipInProcess`, `onSkipInWrite`) yoki `ClassifierCompositeItemWriter` bilan xato oqimini `JdbcBatchItemWriter`ga yo'naltirish. Backoff uchun Spring Retry (`RetryTemplate`, `BackOffPolicy`). Message-driven batch'da Spring for Apache Kafka'ning `DefaultErrorHandler` + `DeadLetterPublishingRecoverer` (`<topic>.DLT`) yoki Spring AMQP'da dead-letter exchange sozlamalari (`x-dead-letter-exchange`) shu patternning broker versiyasi.

```java
return new StepBuilder("importStep", jobRepository)
    .<Row, Row>chunk(500, txManager)
    .reader(reader).processor(processor).writer(writer)
    .faultTolerant()
    .retryLimit(3).retry(TransientDataAccessException.class)
    .skipLimit(200).skip(ValidationException.class)
    .listener(rejectRecordingSkipListener)
    .build();
```

**Qo'llanish keyslari:**
- Hamkor CSV faylidagi noto'g'ri formatlangan qatorlarni reject fayliga chiqarib, qolgan 99% ni yuklash.
- Validatsiyadan o'tmagan buyurtmalarni `import_rejects` jadvaliga sabab kodi bilan yozib, operator UI'da ko'rsatish.
- Tashqi servis 500 qaytarganda retry qilish, 400 qaytarganda esa darhol dead-letter'ga yuborish.
- Kafka'dan o'qiydigan batch consumer'da deserializatsiya xatosi bo'lgan xabarlarni DLT topic'ga ko'chirish.
- Tuzatilgan reject'larni qayta ishlash uchun alohida "replay" jobini ishga tushirish.

**Ehtiyot bo'ling:** `skipLimit`ni juda katta (yoki `Integer.MAX_VALUE`) qilib qo'yish eng xavfli antipattern - manba tizimida global buzilish yuz berganda job "muvaffaqiyatli" tugab, ma'lumotning yarmi jimgina yo'qoladi; limitni biznes uchun qabul qilinadigan darajada past tutib, oshsa job'ni fail qildiring. Shuningdek `skip` bilan birga tranzaksiya rollback va chunk'ni element-element qayta ishlash yuz beradi, bu performansni sezilarli pasaytiradi, va dead-letter store'ni monitoring qilmasangiz u hech kim qaramaydigan "ma'lumot qabristoni"ga aylanadi.

## 20.31 Amalda qo'llash

- [ ] Har bir batch job uchun chunk hajmi, commit chegarasi va qayta ishga tushirish xatti-harakatini yozib qo'ying.
- [ ] Job larning takrorlanishiga qarshi himoyasi borligini tekshiring: ikki marta ishga tushsa nima bo'ladi.
- [ ] `@Scheduled` metodlarni sanab chiqing va ko'p nusxada ishlaydigan ilovada ShedLock yoki shunga o'xshash qulf borligini tasdiqlang.
- [ ] Batch job larning ishlash vaqtini o'lchab, reliz oynasi va kunlik yuk cho'qqisi bilan kesishmasligini tekshiring.
- [ ] Xato bo'lgan yozuvlar uchun skip va retry siyosatini yozib qo'ying; jimgina o'tkazib yuborilgan yozuvlar kuzatilishi kerak.
- [ ] Katta hajmli job larni partitioning bilan bo'lish foydasini o'lchang va natijani yozib qo'ying.
- [ ] Har bir job uchun metrika chiqarilayotganini tasdiqlang: ishlash vaqti, ishlangan yozuv soni, xato soni.
- [ ] Job to'xtatilganda yoki pod o'chirilganda holat qanday saqlanishini sinab ko'rib, natijani hujjatlashtiring.

---

[&larr; 19. Reactive patternlar](19-reactive-patternlar.md) · [Mundarija](README.md) · [21. Observability patternlari &rarr;](21-observability-patternlari.md)
