<!-- doc: clean-code | chapter: 22 | part: VII. Java tilining toza ishlatilishi -->

[Toza kod yozuvchining qoidalari](../../README.md) / [Toza kod qoidalari](README.md)

# 22. Sana, vaqt va mintaqa (Date, Time and Zone)

<details>
<summary>Bu bobdagi 10 bo'lim</summary>

- [22.1 `Date`, `Calendar`, `SimpleDateFormat` dan voz kechish](#221-date-calendar-simpledateformat-dan-voz-kechish)
- [22.2 To'g'ri turni tanlash](#222-togri-turni-tanlash)
- [22.3 `Clock` ni inyeksiya qilish va testlanadigan vaqt](#223-clock-ni-inyeksiya-qilish-va-testlanadigan-vaqt)
- [22.4 `ZoneId` va UTC siyosati](#224-zoneid-va-utc-siyosati)
- [22.5 Davomiylik: `Duration`, `Period` va birlik nomi](#225-davomiylik-duration-period-va-birlik-nomi)
- [22.6 Chegaralar: inklyuziv va eksklyuziv oraliq](#226-chegaralar-inklyuziv-va-eksklyuziv-oraliq)
- [22.7 Formatlash va parslash](#227-formatlash-va-parslash)
- [22.8 Yoz/qish vaqti, sakrash soati va oy oxiri](#228-yozqish-vaqti-sakrash-soati-va-oy-oxiri)
- [22.9 Bazada, API da va kodda vaqt turi muvofiqligi](#229-bazada-api-da-va-kodda-vaqt-turi-muvofiqligi)
- [22.10 Amalda qo'llash](#2210-amalda-qollash)

</details>


Vaqt bilan ishlash xatolari odatda production da, ma'lum sanada va bir marta chiqadi: yoz vaqti o'tishida, oy oxirida, yoki boshqa mintaqadagi foydalanuvchida. Bu bobda `java.time` ni to'g'ri ishlatishning qoidalari va testlanadigan vaqt.

## 22.1 `Date`, `Calendar`, `SimpleDateFormat` dan voz kechish

Eski API uch sababdan tashlab yuborilgan: `Date` o'zgaradigan (16.2 dagi sayoz o'zgarmaslik muammosi), `Calendar` oy indeksini 0 dan boshlaydi (`JANUARY == 0`), va `SimpleDateFormat` thread-safe emas - u statik maydonda saqlansa, yuk ostida tasodifiy noto'g'ri sanalar beradi.

```java
// yomon: statik SimpleDateFormat - yuk ostida buziladi
private static final SimpleDateFormat FORMAT = new SimpleDateFormat("dd.MM.yyyy");

// yaxshi: DateTimeFormatter o'zgarmas va thread-safe
private static final DateTimeFormatter FORMAT =
        DateTimeFormatter.ofPattern("dd.MM.yyyy", Locale.ROOT);
```

Legacy API ni taqiqlash uchun Checkstyle `IllegalType` qoidasi ishlatiladi (13.4) yoki ArchUnit qoidasi (42.4).

## 22.2 To'g'ri turni tanlash

`java.time` da turlar ko'p va ularni aralashtirish eng ko'p uchraydigan xato. Tanlov savoli bitta: bu qiymat **vaqt nuqtasimi** yoki **kalendar qiymatimi**.

| Tur | Nima ifodalaydi | Qachon |
|---|---|---|
| `Instant` | mutlaq vaqt nuqtasi (UTC) | hodisa vaqti, `created_at`, log |
| `LocalDate` | mintaqasiz sana | tug'ilgan kun, hisobot kuni, muddat |
| `LocalTime` | mintaqasiz vaqt | ish boshlanishi (09:00) |
| `LocalDateTime` | mintaqasiz sana va vaqt | kamdan-kam; mintaqa yo'q - noaniq |
| `OffsetDateTime` | sana, vaqt va offset | API shartnomasi, tashqi tizim |
| `ZonedDateTime` | mintaqa qoidalari bilan | kelajakdagi rejalashtirish |
| `Duration` | vaqt oralig'i (sekund) | timeout, davomiylik |
| `Period` | kalendar oralig'i (kun, oy) | "3 oy", "1 yil" |
| `YearMonth` | yil va oy | karta muddati, hisobot davri |

Qoida: hodisa vaqti **har doim** `Instant` (bazada `timestamptz`), foydalanuvchiga ko'rsatishda esa uning mintaqasiga aylantiriladi.

## 22.3 `Clock` ni inyeksiya qilish va testlanadigan vaqt

`Instant.now()` ni kod bo'ylab chaqirish vaqtni testlanmaydigan qiladi: "30 kundan keyin muddati o'tadi" qoidasini test qilish uchun tizim vaqtini o'zgartirish kerak bo'ladi. Yechim: `Clock` ni bog'liqlik sifatida uzatish.

```java
@Service
public class OrderExpiryService {

    private final Clock clock;        // inyeksiya qilinadi

    public OrderExpiryService(Clock clock) { this.clock = clock; }

    public boolean isExpired(Order order) {
        return order.createdAt().plus(ORDER_TTL).isBefore(clock.instant());
    }
}

@Configuration
class TimeConfig {
    @Bean
    Clock clock() { return Clock.systemUTC(); }      // production
}

// Test: vaqt qotirilgan, hech qanday kutish yo'q
@Test
void expiresAfterThirtyDays() {
    Clock fixed = Clock.fixed(Instant.parse("2026-03-01T00:00:00Z"), ZoneOffset.UTC);
    var service = new OrderExpiryService(fixed);
    assertThat(service.isExpired(orderCreatedAt("2026-01-01T00:00:00Z"))).isTrue();
}
```

## 22.4 `ZoneId` va UTC siyosati

Mintaqa bilan ishlashda bitta qoida xatolarning katta qismini to'sadi: **saqlash va hisob UTC da, ko'rsatish foydalanuvchi mintaqasida**. Shu chegara aniq bo'lmasa, bir xil hodisa turli joyda turli sanada ko'rinadi.

```java
// yomon: server mintaqasiga bog'liq - serverni ko'chirsa natija o'zgaradi
LocalDate today = LocalDate.now();
ZonedDateTime now = ZonedDateTime.now();

// yaxshi: mintaqa oshkor
LocalDate today = LocalDate.now(clock);                       // clock UTC da
LocalDate userToday = LocalDate.now(clock.withZone(userZone));

// Ko'rsatish chegarasida aylantirish
String display = settledAt.atZone(userZone)
        .format(DateTimeFormatter.ofLocalizedDateTime(FormatStyle.SHORT)
                .withLocale(userLocale));
```

`ZoneId.systemDefault()` ni biznes kodida ishlatish taqiqlanishi kerak: u muhitga bog'liq va testda boshqa natija beradi.

## 22.5 Davomiylik: `Duration`, `Period` va birlik nomi

`Duration` aniq vaqt oralig'ini (sekund va nanosekund) ifodalaydi, `Period` esa kalendar oralig'ini (yil, oy, kun). Farq yoz vaqti o'tishida ko'rinadi: `Duration.ofDays(1)` har doim 24 soat, `Period.ofDays(1)` esa "ertangi kun" (23 yoki 25 soat bo'lishi mumkin).

```java
// yomon: raqam va birlik kodda tarqoq
if (order.getCreatedAt() + 30 * 24 * 60 * 60 * 1000L < now) { ... }

// yaxshi: tur birlikni ushlaydi (3.3)
private static final Duration ORDER_TTL = Duration.ofDays(30);
private static final Duration GATEWAY_TIMEOUT = Duration.ofSeconds(5);

// Konfiguratsiyada ham Duration: "30d", "5s" shaklida yoziladi
@ConfigurationProperties("shop.order")
record OrderProperties(Duration ttl, Duration gatewayTimeout) { }
```

## 22.6 Chegaralar: inklyuziv va eksklyuziv oraliq

Vaqt oraliqlarida chegara xatosi eng ko'p uchraydigan hisobot xatosi: bir kunlik hisobot oxirgi soniyani yo'qotadi yoki keyingi kunni qo'shib yuboradi.

```java
// yomon: 23:59:59 dan keyingi soniyalar yo'qoladi
between(day.atStartOfDay(), day.atTime(23, 59, 59));

// yaxshi: yarim ochiq oraliq [from, to)
Instant from = day.atStartOfDay(zone).toInstant();
Instant toExclusive = day.plusDays(1).atStartOfDay(zone).toInstant();

// SQL da ham shu shakl: >= va < (indeksni ham to'g'ri ishlatadi)
// where settled_at >= ? and settled_at < ?
```

Qoida: barcha vaqt oraliqlari **yarim ochiq** (`[from, to)`) bo'ladi va bu nomda yoziladi (6.7).

## 22.7 Formatlash va parslash

`DateTimeFormatter` o'zgarmas va thread-safe, shuning uchun `static final` maydonda saqlanadi. Ikki tafsilot muhim: locale oshkor berilishi (21.4) va shablonning to'g'ri harflari.

```java
private static final DateTimeFormatter BANK_FILE_DATE =
        DateTimeFormatter.ofPattern("yyyyMMdd", Locale.ROOT);

// Eng ko'p uchraydigan shablon xatolari:
// "YYYY" - hafta-asosli yil (yanvar boshida noto'g'ri yil beradi!)
// "DD"   - yildagi kun raqami, oydagi kun emas
// "hh"   - 12 soatlik format, "HH" 24 soatlik
// To'g'ri: "yyyy-MM-dd HH:mm:ss"
```

API shartnomasida esa shablon yozmaslik kerak: ISO-8601 (`DateTimeFormatter.ISO_INSTANT`) standart va u aniq.

## 22.8 Yoz/qish vaqti, sakrash soati va oy oxiri

Uchta kalendar hodisasi kodni buzadi va ularning hammasi testlanishi kerak.

**Yoz vaqti o'tishi**: ba'zi sana-vaqtlar mavjud bo'lmaydi (soat 02:00 dan 03:00 ga o'tganda) yoki ikki marta bo'ladi. `ZonedDateTime` bu holatlarni o'zi hal qiladi, `LocalDateTime` esa yo'q - shu sababli rejalashtirish uchun `ZonedDateTime` kerak.

**Oy oxiri**: `plusMonths` kunni moslaydi (31-yanvar + 1 oy = 28/29-fevral) va bu odatda to'g'ri xatti-harakat, lekin biznes qoidasi boshqa bo'lishi mumkin.

**Kabisa yili**: 29-fevral `LocalDate.of(2026, 2, 29)` istisno beradi; foydalanuvchi kiritgan sanani har doim `try/catch` yoki `ResolverStyle` bilan tekshirish kerak.

```java
// Testda chegaraviy sanalar majburiy
@ParameterizedTest
@ValueSource(strings = {
        "2026-03-29T01:30:00",   // yoz vaqtiga o'tish kuni (Toshkentda yo'q, Yevropada bor)
        "2026-01-31",            // oy oxiri
        "2024-02-29",            // kabisa yili
        "2026-12-31T23:59:59"    // yil oxiri
})
void handlesCalendarEdges(String input) { ... }
```

## 22.9 Bazada, API da va kodda vaqt turi muvofiqligi

Uch qatlamda vaqt turi mos bo'lishi kerak, aks holda konvertatsiya paytida mintaqa yo'qoladi.

| Qatlam | To'g'ri tur |
|---|---|
| PostgreSQL ustuni | `timestamptz` (hodisa), `date` (kalendar kuni) |
| JDBC/JPA maydoni | `Instant` yoki `OffsetDateTime`, `LocalDate` |
| Domen obyekti | `Instant`, `LocalDate` |
| JSON API | ISO-8601 satr (`2026-03-01T10:15:30Z`) |
| Konfiguratsiya | `Duration` (`30s`, `5m`) |
| Log | ISO-8601, UTC |
| Metrika | Unix epoch |

`timestamp without time zone` ustunini `Instant` ga bog'lash eng ko'p uchraydigan nomuvofiqlik: baza mintaqani saqlamaydi va qiymat server mintaqasiga qarab o'zgaradi ([arxitektor hujjatidagi](../architect/README.md) sxema dizayni bo'limi sxema dizaynini ko'rib chiqadi).

## 22.10 Amalda qo'llash

- [ ] `java.util.Date`, `Calendar` va `SimpleDateFormat` ni Checkstyle yoki ArchUnit bilan taqiqlang va qolganlarini ko'chiring.
- [ ] `Instant.now()`, `LocalDate.now()` chaqiruvlarini topib, `Clock` inyeksiyasiga o'tkazing.
- [ ] `Clock` bean ini `Clock.systemUTC()` sifatida e'lon qilib, testlarda `Clock.fixed` ishlatishni standart qiling.
- [ ] `ZoneId.systemDefault()` ishlatilgan joylarni oshkor mintaqaga almashtiring.
- [ ] Vaqt oraliqlarini yarim ochiq (`[from, to)`) shaklga keltirib, nomda inklyuzivlikni yozing.
- [ ] Timeout va TTL qiymatlarini `Duration` ga o'tkazib, konfiguratsiyada `30s` shaklida yozing.
- [ ] `DateTimeFormatter` shablonlarida `YYYY`, `DD`, `hh` xatolarini qidirib tuzating.
- [ ] Baza ustunlarini `timestamptz` ga keltirib, JPA maydonlari `Instant` ekanini tekshiring.

---

[&larr; 21. Satr, matn va regex](21-satr-matn-va-regex.md) · [Mundarija](README.md) · [23. To'plamlar va generiklar gigiyenasi &rarr;](23-toplamlar-va-generiklar-gigiyenasi.md)
