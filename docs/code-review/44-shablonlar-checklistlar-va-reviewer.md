<!-- doc: code-review | chapter: 44 | part: IX. Jarayon, madaniyat va o'lchov -->

[Barcha hujjatlar](../../README.md) / [Kod review](README.md)

# 44. Shablonlar, checklistlar va reviewer yetukligi (Templates and Maturity)

<details>
<summary>Bu bobdagi 9 bo'lim</summary>

- [44.1 Universal review o'tishi: 15 daqiqalik ro'yxat](#441-universal-review-otishi-15-daqiqalik-royxat)
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

## 44.1 Universal review o'tishi: 15 daqiqalik ro'yxat

Har qanday PR uchun, xavf darajasidan qat'i nazar:

```text
1.  PR tavsifi va tiket: niyat aniqmi?
2.  Fayllar ro'yxati: kutilmagan fayl bormi? Migratsiya, konfiguratsiya,
    xavfsizlik, bog'liqlik o'zgardimi?
3.  Hajm: mantiq satrlari 400 dan oshdimi? (oshsa - bo'lish taklifi)
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

# Yo'q test
suggest: `{holat}` qamralmagan. Nega muhim: {oqibat}. Bu `@CsvSource` ga
bir qator qo'shish bilan hal bo'ladi: `{namuna}`.

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

# Arxitektura
suggest: `{klass}` `{paket}` da `{bog'liqlik}` ga bog'langan. Oqibati:
{1,2,3}. Alternativa: {yechim}. Hajmi: {taxmin}. Bu PR da katta bo'lsa,
tiket ochib keyingi sprintda yopsak bo'ladi.

# Katta PR
Bu PR da {N} satr mantiq o'zgargan. Shu hajmda satr-satr review samarasiz
(2.2) - men xavf nuqtalari bo'yicha o'qidim va buni ochiq aytaman.
Keyingi marta bo'lib yuborsak: {taklif qilingan bo'laklar}. Hozir
to'xtatmayman, lekin {aniq joy} ni alohida ko'rib chiqishni so'raymiz.

# Maqtov
praise: bu yerda idempotentlik kaliti unique constraint bilan
himoyalangan - aynan shunday bo'lishi kerak. `FOR UPDATE SKIP LOCKED`
tanlovi ham to'g'ri: workerlar bir-birini kutmaydi.
```

## 44.4 Review xulosasi shablonlari

```text
# Approve
Approve (daraja 2).
Tekshirdim: {ro'yxat}.
Tekshirmadim: {ro'yxat}.
Qolgan xavf: {bor bo'lsa}. Yo'q bo'lsa: "sezilarli xavf ko'rmadim".

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

# Bo'lishni so'rash
Bu PR {N} satr. Review ni foydali qilish uchun bo'lishni so'raymiz:
1. {bo'lak 1} - mustaqil merge qilinadi
2. {bo'lak 2} - birinchisiga tayanadi
3. {bo'lak 3}

Birinchi bo'lakni bugun ko'rib chiqaman.
```

## 44.5 Reviewer yetukligi darajalari

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
1.  Oxirgi 10 review da nechtasida uch o'qishni (niyat, mexanika, xavf)
    ongli ajratdim?
2.  Nechtasida "nimani tekshirmadim" ro'yxatini yozdim?
3.  Qaysi izohimni uchinchi marta yozdim va uni qoidaga aylantirdimmi?

Java va JVM:
4.  Diffda thread-safe emas holatni ko'ra olamanmi (singleton bean maydoni,
    statik kolleksiya, SimpleDateFormat)?
5.  Resurs oqishi va chegarasiz to'plamni hajm hisobi bilan ko'rsata olamanmi?
6.  `equals`/`hashCode`/`compareTo` nomuvofiqligini topa olamanmi?

Spring:
7.  Proxy ishlamaydigan to'rt holatni yoddan bilamanmi?
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

```text
1-hafta: asos
[ ] `REVIEW.md` yozish: maqsad, izoh darajalari, SLA, xavfli yo'llar
[ ] `CODEOWNERS` yaratish
[ ] Branch protection: conversation resolution, stale approvals
[ ] `spotless` yoki formatter ni CI ga qo'yish

2-hafta: instrumentlar
[ ] ErrorProne ni yoqish (3-5 muhim qoida ERROR darajasida)
[ ] ArchUnit testlari: qatlam, sikl, inyeksiya, tranzaksiya chegarasi
[ ] `gitleaks` ni pre-commit va CI ga qo'shish
[ ] CI ni bosqichlarga bo'lish: tez signal 2 daqiqada

3-hafta: o'lchov va kontekst
[ ] Review metrikalarini bir marta o'lchash (kutish vaqti, hajm, taqsimot)
[ ] `GLOSSARY.md` va `CLAUDE.md` yozish
[ ] Eng katta 5 jadval hajmini `REVIEW.md` ga yozish
[ ] Performance byudjetini uchta asosiy endpoint uchun belgilash

4-hafta: checklist va madaniyat
[ ] PR shabloni (majburiy qism 6 band)
[ ] Xavf darajasini avtomatik belgilash
[ ] Oxirgi 3 incidentni `REVIEW-SMELLS.md` ga kiritish
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

---

[&larr; 43. AI yozgan kodni review qilish va AI bilan review qilish](43-ai-yozgan-kodni-review-qilish-va-ai-bilan.md) · [Mundarija](README.md)
