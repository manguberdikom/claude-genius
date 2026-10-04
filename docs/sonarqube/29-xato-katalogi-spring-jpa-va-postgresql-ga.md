<!-- doc: sonarqube | chapter: 29 | part: VII. Xato katalogi: qanday kod qanday xato hisoblanadi -->

[SonarQube](../../README.md) / [SonarQube](README.md)

# 29. Xato katalogi: Spring, JPA va PostgreSQL ga xos xatolar (Catalog: Spring, JPA and PostgreSQL)

<details>
<summary>Bu bobdagi 17 bo'lim</summary>

- [29.1 Maydonga `@Autowired` qo'yish](#291-maydonga-autowired-qoyish)
- [29.2 Singleton bean ichida o'zgaruvchan holat saqlash](#292-singleton-bean-ichida-ozgaruvchan-holat-saqlash)
- [29.3 `@Transactional` ni `private` yoki ichki chaqiriladigan metodga qo'yish](#293-transactional-ni-private-yoki-ichki-chaqiriladigan-metodga-qoyish)
- [29.4 Controller da biznes mantiq va uni servisga ko'chirish](#294-controller-da-biznes-mantiq-va-uni-servisga-kochirish)
- [29.5 Entity ni to'g'ridan-to'g'ri API javobida qaytarish](#295-entity-ni-togridan-togri-api-javobida-qaytarish)
- [29.6 Entity da `equals` va `hashCode` ni noto'g'ri yozish](#296-entity-da-equals-va-hashcode-ni-notogri-yozish)
- [29.7 `@OneToMany` da `FetchType.EAGER` va N+1 xavfi](#297-onetomany-da-fetchtypeeager-va-n1-xavfi)
- [29.8 Repository metodida barcha qatorlarni olish va sahifalashsiz ishlash](#298-repository-metodida-barcha-qatorlarni-olish-va-sahifalashsiz-ishlash)
- [29.9 Native query da satr birlashtirish](#299-native-query-da-satr-birlashtirish)
- [29.10 `@Value` bilan maxfiy ma'lumotni standart qiymat sifatida yozish](#2910-value-bilan-maxfiy-malumotni-standart-qiymat-sifatida-yozish)
- [29.11 Konfiguratsiyada parol va kalitni ochiq saqlash](#2911-konfiguratsiyada-parol-va-kalitni-ochiq-saqlash)
- [29.12 Katta `@Configuration` klassi va ortiqcha bean](#2912-katta-configuration-klassi-va-ortiqcha-bean)
- [29.13 Istisnolarni controller da umumiy ushlash va ma'lumotni oshkor qilish](#2913-istisnolarni-controller-da-umumiy-ushlash-va-malumotni-oshkor-qilish)
- [29.14 `RestTemplate` yoki `WebClient` ni timeout siz ishlatish](#2914-resttemplate-yoki-webclient-ni-timeout-siz-ishlatish)
- [29.15 Oddiy yondashuv va arxitektor yondashuvi](#2915-oddiy-yondashuv-va-arxitektor-yondashuvi)
- [29.16 Tuzoq va yechim](#2916-tuzoq-va-yechim)
- [29.17 Amalda qo'llash](#2917-amalda-qollash)

</details>



Spring va JPA loyihalarida Sonar shikoyatlarining katta qismi bir necha o'nlab takrorlanuvchi holatdan kelib chiqadi. Bu bob shu holatlarni katalog sifatida yig'adi: avval qisqa xulosa jadvali, keyin har bir holat uchun shikoyat qilinadigan kod va tuzatilgan variant. Bu yerda faqat bitta savolga javob bor: Sonar nima deydi va kodni qanday o'zgartirsak shikoyat yo'qoladi.

| Kod holati | Sonar nima deydi | Toifa | Jiddiylik (taxminan) | Ta'siri |
|---|---|---|---|---|
| Maydonga `@Autowired` | Field injection ishlatilmasin, konstruktor orqali kirit (`java:S6813`) | maintainability (code smell) | Major | Bean ni test da yaratish qiyin, majburiy bog'liqlik ko'rinmaydi |
| Singleton bean da o'zgaruvchan maydon | Umumiy holat sinxronlanmagan, poyga xavfi bor | reliability (bug) | Critical | Yuklama ostida natija noto'g'ri, xato takrorlanmaydi |
| `private` metodda `@Transactional` | Annotatsiya kuchga kirmaydi, proxy uni ko'rmaydi | reliability (bug) | Major | Tranzaksiya ochilmaydi, rollback ishlamaydi |
| Controller da biznes mantiq | Metod juda murakkab, cognitive complexity chegaradan oshdi (`java:S3776`) | maintainability (code smell) | Critical | Test yozish qiyin, coverage past qoladi |
| Entity ni API javobida qaytarish | Ichki modelni tashqariga ochish, lazy maydon va ortiqcha ma'lumot | security hotspot va code smell | Major | Ma'lumot oshkor bo'ladi, sxema o'zgarsa API sinadi |
| Entity da `equals` faqat `id` bo'yicha emas | `equals` va `hashCode` kelishmaydi, shartnoma buzildi | reliability (bug) | Critical | `Set` ichida dublikat, collection da element topilmaydi |
| `@OneToMany(fetch = EAGER)` | Eager yuklash keraksiz so'rovlarni keltiradi | maintainability (code smell) | Major | N+1 so'rov, javob vaqti o'sadi |
| `findAll()` ni cheklovsiz chaqirish | Natija hajmi cheklanmagan, sahifalash yo'q | reliability (bug) | Major | Katta jadvalda xotira tugaydi |
| Native query da satr birlashtirish | SQL ni dinamik qurish, injection xavfi (`java:S2077`) | security (vulnerability) | Blocker | Tashqi kiritish bilan baza o'qiladi yoki o'zgartiriladi |
| `@Value` da maxfiy standart qiymat | Kodda qattiq yozilgan parol yoki kalit (`java:S2068`) | security (vulnerability) | Blocker | Kalit git tarixida qoladi, rotatsiya qilinmaydi |
| `application.yml` da ochiq parol | Konfiguratsiyada credential saqlanmoqda (`java:S2068`) | security (vulnerability) | Blocker | Artifact ichida parol tarqaladi |
| 40 ta bean li `@Configuration` | Klass juda katta, javobgarlik aralashgan | maintainability (code smell) | Major | O'zgarish narxi oshadi, kontekst sekin ko'tariladi |
| `catch (Exception e)` va stack trace javobda | Umumiy istisno ushlanmoqda (`java:S2221`), ichki ma'lumot oshkor | security hotspot va code smell | Critical | Ichki tuzilma tashqariga chiqadi, xato yashiriladi |
| `RestTemplate` timeout siz | Tashqi chaqiruv cheksiz kutishi mumkin | reliability (bug) | Major | Thread pool to'ladi, servis javob bermaydi |

## 29.1 Maydonga `@Autowired` qo'yish

Shikoyat qilinadigan kod:

```java
@Service
public class ToLovServisi {
    // Sonar shikoyati: field injection
    @Autowired
    private HisobRepository hisobRepository;
    @Autowired
    private KursProvayderi kursProvayderi;
}
```

Sonar buni `java:S6813` bo'yicha belgilaydi. Maydonga kiritilgan bog'liqlikni `final` qilib bo'lmaydi, shuning uchun bean yaratilgandan keyin ham almashtirilishi mumkin.

Tuzatilgan kod:

```java
@Service
public class ToLovServisi {
    private final HisobRepository hisobRepository;
    private final KursProvayderi kursProvayderi;

    // Bitta konstruktor bo'lsa @Autowired shart emas
    public ToLovServisi(HisobRepository hisobRepository,
                        KursProvayderi kursProvayderi) {
        this.hisobRepository = hisobRepository;
        this.kursProvayderi = kursProvayderi;
    }
}
```

Tavsiya: barcha majburiy bog'liqlikni `final` maydon va bitta konstruktor orqali kirit.

## 29.2 Singleton bean ichida o'zgaruvchan holat saqlash

Shikoyat qilinadigan kod:

```java
@Service
public class HisobotServisi {
    // Sonar shikoyati: singleton da umumiy o'zgaruvchan holat
    private BigDecimal joriyJami = BigDecimal.ZERO;

    public BigDecimal hisobla(List<Buyurtma> buyurtmalar) {
        joriyJami = BigDecimal.ZERO;
        buyurtmalar.forEach(b -> joriyJami = joriyJami.add(b.summa()));
        return joriyJami;
    }
}
```

Sonar bu holatni ikki tomondan ko'radi: bean maydoni sinxronlanmagan holda o'zgartiriladi va metod natijasi umumiy maydonga bog'liq. Spring bean i standart holda singleton, shuning uchun bir vaqtda kelgan ikki so'rov bir xil maydonni yozadi.

Tuzatilgan kod:

```java
@Service
public class HisobotServisi {
    public BigDecimal hisobla(List<Buyurtma> buyurtmalar) {
        // Holat metod ichida, har bir chaqiruv mustaqil
        return buyurtmalar.stream()
                .map(Buyurtma::summa)
                .reduce(BigDecimal.ZERO, BigDecimal::add);
    }
}
```

Tavsiya: bean maydoni faqat `final` bog'liqlik uchun, hisob holati esa metod lokal o'zgaruvchisida yashasin.

## 29.3 `@Transactional` ni `private` yoki ichki chaqiriladigan metodga qo'yish

Shikoyat qilinadigan kod:

```java
@Service
public class BuyurtmaServisi {
    public void qabulQil(Buyurtma b) {
        // Shikoyat: o'z klassidan chaqirilgan @Transactional ishlamaydi
        saqla(b);
    }

    @Transactional
    private void saqla(Buyurtma b) {
        buyurtmaRepository.save(b);
        qoldiqRepository.kamaytir(b.mahsulotId(), b.soni());
    }
}
```

Sonar `@Transactional` ni `private` metodda yoki o'z klassi ichidan chaqirilgan metodda ko'rsa shikoyat qiladi. Sabab proxy orqali chaqiruv bo'lmasligi, demak annotatsiya umuman bajarilmaydi.

Tuzatilgan kod:

```java
@Service
public class BuyurtmaServisi {
    // Annotatsiya tashqaridan chaqiriladigan public metodda
    @Transactional
    public void qabulQil(Buyurtma b) {
        buyurtmaRepository.save(b);
        qoldiqRepository.kamaytir(b.mahsulotId(), b.soni());
    }
}
```

Tavsiya: `@Transactional` ni faqat tashqaridan chaqiriladigan `public` metodga qo'y, ichki chaqiruvga tayanma.

## 29.4 Controller da biznes mantiq va uni servisga ko'chirish

Shikoyat qilinadigan kod:

```java
@PostMapping("/buyurtma")
public ResponseEntity<?> yarat(@RequestBody BuyurtmaSorovi s) {
    if (s.soni() <= 0) return ResponseEntity.badRequest().build();
    var mahsulot = mahsulotRepository.findById(s.mahsulotId()).orElse(null);
    if (mahsulot == null) return ResponseEntity.notFound().build();
    if (mahsulot.getQoldiq() < s.soni()) return ResponseEntity.status(409).build();
    var chegirma = s.soni() > 10 ? new BigDecimal("0.1") : BigDecimal.ZERO;
    // ... yana o'nlab shart va hisob
    return ResponseEntity.ok(buyurtmaRepository.save(new Buyurtma()));
}
```

Sonar bu metodda `java:S3776` cognitive complexity chegarasidan oshganini aytadi va ko'pincha metod uzunligi haqida ham ogohlantiradi. Bunday metodni test bilan yopish uchun o'nlab mock kerak, shuning uchun coverage past qoladi.

Tuzatilgan kod:

```java
@PostMapping("/buyurtma")
public ResponseEntity<BuyurtmaJavobi> yarat(@Valid @RequestBody BuyurtmaSorovi s) {
    // Controller faqat uzatadi, qaror servisda
    return ResponseEntity.ok(buyurtmaServisi.yarat(s));
}
```

Tavsiya: controller da faqat validatsiya annotatsiyasi va chaqiruv qolsin, qarorni servisga ko'chir va shu servisni oddiy unit test bilan yop.

## 29.5 Entity ni to'g'ridan-to'g'ri API javobida qaytarish

Shikoyat qilinadigan kod:

```java
@GetMapping("/hisob/{id}")
public Hisob hisob(@PathVariable Long id) {
    // Shikoyat: ichki model tashqariga chiqdi
    return hisobRepository.findById(id).orElseThrow();
}
```

Sonar bu holatda bir nechta shikoyat beradi: ichki domen obyektini tashqi chegaraga chiqarish code smell, parol hash i yoki ichki izoh kabi maydonlar bo'lsa security hotspot. JPA entity sida lazy bog'lanish bo'lsa serializatsiya paytida qo'shimcha so'rov yoki istisno chiqadi.

Tuzatilgan kod:

```java
public record HisobJavobi(Long id, String raqam, BigDecimal qoldiq) {
    // Faqat tashqariga kerak maydonlar
    static HisobJavobi dan(Hisob h) {
        return new HisobJavobi(h.getId(), h.getRaqam(), h.getQoldiq());
    }
}

@GetMapping("/hisob/{id}")
public HisobJavobi hisob(@PathVariable Long id) {
    return HisobJavobi.dan(hisobServisi.topish(id));
}
```

Tavsiya: har bir endpoint uchun alohida `record` javob tipi tuz va entity ni web qatlamidan chiqarma.

## 29.6 Entity da `equals` va `hashCode` ni noto'g'ri yozish

Shikoyat qilinadigan kod:

```java
@Entity
public class Mahsulot {
    @Id @GeneratedValue
    private Long id;
    private String nomi;

    // Shikoyat: faqat equals bor, hashCode yo'q
    @Override
    public boolean equals(Object o) {
        return o instanceof Mahsulot m && Objects.equals(nomi, m.nomi);
    }
}
```

Sonar `equals` va `hashCode` ni juft holda talab qiladi va faqat bittasi yozilgan bo'lsa reliability xatosi beradi. Ikkinchi muammo esa o'zgaradigan maydon bo'yicha taqqoslash: entity `HashSet` ga qo'shilgandan keyin `nomi` o'zgarsa, element topilmay qoladi.

Tuzatilgan kod:

```java
@Entity
public class Mahsulot {
    @Id @GeneratedValue
    private Long id;
    private String nomi;

    @Override
    public boolean equals(Object o) {
        // Faqat saqlangan entity lar id bo'yicha teng
        if (!(o instanceof Mahsulot m)) return false;
        return id != null && id.equals(m.id);
    }

    @Override
    public int hashCode() {
        // Doimiy qiymat, id keyin o'rnatilsa ham buzilmaydi
        return Mahsulot.class.hashCode();
    }
}
```

Tavsiya: entity da `equals` ni faqat `id` bo'yicha yoz, `hashCode` ni esa o'zgarmaydigan qiymatga bog'la.

## 29.7 `@OneToMany` da `FetchType.EAGER` va N+1 xavfi

Shikoyat qilinadigan kod:

```java
@Entity
public class Buyurtma {
    // Shikoyat: EAGER kolleksiya
    @OneToMany(mappedBy = "buyurtma", fetch = FetchType.EAGER)
    private List<BuyurtmaQatori> qatorlar = new ArrayList<>();
}
```

Sonar `EAGER` kolleksiyani maintainability shikoyati sifatida belgilaydi, chunki har qanday o'qish avtomatik qo'shimcha so'rov keltiradi. Ro'yxat so'rovida bu N+1 ga aylanadi: yuz buyurtma uchun yuz bitta qo'shimcha so'rov ketadi.

Tuzatilgan kod:

```java
@Entity
public class Buyurtma {
    // Standart LAZY, kerak bo'lganda aniq yuklaymiz
    @OneToMany(mappedBy = "buyurtma", fetch = FetchType.LAZY)
    private List<BuyurtmaQatori> qatorlar = new ArrayList<>();
}

public interface BuyurtmaRepository extends JpaRepository<Buyurtma, Long> {
    @EntityGraph(attributePaths = "qatorlar")
    List<Buyurtma> findByMijozId(Long mijozId);
}
```

Tavsiya: barcha bog'lanishni `LAZY` qoldir va kerak bo'lgan joyda `@EntityGraph` yoki `join fetch` bilan aniq yukla.

## 29.8 Repository metodida barcha qatorlarni olish va sahifalashsiz ishlash

Shikoyat qilinadigan kod:

```java
public List<BuyurtmaJavobi> hammasi() {
    // Shikoyat: cheklovsiz natija
    return buyurtmaRepository.findAll().stream()
            .map(BuyurtmaJavobi::dan)
            .toList();
}
```

Sonar cheklovsiz `findAll()` natijasini xotiraga yig'ishni reliability muammosi deb belgilaydi, ayniqsa natija tashqi so'rovga javob bo'lib ketsa. Jadval o'sgani sari metod sekinlashadi va bir kun `OutOfMemoryError` bilan tugaydi.

Tuzatilgan kod:

```java
public Page<BuyurtmaJavobi> royxat(Pageable pageable) {
    // Sahifa hajmi tashqaridan keladi, lekin cheklangan
    return buyurtmaRepository.findAll(pageable).map(BuyurtmaJavobi::dan);
}
```

```properties
# Sahifa hajmiga qattiq chegara
spring.data.web.pageable.default-page-size=20
spring.data.web.pageable.max-page-size=100
```

Tavsiya: tashqariga chiqadigan har bir ro'yxat `Pageable` qabul qilsin va maksimal sahifa hajmi konfiguratsiyada cheklansin.

## 29.9 Native query da satr birlashtirish

Shikoyat qilinadigan kod:

```sql
-- Kodda shunday qurilgan so'rov
SELECT * FROM buyurtma WHERE holat = 'YANGI' AND mijoz_id = 42 ORDER BY yaratilgan_at
```

```java
public List<Buyurtma> topish(String holat, String tartib) {
    // Shikoyat: SQL satr birlashtirish bilan qurilmoqda
    String sql = "SELECT * FROM buyurtma WHERE holat = '" + holat
            + "' ORDER BY " + tartib;
    return em.createNativeQuery(sql, Buyurtma.class).getResultList();
}
```

Bu `java:S2077` qoidasi, security vulnerability toifasi va eng yuqori jiddiylik. Sonar tashqaridan kelgan qiymat SQL satriga qo'shilayotganini taint tahlili bilan kuzatadi. Parametrga bog'lanmagan har qanday qiymat injection yo'li, `ORDER BY` qismi esa parametr bo'lolmaydi, shuning uchun uni ruxsat etilgan ro'yxat orqali tekshirish kerak.

Tuzatilgan kod:

```java
private static final Set<String> RUXSAT = Set.of("yaratilgan_at", "summa");

public List<Buyurtma> topish(String holat, String tartib) {
    // Tartib ustuni faqat ruxsat ro'yxatidan
    String ustun = RUXSAT.contains(tartib) ? tartib : "yaratilgan_at";
    return em.createNativeQuery(
                    "SELECT * FROM buyurtma WHERE holat = :holat ORDER BY " + ustun,
                    Buyurtma.class)
            .setParameter("holat", holat)
            .getResultList();
}
```

Tavsiya: qiymatni har doim nomli parametr bilan uzat, identifikatorni esa qattiq ruxsat ro'yxatidan tanla.

## 29.10 `@Value` bilan maxfiy ma'lumotni standart qiymat sifatida yozish

Shikoyat qilinadigan kod:

```java
@Service
public class ToLovShlyuzi {
    // Shikoyat: kodda qattiq yozilgan kalit
    @Value("${tolov.api-kalit:sk_live_9f3a21bc77}")
    private String apiKalit;
}
```

Sonar buni `java:S2068` bo'yicha hard-coded credential deb belgilaydi. Standart qiymat qulay ko'rinadi, lekin u git tarixiga tushadi va o'chirilganidan keyin ham tarixda qoladi.

Tuzatilgan kod:

```java
@Service
public class ToLovShlyuzi {
    private final String apiKalit;

    // Standart qiymat yo'q: kalit bo'lmasa kontekst ko'tarilmaydi
    public ToLovShlyuzi(@Value("${tolov.api-kalit}") String apiKalit) {
        this.apiKalit = apiKalit;
    }
}
```

Tavsiya: maxfiy qiymatga standart berma, u yo'q bo'lsa ilova ishga tushmasligi to'g'ri xatti harakat.

## 29.11 Konfiguratsiyada parol va kalitni ochiq saqlash

Shikoyat qilinadigan kod:

```yaml
spring:
  datasource:
    url: jdbc:postgresql://db.prod.internal:5432/buyurtma
    username: buyurtma_app
    # Shikoyat: ochiq parol
    password: Pr0d_Parol_2025
```

Sonar konfiguratsiya faylidagi parolni ham `java:S2068` yoki unga mos secrets qoidasi bilan topadi va ko'pincha `sonar.secrets` tahlili alohida ogohlantirish beradi. Bu qiymat build artifact ichiga kirib ketadi, demak jar ni olgan har kim bazaga ulanadi.

Tuzatilgan kod:

```yaml
spring:
  datasource:
    url: ${DB_URL}
    username: ${DB_USER}
    # Qiymat muhit o'zgaruvchisi yoki secret manager dan keladi
    password: ${DB_PASSWORD}
```

Tavsiya: har qanday credential ni muhit o'zgaruvchisi yoki secret store ga ko'chir, repozitoriyada faqat placeholder qolsin.

## 29.12 Katta `@Configuration` klassi va ortiqcha bean

Shikoyat qilinadigan kod:

```java
@Configuration
public class IlovaKonfiguratsiyasi {
    // Shikoyat: klass juda katta, javobgarlik aralashgan
    @Bean ObjectMapper objectMapper() { return new ObjectMapper(); }
    @Bean RestTemplate restTemplate() { return new RestTemplate(); }
    @Bean DataSource dataSource() { /* ... */ }
    @Bean CacheManager cacheManager() { /* ... */ }
    @Bean TaskExecutor taskExecutor() { /* ... */ }
    // ... yana 30 ta bean
}
```

Sonar bunday klassda bir necha qoidani birga ishga tushiradi: klass hajmi, metodlar soni va ko'pincha ortiqcha `import` bog'liqligi. Yana bir shikoyat Spring Boot allaqachon beradigan bean ni qo'lda qayta e'lon qilish, masalan `ObjectMapper`, chunki bu auto configuration ni jimgina buzadi.

Tuzatilgan kod:

```java
// Har bir mavzu alohida konfiguratsiyada
@Configuration
class TashqiMijozKonfiguratsiyasi {
    @Bean
    RestClient tolovMijozi(RestClient.Builder builder) {
        return builder.baseUrl("https://tolov.internal").build();
    }
}

@Configuration
@EnableCaching
class KeshKonfiguratsiyasi { /* faqat kesh bean lari */ }
```

Tavsiya: konfiguratsiyani mavzu bo'yicha bo'l va Boot auto configuration bergan bean ni qo'lda qayta e'lon qilma.

## 29.13 Istisnolarni controller da umumiy ushlash va ma'lumotni oshkor qilish

Shikoyat qilinadigan kod:

```java
@PostMapping("/tolov")
public ResponseEntity<String> tolov(@RequestBody TolovSorovi s) {
    try {
        return ResponseEntity.ok(tolovServisi.bajar(s).id());
    } catch (Exception e) {
        // Shikoyat: umumiy catch va stack trace javobda
        return ResponseEntity.status(500).body(e.toString());
    }
}
```

Bu yerda `java:S2221` umumiy `Exception` ushlanayotganini aytadi, chunki shu blok `NullPointerException` ni ham biznes xatosi bilan birga yashiradi. Ikkinchi shikoyat ichki ma'lumotni javobga qo'yish, bu security hotspot: xato matni klass nomini, jadval nomini va ba'zan SQL ni oshkor qiladi.

Tuzatilgan kod:

```java
@RestControllerAdvice
class XatoIshlovchi {
    private static final Logger log = LoggerFactory.getLogger(XatoIshlovchi.class);

    @ExceptionHandler(QoldiqYetmadi.class)
    ResponseEntity<XatoJavobi> qoldiq(QoldiqYetmadi e) {
        return ResponseEntity.status(409).body(new XatoJavobi("QOLDIQ_YETMADI"));
    }

    @ExceptionHandler(Exception.class)
    ResponseEntity<XatoJavobi> kutilmagan(Exception e) {
        // Tafsilot faqat log ga, foydalanuvchiga neytral kod
        log.error("Kutilmagan xato", e);
        return ResponseEntity.status(500).body(new XatoJavobi("ICHKI_XATO"));
    }
}
```

Tavsiya: istisnoni `@RestControllerAdvice` da markazlashtir, tafsilotni log ga yoz va mijozga faqat barqaror xato kodini qaytar.

## 29.14 `RestTemplate` yoki `WebClient` ni timeout siz ishlatish

Shikoyat qilinadigan kod:

```java
@Bean
RestTemplate restTemplate() {
    // Shikoyat: timeout sozlanmagan
    return new RestTemplate();
}
```

Sonar bu holatda tashqi chaqiruv uchun timeout belgilanmaganini reliability muammosi sifatida ko'rsatadi, ba'zi profillarda u resurs boshqaruvi qoidalari bilan birga keladi. Standart `RestTemplate` da connect va read timeout cheksiz, demak sekin javob beradigan servis bizning thread larimizni band qiladi.

Tuzatilgan kod:

```java
@Bean
RestClient tolovMijozi(RestClient.Builder builder) {
    var sozlama = new SimpleClientHttpRequestFactory();
    // Ulanish va o'qish uchun aniq chegara
    sozlama.setConnectTimeout(Duration.ofSeconds(2));
    sozlama.setReadTimeout(Duration.ofSeconds(5));
    return builder.requestFactory(sozlama)
            .baseUrl("https://tolov.internal")
            .build();
}
```

Tavsiya: har bir HTTP mijoziga connect va read timeout ni aniq qiymat bilan belgila va uni konfiguratsiyadan boshqar.

## 29.15 Oddiy yondashuv va arxitektor yondashuvi

| Holat | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Field injection shikoyati | Qoidani profil dan o'chirish | Konstruktor injection ni ArchUnit testi bilan majburlash |
| Singleton holati | `synchronized` qo'shish | Holatni metod lokaliga ko'chirish, bean stateless qolishi |
| Controller murakkabligi | Metodni ikkiga bo'lish | Qarorni domen servisiga ko'chirish va unit test bilan yopish |
| Entity API da | `@JsonIgnore` qo'shish | Har bir endpoint uchun alohida javob `record` i |
| Cheklovsiz `findAll` | Qo'lda `limit` qo'shish | `Pageable` ni shartnomaga kiritish va max hajmni cheklash |
| Native query | Qiymatni `replace` bilan tozalash | Nomli parametr va identifikator uchun ruxsat ro'yxati |
| Ochiq parol | `.gitignore` ga fayl qo'shish | Secret store, kalit rotatsiyasi va CI da secrets tahlili |
| Umumiy `catch` | `Exception` o'rniga `Throwable` yozish | Aniq istisno ierarxiyasi va markazlashgan `@RestControllerAdvice` |

## 29.16 Tuzoq va yechim

| Tuzoq | Nega yuzaga keladi | Yechim |
|---|---|---|
| Shikoyat `Won't fix` bilan yopiladi | Tuzatish vaqt talab qiladi | Faqat haqiqiy false positive ga `Won't fix`, qolganiga issue |
| Qoida profil dan o'chiriladi | Bitta klass noqulaylik tug'diradi | Qoidani saqlab, faqat generatsiya qilingan kodni exclusion ga qo'y |
| Yangi kod uchun quality gate o'tadi, lekin eski kod chirik | Gate faqat new code ni o'lchaydi | Eski kodga alohida texnik qarz backlog i |
| Security hotspot e'tiborsiz qoladi | U gate ni har doim buzmaydi | Har bir hotspot ni review qilib, sabab bilan yop |
| Timeout qo'shilgach test sekinlashadi | Timeout qiymati testda ham ishlaydi | Test profilida kichik timeout, WireMock bilan kechikishni simulyatsiya qil |

Generatsiya qilingan yoki migratsiya kodini chiqarib tashlash kerak bo'lsa, buni qoidani o'chirmasdan `pom.xml` da aniq qil:

```xml
<properties>
  <!-- Faqat generatsiya qilingan klasslar tahlildan chiqariladi -->
  <sonar.exclusions>
    **/generated/**,**/*MapperImpl.java
  </sonar.exclusions>
  <!-- Entity larda coverage o'lchanmasin, mantiq yo'q -->
  <sonar.coverage.exclusions>
    **/domain/*Entity.java
  </sonar.coverage.exclusions>
</properties>
```

Tahlilni lokal yurgizib, natijani gate bo'yicha tekshir:

```bash
# Avval test va coverage, keyin tahlil
./mvnw clean verify
./mvnw sonar:sonar \
  -Dsonar.projectKey=buyurtma-servisi \
  -Dsonar.host.url="$SONAR_HOST_URL" \
  -Dsonar.token="$SONAR_TOKEN"
# Natijani gate bo'yicha tekshirish
curl -s -u "$SONAR_TOKEN": \
  "$SONAR_HOST_URL/api/qualitygates/project_status?projectKey=buyurtma-servisi"
```

## 29.17 Amalda qo'llash

- [ ] Loyihadagi barcha maydon `@Autowired` larni konstruktor injection ga ko'chir va shu qoidani ArchUnit testi bilan muhrla.
- [ ] Har bir `@Service` klassini ko'rib chiq va `final` bo'lmagan holat maydonlarini metod lokaliga ko'chir.
- [ ] `@Transactional` ni `grep` bilan topib, `private` yoki ichki chaqiriladigan metoddagi har bir holatni tuzat.
- [ ] Barcha `FetchType.EAGER` ni `LAZY` ga o'zgartir va kerakli joyga `@EntityGraph` qo'sh.
- [ ] Tashqariga chiqadigan har bir ro'yxat metodiga `Pageable` kirit va `max-page-size` ni konfiguratsiyada chekla.
- [ ] Native query larni ko'rib chiq, qiymatlarni nomli parametrga, `ORDER BY` ni ruxsat ro'yxatiga o'tkaz.
- [ ] Konfiguratsiya va `@Value` dagi har bir credential ni muhit o'zgaruvchisiga ko'chir, keyin kalitlarni rotatsiya qil.
- [ ] Har bir HTTP mijoziga connect va read timeout belgilab, test profilida kichik qiymat bilan tekshir.

---

[&larr; 28. Xato katalogi: maintainability, nomlash, o'lik kod va uslub](28-xato-katalogi-maintainability-nomlash-olik.md) · [Mundarija](README.md) · [30. Xato katalogi: test kodidagi xatolar &rarr;](30-xato-katalogi-test-kodidagi-xatolar.md)
