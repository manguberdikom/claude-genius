# xavfsizlik: SQL

Minimal shakl (code-review 29.1, 29.3):

```java
enum OrderSort {
    CREATED("created_at"), TOTAL("total");
    final String column;
    OrderSort(String column) { this.column = column; }
}

List<OrderRow> find(UUID customerId, OrderSort sort) {
    return jdbcClient.sql("""
            SELECT id, number, total FROM orders
            WHERE customer_id = :customerId ORDER BY %s""".formatted(sort.column))
        .param("customerId", customerId)
        .query(OrderRow.class)
        .list();
}
```

Allaqachon bor, yozmang:
- Qo'lda escape yoki satr yig'ish o'rniga `JdbcClient.param(...)` yoki `JdbcTemplate` dagi `?` bind parametr (code-review 29.3)
- `IN (...)` ni satrdan yig'ish o'rniga `in :ids` ga `Collection` yoki PostgreSQL da `= ANY(:ids)` (code-review 29.2)
- Sort maydonini qo'lda tekshirish o'rniga Spring Data `Sort.by(...)`, u nomni entity maydonlari bilan solishtiradi (code-review 29.2)

Tuzoqlar:
- Native `@Query` da qo'shtirnoq ichidagi `'?1'` parametr emas, satr literali; qo'shtirnoqsiz `?1` yoki `:name` yozing (code-review 29.2)
- SpEL `:#{...}` va `JpaSort.unsafe` qiymatni SQL matniga qo'shadi; oddiy `:name` va tekshiriladigan `Sort` ishlating (code-review 29.2)
- Qiymatni `String.format` bilan qo'yish Sonar ni jim qiladi, injection qoladi; qiymat faqat bind parametr, ustun va yo'nalish faqat enum yoki oq ro'yxat (sonarqube 26.16, 26.2)
