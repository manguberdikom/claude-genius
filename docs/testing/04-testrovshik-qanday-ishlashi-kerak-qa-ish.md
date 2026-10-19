<!-- doc: testing | chapter: 4 | part:  -->

[Barcha hujjatlar](../../README.md) / [Testlash qo'llanmasi](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

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



Ko'pchilik arxitektorlar QA ishini "testni bosib ko'rish" deb tasavvur qiladi, lekin ishning katta qismi talablarni tahlil qilish, risklarni baholash va topilganlarni boshqalar tushunadigan tilda yozishga ketadi. Bu bob QA'ning kundalik ritmini, test dizayn texnikalarini, defekt bilan ishlash standartini va qo'lda testlashdan avtomatlashtirishga o'tish mezonlarini ko'rsatadi.

Bobni o'qishdan oldin bir ogohlantirish: QA jarayonining bosqichlari bo'yicha standart hujjatlar (ISTQB kabi) bu korpusda yo'q, shuning uchun bu yerda hech qanday standartga iqtibos qilinmaydi. Kitobdan tasdiqlangan qismlar manba bilan belgilangan; qolgani - korpusning o'z amaliy tartibi va shu holat bo'lim ichida aytiladi.

Arxitektor uchun bu bob ikki jihatdan muhim: birinchidan, siz QA'dan nima kutish kerakligini bilib olasiz; ikkinchidan, QA ishini imkonsiz qiladigan arxitektura qarorlarini (masalan trace ID yo'qligi yoki muhitlar nomosligi) oldindan ko'rasiz. Quyidagi barcha misollar bitta domenda - kredit limiti va buyurtma statuslari ustida - qurilgan, shuning uchun texnikalarni bir-biriga qiyoslash oson.

## 4.1 QA'ning ish oqimi va sprint ritmi

QA ishi chiziqli emas, aylanma: har bir talab bir necha bosqichdan o'tadi va har bosqichda orqaga qaytish ehtimoli bor. Quyidagi to'qqiz bosqich korpusning o'z tartibi; uning asosidagi bitta qoida esa kitobdan: test case'larni mahsulot bilan birga dizayn qilish kerak, chunki bu talab va dizayn xatolarini ochadi, ular esa kodlash xatolaridan qimmatroq turadi, va defektni iloji boricha erta topish arzonroq tushadi (*Code Complete*, 2-nashr, 22-bob, 503-bet).

**1. Talabni o'qish.** QA user story'ni, qabul kriteriyalarini, maketlarni va bog'liq API shartnomasini o'qiydi. Maqsad - "nima qurilayotganini" emas, "nima buzilishi mumkinligini" tushunish.

**2. Savol berish.** Noaniq joylar ro'yxatga olinadi va business analyst yoki product owner'ga beriladi. Bu bosqich eng arzon tuzatish nuqtasi: hali kod yozilmagan.

**3. Qabul kriteriyalarini aniqlashtirish.** Noaniq kriteriya testlanadigan shaklga qayta yoziladi. McConnell buni teskari tomondan ham tushuntiradi: test case'ni avval yozish talabdagi muammolarni tezroq ochadi, chunki yomon talab uchun test case yozish qiyin (o'sha joy, 504-bet).

**4. Test dizayni.** Texnikalar qo'llanadi (4.3-bo'lim), test case'lar va checklist'lar tayyorlanadi, risk yuqori bo'lgan joylarga ko'proq e'tibor beriladi. Test case'larni talab bosqichida yoki iloji boricha ertaroq, tekshirilishi kerak bo'lgan birlik yozilishidan oldin rejalashtirish tavsiya etiladi (o'sha joy, 503-bet).

**5. Testni bajarish.** Yangi funksionallik test qilinadi: avval smoke, keyin asosiy ssenariylar, keyin chegaralar va salbiy holatlar, oxirida exploratory session.

**6. Defekt ochish.** Topilgan muammo standart formatda yoziladi (4.6-bo'lim), log va trace ID ilova qilinadi.

**7. Retest.** Developer tuzatgandan keyin QA aynan o'sha qadamlarni qaytaradi va yondosh joylarni ham tekshiradi.

**8. Regressiya.** Risk asosida tanlangan regression suite ishga tushiriladi - qo'lda yoki avtomatik (4.8-bo'lim).

**9. Release holati bo'yicha hisobot.** QA nima test qilindi, nima qilinmadi va qanday ochiq risklar borligini yozma bayon qiladi. Bu hisobot "bug yo'q" degani emas; qarorni biznes tomoni qabul qiladi. Bu bosqich korpusning amaliy tartibi.

Bosqichlarni kun bo'yicha qattiq jadvalga bog'lash foydasiz, chunki amalda ular parallel ketadi: QA ertalab kechagi defektlarni retest qiladi, kunduzi yangi story'ni testlaydi, kun oxirida keyingi story uchun test dizayn qiladi.

Arxitektor uchun muhim xulosa: QA sprintning faqat oxirgi kunlarida ishga tushsa, feedback aylanasi ataylab uzaytirilgan bo'ladi. Kitob feedback aylanalarini eng tezdan eng sekinga qarab tartiblaydi: lokal edit-compile-debug; presubmit avtomatik test natijasi; submit'dan keyin topilgan integratsiya xatosi; staging muhitida QA tester topgan nomoslik; feature'ga ulangan ichki foydalanuvchilarning hisobotlari; tashqi foydalanuvchi yoki matbuot hisoboti (*Software Engineering at Google*, 23-bob "Continuous Integration"). Testlashni sprint oxiriga siqish bu ro'yxatda pastga tushish degani.

## 4.2 Talablarni testlash

Talabni testlash - kod yozilmasdan oldin bajariladigan eng foydali test turi. Uning asosi kitobda ikki joyda qo'yilgan. McConnell: har bir tegishli talab uchun test yozib, talab amalga oshirilganini tekshirish kerak, va test case'ni yozish qiyinligi talabning sifatsizligidan xabar beradi (*Code Complete*, 2-nashr, 22-bob, 503-504-bet). Meszaros: testlarni ishni boshlashdan oldin sanab chiqish, avtomatlashtiriladimi yoki yo'qmi, jamoaga mijoz nimani xohlayotganini tushuntiradi va muvaffaqiyat nima ekanini belgilaydi (*xUnit Test Patterns*, 1-bob, 5-bet).

