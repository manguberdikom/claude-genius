<!-- doc: clean-code | chapter: 48 | part: XIII. Ma'lumotnoma -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 48. Tezkor ma'lumotnoma: qoidalar va tekshiruv ro'yxatlari (Quick Reference)

<details>
<summary>Bu bobdagi 12 bo'lim</summary>

- [48.1 Nomlash qoidalari jadvali](#481-nomlash-qoidalari-jadvali)
- [48.2 Funksiya qoidalari jadvali](#482-funksiya-qoidalari-jadvali)
- [48.3 Izoh qoidalari jadvali](#483-izoh-qoidalari-jadvali)
- [48.4 Formatlash qoidalari jadvali](#484-formatlash-qoidalari-jadvali)
- [48.5 Xato bilan ishlash jadvali](#485-xato-bilan-ishlash-jadvali)
- [48.6 Hid → refaktoring moslik jadvali](#486-hid--refaktoring-moslik-jadvali)
- [48.7 Commit oldidan tekshiruv ro'yxati](#487-commit-oldidan-tekshiruv-royxati)
- [48.8 Review paytida tekshiruv ro'yxati (toza kod qismi)](#488-review-paytida-tekshiruv-royxati-toza-kod-qismi)
- [48.9 Yangi sinf uchun tekshiruv ro'yxati](#489-yangi-sinf-uchun-tekshiruv-royxati)
- [48.10 Terminlar lug'ati](#4810-terminlar-lugati)
- [48.11 Olti hujjat bilan bog'lanish xaritasi](#4811-olti-hujjat-bilan-boglanish-xaritasi)
- [48.12 Amalda qo'llash](#4812-amalda-qollash)

</details>


Bu bob kundalik ishlatish uchun: jadvallar va tekshiruv ro'yxatlari. Hujjatning qolgan qismi "nega" ga javob beradi, bu bob "qanday" ni bir sahifada beradi.

## 48.1 Nomlash qoidalari jadvali

| Element | Qoida | Misol | Bo'lim |
|---|---|---|---|
| Sinf | ot iborasi, `Manager`/`Helper` siz | `SettlementImporter` | 2.9 |
| Interfeys | domen roli, `I` prefiksisiz | `PaymentGateway` | 2.7 |
| Implementatsiya | mexanika nomi, `Impl` siz | `StripePaymentGateway` | 3.6 |
| Metod | fe'l iborasi | `reserveStockFor` | 2.9 |
| `boolean` | `is`/`has`/`can`/`should`, inkorsiz | `settled`, `canBeCancelled` | 3.1 |
| To'plam | ko'plik, tur nomisiz | `orders`, `ordersByCustomer` | 3.2 |
| Konstanta | `UPPER_SNAKE`, birlik bilan | `MAX_RETRY_ATTEMPTS` | 3.4 |
| Enum turi | birlikda ot | `SettlementStatus` | 3.5 |
| Istisno | muammo + `Exception` | `RefundExceedsPaymentException` | 3.10 |
| Generik | `T`, `K`, `V`; ko'p bo'lsa to'liq | `Repository<T, ID>` | 3.8 |
| Paket | kichik harf, xususiyat bo'yicha | `uz.shop.payment` | 3.11 |
| Birlik | nomda yoki turda | `timeoutMs`, `Duration` | 3.3 |
| Nom uzunligi | qamrovga mutanosib | `i` → `taxedOrderTotal` | 2.15 |

## 48.2 Funksiya qoidalari jadvali

| Jihat | Qoida | Bo'lim |
|---|---|---|
| Uzunlik | bir ekranga sig'adi; 4-12 qator tipik | 4.1 |
| Javobgarlik | bitta ish; ajratib bo'lmaslik sinovi | 4.2 |
| Abstraksiya | bir funksiya - bir daraja | 4.2 |
| Tartib | chaqiruvchi yuqorida (stepdown) | 4.4, 11.9 |
| Argument soni | 0-2 yaxshi, 3 asoslanadi, 4+ obyekt | 5.1 |
| Flag argumenti | yo'q; ikki metod yoki enum | 5.3 |
| Chiqish argumenti | yo'q; qaytish qiymati | 5.5 |
| `return` soni | kichik funksiyada muhim emas | 4.7 |
| Chuqurlik | ikki darajadan oshmasin | [6-bob](06-shart-mantiq-va-boshqaruv-oqimi.md), arxitektor 4.4 |
| Qavs | har doim, bir qator uchun ham | 4.8 |
| `null` | qaytarilmaydi, uzatilmaydi | 18.7 |
| To'plam qaytarish | bo'sh to'plam, `null` emas | 18.8 |

## 48.3 Izoh qoidalari jadvali

| Izoh turi | Qoldiriladi? | Bo'lim |
|---|---|---|
| Litsenziya | ha, qisqa | 8.3 |
| Qaror asosi ("nega") | ha | 8.4, arxitektor 4.5 |
| Tashqi cheklov (limit, format) | ha | 8.4 |
| Oqibat haqida ogohlantirish | ha | 8.6 |
| Formula/huquqiy asos havolasi | ha | 8.9 |
| `TODO` (ticket + shart bilan) | ha | 8.7 |
| Kodni takrorlash | yo'q | 9.2 |
| Chalg'ituvchi | yo'q | 9.3 |
| Mazmunsiz Javadoc | yo'q | 9.4 |
| O'zgarish jurnali, `@author` | yo'q | 9.5 |
| Banner, qavs izohi | yo'q | 9.7 |
| Izohga olingan kod | yo'q, darhol o'chirish | 9.8 |
| `FIXME` | yo'q, CI bloklaydi | 8.7 |

## 48.4 Formatlash qoidalari jadvali

| Jihat | Qiymat | Bo'lim |
|---|---|---|
| Indentatsiya | 4 bo'shliq, tab emas | 12.4 |
| Qator uzunligi | 100 (yoki 120) | 12.1 |
| Fayl uzunligi | 500 dan kam | 11.1 |
| A'zolar tartibi | konstanta, maydon, konstruktor, metod | 11.6 |
| Import | guruhlangan, yulduzcha yo'q | 12.7 |
| Gorizontal tekislash | ishlatilmaydi | 12.3 |
| Zanjirli chaqiruv | har bo'g'in alohida qatorda | 12.8 |
| Kodirovka | UTF-8 | 12.10 |
| Qator oxiri | LF | 12.10 |
| Formatter | Spotless, majburiy | 13.3 |
| Formatlash commiti | alohida | 13.6 |

## 48.5 Xato bilan ishlash jadvali

| Vaziyat | To'g'ri harakat | Bo'lim |
|---|---|---|
| Topilmasligi normal | `Optional.empty()` | 18.1 |
| Topilmasligi xato | domen istisnosi | 18.1 |
| Istisnoni qayta tashlash | sabab bilan (`cause`) | 19.1 |
| Resurs | `try-with-resources` | 19.4 |
| `InterruptedException` | belgini tiklash | 19.5 |
| `Throwable`/`Error` | tutilmaydi | 19.6 |
| Log va tashlash | ikkisi birga qilinmaydi | 19.7 |
| Kirish tekshiruvi | oshkor istisno, `assert` emas | 19.8 |
| Validatsiya joyi | chegara, konstruktor, domen | 5.11 |
| API xatosi | `ProblemDetail` + barqaror kod | 27.3 |
| Xato xabari | adresatga qarab uch xil | 19.10 |

## 48.6 Hid → refaktoring moslik jadvali

To'liq jadval 37.16 da. Eng ko'p ishlatiladigan o'ntasi:

| Hid | Harakat |
|---|---|
| Uzun funksiya | Extract Function |
| Sirli nom | Rename |
| Uzun parametr ro'yxati | Introduce Parameter Object |
| Ma'lumot to'dasi | Extract Class |
| Primitivlarga berilish | Replace Primitive with Object |
| Takrorlangan `switch` | Replace Conditional with Polymorphism |
| Feature envy | Move Function |
| Xabar zanjiri | Hide Delegate |
| Global ma'lumot | Encapsulate Variable |
| `null` zanjiri | Introduce Special Case |

## 48.7 Commit oldidan tekshiruv ro'yxati

- [ ] Diff ni to'liq o'qib chiqdim; har bir qator kerakli.
- [ ] Debug log, `System.out`, izohga olingan kod, yangi `TODO` qolmadi.
- [ ] Formatlash va lint o'tdi (`spotless:check`, `checkstyle:check`).
- [ ] Testlar lokalda yashil; yangi xatti-harakat uchun test bor.
- [ ] Commit atomik: formatlash va mantiq aralashmagan.
- [ ] Commit xabarida "nega" yozilgan va prefiks to'g'ri.
- [ ] Sir, token, parol diff da yo'q.
- [ ] Public API o'zgargan bo'lsa Javadoc yangilangan.

## 48.8 Review paytida tekshiruv ro'yxati (toza kod qismi)

Arxitektor hujjati 36.1-36.4 review ning nimani topishi kerakligini ko'rib chiqadi. Bu ro'yxat uning toza kodga tegishli qismi.

- [ ] Nomlar maqsadni ochib beradi; qisqartma va shovqin so'z yo'q (2-3 bob).
- [ ] Funksiyalar bitta ish qiladi; chuqurlik ikki darajadan oshmaydi (4, 6 bob).
- [ ] `boolean` va chiqish argumentlari yo'q (5.3, 5.5).
- [ ] Izohlar "nega" ni aytadi; eskirgan izoh yo'q (8-9 bob).
- [ ] `null` qaytarilmaydi; bo'sh to'plam qaytariladi (18.7-18.8).
- [ ] Istisnolar kontekst bilan; sabab uzatiladi; log bir joyda (19.1, 19.7).
- [ ] Pul `BigDecimal`/`Money`; vaqt `Clock` orqali (20.1, 22.3).
- [ ] To'plam getter lari o'zgartirilmas qaytaradi (14.7).
- [ ] `equals`/`hashCode` juftlikda va to'g'ri (15.1-15.2).
- [ ] Testlar xatti-harakatni tekshiradi; mantiq yo'q (30.4).
- [ ] Yangi bog'liqlik asoslangan (arxitektor 38.4-38.5).
- [ ] O'zgarish qaytarilishi oson (atomik, feature flag).

## 48.9 Yangi sinf uchun tekshiruv ro'yxati

- [ ] Sinf nomi ot iborasi va javobgarligini cheklaydi.
- [ ] `final` (vorislik uchun mo'ljallanmagan bo'lsa).
- [ ] Barcha maydonlar `private final`.
- [ ] Konstruktor invariantni tekshiradi; yaroqsiz obyekt yaratib bo'lmaydi.
- [ ] Tashqaridan kelgan to'plam va massivlar nusxalanadi.
- [ ] Value object bo'lsa `record`; entitet bo'lsa id bo'yicha tenglik.
- [ ] `toString` sezgir ma'lumot chiqarmaydi.
- [ ] Ko'rinish eng kichik darajada (`package-private` standart).
- [ ] Javadoc faqat public API da va shartnoma bilan.
- [ ] Bog'liqliklar konstruktor orqali, soni 4 dan kam.
- [ ] Test yozish oson bo'ldi (aks holda dizayn signali, 31.5).

## 48.10 Terminlar lug'ati

| Atama | Ma'nosi |
|---|---|
| Guard clause | metod boshida yaroqsiz holatni tekshirib erta qaytish |
| Stepdown rule | har bir funksiya o'zidan keyingi funksiyalarni chaqiradi |
| DAMP | testda tavsifiy va takrorlanadigan kodga ruxsat |
| Data clump | birga sayohat qiladigan parametr guruhi |
| Train wreck | `a.b().c().d()` shaklidagi zanjir |
| Middle man | faqat delegatsiya qiladigan sinf |
| Refused bequest | voris sinf merosni ishlatmasligi |
| Seam | xatti-harakatni almashtirish mumkin bo'lgan nuqta |
| Branch by abstraction | abstraksiya ortida bosqichma-bosqich almashtirish |
| PECS | Producer Extends, Consumer Super |
| DAMP/DRY | tavsifiylik va takrorlanmaslik muvozanati |
| Boy Scout Rule | tegilgan kodni topganingdan tozaroq qoldirish |
| Flaky test | bir xil kodda ba'zan yiqiladigan test |
| Sunk cost | sarflangan vaqt; qaror uchun argument emas |
| Noaniqlik konusi | baho aniqligi ma'lumot bilan oshishi |
| Diqqat-mana | kun bo'yi cheklangan aqliy diqqat resursi |

## 48.11 Olti hujjat bilan bog'lanish xaritasi

| Savol | Hujjat va bo'lim |
|---|---|
| Nomni qanday yozaman? | shu hujjat, 2-3 |
| Nomni domen tilidan olish | arxitektor: nomlash bo'limi |
| Funksiya qanday bo'linadi? | shu hujjat, 4-5 |
| Kognitiv yuk va chuqurlik | arxitektor: kognitiv yuk va erta qaytish |
| Izoh qoldirilsinmi? | shu hujjat, 8-9 |
| Formatlash sozlamasi | shu hujjat, 11-13 |
| `equals`/`hashCode` | shu hujjat, 15 |
| Abstraksiya va chegara | arxitektor: abstraksiya va chegara bo'limi |
| Murakkablik va texnik qarz | arxitektor: murakkablikni boshqarish bo'limi |
| Qaysi pattern kerak? | patternlar: mavzuga mos pattern bo'limi |
| SOLID va GRASP | patternlar: dizayn printsiplari bo'limi |
| Anti-pattern nomi | patternlar: anti-patternlar bo'limi |
| Xato bilan ishlash | shu hujjat, 18-19 |
| Istisno ierarxiyasi dizayni | arxitektor: istisnolar dizayni bo'limi |
| Pul, vaqt, satr, to'plam | shu hujjat, 20-23 |
| Record, sealed, `Optional`, Stream | arxitektor: zamonaviy Java bo'limi |
| Spring mexanikasi | arxitektor: Spring mexanikasi boblari |
| Spring kodi uslubi | shu hujjat, 26-27 |
| JPA mexanikasi va N+1 | arxitektor: Spring Data JPA va Hibernate bo'limi |
| JPA kodi uslubi | shu hujjat, 28 |
| PostgreSQL ichki tuzilishi | arxitektor: PostgreSQL boblari |
| Log narxi va kuzatuvchanlik | arxitektor: kuzatuvchanlik amaliyoti bo'limi |
| Log kodi uslubi | shu hujjat, 29 |
| Test strategiyasi va texnikasi | [testlash qo'llanmasi](../testing/README.md) |
| Test kodi tozaligi va TDD | shu hujjat, 30-31 |
| Kod hidi va refaktoring harakati | shu hujjat, 32-38 |
| Legacy refaktoring strategiyasi | arxitektor: legacy kod va refaktoring bo'limi |
| Build va versiya nazorati | shu hujjat, 39-41 |
| Statik tahlil vositalari | shu hujjat, 42 |
| Sonar qoidalari va quality gate | [SonarQube hujjati](../sonarqube/README.md) |
| Professional intizom | shu hujjat, 43-47 |
| Review jarayoni va yetakchilik | arxitektor: code review va texnik yetakchilik |
| Diffda xatoni ko'rish | [review hujjati](../code-review/README.md) |
| Review izohi matni va kelishmovchilik | [review hujjati](../code-review/README.md): madaniyat va til bo'limi |
| Xavfsizlik review metodikasi | [review hujjati](../code-review/README.md): xavfsizlik boblari |
| O'rganish va texnologiya tanlash | arxitektor: doimiy o'rganish bo'limi |

## 48.12 Amalda qo'llash

- [ ] 48.1-48.5 jadvallarini bitta sahifaga chiqarib, jamoa kelishuviga ilova qiling.
- [ ] 48.7 ro'yxatini pre-push hook yoki PR shabloniga kiriting.
- [ ] 48.8 ro'yxatidan jamoaga eng ko'p tegishli 10 bandni tanlab, review checklistiga qo'ying.
- [ ] 48.9 ro'yxatini yangi sinf shabloni (IDE live template) sifatida saqlang.
- [ ] 48.10 lug'atidagi atamalarni `docs/glossary.md` ga qo'shing.
- [ ] 48.11 xaritasini yangi odamning birinchi kun materialiga kiriting.
- [ ] Jadvallardagi qoidalardan mashina tekshira oladiganlarini ajratib, statik tahlilga ko'chiring.
- [ ] Har chorakda jadvallarni ko'rib chiqib, ishlamayotgan qoidalarni olib tashlang.

---

[&larr; 47. Birgalikda ishlash va o'rgatish](47-birgalikda-ishlash-va-orgatish.md) · [Mundarija](README.md) · [49. O'z-o'zini baholash: toza kod yetukligi &rarr;](49-oz-ozini-baholash-toza-kod-yetukligi.md)
