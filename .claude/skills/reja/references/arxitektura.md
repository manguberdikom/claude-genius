# 3-bosqich: arxitektura qarori

Bu bosqichda rejaga **qaror** kiradi: chegaralar qayerda, qaysi mexanizm
tanlandi, nima qurbon qilindi. Pattern tanlash keyingi bosqich; hozir savol
"tizim qanday bo'ladi", "qaysi sinfda qanday kod turadi" emas.

Qoida: **eng zerikarli yechim g'olib.** Mavjud tuzilishda ishlaydigan yo'l bor
bo'lsa, yangi qatlam, yangi servis, yangi broker kiritilmaydi. Yangi mexanizm
faqat o'lchanadigan talab uni majbur qilganda qo'shiladi.

## 3.1 Avval NFR budjeti

Funksional talab "nima qiladi" ni aytadi; arxitekturani esa **raqamlar**
belgilaydi. Shu jadval rejada bo'lishi shart (noma'lum qiymat `?` bilan):

| O'lchov | Qiymat | Manba / asos |
|---|---|---|
| So'rov hajmi (RPS, o'rtacha / peak) | 40 / 400 | Actuator metrikasi, log hajmi |
| Javob budjeti (p99) | 300 ms | mahsulot talabi / mavjud SLO |
| Ma'lumot hajmi va o'sishi | 12M qator, +400k/oy | `count(*)`, jadval o'sishi |
| Konsistentlik talabi | to'lovda qat'iy, hisobotda 5 s kechikish mumkin | biznes qarori |
| Nosozlikka chidamlilik | tashqi servis 1 daqiqa yo'q bo'lsa, buyruq yo'qolmasligi kerak | biznes qarori |
| Ma'lumot yo'qolishi (RPO/RTO) | 0 / 5 daqiqa | operatsion talab |

Raqamlardan keyin napkin math qilinadi (arxitektor 8-bob): bitta so'rovga nechta
DB chaqiruvi, qancha bayt, qancha latency qo'shiladi. Natija bitta qator bo'lib
rejaga tushadi:

```
400 RPS x 3 so'rov x 2 ms = 2400 DB chaqiruvi/s -> pool 10 ta ulanish bilan
yetmaydi (hozir 10, `application.yml:22`); kerak: batch bilan 1 so'rovga
tushirish yoki pool 30.
```

Agar raqam yo'q bo'lsa, u ham qaror: `TAXMIN: peak 400 RPS` deb yoziladi va
rejaning birinchi qadami uni o'lchash bo'ladi.

## 3.2 Sifat atributidan mexanizmga

