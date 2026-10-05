# A/B sinovi: manguberdi foyda beradimi

Bu papka sinovni **tayyorlaydi**. Sessiyalarni odam yurgizadi: bitta
sessiya ikki holatni xolis solishtira olmaydi, chunki u o'z ishini
baholaydi.

Savol bitta: `/manguberdi` orkestratori, budjet hisoblagichi va majburiy
`rules_for` natijani yaxshilaydimi, yoki faqat token va vaqt sarflaydimi.

## Sinov proyekti

| | |
|---|---|
| Repo | https://github.com/spring-projects/spring-petclinic |
| Commit | `500158f732419217507c7656904b8e6aa1bcc0d6` (`main`, 2026-10-05) |
| Spring Boot | 4.1.0 |
| Yig'uvchi | Maven (`./mvnw`), format darvozasi `spring-javaformat` bilan |

Har sessiya aynan shu commitdan boshlanadi:

```bash
git clone https://github.com/spring-projects/spring-petclinic pc
cd pc && git checkout 500158f732419217507c7656904b8e6aa1bcc0d6
```

Boshlang'ich holat o'lchangan: konteyner talab qilmaydigan testlar
**76/76 yashil**, taxminan 20 sekundda:

```bash
./mvnw -B test -Dtest='!MySqlIntegrationTests,!PostgresIntegrationTests,!PetClinicConcurrencyTests' -DfailIfNoSpecifiedTests=false
```

Testcontainers talab qiladigan uchta sinov (`MySqlIntegrationTests`,
`PostgresIntegrationTests`, `PetClinicConcurrencyTests`) hamma joyda
chiqarib tashlanadi: ularning yiqilishi holatga emas, muhitga bog'liq.

## Ikki holat

| Holat | Qanday |
|---|---|
| **A** | Oddiy Claude Code. `GENIUS_HOOKS=off`, `/manguberdi` chaqirilmaydi, aktyorlar qo'lda chaqirilmaydi. |
| **B** | `/manguberdi` sessiya boshida bir marta chaqiriladi, qolganini orkestrator o'zi qiladi. |

A holatida ham skilllar o'z-o'zidan ko'rinadi (ular Claude Code
mexanizmi), lekin hooklar o'chirilgan va orkestrator chaqirilmaydi.
Shuning uchun sinov o'lchayotgani aynan **orkestrator qatlami**:
aktyorlarga taqsimlash, budjet va majburiy `rules_for`.

Har vazifa har holatda **yangi sessiyada** bajariladi, ya'ni 10 vazifa
uchun 20 sessiya. Tartib almashinadi, chunki birinchi yurgizish
muammoni o'rganib qo'yadi:

| Vazifa | Birinchi | Ikkinchi |
|---|---|---|
| 1, 3, 5, 7, 9 | A | B |
| 2, 4, 6, 8, 10 | B | A |

Prompt matni ikkala holatda **aynan bir xil**: `vazifalar/` dagi
fayldan nusxalanadi, bir harf ham qo'shilmaydi.

## Vazifalar

| # | Fayl | Tur | Tekshiruv |
|---|---|---|---|
| 1 | [01-bug-ism-uzunligi.md](vazifalar/01-bug-ism-uzunligi.md) | bug | `PetValidatorTests` |
| 2 | [02-bug-bosh-ism.md](vazifalar/02-bug-bosh-ism.md) | bug | `PetControllerTests` |
| 3 | [03-bug-sahifalash.md](vazifalar/03-bug-sahifalash.md) | bug (jim) | yangi regressiya testi |
| 4 | [04-refaktoring-owner-controller.md](vazifalar/04-refaktoring-owner-controller.md) | refaktoring | butun to'plam |
| 5 | [05-refaktoring-getpet.md](vazifalar/05-refaktoring-getpet.md) | refaktoring | butun to'plam |
| 6 | [06-test-pettypeformatter.md](vazifalar/06-test-pettypeformatter.md) | test | yangi testlar |
| 7 | [07-test-addpet.md](vazifalar/07-test-addpet.md) | test | yangi testlar |
| 8 | [08-review-kesh.md](vazifalar/08-review-kesh.md) | review | 4 kiritilgan nuqson |
| 9 | [09-review-pul-va-sana.md](vazifalar/09-review-pul-va-sana.md) | review | 4 kiritilgan nuqson |
| 10 | [10-reja-tashrif-narxi.md](vazifalar/10-reja-tashrif-narxi.md) | reja | reja mezoni |

Uchta bug va ikki review diffi `vazifalar/diff/` da. Har biri shu
commitga toza qo'llanadi (`git apply --check` bilan tekshirilgan) va
kompilyatsiyadan hamda format darvozasidan o'tadi, ya'ni vazifa
nuqsonlar haqida bo'ladi, formatlash haqida emas.

