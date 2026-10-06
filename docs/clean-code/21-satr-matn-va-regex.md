<!-- doc: clean-code | chapter: 21 | part: VII. Java tilining toza ishlatilishi -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 21. Satr, matn va regex (Strings, Text and Regex)

<details>
<summary>Bu bobdagi 10 bo'lim</summary>

- [21.1 `==` emas `equals`, `intern` va literal pool](#211--emas-equals-intern-va-literal-pool)
- [21.2 Birlashtirish: `+`, `StringBuilder`, `String.join`, `formatted`](#212-birlashtirish--stringbuilder-stringjoin-formatted)
- [21.3 Kodirovka va `Charset` ni oshkor berish](#213-kodirovka-va-charset-ni-oshkor-berish)
- [21.4 `toLowerCase`, `format` va `Locale` tuzog'i](#214-tolowercase-format-va-locale-tuzogi)
- [21.5 `split`, `trim`, `strip`, `isBlank` farqlari](#215-split-trim-strip-isblank-farqlari)
- [21.6 Regexni oldindan kompilyatsiya qilish va nomlash](#216-regexni-oldindan-kompilyatsiya-qilish-va-nomlash)
- [21.7 Katastrofik backtracking va kiritish uzunligi](#217-katastrofik-backtracking-va-kiritish-uzunligi)
- [21.8 Satr bilan tiplash o'rniga tur](#218-satr-bilan-tiplash-orniga-tur)
- [21.9 Matn blokida SQL va JSON](#219-matn-blokida-sql-va-json)
- [21.10 Amalda qo'llash](#2110-amalda-qollash)

</details>


Satr Java da eng ko'p ishlatiladigan tur va shu sababli eng ko'p yashirin xato manbasi: kodirovka, locale, `==` solishtirish, regex narxi. Bu bobda shu xatolarning hammasini to'sadigan qoidalar. Satr bilan tiplash (stringly typed) anti-patterni [patternlar hujjatidagi](../patterns/README.md) satr bilan tiplash anti-patternida.

## 21.1 `==` emas `equals`, `intern` va literal pool

`==` satrlar uchun havolani solishtiradi. Literal satrlar pool da saqlanadi, shuning uchun `"a" == "a"` → `true`, lekin ish vaqtida qurilgan satrlar uchun `false`. Natija: kod testda ishlaydi, production da ishlamaydi.

```java
// yomon: foydalanuvchi kiritgan satr bilan ishlamaydi
if (status == "SETTLED") { ... }

// yaxshi
if ("SETTLED".equals(status)) { ... }              // null-xavfsiz tartib
if (Objects.equals(status, expected)) { ... }

// eng yaxshi: satr emas, enum (25.27)
if (payment.status() == SettlementStatus.SETTLED) { ... }
```

`String.intern()` ni qo'lda ishlatish deyarli hech qachon kerak emas: u xotirani tejaydi, lekin JVM ichki pool ini to'ldiradi va `==` ga asoslangan xavfli kodni rag'batlantiradi.

## 21.2 Birlashtirish: `+`, `StringBuilder`, `String.join`, `formatted`

Har bir usulning o'z o'rni bor va noto'g'ri tanlov yo o'qilishni, yo tezlikni buzadi.

| Vaziyat | To'g'ri usul |
|---|---|
| Bir-ikki qism, bir marta | `+` (kompilyator optimizatsiya qiladi) |
| Siklda yig'ish | `StringBuilder` |
| Ro'yxatni ajratgich bilan birlashtirish | `String.join` yoki `Collectors.joining` |
| Shablon bo'yicha formatlash | `"...".formatted(...)` yoki `String.format` |
| Ko'p qatorli matn (SQL, JSON) | matn bloki `"""` (12.9) |
| Log xabari | SLF4J `{}` placeholder (29.1) |
| Istisno xabari | `.formatted(...)` |

```java
// yomon: siklda + - har iteratsiyada yangi String
String csv = "";
for (Sku sku : skus) { csv += sku.code() + ","; }

// yaxshi
String csv = skus.stream().map(Sku::code).collect(joining(","));

// yomon: log'da birlashtirish - daraja o'chirilgan bo'lsa ham bajariladi
log.debug("to'lov " + paymentId + " yopildi " + settledAt);

// yaxshi
log.debug("to'lov {} yopildi {}", paymentId, settledAt);
```

## 21.3 Kodirovka va `Charset` ni oshkor berish

`new String(bytes)`, `String.getBytes()`, `new FileReader(file)` platformaning standart kodirovkasini ishlatadi. Bu mahalliy mashinada UTF-8, serverda boshqa bo'lishi mumkin va natijada kirill yoki o'zbek harflari buziladi. Java 18 dan beri standart UTF-8, lekin eski kod va eski JVM lar uchun oshkor berish qoidasi qoladi.

```java
// yomon: platformaga bog'liq
String content = new String(Files.readAllBytes(path));
byte[] bytes = text.getBytes();

// yaxshi: har doim oshkor
String content = Files.readString(path, StandardCharsets.UTF_8);
byte[] bytes = text.getBytes(StandardCharsets.UTF_8);
```

Shu qoida build va runtime sozlamalariga ham tegishli: `pom.xml` da `project.build.sourceEncoding=UTF-8`, Docker da `LANG=C.UTF-8`, JVM da `-Dfile.encoding=UTF-8`.

## 21.4 `toLowerCase`, `format` va `Locale` tuzog'i

`toLowerCase()` va `toUpperCase()` locale ga bog'liq. Turk tilida `"I".toLowerCase()` → `"ı"` (nuqtasiz), va natijada `"ID".toLowerCase().equals("id")` → `false`. Bu xato turk serverida ishga tushgan ilovada haqiqatan uchraydi.

```java
// yomon: locale ga bog'liq
if (header.toLowerCase().equals("content-type")) { ... }
String formatted = String.format("%.2f", amount);     // kasr ajratgichi locale ga bog'liq

// yaxshi: texnik solishtirish uchun ROOT
if (header.toLowerCase(Locale.ROOT).equals("content-type")) { ... }
if (header.equalsIgnoreCase("content-type")) { ... }   // yana soddaroq

// yaxshi: mashina uchun ROOT, foydalanuvchi uchun uning locale i
String forLog = String.format(Locale.ROOT, "%.2f", amount);
String forUser = NumberFormat.getCurrencyInstance(userLocale).format(amount);
```

Qoida: **mashina** uchun `Locale.ROOT`, **foydalanuvchi** uchun uning locale i. Locale ni tashlab ketish eng yomon variant.

## 21.5 `split`, `trim`, `strip`, `isBlank` farqlari

Bu metodlarning o'xshash nomlari ortida boshqacha xatti-harakat turadi.

| Metod | Nima qiladi | Tuzoq |
|---|---|---|
| `trim()` | `<= U+0020` belgilarni olib tashlaydi | Unicode bo'shliqlarni ko'rmaydi |
| `strip()` | Unicode bo'shliqlarni olib tashlaydi | Java 11+ |
| `isEmpty()` | uzunlik 0 | `" "` uchun `false` |
| `isBlank()` | bo'sh yoki faqat bo'shliq | Java 11+ |
| `split(regex)` | **regex** qabul qiladi | `split(".")` hamma narsani bo'ladi |
| `split(regex, -1)` | oxirgi bo'sh qismlarni saqlaydi | standart shakl ularni tashlaydi |
| `replaceAll` | regex | `replace` literal ishlatadi |
| `matches` | **butun** satrni tekshiradi | qisman moslik uchun `find()` |

```java
// yomon: nuqta regex da "har qanday belgi"
String[] parts = version.split(".");        // bo'sh massiv!
// yaxshi
String[] parts = version.split("\\.");
String[] parts = version.split(Pattern.quote("."));

// yomon: oxirgi bo'sh ustunlar yo'qoladi - CSV da ustun soni o'zgaradi
String[] columns = line.split(",");         // "a,b,," -> 2 element
// yaxshi
String[] columns = line.split(",", -1);     // "a,b,," -> 4 element
```

## 21.6 Regexni oldindan kompilyatsiya qilish va nomlash

`String.matches`, `replaceAll` va `split` har bir chaqiruvda regexni qaytadan kompilyatsiya qiladi. Issiq yo'lda bu sezilarli narx. Yechim: `Pattern` ni `static final` maydonga chiqarish - bu bir vaqtda tezlikni va o'qilishni yaxshilaydi, chunki regex nom oladi.

```java
// yomon: har chaqiruvda kompilyatsiya, regex nomsiz
boolean valid = iban.matches("^[A-Z]{2}\\d{2}[A-Z0-9]{1,30}$");

// yaxshi: bir marta kompilyatsiya, nom ma'no beradi
private static final Pattern IBAN_FORMAT =
        Pattern.compile("^[A-Z]{2}\\d{2}[A-Z0-9]{1,30}$");

boolean valid = IBAN_FORMAT.matcher(iban).matches();
```

Murakkab regex uchun `Pattern.COMMENTS` flagi bilan izohli shaklga o'tish mumkin, bu uzun regexni o'qiladigan qiladi.

```java
private static final Pattern SETTLEMENT_LINE = Pattern.compile("""
        ^(?<bank>[A-Z]{4})      # bank kodi: to'rt harf
        (?<date>\\d{8})          # sana: yyyyMMdd
        (?<amount>\\d{12})       # summa: tiyinda, chapdan nol bilan
        $""", Pattern.COMMENTS);
```

Nomlangan guruhlar (`(?<bank>...)`) indeks bo'yicha murojaatdan ancha o'qiladi: `matcher.group("bank")`.

## 21.7 Katastrofik backtracking va kiritish uzunligi

Ba'zi regex shakllari (ichma-ich kvantifikatorlar: `(a+)+`, `(\\w+\\s?)*`) ma'lum kiritishda eksponensial vaqtda ishlaydi va ilovani to'xtatadi. Bu ReDoS (regex denial of service) deb ataladi va tashqi kiritishni regex bilan tekshiradigan har bir joyda xavf bor.

```java
// yomon: ichma-ich kvantifikator - ReDoS xavfi
Pattern.compile("^(\\w+\\s?)*$");

// yaxshi: aniq va chegaralangan
Pattern.compile("^[\\w ]{1,200}$");
```

Qo'shimcha himoya: tashqi kiritish uzunligini regexdan **oldin** cheklash, va murakkab parsing uchun regex o'rniga haqiqiy parser ishlatish.

## 21.8 Satr bilan tiplash o'rniga tur

Satr har qanday qiymatni ushlaydi va shu sababli hech qanday xatoni to'smaydi. Domen tushunchalarini satrda saqlash eng ko'p uchraydigan tur xatosi ([patternlar hujjatidagi](../patterns/README.md) satr bilan tiplash anti-patterni).

```java
// yomon: hammasi String - almashtirish kompilyatsiyadan o'tadi
void transfer(String fromIban, String toIban, String currency, String amount);

// yaxshi
void transfer(Iban from, Iban to, Money amount);
```

Qaysi tushunchalar satrda qolishi mumkin: erkin matn (izoh, tavsif, ism), va tashqi chegaradan kelgan xom qiymat (lekin u darhol turga aylantiriladi).

## 21.9 Matn blokida SQL va JSON

Matn bloki (`"""`) indentatsiyani avtomatik normallashtiradi va qochirishni (escaping) yo'qotadi, shuning uchun SQL, JSON va XML uchun to'g'ri tanlov (12.9). Uch mexanik tafsilot bilish kerak.

Birinchi, yopiluvchi `"""` ning joylashuvi indentatsiyani belgilaydi: eng chapdagi mazmun qatori va yopiluvchi qator orasidagi eng kichik indentatsiya olib tashlanadi. Ikkinchi, `\` qator oxirida yangi qatorni bostiradi. Uchinchi, `\s` bo'shliqni saqlab qoladi (orqa bo'shliqlar aks holda olib tashlanadi).

```java
// Yopiluvchi """ chapda bo'lsa, indentatsiya saqlanadi - odatda keraksiz
String json = """
        {
          "paymentId": "%s",
          "amount": %s
        }
        """.formatted(paymentId, amount);

// Bir qatorli natija kerak bo'lsa: qator oxirida \ bilan birlashtirish
String query = """
        select p.id, p.amount from payment p \
        where p.order_id = ? and p.settled_at is not null\
        """;
```

## 21.10 Amalda qo'llash

- [ ] `==` bilan satr solishtirilgan joylarni grep qilib, `equals` yoki enum ga o'tkazing.
- [ ] `getBytes()`, `new String(byte[])` va `FileReader` chaqiruvlariga oshkor `UTF_8` qo'shing.
- [ ] `toLowerCase()`/`toUpperCase()` chaqiruvlariga `Locale.ROOT` qo'shing yoki `equalsIgnoreCase` ga o'tkazing.
- [ ] `String.format` chaqiruvlarida locale oshkor berilganini tekshiring.
- [ ] `split(",")` chaqiruvlarini CSV uchun `split(",", -1)` ga o'tkazing va regex metabelgilarni qochiring.
- [ ] Barcha inline regexlarni `static final Pattern` maydonlariga chiqarib, nom bering.
- [ ] Tashqi kiritishni tekshiradigan regexlarni ichma-ich kvantifikatorga qarshi ko'rib chiqing va uzunlik chegarasi qo'ying.
- [ ] `+` bilan qurilgan SQL va JSON literallarini matn blokiga o'tkazing.

---

[&larr; 20. Primitiv, son va pul](20-primitiv-son-va-pul.md) · [Mundarija](README.md) · [22. Sana, vaqt va mintaqa &rarr;](22-sana-vaqt-va-mintaqa.md)