McConnell yana bir amaliy ro'yxat beradi: talab bosqichida odatda chetda qoladigan narsalarni ataylab testlash kerak - xavfsizlik darajasi, saqlash, o'rnatish protsedurasi va tizim ishonchliligi (o'sha joy, 503-bet). QA savollar ro'yxatini shu to'rtta mavzudan boshlashi foydali.

Testlanmaydigan qabul kriteriyasining tipik belgilari: "tez ishlashi kerak", "qulay bo'lishi kerak", "to'g'ri hisoblanishi kerak", "kerakli hollarda xabar chiqsin". Bularda o'lchov, chegara va aktor yo'q. Quyidagi jadvaldagi qayta yozilgan variantlar korpusning misollari, o'lchangan ko'rsatkichlar emas.

| Yomon qabul kriteriyasi | Nega yomon | Qayta yozilgan (yaxshi) variant |
| --- | --- | --- |
| "Kredit limiti to'g'ri hisoblanishi kerak" | "To'g'ri" aniqlanmagan, formula yo'q | "Daromadi 10 000 000 so'mdan yuqori va kechikishi 0 bo'lgan mijoz uchun limit = daromad x 3, maksimum 50 000 000 so'm" |
| "Tizim tez javob bersin" | O'lchov va yuk darajasi yo'q | "`POST /api/credit-limit` uchun maqsadli p95 va yuk darajasi raqam bilan yoziladi" |
| "Noto'g'ri ma'lumotda xato ko'rsatilsin" | Qaysi xato, qanday kod, qaysi maydon - noaniq | "Daromad maydoni bo'sh bo'lsa, HTTP 400 va `{\"field\":\"income\",\"code\":\"REQUIRED\"}` qaytadi" |
| "Admin hamma narsani ko'ra oladi" | Rollar va resurslar aniqlanmagan | "ROLE_ADMIN barcha mijozlarning limit tarixini ko'radi; ROLE_AGENT faqat o'z filialidagi mijozlarni ko'radi; boshqasiga 403" |
| "Buyurtma bekor qilinsin" | Qaysi statuslardan bekor qilish mumkinligi aytilmagan | "NEW va PAID statuslarida bekor qilish mumkin; SHIPPED va DELIVERED'da 409 va `ORDER_NOT_CANCELLABLE` qaytadi" |

Yaxshi qabul kriteriyasining mezonlari: (1) aktor ko'rinadi, (2) shart o'lchanadi, (3) kutilgan natija bitta ma'noda tushuniladi, (4) xato yo'li ham yozilgan, (5) chegaralar raqam bilan berilgan. Bu beshlik korpusning checklisti; uni har story uchun tekshirib, yetishmaganini savol sifatida qaytarish kerak.

## 4.3 Test dizayn texnikalari

Test dizayn - cheksiz ko'p variantdan foydali bo'lganini tanlash. Nega tanlash kerakligini McConnell oddiy hisob bilan ko'rsatadi: hatto ism, manzil va telefon raqamini saqlaydigan dastur uchun ham barcha mumkin bo'lgan kirishlarni sinab ko'rish amalda imkonsiz, shuning uchun test bilan dasturning to'g'riligini isbotlab bo'lmaydi (*Code Complete*, 2-nashr, 22-bob, 505-bet). Minimal mezon shu kitobda berilgan: hech bo'lmaganda kodning har bir satri bir marta bajarilishi kerak (o'sha joy, 503-bet).

**Ekvivalentlik sinflari (equivalence partitioning).** Kirish qiymatlarini bir xil ishlov ko'radigan guruhlarga bo'lamiz va har guruhdan bittasini tekshiramiz. Kitobdagi ta'rif: yaxshi test case mumkin bo'lgan kirish ma'lumotining katta qismini qoplaydi, va ikki test case aynan bir xil xatolarni ochsa, ulardan faqat bittasi kerak; ekvivalentlik sinflari shu g'oyani rasmiylashtiradi va test case sonini kamaytiradi. Texnika ayniqsa kodga emas, spetsifikatsiyaga qarab ishlaganda yoki ma'lumot murakkab bo'lganda foydali (*Code Complete*, 22-bob, 512-bet). Kredit limiti misolida daromad maydoni: manfiy qiymatlar (xato), limit berilmaydigan oraliq, bazaviy limit oralig'i, oshirilgan limit oralig'i, raqam bo'lmagan matn (validatsiya xatosi).

**Chegara qiymatlari (boundary analysis).** Kitob bu yo'nalishni testlashning eng samarali sohalaridan biri deb ataydi va sababini aytadi: off-by-one xatolari, ya'ni `num` o'rniga `num - 1` yozish va `>` o'rniga `>=` yozish eng keng tarqalgan xatolardan. Shuning uchun har bir chegara uchun uchta holat tekshiriladi: chegaradan bir oz past, chegaraning o'zi va chegaradan bir oz yuqori - shu uchtasi bo'lmasa, odatiy xatolardan birortasi ochilmagan qoladi (*Code Complete*, 22-bob, 513-514-bet). `>= 10 000 000` sharti uchun bu 9 999 999, 10 000 000 va 10 000 001 qiymatlari bo'ladi.

Kitob shu yerda **birlashgan chegara (compound boundary)** holatini ham qo'shadi: chegara bir necha o'zgaruvchining kombinatsiyasidan kelib chiqqanda, masalan ikki qiymat ko'paytirilganda ikkisi ham katta musbat, katta manfiy yoki nol bo'lsa nima bo'ladi, yoki metodga uzatilgan barcha satrlar g'ayrioddiy uzun bo'lsa nima bo'ladi (o'sha joy, 514-bet). Kredit limitida bu "katta guruh mijozning hammasida yuqori daromad" va "guruhning hammasida nol daromad" holatlari.

**Yomon ma'lumot sinflari (classes of bad data).** Chegaradan tashqari, kitob yomon ma'lumotning beshta sinfini sanaydi: juda kam ma'lumot yoki umuman yo'q, juda ko'p ma'lumot, noto'g'ri turdagi ma'lumot, noto'g'ri o'lchamdagi ma'lumot va initsializatsiya qilinmagan ma'lumot (*Code Complete*, 22-bob, 514-515-bet). Shu beshlik API validatsiyasi uchun tayyor checklist beradi: bo'sh ro'yxat, juda katta ro'yxat, matn o'rniga raqam, chegaradan uzun satr, `null`.

**Yaxshi ma'lumot sinflari (classes of good data).** Nominal holatning o'zida ham xato bo'lishi mumkin, shuning uchun kitob to'rtta yaxshi ma'lumot sinfini tekshirishni tavsiya qiladi: nominal (kutilgan o'rta) qiymatlar, minimal normal konfiguratsiya, maksimal normal konfiguratsiya va eski ma'lumot bilan moslik (*Code Complete*, 22-bob, 515-516-bet). Oxirgisi migratsiyadan keyin eng ko'p unutiladigan tekshiruv.

**Xato taxmin qilish (error guessing).** Kitobda bu rasmiy bo'lmagan, lekin mo'tabar texnika sifatida beriladi: test case'larni dasturda xato bo'lishi mumkin bo'lgan joylar haqidagi taxminga qarab yaratish; taxminni intuitsiya yoki avvalgi tajribaga asoslash mumkin, va avval qilgan xatolaringiz yozib borilsa, taxmin aniqroq bo'ladi (*Code Complete*, 22-bob, 513-bet). Shu sababli ikkita yozuv foydali: loyihadagi xatolar ro'yxati (22.2-bo'limdagi tavsiya, 503-bet) va shaxsiy xatolar checklisti (22.7-bo'lim, 530-bet).

Quyidagi uchta texnika korpusning o'z amaliyoti: mavjud kitoblarda ular test dizayn texnikasi sifatida ta'riflanmagan, shuning uchun ularni kitob tavsiyasi deb o'qimang.

**Qaror jadvali (decision table).** Bir necha shart birgalikda natijani belgilaganda shartlar va kutilgan natijalarni jadvalga yozish, keyin ortiqcha qatorlarni birlashtirish. Kredit limiti qarori:

| # | Daromad chegaradan yuqori | Kechikish tarixi bor | KYC tasdiqlangan | Kutilgan natija |
| --- | --- | --- | --- | --- |
| R1 | Ha | Yo'q | Ha | Oshirilgan limit |
| R2 | Ha | Ha | Ha | Qo'lda ko'rib chiqish |
| R3 | Yo'q | Yo'q | Ha | Boshlang'ich limit |
| R4 | Yo'q | Ha | Ha | `DECLINED` |
| R5 | Ahamiyatsiz | Ahamiyatsiz | Yo'q | `KYC_REQUIRED`, limit 0 |

Jadvalning foydasi shu yerda ko'rinadi: KYC yo'q bo'lsa boshqa shartlar ahamiyatsiz, shuning uchun to'rtta qator bitta R5 ga birlashadi va ortiqcha test yozilmaydi. McConnell qaror jadvalini test texnikasi sifatida emas, kod texnikasi sifatida tavsiya qiladi: murakkab shartlar to'dasini qaror jadvali bilan almashtirish mumkin va keyin jadvalni kodni o'zgartirmasdan o'zgartirish mumkin (*Code Complete*, 19.1-bo'lim, 435-bet) - test uchun ham, kod uchun ham bitta jadval ishlatilishi shu sababli qulay.

