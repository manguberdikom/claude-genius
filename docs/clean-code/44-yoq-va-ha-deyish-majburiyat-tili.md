<!-- doc: clean-code | chapter: 44 | part: XII. Professional intizom -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 44. "Yo'q" va "ha" deyish: majburiyat tili (Saying No and Saying Yes)

<details>
<summary>Bu bobdagi 6 bo'lim</summary>

- [44.1 "Yo'q" ni qachon va qanday aytish](#441-yoq-ni-qachon-va-qanday-aytish)
- [44.2 "Urinib ko'raman" nega yolg'on](#442-urinib-koraman-nega-yolgon)
- [44.3 Majburiyat tili: aytaman, qilaman, qachongacha](#443-majburiyat-tili-aytaman-qilaman-qachongacha)
- [44.4 Passiv tavakkalchilik va uning narxi](#444-passiv-tavakkalchilik-va-uning-narxi)
- [44.5 Jamoa bo'lib "yo'q" deyish](#445-jamoa-bolib-yoq-deyish)
- [44.6 Amalda qo'llash](#446-amalda-qollash)

</details>


Toza kodni buzadigan eng kuchli kuch - noto'g'ri majburiyat. "Juma kuniga bo'ladi" degan gap aytilgach, sifat birinchi qurbon bo'ladi. Bu bobda majburiyat tilining qoidalari, baho va majburiyat farqi esa [baho va majburiyat farqi](45-baholash-muddat-va-bosim.md#451-baho-va-majburiyat-farqi) bo'limida.

## 44.1 "Yo'q" ni qachon va qanday aytish

McConnell *Code Complete* ning 33-bobida intellektual halollik belgilari ro'yxatiga ikkita band qo'yadi: realistik jadval bahosini berish va boshqaruv uni o'zgartirishni so'raganda o'z pozitsiyasida qolish. Shu ro'yxat "yo'q" deyishni xarakter masalasidan kasbiy talabga aylantiradi.

Nega pozitsiyada qolish kerak - McConnell buni Bert misolida ko'rsatadi. Bert sakkiz programmist va olti oy deb baholaydi, menejer "qisqarog'i bo'lmaydimi" deb so'raydi, Bert ta'lim va ta'tilni qirqib olti programmist va to'rt oyga tushadi. Xatosi bitta: baho muhokama qilinmaydi. Bahoni aniqroq qilish mumkin, lekin menejer bilan savdolashish ishning qancha vaqt olishini o'zgartirmaydi. To'rt oy deb va'da berib olti oyda topshirish, olti oy deb va'da berib olti oyda topshirishdan yaxshi emas: birinchi yo'lda ishonch yo'qoladi, ikkinchisida hurmat ortadi. IBM dagi Bill Weimer ning kuzatishi ham shu kitobda keltirilgan: texnik odamlar baholashni yaxshi bajaradi, qiyinchilik qarorini himoya qilishda - ular pozitsiyada qolishni o'rganishi kerak.

Shu sababli "yo'q" maqsadga emas, aniq muddat yoki qamrovga aytiladi. McConnell bosim ostidagi javobning shaklini ham beradi: bu qancha turishini men aytaman, bunga arziydimi yoki yo'qmi - boshqaruvning qarori; muddatning o'zini "savdolashish" esa bir milda qancha fut borligi haqida savdolashishga o'xshaydi, tabiat qonuni bilan savdolashilmaydi. Savdolashiladigan narsa boshqa: loyihaning jadvalga ta'sir qiladigan qismlari. McConnell sanaydigan muqobillar - xususiyatni olib tashlash, unumdorlik talabini pasaytirish, bosqichlarga bo'lib yetkazish, kam odam va uzoq jadval yoki ko'p odam va qisqa jadval.

Jadval orqada qolganda qamrovni qisqartirish - McConnell alohida ta'kidlaydigan va ko'pincha e'tibordan chetda qoladigan usul. Xususiyat olib tashlansa, uning dizayni, kodi, debugi, testi, hujjati va boshqa xususiyatlar bilan interfeysi ham olib tashlanadi. Buning uchun mahsulot qismlari oldindan uch toifaga bo'linadi: bo'lishi shart, bo'lsa yaxshi, ixtiyoriy. Qisqartirishning yumshoq shakli ham bor - xuddi shu funksiyani arzonroq variantda berish, masalan unumdorlik uchun sozlanmagan yoki eng kam ahamiyatli qismi sodda bajarilgan variant.

```text
Yomon: "Mumkin emas" (sabab yo'q, muqobil yo'q)

Yaxshi: "Juma kuniga to'liq xususiyat chiqmaydi: migratsiya va bank
integratsiyasi shu qadar vaqt oladi. Juma kuniga qaytarish qismini
chiqara olaman, bank integratsiyasi keyingi bosqichda. Buni qilish
kerakmi yoki muddat muhimroqmi - qaror sizda."
```

Kodni himoya qilish tomoni [mijoz va ishlab chiquvchi maqsadlari to'qnashuvi](43-professional-masuliyat.md#434-mijoz-va-ishlab-chiquvchi-maqsadlari-toqnashuvi) bo'limida: Martin *Clean Code* da jadvalni himoya qilish menejerning ishi, kodni himoya qilish esa ishlab chiquvchining ishi deb yozadi va chalkashlik xavfini tushunmagan irodaga bo'ysunishni professional emas deb ataydi.

## 44.2 "Urinib ko'raman" nega yolg'on

Aniq majburiyat o'rniga mujmal javob berishning sababi odatda bitta: menejer eshitishni xohlagan javobni aytish. McConnell holat hisobotini "shov-shuvli ikkiyuzlamachilik sohasi" deb ataydi va programmistlar loyihaning oxirgi yarmida ham "90 foiz tayyor" deyishga moyil ekanini yozadi. Lekin u ikki sababni ajratadi. Birinchisi - o'z progressini yomon sezish: bu o'z ish usulini o'rganish bilan tuzatiladi. Ikkinchisi - fikrini aytmaslik, chunki menejer kutgan javobni berish osonroq: bu butunlay boshqa masala va uni intizom bilan tuzatish kerak.

McConnell ning kuzatishi aks tomonga ishlaydi: menejer loyiha holati haqidagi halol kuzatishni, hatto u kutgan fikr bo'lmasa ham, qadrlaydi. Shart bitta - kuzatish o'ylangan bo'lsin, iloji boricha hissiyotsiz va yolg'iz holda aytilsin. Boshqaruvga ishni muvofiqlashtirish uchun aniq ma'lumot kerak, shuning uchun to'liq hamkorlik shart.

Mujmal javobni aniqlashtirishning oson vositasi ham shu bobda: har masalada o'z ishonch darajangizni raqamlashga tayyor turing. "Urinib ko'raman" ning o'rniga aytiladigan narsa shundan kelib chiqadi - qancha ishonch borligi, nimaga bog'liqligi va qachon aniq javob berilishi.

Noto'g'ri bahoni oshirib yuborish ham xuddi shu masalaning davomi. McConnell loyihani boshlatish uchun bahoni ataylab kamaytirishni tavsiya qilgan ma'ruzachini qattiq tanqid qiladi: xarajat haqida yolg'on aytish boshqaruvning qaror qabul qilish huquqini yashirincha o'g'irlash degani, chunki ish kompaniyaga arziydimi yoki yo'qmi - bu boshqaruvning javobgarligi.

"90 foiz tayyor" tuzog'ining mexanikasi [kechikishni oshkor qilish](45-baholash-muddat-va-bosim.md#456-kechikishni-oshkor-qilish-va-90-tayyor-tuzogi) bo'limida.

## 44.3 Majburiyat tili: aytaman, qilaman, qachongacha

Majburiyat olingach, bajarilmasligi aniq bo'lgan zahoti darhol xabar qilish kerak, oxirgi kungacha kutmaslik. Buning sababi kitobda o'lchangan: McConnell orqada qolgan loyihada "keyin yetib olamiz" degan umidni eng keng tarqalgan javob deb ataydi va uning deyarli hech qachon ishlamasligini aytadi - uch yuzdan ortiq loyiha tekshirilgan kuzatishda kechikish va oshib ketish loyiha oxiriga qarab ortgan. Loyihalar yo'qotilgan vaqtni keyin qoplamaydi, ular yana ko'proq orqada qoladi.

Orqada qolganda odam qo'shish ham javob emas: Brooks qoidasi bo'yicha kechikkan loyihaga odam qo'shish uni yana kechiktiradi, chunki yangi odamlar o'rganishi kerak va bu o'rganish allaqachon ishlayotganlarning vaqtini oladi. McConnell faqat bir shartda istisno bo'lishini aytadi - vazifalar mustaqil bo'linadigan bo'lsa.

Quyidagi jadval shu korpusning amaliy shakli: majburiyatni kim, nima va qachongacha qismlari bilan yozish, shunda uni bajarilgan yoki bajarilmagan deb belgilash mumkin bo'ladi.

| Shakl | Majburiyatmi |
|---|---|
| "Buni qilishimiz kerak" | yo'q (kim?) |
| "Tez orada tayyor bo'ladi" | yo'q (qachon?) |
| "Agar vaqt bo'lsa qilaman" | yo'q (shart) |
| "Seshanba kuni soat 12 gacha PR ochaman" | ha |

## 44.4 Passiv tavakkalchilik va uning narxi

Passiv tavakkalchilik - "menga aytilgani shu" deb aniq xato bo'lgan yo'lni davom ettirish. Martin *Clean Code* da bu urinishning nega ishlamasligini aytadi: ishlab chiquvchi rejalashtirishda chuqur qatnashadi va nosozlik uchun javobgarlikni, ayniqsa u yomon kod sababli bo'lsa, bo'lishadi. Javobgarlik boshqaga o'tmaydi.

McConnell menejer bilan ishlash variantlarini sanaganda rad etishni ham ro'yxatga kiritadi: menejer aytganini bajarmaslik va ishni to'g'ri yo'lda qilishni talab qilish. Lekin u eng yaxshi uzoq muddatli yechim boshqa deb hisoblaydi - menejerni o'rgatish, ya'ni to'g'ri yo'lni tushuntirishni uzluksiz ish deb qabul qilish.

Professional xatti-harakat shundan kelib chiqadi: xavfni yozib xabar qilish, muqobil taklif qilish, qaror boshqa tomondan kelsa uni qayd etib davom etish. "Rozi emasman, lekin bajaraman" qoidasi [jamoadagi kelishmovchilik](../architect/03-qaror-qabul-qilish-va-uni-hujjatlashtirish.md#36-jamoadagi-kelishmovchilik-va-rozi-emasman-lekin-bajaraman-qoidasi) bo'limida ko'rilgan.

Quyidagi shablon shu korpusning amaliy shakli, kitobdan olingan emas:

```markdown
## Xavf haqida xabar (qisqa shakl)
**Qaror**: <qanday qaror qabul qilinmoqda va nima sababdan>.
**Xavf**: <qanday sharoitda nima buziladi va kim sezadi>.
**Asos**: <o'lchov, log yoki incident havolasi>.
**Taklif**: <muqobil va uning narxi>.
**Qabul qilingan qaror**: <nima tanlandi, qanday chegaralar bilan>.
**Qayta ko'rish**: <qanday hodisadan keyin yoki qaysi sanada>.
```

## 44.5 Jamoa bo'lib "yo'q" deyish

Majburiyat haqidagi tashqi suhbatga jamoa bo'lib kirish uchun jamoa ichida avval kelishuv bo'lishi kerak. Agar bir odam "bo'ladi" deb aytsa, qolganlarning "yo'q" i kuchini yo'qotadi.

*Software Engineering at Google* ning 5-bobi kelishuv qurishni yetakchining eng ko'p qiladigan ishi deb ataydi va muhim nuqtani qo'shadi: vakolat bo'lsa ham, yo'nalishni buyurish kelishuv qurishdan ko'ra kamroq samarali. Shu kitobning 2-bobi esa yolg'iz dahiy haqidagi afsonani rad etadi va jamoani kamtarlik, hurmat va ishonch ustiga quradi - ya'ni "yo'q" ni jamoa nomidan aytish uchun avval jamoa ichida shu uchta ustun ishlashi kerak.

Baholashni jamoa bo'lib qilish ham shu kitobdan emas, baholash amaliyotidan kelib chiqadi: McConnell baholash usullari ro'yxatiga bahoni walk-through majlisida ko'rib chiqishni va har kim o'z vazifasini baholab, keyin baholarni qo'shishni kiritadi hamda bir necha usulni qo'llab natijalarni solishtirishni tavsiya qiladi. Birlik bilan chiqadigan raqam shu yerda tug'iladi. Mexanikasi [planning poker va kattalik birligi](45-baholash-muddat-va-bosim.md#453-planning-poker-va-kattalik-birligi) bo'limida.

## 44.6 Amalda qo'llash

- [ ] Keyingi hafta "urinib ko'raman" iborasini umuman ishlatmaslikni sinab ko'ring; har safar ishonch darajasi va shartlari bilan aniq shaklga aylantiring.
- [ ] Har bir majburiyatni kim, nima va qachongacha shaklida yozib boring va bajarilishini kuzating.
- [ ] Muddat suhbatiga kirishdan oldin muqobillar ro'yxatini tayyorlang: qaysi xususiyat olib tashlanadi, nima bosqichlarga bo'linadi, qaysi talab pasayadi.
- [ ] Mahsulot qismlarini "bo'lishi shart", "bo'lsa yaxshi" va "ixtiyoriy" toifalariga ajratib, jamoa bilan kelishib oling.
- [ ] Rozi bo'lmagan qarorlar uchun [passiv tavakkalchilik](#444-passiv-tavakkalchilik-va-uning-narxi) bo'limidagi xavf xabari shablonini ishlating.
- [ ] Muddat haqidagi tashqi suhbatdan oldin jamoa ichida kelishuvga erishish qoidasini kiriting.
- [ ] Bajarilmaydigan majburiyat haqida darhol xabar qilish qoidasini kelishuvga yozing.
- [ ] Oxirgi uch kechikishni ko'rib chiqib, qaysi birida majburiyat aniq bo'lmaganini aniqlang.

## Manbalar

- Steve McConnell, *Code Complete* 2-nashr, Microsoft Press, 2004, 33-bob (826-bet) - intellektual halollik ro'yxati: realistik jadval bahosi va boshqaruv bosimida pozitsiyada qolish
- Steve McConnell, *Code Complete* 2-nashr, Microsoft Press, 2004, 33-bob (827-828 betlar) - Bert misoli, bahoning muhokama qilinmasligi, tabiat qonuni bilan savdolashmaslik va savdolashiladigan muqobillar ro'yxati
- Steve McConnell, *Code Complete* 2-nashr, Microsoft Press, 2004, 33-bob (827-bet) - holat hisobotidagi ikkiyuzlamachilik, "90 foiz tayyor" va menejer kutgan javobni aytish muammosi
- Steve McConnell, *Code Complete* 2-nashr, Microsoft Press, 2004, 33-bob (826-bet) - ishonch darajasini raqamlashga tayyor turish
- Steve McConnell, *Code Complete* 2-nashr, Microsoft Press, 2004, 33-bob (828-bet) - bahoni ataylab kamaytirish boshqaruvning qaror huquqini o'g'irlash degani
- Steve McConnell, *Code Complete* 2-nashr, Microsoft Press, 2004, 28-bob (675-676 betlar) - "keyin yetib olamiz" umidi ishlamasligi, kechikishning oxirga qarab ortishi, Brooks qoidasi va qamrovni qisqartirish usuli
- Steve McConnell, *Code Complete* 2-nashr, Microsoft Press, 2004, 28-bob (671-672 betlar) - baholash usullari: walk-through majlisi, har kimning o'z vazifasini baholashi, bir necha usulni solishtirish
- Steve McConnell, *Code Complete* 2-nashr, Microsoft Press, 2004, 28-bob (686-bet) - menejer bilan ishlash variantlari, shu jumladan rad etish, va menejerni o'rgatishning uzoq muddatli afzalligi
- Robert C. Martin, *Clean Code*, Prentice Hall, 2009, 1-bob (5-6 betlar) - rejalashtirishdagi ulush va javobgarlik, kodni jadval kabi himoya qilish
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 5-bob - kelishuv qurish yetakchining asosiy ishi, buyurish undan kamroq samarali
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 2-bob - yolg'iz dahiy afsonasining rad etilishi, kamtarlik, hurmat va ishonch ustunlari
- ESLATMA: 44.3 dagi kim/nima/qachongacha jadvali, 44.4 dagi xavf xabari shabloni va 44.6 dagi tekshiruv ro'yxati shu korpusning amaliy shakli, kitobdan olingan emas

---

[&larr; 43. Professional mas'uliyat](43-professional-masuliyat.md) · [Mundarija](README.md) · [45. Baholash, muddat va bosim &rarr;](45-baholash-muddat-va-bosim.md)
