<!-- doc: testing | chapter: 8 | part:  -->

[Barcha hujjatlar](../../README.md) / [Testlash qo'llanmasi](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 8. Testcontainers bilan real infratuzilmada test (Integration Testing with Testcontainers)

<details>
<summary>Bu bobdagi 13 bo'lim</summary>

- [8.1 Nega H2 yoki in-memory baza yetarli emas](#81-nega-h2-yoki-in-memory-baza-yetarli-emas)
- [8.2 Testcontainers asoslari: Docker API ustida hayot aylanishi](#82-testcontainers-asoslari-docker-api-ustida-hayot-aylanishi)
- [8.3 Spring Boot bilan integratsiya: @ServiceConnection va @DynamicPropertySource](#83-spring-boot-bilan-integratsiya-serviceconnection-va-dynamicpropertysource)
- [8.4 Singleton container pattern va kontekst keshi](#84-singleton-container-pattern-va-kontekst-keshi)
- [8.5 Konteynerni qayta ishlatish (reuse)](#85-konteynerni-qayta-ishlatish-reuse)
- [8.6 Turli texnologiyalar uchun konteynerlar](#86-turli-texnologiyalar-uchun-konteynerlar)
- [8.7 Spring Boot Docker Compose qo'llab-quvvatlashi va @TestConfiguration](#87-spring-boot-docker-compose-qollab-quvvatlashi-va-testconfiguration)
- [8.8 Ma'lumotlar bazasi migratsiyasini testlash](#88-malumotlar-bazasi-migratsiyasini-testlash)
- [8.9 Kafka bilan integratsion test](#89-kafka-bilan-integratsion-test)
- [8.10 Tezlik va resurs byudjeti](#810-tezlik-va-resurs-byudjeti)
- [8.11 Testcontainers'ni CI'da ishlatish](#811-testcontainersni-cida-ishlatish)
- [8.12 Anti-patternlar](#812-anti-patternlar)
- [8.13 Arxitektor nazorat ro'yxati](#813-arxitektor-nazorat-royxati)

</details>



Integratsion test faqat "ko'proq bean ko'tarish" degani emas - bu sizning kodingiz ishlab chiqarishda uchraydigan real infratuzilma bilan muloqotini tasdiqlash. Testcontainers (1.19+ va ayniqsa 1.20+) Docker konteynerlarini test hayot aylanishiga bog'laydi, Spring Boot 3.1+ esa `@ServiceConnection` orqali bu konteynerlarni avtomatik konfiguratsiya qiladi, ya'ni property'larni qo'lda yozish zaruriyati yo'qoladi. Bu bobda arxitektor nuqtai nazaridan qaror daraxti beriladi: qachon real konteyner kerak, qanday qilib uni tez va barqaror ushlab turish, va qaysi naqshlar test bazangizni sekin hamda ishonchsiz qiladi.

## 8.1 Nega H2 yoki in-memory baza yetarli emas

H2 `MODE=PostgreSQL` rejimida ham PostgreSQL emulyatori bo'lib qolaveradi - u sintaksisning bir qismini qabul qiladi, lekin semantikasi boshqa. Natijada test yashil, prod qizil bo'ladi. Eng ko'p uchraydigan farqlar:

**SQL dialekti va funksiyalar.** `INSERT ... ON CONFLICT (id) DO UPDATE`, `FILTER (WHERE ...)`, `DISTINCT ON`, `LATERAL JOIN`, window funksiyalarning ayrim shakllari, `generate_series`, `tsvector`/`to_tsquery` full-text izlash, `ILIKE`, massiv tiplari (`text[]`, `unnest`) - H2'da yo yo'q, yo boshqacha ishlaydi. Agar repository'da `@Query(nativeQuery = true)` bo'lsa, H2 testi faqat "metod chaqirildi"ni tasdiqlaydi.

**Tip tizimi.** PostgreSQL'da `jsonb` indekslanadigan va operatorlari (`->>`, `@>`, `jsonb_path_query`) bor haqiqiy tip; H2'da bu `CLOB`/`JSON` ko'rinishida taqlid qilinadi. `numeric` aniqligi, `timestamptz` va `timestamp` farqi, `interval`, `uuid`, `enum` tiplari, `citext` - barchasi xatti-harakat farqi manbai. Klassik bug: `timestamptz` ustunga `LocalDateTime` yozilib, prod'da server time zone UTC bo'lgani uchun soat siljiydi - H2'da bu hech qachon ko'rinmaydi.

**Locking va tranzaksiya izolyatsiyasi.** `SELECT ... FOR UPDATE SKIP LOCKED` (navbat/outbox naqshining asosi), `FOR UPDATE NOWAIT`, advisory lock'lar (`pg_advisory_xact_lock`), `REPEATABLE READ`da seriyalizatsiya xatosi (`40001`), deadlock aniqlanishi va `SQLState` kodlari - H2'da yoki yo'q, yoki boshqa xato kodi beradi. Optimistik/pessimistik locking retry logikasini H2'da sinash deyarli ma'nosiz.

**Sequence va identifier generatsiyasi.** Hibernate `SEQUENCE` strategiyasi, `allocationSize`, `IDENTITY` bilan batch insert o'chib qolishi, `nextval` keshlanishi - PostgreSQL'ga xos. H2'da sekvens raqamlari boshqa tartibda beriladi va "aynan shu ID" ga asoslangan assert'lar yolg'on ishonch beradi.

**Index va constraint xatti-harakati.** Partial index (`WHERE deleted_at IS NULL`), `UNIQUE` index NULL'larni qanday ko'rishi, `GIN`/`GiST`, `CREATE INDEX CONCURRENTLY`, `DEFERRABLE` constraint'lar, `ON DELETE CASCADE` tartibi, unique violation'ning `23505` kodi - real bazada boshqacha. Unique constraint buzilishini "do'stona xato"ga aylantiruvchi handler faqat PostgreSQL'da to'g'ri sinaladi.

**Migratsiya skriptlari.** Bu eng og'riqli nuqta: Flyway/Liquibase skriptlari `CREATE EXTENSION pgcrypto`, `ALTER TYPE ... ADD VALUE`, `CREATE INDEX CONCURRENTLY`, `jsonb_set` ishlatsa, H2 ularni umuman bajara olmaydi. Natijada jamoa "test uchun alohida schema.sql" yozadi - va shu lahzada test real DDL'ni tekshirishdan voz kechadi. Migratsiyani tekshirish qobiliyatini yo'qotish Testcontainers'ga o'tish uchun yetarli yakka sabab.

## 8.2 Testcontainers asoslari: Docker API ustida hayot aylanishi

Testcontainers - Docker daemon'ning HTTP API'si ustidagi Java kutubxonasi. U `DOCKER_HOST`ni aniqlaydi (Docker Desktop, Colima, Podman, Rancher Desktop, Testcontainers Cloud), kerakli image'ni pull qiladi, konteynerni ko'taradi va tozalashni **Ryuk** nomli sidecar konteynerga topshiradi: JVM to'satdan o'lsa ham Ryuk label'i bo'yicha konteynerlarni o'chiradi, ya'ni "orfan" konteynerlar qolmaydi.

Hayot aylanishi: `start()` → image pull → create → start → wait strategy bajariladi → konteyner "ready" deb belgilanadi → test ishlaydi → `stop()`/Ryuk tozalaydi.

**Port mapping muhim arxitektura detali.** Konteyner ichidagi port (masalan 5432) host'da **tasodifiy ephemeral portga** map qilinadi. Shuning uchun hech qachon `localhost:5432` deb qo'lda yozmaysiz - `container.getMappedPort(5432)`, `getHost()`, `getJdbcUrl()`, `getBootstrapServers()` metodlarini ishlatasiz. Bu random port parallel testlarda to'qnashuvni o'z-o'zidan hal qiladi.

JUnit 5 integratsiyasi Testcontainers ning JUnit Jupiter modulidan keladi (artifactId versiyaga bog'liq, pastdagi pom ga qarang): `@Testcontainers` annotatsiyasi extension'ni yoqadi, `@Container` esa maydonni boshqaradi - **instance** maydon har test metodidan oldin yangi konteyner ko'taradi, **static** maydon butun sinf uchun bir marta. Prodga yaqin loyihada deyarli hamma vaqt `static` to'g'ri javob.

Wait strategiyasi - barqarorlikning kaliti. Uch asosiy tur: `Wait.forListeningPort()` (TCP ochilishi - eng zaif, chunki port ochilishi "xizmat tayyor" degani emas), `Wait.forLogMessage(regex, times)` (log'dagi tayyorlik satrini kutish), `Wait.forHttp("/health").forStatusCode(200)` (HTTP probe). Qo'shimcha: `Wait.forHealthcheck()` agar image'da Docker HEALTHCHECK bo'lsa, va `Wait.forSuccessfulCommand(...)`. Modullarning o'z default strategiyasi bor (`PostgreSQLContainer` log'dagi tayyorlik xabarini ikki marta kutadi), lekin custom image yoki o'z app konteyneringiz uchun strategiyani ochiq yozish shart.

Modul nomi Testcontainers versiyasiga bog'liq. Spring Boot 3.5 Testcontainers 1.21 ni boshqaradi, Spring Boot 4 esa 2.x ni ([spring-boot-dependencies 3.5.0](https://repo1.maven.org/maven2/org/springframework/boot/spring-boot-dependencies/3.5.0/spring-boot-dependencies-3.5.0.pom) da `1.21.0`, [4.0.0](https://repo1.maven.org/maven2/org/springframework/boot/spring-boot-dependencies/4.0.0/spring-boot-dependencies-4.0.0.pom) da `2.0.2`). 2.x da har modul `testcontainers-` prefiksini oldi ([testcontainers-bom 2.0.5](https://repo1.maven.org/maven2/org/testcontainers/testcontainers-bom/2.0.5/testcontainers-bom-2.0.5.pom) da eski `postgresql`, `junit-jupiter`, `kafka` nomlari yo'q). Boot 4 loyihasiga eski nom ko'chirilsa Maven versiyasi yo'q dependency deb build ni to'xtatadi.

Spring Boot 3.5 (Testcontainers 1.21):

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-testcontainers</artifactId>
  <scope>test</scope>
</dependency>
<dependency>
  <groupId>org.testcontainers</groupId>
  <artifactId>junit-jupiter</artifactId>
  <scope>test</scope>
</dependency>
<dependency>
  <groupId>org.testcontainers</groupId>
  <artifactId>postgresql</artifactId>
  <scope>test</scope>
</dependency>
<dependency>
  <groupId>org.awaitility</groupId>
  <artifactId>awaitility</artifactId>
  <scope>test</scope>
</dependency>
```

Spring Boot 4 (Testcontainers 2.x), farq faqat ikki artifactId da:

```xml
<dependency>
  <groupId>org.testcontainers</groupId>
  <artifactId>testcontainers-junit-jupiter</artifactId>
  <scope>test</scope>
</dependency>
<dependency>
  <groupId>org.testcontainers</groupId>
  <artifactId>testcontainers-postgresql</artifactId>
  <scope>test</scope>
</dependency>
```

Testcontainers 2.x da modul sinflari ham o'z paketiga ko'chdi: yangi kodda generiksiz `org.testcontainers.postgresql.PostgreSQLContainer` ishlatiladi. Eski generik `org.testcontainers.containers.PostgreSQLContainer<SELF>` 2.x jar ida `@Deprecated` bo'lib qolgan, ya'ni bu bobdagi `PostgreSQLContainer<?>` misollari 2.x da deprecation ogohlantirishi bilan kompilyatsiya bo'ladi. `-Xlint:all -Werror` yoqilgan loyihada esa yangi sinfga o'tish kerak.

Testcontainers versiyasini qo'lda yozmang: `spring-boot-dependencies` BOM uni boshqaradi, aks holda `org.testcontainers:testcontainers-bom` import qiling.

## 8.3 Spring Boot bilan integratsiya: @ServiceConnection va @DynamicPropertySource

Spring Boot 3.1'dan beri eng toza usul - `@ServiceConnection`. U `ConnectionDetails` bean'ini yaratadi va auto-konfiguratsiya property'lar o'rniga shu bean'dan foydalanadi. Siz URL, username, password, driver nomini yozmaysiz; konteyner turiga qarab Boot o'zi aniqlaydi.

```java
@SpringBootTest
@Testcontainers
class OrderRepositoryIT {

    @Container
    @ServiceConnection
    static PostgreSQLContainer<?> postgres =
            new PostgreSQLContainer<>("postgres:16.4-alpine");

    @Autowired
    OrderRepository repository;

    @Test
    void saves_and_reads_back_jsonb_payload() {
        Order saved = repository.save(new Order("A-1", Map.of("ref", "X")));

        Order found = repository.findById(saved.getId()).orElseThrow();

        assertThat(found.getPayload()).containsEntry("ref", "X");
    }
}
```

Boot 3.1'dan oldingi (va hali ham qo'l keladigan) usul - `@DynamicPropertySource`: konteyner ko'tarilgandan keyin `Environment`ga property qo'shiladi. `Supplier` ishlatilgani uchun qiymat kech, ya'ni konteyner start bo'lgandan keyin o'qiladi.

```java
@SpringBootTest
@Testcontainers
class LegacyPropertiesIT {

    @Container
    static PostgreSQLContainer<?> postgres =
            new PostgreSQLContainer<>("postgres:16.4-alpine")
                    .waitingFor(Wait.forListeningPort());

    @DynamicPropertySource
    static void datasource(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", postgres::getJdbcUrl);
        registry.add("spring.datasource.username", postgres::getUsername);
        registry.add("spring.datasource.password", postgres::getPassword);
    }
}
```

Taqqoslash: `@ServiceConnection` kamroq kod, property nomini xato yozish imkoni yo'q, Boot qo'llab-quvvatlagan barcha xizmatlar uchun bir xil, va SSL/credential detallarini o'zi uzatadi. `@DynamicPropertySource` esa moslashuvchan - `@ServiceConnection` qo'llab-quvvatlamaydigan xizmatlar (masalan custom `app.external.base-url`, LocalStack endpoint'lari, Keycloak issuer URI) uchun hamon kerak. Amaliy qoida: **standart infratuzilma uchun `@ServiceConnection`, nostandart property'lar uchun `@DynamicPropertySource`** - ikkisi bir sinfda bemalol yashaydi.

## 8.4 Singleton container pattern va kontekst keshi

Agar har integratsion test sinfi o'z konteynerini ko'tarsa, 40 sinfli loyihada 40 marta PostgreSQL start bo'ladi. Singleton container pattern buni oldini oladi: konteyner `static final` maydonda, JVM ichida bir marta ko'tariladi va JVM tugashida Ryuk tozalaydi. `@Container` annotatsiyasi **ishlatilmaydi** - aks holda JUnit uni sinf oxirida to'xtatib qo'yadi.

```java
@SpringBootTest
@ActiveProfiles("integration")
public abstract class AbstractIntegrationTest {

    static final PostgreSQLContainer<?> POSTGRES =
            new PostgreSQLContainer<>("postgres:16.4-alpine");

    static final KafkaContainer KAFKA =
            new KafkaContainer("apache/kafka:3.8.0");

    static {
        Startables.deepStart(POSTGRES, KAFKA).join();
    }

    @DynamicPropertySource
    static void props(DynamicPropertyRegistry registry) {
        registry.add("spring.datasource.url", POSTGRES::getJdbcUrl);
        registry.add("spring.datasource.username", POSTGRES::getUsername);
        registry.add("spring.datasource.password", POSTGRES::getPassword);
        registry.add("spring.kafka.bootstrap-servers", KAFKA::getBootstrapServers);
    }
}
```

`Startables.deepStart(...)` konteynerlarni **parallel** ko'taradi - PostgreSQL va Kafka ketma-ket emas, bir vaqtda start bo'ladi.

Bu naqsh Spring'ning kontekst keshi bilan birga ishlaganda haqiqiy samara beradi. Spring TestContext Framework kontekstni konfiguratsiya "kaliti" bo'yicha keshlaydi: bir xil `@SpringBootTest` atributlari, bir xil profil, bir xil `@MockitoBean` to'plami → **bitta kontekst**. Bazaviy sinfdan meros olgan barcha testlar ayni kalitni ulashadi, demak kontekst ham, konteyner ham bir marta ko'tariladi. Shuning uchun: bazaviy sinflar sonini minimal saqlang, test sinflarida qo'shimcha `@TestPropertySource` yoki ad-hoc mock qo'shib kalitni "sindirmang". `@DirtiesContext` ni esa integratsion testlarda umuman ishlatmang - u keshni tashlab, keyingi sinfga to'liq qayta start narxini yuklaydi.

## 8.5 Konteynerni qayta ishlatish (reuse)

Reuse - JVM tugaganda ham konteynerni tirik qoldirish: keyingi test ishga tushganda tayyor konteyner topiladi va start vaqti nolga yaqinlashadi. Yoqish uchun ikki shart birga kerak: konteynerda `.withReuse(true)` va developer mashinasida `~/.testcontainers.properties` faylida `testcontainers.reuse.enable=true`. Bu fayl **repoga qo'shilmaydi** - bu developer'ning shaxsiy sozlamasi.

Reuse yoqilganda Ryuk o'sha konteynerni o'chirmaydi va Testcontainers konteyner konfiguratsiyasidan hash hisoblab mavjudini topadi; konfiguratsiyani o'zgartirsangiz (image tag, env, buyruq) yangi konteyner ko'tariladi.

Muhim nozik jihat: reuse'da **ma'lumot ham saqlanadi**. Lokalda ketma-ket ishlatilgan testlar bir-birining qoldiqlarini ko'radi. Shuning uchun reuse strategiyasi albatta ishonchli tozalash bilan juftlanadi - har test uchun `@Transactional` rollback, yoki har klass oldidan `TRUNCATE ... RESTART IDENTITY CASCADE`, yoki har run uchun alohida schema. CI'da reuse **o'chirilgan** bo'lishi kerak: runner har safar yangi, hash topilmaydi, va "nopok holat" xavfini CI'ga olib kirish mantiqsiz. Natijada ikki rejim: lokal - tez va reuse'li, CI - toza va takrorlanadigan.

## 8.6 Turli texnologiyalar uchun konteynerlar

| Texnologiya | Modul, TC 1.x (Boot 3.5) | Modul, TC 2.x (Boot 4) | Konteyner sinfi | Spring'da ulash usuli |
|---|---|---|---|---|
| PostgreSQL | `org.testcontainers:postgresql` | `org.testcontainers:testcontainers-postgresql` | `PostgreSQLContainer` | `@ServiceConnection` |
| MySQL / MariaDB | `mysql`, `mariadb` | `testcontainers-mysql`, `testcontainers-mariadb` | `MySQLContainer`, `MariaDBContainer` | `@ServiceConnection` |
| Kafka (apache/kafka) | `org.testcontainers:kafka` | `org.testcontainers:testcontainers-kafka` | `org.testcontainers.kafka.KafkaContainer` | `@ServiceConnection` |
| Kafka (Confluent) | `org.testcontainers:kafka` | `org.testcontainers:testcontainers-kafka` | `ConfluentKafkaContainer` | `@ServiceConnection` |
| Redis | `GenericContainer` yoki `com.redis:testcontainers-redis` | ikkalasida bir xil | `GenericContainer`, `RedisContainer` | `@ServiceConnection(name = "redis")` |
| MongoDB | `org.testcontainers:mongodb` | `org.testcontainers:testcontainers-mongodb` | `MongoDBContainer` | `@ServiceConnection` |
| Elasticsearch | `org.testcontainers:elasticsearch` | `org.testcontainers:testcontainers-elasticsearch` | `ElasticsearchContainer` | `@ServiceConnection` |
| OpenSearch | `org.opensearch:opensearch-testcontainers` | ikkalasida bir xil | `OpensearchContainer` | `@DynamicPropertySource` |
| RabbitMQ | `org.testcontainers:rabbitmq` | `org.testcontainers:testcontainers-rabbitmq` | `RabbitMQContainer` | `@ServiceConnection` |
| LocalStack (S3, SQS) | `org.testcontainers:localstack` | `org.testcontainers:testcontainers-localstack` | `LocalStackContainer` | `@DynamicPropertySource` |
| Keycloak | `com.github.dasniko:testcontainers-keycloak` | ikkalasida bir xil | `KeycloakContainer` | `@DynamicPropertySource` (issuer-uri) |
| Ixtiyoriy image | `org.testcontainers:testcontainers` | ikkalasida bir xil | `GenericContainer` | `@DynamicPropertySource` |

TC 2.x ustunidagi nomlar [testcontainers-bom 2.0.5](https://repo1.maven.org/maven2/org/testcontainers/testcontainers-bom/2.0.5/testcontainers-bom-2.0.5.pom) dan olingan. 2.x da sinflar ham modul paketiga ko'chgan (`org.testcontainers.postgresql.PostgreSQLContainer`, `org.testcontainers.mysql.MySQLContainer`, `org.testcontainers.localstack.LocalStackContainer`), `org.testcontainers.containers` dagi eski nomlar esa `@Deprecated` bo'lib qolgan.

`org.testcontainers.containers.KafkaContainer` (Confluent image'ga bog'langan eski sinf) 1.20'dan boshlab deprecated; yangi kodda `org.testcontainers.kafka.KafkaContainer` (apache/kafka image, KRaft rejimi) yoki `ConfluentKafkaContainer` ishlatiladi.

LocalStack misoli - bu yerda `@ServiceConnection` yo'q, endpoint'ni o'zingiz uzatasiz:

```java
static final LocalStackContainer LOCALSTACK =
        new LocalStackContainer(DockerImageName.parse("localstack/localstack:3.8"))
                .withServices(Service.S3, Service.SQS);

@DynamicPropertySource
static void aws(DynamicPropertyRegistry registry) {
    registry.add("app.aws.endpoint", () -> LOCALSTACK.getEndpoint().toString());
    registry.add("app.aws.region", LOCALSTACK::getRegion);
    registry.add("app.aws.access-key", LOCALSTACK::getAccessKey);
    registry.add("app.aws.secret-key", LOCALSTACK::getSecretKey);
}
```

## 8.7 Spring Boot Docker Compose qo'llab-quvvatlashi va @TestConfiguration

`spring-boot-docker-compose` moduli (3.1+) - bu **dev-time** qulayligi: `compose.yaml` loyiha ildizida bo'lsa, `bootRun`/`bootTestRun` ilovani ko'targanda `docker compose up` ni o'zi bajaradi va servislarni `ConnectionDetails` sifatida ulanadi, ilova to'xtaganda `down` qiladi.

```yaml
services:
  postgres:
    image: postgres:16.4-alpine
    environment:
      POSTGRES_DB: app
      POSTGRES_USER: app
      POSTGRES_PASSWORD: app
    ports:
      - '5432'
  redis:
    image: redis:7.4-alpine
    ports:
      - '6379'
```

Farqi aniq: Docker Compose qo'llab-quvvatlashi **umumiy, uzoq yashovchi** muhit beradi (developer ilovani qo'lda ko'targanda), Testcontainers esa **test hayot aylanishiga bog'langan, izolyatsiyalangan** muhit beradi (har run uchun toza, random port, programmatik boshqaruv). Compose'ni avtomatik testlarga asos qilish xato: port fiksatsiyalangan, holat bo'linadi, CI'da fayl mavjudligiga bog'liq bo'ladi. Shuning uchun `spring.docker.compose.enabled: false` ni test profilida qo'yib, dev-time va test-time ni qat'iy ajratish tavsiya etiladi. Aksincha yo'nalish ham mumkin: Testcontainers'ni `compose.yaml` o'rniga dev rejimda ishlatish (`@TestConfiguration` + `SpringApplication.from(...).with(...)` bilan `TestMyApplication` klassi).

Konteynerlarni bean sifatida e'lon qilish - eng qayta ishlatiladigan shakl:

```java
@TestConfiguration(proxyBeanMethods = false)
public class ContainersConfig {

    @Bean
    @ServiceConnection
    PostgreSQLContainer<?> postgres() {
        return new PostgreSQLContainer<>("postgres:16.4-alpine");
    }

    @Bean
    @ServiceConnection(name = "redis")
    GenericContainer<?> redis() {
        return new GenericContainer<>("redis:7.4-alpine")
                .withExposedPorts(6379)
                .waitingFor(Wait.forLogMessage(".*Ready to accept connections.*\\n", 1));
    }
}
```

Test sinfida `@Import(ContainersConfig.class)` yetarli. Bean bo'lgani uchun konteyner hayot aylanishi Spring kontekstiga bog'lanadi, ya'ni kontekst keshida qolgan ekan konteyner ham tirik - bu singleton pattern'ning idiomatik Spring varianti. `@ServiceConnection(name = "redis")` dagi `name` - image nomi emas, **connection detail turini** aniqlash uchun ishlatiladigan xizmat nomi; `GenericContainer` bilan ishlaganda shu sababli majburiy.

## 8.8 Ma'lumotlar bazasi migratsiyasini testlash

Real bazadagi eng qimmatli test - migratsiyaning o'zi. Minimal daraja: ilova konteksti ko'tarilganda Flyway/Liquibase barcha skriptlarni real PostgreSQL'da bajaradi. Bu allaqachon H2 bermaydigan qiymat: noto'g'ri DDL, mavjud bo'lmagan extension, buzilgan checksum shu zahoti ko'rinadi.

Keyingi daraja - maqsadli migratsiya testlari:

```java
@Test
void migration_v12_backfills_legacy_rows() {
    Flyway baseline = Flyway.configure()
            .dataSource(POSTGRES.getJdbcUrl(), POSTGRES.getUsername(), POSTGRES.getPassword())
            .target(MigrationVersion.fromVersion("11"))
            .load();
    baseline.migrate();
    jdbc.update("INSERT INTO orders(id, code) VALUES (1, 'A-1')");

    Flyway upgrade = Flyway.configure()
            .dataSource(POSTGRES.getJdbcUrl(), POSTGRES.getUsername(), POSTGRES.getPassword())
            .load();
    upgrade.migrate();

    assertThat(upgrade.info().current().getVersion().getVersion()).isEqualTo("12");
    assertThat(jdbc.queryForObject("SELECT status FROM orders WHERE id = 1", String.class))
            .isEqualTo("LEGACY");
}
```

Bu test eng muhim savolga javob beradi: **yangi migratsiya eski ma'lumot bilan ishlaydimi?** Bo'sh bazada o'tgan `ALTER TABLE ... SET NOT NULL` real tarixiy NULL'lar borida yiqiladi.

Boshqa tekshiruvlar:
- **Orqaga qaytmaslik prinsipi**: `flyway.validate()` va CI'da checksum tekshiruvi - allaqachon bajarilgan skriptni tahrirlash taqiqlanadi. Flyway'da `undo` faqat Teams'da, Liquibase'da `rollback` bloki bor, lekin arxitektura qarori sifatida "forward-only migration" tavsiya etiladi: orqaga qaytarish o'rniga tuzatuvchi yangi migratsiya.
- **Zero-downtime**: expand/contract naqshi. Test N-1 versiya kodi N versiya schema'si bilan ishlashini tasdiqlaydi - eski entity mapping bilan yangi schema'ga `INSERT` qilib ko'ring. Yangi ustun `NOT NULL DEFAULT` bilan qo'shilgani, eski ustun darhol o'chirilmagani, rename o'rniga "yangi ustun + backfill + eski ustunni keyingi relizda o'chirish" ketma-ketligi bajarilgani shu testda ko'rinadi.
- **Liquibase** uchun xuddi shu yondashuv: `SpringLiquibase` bean'ini sozlab `setChangeLog(...)`, yoki `liquibase.update(new Contexts(...))` bilan ma'lum tag'gacha yugurtirib, keyin qolganini bajarish.
- **Idempotentlik**: migratsiyani ikki marta ishga tushirsangiz, ikkinchisi hech narsa qilmasligi kerak.
- **Entity va sxema kontrakti**: `@Column(length = n)` sxemadagi `VARCHAR(n)` ga teng bo'lsin, view ga bog'langan entity larda ham. Farq jim yuradi: kichik testlar o'tadi, uzun qiymat esa faqat real bazada yoki productionda yiqiladi. Schema-mapping kontrakt testi (Hibernate metadata dagi ustun uzunligini `information_schema.columns` bilan solishtirish) bunday farqni ushlaydi.

## 8.9 Kafka bilan integratsion test

Kafka'da mock broker (`EmbeddedKafka`) mavjud, lekin real brokerda sinaladigan narsalar boshqa: serializer/deserializer xatolari, partition assignment, consumer group rebalansi, `auto.offset.reset` semantikasi, retry/backoff va dead letter topic marshrutizatsiyasi, transactional producer.

Test dizaynining uch qoidasi. Birinchi: **consumer group'ni har test uchun unikal qiling** (`group-id: test-` + UUID) yoki topik nomini randomlashtiring - aks holda oldingi testning offset'i keyingisini "xabar yo'q" holatiga olib keladi. Ikkinchi: producer `send(...)` dan keyin **`get()` bilan metadata'ni kutib** olish - bu xabar brokerga yetganini tasdiqlaydi. Uchinchi: natijani Awaitility bilan kutish, hech qachon `Thread.sleep` bilan emas.

```java
@Test
void failed_message_lands_in_dead_letter_topic() {
    List<String> received = new CopyOnWriteArrayList<>();
    try (KafkaConsumer<String, String> dlt = newConsumer(UUID.randomUUID().toString())) {
        dlt.subscribe(List.of("orders.DLT"));

        kafkaTemplate.send("orders", "broken-payload").get(5, TimeUnit.SECONDS);

        await().atMost(Duration.ofSeconds(20))
                .pollInterval(Duration.ofMillis(250))
                .untilAsserted(() -> {
                    dlt.poll(Duration.ofMillis(200))
                       .forEach(r -> received.add(r.value()));
                    assertThat(received).isNotEmpty();
                });
    }
    assertThat(received).containsExactly("broken-payload");
}
```

DLT xatti-harakatini tasdiqlash uchun `DefaultErrorHandler` + `DeadLetterPublishingRecoverer` konfiguratsiyasini test profilida ham yoqilgan holda qoldiring va `FixedBackOff` intervalini test uchun kichraytiring (masalan `new FixedBackOff(100L, 2L)`), aks holda prod'dagi 10 sekundlik backoff testni cho'zadi. Offset'ni tekshirish kerak bo'lsa `AdminClient.listConsumerGroupOffsets(groupId)` ishlatiladi - bu consumer kommit qilganini (ya'ni xabar qayta ishlangani) deklarativ tasdiqlaydi.

## 8.10 Tezlik va resurs byudjeti

Tipik start vaqtlari (image allaqachon lokalda bo'lganda, o'rtacha developer mashinasi): PostgreSQL alpine ~1-3 s, MySQL ~5-10 s, Redis <1 s, RabbitMQ ~3-6 s, Kafka (KRaft) ~5-10 s, MongoDB ~2-4 s, LocalStack ~5-15 s, Elasticsearch/OpenSearch ~15-35 s, Keycloak ~10-20 s. Image birinchi marta pull qilinsa, ustiga 10-90 s qo'shiladi. Spring kontekstining o'zi odatda 2-6 s.

Shundan byudjet qoidasi: integratsion test to'plami lokalda 2-4 daqiqada, CI'da 10 daqiqada tugashi kerak; agar oshsa, bu arxitektura muammosi, "testlar shunchaki sekin" emas.

Optimizatsiya ro'yxati, ta'sir bo'yicha tartiblangan:
1. **Konteynerlar sonini kamaytirish**: bir baza konteyneriga ko'p schema; bir Kafka'ga ko'p topik.
2. **Kontekst keshini saqlash**: bitta `AbstractIntegrationTest`, `@DirtiesContext` yo'q, `@MockitoBean` to'plamini unifikatsiya qilish.
3. **Parallel start**: `Startables.deepStart(...)`.
4. **Yengil image**: `-alpine` variantlar, Elasticsearch o'rniga imkon bo'lsa yengil alternativ.
5. **Reuse** lokalda.
6. **Pre-pull** CI'da (keyingi bo'lim).
7. **Parallel test**: JUnit 5 `junit-platform.properties` da `junit.jupiter.execution.parallel.enabled=true` va `...mode.default=same_thread`, `...mode.classes.default=concurrent`. Port to'qnashuvi random mapping tufayli bo'lmaydi - **agar** `FixedHostPortGenericContainer` yoki `withCreateContainerCmdModifier` bilan fiksatsiyalangan port ishlatmasangiz; ularni butunlay taqiqlash kerak. Haqiqiy xavf - umumiy baza ustida parallel yozuv, shuning uchun parallel rejimda har sinfga alohida schema yoki alohida tranzaksiya izolyatsiyasi kerak.
8. **Testlarni ajratish**: `*Test` (unit, har commit'da) va `*IT` (integratsion, Maven `failsafe` yoki Gradle alohida `integrationTest` task'ida).
9. **tmpfs**: `.withTmpFs(Map.of("/var/lib/postgresql/data", "rw"))` - disk I/O ni olib tashlaydi, baza ma'lumotini saqlash kerak bo'lmagan testlarda sezilarli tezlanish.
10. **Resurs chegarasi**: Docker Desktop'ga kamida 4 CPU / 8 GB RAM; CI runner'da konteynerlar sonini xotiraga moslab cheklash.

## 8.11 Testcontainers'ni CI'da ishlatish

Yagona qattiq talab - CI agent'ida ishlaydigan Docker daemon'ga kirish. Variantlar:

**Docker socket (DooD)** - eng keng tarqalgan: agent konteyneriga `/var/run/docker.sock` mount qilinadi. Tez, lekin konteynerlar host daemon'da ko'tarilgani uchun izolyatsiya kamroq va `localhost` marshrutizatsiyasi nozik.

**Docker-in-Docker (DinD)** - `docker:dind` service konteyneri, `privileged: true` kerak. To'liq izolyatsiya, lekin har job'da image keshini qaytadan to'ldiradi (sekinlashtiradi), ba'zi platformalarda privileged taqiqlangan.

**GitHub Actions** - `ubuntu-*` runner'larda Docker allaqachon o'rnatilgan, hech qanday qo'shimcha sozlash kerak emas: `./mvnw verify` shundayin ishlaydi. `macos-*` va `windows-*` runner'larda Linux konteynerlari uchun Docker **yo'q** - bu ko'p jamoalarni kutilmagan holda urgan fakt.

**Testcontainers Cloud** - Docker daemon'ni masofaviy, boshqariladigan muhitga ko'chiradi (`DOCKER_HOST` ni agent o'rnatadi). Runner'da Docker bo'lmaganda, privileged ruxsat yo'q bo'lganda yoki parallellikni oshirish kerak bo'lganda yechim; narx va tashqi xizmatga bog'liqlik - kelishuv nuqtasi.

**Pre-pull** - eng arzon optimizatsiya: image'larni test start bo'lishidan oldin, mustaqil step'da yuklab olish. Bu pull vaqtini wait strategiya timeout'idan chiqaradi va flaky "container did not start" xatolarini kamaytiradi.

```yaml
jobs:
  integration-test:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: '21'
          cache: maven
      - name: Pre-pull container images
        run: |
          docker pull postgres:16.4-alpine
          docker pull apache/kafka:3.8.0
      - name: Run integration tests
        run: ./mvnw -B verify -Pintegration
```

Yana ikki amaliy nuqta: korporativ muhitda Docker Hub rate limit'ini chetlab o'tish uchun `testcontainers.properties` da `hub.image.name.prefix` bilan ichki registry prefiksini bering; va Ryuk'ni faqat u ishlamaydigan platformalarda (`TESTCONTAINERS_RYUK_DISABLED=true`) o'chiring - aks holda orfan konteynerlar CI agent'ini to'ldiradi.

Mavzuning to'liq yozuvi [Testcontainers](#82-testcontainers-asoslari-docker-api-ustida-hayot-aylanishi) bo'limida; bu yerda faqat shu bo'limning nuqtai nazari.

## 8.12 Anti-patternlar

**Har test sinfida yangi konteyner.** `@Container` ni instance maydonda ishlatish yoki har sinfda alohida `PostgreSQLContainer` e'lon qilish. Natija: 40 sinf × 2 s = 80 s faqat start uchun, plus kontekst keshi buzilishi. Yechim - bitta abstract bazaviy sinf yoki `@TestConfiguration` bean'lari.

**Konteyner ichida ma'lumotni tozalamaslik.** Singleton konteyner + tozalash yo'q = testlar tartibiga bog'liq. "Lokalda o'tadi, CI'da yiqiladi" ning asosiy sababi. Yechim: `@Transactional` rollback o'qish-yozish testlari uchun, `TRUNCATE ... RESTART IDENTITY CASCADE` yoki schema-per-class aksincha holatlar uchun.

**Testlar orasida umumiy holat.** Statik `List`da yig'ilgan event'lar, umumiy Kafka consumer group, umumiy Redis kalitlari, `@MockitoBean` ustiga oldingi testdan qolgan `when(...)`. Har test o'z nomlar maydonini (topic suffix, key prefix, tenant ID) olishi kerak.

**`Thread.sleep` bilan kutish.** Asinxron natijani kutishda sleep ikki yo'l bilan yomon: sekin (har doim to'liq kutadi) va ishonchsiz (sekin CI'da yetmaydi). Awaitility `await().atMost(...).untilAsserted(...)` yagona to'g'ri javob - tez muhitda bir necha millisekundda tugaydi.

**`latest` tag.** `postgres:latest`, `confluentinc/cp-kafka:latest` - bu testlarni tashqi relizlarga bog'laydi: bir kun major versiya chiqadi va butun pipeline yiqiladi, kod o'zgarmagan holda. Har doim aniq versiyani (ideal holda digest'ni) yozing va prod versiyasiga mos qiling: prodda PostgreSQL 16 bo'lsa, testda ham 16.

**Integration testlarni uzoq yurgizmaslik.** Integration testlar CI da yoki lokal muntazam yurmasa, ko'p fazali refaktoringdan keyin ommaviy yiqiladi va sabablar bir-biriga aralashadi. Har partiya (faza) oxirida to'liq integrationTest ni bir marta yurgizing, shunda yiqilish aynan shu partiyaga bog'lanadi.

Qo'shimcha ikki xato: **`FixedHostPortGenericContainer`** (parallellikni o'ldiradi) va **mapped port'ni qo'lda yozish** (`localhost:5432`). Ikkisi ham `getMappedPort()`/`@ServiceConnection` bilan almashtiriladi.

## 8.13 Arxitektor nazorat ro'yxati

- [ ] Barcha integratsion testlar real baza (Testcontainers) ustida ishlaydi; H2/in-memory baza test uchun ishlatilmaydi va `schema.sql` dublikati yo'q.
- [ ] Bitta `AbstractIntegrationTest` (yoki `@TestConfiguration` + `@ServiceConnection` bean'lari) mavjud; konteynerlar `static` va `Startables.deepStart` bilan parallel ko'tariladi.
- [ ] Spring kontekst keshi buzilmaydi: `@DirtiesContext` yo'q, test sinflarida ad-hoc property/mock qo'shilmaydi, kontekst sonlari o'lchab turiladi.
- [ ] Har bir konteyner image'i aniq versiya tag bilan yopishtirilgan (`latest` yo'q) va prod versiyasiga mos.
- [ ] Wait strategiyasi har bir custom konteyner uchun ochiq belgilangan; test kodida `Thread.sleep` yo'q, asinxron kutish faqat Awaitility bilan.
- [ ] Testlar orasidagi tozalash strategiyasi yozib qo'yilgan (rollback / TRUNCATE / schema-per-class) va reuse yoqilgan lokal muhitda ham ishlaydi.
- [ ] Migratsiya testlari bor: to'liq Flyway/Liquibase ishga tushishi, eski ma'lumot bilan yangi migratsiya, forward-only va zero-downtime (expand/contract) tekshiruvi.
- [ ] CI'da Docker mavjudligi tasdiqlangan, image'lar pre-pull qilinadi, reuse o'chirilgan va integratsion test to'plami kelishilgan vaqt byudjetidan oshmaydi.

---

[&larr; 7. Integratsion test: Spring Boot slice testlari](07-integratsion-test-spring-boot-slice-testlari.md) · [Mundarija](README.md) · [9. Tashqi servislarni taqlid qilish va contract testing &rarr;](09-tashqi-servislarni-taqlid-qilish-va.md)
