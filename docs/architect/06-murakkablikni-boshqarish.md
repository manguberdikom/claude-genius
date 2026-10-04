<!-- doc: architect | chapter: 6 | part: I. Fikrlash va qarorlar -->

[Kod yozadigan arxitektorning miyyasi](../../README.md) / [Arxitektor miyyasi](README.md)

# 6. Murakkablikni boshqarish (Managing Complexity)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

- [6.1 Muhim murakkablik va tasodifiy murakkablik farqi](#61-muhim-murakkablik-va-tasodifiy-murakkablik-farqi)
- [6.2 Murakkablik qayerda to'planadi: shart, holat, integratsiya nuqtalari](#62-murakkablik-qayerda-toplanadi-shart-holat-integratsiya-nuqtalari)
- [6.3 Holat (state) ni kamaytirish: immutable obyekt va sof funksiya](#63-holat-state-ni-kamaytirish-immutable-obyekt-va-sof-funksiya)
- [6.4 Konfiguratsiya murakkabligi: har bir flag kelajakdagi xato](#64-konfiguratsiya-murakkabligi-har-bir-flag-kelajakdagi-xato)
- [6.5 Kodni o'chirish: eng kam baholangan arxitektura ishi](#65-kodni-ochirish-eng-kam-baholangan-arxitektura-ishi)
- [6.6 Texnik qarz: ongli qarz va tasodifiy loyqalik](#66-texnik-qarz-ongli-qarz-va-tasodifiy-loyqalik)
- [6.7 Murakkablikni o'lchash: o'zgarish vaqti, incident soni, yangi odam vaqti](#67-murakkablikni-olchash-ozgarish-vaqti-incident-soni-yangi-odam-vaqti)
- [6.8 Servislar soni va operatsion murakkablik narxi](#68-servislar-soni-va-operatsion-murakkablik-narxi)
- [6.9 Umumiylashtirish tuzog'i: uchta foydalanuvchiga mo'ljallangan platforma](#69-umumiylashtirish-tuzogi-uchta-foydalanuvchiga-moljallangan-platforma)
- [6.10 Murakkablikni jamoaga tushuntirish va qarorni himoya qilish](#610-murakkablikni-jamoaga-tushuntirish-va-qarorni-himoya-qilish)
- [6.11 Amalda qo'llash](#611-amalda-qollash)

</details>


Arxitektorning asosiy ishi tezlik emas, murakkablikni boshqarish. Kod ishlayotgan holatda ham tizim o'lishi mumkin, chunki uni o'zgartirish narxi daromaddan oshib ketadi. Shu bobda murakkablik qayerdan kelib chiqadi, qanday o'lchanadi va uni kamaytiradigan qarorlar qanday himoya qilinadi degan savollarga javob beramiz. Misollar bitta tizimdan olinadi: to'lov servisi, buyurtma oqimi va ombor qoldig'i.

## 6.1 Muhim murakkablik va tasodifiy murakkablik farqi

Muhim murakkablik (essential) biznesning o'zidan keladi. Ombor qoldig'i rezervatsiya, bekor qilish, qaytarish va inventarizatsiya hisobiga o'zgaradi, va bu to'rt oqim bir-biri bilan kesishadi. Bu murakkablikni yo'qotib bo'lmaydi, uni faqat ko'chirish mumkin: kodga, ma'lumotlar modeliga yoki operator qo'llanmasiga.

Tasodifiy murakkablik (accidental) bizning qarorlarimizdan keladi. Uch qatlamli mapper, keraksiz event bus, har bir DTO uchun abstract factory, oltita profil, ikkita ORM. Buni o'lchash oson: biznes qoidasini bitta gap bilan aytib bo'ladimi, lekin uni kodda topish uchun beshta faylni ochish kerakmi. Agar shunday bo'lsa, qolgan to'rtta fayl tasodifiy murakkablik.

Amaliy test: yangi talab kelganda nechta joyga tegish kerak. "Rezerv 30 daqiqadan keyin bo'shasin" talabi bitta domen metodida bo'lsa, model to'g'ri. Agar bu scheduler, cache evict listener, DTO flag va frontend timerga tarqalgan bo'lsa, murakkablik tarqab ketgan.

```java
// Tasodifiy murakkablik: qoida uch joyga tarqalgan
if (order.getStatus() == Status.NEW && order.getPayment() != null
        && order.getPayment().getState().equals("AUTHORIZED")
        && !order.getItems().isEmpty()
        && order.getCreatedAt().isAfter(Instant.now().minus(Duration.ofMinutes(30)))) {
    reserve(order);
}

// Muhim murakkablik model ichida: qoida bitta nom oldi
if (order.readyForReservation(clock.instant())) {
    reserve(order);
}

// Order ichida, testlanadigan sof shart
boolean readyForReservation(Instant now) {
    return status == Status.NEW
        && payment.isAuthorized()
        && !items.isEmpty()
        && createdAt.isAfter(now.minus(RESERVATION_WINDOW));
}
```

## 6.2 Murakkablik qayerda to'planadi: shart, holat, integratsiya nuqtalari

Murakkablik tizimda bir tekis tarqalmaydi, u uchta joyga yig'iladi. Birinchi joy shartlar. Har bir `if` ikkita yo'l hosil qiladi, ketma-ket beshta mustaqil shart esa nazariy jihatdan 32 holat beradi. Amalda ularning yarmi hech qachon test qilinmaydi va aynan shu yarmidan incident chiqadi.

Ikkinchi joy holat. O'zgaradigan maydon vaqt o'qini kiritadi: javob endi "qaysi tartibda chaqirildi" degan savolga bog'liq. Spring kontekstida singleton bean ichidagi o'zgaradigan maydon eng qimmat xato, chunki u barcha request thread'lari bilan bo'linadi.

Uchinchi joy integratsiya nuqtalari. Har bir tashqi chaqiruv to'rtta yangi natija qo'shadi: muvaffaqiyat, biznes xatosi, timeout va noaniq holat. Noaniq holat eng qimmati, chunki to'lov provayderi timeout bergan paytda pul o'tgan yoki o'tmaganini bilmaymiz. Shu sababli to'lovda idempotency key va status so'rovi arxitekturaning bir qismi, qo'shimcha emas.

```java
// Integratsiya nuqtasi: uchta natija emas, to'rtta
PaymentOutcome charge(ChargeCommand cmd) {
    try {
        var res = client.charge(cmd.idempotencyKey(), cmd.amount());
        return res.approved() ? PaymentOutcome.approved(res.id())
                              : PaymentOutcome.declined(res.reason());
    } catch (PaymentDeclinedException e) {
        return PaymentOutcome.declined(e.getReason());   // biznes xatosi
    } catch (ResourceAccessException e) {
        // noaniq holat: pul o'tgan bo'lishi ham mumkin
        return PaymentOutcome.unknown(cmd.idempotencyKey());
    }
}
```

`unknown` holatini alohida nom bilan belgilash murakkablikni kamaytiradi. Aks holda u `catch (Exception e) { return false; }` ichida yashirinadi va bir yildan keyin ikki marta pul olish incidenti bo'lib qaytadi.

## 6.3 Holat (state) ni kamaytirish: immutable obyekt va sof funksiya

O'zgarmas obyekt bitta savolni butunlay o'chiradi: "bu qiymat qachon o'zgardi". Java 17 dan keyin `record` buni arzon qiladi, Java 21 da pattern matching bilan birga esa domen modelini o'qish osonlashadi. Qoida sodda: hisob-kitob sof funksiyada, o'zgarish esa faqat bitta joyda, aggregate ichida.

Sof funksiya testda mock talab qilmaydi. Narx hisoblashni `Clock` va narx jadvalini argument sifatida olgan funksiyaga aylantirsangiz, uning testi 1 ms da ishlaydi va Spring konteksti ko'tarilmaydi. Shu bilan test paketining ishlash vaqti o'nlab barobar qisqaradi, buning tafsiloti [testlash qo'llanmasidagi](../testing/README.md) unit test bo'limida.

```java
// Immutable buyruq va natija, sof hisob-kitob
public record PriceRequest(String sku, int qty, BigDecimal unitPrice,
                           BigDecimal discountRate) {
    public PriceRequest {
        if (qty <= 0) throw new IllegalArgumentException("qty musbat bo'lishi kerak");
    }
}

public record PriceResult(BigDecimal net, BigDecimal vat, BigDecimal total) {}

public final class Pricing {
    private static final BigDecimal VAT = new BigDecimal("0.12");

    // Sof funksiya: tashqi holat yo'q, natija faqat argumentlarga bog'liq
    public static PriceResult calculate(PriceRequest r) {
        var gross = r.unitPrice().multiply(BigDecimal.valueOf(r.qty()));
        var net = gross.subtract(gross.multiply(r.discountRate()))
                       .setScale(2, RoundingMode.HALF_UP);
        var vat = net.multiply(VAT).setScale(2, RoundingMode.HALF_UP);
        return new PriceResult(net, vat, net.add(vat));
    }
}
```

Kolleksiyalarni ham himoyalash kerak. `record` maydonidagi `List` havolasi hali ham o'zgaradi, shuning uchun konstruktorda `List.copyOf(items)` chaqiriladi. Hibernate 6.x bilan ishlaganda entity o'zgaruvchan bo'lib qoladi, lekin uning atrofida immutable projection va read model yarating. Bitta amaliy qoida: tranzaksiyadan tashqariga entity emas, record chiqsin, shunda lazy loading va detached holat muammosi tug'ilmaydi.

## 6.4 Konfiguratsiya murakkabligi: har bir flag kelajakdagi xato

Feature flag arzon ko'rinadi, chunki uni qo'shish bir qator. Narx esa kombinatsiyada. Oltita boolean flag 64 ta konfiguratsiya varianti beradi, va siz ulardan ikkitasini test qilasiz. Qolgan 62 tasi production'da "bizda shunday sozlanmagan edi" degan incident sifatida ochiladi.

Flag ikki turga bo'linadi. Release flag vaqtinchalik, uning muddati bor va u yopilgandan keyin o'chiriladi. Operatsion flag doimiy, masalan timeout qiymati yoki pool kattaligi. Release flag kodda qolib ketsa, u darhol texnik qarzga aylanadi. Shu sababli har bir release flag yaratilganda ikkita narsa yoziladi: egasi va o'lim sanasi.

```yaml
# Flag ro'yxati: har birida ega va o'lim sanasi bor
app:
  payments:
    # operatsion sozlama, doimiy qoladi
    connect-timeout: 2s
    read-timeout: 5s
    pool-max-connections: 50
  features:
    # release flag, 2026-11-15 da kod bilan birga o'chiriladi
    new-refund-flow:
      enabled: false
      owner: payments-team
      remove-after: 2026-11-15
```

```java
// Flag sonini cheklash uchun: tipli konfiguratsiya va validatsiya
@Validated
@ConfigurationProperties(prefix = "app.payments")
public record PaymentProperties(
        @NotNull Duration connectTimeout,
        @NotNull Duration readTimeout,
        @Min(5) @Max(200) int poolMaxConnections) {}
```

Tipli `@ConfigurationProperties` noto'g'ri qiymatni ishga tushish paytida ushlaydi, ya'ni soat 03:00 dagi incident o'rniga deploy paytidagi xato beradi. Spring Boot'ning `configprops` actuator endpoint'i joriy qiymatlarni ko'rsatadi, shuning uchun "qaysi qiymat ishlayapti" savoli bahsga aylanmaydi. Qoida: `@Value` bilan tarqalgan o'nlab satr o'rniga bitta tipli record yaxshi.

## 6.5 Kodni o'chirish: eng kam baholangan arxitektura ishi

Kod o'chirish murakkablikni kamaytiradigan eng ishonchli usul. U yangi abstraksiya qo'shishdan farqli ravishda hech qanday yangi xato kiritmaydi, agar o'chirilayotgan kod haqiqatan ishlatilmayotgan bo'lsa. Muammo faqat bitta: "ishlatilmayapti" degan gapni dalil bilan tasdiqlash kerak.

Dalil uchta manbadan olinadi. Birinchisi kod tahlili: statik qidiruv, reflection va SpEL ishlatilishini qo'lda tekshirish. Ikkinchisi runtime telemetriya: endpoint uchun request soni, bean uchun metrika, SQL uchun statistika. Uchinchisi ma'lumot: jadvalda yangi qator qo'shilganmi.

```sql
-- PostgreSQL 15-17: oxirgi statistika tiklanishidan beri tegilmagan indekslar
SELECT s.relname AS jadval, s.indexrelname AS indeks,
       s.idx_scan AS skanlar,
       pg_size_pretty(pg_relation_size(s.indexrelid)) AS hajm
FROM pg_stat_user_indexes s
JOIN pg_index i ON i.indexrelid = s.indexrelid
WHERE s.idx_scan = 0 AND NOT i.indisunique
ORDER BY pg_relation_size(s.indexrelid) DESC
LIMIT 20;

-- Jadval haqiqatan o'likmi: oxirgi yozuv vaqti va o'sish
SELECT relname, n_live_tup, n_tup_ins, n_tup_upd, last_autoanalyze
FROM pg_stat_user_tables
WHERE n_tup_ins = 0 AND n_tup_upd = 0
ORDER BY n_live_tup DESC;
```

Statistika `pg_stat_reset()` dan keyin yig'ilganini tekshiring, aks holda "0 skan" degan xulosa yolg'on bo'ladi. Kamida ikki hafta, mavsumiy hisobotlar bor bo'lsa bir oy kuzatish kerak, chunki chorak oxiridagi hisobot indeksni yiliga to'rt marta ishlatadi.

```bash
# O'chirishga nomzod: 12 oy davomida tegilmagan paketlar
git log --since="12 months ago" --name-only --pretty=format: \
  | grep -E '^src/main/java' | sort -u > /tmp/tegilgan.txt
find src/main/java -name '*.java' | sort > /tmp/hammasi.txt
comm -13 /tmp/tegilgan.txt /tmp/hammasi.txt | head -50

# O'chirishni bosqichli qilish: avval @Deprecated, keyin log, keyin olib tashlash
grep -rn "@Deprecated" src/main/java | wc -l
```

O'chirish bosqichli bo'ladi. Avval `@Deprecated` va WARN log qo'yiladi, ikki hafta kuzatiladi, log bo'sh bo'lsa kod olib tashlanadi. Ma'lumotlar bazasida ustun darhol `DROP` qilinmaydi, avval yozishni to'xtatish, keyin o'qishni to'xtatish, so'ng bir release kutib `DROP COLUMN` qilish kerak.

## 6.6 Texnik qarz: ongli qarz va tasodifiy loyqalik

Qarzning ikki turi bor va ular bilan muomala butunlay boshqacha. Ongli qarz qaror bilan olinadi: "Qora juma oldidan hisobotni to'g'ri modellashtirishga vaqt yo'q, vaqtinchalik SQL view bilan chiqaramiz, yanvarda qaytamiz". Bunda shart ma'lum, muddat ma'lum, egasi ma'lum.

Tasodifiy loyqalik hech qanday qaror bilan olinmagan. U shunchaki paydo bo'ladi: nomlash buzilgan, qatlam chegarasi yo'q, bitta servis ikki xil tranzaksiya modelini ishlatadi. Bu turdagi qarz foizi yuqori, chunki uning mavjudligini hech kim bilmaydi.

Arxitektor vazifasi loyqalikni ongli qarzga aylantirish. Bu ADR (arxitektura qaror yozuvi) orqali qilinadi: muammo, variantlar, tanlangan yo'l, narxi va qaytish sharti yoziladi. Qaytish sharti eng muhim qism, chunki u "bir kun kelib tozalaymiz" degan gapni o'lchanadigan narsaga aylantiradi. Masalan: "kunlik hisobot 90 sekunddan oshsa, yoki jadval 50 mln qatordan o'tsa, read model kiritiladi".

| Tuzoq | Nimaga olib keladi | Yechim |
|---|---|---|
| Flag kod bilan birga o'chirilmaydi | Har release'da kombinatsiya soni ikki barobar | Flag yaratilganda `remove-after` sanasi va CI tekshiruvi |
| "Umumiy" `util` paketi o'sib ketadi | Hamma hammaga bog'lanadi, modul chegarasi yo'qoladi | ArchUnit qoidasi: `util` faqat JDK ga bog'lansin |
| Singleton bean ichida o'zgaradigan maydon | Yuk ostida tasodifiy noto'g'ri natija | Holatni `record` ga, yoki `ThreadLocal` emas, argumentga ko'chirish |
| Entity DTO sifatida API dan chiqadi | Sxema o'zgarishi mijozni buzadi, lazy loading xatosi | Alohida projection record va `@Query` bilan to'g'ridan-to'g'ri map |
| Har bir servis o'zi retry qiladi | Timeout ostida chaqiruvlar ko'payib yuk oshadi | Retry faqat eng chetki qatlamda, idempotency key bilan |
| Konfiguratsiya 6 ta profil ichida takrorlanadi | Qaysi qiymat ishlayotgani noma'lum | Bitta asosiy fayl, profil faqat farqni override qiladi |
| Ko'p mayda servis bitta tranzaksiyani bo'ladi | Taqsimlangan nomuvofiqlik, qo'lda tuzatish | Tranzaksiya chegarasini bitta servisga qaytarish |
| Qarz hech qayerda yozilmagan | Har yangi odam uni qaytadan kashf qiladi | ADR va kodda `// QARZ: shart, muddat, ega` izohi |

## 6.7 Murakkablikni o'lchash: o'zgarish vaqti, incident soni, yangi odam vaqti

Murakkablikni "chiroyli emas" degan his bilan himoya qilib bo'lmaydi, raqam kerak. Uchta metrika amalda ishlaydi. Birinchisi o'zgarish vaqti: oddiy talab (masalan yangi to'lov usuli qo'shish) uchun idea'dan production'gacha necha kun ketadi. Ikkinchisi incident soni va ularning taqsimoti: qaysi modul oyiga nechta incident beradi. Uchinchisi yangi odam vaqti: yangi developer birinchi mustaqil PR'ini qancha vaqtda yuboradi.

Mo'ljal raqamlari: kichik o'zgarish uchun lead time 1-3 kun, deploy chastotasi kuniga kamida bir marta, change failure rate 15 foizdan past, yangi odamning birinchi PR'i 3-5 ish kuni. Agar yangi odam ikki haftada ham mustaqil PR yubora olmasa, bu tizim murakkabligining to'g'ridan-to'g'ri o'lchovi.

Kodga tegishli yordamchi signal: churn va bog'lanish. Oyiga 30 martadan ko'p o'zgaradigan va 40 ta boshqa klassga bog'langan fayl keyingi incident manbai. Bunday fayllarni git tarixidan topish oson, va u sub'ektiv bahsni ma'lumotga aylantiradi.

```bash
# Eng ko'p o'zgargan fayllar: murakkablik issiq nuqtalari
git log --since="6 months ago" --name-only --pretty=format: \
  | grep '\.java$' | sort | uniq -c | sort -rn | head -15

# Bitta fayl ustida nechta odam ishlagan: egasi noaniq modul belgisi
git log --since="6 months ago" --format='%an' -- \
  src/main/java/com/shop/order/OrderService.java | sort -u | wc -l
```

| Mavzu | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Yangi talab | Mavjud servisga yana bitta `if` qo'shish | Shart domen metodiga nom bilan ko'chiriladi, holat soni hisoblanadi |
| Holat | Entity har joyda o'zgartiriladi | O'zgarish aggregate ichida, tashqariga immutable record chiqadi |
| Konfiguratsiya | Yangi ehtiyojga yangi flag | Flag egasi, o'lim sanasi va kombinatsiya narxi yoziladi |
| Abstraksiya | Kelajak uchun oldindan interfeys | Uchinchi real foydalanuvchi paydo bo'lganda chiqariladi |
| Eski kod | "Tegmaymiz, ishlayapti" | Telemetriya bilan o'likligi tasdiqlanadi va bosqichli o'chiriladi |
| Texnik qarz | Backlog'da nomsiz ticket | ADR: shart, narx, qaytish mezoni va muddat |
| Servis ajratish | Modul katta bo'ldi, ajratamiz | Avval modul chegarasi, ajratish faqat alohida masshtab yoki SLA uchun |
| O'lchov | "Kod chigal" degan his | Lead time, incident taqsimoti, yangi odam vaqti raqamda |
| Integratsiya | `try/catch (Exception e)` | Timeout, noaniq holat va idempotency alohida modellashtiriladi |
| Qaror | Eng yangi texnologiya tanlanadi | Operatsion narx va jamoa tajribasi hisobga olinadi |

## 6.8 Servislar soni va operatsion murakkablik narxi

Har bir yangi servis kod emas, operatsion birlik qo'shadi. Unga pipeline, sekretlar, monitoring, alert, on-call egasi, versiya yangilash jadvali va migratsiya mexanizmi kerak. Taxminiy hisob: bitta servisni "bor" holatda saqlash yiliga bir muhandisning 10-15 foiz vaqtini oladi, hech qanday yangi funksiya qo'shilmasa ham.

Ikkinchi narx chaqiruv zanjirida. Agar bitta tashqi so'rov ketma-ket beshta servisdan o'tsa va har biri 99.9 foiz mavjud bo'lsa, umumiy mavjudlik taxminan 99.5 foizga tushadi. Latency ham qo'shiladi: har bir hop tarmoq va serializatsiya uchun taxminan 1-5 ms, ichki retry bo'lsa ko'proq. Sinxron zanjirni qisqartirish eng arzon performance optimizatsiyasi.

Uchinchi narx ma'lumotda. Bitta tranzaksiya ikki servisga bo'linsa, siz ACID'dan voz kechib eventual consistency olasiz. Buning o'rnini outbox, kompensatsiya va reconciliation job to'ldiradi, ya'ni uchta yangi mexanizm (tafsiloti dizayn [patternlar hujjatidagi](../patterns/README.md) outbox va saga bo'limlarida). Shu sababli servis chegarasi birinchi navbatda tranzaksiya chegarasiga qarab tanlanadi, kod hajmiga qarab emas.

Praktik yo'l: modular monolit bilan boshlash. Modul chegarasini kodda majburlash, ma'lumotlar bazasida sxema bilan ajratish, keyin faqat haqiqiy sabab bo'lganda ajratish. Haqiqiy sabab uchta: alohida masshtab profili, alohida ishonchlilik talabi, alohida release tezligi. "Jamoa alohida" ham sabab, lekin faqat jamoa 6-8 odamdan oshganda.

```java
// Modul chegarasini testda majburlash: kelajakdagi ajratishni arzon qiladi
@AnalyzeClasses(packages = "com.shop", importOptions = DoNotIncludeTests.class)
class ModuleRulesTest {

    // Ombor moduli to'lov modulining ichki klasslariga bog'lanmasin
    @ArchTest
    static final ArchRule chegara = noClasses()
            .that().resideInAPackage("..inventory..")
            .should().dependOnClassesThat()
            .resideInAPackage("..payment.internal..");

    // Domen qatlami Spring web'ga bog'lanmasin
    @ArchTest
    static final ArchRule domenMustaqil = noClasses()
            .that().resideInAPackage("..domain..")
            .should().dependOnClassesThat()
            .resideInAPackage("org.springframework.web..");
}
```

## 6.9 Umumiylashtirish tuzog'i: uchta foydalanuvchiga mo'ljallangan platforma

Eng qimmat murakkablik yaxshi niyatdan keladi. Jamoa ikkinchi mijoz uchun shunga o'xshash xususiyat so'raganini ko'radi va "keling, umumiy platforma qilamiz" deydi. Natijada ikki holatni qoplaydigan abstraksiya tug'iladi, lekin u uchinchi holatni qoplamaydi, chunki uchinchi holat hali ma'lum emas.

Qoida sodda: ikkita o'xshash joy takrorlanish emas. Uchinchi real holat paydo bo'lgandan keyin abstraksiya chiqarilsa, u haqiqiy o'zgaruvchanlik o'qini ko'radi. Undan oldin chiqarilgan abstraksiya tasodifiy o'q tanlaydi va keyin har yangi talab unga `if` qo'shib buziladi.

Ikkinchi belgi: parametr soni. Agar "umumiy" metod sakkizta argument, uchta enum va bitta `Map<String, Object>` olsa, u umumiy emas, u uchta alohida metodning ustiga tashlangan plash. Bunday holatda plashni yechib, uchta aniq nomli metod qoldirish kodni uzaytiradi, lekin murakkablikni kamaytiradi.

```java
// Erta umumiylashtirish: nima bo'layotgani o'qilmaydi
report.generate("ORDERS", Map.of("from", from, "to", to,
        "groupBy", "WAREHOUSE", "includeVat", true, "format", "XLSX"));

// Uchta aniq yo'l: har biri o'z testi va o'z SQL'i bilan
OrdersByWarehouseReport r1 = reports.ordersByWarehouse(from, to);
VatSummaryReport       r2 = reports.vatSummary(from, to);
StockSnapshotReport    r3 = reports.stockSnapshot(asOf);
```

Takrorlanishning o'zi ham narx, shuni inkor qilmaymiz. Farq shundaki, takrorlangan kodni birlashtirish keyinroq oson, noto'g'ri abstraksiyani yechish esa qiyin. Shu sababli tanlov nosimmetrik: shubha bo'lsa, takrorlanishni qoldiring.

## 6.10 Murakkablikni jamoaga tushuntirish va qarorni himoya qilish

Murakkablikni kamaytirish taklifi deyarli har doim "bu biznes qiymati bermaydi" degan e'tirozga uchraydi. Javob his bilan emas, narx bilan beriladi. "Bu modul oxirgi chorakda 7 ta incident berdi, har biri o'rtacha 4 soat ishni oldi, va unga tegadigan o'zgarish o'rtacha 9 kun ketadi" degan gap bahsni tugatadi.

Taklifni uchta ustunda bering. Birinchisi hozirgi narx raqamda. Ikkinchisi taklif va uning hajmi (masalan ikki hafta, bitta developer). Uchinchisi natija qanday o'lchanadi (lead time 9 kundan 3 kunga, incident oyiga 2 dan 0-1 ga). Agar uchinchi ustunni yozolmasangiz, taklif hali tayyor emas.

Bir vaqtda hamma narsani tozalashni so'ramang. Issiq nuqta ro'yxatidan eng qimmat bittasini tanlang va uni oqim ichida qiling: har bir funksional ishga 20 foiz tozalash qo'shing. Bu rejani buzmaydi va bir chorakda sezilarli natija beradi.

Teskari yo'nalishni ham unutmang. Ba'zan to'g'ri qaror murakkablikni ataylab qabul qilish: to'lovda idempotency, reconciliation va audit log kerak, chunki pul yo'qolishining narxi kodning chiroyliligidan baland. Arxitektorning mahorati murakkablikni yo'qotishda emas, uni qayerga qo'yishni tanlashda.

## 6.11 Amalda qo'llash

- [ ] Eng ko'p incident bergan uch modulni aniqlang va har biri uchun lead time hamda incident sonini raqamda yozib qo'ying.
- [ ] Git tarixidan oxirgi 6 oyda eng ko'p o'zgargan 15 faylni chiqarib, ularning bog'lanish sonini tekshiring va ikkitasini bo'lishni rejalashtiring.
- [ ] Barcha feature flag'larni ro'yxatga oling, har biriga ega va `remove-after` sanasi qo'shing, muddati o'tganlarini kod bilan birga o'chiring.
- [ ] Bitta muhim oqimdagi (masalan buyurtmani to'lash) tashqi chaqiruvlarni sanab chiqing va har biri uchun timeout, retry va noaniq holat qanday modellashtirilganini yozing.
- [ ] Bitta servisda `@Value` bilan tarqalgan sozlamalarni tipli `@ConfigurationProperties` record'ga yig'ib, validatsiya qo'shing.
- [ ] `pg_stat_user_indexes` va `pg_stat_user_tables` asosida o'lik indeks va jadvallar ro'yxatini tuzing, statistika yig'ilgan muddatni tekshirib, bosqichli o'chirish rejasini yozing.
- [ ] Modul chegaralari uchun kamida uchta ArchUnit qoidasi qo'shib, ularni CI darvozasiga ulang.
- [ ] Mavjud eng katta nomsiz texnik qarz uchun ADR yozing: shart, narx, qaytish mezoni va muddat.

---

[&larr; 5. Abstraksiya hissi, bog'liqlik va chegaralar](05-abstraksiya-hissi-bogliqlik-va-chegaralar.md) · [Mundarija](README.md) · [7. Nosozlik haqida fikrlash &rarr;](07-nosozlik-haqida-fikrlash.md)
