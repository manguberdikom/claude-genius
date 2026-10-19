<!-- doc: architect | chapter: 6 | part: I. Fikrlash va qarorlar -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 6. Murakkablikni boshqarish (Managing Complexity)

<details>
<summary>Bu bobdagi 17 bo'lim</summary>

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
- [6.11 Arxitektura qarzi: eskirgan qaror qanday sekinlashtiradi](#611-arxitektura-qarzi-eskirgan-qaror-qanday-sekinlashtiradi)
- [6.12 Umumiylashtirish qachon chuqurlashtiradi: interfeys umumiy, funksionallik hozirgi ehtiyoj bo'yicha](#612-umumiylashtirish-qachon-chuqurlashtiradi-interfeys-umumiy-funksionallik-hozirgi-ehtiyoj-boyicha)
- [6.13 Murakkablikni pastga tortishning chegarasi: modul hamma qarorni o'ziga olmasin](#613-murakkablikni-pastga-tortishning-chegarasi-modul-hamma-qarorni-oziga-olmasin)
- [6.14 Inkrement birligi: xususiyat emas, abstraksiya](#614-inkrement-birligi-xususiyat-emas-abstraksiya)
- [6.15 Dizayn jarayonining nomukammalligi: wicked problem va qo'pol yechim](#615-dizayn-jarayonining-nomukammalligi-wicked-problem-va-qopol-yechim)
- [6.16 Lokal dasturchi tajribasi: bitta noutbukda nechta servis ko'tariladi](#616-lokal-dasturchi-tajribasi-bitta-noutbukda-nechta-servis-kotariladi)
- [6.17 Amalda qo'llash](#617-amalda-qollash)

</details>



Arxitektorning asosiy ishi tezlik emas, murakkablikni boshqarish. Kod ishlayotgan holatda ham tizim o'lishi mumkin, chunki uni o'zgartirish narxi daromaddan oshib ketadi. Shu bobda murakkablik qayerdan kelib chiqadi, qanday o'lchanadi va uni kamaytiradigan qarorlar qanday himoya qilinadi degan savollarga javob beramiz. Misollar bitta tizimdan olinadi: to'lov servisi, buyurtma oqimi va ombor qoldig'i.

## 6.1 Muhim murakkablik va tasodifiy murakkablik farqi

Muhim murakkablik (essential) biznesning o'zidan keladi. Ombor qoldig'i rezervatsiya, bekor qilish, qaytarish va inventarizatsiya hisobiga o'zgaradi, va bu to'rt oqim bir-biri bilan kesishadi. Bu murakkablikni butunlay yo'qotib bo'lmaydi, uni ko'chirish mumkin: kodga, ma'lumotlar modeliga yoki operator qo'llanmasiga. Bir eslatma: *Code Complete* bu ajratishni bergan joyda muhim murakkablikni ham MINIMALLASHTIRISH kerakligini aytadi, ya'ni "muhim" degani "tegmaslik kerak" degani emas - domenni soddalashtirish bo'yicha biznes bilan suhbat ham arxitektorning ishi.

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

Oldin murakkablikni QANDAY sezish mumkinligini aytib olaylik, chunki bu joyni topishdan oson. Ousterhout murakkablikning uch belgisini sanaydi va ular amalda tashxis savoli sifatida ishlaydi. **Change amplification**: oddiy ko'rinadigan o'zgarish uchun ko'p joyni tahrirlash kerak. **Cognitive load**: biror narsani o'zgartirish uchun qancha bilim boshda bo'lishi kerak. **Unknown unknowns**: qaysi kodga tegish kerakligini oldindan bilish umuman imkonsiz - Ousterhout shu uchinchisini eng yomoni deb ataydi, chunki boshqa ikkisini hech bo'lmaganda o'lchash mumkin, buni esa faqat production'da bilib olasiz. Sabablarni esa u ikkiga qaytaradi: bog'liqlik (dependency) va noaniqlik (obscurity).

Shu ramkada quyidagi uchta joy - shart, holat, integratsiya - murakkablik TO'PLANADIGAN joylar. Bu taqsimot shu korpusning amaliy ajratishi, kitob ta'rifi emas, lekin yuqoridagi uch belgi bilan birga ishlaganda tashxis aniq bo'ladi. Birinchi joy shartlar. Har bir `if` ikkita yo'l hosil qiladi, ketma-ket beshta mustaqil shart esa nazariy jihatdan 32 holat beradi. Amalda ularning yarmi hech qachon test qilinmaydi va aynan shu yarmidan incident chiqadi.

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

Ousterhout bu mavzuda boshqa boblardan keskinroq turadi va uni bilib qo'yish foydali: konfiguratsiya parametri qo'shish murakkablikni YUQORIGA, foydalanuvchiga suradi, va ko'pincha bu "oson bahona" bo'ladi - modul to'g'ri qiymatni o'zi aniqlashi kerak bo'lgan joyda, mas'uliyat tashqariga chiqariladi. Uning misoli aynan shu bobdagi mavzuga tegadi: protokol retry intervalini foydalanuvchidan so'ramasligi, o'zi hisoblashi kerak. Shuning uchun har bir yangi flag uchun savol bitta: bu qiymatni ilovaning o'zi runtime'da aniqlay oladimi? Agar ha, flag kerak emas.

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

Ikkinchi qoida konfiguratsiyaning qayerda yashashi haqida. Fairbanks komponent konfiguratsiyasini bajariladigan koddan deklarativ konfiguratsiya fayliga chiqarishni tavsiya qiladi va sababi tahlilga tegishli: manba kodini statik tahlil qilish mumkin, lekin bu qiyin ish, deklarativ konfiguratsiya faylini tahlil qilish esa oson. Ya'ni "qaysi komponent qaysi komponentga ulangan" savoliga javob kodni o'qimasdan chiqadi. Spring da bu amalda `@Bean` metodlari ichida shartli mantiq yozish va `if (env.equals("prod"))` ko'rinishidagi tarmoqlanish o'rniga `@ConditionalOnProperty`, profil fayllari va `application-<profil>.yml` ishlatishni bildiradi. Chegarasi ham bor: deklarativ fayl kod bilan tekshirilmaydi, shuning uchun uning o'rnini yuqoridagi tipli `@ConfigurationProperties` bilan validatsiya to'ldiradi.

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

O'chirishdan arzonroq yo'l esa kodni umuman yozmaslik, va bu uchun uch qoida bor.

**Kod aktiv emas, majburiyat.** *Software Engineering at Google* ning formulasi aniq: kodning o'zi majburiyat, ehtimol zarur majburiyat, lekin o'z-o'zidan kelgusida kimgadir tushadigan texnik xizmat vazifasi; samolyot ko'tarib yuradigan yonilg'i kabi, uning og'irligi bor. Shundan ikki amaliy qoida chiqadi. Birinchisi, yangi xususiyat yozishdan oldin uning haqiqatan kerakligi tekshiriladi. Ikkinchisi, dublikat kod shunchaki behuda mehnat emas, u kodning umuman bo'lmasligidan ham qimmatroq tushishi mumkin: bitta shaklda oson bajariladigan o'zgarish kod bazasida takrorlanish bo'lsa ko'proq kuch talab qiladi. Kitob bu fikrni utility va kutubxona kodiga ayniqsa qattiq qo'llaydi: yirik kod bazasida sizdan avval kimdir o'xshash narsa qilgan bo'lish ehtimoli yuqori, shuning uchun qidirish asbobi dublikatni topish va oldini olish uchun hayotiy. Google dagi maqol ham shu haqda: "noldan yozayotgan bo'lsangiz, noto'g'ri qilayotgansiz".

**Ishlatilmaydigan xususiyat o'chiriladi.** Xususiyatning narxi va qiymati u ishlab turganda kuzatiladi, va bu uchun reliz muhandisligi qoidasi nomlangan: ship only what gets used. Ishlatilmaydigan xususiyat build vaqtiga, deploy hajmiga va foydalanuvchi qurilmasidagi resursga xarajat qo'shadi, ya'ni nol foyda bilan doimiy narx beradi. Qaror esa his bilan emas, A/B tajriba bilan muvozanatlanadi: xususiyatning narxi va foydasi o'lchanib taqqoslanadi.

**Ba'zan dastur umuman yozilmaydi.** Boswell va Foucher bir martalik vazifa uchun kod yozishni ochiq tanqid qiladi va misol beradi: web server access log idan eng ko'p 4xx va 5xx xato beradigan URL larni topish. C++ yoki Java da bu oson 20 qator oladi. Unix da esa bitta buyruq quvuri bo'ladi, va kitobning e'tibor qaratgan nuqtasi natija emas: hech qanday "haqiqiy" kod yozilmadi va manba nazoratiga hech narsa qo'shilmadi, demak tekshiruv, review va texnik xizmat yuki ham qolmadi (13-bob, 144-145-betlar).

```bash
# Log tahlili uchun dastur yozilmaydi: 20 qator kod o'rniga bitta quvur.
cat access.log | awk '{ print $5 " " $7 }' | egrep "[45]..$" \
  | sort | uniq -c | sort -nr
```

Chegara ham ochiq: bu qoida bir martalik tahlil uchun. Takrorlanadigan va boshqalar tayanadigan ish uchun quvur noto'g'ri yechim bo'ladi, chunki unda test ham, xato ishlovi ham yo'q. Mezon shu: natija bir marta kerakmi yoki u kelgusida kimningdir ishiga asos bo'ladimi.

## 6.6 Texnik qarz: ongli qarz va tasodifiy loyqalik

Qarzning ikki turi bor va ular bilan muomala butunlay boshqacha. Ongli qarz qaror bilan olinadi: "Qora juma oldidan hisobotni to'g'ri modellashtirishga vaqt yo'q, vaqtinchalik SQL view bilan chiqaramiz, yanvarda qaytamiz". Bunda shart ma'lum, muddat ma'lum, egasi ma'lum.

Tasodifiy loyqalik hech qanday qaror bilan olinmagan. U shunchaki paydo bo'ladi: nomlash buzilgan, qatlam chegarasi yo'q, bitta servis ikki xil tranzaksiya modelini ishlatadi. Bu turdagi qarz foizi yuqori, chunki uning mavjudligini hech kim bilmaydi.

Shuni bilib qo'ying: "texnik qarz" atamasi bu yerda shu korpusning tili, Ousterhout uni ishlatmaydi. Uning ramkasida muammo taktik dasturlash deb ataladi va u "taktik bo'ron" (tactical tornado) figurasini keskin tanqid qiladi: tez ishlaydigan, lekin har safar murakkablik qoldirib ketadigan muhandis tashkilotda ko'pincha samarali deb qabul qilinadi, aslida esa qarzni boshqalar to'laydi. Ousterhout murakkablik bosqichma-bosqich o'sishini (complexity is incremental) alohida ta'kidlaydi: bitta qaror hech qachon halokatli ko'rinmaydi, yig'indisi esa halokatli bo'ladi.

Arxitektor vazifasi loyqalikni ongli qarzga aylantirish. Bu ADR (arxitektura qaror yozuvi) orqali qilinadi: muammo, variantlar, tanlangan yo'l, narxi va qaytish sharti yoziladi. Qaytish sharti eng muhim qism, chunki u "bir kun kelib tozalaymiz" degan gapni o'lchanadigan narsaga aylantiradi. Masalan: "kunlik hisobot 90 sekunddan oshsa, yoki jadval 50 mln qatordan o'tsa, read model kiritiladi".

Startap sharoiti bu qarorga alohida bosim beradi, va Ousterhout bosimni nomlab, javobini ham beradi. Erta bosqichdagi kompaniyada birinchi relizni tez chiqarish zarurati shunchalik kuchli ko'rinadi, hatto 10-20 foizlik investitsiya ham ko'tarib bo'lmaydigan narx bo'lib tuyuladi; o'rniga taktik yo'l tanlanadi va "muvaffaqiyat kelsa, tozalashga qo'shimcha muhandis yollaymiz" degan fikr bilan asoslanadi. Kitobning uch qarshi dalili bor. Birinchi: kod bazasi spagettiga aylangandan keyin uni tuzatish deyarli imkonsiz va yuqori ishlab chiqish narxi mahsulotning butun umri davomida to'lanadi. Ikkinchi: yaxshi yoki yomon dizaynning natijasi tez ko'rinadi, shuning uchun taktik yo'l hatto birinchi relizni ham tezlashtirmasligi ehtimoli katta. Uchinchi: eng kuchli muhandislar dizaynga e'tibor beradi, kod bazasi buzuq degan gap tarqalsa yollash qiyinlashadi, natijada o'rtamiyona jamoa qoladi va tuzilish yana yemiriladi. Kitob "tez yur va buz" (move fast and break things) shiorini aynan shu misolda ko'rib chiqadi: o'sha madaniyat bilan kompaniya juda muvaffaqiyatli bo'lgan, lekin kodi beqaror, izohsiz va testsiz bo'lib qolgan va keyinchalik shior "mustahkam infratuzilma bilan tez yur" ga o'zgargan. Teskari misol ham bor: taxminan shu davrda strategik yondashuvni tanlagan kompaniyalarning texnik madaniyati ularga eng kuchli muhandislarni yollashda ustunlik bergan. Kitobning xulosasi ehtiyotkor, ikki yo'l bilan ham muvaffaqiyat qozonish mumkin, demak bu prognoz emas, narx haqidagi dalil.

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

Ta'rifning o'zi ham aniqlanishi kerak, chunki "qarz" so'zi ko'pincha "kod chiroyli emas" degan hissiyot bilan almashtiriladi. Fairbanks Ward Cunningham ning ta'rifini keltiradi va u ancha aniqroq: texnik qarz bu kodning muammo haqidagi **joriy tushunchaga** nisbatan to'plangan nomuvofiqligi. Ya'ni mezon kodning go'zalligi emas, modelning bugungi eng yaxshi tushunchasi bilan kodda ifodalangan model orasidagi farq (divergence). Ta'rifning foydasi amaliy: model kodda ifodalangan bo'lsa, qarzni "kod xunuklashmoqda" degan ichki sezgi orqali emas, modelni kod bilan solishtirib aniq topish mumkin, ya'ni qaysi qism tuzatishga muhtojligi nomlanadi. Bu [5.21](05-abstraksiya-hissi-bogliqlik-va-chegaralar.md#521-har-darajada-hikoya-ierarxiya-element-soni-va-domen-otlari) dagi model-in-code printsipining to'g'ridan to'g'ri natijasi. Kitob ta'rifni domen modelidan tashqariga ham kengaytiradi: bazaning yangi versiyasiga o'tmaslik kabi misollar qarz tushunchasini dizaynning boshqa turlariga, arxitektura ham ichida, yoyadi.

Shu ta'rifdan Newman ning kuzatuvi ham chiqadi va u kutilmagan tomondan keladi: qarz faqat shoshilinch yo'l tanlashdan paydo bo'lmaydi. Tizim haqidagi ko'rinish (vision) o'zgarsa, lekin tizimning hamma qismi unga mos kelmasa, mos kelmagan eski qismlar ham yangi qarz manbaiga aylanadi, hech kim hech qanday shortcut qilmagan bo'lsa ham. Arxitektorning ishi shu yerda ikki qismdan iborat: kattaroq rasmga qarab muvozanatni tushunish, va qarz darajasi hamda qayerga aralashish kerakligi haqida qarashga ega bo'lish. Shaklini tashkilot belgilaydi: ba'zi tashkilotda yumshoq yo'l-yo'riq yetadi va jamoalar qarzni o'zi kuzatib, o'zi to'laydi; boshqalarida muntazam ko'rib chiqiladigan qarz jurnali (debt log) kerak bo'ladi. Ikkisining tanlovi [6.10](#610-murakkablikni-jamoaga-tushuntirish-va-qarorni-himoya-qilish) dagi ishonch darajasi bilan bog'liq.

## 6.7 Murakkablikni o'lchash: o'zgarish vaqti, incident soni, yangi odam vaqti

Murakkablikni "chiroyli emas" degan his bilan himoya qilib bo'lmaydi, raqam kerak. Uchta metrika amalda ishlaydi. Birinchisi o'zgarish vaqti: oddiy talab (masalan yangi to'lov usuli qo'shish) uchun idea'dan production'gacha necha kun ketadi. Ikkinchisi incident soni va ularning taqsimoti: qaysi modul oyiga nechta incident beradi. Uchinchisi yangi odam vaqti: yangi developer birinchi mustaqil PR'ini qancha vaqtda yuboradi.

Mo'ljal raqamlari: kichik o'zgarish uchun lead time 1-3 kun, deploy chastotasi kuniga kamida bir marta, change failure rate 15 foizdan past, yangi odamning birinchi PR'i 3-5 ish kuni. Agar yangi odam ikki haftada ham mustaqil PR yubora olmasa, bu tizim murakkabligining to'g'ridan-to'g'ri o'lchovi.

Kodga tegishli yordamchi signal: churn va bog'lanish. Oyiga 30 martadan ko'p o'zgaradigan va 40 ta boshqa klassga bog'langan fayl keyingi incident manbai. Bunday fayllarni git tarixidan topish oson, va u sub'ektiv bahsni ma'lumotga aylantiradi.

Hajmning o'zi ham o'lchov, va bu yerda o'lchangan ma'lumot bor. *Code Complete* loyiha kattaligining nuqsonlarga ta'sirini to'plab, ikki xulosaga keladi. Birinchi, nuqsonning turi o'zgaradi: kichik loyihalarda topilgan xatolarning taxminan 75 foizi konstruksiya, ya'ni kod yozish xatosi; katta loyihalarda bu ulush 50 foizga tushadi va farqni talab hamda arxitektura xatolari egallaydi (ba'zi juda katta loyihalarda esa konstruksiya ulushi baribir 75 foizda qoladi). Ikkinchi va muhimrog'i: zichlikning o'zi o'sadi, ya'ni ikki barobar katta mahsulotda ikki barobardan ko'p xato bo'ladi.

| Loyiha hajmi (kod satri) | Odatiy xato zichligi |
|---|---|
| 2K dan kichik | 1000 satrga 0-25 xato |
| 2K-16K | 1000 satrga 0-40 xato |
| 16K-64K | 1000 satrga 0.5-50 xato |
| 64K-512K | 1000 satrga 2-70 xato |
| 512K va ko'proq | 1000 satrga 4-100 xato |

Kitob bu raqamlarni aniq loyihalardan olingan deb ogohlantiradi va ularni o'z loyihangizga ko'chirishni taklif qilmaydi; sanoat suratida muhim bo'lgan narsa yo'nalish. Juda katta loyihada 1000 satrga to'g'ri keladigan xato soni kichik loyihadagidan to'rt barobarga ko'p bo'lishi mumkin, demak katta loyiha bir xil xato darajasiga erishish uchun ko'proq ishlashi kerak. Arxitektor uchun bu [6.5](#65-kodni-ochirish-eng-kam-baholangan-arxitektura-ishi) va [6.8](#68-servislar-soni-va-operatsion-murakkablik-narxi) qarorlarining asosi: hajmni kamaytirish sifat ishi ham, nafaqat tartib ishi.

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

Chegara qo'yishdan oldin Ousterhout ning asosiy mezonini eslang, chunki u servis darajasida ham, sinf darajasida ham bir xil ishlaydi: **chuqur modul** kuchli funksionallikni sodda interfeys ortida yashiradi, **yuzaki modul** esa interfeysi o'z mazmuniga nisbatan qimmat. Yaxshi modul - interfeysi kichik, ichi katta bo'lgani. Bundan ikki amaliy qoida chiqadi. Birinchisi - **ma'lumotni yashirish** (information hiding): modul o'z qarorini ichida ushlasin, tashqariga chiqarmasin. Ikkinchisi - **murakkablikni pastga tortish** (pull complexity downwards): tanlov bo'lganda qiyin ishni modulning o'zi bajarsin, chaqiruvchiga topshirmasin. Yuzaki mikroservis eng qimmat xato: u tarmoq chaqiruvi, deploy, monitoring va versiyalash narxini oladi, lekin almashtirgan narsasi bitta metod chaqiruvi bo'ladi.

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

Chegaradan nimani chiqarish haqidagi qarorda bitta asimmetriya bor va u tezlikni belgilaydi. Newman uni ochiq aytadi: interfeysga chiqqan narsani qaytarib olish qiyin, lekin bugun yashirilgan narsani keyin istalgan paytda ochish mumkin. Shuning uchun uning o'z yondashuvi modul yoki mikroservis chegarasidan iloji boricha kam narsa ochish. Mantiq Parnas ning axborotni yashirish g'oyasidan keladi: kodning tez o'zgaradigan qismi statik qismidan ajratiladi, chegara barqaror bo'lishi kerak va u modul implementatsiyasining ko'proq o'zgarishi kutiladigan qismlarini yashirishi lozim; shunda modul moslikni saqlagani qadar ichki o'zgarishlar xavfsiz kiritiladi. Amalda bu yangi servis uchun API loyihalashda qo'llanadigan standart: shubha bo'lsa maydon qo'shilmaydi, endpoint ochilmaydi va enum qiymati chiqarilmaydi.

Servislar soni o'sgandan keyin esa teskari muammo paydo bo'ladi: servis bor, lekin uning egasi yo'q. Newman buni egasiz servis (orphaned service) deb ataydi va ikki qarama-qarshi kuchni ajratadi. Bir tomondan, mayda servisning oylar davomida o'zgarmasligi aynan kutilgan natija: mustaqil deploy qilish imkoniyatining jozibasi qolgan tizim barqaror turishida. Boshqa tomondan, agar jamoa tuzilmasi bounded context ga mos bo'lsa, kamdan kam o'zgaradigan servis ham egasiz emas, o'sha kontekstdagi jamoa unga de facto egalik qiladi, va kerak bo'lsa uni qaytadan yozish ham uzoq vaqt olmaydi, chunki mikroservis kichik. Haqiqiy xavf polyglot stek da: jamoa servis yozilgan texnologiyani endi bilmasa, egasiz servisga o'zgarish kiritish qiyinlashadi, va eng og'ir holatda manba kodining qayerda ekani ham ma'lum bo'lmaydi.

Shu muammoni aniqlash uchun Newman ikki vositani keltiradi. Birinchisi metadata reyestri: ba'zi kompaniyalar sodda ichki reyestr qurgan, u manba kodi repozitoriylarini skanerlab metadata fayllarini qidiradi va servislar ro'yxatini yig'adi; bu ma'lumot Consul yoki etcd kabi service discovery tizimidan kelgan haqiqiy ma'lumot bilan birlashtirilsa, nima ishlab turgani va kim bilan gaplashish mumkinligi haqida boyroq rasm chiqadi. Financial Times ning Biz Ops vositasi shu yo'lni eng uzoqqa olib borgan: bir necha yuz servis haqidagi ma'lumotni tarmoq va fayl serverlari kabi boshqa infratuzilma ma'lumoti bilan birga bitta joyda beradi va graf bazasi ustida qurilgani uchun qanday ma'lumot yig'ish va modellashtirishda erkinlik beradi. Ikkinchisi System Operability Score: servis va uning jamoasi servisni oson boshqarilishi uchun bajarishi kerak narsalar ro'yxati ball bilan hisoblanadi, reyestrda to'g'ri ma'lumot berilganidan to health check larning mavjudligigacha; ball ko'rinib turgani uchun jamoa nimani tuzatish kerakligini bir qarashda ko'radi.

| Signal | Qanday o'lchanadi | Qaror |
|---|---|---|
| Servisning repozitoriysi topilmaydi | reyestr skaneri metadata faylini topmaydi | servis ro'yxatga olinadi, egasi izlanadi |
| Discovery da ishlab turgan, reyestrda yo'q | discovery va reyestr farqini solishtirish | ish elementi ochiladi |
| Health check yo'q yoki metadata to'ldirilmagan | operability ball pasayadi | jamoa biriktiriladi yoki ball oshiriladi |
| Jamoa servis texnologiyasini bilmaydi | polyglot steklar ro'yxati va jamoa ko'nikmasi | stekni standartlash yoki servisni qayta yozish |

Bu [6.8](#68-servislar-soni-va-operatsion-murakkablik-narxi) dagi asosiy qoidaning davomi: har yangi servis operatsion birlik, unga on-call egasi kerak, va egalik o'z-o'zidan saqlanmaydi, uni o'lchash kerak.

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

Takrorlanishning o'zi ham narx, shuni inkor qilmaymiz. Farq shundaki, takrorlangan kodni birlashtirish keyinroq oson, noto'g'ri abstraksiyani yechish esa qiyin. Shu sababli tanlov nosimmetrik: shubha bo'lsa, takrorlanishni vaqtincha qoldiring.

Lekin bu qoidani juda uzoqqa olib bormang, chunki adabiyotda teskari pozitsiya ham bor va u kuchli. Ousterhout takrorlanishni "qizil bayroq" deb ataydi: bir xil kod qayta-qayta uchrayotgan bo'lsa, bu siz hali to'g'ri abstraksiyani topmaganingiz belgisi. Ikki pozitsiyani birlashtiradigan amaliy o'rta yo'l shunday: takrorlanishga vaqtincha chidash mumkin, lekin uni NORMA deb qabul qilmaslik kerak. Uchinchi nusxa paydo bo'lganda endi savol "birlashtirsammi?" emas, "qaysi abstraksiyani o'tkazib yubordim?" bo'ladi.

Ziddiyatning to'liq yechimi va ikki pozitsiyani ajratadigan shart [6.12](#612-umumiylashtirish-qachon-chuqurlashtiradi-interfeys-umumiy-funksionallik-hozirgi-ehtiyoj-boyicha) da: bu bo'lim implementatsiyani oldindan umumiy qilish tuzog'i haqida, 6.12 esa yozilayotgan modulning interfeysini umumiy shaklda qo'yish haqida, va ikkisi bir modulda bir vaqtda to'g'ri bo'ladi.

## 6.10 Murakkablikni jamoaga tushuntirish va qarorni himoya qilish

Murakkablikni kamaytirish taklifi deyarli har doim "bu biznes qiymati bermaydi" degan e'tirozga uchraydi. Javob his bilan emas, narx bilan beriladi. "Bu modul oxirgi chorakda 7 ta incident berdi, har biri o'rtacha 4 soat ishni oldi, va unga tegadigan o'zgarish o'rtacha 9 kun ketadi" degan gap bahsni tugatadi.

Taklifni uchta ustunda bering. Birinchisi hozirgi narx raqamda. Ikkinchisi taklif va uning hajmi (masalan ikki hafta, bitta developer). Uchinchisi natija qanday o'lchanadi (lead time 9 kundan 3 kunga, incident oyiga 2 dan 0-1 ga). Agar uchinchi ustunni yozolmasangiz, taklif hali tayyor emas.

Bir vaqtda hamma narsani tozalashni so'ramang. Issiq nuqta ro'yxatidan eng qimmat bittasini tanlang va uni oqim ichida qiling: har bir funksional ishga tozalash ulushini qo'shing. Ousterhout umumiy ish vaqtining 10-20 foizini investitsiya deb ataydi - bu bitta ishga emas, umumiy byudjetga nisbatan o'lchov. Bu rejani buzmaydi va bir chorakda sezilarli natija beradi.

Teskari yo'nalishni ham unutmang. Ba'zan to'g'ri qaror murakkablikni ataylab qabul qilish: to'lovda idempotency, reconciliation va audit log kerak, chunki pul yo'qolishining narxi kodning chiroyliligidan baland. Arxitektorning mahorati murakkablikni yo'qotishda emas, uni qayerga qo'yishni tanlashda.

## 6.11 Arxitektura qarzi: eskirgan qaror qanday sekinlashtiradi

[Texnik qarz](#66-texnik-qarz-ongli-qarz-va-tasodifiy-loyqalik) kod darajasida yig'iladi, arxitektura qarzi esa qaror darajasida. Orosz uni texnik qarzning bir ko'rinishi deb ta'riflaydi: eski arxitektura qarorlari dasturni yoki servisni kengaytirishni, yuritishni, hatto ishlatishni sekinlashtiradi; va hech bir jamoa uni ataylab yaratmaydi, bir paytlar oqilona bo'lgan qaror vaqt o'tib nooptimal bo'lib qoladi (Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 25-bob, 361-bet). Shu sababli bu qarzni axloqiy baho bilan emas, belgilari bilan topish kerak. Orosz to'rt namunani sanaydi.

Birinchisi tezlik uchun ochilgan alohida servislar. Jamoaga yangi funksiya kerak, eng to'g'ri yo'l mavjud backend servisini kengaytirish, lekin uning egasi boshqa jamoa va u o'zgarishga qarshi chiqadi. Jamoa tez chiqish uchun yangi servis quradi va keyingi safar ham shunday qiladi. Vaqt o'tib narxi ko'rinadi: funksiyani o'zgartirish uchun avval qaysi servis ekanini va uning konvensiyasini topish kerak, servislar turli tilda yozilgani kontekst almashtirishni qiyinlashtiradi, va har biri bir xil kutubxonaning turli versiyasiga bog'lanadi; qarz tizimni yuritishdan ko'ra tezlikni ustun qo'yishdan tug'ildi (362-bet). Operatsion narx hisobi [6.8](#68-servislar-soni-va-operatsion-murakkablik-narxi) da.

Ikkinchisi teskari: monolitni ajratmaslik. Boshida bitta kod bazasini bitta birlik qilib deploy qilish oqilona. Jamoa o'sgach og'riq paydo bo'ladi: monolitning ichki tuzilishi yetarlicha mayda bo'lmasa, turli funksiya ustida ishlayotgan odamlar bir xil fayllarda uzoq ishlaydi va merge conflict yechadi; monolit faqat yaxlit deploy qilinsa, deploy vaqti o'sadi va hali chiqarishni xohlamagan jamoa bilan chiqarmoqchi bo'lgan jamoa o'rtasida ziddiyat ehtimoli ortadi (362-bet).

Uchinchisi funksional bo'lmagan xossalarning yemirilishi. Qaror qurilish paytida yaxshi ishlaydi, lekin yuk oshib, use case lar qo'shilgach, unum (latency qabul qilib bo'lmas darajaga chiqadi, CPU yoki xotira sarfi qo'ldan ketadi, throughput yetmaydi), masshtablanish va ishonchlilik seziladigan darajada yomonlashadi (362-363-betlar). Bu turdagi qarzni faqat o'lchov ko'rsatadi, shuning uchun u [murakkablik o'lchovlari](#67-murakkablikni-olchash-ozgarish-vaqti-incident-soni-yangi-odam-vaqti) bilan birga kuzatiladi.

To'rtinchisi eskirgan til yoki framework. Qo'llab-quvvatlanmaydigan versiya xavfsizlik riski va interoperability muammosini keltiradi, ba'zan unumi zamonaviy muqobilidan sezilarli past bo'ladi; almashtirish katta ish, shuning uchun qayta yozish doirasida eski arxitektura qarorlarini ham qayta ko'rish o'rinli. Orosz misol qiladi: Khan Academy Python 2 dan Go ga o'tganda monolitni kichik servislarga bo'lgan va REST endpoint laridan GraphQL ga ko'chgan (363-bet).

Shu yerda qarshi shart bor: eski stack avtomatik ravishda qarz emas. Barqaror, lekin modadan chiqqan framework da kutilmagan to'siq kamroq uchraydi; faol ishlab chiqilayotganida esa boshqa jamoalar duch kelmagan muammoga tushish riski bor. Riskni kamaytirish yo'li sodda: alpha va beta emas, barqaror versiyalarda qolish (363-bet).

## 6.12 Umumiylashtirish qachon chuqurlashtiradi: interfeys umumiy, funksionallik hozirgi ehtiyoj bo'yicha

[6.9](#69-umumiylashtirish-tuzogi-uchta-foydalanuvchiga-moljallangan-platforma) erta umumiylashtirish tuzog'ini yozadi va "uchinchi real holatni kut" deydi. Ousterhout ning P7 printsipi esa teskari tomonda turadi: umumiy maqsadli modullar chuqurroq (general-purpose modules are deeper). Ikki pozitsiya bir xil narsa haqida emas, va ularni ajratadigan shartni kitobning o'zi beradi: modulni "birmuncha umumiy" (somewhat general-purpose) qil, ya'ni **modulning funksionalligi hozirgi ehtiyojni aks ettirsin, interfeysi esa aks ettirmasin**. Interfeys bir nechta ishlatishni ko'taradigan darajada umumiy bo'lishi kerak, lekin bugungi ehtiyoj uchun ishlatishga qulay qolishi shart; "birmuncha" so'zi aynan shuni ushlab turadi.

| Savol | Javob qaysi bo'limda |
|---|---|
| Abstraksiyani qachon chiqarish kerak | 6.9: uchinchi real holat paydo bo'lganda, chunki undan oldin o'zgaruvchanlik o'qi ma'lum emas |
| Chiqarilgan modulning interfeysi qanday shaklda bo'lishi kerak | shu bo'lim: bitta ishlatish uchun ham umumiy shaklda, chunki umumiy interfeys chuqurroq va ma'lumotni yaxshiroq yashiradi |
| Implementatsiya necha holatni qoplashi kerak | faqat bugungi holatni; bu yerda 6.9 ning ogohlantirishi to'liq amal qiladi |

Ya'ni 6.9 implementatsiyani oldindan umumiy qilish haqida (ikki mijozni qoplaydigan platforma, sakkiz argumentli metod va `Map<String, Object>`), bu bo'lim esa yoziladigan modulning interfeys shakli haqida. Bir modulda ikkisi bir vaqtda to'g'ri bo'ladi: implementatsiya bitta holatni qoplaydi, interfeys esa chaqiruvchining atamalarini o'ziga olmaydi.

Kitobning misoli matn tahrirlagich. Talabalar `Text` sinfiga `backspace(Cursor)`, `delete(Cursor)` va `deleteSelection(Selection)` metodlarini yozgan, chunki har biri UI ning bitta tugmasiga mos edi. Natijada `Text` da ko'p sayoz metod paydo bo'lgan, UI atamalari (kursor, tanlov, backspace tugmasi) matn sinfiga oqib o'tgan, va har yangi UI amali `Text` da yangi metod talab qilgan. Umumiy interfeys esa uch metodga tushadi (misol Java ga o'tkazilgan):

```java
public interface Text {
    void insert(Position position, String newText);
    void delete(Position start, Position end);
    Position changePosition(Position position, int charCount);
}

// backspace endi UI tomonida va u nimani o'chirayotgani o'qilib turadi
text.delete(text.changePosition(cursor, -1), cursor);
```

Dalil ikki qismli. Birinchi, bu ma'lumotni yashirishni yaxshilaydi: `Text` endi UI tafsilotini bilmaydi, yangi UI amali `Text` ga tegmasdan qo'shiladi, va UI da ishlayotgan odam uchta sodda metodni o'rganadi, o'n beshtasini emas. Ikkinchi, eski `backspace` metodi yolg'on abstraksiya edi: u qaysi belgi o'chirilishini yashirayotgandek ko'rinadi, lekin UI ga aynan shu ma'lumot kerak, shuning uchun UI developeri baribir `backspace` ning kodini o'qishga boradi. Tafsilot muhim bo'lsa, uni interfeys ortiga yashirish aniqlik bermaydi, loyqalik beradi.

Chegara qayerda? Kitob uchta tekshirish savolini beradi: hozirgi hamma ehtiyojni qoplaydigan eng sodda interfeys qanday; bu metod necha xil holatda ishlatiladi (bitta holat uchun yozilgan metod qizil bayroq); bu API hozirgi ehtiyoj uchun ishlatishga qulaymi. Uchinchi savol 6.9 bilan tutashadigan joy: sinfni bugungi maqsad uchun ishlatish uchun ko'p qo'shimcha kod yozish kerak bo'lsa, umumiylashtirish uzoqqa ketgan. Signal esa o'lchanadigan: metodlar soni kamaygan va har bir metodning API si sodda qolgan bo'lsa, umumiylashtirish to'g'ri; metodlar soni kamaygan, lekin argumentlar soni o'sgan bo'lsa, bu 6.9 dagi plash.

## 6.13 Murakkablikni pastga tortishning chegarasi: modul hamma qarorni o'ziga olmasin

Murakkablikni pastga tortish qoidasi [6.8](#68-servislar-soni-va-operatsion-murakkablik-narxi) da aytilgan: tanlov bo'lganda qiyin ishni modulning o'zi bajarsin, chaqiruvchiga topshirmasin. Ousterhout bu qoidaga alohida bo'lim bilan chek qo'yadi, chunki uni oshirib yuborish oson: chegaraviy holatda butun ilovaning funksionalligi bitta sinfga tortiladi, bu esa aniq ma'nosizlik.

Kitobning uchta sharti bor va ular birgalikda tekshiriladi: (a) pastga tortilayotgan murakkablik sinfning mavjud funksionalligiga yaqin bo'lsin; (b) tortish ilovaning boshqa joylarida ko'p soddalashtirishga olib kelsin; (c) tortish sinfning interfeysini soddalashtirsin. Maqsad tizimning umumiy murakkabligini kamaytirish, bitta sinfni "kuchli" qilish emas.

Kitobning o'z qarshi misoli [6.12](#612-umumiylashtirish-qachon-chuqurlashtiradi-interfeys-umumiy-funksionallik-hozirgi-ehtiyoj-boyicha) dagi matn sinfi: `backspace` metodini `Text` ga qo'yish murakkablikni pastga tortishdek ko'rinadi, lekin yuqori darajadagi kodni deyarli soddalashtirmaydi va UI bilimi matn sinfining asosiy vazifasiga tegishli emas. Natija soddalashtirish emas, ma'lumot oqib chiqishi bo'ladi.

ESLATMA, Spring kontekstidagi quyidagi jadval shu korpusning tarjimasi, kitobdan olingan emas:

| Pastga tortilayotgan narsa | (a) yaqin | (b) yuqorida soddalashtiradi | (c) interfeysni soddalashtiradi | Qaror |
|---|---|---|---|---|
| Repository ichida sahifalash va saralash standart qiymati | ha | ha | ha | torting |
| Aggregate ichida invariant tekshiruvi | ha | ha | ha | torting |
| Repository ichida retry va circuit breaker | yo'q | yo'q | yo'q, sozlama qo'shiladi | tortmang |
| Domen servisi ichida HTTP status kodini tanlash | yo'q | yo'q | yo'q | tortmang |
| Servis metodiga `boolean dryRun` qo'shib ikki xatti-harakat berish | ha | yo'q | yo'q | tortmang |

```java
// Chegaradan o'tgan holat: sinf o'ziga tegishli bo'lmagan qarorni ham oldi
public interface OrderRepository {
    // (c) buzilgan: interfeys sodda bo'lmadi, retry va tenant qarori chiqib qoldi
    List<Order> findRecent(TenantId tenant, int retries, boolean includeCancelled);
}

// Chegarada qolgan holat: qiyin ish ichida, interfeys bitta savolga javob beradi
public interface OrderRepository {
    List<Order> findRecent(OrderQuery query);   // standart qiymatlar va saralash ichida
}
```

## 6.14 Inkrement birligi: xususiyat emas, abstraksiya

Bosqichma-bosqich ishlab chiqish to'g'ri yondashuv, chunki murakkab tizimni boshida yetarlicha aniq ko'rib, eng yaxshi dizaynni tanlab bo'lmaydi. Ousterhout ning qo'shimchasi esa inkrementning birligi haqida va u printsip darajasiga ko'tarilgan (P15): **ishlab chiqish inkrementlari abstraksiyalar bo'lishi kerak, xususiyatlar emas**. Har bir inkrement bir necha yangi abstraksiya qo'shadi va mavjud abstraksiyalarni tajribaga qarab refaktoring qiladi.

Kitob xavfni ham nomlaydi: agile ning bir xavfi taktik dasturlashga olib borishi, chunki u developerlarni abstraksiyalarga emas, xususiyatlarga qaratadi va ishlaydigan dasturni imkon qadar tez chiqarish uchun dizayn qarorlarini keyinga qoldirishni rag'batlantiradi. Bu esa murakkablikning tez to'planishiga olib keladi. Ba'zi agile amaliyotchilarining dalili aynan shunday yangraydi: umumiy maqsadli mexanizmni darhol qurmang, minimal maxsus yechim bilan boshlang va keyin, kerak bo'lgani ma'lum bo'lganda, umumiyroq narsaga refaktoring qiling. Ousterhout bu dalilni ma'lum darajada o'rinli deb tan oladi, lekin u investitsiya yondashuviga qarshi ishlaydi deb hisoblaydi.

Kitobning o'z chizgan chizig'i aniq va u [6.9](#69-umumiylashtirish-tuzogi-uchta-foydalanuvchiga-moljallangan-platforma) bilan ziddiyatda emas: ma'lum bir abstraksiya haqida o'ylashni u xususiyatga kerak bo'lgunicha butunlay qoldirib qo'yish mumkin. Lekin kerak bo'lgan paytda uni toza loyihalashga vaqt sarflash kerak va [6.12](#612-umumiylashtirish-qachon-chuqurlashtiradi-interfeys-umumiy-funksionallik-hozirgi-ehtiyoj-boyicha) ning qoidasi bo'yicha birmuncha umumiy qilish kerak. Ya'ni qoldirish ruxsat etilgan, abstraksiyani umuman chiqarmasdan xususiyatni "tayyor" deb yopish ruxsat etilmagan.

ESLATMA, shu korpusning amaliy shakli: sprint natijasini xususiyat nomi bilan emas, qo'shilgan yoki tozalangan abstraksiya nomi bilan ham yozib qo'yish. "To'lovni Click orqali qabul qilish" xususiyati, "`PaymentProvider` porti va uning ikki implementatsiyasi" esa inkrement. Agar ketma-ket uch sprintda bitta ham yangi yoki tozalangan abstraksiya yo'q bo'lsa, jamoa [6.6](#66-texnik-qarz-ongli-qarz-va-tasodifiy-loyqalik) dagi taktik rejimga o'tgan, va buni retrospektivada raqam bilan ko'rsatish mumkin.

## 6.15 Dizayn jarayonining nomukammalligi: wicked problem va qo'pol yechim

Murakkablikni boshqarish haqidagi bob ikkita noqulay haqiqat bilan yopiladi. Ikkisi ham *Code Complete* ning dizayn bobidan keladi va ikkisi ham arxitektorning rejasini emas, uning kutishini tuzatadi.

**Dizayn "wicked problem".** Horst Rittel va Melvin Webber 1973 yilda "wicked" muammoni shunday ta'riflagan: uni faqat yechib, yoki bir qismini yechib aniq ta'riflash mumkin. Bundan paradoks chiqadi: muammoni aniq ta'riflash uchun uni bir marta "yechish" kerak, keyin esa ishlaydigan yechim qurish uchun uni yana yechish kerak. Kitobning misoli Tacoma Narrows ko'prigi: qurilish paytida asosiy mezon ko'prikning rejalashtirilgan yukni ko'tarishi edi, shamol hosil qilgan yon tomonga garmonik tebranish esa hisobga olinmagan, va 1940 yilda tebranish o'sib ko'prikni yiqitgan. Aerodinamikani shu darajada hisobga olish kerakligi faqat muammo "yechilgandan" keyin ma'lum bo'lgan. Kitob maktab topshirig'i bilan professional ishning farqini ham shu yerda qo'yadi: maktab topshirig'i boshidan oxiriga to'g'ri chiziq bo'lib tuzilgan, professional ishda esa talab siz dizaynni tugatganingizda o'zgaradi. Arxitektor uchun amaliy natija bitta: birinchi tuzilishni tashlab yuborish ehtimolini rejaga kiritish kerak, va shu sababli qaror [6.6](#66-texnik-qarz-ongli-qarz-va-tasodifiy-loyqalik) dagi qaytish sharti bilan birga yoziladi.

**Qo'pol kuch (brute force).** Butler Lampson ning qoidasi kitobda shunday keltirilgan: shubha bo'lsa, qo'pol kuch ishlat. Ishlaydigan qo'pol yechim ishlamaydigan nozik yechimdan yaxshiroq, chunki nozik yechimni ishlaydigan holatga keltirishga uzoq vaqt ketishi mumkin. Kitobning dalili tarixiy: ikkilik qidiruv algoritmining birinchi tavsifi 1946 yilda chop etilgan, lekin hamma hajmdagi ro'yxatlarni to'g'ri qidiradigan algoritm chop etilishiga yana 16 yil ketgan. Ikkilik qidiruv nozikroq, lekin ketma-ket qidiruv ko'p holatda yetarli. Spring kontekstida bu odatda shunday chiqadi: 300 qatorli jadvalni xotiraga olib oddiy tsikl bilan tekshirish, murakkab SQL yoki kesh invalidatsiyasi qurishdan oldin yoziladigan to'g'ri yechim, va uni almashtirish qarori o'lchovdan keyin keladi. Qo'pol yechimning sharti bitta: u [6.6](#66-texnik-qarz-ongli-qarz-va-tasodifiy-loyqalik) ma'nosida ongli qarz bo'lsin, ya'ni qaytish mezoni yozilgan bo'lsin, aks holda u tasodifiy loyqalikka aylanadi.

## 6.16 Lokal dasturchi tajribasi: bitta noutbukda nechta servis ko'tariladi

[Servislar soni](#68-servislar-soni-va-operatsion-murakkablik-narxi) bo'limi operatsion narxni sanadi. Narxning yana bitta qismi odatda hisobga olinmaydi va u JVM stack'ida eng tez seziladi: dasturchining noutbugi. Newman buni ikki kitobida deyarli bir xil yozadi, demak bu kuzatuv emas, qoida. JVM kabi resursga o'ch runtime bitta mashinada ko'tarila oladigan servis sonini cheklaydi, va o'lchov aniq: muallif o'z noutbugida to'rt yoki beshta JVM servisini alohida protsess sifatida ko'tarishi mumkin, o'n yoki yigirmatasini esa ko'tarib bo'lmaydi (Sam Newman, *Building Microservices: Designing Fine-Grained Systems*, 2-nashr, O'Reilly, 2021, 1-bob, "Developer Experience" bo'limi; Sam Newman, *Monolith to Microservices*, O'Reilly, 2019, 5-bob, 222-bet). Resursga kamroq talabchan runtime bilan ham chegara bor, faqat u kechroq keladi: Go, Node yoki Python jamoasi ko'proq servisni lokal ko'tara oladi, JVM jamoasi esa muammoga birinchi duch keladi (*Monolith to Microservices*, 222-bet).

Belgilarni oldindan bilish kerak, chunki ular jim keladi. Kunlik ish sekinlashadi, lokal build va ishga tushirish uzayadi, va dasturchilar kattaroq mashina so'ray boshlaydi; Newman buni qisqa muddatli yechim deb ataydi, chunki servis sonining o'sishi davom etsa, kattaroq mashina faqat vaqt sotib beradi (*Monolith to Microservices*, 223-bet). Yana bir belgi egalik modelidan chiqadi: bir nechta servisga jamoaviy egalik qiladigan jamoalar bu muammoga ko'proq moyil, chunki ular ish paytida servislar orasida almashishi kerak bo'ladi; bir nechta servisga qattiq egalik qiladigan jamoa esa asosan o'z servislari bilan ishlaydi va o'zi nazorat qilmaydigan servislarni stub bilan to'sish mexanizmini o'zi quradi (*Monolith to Microservices*, 223-bet). Bulut servislaridan foydalanilsa va ularni lokal ko'tarib bo'lmasa, holat yana murakkablashadi (*Building Microservices*, 1-bob).

Yechim tanlashda Newman ning pozitsiyasi aniq va u moda yo'nalishiga qarshi. "Bulutda ishlab chiqish" (developing in the cloud), ya'ni dasturchining lokal ishlash imkoniyatidan butunlay voz kechishi u ekstremal yechim deb ataydi va bunga tarafdor emasligini aytadi, chunki qayta aloqa tsikli jiddiy zarar ko'radi; uning o'rniga dasturchi ishlashi kerak bo'lgan qismlarning qamrovini cheklash ancha to'g'ri yo'l, lekin bu jamoaviy egalik modeliga intilayotgan jamoada muammo tug'diradi (*Building Microservices*, 1-bob).

| Yechim | Qanday ishlaydi | Narxi |
| --- | --- | --- |
| Qamrovni cheklash | dasturchi faqat o'z servisi va uning bir-ikki qo'shnisini ko'taradi | jamoaviy egalik modeli bilan to'qnashadi |
| Stub bilan to'sish | ko'tarilmaydigan servislar o'rniga stub qo'yiladi | stub shartnomadan ortda qolishi mumkin |
| Masofaviy nusxaga qaratish | lokal servis boshqa joyda ishlayotgan nusxalarga murojaat qiladi | tarmoq ulanishiga bog'liqlik |
| To'liq masofaviy muhit | hamma narsa kuchli infratuzilmada ishlaydi | ulanish talabi, qayta aloqa tsikli sekinlashadi, muhit resursi va narxi portlashi mumkin |
| Gibrid (lokal plus masofaviy) | servis lokal ishlaydi, chaqiruvlar masofaviy klasterga proxy qilinadi | asbobga bog'liqlik, Kubernetes da Telepresence misoli |

Jadvaldagi variantlar *Monolith to Microservices* ning 223-betidagi matndan yig'ilgan: u yerda stub bilan to'sish yoki boshqa joydagi nusxaga qaratish eng keng tarqalgan usul deb ataladi, to'liq masofaviy muhitning uch narxi (ulanish talabi, sekin qayta aloqa, resurs va xarajat portlashi) sanaladi, va Kubernetes foydalanuvchilari uchun gibrid oqimni osonlashtiradigan Telepresence misol qilib keltiriladi.

Bitta tavsiya ro'yxatdan tashqarida va u o'lchovga tegishli: Newman servis soni o'sgani sayin dasturchi tajribasi qanday o'zgarayotganini ko'rib turish muhim ekanini va buning uchun qayta aloqa mexanizmi qo'yilishi kerakligini aytadi (*Monolith to Microservices*, 223-bet). Amalda bu sprint retrospektivasiga bitta savol qo'shish degani: lokal muhitni ko'tarish bugun qancha vaqt oldi.

Spring tomonida qamrovni cheklash sozlamaga tushadi: o'z servisingizning haqiqiy bog'liqliklari ko'tariladi, qolgan servislar o'rniga stub qo'yiladi.

```yaml
# compose.yaml: faqat shu servisga kerak bo'lgan narsalar ko'tariladi.
# Qo'shni servislar o'rniga WireMock, shunda noutbukda bitta JVM qoladi.
services:
  postgres:
    image: postgres:16.4
    environment:
      POSTGRES_DB: orders
      POSTGRES_USER: order_app
      POSTGRES_PASSWORD: local
    ports: [ "5432:5432" ]

  payment-stub:
    image: wiremock/wiremock:3.9.1
    command: [ "--verbose", "--global-response-templating" ]
    volumes:
      - ./stubs/payment:/home/wiremock
    ports: [ "8081:8080" ]

  inventory-stub:
    image: wiremock/wiremock:3.9.1
    volumes:
      - ./stubs/inventory:/home/wiremock
    ports: [ "8082:8080" ]
```

Stub ning asosiy xavfi shartnomadan ortda qolishi, shuning uchun stub fayllari qo'lda yozilmaydi: ular shartnoma testidan hosil qilinadi yoki real infratuzilma bilan yonma-yon tekshiriladi ([testcontainers asoslari](../testing/08-testcontainers-bilan-real-infratuzilmada.md#82-testcontainers-asoslari-docker-api-ustida-hayot-aylanishi)).

ESLATMA: `compose.yaml` misoli, versiya raqamlari va retrospektiva savoli shu korpusning amaliy tavsiyasi. Kitoblar yechim turlarini sanaydi, aniq konfiguratsiya bermaydi.

## 6.17 Amalda qo'llash

- [ ] Eng ko'p incident bergan uch modulni aniqlang va har biri uchun lead time hamda incident sonini raqamda yozib qo'ying.
- [ ] Git tarixidan oxirgi 6 oyda eng ko'p o'zgargan 15 faylni chiqarib, ularning bog'lanish sonini tekshiring va ikkitasini bo'lishni rejalashtiring.
- [ ] Barcha feature flag'larni ro'yxatga oling, har biriga ega va `remove-after` sanasi qo'shing, muddati o'tganlarini kod bilan birga o'chiring.
- [ ] Bitta muhim oqimdagi (masalan buyurtmani to'lash) tashqi chaqiruvlarni sanab chiqing va har biri uchun timeout, retry va noaniq holat qanday modellashtirilganini yozing.
- [ ] Bitta servisda `@Value` bilan tarqalgan sozlamalarni tipli `@ConfigurationProperties` record'ga yig'ib, validatsiya qo'shing.
- [ ] `pg_stat_user_indexes` va `pg_stat_user_tables` asosida o'lik indeks va jadvallar ro'yxatini tuzing, statistika yig'ilgan muddatni tekshirib, bosqichli o'chirish rejasini yozing.
- [ ] Modul chegaralari uchun kamida uchta ArchUnit qoidasi qo'shib, ularni CI darvozasiga ulang.
- [ ] Mavjud eng katta nomsiz texnik qarz uchun ADR yozing: shart, narx, qaytish mezoni va muddat.

## Manbalar

- John Ousterhout, *A Philosophy of Software Design*, 1-nashr (v1.0), 2018, 2-bob - murakkablikning uch belgisi (change amplification, cognitive load, unknown unknowns) va ikki sababi (dependency, obscurity); murakkablik bosqichma-bosqich o'sishi
- John Ousterhout, *A Philosophy of Software Design*, 1-nashr, 2018, 3-bob, 13-15-betlar - strategik va taktik dasturlash, "taktik bo'ron" figurasi, umumiy vaqtning 10-20 foizini investitsiya qilish
- John Ousterhout, *A Philosophy of Software Design*, 1-nashr, 2018, 4-bob, 22 va 25-betlar - chuqur va yuzaki modul; 5-bob, 29-bet - ma'lumotni yashirish; 8-bob, 55-56-betlar - murakkablikni pastga tortish va konfiguratsiya parametrlari tanqidi
- John Ousterhout, *A Philosophy of Software Design*, 1-nashr, 2018, 6-bob, 39-40-betlar - modulni "birmuncha umumiy" qilish; 9-bob, 62-bet - takrorlanish qizil bayroq sifatida
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 5.2 "Key Design Concepts", 77-79-betlar - muhim va tasodifiy murakkablik, muhim murakkablikni ham minimallashtirish; 5.3, 95-bet - global holat
- Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer BV, 2023, 25-bob, 361-363-betlar - arxitektura qarzining ta'rifi va to'rt namunasi (tezlik uchun ochilgan alohida servislar, monolitni ajratmaslik, funksional bo'lmagan xossalarning yemirilishi, eskirgan til yoki framework), Khan Academy ning Python 2 dan Go ga o'tishi, eski stack avtomatik qarz emasligi va barqaror versiyada qolish qoidasi
- John Ousterhout, *A Philosophy of Software Design*, 1-nashr, Yaknyam Press, 2018, 3.4 - startap sharoitida dizayn investitsiyasi, spagetti kod bazasining butun umr narxi, "tez yur va buz" shiorining tanqidi va dizayn sifatining yollashga ta'siri
- John Ousterhout, *A Philosophy of Software Design*, 1-nashr, Yaknyam Press, 2018, 6.1 va 6.3-6.5, hamda P7 printsipi ("umumiy maqsadli modullar chuqurroq") - funksionallik hozirgi ehtiyoj bo'yicha, interfeys umumiy; umumiylashtirish ma'lumotni yashirishni yaxshilashi; `backspace` yolg'on abstraksiya sifatida; o'zingizga beradigan uchta savol
- John Ousterhout, *A Philosophy of Software Design*, 1-nashr, Yaknyam Press, 2018, 8.3 - murakkablikni pastga tortishning uchta sharti va chegarasi
- John Ousterhout, *A Philosophy of Software Design*, 1-nashr, Yaknyam Press, 2018, 19.2 va P15 printsipi - inkrement birligi abstraksiya bo'lishi, xususiyat emas; agile ning taktik dasturlashga og'ish xavfi; abstraksiyani kerak bo'lgunicha qoldirish mumkinligi
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 5.1 (74-75-betlar) - dizayn "wicked problem" ekani (Rittel va Webber, 1973), Tacoma Narrows ko'prigi misoli, dizayn jarayonining loyqa ekani; 5.3 (107-bet) - qo'pol kuch evristikasi (Lampson) va ikkilik qidiruv tarixi misoli
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 27.3 (651-652-betlar) - loyiha hajmi oshganda xato turining o'zgarishi (kichik loyihada 75 foiz konstruksiya xatosi, kattada 50 foiz) va hajm bo'yicha xato zichligi jadvali
- Sam Newman, *Building Microservices: Designing Fine-Grained Systems*, 2-nashr, O'Reilly, 2021, 1-bob ("Developer Experience" bo'limi) - JVM kabi resursga o'ch runtime bitta dasturchi mashinasida ko'tariladigan servis sonini cheklashi, to'rt yoki beshta JVM servisiga qarshi o'n yoki yigirmata, lokal ko'tarib bo'lmaydigan bulut servislari, "bulutda ishlab chiqish" ga qarshi dalil (qayta aloqa tsikli) va qamrovni cheklash tavsiyasi hamda uning jamoaviy egalik bilan to'qnashuvi. Bu nashrning qo'limizdagi elektron nusxasida barqaror bet raqami yo'q, shuning uchun faqat bob va bo'lim nomi ko'rsatilgan
- Sam Newman, *Monolith to Microservices*, O'Reilly, 2019, 5-bob (222-223) - lokal dasturchi tajribasi: bir xil to'rt yoki beshta JVM servisi o'lchovi, belgilari (lokal build va ishga tushirish uzayishi, kattaroq mashina so'rovi qisqa muddatli yechim ekani), Go, Node va Python jamoalarining chegaraga kechroq yetishi, jamoaviy egalikning moyilligi va qattiq egalikdagi jamoaning stub mexanizmi, yechimlar (stub bilan to'sish, boshqa joydagi nusxaga qaratish, to'liq masofaviy muhit va uning uch narxi, Kubernetes uchun Telepresence gibridi), dasturchi tajribasi uchun qayta aloqa mexanizmi talabi
- Titus Winters, Tom Manshreck, Hyrum Wright (tahr.), *Software Engineering at Google*, O'Reilly, 2020, 9-bob ("Code Is a Liability" bo'limi) - kod majburiyat ekani va samolyot yonilg'isi taqqoslashi, yangi xususiyat haqiqatan kerakligini oldindan tekshirish, dublikat kodning kodning umuman bo'lmasligidan ham qimmat tushishi, utility kodi uchun avval qidirish va "noldan yozayotgan bo'lsangiz, noto'g'ri qilayotgansiz"
- Titus Winters, Tom Manshreck, Hyrum Wright (tahr.), *Software Engineering at Google*, O'Reilly, 2020, 24-bob ("ship only what gets used" xulosasi) - xususiyatning narxi va qiymatini ishlab turganda kuzatish, ishlatilmaydigan xususiyatni olib tashlash va A/B tajriba bilan muvozanatlash
- Dustin Boswell, Trevor Foucher, *The Art of Readable Code*, 1-nashr, O'Reilly, 2011 (copyright 2012), 13-bob (144-145-betlar) - bir martalik log tahlili uchun dastur yozilmasligi, Unix buyruqlari quvuri 20 qatorlik kodni almashtirishi va manba nazoratiga hech narsa qo'shilmagani uchun tekshiruv hamda texnik xizmat yuki qolmasligi
- George Fairbanks, *Just Enough Software Architecture*, 1-nashr, 2010, 9.7 - komponent konfiguratsiyasini bajariladigan koddan deklarativ konfiguratsiya fayliga chiqarish (manba kodini statik tahlil qilish qiyin, deklarativ faylni tahlil qilish oson); 10.5 - Ward Cunningham ning texnik qarz ta'rifi (kodning muammo haqidagi joriy tushunchaga nisbatan to'plangan nomuvofiqligi), divergence ni modelni kod bilan solishtirib topish va ta'rifning arxitekturaga ham yoyilishi
- Sam Newman, *Monolith to Microservices*, 1-nashr, O'Reilly, 2020, 1-bob (18-bet) - modul yoki mikroservis chegarasidan iloji boricha kam narsa ochish, interfeysga chiqqanni qaytarib olish qiyinligi va yashirilganni keyin ochish mumkinligi, Parnas ning axborotni yashirish g'oyasi; 5-bob (233-235-betlar) - egasiz servis muammosi, metadata reyestri (repozitoriy skaneri va service discovery bilan boyitilgan), Financial Times ning Biz Ops vositasi va System Operability Score
- Sam Newman, *Building Microservices: Designing Fine-Grained Systems*, 2-nashr, O'Reilly, 2021, 15-bob ("The Orphaned Service" bo'limi) - mayda servis oylar o'zgarmasligi kutilgan natija ekani, jamoa tuzilmasi bounded context ga mos bo'lsa de facto egalik bo'lishi va qayta yozish arzonligi, hamda polyglot stek da jamoa texnologiyani bilmasa o'zgartirish qiyinlashishi; 16-bob ("Technical Debt" bo'limi) - vision o'zgarganda unga mos kelmaydigan qismlarning yangi qarz bo'lishi, arxitektorning qarz darajasini bilishi, yumshoq yo'l-yo'riq yoki muntazam ko'riladigan debt log tanlovi. Bu nashrning qo'limizdagi elektron nusxasida barqaror bet raqami yo'q, shuning uchun faqat bob va bo'lim nomi ko'rsatilgan
- ESLATMA: 6.4 dagi `@ConditionalOnProperty` va profil fayllari misoli, 6.5 dagi "bir marta kerakmi" mezoni, 6.8 dagi egasiz servis signallari jadvali shu korpusning qo'shimchasi
- ESLATMA: 6.2 dagi uch joy modeli, 6.7 dagi raqamli mo'ljallar (lead time, change failure rate, churn chegaralari), 6.8 dagi mavjudlik hisobi va jamoa o'lchami qoidasi, 6.9 dagi "uchinchi real holat" qoidasi, 6.10 dagi taklif shabloni, 6.13 dagi Spring jadvali 6.14 dagi sprint o'lchovi va 6.16 dagi `compose.yaml` misoli bilan retrospektiva savoli shu korpusning amaliy tavsiyasi, kitobdan olingan emas

---

[&larr; 5. Abstraksiya hissi, bog'liqlik va chegaralar](05-abstraksiya-hissi-bogliqlik-va-chegaralar.md) · [Mundarija](README.md) · [7. Nosozlik haqida fikrlash &rarr;](07-nosozlik-haqida-fikrlash.md)