**Holat o'tishlari (state transition).** Buyurtma statuslari: NEW, PAID, SHIPPED, DELIVERED, hamda NEW va PAID dan CANCELLED, DELIVERED dan RETURNED. Test dizayni uchta qismdan iborat: (a) ruxsat etilgan har bir o'tish ishlaydi, (b) ruxsat etilmagan o'tish rad etiladi (SHIPPED dan CANCELLED ga - 409), (c) bir xil o'tishning takrori idempotent. Arxitektor uchun signal: status o'tishlari kodda `if` lar to'dasiga sochilgan bo'lsa, QA ularni to'liq qamray olmaydi; o'tish qoidalarini bitta joyda saqlash yuqoridagi qaror jadvali tavsiyasining aynan davomi.

**CRUD matritsasi.** Har bir entity uchun to'rt amal va ruxsat yoki holat kesishmasi tekshiriladi. Bu "o'chirilgan yozuvni yangilash" yoki "boshqa filial mijozini ko'rish" kabi teshiklarni ochadi.

| Entity | Create | Read | Update | Delete |
| --- | --- | --- | --- | --- |
| CreditLimit | AGENT: ha; CUSTOMER: yo'q (403) | Egasi va AGENT: ha | Faqat ADMIN, audit log yoziladi | Soft delete; o'chirilgandan keyin Read 404 |
| Order | CUSTOMER: ha | Egasi: ha; boshqa: 403 | Faqat NEW statusida | DELIVERED'ni o'chirish taqiqlanadi (409) |

**Foydalanuvchi yo'li bo'yicha ssenariylar.** Mijoz ro'yxatdan o'tadi, KYC yuboradi, limit so'raydi, buyurtma yaratadi, to'laydi, yetkazib berishni kuzatadi. Bu yondashuvning asosi Meszaros da bor: customer testlar tizim real qanday ishlatilishini aks ettirishi kerak, va ular foydalanish shablonlarini qayd etib, qo'llab-quvvatlanishi kerak bo'lgan ssenariylarni sanab chiqishga yordam beradi (*xUnit Test Patterns*, 1-bob, 5-bet va 4-bob, 34-bet). Shu bilan birga kitob ogohlantiradi: uzun customer testlar Obscure Test bo'lib qoladi va yiqilganda muammo qayerda ekanini ko'rsatmaydi, shuning uchun ularni qisqa ushlash va UI ni chetlab o'tib servis darajasiga urish kerak (o'sha joy, 5-bet).

## 4.4 Test case yozish

Test case - boshqa odam hech nima so'ramasdan bajara oladigan yozma ko'rsatma. Quyidagi shablon korpusning o'z formati; uning maydonlari esa kitobdagi defekt yozuvi maydonlari bilan ataylab moslashtirilgan (4.6-bo'limga qarang).

```text
ID:            TC-CREDIT-014
Sarlavha:      Daromad chegarasida oshirilgan limit hisoblanadi
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

Yaxshi test case belgilari kitobdagi test yozish qoidalari bilan bir xil. Bitta maqsadni tekshiradi: Meszaros buni principle qilib qo'yadi - bitta testda bitta shart tekshiriladi, qamrovi katta customer testlarda bu doim amalga oshmasligi mumkin, lekin undan ongli ravishda chekinish kerak (*xUnit Test Patterns*, 5-bob, Verify One Condition per Test, 45-bet). Mustaqil bo'ladi va muhitni o'zi tayyorlaydi: test hermetic bo'lishi, ya'ni muhitini sozlash, bajarish va tozalash uchun kerakli hamma narsani o'zida saqlashi, tashqi muhit haqida iloji boricha kam narsa taxmin qilishi va umumiy bazaga tayanmasligi kerak (*Software Engineering at Google*, 11-bob "Properties Common to All Test Sizes"). Niyatni ko'rsatadi: test faqat tekshirilayotgan xulq uchun kerak bo'lgan ma'lumotni saqlashi va o'qilganda darhol tushunarli bo'lishi kerak, chunki testning testi yo'q (o'sha joy).

Yomon test case belgilari: "tizim to'g'ri ishlashini tekshir" kabi noaniq kutilgan natija; o'nlab qadamli zanjir; "oldingi test case'dan keyin bajariladi" degan bog'liqlik; UI piksel joylashuviga bog'langan qadamlar.

**Checklist va test case farqi.** Checklist - tekshirilishi kerak bo'lgan narsalar ro'yxati, qadamlarsiz. Checklist'ning o'zi kitob tavsiyasi: loyihada va avvalgi loyihalarda qilingan xatolar turlarining checklisti test dizaynida ishlatiladi (*Code Complete*, 2-nashr, 22-bob, 503-bet), shaxsiy darajada esa eng ko'p qilinadigan xatolar ro'yxatini yuritish tavsiya etiladi (o'sha bob, 530-bet). Batafsil test case esa boshqa odam bajaradigan yoki yozma iz talab qilinadigan joyda kerak. Amaliy qoida: yangi funksionallikni exploratory va checklist bilan tekshirib, barqarorlashgan qismini test case'ga aylantirib avtomatlashtirish - bu korpusning tartibi.

**Qachon avtomatlashtirish kerak.** Kitob regressiya uchun javobni ochiq beradi: regressiya testini boshqarishning yagona amaliy yo'li - uni avtomatlashtirish, chunki odam bir xil testni ko'p marta bajarib natijaga ko'nikib qoladi va xatoni sezmay qo'yadi; Beizer ning kuzatuvi bo'yicha qo'lda testlashdagi xato darajasi tekshirilayotgan koddagi bug darajasiga teng va qo'lda testlashda testlarning taxminan yarmigina to'g'ri bajariladi (*Code Complete*, 22-bob, 528-bet). Shu bobda avtomatlashtirishning foydalari ham sanalgan: avtomatik test qo'lda testdan kam xato qiladi; bir marta yozilgandan keyin butun loyiha davomida arzimas qo'shimcha kuch bilan ishlatiladi; har check-in dan keyin ishga tushirilishi mumkin; muammoni eng erta nuqtada ochadi; katta o'zgarishlar uchun xavfsizlik to'ri bo'ladi.

Qo'lda qolishi kerak bo'lgan ishlar ham kitobda aniq: avtomatlashtirish barcha test vazifalariga mos kelmaydi - qidiruv natijalari sifatini baholash odam hukmini talab qiladi, audio va video sifatining nozikliklarini avtomatik testga solish qiyin, murakkab xavfsizlik zaifliklarini izlashda esa odam avtomatik tizimdan yaxshi ishlaydi; odam zaiflikni topgandan keyin u avtomatik tizimga qo'shiladi va keyin uzluksiz ishlaydi (*Software Engineering at Google*, 11-bob "The Limits of Automated Testing").

## 4.5 Exploratory testing

Exploratory testing - "tasodifiy bosib ko'rish" emas. Kitobdagi ta'rif: bu tubdan ijodiy ish, unda odam tizimni buzilishi kerak bo'lgan jumboq deb qaraydi, kutilmagan qadamlar ketma-ketligini bajaradi yoki kutilmagan ma'lumot kiritadi; sessiya boshida qanday muammo topilishi ma'lum emas, muammolar kam qaraladigan kod yo'llarini va g'ayrioddiy javoblarni paypaslab asta-sekin ochiladi (*Software Engineering at Google*, 11-bob "The Limits of Automated Testing").

Boshqa bobda u test turi sifatida rasmiylashtirilgan: exploratory testing - qo'lda testlashning bir shakli, uning maqsadi ma'lum test oqimlarini qaytarib regressiya izlash emas, balki yangi foydalanuvchi ssenariylarini sinab shubhali xulqni izlash; o'qitilgan testerlar mahsulot bilan uning ochiq API'lari orqali ishlaydi va tizim ichidan yangi yo'llarni, kutilgan yoki intuitiv xulqdan chetga chiqishni hamda xavfsizlik zaifliklarini qidiradi. U yangi tizim uchun ham, allaqachon ishga tushgan tizim uchun ham foydali: turli yo'llardan yurish tizim qamrovini oshiradi va topilgan buglardan yangi avtomatik funksional testlar tug'iladi (*Software Engineering at Google*, 14-bob "Exploratory Testing").

Texnikaning ikki cheklovi ham shu joyda: qo'lda testlash chiziqlidan yaxshi masshtablanmaydi, ya'ni har test uchun odam vaqti ketadi; va exploratory'da topilgan har qanday defekt ancha tez-tez ishlashi mumkin bo'lgan avtomatik test bilan takrorlanishi kerak. Google da ishlatiladigan bir format - **bug bash**: muhandislar va mahsulotni biladigan boshqa xodimlar (menejerlar, product manager'lar, test engineer'lar) yig'ilish belgilaydi va o'sha sessiya davomida hamma mahsulotni qo'lda testlaydi; sessiya uchun alohida e'tibor sohalari yoki boshlang'ich nuqtalar e'lon qilinishi mumkin, maqsad esa shubhali xulqni va ochiq buglarni qayd etishga yetarli xilma-xillik yaratish (o'sha joy, "Bug Bashes").

Quyidagi tartib korpusning amaliy formati, kitobdan olingan emas.

**Charter.** Sessiya maqsadining bir-ikki gaplik ta'rifi. Shablon: "`<nimani>` ni `<qanday vositalar bilan>` o'rganib, `<qanday ma'lumotni>` topish". Misol: "Kredit limiti hisoblanishini chegara qiymatlari va KYC statuslari kombinatsiyasi bilan o'rganib, noto'g'ri limit beradigan holatlarni topish".

