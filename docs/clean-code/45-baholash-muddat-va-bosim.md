<!-- doc: clean-code | chapter: 45 | part: XII. Professional intizom -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 45. Baholash, muddat va bosim (Estimation, Deadlines and Pressure)

<details>
<summary>Bu bobdagi 10 bo'lim</summary>

- [45.1 Baho va majburiyat farqi](#451-baho-va-majburiyat-farqi)
- [45.2 Uch nuqtali baho va PERT](#452-uch-nuqtali-baho-va-pert)
- [45.3 Planning poker va kattalik birligi](#453-planning-poker-va-kattalik-birligi)
- [45.4 Katta ishni baholash va noaniqlik konusi](#454-katta-ishni-baholash-va-noaniqlik-konusi)
- [45.5 Bosim ostida intizomni saqlash](#455-bosim-ostida-intizomni-saqlash)
- [45.6 Kechikishni oshkor qilish va "90% tayyor" tuzog'i](#456-kechikishni-oshkor-qilish-va-90-tayyor-tuzogi)
- [45.7 Qamrovni qisqartirish yoki sifatni qisqartirish](#457-qamrovni-qisqartirish-yoki-sifatni-qisqartirish)
- [45.8 Texnik qarz ishini raqam bilan himoya qilish](#458-texnik-qarz-ishini-raqam-bilan-himoya-qilish)
- [45.9 Ish turiga qarab baholash va noaniqlikni kamaytirish](#459-ish-turiga-qarab-baholash-va-noaniqlikni-kamaytirish)
- [45.10 Amalda qo'llash](#4510-amalda-qollash)

</details>


Noto'g'ri baho toza kodni buzadigan ikkinchi kuch: vaqt yetmaganda test, refaktoring va hujjat birinchi qurbon bo'ladi. Bu bobda baholashning amaliy texnikalari va bosim ostida intizomni saqlash.

## 45.1 Baho va majburiyat farqi

Eng ko'p chalkashlik shu ikki tushunchani aralashtirishdan keladi. **Baho** - ehtimollik bilan aytilgan taxmin, u xato bo'lishi mumkin va bu normal. **Majburiyat** - bajarilishi kerak bo'lgan gap (44.3), u xato bo'lmasligi kerak.

Baho noaniqligi o'lchangan. McConnell keltirgan ma'lumotda o'rtacha katta dasturiy loyiha bir yil kechikadi va budjetdan 100 foiz oshadi; alohida ishlab chiquvchilarning bahosi esa 20-30 foizlik optimizm koeffitsientiga ega, ya'ni muntazam ravishda kam ko'rsatiladi (*Code Complete* 2-nashr, 671-bet, Standish Group 1994, Jones 1997, Johnson 1999 va van Genuchten 1991 ga tayanib).

Shu sababli ikkinchi qoida muhim: **baho muhokama qilinmaydi**. Bahoni aniqroq qilish uchun qayta hisoblash mumkin, lekin rahbar bilan savdolashish ishning qancha vaqt olishini o'zgartirmaydi. McConnell bu xatoni Bert misolida ko'rsatadi: sakkiz odam va olti oylik baho "qisqartir" degan iltimosdan keyin olti odam va to'rt oyga aylanadi, holbuki ishning hajmi o'zgarmagan. IBM dagi Bill Weimer ning kuzatuvi ham shu: texnik odamlar baholashni yaxshi bajaradi, qiyinchilik bahoni himoya qilishda (*Code Complete* 2-nashr, 827-828-bet).

Bahoni emas, loyihaning boshqa o'lchamlarini muhokama qilish mumkin: xususiyatni olib tashlash, bosqichlarga bo'lib yetkazish, odam soni va muddatni almashtirish (shu yerda, 828-bet).

| Savol | To'g'ri javob turi |
|---|---|
| "Qancha vaqt oladi?" | baho (noaniqligi bilan) |
| "Juma kuniga bo'ladimi?" | majburiyat (ha/yo'q) |
| "Eng tez qachon?" | optimistik baho, oshkor belgilangan |
| "Bahoni qisqartira olasizmi?" | yo'q; qamrovni qisqartirish mumkin (45.7) |

## 45.2 Uch nuqtali baho va PERT

Bitta son bilan baholash ma'lumot yo'qotadi. McConnell baholash ishini boshlashdan oldin maqsadni aniqlashni talab qiladi va shu savollarni beradi: baho qanchalik aniq bo'lishi kerak, unga qanday ishonch darajasi biriktiriladi, optimistik yoki pessimistik baho natijani tubdan o'zgartiradimi (*Code Complete* 2-nashr, 671-bet). Ya'ni optimistik va pessimistik chegarani oshkor aytish baholashning bir qismi.

ESLATMA: PERT ning `(O + 4M + P) / 6` kabi tortilgan formulasi va chetlanishni kvadratik qo'shish qoidasi shu korpusdagi kitoblarda yo'q, shuning uchun bu yerda raqamli formula berilmaydi. Sarlavhadagi "PERT" atamasi mavzuni belgilaydi, kitobdan olingan hisob usuli emas.

Formula o'rniga kitobda tasdiqlangan ikki qoida ishlaydi.

**Mayda darajada baholash.** Baho qancha batafsil tekshirishga tayansa, shuncha aniq bo'ladi. McConnell buni Katta sonlar qonuni bilan izohlaydi: bitta katta bo'lakdagi 10 foizlik xato o'sha 10 foiz bo'lib qoladi, 50 kichik bo'lakda esa xatolarning bir qismi yuqoriga, bir qismi pastga ketadi va o'zaro qisqaradi (*Code Complete* 2-nashr, 672-bet). Ishni bo'lishning matematik asosi shu.

**Bir necha usul bilan baholab, natijalarni taqqoslash.** Usullar bir xil natija bermaydi va aynan farqning o'zi ma'lumot beradi. McConnell o'z kitobining birinchi nashrini misol qiladi: ko'z bilan bergan bahosi 250-300 bet edi, batafsil baho 873 bet chiqdi, butunlay boshqa usul bilan qaytarilgan baho 828 bet; ikki batafsil baho bir-biridan besh foizcha farq qilgani uchun u 250 emas, 850 betga yaqin bo'lishiga ishonch hosil qildi (*Code Complete* 2-nashr, 672-bet).

Shoshib berilgan baho aniq bo'lmaydi: katta ishni baholash o'zi kichik loyiha sifatida rejalashtiriladi (shu yerda, 671-bet).

## 45.3 Planning poker va kattalik birligi

Code Complete baholash yondashuvlari ro'yxatida jamoa bilan baholashning ikki shakli bor: bahoni muhokama majlisida ko'rib chiqish, va har kim o'z vazifasini baholab, keyin baholarni qo'shish. Shu ro'yxatdagi yana ikki punkt o'z tarixingizga tayanadi: avvalgi loyihalar tajribasiga qarash, va avvalgi baholarni saqlab, ular qanchalik to'g'ri chiqqanini ko'rib yangi bahoni tuzatish (*Code Complete* 2-nashr, 671-bet).

Oxirgi punkt eng arzon va eng ko'p o'tkazib yuboriladigan vosita: o'z jamoangizning baho va haqiqiy vaqt tarixi hech qanday umumiy koeffitsientdan ko'ra aniqroq.

Baholashdan oldin talab aniq bo'lishi shart. McConnell ni so'zma-so'z emas, mazmunan: arxitektor "ancha katta" uyning narxini aytolmaydi, siz ham "ancha katta" loyihani baholay olmaysiz; baho berishdan oldin talab yoziladi yoki dastlabki o'rganish bosqichi rejalashtiriladi (*Code Complete* 2-nashr, 672-bet).

ESLATMA: planning poker nomi, story point va Fibonachchi shkalasi (1, 2, 3, 5, 8, 13) shu korpusdagi kitoblarda yo'q. Nisbiy kattalik birligida baholash va katta baholangan ishni majburiy bo'lish - shu korpusning amaliy tavsiyasi, kitobdan olingan emas; shuning uchun kattalik birligini soatga aylantiradigan jadval berilmaydi.

## 45.4 Katta ishni baholash va noaniqlik konusi

Code Complete dagi 28-2 rasm bahoning tabiatini bitta grafikda ko'rsatadi: loyiha boshida baho tarqalishi 4x dan 0.25x gacha yetadi, loyiha oldinga siljigan sari diapazon 2x, 1.5x, 1.25x orqali 1.0x ga torayadi. Rasm izohi bitta xulosa beradi: boshida berilgan baho tabiatan noaniq, shuning uchun baho davriy ravishda qayta ko'riladi va har bosqichda o'rganilgan narsa keyingi bahoga kiritiladi (*Code Complete* 2-nashr, 673-bet).

ESLATMA: "noaniqlik konusi" nomi Code Complete 2-nashrida uchramaydi; kitobda faqat rasm va uning diapazoni bor. Shu sababli bu yerda diapazon raqamlari rasmdan olinadi, nomga esa kitob kafolat bermaydi. Diapazonni loyiha bosqichlariga qattiq bog'lab ("talab tugagach 2x, dizayn tugagach 1.5x") aytish kitobda yo'q va shuning uchun berilmaydi.

Amaliy natija: katta ish uchun bitta son bermaslik, balki **diapazon** berish va qayta ko'rish nuqtalarini belgilash. Noaniqlikni kamaytirishning kitobda ko'rsatilgan yo'li - baho berishdan oldin dastlabki o'rganish bosqichini rejaga qo'yish (*Code Complete* 2-nashr, 672-bet); shu bosqichning amaliy shakli spike ([arxitektor hujjatidagi](../architect/README.md) spike va prototip bo'limi).

Nega katta ishda noaniqlik tabiiy ekanini *Software Engineering at Google* boshqa tomondan ko'rsatadi: kodning kutilayotgan umri uchun maqbul javoblar taxminan 100 000 barobar farq qiladi, va dasturiy injiniring qarorlari vaqt va o'sish bo'yicha aniq bo'lmagan baholar ustida qabul qilinadi (1-bob).

## 45.5 Bosim ostida intizomni saqlash

Bosim paytida odatiy reaksiya - intizomni tashlash: testni o'tkazib yuborish, review ni qisqartirish, kodni shoshilib yozish. Kitoblar buni ikki tomondan rad etadi.

Birinchisi - sifat va narx bir yo'nalishda harakat qiladi. McConnell debug bo'yicha tadqiqotdan Sifatning umumiy printsipini chiqaradi: eng yaxshi programmistlar eng ko'p xatoni eng tez topdi va tuzatishni eng to'g'ri bajardi, ya'ni sifat, narx va vaqt orasida tanlov qilish kerak emas, ular birga yuradi (*Code Complete* 2-nashr, 537-bet).

Ikkinchisi - muammoni ertaroq topish arzonroq. *Software Engineering at Google* buni "shifting left" deb ataydi: ishlab chiqish yo'lida muammo qancha chapda, ya'ni qancha erta topilsa, uni tuzatish shuncha arzon; statik tahlil va review da ushlangan xato ishlab chiqarishga chiqqan xatodan ancha arzon (1-bob). Review va testni bosim ostida o'tkazib yuborish aynan xatoni o'ngga, qimmat zonaga surish.

Uchinchisi - intizom ijodkorlikka zid emas. NASA ning Software Engineering Laboratory ishidan 15 yillik retrospektivada inson intizomiga tayangan usul va asboblar ayniqsa samarali bo'lgani qayd etilgan (*Code Complete* 2-nashr, 829-bet, McGarry va Pajerski 1990 ga tayanib). McConnell ning amaliy xulosasi: ijodkorlikni ahamiyatsiz narsaga sarflamaslik, nomuhim sohalarda konvensiya o'rnatib, ijodiy kuchni muhim joyga qoldirish (shu yerda).

| Bosim ostida | To'g'ri harakat |
|---|---|
| "Test yozishga vaqt yo'q" | xatoni keyin topish qimmatroq (537-bet) |
| "Review ni o'tkazib yuboraylik" | review eng arzon xato to'suvchi (SEaG 1-bob) |
| "Keyin tozalaymiz" | tozalash ishning qismi (1.3) |
| "Hamma kech qolib ishlasin" | tunda yozilgan kod keyin haftalab tuzatiladi (46.2) |
| "Parallel qilib tezlashtiramiz" | Brooks qonuni, pastda |
| "Yetib olamiz" | kechikish oxirga borib ortadi, pastda |
| "Qamrovni qisqartiramiz" | **to'g'ri yechim** (45.7) |

**"Yetib olamiz" umidi.** McConnell buni eng ko'p uchraydigan reaksiya deb ataydi va 300 dan ortiq loyihani qamragan tadqiqotga tayanadi: kechikish va oshib ketish odatda loyiha oxiriga borib ortadi, loyihalar yo'qotilgan vaqtni keyin qaytarib olmaydi, balki yana ko'proq orqada qoladi (*Code Complete* 2-nashr, 675-bet, van Genuchten 1991 ga tayanib).

**Odam qo'shish.** Kechikkan loyihaga odam qo'shish uni yana kechiktiradi: yangi odam loyihaga kirishishga vaqt sarflaydi, uning o'qishi allaqachon kirishgan odamlarning vaqtini oladi, va odam soni ortishi aloqa hajmini ko'paytiradi (*Code Complete* 2-nashr, 676-bet, Fred Brooks ga tayanib). Shu yerda muhim nuqta bor: McConnell qoidani mutlaqlashtirmaydi. Vazifalar bo'linmaydigan bo'lsa, odam qo'shish yordam bermaydi; bo'linadigan bo'lsa, kech qo'shilgan odamga ham mustaqil bo'lak berish mumkin (shu yerda).

## 45.6 Kechikishni oshkor qilish va "90% tayyor" tuzog'i

Holat haqida halol hisobot berish intellektual halollikning bir qismi: real holat hisoboti va real baho, rahbar ularni o'zgartirishni so'raganda esa o'z pozitsiyasini saqlash (*Code Complete* 2-nashr, 826-bet).

McConnell holat hisobotini "shov-shuvli ikkiyuzlamachilik sohasi" deb ataydi va aniq shaklini keltiradi: programmistlar loyihaning oxirgi 50 foizi davomida dastur "90 foiz tayyor" deb aytish bilan mashhur. Shu yerda Tom Cargill qoidasi keltiriladi: kodning birinchi 90 foizi ishlab chiqish vaqtining birinchi 90 foizini oladi, qolgan 10 foiz kod esa vaqtning yana 90 foizini oladi (*Code Complete* 2-nashr, 827-bet).

Yechim: foiz emas, **tugallangan qismlar** bilan hisobot berish. Va kuzatuvlarni hissiyotsiz, yolg'iz suhbatda aytish: rahbar odatda o'zi eshitishni xohlagan javobni emas, halol kuzatuvni qadrlaydi, chunki ishni muvofiqlashtirish uchun unga aniq ma'lumot kerak (shu yerda).

```text
Yomon: "90% tayyor"
Yaxshi: "Qaytarish oqimi tugadi va testlari o'tyapti. Bank integratsiyasi
         yozilgan, lekin sandbox'da hali sinalmagan. Xato oqimi va
         idempotentlik qolgan: taxminan 2 kun."
```

Agar muammo o'z holatini yomon sezishda bo'lsa, yechim o'z ishini o'lchab o'rganish; agar muammo rahbar eshitishni xohlagan javobni aytishda bo'lsa, bu boshqa masala va uni intizom bilan hal qilish kerak (shu yerda, 827-bet).

## 45.7 Qamrovni qisqartirish yoki sifatni qisqartirish

Vaqt yetmaganda McConnell ro'yxatidagi eng kuchli va eng ko'p o'tkazib yuboriladigan vosita - loyiha qamrovini qisqartirish. Sababi aniq: xususiyatni olib tashlaganingizda uning dizayni, kodi, debugi, testi va hujjati ham olib tashlanadi, shuningdek uning boshqa xususiyatlar bilan interfeysi ham (*Code Complete* 2-nashr, 676-bet).

Buning uchun imkoniyatlar oldindan uch guruhga bo'linadi: **shart** (must have), **yaxshi bo'lardi** (nice to have) va **ixtiyoriy** (optional). Orqada qolganda ixtiyoriy va "yaxshi bo'lardi" guruhlari tartiblanadi va eng kam muhimlari tushiriladi (shu yerda).

Xususiyatni butunlay tashlamasdan ham arzonlashtirish mumkin: tezlik uchun sozlanmagan versiya berish, eng kam muhim funksionallikni qo'pol shaklda qilish, tezlik yoki xotira talabidan chekinish (shu yerda). Shu bir xil ro'yxat 33-bobda rahbar bilan nima muhokama qilish mumkinligi sifatida qaytadi: xususiyatni olib tashlash, unumdorlikni pasaytirish, bosqichlarga bo'lib yetkazish, odam soni va muddatni almashtirish (*Code Complete* 2-nashr, 828-bet).

Sifat esa bu ro'yxatda yo'q, va buning sababi iqtisodiy: Sifatning umumiy printsipiga ko'ra sifatni oshirish ishlab chiqish narxini kamaytiradi, ya'ni sifatni qisqartirish tejamkorlik emas (*Code Complete* 2-nashr, 537-bet).

| Qisqartirish mumkin (kitobdan) | Nega |
|---|---|
| Xususiyat soni | dizayn, kod, debug, test, hujjat va interfeys birga ketadi (676-bet) |
| Unumdorlik sozlashi | sozlanmagan versiya ham yetkazilishi mumkin (676, 828-bet) |
| Eng kam muhim funksionallikning sayqali | qo'pol shakl ham ishlaydi (676-bet) |
| Tezlik va xotira talabi | sekin yoki xotira talab versiya arzonroq (676-bet) |
| Yetkazish shakli | bosqichlarga bo'lish mumkin (828-bet) |

ESLATMA: qisqartirilmaydigan narsalarning aniq ro'yxati (testlar, xavfsizlik tekshiruvi, ma'lumot butunligi, migratsiyaning orqaga mosligi, xato bilan ishlash, monitoring) - shu korpusning amaliy kelishuvi. Kitob umumiy printsipni beradi, bu ro'yxatni emas.

## 45.8 Texnik qarz ishini raqam bilan himoya qilish

Bosim ostidagi prioritet suhbatida texnik qarz ishi deyarli har doim yutqazadi, chunki biznes ishining qiymati raqamda, qarz ishiniki esa his-tuyg'uda aytiladi. Gergely Orosz yechimni shu nomutanosiblikni yo'qotishda ko'radi: katta qarz bo'laklari ro'yxatga olinadi, har birining ta'siri va uni yo'qotish uchun ketadigan mehnat baholanadi. Ma'lumot bo'lmasa, bir necha hafta yoki oy oladigan qarz haqida yaxshi qaror ham chiqmaydi (Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 13-bob, 188-bet).

Orosz qarzni olib tashlash taklifida ko'p keltiriladigan ta'sir turlarini sanaydi: ishonchlilik, xarajat tejash, ishlab chiqish siklining tezlashishi va xatolarning kamayishi (o'sha manba, 188-bet). Hisobning o'zi ko'pincha oddiy ko'paytirish bo'ladi. Sekin build misolida Orosz beradigan shakl:

```text
Kunlik yo'qotish = (bir build da yo'qotilgan vaqt)
                 x (muhandis kuniga nechta build yurgizadi)
                 x (shunday qiladigan muhandislar soni)
```

Qiymatlar o'z jamoangizning o'lchovidan olinadi: Orosz shaklni beradi, raqamni emas.

Bir xil qarzning qiymati kontekstga qarab o'zgaradi, shuning uchun bir marta hisoblangan son boshqa joyga ko'chirilmaydi. Orosz takrorlangan mantiq misolini keltiradi: uni umumiy kutubxonaga ko'chirishning ta'siri tez-tez ishlatiladigan kod bazasida ancha katta bo'ladi, tez orada bekor qilinadigan kod bazasida esa katta mehnat evaziga kichik foyda chiqadi (o'sha manba, 188-bet).

Oxirgi vosita ruxsat so'rash bosqichini butunlay chetlab o'tadi. Orosz unumdor deb ko'riladigan va ayni paytda qarzni kamaytiradigan muhandislarning usulini shunday ta'riflaydi: tozalashga alohida ruxsat so'ralmaydi, u yuqori ta'sirli loyihaning ichiga qo'shib bajariladi. Mantiq ketma-ket: eng yuqori prioritetli loyihalar ko'pincha aynan qarzi ko'p tizimlarga tegadi, demak u yerdagi ish baribir sekinroq boradi, va qarzni kamaytirish uchun asos shu bilan tayyor bo'ladi (o'sha manba, 188-bet).

Chegarasi [qamrovni qisqartirish yoki sifatni qisqartirish](#457-qamrovni-qisqartirish-yoki-sifatni-qisqartirish) bo'limidagi bilan bir xil mantiqda: bu usul rejalashtirilgan ishning qamrovini jim kengaytirish uchun emas, qarz ishini ko'rinadigan, baholangan va kelishilgan qilish uchun.

## 45.9 Ish turiga qarab baholash va noaniqlikni kamaytirish

Bitta baholash usuli har ishga to'g'ri kelmaydi. Gergely Orosz baholashni o'rganiladigan ko'nikma deb ataydi va qiyinchilik ish turiga qarab o'zgarishini ta'kidlaydi: ishonchli muhandis "baholab bo'lmaydi" demaydi, aniq baho beradi va noma'lum joylar bilan kechikishni oshkor aytadi (Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 7-bob, 103-bet).

Eng oson holat - avval qilingan ishga o'xshash ish: yana bitta endpoint yoki yana bitta sahifa o'tgan safar qancha vaqt olganiga qarab baholanadi (o'sha manba, 103-bet). Avval qilinmagan ish uchun Orosz yetti turni sanaydi va har turda noaniqlik boshqa joydan keladi.

| Ish turi | Noaniqlik manbai | Orosz beradigan yo'l |
|---|---|---|
| Hamkasb qilgan ishga o'xshash | kontekstni bilmaslik | hamkasbdan yondashuvni so'rash, bahoni biroz uzaytirish |
| Refaktoring | hajmi oldindan ko'rinmaydi | avvalgi refaktoring tajribasi yoki timebox |
| Bilgan texnologiyada greenfield | biznes talabining noaniqligi | talab aniq bo'lsa, baho ham yetarli aniq |
| Bilmagan tizimga integratsiya | tizimning haqiqiy xulqi | avval prototip, bo'lmasa ideal va eng yomon holat bahosi |
| Yetuk, lekin o'zingizga yangi texnologiya | o'rganish vaqti | tajribali muhandisdan so'rash, juftlikda ishlash, timebox |
| Butunlay yangi texnologiya | kam material, freymvorkning o'z xatolari | prototipsiz baho bermaslik |
| Murakkab ish, notanish tizim va texnologiya | hammasi birga | prototip va ishni har bo'lagida bitta noma'lum qoladigan qilib bo'lish |

**Timebox - baholash vositasi.** Orosz ning ta'rifi sodda: vazifaga muddat biriktiriladi va unda faqat shu muddat davomida ishlanadi, undan uzoq emas (o'sha manba, 103-bet). Oxiri oldindan ko'rinmaydigan ishda timebox bahoning o'rnini bosadi, kattaligi esa maqsadga qarab tanlanadi: texnologiyani o'rganish timeboxi tutoriallarga, kod yozishga va birinchi iteratsiyalar odatdagidan ko'proq debug talab qilishini bilib olishga yetishi kerak (o'sha manba, 104-bet). Timeboxning buzilgan ko'rinishi, ya'ni qarorni cheksiz cho'zish, [patterns hujjatida](../patterns/25-anti-patternlar.md) tahlil falaji sifatida yozilgan.

**Bosim bo'lsa, eng yomon holatni ayting.** Notanish tizimga integratsiyada Orosz ikki raqamni beradi: hech qanday muammo chiqmasligini faraz qiladigan "ideal" baho va tizim g'alati ishlashini hamda vaqtinchalik yechim kerak bo'lishini faraz qiladigan "eng yomon holat" bahosi; ta'rifiga ko'ra ikkinchisi yuqori chiqadi. Darhol baho talab qilinsa, aynan eng yomon holat aytiladi: u hammaga yoqmaydi, lekin prototip uchun timebox so'rashga asos beradi (o'sha manba, 104-bet). Orosz ning o'z tavsiyasi bitta jumla: iloji bo'lsa doim prototip quriladi.

Bu [45.4](#454-katta-ishni-baholash-va-noaniqlik-konusi) ni to'ldiradi: diapazon noaniqlikni ko'rsatadi, prototip va timebox esa uni kamaytiradi.

## 45.10 Amalda qo'llash

- [ ] Har bahoda optimistik va pessimistik chegarani oshkor aytib, kerakli aniqlik darajasini oldin kelishib oling (671-bet).
- [ ] Katta ishni bitta bo'lak sifatida emas, mayda darajada baholab, xatolarning o'zaro qisqarishiga joy bering (672-bet).
- [ ] Bitta bahoni ikki xil usulda hisoblab, natijalarni taqqoslang; farq katta bo'lsa sabab topilmaguncha son bermang (672-bet).
- [ ] Avvalgi baho va haqiqiy vaqtni saqlab boradigan jadval tuting va yangi bahoni shu tarixga qarab tuzating (671-bet).
- [ ] Baho berishdan oldin talab yozilganiga ishonch hosil qiling; yozilmagan bo'lsa dastlabki o'rganish bosqichini rejaga qo'ying (672-bet).
- [ ] "Foiz tayyor" hisobotini tugallangan qismlar ro'yxatiga almashtiring (827-bet).
- [ ] Kechikish haqida xabar berish muddatini ("bilgan kuni") kelishuvga yozing.
- [ ] Qamrovni oldindan "shart", "yaxshi bo'lardi" va "ixtiyoriy" guruhlariga bo'lib qo'ying, orqada qolganda tanlov tayyor bo'lsin (676-bet).
- [ ] Bosim paytida qisqartirilmaydigan narsalar ro'yxatini (45.7) jamoa kelishuviga kiriting.
- [ ] Notanish tizim yoki notanish texnologiya bo'lsa, baho berishdan oldin prototip uchun timebox so'rang; darhol raqam talab qilinsa eng yomon holat bahosini ayting (104-bet).

## Manbalar

- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 28-bob (671-672) - baholash yondashuvlari ro'yxati, maqsad va ishonch darajasini oldin aniqlash, Katta sonlar qonuni, bir necha usulni taqqoslash va talabsiz baho bermaslik
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 28-bob (671) - o'rtacha katta loyiha bir yil kechikadi va budjetdan 100 foiz oshadi; ishlab chiquvchi bahosining 20-30 foizlik optimizm koeffitsienti
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 28-bob (673, 28-2 rasm) - baho tarqalishi loyiha boshida 4x dan 0.25x gacha va oxiriga borib 1.0x ga torayishi, bahoni davriy qayta ko'rish
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 28-bob (675) - 300 dan ortiq loyiha tadqiqoti: kechikish va oshib ketish loyiha oxiriga borib ortadi, yo'qotilgan vaqt keyin qaytmaydi
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 28-bob (676), Fred Brooks ga tayanib - kechikkan loyihaga odam qo'shish uni yana kechiktiradi, va bu qoidaning bo'linadigan vazifalar uchun cheklovi
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 28-bob (676) - qamrovni qisqartirish eng kuchli va eng ko'p o'tkazib yuboriladigan vosita; shart / yaxshi bo'lardi / ixtiyoriy bo'linishi va arzonroq versiya variantlari
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 33-bob (826-828) - intellektual halollik, baho muhokama qilinmasligi, Bill Weimer ning bahoni himoya qilish haqidagi kuzatuvi, muhokama qilinadigan o'lchamlar ro'yxati
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 33-bob (827) - "90 foiz tayyor" hisoboti loyihaning oxirgi 50 foizida aytiladi; Tom Cargill ning 90/90 qoidasi
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 33-bob (829) - intizom ijodkorlikni bo'g'maydi; NASA Software Engineering Laboratory ning 15 yillik retrospektivasi
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 23-bob (537) - Sifatning umumiy printsipi: sifat, narx va vaqt orasida tanlov qilish kerak emas
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 1-bob - "shifting left": muammoni ertaroq topish arzonroq; kod umrining 100 000 barobarlik tarqalishi va aniq bo'lmagan baholar ustidagi qarorlar
- Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 13-bob (188-bet) - katta qarzni ro'yxatga olish va ta'sirini baholash, taklifda keltiriladigan ta'sir turlari, sekin build ni ko'paytirish bilan hisoblash, qarzni yuqori ta'sirli loyihaga qo'shib olib tashlash
- Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 7-bob (102-105-bet) - baholash o'rganiladigan ko'nikma va qiyinchiligi ish turiga bog'liq; avval qilingan ishga o'xshash ishni o'tgan safargi vaqtga qarab baholash; avval qilinmagan ishning yetti turi; timeboxing ta'rifi; notanish tizim uchun ideal va eng yomon holat bahosi hamda prototip tavsiyasi
- ESLATMA: 45.2 dagi PERT formulasi, 45.3 dagi planning poker nomi va story point shkalasi, 45.4 dagi "noaniqlik konusi" atamasi va 45.7 dagi qisqartirilmaydigan narsalar ro'yxati shu korpusning amaliy tavsiflari, kitobdan olingan emas

---

[&larr; 44. "Yo'q" va "ha" deyish: majburiyat tili](44-yoq-va-ha-deyish-majburiyat-tili.md) · [Mundarija](README.md) · [46. Vaqt, diqqat va mashq &rarr;](46-vaqt-diqqat-va-mashq.md)
