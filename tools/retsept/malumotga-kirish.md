# ma'lumotga kirish

Minimal shakl (patterns 9.2, architect 18.5, code-review 24.6):

```java
public record OrderRow(Long id, String number, BigDecimal total) {}

public interface OrderRepository extends JpaRepository<Order, Long> {

    List<Order> findByStatusAndCreatedAtAfter(OrderStatus status, Instant since);

    @Query("""
           select new com.acme.order.OrderRow(o.id, o.number, o.total)
           from Order o where o.status = :status
           """)
    Slice<OrderRow> rows(OrderStatus status, Pageable page);
}
```

Allaqachon bor, yozmang:
- `EntityManager` bilan qo'lda CRUD DAO o'rniga `JpaRepository` interfeysi, proxy ni Spring Data yasaydi (patterns 9.2)
- Har filtr kombinatsiyasiga metod yoki satr ulab SQL o'rniga `Specification` va `JpaSpecificationExecutor` (architect 18.10, code-review 24.5)
- Window, CTE, `on conflict` ni JPQL ga sig'dirish o'rniga `JdbcClient.sql(..).param(..).query(Rec.class).list()` (architect 18.11)
- Literali farqli `findActive()`/`findCancelled()` o'rniga bitta `findByStatus(s)` yoki `findByStatusIn(Collection)` (clean-code 37.8, 28.5)

Tuzoqlar:
- Sikl yoki DTO mapping ichida lazy bog'lanishga tegish N+1 beradi; `join fetch`, `@EntityGraph` yoki projection bilan bitta so'rov qiling (code-review 23.1)
- To'plamni `join fetch` qilib `Pageable` berish sahifani xotirada kesadi; avval id lar sahifasi, keyin ular bo'yicha fetch (architect 18.4)
- Katta jadvalda `Page` har so'rovda `count(*)` yuboradi; faqat "keyingisi bormi" kerak bo'lsa `Slice` qaytaring (code-review 24.6)
- Sortsiz `Pageable` da qator sahifalar orasida takrorlanadi, yo'qoladi; `@PageableDefault(sort = ..)` yoki `Sort.by(..)`, oxirida `id` (code-review 20.5, clean-code 27.5)
- Derived query uch shartdan oshsa `@Query` yoki Specification (clean-code 28.5)
