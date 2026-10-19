# Lombok

Minimal shakl (sonarqube 41.5):

```java
@Entity
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@ToString(onlyExplicitlyIncluded = true)
public class Order {
    @Id @GeneratedValue
    private Long id;

    @ToString.Include
    @Column(nullable = false, unique = true, updatable = false)
    private String orderNumber;

    public Order(String orderNumber) {
        this.orderNumber = Objects.requireNonNull(orderNumber);
    }
}
```

Allaqachon bor, yozmang:
- qo'lda `final` maydonli konstruktor o'rniga `@RequiredArgsConstructor` (clean-code 26.10)
- qo'lda `static final Logger` o'rniga `@Slf4j` (sonarqube 41.7)
- DTO, command, event uchun Lombok klass o'rniga `record` va kompakt konstruktor (sonarqube 41.8)
- review da `@Data` ni qidirish o'rniga `lombok.config` dagi `lombok.data.flagUsage` (sonarqube 41.3)

Tuzoqlar:
- Entity ustida `@Data` `HashSet` va lazy yuklashni buzadi: `@Getter`, tenglik esa o'zgarmas biznes kaliti ustida qo'lda (sonarqube 41.5)
- `@Builder` hech narsa tekshirmaydi: uni private konstruktor ustiga qo'yib `requireNonNull` yozing; bunda `@Builder.Default` ishlamaydi, boshlang'ich qiymat konstruktorda beriladi (sonarqube 41.6)
- Getter uchun test yozib coverage ko'tarmang: `lombok.addLombokGeneratedAnnotation = true` generatsiyani filtrlaydi (sonarqube 41.3)