| Talab | Birinchi tanlanadigan mexanizm | Qarash kerak |
|---|---|---|
| Javob tezligi (o'qish) | indeks, proyeksiya (DTO), keyset pagination | arxitektor 23, 24-bob; patternlar 9.22, 7.7 |
| Javob tezligi (takroriy o'qish) | kesh + aniq invalidatsiya | patternlar 11-bo'lim; arxitektor 28-bob |
| O'tkazuvchanlik (yozish) | batch, partiya, asinxron | patternlar 10.20; arxitektor 18-bob |
| Tashqi servis ishonchsizligi | timeout -> retry (jitter) -> circuit breaker -> fallback, shu tartibda | patternlar 17.1, 17.2, 19.10; arxitektor 32-bob |
| Xabar yo'qolmasligi | tranzaksion outbox, idempotent consumer | patternlar 10.14, 14.18, 16.16 |
| Ikki tizimga yozish | outbox yoki saga; dual write taqiqlanadi | patternlar 10.31, 14.8, 14.9 |
| Raqobatli yangilanish | optimistik lock (`@Version`), kerak bo'lsa pessimistik | patternlar 9.23, 9.24; arxitektor 22-bob |
| O'sib boradigan jadval | indeks strategiyasi -> partitioning -> arxivlash | arxitektor 23, 26-bob |
| Xavfsiz kiritish | validatsiya chegarada, parametrli so'rov | patternlar 18-bo'lim; sonarqube 26, 37-bob |
| To'xtashsiz reliz | expand/contract migratsiya, feature flag | patternlar 10.5, 22.10; arxitektor 33-bob |
| Kuzatuvchanlik | strukturali log + metrika + trace, kardinallik chegarasi bilan | patternlar 21-bo'lim; arxitektor 30-bob |
| Legacy ni xavfsiz o'zgartirish | seam topish, branch by abstraction, strangler | patternlar 27.1, 27.3; arxitektor 34-bob |

Jadval "mexanizm" beradi, "pattern" bermaydi. Mexanizmni kodda qanday
ko'rinishga keltirish — 4-bosqich.

## 3.3 Chegara qarorlari

Uch savolga javob yoziladi:

1. **Yangi kod qayerga tushadi?** Mavjud modul ichiga, yangi paketga yoki yangi
   modulga? Asos: kim o'zgarsa, kim bilan birga o'zgaradi.
2. **Bog'liqlik yo'nalishi qanday?** Domen hech kimga qaramaydi; infrastruktura
   domenga qaraydi. Yo'nalish buzilsa — port/adapter (patternlar 12.2) yoki
   anti-corruption layer (13.7).
3. **Tranzaksiya chegarasi qayerda?** Bitta tranzaksiya = bitta agregat
   (patternlar 13.15). Tranzaksiya ichida tashqi chaqiruv — taqiq.

Chegaraga tegmaslik ham qaror: "bu o'zgarish `order` moduli ichida qoladi, yangi
modul ochilmaydi" — rejada aniq yoziladi, chunki bu keyingi savollarni yopadi.

## 3.4 ADR: qaytarib bo'lmaydigan qarorlar

ADR yoziladigan holatlar: ma'lumot sxemasi, tashqi kontrakt (API, event formati),
yangi infratuzilma komponenti, konsistentlik modeli, texnologiya tanlovi.

ADR **yozilmaydi**: fayl nomi, metod joyi, ichki refaktoring — arzon qaytariladi.

Shabloni (arxitektor 3-bob bilan bir xil):

```markdown
### ADR-1: Buyruq hodisalarini outbox orqali chiqarish

**Kontekst.** `OrderService:142` tranzaksiya ichida Kafka ga yozadi; broker
yo'q bo'lsa tranzaksiya qaytadi, broker bor-u DB qaytsa - yolg'on hodisa
(`fayl:qator`). Kunlik hajm ~120k buyruq.

**Qaror.** Hodisa bir xil tranzaksiyada `outbox` jadvaliga yoziladi; alohida
publisher uni Kafka ga jo'natadi va `sent_at` ni belgilaydi.

**Ko'rib chiqilgan variantlar.**
- Kafka transaction + DB tranzaksiyasi: ikki fazali kelishuv, ortiqcha murakkab.
- `@TransactionalEventListener(AFTER_COMMIT)`: ilova commitdan keyin o'lsa
  hodisa yo'qoladi.
- Debezium CDC: infratuzilma qo'shadi, hozirgi hajm uni oqlamaydi.

**Oqibatlar.** Kechikish ~1 s ga oshadi; consumer idempotent bo'lishi shart
(patternlar 14.18); yangi jadval va publisher kuzatuvi kerak.

**Taxminlar.** Kunlik hajm 10x oshmaydi; publisher bitta nusxada ishlaydi.

**Kuzatiladigan metrika.** `outbox_lag_seconds` p99 < 5 s; `outbox` dagi
jo'natilmagan qator soni < 100.
```

## 3.5 Nosozlik haqida fikrlash

Rejadagi har yangi tashqi chaqiruv uchun to'rt javob bo'lishi shart
(arxitektor 7, 32-bob):

| Savol | Rejada ko'rinishi |
|---|---|
| Timeout qancha? | connect 1 s, read 3 s (`application.yml` ga qo'shiladi) |
| Qayta urinish bormi? | 2 marta, exponential + jitter; faqat idempotent operatsiyada |
| Ishlamasa nima bo'ladi? | buyruq `PENDING` holatda qoladi, foydalanuvchi 202 oladi |
| Takroriy xabar kelsa? | `request_id` unique indeks -> ikkinchisi e'tiborsiz qoldiriladi |

Retry budjetini hisoblash kerak: 3 marta retry x 3 s timeout = bitta so'rov 9 s
ushlab turadi; thread pool va upstream timeout bilan solishtiriladi (retry
bo'roni: patternlar 17.42).

## 3.6 Ma'lumot va konsistentlik

- Sxema o'zgarishi bo'lsa: expand/contract tartibi (patternlar 10.5; arxitektor
  33-bob) — avval qo'shish, keyin to'ldirish, keyin kodni almashtirish, oxirida
  o'chirish. Har bosqich alohida reliz.
- Yangi so'rov bo'lsa: kutilgan plan aytiladi (`EXPLAIN ANALYZE` bilan
  tekshirish qadami qo'yiladi) va kerakli indeks nomlanadi (arxitektor 23, 24-bob).
- Katta jadvalga indeks: `CREATE INDEX CONCURRENTLY`, aks holda lock.
- Izolyatsiya darajasi o'zgarishi — ADR, chunki u xulqni o'zgartiradi
  (arxitektor 22-bob).

## 3.7 Risk ro'yxati

Har risk uchta ustun bilan yoziladi:

| Risk | Ehtimol / ta'sir | Yumshatish va qanday bilib olamiz |
|---|---|---|
| Outbox publisher sekinlashadi | o'rta / yuqori | `outbox_lag_seconds` alert > 30 s; qo'lda qayta jo'natish buyrug'i |
| Migratsiya katta jadvalni lock qiladi | past / yuqori | `CONCURRENTLY`, test bazada o'lchash, reliz oynasi |
| Consumer idempotent emas | o'rta / o'rta | unique indeks + takroriy xabar testi (testlash 11-bob) |

"Risk bor" deb yozib, yumshatish yozmaslik — risk ro'yxati emas, ogohlantirish.

## Bosqich tugaganini qanday bilamiz

- NFR jadvali to'ldirilgan (yoki `?` va o'lchash qadami bor)
- Har qaytarib bo'lmaydigan qarorga ADR bor va unda kamida ikki variant
- Har yangi tashqi chaqiruvda timeout/retry/fallback/idempotentlik javobi bor
- Tranzaksiya chegarasi aytilgan
- Risk ro'yxatida har risk uchun yumshatish va kuzatiladigan signal bor
