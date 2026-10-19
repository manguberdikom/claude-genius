# konkurentlik

Minimal shakl (architect 11.7):

```java
@Component
class HitCounter {
  private final ConcurrentHashMap<String, LongAdder> hits = new ConcurrentHashMap<>();

  void hit(String key) {
    hits.computeIfAbsent(key, k -> new LongAdder()).increment();
  }

  long count(String key) {
    LongAdder adder = hits.get(key);
    return adder == null ? 0 : adder.sum();
  }
}
```

Allaqachon bor, yozmang:
- `synchronized` hisoblagich o'rniga `AtomicLong`, ko'p yozuvchida `LongAdder`, holatni almashtirishga `AtomicReference.compareAndSet` va immutable record (architect 11.5)
- `containsKey` keyin `put` (check-then-act) o'rniga `ConcurrentHashMap.computeIfAbsent` (architect 11.16)
- `new Thread` yoki `Executors.newFixedThreadPool` o'rniga `@Async` va `spring.task.execution.pool.*` (chekli `queue-capacity`) (architect 11.8)
- `Timer` o'rniga `@Scheduled(fixedDelayString = ...)` (architect 11.8)

Tuzoqlar:
- `volatile` maydonda `count++` atomar emas, faqat ko'rinuvchanlik beradi; hisoblagich uchun atomic sinf oling (architect 11.6)
- `computeIfAbsent` funksiyasida IO yoki shu map ga yozish boshqa yozuvchilarni to'sadi yoki `IllegalStateException` beradi, funksiya qisqa va yon ta'sirsiz bo'lsin (architect 11.7)
- read qulfini ushlab turib write qulfini so'rash thread ni o'zini qotiradi, read ni bo'shatib write ostida shartni qayta tekshiring (architect 11.4)