**Vaqt oynasi.** Sessiyaga oldindan belgilangan vaqt oynasi beriladi; vaqt tugasa sessiya tugaydi, topilgan narsa yoziladi va keyingi charter rejalashtiriladi. Buning foydasi diqqatni ushlab turish va ish hajmini rejalashtirish mumkin bo'lishi.

**E'tibor yo'nalishlari.** Google ning bug bash formatidagi "e'lon qilingan e'tibor sohalari" ni korpusda quyidagi ro'yxat bilan to'ldiramiz: pul oqimi (limit, buyurtma, to'lov, hisob-faktura); ataylab xato qilish (bo'sh maydon, noto'g'ri format, muddati o'tgan token, ikki marta to'lov, tarmoqni uzish); kam ishlatiladigan funksiyalar; rollar, sozlamalar va feature flag kombinatsiyalari. Ro'yxat korpusning o'z checklisti.

**Yozib borish.** Sessiya davomida vaqt, qilingan harakat, kuzatilgan natija va savol qayd etiladi. Sessiya oxiridagi hisobot uchta qismdan iborat: charter va sarflangan vaqt; topilgan defektlar va havolalari; yangi savollar va keyingi charter takliflari. Hisobotning asosiy qiymati - regression suite'ni boyitish: yuqorida keltirilgan kitob qoidasiga ko'ra exploratory'da topilgan har bir jiddiy defekt uchun avtomatik test yozilishi kerak.

## 4.6 Defekt hisoboti standarti

Bug report - developer uchun yozilgan texnik hujjat. Uning yagona vazifasi: muammoni minimal vaqtda qayta ishlab chiqarishga (reproduce) imkon berish.

Hisobot maydonlarining asosiy ro'yxati kitobda bor. McConnell defekt yozuvida saqlanishi kerak bo'lgan ma'lumotni sanaydi: administrativ tavsif (qachon xabar qilindi, kim xabar qildi, sarlavha yoki tavsif, build raqami, qachon tuzatildi), muammoning to'liq tavsifi, muammoni qaytarish qadamlari, taklif qilingan vaqtinchalik yechim, bog'liq defektlar, muammoning severity'si (masalan halokatli, bezovta qiluvchi yoki kosmetik), defektning kelib chiqishi (talab, dizayn, kodlash yoki testlash), kodlash defektining kichik turi, tuzatish tekkan klass va metodlar, defektni topishga va tuzatishga ketgan vaqt (*Code Complete*, 2-nashr, 22-bob, 529-bet).

Trace ID ni majburiy qilish talabi ham kitobga tayanadi: qamrovi katta testda stack trace foydasiz, chunki chaqiruv zanjiri bir necha process chegarasidan o'tadi, shuning uchun zanjir bo'ylab trace olish kerak; Google da Dapper bitta so'rov ID'sini RPC zanjiridagi barcha so'rovlar bilan bog'laydi va shu ID bo'yicha log'larni bir joyga yig'ish mumkin bo'ladi (*Software Engineering at Google*, 14-bob "Larger Testing"). Shu sababli so'rov trace ID qaytarmasa, bu arxitektura kamchiligi, QA ning e'tiborsizligi emas.

**Sarlavha formulasi:** `<qayerda> <qanday shartda> <nima noto'g'ri bo'ladi>`. Misol: "Kredit limiti: daromad aynan chegara qiymatida bo'lganda limit oshirilmaydi".

Yomon bug report misoli:

```text
Sarlavha: Limit ishlamaydi
Tavsif:   Limitni tekshirdim, natija xato. Tuzatinglar.
```

Bu hisobotda muhit, qadamlar, ma'lumot, kutilgan natija va log yo'q - developer QA bilan ikki marta yozishmasdan boshlay olmaydi.

Yaxshi bug report shabloni (maydonlar yuqoridagi kitob ro'yxatiga mos, formatlash korpusning o'zi):

