<!-- doc: architect | chapter: 41 | part: VII. Kengaytirilgan mavzular -->

[Barcha hujjatlar](../../README.md) / [Arxitektor miyasi](README.md)

> Holat: tekshirilgan (2026-10-19). Manbalar bob oxirida.

# 41. Ko'p region: kechikish, ma'lumot rezidentligi va failover (Multi-Region: Latency, Data Residency and Failover)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

- [41.1 Uchta turli sabab, uchta turli yechim](#411-uchta-turli-sabab-uchta-turli-yechim)
- [41.2 Kechikish byudjeti: RTT qayerdan keladi](#412-kechikish-byudjeti-rtt-qayerdan-keladi)
- [41.3 Sinxron replikatsiyaning narxi: har commit bitta RTT](#413-sinxron-replikatsiyaning-narxi-har-commit-bitta-rtt)
- [41.4 Aktiv-passiv va aktiv-aktiv orasidagi tanlov](#414-aktiv-passiv-va-aktiv-aktiv-orasidagi-tanlov)
- [41.5 Yozishni bitta regionga yig'ish, o'qishni tarqatish](#415-yozishni-bitta-regionga-yigish-oqishni-tarqatish)
- [41.6 Ma'lumot rezidentligi sxemaga qanday tushadi](#416-malumot-rezidentligi-sxemaga-qanday-tushadi)
- [41.7 Failover: RTO, RPO va split brain](#417-failover-rto-rpo-va-split-brain)
- [41.8 Kesh, sessiya va idempotentlik ko'p regionda](#418-kesh-sessiya-va-idempotentlik-kop-regionda)
- [41.9 Deploy va sxema migratsiyasi ko'p regionda](#419-deploy-va-sxema-migratsiyasi-kop-regionda)
- [41.10 Nimani ko'p region qilmaslik kerak](#4110-nimani-kop-region-qilmaslik-kerak)
- [41.11 Amalda qo'llash](#4111-amalda-qollash)

</details>


Ko'p region qarori ko'pincha noto'g'ri savoldan boshlanadi: "ikkinchi regionni qo'shamizmi". To'g'ri savol boshqa: "qaysi muammoni hal qilyapmiz". Uchta turli muammo bor va ularning yechimi ham, narxi ham turlicha. Ularni aralashtirish eng qimmat xatoga olib keladi: tizim ikki regionda ishlaydi, lekin na tezroq, na chidamli bo'ladi, faqat ikki marta qimmat va ikki marta murakkab bo'ladi.

## 41.1 Uchta turli sabab, uchta turli yechim

| Sabab | Nima talab qiladi | Nima talab qilmaydi |
|---|---|---|
| Foydalanuvchiga yaqinlik (kechikish) | o'qishni va statik kontentni chekkaga chiqarish | ikkinchi yozuv nuqtasi |
| Region yo'qolishiga chidamlilik | boshqa regionda tayyor nusxa va mashq qilingan failover | aktiv-aktiv yozish |
| Qonun talabi (rezidentlik) | ma'lumotni geografik bo'lib saqlash | butun tizimni ikkilantirish |

Birinchi sabab eng ko'p uchraydi va eng arzon hal bo'ladi: CDN, chekkadagi kesh va o'qish replikasi. Ikkinchisi tayyorlikni talab qiladi, aktiv-aktiv ni emas. Uchinchisi esa sxema va marshrutlash qarori, chidamlilik qarori emas.

## 41.2 Kechikish byudjeti: RTT qayerdan keladi

Ko'p region hisobida bitta raqam hal qiladi: ikki region orasidagi borib-kelish vaqti (RTT). U yorug'lik tezligi va tolaning yo'li bilan chegaralangan, ya'ni uni sozlama bilan kamaytirib bo'lmaydi. Shu sababli arxitektura qarori "nechta marta RTT to'laymiz" savoliga aylanadi.

Byudjet shunday hisoblanadi: foydalanuvchi so'rovining umumiy vaqti ichida regionlar orasidagi har bir safar bitta RTT qo'shadi. Bitta so'rov ichida uchta ketma-ket cross-region chaqiruv bo'lsa, u uch RTT to'laydi va bu vaqtni keshlash ham, pool ham qaytarmaydi. Shundan amaliy qoida chiqadi: so'rov yo'lida cross-region safar soni nolga yoki bittaga tushirilishi kerak, aks holda ko'p region kechikishni kamaytirmaydi, oshiradi.

Aniq raqamlar o'lchanadi, taxmin qilinmaydi: `ping` emas, ilovaning o'z yo'lida (TLS, pool, baza) o'lchangan vaqt kerak. [Napkin math](08-ishlash-va-resurs-hissi-napkin-math.md#811-amdahl-qonuni-ketma-ket-ulush-masshtablanishning-chegarasi) boblarida ko'rilgan tartib shu yerda ham amal qiladi: avval o'lchov, keyin tuzilma.

## 41.3 Sinxron replikatsiyaning narxi: har commit bitta RTT

PostgreSQL streaming replikatsiyasi sukut bo'yicha **asinxron**. Primary yiqilsa, commit bo'lgan, lekin standby ga yetib bormagan tranzaksiyalar yo'qoladi va yo'qotish hajmi failover paytidagi replikatsiya kechikishiga mutanosib.

Sinxron rejimda har bir yozuv tranzaksiyasining commiti WAL ning primary va standby diskiga yozilganini tasdiqlashini kutadi. Shundan kelib chiqadigan asosiy fakt: **kutishning minimal vaqti primary va standby orasidagi RTT ga teng**. Ya'ni standby boshqa regionda bo'lsa, har bir yozuv commiti o'sha RTT ni to'laydi.

```properties
# Sinxron standby: har commit RTT kutadi, ma'lumot yo'qolmaydi
synchronous_standby_names = 'standby_eu'
synchronous_commit = on

# Oraliq: standby xotirasiga yetgani yetarli (group-1-safe)
synchronous_commit = remote_write
```

Shu yerda ikki narsa muhim. Birinchisi: faqat tashqi (top-level) commit kutadi; o'qish tranzaksiyalari, rollback va subtransaction commiti kutmaydi. Ikkinchisi: `synchronous_commit` ning oraliq darajalari kutishni qisqartiradi, lekin chidamlilikni ham pasaytiradi, chunki standby diskiga yozilgani kafolatlanmaydi.

Amaliy xulosa: cross-region sinxron replikatsiya yozuv ko'p bo'lgan OLTP tizimida odatda to'lanmaydigan narx. Shu sababli ko'p region dizayni asinxron replikatsiya va ongli RPO bilan quriladi, yoki yozish bitta regionda qoladi (41.5).

## 41.4 Aktiv-passiv va aktiv-aktiv orasidagi tanlov

| Jihat | Aktiv-passiv | Aktiv-aktiv |
|---|---|---|
| Yozish nuqtasi | bitta region | ikki yoki undan ko'p |
| Konflikt | yo'q | bor, hal qilish qoidasi kerak |
| Failover | marshrutni almashtirish | yo'q, trafik qaytadan taqsimlanadi |
| RPO | asinxron lag ga teng | yechimga bog'liq |
| Murakkablik | o'rtacha | yuqori: identifikator, tartib, idempotentlik |

Aktiv-aktiv yozish ko'rinishdan jozibali, lekin u bitta masalani butun tizim bo'ylab tarqatadi: ikki regionda bir vaqtda o'zgargan bir qator bilan nima qilish. Yechimlar bor (oxirgi yozuv g'alaba qiladi, CRDT, regionga biriktirilgan egalik), lekin ularning har biri domen qaroriga aylanadi va u kodda ko'rinadi. Shu sababli standart tavsiya: aktiv-passivdan boshlash, aktiv-aktivga faqat o'lchangan ehtiyoj bilan o'tish.

"Oxirgi yozuv g'alaba qiladi" qoidasini timestamp bilan qurish esa alohida tuzoq: soat farqi (clock skew) tufayli u jim ma'lumot yo'qotadi ([soat ishonchsiz](32-tarmoq-timeout-va-integratsiya-haqiqati.md#3213-soat-ishonchsiz-monoton-soat-clock-skew-va-ttl-ga-tayanmaslik)).

## 41.5 Yozishni bitta regionga yig'ish, o'qishni tarqatish

Amalda eng ko'p ishlaydigan shakl shu: yozish bitta regionda (home region), o'qish esa foydalanuvchiga yaqin regionda. U aktiv-aktiv murakkabligini keltirmaydi va kechikishning katta qismini oladi, chunki ko'p tizimda o'qish yozishdan ancha ko'p.

Narxi ikki joyda ko'rinadi. Birinchisi: yozuv so'rovi uzoq regiondan kelsa, u RTT to'laydi va bu foydalanuvchiga seziladi. Ikkinchisi va nozigi: o'z yozuvini o'qish kafolati buziladi. Foydalanuvchi mahalliy replikadan o'qiydi, replika esa hali lag da, natijada u o'zi saqlagan ma'lumotni ko'rmaydi.

Yechim marshrutlashda: yozuvdan keyingi ma'lum vaqt ichida shu foydalanuvchining o'qishlari home regionga yoki primary ga yo'naltiriladi (sticky read). Buni sessiyada yoki cookie da belgilash mumkin. Replikatsiya lag va undan kelib chiqadigan xatolarning to'liq yozuvi [replikatsiya bobida](26-partitioning-replikatsiya-va-katta-hajm.md#268-oqishni-standby-ga-yonaltirish-va-replikatsiya-lag-dan-kelib-chiqadigan-xatolar).

## 41.6 Ma'lumot rezidentligi sxemaga qanday tushadi

Qonun talabi "ma'lumot shu davlatda qolsin" deganda, u arxitekturada uch qarorga aylanadi va ularni keyinga qoldirish qimmat.

Birinchisi: qaysi ma'lumot talabga tushadi. Odatda hammasi emas, faqat shaxsiy ma'lumot. Shu sababli sxema shaxsiy va noshaxsiy ma'lumotni ajratadigan bo'lishi kerak: identifikator va hisob-kitob hamma regionda, ism va manzil esa o'z regionida.

Ikkinchisi: ajratish qanday bajariladi. Ikki yo'l bor: regionga biriktirilgan alohida baza (har region o'z bazasiga yozadi) yoki bitta sxemada regionga bo'lingan jadval. Ikkinchisi arzonroq ko'rinadi, lekin u talabni bajarmaydi: ma'lumot fizik jihatdan bitta joyda qoladi.

Uchinchisi: identifikatorlar. Foydalanuvchi qaysi regionda ekani so'rovning boshida ma'lum bo'lishi kerak, aks holda marshrutlash uchun avval ma'lumotni qidirish kerak bo'ladi va bu cross-region safar qo'shadi. Shu sababli region belgisi identifikatorning o'ziga joylanadi yoki markaziy yengil katalogda saqlanadi.

To'rtinchisi: geografik bo'lish qaysi sababdan qilinayotgani. Newman geografik partitioning ning ikki haqiqiy foydasini sanaydi va ikkisi ham rezidentlikdan iborat emas. Birinchisi qonun talabi, ya'ni ma'lumot ma'lum yurisdiksiyadan chiqmasligi, masalan EU fuqarolari ma'lumotining EU ichida saqlanishi. Ikkinchisi operatsion: partitsiyalar yaratilishi texnik ishlarning ta'sirini va qamrovini kamaytiradi, yangilanishni partitsiya bo'yicha chiqarish mumkin bo'ladi, va aks holda to'xtash talab qiladigan amallar faqat bitta partitsiyaga ta'sir qiladi; geografik bo'lishda esa xizmat uzilishiga olib kelishi mumkin amallarni kunning eng kam ta'sirli vaqtida, masalan erta tongda bajarish mumkin bo'ladi, va bu vaqt har region uchun boshqacha.

Shu bilan birga kitob teskari tomonni ham aniq ko'rsatadi, va bu qaror mezoni bo'ladi: biznes yangi mamlakatlarga kengayib, bir nechta geografik hududni bitta tizimdan xizmat qilib samaradorlik olishni rejalashtirgan bo'lsa, geografik partitioning noto'g'ri tanlov. Asosiy muammo aniq, har yangi mamlakat uchun doimiy ravishda yangi partitsiya ko'tarish yangi mamlakatga chiqish xarajatini keskin oshiradi. Ya'ni mezon sodda: geografik bo'lish qonun yoki operatsion oyna uchun qilinadi, kengayish uchun qilinmaydi. Qonun talabi bo'lmagan holatda [41.1](#411-uchta-turli-sabab-uchta-turli-yechim) dagi uch sabab qayta ko'riladi.

## 41.7 Failover: RTO, RPO va split brain

Ikkinchi region chidamlilik uchun qo'yilgan bo'lsa, uning qiymati failover **mashq qilinganida** paydo bo'ladi. Mashq qilinmagan failover ishlamaydi: DNS TTL, ulanish satrlari, sertifikatlar, migratsiya holati va keshdagi eski ma'lumot hammasi real o'tishda chiqadi.

Ikki raqam oldindan kelishiladi: RTO (qancha vaqt ichida tiklanamiz) va RPO (qancha ma'lumot yo'qolishiga toqat qilamiz). Asinxron replikatsiyada RPO nolga teng bo'lmaydi va u lag ga bog'liq, shuning uchun RPO ni e'lon qilishdan oldin lag o'lchanadi va uning cho'qqisi olinadi.

Eng xavfli holat split brain: eski primary tirik, yangi primary ko'tarilgan va ikkisi ham yozuv qabul qilyapti. Himoyasi uchta: avtomatik failover uchun kvorum (ikki tugunli sxemada avtomatik failover xavfli), eski primary ni majburan to'xtatish (fencing), va yozuv nuqtasini bitta joyda tasdiqlash. Ma'lumot ikki tomonga oqib ketgandan keyin ularni birlashtirish qo'lda ish bo'lib qoladi.

## 41.8 Kesh, sessiya va idempotentlik ko'p regionda

Ko'p regionda uchta holat saqlovchi narsa muammo tug'diradi va ularning yechimi bir xil emas.

Kesh: har region o'z keshini yuritadi, invalidatsiya esa global bo'ladi. Shu sababli invalidatsiya xabari yo'qolsa, bir regionda eski qiymat qolib ketadi. Yechim TTL ni keshga chidamlilik chegarasi sifatida qoldirish: invalidatsiya tezlik uchun, TTL to'g'rilik uchun.

Sessiya: sticky session ko'p regionda failover ni buzadi, chunki region yo'qolganda sessiya ham yo'qoladi. Shu sababli sessiya holati tokenda (stateless) yoki regionlar orasida replikatsiya qilinadigan omborda saqlanadi.

Idempotentlik: qayta urinish ko'p regionda ikkinchi regionga tushishi mumkin, demak idempotentlik kaliti global bo'lishi kerak. Mahalliy saqlangan idempotentlik kaliti failover dan keyin ikki marta bajarishga yo'l qoldiradi; [idempotentlik kaliti](../patterns/07-api-dizayn-patternlari.md#79-idempotentlik-kaliti-idempotency-key) shu sababli umumiy omborda yashaydi.

## 41.9 Deploy va sxema migratsiyasi ko'p regionda

Bir region deploy qilinib, ikkinchisi eski versiyada turgan payt har relizda bo'ladi, ya'ni ikki versiya bir vaqtda ishlaydi. Bu holat bitta regionli tizimdagi rolling update bilan bir xil, lekin uzoqroq davom etadi va sxema migratsiyasiga qattiqroq talab qo'yadi.

Qoida o'zgarmaydi: migratsiya kengaytirish va qisqartirish bosqichlariga bo'linadi va har bosqich ikki versiyaga mos bo'lishi kerak ([sxema migratsiyasi](33-sxema-migratsiyasi-va-toxtashsiz-reliz.md)). Qo'shimcha talab esa shu: migratsiya qaysi regionda bajariladi va replikatsiya orqali ikkinchisiga qanday yetadi. Mantiqiy replikatsiyada DDL avtomatik ko'chmaydi, shuning uchun u har regionda alohida bajariladi va tartibi rejada yoziladi.

Reliz tartibi ham qaror: avval passiv region, keyin aktiv region. Shunda muammo chiqsa, u foydalanuvchi trafigi yo'q joyda chiqadi.

## 41.10 Nimani ko'p region qilmaslik kerak

Ko'p region narxini kamaytirishning eng samarali yo'li uni kichik qoldirish. Quyidagilar odatda bitta regionda qoladi va bu to'g'ri qaror.

- Admin panel va ichki asboblar: ular uchun kechikish muhim emas.
- Hisobot va analitika: ular allaqachon alohida yo'lga chiqarilgan (26.13).
- Batch va rejalashtirilgan joblar: ikki regionda bir vaqtda ishga tushsa, ikki marta bajariladi. Ularga qulf yoki bitta regionda ishga tushirish qoidasi kerak.
- Sxema migratsiyasi va ma'lumot tozalash: bitta joydan boshqariladi.
- Monitoring va alert: bitta joydan ko'rinadi, aks holda incident vaqtida ikki panelga qarash kerak bo'ladi.

## 41.11 Amalda qo'llash

- [ ] Ko'p region sababini yozib qo'ying: kechikish, chidamlilik yoki qonun talabi. Uchtasidan qaysi biri ekanini aytmasdan tuzilma tanlanmaydi.
- [ ] Bitta foydalanuvchi so'rovi yo'lida nechta cross-region safar borligini sanang va uni bittaga tushirish rejasini tuzing.
- [ ] Regionlar orasidagi RTT ni ilovaning o'z yo'lida o'lchab, uni yozuv so'rovining p95 byudjetiga qo'shib ko'ring.
- [ ] Replikatsiya lag ining cho'qqisini bir hafta o'lchab, RPO ni shu raqam bilan e'lon qiling.
- [ ] Failover ni mashq qilib ko'ring: DNS TTL, ulanish satri, sertifikat va migratsiya holatini ro'yxatga oling.
- [ ] Idempotentlik kalitlari va sessiya holati regionlar orasida umumiy ekanini tekshiring.
- [ ] Rejalashtirilgan joblarning ikki regionda bir vaqtda ishga tushmasligini ta'minlang.

## Manbalar

- [PostgreSQL 17, Synchronous Replication (high-availability.sgml)](https://raw.githubusercontent.com/postgres/postgres/REL_17_STABLE/doc/src/sgml/high-availability.sgml) - streaming replikatsiya sukut bo'yicha asinxron, yo'qotish lag ga mutanosib; sinxron rejimda kutishning minimal vaqti primary va standby orasidagi RTT
- [PostgreSQL 17, synchronous_commit darajalari (high-availability.sgml)](https://raw.githubusercontent.com/postgres/postgres/REL_17_STABLE/doc/src/sgml/high-availability.sgml) - `remote_write` group-1-safe ekani, faqat top-level commit kutishi, o'qish va rollback kutmasligi
- Martin Kleppmann, *Designing Data-Intensive Applications*, 5-bob - ko'p yetakchili replikatsiya, konflikt va "o'z yozuvini o'qish" kafolati
- Martin Kleppmann, *Designing Data-Intensive Applications*, 8-bob - soat farqi va "oxirgi yozuv g'alaba qiladi" qoidasining ma'lumot yo'qotishi
- Martin Kleppmann, *Designing Data-Intensive Applications*, 9-bob - kvorum, fencing va split brain
- Sam Newman, *Building Microservices: Designing Fine-Grained Systems*, 2-nashr, O'Reilly, 2021, 13-bob ("Data Partitioning" bo'limi) - geografik partitioning ning ikki foydasi (yurisdiksiyadan chiqmaslik talabi va texnik ishni partitsiya bo'yicha eng kam ta'sirli vaqtda bajarish) hamda biznes yangi mamlakatlarga kengayib bir tizimdan xizmat qilmoqchi bo'lsa har mamlakatga yangi partitsiya ochish xarajatni keskin oshirishi. Bu nashrning qo'limizdagi elektron nusxasida barqaror bet raqami yo'q, shuning uchun faqat bob va bo'lim nomi ko'rsatilgan

---

[&larr; 40. Qidiruv: PostgreSQL FTS chegarasi va alohida dvigatelga o'tish](40-qidiruv-postgresql-fts-va-alohida-dvigatel.md) · [Mundarija](README.md)
