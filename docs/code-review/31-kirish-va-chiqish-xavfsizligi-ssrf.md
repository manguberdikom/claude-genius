<!-- doc: code-review | chapter: 31 | part: VI. Xavfsizlik review -->

[Kod review](../../README.md) / [Kod review](README.md)

# 31. Kirish va chiqish xavfsizligi: SSRF, deserializatsiya, fayllar (Input and Output Safety)

<details>
<summary>Bu bobdagi 8 bo'lim</summary>

- [31.1 SSRF: URL ni kirishdan qurish](#311-ssrf-url-ni-kirishdan-qurish)
- [31.2 Deserializatsiya](#312-deserializatsiya)
- [31.3 Fayl yo'li va arxivlar](#313-fayl-yoli-va-arxivlar)
- [31.4 Rasm va hujjat qayta ishlash](#314-rasm-va-hujjat-qayta-ishlash)
- [31.5 Regex va DoS (ReDoS)](#315-regex-va-dos-redos)
- [31.6 Resurs charchatish (DoS) yo'llari](#316-resurs-charchatish-dos-yollari)
- [31.7 Review checklisti: kirish va chiqish](#317-review-checklisti-kirish-va-chiqish)
- [31.8 Amalda qo'llash](#318-amalda-qollash)

</details>


Bu bob tashqi dunyo bilan aloqa qiladigan qolgan yo'llarni oladi: tizim boshqa manzilga so'rov yuborganda, baytlarni obyektga aylantirganda va fayl bilan ishlaganda. Har uchida umumiy xato bor - tashqi ma'lumotning strukturaviy qismiga ishonish.

## 31.1 SSRF: URL ni kirishdan qurish

```java
// Zaiflik: foydalanuvchi bergan URL ga so'rov yuborish.
@PostMapping("/import")
public ImportResult importFrom(@RequestParam String url) {
    String body = restClient.get().uri(url).retrieve().body(String.class);
    return parse(body);
}
// Hujumchi quyidagilarni so'raydi:
//   http://169.254.169.254/latest/meta-data/iam/...  (cloud metadata, kalitlar)
//   http://localhost:9090/actuator/env                (ichki actuator)
//   http://postgres:5432                              (ichki servislar skanerlash)
//   file:///etc/passwd                                (fayl o'qish)
//   http://internal-admin.svc.cluster.local/          (ichki tarmoq)
```

```java
// Himoya: whitelist birinchi tanlov, blacklist ikkinchi.
@Component
public class SafeUrlResolver {

    private final Set<String> allowedHosts;      // konfiguratsiyadan

    public URI validate(String raw) {
        URI uri = URI.create(raw);

        // 1) Faqat https (yoki http, agar kerak bo'lsa). file:, gopher:, ftp: yo'q.
        if (!"https".equalsIgnoreCase(uri.getScheme())) {
            throw new UnsafeUrl("faqat https ruxsat etilgan");
        }
        // 2) Host whitelist da bo'lishi kerak.
        if (!allowedHosts.contains(uri.getHost())) {
            throw new UnsafeUrl("ruxsat etilmagan host: " + uri.getHost());
        }
        // 3) DNS ni hal qilib, IP ni tekshirish (DNS rebinding dan himoya
        //    to'liq emas, lekin oddiy hujumlarni to'xtatadi).
        for (InetAddress addr : InetAddress.getAllByName(uri.getHost())) {
            if (addr.isLoopbackAddress() || addr.isSiteLocalAddress()
                || addr.isLinkLocalAddress() || addr.isAnyLocalAddress()) {
                throw new UnsafeUrl("ichki manzil: " + addr);
            }
        }
        return uri;
    }
}
// Qo'shimcha himoyalar (review da so'raladi):
// - redirect larni kuzatmaslik yoki ularni ham tekshirish;
// - chiqish trafigi uchun alohida proksi va tarmoq siyosati (eng ishonchli);
// - javob hajmi va timeout chegarasi;
// - metadata servisiga kirishni infratuzilma darajasida bloklash.
```

```java
// Redirect: eng ko'p o'tkazib yuboriladigan nuqta.
// Hujumchi ruxsat etilgan hostdan 302 bilan ichki manzilga yo'naltiradi.
HttpClient client = HttpClient.newBuilder()
    .followRedirects(HttpClient.Redirect.NEVER)       // review talabi
    .connectTimeout(Duration.ofSeconds(2))
    .build();
```

## 31.2 Deserializatsiya

```java
// Eng xavfli: Java native deserializatsiya ishonilmaydigan ma'lumotdan.
ObjectInputStream in = new ObjectInputStream(request.getInputStream());
Object obj = in.readObject();                    // RCE yo'li
// Review qoidasi: `readObject` ishonilmaydigan ma'lumot bilan hech qachon.
// Agar meros kod shunday ishlatsa: ObjectInputFilter bilan cheklash
// (JDK 9+) yoki butunlay JSON ga o'tish.
ObjectInputFilter filter = ObjectInputFilter.Config.createFilter(
    "com.acme.dto.*;java.util.*;!*");            // whitelist, qolgani rad etiladi
in.setObjectInputFilter(filter);

// Jackson: polimorfik deserializatsiya xavfi.
ObjectMapper mapper = new ObjectMapper();
mapper.enableDefaultTyping();                    // taqiqlanadi (eski API)
mapper.activateDefaultTyping(LaissezFaireSubTypeValidator.instance);   // xavfli
// Hujumchi JSON ga `"@class": "..."` qo'yib, gadget zanjirini ishga tushiradi.

// Xavfsiz polimorfizm: aniq ro'yxat bilan.
@JsonTypeInfo(use = Id.NAME, include = As.PROPERTY, property = "type")
@JsonSubTypes({
    @JsonSubTypes.Type(value = CardPayment.class, name = "CARD"),
    @JsonSubTypes.Type(value = WalletPayment.class, name = "WALLET")
})
public sealed interface PaymentMethod { }
// Faqat sanab o'tilgan turlar yaratiladi. `sealed` bilan birga -
// kompilyator ham to'liqlikni tekshiradi.

// XML: XXE himoyasi.
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
dbf.setFeature("http://xml.org/sax/features/external-general-entities", false);
dbf.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
dbf.setXIncludeAware(false);
dbf.setExpandEntityReferences(false);
// Review qoidasi: har bir XML parser yaratilgan joyda shu sozlamalar bo'lishi
// kerak - standart holatda XXE mumkin.

// YAML: SnakeYAML da ham deserializatsiya xavfi bor.
Yaml yaml = new Yaml(new SafeConstructor(new LoaderOptions()));   // ixtiyoriy turlar yo'q
```

## 31.3 Fayl yo'li va arxivlar

```java
// Path traversal: fayl nomi kirishdan.
@GetMapping("/files/{name}")
public Resource download(@PathVariable String name) {
    return new FileSystemResource("/var/data/" + name);   // ../../etc/passwd
}

// Himoya: yo'lni normalizatsiya qilib, baza katalog ichida ekanini tekshirish.
private static final Path BASE = Paths.get("/var/data").toAbsolutePath().normalize();

public Resource download(String name) {
    Path target = BASE.resolve(name).normalize();
    if (!target.startsWith(BASE)) {               // majburiy tekshiruv
        throw new InvalidPath(name);
    }
    if (!Files.isRegularFile(target)) throw new FileNotFound(name);
    return new FileSystemResource(target);
}
// Yana yaxshiroq: fayl nomini foydalanuvchi bermasligi - ID bo'yicha
// bazadan haqiqiy nomni olish (20.7).

// Zip slip: arxiv ichidagi yo'l `../` bo'lishi mumkin.
try (ZipInputStream zis = new ZipInputStream(input)) {
    ZipEntry entry;
    long totalSize = 0;
    int entryCount = 0;
    while ((entry = zis.getNextEntry()) != null) {
        // 1) Yo'l tekshiruvi (zip slip).
        Path out = BASE.resolve(entry.getName()).normalize();
        if (!out.startsWith(BASE)) throw new InvalidArchive(entry.getName());
        // 2) Zip bomba himoyasi: hajm va element soni chegarasi.
        if (++entryCount > 1_000) throw new InvalidArchive("juda ko'p element");
        totalSize += entry.getSize() < 0 ? 0 : entry.getSize();
        if (totalSize > 100L * 1024 * 1024) throw new InvalidArchive("juda katta");
        // 3) Symlink va katalog e'tibor bilan.
        if (entry.isDirectory()) { Files.createDirectories(out); continue; }
        Files.copy(zis, out, StandardCopyOption.REPLACE_EXISTING);
    }
}
// Diqqat: entry.getSize() arxiv metadata sidan keladi va yolg'on bo'lishi
// mumkin - haqiqiy hajmni o'qish paytida ham cheklash kerak (BoundedInputStream).
```

## 31.4 Rasm va hujjat qayta ishlash

```java
// Tashqi fayl bilan ishlaydigan kutubxonalar - alohida xavf manbasi.
// ImageMagick, Ghostscript, LibreOffice tarixan RCE zaifliklariga ega.
// Review savollari:
// 1) Fayl sandbox da (alohida konteyner, cheklangan huquq) qayta ishlanadimi?
// 2) Kutubxona versiyasi yangilanadimi ([33-bob](33-bogliqlik-va-supply-chain-review.md))?
// 3) Hajm, o'lcham va vaqt chegarasi bormi?
// 4) Rasm o'lchami tekshiriladimi (decompression bomba)?

// Rasm o'lchamini ochmasdan tekshirish: "piksel bombasi" dan himoya.
try (ImageInputStream iis = ImageIO.createImageInputStream(file)) {
    Iterator<ImageReader> readers = ImageIO.getImageReaders(iis);
    if (!readers.hasNext()) throw new UnsupportedFileType("rasm emas");
    ImageReader reader = readers.next();
    reader.setInput(iis);
    int w = reader.getWidth(0), h = reader.getHeight(0);
    // 10 000 x 10 000 rasm = 400 MB xotira (4 bayt/piksel).
    if ((long) w * h > 50_000_000L) throw new ImageTooLarge(w, h);
}
```

## 31.5 Regex va DoS (ReDoS)

```java
// Katastrofik backtracking: kichik kirish, cheksiz vaqt.
Pattern.compile("^(a+)+$").matcher("aaaaaaaaaaaaaaaaaaaaaaaaaaaaX").matches();
// Bu kod minutlarga cho'ziladi va CPU ni to'liq egallaydi.

// Xavfli naqshlar: ichma-ich kvantifikatorlar `(a+)+`, `(a|a)*`,
// va kirish uzunligi cheklanmagan `.*` zanjirlari.
// Review qoidasi: (1) foydalanuvchi regex bermasligi kerak;
// (2) kirish uzunligi oldin cheklanadi; (3) murakkab validatsiya uchun
// regex o'rniga parser.

// Email validatsiyasi: murakkab regex o'rniga oddiy tekshiruv.
// Zaif: internetdan olingan "to'liq RFC 5322" regex - ReDoS manbasi.
// Yaxshi: oddiy shakl tekshiruvi + haqiqiy tasdiqlash (email yuborish).
private static final Pattern EMAIL = Pattern.compile("^[^@\\s]{1,64}@[^@\\s]{1,255}$");

// Kirish uzunligini oldin cheklash - eng oddiy va eng samarali himoya.
if (input.length() > 256) throw new InputTooLong();
```

## 31.6 Resurs charchatish (DoS) yo'llari

| Yo'l | Himoya |
| --- | --- |
| Katta so'rov tanasi | `max-http-request-header-size`, multipart chegaralari |
| Chuqur JSON | `StreamReadConstraints` (20.8) |
| Katta massiv parametri | `@Size(max = ...)` |
| Chegarasiz `size` parametri | `@Max(100)` |
| ReDoS | Kirish uzunligi, oddiy regex |
| Zip/rasm bombasi | Hajm va o'lcham chegarasi |
| Ko'p parallel so'rov | Rate limit, bulkhead |
| Sekin mijoz (slowloris) | Ulanish timeout i, reverse proxy |
| Qimmat so'rov (hisobot) | Navbat, kesh, rate limit |
| Log to'lishi | Log darajasi, rate limit, disk alert |

```java
// Rate limit: review da so'raladigan minimal himoya.
// Bucket4j bilan, foydalanuvchi va IP bo'yicha.
@Component
public class RateLimitFilter extends OncePerRequestFilter {

    private final Cache<String, Bucket> buckets = Caffeine.newBuilder()
        .maximumSize(100_000)                           // kesh ham chegaralangan
        .expireAfterAccess(Duration.ofMinutes(10))
        .build();

    @Override
    protected void doFilterInternal(HttpServletRequest req, HttpServletResponse res,
                                    FilterChain chain) throws IOException, ServletException {
        String key = keyFor(req);                       // user ID yoki IP
        Bucket bucket = buckets.get(key, k -> Bucket.builder()
            .addLimit(limit -> limit.capacity(100).refillGreedy(100, Duration.ofMinutes(1)))
            .build());
        if (!bucket.tryConsume(1)) {
            res.setStatus(429);
            res.setHeader("Retry-After", "60");
            return;
        }
        chain.doFilter(req, res);
    }
}
// Review savollari: kalit nima (IP proksi ortida ishonchli emas),
// chegara qanday tanlangan, va qimmat endpointlar uchun alohida
// (qattiqroq) chegara bormi.
```

## 31.7 Review checklisti: kirish va chiqish

| Savol | Nega |
| --- | --- |
| Tashqi URL ga so'rov bormi, whitelist bormi | SSRF |
| Redirect kuzatilmaydimi | SSRF chetlab o'tish |
| `readObject` ishonilmaydigan ma'lumot bilan ishlatilmaydimi | RCE |
| Jackson polimorfizmi aniq ro'yxat bilanmi | Deserializatsiya hujumi |
| XML parser XXE dan himoyalanganmi | Fayl o'qish, SSRF |
| Fayl yo'li normalizatsiya qilinib tekshiriladimi | Path traversal |
| Arxiv ichidagi yo'l va hajm tekshiriladimi | Zip slip, zip bomba |
| Rasm o'lchami ochishdan oldin tekshiriladimi | Xotira charchatish |
| Regex da ichma-ich kvantifikator yo'qmi | ReDoS |
| Kirish uzunligi cheklanganmi | DoS |
| Rate limit bormi | Zo'ravonlik va bo'ron |
| Tashqi jarayon sandbox dami | RCE ta'sirini cheklash |

## 31.8 Amalda qo'llash

- [ ] Tashqi URL ga so'rov yuboradigan barcha joylarni toping va ularga whitelist, sxema va IP tekshiruvini qo'shing.
- [ ] HTTP mijozlarda `followRedirects` ni o'chiring yoki redirect manzilini ham tekshiring.
- [ ] `ObjectInputStream` ishlatilgan joylarni toping va ularni JSON ga o'tkazish yoki `ObjectInputFilter` qo'shish rejasini tuzing.
- [ ] `activateDefaultTyping` va `enableDefaultTyping` ishlatilgan joylarni butunlay olib tashlang.
- [ ] Barcha XML parser yaratilgan joylarga XXE himoyasini qo'shing va buni yordamchi fabrika metodiga yig'ing.
- [ ] Fayl yo'li quruvchi kodni `normalize()` + `startsWith(BASE)` tekshiruvi bilan himoyalang.
- [ ] Arxiv ochadigan kodga element soni, umumiy hajm va yo'l tekshiruvini qo'shing.
- [ ] Loyihadagi regex larni ko'rib chiqib, ichma-ich kvantifikatorli naqshlarni toping va kirish uzunligini cheklang.
- [ ] Qimmat endpointlar (hisobot, eksport, qidiruv) uchun alohida rate limit qo'ying.

---

[&larr; 30. Autentifikatsiya va avtorizatsiya review](30-autentifikatsiya-va-avtorizatsiya-review.md) · [Mundarija](README.md) · [32. Secret, maxfiy ma'lumot va kriptografiya review &rarr;](32-secret-maxfiy-malumot-va-kriptografiya.md)
