# satr va regex

Minimal shakl (clean-code 21.6, 21.2):

```java
private static final Pattern IBAN_FORMAT =
        Pattern.compile("^[A-Z]{2}\\d{2}[A-Z0-9]{1,30}$");

boolean isValidIban(String iban) {
    return IBAN_FORMAT.matcher(iban).matches();
}

String toCsv(List<Sku> skus) {
    return skus.stream().map(Sku::code).collect(Collectors.joining(","));
}
```

Allaqachon bor, yozmang:
- siklda `+` yoki ajratgichni qo'lda qo'yish o'rniga `Collectors.joining` / `String.join` (clean-code 21.2)
- `toLowerCase().equals(...)` o'rniga `equalsIgnoreCase` (clean-code 21.4)
- `trim().isEmpty()` o'rniga `isBlank()` va `strip()` (clean-code 21.5)

Tuzoqlar:
- `split` regex oladi: `split(".")` bo'sh massiv beradi, `split("\\.")` yoki `Pattern.quote(".")`, CSV da bo'sh ustun yo'qolmasligi uchun `split(",", -1)` (clean-code 21.5)
- regexda `"\s"` bo'shliq escape (Java 15+), whitespace sinfi `"\\s"`; `matches` butun satr, qisman moslik `find()` (clean-code 21.6, 21.5)
- `String.format` va `toLowerCase` ni locale siz chaqirmang: mashina uchun `Locale.ROOT`, foydalanuvchi uchun uning locale i (clean-code 21.4)
- tashqi kiritishga `(\\w+\\s?)*` kabi ichma-ich kvantifikator ReDoS beradi: chegaralangan sinf yozing va uzunlikni regexdan oldin cheklang (clean-code 21.7)
