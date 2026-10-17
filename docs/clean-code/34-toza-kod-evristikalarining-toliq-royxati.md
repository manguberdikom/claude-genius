<!-- doc: clean-code | chapter: 34 | part: X. Hid katalogi va refaktoring harakatlari -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: tekshirilmoqda. Da'volar hali manbaga solishtirilmoqda.

# 34. Toza kod evristikalarining to'liq ro'yxati (Clean Code Heuristics)

<details>
<summary>Bu bobdagi 13 bo'lim</summary>

- [34.1 Izohlar (C1-C5)](#341-izohlar-c1-c5)
- [34.2 Muhit (E1-E2)](#342-muhit-e1-e2)
- [34.3 Funksiyalar (F1-F4)](#343-funksiyalar-f1-f4)
- [34.4 Umumiy evristikalar (G1-G12)](#344-umumiy-evristikalar-g1-g12)
- [34.5 Umumiy evristikalar (G13-G24)](#345-umumiy-evristikalar-g13-g24)
- [34.6 Umumiy evristikalar (G25-G36)](#346-umumiy-evristikalar-g25-g36)
- [34.7 Java ga xos evristikalar (J1-J3)](#347-java-ga-xos-evristikalar-j1-j3)
- [34.8 Nomlar (N1-N7)](#348-nomlar-n1-n7)
- [34.9 Testlar (T1-T9)](#349-testlar-t1-t9)
- [34.10 Kitobdagi nomlar va betlar: C, E, F va G1-G18](#3410-kitobdagi-nomlar-va-betlar-c-e-f-va-g1-g18)
- [34.11 Kitobdagi nomlar va betlar: G19-G36, J, N va T](#3411-kitobdagi-nomlar-va-betlar-g19-g36-j-n-va-t)
- [34.12 Evristikani review da ishlatish](#3412-evristikani-review-da-ishlatish)
- [34.13 Amalda qo'llash](#3413-amalda-qollash)

</details>


Bu bob toza kod evristikalarining klassik ro'yxatini to'liq beradi: izohlar (C), muhit (E), funksiyalar (F), umumiy (G), Java (J), nomlar (N) va testlar (T). Ro'yxat jadval shaklida, chunki uning vazifasi - review va o'z-o'zini tekshirish paytida tez ko'rib chiqish. Har bir satrda ushbu hujjatning yoki qardosh hujjatlarning tegishli bo'limiga havola bor. 34.10 va 34.11 esa shu 66 evristikaning kitobdagi aniq inglizcha nomi va betini beradi: iqtibos va review izohi uchun shu ikki jadval ishlatiladi.

## 34.1 Izohlar (C1-C5)

| Kod | Evristika | Mazmuni | Batafsil |
|---|---|---|---|
| C1 | Noo'rin ma'lumot | izohda o'zgarish tarixi, mualliflik, ticket tafsiloti | 9.5 |
| C2 | Eskirgan izoh | izoh koddan orqada qolgan | 9.3 |
| C3 | Ortiqcha izoh | kodni so'zma-so'z takrorlaydi | 9.2 |
| C4 | Yomon yozilgan izoh | g'o'ldirash, noaniq, uzun | 9.1, 9.9 |
| C5 | Izohga olingan kod | o'chirilishi kerak | 9.8 |

## 34.2 Muhit (E1-E2)

| Kod | Evristika | Mazmuni | Batafsil |
|---|---|---|---|
| E1 | Build bir qadamdan ko'p | `git clone` dan keyin bitta buyruq yetmaydi | 39.1 |
| E2 | Test bir qadamdan ko'p | testni ishga tushirish qo'lda sozlash talab qiladi | 39.2 |

## 34.3 Funksiyalar (F1-F4)

| Kod | Evristika | Mazmuni | Batafsil |
|---|---|---|---|
| F1 | Juda ko'p argument | uchdan ko'p argument asoslanishi kerak | 5.1 |
| F2 | Chiqish argumenti | argument orqali natija qaytarish | 5.5 |
| F3 | Flag argumenti | `boolean` parametr funksiyani ikkiga bo'ladi | 5.3 |
| F4 | O'lik funksiya | hech kim chaqirmaydi | 33.10 |

## 34.4 Umumiy evristikalar (G1-G12)

| Kod | Evristika | Mazmuni | Batafsil |
|---|---|---|---|
| G1 | Bir faylda bir necha til | Java ichida SQL, HTML, JSON aralash | 12.9, 28.6 |
| G2 | Aniq xatti-harakat amalga oshirilmagan | `Day.valueOf("Monday")` kutilgandek ishlamaydi | patternlar 26.22 |
| G3 | Chegarada noto'g'ri xatti-harakat | off-by-one, bo'sh to'plam, `null` | 6.7, 7.8 |
| G4 | Xavfsizlik mexanizmlari o'chirilgan | `@SuppressWarnings`, o'chirilgan test | 23.7, 30.9 |
| G5 | Takrorlanish | DRY buzilishi, uch turi bor | 32.2 |
| G6 | Noto'g'ri abstraksiya darajasidagi kod | past darajali tafsilot yuqori darajada | 4.2 |
| G7 | Bazaviy sinf vorisga bog'liq | ierarxiya teskari | 17.5, 33.14 |
| G8 | Haddan tashqari ko'p ma'lumot | keng public API | 33.8 |
| G9 | O'lik kod | erishilmaydigan shox, chaqirilmaydigan metod | 33.10 |
| G10 | Vertikal ajralish | e'lon va ishlatish orasida masofa | 11.5 |
| G11 | Izchilsizlik | bir narsa turli joyda turlicha | 33.9 |
| G12 | Keraksizlik (clutter) | bo'sh konstruktor, ishlatilmaydigan maydon | 33.10 |

## 34.5 Umumiy evristikalar (G13-G24)

| Kod | Evristika | Mazmuni | Batafsil |
|---|---|---|---|
| G13 | Sun'iy bog'liqlik | tegishli bo'lmagan narsalar birga | 33.11 |
| G14 | Begona ma'lumotga havas | metod boshqa sinf ma'lumotiga qiziqadi | patternlar 25.20 |
| G15 | Tanlov argumenti | `switch` ni argumentga ko'chirish | 5.4 |
| G16 | Yashirin niyat | zich, "aqlli" kod | 1.1, 9.10 |
| G17 | Noto'g'ri joylashgan javobgarlik | funksiya noto'g'ri sinfda | 33.12 |
| G18 | Noo'rin statik | statik metod polimorfizm talab qiladi | 33.13 |
| G19 | Tushuntiruvchi o'zgaruvchi ishlatish | oraliq natijaga nom berish | 6.1, [35-bob](35-refaktoring-harakatlari-katalogi-i-funksiya.md) |
| G20 | Funksiya nomi nima qilishini aytsin | nom va xatti-harakat mos kelishi | 3.9, 4.6 |
| G21 | Algoritmni tushunish | ishlagani yetarli emas, tushunish kerak | 41.2 |
| G22 | Mantiqiy bog'liqlikni fizik qilish | taxminni oshkor qilish | 6.9, [35-bob](35-refaktoring-harakatlari-katalogi-i-funksiya.md) |
| G23 | `if/else` o'rniga polimorfizm | turga qarab shoxlanish | 6.10, 32.7 |
| G24 | Standart konvensiyalarga rioya | jamoa uslubi, formatter | [13-bob](13-formatlashni-avtomatlashtirish-va-diff.md) |

## 34.6 Umumiy evristikalar (G25-G36)

| Kod | Evristika | Mazmuni | Batafsil |
|---|---|---|---|
| G25 | Magic number o'rniga konstanta | nomlangan konstanta | 3.4, patternlar 25.8 |
| G26 | Aniq bo'lish | `double` bilan pul, `null` siyosati, qulflash | 20.1, 18.7 |
| G27 | Konvensiyadan ustun tuzilish | tuzilish qoidani majburlasin | 17.4, 42.4 |
| G28 | Shartni inkapsulyatsiya qilish | shartni nomlash | 6.1 |
| G29 | Inkor shartdan qochish | ijobiy shart afzal | 6.2, 3.1 |
| G30 | Funksiya bitta ish qilsin | bo'linish sinovi | 4.2 |
| G31 | Yashirin vaqt bog'liqligi | tartib imzoda ko'rinmaydi | 6.9 |
| G32 | Tasodifiy bo'lmaslik | tuzilish sabab bilan tanlangan bo'lsin | 33.11 |
| G33 | Chegaraviy shartni inkapsulyatsiya | `i+1`, `<=` tarqalmasin | 6.7 |
| G34 | Bir darajadan pastga tushish | abstraksiya darajasi izchil | 4.2, patternlar 26.28 |
| G35 | Sozlanadigan ma'lumot yuqori darajada | konstanta yuqorida, chaqiruvda uzatiladi | 26.3 |
| G36 | O'tkinchi navigatsiyadan qochish | Demeter qonuni | 14.4, patternlar 26.15 |

## 34.7 Java ga xos evristikalar (J1-J3)

| Kod | Evristika | Mazmuni | Batafsil |
|---|---|---|---|
| J1 | Uzun import ro'yxatidan qochish | yulduzcha import haqida: **bu hujjat taqiqlaydi** | 12.7 |
| J2 | Konstantani voris olmaslik | constant interface anti-patterni | 17.8 |
| J3 | Konstanta emas, enum | enum xatti-harakat va tur xavfsizligi beradi | 3.5, 25.9 |

J1 bo'yicha izoh: klassik ro'yxat uzun import ro'yxatidan qochish uchun yulduzcha importni tavsiya qiladi. Zamonaviy amaliyot teskari: IDE importlarni o'zi boshqaradi va yulduzcha import nom konfliktlari bilan muammo tug'diradi (12.7). Shu sababli bu hujjatda J1 ning amaliy shakli - importlarni IDE va formatter boshqarishi, yulduzchani taqiqlash.

## 34.8 Nomlar (N1-N7)

| Kod | Evristika | Mazmuni | Batafsil |
|---|---|---|---|
| N1 | Tavsifiy nom tanlash | nom maqsadni ochib bersin | 2.1 |
| N2 | Abstraksiya darajasiga mos nom | nom implementatsiyani oshkor qilmasin | 2.13 |
| N3 | Standart nomenklaturadan foydalanish | pattern nomlari, konvensiyalar | 2.13, 3.6 |
| N4 | Noaniq nomlardan voz kechish | `doIt`, `handle`, `data` | 2.4, 32.1 |
| N5 | Katta qamrov uchun uzun nom | nom uzunligi qamrovga mutanosib | 2.15 |
| N6 | Kodlashdan voz kechish | Hungarian notation, prefikslar | 2.7 |
| N7 | Nom yon ta'sirni aytsin | `getOos()` aslida yaratadi | 3.9, patternlar 26.23 |

## 34.9 Testlar (T1-T9)

| Kod | Evristika | Mazmuni | Batafsil |
|---|---|---|---|
| T1 | Yetarlicha test yo'q | har bir shart va chegara qamralgan bo'lsin | [testlash qo'llanmasi](../testing/README.md) |
| T2 | Qamrov vositasidan foydalanish | qamralmagan shoxlarni ko'rsatadi | [SonarQube hujjatidagi](../sonarqube/README.md) branch qamrovi |
| T3 | Mayda testni e'tiborsiz qoldirmaslik | kichik test ham qoida hujjatlaydi | 30.1 |
| T4 | O'chirilgan testni tekshirish | `@Disabled` sababsiz qolmasin | 30.9 |
| T5 | Chegaraviy shartlarni sinash | oldin, chegarada, keyin | 7.8 |
| T6 | Xato atrofini to'liq sinash | bitta xato topilsa, atrofini ham sinash | 31.1 |
| T7 | Yiqilish naqshini o'rganish | yiqilgan testlar tartibi sababni ko'rsatadi | 41.3 |
| T8 | Qamrov naqshini o'rganish | qamralmagan qatorlar nimani bildiradi | [SonarQube hujjatidagi](../sonarqube/README.md) qamralmagan kod |
| T9 | Sekin testlarni tezlashtirish | sekin test ishga tushirilmaydi | 30.9, 39.7 |

## 34.10 Kitobdagi nomlar va betlar: C, E, F va G1-G18

34.1-34.9 jadvallari evristikalarning mazmunini o'zbekcha beradi va shu
korpusdagi batafsil bo'limga yo'naltiradi. Review izohida yoki ADR da
evristikaga havola qilish uchun kitobning **o'z nomi** va **beti** kerak
bo'ladi; shu ikki bo'lim aynan shu uchun turadi. Betlar *Clean Code*
ning 17-bobidan ("Smells and Heuristics", 285-314 bet), nomlar
sarlavhalardan aynan olingan.

Jami 66 evristika: C1-C5 (5), E1-E2 (2), F1-F4 (4), G1-G36 (36), J1-J3
(3), N1-N7 (7), T1-T9 (9). Ro'yxat kitobdagi tartibda to'liq.

| Kod | Kitobdagi nomi | Bet | Shu korpusda |
|---|---|---|---|
| C1 | Inappropriate Information | 286 | 34.1 |
| C2 | Obsolete Comment | 286 | 34.1 |
| C3 | Redundant Comment | 286 | 34.1 |
| C4 | Poorly Written Comment | 287 | 34.1 |
| C5 | Commented-Out Code | 287 | 34.1 |
| E1 | Build Requires More Than One Step | 287 | 34.2 |
| E2 | Tests Require More Than One Step | 287 | 34.2 |
| F1 | Too Many Arguments | 288 | 34.3 |
| F2 | Output Arguments | 288 | 34.3 |
| F3 | Flag Arguments | 288 | 34.3 |
| F4 | Dead Function | 288 | 34.3 |
| G1 | Multiple Languages in One Source File | 288 | 34.4 |
| G2 | Obvious Behavior Is Unimplemented | 288 | 34.4 |
| G3 | Incorrect Behavior at the Boundaries | 289 | 34.4 |
| G4 | Overridden Safeties | 289 | 34.4 |
| G5 | Duplication | 289 | 34.4 |
| G6 | Code at Wrong Level of Abstraction | 290 | 34.4 |
| G7 | Base Classes Depending on Their Derivatives | 291 | 34.4 |
| G8 | Too Much Information | 291 | 34.4 |
| G9 | Dead Code | 292 | 34.4 |
| G10 | Vertical Separation | 292 | 34.4 |
| G11 | Inconsistency | 292 | 34.4 |
| G12 | Clutter | 293 | 34.4 |
| G13 | Artificial Coupling | 293 | 34.5 |
| G14 | Feature Envy | 293 | 34.5 |
| G15 | Selector Arguments | 294 | 34.5 |
| G16 | Obscured Intent | 295 | 34.5 |
| G17 | Misplaced Responsibility | 295 | 34.5 |
| G18 | Inappropriate Static | 296 | 34.5 |

G5 va G9 nomi hid nomi bilan ustma-ust tushadi: *Refactoring* dagi
Duplicated Code (32.2) va Dead Code (33.10) bilan bir narsa haqida.
G7 va G14 ham ikki katalogda bor: G7 - 33.14, G14 - 33.18.

## 34.11 Kitobdagi nomlar va betlar: G19-G36, J, N va T

34.10 ning davomi. Nomlar va betlar *Clean Code* 17-bobidan.

| Kod | Kitobdagi nomi | Bet | Shu korpusda |
|---|---|---|---|
| G19 | Use Explanatory Variables | 296 | 34.5 |
| G20 | Function Names Should Say What They Do | 297 | 34.5 |
| G21 | Understand the Algorithm | 297 | 34.5 |
| G22 | Make Logical Dependencies Physical | 298 | 34.5 |
| G23 | Prefer Polymorphism to If/Else or Switch/Case | 299 | 34.5 |
| G24 | Follow Standard Conventions | 299 | 34.5 |
| G25 | Replace Magic Numbers with Named Constants | 300 | 34.6 |
| G26 | Be Precise | 301 | 34.6 |
| G27 | Structure over Convention | 301 | 34.6 |
| G28 | Encapsulate Conditionals | 301 | 34.6 |
| G29 | Avoid Negative Conditionals | 302 | 34.6 |
| G30 | Functions Should Do One Thing | 302 | 34.6 |
| G31 | Hidden Temporal Couplings | 302 | 34.6 |
| G32 | Don't Be Arbitrary | 303 | 34.6 |
| G33 | Encapsulate Boundary Conditions | 304 | 34.6 |
| G34 | Functions Should Descend Only One Level of Abstraction | 304 | 34.6 |
| G35 | Keep Configurable Data at High Levels | 306 | 34.6 |
| G36 | Avoid Transitive Navigation | 306 | 34.6 |
| J1 | Avoid Long Import Lists by Using Wildcards | 307 | 34.7 |
| J2 | Don't Inherit Constants | 307 | 34.7 |
| J3 | Constants versus Enums | 308 | 34.7 |
| N1 | Choose Descriptive Names | 309 | 34.8 |
| N2 | Choose Names at the Appropriate Level of Abstraction | 311 | 34.8 |
| N3 | Use Standard Nomenclature Where Possible | 311 | 34.8 |
| N4 | Unambiguous Names | 312 | 34.8 |
| N5 | Use Long Names for Long Scopes | 312 | 34.8 |
| N6 | Avoid Encodings | 312 | 34.8 |
| N7 | Names Should Describe Side-Effects | 313 | 34.8 |
| T1 | Insufficient Tests | 313 | 34.9 |
| T2 | Use a Coverage Tool! | 313 | 34.9 |
| T3 | Don't Skip Trivial Tests | 313 | 34.9 |
| T4 | An Ignored Test Is a Question about an Ambiguity | 313 | 34.9 |
| T5 | Test Boundary Conditions | 314 | 34.9 |
| T6 | Exhaustively Test Near Bugs | 314 | 34.9 |
| T7 | Patterns of Failure Are Revealing | 314 | 34.9 |
| T8 | Test Coverage Patterns Can Be Revealing | 314 | 34.9 |
| T9 | Tests Should Be Fast | 314 | 34.9 |

G19 va G23 nomlari refaktoring harakatlari nomiga yaqin, lekin ular
harakat emas, evristika: harakatlarning o'zi 35.3 (Extract Variable) va
37.4 (Replace Conditional with Polymorphism) da; G25 uchun nomlangan
konstanta qoidasi 3.4 da. T2 va T8 ning sarlavhasi kitobda undov
belgisi va to'liq gap shaklida, shuning uchun ular jadvalda shu holida
keltiriladi.

## 34.12 Evristikani review da ishlatish

66 ta evristikani har bir review da ko'rib chiqish amalda mumkin emas. Ishlaydigan yondashuv - **kichik to'plam** bilan boshlash va vaqt o'tib ularni mashinaga topshirish.

| Bosqich | Nima qilinadi |
|---|---|
| 1 | Mashina tekshiradiganlarini CI ga ko'chirish (C5, G5, G9, G12, J1, F4) |
| 2 | Jamoaga eng ko'p tegishli 10 evristikani tanlab, review checklistiga kiritish |
| 3 | Har chorakda ro'yxatni ko'rib chiqish: qaysi evristika hech qachon ishlamadi |
| 4 | Takrorlangan review izohini qoidaga aylantirish (42.5) |
| 5 | Qolgan evristikalarni o'z-o'zini tekshirish uchun qoldirish ([49-bob](49-oz-ozini-baholash-toza-kod-yetukligi.md)) |

## 34.13 Amalda qo'llash

- [ ] 34-bobdagi 66 evristikani bir marta to'liq o'qib, kod bazasiga eng ko'p tegishli 10 tasini belgilang.
- [ ] Mashina tekshira oladigan evristikalarni Error Prone, Checkstyle va Sonar qoidalariga ko'chiring ([42-bob](42-statik-tahlil-va-avtomatik-qoidalar.md)).
- [ ] Review checklistiga tanlangan 10 evristikani qisqa shaklda kiriting (48.8).
- [ ] C1-C5 bo'yicha izohlarni bir marta to'liq ko'rib chiqib, tozalang.
- [ ] E1 va E2 ni tekshirish uchun yangi mashinada `git clone` dan keyin build va testni bir buyruq bilan ishga tushirib ko'ring.
- [ ] G25 bo'yicha kodni magic number uchun skanerlab, nomlangan konstantalar kiriting.
- [ ] N1-N7 bo'yicha eng ko'p o'zgaradigan 5 faylning nomlarini qayta ko'rib chiqing.
- [ ] T1-T9 bo'yicha test to'plamini baholab, eng sekin 10 testni ro'yxatlab tezlashtirish rejasini tuzing.

## Manbalar

- Robert C. Martin, *Clean Code*, 17-bob - evristikalarning to'liq ro'yxati: C1-C5, E1-E2, F1-F4, G1-G36, J1-J3, N1-N7, T1-T9
- Robert C. Martin, *Clean Code*, C ilovasi - evristikalarning o'zaro havolalari
- Robert C. Martin, *Clean Code*, Prentice Hall, 2008, 17-bob "Smells
  and Heuristics" (285-314 bet) - 34.10 va 34.11 jadvallaridagi 66
  evristikaning kitobdagi aniq nomi va beti: C1-C5 (286-287), E1-E2
  (287), F1-F4 (288), G1-G36 (288-306), J1-J3 (307-308), N1-N7
  (309-313), T1-T9 (313-314)

---

[&larr; 33. Kod hidlari katalogi II: sinf, ierarxiya, bog'liqlik](33-kod-hidlari-katalogi-ii-sinf-ierarxiya.md) · [Mundarija](README.md) · [35. Refaktoring harakatlari katalogi I: funksiya va o'zgaruvchi &rarr;](35-refaktoring-harakatlari-katalogi-i-funksiya.md)
