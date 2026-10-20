# keshlash

Minimal shakl (patterns 11.10):

```java
@Configuration @EnableCaching class CacheConfig {}

@Service
class ProductService {
  private final ProductRepository repo;
  ProductService(ProductRepository repo) { this.repo = repo; }

  @Cacheable(cacheNames = "products", key = "#id", sync = true)
  public ProductView find(long id) { return ProductView.from(repo.findById(id).orElseThrow()); }

  @CacheEvict(cacheNames = "products", key = "#p.id")
  public void save(Product p) { repo.save(p); }
}
```

Allaqachon bor, yozmang:
- qo'lda Map get/put o'rniga `@Cacheable`, `@CachePut`, `@CacheEvict` (patterns 11.10)
- qo'lda lock bilan bitta yuklash o'rniga `@Cacheable(sync = true)`, `unless` bilan birga emas (patterns 11.10)
- qo'lda muddat hisobi o'rniga `spring.cache.caffeine.spec=maximumSize=..,expireAfterWrite=..` yoki `RedisCacheConfiguration.entryTtl` (patterns 11.12)
- har chaqiruvda try/catch o'rniga `CachingConfigurer.errorHandler()` qaytargan `CacheErrorHandler` (architect 28.12)

Tuzoqlar:
- `@EnableCaching` (Boot da ham) bo'lmasa proxy yo'q va `@Cacheable` jim ishlamaydi (patterns 11.10)
- bean ichida `this.find()` proxy dan o'tmaydi va kesh jim chetlanadi, keshli metodni alohida bean ga chiqaring (architect 28.4)
- yangilashda `@CachePut` emas `@CacheEvict`: parallel thread lar `@CachePut` bilan eski qiymatni yozib qo'yadi (patterns 11.22); `@Transactional` ichida evict commit dan oldin ishlaydi va rollback da nomuvofiqlik qotadi, tozalashni `@TransactionalEventListener(phase = AFTER_COMMIT)` da qiling (architect 28.8)
- default kalit argumentning `equals`/`hashCode` iga tayanadi, entity yoki DTO o'rniga `key = "#id"` kabi aniq kalit bering va tenant kabi scope ni qo'shing (patterns 11.15); qiymat entity emas, record DTO (architect 28.11)
