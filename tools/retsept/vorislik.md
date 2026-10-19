# vorislik

Minimal shakl (clean-code 17.4, patterns 3.10):

```java
public abstract class AbstractImporter<T> {

    public final void importFile(Path file) {
        for (T row : parse(file)) {
            if (isValid(row)) {
                save(row);
            }
        }
    }

    protected abstract List<T> parse(Path file);
    protected abstract boolean isValid(T row);
    protected abstract void save(T row);
}
```

Allaqachon bor, yozmang:
- Resursni ochib yopadigan o'z abstrakt shabloni o'rniga `JdbcTemplate`, `TransactionTemplate` callback (patterns 3.10)
- O'z bazaviy filtri o'rniga `OncePerRequestFilter.doFilterInternal` (patterns 3.10)
- To'plamning hamma metodini yozish o'rniga `AbstractList` yoki `AbstractMap` skeleti (clean-code 17.7)
- `kind` maydonli teglangan sinf o'rniga `sealed interface` va `record` (clean-code 17.10)

Tuzoqlar:
- Bazaviy konstruktor override qilinadigan metodni chaqirsa voris maydonlari hali `null` yoki 0; sozlashni konstruktor parametriga yoki `private`/`static` metodga oling (clean-code 17.2)
- `HashMap` yoki `HashSet` dan voris olish self-use tufayli invariantni buzadi va butun API ni ochadi; maydonga delegatsiya qiling (clean-code 17.9)
- `protected` maydon va "super ni chaqiring" shartnomasi bazaviy invariantni ochiq qoldiradi; maydon `private`, tartib `final` shablon metodda, vorislikka mo'ljallanmagan sinf `final` (clean-code 17.3, 17.4, 17.1)
