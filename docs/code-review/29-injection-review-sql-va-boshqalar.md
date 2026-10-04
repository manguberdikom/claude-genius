<!-- doc: code-review | chapter: 29 | part: VI. Xavfsizlik review -->

[Kod review](../../README.md) / [Kod review](README.md)

# 29. Injection review: SQL va boshqalar (Injection)

<details>
<summary>Bu bobdagi 10 bo'lim</summary>

- [29.1 Parametrlashtirish: nima parametr bo'la oladi](#291-parametrlashtirish-nima-parametr-bola-oladi)
- [29.2 Spring Data da injection yo'llari](#292-spring-data-da-injection-yollari)
- [29.3 JdbcTemplate va JdbcClient](#293-jdbctemplate-va-jdbcclient)
- [29.4 Ikkilamchi injection (second-order)](#294-ikkilamchi-injection-second-order)
- [29.5 SQL dan tashqari injection sinflari](#295-sql-dan-tashqari-injection-sinflari)
- [29.6 Shablon va hisobot injectionlari](#296-shablon-va-hisobot-injectionlari)
- [29.7 Review paytida injection ni qidirish](#297-review-paytida-injection-ni-qidirish)
- [29.8 Himoyani test bilan qulflash](#298-himoyani-test-bilan-qulflash)
- [29.9 Review checklisti: injection](#299-review-checklisti-injection)
- [29.10 Amalda qo'llash](#2910-amalda-qollash)

</details>


SQL injection eng qadimgi zaiflik sinfi, lekin u hali ham topiladi - chunki parametrlashtirish qoidasi bir joyda buzilsa yetarli. Spring va JPA ko'p holatda himoya beradi, lekin ularda ham teshiklar bor: so'rovning strukturaviy qismi (ustun nomi, tartib, jadval) parametr bo'la olmaydi, va aynan shu yerda xatolar to'planadi. Bu bob SQL injection ning Java/Spring dagi hamma yo'lini va qolgan injection sinflarini ko'radi.

## 29.1 Parametrlashtirish: nima parametr bo'la oladi

Bu farqni tushunmaslik barcha SQL injection larning sababi.

| So'rov qismi | Parametr bo'la oladimi | Xavfsiz yo'l |
| --- | --- | --- |
| Qiymat (`WHERE id = ?`) | Ha | `?` yoki `:name` |
| Qiymatlar ro'yxati (`IN`) | Ha | `= ANY(?)` massiv yoki `IN (:ids)` |
| `LIKE` naqshi | Ha (qiymat sifatida) | Parametr + escape |
| `LIMIT`/`OFFSET` | Ha | Parametr yoki tekshirilgan butun son |
| Ustun nomi | Yo'q | Whitelist (enum) |
| Jadval nomi | Yo'q | Whitelist |
| `ORDER BY` ifodasi | Yo'q | Whitelist (enum) |
| `ASC`/`DESC` | Yo'q | Enum |
| Operator (`>`, `<`) | Yo'q | Enum |
| Sxema nomi | Yo'q | Whitelist |

```java
// Eng ko'p uchraydigan zaiflik: tartiblash va yo'nalish.
// Zaif:
String sql = "SELECT * FROM orders ORDER BY " + sortBy + " " + direction;

// Xavfsiz: ikkisi ham enum, foydalanuvchi qiymati kodga aylanadi.
public enum OrderSortColumn {
    CREATED_AT("o.created_at"), TOTAL("o.total"), NUMBER("o.number");
    private final String sql;
    OrderSortColumn(String sql) { this.sql = sql; }
    public String sql() { return sql; }
    public static OrderSortColumn of(String raw) {
        for (OrderSortColumn c : values()) {
            if (c.name().equalsIgnoreCase(raw)) return c;
        }
        return CREATED_AT;                      // xavfsiz standart
    }
}
public enum SortDirection { ASC, DESC;
    public static SortDirection of(String raw) {
        return "desc".equalsIgnoreCase(raw) ? DESC : ASC;
    }
}
// Ishlatilishi: tashqi satr hech qachon SQL ga tushmaydi.
String sql = "SELECT id, number, total FROM orders ORDER BY %s %s LIMIT :limit"
    .formatted(OrderSortColumn.of(sortBy).sql(), SortDirection.of(direction));
```

## 29.2 Spring Data da injection yo'llari

Spring Data xavfsiz deb hisoblanadi, lekin uchta teshigi bor.

```java
// Teshik 1: nativeQuery da konkatenatsiya (odatda SpEL yoki satr bilan).
@Query(value = "SELECT * FROM orders WHERE status = '?1'", nativeQuery = true)
List<Order> byStatus(String status);
// Diqqat: qo'shtirnoq ichidagi ?1 PARAMETR EMAS - u satr literali ichida
// va JDBC uni parametr deb ko'rmaydi. To'g'risi: qo'shtirnoqsiz `?1`.

// Teshik 2: SpEL ifodasi orqali qiymat qo'yish.
@Query(value = "SELECT * FROM #{#entityName} WHERE name = :#{#filter.name}",
       nativeQuery = true)
// SpEL natijasi SQL matniga QO'SHILADI, parametr sifatida emas -
// ya'ni bu injection yo'li. Parametrlar uchun oddiy `:name` ishlatiladi.

// Teshik 3: Sort va Pageable orqali.
repository.findAll(PageRequest.of(0, 20, Sort.by(userProvidedField)));
// Spring Data `Sort` da property nomini tekshiradi (entity maydonlari
// bilan solishtiradi) - shuning uchun bu nisbatan xavfsiz. LEKIN
// `JpaSort.unsafe(...)` tekshiruvni chetlab o'tadi:
Sort.by(JpaSort.unsafe("(SELECT ...)"));        // injection - nomi ham shuni aytadi
// Review qoidasi: `JpaSort.unsafe` loyihada taqiqlanadi.

// Xavfsiz shakl: ro'yxatlar uchun.
@Query("select o from Order o where o.status in :statuses")
List<Order> byStatuses(@Param("statuses") Collection<OrderStatus> statuses);
// PostgreSQL massiv bilan (ko'p elementda tezroq, reja barqaror):
@Query(value = "SELECT * FROM orders WHERE id = ANY(:ids)", nativeQuery = true)
List<Order> byIds(@Param("ids") UUID[] ids);
```

## 29.3 JdbcTemplate va JdbcClient

```java
// Zaif: queryForList satr bilan.
jdbc.queryForList("SELECT * FROM orders WHERE number = '" + number + "'");

// Xavfsiz: parametrlar.
jdbc.queryForList("SELECT * FROM orders WHERE number = ?", number);

// Spring 6.1+ JdbcClient: o'qiladigan va xavfsiz.
List<OrderRow> rows = jdbcClient
    .sql("""
         SELECT id, number, total FROM orders
          WHERE customer_id = :customerId
            AND created_at >= :from
          ORDER BY created_at DESC
          LIMIT :limit
         """)
    .param("customerId", customerId)
    .param("from", from)
    .param("limit", Math.min(limit, 100))
    .query(OrderRow.class)
    .list();

// LIKE bilan ishlash: foydalanuvchi kiritgan `%` va `_` ni escape qilish.
String pattern = search.replace("\\", "\\\\")
                       .replace("%", "\\%")
                       .replace("_", "\\_");
jdbc.queryForList("SELECT * FROM customer WHERE name LIKE ? ESCAPE '\\'",
                  "%" + pattern + "%");
// Escape qilinmasa: injection emas, lekin `%` bilan butun jadval
// skanerlanadi - DoS yo'li (31.8).
```

## 29.4 Ikkilamchi injection (second-order)

Eng ko'p e'tibordan chetda qoladigan shakl: ma'lumot avval bazaga xavfsiz yoziladi, keyin undan so'rov quriladi.

```java
// 1-qadam: foydalanuvchi "filtr" saqlaydi - parametr bilan, xavfsiz.
jdbc.update("INSERT INTO saved_filter (user_id, expr) VALUES (?, ?)", userId, expr);

// 2-qadam: saqlangan filtr so'rovga qo'shiladi - zaiflik shu yerda.
String expr = jdbc.queryForObject(
    "SELECT expr FROM saved_filter WHERE id = ?", String.class, filterId);
List<Map<String,Object>> rows = jdbc.queryForList(
    "SELECT * FROM orders WHERE " + expr);      // injection!

// Review qoidasi: bazadan kelgan qiymat ham ishonilmaydigan ma'lumot,
// agar u avval tashqaridan kelgan bo'lsa. Yechim: filtrni strukturaviy
// shaklda saqlash (JSON: maydon, operator, qiymat) va uni whitelist
// bo'yicha SQL ga aylantirish.
public record FilterCriterion(FilterField field, FilterOp op, String value) { }
// field va op - enum, value - parametr. Injection yo'li yo'q.
```

## 29.5 SQL dan tashqari injection sinflari

```java
// 1) Command injection: shell orqali bajarish.
Runtime.getRuntime().exec("convert " + fileName + " out.png");     // zaif
// Xavfsiz: shell yo'q, argumentlar massiv sifatida.
new ProcessBuilder("convert", fileName, "out.png").start();
// Lekin fileName hali ham tekshirilishi kerak: "-write" kabi flaglar
// bilan boshlangan nom ImageMagick uchun buyruqqa aylanadi.
if (!fileName.matches("[A-Za-z0-9._-]{1,100}")) throw new InvalidFileName();

// 2) SpEL injection: eng xavfli, chunki RCE beradi.
ExpressionParser parser = new SpelExpressionParser();
parser.parseExpression(userInput).getValue();                       // RCE!
// Review qoidasi: foydalanuvchi kiritgan SpEL hech qachon bajarilmaydi.
// @PreAuthorize ichida ham ehtiyot: @PreAuthorize("hasRole('" + role + "')")
// shaklidagi dinamik qurish xavfli.

// 3) Log injection va forging.
log.info("Foydalanuvchi kirdi: " + username);
// username = "admin\n2026-10-04 12:00:00 INFO Foydalanuvchi kirdi: root"
// Natija: logda yolg'on yozuv. JSON log formati bu muammoni yo'q qiladi.
log.info("Foydalanuvchi kirdi: {}", username);   // structured, xavfsizroq

// 4) Header injection (CRLF).
response.setHeader("X-Trace", userValue);        // \r\n bo'lsa yangi header
// Spring zamonaviy versiyalarida bu bloklangan, lekin qo'lda yozilgan
// javoblarda tekshirish kerak.

// 5) Open redirect.
return "redirect:" + request.getParameter("next");                  // zaif
// Xavfsiz: nisbiy yo'llar yoki whitelist.
if (!next.startsWith("/") || next.startsWith("//")) next = "/";

// 6) XSS: API da ham muhim.
// JSON javob odatda xavfsiz, LEKIN:
//  - `Content-Type: text/html` bilan qaytarilsa - XSS;
//  - frontend `innerHTML` ga qo'ysa - XSS;
//  - PDF yoki email shabloniga qo'shilsa - shablon injection.
// Review savoli: bu qiymat qayerda ko'rsatiladi va u yerda escape qilinadimi?
```

## 29.6 Shablon va hisobot injectionlari

```java
// Thymeleaf: ifoda injectioni mumkin.
// Zaif: shablon nomi foydalanuvchidan.
return "redirect:" + page;                       // yoki
return userProvidedTemplateName;                 // SSTI yo'li
// Review qoidasi: shablon nomi faqat kod ichidagi konstantalardan.

// Thymeleaf da matn chiqarish:
// th:text  - escape qiladi (xavfsiz)
// th:utext - escape QILMAYDI (xavfli, faqat ishonchli HTML uchun)
// Review da har `th:utext` uchun savol: bu kontent qayerdan keladi?

// CSV injection (formula injection): Excel da ochilganda bajariladi.
// Foydalanuvchi ismi "=cmd|'/c calc'!A1" bo'lsa, eksport qilingan CSV
// Excel da ochilganda buyruq bajarilishi mumkin.
static String csvSafe(String value) {
    if (value == null) return "";
    // =, +, -, @, tab, CR bilan boshlangan qiymatni neytrallash.
    if (value.matches("^[=+\\-@\\t\\r].*")) return "'" + value;
    return value;
}
```

## 29.7 Review paytida injection ni qidirish

```bash
# Injection xavfini tizimli qidirish.
SRC=src/main/java

echo "=== SQL satr qurish ==="
grep -rnE '("(SELECT|INSERT|UPDATE|DELETE|WHERE|ORDER BY|FROM)[^"]*"\s*\+|\+\s*"\s*(WHERE|AND|OR|ORDER))' $SRC

echo "=== formatted va String.format bilan SQL ==="
grep -rnE '(SELECT|UPDATE|DELETE|INSERT)[^;]*(\.formatted\(|String\.format\()' $SRC

echo "=== nativeQuery va createNativeQuery ==="
grep -rnE 'nativeQuery\s*=\s*true|createNativeQuery\(|createQuery\(' $SRC

echo "=== JpaSort.unsafe - har doim taqiqlanadi ==="
grep -rn 'JpaSort.unsafe' $SRC

echo "=== SpEL va ifoda bajarish ==="
grep -rnE 'SpelExpressionParser|parseExpression|ExpressionParser|ScriptEngine' $SRC

echo "=== buyruq bajarish ==="
grep -rnE 'Runtime\.getRuntime\(\)\.exec|new ProcessBuilder' $SRC

echo "=== th:utext (escape qilinmagan HTML) ==="
grep -rn 'th:utext' src/main/resources/templates 2>/dev/null

echo "=== ORDER BY ga o'zgaruvchi ==="
grep -rnE 'ORDER BY"\s*\+|append\("ORDER BY"\)' $SRC
```

## 29.8 Himoyani test bilan qulflash

```java
// Injection himoyasini test bilan tasdiqlash: review izohidan ko'ra ishonchli.
@ParameterizedTest
@ValueSource(strings = {
    "created_at; DROP TABLE orders",
    "(SELECT password_hash FROM app_user LIMIT 1)",
    "1 UNION SELECT NULL, password_hash, NULL FROM app_user",
    "created_at/**/DESC,(SELECT 1)",
    "../../etc/passwd"
})
void malformedSortIsRejectedOrIgnored(String evilSort) {
    // Natija: xato yoki standart tartib. Hech qanday holatda ham
    // so'rov bajarilmasligi va ma'lumot chiqmasligi kerak.
    assertThatCode(() -> service.list(evilSort))
        .doesNotThrowAnyException();
    assertThat(service.list(evilSort))
        .as("standart tartibga tushishi kerak")
        .isEqualTo(service.list("created_at"));
}

// Injection himoyasi arxitektura testi bilan: yangi joyda takrorlanmasligi.
@ArchTest
static final ArchRule no_string_concatenation_in_queries =
    noClasses().should().callMethodWhere(
        JavaCall.Predicates.target(nameMatching("createNativeQuery")))
        .because("native so'rovlar faqat repository qatlamida va parametrlar bilan");
```

## 29.9 Review checklisti: injection

| Savol | Nega |
| --- | --- |
| SQL satr konkatenatsiyasi bormi | Injection |
| `ORDER BY`, ustun, jadval nomi whitelist dami | Parametr bo'la olmaydi |
| `nativeQuery` da parametrlar to'g'ri ishlatilganmi | Qo'shtirnoq ichidagi `?1` parametr emas |
| `JpaSort.unsafe` ishlatilmaganmi | Tekshiruvni chetlab o'tish |
| SpEL yoki skript foydalanuvchi kirishi bilan bajarilmaydimi | RCE |
| `exec` shell orqali chaqirilmaydimi | Command injection |
| `LIKE` naqshi escape qilinganmi | DoS va kutilmagan natija |
| Bazadan kelgan qiymat so'rovga qo'shilmaydimi | Ikkilamchi injection |
| `th:utext` va HTML chiqarish xavfsizmi | XSS |
| CSV eksportda formula neytrallanganmi | CSV injection |
| Redirect manzili tekshirilganmi | Open redirect |
| Himoya test bilan qulflangangmi | Regressiya |

## 29.10 Amalda qo'llash

- [ ] Injection qidiruv skriptini ishga tushirib, topilgan har bir joy uchun kirish manbasini kuzatib chiqing.
- [ ] Barcha dinamik tartiblash joylarini enum whitelist ga o'tkazing.
- [ ] `JpaSort.unsafe` ni ArchUnit yoki Semgrep qoidasi bilan taqiqlang.
- [ ] `nativeQuery` ishlatilgan barcha so'rovlarda parametrlar qo'shtirnoq ichida emasligini tekshiring.
- [ ] `LIKE` ishlatadigan qidiruvlarda escape va minimal uzunlik talabini qo'shing.
- [ ] Saqlanadigan filtr yoki ifoda bo'lsa, uni strukturaviy shaklga (enum + parametr) o'tkazing.
- [ ] CSV va Excel eksportida formula neytrallash funksiyasini qo'shing.
- [ ] Injection himoyasi uchun parametrlashtirilgan testni yozib, zararli kirish namunalarini CI ga kiriting.

---

[&larr; 28. Xavfsizlik review metodikasi](28-xavfsizlik-review-metodikasi.md) · [Mundarija](README.md) · [30. Autentifikatsiya va avtorizatsiya review &rarr;](30-autentifikatsiya-va-avtorizatsiya-review.md)
