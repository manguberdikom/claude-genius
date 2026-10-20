# asinxron

Minimal shakl (patterns 4.26, code-review 15.8):

```java
@Configuration
@EnableAsync
class AsyncConfig {}

@Service
class ReceiptSender {
    private final Mailer mailer;
    ReceiptSender(Mailer mailer) { this.mailer = mailer; }

    @Async
    public CompletableFuture<Void> send(OrderId id) {
        mailer.send(id);
        return CompletableFuture.completedFuture(null);
    }
}
```

Allaqachon bor, yozmang:
- `new Thread` yoki qo'lda `ExecutorService` o'rniga `@EnableAsync` + `@Async` va Boot bergan `applicationTaskExecutor` (patterns 4.26)
- Qo'lda pool bean o'rniga `spring.task.execution.pool.core-size`, `max-size`, `queue-capacity` (patterns 25.49)
- MDC va trace ni qo'lda ko'chirish o'rniga `@Bean TaskDecorator` = `new ContextPropagatingTaskDecorator()`, SecurityContext uchun `DelegatingSecurityContextAsyncTaskExecutor` (code-review 39.5, patterns 25.49)
- Java 21+ da pool sozlash o'rniga `spring.threads.virtual.enabled=true`, `@Async` ham virtual thread oladi (architect 12.5)

Tuzoqlar:
- O'sha bean ichidan chaqiruv yoki `private` metod proxy ni chetlab o'tadi va ish sinxron bo'ladi: async metodni alohida bean ga chiqaring (patterns 4.26)
- `void` metoddagi xato chaqiruvchiga yetmaydi, faqat log da qoladi: `CompletableFuture` qaytaring yoki `AsyncUncaughtExceptionHandler` ni metrikaga ulang (patterns 25.49, code-review 15.8)
- Executorsiz `supplyAsync` umumiy `commonPool` ga tushadi, Boot pool navbati esa cheksiz: aniq `Executor` bering va `queue-capacity` qo'ying (architect 11.9, patterns 25.49)
- `@Transactional` ichidan `@Async`: tranzaksiya ko'chmaydi, ish commit dan oldin boshlanib yangi qatorni ko'rmaydi; entity emas id uzating, chaqiruv `@TransactionalEventListener(phase = AFTER_COMMIT)` dan (code-review 15.8, architect 11.8, 19.8)
