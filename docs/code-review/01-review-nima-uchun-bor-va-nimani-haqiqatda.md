<!-- doc: code-review | chapter: 1 | part: I. Review ning mohiyati va iqtisodi -->

[Barcha hujjatlar](../../README.md) / [Kod review](README.md)

> Holat: tekshirilmoqda. Da'volar hali manbaga solishtirilmoqda.

# 1. Review nima uchun bor va nimani haqiqatda beradi (Why Review Exists)

<details>
<summary>Bu bobdagi 14 bo'lim</summary>

- [1.1 Review ning uchta haqiqiy mahsuloti](#11-review-ning-uchta-haqiqiy-mahsuloti)
- [1.2 Review nimani topmaydi](#12-review-nimani-topmaydi)
- [1.3 Filtrlarning mehnat taqsimoti](#13-filtrlarning-mehnat-taqsimoti)
- [1.4 Approve nimani anglatadi va nimani anglatmaydi](#14-approve-nimani-anglatadi-va-nimani-anglatmaydi)
- [1.5 Review mas'uliyatni ko'chirmaydi](#15-review-masuliyatni-kochirmaydi)
- [1.6 Review ning yon ta'siri: PR hajmini kichraytirishga majbur qilish](#16-review-ning-yon-tasiri-pr-hajmini-kichraytirishga-majbur-qilish)
- [1.7 Qachon review foyda bermaydi](#17-qachon-review-foyda-bermaydi)
- [1.8 Review arxitektura qaroridan keyin keladi](#18-review-arxitektura-qaroridan-keyin-keladi)
- [1.9 Review maqsadini jamoada yozib qo'yish](#19-review-maqsadini-jamoada-yozib-qoyish)
- [1.10 Review madaniyatini o'lchash uchun uchta savol](#110-review-madaniyatini-olchash-uchun-uchta-savol)
- [1.11 Review ning oltita foydasi va eng muhimi qaysi](#111-review-ning-oltita-foydasi-va-eng-muhimi-qaysi)
- [1.12 Xato topish usullarining o'lchangan samarasi](#112-xato-topish-usullarining-olchangan-samarasi)
- [1.13 Review mavjudligining oldini olish ta'siri](#113-review-mavjudligining-oldini-olish-tasiri)
- [1.14 Amalda qo'llash](#114-amalda-qollash)

</details>


Review haqidagi eng keng tarqalgan xato - uni xato topish mashinasi deb o'ylash. Agar maqsad faqat xato topish bo'lsa, review raqamlar bilan taqqoslaganda qimmat usul: bir soat odam vaqti ketadi va xatolarning yarmidan ko'pi o'tib ketadi. Review o'z narxini boshqa narsa bilan qoplaydi: u kod ustidan egalikni tarqatadi, qarorni ikkinchi miya bilan tekshiradi va jamoaga umumiy did beradi. Shu sababli review maqsadini aniq yozmagan jamoada u tez orada marosimga aylanadi: "LGTM" bosiladi, vaqt ketadi, foyda ko'rinmaydi.

## 1.1 Review ning uchta haqiqiy mahsuloti

Birinchi mahsulot - topilgan xato. Bu eng ko'rinadigan, lekin eng kichik qismi. Modern code review bo'yicha o'tkazilgan kuzatuvlarda review izohlarining katta qismi (taxminan uchdan ikki qismi va undan ko'pi) funksional xato haqida emas, o'qiluvchanlik, nomlash, tuzilish va mavjud kod bilan moslik haqida bo'ladi. Ya'ni review amalda ko'proq maintainability filtri.

Ikkinchi mahsulot - tarqalgan bilim. PR ni ikkinchi odam o'qiganida kod ustida kamida ikki kishi biladigan holat yuzaga keladi. Bitta modulni faqat bitta odam biladigan loyihada u odam ta'tilga chiqsa, o'zgarish tezligi nolga tushadi. Review shu xavfni arzon narxda kamaytiradi.

Uchinchi mahsulot - tekshirilgan qaror. Kodda ko'rinmaydigan qaror ham bor: nega shu yerga kesh qo'yildi, nega bu jadvalga yangi ustun qo'shildi, nega retry 3 marta. Review shu qarorni ovoz chiqarib aytishga majbur qiladi. Ko'p hollarda muallif izohga javob yozayotganda o'zi xatoni topadi.

| Mahsulot | Qanday ko'rinadi | O'lchash usuli | Yo'qolsa nima bo'ladi |
| --- | --- | --- | --- |
| Topilgan xato | Blocker izoh, keyin tuzatish | Review da topilgan va prodda topilgan xato nisbati | Xato prodga chiqadi, narxi 10-100 barobar oshadi |
| Tarqalgan bilim | Savol-javob, "bu nega shunday" | Modul bo'yicha bilimli odam soni | Bitta odamga bog'liqlik, ta'til xavfi |
| Tekshirilgan qaror | Alternativa muhokamasi, ADR havolasi | Qaror yozuvlari soni | Qaror yozilmaydi, olti oydan keyin hech kim sababini bilmaydi |
| Umumiy did | Bir xil uslub, takrorlanmaydigan izoh | Bir xil izohning takrorlanish soni | Har fayl boshqa qo'l bilan yozilgan kodga o'xshaydi |
| Egalik hissi | Reviewer ham javobgar | Incidentda kim keladi | "Mening kodim emas" madaniyati |

## 1.2 Review nimani topmaydi

Reviewer diffni o'qiydi, tizimni ishlatmaydi. Shu bitta jumla review ning chegarasini belgilaydi. Diffdan ko'rinmaydigan narsalar: real yuk ostidagi xulq, ma'lumotlar bazasidagi haqiqiy taqsimot, ishlab turgan tizimdagi konfiguratsiya, boshqa servisning javob vaqti, migratsiyaning real jadvalda qancha turishi.

Statistik kuzatuvlar klassik formal inspeksiyada xato topish darajasi taxminan 50-70 foiz atrofida ekanini ko'rsatadi, zamonaviy yengil PR review da esa bundan past. Ya'ni har uchta xatodan kamida bittasi review dan o'tadi. Shundan kelib chiqadigan amaliy xulosa: review ni oxirgi himoya chizig'i deb hisoblash xato. U ko'p qatlamli filtrning bir qatlami.

Yana bir chegara: reviewer muallifning taxminlarini meros qilib oladi. Agar muallif talabni noto'g'ri tushungan bo'lsa, kod shu noto'g'ri tushunishga mos holda toza yozilgan bo'ladi va review hech narsa sezmaydi. Shu sababli talabni tushunish review da emas, undan oldin tekshiriladi.

## 1.3 Filtrlarning mehnat taqsimoti

Har bir filtr boshqa sinf xatoni tutadi. Filtrlarni bir-birining o'rniga qo'ymaslik kerak.

| Filtr | Yaxshi tutadi | Tutmaydi | Narxi |
| --- | --- | --- | --- |
| Kompilyator va tur tizimi | Tur xatosi, yo'q metod | Mantiq xatosi | Nol |
| Linter va formatter | Uslub, oddiy shablon xato | Dizayn, kontekst | Juda arzon |
| Statik tahlil | Null yo'li, resurs oqishi, ma'lum shablonlar | Biznes mantiqi | Arzon, lekin shovqin beradi |
| Unit test | Mantiq va chegaraviy holat | Integratsiya, konfiguratsiya | O'rtacha |
| Integratsion test | Sxema, tranzaksiya, mapping | Yuk ostidagi xulq | Qimmat |
| Kod review | Niyat, dizayn, yo'q kod, xavf | Yuk, real ma'lumot | Qimmat odam vaqti |
| Canary va prod monitoring | Real xulq, real taqsimot | Hech narsa oldini olmaydi, faqat aytadi | Eng qimmat |

Shu jadvaldan asosiy qoida chiqadi: review da arzon filtr tutadigan narsani qo'lda tekshirish - vaqtni yoqish. Agar PR da formatlash haqida izoh yozilayotgan bo'lsa, demak formatter sozlanmagan. Reviewer ning vaqti faqat mashina tuta olmaydigan narsaga sarflanishi kerak: niyat, dizayn, xavf va kontekst.

## 1.4 Approve nimani anglatadi va nimani anglatmaydi

Approve - "men bu kodni o'qidim, tushundim va shu holda prodga chiqishiga qarshi emasman" degani. U "kodda xato yo'q" degani emas, chunki bunday kafolatni hech kim bera olmaydi. Jamoada shu farq kelishib olinmasa, incidentdan keyin "sen approve qilgansan" degan ayblov paydo bo'ladi.

Approve qachon berilishi kerakligiga Google ning review standarti bitta aniq qoida beradi va u shu hujjatlar ichida eng yuqori darajali printsip deb atalgan: reviewer CL ni **tizimning umumiy kod salomatligini aniq yaxshilagan** holatga kelgan zahoti approve qilishga moyil bo'lishi kerak, hatto CL mukammal bo'lmasa ham. Buning ortida oddiy haqiqat turadi: mukammal kod degan narsa yo'q, faqat yaxshiroq kod bor. Shuning uchun reviewer muallifdan approve dan oldin har bir mayda joyni silliqlashni talab qilmasligi kerak; maqsad mukammallik emas, uzluksiz yaxshilanish. Chegarasi ham bor va u aniq: umumiy kod salomatligini aniq **yomonlashtiradigan** o'zgarishni o'tkazishni hech narsa oqlamaydi.

Shu qoidadan bir amaliy vosita kelib chiqadi: muhim bo'lmagan izohni `Nit:` bilan boshlash. Bu muallifga "bu silliqlash, xohlasang e'tiborsiz qoldir" degan signal beradi va izohni aytmaslik bilan bajarishni talab qilish orasidagi uchinchi yo'lni ochadi. Sof o'rgatuvchi izoh ham shunday belgilanadi.

Kelishmovchilikda hujjat tartibni ham beradi: avval muallif va reviewer standartga tayanib kelishishga urinadi; qiyin bo'lsa yuzma-yuz yoki video suhbat (lekin natija keyingi o'quvchilar uchun PR izohiga yozilishi shart); bu ham yetmasa eskalatsiya, ya'ni jamoa muhokamasi, texnik yetakchi, kod egasi yoki menejer. Asosiysi: PR muallif bilan reviewer kelisha olmagani uchun turib qolmasligi kerak.

Qaror qanday tortilishi ham yozilgan: texnik fakt va ma'lumot shaxsiy xohishdan ustun; uslub masalasida style guide mutlaq hokim, unda yo'q narsa shaxsiy xohish va atrofdagi kodga mos bo'lishi yetarli; dizayn esa deyarli hech qachon shaxsiy xohish emas, u printsip bilan tortiladi, va muallif bir nechta yondashuv teng darajada to'g'ri ekanini ko'rsata olsa, tanlov muallifning.

Amalda foydali shakl: approve uch darajada bo'ladi (bu loyihaning o'z amaliyoti, standartning talabi emas). Birinchi daraja - "o'qidim, dizayn to'g'ri, detallarni tekshirmadim". Ikkinchi daraja - "satr-satr o'qidim, chegaraviy holatlarni ko'rdim". Uchinchi daraja - "lokalda ishga tushirdim, migratsiyani sinab ko'rdim". Yuqori xavfli PR uchun uchinchi daraja talab qilinadi, oddiy PR uchun birinchi yetarli. Darajani izohda bitta jumla bilan yozish reviewer ni ham, muallifni ham himoya qiladi.

```text
# Review xulosasi uchun shablon: nimani tekshirdim, nimani tekshirmadim.

Approve (daraja 2).
Tekshirdim: tranzaksiya chegarasi, null yo'llari, yangi indeks tanlovi,
            xato javobining shakli.
Tekshirmadim: migratsiyani real hajmdagi ma'lumotda ishga tushirmadim.
Xavf: backfill 12 mln qatorga tegadi, staging da vaqtini o'lchab ko'rishni
      so'raymiz. Qolgan qismiga qarshilik yo'q.
```

## 1.5 Review mas'uliyatni ko'chirmaydi

Review dan keyin ham kod muallifning kodi bo'lib qoladi. Bu nazariy gap emas, operatsion qoida: alert kelganda birinchi chaqiriladigan odam - o'zgarishni kiritgan odam. Agar jamoa "review o'tgandan keyin bu jamoaning kodi" qoidasini qabul qilsa, egalik yo'qoladi va sifat tushadi.

Teskari tomoni ham bor: reviewer "men faqat ko'rib qo'ydim" deb o'zini chetga ola olmaydi. To'g'ri muvozanat shunday: muallif to'g'riligi uchun javob beradi, reviewer o'zi ko'rgan va o'tkazib yuborgan narsa uchun javob beradi. Incident tahlilida ikkinchi savol har doim beriladi: nega review bu xatoni ko'rmadi, va checklistga nima qo'shiladi.

## 1.6 Review ning yon ta'siri: PR hajmini kichraytirishga majbur qilish

Review jarayoni mavjud bo'lgan jamoada PR lar o'z-o'zidan kichikroq bo'ladi, chunki katta PR uzoq kutadi. Bu review ning eng kam gapiriladigan foydasi: u o'zgarishni mayda bo'laklarga bo'lishga iqtisodiy sabab yaratadi. Mayda o'zgarish esa osonroq qaytariladi, osonroq test qilinadi va incidentda tezroq topiladi.

Shu sababli review vaqtini qisqartirish uchun qoidani "katta PR ni tezroq o'qing" emas, "katta PR ni bo'lib yuboring" deb qo'yish kerak. Birinchi variant reviewer ni charchatadi, ikkinchisi tizimni yaxshilaydi.

## 1.7 Qachon review foyda bermaydi

Uch holat bor. Birinchi - mashina generatsiya qilgan kod: OpenAPI dan chiqqan client, protobuf stublar, jOOQ klasslari. Ularni o'qish vaqtni yoqish, chunki ular o'zgarmaydi va qo'lda tuzatilmaydi. Review generatsiya sozlamasiga qaratiladi, chiqqan kodga emas.

Ikkinchi - formatlash va avtomatik refactoring: IDE butun paketdagi importlarni tartiblagan PR. Bunday diffni odam o'qiy olmaydi. Qoida: formatlash o'zgarishi alohida commit va alohida PR bo'ladi, va `.git-blame-ignore-revs` ga qo'shiladi.

Uchinchi - vendor va uchinchi tomon kodi repoga ko'chirilgan holat. Uni review qilish emas, bog'liqlik sifatida boshqarish kerak.

```bash
# Generated va vendor kodni review va blame dan chiqarib tashlash.
# 1) Diffda ko'rinmasin: GitHub linguist generated deb belgilaydi.
cat > .gitattributes <<'EOA'
src/main/generated/**      linguist-generated=true
**/*.pb.go                 linguist-generated=true
src/main/java/**/jooq/**   linguist-generated=true
EOA

# 2) Formatlash commitlari blame ni buzmasin.
git log --oneline --grep='^style: ' --format='%H' > .git-blame-ignore-revs
git config blame.ignoreRevsFile .git-blame-ignore-revs

# 3) Statik tahlil ham tegmasin: shovqin review vaqtini yeydi.
#    sonar-project.properties da:
#    sonar.exclusions=src/main/generated/**,**/jooq/**
```

## 1.8 Review arxitektura qaroridan keyin keladi

PR - arxitektura muhokamasi uchun eng yomon joy. Diff ochilganida qaror allaqachon qabul qilingan, kod yozilgan, muallif unga bir hafta sarflagan. Shu nuqtada "bu yondashuv noto'g'ri" deyish ikki tomon uchun ham qimmat.

Shu sababli yetuk jamoada katta o'zgarish ikki bosqichda ko'riladi: avval bir sahifali dizayn eskizi yoki ADR qoralamasi, keyin kod. Birinchi bosqichda qarorni o'zgartirish narxi nolga yaqin. Agar PR da arxitektura darajasidagi e'tiroz paydo bo'lsa, bu ko'pincha jarayon xatosi: dizayn muhokamasi o'tkazib yuborilgan.

Amaliy chegara: diffda 5 tadan ko'p yangi fayl yoki yangi tashqi bog'liqlik yoki yangi jadval paydo bo'lsa, bu PR dizayn muhokamasini talab qilgan o'zgarish. Review izohida shuni aytish o'rinli: keyingi marta eskizdan boshlaymiz.

## 1.9 Review maqsadini jamoada yozib qo'yish

Yozilmagan maqsad har kimda boshqacha bo'ladi. Natijada bir reviewer nomlash haqida uch izoh yozadi, boshqasi tranzaksiya chegarasini ko'rmaydi. Review siyosati repoda `REVIEW.md` sifatida turishi kerak va u uzun bo'lmasligi lozim: bir sahifa yetadi.

```markdown
<!-- REVIEW.md: jamoaning review shartnomasi. Bir sahifa, ko'p emas. -->
# Review shartnomasi

## Maqsad
1. Prodga chiqadigan xavfni kamaytirish.
2. Kod ustidan egalikni ikki kishiga tarqatish.
3. Qarorni yozib qoldirish.

## Reviewer vaqtini nimaga sarflaymiz
Niyat, dizayn, yo'q kod, xavf, ma'lumot to'g'riligi, orqaga moslik.

## Nimaga sarflamaymiz
Formatlash (spotless), import tartibi, uslub (checkstyle), generated kod.

## Izoh darajalari
- `blocker:` tuzatilmasa merge bo'lmaydi.
- `suggest:` yaxshilanish, muallif qaroriga qoldiriladi.
- `nit:` did, majburiy emas.
- `question:` javob kerak, tuzatish shart emas.

## SLA
Birinchi javob: 4 ish soati. Yuqori xavfli PR: ikki reviewer.

## Xavfli o'zgarishlar ro'yxati
Migratsiya, autentifikatsiya, to'lov, tashqi API shakli, pul va vaqt hisobi.
```

## 1.10 Review madaniyatini o'lchash uchun uchta savol

Birinchi savol: oxirgi oyda review da topilgan va prodga o'tib ketgan xatolar nisbati qanday. Ikkinchi savol: PR ning birinchi javobni kutish vaqti qancha. Uchinchi savol: izohlarning qanchasi mashina tuta oladigan narsa haqida. Uchinchi raqam yuqori bo'lsa, muammo odamda emas, instrumentda.

Bu uch raqam review ni did muhokamasidan muhandislik mavzusiga olib chiqadi. Keyingi bob shu iqtisodni raqamlarda ko'rsatadi.

## 1.11 Review ning oltita foydasi va eng muhimi qaysi

Google ning muhandislik kitobi review foydasini oltita band bilan sanaydi: kod to'g'riligini tekshirish, o'zgarish boshqa muhandis uchun tushunarli bo'lishini ta'minlash, kodbaza bo'ylab izchillikni majburlash, jamoaviy egalikni psixologik tarzda qo'llab-quvvatlash, bilim almashishni ochish va review ning o'zini tarixiy yozuv sifatida qoldirish.

Ro'yxatning eng kutilmagan jumlasi shu: kitob to'g'rilikni tekshirish Google da review dan olinadigan asosiy foyda emasligini ochiq aytadi. To'g'rilik tekshiruvi o'zgarish ishlashini ta'minlaydi, lekin kitob undan ko'proq ahamiyatni o'zgarishning tushunarli bo'lishiga va kodbaza o'sgani sari ma'noli qolishiga beradi. Shu sababli kitob review ni "panatseya ham, to'g'rilikning yagona tekshiruvi ham emas, ko'p qatlamli himoyaning bir elementi" deb qo'yadi va review natija berishi uchun mukammal bo'lishi shart emasligini aytadi.

[1.1](#11-review-ning-uchta-haqiqiy-mahsuloti) dagi jadvalda yo'q ikki band aynan shu sababli muhim.

| Kitobdagi foyda | Java/Spring loyihasida nima degani |
| --- | --- |
| Izchillik (consistency) | bir xil naqsh bir xil yozilsa, uni refactoring asbobi ham, keyingi o'quvchi ham taniydi; kitob izchil kodbazani avtomatik qayta yozish osonligi bilan oqlaydi |
| Tarixiy yozuv | PR izohi va tavsifi kodga qo'shilmagan sababni saqlaydi; keyin har kim naqsh qachon va nega kiritilganini topa oladi |

Tushunarlilik bo'yicha kitob alohida qoida beradi: dizayn tanlovida reviewer muallifga yon beradi, lekin tushunarlilik savolida "mijoz har doim haq" qoidasi ishlaydi. Hozir berilgan savol keyin ko'p marta takrorlanadi, shuning uchun har bir tushunarlilik savoli asosli deb olinadi. Bu mantiqni o'zgartirishni talab qilmaydi: ko'pincha javob kodni emas, tushuntirishni aniqlashtirish bo'ladi.

```java
// Kod to'g'ri: test o'tadi, mantiq ham to'g'ri. Review topilmasi boshqa:
// reviewer uch marta o'qib ham "7" nimani bildirishini tushunmadi.
public boolean isEligible(Account account) {
    return account.balance().signum() > 0 && account.ageInDays() > 7;
}

// Tushunarlilik savoliga javob: mantiq o'zgarmadi, nom va tur o'zgardi.
private static final Period TRIAL_PERIOD = Period.ofDays(7);

public boolean isEligible(Account account) {
    boolean funded = account.balance().signum() > 0;
    boolean pastTrial = account.ageInDays() > TRIAL_PERIOD.getDays();
    return funded && pastTrial;
}
```

Diqqat: Google da review deyarli har bir o'zgarish uchun majburiy va kitob buni kompaniyaning kam sonli umumiy majburiyatlaridan biri deb ataydi. Ayni paytda kitobning o'zi shu majburiyatning narxi borligini, yangi kodning kodbazaga kirishini sekinlashtirishini va ishlab chiqarishga chiqish vaqtiga ta'sir qilishini aytadi, bobning boshida esa review amaliyoti sanoat bo'ylab juda xilma-xil ekanini eslatadi. Ya'ni oltita foyda ro'yxatini ko'chirish mumkin, "hamma o'zgarish majburiy review dan o'tadi" qoidasini esa har jamoa o'z narxiga qarab qaror qiladi.

## 1.12 Xato topish usullarining o'lchangan samarasi

[1.2](#12-review-nimani-topmaydi) da berilgan "har uchta xatodan kamida bittasi review dan o'tadi" da'vosining o'lchovi Code Complete ning sifat boblarida turadi. Kitob xato topish usullarini bir jadvalda taqqoslaydi; quyida shu jadvalning review ga tegishli qatorlari.

| Usul | Eng past | Modal | Eng yuqori |
| --- | --- | --- | --- |
| Norasmiy dizayn review | 25% | 35% | 40% |
| Rasmiy dizayn inspeksiyasi | 45% | 55% | 65% |
| Norasmiy kod review | 20% | 25% | 35% |
| Rasmiy kod inspeksiyasi | 45% | 60% | 70% |
| Kodni o'zi tekshirish (desk-checking) | 20% | 40% | 60% |
| Unit test | 15% | 30% | 50% |
| Integratsion test | 25% | 35% | 40% |
| Tizim testi | 25% | 40% | 55% |

Kitob jadvaldan ikki xulosa chiqaradi. Birinchi: hech bir usulning modal darajasi 75 foizdan oshmaydi va usullar o'rtacha taxminan 40 foiz beradi. Ikkinchi: test ga tayangan odatiy tashkilot taxminan 85 foiz xatoni olib tashlaydi, usullarni kengroq birlashtirgan yetakchi tashkilotlar esa 95 foiz va undan yuqori darajaga chiqadi.

Shu jadvalning eng amaliy qatori birinchi va to'rtinchisining farqi. Odatdagi PR review kitobning tasnifida "norasmiy kod review", ya'ni modal 25 foiz; tayyorgarlik va tekshiruv ro'yxati bilan o'tkazilgan review esa "rasmiy kod inspeksiyasi", ya'ni modal 60 foiz. Farqni odamlar emas, tartib yaratadi. Boshqa bir jadvalda kitob uchta shaklni yonma-yon qo'yadi: juftlikda ishlash 40-60 foiz, rasmiy inspeksiya 45-70 foiz, norasmiy review va walk-through 20-40 foiz.

```text
# Kitobning modal darajalaridan hisoblangan kumulyativ filtr
# (kitob xuddi shu hisobni Extreme Programming uchun o'zi qiladi).
# Formula: 1 - (1-r1)(1-r2)...; raqamlar yuqoridagi jadvaldan.

Norasmiy PR review (0.25) + unit (0.30) + integratsion (0.35) + tizim (0.40)
  => 1 - 0.75*0.70*0.65*0.60 = 0.795   (taxminan 80 foiz)

Ro'yxatli review (0.60) + unit (0.30) + integratsion (0.35) + tizim (0.40)
  => 1 - 0.40*0.70*0.65*0.60 = 0.891   (taxminan 89 foiz)

Xulosa: faqat review tartibini o'zgartirish bilan o'tib ketadigan
xatolarning taxminan yarmi yo'qoladi. Yangi test turi qo'shilmaydi.
```

Kitob usullarni birlashtirish zarurligini alohida tajriba bilan ham asoslaydi. Myers o'tkazgan klassik tajribada bitta usul boshqasidan statistik jihatdan ustun chiqmagan, lekin odamlar topgan xatolar shunchalik har xil bo'lgan-ki, ikki usulning har qanday birikmasi, hatto bir xil usulni ishlatgan ikki mustaqil guruh ham, topilgan xatolar sonini qariyb ikki barobar oshirgan. Bir nechta tashkilotda o'tkazilgan kuzatuvlarda esa inspeksiyada topilgan xatolarning faqat taxminan 20 foizi bir nechta inspektor tomonidan topilgan. Kitob yo'nalishni ham ko'rsatadi: kodni o'qish interfeys xatolarini, funksional test esa boshqaruv oqimi xatolarini ko'proq topadi.

Shu uch fakt [1.3](#13-filtrlarning-mehnat-taqsimoti) dagi mehnat taqsimotining asosi: filtrlar bir-birining o'rnini bosmaydi, chunki ular boshqa sinf xatoni ko'radi, va ikkinchi reviewer ning foydasi takrorlashda emas, boshqa narsani ko'rishda.

## 1.13 Review mavjudligining oldini olish ta'siri

Review ning bir qismi reviewer diffni ochmasidan oldin ishlaydi. Code Complete buni birgalikda ishlash amaliyotlarining ikkilamchi ta'siri deb ataydi: odamlar ishi ko'rib chiqilishini bilsa, uni sinchiklab tekshiradi. Google kitobi shu ta'sirni batafsil ochadi: review ga yuborish uchun o'zgarishni yig'ish muallifni hammasi joyidami deb tekshirishga majbur qiladi, va "unit testlarning hammasi yo'q, lekin keyin yozaman" turidagi qisqa yo'llar aynan shu nuqtada yopiladi. Kitob jo'natishdan oldingi qisqa to'xtalishni o'zgarishni oxirgi marta o'qib chiqish uchun eng yaxshi payt deb ataydi.

Bundan amaliy xulosa chiqadi: review ni faqat topilgan xato bilan o'lchash uning qiymatini kam ko'rsatadi, chunki eng arzon topilma hisobga tushmaydi. Metrikalarning shu tuzog'i [42-bobda](42-review-metrikalari.md#422-zararli-metrikalar) ko'rilgan; o'zini tekshirish ro'yxati esa [44-bobda](44-shablonlar-checklistlar-va-reviewer.md#446-ozini-tekshirish-savollari).

Ikkinchi fakt: odam reviewer ko'radigan, lekin test hech qachon ko'rmaydigan xatolar sinfi bor. Code Complete Wiegers ning ro'yxatini keltiradi: noaniq xato xabari, yetarli bo'lmagan izoh, kodga qotib qolgan qiymat va birlashtirilishi kerak bo'lgan takroriy naqsh. Test ularning birortasini tutmaydi.

```java
// Test o'tadi: metod to'g'ri hisoblaydi. Review topadigan uch narsa:
// qotib qolgan qiymat, mijozga foydasiz xato xabari va takroriy naqsh.
@Service
public class PayoutService {

    public BigDecimal fee(BigDecimal amount) {
        if (amount.compareTo(BigDecimal.ZERO) <= 0) {
            throw new IllegalArgumentException("xato");          // xabar bo'sh
        }
        return amount.multiply(new BigDecimal("0.019"))          // qotib qolgan
                .setScale(2, RoundingMode.HALF_UP);
    }

    public BigDecimal refundFee(BigDecimal amount) {
        if (amount.compareTo(BigDecimal.ZERO) <= 0) {
            throw new IllegalArgumentException("xato");          // takror
        }
        return amount.multiply(new BigDecimal("0.019"))          // takror
                .setScale(2, RoundingMode.HALF_UP);
    }
}
```

Uchinchi fakt tartibning o'zi haqida. Code Complete Capers Jones ning kuzatuvini keltiradi: u o'rgangan loyihalardan 99 foiz va undan yuqori xato topish darajasiga chiqqanlarining hammasi rasmiy inspeksiya ishlatgan, 75 foizdan past darajada qolganlarining birortasi esa ishlatmagan. Bu sababiy bog'liqlikni isbotlamaydi, lekin yo'nalishni aniq ko'rsatadi: yuqori topish darajasi tasodifan kelmaydi, u tartibdan keladi.

## 1.14 Amalda qo'llash

- [ ] Jamoa bilan bir sahifali `REVIEW.md` yozing: maqsad, izoh darajalari, SLA va xavfli o'zgarishlar ro'yxati.
- [ ] Oxirgi 50 ta PR izohini uch sinfga ajratib sanang: xato, maintainability, mashina tuta oladigan narsa. Uchinchi sinf 20 foizdan ko'p bo'lsa, linter va formatter sozlamasini tuzating.
- [ ] `spotless` yoki `google-java-format` ni CI ga qo'ying, shundan keyin formatlash haqidagi izohni taqiqlang.
- [ ] `.gitattributes` da generated kodni `linguist-generated=true` qilib belgilang va statik tahlildan chiqaring.
- [ ] Formatlash commitlarini `.git-blame-ignore-revs` ga qo'shib, `blame.ignoreRevsFile` ni sozlang.
- [ ] Approve uchun uch darajali shablonni joriy qiling va yuqori xavfli PR uchun 3-darajani majburiy qilib qo'ying.
- [ ] Oxirgi uchta incidentni olib, har biri uchun "review nega ko'rmadi" savoliga javob yozing va checklistga bitta band qo'shing.
- [ ] Katta o'zgarishlar uchun dizayn eskizi bosqichini joriy qiling: 5 dan ko'p yangi fayl yoki yangi jadval bo'lsa, avval bir sahifa.

## Manbalar

- [Google, The Standard of Code Review](https://raw.githubusercontent.com/google/eng-practices/3bb3ec25b3b0199f4940b1aa75f0ac5c5753301c/review/reviewer/standard.md) - approve mezoni (kod salomatligini aniq yaxshilasa, mukammal bo'lmasa ham), mukammal kod yo'qligi, `Nit:` konvensiyasi, qaror tortish printsiplari va kelishmovchilikni hal qilish tartibi
- [Google, What to Look For in a Code Review](https://raw.githubusercontent.com/google/eng-practices/3bb3ec25b3b0199f4940b1aa75f0ac5c5753301c/review/reviewer/looking-for.md) - review nimaga qaraydi: dizayn, funksionallik, murakkablik, testlar, nomlash, izoh, uslub, hujjat
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 9-bob, "Code Review Benefits" - review foydasining oltita bandi; to'g'rilik tekshiruvi asosiy foyda emasligi; izchillik va tarixiy yozuv; tushunarlilik savolida "mijoz har doim haq"; review ko'p qatlamli himoyaning bir elementi va mukammal bo'lishi shart emasligi
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 9-bob, kirish va "Code Review Benefits" - review amaliyoti sanoat bo'ylab xilma-xil; Google da deyarli har o'zgarish uchun majburiy va bu majburiyatning tezlikka narxi bor
- Titus Winters, Tom Manshreck, Hyrum Wright, *Software Engineering at Google*, O'Reilly, 2020, 9-bob, "Psychological and Cultural Benefits" - review ga yig'ish muallifni tekshirishga majbur qilishi; "keyin yozaman" qisqa yo'lining yopilishi
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 20.3, jadval 20-2 "Defect-Detection Rates" (470-bet) - usullar bo'yicha eng past, modal va eng yuqori topish darajalari
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 20.3, "Percentage of Defects Detected" (470-471-betlar) - modal daraja 75 foizdan oshmasligi, o'rtacha taxminan 40 foiz; odatiy tashkilot 85 foiz, yetakchi tashkilot 95 foiz va yuqori
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 20.3 (471-bet) - Myers tajribasi: ikki usulning har qanday birikmasi topilmani qariyb ikki barobar oshiradi; inspeksiya xatolarining taxminan 20 foizi bir nechta inspektor tomonidan topilgan; kodni o'qish interfeys, funksional test boshqaruv xatolarini ko'proq topadi
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 20.3, jadval 20-3 (472-bet) - modal darajalardan kumulyativ samarani hisoblash usuli
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 21.4, jadval 21-1 (495-bet) - juftlikda ishlash 40-60 foiz, rasmiy inspeksiya 45-70 foiz, norasmiy review 20-40 foiz
- Steve McConnell, *Code Complete*, 2-nashr, Microsoft Press, 2004, 21.1 "Collaborative Construction Complements Other Quality-Assurance Techniques" (481-bet) - ishim ko'riladi deb bilgan odam o'zini sinchiklab tekshiradi; Wiegers ro'yxati (noaniq xato xabari, yetarli bo'lmagan izoh, qotib qolgan qiymat, takroriy naqsh); Capers Jones: 99 foiz topish darajasiga chiqqan loyihalarning hammasi rasmiy inspeksiya ishlatgan

---

[Mundarija](README.md) · [2. Review iqtisodi: xato narxi, navbat va PR hajmi &rarr;](02-review-iqtisodi-xato-narxi-navbat-va-pr.md)