```text
ID:        BUG-2291
Sarlavha:  Kredit limiti: income = 10 000 000 da limit oshirilmaydi

Muhit:
  Stend:      QA (qa-2.internal)
  Backend:    credit-service 1.14.3 (build #872, commit a3f91c2)
  Baza:       PostgreSQL 15, schema migration V41
  Mijoz:      REST API (curl), UI orqali ham takrorlanadi

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

Takrorlanish:  har safar takrorlanadi
Trace ID:      4b9f1ad2c77e4e1b9a1f0c3d8e2b5a66
Log parchasi:  CreditLimitCalculator.java:88 -> "tier resolved: TIER_1 for income=10000000"
Ilova:         curl-request.txt, response.json, screenshot-ui.png
Severity:      Major (QA taklifi)
Bog'liq talab: STORY-452
Bog'liq defekt: -
Vaqtinchalik yechim: daromadni chegaradan bir birlik yuqori kiritish
```

**Severity.** Kitobdagi misol shkala uch darajali: halokatli, bezovta qiluvchi, kosmetik (o'sha joy, 529-bet). Korpusda to'rt darajali shkala ishlatiladi (Blocker, Critical, Major, Minor) - bu korpusning tanlovi, kitobdan olingan emas; muhimi shkalaning o'zi emas, balki har severity darajasida ochiq turgan defektlar sonini kuzatish, chunki kitob shu ko'rsatkichni loyiha sog'lig'ini o'lchaydigan raqamlar qatorida sanaydi (o'sha bob, 530-bet).

**Priority.** Tuzatish navbatini severity'dan ajratish va uni kim belgilashi (QA yoki product owner) bo'yicha korpusda mavjud kitoblarda qoida yo'q, shuning uchun bu yerda severity va priority ni kesishtirgan matritsa berilmaydi. Kitobga tayanadigan yagona ajratish - release'ni to'sadigan va to'smaydigan defekt: Google da release'ni to'suvchi buglar darhol tuzatiladi, to'smaydiganlari ham tuzatiladi, lekin shoshilinch emas va prioritetlanadi (*Software Engineering at Google*, 23-bob "Continuous Integration"). Amalda ishlaydigan taqsimot - ta'sirni ko'rgan QA severity taklif qiladi, release navbatini biznes tomoni belgilaydi, arxitektor esa texnik risk (ma'lumot buzilishi, xavfsizlik, migratsiya) bo'yicha ovoz beradi; bu taqsimot korpusning amaliy tartibi.

## 4.7 Defekt hayot aylanishi va triage

Quyidagi holatlar jadvali korpusning o'z workflow'i: defekt hayot aylanishi bo'yicha standart hujjat korpusda yo'q, shuning uchun bu jadvalni standart deb o'qimang. Uni issue tracker'ingizdagi holatlar bilan moslashtirish kerak.

| Holat | Kim o'tkazadi | Ma'nosi va chiqish sharti |
| --- | --- | --- |
| **New** | QA | Yangi yozilgan defekt, hali ko'rib chiqilmagan |
| **Triage** | PO + Tech lead + QA | Tasdiqlanadi, ta'sir darajasi va egasi belgilanadi |
| **In Progress** | Developer | Tuzatish ustida ish ketmoqda |
| **Ready for Test** | Developer | Tuzatish qaysi build yoki muhitda ekani ko'rsatilgan |
| **Reopened** | QA | Retest o'tmadi - aynan qadamlar va yangi log bilan qaytariladi |
| **Closed** | QA | Retest o'tdi, kerak bo'lsa regression test qo'shildi |
| **Won't Fix** | PO (QA xabardor) | Ongli qaror: sabab va qabul qilingan risk yozma qayd etiladi |

Qo'shimcha holatlar amalda uchraydi: `Duplicate` (mavjud defektga havola bilan), `Cannot Reproduce` (QA qo'shimcha ma'lumot - trace ID, video - beradi va qayta ochadi), `Deferred` (keyingi release'ga ko'chirildi).

Triage'ning kitobga tayanadigan qismi ikkita. Birinchi - yo'naltirish: Google da keng tarqalgan usul bug "hotlist" lari bo'lib, ularni on-call yoki release muhandisi to'ldiradi va tegishli jamoaga triage qiladi; ro'yxat kuzatilib turilishi kerak, release'ni to'suvchi buglar darhol tuzatiladi, to'smaydiganlari ham prioritetlanadi, aks holda to'plam o'chirilgan eski testlarning o'sib boruvchi uyumiga aylanadi (*Software Engineering at Google*, 23-bob "Continuous Integration"). Ba'zi yirik mahsulotlarda bunday buglar avtomatik yaratiladi va joylashtiriladi (o'sha joy).

Ikkinchi - sababni guruhlab ko'rish. McConnell defekt yozuvlarining uzoq muddatli qiymatini shunday ta'riflaydi: vaqt o'tishi bilan testda topilgan defektlar yozuvi eng ko'p uchraydigan xato turlarini ko'rsatadi, va shu ma'lumot bilan o'qitishni tanlash, keyingi texnik review larni yo'naltirish va keyingi test case'larni loyihalash mumkin (*Code Complete*, 2-nashr, 22-bob, 502-bet). Arxitektorning triage'dagi roli ham aynan shu: bir xil sababdan kelayotgan defekt guruhlarini payqash va ularni bitta arxitektura ishiga aylantirish.

Triage uchrashuvining shakli (qisqa, muntazam, har defekt uchun to'rtta qaror: bu defektmi yoki yangi talabmi, ta'sir darajasi to'g'rimi, navbati qanday, egasi kim) va unda yechim o'ylamaslik qoidasi - korpusning amaliy tartibi.

## 4.8 Regressiya testlash

Regressiyaning ta'rifi kitobda: mahsulot biror joyda o'zgargandan keyin u avval o'tgan testlardan hali ham o'tayotganini, ya'ni dastur orqaga qadam tashlamaganini tekshirish (*Code Complete*, 2-nashr, 22-bob, 528-bet). Shu joyda ikki qoida bor. Birinchi - regressiya har safar aynan bir xil testlarni ishga tushirishi kerak; mahsulot yetilgani sayin yangi testlar qo'shiladi, lekin eskilari saqlanadi, aks holda yangi defekt kirmaganini bilishning yo'li yo'q. Ikkinchi - uni boshqarishning yagona amaliy yo'li avtomatlashtirish (o'sha joy).

Regressiyaning real samarasini ortiqcha baholamaslik kerak: defekt topish darajalari jadvalida regressiya testining modal ko'rsatkichi 25 foiz, ya'ni u xatolarni topish usuli sifatida unit testdan ham past turadi (*Code Complete*, 20-bob, 470-bet, Table 20-2). Regressiyaning vazifasi yangi xato topish emas, eski xulqning saqlanganini tasdiqlash.

