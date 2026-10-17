<!-- doc: code-review | chapter: 44 | part: IX. Jarayon, madaniyat va o'lchov -->

[Barcha hujjatlar](../../README.md) / [Kod review](README.md)

> Holat: tekshirilmoqda. Da'volar hali manbaga solishtirilmoqda.

# 44. Shablonlar, checklistlar va reviewer yetukligi (Templates and Maturity)

<details>
<summary>Bu bobdagi 9 bo'lim</summary>

- [44.1 Universal review o'tishi: qisqa ro'yxat](#441-universal-review-otishi-qisqa-royxat)
- [44.2 Yuqori xavfli PR uchun qo'shimcha o'tish](#442-yuqori-xavfli-pr-uchun-qoshimcha-otish)
- [44.3 Review izohlari uchun tayyor iboralar](#443-review-izohlari-uchun-tayyor-iboralar)
- [44.4 Review xulosasi shablonlari](#444-review-xulosasi-shablonlari)
- [44.5 Reviewer yetukligi darajalari](#445-reviewer-yetukligi-darajalari)
- [44.6 O'zini tekshirish savollari](#446-ozini-tekshirish-savollari)
- [44.7 Loyihada review ni yo'lga qo'yishning birinchi 30 kuni](#447-loyihada-review-ni-yolga-qoyishning-birinchi-30-kuni)
- [44.8 Hujjatni qanday ishlatish](#448-hujjatni-qanday-ishlatish)
- [44.9 Amalda qo'llash](#449-amalda-qollash)

</details>


Bu bob hujjatning ma'lumotnoma qismi: tayyor checklistlar, izoh iboralari va o'zini baholash mezonlari. U boshidan oxirigacha o'qilishi uchun emas, review paytida ochib ishlatish uchun yozilgan.

## 44.1 Universal review o'tishi: qisqa ro'yxat

Har qanday PR uchun, xavf darajasidan qat'i nazar. Ro'yxat qancha vaqt
olishi PR hajmiga bog'liq, shuning uchun unga aniq daqiqa yozilmaydi.
Muhimi ro'yxat TO'LIQ O'QISHNI ALMASHTIRMASLIGI: Google ning qoidasi
qat'iy, review qilish uchun berilgan HAR SATRga qarash kerak, va kodni
o'qib bo'lmasa to'g'ri javob muallifdan tushuntirish so'rash.

```text
0.  Dizayn: bu o'zgarish shu kodbazaga tegishlimi, tizimning qolgan
    qismi bilan mos keladimi, hozir qo'shilishi to'g'rimi? Google
    ro'yxatda buni BIRINCHI o'ringa qo'yadi. Dizaynga savol bo'lsa,
    satrlarni o'qishdan oldin shuni yuborish kerak (44.4).
1.  PR tavsifi va tiket: niyat aniqmi? Birinchi qator buyruq shaklida
    nima qilinganini aytadimi, tavsifda "nega" bormi?
2.  Fayllar ro'yxati: kutilmagan fayl bormi? Migratsiya, konfiguratsiya,
    xavfsizlik, bog'liqlik o'zgardimi?
3.  Hajm: PR bitta o'zini o'zi to'ldiradigan o'zgarishmi? Qator soni
    yagona o'lchov emas, o'zgarish necha faylga tarqalgani ham hisobga
    olinadi (2.2). Bo'lish taklifi hajm emas, mazmun bo'yicha beriladi.
4.  Migratsiya va sxema (agar bor): qulf, orqaga moslik, qaytarish.
5.  Public API (agar o'zgargan): breaking change katalogi (37.1).
6.  Domen mantiqi: invariantlar, chegaraviy holatlar, holat o'tishlari.
7.  Yo'q kod ro'yxati: validatsiya, avtorizatsiya, timeout, indeks, test,
    log, idempotentlik, null, bo'sh to'plam, qaytarish rejasi (3.5).
8.  Beshta ssenariy: happy, chegara, ikki marta, ikki parallel,
    o'rtada yiqilish (3.6).
9.  Tranzaksiya chegarasi: ichida tashqi chaqiruv bormi?
10. So'rovlar soni: siklda I/O bormi? Hajm ma'lumotga bog'liqmi?
11. Testlar: assertion qiymatni tekshiradimi? Chegaralar va xato yo'llari?
12. Observability: xato bo'lsa qanday bilamiz?
13. O'chirilgan satrlar: olib tashlangan tekshiruv yoki test bormi?
14. Xulosa: nimani tekshirdim, nimani tekshirmadim, qolgan xavf.
```

## 44.2 Yuqori xavfli PR uchun qo'shimcha o'tish

```text
Migratsiya:
[ ] Qulf turi aniqlandi (25.1 jadvali)
[ ] `lock_timeout` qo'yilgan
[ ] Jadval hajmi tekshirildi (pg_stat_user_tables)
[ ] Rolling deploy da eski kod ishlaydi (25.3)
[ ] Backfill alohida va bo'laklangan
[ ] Qaytarish rejasi yozilgan
[ ] Real hajmga yaqin nusxada sinalgan, vaqti ma'lum

Xavfsizlik:
[ ] Yangi endpoint uchun avtorizatsiya qoidasi va test
[ ] Resurs egaligi tekshiriladi (IDOR, 30.1)
[ ] Foydalanuvchi ID si so'rovdan olinmaydi
[ ] Tashqi ma'lumot SQL, URL, fayl yo'li, buyruqqa tushmaydi
[ ] Logda va xato javobida maxfiy ma'lumot yo'q
[ ] Yangi bog'liqlik CVE tekshirildi

Pul va hisob:
[ ] `BigDecimal`/`Money`, `double` yo'q
[ ] Yaxlitlash qoidasi aniq va kelishilgan
[ ] Valyuta har summa bilan
[ ] Manfiy va chegaraviy qiymatlar tekshirilgan
[ ] Idempotentlik kaliti va unique constraint
[ ] Audit yozuvi qoladi

Konkurentlik:
[ ] Tekshir-keyin-yoz himoyalangan (unique yoki atomik UPDATE)
[ ] `@Version` yoki qulf kerakli joyda
[ ] Qulf tartibi barqaror
[ ] `@Scheduled` uchun taqsimlangan qulf
[ ] Pool va navbat chegaralangan
```

## 44.3 Review izohlari uchun tayyor iboralar

Pastdagi iboralar `blocker`, `suggest` va `praise` belgilaridan
foydalanadi. Belgilar to'plami bu hujjatda 41.3 da belgilangan
(beshtasi: `blocker`, `suggest`, `question`, `nit`, `praise`); shu
yerda faqat uchtasi uchraydi, chunki qolgan ikkitasi tayyor ibora
talab qilmaydi. Google ning o'z to'plami boshqacha nomlanadi (`Nit:`,
`Optional:` yoki `Consider:`, `FYI:`), lekin maqsad bir xil va manba
sababini ham aytadi: belgisiz izohni muallif hammasini majburiy deb
o'qishi mumkin. Arxitektura hujjatidagi 36.4 da yana bir, to'rt
belgili variant bor; jamoa BITTA to'plamni tanlab, uni PR shablonida
yozib qo'yishi kerak, uchtasini aralashtirmasligi kerak.

```text
# N+1
blocker: `{metod}` sikl ichida chaqirilgan, ya'ni {N} element uchun {N}
so'rov. {jadval} da hozir {hajm} qator. `JOIN FETCH` yoki ommaviy
yuklash (38.2) kerak. So'rov sonini test bilan qulflashni ham taklif
qilaman.

# Tranzaksiya ichida tashqi chaqiruv
blocker: `{servis}.{metod}` tranzaksiya ichida chaqirilgan. DB ulanishi
va qator qulfi tashqi javobni kutib turadi. Pool {N} ta - {N} parallel
so'rov butun ilovani to'xtatadi. Tranzaksiyani qisqartirish yoki outbox
(10.8) kerak.

# Poyga holati
blocker: `{tekshiruv}` va `{yozuv}` orasida boshqa so'rov o'zgartirishi
mumkin. READ COMMITTED da ikki parallel so'rov ikkisi ham o'tadi.
Himoya: `{jadval}` da unique indeks (eng ishonchli) yoki atomik UPDATE.

# IDOR
blocker: `{endpoint}` da `{id}` so'rovdan keladi va egalik tekshirilmaydi.
Har qanday autentifikatsiya qilingan foydalanuvchi boshqa odamning
ma'lumotini ko'radi. So'rovga egalik sharti qo'shish kerak, va topilmasa
404 qaytarish (403 emas - enumeratsiya).

# SQL injection
blocker: `{parametr}` to'g'ridan-to'g'ri SQL ga qo'shilgan. {Yo'l:
endpoint -> metod -> so'rov}. Ruxsat etilgan qiymatlar enum i kerak
(29.1), chunki ustun nomi va ORDER BY parametr bo'la olmaydi.

# Migratsiya qulfi
blocker: `{operatsiya}` `{jadval}` da ACCESS EXCLUSIVE qulf oladi.
Jadvalda {hajm} qator - bu taxminan {vaqt} to'liq to'xtash. Xavfsiz
ketma-ketlik: {qadamlar} (25.1).

# Yo'q test: YANGI ishlab chiqarish mantig'i uchun
blocker: `{holat}` qamralmagan. Test ishlab chiqarish kodi bilan BITTA
PR da keladi (34), favqulodda holatdan boshqa paytda keyinga
qoldirilmaydi. Nega muhim: {oqibat}. Bu `@CsvSource` ga bir qator
qo'shish bilan hal bo'ladi: `{namuna}`.

# Yo'q test: avvaldan qamralmagan yo'l uchun
suggest: `{holat}` qamralmagan va bu PR unga tegmaydi. Nega muhim:
{oqibat}. Shu PR da qo'shsak yaxshi bo'lardi, lekin ushlab turmaymiz.

# Yolg'on test
blocker: bu test `assertNotNull` bilan tugaydi, ya'ni `{metod}` ichidagi
har qanday o'zgarishda ham o'tadi. Kutilgan qiymat aniq yozilishi kerak.

# Kesh xavfsizligi
blocker: kesh kalitida foydalanuvchi identifikatori yo'q. Birinchi
so'rovning natijasi barcha foydalanuvchilarga qaytariladi.

# Timeout yo'q
blocker: `{mijoz}` da timeout sozlanmagan. Tashqi servis javob bermasa,
thread cheksiz kutadi va pool to'ladi. Ulanish uchun 500 ms, o'qish
uchun {byudjet} taklif qilaman (22.1).

# Breaking change
blocker: `{maydon}` o'zgarishi breaking change (37.1). Oxirgi 30 kunda
bu endpointni {mijozlar} ishlatgan. O'tish rejasi kerak: yangi maydon
qo'shish, ikkisini to'ldirish, eski maydonni {sana} da olib tashlash.

# Arxitektura: muammoni SHU PR keltirgan bo'lsa
blocker: `{klass}` `{paket}` da `{bog'liqlik}` ga bog'langan va bu
bog'liqlik shu PR da paydo bo'lgan. Oqibati: {1,2,3}. Alternativa:
{yechim}. Buni merge dan oldin tuzatish kerak: PR keltirgan murakkablik
"keyin" tozalanmaydi.

# Arxitektura: muammo AVVALDAN bor bo'lsa
suggest: `{klass}` `{paket}` da `{bog'liqlik}` ga bog'langan, lekin bu
shu PR ning ishi emas, u avvaldan shunday. Oqibati: {1,2,3}. Hajmi:
{taxmin}. Shu PR ni ushlab turmaymiz: tiket ochib, muallifga tayinlab
qo'yamiz, va kerak bo'lsa kodga tiket raqamli `TODO` qoldiramiz.

# Katta PR: birinchi javob bo'lishni so'rash
Bu PR da {N} satr mantiq {M} faylda o'zgargan. Shu hajmda satr-satr
review samarasiz (2.2), shuning uchun bo'lishni so'raymiz: {taklif
qilingan bo'laklar}. Birinchi bo'lakni bugun ko'rib chiqaman.

# Katta PR: bo'lish imkoni bo'lmasa
Bo'lish imkoni yo'q ekanini tushundim. Bu holatda umumiy dizayn
bo'yicha izohlarimni hozir yuboraman, chunki to'liq o'qishni kutsak PR
kunlab turadi: {dizayn izohlari}. Shundan keyin satr-satr o'qib
chiqaman.

# Katta PR: men faqat bir qismini o'qidim
Men {qism} ni o'qidim, {qolgan qism} ni o'qimadim, uni {ikkinchi
reviewer} ko'radi. Buni ochiq yozib qo'yaman, chunki "approve"
belgisining ma'nosi aks holda noto'g'ri tushuniladi. DIQQAT: bu shakl
faqat PR da bir nechta reviewer bo'lganda ishlaydi. Yolg'iz reviewer
sifatida "xavf nuqtalari bo'yicha o'qidim" deb approve berish mumkin
emas: unda approve belgisi hech narsani bildirmaydi.

# Maqtov
praise: bu yerda idempotentlik kaliti unique constraint bilan
himoyalangan - aynan shunday bo'lishi kerak. `FOR UPDATE SKIP LOCKED`
tanlovi ham to'g'ri: workerlar bir-birini kutmaydi.
```

## 44.4 Review xulosasi shablonlari

```text
# Approve
Approve ({loyihaning approve darajasi, 1.4 dagi shkala bo'yicha}).
Tekshirdim: {ro'yxat}.
Tekshirmadim: {ro'yxat}.
Qolgan xavf: {bor bo'lsa}. Yo'q bo'lsa: "sezilarli xavf ko'rmadim".

Tasdiqlash chegarasi: PR mukammal bo'lishi shart emas. Google ning
asosiy prinsipi shu, PR tizimning kod salomatligini aniq yaxshilaydigan
holatga kelgandan keyin tasdiqlanadi.

# Approve, lekin yopilmagan izohlar bilan (LGTM with comments)
Approve. Quyidagi izohlar ochiq qoldi, lekin ular merge ni
to'xtatmaydi, chunki {sabablardan bittasi}: (a) ularni o'zingiz
to'g'ri hal qilishingizga ishonaman; (b) ularni bajarish shart emas;
(v) ular mayda (import tartibi, yondagi xato yozilgan so'z).
Qaysi sababni nazarda tutganimni ataylab yozdim, aks holda "approve"
ning ma'nosi noaniq qoladi.

# O'zgarish so'rash
{N} blocker bor, qolgani ixtiyoriy.

Blocker lar:
1. {qisqa} - {satr havolasi}
2. {qisqa} - {satr havolasi}

Umumiy: yondashuv to'g'ri, {aniq joy} ni tuzatgandan keyin merge qilamiz.

# Dizayn savoli (detallarga tushmasdan)
Satrlarga izoh yozmadim, chunki bitta asosiy savol bor: {savol}.

Bu qaror o'zgarsa, {N} fayl ham o'zgaradi. Variantlar: {1}, {2}.
Men {tanlov} ni taklif qilaman, chunki {sabab}. Kelishib olgandan keyin
satr-satr o'qib chiqaman.

# "Keyin tozalaymiz" javobiga javob
Tushunaman, lekin tajriba shuni ko'rsatadi: PR yozilgandan keyin vaqt
o'tgani sayin tozalash ehtimoli kamayadi, va darhol qilinmasa amalda
hech qachon bo'lmaydi. Buning sababi mas'uliyatsizlik emas, ish
oqimida vazifaning yo'qolishi. Shu PR keltirgan murakkablikni hozir
tozalaymiz; PR ochib bergan AVVALGI muammo uchun esa tiket ochamiz va
uni o'zingizga tayinlaymiz.

# Kelishmovchilik cho'zilganda
Yozma izohlarda kelishuvga kelmayapmiz, shuning uchun {15 daqiqalik
qo'ngiroq} taklif qilaman. Bitta shart: natijani PR ga izoh qilib
yozib qo'yamiz, chunki review oynasida qolgan tushuntirish kelajakdagi
o'quvchiga yetib bormaydi. Agar qo'ngiroqdan keyin ham kelishmasak,
{texnik yetakchi yoki maintainer} ni jalb qilamiz. PR kelishmovchilik
tufayli turib qolmasligi kerak.

# Bo'lishni so'rash
Bu PR {N} satr. Review ni foydali qilish uchun bo'lishni so'raymiz:
1. {bo'lak 1} - mustaqil merge qilinadi
2. {bo'lak 2} - birinchisiga tayanadi
3. {bo'lak 3}

Birinchi bo'lakni bugun ko'rib chiqaman.
```

## 44.5 Reviewer yetukligi darajalari

Quyidagi beshta daraja shu hujjatning o'z modeli, u Google
qo'llanmasidan olinmagan va o'lchovga tayanmaydi. Uni jamoada
o'rgatish uchun til sifatida ishlatish mumkin, baho shkalasi sifatida
emas. Diqqat: bu yerdagi "daraja" 44.4 dagi approve darajasi (1.4) ga
umuman aloqasi yo'q, ikkisini aralashtirmaslik kerak.

| Daraja | Nimani ko'radi | Nimani hali ko'rmaydi |
| --- | --- | --- |
| 1. Uslub | Format, nomlash, uslub | Mantiq xatolari |
| 2. Mantiq | Null, chegara, shartlar, test holatlari | Tizim darajasidagi oqibatlar |
| 3. Tizim | Tranzaksiya, poyga, N+1, migratsiya qulfi, xavfsizlik | Uzoq muddatli oqibatlar |
| 4. Arxitektura | Chegara, bog'liqlik yo'nalishi, eroziya, API evolyutsiyasi | - |
| 5. Jarayon | Takrorlanadigan izohni qoidaga aylantirish, checklistni incidentlardan o'stirish, jamoani o'rgatish | - |

Yuqori darajaga o'tish mezoni - oldingi darajani avtomatlashtirish. Uslub izohlarini formatter ga, mantiq izohlarini statik tahlil va testga, tizim izohlarini ArchUnit va monitoringga ko'chirgan reviewer keyingi darajada ishlaydi.

## 44.6 O'zini tekshirish savollari

```text
Fikrlash va jarayon:
1.  Oxirgi review larimda (so'nggi ikki haftadagilarni oling)
    nechtasida uch o'qishni (niyat, mexanika, xavf) ongli ajratdim?
2.  Nechtasida "nimani tekshirmadim" ro'yxatini yozdim?
3.  Qaysi izohimni uchinchi marta yozdim va uni qoidaga aylantirdimmi?

Java va JVM:
4.  Diffda thread-safe emas holatni ko'ra olamanmi (singleton bean maydoni,
    statik kolleksiya, SimpleDateFormat)?
5.  Resurs oqishi va chegarasiz to'plamni hajm hisobi bilan ko'rsata olamanmi?
6.  `equals`/`hashCode`/`compareTo` nomuvofiqligini topa olamanmi?

Spring:
7.  Proxy ishlamaydigan holatlarni yoddan bilamanmi?
8.  Tranzaksiya ichidagi tashqi chaqiruvning to'rt oqibatini sanab bera olamanmi?
9.  `REQUIRED` ichida ushlangan istisno nega `UnexpectedRollbackException`
    berishini tushuntirib bera olamanmi?

PostgreSQL:
10. `ALTER TABLE` ning qaysi shakllari jadvalni qayta yozishini bilamanmi?
11. Diffdagi so'rovga qarab indeks ishlatiladimi yoki yo'qligini aytib bera olamanmi?
12. Write skew nima va uni qanday himoyalash kerakligini bilamanmi?

Xavfsizlik:
13. IDOR ni diffda ko'ra olamanmi va 404/403 tanlovini tushuntira olamanmi?
14. SQL da nima parametr bo'la olmasligini sanab bera olamanmi?
15. Tenant izolyatsiyasini majburlashning eng ishonchli yo'lini bilamanmi?

Testlar:
16. Test holatlari to'liqligini ekvivalentlik sinflari bilan baholay olamanmi?
17. Mutatsion fikrlashni qo'llab, testni aldab o'tish yo'lini topa olamanmi?
18. Yolg'on testni (assertion siz, mock ni tekshiradigan) tanib olamanmi?

Madaniyat:
19. Oxirgi izohlarimda oqibat va alternativa bormidi, yoki faqat baho?
20. Kelishmovchilikni ikki davradan oshirdimmi?
```

## 44.7 Loyihada review ni yo'lga qo'yishning birinchi 30 kuni

Quyidagi to'rt haftalik reja shu hujjatning taklifi, u o'lchovga
tayanmaydi: tartib mantiqiy (avval arzon avtomatika, keyin o'lchov,
oxirida madaniyat), lekin har bandning aniq vaqti jamoaga bog'liq.
Rejadagi yagona manbaga tayangan raqam javob vaqti: `REVIEW.md` ga
yoziladigan SLA uchun Google ning qoidasi bitta ish kuni maksimum,
va javob tez kelishi butun jarayonning tez tugashidan ham muhimroq.

```text
1-hafta: asos
[ ] `REVIEW.md` yozish: maqsad, izoh belgilari (44.3), javob vaqti
    chegarasi (Google: ko'pi bilan bitta ish kuni), xavfli yo'llar
[ ] `CODEOWNERS` yaratish
[ ] Branch protection: conversation resolution, stale approvals
[ ] `spotless` yoki formatter ni CI ga qo'yish

2-hafta: instrumentlar
[ ] ErrorProne ni yoqish (3-5 muhim qoida ERROR darajasida)
[ ] ArchUnit testlari: qatlam, sikl, inyeksiya, tranzaksiya chegarasi
[ ] `gitleaks` ni pre-commit va CI ga qo'shish
[ ] CI ni bosqichlarga bo'lish: tez signal alohida, sekin suite keyin

3-hafta: o'lchov va kontekst
[ ] Review metrikalarini bir marta o'lchash (kutish vaqti, hajm, taqsimot)
[ ] `GLOSSARY.md` va `CLAUDE.md` yozish
[ ] Eng katta 5 jadval hajmini `REVIEW.md` ga yozish
[ ] Performance byudjetini uchta asosiy endpoint uchun belgilash

4-hafta: checklist va madaniyat
[ ] PR shabloni (majburiy qism 6 band)
[ ] Xavf darajasini avtomatik belgilash
[ ] So'nggi incidentlarni `REVIEW-SMELLS.md` ga kiritish (hammasini
    emas, review topa olishi mumkin bo'lganlarini)
[ ] Jamoada bitta review ni birga tahlil qilish
```

## 44.8 Hujjatni qanday ishlatish

| Vaziyat | Qaysi bob |
| --- | --- |
| Review ni qanday boshlash kerakligini bilmayman | 3, 4, 44.1 |
| Sonar topadigan narsani oldin ko'rmoqchiman | 5 |
| Arxitektura buzilishini diffda ko'rmoqchiman | 6, 7 |
| Pattern kerak yoki kerak emasligini aniqlash | 10, 11 |
| Java tilidagi tuzoqlar | 14, 15, 16, 17 |
| Spring annotatsiyasi ishlamayapti | 18 |
| Tranzaksiya chegarasi to'g'rimi | 19 |
| Controller va DTO review | 20 |
| Konfiguratsiya o'zgarishi xavfli ko'rinadi | 21 |
| Tashqi integratsiya qo'shilyapti | 22 |
| N+1 va JPA muammolari | 23 |
| So'rov sekin ishlaydi | 24, 38 |
| Migratsiya PR i keldi | 25 |
| Ma'lumot to'g'riligi | 26 |
| Poyga holati bormi | 27 |
| Xavfsizlik review | 28-33 |
| Testlar yetarlimi | 34, 35, 36 |
| API o'zgarishi mijozni sindiradimi | 37 |
| Incidentda ko'r qolmaslik | 39 |
| Jarayon va madaniyat | 40, 41, 42 |
| AI yozgan kod | 43 |
| Tayyor iboralar va checklistlar | 44 |

## 44.9 Amalda qo'llash

- [ ] 15 daqiqalik universal o'tish ro'yxatini chop etib, ish joyingizda saqlang yoki IDE snippet qilib qo'ying.
- [ ] Yuqori xavfli PR checklistlarini `REVIEW.md` ga kiriting.
- [ ] Tayyor iboralarni jamoa wiki siga yoki GitHub saved replies ga qo'shing.
- [ ] Review xulosasi shablonlarini ishlatishni boshlang - ayniqsa "tekshirmadim" ro'yxatini.
- [ ] O'z yetuklik darajangizni belgilab, keyingi darajaga o'tish uchun bitta avtomatlashtirish ishini tanlang.
- [ ] 20 savolli o'zini tekshirish ro'yxatini bajarib, javob bera olmagan savollar bo'yicha tegishli bobni o'qing.
- [ ] 30 kunlik rejani jamoa bilan kelishib, birinchi haftadan boshlang.
- [ ] Har incidentdan keyin bu hujjatdagi tegishli checklistga bitta band qo'shing - eng qimmatli checklist loyihaning o'z tarixidan o'sadi.

## Manbalar

- Google, *Engineering Practices: The Standard of Code Review*
  ([https://github.com/google/eng-practices/blob/3bb3ec2/review/reviewer/standard.md](https://github.com/google/eng-practices/blob/3bb3ec2/review/reviewer/standard.md),
  commit `3bb3ec2`, CC BY 3.0) - 44.4 dagi tasdiqlash chegarasi (PR
  mukammal bo'lishi shart emas) va kelishmovchilikda eskalatsiya,
  hamda qarorni PR ga yozib qoldirish talabi.
- Google, *Engineering Practices: What to Look For in a Code Review*
  ([https://github.com/google/eng-practices/blob/3bb3ec2/review/reviewer/looking-for.md](https://github.com/google/eng-practices/blob/3bb3ec2/review/reviewer/looking-for.md),
  commit `3bb3ec2`, CC BY 3.0) - 44.1 dagi dizaynning birinchi o'rni va
  har satrni o'qish qoidasi, 44.3 dagi testning ishlab chiqarish kodi
  bilan bitta PR da kelishi.
- Google, *Engineering Practices: Speed of Code Reviews*
  ([https://github.com/google/eng-practices/blob/3bb3ec2/review/reviewer/speed.md](https://github.com/google/eng-practices/blob/3bb3ec2/review/reviewer/speed.md),
  commit `3bb3ec2`, CC BY 3.0) - 44.4 dagi izohlar bilan approve (LGTM
  with comments) va uning uch sharti, 44.7 dagi bitta ish kunlik javob
  chegarasi, katta PR uchun bo'lishni so'rash.
- Google, *Engineering Practices: How to Write Code Review Comments*
  ([https://github.com/google/eng-practices/blob/3bb3ec2/review/reviewer/comments.md](https://github.com/google/eng-practices/blob/3bb3ec2/review/reviewer/comments.md),
  commit `3bb3ec2`, CC BY 3.0) - 44.3 dagi izoh belgilari va belgisiz
  izohning majburiy deb o'qilishi, maqtov izohining sababi bilan
  kelishi.
- Google, *Engineering Practices: Handling Pushback in Code Reviews*
  ([https://github.com/google/eng-practices/blob/3bb3ec2/review/reviewer/pushback.md](https://github.com/google/eng-practices/blob/3bb3ec2/review/reviewer/pushback.md),
  commit `3bb3ec2`, CC BY 3.0) - 44.3 dagi arxitektura shablonining ikkiga
  bo'linishi (PR keltirgan murakkablik hozir tozalanadi, avvalgi
  muammo uchun tiket) va 44.4 dagi "keyin tozalaymiz" javobi.
- Google, *Engineering Practices: Small CLs*
  ([https://github.com/google/eng-practices/blob/3bb3ec2/review/developer/small-cls.md](https://github.com/google/eng-practices/blob/3bb3ec2/review/developer/small-cls.md),
  commit `3bb3ec2`, CC BY 3.0) - 44.1 dagi hajm bandi: qator soni yagona
  o'lchov emas, fayl soni ham hisobga olinadi.
- Google, *Engineering Practices: Writing Good CL Descriptions*
  ([https://github.com/google/eng-practices/blob/3bb3ec2/review/developer/cl-descriptions.md](https://github.com/google/eng-practices/blob/3bb3ec2/review/developer/cl-descriptions.md),
  commit `3bb3ec2`, CC BY 3.0) - 44.1 dagi tavsif bandi.

---

[&larr; 43. AI yozgan kodni review qilish va AI bilan review qilish](43-ai-yozgan-kodni-review-qilish-va-ai-bilan.md) · [Mundarija](README.md)
