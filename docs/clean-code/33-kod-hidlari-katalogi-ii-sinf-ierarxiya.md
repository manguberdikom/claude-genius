<!-- doc: clean-code | chapter: 33 | part: X. Hid katalogi va refaktoring harakatlari -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 33. Kod hidlari katalogi II: sinf, ierarxiya, bog'liqlik (Code Smells II)

<details>
<summary>Bu bobdagi 22 bo'lim</summary>

- [33.1 Tarqoq o'zgarish (Divergent Change)](#331-tarqoq-ozgarish-divergent-change)
- [33.2 Ma'lumot sinfi (Data Class)](#332-malumot-sinfi-data-class)
- [33.3 Noo'rin yaqinlik (Inappropriate Intimacy / Insider Trading)](#333-noorin-yaqinlik-inappropriate-intimacy--insider-trading)
- [33.4 Muqobil sinflar, turli interfeyslar (Alternative Classes with Different Interfaces)](#334-muqobil-sinflar-turli-interfeyslar-alternative-classes-with-different-interfaces)
- [33.5 Rad etilgan meros (Refused Bequest)](#335-rad-etilgan-meros-refused-bequest)
- [33.6 Parallel ierarxiyalar (Parallel Inheritance Hierarchies)](#336-parallel-ierarxiyalar-parallel-inheritance-hierarchies)
- [33.7 To'liq bo'lmagan kutubxona sinfi (Incomplete Library Class)](#337-toliq-bolmagan-kutubxona-sinfi-incomplete-library-class)
- [33.8 Haddan tashqari ko'p ma'lumot (Too Much Information)](#338-haddan-tashqari-kop-malumot-too-much-information)
- [33.9 Izchilsizlik (Inconsistency)](#339-izchilsizlik-inconsistency)
- [33.10 Keraksizlik (Clutter)](#3310-keraksizlik-clutter)
- [33.11 Sun'iy bog'liqlik (Artificial Coupling)](#3311-suniy-bogliqlik-artificial-coupling)
- [33.12 Noto'g'ri joylashgan javobgarlik (Misplaced Responsibility)](#3312-notogri-joylashgan-javobgarlik-misplaced-responsibility)
- [33.13 Noo'rin statik (Inappropriate Static)](#3313-noorin-statik-inappropriate-static)
- [33.14 Bazaviy sinf vorisga bog'liq (Base Class Depending on Derivatives)](#3314-bazaviy-sinf-vorisga-bogliq-base-class-depending-on-derivatives)
- [33.15 Majburiy sozlash kodi (Required Setup Code)](#3315-majburiy-sozlash-kodi-required-setup-code)
- [33.16 Kombinatorik portlash (Combinatorial Explosion)](#3316-kombinatorik-portlash-combinatorial-explosion)
- [33.17 Sochma jarrohlik (Shotgun Surgery)](#3317-sochma-jarrohlik-shotgun-surgery)
- [33.18 Begona ma'lumotga havas (Feature Envy)](#3318-begona-malumotga-havas-feature-envy)
- [33.19 Katta sinf (Large Class)](#3319-katta-sinf-large-class)
- [33.20 Spekulyativ umumiylik (Speculative Generality)](#3320-spekulyativ-umumiylik-speculative-generality)
- [33.21 Katta sinfda mas'uliyatni ko'rish: metod guruhlash va feature sketch](#3321-katta-sinfda-masuliyatni-korish-metod-guruhlash-va-feature-sketch)
- [33.22 Amalda qo'llash](#3322-amalda-qollash)

</details>


Bu bob sinf darajasidagi va sinflar orasidagi hidlarni qamrab oladi.
Manbalar [32-bob](32-kod-hidlari-katalogi-i-nom-funksiya-malumot.md) bilan
bir xil va nashr qoidasi ham shunday: hidning **nomi** va **beti**
*Refactoring* ning 2-nashridan keltirilishi mumkin (2019, mundarija
tasdiqlaydi), hidning **ta'rifi va mexanikasi** esa faqat 1-nashrdan
(1999, 3-bob, 63-72 bet). Ikkinchi katalog Robert C. Martin ning *Clean
Code* 17-bobidagi evristikalar (285-308 bet); 33.8-33.14 aynan shu
katalogdan.

Bu bobda nashrlar farqi sezilarli: 1-nashrdagi ikki hid 2-nashr
ro'yxatida yo'q (33.6 va 33.7), bittasining nomi o'zgargan (33.3), va
ikki bo'limning sarlavhasidagi nom ikki katalogning hech birida yo'q
(33.15 va 33.16) - bu ikkisi bo'limning o'zida belgilangan.

God Object, Big Ball of Mud, Circular Dependency va boshqa arxitektura
darajasidagi anti-patternlar [patternlar hujjatining anti-patternlar
bobida](../patterns/25-anti-patternlar.md); bu yerda ularning kod
darajasidagi qardoshlari. 33.17-33.20 - 2-nashr ro'yxatining qolgan
to'rt hidi; ularning Spring darajasidagi tahlili shu anti-patternlar
bobida, bu yerda esa katalog yozuvi: nom, bet, kitobdagi sabab va
harakat.

## 33.1 Tarqoq o'zgarish (Divergent Change)

**Manba**: 1-nashr 66-bet, 2-nashr 76-bet; nom ikki nashrda bir xil.

**Belgisi**: bitta sinf turli sabablarga ko'ra turli yo'llar bilan
o'zgaradi. Fowler ning aniq ta'rifi shunday: sinfga qarab "yangi
ma'lumot bazasi kelganda shu uchta metodni o'zgartirishim kerak, yangi
moliyaviy instrument kelganda esa shu to'rtta metodni" deb aytsangiz,
bu bir obyekt o'rniga ikkitasi yaxshi bo'lgan holat (1-nashr, 66-bet).

**Nega muammo**: dasturni o'zgarishni osonlashtirish uchun
tuzilmalashtiramiz; o'zgarish kerak bo'lganda tizimning bitta aniq
nuqtasiga borib o'zgartirish imkoni bo'lishi kerak. Variantni qo'llash
uchun kiritilgan har qanday o'zgarish bitta sinfni o'zgartirishi va
yangi sinfdagi butun yozuv shu variantni ifodalashi kerak (1-nashr,
66-bet). Bu yagona javobgarlik printsipining buzilishi ([patternlar
hujjatidagi](../patterns/README.md) yagona javobgarlik printsipi).

**Tuzatish**: ma'lum bir sabab uchun o'zgaradigan hamma narsani
aniqlash va ularni Extract Class bilan birga yig'ish (1-nashr, 66-bet;
2-nashrda Extract Class 182-bet, Split Phase 154-bet).

**Juftlik hid**: Shotgun Surgery (1-nashr, 66-bet; 2-nashr, 76-bet) -
teskari holat: har bir o'zgarish turi uchun ko'p sinfda ko'p kichik
o'zgarish qilish kerak bo'ladi, ular tarqoq bo'lgani uchun topish qiyin
va muhim o'zgarishni o'tkazib yuborish oson. Yechimi Move Method va
Move Field bilan o'zgarishlarni bitta sinfga yig'ish, nomzod sinf
bo'lmasa yaratish, ba'zan Inline Class (1-nashr, 66-bet). Fowler ikkisini
bir jumlada farqlaydi: tarqoq o'zgarish - ko'p xil o'zgarishdan jabr
ko'radigan bitta sinf, shotgun surgery - ko'p sinfni o'zgartiradigan
bitta o'zgarish; ikki holatda ham maqsad - umumiy o'zgarishlar va
sinflar orasida bir-bir munosabat bo'lishi (1-nashr, 66-bet).

**Aniqlash usuli** (korpusning amaliy tavsiyasi, kitobdan olingan emas):
`git log` bilan sinf o'zgarishlarining sabablarini sanash; chegara
aniqlash texnikasi [arxitektor hujjatida](../architect/README.md).

## 33.2 Ma'lumot sinfi (Data Class)

**Manba**: 1-nashr 70-71 bet, 2-nashr 83-bet; nom ikki nashrda bir xil.

**Belgisi**: sinfda maydonlar, ularning getter va setter lari bor va
boshqa hech narsa yo'q. Bunday sinflar aqlsiz ma'lumot saqlagichlar va
ular deyarli aniq boshqa sinflar tomonidan haddan tashqari mayda
tafsilot darajasida boshqariladi (1-nashr, 70-bet).

**Nega muammo**: shu sinf bilan bog'liq mantiq boshqa sinflarda
tarqalgan. Fowler ning o'z o'xshatishi: ma'lumot sinflari bolalarga
o'xshaydi, boshlanish nuqtasi sifatida yaxshi, lekin katta obyekt
sifatida ishtirok etish uchun biror javobgarlikni o'z ustiga olishi
kerak (1-nashr, 71-bet). Anemik domen modeli bilan aloqasi [patternlar
hujjatida](../patterns/25-anti-patternlar.md).

**Tuzatish** (1-nashr, 70-71 bet):

- maydonlar `public` bo'lsa, darhol Encapsulate Field;
- collection maydonlari to'g'ri inkapsulyatsiya qilinmagan bo'lsa,
  Encapsulate Collection;
- o'zgarmasligi kerak bo'lgan maydon uchun Remove Setting Method;
- getter va setter larni boshqa sinflar qaerda ishlatayotganiga qarab,
  Move Method bilan xatti-harakatni ma'lumot sinfiga ko'chirish; butun
  metodni ko'chirish imkoni bo'lmasa, avval Extract Method;
- vaqt o'tib getter va setter larga Hide Method qo'llash.

2-nashrdagi nomlar: Encapsulate Record (162-bet), Encapsulate Collection
(170-bet), Remove Setting Method (331-bet), Move Function (198-bet).

Korpusning amaliy tavsiyasi (kitobdan olingan emas): DTO va `record`
chegarada ataylab ma'lumot sinfi bo'ladi (14.5) - bu hid emas.

## 33.3 Noo'rin yaqinlik (Inappropriate Intimacy / Insider Trading)

**Manba**: 1-nashrda "Inappropriate Intimacy" (70-bet); 2-nashrda nom
"Insider Trading" ga o'zgargan (82-bet). Ta'rif shu yerda 1-nashrdan.

**Belgisi**: sinflar bir-biriga haddan tashqari yaqinlashib, vaqtining
ko'p qismini bir-birining private qismlarini kavlashga sarflaydi
(1-nashr, 70-bet). Java da bu ichma-ich sinflar va `package-private`
kirish orqali ko'rinadi.

**Nega muammo**: ikki sinf aslida bitta, lekin ikkiga bo'lingan; yoki
chegara noto'g'ri joyda. Fowler alohida ta'kidlaydi: vorislik ko'pincha
ortiqcha yaqinlikka olib keladi, chunki voris sinf ota-onasi istagandan
ko'proq narsani biladi (1-nashr, 70-bet).

**Tuzatish** (1-nashr, 70-bet): bo'laklarni ajratish uchun Move Method
va Move Field; ikki tomonlama bog'lanishni bir tomonlamaga keltirish
mumkin bo'lsa Change Bidirectional Association to Unidirectional;
sinflarda umumiy qism bo'lsa Extract Class bilan umumiylikni xavfsiz
joyga chiqarish; yoki Hide Delegate bilan uchinchi sinfni oraliq
sifatida qo'yish. 2-nashrdagi nomlar: Move Function (198-bet), Move
Field (207-bet), Extract Class (182-bet), Hide Delegate (189-bet),
Inline Class (186-bet).

## 33.4 Muqobil sinflar, turli interfeyslar (Alternative Classes with Different Interfaces)

**Manba**: 1-nashr 70-bet, 2-nashr 83-bet; nom ikki nashrda bir xil.

**Belgisi**: ikki sinf bir xil ish qiladi, lekin metod nomlari va
imzolari boshqa: `SmsSender.send(to, text)` va
`EmailGateway.deliverMessage(address, body, subject)`.

**Tuzatish** (1-nashr, 70-bet): bir xil ish qiladigan, lekin imzosi
boshqa metodlarga Rename Method. Fowler buning ko'pincha yetarli
bo'lmasligini aytadi: bunday holatda sinflarning o'zi hali yetarli ish
qilmaydi, shuning uchun protokollar bir xil bo'lguncha Move Method
bilan xatti-harakatni ko'chirish davom etadi; shu yo'lda kodni
takroriy ko'chirishga to'g'ri kelsa, Extract Superclass bilan
tuzatiladi. 2-nashrdagi nomlar: Change Function Declaration (124-bet),
Move Function (198-bet), Extract Superclass (375-bet).

Korpusning amaliy tavsiyasi (kitobdan olingan emas): sinflardan biri
uchinchi tomon sinfi bo'lsa va uni o'zgartirib bo'lmasa, adapter
([patternlar hujjati](../patterns/02-strukturaviy-patternlar.md#21-adapter-adapter)).
1-nashr o'zgartirib bo'lmaydigan kutubxona sinfi uchun boshqa ikki
harakatni beradi (33.7).

## 33.5 Rad etilgan meros (Refused Bequest)

[Rad etilgan meros va interfeysni bo'lish](17-vorislik-kompozitsiya-va-polimorfizm.md#176-rad-etilgan-meros-va-interfeysni-bolish)
bo'limida ko'rilgan.

**Manba**: 1-nashr 71-bet, 2-nashr 83-bet; nom ikki nashrda bir xil.

**Belgisi**: voris sinflar ota-onasining metod va ma'lumotini meros
oladi, lekin ularning hammasini xohlamaydi yoki ularga muhtoj emas:
berilgan sovg'alardan faqat bir nechtasini olib o'ynaydi (1-nashr,
71-bet). Java dagi ko'rinishi: meros olgan metod
`UnsupportedOperationException` tashlaydi.

**An'anaviy yechim va Fowler ning fikri**: an'anaviy hikoya - ierarxiya
xato, yangi qardosh sinf yaratib, ishlatilmaydigan metodlarni Push Down
Method va Push Down Field bilan unga tushirish kerak, shunda ota-ona
faqat umumiyni ushlab turadi. Fowler bunga doim ergashmaydi: voris sinf
bilan biror xatti-harakatni qayta ishlatish normal ish usuli; hid bor,
lekin kuchli emas, va o'n holatning to'qqiztasida bu hid tozalashga
arzigulik darajada sezilmaydi. Agar rad etilgan meros chalkashlik va
muammo keltirsa, an'anaviy yo'ldan borish kerak (1-nashr, 71-bet).

**Hid kuchli bo'ladigan holat**: voris sinf xatti-harakatni qayta
ishlatadi, lekin ota-sinfning **interfeysini** qo'llab-quvvatlashni
istamaydi. Fowler implementatsiyani rad etishga qarshi emas, interfeysni
rad etishga qarshi; bu holatda ierarxiyani tuzatish emas, Replace
Inheritance with Delegation bilan uni butunlay olib tashlash kerak
(1-nashr, 71-bet; 1-nashrda harakatning beti 287, 2-nashrda nom Replace
Superclass with Delegate, 399-bet). 2-nashrdagi boshqa nomlar: Push Down
Method (359-bet), Push Down Field (361-bet).

## 33.6 Parallel ierarxiyalar (Parallel Inheritance Hierarchies)

**Manba**: faqat 1-nashr, 68-bet. 2-nashr 3-bobining ro'yxatida bu hid
yo'q (2-nashr mundarijasi, 71-84 bet). Shuning uchun bu bo'limda
2-nashrdan bet keltirilmaydi.

**Belgisi**: bitta sinfning vorisi yaratilganda, ikkinchi ierarxiyada
ham mos voris yaratish kerak bo'ladi: `CardPayment` va
`CardPaymentValidator`, `BankPayment` va `BankPaymentValidator`.
Fowler aniq belgi beradi: bir ierarxiyadagi sinf nomlarining prefiksi
ikkinchi ierarxiyadagi prefikslar bilan bir xil bo'ladi (1-nashr,
68-bet).

**Nega muammo**: Fowler buni shotgun surgery ning xususiy holati deb
ataydi (1-nashr, 68-bet; 33.1): ikki ierarxiya bitta o'q bo'ylab
o'sadi va ularni sinxron ushlash qo'lda bajariladi.

**Tuzatish**: takrorlanishni yo'qotishning umumiy strategiyasi - bir
ierarxiyaning instanslari ikkinchisining instanslariga murojaat
qilsin. Move Method va Move Field qo'llanilsa, murojaat qiladigan
sinfdagi ierarxiya yo'qoladi (1-nashr, 68-bet).

Korpusning amaliy tavsiyasi (kitobdan olingan emas): Java da ikkinchi
o'qni `sealed` ierarxiya va pattern matching bilan bitta o'qga
qisqartirish (25.3).

## 33.7 To'liq bo'lmagan kutubxona sinfi (Incomplete Library Class)

**Manba**: faqat 1-nashr, 70-bet. 2-nashr 3-bobining ro'yxatida bu hid
yo'q (2-nashr mundarijasi, 71-84 bet).

**Belgisi**: uchinchi tomon sinfi kerakli metodni bermaydi va kod
bazasida uning atrofida yordamchi funksiyalar tarqalgan.

**Nega muammo**: kutubxona mualliflari hamma narsani oldindan bilmaydi,
lekin kutubxona sinfini kerakli ishni qilishi uchun o'zgartirish
ko'pincha noto'g'ri, ko'pincha esa umuman imkonsiz. Shuning uchun Move
Method kabi sinalgan usullar bu yerda ishlamaydi (1-nashr, 70-bet).

**Tuzatish** (1-nashr, 70-bet): bu ish uchun ikkita maxsus harakat bor.
Kutubxona sinfida bir-ikki metod yetishmasa, Introduce Foreign Method
(1-nashr, 131-bet). Qo'shimcha xatti-harakat katta bo'lsa, Introduce
Local Extension (1-nashr, 133-bet): shu qo'shimcha metodlarni o'z
ichiga olgan yangi sinf yaratiladi va u asl sinfning voris sinfi yoki
wrapper i qilinadi.

Korpusning amaliy tavsiyasi (kitobdan olingan emas): kutubxona turini
domen kodi bo'ylab tarqatmaslik va yordamchilarni bitta joyda ushlash
(14.8, 18.3).

## 33.8 Haddan tashqari ko'p ma'lumot (Too Much Information)

**Manba**: Robert C. Martin, *Clean Code*, 17-bob, G8 "Too Much
Information" (291-292 bet).

**Belgisi**: keng va chuqur interfeys; `public` modifikatori standart
tanlov.

**Nega muammo**: yaxshi aniqlangan modulning interfeysi juda kichik va
u kam narsa bilan ko'p ishni qilishga imkon beradi; yomon aniqlangan
modul esa oddiy ishni bajarish uchun ko'p turli harakat talab qiladigan
keng va chuqur interfeys beradi. Yaxshi interfeys bog'lanish uchun kam
funksiya taklif qiladi, shuning uchun coupling past bo'ladi; yomon
interfeys ko'p funksiya beradi va coupling baland bo'ladi (G8,
291-bet).

Martin ning tavsiyasi raqamsiz va qiyosiy: sinfda metod kamroq
bo'lsa yaxshiroq, funksiya kamroq o'zgaruvchini bilsa yaxshiroq,
sinfda instans o'zgaruvchisi kamroq bo'lsa yaxshiroq. Ma'lumotni,
yordamchi funksiyalarni, konstantalarni va vaqtinchalik qiymatlarni
yashirish kerak; voris sinflar uchun ko'p `protected` o'zgaruvchi va
funksiya yaratmaslik kerak (G8, 292-bet). Bu korpusda public metod soni
uchun raqamli chegara yo'q.

**Tuzatish**: ko'rinishni toraytirish (14.6), interfeysni bo'lish,
paketdan faqat API turlarini chiqarish (26.2). Orqaga moslik
majburiyati [arxitektor hujjatida](../architect/README.md).

## 33.9 Izchilsizlik (Inconsistency)

**Manba**: *Clean Code*, 17-bob, G11 "Inconsistency" (292-bet).

**Belgisi va qoida**: bir narsani ma'lum yo'l bilan qilsangiz, shunga
o'xshash hamma narsani shu yo'l bilan qiling. Martin buni eng kam
hayron qoldirish printsipiga bog'laydi: konvensiyani tanlashda ehtiyot
bo'lish, tanlangandan keyin esa unga ergashishda davom etish kerak.
Kitobdagi misol: bir funksiyada `HttpServletResponse` uchun `response`
nomi ishlatilsa, shu turni ishlatadigan boshqa funksiyalarda ham shu
nom ishlatiladi; metod `processVerificationRequest` deb nomlangan bo'lsa,
boshqa turdagi so'rovlarni ishlovchi metod `processDeletionRequest`
kabi o'xshash nom oladi (G11, 292-bet). Java dagi ko'rinishi: bir joyda
`Optional`, boshqa joyda `null`; bir joyda konstruktor inyeksiyasi,
boshqa joyda maydon; bir joyda `find`, boshqa joyda `get`.

**Nega muammo**: shunday oddiy izchillik ishonchli qo'llanganda kodni
o'qish va o'zgartirishni sezilarli osonlashtiradi (G11, 292-bet);
izchilsizlik esa teskarisini qiladi - o'quvchi har joyda qaytadan
o'ylaydi.

**Tuzatish**: konvensiyani hujjatlashtirish
([48-bob](48-tezkor-malumotnoma-qoidalar-va-tekshiruv.md)), keyin uni
mashinaga topshirish
([42-bob](42-statik-tahlil-va-avtomatik-qoidalar.md)).

## 33.10 Keraksizlik (Clutter)

**Manba**: *Clean Code*, 17-bob, G12 "Clutter" (293-bet); o'lik kod
uchun G9 "Dead Code" (292-bet).

**Belgisi**: Martin ro'yxatni savol bilan boshlaydi - implementatsiyasi
yo'q default konstruktorning nima foydasi bor? U faqat kodni ma'nosiz
artefaktlar bilan to'ldiradi. Shu qatorda: ishlatilmaydigan
o'zgaruvchilar, hech kim chaqirmaydigan funksiyalar, ma'lumot
qo'shmaydigan izohlar. Bularning hammasi keraksizlik va olib tashlanadi
(G12, 293-bet).

O'lik kod alohida evristika: bajarilmaydigan kod. U bo'lmaydigan
shartni tekshiradigan `if` tanasida, hech qachon istisno tashlamaydigan
`try` ning `catch` blokida, hech qachon chaqirilmaydigan kichik
yordamchi metodlarda va hech qachon yuz bermaydigan `switch` shoxlarida
uchraydi. Muammosi shunda: o'lik kod dizayn o'zgarganda to'liq
yangilanmaydi, u kompilyatsiya bo'ladi, lekin yangi konvensiya va
qoidalarga ergashmaydi; topilsa, o'chirib tashlanadi (G9, 292-bet).

**Tuzatish**: Remove Dead Code (2-nashr, 237-bet). O'lik kodni topish
uchun IDE inspeksiyasi, `-Xlint` va kod qamrovi hisoboti; o'lik kod
qoidalarining katalogi [SonarQube hujjatida](../sonarqube/README.md).

## 33.11 Sun'iy bog'liqlik (Artificial Coupling)

**Manba**: *Clean Code*, 17-bob, G13 "Artificial Coupling" (293-bet).

**Belgisi**: bir-biriga bog'liq bo'lmagan narsalar sun'iy bog'langan.
Martin ning misoli: umumiy enum lar aniqroq sinflar ichida turmasligi
kerak, chunki bu butun dasturni shu aniq sinflarni bilishga majbur
qiladi; umumiy maqsadli statik funksiyalarni aniq sinflarda e'lon qilish
ham shunday (G13, 293-bet).

**Nega muammo**: sun'iy bog'liqlik - hech qanday to'g'ridan-to'g'ri
maqsadga xizmat qilmaydigan bog'liqlik. U o'zgaruvchi, konstanta yoki
funksiyani vaqtincha qulay, lekin noto'g'ri joyga qo'yish natijasi, va
Martin buni dangasalik va e'tiborsizlik deb ataydi (G13, 293-bet).

**Tuzatish**: funksiya, konstanta va o'zgaruvchilar qayerda e'lon
qilinishi kerakligini aniqlashga vaqt ajratish; eng qulay joyga tashlab
qo'ymaslik (G13, 293-bet). Refaktoring harakati sifatida Move Function
(2-nashr, 198-bet) va Move Field (2-nashr, 207-bet).

## 33.12 Noto'g'ri joylashgan javobgarlik (Misplaced Responsibility)

**Manba**: *Clean Code*, 17-bob, G17 "Misplaced Responsibility"
(295-296 bet).

**Belgisi**: funksiya nomi bilan sinf nomi mos kelmaydi:
`OrderService.calculateTax()`, `UserController.sendEmail()`,
`PaymentRepository.formatReceipt()`.

**Nega muammo**: Martin kodni qaerga qo'yish qarorini dasturchining eng
muhim qarorlaridan biri deb ataydi va bu yerda ham eng kam hayron
qoldirish printsipini qo'llaydi: kod o'quvchi uni tabiiy ravishda
kutgan joyda turishi kerak. `PI` konstantasi trigonometriya
funksiyalari e'lon qilingan joyda, `OVERTIME_RATE` esa ish haqini
hisoblaydigan sinfda bo'lishi kerak (G17, 295-bet).

**Aniqlash savoli** (kitobdagi shakli): funksiyalarning nomlariga
qarash. Agar hisobot moduli `getTotalHours` nomli funksiyaga ega
bo'lsa, vaqt kartalarini qabul qiladigan modulda esa `saveTimeCard`
bo'lsa, nomi bo'yicha qaysi biri jamini hisoblashini aytadi - javob
ravshan. Unumdorlik sababi bilan jami boshqa joyda hisoblanishi mumkin,
lekin bunda funksiya nomi shuni aks ettirishi kerak, masalan vaqt
kartalari modulida `computeRunningTotalOfHours` (G17, 295-296 bet).

**Tuzatish**: Move Function (2-nashr, 198-bet). Fowler ning Feature
Envy yozuvidagi evristika ham shu qarorga yordam beradi: metod bir
necha sinfning imkoniyatlarini ishlatsa, ma'lumotning ko'p qismi qaysi
sinfda bo'lsa, metod shu ma'lumot bilan qo'yiladi (1-nashr, 67-bet).
GRASP ning Information Expert printsipi [patternlar
hujjatida](../patterns/26-dizayn-printsiplari-solid-grasp-va-umumiy.md).

## 33.13 Noo'rin statik (Inappropriate Static)

**Manba**: *Clean Code*, 17-bob, G18 "Inappropriate Static" (296-bet).

**Belgisi**: statik metod aslida polimorfizm talab qiladi. Martin
ikkita misolni qarshi qo'yadi. `Math.max(double, double)` yaxshi statik
metod: u bitta instans ustida ishlamaydi, barcha ma'lumotni ikki
argumentidan oladi, va uning polimorf bo'lishini xohlash ehtimoli
deyarli yo'q. `HourlyPayCalculator.calculatePay(employee, overtimeRate)`
esa birinchi qarashda shunday ko'rinadi, lekin uning polimorf bo'lishi
kerak bo'lish ehtimoli jiddiy: ish haqini hisoblashning bir necha
algoritmi kerak bo'lishi mumkin, shuning uchun bu funksiya statik
bo'lmasligi va `Employee` ning instans metodi bo'lishi kerak (G18,
296-bet).

**Qoida**: umuman statik metoddan ko'ra statik bo'lmagan metodni
tanlash kerak; ikkilanganda metod statik bo'lmaydi. Metod haqiqatan
statik bo'lishi kerak bo'lsa, uning polimorf bo'lishini xohlash
ehtimoli yo'qligiga ishonch hosil qilish lozim (G18, 296-bet).

**Tuzatish**: statik metodni instans metodiga aylantirish, keyin kerak
bo'lsa strategiya interfeysiga chiqarish. Haqiqiy sof funksiyalar
statik qoladi (14.8). Test uchun statik metodni almashtirish
qiyinligi (31.5) shu korpusning qo'shimchasi, G18 da aytilmagan.

## 33.14 Bazaviy sinf vorisga bog'liq (Base Class Depending on Derivatives)

[Bazaviy sinfning voris sinfga bog'liqligi](17-vorislik-kompozitsiya-va-polimorfizm.md#175-bazaviy-sinfning-voris-sinfga-bogliqligi)
bo'limida ko'rilgan.

**Manba**: *Clean Code*, 17-bob, G7 "Base Classes Depending on Their
Derivatives" (291-bet).

**Belgisi**: bazaviy sinfda voris sinf nomlari, `instanceof`
tekshiruvlari yoki voris sinflarga mos `switch`.

**Nega muammo**: tushunchalarni bazaviy va voris sinflarga ajratishning
eng keng tarqalgan sababi - yuqori darajadagi bazaviy sinf tushunchalari
quyi darajadagi voris sinf tushunchalaridan mustaqil bo'lishi. Shuning
uchun bazaviy sinf vorislarining nomini aytsa, muammo gumon qilinadi:
umuman bazaviy sinf vorislari haqida hech narsa bilmasligi kerak (G7,
291-bet).

**Istisno** (kitobda aytilgan): vorislar soni qat'iy belgilangan va
bazaviy sinfda vorislar orasidan tanlaydigan kod bo'lgan holat;
Martin buni finite state machine implementatsiyalarida ko'p
uchratganini yozadi. Bunda vorislar va bazaviy sinf qattiq bog'langan
va doim bitta jar fayl bilan birga deploy qilinadi. Umumiy holatda
vorislarni va bazani alohida jar fayllarda deploy qilish imkoni
bo'lishi kerak: bu o'zgarishning ta'sirini kamaytiradi va tizimni
mustaqil komponentlar sifatida deploy qilishga imkon beradi (G7,
291-bet).

**Tuzatish**: abstrakt metod kiritish (Replace Conditional with
Polymorphism, 2-nashr, 272-bet), yoki bazaviy sinfni interfeysga
aylantirish.

## 33.15 Majburiy sozlash kodi (Required Setup Code)

**Nomi haqida**: "Required Setup Code" nomi na *Refactoring* ning
ikki nashrida, na *Clean Code* 17-bobida yo'q; u shu korpusning
sarlavhasi. Kitobdagi nomi - Martin ning G31 "Hidden Temporal
Couplings" evristikasi (*Clean Code*, 17-bob, 302-303 bet), bu
korpusda 6.9 da ham ko'rilgan.

**Belgisi**: obyektni ishlatishdan oldin bir necha metodni ma'lum
tartibda chaqirish kerak, lekin tartib kodda majburlanmagan.
Kitobdagi misolda uchta metod ketma-ket chaqiriladi va tartib muhim,
chunki birinchisi bajarilmasa ikkinchisi ishlamaydi; lekin kod bu
tartibni majburlamaydi va boshqa dasturchi ularni teskari tartibda
chaqirib istisno oladi (G31, 302-303 bet).

**Nega muammo**: vaqt bog'liqligi ko'pincha zarur, lekin uni
yashirmaslik kerak; funksiyalarning argumentlarini chaqiruv tartibi
ravshan bo'ladigan shaklda tuzish lozim (G31, 302-bet).

**Tuzatish**: tartibni imzoga olib chiqish. Kitobdagi yechim - har bir
funksiya keyingisiga kerak bo'lgan natijani qaytaradi, shunda ularni
tartibsiz chaqirishning aqlga sig'adigan yo'li qolmaydi; Martin buni
"bucket brigade" deb ataydi va bu funksiyalarning sintaktik
murakkabligini oshirishini tan oladi, lekin bu qo'shimcha murakkablik
vaziyatning haqiqiy vaqt murakkabligini ochib berishini aytadi (G31,
303-bet).

Korpusning amaliy tavsiyasi (kitobdan olingan emas): Java da
konstruktorda to'liq qurish (14.9), builder (16.5), yoki 6.9 dagi
"o'tkazish" uslubi; testdagi sozlash uchun builder va object mother
(30.3).

## 33.16 Kombinatorik portlash (Combinatorial Explosion)

**Nomi haqida**: "Combinatorial Explosion" nomi na *Refactoring* ning
ikki nashrida, na *Clean Code* 17-bobida yo'q; u shu korpusning
sarlavhasi va bu bo'lim kitobdan hid sifatida iqtibos qilinmaydi.

**Belgisi**: bir xil ishning har bir kombinatsiyasi uchun alohida metod
yoki sinf: `findByCustomer`, `findByCustomerAndStatus`,
`findByCustomerAndStatusAndDate`, va shu davom etadi (28.5).

**Kitobda nimaga tayanadi**: tuzilishi bir xil, faqat qiymatlari
boshqa bo'lgan kod Fowler da takrorlanishning shakli sifatida sanalgan
(1-nashr, 63-64 bet; 32.2), va birga yuradigan parametrlar to'dasi
Data Clumps yozuvining mavzusi (1-nashr, 67-bet; 32.6). Ikkisining ham
yechimi bitta yo'nalishni ko'rsatadi: parametrlarni obyektga yig'ish.

**Tuzatish**: Introduce Parameter Object (1-nashr, 238-bet; 2-nashr,
140-bet) - mezon obyekti. Korpusning qo'shimchasi (kitobdan olingan
emas): Specification pattern ([patternlar
hujjatida](../patterns/13-domain-driven-design-patternlari.md)) yoki
builder bilan so'rov qurish (28.5).

## 33.17 Sochma jarrohlik (Shotgun Surgery)

**Manba**: 1-nashr 66-bet, 2-nashr 76-bet; nom ikki nashrda bir xil.

**Belgisi**: bitta turdagi o'zgarish kerak bo'lganda ko'p sinfda ko'p
kichik o'zgarish qilishga to'g'ri keladi; o'zgarishlar tarqoq bo'lgani
uchun ularni topish qiyin va muhim birini o'tkazib yuborish oson
(1-nashr, 66-bet).

**Nega muammo va tuzatish**: bu hid 33.1 ning teskarisi va ikkisi
kitobda bir sahifada juft sifatida beriladi, shuning uchun to'liq
tahlil, farqi va 1-nashr tavsiya qilgan harakatlar ketma-ketligi
(Move Method, Move Field, kerak bo'lsa yangi sinf, ba'zan Inline Class)
33.1 ning **Juftlik hid** qismida turadi va bu yerda takrorlanmaydi.
2-nashrdagi nomlar: Move Function (198-bet), Move Field (207-bet),
Inline Class (186-bet).

Bu bo'lim katalogni to'liq saqlash uchun alohida raqam oladi: hid
2-nashr 3-bobining 24 ta yozuvidan biri.

Spring kontekstidagi ko'rinishi - bitta maydonni entity, DTO, mapper,
migratsiya, validatsiya va OpenAPI sxemasiga qo'shish: [patternlar
hujjatining sochma jarrohlik
yozuvi](../patterns/25-anti-patternlar.md#2521-sochma-jarrohlik-shotgun-surgery).
Diffda ikki hidni birga ko'rish usuli [code review
hujjatida](../code-review/07-bogliqlik-koheziya-va-abstraksiya-review.md#77-feature-envy-va-shotgun-surgery).

## 33.18 Begona ma'lumotga havas (Feature Envy)

**Manba**: 1-nashr 66-67 bet, 2-nashr 77-bet; nom ikki nashrda bir xil.
*Clean Code* da shu hid G14 kodi bilan turadi (293-bet).

**Belgisi**: metod o'zi turgan sinfdan ko'ra boshqa sinfga ko'proq
qiziqadi. Havasning eng ko'p uchraydigan nishoni - ma'lumot: qiymat
hisoblash uchun boshqa obyektning yarim dyuzina getter ini ketma-ket
chaqiradigan metod (1-nashr, 66-bet).

**Nega muammo**: obyektlarning butun ma'nosi - ma'lumotni shu ma'lumot
ustida ishlatiladigan jarayonlar bilan birga qadoqlash texnikasi
bo'lishi (1-nashr, 66-bet).

**Tuzatish** (1-nashr, 66-67 bet): metod boshqa joyda bo'lishni
xohlayotgani ravshan, shuning uchun Move Method. Metodning faqat bir
qismi havas qilsa, havasli bo'lakka Extract Method va keyin Move
Method. Metod bir necha sinf xususiyatini ishlatsa, kitobning
evristikasi shunday: ma'lumotning ko'pi qaysi sinfda bo'lsa, metod shu
ma'lumot bilan birga qo'yiladi; Extract Method bilan metodni turli
joyga ketadigan bo'laklarga bo'lish bu qadamni osonlashtiradi.
2-nashrdagi nomlar: Move Function (198-bet), Extract Function
(106-bet); mexanikasi 35.12 va 35.1 da.

**Qoidani ataylab buzadigan patternlar** (1-nashr, 67-bet): GoF ning
Strategy va Visitor patternlari, hamda Kent Beck ning Self Delegation
usuli. Ular tarqoq o'zgarish hidiga (33.1) qarshi ishlatiladi. Asosiy
qoida - birga o'zgaradigan narsalarni birga qo'yish; ma'lumot va unga
murojaat qiladigan xatti-harakat odatda birga o'zgaradi, lekin
istisnolar bo'ladi va shunda xatti-harakat o'zgarishni bir joyda
saqlash uchun ko'chiriladi. Strategy va Visitor override qilinishi
kerak bo'lgan kichik xatti-harakatni ajratib, uni oson o'zgartirishga
imkon beradi; narxi - qo'shimcha vositachilik.

Noto'g'ri joylashgan javobgarlik (33.12) shu hidning *Clean Code*
tomonidagi qardoshi. Spring kontekstidagi shakli - anemik domen modeli:
[patternlar hujjatining begona ma'lumotga havas
yozuvi](../patterns/25-anti-patternlar.md#2520-begona-malumotga-havas-feature-envy).
Diffda aniqlash usuli [code review
hujjatida](../code-review/07-bogliqlik-koheziya-va-abstraksiya-review.md#77-feature-envy-va-shotgun-surgery).

## 33.19 Katta sinf (Large Class)

**Manba**: 1-nashr 65-bet, 2-nashr 82-bet; nom ikki nashrda bir xil.

**Belgisi**: sinf juda ko'p ish qilmoqchi bo'lganda bu ko'pincha juda
ko'p instansiya o'zgaruvchisi sifatida ko'rinadi. Kitob ketma-ketlikni
aniq aytadi: instansiya o'zgaruvchilari ko'p bo'lsa, takrorlangan kod
uzoqda emas (1-nashr, 65-bet).

**Nega muammo**: ham o'zgaruvchisi ko'p, ham kodi ko'p sinf -
takrorlanish, tartibsizlik va o'lim uchun eng yaxshi ko'payish joyi
(1-nashr, 65-bet). Bu yagona javobgarlik printsipining buzilishi.

**Tuzatish** (1-nashr, 65-bet):

- o'zgaruvchilarning bir qismini Extract Class bilan bitta komponentga
  bog'lash; birga ketadigan o'zgaruvchilarni tanlash, masalan
  `depositAmount` va `depositCurrency` bitta komponentga tegishli;
  umumiy prefiks yoki suffiks komponent imkoniyatini ko'rsatadi;
- komponent voris sinf sifatida ma'noli bo'lsa, Extract Subclass
  ko'pincha osonroq;
- sinf o'z instansiya o'zgaruvchilarining hammasini har doim
  ishlatmasa, Extract Class yoki Extract Subclass ni bir necha marta
  qo'llash mumkin;
- kodi ko'p sinfda avval sinf ichidagi ortiqchalikni yo'qotish: umumiy
  kodi ko'p bo'lgan beshta yuz qatorli metodni beshta o'n qatorli
  metodga va ulardan ajratilgan o'nta ikki qatorli metodga aylantirish;
- mijozlar sinfdan qanday foydalanayotganini aniqlab, har bir
  foydalanish uchun Extract Interface qo'llash - bu sinfni yanada
  bo'lish g'oyasini beradi.

**Nashrlar farqi**: 1-nashr tavsiya qiladigan Extract Subclass va
Extract Interface 2-nashrning "List of Refactorings" ro'yxatida yo'q.
2-nashrda shu yo'nalishdagi nomlar: Extract Class (182-bet), Extract
Superclass (375-bet), Replace Type Code with Subclasses (362-bet);
mexanikasi 36.1, 37.15 va 37.13 da.

Qaysi maydon va metod bitta komponentga tegishli ekanini topish usullari
(metod guruhlash, yashirin metodlar va feature sketch) [mas'uliyatni
ko'rish bo'limida](#3321-katta-sinfda-masuliyatni-korish-metod-guruhlash-va-feature-sketch).

Arxitektura darajasidagi haddan oshgan shakli - [patternlar hujjatining
xudo obyekt yozuvi](../patterns/25-anti-patternlar.md#251-xudo-obyekt-god-object).

## 33.20 Spekulyativ umumiylik (Speculative Generality)

**Manba**: 1-nashr 68-bet, 2-nashr 80-bet; nom ikki nashrda bir xil.
Nomni Brian Foote taklif qilgan (1-nashr, 68-bet).

**Belgisi**: "Oh, menimcha bir kun kelib shunday narsa qilish qobiliyati
kerak bo'ladi" degan asosda talab qilinmagan narsalarni boshqarish uchun
har xil hook va maxsus holatlar kiritiladi (1-nashr, 68-bet).

**Nega muammo**: natija ko'pincha tushunish va saqlashga qiyinroq
bo'ladi. Kitob mezonini oshkor beradi: agar bu butun mashina
ishlatilayotgan bo'lsa, u o'zini oqlaydi; ishlatilmasa, oqlamaydi -
mashina shunchaki yo'lni to'sadi, demak uni olib tashlash kerak
(1-nashr, 68-bet).

**Tuzatish** (1-nashr, 68-bet): ko'p ish qilmaydigan abstrakt sinflar
uchun Collapse Hierarchy; keraksiz delegatsiyani Inline Class bilan
olib tashlash; ishlatilmaydigan parametrli metodlarga Remove Parameter;
g'alati abstrakt nom bilan nomlangan metodlarni Rename Method bilan
yerga tushirish. 2-nashrdagi nomlar: Collapse Hierarchy (380-bet),
Inline Class (186-bet) va Change Function Declaration (124-bet, 1-nashr
Remove Parameter bilan Rename Method ni shu bitta harakatga
birlashtirgan); mexanikasi 37.15, 36.2 va 35.5 da.

**Kitobdagi aniqlash usuli** (1-nashr, 68-bet): metod yoki sinfning
yagona foydalanuvchisi test holatlari bo'lsa, bu spekulyativ umumiylik
belgisi. Bunday metod yoki sinfni va uni ishlatadigan testni o'chirish
kerak. Lekin metod yoki sinf qonuniy funksionallikni sinaydigan test
uchun yordamchi bo'lsa, u albatta joyida qoldiriladi.

Dangasa element (32.9) bilan farqi: 32.9 - o'zini oqlamay qolgan
element, bu yerdagi hid esa hech qachon o'zini oqlamagan element.
Spring kontekstidagi shakli va "Rule of Three" mezoni [patternlar
hujjatining spekulyativ umumiylik
yozuvida](../patterns/25-anti-patternlar.md#2525-spekulyativ-umumiylik--ortiqcha-injinerlik-speculative-generality--over-engineering).

## 33.21 Katta sinfda mas'uliyatni ko'rish: metod guruhlash va feature sketch

33.19 Extract Class ni harakat sifatida beradi, lekin "qaysi maydon va
qaysi metod bitta komponentga tegishli" savolini ochiq qoldiradi.
Feathers shu savolni alohida ko'nikma deb ataydi va muhim shartini
aytadi: mas'uliyat o'ylab chiqarilmaydi, mavjud koddan topiladi - kod
qanday tuzilgan bo'lishidan qat'i nazar, uning bo'laklari aniq ishlarni
qiladi (Feathers, *Working Effectively with Legacy Code*, Prentice Hall
PTR, 2004 (copyright 2005), 20-bob, 249-bet).

| Evristika | Nima qilinadi | Belgi va manba |
|---|---|---|
| Metodlarni guruhlash | sinfning hamma metodi kirish darajasi (`public`, `private`) bilan yozib chiqiladi va nomi bir-biriga o'xshaganlari bitta ro'yxatga yig'iladi | "bu metod nega shu yerda" va "u sinf uchun nima qilyapti" savollariga javobi bir xil bo'lgan metodlar bitta mas'uliyat (249-bet) |
| Yashirin metodlarga qarash | `private` va `protected` metodlar sanaladi | ularning ko'pligi sinf ichida chiqishga intilgan boshqa sinf borligini bildiradi; "private metodni qanday testlayman" savoli shuning belgisi (250-bet) |
| Ichki munosabatlarni izlash | qaysi instansiya maydoni qaysi metodda ishlatilayotgani chiziladi | maydon va metodlar to'da bo'lib yig'iladi: uch metod faqat uch maydonga tegadi, qolganlariga tegmaydi (251-252-bet) |

Uchinchi evristikaning asbobi **feature sketch**: sinf ichidagi
metodlar bir-birini va instansiya maydonlarini qanday ishlatishini
ko'rsatadigan kichik qo'lda chizma; u katta sinfni qanday bo'lish
haqida qaror qilayotganda foydali (shu yerda, lug'at, 421-bet). Chizma
bir martalik asbob: o'zgarishdan oldin juftlikda taxminan o'n daqiqada
chiziladi va keyin tashlanadi, shuning uchun uni chiroyli qilishga
urinish kerak emas (shu yerda, 254-bet).

```java
public class SettlementImporter {
    private final BankGateway gateway;
    private final RowParser parser;
    private final List<String> auditLines = new ArrayList<>();
    private int acceptedCount;
    private int rejectedCount;

    public void importFile(Path file) { ... }
    private SettlementRow parse(String line) { ... }
    private boolean isValid(SettlementRow row) { ... }
    private void send(SettlementRow row) { ... }
    private void audit(String message) { ... }
    public ImportReport report() { ... }
}
```

Shu sinfning feature sketch ini matn shaklida yozsak:

| Metod | Tegadigan maydon |
|---|---|
| `parse` | `parser` |
| `isValid` | yo'q |
| `send` | `gateway` |
| `audit` | `auditLines` |
| `report` | `auditLines`, `acceptedCount`, `rejectedCount` |
| `importFile` | hammasi |

Jadvaldan ikki to'da ko'rinadi. Birinchisi `audit`, `report`,
`auditLines`, `acceptedCount` va `rejectedCount`: bu import hisobini
yuritish mas'uliyati va u `ImportAudit` sinfiga chiqadi. Ikkinchisi
`parse` va `isValid`: ular sinfning hech bir holatiga tegmaydi, ya'ni
`SettlementRowParser` sifatida mustaqil yashaydi. Ikkinchi evristika shu
yerda birinchisini tasdiqlaydi: `parse` va `isValid` ning `private`
bo'lishi tasodif emas, ular boshqa sinfning public metodlari.
Yangi sinfda ularni `public` qilish inkapsulyatsiyani buzmaydi, chunki
importer ularni o'zi uchun, private tarzda ishlatishda davom etadi
(shu yerda, 250-bet).

Feathers bu ishni darhol refaktoringga aylantirishni talab qilmaydi:
asosiy mas'uliyatdan chetda turgan guruhni topish yetarli, keyin shu
guruhdagi metodlardan birini o'zgartirish kerak bo'lganda sinfni
ajratish haqida qaror qilinadi (shu yerda, 250-bet). Ajratishning o'zi
33.19 dagi Extract Class va 36-bobdagi mexanika.

Ajratishdan keyin bitta kutilmagan natija chiqadi va unga oldindan
tayyor bo'lish kerak: refaktoring qilingan kod ko'pincha **uzunroq**
bo'ladi. Uchta sabab bor va uchalasi ham ataylab: nom uzunroq va
tavsifiy bo'ladi, izoh o'rniga funksiya va sinf e'lonlari paydo
bo'ladi, hamda bo'sh joy bilan formatlash o'qish guruhlarini ajratadi.
Qator soni ortgani sifat pasaygani emas: review da "refaktoring kodni
uzaytirdi" e'tirozi chiqsa, javob shu - o'lchov qator soni emas,
bo'lakning tushunarliligi va o'zgarishga tayyorligi.

ESLATMA: feature sketch ni jadval shaklida yozish shu korpusning matn
uchun moslashtirilgan shakli; kitobda u doira va chiziqlardan iborat
qo'lda chizma. Yuqoridagi `SettlementImporter` misoli ham korpusning
o'zi: kitobdagi misol `Reservation` sinfi.

## 33.22 Amalda qo'llash

- [ ] Eng ko'p o'zgargan 10 sinf uchun `git log` dan o'zgarish sabablarini sanab, tarqoq o'zgarishni (33.1) aniqlang.
- [ ] Faqat getter va setter dan iborat domen sinflarini topib, 33.2 dagi besh qadamni tartib bilan qo'llang.
- [ ] Bir-birining private holatiga murojaat qiladigan sinf juftliklarini topib, chegarani qayta chizing; vorislik orqali kelgan yaqinlikni alohida belgilang.
- [ ] Bir xil vazifani bajaradigan, lekin turli imzolarga ega sinflarni avval Change Function Declaration bilan moslang, protokol bir xil bo'lgandan keyin Extract Superclass ni ko'rib chiqing.
- [ ] Parallel ierarxiyalarni nom prefikslari bo'yicha topib, bir ierarxiya ikkinchisiga murojaat qiladigan shaklga keltiring.
- [ ] Public API ni ko'rib chiqishda metod sonini sanashdan boshlamang: G8 ning savolini bering - shu element tashqariga chiqishi shartmi?
- [ ] Izchilsizlik ro'yxatini tuzib (`Optional` va `null`, nomlash, inyeksiya), har biri uchun bitta konvensiya kelishib oling va uni linterga topshiring.
- [ ] Ishlatilmaydigan maydon, metod va importlarni IDE inspeksiyasi bilan topib o'chiring; bo'sh default konstruktorlarni alohida qidiring.
- [ ] Ma'lum tartibda chaqirilishi kerak bo'lgan metodlarni topib, tartibni imzoga chiqaring (33.15).
- [ ] Eng katta sinflar uchun metod-maydon jadvalini (feature sketch) tuzib, to'da bo'lib ajralgan guruhni Extract Class nomzodi sifatida yozib qo'ying (33.21).

## Manbalar

- Martin Fowler va Kent Beck, *Refactoring: Improving the Design of
  Existing Code*, 1-nashr, Addison-Wesley, 1999, 3-bob "Bad Smells in
  Code" (63-72 bet) - 33.1-33.7 dagi hidlarning nomi, ta'rifi va
  mexanikasi: Divergent Change va Shotgun Surgery (66), Feature Envy
  evristikasi (67), Parallel Inheritance Hierarchies (68), Inappropriate
  Intimacy, Alternative Classes with Different Interfaces, Incomplete
  Library Class va Data Class (70), Refused Bequest (71)
- Robert C. Martin, *Clean Code*, 10-bob (146-bet) - refaktoring qilingan
  kodning uzunroq bo'lishi va uning uchta sababi: uzunroq tavsifiy nom,
  izoh o'rnidagi funksiya va sinf e'lonlari, bo'sh joy bilan formatlash
- Martin Fowler, *Refactoring*, 1-nashr, Addison-Wesley, 1999, 7, 10 va
  11 boblar - 33.7 va 33.16 da keltirilgan harakatlarning betlari:
  Introduce Foreign Method (131), Introduce Local Extension (133,
  voris sinf yoki wrapper shakli), Introduce Parameter Object (238),
  Replace Inheritance with Delegation (287)
- Martin Fowler, *Refactoring*, 2-nashr, Pearson Addison-Wesley, 2019,
  mundarija (71-84 bet) - 2-nashrdagi 24 hidning ro'yxati: Divergent
  Change (76), Shotgun Surgery (76), Insider Trading (82, 1-nashrdagi
  Inappropriate Intimacy ning yangi nomi), Alternative Classes with
  Different Interfaces (83), Data Class (83), Refused Bequest (83);
  shu ro'yxatda Parallel Inheritance Hierarchies va Incomplete Library
  Class yo'q, ya'ni 33.6 va 33.7 faqat 1-nashrdan
- Martin Fowler, *Refactoring*, 2-nashr, Pearson Addison-Wesley, 2019,
  mundarija, 6-12 boblar - harakatlarning 2-nashrdagi nomlari va
  betlari: Introduce Parameter Object (140), Split Phase (154),
  Encapsulate Record (162), Encapsulate Collection (170), Extract Class
  (182), Inline Class (186), Hide Delegate (189), Move Function (198),
  Move Field (207), Remove Dead Code (237), Replace Conditional with
  Polymorphism (272), Remove Setting Method (331), Push Down Method
  (359), Push Down Field (361), Extract Superclass (375), Replace
  Superclass with Delegate (399)
- Robert C. Martin, *Clean Code*, Prentice Hall, 2008, 17-bob "Smells
  and Heuristics" - 33.8-33.15 ning manbasi: G7 Base Classes Depending
  on Their Derivatives (291), G8 Too Much Information (291-292), G9 Dead
  Code (292), G11 Inconsistency (292), G12 Clutter (293), G13 Artificial
  Coupling (293), G17 Misplaced Responsibility (295-296), G18
  Inappropriate Static (296), G31 Hidden Temporal Couplings (302-303)
- ESLATMA: 33.15 va 33.16 sarlavhalaridagi nomlar ("Required Setup
  Code", "Combinatorial Explosion") ikki katalogda ham yo'q, ular shu
  korpusning atamalari; 33.15 ning kitobdagi nomi G31 "Hidden Temporal
  Couplings"
- ESLATMA: 33.1 dagi `git log` bilan o'zgarish sabablarini sanash,
  33.2 dagi DTO va `record` istisnosi, 33.4 dagi adapter varianti,
  33.6 dagi `sealed` ierarxiya, 33.7 dagi kutubxona turini domenda
  tarqatmaslik, 33.13 dagi testda almashtirish qiyinligi va 33.16 dagi
  Specification pattern shu korpusning amaliy tavsiyalari, kitobdan
  olingan emas
- ESLATMA: 33.21 dagi tekshiruv ro'yxati shu korpusning amaliy
  tavsiyasi, kitobdan olingan emas
- Martin Fowler va Kent Beck, *Refactoring: Improving the Design of
  Existing Code*, 1-nashr, Addison-Wesley, 1999, 3-bob "Bad Smells in
  Code" (65-68 bet) - 33.17-33.20 ning ta'rifi va harakatlari: Large
  Class (65, instansiya o'zgaruvchilari va Extract Class / Extract
  Subclass / Extract Interface yo'li), Shotgun Surgery (66), Feature
  Envy (66-67, ma'lumot ko'pi qaysi sinfda bo'lsa mezoni, hamda
  Strategy, Visitor va Self Delegation istisnolari), Speculative
  Generality (68, Brian Foote nomlagani va faqat test ishlatadigan
  element mezoni)
- Martin Fowler, *Refactoring*, 2-nashr, Pearson Addison-Wesley, 2019,
  mundarija (71-84 bet) va "List of Refactorings" - 33.17-33.20 dagi
  2-nashr nomlari va betlari: Shotgun Surgery (76), Feature Envy (77),
  Speculative Generality (80), Large Class (82), Collapse Hierarchy
  (380), Change Function Declaration (124), Extract Superclass (375),
  Replace Type Code with Subclasses (362); 1-nashrdagi Extract Subclass
  va Extract Interface bu ro'yxatda yo'q
- Robert C. Martin, *Clean Code*, Prentice Hall, 2008, 17-bob "Smells
  and Heuristics" - 33.18 ning *Clean Code* dagi kodi: G14 Feature Envy
  (293)
- Michael Feathers, *Working Effectively with Legacy Code*, Prentice Hall PTR,
  2004 (copyright 2005), 20-bob (249-254) - mas'uliyatni mavjud koddan
  topish; metod guruhlash, yashirin metodlar va ichki munosabatlar
  evristikalari; feature sketch chizmasi va uning bir martaligi
- Michael Feathers, *Working Effectively with Legacy Code*, Prentice Hall PTR,
  2004 (copyright 2005), lug'at (421) - feature sketch ta'rifi

---

[&larr; 32. Kod hidlari katalogi I: nom, funksiya, ma'lumot](32-kod-hidlari-katalogi-i-nom-funksiya-malumot.md) · [Mundarija](README.md) · [34. Toza kod evristikalarining to'liq ro'yxati &rarr;](34-toza-kod-evristikalarining-toliq-royxati.md)
