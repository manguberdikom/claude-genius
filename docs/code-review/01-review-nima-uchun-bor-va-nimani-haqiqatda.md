<!-- doc: code-review | chapter: 1 | part: I. Review ning mohiyati va iqtisodi -->

[Barcha hujjatlar](../../README.md) / [Kod review](README.md)

# 1. Review nima uchun bor va nimani haqiqatda beradi (Why Review Exists)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

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
- [1.11 Amalda qo'llash](#111-amalda-qollash)

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

Amalda foydali shakl: approve uch darajada bo'ladi. Birinchi daraja - "o'qidim, dizayn to'g'ri, detallarni tekshirmadim". Ikkinchi daraja - "satr-satr o'qidim, chegaraviy holatlarni ko'rdim". Uchinchi daraja - "lokalda ishga tushirdim, migratsiyani sinab ko'rdim". Yuqori xavfli PR uchun uchinchi daraja talab qilinadi, oddiy PR uchun birinchi yetarli. Darajani izohda bitta jumla bilan yozish reviewer ni ham, muallifni ham himoya qiladi.

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

## 1.11 Amalda qo'llash

- [ ] Jamoa bilan bir sahifali `REVIEW.md` yozing: maqsad, izoh darajalari, SLA va xavfli o'zgarishlar ro'yxati.
- [ ] Oxirgi 50 ta PR izohini uch sinfga ajratib sanang: xato, maintainability, mashina tuta oladigan narsa. Uchinchi sinf 20 foizdan ko'p bo'lsa, linter va formatter sozlamasini tuzating.
- [ ] `spotless` yoki `google-java-format` ni CI ga qo'ying, shundan keyin formatlash haqidagi izohni taqiqlang.
- [ ] `.gitattributes` da generated kodni `linguist-generated=true` qilib belgilang va statik tahlildan chiqaring.
- [ ] Formatlash commitlarini `.git-blame-ignore-revs` ga qo'shib, `blame.ignoreRevsFile` ni sozlang.
- [ ] Approve uchun uch darajali shablonni joriy qiling va yuqori xavfli PR uchun 3-darajani majburiy qilib qo'ying.
- [ ] Oxirgi uchta incidentni olib, har biri uchun "review nega ko'rmadi" savoliga javob yozing va checklistga bitta band qo'shing.
- [ ] Katta o'zgarishlar uchun dizayn eskizi bosqichini joriy qiling: 5 dan ko'p yangi fayl yoki yangi jadval bo'lsa, avval bir sahifa.

---

[Mundarija](README.md) · [2. Review iqtisodi: xato narxi, navbat va PR hajmi &rarr;](02-review-iqtisodi-xato-narxi-navbat-va-pr.md)
