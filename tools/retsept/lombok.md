# Lombok

Minimal shakl (clean-code 26.10, 26.1):

```java
@Service
@RequiredArgsConstructor
class OrderService {
    private final OrderRepository orders;
}
```

Allaqachon bor, yozmang:
- DTO, command, event uchun Lombok klass o'rniga `record` va kompakt konstruktor (sonarqube 41.8)
- review da `@Data` ni qidirish o'rniga `lombok.config` dagi `lombok.data.flagUsage` (sonarqube 41.3)

Tuzoqlar:
- Entity da `@Data`, `@Setter`, `@EqualsAndHashCode`, `@ToString` yo'q: `@Getter` va `@NoArgsConstructor(access = AccessLevel.PROTECTED)`, `equals`/`hashCode` entity kartasidagi id shaklida (clean-code 26.10, 28.2, 28.1)
- `@SneakyThrows` yo'q: checked istisno imzoda yoki domen istisnosiga o'raladi (clean-code 26.10)
- `@Builder` hech narsa tekshirmaydi: uni private konstruktor ustiga qo'yib `requireNonNull` yozing; bunda `@Builder.Default` ishlamaydi, boshlang'ich qiymat konstruktorda beriladi (sonarqube 41.6)
- Getter uchun test yozib coverage ko'tarmang: `lombok.addLombokGeneratedAnnotation = true` generatsiyani filtrlaydi (sonarqube 41.3)
