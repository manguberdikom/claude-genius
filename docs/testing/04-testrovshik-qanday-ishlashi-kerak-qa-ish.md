<!-- doc: testing | chapter: 4 | part:  -->

[Barcha hujjatlar](../../README.md) / [Testlash qo'llanmasi](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 4. Tester qanday ishlashi kerak: QA ish jarayoni (How a Tester Actually Works - The QA Workflow)

<details>
<summary>Bu bobdagi 12 bo'lim</summary>

- [4.1 QA'ning ish oqimi va sprint ritmi](#41-qaning-ish-oqimi-va-sprint-ritmi)
- [4.2 Talablarni testlash](#42-talablarni-testlash)
- [4.3 Test dizayn texnikalari](#43-test-dizayn-texnikalari)
- [4.4 Test case yozish](#44-test-case-yozish)
- [4.5 Exploratory testing](#45-exploratory-testing)
- [4.6 Defekt hisoboti standarti](#46-defekt-hisoboti-standarti)
- [4.7 Defekt hayot aylanishi va triage](#47-defekt-hayot-aylanishi-va-triage)
- [4.8 Regressiya testlash](#48-regressiya-testlash)
- [4.9 Muhitlar (environments)](#49-muhitlar-environments)
- [4.10 Qo'lda testlashdan avtomatlashtirishga o'tish mezonlari](#410-qolda-testlashdan-avtomatlashtirishga-otish-mezonlari)
- [4.11 QA ishini o'lchash](#411-qa-ishini-olchash)
- [4.12 Arxitektor nazorat ro'yxati](#412-arxitektor-nazorat-royxati)

</details>



Ko'pchilik arxitektorlar QA ishini "testni bosib ko'rish" deb tasavvur qiladi, lekin haqiqiy QA mutaxassisining kunining katta qismi talablarni tahlil qilish, risklarni baholash va topilganlarni boshqalar tushunadigan tilda yozishga ketadi. Bu bob QA'ning kundalik ritmini, test dizayn texnikalarini, defekt bilan ishlash standartini va qo'lda testlashdan avtomatlashtirishga o'tish mezonlarini bosqichma-bosqich ko'rsatadi. Arxitektor uchun bu bob ikki jihatdan muhim: birinchidan, siz QA'dan nima kutish kerakligini bilib olasiz; ikkinchidan, QA ishini imkonsiz qiladigan arxitektura qarorlarini (masalan trace ID yo'qligi yoki muhitlar nomosligi) oldindan ko'rasiz. Quyidagi barcha misollar bitta domenda - kredit limiti va buyurtma statuslari ustida - qurilgan, shuning uchun texnikalarni bir-biriga qiyoslash oson.

## 4.1 QA'ning ish oqimi va sprint ritmi

QA ishi chiziqli emas, aylanma: har bir talab bir necha bosqichdan o'tadi va har bosqichda orqaga qaytish ehtimoli bor. To'liq oqim quyidagicha ko'rinadi.

**1. Talabni o'qish.** QA user story'ni, qabul kriteriyalarini (acceptance criteria), maketlarni va bog'liq API shartnomasini o'qiydi. Maqsad - "nima qurilayotganini" emas, "nima buzilishi mumkinligini" tushunish.

**2. Savol berish.** Noaniq joylar ro'yxatga olinadi va business analyst yoki product owner'ga beriladi. Bu bosqich eng arzon bug tuzatish nuqtasi: hali kod yozilmagan.

**3. Qabul kriteriyalarini aniqlashtirish.** Noaniq kriteriya testlanadigan shaklga qayta yoziladi. Natija - story'ning Definition of Ready holatiga yetishi.

**4. Test dizayni.** Texnikalar qo'llanadi (ekvivalentlik sinflari, chegaralar, qaror jadvali), test case'lar va checklist'lar tayyorlanadi, risk yuqori bo'lgan joylarga ko'proq e'tibor beriladi.

**5. Testni bajarish.** Yangi funksionallik test qilinadi: avval smoke, keyin asosiy ssenariylar, keyin chegaralar va salbiy holatlar, oxirida exploratory session.

**6. Defekt ochish.** Topilgan muammo standart formatda yoziladi, severity taklif qilinadi, log va trace ID ilova qilinadi.

**7. Retest.** Developer tuzatgandan keyin QA aynan o'sha qadamlarni qaytaradi va yondosh joylarni ham tekshiradi (tuzatish nimani buzgan bo'lishi mumkin?).

**8. Regressiya.** Risk asosida tanlangan regression suite ishga tushiriladi - qo'lda yoki avtomatik.

**9. Sign-off.** QA release holatini yozma bayon qiladi: nima test qilindi, nima qilinmadi, qanday ochiq risklar bor. Sign-off "bug yo'q" degani emas - "ma'lum risklar qabul qilinadigan darajada" degani.

Sprint bo'yicha kunlik ritm (ikki haftalik sprint misolida):

| Sprint kuni | QA'ning asosiy faoliyati | Chiqish artefakti |
| --- | --- | --- |
| 1-2 | Backlog refinement, talablarni tahlil, savollar | Aniqlashtirilgan AC, risk ro'yxati |
| 2-4 | Test dizayni, test ma'lumotlari talabi | Test case'lar, checklist |
| 4-8 | Tayyor bo'lgan story'larni testlash, defekt ochish | Bug report'lar, test natijalari |
| 6-9 | Retest, avtomatlashtirishga nomzodlarni belgilash | Yopilgan defektlar, avtomatlashtirish backlog'i |
| 9 | Regressiya (risk asosida qisqartirilgan) | Regression hisoboti |
| 10 | Sign-off, release notes'ga QA qismi, retrospektiva | Sign-off xati, escaped defect tahlili |

Amalda bu bosqichlar parallel ketadi: QA ertalab kechagi defektlarni retest qiladi, kunduzi yangi story'ni testlaydi, kun oxirida keyingi story uchun test dizayn qiladi. Arxitektor uchun muhim xulosa: agar QA sprintning faqat oxirgi ikki kunida ishga tushsa, bu jarayon buzilgan - testlash "siqilib" qoladi va regressiya hisobidan qisqartiriladi.

## 4.2 Talablarni testlash

Talabni testlash - kod yozilmasdan oldin bajariladigan eng foydali test turi. QA talabga qarab bir necha savol beradi: bu shart o'lchanadimi? chegarasi qayerda? xato holatida nima bo'ladi? kim ko'rishi mumkin? Agar savolga javob yo'q bo'lsa, talab testlanmaydi.

Testlanmaydigan qabul kriteriyasining tipik belgilari: "tez ishlashi kerak", "qulay bo'lishi kerak", "to'g'ri hisoblanishi kerak", "kerakli hollarda xabar chiqsin". Bularda o'lchov, chegara va aktor yo'q.

| Yomon qabul kriteriyasi | Nega yomon | Qayta yozilgan (yaxshi) variant |
| --- | --- | --- |
| "Kredit limiti to'g'ri hisoblanishi kerak" | "To'g'ri" aniqlanmagan, formula yo'q | "Daromadi 10 000 000 so'mdan yuqori va kechikishi 0 bo'lgan mijoz uchun limit = daromad × 3, maksimum 50 000 000 so'm" |
| "Tizim tez javob bersin" | O'lchov va yuk darajasi yo'q | "`POST /api/credit-limit` 100 RPS yukda p95 < 400 ms javob qaytaradi" |
| "Noto'g'ri ma'lumotda xato ko'rsatilsin" | Qaysi xato, qanday kod, qaysi maydon - noaniq | "Daromad maydoni bo'sh bo'lsa, HTTP 400 va `{\"field\":\"income\",\"code\":\"REQUIRED\"}` qaytadi" |
| "Admin hamma narsani ko'ra oladi" | Rollar va resurslar aniqlanmagan | "ROLE_ADMIN barcha mijozlarning limit tarixini ko'radi; ROLE_AGENT faqat o'z filialidagi mijozlarni ko'radi; boshqasiga 403" |
| "Buyurtma bekor qilinsin" | Qaysi statuslardan bekor qilish mumkinligi aytilmagan | "NEW va PAID statuslarida bekor qilish mumkin; SHIPPED va DELIVERED'da 409 va `ORDER_NOT_CANCELLABLE` qaytadi" |

Yaxshi qabul kriteriyasining mezonlari: (1) aktor ko'rinadi, (2) shart o'lchanadi, (3) kutilgan natija bitta ma'noda tushuniladi, (4) xato yo'li ham yozilgan, (5) chegaralar raqam bilan berilgan. QA bu beshtasini har bir story uchun tekshirib chiqadi va yetishmaganini savol sifatida qaytaradi.

## 4.3 Test dizayn texnikalari

Test dizayn - cheksiz ko'p variantdan foydali bo'lganini tanlash san'ati. Quyida har bir texnika va uning aniq misoli.

**Ekvivalentlik sinflari (equivalence partitioning).** Kirish qiymatlarini bir xil ishlov ko'radigan guruhlarga bo'lamiz va har guruhdan bittasini tekshiramiz. Kredit limiti misolida daromad maydoni: manfiy qiymatlar (xato), 0-999 999 (limit berilmaydi), 1 000 000-9 999 999 (bazaviy limit), 10 000 000 va yuqori (×3 limit), raqam bo'lmagan matn (validatsiya xatosi). Beshta sinf - beshta test, 10 000 ta qiymat emas.

**Chegara qiymatlari (boundary value analysis).** Xatolar aksariyat chegarada yashaydi. Yuqoridagi `>= 10 000 000` sharti uchun tekshirilishi kerak bo'lgan nuqtalar: 9 999 999, 10 000 000, 10 000 001. Limit maksimumi 50 000 000 bo'lsa: daromad 16 666 666 (limit 49 999 998), 16 666 667 (50 000 001 → 50 000 000 ga qisqaradi). Ikki chegarani birlashtirish `>` va `>=` xatosini (klassik off-by-one) darhol ochadi.

**Qaror jadvali (decision table).** Bir necha shart birgalikda natijani belgilaganda ishlatiladi. Kredit limiti qarori:

| # | Daromad >= 10 mln | Kechikish tarixi bor | KYC tasdiqlangan | Kutilgan natija |
| --- | --- | --- | --- | --- |
| R1 | Ha | Yo'q | Ha | Limit = daromad × 3 (max 50 mln) |
| R2 | Ha | Yo'q | Yo'q | `KYC_REQUIRED`, limit 0 |
| R3 | Ha | Ha | Ha | Limit = daromad × 1 (qo'lda ko'rib chiqish) |
| R4 | Ha | Ha | Yo'q | `KYC_REQUIRED`, limit 0 |
| R5 | Yo'q | Yo'q | Ha | Limit = 1 mln (boshlang'ich) |
| R6 | Yo'q | Yo'q | Yo'q | `KYC_REQUIRED`, limit 0 |
| R7 | Yo'q | Ha | Ha | `DECLINED` |
| R8 | Yo'q | Ha | Yo'q | `KYC_REQUIRED`, limit 0 |

Jadval sakkizta qatorni beradi va darhol ko'rinadi: KYC yo'q bo'lsa boshqa shartlar ahamiyatsiz. Shu sababli R2, R4, R6, R8'ni bitta qoidaga birlashtirib, test sonini 8'dan 5'ga tushirish mumkin - bu qaror jadvalining asosiy foydasi: ortiqcha testni ko'rsatadi.

**Holat o'tishlari (state transition).** Buyurtma statuslari: NEW → PAID → SHIPPED → DELIVERED, hamda NEW/PAID → CANCELLED va DELIVERED → RETURNED. Test dizayni uchta qismdan iborat: (a) ruxsat etilgan har bir o'tish ishlaydi, (b) ruxsat etilmagan o'tish rad etiladi (SHIPPED → CANCELLED → 409), (c) bir xil o'tishning takrori idempotent (PAID → PAID ikkinchi to'lov hodisasida ikkinchi marta hisoblanmaydi). Arxitektor uchun signal: agar status o'tishlari kodda `if` lar to'dasiga sochilgan bo'lsa, QA ularni to'liq qamray olmaydi - o'tish qoidalari bitta joyda (state machine) saqlanishi kerak.

**Pairwise / orthogonal array.** Ko'p parametrli konfiguratsiyada barcha kombinatsiya portlashini kamaytiradi. Masalan: valyuta (UZS, USD), kanal (mobil, web, filial), mijoz turi (jismoniy, yuridik), to'lov usuli (karta, pul ko'chirish) - 2×3×2×2 = 24 kombinatsiya. Pairwise yondashuv har juft qiymat kamida bir marta uchrashishini kafolatlab, bu sonni 6-7 testga tushiradi. Amaliyotda defektlarning katta qismi ikki parametrning o'zaro ta'siridan kelib chiqadi, shuning uchun pairwise qamrov/xarajat nisbati bo'yicha juda samarali.

**Use case testing.** Foydalanuvchining to'liq yo'lini boshidan oxirigacha tekshiradi: mijoz ro'yxatdan o'tadi → KYC yuboradi → limit so'raydi → buyurtma yaratadi → to'laydi → yetkazib berishni kuzatadi. Bu texnika alohida birliklar to'g'ri, lekin birgalikda ishlamaydigan holatlarni ochadi (masalan limit berildi, ammo buyurtma yaratishda limit tekshirilmadi).

**Xato taxmin qilish (error guessing).** Tajribaga asoslangan texnika: QA qayerda xato bo'lishi ehtimolini taxmin qiladi. Tipik nomzodlar: bo'sh ro'yxat, bitta elementli ro'yxat, `null`, juda uzun matn (255+ belgi), emoji va maxsus belgilar, ikki marta tez bosilgan "To'lash" tugmasi (double submit), vaqt zonasi chegarasi (23:59 va 00:01), yil oxiri, sessiya tugashi, tarmoq uzilishi o'rtasida yuborilgan so'rov.

**CRUD matritsasi.** Har bir entity uchun to'rt amal × ruxsat/holat kesishmasi tekshiriladi. Bu "o'chirilgan yozuvni yangilash" yoki "boshqa filial mijozini ko'rish" kabi teshiklarni muntazam ochadi.

| Entity | Create | Read | Update | Delete |
| --- | --- | --- | --- | --- |
| CreditLimit | AGENT: ha; CUSTOMER: yo'q (403) | Egasi va AGENT: ha | Faqat ADMIN, audit log yoziladi | Soft delete; o'chirilgandan keyin Read 404 |
| Order | CUSTOMER: ha | Egasi: ha; boshqa: 403 | Faqat NEW statusida | DELIVERED'ni o'chirish taqiqlanadi (409) |

## 4.4 Test case yozish

Test case - boshqa odam (yoki kelgusi yildagi o'zingiz) hech nima so'ramasdan bajara oladigan yozma ko'rsatma. Standart tuzilishi:

```text
ID:            TC-CREDIT-014
Sarlavha:      10 mln chegarasida limit x3 hisoblanadi
Bog'liq talab: STORY-452 / AC-3
Prioritet:     High
Dastlabki shart (precondition):
  - Mijoz KYC_APPROVED holatida
  - Kechikish tarixi bo'sh
  - Test ma'lumoti: customer_id = CUST-1001
Test ma'lumoti:
  income = 10 000 000 (chegara nuqtasi)
Qadamlar:
  1. POST /api/credit-limit so'rovini customer_id va income bilan yubor
  2. Javob kodi va tanasini o'qi
  3. GET /api/credit-limit/CUST-1001 bilan saqlangan qiymatni tekshir
Kutilgan natija:
  - 2-qadam: HTTP 200, body.limit = 30 000 000, body.reason = "INCOME_TIER_3"
  - 3-qadam: saqlangan limit = 30 000 000, audit log'da LIMIT_ASSIGNED hodisasi bor
Keyingi holat (postcondition):
  - Mijoz limiti o'zgargan, boshqa mijozlarga ta'sir yo'q
Avtomatlashtirish: ha (API darajasida, regression suite'ga kiradi)
```

Yaxshi test case belgilari: bitta maqsadni tekshiradi; dastlabki shart to'liq yozilgan; qadamlar imperativ va aniq (tugma nomi, endpoint, maydon); kutilgan natija o'lchanadigan; test ma'lumoti test ichida ko'rsatilgan yoki fixture'ga havola qilingan; boshqa test case'ning natijasiga bog'liq emas (mustaqil); bajarilgandan keyin muhitni iflos qoldirmaydi.

Yomon test case belgilari: "tizim to'g'ri ishlashini tekshir" kabi noaniq kutilgan natija; 30 qadamli zanjir; "oldingi test case'dan keyin bajariladi" degan bog'liqlik; UI piksel joylashuviga bog'langan qadamlar.

**Checklist va test case farqi.** Checklist - tekshirilishi kerak bo'lgan narsalar ro'yxati, qadamlarsiz ("limit chegarasi 10 mln", "KYC yo'q holati", "manfiy daromad", "403 boshqa filial"). Tajribali QA uchun checklist tezroq va moslashuvchan. Test case - batafsil skript, yangi odam yoki audit talab qilgan joyda (masalan regulyator talabi, sertifikatsiya) kerak. Amaliy qoida: yangi funksionallikni exploratory + checklist bilan tekshiring, barqarorlashgan va takrorlanadigan qismini test case'ga aylantirib avtomatlashtiring.

**Qachon avtomatlashtirish kerak.** Test case avtomatlashtirishga munosib bo'ladi, agar: u har release'da bajariladi; natijasi deterministik; biznes uchun yuqori risk ko'taradi (to'lov, limit, ruxsatlar); qo'lda bajarish qimmat yoki zerikarli (katta ma'lumot to'plami bilan hisob-kitob); regressiya ehtimoli yuqori (ko'p o'zgaradigan kod). Qo'lda qolishi kerak bo'lganlar: bir martalik migratsiya tekshiruvi, vizual estetika va UX hissi, hali shakli o'zgarib turgan yangi ekran, murakkab tashqi tizim bilan qo'lda sozlanadigan holatlar.

## 4.5 Exploratory testing

Exploratory testing - "tasodifiy bosib ko'rish" emas, balki boshqarilgan tadqiqot. Eng keng tarqalgan format - session-based test management (SBTM): aniq charter, qat'iy timebox va yozma hisobot.

**Charter yozish.** Charter - session maqsadining bir-ikki gaplik ta'rifi. Shablon: "`<nimani>` ni `<qanday vositalar bilan>` o'rganib, `<qanday ma'lumotni>` topish". Misollar: "Kredit limiti hisoblanishini chegara qiymatlari va KYC statuslari kombinatsiyasi bilan o'rganib, noto'g'ri limit beradigan holatlarni topish"; "Buyurtma bekor qilish oqimini parallel so'rovlar bilan o'rganib, status race condition'larini topish".

**Timebox.** Odatda 60 yoki 90 daqiqa. Vaqt tugasa session tugaydi - topilgan narsa yozilib, keyingi charter rejalashtiriladi. Timebox ikki foyda beradi: diqqat tarqalmaydi va ish hajmi rejalashtirish mumkin bo'ladi.

**Tour'lar** - tadqiqot yo'nalishini beruvchi metaforalar:

- **Pul yo'li (money tour).** Mahsulot pul topadigan oqimni kuzatish: limit → buyurtma → to'lov → hisob-faktura. Bu yo'ldagi bug eng qimmat.
- **Xato yo'li (bad-neighborhood / error tour).** Ataylab xato qilish: bo'sh maydon, noto'g'ri format, muddati o'tgan token, ikki marta to'lov, tarmoqni uzish.
- **Sertifikat yo'li (landmark tour).** Qabul kriteriyalarini "nishon" sifatida belgilab, ular orasida erkin yurish.
- **Orqa ko'cha (back-alley tour).** Eng kam ishlatiladigan funksiyalarni sinash - ular eng kam test qilingan.
- **Supervisor yo'li (configuration tour).** Rollar, sozlamalar, feature flag'lar kombinatsiyalarini almashtirish.

**Topilganlarni yozib borish.** Session davomida QA bitta oddiy jurnal yuritadi: vaqt, qilingan harakat, kuzatilgan natija, savol yoki shubha. Session oxirida hisobot uchta qismdan iborat bo'ladi: (1) charter va sarflangan vaqt taqsimoti (test / setup / bug yozish), (2) topilgan defektlar ro'yxati va ularning havolalari, (3) yangi savollar va keyingi charter takliflari. Bu hisobot regression suite'ni boyitishning asosiy manbai: exploratory'da topilgan har bir jiddiy bug uchun avtomatlashtirilgan regression test yozilishi kerak.

## 4.6 Defekt hisoboti standarti

Bug report - developer uchun yozilgan texnik hujjat. Uning yagona vazifasi: muammoni minimal vaqtda qayta ishlab chiqarishga (reproduce) imkon berish.

**Sarlavha formulasi:** `<qayerda> <qanday shartda> <nima noto'g'ri bo'ladi>`. Misol: "Kredit limiti: daromad aynan 10 000 000 bo'lganda limit ×1 hisoblanadi (×3 kutilgan)".

Yomon bug report misoli:

```text
Sarlavha: Limit ishlamaydi
Tavsif:   Limitni tekshirdim, natija xato. Tuzatinglar.
```

Bu hisobotda muhit, qadamlar, ma'lumot, kutilgan natija va log yo'q - developer QA bilan ikki marta yozishmasdan boshlay olmaydi.

Yaxshi bug report shabloni:

```text
ID:        BUG-2291
Sarlavha:  Kredit limiti: income = 10 000 000 da limit x1 hisoblanadi (x3 kutilgan)

Muhit:
  Stend:      QA (qa-2.internal)
  Backend:    credit-service 1.14.3 (build #872, commit a3f91c2)
  Baza:       PostgreSQL 15, schema migration V41
  Mijoz:      REST API (curl), Chrome 139 (UI orqali ham takrorlanadi)
  Vaqt:       2026-10-02 11:24 (UTC+5)

Dastlabki shart:
  customer_id = CUST-1001, KYC_APPROVED, kechikish tarixi bo'sh

Qayta ishlab chiqarish qadamlari:
  1. POST /api/credit-limit
     {"customerId":"CUST-1001","income":10000000}
  2. Javobni o'qi

Kutilgan natija:
  HTTP 200, limit = 30000000, reason = "INCOME_TIER_3"
  (STORY-452 / AC-3 ga muvofiq)

Kuzatilgan natija:
  HTTP 200, limit = 10000000, reason = "INCOME_TIER_1"

Takrorlanish:  3/3 (har safar takrorlanadi)
Trace ID:      4b9f1ad2c77e4e1b9a1f0c3d8e2b5a66
Log parchasi:  CreditLimitCalculator.java:88 -> "tier resolved: TIER_1 for income=10000000"
Ilova:         curl-request.txt, response.json, screenshot-ui.png, screen-recording.mp4
Severity:      Major (QA taklifi)
Priority:      (triage belgilaydi)
Bog'liq talab: STORY-452
Vaqtinchalik yechim: daromadni 10 000 001 kiritish
```

**Severity va priority farqi.** Severity - defektning texnik/biznes ta'sir kuchi (tizim qanchalik buzilgan). Priority - uni qachon tuzatish kerakligi (navbatdagi o'rni). Ikkisi mustaqil: bosh sahifadagi logotip xato yozilishi severity bo'yicha Minor, lekin priority bo'yicha Critical bo'lishi mumkin (brend zarari, release blocker). Teskarisi ham bo'ladi: kam ishlatiladigan hisobotni eksport qilishda crash - severity Critical, priority Low.

Kim belgilaydi: **severity'ni QA** belgilaydi (u ta'sirni o'z ko'zi bilan ko'rgan), **priority'ni product owner / triage** belgilaydi (u biznes navbatini biladi). Arxitektor texnik risk (ma'lumot buzilishi, xavfsizlik, migratsiya) haqida ovoz beradi.

| Severity ↓ / Priority → | Critical (shu release) | High (joriy sprint) | Medium (keyingi sprint) | Low (backlog) |
| --- | --- | --- | --- | --- |
| **Blocker** (ishni to'xtatadi) | To'lov umuman o'tmaydi | Faqat test stendda deploy buzilgan | - | - |
| **Critical** (ma'lumot/pul buzilishi) | Limit ikki marta hisoblanadi | Kam uchraydigan valyutada noto'g'ri kurs | Eski arxiv hisobotida xato summa | - |
| **Major** (asosiy funksiya ishlamaydi) | Chegara qiymatida noto'g'ri limit | Buyurtma bekor qilish 500 qaytaradi | Filtr noto'g'ri tartiblanadi | Kam ishlatiladigan eksport ishlamaydi |
| **Minor** (noqulaylik, chetlab o'tish bor) | Logotipda xato yozilgan nom | Xato xabari ingliz tilida | Tooltip kesilgan | Formatlash nomuvofiqligi |

## 4.7 Defekt hayot aylanishi va triage

Standart holatlar va o'tishlar:

| Holat | Kim o'tkazadi | Ma'nosi va chiqish sharti |
| --- | --- | --- |
| **New** | QA | Yangi yozilgan defekt, hali ko'rib chiqilmagan |
| **Triage** | PO + Tech lead + QA | Tasdiqlanadi, severity/priority va egasi belgilanadi |
| **In Progress** | Developer | Tuzatish ustida ish ketmoqda |
| **Ready for Test** | Developer | Tuzatish qaysi build/muhitda ekani ko'rsatilgan |
| **Reopened** | QA | Retest o'tmadi - aynan qadamlar va yangi log bilan qaytariladi |
| **Closed** | QA | Retest o'tdi, regression test qo'shildi (kerak bo'lsa) |
| **Won't Fix** | PO (QA xabardor) | Ongli qaror: sabab va qabul qilingan risk yozma qayd etiladi |

Qo'shimcha holatlar amalda uchraydi: `Duplicate` (mavjud defektga havola bilan), `Cannot Reproduce` (QA qo'shimcha ma'lumot - trace ID, video - beradi va qayta ochadi), `Deferred` (keyingi release'ga ko'chirildi).

**Triage uchrashuvi** - qisqa (20-30 daqiqa), muntazam (kuniga yoki kunora bir marta) va qat'iy formatli yig'ilish. Qatnashchilar: product owner (biznes prioriteti), tech lead yoki arxitektor (texnik ta'sir va murakkablik), QA (ta'sir va takrorlanish ma'lumoti). Har bir yangi defekt uchun to'rtta qaror qabul qilinadi: (1) bu haqiqatan defektmi yoki yangi talabmi? (2) severity to'g'ri baholanganmi? (3) priority qanday - shu release'da, keyingi sprintda yoki backlog'da? (4) egasi kim? Triage'da bug'ni muhokama qilib yechim o'ylash taqiqlanadi - bu alohida suhbat, aks holda uchrashuv cho'ziladi. Arxitektorning roli: bir xil sababdan kelayotgan defekt guruhlarini payqash ("oxirgi haftada beshta defekt status o'tishlariga bog'liq") va ularni bitta arxitektura ishiga aylantirish.

## 4.8 Regressiya testlash

Regressiya - oldin ishlagan funksionallik hali ham ishlayotganini tekshirish. Asosiy qiyinchilik: hamma narsani har safar tekshirish imkonsiz, demak tanlash kerak.

**Regression suite'ni tanlash mezonlari:** biznes uchun kritik oqimlar (pul yo'li) - har safar; o'zgargan kod atrofidagi funksionallik (change impact analysis) - har safar; tarixda ko'p bug chiqqan modullar - har safar; integratsiya nuqtalari va shartnomalar - har safar; kam ishlatiladigan va barqaror qismlar - kamroq (masalan har uchinchi release'da).

**Smoke va regression farqi:** smoke - "tizim umuman tirikmi?" degan 5-15 daqiqalik tekshiruv (login ishlaydi, asosiy sahifa yuklanadi, bitta buyurtma yaratiladi, health endpoint 200 qaytaradi). Regression - "oldingi funksionallik buzilmaganmi?" degan kengroq, bir necha soatlik yoki avtomatik holda o'n-o'n besh daqiqalik to'plam. Release oldidan tartib: deploy → smoke (qisqa, deploy to'g'riligini tasdiqlaydi) → regression (risk asosida tanlangan) → yangi funksionallik testi → sign-off.

**Risk asosida qisqartirish.** Har bir modulga ikki ko'rsatkich beriladi: buzilish ehtimoli (o'zgarish hajmi, kod murakkabligi, tarixiy defektlar) va buzilish narxi (foydalanuvchi soni, pul, regulyativ ta'sir). Ikkisi yuqori bo'lgan modullar to'liq test qilinadi; biri yuqori bo'lganlar qisqartirilgan to'plam bilan; ikkisi past bo'lganlar faqat smoke bilan qoplanadi. Bu yondashuv sign-off'da "nima test qilinmadi" savoliga aniq javob berish imkonini beradi - "past riskli X moduli faqat smoke bilan qoplandi" degan yozuv to'liq legitim.

## 4.9 Muhitlar (environments)

Muhitlar nomuvofiqligi QA ishini buzadigan birinchi sabab. Arxitektor har bir muhit uchun uchta narsani aniq belgilashi kerak: kim egasi, ma'lumot qayerdan keladi, qaysi versiyalar turadi.

| Muhit | Egasi | QA nima qiladi | Ma'lumot holati | Versiyalar mosligi |
| --- | --- | --- | --- | --- |
| **local** | Developer | QA kirmaydi (ba'zan bug'ni takrorlash uchun) | Embedded/Testcontainers, har ishga tushishda toza | Faqat joriy branch |
| **dev** | Developer jamoasi | Smoke, erta fikr-mulohaza | Beqaror, tez-tez tozalanadi | Har commit'da o'zgaradi, beqaror |
| **test / QA** | QA | Asosiy test ishi: yangi funksionallik, defekt tekshiruvi, exploratory | Boshqariladigan seed ma'lumot, QA tiklashi mumkin | Sprint build'lari, mock yoki stub'langan tashqi tizimlar |
| **staging** | QA + Release manager | Regressiya, integratsiya, E2E, release repetitsiyasi | Prod'ga o'xshash hajm, maskalangan (anonimlashtirilgan) ma'lumot | Prod'ga teng konfiguratsiya, haqiqiy tashqi tizimlarning sandbox'lari |
| **pre-prod** | Release manager / SRE | Oxirgi smoke, migratsiya repetitsiyasi, performance tekshiruvi | Prod nusxasi yoki prod'ga juda yaqin | Prod bilan aynan bir xil artefakt |
| **prod** | SRE / Operations | Faqat read-only smoke, monitoring kuzatuvi, canary tekshiruvi | Haqiqiy mijoz ma'lumoti - o'zgartirish taqiqlanadi | Release qilingan versiya |

QA uchun amaliy qoidalar: bug report'da muhit, build raqami va commit hash majburiy; "faqat staging'da takrorlanadi" degan defekt alohida e'tibor talab qiladi (konfiguratsiya farqi odatda sabab); test muhitida ma'lumotni tiklash (reset) QA o'zi bajara olishi kerak, developer'dan so'ramasdan; har bir muhitda tashqi tizim sandbox'i yoki stub'i aniq hujjatlashtirilgan bo'lishi kerak.

Arxitektor uchun ogohlantirish belgilari: QA muhiti haftada bir necha marta ishdan chiqadi; har bir muhitda schema versiyasi boshqa; test ma'lumotini tiklash qo'lda SQL yozishni talab qiladi; staging'da feature flag'lar prod'dan farq qiladi va buni hech kim bilmaydi.

## 4.10 Qo'lda testlashdan avtomatlashtirishga o'tish mezonlari

Avtomatlashtirish - maqsad emas, vosita. Qarorni to'rt savol bilan qabul qiling: bu test necha marta takrorlanadi? natijasi deterministikmi? muvaffaqiyatsizlikda signal aniqmi? saqlash narxi qanchaga tushadi?

Avtomatlashtirishga munosib: biznes qoidalari va hisob-kitoblar (limit formulalari, chegaralar - bular juda ko'p variantga ega va qo'lda tekshirish qimmat); API shartnomalari va status kodlari; ruxsatlar matritsasi (rol × resurs - tez o'sadi va qo'lda unutiladi); status o'tishlari, ayniqsa taqiqlangan o'tishlar; har release'dagi smoke; tarixda bug chiqqan joylar uchun regression testlar; ma'lumot migratsiyasidan keyingi yaxlitlik tekshiruvlari.

Qo'lda qolishi kerak: vizual estetika, maket bilan moslik va "his-tuyg'u" (UX); bir martalik migratsiya va release repetitsiyasi; exploratory testing - uni avtomatlashtirish mumkin emas, chunki qiymati aynan improvizatsiyada; shakli hali o'zgarib turgan yangi ekranlar (avtomat test ertaga qayta yozilishi kerak bo'ladi); tashqi tizim bilan qo'lda sozlash talab qiladigan kam uchraydigan holatlar; murakkab xato diagnostikasi.

Amaliy ketma-ketlik: yangi funksionallik → qo'lda + exploratory → barqarorlashgandan keyin eng qimmatli ssenariylar avtomatlashtiriladi → topilgan har bir jiddiy bug uchun regression test yoziladi (bug-driven automation, eng yuqori ROI'li yondashuv) → qo'lda vaqt yangi funksionallik va exploratory'ga qayta yo'naltiriladi. Agar QA vaqtining 80 foizi takrorlanadigan qo'lda regressiyaga ketayotgan bo'lsa, bu arxitektura muammosi, QA samaradorligi muammosi emas.

## 4.11 QA ishini o'lchash

To'g'ri o'lchov QA'ni yaxshilashga, noto'g'ri o'lchov tizimni o'ynashga undaydi.

**O'lchash mumkin va foydali:** escaped defect - prod'ga chiqib ketgan defektlar soni va ularning severity'si (bu butun jamoaning, nafaqat QA'ning ko'rsatkichi); defekt topish fazasi - qancha defekt talab tahlilida, qancha unit testda, qancha QA'da, qancha prod'da topildi (siljish chapga qarab bo'lishi kerak); bug report sifati - "Cannot Reproduce" va qo'shimcha ma'lumot so'ralgan defektlar ulushi; retest aylanishlari soni (reopen darajasi yuqori bo'lsa, talablar yoki muloqot muammosi bor); regression suite ishonchliligi - flaky test ulushi; talab aniqlashtirish samarasi - QA savollari natijasida o'zgartirilgan qabul kriteriyalari soni.

**O'lchamaslik kerak:** topilgan bug soni bo'yicha bonus yoki reyting. Bu metrika darhol xatti-harakatni buzadi: QA ko'p mayda-chuyda defekt yozadi, bitta katta muammoni o'nta kichik defektga bo'ladi, jiddiy risklarni tahlil qilishga vaqt sarflamaydi (chunki tahlil "bug soni"ni oshirmaydi), developer bilan munosabat raqobatga aylanadi va developer defektni "Duplicate" yoki "Not a bug" deb yopishga harakat qiladi. Shu sababli yozilgan test case soni ham yaxshi metrika emas (ko'p test case ≠ yaxshi qamrov), avtomatlashtirilgan test soni ham (ko'p sayoz test tez-tez buziladi), qamrov foizi ham yolg'iz holda ma'nosiz.

Asosiy printsip: QA'ning qiymati topilgan bug sonida emas, prod'ga chiqmagan bug'larda va jamoaga berilgan aniq risk ma'lumotida. Bu qiymatni o'lchash qiyin, lekin uni noto'g'ri proksilar bilan almashtirish - eng tez yo'l yomon QA madaniyatiga.

## 4.12 Arxitektor nazorat ro'yxati

- [ ] Har bir story'ning qabul kriteriyalari testlanadigan shaklda (aktor, o'lchanadigan shart, xato yo'li, raqamli chegara) yozilgan va QA Definition of Ready'ni tasdiqlagan
- [ ] QA sprintning birinchi kunidan ishtirok etadi; test dizayni kod yozilishidan oldin boshlanadi, oxirgi ikki kunga siqilmaydi
- [ ] Bug report shabloni jamoada yagona va majburiy maydonlar bor: muhit, build/commit, qadamlar, kutilgan va kuzatilgan natija, trace ID, log parchasi
- [ ] Har bir so'rov trace ID qaytaradi va log'larda uni izlash mumkin - QA developer'ga "qayerda qarash kerak"ni ko'rsata oladi
- [ ] Severity QA tomonidan, priority product owner tomonidan belgilanadi; triage muntazam o'tadi va unda texnik risk ovozi bor
- [ ] Status o'tishlari va biznes qoidalari kodda bitta joyda jamlangan (state machine, qaror jadvali) - QA ularni to'liq qamray oladi
- [ ] Muhitlar jadvali hujjatlashtirilgan: egasi, versiyalar mosligi, ma'lumot manbasi; QA test muhitini mustaqil tiklay oladi
- [ ] QA metrikalari escaped defect va defekt topish fazasiga asoslangan; topilgan bug soni bo'yicha hech qanday bonus yoki reyting yo'q

---

[&larr; 3. Kim nima yozadi: rollar va mas'uliyat](03-kim-nima-yozadi-rollar-va-masuliyat.md) · [Mundarija](README.md) · [5. Unit test: asoslar, qoidalar va JUnit 5 &rarr;](05-unit-test-asoslar-qoidalar-va-junit-5.md)