**Smoke va regression farqi.** Smoke test ning ta'rifi ham kitobda: u tizimni boshdan oxirigacha bir marta ishlatib ko'radi, to'liq bo'lishi shart emas, lekin katta muammolarni ochishga qodir bo'lishi kerak, va agar build smoke'dan o'tsa, uni chuqurroq testlash uchun yetarlicha barqaror deb hisoblash mumkin bo'lishi kerak. Smoke test tizim bilan birga o'sadi: boshida u bir necha sekund ishlaydi, tizim o'sgani sayin o'n daqiqa, bir soat yoki undan ko'proq vaqt olishi mumkin; agar u yangilanmasa, kundalik build o'zini o'zi aldashga aylanadi (*Code Complete*, 29.4-bo'lim, 703-bet). Release oldidan tartib: deploy, keyin smoke, keyin risk asosida tanlangan regressiya, keyin yangi funksionallik testi, oxirida release holati bo'yicha hisobot.

**Risk asosida qisqartirish.** Hammasini har safar tekshirish imkonsiz, demak tanlash kerak. Tanlovning asosi kitobda strategiya darajasida qo'yilgan: dizaynning bir qismi test rejasini tuzish, test rejasining asosiy qismi esa qaysi test turlari va qancha kerakligining strategik bayoni; strategiya tizimning asosiy risk yo'nalishlarini aniqlaydi va har risk yo'nalishini yopadigan yondashuvni belgilaydi (*Software Engineering at Google*, 14-bob "Larger Testing"). Amalda bu quyidagicha bo'ladi: har modulga buzilish ehtimoli (o'zgarish hajmi, kod murakkabligi, tarixiy defektlar) va buzilish narxi (foydalanuvchi soni, pul, regulyativ ta'sir) beriladi; ikkisi yuqori bo'lgan modullar to'liq, biri yuqori bo'lganlar qisqartirilgan to'plam bilan, ikkisi past bo'lganlar faqat smoke bilan qoplanadi. Shu yondashuv release holati haqidagi hisobotda "nima test qilinmadi" savoliga aniq javob berish imkonini beradi. Modullarni baholash tartibi korpusning amaliy usuli.

## 4.9 Muhitlar (environments)

Muhitlar nomuvofiqligi QA ishini buzadigan birinchi sabablardan. Arxitektor har bir muhit uchun uchta narsani aniq belgilashi kerak: kim egasi, ma'lumot qayerdan keladi, qaysi versiyalar turadi.

Kitob muhit tanlashni system under test (SUT) tanlovi deb qo'yadi va uchta variantni qiyoslaydi. Production'da test qilish qo'shimcha muhit xarajati talab qilmaydi, lekin kod o'sha muhitga yetib kelmaguncha ishlamaydi, ya'ni bunday test kodning shu muhitga chiqishini to'sa olmaydi. Keyingi variant - katta umumiy staging muhiti; u ham testni kod tayyor bo'lgan vaqtga bog'laydi, muhitni "band qilish" tartibi esa muhandislar va servislar soni o'sgani sayin masshtablanmaydi, chunki konfliktlar ehtimoli tez oshadi. Uchinchi qadam - cloud'da izolyatsiyalangan yoki bitta mashinada hermetic SUT, bu konflikt va band qilish talabini yo'qotadi (*Software Engineering at Google*, 14-bob "Larger Testing"). Shuningdek, muhitlar bir-biridan ataylab farq qiladi: presubmit'da ko'rib chiqilmagan koddan qurilgan ilovaning real production backend bilan gaplashishi xavfli (xavfsizlik va kvota nuqtai nazaridan), staging uchun esa bu odatda qabul qilinadi (o'sha kitob, 23-bob "Continuous Integration").

Release nomzodi muhitlar ketma-ketligi orqali o'tkaziladi va har deployda testlanadi; bu ketma-ketlikda vaqtinchalik sandbox muhitlar ham, dev yoki staging kabi umumiy muhitlar ham bo'ladi, va umumiy muhitlarda release nomzodini qo'lda QA testidan o'tkazish keng tarqalgan (o'sha bob, release nomzodini testlash qismi). Production'dagi tekshiruvlar alohida turda ajratilgan: prober va canary tahlili, ularda SUT ham ma'lumot ham production, tekshirish esa assertion va metrikalar bo'yicha A/B taqqoslash (o'sha kitob, 14-bob).

Quyidagi jadval korpusning o'z modeli; egasi va ma'lumot ustunlari tavsiya, kitob talabi emas.

| Muhit | Egasi | QA nima qiladi | Ma'lumot holati | Versiyalar mosligi |
| --- | --- | --- | --- | --- |
| **local** | Developer | QA kirmaydi (ba'zan bug'ni takrorlash uchun) | Embedded yoki Testcontainers, har ishga tushishda toza | Faqat joriy branch |
| **dev** | Developer jamoasi | Smoke, erta fikr-mulohaza | Beqaror, tez-tez tozalanadi | Har commit'da o'zgaradi |
| **test / QA** | QA | Asosiy test ishi: yangi funksionallik, defekt tekshiruvi, exploratory | Boshqariladigan seed ma'lumot, QA tiklashi mumkin | Sprint build'lari, tashqi tizimlar stub yoki sandbox |
| **staging** | QA va release manager | Regressiya, integratsiya, E2E, release repetitsiyasi | Prod'ga o'xshash hajm, maskalangan ma'lumot | Prod konfiguratsiyasiga yaqin, tashqi tizimlarning sandbox'lari |
| **pre-prod** | Release manager / SRE | Oxirgi smoke, migratsiya repetitsiyasi, performance tekshiruvi | Prod nusxasi yoki unga juda yaqin | Prod bilan bir xil artefakt |
| **prod** | SRE / Operations | Prober va canary kuzatuvi, read-only smoke | Haqiqiy mijoz ma'lumoti - o'zgartirish taqiqlanadi | Release qilingan versiya |

QA uchun amaliy qoidalar: bug report'da muhit, build raqami va commit hash majburiy (kitobdagi defekt yozuvi maydonlari ham build raqamini talab qiladi, 4.6-bo'limga qarang); "faqat staging'da takrorlanadi" degan defektda birinchi gumon konfiguratsiya farqida; test muhitidagi ma'lumotni tiklashni QA o'zi bajara olishi kerak.

Arxitektor uchun ogohlantirish belgilari: QA muhiti tez-tez ishdan chiqadi; har muhitda schema versiyasi boshqa; test ma'lumotini tiklash qo'lda SQL yozishni talab qiladi; staging'da feature flag'lar prod'dan farq qiladi va buni hech kim bilmaydi. Oxirgisi kitobda nomlangan muammoga qo'shni: bir vaqtda bir necha versiya ishlab turganda yuzaga keladigan version skew, ya'ni tizimda kod, ma'lumot va konfiguratsiyaning o'zaro mos kelmaydigan versiyalari bo'lishi (*Software Engineering at Google*, 23-bob).

## 4.10 Qo'lda testlashdan avtomatlashtirishga o'tish mezonlari

Avtomatlashtirish - maqsad emas, vosita. Qarorni to'rt savol bilan qabul qilish mumkin: bu test necha marta takrorlanadi? natijasi deterministikmi? muvaffaqiyatsizlikda signal aniqmi? saqlash narxi qanchaga tushadi? Birinchi savolga kitob javob beradi: regressiyani boshqarishning yagona amaliy yo'li avtomatlashtirish, chunki qo'lda takrorlangan testda odam xatosi darajasi tekshirilayotgan koddagi bug darajasiga yaqin (*Code Complete*, 2-nashr, 22-bob, 528-bet).

Avtomatlashtirishga munosib ishlar: biznes qoidalari va hisob-kitoblar (ularda variant ko'p va qo'lda tekshirish qimmat); API shartnomalari va status kodlari; ruxsatlar matritsasi; status o'tishlari, ayniqsa taqiqlangan o'tishlar; har release'dagi smoke; tarixda bug chiqqan joylar uchun regression testlar; migratsiyadan keyingi yaxlitlik tekshiruvlari. Bu ro'yxat korpusning tanlovi, lekin uning ikki bandi kitobda to'g'ridan-to'g'ri aytilgan: smoke test har build'da ishlashi kerak (*Code Complete*, 29.4-bo'lim, 703-bet) va exploratory'da topilgan har qanday defekt avtomatik test bilan takrorlanishi kerak (*Software Engineering at Google*, 14-bob "Exploratory Testing").

