# xato bilan ishlash

Minimal shakl (clean-code 19.1, clean-code 19.7, sonarqube 11.9):

```java
Settlement load(Path file) {
    Settlement result;
    try (var reader = Files.newBufferedReader(file, UTF_8)) {
        result = parse(reader);
    } catch (IOException e) {
        throw new ImportException("import fayli o'qilmadi: " + file, e);
    }
    return result;
}

@ExceptionHandler(ImportException.class)
ProblemDetail handle(ImportException e) {
    log.error("import muvaffaqiyatsiz", e);
    return ProblemDetail.forStatusAndDetail(UNPROCESSABLE_ENTITY, "Import fayli o'qilmadi");
}
```

Allaqachon bor, yozmang:
- O'z `InvalidXxxException` sinfi o'rniga `IllegalArgumentException` yoki `IllegalStateException`, kontekst xabarda (clean-code 18.11)
- Qo'lda `finally { close(); }` o'rniga `try-with-resources` (clean-code 19.4)
- Qo'lda `if (x == null) throw` o'rniga `Objects.requireNonNull(x, "x")` (clean-code 19.9)
- O'z xato JSON formati o'rniga `@RestControllerAdvice` va `ProblemDetail` (clean-code 27.3)

Tuzoqlar:
- `throw new X(e.getMessage())` asl stack trace ni yo'qotadi; `e` ni har doim cause qilib uzating (clean-code 19.1)
- `catch` ichida ham log, ham throw bitta xatoni log da bir necha marta chiqaradi; log faqat xatoni qayta ishlagan chegarada (clean-code 19.7)
- `InterruptedException` ni yutish uzilish belgisini o'chiradi va shutdown ishlamaydi; `Thread.currentThread().interrupt()` bilan tiklang (clean-code 19.5)
