<!-- doc: code-review | chapter: 8 | part: II. Arxitektura, dizayn va clean code review -->

[Kod review](../../README.md) / [Kod review](README.md)

# 8. Clean code review: nomlash, kognitiv yuk, metod shakli (Clean Code at the Review Table)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

- [8.1 Nom - eng arzon hujjat va eng qimmat xato](#81-nom---eng-arzon-hujjat-va-eng-qimmat-xato)
- [8.2 Birlik, valyuta va vaqt zonasi nomda](#82-birlik-valyuta-va-vaqt-zonasi-nomda)
- [8.3 Metod shakli: uzunlik emas, shoxlanish](#83-metod-shakli-uzunlik-emas-shoxlanish)
- [8.4 Boolean parametr - yashirin ikki metod](#84-boolean-parametr---yashirin-ikki-metod)
- [8.5 Primitive obsession: domen tilini turga aylantirish](#85-primitive-obsession-domen-tilini-turga-aylantirish)
- [8.6 Izoh qachon kerak](#86-izoh-qachon-kerak)
- [8.7 O'lik kod va yarim ishlangan narsalar](#87-olik-kod-va-yarim-ishlangan-narsalar)
- [8.8 Clean code bahonasida haddan oshish](#88-clean-code-bahonasida-haddan-oshish)
- [8.9 Formatlash izohi review da bo'lmasligi kerak](#89-formatlash-izohi-review-da-bolmasligi-kerak)
- [8.10 O'qiluvchanlikni o'lchash: review ning o'zi sinov](#810-oqiluvchanlikni-olchash-review-ning-ozi-sinov)
- [8.11 Amalda qo'llash](#811-amalda-qollash)

</details>


Clean code review ning eng ko'p noto'g'ri bajariladigan qismi, chunki u didga eng yaqin. Natijada review ikki qutbga ketadi: yoki uslub haqida uzun bahs, yoki hech qanday izoh. To'g'ri yo'l o'rtada: nomlash va shakl haqidagi izoh faqat kelajakdagi o'qish narxini oshiradigan holatlarda yoziladi va har doim sabab bilan birga keladi.

## 8.1 Nom - eng arzon hujjat va eng qimmat xato

Kod bir marta yoziladi, o'nlab marta o'qiladi. Nom esa o'qishning har safarida ishlaydi. Shu sababli nom haqidagi izoh "did" emas - u o'qish narxini kamaytiradi. Lekin mezon kerak: nom qachon yomon.

| Yomon nom belgisi | Misol | Nega muammo |
| --- | --- | --- |
| Turini aytadi, ma'nosini aytmaydi | `List<String> list`, `Map<String,String> map` | O'qiyotgan odam yana koddan izlaydi |
| Qisqartma domen tilida emas | `ordNum`, `custTp`, `amtUsd` | Yangi odam dekodlashga vaqt sarflaydi |
| Yolg'on nom | `validateOrder` ichida saqlaydi ham | Noto'g'ri taxmin, keyin xato |
| Juda umumiy | `data`, `info`, `process`, `handle`, `manager` | Hech narsa aytmaydi |
| Raqam bilan ajratilgan | `result1`, `result2`, `temp2` | Farqi kodni o'qimasdan bilinmaydi |
| Inkor bilan | `isNotInactive` | Ikki marta inkor, miyada aylantirish kerak |
| Birlik yo'q | `timeout = 30`, `size = 5` | 30 nima: sekund, millisekund? |
| Domen tiliga qarshi | Biznes "invoys" deydi, kodda `bill` | Suhbat va kod tili ajraladi |

```java
// Nom orqali bilimni kodga kiritish. Birinchi variant: nom hech narsa aytmaydi.
public boolean check(Order o, int d) {
    return o.getCreated().plusDays(d).isAfter(LocalDate.now());
}

// Ikkinchi variant: nom qoidani aytadi, izoh kerak emas.
public boolean isWithinReturnWindow(Order order, int returnWindowDays) {
    return order.placedOn().plusDays(returnWindowDays).isAfter(today());
}

// Uchinchi variant: birlik va domen tur bilan kiritilgan - noto'g'ri
// qiymat uzatish kompilyatsiyada tutiladi.
public boolean isWithinReturnWindow(Order order, ReturnWindow window) { ... }
public record ReturnWindow(Period period) { }
```

Review da nom haqidagi izohning foydali shakli: yangi nomni taklif qilish, shunda muallif o'ylab topishga vaqt sarflamaydi. "Nomi tushunarsiz" degan izoh ish qo'shadi, "`pendingShipments` desak, keyingi o'qiyotgan odam ro'yxat nimadan iboratligini bilib turadi" degan izoh ishni kamaytiradi.

## 8.2 Birlik, valyuta va vaqt zonasi nomda

Eng qimmat nomlash xatolari o'lchov birligi bilan bog'liq. `timeout = 30` satri ikki xil o'qiladi va noto'g'ri o'qish prodda chiqadi.

```java
// Yomon: birlik nomda yo'q, tur hech narsa kafolatlamaydi.
public void retry(int delay, int timeout) { ... }
retry(30, 5);                                  // 30 nima? 5 nima?

// Yaxshiroq: birlik nomda.
public void retry(long delayMillis, long timeoutMillis) { ... }

// Eng yaxshi: tur birlikni ushlab turadi, aralashtirib bo'lmaydi.
public void retry(Duration delay, Duration timeout) { ... }
retry(Duration.ofSeconds(30), Duration.ofSeconds(5));

// Pul uchun ham xuddi shunday: valyuta turning ichida.
public record Money(BigDecimal amount, Currency currency) {
    public Money add(Money other) {
        if (!currency.equals(other.currency)) {
            throw new IllegalArgumentException("valyutalar mos emas");
        }
        return new Money(amount.add(other.amount), currency);
    }
}
// Review izohi: BigDecimal total parametri valyutani ushlamaydi. Ikki
// valyutadagi summalarni qo'shib qo'yish kompilyatsiyada tutilmaydi va
// hisobot noto'g'ri bo'ladi.
```

## 8.3 Metod shakli: uzunlik emas, shoxlanish

"Metod 20 satrdan oshmasin" qoidasi mexanik va foydasi kam. Haqiqiy mezon - metodni tushunish uchun miyada qancha narsa ushlab turish kerak. 40 satrli chiziqli metod 12 satrli uch darajali ichma-ich shartli metoddan osonroq o'qiladi.

```java
// Uch darajali ichma-ich shart: har qadamda kontekst to'planadi.
public Result process(Order order) {
    if (order != null) {
        if (order.getStatus() == NEW) {
            if (order.getLines() != null && !order.getLines().isEmpty()) {
                if (inventory.hasStock(order)) {
                    return doProcess(order);
                } else {
                    return Result.outOfStock();
                }
            } else {
                return Result.empty();
            }
        } else {
            return Result.wrongStatus();
        }
    }
    return Result.invalid();
}

// Erta qaytish: har satrdan keyin kontekst kamayadi, oxirida faqat
// "hammasi yaxshi" holati qoladi.
public Result process(Order order) {
    if (order == null)              return Result.invalid();
    if (order.status() != NEW)      return Result.wrongStatus();
    if (order.lines().isEmpty())    return Result.empty();
    if (!inventory.hasStock(order)) return Result.outOfStock();
    return doProcess(order);
}
```

Review mezonlari shakl uchun: ichma-ich chuqurlik 2 dan oshmasin, bitta metodda `if` zanjiri 5 dan oshmasin, va `else` bloki bo'sh yoki faqat qaytarishdan iborat bo'lsa, erta qaytishga aylantirilsin.

## 8.4 Boolean parametr - yashirin ikki metod

Metod chaqiruvida `true` yoki `false` ko'rilsa, chaqiruv joyi hech narsa aytmaydi. Bundan tashqari bu boshqaruv bog'liqligi: chaqiruvchi chaqirilgan metodning ichidagi shoxni tanlaydi.

```java
// Chaqiruv joyi o'qilmaydi.
exporter.export(orders, true, false, true);

// Variant 1: alohida metodlar - eng aniq.
exporter.exportWithHeaders(orders);
exporter.exportRaw(orders);

// Variant 2: nomlangan sozlama obyekti - parametrlar ko'p bo'lsa.
exporter.export(orders, ExportOptions.builder()
                                     .withHeaders(true)
                                     .delimiter(';')
                                     .compress(false)
                                     .build());

// Variant 3: enum - ikkidan ko'p holat bo'lsa.
exporter.export(orders, ExportFormat.CSV_WITH_HEADERS);
```

## 8.5 Primitive obsession: domen tilini turga aylantirish

Hamma narsa `String` va `long` bo'lgan kodda kompilyator hech narsa himoya qilmaydi. `userId` va `orderId` ni almashtirib qo'yish - kompilyatsiya bo'ladigan, lekin xato kod.

```java
// Xavfli: ikki long ni almashtirib qo'yish mumkin, kompilyator jim.
public void transfer(long fromAccount, long toAccount, BigDecimal amount) { }
transfer(toId, fromId, amount);                 // xato, lekin kompilyatsiya bo'ladi

// Xavfsiz: tur almashtirishni taqiqlaydi.
public record AccountId(UUID value) {
    public AccountId { Objects.requireNonNull(value); }
}
public void transfer(AccountId from, AccountId to, Money amount) { }

// Domen qoidasi turning ichida: noto'g'ri qiymat yaratilmaydi.
public record Email(String value) {
    private static final Pattern RE = Pattern.compile("^[^@\\s]+@[^@\\s]+\\.[^@\\s]+$");
    public Email {
        if (value == null || !RE.matcher(value).matches()) {
            throw new IllegalArgumentException("email shakli noto'g'ri");
        }
        value = value.toLowerCase(Locale.ROOT);   // normalizatsiya bir joyda
    }
}
// Review foydasi: email tekshiruvi 7 joyda takrorlanmaydi, va bazaga
// normalizatsiya qilinmagan email tushmaydi.
```

Review da mezon: qiymat domen qoidasiga egami (email, telefon, pul, identifikator, status) va u noto'g'ri bo'lishi mumkinmi. Ikkisiga "ha" bo'lsa, u o'z turiga arziydi. Oddiy texnik qiymat (hisoblash natijasi, ichki indeks) uchun primitiv yetadi.

## 8.6 Izoh qachon kerak

Izoh kodni takrorlasa - u ikki marta qarishadi. Izoh sababni aytsa - u kodda bo'lmagan bilimni saqlaydi.

```java
// Foydasiz izoh: kod aytganini takrorlaydi.
// Buyurtmani saqlaydi
orders.save(order);

// Foydali izoh: nega shunday qilingani, va nima bo'lsa o'zgartirish mumkinligi.
// PostgreSQL da bu jadval 40 mln qator. created_at bo'yicha indeks bor,
// lekin status bo'yicha yo'q: qiymatlar notekis taqsimlangan (99% CLOSED),
// shuning uchun planner indeksni ishlatmaydi. Partial indeks qo'shilsa,
// bu filtr ham indeksga tushadi: INDEX ... WHERE status <> 'CLOSED'.
List<Order> open = orders.findOpenCreatedAfter(since);

// Foydali izoh: tashqi tizim xulqi haqida, kodda ko'rinmaydigan bilim.
// To'lov provayderi 409 ni "allaqachon bajarilgan" ma'nosida qaytaradi,
// hujjatda 409 "konflikt" deb yozilgan. 2026-02 da support bilan
// tasdiqlangan. Shuning uchun 409 muvaffaqiyat deb hisoblanadi.
if (response.statusCode() == 409) return AuthResult.approved(idemKey);
```

Review qoidasi: har bir `// hack`, `// vaqtincha`, `// TODO` izohiga egasi va sanasi kerak, aks holda u abadiy qoladi.

```bash
# Egasi yo'q TODO larni topish: ular texnik qarzning yashirin qismi.
grep -rn --include='*.java' -E 'TODO|FIXME|HACK|XXX' src/main/java \
  | grep -vE 'TODO\([a-z.]+,[ ]*[0-9]{4}-[0-9]{2}\)' | head -20
# Konvensiya: TODO(ism, 2026-06): sabab va shart.
```

## 8.7 O'lik kod va yarim ishlangan narsalar

Diffda qo'shilgan, lekin hech kim chaqirmaydigan kod - kelajakdagi chalg'itish manbasi. Keyingi odam uni ishlaydi deb o'ylaydi.

```bash
# Yangi qo'shilgan public metodlar chaqirilyaptimi.
git diff origin/main...HEAD -- '*.java' \
  | grep -oE '^\+\s+(public|protected).* ([a-zA-Z][a-zA-Z0-9]*)\(' \
  | grep -oE '[a-zA-Z][a-zA-Z0-9]*\($' | tr -d '(' | sort -u \
  | while read -r m; do
      c=$(grep -rn --include='*.java' "\.$m(\|::$m" src/ | wc -l)
      [ "$c" -eq 0 ] && echo "CHAQIRILMAYDI: $m"
    done

# Kommentga olingan kod bloklari: review da darhol olib tashlash so'raladi.
git diff origin/main...HEAD | grep -E '^\+\s*//\s*[a-zA-Z].*[;{)]' | head
```

Kommentga olingan kod uchun javob har doim bitta: o'chirish. Git tarixi uni saqlaydi, va kommentdagi kod hech qachon yangilanmaydi.

## 8.8 Clean code bahonasida haddan oshish

Review ning teskari xatosi ham bor: toza kod nomidan ortiqcha talab qo'yish. Buning belgilari: har bir uch satrli bo'lak alohida metodga ajratish, har bir `if` ni Strategy ga aylantirish, har bir klassga interfeys, har bir konstantaga enum.

Mezon: o'zgarish o'qish narxini kamaytiradimi yoki faqat qoidaga moslashtiradimi. Ikkinchi holatda izoh `nit` darajasida qoladi va majburiy bo'lmaydi.

| Haddan oshish shakli | Natija |
| --- | --- |
| Har 3 satr alohida metod | Metodlar zanjiri, bitta mantiqni o'qish uchun 8 joyga sakrash |
| Har joyda interfeys | Navigatsiya qiyinlashadi, foyda nol |
| Har `if` uchun Strategy | Ikki holat uchun 5 klass |
| Har konstanta uchun enum | Ortiqcha ceremony |
| Har metodda Javadoc | Takrorlangan matn, qarishadi |
| Har DTO uchun builder | Record bilan osonroq |

## 8.9 Formatlash izohi review da bo'lmasligi kerak

Agar PR da formatlash haqida izoh yozilayotgan bo'lsa, bu instrument yo'qligini bildiradi. Bitta marta sozlangan formatter shu izohlarning hammasini abadiy yo'q qiladi.

```xml
<!-- spotless: formatlash muhokamasini butunlay tugatish. -->
<plugin>
  <groupId>com.diffplug.spotless</groupId>
  <artifactId>spotless-maven-plugin</artifactId>
  <configuration>
    <java>
      <googleJavaFormat><style>AOSP</style></googleJavaFormat>
      <removeUnusedImports/>
      <importOrder><order>java,javax,jakarta,org,com,</order></importOrder>
      <trimTrailingWhitespace/>
      <endWithNewline/>
    </java>
    <sql><dbeaver/></sql>
  </configuration>
  <executions>
    <execution>
      <!-- CI da tekshiradi, lokalda `mvn spotless:apply` tuzatadi. -->
      <goals><goal>check</goal></goals>
      <phase>validate</phase>
    </execution>
  </executions>
</plugin>
```

## 8.10 O'qiluvchanlikni o'lchash: review ning o'zi sinov

O'qiluvchanlikning eng yaxshi sinovi - review ning o'zi. Agar reviewer kodni tushunish uchun savol berishga majbur bo'lsa, demak kod yetarlicha aytmagan. Shu holatda to'g'ri javob - izohda tushuntirish emas, kodni tushunarli qilish.

Foydali odat: muallif review savoliga javob yozganida o'zidan so'rashi kerak - shu javob kodda bo'lishi kerakmidi. Ko'p hollarda javob "ha" bo'ladi va u nom, tur yoki qisqa izohga aylanadi. Shu bilan review bir martalik suhbatdan doimiy bilimga aylanadi.

## 8.11 Amalda qo'llash

- [ ] `spotless` yoki `google-java-format` ni CI ga qo'shib, formatlash izohlarini butunlay taqiqlang.
- [ ] Loyihada birlik ko'rsatilmagan vaqt va hajm parametrlarini toping (`int timeout`, `long delay`) va `Duration` ga o'tkazishni rejalashtiring.
- [ ] Pul hisobida `BigDecimal` valyutasiz ishlatilgan joylarni toping va `Money` turini kiriting.
- [ ] Boolean parametrli public metodlarni grep bilan toping va ularni alohida metod yoki enum ga ajratish ro'yxatini tuzing.
- [ ] Email, telefon, identifikator kabi domen qiymatlari uchun value object kiritib, takrorlangan validatsiyalarni bitta joyga yig'ing.
- [ ] `TODO(ism, sana)` konvensiyasini joriy qilib, egasi yo'q TODO larni CI da ogohlantirishga chiqaring.
- [ ] Yangi qo'shilgan, lekin chaqirilmaydigan public metodlarni aniqlaydigan skriptni review oqimiga qo'shing.
- [ ] Review izohlarining qanchasi `nit` ekanini sanab, ularning 20 foizdan ko'pi bo'lsa, instrumentlarga ko'chirish mumkinligini tekshiring.

---

[&larr; 7. Bog'liqlik, koheziya va abstraksiya review](07-bogliqlik-koheziya-va-abstraksiya-review.md) · [Mundarija](README.md) · [9. SOLID va dizayn printsiplarini diffda tekshirish &rarr;](09-solid-va-dizayn-printsiplarini-diffda.md)
