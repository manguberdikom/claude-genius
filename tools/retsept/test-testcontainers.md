# test: Testcontainers

Minimal shakl (testing 8.7, 8.2):

```java
import org.testcontainers.postgresql.PostgreSQLContainer;

@TestConfiguration(proxyBeanMethods = false)
public class ContainersConfig {
    @Bean
    @ServiceConnection
    PostgreSQLContainer postgres() {
        return new PostgreSQLContainer("postgres:16.4-alpine");
    }
}

@SpringBootTest
@Import(ContainersConfig.class)
class OrderRepositoryIT { }
```

- Boot 3 / TC 1.x: `org.testcontainers.containers.PostgreSQLContainer<?>` va `new PostgreSQLContainer<>(...)`; TC 2.x da u deprecated (testing 8.2)

Allaqachon bor, yozmang:
- `spring.datasource.url/username/password` ni qo'lda uzatish o'rniga `@ServiceConnection` (testing 8.3)
- Qotirilgan `localhost:5432` o'rniga `getMappedPort()` yoki `@ServiceConnection` (testing 8.12)
- Konteynerlarni ketma-ket start qilish o'rniga `Startables.deepStart(...)` (testing 8.4)
- Nostandart property (`app.external.base-url`) ni qotirib yozish o'rniga `@DynamicPropertySource` va `Supplier` (testing 8.3)

Tuzoqlar:
- Har sinfda o'z konteyneri yoki `static final` singletonga `@Container` qo'yish start vaqtini ko'paytiradi; bitta bazaviy sinf yoki `@TestConfiguration` bean, `@DirtiesContext` siz (testing 8.4, 8.12)
- `postgres:latest` testni tashqi relizga bog'laydi; prod bilan bir xil aniq versiya yozing (testing 8.12)
- Umumiy konteynerda ma'lumot tozalanmasa testlar tartibga bog'lanadi; `@Transactional` rollback yoki `TRUNCATE ... RESTART IDENTITY CASCADE` (testing 8.12)
- Konteyner testi muntazam yurmasa yiqilishlar bir necha o'zgarishga aralashadi; har partiya oxirida to'liq integration suite bir marta: `run_tests.py --hammasi --yurgiz` (testing 8.12)
