<!-- doc: clean-code | chapter: 48 | part: XIII. Ma'lumotnoma -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

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


Bu bob kundalik ishlatish uchun: jadvallar va tekshiruv ro'yxatlari. Hujjatning qolgan qismi "nega" ga javob beradi, bu bob "qanday" ni bir sahifada beradi. Bu bobda yangi qoida yo'q: har bir qator korpusning o'z bo'limidan olingan va shu bo'limga havola qiladi, dalil va manba esa o'sha bo'limda turadi.

## 48.1 Nomlash qoidalari jadvali

| Element | Qoida | Misol | Bo'lim |
|---|---|---|---|
| Sinf | ot iborasi, `Manager`/`Helper` siz | `SettlementImporter` | [2.9](02-nomlash-qoidalari-maqsadni-ochib-beruvchi.md#29-sinf-nomi-ot-metod-nomi-fel-getter-konvensiyasi) |
| Interfeys | domen roli, `I` prefiksisiz | `PaymentGateway` | [2.7](02-nomlash-qoidalari-maqsadni-ochib-beruvchi.md#27-kodlash-va-prefikslar-hungarian-notation-m_-i-prefiksi) |
| Implementatsiya | mexanika nomi; `Impl` faqat bitta holatda haqli | `StripePaymentGateway` | [3.6](03-nom-turlari-boyicha-aniq-konvensiyalar.md#36-interfeys-va-implementatsiya-nomlari-impl-qachon-haqli) |
| Metod | fe'l iborasi | `reserveStockFor` | [2.9](02-nomlash-qoidalari-maqsadni-ochib-beruvchi.md#29-sinf-nomi-ot-metod-nomi-fel-getter-konvensiyasi) |
| `boolean` | `is`/`has`/`can`/`should`, inkorsiz | `settled`, `canBeCancelled` | [3.1](03-nom-turlari-boyicha-aniq-konvensiyalar.md#31-mantiqiy-nomlar-is-has-can-should-va-inkor-tuzogi) |
| To'plam | ko'plik, tur nomisiz | `orders`, `ordersByCustomer` | [3.2](03-nom-turlari-boyicha-aniq-konvensiyalar.md#32-toplam-massiv-va-oqim-nomlari) |
| Konstanta | `UPPER_SNAKE`, birlik bilan | `MAX_RETRY_ATTEMPTS` | [3.4](03-nom-turlari-boyicha-aniq-konvensiyalar.md#34-konstanta-static-final-va-enum-azolari) |
| Enum turi | birlikda ot | `SettlementStatus` | [3.5](03-nom-turlari-boyicha-aniq-konvensiyalar.md#35-enum-turi-va-holat-nomlari) |
| Istisno | muammo + `Exception` | `RefundExceedsPaymentException` | [3.10](03-nom-turlari-boyicha-aniq-konvensiyalar.md#310-istisno-sinflari-nomlari) |
| Generik | `T`, `K`, `V`; ko'p bo'lsa to'liq | `Repository<T, ID>` | [3.8](03-nom-turlari-boyicha-aniq-konvensiyalar.md#38-generik-tur-parametrlari) |
| Paket | kichik harf, xususiyat bo'yicha | `uz.shop.payment` | [3.11](03-nom-turlari-boyicha-aniq-konvensiyalar.md#311-paket-modul-va-artefakt-nomlari) |
| Birlik | nomda yoki turda | `timeoutMs`, `Duration` | [3.3](03-nom-turlari-boyicha-aniq-konvensiyalar.md#33-birlik-nomda-timeoutms-sizebytes-priceminor) |
| Nom uzunligi | qamrovga mutanosib | `i` -> `taxedOrderTotal` | [2.15](02-nomlash-qoidalari-maqsadni-ochib-beruvchi.md#215-nom-uzunligi-qamrovga-mutanosib) |
| Bitta tushunchaga bitta so'z | `get`/`find`/`fetch` aralashmaydi | `findById`, `getTotal` | [2.11](02-nomlash-qoidalari-maqsadni-ochib-beruvchi.md#211-bitta-tushunchaga-bitta-soz) |

## 48.2 Funksiya qoidalari jadvali

| Jihat | Qoida | Bo'lim |
|---|---|---|
| Uzunlik | 100 qator bo'lmasin, 20 qator deyarli hech qachon bo'lmasin | [4.1](04-funksiya-kichiklik-va-bitta-ish.md#41-birinchi-qoida-kichik-ikkinchi-qoida-yana-kichikroq) |
| Javobgarlik | bitta ish; ajratib bo'lmaslik sinovi | [4.2](04-funksiya-kichiklik-va-bitta-ish.md#42-bitta-ish-qiladi-ni-qanday-tekshirish) |
| Abstraksiya | bir funksiya - bir daraja | [4.2](04-funksiya-kichiklik-va-bitta-ish.md#42-bitta-ish-qiladi-ni-qanday-tekshirish) |
| Tartib | chaqiruvchi yuqorida (stepdown) | [4.4](04-funksiya-kichiklik-va-bitta-ish.md#44-pastga-tushish-qoidasi-va-gazeta-metaforasi), [11.9](11-vertikal-formatlash.md#119-vertikal-tartib-chaqiruvchi-yuqorida) |
| Argument soni | 0-2 yaxshi, 3 asoslanadi, 4+ argument obyekti | [5.1](05-funksiya-argumentlari.md#51-argument-soni-nol-bir-ikki-uch-va-undan-keyin) |
| Flag argumenti | yo'q; ikki metod yoki enum | [5.3](05-funksiya-argumentlari.md#53-flag-argumenti-va-uni-ikki-funksiyaga-bolish) |
| Chiqish argumenti | yo'q; qaytish qiymati | [5.5](05-funksiya-argumentlari.md#55-chiqish-argumenti-va-void-dan-qaytishga-otish) |
| `return` soni | kichik funksiyada muhim emas | [4.7](04-funksiya-kichiklik-va-bitta-ish.md#47-funksiya-qaytish-nuqtalari-bitta-return-afsonasi) |
| Chuqurlik | ichma-ich daraja birdan yoki ikkidan oshmasin | [4.1](04-funksiya-kichiklik-va-bitta-ish.md#41-birinchi-qoida-kichik-ikkinchi-qoida-yana-kichikroq), [6-bob](06-shart-mantiq-va-boshqaruv-oqimi.md) |
| Qavs | har doim, bir qator uchun ham | [4.8](04-funksiya-kichiklik-va-bitta-ish.md#48-funksiya-ichidagi-bosh-joy-blok-va-qavs) |
| `null` | qaytarilmaydi, uzatilmaydi | [18.7](18-xato-bilan-ishlash-qoidalari.md#187-null-qaytarmaslik-va-null-uzatmaslik) |
| To'plam qaytarish | bo'sh to'plam, `null` emas | [18.8](18-xato-bilan-ishlash-qoidalari.md#188-bosh-toplam-qaytarish-qoidasi) |

## 48.3 Izoh qoidalari jadvali

| Izoh turi | Qoldiriladi? | Bo'lim |
|---|---|---|
| Litsenziya | ha, qisqa | [8.3](08-izoh-qoidalari-yaxshi-izohlar.md#83-huquqiy-va-litsenziya-izohlari) |
| Qaror asosi ("nega") | ha | [8.4](08-izoh-qoidalari-yaxshi-izohlar.md#84-malumot-beruvchi-va-maqsadni-tushuntiruvchi-izoh) |
| Tashqi cheklov (limit, format) | ha | [8.4](08-izoh-qoidalari-yaxshi-izohlar.md#84-malumot-beruvchi-va-maqsadni-tushuntiruvchi-izoh) |
| Oqibat haqida ogohlantirish | ha | [8.6](08-izoh-qoidalari-yaxshi-izohlar.md#86-oqibat-haqida-ogohlantirish) |
| Formula/huquqiy asos havolasi | ha | [8.9](08-izoh-qoidalari-yaxshi-izohlar.md#89-formula-standart-va-huquqiy-asos-havolasi) |
| `TODO` (ticket + shart bilan) | ha | [8.7](08-izoh-qoidalari-yaxshi-izohlar.md#87-todo-fixme-va-ularning-hayot-muddati) |
| Kodni takrorlash | yo'q | [9.2](09-yomon-izohlar-katalogi.md#92-ortiqcha-izoh-kodni-sozma-soz-takrorlash) |
| Chalg'ituvchi | yo'q | [9.3](09-yomon-izohlar-katalogi.md#93-chalgituvchi-izoh) |
| Mazmunsiz Javadoc | yo'q | [9.4](09-yomon-izohlar-katalogi.md#94-majburiy-izoh-har-bir-maydonga-javadoc) |
| O'zgarish jurnali, `@author` | yo'q | [9.5](09-yomon-izohlar-katalogi.md#95-jurnal-izohlari-va-mualliflik-imzolari) |
| Banner, qavs izohi | yo'q | [9.7](09-yomon-izohlar-katalogi.md#97-pozitsiya-belgilari-va-qavs-yopilishi-izohlari) |
| Izohga olingan kod | yo'q, darhol o'chirish | [9.8](09-yomon-izohlar-katalogi.md#98-izohga-olingan-kod) |
| `FIXME` | yo'q: "buzilgan kod merge qilindi" degani | [8.7](08-izoh-qoidalari-yaxshi-izohlar.md#87-todo-fixme-va-ularning-hayot-muddati) |

## 48.4 Formatlash qoidalari jadvali

| Jihat | Qiymat | Bo'lim |
|---|---|---|
| Indentatsiya | 4 bo'shliq, tab emas | [12.4](12-gorizontal-formatlash-va-kod-uslubi.md#124-indentatsiya-va-uni-buzmaslik) |
| Qator uzunligi | 100 yoki 120; muhimi chegara borligi | [12.1](12-gorizontal-formatlash-va-kod-uslubi.md#121-qator-uzunligi-chegarasi-va-uni-tanlash) |
| Fayl uzunligi | tipik 200 dan kichik, yuqori chegara 500 | [11.1](11-vertikal-formatlash.md#111-fayl-olchami-va-sinf-uzunligi) |
| Vertikal zichlik | birga o'qiladigan qatorlar ajratilmaydi | [11.4](11-vertikal-formatlash.md#114-vertikal-zichlik-birga-oqiladigan-qatorlarni-ajratmaslik) |
| A'zolar tartibi | konstanta, maydon, konstruktor, metod | [11.6](11-vertikal-formatlash.md#116-maydonlar-joylashuvi-va-azolar-tartibi) |
| Import | guruhlangan, yulduzcha yo'q | [12.7](12-gorizontal-formatlash-va-kod-uslubi.md#127-import-tartibi-va-yulduzcha-import) |
| Gorizontal tekislash | ishlatilmaydi | [12.3](12-gorizontal-formatlash-va-kod-uslubi.md#123-gorizontal-tekislash-nega-zarar-qiladi) |
| Zanjirli chaqiruv | har bo'g'in alohida qatorda | [12.8](12-gorizontal-formatlash-va-kod-uslubi.md#128-zanjirli-chaqiruv-va-oqimni-bolish) |
| Kodirovka | UTF-8 | [12.10](12-gorizontal-formatlash-va-kod-uslubi.md#1210-fayl-kodirovkasi-qator-oxiri-va-oxirgi-bosh-qator) |
| Qator oxiri | LF | [12.10](12-gorizontal-formatlash-va-kod-uslubi.md#1210-fayl-kodirovkasi-qator-oxiri-va-oxirgi-bosh-qator) |
| Formatter | Spotless, majburiy | [13.3](13-formatlashni-avtomatlashtirish-va-diff.md#133-spotless-va-google-java-format-ornatish) |
| Formatlash commiti | alohida | [13.6](13-formatlashni-avtomatlashtirish-va-diff.md#136-formatlash-ozgarishini-mantiq-ozgarishidan-ajratish) |

## 48.5 Xato bilan ishlash jadvali

| Vaziyat | To'g'ri harakat | Bo'lim |
|---|---|---|
| Topilmasligi normal | `Optional.empty()` | [18.1](18-xato-bilan-ishlash-qoidalari.md#181-xato-kodi-emas-istisno) |
| Topilmasligi xato | domen istisnosi | [18.1](18-xato-bilan-ishlash-qoidalari.md#181-xato-kodi-emas-istisno) |
| Istisnoni qayta tashlash | sabab bilan (`cause`) | [19.1](19-istisno-mexanikasi-va-resurslar.md#191-stack-trace-ni-yoqotmaslik-wrap-va-rethrow) |
| Resurs | `try-with-resources` | [19.4](19-istisno-mexanikasi-va-resurslar.md#194-try-with-resources-va-autocloseable) |
| `InterruptedException` | belgini tiklash | [19.5](19-istisno-mexanikasi-va-resurslar.md#195-interruptedexception-ni-togri-qayta-tiklash) |
| `Throwable`/`Error` | tutilmaydi | [19.6](19-istisno-mexanikasi-va-resurslar.md#196-throwable-error-va-outofmemoryerror-siyosati) |
| Log va tashlash | ikkisi birga qilinmaydi | [19.7](19-istisno-mexanikasi-va-resurslar.md#197-log-qilish-yoki-tashlash-ikkisini-birga-qilmaslik) |
| Kirish tekshiruvi | oshkor istisno, `assert` emas | [19.8](19-istisno-mexanikasi-va-resurslar.md#198-assertion-va--ea-qachon-haqli) |
| Validatsiya joyi | chegara, konstruktor, domen | [5.11](05-funksiya-argumentlari.md#511-argumentni-tekshirish-joyi-chegara-konstruktor-domen) |
| API xatosi | `ProblemDetail` + barqaror kod | [27.3](27-rest-api-kodining-oqilishi.md#273-xato-javobi-formati-problemdetail-va-exceptionhandler) |
| Xato xabari | adresatga qarab uch xil | [19.10](19-istisno-mexanikasi-va-resurslar.md#1910-xato-xabari-matni-uch-xil-adresat) |
| `finally` ichida `return` | yo'q: istisnoni bostiradi | [19.3](19-istisno-mexanikasi-va-resurslar.md#193-finally-ichidagi-return-va-bostirilgan-istisno) |

## 48.6 Hid → refaktoring moslik jadvali

To'liq jadval [37.16](37-refaktoring-harakatlari-katalogi-iii-shart.md#3716-refaktoring-harakatini-tanlash-jadvali) da: u Fowler ning hid va harakat juftliklari ro'yxatiga tayanadi. Eng ko'p ishlatiladigan o'ntasi:

| Hid | Harakat |
|---|---|
| [Uzun funksiya](32-kod-hidlari-katalogi-i-nom-funksiya-malumot.md#323-uzun-funksiya-long-function) | [Extract Function](35-refaktoring-harakatlari-katalogi-i-funksiya.md#351-funksiya-ajratish-extract-function) |
| [Sirli nom](32-kod-hidlari-katalogi-i-nom-funksiya-malumot.md#321-sirli-nom-mysterious-name) | [Rename](35-refaktoring-harakatlari-katalogi-i-funksiya.md#357-ozgaruvchini-qayta-nomlash-rename-variable--rename-field) |
| [Uzun parametr ro'yxati](05-funksiya-argumentlari.md#51-argument-soni-nol-bir-ikki-uch-va-undan-keyin) | [Introduce Parameter Object](35-refaktoring-harakatlari-katalogi-i-funksiya.md#358-parametr-obyektini-kiritish-introduce-parameter-object) |
| [Ma'lumot to'dasi](32-kod-hidlari-katalogi-i-nom-funksiya-malumot.md#326-malumot-todasi-data-clumps) | [Extract Class](36-refaktoring-harakatlari-katalogi-ii-malumot.md#361-sinf-ajratish-extract-class) |
| [Primitivlarga berilish](37-refaktoring-harakatlari-katalogi-iii-shart.md#3716-refaktoring-harakatini-tanlash-jadvali) | [Replace Primitive with Object](36-refaktoring-harakatlari-katalogi-ii-malumot.md#368-primitivni-obyektga-almashtirish-replace-primitive-with-object) |
| [Takrorlangan `switch`](32-kod-hidlari-katalogi-i-nom-funksiya-malumot.md#327-takrorlangan-switch-repeated-switches) | [Replace Conditional with Polymorphism](37-refaktoring-harakatlari-katalogi-iii-shart.md#374-shartni-polimorfizmga-almashtirish-replace-conditional-with-polymorphism) |
| [Feature envy](37-refaktoring-harakatlari-katalogi-iii-shart.md#3716-refaktoring-harakatini-tanlash-jadvali) | [Move Function](35-refaktoring-harakatlari-katalogi-i-funksiya.md#3512-funksiyani-kochirish-move-function) |
| [Xabar zanjiri](32-kod-hidlari-katalogi-i-nom-funksiya-malumot.md#3211-uzun-xabar-zanjiri-message-chains) | [Hide Delegate](36-refaktoring-harakatlari-katalogi-ii-malumot.md#363-delegatni-yashirish-hide-delegate) |
| [Global ma'lumot](32-kod-hidlari-katalogi-i-nom-funksiya-malumot.md#324-global-malumot-global-data) | [Encapsulate Variable](35-refaktoring-harakatlari-katalogi-i-funksiya.md#356-ozgaruvchini-inkapsulyatsiya-qilish-encapsulate-variable) |
| [`null` zanjiri](06-shart-mantiq-va-boshqaruv-oqimi.md#68-null-tekshiruvi-zinapoyasi-va-undan-chiqish) | [Introduce Special Case](37-refaktoring-harakatlari-katalogi-iii-shart.md#375-maxsus-holatni-kiritish-introduce-special-case) |

## 48.7 Commit oldidan tekshiruv ro'yxati

- [ ] Diff ni to'liq o'qib chiqdim; har bir qator kerakli ([41.6](41-ozgarishni-kiritish-jarayoni-kichik-qadamlar.md#416-ozini-review-qilish-royxati)).
- [ ] Debug log, `System.out`, izohga olingan kod qolmadi ([9.8](09-yomon-izohlar-katalogi.md#98-izohga-olingan-kod), [29.1](29-log-kodining-tozaligi.md#291-slf4j-parametrlangan-xabar-va-satr-birlashtirmaslik)).
- [ ] Yangi `TODO` shartsiz emas; `FIXME` yo'q ([8.7](08-izoh-qoidalari-yaxshi-izohlar.md#87-todo-fixme-va-ularning-hayot-muddati)).
- [ ] Formatlash va lint o'tdi ([13.3](13-formatlashni-avtomatlashtirish-va-diff.md#133-spotless-va-google-java-format-ornatish), [42.3](42-statik-tahlil-va-avtomatik-qoidalar.md#423-spotbugs-pmd-va-checkstyle-rollari)).
- [ ] Testlar lokalda yashil; yangi xatti-harakat uchun test bor ([30.1](30-test-kodi-ham-ishlab-chiqarish-kodi.md#301-toza-test-nega-kod-bazasini-saqlab-qoladi)).
- [ ] Commit atomik: formatlash va mantiq aralashmagan ([40.1](40-versiya-nazorati-gigiyenasi.md#401-atomik-commit-bitta-mantiqiy-ozgarish), [13.6](13-formatlashni-avtomatlashtirish-va-diff.md#136-formatlash-ozgarishini-mantiq-ozgarishidan-ajratish)).
- [ ] Commit xabarida "nega" yozilgan va prefiks to'g'ri ([40.2](40-versiya-nazorati-gigiyenasi.md#402-commit-xabari-tuzilishi), [40.3](40-versiya-nazorati-gigiyenasi.md#403-conventional-commits-va-avtomatik-changelog)).
- [ ] Sir, token, parol diff da yo'q ([40.8](40-versiya-nazorati-gigiyenasi.md#408-tarixdan-sirni-ochirish-va-uning-chegarasi)).
- [ ] Public API o'zgargan bo'lsa Javadoc yangilangan ([10.3](10-javadoc-va-api-hujjati.md#103-param-return-throws-toliqligi)).

## 48.8 Review paytida tekshiruv ro'yxati (toza kod qismi)

Arxitektor hujjati review ning nimani topishi va nimani topmasligi kerakligini ko'rib chiqadi ([arxitektor 36.1](../architect/36-code-review-va-jamoada-texnik-yetakchilik.md#361-code-review-nimani-topishi-kerak-xatti-harakat-chegara-nom-xavfsizlik) - [36.4](../architect/36-code-review-va-jamoada-texnik-yetakchilik.md#364-majburiy-va-ixtiyoriy-izohlarni-ajratish)). Bu ro'yxat uning toza kodga tegishli qismi.

- [ ] Nomlar maqsadni ochib beradi; qisqartma va shovqin so'z yo'q ([2-bob](02-nomlash-qoidalari-maqsadni-ochib-beruvchi.md), [3-bob](03-nom-turlari-boyicha-aniq-konvensiyalar.md)).
- [ ] Funksiyalar bitta ish qiladi; chuqurlik ikki darajadan oshmaydi ([4.2](04-funksiya-kichiklik-va-bitta-ish.md#42-bitta-ish-qiladi-ni-qanday-tekshirish), [4.1](04-funksiya-kichiklik-va-bitta-ish.md#41-birinchi-qoida-kichik-ikkinchi-qoida-yana-kichikroq)).
- [ ] `boolean` va chiqish argumentlari yo'q ([5.3](05-funksiya-argumentlari.md#53-flag-argumenti-va-uni-ikki-funksiyaga-bolish), [5.5](05-funksiya-argumentlari.md#55-chiqish-argumenti-va-void-dan-qaytishga-otish)).
- [ ] Izohlar "nega" ni aytadi; eskirgan izoh yo'q ([8.4](08-izoh-qoidalari-yaxshi-izohlar.md#84-malumot-beruvchi-va-maqsadni-tushuntiruvchi-izoh), [9.3](09-yomon-izohlar-katalogi.md#93-chalgituvchi-izoh)).
- [ ] `null` qaytarilmaydi; bo'sh to'plam qaytariladi ([18.7](18-xato-bilan-ishlash-qoidalari.md#187-null-qaytarmaslik-va-null-uzatmaslik), [18.8](18-xato-bilan-ishlash-qoidalari.md#188-bosh-toplam-qaytarish-qoidasi)).
- [ ] Istisnolar kontekst bilan; sabab uzatiladi; log bir joyda ([19.1](19-istisno-mexanikasi-va-resurslar.md#191-stack-trace-ni-yoqotmaslik-wrap-va-rethrow), [19.7](19-istisno-mexanikasi-va-resurslar.md#197-log-qilish-yoki-tashlash-ikkisini-birga-qilmaslik)).
- [ ] Pul `BigDecimal`/`Money`; vaqt `Clock` orqali ([20.1](20-primitiv-son-va-pul.md#201-pul-uchun-double-ishlatmaslik), [22.3](22-sana-vaqt-va-mintaqa.md#223-clock-ni-inyeksiya-qilish-va-testlanadigan-vaqt)).
- [ ] To'plam getter lari o'zgartirilmas qaytaradi ([14.7](14-obyekt-va-malumot-tuzilmasi-inkapsulyatsiya.md#147-ichki-toplamni-oshkor-qilish-va-himoyalangan-nusxa)).
- [ ] `equals`/`hashCode` juftlikda va to'g'ri ([15.1](15-tenglik-hash-va-obyekt-shartnomalari.md#151-equals-shartnomasi-besh-qoida), [15.2](15-tenglik-hash-va-obyekt-shartnomalari.md#152-hashcode-shartnomasi-va-equals-bilan-bogliqligi)).
- [ ] Testlar xatti-harakatni tekshiradi; mantiq yo'q ([30.4](30-test-kodi-ham-ishlab-chiqarish-kodi.md#304-testda-mantiq-bolmasligi)).
- [ ] Yangi bog'liqlik asoslangan ([arxitektor 38.4](../architect/38-doimiy-organish-va-texnologiya-tanlash.md#384-yangi-kutubxonani-baholash-mezonlari-qollab-quvvatlash-bogliqlik-chiqish-yoli), [38.5](../architect/38-doimiy-organish-va-texnologiya-tanlash.md#385-bogliqlik-qoshishning-yashirin-narxi-va-uni-yangilash-majburiyati)).
- [ ] O'zgarish qaytarilishi oson: atomik commit, feature flag ([40.1](40-versiya-nazorati-gigiyenasi.md#401-atomik-commit-bitta-mantiqiy-ozgarish), [41.5](41-ozgarishni-kiritish-jarayoni-kichik-qadamlar.md#415-yarim-ishni-boshqarish-va-feature-flag)).

## 48.9 Yangi sinf uchun tekshiruv ro'yxati

- [ ] Sinf nomi ot iborasi va javobgarligini cheklaydi ([2.9](02-nomlash-qoidalari-maqsadni-ochib-beruvchi.md#29-sinf-nomi-ot-metod-nomi-fel-getter-konvensiyasi)).
- [ ] `final` (vorislik uchun mo'ljallanmagan bo'lsa) ([17.1](17-vorislik-kompozitsiya-va-polimorfizm.md#171-vorislik-uchun-dizayn-qilish-yoki-final-qilish)).
- [ ] Barcha maydonlar `private final` ([16.1](16-ozgarmaslik-va-holat-boshqaruvi-kod.md#161-final-maydon-final-sinf-va-haqiqiy-ozgarmaslik)).
- [ ] Konstruktor invariantni tekshiradi; yaroqsiz obyekt yaratib bo'lmaydi ([14.9](14-obyekt-va-malumot-tuzilmasi-inkapsulyatsiya.md#149-obyekt-oz-invariantini-qanday-himoya-qiladi), [5.11](05-funksiya-argumentlari.md#511-argumentni-tekshirish-joyi-chegara-konstruktor-domen)).
- [ ] Tashqaridan kelgan to'plam va massivlar nusxalanadi ([14.7](14-obyekt-va-malumot-tuzilmasi-inkapsulyatsiya.md#147-ichki-toplamni-oshkor-qilish-va-himoyalangan-nusxa), [16.2](16-ozgarmaslik-va-holat-boshqaruvi-kod.md#162-chuqur-va-sayoz-ozgarmaslik)).
- [ ] Value object bo'lsa `record`; entitet bo'lsa id bo'yicha tenglik ([15.5](15-tenglik-hash-va-obyekt-shartnomalari.md#155-entitet-va-value-object-tengligi-farqi)).
- [ ] `toString` sezgir ma'lumot chiqarmaydi ([15.7](15-tenglik-hash-va-obyekt-shartnomalari.md#157-tostring-foydali-xavfsiz-mantiqda-ishlatilmaydigan)).
- [ ] Ko'rinish eng kichik darajada (`package-private` standart) ([14.6](14-obyekt-va-malumot-tuzilmasi-inkapsulyatsiya.md#146-maydon-korinishi-public-maydon-package-private-final)).
- [ ] Javadoc faqat public API da va shartnoma bilan ([10.1](10-javadoc-va-api-hujjati.md#101-javadoc-kimga-yoziladi-va-qayerga-yozilmaydi), [10.4](10-javadoc-va-api-hujjati.md#104-shartnoma-yozish-oldin-shart-keyin-shart-invariant)).
- [ ] Bog'liqliklar konstruktor orqali; soni to'rtdan oshsa sinf ko'p ish qilyapti ([26.1](26-spring-kodining-tozaligi.md#261-konstruktor-inyeksiyasi-va-final-maydon), [5.1](05-funksiya-argumentlari.md#51-argument-soni-nol-bir-ikki-uch-va-undan-keyin)).
- [ ] Test yozish oson bo'ldi (aks holda dizayn signali, [31.5](31-tdd-intizomi-va-kod-dizayniga-tasiri.md#315-test-yozish-qiyin-bolsa-dizayn-signal-beradi)).

## 48.10 Terminlar lug'ati

| Atama | Ma'nosi | Bo'lim |
|---|---|---|
| Guard clause | metod boshida yaroqsiz holatni tekshirib erta qaytish | [37.3](37-refaktoring-harakatlari-katalogi-iii-shart.md#373-ichma-ich-shartni-guard-clause-ga-almashtirish) |
| Stepdown rule | har bir funksiya o'zidan keyingi funksiyalarni chaqiradi | [4.4](04-funksiya-kichiklik-va-bitta-ish.md#44-pastga-tushish-qoidasi-va-gazeta-metaforasi), [11.9](11-vertikal-formatlash.md#119-vertikal-tartib-chaqiruvchi-yuqorida) |
| DAMP | testda tavsifiy va takrorlanadigan kodga ruxsat; DRY bilan muvozanatda | [30.2](30-test-kodi-ham-ishlab-chiqarish-kodi.md#302-dry-va-damp-muvozanati-testda) |
| Data clump | birga sayohat qiladigan parametr guruhi | [32.6](32-kod-hidlari-katalogi-i-nom-funksiya-malumot.md#326-malumot-todasi-data-clumps) |
| Train wreck | `a.b().c().d()` shaklidagi zanjir | [14.4](14-obyekt-va-malumot-tuzilmasi-inkapsulyatsiya.md#144-poyezd-avariyasi-va-tuzilmani-yashirish) |
| Middle man | faqat delegatsiya qiladigan sinf | [32.12](32-kod-hidlari-katalogi-i-nom-funksiya-malumot.md#3212-vositachi-middle-man) |
| Refused bequest | voris sinf merosni ishlatmasligi | [33.5](33-kod-hidlari-katalogi-ii-sinf-ierarxiya.md#335-rad-etilgan-meros-refused-bequest) |
| Seam | xatti-harakatni almashtirish mumkin bo'lgan nuqta | [arxitektor 34.4](../architect/34-legacy-kod-va-bosqichma-bosqich-refaktoring.md#344-chok-seam-topish-ozgarishni-kiritish-mumkin-bolgan-nuqta) |
| Branch by abstraction | abstraksiya ortida bosqichma-bosqich almashtirish | [38.5](38-refaktoringni-xavfsiz-bajarish.md#385-katta-refaktoringni-bolish-abstraksiya-orqali-shox) |
| PECS | Producer Extends, Consumer Super | [23.8](23-toplamlar-va-generiklar-gigiyenasi.md#238-wildcard-qoidalari-pecs) |
| Boy Scout Rule | tegilgan kodni topganingdan tozaroq qoldirish | [1.4](01-toza-kod-nima-va-nega-qimmat.md#14-skaut-qoidasi-va-imkoniyatli-refaktoring) |
| Flaky test | bir xil kodda ba'zan yiqiladigan test | [testlash 16.1](../testing/16-flaky-testlar-test-qarzi-va-test-kodini.md#161-flaky-test-nima-va-nega-eng-qimmat-muammo) |
| Sunk cost | sarflangan vaqt; qaror uchun argument emas | [46.5](46-vaqt-diqqat-va-mashq.md#465-kor-yolak-va-botqoqdan-chiqish) |
| Noaniqlik konusi | baho aniqligi ma'lumot bilan oshishi | [45.4](45-baholash-muddat-va-bosim.md#454-katta-ishni-baholash-va-noaniqlik-konusi) |
| Diqqat-mana | kun bo'yi cheklangan aqliy diqqat resursi (korpusning metaforasi) | [46.1](46-vaqt-diqqat-va-mashq.md#461-diqqat-resursi-va-uni-sarflash) |

## 48.11 Olti hujjat bilan bog'lanish xaritasi

| Savol | Hujjat va bo'lim |
|---|---|
| Nomni qanday yozaman? | shu hujjat, [2-bob](02-nomlash-qoidalari-maqsadni-ochib-beruvchi.md), [3-bob](03-nom-turlari-boyicha-aniq-konvensiyalar.md) |
| Nomni domen tilidan olish | arxitektor: nomlash bo'limi |
| Funksiya qanday bo'linadi? | shu hujjat, [4-bob](04-funksiya-kichiklik-va-bitta-ish.md), [5-bob](05-funksiya-argumentlari.md) |
| Kognitiv yuk va chuqurlik | arxitektor: kognitiv yuk va erta qaytish |
| Izoh qoldirilsinmi? | shu hujjat, [8-bob](08-izoh-qoidalari-yaxshi-izohlar.md), [9-bob](09-yomon-izohlar-katalogi.md) |
| Formatlash sozlamasi | shu hujjat, [11-bob](11-vertikal-formatlash.md), [12-bob](12-gorizontal-formatlash-va-kod-uslubi.md), [13-bob](13-formatlashni-avtomatlashtirish-va-diff.md) |
| `equals`/`hashCode` | shu hujjat, [15-bob](15-tenglik-hash-va-obyekt-shartnomalari.md) |
| Abstraksiya va chegara | arxitektor: abstraksiya va chegara bo'limi |
| Murakkablik va texnik qarz | arxitektor: murakkablikni boshqarish bo'limi |
| Qaysi pattern kerak? | patternlar: mavzuga mos pattern bo'limi |
| SOLID va GRASP | patternlar: dizayn printsiplari bo'limi |
| Anti-pattern nomi | patternlar: anti-patternlar bo'limi |
| Xato bilan ishlash | shu hujjat, [18-bob](18-xato-bilan-ishlash-qoidalari.md), [19-bob](19-istisno-mexanikasi-va-resurslar.md) |
| Istisno ierarxiyasi dizayni | arxitektor: istisnolar dizayni bo'limi |
| Pul, vaqt, satr, to'plam | shu hujjat, [20-bob](20-primitiv-son-va-pul.md), [21-bob](21-satr-matn-va-regex.md), [22-bob](22-sana-vaqt-va-mintaqa.md), [23-bob](23-toplamlar-va-generiklar-gigiyenasi.md) |
| Record, sealed, `Optional`, Stream | arxitektor: zamonaviy Java bo'limi |
| Spring mexanikasi | arxitektor: Spring mexanikasi boblari |
| Spring kodi uslubi | shu hujjat, [26-bob](26-spring-kodining-tozaligi.md), [27-bob](27-rest-api-kodining-oqilishi.md) |
| JPA mexanikasi va N+1 | arxitektor: Spring Data JPA va Hibernate bo'limi |
| JPA kodi uslubi | shu hujjat, [28-bob](28-jpa-va-sql-kodining-tozaligi.md) |
| PostgreSQL ichki tuzilishi | arxitektor: PostgreSQL boblari |
| Log narxi va kuzatuvchanlik | arxitektor: kuzatuvchanlik amaliyoti bo'limi |
| Log kodi uslubi | shu hujjat, [29-bob](29-log-kodining-tozaligi.md) |
| Test strategiyasi va texnikasi | [testlash qo'llanmasi](../testing/README.md) |
| Test kodi tozaligi va TDD | shu hujjat, [30-bob](30-test-kodi-ham-ishlab-chiqarish-kodi.md), [31-bob](31-tdd-intizomi-va-kod-dizayniga-tasiri.md) |
| Kod hidi va refaktoring harakati | shu hujjat, [32-bob](32-kod-hidlari-katalogi-i-nom-funksiya-malumot.md), [37-bob](37-refaktoring-harakatlari-katalogi-iii-shart.md) |
| Legacy refaktoring strategiyasi | arxitektor: legacy kod va refaktoring bo'limi |
| Build va versiya nazorati | shu hujjat, [39-bob](39-bir-qadamli-build-va-mahalliy-qaytish.md), [40-bob](40-versiya-nazorati-gigiyenasi.md), [41-bob](41-ozgarishni-kiritish-jarayoni-kichik-qadamlar.md) |
| Statik tahlil vositalari | shu hujjat, [42-bob](42-statik-tahlil-va-avtomatik-qoidalar.md) |
| Sonar qoidalari va quality gate | [SonarQube hujjati](../sonarqube/README.md) |
| Professional intizom | shu hujjat, [43-bob](43-professional-masuliyat.md), [47-bob](47-birgalikda-ishlash-va-orgatish.md) |
| Review jarayoni va yetakchilik | arxitektor: code review va texnik yetakchilik |
| Diffda xatoni ko'rish | [review hujjati](../code-review/README.md) |
| Review izohi matni va kelishmovchilik | [review hujjati](../code-review/README.md): madaniyat va til bo'limi |
| Xavfsizlik review metodikasi | [review hujjati](../code-review/README.md): xavfsizlik boblari |
| O'rganish va texnologiya tanlash | arxitektor: doimiy o'rganish bo'limi |

## 48.12 Amalda qo'llash

- [ ] 48.1-48.5 jadvallarini bitta sahifaga chiqarib, jamoa kelishuviga ilova qiling: McConnell tekshiruv ro'yxati bir sahifadan oshmasligini talab qiladi.
- [ ] 48.7 ro'yxatini pre-push hook yoki PR shabloniga kiriting.
- [ ] 48.8 ro'yxatidan jamoaga eng ko'p tegishli bandlarni tanlab, review checklistiga qo'ying; qolganini olib tashlang.
- [ ] 48.9 ro'yxatini yangi sinf shabloni (IDE live template) sifatida saqlang.
- [ ] 48.10 lug'atidagi atamalarni `GLOSSARY.md` ga qo'shing.
- [ ] 48.11 xaritasini yangi odamning birinchi kun materialiga kiriting ([47.3](47-birgalikda-ishlash-va-orgatish.md#473-yangi-odamga-toza-kod-standartini-yetkazish)).
- [ ] Jadvallardagi qoidalardan mashina tekshira oladiganlarini ajratib, statik tahlilga ko'chiring ([42.1](42-statik-tahlil-va-avtomatik-qoidalar.md#421-kompilyator-birinchi-tekshiruvchi)).
- [ ] Har chorakda ro'yxatni ko'rib chiqib, endi uchramaydigan xatolar bandini o'chiring: McConnell ro'yxatni tashkilotning o'z tajribasidan yig'ishni tavsiya qiladi.

## Manbalar

- Bu bob korpusning o'z boblaridan yig'ilgan xulosa: har qator o'z bo'limiga havola qiladi va birlamchi manba shu bo'limda keltirilgan. Pastdagi uch qator faqat bu bobda to'g'ridan-to'g'ri takrorlangan raqamli chegaralarga tegishli.
- Robert C. Martin, *Clean Code*, Prentice Hall, 2009, 3-bob ("Functions") - funksiya 100 qator bo'lmasligi va 20 qator deyarli hech qachon bo'lmasligi; argument sonining tartibi (nol, bir, ikki, uchtasi asoslanadi, to'rttasi va ko'pi asoslanmaydi); ichma-ich daraja birdan yoki ikkidan oshmasligi
- Robert C. Martin, *Clean Code*, Prentice Hall, 2009, 5-bob ("Formatting") - fayl uzunligi: tipik 200 qator, yuqori chegara 500 qator (JUnit, FitNesse, Time and Money o'lchovlari)
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 21.3 (489-490-betlar) - tekshiruv ro'yxati bir sahifadan oshmasin; ro'yxat tashkilotning o'z inspeksiya tajribasidan yig'iladi va uchramaydigan bandlar o'chiriladi
- Martin Fowler, *Refactoring*, Addison-Wesley, 1999, 3-bob (63-72-betlar) - 48.6 dagi hid va harakat juftliklari; to'liq ro'yxat va betlar [37.16](37-refaktoring-harakatlari-katalogi-iii-shart.md#3716-refaktoring-harakatini-tanlash-jadvali) da
- ESLATMA: 48.4 dagi indentatsiya (4 bo'shliq) va qator uzunligi (100 yoki 120) qiymatlari Java konvensiyasi va korpusning tanlovi ([12.1](12-gorizontal-formatlash-va-kod-uslubi.md#121-qator-uzunligi-chegarasi-va-uni-tanlash), [12.4](12-gorizontal-formatlash-va-kod-uslubi.md#124-indentatsiya-va-uni-buzmaslik)), kitobdan olingan raqam emas: Clean Code bu yerda faqat "qator 150 belgidan uzun bo'lmasin" deydi
- ESLATMA: 48.7-48.9 tekshiruv ro'yxatlari va 48.10 lug'ati shu korpusning o'z yig'masi, kitobdagi ro'yxatning tarjimasi emas
- ESLATMA: 48.10 dagi "diqqat-mana" shu korpusning metaforasi ([46.1](46-vaqt-diqqat-va-mashq.md#461-diqqat-resursi-va-uni-sarflash)), kitob atamasi emas
---

[&larr; 47. Birgalikda ishlash va o'rgatish](47-birgalikda-ishlash-va-orgatish.md) · [Mundarija](README.md) · [49. O'z-o'zini baholash: toza kod yetukligi &rarr;](49-oz-ozini-baholash-toza-kod-yetukligi.md)
