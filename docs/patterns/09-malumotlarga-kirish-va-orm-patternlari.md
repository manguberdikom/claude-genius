<!-- doc: patterns | chapter: 9 | part:  -->

[Java Spring arxitektori bilishi kerak bo'lgan barcha dizayn patternlar](../../README.md) / [Dizayn patternlar](README.md)

# 9. Ma'lumotlarga kirish va ORM patternlari (Data Access & ORM Patterns)

<details>
<summary>Bu bo'limdagi 37 bo'lim</summary>

- [9.1 Ma'lumotlarga kirish obyekti (Data Access Object - DAO)](#91-malumotlarga-kirish-obyekti-data-access-object---dao)
- [9.2 Repository (Repository - Spring Data)](#92-repository-repository---spring-data)
- [9.3 Jadval ma'lumotlari shlyuzi (Table Data Gateway)](#93-jadval-malumotlari-shlyuzi-table-data-gateway)
- [9.4 Satr ma'lumotlari shlyuzi (Row Data Gateway)](#94-satr-malumotlari-shlyuzi-row-data-gateway)
- [9.5 Faol yozuv (Active Record)](#95-faol-yozuv-active-record)
- [9.6 Ma'lumot mapper'i (Data Mapper)](#96-malumot-mapperi-data-mapper)
- [9.7 Ish birligi (Unit of Work - persistence context)](#97-ish-birligi-unit-of-work---persistence-context)
- [9.8 Identifikatsiya xaritasi (Identity Map - first-level cache)](#98-identifikatsiya-xaritasi-identity-map---first-level-cache)
- [9.9 Kechiktirilgan yuklash (Lazy Load - proxy, ghost, value holder)](#99-kechiktirilgan-yuklash-lazy-load---proxy-ghost-value-holder)
- [9.10 Identifikator maydoni (Identity Field)](#910-identifikator-maydoni-identity-field)
- [9.11 Tashqi kalit mapping'i (Foreign Key Mapping)](#911-tashqi-kalit-mappingi-foreign-key-mapping)
- [9.12 Assotsiatsiya jadvali mapping'i (Association Table Mapping)](#912-assotsiatsiya-jadvali-mappingi-association-table-mapping)
- [9.13 Qaram Maplash (Dependent Mapping)](#913-qaram-maplash-dependent-mapping)
- [9.14 Ichki O'rnatilgan Qiymat (Embedded Value)](#914-ichki-ornatilgan-qiymat-embedded-value)
- [9.15 Serializatsiyalangan LOB (Serialized LOB)](#915-serializatsiyalangan-lob-serialized-lob)
- [9.16 Yagona Jadval Merosi (Single Table Inheritance)](#916-yagona-jadval-merosi-single-table-inheritance)
- [9.17 Sinf Jadvallari Merosi (Class Table Inheritance / JOINED)](#917-sinf-jadvallari-merosi-class-table-inheritance--joined)
- [9.18 Konkret Jadval Merosi (Concrete Table Inheritance / TABLE_PER_CLASS)](#918-konkret-jadval-merosi-concrete-table-inheritance--table_per_class)
- [9.19 Meros Mapper'lari (Inheritance Mappers)](#919-meros-mapperlari-inheritance-mappers)
- [9.20 Metama'lumot Maplash (Metadata Mapping)](#920-metamalumot-maplash-metadata-mapping)
- [9.21 So'rov Obyekti (Query Object)](#921-sorov-obyekti-query-object)
- [9.22 DTO Proyeksiyasi (DTO Projection)](#922-dto-proyeksiyasi-dto-projection)
- [9.23 Optimistik Oflayn Qulf (Optimistic Offline Lock)](#923-optimistik-oflayn-qulf-optimistic-offline-lock)
- [9.24 Pessimistik Oflayn Qulf (Pessimistic Offline Lock)](#924-pessimistik-oflayn-qulf-pessimistic-offline-lock)
- [9.25 Yirik donali qulf (Coarse-Grained Lock)](#925-yirik-donali-qulf-coarse-grained-lock)
- [9.26 Yashirin qulf (Implicit Lock)](#926-yashirin-qulf-implicit-lock)
- [9.27 N+1 muammosi yechimlari (N+1 Problem Solutions)](#927-n1-muammosi-yechimlari-n1-problem-solutions)
- [9.28 View ichida ochiq sessiya - antipattern (Open Session in View)](#928-view-ichida-ochiq-sessiya---antipattern-open-session-in-view)
- [9.29 Faqat o'qish uchun tranzaksiyalar (Read-only Transactions)](#929-faqat-oqish-uchun-tranzaksiyalar-read-only-transactions)
- [9.30 Connection Pool (Connection Pool - HikariCP)](#930-connection-pool-connection-pool---hikaricp)
- [9.31 Natural va surrogate kalit (Natural vs Surrogate Key)](#931-natural-va-surrogate-kalit-natural-vs-surrogate-key)
- [9.32 ID generatsiyasi (ID Generation - SEQUENCE, IDENTITY, UUIDv7, TSID, Hi/Lo)](#932-id-generatsiyasi-id-generation---sequence-identity-uuidv7-tsid-hilo)
- [9.33 Hibernate flush rejimlari va dirty checking (Hibernate Flush Modes & Dirty Checking)](#933-hibernate-flush-rejimlari-va-dirty-checking-hibernate-flush-modes--dirty-checking)
- [9.34 Spring Data JDBC aggregate-yo'naltirilgan mapping (Spring Data JDBC Aggregate-Oriented Mapping)](#934-spring-data-jdbc-aggregate-yonaltirilgan-mapping-spring-data-jdbc-aggregate-oriented-mapping)
- [9.35 Spetsifikatsiya (Specification - Spring Data JPA)](#935-spetsifikatsiya-specification---spring-data-jpa)
- [9.36 Domen ombori (Domain Store)](#936-domen-ombori-domain-store)
- [9.37 Yozuvlar to'plami (Record Set)](#937-yozuvlar-toplami-record-set)

</details>



Ma'lumotlarga kirish va ORM patternlari - domen modeli bilan relyatsion ma'lumotlar bazasi o'rtasidagi "impedance mismatch"ni boshqarish uchun ishlab chiqilgan patternlar to'plami. Ular obyektlar grafigi, tranzaksiya chegaralari, identifikatsiya va kechiktirilgan yuklash kabi muammolarni tartibga soladi. Arxitektor uchun bu patternlarni bilish shuning uchun muhim: Spring Data va Hibernate kabi freymvorklar ularni allaqachon ichki implementatsiya qilgan, va ularning ishlash mexanizmini tushunmaslik N+1 query, detached entity, lazy initialization exception va kutilmagan dirty checking kabi production muammolariga olib keladi. Shu bo'limdagi patternlar "freymvork nima qilayotganini" ko'rish imkonini beradi - ya'ni abstraksiya ostidagi mexanizmni.

## 9.1 Ma'lumotlarga kirish obyekti (Data Access Object - DAO)

**Tavsif:** DAO persistence logikasini alohida obyekt ichiga kapsulalaydi va biznes qatlamga faqat domen-orientirlangan interfeys taqdim etadi. Chaqiruvchi kod SQL, JDBC `Connection`, `ResultSet` yoki JPQL bilan hech qachon to'g'ridan-to'g'ri ishlamaydi. Bu ma'lumotlar manbasini (RDBMS, NoSQL, tashqi API) almashtirish imkonini beradi va persistence texnologiyasini biznes qoidalardan ajratadi.

**Spring'da qayerda uchraydi:** `@Repository` annotatsiyasi bilan belgilangan sinflar; `PersistenceExceptionTranslationPostProcessor` ularni o'rab, vendor-specific exception'larni Spring'ning `DataAccessException` ierarxiyasiga tarjima qiladi. Implementatsiya uchun `JdbcTemplate`, `NamedParameterJdbcTemplate`, `JdbcClient` (Spring Framework 6.1+), yoki JPA `EntityManager` `@PersistenceContext` orqali inyeksiya qilinadi. Spring Framework 6.x/7.x'da `JdbcClient` fluent API eng zamonaviy variant hisoblanadi.

**Qo'llanish keyslari:**
- Legacy stored procedure'larga asoslangan tizimlarda `SimpleJdbcCall` orqali protsedura chaqiruvlarini kapsulalash.
- Hisobot va analytics uchun murakkab native SQL query'larni domen interfeysi ortida yashirish.
- Ikki xil ma'lumot manbasi (masalan Oracle va Elasticsearch) uchun bir xil interfeysning ikki implementatsiyasini berish.
- Unit test'da DAO interfeysini mock qilib, service qatlamini DB'siz sinash.
- Multi-tenant tizimda tenant filtrini DAO ichida markazlashtirib qo'llash.

**Ehtiyot bo'ling:** Spring Data JPA mavjud bo'lgan loyihada har bir entity uchun qo'lda DAO yozish ortiqcha boilerplate keltiradi - bu holda `Repository` patternini tanlang. Shuningdek DAO'ni "anemic passthrough" ga aylantirmang: agar metodlar faqat `em.find()` ni o'raydigan bo'lsa, qatlam qiymat qo'shmaydi.

## 9.2 Repository (Repository - Spring Data)

**Tavsif:** Repository domen obyektlari to'plamini xuddi in-memory kolleksiya kabi taqdim etadi va query mantiqini deklarativ ifodalash imkonini beradi. DAO'dan farqi - u persistence texnologiyasiga emas, domen aggregate'iga yo'naltirilgan va DDD kontekstida aggregate root uchun yagona kirish nuqtasi bo'lib xizmat qiladi. Spring Data bu patternni interfeys deklaratsiyasidan runtime'da proxy generatsiya qilib amalga oshiradi.

**Spring'da qayerda uchraydi:** `Repository`, `CrudRepository`, `ListCrudRepository`, `PagingAndSortingRepository`, `JpaRepository` interfeyslari; `@EnableJpaRepositories` yoki Spring Boot 3.x/4.x auto-configuration orqali yoqiladi. Query derivation (`findByLastNameAndActiveTrue`), `@Query` (JPQL yoki `nativeQuery = true`), `@Modifying`, `Specification<T>` (JPA Criteria API ustida), `Pageable`/`Slice`/`Window`, va `@EntityGraph` mavjud. Spring Data JPA 3.x'da `JpaSpecificationExecutor`, projection interfeyslari va `ScrollPosition` bilan keyset pagination qo'llaniladi.

**Qo'llanish keyslari:**
- Standart CRUD + paginatsiya kerak bo'lgan entity'lar uchun kodsiz repository olish.
- `Specification` yoki Querydsl orqali foydalanuvchi tanlagan dinamik filtrlardan query qurish.
- DTO projection interfeysi bilan faqat kerakli ustunlarni tanlab, tarmoq va heap yukini kamaytirish.
- Katta eksport uchun `Stream<T>` qaytaruvchi metod yoki `ScrollPosition` bilan keyset pagination qilish.
- `@EntityGraph` orqali ma'lum use-case uchun fetch planni aniq belgilash va N+1'dan qochish.

**Ehtiyot bo'ling:** Query derivation nomlari 5-6 shartdan oshsa o'qilmaydigan bo'ladi - bunday hollarda `@Query` yoki `Specification` ishlating. Shuningdek `findAll()` ni production'da filtrlarsiz chaqirish va `@Transactional` ni faqat repository darajasida qoldirish (service'da emas) tipik xato: aggregate bo'ylab atomarlik buziladi.

## 9.3 Jadval ma'lumotlari shlyuzi (Table Data Gateway)

**Tavsif:** Bitta jadval (yoki view) uchun barcha SQL operatsiyalarini o'z ichiga oladigan yagona obyekt. U domen obyektlarini qaytarmaydi, balki primitiv qiymatlar, `Map` yoki record/DTO ko'rinishidagi natijalar bilan ishlaydi va har bir metod bitta SQL bayonotiga mos keladi. Bu pattern jadval sxemasi bilan kod o'rtasida yupqa, oldindan aytib bo'ladigan qatlam yaratadi.

**Spring'da qayerda uchraydi:** `JdbcTemplate` / `JdbcClient` asosida yozilgan gateway sinflari; `RowMapper`, `DataClassRowMapper` (Java record'lar uchun), `BeanPropertyRowMapper`, `ResultSetExtractor` natijani mapping qiladi. Yozish uchun `SimpleJdbcInsert` (`usingGeneratedKeyColumns`) va `batchUpdate` qo'llaniladi. jOOQ generatsiya qilgan `TableRecord`/DAO sinflari ham aynan shu patternning sanoat implementatsiyasi hisoblanadi.

**Qo'llanish keyslari:**
- Reporting va read-model jadvallarini ORM'siz, aniq SQL bilan o'qish.
- ETL/batch yuklash vazifasida `batchUpdate` orqali minglab satrni tez insert qilish.
- Audit yoki outbox jadvali kabi domen modeliga tegishli bo'lmagan texnik jadvallarga kirish.
- Legacy sxemadagi kompozit kalitli, ORM'ga mos kelmaydigan jadvallar bilan ishlash.
- Hibernate second-level cache'ni chetlab o'tib, aniq va yangi ma'lumot kerak bo'lgan query'larni bajarish.

**Ehtiyot bo'ling:** Bu pattern boy domen mantiqini qo'ymaslik uchun - agar gateway ichida biznes qoidalari ko'paysa, Data Mapper + domen modeliga o'tish kerak. Shuningdek bir xil JPA entity va gateway bir tranzaksiyada bir jadvalga yozsa, persistence context stale bo'lib qolishi mumkin.

## 9.4 Satr ma'lumotlari shlyuzi (Row Data Gateway)

**Tavsif:** Jadvalning bitta satriga mos keladigan obyekt: har bir ustun - maydon, qo'shimcha ravishda `insert()`, `update()`, `delete()` metodlari mavjud. Table Data Gateway'dan farqi shundaki, bu yerda bitta instance bitta satrni ifodalaydi va uning identifikatsiyasi aniq. Biznes mantiqi bu obyektda emas, alohida service yoki domen sinfida qoladi.

**Spring'da qayerda uchraydi:** Spring'da tayyor abstraksiya yo'q - odatda Java `record` yoki POJO + `RowMapper` juftligi bilan qo'lda yoziladi, saqlash esa `JdbcClient`/`SimpleJdbcInsert` orqali bajariladi. jOOQ'ning `UpdatableRecord` (`store()`, `delete()`, `refresh()` metodlari bilan) bu patternning aniq va keng tarqalgan implementatsiyasi. MyBatis mapper + plain DTO kombinatsiyasi ham shu ko'rinishga yaqin.

**Qo'llanish keyslari:**
- Konfiguratsiya yoki lookup jadvallarining alohida satrlarini o'qib-yozish.
- jOOQ'da generatsiya qilingan record'lar bilan tez CRUD skriptlari yozish.
- Migratsiya utilitasida satrni o'qib, o'zgartirib, darhol qaytarib yozish.
- Legacy jadvalga yupqa, ORM yuklamasi yo'q qatlam kerak bo'lgan integratsiya moduli.
- Feature-flag yoki counter satrini atomar `UPDATE ... WHERE version = ?` bilan yangilash.

**Ehtiyot bo'ling:** Satr-satr `update()` chaqiruvlari katta hajmda juda sekin ishlaydi - batch operatsiya kerak bo'lsa Table Data Gateway'ga o'ting. Bundan tashqari bu obyektga domen metodlari qo'shilsa, u beixtiyor Active Record'ga aylanadi va sinov qilish qiyinlashadi.

## 9.5 Faol yozuv (Active Record)

**Tavsif:** Obyekt ham ma'lumotlarni (jadval satri), ham ular ustidagi biznes mantiqni, ham persistence metodlarini (`save`, `delete`) o'zida birlashtiradi. Bu CRUD-ustun loyihalarda juda tez natija beradi, chunki alohida repository qatlami talab qilinmaydi. Kamchiligi - domen modeli ma'lumotlar bazasi sxemasiga qattiq bog'lanib qoladi.

**Spring'da qayerda uchraydi:** Java'da to'liq Active Record kam qo'llaniladi, lekin Spring Data JDBC/JPA entity'siga `save` mantiqini kiritish yoki Hibernate'ning deprecated `ManagedEntity`/`LifecycleCallback` yondashuvlari shu yo'nalishda. Eng aniq misol - Kotlin/Java loyihalarida Spring Data Kotlin extension'lari va Hibernate 6.x `StatelessSession` ustida qurilgan yordamchi metodlar; Groovy ekotizimida GORM (`Book.get(1)`, `book.save()`) bu patternning sof ko'rinishi.

**Qo'llanish keyslari:**
- Prototip yoki internal admin tool'da tez CRUD ekranlarini yozish.
- Kichik microservice'da bitta-ikkita entity bo'lsa, qatlamlar sonini kamaytirish.
- Migratsiya skriptlari va bir martalik data-fix utilitalari.
- Domen mantiqi juda yupqa bo'lgan lookup/reference ma'lumotlar moduli.

**Ehtiyot bo'ling:** Entity ichida `save()` chaqirish uchun unga `EntityManager` yoki static locator kerak bo'ladi - bu testlashni va dependency injection'ni buzadi. Murakkab domen qoidalari, bir nechta aggregate va bounded context mavjud tizimlarda bu patterndan voz kechib, Data Mapper + Repository'ni tanlang.

## 9.6 Ma'lumot mapper'i (Data Mapper)

**Tavsif:** Domen obyektlari va ma'lumotlar bazasi o'rtasida ikki tomonlama o'zgartirishni bajaradigan mustaqil qatlam. Domen obyekti persistence haqida hech narsa bilmaydi - u na SQL, na session, na jadval nomlarini ko'radi. Bu domen modelini sxemadan to'liq ajratadi va ikkisini mustaqil evolyutsiya qilish imkonini beradi.

**Spring'da qayerda uchraydi:** JPA/Hibernate'ning o'zi - eng mashhur Data Mapper implementatsiyasi: `EntityManager`, `@Entity`, `@Table`, `@Column`, `@Embeddable`, `AttributeConverter`, `@Converter`. Spring Data JDBC ham mapper yondashuviga asoslangan (`JdbcAggregateTemplate`, `NamingStrategy`, `@MappedCollection`). MyBatis'ning XML/annotatsiya mapper'lari va MapStruct (`@Mapper`, compile-time generatsiya) DTO-domen mapping uchun ishlatiladi.

**Qo'llanish keyslari:**
- Legacy sxema bilan toza DDD domen modelini bog'lash (`@Embedded` value object'lar bilan).
- `AttributeConverter` orqali domen value type'ini (masalan `Money`, `EmailAddress`) ustun turiga o'girish.
- Bitta jadvalni bir nechta domen obyektiga yoki bir obyektni bir nechta jadvalga (`@SecondaryTable`) mapping qilish.
- Read-model DTO'larini MapStruct bilan compile-time, reflection'siz generatsiya qilish.
- Sxema o'zgarganda domen kodini o'zgartirmasdan faqat mapping metadatasini yangilash.

**Ehtiyot bo'ling:** Mapping metadatasi (annotatsiyalar) domen sinfiga tushib qolsa, "ajratish" faqat nomigagina bo'ladi - `orm.xml` yoki alohida persistence model bu holda yaxshiroq. Shuningdek chuqur obyekt grafiklarini avtomatik mapping qilishga ishonib, fetch strategiyasini e'tibordan chetda qoldirmang.

## 9.7 Ish birligi (Unit of Work - persistence context)

**Tavsif:** Biznes tranzaksiyasi davomida o'zgargan barcha obyektlarni kuzatib boradi va yozish operatsiyalarini commit vaqtiga qadar jamlab turadi. Keyin ularni to'g'ri tartibda, minimal sonli SQL bayonotlari bilan bazaga yuboradi. Bu tranzaksion yaxlitlikni ta'minlaydi va DB bilan aloqa sonini keskin kamaytiradi.

**Spring'da qayerda uchraydi:** JPA `EntityManager` persistence context'i aynan shu pattern: dirty checking, `flush()`, `FlushModeType`, `@Transactional` chegarasidagi avtomatik flush-before-commit. Spring tomonida `PlatformTransactionManager`, `JpaTransactionManager`, `TransactionSynchronizationManager`, `@Transactional(propagation, isolation, readOnly)` boshqaradi. Hibernate 6.x `Session`, `ActionQueue`, va `hibernate.jdbc.batch_size`/`order_inserts`/`order_updates` sozlamalari yozishni guruhlaydi.

**Qo'llanish keyslari:**
- Bir service metodida bir necha entity'ni o'zgartirib, hammasini bitta atomar commit bilan saqlash.
- `hibernate.jdbc.batch_size` + `order_inserts` bilan ommaviy insert'ni batch'ga aylantirish.
- `@Transactional(readOnly = true)` bilan dirty checking va flush'ni o'chirib, read query'larni tezlashtirish.
- Optimistik locking (`@Version`) bilan bir vaqtda yozishni aniqlash va konfliktni qaytarish.
- Domain event'larni `TransactionSynchronization`/`@TransactionalEventListener(AFTER_COMMIT)` orqali commit'dan keyin chiqarish.

**Ehtiyot bo'ling:** Katta hajmli batch'da persistence context cheksiz o'sadi va `OutOfMemoryError` keltiradi - har N satrdan keyin `flush()` + `clear()` qiling yoki Hibernate `StatelessSession` ishlating. Shuningdek `@Transactional` ni bir sinf ichidagi self-invocation bilan chaqirish proxy'ni chetlab o'tadi va tranzaksiya umuman boshlanmaydi.

## 9.8 Identifikatsiya xaritasi (Identity Map - first-level cache)

**Tavsif:** Bitta tranzaksiya ichida har bir ma'lumot bazasi satri uchun xotirada aynan bitta obyekt instance'i bo'lishini kafolatlaydi. Takroriy `find()` chaqiruvlari bazaga bormasdan, xaritadan qaytariladi va shu bilan ortiqcha query'lar yo'qoladi. Bundan tashqari bu obyekt identifikatsiyasini (`==` taqqoslash) va dirty checking'ni to'g'ri ishlashini ta'minlaydi.

**Spring'da qayerda uchraydi:** JPA persistence context'ining first-level cache'i - `EntityManager.find()` birinchi marta SQL yuboradi, keyingi chaqiruvlar cache'dan qaytadi; `em.clear()`, `em.detach()`, `em.refresh()` bu xaritani boshqaradi. Hibernate 6.x'da bu `StatefulPersistenceContext` sinfi orqali amalga oshirilgan. Second-level cache alohida: `@Cacheable` (JPA/Hibernate), `hibernate.cache.use_second_level_cache` va Ehcache/Infinispan provider'lari.

**Qo'llanish keyslari:**
- Bir tranzaksiyada bir xil referens entity'ga ko'p murojaat qilinadigan hisob-kitob mantiqi.
- Graf bo'ylab yurganda bir obyektga turli yo'llardan kelib, bir xil instance olish.
- `em.getReference()` bilan faqat FK qiymatini o'rnatish uchun query'siz proxy olish.
- Batch jarayonida `clear()` chaqirib, xotirani ataylab bo'shatish.

**Ehtiyot bo'ling:** First-level cache faqat primary key bo'yicha ishlaydi - JPQL query har safar DB'ga boradi, lekin natijani cache'dagi (ehtimol o'zgargan) instance bilan birlashtiradi, bu kutilmagan natija berishi mumkin. Native SQL bilan to'g'ridan-to'g'ri `UPDATE` qilsangiz, cache stale bo'lib qoladi - `@Modifying(clearAutomatically = true, flushAutomatically = true)` kerak bo'ladi.

## 9.9 Kechiktirilgan yuklash (Lazy Load - proxy, ghost, value holder)

**Tavsif:** Obyektning barcha ma'lumotlarini darhol yuklamasdan, haqiqatan kerak bo'lgan paytda bazadan olib keladi. Uch asosiy varianti bor: proxy (haqiqiy obyekt o'rniga stub), ghost (identifikatori bor, bo'sh obyekt, birinchi getter'da to'ladi) va value holder (o'rash obyekti ichidagi qiymat). Bu dastlabki yuklash vaqtini va xotirani keskin kamaytiradi.

**Spring'da qayerda uchraydi:** JPA `FetchType.LAZY` (`@ManyToOne`, `@OneToOne`, `@ManyToMany`, `@OneToMany` - oxirgi ikkisi default LAZY); Hibernate 6.x ByteBuddy orqali proxy generatsiya qiladi, `PersistentBag`/`PersistentSet` kolleksiya wrapper'lari value holder rolini o'ynaydi. `@Basic(fetch = LAZY)` + bytecode enhancement (`hibernate-enhance-maven-plugin`) atribut darajasida lazy loading beradi; `Hibernate.initialize()`, `Hibernate.isInitialized()` va `@EntityGraph`/`JOIN FETCH` boshqarish vositalari.

**Qo'llanish keyslari:**
- Katta `@Lob` maydonni (hujjat, rasm) faqat so'ralganda o'qish.
- Keng aggregate'da kam ishlatiladigan kolleksiyalarni (audit log, izohlar) kerak bo'lganda yuklash.
- Faqat FK qiymati kerak bo'lganda `getReference()` proxy'si bilan query'dan butunlay qochish.
- Ro'yxat ekranida yengil projection, detail ekranida `@EntityGraph` bilan to'liq graf olish.

**Ehtiyot bo'ling:** Tranzaksiya yopilgandan keyin lazy maydonga murojaat `LazyInitializationException` beradi - bu muammoni `spring.jpa.open-in-view=true` bilan yashirmang, chunki u N+1 query'larni controller qatlamiga ko'chiradi. Entity'ni to'g'ridan-to'g'ri JSON'ga serializatsiya qilish esa butun grafni beixtiyor yuklab yuboradi; DTO ishlating.

## 9.10 Identifikator maydoni (Identity Field)

**Tavsif:** Domen obyektida ma'lumotlar bazasi primary key'ini saqlovchi maydon - shu orqali xotiradagi obyekt va DB satri o'rtasida bog'liqlik o'rnatiladi. Kalit tabiiy (natural), sun'iy (surrogate), oddiy yoki kompozit bo'lishi mumkin, va uni generatsiya qilish strategiyasi tizim unumdorligiga sezilarli ta'sir qiladi. Identifikator `equals`/`hashCode` semantikasini ham belgilaydi.

**Spring'da qayerda uchraydi:** `@Id`, `@GeneratedValue(strategy = IDENTITY | SEQUENCE | TABLE | UUID | AUTO)`, `@SequenceGenerator`, `@EmbeddedId` + `@Embeddable`, `@IdClass`. Hibernate 6.x'da `@GeneratedValue(strategy = GenerationType.UUID)` standart, `SequenceStyleGenerator` esa `allocationSize` bilan pooled optimizer beradi. Spring Data'da `Persistable<ID>` interfeysi yangi/mavjud entity'ni ajratish uchun, `@Version` esa optimistik locking uchun ishlatiladi.

**Qo'llanish keyslari:**
- PostgreSQL/Oracle'da `SEQUENCE` + `allocationSize=50` bilan batch insert'ni haqiqatan batch qilish.
- Distributed tizimda ID'ni client tomonda generatsiya qilish uchun UUIDv7 yoki ULID ishlatish.
- Legacy sxemadagi kompozit kalitni `@EmbeddedId` orqali mapping qilish.
- `equals`/`hashCode` ni business key bo'yicha yozib, transient entity'larni `Set` ichida to'g'ri ishlashini ta'minlash.
- `@Version` bilan konkurent tahrirlashda "lost update"ni oldini olish.

**Ehtiyot bo'ling:** `GenerationType.IDENTITY` Hibernate'da JDBC batch insert'ni o'chiradi, chunki har insert'dan keyin generatsiya qilingan kalit o'qilishi kerak - ommaviy yozishda `SEQUENCE` tanlang. Tasodifiy UUIDv4'ni clustered primary key qilish esa index fragmentatsiyasi va yozish unumdorligi pasayishiga olib keladi.

## 9.11 Tashqi kalit mapping'i (Foreign Key Mapping)

**Tavsif:** Obyektlar orasidagi bitta-ko'pga yoki bitta-bitta aloqani relyatsion jadvaldagi foreign key ustuni bilan bog'laydi. Mapper obyekt referensini FK qiymatiga va teskarisiga aylantiradi, bir tomonni "egasi" (owning side) deb belgilaydi. Bu aloqa yo'nalishi, cascade xatti-harakati va yuklash strategiyasini aniq belgilashni talab qiladi.

**Spring'da qayerda uchraydi:** `@ManyToOne` + `@JoinColumn(name = "...", nullable = false)`, teskari tomonda `@OneToMany(mappedBy = "...")`; `@OneToOne` uchun `@JoinColumn` yoki `@MapsId` (shared primary key). `CascadeType` (`PERSIST`, `MERGE`, `REMOVE`, `ALL`), `orphanRemoval = true`, `@OnDelete(action = CASCADE)` (Hibernate) xatti-harakatni boshqaradi. Spring Data JDBC'da esa aggregate ichidagi aloqalar `@MappedCollection(idColumn = "...")` orqali ifodalanadi.

**Qo'llanish keyslari:**
- `Order` → `OrderLine` aggregate'ini `@OneToMany(mappedBy, cascade = ALL, orphanRemoval = true)` bilan modellashtirish.
- `@MapsId` orqali `User` va `UserProfile` ni bir xil primary key ustida bog'lash.
- Bidirectional aloqada faqat owning side'ni yangilab, ortiqcha `UPDATE` bayonotlaridan qochish.
- Boshqa aggregate'ga faqat ID referens (`UUID customerId`) saqlab, bounded context chegarasini saqlash.
- `@ManyToOne(fetch = LAZY)` + `@EntityGraph` bilan use-case'ga mos fetch plan qurish.

**Ehtiyot bo'ling:** `mappedBy` ni unutib, ikki tomonni ham owning qilib qo'ysangiz, Hibernate ortiqcha `UPDATE` yuboradi yoki ikki xil FK ustuni kutadi. Bidirectional aloqada ikki tomonni kodda sinxron ushlab turish (`addLine()` helper metodi) majburiy - aks holda in-memory holat bazadagi holatdan chetga chiqadi.

## 9.12 Assotsiatsiya jadvali mapping'i (Association Table Mapping)

**Tavsif:** Ko'pga-ko'p aloqani alohida bog'lovchi (join) jadval orqali ifodalaydi: bu jadval har ikki tomonning foreign key'larini saqlaydi. Agar aloqaning o'zida atributlar bo'lsa (masalan sana, rol, miqdor), join jadvali to'liq entity'ga aylantiriladi. Bu relyatsion modelda ko'pga-ko'pni ifodalashning yagona to'g'ri yo'li.

**Spring'da qayerda uchraydi:** `@ManyToMany` + `@JoinTable(name, joinColumns, inverseJoinColumns)`; atributli aloqa uchun ikki `@ManyToOne` li alohida `@Entity` va `@EmbeddedId`/`@IdClass` kompozit kaliti. Oddiy qiymatlar kolleksiyasi uchun `@ElementCollection` + `@CollectionTable`. Hibernate 6.x'da `@ManyToMany` ni `Set` bilan ishlatish tavsiya etiladi, `@OrderColumn` esa tartiblangan `List` uchun.

```java
@Entity
class Enrollment {
    @EmbeddedId EnrollmentId id;
    @MapsId("studentId") @ManyToOne(fetch = FetchType.LAZY) Student student;
    @MapsId("courseId")  @ManyToOne(fetch = FetchType.LAZY) Course course;
    LocalDate enrolledAt;
    @Enumerated(EnumType.STRING) EnrollmentStatus status;
}
```

**Qo'llanish keyslari:**
- `User` ↔ `Role` kabi atributsiz, sodda ko'pga-ko'p aloqani `@ManyToMany` bilan mapping qilish.
- `Student` ↔ `Course` aloqasiga ro'yxatga olish sanasi kerak bo'lganda `Enrollment` entity'siga o'tish.
- Tag tizimida `@ElementCollection` bilan yengil string kolleksiyasini saqlash.
- Join jadvaliga `createdBy`/`createdAt` audit ustunlarini qo'shib, aloqa tarixini kuzatish.
- Ko'p a'zoli guruhlarda join jadvalini to'g'ridan-to'g'ri SQL bilan o'qib, N+1'dan qochish.

**Ehtiyot bo'ling:** `@ManyToMany` ustida `List` ishlatilsa, Hibernate bitta element o'chirishda butun aloqalar to'plamini `DELETE` qilib qaytadan `INSERT` qiladi - `Set` tanlang. Agar aloqaga kelajakda atribut qo'shilishi ehtimoli bo'lsa, boshidan alohida entity bilan modellashtiring, chunki keyinchalik migratsiya qilish qimmatga tushadi.

## 9.13 Qaram Maplash (Dependent Mapping)

**Tavsif:** Bir sinf o'z mavjudligi bilan boshqa sinfga butunlay bog'lanib qolganda (masalan, Order va OrderLine), qaram obyektning yuklanishi, saqlanishi va o'chirilishini mustaqil mapper emas, balki ota (owner) obyektning mapper'i boshqaradi. Bu yondashuv qaram tomon uchun alohida repository va o'z-o'zidan hayot tsikli (lifecycle) yaratishni bekor qiladi. Natijada agregat chegarasi (aggregate boundary) kod darajasida ham mustahkamlanadi: tashqi kod faqat ota obyekt orqali kiradi. Qaram obyektning identifikatori ko'pincha ota kalit bilan birgalikda ma'noga ega bo'ladi.

**Spring'da qayerda uchraydi:** JPA'da `@OneToMany(cascade = CascadeType.ALL, orphanRemoval = true)` va `@ElementCollection` aniq shu patternni amalga oshiradi - faqat ota entity uchun `JpaRepository` yaratiladi, bola uchun yaratilmaydi. Hibernate'ning `@OnDelete`, `@JoinColumn(nullable = false)` va Spring Data JDBC'ning agregat modeli (`AggregateReference`, root'ni saqlaganda bolalar avtomatik `DELETE`/`INSERT` qilinishi) ham shu mantiqqa asoslangan. Spring Data JDBC 3.x bu yondashuvni majburlaydi: bola jadvallari faqat root orqali boshqariladi.

**Qo'llanish keyslari:**
- `Order` → `OrderLine`: buyurtma satrlari buyurtmasiz mavjud bo'lmaydi va u bilan birga o'chadi.
- `Invoice` → `InvoiceItem`: hisob-faktura pozitsiyalari faqat hujjat ichida tahrirlanadi.
- `Survey` → `Question` → `AnswerOption`: so'rovnoma shakli yagona agregat sifatida saqlanadi.
- `Employee` → `Address` ro'yxati: `@ElementCollection` bilan ID'siz qiymat jadvali.
- `BlogPost` → `Comment` moderatsiya qilinmaydigan oddiy tizimda: post o'chsa, comment'lar ham ketadi.

**Ehtiyot bo'ling:** Agar qaram obyektga tashqi kontekstdan mustaqil murojaat kerak bo'lsa (alohida qidiruv, o'z audit tarixi, boshqa agregatdan FK), u allaqachon qaram emas - unga alohida repository va aggregate root kerak. `orphanRemoval` bilan katta kolleksiyalarni yuklash N+1 va ortiqcha `DELETE`larga olib keladi, shuning uchun minglab elementli kolleksiyalarni qaram maplash bilan boshqarmang.

---

## 9.14 Ichki O'rnatilgan Qiymat (Embedded Value)

**Tavsif:** Bir nechta ustunni mustaqil jadvalga chiqarmasdan, ularni domen tilida ma'noli bo'lgan yagona value object sifatida guruhlash imkonini beradi. Jadval tuzilishi o'zgarmaydi - obyekt maplanadi, ustunlar esa ota jadvalda qoladi. Bu primitive obsession muammosini yo'qotadi: `String street, String city, String zip` o'rniga `Address` tipi paydo bo'ladi, unga validatsiya va xatti-harakat (behavior) joylashtiriladi. Value object immutable va `equals`/`hashCode` qiymat bo'yicha solishtiriladigan bo'lishi kerak.

**Spring'da qayerda uchraydi:** JPA'da `@Embeddable` sinf va ota entity'da `@Embedded`, ustun nomlarini qayta yozish uchun `@AttributeOverride`/`@AttributeOverrides`, kompozit kalit uchun `@EmbeddedId`. Java 17+ `record` JPA 3.1'da to'g'ridan-to'g'ri `@Embeddable` bo'la olmaydi (no-arg constructor talab qilinadi), shu sababli odatda `final` maydonli oddiy sinf yoki Hibernate 6.x'ning `@Embeddable` + `@Immutable` kombinatsiyasi ishlatiladi; Hibernate 6.2+ esa `EmbeddableInstantiator` orqali record'ga yo'l beradi. Spring Data JDBC'da shu rolni `@Embedded(onEmpty = Embedded.OnEmpty.USE_NULL)` bajaradi.

**Qo'llanish keyslari:**
- `Money` (amount + currency) - narx, balans, chegirma maydonlari uchun yagona tip.
- `Address` (ko'cha, shahar, index) - `billingAddress` va `shippingAddress` sifatida `@AttributeOverride` bilan ikki marta.
- `DateRange` / `Period` (startDate + endDate) - shartnoma yoki bron muddati, ichida `overlaps()` metodi bilan.
- `PersonName` (ism, familiya, otasining ismi) - formatlash mantig'i bitta joyda.
- `GeoPoint` (latitude + longitude) - geo-qidiruv entity'larida.

**Ehtiyot bo'ling:** Embedded qiymat o'z identifikatoriga ega bo'lmaydi, shuning uchun uni ikki entity o'rtasida "ulash" (share) qilish mumkin emas - bir xil instance'ni ikki entity'ga bersangiz, Hibernate'da kutilmagan natija olasiz. `@Embedded` maydonining barcha ustunlari `NULL` bo'lsa, Hibernate ko'pincha butun obyektni `null` qiladi, bu esa `NullPointerException`ga olib keladi; `Optional` qaytaruvchi getter yoki null-object bilan himoyalaning.

---

## 9.15 Serializatsiyalangan LOB (Serialized LOB)

**Tavsif:** Murakkab obyekt grafini alohida jadvallarga normalizatsiya qilmasdan, uni yagona ustunda (BLOB yoki CLOB) serializatsiyalangan ko'rinishda saqlaydi. Agar ma'lumot faqat butunligicha o'qilsa va SQL bilan uning ichidan qidirish, agregatsiya qilish talab qilinmasa, bu yondashuv sxemani soddalashtiradi va JOIN'larni yo'qotadi. Format sifatida odatda JSON tanlanadi - u inson o'qiy oladigan va versiyalanishi osonroq. Bugungi kunda PostgreSQL `jsonb` kabi tiplar bu patternni "yarim-strukturali" darajaga olib chiqdi.

**Spring'da qayerda uchraydi:** Hibernate 6.x'da `@JdbcTypeCode(SqlTypes.JSON)` yoki `@JdbcTypeCode(SqlTypes.JSON_ARRAY)` standart yo'l (eski `io.hypersistence:hypersistence-utils` `@Type(JsonType.class)` o'rnida), `@Lob` esa xom BLOB/CLOB uchun. JPA `AttributeConverter` (`@Converter(autoApply = true)`) bilan Jackson `ObjectMapper` orqali qo'lda ham serializatsiya qilinadi. Spring Data MongoDB'da esa bu pattern tabiiy holat - hujjat ichidagi nested obyektlar.

```java
@Entity
class AuditEvent {
    @Id Long id;
    @JdbcTypeCode(SqlTypes.JSON)
    Map<String, Object> payload;   // PostgreSQL: jsonb
}
```

**Qo'llanish keyslari:**
- Audit log'da so'rov/javob snapshot'ini saqlash - faqat ko'rish uchun o'qiladi.
- Foydalanuvchi UI sozlamalari (dashboard layout, filtr presetlari) - sxemasi tez o'zgaradi.
- Tashqi API javobining xom (raw) nusxasini debug uchun saqlash.
- Workflow qadamlarining dinamik konfiguratsiyasi - har bir tip uchun alohida jadval yasash samarasiz.
- Feature flag yoki A/B test metadata'si entity bilan birga.

**Ehtiyot bo'ling:** LOB ichidagi ma'lumot bo'yicha hisobot, `GROUP BY` yoki indeksli qidiruv kerak bo'lsa, bu pattern tuzoqqa aylanadi - `jsonb` operatorlari (`->>`, GIN indeks) native query talab qiladi va portativlikni yo'qotadi. Java'ning `Serializable` binar formatini hech qachon ishlatmang: sinf o'zgarishi bilan eski yozuvlar o'qilmay qoladi va deserializatsiya xavfsizlik zaifligi (RCE) hisoblanadi.

---

## 9.16 Yagona Jadval Merosi (Single Table Inheritance)

**Tavsif:** Butun meros ierarxiyasi bitta jadvalga joylashtiriladi; qaysi konkret sinf ekanligini discriminator ustuni ko'rsatadi. JOIN'lar bo'lmaganligi uchun bu strategiya o'qish va polimorf so'rovlar bo'yicha eng tez variant. Subclass'larga tegishli maydunlar jadvalda `NULL` bo'lib qoladi, shuning uchun ularga `NOT NULL` qo'yib bo'lmaydi. JPA'ning default strategiyasi aynan shu.

**Spring'da qayerda uchraydi:** `@Inheritance(strategy = InheritanceType.SINGLE_TABLE)` (default), `@DiscriminatorColumn(name = "payment_type", discriminatorType = DiscriminatorType.STRING)` va subclass'larda `@DiscriminatorValue("CARD")`. Hibernate 6.x'da `@DiscriminatorFormula` bilan mavjud ustunlardan discriminator hisoblash, hamda `TREAT(... AS ...)` JPQL operatori va Criteria API'ning `CriteriaBuilder.treat()` metodi orqali subtype bo'yicha filtrlash mumkin. Spring Data'da bitta `JpaRepository<Payment, Long>` butun ierarxiyani qaytaradi, `@Query` bilan `TYPE(p) = CardPayment` shartini qo'shish mumkin.

**Qo'llanish keyslari:**
- `Payment` → `CardPayment`, `BankTransferPayment`, `CryptoPayment`: subclass'lar 1-3 ta qo'shimcha maydonga ega.
- `Notification` → `EmailNotification`, `SmsNotification`, `PushNotification`: umumiy navbatdan polimorf o'qish.
- `Event`/`DomainEvent` jurnali - hamma tip bitta jadvaldan vaqt bo'yicha tartiblanib o'qiladi.
- `User` → `Customer`, `Admin` kabi kichik ierarxiyalar: autentifikatsiya bitta jadvaldan.
- Dars/kurs kontenti tiplari (`VideoLesson`, `QuizLesson`) - bitta tartiblangan ro'yxatda ko'rsatiladi.

**Ehtiyot bo'ling:** Subclass'lar ko'p va har birining maydonlari ko'p bo'lsa, jadval ko'plab nullable ustunlar bilan "siyraklashadi" (sparse table) va ma'lumot butunligini DB darajasida ta'minlash imkoni yo'qoladi. Yangi subclass qo'shish har safar `ALTER TABLE` talab qiladi, shuning uchun tez o'sadigan va tarkibi juda farq qiladigan ierarxiyalar uchun JOINED strategiyani ko'rib chiqing.

---

## 9.17 Sinf Jadvallari Merosi (Class Table Inheritance / JOINED)

**Tavsif:** Ierarxiyadagi har bir sinf - abstrakt bo'lsa ham - o'z jadvaliga ega bo'ladi; bola jadvallari ota jadval bilan birlamchi kalit orqali bog'lanadi. Natijada sxema normalizatsiyalangan bo'ladi, subclass maydonlariga `NOT NULL` va unikal cheklovlar qo'yish mumkin. Buning narxi: har bir subtype obyektini o'qish uchun `JOIN`, polimorf so'rovlar uchun esa `LEFT JOIN`lar yoki `UNION` kerak. Bu strategiya domen modeli sofligini DB butunligi bilan birga saqlamoqchi bo'lganda tanlanadi.

**Spring'da qayerda uchraydi:** `@Inheritance(strategy = InheritanceType.JOINED)`, bola tomonda FK ustun nomini belgilash uchun `@PrimaryKeyJoinColumn(name = "payment_id")`. Hibernate 6.x bu strategiyada ham `TREAT`, `TYPE()` va `CriteriaBuilder.treat()` ni to'liq qo'llab-quvvatlaydi; `@DiscriminatorColumn` ixtiyoriy bo'lsa-da, Hibernate uni qo'shilganda yuklashni optimallashtirishi mumkin. Flyway/Liquibase migratsiyalarida har bir subclass jadvali alohida `CREATE TABLE` sifatida yoziladi, bu esa sxema evolyutsiyasini aniqroq qiladi.

**Qo'llanish keyslari:**
- `Vehicle` → `Car`, `Truck`, `Motorcycle`: har birida o'ziga xos 5-10 majburiy maydon.
- `Product` → `PhysicalProduct` (vazn, o'lcham `NOT NULL`), `DigitalProduct` (yuklab olish URL).
- `Party` → `Person`, `Organization`: moliya/CRM tizimlarining klassik modeli.
- `Contract` → `LeaseContract`, `ServiceContract`: regulyator talablari bo'yicha har bir tip to'liq cheklovlarga ega.
- `Account` → `SavingsAccount`, `CreditAccount`: subtype maydonlariga DB-level check constraint kerak.

**Ehtiyot bo'ling:** Chuqur ierarxiya (3+ daraja) va tez-tez bajariladigan polimorf ro'yxat so'rovlari JOIN sonini ko'paytirib, performance'ni sezilarli pasaytiradi - bunday hollarda o'qish uchun DTO projection yoki alohida read model tuzing. Shuningdek har bir `INSERT` bir nechta jadvalga yoziladi, shuning uchun yuqori yozuv intensivligida bu strategiya SINGLE_TABLE'dan qimmatroq.

---

## 9.18 Konkret Jadval Merosi (Concrete Table Inheritance / TABLE_PER_CLASS)

**Tavsif:** Faqat konkret (instantiatsiya qilinadigan) sinflar uchun jadval yaratiladi va har bir jadval ierarxiyadagi barcha maydonlarni - meros olinganlari bilan birga - o'zida takrorlaydi. Bitta tip bilan ishlaganda hech qanday JOIN kerak emas, shuning uchun bir tipli operatsiyalar juda tez bo'ladi. Buning evaziga polimorf so'rov `UNION ALL` ga aylanadi va umumiy maydonlar bir nechta jadvalda dublikat bo'ladi. JPA spetsifikatsiyasida bu strategiyani qo'llab-quvvatlash ixtiyoriy (optional) deb belgilangan.

**Spring'da qayerda uchraydi:** `@Inheritance(strategy = InheritanceType.TABLE_PER_CLASS)`; ID generatsiyasida `GenerationType.IDENTITY` ishlamaydi (kalit butun ierarxiya bo'ylab unikal bo'lishi kerak), shuning uchun `GenerationType.SEQUENCE` yoki `TABLE`, ya'ni `@SequenceGenerator` ishlatiladi. Alternativa sifatida Hibernate'ning `@MappedSuperclass` ko'proq qo'llanadi: u maydonlarni meros qilib beradi, lekin polimorf so'rovlarni umuman yo'qotadi va shu bilan `UNION` muammosini chetlab o'tadi.

**Qo'llanish keyslari:**
- Legacy jadvallarni (`crm_customer`, `erp_customer`) umumiy abstrakt sinf ostida maplash, sxemani o'zgartirmasdan.
- Har bir tip bilan alohida, mustaqil ishlaydigan modullar (masalan `ArchivedOrder` va `ActiveOrder`).
- Multi-tenant yoki shard'langan jadvallar, bir xil maydon to'plami bilan.
- Hisobot jadvallari: `MonthlyReport`, `QuarterlyReport` - hamma so'rov bitta tip bo'yicha.
- `@MappedSuperclass` bilan umumiy audit maydonlarini (`createdAt`, `createdBy`) barcha entity'ga berish.

**Ehtiyot bo'ling:** Abstrakt ota tip bo'yicha so'rov yozsangiz, Hibernate barcha konkret jadvallarni `UNION ALL` bilan birlashtiradi - bu so'rov rejasi (query plan) ko'pincha yomon bo'ladi va tashqi FK'lar ota tipga ishora qila olmaydi. Umumiy maydonni o'zgartirish har bir jadvalda migratsiya talab qiladi, shuning uchun bu strategiyani faqat polimorf so'rov deyarli kerak bo'lmaganda tanlang; aks holda `@MappedSuperclass` yoki JOINED afzal.

---

## 9.19 Meros Mapper'lari (Inheritance Mappers)

**Tavsif:** Meros ierarxiyasini maplashda umumiy maydonlar uchun yozilgan kodni takrorlamaslik maqsadida mapper'larning o'zi ham ierarxiya hosil qiladi: abstrakt ota mapper umumiy ustunlarni o'qish/yozishni bajaradi, bola mapper'lar faqat o'ziga xos maydonlar bilan shug'ullanadi. Bu pattern asosan qo'lda yozilgan data access qatlami yoki DTO konvertatsiyasi uchun ma'noga ega, chunki JPA kabi ORM'lar bu ishni o'zi bajaradi. Zamonaviy Spring loyihalarida u ko'proq mapping kutubxonalari konfiguratsiyasi sifatida namoyon bo'ladi.

**Spring'da qayerda uchraydi:** MapStruct (`@Mapper`, `@SubclassMapping` - MapStruct 1.5+, `@InheritConfiguration`, `@InheritInverseConfiguration`) polimorf entity → DTO konvertatsiyasini kompilyatsiya vaqtida hal qiladi. Jackson tomonida `@JsonTypeInfo` + `@JsonSubTypes` polimorf serializatsiya uchun shu rolni bajaradi. Spring JDBC bilan qo'lda yozganda abstrakt `RowMapper<T>` implementatsiyasi (`AbstractPaymentRowMapper` → `CardPaymentRowMapper`) yoki `BeanPropertyRowMapper` bilan subclass'lar bo'yicha dispatch qiluvchi factory ishlatiladi.

```java
@Mapper(componentModel = "spring")
interface PaymentMapper {
    @SubclassMapping(source = CardPayment.class, target = CardPaymentDto.class)
    @SubclassMapping(source = CryptoPayment.class, target = CryptoPaymentDto.class)
    PaymentDto toDto(Payment payment);
}
```

**Qo'llanish keyslari:**
- Polimorf entity ierarxiyasini API DTO ierarxiyasiga MapStruct `@SubclassMapping` bilan o'girish.
- `JdbcTemplate` bilan ishlaydigan legacy modulda discriminator bo'yicha `RowMapper` tanlash.
- Event sourcing'da event tiplarini JSON'dan tiklashda Jackson `@JsonSubTypes` ierarxiyasi.
- Umumiy audit/metadata maydonlarini bitta abstrakt mapper'da bir marta maplash.
- Bir nechta tashqi tizim formatini (`XmlOrder`, `CsvOrder`) umumiy domen modeliga keltirish.

**Ehtiyot bo'ling:** JPA ishlatib turib qo'lda mapper ierarxiyasi qurish - ortiqcha ish va xatolar manbai; bu patternga faqat ORM'siz yoki ORM chegarasidan tashqarida (DTO, tashqi format) murojaat qiling. `instanceof` zanjiri bilan qilingan dispatch yangi subclass qo'shilganda jimgina ishdan chiqadi, shuning uchun Java 21 `switch` pattern matching'ni `sealed` ierarxiya bilan birga ishlatib, kompilyator to'liqligini (exhaustiveness) tekshirishga majburlang.

---

## 9.20 Metama'lumot Maplash (Metadata Mapping)

**Tavsif:** Obyekt maydonlari bilan jadval ustunlari o'rtasidagi moslikni imperativ kodda yozish o'rniga, uni deklarativ metama'lumot sifatida tasvirlaydi; framework esa shu metama'lumotdan SQL'ni runtime'da generatsiya qiladi. Shu tufayli boilerplate mapping kodi butunlay yo'qoladi va sxema bilan model o'rtasidagi bog'liqlik bitta joyda, o'qiladigan ko'rinishda saqlanadi. Metama'lumot annotatsiya, XML yoki konvensiya (convention over configuration) shaklida bo'lishi mumkin. Bu - butun JPA'ning asos pattern'i.

**Spring'da qayerda uchraydi:** JPA annotatsiyalari: `@Entity`, `@Table`, `@Column`, `@Id`, `@GeneratedValue`, `@JoinColumn`, `@OneToMany`, `@Transient`, `@Convert`, `@NamedQuery`; alternativa sifatida `orm.xml` deskriptori. Runtime'da bu metama'lumotga `jakarta.persistence.metamodel.Metamodel` va `EntityManager.getMetamodel()` orqali, kompilyatsiya vaqtida esa Hibernate JPA Metamodel Generator yaratgan `Entity_` sinflari (`Payment_.amount`) orqali kirish mumkin. Spring Data o'z tomonidan `PersistentEntity`/`PersistentProperty` abstraksiyasini va `NamingStrategy` (Spring Boot 3.x'da `CamelCaseToUnderscoresNamingStrategy`) ni qo'shadi.

**Qo'llanish keyslari:**
- Entity'ni `@Entity`/`@Column` bilan maplash va `JdbcTemplate` uchun qo'lda SQL yozishdan voz kechish.
- `@Converter(autoApply = true)` bilan barcha `Money` yoki enum maydonlarini markazlashgan tarzda o'girish.
- Hibernate `hbm2ddl`/Flyway'ga sxema yoki validatsiya uchun metama'lumotdan DDL olish (`spring.jpa.hibernate.ddl-auto=validate`).
- Typesafe Criteria API so'rovlarini generatsiyalangan `Entity_` metamodel sinflari bilan yozish.
- Ko'p DB'ni qo'llab-quvvatlash: `@Table(name=...)` va naming strategy orqali bitta model, turli sxema nomlari.

**Ehtiyot bo'ling:** Annotatsiyalar domen sinflarini infratuzilmaga bog'laydi - qattiq hexagonal arxitekturada mapping metama'lumotini alohida persistence model yoki `orm.xml`ga chiqarish kerak bo'lishi mumkin. Ishlab chiqarishda (production) `ddl-auto=update` yoki `create` ni hech qachon yoqmang: metama'lumotdan avtomatik generatsiya qilingan sxema nazoratsiz o'zgarishlarga va ma'lumot yo'qolishiga olib keladi - migratsiyani Flyway yoki Liquibase boshqarsin.

---

## 9.21 So'rov Obyekti (Query Object)

**Tavsif:** So'rovni satr ko'rinishidagi SQL/JPQL sifatida emas, balki obyektlar grafigi sifatida tasvirlaydi: shartlar, tartiblash va proyeksiya tiplangan (type-safe) API orqali qurib boriladi. Shu tufayli so'rov qismlarini dinamik ravishda kombinatsiya qilish, qayta ishlatish va kompilyatsiya vaqtida tekshirish mumkin bo'ladi. Bu pattern, ayniqsa, foydalanuvchi tanlagan filtrlar soni oldindan noma'lum bo'lgan qidiruv ekranlarida if-else bilan SQL yopishtirishni (string concatenation) yo'q qiladi. Interpreter pattern'ining ma'lumotlarga kirish sohasidagi ko'rinishi.

**Spring'da qayerda uchraydi:** JPA Criteria API (`CriteriaBuilder`, `CriteriaQuery`, `Root`, `Predicate`), Spring Data JPA'ning `Specification<T>` interfeysi (`JpaSpecificationExecutor<T>`, `Specification.where(...).and(...)`, Spring Data 3.x'da `Specification.allOf`/`anyOf`), Querydsl (`QPayment.payment.amount.gt(...)`, `QuerydslPredicateExecutor`), Blaze-Persistence Entity Views va Spring Data'ning `Example`/`QueryByExampleExecutor`'i. Spring Data JDBC/MongoDB tomonida `Query`/`Criteria` sinflari (`Criteria.where("status").is("NEW")`) shu rolni bajaradi.

```java
Specification<Payment> spec = Specification
    .where(amountGreaterThan(min))
    .and(statusIn(statuses));
Page<Payment> page = repo.findAll(spec, pageable);
```

**Qo'llanish keyslari:**
- Admin panelidagi ko'p filtrli qidiruv: 10 ta ixtiyoriy filtr, har biri alohida `Specification` metodi.
- Xavfsizlik shartini (`tenantId = :current`) barcha so'rovlarga markazlashgan `Specification` sifatida qo'shish.
- Hisobot konstruktori: foydalanuvchi tanlagan ustunlar va shartlar bo'yicha so'rov qurish.
- Querydsl bilan kompilyatsiya vaqtida tekshiriladigan murakkab `JOIN` va subquery'lar.
- `Pageable` va `Sort` bilan birga dinamik sahifalangan ro'yxatlar.

**Ehtiyot bo'ling:** Criteria API ortiqcha "shovqinli" (verbose) va juda murakkab so'rovlarda o'qilmas holga keladi - bunday hollarda `@Query` bilan aniq JPQL yoki `JdbcClient` bilan xom SQL ko'proq saqlanadigan yechim. Dinamik so'rovlar har bir kombinatsiya uchun yangi query plan yaratishi mumkin, shuning uchun cheksiz filtr kombinatsiyalariga ruxsat bermang va foydalanuvchi kiritgan maydon nomini to'g'ridan-to'g'ri `Root.get(...)` ga uzatmang (whitelist qiling).

---

## 9.22 DTO Proyeksiyasi (DTO Projection)

**Tavsif:** To'liq entity grafini yuklash o'rniga, DB'dan faqat kerakli maydonlarni o'qib, ularni to'g'ridan-to'g'ri yengil obyektga (interface yoki record) joylashtiradi. Bu kam ma'lumot uzatish, kamroq xotira va persistence context'ga ortiqcha obyekt qo'shilmasligi hisobiga o'qish operatsiyalarini sezilarli tezlashtiradi. Shuningdek domen entity'sini API javobidan ajratib, lazy loading va `LazyInitializationException` muammolarini manbada yo'q qiladi. CQRS'ning o'qish tomonida asosiy vosita.

**Spring'da qayerda uchraydi:** Spring Data JPA uchta variantni beradi: closed/open interface projection (getter'li interfeys, `@Value("#{target.x}")` SpEL bilan), class-based projection (Java `record` yoki konstruktorli DTO - `SELECT new com.app.OrderSummary(o.id, o.total) FROM Order o` yoki Spring Data 3.2+ da `record` bilan avtomatik), hamda dynamic projection (`<T> List<T> findByStatus(String s, Class<T> type)`). Qo'shimcha: `@EntityGraph` bilan nimani yuklashni boshqarish, `JdbcClient` (Spring Framework 6.1+) yoki `JdbcTemplate` + `DataClassRowMapper` bilan record'ga maplash, Querydsl `Projections.constructor(...)`, Blaze-Persistence Entity Views.

**Qo'llanish keyslari:**
- Ro'yxat/grid ekrani: 40 maydonli entity o'rniga 5 ustunli `OrderRow` record.
- Avtokomplit (autocomplete) uchun faqat `id` va `name` qaytaruvchi interface projection.
- Agregatsiya natijalari: `SELECT new ...Stats(o.status, count(o))` - entity'ga sig'maydigan shakl.
- REST API javobi: entity'ni to'g'ridan-to'g'ri serializatsiya qilmasdan, DTO orqali kontraktni barqarorlashtirish.
- Eksport (CSV/Excel) uchun minglab satrni `Stream` bilan yengil DTO sifatida o'qish.

**Ehtiyot bo'ling:** Projection obyektlari persistence context tomonidan boshqarilmaydi - ularni o'zgartirib saqlab bo'lmaydi, shuning uchun yozish (write) operatsiyalarida haqiqiy entity yuklang. Open projection'lar (SpEL bilan) butun entity'ni yuklashga majbur qiladi va optimallashtirish samarasini yo'qotadi; nested interface projection'lar esa jimgina N+1 so'rov keltirib chiqarishi mumkin - SQL log'ni (`spring.jpa.show-sql` yoki `datasource-proxy`) tekshirib ko'ring.

---

## 9.23 Optimistik Oflayn Qulf (Optimistic Offline Lock)

**Tavsif:** Bir nechta tranzaksiya bir xil yozuvni o'zgartirishga urinishi kamdan-kam uchraydi degan taxminga asoslanib, ma'lumotni o'qiyotganda hech narsani bloklamaydi, balki yozish paytida yozuv o'zgarmaganini tekshiradi. Buning uchun har bir satrda versiya raqami (yoki timestamp) saqlanadi: `UPDATE ... WHERE id = ? AND version = ?` nol satr o'zgartirsa, demak boshqa kimdir allaqachon yozgan va konflikt e'lon qilinadi. Bu "oflayn" deb ataladi, chunki tekshiruv bitta DB tranzaksiyasidan uzun bo'lgan biznes tranzaksiyasini (foydalanuvchi formani to'ldirgan vaqtni) qamrab oladi. Concurrency'ni ushlab qolish (throughput) jihatidan eng arzon usul.

**Spring'da qayerda uchraydi:** JPA'da `@Version` annotatsiyasi (`int`, `long`, `short` yoki `java.sql.Timestamp`/`Instant` maydonida), konflikt yuz berganda `jakarta.persistence.OptimisticLockException`, Spring esa uni `org.springframework.orm.ObjectOptimisticLockingFailureException` ga tarjima qiladi. Qo'shimcha nazorat uchun `LockModeType.OPTIMISTIC` va `OPTIMISTIC_FORCE_INCREMENT` (`@Lock` annotatsiyasi repository metodida), Hibernate'ning `@OptimisticLocking(type = OptimisticLockType.DIRTY|ALL)` - versiya ustunisiz legacy jadvallar uchun. Spring Data JDBC ham `@Version` ni qo'llab-quvvatlaydi. Qayta urinish uchun Spring Retry'ning `@Retryable(retryFor = ObjectOptimisticLockingFailureException.class)` ishlatiladi.

**Qo'llanish keyslari:**
- Web formada entity tahrirlash: foydalanuvchi 5 daqiqa yozgan, saqlashda "yozuv o'zgargan" xabari chiqadi.
- Ombor qoldig'ini (`stock`) kamaytirish - konflikt kam, lekin yo'qotishga yo'l qo'yilmaydi.
- REST API'da `ETag`/`If-Match` sarlavhasini `@Version` qiymatiga bog'lab, HTTP 409/412 qaytarish.
- Hujjat holatini (`DRAFT → APPROVED`) bir nechta moderator bir vaqtda o'zgartirishiga qarshi himoya.
- Batch ishlovida yozuvlarni qayta ishlash va konflikt bo'lganda `@Retryable` bilan takrorlash.

**Ehtiyot bo'ling:** `@Version` maydonini qo'lda o'zgartirish yoki `setVersion(...)` ni DTO'dan ko'r-ko'rona ko'chirish butun mexanizmni buzadi - versiyani faqat provayder boshqarsin, lekin DTO orqali uzatilgan eski versiyani entity'ga qaytarish aynan optimistik tekshiruvning to'g'ri usuli, chunki u foydalanuvchi ko'rgan holatni ifodalaydi. Yuqori konkurensiyali "hot row" (umumiy hisoblagich, yagona balans satri) uchun bu pattern cheksiz retry'ga aylanadi - bunda pessimistik qulf yoki atomik `UPDATE ... SET x = x - ?` ni tanlang.

---

## 9.24 Pessimistik Oflayn Qulf (Pessimistic Offline Lock)

**Tavsif:** Konflikt ehtimoli yuqori yoki konflikt narxi juda qimmat bo'lganda, yozuv o'qilishi bilanoq boshqa tranzaksiyalar uchun bloklanadi va ish tugagunicha ushlab turiladi. Bu konkurent o'zgarishlarni butunlay oldini oladi, lekin kutish (contention), throughput pasayishi va deadlock xavfini keltiradi. DB darajasida bu odatda `SELECT ... FOR UPDATE` bilan amalga oshiriladi. Biznes tranzaksiyasi uzun bo'lsa, DB qulfini emas, balki alohida "lock table" yoki Redis-asosidagi distributed lock'ni ishlatish to'g'riroq.

**Spring'da qayerda uchraydi:** JPA'da `LockModeType.PESSIMISTIC_READ`, `PESSIMISTIC_WRITE`, `PESSIMISTIC_FORCE_INCREMENT` - `entityManager.find(Order.class, id, LockModeType.PESSIMISTIC_WRITE)` yoki Spring Data'da repository metodi ustida `@Lock(LockModeType.PESSIMISTIC_WRITE)`. Kutish vaqtini `@QueryHints(@QueryHint(name = "jakarta.persistence.lock.timeout", value = "3000"))` bilan cheklash, xatolar: `PessimisticLockException`, `LockTimeoutException` → Spring'da `PessimisticLockingFailureException`/`CannotAcquireLockException`. Alohida pattern sifatida Spring Integration'ning `JdbcLockRegistry`, `RedisLockRegistry` yoki ShedLock kutubxonasi node'lar o'rtasida qulf beradi. Qulf doimo `@Transactional` ichida bo'lishi shart.

**Qo'llanish keyslari:**
- Hisob balansidan pul yechish: yozuv `PESSIMISTIC_WRITE` bilan o'qiladi, double-spend butunlay yo'qoladi.
- Chipta/o'rindiq bron qilish - ikki foydalanuvchi bitta o'rindiqqa bir vaqtda da'vo qiladi.
- Navbatdan ish olish (job queue) `SELECT ... FOR UPDATE SKIP LOCKED` bilan - bir ish faqat bitta worker'ga.
- Scheduled task'ni klasterda faqat bitta node bajarishi - ShedLock yoki `JdbcLockRegistry`.
- Ketma-ket raqam generatsiyasi (hisob-faktura nomeri) - bo'shliqsiz (gapless) seriya kerak bo'lganda.

**Ehtiyot bo'ling:** Qulfni tranzaksiya ichida uzoq ushlash (tashqi HTTP chaqiruvi, foydalanuvchi kutishi) tizimni to'xtatib qo'yadi va deadlock keltiradi - har doim lock timeout bering va qulflarni barcha kodda bir xil tartibda oling. Foydalanuvchi o'ylab turgan paytga DB qulfini qoldirmang: uzun biznes tranzaksiyasi uchun optimistik qulf yoki ochiq-oydin (explicit) "kim tahrirlab turibdi" belgisi bilan ishlovchi alohida lock jadvalidan foydalaning.

## 9.25 Yirik donali qulf (Coarse-Grained Lock)

**Tavsif:** Bir-biriga bog'liq obyektlar guruhini (aggregate'ni) bitta umumiy qulf bilan himoyalash patterni. Har bir child entity uchun alohida version yuritish o'rniga, aggregate root'dagi bitta version yoki lock nuqtasi butun klasterni qamrab oladi. Bu concurrency nazoratini soddalashtiradi va qisman o'zgargan (yarim yangilangan) aggregate holatini oldini oladi.

**Spring'da qayerda uchraydi:** JPA/Hibernate'da aggregate root'da `@Version` maydoni va child'larda `@OptimisticLock` semantikasi orqali amalga oshiriladi: Hibernate'ning `OPTIMISTIC_FORCE_INCREMENT` yoki `PESSIMISTIC_FORCE_INCREMENT` lock mode'lari (`jakarta.persistence.LockModeType`) child o'zgarganda ham root version'ini oshiradi. `EntityManager.lock(root, LockModeType.OPTIMISTIC_FORCE_INCREMENT)` yoki Spring Data JPA'da `@Lock(LockModeType.PESSIMISTIC_FORCE_INCREMENT)` repository metodida ishlatiladi. Spring Data JDBC esa bu patternni tabiiy ravishda qo'llaydi - aggregate butunlay root orqali saqlanadi va `@Version` faqat root'da bo'ladi.

**Qo'llanish keyslari:**
- Buyurtma (`Order`) va uning `OrderLine` qatorlari bir vaqtda ikki operator tomonidan tahrirlanishini oldini olish.
- Invoice va uning `InvoiceItem`'lari yig'indisi invariantini (jami summa) saqlab qolish.
- Shartnoma hujjati va uning ilovalari bitta tranzaksion birlik sifatida tasdiqlanadigan workflow'lar.
- Bank hisobi va unga tegishli limit sozlamalarini bir qulf ostida o'zgartirish.
- Aggregate ichidagi har bir child'ga alohida version qo'ymasdan, lost update'ni butun klaster bo'yicha aniqlash.

**Ehtiyot bo'ling:** Qulf chegarasi juda keng bo'lsa, bir-biriga aloqasi yo'q child'larni o'zgartirgan foydalanuvchilar ham `OptimisticLockException` oladi va contention keskin oshadi - aggregate'ni kichik saqlang. Shuningdek, `PESSIMISTIC_FORCE_INCREMENT` uzun tranzaksiyalarda DB satr qulflarini ushlab turadi, bu deadlock xavfini oshiradi.

## 9.26 Yashirin qulf (Implicit Lock)

**Tavsif:** Qulflashni har bir developer qo'lda yozishi o'rniga, framework yoki infratuzilma qatlami uni avtomatik va bir xil tarzda qo'llashi patterni. Maqsad - inson xatosini yo'q qilish: qulfni "esdan chiqarish" imkonsiz bo'ladi, chunki u domen kodidan tashqarida, deklarativ ravishda qo'llanadi. Odatda mapping metadatasi, AOP yoki repository qatlami orqali amalga oshiriladi.

**Spring'da qayerda uchraydi:** `@Version` maydoni eng toza misol - Hibernate har bir `UPDATE`ga `WHERE version = ?` shartini o'zi qo'shadi, developer hech narsa yozmaydi. Spring Data JPA'da `@Lock(LockModeType.PESSIMISTIC_WRITE)` repository metodi darajasida deklarativ qulf beradi; `@Transactional` esa tranzaksiya chegarasini AOP proxy orqali yashirin boshqaradi. Spring Integration/Spring Boot'da `LockRegistry` (`JdbcLockRegistry`, `RedisLockRegistry`, `ZookeeperLockRegistry`) va ShedLock kutubxonasining `@SchedulerLock` annotatsiyasi ham yashirin qulf sifatida ishlaydi.

**Qo'llanish keyslari:**
- Barcha mutable entity'larga `@Version` qo'yib, optimistic locking'ni butun domen bo'ylab majburiy qilish.
- `@SchedulerLock` bilan cluster'dagi bir nechta instance'dan faqat bittasi scheduled job'ni bajarishini ta'minlash.
- Repository'da `findByIdForUpdate` kabi metodga `@Lock` qo'yib, pessimistic qulfni bir joyda markazlashtirish.
- Base entity (`@MappedSuperclass`) ichida version va audit maydonlarini e'lon qilib, yangi entity'lar avtomatik qulflanishi.
- `JdbcLockRegistry` orqali taqsimlangan muhitda umumiy resursga (fayl eksporti, hisobot generatsiyasi) kirishni seriyalash.

**Ehtiyot bo'ling:** Yashirin qulf "ko'rinmas" bo'lgani uchun developer uning narxini sezmaydi - pessimistic rejimda bu kutilmagan blocking va timeout'larga olib keladi. Ayniqsa qulf olinadigan joy `@Transactional` chegarasi tashqarisida qolsa (self-invocation, proxy chetlab o'tilishi), qulf aslida hech narsani himoya qilmaydi.

## 9.27 N+1 muammosi yechimlari (N+1 Problem Solutions)

**Tavsif:** Bitta so'rov N ta ota obyektni yuklaydi, so'ngra har biri uchun bog'langan kolleksiya alohida so'rov bilan olinadi - natijada N+1 ta SQL ketadi va latency chiziqli o'sadi. Yechimlar assotsiatsiyalarni oldindan, boshqariladigan tarzda yuklashga asoslanadi: `JOIN FETCH`, entity graph, batch fetching va subselect. Tanlov kardinallik va pagination talablariga qarab qilinadi.

**Spring'da qayerda uchraydi:** JPQL'da `JOIN FETCH` (`@Query("select o from Order o join fetch o.lines")`), `@EntityGraph(attributePaths = {"lines", "customer"})` Spring Data JPA repository metodida, dinamik holatda `EntityManager.createEntityGraph()` yoki `jakarta.persistence.fetchgraph` hint. Hibernate 6.x'da `@BatchSize(size = 50)`, global `hibernate.default_batch_fetch_size` property (Spring Boot'da `spring.jpa.properties.hibernate.default_batch_fetch_size`) va `@Fetch(FetchMode.SUBSELECT)` mavjud. Diagnostika uchun `hibernate.query.plan_cache`emas, balki `spring.jpa.show-sql`, Hibernate statistics (`hibernate.generate_statistics`) yoki datasource-proxy / p6spy ishlatiladi.

**Qo'llanish keyslari:**
- Buyurtmalar ro'yxatini mahsulot qatorlari bilan bitta sahifada ko'rsatish - `@EntityGraph` bilan bir so'rovga keltirish.
- REST API'da DTO projection (`interface`-based yoki konstruktor expression) bilan faqat kerakli maydonlarni olish.
- `ManyToOne` referencelar ko'p bo'lgan jadval uchun `default_batch_fetch_size` qo'yib, N so'rovni `IN (...)` ga birlashtirish.
- Pagination bilan birga kolleksiya kerak bo'lsa: avval ID'larni sahifalab olish, keyin `where id in :ids join fetch` bilan ikkinchi so'rov.
- Integration testda so'rov sonini assert qilib (Hibernate `Statistics.getQueryExecutionCount()`), regressiyani CI'da ushlash.

**Ehtiyot bo'ling:** Bir nechta `JOIN FETCH` bilan kolleksiyalarni birga yuklash kartezian ko'paytmasi beradi (Hibernate 6 `MultipleBagFetchException` yoki xotira portlashi), shuning uchun bir so'rovda faqat bitta kolleksiyani fetch qiling. `JOIN FETCH` + `setFirstResult/setMaxResults` kombinatsiyasi pagination'ni xotirada bajarishga majbur qiladi - buni Hibernate 6 ogohlantirish bilan bildiradi.

## 9.28 View ichida ochiq sessiya - antipattern (Open Session in View)

**Tavsif:** Hibernate `Session` (yoki JPA `EntityManager`) HTTP so'rov oxirigacha, ya'ni view render qilinishigacha ochiq qoldiriladi, shunda template lazy assotsiatsiyalarni erkin yuklay oladi. Bu `LazyInitializationException`ni yo'qotadi, lekin ma'lumotlarga kirishni prezentatsiya qatlamiga sizdiradi: so'rovlar nazoratsiz joyda, tranzaksiyadan tashqarida va ko'pincha N+1 shaklida ketadi. Shu sababli zamonaviy arxitekturalarda antipattern hisoblanadi.

**Spring'da qayerda uchraydi:** Spring Boot'da `spring.jpa.open-in-view` property (JPA uchun) sukut bo'yicha `true` va ishga tushganda ogohlantirish log'i chiqaradi; uni `false` qilish tavsiya etiladi. Texnik jihatdan `OpenEntityManagerInViewInterceptor` / `OpenEntityManagerInViewFilter` (va klassik `OpenSessionInViewFilter`) sinflari orqali amalga oshadi. To'g'ri alternativa - service qatlamida `@Transactional` ichida `@EntityGraph`/`JOIN FETCH` bilan kerakli grafni yuklash va controller'ga DTO qaytarish (MapStruct yoki record'lar bilan).

**Qo'llanish keyslari:**
- Legacy JSP/Thymeleaf monolitda tez vaqtinchalik yechim sifatida (migratsiya rejasi bilan birga).
- Prototip yoki demo'da fetch strategiyasini loyihalashga vaqt yo'q bo'lganda.
- Uni `false` qilib, `LazyInitializationException`lar orqali yashirin lazy yuklashlarni topish - texnik qarzni audit qilish usuli.
- Serializatsiya chog'ida (Jackson) lazy proxy'larga tegilishini aniqlab, DTO qatlamiga o'tish zaruratini asoslash.
- Reaktiv yoki stateless REST servislarga ko'chishda nima buzilishini oldindan o'lchash.

**Ehtiyot bo'ling:** `open-in-view=true` holatida DB connection so'rovning butun davomiyligi bo'yicha ushlab turiladi, bu HikariCP pool'ini tugatadi va yuklama ostida timeout'larga olib keladi; render paytidagi yozishlar esa tranzaksiyadan tashqarida (auto-commit) ketishi mumkin. Yangi loyihada uni darhol `false` qilib, fetch strategiyasini oshkora boshqarish kerak.

## 9.29 Faqat o'qish uchun tranzaksiyalar (Read-only Transactions)

**Tavsif:** O'qish operatsiyalarini yozishga ruxsat bermaydigan tranzaksiya kontekstida bajarish patterni. Bu ORM'ga dirty checking va flush'ni o'tkazib yuborish imkonini beradi, JDBC driver va DB'ga esa optimallashtirish (replica'ga yo'naltirish, snapshot rejimi) haqida ishora beradi. Natijada CPU va xotira sarfi kamayadi, tasodifiy yozishlar esa oldini olinadi.

**Spring'da qayerda uchraydi:** `@Transactional(readOnly = true)` - `JpaTransactionManager` buni Hibernate `Session`ga `FlushMode.MANUAL` sifatida uzatadi va `Connection.setReadOnly(true)` chaqiradi. Spring Data JPA'ning `SimpleJpaRepository` sinfi allaqachon `@Transactional(readOnly = true)` bilan belgilangan, shu sababli `findAll`/`findById` o'qish rejimida ketadi. Multi-datasource holatida `AbstractRoutingDataSource` + `TransactionSynchronizationManager.isCurrentTransactionReadOnly()` orqali read replica'ga routing qilinadi.

**Qo'llanish keyslari:**
- Hisobot va ro'yxat endpoint'larida katta natija to'plamini yuklaganda dirty checking yukini olib tashlash.
- `AbstractRoutingDataSource` bilan barcha read-only tranzaksiyalarni read replica'ga yuborish.
- Service metodlarini sinf darajasida `readOnly = true` qilib, yozadiganlarini `@Transactional` bilan override qilish konvensiyasi.
- Batch eksportda (CSV/Excel) `Stream`/`ScrollableResults` bilan o'qiganda connection rejimini aniq belgilash.
- Audit yoki tekshiruv so'rovlarida tasodifiy entity modifikatsiyasining DB'ga tushishini oldini olish.

**Ehtiyot bo'ling:** `readOnly = true` yozishni kafolatli bloklamaydi - ba'zi DB/driverlarda bu faqat ishora, native query yoki `flush()` chaqirilsa o'zgarish baribir ketishi mumkin. Shuningdek, read replica'ga routing qilsangiz, replication lag sababli "o'zim yozganni o'zim ko'rmayman" (read-your-own-writes buzilishi) muammosi paydo bo'ladi.

## 9.30 Connection Pool (Connection Pool - HikariCP)

**Tavsif:** DB ulanishini har safar ochish qimmat (TCP + autentifikatsiya + sessiya sozlash), shuning uchun ulanishlar oldindan yaratilib, pool'da saqlanadi va qayta ishlatiladi. Pool bir vaqtda ochiq ulanishlar sonini cheklab, DB'ni ortiqcha yuklamadan himoya qiladi va kutish navbatini boshqaradi. To'g'ri sozlangan pool - ko'pincha backend latency'ining eng katta yagona omili.

**Spring'da qayerda uchraydi:** Spring Boot 3.x/4.x'da `spring-boot-starter-data-jpa` / `-jdbc` bilan HikariCP sukut bo'yicha keladi (`com.zaxxer.hikari.HikariDataSource`). Sozlamalar: `spring.datasource.hikari.maximum-pool-size`, `minimum-idle`, `connection-timeout`, `max-lifetime`, `idle-timeout`, `leak-detection-threshold`, `pool-name`. Metrikalar Micrometer orqali `hikaricp.connections.*` nomi bilan Actuator'ga chiqadi; sog'liq tekshiruvi `DataSourceHealthIndicator`. Alternativalar: Tomcat JDBC, Oracle UCP, reaktiv tomonda R2DBC `ConnectionPoolConfiguration`.

**Qo'llanish keyslari:**
- Yuqori RPS'li REST servisda pool o'lchamini DB'ning `max_connections` chegarasi va instance soniga qarab hisoblash.
- `leak-detection-threshold` qo'yib, yopilmagan `Connection`/uzun `@Transactional` metodlarini log'da aniqlash.
- `max-lifetime`ni DB yoki proxy (PgBouncer, RDS Proxy) idle timeout'idan kichik qilib, uzilgan ulanishlarni oldini olish.
- Kubernetes'da replica soni oshganda umumiy ulanish byudjetini qayta taqsimlash.
- Batch job uchun alohida, kichik pool'li `DataSource` ajratib, OLTP trafikni himoya qilish.

**Ehtiyot bo'ling:** Pool'ni kattalashtirish ko'pincha yomonlashtiradi - DB'da kontekst almashinuvi va qulf contention'i oshadi; HikariCP hujjatlari kichik pool (masalan, yadro soniga bog'liq o'nlab emas, balki birliklar) tavsiya qiladi. Eng ko'p uchraydigan tuzoq - uzun tashqi HTTP chaqiruvlarini `@Transactional` ichida bajarib, ulanishni bekordan-bekorga ushlab turish.

## 9.31 Natural va surrogate kalit (Natural vs Surrogate Key)

**Tavsif:** Natural kalit - domenning o'zidan kelib chiqadigan, biznes ma'nosi bor identifikator (INN, ISBN, email, IATA kodi). Surrogate kalit - biznes ma'nosi yo'q, faqat identifikatsiya uchun generatsiya qilinadigan qiymat (sequence'dan son, UUID). Surrogate kalit o'zgarmaslik va barqarorlik beradi, natural kalit esa join'larni kamaytiradi va tabiiy unikallikni DB darajasida majburlaydi.

**Spring'da qayerda uchraydi:** JPA'da surrogate uchun `@Id @GeneratedValue`, natural kalit uchun `@Id` bilan `@Column(updatable = false)` yoki kompozit holatda `@EmbeddedId`/`@IdClass`. Hibernate'da natural kalitni alohida e'lon qilish uchun `@NaturalId` va `@NaturalIdCache` bor - `session.byNaturalId(Entity.class).using("code", value).load()` orqali keshdan topiladi. Natural unikallikni surrogate PK bilan birga saqlash uchun `@Table(uniqueConstraints = @UniqueConstraint(columnNames = "email"))` ishlatiladi; Spring Data JDBC'da esa entity `Persistable` interfeysini amalga oshirib, yangi/mavjudligini aniq boshqaradi.

**Qo'llanish keyslari:**
- Mijoz jadvalida surrogate `id` + `@NaturalId` sifatida `taxNumber` - ikkisi ham indekslangan.
- Reference/lookup jadvallarda (valyuta, davlat kodi) natural kalitni PK qilib, join'larni qisqartirish.
- Tashqi tizim bilan integratsiyada `externalId`ni natural kalit sifatida saqlab, idempotent import qilish.
- Surrogate kalitni public API'da ko'rsatmaslik uchun alohida `publicId` (UUID) qo'shish.
- Hibernate `@NaturalIdCache` bilan tez-tez takrorlanadigan kod bo'yicha qidiruvni second-level cache'dan olish.

**Ehtiyot bo'ling:** Natural kalitni PK qilish xavfli - biznes qiymatlari o'zgaradi (email, telefon, hatto soliq raqami) va PK o'zgarishi barcha foreign key'larni kaskad yangilashga olib keladi. Mutable yoki qayta ishlatiladigan natural kalitlardan PK yasashdan saqlaning; `equals`/`hashCode`ni esa surrogate ID emas, balki barqaror natural kalit yoki business key asosida yozish Hibernate bilan to'g'riroq ishlaydi.

## 9.32 ID generatsiyasi (ID Generation - SEQUENCE, IDENTITY, UUIDv7, TSID, Hi/Lo)

**Tavsif:** Yangi yozuv uchun unikal birlamchi kalit yaratish strategiyasi: DB sequence, auto-increment ustun, ilova tomonida generatsiya qilinadigan vaqt-tartibli identifikatorlar yoki blok-ajratish (Hi/Lo) algoritmi. Tanlov batch insert imkoniyati, index lokalligi, taqsimlangan generatsiya va ID'ni oshkor qilish xavfsizligiga ta'sir qiladi. ORM uchun eng muhim farq - ID qachon ma'lum bo'ladi: `persist()` paytida yoki `INSERT`dan keyin.

**Spring'da qayerda uchraydi:** JPA `@GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "...")` + `@SequenceGenerator(allocationSize = 50)`, `GenerationType.IDENTITY`, `GenerationType.UUID` (JPA 3.x, Hibernate 6). Hibernate 6.x'da `@IdGeneratorType`, legacy `@GenericGenerator` o'rnini bosdi; `org.hibernate.id.enhanced.SequenceStyleGenerator` va pooled/pooled-lo optimizer'lar Hi/Lo rolini bajaradi. UUIDv7/TSID uchun `io.hypersistence:hypersistence-utils` (`@Tsid`), `com.github.f4b6a3:uuid-creator`/`tsid-creator` yoki Java 17+ qo'lda yozilgan `IdentifierGenerator` ishlatiladi; Spring Data JDBC'da ID'ni ko'pincha ilova o'zi beradi.

**Qo'llanish keyslari:**
- PostgreSQL'da `SEQUENCE` + `allocationSize=50` bilan JDBC batch insert'ni yoqish (yuqori throughput'li import).
- MySQL'da `IDENTITY` ishlatilganda batch insert o'chib qolishini bilib, migratsiya rejasini tuzish.
- Ko'p regionli yoki offline-first tizimda UUIDv7/TSID bilan ID'ni client/service tomonida generatsiya qilish.
- Public URL'da ketma-ket ID'ni yashirish uchun TSID yoki UUID qo'llab, enumeration hujumini kamaytirish.
- Sharding/merge qilinadigan jadvallarda global unikal, vaqt bo'yicha o'sadigan kalitlar bilan konfliktsiz birlashtirish.

```java
@Entity
class Order {
    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "order_seq")
    @SequenceGenerator(name = "order_seq", sequenceName = "order_seq",
                       allocationSize = 50)
    private Long id;
}
```

**Ehtiyot bo'ling:** `GenerationType.IDENTITY` Hibernate'ni har bir `persist()`da darhol `INSERT` yuborishga majbur qiladi va JDBC batching'ni butunlay o'chiradi. Tasodifiy UUIDv4 esa PK indeksida fragmentatsiya va yomon cache lokalligi beradi - vaqt-tartibli UUIDv7/TSID tanlang; `allocationSize`ni DB sequence `INCREMENT BY` qiymatiga mos qilmaslik ID konfliktlariga olib keladi.

## 9.33 Hibernate flush rejimlari va dirty checking (Hibernate Flush Modes & Dirty Checking)

**Tavsif:** Hibernate persistence context'dagi o'zgarishlarni darhol emas, flush paytida SQL'ga aylantiradi. Dirty checking - har bir managed entity'ning hozirgi holatini yuklangan snapshot bilan taqqoslab, qaysi ustunlar o'zgarganini aniqlash jarayoni. Flush mode qachon flush bo'lishini belgilaydi: commit oldidan, har bir so'rovdan avval (`AUTO`), yoki faqat qo'lda chaqirilganda (`MANUAL`/`COMMIT`).

**Spring'da qayerda uchraydi:** `jakarta.persistence.FlushModeType.AUTO|COMMIT`, Hibernate'da qo'shimcha `FlushMode.MANUAL` va `FlushMode.ALWAYS`; `EntityManager.setFlushMode()`, `Session.setHibernateFlushMode()`, so'rov darajasida `Query.setFlushMode()` yoki Spring Data JPA'da `@QueryHints(@QueryHint(name = "org.hibernate.flushMode", value = "COMMIT"))`. `@Transactional(readOnly = true)` Spring'da flush mode'ni `MANUAL`ga o'rnatadi. Dirty checking'ni tezlashtirish uchun Hibernate bytecode enhancement (`hibernate-enhance-maven-plugin` yoki Gradle plugin) va `@DynamicUpdate` ishlatiladi; `Session.setReadOnly(entity, true)` esa snapshot saqlamaydi.

**Qo'llanish keyslari:**
- Katta hisobot o'qishda `readOnly = true` orqali flush va snapshot yukini olib tashlash.
- Batch importda `flush()` + `clear()` ni har N yozuvda chaqirib, persistence context o'sishini cheklash.
- `@DynamicUpdate` bilan faqat o'zgargan ustunlarni `UPDATE` qilish (keng jadvallar va trigger'li DB'larda).
- Bytecode enhancement yoqib, minglab managed entity'li kontekstda dirty checking CPU sarfini kamaytirish.
- `FlushModeType.COMMIT` bilan ortiqcha auto-flush'ni o'chirib, read-heavy service metodida so'rovlar sonini barqarorlashtirish.

**Ehtiyot bo'ling:** `COMMIT`/`MANUAL` rejimida flush kechiktirilgani uchun shu tranzaksiya ichidagi JPQL yoki native so'rov hali yozilmagan o'zgarishlarni ko'rmaydi - stale natija xavfi. Native query ishlatganda Hibernate qaysi jadvallar tegishli ekanini bilmaydi va `AUTO` rejimda ham flush qilmasligi mumkin, shu sababli `Query.addSynchronizedEntityClass()` yoki qo'lda `flush()` kerak bo'ladi.

## 9.34 Spring Data JDBC aggregate-yo'naltirilgan mapping (Spring Data JDBC Aggregate-Oriented Mapping)

**Tavsif:** Spring Data JDBC DDD'ning aggregate tushunchasini mapping'ning asosiy qoidasiga aylantiradi: har bir repository bitta aggregate root'ga tegishli, child entity'lar faqat root orqali yuklanadi va saqlanadi. Lazy loading, dirty checking va persistence context yo'q - `save()` butun aggregate'ni yozadi, aggregate'lar orasidagi bog'lanish esa obyekt referensi emas, `AggregateReference` (ya'ni ID) bilan ifodalanadi. Bu Hibernate'dan sodda va oldindan taxmin qilinadigan SQL beradi.

**Spring'da qayerda uchraydi:** `spring-boot-starter-data-jdbc` moduli; `org.springframework.data.annotation.Id`, `@Table`, `@Column`, `@MappedCollection(idColumn, keyColumn)`, `@Embedded`, `@Version`, `AggregateReference<T, ID>`. Repository interfeyslari `CrudRepository`/`ListCrudRepository` yoki `@Query` bilan aniq SQL; maxsus mantiq uchun `JdbcAggregateTemplate` va `NamingStrategy`. Hodisalar `BeforeConvertCallback`, `BeforeSaveCallback`, `AfterLoadCallback` orqali ushlanadi; Spring Boot migratsiyani Flyway/Liquibase bilan boshqaradi.

**Qo'llanish keyslari:**
- Mikroservisda kichik, aniq chegarali aggregate'lar (Order + OrderItem) uchun Hibernate o'rniga sodda persistence tanlash.
- CQRS'ning yozish tomonida aggregate'ni to'liq saqlash, o'qish tomonida esa `JdbcTemplate` bilan projection qurish.
- Lazy loading va `LazyInitializationException` muammolarini butunlay yo'q qilish kerak bo'lgan servislarda.
- Native SQL ustidan to'liq nazorat kerak bo'lgan, ammo ORM boilerplate'i keraksiz CRUD servislarida.
- Event-driven tizimda `@DomainEvents` bilan aggregate saqlanganda domen hodisalarini chiqarish.

**Ehtiyot bo'ling:** `save()` child kolleksiyani ko'pincha o'chirib qayta yozadi (delete-then-insert), shuning uchun juda katta kolleksiyali aggregate'larda bu qimmat va foreign key/trigger bilan muammoli bo'ladi. Shuningdek, many-to-many va ikki tomonlama assotsiatsiyalar to'g'ridan-to'g'ri qo'llab-quvvatlanmaydi - aggregate chegaralarini noto'g'ri qo'ysangiz, modelni Hibernate uslubida yozishga urinib qarshilikka uchraysiz.

## 9.35 Spetsifikatsiya (Specification - Spring Data JPA)

**Tavsif:** Qidiruv shartini alohida, qayta ishlatiladigan va kompozitsiyalanadigan obyekt sifatida ifodalash patterni. Har bir Specification bitta predikatni qamrab oladi, ularni `and`/`or`/`not` bilan birlashtirib dinamik so'rov qurish mumkin - shu bilan `findByAAndBAndC...` kabi o'nlab repository metodlari portlashi oldini olinadi. Asosi - JPA Criteria API, ya'ni shartlar type-safe va string konkatenatsiyasiz quriladi.

**Spring'da qayerda uchraydi:** `org.springframework.data.jpa.domain.Specification<T>` interfeysi va `JpaSpecificationExecutor<T>` (`findAll(Specification, Pageable)`, `count`, `exists`, `delete`). Statik yordamchilar: `Specification.where(...)`, `.and(...)`, `.or(...)`, `Specification.allOf(...)`/`anyOf(...)` (Spring Data JPA 3.x). Ichida `Root`, `CriteriaQuery`, `CriteriaBuilder` (`jakarta.persistence.criteria`) ishlatiladi; type-safe maydon nomlari uchun Hibernate JPA Metamodel Generator (`Order_.status`). Alternativalar - Querydsl `QuerydslPredicateExecutor` va Query by Example (`Example.of(...)`).

**Qo'llanish keyslari:**
- Admin panelidagi ko'p filtrli qidiruv (status, sana oralig'i, mijoz, summa) - faqat to'ldirilgan filtrlarni qo'shish.
- Multi-tenancy yoki soft-delete shartini (`deleted = false`) umumiy Specification sifatida barcha so'rovlarga qo'shish.
- Ruxsatga asoslangan filtr: foydalanuvchi roliga qarab ko'rinadigan yozuvlarni cheklovchi Specification.
- Pagination va sorting bilan birga ishlatib, `Page<T>` qaytaruvchi REST qidiruv endpoint'i qurish.
- `@EntityGraph` bilan birlashtirib, filtrlangan natijada N+1'ni oldini olish.

**Ehtiyot bo'ling:** Criteria API batafsil va o'qishga qiyin - murakkab reporting so'rovlari uchun Specification o'rniga oshkora JPQL/native SQL yoki Querydsl tanlash soddaroq bo'ladi. Shuningdek, Specification ichida `root.join(...)`ni har bir predikatda takrorlasangiz, Hibernate bir nechta ortiqcha JOIN yasaydi va natijada dublikat qatorlar paydo bo'ladi - join'ni qayta ishlatish yoki `query.distinct(true)` kerak bo'ladi.

## 9.36 Domen ombori (Domain Store)

**Tavsif:** Domain Store (asli Core J2EE Patterns kataloqidan) - domen obyektlarini saqlash mantiqini ularning o'zidan to'liq ajratib, "shaffof persistence" (transparent persistence) beradigan pattern. Domen sinflari SQL yoki saqlash API'sini bilmaydi: alohida persistence qatlami managed obyektlarni identity map'da kuzatadi, o'zgarganini dirty checking bilan aniqlaydi va transaction oxirida kerakli INSERT/UPDATE/DELETE'ni o'zi generatsiya qiladi. Data Mapper'dan asosiy farqi - mapper chaqiruvi ham ilova kodidan yashirin: obyekt holatini o'zgartirish yetarli, `save()` ni qo'lda chaqirish shart emas. Buning narxi - lazy loading proxy'lari, flush tartibi va cache invalidatsiyasini boshqaruvchi og'ir infratuzilma.

**Spring'da qayerda uchraydi:** Spring ekotizimida bu patternning amaliy ko'rinishi JPA/Hibernate: `jakarta.persistence.EntityManager`, `@Entity`, `@PersistenceContext` va Hibernate ORM 6.x (Spring Boot 3.x/4.x'dagi standart provider, `spring-boot-starter-data-jpa`). Persistence context (first-level cache) - aynan Domain Store yadrosi: `@Transactional` metod ichida managed entity'ning setter'ini chaqirsangiz, commit paytidagi flush'da Hibernate UPDATE yozadi. Yondosh Spring qismlari: `JpaTransactionManager`, `JpaRepository`, `@Version` (optimistic locking), `@EntityGraph`, `@DynamicUpdate`, `@Embeddable`/`@Convert` mapping'lari. Spring Data JDBC esa ataylab Domain Store emas - unda dirty checking va lazy loading yo'q, `save()` aniq chaqiriladi, ya'ni u Data Mapper'ga yaqinroq.

```java
@Transactional
public void renameCustomer(Long id, String newName) {
    Customer c = em.find(Customer.class, id);  // managed obyekt
    c.setName(newName);                        // repository.save() CHAQIRILMAYDI
}                                              // commit -> dirty checking -> UPDATE
```

**Qo'llanish keyslari:**
- Boy domen modeli bo'lgan monolit yoki modular monolitda murakkab agregat o'zgarishlarini bitta transactionda saqlash.
- Aggregate root va uning bola kolleksiyalarini `cascade` hamda `orphanRemoval` bilan yaxlit yozish.
- Konkurent tahrirlash ekranlari: `@Version` orqali optimistic locking va "sizdan oldin kimdir o'zgartirdi" xabarini berish.
- Legacy relational sxemani domen tiliga moslash (`@Embeddable`, `@AttributeOverride`, `@Convert`).
- Hibernate Envers ustida qurilgan audit/versioning tarix jadvallari.

**Ehtiyot bo'ling:** Shaffoflik SQL'ni yashiradi - N+1 so'rov, keraksiz `SELECT`lar va kutilmagan `UPDATE`lar faqat profiling (Hibernate statistics, `spring.jpa.show-sql`, datasource-proxy) bilan ko'rinadi, shuning uchun `spring.jpa.open-in-view` ni `false` qilib, graf yuklanishini `@EntityGraph`/`join fetch` bilan ataylab boshqarish kerak. Hisobot uslubidagi o'qishlar, bulk UPDATE/DELETE va juda yuqori throughput'li yozuvlar uchun Domain Store noto'g'ri tanlov - bunday joylarda `JdbcClient`, jOOQ yoki CQRS o'qish tomoni arzonroq va oldindan bashorat qilinadigan bo'ladi.

## 9.37 Yozuvlar to'plami (Record Set)

**Tavsif:** Record Set - SQL natijasining xotiradagi, jadval shaklidagi va ko'pincha connection'dan ajralgan (disconnected) tasviri: satrlar hamda nomlangan ustunlar to'plami. Xom `ResultSet`dan farqi shunda - u ochiq cursor va connection'ga bog'lanmagan, shuning uchun transaction yopilgandan keyin ham o'qiladi va qatlamlar orasida xavfsiz uzatiladi. Maqsadi - har bir so'rov uchun entity yoki DTO yaratmasdan, tabular ma'lumotni to'g'ridan-to'g'ri hisobot, eksport yoki UI grid'iga yetkazish.

**Spring'da qayerda uchraydi:** Spring'dagi bevosita ifodasi - `org.springframework.jdbc.support.rowset.SqlRowSet` (default implementatsiya `ResultSetWrappingSqlRowSet`) va `JdbcTemplate#queryForRowSet(...)`; u JDK'ning `javax.sql.rowset.CachedRowSet` ustida disconnected ishlaydi hamda checked `SQLException` o'rniga Spring'ning `InvalidResultSetAccessException`ini tashlaydi. Ustun nomlari va turlari `SqlRowSetMetaData` orqali o'qiladi, `SqlRowSetResultSetExtractor` esa ixtiyoriy `query(...)` chaqiruvida shu turni qaytaradi. Yengilroq variant - Spring Framework 6.1+ `JdbcClient`: `sql(...).query().listOfRows()` → `List<Map<String, Object>>`. Spring'dan tashqarida jOOQ `Result<Record>` to'laqonli va type-safe Record Set beradi, toza JDK yo'li esa `RowSetProvider.newFactory().createCachedRowSet()` (Java 17-25).

```java
SqlRowSet rs = jdbcTemplate.queryForRowSet(
        "select region, sum(amount) as total from orders group by region");
while (rs.next()) {                         // connection allaqachon yopilgan
    report.add(rs.getString("region"), rs.getBigDecimal("total"));
}
```

**Qo'llanish keyslari:**
- Ad-hoc analitik hisobotlar va dashboard so'rovlari - har bir aggregatsiya uchun alohida entity/DTO yozmaslik.
- CSV yoki Excel eksporti: ustunlarni metadata bo'yicha dinamik aylanib chiqish.
- Admin paneldagi "ixtiyoriy SQL natijasini grid'da ko'rsatish" funksiyasi, ustunlar oldindan ma'lum bo'lmaganda.
- Ko'p va o'zgaruvchan ustunli legacy stored procedure natijalarini qatlamlar orasida uzatish.
- Migration va reconciliation skriptlarida ikki manbadan olingan tabular natijalarni solishtirish.

**Ehtiyot bo'ling:** Record Set type-safe emas - ustun nomidagi xato yoki tur nomuvofiqligi faqat runtime'da chiqadi, bundan tashqari baza sxemasi service va web qatlamlariga "oqib" ketadi, shuning uchun uning ustiga domen mantiqini qurmang va tashqi API javobi sifatida bermang. Katta natijani butunlay xotiraga yuklash OOM keltiradi: bunday holatda `RowCallbackHandler` va mos `fetchSize` bilan stream qilish yoki kursor/pagination bo'yicha ishlash kerak.

---

[&larr; 8. Biznes logika va Service qatlam patternlari](08-biznes-logika-va-service-qatlam-patternlari.md) · [Mundarija](README.md) · [10. Ma'lumotlarni boshqarish va taqsimlash patternlari &rarr;](10-malumotlarni-boshqarish-va-taqsimlash.md)
