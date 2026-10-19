<!-- doc: clean-code | chapter: 46 | part: XII. Professional intizom -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 46. Vaqt, diqqat va mashq (Time, Focus and Practice)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

- [46.1 Diqqat resursi va uni sarflash](#461-diqqat-resursi-va-uni-sarflash)
- [46.2 Oqim holati haqidagi afsona](#462-oqim-holati-haqidagi-afsona)
- [46.3 Uzilishlarni boshqarish](#463-uzilishlarni-boshqarish)
- [46.4 Pomodoro va vaqt bloklari](#464-pomodoro-va-vaqt-bloklari)
- [46.5 Ko'r yo'lak va botqoqdan chiqish](#465-kor-yolak-va-botqoqdan-chiqish)
- [46.6 Majlis: qachon chiqib ketish haqli](#466-majlis-qachon-chiqib-ketish-haqli)
- [46.7 Kod kata, dojo va ataylab mashq](#467-kod-kata-dojo-va-ataylab-mashq)
- [46.8 Debug vaqti: eng qimmat va eng kam hisobga olinadigan](#468-debug-vaqti-eng-qimmat-va-eng-kam-hisobga-olinadigan)
- [46.9 Debugger asbobini o'zlashtirish](#469-debugger-asbobini-ozlashtirish)
- [46.10 Xatoni topish va tuzatish tartibi](#4610-xatoni-topish-va-tuzatish-tartibi)
- [46.11 Amalda qo'llash](#4611-amalda-qollash)

</details>


Kod sifati diqqat sifatiga bog'liq va diqqat cheklangan resurs. Bu bobda shu resursni boshqarish: uzilishlar, vaqt bloklari, qotib qolgan ishdan chiqish va mashq. Vaqtni taqsimlash yetakchi nuqtai nazaridan arxitektor hujjatidagi [vaqtni taqsimlash](../architect/36-code-review-va-jamoada-texnik-yetakchilik.md#3612-vaqtni-taqsimlash-kod-hujjat-suhbat-organish) bo'limida, [o'rganish rejasi](../architect/38-doimiy-organish-va-texnologiya-tanlash.md#3812-oz-organish-rejangizni-tuzish-chorak-uchun-aniq-maqsadlar) esa o'sha hujjatning o'rganish bobida.

## 46.1 Diqqat resursi va uni sarflash

Programmistning ish kuni kod yozishdan ancha kengroq. McConnell Bell Laboratories da 70 programmist ustida o'tkazilgan vaqt-harakat tadqiqotini keltiradi: vaqtning 35 foizi kod manbasiga, 29 foizi tashkiliy ishga, 13 foizi shaxsiy ishga, 7 foizi majlisga, 6 foizi o'qishga ketgan. Taxminan 30 foiz vaqt loyihaga bevosita yordam bermaydigan faoliyatga sarflangan. Faqat yurishga 6 foiz, ya'ni haftada 2.5 soat va yilda 125 soat ketgan: bu o'qishga ketgan vaqt bilan teng, texnik qo'llanma o'qishdan uch barobar va rahbar bilan suhbatdan olti barobar ko'p (*Code Complete* 2-nashr, 681-bet, Bairdain 1964 ga tayanib).

Ma'lumot 1964 yilga tegishli va nisbatlar odamdan odamga farq qiladi, lekin xulosa o'z kuchini saqlaydi: kod yozish vaqti kun bo'yi mavjud bo'lgan vaqtning kichik qismi, demak uni rejalashtirish kerak.

Ikkinchi nuqta - band ko'rinish bilan natijani aralashtirmaslik. McConnell dangasalik haqidagi bo'limda aniq aytadi: samarali programmlashdagi eng muhim ish o'ylash, va o'ylayotgan odam band ko'rinmaydi; "harakat qilish" ko'pincha ortiqcha, keraksiz kuch bo'lib, harakatni oldinga siljish bilan, bandlikni esa unumdorlik bilan adashtirish oson (*Code Complete* 2-nashr, 830-bet).

Uchinchi nuqta - muhim va shoshilinch farqi. *Software Engineering at Google* buni yetakchilik nuqtai nazaridan tasvirlaydi: elektron pochta, chat va majlis birgalikda vaqt va diqqatga qaratilgan xizmatni rad etish hujumiga o'xshab qoladi, va ehtiyot bo'lmasa odam vaqtining 100 foizini reaktiv rejimda o'tkazadi, ya'ni faqat shoshilinch, lekin muhim bo'lmagan ishlar bilan (6-bob). Kitob keltirgan yechimlardan biri - vazifani boshqaga topshirish, ikkinchisi quyida, 46.4 da.

## 46.2 Oqim holati haqidagi afsona

Uzun uzluksiz "oqim" sessiyasi professionalizm belgisi deb ko'rsatiladi. McConnell bu tasavvurni to'g'ridan-to'g'ri rad etadi. U Edward Yourdon ning bir dasturda bir oy, kuniga 16 soat ishlash va "oxirgi xato" uchun bir necha tunni o'tkazish haqidagi maqtovini keltirib, uni muvaffaqiyatsizlikning deyarli kafolatlangan retsepti deb ataydi: tunni kodda o'tkazish odamga o'zini dunyodagi eng yaxshi programmist deb his qildiradi, keyin esa shu alanga paytida kiritilgan xatolarni tuzatishga bir necha hafta ketadi. Uning xulosasi qisqa: ishtiyoq malakaning o'rnini bosmaydi (*Code Complete* 2-nashr, 832-bet).

Shu yerda ikki narsani aralashtirmaslik kerak, chunki ular bir-biriga zid ko'rinadi.

- **Uzilmasdan ishlangan tinch vaqt foydali.** Buni o'lchangan ma'lumot tasdiqlaydi (46.3).
- **Uzun marafon foydali emas.** Uzilmaslik bilan charchoqqacha ishlash bir narsa emas (43.3).

Ikkinchi afsona - qotib qolgan joyda qat'iyat ko'rsatish. McConnell dasturiy ishda qat'iyat ko'pincha o'jarlik bo'lib chiqishini aytadi: yangi kod ustida qotib qolganda qat'iyat deyarli hech qachon fazilat emas, to'g'ri harakat esa sinfni qayta loyihalash, boshqa yondashuvni sinash yoki keyinroq qaytish (*Code Complete* 2-nashr, 831-bet, Pirsig 1974 ga tayanib). Shu sababli amaliy tavsiya oqimni maqsad qilish emas, qisqa va ongli siklda ishlash (TDD sikli, 31.1) hamda har sikldan keyin bir qadam orqaga chiqib qarash. Juftlikda ishlash uzun marafonni tabiiy ravishda buzadi (41.7).

## 46.3 Uzilishlarni boshqarish

Uzilish va tinch ish joyining unumdorlikka ta'siri o'lchangan. McConnell DeMarco va Lister ning 35 tashkilotdan 166 programmist qatnashgan ishini keltiradi. Musobaqada eng yuqori 25 foizga tushgan programmistlarning ish joyi kattaroq, tinchroq va yopiqroq bo'lgan:

| Muhit omili | Yuqori 25% | Pastki 25% |
|---|---|---|
| Ajratilgan ish maydoni | 78 kvadrat fut | 46 kvadrat fut |
| Yetarlicha tinch ish joyi | 57% ha | 29% ha |
| Yetarlicha yopiq ish joyi | 62% ha | 19% ha |
| Telefonni o'chirish imkoni | 52% ha | 10% ha |
| Qo'ng'iroqni boshqaga yo'naltirish | 76% ha | 19% ha |
| Tez-tez keraksiz uzilish | 38% ha | 76% ha |

Yuqori 25 foiz pastki 25 foizdan 2.6 barobar unumli bo'lgan. DeMarco va Lister yaxshi programmistlar shunchaki lavozim ko'tarilgani uchun yaxshi xonaga tushgan bo'lishi mumkin deb taxmin qilgan, lekin tekshiruv buni rad etdi: bir tashkilotdagi programmistlarning sharoiti unumdorlik farqidan qat'i nazar bir xil edi (*Code Complete* 2-nashr, 684-685-bet, *Peopleware*, DeMarco va Lister 1999 ga tayanib).

McConnell shu ma'lumotdan aniq xulosa chiqaradi: ish joyi pastki 25 foizda bo'lsa, uni yuqori 25 foizga ko'tarish bilan unumdorlikni taxminan 100 foizga oshirish mumkin; o'rtacha bo'lsa, 40 foiz va undan ko'p (shu yerda, 685-bet).

Shu jadvaldagi omillarning ko'pi tashkilot qo'lida, lekin ikkitasi ishlab chiquvchining o'z qo'lida: telefonni o'chirish va keraksiz uzilishni kamaytirish.

| Uzilish turi | Boshqarish usuli |
|---|---|
| Chat xabari | belgilangan vaqtlarda javob berish |
| "Bir daqiqaga" savol | "15 daqiqadan keyin bo'ladimi?" |
| Majlis | bloklangan ish vaqtini kalendarda belgilash (46.4) |
| Incident | to'xtash shart, lekin kontekstni yozib qo'yish |
| O'z-o'zini uzish (brauzer) | muhit sozlamasi, telefon uzoqda |
| Review so'rovi | navbatga qo'yish, darhol emas |

ESLATMA: bu jadval shu korpusning amaliy tavsiyasi, kitobdan olingan emas. Uzilishdan oldin kontekstni bir-ikki qatorda yozib qo'yish ham shunday: foydasi amalda ko'rinadi, lekin tiklash vaqtini qancha qisqartirishi o'lchangan emas, shuning uchun raqam berilmaydi.

## 46.4 Pomodoro va vaqt bloklari

ESLATMA: pomodoro texnikasi, uning 25/5 sikli va 50/10 varianti shu korpusdagi kitoblarda uchramaydi. Oldin bu yerda turgan raqamlar manbasiz edi va o'chirildi. Sarlavha mavzuni belgilaydi, kitobdan olingan usulni emas.

Kitoblarda tasdiqlangan shakl boshqa: **kalendardan vaqt ajratish**. *Software Engineering at Google* muhim va shoshilinch ishlarni ajratish bo'limida aniq tavsiya beradi: muntazam ravishda kamida ikki soatlik blok ajratib, o'sha vaqtda faqat muhim, lekin shoshilinch bo'lmagan ishlar bilan jim o'tirib shug'ullanish (6-bob). Shu yerda yana ikki vosita keltiriladi: vazifani boshqaga topshirish, va ishni kuzatib boradigan tizim tanlash, bunda qaysi tizim ishlashini sinab aniqlash kerak.

Blokning qiymati vaqt o'lchashda emas, uzilishdan himoyada: 46.3 dagi ma'lumot aynan tinch va yopiq ish vaqtining unumdorlik bilan bog'liqligini ko'rsatadi.

Vaqt chegarasining ikkinchi, tasdiqlangan shakli - bitta ishga oldindan maksimal vaqt belgilash. McConnell buni debug uchun aytadi: tez va qo'pol yondashuvni sinashga qaror qilsangiz, unga maksimal vaqt chegarasini qo'ying; chegara oshsa, xato o'ylaganingizdan qiyinroq ekanini tan olib tizimli yo'lga o'tasiz (*Code Complete* 2-nashr, 549-bet). Shu qoida debugdan tashqarida ham ishlaydi (46.5).

## 46.5 Ko'r yo'lak va botqoqdan chiqish

Qotib qolish ikki shaklda keladi: tanlangan yondashuv umuman ishlamaydi, yoki ishlaydi lekin har qadam qiyinlashadi. Ikkisida ham to'g'ri harakat bir xil - to'xtash va yo'lni qayta ko'rish. Sarflangan vaqt davom etish uchun argument emas: u allaqachon ketgan.

McConnell buni qat'iyat haqidagi bo'limda ochiq yozadi. Debugda to'rt soat davomida asabni buzgan xatoni topish yoqimli bo'lishi mumkin, lekin natijasiz ma'lum vaqtdan keyin, aytaylik 15 daqiqadan keyin, voz kechish ko'pincha yaxshiroq: ongsiz ongga muammoni chaynashga vaqt bering, muammoni butunlay chetlab o'tadigan boshqa yondashuvni o'ylab ko'ring, muammoli bo'lakni noldan qayta yozing, yoki keyinroq tetik bosh bilan qaytib keling. Uning xulosasi: kompyuter muammolari bilan jang qilish fazilat emas, ulardan qochish yaxshiroq (*Code Complete* 2-nashr, 831-bet).

Qachon to'xtashni bilish qiyin, lekin savolni berishning o'zi muhim. McConnell belgi sifatida asabiylashuvni ko'rsatadi: o'zingizning asabiylashganini sezgan payt - savol berish payti. Savol berish darhol voz kechish degani emas, lekin ishga chegara qo'yish payti kelganini bildiradi: "shu yondashuv bilan 30 daqiqada hal qilmasam, 10 daqiqa boshqa yondashuvlarni o'ylab, eng yaxshisini keyingi bir soatga sinab ko'raman" (shu yerda).

| Belgi | Harakat (kitobdan) |
|---|---|
| 15 daqiqa natijasiz urinish | to'xtash, boshqa yondashuvni ko'rib chiqish (831-bet) |
| Asabiylashuv boshlandi | tanaffus, bu aniq belgi (548-bet) |
| Tez yo'l uchun belgilangan vaqt oshdi | tizimli yo'lga o'tish (549-bet) |
| Har bir tuzatish yangi xato beradi | bo'lakni noldan qayta yozish (831-bet) |
| Yechim tushunilmaydi, lekin ishlaydi | tushunmaguncha davom etmaslik (41.2) |

Eng arzon chiqish usuli - boshqa odamga tushuntirish. McConnell buni "confessional debugging" deb ataydi: muammoni boshqa odamga tushuntirish paytining o'zida ko'pincha o'z xatongizni topasiz. Kitobdagi misolda tinglovchi bitta so'z ham aytmaydi, muammo esa tushuntirish o'rtasida hal bo'ladi (*Code Complete* 2-nashr, 547-548-bet).

Tanaffusning foydasi ham aytilgan: kofe olishga borganda, tushlik o'rtasida yoki ertasi kuni dushda yechim o'zi keladi; ilgarilash bo'lmasa, barcha variantni sinab bo'lgandan keyin ishni qoldirish kerak. Vaqtincha voz kechishning qo'shimcha foydasi - debug bilan bog'liq asabiylashuvni kamaytirish (shu yerda, 548-bet).

ESLATMA: "ko'r yo'lak" va "botqoq" nomlari shu bo'limda holatni ajratish uchun ishlatiladi; bu nomlar bilan taksonomiya shu korpusdagi kitoblarda yo'q.

## 46.6 Majlis: qachon chiqib ketish haqli

Majlisga ketadigan vaqt o'lchangan va u odam o'ylaganidan kichik: 46.1 dagi tadqiqotda majlisga 7 foiz, o'qishga 6 foiz, rahbar bilan suhbatga esa 1 foiz vaqt ketgan (*Code Complete* 2-nashr, 681-bet). Ya'ni majlis o'zi emas, balki majlis ish vaqtini bo'lib tashlashi (46.3) asosiy narx.

*Software Engineering at Google* majlis muammosini vaqtni boshqarish masalasi sifatida qo'yadi. Aloqa kanallari birgalikda diqqatga hujumga aylanadi, va kitob buni ikki yo'l bilan hal qiladi: ishni boshqaga topshirish, va to'pni ataylab tushirish. Ikkinchisi muhim: hammasini ushlab qolish imkonsiz bo'lsa, qaysi to'pni tushirishni tasodifga qoldirmasdan o'zing tanlashing yaxshiroq, shunda hech bo'lmaganda nazorat qo'lingda qoladi (6-bob).

Majlis bo'yicha kitobdan chiqadigan mezon shu: majlis sizning muhim ishingizdan vaqt olayotgan bo'lsa, u tushiriladigan to'plar ro'yxatida bo'lishi mumkin va bu ongli tanlov sifatida qabul qilinadi.

ESLATMA: "kun tartibi bo'lmagan majlisga rozilik bermaslik" va "majlis maqsadi bajarilgach chiqib ketish haqli" qoidalari shu korpusning amaliy kelishuvi, kitobdan olingan emas.

## 46.7 Kod kata, dojo va ataylab mashq

Mashq va ish bir narsa emas: ishda natija muhim, mashqda usul muhim. Code Complete mashqning uch tasdiqlangan shaklini beradi.

**Qisqa programma bilan tajriba.** Til yoki kutubxonaning bir xususiyati qanday ishlashini bilmasangiz, shu xususiyatni ishlatadigan qisqa programma yozib, uni debuggerda kuzatib ko'rish kerak: tushunmagan xususiyat bilan katta programma yozishdan ko'ra kichik programmada sinash yaxshiroq. McConnell ning qoidasi: xatoni tez qilishni va har safar undan o'rganishni o'rganish; xato qilish gunoh emas, xatodan o'rganmaslik gunoh (*Code Complete* 2-nashr, 822-823-bet).

**Boshqa odamlarning kodini o'qish.** O'zingizdan kuchli programmistlarning kodini topib o'qish, hurmat qilgan va hurmat qilmagan programmistlarning kodini so'rab olib taqqoslash: farq nimada, nega farq qiladi, qaysi biri yaxshiroq va nega. Shu bilan birga o'z kodingiz haqida ekspert programmistlar nima deb o'ylashini bilish istagini rivojlantirish va tanqidni so'rab olish (shu yerda, 824-bet).

**O'qishni muntazam qilish.** McConnell DeMarco va Lister ga tayanib aytadi: bitta kitob ko'pchilik programmistning bir yilda o'qiganidan ko'p. Har ikki oyda bitta yaxshi programmlash kitobi, ya'ni haftada taxminan 35 bet o'qish sohada mustahkam tushuncha beradi (shu yerda, 824-bet).

Mashqning materialini uzoqdan izlash kerak emas: o'z xatolaringiz shu material. McConnell nuqsonni o'rganish imkoni deb ko'rishni taklif qiladi, chunki nuqson borligi programmaning nima qilayotganini to'liq tushunmaganingizni bildiradi. Topilgan xato beshta narsani o'rgatadi: programmaning o'zini (bilganingizda nuqson qolmagan bo'lardi); o'zingiz qiladigan xato turlarini; kodingizning o'qilishini, chunki xatoni topish uchun uni o'qishga majbur bo'lasiz; muammoni qanday yechayotganingizni; va nuqsonni qanday tuzatayotganingizni - simptomni bosib ketyapsizmi yoki sababni tuzatyapsizmi (*Code Complete* 2-nashr, 537-538-bet). Ikkinchi punkt uchun kitob to'rtta savol beradi: xatoni qanday va nega qildim, uni qanday tezroq topishim mumkin edi, uni qanday oldini olishim mumkin edi, va kodda shunga o'xshash boshqa xato bormi (shu yerda, 538-bet).

Shu savollarning javobi yozib borilsa, u **shaxsiy xato ro'yxatiga** aylanadi. McConnell loyiha darajasidagi test yozuvlaridan tashqari shaxsiy yozuv yuritishni tavsiya qiladi: eng ko'p qiladigan xatolaringizning checklisti, hamda kod yozishga, testlashga va xatoni tuzatishga qancha vaqt ketgani yozuvi (shu yerda, 530-bet). Ro'yxat ikki joyda ishlaydi: PR ochishdan oldingi o'z-o'zini review qilishda va xato topilganda o'xshashini izlash qadamida (46.10).

Mashq nega odat shaklida kerakligini 33.9 bo'lim izohlaydi: programmist qiladigan ishning ko'p qismi ongli o'ylamasdan, odat bilan bajariladi, shuning uchun bir narsani birinchi marta o'rganayotganda uni to'g'ri o'rganish kerak. Yomon odatni bo'sh joy bilan almashtirish ishlamaydi: uning o'rniga yangi, ishlaydigan odat qo'yiladi (*Code Complete* 2-nashr, 833-834-bet).

Tajriba haqidagi noto'g'ri tasavvur ham shu yerda tuzatiladi: o'n yil ishlagan odam o'n yillik tajriba oladimi yoki bir yillik tajribani o'n marta oladimi - bu o'z faoliyatini tahlil qilishiga bog'liq; o'rganishni doimiy majburiyatga aylantirmasa, yillar soni tajriba bermaydi (*Code Complete* 2-nashr, 832-bet).

Jamoa darajasida mashq o'rganish madaniyatini talab qiladi. *Software Engineering at Google* buning sharti sifatida psixologik xavfsizlikni ko'rsatadi: odamlar bilmasligini tan olishdan qo'rqmasligi kerak. Kitobning asosiy gapi: har bir ekspert bir vaqtlar yangi boshlovchi edi, va tashkilot muvaffaqiyati odamlarni o'stirishga qilingan sarmoyaga bog'liq. Kitob o'rganishga to'sqinlik qiladigan holatlarni ham sanaydi: bilim orollari, bilim bitta odamda to'planib qolishi (SPOF), "hammasini biladigan yoki hech narsa bilmaydigan" bo'linishi, tushunmasdan nusxalash va qo'rqib tegilmaydigan kod joylari (3-bob).

ESLATMA: kata, dojo, randori va ping-pong kata nomlari, shuningdek FizzBuzz, Roman Numerals, Bowling Game, Gilded Rose kabi mashhur mashq masalalari shu korpusdagi kitoblarda uchramaydi. Ular shu korpusning amaliy tavsiyasi sifatida qoldiriladi: haftada bir soatlik jamoa mashq sessiyasi, bir masalani har safar boshqa usulda yechish, juftlikda navbat bilan klaviaturada ishlash va cheklovli mashq ("metod uch qatordan oshmasin"). Gilded Rose aynan refaktoring uchun yozilgani haqidagi da'vo manbasiz edi va o'chirildi.

## 46.8 Debug vaqti: eng qimmat va eng kam hisobga olinadigan

Debug rejada kam ko'rinadi, lekin amalda ishning katta qismini oladi. McConnell aniq aytadi: ba'zi loyihalarda debug butun ishlab chiqish vaqtining 50 foizigacha egallaydi va ko'p programmist uchun bu programmlashning eng qiyin qismi (*Code Complete* 2-nashr, 535-bet).

Debug vaqti odamdan odamga keskin farq qiladi. Tajribali programmistlar bir xil xato to'plamini topishga ketgan vaqt bo'yicha taxminan 20 barobar farq qiladi. Kamida to'rt yillik tajribali professional programmistlar 12 xatosi bor programmani debug qilgan klassik tadqiqot natijasi:

| O'lchov | Eng tez uchlik | Eng sekin uchlik |
|---|---|---|
| O'rtacha debug vaqti | 5.0 daqiqa | 14.1 daqiqa |
| Topilmagan xato soni | 0.7 | 1.7 |
| Tuzatish paytida kiritilgan xato | 3.0 | 7.7 |

Eng yaxshi programmist 12 xatoning hammasini topdi va tuzatish paytida bitta ham yangi xato kiritmadi; eng yomoni 4 xatoni o'tkazib yubordi va topgan 8 tasini tuzatishda 11 yangi xato kiritdi (*Code Complete* 2-nashr, 536-537-bet, Gould 1975 ga tayanib). Shu farq boshqa tadqiqotlarda ham tasdiqlangan; Sackman, Erikson va Grant ning ishida debug vaqti nisbati 25 barobardan oshgan, va o'sha ishda programmist tajribasining yillari bilan kod sifati yoki unumdorligi orasida bog'liqlik topilmagan (*Code Complete* 2-nashr, 682-bet, Sackman 1968 ga tayanib).

Shu yerdan Sifatning umumiy printsipi chiqadi: eng yaxshi programmistlar eng ko'p xatoni eng tez topdi va tuzatishni eng to'g'ri bajardi, ya'ni sifat, narx va vaqt orasida tanlov qilish kerak emas (shu yerda, 537-bet).

Debugni kamaytirishning birinchi yo'li uni kamroq qilish. McConnell debugni oxirgi chora deb ataydi: sifat boshidan qurilishi kerak, ya'ni talabni ehtiyotkorlik bilan yozish, yaxshi loyihalash va yuqori sifatli kodlash amaliyotlaridan foydalanish (*Code Complete* 2-nashr, 536-bet). Xato borligi programmani to'liq tushunmaganingizni bildiradi, va kodni tasodifiy o'zgartirib ko'rish usuli xatoni kafolatlaydi (shu yerda, 537-538-bet).

Debug boshlanganda esa kitob kafolatli, lekin zerikarli usullar ro'yxatini beradi: buzilgan kodni to'liq review qilish, bo'lakni tashlab noldan qayta yozish, eng qattiq ogohlantirish darajasida kompilyatsiya qilib hamma ogohlantirishni tuzatish, bo'lakni izolyatsiyada unit test bilan sinash, avtomatik test to'plamini butun tunga qo'yib yuborish, kodga log qo'yish, boshqa kompilyator yoki boshqa muhitda ishga tushirish, oxirgi foydalanuvchining konfiguratsiyasini takrorlash, yangi kodni kichik bo'laklarda integratsiya qilib har bo'lakni to'liq sinash (*Code Complete* 2-nashr, 548-549-bet).

Bu ro'yxat uzun ko'rinadi, lekin McConnell savolni teskari qo'yadi: 30 daqiqada yozilgan kodni debug qilishga qancha marta ikki soat sarfladingiz? Shuning uchun tez yo'lni sinashdan oldin unga maksimal vaqt chegarasi qo'yiladi, va chegara oshsa tizimli yo'lga o'tiladi (shu yerda, 549-bet).

| Debug usuli | Kitobdagi asos |
|---|---|
| Boshqa odamga tushuntirish | muammo tushuntirish paytida hal bo'ladi (547-548-bet) |
| Tanaffus | asabiylashuv belgisi bo'lsa to'xtash (548-bet) |
| Xatoni takrorlaydigan test, izolyatsiyada | kafolatli usullar ro'yxatida (548-bet) |
| Log qo'yish | kafolatli usullar ro'yxatida (548-bet); strukturali log kerak, 29.6 |
| Buzilgan bo'lakni noldan qayta yozish | kafolatli usullar ro'yxatida (548-bet) |
| Eng qattiq ogohlantirish darajasi | kafolatli usullar ro'yxatida (548-bet) |
| Kodni tasodifiy o'zgartirib ko'rish | xatoni kafolatlaydi, usul emas (537-538-bet) |

ESLATMA: `git bisect` bilan buzilgan commitni topish shu ro'yxatda kitobdan emas, korpusning o'z tavsiyasi sifatida turadi va atomik commitni talab qiladi (40.1).

## 46.9 Debugger asbobini o'zlashtirish

46.8 debug vaqtining qimmatligini ko'rsatadi; shu vaqtni qisqartiradigan eng oddiy qadam asbobning o'zini bilish. Orosz tajribasiz muhandislar IDE debuggerining qanchalik kuchli ekanini ko'pincha bilmasligini yozadi, holbuki kodni bajarilish paytida kuzatish qaysi taxmin noto'g'ri ekanini ko'rsatadi va "o'zgartirib ko'ramiz, ishlasa kerak" usuliga nisbatan soatlab vaqt tejaydi (Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 9-bob, 125-126-bet).

Breakpoint qo'yish va lokal o'zgaruvchini ko'rish boshlanish nuqtasi. Kitob undan keyingi imkoniyatlarni sanaydi; chap ustun kitobnikidir, o'ng ustun esa shu korpusning Java va Spring dagi tipik ishlatilishi (shu yerda, 126-bet).

| Imkoniyat | Java va Spring dagi tipik holat |
|---|---|
| Shartli breakpoint | 10 ming qatorli faylning faqat bitta muammoli qatori |
| Istisno breakpointi | `catch` ichida yutib yuborilgan istisno qayerdan chiqadi |
| Watchpoint (maydon o'zgarganda) | mutable maydonni kim o'zgartirgani noma'lum |
| Ifodani hisoblash | `Optional` zanjirining qaysi bo'g'ini bo'sh |
| O'zgaruvchini joyida o'zgartirish | xato yo'lini qayta ishga tushirmasdan sinash |
| Freymga qaytish (drop frame) | metodni qaytadan, boshqa kirish bilan kuzatish |
| Threadlar orasida o'tish | ikki thread qulf kutayotgan holat |
| Muhit o'zgaruvchisini o'zgartirish | konfiguratsiyaga bog'liq shoxni tekshirish |

```java
// Shartli breakpoint: butun fayl emas, faqat muammoli yozuv.
// IDE dagi shart: row.currency().equals("USD")
void importRow(SettlementRow row) {
    Money amount = converter.toBaseCurrency(row.amount(), row.currency());
    ledger.post(row.accountId(), amount);
}
```

Asbobni o'rganishning ikkinchi yo'li boshqa odamni kuzatish. Orosz jamoadagi har bir muhandis bilan kamida bir marta debug seansida juft ishlashni maslahat beradi: undan yangi texnika yoki yangi asbob chiqishi deyarli kafolatlangan (shu yerda, 126-bet). Debugger ishlamaydigan holatlar uchun 46.8 dagi usullar ro'yxati qoladi.

## 46.10 Xatoni topish va tuzatish tartibi

46.8 debug vaqtining qimmatligini ko'rsatdi. Shu vaqtni kamaytiradigan narsa asbob emas, tartib: debug ikki ishdan iborat - nuqsonni topish va uni tuzatish, va topish bilan tushunish odatda ishning 90 foizini oladi (*Code Complete* 2-nashr, 540-bet). Samarali programmistlar bu yerda taxmin qilmaydi, ilmiy usulni ishlatadi: kuzatish, faraz, farazni tekshiradigan tajriba (shu yerda, 540-bet).

Kitob ilmiy usulning debugdagi shaklini besh qadam qilib beradi (shu yerda, 541-bet):

1. **Xatoni barqarorlashtirish.** Xato ishonchli takrorlanmasa, uni diagnoz qilish imkoni yo'q. Birinchi ish - uni har safar chiqaradigan eng kichik shartni topish.
2. **Manbani lokalizatsiya qilish.** Bu qadam o'z ichida to'rt qismdan iborat: xatoni chiqargan ma'lumotni yig'ish; ma'lumotni tahlil qilib nuqson haqida faraz tuzish; farazni test bilan yoki kodni ko'rib isbotlash yoki rad etish yo'lini aniqlash; shu yo'l bilan farazni isbotlash yoki rad etish. Rad etilsa, yangi faraz bilan qaytariladi.
3. **Nuqsonni tuzatish.**
4. **Tuzatishni test qilish.**
5. **O'xshash xatolarni izlash.**

Uchinchi qadam oson ko'rinadi va aynan shuning uchun xatoga moyil: o'lchangan ma'lumotga ko'ra tuzatishlarning yarmidan ko'pi birinchi urinishda noto'g'ri chiqqan (shu yerda, 550-bet, Yourdon 1986b ga tayanib). Kitobning tuzatish qoidalari (shu yerda, 550-554-bet):

| Qoida | Mazmuni |
|---|---|
| Tuzatishdan oldin muammoni tushunish | xatoni chiqaradigan va chiqarmaydigan holatlar bilan uni ikki tomondan qisish |
| Diagnozni tasdiqlash | raqobatdagi farazlarni ham rad etish; "sabablardan biri bo'lishi mumkin" bitta sabab ustida ishlash uchun yetarli emas |
| Asl kodni saqlab qo'yish | qaytib boriladigan versiya bo'lsin, keyin qaysi o'zgarish muhim bo'lganini solishtirib topish mumkin |
| Simptomni emas sababni tuzatish | maxsus holat qo'shish (`if (clientId == 45) ...`) ko'p holatda ishlamaydi, chunki sabab odatda initsializatsiya nuqsoni; maxsus holatlar esa to'planib kodning asosiy xususiyatiga aylanadi |
| Kodni sababsiz o'zgartirmaslik | `+1` va `-1` ni navbat bilan qo'yib ko'rish usul emas; o'zgarishdan oldin uning ishlashiga ishonch bo'lishi kerak |
| Bir vaqtda bitta o'zgarish | ikkitasi birga kiritilsa, xato tuzalmaganini, tuzalib yangisi kirganini yoki ikkisini ajratib bo'lmaydi |
| Tuzatishni tekshirish | diagnozda ishlatilgan holatlarni va butun regression to'plamini qayta yurgizish |
| Xatoni ochadigan test qo'shish | test to'plami ushlamagan xato uchun yangi test yoziladi |
| O'xshash nuqsonlarni izlash | nuqsonlar guruh bo'lib yuradi; o'xshashini qanday izlashni tasavvur qila olmaslik muammo hali to'liq tushunilmaganining belgisi |

```java
// 1-qadam: xatoni testda barqarorlashtirish (avval yiqiladi)
@Test
void aralashValyutaliQatorRadEtiladi() {
    SettlementBatch batch = SettlementBatch.of(
            row("USD", "100.00"), row("UZS", "100.00"));

    ImportReport report = importer.importBatch(batch);

    assertThat(report.rejected()).hasSize(1);
    assertThat(report.acceptedTotal()).isEqualByComparingTo("100.00");
}
```

Ikkinchi qadamning psixologik tomoni ham bor: odam kutgan narsasini ko'radi (psychological set). `Num` tokenini hamma "Number" deb o'qiydi, qavs qo'yilmagan `if` ni ko'pchilik qavsli deb ko'radi, bir harf bilan farq qiladigan ikki o'zgaruvchi bitta deb o'qiladi (shu yerda, 554-555-bet). Bundan ikki xulosa chiqadi. Birinchisi: toza formatlash, nomlash va izoh debug asbobi hisoblanadi, chunki ular fon yaratadi va xato shu fonda chetga chiqqan narsa bo'lib ko'rinadi. Ikkinchisi xavf: samarali debug qiluvchilar programmaning ahamiyatsiz qismini aqlan kesib tashlaydi, ba'zan esa aynan nuqson turgan qism kesiladi va vaqt xato yo'q joyga ketadi. Bu debug ko'rligi; undan chiqish yo'li yo'l ayrilishiga qaytib kesilgan qismni qaytarish, oldini olish yo'li esa nomlar orasidagi masofani katta qilish (2.16).

Bu tartibni [arxitektor hujjatidagi diagnostika tartibi](../architect/14-jvm-profiling-va-diagnostika-jfr-async.md#141-diagnostika-tartibi-avval-olchov-keyin-faraz-keyin-tuzatish) bilan aralashtirmaslik kerak: u ishlash muammosi uchun (belgini raqamga aylantirish, resursni aniqlash, farazni tekshirish, bitta o'zgarish), bu esa kod xatosi uchun. Farq birinchi qadamda: ishlash diagnostikasi o'lchovdan boshlanadi, chunki simptom statistik (p99, p50); kod xatosi esa barqarorlashtirishdan boshlanadi, chunki takrorlanmaydigan xato ustida faraz tekshirib bo'lmaydi. Umumiy qismi ikkisida bir xil: avval faraz, keyin o'zgarish, va bir vaqtda bitta o'zgarish.

## 46.11 Amalda qo'llash

- [ ] Bir hafta davomida vaqtingiz qayerga ketganini yozib borib, 46.1 dagi nisbatlar bilan taqqoslang.
- [ ] Kalendarda muntazam ravishda kamida ikki soatlik blok ajratib, o'sha vaqtda faqat muhim ishni qiling (SEaG 6-bob).
- [ ] Ish joyingizdagi telefonni o'chirish va keraksiz uzilishni kamaytirish imkonini tekshirib, 46.3 jadvalidagi yuqori 25 foiz sharoitiga yaqinlashtiring.
- [ ] Uzilishdan oldin kontekstni yozib qoldirish odatini joriy qiling.
- [ ] Har bir qiyin ish uchun oldindan maksimal vaqt chegarasi belgilab, oshganda tizimli yo'lga o'tish qoidasini qo'llang (549-bet).
- [ ] 15 daqiqa natijasiz urinishdan keyin to'xtab, boshqa yondashuvni ko'rib chiqish qoidasini sinab ko'ring (831-bet).
- [ ] Qotib qolganda birinchi harakat sifatida muammoni boshqa odamga tushuntirib bering (547-548-bet).
- [ ] Har ikki oyda bitta programmlash kitobini o'qish rejasini tuzing, haftada taxminan 35 bet (824-bet).
- [ ] O'zingizdan kuchli programmistning kodini topib o'qing va o'z kodingiz bilan taqqoslab, farqning sababini yozib qo'ying (824-bet).
- [ ] Debug vaqtini bir oy davomida o'lchab, eng ko'p vaqt ketgan sohaga test va log qo'shing.
- [ ] Xato topilganda besh qadamli tartibni (barqarorlashtirish, lokalizatsiya, tuzatish, tuzatishni test qilish, o'xshashini izlash) qo'llang va o'z xatolaringizning shaxsiy ro'yxatini yurita boshlang (46.10, 46.7).

## Manbalar

- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 28-bob (681) - 70 programmist ustidagi vaqt-harakat tadqiqoti: kod manbasiga 35 foiz, majlisga 7 foiz, o'qishga 6 foiz, loyihaga bevosita yordam bermaydigan faoliyatga 30 foizcha vaqt
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 28-bob (684-685) - *Peopleware* (DeMarco va Lister 1999) ma'lumoti: yuqori 25 foizning tinch va yopiq ish joyi, keraksiz uzilish 38 va 76 foiz, unumdorlikdagi 2.6 barobar farq va muhitni yaxshilashdan kutiladigan foyda
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 28-bob (682) - Sackman, Erikson va Grant 1968: debug vaqti nisbati 25 barobardan oshishi, tajriba yillari bilan sifat orasida bog'liqlik yo'qligi
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 23-bob (535-538) - debug ba'zi loyihalarda vaqtning 50 foizigacha; Gould 1975 tadqiqotining raqamlari; debug oxirgi chora ekani; tasodifiy o'zgartirish xatoni kafolatlashi; Sifatning umumiy printsipi
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 23-bob (547-549) - "confessional debugging", tanaffus va asabiylashuv belgisi, kafolatli usullar ro'yxati, tez yo'l uchun maksimal vaqt chegarasi
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 33-bob (822-824) - qisqa programma bilan tajriba, kuchli programmistlarning kodini o'qish va tanqid so'rash, har ikki oyda bitta kitob va haftada 35 bet
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 33-bob (830) - eng muhim ish o'ylash ekani; bandlikni unumdorlik bilan adashtirish
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 33-bob (831) - qotib qolganda qat'iyat fazilat emasligi, 15 daqiqa qoidasi va ishga vaqt chegarasi qo'yish
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 33-bob (832) - "Gonzo Programming": tunni kodda o'tkazish afsonasi va undan keyingi haftalab tuzatish; o'n yillik tajriba va bir yillik tajribani o'n marta olish farqi
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 33-bob (833-834) - odatning roli, birinchi marta to'g'ri o'rganish va yomon odatni yangi odat bilan almashtirish
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 6-bob - muhim va shoshilinch farqi, aloqa kanallarining diqqatga hujumi, kamida ikki soatlik bloklangan vaqt, topshirish va to'pni ataylab tushirish
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 3-bob - o'rganish madaniyati va psixologik xavfsizlik; har ekspert bir vaqtlar yangi boshlovchi ekani; bilim orollari, SPOF, tushunmasdan nusxalash
- Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 9-bob (125-126) - 46.9 dagi debuggerning kam ishlatilishi, "o'zgartirib ko'rish" usuliga nisbatan vaqt tejashi, kengaytirilgan imkoniyatlar ro'yxati va har jamoadoshi bilan bir marta debug seansida juft ishlash maslahati
- ESLATMA: 46.3 dagi uzilishni boshqarish jadvali, 46.4 dagi pomodoro atamasi, 46.5 dagi "ko'r yo'lak" va "botqoq" nomlari, 46.6 dagi majlis qoidalari va 46.7 dagi kata va dojo shakllari, 46.9 jadvalining o'ng ustuni shu korpusning amaliy tavsiflari, kitobdan olingan emas
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 23-bob
  (540-541) - debugda topish ishning 90 foizi ekani, ilmiy usul va xatoni
  topishning besh qadami (barqarorlashtirish, lokalizatsiya, tuzatish,
  tuzatishni test qilish, o'xshash xatolarni izlash)
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 23-bob
  (550-554) - tuzatishlarning yarmidan ko'pi birinchi urinishda noto'g'ri
  chiqishi (Yourdon 1986b), diagnozni tasdiqlash, asl kodni saqlash,
  simptom emas sababni tuzatish, kodni sababsiz o'zgartirmaslik, bir vaqtda
  bitta o'zgarish, tuzatishni tekshirish va o'xshash nuqsonlarni izlash
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 23.4
  (554-555) - psychological set: kutilgan narsani ko'rish, misollari va
  debug ko'rligi; toza formatlash va nomlashning debugdagi roli
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 22.7
  (530) - shaxsiy test yozuvlari: eng ko'p qiladigan xatolar checklisti va
  yozish, testlash, tuzatishga ketgan vaqt yozuvi
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 23.1
  (537-538) - nuqsonni o'rganish imkoni sifatida ko'rish va undan
  chiqadigan besh savol

---

[&larr; 45. Baholash, muddat va bosim](45-baholash-muddat-va-bosim.md) · [Mundarija](README.md) · [47. Birgalikda ishlash va o'rgatish &rarr;](47-birgalikda-ishlash-va-orgatish.md)