Bug diffi **vazifa boshlanishidan oldin** qo'llanadi va bu haqda
modelga aytilmaydi: u buzilgan kodni oldida ko'radi, xuddi haqiqiy
ishdagidek.

## Nima o'lchanadi

Har sessiya uchun `natijalar.tsv` ga bitta qator:

| Ustun | Qanday olinadi |
|---|---|
| `vazifa` | 1-10 |
| `holat` | A yoki B |
| `muvaffaqiyat` | vazifa faylidagi qabul mezoni to'liq bajarildimi: 1 yoki 0 |
| `xato_topildi` | faqat review vazifalarida: kiritilgan 4 nuqsondan nechtasi topildi |
| `yolgon_topilma` | review da: mavjud bo'lmagan muammo deb aytilgan topilma soni |
| `token` | `python3 tools/usage.py` yoki `/cost` chiqishi (jami) |
| `daqiqa` | sessiya boshidan oxirigacha |
| `aralashuv` | foydalanuvchi tuzatish yoki yo'naltirish uchun yozgan xabar soni (dastlabki prompt sanalmaydi) |
| `kor_baho` | ko'r baholash natijasi, 1-5 |
| `izoh` | bir qator, ixtiyoriy |

Muvaffaqiyat **ikkilik**: qabul mezoni to'liq bajarilsa 1, aks holda 0.
"Deyarli" degan baho yo'q, aks holda natijani keyin talqin qilib
bo'ladi.

## Ko'r baholash

Diff sifatini baholash uchun **uchinchi** sessiya ishlatiladi: u A va B
ni bilmaydi.

1. Har vazifa uchun ikki diff `A.diff` va `B.diff` nomi bilan emas,
   tanga tashlab `1.diff` va `2.diff` nomi bilan saqlanadi. Moslik
   alohida faylda, baholovchiga berilmaydi.
2. Baholovchi sessiyaga faqat vazifa matni va ikki diff beriladi.
   Qo'llanma, hooklar va bu papka berilmaydi.
3. Baho 1-5: 1 = noto'g'ri yoki xavfli, 3 = ishlaydi lekin tozalash
   kerak, 5 = shunday qoldirib ketiladi.
4. Baholovchi qaysi diff qaysi holatdan ekanini **bilmasligi** kerak,
   shuning uchun unga `natijalar.tsv` ko'rsatilmaydi.

## Qaror qoidasi

Bu qoida sinovdan **OLDIN** yozilgan va natijaga qarab o'zgartirilmaydi.
Shu band commit tarixida sinov natijalaridan oldin turishi kerak.

B qoladi, agar **ikkisi ham** bajarilsa:

1. `muvaffaqiyat` yig'indisi bo'yicha B A dan **kamida 2 vazifa** ko'p
   yutadi (B >= A + 2);
2. B ning jami `token` i A dan **50% dan ko'p oshmaydi**
   (token_B <= 1.5 * token_A).

Aks holda quyidagilar olib tashlanadi: orkestrator (`/manguberdi` skilli
va `references/`), budjet hisoblagichi (`tools/budget.py` va uning
hooklari) va majburiy `rules_for` darvozasi (`check_code.py` dagi
zanjir sharti).

Qoladi: marshrut skilllari, `docs/` qo'llanmalari, `review` aktyori,
`tools/doc.sh` va qidiruv qatlami, `guard.py` ning katta bob to'sig'i.
Ular bu sinovda o'lchanmaydi, shuning uchun qaror ularga tegmaydi.

Review vazifalarida (8, 9) `xato_topildi` qo'shimcha dalil:
`yolgon_topilma` B da A dan ko'p bo'lsa, bu qarorga qarshi dalil bo'lib
hisobotda aytiladi, lekin yuqoridagi ikki shartni almashtirmaydi.

Natija qanday chiqsa ham shu README ga yoziladi: "B qoldi, chunki ..."
yoki "B olib tashlandi, chunki ...", raqamlari bilan.

## Nima o'lchanmaydi, ochiq aytilsin

- Uzoq muddatli foyda: memory va qoidalarning bir necha haftadagi ta'siri.
- Katta legacy loyihadagi xulq: petclinic kichik va toza.
- Odamning qulayligi: faqat aralashuv soni sanaladi, qanoat o'lchanmaydi.
- Bitta o'lchov takrorlanmaydi: har vazifa har holatda bir marta
  yurgiziladi, ya'ni tasodif ta'siri qoladi. Shuning uchun qaror
  qoidasi "kamida 2 vazifa" deb qo'yilgan, "bittaga ko'p" emas.
