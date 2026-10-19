<!-- doc: architect | chapter: 3 | part: I. Fikrlash va qarorlar -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 3. Qaror qabul qilish va uni hujjatlashtirish (Decisions and ADRs)

<details>
<summary>Bu bobdagi 27 bo'lim</summary>

- [3.1 ADR (Architecture Decision Record) tuzilishi: kontekst, qaror, oqibat, holat](#31-adr-architecture-decision-record-tuzilishi-kontekst-qaror-oqibat-holat)
- [3.2 Variantlarni taqqoslash: mezon jadvali va og'irlik berish](#32-variantlarni-taqqoslash-mezon-jadvali-va-ogirlik-berish)
- [3.3 Oxirgi mas'ul daqiqa (last responsible moment) tamoyili](#33-oxirgi-masul-daqiqa-last-responsible-moment-tamoyili)
- [3.4 Taxminlarni yozib qo'yish va keyin ularni tekshirish](#34-taxminlarni-yozib-qoyish-va-keyin-ularni-tekshirish)
- [3.5 Spike va prototip: qarorni ma'lumot bilan quvvatlash](#35-spike-va-prototip-qarorni-malumot-bilan-quvvatlash)
- [3.6 Jamoadagi kelishmovchilik va "rozi emasman, lekin bajaraman" qoidasi](#36-jamoadagi-kelishmovchilik-va-rozi-emasman-lekin-bajaraman-qoidasi)
- [3.7 Qaror oqibatini kuzatish: metrika va qayta ko'rish sanasi](#37-qaror-oqibatini-kuzatish-metrika-va-qayta-korish-sanasi)
- [3.8 ADR ni repoda saqlash, raqamlash va eskirganini belgilash](#38-adr-ni-repoda-saqlash-raqamlash-va-eskirganini-belgilash)
- [3.9 Yomon ADR belgilari: allaqachon qilingan ishni oqlash uchun yozilgan hujjat](#39-yomon-adr-belgilari-allaqachon-qilingan-ishni-oqlash-uchun-yozilgan-hujjat)
- [3.10 To'liq misol: PostgreSQL da qolish yoki alohida qidiruv tizimi qo'shish qarori](#310-toliq-misol-postgresql-da-qolish-yoki-alohida-qidiruv-tizimi-qoshish-qarori)
- [3.11 Nega eskiz kerak va nega ko'pchilik diagramma ishlamaydi](#311-nega-eskiz-kerak-va-nega-kopchilik-diagramma-ishlamaydi)
- [3.12 C4 modeli: to'rt daraja va har darajaning o'quvchisi](#312-c4-modeli-tort-daraja-va-har-darajaning-oquvchisi)
- [3.13 Kontekst diagrammasi: tizim chegarasi va tashqi aktyorlar](#313-kontekst-diagrammasi-tizim-chegarasi-va-tashqi-aktyorlar)
- [3.14 Konteyner diagrammasi: alohida deploy qilinadigan birliklar](#314-konteyner-diagrammasi-alohida-deploy-qilinadigan-birliklar)
- [3.15 Komponent diagrammasi va nega kod darajasiga tushmaslik kerak](#315-komponent-diagrammasi-va-nega-kod-darajasiga-tushmaslik-kerak)
- [3.16 "Kodda shunday qilasizmi" sinovi va model bilan kod orasidagi uzilish](#316-kodda-shunday-qilasizmi-sinovi-va-model-bilan-kod-orasidagi-uzilish)
- [3.17 Samarali eskiz: sarlavha, legend, javobgarlik va strelka](#317-samarali-eskiz-sarlavha-legend-javobgarlik-va-strelka)
- [3.18 Arxitektura ko'rinishi (view) va uni hujjatlashtirish qoidalari](#318-arxitektura-korinishi-view-va-uni-hujjatlashtirish-qoidalari)
- [3.19 Software guidebook: kod aytmagan narsani yozish](#319-software-guidebook-kod-aytmagan-narsani-yozish)
- [3.20 RFC: dizayn hujjatini fikr yig'ish uchun tarqatish](#320-rfc-dizayn-hujjatini-fikr-yigish-uchun-tarqatish)
- [3.21 Muhokama tiqilib qolganda qarorni ochish yo'llari](#321-muhokama-tiqilib-qolganda-qarorni-ochish-yollari)
- [3.22 Strategik maqsad, printsip va amaliyot: qarorni ramkaga solish](#322-strategik-maqsad-printsip-va-amaliyot-qarorni-ramkaga-solish)
- [3.23 Trade-off tahlilining ikki qadami: chalkash o'lchamlarni topish va birikmani modellash](#323-trade-off-tahlilining-ikki-qadami-chalkash-olchamlarni-topish-va-birikmani-modellash)
- [3.24 Model va kod sinxronligi: toqat qilinadigan nomuvofiqlik va strategiyalar](#324-model-va-kod-sinxronligi-toqat-qilinadigan-nomuvofiqlik-va-strategiyalar)
- [3.25 Texnika tartibi: arzondan boshlash, integratsiyani birinchi tekshirish va iteratsiya nol](#325-texnika-tartibi-arzondan-boshlash-integratsiyani-birinchi-tekshirish-va-iteratsiya-nol)
- [3.26 Qaror, printsip va istisno: governance mexanikasi](#326-qaror-printsip-va-istisno-governance-mexanikasi)
- [3.27 Amalda qo'llash](#327-amalda-qollash)

</details>



Arxitektorning asosiy mahsuloti kod emas, qaror. Kod qaytarilishi mumkin, qaror esa jamoaning keyingi ikki yilini belgilaydi. Qaror yozilmasa, u yo'q: olti oydan keyin "nega bu yerda Kafka turibdi" degan savolga javob beradigan hujjat kerak. Bu bob qarorni qanday pishitish, qanday yozib qo'yish va keyin uning natijasini qanday kuzatish haqida.

## 3.1 ADR (Architecture Decision Record) tuzilishi: kontekst, qaror, oqibat, holat

ADR bitta arxitektura qarorini tasvirlaydigan qisqa matn fayli, odatda bir-ikki bet. Uni Michael Nygard blog postida birinchi bo'lib targ'ib qilgan, keyin u Thoughtworks Technology Radar da "adopt" belgisini olgan. Fayl oddiy matn bo'lishi mumkin, lekin odatda AsciiDoc yoki Markdown da, yoki wiki sahifa shabloni sifatida yoziladi (Neal Ford va boshqalar, *Software Architecture: The Hard Parts*, 1-bob, 5-bet).

Nygard shaklida sarlavha va uchta bo'lim bor. Sarlavha qarorni nomlaydigan qisqa ot iborasi. Kontekst muammoni bir-ikki gapda bayon qiladi va muqobil yechimlarni sanaydi. Qaror qarorning o'zini aytadi va uni batafsil asoslaydi: asoslash aynan shu bo'limda turadi, alohida "sabab" bo'limi kerak emas. Oqibatlar qaror qo'llangandan keyingi natijalarni va ko'rib chiqilgan trade-off larni yozadi (*The Hard Parts*, 1-bob, 5-bet).

Holat (Status) maydoni Nygard shakliga *Fundamentals of Software Architecture* 19-bobida qo'shilgan va uning qiymatlaridan biri Proposed. Korpusdagi nusxada shu kitobning 19-bob tanasi yo'q, faqat ilovadagi o'z-o'zini tekshirish savollari bor, shuning uchun bu yerda maydonlarning to'liq ro'yxati emas, faqat savollar tasdiqlagani iqtibos qilinadi: 19-bob ADR ning besh asosiy bo'limini tasvirlaydi, asoslash Qaror bo'limida turadi, alohida Alternatives bo'limi bo'lmasa muqobillar Kontekst da sanaladi, va Proposed holatini qo'yishning uch mezoni bor (Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, ilova "Self-Assessment Questions", 19-bob savollari).

Eng ko'p xato qilinadigan joy kontekst. "Tizim tez ishlashi kerak" kontekst emas, chunki uni tekshirish mumkin emas: arxitektor "yuqori unumli" deb ayta olmaydi, u test yoki monitor o'lchay oladigan obyektiv qiymat berishi shart (*The Hard Parts*, 1-bob, 7-bet). Shunga ko'ra kontekst o'lchanadigan qiymat bilan yoziladi: qidiruvning hozirgi p95 si, maqsad qiymati, kunlik so'rov soni, baza hajmi. Kontekst o'qilganda qaror o'z-o'zidan kelib chiqishi kerak. Agar o'qiganingizda "unda nega boshqasini tanlamadilar" degan savol tug'ilsa, kontekst to'liq emas.

Oqibat bo'limi ADR ni boshqa hujjatdan ajratib turadi. *Fundamentals* ning birinchi qonuni shunday: arxitekturada hamma narsa trade-off, va arxitektor trade-off topilmadi deb o'ylasa, demak u hali topilmagan (1-bob, "Laws of Software Architecture" va Corollary 1). Rich Hickey ning shu kitobda keltirilgan gapi buni ochadi: dasturchi hamma narsaning foydasini biladi, trade-off ini bilmaydi, arxitektor ikkisini ham bilishi kerak (2-bob, "Analyzing Trade-Offs"). Shuning uchun "salbiy oqibat yo'q" degan ADR tahlil qilinmagan ADR. Qaytarish narxini ham shu yerga yozing: qaytarish kichik ishmi yoki migratsiyami.

Shu yerda hajm savoli turadi: har bir qaror uchun ADR yozilsa, ADR papkasi shovqinga aylanadi. Fairbanks chegarani qat'iy qo'yadi: developerlar tizim dizayni haqida har kuni qaror qabul qiladi va ularning ko'pchiligi tizim haqida deyarli hech qanday insight bermaydi, faqat bir nechtasi hal qiluvchi (pivotal) deb hisoblanishga arziydi, shuning uchun kam muhim qarorlarni ifodalab vaqt sarflashdan ehtiyot bo'lish kerak, bu yozma shaklda ham, og'zaki muhokamada ham bir xil (*Just Enough Software Architecture*, 12.5-bo'lim). Hal qiluvchi qarorning belgisi aniq: u shu nuqtadan keyingi qarorlarni shakllantiradi va dizayn fazosini toraytiradi, shuning uchun uning ortida batafsil asos turadi.

Qaror yozuvining minimal shakli esa ikki qismdan iborat, ya'ni qaror va asos. Fairbanks ning kutubxona tizimidagi misoli shu juftlikni ko'rsatadi: "tizim Java da quriladi, chunki jamoaning Java tajribasi bor, statik tipli yuqori darajadagi til biz qadrlaydigan modifiability ni yaxshilaydi, C ni rivojlantirish qiyinroq bo'lardi, uning unum foydasi bizda ustuvor emas, va ehtimoliy pointer buglari ishonchlilikka zarar beradi" (12.5-bo'lim). Qaror o'zi ham qiziqarli, lekin insight ni asos beradi: Java tanlanganini bilish "nega mening sevimli tilim emas" savoliga javob bermaydi, asos esa beradi, va o'quvchi tanlovga qo'shilmasa ham nega shunday qilinganini biladi.

Uchinchi va eng amaliy sabab mavjud tizimga tegishli. Fairbanks ikki marta, modellashtirish va kod kontekstida bir xil narsani aytadi: dizaynga yoki kodga qaragan boshqa odam qaysi qarorlar ixtiyoriy, qaysilari hal qiluvchi ekanini ayirib bera olmaydi; ixtiyoriy qarorni dizaynni buzmasdan o'zgartirish mumkin, hal qiluvchisini esa mumkin emas (12.5 va 9.5.5-bo'limlar). Uning kontekst diagrammasidagi misoli shuni ko'rsatadi: client-server bo'lish katta qaror bo'lishi mumkin, thin client ni thick client o'rniga tanlash esa bir nechta maqbul variantdan bittasi bo'lishi mumkin, va ikkisi diagrammada bir xil ko'rinadi. Shundan korpusdagi amaliy qoida chiqadi: ADR faqat hal qiluvchi qarorlar uchun ochiladi, qolgan dizayn esa [software guidebook](#319-software-guidebook-kod-aytmagan-narsani-yozish) da bayon qilinadi yoki umuman yozilmaydi; ADR ro'yxatining o'zi shu bilan "nimani o'zgartirish qimmat" degan xaritaga aylanadi.

Quyidagi shablon kitobdagi to'rt qismning (sarlavha, Kontekst, Qaror, Oqibatlar) ustiga shu korpusning qo'shimcha maydonlarini qo'yadi. Holat qiymatlaridan faqat "Taklif qilindi" (Proposed) kitobdan tasdiqlangan; qolgan qiymatlar va Sana, Qaror egasi, Qayta ko'rish sanasi, Taxminlar, Kuzatiladigan metrika maydonlari korpusning amaliy tanlovi.

```markdown
# ADR-0042: <Qaror sarlavhasi, qisqa ot iborasi>

- Holat: Taklif qilindi | Qabul qilindi | Rad etildi | Eskirdi | O'rnini bosdi
- Sana: 2026-03-11
- Qaror egasi: <ism>, ishtirokchilar: <jamoa>
- Qayta ko'rish sanasi: 2026-09-01
- Bog'liq ADR: ADR-0012 (o'rnini bosadi)

## Kontekst
Majburlovchi holat raqamlar bilan: latency, hajm, o'sish, muddat, cheklovlar.

## Qaror
Biz <X> ni tanlaymiz.

## Ko'rib chiqilgan variantlar
1. <Variant A>: rad etildi, sababi ...
2. <Variant B>: rad etildi, sababi ...

## Oqibatlar
- Ijobiy: ...
- Salbiy: ...
- Qaytarish narxi: <taxminan N kun / N oy>

## Taxminlar
- T1: <taxmin>. Tekshirish usuli: <o'lchov>. Muddat: <sana>.

## Kuzatiladigan metrika
- <metrika nomi>, hozirgi qiymat, maqsad qiymat, dashboard havolasi
```

| Masala | Oddiy yondashuv | Arxitektor yondashuvi |
|---|---|---|
| Qaror sababi | Chat xabarida qoladi | Repoda ADR fayli, kontekst raqamlari bilan |
| Variantlar | Bitta tanlangan variant aytiladi | Rad etilganlar va rad sababi yoziladi |
| Oqibat | Faqat foyda sanaladi | Narx, cheklov va qaytarish narxi yoziladi |
| Taxminlar | Boshda qoladi | Yozib qo'yiladi va tekshirish muddati beriladi |
| Qaror vaqti | Sprint boshida hammasi hal qilinadi | Oxirgi mas'ul daqiqaga qoldiriladi |
| Ma'lumot | "Men shunday o'ylayman" | Spike natijasi, EXPLAIN chiqishi, yuklama testi |
| Kelishmovchilik | Ovoz berish yoki eng baland ovoz | Yozma e'tiroz, qaror egasi, bajarish majburiyati |
| Natija | Deploy dan keyin unutiladi | Metrika va qayta ko'rish sanasi bilan kuzatiladi |
| Eskirgan qaror | Hujjat jimgina o'zgartiriladi | Yangi ADR yoziladi, eskisi "O'rnini bosdi" bo'ladi |

## 3.2 Variantlarni taqqoslash: mezon jadvali va og'irlik berish

Taqqoslashni jadvalga aylantirish muhokamani fikrdan mezonga ko'chiradi. Kitoblardagi trade-off jadvali ball yig'maydi: u yoki ustunlarni "afzallik" va "kamchilik" sifatida yozadi, yoki har mezonga sifat darajasini (juda past, past, o'rta, yuqori, juda yuqori) beradi va "qaysi biri muhimroq" savolini odamga qoldiradi. *Fundamentals of Software Architecture* 2-bobidagi topic va queue taqqoslashi shu shaklda va yakuniy javob "it depends" bo'lib qoladi; *The Hard Parts* 15-bobidagi jadvallar ham sifat darajalari bilan to'ldiriladi (402-403-betlar, Table 15-1 va Table 15-2).

Mezonlarni variantlarni ko'rib chiqishdan OLDIN yozing, aks holda mezonlar o'zingiz yoqtirgan variantga moslashib qoladi. *The Hard Parts* bu ro'yxatga MECE talabini qo'yadi: mutually exclusive, collectively exhaustive, ya'ni taqqoslanadigan narsalar bir-birining imkoniyatini qoplamasin va qaror maydonida ochiq qolgan variant qolmasin. Oddiy message queue ni butun enterprise service bus bilan taqqoslash noto'g'ri, chunki ular bir kategoriya emas; yuqori unumli navbatlarni baholaganda Kafka ni ro'yxatga kiritmaslik esa ro'yxatni to'liq qilmaydi (404-405-betlar).

Ikkita tuzoqdan saqlaning. Birinchisi kontekstdan chiqib ketish: yechimning ko'p yaxshi tomoni bo'lishi mumkin, lekin muvaffaqiyatga to'sqinlik qiladigan bitta imkoniyati yetishmasa, jadvaldagi umumiy ustunlik yolg'on ustunlik bo'lib chiqadi, shuning uchun mavjud barcha trade-off emas, to'g'ri to'plami tarozilanadi (405-407-betlar). Ikkinchisi dalilga ko'mib tashlash: arxitektor yiqqan texnik tafsilot nontexnik tarafga begona, shuning uchun tahlil bir necha kalit nuqtaga qisqartirib beriladi (410-bet).

Mezonni oldin yozish bitta qarorni himoya qiladi, lekin kundalik qarorlarni himoya qilmaydi. Fairbanks shu bo'shliqni "rasional arxitektura tanlovi" bilan to'ldiradi: dizayn trade-off demak, shuning uchun hamma yaxshi sifatni birga olish mumkin emas, va tanlov rasional bo'lishi, ya'ni trade-off laringiz sifat atributi ustuvorliklaringizga mos tushishi kerak (*Just Enough Software Architecture*, 5.4-bo'lim). Uning misoli qanday buzilishini ko'rsatadi: developer tizim talablari maintainability ni unumdan ustun qo'yganini biladi, lekin o'zining tajribasi yuqori unumli tizimlarda, shuning uchun baza sxemasini loyihalaganda so'rovlarni tezlashtirish uchun ayrim jadvallarni denormalizatsiya qiladi va maintenance ni qiyinlashtiradi. Fairbanks bu qarorning tabiatini ham aytadi: u o'ylangandan ko'ra instinktiv bo'lgan, va dizayn tizim ustuvorliklariga zid kelganini developer ongli ravishda sezadigan payt umuman bo'lmagan.

Shu sababli nom aniq: bu irrasional arxitektura tanlovi emas, umumiy ustuvorlik hisobiga qilingan lokal optimallashtirish. Boshqa kontekstda, ya'ni unum ustuvor bo'lgan tizimda xuddi shu dizayn maqtovga arzirdi. Amalda ikki belgini kuzatish kerak: ustuvorliklar "xira" bo'lsa va dizayn asoslari ochiq aytilmasa, irrasional tanlovlar ko'rinmaydi. Korpusdagi qarshi chora oddiy: ustuvorlik tartibini [sifat atributi ssenariysi](02-muammoni-tushunish-va-togri-savol-berish.md#218-sifat-atributi-ssenariysi-qa-scenario-va-architecture-driver) bo'limidagi shaklda yozib, review da bitta savolni berish, ya'ni bu o'zgarish birinchi o'rindagi atributga qarshi ishlayaptimi.

Jadval qarorni chiqarmaydi, u qaror qayerda tug'ilishini ko'rsatadi. Umumiy va abstrakt mulohaza arxitektorni faqat ma'lum joygacha olib boradi: *The Hard Parts* domendagi aniq ssenariylarni modellashtirishni tavsiya qiladi, ya'ni har variant uchun bir nechta real ish oqimini chizib, haqiqiy trade-off nimaga borib taqalishini ochish (408-409-betlar). Formal metodika ham bor, masalan ATAM (Architecture Tradeoff Analysis Method), lekin *The Hard Parts* uni arxitektorning kundalik muammolaridan uzoq deb baholaydi (26-bet).

| Variant | Qidiruv sifati | Operatsion murakkablik | Ma'lumot izchilligi | Jamoadagi tajriba |
|---|---|---|---|---|
| PostgreSQL FTS | o'rta | past | yuqori | yuqori |
| Alohida qidiruv tizimi | yuqori | yuqori | past | past |

Sarlavhadagi "og'irlik berish" haqida ogohlantirish: mezonlarga raqamli og'irlik qo'yib og'irlangan yig'indi hisoblash usuli bu bobda iqtibos qilingan kitoblarning birortasida yo'q. Ular jadvalni sifat darajasi bilan to'ldiradi va ustuvorlikni ochiq savol sifatida qoldiradi, chunki og'irlangan ball bitta raqam chiqarib, aynan muhokama qilinishi kerak bo'lgan ustuvorlik tortishuvini yashirib qo'yadi. Og'irlik qo'ymoqchi bo'lsangiz, uni qaror hujjatida alohida yozing va ballni qaror sifatida emas, muhokama kirish nuqtasi sifatida ishlatib qo'ying.

## 3.3 Oxirgi mas'ul daqiqa (last responsible moment) tamoyili

Kechiktirish g'oyasining kitobdagi asosi aniq. *Clean Code* 11-bobi shunday deydi: qarorni oxirgi imkon bo'lgan daqiqaga qoldirish dangasalik emas, u eng yaxshi ma'lumot bilan xabardor tanlov qilish imkonini beradi, chunki muddatidan oldin qilingan qaror bu kam ma'lumot bilan qilingan qaror (Robert C. Martin, *Clean Code*, 11-bob "Systems", "Optimize Decision Making", 167-168-betlar). *Clean Architecture* buni mexanizm bilan bog'laydi: siyosat (business rules) detallardan ajratilsa, detallar haqidagi qaror kechiktirilishi mumkin, va variantlar qancha uzoq ochiq qolsa, qarorni qilish paytida qo'lda shuncha ko'p ma'lumot va shuncha ko'p o'tkazilgan eksperiment bo'ladi (Robert C. Martin, *Clean Architecture*, 15-bob, "Keeping Options Open", 140-142-betlar).

Tamoyil bahona bo'lib ham ishlatiladi. Simon Brown treninglarda arxitektura diagrammasida texnologiya qarori ko'rsatilmaganini so'raganida eng ko'p eshitgan javoblaridan biri aynan "biz 'last responsible moment' tamoyiliga amal qilamiz" bo'lgan; uning xulosasi: "har qanday texnologiyada qurish mumkin" degani "qurish kerak" degani emas, nofunksional talab yoki cheklov bo'lsa texnologiya tanlovi implementation detail emas (Simon Brown, *Software Architecture for Developers*, 26-bob, 67-bet va 39-bob, 116-118-betlar).

Qaysi qarorni kechiktirish mumkinligini Booch ning ta'rifi hal qiladi: arxitektura bu tizimni shakllantiruvchi muhim qarorlar, muhimlik esa o'zgartirish narxi bilan o'lchanadi, ya'ni arxitektura qarori bu tushdan keyingi bitta refactoring bilan qaytarib bo'lmaydigan qaror (Brown, 5-bob, 12-13-betlar). *Clean Architecture* detal deb aniq nomlaganlari: baza turi, web server, REST, dependency injection framework (140-142-betlar). Teskari tarafda *The Hard Parts* ogohlantiradi: bazani servis chegarasi ichiga ko'chirgandan keyin tranzaksionallik birinchi darajali arxitektura masalasiga aylanadi (26-bet), ya'ni tranzaksiya chegarasi kechiktirib bo'lmaydigan qarorlar qatorida.

Amalda bu shunday ko'rinadi. Buyurtma servisida "qanday message broker" savolini birinchi sprintda hal qilish shart emas, agar hodisani chiqarish interfeys orqasiga yashirilgan va dizayn [patternlar hujjatidagi](../patterns/README.md) outbox pattern bilan qurilgan bo'lsa. Lekin "buyurtma identifikatori UUID bo'ladimi yoki bigint" savoli sxemaga, indeks hajmiga va tashqi integratsiyaga kirib ketadi: uni keyin o'zgartirish kichik refactoring emas, migratsiya bo'ladi. ADR da "nega hozir" degan bir qatorni yozib qo'ying: bu qaror vaqtini ham hujjatlashtiradi.

## 3.4 Taxminlarni yozib qo'yish va keyin ularni tekshirish

Har bir qaror ostida tekshirilmagan taxminlar yotadi: "kunlik buyurtma soni shu chegaradan oshmaydi", "hisobot kechikishi bir necha daqiqa bo'lishi mumkin", "ombor qoldig'i faqat bitta mintaqada o'zgaradi". Taxmin aslida risk, va George Fairbanks ning risk-driven modeli aynan shu ro'yxatni talab qiladi: model tinimsiz savol berishdan boshlanadi, "risklarim nima, ularni kamaytirishning eng yaxshi usuli qaysi, risk yetarlicha yumshatildimi va kodga qaytsam bo'ladimi" (George Fairbanks, *Just Enough Software Architecture*, 3.1). Fairbanks risk-driven ishlamayotganining birinchi belgisini ham aytadi: dasturchi o'z risklarini va ularga qarshi qo'llagan usullarini sanab bera olmasligi (3.2). Taxmin yozilmasa, u shunchaki haqiqatga aylanib qoladi va hech kim uni shubha ostiga olmaydi.

Har bir taxminga uch narsa biriktiring: qanday o'lchanadi, qachon tekshiriladi, buzilsa nima qilinadi. Uchinchisi eng qimmatli: "chegara oshsa partitsiyalashga o'tamiz" degan qator keyingi arxitektorga tayyor yo'l xaritasi beradi. O'lchov tarafini *Fundamentals* ning talabi bilan yozing: arxitektura xarakteristikasi obyektiv ta'riflanmasa, u haqida muhokama ham bo'lmaydi, chunki bitta tashkilot ichida ham bo'limlar "unum" so'zini boshqacha tushunadi (Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, 6-bob, "Measuring Architecture Characteristics").

Taxminni o'lchash ko'pincha bitta so'rov bilan hal bo'ladi. Ishlab chiqarish bazasida o'sish tezligini ko'rish uchun quyidagicha yozing, keyin natijani ADR ga nusxa qiling.

```sql
-- Taxmin T1: kunlik buyurtma soni 50 mingdan oshmaydi.
-- Oxirgi 90 kunning kunlik hajmi va o'sish trendi.
SELECT date_trunc('day', created_at)::date AS kun,
       count(*)                            AS buyurtma_soni,
       pg_size_pretty(sum(pg_column_size(o.*))) AS taxminiy_hajm
FROM orders o
WHERE created_at >= now() - interval '90 days'
GROUP BY 1
ORDER BY 1 DESC
LIMIT 10;

-- Jadval va indeks hajmi: qidiruv indeksi qancha joy egallaydi.
SELECT relname,
       pg_size_pretty(pg_relation_size(oid))       AS jadval,
       pg_size_pretty(pg_indexes_size(oid))        AS indekslar
FROM pg_class
WHERE relname IN ('orders', 'order_items')
  AND relkind = 'r';
```

Taxminni tekshirishni odamning esiga tayanib qoldirmang. Agar taxmin raqam bo'lsa, uni metrikaga aylantirib, chegara o'tilganda signal bering. Shunda taxmin o'z-o'zini tekshiradi.

## 3.5 Spike va prototip: qarorni ma'lumot bilan quvvatlash

Spike bu vaqti chegaralangan tadqiqot: maqsadi mahsulot emas, javob. Spike ni boshlashdan oldin uch narsani yozing: qaysi savolga javob izlayapmiz, qancha vaqt beramiz, qanday natija javob hisoblanadi. Vaqt chegarasi bo'lmasa spike loyihaga aylanadi.

Qachon to'xtash kerakligini Fairbanks aytadi: usulni qo'llash ko'pincha qog'ozda yoki doskada model qurish demakdir, model esa oraliq mahsulot, va arxitektura risklarni yopishga yaraydi degan ishonch paydo bo'lgan zahoti model ustida ishlashni to'xtatish mumkin. Uning asosiy printsipi ham shu: arxitektura ishiga ketadigan kuch nosozlik riski bilan mutanosib bo'lishi kerak (George Fairbanks, *Just Enough Software Architecture*, 3.6).

Spike natijasi ADR ga kirishi shart. *Documenting Software Architectures* ning qoidasi aniq: agar siz dizayn variantlarini baholash uchun texnik eksperiment, tadqiqot o'tkazgan yoki prototip qurgan bo'lsangiz, shu ishning xulosasi tanlangan variantning rationale si sifatida yozib qo'yilishi kerak (Paul Clements va boshqalar, *Documenting Software Architectures: Views and Beyond*, 2-nashr, Prolog, "Rule 5: Record Rationale", 44-bet). Simon Brown ham decision log da proof of concept, unum testi natijasi va mahsulot baholash hujjatlariga havola berishni aytadi (*Software Architecture for Developers*, 60-bob, 172-173-betlar).

Qidiruv qarori uchun spike shunday ko'rinadi: haqiqiy ma'lumotning nusxasini oling, indeks quring, o'nta tipik so'rovni o'lchang. Sun'iy ma'lumotda o'lchash behuda, chunki PostgreSQL planner statistikaga qarab boshqa plan tanlaydi.

```sql
-- Spike S-07: PostgreSQL full text search 300 ms ga sig'adimi.
-- 1. Generated ustun va GIN indeks.
ALTER TABLE orders
  ADD COLUMN search_doc tsvector
  GENERATED ALWAYS AS (
    to_tsvector('simple',
      coalesce(customer_name, '') || ' ' ||
      coalesce(order_number, '') || ' ' ||
      coalesce(notes, ''))
  ) STORED;

CREATE INDEX CONCURRENTLY idx_orders_search
  ON orders USING gin (search_doc);

-- 2. Haqiqiy so'rovni o'lchash. Buffer va vaqt bilan.
EXPLAIN (ANALYZE, BUFFERS)
SELECT id, order_number, created_at,
       ts_rank(search_doc, q) AS reyting
FROM orders, websearch_to_tsquery('simple', 'alisher toshkent') q
WHERE search_doc @@ q
ORDER BY reyting DESC, created_at DESC
LIMIT 20;
```

Natijani o'qiyotganda ikki raqamga qarang: Execution Time va shared read bloklari soni. Agar plan Bitmap Index Scan ko'rsatsa va bloklar soni cache ga sig'sa, bu yondashuv ishlaydi. Agar Seq Scan qolsa yoki ORDER BY katta natija to'plamini saralashga majbur qilsa, raqam yuklama ostida yomonlashadi.

## 3.6 Jamoadagi kelishmovchilik va "rozi emasman, lekin bajaraman" qoidasi

Texnik kelishmovchilikni yo'q qilish kerak emas, uni muhokama qilinadigan shaklga keltirish kerak. Fairbanks ning yechimi qaror qabul qilish jarayonini ochiq qo'yish: "A varianti yaxshi" va "B varianti yaxshi" degan ikki fikr orasida tanlash qiyin, lekin har biri sabab shabloni bilan yozilsa, A usability ga, B esa testability ga yordam berishi ko'rinadi va savol "kim yaxshi dizayner" dan "loyiha uchun qaysi sifat ustuvor" ga ko'chadi. Fairbanks buni muhokamadan ego ni olib tashlash deb ataydi (George Fairbanks, *Just Enough Software Architecture*, 5.4).

Shablonning o'zi ham shu bo'limda: "<x> ustuvor, shuning uchun <y> dizaynini tanladik va <z> kamchiligini qabul qildik" (5.4). Risk tarafida Fairbanks shuni ham ko'rsatadi: risk-driven model baholab ko'rish mumkin bo'lgan dalil beradi, ya'ni "A, B, C ni risk deb bildik, B birlamchi, uni kamaytirish uchun X va Y usullarini qo'lladik, natijani baholadik va yetarli deb topdik" shaklidagi argument. Boshqa dasturchi bunga qarshi shu shakldagi argument qo'yib, masalan D riskini qo'shishni taklif qilib, muhokamani injenerlik muhokamasiga aylantira oladi (3.1, "Logical rationale").

Shuning uchun muhokama davrida har kim e'tirozini yozma shaklda, ADR ga izoh sifatida qo'yishi kerak. Yozma e'tiroz og'zakisidan foydaliroq, chunki u shu shaklni tutishga majbur qiladi: "menga yoqmaydi" dan "bu yondashuvda hisobot so'rovi asosiy bazaga yuk beradi" ga o'tadi. Rad etilgan e'tiroz ADR ichida ko'rinadigan joyda qoladi, chunki *Documenting Software Architectures* rad etilgan muqobillarni va rad sababini yozib qo'yishni talab qiladi (Paul Clements va boshqalar, *Documenting Software Architectures: Views and Beyond*, 2-nashr, Prolog, "Rule 5: Record Rationale", 44-bet).

Kelishmovchilikni muhokama shakliga keltirmaslikning narxi aniq va u to'rt oqibatda ko'rinadi. Brown arxitektor bilan jamoa orasidagi uzilish natijasini sanaydi: jamoa arxitektorni hurmat qilmaydi, hatto qaror to'g'ri bo'lsa ham; jamoa motivatsiyani yo'qotadi; javobgarlik aniq emasligi uchun muhim qarorlar oradan tushib ketadi; va loyiha shundan zarar ko'radi (Simon Brown, *Software Architecture for Developers*, Leanpub, 16-bob, 43-bet). Uchinchi oqibat eng jim va eng qimmat, chunki u hech qanday tortishuv ko'rinishida chiqmaydi: hamma qarorni boshqa birov qabul qiladi deb o'ylaydi va qaror umuman qabul qilinmaydi. Shu sababli pastdagi "qaror egasi" mexanizmi kosmetik emas.

Shu bog'lanishning ikkinchi tomoni egalik haqida. Brown kollektiv egalikni arxitekturaga bog'laydi: hamma kodni o'zgartirishga haqli bo'lishi uchun hammada umumiy manzara haqida kamida asosiy tushuncha bo'lishi shart (18-bob, 47-bet). Ya'ni kollektiv egalik arxitektura hujjatining o'rnini bosmaydi, balki uni talab qiladi: umumiy manzara bo'lmasa, "hamma hamma joyga tegadi" qoidasi chegaralarni yemiradi. Amalda shart [qarorlarni jamoaga tarqatish](36-code-review-va-jamoada-texnik-yetakchilik.md#368-arxitektura-qarorlarini-jamoaga-tarqatish-hujjat-ichki-suhbat-namuna-kod) yo'li bilan bajariladi, va uning o'lchovi oddiy: jamoadan tasodifiy olingan odam tizim chegarasini va unda nima yashashini chiza oladimi.

Sarlavhadagi "rozi emasman, lekin bajaraman" qoidasi va har ADR ga bitta qaror egasini tayinlash shu korpusning amaliy tanlovi: yuqoridagi kitoblarda bu nom bilan qoida yo'q. Mazmuni oddiy: e'tiroz yozib qoldiriladi, lekin qaror chiqqandan keyin hamma bir xil qarorni bajaradi va unga qarshi ishlamaydi, e'tiroz esa qayta ko'rish sanasida metrika bilan birga qayta ochiladi.

## 3.7 Qaror oqibatini kuzatish: metrika va qayta ko'rish sanasi

Qarorni hujjatlash bilan uning to'g'ri qo'llanishini nazorat qilish ikki boshqa ish. *The Hard Parts* buni ADR bo'limidan keyin darhol aytadi: qarorni yozib qo'yish arxitektor uchun muhim, lekin qarorning to'g'ri ishlatilishini boshqarish alohida mavzu, va zamonaviy injenerlik amaliyoti bu boshqaruvning ko'p qismini architecture fitness function lar bilan avtomatlashtiradi (Neal Ford va boshqalar, *Software Architecture: The Hard Parts*, 1-bob, 5-6-betlar). Fitness function ning ta'rifi "biror arxitektura xarakteristikasining obyektiv butunlik bahosini beradigan har qanday mexanizm", va shu ta'rifning kalit sharti: arxitektor "yuqori unumli" deb ayta olmaydi, u test yoki monitor o'lchay oladigan obyektiv qiymat berishi shart (7-bet). Shuning uchun ADR da kamida bitta o'lchanadigan metrika bo'lishi kerak va u qarorning asosiy da'vosini o'lchasin: "qidiruv tezlashadi" degan qaror uchun qidiruv latency si o'lchanadi, umumiy CPU emas.

Metrikaning shaklini tanlashda *Fundamentals* ikki ogohlantirish beradi. Birinchisi: faqat o'rtachani o'lchash chegaradagi holatni yashiradi, so'rovlarning kichik ulushi bir necha barobar sekin ketsa u o'rtachada ko'rinmaydi, shuning uchun outlier ni ushlaydigan o'lchov ham kerak. Ikkinchisi: yetuk jamoalar maqsad qiymatni o'zboshimchalik bilan tanlamaydi, uni statistik tahlilga tayantiradi va real metrika modeldan chiqib ketsa signal beradi (Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, 6-bob, "Operational Measures" va "The Many Flavors of Performance").

Metrikani kod yozilgan paytda joylashtiring, keyin emas. Micrometer bilan bu bir necha qatorlik ish va natijasi ADR ning haqiqiy nazoratchisi bo'ladi.

```java
@Service
public class OrderSearchService {
    private final Timer qidiruvVaqti;
    private final Counter boshNatija;
    private final OrderSearchRepository repository;

    public OrderSearchService(MeterRegistry registry, OrderSearchRepository repository) {
        this.repository = repository;
        // ADR-0042 metrikasi: p95 maqsad 300 ms.
        this.qidiruvVaqti = Timer.builder("order.search.duration")
                .description("Buyurtma qidiruvi davomiyligi")
                .publishPercentiles(0.5, 0.95, 0.99)
                .tag("engine", "postgres_fts")
                .register(registry);
        this.boshNatija = Counter.builder("order.search.empty")
                .register(registry);
    }

    public List<OrderView> search(String query, Pageable page) {
        return qidiruvVaqti.record(() -> {
            List<OrderView> natija = repository.search(query, page);
            if (natija.isEmpty()) {
                boshNatija.increment();  // sifat signali, tezlik emas
            }
            return natija;
        });
    }
}
```

Metrikani fitness function ga aylantirishning to'rt qoidasi bor va ularni *The Hard Parts* 1-bobi beradi.

- **Fitness function mi yoki unit test mi.** Fitness function arxitektura xossasini tekshiradi, unit test esa domen mezonini. Ajratishning savoli bitta: bu testni bajarish uchun domen bilimi kerakmi. Javob "ha" bo'lsa unit, funksional yoki qabul testi kerak, "yo'q" bo'lsa fitness function (1-bob, 8-bet). Elasticity, ya'ni foydalanuvchi sonining keskin o'sishini ko'tarish, domen bilimini talab qilmaydi, shuning uchun u fitness function doirasida; manzil maydonining to'g'ri qismlarini tekshirish esa oddiy test.
- **Atomic va holistic qamrov.** Atomic fitness function bitta arxitektura xossasini alohida tekshiradi, masalan kod bazasida komponent sikllari borligini. Holistic esa bir nechta o'zaro bog'liq xossani birga tekshiradi, chunki atributlar bir-biri bilan sinergiyada bo'ladi: xavfsizlikni yaxshilash unumga tegishi ehtimoli katta, scalability va elasticity esa ba'zan bir-biriga qarshi ishlaydi, ya'ni ko'p sonli konkurent foydalanuvchini ko'tarish keskin burstni ko'tarishni qiyinlashtiradi (1-bob, 7-bet).
- **Natija statik bo'lishi shart emas.** Obyektiv bo'lish statik bo'lishni anglatmaydi. Ayrim fitness function lar kontekstdan mustaqil qiymat qaytaradi, masalan true/false yoki unum chegarasi; dynamic deb atalgan boshqalari esa kontekstga qarab qiymat qaytaradi. Kitobning misoli: scalability ni o'lchaganda konkurent foydalanuvchi soni ham, har bir foydalanuvchi uchun unum ham o'lchanadi va arxitektor tizimni shunday loyihalaydiki, foydalanuvchi soni oshganda har biriga tegadigan unum bir oz pasayadi, lekin keskin qulamaydi; shuning uchun unum fitness function i konkurent foydalanuvchi sonini hisobga oladi (1-bob, 11-bet).
- **Ayrimlari qo'lda bajariladi.** Ko'pchilik fitness function avtomatlashtirilishi va uzluksiz ishlashi kerak, lekin ba'zilari majburan qo'lda bo'ladi: huquqiy jihatdan nozik ma'lumotli tizimda yurist kritik qismlardagi o'zgarishni qonuniylik uchun ko'rib chiqishi kerak va buni avtomatlashtirib bo'lmaydi. Ko'pchilik deployment pipeline qo'lda bosqichni qo'llab-quvvatlaydi, shuning uchun qo'lda tekshiruv ham pipeline ichiga joylashtiriladi va imkon qadar tez-tez bajariladi, chunki bajarilmaydigan tekshiruv hech narsani tekshirmaydi (1-bob, 11-bet).

Uzluksizlikning tashkiliy qiymatini kitob bitta ssenariy bilan ko'rsatadi va u korpusdagi [standart o'rnatish](36-code-review-va-jamoada-texnik-yetakchilik.md#369-standart-ornatish-linter-formatlash-archunit-qoidalari-shablon-loyiha) qoidasining xavfsizlik tomoni. Kompaniyada ishlatilayotgan framework yoki kutubxonada zero-day exploit topilsa, odatda xavfsizlik mutaxassislari loyihalarni qo'lda tekshirib yuradi va bu jarayon xatoga moyil. *The Hard Parts* Equifax nosozligini keltiradi: Struts dagi zaiflik uchun patch 2017 yil 7 martda chiqarildi, Homeland Security kompaniyalarni ertasi kuni ogohlantirdi, 15 martdagi skanerlash esa barcha ta'sirlangan tizimlarni topmadi, va kritik patch ko'p eski tizimga faqat 29 iyulda, hujum xatti-harakati aniqlangandan keyin qo'llanildi (1-bob, 11-12-betlar). Kitobning muqobil dunyosi oddiy: har bir loyiha deployment pipeline ishlatadi va xavfsizlik jamoasining har bir pipeline da o'z "sloti" bo'ladi; odatdagi vaqtda u parolni bazada saqlashni taqiqlash kabi oddiy tekshiruvlarni bajaradi, zero-day chiqqanda esa bir xil mexanizm bilan barcha loyihaga framework va versiya raqamini tekshiradigan test qo'yiladi, xavfli versiya topilsa build yiqiladi va xavfsizlik jamoasi xabar oladi.

Natijasiz qidiruvlar ulushi muhim, chunki tezlik yaxshilanib, sifat yomonlashishi mumkin. Qayta ko'rish sanasi kelganda uchta javobdan birini yozasiz: qaror o'zini oqladi, qaror qisman ishladi va tuzatish kerak, yoki qaror xato bo'ldi va yangi ADR yoziladi. Uchinchi javob eng qimmatli, lekin uni faqat sana va metrika bo'lgan jamoa chiqara oladi.

## 3.8 ADR ni repoda saqlash, raqamlash va eskirganini belgilash

Saqlash joyi haqida kitob ikki variantni teng qo'yadi: ADR matn fayli (AsciiDoc yoki Markdown) yoki wiki sahifa shabloni bo'lishi mumkin (Neal Ford va boshqalar, *Software Architecture: The Hard Parts*, 1-bob, 5-bet). Shu korpus kod bilan bir repoda, `docs/adr/` papkasida saqlashni tanlaydi, chunki pull request ichidagi fayl review ga tushadi. Nom shabloni `NNNN-qisqa-sarlavha.md`, raqam to'rt xonali va ketma-ket; raqam qayta ishlatilmaydi, hatto ADR rad etilgan bo'lsa ham. Nom shabloni va raqamlash qoidasi korpusning tanlovi, kitobda bunday shablon yo'q.

Qaysi joyni tanlasangiz ham, asosiy shart hujjatning yangiligi. *Documenting Software Architectures* buni alohida qoida qilib qo'yadi: to'liq bo'lmagan yoki eskirgan hujjat haqiqatni aks ettirmaydi va ishlatilmaydi, yangilanib turgan hujjat esa ishlatiladi, chunki tizim haqidagi savolga eng tez javob shu hujjatdan topiladi (Paul Clements va boshqalar, *Documenting Software Architectures: Views and Beyond*, 2-nashr, Prolog, "Rule 6: Keep Documentation Current but Not Too Current", 44-45-betlar).

Eskirgan ADR o'chirilmaydi va tahrirlanmaydi. Uning holati `Eskirdi` yoki `O'rnini bosdi: ADR-0057` ga o'zgaradi va shu bitta qator qo'shiladi. Mazmuni esa o'sha paytdagi haqiqat sifatida qoladi. Buning sababi "Rule 5" da yozilgan: qaror keyinchalik shubha ostiga olinganda yoki o'zgartirish bosimi paydo bo'lganda siz o'sha dalillarni yana boshidan ko'rib chiqasiz va nega boshqa yo'ldan bormaganingizni o'ylab qolasiz, sababni yozib qo'yish esa uzoq muddatda katta vaqt tejaydi (44-bet).

```bash
#!/usr/bin/env bash
# docs/adr/new.sh: keyingi ADR raqamini topib, shablondan fayl yaratadi.
set -euo pipefail

DIR="$(dirname "$0")"
LAST=$(ls "$DIR" | grep -E '^[0-9]{4}-' | sort | tail -n 1 | cut -c1-4)
NEXT=$(printf "%04d" $((10#${LAST:-0} + 1)))
SLUG=$(echo "$*" | tr '[:upper:] ' '[:lower:]-' | tr -cd 'a-z0-9-')

cp "$DIR/template.md" "$DIR/$NEXT-$SLUG.md"
sed -i "s/ADR-0000/ADR-$NEXT/; s/<SANA>/$(date +%F)/" "$DIR/$NEXT-$SLUG.md"
echo "Yaratildi: $DIR/$NEXT-$SLUG.md"
```

CI da ikkita oddiy tekshiruv katta foyda beradi: har bir ADR da `Holat` qatori borligi va qayta ko'rish sanasi o'tgan ADR lar ro'yxatini chiqarish.

```yaml
# .github/workflows/adr-check.yml dagi qadamlar
- name: ADR holat qatori bormi
  run: |
    for f in docs/adr/[0-9]*.md; do
      grep -q '^- Holat:' "$f" || { echo "Holat yo'q: $f"; exit 1; }
    done

- name: Qayta ko'rish sanasi o'tgan ADR lar
  run: |
    BUGUN=$(date +%F)
    grep -H '^- Qayta ko.rish sanasi:' docs/adr/[0-9]*.md \
      | awk -v t="$BUGUN" -F': ' '$2 != "" && $2 < t {print "Muddati o-tdi: " $0}'
```

## 3.9 Yomon ADR belgilari: allaqachon qilingan ishni oqlash uchun yozilgan hujjat

Eng keng tarqalgan nosog'lom ADR bu keyin yozilgan oqlash hujjati. Uni tanib olish oson: unda bitta variant bor, salbiy oqibatlar bo'limi bo'sh yoki "jiddiy salbiy oqibat yo'q" deb yozilgan, va kontekstda o'lchanadigan qiymat yo'q. Uchta belgining uchtasi ham kitobdagi talabni buzadi: muqobillar Kontekst da sanalishi kerak (*The Hard Parts*, 1-bob, 5-bet), rad etilgan muhim muqobillar va rad sababi yozilishi kerak (*Documenting Software Architectures*, 2-nashr, Prolog, "Rule 5", 44-bet), trade-off topilmagan bo'lsa demak u hali topilmagan (*Fundamentals of Software Architecture*, 1-bob, Corollary 1). Agar qaror chindan ham allaqachon qilingan bo'lsa, buni ochiq yozing: "bu qaror avval amalga oshirilgan, ADR retrospektiv yozilmoqda". Shu bir gap hujjatning ishonchini saqlaydi.

*Fundamentals* 19-bobi arxitektura qarorining alohida antipatternlarini nomlaydi, ular ichida "covering your assets" va "email-driven architecture" bor. Korpusdagi nusxada 19-bobning tanasi yo'q, faqat ilovadagi savollar bu nomlarni tasdiqlaydi, shuning uchun bu yerda ularning tavsifi berilmaydi: nomlari sanaladi va tavsif uchun asl 19-bobga murojaat qilish kerak (*Fundamentals of Software Architecture*, ilova "Self-Assessment Questions", 19-bob savollari).

| Tuzoq | Nega xavfli | Yechim |
|---|---|---|
| Bitta variantli ADR | Muqobil ko'rib chiqilmaganini yashiradi | Kamida ikki rad etilgan variant va rad sababi |
| Salbiy oqibatsiz ADR | Narx yashiringan, keyin kutilmagan bo'lib chiqadi | "Salbiy" bo'limi bo'sh ADR review dan o'tmaydi |
| O'lchovsiz kontekst | Qaror did asosida qilinganini bildiradi | Test yoki monitor o'lchay oladigan qiymat yoziladi (*The Hard Parts*, 7-bet) |
| Eski ADR ni tahrirlash | Tarix yo'qoladi, sabab izi uziladi | Yangi ADR, eskisiga "O'rnini bosdi" |
| Uzun ADR | Hech kim o'qimaydi | Odatdagi ADR bir-ikki bet (*The Hard Parts*, 5-bet), chuqur tahlil ilova havolasida |
| Sanasiz qayta ko'rish | Qaror hech qachon tekshirilmaydi | Majburiy maydon, CI tekshiradi (korpus tavsiyasi) |
| Egasi yo'q ADR | Javobgarlik tarqaladi | Bitta ism, jamoa nomi yetarli emas (korpus tavsiyasi) |
| Spike natijasiz qaror | Taxmin ma'lumot o'rniga qo'yiladi | Eksperiment va prototip xulosasi rationale sifatida yoziladi (*Documenting Software Architectures*, 44-bet) |

## 3.10 To'liq misol: PostgreSQL da qolish yoki alohida qidiruv tizimi qo'shish qarori

Bu bo'lim shartli misol: quyidagi barcha raqam o'lchanmagan taxmin, ular ADR ning shaklini ko'rsatish uchun qo'yilgan, biror kitob yoki o'lchovdan olingan emas. Holat shunday. Buyurtma qidiruvi admin panelda ishlatiladi, kunlik taxminan 40 ming so'rov, `orders` jadvalida 42 million qator, jadval hajmi taxminan 180 GB. Hozirgi qidiruv `ILIKE '%...%'` bilan qurilgan va p95 da 1.8 soniya beradi. Maqsad 300 ms. Jamoa uch kishi, alohida infratuzilma injeneri yo'q. Spike S-07 natijasi: generated `tsvector` ustun va GIN indeks bilan p95 taxminan 90 ms, indeks hajmi taxminan 11 GB, yozish tezligi sezilarli darajada pasaydi.

```markdown
# ADR-0042: Buyurtma qidiruvini PostgreSQL FTS da qoldirish

- Holat: Qabul qilindi
- Sana: 2026-03-11
- Qaror egasi: A. Qoraev. Ishtirokchilar: order-platform jamoasi
- Qayta ko'rish sanasi: 2026-09-01

## Kontekst
42 mln qator, 180 GB, kunlik 40 ming qidiruv. ILIKE bilan p95 = 1.8 s,
maqsad 300 ms. Jamoa 3 kishi. Spike S-07: GIN + tsvector da p95 = 90 ms.

## Qaror
Qidiruvni PostgreSQL full text search ustida qoldiramiz.

## Ko'rib chiqilgan variantlar
1. Alohida qidiruv klasteri: qidiruv sifati yuqori, lekin operatsion
   murakkablik yuqori va izchillik eventual bo'lib qoladi.
2. Faqat trigram (pg_trgm): opechatkaga chidamli, lekin ranking yo'q.

## Oqibatlar
- Ijobiy: yangi tizim yo'q, qidiruv tranzaksiya bilan izchil.
- Salbiy: morfologiya cheklangan, facet va fuzzy qidiruv zaif.
- Qaytarish narxi: migratsiya darajasida (outbox bilan indeksga ko'chirish).

## Taxminlar
- T1: qidiruv hajmi yil davomida belgilangan chegaradan oshmaydi.
  O'lchov: QPS metrikasi.

## Kuzatiladigan metrika
- order.search.duration p95 maqsad qiymati, order.search.empty ulushi
```

Qaror sozlash bilan to'liq bo'ladi. Qidiruv so'rovi analitik xarakterda, shuning uchun uni alohida connection pool va qisqa statement timeout ortiga qo'yish kerak, aks holda bitta og'ir so'rov asosiy buyurtma oqimini to'sib qo'yadi.

```properties
# Qidiruv uchun alohida pool: asosiy oqimdan ajratilgan.
spring.datasource.search.hikari.maximum-pool-size=8
spring.datasource.search.hikari.connection-timeout=2000
spring.datasource.search.hikari.pool-name=search-pool

# Qidiruv so'rovi 1 soniyadan oshsa uzilsin, foydalanuvchi kutmasin.
spring.datasource.search.hikari.data-source-properties.options=-c statement_timeout=1000

# Hibernate ni bu pool da faqat o'qish uchun ishlatamiz.
spring.jpa.properties.hibernate.jdbc.fetch_size=50
```

Bu ADR nimani ko'rsatdi: tanlov "yaxshi texnologiya" bilan "yomon texnologiya" orasida emas edi. Tanlov jamoa o'lchami, izchillik talabi va spike natijasi orasida edi, ya'ni savol "qaysi biri yaxshi" emas, "qaysi biri muhimroq" edi - *Fundamentals* 2-bobida trade-off tahlili aynan shu savol bilan yopiladi va javob "it depends" bo'ladi. Agar keyinchalik facet qidiruv mahsulot talabiga aylansa, qidiruv sifati haqidagi taxmin buziladi, ADR-0042 "O'rnini bosdi" bo'ladi va yangi ADR alohida indeks hamda outbox orqali sinxronizatsiyani yozadi. Bu muvaffaqiyatsizlik emas, bu ADR ning maqsadga muvofiq ishlashi.

## 3.11 Nega eskiz kerak va nega ko'pchilik diagramma ishlamaydi

Jamoalar jarayonni vizuallashtirishni o'rgandi: Kanban taxtasi bir qarashda nima boshlanmagan, nima ishda va nima tugaganini ko'rsatadi. Simon Brown ning kuzatuvi shu: biz qurayotgan dasturning o'zini vizuallashtirishni unutib qo'ydik, va arxitekturani tushunish bilan uni muloqotda yetkazib bera olish bir narsa emas. Minglab odam bilan arxitektura mashg'uloti o'tkazgandan keyin uning xulosasi aniq: tizim arxitekturasini vizuallashtirish juda kam odamda bor ko'nikma, diagramma chizadiganlar ko'p, lekin bu diagrammalar ko'p narsani o'quvchining tasavvuriga qoldiradi (Simon Brown, *Software Architecture for Developers*, Leanpub, 32-bob, 79-bet).

Brown qutilar va chiziqlardan iborat norasmiy eskizning sakkiz tipik nuqsonini sanaydi: rang kodi tushuntirilmagan yoki izchil emas; qutilar va chiziqlarning turli uslublari nimani bildirishi aytilmagan; elementlar orasidagi kalit munosabat yo'q yoki noaniq; "business logic" kabi umumiy atamalar ishlatilgan; texnologiya tanlovi tushirib qoldirilgan; abstraksiya darajalari aralashtirilgan; diagramma juda ko'p tafsilot ko'rsatishga urinadi; diagrammada kontekst yoki mantiqiy boshlanish nuqtasi yo'q (32-bob, 80-bet). Shu yerdan bitta amaliy sinov chiqadi: kimdir sizga eskiz bilan dizayn ko'rsatsa, o'zingizdan so'rang, u eskizda turgan narsani aytayaptimi yoki o'z boshidagi narsani.

Eskiz chizish rassomlik emas. Brown bu haqda ochiq yozadi: muhimi san'at asari yasash emas, narsaning tubiga tez tushib, muhim nuqtalarni boshqalar tushunadigan shaklda qisqa bayon qilish. Gap batafsil modellashtirish yoki model asosida kod generatsiya qilish haqida ham emas (33-bob, 83-bet). Eskizning foydasi ro'yxat bilan beriladi: jamoada umumiy ko'rinish va umumiy maqsad tasavvuri paydo bo'ladi; texnik suhbat uchun bitta fokus nuqtasi bo'ladi; dasturchi kod ichida yurganda eskiz xarita bo'lib ishlaydi; jamoadan tashqaridagi odamlarga (operatsiya, qo'llab-quvvatlash, biznes) tushuntirish osonlashadi; yangi dasturchining jamoaga kirishi tezlashadi. Brown ning o'z xulosasi: kontekst, konteyner va komponent diagrammalari odatda yetarli (83-bet).

Brown mashg'ulotlarda to'plangan samarasiz eskizlarni nomlab chiqadi, va bu nomlar tashxis qo'yish uchun qulay (34-bob, 84-97-betlar).

| Eskiz turi | Nimasi yetishmaydi |
|---|---|
| "Xarid ro'yxati" (the shopping list) | Faqat texnologiya nomlari turadi; qaysi mahsulot nima qilayotgani va ular orasidagi ulanish yo'q |
| "Qutilar bor, chiziq yo'q" (boxes and no lines) | Javobgarlik va o'zaro ta'sir yo'q; arxitektura narsalar bilan birga ularning ta'sirini ham bildiradi |
| "Funksional ko'rinish" (the functional view) | Funksional bo'linish chizilgan, lekin javobgarlik, ta'sir va rang kodining ma'nosi yo'q |
| "Aviachipta marshrut xaritasi" (the airline route map) | Markazda tushunarli oqim bor, atrofida izohsiz belgi, turli rang va uslubdagi chiziqlar |
| "Umumiy ma'noda to'g'ri" (generically true) | Markazda "business logic" qutisi turadi; domen nomi yo'q, shuning uchun hech narsa aytmaydi |
| "Mantiqiy ko'rinish" (the logical view) | Shakl va javobgarlik bor, texnologiya tanlovi tasavvurga qoldirilgan |
| Nomlanmagan aktyorlar | Foydalanuvchi qutisi bor, lekin u kim ekani yozilmagan: yuzsiz nusxalar |

Uchinchi sabab ham bor va u tashkiliy: Brown ko'pchilik jamoa agile ga shoshilishda modellashtirish va hujjatni reja asosidagi metodologiya bilan birga uloqtirib yuborganini, UML ni tashlaganini va bu ko'nikmani o'rgatadigan odam juda kam ekanini aytadi (34-bob, 84-bet).

Brown eskizning shakli haqida gapiradi, Evans esa uning chegarasi haqida, va bu ikki pozitsiya bir-birini to'ldiradi. Evans eskizni rad etmaydi: muhokamada u doskada chizmasdan ishlay olmasligini, chizganining ko'pi esa UML sinf yoki obyekt o'zaro ta'sir diagrammalari ekanini aytadi, va sodda norasmiy UML muhokamani bitta joyga mixlab turadi, ya'ni masalaga markaziy uch-beshta obyektni chizsangiz, hamma shu obyektlar, ularning munosabatlari va eng muhimi nomlari haqida bitta tasavvurga keladi (Eric Evans, *Domain-Driven Design*, 2-bob, Documents and Diagrams). Muammo diagramma orqali butun modelni yetkazishga urinishdan boshlanadi: bunday diagrammalar bir vaqtda juda to'liq va juda kam bo'ladi, chunki modellash asbobiga kodga tushadigan hamma obyekt solinadi va tafsilot ichida asosiysi ko'rinmaydi.

Evans ning asosiy da'vosi shu: UML diagrammasi modelning eng muhim ikki jihatini ifodalay olmaydi, ya'ni tushunchalarning ma'nosini va ular nima qilishi kerakligini; xulqni operatsiya nomlari bilan ishora qilish va o'zaro ta'sir diagrammasi bilan yashirin ko'rsatish mumkin, lekin aytib bo'lmaydi, shuning uchun bu qism matnga yoki suhbatga tushadi (2-bob, Documents and Diagrams). Shundan Brown ning eskiz qoidalari bilan ziddiyatsiz, lekin boshqa tomonga qaragan ikki amaliy qoida chiqadi. Birinchisi hujjatning shakliga tegishli: matn bilan izohlangan diagramma emas, tanlangan va soddalashtirilgan diagrammalar bilan tasvirlangan matn hujjati yoziladi, dizaynning hayotiy tafsiloti esa kodda qoladi, chunki yaxshi yozilgan implementatsiya ostidagi modelni shaffof ko'rsatib turadi. Ikkinchisi hujjatni baholash mezoni: hujjat kod allaqachon yaxshi bajaradigan ishni takrorlamasin, va hujjat loyiha faoliyatiga aralashgan bo'lsin; buni tekshirishning eng oson yo'li uning ubiquitous language bilan o'zaro ta'siriga qarash, ya'ni hujjatdagi atamalar suhbatda va kodda paydo bo'lmasa, hujjat o'z vazifasini bajarmayapti va uni iroda bilan yangilab turish behuda mehnat bo'ladi (2-bob, Written Design Documents).

Uchinchi nuqta chalkashlikni oldini oladi: domenni tushuntirish uchun chizilgan rasm dizaynni boshqaradigan model emas. Evans tushuntiruvchi modelni (explanatory model) alohida ataylab ajratadi, uning obyekt modeli bo'lishi shart emasligini, va UML dan ayniqsa qochish kerakligini aytadi, chunki UML dasturiy dizayn bilan mos kelish degan yolg'on taassurot beradi; ikki model o'rtasida ba'zan moslik bo'ladi, lekin u hech qachon aniq bo'lmaydi (2-bob, Explanatory Models). Amalda bu doskadagi "biznes qanday ishlaydi" rasmini dizayn diagrammasi deb repoga qo'ymaslik degani.

## 3.12 C4 modeli: to'rt daraja va har darajaning o'quvchisi

Dasturni rasm bilan tushuntirganda odamlarning tipik xatosi bitta "uber-diagramma" yasash: unda barcha abstraksiya darajasidagi barcha tafsilot bir vaqtda bo'lishi kerak. Natija tirband, murakkab va chalkash rasm bo'ladi. Brown ning yechimi oddiy: bitta murakkab diagramma o'rniga turli abstraksiya darajasida bir nechta sodda diagramma chiziladi (Simon Brown, *Software Architecture for Developers*, Leanpub, 35-bob, 98-bet).

Buning uchun umumiy abstraksiyalar to'plami kerak. Brown ning ierarxiyasi: tizim bir nechta konteynerdan tashkil topadi, konteyner bir nechta komponentdan, komponent esa bir yoki bir nechta sinf bilan amalga oshiriladi. Sinf OO tilda eng kichik qurilish bloki. Komponent bir yoki bir nechta sinfning mantiqiy guruhi, yuqori darajali shartnoma ortida turadi. Konteyner komponentlar bajariladigan yoki ma'lumot yashaydigan narsa: web server, ilova serveri, boy klient yoki baza. Tizim eng yuqori daraja va kimgadir qiymat yetkazadigan narsani bildiradi (35-bob, 99-bet).

Shu abstraksiyalar ustida Brown dasturning statik ko'rinishini to'rt turdagi diagramma bilan xulosalaydi: kontekst (sahnani qo'yadi, kalit bog'liqlik va aktyorlarni ko'rsatadi), konteyner (yuqori darajali texnologiya tanlovi, javobgarlikning taqsimlanishi, konteynerlar qanday muloqot qilishi), komponent (har konteyner uchun kalit mantiqiy komponentlar va ularning munosabati) va sinf (ixtiyoriy daraja, faqat biror pattern yoki komponent qanday amalga oshirilganini tushuntirish kerak bo'lsa) (35-bob, 100-bet). O'quvchi har darajada boshqacha, va Brown uni har bobda alohida yozadi.

| Daraja | Nimani ko'rsatadi | O'quvchi | Manba |
|---|---|---|---|
| Kontekst | Tizim chegarasi, foydalanuvchilar, qo'shni tizimlar | Texnik va notexnik, jamoa ichi va tashqarisi | 36-bob, 104-bet |
| Konteyner | Alohida deploy qilinadigan birliklar va texnologiya tanlovi | Jamoa ichi va tashqarisidagi texnik odamlar, operatsiya va qo'llab-quvvatlash xodimi ham | 37-bob, 108-bet |
| Komponent | Bitta konteyner ichidagi mantiqiy komponentlar | Faqat ishlab chiqish jamoasi ichidagi texnik odamlar | 38-bob, 113-bet |
| Sinf | Bitta pattern yoki komponentning ichki tuzilishi | Ishlab chiqish jamoasi; ixtiyoriy daraja | 35-bob, 100-bet |

Brown uchun umumiy abstraksiya to'plami umumiy notatsiyadan muhimroq: UML ikkisini ham beradi, lekin uni samarali ishlatadigan jamoa kam uchraydi. Xarita analogiyasi shu fikrni ochadi: barcha xarita yo'l, daryo, ko'l va shahar ko'rsatadi, lekin rang, chiziq uslubi va belgilar har xil; ularni tushunish kaliti burchakdagi legend (35-bob, 100-bet). Shuning uchun norasmiy eskiz izchillikni moslashuvchanlikka almashtiradi va har diagrammada kichik legend bo'lishi kerak. Yana bir maslahat: faqat nomlangan qutilar to'plamidan iborat diagramma yasamang, qutiga javobgarlikni yozish noaniqlikni olib tashlaydi (101-bet).

C4 bitta tizimga qaraydi. Agar tashkilotdagi barcha tizim qanday joylashganini ko'rsatish kerak bo'lsa, Brown C4 ustiga yana bitta diagramma qo'yadi va model C5 ga aylanadi: tashkilot chegarasi, ichki va tashqi foydalanuvchilar, ichki va tashqi tizimlar (javobgarlik xulosasi va kimga qanday ma'lumot tegishli ekani bilan). Har qiziqtirgan tizim uchun esa C4 bo'yicha pastga tushiladi (44-bob, 138-bet).

Mark Richards va Neal Ford ning *Fundamentals of Software Architecture* kitobida C4 ga alohida bob (21-bob, "Diagramming and Presenting Architecture") bag'ishlangan, lekin korpusdagi nusxada shu bobning tanasi yo'q: PDF 20-bobdan 24-bobga o'tadi. Faqat ilovadagi o'z-o'zini tekshirish savollari C4 ning "to'rt C" si haqida savol borligini tasdiqlaydi. Shuning uchun bu yerda shu kitobdan hech narsa iqtibos qilinmaydi, C4 ning butun bayoni Brown dan olingan (Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, ilova "Self-Assessment Questions", 21-bob savollari).

## 3.13 Kontekst diagrammasi: tizim chegarasi va tashqi aktyorlar

Kontekst diagrammasi uch savolga javob beradi: biz qanday tizim qurayapmiz yoki qurganmiz, undan kim foydalanadi, va u mavjud IT muhitiga qanday joylashadi (Simon Brown, *Software Architecture for Developers*, Leanpub, 36-bob, 102-bet). Shakli juda oddiy: markazda tizimingiz bitta quti bo'lib turadi, atrofida foydalanuvchilar va u bilan integratsiyaga kiradigan boshqa tizimlar. Brown bu yerda tafsilot muhim emasligini ta'kidlaydi: bu keng burchakli ko'rinish, va fokus texnologiya va protokolda emas, odam va tizimda (102-bet, 105-bet).

Chiziqlarni izohsiz qoldirmang. Brown har o'zaro ta'sirni maqsad bilan annotatsiya qilishni tavsiya qiladi, foydalanuvchi va tizim orasidagi chiziqqa esa shu turdagi foydalanuvchi tizimdan qanday foydalanishini xulosalaydigan bir necha muhim use case ni qisqa ro'yxat qilib yozib qo'yadi (36-bob, 103-bet).

Nega bu oddiy rasm foydali ekanini Brown to'rt punktda beradi: kontekst ochiq yoziladi, demak taxmin qolmaydi; mavjud IT muhitiga nima qo'shilayotgani ko'rinadi; texnik va notexnik odam birga ishlatadigan boshlanish nuqtasi paydo bo'ladi; tizimlar orasidagi interfeysni tushunish uchun kim bilan gaplashish kerakligi ma'lum bo'ladi. Uni chizish ikki daqiqada bo'ladi, shuning uchun chizmaslikka bahona yo'q (36-bob, 103-bet).

Quyidagi misol buyurtma platformasi uchun. Diagramma matni korpusning namunasi, kitobdagi rasm emas: Brown ning misoli financial risk system va techtribes.je.

```text
Kontekst diagrammasi: Buyurtma platformasi

  [Xaridor]                         [Omborchi]            [Qo'llab-quvvatlash operatori]
      |                                 |                             |
      | buyurtma beradi,                | yig'ish ro'yxatini          | buyurtmani qidiradi,
      | holatini kuzatadi               | oladi va yopadi            | bekor qiladi
      v                                 v                             v
  +---------------------------------------------------------------------------+
  |                        BUYURTMA PLATFORMASI                               |
  |      buyurtmani qabul qiladi, to'lovni boshlaydi, holatni yuritadi        |
  +---------------------------------------------------------------------------+
      |                        |                       |                 |
      | to'lovni avtorizatsiya | yetkazib berish       | hisob-faktura   | identifikatsiya
      | qiladi (HTTPS/REST)    | buyurtmasi (HTTPS)    | (fayl, SFTP)    | (OIDC)
      v                        v                       v                 v
  [To'lov provayderi]   [Logistika hamkori]      [Buxgalteriya tizimi]  [Keycloak]

Legend: to'rtburchak - tizim; kvadrat qavs - tashqi aktyor yoki tashqi tizim;
strelka - bog'liqlik yo'nalishi (chaqiruvchidan chaqirilganga);
chiziq yozuvi - o'zaro ta'sirning maqsadi va protokoli.
```

Kontekst diagrammasidagi aktyorlar ro'yxati [kim foydalanadi](02-muammoni-tushunish-va-togri-savol-berish.md#27-kim-foydalanadi-tashqi-foydalanuvchi-ichki-jamoa-boshqa-servis) bo'limidagi iste'molchi ro'yxatidan chiqadi: o'sha ro'yxat tayyor bo'lsa, diagramma uni rasm qilib ko'rsatadi. C4 kontekst diagrammasini DDD dagi [kontekst xaritasi](../patterns/13-domain-driven-design-patternlari.md#133-kontekst-xaritasi-context-map) bilan aralashtirmang: xarita bitta tizim ichidagi bounded context lar va jamoalar orasidagi munosabat turini ko'rsatadi, kontekst diagrammasi esa bitta tizimning tashqi dunyo bilan chegarasini.

## 3.14 Konteyner diagrammasi: alohida deploy qilinadigan birliklar

Kontekst diagrammasi tizimni bitta quti qilib ko'rsatadi, konteyner diagrammasi shu qutini ochadi. U besh savolga javob beradi: tizimning umumiy shakli qanday, yuqori darajadagi texnologiya qarorlari nima, javobgarlik qanday taqsimlangan, konteynerlar bir-biri bilan qanday muloqot qiladi, va dasturchi sifatida men funksiyani qaysi joyga yozishim kerak (Simon Brown, *Software Architecture for Developers*, Leanpub, 37-bob, 106-bet).

Brown konteyner deganda tizimni tashkil qiladigan mantiqiy bajariladigan birlik yoki processni tushunadi: web server, ilova serveri, SQL va NoSQL baza, fayl tizimi, `public static void main` uslubidagi mustaqil ilova, web brauzer, cron va shunga o'xshash rejalashtiruvchi (37-bob, 107-bet). Har konteyner uchun uch narsa yoziladi: nom, texnologiya va javobgarlikning juda yuqori darajali bayoni. Brown konteyner ichidagi komponentlarni ko'rsatish mumkin, lekin odatda bu diagrammani tirband qilib qo'yadi, deb ogohlantiradi (107-bet).

Quti diagrammaga tushadimi yoki yo'qmi degan savolga Brown bitta sinov beradi: o'zingizdan so'rang, bu quti alohida fizik yoki virtual apparatga deploy qilinadimi yoki qilinishi mumkinmi. Konteyner diagrammasida ko'rsatilgan har narsa alohida deploy qilinishi kerak. Bu ularni alohida infratuzilmaga qo'yish shart degani emas, qo'yish imkoni borligi yetarli (37-bob, 107-bet).

Chiziqlar bu yerda processlar orasidagi muloqot. Brown qo'shishni tavsiya qiladigan ma'lumot: o'zaro ta'sirning maqsadi ("ma'lumot o'qiydi va yozadi", "hisobot yuboradi"), muloqot usuli, muloqot uslubi (sinxron, asinxron, batch) va protokol bilan port (37-bob, 107-108-betlar). Agar diagrammaga tashqi foydalanuvchi va tizimlarni ham qo'ygan bo'lsangiz, o'z konteynerlaringiz atrofiga quti chizib tizim chegarasini ochiq ajratib qo'ying: shu chegara kontekst diagrammasidagi bitta qutiga to'g'ri keladi (108-bet).

```text
Konteyner diagrammasi: Buyurtma platformasi (tizim chegarasi ichida)

  [Xaridor]                                   [Omborchi]
      | HTTPS                                     | HTTPS
      v                                           v
  +=============================================================================+
  |  +----------------------------+        +-----------------------------+       |
  |  | order-api                  |  REST  | warehouse-ui                |       |
  |  | Spring Boot 3, embedded    |<-------| Spring Boot 3 + Thymeleaf   |       |
  |  | Tomcat, port 8080          |  HTTPS |                             |       |
  |  | buyurtmani qabul qiladi,   |        | yig'ish ro'yxatini beradi   |       |
  |  | holat o'zgarishini e'lon   |        +-----------------------------+       |
  |  | qiladi                     |                                             |
  |  +----------------------------+                                             |
  |     |  JDBC          |  produce           |  RESP                           |
  |     |  (HikariCP)    |  (order.events)    |  (Lettuce)                      |
  |     v                v                    v                                 |
  |  +------------+  +------------------+  +---------------+                     |
  |  | PostgreSQL |  | Kafka            |  | Redis         |                     |
  |  | 16, buyurt-|  | 3 partition,     |  | katalog keshi |                     |
  |  | ma va out- |  | order.events     |  | va idempoten- |                     |
  |  | box jadvali|  | topic            |  | tlik kaliti   |                     |
  |  +------------+  +------------------+  +---------------+                     |
  |                         ^ consume (order-notifier, Spring Boot, cron emas)   |
  +=============================================================================+

Legend: qo'sh chiziqli quti - tizim chegarasi; ichkaridagi har quti alohida
deploy qilinadigan konteyner; chiziq yozuvi - protokol va maqsad.
```

Konteyner diagrammasi nusxa soni haqida hech narsa aytmaydi. Brown web server fermasi yoki klaster bu diagrammada ko'rinmasligini, fizik nusxa, failover va klasterlash alohida deployment diagrammasida turishini aniq yozadi (37-bob, 110-bet). Korpusda deploy tomoni [konteyner va cgroup](31-deployment-haqiqati-konteyner-cgroup-jvm-va.md#311-konteyner-nima-va-nima-emas) bobida ko'rilgan; diqqat qiling, C4 dagi "konteyner" Docker konteyneri degani emas, u Brown ning atamasi va bazani ham qamraydi.

## 3.15 Komponent diagrammasi va nega kod darajasiga tushmaslik kerak

Konteyner diagrammasidan keyin har konteynerni ichkaridan ochish navbati keladi. Komponent diagrammasi uch savolga javob beradi: tizim qanday komponentlardan tashkil topgan, tizim yuqori darajada qanday ishlashi tushunarlimi, va har komponentning uyi bormi, ya'ni u qaysi konteynerda yashaydi (Simon Brown, *Software Architecture for Developers*, Leanpub, 38-bob, 111-bet). Brown bitta muhim cheklov qo'yadi: komponent diagrammasi odatda faqat bitta konteyner ichidagi komponentlarni ko'rsatadi. Bu qat'iy qoida emas, kichik tizimda hammasini bitta diagrammaga sig'dirish mumkin, lekin tirband bo'lsa bo'lish vaqti keldi (112-bet).

Komponent nima degan savolga javob 41-bobda: komponent interfeys ortidagi bog'liq xatti-harakatlar to'plami, u bir yoki bir nechta hamkorlik qiladigan sinf bilan amalga oshiriladi. Yaxshi komponent yaxshi sinf bilan bir xil xususiyatga ega: yuqori kogeziya, past bog'liqlik, aniq belgilangan ochiq interfeys va yaxshi enkapsulyatsiya (41-bob, 122-bet). Har komponent uchun diagrammada nom, texnologiya va javobgarlikning qisqa bayoni yoziladi (38-bob, 112-bet).

Nega sinf darajasiga tushmaslik kerak. Brown ning javobi: komponent darajasida ishlash sinf va koddan bir pog'ona yuqoridagi dizayn, va u tizimning ichki tuzilishini, qayerda qayta ishlatish imkoni borligini, komponentlar orasida va komponent bilan konteyner orasida qanday bog'liqlik borligini ko'rish uchun eng qulay daraja. Bu darajada dizayn haftalar emas, bir necha soat yoki kun ishi, va u sinf darajasidagi ishga umumiy tuzilish haqida qayg'urmasdan o'tishga tayyorlab qo'yadi (38-bob, 113-bet). Shu bilan birga bu to'liqlikni tekshirish usuli ham: har use case ni bir yoki bir nechta komponent orqali kuzatib chiqa olish kerak, va masalan audit talabi bo'lib audit komponenti yoki javobgarligi yo'q bo'lsa, demak nimadir o'tkazib yuborilgan (112-113-betlar).

Spring da komponent chegarasi paket bilan beriladi va ichki sinflar paket darajasida yopiladi. Quyidagi misolda bitta komponent (`pricing`) ichida Spring stereotiplari turadi, tashqariga faqat interfeys chiqadi.

```java
// src/main/java/com/shop/order/pricing/PricingFacade.java
package com.shop.order.pricing;

// Komponentning ochiq shartnomasi: diagrammadagi "Pricing" qutisi shu.
public interface PricingFacade {
    Money quote(OrderDraft draft);
}

// src/main/java/com/shop/order/pricing/PricingService.java
package com.shop.order.pricing;

import org.springframework.stereotype.Service;

@Service
class PricingService implements PricingFacade {   // paket darajasida: tashqaridan ko'rinmaydi

    private final DiscountRepository discounts;   // @Repository, ham paket darajasida

    PricingService(DiscountRepository discounts) {
        this.discounts = discounts;
    }

    @Override
    public Money quote(OrderDraft draft) {
        return discounts.findActive(draft.customerId())
                .map(discount -> discount.applyTo(draft.subtotal()))
                .orElseGet(draft::subtotal);
    }
}
```

Shu shakl kod tashkil etishning paket bo'yicha emas, komponent bo'yicha variantini bildiradi; tanlovning afzalligi va narxi [feature bo'yicha vs qatlam bo'yicha paketlash](../patterns/12-arxitektura-uslublari.md#1228-feature-boyicha-vs-qatlam-boyicha-paketlash-package-by-feature-vs-package-by-layer) yozuvida, uslubning o'zi esa [komponentga asoslangan arxitektura](../patterns/12-arxitektura-uslublari.md#1230-komponentga-asoslangan-arxitektura-component-based-architecture) yozuvida ko'rilgan.

Ikki tipik savolga Brown ning javobi bor. Umumiy komponent (masalan ikki konteyner ishlatadigan baza kirish qatlami) har mos komponent diagrammasida chiziladi va "bu umumiy komponent" degan izoh bilan belgilanadi. Utility komponent (masalan hamma ishlatadigan logging) uchun ikki variant bor va biri aniq toza: uni markazga qo'yib hamma komponentdan chiziq tortish to'g'ri, lekin diagrammani tez tirband qiladi; uni chetga qo'yib "bu hamma komponent ishlatadigan utility komponent" deb izohlash ma'qul (44-bob, 137-138-betlar).

## 3.16 "Kodda shunday qilasizmi" sinovi va model bilan kod orasidagi uzilish

Diagramma qanday chizilishi kerakligi haqidagi ko'p savolga Brown bitta savol bilan javob beradi: kodda ham shunday qilasizmi. Mashg'ulotdagi tipik dialog shunday ketadi. Savol: logging komponentini web server va ilova serveridan tashqariga chizaylikmi, ikkisi ham ishlatadi. Brown ning javobi: kodda shunday qilasizmi, u chindan ham alohida process bo'lib ikkisidan tashqarida ishlaydimi. Javob yo'q bo'lsa va u ikki serverga deploy qilinadigan umumiy JAR bo'lsa, diagrammada ham shunday chiziladi: har server ichida logging komponenti turadi va u annotatsiya bilan umumiy komponent deb belgilanadi (Simon Brown, *Software Architecture for Developers*, Leanpub, 40-bob, 120-bet).

Ikkinchi dialog qatlamlar haqida. Savol: UI dan bazaga hamma murojaat servis qatlami orqali o'tishini ko'rsataylikmi. Brown ning javobi yana bir xil: siz uni shunday amalga oshirasizmi yoki UI bazaga to'g'ridan-to'g'ri boradimi. Agar jamoa CQRS ni mo'ljallayotgan bo'lsa va UI servis qatlamini chetlab o'tib data access ni ishlatsa, diagramma aynan shunday chiziladi, UI dan ikki chiziq bilan, va chiziqlar niyat va sabab bilan annotatsiya qilinadi (40-bob, 120-121-betlar).

Qoida umumiy: diagramma haqiqatni aks ettiradigan abstraksiya berishi kerak, mavjud bo'lmagan konseptual tasvir emas. Diagramma elementlarining kod bazasida qanday aks etganini va teskarisini ko'rish imkoni bo'lishi kerak. Allaqachon qurilgan tizimni retrospektiv chizayotgan bo'lsangiz, savol "biz uni shunday kodladikmi" ga aylanadi, printsip esa o'zgarmaydi (40-bob, 121-bet).

Bu sinov kerak bo'lishining sababi Brown da ochiq aytilgan: biz komponent haqida gaplashamiz, lekin sinf yozamiz. Odamlar tizimni komponent sifatida muhokama qiladi, lekin bu tuzilish kodda aks etmaydi, va shu yerdan arxitektura bilan kod orasidagi uzilish chiqadi: devordagi diagramma bir narsa, kod boshqa narsa aytadi. George Fairbanks buni o'z kitobida "model-code gap" deb nomlaydi (41-bob, 123-124-betlar). Sababi ko'pincha paketlash uslubi: qatlam bo'yicha paketlashda diagrammadagi bitta komponent bir necha paketga sochilib ketadi, va pastki qatlam sinflari ochiq ko'rinishda bo'lgani uchun istalgan joydan chaqirilishi mumkin (41-bob, 124-125-betlar). Brown ning xulosasi qisqa: agar tizim tuzilishini tushuntirish qiyin bo'lsa, tuzilishni o'zgartiring (41-bob, 127-bet).

Diagramma bilan kodning mos kelishini odamning diqqatiga tashlab qo'ymang. Bu moslikni avtomatik tekshirish korpusning tanlovi, kitobda bunday vosita yo'q: Brown 2014 da bu ishni qo'lda ko'rib chiqish deb qoldiradi. Java da chegarani [ArchUnit asoslari](../testing/14-arxitektura-testlari-va-kod-sifati.md#142-archunit-asoslari) bobidagi test sifatida yozib qo'yish mumkin, va shunda diagrammadagi strelka yo'nalishi CI da qo'riqlanadi.

```java
// Diagrammadagi da'vo: order-api konteynerida pricing komponenti
// checkout komponentini CHAQIRMAYDI, faqat teskarisi.
@AnalyzeClasses(packages = "com.shop.order", importOptions = DoNotIncludeTests.class)
class KomponentChegarasiTest {

    @ArchTest
    static final ArchRule pricing_checkoutga_bogliq_emas =
            noClasses().that().resideInAPackage("..order.pricing..")
                    .should().dependOnClassesThat().resideInAPackage("..order.checkout..");

    // Komponent ichki sinflari tashqariga chiqmasin: diagrammadagi quti
    // haqiqatan ham interfeys ortida yopilgan bo'lsin.
    @ArchTest
    static final ArchRule faqat_fasad_ochiq =
            classes().that().resideInAPackage("..order.pricing..")
                    .and().areNotInterfaces()
                    .should().notBePublic();
}
```

## 3.17 Samarali eskiz: sarlavha, legend, javobgarlik va strelka

UML dan voz kechib qutilar va chiziqlarga o'tgan jamoa izchillikni moslashuvchanlikka almashtiradi, va natijada diagramma elementlari bir xil ishlatilmaydi hamda rasm yonida og'zaki bayon kerak bo'lib qoladi. Brown "NoUML" diagramma chizadiganlar uchun aniq ro'yxat beradi (Simon Brown, *Software Architecture for Developers*, Leanpub, 43-bob, 131-bet).

Sarlavha. Diagrammada sarlavha bo'lishi birinchi yordam beradigan narsa: qisqa va ma'noli bo'lsin, diagrammalar ma'lum tartibda o'qilishi kerak bo'lsa raqamlab qo'yiladi (131-bet). Yorliqlar. Qisqartmadan saqlaning, kerak bo'lsa ularni loyiha glossariysida yoki diagrammadagi legendda yozib qo'ying; sanoatda keng ishlatiladigan texnologiya qisqartmalari (JMS, POJO) bundan mustasno, lekin shubha bo'lsa to'liq nom yozing (131-bet). Shakllar. Ko'pchilik silindrni baza deb o'qiydi, lekin shu taxmin to'g'rimi yoki yo'qmi, diagrammaning o'zi tasdiqlashi kerak (131-bet).

Javobgarlik. Faqat nom yozilgan qutilar bilan to'ldirilgan diagramma vasvasasiga berilmang: tizim va komponentga javobgarlikning juda qisqa bayonini qo'shish noaniqlikni olib tashlaydi. Brown shakl beradi: etti qo'shuv-ayirish ikki banddan oshmaydigan ro'yxat yoki bitta qisqa gap, kichik shriftda (43-bob, 132-bet).

Chiziqlar. Brown chiziqlarni diagrammaning eng e'tiborsiz qolgan qismi deb hisoblaydi: ular qutilarni ushlab turadi, lekin o'zlariga diqqat qaratilmaydi. Ikki savolga javob kerak: chiziq uslubi (uzluksiz, nuqtali, chizikli) ahamiyatlimi va nimani bildiradi; strelkalar bog'liqlik yo'nalishini ko'rsatadimi yoki ma'lumot oqimi yo'nalishini. Chiziqqa yozilgan izoh ("ishlatadi", "ma'lumot yuboradi", "hisobotni yuklab oladi") ko'pincha shu noaniqlikni yopadi, lekin ikki tomoni ham strelkali chiziqdan ehtiyot bo'lish kerak (43-bob, 132-133-betlar). Rang, chegara, joylashuv va yo'nalish uchun ham bir xil talab: rang kodi legendda bo'lsin, element atrofidagi chegara nimani bildirishi yozilsin; "to'g'ri" yo'nalish yo'q, lekin odatdagidan teskari chizilgan diagramma yoki chalkashtiradi yoki ataylab ishlaydi (133-135-betlar).

Shu ro'yxatdan bitta taqiq ham chiqadi va u vositaga tegishli. Brown IDE yoki UML vositasi avtomatik generatsiya qiladigan to'liq diagrammadan voz kechishni maslahat beradi: qo'lda chizilgan, faqat tanlangan maydon va metodni ko'rsatadigan yuqori darajali diagramma foydaliroq (Simon Brown, *Software Architecture for Developers*, Leanpub, 55-bob, 163-bet). Sabab yuqoridagi talablarning o'zidan chiqadi: avtomatik diagramma sarlavha ham, javobgarlik bayoni ham, legend ham bermaydi va tanlov qilmaydi, ya'ni u modelni emas, kodni ko'rsatadi. Shu sababli generatsiya qilingan rasmni hujjatga qo'yish [model bilan kod orasidagi uzilish](#316-kodda-shunday-qilasizmi-sinovi-va-model-bilan-kod-orasidagi-uzilish) muammosini hal qilmaydi: u diagramma sonini oshiradi, abstraksiya darajasini esa pasaytiradi.

Legend hammasini bog'laydi. Brown legendga shakl, chiziq, rang, chegara va qisqartmalarning izohi tushishini aytadi, va ko'rinib turgan narsa ham boshqa tajribaga ega odam tomonidan boshqacha o'qilishi mumkinligi uchun legendni qo'shishni tavsiya qiladi (43-bob, 135-bet). Oxirgi maslahat amaliy: diagramma chizilayotganda berilgan savollarga quloq soling, agar o'zingiz "aniqlik uchun aytaman, bu strelkalar ma'lumot oqimi" deb tushuntirayotgan bo'lsangiz, shu ma'lumot legendda turishi kerak (136-bet).

```text
Legend (har diagrammaga qo'yiladigan minimal to'plam)

  To'rtburchak           deploy qilinadigan konteyner (nom + texnologiya + javobgarlik)
  Yumaloq burchakli quti mantiqiy komponent (interfeys ortidagi xatti-harakat to'plami)
  Kvadrat qavs [ ]       tizim chegarasidan tashqaridagi aktyor yoki tizim
  Qo'sh chiziqli quti    tizim chegarasi (kontekst diagrammasidagi bitta qutiga teng)
  Uzluksiz strelka       sinxron chaqiruv; yo'nalish: chaqiruvchidan chaqirilganga
  Nuqtali strelka        asinxron hodisa; yo'nalish: chiqaruvchidan iste'molchiga
  Kulrang to'ldirish     mavjud tizim, bu ishda o'zgarmaydi
  Qisqartmalar           OIDC - OpenID Connect; DLQ - dead letter queue
```

Brown bobni diagrammani review qilish ro'yxati bilan yopadi va u to'qqiz banddan iborat: yechimni bir necha abstraksiya darajasida ko'ra olaman va tushunaman; katta manzarani tushunaman, kim ishlatishini va mavjud IT muhitiga qanday bog'liqlik borligini bilaman; mantiqiy konteynerlarni va yuqori darajali texnologiya tanlovini tushunaman; asosiy komponentlar nima va ular muhim use case larni qanday qoplaydi, buni tushunaman; barcha komponentning nima qilishini va har birining uyi borligini ko'raman; notatsiya, konvensiya va rang kodini tushunaman; diagrammalar orasidagi izchillikni ko'raman va elementlar bir xil ishlatilgan; biznes domen nimaligini tushunaman; amalga oshirish strategiyasini (framework, kutubxona, API) tushunaman va tizim qanday qurilishini deyarli tasavvur qila olaman (43-bob, 135-136-betlar). Bu ro'yxat ham yangi dizayn uchun, ham mavjud tizimni retrospektiv hujjatlash uchun ishlaydi. Diagrammani review ga qo'yish tartibi [arxitektura qarorlarini jamoaga tarqatish](36-code-review-va-jamoada-texnik-yetakchilik.md#368-arxitektura-qarorlarini-jamoaga-tarqatish-hujjat-ichki-suhbat-namuna-kod) bo'limidagi yo'l bilan bir xil: diagramma pull request ichidagi fayl bo'lsa, u review ga tushadi.

*Fundamentals of Software Architecture* 21-bobi bu mavzuda yana uch nomni beradi: "irrational artifact attachment", komponentlar orasidagi nuqtali chiziqning ma'nosi va taqdimotdagi "bullet-riddled corpse" antipatterni. Korpusdagi nusxada shu bobning tanasi yo'q, faqat ilovadagi savollar bu nomlarni tasdiqlaydi, shuning uchun bu yerda ularning tavsifi berilmaydi: nomlari sanaladi va tavsif uchun asl 21-bobga murojaat qilish kerak (Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, ilova "Self-Assessment Questions", 21-bob savollari).

## 3.18 Arxitektura ko'rinishi (view) va uni hujjatlashtirish qoidalari

C4 bitta yondashuv, lekin arxitektura hujjatlashning umumiy apparati "ko'rinish" (view) tushunchasi ustida qurilgan. *Documenting Software Architectures* uni eng muhim tushuncha deb ataydi va ta'rifni qisqa beradi: ko'rinish bu tizim elementlarining bir to'plami va ular bilan bog'liq munosabatlarning tasviri (Paul Clements va boshqalar, *Documenting Software Architectures: Views and Beyond*, 2-nashr, Addison-Wesley, 2010, Prolog, P.3, 22-bet). Kitobning analogiyasi qush qanoti: patlar, skelet, qon aylanishi, mushaklar ko'rinishlari bor, va qaysi biri qanotning arxitekturasi degan savolga javob hech biri, qaysilari arxitekturani yetkazadi degan savolga javob esa hammasi (22-bet).

Shundan kitobning asosiy printsipi chiqadi: arxitekturani hujjatlashtirish bu tegishli ko'rinishlarni hujjatlashtirish va ustiga bir nechta ko'rinishga tegishli hujjatni qo'shish (P.3, 22-bet). Qaysi ko'rinish tegishli ekani maqsadga bog'liq. Kitob buni sifat atributlari bilan bog'laydi: har ko'rinish turli sifat atributini turli darajada ochadi, qatlamli ko'rinish portativlik haqida gapiradi, deployment ko'rinishi esa unum va ishonchlilik haqida mulohaza yuritishga imkon beradi (22-bet). Bitta ko'rinish arxitekturani to'liq ifodalay olmaydi, va bu kamchilik emas: arxitekturaning mohiyati hozirgi vazifaga kerak bo'lmagan ma'lumotni bosib turish, shuning uchun har ko'rinish ba'zi tomonlarni ta'kidlab, boshqalarini e'tibordan chetga suradi (23-bet).

Eng amaliy qism bu ko'rinishni hujjatlashtirish tarkibi. Kitob bitta ko'rinish hujjatiga besh element qo'yadi: birlamchi taqdimot (odatda grafik, ko'rinishning asosiy elementlari va munosabatlarini ko'rsatadi); element katalogi (diagrammada ko'rsatilgan elementlarni tushuntiradi, ta'riflaydi va ularning xususiyatlarini sanaydi); elementlarning interfeysi va xatti-harakatining spetsifikatsiyasi; variativlik qo'llanmasi (arxitekturani moslashtirish uchun qurilgan mexanizmlar); sabab va dizayn ma'lumoti (P.3, 23-bet). Barcha ko'rinishga tegishli hujjat esa to'rt narsani o'z ichiga oladi: butun to'plamga kirish va o'quvchi qo'llanmasi; ko'rinishlar bir-biri bilan va tizim bilan qanday bog'liqligi; umumiy arxitektura uchun cheklovlar va sabab; to'plamni yuritish uchun kerakli boshqaruv ma'lumoti (23-bet).

Ko'rinish, uslub (style) va ko'rinish turi aralashtirilmasin. Kitobda uslub elementlar va munosabat turlarining ixtisoslashishi hamda ularni qanday ishlatish mumkinligi haqidagi cheklovlar to'plami (P.4, 25-bet), va uslubni tizimga qo'llaganda natija ko'rinish bo'ladi. Kitob uslublarni uch kategoriyaga ajratadi, chunki arxitektor dasturi haqida bir vaqtda uch xil o'ylashi kerak: u amalga oshirish birliklari to'plami sifatida qanday tuzilgan, runtime da xatti-harakat va o'zaro ta'siri bor elementlar to'plami sifatida qanday tuzilgan, va atrof-muhitdagi dastur bo'lmagan tuzilmalar bilan qanday bog'langan (P.4.1, 29-bet).

| Kategoriya | Nimani hujjatlashtiradi | Java va Spring da nima bo'ladi |
|---|---|---|
| Module styles | Tizimning asosiy amalga oshirish birliklari | Maven yoki Gradle modul, Java paket, Spring Modulith moduli |
| Component-and-connector (C&C) styles | Tizimning bajarilish birliklari | Bean, ishga tushgan Spring Boot process, Kafka consumer group, ulanish: REST, topic |
| Allocation styles | Dastur bilan dastur bo'lmagan resurs orasidagi munosabat | Pod va node, jamoa egaligi (`docs/OWNERS.tsv` kabi), CI muhiti |

Modul bilan komponentni farqlash shu uch kategoriyaning asosi. Kitob modulni avvalo amalga oshirish birligi deb ta'riflaydi (Parnas da javobgarlikni modulga berish mezoni information hiding), komponentni esa runtime birligi deb ta'riflaydi va Szyperski ning ta'rifini keltiradi: komponent mustaqil deploy qilinishi mumkin va uchinchi taraf uni kompozitsiyaga kirita oladi (P.4.1, 29-30-betlar). Shu farq C4 da ham ko'rinadi: Brown ning "komponent" i interfeys ortidagi mantiqiy guruh, ya'ni Clements ma'nosida modulga yaqinroq, "konteyner" i esa bajarilish birligi. Diqqat qiling, ikki kitob bir xil so'zni boshqacha ishlatadi, va hujjatda qaysi ma'noda ishlatayotganingizni aytib qo'yish kerak.

Uslub tanlash hujjatlashtirish majburiyatini ham yuklaydi, va bu majburiyat ko'pincha o'tkazib yuboriladi. Kitob talabni aniq qo'yadi: uslub tanlanganda uning kiritgan ixtisoslashishi va cheklovlari hamda u tizimga berayotgan xususiyatlar yoziladi; agar uslub adabiyotda ta'riflangan bo'lsa, majburiyat shu ta'rifga havola bilan qoplanadi, o'z uslubingizni o'ylab topgan bo'lsangiz esa uning style guide ini o'zingiz yozasiz (P.4, 26-bet). Amaliy natija: "biz qatlamli arxitektura ishlatamiz" degan jumla hujjat emas, chunki u qaysi qatlam qaysi qatlamga murojaat qila olishini va bu cheklov nimani kafolatlashini aytmaydi. [ADR](#31-adr-architecture-decision-record-tuzilishi-kontekst-qaror-oqibat-holat) shaklida bu kontekst va oqibat qatorlariga tushadi.

Ikkinchi majburiyat ko'rinishlar orasidagi bog'lanishga tegishli, va yuqoridagi "ko'rinishlar bir-biri bilan qanday bog'liqligi" punktining aniq mexanizmi shu. Agar bitta element ikki ko'rinishda chiqsa, u ko'priklovchi element (bridging element) bo'ladi va unga ikki ko'rinish orasidagi moslikni ko'rsatadigan hujjat, ya'ni mapping biriktiriladi; aks holda ikki qism bir-biri bilan qanday gaplashishi hujjatdan tushib qoladi (P.4, 26-bet). Spring loyihasida tipik ko'priklovchi element modul bilan konteyner orasida turadi: `payment` Maven moduli module ko'rinishida bitta quti, deployment ko'rinishida esa u `order-service` pod i ichida yashaydi, va mapping shu ikkisini bog'laydi. Mapping yozilmasa, "modul chegarasi" bilan "deploy chegarasi" aralashadi.

Shundan uchinchi qaror chiqadi: bir tizimda ikki uslub uchrashsa ikki yo'l bor. Birinchisi ko'rinishlarni alohida hujjatlashtirish, ikkinchisi ularni bitta birlashgan ko'rinishga (overlay) yig'ish; tanlov esa manfaatdor kim ekaniga qarab qilinadi (P.4, 27-bet). Mezoni amaliy: o'quvchi ikki uslubni birga ko'rishi shart bo'lsa overlay, har biri bilan alohida ishlasa alohida ko'rinish. Overlay ning narxi diagrammaning zichligi, alohida ko'rinishning narxi esa ikkisi orasidagi mapping ni qo'lda saqlash.

Brown bu terminologiyadan ogohlantiradi: IEEE 1471, ISO/IEC/IEEE 42010 va Kruchten ning 4+1 modeli ko'rinishlar beradi, lekin atamaga ko'nikmagan odam uchun "konseptual ko'rinish" bilan "mantiqiy ko'rinish" farqi haqidagi tortishuv tez boshlanadi. Uning maslahati: nimani yetkazayotganingizni aniq bilib, bo'limni shunga mos nomlang (Simon Brown, *Software Architecture for Developers*, Leanpub, 47-bob, 147-148-betlar).

## 3.19 Software guidebook: kod aytmagan narsani yozish

Kod hamma narsani aytmaydi. Brown yangi loyihaga kelgan dasturchining holatidan boshlaydi: kod bazasini ochib, paket va papka tuzilishidan, nom konvensiyasidan arxitektura haqida bir narsa chiqarish mumkin, lekin bir qancha savol javobsiz qoladi. Uning ro'yxati: tizim mavjud tizim manzarasiga qanday joylashadi; nega aynan shu texnologiya tanlangan; tizimning umumiy tuzilishi qanday; komponentlar runtime da qayerda deploy qilinadi va qanday muloqot qiladi; logging, konfiguratsiya va xatolarni qayta ishlashga qanday yondashilgan va u kod bo'ylab izchilmi; kod bazasida qanday pattern va printsiplar ishlatiladi; yangi funksiyani qayerga va qanday qo'shiladi; xavfsizlik stack bo'ylab qanday amalga oshirilgan; masshtablanish qanday erishiladi; boshqa tizimlar bilan interfeys qanday ishlaydi (Simon Brown, *Software Architecture for Developers*, Leanpub, 46-bob, 142-bet). Javobni koddan ham topish mumkin, lekin bu og'ir ish, va to'g'ri savol bermasa to'g'ri javob chiqmaydi: nimani bilmasligingizni bilmaysiz (142-bet).

Brown yechimni shabloni bilan beradi va metafora tanlaydi: qo'shimcha hujjat 1990-yillardagi arxitektura hujjati shabloni emas, o'zgarib turadigan sayohat qo'llanmasi (guidebook) bo'lishi kerak (47-bob, 144-bet). Qo'llanmaning to'rt qismi: xaritalar (turli abstraksiya darajasidagi kichik sondagi sodda diagramma, kod bazasida yurish uchun), diqqatga sazovor joylar (hamma narsani emas, qiziqish nuqtalarini sanash: web sahifa patterni, ma'lumotga kirish strategiyasi, xavfsizlik va masshtablanish), tarix va madaniyat (nega tizim shunday ekanini tushuntiradigan sabab, yangi odam uchun ayniqsa qimmatli), va amaliy ma'lumot (kod qayerda, qanday build qilinadi, qanday deploy qilinadi, jamoa qanday printsiplarga amal qiladi) (145-147-betlar).

Brown qo'llanmaga o'n uch bo'lim taklif qiladi: Context, Functional Overview, Quality Attributes, Constraints, Principles, Software Architecture, External Interfaces, Code, Data, Infrastructure Architecture, Deployment, Operation and Support, Decision Log (47-bob, 147-bet). Uchtasi majburiy va Brown har biri uchun "Required: Yes" deb yozadi. Context sahnani qo'yadi, bir-ikki bet yetarli va kontekst diagrammasi hikoyaning ko'p qismini aytib beradi (48-bob, 149-bet). Functional Overview tizim nima qilishini xulosalaydi va qaysi funksiya, use case yoki rol arxitektura uchun ahamiyatli ekanini hamda nega ahamiyatli ekanini ochiq bog'laydi (49-bob, 150-bet). Software Architecture bo'limi "katta manzara": Brown unda konteyner va komponent diagrammalarini asosiy fokus qilib qo'yadi, yoniga qisqa bayon va har konteyner bilan komponentning xulosasini yozadi (53-bob, 158-bet).

Qo'llanma mahsulot haqida, loyiha haqida emas. Brown yigirma yillik tizimlarni ko'rgan: ularda loyiha darajasidagi hujjat bor, lekin mahsulot qanday ishlashi va qanday evolyutsiya qilgani haqida hech narsa yo'q. Uning tavsiyasi: har tizim uchun bitta software guidebook, va keyin har loyiha yoki o'zgarish oqimi shu qo'llanmaga kichik delta bo'ladi (47-bob, 148-bet). Hujjat yangilanib turishi sharti [ADR ni repoda saqlash](#38-adr-ni-repoda-saqlash-raqamlash-va-eskirganini-belgilash) bo'limida "Rule 6" bilan birga ko'rilgan.

Korpusda qo'llanmaning aksar bo'limi uchun to'liq yozuv allaqachon bor, shuning uchun quyidagi daraxt faqat joylashuvni ko'rsatadi: bu korpusning tanlovi, kitobda papka tuzilishi yo'q.

```text
docs/
  guidebook/
    01-context.md               kontekst diagrammasi + aktyorlar ro'yxati
    02-functional-overview.md   kalit funksiya va arxitektura uchun ahamiyatlilari
    03-quality-attributes.md    -> architect 1.4 sifat atributlari va ularni o'lchash
    04-constraints.md           -> architect 1.2 kontekst va cheklovlar
    05-principles.md            -> patterns 26 dizayn printsiplari
    06-software-architecture.md konteyner + komponent diagrammasi, har qutining xulosasi
    07-external-interfaces.md   -> architect 32 tarmoq va integratsiya haqiqati
    08-code.md                  pattern va framework ishlatilishi
    09-data.md                  -> architect 25 sxema dizayni; migratsiya: architect 33
    10-infrastructure.md        -> architect 31 konteyner va cgroup
    11-deployment.md            -> architect 31, 33 reliz va migratsiya
    12-operation-support.md     -> architect 30 kuzatuvchanlik, 35 on-call
  adr/
    0001-...md                  -> Decision Log: 3.1 va 3.8 shu bo'limning o'rnini bosadi
```

Qo'llanma va ADR orasida bitta tirqish qoladi: bir nechta modulga tarqalgan, lekin ADR uchun juda kichik qaror. Ousterhout muammoni aynan shu joyda qo'yadi: ideal holda har bir muhim dizayn qarori bitta sinf ichida yashiringan bo'lardi, lekin haqiqiy tizimda bir nechta sinfga tegadigan qarorlar bo'lmasligi mumkin emas (tarmoq protokolining dizayni jo'natuvchiga ham, qabul qiluvchiga ham tegadi), bunday qarorlar esa murakkab, nozik va ko'p xatoning manbasi. Qiyinligi hujjatning mazmunida emas, joyida: dasturchi uni tabiiy ravishda topadigan joy kerak (Ousterhout, *A Philosophy of Software Design*, 1-nashr, Yaknyam Press, 2018, 13.7).

Ousterhout ikki holatni ajratadi. Agar aniq markaziy joy bo'lsa, hujjat shu yerga qo'yiladi: uning misolida yangi xato holati qo'shish bir nechta faylga tegadi, lekin dasturchi albatta `Status` sanog'ini ochadi, shuning uchun qolgan hamma joyni sanab chiqadigan izoh aynan shu sanoqqa, yangi qiymatlar qo'shiladigan oxirgi qatorga yozilgan (13.7). Agar aniq markaziy joy bo'lmasa (uning misolida bir nechta modulga tarqalgan va bir-biriga bog'liq "zombi server" mantig'i), u markaziy `designNotes` faylini sinab ko'rganini aytadi: fayl aniq nomlangan bo'limlarga bo'linadi, har bo'lim bitta mavzuni oladi, kodda esa qisqa ishora qoladi (13.7). Shu yondashuvni u izohni takrorlashdan qochish qoidasida ham qaytaradi: hujjat uchun aniq bitta joy bo'lmasa, `designNotes` fayli yaratiladi, aks holda mavjud joylarning eng yaxshisi tanlanadi va qolgan joylarda markaziy izohga havola yoziladi (16.4).

Ousterhout bu usulning narxini o'zi aytadi: hujjatning bitta nusxasi bo'ladi va uni topish oson, lekin u o'ziga bog'liq kodning yonida turmaydi, shuning uchun tizim rivojlanganda uni yangilab turish qiyin bo'lishi mumkin (13.7). Shu sababli korpusdagi tartib shunday: chegara yoki texnologiya tanlovi darajasidagi qaror ADR ga, mahsulot darajasidagi bayon guidebook ga, bir nechta moduldagi kodni bir vaqtda o'zgartirishni talab qiladigan mayda qaror esa `designNotes` ga tushadi va kodda unga ishora qoladi.

Quyidagi misol kitobdagi g'oyani Java ga o'tkazadi, kitobda u boshqa tilda berilgan: ro'yxatga yangi qiymat qo'shadigan odam ko'radigan joyga tekshiruv punktlari yoziladi.

```java
public enum PaymentStatus {

    PENDING,
    AUTHORIZED,
    CAPTURED,
    REFUNDED;

    // DIQQAT: yangi holat qo'shilsa, quyidagilar ham o'zgaradi.
    // (1) PaymentStatusMessages: foydalanuvchiga ko'rinadigan matn.
    // (2) PaymentStateMachine.ALLOWED: ruxsat etilgan o'tishlar jadvali.
    // (3) V12__payment_status_check.sql: bazadagi CHECK cheklovi.
    // (4) PaymentStatusDto: tashqi API nomi (eski nomlar o'zgarmaydi).
    // Kesib o'tuvchi qarorning bayoni: docs/designNotes.md, "To'lov holati".
}
```

Qo'llanmaning to'liqlik mezoni ham kerak, aks holda o'n uch bo'lim cheksiz o'sadi. Fairbanks to'xtash qoidasini o'z misolida ko'rsatadi: uzoqdagi yangi developerlarga dizaynni yetkazayotgan jamoa hujjatni yozayotganda uchta asosiy model, ya'ni domen, dizayn va kod modelini, hamda uchta arxitektura ko'rinish turini, ya'ni module, runtime va allocation ko'rinishlarini qoplayotganini kuzatib bordi; har bir qadamdan keyin risk sezilarli kamaydimi degan savol berildi va baho aynan shu qoplash darajasiga tayandi; ish esa asosiy modellar va ko'rinishlar qoplanganda to'xtatildi (*Just Enough Software Architecture*, 4.1.5-bo'lim). Qolgan tafsilotni yangi developerlar o'zi ilib ketadi degan ishonch shu to'xtashning asosi: hujjat skelet beradi, go'shtini kod beradi.

Shu misolda tartib ham bor va u arzonlik bo'yicha: jamoa ishlab chiqarish eng oson hujjatdan boshlab, qimmatroq qismlarni asta qo'shib bordi, va imkon bo'lganda to'liq umumlashgan grafik model o'rniga vakil (representative) va matnli modellarni qurdi; grafik modelni faqat ikki joyda, ya'ni modullar va komponent yig'masi uchun tanladi, chunki ularni qurish nisbatan oson va ular matnli modeldan ko'proq ma'lumot yetkazardi (4.1.5-bo'lim). Korpusdagi tarjimasi: `docs/guidebook/` papkasini matnli ro'yxat va jadval bilan boshlang, diagramma faqat matn chalkash bo'lib qolgan joyda chiziladi.

Uzun yozishdan saqlaning. Brown ning o'z ogohlantirishi: juda chuqur texnik tafsilotga tushish vasvasasiga berilmang, chunki shu darajani tushunadigan texnik odam uni kod bazasidan o'zi topa oladi (47-bob, 147-bet).

Oxirgi e'tiroz avtomatlashtirish tomonidan keladi va uni oldindan yopish kerak. Brown deployment bo'limi haqida yozganda shuni ta'kidlaydi: Puppet, Chef yoki continuous delivery bilan hamma deploy avtomatlashtirilgan jamoalarda ham bu bo'lim foydali bo'lib qoladi, chunki skript nima qilayotganini bir qarashda ko'rsatadigan umumiy manzara skriptning o'zida yo'q (Simon Brown, *Software Architecture for Developers*, Leanpub, 58-bob, 169-bet). Dalil shu bobning boshidagi dalilning aynan o'zi, faqat kod o'rniga infratuzilma kodi qo'yilgan: skriptni o'qib nima bo'layotganini aniqlash mumkin, nega shunday ekanini va qaysi komponent qayerga tushishini esa aniqlab bo'lmaydi. Shuning uchun "bizda hammasi kodda" degan dalil guidebook ning deployment bo'limini bekor qilmaydi: u faqat bo'limning hajmini kichraytiradi, ya'ni bitta jadval va bitta diagramma yetadi.

## 3.20 RFC: dizayn hujjatini fikr yig'ish uchun tarqatish

ADR qabul qilingan qarorni yozib qo'yadi, RFC esa qaror hali chiqmaganda fikr yig'adi. Orosz farqni ochiq qo'yadi: arxitektura hujjatlari qabul qilingan qarorni qayd etish uchun yoziladi va ulardan fikr kutilmaydi, RFC esa aynan fikr olish uchun tarqatiladi (Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 15-bob, 209-bet). RFC "Request for Comments" dan olingan va ko'p kompaniyada shunchaki dizayn hujjati ma'nosida ishlatiladi: muhandis jiddiy ish boshlashdan oldin kontekstni, taklif qilgan yondashuvini va trade-off larni yozib, izoh so'raydi; qat'iy shakl talabi yo'q (207-208-betlar).

Hujjatning asl maqsadi yozish emas, vaqt yutish: kalit fikrni erta olib, loyihani tugatish muddatini qisqartirish (208-bet). Shundan RFC ni ish oqimiga qo'yishning to'rt shakli chiqadi.

| Shakl | Qachon mos keladi | Orosz ning izohi |
|---|---|---|
| Prototip, keyin RFC, keyin qurish | Noma'lum ko'p, masalan yangi framework ustida qurilyapti | Prototip noma'lumlarni ochadi, RFC qisman to'ldirilgan rejani ulashadi |
| RFC, fikrni kutish, keyin qurish | Bog'liqlik ko'p yoki boshqa jamoalar natijaga bog'liq | Hamma manfaatdordan fikr oldin yig'ilsa, umumiy tezlik yuqoriroq bo'ladi |
| RFC, fikr kutilayotganda qurish | Murakkablik bor, lekin ko'p savol kutilmaydi | Fikrni yo'l-yo'lakay singdirish mumkin, o'zgarish kerak bo'lsa ham ko'p vaqt yo'qolmaydi |
| Avval qurish, keyin RFC | Ish allaqachon qilingan yoki ichki qoida talab qiladi | Xatarli: hujjat "katak belgilash" ga aylanadi va jamoa haqiqiy fikrni qabul qilmaydi; Orosz bu shakl amalda ancha keng tarqalganini aytadi |

Yozishning foydasi faqat o'quvchida emas. Orosz to'rt foydani sanaydi: fikringiz tiniqlashadi, chunki hujjat yondashuvingizni o'zingizga ham, boshqaga ham tushunarli qilib aytishga majbur qiladi; muhim fikr tezroq keladi, chunki yetishmagan chekka holat yoki noto'g'ri use case kod yozilgunga qadar aytiladi; g'oyangiz masshtablanadi, chunki hujjat bo'lmasa beshta muhandis sizning fikringizni tushunish uchun beshta alohida suhbat talab qiladi; va jamoada yozish madaniyati tarqaladi (208-209-betlar).

Fikr yig'ishning uch yo'li bor: hujjat ichidagi izohlar orqali asinxron, RFC ni muhokama qiladigan uchrashuv orqali sinxron, va aralash shakl, ya'ni hujjat tarqatiladi va murakkablik yoki izohlar soni talab qilsa uchrashuv chaqiriladi (209-bet). Shaklni loyiha tanlaydi: yigirma jamoaga tegadigan loyiha uchun kerakli yondashuv sizning jamoangiz va bitta hamkor jamoa ishlatadigan servis uchun keraklisidan boshqacha bo'ladi (209-bet).

Korpusdagi joyi oddiy: RFC qaror pishayotgan paytdagi hujjat, [ADR](#31-adr-architecture-decision-record-tuzilishi-kontekst-qaror-oqibat-holat) esa qaror chiqqandan keyingi yozuv. RFC muhokamasida aytilgan e'tiroz va rad etilgan variant ADR ning "Ko'rib chiqilgan variantlar" qismiga ko'chadi, shunda muhokama repoda qoladi va [eskirganini belgilash](#38-adr-ni-repoda-saqlash-raqamlash-va-eskirganini-belgilash) qoidasiga bo'ysunadi.

## 3.21 Muhokama tiqilib qolganda qarorni ochish yo'llari

Ba'zan muhokama sifatli, dalillar yozilgan, lekin guruh ikkiga bo'linib qoladi va qaror chiqmaydi. [Kelishmovchilik qoidasi](#36-jamoadagi-kelishmovchilik-va-rozi-emasman-lekin-bajaraman-qoidasi) e'tirozni shaklga soladi, bu bo'lim esa tiqilishni ochadi. Orosz besh usulni sanaydi (Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 15-bob, 214-bet).

Birinchisi eng kuchlisi: imkoniyat talablarini (capability requirements) yozish. Bu talablar natijani belgilaydi, amalga oshirishni emas. Ular tizim darajasidagi cheklov bo'lishi mumkin, masalan kutilayotgan latency yoki qabul qilinadigan consistency darajasi; UX tomonidagi cheklov, masalan javob vaqti 500 ms dan oshmasligi; yoki biznes cheklovi, masalan ikki marta pul yechish mumkin emasligi. Ular yechimdan oldin yoziladi, shunda har bir taklif shu linza orqali tekshiriladi va "muammoni tushunmasdan yechim rejimiga o'tish" yo'qoladi (214-bet). Korpus tilida bu [sifat atributlari](01-arxitektorning-fikrlash-modeli.md#14-sifat-atributlari-va-ularni-olchash) ning qaror oldidan o'lchanadigan shaklga keltirilishi.

Qolgan to'rttasi tartib bo'yicha: qaror egasi muhokamadan oldin tayinlansin, chunki nizo paytida kiritilgan qaror egasi neytralligi haqidagi savolni ochadi va ishqalanish qo'shadi, ayniqsa ishtirokchi o'z menejerini olib kirsa; eng sodda va adolatli teng hisobni buzuvchi mezon kodni kim yozsa, chunki yechimni keyin u yuritadi; muhokama turib qolganda prototip qurilsin, shunda gap tiqilish haqida emas, ko'rinadigan narsa haqida boradi (prototipni vaqt bilan cheklash [3.5](#35-spike-va-prototip-qarorni-malumot-bilan-quvvatlash) da); va mahsulot tomonidagi hamkordan homiylik olinsin, chunki product manager ham qisqa muddatli yechimdan, ham uzoq muddatli yuritish narxidan manfaatdor (214-bet).

Oxirgi tayanch nuqtasi fikrlashda. Orosz ning qoidasi: dasturiy ta'minotda deyarli har bir qaror keyin qaytariladi, faqat qaytarish narxi har xil, shuning uchun qaytarilishi arzon qaror bo'yicha turib qolgandan ko'ra bittasini tanlab oldinga yurish yaxshiroq (215-bet). Shu yerda yana bitta amaliy talab bor: qarordan qaytilganda nega yondashuv ishlamaganini yozib, tegishli odamlarga tarqatish kerak (215-bet). Korpusda bu yozuv ADR ning `Superseded` holati va [qayta ko'rish](#37-qaror-oqibatini-kuzatish-metrika-va-qayta-korish-sanasi) qismiga tushadi.

## 3.22 Strategik maqsad, printsip va amaliyot: qarorni ramkaga solish

[Mezon jadvali](#32-variantlarni-taqqoslash-mezon-jadvali-va-ogirlik-berish) bitta qarorni taqqoslaydi, lekin mezonning o'zi qayerdan keladi degan savolga javob bermaydi. Newman shu bo'shliqni uch darajali ramka bilan to'ldiradi va sababini aytadi: ba'zi qarorlar to'liq ma'lumot bilan joyida qabul qilinadi, qiyinlari esa to'liq bo'lmagan ma'lumot bilan qabul qilinishi kerak, va shu yerda ramka kerak bo'ladi (Sam Newman, *Building Microservices: Designing Fine-Grained Systems*, 2-nashr, O'Reilly, 2021, 16-bob, "A Principled Approach" bo'limi).

| Daraja | Kim yozadi va nima deydi | Qanchalik tez o'zgaradi |
| --- | --- | --- |
| Strategik maqsad | kompaniya yoki bo'lim: biznes qayerga borayotgani va mijozni qanday xursand qilmoqchi ekani; texnologiya umuman tilga olinmasligi mumkin | kam |
| Printsip | arxitektura roli: maqsadga moslashtirish uchun qo'yilgan qoida, o'ntadan kam bo'lsin | ba'zan |
| Amaliyot | jamoa: printsipni bajarishning aniq, past darajadagi va ko'pincha texnologiyaga bog'liq ko'rsatmasi | tez-tez |

Birinchi daraja arxitektorning ishi emas va Newman buni ochiq aytadi: strategik maqsadni odatda boshqalar belgilaydi, arxitektorning ishi texnologiyani shunga moslashtirish. Maqsad "Janubi-Sharqiy Osiyoga chiqib yangi bozor ochish" yoki "mijoz imkon qadar ko'p narsani o'zi, self-service bilan bajarsin" shaklida bo'ladi, ya'ni yuqori darajali va texnologiyasiz (16-bob, "Strategic Goals"). Agar texnik yo'nalishni siz belgilayotgan bo'lsangiz, bundan amaliy natija chiqadi: biznes tomoni bilan ko'proq vaqt o'tkazib, harakatlantiruvchi tasavvur nima va u qanday o'zgarayotganini bilib turish kerak.

Ikkinchi daraja maqsaddan chiqadi. Newman ikki misol beradi: maqsad yangi funksiyaning bozorga chiqish vaqtini qisqartirish bo'lsa, printsip "yetkazib berish jamoalari o'z dasturining butun hayot tsikliga egalik qiladi va boshqa jamoadan mustaqil chiqaradi" bo'lishi mumkin; maqsad boshqa mamlakatlarda kengayish bo'lsa, printsip "butun tizim lokal deploy qilinadigan darajada ko'chma bo'lishi kerak" bo'ladi, chunki ma'lumot suvereniteti shuni talab qiladi (16-bob, "Principles"). Printsip soni o'ntadan kam bo'lsin: odam ularni eslab qolishi kerak, va soni ko'paygani sayin bir-biriga zid kelish ehtimoli oshadi. Shu yerda Newman printsip bilan cheklovni (constraint) ajratadi: cheklov o'zgartirish deyarli mumkin bo'lmagan narsa, printsip esa biz tanlagan narsa. Uning o'z tavsiyasi ikkisini bitta ro'yxatda ushlash, chunki shunda cheklov vaqti-vaqti bilan qayta so'roq qilinadi va u haqiqatan qo'zg'almas ekani tekshiriladi.

Uchinchi daraja printsipni ishga aylantiradi. Amaliyot batafsil va amaliy ko'rsatma bo'ladi, odatda texnologiyaga bog'liq, va har bir dasturchi tushunadigan darajada past bo'lishi kerak: kod yozish qoidalari, barcha log ma'lumotining markazda yig'ilishi, integratsiyaning standart shakli HTTP/REST ekani (16-bob, "Practices"). Printsip va amaliyot orasidagi bog'lanish aniq bo'lishi kerak: "jamoa butun hayot tsiklini boshqaradi" printsipi "har bir servis izolyatsiyalangan hisobga deploy qilinadi" amaliyotiga aylanadi. Bitta odamning printsipi boshqasining amaliyoti bo'lishi mumkin va Newman bunga e'tiroz bildirmaydi: kichik jamoada ikkisini birga yozish ham yetarli, katta tashkilotda esa turli joyda turli amaliyot bo'lib, hammasi bitta printsip to'plamiga bog'lanadi, masalan .NET jamoasida bir xil, Java jamoasida boshqa xil amaliyot (16-bob, "Combining Principles and Practices").

Ramkaning qiymati uning hajmida: Newman keltirgan haqiqiy misolda maqsad, printsip va amaliyot bitta varaqqa sig'adi, o'ng tomondagi amaliyotlar bir-ikki yilda muntazam o'zgaradi, printsiplar esa deyarli o'zgarmasdan turadi (16-bob, "A Real-World Example").

```text
Strategik maqsad          Printsip                        Amaliyot
------------------------  ------------------------------  ------------------------------
Yangi funksiya bozorga    Jamoa o'z servisining butun     Har servis o'z sxemasi va
tezroq chiqsin            hayot tsikliga egalik qiladi    o'z Flyway papkasi bilan
                                                          Kelishuvsiz chiqarish: bitta
                                                          servis, bitta pipeline

Mijoz o'zi bajarsin       Har imkoniyat API orqali        OpenAPI shartnomasi avval
                          ochiladi                        yoziladi, keyin kod
                                                          Xato javobi yagona formatda

Ma'lumot mamlakatda       Tizim lokal deploy              Konfiguratsiya muhitdan,
qolsin                    qilinadigan bo'lsin             kodda region nomi yo'q
```

Oxirgi qadam amaliyotni bajarilishi oson qilish. Newman ning formulasi "to'g'ri ishni qilish oson bo'lsin": amaliyotni qo'llab-quvvatlovchi hujjat bo'lsin, undan ham yaxshisi ishlaydigan namuna kod bo'lsin, platforma esa amaliyotga ergashishni eng oson yo'lga aylantirsin va amaliyot o'zgarganda platforma ham o'zgarsin (16-bob, "A Real-World Example"). Korpusda bu mexanizmlar [standart o'rnatish](36-code-review-va-jamoada-texnik-yetakchilik.md#369-standart-ornatish-linter-formatlash-archunit-qoidalari-shablon-loyiha) bo'limida: linter, ArchUnit qoidasi va shablon loyiha aslida yozilgan amaliyotning majburlangan shakli. Ramkaning o'zi esa [ADR](#31-adr-architecture-decision-record-tuzilishi-kontekst-qaror-oqibat-holat) ni almashtirmaydi: ADR bitta qarorni yozadi, ramka esa shu qarorning kontekst qismiga nima yozilishini belgilaydi.

## 3.23 Trade-off tahlilining ikki qadami: chalkash o'lchamlarni topish va birikmani modellash

[Mezon jadvali](#32-variantlarni-taqqoslash-mezon-jadvali-va-ogirlik-berish) tayyor mezonlar bilan ishlaydi. Lekin notanish muammoda mezonning o'zi ma'lum bo'lmaydi, va *The Hard Parts* ning oxirgi bobi aynan shu holat uchun: mualliflar kitobdagi umumiy tahlil to'liq emasligini aytib, o'quvchiga o'z muammosiga chalkashgan elementlar uchun qo'shimcha ustun qo'shishni tavsiya qiladi (Neal Ford va boshqalar, *Software Architecture: The Hard Parts*, 1-nashr, O'Reilly, 2021, 15-bob, 400-bet). Ularning jarayoni uch qadamdan iborat: qaysi qismlar bir-biriga chalkashganini topish, ular qanday bog'langanini tahlil qilish, keyin o'zaro bog'liq tizimlarda o'zgarishning ta'sirini aniqlab kelishuvlarni baholash (15-bob, 400-bet). Birinchi ikkisi ish hajmining ko'pini oladi.

**Birinchi qadam: chalkash o'lchamlarni topish.** Savol bitta va u ataylab eng sodda shaklda qo'yilgan: kimdir X ni o'zgartirsa, bu Y ni ham o'zgartirishga majbur qiladimi (15-bob, 401-bet). Javobni yig'adigan vosita statik bog'liqlik diagrammasi. Universal asbob yo'q, chunki har bir arxitektura o'ziga xos, lekin jamoa uni qo'lda yoki avtomatlashtirish bilan o'zi qura oladi. Mikroservis uchun kitob yig'ilishi kerak bo'lgan ma'lumotni sanab beradi: operatsion tizim va konteyner bog'liqliklari; tranzitiv bog'liqlik boshqaruvi orqali keladigan framework va kutubxonalar; baza, qidiruv dvigateli va bulut muhitiga persistent bog'liqliklar; servis o'zini ko'tarishi uchun kerak bo'lgan integratsiya nuqtalari; aloqa uchun kerak bo'lgan messaging infratuzilmasi (15-bob, 401-bet).

Diqqat qiladigan chegara ham bor: statik bog'liqlik diagrammasi faqat workflow aloqasi bilan bog'langan kvantlarni hisobga olmaydi. Kitobning misoli: `AssignTicketService` workflow ichida `ManageTicket` bilan ishlaydi, lekin boshqa bog'lanish nuqtasi bo'lmasa, ular statik mustaqil, workflow davomida esa dinamik bog'langan bo'ladi (15-bob, 401-bet). Statik va dinamik bog'liqlik farqining korpusdagi yozuvi [bog'liqlik turlari](05-abstraksiya-hissi-bogliqlik-va-chegaralar.md#54-bogliqlik-turlari-malumot-vaqt-joylashuv-sxema-boyicha-bogliqlik) bo'limida.

Muhiti avtomatlashtirish bilan qurilgan jamoa uchun kitob arzon yo'l ko'rsatadi: tizim qurilayotganda bog'liqlik nuqtalarini hujjatlashtirishni shu generativ mexanizmga qo'shish (15-bob, 401-bet). Spring loyihasida bu bitta CI qadami bo'lib qoladi.

```bash
# Statik bog'liqlik ro'yxatini qo'lda yozmaslik uchun: har reliz uchun bitta fayl.
# Har bir manba kitob sanagan toifalardan biriga mos keladi.
mvn -q dependency:tree -DoutputFile=target/coupling-libs.txt       # kutubxona va tranzitivlar
grep -rhoE 'jdbc:[a-z]+://[^"]+' src/main/resources > target/coupling-db.txt   # persistent
grep -rhoE 'spring\.kafka\.bootstrap-servers.*' src/main/resources > target/coupling-msg.txt
grep -rhoE '^[A-Z_]+_URL=.*' .env.example > target/coupling-integration.txt    # integratsiya
awk 'FNR==1{print "== " FILENAME}1' target/coupling-*.txt > target/static-coupling.md
```

**Ikkinchi qadam: bog'liqlik nuqtalarini modellash.** Chalkash nuqtalar topilgandan keyin mumkin bo'lgan birikmalar yengil shaklda modellanadi, ya'ni og'ir prototip emas, qog'ozdagi variantlar. Kitobning amaliy maslahati tejamkor: birikmalarning bir qismi umuman amalga oshmaydi, ularni modellamasdan tashlab ketish mumkin (15-bob, 402-bet). Maqsad ham aniq aytilgan: qaysi kuchlar haqiqatan trade-off tahlilini talab qilishini aniqlash. Kitobning o'zida bu baho jadvaliga aylanadi, unda har bir pattern uchun aloqa, izchillik va muvofiqlashtirish qiymatlari hamda bog'liqlik darajasi, murakkablik, javob berish va masshtab baholari turadi (15-bob, 402-bet).

Modellashning qiymati jadvalni to'ldirgandan keyin ko'rinadi. Mualliflar sakkiz patternni yonma-yon qo'yib ikki bog'lanishni topdi: bog'liqlik darajasi bilan masshtab orasida teskari korrelyatsiya (workflow da servis ko'p bo'lsa, masshtabni loyihalash qiyinlashadi) va bog'liqlik bilan javob berish hamda mavjudlik orasida shunga o'xshash, kuchsizroq bog'lanish (servis ko'p bo'lsa, bittasining nosozligidan butun workflow yiqilish ehtimoli oshadi) (15-bob, 403-bet). Bunday kuzatuv alohida variantni o'qiganda ko'rinmaydi, faqat matritsada ko'rinadi.

Uchinchi qadam qisqa, chunki unga kirishdan oldin ish bajarilgan bo'ladi: avval tub o'lchamni fiksatsiya qilish kerak, masalan aloqa sinxron yoki asinxron bo'lishi, chunki bu tanlov keyingi imkoniyatlarni darhol cheklaydi; keyin shu cheklov ostida tahlil takrorlanadi va chalkash o'lchamlar tugaganda qolgan ish dizayn bo'ladi (15-bob, 403-404-betlar). Yana bir ogohlantirish mezonning turiga tegishli: kitobning trade-off jadvallari deyarli hammasi sifat (qualitative) baholari, chunki ikki arxitektura hech qachon haqiqiy miqdoriy taqqoslashga yetarli darajada o'xshash bo'lmaydi; shuning uchun mualliflar sifat tahlilini ko'nikma sifatida mashq qilishni tavsiya qiladi (15-bob, 404-bet).

ESLATMA: yuqoridagi `bash` qadamlari shu korpusning misoli. Kitob statik bog'liqlik uchun yig'iladigan ma'lumot toifalarini beradi, aniq buyruqlarni bermaydi.

## 3.24 Model va kod sinxronligi: toqat qilinadigan nomuvofiqlik va strategiyalar

["Kodda shunday qilasizmi" sinovi](#316-kodda-shunday-qilasizmi-sinovi-va-model-bilan-kod-orasidagi-uzilish) bo'limi model-kod uzilishini nomlaydi. Keyingi savol amaliy: uzilish bilan nima qilish kerak. Fairbanks birinchi navbatda eng keng tarqalgan xato reaksiyani rad etadi. Uzilish haqida bilgan ba'zi odam qiyinlikni arxitektura abstraksiyalaridan butunlay voz kechish uchun imkoniyat deb ko'radi va tanish yerga chekinadi; Fairbanks buni big ball of mud arxitekturasidan bir qadam narida deb baholaydi, chunki abstraksiyalar aynan murakkablik va hajmni ushlab turish uchun mavjud, va sinflar dengizini boshqarish ehtimol undan ham qiyinroq (*Just Enough Software Architecture*, 10.1-bo'lim). Uzilishning sababi ham shu yerda: arxitektura modellari abstrakt va intensional bo'lgani uchun murakkablik haqida fikrlashga yaraydi, kod esa konkret va ekstensional bo'lgani uchun mashinada bajariladi; shuning uchun yaqin kelajakda umumiy yechim kutilmaydi.

Chekinish ishlamasa, uzilishni boshqarish kerak. Fairbanks ikki yo'lni sanaydi: mexanik, ya'ni yuqori darajadagi tilda yozib kod generatsiya qilish (Model Driven Engineering), va qo'lda, ya'ni developer ikkisini ham tushunib izchillikni o'zi ta'minlashi (10.1-bo'lim). Mexanik yo'l ayrim domenlarda amaliy, lekin MDE ning katta tasavvuri hali keng qo'llashga tayyor emas. Qo'lda boshqarish ikki qadamdan iborat: avval tasodifiy murakkablikni olib tashlash, ya'ni arxitektura elementlarini dasturlash tili elementlariga moslashtirish va arxitektura tushunchalarini kodda ifodalash, keyin modellarni vaqti-vaqti bilan kod bilan sinxronlash. Birinchi qadam [arxitektura niyatini kodda qoldirish](04-kod-muloqot-vositasi-nomlash-aniqlik.md#411-architecturally-evident-coding-style-arxitektura-niyatini-kodda-qoldirish) bobida, ikkinchisi shu yerda.

Hamma nomuvofiqlik bir xil emas va Fairbanks mezonni beradi: ayrim nomuvofiqliklar toqat qilinadi, lekin bu nomuvofiqlikning tabiatiga bog'liq (10.2-bo'lim). Uning ikki misoli chegarani ko'rsatadi. Modelingiz online unumni tasvirlasa, offline statistik tahlil uchun qo'shilgan kod o'sha modelni buzmaydi, ya'ni nomuvofiqlik zararsiz. Buning qarshisida: ko'p threadli kodga kiritilgan ko'rinishdan arzimas o'zgarish konkurentlik modelingizni buzadi. Korpusdagi amaliy qoida shundan chiqadi: modelni "qancha eski" emas, "qaysi da'vosi hali rostmi" bo'yicha baholash kerak, va bu da'volar yozilgan bo'lsa tekshirish arzon.

Sinxronlash strategiyalari esa aniq ro'yxat va Fairbanks ularni amalda uchraydigan shaklda sanaydi (10.2-bo'lim).

| Strategiya | Nima qilinadi | Amalda |
| --- | --- | --- |
| Divergensiyani e'tiborsiz qoldirish | eski model ishlatiladi, farqlar esda tutiladi va taqdimotda og'zaki aytiladi | kutilganidan ko'ra keng tarqalgan |
| Ad hoc modellashtirish | model kerak bo'lganda, ko'pincha doskada qayta yaratiladi | agile jamoalarda ko'p |
| Faqat yuqori darajadagi model | arxitekturaning eng fundamental qismlari sekin o'zgaradi, shuning uchun faqat ular saqlanadi | keng tarqalgan |
| Hayot tsikli bosqichida sinxronlash | iteratsiya, bosqich yoki reliz oxirida model yangilanadi | niyat yaxshi, lekin cheksiz kechiktirilishi odatiy |
| Inqirozda sinxronlash | dizayn muammosi, hamkorlik muammosi yoki review oldidan shoshilinch tiklanadi | ajablanarli darajada ko'p |
| Doimiy sinxronlash | model va kod har doim mos ushlanadi | qimmat va kam uchraydi |

Ro'yxatdan uchinchi qoida chiqadi: abstraksiya darajasi divergensiyaga chidamlilikni belgilaydi. Fairbanks buni umumiy qilib aytadi, ya'ni model qanchalik umumiy yoki abstrakt bo'lsa, koddagi o'zgarishni shunchalik yaxshi hazm qiladi, va misol beradi: faqat client va server ni tasvirlaydigan arxitektura modeli koddagi o'zgarishga juda chidamli (10.2-bo'lim). Shundan amaliy tanlov tug'iladi va u keng tarqalgan: loyiha yuqori darajadagi diagrammalarni yangilab turadi va tafsilotni ad hoc modellashtiradi, shu bilan hujjat yukini minimallashtiradi, lekin yangi developer uchun va boshqa jamoa bilan muloqot uchun bir nechta diagrammani saqlab qoladi. Teskari tomoni ham bor: tafsiloti ko'p model divergensiyani tezroq yig'adi va ko'proq sinxronlash kuchi talab qiladi.

Strategiyani tanlash uchun Fairbanks uch mezonni beradi (10.2-bo'lim): asbob yoki yuqori darajadagi tildan foydalanish uzilish va divergensiyani kamaytiradi hamda sinxronlash kuchini tushiradi; tafsilot darajasi divergensiya tezligini belgilaydi; va loyihangizning chetga chiqishga toqati, ya'ni model qachon kodni aniq aks ettirishi kerak va undan kim foydalanadi. Oxirgi mezon eng kuchlisi: xavfsizlik modeli kodga yaqin mos kelmasa foydasiz bo'lishi mumkin, [architecture driver](02-muammoni-tushunish-va-togri-savol-berish.md#218-sifat-atributi-ssenariysi-qa-scenario-va-architecture-driver) larni sanaydigan model esa bir oz eskirganda ham qiymatini saqlaydi.

## 3.25 Texnika tartibi: arzondan boshlash, integratsiyani birinchi tekshirish va iteratsiya nol

[Texnikani riskka moslash](01-arxitektorning-fikrlash-modeli.md#118-texnikani-riskka-moslash-tur-mosligi-toplam-va-toxtash-qoidasi) bo'limi qaysi texnika kerakligini hal qiladi. Qolgan savol tartib haqida: bir nechta texnika kerak bo'lsa, qaysi biri birinchi.

**Eng arzon texnikadan boshlab, risk pasayguncha qimmatroq qo'shish.** Fairbanks buni o'z misolining ichida qoida sifatida beradi. Uning jamoasi muvaffaqiyatli prototipni mahsulotga aylantirayotgan va loyihaga uzoqdagi yangi developerlar qo'shilayotgan paytda bitta riskni nomladi: shoshilinch ishda yangi developerlar dizaynga zid kod yozib qo'yishi, ya'ni arxitektura eroziyasi yoki architectural drift (*Just Enough Software Architecture*, 4.1-bo'lim; atama Perry va Wolf, 1992 dan). Riskni kamaytirish uchun dizaynni yetkazishga qaror qilindi, va tartib aniq: eng kam qimmat texnikadan boshlanadi, keyin risk pasaygan deb o'ylaguncha qimmatroqlari tanlanadi. Birinchi nomzod manba kodini o'qitish bo'ldi, chunki kod allaqachon bor va hozirgi jamoadan vaqt talab qilmaydi; lekin Fairbanks uning chegarasini ham o'lchadi: papka tuzilishi ishora beradi, lekin har bir papka modulga to'g'ri keladi deb o'ylash xato bo'lardi va papka tuzilishi modul bog'liqligini umuman ifodalay olmaydi. Xulosa: kod modul ko'rinishini qoniqarli, kod modelini yaxshi yetkazadi, runtime va allocation ko'rinishlarini hamda domen va dizayn modellarini esa yomon yetkazadi, shuning uchun navbatdagi texnika kerak bo'ladi.

**O'zaro bog'liq risklar bo'lsa, avval integratsiyani tekshirish.** Fairbanks ning ikkinchi misoli tartibning sababini ko'rsatadi. Jamoa ikki yangi tashqi komponentni (COTS) qo'shishi kerak bo'lganda to'rt risk sanaldi: integratsiya, ishonchlilik, ekranda ko'rsatish va latency. Fairbanks risklarning o'zaro bog'liqligini qayd qiladi va tartibni shundan chiqaradi: integratsiya muammosini qanday yechish ishonchlilik va latency ga ta'sir qiladi, shuning uchun avval integratsiya tekshiriladi, chunki yangi komponentlarni integratsiya qilish mumkin bo'lmasa latency va ishonchlilik tahlilini boshlashning ma'nosi yo'q (4.2-bo'lim). Korpusdagi shakli: spike larni ketma-ketlikka qo'yganda birinchi spike eng ko'p keyingi ishni bekor qilishi mumkin bo'lgani bo'lsin.

**Integratsiyani tekshirishda nimani izlash kerak.** Fairbanks javobni architectural mismatch katalogi bilan beradi. Atama Garlan boshchiligidagi jamoa mavjud qismlardan tizim yig'ganda paydo bo'ldi va ularning qiyinchiliklari tanish: kod shishishi, sekin bajarilish, qayta implementatsiya qilingan funksiyalar, konkurentlik qiyinchiliklari va xatoga moyil kompozitsiya. Ularning hissasi integratsiyaning qiyinligini qayd qilishdan tashqariga chiqdi: ikki dasturiy qismni nomos qiladigan arxitektura xossalarini toifalarga ajratdi (15.7-bo'lim; Garlan, Allen va Ockerbloom, 1995).

- **Komponent haqidagi taxminlar:** infratuzilma, nazorat kimda, ma'lumotdan qanday foydalaniladi.
- **Connector haqidagi taxminlar:** protokollar, uzatiladigan ma'lumotning tuzilishi.
- **Tizim haqidagi taxminlar:** tizim topologiyasi, komponentning mavjudligi yoki yo'qligi.
- **Qurilish jarayoni haqidagi taxminlar:** initsializatsiya ketma-ketligi.

Fairbanks maqoladagi tavsiyalardan faqat bittasini amaliy deb ajratadi: arxitektura taxminlarini ko'rsatadigan modellar qurish. Model muammoli taxminni ko'rsatganda nomoslikni erta sezasiz va ikki yo'ldan birini tanlaysiz, ya'ni mos keladigan boshqa COTS olasiz yoki o'z dizayningizni o'sha taxminlarga moslashtirasiz. Joyi ham muhim: taxminlarni qayerda yozish konseptual jihatdan farq qilmaydi, lekin amalda ularni to'g'ridan-to'g'ri arxitektura diagrammasiga izoh (UML note) sifatida qo'yish kerak, aks holda ular osongina e'tibordan chetda qoladi. Fairbanks ning o'z misolida video komponenti haqidagi uchta taxmin shunday yozildi: u displey ni o'zi initsializatsiya qilmaydi, displey dan faqat o'zi foydalanayotganini taxmin qiladi, va buyruqlarni polling bilan oladi (4.2.1-bo'lim).

**Ma'lum risklar iteratsiya nolda yopiladi.** Agile jarayonda tartib savoli boshqa shaklda qaytadi: arxitektura risklarini qachon ishlash kerak. Fairbanks javobni uch qismga ajratadi (3.11-bo'lim). Loyiha boshida bilingan risklar, masalan arxitektura uslubi, framework va boshqa COTS komponentlarning tanlovi, vaqt bilan cheklangan iteratsiya nolda hal qilinadi: ba'zi jamoalar iteratsiya nolni muhitni sozlashga, ya'ni versiya nazorati va avtomatik build ga ishlatadi, va aniqlangan risklarni kamaytirishni shu yerga ulash mumkin. Uning misollari arzon: uslub bo'yicha hamma kelishganini tasdiqlash uchun oddiy doska yig'ilishi, yoki muhim bo'lgan COTS komponentning unum ko'rsatkichlari noma'lum bo'lsa, taxminiy tezlik va o'tkazuvchanlik raqamlarini olish uchun tez prototip. Kichik risklar iteratsiya ichida yuzaga chiqqanda hal qilinadi va backlog ga umuman tushmaydi, kattalari esa feature lar bilan bir qatorga qo'yilib, birlashgan feature va risk backlog iga kiritiladi.

Fairbanks shu yerda aniq taqiqni ham qo'yadi: bu nominal iteratsiya nolni amaldagi Big Design Up Front ga aylantirish uchun bahona emas; iteratsiya nolning vaqtini uzaytirish o'rniga risklar backlog ga suriladi (3.11-bo'lim). Birlashgan backlog ning bitta oqibati bor: feature va risk birga ustuvorlashtiriladi, shuning uchun developerlarning ishiga product owner ga texnik riskni tushuntirish ham qo'shiladi, masalan backlog ning quyi qismida turgan xavfsizlik ishi keyin qo'shilishi qiyin yoki mumkin emas ekanini aytish.

## 3.26 Qaror, printsip va istisno: governance mexanikasi

[Strategik maqsad, printsip va amaliyot](#322-strategik-maqsad-printsip-va-amaliyot-qarorni-ramkaga-solish) bo'limi ramkani beradi. Ramkadan keyin uchta mexanika qoladi: qaror bilan printsipning majburiylik darajasi qanday farq qiladi, istisno bilan nima qilinadi, va buni kim yuritadi.

**Qaror qoida, printsip yo'riqnoma.** Richards va Ford farqni majburiylik orqali qo'yadi: arxitektura qarori tizim quriladigan qoida, design principle esa qat'iy qoida emas, yo'riqnoma (*Fundamentals of Software Architecture*, 1-bob, "Defining Software Architecture"). Ularning misoli aniq: "servislar orasida asinxron messaging ishlatilsin" printsipi unum uchun afzal yo'lni ko'rsatadi, lekin developer vaziyatga qarab REST yoki gRPC kabi mosroq protokolni tanlashiga yo'l qoldiradi; arxitektura qarori esa servislar orasidagi aloqaning har bir shart va variantini qoplab bo'lmaydi, shuning uchun bu yerda printsip kerak bo'ladi. Shundan amaliy belgi chiqadi: gapni "shunday qilinadi" deb yozib bo'lmasa, u qaror emas, printsip, va u holda ADR o'rniga printsip ro'yxatiga yoziladi.

**Qarorni buzish rasmiy yo'l bilan bo'ladi.** Richards va Ford qarorning qoida ekanini oxiriga yetkazadi: agar arxitektura qarori tizimning bir qismida qaysidir shart yoki cheklov sababli bajarilmasa, u qaror variance deb atalgan narsa orqali buzilishi mumkin, va ko'pchilik tashkilotda variance modellari bor; ularni architecture review board (ARB) yoki chief architect yuritadi, va model aniq standartga yoki arxitektura qaroriga variance so'rash jarayonini rasmiylashtiradi (1-bob). Natija ikki tomonli bo'ladi: istisno asos va trade-off larga qarab tahlil qilinadi, keyin tasdiqlanadi yoki rad etiladi. Korpusdagi tarjimasi: ARB bo'lmasa ham mexanizm kerak, va uning eng arzon shakli istisno so'ralgan ADR ga "variance" bo'limi qo'shish, unda qaysi qism, qaysi muddatga va qanday asosga ko'ra chetga chiqayotgani yozilishi.

**Istisnolar jurnalga yoziladi va amaliyotni o'zgartiradi.** Newman shu nuqtani printsip va amaliyot ramkasining davomi qilib beradi: printsip va amaliyot tizim qanday qurilishini boshqaradi, lekin tizim ulardan chetga chiqsa nima bo'ladi degan savol qoladi, va ba'zan qaror shunchaki qoidaga istisno bo'ladi; shu holatda qarorni keyingi murojaat uchun biror jurnalga yozib qo'yish o'rinli (*Building Microservices: Designing Fine-Grained Systems*, 2-nashr, 16-bob, "Exception Handling"). Mexanizmning asl qiymati esa teskari yo'nalishda: istisnolar yetarlicha yig'ilsa, tegishli printsip yoki amaliyotning o'zini dunyo haqidagi yangi tushunishga moslab o'zgartirish ma'noga ega bo'ladi. Newman ning misoli qisqa: amaliyot "ma'lumotni saqlash uchun doim MySQL ishlatamiz" bo'lgan, keyin yuqori masshtablanadigan saqlash uchun Cassandra ning asosli sabablari ko'rindi, va amaliyot "ko'pchilik saqlash talabi uchun MySQL, hajmda katta o'sish kutilsa Cassandra" ga o'zgartirildi.

Istisno kuzatuvining narxi tashkilotga bog'liq va Newman ikki uchini ham aytadi: developer jamoalariga ishonch yuqori va printsiplar yengil bo'lgan kompaniyalarda ochiq istisno kuzatuviga ehtiyoj sezilarli kamayadi, ba'zan umuman qolmaydi; developerlar erkinligi kam bo'lgan qattiq tashkilotda esa istisnolarni kuzatish o'rnatilgan qoidalar odamlar duch kelayotgan muammolarni to'g'ri aks ettirishini ta'minlash uchun hayotiy bo'lishi mumkin (16-bob). Ya'ni istisno jurnali o'zi maqsad emas, u qoidalarning haqiqat bilan aloqasini tekshiradigan asbob.

**Governance guruhi asosan ish bajaruvchilardan iborat bo'lsin.** Newman governance ni uch ishga ajratadi: keng ma'noda narsalar qanday qilinishi kerakligiga kelishish, odamlar buni bilishini ta'minlash, va narsalar shunday bajarilishini ta'minlash (16-bob, "Governance and the Paved Road"). Uning talabi esa guruhning tarkibiga tegishli: governance tub mohiyati bilan guruh faoliyati bo'lishi kerak, va agar rasmiy guruh kerak bo'lsa, u asosan boshqarilayotgan ishni bajarayotgan odamlardan iborat bo'lishi hamda texnik xavflarni kuzatish va boshqarish uchun javobgar bo'lishi kerak. Ikkinchi talab yuritishning shakliga tegishli: odamlar ko'rsatmaga ergashayotganini tekshirib yurish zerikarli ish, shuning uchun to'g'ri ishni qilish oson bo'lishi kerak; arxitektorning roli yo'nalishni aniq aytish va unga yetishni osonlashtirish, demak u qurilayotgan paved road ning talablarini shakllantirishda qatnashishi kerak, va ko'pchilik tashkilotda bunga eng katta misol platforma bo'lib, arxitektor platforma jamoasi uchun muhim manfaatdorga aylanadi.

**Governance maqsadlar to'qnashganda kerak bo'ladi.** Newman migratsiya misolida mexanikaning nega zarurligini ko'rsatadi: trafikning sezilarli o'sishini ko'tarish uchun arxitekturani qayta qurish kerak bo'lgan paytda kimdir jamoa avtonomiyasini oshirishni, boshqasi yangi tilni sinab ko'rishni qo'shadi, va bilmasdan avtonomiya, masshtab hamda yangi texnologiyani bir vaqtda joriy qiladigan katta o'zgarish dasturi paydo bo'ladi (*Monolith to Microservices*, 2-bob, 45-46-betlar). Zarar aniq: faqat masshtabga qarasangiz, migratsiya davomida mavjud monolitni gorizontal masshtablash yaxshiroq ekani ma'lum bo'lishi mumkin, lekin bu yangi ikkilamchi maqsadlarga yordam bermaydi, shuning uchun mikroservis yondashuv sifatida qulflanib qoladi. Newman ning qoidasi: asosiy haydovchini ikkilamchi foydalardan ajratish, va ikkilamchi maqsad asosiy maqsadga xalaqit berganda yoki undan diqqatni tortganda orqa o'rinni olishi. Uning usuli ham arzon: har bir istalgan natijani slider deb ko'rish, hammasi o'rtadan boshlanadi, va bittasini muhimroq qilganda boshqasining ustuvorligi tushishi shart; natijada "polyglot programming ni osonlashtirish ishonchlilikni oshirishdan muhim emas" shaklidagi gap yozma shaklga keladi va keyingi qarorlarni osonlashtiradi. Ustuvorliklar o'zgarishi mumkin va o'rganilgan narsaga qarab o'zgarishi kerak, lekin ularning yozilgan bo'lishi avtonom jamoalarga lokal qarorni kompaniya maqsadiga moslashtirishga yordam beradi.

ESLATMA: variance ni ADR ga alohida bo'lim sifatida qo'shish va istisno jurnalini ADR papkasining yonida ushlash shu korpusning tanlovi. Richards va Ford variance modelining shaklini bermaydi, Newman esa jurnalning joyini "biror jurnal" deb qoldiradi.

## 3.27 Amalda qo'llash

- [ ] `docs/adr/` papkasini va `template.md` shablonini repoga qo'shing, raqamlash skriptini ishga tushiring.
- [ ] Yaqin o'tmishdagi eng katta qarorlarni retrospektiv ADR sifatida yozing va retrospektiv ekanini ochiq belgilang; tanlash mezoni "Rule 5" dan: qaror sifat talabiga erishish uchun kalit bo'lgan, uzoq muhokama talab qilgan yoki prototip bilan tekshirilgan bo'lsa, u yozishga arziydi.
- [ ] Har bir ochiq ADR ga qaror egasining ismini va qayta ko'rish sanasini qo'ying, egasiz ADR ni merge qilmang.
- [ ] CI ga ikki tekshiruv qo'shing: `Holat` qatori majburiy, muddati o'tgan qayta ko'rish sanalari ro'yxati haftalik chiqsin.
- [ ] Keyingi arxitektura qarori uchun variantlar ro'yxatini MECE qilib tekshiring (bir-birini qoplamasin, ochiq variant qolmasin), keyin trade-off jadvalini sifat darajalari bilan to'ldiring.
- [ ] Hozir muhokamada turgan bitta savolni spike ga aylantiring: savol, vaqt chegarasi va javob mezonini yozib qo'ying.
- [ ] Har bir qabul qilingan ADR uchun bitta Micrometer metrikasi va bitta alert chegarasini kod bilan birga joylashtiring.
- [ ] Jamoa bilan "rozi emasman, lekin bajaraman" qoidasini kelishib oling va rad etilgan e'tirozlarni ADR ichida saqlaydigan bo'lim qo'shing.

## Manbalar

- Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani, *Software Architecture: The Hard Parts*, 1-nashr, O'Reilly, 2021 (copyright 2022), 1-bob, 5-bet - ADR ni Michael Nygard blog postida targ'ib qilgani va Thoughtworks Technology Radar da "adopt" belgisini olgani; ADR odatda bir-ikki bet; AsciiDoc, Markdown yoki wiki shabloni; sarlavha qisqa ot iborasi, Kontekst muqobillarni sanaydi, Qaror asoslashni o'z ichiga oladi, Oqibatlar trade-off larni yozadi
- Neal Ford va boshqalar, *Software Architecture: The Hard Parts*, 1-nashr, 2021, 1-bob, 5-7-betlar - qarorni hujjatlash va uning qo'llanishini boshqarish ikki alohida ish; fitness function "obyektiv butunlik bahosi"; "yuqori unumli" yaramaydi, o'lchanadigan qiymat kerak
- Neal Ford va boshqalar, *Software Architecture: The Hard Parts*, 1-nashr, 2021, 2-bob, 26-27-betlar - murakkab real tizimlar uchun universal qoida yo'q, best practice mavjud emas; ATAM kabi metodikalar kundalik muammolardan uzoq; trade-off tahlilining uch qadami
- Neal Ford va boshqalar, *Software Architecture: The Hard Parts*, 1-nashr, 2021, 15-bob, 399-412-betlar - sifat darajali trade-off jadvali (402-403-betlar, Table 15-1 va Table 15-2); MECE ro'yxati (404-405-betlar); kontekstdan chiqib ketish tuzog'i (405-407-betlar); domen ssenariylarini modellashtirish (408-409-betlar); dalilni kalit nuqtalarga qisqartirish (410-bet)
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, 1-nashr, O'Reilly, 2020, 1-bob - birinchi qonun: arxitekturada hamma narsa trade-off; Corollary 1: trade-off topilmagan bo'lsa u hali topilmagan; ikkinchi qonun: "why" "how" dan muhimroq
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, 1-nashr, 2020, 2-bob - trade-off tahlili afzallik va kamchilik jadvali bilan yoziladi va javob "it depends" bo'ladi; Rich Hickey ning gapi: dasturchi foydani biladi, arxitektor trade-off ni ham bilishi kerak
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, 1-nashr, 2020, 6-bob - obyektiv ta'rif bo'lmasa xarakteristika haqida muhokama bo'lmaydi; o'rtacha outlier ni yashiradi; maqsad qiymat o'zboshimchalik bilan emas, statistik tahlil bilan qo'yiladi
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, 1-nashr, 2020, ilova "Self-Assessment Questions", 19-bob savollari - 19-bobda ADR ning besh asosiy bo'limi borligi, asoslash Qaror bo'limida turishi, alohida Alternatives bo'limi bo'lmasa muqobillar Kontekst da sanalishi, Proposed holatining uch mezoni, va "covering your assets" hamda "email-driven architecture" antipatternlarining nomlari
- Paul Clements, Felix Bachmann, Len Bass, David Garlan va boshqalar, *Documenting Software Architectures: Views and Beyond*, 2-nashr, Addison-Wesley, 2010, Prolog, 44-bet ("Rule 5: Record Rationale") - eng muhim qarorlar uchun sababni yozish; rad etilgan muhim muqobillarni va rad sababini yozish; sababni yozishga arziydigan uch holat (sifat talabiga erishish uchun kalit qaror, uzoq muhokama talab qilgan qaror, eksperiment yoki prototip bilan baholangan qaror)
- Paul Clements va boshqalar, *Documenting Software Architectures: Views and Beyond*, 2-nashr, 2010, Prolog, 44-45-betlar ("Rule 6") - eskirgan hujjat ishlatilmaydi, yangilanib turgan hujjat ishlatiladi
- Paul Clements va boshqalar, *Documenting Software Architectures: Views and Beyond*, 2-nashr, Addison-Wesley, 2010, Prolog, P.4 (26-27-betlar) - uslub tanlashning hujjatlashtirish majburiyati (kiritgan ixtisoslashish, cheklovlar va berayotgan xususiyatlar; adabiyotdagi ta'rifga havola yoki o'z style guide i); bir element ikki ko'rinishda chiqsa u ko'priklovchi element (bridging element) bo'lishi va unga ko'rinishlar orasidagi mapping biriktirilishi; bir tizimda ikki uslub uchrashsa ko'rinishlarni alohida hujjatlash yoki overlay ga yig'ish, tanlov manfaatdorga qarab qilinishi
- Simon Brown, *Software Architecture for Developers*, Leanpub, 16-bob (43-bet) va 18-bob (47-bet) - arxitektor bilan jamoa orasidagi uzilishning to'rt oqibati (hurmatning yo'qolishi, motivatsiyaning tushishi, muhim qarorlarning javobgarlik aniq emasligi uchun oradan tushib ketishi, loyihaning zarar ko'rishi); kollektiv egalikning sharti, ya'ni hammada umumiy manzara haqida kamida asosiy tushuncha bo'lishi
- Simon Brown, *Software Architecture for Developers*, Leanpub, 55-bob (163-bet) - IDE yoki UML vositasi avtomatik generatsiya qiladigan to'liq diagrammadan voz kechish, qo'lda chizilgan va tanlangan maydon bilan metodni ko'rsatadigan yuqori darajali diagrammaning foydaliroq bo'lishi
- Simon Brown, *Software Architecture for Developers*, Leanpub, 58-bob (169-bet) - deploy to'liq avtomatlashtirilgan (Puppet, Chef, continuous delivery) jamoalarda ham deployment bo'limining foydali bo'lib qolishi, chunki skript nima qilayotganini bir qarashda ko'rsatadigan umumiy manzara skriptning o'zida yo'q
- George Fairbanks, *Just Enough Software Architecture: A Risk-Driven Approach*, 1-nashr, Marshall & Brainerd, 2010, 3-bob - risk-driven model: "risklarim nima, qaysi usul ularni kamaytiradi, risk yopildimi" (3.1); risk-driven ishlamayotganining belgisi risklarni sanab bera olmaslik (3.2); arxitektura ishi nosozlik riski bilan mutanosib bo'lishi va model oraliq mahsulot ekani (3.6); "Logical rationale" argument shakli (3.1)
- George Fairbanks, *Just Enough Software Architecture*, 1-nashr, 2010, 5.4 - rasional arxitektura tanlovi shabloni "<x> ustuvor, shuning uchun <y> ni tanladik va <z> kamchiligini qabul qildik"; sababni ochiq yozish kelishmovchilikni injenerlik savoliga aylantiradi va muhokamadan ego ni olib tashlaydi
- George Fairbanks, *Just Enough Software Architecture*, 1-nashr, 2010, 12.5 - faqat sanoqli qaror pivotal, qolganlari yozishga arzimaydi; qaror yozuvi qaror va sabab juftligidan iborat
- Simon Brown, *Software Architecture for Developers*, Leanpub, 5-bob, 12-13-betlar - Booch ta'rifi: arxitektura tizimni shakllantiruvchi muhim qarorlar, muhimlik o'zgartirish narxi bilan o'lchanadi; arxitektura qarori tushdan keyingi bitta refactoring bilan qaytarilmaydi
- Simon Brown, *Software Architecture for Developers*, 26-bob, 67-bet va 39-bob, 116-118-betlar - "last responsible moment" texnologiya qarorini chetlab o'tish bahonasi sifatida ishlatilishi; "har qanday texnologiyada qurish mumkin" degani "qurish kerak" degani emas
- Simon Brown, *Software Architecture for Developers*, 60-bob, 172-173-betlar - decision log: texnologiya va arxitektura tanlovini, qanday tekshirilganini (product evaluation yoki proof of concept) va ko'rib chiqilgan boshqa variantlarni yozish; proof of concept va unum testi natijalariga havola berish
- Robert C. Martin, *Clean Architecture*, 1-nashr, Prentice Hall, 2017, 15-bob, 140-142-betlar ("Keeping Options Open") - siyosatni detaldan ajratish qarorni kechiktirishga imkon beradi; detal deb nomlanganlar: baza, web server, REST, DI framework; variantlar uzoq ochiq qolsa ma'lumot ko'p bo'ladi
- Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer BV, 2023, 15-bob, 207-209 va 214-215-betlar - RFC ning maqsadi (kalit fikrni erta olib loyiha muddatini qisqartirish), RFC ni ish oqimiga qo'yishning to'rt shakli, yozishning to'rt foydasi, fikr yig'ishning asinxron, sinxron va aralash shakllari, arxitektura hujjati RFC dan farqli ravishda fikr uchun emas qayd uchun yozilishi, muhokamani ochadigan besh usul (imkoniyat talablari, oldindan tayinlangan qaror egasi, kodni yozadigan odam mezoni, prototip, mahsulot homiyligi), qaytarilishi arzon qarorda tiqilib qolmaslik va qaytish sababini yozib tarqatish
- Robert C. Martin, *Clean Code*, 1-nashr, Prentice Hall, 2008, 11-bob "Systems", "Optimize Decision Making", 167-168-betlar - qarorni oxirgi imkon bo'lgan daqiqaga qoldirish dangasalik emas; muddatidan oldin qilingan qaror kam ma'lumot bilan qilingan qaror
- Simon Brown, *Software Architecture for Developers*, Leanpub, 32-bob, 79-81-betlar - arxitekturani tushunish bilan uni muloqotda yetkazish bir narsa emas; norasmiy eskizning sakkiz nuqsoni (rang kodi, qutilar va chiziqlar ma'nosi, yo'q munosabat, umumiy atama, tushirib qoldirilgan texnologiya, aralashgan abstraksiya darajalari, ortiqcha tafsilot, kontekst yo'qligi)
- Simon Brown, *Software Architecture for Developers*, Leanpub, 33-bob, 82-83-betlar - eskiz rassomlik emas va to'liq model emas; eskizning foydalari ro'yxati; kontekst, konteyner va komponent diagrammalari odatda yetarli
- Simon Brown, *Software Architecture for Developers*, Leanpub, 34-bob, 84-97-betlar - jamoalar nega vizuallashtira olmaydi (uchta sabab, 84-bet); samarasiz eskiz turlarining nomlari: shopping list, boxes and no lines, functional view, airline route map, generically true, logical view, deployment vs execution context, nomlanmagan aktyorlar (95-bet)
- Simon Brown, *Software Architecture for Developers*, Leanpub, 35-bob, 98-101-betlar - bitta uber-diagramma muammosi va turli abstraksiya darajasidagi bir nechta diagramma; tizim, konteyner, komponent, sinf ierarxiyasi (99-bet); to'rt turdagi diagramma va sinf darajasining ixtiyoriyligi (100-bet); umumiy abstraksiya umumiy notatsiyadan muhimroq, xarita va legend analogiyasi (100-bet); qutiga javobgarlik yozish (101-bet)
- Simon Brown, *Software Architecture for Developers*, Leanpub, 36-bob, 102-105-betlar - kontekst diagrammasining uch savoli; markazda bitta quti, atrofida foydalanuvchi va qo'shni tizimlar; fokus texnologiya emas, odam va tizimda; o'zaro ta'sirni maqsad bilan annotatsiya qilish va use case ro'yxati (103-bet); to'rt motivatsiya va "ikki daqiqada chiziladi" (103-bet); o'quvchisi texnik va notexnik (104-bet)
- Simon Brown, *Software Architecture for Developers*, Leanpub, 37-bob, 106-110-betlar - konteyner diagrammasining besh savoli; konteyner turlari ro'yxati va har konteyner uchun nom, texnologiya, javobgarlik (107-bet); "alohida deploy qilinadimi" sinovi (107-bet); chiziqqa maqsad, usul, uslub, protokol va port yozish (107-108-betlar); tizim chegarasi qutisi va u kontekst diagrammasidagi bitta qutiga to'g'ri kelishi (108-bet); o'quvchisi operatsiya va qo'llab-quvvatlash ham (108-bet); nusxa soni, failover va klasterlash alohida deployment diagrammasida (110-bet)
- Simon Brown, *Software Architecture for Developers*, Leanpub, 38-bob, 111-115-betlar - komponent diagrammasining uch savoli; odatda faqat bitta konteyner ichi ko'rsatiladi (112-bet); har komponent uchun nom, texnologiya, javobgarlik (112-bet); use case ni komponentlar bo'ylab kuzatish to'liqlik sinovi, audit komponenti misoli (112-113-betlar); komponent darajasi sinfdan bir pog'ona yuqori va dizayn soat yoki kun ishi, o'quvchisi faqat ishlab chiqish jamoasi (113-bet)
- Simon Brown, *Software Architecture for Developers*, Leanpub, 40-bob, 120-121-betlar - "kodda shunday qilasizmi" sinovi; umumiy logging komponenti va CQRS dagi qatlam dialoglari; diagramma haqiqatni aks ettiruvchi abstraksiya berishi va element bilan kod o'zaro kuzatiladigan bo'lishi; retrospektiv chizishda savol "biz uni shunday kodladikmi" ga aylanadi
- Simon Brown, *Software Architecture for Developers*, Leanpub, 41-bob, 122-127-betlar - komponent interfeys ortidagi bog'liq xatti-harakatlar to'plami, yuqori kogeziya va past bog'liqlik (122-bet); "komponent haqida gaplashamiz, sinf yozamiz" va Fairbanks ning "model-code gap" atamasi (123-124-betlar); qatlam bo'yicha paketlashda komponent paketlar bo'ylab sochilishi (124-125-betlar); komponent bo'yicha paketlash (126-bet); "tuzilishni tushuntirish qiyin bo'lsa, tuzilishni o'zgartiring" (127-bet)
- Simon Brown, *Software Architecture for Developers*, Leanpub, 43-bob, 131-136-betlar - sarlavha, yorliq va qisqartma, shakl (131-bet); javobgarlikni etti qo'shuv-ayirish ikki banddan oshmaydigan ro'yxat yoki bitta gap bilan yozish (132-bet); chiziq uslubi va strelka bog'liqlikni yoki ma'lumot oqimini ko'rsatishi, ikki tomoni strelkali chiziqdan ehtiyot bo'lish (132-133-betlar); rang, chegara, joylashuv va yo'nalish (133-135-betlar); legend tarkibi (135-bet); diagramma review ro'yxatining to'qqiz bandi (135-136-betlar); chizish paytidagi savollarga quloq solish (136-bet)
- Simon Brown, *Software Architecture for Developers*, Leanpub, 44-bob, 137-138-betlar - konteyner va komponent diagrammalarini qo'shish faqat sodda tizimda, aks holda konteyner diagrammasiga javobgarlik ro'yxati yoziladi (137-bet); umumiy komponentni har diagrammada izoh bilan ko'rsatish; utility komponentni chetga qo'yib izohlash (138-bet); C4 ustiga tashkilot kontekst diagrammasi qo'shilsa model C5 ga aylanadi (138-bet)
- Simon Brown, *Software Architecture for Developers*, Leanpub, 46-bob, 141-143-betlar - kod hamma narsani aytmaydi; koddan javob topilmaydigan savollar ro'yxati va "nimani bilmasligingizni bilmaysiz" (142-bet); kod ustidagi qo'shimcha ma'lumot qatlami (143-bet)
- Simon Brown, *Software Architecture for Developers*, Leanpub, 47-bob, 144-148-betlar - qo'shimcha hujjatni sayohat qo'llanmasi sifatida ko'rish (144-bet); qo'llanmaning to'rt qismi: xaritalar, diqqatga sazovor joylar, tarix va madaniyat, amaliy ma'lumot (145-147-betlar); o'n uch bo'limli ro'yxat va chuqur texnik tafsilotdan saqlanish (147-bet); "beware of the views" va bo'limni yetkazilayotgan narsaga mos nomlash (147-148-betlar); mahsulot uchun bitta qo'llanma, loyiha esa delta (148-bet)
- Simon Brown, *Software Architecture for Developers*, Leanpub, 48-bob, 149-bet - Context bo'limi majburiy, bir-ikki bet yetarli va kontekst diagrammasi hikoyaning ko'p qismini aytadi
- Simon Brown, *Software Architecture for Developers*, Leanpub, 49-bob, 150-151-betlar - Functional Overview bo'limi majburiy; tizim nima qilishini xulosalaydi va qaysi funksiya yoki rol arxitektura uchun ahamiyatli ekanini hamda nega ahamiyatli ekanini bog'laydi
- Simon Brown, *Software Architecture for Developers*, Leanpub, 53-bob, 158-159-betlar - Software Architecture bo'limi majburiy; asosiy fokus konteyner va komponent diagrammalari, yoniga qisqa bayon va har konteyner bilan komponentning xulosasi
- Paul Clements va boshqalar, *Documenting Software Architectures: Views and Beyond*, 2-nashr, Addison-Wesley, 2010, Prolog, P.3, 22-23-betlar - ko'rinish ta'rifi: tizim elementlarining to'plami va ular bilan bog'liq munosabatlarning tasviri; qush qanoti analogiyasi; asosiy printsip "tegishli ko'rinishlarni hujjatlashtirish va ustiga bir nechta ko'rinishga tegishli hujjatni qo'shish"; qatlamli ko'rinish portativlik, deployment ko'rinishi unum va ishonchlilik haqida gapiradi; bitta ko'rinish hujjatining besh elementi va barcha ko'rinishga tegishli hujjatning to'rt elementi (23-bet)
- Paul Clements va boshqalar, *Documenting Software Architectures: Views and Beyond*, 2-nashr, 2010, Prolog, P.4 va P.4.1, 25 va 29-30-betlar - uslub (style) elementlar va munosabat turlarining ixtisoslashishi hamda cheklovlar to'plami (25-bet); arxitektor bir vaqtda uch xil o'ylashi va uch kategoriya: module, component-and-connector, allocation; uslubni tizimga qo'llaganda natija ko'rinish bo'ladi (29-bet); modul avvalo amalga oshirish birligi, komponent runtime birligi, Szyperski ta'rifi (29-30-betlar)
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, 1-nashr, 2020, ilova "Self-Assessment Questions", 21-bob savollari - 21-bob ("Diagramming and Presenting Architecture") C4 ning "to'rt C" si, komponentlar orasidagi nuqtali chiziqning ma'nosi, "irrational artifact attachment" va taqdimotdagi "bullet-riddled corpse" antipatterni haqida gapirishi
- Sam Newman, *Building Microservices: Designing Fine-Grained Systems*, 2-nashr, O'Reilly, 2021, 16-bob ("A Principled Approach", "Strategic Goals", "Principles", "Practices", "Combining Principles and Practices", "A Real-World Example" bo'limlari) - uch darajali ramka: strategik maqsad texnologiyasiz yo'nalish beradi va uni odatda arxitektor belgilamaydi, printsip maqsaddan kelib chiqadi va o'ntadan kam bo'ladi, amaliyot printsipni bajaradi va tez-tez o'zgaradi; printsip bilan cheklov (constraint) farqi va ikkisini bitta ro'yxatda ushlash tavsiyasi; Heroku Twelve Factors printsip to'plamiga misol; Evan Bottcher ning bitta varaqqa sig'adigan maqsad-printsip-amaliyot jadvali; amaliyotni hujjat, ishlaydigan namuna kod va platforma bilan oson bajariladigan qilish. Bu nashrning qo'limizdagi elektron nusxasida barqaror bet raqami yo'q, shuning uchun faqat bob va bo'lim nomi ko'rsatilgan
- Neal Ford, Mark Richards, Pramod Sadalage, Zhamak Dehghani, *Software Architecture: The Hard Parts*, 1-nashr, O'Reilly, 2021 (copyright 2022), 15-bob (400-404-betlar) - trade-off tahlilining uch qadami; bog'liqlikning ishchi ta'rifi ("X o'zgarsa, Y ham o'zgarishga majbur bo'ladimi"); statik bog'liqlik diagrammasi uchun yig'iladigan besh toifa ma'lumot; faqat workflow bilan bog'langan kvantlar statik mustaqil ekani; birikmalarni yengil modellash va amalga oshmaydiganlarini tashlab ketish; matritsadan chiqqan ikki korrelyatsiya (bog'liqlik bilan masshtab, bog'liqlik bilan javob berish va mavjudlik); tub o'lchamni avval fiksatsiya qilish; trade-off jadvallarining sifat tahlili ekani
- Eric Evans, *Domain-Driven Design*, Addison-Wesley, 2004, 2-bob (Documents and Diagrams, Written Design Documents, Explanatory Models) - sodda norasmiy UML eskizi muhokamani mixlab turishi va uch-beshta markaziy obyekt qoidasi; UML modelning ma'nosini va nima qilishi kerakligini ifodalay olmasligi; to'liq diagramma o'rniga tanlangan diagrammalar bilan tasvirlangan matn hujjati; dizayn tafsiloti kodda qolishi; hujjatni baholashning ikki mezoni, ikkinchisi ubiquitous language bilan o'zaro ta'siri; tushuntiruvchi modelni ajratish va unda UML dan qochish. Qo'limizdagi nusxa 2003 yilgi yakuniy qo'lyozma, bet raqamlari nashrga mos kelmaydi, shuning uchun faqat bob va bo'lim nomi ko'rsatilgan
- Mark Richards, Neal Ford, *Fundamentals of Software Architecture*, 1-nashr, O'Reilly, 2020, 1-bob ("Defining Software Architecture") - arxitektura qarori tizim quriladigan qoida, design principle esa qat'iy qoida emas yo'riqnoma (asinxron messaging afzal, lekin REST yoki gRPC ham mumkin); qarorni bir joyda bajarib bo'lmasa variance orqali buzish, variance modellarini architecture review board yoki chief architect yuritishi, istisnoning asos va trade-off bo'yicha tahlil qilinib tasdiqlanishi yoki rad etilishi
- Neal Ford va boshqalar, *Software Architecture: The Hard Parts*, 1-nashr, 2021, 1-bob, 7-12-betlar - fitness function va unit test ajratmasi hamda "domen bilimi kerakmi" savoli (8-bet); atomic va holistic qamrov, xavfsizlik bilan unum hamda scalability bilan elasticity sinergiyasi (7-bet); dynamic fitness function va konkurent foydalanuvchi soniga bog'liq unum chegarasi, qo'lda bajariladigan fitness function va pipeline ning qo'lda bosqichi (11-bet); zero-day exploit va Equifax nosozligining xronologiyasi, xavfsizlik jamoasi uchun har bir pipeline da "slot" (11-12-betlar)
- George Fairbanks, *Just Enough Software Architecture: A Risk-Driven Approach*, Marshall & Brainerd, 2010, 4.1, 4.1.5, 4.2 va 4.2.1-bo'limlar - arxitektura eroziyasi (architectural drift, Perry va Wolf, 1992) riski va dizaynni yetkazish qarori; eng arzon texnikadan boshlab risk pasayguncha qimmatroq texnika qo'shish tartibi; manba kodini o'qitishning chegarasi (papka modulga teng emas, papka tuzilishi bog'liqlikni ifodalamaydi); hujjatlashni uchta asosiy model va uchta ko'rinish turi qoplanganda to'xtatish, matnli va vakil modelni grafikdan oldin qo'yish; o'zaro bog'liq risklar bo'lganda integratsiyani birinchi tekshirish; komponent haqidagi taxminlarni diagrammaga UML izohi sifatida yozish
- George Fairbanks, *Just Enough Software Architecture: A Risk-Driven Approach*, Marshall & Brainerd, 2010, 3.11-bo'lim - ma'lum arxitektura risklarini vaqt bilan cheklangan iteratsiya nolda hal qilish (uslub bo'yicha doska yig'ilishi, COTS unumini prototip bilan o'lchash), iteratsiya nolni BDUF ga aylantirmaslik va qolgan riskni backlog ga surish, birlashgan feature va risk backlog i hamda product owner ga texnik riskni tushuntirish majburiyati
- George Fairbanks, *Just Enough Software Architecture: A Risk-Driven Approach*, Marshall & Brainerd, 2010, 5.4-bo'lim misoli - ustuvorlikka zid lokal optimallashtirish: maintainability ustuvor bo'lganda tezlik uchun jadvalni denormalizatsiya qilish, qarorning instinktiv va ongsiz bo'lishi, xira ustuvorlik va yozilmagan asos irrasional tanlovni yashirishi
- George Fairbanks, *Just Enough Software Architecture: A Risk-Driven Approach*, Marshall & Brainerd, 2010, 9.5.5, 10.1, 10.2 va 12.5-bo'limlar - faqat hal qiluvchi (pivotal) qarorni yozish va kam muhimini ifodalab vaqt sarflamaslik, qaror va asos juftligi (Java tanlovi misoli), tashqi odam ixtiyoriy va hal qiluvchi qarorni ajratib bera olmasligi, thin client misoli; model-kod uzilishidan qochib arxitektura abstraksiyalarini tashlamaslik (big ball of mud ga bir qadam, sinflar dengizini boshqarish qiyinroq), uzilishni mexanik (MDE) va qo'lda boshqarish; toqat qilinadigan nomuvofiqlik mezoni (offline statistika va ko'p threadli kod misollari), sinxronlashning olti strategiyasi (e'tiborsiz, ad hoc, faqat yuqori darajali, hayot tsikli bosqichida, inqirozda, doimiy), abstrakt modelning divergensiyaga chidamliligi va strategiya tanlashning uch mezoni (asbob, tafsilot darajasi, toqat)
- George Fairbanks, *Just Enough Software Architecture: A Risk-Driven Approach*, Marshall & Brainerd, 2010, 15.7-bo'lim - architectural mismatch atamasi va Garlan boshchiligidagi jamoaning COTS integratsiyasidagi qiyinchiliklari (kod shishishi, sekin bajarilish, qayta implementatsiya, konkurentlik, xatoga moyil kompozitsiya); nomoslik taxminlarining to'rt toifasi (komponent, connector, tizim, qurilish jarayoni; Garlan, Allen va Ockerbloom, 1995); taxminlarni diagrammaga izoh sifatida yozish tavsiyasi
- Sam Newman, *Building Microservices: Designing Fine-Grained Systems*, 2-nashr, O'Reilly, 2021, 16-bob ("Governance and the Paved Road", "Exception Handling" bo'limlari) - governance ning uch ishi (kelishish, bilishini ta'minlash, bajarilishini ta'minlash); rasmiy guruh asosan boshqarilayotgan ishni bajaruvchilardan iborat bo'lishi va texnik xavflarni yuritishi; ko'rsatmaga rioyani tekshirib yurish zerikarli ekani, "to'g'ri ishni qilish oson bo'lsin" va arxitektorning paved road talablarini shakllantirishdagi roli hamda platforma jamoasi uchun manfaatdorga aylanishi; amaliyotdan istisnoni jurnalga yozish, istisnolar yig'ilsa printsip yoki amaliyotni o'zgartirish ("hamma joyda MySQL" dan "MySQL, katta o'sish kutilsa Cassandra" ga), ishonch yuqori tashkilotda istisno kuzatuvining kerak bo'lmasligi va qattiq tashkilotda hayotiyligi. Bu nashrning qo'limizdagi elektron nusxasida barqaror bet raqami yo'q, shuning uchun faqat bob va bo'lim nomi ko'rsatilgan
- Sam Newman, *Monolith to Microservices*, O'Reilly, 2019, 2-bob (45-46-betlar) - bir vaqtda ko'p maqsadni (masshtab, jamoa avtonomiyasi, yangi til) qo'shish katta o'zgarish dasturini keltirib chiqarishi va mikroservisni yondashuv sifatida qulflab qo'yishi; asosiy haydovchini ikkilamchi foydalardan ajratish va ikkilamchisi xalaqit berganda orqa o'rinni olishi; har bir natijani slider deb ko'rish va bittasini ko'targanda boshqasini tushirish; ustuvorliklarning o'zgarishi va yozilgan ustuvorlikning avtonom jamoaga yordami
- ESLATMA: korpusdagi *Fundamentals of Software Architecture* nusxasida 19-bob ("Architecture Decisions") ning tanasi yo'q, faqat ilovadagi o'z-o'zini tekshirish savollari bor. Shuning uchun ADR maydonlarining to'liq ro'yxati, antipatternlarning tavsifi va "architecturally significant" ning Nygard bergan besh omili bu bobda iqtibos qilinmaydi. "Architecturally significant" ta'rifi uchun Booch ning Brown keltirgan ta'rifi ishlatilgan
- ESLATMA: korpusdagi *Fundamentals of Software Architecture* nusxasida 21-bob ("Diagramming and Presenting Architecture") ning tanasi ham yo'q: PDF 20-bobdan 24-bobga o'tadi. Shuning uchun 3.12 va 3.17 da shu kitobdan faqat ilovadagi savollar tasdiqlagan nomlar sanaladi, mazmuni iqtibos qilinmaydi. C4 ning butun bayoni Simon Brown dan olingan
- ESLATMA: 3.13, 3.14 va 3.17 dagi diagramma va legend matni korpusning namunasi, kitobdagi rasm emas: Brown ning misollari financial risk system va techtribes.je. 3.15 dagi Java misoli va 3.16 dagi ArchUnit testi ham korpusning tanlovi, kitobda kod yoki avtomatik tekshiruv yo'q. 3.19 dagi `docs/guidebook/` papka daraxti korpusning joylashuv tanlovi, Brown faqat o'n uch bo'lim nomini beradi
- ESLATMA: 3.1 dagi shablon maydonlari (Sana, Qaror egasi, Qayta ko'rish sanasi, Bog'liq ADR, Taxminlar, Kuzatiladigan metrika), Proposed dan boshqa holat qiymatlari, 3.3 dagi erta va kech qaror ro'yxati, 3.6 dagi "rozi emasman, lekin bajaraman" qoidasi va qaror egasi, 3.7 dagi qayta ko'rish sanasi va uchta javob, 3.8 dagi `docs/adr/` joyi va `NNNN-` nom shabloni, 3.9 jadvalidagi "korpus tavsiyasi" deb belgilangan qatorlar, 3.11 dagi checklist, 3.22 dagi uch ustunli varaq namunasi va 3.23 dagi `bash` qadamlari shu korpusning amaliy tavsiyasi, kitobdan olingan emas
- John Ousterhout, *A Philosophy of Software Design*, 1-nashr, Yaknyam Press, 2018, 13.7 va 16.4 - bir nechta modulga tegadigan dizayn qarorlari va ularni hujjatlashtirish joyi; aniq markaziy joy bo'lsa izohni shu yerga qo'yish (yangi qiymat qo'shiladigan sanoqning oxiri), bo'lmasa bo'limlarga ajratilgan markaziy `designNotes` fayli va koddagi qisqa ishora; usulning narxi: bitta nusxa topish oson, lekin kod yonida turmagani uchun yangilash qiyin
- ESLATMA: 3.19 dagi `PaymentStatus` misoli va `designNotes` ni ADR va guidebook orasiga joylashtirish tartibi korpusning tanlovi: Ousterhout misolini boshqa tilda va boshqa domenda beradi
- ESLATMA: 3.24 dagi sinxronlash strategiyalari jadvalining "Amalda" ustuni Fairbanks ning matnidagi baholarini jadvalga ko'chirgan shakl; 3.25 dagi "birinchi spike eng ko'p keyingi ishni bekor qiladigani bo'lsin" formulasi, 3.26 dagi ADR ga variance bo'limi qo'shish va istisno jurnalini ADR papkasi yonida ushlash tartibi shu korpusning tanlovi
- ESLATMA: 3.10 dagi barcha raqam (so'rov soni, qator soni, hajm, p95, indeks hajmi) o'lchanmagan taxmin: ular ADR shaklini ko'rsatish uchun qo'yilgan shartli misol

---

[&larr; 2. Muammoni tushunish va to'g'ri savol berish](02-muammoni-tushunish-va-togri-savol-berish.md) · [Mundarija](README.md) · [4. Kod - muloqot vositasi: nomlash, aniqlik, kognitiv yuk &rarr;](04-kod-muloqot-vositasi-nomlash-aniqlik.md)
