<!-- doc: clean-code | chapter: 43 | part: XII. Professional intizom -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 43. Professional mas'uliyat (Professionalism)

<details>
<summary>Bu bobdagi 7 bo'lim</summary>

- [43.1 "Zarar qilmaslik": funksiyaga va tuzilishga](#431-zarar-qilmaslik-funksiyaga-va-tuzilishga)
- [43.2 O'z xatosi uchun javob berish](#432-oz-xatosi-uchun-javob-berish)
- [43.3 Ishga layoqat: charchagan holda kod yozmaslik](#433-ishga-layoqat-charchagan-holda-kod-yozmaslik)
- [43.4 Mijoz va ishlab chiquvchi maqsadlari to'qnashuvi](#434-mijoz-va-ishlab-chiquvchi-maqsadlari-toqnashuvi)
- [43.5 Kasbiy etika: sir, ma'lumot, xavfsizlik](#435-kasbiy-etika-sir-malumot-xavfsizlik)
- [43.6 Sifat me'yorini eng tajribali muhandis belgilaydi](#436-sifat-meyorini-eng-tajribali-muhandis-belgilaydi)
- [43.7 Amalda qo'llash](#437-amalda-qollash)

</details>


Toza kod texnik qoidalar to'plami emas, kasbiy munosabat natijasi. Bu va keyingi to'rt bob shu munosabatni ko'rib chiqadi: javobgarlik, majburiyat, baholash, vaqt va birgalikda ishlash. Texnik yetakchilik va jamoada qaror tarqatish [arxitektor hujjatidagi](../architect/README.md) code review va texnik yetakchilik bo'limida, ataylab mashq esa [kod kata va dojo](46-vaqt-diqqat-va-mashq.md#467-kod-kata-dojo-va-ataylab-mashq) bo'limida.

## 43.1 "Zarar qilmaslik": funksiyaga va tuzilishga

Ishlaydigan narsani buzmaslik ko'rinadigan talab: xato, regressiya va ma'lumot yo'qolishi darhol seziladi. Ikkinchi zarar ko'rinmaydi - kod bazasini o'zgartirishga qarshilik qiladigan holga keltirish.

Robert Martin *Clean Code* ning 1-bobida shu ikkinchi zararning mexanikasini ketma-ket tasvirlaydi: har bir o'zgarish kodning yana ikki-uch joyini buzadi, hech bir o'zgarish arzon bo'lmay qoladi va jamoa unumdorligi nolga qarab intiladi. Boshqaruv javob sifatida odam qo'shadi, yangi odamlar esa dizayn niyatini bilmaydi, shuning uchun chalkashlik yana ko'payadi. Shu bobdagi LeBlanc qoidasi buni bir qatorga sig'diradi: "keyin" degani "hech qachon".

Shundan muhim amaliy xulosa kelib chiqadi: muddatni chalkashlik hisobiga ushlab qolish ishlamaydi. Martin buni asosiy ziddiyat deb ataydi - chalkashlik sizni darhol sekinlashtiradi, ya'ni aynan o'sha muddatni o'tkazib yuborishga majbur qiladi; tez borishning yagona yo'li kodni har doim iloji boricha toza tutish.

"Xato qilmayman" degan da'vo esa haqiqatga mos emas. McConnell *Code Complete* da intellektual halollikning birinchi belgilari sifatida bilmagan narsada ekspert bo'lib ko'rsatmaslikni va xatoni darhol tan olishni sanaydi, keyin bitta oson tekshiruvni qo'shadi: har masalada o'z ishonch darajangizni raqamlashga tayyor turing, agar u deyarli doim 100 foiz bo'lsa, bu ogohlantirish belgisi.

## 43.2 O'z xatosi uchun javob berish

Xato chiqqanda uchta ish bor: tan olish, oqibatni bartaraf etish va takrorlanmasligi uchun tizimni o'zgartirish. Uchinchisi eng ko'p e'tibordan chetda qoladi.

*Software Engineering at Google* ning 2-bobi ayblamaydigan post-mortem madaniyatini aynan shu uchinchi qism atrofida ta'riflaydi. Hujjat kechirim, bahona yoki barmoq bilan ko'rsatish ro'yxati bo'lmasligi kerak; unda nima o'rganilgani va natijada nima o'zgarishi yozilishi shart. Kitob sanaydigan tarkib: hodisaning qisqa bayoni, aniqlashdan hal qilishgacha vaqt chizig'i, asosiy sabab, ta'sir va zarar bahosi, muammoni darhol tuzatadigan harakatlar (har biri egasi bilan), takrorlanishini to'sadigan harakatlar va o'rganilgan saboqlar. Hujjat ochiq turishi va jamoa kelishilgan o'zgarishlarni oxirigacha bajarishi ham shu talabning qismi.

McConnell shu nuqtani shaxs darajasida aytadi: xatoni tan olmaslik hech kimni chalg'itmaydi, chunki xato allaqachon ko'rinadi. E'tiborsizlik bo'lmasa, xato murakkab aqliy ishning tabiiy qismi deb qabul qilinadi; tan olmaslik esa xatoning o'zidan og'irroq nuqson bo'lib qoladi. Shuning uchun xato bo'lsa, tez va aniq tan olinadi.

| Xato turi | Noto'g'ri javob | To'g'ri javob |
|---|---|---|
| Production da xato | bahona (muhit boshqa edi) | tuzatish va takrorlanishni to'sadigan harakat, egasi bilan |
| Noto'g'ri baho | "talab o'zgardi" | bahoni qayta ko'rish: McConnell bahoni loyiha davomida davriy qayta ko'rishni talab qiladi |
| Review da o'tkazib yuborilgan xato | "u yozgan" | post-mortem, ayblovsiz: nima o'rganildi va qoidada nima o'zgaradi |

Post-mortem hujjatining mexanikasi [ayblamaydigan post-mortem](../architect/35-incident-on-call-va-post-mortem.md#358-ayblamaydigan-post-mortem-tuzilishi-va-yozish-qoidalari) bo'limida.

## 43.3 Ishga layoqat: charchagan holda kod yozmaslik

McConnell diqqat bilan ishlashning kun ichidagi chegarasini *Code Complete* ning 33-bobida tasvirlaydi: ertalab 8 dan 14 gacha yaxshi ishlab, keyin to'xtash kerak bo'lgan holat programmistlarga tanish; 14 dan 17 gacha davom etilsa, haftaning qolgani aynan o'sha uch soatda yozilgan narsani tuzatishga ketadi. Bir kun yoki bir oy davomida ortiqcha diqqat sarflashdan keyingi kuyish ham shu bobda aytilgan.

Xuddi shu bobdagi "gonzo programming" tanqidi uzun tunlar haqida: tun bo'yi kod yozish o'zini dunyodagi eng yaxshi programmist deb his qilishga olib keladi, keyin esa o'sha jo'shqinlik paytida kiritilgan nuqsonlarni tuzatishga bir necha hafta ketadi. McConnell xulosasi qisqa: hayajon layoqat o'rnini bosmaydi.

Shu bobda McConnell yana bir chalkashlikni ajratadi: harakatni natija bilan, bandlikni unumdorlik bilan adashtirish oson. Samarali programmistlikdagi eng muhim ish o'ylash, o'ylab turgan odam esa band ko'rinmaydi.

Amaliy natija bitta: charchagan holda murakkab mantiq yozilmaydi. O'rniga hujjat, review yoki aniq va oddiy vazifa olinadi.

## 43.4 Mijoz va ishlab chiquvchi maqsadlari to'qnashuvi

Mijoz va boshqaruv tez va arzon natija xohlaydi, shu bosim ostida sifatni jim qurbon qilish eng oson yo'l bo'lib ko'rinadi. Martin *Clean Code* ning 1-bobida bu yo'lni professionalizmning yo'qligi deb baholaydi va javobgarlikni ishlab chiquvchiga qaytaradi: menejer va marketing va'da berish uchun kerakli ma'lumotni bizdan oladi, loyiha menejeri jadvalni biz bilan tuzadi, ya'ni biz rejalashtirishda chuqur qatnashamiz va nosozlik uchun javobgarlikni, ayniqsa u yomon kod sababli bo'lsa, bo'lishamiz. "Menejer shunday dedi" shuning uchun himoya emas.

Martin ikkinchi nuqtani ham aniq aytadi: jadvalni qizg'in himoya qilish menejerning ishi, kodni xuddi shunday qizg'in himoya qilish esa sizning ishingiz. Ko'pchilik menejer jadval haqida qattiq gapirsa ham haqiqatni va yaxshi kodni xohlaydi.

Nima muhokama qilinadi va nima qilinmaydi - Martin buni shifokor misolida ko'rsatadi. Bemor operatsiyadan oldin qo'l yuvishni "vaqt ketadi" deb to'xtatishni talab qilsa, buyurtmachi bemor bo'lsa ham, shifokor bajarmasligi kerak, chunki infeksiya xavfini u bemordan yaxshi biladi. Xuddi shunday, chalkashlik xavfini tushunmagan boshqaruvning irodasiga bo'ysunish professional emas.

To'g'ri yondashuv shundan kelib chiqadi: tanlovni oshkor qilish, narxini aytish va qarorni birga qabul qilish. Jim testsiz yozish esa qaror emas, yashirin qaror. Qamrov bilan sifat orasidagi tanlov [qamrovni qisqartirish yoki sifatni qisqartirish](45-baholash-muddat-va-bosim.md#457-qamrovni-qisqartirish-yoki-sifatni-qisqartirish) bo'limida.

## 43.5 Kasbiy etika: sir, ma'lumot, xavfsizlik

Professional xatti-harakatning etik o'lchovi bor. *Software Engineering at Google* ning 2-bobi jamoadan kutiladigan xatti-harakatlar ro'yxatida buni "to'g'ri ishni qilish" deb nomlaydi: har ishda kuchli etika hissi va jamoa hamda mahsulot butunligini saqlash uchun noqulay yoki og'ir qarorni qabul qilishga tayyorlik.

**Ma'lumot**. OWASP Logging Cheat Sheet qonuniy asos bo'lmasa ma'lumotni log ga yozmaslikni talab qiladi va log ga to'g'ridan-to'g'ri yozilmasligi kerak bo'lgan ro'yxatni beradi: parol, sessiya identifikatori, access token, shifrlash kalitlari va boshqa sirlar, baza ulanish satri, karta va bank hisobi ma'lumoti, sog'liq hamda davlat identifikatori kabi sezgir shaxsiy ma'lumot, tijorat siri va log tizimining xavfsizlik darajasidan yuqori ma'lumot. Ular o'rniga maskalangan, tozalangan, hashlangan yoki shifrlangan shakl yoziladi. Shaxs kimligi kerak bo'lmagan joyda esa to'g'ri va bilvosita identifikatorlarni o'chirish, chalkashtirish yoki psevdonimlashtirish tavsiya etiladi. Maskalashning kod darajasidagi mexanikasi [sezgir ma'lumot va maskalash](29-log-kodining-tozaligi.md#298-sezgir-malumot-va-maskalash) bo'limida.

**Xavfsizlik**. O'zingiz kiritgan zaiflikni yashirmaslik - bu [o'z xatosi uchun javob berish](#432-oz-xatosi-uchun-javob-berish) dagi "xatoni tez va aniq tan olish" qoidasining xavfsizlikdagi shakli, boshqa qoida emas.

## 43.6 Sifat me'yorini eng tajribali muhandis belgilaydi

Professional mas'uliyat tajriba bilan birga kengayadi: siz yozgan kod faqat sizning ishingiz emas, jamoaning me'yori bo'lib qoladi. Gergely Orosz buni to'g'ridan-to'g'ri aytadi - kichik tajribali hamkasblar sifat chegarasini eng tajribali muhandislardan oladi va ularning kodi ergashiladigan misol bo'ladi; jamoa sizning ishingizda chegara pastroq ekanini ko'rsa, bu boshqa joyda ham past standartni qonuniylashtiradi, chunki "unga mumkin bo'lsa, nega qolganlarga mumkin emas" (Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 23-bob, 322-bet).

Bu nazariy xavf emas, aniq vaziyatdan kelib chiqadi. Orosz tasvirlaydigan holat tanish: ko'nikma biroz zanglagan yoki ish shoshilinch bo'lgan paytda kod tez yoziladi va testsiz, tartibsiz, yarim tayyor PR ochiladi. Jamoa buni ko'radi va xulosa chiqaradi (o'sha manba, 322-bet).

Shundan ikki amaliy qoida kelib chiqadi. Birinchi, PR ning o'zi namuna sifatida tayyorlanadi: Orosz kod review ni ko'pincha o'rganish jarayoni deb ataydi va yaxshi PR qanday bo'lishini ko'rsatadigan, tavsifi to'liq va tushunarli PR yozishni tavsiya qiladi (o'sha manba, 322-bet). Ikkinchi, juftlikda ishlaganda yetakchilikni o'z qo'lingizga olmaslik: Orosz hamkasbni "to'g'ri" yo'l bo'ylab o'zingiz olib bormasdan, turtki berib yo'naltirishni maslahat beradi - bu o'zingiz qilganingizdan sekinroq, lekin jamoaning malakasini ko'taradi (o'sha manba, 322-bet).

Teskari xatti-harakatning nomi ham bor. Orosz "chayqa menejmenti" (seagull management) ni ogohlantirish sifatida keltiradi: yuqoridan kelib jamoaning ishiga aralashish, barqaror yechim emas, hack bo'lgan kodni commit qilish va kelgan tezlikda ketish (o'sha manba, 322-bet). Qiynalayotgan jamoaga yordam berish foydali, lekin qoldirilgan kodga egalik qilmaslik mas'uliyatning buzilishi.

Shu nuqta [zarar qilmaslik](#431-zarar-qilmaslik-funksiyaga-va-tuzilishga) bo'limidagi ikkinchi zararning jamoa darajasidagi shakli: zarar kod bazasiga emas, jamoada amal qiladigan me'yorga yetadi, va u kod bazasidan ko'ra sekinroq tuzatiladi.

## 43.7 Amalda qo'llash

- [ ] Oxirgi uch incidentni ko'rib chiqib, har biri uchun tizim o'zgarishi kiritilganini tekshiring.
- [ ] "Sifat me'yori muhokama qilinmaydi" ro'yxatini yozib, jamoa va menejer bilan kelishib oling.
- [ ] Charchagan holda merge va reliz qilmaslik qoidasini jamoa kelishuviga kiriting.
- [ ] Texnik qarz haqidagi suhbatni narx tilida olib borish uchun bitta misol tayyorlang ([qamrovni qisqartirish yoki sifatni qisqartirish](45-baholash-muddat-va-bosim.md#457-qamrovni-qisqartirish-yoki-sifatni-qisqartirish)).
- [ ] Production ma'lumotini test muhitiga ko'chirish tartibini (de-identifikatsiya bilan) hujjatlashtiring.
- [ ] Log va `toString` larda sezgir ma'lumot yo'qligini bir marta to'liq audit qiling ([sezgir ma'lumot va maskalash](29-log-kodining-tozaligi.md#298-sezgir-malumot-va-maskalash)).
- [ ] Topilgan zaifliklarni xabar qilish kanalini (kimga, qanday) aniq belgilang.
- [ ] O'z xatolaringizni yozib boradigan shaxsiy jurnal yuritib, har chorakda naqshlarni ko'rib chiqing.

## Manbalar

- Robert C. Martin, *Clean Code*, Prentice Hall, 2009, 1-bob (4-5 betlar) - chalkashlikning egalik narxi: har o'zgarish boshqa joyni buzishi, unumdorlikning nolga intilishi va LeBlanc qoidasi
- Robert C. Martin, *Clean Code*, Prentice Hall, 2009, 1-bob (6-bet) - asosiy ziddiyat: chalkashlik bilan muddat ushlanmaydi, tez borishning yagona yo'li kodni toza tutish
- Robert C. Martin, *Clean Code*, Prentice Hall, 2009, 1-bob (5-6 betlar) - rejalashtirishdagi ulush va javobgarlik, kodni jadval kabi himoya qilish, shifokor va qo'l yuvish misoli
- Steve McConnell, *Code Complete* 2-nashr, Microsoft Press, 2004, 33-bob (826-827 betlar) - intellektual halollik: ekspert bo'lib ko'rsatmaslik, xatoni darhol tan olish, ishonch darajasini raqamlash
- Steve McConnell, *Code Complete* 2-nashr, Microsoft Press, 2004, 33-bob (820-bet) - diqqatning kun ichidagi chegarasi va charchagan uch soatda yozilgan kodni keyin tuzatish
- Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 23-bob (322-bet) - sifat chegarasini eng tajribali muhandis belgilashi va past chegaraning qonuniylashishi, namunali PR, juftlikda turtki berish, "chayqa menejmenti" ogohlantirishi
- Steve McConnell, *Code Complete* 2-nashr, Microsoft Press, 2004, 33-bob (832-bet) - "gonzo programming": tun bo'yi yozilgan kodning nuqsonlarini tuzatishga ketgan haftalar
- Steve McConnell, *Code Complete* 2-nashr, Microsoft Press, 2004, 33-bob (830-bet) - harakatni natija bilan adashtirish, eng muhim ish o'ylash
- Steve McConnell, *Code Complete* 2-nashr, Microsoft Press, 2004, 28-bob (672-bet) - bahoni loyiha davomida davriy qayta ko'rish
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 2-bob - ayblamaydigan post-mortem tarkibi va "to'g'ri ishni qilish" xatti-harakati
- [OWASP, Logging Cheat Sheet](https://raw.githubusercontent.com/OWASP/CheatSheetSeries/72865b1e3b5754246a101778dc00b37f9c233373/cheatsheets/Logging_Cheat_Sheet.md) - log ga yozilmasligi kerak bo'lgan ma'lumot ro'yxati va de-identifikatsiya usullari
- ESLATMA: 43.5 sarlavhasidagi "sir" (mijoz ma'lumoti va ichki arxitektura haqida tashqarida gapirmaslik) uchun mavjud kitoblarda tasdiq topilmadi, shuning uchun bo'lim tanasida u yo'q
- ESLATMA: 43.6 dagi tekshiruv ro'yxati, shu jumladan production ma'lumotini test muhitiga ko'chirish tartibi va zaiflik haqida xabar qilish kanali, shu korpusning amaliy tavsiyasi, kitobdan olingan emas

---

[&larr; 42. Statik tahlil va avtomatik qoidalar](42-statik-tahlil-va-avtomatik-qoidalar.md) · [Mundarija](README.md) · [44. "Yo'q" va "ha" deyish: majburiyat tili &rarr;](44-yoq-va-ha-deyish-majburiyat-tili.md)
