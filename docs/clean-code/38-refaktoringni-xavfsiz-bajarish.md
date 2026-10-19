<!-- doc: clean-code | chapter: 38 | part: X. Hid katalogi va refaktoring harakatlari -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 38. Refaktoringni xavfsiz bajarish (Safe Refactoring Mechanics)

<details>
<summary>Bu bobdagi 18 bo'lim</summary>

- [38.1 Bir vaqtda bitta harakat](#381-bir-vaqtda-bitta-harakat)
- [38.2 Kompilyator va test bilan boshqarish](#382-kompilyator-va-test-bilan-boshqarish)
- [38.3 IDE refaktoringiga ishonish chegarasi](#383-ide-refaktoringiga-ishonish-chegarasi)
- [38.4 Refaktoringni mantiq o'zgarishidan ajratish](#384-refaktoringni-mantiq-ozgarishidan-ajratish)
- [38.5 Katta refaktoringni bo'lish: abstraksiya orqali shox](#385-katta-refaktoringni-bolish-abstraksiya-orqali-shox)
- [38.6 Refaktoringni to'xtatish nuqtasi](#386-refaktoringni-toxtatish-nuqtasi)
- [38.7 Refaktoring va ishlash: o'lchovsiz qadam qo'ymaslik](#387-refaktoring-va-ishlash-olchovsiz-qadam-qoymaslik)
- [38.8 Refaktoring commitlarini o'qiladigan ushlash](#388-refaktoring-commitlarini-oqiladigan-ushlash)
- [38.9 Evolyutsiyaning ikki turi: sifat oshadimi yoki pasayadimi (Kinds of Software Evolution)](#389-evolyutsiyaning-ikki-turi-sifat-oshadimi-yoki-pasayadimi-kinds-of-software-evolution)
- [38.10 Ongli tahrir va bitta maqsadli tahrir (Hyperaware va Single-Goal Editing)](#3810-ongli-tahrir-va-bitta-maqsadli-tahrir-hyperaware-va-single-goal-editing)
- [38.11 Imzoni saqlash (Preserve Signatures)](#3811-imzoni-saqlash-preserve-signatures)
- [38.12 Kompilyatorga tayanish (Lean on the Compiler)](#3812-kompilyatorga-tayanish-lean-on-the-compiler)
- [38.13 Testsiz monstr metodni qo'lda bo'lish (Introduce Sensing Variable, Extract What You Know, Coupling Count, Gleaning Dependencies)](#3813-testsiz-monstr-metodni-qolda-bolish-introduce-sensing-variable-extract-what-you-know-coupling-count-gleaning-dependencies)
- [38.14 Qo'lda ajratish strategiyasi (Skeletonize Methods, Find Sequences, Extract to the Current Class First, Be Prepared to Redo Extractions)](#3814-qolda-ajratish-strategiyasi-skeletonize-methods-find-sequences-extract-to-the-current-class-first-be-prepared-to-redo-extractions)
- [38.15 Farq bilan programmalash (Programming by Difference)](#3815-farq-bilan-programmalash-programming-by-difference)
- [38.16 Kodbaza bo'ylab mexanik o'zgarish (Large-Scale Change)](#3816-kodbaza-boylab-mexanik-ozgarish-large-scale-change)
- [38.17 Qadam yiqilganda: debug emas, oxirgi yaxshi commitga qaytish](#3817-qadam-yiqilganda-debug-emas-oxirgi-yaxshi-commitga-qaytish)
- [38.18 Amalda qo'llash](#3818-amalda-qollash)

</details>


Refaktoring - programma ko'rinadigan xatti-harakatini o'zgartirmasdan uning
ichki tuzilishini tushunarli va o'zgartirish arzonroq qiladigan o'zgarish
(Fowler 1999, 46-bet). "Ko'rinadigan xatti-harakatni o'zgartirmasdan" qismi
uni xavfli qiladi: har bir qadam regressiya kiritishi mumkin. Bu bobda shu
xavfni kamaytiradigan intizom.

Fowler ning o'zi 1999 da bu sohani yopiq deb hisoblamagan: "Problems with
Refactoring" bo'limi, uning so'zlari bilan, "men xohlagandan qisqaroq va
ko'proq taxminiy", chunki refaktoringning chegaralarini ko'rish uchun hali
yetarli tajriba yo'q edi (1-nashr, 54-bet). Shu sababli bu bobdagi qoidalar
ikki manbadan keladi: Fowler 1999 ning 2 va 4-boblari, va McConnell ning
*Code Complete* 24.4 "Refactoring Safely" bo'limi, u aynan shu mavzuga
bag'ishlangan.

Legacy kodda chok topish va bosqichma-bosqich almashtirish strategiyasi
[arxitektor hujjatidagi](../architect/README.md) legacy kod va bosqichma-bosqich
refaktoring bo'limida.

## 38.1 Bir vaqtda bitta harakat

Asosiy qoida McConnell da shunday yozilgan: eng oddiylaridan boshqa hamma
refaktoring bittadan bajariladi, va keyingisiga o'tishdan oldin qayta
kompilyatsiya va qayta test qilinadi (*Code Complete*, 2-nashr, 580-bet).
Sababi vaqt tejash emas: harakat kichik bo'lsa, uning hamma ta'sirini
to'liq tushunib turasiz.

McConnell shu bo'limda refaktoringdan oldin va keyin bajariladigan
qadamlarni ham sanaydi (579-581-bet):

| Qadam | Nima uchun |
|---|---|
| Boshlagan kodni saqlash | orqaga qaytish yo'li bo'lishi uchun |
| Harakatlarni kichik ushlash | o'zgarishning hamma ta'sirini tushunib turish |
| Bittadan bajarish, har biridan keyin kompilyatsiya va test | xato qaysi harakatdan kelganini bilish |
| Qadamlar ro'yxatini oldin yozish | har bir o'zgarishni kontekstda ushlash |
| "Parking lot" ro'yxati | hozir kerak bo'lmagan o'zgarishlar yo'lni chalg'itmasligi uchun |
| Tez-tez checkpoint | ko'chaga kirib qolganda ishlaydigan holatga qaytish |
| Kompilyator ogohlantirishlarini eng qattiq darajaga qo'yish | kompilyatordan o'tib ketadigan kichik xatolarni ushlash |

McConnell qoidani mutlaq qilmaydi, xavf darajasiga qarab moslaydi
(581-bet): "nomli konstanta bilan sehrli sonni almashtirish" kabi harakat
deyarli xavfsiz, shu sababli unda bir necha harakatni birga bajarib, faqat
qayta test qilish mumkin. Sinf yoki metod interfeysiga, baza sxemasiga yoki
boolean tekshiruvga tegadigan harakatlar xavfliroq: ularda bittadan borish,
kompilyator va unit testdan tashqari ikkinchi odamning reviewi yoki pair
programming qo'shiladi.

Shu yerdagi raqamlar McConnell da manbasi bilan berilgan (580-581-bet):
programmist o'zgarishni birinchi urinishda xato qilish ehtimoli 50 foizdan
yuqori (Yourdon 1986b); bir qatorli o'zgarishlarga ham review joriy qilgan
tashkilotda xato darajasi 55 foizdan 2 foizga tushgan (Freedman va Weinberg
1982); telekommunikatsiya tashkilotida o'zgarishlarni reviewdan o'tkazish
to'g'ri o'zgarish ulushini 86 foizdan 99.6 foizga ko'targan (Perrott 2004).
Xulosa McConnell ning o'z so'zlari bilan: oddiy o'zgarishga murakkab
o'zgarishday munosabat qilish kerak.

```bash
# Har bir harakatdan keyin: tez testlar (butun to'plam emas)
./mvnw -q -pl payment test -Dtest='*Test' -DfailIfNoTests=false

# Harakat ishladi: commit - bu McConnell aytgan checkpoint
git add -A && git commit -m "refactor: Payment dan TelephoneNumber ni ajratish"
```

## 38.2 Kompilyator va test bilan boshqarish

Testlar haqida Fowler ning gapi qat'iy: refaktoring qilmoqchi bo'lsangiz,
asosiy oldingi shart - mustahkam testlar. Refaktoringni avtomatlashtiradigan
asbob bo'lsa ham testlar kerak, chunki hamma refaktoringni avtomatlashtirish
uzoq vaqt imkonsiz bo'lib qoladi (1-nashr, 73-bet).

Fowler ikki qoida qo'yadi (1-nashr, 73-74-bet):

- Testlar to'liq avtomatik bo'lsin va o'z natijasini o'zi tekshirsin.
- Test to'plami xatoni topish vaqtini keskin qisqartiradigan detektor: tez
  va tez yurgizilsa, xato oxirgi bir necha daqiqada yozilgan kodda
  ekanligi ma'lum bo'ladi va uni topish daqiqalar ishiga aylanadi.

Kompilyator ikkinchi tomon. McConnell ni (580-bet) kompilyatorni eng qattiq
ogohlantirish darajasiga qo'yishni tavsiya qiladi: kichik xatolar deyarli
yozilgan zahoti ushlanadi. Lekin kompilyator hamma narsani ko'rmaydi, 38.3
shuning ro'yxati.

Testlar yo'q bo'lsa, birinchi qadam refaktoring emas, test. Legacy kodda
Feathers buning uchun aniq usul beradi: **characterization test** - kod
*nima qilishi kerak* emas, *aslida nima qilayotganini* qayd etadigan test.
Uni yozish algoritmi (*Working Effectively with Legacy Code*, 186-bet):

1. Kod bo'lagini test harness ichiga olish.
2. Yiqilishi aniq bo'lgan assertion yozish.
3. Yiqilish xabari xatti-harakatni aytib beradi.
4. Testni kod haqiqatan qaytargan natijani kutadigan qilib o'zgartirish.
5. Takrorlash.

Feathers nega shunday qilish kerakligini ham aytadi: legacy tizimda kod nima
qilayotgani u nima qilishi kerak bo'lganidan muhimroq; taxminga qarab test
yozish esa yana xato qidirishga aylanadi, maqsad esa o'zgarishni
aniqlashtirish (186-bet).

Kodni test harness ichiga olish uchun **chok** (seam) kerak: Feathers ning
ta'rifi bilan, chok - programmada xatti-harakatni shu joyning o'zini tahrir
qilmasdan o'zgartirish mumkin bo'lgan nuqta (31-bet).

Test yozish imkoni hozir bo'lmasa, Feathers ikki yo'l beradi: yangi
funksiyani alohida metodda yozib, uni kerakli joydan chaqirish (**Sprout
Method**, 59-bet) yoki mavjud metodni o'rab, yangi xatti-harakatni o'ram
ichiga qo'yish (**Wrap Method**, 67-bet). Ikkisida ham yangi kod testlanadi;
ogohlantirish Feathers ning o'zidan: chaqiruv nuqtalarini qamrab olmasangiz,
yangi kodning *ishlatilishi* testlanmagan qoladi (59-bet).

## 38.3 IDE refaktoringiga ishonish chegarasi

Asbobning maqsadi aniq: refaktoring asbobining asosiy vazifasi - programmistga
kodni qayta testlamasdan refaktoring qilish imkonini berish (Roberts va
Brant, Fowler 1999, 14-bob, 329-bet). Shu sababli asbobdan nimani kutish
mumkin emasligini bilish kerak.

Chegara kitobda oshkor aytilgan (1-nashr, 331-bet): xatti-harakatni to'liq
saqlash erishilmaydigan maqsad. Berilgan misol aynan Java haqida: programma
satr yasab, shu satr nomlagan metodni Reflection API bilan chaqirsa, metodni
qayta nomlash programmani asl kod tashlamagan istisno tashlaydigan qilib
qo'yadi. Xulosa ham shu yerda: refaktoringni buzadigan holatlar aniqlangan
bo'lsa, programmist yoki shu refaktoringdan voz kechadi, yoki asbob tuzata
olmagan joyni qo'lda tuzatadi.

`grep` bu yerda to'liq javob emas: matn asboblari `foo` nomli o'zgaruvchi
bilan `foo` nomli funksiyani ajrata olmaydi, shu sababli asbobning o'zi
semantik tahlilga tayanadi (1-nashr, 330-bet).

Shu korpus o'z stekida qayta nomlashdan keyin qo'lda tekshiradigan joylar
ro'yxatini yuritadi. Olti joy:

| Xavf | Nega asbob ko'rmaydi | Tekshiruv |
|---|---|---|
| Satr literalidagi nom | matn sifatida saqlangan | `grep` bilan qidirish (3.15) |
| Refleksiya va `Class.forName` | ish vaqtida hal qilinadi | grep + integratsion test |
| Spring XML va `@Value` kalitlari | kod emas | konfiguratsiyani grep |
| JPA `@Query` ichidagi maydon nomi | satr | repository testlari |
| Jackson `@JsonProperty` nomlari | API shartnomasi | contract test |
| SQL migratsiyalari | alohida fayl | migratsiya testi |

Birinchi ikki qator kitobda nomi bilan turadi (Reflection API misoli,
331-bet); qolgan to'rttasi shu ro'yxatning Spring stekiga moslangan davomi.

## 38.4 Refaktoringni mantiq o'zgarishidan ajratish

Bu qoidaning manbasi Kent Beck ning ikki shlyapa metaforasi, Fowler orqali
(1-nashr, 47-bet): dasturni rivojlantirganda vaqt ikki alohida ish orasida
bo'linadi - funksiya qo'shish va refaktoring. Funksiya qo'shganda mavjud kod
o'zgartirilmaydi, faqat yangi imkoniyat qo'shiladi va progress yangi test
qo'shib uni ishlatish bilan o'lchanadi. Refaktoring qilganda funksiya
qo'shilmaydi, faqat tuzilish o'zgaradi: yangi test qo'shilmaydi (ilgari
o'tkazib yuborilgan holat topilmasa) va test faqat interfeys o'zgarishini
qoplash uchun, shunda ham zarurat bo'lsa o'zgartiriladi.

Fowler shlyapani kuni bo'yi ko'p marta almashtirishni normal deb hisoblaydi;
talab bitta - hozir qaysi shlyapada ekanini bilib turish (1-nashr, 47-bet).
Bu 13.6 (formatlashni alohida commitga ajratish) ning umumiy shakli.

McConnell shu chiziqni teskari tomondan tasvirlaydi (*Code Complete*,
582-bet): refaktoringning eng yomon muammosi - uni niqob qilib ishlatish.
Programmist "refaktoring qilayapman" deydi, aslida esa kodni ishlaydigan
qilish uchun paypaslab o'zgartiradi. Refaktoring - *ishlaydigan* koddagi,
xatti-harakatni o'zgartirmaydigan o'zgarish; buzilgan kodni paypaslash
refaktoring emas, hacking.

```bash
# Ikki commit, ikki shlyapa
git commit -m "refactor: SettlementService dan import mantiqini ajratish"
git commit -m "feat: import faylida valyuta tekshiruvini qo'shish"
```

Tartib Fowler da ham bir tomonlik emas: siz yangi funksiya qo'shishni
boshlaysiz, kod boshqa tuzilishda bo'lsa osonroq bo'lishini payqaysiz,
shlyapani almashtirib refaktoring qilasiz, keyin funksiyani qo'shasiz. Taqiq
faqat bittasiga: ikki ishni bir vaqtda qilmaslik.

## 38.5 Katta refaktoringni bo'lish: abstraksiya orqali shox

Katta refaktoring kichiklaridan sifat jihatidan farq qiladi va buni Beck
bilan Fowler alohida bobda ta'kidlaydi (1-nashr, 12-bob, 293-bet):

- Qadamlar kichik refaktoringlardagiday batafsil yozilmaydi, chunki vaziyat
  har safar boshqa: metodga parametr qo'shishda qamrov aniq, chalkash
  ierarxiyani yechishda har bir chalkashlik o'ziga xos.
- Vaqt o'lchovi boshqa. 6-11-boblardagi harakatlar bir necha daqiqada yoki
  ko'pi bilan bir soatda bajariladi; katta refaktoringlar bo'yicha mualliflar
  ishlaydigan tizimlarda oylab va yillab ishlagan.
- Shu sababli yo'l bitta: progressni ikki oyga to'xtatib turishga ruxsat
  so'ramaslik, chekkalaridan tishlab borish - bugun bir oz, ertaga yana bir
  oz.
- Harakatni o'z ishingiz boshqarsin: refaktoring funksiya qo'shish va xato
  tuzatish ehtiyoji bilan bajariladi. Boshlagan refaktoringni oxirigacha
  bajarish shart emas; hozirgi vazifaga yetadigancha qilib, qolganiga
  ertaga qaytiladi.
- Katta refaktoring butun jamoaning kelishuvini talab qiladi, kichiklari
  esa yo'q: u ko'p o'zgarishning yo'nalishini belgilaydi, shu sababli jamoa
  qaysi katta refaktoring "o'ynalayotganini" bilib turishi kerak.

McConnell shu yerga Beck ning qisqa xulosasini keltiradi: katta refaktoring -
falokat retsepti (*Code Complete*, 582-bet). Uning ikkinchi ogohlantirishi
ham shu bo'limda: o'zingizni katta refaktoring seansida ko'rsangiz, o'zingizdan
shu bo'lakni noldan qayta loyihalash va qayta yozish kerakmi deb so'rang.

Fowler bitta oraliq yo'lni ko'rsatadi (1-nashr, 56-bet): katta tizimni
avval kuchli inkapsulyatsiyali komponentlarga ajratish, keyin har bir
komponent uchun "refaktoring qilamizmi yoki qayta yozamizmi" qarorini
alohida qabul qilish. Fowler buni istiqbolli yo'nalish deb ataydi va legacy
tizim uchun jozibali deydi, lekin unga qoida yozish uchun ma'lumot
yetishmasligini oshkor tan oladi.

Bu korpusda shu "tishlab borish" intizomining amaliy shakli - abstraksiya
ortida ishlash:

1. Mavjud implementatsiya ustiga abstraksiya (interfeys) qo'yish va barcha
   chaqiruvchilarni unga o'tkazish. Merge qilinadi.
2. Yangi implementatsiyani abstraksiya ortida yozish, hali ishlatilmaydi.
   Merge qilinadi.
3. Konfiguratsiya yoki feature flag bilan trafikni bosqichma-bosqich
   yangisiga o'tkazish (41.5). Merge qilinadi.
4. Eski implementatsiyani o'chirish. Merge qilinadi.

Har bir qadam mustaqil ravishda production ga chiqadi va orqaga qaytarish
oson. Bu to'rt qadamli shakl shu korpusning tavsiyasi; kitoblardagi asos -
yuqoridagi "chekkalaridan tishlab borish" va "komponent bo'yicha qaror"
printsiplari.

## 38.6 Refaktoringni to'xtatish nuqtasi

Refaktoring cheksiz davom etishi mumkin, chunki har qanday programmada
foydali bo'lishi mumkin bo'lgan refaktoring soni amalda cheksiz. McConnell
mezonni shunday qo'yadi (*Code Complete*, 582-bet): refaktoring ham boshqa
programmalash ishlari kabi kamayuvchi qaytim qonuniga bo'ysunadi va unda
80/20 qoidasi ishlaydi - foydaning 80 foizini beradigan 20 foiz
refaktoringga vaqt sarflash kerak.

To'xtatish shartlari, manbasi bilan:

| To'xtatish sharti | Manba |
|---|---|
| Hozirgi vazifaga yetadigancha qilindi | Fowler 1999, 293: boshlagan refaktoringni tugatish shart emas |
| Kod ishlamayotgani aniqlandi | Fowler 1999, 56: refaktoringdan oldin kod ko'pincha to'g'ri ishlashi kerak; test bilan barqarorlashtirib bo'lmasa, qayta yozish kerak |
| Keyingi qadam test talab qiladi | Fowler 1999, 73: mustahkam test asosiy oldingi shart |
| Muddat juda yaqin | Fowler 1999, 56: refaktoring foydasi muddatdan keyin ko'rinadi, demak kech bo'ladi |
| Keyingi foyda 80/20 ning quyruq qismida | McConnell 582 |
| Hozir kerak bo'lmagan o'zgarish chiqdi | McConnell 579: "parking lot" ro'yxatiga yoziladi |
| Qaror arxitektura darajasiga chiqdi | shu korpus qoidasi: ADR kerak ([arxitektor hujjatidagi](../architect/README.md) ADR va qaror hujjatlashtirish bo'limi) |

Muddat masalasida Fowler ning qo'shimchasi muhim: muddat juda yaqin
bo'lmasa, "vaqt yo'q" degan sabab bilan refaktoringni kechiktirmaslik kerak.
Bir necha loyiha tajribasi shuni ko'rsatgan: refaktoring seansi
unumdorlikni oshiradi, va vaqt yetmayotgani odatda refaktoring kerak
ekanining belgisi (1-nashr, 56-57-bet). Ward Cunningham ning shu yerda
keltirilgan metaforasi: tugallanmagan refaktoring - qarzga kirish; ko'p
tashkilot samarali ishlash uchun biror qarzga kiradi, lekin qarz bilan
foiz ham keladi - haddan oshgan murakkab kod keltirgan qo'shimcha
qo'llab-quvvatlash va kengaytirish narxi.

Shu toifadagi ikkinchi signal xato xabari: xato xabari kelsa, bu kod xatoni
ko'rishga yetarlicha ravshan bo'lmaganini bildiradi, ya'ni refaktoring kerak
ekanining belgisi (2-nashr, 51-bet). Shuning uchun xato tuzatish ikki
qadamdan iborat bo'ladi - avval xatoni ko'rinadigan qiladigan refaktoring,
keyin tuzatishning o'zi. Tartib teskari bo'lsa, kod shu joyda yana xato
yashirish qobiliyatini saqlab qoladi va keyingi xato ham shu yerdan
chiqadi.

## 38.7 Refaktoring va ishlash: o'lchovsiz qadam qo'ymaslik

Fowler bu masalada chetlab o'tmaydi: refaktoring programmani sekinlashtiradi,
lekin uni sozlashga qulay qiladi; tez programmaning siri (qattiq real vaqt
konteksti bundan tashqari) - avval sozlanadigan programma yozib, keyin uni
yetarli tezlikka sozlash (1-nashr, 59-bet).

Kitob tez programma yozishning uch yo'lini sanaydi (1-nashr, 59-60-bet):

| Yo'l | Mazmuni | Qachon |
|---|---|---|
| Vaqt byudjeti | dizaynni parchalaganda har bir komponentga vaqt va hajm byudjeti beriladi va u oshmaydi | qattiq real vaqt tizimlari, masalan yurak stimulyatori |
| Doimiy e'tibor | har bir programmist har doim ishlashni yuqori ushlashga harakat qiladi | intuitiv jozibali, lekin yaxshi ishlamaydi |
| Kech, maqsadli optimizatsiya | kod yaxshi tuzilgan holda yoziladi, optimizatsiya alohida bosqichda, profiler bilan | qolgan hamma holat |

Ikkinchi yo'lning nega ishlamasligi aniq aytilgan: ishlashni yaxshilaydigan
o'zgarishlar kodni qiyinlashtiradi va natijada programma odatda tezroq ham
bo'lmaydi. Sababi statistik: programmalar vaqtining ko'p qismini kodning
kichik ulushida sarflaydi, shu sababli hamma kodni teng optimizatsiya
qilsangiz, optimizatsiyalarning 90 foizi behuda ketadi - ko'p ishlamaydigan
kod optimizatsiya qilinadi (1-nashr, 59-bet).

Uchinchi yo'lning qadamlari (1-nashr, 60-bet): programmani profiler ostida
yurgizib, vaqt va xotira sarflanayotgan nuqtani topish → shu nuqtaga
e'tiborni qaratib optimizatsiya qilish → o'zgarishni, refaktoringdagiday,
kichik qadamlarda qilish → har qadamdan keyin kompilyatsiya, test va
profilerni qaytadan yurgizish → ishlash yaxshilanmasa, o'zgarishni qaytarish
→ foydalanuvchini qanoatlantiradigan natijaga yetguncha davom etish.

Qoida, kitobdagi hikoyadan (Ron Jeffries, 1-nashr, 59-bet): tizimda nima
bo'layotganini aniq bilsangiz ham ishlashni o'lchang, taxmin qilmang.
Jeffries ning jamoasi juda yaxshi bilgan kodda muammo qayerda ekanini
muhokama qilib, hatto yaxshilash eskizlarini chizgan; o'lchagandan keyin
ma'lum bo'lgan narsa - ular butunlay noto'g'ri edi.

Refaktoring harakatlarining ishlashga ta'siri shu korpusda kuzatilgan:
Replace Derived Variable with Query
([35.20](35-refaktoring-harakatlari-katalogi-i-funksiya.md#3520-hosila-ozgaruvchini-sorovga-almashtirish))
hisobni har chaqiruvda bajaradi, Extract Function qo'shimcha chaqiruv
qo'shadi, Replace Loop with Pipeline qo'shimcha obyektlar yaratadi. Qaysi
biri sezilarli ekanini faqat o'lchov aytadi, shu sababli har biriga
umumiy qoida qo'llanadi: refaktoringni o'qilishi uchun bajarish, keyin
o'lchash, muammo chiqsa maqsadli optimizatsiya qilish va **nega** shunday
qilinganini izohlash (8.4).

## 38.8 Refaktoring commitlarini o'qiladigan ushlash

Versiya nazorati bu bobda ikki vazifani bajaradi. Birinchisi McConnell
dan (*Code Complete*, 579-bet): boshlagan kodni versiya nazoratiga saqlash
va seans ichida checkpointlar qoldirish - bu refaktoringni qaytarish
imkonini beradigan narsa. Ikkinchisi tarix: refaktoring commiti keyinchalik
"bu sinf nega shunday bo'lgan?" savoliga javob beradi.

Reviewer uchun eng ishonchli signal Fowler ning ikki shlyapa qoidasidan
kelib chiqadi: refaktoring shlyapasida test faqat interfeys o'zgarishini
qoplash uchun o'zgartiriladi (1-nashr, 47-bet). Demak diffda testlar
o'zgarmagani - xatti-harakat o'zgarmaganining tekshiriladigan belgisi.
Buning teskarisi ham ishlaydi: refaktoring commitida testlar o'zgargan
bo'lsa, nega o'zgarganini tushuntirish kerak.

Shu korpus commit xabarining shaklini quyidagicha yuritadi (40.2 bilan
birga). Bu kitoblardan olingan emas, lekin yuqoridagi ikki signalni
commitda ko'rinadigan qiladi:

```text
refactor: Payment dan TelephoneNumber value object ini ajratish

Extract Class: officeAreaCode va officeNumber maydonlari birga sayohat
qilayotgan edi va formatlash mantiqi uch joyda takrorlangan.

Xatti-harakat o'zgarmadi; mavjud testlar o'zgartirilmagan.
```

## 38.9 Evolyutsiyaning ikki turi: sifat oshadimi yoki pasayadimi (Kinds of Software Evolution)

Bu bob o'zgarishni qanday qilishni aytadi; shu bo'lim o'zgarishni nimaga
qarab baholash kerakligini aytadi. McConnell refaktoring bobini bitta
ajratish bilan boshlaydi: evolyutsiya turlarini bir-biridan ajratadigan
asosiy farq - o'zgarish ostida programmaning sifati oshadimi yoki
pasayadimi (McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004,
24.1 (564-bet)). Xatoni "mantiqiy skotch va irim" bilan tuzatsangiz sifat
pasayadi; o'zgarishni dastlabki dizaynni mahkamlash imkoniyati deb
qarasangiz sifat oshadi. Sifat pasayayotgani ko'rinsa, McConnell buni
shaxtadagi kanareyka signaliga tenglashtiradi: programma noto'g'ri
yo'nalishda rivojlanyapti.

Ikkinchi ajratish - o'zgarish qachon kiritilyapti (564-bet):

| | Construction paytida | Maintenance paytida |
|---|---|---|
| Kim kiritadi | odatda kodni yozgan odamning o'zi | ko'pincha boshqa odam |
| Kod yodidami | ha, hali esdan chiqmagan | yo'q |
| Bosim | faqat muddat bosimi | ishlab turgan tizim va foydalanuvchi |
| Xato narxi | past, harakat erkinroq | yuqori |

Shu farq intizom darajasini belgilaydi: construction da bir necha kichik
harakatni birga bajarish mumkin bo'lgan joyda (38.1) maintenance da
bittadan borish va ikkinchi odamning reviewi kerak bo'ladi.

McConnell ning asosiy qoidasi (*Cardinal Rule of Software Evolution*):
evolyutsiya programmaning ichki sifatini oshirishi shart (565-bet). Uning
amaliy shakli ham shu yerda: o'zgarish kiritish kerak bo'lganda kodni
keyingi o'zgarish osonlashadigan qilib yaxshilashga harakat qilish, chunki
programmani yozishni boshlaganda u haqida keyinchalik bilgancha hech qachon
bilmaysiz (564-bet).

```java
// Sifatni pasaytiradigan tuzatish: alomat bosiladi, sababi yozilmaydi
public BigDecimal total(Order order) {
    if (order.getLines() == null) {   // nega null bo'lishi mumkin - noma'lum
        return BigDecimal.ZERO;
    }
    return order.getLines().stream()
            .map(OrderLine::amount)
            .reduce(BigDecimal.ZERO, BigDecimal::add);
}

// Sifatni oshiradigan tuzatish: null ning manbasi yopiladi
public final class Order {
    private final List<OrderLine> lines;

    public Order(List<OrderLine> lines) {
        this.lines = List.copyOf(lines);   // null ham, keyingi mutatsiya ham yo'q
    }
}
```

## 38.10 Ongli tahrir va bitta maqsadli tahrir (Hyperaware va Single-Goal Editing)

38.1 refaktoring harakatining hajmini kichik ushlaydi. Feathers shu
intizomni bir pog'ona pastga tushiradi: tahrirning o'ziga va tahrir
seansining maqsadiga.

**Hyperaware Editing** (ongli tahrir). Klaviaturaga o'tirganda har bir tugma
bosishini ikki toifadan biriga kiritish mumkin: u programmaning
xatti-harakatini o'zgartiradi yoki o'zgartirmaydi (Feathers, *Working
Effectively with Legacy Code*, Prentice Hall PTR, 2004 (copyright 2005),
23-bob, 310-bet). Izoh ichidagi matn o'zgartirmaydi; satr literali ichidagi
matn ko'pincha o'zgartiradi, lekin kod hech qachon chaqirilmasa yo'q -
o'zgartiradigani keyin shu literalni ishlatadigan chaqiruvni tugatadigan
tugma bosishi bo'ladi. Ishlatilayotgan ifodadagi son literalini o'zgartirish
refaktoring emas, funksional o'zgarish. Feathers ning xulosasi:
programmalashning mag'zi - har bir tugma bosishi nima qilayotganini aniq
bilish. Bu hammasini bilishni talab qilmaydi, teskari aloqani talab qiladi:
bir sekunddan kam ishlaydigan test to'plami va pair programming shu aloqani
beradi. Aloqa bo'lmaganda nimani o'zgartirganini va nimani o'zgartirmaganini
boshda ushlab turish kerak bo'ladi va charchoq aynan shundan keladi
(310-bet).

**Single-Goal Editing** (bitta maqsadli tahrir). Feathers ning o'ziga
qaratgan mantrasi: programmalash - bir vaqtda bitta ishni qilish san'ati
(311-312-bet). Pair da ishlaganda u sherigidan "hozir nima qilyapsan?" deb
so'rashni talab qiladi; javob bittadan ko'p ish nomlasa, bittasi tanlanadi
va qolgani qog'ozga yoziladi - bu 38.1 jadvalidagi "parking lot" ning
tahrir darajasidagi shakli. Sababi tartib emas, tezlik: bir vaqtda juda
katta bo'lak olinsa, ish ongli borishdan "ishlab ketsin" deb paypaslashga
aylanadi.

```java
// Xatti-harakatni o'zgartirmaydigan tahrir: izoh, bo'shliq, qator uzilishi
public Money fee(Money amount) {
    // tarif 2025-01-01 dan beri o'zgarmagan
    return amount.multiply(STANDARD_RATE);
}

// Xatti-harakatni o'zgartiradigan tahrir: ishlatilgan ifodadagi son literali.
// Bu refaktoring emas; alohida commit va alohida test talab qiladi (38.4).
private static final BigDecimal STANDARD_RATE = new BigDecimal("0.015");
```

## 38.11 Imzoni saqlash (Preserve Signatures)

Refaktoring xatoga ayniqsa moyil, chunki tahrir bosqinchi: bo'laklar
ko'chiriladi, yangi sinf va metod yaratiladi, hajm bitta qator qo'shishdan
ancha katta (Feathers, *Working Effectively with Legacy Code*, Prentice Hall
PTR, 2004 (copyright 2005), 23-bob, 312-bet). Odatdagi javob - test. Lekin
ko'p tizimda testni yozish uchun avval bir oz refaktoring qilish kerak
bo'ladi: shu dastlabki harakatlar (Feathers ning bog'liqlikni uzish
texnikalari, 25-bob) testsiz bajariladi va shu sababli ayniqsa ehtiyotkor
bo'lishi shart. Shu nuqtada 38.2 ning "avval test yoz" qoidasi javob
bermaydi, chunki test yozish yo'li shu refaktoringning o'zidan o'tadi.

Feathers o'z xatosini aytib beradi (313-bet): metod tanasini ajratish kerak
bo'lganda u bir vaqtning o'zida dizaynni ham yaxshilashga urinib,
parametrlarni yangi yordamchi sinflarga o'rab yuborgan. Niyat yaxshi edi,
natija - testsiz ushlanmaydigan va kerak bo'lganidan ancha keyin topiladigan
xatolar.

Qoida: test uchun bog'liqlikni uzayotganda imzo imkoni boricha
o'zgartirilmaydi. Imzo butunligicha o'zgarmasa, uni bir joydan ikkinchisiga
nusxa-joylashtirish bilan ko'chirish mumkin bo'ladi va xato ehtimoli
minimumga tushadi (313-bet). Mexanika, Feathers ning olti qadami (314-bet):

1. Butun parametr ro'yxatini buferga nusxalash.
2. Yangi metod e'lonini bo'sh qavs bilan yozish.
3. Buferni e'lon qavsiga joylashtirish.
4. Yangi metod chaqiruvini bo'sh qavs bilan yozish.
5. Buferni chaqiruv qavsiga joylashtirish.
6. Chaqiruvdagi turlarni o'chirib, faqat argument nomlarini qoldirish.

```java
// Oldin: tana ajratilishi kerak, test esa hali yo'q
public void process(List<Order> orders, int dailyTarget,
                    BigDecimal interestRate, int compensationPercent) {
    // uzun va chalkash mantiq
}

// Keyin: imzo nusxa-joylashtirilgan, birorta parametr qo'lda qayta yozilmagan
public void process(List<Order> orders, int dailyTarget,
                    BigDecimal interestRate, int compensationPercent) {
    processOrders(orders, dailyTarget, interestRate, compensationPercent);
}

private static void processOrders(List<Order> orders, int dailyTarget,
                                  BigDecimal interestRate, int compensationPercent) {
    // ko'chirilgan mantiq
}
```

Shu bosqichda parametrlarni `OrderBatch` yoki `CompensationTarget` kabi yangi
obyektga o'rash jozibali ko'rinadi va aynan shu Feathers ogohlantirgan xato:
dizaynni yaxshilash keyingi qadam, hozir esa faqat imzoning nusxasi.
Qadamlar avtomatlashgandan keyin diqqat qolgan xavflarga bo'shaydi; Feathers
bittasini nomlab ko'rsatadi - yangi metod bazaviy sinfdagi bir xil imzoli
metodni yashirib qo'ymadimi (314-bet). Ikkinchi qo'llanish joyi: Break Out
Method Object harakatida metodning barcha argumentlari uchun maydon va
kirish metodlari yasashda ham shu nusxa-joylashtirish ishlatiladi (314 va
330-bet).

ESLATMA: IDE ning shu kodda ishlaydigan `Extract Method` i bo'lsa bu qoida
kerak emas, u asbob yo'q yoki asbob bu kodni qo'lidan chiqarmaydigan holat
uchun (38.3). Imzoni atayin o'zgartirish kerak bo'lsa, u alohida qadam
bo'ladi: Change Function Declaration
([funksiya e'lonini o'zgartirish](35-refaktoring-harakatlari-katalogi-i-funksiya.md#355-funksiya-elonini-ozgartirish-change-function-declaration)).

## 38.12 Kompilyatorga tayanish (Lean on the Compiler)

Statik turlangan tilda kompilyator faqat tarjimon emas: uning tur
tekshiruvini kerakli o'zgarishlarni topish uchun ishlatish mumkin. Feathers
bu amaliyotni *leaning on the compiler* deb ataydi (Feathers, *Working
Effectively with Legacy Code*, Prentice Hall PTR, 2004 (copyright 2005),
23-bob, 315-bet) va ikki qadamga ajratadi (316-bet):

1. E'lonni atayin o'zgartirib kompilyatsiya xatosi chiqarish.
2. Har bir xatoga borib, kerakli o'zgarishni kiritish.

Ikki xil qo'llanishi bor (316-bet). Birinchisi tuzilish o'zgarishi: global
e'lonlarni sinf ichiga o'rab, kompilyator topgan har bir joyni yangi obyekt
orqali murojaat qiladigan qilish. Ikkinchisi tur o'zgarishi va eng ko'p
uchraydigani shu: o'zgaruvchi e'lonining turini konkret sinfdan interfeysga
almashtirib, chiqqan xatolar bo'yicha interfeysda qaysi metodlar bo'lishi
kerakligini aniqlash. Kitobdagi misol C++ dagi global o'zgaruvchilar
haqida; Java da global o'zgaruvchi yo'q, shu sababli g'oyaning to'g'ri
keladigan shakli - ikkinchi qo'llanish:

```java
// 1-qadam: e'lonni atayin "buzish" - konkret turni hali bo'sh interfeysga almashtirish
public class SettlementService {
    private final PaymentGateway gateway;   // oldin: StripePaymentGateway
}

// 2-qadam: kompilyatorning har bir "cannot find symbol" xatosi interfeysga
// kerak bo'lgan metodni ko'rsatadi. Ro'yxat kompilyatordan keladi, taxmindan emas.
public interface PaymentGateway {
    PaymentResult charge(Money amount, CardToken token);
    void refund(PaymentId id);
}
```

Kalit nuqta Feathers da oshkor aytilgan (315-bet): kompilyator sizning
o'rningizga o'ylamaydi, faqat yurib chiqadigan ishni bajaradi, shu sababli
uning nimani topadigani va nimani topmasligini bilish shart - aks holda u
yolg'on ishonch beradi. Chegaralari:

- Build uzoq bo'lsa bu amaliyot amaliy emas: joylarni qidirib topish tezroq
  (316-bet).
- Eng xavfli til imkoniyati - vorislik, va kitobdagi misol aynan Java da:
  sinfdagi `getX()` metodini izohga olib kompilyatsiya qilasiz va hech
  qanday xato chiqmaydi. Bu `getX()` ishlatilmayotganini bildirmaydi - agar
  `getX()` super sinfda konkret metod bo'lsa, izohga olish shunchaki super
  sinfdagisini ishlatadigan qilib qo'yadi. Maydonlar bilan ham shunday
  bo'ladi (316-bet).
- Ko'r-ko'rona bajarilsa texnika nozik xato kiritadi (316-bet).

ESLATMA: shu vorislik tuzog'ini Java da aniqlash uchun metodni izohga olish
o'rniga qayta nomlash ishonchliroq, chunki o'sha paytda haqiqiy chaqiruvchilar
kompilyatsiyadan o'tmaydi; `@Override` annotatsiyasi esa teskari tomonni
ushlaydi, ya'ni super sinfda yo'q metodni override qilishni. Bu ikkisi
kitobda yo'q, korpusning qo'shimchasi.

## 38.13 Testsiz monstr metodni qo'lda bo'lish (Introduce Sensing Variable, Extract What You Know, Coupling Count, Gleaning Dependencies)

Eng og'ir holat: metod katta, IDE ning ishlaydigan refaktoring asbobi yo'q
va metodni test harness ichiga olish ham qiyin. Feathers bu holatga alohida
bob bag'ishlaydi (Feathers, *Working Effectively with Legacy Code*, Prentice
Hall PTR, 2004 (copyright 2005), 22-bob, 289-307-bet) va ikki xil monstrni
ajratadi: **bulleted method** - deyarli chekinishsiz, ketma-ket kod
bo'laklaridan iborat metod (290-bet); **snarled method** - bitta katta
chekingan bo'lak hukmron bo'lgan metod, eng oddiy holi bitta ulkan shart
(292-bet).

Qo'lda Extract Method qilganda nima xato bo'lishi mumkin (297-bet):

| Xato | Nega ushlanmaydi |
|---|---|
| o'zgaruvchini ajratilgan metodga uzatish esdan chiqadi | nomi maydon nomi bilan bir xil bo'lsa kompilyator jim qoladi, siz esa uni lokal deb e'lon qilib qo'yasiz |
| ajratilgan metod nomi bazaviy sinf metodini yashiradi yoki override qiladi | kompilyatsiya o'tadi |
| parametr uzatish yoki qaytarish qiymatida xato, ayniqsa noto'g'ri tur | turlar bir-biriga keltirilsa kompilyator o'tkazib yuboradi |

Shu uch xatoni kamaytiradigan to'rt taktika bitta oilani tashkil qiladi:

- **Introduce Sensing Variable** (298-301-bet). Refaktoring paytida
  production kodga funksiya qo'shilmaydi, lekin kod qo'shish taqiqlanmagan:
  sinfga vaqtincha maydon qo'shib, ajratmoqchi bo'lgan metod ichidagi
  shartni "sezish" mumkin. Keyin shu shartni qoplaydigan kirish
  tayyorlanadi, bo'lak ajratiladi va test hali ham o'tishi kerak. Feathers
  ning qo'shimcha qoidasi: sezgir maydonni bitta ajratishdan keyin
  o'chirmang, butun seans davomida sinfda qoldiring - shunda yozgan
  testlaringiz ko'rinib turadi va ajratishni boshqacha qilishni xohlasangiz
  qaytarish oson (301-bet). Seans oxirida maydon ham, uni tekshirgan test
  ham o'chiriladi yoki test ajratilgan metodni tekshiradigan qilib qayta
  yoziladi.
- **Extract What You Know** (301-302-bet). Kichikdan boshlash: testsiz,
  ishonch bilan ajratadigan bo'laklarni topib ajratish va keyin ularga test
  yozish. "Kichik" ning o'lchovi kitobda aniq - ikki-uch qator, ko'pi bilan
  besh, nom berish oson bo'lgan bo'lak. Progress ko'rinmaydi, lekin har bir
  kichik ajratish metodni bir oz aniqlashtiradi va vaqt o'tib metodning
  shakli boshqacha ko'rinib qoladi.
- **coupling count**. Kichik ajratishda qaraladigan o'lchov: ajratilayotgan
  metodga kiradigan va undan chiqadigan qiymatlar soni (301-bet). Ikki
  argumentdan maksimumni hisoblaydigan bo'lakni ajratsangiz count 3 ga
  teng - ikki kirish, bir chiqish. Maydonlarga murojaat hisobga kirmaydi:
  ular metod interfeysidan o'tmaydi, shunchaki ko'chib ketadi. Kichik count
  afzal, chunki asosiy xavf tur konversiyasi xatosi; count 0 esa eng
  xavfsiz, ya'ni parametr qabul qilmaydigan va qiymat qaytarmaydigan
  buyruq-metodlar. Feathers asbob bo'lmaganda umumiy tuzilishni ko'rish
  uchun aynan 0-count metodlardan boshlaydi (302-bet). Nomzod topilganda
  har bir uzatiladigan o'zgaruvchi qayerda e'lon qilinganini qaytib
  tekshirish kerak, imzo shundan to'g'ri chiqadi; count 0 dan katta bo'lsa
  ko'pincha sezgir o'zgaruvchi qo'shish foyda beradi.
- **Gleaning Dependencies** (303-bet). Monstr metodda ikkinchi darajali kod
  bo'ladi: kerakli, lekin murakkab emas va buzilsa darhol ko'rinadi. Shu
  holatda tartib teskari: avval saqlanishi shart bo'lgan muhim mantiq uchun
  test yoziladi, keyin test qoplamagan narsalar ajratiladi. Feathers buni
  o'zi "qochish kabi ko'rinadi" deb tan oladi va sababini ham aytadi:
  ilovada hamma xatti-harakat teng emas, ba'zilari muhimroq.

```java
public class InvoiceBuilder {

    // Vaqtincha sezgir maydon: faqat ajratish seansi davomida turadi
    boolean lineAdded = false;

    void addLines(Invoice invoice, List<Order> orders) {
        for (Order order : orders) {
            if (isBillable(order)) {   // ajratilgan shart
                invoice.add(order);
                lineAdded = true;      // shart ajratishdan keyin ham yo'lda qolganini ko'rsatadi
            }
        }
    }

    private boolean isBillable(Order order) {
        return order.type() == OrderType.RECURRING || order.type() == OrderType.ONE_OFF;
    }
}
```

## 38.14 Qo'lda ajratish strategiyasi (Skeletonize Methods, Find Sequences, Extract to the Current Class First, Be Prepared to Redo Extractions)

38.13 taktika beradi, bu bo'lim esa bo'laklarni qanday chizish haqidagi
strategiya (Feathers, *Working Effectively with Legacy Code*, Prentice Hall
PTR, 2004 (copyright 2005), 22-bob, 304-307-bet).

Shartli gapni ajratganda ikki yo'l bor va Feathers ularning ikkisini ham
tavsiya qiladi:

- **Skeletonize Methods** (304-305-bet): shartni va tanani ikki alohida
  metodga ajratish. Natijada asl metodda faqat skelet qoladi, ya'ni
  boshqaruv tuzilishi va delegatsiyalar; mantiqni keyinchalik qayta
  tartiblash osonlashadi.
- **Find Sequences** (305-bet): shartni va tanani bitta metodga ajratish.
  Natijada metodning qolgani ketma-ket bajariladigan amallar qatoriga
  o'xshab qoladi va shu ketma-ketlikni ko'rish oson bo'ladi.

Feathers ikkisi bir-biriga zid maslahat ekanini oshkor aytadi va ikkisi
orasida borib-kelib ishlaydi (305-bet). Tanlov mezoni:

| Hozirgi holat | Tanlov |
|---|---|
| boshqaruv tuzilishining o'zi aniqlangandan keyin refaktoring qilinadi | skeletonize |
| umumiy ketma-ketlikni ko'rish kodni tushunarli qiladi | find sequences |
| snarled method, chekinish hukmron | skeletonize |
| bulleted method, bo'laklar ketma-ketligi | find sequences |

```java
// Asl shart
if (marginalRate() > 2 && order.hasLimit()) {
    order.readjust(rateCalculator.rateForToday());
    order.recalculate();
}

// Skeletonize: shart va tana ikki metodda, asl metodda skelet qoladi
if (needsRecalculation(order)) {
    recalculate(order, rateCalculator);
}

// Find sequences: shart va tana bitta metodda, chaqiruv ketma-ketlikka qo'shiladi
recalculateOrder(order, rateCalculator);
```

Qolgan ikki qoida tartibga tegishli:

- **Extract to the Current Class First** (306-bet). Ajratilgan bo'lak boshqa
  sinfga tegishli ekanining kuchli belgisi - sizga kelgan nom: bo'lak
  ichidagi o'zgaruvchining nomini metod nomiga qo'shgingiz kelsa, kod
  ehtimol shu o'zgaruvchining sinfiga tegishli. Shunga qaramay darhol boshqa
  sinfga ajratmaslik kerak. Avval o'sha noqulay nom bilan
  (`recalculateOrder`) o'z sinfiga ajratiladi: bu oson qaytariladigan
  harakat va to'g'ri bo'lak olinganini tekshirish imkonini beradi.
  Ko'chirish keyin, yo'nalish aniqlashganda qilinadi
  ([funksiyani ko'chirish](35-refaktoring-harakatlari-katalogi-i-funksiya.md#3512-funksiyani-kochirish-move-function)).
- **Be Prepared to Redo Extractions** (307-bet). Pirogni kesishning ko'p
  yo'li bor. Bir necha ajratishdan keyin yangi funksiyani joylashtirishning
  yaxshiroq yo'li ko'rinadi va ba'zan oldinga yurishning eng yaxshi yo'li -
  bir-ikki ajratishni qaytarib, boshqacha ajratish. Bu avvalgi ishni behuda
  qilmaydi: u eski dizayn haqida tushuncha berib bo'lgan.

Kitob yana bitta tartib ta'kidini qo'shadi (306-307-bet): avval kichik
bo'laklar ajratiladi. Metodni boshidan katta bo'laklarga bo'lishga urinish
ko'rinishidan osonroq, amalda esa osonroq ham, xavfsizroq ham emas -
tafsilotni o'tkazib yuborish osonlashadi, kodni ishlatib turgan narsa esa
aynan tafsilot.

## 38.15 Farq bilan programmalash (Programming by Difference)

Test ostiga olingan sinfga yangi variant kerak bo'lganda uchinchi yo'l bor:
sinfni to'g'ridan-to'g'ri o'zgartirmasdan, vorislik bilan funksiyani
kiritish, keyin esa funksiya qanday integratsiya qilinishi kerakligini hal
qilish (Feathers, *Working Effectively with Legacy Code*, Prentice Hall PTR,
2004 (copyright 2005), 8-bob, 94-bet). Feathers buni eski texnika deb
ataydi: 1980-larda ko'p ishlatilgan, 1990-larda OO jamoasi vorislikning
haddan oshishi muammo ekanini payqagach obro'sizlangan. Uning javobi aniq -
boshida vorislikdan foydalanish uni o'sha joyda qoldirish degani emas;
test bor bo'lsa boshqa tuzilishga o'tish oson.

```java
// 1-qadam: mavjud sinfga tegmasdan variant kiritiladi, test shu vorisda yoziladi
class AnonymousNotificationSender extends NotificationSender {

    @Override
    protected EmailAddress fromAddress(Notification notification) {
        return EmailAddress.of("anon-members@" + domain());
    }
}

// 2-qadam: ikkinchi variant kerak bo'lganda vorislik yetmaydi. Test bor,
// shuning uchun variantni obyektga o'tkazish xavfsiz.
class NotificationSender {

    private final MailingList list;   // variantni ro'yxat hal qiladi, voris emas

    protected EmailAddress fromAddress(Notification notification) {
        return list.fromAddress(notification);
    }
}
```

Narxi ham bor va Feathers uni nomlab ko'rsatadi:

- **Bir vaqtda bitta variant** (97-bet). Funksiyalarni alohida vorislarga
  joylasangiz, bir vaqtda ulardan faqat bittasini olasiz. Ikkinchi variant
  kerak bo'lganda yo'l: ikkinchisini qo'shishdan oldin to'xtab, tuzilishni
  o'zgartirish. Birinchi variant uchun yozilgan test shu ko'chishda
  xatti-harakat saqlanganini tekshiradi.
- **LSP buzilishi** (101-102-bet). Ikki amaliy qoida: iloji boricha konkret
  metodni override qilmaslik; override qilish kerak bo'lsa, override ichida
  o'zi override qilayotgan metodni chaqirish imkonini qarash. Feathers o'z
  misolida bu qoidalarning teskarisini qilganini tan oladi va nega xavfli
  ekanini aytadi: kodda bazaviy sinf havolasini ko'rgan odam o'sha sinfdagi
  metod ishlayotganini o'ylaydi, aslida esa voris metodi ishlaydi.
- **Normalizatsiya qilingan ierarxiya** (103-bet). Yechim shakli: hech bir
  sinf metodning bir nechta implementatsiyasiga ega bo'lmasin, ya'ni hech
  bir sinf voris olgan konkret metodni override qilmasin. Metod yo o'sha
  sinfda turadi, yo abstrakt bo'lib vorislarda implementatsiya qilinadi.
  Shunda "bu sinf X ni qanday qiladi?" savoliga sinfga qarab javob berish
  mumkin bo'ladi.

Feathers qoidani mutlaqlashtirmaydi (104-bet): LSP buzilmasa, vaqti-vaqti
bilan qilingan bir necha konkret override zarar bermaydi; lekin sinflar
normalizatsiyadan qanchalik uzoq ekanini vaqti-vaqti bilan ko'rib chiqish va
javobgarliklarni ajratishga tayyorlanayotganda shu tomonga yurish kerak.

Bu harakatning teskari tomoni korpusda bor:
[delegatsiya bilan vorislikni almashtirish](17-vorislik-kompozitsiya-va-polimorfizm.md#179-delegatsiya-bilan-vorislikni-almashtirish).
Farq bilan programmalash shu harakatning kirish nuqtasini beradi: vorislik -
boshlang'ich holat, delegatsiya esa test qo'yilgandan keyingi maqsad.

## 38.16 Kodbaza bo'ylab mexanik o'zgarish (Large-Scale Change)

38.5 katta refaktoringni bitta jamoa ichida bo'lishni ko'rsatdi. Ba'zi o'zgarishlar esa butun kodbazaga tegadi: eskirgan API dan yangisiga ko'chish, kutubxona nomini o'zgartirish, til konstruksiyasini almashtirish. Google bunday ishni **large-scale change** deb ataydi va u alohida apparat talab qiladi.

- **O'zgarish mexanik asbob bilan yaratiladi, qo'lda emas.** Mezon: o'zgarish yaratish uchun ketgan **inson mehnati kodbaza hajmi bilan chiziqli o'smasligi** kerak, ya'ni repozitoriy ikki baravar kattalashganda ham to'plamni yaratish taxminan bir xil vaqt olishi lozim. Ikkinchi talab - asbob kodbaza bo'ylab **to'liq** bo'lishi: muallif o'zgarish u tuzatmoqchi bo'lgan hamma holatni qamraganiga ishonishi kerak. Vositalar: AST ga asoslangan transformatsiya (Java da OpenRewrite yoki Error Prone ning `Refaster` shablonlari), kichik hajmda esa regulyar ifoda, `sed` yoki oddiy skript. Google ning qo'pol mo'ljali: o'zgarish taxminan 500 tahrirdan oshsa, asbobni o'rganib ishlatish qo'lda bajarishdan samaraliroq; tajribali "kod farroshi" uchun bu son ancha kichik.
- **O'zgarish mustaqil commit qilinadigan bo'laklarga shardlanadi.** Atomik katta commit amalda ishlamaydi: VCS operatsiyalari o'zgarish hajmi bilan chiziqli o'sadi, minglab faylni bir commitda yozish xotira yoki quvvat yetmasligi sababli umuman imkonsiz bo'lishi mumkin, markazlashgan tizimda esa katta commit boshqa yozuvchilarni to'sib qo'yadi. Ikkinchi sabab - **merge konflikti**: o'zgarishdagi fayllar soni oshgani sari konflikt ehtimoli oshadi, va u repozitoriydagi muhandislar soni bilan ko'payadi. Shuning uchun global o'zgarish egalik chegarasi bo'yicha bo'laklanadi, har bo'lak o'z test, review va submit quvuridan mustaqil o'tadi, bir-biriga bog'liq bo'laklar esa birga guruhlanadi.
- **Bo'lak kichik bo'lgani uchun xato sababi oson topiladi.** Kichik o'zgarishda qaysi tahrir regressiya berganini aniqlash arzon. Qayta ishga tushgan testlarning hisob-kitob narxi esa muhandis vaqtidan arzon: Google da har bo'lak unga tegishli testlarning tranzitiv yopilishida yurgiziladi va bu CI ga katta yuk beradi, lekin bu almashtiruv ongli qilingan.
- **Yaratilgan o'zgarish "uy hayvoni" emas, "mol".** Qo'lda yozilgan commit muallif uchun shaxsiy: unga kunlar sarflanadi va rad etilishi og'ir qabul qilinadi. Avtomatik yaratilgan o'zgarish esa nomsiz: rad etilsa yoki merge konfliktga tushsa, u qo'lda yamalmaydi, **asbob uni qayta yaratadi**. Shu sababli asosiy o'zgarishni yaratish jarayoni avtomatlashtirilgan bo'lishi kerak: tizimda yangi eski foydalanishlar paydo bo'lsa (kimdir eski API ni yana ishlatsa) yoki matnli konflikt chiqsa, asosiy o'zgarish yangilanib qayta shardlanadi.
- **Yo'naltiruvchi alias migratsiya qadami bo'ladi.** Til yordam beradigan joyda eski tur yoki metod yangisiga yo'naltiriladi: tur aliasi yoki eskirgan delegatlovchi metod. Chaqiruvchilar bosqichma-bosqich almashtiriladi, oxirida alias olib tashlanadi. Google ning `scoped_ptr` dan `std::unique_ptr` ga ko'chishi aynan shunday yakunlangan: avval eski nom yangisining aliasiga aylantirilgan, keyin matnli almashtirish bajarilgan, oxirida eski alias o'chirilgan. Bunday imkon bo'lmasa (til alias bermasa yoki tur API imzosida parametr bo'lsa) ko'chish atomik bajarilishi kerak, va bu ancha qimmat. Java da bu `@Deprecated(forRemoval = true)` delegatlovchi metod.
- **Arzon mexanika bilan kichik nomuvofiqliklar ham tuzatiladi.** Katta o'zgarish apparati bo'lsa, ilgari "arzimas" deb qoldirilgan nuqsonlarni tuzatish mumkin bo'ladi. Google ning misoli: ichki kutubxonada bir fayl `stl_util.h`, boshqasi `map-util.h` deb nomlangan edi, ya'ni ajratgich belgisi har xil. Bitta belgi farqi, lekin u muhandislarni qaysi fayl qaysi belgini ishlatganini eslab yurishga majbur qilgan va noto'g'ri yozilganda uzoq kompilyatsiya siklidan keyin xato bergan; o'zgarish bir necha haftalik fon ishi bilan bajarilgan va build nosozliklari soni o'lchangan holda kamaytirilgan.

```java
// Alias qadami: eski nom saqlanadi, yangisiga yo'naltiriladi
public final class PaymentService {

    /** @deprecated o'rniga {@link #settle(PaymentId)}; 3.0 da o'chiriladi. */
    @Deprecated(since = "2.4", forRemoval = true)
    public void settleLegacy(long paymentId) {
        settle(new PaymentId(paymentId));
    }

    public void settle(PaymentId id) { ... }
}
```

```bash
# AST ga asoslangan o'zgarish: barcha chaqiruvchilarni bir yurishda ko'chirish
./mvnw -U org.openrewrite.maven:rewrite-maven-plugin:run \
  -Drewrite.activeRecipes=uz.shop.MigrateSettleLegacy
```

Shardlashda birinchi mezon - **egalik chegarasi**: Maven modul, paket yoki `CODEOWNERS` yozuvi. Har bo'lak o'z PR i bo'lib, o'z egalari tomonidan review qilinadi; bir modulning ikki faylini bo'lib tashlash esa foydasiz, chunki ular birga test qilinadi.

## 38.17 Qadam yiqilganda: debug emas, oxirgi yaxshi commitga qaytish

Oldingi bo'limlar oldinga qarab intizomni beradi: bitta harakat,
kompilyatsiya, test. Yiqilgandan keyin nima qilish kerakligi esa alohida
qoida, chunki tabiiy reaksiya - debug qilib oldinga ketish - eng qimmat yo'l.

Qoida: test yiqilib, qaysi o'zgarish sababchi ekani darhol ko'rinmasa, debug
bilan oldinga ketilmaydi. Oxirgi ishlagan holatga qaytiladi va o'zgarishlar
bittalab qayta qo'yiladi, har biridan keyin test yurgiziladi. Fowler buni ikki
nashrda ikki marta aytadi: 1-nashrda qoida "orqaga qaytish" shaklida
(15-bob, 334-bet), 2-nashrda esa commit tilida - oxirgi yaxshi commitga
qaytib, o'sha ishni kichikroq qadamlar bilan qaytadan bajarish (1-bob,
21-bet).

Qoidaning ostida Beck ning iqtisodi turadi: bir soatlik ishni kichik qadamlar
bilan qayta qo'yish o'n daqiqa oladi, xatoni debug qilish esa besh sekunddan
ikki soatgacha cho'zilishi mumkin va qancha cho'zilishini oldindan bilib
bo'lmaydi. Ya'ni qaytish narxi ma'lum, debug narxi noma'lum; shuning uchun
qaytish tanlanadi. Bu 38.6 dagi "kod ishlamayotgani aniqlandi" shartidan
farq qiladi: u yerda refaktoring to'xtatiladi, bu yerda esa refaktoring davom
etadi, faqat boshqa yo'ldan.

Buning ishlashi uchun qaytish nuqtalari zich bo'lishi kerak, va bu ikkinchi
qoida: har bir mikro-qadamdan keyin kompilyatsiya, test va **mahalliy**
repozitoriyga commit. 2-nashrning birinchi bobi Split Loop, Slide Statements,
Extract Function va Inline Variable ketma-ketligini aynan shu tarzda
yurgizadi (1-bob, 20-bet). Bu 38.8 dagi commit gigiyenasiga qarshi emas:
mahalliy commitlar ishchi nuqtalar bo'lib, push qilishdan oldin bitta mantiqiy
o'zgarish darajasiga yig'iladi (40.1).

Uchinchi qoida qadam o'lchamiga tegishli: ish qiyinlashsa, qadam
qisqartiriladi. Qiyinlashish belgilari - test bir necha harakatdan keyin
yiqilishi, diff kutilgandan katta bo'lishi, "bu yerda nima bo'layotganini
bilmayman" holati. Javob har safar bir xil: oxirgi yaxshi commitga qaytib,
shu ishni kichikroq qadamlar bilan qaytadan bajarish. Juftlikda ishlanayotgan
bo'lsa, buning yana bitta signali bor - sherikning tushunmasligi (41.7).

```bash
# Yiqildi va sababchi o'zgarish ko'rinmaydi: oldinga debug qilinmaydi
git stash                            # yarim ish yo'qolmasligi uchun
git reset --hard HEAD                # oxirgi yaxshi commit

# keyin o'zgarishlar bittalab qayta qo'yiladi, har biridan keyin test va commit
./mvnw -q -pl payment test -Dtest='*Test' -DfailIfNoTests=false
git commit -am "refactor: Split Loop (1/4)"
```

## 38.18 Amalda qo'llash

- [ ] Refaktoringni bittadan bajarib, har biridan keyin kompilyatsiya va tez
      testlarni yurgizish odatini joriy qiling (McConnell 580).
- [ ] Harakatni boshlashdan oldin qadamlar ro'yxatini yozing va yo'lda
      chiqqan keraksiz g'oyalar uchun "parking lot" ro'yxati yuriting.
- [ ] Kompilyatorni eng qattiq ogohlantirish darajasiga qo'yib, ogohlantirish
      bilan build yiqiladigan qilib sozlang.
- [ ] Testsiz kodni refaktoring qilishdan oldin characterization test
      yozishni majburiy qiling: assertion ni yiqitib, kod aslida nima
      qaytarayotganini qayd eting (Feathers 186).
- [ ] Refaktoring va xatti-harakat o'zgarishini alohida commitlarga ajratish
      qoidasini jamoa kelishuviga kiriting; "refaktoring" nomi ostida
      buzilgan kodni paypaslashga yo'l qo'ymang.
- [ ] 38.3 jadvalidagi olti xavfni nomni o'zgartirishdan keyin har safar
      grep bilan tekshiring; refleksiya va satr literali asbobdan o'tib
      ketadi.
- [ ] Xavf darajasini oldin baholang: interfeys, baza sxemasi yoki boolean
      tekshiruvga tegadigan harakatga ikkinchi odamning reviewini qo'shing.
- [ ] Katta refaktoringni jamoa kelishuvi bilan boshlang va uni hozirgi
      vazifaga yetadigancha bajarib to'xtatishni normal hisoblang.
- [ ] Refaktoringdan keyin ishlashni profiler bilan o'lchab taqqoslang;
      yaxshilanish bo'lmasa o'zgarishni qaytaring.
- [ ] Har o'zgarishdan keyin bitta savolni bering: programmaning ichki sifati
      oshdimi yoki pasaydimi (McConnell 564-565)?
- [ ] Tahrir qilayotganda har bir tugma bosishini "xatti-harakatni
      o'zgartiradi" va "o'zgartirmaydi" ga ajratib turing; bir sekunddan kam
      ishlaydigan test to'plami shu aloqani beradi (Feathers 310).
- [ ] Pair da "hozir nima qilyapsan?" savolini kelishib oling: javob bittadan
      ko'p ish nomlasa, bittasi tanlanadi, qolgani qog'ozga yoziladi
      (Feathers 311).
- [ ] Test uchun bog'liqlikni uzayotganda imzoni o'zgartirmang: parametr
      ro'yxatini nusxa-joylashtirish bilan ko'chiring va dizayn yaxshilashni
      keyingi qadamga qoldiring (Feathers 313-314).
- [ ] Interfeys ajratishdan oldin e'lonni almashtirib kompilyatorga tayaning,
      lekin vorislik tuzog'ini eslang: izohga olingan metod xatosiz o'tsa, u
      ishlatilmaydi degani emas (Feathers 316).
- [ ] Testsiz ajratishda coupling count ni hisoblang va 0-count metodlardan
      boshlang; count 0 dan katta bo'lsa sezgir maydon qo'shing
      (Feathers 301-302).
- [ ] Muhim mantiqni test bilan qoplab, test qoplamagan ikkinchi darajali
      kodni ajratish tartibini jamoa kelishuviga kiriting (Feathers 303).
- [ ] Ajratishni avval o'z sinfiga, noqulay nom bilan qiling; boshqa sinfga
      ko'chirishni alohida qadamga qoldiring va bir-ikki ajratishni qaytarib
      qayta boshlashni normal hisoblang (Feathers 306-307).
- [ ] Vorislik bilan kiritilgan variantni test bilan qulflangandan keyin
      normalizatsiya qilingan ierarxiyaga yoki delegatsiyaga o'tkazing
      (Feathers 97, 103).

## Manbalar

- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 22-bob ("Codebase Insight", "Change Management", "Filling Potholes") - kodbaza bo'ylab o'zgarishni AST ga asoslangan asbob bilan yaratish, inson mehnatining kodbaza hajmi bilan chiziqli o'smasligi va o'zgarishning to'liq bo'lishi talabi, 500 tahrir mo'ljali, hamda arzon mexanika bilan kichik nomuvofiqliklarni tuzatish. Bu nashrning nusxasida barqaror bet raqami yo'q, shuning uchun bob va bo'lim nomi ko'rsatilgan
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 22-bob ("Barriers to Atomic Changes", "Sharding and Submitting", "Cattle Versus Pets", "Change Creation") - katta o'zgarishni atomik commit qilishga to'siqlar (VCS cheklovlari va merge konflikti), egalik chegarasi bo'yicha shardlash va har bo'lakning mustaqil test-review-submit quvuri, yaratilgan o'zgarishning qayta yaratiladigan bo'lishi. Bu nashrning nusxasida barqaror bet raqami yo'q, shuning uchun bob va bo'lim nomi ko'rsatilgan
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 22-bob ("scoped_ptr to std::unique_ptr", "Language Support") - eski turni yangisining aliasiga aylantirib bosqichma-bosqich ko'chirish va oxirida aliasni olib tashlash, til alias va yo'naltiruvchi funksiya bermasa ko'chirishning atomik bo'lishi kerakligi. Bu nashrning nusxasida barqaror bet raqami yo'q, shuning uchun bob va bo'lim nomi ko'rsatilgan
- Martin Fowler, *Refactoring: Improving the Design of Existing Code*,
  1-nashr, Addison-Wesley, 1999, 2-bob "Principles in Refactoring" (46-62) -
  refaktoring ta'rifi (46), Kent Beck ning ikki shlyapa metaforasi (47),
  "Problems with Refactoring" ning taxminiyligi (54), refaktoring o'rniga
  qayta yozish va muddat yaqin bo'lgan holat, Ward Cunningham ning qarz
  metaforasi (56-57), ishlash bo'yicha uch yo'l, 90 foiz statistikasi va
  profiler bilan ishlash tartibi (59-60)
- Martin Fowler, *Refactoring: Improving the Design of Existing Code*,
  1-nashr, Addison-Wesley, 1999, 4-bob "Building Tests" (73-84) -
  refaktoringning asosiy oldingi sharti mustahkam testlar, testlar to'liq
  avtomatik va o'z natijasini o'zi tekshiradigan bo'lishi, test to'plami
  xatoni topish vaqtini qisqartirishi
- Martin Fowler, *Refactoring: Improving the Design of Existing Code*,
  1-nashr, Addison-Wesley, 1999, 12-bob "Big Refactorings" (293-294, Kent
  Beck bilan) - katta refaktoringning qadamlari batafsil yozilmasligi, oy va
  yil o'lchovi, chekkalaridan tishlab borish, hozirgi vazifaga yetadigancha
  bajarish, butun jamoa kelishuvi talabi
- Martin Fowler, *Refactoring: Improving the Design of Existing Code*,
  1-nashr, Addison-Wesley, 1999, 14-bob "Refactoring Tools" (328-331, Don
  Roberts va John Brant) - asbobning maqsadi qayta testlashni kamaytirish,
  xatti-harakatni to'liq saqlash imkonsizligi, Reflection API misoli,
  `grep` ning semantik chegarasi
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 24.4
  "Refactoring Safely" (579-582) - boshlagan kodni saqlash, harakatlarni
  kichik ushlash, bittadan bajarish va har biridan keyin qayta kompilyatsiya
  va test, qadamlar ro'yxati, "parking lot", checkpointlar, kompilyator
  ogohlantirishlari, review va xatolar statistikasi (Yourdon 1986b,
  Freedman va Weinberg 1982, Perrott 2004), xavf darajasiga qarab moslash,
  refaktoringni niqob qilib ishlatish va Kent Beck ning "katta refaktoring -
  falokat retsepti" gapi
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 24.5
  "Refactoring Strategies" (582-583) - refaktoringning kamayuvchi qaytim
  qonuniga bo'ysunishi va 80/20 qoidasi
- Martin Fowler, *Refactoring: Improving the Design of Existing Code*,
  1-nashr, Addison-Wesley, 1999, 15-bob (334-bet) - test yiqilib sababchi
  o'zgarish ko'rinmaganda debug bilan oldinga ketmaslik: oxirgi ishlagan
  holatga qaytib o'zgarishlarni bittalab qayta qo'yish, va buning iqtisodi
  (qayta qo'yish narxi ma'lum, debug narxi noma'lum)
- Martin Fowler, *Refactoring*, 2-nashr, Addison-Wesley, 2019, 1-bob (20-bet,
  nashriyotning ochiq preview nusxasi) - har bir mikro-qadamdan keyin
  kompilyatsiya, test va mahalliy repozitoriyga commit; Split Loop, Slide
  Statements, Extract Function va Inline Variable ketma-ketligining shu
  tarzda yurgizilishi
- Martin Fowler, *Refactoring*, 2-nashr, Addison-Wesley, 2019, 1-bob (21-bet,
  nashriyotning ochiq preview nusxasi) - ish qiyinlashsa qadamni qisqartirish
  va test yiqilib muammo darhol ko'rinmasa oxirgi yaxshi commitga qaytib
  ishni kichikroq qadamlar bilan qaytadan bajarish (1-nashr, 334-bet dagi
  qoidaning commit tilidagi shakli)
- Martin Fowler, *Refactoring*, 2-nashr, Addison-Wesley, 2019, 2-bob (51-bet,
  nashriyotning ochiq preview nusxasi) - xato xabarini refaktoring kerak
  ekanining belgisi deb o'qish: kod xatoni ko'rishga yetarlicha ravshan
  bo'lmagan
- ESLATMA: 38.17 dagi `git` va Maven buyruqlari hamda mahalliy commitlarni
  push dan oldin yig'ish tavsiyasi korpus qo'shimchasi; Fowler qoidani
  vositadan mustaqil shaklda beradi
- Michael Feathers, *Working Effectively with Legacy Code*, Prentice Hall PTR,
  2004 (copyright 2005), 4-bob (31-32) va 13-bob (186-187) - chok (seam) ta'rifi,
  characterization test ta'rifi va uni yozishning besh qadami
- Michael Feathers, *Working Effectively with Legacy Code*, Prentice Hall PTR,
  2004 (copyright 2005), 6-bob (59, 67) - Sprout Method va Wrap Method, va yangi kodning
  chaqiruv nuqtalari testlanmagan qolishi haqidagi ogohlantirish
- Michael Feathers, *Working Effectively with Legacy Code*, Prentice Hall PTR,
  2004 (copyright 2005), 8-bob (94-104) - Programming by Difference: vorislik
  bilan variantni sinfga tegmasdan kiritish, texnikaning 1980 va 1990-yillardagi
  taqdiri, bir vaqtda bitta variant chegarasi (97), LSP buzilishi va ikki amaliy
  qoida (101-102), normalizatsiya qilingan ierarxiya ta'rifi (103), qoidani
  mutlaqlashtirmaslik (104)
- Michael Feathers, *Working Effectively with Legacy Code*, Prentice Hall PTR,
  2004 (copyright 2005), 22-bob "I Need to Change a Monster Method and I Can't
  Write Tests for It" (289-307) - bulleted va snarled monstr metod ta'riflari
  (290, 292), qo'lda Extract Method ning uch xatosi (297), Introduce Sensing
  Variable va sezgir maydonni seans oxirigacha saqlash (298-301), Extract What
  You Know va "kichik" ning o'lchovi hamda coupling count (301-302), Gleaning
  Dependencies (303), Skeletonize Methods (304-305), Find Sequences va ikki
  maslahatning ziddiyati (305), Extract to the Current Class First (306), kichik
  bo'laklardan boshlash (306-307), Be Prepared to Redo Extractions (307)
- Michael Feathers, *Working Effectively with Legacy Code*, Prentice Hall PTR,
  2004 (copyright 2005), 23-bob "How Do I Know That I'm Not Breaking Anything?"
  (309-317) - ongli tahrir va tugma bosishining ikki toifasi (310), bitta
  maqsadli tahrir va "bir vaqtda bitta ish" mantrasi (311-312), Preserve
  Signatures: sababi, Feathers ning o'z xatosi va olti qadamli
  nusxa-joylashtirish mexanikasi (312-314), Lean on the Compiler: ikki qadam,
  tuzilish va tur o'zgarishi, build vaqti chegarasi va vorislik tuzog'i
  (315-316)
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 24.1 "Kinds
  of Software Evolution" (564-565) - sifat oshadimi yoki pasayadimi ajratishi,
  construction va maintenance paytidagi o'zgarish farqi, evolyutsiyaning asosiy
  qoidasi (Cardinal Rule of Software Evolution)
- ESLATMA: 38.3 jadvalining Spring, JPA, Jackson va migratsiyaga tegishli
  to'rt qatori shu korpusning stekiga moslangan ro'yxat; kitobda nomi bilan
  turgani satr literali va refleksiya
- ESLATMA: 38.5 dagi to'rt qadamli abstraksiya ortida ishlash tartibi va
  38.8 dagi commit xabari shakli shu korpusning amaliy tavsiyasi, kitobdan
  olingan emas
- ESLATMA: 38.11 oxiridagi IDE chegarasi izohi va 38.12 dagi "metodni izohga
  olish o'rniga qayta nomlash" hamda `@Override` tavsiyasi shu korpusning
  qo'shimchasi; kitoblarda ular yo'q. 38.9 dagi construction/maintenance
  jadvali McConnell 564-betdagi nasrni jadvalga keltirgan shakli

---

[&larr; 37. Refaktoring harakatlari katalogi III: shart, API va ierarxiya](37-refaktoring-harakatlari-katalogi-iii-shart.md) · [Mundarija](README.md) · [39. Bir qadamli build va mahalliy qaytish halqasi &rarr;](39-bir-qadamli-build-va-mahalliy-qaytish.md)
