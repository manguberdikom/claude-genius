<!-- doc: patterns | chapter: 11 | part:  -->

[Barcha hujjatlar](../../README.md) / [Dizayn patternlar](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 11. Keshlash patternlari (Caching Patterns)

<details>
<summary>Bu bobdagi 23 bo'lim</summary>

- [11.1 Kesh-yonida (Cache-Aside)](#111-kesh-yonida-cache-aside)
- [11.2 O'qish-orqali (Read-Through)](#112-oqish-orqali-read-through)
- [11.3 Yozish-orqali (Write-Through)](#113-yozish-orqali-write-through)
- [11.4 Yozish-ortda (Write-Behind)](#114-yozish-ortda-write-behind)
- [11.5 Yozish-atrofida (Write-Around)](#115-yozish-atrofida-write-around)
- [11.6 Oldindan-yangilash (Refresh-Ahead)](#116-oldindan-yangilash-refresh-ahead)
- [11.7 Yaqin kesh / Ko'p qatlamli kesh (Near Cache / Multi-level L1-L2 Cache)](#117-yaqin-kesh--kop-qatlamli-kesh-near-cache--multi-level-l1-l2-cache)
- [11.8 Taqsimlangan kesh (Distributed Cache - Redis, Hazelcast)](#118-taqsimlangan-kesh-distributed-cache---redis-hazelcast)
- [11.9 Hibernate ikkinchi darajali kesh va query kesh (Hibernate Second-Level Cache & Query Cache)](#119-hibernate-ikkinchi-darajali-kesh-va-query-kesh-hibernate-second-level-cache--query-cache)
- [11.10 Spring Cache abstraksiyasi (Spring Cache Abstraction)](#1110-spring-cache-abstraksiyasi-spring-cache-abstraction)
- [11.11 Kesh bosqini himoyasi (Cache Stampede / Thundering Herd Protection)](#1111-kesh-bosqini-himoyasi-cache-stampede--thundering-herd-protection)
- [11.12 TTL / TTI muddati tugashi (TTL / TTI Expiration)](#1112-ttl--tti-muddati-tugashi-ttl--tti-expiration)
- [11.13 Chiqarib tashlash siyosatlari (Eviction Policies: LRU, LFU, W-TinyLFU / Caffeine)](#1113-chiqarib-tashlash-siyosatlari-eviction-policies-lru-lfu-w-tinylfu--caffeine)
- [11.14 Kesh invalidation strategiyalari (Cache Invalidation Strategies: Event-based, Versioned Keys)](#1114-kesh-invalidation-strategiyalari-cache-invalidation-strategies-event-based-versioned-keys)
- [11.15 Kesh kalitini loyihalash (Cache Key Design)](#1115-kesh-kalitini-loyihalash-cache-key-design)
- [11.16 HTTP keshlash (HTTP Caching: Cache-Control, ETag, CDN)](#1116-http-keshlash-http-caching-cache-control-etag-cdn)
- [11.17 Memoizatsiya (Memoization)](#1117-memoizatsiya-memoization)
- [11.18 Salbiy keshlash (Negative Caching)](#1118-salbiy-keshlash-negative-caching)
- [11.19 Keshni oldindan to'ldirish (Cache Warming)](#1119-keshni-oldindan-toldirish-cache-warming)
- [11.20 Hot key ta'sirini yumshatish (Hot Key Mitigation)](#1120-hot-key-tasirini-yumshatish-hot-key-mitigation)
- [11.21 So'rov doirasidagi kesh (Request-Scoped Cache)](#1121-sorov-doirasidagi-kesh-request-scoped-cache)
- [11.22 Kesh konsistensiyasi murosalari (Cache Consistency Trade-offs)](#1122-kesh-konsistensiyasi-murosalari-cache-consistency-trade-offs)
- [11.23 Amalda qo'llash](#1123-amalda-qollash)

</details>



Keshlash patternlari - bu ma'lumotni asl manbadan (relational database, tashqi REST API, hisob-kitob qiluvchi servis) qayta-qayta olib kelmaslik uchun uni tezroq va yaqinroq joyda vaqtincha saqlash usullari majmuasi. Arxitektor uchun keshlash ikki tomonlama qurol: to'g'ri qo'llanganda latency'ni o'n barobar kamaytiradi va database'dagi yukni keskin pasaytiradi, xato qo'llanganda esa eskirgan (stale) ma'lumot, xotira sizib ketishi (memory leak) va diagnostika qilish qiyin bo'lgan consistency bug'larni keltiradi. Shu sababli har bir pattern "kim keshga yozadi", "kim keshdan o'qiydi" va "eskirgan ma'lumot qancha vaqt yashashi mumkin" degan savollarga aniq javob beradi. Quyidagi entry'lar read/write strategiyalari, ko'p qatlamli (multi-level) topologiyalar va Spring ekotizimidagi aniq amalga oshirish vositalarini qamrab oladi.

## 11.1 Kesh-yonida (Cache-Aside)

**Tavsif:** Eng keng tarqalgan keshlash strategiyasi, uni "lazy loading" deb ham ataydilar. Application kodi birinchi navbatda keshdan so'raydi; agar topilmasa (cache miss) - asl manbadan o'qiydi, keshga yozadi va qaytaradi. Kesh bu yerda application'ga bo'ysunuvchi yordamchi, uni boshqarish mas'uliyati to'liq chaqiruvchi kodda bo'ladi.

**Spring'da qayerda uchraydi:** `RedisTemplate` yoki `StringRedisTemplate` (`spring-boot-starter-data-redis`) bilan qo'lda yoziladi: `opsForValue().get(key)` → miss bo'lsa repository, keyin `opsForValue().set(key, value, Duration.ofMinutes(10))`. Caffeine'ning `Cache#getIfPresent` + `put` juftligi ham aynan shu pattern. Spring Cache abstraction'ning `@Cacheable` annotatsiyasi ham texnik jihatdan cache-aside'ni proxy orqali avtomatlashtiradi, lekin manual variant TTL, serialization va fallback'ni to'liq nazorat qilish kerak bo'lganda afzal.

**Qo'llanish keyslari:**
- Foydalanuvchi profil ma'lumotlarini (ism, avatar, til sozlamalari) har request'da database'dan olmaslik uchun keshlash.
- Kurs valyutalari yoki soliq stavkalari kabi kam o'zgaruvchi reference data'ni keshlash.
- Tashqi to'lov provayderidan olingan kartalar ro'yxatini bir necha daqiqaga keshlab, rate limit'ga tushmaslik.
- Og'ir `GROUP BY` hisobotining natijasini keshlab, dashboard'ni bir necha millisekundda ko'rsatish.
- Feature flag konfiguratsiyasini keshlab, har evaluation'da config servisga bormaslik.

**Ehtiyot bo'ling:** Kesh va database o'rtasidagi consistency butunlay sizning mas'uliyatingizda - yozish yo'lida evict qilishni eslab qolmasangiz, stale ma'lumot cheksiz yashaydi. Yana bir tuzoq: bir vaqtda ko'p thread miss bo'lgan kalitni yuklay boshlaydi (stampede), shu sababli TTL bilan birga sync/lock mexanizmini ham o'ylab ko'ring.

```java
// Cache-aside: ilova keshni o'zi boshqaradi
public Rate rate(String pair) {
    Rate cached = redis.opsForValue().get(key(pair));
    if (cached != null) return cached;

    Rate fresh = cbuClient.fetch(pair);          // kesh bo'sh: manbadan
    redis.opsForValue().set(key(pair), fresh, Duration.ofMinutes(10));
    return fresh;
}
// Eng ko'p ishlatiladigan strategiya. Ikki xavf: stampede (bir vaqtda
// ko'p so'rov manbaga ketadi) va invalidatsiya unutilishi.
```

## 11.2 O'qish-orqali (Read-Through)

**Tavsif:** Application faqat kesh bilan gaplashadi, kesh esa miss bo'lganda asl manbadan ma'lumotni o'zi yuklab oladi. Yuklash logikasi loader (ya'ni kesh provayderiga berilgan funksiya) ichiga ko'chiriladi, shuning uchun chaqiruvchi kod "bor-yo'qligini tekshirish" kodidan xoli bo'ladi. Natijada cache-aside bilan bir xil effekt, lekin mas'uliyat kesh qatlamiga o'tadi.

**Spring'da qayerda uchraydi:** Caffeine'ning `LoadingCache<K, V>` (`Caffeine.newBuilder().build(key -> repository.findById(key))`) va uning `get(key)` metodi klassik read-through. JCache (JSR-107) standartida `CacheLoader` interfeysi va `CompleteConfiguration#setReadThrough(true)` mavjud, Spring buni `JCacheCacheManager` orqali qo'llab-quvvatlaydi. Hazelcast'da `MapLoader`/`MapStore` interfeysi `IMap` uchun read-through ta'minlaydi. Spring'ning `@Cacheable` bilan `CaffeineCacheManager` juftligi ham loader'siz ishlaydi, chunki method'ning o'zi loader rolini bajaradi.

**Qo'llanish keyslari:**
- Mahsulot katalogini `LoadingCache` orqali keshlab, controller kodida miss tekshiruvi bo'lmasligi.
- Hazelcast `MapStore` bilan entity'larni kesh ichida database'ga shaffof bog'lash.
- JWT public kalitlarini JWKS endpoint'dan avtomatik yuklab, kesh orqali berish.
- Geo-IP yoki pochta indeks lookup jadvalini birinchi murojaatda lazy yuklash.
- Konfiguratsiya daraxtini (tenant sozlamalari) loader bilan tenant kaliti bo'yicha yuklash.

**Ehtiyot bo'ling:** Loader ichidagi exception kesh provayderining semantikasiga qarab turlicha ishlanadi - Caffeine `null` qaytarsa kalit umuman keshlanmaydi, bu esa har request'da database'ga urilishga olib keladi. Loader ichida uzun bloklanuvchi I/O qilsangiz, kesh'ni ishlatuvchi barcha thread'lar shu yerda navbatga tizilib qolishi mumkin.

```java
// Read-through: keshni abstraksiya boshqaradi, ilova bilmaydi
@Service
public class RateService {

    @Cacheable(cacheNames = "rates", key = "#pair")
    public Rate rate(String pair) {
        return cbuClient.fetch(pair);    // faqat kesh bo'sh bo'lsa chaqiriladi
    }
}
// Afzalligi: chaqiruvchi kodda kesh mantig'i yo'q.
// Narxi: kesh qachon o'qilganini ko'rish qiyinroq, proxy chetlab o'tilsa
// (self-invocation) kesh jimgina ishlamaydi.
```

## 11.3 Yozish-orqali (Write-Through)

**Tavsif:** Yozish operatsiyasi keshga va asl manbaga bir xil, sinxron tranzaksiyada boradi: kesh yangilanadi, so'ng (yoki bir vaqtda) database'ga yoziladi va faqat ikkisi muvaffaqiyatli bo'lgandan keyin chaqiruvchiga javob qaytadi. Bu kesh bilan database o'rtasidagi nomuvofiqlik oynasini (inconsistency window) minimumga tushiradi. Narxi - har bir yozishning latency'si oshadi.

**Spring'da qayerda uchraydi:** Spring Cache abstraction'da `@CachePut` aynan shu uchun: method database'ga yozadi, annotatsiya qaytgan natijani keshga majburan joylaydi (`@CachePut(value = "users", key = "#user.id")`). Hazelcast'da `MapStore#store` write-through rejimida (`write-delay-seconds = 0`) sinxron ishlaydi. JCache'da `CacheWriter` + `setWriteThrough(true)`. Tranzaksiya bilan birga ishlatilganda `TransactionAwareCacheManagerProxy` kesh operatsiyasini commit'dan keyingi fazaga surib, rollback holatida keshni buzmaslikka yordam beradi.

**Qo'llanish keyslari:**
- Foydalanuvchi profilini tahrirlashda `@CachePut` bilan keshni darhol yangi qiymat bilan yangilash.
- Narx yoki chegirma qoidalarini admin panelidan o'zgartirganda barcha node'lar darhol yangi narxni ko'rishi.
- Session yoki shopping cart holatini Redis'ga sinxron yozib, keyingi request boshqa instance'ga tushsa ham to'g'ri ko'rinishi.
- Hazelcast `IMap` ustida ishlaydigan inventar hisoblagichini database bilan sinxron saqlash.
- Audit konfiguratsiyasi kabi stale bo'lishi mutlaqo mumkin bo'lmagan sozlamalarni yangilash.

**Ehtiyot bo'ling:** `@CachePut` va `@Cacheable`ni bitta method'ga birga qo'yish mantiqiy xato - `@Cacheable` chaqiruvni butunlay o'tkazib yuborishi mumkin, `@CachePut` esa har safar bajarilishini talab qiladi. Shuningdek yozish yo'li kesh cluster'iga bog'lanib qoladi: Redis tushsa, business yozuv ham fail bo'lishi mumkin, shuning uchun degradation strategiyasini oldindan belgilang.

```java
// Write-through: yozuv bir vaqtda keshga va manbaga ketadi
@Service
public class ProfileService {

    @Transactional
    @CachePut(cacheNames = "profiles", key = "#profile.id")
    public Profile save(Profile profile) {
        return repo.save(profile);       // natija keshga yoziladi
    }
}
// Kesh har doim yangi, lekin yozuv sekinlashadi.
// Tranzaksiya rollback bo'lsa kesh eskirgan qiymat bilan qoladi:
// shuning uchun keshni commit'dan keyin yangilash xavfsizroq.
```

## 11.4 Yozish-ortda (Write-Behind)

**Tavsif:** Yozish avval faqat keshga tushadi va chaqiruvchiga darhol javob qaytadi; asl manbaga yozish esa asinxron, ko'pincha batch holida va kechiktirilgan tarzda bajariladi. Bu yozish latency'sini keskin kamaytiradi va database'dagi write IOPS'ni batching hisobiga pasaytiradi. Buning evaziga ma'lumot yo'qolish riski paydo bo'ladi: kesh node'i flush'gacha o'lsa, yozuvlar yo'qoladi.

**Spring'da qayerda uchraydi:** Hazelcast `MapStore` + `write-delay-seconds > 0` va `write-batch-size` - bu klassik write-behind. Redis holatida odatda qo'lda quriladi: `RedisTemplate` bilan keshga yozib, `ApplicationEventPublisher` yoki `@Async` / `TaskExecutor` orqali database'ga keyinroq yozish, yoki Redis Streams'ga event qo'yib, alohida consumer bilan persist qilish. Spring Boot'da `@Scheduled` bilan vaqti-vaqti bilan flush qiluvchi buffer ham shu patternning sodda shakli; Java 21+ virtual thread'lar bunday flush worker'larni arzon qiladi.

**Qo'llanish keyslari:**
- Sahifa ko'rishlari yoki "like" hisoblagichlarini keshda to'plab, har 10 sekundda database'ga bitta batch update qilish.
- IoT sensor telemetriyasini keshga yozib, keyin batch holida time-series storage'ga yuklash.
- Oxirgi aktivlik vaqti (`lastSeenAt`) kabi muhim bo'lmagan maydonni har request'da yozmaslik.
- O'yin yoki reyting (leaderboard) ballarini Redis'da ushlab, davriy ravishda persist qilish.
- Log/metrik agregatsiyasini xotirada yig'ib, keyin bitta tranzaksiyada yozish.

**Ehtiyot bo'ling:** Pul, buyurtma, to'lov kabi durability talab qiladigan ma'lumot uchun hech qachon ishlatmang - flush'gacha bo'lgan oynada yo'qolgan yozuvni tiklash imkoni bo'lmaydi. Yana bir muammo: database'dagi constraint violation asinxron yuzaga keladi, ya'ni foydalanuvchi allaqachon "muvaffaqiyatli" javobni olgan bo'ladi, shuning uchun kompensatsiya mexanizmi kerak.

```java
// Write-behind: keshga yozildi, manbaga keyinroq (batch bilan)
@Component
public class ViewCounterBuffer {
    private final Map<Long, LongAdder> buffer = new ConcurrentHashMap<>();

    public void increment(long articleId) {
        buffer.computeIfAbsent(articleId, k -> new LongAdder()).increment();
    }

    @Scheduled(fixedDelay = 5_000)
    void flush() {
        buffer.forEach((id, adder) -> repo.addViews(id, adder.sumThenReset()));
    }
}
// Yozuv tez, lekin ilova yiqilsa buffer yo'qoladi. Faqat yo'qotish
// qabul qilinadigan ma'lumot uchun (ko'rish soni, metrika).
```

## 11.5 Yozish-atrofida (Write-Around)

**Tavsif:** Yozish operatsiyasi keshni butunlay chetlab o'tib, to'g'ridan-to'g'ri database'ga boradi; kesh esa yoki invalidatsiya qilinadi, yoki umuman tegilmaydi va kalit faqat keyingi o'qishda (read-through/cache-aside orqali) to'ldiriladi. Bu strategiya "yozilgan ma'lumot tez orada o'qilmaydi" degan taxminga asoslanadi va keshni hech kim so'ramaydigan qiymatlar bilan to'ldirib yuborishdan (cache pollution) saqlaydi.

**Spring'da qayerda uchraydi:** Spring Cache abstraction'da bu `@CacheEvict(value = "orders", key = "#order.id")` yozish method'i ustida - qiymat keshga qo'yilmaydi, faqat eski nusxa o'chiriladi. To'liq tozalash uchun `@CacheEvict(allEntries = true)`, tranzaksiya commit'idan keyin ishlashi uchun `beforeInvocation = false` (default) va `TransactionAwareCacheManagerProxy`. Hibernate darajasida `@Cache(usage = CacheConcurrencyStrategy.READ_WRITE)` bo'lmagan, keshlanmagan entity'lar ham amalda write-around tarzida xizmat qiladi.

**Qo'llanish keyslari:**
- Bulk import yoki migratsiyada millionlab satrni yozish - keshga umuman tegmaslik.
- Bir marta yozilib, keyin faqat hisobotda o'qiladigan audit log yozuvlari.
- Yangi buyurtma yaratilganda uning keshini to'ldirmaslik, chunki darhol qayta o'qilmaydi.
- Fayl metadata'sini yozishda, o'qishlar faqat ro'yxat endpoint'i orqali bo'lganda.
- Batch job natijalarini yozib, keshni faqat `allEntries = true` bilan tozalash.

**Ehtiyot bo'ling:** Yozishdan so'ng darhol o'qish bo'ladigan oqimda (read-your-own-writes) bu pattern foydalanuvchiga eski ma'lumot ko'rsatadi yoki kafolatlangan cache miss keltiradi. `@CacheEvict`ni `beforeInvocation = true` bilan ishlatish rollback holatida keshni allaqachon bo'shatib qo'yadi - bu ko'pincha xavfsizroq, lekin miss to'lqinini keltiradi.

```java
// Write-around: yozuv faqat manbaga, kesh invalidatsiya qilinadi
@Service
public class CatalogService {

    @Transactional
    @CacheEvict(cacheNames = "products", key = "#product.id")
    public Product update(Product product) {
        return repo.save(product);       // keshga yozilmaydi, o'chiriladi
    }
}
// Bir marta yozilib kamdan-kam o'qiladigan ma'lumot uchun to'g'ri:
// kesh keraksiz qiymat bilan to'lmaydi. Keyingi o'qish kesh bo'sh bo'ladi.
```

## 11.6 Oldindan-yangilash (Refresh-Ahead)

**Tavsif:** Kesh yozuvi muddati tugashini kutmasdan, TTL'ning oxiriga yaqinlashganda fonda proaktiv yangilanadi. Agar yozuvga murojaat bo'lsa, chaqiruvchi eski (lekin hali yaroqli) qiymatni darhol oladi, yangilash esa asinxron ravishda alohida thread'da ketadi. Shu tariqa foydalanuvchi hech qachon "sovuq" miss latency'siga duch kelmaydi.

**Spring'da qayerda uchraydi:** Caffeine'ning `refreshAfterWrite(Duration)` + `LoadingCache` juftligi aynan shu pattern (`expireAfterWrite`dan farqli - eski qiymat qaytariladi, yangilash fonda). Spring Boot'da `spring.cache.caffeine.spec=maximumSize=1000,refreshAfterWrite=5m` bilan sozlanadi, lekin `CacheLoader` bean'i kerak. Alternativ: `@Scheduled(fixedDelay = ...)` method ichida `@CachePut` chaqirib keshni oldindan to'ldirish, yoki Caffeine'ga `Executor` berib (`Caffeine.newBuilder().executor(taskExecutor)`) refresh'ni boshqarish.

```java
LoadingCache<String, Rate> rates = Caffeine.newBuilder()
    .refreshAfterWrite(Duration.ofMinutes(5))
    .expireAfterWrite(Duration.ofHours(1))
    .build(code -> rateClient.fetch(code));
```

**Qo'llanish keyslari:**
- Valyuta kurslarini har 5 daqiqada fonda yangilab, API'ning sekin javobini foydalanuvchiga ko'rsatmaslik.
- Sekin tashqi SOAP/REST servisdan olingan ma'lumotni "har doim iliq" holda ushlash.
- Bosh sahifadagi top-10 mahsulot ro'yxatini fonda qayta hisoblash.
- OAuth2 access token'ni muddati tugashidan oldin yangilash.
- ML model koeffitsiyentlarini davriy fonda qayta yuklash.

**Ehtiyot bo'ling:** `refreshAfterWrite` ni `expireAfterWrite`dan kichik qilib belgilamasangiz, pattern umuman ishlamaydi - yozuv refresh'gacha allaqachon o'chib ketadi. Shuningdek refresh thread pool'i cheklangan, kalitlar soni ko'p bo'lsa fon yangilashlari navbat yasab, latency afzalligini yo'qotadi.

## 11.7 Yaqin kesh / Ko'p qatlamli kesh (Near Cache / Multi-level L1-L2 Cache)

**Tavsif:** Ikki qatlamli topologiya: L1 - har bir application instance ichidagi local in-memory kesh (nanosekundlar, tarmoqsiz), L2 - barcha instance'lar uchun umumiy distributed kesh (millisekundlar, tarmoq orqali). O'qish L1'dan boshlanadi, miss bo'lsa L2'ga, undan ham miss bo'lsa asl manbaga boradi va yo'l-yo'lakay ikki qatlam ham to'ldiriladi. Bu tarmoq chaqiruvlari sonini keskin kamaytiradi, lekin L1'larni invalidatsiya qilish muammosini keltiradi.

**Spring'da qayerda uchraydi:** Spring Framework'ning `CompositeCacheManager` bir nechta `CacheManager`ni ketma-ket birlashtiradi, lekin haqiqiy L1→L2 promotion logikasi uchun ko'pincha `AbstractValueAdaptingCache`dan meros olgan custom `Cache` implementatsiyasi yoziladi (Caffeine + Redis). Hazelcast'da buning tayyor shakli bor: client yoki member near-cache (`NearCacheConfig`, `invalidate-on-change=true`). Redis holatida L1 invalidatsiyasi `RedisMessageListenerContainer` (pub/sub) yoki Redis 6 client-side caching (`CLIENT TRACKING`, Lettuce'ning `CacheFrontend`) orqali amalga oshiriladi.

**Qo'llanish keyslari:**
- Yuqori QPS'li autentifikatsiya filtrida permission'larni L1'da ushlab, Redis'ga har request'da bormaslik.
- Mahsulot katalogi kabi ko'p o'qiladigan, kam yoziladigan ma'lumot uchun Caffeine + Redis kombinatsiyasi.
- Hazelcast near-cache bilan reference data'ni client tomonda saqlash.
- Feature flag'larni L1'da mikrosekundlarda o'qib, o'zgarishni pub/sub orqali tarqatish.
- Multi-tenant konfiguratsiyani instance ichida keshlab, tarmoq yukini kamaytirish.

**Ehtiyot bo'ling:** Asosiy xavf - L1 invalidatsiyasi: bitta node'da `@CacheEvict` ishlasa, boshqa node'larning local keshida eski qiymat qolib ketadi, shuning uchun invalidatsiya event'i (pub/sub yoki Hazelcast invalidation) bo'lmagan multi-level kesh deyarli har doim bug manbai. L1 TTL'ni qisqa (sekundlar) tutish bu riskni cheklaydi, lekin L1'ning foydasini ham kamaytiradi.

```java
// Ko'p qatlamli kesh: L1 lokal (tez), L2 taqsimlangan (umumiy)
@Bean
CacheManager cacheManager(RedisConnectionFactory redis) {
    CaffeineCacheManager l1 = new CaffeineCacheManager("rates");
    l1.setCaffeine(Caffeine.newBuilder()
            .maximumSize(10_000)
            .expireAfterWrite(Duration.ofSeconds(30)));   // qisqa TTL shart

    RedisCacheManager l2 = RedisCacheManager.builder(redis).build();
    return new CompositeCacheManager(l1, l2);
}
// L1 ning TTL si qisqa bo'lishi kerak: u invalidatsiya xabarini ko'rmaydi,
// shuning uchun nusxalar orasida farq (stale read) paydo bo'ladi.
```

## 11.8 Taqsimlangan kesh (Distributed Cache - Redis, Hazelcast)

**Tavsif:** Kesh application process'idan tashqarida, alohida cluster'da yashaydi va barcha instance'lar uchun bitta umumiy haqiqat manbasi bo'ladi. Bu horizontal scaling'da keshning bir xil ko'rinishini kafolatlaydi, deploy va restart'dan keyin ham ma'lumot saqlanib qoladi va JVM heap'ni shishirmaydi. Narxi - har murojaat tarmoq hop'i, serialization va cluster'ga operatsion qaramlik.

**Spring'da qayerda uchraydi:** `spring-boot-starter-data-redis` + `RedisCacheManager` (Spring Boot 3.x'da `spring.cache.type=redis` bilan avtomatik), default client Lettuce; serialization `RedisCacheConfiguration#serializeValuesWith` (masalan `GenericJackson2JsonRedisSerializer`) orqali belgilanadi. Hazelcast uchun `hazelcast-spring` va `HazelcastCacheManager`, yoki JCache orqali `JCacheCacheManager`. Qo'shimcha: `spring-session-data-redis` session'ni, `spring-data-redis`ning `@EnableRedisRepositories` esa entity'larni Redis'da saqlaydi. Spring Boot 3.x'da Redis TTL'ni `spring.cache.redis.time-to-live` bilan yoki har kesh uchun alohida `RedisCacheManagerBuilderCustomizer` bilan sozlash mumkin.

**Qo'llanish keyslari:**
- Kubernetes'da bir nechta pod ishlayotganda HTTP session'ni Redis'da umumiy saqlash.
- Rate limiting hisoblagichlarini barcha instance'lar uchun atomik tarzda Redis'da yuritish.
- Og'ir hisobot natijalarini butun cluster uchun bir marta hisoblab keshlash.
- Distributed lock (Redisson yoki `SETNX`) orqali bir vaqtda bitta job ishlashini kafolatlash.
- Hazelcast `IMap` bilan real-vaqt narx jadvalini cluster bo'ylab tarqatish.

**Ehtiyot bo'ling:** Serialization formatini puxta tanlang - default `JdkSerializationRedisSerializer` class nomiga bog'lanib qoladi va deploy'dan keyin `ClassCastException` yoki deserialization xatosiga olib keladi; JSON ishlatganda esa polymorphic type'lar va `LocalDateTime` uchun `JavaTimeModule` kerak. Kesh cluster'i yagona nuqtali nosozlikka (single point of failure) aylanmasligi uchun timeout, circuit breaker va `CacheErrorHandler` bilan graceful degradation qo'shing.

```java
@Bean
RedisCacheManager cacheManager(RedisConnectionFactory cf) {
    RedisCacheConfiguration base = RedisCacheConfiguration.defaultCacheConfig()
            .entryTtl(Duration.ofMinutes(10))
            .disableCachingNullValues()
            .prefixCacheNameWith("payments:")     // nom maydoni ajratilgan
            .serializeValuesWith(SerializationPair.fromSerializer(
                    new GenericJackson2JsonRedisSerializer()));   // JDK emas: JSON

    return RedisCacheManager.builder(cf)
            .cacheDefaults(base)
            .withCacheConfiguration("rates", base.entryTtl(Duration.ofMinutes(1)))
            .build();
}
// JDK serializatsiyasi sinf o'zgarsa buziladi: JSON yoki sxema asosida saqlang
```

## 11.9 Hibernate ikkinchi darajali kesh va query kesh (Hibernate Second-Level Cache & Query Cache)

**Tavsif:** Hibernate'ning birinchi darajali keshi `EntityManager`/`Session` ichida va faqat bitta tranzaksiya umrida yashaydi; ikkinchi darajali kesh (L2) esa `SessionFactory` darajasida, barcha session'lar uchun umumiy bo'lib, entity'larni `id` bo'yicha keshlaydi. Query cache alohida mexanizm: u SQL/JPQL so'rovining parametrlari bo'yicha qaytgan identifikatorlar ro'yxatini saqlaydi, entity'larning o'zini esa L2'dan oladi. Collection cache bog'langan kolleksiyalarning id ro'yxatini keshlaydi.

**Spring'da qayerda uchraydi:** Entity ustida `@Cache(usage = CacheConcurrencyStrategy.READ_WRITE, region = "products")` (`org.hibernate.annotations.Cache`) va JPA'ning `@Cacheable`i (`jakarta.persistence.Cacheable`). Konfiguratsiya: `spring.jpa.properties.hibernate.cache.use_second_level_cache=true`, `hibernate.cache.use_query_cache=true`, `hibernate.cache.region.factory_class=org.hibernate.cache.jcache.JCacheRegionFactory` va provider sifatida Ehcache 3, Caffeine yoki Hazelcast (JSR-107 orqali). Query darajasida `@QueryHints(@QueryHint(name = "org.hibernate.cacheable", value = "true"))` yoki `Session#createQuery(...).setCacheable(true)`. Statistikani `hibernate.generate_statistics=true` + Micrometer `HibernateMetrics` bilan kuzatish mumkin.

**Qo'llanish keyslari:**
- Davlatlar, valyutalar, kategoriyalar kabi deyarli o'zgarmas reference entity'larni `READ_ONLY` strategiya bilan keshlash.
- `@ManyToOne` lookup'lar ko'p bo'lgan sahifalarda N+1 natijasida tug'ilgan `SELECT`larni L2 orqali yo'q qilish.
- `findById` bo'yicha tez-tez o'qiladigan agregat ildizini (aggregate root) keshlash.
- Kam o'zgaruvchi filtr bo'yicha ishlaydigan `@QueryHints` bilan keshlangan ro'yxat so'rovi.
- Read-only replica'ga tushadigan hisobot yukini L2 bilan kamaytirish.

**Ehtiyot bo'ling:** Query cache deyarli har doim muammoli: keshlangan so'rov tegib turgan jadvallardan biri o'zgarsa butun region invalidatsiya bo'ladi, shuning uchun yozish aktiv bo'lgan jadvallarda u foydadan ko'ra zarar keltiradi. Native SQL yoki JPQL `UPDATE`/`DELETE` bulk so'rovlari L2'ni bexabar eskirtiradi; `CacheConcurrencyStrategy.NONSTRICT_READ_WRITE` esa qisqa muddatli stale o'qishga yo'l qo'yadi - bu moliyaviy ma'lumot uchun qabul qilinmaydi.

```yaml
# Ikkinchi darajali kesh: entity bo'yicha, aniq yoqiladi
spring:
  jpa:
    properties:
      hibernate:
        cache:
          use_second_level_cache: true
          use_query_cache: false       # query kesh ko'pincha zarar keltiradi
          region.factory_class: jcache

# Entity tomonida:
# @Cache(usage = CacheConcurrencyStrategy.READ_WRITE)
# Faqat kamdan-kam o'zgaradigan ma'lumot uchun (lug'at, tarif, sozlama).
# Query kesh har jadval o'zgarishida butunlay bekor bo'ladi, shuning uchun
# yozuv ko'p bo'lgan tizimda u foyda bermaydi.
```

## 11.10 Spring Cache abstraksiyasi (Spring Cache Abstraction)

**Tavsif:** Spring Framework kesh provayderidan mustaqil deklarativ keshlash qatlamini beradi: annotatsiyalar AOP proxy orqali method chaqiruvini o'rab, natijani `Cache` interfeysi ustida saqlaydi. `@Cacheable` natijani keshlaydi va mavjud bo'lsa method'ni umuman chaqirmaydi, `@CachePut` har doim bajarib natijani keshga yozadi, `@CacheEvict` yozuvni o'chiradi, `@Caching` esa bir method ustida bir nechta kesh operatsiyasini birlashtiradi. `sync = true` bitta kalit uchun parallel yuklashlarni bitta thread'ga qisqartiradi.

**Spring'da qayerda uchraydi:** `@EnableCaching` (yoki Spring Boot auto-configuration) + `CacheManager` bean: `CaffeineCacheManager`, `RedisCacheManager`, `ConcurrentMapCacheManager` (faqat test/dev uchun), `JCacheCacheManager`. Kalit strategiyasi: `key = "#id"`, `keyGenerator`, yoki `SimpleKeyGenerator` (default). Shartlar: `condition = "#id > 0"` (chaqiruvdan oldin) va `unless = "#result == null"` (natijadan keyin). `CacheResolver` bir nechta kesh orasida dinamik tanlash uchun, `CacheErrorHandler` kesh nosozligini business xatosiga aylantirmaslik uchun ishlatiladi.

```java
@Cacheable(cacheNames = "products", key = "#id", sync = true,
           unless = "#result == null")
public Product find(Long id) { return repo.findById(id).orElse(null); }

@Caching(evict = {@CacheEvict(cacheNames = "products", key = "#p.id"),
                  @CacheEvict(cacheNames = "productList", allEntries = true)})
public void save(Product p) { repo.save(p); }
```

**Qo'llanish keyslari:**
- Service qatlamidagi og'ir `calculatePricing` method'ini `@Cacheable` bilan keshlash.
- Admin yangilaganda `@Caching` bilan bir vaqtda element keshini va ro'yxat keshini tozalash.
- `sync = true` bilan sovuq start'dagi parallel yuklanishlarni bitta database so'roviga qisqartirish.
- `@CacheEvict(allEntries = true)` ni `@Scheduled` bilan birga ishlatib, davriy to'liq yangilash.
- `CacheErrorHandler` bilan Redis tushganda application'ni ishlashda davom etishiga erishish.

**Ehtiyot bo'ling:** Annotatsiyalar proxy orqali ishlaydi, shuning uchun bitta bean ichida `this.find(id)` deb o'z method'ini chaqirsangiz kesh butunlay chetlab o'tiladi (self-invocation muammosi) - alohida bean'ga ajratish yoki `AopContext`/`ObjectProvider` orqali o'ziga murojaat qilish kerak. `sync = true` `unless` bilan birga ishlamaydi va ko'p provayderlarda faqat bitta kesh nomi bilan qo'llanadi; `@CacheEvict`ni tranzaksiya ichida ishlatganda esa rollback holatida kesh allaqachon o'zgargan bo'lishi mumkin - `TransactionAwareCacheManagerProxy` qo'shishni o'ylab ko'ring.

## 11.11 Kesh bosqini himoyasi (Cache Stampede / Thundering Herd Protection)

**Tavsif:** Ommabop (hot) kalitning TTL'si tugagan yoki kesh bo'shatilgan paytda yuzlab parallel request bir vaqtda miss oladi va hammasi birdan database'ga yoki tashqi servisga uriladi - natijada aynan keshlash oldini olishi kerak bo'lgan overload yuzaga keladi. Himoya mexanizmlari: bitta yuklovchiga ruxsat berib qolganlarini kutdirish (single-flight/mutex), TTL'ga tasodifiy jitter qo'shish, muddati tugagan qiymatni vaqtincha qaytarish (stale-while-revalidate) va proaktiv refresh.

**Spring'da qayerda uchraydi:** Eng oddiy yechim - `@Cacheable(sync = true)`, bu bitta JVM ichida bitta kalit uchun yuklashni serializatsiya qiladi (Caffeine'ning `LoadingCache` semantikasiga tayanadi). Caffeine'da `refreshAfterWrite` stale-while-revalidate beradi. Cluster bo'ylab himoya uchun distributed lock kerak: Redisson'ning `RLock` yoki `RedisTemplate` bilan `SET key value NX PX ttl` pattern'i, Spring Integration'ning `RedisLockRegistry`. TTL jitter'ni `RedisCacheManagerBuilderCustomizer` ichida har kesh uchun turli `entryTtl` berib yoki yozishda tasodifiy qo'shimcha soniya qo'shib amalga oshiriladi. Resilience4j `Bulkhead`/`RateLimiter` esa downstream'ni ortiqcha chaqiruvlardan himoya qiladi.

**Qo'llanish keyslari:**
- Bosh sahifaning og'ir "trending" so'rovini `sync = true` bilan bitta hisoblashga qisqartirish.
- Deploy'dan keyingi sovuq kesh holatida database'ni qulab tushishdan saqlash (cache warming + lock).
- Barcha kalitlarga bir xil 10 daqiqali TTL berilgan tizimda jitter qo'shib, massiv bir vaqtda expiry'ni yoyish.
- Tashqi API'ga Redisson lock bilan butun cluster'dan faqat bitta chaqiruv yuborish.
- Stale qiymatni qaytarib, fonda yangilash orqali yangilanish paytida ham javob berish.

**Ehtiyot bo'ling:** `sync = true` faqat bitta JVM ichida yordam beradi - 20 pod'li deployment'da hamon 20 parallel so'rov ketadi, shuning uchun gorizontal scale'da distributed lock yoki jitter zarur. Distributed lock'ning o'zi ham xavf: lock TTL'si yuklash vaqtidan qisqa bo'lsa ikki yuklovchi paydo bo'ladi, uzun bo'lsa esa node o'lganda kalit uzoq muddatga bloklanib qoladi.

```java
// Stampede: bitta kalit bo'sh bo'lganda ko'p so'rov manbaga ketadi
@Cacheable(cacheNames = "rates", key = "#pair", sync = true)
public Rate rate(String pair) {
    return cbuClient.fetch(pair);        // sync = true: bitta thread hisoblaydi
}

// Taqsimlangan muhitda `sync` faqat bitta nusxa ichida ishlaydi.
// Klaster bo'ylab himoya uchun qisqa muddatli qulf kerak:
Boolean acquired = redis.opsForValue()
        .setIfAbsent("lock:rate:" + pair, "1", Duration.ofSeconds(5));
// Qo'shimcha chora: TTL ga tasodifiy qo'shimcha (jitter) berib, kalitlar
// bir vaqtda eskirmasligini ta'minlash.
```

## 11.12 TTL / TTI muddati tugashi (TTL / TTI Expiration)

**Tavsif:** Keshdagi yozuv cheksiz yashamasligi uchun unga yashash muddati beriladi: TTL (time-to-live) yozuv yozilgan paytdan boshlab sanaladi, TTI (time-to-idle, ya'ni expireAfterAccess) esa oxirgi murojaatdan boshlab. TTL ma'lumotning "eskirish" darajasini (staleness bound) cheklab, invalidation logikasi bo'lmagan joyda ham eventual consistency beradi. TTI kam ishlatiladigan yozuvlarni o'zi tozalab, kesh hajmini ish yuki profiliga moslashtiradi. Ikkisi birga ishlatilsa, TTL yuqori chegara, TTI esa resurs tejash vositasi bo'ladi.

**Spring'da qayerda uchraydi:** Spring Cache abstraksiyasining o'zida TTL yo'q - u har bir provider konfiguratsiyasiga qoldiriladi. Caffeine'da `Caffeine.newBuilder().expireAfterWrite(...)` / `expireAfterAccess(...)` yoki `spring.cache.caffeine.spec=maximumSize=10000,expireAfterWrite=5m`; Redis'da `RedisCacheConfiguration.defaultCacheConfig().entryTtl(Duration.ofMinutes(10))` va `RedisCacheManagerBuilderCustomizer` bilan cache-per-cache TTL, `spring.cache.redis.time-to-live`; Spring Data Redis'da `@RedisHash(timeToLive = ...)` yoki `@TimeToLive`; Hazelcast/Infinispan'da `MapConfig` va `expiration` elementlari. JCache (JSR-107) yo'lida `ExpiryPolicy` implementatsiyalari (`CreatedExpiryPolicy`, `AccessedExpiryPolicy`) ishlatiladi. Caffeine `Expiry` interfeysi orqali yozuv bo'yicha turlicha (per-entry) TTL ham beriladi.

**Qo'llanish keyslari:**
- Kursi tez o'zgaruvchi valyuta yoki narx ma'lumotini 30-60 sekundlik TTL bilan keshlash.
- JWT public key (JWKS) va OIDC discovery metadata'sini soatlik TTL bilan ushlab turish.
- Feature flag va konfiguratsiya snapshot'ini qisqa TTL bilan keshlab, deploy'siz yangilash.
- Foydalanuvchi sessiya profilini `expireAfterAccess` bilan keshlab, nofaol userlar xotirani egallamasligini ta'minlash.
- Tashqi SOAP/REST provayder javobini SLA ruxsat bergan eskirish oynasi bo'yicha TTL bilan saqlash.

**Ehtiyot bo'ling:** Faqat `expireAfterAccess` qo'yilsa, doimiy so'rov tushadigan hot key hech qachon eskirmay, yillar davomida stale ma'lumot qaytarishi mumkin - har doim TTL bilan birga chegaralang. Barcha yozuvlarga bir xil TTL berib, ularni bir vaqtda yozsangiz, muddat tugashi sinxron bo'lib "cache stampede" keltiradi; TTL'ga kichik tasodifiy jitter qo'shing.

```java
// TTL: yozilgandan keyin. TTI: oxirgi murojaatdan keyin.
Caffeine.newBuilder()
        .expireAfterWrite(Duration.ofMinutes(10))   // TTL: eskirish kafolati
        .expireAfterAccess(Duration.ofMinutes(2))   // TTI: issiq kalit uzoq yashaydi
        .refreshAfterWrite(Duration.ofMinutes(5))   // fonda yangilash
        .maximumSize(50_000)
        .build(key -> source.load(key));
// TTL bo'lmasa kesh abadiy eskirgan qiymatni ushlab turadi.
// Faqat TTI bo'lsa, doimiy so'raladigan kalit hech qachon yangilanmaydi.
```

## 11.13 Chiqarib tashlash siyosatlari (Eviction Policies: LRU, LFU, W-TinyLFU / Caffeine)

**Tavsif:** Kesh sig'imi cheklangan bo'lgani uchun to'lganda qaysi yozuvni chiqarib tashlashni siyosat belgilaydi. LRU eng uzoq vaqt murojaat qilinmaganini, LFU eng kam chastotalini olib tashlaydi; LRU scan (bir martalik katta o'tish) tufayli "ifloslanadi", LFU esa o'tmishdagi mashhurlikka yopishib qoladi. W-TinyLFU ikkisini birlashtiradi: kichik window-LRU yangi yozuvlarni qabul qiladi, keyin chastota eskizi (count-min sketch) asosida admission filter yangi nomzodni qurbon bilan solishtiradi. Natijada Zipf taqsimotli real ish yuklarida hit ratio LRU'dan sezilarli yuqori bo'ladi.

**Spring'da qayerda uchraydi:** Caffeine (`com.github.benmanes.caffeine`) W-TinyLFU'ni amalga oshiradi va Spring Boot 3.x/4.x'da local kesh uchun amalda standart: `CaffeineCacheManager`, `Caffeine.newBuilder().maximumSize(...)` yoki og'irlik bo'yicha `maximumWeight(...).weigher(...)`. Hajm bo'yicha eviction'ni Redis o'zi `maxmemory-policy` (`allkeys-lru`, `allkeys-lfu`, `volatile-ttl`) bilan server tomonda bajaradi - bu Spring konfiguratsiyasi emas, infratuzilma sozlamasi. Hazelcast'da `EvictionConfig` (`LRU`, `LFU`, `RANDOM`), Infinispan'da `memory().maxCount(...)` ishlatiladi. Statistikani `recordStats()` va `CacheMetricsRegistrar` / Micrometer orqali `cache.gets{result=miss}` ko'rinishida kuzatish mumkin.

```java
@Bean
CacheManager cacheManager() {
    CaffeineCacheManager cm = new CaffeineCacheManager("products");
    cm.setCaffeine(Caffeine.newBuilder()
            .maximumSize(50_000)
            .expireAfterWrite(Duration.ofMinutes(10))
            .recordStats());
    return cm;
}
```

**Qo'llanish keyslari:**
- Mahsulot katalogining eng ko'p so'raladigan qismini cheklangan heap ichida ushlab turish.
- Authorization qaroriga ketadigan permission matritsasini maximumSize bilan chegaralab keshlash.
- Katta JSON javoblarni `maximumWeight` + bayt og'irligi bilan keshlab, OOM'ni oldini olish.
- Batch/report job vaqtidagi scan'dan local keshni himoyalash (W-TinyLFU admission filter).
- Redis'da `allkeys-lfu` bilan uzoq muddatli "mashhur" kalitlarni saqlab, tasodifiy kalitlarni chiqarib tashlash.

**Ehtiyot bo'ling:** `maximumSize` yozuv soni bo'yicha ishlaydi, bayt bo'yicha emas - yozuv o'lchami juda xilma-xil bo'lsa heap bashorat qilinmas bo'ladi, `weigher` ishlatish yoki o'lchov o'tkazish kerak. Eviction'ni correctness mexanizmi deb o'ylamang: yozuv istalgan paytda yo'qolishi mumkin, shuning uchun kesh hech qachon yagona haqiqat manbasi (source of truth) bo'lmasligi lozim.

## 11.14 Kesh invalidation strategiyalari (Cache Invalidation Strategies: Event-based, Versioned Keys)

**Tavsif:** TTL faqat vaqt o'tishi bilan eskirishni hal qiladi; ma'lumot o'zgarganda keshni darhol to'g'rilash uchun invalidation kerak. Event-based yondashuvda yozuv operatsiyasi (yoki outbox/CDC hodisasi) keshdan tegishli kalitni o'chiradi yoki yangilaydi - bu aniq, lekin distributed muhitda hodisa yetib bormasligi riski bor. Versioned keys yondashuvida kalitga versiya yoki entity `updatedAt`/`version` qo'shiladi, shuning uchun o'chirish umuman kerak bo'lmaydi: yangi versiya yangi kalit yaratadi, eskisi TTL bilan o'z-o'zidan tushib ketadi. Ikkinchi usul "o'chirish yetib bormadi" muammosini yo'qotadi, lekin kesh hajmini oshiradi.

**Spring'da qayerda uchraydi:** `@CacheEvict(value = "users", key = "#id")` va `@CacheEvict(allEntries = true)`, `@CachePut` bilan yangilash, `@Caching` bilan bir nechta amalni birlashtirish. Transaction bilan kelishish uchun `TransactionAwareCacheManagerProxy` yoki `@TransactionalEventListener(phase = AFTER_COMMIT)`. Distributed invalidation uchun Redis Pub/Sub (`RedisMessageListenerContainer`), Redis client-side caching tracking (Lettuce `CacheFrontend`), Hazelcast/Infinispan'ning o'zidagi cluster-wide invalidation, yoki Debezium CDC + Kafka (`@KafkaListener`) orqali keshni tozalash. Versioned key'ni `@Cacheable(key = "#user.id + ':' + #user.version")` yoki `KeyGenerator` implementatsiyasi bilan qurish mumkin.

**Qo'llanish keyslari:**
- Admin profilni o'zgartirganda barcha node'lardagi user keshini Redis Pub/Sub orqali tozalash.
- Narx o'zgarishi CDC hodisasi kelganda faqat tegishli SKU kalitlarini evict qilish.
- Katalog versiyasini `catalog:v{n}:...` prefiksi bilan oshirib, butun generatsiyani bir zarbada "almashtirish".
- Multi-tenant tizimda tenant konfiguratsiyasi o'zgarganda shu tenant prefiksini invalidate qilish.
- Deploy vaqtida build raqami kalitga kirgani uchun eski keshni avtomatik chetlab o'tish.

**Ehtiyot bo'ling:** `@CacheEvict`ni o'z-o'zidan transaction commit'dan oldin ishlashi tufayli rollback bo'lsa ham kesh tozalanadi yoki, battarroq, commit'gacha bo'shliqda eski qiymat qaytib yoziladi - transaction-aware rejim yoki after-commit hodisa ishlating. `allEntries = true` ni tez-tez chaqirish esa butun keshni yo'q qilib, DB'ga stampede yuboradi.

```java
// 1) Hodisaga asoslangan: manba o'zgarganda kesh o'chiriladi
@TransactionalEventListener(phase = TransactionPhase.AFTER_COMMIT)
void onProductUpdated(ProductUpdated e) {
    cacheManager.getCache("products").evict(e.productId());
}

// 2) Versiyalangan kalit: o'chirish kerak emas, kalit o'zgaradi
String key = "product:%d:v%d".formatted(id, product.version());
// Eski kalitlar TTL bilan o'zi o'ladi. Klaster bo'ylab izchil,
// invalidatsiya xabarini tarqatish kerak emas.
```

## 11.15 Kesh kalitini loyihalash (Cache Key Design)

**Tavsif:** Kalit keshning "indeksi" bo'lgani uchun uning dizayni to'g'ri natija, hit ratio va xavfsizlikni bir vaqtda belgilaydi. Yaxshi kalitda javobga ta'sir qiluvchi barcha o'lchamlar - entity id, tenant, locale, rol/permission scope, API versiyasi, serializatsiya formati - aniq va barqaror tartibda jamlanadi. Aks holda bir foydalanuvchi boshqasining ma'lumotini ko'radi yoki bir xil ma'lumot o'nlab kalitga tarqalib hit ratio tushadi. Kalit qisqa, deterministik va inson o'qiy oladigan bo'lsa, operatsion debugging ham osonlashadi.

**Spring'da qayerda uchraydi:** SpEL bilan aniq kalit: `@Cacheable(value = "report", key = "#tenantId + ':' + #from + ':' + #to")`; umumiy qoida uchun `KeyGenerator` bean'i (`SimpleKeyGenerator` default bo'lib, bir nechta argumentni `SimpleKey`ga o'raydi va `toString()` barqarorligiga tayanadi); Redis uchun `CacheKeyPrefix` va `RedisCacheConfiguration.computePrefixWith(...)`. Spring Security konteksti kalitga `@Cacheable(key = "#root.methodName + ':' + authentication.name")` yoki `SecurityContextHolder` orqali kiritiladi. HTTP darajasida `Vary` header bilan bir xil g'oya CDN tomonida takrorlanadi.

**Qo'llanish keyslari:**
- Multi-tenant SaaS'da har bir kalitga `tenantId` prefiksini majburiy kiritish.
- Lokalizatsiyalangan kontentni `locale` o'lchami bilan ajratib keshlash.
- API `v2`/`v3` javob shakllarini kalitdagi versiya segmenti bilan izolyatsiya qilish.
- Qidiruv filtri kombinatsiyasini normalizatsiya qilib (tartiblangan parametrlar) bitta kalitga keltirish.
- Rolga bog'liq ko'rinishlarni `role` segmenti bilan ajratib, permission oqishini oldini olish.

**Ehtiyot bo'ling:** Default `SimpleKeyGenerator` argument sinflarining `equals`/`hashCode`iga tayanadi - DTO'da ularni yozmagan bo'lsangiz kesh deyarli hech qachon hit bermaydi yoki kutilmagan to'qnashuv beradi. Kalitga tenant yoki foydalanuvchi scope'ini qo'shishni unutish - eng ko'p uchraydigan va eng xavfli kesh bug'i (ma'lumot oqishi); mutable obyektni kalit sifatida ishlatish ham yozuvni "yo'qotadi".

```java
// Kalit tarkibi: kim, nima, qanday ko'rinishda
private String key(long productId) {
    return "catalog:%s:%s:product:%d:v%d".formatted(
            TenantContext.get(),             // tenant: ma'lumot oqib ketmasligi uchun
            LocaleContextHolder.getLocale(), // til: tarjima aralashmasligi uchun
            productId,
            schemaVersion);                  // format o'zgarsa eski kalit o'qilmaydi
}
// Kalitga foydalanuvchi roli ham kirishi kerak, agar javob rolga bog'liq bo'lsa.
// Aks holda bir foydalanuvchi boshqasining ko'rinishini oladi.
```

## 11.16 HTTP keshlash (HTTP Caching: Cache-Control, ETag, CDN)

**Tavsif:** Eng arzon kesh - serverga umuman kelmagan so'rov; HTTP keshlash buni browser, proxy va CDN qatlamlarida bajaradi. `Cache-Control` (`max-age`, `s-maxage`, `no-store`, `private`, `stale-while-revalidate`) javobni kim va qancha vaqt saqlashi mumkinligini aytadi, `ETag`/`Last-Modified` esa shartli so'rov (`If-None-Match`) bilan 304 Not Modified qaytarib tarmoq trafigini yo'qqa chiqaradi. CDN qatlamida `s-maxage` va surrogate kalitlar bilan shared kesh boshqariladi. Bu pattern ayniqsa o'qishga og'ir public API va statik asset'lar uchun eng katta samara beradi.

**Spring'da qayerda uchraydi:** `ResponseEntity.ok().cacheControl(CacheControl.maxAge(Duration.ofMinutes(5)).cachePublic()).eTag(tag).body(...)`; `ShallowEtagHeaderFilter` (javob tanasidan ETag hisoblaydi); `WebRequest#checkNotModified(...)` controller ichida shartli javob uchun; `WebContentInterceptor` va statik resurslar uchun `WebMvcConfigurer#addResourceHandlers` bilan `setCacheControl(...)` hamda `ResourceUrlProvider` / `VersionResourceResolver` (content-hash fingerprint). WebFlux'da `ServerResponse`/`ServerWebExchange#checkNotModified`. Spring Security default holda `Cache-Control: no-store` qo'yadi - buni `headers().cacheControl().disable()` bilan tanlab o'chirish kerak bo'ladi.

**Qo'llanish keyslari:**
- SPA'ning hash'langan JS/CSS fayllariga `max-age=31536000, immutable` berib CDN'dan uzatish.
- Public mahsulot API'siga `s-maxage=60, stale-while-revalidate=120` qo'yib origin yukini pasaytirish.
- Og'ir JSON ro'yxatga ETag qo'yib mobil klientlarga 304 qaytarish va mobil trafikni tejash.
- OpenAPI spetsifikatsiyasi yoki referens ma'lumotnoma (davlatlar, valyutalar) javoblarini uzoq TTL bilan keshlash.
- Rasm/fayl yuklab olish endpoint'ida `Last-Modified` bilan shartli GET qo'llash.

**Ehtiyot bo'ling:** Autentifikatsiyalangan, foydalanuvchiga xos javobga `public` yoki `s-maxage` qo'yish shared CDN keshi orqali boshqa foydalanuvchiga ma'lumot oqishiga olib keladi - bunday javoblarda `private`/`no-store` va kerakli `Vary` (masalan `Vary: Authorization`) majburiy. `ShallowEtagHeaderFilter` javobni buferlab ETag hisoblaydi, ya'ni CPU va xotira sarflaydi hamda streaming/SSE javoblarni buzadi.

```java
// HTTP kesh: eng arzon kesh, chunki server umuman chaqirilmaydi
@GetMapping("/products/{id}")
ResponseEntity<ProductDto> get(@PathVariable long id) {
    Product p = service.load(id);
    return ResponseEntity.ok()
            .eTag("\"" + p.version() + "\"")
            .cacheControl(CacheControl.maxAge(Duration.ofMinutes(5))
                    .cachePublic()
                    .staleWhileRevalidate(Duration.ofMinutes(1)))
            .body(ProductDto.of(p));
}
// Shaxsiy ma'lumot uchun `cachePublic()` ishlatmang: CDN uni boshqa
// foydalanuvchiga beradi.
```

## 11.17 Memoizatsiya (Memoization)

**Tavsif:** Memoizatsiya - toza (pure), deterministik funksiya natijasini argumentlari bo'yicha saqlab, takroriy chaqiruvda hisoblashni butunlay chetlab o'tish. Bu kesh emas, balki funksiya darajasidagi mikro-optimizatsiya: I/O emas, CPU yoki allocation tejaladi. Rekursiv va dinamik algoritmlarda eksponensial ishni polinomialga tushiradi, enterprise kodda esa qimmat regex kompilyatsiyasi, reflection tahlili yoki format parsing'ini bir martaga qisqartiradi. Shart - funksiyaning yon ta'siri bo'lmasligi va natijasi vaqt bilan o'zgarmasligi.

**Spring'da qayerda uchraydi:** Eng oddiy shakli `ConcurrentHashMap#computeIfAbsent`, chegara kerak bo'lsa Caffeine `LoadingCache` (`Caffeine.newBuilder().build(key -> compute(key))`) yoki `AsyncLoadingCache`. Spring'ning o'zi ichida xuddi shu pattern keng ishlatiladi: `ResolvableType` keshlari, `AnnotationUtils`/`MergedAnnotations` ichidagi `ConcurrentReferenceHashMap`, `ConcurrentLruCache` (masalan `MimeTypeUtils`, `PathPatternParser` yo'lida), `SpelExpressionParser` natijalarini saqlash. Java darajasida `Suppliers`-uslubidagi lazy holder yoki `record` kalit bilan map, Hibernate'da query plan cache ham shu g'oyada. `@Cacheable` ham texnik jihatdan memoizatsiya, lekin proxy va serialization xarajati bilan.

**Qo'llanish keyslari:**
- Kompilyatsiya qilingan `Pattern`, `DateTimeFormatter` yoki `JsonPath` obyektlarini kalit bo'yicha saqlash.
- Reflection orqali topilgan metadata (annotatsiya, property descriptor) natijasini bir marta hisoblash.
- Murakkab tarif/soliq kalkulyatsiyasining sof funksional qismini argument bo'yicha memoize qilish.
- Grafdagi takrorlanuvchi yo'l hisob-kitobini (shortest path, dependency resolution) rekursiv memoizatsiya bilan tezlashtirish.
- Jackson `ObjectWriter` yoki `JavaType` instance'larini tip bo'yicha keshlash.

**Ehtiyot bo'ling:** Chegarasiz `HashMap` bilan memoizatsiya - klassik xotira oqishi (memory leak), ayniqsa kalit foydalanuvchi kiritmasidan kelsa; har doim `maximumSize` yoki weak/soft referens ishlating. Natija deterministik bo'lmasa (vaqt, random, tashqi holatga bog'liq) memoizatsiya nozik, takrorlanmaydigan bug'lar keltiradi. Rekursiv memoizatsiyada `computeIfAbsent` ichidan yana shu xaritaga yozilmaydi: `ConcurrentHashMap` `IllegalStateException` beradi yoki osilib qoladi, `HashMap` esa `ConcurrentModificationException` tashlaydi, shuning uchun bunday joyda `get` va `put` alohida chaqiriladi.

```java
// Memoizatsiya: bir xil argument uchun natija qayta hisoblanmaydi
@Service
public class TaxTableService {
    private final Map<Integer, TaxTable> byYear = new ConcurrentHashMap<>();

    public TaxTable forYear(int year) {
        return byYear.computeIfAbsent(year, this::loadFromDb);
    }
}
// Argument to'plami chegaralangan bo'lishi shart: aks holda bu memory leak.
// Chegarasiz bo'lsa Caffeine va maximumSize ishlatilsin.
```

## 11.18 Salbiy keshlash (Negative Caching)

**Tavsif:** Salbiy keshlash "topilmadi" yoki "yo'q" javobini ham keshlaydi, ya'ni mavjud bo'lmagan kalit uchun takroriy qimmat qidiruvni to'xtatadi. Bunisiz tizim mavjud bo'lmagan id'lar bo'yicha so'rovlar ostida DB'ga to'g'ridan-to'g'ri o'tib ketadi - bu cache penetration hujumining asosi. Amalda `null` o'rniga maxsus sentinel qiymat (`EMPTY`, bo'sh `Optional`, tombstone) saqlanadi va unga odatdagidan qisqaroq TTL beriladi, chunki "yo'q" holati "bor"ga aylanishi mumkin. Katta kalit maydoni uchun Bloom filter bilan birgalikda ishlatiladi.

**Spring'da qayerda uchraydi:** Spring Cache'da `@Cacheable(cacheNames = "users", unless = "#result == null")` default emas - aksincha, `null` ham keshlanadi va `NullValue.INSTANCE` sentinel sifatida saqlanadi; buni `RedisCacheConfiguration#disableCachingNullValues()` bilan o'chirish yoki ataylab yoqib qoldirish mumkin. Caffeine `null` qiymatni saqlamaydi, shuning uchun `Optional<T>` yoki bo'sh collection qaytarish amaliyoti qo'llaniladi. DNS darajasida JVM `networkaddress.cache.negative.ttl`, HTTP darajasida 404 javobiga `Cache-Control` berish, Resilience4j bilan esa muvaffaqiyatsiz chaqiruv natijasini qisqa muddat ushlab turish mumkin.

**Qo'llanish keyslari:**
- Mavjud bo'lmagan mahsulot SKU'si bo'yicha kelayotgan bot trafigidan DB'ni himoyalash.
- Tashqi KYC/ID tekshiruvining "topilmadi" natijasini bir necha daqiqa saqlab, qayta chaqiruv narxini tejash.
- Promo-kod tekshiruvida yaroqsiz kodlarni qisqa TTL bilan keshlash.
- Geo/IP lookup'da natija bermagan so'rovlarni keshlab, tashqi API kvotasini saqlash.
- Fayl mavjudligini tekshirishda yo'q fayl holatini qisqa muddat eslab qolish.

**Ehtiyot bo'ling:** Negative TTL uzoq bo'lsa, yangi yaratilgan resurs foydalanuvchiga "mavjud emas" bo'lib ko'rinadi - yaratish yo'lida albatta negative yozuvni evict qilish kerak. Shuningdek, xatolik (timeout, 500) bilan "haqiqatan yo'q" (404) ni farqlamay keshlash vaqtinchalik uzilishni soatlab davom etuvchi buzuq holatga aylantiradi.

```java
// Negative caching: "yo'q" javobi ham keshlanadi, lekin qisqaroq
public Optional<Profile> find(long id) {
    String key = "profile:" + id;
    String cached = redis.opsForValue().get(key);
    if ("__MISSING__".equals(cached)) return Optional.empty();   // keshlangan yo'qlik
    if (cached != null) return Optional.of(json.read(cached, Profile.class));

    Optional<Profile> found = repo.findById(id);
    redis.opsForValue().set(key,
            found.map(json::write).orElse("__MISSING__"),
            found.isPresent() ? Duration.ofMinutes(10) : Duration.ofSeconds(30));
    return found;
}
// Yo'qlikni keshlash mavjud bo'lmagan ID bilan bazani urishdan saqlaydi,
// lekin TTL qisqa bo'lishi kerak: yozuv paydo bo'lsa tez ko'rinishi uchun.
```

## 11.19 Keshni oldindan to'ldirish (Cache Warming)

**Tavsif:** Cache warming - kesh bo'sh paytdagi "sovuq start" muammosini oldini olish uchun yozuvlarni foydalanuvchi so'rovidan oldin to'ldirish. Deploy, restart yoki failover'dan keyin hit ratio nolga tushadi va butun yuk DB'ga o'tadi; oldindan to'ldirish bu cho'qqini tekislaydi. Amalda ikki shakli bor: startup'da ma'lum "issiq" to'plamni yuklash va fon rejimida davriy yangilash (refresh-ahead), ya'ni muddati tugashidan oldin qiymatni qayta hisoblash. Shunda foydalanuvchi hech qachon miss kutib turmaydi.

**Spring'da qayerda uchraydi:** Startup hook'lari: `ApplicationRunner`/`CommandLineRunner`, `@EventListener(ApplicationReadyEvent.class)`, `SmartInitializingSingleton`. Davriy yangilash uchun `@Scheduled(fixedDelay = ...)` metodida `@CachePut` yoki `Cache#put` chaqirish. Caffeine'da `refreshAfterWrite(...)` + `LoadingCache` eski qiymatni qaytarib, fon thread'da yangilaydi; `AsyncLoadingCache` bilan reaktiv yuklanish. Kubernetes muhitida warming'ni readiness probe'dan oldin bajarish uchun Spring Boot Actuator `readinessState` va `AvailabilityChangeEvent` ishlatiladi. Redis uchun warming odatda alohida job yoki `ApplicationRunner`dan `RedisTemplate` bilan bulk `opsForValue().multiSet(...)`.

```java
@EventListener(ApplicationReadyEvent.class)
void warmUp() {
    productRepository.findTopSellingIds(500)
            .forEach(productService::findById); // @Cacheable to'ldiradi
}
```

**Qo'llanish keyslari:**
- Blue-green deploy'da yangi instance'ni trafikka qo'shishdan oldin katalog keshini to'ldirish.
- Savdo aksiyasi (flash sale) boshlanishidan oldin aksiya mahsulotlarini keshga yuklash.
- Referens ma'lumotlarni (valyuta, davlat, soliq jadvali) startup'da bir marta yuklash.
- Caffeine `refreshAfterWrite` bilan hot konfiguratsiya qiymatlarini uzilishsiz yangilab turish.
- Hisobot dashboard'ining kunlik agregatlarini tungi job bilan oldindan hisoblab keshlash.

**Ehtiyot bo'ling:** Startup'da juda ko'p yozuvni yuklash ishga tushish vaqtini cho'zadi va readiness'ni kechiktiradi - warming'ni cheklangan "issiq to'plam" bilan va kerak bo'lsa asinxron bajaring. Agar warming DB'ga parallel og'ir so'rovlar yuborsa, o'zi aynan oldini olmoqchi bo'lgan yuk cho'qqisini yaratadi; throttle va batch ishlating.

## 11.20 Hot key ta'sirini yumshatish (Hot Key Mitigation)

**Tavsif:** Hot key - trafikning nomutanosib katta qismi tushadigan yagona kalit (mashhur mahsulot, bosh sahifa banneri, global konfiguratsiya). Distributed keshda u bitta shard yoki node'ni cho'ktiradi, local keshda esa shu kalit atrofida lock contention keltiradi; kalit muddati tugaganda esa minglab thread bir vaqtda DB'ga yuguradi (cache stampede / thundering herd). Yumshatish usullari: shu kalitni local (near) keshda ham ushlab turish, kalitni N nusxaga "shard"lash (`key#1..key#N`), TTL'ga jitter qo'shish va qayta hisoblashni bitta thread'ga cheklash (single-flight). Maqsad - bitta kalit uchun bir vaqtda faqat bitta qimmat hisob ketishi.

**Spring'da qayerda uchraydi:** Caffeine `LoadingCache` o'zi per-key single-flight beradi - bir kalit uchun bir yuklovchi thread ishlaydi, qolganlari kutadi; `AsyncLoadingCache` buni non-blocking qiladi. Ikki qatlamli (near cache) tuzilma uchun Caffeine + Redis'ni `CompositeCacheManager` yoki Redis client-side caching (Lettuce tracking) bilan birlashtirish; Hazelcast'da `NearCacheConfig` tayyor. Distributed single-flight uchun Redisson `RLock`/`getSemaphore`, Spring Integration `LockRegistry` (`RedisLockRegistry`, `JdbcLockRegistry`) ishlatiladi; Resilience4j `Bulkhead` bilan backend'ga parallel chaqiruvni cheklash mumkin. Hot key'ni aniqlashda Redis `--hotkeys` va Micrometer kesh metrikalari yordam beradi.

**Qo'llanish keyslari:**
- Bosh sahifa feed'ini har bir app node'ida near cache sifatida saqlab, Redis'dagi hot shard'ni bo'shatish.
- Flash sale paytida bitta mahsulot kalitini `product:123#0..#7` ko'rinishida bo'lib, shard yukini tarqatish.
- Global feature-flag snapshot'ini local keshda ushlab, Redis'ga faqat invalidation signalini qoldirish.
- Muddati tugagan hot kalitni distributed lock bilan faqat bitta instance qayta hisoblashi.
- TTL'ga ±10% jitter qo'shib, mashhur kalitlar guruhining bir vaqtda eskirishini yoyish.

**Ehtiyot bo'ling:** Distributed lock bilan single-flight qilish deadlock va lock timeout muammolarini olib keladi - lock muddatini hisob vaqtidan uzunroq qo'yib, lock olmagan thread uchun "eski qiymatni qaytarish" (serve-stale) yo'lini ko'rib chiqing. Near cache qo'shish esa consistency oynasini kengaytiradi: endi invalidation ikki qatlamga ham yetib borishi kerak.

```java
// Hot key: bitta kalit butun yukni tortadi
// 1) Lokal L1 kesh qo'shish: so'rov Redis ga ham yetib bormaydi
Caffeine.newBuilder().maximumSize(1_000)
        .expireAfterWrite(Duration.ofSeconds(5)).build();

// 2) Kalitni bo'lish (key splitting): yuk nusxalar bo'ylab tarqaladi
int shard = ThreadLocalRandom.current().nextInt(8);
String key = "banner:active:" + shard;      // 8 ta nusxa, biri o'qiladi

// Hot key ni topish: Redis `--hotkeys` yoki kalit prefiksi bo'yicha metrika.
```

## 11.21 So'rov doirasidagi kesh (Request-Scoped Cache)

**Tavsif:** Bitta HTTP so'rovi yoki bitta transaction ichida bir xil ma'lumot bir necha marta so'ralishi juda keng tarqalgan (validator, mapper, security check hammasi bir xil userni oladi). Request-scoped kesh shu qiymatni so'rov davomiyligida saqlab, takroriy DB yoki remote chaqiruvni yo'qotadi, lekin so'rov tugashi bilan o'chadi. Shu sababli unda eskirish (staleness) riski deyarli yo'q - ma'lumot faqat bir so'rov ichida "muzlatiladi". Bu read-your-own-writes semantikasini buzmasligi uchun ham qulay.

**Spring'da qayerda uchraydi:** `@Scope(value = "request", proxyMode = ScopedProxyMode.TARGET_CLASS)` bilan bean (yoki `@RequestScope`, `@SessionScope`), `RequestContextHolder` va `ServletRequestAttributes#setAttribute(..., SCOPE_REQUEST)`. JPA'ning first-level cache'i (`EntityManager`/Hibernate `Session`) amalda transaction-scoped keshdir va `@Transactional` chegarasida ishlaydi; Hibernate `StatelessSession`da esa yo'q. GraphQL'da `DataLoader` per-request batching va keshni birga beradi (`spring-graphql` `BatchLoaderRegistry`). WebFlux'da request scope ishlamaydi - o'rniga `Mono#cache()`, `contextWrite` yoki `ServerWebExchange` atributlari ishlatiladi. Micrometer Tracing/MDC bilan bir xil so'rov kontekstini ulash ham shu doirada.

**Qo'llanish keyslari:**
- Bir so'rov ichida bir necha joyda kerak bo'lgan `Authentication` → `User` entity'sini bir marta yuklash.
- GraphQL resolverlarda N+1 muammosini `DataLoader` per-request kesh bilan yo'qotish.
- Murakkab validatsiya zanjirida bir xil referens ma'lumotni qayta-qayta o'qimaslik.
- Hisobot generatsiyasida bir transaction ichida takroriy lookup natijalarini saqlash.
- Tashqi provayder (masalan, tarif xizmati) javobini bitta so'rov doirasida bir martaga qisqartirish.

**Ehtiyot bo'ling:** Request-scoped bean'ni singleton'ga to'g'ridan-to'g'ri inject qilish `scoped proxy` bo'lmasa xato beradi yoki, battarroq, birinchi so'rovning holatini barcha so'rovlarga tarqatadi. Async yoki reaktiv kodda `ThreadLocal` asosidagi kontekst thread almashganda yo'qoladi yoki boshqa so'rovga "sizib" o'tadi - `@Async`, `CompletableFuture` va WebFlux yo'lida kontekst propagatsiyasini ataylab sozlang.

```java
// So'rov doirasidagi kesh: bir so'rov ichida takroriy chaqiruv bir marta
@Component
@RequestScope
public class RequestRateCache {
    private final Map<String, Rate> cache = new HashMap<>();   // thread bitta
    private final RateService source;

    public Rate rate(String pair) {
        return cache.computeIfAbsent(pair, source::rate);
    }
}
// Bir so'rovda 50 qator uchun bir xil kursni 50 marta so'rash o'rniga bir marta.
// Invalidatsiya muammosi yo'q: so'rov tugashi bilan kesh yo'qoladi.
```

## 11.22 Kesh konsistensiyasi murosalari (Cache Consistency Trade-offs)

**Tavsif:** Kesh - joylangan nusxa, ya'ni har qanday kesh dizayni "qanchalik eski ma'lumotga toqat qilamiz" degan savolga javobdir. Strong consistency uchun write-through + sinxron invalidation va distributed lock kerak bo'ladi, bu esa kechikish va murakkablik qo'shadi; eventual consistency arzon va tez, lekin foydalanuvchi o'z o'zgarishini darhol ko'rmasligi mumkin. Amaliy yechim - SLA darajasida eskirish chegarasini (staleness budget) ochiq belgilash: pul va huquqiy ma'lumotlarga nol, katalog va analitikaga sekundlar yoki daqiqalar. Alohida e'tibor - bir vaqtdagi yozuv va o'qish oralig'ida eski qiymat keshga qaytib yozilishi (stale set) muammosi.

**Spring'da qayerda uchraydi:** `@Transactional` + `TransactionAwareCacheManagerProxy` yoki `@TransactionalEventListener(AFTER_COMMIT)` bilan kesh amallarini commit'ga bog'lash; Hibernate second-level cache'da `@Cache(usage = CacheConcurrencyStrategy.READ_WRITE | NONSTRICT_READ_WRITE | TRANSACTIONAL)` tanlovi aynan bu murosani ifodalaydi, `@NaturalIdCache` va query cache esa qo'shimcha nozikliklar keltiradi. Redis tomonida optimistik yangilash uchun `RedisTemplate` + `WATCH/MULTI` (`SessionCallback`) yoki Redisson'ning atomik tuzilmalari; `@Version` bilan optimistic locking esa stale yozuvni DB darajasida ushlaydi. Monitoring uchun Micrometer `cache.*` metrikalari va "oxirgi invalidation yoshi" ko'rsatkichi.

**Qo'llanish keyslari:**
- Hisob balansi va to'lov holatini umuman keshlamaslik yoki faqat request-scoped keshda ushlash.
- Katalog va kontent sahifalariga 1-5 daqiqalik eventual consistency'ni ataylab qabul qilish.
- Foydalanuvchi o'z profilini tahrirlagandan keyin read-your-own-writes uchun shu sessiyani keshni chetlab o'tishga majburlash.
- Audit/compliance hisobotlarini faqat snapshot vaqti aniq belgilangan holda keshlash.
- Hibernate `READ_WRITE` strategiyasini kam o'zgaruvchi referens entity'lar uchun tanlash.

**Ehtiyot bo'ling:** Eng ko'p uchraydigan xato - konsistensiya talabini hujjatlashtirmaslik: kesh "optimizatsiya" sifatida kiritiladi, keyin biznes uni haqiqat manbai deb o'ylaydi va eskirgan qiymat moliyaviy xatoga aylanadi. "Avval DB'ni yangila, keyin keshni o'chir" tartibini buzish yoki yangilashda `@CachePut` bilan eski qiymatni yozib qo'yish ham bir vaqtda ishlayotgan thread'lar tufayli doimiy stale holat qoldiradi.

```java
// Izchillik tanlovi aniq yozilishi kerak
@Transactional
public void updatePrice(long id, Money price) {
    repo.updatePrice(id, price);
    // Variant A: commit'dan keyin o'chirish - qisqa vaqt eskirgan qiymat o'qiladi
    TransactionSynchronizationManager.registerSynchronization(
            new TransactionSynchronization() {
                @Override public void afterCommit() { cache.evict(id); }
            });
    // Variant B: oldin o'chirish - rollback bo'lsa kesh keraksiz bo'shaydi (xavfsiz)
    // Variant C: versiyalangan kalit - eskirgan qiymat umuman o'qilmaydi
}
// Har bir kesh uchun javob yozilgan bo'lishi kerak: necha sekund eskirish
// qabul qilinadi va bu biznes uchun nimani bildiradi.
```

## 11.23 Amalda qo'llash

- [ ] Har bir kesh uchun TTL, maksimal hajm va eviction siyosatini yozib qo'ying; chegarasiz kesh xotira oqishi demak.
- [ ] Keshlanadigan har bir so'rovning `EXPLAIN (ANALYZE, BUFFERS)` natijasini o'lchang; 1 ms dan tez bo'lsa keshni olib tashlashni taklif qiling.
- [ ] `@Cacheable` metodlari o'z sinfi ichidan chaqirilmayotganini tekshiring - self-invocation proxy'ni chetlab o'tadi.
- [ ] Kesh kaliti tarkibini ko'rib chiqing: foydalanuvchi, tenant va lokal kalitga kiritilganmi, aks holda ma'lumot oqib ketadi.
- [ ] Invalidatsiya yo'lini har bir kesh uchun chizib bering: kim, qachon va qanday tozalaydi.
- [ ] Stampede himoyasi borligini tekshiring: bitta kalit bir vaqtda ko'p so'rovga tushganda nima bo'ladi.
- [ ] Redis ishlatilsa, serializatsiya formati va versiyalashni hujjatlashtiring; sinf o'zgarsa eski qiymatlar o'qiladimi.
- [ ] Kesh hit nisbatini metrika sifatida chiqarib, 80 foizdan past keshlarni qayta ko'rib chiqish ro'yxatiga qo'ying.

---

[&larr; 10. Ma'lumotlarni boshqarish va taqsimlash patternlari](10-malumotlarni-boshqarish-va-taqsimlash.md) · [Mundarija](README.md) · [12. Arxitektura uslublari &rarr;](12-arxitektura-uslublari.md)
