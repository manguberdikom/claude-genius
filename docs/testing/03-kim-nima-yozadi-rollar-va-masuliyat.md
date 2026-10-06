<!-- doc: testing | chapter: 3 | part:  -->

[Barcha hujjatlar](../../README.md) / [Testlash qo'llanmasi](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 3. Kim nima yozadi: rollar va mas'uliyat (Who Writes What - Roles & Responsibilities)

<details>
<summary>Bu bobdagi 10 bo'lim</summary>

- [3.1 Rollar ta'rifi va farqi](#31-rollar-tarifi-va-farqi)
- [3.2 Mas'uliyat matritsasi (RACI)](#32-masuliyat-matritsasi-raci)
- [3.3 "Developer unit test yozadi, QA E2E yozadi" qoidasining chegaralari](#33-developer-unit-test-yozadi-qa-e2e-yozadi-qoidasining-chegaralari)
- [3.4 Three Amigos va Example Mapping](#34-three-amigos-va-example-mapping)
- [3.5 QA'ning sprint ichidagi joyi](#35-qaning-sprint-ichidagi-joyi)
- [3.6 Test kodini code review qilish](#36-test-kodini-code-review-qilish)
- [3.7 Jamoa modellari](#37-jamoa-modellari)
- [3.8 Test ownership](#38-test-ownership)
- [3.9 1 QA va 5 developer: kichik jamoa uchun amaliy model](#39-1-qa-va-5-developer-kichik-jamoa-uchun-amaliy-model)
- [3.10 Arxitektor nazorat ro'yxati](#310-arxitektor-nazorat-royxati)

</details>



Testlash strategiyasi qog'ozda qanchalik go'zal bo'lsa ham, uni real hayotga aylantiradigan narsa - kim nimani yozadi, kim nimaga javob beradi va buzilgan testni kim tuzatadi degan savollarga berilgan aniq javoblardir. Amalda ko'p jamoalarda sifat "QA'ning ishi" deb atalib, developer'lar test yozishni majburiyat emas, balki qo'shimcha xizmat deb qabul qilishadi - natijada test piramidasi teskari aylanadi va release oldidan har doim panika boshlanadi. Bu bobda rollarni, RACI matritsasini, jamoa modellarini va test ownership masalasini arxitektor nuqtai nazaridan ko'rib chiqamiz. Maqsad - tashkiliy chizma chizish emas, balki sifat uchun javobgarlikni texnik qarorlar bilan bir xil joyga, ya'ni kodni yozadigan jamoaga yaqinlashtirish.

## 3.1 Rollar ta'rifi va farqi

Rol - bu lavozim emas, balki mas'uliyat to'plami. Kichik jamoada bitta odam uch-to'rt rolni olib yurishi mutlaqo normal; muhimi - rol egasi yo'q bo'lib qolmasligi. Spring loyihalarida eng ko'p uchraydigan rollar va ularning sifatga qo'shadigan hissasi quyidagicha.

| Rol | Asosiy mas'uliyat | Odatda yozadigan/boshqaradigan testlar | Muvaffaqiyat ko'rsatkichi |
|---|---|---|---|
| Developer | O'zi yozgan kodning ishlashiga javob beradi; testni kod bilan bir PR'da yetkazadi | Unit, slice (`@WebMvcTest`, `@DataJpaTest`), integratsion (Testcontainers), contract producer/consumer | PR'da test bor; o'z feature'idagi bug'lar soni kamayadi |
| QA Engineer (manual) | Exploratory testing, qabul kriteriyalarini tekshirish, edge case'larni kashf qilish | Qo'lda exploratory sessiyalar, qabul testi, UAT yordami | Production'ga chiqib ketgan bug'larning kamligi, topilgan muhim defektlar sifati |
| Automation QA / SDET | Avtomatlashtirish freymvorki, E2E va API test suite'lari, test ma'lumotlari vositalari | E2E (Selenium/Playwright), API testlar, `RestAssured` ssenariylari, test data builder'lar | Suite'ning barqarorligi, flaky foizi, ishlash vaqti |
| QA Lead | Sprint ichidagi sifat jarayoni, QA resurslarini taqsimlash, release sign-off | Test rejasi, regressiya qamrovi, risk bo'yicha prioritetlash | Release sign-off ishonchliligi, qamrov va risk muvofiqligi |
| Test Architect | Test strategiyasi, piramidaning shakli, test freymvork standartlari | Shablonlar, baza test klasslari, konvensiyalar, qamrov siyosati | Piramidaning real shakli, test yozish narxi (yangi test qancha vaqt oladi) |
| DevOps / Platform | CI/CD pipeline, test muhiti, Testcontainers uchun resurslar, parallel bajarilish | Infratuzilma, Docker image'lar, cache, test reportlari | Pipeline vaqti, muhit beqarorligidan kelgan nosozliklar soni |
| Product Owner | Testlanadigan qabul kriteriyalari, biznes qoidalarining aniqligi, prioritet | Qabul kriteriyalari, misollar (example), UAT qarori | Noaniq AC sababli qaytgan tasklar soni |
| Arxitektor | Testlanuvchanlikni dizaynga kiritish, modul chegaralari, contract'lar, nofunksional talablar | Arxitektura testlari (ArchUnit), contract chegaralari, SLA/SLO talablari | Testlash qiyin bo'lgan joylarning kamayishi, chegaralarning buzilmasligi |

Arxitektor bu ro'yxatda alohida o'rinda turadi: u test yozmasligi mumkin, lekin testlash mumkin bo'lmagan arxitektura uchun aynan u javobgar. Static metodlarga to'la util'lar, `new` bilan yaratilgan dependency'lar, bitta 4000 satrli service - bular QA muammosi emas, dizayn muammosi.

## 3.2 Mas'uliyat matritsasi (RACI)

RACI'da **R** (Responsible) - ishni bajaradigan, **A** (Accountable) - yakuniy javobgar (har qatorda faqat bitta), **C** (Consulted) - maslahat so'raladigan, **I** (Informed) - xabardor qilinadigan tomon. Quyidagi matritsa ko'pchilik Spring loyihalari uchun yaxshi boshlang'ich nuqta; uni jamoangizga moslashtirish kerak, lekin "A" ustunini bo'sh qoldirmang.

| Faoliyat | Developer | QA / SDET | QA Lead | Arxitektor / Test Architect | DevOps | PO |
|---|---|---|---|---|---|---|
| Unit test | **R** | I | I | **A** (standart) | - | - |
| Slice test (`@WebMvcTest`, `@DataJpaTest`) | **R** | C | I | **A** | I | - |
| Integratsion test (Testcontainers) | **R** | C | I | **A** | C | - |
| Contract test (producer/consumer) | **R** | C | I | **A** | C | I |
| E2E test | C | **R** | **A** | C | C | I |
| Performance test | C | **R** | C | **A** | C | I |
| Security test (SAST/DAST, authz) | C | **R** | I | **A** | C | I |
| Test ma'lumotlari (fixture, builder, seed) | **R** | **R** | C | **A** | C | C |
| Test infratuzilmasi va CI | C | C | I | C | **R/A** | - |
| Flaky test tozalash | **R** | **R** | C | **A** | C | - |
| Test strategiyasi va piramida shakli | C | C | C | **R/A** | C | I |
| Release sign-off | C | C | **R** | C | C | **A** |

Ikki muhim nuqta. Birinchi - unit va integratsion testlarda "A" arxitektorda, chunki standartni u belgilaydi, lekin "R" doimo developer'da: test yozishni delegatsiya qilish mumkin emas. Ikkinchi - release sign-off'da yakuniy javobgar PO, QA Lead emas. QA Lead risk haqida ma'lumot beradi, qarorni biznes qabul qiladi. Bu farq buzilganda QA "darvozabon" ga aylanadi va jamoa sifatni o'z zimmasidan oladi.

## 3.3 "Developer unit test yozadi, QA E2E yozadi" qoidasining chegaralari

Bu qoida boshlang'ich taqsimot sifatida foydali, lekin qattiq devorga aylansa quyidagi zararlarni keltiradi.

Birinchidan, o'rtadagi qatlam egasiz qoladi. Unit va E2E orasida service-to-service integratsiya, DB tranzaksiyalari, mapping, xato ishlovi va contract'lar bor. Developer "bu mening ishim emas, integratsiya - QA'da" deb o'ylaydi, QA esa "bu kod ichida, developer qarasin" deydi. Natija - bo'shliq E2E bilan to'ldiriladi, E2E sekin va flaky bo'ladi, piramida karamelga aylanadi.

Ikkinchidan, feedback aylanasi uzayadi. Developer o'z kodining integratsiyada ishlashini faqat QA sprintning oxirida tekshirgandan keyin biladi. Bir hafta oldin yozilgan kod kontekstini qayta tiklash - eng qimmat debug turi.

Uchinchidan, bilim bir tomonlama to'planadi. QA test dizayni texnikalarini biladi (boundary value, equivalence partitioning), developer esa kodning ichki tuzilishini biladi. Qattiq bo'linishda bu bilimlar almashmaydi: developer'ning unit testlari faqat happy path'ni tekshiradi, QA'ning E2E testlari esa kodning qaysi joyi xavfli ekanini bilmaydi.

To'g'ri yondashuv - "kim yozadi" emas, "kim qaysi riskka javob beradi". Developer kod ichidagi riskni yopadi (barcha darajada, unit'dan Testcontainers'gacha), QA esa foydalanuvchi va biznes riskini yopadi (exploratory, qabul, end-to-end ssenariylar). Qatlam emas, risk turi bo'yicha bo'linish barqarorroq.

## 3.4 Three Amigos va Example Mapping

Three Amigos - bu PO (nima kerak), developer (qanday qilamiz) va QA (qanday buzilishi mumkin) birgalikda user story'ni muhokama qiladigan 25-40 daqiqalik uchrashuv. Uning maqsadi test yozish emas, balki noaniqlikni kod yozilishidan oldin topish.

Example Mapping - bu muhokamani to'rt rangli kartada tuzadigan texnika: sariq - story, ko'k - qoida (biznes qoidasi / qabul kriteriyasi), yashil - misol (konkret ssenariy), qizil - savol (javobi yo'q, bloklovchi).

Misol: "Foydalanuvchi buyurtmani bekor qilishi mumkin" story'si.

- Qoida 1: faqat `NEW` yoki `PAID` statusdagi buyurtma bekor qilinadi.
  - Misol: `NEW` buyurtma → bekor qilindi, status `CANCELLED`.
  - Misol: `SHIPPED` buyurtma → `409 Conflict`, status o'zgarmaydi.
- Qoida 2: `PAID` buyurtma bekor qilinsa, to'lov avtomatik qaytariladi.
  - Misol: 100 000 so'm to'langan → refund `PaymentService`'ga yuboriladi, event `OrderCancelled` chiqadi.
  - Savol (qizil): refund xato bersa, buyurtma `CANCELLED` bo'lib qoladimi yoki rollback bo'ladimi?
- Qoida 3: bekor qilish faqat buyurtma egasi yoki `ROLE_SUPPORT` tomonidan.
  - Misol: boshqa foydalanuvchi → `403`.

Bu yerda eng qimmatli natija - qizil karta. U aniqlanmasa, developer o'zicha qaror qabul qiladi, QA boshqa narsani kutadi va bug sprintning oxirida chiqadi. Amaliy qoida: story'da ochiq qizil karta bo'lsa, u sprintga kirmaydi. Yashil misollar esa keyinchalik to'g'ridan-to'g'ri test nomlariga aylanadi - `shouldReturn409WhenCancellingShippedOrder` kabi.

## 3.5 QA'ning sprint ichidagi joyi

QA sprintning oxirida paydo bo'ladigan bosqich emas, balki butun sprint davomida ishtirok etadigan rol.

Grooming / refinement bosqichida QA eng foydali savollarni beradi: "bu holatda nima bo'ladi?", "chegara qiymati qanday?", "eski ma'lumotlar bilan nima qilamiz?", "bu o'zgarish qaysi integratsiyalarga ta'sir qiladi?". Bu bosqichda topilgan noaniqlik eng arzon.

Qabul kriteriyalarini testlanadigan holatga keltirish - QA'ning asosiy hissasi. "Tez ishlashi kerak" → "p95 javob vaqti 300 ms dan kam, 200 RPS yuklamada". "To'g'ri hisoblanishi kerak" → konkret kirish va chiqish qiymatlari jadvali.

Story ishlanayotganda QA tayyor bo'lgan qismni darhol tekshiradi (sprintning oxirini kutmaydi), exploratory sessiyalar o'tkazadi va avtomatlashtirish uchun ssenariylarni tanlaydi. Sprint oxirida regressiya ko'p hollarda avtomatik ishlaydi - QA faqat o'zgargan sohaga yo'naltirilgan qo'shimcha exploratory qiladi. Release sign-off esa "men ruxsat beraman" degani emas: QA risk hisobotini beradi - nima tekshirildi, nima tekshirilmadi, qanday ma'lum muammolar qoldi - qaror PO'da.

## 3.6 Test kodini code review qilish

Test kodi - production kodi. U ham o'qiladi, ham o'zgartiriladi, ham buziladi. Shuning uchun bir xil standartda review qilinishi kerak: formatlash, nomlash, duplikatsiyani kamaytirish, abstraksiya darajasi. Test kodida eng ko'p uchraydigan qarz - copy-paste qilingan setup va tushunarsiz magic constant'lar.

Review'ni kim qiladi: unit/integratsion testlarni boshqa developer; E2E va avtomatlashtirish freymvorkini SDET yoki QA Lead; yangi test turi yoki yangi baza klass qo'shilganda arxitektor ham ko'radi. Kichik jamoada QA developer'ning test PR'iga review qo'shilishi juda foydali - QA test dizayni bo'yicha bo'shliqlarni ko'radi.

Test review checklist:

- Test nomi nimani tekshirayotganini kod o'qimasdan tushuntiradimi?
- Bitta testda bitta sabab bormi (bir nechta mustaqil assertion bitta testga tiqilmaganmi)?
- Assertion mazmunlimi - `assertNotNull` yoki `assertTrue(true)` bilan "yashil" qilinmaganmi?
- Test implementatsiyani emas, xulq-atvorni tekshiradimi (mock'lar ichki chaqiruvlarni ko'chirib yozmaganmi)?
- Testlar bir-biridan mustaqilmi: tartibga, umumiy static holatga yoki oldingi testdan qolgan ma'lumotga bog'liq emasmi?
- `Thread.sleep`, haqiqiy tarmoq chaqiruvi, hardcode qilingan sana/vaqt yoki tasodifiy qiymat ishlatilmaganmi?
- Test ma'lumotlari builder/factory orqali, o'qiladigan holatda tayyorlanganmi?
- Negative va boundary holatlar qamrab olinganmi, yoki faqat happy path bormi?
- Test to'g'ri qatlamda turganmi - unit bilan yetarli bo'ladigan narsa uchun butun Spring context ko'tarilmaganmi?
- Test buzilganda xato xabari muammoni ko'rsatadimi (`AssertJ` tavsifli assertion'lar)?

## 3.7 Jamoa modellari

| Model | Kuchli tomoni | Kuchsiz tomoni | Qachon mos |
|---|---|---|---|
| Embedded QA (jamoa ichida) | Tez feedback, kontekstni chuqur bilish, Three Amigos tabiiy ishlaydi | QA'lar o'rtasida standart tarqaladi, bilim almashinuvi sust | Mustaqil product jamoalari, 5-9 kishilik squad'lar |
| Markazlashgan QA bo'limi | Yagona standart, resurslarni qayta taqsimlash oson, chuqur ekspertiza | "Devor ustidan tashlash", uzun feedback, QA bottleneck'ga aylanadi | Qattiq regulyatsiya, auditga tayyorlik, ko'p mahsulotli yirik tashkilot |
| QA enabling team (platforma sifatida) | Freymvork, shablon va CI'ni markaziy beradi, jamoalar o'zi yozadi | Jamoalarda minimal test madaniyati bo'lishi talab qilinadi | 5+ jamoa, o'sayotgan tashkilot, mikroservis landshaft |
| "QA yo'q" (developer-owned quality) | Eng qisqa feedback, to'liq ownership, tez release | Exploratory va UX riski ko'rinmaydi, developer ko'r nuqtalari qoladi | Kuchli muhandislik madaniyati, past biznes riski, SaaS va feature flag'lar |

Ko'p tashkilotlar uchun eng barqaror kombinatsiya - embedded QA plus kichik enabling team: har jamoada sifat egasi bor, umumiy freymvork va CI esa markazda saqlanadi.

## 3.8 Test ownership

Har bir test suite'ning nomma-nom egasi bo'lishi kerak - jamoa yoki shaxs, `CODEOWNERS` faylida qayd etilgan. Egasi yo'q suite muqarrar ravishda tark etiladi: flaky testlar `@Disabled` bo'ladi, qamrov pasayadi, keyin esa butun suite "ishonchsiz" deb o'chiriladi.

Buzilgan testni kim tuzatadi degan savolga eng sog'lom javob: testni buzgan o'zgarishni kiritgan odam. "Ishlatgan odam tuzatadi" qoidasi (you break it, you fix it) PR darajasida ishlaydi - qizil pipeline bilan PR merge qilinmaydi. Main branch'da test buzilgan bo'lsa, u eng yuqori prioritetli ish bo'ladi: yangi feature yozish to'xtaydi, chunki qizil main butun jamoani sekinlashtiradi.

On-call bilan bog'liq qoidalar: test infratuzilmasi nosozligi (muhit, Docker, registry) DevOps/Platform on-call'ga boradi; test mazmunidagi nosozlik - suite egasiga. Tungi nightly suite buzilsa, uni ertalab birinchi navbatda ko'radigan rotatsiya bo'lishi kerak, aks holda nightly natijalari oylar davomida hech kim o'qimaydigan email'ga aylanadi.

## 3.9 1 QA va 5 developer: kichik jamoa uchun amaliy model

O'zbekistondagi ko'p jamoalarda real nisbat 1:5 yoki 1:8. Bu holatda QA'ni hamma narsani test qiluvchi sifatida ishlatish - eng keng tarqalgan xato: u bottleneck'ga aylanadi va sprint oxirida "QA ulgurmadi" degan doimiy holat paydo bo'ladi.

Ishlaydigan taqsimot quyidagicha. Developer'lar barcha kod ichidagi testlarni o'zi yozadi va egalik qiladi: unit, slice, Testcontainers bilan integratsion, contract. Bu muhokama mavzusi emas - Definition of Done'ga yoziladi va PR'da tekshiriladi. QA kod yozishdan ko'ra ko'proq "sifat dizayneri" bo'ladi: grooming'da qatnashadi, qabul kriteriyalarini misollar bilan to'ldiradi (Example Mapping), har story uchun qisqa risk ro'yxatini beradi va eng ko'p vaqtini exploratory testing'ga sarflaydi - chunki aynan shu ishni developer o'rniga bajara olmaydi.

E2E suite'ni kichik ushlab turish shart: 10-20 ta eng muhim biznes yo'li, boshqa hech narsa. Bu suite'ni yozishda QA ssenariyni belgilaydi, developer esa texnik qismini yozadi (yoki juftlikda ishlashadi) - bunda QA avtomatlashtirish bo'yicha ortiqcha yuklanmaydi va suite jamoa bilimida qoladi.

Qolgan ishlar aniq egalarga tarqatiladi: CI/CD va test muhiti - bitta developer "build egasi" sifatida (yoki DevOps bo'lsa, u); performance testlari - talab paydo bo'lganda arxitektor bilan birga; security skanerlar - pipeline'da avtomatik. Arxitektor esa testlanuvchanlikni dizaynga kiritadi va shablonlarni beradi, shunda yangi test yozish 20 daqiqalik ish bo'ladi, bir kunlik emas. Qoida sodda: QA bitta bo'lsa, u testlarni emas, sifat jarayonini masshtablashi kerak.

## 3.10 Arxitektor nazorat ro'yxati

- [ ] Har bir test turi uchun RACI'da "Accountable" aniq belgilangan va hech bir qator egasiz emas.
- [ ] Definition of Done'da developer uchun unit, slice va integratsion test majburiyati yozilgan va PR'da tekshiriladi.
- [ ] Three Amigos yoki Example Mapping jarayoni mavjud; ochiq "qizil karta"li story sprintga kirmaydi.
- [ ] Test kodi production kodi bilan bir xil review standartida va test review checklist jamoada qo'llaniladi.
- [ ] Har bir test suite'ning egasi `CODEOWNERS` yoki shunga teng joyda qayd etilgan.
- [ ] Buzilgan test uchun "kim tuzatadi" qoidasi yozilgan, qizil main branch eng yuqori prioritet deb qabul qilingan.
- [ ] Tanlangan jamoa modeli (embedded / markazlashgan / enabling / developer-owned) ongli ravishda tanlangan, tasodifiy shakllanmagan.
- [ ] QA soni kam bo'lsa, QA vaqti exploratory va qabul kriteriyalariga, regressiya esa avtomatlashtirishga yo'naltirilgan.

---

[&larr; 2. Test piramidasi va test turlari xaritasi](02-test-piramidasi-va-test-turlari-xaritasi.md) · [Mundarija](README.md) · [4. Tester qanday ishlashi kerak: QA ish jarayoni &rarr;](04-testrovshik-qanday-ishlashi-kerak-qa-ish.md)