Qo'lda qolishi kerak bo'lgan ishlar kitobda nomlangan: odam hukmini talab qiladigan sifat baholashlari (qidiruv natijalari sifati, audio va video sifati), murakkab xavfsizlik zaifliklarini izlash va exploratory testing'ning o'zi; avtomatlashtirish yaxshi tushunilgan xulqni qoplaydi va odamning qimmat, sifat jihatidan boy ishini eng ko'p qiymat beradigan joyga bo'shatadi (*Software Engineering at Google*, 11-bob "The Limits of Automated Testing"). Bunga korpus yana ikki bandni qo'shadi: shakli hali o'zgarib turgan yangi ekranlar va bir martalik migratsiya repetitsiyalari.

Amaliy ketma-ketlik: yangi funksionallik uchun qo'lda va exploratory test; barqarorlashgandan keyin eng qimmatli ssenariylarni avtomatlashtirish; topilgan har bir jiddiy bug uchun regression test yozish; qo'lda vaqtni yangi funksionallik va exploratory'ga qayta yo'naltirish.

Qo'lda regressiyaning narxi qanday ko'rinishini kitobdagi misol ko'rsatadi: YouTube ning monolit Python ilovasida har release uchun masofadagi QA jamoasi bajaradigan 50 soatlik qo'lda regressiya tsikli bor edi; release operatsion narxi shunchalik yuqori bo'lganda jamoa release'ni kechiktirib "yana bir oz test qilaylik" aylanasiga tushadi, natijada jarayon og'ir, xatoga moyil va sekin bo'lib qoladi (*Software Engineering at Google*, 24-bob "Continuous Delivery"). Agar QA vaqtining katta qismi takrorlanadigan qo'lda regressiyaga ketayotgan bo'lsa, bu release jarayonining va arxitekturaning muammosi, QA samaradorligining muammosi emas.

## 4.11 QA ishini o'lchash

Birinchi qoida kitobdan: testlashning o'zi sifatni yaxshilamaydi. Test natijasi sifatning ko'rsatkichi, lekin o'zi uni oshirmaydi; test hajmini oshirib sifatni yaxshilashga urinish o'zini tez-tez tarozida o'lchab vazn kamaytirishga urinish bilan bir xil - tarozi emas, ovqat o'zgarishi kerak (*Code Complete*, 2-nashr, 22-bob, 501-bet).

**O'lchash mumkin va foydali.** McConnell loyihani o'lchash uchun yig'iladigan raqamlarni sanaydi: har klass va metoddagi defektlar soni (o'lchamga normallashtirilgan holda), topilgan bitta defektga ketgan o'rtacha test vaqti, bitta test case'ga topilgan o'rtacha defekt soni, tuzatilgan bitta defektga ketgan o'rtacha dasturlash vaqti, test case'lar qoplagan kod foizi va har severity darajasida ochiq turgan defektlar soni (o'sha bob, 529-530-bet). Shu ro'yxatga defektning kelib chiqishi bo'yicha klassifikatsiya qo'shiladi: talab, dizayn, kodlash yoki testlash (o'sha joy, 529-bet) - aynan shu ko'rsatkich QA ishining ta'sirini eng yaxshi ko'rsatadi, chunki u defekt topish nuqtasining oqimda qanchalik erta ekanini o'lchaydi.

Flaky test ulushini o'lchash ham asoslangan: testlarning nondeterministik yiqilishi 1 foizga yaqinlashganda test to'plami qiymatini yo'qota boshlaydi; Google da bu daraja 0.15 foiz atrofida ushlab turiladi va buning uchun ataylab muhandislik vaqti sarflanadi (*Software Engineering at Google*, 11-bob "Flaky Tests Are Expensive").

