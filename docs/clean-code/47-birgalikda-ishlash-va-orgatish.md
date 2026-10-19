<!-- doc: clean-code | chapter: 47 | part: XII. Professional intizom -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 47. Birgalikda ishlash va o'rgatish (Collaboration and Mentoring)

<details>
<summary>Bu bobdagi 7 bo'lim</summary>

- [47.1 Kodga egalik: shaxsiy emas, jamoaviy](#471-kodga-egalik-shaxsiy-emas-jamoaviy)
- [47.2 Ustoz-shogird modeli](#472-ustoz-shogird-modeli)
- [47.3 Yangi odamga toza kod standartini yetkazish](#473-yangi-odamga-toza-kod-standartini-yetkazish)
- [47.4 Review ni o'rgatish vositasiga aylantirish](#474-review-ni-orgatish-vositasiga-aylantirish)
- [47.5 Jamoa kelishuvi (working agreement) yozish](#475-jamoa-kelishuvi-working-agreement-yozish)
- [47.6 Yordam so'rash va yordam berish: blokni ochish odobi](#476-yordam-sorash-va-yordam-berish-blokni-ochish-odobi)
- [47.7 Amalda qo'llash](#477-amalda-qollash)

</details>


Toza kod jamoaviy natija: bir odam yolg'iz uni saqlab qola olmaydi. Bu bobda jamoaviy egalik, ustoz-shogird munosabati, standartni yetkazish va jamoa kelishuvi. Code review mexanikasi va texnik yetakchilik [arxitektor hujjatidagi](../architect/README.md) code review va texnik yetakchilik bo'limida.

## 47.1 Kodga egalik: shaxsiy emas, jamoaviy

Jamoaviy egalik (collective ownership) - kodning guruhga tegishli bo'lishi va uni guruhning har bir a'zosi o'qib, o'zgartira olishi. McConnell bu yondashuvning uch foydasini sanaydi: kodga bir necha juft ko'z qaragani uchun sifat ko'tariladi; odam loyihadan ketganda zarar kichik bo'ladi, chunki har bir qismni bir necha kishi biladi; va xatoni tuzatish davri qisqaradi, chunki tuzatishni bo'sh turgan har qanday dasturchiga berish mumkin.

Teskari holat ikki ko'rinishda chiqadi va ikkisi ham kitoblarda nomlangan. Birinchisi - bilimning bitta odamda to'planishi. Google kitobi buni **bus factor** deb ataydi: loyiha to'xtab qolishi uchun qancha odam yo'qolishi kerak. Yolg'iz ishlamay, bir kolleg bilan ishlash bu sonni ikki barobar oshiradi. O'sha kitobning bilim almashish bobi bu yagona nuqtaning (SPOF) qaerdan o'sib chiqishini ham ko'rsatadi: "buni men o'zim qilib beraman" odati qisqa muddatda tez, uzoq muddatda esa jamoa hech qachon o'rganmaydi. Ikkinchi ko'rinishi - o'sha kitobdagi **arvohli qabristonlar** (haunted graveyards): kodning odamlar qo'rquv tufayli tegmaydigan joylari.

Jamoaviy egalik tekin emas. McConnell uning ishni muvofiqlashtirish ehtiyojini oshirishini alohida aytadi, shuning uchun "hamma hammasini o'zgartiradi" degani "hech kim javob bermaydi" degan ma'noni bermaydi: CODEOWNERS bilan sohaga mas'ul belgilanadi ([arxitektor 36.10](../architect/36-code-review-va-jamoada-texnik-yetakchilik.md#3610-jamoaning-bilim-xaritasi-va-bitta-odamga-bogliqlikni-kamaytirish)), lekin mas'ullik to'siq emas, bilim markazi bo'ladi. Shu bilan birga fayl boshidagi `@author` tegi egalikni shaxsiylashtiradi va eskiradi, shuning uchun ishlatilmaydi ([9.5](09-yomon-izohlar-katalogi.md#95-jurnal-izohlari-va-mualliflik-imzolari)).

"Bu mening kodim" munosabatining ildizi psixologik. Google kitobining jamoada ishlash bobi buni to'g'ridan-to'g'ri aytadi: sizning qadringiz yozgan kodingizga bog'liq emas, va kasbiy muhitda tanqid deyarli hech qachon shaxsga qaratilmaydi, u loyihani yaxshilash jarayonining bir qismi. O'sha kitobning code review bobi review ning madaniy ta'sirini shunday izohlaydi: review dasturchiga kod "uning mulki" emas, umumiy ishning bo'lagi ekanini eslatadi va tanqidni belgilangan, neytral shaklga soladi.

Shu sababli review izohi kod haqida gapiradi, muallif haqida emas. McConnell inspeksiyadagi egolar haqidagi bo'limida aynan shu chegarani chizadi: inspeksiyaning maqsadi muallifni tanqid qilish emas, va "Java ni biladigan har qanday odam buni biladi" uslubidagi izoh butunlay nomaqbul, uni moderator darhol to'xtatishi kerak.

```text
Yomon: "Nega sen bu yerda Optional ishlatmagansan?"
Yaxshi: "Bu metod null qaytarishi mumkinmi? Optional aniqroq bo'lardi."
```

Oxirgi qaror muallifda qoladi: McConnell reviewer xatoni topishga haqli, lekin uni qanday tuzatish kerakligini hal qilish huquqi muallifda ekanini yozadi.

## 47.2 Ustoz-shogird modeli

Qoidani hujjatga yozib qo'yish bilan u amalga oshmaydi. McConnell buni qisqa qilib aytadi: standartni yozib tarqatish mumkin, lekin u haqda hech kim gapirmasa va uni ishlatishga undamasa, standart bajarilmaydi. Shuning uchun birgalikda ishlash amaliyotlari (review, inspeksiya, juftlikda ishlash) bir vaqtda ikki ish qiladi: xato topadi va kasbni uzatadi. Tajribasiz dasturchiga ko'proq biladigan odamning yo'riqnomasi kerak, ko'p biladigan va shu sababli band odamni esa bilganini ulashishga undash kerak.

Google kitobi mentorlikni rasmiy rolga aylantiradi va uning shaklini aniq belgilaydi.

| Jihat | Google kitobidagi mentor modeli |
|---|---|
| Kim | ixtiyoriy, kompaniyada bir yildan ortiq ishlagan odam |
| Kim emas | mentee ning rahbari yoki tech lead i emas |
| Qaysi jamoadan | boshqa jamoadan: shunda qiyin vaziyatda so'rash osonroq |
| Vazifasi | savollarga javob berish va yangi odamni ishga kirishtirish |
| Maqsadi | psixologik xavfsizlik: savol berish uchun aniq adres bo'lishi |

Modelning mohiyati rasmiylikda emas, yangi odamning "kimning vaqtini olyapman" degan to'siqdan xalos bo'lishida: mentor borligi savol berishni qimmat qilmaydi. Google kitobi o'z tadqiqotiga tayanib psixologik xavfsizlikni samarali jamoaning eng muhim qismi deb ataydi, mentor tayinlash esa uni qurishning amaliy yo'li.

Ustozning asosiy xatosi ishni o'zi qilib qo'yish. Google kitobining yetakchilik bobi teskarisini tavsiya qiladi: ishni boshqa dasturchiga topshirish kerak, hatto u sizdan sekinroq bajarsa ham, chunki jamoa faqat shunday o'rganadi.

Bu ishning natijasi kuzatilgan: McConnell rasmiy inspeksiyani joriy qilgan bir jamoaning hisobotini keltiradi - inspeksiya barcha dasturchilarni tez orada eng yaxshi dasturchining darajasiga ko'targan.

## 47.3 Yangi odamga toza kod standartini yetkazish

Google kitobi bilim uzatishning beshta kanalini sanaydi: ochiq soat (office hours), texnik ma'ruza, dars, hujjat va code review. Yangi odamga ularning hammasi bir vaqtda berilmaydi. Quyidagi tartib shu kanallarning onboarding uchun joylashuvi: ro'yxatning o'zi shu korpusning tavsiyasi, har bir bandning asosi esa havola qilingan manbada.

1. **Namuna kod**: shablon loyiha va mavjud eng toza modul - yangi odam birinchi navbatda shunga qaraydi ([arxitektor 36.9](../architect/36-code-review-va-jamoada-texnik-yetakchilik.md#369-standart-ornatish-linter-formatlash-archunit-qoidalari-shablon-loyiha)).
2. **Mashina**: formatter va linter qoidani darhol, muhokamasiz o'rgatadi ([13-bob](13-formatlashni-avtomatlashtirish-va-diff.md), [42-bob](42-statik-tahlil-va-avtomatik-qoidalar.md)).
3. **Review**: birinchi o'zgarishlarda batafsil va sabab bilan izoh. Google kitobi bu amaliyotning tarixini keltiradi: kompaniyaning boshida bir odam har bir yangi xodimning birinchi katta commitini qator-qator ko'rib chiqar edi, va bu ish uslubni tekislashdan ko'ra ko'proq ishni bajargan - u eng yaxshi amaliyotlarni o'rgatgan. Keyinchalik shu ish "readability" degan kompaniya darajasidagi mentorlik jarayoniga aylandi.
4. **Juftlikda ishlash**: faqat bitta shart bilan - McConnell ikki yangi odamni juftlashtirmaslikni tavsiya qiladi, juftlikda kamida bittasi avval juftlikda ishlagan bo'lishi kerak ([41.7](41-ozgarishni-kiritish-jarayoni-kichik-qadamlar.md#417-pair-va-mob-programming-mexanikasi)).
5. **Hujjat**: qolgan qism uchun havola sifatida ([48-bob](48-tezkor-malumotnoma-qoidalar-va-tekshiruv.md)).

Hujjatni birinchi o'ringa qo'yish ishlamaydi, lekin undan voz kechish ham noto'g'ri: Google kitobi hujjatni tuzatish uchun eng yaxshi payt - uni birinchi marta o'qib o'rgangan payt deb yozadi, chunki keyinroq nimaning qiyin bo'lgani esdan chiqadi. Yangi odamning savoli va tuzatishi shu sababli hujjatning eng qimmatli qaytarma aloqasi.

Ro'yxatning uzunligi ham ahamiyatli. McConnell inspeksiya ro'yxati haqida aniq chegara beradi: ro'yxat bir sahifadan oshmasin, uzunini kerakli tafsilot darajasida ishlatish qiyin. Shu mantiq yangi odamga beriladigan qoida to'plamiga ham tegishli: bir varaqqa sig'maydigan ro'yxat o'qilmaydi.

Oxirgi va eng ko'p esdan chiqadigan qism - mavjud kodni hurmat qilish. Google kitobi buni "Chesterson's fence" printsipi deb keltiradi (kitobda shu imloda): biror narsani o'chirish yoki o'zgartirishdan oldin u nega borligini tushunish kerak. Yangi odam notanish kodga "bu yomon" deb baho berishga moyil; to'g'ri yo'l - avval sababini topish, keyin o'zgartirish hamon ma'noli bo'lsa kiritish va sababni keyingi o'quvchi uchun yozib qoldirish.

## 47.4 Review ni o'rgatish vositasiga aylantirish

Review ning o'qitish funksiyasi [arxitektor 36.7](../architect/36-code-review-va-jamoada-texnik-yetakchilik.md#367-yangi-odamga-review-orqali-orgatish) da ko'rilgan. Google kitobi bu funksiyani code review ning eng muhim, lekin eng kam qadrlanadigan foydasi deb ataydi va bilim ikki yo'nalishda yurishini ta'kidlaydi: reviewer muallifga yangi texnika yoki kutubxonani ko'rsatadi, muallifning kodidan esa reviewer o'rganadi. McConnell walk-through haqida shu fikrni boshqa tomondan beradi: u tajribali dasturchi uchun tajriba va madaniyatni uzatish imkoni, yangi dasturchi uchun esa eskirgan taxminlarga savol berish imkoni.

Shu funksiya ishlashi uchun izohning shakli muhim. Google kitobidagi readability jarayonining qoidasi: reviewer izohiga sababni ko'rsatadigan havola qo'yadi, shunda muallif qoidaning kelib chiqishini o'rganadi; qoida sababi aniq bo'lmasa, muallif so'raydi.

| Izoh shakli | Nega shunday |
|---|---|
| "Bu yomon" | nol foyda: ko'rsatma yo'q, o'rganiladigan narsa yo'q |
| "Java ni biladigan har kim buni biladi" | nomaqbul: McConnell bunday izohni inspeksiyada to'xtatishni talab qiladi |
| "Bu metod ikki ish qiladi; `validate` ni ajratsak testlash osonlashadi" | muqobil taklif bor: muallif nima qilishini biladi |
| "Shu holatda `Optional` afzal, chunki ... ([18.7](18-xato-bilan-ishlash-qoidalari.md#187-null-qaytarmaslik-va-null-uzatmaslik))" | sabab havola bilan: readability jarayonining shakli |

Ikkinchi texnika - izohning majburiyligini ko'rsatish. Google kitobi reviewer ning izohni "FYI" deb belgilashi mumkinligini aytadi: bunday izoh hech qanday harakat talab qilmaydi, u faqat muallif uchun ma'lumot. Amalda shu g'oyaning kengaytirilgan shakli ishlatiladi: izohga `[majburiy]`, `[taklif]`, `[savol]`, `[nit]` prefiksini qo'yish. Prefiks muallifga nimani tuzatish shart va nimani ixtiyoriy ekanini darhol ko'rsatadi.

O'zgarishning hajmi review ning o'qitish qobiliyatiga to'g'ridan-to'g'ri ta'sir qiladi. Google kitobi "kichik o'zgarish" ni taxminan 200 qator kod deb belgilaydi va Google da o'zgarishlarning ko'pi bir kun ichida ko'rilishi kutilishini aytadi (bu review tugashi emas, birinchi qaytarma aloqa bir kun ichida kelishi). Katta o'zgarishda izohlar prioritetini ko'rsatib bo'lmaydi va muallif ularni o'rganish uchun emas, yopish uchun tuzatadi. Bu raqam korpusning [40.6](40-versiya-nazorati-gigiyenasi.md#406-pr-hajmi-va-bolish-texnikasi) bo'limidagi 400 qatorli chegara bilan ziddiyatda emas: 200 qator - normal o'zgarishning kutilgan o'lchami, 400 qator esa review sifati tushib ketadigan nuqta.

## 47.5 Jamoa kelishuvi (working agreement) yozish

Jamoa kelishuvi - og'zaki qoidalarni yozma shaklga keltirish. Uning birinchi qiymati - did haqidagi bahsni review dan olib tashlash. McConnell buni juftlikda ishlash sharti sifatida aytadi: kodlash standarti bo'lmasa, juftlik vaqtini uslub haqida bahslashishga sarflaydi va amaliyot samarasiz bo'ladi. Ikkinchi qiymati - yo'nalish: Google kitobining yetakchilik bobi jamoani bir yo'nalishda harakatlantirishning eng oson yo'li qisqa, hamma tushunadigan maqsad bayonotini yozish deb ko'rsatadi, chunki aniq maqsadsiz jamoa muvaffaqiyatga erishadi, lekin har a'zo mahsulotni o'z tomoniga tortgani uchun ko'p energiya yo'qotadi.

```markdown
# Jamoa kelishuvi

## Kod
- Formatlash: Spotless (google-java-format AOSP); review da uslub muhokama qilinmaydi.
- Yangi value object lar `record` sifatida yoziladi.
- Pul `Money` turida; `double` taqiqlangan (ArchUnit tekshiradi).
- Konstruktor inyeksiyasi; maydon inyeksiyasi taqiqlangan.
- Lombok: `@Getter`, `@RequiredArgsConstructor`, `@Slf4j` ruxsat; `@Data`, `@SneakyThrows` taqiqlangan.

## Commit va PR
- Atomik commit; formatlash va mantiq alohida commitda.
- Conventional commits prefikslari.
- PR hajmi chegarasi yozilgan va u kuzatiladi (47.4, 40.6).
- PR ochishdan oldin o'zini review qilish ro'yxati to'ldiriladi.

## Review
- Navbat: birinchi qaytarma aloqa bir ish kuni ichida (47.4).
- Izoh prefikslari: [majburiy], [taklif], [savol], [nit].
- Sabab ko'rsatilmagan "majburiy" izoh majburiy emas.

## Tugatish
- Ishni tugatish ta'rifi: `docs/definition-of-done.md`.
- Testsiz xatti-harakat o'zgarishi merge qilinmaydi.

## Qayta ko'rish
- Bu kelishuv har chorakda ko'rib chiqiladi; oxirgi: 2026-01-15.
```

Kelishuvning mazmuni jamoaga bog'liq, lekin ikki xususiyati umumiy: unda faqat bahsga sabab bo'lgan qoidalar turadi, va har bir qoidaning yoniga uni kim tekshiradi (mashina yoki odam) deb yoziladi. Mashina tekshiradigan qoida kelishuvdan statik tahlilga ko'chadi ([42-bob](42-statik-tahlil-va-avtomatik-qoidalar.md)).

**Har qoida yonida uning sababi va tortilgan foyda-zarari yoziladi.** Google ning uslub ko'rsatmalarida bu majburiy amaliyot: qoida qo'shilganda uning ustunligi va kamchiligi muhokama qilinadi va bu mulohaza qoidaning o'zi bilan birga yoziladi. Foydasi uzoq muddatli: **qoidani qayta ko'rish vaqti kelganini bilish mumkin bo'ladi**. Qoidaga ta'sir qilgan omillar ochiq yozilgan bo'lsa, ulardan biri o'zgarganda (til yangi versiya chiqardi, vositani saqlash qimmatlashdi, muhandislar qoidani chetlab o'tishga vaqt sarflay boshladi) qoidani qayta baholash kerakligi ko'rinadi. Sabab yozilmagan qoida esa jim eskiradi va "shunday qabul qilingan" holatiga o'tadi.

Qoidani o'zgartirish ham shu asosda ishlaydi: o'zgarish **aniq namunalarda ko'rsatilgan muammoga** tayanadi, shaxsiy didga emas. Google da bu qarorlarni uslub arbitrlari guruhi qabul qiladi va qaror ovoz berish bilan emas, konsensus bilan chiqadi, chunki har qaror shaxsiy afzallik emas, tortilgan foyda-zarar bahosi.

**Istisno (waiver) kamdan-kam beriladi.** Istisno faqat qoidani buzish undan qochishdan foydaliroq bo'lgan holatda beriladi. Rad etiladigan tipik sabab - "nom uzun chiqadi" yoki "loyiha ichidagi izchillik buziladi": kod bazasining butunligi bitta loyihaning izchilligidan ustun. Agar bitta qoida uchun o'rinli ko'rinadigan, lekin aslida o'rinsiz istisno so'rovlari ko'p kelsa, bu qoidani aniqlashtirish kerakligining signali.

```markdown
## Istisnolar
- `UZB_` prefiksi: taqiqlangan (42.3). Istisno yo'q.
- `@SuppressWarnings`: faqat sabab izohi bilan va ticket havolasi bilan.
  Istisnoni ikki reviewer tasdiqlaydi; "nom uzun" sabab emas.
```

## 47.6 Yordam so'rash va yordam berish: blokni ochish odobi

Katta tashkilotda to'siqlarning ko'pi texnik emas. Orosz ro'yxatini beradi: kerakli funksiyaga qaysi jamoa egalik qilishini bilmaslik, konfiguratsiyani o'zgartirish huquqi yo'qligi, boshqa jamoadan code review kutish, ya'ni hamkasbning kiritishiga bog'liq deyarli har qanday ish (Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 7-bob, 95-bet). Bunday to'siqda kodni emas, suhbatni to'g'ri olib borish kerak. Qachon to'xtash va "men qotib qoldim" deb tan olish kerakligi [ko'r yo'lak va botqoqdan chiqish](46-vaqt-diqqat-va-mashq.md#465-kor-yolak-va-botqoqdan-chiqish) bo'limida.

So'rashdan oldingi tayyorgarlik so'rovning narxini belgilaydi. Orosz buni "xayrixohlik balansi" (goodwill balance) deb ataydi: boshqalarga yordam bersangiz balans o'sadi, sababsiz uzsangiz tushadi, va yangi odamda balans yuqori bo'ladi, lekin arzimagan savol bilan tez tugaydi (7-bob, 107-bet). Shuning uchun tartib: avval odatiy debug va ma'lumot yig'ish qadamlari, o'z jamoangiz kodida esa manba tarixi va so'nggi commit lar; shundan keyin hamkasbga tayyorlanib borasiz, ya'ni muammoni aniq tushuntirib, nima sinaganingizni va yordam bo'lmasa keyingi qadamingiz nima bo'lishini aytasiz (7-bob, 107-bet).

ESLATMA: pastdagi ikki namunadagi so'rov shakli shu korpusning amaliy ko'rinishi; kitobdan olingani tayyorlanib borish talabining o'zi.

```text
Yomon: "Kafka consumer ishlamayapti, qarab bera olasizmi?"

Yaxshi: "OrderEventListener offset commit qilmayapti, lag o'syapti.
Sinaganim: auto-commit o'chirilgan, ack rejimi MANUAL, log'da rebalance
ko'rinmaydi. Taxminim: listener container konfiguratsiyasi.
Yordam bo'lmasa keyingi qadamim: consumer ni alohida profilda ishga
tushirib trace yoqish. Bir necha daqiqa vaqtingiz bormi?"
```

Yordam berish tomonida asosiy xato yechimni darhol aytish. Orosz qoidasi aniq: hamkasb qotib qolganida, xatoli qatorni bilsangiz ham uni ko'rsatib qo'ymang, ularga blokni o'zlari ochishni o'rgating, ya'ni yangi debug usulini ko'rsatib, keyin savollar bilan o'sha qatorga olib boring (11-bob, 162-163-bet). Bu [ustoz-shogird modeli](#472-ustoz-shogird-modeli) dagi "ishni o'zing qilib qo'yma" qoidasining kundalik shakli. Bir necha kun bir muammo ustida turgan odamni ko'rsangiz juftlik taklif qilinadi (11-bob, 162-bet); juftlikning shakllari [pair va mob programming mexanikasi](41-ozgarishni-kiritish-jarayoni-kichik-qadamlar.md#417-pair-va-mob-programming-mexanikasi) da.

Jamoadan tashqaridagi to'siq uchun Orosz to'rt qadamli zinani beradi va tartibni buzmaslikni talab qiladi: tushuntirish (nega kerak, nimani bloklayapti, muddat qachon), so'rash (qachon qarashini so'rab, yangilanish olish), ogohlantirish (javob bo'lmasa, menejerga murojaat qilishni oldindan aytish) va shundan keyingina eskalatsiya (7-bob, 97-98-bet). Sababi munosabat: yaxshi munosabat uzoq muddatda bitta vazifani tezroq yopishdan muhimroq, shuning uchun eskalatsiya hamkasbni rahbari oldida yomon ko'rsatadigan shaklda qilinmaydi va ish bitgach o'sha odamga ochiq rahmat aytiladi (7-bob, 97-98-bet).

## 47.7 Amalda qo'llash

- [ ] `@author` teglarini olib tashlab, egalikni CODEOWNERS ga ko'chiring.
- [ ] Review izohlarini kodga qaratilgan shaklga o'tkazish uchun 47.1 dagi misollarni jamoaga ko'rsating.
- [ ] Izoh prefikslarini ([majburiy], [taklif], [savol], [nit]) joriy qiling va "FYI" (harakat talab qilmaydigan) izohni ajratib ko'rsatadigan qilib yozing.
- [ ] Yangi odam uchun birinchi hafta rejasini yozing: bir varaqqa sig'adigan qoida ro'yxati, shablon loyiha, tajribali odam bilan juftlik sessiyasi.
- [ ] Yangi odamga mentor tayinlang: rahbari va tech lead i emas, imkon bo'lsa boshqa jamoadan.
- [ ] Shablon loyihani (yoki mavjud eng toza modulni) namuna sifatida belgilang va havola bering.
- [ ] Jamoa kelishuvini 47.5 shabloni bo'yicha yozib, repoda saqlang.
- [ ] Kelishuvni har chorakda ko'rib chiqish sanasini kalendarda belgilang.
- [ ] Har bir kritik tizimda kamida ikki odam o'zgartirish kirita olishini ta'minlang ([arxitektor 36.10](../architect/36-code-review-va-jamoada-texnik-yetakchilik.md#3610-jamoaning-bilim-xaritasi-va-bitta-odamga-bogliqlikni-kamaytirish)).

## Manbalar

- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 8-bob ("Changing the Rules", "Exceptions") - har qoida bilan birga uning sababi va tortilgan foyda-zararini yozish va bu yozuvning qoidani qayta ko'rish vaqtini ko'rsatishi, qoida o'zgarishining aniq namunalarga tayanishi va konsensus bilan qabul qilinishi, istisnoning kamdan-kam berilishi hamda kodbaza butunligining loyiha izchilligidan ustunligi. Bu nashrning nusxasida barqaror bet raqami yo'q, shuning uchun bob va bo'lim nomi ko'rsatilgan
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 21-bob, "Collective Ownership Applies to All Forms of Collaborative Construction" (482-bet) - jamoaviy egalikning uch foydasi va uning muvofiqlashtirish narxi
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 21-bob, "Collaborative Construction Provides Mentoring in Corporate Culture and Programming Expertise" (482-bet) - yozilgan standart o'z-o'zidan bajarilmasligi; review orqali kasbni uzatish; inspeksiya jamoani eng yaxshi dasturchi darajasiga ko'targan hisobot
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 21.3 "Egos in Inspections" (490-bet) - maqsad muallifni tanqid qilish emas; "Java ni biladigan har kim" uslubidagi izohning nomaqbulligi; tuzatish yo'lini tanlash huquqi muallifda
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 21.3, inspeksiya ro'yxati (489-490-betlar) - ro'yxat bir sahifadan oshmasin
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 21.2 "Keys to Success with Pair Programming" (483-484-betlar) - kodlash standarti bo'lmasa juftlik uslub haqida bahslashadi; ikki yangi odamni juftlashtirmaslik
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 21.4 "Walk-Throughs" (492-bet) - walk-through tajriba va madaniyatni uzatish, hamda eskirgan taxminlarga savol berish imkoni
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 2-bob - bus factor ta'rifi va uni oshirish; tanqid shaxsga qaratilmasligi, "siz yozgan kodingiz emassiz"
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 3-bob - psixologik xavfsizlik samarali jamoaning eng muhim qismi; mentor tayinlash modeli (ixtiyoriy, bir yildan ortiq, rahbar emas, boshqa jamoadan); SPOF va arvohli qabristonlar; bilim uzatishning besh kanali; hujjatni birinchi o'qishda tuzatish; "Chesterson's fence"; readability jarayoni va birinchi commitni qator-qator ko'rib chiqish
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 5-bob - ishni sekinroq bajarsa ham topshirish, chunki jamoa shunday o'rganadi; qisqa maqsad bayonoti jamoani bir yo'nalishga qo'yishi
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 9-bob - review kod "shaxsiy mulk" emasligini eslatishi va tanqidni neytral shaklga solishi; bilim almashish ikki yo'nalishda; "FYI" izohi; kichik o'zgarish taxminan 200 qator va birinchi qaytarma aloqa bir kun ichida
- Gergely Orosz, *The Software Engineer's Guidebook*, 1-nashr, Pragmatic Engineer, 2023, 7-bob (95, 97-98, 107-bet) va 11-bob (162-163-bet) - katta tashkilotda to'siqlarning texnik emasligi (egalik, huquq, boshqa jamoadan review kutish), xayrixohlik balansi va yordam so'rashdan oldingi tayyorgarlik, eskalatsiya zinasi (tushuntirish, so'rash, ogohlantirish, eskalatsiya) hamda munosabatni saqlash va rahmat aytish, blokdagi hamkasbga yechimni aytmasdan savol bilan yo'naltirish va juftlik taklif qilish
- ESLATMA: 47.3 dagi besh bandning tartibi, 47.4 dagi `[majburiy]`, `[taklif]`, `[savol]`, `[nit]` prefiks to'plami va 47.5 dagi kelishuv shabloni shu korpusning amaliy tavsiyasi, kitobdan olingan emas; kitobdan olingani faqat harakat talab qilmaydigan izohni ajratish g'oyasi ("FYI") va bandlarning har biri uchun keltirilgan asos
---

[&larr; 46. Vaqt, diqqat va mashq](46-vaqt-diqqat-va-mashq.md) · [Mundarija](README.md) · [48. Tezkor ma'lumotnoma: qoidalar va tekshiruv ro'yxatlari &rarr;](48-tezkor-malumotnoma-qoidalar-va-tekshiruv.md)
