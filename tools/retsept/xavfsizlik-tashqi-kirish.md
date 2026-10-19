# xavfsizlik: tashqi kirish

Minimal shakl (code-review 31.1, 31.3):

```java
private static final Path BASE = Path.of("/var/data").toAbsolutePath().normalize();

Path safePath(String name) {
    Path target = BASE.resolve(name).normalize();
    if (!target.startsWith(BASE)) throw new InvalidPath(name);
    return target;
}

URI safeUri(String raw) {
    URI uri = URI.create(raw);
    if (!"https".equalsIgnoreCase(uri.getScheme()) || !allowedHosts.contains(uri.getHost()))
        throw new UnsafeUrl(raw);
    return uri;
}
```

Allaqachon bor, yozmang:
- `readObject` yoki `@class` li JSON o'rniga `@JsonTypeInfo(use = NAME)` + `@JsonSubTypes` va `sealed` interfeys (code-review 31.2)
- meros `ObjectInputStream` uchun qo'lda `resolveClass` o'rniga `ObjectInputFilter.Config.createFilter("com.acme.dto.*;maxdepth=20;!*")` (code-review 31.2)
- YAML da `new Yaml()` o'rniga `new Yaml(new SafeConstructor(new LoaderOptions()))` (code-review 31.2)
- redirect tekshiruvi o'rniga `HttpClient.Redirect.NEVER` (code-review 31.1)

Tuzoqlar:
- IP ni tekshirib host nomi bilan ulanish DNS rebinding ga ochiq: ulanishni tekshirilgan IP ga bog'lang (code-review 31.1)
- XML parser standart holatda XXE ga ochiq: har factory da `disallow-doctype-decl` ni yoqing (code-review 31.2)
- zip ichidagi nom `../` bo'lishi va hajm yolg'on bo'lishi mumkin: har entry ni `normalize`/`startsWith` bilan tekshiring, o'qilgan baytni cheklang (code-review 31.3)