**O'lchamaslik kerak.** Qamrov foizini yolg'iz o'zida maqsad qilish kitobda alohida ogohlantirish bilan berilgan: qamrov metrikasi o'zi maqsadga aylanadi, jamoa 80 foizni pol deb emas, shift deb qabul qiladi va shundan keyin o'zgarishlar aynan shu chegara bilan kela boshlaydi; bundan tashqari qamrov faqat satr bajarilganini o'lchaydi, natija to'g'riligini emas, shuning uchun u test to'plami haqida tanqidiy o'ylashning o'rnini bosmaydi (*Software Engineering at Google*, 11-bob "A Note on Code Coverage"). Shu kitobda qamrovni faqat kichik testlardan o'lchash tavsiya etiladi, aks holda katta testlar qamrovni shishiradi (o'sha joy).

Topilgan bug soni bo'yicha bonus yoki reyting berish korpusning tajribasida eng zararli metrika: QA ko'p mayda defekt yozadi, bitta katta muammoni bir nechta kichik defektga bo'ladi, risk tahliliga vaqt sarflamaydi va developer bilan munosabat raqobatga aylanadi. Bu kuzatish korpusning o'zidan, lekin uning mexanizmi yuqoridagi qamrov misoliga o'xshaydi: metrikani maqsad qilish xatti-harakatni metrikaga moslashtiradi. Shu sababli yozilgan test case soni va avtomatlashtirilgan test soni ham yolg'iz holda ma'nosiz.

**Nega bitta raqam yetmaydi.** Defekt topish usullarining hech biri yolg'iz o'zida yetarli emas: modal ko'rsatkichlar 75 foizdan oshmaydi va o'rtacha 40 foiz atrofida, eng keng tarqalgan usullar - unit va integratsion test - esa 30-35 foizda turadi; shuning uchun yuqori daraja faqat usullar kombinatsiyasidan chiqadi (*Code Complete*, 20-bob, 470-471-bet). Bu QA metrikasiga ham tegishli: bitta ko'rsatkich QA ishining qiymatini o'lchay olmaydi.

## 4.12 Arxitektor nazorat ro'yxati

- [ ] Har bir story'ning qabul kriteriyalari testlanadigan shaklda (aktor, o'lchanadigan shart, xato yo'li, raqamli chegara) yozilgan; test case yozib bo'lmaslik talabning sifatsizligi signali sifatida ishlatiladi
- [ ] Test dizayni kod yozilishidan oldin boshlanadi: test case'lar talab bosqichida rejalashtiriladi, QA sprint oxiriga siqilmaydi
- [ ] Har chegara uchun uchta holat (past, chegara, yuqori) tekshiriladi; yomon va yaxshi ma'lumot sinflari checklisti qo'llaniladi
- [ ] Loyihadagi xatolar turlari yozib boriladi va error guessing hamda keyingi test case'lar shu ro'yxatdan oziqlanadi
- [ ] Bug report shabloni jamoada yagona: muhit, build yoki commit, qadamlar, kutilgan va kuzatilgan natija, trace ID, log parchasi, vaqtinchalik yechim, bog'liq defektlar
- [ ] Har bir so'rov trace ID qaytaradi va log'larda uni izlash mumkin; chaqiruv zanjiri bo'ylab trace mavjud
- [ ] Release'ni to'sadigan va to'smaydigan defekt ajratilgan; to'suvchilar darhol tuzatiladi, qolganlari prioritetlanadi va ro'yxat kuzatilib turiladi
- [ ] Status o'tishlari va biznes qoidalari kodda bitta joyda jamlangan (state machine, qaror jadvali)
- [ ] Regressiya avtomatlashtirilgan va har safar bir xil testlarni ishlatadi; smoke test tizim bilan birga o'sadi va yangilanib turadi
- [ ] Muhitlar jadvali hujjatlashtirilgan: egasi, versiyalar mosligi, ma'lumot manbasi; presubmit va staging muhitlari farqi ongli tanlangan
- [ ] Exploratory'da topilgan har jiddiy defekt uchun avtomatik regression test yoziladi
- [ ] QA metrikalari defektning kelib chiqish fazasiga va ochiq defektlar holatiga asoslangan; qamrov foizi yoki topilgan bug soni bo'yicha hech qanday bonus yoki reyting yo'q

## Manbalar

- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 22-bob "Developer Testing" (499-504-bet) - developer va maxsus test xodimlari bajaradigan test turlari; test case'ni talab va dizayn bosqichida rejalashtirish; yomon talab uchun test case yozish qiyinligi; talabda odatda chetda qoladigan mavzular (xavfsizlik, saqlash, o'rnatish, ishonchlilik); loyihadagi xatolar checklisti; har satrni kamida bir marta bajarish minimal mezoni
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 22.1-bo'lim (501-502-bet) - testlashning o'zi sifatni oshirmaydi, test natijasi faqat ko'rsatkich; defekt yozuvlari vaqt o'tishi bilan eng ko'p uchraydigan xato turlarini ko'rsatadi va review hamda test case tanlovini yo'naltiradi
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 22.3-bo'lim (505-516-bet) - barcha kirishlarni sinab bo'lmasligi; ekvivalentlik sinflari; chegara tahlilining uchta holati va off-by-one sababi; birlashgan chegaralar; yomon ma'lumotning beshta sinfi; yaxshi ma'lumotning to'rtta sinfi; error guessing
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 22.6 va 22.7-bo'limlar (528-530-bet) - regressiya ta'rifi va uni avtomatlashtirish zarurati; qo'lda testlashdagi xato darajasi; avtomatlashtirishning foydalari; defekt yozuvining maydonlari va loyihani o'lchaydigan raqamlar ro'yxati; shaxsiy xatolar checklisti
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 20-bob (470-471-bet) - defekt topish darajalari jadvali: regressiya testi modal 25%, unit test 30%, integratsion test 35%; hech bir usul yolg'iz 75% dan oshmaydi, o'rtacha 40% atrofida
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 29.4-bo'lim (703-bet) - smoke test ta'rifi: tizimni boshdan oxir ishlatadi, to'liq emas, katta muammolarni ochadi; tizim bilan birga o'sadi va yangilanishi shart
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 19.1-bo'lim (435-bet) - murakkab shartlarni qaror jadvali bilan almashtirish va jadvalni kodni o'zgartirmasdan o'zgartirish
- Titus Winters, Tom Manshreck, Hyrum Wright (tahr.), *Software Engineering at Google*, O'Reilly, 2020, 11-bob "Testing Overview" - exploratory testing ijodiy ish sifatida; avtomatlashtirishning chegaralari (odam hukmi, audio va video sifati, xavfsizlik zaifliklari); hermetic test xossalari; flaky daraja 1% da qiymat yo'qoladi, Google da ~0.15%; qamrov foizi metrikaga aylanib polni shiftga o'zgartirishi va faqat satr bajarilganini o'lchashi
- Titus Winters, Tom Manshreck, Hyrum Wright (tahr.), *Software Engineering at Google*, O'Reilly, 2020, 14-bob "Larger Testing" - test strategiyasi risk yo'nalishlarini aniqlaydi; exploratory testing ta'rifi, cheklovlari va bug bash formati; SUT variantlari (production, umumiy staging, cloud yoki hermetic); prober va canary tahlili; Dapper va so'rov ID'si bo'yicha trace
- Titus Winters, Tom Manshreck, Hyrum Wright (tahr.), *Software Engineering at Google*, O'Reilly, 2020, 23-bob "Continuous Integration" - feedback aylanalarining tartibi; presubmit va staging muhitlari farqi hamda real backend bilan ishlash xavfi; release nomzodini muhitlar ketma-ketligidan o'tkazish va umumiy muhitlarda qo'lda QA testi; bug hotlist va release'ni to'suvchi buglarni darhol tuzatish; version skew
- Titus Winters, Tom Manshreck, Hyrum Wright (tahr.), *Software Engineering at Google*, O'Reilly, 2020, 24-bob "Continuous Delivery" - YouTube da har release uchun 50 soatlik qo'lda regressiya tsikli va uning release jarayoniga ta'siri
- Titus Winters, Tom Manshreck, Hyrum Wright (tahr.), *Software Engineering at Google*, O'Reilly, 2020, 12-bob "Unit Testing" - testda control flow ishlatmaslik va testning o'qilganda tushunarli bo'lishi
- Gerard Meszaros, *xUnit Test Patterns*, Addison-Wesley, 2007, 1-bob (5-bet) va 4-bob (34-bet) - testlarni ishni boshlashdan oldin sanab chiqish mijoz talabini aniqlaydi va muvaffaqiyat mezonini belgilaydi; customer test real foydalanishni aks ettirishi, lekin uzun bo'lmasligi kerak
- Gerard Meszaros, *xUnit Test Patterns*, Addison-Wesley, 2007, 5-bob (45-bet) - Verify One Condition per Test principli va undan ongli chekinish
- ESLATMA: 4.1 dagi to'qqiz bosqich va release hisoboti, 4.2 dagi besh mezon va qayta yozilgan kriteriya misollari, 4.3 dagi qaror jadvali, holat o'tishlari va CRUD matritsasi texnikalari, 4.4 dagi test case shabloni va avtomatlashtirish nomzodlari ro'yxati, 4.5 dagi charter, vaqt oynasi va e'tibor yo'nalishlari ro'yxati, 4.6 dagi to'rt darajali severity shkalasi va severity bilan priority ni kim belgilashi, 4.7 dagi defekt holatlari jadvali va triage uchrashuvi shakli, 4.8 dagi modullarni risk bo'yicha baholash tartibi, 4.9 dagi muhitlar jadvalining egasi va ma'lumot ustunlari, 4.10 dagi nomzodlar ro'yxati va 4.12 checklisti shu korpusning amaliy tavsiyasi, kitobdan olingan emas
- ESLATMA: QA jarayoni, test darajalari va defekt hayot aylanishi bo'yicha standart hujjatlar (ISTQB, ISO 29119 kabi) bu korpusda yo'q, shuning uchun bobda ularga iqtibos qilinmaydi va bo'limlardagi jarayon tartiblari standart emas

---

[&larr; 3. Kim nima yozadi: rollar va mas'uliyat](03-kim-nima-yozadi-rollar-va-masuliyat.md) · [Mundarija](README.md) · [5. Unit test: asoslar, qoidalar va JUnit 5 &rarr;](05-unit-test-asoslar-qoidalar-va-junit-5.md)
