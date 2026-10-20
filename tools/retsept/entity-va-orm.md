# entity va ORM

Minimal shakl (clean-code 28.4, 28.2, 28.1):

```java
@Entity
public class OrderLine {
    @Id @GeneratedValue(strategy = GenerationType.SEQUENCE)
    private Long id;
    @ManyToOne(fetch = FetchType.LAZY, optional = false)
    private Order order;
    @Column(nullable = false)
    private int quantity;

    protected OrderLine() {}
    public Long getId() { return id; }

    @Override public boolean equals(Object o) {
        return this == o || o instanceof OrderLine other && id != null && id.equals(other.getId());
    }
    @Override public int hashCode() { return OrderLine.class.hashCode(); }
}
```

Allaqachon bor, yozmang:
- Bog'lanishni mappingda EAGER qilish o'rniga repository metodida `@EntityGraph(attributePaths = ...)` (sonarqube 29.7)
- Entity olib qo'lda DTO ga ko'chirish o'rniga Spring Data interfeys projection yoki `select new` record (code-review 23.7)
- Versiyani qo'lda solishtirish o'rniga `@Version` (architect 18.8)
- Bola qatorlarni qo'lda saqlash va o'chirish o'rniga agregat ichida `cascade = ALL, orphanRemoval = true` (clean-code 28.4)

Tuzoqlar:
- `@ManyToOne` standartda EAGER: har doim `LAZY`, kerakda `join fetch`; Lombok `@Data`/`@ToString` grafni yuklaydi, ishlatmang (clean-code 28.4, 28.2)
- Mustaqil entitetlar orasida `cascade = ALL` ota o'chganda butun tarixni o'chiradi; uni faqat agregat qismlariga qo'ying (code-review 23.4)
- Enum ustun `@Enumerated(EnumType.STRING)`: standart ORDINAL da yangi qiymat eski qatorlar ma'nosini buzadi (code-review 14.8)
- `SEQUENCE` migratsiyasida `INCREMENT BY` = `allocationSize` (standart 50) (architect 18.7)
- Vaqt maydoni initsializatorida `Instant.now()` testlanmaydi: vaqt servisdagi `Clock` dan konstruktorga beriladi (clean-code 22.3)
