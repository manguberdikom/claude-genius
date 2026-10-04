<!-- doc: patterns | chapter: 10 | part:  -->

[Java Spring arxitektori bilishi kerak bo'lgan barcha dizayn patternlar](../../README.md) / [Dizayn patternlar](README.md)

# 10. Ma'lumotlarni boshqarish va taqsimlash patternlari (Data Management & Distribution Patterns)

<details>
<summary>Bu bo'limdagi 31 bo'lim</summary>

- [10.1 Yumshoq o'chirish (Soft Delete)](#101-yumshoq-ochirish-soft-delete)
- [10.2 Audit izi / Auditlash (Audit Trail / Auditing)](#102-audit-izi--auditlash-audit-trail--auditing)
- [10.3 Versiyalangan / Temporal / Bitemporal ma'lumot (Versioned / Temporal / Bitemporal data)](#103-versiyalangan--temporal--bitemporal-malumot-versioned--temporal--bitemporal-data)
- [10.4 Ma'lumotlar bazasi migratsiyasi (Database Migration)](#104-malumotlar-bazasi-migratsiyasi-database-migration)
- [10.5 Keng aytib-toraytirish schema migratsiyasi (Expand/Contract schema migration)](#105-keng-aytib-toraytirish-schema-migratsiyasi-expandcontract-schema-migration)
- [10.6 Ko'p-tenantlilik: umumiy schema, diskriminator (Multi-tenancy: shared schema discriminator)](#106-kop-tenantlilik-umumiy-schema-diskriminator-multi-tenancy-shared-schema-discriminator)
- [10.7 Ko'p-tenantlilik: tenant boshiga schema (Multi-tenancy: schema per tenant)](#107-kop-tenantlilik-tenant-boshiga-schema-multi-tenancy-schema-per-tenant)
- [10.8 Ko'p-tenantlilik: tenant boshiga baza (Multi-tenancy: database per tenant)](#108-kop-tenantlilik-tenant-boshiga-baza-multi-tenancy-database-per-tenant)
- [10.9 Shardlash / Bo'laklash (Sharding / Partitioning)](#109-shardlash--bolaklash-sharding--partitioning)
- [10.10 Replikatsiya va read replica'ga yo'naltirish (Replication & Read Replica routing)](#1010-replikatsiya-va-read-replicaga-yonaltirish-replication--read-replica-routing)
- [10.11 Poliglot persistence (Polyglot Persistence)](#1011-poliglot-persistence-polyglot-persistence)
- [10.12 Har bir servis uchun alohida ma'lumotlar bazasi (Database per Service)](#1012-har-bir-servis-uchun-alohida-malumotlar-bazasi-database-per-service)
- [10.13 Umumiy ma'lumotlar bazasi (Shared Database) - anti-pattern](#1013-umumiy-malumotlar-bazasi-shared-database---anti-pattern)
- [10.14 Tranzaksion Outbox (Transactional Outbox)](#1014-tranzaksion-outbox-transactional-outbox)
- [10.15 Inbox (Idempotent Receiver store)](#1015-inbox-idempotent-receiver-store)
- [10.16 Ma'lumot o'zgarishini ushlash (Change Data Capture / Debezium)](#1016-malumot-ozgarishini-ushlash-change-data-capture--debezium)
- [10.17 Snapshot (Snapshot)](#1017-snapshot-snapshot)
- [10.18 Materiallashtirilgan ko'rinish (Materialized View)](#1018-materiallashtirilgan-korinish-materialized-view)
- [10.19 Indeks jadvali (Index Table)](#1019-indeks-jadvali-index-table)
- [10.20 Ommaviy / paketli kiritish (Bulk / Batch insert)](#1020-ommaviy--paketli-kiritish-bulk--batch-insert)
- [10.21 Ikki fazali commit / XA (Two-Phase Commit / XA)](#1021-ikki-fazali-commit--xa-two-phase-commit--xa)
- [10.22 Try-Confirm-Cancel (TCC)](#1022-try-confirm-cancel-tcc)
- [10.23 Kompensatsiyalovchi tranzaksiya (Compensating Transaction)](#1023-kompensatsiyalovchi-tranzaksiya-compensating-transaction)
- [10.24 Event Sourcing ombori (Event Sourcing Store)](#1024-event-sourcing-ombori-event-sourcing-store)
- [10.25 Arxivlash / tozalash (Archive / Purge)](#1025-arxivlash--tozalash-archive--purge)
- [10.26 Ma'lumotlarni saqlash muddati (Data Retention)](#1026-malumotlarni-saqlash-muddati-data-retention)
- [10.27 Diskda va maydon darajasida shifrlash (Encryption at Rest / Field-Level Encryption)](#1027-diskda-va-maydon-darajasida-shifrlash-encryption-at-rest--field-level-encryption)
- [10.28 O'qish/yozishni ajratish (Read/Write Splitting)](#1028-oqishyozishni-ajratish-readwrite-splitting)
- [10.29 Taqsimlangan lock (Distributed Lock - Redis, ShedLock, Database)](#1029-taqsimlangan-lock-distributed-lock---redis-shedlock-database)
- [10.30 Idempotentlik ombori (Idempotency Store)](#1030-idempotentlik-ombori-idempotency-store)
- [10.31 Dual Write muammosi (Dual Write Problem)](#1031-dual-write-muammosi-dual-write-problem)

</details>



Ma'lumotlarni boshqarish va taqsimlash patternlari ma'lumotning hayot davri - yaratilishi, o'zgarishi, o'chirilishi, tarixi va jismoniy joylashuvi - qanday boshqarilishini belgilaydi. Bu kategoriya arxitektor uchun eng "qaytarib bo'lmas" qarorlar to'plami: kod qatlamini keyin refactor qilish mumkin, lekin yuzlab million qatorli jadvalning schema'si, tenant izolyatsiya modeli yoki shard kaliti bir marta tanlanadi va yillar davomida butun tizimni cheklab turadi. Shuningdek bu patternlar bevosita biznes talablariga - audit va compliance (GDPR, SOX), zero-downtime deploy, SLA va o'qish yuklamasini masshtablashga - tegib ketadi. Shu sababli senior injener bu patternlarning nafaqat "qanday" ishlashini, balki qaysi birining qaytarilish narxi qanchalik qimmat bo'lishini ham bilishi kerak.

## 10.1 Yumshoq o'chirish (Soft Delete)

**Tavsif:** Yozuvni jadvaldan jismoniy `DELETE` qilish o'rniga uni `deleted`/`deleted_at` kabi flag bilan belgilab, barcha o'qish so'rovlarida filtrlab chiqarib tashlash. Bu ma'lumotni tiklash imkonini beradi, foreign key'lar va tarixiy hisobotlar buzilmaydi, "kim nimani o'chirdi" savoliga javob qoladi. Buning narxi - har bir so'rovga qo'shimcha predikat va "o'lik" qatorlarning to'planishi.

**Spring'da qayerda uchraydi:** Hibernate 6.4+ dagi `@SoftDelete` annotatsiyasi (entity yoki field ustida, `SoftDeleteType.DELETED`/`ACTIVE`, `converter` bilan), yoki klassik yondashuv - `@SQLDelete(sql = "update ... set deleted = true where id = ?")` plus `@SQLRestriction("deleted = false")` (ilgari `@Where`, Hibernate 6.3'dan deprecated). Spring Data JPA tomonida `deleteById` ni override qilish yoki repository'da `findAllByDeletedFalse` / `@Query` bilan aniq filtr. Multi-tenant yoki global filtr kerak bo'lsa Hibernate `@FilterDef`/`@Filter` va `Session#enableFilter` ishlatiladi. Spring Modulith / event'lar bilan birga `ApplicationEventPublisher` orqali `EntityDeletedEvent` chiqarish keng tarqalgan.

**Qo'llanish keyslari:**
- Foydalanuvchi akkauntini "deaktivatsiya" qilish, 30 kunlik tiklash oynasi bilan.
- Hujjat yoki buyurtmani savatchadan olib tashlab, keyin "undo" tugmasini berish.
- Moliyaviy tranzaksiyalarni hech qachon jismoniy o'chirmaslik (audit talabi).
- CMS'da kontentni arxivlash, lekin eski URL'larga ishlovchi redirect'ni saqlash.
- Katalog mahsulotini sotuvdan chiqarib, eski buyurtmalardagi havolani buzmaslik.

**Ehtiyot bo'ling:** Unique index'lar soft delete bilan ziddiyatga kiradi - o'chirilgan `email` yangi ro'yxatdan o'tishni bloklaydi, shuning uchun partial/filtered index yoki `deleted_at` ni kalitga qo'shish kerak. Native query, `JOIN`, reporting va `COUNT` joylarida filtr esdan chiqsa "o'chirilgan" ma'lumot ko'rinib qoladi; GDPR "o'chirish huquqi" talab qilsa soft delete yetarli emas - haqiqiy anonimlashtirish yoki hard delete kerak.

## 10.2 Audit izi / Auditlash (Audit Trail / Auditing)

**Tavsif:** Har bir o'zgarish uchun kim, qachon va nimani o'zgartirganini avtomatik qayd qilish. Eng oddiy darajada bu `created_by`/`created_at`/`modified_by`/`modified_at` ustunlari, kuchliroq darajada - har bir `UPDATE` uchun to'liq revision jadvali. Muammosi: biznes kodini audit logikasi bilan ifloslantirmaslik, shuning uchun u framework darajasidagi callback'lar orqali amalga oshiriladi.

**Spring'da qayerda uchraydi:** Spring Data JPA auditing - `@EnableJpaAuditing`, entity ustida `@EntityListeners(AuditingEntityListener.class)`, maydonlarda `@CreatedDate`, `@LastModifiedDate`, `@CreatedBy`, `@LastModifiedBy`, hamda `AuditorAware<T>` bean'i (odatda `SecurityContextHolder` dan foydalanuvchini oladi). Mongo uchun `@EnableMongoAuditing`. To'liq revision tarixi kerak bo'lsa - Hibernate Envers: `@Audited`, `@AuditTable`, `_AUD` jadvallari va `AuditReader`/`AuditQuery` orqali so'rov; Spring Data Envers `RevisionRepository<T, ID, N>` interfeysini beradi (`findRevisions(id)`). Qo'shimcha: `@Version` optimistic lock, Spring Security'da `AuthenticationSuccessEvent`/`AuditEventRepository` (Actuator `/actuator/auditevents`).

**Qo'llanish keyslari:**
- Bank yoki fintech'da har bir balans o'zgarishining revision tarixini saqlash.
- Shartnoma hujjatining har bir tahririni kim kiritganini ko'rsatuvchi "history" ekrani.
- SOX/ISO auditiga rol va ruxsat o'zgarishlari jurnalini topshirish.
- Incident tahlilida "bu narx qachon va kim tomonidan o'zgartirilgan" savoliga javob berish.
- Tibbiy yozuvlarga kirish va o'zgartirishni qonun talabiga ko'ra qayd etish.

**Ehtiyot bo'ling:** Envers yozish hajmini va jadvallar sonini keskin oshiradi - har bir `UPDATE` ikkinchi `INSERT` keltiradi, shuning uchun uni hamma entity'ga emas, faqat biznesga muhim bo'lganlarga qo'llang va retention/arxivlash siyosatini oldindan rejalashtiring. `AuditorAware` async thread yoki batch job ichida bo'sh qaytadi (`SecurityContext` propagate bo'lmaydi), shuningdek audit jadvallariga parol, token yoki PII tushib qolmasligini nazorat qilish kerak.

## 10.3 Versiyalangan / Temporal / Bitemporal ma'lumot (Versioned / Temporal / Bitemporal data)

**Tavsif:** Yozuvning joriy holatini emas, vaqt bo'yicha o'zgarish ketma-ketligini saqlash: har bir versiyaning amal qilish oynasi (`valid_from`, `valid_to`) mavjud. Bitemporal modelda ikki vaqt o'qi bo'ladi - *valid time* (fakt real dunyoda qachon haqiqiy bo'lgan) va *transaction time* (tizim bu haqda qachon bilgan), bu esa "o'tgan oyda biz nimaga ishonganmiz" degan savolga ham javob berish imkonini beradi. Natijada "as-of" so'rovlari, retroaktiv tuzatishlar va reproducible hisobotlar mumkin bo'ladi.

**Spring'da qayerda uchraydi:** Toza JPA'da bu odatda qo'lda modellanadi: `@Embeddable` sifatida `Period`/`ValidityRange` va repository'da `@Query("... where :at between v.validFrom and v.validTo")`; PostgreSQL'da `tstzrange` + `EXCLUDE USING gist` constraint (Hibernate'da custom `UserType`/`@JdbcTypeCode`). Baza darajasida SQL:2011 system-versioned jadvallar (MariaDB `WITH SYSTEM VERSIONING`, SQL Server temporal tables) ishlatilsa, Hibernate `@Subselect` yoki native query orqali `FOR SYSTEM_TIME AS OF` o'qiladi. Hibernate Envers ham cheklangan "as-of" rejimini beradi (`AuditReader#find(Class, id, revision)` yoki `AuditQuery` + `AuditEntity.revisionProperty("timestamp")`). Event-sourcing yondashuvi uchun Axon Framework yoki Spring Modulith event publication registry'si keng qo'llanadi. Java tomonida `java.time` (`Instant`, `LocalDate`, `ZonedDateTime`) va Java 17+ `record` lar immutable versiya obyektlari uchun tabiiy tanlov.

**Qo'llanish keyslari:**
- Sug'urta polisining har bir endorsement'i va uning amal qilish davri.
- Narx va tarif jadvallari: kelasi oydan kuchga kiradigan narxni oldindan kiritish.
- HR tizimida lavozim va maosh tarixi, retroaktiv oshirish bilan.
- Moliyaviy hisobotni "1-iyul holatiga ko'ra" qayta ishlab chiqarish (restatement).
- Reference data (valyuta kursi, soliq stavkasi) ning tarixiy qiymatlari bo'yicha qayta hisoblash.

**Ehtiyot bo'ling:** Temporal model so'rovlar va unique constraint'larni ancha murakkablashtiradi - oynalar kesishib ketmasligini baza darajasida kafolatlash kerak, aks holda bitta sanada ikkita "joriy" versiya paydo bo'ladi. Bitemporal'ni haqiqiy ehtiyoj bo'lmasa tanlamang: ko'p holatda oddiy audit trail yetarli, bitemporal esa butun domen modeli va UI'ni og'irlashtiradi.

## 10.4 Ma'lumotlar bazasi migratsiyasi (Database Migration)

**Tavsif:** Schema o'zgarishlarini versiyalangan, tartiblangan va takrorlanadigan skriptlar ko'rinishida kodga joylashtirish, so'ng ilova ishga tushganda yoki CI/CD bosqichida avtomatik qo'llash. Har bir migratsiya bir marta bajariladi va baza ichidagi maxsus jadvalda (checksum bilan) qayd etiladi, shuning uchun har qanday muhitda schema holati bir xil va kuzatiladigan bo'ladi.

**Spring'da qayerda uchraydi:** Spring Boot 3.x/4.x Flyway va Liquibase'ni avtomatik konfiguratsiya qiladi. Flyway: `org.flywaydb:flyway-core` (PostgreSQL uchun qo'shimcha `flyway-database-postgresql`), skriptlar `classpath:db/migration/V1__init.sql`, `spring.flyway.*` xossalari, `FlywayMigrationStrategy` bean'i orqali boshqarish. Liquibase: `spring.liquibase.change-log=classpath:db/changelog/db.changelog-master.yaml`, XML/YAML/SQL changeset'lar, `databaseChangeLog` jadvali. Ikkalasi ham `DataSource` tayyor bo'lgandan keyin, JPA `EntityManagerFactory` dan oldin ishlaydi. Testda Testcontainers + `@Sql`, `@DynamicPropertySource` bilan birga ishlatiladi; `spring.jpa.hibernate.ddl-auto` esa prod'da `none`/`validate` bo'lishi kerak.

**Qo'llanish keyslari:**
- Yangi jadval, ustun yoki index'ni barcha muhitlarga (dev → stage → prod) bir xil tartibda tarqatish.
- CI'da har bir PR uchun bo'sh bazani noldan qurib, migratsiyalarni Testcontainers ustida sinash.
- Reference/lookup ma'lumotlarini (status kodlari, davlatlar) seed qilish.
- Kubernetes'da migratsiyani alohida init-container yoki Job sifatida ishga tushirish.
- Legacy bazani birinchi marta Flyway nazoratiga olish (`baseline-on-migrate`).

**Ehtiyot bo'ling:** Allaqachon qo'llanilgan migratsiya faylini tahrirlash checksum xatosiga olib keladi - tuzatish uchun yangi migratsiya yozing, eskisini o'zgartirmang. Bir nechta pod bir vaqtda ishga tushsa migratsiya race'i yuz berishi mumkin (Flyway lock ko'p bazalarda yordam beradi, lekin MySQL DDL transactional emas), katta jadvalga `ALTER` esa uzoq lock olib ilovani to'xtatishi mumkin - bunday o'zgarishlarni expand/contract bilan bosqichlang.

## 10.5 Keng aytib-toraytirish schema migratsiyasi (Expand/Contract schema migration)

**Tavsif:** Buzadigan schema o'zgarishini uch bosqichga bo'lish: *expand* - yangi strukturani qo'shish (eski bilan birga, backward compatible), *migrate* - ma'lumotni ko'chirish va kodni ikki tomonga yozishga o'tkazish, *contract* - barcha instance'lar yangilangandan keyin eski strukturani olib tashlash. Bu rolling deploy va blue-green releasda eski va yangi kod versiyalari bir vaqtda ishlashiga imkon beradi, ya'ni zero-downtime migratsiyani ta'minlaydi.

**Spring'da qayerda uchraydi:** Ketma-ket Flyway/Liquibase migratsiyalari (`V12__add_full_name.sql` → `V13__backfill_full_name.sql` → `V20__drop_first_last_name.sql`) plus ilova kodi tomonida vaqtincha ikkala maydonni yozish. JPA tomonida yangi ustunni `nullable = true` qilib qo'shish, eski maydonni `@Deprecated` yoki `insertable = false, updatable = false` bilan belgilash, keyin olib tashlash. Backfill uchun Spring Batch (`Step`, `JpaPagingItemReader`, chunk-oriented processing) yoki `JdbcTemplate` bilan batch update. Feature flag sifatida `@ConditionalOnProperty`, Spring Cloud Config yoki Togglz; API darajasida mos pattern - Spring MVC'da versiyalangan endpoint'lar va Spring Boot 4 / Spring Framework 7 dagi API versioning (`@RequestMapping(version = "1.1")`). Kontrakt mosligini Spring Cloud Contract bilan tekshirish mumkin.

```java
@Entity class Customer {
  @Deprecated @Column(name = "first_name") String firstName; // contract bosqichida o'chadi
  @Column(name = "full_name") String fullName;               // expand bosqichida qo'shildi
  void setFullName(String v) { this.fullName = v; this.firstName = v.split(" ")[0]; }
}
```

**Qo'llanish keyslari:**
- Ustun nomini yoki tipini (`varchar` → `uuid`) ishlab turgan tizimda almashtirish.
- `NOT NULL` constraint'ni avval default qiymat va backfill bilan bosqichma-bosqich joriy etish.
- Bitta jadvalni ikkiga ajratish (normalizatsiya) yoki monolitdan microservice'ga ma'lumotni ko'chirish.
- Kafka yoki REST kontraktidagi maydonni tolerant reader orqali olib tashlash.
- Yuqori yuklamali jadvalga yangi index'ni `CREATE INDEX CONCURRENTLY` bilan qo'shish.

**Ehtiyot bo'ling:** Eng ko'p uchraydigan xato - *contract* bosqichini unutish: vaqtincha dual-write kodi va o'lik ustunlar yillar davomida qolib ketadi, shuning uchun uni darhol backlog'ga aniq relizga bog'lab qo'ying. Shuningdek contract'ni barcha eski pod'lar va eski consumer'lar o'chishidan oldin bajarish mumkin emas - rollback oynasini ham hisobga oling, aks holda orqaga qaytarish bazani buzadi.

## 10.6 Ko'p-tenantlilik: umumiy schema, diskriminator (Multi-tenancy: shared schema discriminator)

**Tavsif:** Barcha tenant'lar bitta baza va bitta schema'da yashaydi, har bir qatorda `tenant_id` ustuni bor va barcha so'rovlar shu ustun bo'yicha majburiy filtrlanadi. Bu eng arzon va eng oson masshtablanadigan model (minglab kichik tenant uchun ideal), lekin izolyatsiya butunlay ilova va baza qoidalariga bog'liq bo'lib qoladi.

**Spring'da qayerda uchraydi:** Hibernate 6.x: `@TenantId` annotatsiyasi entity maydonida plus `CurrentTenantIdentifierResolver` bean'i - Hibernate o'qishda filtrni, yozishda tenant qiymatini o'zi qo'yadi. Alternativa - Hibernate `@FilterDef`/`@Filter` va har bir session'da `enableFilter`. Tenant kontekstini olish uchun `OncePerRequestFilter` yoki Spring MVC `HandlerInterceptor` + `ThreadLocal` holder, reactive stack'da `Context`/`ContextSnapshot`; `@Async` va Spring Batch ichida kontekstni `TaskDecorator` bilan propagate qilish kerak. Baza darajasidagi himoya uchun PostgreSQL Row Level Security + `SET LOCAL app.tenant_id` ni `DataSource` connection prepare qiluvchi proxy'da o'rnatish. Spring Security'da tenant'ni JWT claim'dan (`JwtAuthenticationConverter`) olish keng tarqalgan.

**Qo'llanish keyslari:**
- Freemium SaaS: o'n minglab kichik tenant, tenant boshiga arzon narx.
- Bir xil schema va bir xil reliz sikli hamma mijoz uchun yetarli bo'lgan B2B SaaS.
- Barcha tenant'lar bo'ylab agregat analitika va product metrics hisoblash.
- Tenant'ni darhol, DDL'siz provision qilish (faqat bitta qator qo'shish).
- Connection pool va cache'ni iqtisod qilish kerak bo'lgan resurs-cheklangan muhit.

**Ehtiyot bo'ling:** Bitta unutilgan `WHERE tenant_id = ?` - ayniqsa native query, reporting yoki yangi repository metodida - tenant'lar orasida ma'lumot oqishiga olib keladi; shuning uchun filtrni ilovaga emas, Hibernate `@TenantId` va RLS kabi "default on" mexanizmlarga tayanib qo'ying. Shuningdek "shovqinli qo'shni" (bitta yirik tenant butun bazani sekinlashtirishi) va tenant'ni alohida eksport/o'chirish (GDPR) qiyinligi bu modelning doimiy narxi.

## 10.7 Ko'p-tenantlilik: tenant boshiga schema (Multi-tenancy: schema per tenant)

**Tavsif:** Bitta baza instance'i ichida har bir tenant uchun alohida schema yaratiladi; so'rovlar bir xil, faqat ulanishning joriy schema'si almashtiriladi. Bu izolyatsiya va xarajat o'rtasidagi o'rta yo'l: ma'lumot fizik ajratilgan, backup va o'chirish schema darajasida bajariladi, lekin baza resurslari hamon umumiy.

**Spring'da qayerda uchraydi:** Hibernate multi-tenancy: `hibernate.multiTenancy=SCHEMA`, `MultiTenantConnectionProvider` (connection olingach `SET search_path TO tenant_x` yoki `USE schema` bajaradi) va `CurrentTenantIdentifierResolver`; Spring Boot'da bu bean'lar `HibernatePropertiesCustomizer` orqali ulanadi. Spring Boot 3.x/4.x'da `LocalContainerEntityManagerFactoryBean` ni qo'lda sozlash ko'p uchraydi. Migratsiya tomonida Flyway'ni har bir schema uchun alohida ishga tushirish (`Flyway.configure().schemas(tenant).load().migrate()`) yoki Liquibase `defaultSchemaName` bilan sikl ichida chaqirish. Tenant provisioning - `JdbcTemplate` bilan `CREATE SCHEMA` plus migratsiya; cache tomonida tenant-aware kalit strategiyasi (`CacheResolver` yoki `KeyGenerator`) kerak.

**Qo'llanish keyslari:**
- O'rta hajmdagi B2B SaaS: yuzlab tenant, har biri uchun kuchli izolyatsiya talabi.
- Mijozga "sizning ma'lumotingiz alohida ajratilgan" degan compliance kafolatini berish.
- Bitta tenant'ni to'liq eksport qilish yoki o'chirish (`DROP SCHEMA`) talabi.
- Pilot mijozga vaqtincha boshqa schema versiyasida yangi funksiyani sinab ko'rish.
- Tenant'ni keyinchalik alohida bazaga ko'chirishga tayyor arxitektura qurish.

**Ehtiyot bo'ling:** Schema soni o'sgach migratsiya vaqti chiziqli oshadi va bir nechta schema yarim migratsiya holatida qolib ketishi mumkin - tenant provisioning va migratsiyani idempotent, qayta ishga tushirilishi mumkin qilib yozing. Connection pool ham diqqatli bo'lishni talab qiladi: pool'ga qaytarilgan connection'da `search_path` tozalanmasa, keyingi so'rov boshqa tenant schema'siga tushib qolishi mumkin.

## 10.8 Ko'p-tenantlilik: tenant boshiga baza (Multi-tenancy: database per tenant)

**Tavsif:** Har bir tenant butunlay alohida ma'lumotlar bazasiga (ba'zan alohida serverga) ega bo'ladi, ilova esa so'rov kontekstiga qarab mos `DataSource` ni tanlaydi. Bu eng kuchli izolyatsiya, per-tenant backup, SLA va hatto turli geografik regionlarga joylash imkonini beradi; narxi - infratuzilma xarajati va operatsion murakkablik.

**Spring'da qayerda uchraydi:** `AbstractRoutingDataSource` ni extend qilib `determineCurrentLookupKey()` da tenant ID qaytarish (eng oddiy yo'l), yoki Hibernate `hibernate.multiTenancy=DATABASE` + `MultiTenantConnectionProvider` bilan tenant boshiga HikariCP pool'lari. Tenant → ulanish ma'lumotlari ro'yxati odatda alohida "master"/catalog bazada saqlanadi va `DataSourceBuilder` orqali dinamik yaratiladi; sirlar uchun Spring Cloud Vault yoki AWS Secrets Manager. Tranzaksiyalar uchun har bir `DataSource` ga alohida `PlatformTransactionManager`/`EntityManagerFactory`, yoki routing yondashuvida bitta `JpaTransactionManager`. Migratsiya - tenant ro'yxati bo'ylab Flyway/Liquibase'ni programmatik aylantirish, ko'pincha alohida admin endpoint yoki Spring Batch job orqali.

**Qo'llanish keyslari:**
- Enterprise mijozlar: kam sonli, yirik, shartnomada izolyatsiya talab qilinadigan tenant'lar.
- Ma'lumotni hududiy saqlash talabi (EU mijozi ma'lumoti faqat EU regionida).
- Bank/sog'liq sektorida regulator talab qilgan to'liq fizik ajratish.
- Tenant boshiga alohida backup/restore va point-in-time recovery kafolati.
- "Shovqinli qo'shni" muammosini butunlay yo'q qilish va per-tenant resurs kvotasi berish.

**Ehtiyot bo'ling:** Tenant soni oshgani sari connection pool'lar ko'payib, ilova xotirasi va baza connection limiti tez tugaydi - pool'ni kichik qilib, foydalanilmagan tenant pool'larini lazy yaratib va idle'da yopib boring. Bu modelda cross-tenant hisobot, global migratsiya va deploy koordinatsiyasi sezilarli darajada qimmatlashadi, shuning uchun uni faqat haqiqiy compliance yoki yirik tenant talabi bo'lganda tanlang.

## 10.9 Shardlash / Bo'laklash (Sharding / Partitioning)

**Tavsif:** Jadval yoki butun dataset'ni kalit bo'yicha bir nechta bo'lakka ajratish: *partitioning* bitta baza ichida (range, list, hash), *sharding* esa turli serverlar bo'ylab. Maqsad - jadval hajmi, yozish IOPS'i yoki index kattaligi bitta node imkoniyatidan oshganda horizontal masshtablash va saqlashni boshqarish (eski partition'ni arzon diskka chiqarish yoki `DROP` qilish).

**Spring'da qayerda uchraydi:** Partitioning asosan baza darajasida (PostgreSQL `PARTITION BY RANGE`, declarative partitioning) Flyway migratsiyalari orqali amalga oshiriladi va ilovada shunchaki `WHERE` ga partition key qo'shiladi (`@Query` da `createdAt` oynasi). Sharding tomonida: `AbstractRoutingDataSource` bilan oddiy shard routing, Apache ShardingSphere-JDBC (`spring-boot-starter`, `ShardingSphereDataSource` ni `DataSource` sifatida ulash, sharding va read/write-split qoidalari YAML'da), yoki Vitess/Citus kabi proxy'lar - bu holda Spring tomoni o'zgarmaydi. Spring Data MongoDB va Cassandra uchun shard/partition kaliti model darajasida: `@ShardKey`, Cassandra'da `@PrimaryKeyClass` ichidagi `@PrimaryKeyColumn(type = PARTITIONED)`. Kafka tomonida partition kaliti - `KafkaTemplate#send(topic, key, value)` bilan bir xil mantiq.

**Qo'llanish keyslari:**
- Milliardlab qatorli event/telemetry jadvalini oy bo'yicha range partition qilib eskisini o'chirish.
- Marketplace'da buyurtmalarni `tenant_id` yoki `customer_id` hash'i bo'yicha shardlash.
- Vaqt seriyali metrikalarni retention siyosati bilan boshqarish (`DROP PARTITION` sekundlarda).
- Geo-shardlash: foydalanuvchini o'z regionidagi shard'ga yo'naltirib latency'ni kamaytirish.
- Yozish yuklamasi bitta master'ga sig'maydigan yuqori-TPS tizimlarini masshtablash.

**Ehtiyot bo'ling:** Noto'g'ri tanlangan shard kaliti eng qimmat xato - u notekis taqsimlanish (hot shard) yoki har bir so'rovda scatter-gather'ga olib keladi, resharding esa katta loyihaga aylanadi, shuning uchun kalitni asosiy so'rov pattern'iga qarab tanlang. Shardlangan tizimda cross-shard `JOIN`, global unique ID (UUIDv7/Snowflake kerak bo'ladi) va distributed tranzaksiya qimmat - shardlashni faqat replica va partitioning yetmaganda, eng oxirgi chora sifatida qo'llang.

## 10.10 Replikatsiya va read replica'ga yo'naltirish (Replication & Read Replica routing)

**Tavsif:** Yozish operatsiyalari primary (master) bazaga, o'qish operatsiyalari esa bir yoki bir nechta replica'ga yo'naltiriladi; shu bilan o'qish yuklamasi gorizontal masshtablanadi va primary bo'shaydi. Routing tranzaksiyaning read-only ekanligiga qarab avtomatik bajarilishi mumkin, lekin replikatsiya lag'i tufayli "o'zi yozgan ma'lumotni darhol o'qish" kafolati buziladi.

**Spring'da qayerda uchraydi:** Klassik yechim - `AbstractRoutingDataSource` ni extend qilib `TransactionSynchronizationManager.isCurrentTransactionReadOnly()` natijasiga qarab `"replica"` yoki `"primary"` kalitini qaytarish, va bu routing `DataSource` ni `LazyConnectionDataSourceProxy` ichiga o'rash (aks holda connection tranzaksiya read-only bayrog'i o'rnatilishidan oldin olinadi). Service metodlarida `@Transactional(readOnly = true)` shu bilan routing hint'iga aylanadi. Alternativalar: ShardingSphere-JDBC read/write splitting, AWS Aurora reader endpoint'i, PgBouncer/ProxySQL yoki `spring.datasource.*` ostida ikkita alohida `DataSource` va ikkita `EntityManagerFactory`.

```java
public class RoutingDataSource extends AbstractRoutingDataSource {
  @Override protected Object determineCurrentLookupKey() {
    return TransactionSynchronizationManager.isCurrentTransactionReadOnly() ? "replica" : "primary";
  }
}
```

**Qo'llanish keyslari:**
- Og'ir reporting va dashboard so'rovlarini replica'ga chiqarib primary'ni himoya qilish.
- Katalog va kontent sahifalari kabi o'qish-dominant trafikni masshtablash.
- Analitika yoki BI ETL job'larini faqat replica'dan o'qishga majburlash.
- Geografik replica'lar bilan mahalliy o'qish latency'sini kamaytirish.
- Primary'ni maintenance yoki failover paytida degradatsiya qilib o'qishni davom ettirish.

**Ehtiyot bo'ling:** Replikatsiya lag'i sababli yozgandan keyin darhol o'qish eski ma'lumot qaytarishi mumkin - "read-your-writes" muhim bo'lgan flow'larni (to'lovdan keyingi ekran, forma saqlanishi) majburan primary'ga yo'naltiring yoki sticky session qo'llang. Yana bir tuzoq: `readOnly = true` ni oqibatini o'ylamay hamma joyga qo'yish - ichida yozuv bo'lgan metod silent ravishda xato beradi yoki noto'g'ri node'ga tushadi, `LazyConnectionDataSourceProxy` ni esdan chiqarish ham routingni butunlay ishlamas qiladi.

## 10.11 Poliglot persistence (Polyglot Persistence)

**Tavsif:** Bitta tizim ichida har bir ma'lumot turi uchun unga eng mos saqlash texnologiyasini tanlash: tranzaksion yadro uchun relyatsion baza, qidiruv uchun Elasticsearch/OpenSearch, cache va session uchun Redis, hujjatlar uchun MongoDB, graf aloqalar uchun Neo4j, event log uchun Kafka. Bu har bir use-case'da optimal unumdorlik beradi, lekin ma'lumotni sinxronlashtirish va operatsion murakkablikni tizimga olib kiradi.

**Spring'da qayerda uchraydi:** Spring Data'ning modul oilasi bir xil abstraksiya beradi: Spring Data JPA, Spring Data MongoDB (`MongoTemplate`, `@Document`), Spring Data Redis (`RedisTemplate`, `@RedisHash`), Spring Data Elasticsearch (`ElasticsearchOperations`, `@Document(indexName=...)`), Spring Data Cassandra, Spring Data Neo4j, Spring Data JDBC/R2DBC. Cache qatlami uchun `@EnableCaching`, `@Cacheable` va `RedisCacheManager`; sinxronizatsiya uchun Spring for Apache Kafka (`@KafkaListener`), Spring Integration yoki Debezium orqali CDC. Muhim nuqta: har bir store o'z `TransactionManager` iga ega, shuning uchun cross-store atomiklikni `@Transactional` bera olmaydi - `ChainedTransactionManager` deprecated/olib tashlangan, o'rniga outbox pattern va `@TransactionalEventListener(phase = AFTER_COMMIT)` ishlatiladi.

**Qo'llanish keyslari:**
- E-commerce: buyurtmalar PostgreSQL'da, mahsulot qidiruvi Elasticsearch'da, savatcha Redis'da.
- Foydalanuvchi session va rate-limit counter'larini Redis'da saqlash.
- Tavsiya va "do'stlarning do'stlari" so'rovlari uchun Neo4j graf qatlami.
- IoT telemetriyasini time-series bazaga (TimescaleDB/InfluxDB) yozib, agregatni SQL'da saqlash.
- Audit va event log'ni Kafka yoki object storage'ga uzoq muddatli saqlash uchun chiqarish.

**Ehtiyot bo'ling:** Har bir qo'shimcha store - yangi backup, monitoring, versiya yangilash, failover va jamoa bilimi talabi; "chiroyli" deb qo'shilgan to'rtinchi baza ko'pincha PostgreSQL'ning JSONB, full-text search yoki `LISTEN/NOTIFY` imkoniyatlari bilan ham hal qilinardi. Store'lar orasidagi eventual consistency'ni oshkora loyihalashtiring: qidiruv index'i va asosiy baza farq qilgan holatni UI va biznes qoidalari qanday ko'rishini oldindan belgilang, aks holda "mahsulot bor, lekin topilmaydi" turidagi xatolar doimiy bo'ladi.

## 10.12 Har bir servis uchun alohida ma'lumotlar bazasi (Database per Service)

**Tavsif:** Mikroservis arxitekturasida har bir servis o'zining ma'lumotlar sxemasiga yoki butunlay alohida bazasiga egalik qiladi va unga faqat shu servis bevosita murojaat qila oladi. Boshqa servislar ma'lumotni faqat API yoki event orqali oladi, SQL darajasida emas. Bu loose coupling beradi: sxemani o'zgartirish boshqa servislarni buzmaydi, har bir team o'z deployment tezligida harakatlanadi. Narxi esa - distributed transaction yo'qoladi, JOIN o'rniga API composition yoki CQRS kerak bo'ladi.

**Spring'da qayerda uchraydi:** Har bir Spring Boot 3.x servis o'z `application.yml`ida alohida `spring.datasource.*` ga ega bo'ladi; migratsiyalar servis repozitoriysida Flyway (`spring-boot-starter-data-jpa` + `flyway-core`) yoki Liquibase bilan boshqariladi. Polyglot persistence'da bir servis `spring-boot-starter-data-jpa` (PostgreSQL), boshqasi `spring-boot-starter-data-mongodb`, uchinchisi `spring-boot-starter-data-cassandra` ishlatadi. Bir servis ichida bir nechta baza kerak bo'lsa, `@Configuration` da ikkita `DataSource` bean (`@Primary` + `@Qualifier`), ikkita `LocalContainerEntityManagerFactoryBean` va `@EnableJpaRepositories(basePackages=..., entityManagerFactoryRef=..., transactionManagerRef=...)` bilan ajratiladi. Testlarda Testcontainers (`@ServiceConnection`, Spring Boot 3.1+) har bir servis uchun izolyatsiyalangan baza ko'taradi.

**Qo'llanish keyslari:**
- E-commerce'da Order, Payment, Inventory servislari har biri o'z PostgreSQL sxemasini egallaydi va bir-birining jadvalini o'qimaydi.
- Katalog servisi qidiruv uchun Elasticsearch/Mongo tanlaydi, hisob-kitob servisi esa ACID uchun PostgreSQL'da qoladi.
- Mijoz ma'lumotlari GDPR talabi bilan alohida bazada, alohida shifrlash kaliti ostida saqlanadi.
- Yuqori yozuv oqimiga ega telemetriya servisi Cassandra'ga ko'chiriladi, qolgan servislar ta'sirlanmaydi.
- Har bir team o'z migratsiyasini mustaqil deploy qiladi, umumiy "DBA bottleneck" yo'qoladi.

**Ehtiyot bo'ling:** Bitta jismoniy serverda faqat sxema bilan ajratish "mustaqillik" illyuziyasini beradi - bir servisning og'ir query'si qo'shnilarni sekinlashtiradi. Modul chegaralari hali barqarorlashmagan bo'lsa, erta bo'linish sizni cross-service JOIN va eventual consistency murakkabligiga olib kiradi; monolit ichida modullarga bo'lib, keyin ajratish xavfsizroq.

## 10.13 Umumiy ma'lumotlar bazasi (Shared Database) - anti-pattern

**Tavsif:** Bir nechta servis yoki ilova bitta ma'lumotlar bazasiga va bitta jadvallar to'plamiga bevosita yozadi va o'qiydi. Qisqa muddatda bu qulay: tranzaksiya oson, JOIN ishlaydi, consistency "bepul". Uzoq muddatda baza yashirin integratsiya nuqtasiga aylanadi - bitta ustunni o'zgartirish qaysi servisni buzishini hech kim bilmaydi, deploy'lar bir-biriga bog'lanib qoladi va biznes-qoida bir necha codebase'da dublikat bo'ladi. Shuning uchun u mikroservis kontekstida anti-pattern deb qaraladi; faqat modular monolit ichida ongli tanlov sifatida maqbul.

**Spring'da qayerda uchraydi:** Amalda bir nechta Spring Boot ilovasi bir xil `spring.datasource.url`ni ko'rsatishi va har biri o'z `@Entity` sinflarini bir jadvalga map qilishi ko'rinishida uchraydi - natijada ikki xil JPA model bitta jadvalni "egallaydi" va `@Version` optimistic locking ham faqat bir ilova doirasida ishlaydi. Ikkita ilova `spring.jpa.hibernate.ddl-auto` yoki Flyway bilan bir sxemani migratsiya qilsa, `flyway_schema_history` konflikt beradi. Nazoratli variantda bitta servis "owner" bo'ladi (yozish huquqi faqat unda), qolganlari read-only DB user bilan ulanadi yoki baza view'lari orqali o'qiydi; eng to'g'ri yo'l esa - umumiy domen kodini alohida Maven modulga chiqarib, baza orqali emas, API/event orqali integratsiya qilish.

**Qo'llanish keyslari:**
- Legacy monolit va yangi Spring Boot servis migratsiya davrida vaqtincha bir bazani bo'lishadi (strangler fig bosqichi).
- Reporting/BI vositalari asosiy bazaning read replica'siga to'g'ridan-to'g'ri ulanadi.
- Modular monolitda modullar bir baza, lekin har biri o'z sxemasi va o'z Flyway tarixi bilan ishlaydi.
- Kichik jamoa, bitta deploy birligi - bo'lish narxi foydasidan yuqori bo'lgan holat.
- Bir martalik ETL job ishlab chiqarish bazasidan snapshot oladi.

**Ehtiyot bo'ling:** Uni "tezlik uchun hozircha" tanlasangiz, migratsiya rejasini va o'chirish muddatini yozib qo'ying - aks holda u doimiy arxitekturaga aylanadi. Eng xavfli ko'rinishi: ikki servis bir jadvalga yozadi va biznes-invariant (masalan, balans manfiy bo'lmasligi) faqat application kodda tekshiriladi - bu race condition'larni muqarrar qiladi.

## 10.14 Tranzaksion Outbox (Transactional Outbox)

**Tavsif:** Ma'lumotni o'zgartirish va bu haqda event yuborishni atomik qilish muammosini hal qiladi: broker'ga yuborish va bazaga commit alohida resurslar bo'lgani uchun biri muvaffaqiyatli, ikkinchisi muvaffaqiyatsiz bo'lishi mumkin (dual-write muammosi). Pattern bo'yicha event domen o'zgarishi bilan bir xil local tranzaksiyada `outbox` jadvaliga yoziladi. Keyin alohida publisher (poller yoki CDC) shu jadvalni o'qib brokerga yuboradi va yuborilganini belgilaydi. Natijada "at-least-once" kafolat olinadi - commit bo'lgan hamma o'zgarish albatta event sifatida chiqadi.

**Spring'da qayerda uchraydi:** `@Transactional` metod ichida `OrderRepository.save(...)` bilan birga `OutboxRepository.save(new OutboxEvent(...))` chaqiriladi - ikkisi bir JDBC tranzaksiyasida. Publisher tomonida `@Scheduled` + `SELECT ... FOR UPDATE SKIP LOCKED` (Spring Data JPA'da `@Lock(LockModeType.PESSIMISTIC_WRITE)` yoki native query) bilan batch olinadi va `KafkaTemplate`/`RabbitTemplate` orqali yuboriladi. Domen hodisalarini to'plash uchun Spring Data'ning `AbstractAggregateRoot#registerEvent` va `@DomainEvents`/`@AfterDomainEventPublication` mexanizmi, hamda `ApplicationEventPublisher` + `@TransactionalEventListener(phase = BEFORE_COMMIT)` qulay. Kutubxonalar: Debezium Outbox Event Router (CDC variantida), Axon Framework, Eventuate Tram.

```java
@Transactional
public void placeOrder(OrderCmd cmd) {
    Order order = orderRepo.save(Order.from(cmd));
    outboxRepo.save(OutboxEvent.of("Order", order.getId(),
            "OrderPlaced", json.write(order)));   // bir tranzaksiyada
}
```

**Qo'llanish keyslari:**
- Buyurtma yaratilganda `OrderPlaced` eventi yo'qolmasligi kerak bo'lgan to'lov/omborxona integratsiyasi.
- Saga orchestration'da har bir qadamning komandasi ishonchli yuborilishi.
- Audit yoki analitika uchun hamma domen o'zgarishini broker'ga chiqarish.
- Tashqi SaaS (CRM, email) ga webhook yuborishni retry bilan kafolatlash.
- Broker vaqtincha ishdan chiqqanda ham ilovaning yozish operatsiyalari davom etishi.

**Ehtiyot bo'ling:** Kafolat "exactly-once" emas, "at-least-once" - consumer tomonida idempotentlik (Inbox yoki unique key) majburiy, aks holda dublikat to'lov kabi xatolar paydo bo'ladi. Polling'da `SKIP LOCKED` ishlatmasangiz bir nechta instance bir qatorni oladi; yuborilgan qatorlarni tozalash (partition/TTL) rejasi bo'lmasa outbox jadvali bazaning eng katta jadvaliga aylanadi.

## 10.15 Inbox (Idempotent Receiver store)

**Tavsif:** Outbox'ning juft patterni: at-least-once yetkazib beruvchi broker bir xil xabarni bir necha marta berganda business logic ikki marta bajarilmasligini ta'minlaydi. Consumer har bir xabarning unique identifikatorini (message id, event id) `inbox`/`processed_messages` jadvaliga yozadi va bu yozuvni biznes o'zgarishi bilan bir tranzaksiyada commit qiladi. Agar id allaqachon mavjud bo'lsa, xabar jim tashlab ketiladi (ack qilinadi, lekin qayta ishlanmaydi). Shu bilan "effectively-once" semantikasi olinadi.

**Spring'da qayerda uchraydi:** `@KafkaListener` yoki `@RabbitListener` metodi boshida xabar kalitini olish uchun `@Header(KafkaHeaders.RECEIVED_KEY)` / `MessageHeaders.ID` ishlatiladi; `@Transactional` metod ichida `inboxRepo.save(...)` unique primary key bilan urinadi va `DataIntegrityViolationException` tutilsa - dublikat deb qaraladi. Spring Integration'da buning tayyor varianti bor: `IdempotentReceiverInterceptor` va `MetadataStoreSelector` (`JdbcMetadataStore`, `RedisMetadataStore`, `ZookeeperMetadataStore`). Yana bir yondashuv - biznes jadvalida idempotency key ustuniga unique index qo'yish; HTTP API tomonida `Idempotency-Key` header'ini `HandlerInterceptor`/filter orqali tekshirish. Kafka consumer'da `MANUAL_IMMEDIATE` ack rejimi va `DefaultErrorHandler` bilan birgalikda ishlatiladi.

**Qo'llanish keyslari:**
- To'lov servisi `PaymentRequested` eventini ikki marta olsa ham kartadan bir marta pul yechish.
- Rebalance yoki retry tufayli Kafka'dan qayta kelgan `OrderPlaced`ni ikki marta omborda rezerv qilmaslik.
- Mijoz REST API'da `Idempotency-Key` yuborsa, tarmoq timeout'idan keyingi qayta urinish dublikat buyurtma yaratmasligi.
- Webhook qabul qiluvchi endpoint (Stripe, Telegram) bir xil `event_id` bilan takroriy chaqiriqni filtrlashi.
- Email/SMS yuboruvchi servis bir xabarni foydalanuvchiga ikki marta jo'natmasligi.

**Ehtiyot bo'ling:** Inbox yozuvi va biznes o'zgarishi bir tranzaksiyada bo'lmasa, pattern hech narsani kafolatlamaydi - "avval tekshirdim, keyin ishladim" ketma-ketligi klassik race condition. Jadvalni cheksiz o'stirmang: retention oynasini broker'ning maksimal retry/replay oynasidan kattaroq qilib tanlang va eski yozuvlarni muntazam tozalang.

## 10.16 Ma'lumot o'zgarishini ushlash (Change Data Capture / Debezium)

**Tavsif:** Ilova kodini o'zgartirmasdan, ma'lumotlar bazasidagi har bir INSERT/UPDATE/DELETE ni event oqimiga aylantiradi. Debezium bazaning tranzaksion log'ini (PostgreSQL logical replication slot va WAL, MySQL binlog, MongoDB oplog, Oracle LogMiner) o'qiydi va o'zgarishlarni Kafka topic'lariga `before`/`after` tasvirlari bilan yuboradi. Bu polling'ga qaraganda arzon va ishonchli: bazaga qo'shimcha query yuklanmaydi, o'chirishlar ham ko'rinadi, tartib tranzaksion log tartibida saqlanadi. Odatda legacy bazadan event-driven dunyoga ko'prik yoki read model'ni yangilash uchun ishlatiladi.

**Spring'da qayerda uchraydi:** Eng ko'p tarqalgan sxema - Debezium Kafka Connect'da ishlaydi, Spring Boot ilovasi esa natijani `@KafkaListener` bilan iste'mol qiladi (`spring-kafka`). Debezium Outbox Event Router SMT bilan birga outbox jadvalidagi qatorlar to'g'ridan-to'g'ri domen topic'lariga marshrutlanadi. Embedded variantda ilova ichida `io.debezium:debezium-embedded` va `DebeziumEngine`/`io.debezium.engine.RecordChangeEvent` ishlatiladi; Spring Boot'da bu odatda `@Bean DebeziumEngine<...>` + `ExecutorService` ko'rinishida yoziladi, ammo bu ilovani stateful qiladi (offset file/`KafkaOffsetBackingStore`). Testlar uchun Testcontainers'ning `DebeziumContainer` moduli mavjud. Spring Cloud Stream bilan ham binder orqali ulash mumkin.

**Qo'llanish keyslari:**
- Legacy monolit bazasidan yangi mikroservislarga ma'lumot oqimini chiqarish (strangler migratsiya).
- CQRS read model'ini yoki Elasticsearch indeksini real-time yangilab turish.
- Data lake / warehouse'ga (Snowflake, BigQuery) kechikishi past replikatsiya.
- Cache invalidation: qator o'zgarganda Redis kalitini bekor qilish.
- Transactional Outbox publisher'ini polling o'rniga log-based qilib tezlashtirish.

**Ehtiyot bo'ling:** CDC bazaning jismoniy sxemasini event kontraktiga aylantirib qo'yadi - ustun nomini o'zgartirsangiz consumer'lar buziladi; shuning uchun xom CDC topic'ini tashqi iste'molchilarga ochmang, domen eventiga transform qiling. Operatsion jihatdan ham ehtiyotkorlik kerak: ishlamay qolgan replication slot PostgreSQL'da WAL to'planib diskni to'ldiradi, schema evolution va snapshot (initial load) rejimlari esa alohida rejalashtirishni talab qiladi.

## 10.17 Snapshot (Snapshot)

**Tavsif:** Holatni qayta tiklash uchun uzun o'zgarishlar tarixini boshidan o'ynatish qimmat bo'lganda, vaqti-vaqti bilan joriy holatning to'liq nusxasi saqlanadi. Keyin tiklash snapshot'dan boshlanadi va faqat undan keyingi eventlar qo'llaniladi - O(n) o'rniga O(k). Event sourcing'da bu asosiy optimizatsiya; kengroq ma'noda esa baza/volume snapshot, state store checkpoint yoki hisoblangan oraliq natija ham shu patternga kiradi. Snapshot haqiqat manbai emas - eventlar manba, snapshot faqat kesh.

**Spring'da qayerda uchraydi:** Axon Framework (Spring Boot starter bilan integratsiyalashgan) `@Aggregate` uchun `SnapshotTriggerDefinition` va `EventCountSnapshotTriggerDefinition` beradi, snapshotlar `SnapshotEventStore`da saqlanadi. Eventuate yoki qo'lda yozilgan event store'da aggregate holati JSON sifatida `snapshot` jadvaliga `aggregate_id` + `version` bilan yoziladi va Jackson `ObjectMapper` orqali serializatsiya qilinadi. Spring Statemachine'da `StateMachinePersister`/`StateMachineRuntimePersister` holatni saqlab, keyin qayta tiklaydi. Kafka Streams (`spring-kafka` bilan birga ishlatilganda) RocksDB state store uchun changelog topic va checkpoint yuritadi; Spring Batch'da esa `JobRepository` step'ning bajarilgan nuqtasini saqlab, restart'da shu yerdan davom etadi.

**Qo'llanish keyslari:**
- Minglab eventga ega bank hisobi aggregate'ini millisekundlarda yuklash.
- IoT qurilma holatini har 1000 telemetriya hodisasidan keyin snapshot qilish.
- Uzun ishlaydigan Spring Batch job'ini uzilishdan keyin oxirgi checkpoint'dan davom ettirish.
- Hisobot uchun oyning oxiridagi balans kesimini saqlab, keyingi hisob-kitoblarni shundan boshlash.
- Pre-prod muhitga ishlab chiqarish bazasining snapshot'ini (anonimlashtirilgan) ko'chirish.

**Ehtiyot bo'ling:** Snapshot serializatsiya formatiga bog'liq - aggregate sinfi o'zgarganda eski snapshotlarni o'qiy olmay qolishingiz mumkin, shuning uchun versiyalangan format yoki "schema o'zgarsa snapshotlarni invalidatsiya qilish" strategiyasi kerak. Snapshot'ni haqiqat manbai sifatida ishlatib, eventlarni o'chirib tashlash event sourcing'ning butun qiymatini yo'q qiladi.

## 10.18 Materiallashtirilgan ko'rinish (Materialized View)

**Tavsif:** Query vaqtida qimmat JOIN va agregatsiya qilish o'rniga, natija oldindan hisoblanib alohida o'qishga optimallashtirilgan strukturada saqlanadi. Yozuv tomonida normalizatsiya saqlanadi, o'qish tomonida esa denormalizatsiyalangan ko'rinish - shu bilan read latency keskin tushadi. Ko'rinish event, CDC yoki jadval bo'yicha yangilanadi, ya'ni ma'lumot eventual consistent bo'ladi. Mikroservislarda bu cross-service JOIN muammosining asosiy yechimi: bir servis boshqalarning eventlaridan o'ziga kerakli "o'qish modeli"ni yig'adi.

**Spring'da qayerda uchraydi:** PostgreSQL'da `CREATE MATERIALIZED VIEW` ni Flyway migratsiyasi bilan yaratib, read-only `@Entity` yoki `@Immutable` (Hibernate) sinf bilan map qilish, `REFRESH MATERIALIZED VIEW CONCURRENTLY` ni esa `@Scheduled` + `JdbcTemplate` bilan chaqirish mumkin. Ilova darajasida CQRS read model `@KafkaListener` orqali yangilanib, `spring-boot-starter-data-elasticsearch`, `data-mongodb` yoki `data-redis` ichida saqlanadi. Spring Data'ning projection interfeyslari (`interface OrderSummary { ... }`) va `@Query` bilan DTO projection - "arzon" materiallashtirish shakli; Kafka Streams'da esa `KTable` va interactive queries bilan ko'rinish ilova ichida yuritiladi. Caching qatlami uchun `@Cacheable` + Caffeine/Redis ko'p hollarda yetarli alternativa bo'ladi.

**Qo'llanish keyslari:**
- Mijoz kabinetidagi "buyurtmalar ro'yxati" ko'rinishi Order, Payment va Shipping servislari eventlaridan yig'iladi.
- Dashboard uchun kunlik savdo agregatlari oldindan hisoblanadi, har so'rovda `GROUP BY` bajarilmaydi.
- Mahsulot qidiruvi uchun Elasticsearch indeksi denormalizatsiyalangan hujjatlar bilan to'ldiriladi.
- Leaderboard yoki reyting Redis sorted set'da doimiy yangilanib turadi.
- Og'ir analitik hisobot read replica'dagi materialized view'dan o'qiladi, OLTP yuklanmaydi.

**Ehtiyot bo'ling:** Ko'rinish eventual consistent - foydalanuvchi o'zi yozgan ma'lumotni darhol ko'rmasligi mumkin, shuning uchun read-your-writes kerak bo'lgan ekranlarda to'g'ridan-to'g'ri write model'dan o'qing. Yana bir tuzoq: ko'rinishni qayta qurish (rebuild) yo'lini kun birinchi kunidan loyihalashtirmaslik - event bilan yangilanadigan modelda bug topilganda uni noldan tiklash imkoniyati bo'lishi shart.

## 10.19 Indeks jadvali (Index Table)

**Tavsif:** Asosiy saqlash strukturasi faqat bitta kalit bo'yicha samarali qidiruvga imkon berganda (masalan, NoSQL'da partition key), boshqa maydon bo'yicha qidiruv uchun maxsus "indeks" jadvali yaratiladi: unda kalit - izlanadigan maydon, qiymat - asosiy yozuvning identifikatori (yoki tez-tez kerak bo'ladigan maydonlar nusxasi). Bu secondary index'ni qo'lda qurish demakdir. Natijada full scan o'rniga ikki marta nuqtaviy o'qish bo'ladi, lekin yozuvda bir nechta jadvalni sinxron ushlab turish majburiyati paydo bo'ladi.

**Spring'da qayerda uchraydi:** Cassandra'da Spring Data `@Table` bilan bir xil ma'lumotni bir necha query-specific jadvalga yozish (`users_by_id`, `users_by_email`) odatiy amaliyot; `@PrimaryKeyClass`, `@PrimaryKeyColumn` bilan clustering kalitlari belgilanadi va yozuvlar `CassandraBatchOperations` orqali birga yuboriladi. Redis'da `spring-boot-starter-data-redis` va `@RedisHash` + `@Indexed` Spring Data Redis'ning secondary index'ini (set-based) avtomatik yuritadi. DynamoDB'da AWS SDK v2 Enhanced Client'ning GSI'si shu patternning boshqarilgan shakli. Relyatsion bazada esa bu odatda kerak emas - `@Table(indexes = @Index(columnList = "email"))` yoki Flyway'da `CREATE INDEX` yetarli; indeks jadvali faqat juda katta hajm yoki alohida saqlash talabida oqlanadi.

**Qo'llanish keyslari:**
- Cassandra'da foydalanuvchini `id` bo'yicha ham, `email` va `phone` bo'yicha ham topish uchun uchta jadval.
- Katalogda mahsulotni SKU va barcode bo'yicha nuqtaviy izlash.
- Hodisalar jurnalini `tenant_id` bo'yicha saqlab, `correlation_id` bo'yicha izlash uchun qo'shimcha jadval.
- Redis'da sessiyani token bo'yicha va `userId` bo'yicha ikki tomonlama topish.
- Fayl saqlash (S3) metadata'sini nom va hash bo'yicha ikki xil kalit bilan indekslash.

**Ehtiyot bo'ling:** Indeks jadvali - qo'lda yuritiladigan dublikat, demak uni yangilashni o'tkazib yuborgan har bir kod yo'li "ko'rinmas" ma'lumot nomuvofiqligi yaratadi; yozuvlarni bitta joyda (repository/service) markazlashtiring va muntazam reconciliation job yuritib turing. Kardinalligi past maydon (masalan, `status`) uchun indeks jadvali qilish esa "hot partition" muammosiga olib keladi.

## 10.20 Ommaviy / paketli kiritish (Bulk / Batch insert)

**Tavsif:** Katta hajmdagi yozuvlarni bittalab INSERT qilish tarmoq round-trip va tranzaksiya overhead'i tufayli sekin bo'ladi. Pattern bo'yicha yozuvlar guruhlarga (batch) to'planadi va bitta so'rov yoki bitta statement bilan bazaga yuboriladi - ko'pincha bir necha o'n baravar tezlanish beradi. Muvozanat chegarasi muhim: batch juda kichik bo'lsa foyda yo'q, juda katta bo'lsa memory va lock ushlab turish vaqti oshadi, xato bo'lganda esa butun batch qayta urinishga ketadi.

**Spring'da qayerda uchraydi:** `JdbcTemplate.batchUpdate(...)` va `NamedParameterJdbcTemplate.batchUpdate(...)` - eng to'g'ridan-to'g'ri yo'l; Spring Boot 3.2+ da `JdbcClient` ham bor. JPA/Hibernate'da `spring.jpa.properties.hibernate.jdbc.batch_size`, `order_inserts=true`, `order_updates=true` sozlanadi va `EntityManager.flush()`/`clear()` har batch'dan keyin chaqiriladi; `GenerationType.IDENTITY` batching'ni o'chirib qo'yganini bilish muhim (`SEQUENCE` + `pooled` optimizer tanlang). PostgreSQL JDBC'da `reWriteBatchedInserts=true` parametri INSERT'larni multi-row ga aylantiradi. Juda katta yuklamalarda PostgreSQL `COPY` (pgjdbc `CopyManager`) ishlatiladi. Spring Batch esa butun ETL oqimi uchun chunk-oriented processing beradi: `JdbcBatchItemWriter`, `JpaItemWriter`, `FlatFileItemReader` va `@EnableBatchProcessing`.

```java
jdbcTemplate.batchUpdate("INSERT INTO price(sku, amount) VALUES (?,?)",
    rows, 1000, (ps, row) -> {
        ps.setString(1, row.sku());
        ps.setBigDecimal(2, row.amount());
    });
```

**Qo'llanish keyslari:**
- Kunlik narx faylidan million qatorni katalog bazasiga yuklash.
- Legacy sistemadan bir martalik migratsiyada ma'lumot ko'chirish.
- Telemetriya yoki log eventlarini 1000 talik batch bilan saqlash.
- Spring Batch job'i orqali tungi hisob-kitob natijalarini jadvalga yozish.
- Integratsiya testlari uchun test ma'lumotlarini tez seed qilish.

**Ehtiyot bo'ling:** Bitta ulkan tranzaksiyada hamma narsani yozish WAL o'sishi, lock eskalatsiyasi va rollback'ning juda qimmat bo'lishiga olib keladi - chunk'larga bo'lib commit qiling va qaysi chunk'da to'xtaganini saqlang (idempotent restart). Shuningdek JPA batching jim ravishda o'chib qolishi mumkin (IDENTITY id, har save'dan keyin flush, `saveAll` ichida avtomatik batch yo'q) - tezlikni faraz qilmang, `hibernate.generate_statistics` yoki query log bilan tasdiqlang.

## 10.21 Ikki fazali commit / XA (Two-Phase Commit / XA)

**Tavsif:** Bir nechta resurs (ikki baza, baza va message broker) ustidagi o'zgarishlarni atomik qilish uchun ishlatiladigan distributed tranzaksiya protokoli. Transaction manager avval hamma qatnashchidan "prepare" so'raydi - har biri commit qilishga qodirligini kafolatlaydi va log'ga yozadi; hammasi "ha" desa ikkinchi fazada "commit" buyrug'i yuboriladi, aks holda hammasi rollback qiladi. Bu kuchli consistency beradi, lekin qimmat: ikki marta tarmoq aylanishi, resurslarda uzoq lock, va coordinator prepare bilan commit o'rtasida o'lsa qatnashchilar "in-doubt" holatida blokda qoladi. Zamonaviy mikroservislarda shu sababli Saga va Outbox afzal ko'riladi.

**Spring'da qayerda uchraydi:** `JtaTransactionManager` (Spring Framework 6.x) orqali tashqi JTA provayderga ulanadi; Jakarta EE serverida (WildFly, WebLogic) bu konteynerning transaction manager'i bo'ladi. Standalone Spring Boot'da tarixiy ravishda Atomikos va Bitronix ishlatilgan, ammo Spring Boot 3.x da Bitronix uchun auto-configuration olib tashlangan, Atomikos qo'llab-quvvatlashi ham `spring-boot-starter-jta-atomikos` sifatida 3.0'da tugatilgan - bugun odatda Narayana (`narayana-spring-boot-starter`) yoki konteyner JTA'si tanlanadi. Resurs tomonida `XADataSource` (PostgreSQL `PGXADataSource`, Oracle `OracleXADataSource`) va XA-ga mos JMS `ConnectionFactory` kerak. Muhim fakt: Apache Kafka XA ni qo'llab-quvvatlamaydi - `KafkaTransactionManager` faqat Kafka'ning o'z tranzaksiyalari; Kafka + DB atomikligi uchun `ChainedTransactionManager` ishlatilgan, ammo u Spring'da deprecated va haqiqiy atomiklik bermaydi, shuning uchun to'g'ri yechim Outbox.

**Qo'llanish keyslari:**
- Legacy bank tizimida bir tranzaksiyada ikki alohida RDBMS'ga yozish (masalan, core banking va ledger).
- Jakarta EE/JMS muhitida XA message broker'dan o'qib, bazaga yozishni atomik qilish.
- Monolit migratsiyasi davrida eski va yangi baza vaqtincha sinxron ushlab turilishi.
- Mainframe yoki ERP (SAP) adapterlari XA talab qilgan integratsiyalar.
- Regulyator qat'iy strong consistency talab qilgan va eventual consistency qabul qilinmaydigan hollarda.

**Ehtiyot bo'ling:** XA ni mikroservislar orasida ishlatish eng keng tarqalgan xato - u servislarni availability jihatidan bir-biriga bog'laydi (bir qatnashchi tushsa hammasi bloklanadi) va gorizontal kengayishga to'sqinlik qiladi; bunday hollarda Saga + Outbox + Inbox kombinatsiyasini tanlang. Agar XA zarur bo'lsa, recovery log'ni doimiy diskda saqlash, in-doubt tranzaksiyalarni monitoring qilish va unique transaction manager ID berish operatsion majburiyatga aylanadi - klasterda bir xil ID bilan ikki instance ko'tarish ma'lumotni buzadi.

## 10.22 Try-Confirm-Cancel (TCC)

**Tavsif:** TCC - distributed tranzaksiyalarni uch fazaga ajratadigan pattern: `Try` fazasida resurs rezerv qilinadi (masalan, balansdan pul "frozen" holatga o'tadi), `Confirm` fazasida rezerv haqiqiy o'zgarishga aylanadi, `Cancel` fazasida esa rezerv bo'shatiladi. Saga'dan farqi shundaki, har bir servis o'z resursini oldindan ushlab turadi, shuning uchun `Confirm` fazasi deyarli hech qachon muvaffaqiyatsiz bo'lmaydi. Bu 2PC'ning biznes-darajadagi muqobili: lock ma'lumotlar bazasida emas, balki domen modelida (reserved/available maydonlari) saqlanadi.

**Spring'da qayerda uchraydi:** Har bir mikroservis uchta endpoint beradi (`POST /reserve`, `POST /confirm`, `POST /cancel`) - ular oddiy `@RestController` metodlari bo'lib, har biri `@Transactional` bilan lokal tranzaksiyada ishlaydi. Koordinatorni Spring Boot 3.x'da `RestClient`/`WebClient` yoki Spring Cloud OpenFeign bilan yozish mumkin; Seata framework'ning TCC rejimi uchun `io.seata:seata-spring-boot-starter` va `@LocalTCC` + `@TwoPhaseBusinessAction` annotatsiyalari mavjud. Rezervlarning muddati o'tganini tozalash uchun `@Scheduled` task yoki Quartz job ishlatiladi, idempotentlik uchun esa `reservation_id` ustunida unique constraint qo'yiladi.

**Qo'llanish keyslari:**
- Aviachipta bron qilish: o'rindiq 15 daqiqaga ushlanadi, to'lov tasdiqlansa `Confirm`, aks holda `Cancel`.
- E-commerce'da buyurtma yaratishda ombordagi tovarni rezerv qilish va to'lovdan keyin yakuniy yechib tashlash.
- Hisobdan pul yechishda `frozen_balance` ga ko'chirish, keyin kontragent tasdiqlagandan so'ng yakunlash.
- Telecom'da raqam yoki tarif rejasini vaqtincha band qilib, hujjatlar tekshirilgandan keyin aktivlashtirish.
- Mehmonxona va avtomobil ijarasi kabi "cheklangan inventar" domenlarida overbooking'ni oldini olish.

**Ehtiyot bo'ling:** `Try` muvaffaqiyatli bo'lib, koordinator qulagan holatda rezervlar abadiy "osilib" qolishi mumkin - shuning uchun TTL va majburiy reaper job hayotiy zarur, hamda `Cancel` operatsiyasi `Try` kelmagan holatda ham xatosiz ishlashi (empty rollback) kerak. TCC har bir servisning domen modelini o'zgartirishni talab qiladi, shuning uchun uchinchi tomon API'lari yoki legacy tizimlar bilan amalda qo'llash qiyin; oddiy eventual consistency yetarli bo'lsa, Saga'ni tanlang.

## 10.23 Kompensatsiyalovchi tranzaksiya (Compensating Transaction)

**Tavsif:** Distributed muhitda `ROLLBACK` imkoni bo'lmaganida, allaqachon commit qilingan o'zgarishni semantik jihatdan bekor qiluvchi yangi tranzaksiya bajariladi: pul yechilgan bo'lsa - qaytariladi, email yuborilgan bo'lsa - bekor qilish xabari yuboriladi. Kompensatsiya texnik rollback emas, balki biznes-darajadagi "teskari harakat" bo'lib, audit izini saqlab qoladi. Bu Saga pattern'ining asosiy mexanizmi va TCC'dan farqli ravishda hech qanday oldindan rezerv talab qilmaydi.

**Spring'da qayerda uchraydi:** Saga orkestratsiyasida har bir qadam uchun kompensatsiya metodi yoziladi; Spring Statemachine (`spring-statemachine-core`) yoki Axon Framework'ning `@SagaEventHandler` + `SagaLifecycle` bilan kuzatiladi. Camunda 8 / Zeebe'ning `spring-boot-starter-camunda-sdk` BPMN compensation boundary event'larini beradi. Spring Framework 6.x'da lokal darajada `TransactionSynchronization#afterCompletion` yoki `@TransactionalEventListener(phase = AFTER_ROLLBACK)` orqali tashqi effektlarni tozalash mumkin; takrorlash uchun Spring Retry (`@Retryable`) va oxirgi chora sifatida dead-letter queue ishlatiladi.

**Qo'llanish keyslari:**
- Buyurtma bekor qilinganda to'lovni refund qilish va ombordagi zaxirani qaytarish.
- Bron zanjirida (reys + mehmonxona + avtomobil) oxirgi qadam yiqilsa, avvalgi bronlarni bekor qilish.
- Noto'g'ri hisoblangan bonus ballarini teskari provodka bilan yechib tashlash.
- Tashqi KYC servisi rad etganda yaratilgan hisobni "closed" holatiga o'tkazish.
- Yuborilgan noto'g'ri hisob-faktura uchun credit note (kredit-nota) generatsiya qilish.

**Ehtiyot bo'ling:** Kompensatsiyaning o'zi ham muvaffaqiyatsiz bo'lishi mumkin, shuning uchun u idempotent, retry'ga chidamli va monitoring ostida bo'lishi shart - aks holda tizim yarim-bajarilgan holatda qoladi. Ba'zi harakatlarni kompensatsiya qilib bo'lmaydi (yuborilgan SMS, chop etilgan hujjat, uchinchi tomonga oshkor etilgan ma'lumot), shuning uchun bunday "qaytarib bo'lmaydigan" qadamlarni Saga'ning eng oxiriga qo'ying.

## 10.24 Event Sourcing ombori (Event Sourcing Store)

**Tavsif:** Agregatning joriy holatini jadvalda saqlash o'rniga, unga olib kelgan barcha o'zgarishlar immutable event'lar ketma-ketligi sifatida append-only jurnalga yoziladi. Joriy holat event'larni qayta o'ynatish (replay) yo'li bilan tiklanadi, katta agregatlar uchun esa snapshot'lar qo'llaniladi. Natijada to'liq audit izi, vaqt bo'yicha "orqaga qaytish" (temporal query) va bir xil event oqimidan turli read model'lar qurish imkoni paydo bo'ladi.

**Spring'da qayerda uchraydi:** Axon Framework Spring Boot starter (`axon-spring-boot-starter`) eng keng tarqalgan yechim: `@Aggregate`, `@CommandHandler`, `@EventSourcingHandler`, `AggregateLifecycle.apply()` va `EventStore` abstraksiyasi. Muqobil variantlar - Eventuate Tram, yoki EventStoreDB kliyenti bilan oddiy Spring Boot 3.x servisi. "Qo'lda" realizatsiyada `events` jadvali (`aggregate_id`, `sequence_no`, `event_type`, `payload` jsonb) va `(aggregate_id, sequence_no)` ustida unique constraint optimistik lock vazifasini bajaradi; yozish uchun Spring Data JDBC yoki `JdbcTemplate`, seriyalash uchun Jackson ishlatiladi.

**Qo'llanish keyslari:**
- Bank hisob-raqami: har bir debet/kredit event sifatida, balans esa hisoblanadigan proyeksiya.
- Buyurtma hayotiy sikli (created → paid → shipped → delivered) bo'yicha to'liq tarix va regulator talab qiladigan audit.
- Insurance polisi versiyalari va retroaktiv o'zgartirishlarni (endorsement) aniq sanaga bog'lab saqlash.
- Bug tahlili uchun production holatini aynan replay qilib lokal muhitda tiklash.
- Yangi analitik read model'ni mavjud event'lardan noldan qurib olish (retroactive reporting).

**Ehtiyot bo'ling:** Event schema evolyutsiyasi (upcasting) va GDPR'ning "o'chirilish huquqi" immutable jurnal bilan to'qnashadi - shuning uchun shaxsiy ma'lumotlarni event ichida emas, kalit bilan ajratilgan shifrlangan "crypto-shredding" omborida saqlang. Event Sourcing'ni butun tizimga emas, faqat tarix va audit haqiqatan zarur bo'lgan core domenlarga qo'llang; CRUD'ga yaqin modullarda u ortiqcha murakkablik va juda qimmat debugging keltiradi.

## 10.25 Arxivlash / tozalash (Archive / Purge)

**Tavsif:** Operatsion ma'lumotlar bazasini kichik va tez ushlab turish uchun "sovigan" yozuvlar arzon omborga ko'chiriladi (archive), keyin esa muddati o'tganlari butunlay o'chiriladi (purge). Bu ikki bosqichli bo'lishi muhim: avval nusxa ishonchli joyga ko'chadi, keyingina manba'dan o'chiriladi. Natijada index'lar kichrayadi, backup/restore vaqti qisqaradi, so'rovlar tezlashadi.

**Spring'da qayerda uchraydi:** Spring Boot 3.x'da `@Scheduled(cron = "...")` yoki Quartz (`spring-boot-starter-quartz`) bilan periodik job; katta hajm uchun Spring Batch (`spring-boot-starter-batch`) va `JdbcPagingItemReader` + `JdbcBatchItemWriter` yoki `RepositoryItemReader`, chunk-oriented processing bilan. O'chirishni bo'laklab bajarish uchun `@Modifying @Query` ichida `LIMIT`li DELETE yoki native query; PostgreSQL'da partition'larni `DETACH PARTITION` bilan bir zumda chiqarib yuborish eng arzon usul. Arxiv maqsadi sifatida S3 (`spring-cloud-aws-starter-s3` yoki AWS SDK v2) yoki alohida "cold" DataSource ishlatiladi.

**Qo'llanish keyslari:**
- 2 yildan oshgan buyurtma va to'lov tarixini S3'ga Parquet formatida chiqarib, OLTP bazasidan o'chirish.
- Audit log va access log jadvallarini oylik partition'lar bilan aylantirib turish.
- Tugatilgan Camunda/Quartz process instance'larini history bazasiga ko'chirish.
- Notification/outbox jadvalidagi yuborilgan yozuvlarni 30 kundan keyin tozalash.
- Soft-delete qilingan foydalanuvchi profillarini grace period tugagach butunlay purge qilish.

**Ehtiyot bo'ling:** Katta `DELETE` bir urinishda transaction log'ni to'ldiradi, lock eskalatsiyasiga va replikatsiya lag'iga olib keladi - har doim batch'lab (masalan 5-10 ming qator) va past yuklama oynasida bajaring. Tashqi kalitlar va hisobotlar arxivlangan yozuvlarga murojaat qilishi mumkin, shuning uchun purge'dan oldin bog'liqliklarni va huquqiy saqlash muddatlarini tekshiring.

## 10.26 Ma'lumotlarni saqlash muddati (Data Retention)

**Tavsif:** Har bir ma'lumot toifasi uchun qancha vaqt saqlanishi, qachon anonimlashtirilishi va qachon o'chirilishi oldindan belgilanadigan va avtomatlashtirilgan siyosat. Retention - Archive/Purge'ning "nima uchun va qancha" tomoni: u huquqiy talablardan (GDPR, buxgalteriya qonunlari, PCI DSS) kelib chiqadi va kodda deklarativ qoida sifatida ifodalanadi. To'g'ri qo'yilgan retention ham xarajatni, ham huquqiy riskni kamaytiradi.

**Spring'da qayerda uchraydi:** Siyosatlar `@ConfigurationProperties` orqali `application.yml`da toifa → muddat ko'rinishida saqlanadi, bajarish esa Spring Batch job yoki `@Scheduled` task bilan amalga oshiriladi. TTL'ni ombor darajasida qo'yish ham mumkin: Redis'da `RedisTemplate#expire` va Spring Data Redis'ning `@TimeToLive`, MongoDB'da `@Indexed(expireAfterSeconds = ...)` yoki `@Document` ustidagi TTL index, Kafka'da topic-level `retention.ms`. Spring Session'da `spring.session.timeout`, Spring Security OAuth2 Authorization Server'da token va `OAuth2AuthorizationService` yozuvlarini tozalash alohida ko'rib chiqiladi. Anonimlashtirish uchun JPA entity listener (`@PreUpdate`) emas, aniq batch step yozish afzal.

**Qo'llanish keyslari:**
- GDPR bo'yicha marketing analitikasini 14 oydan keyin anonimlashtirish.
- To'lov kartasi ma'lumotlarini PCI DSS talabiga ko'ra faqat tokenlangan holda va cheklangan muddat saqlash.
- Buxgalteriya hujjatlarini milliy qonun talab qilgan 5-10 yil davomida o'chirmaslik uchun "legal hold" belgisi.
- Chat/support yozishmalarini 180 kundan keyin avtomatik o'chirish.
- Xodim ishdan bo'shagandan keyin HR ma'lumotlarining bir qismini bosqichma-bosqich purge qilish.

**Ehtiyot bo'ling:** Retention siyosati backup, replika, data warehouse, log aggregator va cache nusxalariga ham tatbiq etilishi kerak - asosiy jadvaldan o'chirib, Elasticsearch yoki S3 backup'da qoldirib ketish eng keng tarqalgan xato. Sud yoki tekshiruv davridagi "legal hold" avtomatik o'chirishdan ustun turishi shart, aks holda dalillarni yo'q qilish deb baholanishi mumkin.

## 10.27 Diskda va maydon darajasida shifrlash (Encryption at Rest / Field-Level Encryption)

**Tavsif:** Ma'lumotlar diskda shifrlangan holda saqlanadi, shunda disk, backup yoki dump o'g'irlangan taqdirda ham o'qib bo'lmaydi. Encryption at rest butun hajm yoki tablespace darajasida (TDE) shaffof ishlaydi, field-level encryption esa faqat tanlangan ustunlarni (passport raqami, karta, telefon) ilova darajasida shifrlaydi va DBA'dan ham himoya qiladi. Qidiruv kerak bo'lsa, deterministik shifr yoki blind index (HMAC) qo'shiladi.

**Spring'da qayerda uchraydi:** Spring Security Crypto moduli `Encryptors.stronger(password, salt)` (AES-GCM) va `TextEncryptor` beradi; JPA'da `@Convert(converter = ...)` bilan `AttributeConverter` yozib, ustunni shaffof shifrlash odatiy yondashuv. Kalitlarni Spring Cloud Vault (`spring-cloud-starter-vault-config`), AWS KMS yoki `spring-cloud-aws-starter-secrets-manager` orqali olish kerak - `application.properties`da emas. Spring Cloud Config Server `{cipher}` prefiksli qiymatlarni va `/encrypt` endpoint'ini qo'llab-quvvatlaydi; Jasypt (`jasypt-spring-boot-starter`) konfiguratsiya shifrlash uchun keng ishlatiladi. Java 17+ da `javax.crypto` va `KeyStore` standart API sifatida mavjud.

```java
@Converter
public class EncryptedStringConverter implements AttributeConverter<String, String> {
    private final TextEncryptor enc; // Vault'dan olingan kalit bilan quriladi
    EncryptedStringConverter(TextEncryptor enc) { this.enc = enc; }
    public String convertToDatabaseColumn(String v) { return v == null ? null : enc.encrypt(v); }
    public String convertToEntityAttribute(String v) { return v == null ? null : enc.decrypt(v); }
}
```

**Qo'llanish keyslari:**
- Fintech'da pasport, STIR va karta oxirgi raqamlarini maydon darajasida shifrlash.
- Tibbiy ilovada diagnoz va analiz natijalarini DBA ham ko'ra olmasligi uchun ilova tomonida shifrlash.
- Backup va dump fayllarining o'g'irlanishiga qarshi butun bazani TDE bilan himoyalash.
- Event Sourcing'da shaxsiy ma'lumotlarni foydalanuvchi kaliti bilan shifrlab, "crypto-shredding" orqali o'chirish.
- Multi-tenant SaaS'da har bir tenant uchun alohida kalit bilan izolyatsiya.

**Ehtiyot bo'ling:** Shifrlangan ustun bo'yicha `LIKE`, `ORDER BY` va oddiy index ishlamaydi - qidiruv kerak bo'lsa oldindan blind index yoki deterministik shifrni loyihalashtiring, aks holda butun jadvalni dekriptlash bilan tugaydi. Kalit rotatsiyasi va kalitni yo'qotish rejasini boshidan o'ylab qo'ying: kalitsiz backup - foydasiz backup, va kodga "hardcode" qilingan kalit shifrlashni butunlay ma'nosiz qiladi.

## 10.28 O'qish/yozishni ajratish (Read/Write Splitting)

**Tavsif:** Yozish operatsiyalari primary (master) nodega, o'qish operatsiyalari esa bir yoki bir nechta replikaga yo'naltiriladi. Bu primary'dagi yuklamani kamaytiradi va o'qish bo'yicha gorizontal masshtablash imkonini beradi, ayniqsa read-heavy tizimlarda. Buning narxi - replikatsiya lag'i, ya'ni replikadan o'qilgan ma'lumot bir necha millisekund yoki sekund eskirgan bo'lishi mumkin.

**Spring'da qayerda uchraydi:** Klassik yechim - `AbstractRoutingDataSource`'ni extend qilib, `determineCurrentLookupKey()` ichida `TransactionSynchronizationManager.isCurrentTransactionReadOnly()` natijasiga qarab primary/replica DataSource tanlash; so'ng `@Transactional(readOnly = true)` avtomatik ravishda replikaga yo'naltiradi. `LazyConnectionDataSourceProxy` bilan o'rash shart, aks holda connection tranzaksiya read-only flag o'rnatilgunga qadar olinadi. Muqobil variantlar: PostgreSQL JDBC'ning `targetServerType=preferSecondary` + `hosts` ro'yxati, MySQL Connector/J'ning replication URL'i, yoki infratuzilma darajasida PgBouncer/ProxySQL. R2DBC uchun Spring Data R2DBC'da `@Transactional(readOnly = true)` ham shu mantiqqa ulanadi.

**Qo'llanish keyslari:**
- Katalog va mahsulot qidiruvi kabi og'ir `SELECT`larni replikalarga chiqarish.
- Hisobot va BI so'rovlarini alohida "reporting replica"da bajarib, OLTP'ni himoyalash.
- Spring Batch'ning o'qish step'larini replikadan, yozish step'ini primary'dan ishlatish.
- Mobil ilova uchun feed/listing endpoint'larini replikadan xizmat qilish.
- Ko'p regionli deploy'da foydalanuvchiga eng yaqin replikadan o'qib, latency'ni kamaytirish.

**Ehtiyot bo'ling:** "Write-then-read" senariysi (yozgandan keyin darhol o'qish) replikatsiya lag'i sababli eski ma'lumot qaytaradi - bunday oqimlarda majburan primary'dan o'qing yoki read-your-writes uchun sticky routing qo'llang. `@Transactional(readOnly = true)` ni faqat optimizatsiya deb o'ylab qo'yish xavfli: routing sozlanmagan bo'lsa u hech narsani ajratmaydi, sozlangan bo'lsa esa kutilmaganda yozuvni `SQLException` bilan yiqitadi.

## 10.29 Taqsimlangan lock (Distributed Lock - Redis, ShedLock, Database)

**Tavsif:** Bir nechta instance bir vaqtda ishlayotganda, faqat bittasi ma'lum bir critical section'ni bajarishi kerak bo'lsa, umumiy ombor (Redis, DB qatori, ZooKeeper) orqali mutual exclusion ta'minlanadi. Lock egasi TTL bilan belgilanadi, shunda instance qulasa lock avtomatik bo'shaydi. Eng keng tarqalgan ko'rinishi - cluster'da `@Scheduled` job'larning faqat bir marta ishga tushishini kafolatlash.

**Spring'da qayerda uchraydi:** Spring Integration'ning `LockRegistry` abstraksiyasi va uning realizatsiyalari: `RedisLockRegistry` (`spring-integration-redis`), `JdbcLockRegistry` (`spring-integration-jdbc`), `ZookeeperLockRegistry`. Scheduled job'lar uchun ShedLock (`net.javacrumbs.shedlock:shedlock-spring` + `shedlock-provider-jdbc-template` yoki `-redis-spring`) va `@SchedulerLock(name = "...", lockAtMostFor = "...")` annotatsiyasi de-fakto standart. Redisson (`redisson-spring-boot-starter`) `RLock` va Redlock algoritmini beradi; eng sodda variant - PostgreSQL'ning `SELECT ... FOR UPDATE SKIP LOCKED` yoki advisory lock'lari (`pg_try_advisory_lock`) `JdbcTemplate` orqali. Quartz'ning cluster rejimi ham JDBC jobStore orqali shu muammoni hal qiladi.

**Qo'llanish keyslari:**
- Kubernetes'da 5 ta pod ishlayotganda kunlik hisobot job'ini faqat bir marta bajarish.
- Outbox yoki notification queue'ni bir nechta worker bilan `SKIP LOCKED` orqali to'qnashuvsiz o'qish.
- Cache'ni qayta qurishda "cache stampede"ni oldini olish (faqat bitta instance qayta hisoblaydi).
- Migratsiya yoki schema update skriptini cluster'da bitta instance ishga tushirishi (Liquibase/Flyway lock).
- Tashqi API'ning rate limit'ini butun cluster bo'yicha markazlashtirib boshqarish.

**Ehtiyot bo'ling:** Redis asosidagi lock - correctness kafolati emas, balki optimizatsiya: network partition, GC pauza yoki clock drift tufayli ikki instance bir vaqtda o'zini lock egasi deb hisoblashi mumkin, shuning uchun pul va buxgalteriyaga tegishli invariantlarni DB constraint yoki idempotentlik bilan himoyalang. `lockAtMostFor`ni job'ning real davomiyligidan kattaroq qo'ying, aks holda lock ish tugamasdan bo'shab, parallel bajarilish yuzaga keladi.

## 10.30 Idempotentlik ombori (Idempotency Store)

**Tavsif:** Takroriy so'rov yoki xabar bir necha marta kelganda ham effekt faqat bir marta qo'llanishini kafolatlash uchun bajarilgan operatsiyalarning kaliti (idempotency key, message id) alohida omborda saqlanadi. Yangi so'rov kelganda kalit tekshiriladi: mavjud bo'lsa, qayta bajarish o'rniga saqlangan natija qaytariladi. Bu at-least-once yetkazib berish semantikasini amalda exactly-once ga aylantiradi.

**Spring'da qayerda uchraydi:** HTTP tomonida `Idempotency-Key` header'ini o'qiydigan `HandlerInterceptor` yoki `OncePerRequestFilter`, so'ng kalit va javobni jadvalga unique constraint bilan yozish - `DataIntegrityViolationException` tushsa, bu dublikat demak. Spring Integration `IdempotentReceiverInterceptor` va `MetadataStore` (`RedisMetadataStore`, `JdbcMetadataStore`) bilan tayyor "Idempotent Receiver" beradi; Kafka iste'molchilarida `@KafkaListener` ichida `consumed_messages` jadvaliga `message_id` yozib, uni biznes o'zgarishi bilan bir `@Transactional` ichida commit qilish eng ishonchli usul. Kafka producer tomonida `enable.idempotence=true` va `spring.kafka.producer.transaction-id-prefix` broker darajasidagi dublikatlarni kamaytiradi; Redis'da `SET key NX EX` oddiy, lekin TTL cheklovli variant.

**Qo'llanish keyslari:**
- To'lov yaratish API'sida kliyent retry qilganda ikki marta pul yechilishini oldini olish.
- Kafka/RabbitMQ'dan at-least-once kelgan buyurtma event'ini ikki marta qayta ishlamaslik.
- Webhook qabul qiluvchi endpoint'da provayderning takroriy yuborishlarini filtrlash (Stripe, bank callback'lari).
- Mobil ilovada tarmoq uzilganda qayta yuborilgan "submit" tugmasi so'rovini bitta buyurtmaga aylantirish.
- Batch import'da bir xil fayl ikki marta yuklanganda yozuvlar dublikatlanmasligi.

**Ehtiyot bo'ling:** Idempotentlik yozuvi va biznes o'zgarishi bir atomik tranzaksiyada bo'lmasa, pattern buziladi - alohida Redis'ga yozish "yozildi, lekin biznes qulaganda" holatini yaratadi. Kalitni kliyent generatsiya qilishi, uni so'rov payload'i bilan bog'lab tekshirish (bir xil kalit bilan boshqa summa kelsa xato qaytarish) va TTL'ni retry oynasidan uzunroq tanlash kerak.

## 10.31 Dual Write muammosi (Dual Write Problem)

**Tavsif:** Ilova bir operatsiya ichida ikki xil tizimga (masalan, ma'lumotlar bazasi va Kafka, yoki DB va Elasticsearch) mustaqil yozganda, biri muvaffaqiyatli, ikkinchisi muvaffaqiyatsiz bo'lishi mumkin - natijada tizimlar orasida doimiy nomuvofiqlik paydo bo'ladi. Bu pattern emas, balki anti-pattern: uning yechimi yozishni bitta atomik manbaga (DB) jamlab, ikkinchi tizimga Transactional Outbox yoki Change Data Capture orqali asinxron tarqatishdir. Boshqa yo'l - event store'ni yagona haqiqat manbai qilib olish (Event Sourcing).

**Spring'da qayerda uchraydi:** Tipik buzuq kod - `@Transactional` metod ichida `repository.save(...)` dan keyin darhol `kafkaTemplate.send(...)` chaqirilishi: tranzaksiya rollback bo'lsa ham xabar allaqachon ketgan bo'ladi. To'g'ri yechimlar: outbox jadvaliga yozib, Debezium (Kafka Connect) yoki `@Scheduled` publisher bilan jo'natish; `@TransactionalEventListener(phase = AFTER_COMMIT)` bilan hech bo'lmaganda "rollback'dan keyin yuborish"ni oldini olish (lekin bu hamon yo'qotish riskini qoldiradi); Spring'ning `ChainedTransactionManager` esa deprecated va atomiklik bermaydi. Spring Modulith (`spring-modulith-events-jpa` / `-kafka`) event publication registry bilan tayyor outbox mexanizmini beradi, bu Spring Boot 3.x loyihalarida eng qulay variant.

**Qo'llanish keyslari:**
- Buyurtma saqlangandan keyin `OrderCreated` event'ini ishonchli tarzda Kafka'ga chiqarish.
- DB'dagi mahsulot o'zgarishini Elasticsearch index'i bilan sinxron ushlab turish (CDC orqali).
- Audit log'ni tashqi SIEM tizimiga yo'qotishsiz yetkazish.
- Cache invalidation xabarini faqat haqiqatan commit bo'lgan o'zgarishlar uchun yuborish.
- Legacy monolitdan yangi mikroservisga ma'lumotni real vaqtda ko'chirish (Debezium bilan strangler migratsiyasi).

**Ehtiyot bo'ling:** `@TransactionalEventListener(AFTER_COMMIT)` ni to'liq yechim deb o'ylash eng keng tarqalgan xato - commit bo'lib, keyin JVM qulasa, event abadiy yo'qoladi; faqat davomli (durable) outbox yoki CDC kafolat beradi. Shuningdek, outbox iste'molchisi at-least-once ishlaganini unutmang: qabul qiluvchi tomonda idempotentlik va event tartibini (per-aggregate partition key) albatta ta'minlang.

---

[&larr; 9. Ma'lumotlarga kirish va ORM patternlari](09-malumotlarga-kirish-va-orm-patternlari.md) · [Mundarija](README.md) · [11. Keshlash patternlari &rarr;](11-keshlash-patternlari.md)
