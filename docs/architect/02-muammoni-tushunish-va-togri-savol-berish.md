<!-- doc: architect | chapter: 2 | part: I. Fikrlash va qarorlar -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

# 2. Muammoni tushunish va to'g'ri savol berish (Understanding the Problem)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

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
- [2.11 Amalda qo'llash](#211-amalda-qollash)

</details>



Arxitektorning eng qimmat xatosi kod yozishda emas, talabni tushunishda sodir bo'ladi. Noto'g'ri tushunilgan talab asosida yozilgan toza, test bilan qoplangan, chiroyli kod ham yaroqsiz. Shuning uchun arxitektorning ishi klaviaturadan emas, savoldan boshlanadi. Bu bob savolni qanday berish, javobni qanday o'lchanadigan shaklga aylantirish va qachon talabni umuman rad etish kerakligi haqida.

## 2.1 Talab ortidagi haqiqiy ehtiyojni topish

Biznes odatda talabni yechim shaklida aytadi, ehtiyoj shaklida emas. "Bizga hisobot sahifasida Excel eksport tugmasi kerak" degan gap talab emas, bu allaqachon tanlangan yechim. Arxitektor shu yerda to'xtab, "nima uchun" ni so'raydi. Birinchi javob: "chunki moliya bo'limi raqamlarni ko'rishi kerak". Ikkinchi "nima uchun": "chunki ular har oy bank o'tkazmalarini tizimdagi to'lovlar bilan solishtiradi". Uchinchi "nima uchun": "chunki o'tgan yil 400 ming so'mlik farq topilgan va kim javobgar ekani aniqlanmagan".

Mana haqiqiy ehtiyoj: solishtirish (reconciliation) va audit izi. Excel tugmasi uni qondirmaydi, faqat qo'lda ishlashni osonlashtiradi. To'g'ri yechim boshqa: har kuni avtomatik solishtirish, farqlar uchun alohida jadval va to'lov holati o'zgarishining o'zgarmas tarixi. Excel esa ikkinchi darajali xususiyat bo'lib qoladi.

Qo'shimcha foydali savollar: "hozir buni qanday hal qilib turasiz", "agar biz hech narsa qilmasak nima bo'ladi", "oxirgi marta bu muammo qachon yuz bergan va qancha turdi". Oxirgi savol eng kuchlisi, chunki u talabning narxini oshkor qiladi. Agar javob "aslida hali yuz bermagan" bo'lsa, demak siz hali mavjud bo'lmagan muammoni hal qilmoqchisiz.

## 2.2 Funksional va nofunksional talablarni ajratish

Funksional talab tizim nima qilishini aytadi. Nofunksional talab buni qanday qilishini aytadi. Ikkinchisi arxitekturani birinchisidan ko'ra ko'proq belgilaydi. "Buyurtma yaratiladi" talabi uchun oddiy monolit ham, event-driven tizim ham yaroqli. Lekin "buyurtma yaratish 99 foiz hollarda 200 ms dan tez bo'lsin va ombor servisi o'chganda ham ishlashi kerak" talabi sizni sinxron chaqiruvdan voz kechishga majbur qiladi.

Amalda nofunksional talabni arxitektor o'zi qazib oladi. Buning uchun har bir funksional talabga olti o'lchov bo'yicha savol beriladi.

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

"Tez bo'lsin" talabi qabul qilinmaydi, chunki uni hech kim tekshira olmaydi. Uni o'lchanadigan shaklga aylantirish uchun to'rt narsa kerak: metrika, persentil, qiymat va o'lchash nuqtasi. "Buyurtma yaratish endpoint'i p99 latency'si 300 ms dan kam bo'lsin, server tomonda, 30 daqiqalik oynada, peak trafikda" degan gap allaqachon shartnoma.

Persentilni tanlash muhim. O'rtacha qiymat (mean) sekin so'rovlarni yashiradi: 1000 so'rovdan 990 tasi 50 ms, 10 tasi 5 s bo'lsa, o'rtacha 99 ms chiqadi va grafik sog'lom ko'rinadi, p99 esa 5 s ko'rsatadi. Agar bitta sahifa 20 ta so'rov qilsa, 300 ms lik p99 foydalanuvchining 18 foizi sekin sahifa ko'rishini bildiradi. Shuning uchun p999 ni ham belgilash kerak.

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

O'lchash nuqtasi ham shartnomaning qismi. Server tomonda o'lchangan 200 ms mijoz brauzerida 900 ms bo'lishi mumkin, chunki orada TLS handshake, DNS va mobil tarmoq bor. Agar biznes "foydalanuvchi uchun tez" desa, server uchun budjet 300 ms emas, taxminan 120 ms bo'ladi.

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

Kod va suhbat bir xil so'zlardan foydalanmasa, har bir yig'ilish tarjimaga aylanadi. Biznes "yetkazib berish" deganda kod `ShipmentDto` ni, mijoz esa "qachon keladi" ni tushunadi. Umumiy til (ubiquitous language) shu uchlikni bitta so'zga bog'laydi va o'sha so'z klass nomiga aynan tushadi.

Eng ko'p uchraydigan belgi: bitta so'z ikki xil ma'noda ishlatiladi. "Buyurtma" savdo kontekstida savatcha va narx, ombor kontekstida yig'ish ro'yxati, moliyada esa hisob-faktura asosi. Uchalasi bitta `Order` klassiga siqilsa, o'sha klass 60 maydonga ega bo'ladi va hech kim uni o'zgartirishga jur'at etmaydi. To'g'ri qaror: uch kontekst, uch model, orada aniq tarjima.

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

Event storming shu chegaralarni topishning eng tez usuli. Jarayon oddiy: devorga biznes hodisalarini o'tgan zamonda yozasiz ("to'lov tasdiqlandi", "tovar zahiraga olindi", "yetkazib berish bekor qilindi"), ularni vaqt bo'yicha tartiblaysiz, keyin har bir hodisadan oldin qaysi buyruq va qaysi qoida turganini aniqlaysiz. Ikki soatlik sessiya odatda 40 dan 80 ta hodisa beradi.

Natijada uch narsa ko'rinadi. Hodisalar zich to'planadigan joylar aggregate chegaralarini, oqim uziladigan joylar kontekst va kelajakdagi servis chegaralarini ko'rsatadi. Uchinchisi eng qimmati: hech kim javob bera olmaydigan savollar. "To'lov o'tgan, lekin tovar qolmagan bo'lsa nima qilamiz" savoliga javob yo'q bo'lsa, siz hali loyihani boshlashga tayyor emassiz.

## 2.5 Chegaraviy holatlar va istisnolarni oldindan topish

Baxtli oqim (happy path) kodning taxminan 20 foizini, chegaraviy holatlar qolganini egallaydi. Biznes faqat baxtli oqimni aytadi, qolganini arxitektor o'zi sanab chiqadi va har biriga qaror talab qiladi.

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

Taxminni ikki raqam bilan yozish kerak: bugungi va uch yildan keyingi. Bir yil juda qisqa, unda hech qanday qaror o'zgarmaydi. Besh yil juda uzoq, biznes o'sha vaqtda boshqa ish qilayotgan bo'lishi mumkin.

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

Hisob oddiy. Bitta to'lov qatori indekslar bilan taxminan 400 bayt olsa va kunda 80 ming to'lov bo'lsa, bu kuniga 32 MB, yiliga taxminan 11 GB. Uch yilda 35 GB, o'sish uch barobar bo'lsa 70 GB. Bu bitta serverda muammosiz saqlanadi, ya'ni sharding haqida o'ylash shart emas. Lekin sana bo'yicha hisobot so'rovlari bo'lsa, oylik partitioning asoslanadi: eski partitionlar sovuq saqlashga ko'chadi va `VACUUM` ishi engillashadi.

Xotira hisobi ham shunday. 2000 ta sessiya, har biri 20 KB bo'lsa, bu 40 MB heap va muammo emas. Lekin har bir sessiyada 500 elementli savatcha cache'lansa, raqam taxminan 400 MB ga chiqadi va bu JVM uchun sezilarli.

## 2.7 Kim foydalanadi: tashqi foydalanuvchi, ichki jamoa, boshqa servis

Foydalanuvchi turi API dizaynini, xatolik strategiyasini va mustahkamlik darajasini butunlay o'zgartiradi. Bitta endpoint uchun uch xil iste'molchi uch xil talab qo'yadi.

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

Har bir mezonga o'lchash usuli yozilishi kerak, aks holda u shiorga aylanadi. "Ma'lumot yo'qolmasin" mezoni uchun o'lchash usuli bu tunda ishlaydigan solishtirish jarayoni: u tashqi va ichki yozuvlarni sanab taqqoslaydi, farq nolga teng bo'lmasa ogohlantiradi. Shu o'lchov bo'lmasa, siz bilmaysiz, faqat ishonasiz.

Testlash qo'llanmasidagi performance test bo'limi shu mezonlarni avtomatik darvozaga aylantirish usulini beradi. Arxitektorning bu yerdagi ishi boshqa: mezonni shunday yozish, uni mashinani o'qiydigan shaklga aylantirish mumkin bo'lsin.

## 2.9 Noto'g'ri tushunishning narxi

Talabni noto'g'ri tushunish narxi chiziqli emas, ko'rsatkichli o'sadi. Savollar bosqichida tuzatish bir soat, dizaynda bir kun, ishlab chiqarishda esa oylar oladi, chunki o'sha paytga kelib ma'lumot noto'g'ri sxemada yotadi.

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

Arxitektorning eng kuchli vositasi "yo'q" so'zi, lekin quruq rad etish ishonchni buzadi. To'g'ri shakl uch qismdan iborat: ehtiyojni tan olish, narxni ko'rsatish va arzonroq alternativa taklif qilish.

Misol. Biznes real vaqtda yangilanadigan omborlar dashboard'ini so'raydi. Rad etish shunday ko'rinadi: "Qoldiqni kuzatish kerakligini tushunaman. Real vaqtda yangilanish WebSocket infratuzilmasi, alohida o'qish modeli va taxminan uch hafta ish talab qiladi. Boshqa variant: 30 sekundda bir yangilanadigan sahifa, bu ikki kunlik ish. Agar 30 sekund yetmasa, qaysi qaror shuncha tez qabul qilinishi kerakligini aytsangiz, shu oqim uchun alohida real vaqt kanali qilamiz."

Bu javobda hurmat, raqam va tanlov bor. Biznes odatda ikkinchi variantni oladi, chunki haqiqiy ehtiyoj 30 sekundlik yangilanish bilan qoplanadi.

Qamrovni qisqartirishning foydali usuli: talabni "birinchi relizda kerak", "uchinchi oyda kerak" va "hech qachon kerak bo'lmasligi mumkin" guruhlariga ajratish. Oxirgi guruhga tushgan talablar yozilib qo'yiladi, lekin bajarilmaydi. Uch oydan keyin ularning aksariyati o'z-o'zidan yo'qoladi va bu eng arzon yechim.

Rad etilgan talabni yozib qo'yish majburiy. Qaror hujjatida (ADR) "nimadan voz kechdik va nima uchun" bo'limi bo'lsin. Oltinchi oyda kimdir "nega bu yo'q" deb so'raganda, javob repozitoriyda turadi.

Oxirgi qoida: talabni tushunishga ikki haftadan ko'p vaqt ketsa, talab juda katta va bo'laklarga ajratilishi kerak. Bo'linmaydigan talab odatda yaxshi tushunilmagan talab.

## 2.11 Amalda qo'llash

- [ ] Hozirgi backlog'dagi eng katta uch talabni oling va har biriga uch marta "nima uchun" savolini berib, javoblarni bir betga yozing.
- [ ] Har bir talab uchun olti o'lchov jadvalini (tezlik, hajm, ishonchlilik, ma'lumot yangiligi, xavfsizlik, narx) to'ldiring va bo'sh qolgan katakchalarni biznesdan so'rang.
- [ ] Eng muhim ikki endpoint uchun p99 va p999 qiymatini belgilab, `percentiles-histogram` va `slo` sozlamalarini yoqing, keyin bir hafta haqiqiy raqamni kuzatib SLO ni to'g'rilang.
- [ ] Eng katta uch jadvalning hozirgi hajmini va bitta qator o'rtacha bayt hajmini o'lchab, uch yillik o'sish prognozini yozib qo'ying.
- [ ] Bitta asosiy biznes oqimi uchun kamida 10 ta chegaraviy holatni sanab chiqing va har biriga qaror yozing, qarorsiz qolganini xavf ro'yxatiga kiritasiz.
- [ ] Ikki soatlik event storming sessiyasini o'tkazing va natijada paydo bo'lgan javobsiz savollarni alohida ro'yxatga oling.
- [ ] Kodingizdagi eng katta entity'ni oling va unda necha xil kontekst aralashganini aniqlang, kamida bitta kontekstni alohida modelga ajratish rejasini yozing.
- [ ] Rad etilgan yoki kechiktirilgan talablar uchun ADR shabloniga "nimadan voz kechdik" bo'limini qo'shib, oxirgi uch qarorni retrospektiv yozib chiqing.

---

[&larr; 1. Arxitektorning fikrlash modeli](01-arxitektorning-fikrlash-modeli.md) · [Mundarija](README.md) · [3. Qaror qabul qilish va uni hujjatlashtirish &rarr;](03-qaror-qabul-qilish-va-uni-hujjatlashtirish.md)
