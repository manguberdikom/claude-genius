<!-- doc: code-review | chapter: 41 | part: IX. Jarayon, madaniyat va o'lchov -->

[Barcha hujjatlar](../../README.md) / [Kod review](README.md)

> Holat: tekshirilmoqda. Da'volar hali manbaga solishtirilmoqda.

# 41. Review madaniyati, til va kelishmovchilik (Culture, Language, Disagreement)

<details>
<summary>Bu bobdagi 14 bo'lim</summary>

- [41.1 Izoh tili: kodga qarash, odamga emas](#411-izoh-tili-kodga-qarash-odamga-emas)
- [41.2 Savol shaklida izoh](#412-savol-shaklida-izoh)
- [41.3 Izoh darajasini ajratish](#413-izoh-darajasini-ajratish)
- [41.4 Junior va senior bilan review](#414-junior-va-senior-bilan-review)
- [41.5 Kelishmovchilikni hal qilish](#415-kelishmovchilikni-hal-qilish)
- [41.6 Review izohining narxi](#416-review-izohining-narxi)
- [41.7 Masofaviy va asinxron review](#417-masofaviy-va-asinxron-review)
- [41.8 Review ni o'rgatish](#418-review-ni-orgatish)
- [41.9 Review madaniyatining buzilish belgilari](#419-review-madaniyatining-buzilish-belgilari)
- [41.10 Review natijasi baholashga ishlatilmaydi](#4110-review-natijasi-baholashga-ishlatilmaydi)
- [41.11 Uch ustun va review ni mavjud bo'lmagan jamoaga kiritish](#4111-uch-ustun-va-review-ni-mavjud-bolmagan-jamoaga-kiritish)
- [41.12 Izoh oqimi: bo'lak-bo'lak javob, TODO va PTAL](#4112-izoh-oqimi-bolak-bolak-javob-todo-va-ptal)
- [41.13 Ishni qaytarib olish va mansab bilan bosish](#4113-ishni-qaytarib-olish-va-mansab-bilan-bosish)
- [41.14 Amalda qo'llash](#4114-amalda-qollash)

</details>


Texnik jihatdan to'g'ri review ham zarar keltirishi mumkin, agar u odamni himoyaga o'tishga majbur qilsa. Natija: muallif izohlarni rad etadi, keyingi PR ni kichikroq va kech yuboradi, va review dan qo'rqadi. Bu bob review ni muloqot sifatida ko'radi - lekin yumshoqlik haqida emas, aniqlik haqida.

## 41.1 Izoh tili: kodga qarash, odamga emas

| Yomon shakl | Yaxshi shakl |
| --- | --- |
| "Sen nega bunday qilding?" | "Bu yerda X bo'lsa nima bo'ladi?" |
| "Bu noto'g'ri" | "Bu holatda Y oqibat chiqadi" |
| "Hamma biladi ki..." | "Bizning konvensiyamiz..." (havola bilan) |
| "Yana shu xato" | "Shu naqsh takrorlanyapti - qoidaga aylantirsakmi?" |
| "Men shunday yozmagan bo'lardim" | (sabab bo'lmasa - izoh yozmaslik) |
| "Buni tushunmadim" | "Bu metod nima qilishini nom bilan ko'rsatsak bo'ladimi?" |
| "Bu juda sodda" | "Bu yerda Z holati hisobga olinmagan" |

Asosiy mexanik qoida: izoh kod haqida bo'lsin, muallif haqida emas. "Sen" so'zi izohda deyarli har doim ortiqcha.

## 41.2 Savol shaklida izoh

Savol ikki narsani beradi: muallifga tushuntirish imkonini beradi (balki reviewer kontekstni bilmaydi) va aniqlashtiradi.

```text
# Buyruq: muallif rozi bo'lmasa, bahs boshlanadi.
"Bu yerda cache qo'shish kerak."

# Savol: kontekstni ochadi.
"Bu so'rov qanchalik tez-tez chaqiriladi? Agar har sahifa yuklanishida
bo'lsa, kesh qo'shish arziydi - lekin ma'lumot qanchalik tez eskiradi
degan savol bor. Siz qanday o'ylaysiz?"
```

Lekin savol shakli bilan haddan oshmaslik kerak. Agar aniq xato bo'lsa, savol shakli chalkashtiradi:

```text
# Yomon: aniq blocker savol shaklida - muallif uni ixtiyoriy deb o'ylaydi.
"Bu yerda unique constraint bo'lishi kerak emasmi?"

# Yaxshi: aniq va sababi bilan.
blocker: idempotentlik kaliti bo'yicha unique indeks yo'q. Ikki parallel
so'rov ikki to'lov yaratadi (15.2 naqshi). Migratsiyaga qo'shish kerak.
```

## 41.3 Izoh darajasini ajratish

4.9 da prefikslar berilgan. Ularning asosiy foydasi psixologik: muallif qaysi izohga qancha vaqt sarflashini biladi va `nit` larni rad etishi normal bo'ladi.

```text
blocker:  tuzatilmasa merge bo'lmaydi (xato, xavfsizlik, ma'lumot)
suggest:  yaxshilanish, muallif qaroriga qoldiriladi
question: javob kerak, tuzatish shart emas
nit:      did, majburiy emas (10 foizdan ko'p bo'lmasin)
praise:   to'g'ri qilingan qiyin joy
```

Google ning review izohi qo'llanmasi shu amaliyotni boshqa nomlar bilan beradi va sababini aniq aytadi: `Nit:` (mayda, texnik jihatdan qilish kerak, lekin katta ta'siri yo'q), `Optional:` yoki `Consider:` (yaxshi fikr deb o'ylayman, lekin qat'iy talab emas), `FYI:` (bu CL da kutmayman, kelgusi uchun o'ylab ko'rish foydali). Sababi psixologik emas, aniq: **belgi bo'lmasa, muallif hamma izohni majburiy deb o'qiydi**, hatto ular faqat ma'lumot yoki ixtiyoriy taklif bo'lsa ham. Ya'ni prefiks reviewer ning niyatini oshkor qiladi va muallifga tartiblashga imkon beradi.

Yana bir yo'nalish ham shu hujjatda bor va u korpusdagi `praise` ni oqlaydi: odamlar nimani yaxshi qilganining tasdiqlanishidan ham o'rganadi, faqat nimani yaxshilash kerakligidan emas. CL da yoqqan narsa bo'lsa, u haqda ham yozish kerak, va nega yoqqanini aytish bilan.

Qo'shimcha qoida: `blocker` lar soni cheklangan bo'lishi kerak. Agar PR da 15 blocker bo'lsa, bu alohida muammo - PR dizayn darajasida noto'g'ri yoki muallif kontekstni bilmaydi. Shu holatda 15 izoh yozish o'rniga suhbatlashish kerak.

## 41.4 Junior va senior bilan review

| Muallif | Diqqat | Tuzoq |
| --- | --- | --- |
| Junior | Nega shunday - o'rganish imkoniyati | Haddan ortiq izoh, ruhiy bosim |
| O'rta daraja | Mustaqil qaror va chegaralar | Yetarli diqqat berilmasligi |
| Senior | Dizayn qarori va alternativalar | Yuzaki review (obro'ga ishonish) |
| Boshqa jamoa | Kontekst va konvensiyalar | Yashirin bilim talab qilish |
| Yangi kelgan | Konvensiyalarni ko'rsatish | "Bizda shunday" tushuntirishsiz |

```text
# Junior PR ida: 20 izoh yozish o'rniga eng muhim 5 tasini tanlash.
# Qolganlari keyingi PR larda ko'riladi yoki juftlikda ishlash orqali.

# Aniq va o'rgatuvchi izoh shakli:
blocker: bu yerda tranzaksiya ichida SMS yuborilyapti.

Nega muhim: DB ulanishi SMS provayderining javobini kutib turadi.
Bizda pool 20 ta ulanish - ya'ni 20 parallel buyurtma butun ilovani
to'xtatadi. Bundan tashqari SMS o'tib, keyin commit yiqilsa, mijoz
tasdiq oladi, lekin buyurtma yo'q bo'ladi.

Yechim: SMS ni outbox ga yozish (shunga o'xshash misol
OrderCancellationService da bor, 45-satr).

Bu naqsh haqida: REVIEW.md -> "tranzaksiya ichida tashqi chaqiruv".
```

## 41.5 Kelishmovchilikni hal qilish

Kelishmovchilik normal va foydali - muhimi uning oxiri bo'lishi. Jamoada tartib yozilmasa, bahs PR da uch kun davom etadi.

Birlamchi manbada tartibdan oldin turadigan ikki savol bor. Birinchisi: **kim haq**. Muallif e'tiroz qilganda, reviewer avval uning haq bo'lishi mumkinligini o'ylab ko'rishi kerak, chunki muallif koddan yaqinroq turadi va ko'p narsani yaxshiroq ko'radi. Argumenti mantiqli bo'lsa va kod salomatligi nuqtai nazaridan ham to'g'ri bo'lsa, buni aytib masalani yopish kerak. Muallif haq bo'lmasa, reviewer o'z taklifini qaytadan tushuntiradi, va yaxshi tushuntirish ikki narsani ko'rsatadi: muallifning javobini tushunganini va o'zgarish nega so'ralayotgani haqida qo'shimcha ma'lumotni. Bir necha davra ketishi normal; muhimi odob saqlanishi va muallifga "eshitdim, lekin rozi emasman" degan signal yetib borishi.

Ikkinchisi, va bu amalda ko'p buziladi: **"keyin tozalayman"**. Muallif yana bir davra review ni xohlamay, tozalashni keyingi PR ga qoldirishni va shuni hozir LGTM qilishni so'raydi. Hujjatning kuzatuvi qattiq: tajriba shuni ko'rsatadi: tozalash darhol, shu PR dan keyin qilinmasa, u hech qachon qilinmaydi. Bu mas'uliyatsizlik emas, ish bosimi: tozalash boshqa vazifalar orasida yo'qoladi. Shuning uchun to'g'ri yo'l tozalashni **hozir**, kod kodbazaga kirib "tugagan" bo'lishidan oldin talab qilish. CL yangi murakkablik kiritgan bo'lsa, u merge dan oldin tozalanishi shart (favqulodda holat bundan mustasno); CL atrofdagi eski muammoni ochib bergan va u hozir tuzatilmasa, bug yozib qoldiriladi.

Oxirgi, reviewer ning o'zi bilan bog'liq nuqta: reviewer ko'pincha "talab qilsam muallif xafa bo'ladi" deb o'ylaydi. Hujjat buni rad etadi: xafalik odatda izohning **qanday yozilganidan** keladi, sifat talabining o'zidan emas. Izoh odobli bo'lsa, muallif ko'pincha umuman xafa bo'lmaydi va keyinroq kod yaxshilanganiga minnatdor bo'ladi.

```markdown
<!-- REVIEW.md ichida: kelishmovchilik tartibi -->
## Kelishmovchilik

1. **Dalil almashish.** Ikki tomon o'z pozitsiyasini oqibat tilida yozadi
   (did emas, raqam yoki ssenariy).
2. **Ikki davra.** Izoh almashinuvi ikki davradan oshsa, PR da yozishni
   to'xtatib, 15 daqiqalik suhbat o'tkaziladi. Yozma bahs tezda qimmatlashadi.
3. **Qaytarilish narxi.** Qaror arzon qaytarilsa (ichki kod) - muallif
   qaroriga qoldiriladi. Qimmat qaytarilsa (API, sxema, ma'lumot) -
   uchinchi odam yoki tech lead qaror qiladi.
4. **Yozib qoldirish.** Qaror ADR yoki PR izohida qoladi, shunda keyin
   bahs takrorlanmaydi.
5. **"Rozi emasman, lekin bajaraman".** Qaror qabul qilingach, ikki tomon
   uni qo'llab-quvvatlaydi. Pozitsiya ADR da qayd qilinadi.
```

Alohida holat: reviewer va muallif tajriba darajasi juda farq qilsa, kelishmovchilik teng bo'lmaydi. Bunday holatda qoida foydali: "junior reviewer senior muallifga blocker qo'yishi normal, va senior javob yozishi majburiy".

## 41.6 Review izohining narxi

Har bir izoh muallif vaqtini oladi: o'qish, tushunish, tuzatish yoki javob yozish. Shu sababli izoh yozishdan oldin savol: bu izoh o'z narxini qoplaydimi.

| Izoh | Muallif vaqti | Foyda |
| --- | --- | --- |
| Aniq xato | 10-30 daqiqa | Prodda ancha qimmat (2.1) |
| Xavfsizlik | 30-60 daqiqa | Juda yuqori |
| Dizayn | Soatlar | Uzoq muddatli |
| Nomlash (noto'g'ri nom) | 2 daqiqa | Har o'qishda |
| Nomlash (did) | 2 daqiqa + bahs | Deyarli nol |
| Formatlash | 5 daqiqa | Nol (instrument ishi) |
| Shaxsiy uslub | Bahs | Manfiy |

Oxirgi uch qator review ning eng ko'p isrof qiladigan qismi. Ularni yo'q qilish uchun instrument va yozilgan konvensiya kerak, bahs emas.

## 41.7 Masofaviy va asinxron review

| Muammo | Yechim |
| --- | --- |
| Vaqt zonalari farqi | Yozma izoh to'liq va mustaqil bo'lsin |
| Ohangni noto'g'ri tushunish | Sabab va kontekstni yozish, emoji ortiqcha emas |
| Uzoq davralar | Blocker larni bir martada to'liq berish |
| Kontekst yo'qolishi | PR tavsifi va izohda havolalar |
| "Kim javob beradi" noaniqligi | CODEOWNERS va aniq murojaat |
| Tezkor savollar | 15 daqiqalik qo'ng'iroq, uch kunlik yozishma emas |

Asinxron review ning asosiy qoidasi: izoh o'zini tushuntirsin. Muallif boshqa vaqt zonasida uyg'onib, izohni o'qiganda qo'shimcha savol bermasdan ishlay olishi kerak. Bu "oqibat + alternativa + havola" shaklini majburiy qiladi.

## 41.8 Review ni o'rgatish

```markdown
<!-- Yangi jamoa a'zosi uchun review ga kirish rejasi -->
## Review ga qanday kirishamiz

### 1-hafta: kuzatish
Ikki PR ni tajribali reviewer bilan birga ko'rib chiqing (ekran ulashib).
Maqsad: nimaga qaraladi va qanday tartibda.

### 2-3-hafta: ikkinchi reviewer
PR larga ikkinchi reviewer sifatida qo'shiling. Izohlaringiz birinchi
reviewer bilan solishtiriladi - nima topildi, nima o'tkazib yuborildi.

### 4-hafta: mustaqil, past xavfli PR lar
`risk:low` va `risk:medium` PR larni mustaqil review qilasiz.

### Keyin: xavf darajasini oshirish
`risk:high` PR larda ikkinchi reviewer, keyin birinchi.

### Doimiy
- Har incidentdan keyin: "review nega ko'rmadi" savoliga javob.
- Har oyda bitta review ni birga tahlil qilish (nima yaxshi, nima yo'q).
```

## 41.9 Review madaniyatining buzilish belgilari

| Belgi | Nimani bildiradi |
| --- | --- |
| "LGTM" izohsiz, 2 daqiqada | Review marosimga aylangan |
| Bir xil odam hamma PR ni ko'radi | Bilim tarqalmaydi, nuqta bo'g'in |
| PR lar 3 kundan ko'p kutadi | Review byudjeti yo'q |
| Izohlarning yarmi `nit` | Instrument yo'q |
| Muallif izohlarga javob bermaydi | Jarayon majburiy emas |
| Bahslar PR dan tashqariga chiqadi | Kelishmovchilik tartibi yo'q |
| Katta PR lar normal holat | Bo'lish madaniyati yo'q |
| Junior lar PR yuborishdan qo'rqadi | Izoh tili bilan muammo |
| Review dan keyin ham prodda ko'p xato | Checklist incidentlardan o'smaydi |
| Reviewer "men faqat ko'rib qo'ydim" deydi | Mas'uliyat tarqamagan |

## 41.10 Review natijasi baholashga ishlatilmaydi

Code Complete inspeksiya haqidagi bo'limida ikki taqiqni ketma-ket qo'yadi va ikkisi ham review madaniyatining asosi.

Birinchi: menejmentni inspeksiyaga qo'shish odatda yaxshi fikr emas. Sabab mexanik: menejer ishtirok etganda o'zaro munosabat o'zgaradi, odamlar review materiali emas, o'zlari baholanayotganini his qiladi va diqqat texnik masaladan siyosiy masalaga ko'chadi. Menejmentning natijani bilish huquqi bor va shu uchun inspeksiya hisoboti tayyorlanadi, lekin hisobot va yig'ilish bir narsa emas.

Ikkinchi va kitob buni qat'iy shaklda yozadi: inspeksiya natijalari hech qanday holatda ishni baholash (performance appraisal) uchun ishlatilmaydi. Sababi ham berilgan: inspeksiyada ko'rilgan kod hali ishlab chiqilmoqda, baholash esa tugagan mahsulotga qaralishi kerak, tugallanmagan ishga emas.

Shu taqiq [42-bobdagi](42-review-metrikalari.md#422-zararli-metrikalar) zararli metrikalar ro'yxatining manbasi: muallif bo'yicha sanalgan "xatolar soni" yoki reviewer bo'yicha sanalgan "izohlar soni" aynan shu chegarani buzadi.

```text
# Nima qayerga ketadi: ikki chiqishni aralashtirmaslik kerak.

Review izohlari va topilmalari   -> PR da qoladi, muallif va reviewer o'rtasida
Topilma turlari statistikasi      -> checklistni yangilash uchun, anonim
Jarayon o'lchovlari (kutish, hajm) -> jamoaga, jarayonni tuzatish uchun

Odam bo'yicha topilma soni        -> hech qayerga. Baholashga ham, dashboardga ham.
```

Yig'ilish qoidalaridan ham bittasi shu yerga tegishli: kitob topilma tan olingan zahoti muhokamani to'xtatib keyingisiga o'tishni talab qiladi, va ba'zi guruhlar hatto "bu haqiqatan xatomi" degan bahsni ham taqiqlaydi, chunki kimdir chalkashib xato deb o'ylagan bo'lsa, demak kod yoki hujjat aniqlashtirilishi kerak. Yechim muhokamasi alohida vaqtga olinadi. PR da bu shunday ko'chadi: izoh ostidagi uzun yozishma odatda yechim bahsi va u [41.5](#415-kelishmovchilikni-hal-qilish) dagi tartibga chiqarilishi kerak.

Muallif tomoni uchun kitob yana bir odat beradi: muallif har bir aytilgan topilmani tan olib keyingisiga o'tadi va review paytida ishini himoya qilishga urinmaydi; tan olish rozilik degani emas, har bir bandni keyin alohida o'ylab ko'rish huquqi muallifda qoladi. Ego va izoh shakli haqidagi qolgan qoidalar [toza kod hujjatida](../clean-code/47-birgalikda-ishlash-va-orgatish.md#471-kodga-egalik-shaxsiy-emas-jamoaviy).

## 41.11 Uch ustun va review ni mavjud bo'lmagan jamoaga kiritish

Google kitobining jamoada ishlash bobi muloqotni uch ustunga yig'adi: kamtarlik (siz koinotning markazi emassiz, hammasini bilmaysiz va xato qilmaydigan odam emassiz, o'zingizni yaxshilashga ochiqsiz), hurmat (siz bilan ishlaydigan odamlarga haqiqatan e'tibor berasiz, ularning qobiliyati va natijasini qadrlaysiz) va ishonch (boshqalar malakali va to'g'ri ishni qiladi deb hisoblaysiz va kerak bo'lganda rulni ularga berishga rozisiz). Kitobning da'vosi kuchli: deyarli har qanday ijtimoiy ziddiyatning sababini oxirigacha surib borsangiz, shu uchtadan birining yo'qligiga borib taqaladi.

Review uchun bu uchtadan ikkinchisi muhim: kitob kasbiy muhitda tanqid deyarli hech qachon shaxsga qaratilmasligini aytadi va ikki narsani ajratishni talab qiladi - odamning ijodiy natijasiga qaratilgan konstruktiv tanqid va odamning shaxsiga qaratilgan hujum. Ikkinchisi foydasiz, chunki unga javoban hech narsa qilib bo'lmaydi. Birinchisi esa hurmatga asoslangan: izoh yozayotgan odam haqiqatan ishning yaxshilanishini xohlaydi.

Kitob shu farqni izoh shaklida ham ko'rsatadi va mexanizm [41.1](#411-izoh-tili-kodga-qarash-odamga-emas) dagi jadvalga qo'shimcha beradi: savolni **o'zingiz** haqida qilish. "Sen bu yerda boshqaruv oqimini butunlay noto'g'ri qilgansan, hamma ishlatadigan naqshni ishlat" o'rniga "Bu yerdagi boshqaruv oqimida chalkashib qoldim; X naqshi buni tushunarliroq va saqlashga oson qilarmidi?" Farqi ikki joyda: muallif "noto'g'ri" deb atalmaydi, va taklif rad etilishi mumkin bo'lgan shaklda qoldiriladi.

Eng amaliy qismi esa review madaniyati hali yo'q jamoa haqida. Kitob bir voqeani keltiradi: yangi ishga kirgan dasturchi kodbazani o'rganib, hamkasblariga xushmuomala code review izohlarini yuborishni boshlagan va bir necha haftadan keyin rahbari uni chaqirib, jamoadan "u bizni chapu o'ngdan tanqid qilyapti" degan shikoyatlar kelganini aytgan. Kitobning tahlili ayblovsiz: muammo izohlarda emas, jamoadagi keng tarqalgan ishonchsizlikni hisobga olmaslikda bo'lgan; to'g'ri yo'l review ni madaniyatga yumshoqroq kiritish, masalan g'oyani oldin jamoa bilan muhokama qilish va bir necha hafta sinab ko'rishni taklif qilish edi.

```markdown
<!-- Review yo'q jamoada boshlash: kelishuv birinchi, izoh keyin. -->
## Ikki haftalik sinov

1. Jamoa yig'ilishida maqsad aytiladi: xato topish emas, bilim tarqatish
   va qarorni yozib qoldirish (1-bob).
2. Birinchi ikki hafta FAQAT savol va `praise` izohlari. Blocker yo'q.
3. Formatlash va uslub izohlari taqiqlanadi: ular instrumentga o'tadi.
4. Ikki haftadan keyin jamoa qaror qiladi: davom etamizmi, nimani
   o'zgartiramiz. Qaror `REVIEW.md` ga yoziladi (1-bob).
5. Shundan keyingina `blocker` darajasi va SLA kiritiladi (40-bob).
```

Diqqat: uch ustun va psixologik xavfsizlik mavzusining to'liq yozuvi [toza kod hujjatida](../clean-code/47-birgalikda-ishlash-va-orgatish.md#471-kodga-egalik-shaxsiy-emas-jamoaviy); bu yerda faqat ularning review jarayoniga tegadigan qismi.

## 41.12 Izoh oqimi: bo'lak-bo'lak javob, TODO va PTAL

Google kitobi review ning muloqot tomoniga uch aniq qoida beradi va ularning hammasi vaqt tejaydi.

Birinchi, reviewer uchun: javob tez bo'lishi kerak, Google da kutilgan muddat 24 ish soati, va agar reviewer shu vaqtda ulgurmasa, hech bo'lmaganda o'zgarishni ko'rganini va imkon topishi bilan qarashini yozishi kutiladi.

Ikkinchi, va u korpusda yo'q edi: reviewer izohlarni **bo'lak-bo'lak** bermasligi kerak. Kitobning so'zi bilan, muallifni review dan izoh olib, uni tuzatib, keyin bog'liq bo'lmagan yangi izohlar olishdan ko'proq bezdiradigan narsa kam. Shundan amaliy qoida: reviewer diffni oxirigacha o'qib, keyin barcha izohni bir martada beradi. Yarim o'qilgan diffdan izoh yozish davralar sonini oshiradi va [2.7](02-review-iqtisodi-xato-narxi-navbat-va-pr.md#27-rework-review-ning-yashirin-narxi) dagi rework narxini to'g'ridan-to'g'ri ko'taradi.

Uchinchi, muallif uchun: har bir reviewer izohi TODO bandi sifatida qaraladi. Kitobning ta'rifi ikki qismdan iborat va ikkisi ham muhim: izohni so'zsiz qabul qilish shart emas, lekin unga **javob berilishi** shart. Rozi bo'lmasangiz, buni va sababini aytasiz, va izohni hal qilingan deb belgilamaysiz, chunki ikki tomon ham muqobil taklif qilish imkoniga ega bo'lishi kerak. Bahsni odobli saqlashning keng tarqalgan usuli ham shu: muqobil taklif qilib, reviewer dan qayta qarashni so'rash (PR muhitida "PTAL", please take another look).

```text
# Bo'lak-bo'lak izoh (yomon): uch davra, uch kontekst almashinuvi.
10:05  reviewer: 1-faylga 2 izoh          -> muallif tuzatadi
11:40  reviewer: 4-faylga 3 izoh          -> muallif tuzatadi
15:20  reviewer: dizayn haqida e'tiroz    -> muallif qayta yozadi

# To'liq o'qilgandan keyingi izoh (yaxshi): bir davra.
11:40  reviewer: diff to'liq o'qildi.
       blocker: 2 ta (dizayn e'tirozi birinchi: qolganlari undan keladi)
       suggest: 1 ta
       nit:     1 ta
       Savol:   4-faylda idempotentlik kaliti qayerda saqlanadi?
       -> muallif bir martada javob beradi va PTAL yozadi
```

Yana ikki qoida izoh ohangini belgilaydi. Reviewer muallifning yondashuviga qarab shoshilinch xulosa chiqarmasligi kerak: nimani nega shunday qilganini so'rash, yondashuv noto'g'ri deb taxmin qilishdan yaxshiroq. Va kod egasi tomoni: tashqaridan kelgan muallifning o'zgarishiga ochiq bo'lish kerak, o'zgarish kodbazani yaxshilayotgan bo'lsa, muallifning fikriga yon beriladi. Asinxron review ning qolgan mexanikasi [41.7](#417-masofaviy-va-asinxron-review) da.

## 41.13 Ishni qaytarib olish va mansab bilan bosish

Orosz tajribali muhandisning uchta xatti-harakatini sanaydi; uchalasi ham review da ko'rinadi va uchalasi ham ishonchni bitta PR darajasida emas, jamoa darajasida yo'q qiladi.

Birinchisi **ishni qaytarib olish**. Tajribali muhandis vazifani kamroq tajribali hamkasbiga beradi, keyin uning yechimi odatiy bo'lmagan yo'l bilan yozilganini ko'rib, ishni qaytarib oladi. Orosz ning kuzatuvi natijada emas, keyingi xulqda: bu hamkasbdagi ishonchsizlikni ochiq ko'rsatadi va kamroq tajribali muhandis bundan keyin o'sha odamdan maslahat va yo'l-yo'riq so'rashdan qochadi (Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 22-bob, 309-bet). Review tilida bu reviewer ning PR ni o'zi qayta yozib, "men tuzatib qo'ydim" deb yopishi. To'g'ri yo'l: yondashuv boshqacha bo'lsa-yu ishlasa, uni qabul qilish; haqiqatan noto'g'ri bo'lsa, oqibatni ko'rsatib izoh yozish va tuzatishni muallifga qoldirish ([41.1](#411-izoh-tili-kodga-qarash-odamga-emas)).

Ikkinchisi **mansab bilan bosish**. Taklifni muhokama qilishda hech qanday egiluvchanlik ko'rsatmaslik va o'z nuqtai nazarini oddiygina itarib yuborish. Orosz eng yomon shaklini aniq keltiradi: ratsional dalil o'rniga mansabga tayanish, ya'ni "men staff engineer man va bu shunday bo'lishi kerak, chunki men shunday deyman" ohangidagi javob. Bunday muhandis o'zi haq bo'lganda ham shaxsiy maqsad ko'zlayotgandek ko'rinadi (22-bob, 309-bet). Review da buning yagona davosi [41.5](#415-kelishmovchilikni-hal-qilish) dagi tartib: pozitsiya dalil tilida yoziladi, dalil bo'lmasa qaror qaytarilish narxiga qarab beriladi.

Uchinchisi **majburiyatni zo'rlab olish**. Orosz Amazon ning "disagree and commit" prinsipini keltiradi: qaror qabul qilinayotganda e'tiroz bildirish, qabul qilingandan keyin esa uni qo'llab-quvvatlash. Prinsipning o'zi foydali, lekin Orosz uning quroldek ishlatilishini ko'rsatadi: kelishuv umuman bo'lmagan joyda majburiyat talab qilish. Bu qisqa muddatda ishlaydi, lekin do'st orttirmaydi (22-bob, 309-bet).

| Belgi | PR da qanday ko'rinadi | To'g'ri harakat |
| --- | --- | --- |
| Ishni qaytarib olish | Reviewer muallif branchiga o'zi commit qiladi va PR ni yopadi | Izoh yozib, tuzatishni muallifga qoldirish |
| Mansab bilan bosish | "Shunday bo'ladi" tipidagi javob, sababsiz | Oqibatni raqam yoki ssenariy bilan ko'rsatish |
| Majburiyatni zo'rlash | Bahs ochiq, lekin "kelishdik" deb yopiladi | Kelishmovchilikni yozib qoldirish, keyin qaror |

Uchalasining umumiy ildizi bitta: niyat yaxshi bo'lsa ham, kontekst ko'rinmasa hamkasblar xatti-harakatni o'ziga xizmat qiluvchi deb o'qiydi. Shuning uchun qaror sababini yozib qoldirish review da odob masalasi emas, ishonchni saqlash mexanizmi.

## 41.14 Amalda qo'llash

- [ ] Izoh prefikslari va ularning ma'nosini `REVIEW.md` ga yozib, jamoada kelishib oling.
- [ ] Kelishmovchilik tartibini (ikki davra, keyin suhbat) yozib, uni amalda qo'llashni boshlang.
- [ ] Oxirgi 50 izohni sanab, `nit` ulushini aniqlang; 20 foizdan ko'p bo'lsa, instrumentlarga ko'chiring.
- [ ] Izoh shabloniga "oqibat + alternativa + havola" talabini kiriting.
- [ ] Yangi a'zolar uchun review ga kirish rejasini yozib, uni onboarding ga qo'shing.
- [ ] Har oyda bitta review ni jamoada birga tahlil qilishni odat qiling.
- [ ] Madaniyat buzilish belgilarini chorakda bir marta tekshirib, topilganlarini muhokama qiling.
- [ ] `praise` izohini ongli ishlatishni boshlang: to'g'ri qilingan qiyin joyni ko'rsatish.

## Manbalar

- [Google, How to Write Code Review Comments](https://raw.githubusercontent.com/google/eng-practices/3bb3ec25b3b0199f4940b1aa75f0ac5c5753301c/review/reviewer/comments.md) - kodga qarash va odamga qaramaslik, nega tushuntirish, tuzatish mas'uliyati muallifda, izoh darajasini belgilash (`Nit:`, `Optional:`, `FYI:`) va belgisiz izohning majburiy o'qilishi, yaxshi qilingan ishni ham aytish
- [Google, Handling Pushback in Code Reviews](https://raw.githubusercontent.com/google/eng-practices/3bb3ec25b3b0199f4940b1aa75f0ac5c5753301c/review/reviewer/pushback.md) - kim haq ekanini birinchi o'ylash, kod salomatligining kichik qadamlar bilan o'sishi, "keyin tozalayman" tuzog'i, xafalikning izoh shaklidan kelishi
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 21.3 "Roles During an Inspection", `Management` (486-487-betlar) - menejment ishtiroki diqqatni texnikdan siyosiyga ko'chiradi; inspeksiya natijalari hech qanday holatda ishni baholashga ishlatilmaydi, chunki ko'rilgan kod hali tugallanmagan
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 21.3 "Inspection Meeting" (488-bet) - topilma tan olingach muhokamani to'xtatish; "bu haqiqatan xatomi" bahsini taqiqlagan guruhlar; yechim muhokamasini alohida vaqtga olish
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 21.3 "Egos in Inspections" (490-bet) - muallif har bir aytilgan topilmani tan olib o'tadi va ishini himoya qilishga urinmaydi; tan olish rozilik degani emas
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 2-bob, "The Three Pillars of Social Interaction" - kamtarlik, hurmat va ishonch ta'riflari; ijtimoiy ziddiyatning ildizi shu uchtadan birining yo'qligi
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 2-bob, "Humility, Respect, and Trust in Practice" - konstruktiv tanqid va shaxsga hujum farqi; savolni o'zi haqida qilish va taklifni rad etilishi mumkin shaklda qoldirish; review ni ishonchsiz jamoaga kiritish voqeasi va jamoa bilan oldin kelishish tavsiyasi
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 9-bob, "Be Polite and Professional" - 24 ish soati ichida javob va ulgurmasa "ko'rdim" deb yozish; izohni bo'lak-bo'lak bermaslik; har izohni TODO bandi deb olish, javobsiz qoldirmaslik va muqobil taklif bilan qayta qarashni so'rash; muallif yondashuvi haqida shoshilinch xulosa chiqarmaslik; kod egasining tashqi muallifga ochiq bo'lishi
- Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 22-bob, "Internal Politics" (309-bet) - ishni kamroq tajribali hamkasbdan qaytarib olish va uning maslahat so'rashni to'xtatishi; ratsional dalil o'rniga mansabga tayanish; "disagree and commit" ni kelishuv yo'q joyda majburiyat talab qilish uchun ishlatish

---

[&larr; 40. Review jarayonini qurish](40-review-jarayonini-qurish.md) · [Mundarija](README.md) · [42. Review metrikalari &rarr;](42-review-metrikalari.md)
