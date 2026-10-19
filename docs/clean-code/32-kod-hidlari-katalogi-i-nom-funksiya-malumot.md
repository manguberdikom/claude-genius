<!-- doc: clean-code | chapter: 32 | part: X. Hid katalogi va refaktoring harakatlari -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 32. Kod hidlari katalogi I: nom, funksiya, ma'lumot (Code Smells I)

<details>
<summary>Bu bobdagi 17 bo'lim</summary>

- [32.1 Sirli nom (Mysterious Name)](#321-sirli-nom-mysterious-name)
- [32.2 Takrorlangan kod (Duplicated Code)](#322-takrorlangan-kod-duplicated-code)
- [32.3 Uzun funksiya (Long Function)](#323-uzun-funksiya-long-function)
- [32.4 Global ma'lumot (Global Data)](#324-global-malumot-global-data)
- [32.5 O'zgaradigan ma'lumot (Mutable Data)](#325-ozgaradigan-malumot-mutable-data)
- [32.6 Ma'lumot to'dasi (Data Clumps)](#326-malumot-todasi-data-clumps)
- [32.7 Takrorlangan `switch` (Repeated Switches)](#327-takrorlangan-switch-repeated-switches)
- [32.8 Sikllar (Loops)](#328-sikllar-loops)
- [32.9 Dangasa element (Lazy Element)](#329-dangasa-element-lazy-element)
- [32.10 Vaqtinchalik maydon (Temporary Field)](#3210-vaqtinchalik-maydon-temporary-field)
- [32.11 Uzun xabar zanjiri (Message Chains)](#3211-uzun-xabar-zanjiri-message-chains)
- [32.12 Vositachi (Middle Man)](#3212-vositachi-middle-man)
- [32.13 Izohlar hid sifatida (Comments)](#3213-izohlar-hid-sifatida-comments)
- [32.14 Uzun parametrlar ro'yxati (Long Parameter List)](#3214-uzun-parametrlar-royxati-long-parameter-list)
- [32.15 Primitivlarga berilish (Primitive Obsession)](#3215-primitivlarga-berilish-primitive-obsession)
- [32.16 Bu hid emas: qachon tegmaslik kerak](#3216-bu-hid-emas-qachon-tegmaslik-kerak)
- [32.17 Amalda qo'llash](#3217-amalda-qollash)

</details>


Kod hidi - xato emas, lekin muammo ehtimolini oshiradigan tuzilish. Atama
Kent Beck dan keladi: Fowler *Refactoring* ning 3-bobini ("Bad Smells in
Code") Beck bilan birga yozgan va 1-nashrda 22 hid sanalgan (1999, 63-72
bet). 2-nashrda ro'yxat 24 ga chiqqan, ba'zi nomlar o'zgargan va bir
nechtasi olib tashlangan (2019, 71-84 bet). Bu bob nom, funksiya va
ma'lumot darajasidagi hidlarni beradi, [33-bob](33-kod-hidlari-katalogi-ii-sinf-ierarxiya.md)
sinf va ierarxiya darajasini.

Ikkinchi katalog Robert C. Martin ning *Clean Code* 17-bobidagi
evristikalar (C, E, F, G, J, N, T kodlari, 285-308 bet); ularning to'liq
ro'yxati [34-bobda](34-toza-kod-evristikalarining-toliq-royxati.md).
Arxitektura darajasidagi anti-patternlar [patternlar hujjatining
anti-patternlar bobida](../patterns/25-anti-patternlar.md); bu bob
ularni takrorlamaydi. Ikki hid (32.14 va 32.15) shu hujjatning boshqa
boblarida va patternlar katalogida batafsil yozilgan: bu yerda ularning
katalog yozuvi - nom, bet, kitobdagi sabab va harakat - turadi, Spring
darajasidagi tahlil esa havolada.

Nashr qoidasi shu bobda qat'iy: hidning **nomi** va **beti** 2-nashrdan
keltirilishi mumkin (mundarija tasdiqlaydi), hidning **ta'rifi va
mexanikasi** esa faqat 1-nashrdan (1999) olinadi. Nomi o'zgargan hidda
ikki nom ham ko'rsatiladi. Har bir hid uchun uch qism: belgisi, nega
muammo, va qaysi refaktoring harakati bilan tuzatiladi
([35-37 boblar](35-refaktoring-harakatlari-katalogi-i-funksiya.md)).

## 32.1 Sirli nom (Mysterious Name)

**Belgisi**: nomni o'qib nima qilayotganini aytib bo'lmaydi; `proc`,
`handle`, `data2`, `tmpFlag`.

**Manba**: hid 2-nashr ro'yxatining birinchisi, "Mysterious Name"
(72-bet). 1-nashrda alohida hid sifatida sanalmagan.

**Nega muammo**: McConnell yaxshi nom muammo haqida gapiradi, yechim
haqida emas deb yozadi: xodim ma'lumotlari uchun `inputRec` kompyuter
atamasi, `employeeData` esa predmet sohasining atamasi; printer holati
uchun `bitFlag` dan `printerReady` yaxshi (*Code Complete*, 2-nashr,
11.1, 262-bet).

Nom uzunligi uchun o'lchangan raqam bor: Gorla, Benander va Benander
(1990) tadqiqotida dasturni debug qilish mehnati o'zgaruvchi nomlari
o'rtacha 10-16 belgi bo'lganda eng kam bo'lgan, 8-20 belgi oralig'i
esa deyarli shunday yaxshi (*Code Complete*, 2-nashr, 262-bet). McConnell
buni chegara deb o'qimaslikni alohida aytadi: maqsad hamma nomni shu
oraliqqa keltirish emas, nomlar bundan qisqa bo'lsa, ular yetarlicha
aniqligini tekshirish.

**Tuzatish**: Rename Variable (2-nashr, 137-bet), Rename Field (2-nashr,
244-bet), Change Function Declaration (2-nashr, 124-bet); 1-nashrdagi
mos harakat Rename Method (221-bet).

## 32.2 Takrorlangan kod (Duplicated Code)

Fowler va Beck ro'yxatni shu hiddan boshlaydi va unga birinchi o'rinni
beradi: bir xil kod tuzilishi bir necha joyda ko'rinsa, ularni
birlashtirish yo'lini topish dasturni yaxshilashi aniq (1-nashr,
63-bet). Martin ham buni kitobining eng muhim qoidalaridan biri deb
ataydi, DRY ga va Kent Beck ning "Once, and only once" shakliga
bog'laydi, va har bir takrorlanishni qo'ldan ketgan abstraksiya imkoni
deb o'qiydi (*Clean Code*, G5, 289-290 bet). DRY printsipining o'zi
[patternlar hujjatida](../patterns/README.md).

| Tur | Ko'rinishi | Yechim | Manba |
|---|---|---|---|
| Aynan takrorlanish | bir xil ifoda bitta sinfning ikki metodida | Extract Method va ikki joydan chaqirish | Fowler 1-nashr, 63-bet |
| Qardosh takrorlanish | bir xil ifoda ikki qardosh voris sinfda | ikki sinfda Extract Method, so'ng umumiy metodni bazaga ko'tarish (2-nashr: Pull Up Method, 350-bet) | Fowler 1-nashr, 63-bet |
| Shaklli takrorlanish | tuzilish o'xshash, qatorlar bir xil emas | Extract Method bilan o'xshash va farqli qismni ajratish, keyin Form Template Method; algoritm boshqa bo'lsa Substitute Algorithm | Fowler 1-nashr, 63-64 bet |
| Takrorlangan shart zanjiri | bir xil `switch` yoki `if/else` bir necha modulda, doim bir xil shartlarni tekshiradi | polimorfizm (32.7) | Martin, G5, 290-bet |
| O'xshash algoritm | kod qatorlari umumiy emas, algoritm o'xshash | Template Method yoki Strategy | Martin, G5, 290-bet |
| Aloqasiz sinflarda | ikki bog'lanmagan sinfda bir xil kod | bir sinfda Extract Class, yangi komponentni ikkinchisida ishlatish | Fowler 1-nashr, 63-bet |

Korpusning amaliy qo'shimchasi (kitobdan olingan emas): tasodifan
o'xshash, lekin boshqa sabab bilan o'zgaradigan kodni birlashtirmaslik.
Fowler aloqasiz sinflardagi takrorlanish uchun Extract Class tavsiya
qiladi, ya'ni birlashtirishni taqiqlamaydi; qaror o'zgarish sababining
birligiga qarab qabul qilinadi ([arxitektor
hujjatidagi](../architect/README.md) noto'g'ri abstraksiya narxi
bo'limi).

## 32.3 Uzun funksiya (Long Function)

**Manba**: 2-nashrda "Long Function" (73-bet), 1-nashrda "Long Method"
(64-bet). Metod uzunligi [4-bobda](04-funksiya-kichiklik-va-bitta-ish.md)
va [arxitektor hujjatida](../architect/README.md) ham ko'rilgan.

Fowler ning asosiy nuqtasi uzunlikning o'zi emas: gap metod uzunligida
emas, metod **nima** qilishi va **qanday** qilishi orasidagi semantik
masofada (1-nashr, 64-bet). U amaliy evristika beradi: izoh yozish
ehtiyoji paydo bo'lsa, izoh o'rniga metod yoziladi va metod nomi
niyatni aytadi; hatto bitta qator ham tushuntirish talab qilsa,
ajratishga arziydi (1-nashr, 64-bet).

3-bobning kirishida Beck va Fowler aniq mezon bermasliklarini ochiq
aytadi: ularning tajribasida hech qanday metrika to'plami xabardor
inson sezgisidan ustun emas, va metodda qancha qator ko'p ekanini
o'quvchi o'zi aniqlashi kerak (1-nashr, 63-bet). Shuning uchun bu
bobda funksiya uzunligi uchun qattiq chegara yo'q.

Raqamli tomoni o'lchangan joyda bor. McConnell rutina uzunligi bo'yicha
tadqiqotlarni yig'adi (*Code Complete*, 2-nashr, 7.4, 173-174 bet):

| Tadqiqot | Natija |
|---|---|
| Basili va Perricone (1984) | rutina hajmi xato bilan teskari bog'langan: hajm oshgani sari (200 qatorgacha) qatorga to'g'ri keladigan xato soni kamaygan |
| Shen va boshqalar (1985) | rutina hajmi xato bilan bog'lanmagan; tuzilish murakkabligi va ma'lumot hajmi bog'langan |
| Card, Church va Agresti (1986) | 32 qator va undan kichik rutinalar arzonroq yoki kamroq xatoli bo'lmagan; 65 qator va kattalarini qatoriga arzonroq yozish mumkin bo'lgan |
| Selby va Basili (1991), 450 rutina | 143 ifodadan kichik rutinalarda qatorga 23 foiz ko'p xato bo'lgan, lekin ularni tuzatish 2,4 barobar arzon tushgan (*Code Complete*, 2-nashr, 174-bet) |
| Lind va Vairavan (1989) | kod eng kam o'zgargan holatda rutinalar o'rtacha 100-150 qator bo'lgan |
| Jones (1986), IBM | eng xatoga moyil rutinalar 500 qatordan katta bo'lgan; 500 dan keyin xato darajasi hajmga proporsional |

McConnell xulosasi: obyektga yo'naltirilgan kodda rutinalarning katta
qismi juda qisqa accessor bo'ladi, murakkab algoritm uchun esa rutinaga
100-200 qatorgacha (izohsiz, bo'sh qatorsiz) tabiiy o'sish ruxsat
etiladi; uzunlikni cheklash emas, cohesion, nesting chuqurligi,
o'zgaruvchi soni, qaror nuqtalari soni va kerakli izoh miqdori hal
qilishi kerak. 200 qatordan oshsa ehtiyot bo'lish kerak: katta
rutinalarda narx yoki xato kamayganini ko'rsatgan tadqiqotlarning hech
biri 200 dan yuqori o'lchamlarni bir-biridan ajratmagan (173-174 bet).

**Tuzatish**: 1-nashr Long Method uchun tartibni shunday beradi -
holatlarning deyarli hammasida Extract Method; temp lar yo'lni to'ssa
Replace Temp with Query; uzun parametr ro'yxatini Introduce Parameter
Object va Preserve Whole Object bilan qisqartirish; bu ham yetmasa
Replace Method with Method Object; shart ifodalari uchun Decompose
Conditional; sikl bo'lsa siklni va sikl ichidagi kodni o'z metodiga
chiqarish (64-65 bet). Ajratiladigan bo'lakni topish uchun izohlarga
qarash tavsiya etiladi: izoh semantik masofani ko'rsatadi (64-bet).
2-nashrdagi nomlar: Extract Function (106-bet), Replace Temp with Query
(178-bet), Introduce Parameter Object (140-bet), Preserve Whole Object
(319-bet), Decompose Conditional (260-bet), Split Loop (227-bet),
Replace Conditional with Polymorphism (272-bet).

**Uzun funksiyaning ikki turi**: hidni aniqlashda uzun metodning shakli
ham ma'lumot beradi. Feathers ikki turni nomlaydi (Feathers, *Working
Effectively with Legacy Code*, Prentice Hall PTR, 2004 (copyright
2005), 22-bob, 290-293-bet):

- **Bulleted method** - deyarli indentatsiyasiz metod: ketma-ket kod
  bo'laklaridan iborat va ro'yxatga o'xshaydi. Har bo'lakni Extract
  Function bilan chiqarish oson ko'rinadi, amalda esa vaqtinchalik
  o'zgaruvchi bir bo'lakda e'lon qilinib keyingisida ishlatiladi va
  bo'laklar shunchaki ajralmaydi. Shunga qaramay bu tur kamroq
  qo'rqinchli: indentatsiya yo'qligi yo'nalishni yo'qotmaslikka yordam
  beradi (290-bet).
- **Snarled method** - bitta katta indentatsiyalangan bo'lak hukmron
  bo'lgan metod; eng oddiy holati bitta ulkan shart, haqiqiy snarl esa
  ichma-ich shartlardan iborat. Tekshiruvi oddiy: uzun metodning
  bloklarini bir-biriga moslashtirishga urinib ko'rish kerak, boshingiz
  aylansa bu snarl (292-bet).

Tur ajratish strategiyasini belgilaydi, shuning uchun hidni
toifalashning amaliy qiymati bor: [qo'lda ajratish
strategiyasi](38-refaktoringni-xavfsiz-bajarish.md#3814-qolda-ajratish-strategiyasi-skeletonize-methods-find-sequences-extract-to-the-current-class-first-be-prepared-to-redo-extractions)
bulleted metod uchun ketma-ketlikni topishni, snarled metod uchun
skeletonize ni tavsiya qiladi; testsiz bo'lish taktikalari esa
[testsiz monstr metodni qo'lda
bo'lish](38-refaktoringni-xavfsiz-bajarish.md#3813-testsiz-monstr-metodni-qolda-bolish-introduce-sensing-variable-extract-what-you-know-coupling-count-gleaning-dependencies)
bo'limida.

## 32.4 Global ma'lumot (Global Data)

**Belgisi**: `public static` o'zgaradigan maydon, singleton ichidagi
o'zgaradigan holat, process darajasidagi property larni kod bo'ylab
o'zgartirish.

**Manba**: hid 2-nashrda "Global Data" nomi bilan (74-bet); 1-nashrda
alohida hid sifatida yo'q.

**Nega muammo**: McConnell global ma'lumotning muammolarini sanab
beradi (*Code Complete*, 2-nashr, 13.3, 335-339 bet):

- bexosdan o'zgarish: global qiymat bir joyda o'zgartiriladi, boshqa
  joyda esa o'zgarmagan deb o'ylanadi; bu yon ta'sir (side effect);
- aliasing: bitta o'zgaruvchi global sifatida ham, parametr sifatida
  ham ishlatilganda ikki nom bilan ko'rinadi va natija kutilganidan
  boshqa chiqadi;
- ko'p threadli muhitda umumiy holat;
- qayta ishlatishning qiyinlashishi: global ma'lumot o'qiydigan yoki
  yozadigan sinfni boshqa dasturga shunchaki qo'yib bo'lmaydi;
- initsializatsiya tartibi: turli fayldagi global ma'lumotlarning
  initsializatsiya tartibi ba'zi tillarda aniqlanmagan;
- modullashtirishning zaiflashishi: bir rutinani yolg'iz o'ylab
  bo'lmaydi, u bilan birga shu global ma'lumotni ishlatadigan har bir
  rutinani ham o'ylash kerak.

**Tuzatish**: Encapsulate Variable (2-nashr, 132-bet; 1-nashrda Self
Encapsulate Field, 138-bet) - global ma'lumotni funksiya ortiga
yashirish. McConnell ham aynan shu yo'lni beradi: global ma'lumot
o'rniga access routine (13.3, 339-bet). Keyin uni bog'liqlik sifatida
uzatish (16.9).

## 32.5 O'zgaradigan ma'lumot (Mutable Data)

**Belgisi**: obyektning maydoni kod bo'ylab turli joylarda o'zgaradi;
setter lar ko'p; bir maydonni kim o'zgartirganini kuzatish qiyin.

**Manba**: hid 2-nashrda "Mutable Data" nomi bilan (75-bet); 1-nashrda
alohida hid sifatida yo'q.

**Nega muammo**: Bloch o'zgarmaslikning foydasini ikki jumlada beradi.
O'zgarmas obyekt aniq bitta holatda bo'ladi - yaratilgan holatida, va
konstruktorlar invariantni o'rnatsa, invariant abadiy saqlanadi;
o'zgaradigan obyektning holat fazosi esa istalgancha murakkab bo'lishi
mumkin va mutator metodlarning holat o'tishlari aniq hujjatlanmagan
bo'lsa, sinfni ishonchli ishlatish qiyin yoki imkonsiz. Ikkinchisi:
o'zgarmas obyekt tabiatan thread-safe va sinxronizatsiya talab qilmaydi
(*Effective Java*, 3-nashr, 17-band, 82-83 bet).

**Tuzatish**: Encapsulate Variable (132-bet), Split Variable (240-bet),
Remove Setting Method (331-bet), Replace Derived Variable with Query
(248-bet), Change Reference to Value (252-bet) - hammasi 2-nashr
katalogidan. Java dagi shakli
[16-bob](16-ozgarmaslik-va-holat-boshqaruvi-kod.md) va
[36-bobda](36-refaktoring-harakatlari-katalogi-ii-malumot.md).

## 32.6 Ma'lumot to'dasi (Data Clumps)

**Belgisi**: bir xil uch-to'rt ma'lumot elementi ko'p joyda birga
paydo bo'ladi - bir necha sinfdagi maydonlar, ko'p metod imzosidagi
parametrlar: `from` va `to`; `street`, `city`, `zip`; `amount` va
`currency` (1-nashr, 67-bet).

**Manba**: 1-nashr 67-bet, 2-nashr 78-bet; nom ikki nashrda bir xil.

**Nega muammo**: birga yuradigan ma'lumot to'dasi o'z obyektiga
aylanishi kerak. Aks holda maydon va parametr ro'yxatlari uzun qoladi
va chaqiruv murakkablashadi (1-nashr, 67-bet).

**Tuzatish**: birinchi qadam - to'da maydon sifatida qaerda
ko'rinayotganini topish va maydonlar ustida Extract Class qo'llash;
keyin imzolar uchun Introduce Parameter Object yoki Preserve Whole
Object (1-nashr, 67-bet; 2-nashrda Extract Class 182-bet, Introduce
Parameter Object 140-bet, Preserve Whole Object 319-bet). Yangi
obyektning faqat bir qismini ishlatadigan to'dadan xavotir olmaslik
kerak: ikki yoki undan ko'p maydon almashtirilsa, foyda bor (1-nashr,
67-bet).

**Kitobdagi sinov**: ma'lumot qiymatlaridan birini o'chirib ko'rish;
qolganlari ma'noga egami? Egamas bo'lsa, tug'ilishni kutayotgan obyekt
bor (1-nashr, 67-bet).

## 32.7 Takrorlangan `switch` (Repeated Switches)

**Belgisi**: bir xil `switch` yoki `if/else` zanjiri kod bazasining bir
necha joyida takrorlanadi (6.10).

**Manba**: 2-nashrda "Repeated Switches" (79-bet); 1-nashrda "Switch
Statements" (68-bet).

**Nega muammo**: 1-nashr sababni bitta so'z bilan beradi - takrorlanish.
Bir xil switch dastur bo'ylab turli joylarda uchraydi va yangi shox
qo'shilsa, barcha switch larni topib o'zgartirish kerak (68-bet).
Martin ham takrorlangan shart zanjirini duplication ning nozikroq
shakli deb sanaydi va polimorfizmga almashtirishni aytadi (*Clean
Code*, G5, 290-bet).

**Tuzatish**: 1-nashr tartibi - switch ni Extract Method bilan
ajratish, Move Method bilan polimorfizm kerak bo'lgan sinfga ko'chirish,
so'ng Replace Type Code with Subclasses yoki Replace Type Code with
State/Strategy, va nihoyat Replace Conditional with Polymorphism
(68-bet). Agar bir necha holat faqat bitta metodga ta'sir qilsa va
ularning o'zgarishi kutilmasa, polimorfizm ortiqcha: bunda Replace
Parameter with Explicit Methods (68-bet). 2-nashrdagi nomlar: Replace
Conditional with Polymorphism (272-bet), Replace Type Code with
Subclasses (362-bet). Java da xatti-harakatni enum ichiga ko'chirish
yoki `sealed` ierarxiya va pattern matching (25.3) shu harakatning
tilga xos shakli.

**Arzon mezon**: `switch` kimning ma'lumoti ustida ekanini so'rash.
1-nashr qoidani shunday beradi - `switch` o'z ma'lumotingiz ustida
bo'lishi kerak, boshqa obyektning atributi bo'yicha `switch`
qilinmaydi (35-bet). Bu takrorlanishdan mustaqil, ya'ni bitta joyda
turgan `switch` ham shu mezon bo'yicha hid bo'lishi mumkin: shox
tanlovi boshqa sinfning holatiga qarab qilinsa, mantiq ham o'sha
sinfda turishi kerak. Shuning uchun bu Feature Envy ning `switch`
shakli (33.18).

## 32.8 Sikllar (Loops)

**Belgisi**: filtrlash, mapping va yig'ish qo'lda sikl bilan yozilgan.

**Manba**: hid faqat 2-nashrda, "Loops" nomi bilan (79-bet); 1-nashrda
alohida hid sifatida yo'q. 2-nashr matni bu korpusda mavjud emas,
shuning uchun bu yerda faqat nom, bet va tavsiya etilgan harakat
keltiriladi; hidning sababi kitobdan iqtibos qilinmaydi.

**Tuzatish**: Replace Loop with Pipeline (2-nashr, 231-bet) va Split
Loop (2-nashr, 227-bet). 1-nashr siklni ajratishning oddiy shaklini
Long Method yozuvida beradi: siklni va sikl ichidagi kodni o'z
metodiga chiqarish (64-65 bet).

Qachon sikl qoladi: 7.7 dagi mezon (erta chiqish, yon ta'sir, istisno).
Bu mezon shu korpusning amaliy tavsiyasi, kitobdan olingan emas.

## 32.9 Dangasa element (Lazy Element)

**Belgisi**: o'zini oqlamaydigan element - refaktoringdan keyin
kichrayib qolgan sinf, faqat bazani chaqiradigan voris sinf, bitta
qatordan iborat va nomi tanasi bilan bir xil ma'noda bo'lgan funksiya.

**Manba**: 2-nashrda "Lazy Element" (80-bet); 1-nashrda "Lazy Class"
(68-bet).

**Nega muammo**: 1-nashr narxni ochiq aytadi - yaratilgan har bir sinf
saqlash va tushunish uchun pul turadi, o'zini oqlamaydigan sinf esa
olib tashlanadi. Bu ko'pincha bir vaqtlar o'zini oqlagan, lekin
refaktoringdan keyin kichrayib qolgan sinf, yoki rejalashtirilgan,
ammo amalga oshmagan o'zgarish uchun qo'shilgan sinf bo'ladi (68-bet).

**Tuzatish**: voris sinflar o'zini oqlamasa Collapse Hierarchy, deyarli
foydasiz komponent uchun Inline Class (1-nashr, 68-bet; 2-nashrda
Collapse Hierarchy 380-bet, Inline Class 186-bet, Inline Function
115-bet).

**Qardosh hid**: "kelgusi o'zgarish uchun" qo'yilgan va hozir
ishlatilmaydigan abstraksiya hid bo'lmay qolmaydi. Fowler va Beck uni
alohida hid sifatida sanaydi - Speculative Generality (1-nashr, 68-bet;
2-nashr, 80-bet): kimdir "balki bir kun shunday qilish kerak bo'ladi"
deb hamma hook va maxsus holatni qo'yadi, natija esa tushunish va
saqlash uchun qiyinroq bo'ladi. Agar mashina ishlatilsa, u arzigulik;
ishlatilmasa, faqat yo'lni to'sadi. Yechimlar: ish qilmaydigan abstrakt
sinflar uchun Collapse Hierarchy, keraksiz delegatsiya uchun Inline
Class, ishlatilmaydigan parametr uchun Remove Parameter, g'alati
abstrakt nom uchun Rename Method (1-nashr, 68-bet). Bitta aniq belgi
ham bor: metod yoki sinfning yagona foydalanuvchisi test bo'lsa, uni va
shu testni o'chirish kerak (68-bet).

## 32.10 Vaqtinchalik maydon (Temporary Field)

[Vaqtinchalik maydon va uni yo'qotish](16-ozgarmaslik-va-holat-boshqaruvi-kod.md#168-vaqtinchalik-maydon-va-uni-yoqotish)
bo'limida ko'rilgan.

**Manba**: 1-nashr 69-bet, 2-nashr 80-bet; nom ikki nashrda bir xil.

**Belgisi**: instans o'zgaruvchisi faqat ba'zi holatlarda to'ldiriladi.
Bunday kodni tushunish qiyin, chunki o'quvchi obyekt o'z
o'zgaruvchilarining hammasiga muhtoj deb kutadi; o'zgaruvchi nega
turganini tushunishga urinish o'quvchini holdan toydiradi (1-nashr,
69-bet).

**Tuzatish**: Extract Class bilan yetim o'zgaruvchilarga uy yasash va
ular bilan ishlaydigan kodni shu komponentga ko'chirish; o'zgaruvchilar
yaroqsiz bo'lgan holat uchun Introduce Null Object bilan alternativ
komponent (1-nashr, 69-bet; 2-nashrda Extract Class 182-bet, Introduce
Special Case 289-bet).

**Tez-tez uchraydigan alohida holat**: murakkab algoritm bir necha
o'zgaruvchi talab qilgani va uzun parametr ro'yxatini uzatish
istalmagani uchun ular maydonga chiqarilgan. Maydonlar faqat algoritm
ishlagan vaqtda yaroqli, boshqa kontekstda esa chalg'ituvchi. Yechim:
shu o'zgaruvchilar va ularni talab qiladigan metodlar ustida Extract
Class; natija method object bo'ladi (1-nashr, 69-bet).

## 32.11 Uzun xabar zanjiri (Message Chains)

**Belgisi**: mijoz bir obyektdan ikkinchisini so'raydi, undan
uchinchisini, va shu davom etadi: `a.b().c().d().e()`. Kodda bu
`getThis` turidagi metodlarning uzun qatori yoki temp lar
ketma-ketligi bo'lib ko'rinadi (1-nashr, 69-bet; 14.4).

**Manba**: 1-nashr 69-bet, 2-nashr 81-bet.

**Nega muammo**: bunday navigatsiya mijozni navigatsiya tuzilishiga
bog'laydi; oraliq munosabatlardagi har qanday o'zgarish mijozni
o'zgartirishga majbur qiladi (1-nashr, 69-bet). Martin buni alohida
evristika qilib qo'yadi: Avoid Transitive Navigation (*Clean Code*,
G36, 306-bet).

**Tuzatish**: Hide Delegate (1-nashr, 127-bet; 2-nashr, 189-bet).
Fowler darhol ogohlantiradi: printsipial jihatdan buni zanjirning har
bir obyektida qilish mumkin, lekin bu ko'pincha har bir oraliq obyektni
middle man ga aylantiradi (1-nashr, 69-bet) - ya'ni 32.12 ni yaratadi.
Ko'pincha yaxshisi natija nimaga ishlatilayotganini ko'rib, Extract
Method bilan shu kodni ajratish va Move Method bilan zanjir bo'ylab
pastga surish; zanjirdagi obyektning bir necha mijozi qolgan yo'lni
o'zi bosib o'tmoqchi bo'lsa, shuni qiladigan metod qo'shiladi (1-nashr,
69-bet; 2-nashrda Extract Function 106-bet, Move Function 198-bet).

**Chegara**: Fowler va Beck bu yerda mo'tadillikni ta'kidlaydi - ba'zilar
har qanday metod zanjirini dahshat deb biladi, mualliflar esa o'zlarining
bosiq va o'lchangan mo'tadilligi bilan tanilganini aytadi (1-nashr,
69-bet). Shuning uchun bu bobda zanjir uzunligi uchun raqamli chegara
yo'q.

## 32.12 Vositachi (Middle Man)

**Belgisi**: sinfning interfeysiga qarasangiz, metodlarining yarmi
boshqa sinfga delegatsiya qilayotgani ko'rinadi (1-nashr, 69-70 bet).

**Manba**: 1-nashr 69-70 bet, 2-nashr 81-bet.

**Nega muammo**: inkapsulyatsiya - ichki tafsilotni tashqi dunyodan
yashirish, va u ko'pincha delegatsiya bilan keladi; bu o'zi yaxshi.
Lekin delegatsiya haddan oshib ketishi mumkin va shunda sinf
hech narsa qilmay, faqat uzatuvchiga aylanadi (1-nashr, 69-70 bet).
Bu 32.11 ning teskari tomoni.

**Tuzatish**: Remove Middle Man - haqiqatni biladigan obyekt bilan
to'g'ridan-to'g'ri gaplashish (1-nashr, 130-bet; 2-nashr, 192-bet).
Faqat bir necha metod ish qilmasa, ularni chaqiruvchiga Inline Method
bilan kiritish; qo'shimcha xatti-harakat bo'lsa, 1-nashr vositachini
haqiqiy obyektning voris sinfiga aylantirish variantini ham beradi
(69-70 bet).

Korpusning amaliy tavsiyasi (kitobdan olingan emas): fasad va adapter
atayin vositachi bo'ladi, chunki ular chegara vazifasini bajaradi;
Fowler va Martin bu istisnoni yozmaydi.

## 32.13 Izohlar hid sifatida (Comments)

[9-bobda](09-yomon-izohlar-katalogi.md) izohlarning katalogi berilgan.

**Manba**: 1-nashr 71-72 bet, 2-nashr 84-bet.

Fowler va Beck ochiq aytadi: izoh o'zi yomon hid emas, aksincha yoqimli
hid. Muammo izohning deodorant sifatida ishlatilishida: qalin
izohlangan kodga qarab, izohlar kod yomon bo'lgani uchun turganini
ko'rish hayratlanarli darajada tez-tez uchraydi. Izohlar bobning qolgan
hidlariga olib boradi; birinchi harakat refaktoring bilan hidni
yo'qotish, shundan keyin izohlar ko'pincha ortiqcha bo'lib qoladi
(1-nashr, 71-bet).

Kitobdagi tip ham shunday: izoh yozish ehtiyoji paydo bo'lganda, avval
kodni shunday refaktoring qilish kerakki, har qanday izoh ortiqcha
bo'lib qolsin (1-nashr, 71-bet).

**Tuzatish**: blok nima qilayotganini tushuntirish uchun izoh kerak
bo'lsa Extract Method; metod allaqachon ajratilgan, lekin nima
qilayotganini tushuntirish uchun yana izoh kerak bo'lsa Rename Method;
tizimning talab qilingan holati haqida qoida aytish kerak bo'lsa
Introduce Assertion (1-nashr, 71-bet; 2-nashrda Extract Function
106-bet, Change Function Declaration 124-bet, Introduce Assertion
302-bet).

**Izoh haqli bo'lgan joy**: nima qilishni bilmagan paytda. Izoh nima
bo'layotganini tasvirlashdan tashqari o'zingiz ishonmagan joyni
ko'rsatishi mumkin, va nega shunday qilganini aytish uchun yaxshi joy;
bu kelgusi o'zgartiruvchiga yordam beradi (1-nashr, 71-72 bet).
Izohning xato shakllari Martin da alohida kodlangan: C1-C5 (*Clean
Code*, 286-287 bet), ularning ro'yxati
[34-bobda](34-toza-kod-evristikalarining-toliq-royxati.md).

## 32.14 Uzun parametrlar ro'yxati (Long Parameter List)

**Manba**: 1-nashr 65-66 bet, 2-nashr 74-bet; nom ikki nashrda bir xil.

**Belgisi**: metod imzosi uzun parametr ro'yxatini oladi va yangi
ma'lumot kerak bo'lgan har safar ro'yxat yana o'sadi.

**Nega muammo**: 1-nashr sababni uchga ajratadi - uzun parametr
ro'yxatini tushunish qiyin, u izchilsiz va ishlatishga noqulay bo'lib
qoladi, va yangi ma'lumot kerak bo'lgani uchun uni doimo o'zgartirish
kerak bo'ladi (65-bet). Kitob tarixiy sababni ham aytadi: ilk
dasturlashda rutinaga kerak bo'lgan hamma narsani parametr sifatida
uzatish o'rgatilgan, chunki muqobili global ma'lumot edi. Obyektlar bu
holatni o'zgartiradi - kerakli narsa qo'lda bo'lmasa, uni boshqa
obyektdan so'rab olish mumkin, shuning uchun metodga kerak bo'lgan
hamma narsa emas, kerakligiga yetib olishi uchun yetarlisi uzatiladi
(65-bet).

**Tuzatish** (1-nashr, 65-66 bet): allaqachon ma'lum bo'lgan obyektdan
so'rab olinadigan parametr uchun Replace Parameter with Method; bitta
obyektdan yig'ilgan ma'lumot to'dasi uchun Preserve Whole Object;
mantiqiy obyekti yo'q bir necha element uchun Introduce Parameter
Object. 2-nashrdagi nomlar: Replace Parameter with Query (324-bet),
Preserve Whole Object (319-bet), Introduce Parameter Object (140-bet);
harakatlarning mexanikasi 37.11, 37.10 va 35.8 da.

**Kitobdagi istisno** (1-nashr, 66-bet): chaqirilayotgan obyektdan
kattaroq obyektga bog'liqlik ataylab yaratilmasa, ma'lumotni yechib
parametr sifatida uzatish o'rinli. Kitob shu yerda narxini eslatadi:
ro'yxat juda uzun bo'lsa yoki juda tez o'zgarsa, bog'liqlik tuzilmasini
qaytadan o'ylash kerak.

Java va Spring darajasidagi shakli: argument soni chegarasi va builder
tanlovi 5.1 da, Spring kontekstidagi ko'rinishi [patternlar hujjatining
uzun parametrlar ro'yxati
yozuvida](../patterns/25-anti-patternlar.md#2522-uzun-parametrlar-royxati-long-parameter-list).

## 32.15 Primitivlarga berilish (Primitive Obsession)

**Manba**: 1-nashr 67-68 bet, 2-nashr 78-bet; nom ikki nashrda bir xil.

**Belgisi**: pul sonsiz valyuta bilan, telefon raqami va pochta indeksi
oddiy `String` bilan, oraliq ikkita alohida `int` bilan ifodalanadi; tur
kodi `int` yoki `String` da saqlanadi.

**Nega muammo**: 1-nashr boshlanish nuqtasini aytadi - har bir muhitda
ikki xil ma'lumot bor: yozuv turlari ma'lumotni ma'noli guruhga tuzadi,
primitiv turlar esa quruvchi bloklar. Yozuv turlari ma'lum narx bilan
keladi (bazadagi jadval, bitta-ikkita narsa uchun yaratish noqulay),
shuning uchun obyektlarga yangi kelgan odam kichik ish uchun kichik
obyekt ishlatishdan tortinadi (67-bet). Obyektlarning qimmatli
xususiyati esa aynan shu: ular primitiv bilan kattaroq sinflar
orasidagi chiziqni xiralashtiradi yoki butunlay buzadi - tilning ichki
turlaridan farq qilmaydigan kichik sinf yozish oson. Fowler Java ning
o'zini misol qiladi: Java da son uchun primitivlar bor, lekin ko'p
muhitda primitiv bo'lgan satr va sana Java da sinf (67-bet).

**Tuzatish** (1-nashr, 67-68 bet): alohida ma'lumot qiymati uchun
Replace Data Value with Object; qiymat tur kodi bo'lsa va xatti-harakatga
ta'sir qilmasa Replace Type Code with Class, tur kodiga bog'liq shartlar
bo'lsa Replace Type Code with Subclasses yoki Replace Type Code with
State/Strategy; birga yurishi kerak bo'lgan maydon guruhi uchun Extract
Class; parametr ro'yxatidagi primitivlar uchun Introduce Parameter
Object; massivni bo'lib-bo'lib o'qiyotgan bo'lsangiz Replace Array with
Object. 2-nashrdagi nomlar: Replace Primitive with Object (174-bet),
Replace Type Code with Subclasses (362-bet), Extract Class (182-bet),
Introduce Parameter Object (140-bet); mexanikasi 36.8, 37.13, 36.1 va
35.8 da.

Java va Spring darajasidagi shakli: pul uchun 20.1, [satr bilan tiplash
o'rniga tur](21-satr-matn-va-regex.md#218-satr-bilan-tiplash-orniga-tur),
va [patternlar hujjatidagi primitivlarga berilish
anti-patterni](../patterns/25-anti-patternlar.md#2519-primitivlarga-berilish-primitive-obsession).
Diffda shu hidni ko'rish usuli [code review hujjatida](../code-review/08-clean-code-review-nomlash-kognitiv-yuk.md#85-primitive-obsession-domen-tilini-turga-aylantirish).

## 32.16 Bu hid emas: qachon tegmaslik kerak

Hid ro'yxati nomzod beradi, hukm bermaydi. Buni mualliflar o'zi aytadi:
3-bobda refaktoring qachon kechikkani uchun aniq mezon berish maqsad
qilinmagan, ro'yxat faqat refaktoring yecha oladigan muammo borligiga
ishora qiladi, va aynan o'zingiz sezgan hid ro'yxatda bo'lmasligi ham
mumkin (1-nashr, 63-bet).

| Holat | Nega tegmaslik | Manba |
|---|---|---|
| Kod asosan ishlamaydi | Fowler noldan yozishni tavsiya qiladi: kod shunchalik buzuq bo'lsa, uni testlab barqarorlashtirib ham bo'lmasa, refaktoring emas, qaytadan yozish kerak; refaktoringdan oldin kod asosan to'g'ri ishlashi shart | Fowler 1-nashr, 55-bet |
| Muddat yaqin | refaktoringdan keladigan unum muddatdan keyin paydo bo'ladi, ya'ni kech bo'ladi. Ward Cunningham ning shakli: tugallanmagan refaktoring qarzga kirish; qarz foizi bilan keladi va u boshqarilishi kerak | Fowler 1-nashr, 56-bet |
| Testlar yo'q | refaktoringning muhim sharti mustahkam testlar; refaktoringni avtomatlashtiradigan asbob bo'lsa ham testlar kerak | Fowler 1-nashr, 73-bet |
| Hid zaif | Refused Bequest misolida: o'n holatning to'qqiztasida bu hid tozalashga arzigulik darajada kuchli emas | Fowler 1-nashr, 71-bet |
| Zanjirni butunlay yashirish | Hide Delegate ni zanjirning har bir obyektida qo'llash har bir oraliq obyektni vositachiga aylantiradi | Fowler 1-nashr, 69-bet |

Bunga korpusning ikki qo'shimchasi bor va ikkisi ham kitobdan olingan
emas: chegara kodida (adapter, DTO) ataylab qoldirilgan hid (32.12,
14.5), va boshqa sabab bilan o'zgaradigan o'xshash kodni birlashtirmaslik
(32.2).

## 32.17 Amalda qo'llash

- [ ] Eng ko'p o'zgaradigan 10 faylni olib, shu bobdagi hidlar bo'yicha ro'yxat tuzing va har biriga refaktoring harakatini belgilang.
- [ ] Takrorlangan kod joylarini 32.2 jadvalidagi turlarga ajratib, har biriga shu turning yechimini qo'llang.
- [ ] Bir xil parametr guruhlarini (data clumps) grep bilan topib, 32.6 dagi kitob sinovini o'tkazing: bitta qiymatni o'chirsa, qolganlari ma'noga egami?
- [ ] Takrorlangan `switch` zanjirlarini sanab, xatti-harakatni enum yoki `sealed` ierarxiyaga ko'chiring.
- [ ] `public static` o'zgaradigan maydonlarni topib, access routine ortiga yashiring, keyin bog'liqlikka aylantiring.
- [ ] Chaqiruv zanjirlarini ko'rib, Hide Delegate va Extract Function + Move Function orasidan tanlang; Hide Delegate ni zanjirning har bir obyektida qo'llamang.
- [ ] Metodlarining yarmi delegatsiya qiladigan sinflarni ro'yxatlab, Remove Middle Man ni ko'rib chiqing; chegara sinflarini alohida belgilang.
- [ ] Izohlar eng ko'p to'plangan uch faylni tanlab, har bir izohga bitta savol bering: shu izohni ortiqcha qiladigan refaktoring bormi?
- [ ] Funksiya uzunligi uchun jamoada chegara qo'yishdan oldin 32.3 dagi tadqiqot jadvalini o'qing: qaror chegarada emas, cohesion va nesting da.

## Manbalar

- Martin Fowler va Kent Beck, *Refactoring: Improving the Design of
  Existing Code*, 1-nashr, Addison-Wesley, 1999, 3-bob "Bad Smells in
  Code" (63-72 bet) - 22 hidning nomi, ta'rifi va mexanikasi:
  Duplicated Code (63), Long Method (64), Data Clumps (67), Switch
  Statements (68), Lazy Class va Speculative Generality (68), Temporary
  Field, Message Chains, Middle Man (69), Comments (71); hamda
  ro'yxatning aniq mezon bermasligi (63)
- Martin Fowler, *Refactoring*, 1-nashr, Addison-Wesley, 1999, 2-bob
  "Principles in Refactoring" (55-56 bet) - "When Shouldn't You
  Refactor?": noldan yozish holati va muddat yaqinligi
- Martin Fowler, *Refactoring*, 1-nashr, Addison-Wesley, 1999, 4-bob
  "Building Tests" (73-bet) - mustahkam testlar refaktoringning muhim
  sharti
- Martin Fowler, *Refactoring*, 1-nashr, Addison-Wesley, 1999, 1-bob
  (35-bet) - `switch` o'z ma'lumoti ustida bo'lishi kerakligi va boshqa
  obyektning atributi bo'yicha `switch` qilinmasligi
- Martin Fowler, *Refactoring*, 1-nashr, Addison-Wesley, 1999, 6-11
  boblar (89-292 bet) - 32.2-32.13 da keltirilgan harakatlarning
  1-nashrdagi nomlari va betlari: Inline Method (95), Hide Delegate
  (127), Remove Middle Man (130), Self Encapsulate Field (138),
  Introduce Null Object (209), Rename Method (221), Replace Parameter
  with Explicit Methods (230), Preserve Whole Object (232), Introduce
  Parameter Object (238)
- Martin Fowler, *Refactoring*, 2-nashr, Pearson Addison-Wesley, 2019,
  mundarija - 3-bobdagi 24 hidning nomi va beti (71-84): Mysterious Name
  (72), Duplicated Code (72), Long Function (73), Global Data (74),
  Mutable Data (75), Data Clumps (78), Repeated Switches (79), Loops
  (79), Lazy Element (80), Speculative Generality (80), Temporary Field
  (80), Message Chains (81), Middle Man (81), Comments (84)
- Martin Fowler, *Refactoring*, 2-nashr, Pearson Addison-Wesley, 2019,
  mundarija, 6-12 boblar - harakatlarning 2-nashrdagi nomlari va
  betlari: Extract Function (106), Inline Function (115), Change
  Function Declaration (124), Encapsulate Variable (132), Rename
  Variable (137), Introduce Parameter Object (140), Split Phase (154),
  Replace Temp with Query (178), Extract Class (182), Inline Class
  (186), Hide Delegate (189), Remove Middle Man (192), Move Function
  (198), Split Loop (227), Replace Loop with Pipeline (231), Split
  Variable (240), Rename Field (244), Replace Derived Variable with
  Query (248), Change Reference to Value (252), Decompose Conditional
  (260), Replace Conditional with Polymorphism (272), Introduce Special
  Case (289), Introduce Assertion (302), Preserve Whole Object (319),
  Remove Setting Method (331), Pull Up Method (350), Replace Type Code
  with Subclasses (362), Collapse Hierarchy (380)
- Robert C. Martin, *Clean Code*, Prentice Hall, 2008, 17-bob "Smells
  and Heuristics" (285-308 bet) - G5 Duplication (289-290 bet) va
  takrorlanishning to'rt shakli, G36 Avoid Transitive Navigation
  (306-bet), C1-C5 izoh hidlari (286-287 bet)
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 7.4
  "How Long Can a Routine Be?" (173-174 bet) - rutina uzunligi bo'yicha
  oltita empirik tadqiqot va 100-200 qatorlik tavsiya; 200 dan yuqori
  o'lchamlar tadqiqotlarda ajratilmagani
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004,
  11.1 "Considerations in Choosing Good Names" (259-263 bet) - nom
  muammoni ifodalashi kerakligi va nom uzunligi bo'yicha Gorla,
  Benander va Benander (1990) o'lchovi (262-bet)
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004,
  13.3 "Global Data" (335-341 bet) - global ma'lumotning oltita
  muammosi va global ma'lumot o'rniga access routine yechimi (339-bet)
- Joshua Bloch, *Effective Java*, 3-nashr, Addison-Wesley, 2018,
  17-band "Minimize mutability" (80-83 bet) - o'zgarmas obyekt aniq
  bitta holatda bo'ladi va tabiatan thread-safe
- ESLATMA: 32.2 oxiridagi "boshqa sabab bilan o'zgaradigan o'xshash
  kodni birlashtirmaslik" qoidasi shu korpusning amaliy tavsiyasi,
  kitobdan olingan emas
- ESLATMA: 32.8 dagi siklni qoldirish mezoni (erta chiqish, yon ta'sir,
  istisno) shu korpusning amaliy tavsiyasi, kitobdan olingan emas
- ESLATMA: 32.12 dagi "fasad va adapter atayin vositachi" istisnosi va
  32.16 dagi chegara kodi qatori shu korpusning amaliy tavsiyasi,
  kitobdan olingan emas
- ESLATMA: 32.17 dagi tekshiruv ro'yxati shu korpusning amaliy
  tavsiyasi, kitobdan olingan emas
- Martin Fowler va Kent Beck, *Refactoring: Improving the Design of
  Existing Code*, 1-nashr, Addison-Wesley, 1999, 3-bob "Bad Smells in
  Code" (65-68 bet) - 32.14 va 32.15 ning ta'rifi, sababi va tavsiya
  qilingan harakatlari: Long Parameter List (65-66, uzun ro'yxatning
  uchta sababi va bog'liqlik istisnosi), Primitive Obsession (67-68,
  yozuv turi bilan primitiv orasidagi chiziq va tur kodi uchun uch
  variant)
- Martin Fowler, *Refactoring*, 2-nashr, Pearson Addison-Wesley, 2019,
  mundarija (71-84 bet) va "List of Refactorings" - 32.14 va 32.15
  dagi 2-nashr nomlari va betlari: Long Parameter List (74), Primitive
  Obsession (78), Replace Parameter with Query (324), Preserve Whole
  Object (319), Introduce Parameter Object (140), Replace Primitive with
  Object (174), Replace Type Code with Subclasses (362), Extract Class
  (182)
- Michael Feathers, *Working Effectively with Legacy Code*, Prentice Hall PTR,
  2004 (copyright 2005), 22-bob (290-293) - 32.3 dagi uzun funksiyaning ikki
  turi (bulleted va snarled method) va snarl ni aniqlash tekshiruvi

---

[&larr; 31. TDD intizomi va kod dizayniga ta'siri](31-tdd-intizomi-va-kod-dizayniga-tasiri.md) · [Mundarija](README.md) · [33. Kod hidlari katalogi II: sinf, ierarxiya, bog'liqlik &rarr;](33-kod-hidlari-katalogi-ii-sinf-ierarxiya.md)
