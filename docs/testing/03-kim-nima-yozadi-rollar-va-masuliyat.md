<!-- doc: testing | chapter: 3 | part:  -->

[Barcha hujjatlar](../../README.md) / [Testlash qo'llanmasi](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 3. Kim nima yozadi: rollar va mas'uliyat (Who Writes What - Roles & Responsibilities)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

- [3.1 Rollar ta'rifi va farqi](#31-rollar-tarifi-va-farqi)
- [3.2 Mas'uliyat matritsasi (RACI)](#32-masuliyat-matritsasi-raci)
- [3.3 "Developer unit test yozadi, QA E2E yozadi" qoidasining chegaralari](#33-developer-unit-test-yozadi-qa-e2e-yozadi-qoidasining-chegaralari)
- [3.4 Three Amigos va Example Mapping](#34-three-amigos-va-example-mapping)
- [3.5 QA'ning sprint ichidagi joyi](#35-qaning-sprint-ichidagi-joyi)
- [3.6 Test kodini code review qilish](#36-test-kodini-code-review-qilish)
- [3.7 Jamoa modellari](#37-jamoa-modellari)
- [3.8 Test ownership](#38-test-ownership)
- [3.9 1 QA va 5 developer: kichik jamoa uchun amaliy model](#39-1-qa-va-5-developer-kichik-jamoa-uchun-amaliy-model)
- [3.10 Ishni QA ga "devor orqali" uzatmaslik](#310-ishni-qa-ga-devor-orqali-uzatmaslik)
- [3.11 Arxitektor nazorat ro'yxati](#311-arxitektor-nazorat-royxati)

</details>



Testlash strategiyasi qog'ozda qanchalik go'zal bo'lsa ham, uni real hayotga aylantiradigan narsa - kim nimani yozadi, kim nimaga javob beradi va buzilgan testni kim tuzatadi degan savollarga berilgan aniq javoblardir. Meszaros bu holatni loyiha darajasidagi "smell" deb qayd etadi: "Developers Not Writing Tests" ning sabablari vaqt yetishmasligi, testlash qiyin bo'lgan dizayn yoki noto'g'ri avtomatlashtirish strategiyasi bo'ladi, natijada jamoa test qarzi hisobidan ishlaydi va yangi funksionallik qo'shish asta-sekin qimmatlashadi (Gerard Meszaros, *xUnit Test Patterns*, 17-bob, 263-265-bet). Bu bobda rollarni, mas'uliyat matritsasini, jamoa modellarini va test ownership masalasini arxitektor nuqtai nazaridan ko'rib chiqamiz. Maqsad - tashkiliy chizma chizish emas, balki sifat uchun javobgarlikni texnik qarorlar bilan bir xil joyga, ya'ni kodni yozadigan jamoaga yaqinlashtirish.

## 3.1 Rollar ta'rifi va farqi

Rol - bu lavozim emas, balki mas'uliyat to'plami. Kichik jamoada bitta odam uch-to'rt rolni olib yurishi mutlaqo normal; muhimi - rol egasi yo'q bo'lib qolmasligi.

Kitoblar rollarni nomlab bermaydi, lekin ishni kim bajarishi bo'yicha aniq chiziq tortadi. McConnell test turlarini ikkiga ajratadi: developer o'zi bajaradigan testlar (unit, component, integratsion, ba'zan regressiya va system testi) va maxsus test xodimlari bajaradigan, developer kamdan-kam qiladigan testlar (beta test, mijoz qabul testi, performance, konfiguratsiya, platforma, stress va usability testlari). Shu yerda yana bir chiziq bor: white-box test - o'zi yozgan kodni ichidan bilib tekshirish, black-box esa o'zi yozgan kodga qo'llanmaydi (*Code Complete*, 2-nashr, 22-bob, 499-500-bet).

Google da test yozish butun muhandislik xodimlariga taqsimlangan: tizimni quradigan muhandislar o'z kodi uchun avtomatik test yozishda va uni ishga tushirishda faol qatnashadi, va QA kuchli tashkilot bo'lgan kompaniyalarda ham developer yozgan test odatiy hol (*Software Engineering at Google*, 11-bob "Testing Overview"). Shu bilan birga Google da "Test Engineer" degan alohida muhandislik roli bor va yaxshi test engineer dan kutiladigan asosiy ko'nikma - mahsulot uchun test strategiyasini tuzish, ya'ni asosiy risk yo'nalishlarini va ularni yopadigan test turlarini belgilash (o'sha kitob, 14-bob "Larger Testing").

Quyidagi ro'yxat shu ikki chiziqni Spring loyihalari lug'atiga ko'chiradi. Rol nomlari korpusning o'z modeli; kitobdan olingani - ishning taqsimlanish chizig'i.

| Rol | Asosiy mas'uliyat | Odatda yozadigan yoki boshqaradigan testlar |
|---|---|---|
| Developer | O'zi yozgan kodning ishlashiga javob beradi; testni kod bilan bir PR'da yetkazadi | Unit, slice (`@WebMvcTest`, `@DataJpaTest`), integratsion (Testcontainers), contract producer/consumer |
| QA Engineer (manual) | Exploratory testing, qabul kriteriyalarini tekshirish, edge case'larni kashf qilish | Qo'lda exploratory sessiyalar, qabul testi, UAT yordami |
| Automation QA / SDET | Avtomatlashtirish freymvorki, E2E va API test suite'lari, test ma'lumotlari vositalari | E2E (Selenium/Playwright), API testlar, `RestAssured` ssenariylari, test data builder'lar |
| QA Lead | Sprint ichidagi sifat jarayoni, QA resurslarini taqsimlash, release holati haqida hisobot | Test rejasi, regressiya qamrovi, risk bo'yicha prioritetlash |
| Test Architect | Test strategiyasi, piramidaning shakli, test freymvork standartlari | Shablonlar, baza test klasslari, konvensiyalar, qamrov siyosati |
| DevOps / Platform | CI/CD pipeline, test muhiti, Testcontainers uchun resurslar, parallel bajarilish | Infratuzilma, Docker image'lar, cache, test reportlari |
| Product Owner | Testlanadigan qabul kriteriyalari, biznes qoidalarining aniqligi, prioritet | Qabul kriteriyalari, misollar (example), UAT qarori |
| Arxitektor | Testlanuvchanlikni dizaynga kiritish, modul chegaralari, contract'lar, nofunksional talablar | Arxitektura testlari (ArchUnit), contract chegaralari, SLA/SLO talablari |

Arxitektor bu ro'yxatda alohida o'rinda turadi: u test yozmasligi mumkin, lekin testlash mumkin bo'lmagan arxitektura uchun aynan u javobgar. Meszaros "Developers Not Writing Tests" ning uchta sababini sanaydi va ikkitasi to'g'ridan-to'g'ri dizaynga tegishli: testlashga moslanmagan kod (Hard-to-Test Code) va Fragile Test keltirib chiqaradigan test muhiti yoki avtomatlashtirish strategiyasi; uchinchisi - vaqt va ko'nikma yetishmasligi (*xUnit Test Patterns*, 17-bob, 263-264-bet). Static metodlarga to'la util'lar, `new` bilan yaratilgan dependency'lar, bitta 4000 satrli service - bular QA muammosi emas, dizayn muammosi.

## 3.2 Mas'uliyat matritsasi (RACI)

RACI'da **R** (Responsible) - ishni bajaradigan, **A** (Accountable) - yakuniy javobgar (har qatorda faqat bitta), **C** (Consulted) - maslahat so'raladigan, **I** (Informed) - xabardor qilinadigan tomon. Quyidagi matritsa korpusning o'z taklifi, kitobdan ko'chirilgan jadval emas: uni jamoangizga moslashtirish kerak, lekin "A" ustunini bo'sh qoldirmang.

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

Matritsadagi ikki qator kitobga tayanadi. Birinchi - unit va integratsion testda "R" doimo developer'da: Google da har bir o'zgarish code review dan o'tadi, har o'zgarishdan funksional kod bilan birga test kutiladi va test yo'q bo'lgani uchun o'zgarishni to'sish mutlaqo o'rinli deb qabul qilingan (*Software Engineering at Google*, 11-bob). Ikkinchi - test strategiyasi va qamrovi katta testlar bo'yicha "A" ni egasiz qoldirmaslik: egasi hujjatlashtirilmagan katta test chiriydi, chunki uni o'zgartirish qiyinlashadi va nosozlikni tahlil qilish uzoqqa cho'ziladi (o'sha kitob, 14-bob "Owning Large Tests").

Release sign-off qatorida yakuniy javobgarni biznes tomoniga qo'yish - korpusning amaliy tanlovi, kitobdan olingan qoida emas.

## 3.3 "Developer unit test yozadi, QA E2E yozadi" qoidasining chegaralari

Bu qoida boshlang'ich taqsimot sifatida foydali, lekin qattiq devorga aylansa quyidagi zararlarni keltiradi.

Birinchidan, o'rtadagi qatlam egasiz qoladi. Unit va E2E orasida service-to-service integratsiya, DB tranzaksiyalari, mapping, xato ishlovi va contract'lar bor. Qamrovi katta testda egalik muammosi kitobda ham aynan shunday qo'yilgan: unit testning egasi aniq - birlikni egallagan muhandis va jamoa, qamrovi katta test esa bir necha egani kesib o'tadi, shuning uchun uni kim qo'llab-turadi va buzilganda kim tahlil qiladi degan savol uzoq muddatli muammoga aylanadi; aniq egasi bo'lmagan test chiriydi (*Software Engineering at Google*, 14-bob "Why Not Have Larger Tests?"). Natijada bo'shliq E2E bilan to'ldiriladi va test to'plami "ice cream cone" shakliga o'tadi: ko'p end-to-end test, kam integratsion va unit test; bunday to'plam sekin, ishonchsiz va ishlash uchun og'ir bo'ladi (o'sha kitob, 11-bob "Test Scope").

Ikkinchidan, feedback aylanasi uzayadi. Kitob feedback aylanalarini eng tezdan eng sekinga qarab tartiblaydi: lokal edit-compile-debug, presubmit avtomatik test natijasi, submit'dan keyin topilgan integratsiya xatosi, staging muhitida QA tester topgan nomoslik, ichki foydalanuvchi hisoboti, tashqi foydalanuvchi yoki matbuot hisoboti (*Software Engineering at Google*, 23-bob "Continuous Integration"). Developer o'z kodining integratsiyada ishlashini sprintning oxirida QA dan bilsa, u shu ro'yxatning quyi qismida ishlayotgan bo'ladi.

Uchinchidan, developer testining o'z tizimli cheklovlari bor va ularni rolni qattiq ajratish bilan yopib bo'lmaydi. McConnell uchta cheklovni sanaydi: developer "clean test" yozishga moyil, ya'ni kod ishlashini tekshiradi, kodning qanday buzilishini emas - yetuk test tashkilotlarida bitta clean test'ga besh dirty test to'g'ri keladi, yetuk bo'lmaganida esa nisbat teskari; developer o'z qamrovini ortiqcha baholaydi; va developer murakkabroq qamrov turlarini chetlab o'tadi, statement coverage ni yetarli deb hisoblaydi (*Code Complete*, 2-nashr, 22-bob, 503-504-bet). Xulosa shu yerda ham yozilgan: developer testi qimmatli, lekin yolg'iz o'zi sifat kafolati uchun yetarli emas va mustaqil test hamda collaborative construction texnikalari bilan to'ldirilishi kerak.

Shu bilan birga "test dizayni texnikalari QA'ning bilimi" degan qarash noto'g'ri: ekvivalentlik sinflari, chegara tahlili va error guessing *Code Complete* da developer testining asboblari sifatida beriladi (22.3-bo'lim, 512-515-bet). Haqiqiy farq bilimda emas, ko'r nuqtada: barcha collaborative texnikalar developer o'z ishidagi muammoli joylarni ko'rmasligi va boshqa odamning ko'r nuqtasi boshqa joyda bo'lishi g'oyasiga tayanadi (*Code Complete*, 21-bob, 480-bet). Buni raqam ham tasdiqlaydi: inspeksiyada topilgan xatolarning faqat 20 foizini bir nechta tekshiruvchi topgan, ya'ni odamlar bir-biriga o'xshamagan defektlarni ko'radi (o'sha kitob, 20-bob, 471-bet).

To'rtinchidan, unit testni kodni yozgan odam yozadi va shu sabab **tushunmovchilik kodda ham, testda ham bir xil takrorlanadi**. Google buni "working as implemented" deb ataydi: test kod yozilganiday ishlayotganini tasdiqlaydi, niyatga mosligini emas. Uning qarshi vositasi - UAT (user acceptance test): aniq oxirgi mijoz yoki uning vakili (mijoz qo'mitasi, product manager) bo'lgan joyda mahsulotni **ochiq API orqali** o'tadigan foydalanuvchi yo'li testlari yoziladi va ular xulqning niyatga mosligini tekshiradi. Cucumber va RSpec kabi freymvorklar bu testlarni "bajariladigan spetsifikatsiya" shaklida yozishga xizmat qiladi.

ESLATMA: Google ning o'zi avtomatik UAT ni ko'p ishlatmaydi va spetsifikatsiya tillarini deyarli qo'llamaydi, chunki ularning mahsulotlarini tarixiy jihatdan muhandislarning o'zi yaratgan va kutilgan xulqni belgilaydigan odamlar kod tilini biladi. Ya'ni UAT ning qiymati rolga bog'liq: mijoz vakili texnik bo'lmasa, bajariladigan spetsifikatsiya o'zini oqlaydi; bo'lmasa, oddiy integratsion test arzonroq.

To'g'ri yondashuv - "kim yozadi" emas, "kim qaysi riskka javob beradi". Developer kod ichidagi riskni yopadi (unit'dan Testcontainers'gacha), QA esa foydalanuvchi va biznes riskini yopadi (exploratory, qabul, end-to-end ssenariylar). Qatlam emas, risk turi bo'yicha bo'linish barqarorroq.

## 3.4 Three Amigos va Example Mapping

Bu bo'limdagi ikki format nomi (Three Amigos uchrashuvi va Example Mapping kartalari) korpusda mavjud kitoblarda yo'q, shuning uchun ularni kitob tavsiyasi deb o'qimang. Formatning ostidagi g'oya esa ikki kitobda ham bor: misollarni kod yozilishidan oldin sanab chiqish.

Meszaros buni customer test darajasida yozadi: testlarni ishni boshlashdan oldin sanab chiqish avtomatlashtiriladimi yoki yo'qmi - muhim qadam, chunki u jamoaga mijoz nimani xohlayotganini tushuntiradi va muvaffaqiyat nima ekanini aniqlaydi; bir story uchun testlarni story ishiga kirishdan oldin tayyorlash mantiqan to'g'ri, ba'zi jamoalar esa story ni baholashdan oldin ham testlar belgilangan bo'lishini talab qiladi, chunki testlar story ni shakllantiradi (*xUnit Test Patterns*, 1-bob, 5-bet va 4-bob, 34-bet).

McConnell shu fikrni talab darajasiga ko'taradi: test case'larni talab bosqichida yoki iloji boricha ertaroq, tekshirilishi kerak bo'lgan birlik yozilishidan oldin rejalashtirish kerak, va test case'ni avval yozish talabdagi muammolarni tezroq ochadi - yomon talab uchun test case yozish qiyin (*Code Complete*, 2-nashr, 22-bob, 503-504-bet). U yana bir foydali ro'yxat beradi: talab bosqichida odatda e'tibordan chetda qoladigan narsalarni ataylab testlash kerak - xavfsizlik darajasi, saqlash, o'rnatish protsedurasi va tizim ishonchliligi (o'sha joy, 503-bet).

Amalda bu quyidagicha ko'rinadi. "Foydalanuvchi buyurtmani bekor qilishi mumkin" story'si uchun qoidalar va ularning har biriga konkret misol yoziladi, javobi yo'q savollar esa alohida belgilanadi.

- Qoida 1: faqat `NEW` yoki `PAID` statusdagi buyurtma bekor qilinadi.
  - Misol: `NEW` buyurtma → bekor qilindi, status `CANCELLED`.
  - Misol: `SHIPPED` buyurtma → `409 Conflict`, status o'zgarmaydi.
- Qoida 2: `PAID` buyurtma bekor qilinsa, to'lov avtomatik qaytariladi.
  - Misol: to'langan buyurtma → refund `PaymentService`'ga yuboriladi, event `OrderCancelled` chiqadi.
  - Ochiq savol: refund xato bersa, buyurtma `CANCELLED` bo'lib qoladimi yoki rollback bo'ladimi?
- Qoida 3: bekor qilish faqat buyurtma egasi yoki `ROLE_SUPPORT` tomonidan.
  - Misol: boshqa foydalanuvchi → `403`.

Eng qimmatli natija - ochiq savol. U aniqlanmasa, developer o'zicha qaror qabul qiladi, QA boshqa narsani kutadi va bug sprintning oxirida chiqadi. Yashil misollar esa keyinchalik to'g'ridan-to'g'ri test nomlariga aylanadi - `shouldReturn409WhenCancellingShippedOrder` kabi; test nomini tekshirilayotgan xulqdan olish Google ning test yozish qoidalaridan biri (*Software Engineering at Google*, 12-bob "Name Tests After the Behavior Being Tested").

## 3.5 QA'ning sprint ichidagi joyi

QA sprintning oxirida paydo bo'ladigan bosqich emas, balki butun sprint davomida ishtirok etadigan rol. Bunday taqsimotning asosi - defektni ishlab chiqish oqimida qancha erta topsang, shuncha arzon tushishi: test case'larni mahsulot bilan birga dizayn qilish talab va dizayn xatolarini ochadi, ular esa kodlash xatolaridan qimmatroq turadi (*Code Complete*, 2-nashr, 22-bob, 503-bet).

Grooming yoki refinement bosqichida QA eng foydali savollarni beradi: "bu holatda nima bo'ladi?", "chegara qiymati qanday?", "eski ma'lumotlar bilan nima qilamiz?", "bu o'zgarish qaysi integratsiyalarga ta'sir qiladi?". Shu bosqichda topilgan noaniqlik eng arzon.

Qabul kriteriyalarini testlanadigan holatga keltirish - QA'ning asosiy hissasi, chunki yomon talab uchun test case yozib bo'lmaydi va shu qiyinchilikning o'zi talabdagi kamchilikni ko'rsatadi (o'sha joy, 504-bet). "Tez ishlashi kerak" degan kriteriya o'lchov, yuk darajasi va chegara bilan qayta yozilishi kerak; "to'g'ri hisoblanishi kerak" esa konkret kirish va chiqish qiymatlari jadvaliga aylantiriladi. 4.2-bo'limda shu qayta yozish uchun jadval bor.

Story ishlanayotganda QA tayyor bo'lgan qismni darhol tekshiradi, exploratory sessiyalar o'tkazadi va avtomatlashtirish uchun ssenariylarni tanlaydi. Sprint oxirida regressiya ko'p hollarda avtomatik ishlaydi - QA faqat o'zgargan sohaga yo'naltirilgan qo'shimcha exploratory qiladi. Release holati bo'yicha yozma hisobot berish (nima tekshirildi, nima tekshirilmadi, qanday ma'lum muammolar qoldi) va qarorni biznes tomoniga qoldirish - korpusning amaliy tartibi, kitobdan olingan talab emas.

## 3.6 Test kodini code review qilish

Test kodi - production kodi. Kitob buni to'g'ridan-to'g'ri aytadi: katta test to'plami bilan yashashning siri unga hurmat bilan munosabatda bo'lish, testlarni production kodi kabi qarash va oddiy o'zgarish uzoq vaqt talab qila boshlaganda testlarni mo'rtlikdan tozalashga vaqt sarflash (*Software Engineering at Google*, 11-bob "The Pitfalls of a Large Test Suite"). Review ning majburiyligi ham shu kitobda: Google da har bir o'zgarish code review dan o'tadi, har o'zgarishda funksional kod ham test ham bo'lishi kutiladi va reviewer ikkisining sifatini ham to'g'riligini ham tekshiradi (o'sha bob, "Testing Culture Today").

Review ning nega kerakligi *Code Complete* da raqam bilan berilgan: formal code inspection ning defekt topish darajasi (modal) 60 foiz, unit test ning 30 foiz, integratsion testning 35 foiz; hech bir usul yolg'iz 75 foizdan oshmaydi, shuning uchun usullar birgalikda ishlaydi (20-bob, 470-471-bet). Shu bobda yana bir muhim nuqta bor: review test topa olmaydigan narsalarni topadi - tushunarsiz xato xabari, yetarli bo'lmagan izoh, kodga qotib qolgan qiymat, takrorlangan kod shabloni (21-bob, 481-bet).

Review'ni kim qiladi: unit va integratsion testlarni boshqa developer; E2E va avtomatlashtirish freymvorkini SDET yoki QA Lead; yangi test turi yoki yangi baza klass qo'shilganda arxitektor ham ko'radi. Bu taqsimot korpusning amaliy tartibi. Kichik jamoada QA developer'ning test PR'iga review qo'shilishi foydali, chunki u test dizayni bo'yicha bo'shliqlarni ko'radi.

Test review checklist. Har bandning yonida uni tasdiqlagan manba ko'rsatilgan; manbasiz bandlar korpusning o'z tajribasidan.

- Test nomi nimani tekshirayotganini kod o'qimasdan tushuntiradimi? (*Software Engineering at Google*, 12-bob)
- Bitta testda bitta shart tekshirilganmi? (*xUnit Test Patterns*, 5-bob, Verify One Condition per Test, 45-bet)
- Assertion mazmunlimi - `assertNotNull` yoki `assertTrue(true)` bilan "yashil" qilinmaganmi?
- Test implementatsiyani emas, xulq-atvorni tekshiradimi? Mock va behavior verification ni ortiqcha ishlatish Overspecified Software va Fragile Test ga olib keladi (*xUnit Test Patterns*, 5-bob, Use the Front Door First, 40-41-bet); Google da ham mocking freymvorklarini suiiste'mol qilish eng og'ir muammolardan biri bo'lgan (*Software Engineering at Google*, 11-bob)
- Testlar bir-biridan mustaqilmi: tartibga, umumiy static holatga yoki umumiy bazaga bog'liq emasmi? Test hermetic bo'lishi, ya'ni o'z muhitini o'zi tayyorlab o'zi tozalashi kerak (*Software Engineering at Google*, 11-bob "Properties Common to All Test Sizes"; *xUnit Test Patterns*, 5-bob, Keep Tests Independent, 42-43-bet)
- Testda shart va sikl kabi control flow bormi? Test o'qilganda darhol to'g'ri ko'rinishi kerak, chunki testning testi yo'q va uning to'g'riligini faqat odam tekshiradi (*Software Engineering at Google*, 11-bob va 12-bob "Don't Put Logic in Tests")
- `Thread.sleep` yoki shunga o'xshash kutish ishlatilmaganmi? Kitob buni testni sekinlashtiradigan sun'iy chegara deb ataydi va holat o'zgarishini qisqa intervalda tekshirish (poll) hamda timeout bilan almashtirishni tavsiya qiladi (*Software Engineering at Google*, 11-bob)
- Test ma'lumotlari builder yoki test utility metod orqali, niyatni ko'rsatadigan nom bilan tayyorlanganmi? (*xUnit Test Patterns*, 5-bob, Communicate Intent, 41-bet)
- Negative va boundary holatlar qamrab olinganmi, yoki faqat happy path bormi? Developer testi "clean test" ga moyil (*Code Complete*, 22-bob, 503-bet)
- Test to'g'ri darajada turganmi - unit bilan yetarli bo'ladigan narsa uchun butun Spring context ko'tarilmaganmi? Google qoidasi: iloji bo'lsa eng kichik o'lchamdagi testni yozish (*Software Engineering at Google*, 11-bob "Test Size")
- Test buzilganda xato xabari muammoni ko'rsatadimi? (*Software Engineering at Google*, 12-bob "Write Clear Failure Messages")

Yomon test review'dan o'tib ketmasligi kerak: kitob buni ochiq yozadi - yomon test merge qilinishidan oldin tuzatiladi, aks holda u keyingi muhandislarga tormoz bo'ladi (*Software Engineering at Google*, 12-bob "The Importance of Maintainability").

## 3.7 Jamoa modellari

Quyidagi to'rt model korpusning o'z klassifikatsiyasi; kitoblarda bunday taksonomiya yo'q.

| Model | Kuchli tomoni | Kuchsiz tomoni | Qachon mos |
|---|---|---|---|
| Embedded QA (jamoa ichida) | Tez feedback, kontekstni chuqur bilish | QA'lar o'rtasida standart tarqaladi, bilim almashinuvi sust | Mustaqil product jamoalari, kichik squad'lar |
| Markazlashgan QA bo'limi | Yagona standart, resurslarni qayta taqsimlash oson, chuqur ekspertiza | "Devor ustidan tashlash", uzun feedback, QA bottleneck'ga aylanadi | Ko'p mahsulotli yirik tashkilot |
| QA enabling team (platforma sifatida) | Freymvork, shablon va CI'ni markaziy beradi, jamoalar o'zi yozadi | Jamoalarda minimal test madaniyati bo'lishi talab qilinadi | O'sayotgan tashkilot, mikroservis landshaft |
| Developer-owned quality | Eng qisqa feedback, to'liq ownership, tez release | Exploratory va UX riski ko'rinmaydi, developer ko'r nuqtalari qoladi | Kuchli muhandislik madaniyati, past biznes riski |

Oxirgi model Google da qanday ishlaganini kitob batafsil yozadi va undan uch xulosa chiqadi. Birinchi - u "QA funksiyasi yo'q" degani emas: Google da Test Engineer roli bor, avtomatlashtirish qila olmaydigan ishlar uchun esa odam baholashi ishlatiladi (qidiruv natijalari sifati, audio va video sifati, murakkab xavfsizlik zaifliklarini izlash) va bu ishlar exploratory testing deb ataladi (*Software Engineering at Google*, 11-bob "The Limits of Automated Testing"; 14-bob "Exploratory Testing"). Ikkinchi - bunday modelga o'tish buyruq bilan emas, madaniyat bilan boshlanadi: Google da test yozishni yuqoridan majburlash g'oyasi ataylab rad etilgan, buning o'rniga orientatsiya darslari, Test Certified (beshta daraja, har biri bir chorakda bosib o'tiladigan) va Testing on the Toilet qo'llanilgan (o'sha kitob, 11-bob "History of Testing at Google"). Uchinchi - bu vaqt oladi: kitobning o'z xulosasi "tashkilotda test madaniyatini o'zgartirish vaqt talab qiladi" degan jumla bilan tugaydi (o'sha bob, TL;DR).

Ko'p tashkilotlar uchun embedded QA plus kichik enabling team kombinatsiyasi qulay: har jamoada sifat egasi bor, umumiy freymvork va CI esa markazda saqlanadi. Bu tanlov korpusning tavsiyasi.

## 3.8 Test ownership

Har bir test suite'ning nomma-nom egasi bo'lishi kerak. Kitob buni talab darajasida qo'yadi: qamrovi katta testlar hujjatlashtirilgan egaga ega bo'lishi shart - testga kelgan o'zgarishni ko'rib chiqa oladigan va test buzilganda yordam bera oladigan muhandis; egasi bo'lmasa testni o'zgartirish qiyinlashadi, nosozlikni hal qilish cho'ziladi va test chiriydi (*Software Engineering at Google*, 14-bob "Owning Large Tests").

Egalikni kitob quyidagicha taqsimlaydi: bitta loyiha ichidagi komponentlarning integratsion testlari loyiha lead'ida; bir necha servisni kesib o'tadigan, biznes funksiyasiga bog'langan testlar "feature egasi"da - bu funksiyani boshdan oxir amalga oshirgan muhandis, ba'zan product manager yoki biznes ssenariyning tavsifini egallagan test engineer bo'lishi mumkin. Egalikni avtomatlashtirish uchun ikki usul ishlatiladi: kod egaligi (monorepo dagi `OWNERS` ma'lumoti) va test metodining o'ziga yozilgan annotatsiya, bu esa aynan qaysi test metodi yiqilganda kimga murojaat qilish kerakligini ko'rsatadi (o'sha joy). Git asosidagi loyihada bunga `CODEOWNERS` to'g'ri keladi.

Buzilgan testni kim tuzatadi degan savolga kitobda ikki javob bor. Birinchi - testni buzgan o'zgarishni kiritgan odam: Google ning "Beyonce qoidasi" shuni aytadi, agar sizning testlaringiz o'tib ketgan begona infratuzilma o'zgarishi mahsulotingizni buzsa, tuzatish va qo'shimcha test yozish sizning zimmangizda (*Software Engineering at Google*, 11-bob "The Beyonce Rule"). Ikkinchi - tezlik: buzilgan testni nosozlikdan keyin daqiqalar ichida tuzatishni prioritet qilgan jamoalar testga ishonchni yuqori, nosozlikni izolyatsiyalashni tez saqlaydi va testdan ko'proq foyda oladi (o'sha bob, "Write, Run, React"). Shu sababli qizil main branch boshqa ishlardan ustun turadi.

Katta E2E test to'plamlari bilan ishlaydigan jamoalar uchun kitob yana bir amaliy tartibni yozadi: vaqtincha o'chirilgan testlarni ro'yxatga olib borish mexanizmi bo'lishi kerak, release'ni to'sadigan buglar darhol tuzatiladi, to'smaydiganlari esa prioritetlanadi - aks holda to'plam o'chirilgan eski testlarning o'sib boruvchi uyumiga aylanadi (*Software Engineering at Google*, 23-bob "Continuous Integration"). Nightly suite uchun ertalabki rotatsiya va infratuzilma nosozligini platforma on-call'iga yo'naltirish - korpusning amaliy tartibi.

## 3.9 1 QA va 5 developer: kichik jamoa uchun amaliy model

Ko'p jamoada bitta QA bir necha developer'ga to'g'ri keladi. Bu holatda QA'ni hamma narsani test qiluvchi sifatida ishlatish - eng keng tarqalgan xato: u bottleneck'ga aylanadi va sprint oxirida "QA ulgurmadi" degan doimiy holat paydo bo'ladi.

Ishlaydigan taqsimot quyidagicha. Developer'lar barcha kod ichidagi testlarni o'zi yozadi va egalik qiladi: unit, slice, Testcontainers bilan integratsion, contract. Bu muhokama mavzusi emas - Definition of Done'ga yoziladi va PR'da tekshiriladi; Google da ham bu shunday ishlaydi, test yo'qligi uchun o'zgarishni to'sish o'rinli deb qabul qilingan (*Software Engineering at Google*, 11-bob). QA kod yozishdan ko'ra ko'proq sifat dizayneri bo'ladi: grooming'da qatnashadi, qabul kriteriyalarini misollar bilan to'ldiradi, har story uchun qisqa risk ro'yxatini beradi va eng ko'p vaqtini exploratory testing'ga sarflaydi - chunki aynan shu ishni avtomatlashtirish qoplay olmaydi (o'sha kitob, 11-bob "The Limits of Automated Testing").

E2E suite'ni kichik ushlab turish shart. Kitobning taqsimoti aniq: test case soni bo'yicha taxminan 80 foiz tor qamrovli unit test, 15 foiz integratsion test va 5 foiz butun tizimni tekshiradigan end-to-end test, har jamoada nisbat bir oz farq qiladi (*Software Engineering at Google*, 11-bob "Test Scope"). Bu suite'ni yozishda QA ssenariyni belgilaydi, developer esa texnik qismini yozadi (yoki juftlikda ishlashadi) - bunda QA avtomatlashtirish bo'yicha ortiqcha yuklanmaydi va suite jamoa bilimida qoladi.

Arxitektorning bu modeldagi vazifasi - test yozish narxini pasaytirish. Meszaros buni principle qilib qo'yadi: testni yozish yoki o'zgartirishga ketadigan kuch mos funksionallikni amalga oshirishga ketadigan kuchdan oshmasligi kerak, test yozish uchun ishlatiladigan asboblar esa funksionallikni yozish asboblaridan ko'proq ekspertiza talab qilmasligi kerak (*xUnit Test Patterns*, 5-bob, Ensure Commensurate Effort and Responsibility, 47-48-bet). U shu bobda yana bir kuzatuvni yozadi: jarayonni o'zlashtirgan developer test va kodni, avval faqat kod yozib debug qilishga ketgan vaqt ichida yozadi (o'sha kitob, 17-bob, 263-bet).

Qolgan ishlar aniq egalarga tarqatiladi: CI/CD va test muhiti - bitta developer "build egasi" sifatida (yoki DevOps bo'lsa, u); performance testlari - talab paydo bo'lganda arxitektor bilan birga; security skanerlar - pipeline'da avtomatik. Qoida sodda: QA bitta bo'lsa, u testlarni emas, sifat jarayonini masshtablashi kerak.

## 3.10 Ishni QA ga "devor orqali" uzatmaslik

Yuqoridagi taqsimotning eng ko'p buziladigan joyi uzatish nuqtasi. Gergely Orosz buni to'g'ridan-to'g'ri anti-pattern deb ataydi: QA bo'lgan ba'zi muhandislik jamoalari testlash va sifat ta'minotini butunlay QA ning mas'uliyati deb hisoblaydi, shuning uchun ishni qurib bo'lgach, edge case'lar va uni qanday testlash haqida o'ylamasdan, hatto eng sodda qo'lda tekshiruvni ham qilmasdan QA ga uzatadi (Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 11-bob, 160-bet).

Narxi vaqtda o'lchanadi. Orosz aylanani shunday ko'rsatadi: QA eng ko'zga tashlanadigan muammolarni topadi, ya'ni har qanday muhandis eng sodda tekshiruv bilan o'zi topa oladigan turini, va ishni qaytaradi; muhandis tuzatib yana uzatadi; QA bu safar nozikroq xatolarni topadi va yana qaytaradi; ish faqat uchinchi tekshiruv davridan keyin kutilgandek ishlaydi deb e'lon qilinadi (o'sha manba, 160-bet). Ikkita ortiqcha davr to'liq yo'qotilgan vaqt.

Orosz uchta tuzatish beradi (o'sha manba, 160-bet):

- **QA rejalashtirishdan boshlab ishtirok etadi** va test rejasi birgalikda tuziladi. QA muhandislarida ekzotik edge case va qiyin ushlanadigan xatolarni sezish ko'nikmasi kuchli; ular tizimni qanday "stress test" qilishini o'rganib, shu ekspertizani mustahkamroq test rejasiga aylantirish kerak.
- **Yonma-yon ishlash**, tashlab yuborish emas: aks holda muhandis QA tekshirishini kutib bo'sh o'tiradi.
- **QA borligini tabiiy deb bilmaslik.** Ko'p jamoada maxsus QA yo'q; QA bilan ishlaganda undan o'rganib, o'z QA ko'nikmangizni o'stirasiz, chunki keyingi jamoada bu ish sizga qoladi.

Uzatishdan oldingi tayyorgarlik ham shu qoidaning bir qismi. Orosz oddiy bo'lmagan (non-trivial) xususiyatni yozishdan oldin test rejasini tuzishni talab qiladi: qaysi qo'lda test case'lar bo'ladi, qaysi qismi unit, integratsion yoki end-to-end test bilan avtomatlashtiriladi, qaysi qismini faqat production'da tekshirish mumkin va bu qanday qilinadi. Eng yaxshi payt aynan rejalashtirish bosqichi; tayyor reja esa product manager, biznes tomoni, boshqa muhandislar va QA ga ko'rsatilib fikr olinadi (o'sha manba, 11-bob, 159-bet). Test va monitoring ishi bahoning ichiga kiritiladi, alohida band qilib ajratilmaydi: ajratilgan zahoti uni vaqt tejash uchun birinchi bo'lib tashlab yuborishni taklif qilishadi (o'sha joy).

Bu qoida [3.3](#33-developer-unit-test-yozadi-qa-e2e-yozadi-qoidasining-chegaralari) ning teskari tomoni. U yerda QA ning ishi developer'ga yuklanmasligi aytilgan bo'lsa, bu yerda developer'ning ishi QA ga yuklanmasligi aytiladi: PR uzatilishidan oldin muallifning o'zi golden path'ni ishlatib ko'rgan va ma'lum edge case'larni sanab chiqqan bo'lishi kerak.

## 3.11 Arxitektor nazorat ro'yxati

- [ ] Har bir test turi uchun mas'uliyat matritsasida "Accountable" aniq belgilangan va hech bir qator egasiz emas.
- [ ] Definition of Done'da developer uchun unit, slice va integratsion test majburiyati yozilgan va PR'da tekshiriladi; testsiz PR to'siladi.
- [ ] Misollar va ochiq savollar story kod yozilishidan oldin sanab chiqiladi; yomon talab uchun test case yozib bo'lmasligi signal sifatida ishlatiladi.
- [ ] Test kodi production kodi bilan bir xil review standartida va test review checklist jamoada qo'llaniladi.
- [ ] Har bir test suite'ning, ayniqsa qamrovi katta testlarning egasi `CODEOWNERS` yoki test annotatsiyasida qayd etilgan.
- [ ] Buzilgan test uchun "kim tuzatadi" qoidasi yozilgan, qizil main branch eng yuqori prioritet deb qabul qilingan.
- [ ] Tanlangan jamoa modeli ongli ravishda tanlangan va madaniyat o'zgarishiga vaqt ajratilgan, tasodifiy shakllanmagan.
- [ ] QA soni kam bo'lsa, QA vaqti exploratory va qabul kriteriyalariga, regressiya esa avtomatlashtirishga yo'naltirilgan.
- [ ] Yangi test yozish narxi funksionallikni yozish narxidan oshmaydi: shablon, baza klass va test utility metodlar mavjud.
- [ ] Ish QA ga uzatilishidan oldin muallif golden path'ni o'zi ishlatib ko'radi va ma'lum edge case'larni sanab beradi; test rejasi implementatsiyadan oldin tuzilgan (159-160-bet).

## Manbalar

- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 14-bob ("UAT") - unit testni kodni yozgan odam yozgani uchun tushunmovchilik kodda ham, testda ham takrorlanishi ("working as implemented"), mijoz yoki uning vakili uchun ochiq API orqali o'tadigan foydalanuvchi yo'li testlari, hamda Google ning o'zi avtomatik UAT ni ko'p ishlatmasligi. Bu nashrning nusxasida barqaror bet raqami yo'q, shuning uchun bob va bo'lim nomi ko'rsatilgan
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 22-bob "Developer Testing" (499-504-bet) - developer bajaradigan test turlari va maxsus test xodimlari bajaradigan turlar ro'yxati; white-box va black-box farqi; test case'ni talab bosqichida rejalashtirish; developer testining cheklovlari (clean va dirty test nisbati, qamrovni ortiqcha baholash) va uning yolg'iz yetarli emasligi
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 22.3-bo'lim (512-515-bet) - ekvivalentlik sinflari, chegara tahlili va error guessing developer testining texnikalari sifatida
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 20-bob "The Software-Quality Landscape" (470-471-bet) - defekt topish darajalari jadvali (unit test modal 30%, integratsion 35%, formal code inspection 60%), hech bir usul yolg'iz 75% dan oshmaydi, inspeksiyada topilgan xatolarning faqat 20% i bir nechta tekshiruvchi tomonidan topilgan
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 21-bob "Collaborative Construction" (480-481-bet) - developer o'z ishidagi ko'r nuqtalarni ko'rmaydi; review test topa olmaydigan xatolarni topadi
- Titus Winters, Tom Manshreck, Hyrum Wright (tahr.), *Software Engineering at Google*, O'Reilly, 2020, 11-bob "Testing Overview" - muhandislar o'z kodi uchun testni o'zi yozadi; har o'zgarish code review dan o'tadi va unda kod ham test ham tekshiriladi, testsiz o'zgarishni to'sish o'rinli; test o'lchami va qamrovi, 80/15/5 taqsimoti va "ice cream cone" antipattern; hermetic test xossalari; buzilgan testni daqiqalar ichida tuzatish; Beyonce qoidasi; avtomatlashtirishning chegaralari; Test Certified va Testing on the Toilet; madaniyat o'zgarishi vaqt oladi
- Titus Winters, Tom Manshreck, Hyrum Wright (tahr.), *Software Engineering at Google*, O'Reilly, 2020, 12-bob "Unit Testing" - testni tekshirilayotgan xulq nomi bilan atash, testda control flow ishlatmaslik, aniq xato xabari, yomon testni merge qilishdan oldin tuzatish
- Titus Winters, Tom Manshreck, Hyrum Wright (tahr.), *Software Engineering at Google*, O'Reilly, 2020, 14-bob "Larger Testing" - qamrovi katta testda egalik muammosi va uning taqsimoti (loyiha lead, feature egasi, test engineer), `OWNERS` va per-test annotatsiya; Test Engineer roli test strategiyasini tuzadi; exploratory testing manual test shakli sifatida
- Titus Winters, Tom Manshreck, Hyrum Wright (tahr.), *Software Engineering at Google*, O'Reilly, 2020, 23-bob "Continuous Integration" - feedback aylanalarining eng tezdan eng sekinga qarab tartibi; o'chirilgan testlarni ro'yxatga olish va release'ni to'suvchi buglarni darhol tuzatish
- Gerard Meszaros, *xUnit Test Patterns*, Addison-Wesley, 2007, 5-bob "Principles of Test Automation" (39-48-bet) - Use the Front Door First, Communicate Intent, Keep Tests Independent, Verify One Condition per Test va Ensure Commensurate Effort and Responsibility principlari
- Gerard Meszaros, *xUnit Test Patterns*, Addison-Wesley, 2007, 17-bob "Project Smells" (263-265-bet) - "Developers Not Writing Tests" ning sabablari: vaqt yetishmasligi, testlash qiyin kod, noto'g'ri test avtomatlashtirish strategiyasi; jarayonni o'zlashtirgandan keyin test va kod avvalgi vaqt ichida yoziladi
- Gerard Meszaros, *xUnit Test Patterns*, Addison-Wesley, 2007, 1-bob (5-bet) va 4-bob (34-bet) - customer testlarni ishni boshlashdan oldin sanab chiqish mijoz nimani xohlayotganini aniqlaydi va muvaffaqiyat mezonini belgilaydi
- Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 11-bob (159-160-bet) - ishni QA ga "devor orqali" tashlash anti-patterni va uch bosqichli qaytarish aylanasi; QA ni rejalashtirishga jalb qilish, yonma-yon ishlash va QA ko'nikmasini o'zlashtirish; test rejasini implementatsiyadan oldin tuzish va test hamda monitoringni bahoning ichiga kiritish
- ESLATMA: 3.1 dagi rol nomlari, 3.2 dagi RACI matritsasi va release sign-off taqsimoti, 3.5 dagi sprint ichidagi tartib va sign-off hisoboti, 3.6 dagi review'ni kim qiladi taqsimoti, 3.7 dagi to'rt jamoa modeli klassifikatsiyasi, 3.8 dagi nightly rotatsiya va on-call taqsimoti, 3.9 dagi ish taqsimoti va 3.11 checklisti shu korpusning amaliy tavsiyasi, kitobdan olingan emas
- ESLATMA: 3.4 dagi "Three Amigos" uchrashuvi va "Example Mapping" karta formati nomlari korpusda mavjud kitoblarda yo'q; bo'limda faqat ularning ostidagi g'oya (misollarni kod yozilishidan oldin sanab chiqish) kitobga tayangan

---

[&larr; 2. Test piramidasi va test turlari xaritasi](02-test-piramidasi-va-test-turlari-xaritasi.md) · [Mundarija](README.md) · [4. Tester qanday ishlashi kerak: QA ish jarayoni &rarr;](04-testrovshik-qanday-ishlashi-kerak-qa-ish.md)
