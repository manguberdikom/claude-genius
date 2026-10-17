<!-- doc: architect | chapter: 2 | part: I. Fikrlash va qarorlar -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

> Holat: tekshirilmoqda. Da'volar hali manbaga solishtirilmoqda.

# 2. Muammoni tushunish va to'g'ri savol berish (Understanding the Problem)

<details>
<summary>Bu bobdagi 18 bo'lim</summary>

- [2.1 Talab ortidagi haqiqiy ehtiyojni topish](#21-talab-ortidagi-haqiqiy-ehtiyojni-topish)
- [2.2 Funksional va nofunksional talablarni ajratish](#22-funksional-va-nofunksional-talablarni-ajratish)
- [2.3 Noaniq talabni o'lchanadigan talabga aylantirish](#23-noaniq-talabni-olchanadigan-talabga-aylantirish)
- [2.4 Domenni o'rganish: umumiy til va event storming](#24-domenni-organish-umumiy-til-va-event-storming)
- [2.5 Chegaraviy holatlar va istisnolarni oldindan topish](#25-chegaraviy-holatlar-va-istisnolarni-oldindan-topish)
- [2.6 Hajm va o'sish taxmini](#26-hajm-va-osish-taxmini)
- [2.7 Kim foydalanadi: tashqi foydalanuvchi, ichki jamoa, boshqa servis](#27-kim-foydalanadi-tashqi-foydalanuvchi-ichki-jamoa-boshqa-servis)
- [2.8 Muvaffaqiyat mezoni va uni qanday o'lchash](#28-muvaffaqiyat-mezoni-va-uni-qanday-olchash)
- [2.9 Noto'g'ri tushunishning narxi](#29-notogri-tushunishning-narxi)
- [2.10 Talabni rad etish va qamrovni qisqartirish san'ati](#210-talabni-rad-etish-va-qamrovni-qisqartirish-sanati)
- [2.11 Savol birinchi, model ikkinchi](#211-savol-birinchi-model-ikkinchi)
- [2.12 Uch model: domen, dizayn va kod](#212-uch-model-domen-dizayn-va-kod)
- [2.13 Dizayn modeli: chegara modeli va ichki model](#213-dizayn-modeli-chegara-modeli-va-ichki-model)
- [2.14 Model munosabatlari: designation va refinement](#214-model-munosabatlari-designation-va-refinement)
- [2.15 Qaysi model quriladi va qachon tashlab yuboriladi](#215-qaysi-model-quriladi-va-qachon-tashlab-yuboriladi)
- [2.16 Ishni boshlashdan oldin yozma talab va uni tasdiqlash](#216-ishni-boshlashdan-oldin-yozma-talab-va-uni-tasdiqlash)
- [2.17 Tayyorgarlikni o'tkazib yuborish: sabablari, narxi va vaqt ulushi](#217-tayyorgarlikni-otkazib-yuborish-sabablari-narxi-va-vaqt-ulushi)
- [2.18 Amalda qo'llash](#218-amalda-qollash)

</details>



Arxitektorning eng qimmat xatosi kod yozishda emas, talabni tushunishda sodir bo'ladi. McConnell ning jadvali buni raqamda ko'rsatadi: talab bosqichida kiritilgan nuqsonni shu bosqichda topish narxi 1 bo'lsa, uni reliz dan keyin topish narxi 10 dan 100 barobargacha (*Code Complete*, 2-nashr, 3-bob, 29-bet). Shuning uchun arxitektorning ishi klaviaturadan emas, savoldan boshlanadi. Bu bob savolni qanday berish, javobni qanday o'lchanadigan shaklga aylantirish va qachon talabni umuman rad etish kerakligi haqida.

## 2.1 Talab ortidagi haqiqiy ehtiyojni topish

Biznes odatda talabni yechim shaklida aytadi, ehtiyoj shaklida emas. "Bizga hisobot sahifasida Excel eksport tugmasi kerak" degan gap talab emas, bu allaqachon tanlangan yechim. Arxitektor shu yerda to'xtab, "nima uchun" ni so'raydi. Birinchi javob: "chunki moliya bo'limi raqamlarni ko'rishi kerak". Ikkinchi "nima uchun": "chunki ular har oy bank o'tkazmalarini tizimdagi to'lovlar bilan solishtiradi". Uchinchi "nima uchun": "chunki o'tgan yil 400 ming so'mlik farq topilgan va kim javobgar ekani aniqlanmagan".

Mana haqiqiy ehtiyoj: solishtirish (reconciliation) va audit izi. Excel tugmasi uni qondirmaydi, faqat qo'lda ishlashni osonlashtiradi. To'g'ri yechim boshqa: har kuni avtomatik solishtirish, farqlar uchun alohida jadval va to'lov holati o'zgarishining o'zgarmas tarixi. Excel esa ikkinchi darajali xususiyat bo'lib qoladi.

Bu usulning kitobdagi asosi ikkita. Birinchisi Richards va Ford ning ikkinchi qonuni: "nega" "qanday" dan muhimroq (*Fundamentals of Software Architecture*, 1-bob). Ikkinchisi Simon Brown ning talab bilan ishlash tartibi: maqsad talabni o'rganib, uni harakatga keltirayotgan kuchni tushunish, ya'ni "tizim nega mavjud bo'lishi kerak", "yuqori xavfsizlik deganda aynan nimani himoya qilyapmiz" degan savollarga chiqish (*Software Architecture for Developers*, 59-60-betlar). Brown shu yerda savolni suhbatdoshga qarab o'zgartirishni ham tavsiya qiladi.

Fairbanks esa noto'g'ri tushunilgan talabni to'g'ridan-to'g'ri risk deb nomlaydi: "mijoz ehtiyoji tushunilmagan" uning jadvalida loyiha boshqaruvi riski, "noto'g'ri tushunilgan yoki to'liq bo'lmagan sifat atributi talablari" esa keng tarqalgan risk sifatida keltiriladi (*Just Enough Software Architecture*, 3.3-bo'lim).

Qo'shimcha foydali savollar: "hozir buni qanday hal qilib turasiz", "agar biz hech narsa qilmasak nima bo'ladi", "oxirgi marta bu muammo qachon yuz bergan va qancha turdi". Oxirgi savol eng kuchlisi, chunki u talabning narxini oshkor qiladi. Agar javob "aslida hali yuz bermagan" bo'lsa, demak siz hali mavjud bo'lmagan muammoni hal qilmoqchisiz.

## 2.2 Funksional va nofunksional talablarni ajratish

Funksional talab tizim nima qilishini aytadi. Nofunksional talab buni qanday qilishini aytadi. Ikkinchisi arxitekturani birinchisidan ko'ra ko'proq belgilaydi. "Buyurtma yaratiladi" talabi uchun oddiy monolit ham, event-driven tizim ham yaroqli. Lekin "buyurtma yaratish 99 foiz hollarda 200 ms dan tez bo'lsin va ombor servisi o'chganda ham ishlashi kerak" talabi sizni sinxron chaqiruvdan voz kechishga majbur qiladi.

Simon Brown nofunksional talab uchun ikki muqobil nomni ham beradi va ularni yaxshiroq hisoblaydi: tizim xususiyatlari (system characteristics) va sifat atributlari (quality attributes); uning ro'yxatida performance, scalability, availability, security, disaster recovery, accessibility, monitoring, management, audit, flexibility, extensibility, maintainability, huquqiy va tartibga soluvchi talablar, i18n va L10n bor (*Software Architecture for Developers*, 55-58-betlar). O'sha kitobning arxitektura roli bo'limida muammoning sababi aytiladi: loyihalar foydalanuvchidan qanday feature kerakligini so'rashga band bo'lib, qanday nofunksional talab kerakligini kamdan-kam so'raydi (19-bet).

Richards va Ford buning yana bir qatlamini ko'rsatadi: arxitektor va domen manfaatdorlari turli tilda gapiradi. Arxitektor scalability, interoperability, fault tolerance, availability deydi; biznes esa qo'shilish va sotib olish, foydalanuvchi mamnuniyati, bozorga chiqish vaqti, raqobat ustunligi deydi. Ikki tomon bir-birini tushunmaydi va kitob buni "tarjimada yo'qolish" muammosi deb ataydi; chiqish yo'li domen tashvishini sifat atributiga tarjima qiladigan jadval (*Fundamentals of Software Architecture*, 5-bob). O'sha bob ro'yxatni imkon qadar qisqa tutishni va eng muhim uchta atributni tanlashni talab qiladi, chunki har bir qo'shimcha atribut dizaynni murakkablashtiradi.

ESLATMA: pastdagi olti o'lchovli jadval shu korpusning amaliy shakli, kitobdan olingan emas; u Brown ning atributlar ro'yxatini bitta talabga beriladigan savollarga aylantiradi.

| O'lchov | Savol | To'lov servisi uchun misol javob |
|---|---|---|
| Tezlik | Qancha kutish mumkin | p99 < 300 ms, p999 < 1 s |
| Hajm | Kunda necha marta | 80 ming to'lov, peak soatda 12 ming |
| Ishonchlilik | Yo'qolsa nima bo'ladi | Hech bir to'lov yo'qolmasin, takror o'tkazma bo'lmasin |
| Ma'lumot yangiligi | Eski ma'lumot yaraydimi | Balans aniq, hisobot 15 daqiqa kechikishi mumkin |
| Xavfsizlik | Kim ko'rishi mumkin | Karta raqami log'ga tushmasin, PCI doirasi toraytirilsin |
| Narx | Oyiga qancha turadi | Infratuzilma 500 dollardan oshmasin |

"Hech bir to'lov yo'qolmasin" talabi texnik tilga tarjima qilinsa, ikki aniq qarorga olib keladi. Birinchisi: to'lov holati biznes tranzaksiyasi bilan bir atomik yozuvda saqlanadi. Ikkinchisi: tashqi tizimga xabar yuborish o'sha tranzaksiya ichida emas, keyin bajariladi. Bu dizayn [patternlar hujjatidagi](../patterns/README.md) outbox pattern hududi. Arxitektor uni shu yerda nomlaydi, lekin tushuntirib o'tirmaydi.

## 2.3 Noaniq talabni o'lchanadigan talabga aylantirish

"Tez bo'lsin" talabi qabul qilinmaydi, chunki uni hech kim tekshira olmaydi. Simon Brown shunday hujjatni o'z tajribasidan keltiradi: 125 betlik talablar hujjatining oxirgi yarim beti nofunksional talablarga ajratilgan va unda "Performance: tizim tez bo'lishi kerak", "Security: tizim xavfsiz bo'lishi kerak", "Availability: tizim 100 foiz vaqt ishlab turishi kerak" deb yozilgan edi. Uning yechimi: talabga miqdor bog'lash, masalan o'rtacha va pik vaqtda bir vaqtda qancha foydalanuvchi, qanday javob vaqti qabul qilinadi va bu tizimning hamma qismida bir xilmi; miqdor bog'langandan keyin qabul qilish mezoni yozilib, obyektiv test qilish mumkin bo'ladi (*Software Architecture for Developers*, 59-60-betlar).

Fairbanks shu talabni risk tomondan shakllantiradi: riskni kategoriya sifatida, masalan "reliability yetarli emas" deb aytish harakatga keltirmaydi, uni keyin test qilib bo'ladigan nosozlik ssenariysi sifatida yozish kerak, masalan "pik yuk ostida foydalanuvchi interfeysining kechikishi besh sekunddan oshadi" (*Just Enough Software Architecture*, 3.3-bo'lim).

Shu ikki talabni birlashtirsak, o'lchanadigan shakl uchun to'rt narsa kerak: metrika, persentil, qiymat va o'lchash nuqtasi. "Buyurtma yaratish endpoint'i p99 latency'si 300 ms dan kam bo'lsin, server tomonda, 30 daqiqalik oynada, peak trafikda" degan gap allaqachon shartnoma.

Persentilni tanlash muhim va sababi Kleppmann da aniq yozilgan: o'rtacha qiymat "tipik" javob vaqtini bermaydi, chunki bu kechikishni qancha foydalanuvchi sezganini aytmaydi; shu sababli p95, p99 va p999 ishlatiladi (*Designing Data-Intensive Applications*, 1-bob, 14-15-betlar). Hisobda ko'rsak: 1000 so'rovdan 990 tasi 50 ms, 10 tasi 5 s bo'lsa, o'rtacha 99 ms chiqadi va grafik sog'lom ko'rinadi, p99 esa 5 s ko'rsatadi. Kleppmann Amazon ni misol qiladi: ichki servislar uchun talab p999 da qo'yiladi, garchi u mingta so'rovdan bittasiga tegsa ham, chunki eng sekin so'rov egasi odatda akkauntida eng ko'p ma'lumot to'plagan, ya'ni eng qimmatli mijoz; p9999 ni optimallashtirish esa Amazon uchun ham juda qimmat va foydasi kam deb topilgan.

Bitta sahifa bir nechta so'rov qilsa, holat yomonlashadi. Kleppmann buni tail latency amplification deb ataydi: oxirgi foydalanuvchi so'rovi bir nechta backend chaqiruvini talab qilsa, chaqiruvlar parallel bo'lsa ham eng sekinini kutish kerak, shuning uchun sekin chaqiruvga tushish ehtimoli oshadi va sekin sahifalar nisbati ko'payadi (1-bob, 16-bet). Hisobni o'zingiz qilib ko'rishingiz mumkin: 20 ta mustaqil so'rovning hammasi p99 chegarasidan tez bo'lish ehtimoli 0.99 ning 20-darajasi, ya'ni taxminan 0.82, demak sahifalarning taxminan 18 foizida kamida bitta sekin so'rov bo'ladi. Shuning uchun p999 ni ham belgilash kerak.

```yaml
# Spring Boot 3.x: SLO ni metrikaga aylantirish
management:
  endpoints:
    web:
      exposure:
        include: health,metrics,prometheus
  metrics:
    distribution:
      # histogram bo'lmasa persentilni Prometheus tomonda hisoblab bo'lmaydi
      percentiles-histogram:
        http.server.requests: true
      # SLO chegaralari: shu bucket'lar aniq sanaladi
      slo:
        http.server.requests: 100ms,300ms,1s
      # mijoz tomonda ko'rinadigan persentillar
      percentiles:
        http.server.requests: 0.95,0.99,0.999
```

Faqat HTTP latency'ni emas, biznes metrikasini ham o'lchash kerak. "To'lov tasdiqlanishi" bir nechta HTTP so'rovni qamrab oladigan biznes hodisasi.

```java
// To'lov oqimining uchidan uchiga vaqti: biznes SLO si
@Service
public class PaymentConfirmationService {

    private final Timer confirmationTimer;

    public PaymentConfirmationService(MeterRegistry registry) {
        this.confirmationTimer = Timer.builder("payment.confirmation.duration")
                .description("To'lov yaratilgandan tasdiqlangangacha")
                .publishPercentileHistogram()      // persentil uchun zarur
                .serviceLevelObjectives(Duration.ofSeconds(3))
                .register(registry);
    }

    public void onConfirmed(Payment payment) {
        // createdAt biznes hodisasi vaqti, so'rov boshi emas
        Duration elapsed = Duration.between(payment.getCreatedAt(), Instant.now());
        confirmationTimer.record(elapsed);
    }
}
```

O'lchash nuqtasi ham shartnomaning qismi. Kleppmann buni ochiq talab qiladi: yuqori persentillarda javob vaqtining katta qismi navbatda kutishdan keladi va bir nechta sekin so'rov keyingilarini ushlab turadi (head-of-line blocking), shuning uchun javob vaqtini mijoz tomonda ham o'lchash kerak (*Designing Data-Intensive Applications*, 1-bob, 15-16-betlar). Server tomonda o'lchangan qiymat mijoz brauzeridagi qiymatdan past bo'ladi, chunki orada TLS handshake, DNS va mobil tarmoq bor.

Agar biznes "foydalanuvchi uchun tez" desa, budjet qismlarga bo'linadi. Richards va Ford buni performance budget deb ataydi: ilovaning aniq qismlari uchun aniq budjet. Ularning misoli bitta sourced raqam beradi: ko'p tashkilot foydalanuvchi xatti-harakatini o'rganib, birinchi sahifa renderi uchun optimal vaqtni 500 ms deb belgilagan, holbuki ko'p ilova bu metrikada ikki xonali qiymatda turadi; ba'zi tashkilotlar sahifa uchun K-weight budjeti, ya'ni kutubxona va framework larning maksimal bayt hajmini ham qo'yadi (*Fundamentals of Software Architecture*, 6-bob). Server qismiga qancha qolishi shu umumiy budjetdan tarmoq va mijoz qismini ayirish bilan chiqadi; raqamni taxmin qilmasdan, uchidan uchiga o'lchovdan olish kerak.

```bash
# Tezlikni gapirmasdan oldin o'lchab ko'rish: eng arzon tekshiruv
curl -s -o /dev/null -w 'ulanish=%{time_connect}s tls=%{time_appconnect}s \
birinchi_bayt=%{time_starttransfer}s jami=%{time_total}s\n' \
  https://api.internal/orders/42

# Ma'lumotlar bazasi haqiqatan tor joy ekanini tekshirish
# 20 ta parallel ulanish, 60 sekund, faqat o'qish
pgbench -h db-host -U app -d orders -c 20 -j 4 -T 60 -S -P 10
```

## 2.4 Domenni o'rganish: umumiy til va event storming

Kod va suhbat bir xil so'zlardan foydalanmasa, har bir yig'ilish tarjimaga aylanadi. Biznes "yetkazib berish" deganda kod `ShipmentDto` ni, mijoz esa "qachon keladi" ni tushunadi. Umumiy til (ubiquitous language) shu uchlikni bitta so'zga bog'laydi va o'sha so'z klass nomiga aynan tushadi. Atama Eric Evans ning *Domain-Driven Design* kitobidan (2003); Fairbanks uni shunday izohlaydi: turli ekspert bitta tur uchun turli so'z ishlatsa, domen modeli jamoani bitta lug'atga majbur qiladi (*Just Enough Software Architecture*, 8.6-bo'lim). Richards va Ford ham arxitektura atamalaridagi chalkashlikni kamaytirish uchun shu DDD tavsiyasini qo'llashni maslahat beradi (*Fundamentals of Software Architecture*, 4-bob).

Eng ko'p uchraydigan belgi: bitta so'z ikki xil ma'noda ishlatiladi. "Buyurtma" savdo kontekstida savatcha va narx, ombor kontekstida yig'ish ro'yxati, moliyada esa hisob-faktura asosi. Uchalasi bitta `Order` klassiga siqilsa, o'sha klass o'nlab maydonga ega bo'ladi va hech kim uni o'zgartirishga jur'at etmaydi.

To'g'ri qarorni Richards va Ford bounded context orqali ta'riflaydi: DDD dan oldin developerlar tashkilot bo'ylab umumiy entity larni qayta ishlatishga urinardi, lekin umumiy artefakt coupling, koordinatsiya qiyinligi va murakkablik keltiradi; bounded context esa har bir entity o'z lokal kontekstida eng yaxshi ishlashini tan oladi. Kitobning formulasi aniq: tashkilot bo'ylab bitta umumiy `Customer` klassi yaratish o'rniga har bir muammo domeni o'zini yaratadi va farqlar integratsiya nuqtalarida kelishtiriladi (*Fundamentals of Software Architecture*, 7-bob). Demak uch kontekst, uch model, orada aniq tarjima.

```java
// Savdo konteksti: narx va mijoz muhim, ombor joylashuvi yo'q
public record SalesOrder(OrderId id, CustomerId customer,
                         List<OrderLine> lines, Money total) { }

// Ombor konteksti: joylashuv va miqdor muhim, narx yo'q
public record PickingList(OrderId id, WarehouseId warehouse,
                          List<PickTask> tasks, PickPriority priority) { }

// Tarjima faqat bitta joyda: anti-corruption layer
@Component
class SalesToWarehouseTranslator {
    PickingList toPickingList(SalesOrder order, WarehouseId wh) {
        // narx ombor modeliga o'tmaydi, shuning uchun bog'liqlik yo'qoladi
        var tasks = order.lines().stream()
                .map(l -> new PickTask(l.sku(), l.quantity()))
                .toList();
        return new PickingList(order.id(), wh, tasks, PickPriority.NORMAL);
    }
}
```

ESLATMA: quyidagi event storming tartibi shu korpusning amaliy tavsiyasi; yuqorida keltirilgan beshta kitobning hech birida bu usul bayon qilinmagan, shuning uchun uning natijasi haqida raqam berilmaydi. Jarayon oddiy: devorga biznes hodisalarini o'tgan zamonda yozasiz ("to'lov tasdiqlandi", "tovar zahiraga olindi", "yetkazib berish bekor qilindi"), ularni vaqt bo'yicha tartiblaysiz, keyin har bir hodisadan oldin qaysi buyruq va qaysi qoida turganini aniqlaysiz.

Natijada uch narsa ko'rinadi. Hodisalar zich to'planadigan joylar aggregate chegaralarini, oqim uziladigan joylar kontekst va kelajakdagi servis chegaralarini ko'rsatadi. Uchinchisi eng qimmati: hech kim javob bera olmaydigan savollar. Fairbanks shu nuqtani domen modeli orqali aytadi: model "agar men sening kontaktlaringda bo'lsam, sen ham mening kontaktlarimda bo'lishing shartmi" kabi savollarni ochadi; jamoa a'zolari bunday savolga avval turli javob berishi mumkin, lekin domen qanday ishlashi haqida umumiy tushuncha shakllanmasa, dizayn va koddagi xatolar muqarrar (*Just Enough Software Architecture*, 8.6-bo'lim). Demak "to'lov o'tgan, lekin tovar qolmagan bo'lsa nima qilamiz" savoliga javob yo'q bo'lsa, siz hali loyihani boshlashga tayyor emassiz.

## 2.5 Chegaraviy holatlar va istisnolarni oldindan topish

Biznes faqat baxtli oqimni (happy path) aytadi, qolganini arxitektor o'zi sanab chiqadi va har biriga qaror talab qiladi. Chegaraviy holatlar kodning qancha qismini egallashi haqida bu bobda raqam berilmaydi: bunday nisbat yuqoridagi manbalarda o'lchanmagan.

Sanab chiqishning ikki kitobdagi tayanchi bor. Fairbanks domenda bir muddat ishlagandan keyin "prototipik risklar" ko'rinishini aytadi: shu domendagi deyarli har bir loyiha uchraydigan risklar, ular ko'pincha arxitektura ko'riklaridan chiqqan checklist larga yozilgan bo'ladi va tajribasiz developer uchun qimmatli bilim, tajribalisi uchun esa eslatma bo'lib xizmat qiladi (*Just Enough Software Architecture*, 3.3-bo'lim). Fairbanks shu bobda hamma riskni topib bo'lmasligini ham tan oladi: e'tibor oldindan ko'rilgan va yuqori ustuvorlikdagi riskka qaratiladi. Shu sababli sanab chiqilgan holatlar ustuvorlashtiriladi: Richards va Ford ning jadvalida har bir holat ta'sir va ehtimol ko'paytmasi bilan baholanadi va 6 dan 9 gacha bo'lgan holatlar birinchi navbatda yopiladi (*Fundamentals of Software Architecture*, 20-bob).

Ombor qoldig'i misolida sanoq shunday ko'rinadi. Noldan kam qoldiq bo'lishi mumkinmi. Ikki foydalanuvchi oxirgi bitta tovarni bir vaqtda olsa kim yutadi. Tovar zahiraga olingan, lekin to'lov 30 daqiqa kelmasa zahira qachon bo'shaydi. Buyurtma bekor qilingan, lekin tovar allaqachon yig'ilgan bo'lsa qoldiq qanday qaytadi. Inventarizatsiya natijasi tizim raqamidan farq qilsa qaysi biri haqiqat.

Bu savollarning har biri texnik qarorga aylanadi. "Noldan kam bo'lmasin" talabi baza darajasidagi cheklovga aylanadi, chunki faqat ilova kodidagi tekshiruv parallel so'rovlarda ishlamaydi.

```sql
-- Qoldiq manfiy bo'lmasligi: ilova kodiga ishonmaymiz
ALTER TABLE stock_item
  ADD CONSTRAINT stock_item_qty_non_negative
  CHECK (quantity_available >= 0);

-- Parallel kamaytirish: UPDATE o'zi qulflaydi, SELECT keyin UPDATE qilmaymiz
UPDATE stock_item
   SET quantity_available = quantity_available - 3
 WHERE sku = 'SKU-1042'
   AND quantity_available >= 3
RETURNING quantity_available;
-- 0 qator qaytsa, qoldiq yetmagan. Xatoga emas, biznes javobiga aylanadi.

-- Zahira muddati: osilib qolgan rezervlarni topish uchun indeks
CREATE INDEX stock_reservation_expiry_idx
    ON stock_reservation (expires_at)
 WHERE released_at IS NULL;
```

Ikkinchi yondashuv, ya'ni `SELECT` qilib, Java tomonda solishtirib, keyin `UPDATE` qilish, past izolyatsiya darajasida ikki parallel tranzaksiyada ikkisiga ham ruxsat beradi. PostgreSQL ning standart `READ COMMITTED` darajasi buni to'xtatmaydi. Bu mexanika tafsiloti, lekin talab tahlili bosqichida bilinishi kerak, chunki u talabni "oddiy tekshiruv" dan "atomik operatsiya" ga ko'taradi.

## 2.6 Hajm va o'sish taxmini

Har bir talab ortida raqam turadi va u raqam arxitekturani belgilaydi. Kunda 1000 ta buyurtma uchun bitta PostgreSQL instansi va oddiy jadval yetadi. Kunda 5 million buyurtma uchun partitioning, arxivlash va alohida o'qish nusxasi kerak. Bu ikki tizim bir xil kod bilan yozilmaydi.

Taxminni ikki raqam bilan yozish kerak: bugungi va uch yildan keyingi. Uch yil tasodifiy tanlanmagan: Richards va Ford arxitekturaning hayotiyligini aynan "uch yoki undan ko'p yil oldin aniqlangan arxitektura bugun ham yaroqlimi" savoli bilan o'lchaydi (*Fundamentals of Software Architecture*, 1-bob). Tekshirish nuqtasini esa Kleppmann belgilaydi: bitta yuk darajasiga mos arxitektura o'n barobar katta yukni ko'tarishi ehtimoldan uzoq, shuning uchun qayta ko'rish yuk har bir o'n barobar oshganda qilinadi (*Designing Data-Intensive Applications*, 1-bob, 17-bet).

Pikni o'rtachadan ajratish shu yerda ham kerak. Richards va Ford ning misoli: ming talaba va o'n soatlik ro'yxatga olish oynasi berilsa, talabalar vaqt bo'ylab teng tarqaladi deb o'ylash mumkin, lekin domen bilimi hammasi oxirgi o'n daqiqada kelishini aytadi; bunday tafsilot talablar hujjatida kamdan-kam yoziladi, ammo dizaynni belgilaydi (*Fundamentals of Software Architecture*, 5-bob).

```sql
-- Bugungi haqiqat: taxmin qilmasdan o'lchash
SELECT relname AS jadval,
       pg_size_pretty(pg_total_relation_size(c.oid)) AS jami_hajm,
       n_live_tup AS qatorlar
  FROM pg_class c
  JOIN pg_stat_user_tables s ON s.relid = c.oid
 WHERE c.relkind = 'r'
 ORDER BY pg_total_relation_size(c.oid) DESC
 LIMIT 10;

-- Bitta qator qancha joy oladi: o'sishni hisoblash uchun asos
SELECT pg_total_relation_size('payment') / NULLIF(count(*), 0) AS bayt_per_qator
  FROM payment;
```

Hisob o'lchangan raqamdan boshlanadi, taxmindan emas: yuqoridagi so'rov bitta qatorning indekslar bilan qancha bayt olishini beradi. Faraz qilaylik, o'lchov qator uchun 400 bayt chiqardi va kunda 80 ming to'lov bo'lsin. Zanjir shunday: 400 x 80000 = kuniga taxminan 32 MB; 32 MB x 365 = yiliga taxminan 11 GB; uch yil o'sishsiz 33 GB. Agar kunlik hajm uch yil ichida chiziqli uch barobarga chiqsa, yillik qo'shimcha 11, 22 va 33 GB bo'ladi, jami taxminan 66 GB. Bu bitta serverda muammosiz saqlanadi, ya'ni sharding haqida o'ylash shart emas. Lekin sana bo'yicha hisobot so'rovlari bo'lsa, oylik partitioning asoslanadi: eski partitionlar sovuq saqlashga ko'chadi va `VACUUM` ishi engillashadi.

Xotira hisobi ham shunday ishlaydi, shart faqat bitta: har bir ko'paytuvchi yozilgan bo'lsin. 2000 ta sessiya, har biri 20 KB bo'lsa, bu 40 MB heap va muammo emas. Lekin har bir sessiyada 500 elementli savatcha cache'lansa va bitta element 400 bayt olsa, 2000 x 500 x 400 taxminan 400 MB beradi va bu JVM uchun sezilarli. Element hajmi o'lchanadi, chunki hisobning butun natijasi shu ko'paytuvchiga bog'liq.

## 2.7 Kim foydalanadi: tashqi foydalanuvchi, ichki jamoa, boshqa servis

Foydalanuvchi turi API dizaynini, xatolik strategiyasini va mustahkamlik darajasini butunlay o'zgartiradi. Richards va Ford arxitektura katasining majburiy bo'limlari ro'yxatiga "Users", ya'ni kutilayotgan foydalanuvchi soni va turlarini aynan shu sababli kiritadi: bu talablar bilan bir qatorda turadigan mustaqil kirish ma'lumoti (*Fundamentals of Software Architecture*, 5-bob). Simon Brown esa savolni suhbatdoshga qarab o'zgartirishni talab qiladi, chunki bir xil atributga turli manfaatdor turli javob beradi (*Software Architecture for Developers*, 59-bet).

ESLATMA: pastdagi uch iste'molchi bo'yicha taqqoslash shu korpusning amaliy tavsiyasi, kitobdan olingan emas. Bitta endpoint uchun uch xil iste'molchi uch xil talab qo'yadi.

Tashqi mobil ilova sekin tarmoqda ishlaydi, shuning uchun so'rov soni kam, javob kichik va retry ko'p bo'ladi. Bu idempotentlikni majburiy qiladi. Ichki admin paneli trafikni kam beradi, lekin og'ir filtrlar va eksport so'raydi, demak bu so'rovlar o'qish nusxasiga yo'naltiriladi. Boshqa servis sekundda minglab so'rov yuboradi va xatoni ko'rganda darhol qayta urinib tizimni yiqitadi, shuning uchun unga rate limit va aniq xato semantikasi kerak.

```java
// Idempotentlik: tashqi mijoz retry qilsa ikkinchi to'lov yaratilmasin
@PostMapping("/payments")
public ResponseEntity<PaymentResponse> create(
        @RequestHeader("Idempotency-Key") String key,
        @Valid @RequestBody CreatePaymentRequest request) {

    // Kalit bo'yicha unique index bazada: ikkinchi INSERT xato beradi
    var result = paymentService.createOrGet(key, request);

    // Takroriy so'rovga 201 emas, 200 qaytaramiz: mijoz farqni bilsin
    return result.created()
            ? ResponseEntity.status(HttpStatus.CREATED).body(result.payload())
            : ResponseEntity.ok(result.payload());
}
```

Iste'molchi turini bilish versiyalash qarorini ham belgilaydi. Ichki jamoa uchun API ni bugun o'zgartirib, ertaga ikki chaqiruvchini tuzatish mumkin. Tashqi mobil ilova uchun bu imkonsiz, chunki eski versiya telefonlarda yillab yashaydi va majburiy yangilanish mijozni yo'qotadi. Shuning uchun "kim foydalanadi" savoliga javob "tashqi mobil" bo'lsa, orqaga moslik qoidasi birinchi kundan kuchga kiradi.

## 2.8 Muvaffaqiyat mezoni va uni qanday o'lchash

Talab tugagan deb hisoblanishi uchun uch narsa aniq bo'lishi kerak: qaysi raqam o'zgaradi, qancha o'zgaradi va qachon tekshiriladi. "Hisobot tezlashsin" mezon emas. "Oylik moliya hisoboti hozir 14 daqiqa ishlaydi, maqsad 2 daqiqadan kam, 1 million qatorli ma'lumotda, ishga tushirilgandan keyin birinchi oy oxirida o'lchanadi" mezon.

Mezon faqat texnik bo'lmaydi. Biznes mezoni ko'pincha muhimroq. "Qo'lda solishtirish uchun ketadigan vaqt oyiga 16 soatdan 1 soatga tushsin" degan gap loyihaning qiymatini bevosita ko'rsatadi va u loyihani himoya qilish uchun eng yaxshi argument.

Har bir mezonga o'lchash usuli yozilishi kerak, aks holda u shiorga aylanadi. Simon Brown ning shartini eslaymiz: miqdor bog'langandan keyin qabul qilish mezoni yozilib, obyektiv test qilish mumkin bo'ladi (*Software Architecture for Developers*, 60-bet). Richards va Ford buni avtomatlashtirishning nomini beradi: fitness function, ya'ni biror arxitektura xususiyatining obyektiv baholovchisi; ularning misolida sahifa yuklash vaqti muhim xususiyat deb belgilanadi va uni o'lchaydigan test continuous integration ning bir qismi bo'lib ishlaydi (*Fundamentals of Software Architecture*, 1-bob).

*The Hard Parts* mualliflari shu mexanizmning nega kerakligini tushuntiradi: loyihalar shoshilinch ishga g'arq bo'lib, muhim lekin shoshilinch bo'lmagan tamoyillarni chetga surib qo'yadi va texnik qarz aynan shunday to'planadi ("bu yomon ekanini bilamiz, keyin tuzatamiz" deyilib, keyin hech qachon kelmaydi); fitness function esa shu tamoyillarni developer o'tkazib yubora olmaydigan checklist ga aylantiradi (1-bob, 13-bet).

"Ma'lumot yo'qolmasin" mezoni uchun o'lchash usuli bu tunda ishlaydigan solishtirish jarayoni: u tashqi va ichki yozuvlarni sanab taqqoslaydi, farq nolga teng bo'lmasa ogohlantiradi. Shu o'lchov bo'lmasa, siz bilmaysiz, faqat ishonasiz.

Testlash qo'llanmasidagi performance test bo'limi shu mezonlarni avtomatik darvozaga aylantirish usulini beradi. Arxitektorning bu yerdagi ishi boshqa: mezonni shunday yozish, uni mashinani o'qiydigan shaklga aylantirish mumkin bo'lsin.

## 2.9 Noto'g'ri tushunishning narxi

Talabni noto'g'ri tushunish narxi chiziqli emas. McConnell buni jadvalda beradi va manbasini bir nechta sanoat tadqiqotiga bog'laydi (*Code Complete*, 2-nashr, 3-bob, 3-1-jadval, 29-bet). Jadvalning mazmuni: talab bosqichida kiritilgan nuqson shu bosqichda topilsa narxi 1, arxitektura bosqichida topilsa 3, qurish bosqichida 5 dan 10 gacha, tizim testida 10, reliz dan keyin 10 dan 100 gacha. Arxitektura bosqichida kiritilgan nuqson shu bosqichda topilsa 1, qurishda 10, tizim testida 15, reliz dan keyin 25 dan 100 gacha. Kitobning o'z misoli: arxitektura chizilayotganda 1000 dollarga tuzatiladigan nuqson tizim testida 15 ming dollarga chiqishi mumkin. Umumiy tamoyil ham shu yerda: xatoni kiritilgan paytga qanchalik yaqin topsang, shuncha arzon; talab birinchi bajarilganidan talabdagi nuqsonlar tizimda eng uzoq yashaydi va eng qimmat bo'ladi.

Eng qimmat uch xato turi bor. Yaroqsiz sxema: to'lov summasini `double` saqlash qarori arzon ko'rinadi, lekin million qatorda tiyin yo'qolganini topganda migratsiya haftalab davom etadi. Keraksiz servis: "kelajakda kerak bo'ladi" taxmini bilan ajratilgan servis har bir yangi xususiyatga ikki deploy va taqsimlangan tranzaksiya muammosini qo'shadi. Noto'g'ri chegara: agregat chegarasi xato qo'yilsa, har bir operatsiya bir necha agregatga tegadi va lock contention yuzaga keladi.

| Holat | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Biznes yechim aytdi | Aytganini kodlaydi | Uch marta "nima uchun" so'rab, ehtiyojni topadi |
| "Tez bo'lsin" talabi | Keyinroq optimallashtiramiz deydi | p99 va o'lchash nuqtasini shartnomaga yozadi |
| Hajm noma'lum | Standart sozlama bilan ketadi | Bugungi va uch yillik raqamni hisoblaydi |
| Chegaraviy holat | Birinchi bug hisobotida bilib oladi | Oldindan 10 ta holatni sanab, har biriga qaror oladi |
| Domen so'zlari | Dto va Entity deb nomlaydi | Biznes so'zini klass nomiga aynan ko'chiradi |
| Yangi ehtiyoj paydo bo'ldi | Yangi servis ajratadi | Avval mavjud chegara ichida sinab ko'radi |
| Iste'molchi turi | Hamma uchun bitta API | Tashqi, ichki va servis uchun alohida shartnoma |
| Muvaffaqiyat | Vazifa yopilsa tugadi deydi | Raqam o'zgarganini o'lchab tasdiqlaydi |
| Qamrov o'sdi | Hammasini sig'dirishga urinadi | Kesib tashlaydi va nimadan voz kechganini yozadi |
| Qoldiq manfiy bo'lmasligi | Java tomonda if bilan tekshiradi | Baza cheklovi va atomik UPDATE bilan ta'minlaydi |

| Tuzoq | Nimaga olib keladi | Yechim |
|---|---|---|
| Pul uchun `double` | Tiyin yo'qoladi, hisobot farq qiladi | `BigDecimal` yoki `numeric(19,4)`, scale aniq belgilanadi |
| Vaqtni mahalliy zonada saqlash | Yozgi vaqt o'tishida qatorlar takrorlanadi | `timestamptz` va UTC, ko'rsatishda zona qo'llanadi |
| "Nima uchun" so'ralmagan | Keraksiz xususiyat yozildi | Talab bilan biznes natijasi orasida bog'liqlik talab qilinadi |
| O'rtacha latency ni mezon qilish | Sekin so'rovlar yashirinadi | p99 va p999, histogram yoqilgan holda |
| Hajm taxminsiz sxema | Bir yildan keyin majburiy migratsiya | Qator hajmi va yillik o'sish oldindan hisoblanadi |
| Bitta `Order` hamma kontekst uchun | 60 maydonli klass, hech kim o'zgartirmaydi | Kontekstga ko'ra alohida model va tarjima qatlami |
| Idempotentlik yo'q | Mijoz retry qilganda ikki marta to'lov | Idempotency kaliti va unique cheklov |
| Chegaraviy holat kechiktirildi | Ishlab chiqarishda ma'lumot buziladi | Talab bosqichida holatlar ro'yxati va qarorlar |

## 2.10 Talabni rad etish va qamrovni qisqartirish san'ati

Arxitektorning eng kuchli vositasi "yo'q" so'zi, lekin quruq rad etish ishonchni buzadi. To'g'ri shaklni Simon Brown "challenge" deb ataydi va mexanizmini ko'rsatadi: odamga biror narsa kerakmi deb so'rasangiz javob "ha" bo'ladi, shuning uchun har qanday ustuvorlik shkalasida (MoSCoW, yuqori/o'rta/past) hamma talab birinchi urinishda "must have" ga tushadi; fikrni aniqlashtiradigan narsa esa narxni ko'rsatish (*Software Architecture for Developers*, 61-bet).

Brown ning o'z misoli aynan shunday tuzilgan. Arxitektor: 100 foiz uptime kerak bo'lsa, bu yakka nosozlik nuqtalarini yo'qotish uchun ko'p zahira, hamma narsaning ikki nusxasi va avtomatik failover uchun ko'p injener ishini talab qiladi, bu taxminan bir million dollar; muqobil variant soddaroq, ba'zi komponentlarni nosozlikda qo'lda kuzatib qayta ishga tushirish shartida, bu taxminan yuz ming dollar; qaysi biri kerak. Homiy: agar shunday bo'lsa, arzonini olaman. Brown ning xulosasi: hamma narsa mumkin, lekin hamma narsaning trade-off i bor, va shu trade-off ni tushuntirish berilgan kontekstdagi eng yaxshi yechimni topishga yordam beradi. Shakl uch qismdan iborat: ehtiyojni tan olish, narxni ko'rsatish va arzonroq alternativa taklif qilish.

Misol. Biznes real vaqtda yangilanadigan omborlar dashboard'ini so'raydi. Rad etish shunday ko'rinadi: "Qoldiqni kuzatish kerakligini tushunaman. Real vaqtda yangilanish WebSocket infratuzilmasi, alohida o'qish modeli va taxminan uch hafta ish talab qiladi. Boshqa variant: 30 sekundda bir yangilanadigan sahifa, bu ikki kunlik ish. Agar 30 sekund yetmasa, qaysi qaror shuncha tez qabul qilinishi kerakligini aytsangiz, shu oqim uchun alohida real vaqt kanali qilamiz."

Bu javobda hurmat, raqam va tanlov bor. Biznes odatda ikkinchi variantni oladi, chunki haqiqiy ehtiyoj 30 sekundlik yangilanish bilan qoplanadi.

Qamrovni qisqartirishda Richards va Ford ning qoidasi ishlaydi: barcha atributni ustuvorlashtirishga urinish ko'p holda befoyda, chunki hamma manfaatdor har bir atributning tartibiga kelishmaydi; amaliy yo'l domen manfaatdorlariga eng muhim uchtasini (tartibsiz) tanlatish, bu kelishuvni osonlashtiradi va nima muhimligi haqida muhokama ochadi (*Fundamentals of Software Architecture*, 5-bob).

ESLATMA: talabni "birinchi relizda kerak", "uchinchi oyda kerak" va "hech qachon kerak bo'lmasligi mumkin" guruhlariga ajratish shu korpusning amaliy tavsiyasi, kitobdan olingan emas. Oxirgi guruhga tushgan talablar yozilib qo'yiladi, lekin bajarilmaydi va keyingi muhokamada qayta ko'riladi.

Rad etilgan talabni yozib qo'yish majburiy. Qaror hujjatida (ADR) "nimadan voz kechdik va nima uchun" bo'limi bo'lsin. Oltinchi oyda kimdir "nega bu yo'q" deb so'raganda, javob repozitoriyda turadi.

Oxirgi qoida: bo'linmaydigan talab odatda yaxshi tushunilmagan talab. Qancha vaqtdan keyin talabni katta deb hisoblash kerakligi uchun bu bobda raqam berilmaydi, chunki yuqoridagi manbalarda bunday chegara o'lchanmagan; belgi vaqt emas, Fairbanks ning savoli: asosiy nosozlik risklarini va ularga qo'llanayotgan usullarni sanab bera olasizmi (*Just Enough Software Architecture*, 3.2-bo'lim). Javob yo'q bo'lsa, talab hali bo'laklarga ajratilmagan.

## 2.11 Savol birinchi, model ikkinchi

Arxitektor modelni chizishdan oldin modelning qaysi savolga javob berishini biladi. Fairbanks buni qoida shaklida yozadi: savol birinchi, model ikkinchi. Sababi oddiy, javob vaqtini taxmin qiladigan model xavfsizlik teshigini topa olmaydi, shuning uchun savolni bilmasdan model qurish abstraksiya darajasini ham, qaysi tafsilot kirishini ham tasodifga qoldiradi (*Just Enough Software Architecture*, 6.6-bo'lim).

Model nega kerak bo'lishi ham shu bobda. Masala kattalashganda yoki murakkablashganda injener abstraksiyaga o'tadi, chunki tizimni kod o'qib tushunishdan ko'ra model orqali tushunish tezroq: ikki developer bir-biriga yuz minglab qatorlik tizimni bir necha soatda tushuntirmoqchi bo'lsa, kod o'qish emas, eskiz chizish ishlaydi (6.1-bo'lim). Model o'z-o'zidan foyda bermaydi, u ikki narsa beradi: muammoning mohiyatini ko'rsatadigan tushuncha (insight) va uni yechadigan vosita (leverage). Ikki poyezd masalasida poyezd domeni hech qanday vosita bermaydi, algebra esa beradi (6.2-bo'lim).

Fairbanks ning o'z misoli bizdagi N+1 muammosining aynan o'zi. Taqdimotchi X texnologiyasidan Y ga o'tgach throughput yaxshilanganini til ixchamligi, interfeys va kengaytiriluvchanlik bilan izohlagan, lekin butun farq bitta tafsilotda bo'lgan: X ma'lumotni ierarxik saqlagani uchun bitta sahifa so'rovi o'rtacha yigirma marta bazaga borardi, Y da esa bir marta (6.3-bo'lim). Buni ko'rish uchun eng oddiy model yetadi.

```java
// Savol: nega sahifa sekin. Model faqat shu savolga javob beradi.
record LatencyModel(int transportMs, int serverMs, int queryMs, int queryCount) {
    int expectedMs() {
        return transportMs + serverMs + queryMs * queryCount;
    }
}
// Fairbanks ning raqamlari bilan: 10 + 10 + 25 * 20 = 520 ms
// Bitta so'rovga tushirilganda:   10 + 10 + 25 * 1  = 45 ms
```

Bu model keshni ham, navbatni ham hisobga olmaydi va shu bilan haqli, chunki model tafsilotni ataylab tashlaydi. Fairbanks shu yerda Box va Draper ning gapini keltiradi: barcha modellar noto'g'ri, lekin ba'zilari foydali. Keraksiz tafsilot modelni chalkashtiradi, kerakli tafsilotni tashlash esa noto'g'ri javobga olib keladi, va ikkisi orasidagi tanlov trade-off (6.4-bo'lim).

Oxirgi xulosa amaliy: bitta model qurganingizda siz boshqa modelni qurmaslikka qaror qilgan bo'lasiz (6.7-bo'lim). Shuning uchun "arxitekturani chizib chiqaylik" degan gap topshiriq emas. Avval savol yoziladi (p99 ni nima belgilaydi, ma'lumotga ruxsatsiz qaysi yo'ldan kirish mumkin, bitta modulni almashtirish nechta joyga tegadi), keyin shu savolga javob beradigan eng arzon model quriladi.

## 2.12 Uch model: domen, dizayn va kod

Fairbanks ning kanonik model tuzilmasi uch asosiy modeldan iborat va ular abstraktdan konkretga qarab joylashadi: domen modeli, dizayn modeli, kod modeli (*Just Enough Software Architecture*, 7.1 va 7.2-bo'limlar). Ajratmaning qoidasi bir gapda beriladi. Agar narsa shunchaki haqiqat bo'lsa, u domen modeliga tushadi; agar u sizning qaroringiz yoki siz o'ylab topgan mexanizm bo'lsa, dizayn modeliga; agar u programmalash tilida yozilgan bo'lsa, kod modeliga.

Kitobning uchta misoli farqni darhol ko'rsatadi: "billing sikli 30 kun" domen fakti, "font resurslari albatta qo'lda bo'shatiladi" dizayn fakti, "mijoz manzili `varchar(80)` da saqlanadi" implementatsiya fakti. Tuzilmaning foydasi ham shunda: har bir masala kichrayadi, chunki domen haqida fikrlaganda kod tafsiloti chalg'itmaydi va teskarisi (7.1.1-bo'lim).

Java loyihasida bu ajratma ko'pincha yo'qoladi, chunki uchala model bitta faylda yashaydi. JPA entity domen modeli emas, u allaqachon dizayn majburiyatlariga to'lgan.

```java
@Entity
class Payment {

    @Id
    private UUID id;

    // Domen haqiqati: bitta to'lov bitta buyurtmaga tegishli. Bu bizning qarorimiz emas.
    @ManyToOne(optional = false)
    private Order order;

    // Dizayn qarori: parallel yangilanishni optimistic locking bilan ushlaymiz.
    // Domenda "version" degan tushuncha yo'q.
    @Version
    private long version;

    // Kod modeli: ustun numeric(19,4) ga tushadi, ya'ni to'rt kasr xona.
    private BigDecimal amount;
}
```

Dizayn modeli qasddan to'liq emas: u majburiyatlarning bir qismini oladi va past darajadagi tafsilotni kod modeliga qoldiradi. Kod modelida esa majburiyatlar to'plami to'liq, chunki aks holda mashinada ishlamaydi (7.2-bo'lim).

Uchala model, Fairbanks ning atamasi bilan, master model: ular tushuncha darajasida siz bilgan hamma tafsilotni o'z ichiga oladi va shuning uchun to'g'ridan-to'g'ri ishlatish uchun juda katta. Siz chizadigan har bir diagramma master modeldan olingan ko'rinish (view), ya'ni tafsilotlarning belgilangan qismi. Shundan muhim natija chiqadi: barcha ko'rinish bir-biriga mos bo'lishi shart, mos kelmaslik topilsa, bu yo master modeldagi, yo ko'rinishni yasash jarayonidagi xato (7.4-bo'lim). Kruchten ning 4+1 ishiga havola qilib, Fairbanks bitta diagrammada hamma narsani ko'rsatish amalda mumkin emasligini aytadi.

ESLATMA: kitob 2010 yilda yozilgan va modelni UML notatsiyasida chizadi (7.7-bo'lim). Bu korpusda UML sintaksisi o'rgatilmaydi: yuqoridagi uch model ajratmasi notatsiyadan mustaqil va faqat shu ajratma sifatida olinadi. Modelni qanday hujjatlash kerakligi [qaror qabul qilish va uni hujjatlashtirish](03-qaror-qabul-qilish-va-uni-hujjatlashtirish.md) bobida.

## 2.13 Dizayn modeli: chegara modeli va ichki model

Dizayn modeli ikki qismdan iborat va ikkisi bir xil narsa haqida, farq faqat tafsilot darajasida. Chegara modeli (boundary model) tashqaridan ko'rinadigan narsani oladi: xulq, almashinuv ma'lumoti va sifat atributlari. U interfeysga majburiyat beradi, implementatsiyaga emas. Ichki model (internals model) esa chegara modeli yashirgan tafsilotni ochadi (*Just Enough Software Architecture*, 9.2 va 9.3-bo'limlar). Fairbanks "interfeys" o'rniga "chegara" deyishining sababi aniq: Java da `interface` til konstruksiyasi va ikkisi aralashib ketadi.

Eng muhim qoida shu: chegara modelida to'g'ri bo'lgan narsa ichki modelda ham to'g'ri bo'lishi shart. Chegara modeli tizim 99.5 foiz vaqt ishlaydi va Linux da deploy qilinadi deb aytgan bo'lsa, ichki model buni buzmaydi (*Just Enough Software Architecture*, 9.3-bo'lim). Java modulida chegara modeli paketning `public` turlari, ularning shartnomasi va shu modulga qo'yilgan SLO dan iborat; qolgan hamma narsa ichki model.

```java
// Chegara modeli: tashqariga chiqadigan xulq va almashinuv ma'lumoti.
// Chegara majburiyati: p99 < 300 ms, bir xil requestId bir marta hisoblanadi.
public interface PaymentGateway {
    PaymentResult charge(ChargeRequest request);
}

// Ichki model: chegara majburiyatini buzmasligi shart.
@Service
class CardPaymentGateway implements PaymentGateway {

    private final RestClient restClient;

    CardPaymentGateway(RestClient restClient) {
        this.restClient = restClient;
    }

    @Override
    public PaymentResult charge(ChargeRequest request) {
        // Bu yerga ikki sekundlik sinxron chaqiruv qo'shilsa, chegaradagi
        // p99 majburiyati buziladi va dizayn modeli nomuvofiq bo'lib qoladi.
        return restClient.post().uri("/charge")
                .body(request)
                .retrieve()
                .body(PaymentResult.class);
    }
}
```

Tuzilma rekursiv: ichki model kichikroq elementlardan iborat, ularning har biri o'z chegara modeli va o'z ichki modeliga ega, ya'ni bitta element chegara va ichki modellar daraxtiga ajraladi (9.1-bo'lim). Java da bu daraxt tabiiy: tizimning chegarasi uning HTTP shartnomasi, modulning chegarasi paketning `public` yuzi, sinfning chegarasi uning `public` metodlari.

Sifat atributlari ham chegara modeliga tegishli va Fairbanks ularning muhim xususiyatini aytadi: ular emergent, ya'ni koddagi birorta joy xavfsizlik, o'zgartiriluvchanlik yoki kechikish uchun javobgar emas, bu sifatlar arxitektura va dizayndan kelib chiqadi (9.4-bo'lim). Shuning uchun "p99 uchun kim javobgar" savoliga bitta sinf nomi bilan javob berilmaydi: javob chegara modelida yozilgan majburiyat bo'ladi.

## 2.14 Model munosabatlari: designation va refinement

Modellar o'zaro bog'lanmasa, ularning to'plami hujjat bo'lmaydi. Fairbanks to'qqizta munosabatni sanaydi va ularni uy hamda uning chizmasi misolida izohlaydi (*Just Enough Software Architecture*, 13-bob, 13.1-rasm).

| Munosabat | Nimadan nimaga | Ma'nosi |
|---|---|---|
| Projection (view) | model - model | tafsilotning bir qismi, ehtimol o'zgartirish bilan |
| Partition | model - modellar | butunni kesishmaydigan qismlarga bo'lish |
| Composition | modellar - model | qismlardan kattaroq model yig'ish |
| Classification | tur - instance | instance ni kategoriyaga qo'yish |
| Generalization | supertip - subtip | kategoriyalar orasidagi qamrov |
| Designation | dunyo yoki model - model | moslik: bu element o'sha elementga to'g'ri keladi |
| Refinement | model - model | kam tafsilotdan ko'p tafsilotga |
| Binding | model - model | patternga bog'lash |
| Dependency | model - model | biri o'zgarsa ikkinchisi o'zgarishi mumkin |

Ikkitasi kundalik ishda eng ko'p kerak. **Designation** modeldagi elementni dunyodagi yoki boshqa modeldagi element bilan moslashtiradi. Qog'ozga chizilgan "Uy" degan kvadrat yomg'irdan saqlamaydi, lekin sizning niyatingiz shu kvadrat haqiqiy g'isht uyga to'g'ri kelishi. Jackson ga havola qilib, Fairbanks qoida beradi: imkon qadar kam narsa designate qilinadi, qolgani ulardan hisoblanadi (13.6-bo'lim). Haqiqiy narsani va modeldagi narsani aralashtirish xato manbai: tizim bitta odamning ikki email manzilini ikki odam deb bilishi shunday xato (7.3-bo'lim).

Java da designation paket va tur nomida yashaydi: `uz.shop.contract` paketi domendagi "shartnoma" tushunchasiga mos kelsa, designation saqlanadi; `ContractServiceImpl2` esa domenda hech narsaga mos kelmaydi.

**Refinement** bir narsaning kam tafsilotli va ko'p tafsilotli ko'rinishini bog'laydi; ta'rifning ikkinchi shakli foydaliroq: yuqori darajadagi modeldan chiqarilgan hamma xulosa past darajadagi modelda ham to'g'ri bo'ladi (13.7-bo'lim). Qaysi biri avval yozilgani ahamiyatsiz. Fairbanks semantikaning ikki turini ajratadi: ochiq semantikada refinement xohlagan yangi elementni qo'shadi, yopiq semantikada esa qo'shilmaydigan element turlari oldindan sanaladi. Arxitektura modellari uchun uning tavsiyasi aniq, yopiq semantikaga amal qilinadi va yangi port qo'shish taqiqlanadi (13.7.1-bo'lim).

Bu tavsiya Java da testga aylanadi. Modulning chegara modelida sanalgan portlar bor, ichki model ularga yangi chiqish bog'lanishi qo'shmaydi, va buni [ArchUnit asoslari](../testing/14-arxitektura-testlari-va-kod-sifati.md#142-archunit-asoslari) bo'limidagi shakl ushlaydi.

```java
@AnalyzeClasses(packages = "uz.shop")
class ModelRefinementTest {

    // Yopiq refinement semantikasi: payment ning ichki modeli
    // chegara modelida sanalmagan portga bog'lanmaydi.
    @ArchTest
    static final ArchRule paymentUsesOnlyDeclaredPorts =
            classes().that().resideInAPackage("..payment..")
                    .should().onlyDependOnClassesThat()
                    .resideInAnyPackage("..payment..", "..order.api..",
                            "java..", "org.springframework..");
}
```

Qolgan munosabatlardan ikkitasi tez-tez chalkashadi. Partition qismlar kesishmasdan butunni qoplashini talab qiladi, projection esa bunday talab qo'ymaydi (13.2-bo'lim). Generalization uchun Fairbanks Liskov ning testini beradi: subtip supertip o'rniga qo'yilishi mumkin bo'lishi shart (13.5-bo'lim).

## 2.15 Qaysi model quriladi va qachon tashlab yuboriladi

To'liqlik yaxshi modelning belgisi emas. Fairbanks ro'yxatni shu gap bilan boshlaydi: injener model qurish narxini uning foydasiga solishtirishi shart va bu solishtirish odatda to'liq bo'lmagan, lekin foydali modelga olib keladi (*Just Enough Software Architecture*, 15.1-bo'lim). Arzonlik alohida mezon: foyda egri chizig'i ko'pincha narx egri chizig'idan oldinda yuradi, shuning uchun riskni yopadigan eng arzon model tanlanadi. Kitobning eng arzon misoli komponentlar va ulanishlarning matnli ro'yxati, u juda kam kuch talab qiladi, lekin modelsiz holatdan ancha yaxshi (15.1.7-bo'lim).

Spring loyihasida bu ro'yxatni qo'lda yozish ham shart emas, chunki konteyner uni biladi.

```java
@Component
class ComponentListPrinter implements ApplicationRunner {

    private final ConfigurableApplicationContext context;

    ComponentListPrinter(ConfigurableApplicationContext context) {
        this.context = context;
    }

    // Eng arzon model: komponent va ulanishlarning matnli ro'yxati.
    @Override
    public void run(ApplicationArguments args) {
        ConfigurableListableBeanFactory factory = context.getBeanFactory();
        for (String name : factory.getBeanDefinitionNames()) {
            String[] uses = factory.getDependenciesForBean(name);
            if (uses.length > 0) {
                System.out.println(name + " -> " + String.join(", ", uses));
            }
        }
    }
}
```

Keyingi savol qaysi ko'rinishni qurish. Fairbanks ning javobi: har bir tashvish (concern) uchun bitta ko'rinish, va programmada tashvishlar ko'pincha sifat atributlari va funksionallik bilan mos tushadi (15.2-bo'lim). Bu yerda ikki tuzoq bor va ikkisi ham nomlangan. Birinchisi sevimli ko'rinish: developer o'tgan loyihada qatlamli ko'rinish yordam bergani uchun hozirgi loyiha peer-to-peer uslubida bo'lsa ham o'sha ko'rinish bilan fikrlashni davom ettiradi. Ikkinchisi hammasini qamraydigan yagona diagramma: muallif hamma tafsilotni bitta rasmga siqadi va natijada ikki quti orasidagi chiziq modul bog'liqligimi yoki runtime aloqasimi, aniqlab bo'lmaydi (15.2.2-bo'lim).

Abstraksiya darajasi uchun Fairbanks hisob beradi. API darajasidagi model vasvasali, chunki u konkret va kod bilan solishtirib tekshiriladi, lekin har bir API operatsiyasiga ming qator implementatsiya to'g'ri kelsa, million qatorlik tizimda modellashtiriladigan ming operatsiya chiqadi, va uni yangilab turish qurishdan ham qiyin (15.8-bo'lim).

Mavjud tizimni modellashtirishda maqsad modelni belgilaydi. Kitobning jadvalida har sabab uchun nomzod model bor: tizimni tushunish uchun kam tafsilotli domen va chegara modeli; muqobil arxitekturani baholash uchun chegara va ichki model, ustiga tanlangan nozik joylar bo'yicha chuqur tafsilot; tashqi developer uchun hujjatlashda qo'shimcha ravishda uslublar va invariantlar (15.11-bo'lim). Ogohlantirish ham bor: tizim big ball of mud bo'lsa, qancha modellashtirsangiz ham loydan boshqa narsa chiqmaydi.

Modelni qachon tashlab yuborish kerak degan savolga javob shu yerdan chiqadi. Model savol tugashi bilan qiymatini yo'qotadi. U qarorni asoslagan bo'lsa, qaror [qaror qabul qilish va uni hujjatlashtirish](03-qaror-qabul-qilish-va-uni-hujjatlashtirish.md) bobidagi shaklda yozib qoldiriladi, model esa saqlanmaydi. Saqlanadigani faqat kod bilan birga tekshirilib turadigani: ArchUnit qoidasi, sxema migratsiyasi va shartnoma testi.

## 2.16 Ishni boshlashdan oldin yozma talab va uni tasdiqlash

Mahsulotdagi xatoning katta qismi kodda emas, kutilgan narsa bilan qurilgan narsa orasidagi farqda tug'iladi. Orosz buni ochiq aytadi: mahsulotdagi ko'p xato manfaatdorlar kutgani bilan muhandis qurgani orasidagi noto'g'ri tushunishdan keladi, va bunday tushunmovchilikdan qochish uchun funksiya qanday ishlashini, chegaraviy holatlarini va qamrovdan nima chiqib qolganini tasvirlaydigan yozma shartni talab qilish kerak (Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 11-bob, 158-bet). Ishni boshlashni mahsulot va mijoz nuqtai nazaridan to'liq tushunmaguncha orqaga surish ham shu yerda: tushunilgani yozib qo'yiladi (11-bob, 158-159-bet).

Yozma shakl uzun bo'lishi shart emas va uni mahsulot menejeri yozishi ham shart emas. Orosz ning tartibi shunday: yozma shart bo'lmasa, funksiya qanday ishlashi kutilayotganini mahsulot odami yoki biznes manfaatdori bilan muhokama qilasiz, uni bir-ikki betda bullet shaklida xulosalaysiz, keyin "ishlar aynan shunday bo'lishi kerakmi" deb o'sha odamda tasdiqlatasiz; u buni bir soatlik mashq deb ataydi va bu mashq kunlab ishni tejashi mumkinligini aytadi (11-bob, 159-bet). Tejashning sababi [noto'g'ri tushunishning narxi](#29-notogri-tushunishning-narxi) bo'limida raqam bilan ko'rsatilgan: nuqson qancha kech topilsa, shuncha qimmat.

Ikkinchi foyda tasdiqlash paytida chiqadi. Orosz ta'kidlaydi: yozma shartni ko'rsatsangiz, mahsulot odami xato, tushib qolgan tafsilot yoki chegaraviy holatni ko'rsatib berish ehtimoli katta (11-bob, 159-bet). Ya'ni bu hujjat faqat kelishuv emas, [chegaraviy holatlar va istisnolarni oldindan topish](#25-chegaraviy-holatlar-va-istisnolarni-oldindan-topish) uchun ham arzon vosita. Shu mantiq test rejasiga ham tegishli: reja implementatsiyadan oldin, rejalashtirish bosqichida yoziladi va mahsulot menejeri, boshqa muhandislar yoki QA bilan bo'lishiladi, chunki o'tkazib yuborilgan holatni aynan ular ko'radi (11-bob, 159-bet).

Oxirgi qoida qamrov haqida: testlash, monitoring va alerting kelishilgan ishning ichida turadi, alohida muzokara bandi emas. Orosz sababini aytadi: bu qism alohida ko'rsatilsa, mahsulot va biznes tomoni uni vaqt tejash imkoniyati deb ko'radi va birinchi bo'lib shuni kesadi (11-bob, 159-bet).

ESLATMA: pastdagi shablon shu korpusning amaliy shakli, kitobdan olingan emas; u Orosz sanagan to'rt bandni (qanday ishlaydi, chegaraviy holat, qamrovdan tashqari, tasdiq) bir sahifaga joylaydi.

```markdown
# Funksiya: to'lovni qisman qaytarish

## Nima uchun
- Qo'llab-quvvatlash jamoasi har oy qo'lda qaytarish qiladi (soni ularning hisobidan olinadi).

## Qanday ishlaydi
- Operator buyurtmani ochadi va qaytariladigan summani kiritadi.
- Summa to'langan summadan oshmaydi; qolgan balans buyurtmada ko'rinadi.

## Chegaraviy holatlar
- To'lov hali `PENDING` bo'lsa: qaytarish rad etiladi.
- Ikki operator bir vaqtda qaytarsa: ikkinchisi xato oladi, qo'sh qaytarish bo'lmaydi.
- Provayder belgilangan vaqtda javob bermasa: holat `UNKNOWN`, keyin qayta so'raladi.

## Qamrovdan tashqari (birinchi reliz)
- Valyuta konvertatsiyasi bilan qaytarish.
- Operatorsiz, avtomatik qaytarish.

## Tasdiq
- Mahsulot egasi: <ism>, sana: <sana>.
```

## 2.17 Tayyorgarlikni o'tkazib yuborish: sabablari, narxi va vaqt ulushi

[Noto'g'ri tushunishning narxi](#29-notogri-tushunishning-narxi) bo'limi kech topilgan nuqsonning qimmatligini ko'rsatadi. Keyingi savol amaliy: unda tayyorgarlikka qancha vaqt ketadi, va nega jamoalar uni baribir o'tkazib yuboradi. McConnell uchalasiga ham raqam va nom beradi.

Vaqt ulushi avvalo belgilanadi. Yaxshi boshqarilgan loyiha muammoni ta'riflash, talablar va dasturiy arxitekturaga mehnatining taxminan 10 dan 20 foizini va muddatining taxminan 20 dan 30 foizini ajratadi; bu raqamlarga batafsil dizayn kirmaydi, chunki u konstruksiyaning qismi (McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 3.6 (55-bet)). Talablar beqaror bo'lsa qoida boshqacha: talab ishi o'zi alohida loyiha deb olinadi va qolgan loyiha muddati faqat talablar tugagandan keyin baholanadi, chunki nima qurilayotgani bilinmasdan muddat aytishni hech kim asosli talab qila olmaydi (3.6 (56-bet)).

```text
Tayyorgarlik byudjeti (misol korpusning o'zidan, kitobdan emas):
  loyiha           12 hafta, 4 muhandis   = 48 odam-hafta
  mehnat 10 foiz   4.8 odam-hafta   -> talab barqaror, domen tanish
  mehnat 20 foiz   9.6 odam-hafta   -> talab noaniq yoki domen yangi
  muddat 20-30 foiz  2.4 - 3.6 hafta -> kalendar ulushi, mehnat emas
Izoh: batafsil dizayn bu ulushga kirmaydi, u konstruksiya ichida.
```

O'tkazib yuborishning sabablari uchta va ularning har biri boshqa javob talab qiladi (3.1 (25-27-betlar)):

- **Bilmaslik.** Yuqori oqim ishiga qo'yilgan dasturchilarda buni bajarish malakasi yo'q: loyihani rejalashtirish, ishonchli biznes asos yozish, to'liq va aniq talab ishlab chiqish va sifatli arxitektura qurish arzimas ko'nikmalar emas, lekin ko'p dasturchi bu ishlarga o'qitilmagan. Oqibati nozik: malaka bo'lmasa "yuqori oqim ishini ko'proq qil" tavsiyasi bema'ni eshitiladi, chunki yomon bajarilayotgan ishni ko'paytirish foyda bermaydi.
- **Kodga shoshilish.** Ba'zilar yuqori oqim ishini qanday qilishni biladi, lekin imkon qadar tezroq kod yozishni boshlash istagiga qarshi turolmaydi.
- **Menejer bosimi.** Menejerlar tayyorgarlikka vaqt sarflayotgan dasturchiga xushyoqmaydi. McConnell bu hodisaga nom beradi: WISCA yoki WIMP sindromi, ya'ni "Sam nega hech narsa kodlamayapti?" va "Meri nega programmalamayapti?". Kitob to'rt javobni sanaydi (qat'iy rad etish, kodlayotgandek ko'rinish, menejerga tushuntirish, boshqa ish topish) va tushuntirishni yaxshi yondashuv deb tanlaydi, chunki u dunyoda ma'rifatli boshliqlar sonini oshiradi.

Eng ko'p uchraydigan e'tiroz esa iterativ ishlash haqida. Ba'zi mualliflar iterativ texnikadan foydalanadigan loyihaga tayyorgarlik umuman kerak emas deb da'vo qiladi; McConnell bu qarashni noto'g'ri xabardorlik deb ataydi: iterativ yondashuv yetarli bo'lmagan yuqori oqim ishining ta'sirini kamaytiradi, lekin uni yo'q qilmaydi (3.2 (33-bet)). Kitob to'rt ssenariyni yonma-yon qo'yadi va raqamlar faqat illyustratsiya uchun ekanini ochiq aytadi, nisbat esa bobdagi tadqiqotlar bilan quvvatlangan:

| Yondashuv | Ish narxi | Qayta ishlash narxi | Jami |
|---|---|---|---|
| Ketma-ket, tayyorgarliksiz | 500 000 | 500 000 (oxirida bir yo'la) | 1 000 000 |
| Iterativ, tayyorgarliksiz | 500 000 | 375 000 (bosqichlarga tarqalgan) | 875 000 |
| Ketma-ket, tayyorgarlik bilan | 500 000 | 100 000 | 600 000 |
| Iterativ, tayyorgarlik bilan | 500 000 | 50 000 | 550 000 |

Jadvaldan ikki xulosa chiqadi. Birinchi: tayyorgarlikka e'tibor narxni ikki yondashuvda ham kamaytiradi, va tayyorgarlikni e'tibordan chiqargan iterativ loyiha tayyorgarlikka diqqat bilan qaragan ketma-ket loyihadan sezilarli qimmatga tushishi mumkin (3.2 (34-bet)). Ikkinchi: iterativ loyihada narx bo'lak-bo'lak so'rilgani uchun u shuncha katta bo'lib ko'rinmaydi, chang tushgandan keyin esa jami narx o'xshash chiqadi (3.2 (34-bet)).

Amaliy chegara shu yerdan keladi: talablarning yoki dizaynning 100 foizini oldindan belgilash amaliy emas, lekin ko'p loyiha hech bo'lmasa eng kritik talablar va arxitektura elementlarini erta aniqlashdan foyda topadi (3.2 (34-bet)). Kitobdagi ikki tayyor qoida: talablarning taxminan 80 foizini oldindan belgilab, qolganiga vaqt ajratish va keyin tizimli o'zgarish nazorati bilan faqat eng qimmatli yangi talabni qabul qilish; yoki eng muhim 20 foizni oldindan belgilab, qolganini kichik inkrementlarda, borgan sari qo'shilib boradigan talab va dizayn bilan qurish (3.2 (34-bet)). Ikkinchi variant [yozma talab va uni tasdiqlash](#216-ishni-boshlashdan-oldin-yozma-talab-va-uni-tasdiqlash) qoidasini bekor qilmaydi: inkrement kichraysa, yozma shart ham kichrayadi, lekin yo'qolmaydi.

## 2.18 Amalda qo'llash

- [ ] Hozirgi backlog'dagi eng katta uch talabni oling va har biriga uch marta "nima uchun" savolini berib, javoblarni bir betga yozing.
- [ ] Har bir talab uchun olti o'lchov jadvalini (tezlik, hajm, ishonchlilik, ma'lumot yangiligi, xavfsizlik, narx) to'ldiring va bo'sh qolgan katakchalarni biznesdan so'rang.
- [ ] Eng muhim ikki endpoint uchun p99 va p999 qiymatini belgilab, `percentiles-histogram` va `slo` sozlamalarini yoqing, keyin bir hafta haqiqiy raqamni kuzatib SLO ni to'g'rilang.
- [ ] Eng katta uch jadvalning hozirgi hajmini va bitta qator o'rtacha bayt hajmini o'lchab, uch yillik o'sish prognozini yozib qo'ying.
- [ ] Bitta asosiy biznes oqimi uchun kamida 10 ta chegaraviy holatni sanab chiqing va har biriga qaror yozing, qarorsiz qolganini xavf ro'yxatiga kiritasiz.
- [ ] Ikki soatlik event storming sessiyasini o'tkazing va natijada paydo bo'lgan javobsiz savollarni alohida ro'yxatga oling.
- [ ] Kodingizdagi eng katta entity'ni oling va unda necha xil kontekst aralashganini aniqlang, kamida bitta kontekstni alohida modelga ajratish rejasini yozing.
- [ ] Rad etilgan yoki kechiktirilgan talablar uchun ADR shabloniga "nimadan voz kechdik" bo'limini qo'shib, oxirgi uch qarorni retrospektiv yozib chiqing.
- [ ] Hozir ishlayotgan masalaga model qurishdan oldin shu model javob berishi kerak bo'lgan savolni bitta gapda yozib qo'ying, keyin modelni shu savolga qarab qisqartiring.
- [ ] Bitta JPA entity'ni oling va uning har bir maydonini domen haqiqati, dizayn qarori yoki kod tafsiloti deb belgilang; dizayn qarorlari uchun sabab yozilmaganini aniqlang.
- [ ] Eng muhim bitta modulning chegara modelini yozing (chiqadigan `public` turlar, shartnoma va SLO), keyin ichki modeli shu majburiyatlarni buzmasligini tekshiradigan ArchUnit qoidasini qo'shing.

## Manbalar

- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, O'Reilly, 2020, 1-bob - ikkinchi qonun ("nega qandaydan muhimroq"), arxitekturaning hayotiyligi va uch yillik ufq, fitness function ta'rifi
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, O'Reilly, 2020, 4-bob - atama chalkashligini kamaytirish uchun DDD ning umumiy til tavsiyasi
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, O'Reilly, 2020, 5-bob - arxitektor va biznes tili orasidagi "tarjimada yo'qolish", ro'yxatni qisqa tutish va eng muhim uchtani tanlash, talablar hujjatida yozilmagan pik yuk (universitetga ro'yxatga olish misoli), arxitektura katasining "Users" bo'limi
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, O'Reilly, 2020, 6-bob - performance budget va birinchi sahifa renderi uchun 500 ms, K-weight budjeti
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, O'Reilly, 2020, 7-bob - bounded context: umumiy `Customer` klassi o'rniga har bir domen o'zini yaratadi va farqlar integratsiya nuqtalarida kelishtiriladi
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, O'Reilly, 2020, 20-bob - risk jadvali: ta'sir va ehtimol ko'paytmasi, chegaraviy holatlarni ustuvorlashtirish
- Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani, *Software Architecture: The Hard Parts*, 1-nashr, O'Reilly, 2021 (copyright 2022), 1-bob (13-bet) - shoshilinch ish muhim tamoyillarni siqib chiqarishi va fitness function ning checklist roli
- George Fairbanks, *Just Enough Software Architecture: A Risk-Driven Approach*, Marshall & Brainerd, 2010, 3.2 va 3.3-bo'limlar - riskni keyin test qilinadigan nosozlik ssenariysi sifatida yozish, prototipik risklar va checklist lar, "mijoz ehtiyoji tushunilmagan" riski, risk asosida ishlamayotganlikning belgisi
- George Fairbanks, *Just Enough Software Architecture: A Risk-Driven Approach*, Marshall & Brainerd, 2010, 6-bob (6.1-6.4, 6.6 va 6.7-bo'limlar) - injener nega model quradi, abstraksiya beradigan insight va leverage, ierarxik va yassi saqlash misolidagi 10/10/25 ms va yigirma so'rov hisobi, model tafsilotni tashlashi, "savol birinchi, model ikkinchi" qoidasi
- George Fairbanks, *Just Enough Software Architecture: A Risk-Driven Approach*, Marshall & Brainerd, 2010, 7-bob (7.1, 7.1.1, 7.2, 7.3, 7.4 va 7.7-bo'limlar) - kanonik model tuzilmasi, domen, dizayn va kod modeli ajratmasi hamda uning uch misoli, designation va refinement munosabatlari, master model va ko'rinish izchilligi (Kruchten, 1995), kitobning UML notatsiyasiga tayanishi
- George Fairbanks, *Just Enough Software Architecture: A Risk-Driven Approach*, Marshall & Brainerd, 2010, 8.6-bo'lim - umumiy til (Evans, 2003) va domen modeli ochadigan javobsiz savollar
- George Fairbanks, *Just Enough Software Architecture: A Risk-Driven Approach*, Marshall & Brainerd, 2010, 9-bob (9.1-9.4-bo'limlar) - dizayn modeli, chegara modeli va ichki model ta'rifi, chegara majburiyatining ichki modelda saqlanishi (99.5 foiz uptime misoli), rekursiv nesting, sifat atributlarining emergent tabiati
- George Fairbanks, *Just Enough Software Architecture: A Risk-Driven Approach*, Marshall & Brainerd, 2010, 13-bob (13.1-rasm, 13.2, 13.5, 13.6, 13.7 va 13.7.1-bo'limlar) - to'qqizta model munosabati jadvali, designation va Jackson ning kam designate qilish qoidasi, refinement ta'rifi, ochiq va yopiq semantika hamda yangi port taqiqi, partition va projection farqi, generalization uchun Liskov testi
- George Fairbanks, *Just Enough Software Architecture: A Risk-Driven Approach*, Marshall & Brainerd, 2010, 15-bob (15.1, 15.1.7, 15.2, 15.2.2, 15.8 va 15.11-bo'limlar) - to'liqlik mezon emasligi va narx-foyda solishtiruvi, komponent va ulanishlarning matnli ro'yxati eng arzon model sifatida, har tashvishga bitta ko'rinish, "sevimli ko'rinish" va "yagona diagramma" anti-patternlari, API darajasidagi modelning hisobi, mavjud tizimni modellashtirish sabablari jadvali va big ball of mud ogohlantirishi
- Simon Brown, *Software Architecture for Developers*, Leanpub, 2014 - 19-bet (loyihalar nofunksional talabni so'ramasligi), 55-58-betlar (sifat atributlari ro'yxati va muqobil nomlari), 59-61-betlar ("tizim tez bo'lsin" shaklidagi talab, uni miqdorlashtirib obyektiv test qilinadigan mezonga aylantirish, narx orqali challenge va 100 foiz uptime misoli)
- Martin Kleppmann, *Designing Data-Intensive Applications*, O'Reilly, 2017, 1-bob (14-17-betlar) - o'rtachaning yaroqsizligi va p95/p99/p999, Amazon ning p999 tanlovi, tail latency amplification, head-of-line blocking va mijoz tomonda o'lchash, yuk har o'n barobar oshganda arxitekturani qayta ko'rish
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 3-bob (29-30-betlar, 3-1-jadval) - nuqsonni tuzatish narxi kiritilgan va topilgan bosqichga qarab: talab nuqsoni reliz dan keyin 10 dan 100 barobar, arxitektura nuqsoni tizim testida 15 barobar
- Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 11-bob (158-159-bet) - mahsulot xatolarining manfaatdor kutilmasi bilan qurilgan narsa orasidagi tushunmovchilikdan kelishi, yozma shart talab qilish va uni ishdan oldin tasdiqlash, bir-ikki betlik bullet xulosa va "bir soatlik mashq kunlab ishni tejaydi", yozma shartni ko'rsatish chegaraviy holatni ochishi, test rejasini rejalashtirish bosqichida yozib manfaatdorlar bilan bo'lishish, testlash va monitoringni kelishilgan ish ichida saqlash
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 3.1-3.2 va 3.6 (25-27, 33-34, 55-56-betlar) - tayyorgarlikning to'liq bajarilmasligining uch sababi (malaka yetishmasligi, kodga shoshilish, menejer bosimi) va WISCA / WIMP sindromi nomi, menejerga tushuntirish variantining tanlanishi; iterativ yondashuv tayyorgarlikni yo'q qilmasligi, 3-3 va 3-4-jadvallardagi to'rt ssenariyning illyustrativ narxlari (1 000 000, 875 000, 600 000, 550 000) va bo'lak-bo'lak so'rilgan narx taassuroti; talablarning 80 foizini yoki eng muhim 20 foizini oldindan belgilash qoidalari; tayyorgarlikka mehnatning 10-20 foizi va muddatning 20-30 foizi, batafsil dizayn bu ulushga kirmasligi, beqaror talabni alohida loyiha qilish
- ESLATMA: 2.2 dagi olti o'lchovli jadval, 2.4 dagi event storming tartibi, 2.7 dagi uch iste'molchi taqqoslashi va 2.10 dagi uch guruhga ajratish shu korpusning amaliy tavsiyasi, kitobdan olingan emas
- ESLATMA: 2.17 dagi tayyorgarlik byudjeti misoli (12 hafta, 4 muhandis, 48 odam-hafta) shu korpusning hisobi: kitobdan faqat foiz ulushlari olingan

---

[&larr; 1. Arxitektorning fikrlash modeli](01-arxitektorning-fikrlash-modeli.md) · [Mundarija](README.md) · [3. Qaror qabul qilish va uni hujjatlashtirish &rarr;](03-qaror-qabul-qilish-va-uni-hujjatlashtirish.md)
