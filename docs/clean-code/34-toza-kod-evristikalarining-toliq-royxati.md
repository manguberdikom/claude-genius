<!-- doc: clean-code | chapter: 34 | part: X. Hid katalogi va refaktoring harakatlari -->

[Toza kod yozuvchining qoidalari](../../README.md) / [Toza kod qoidalari](README.md)

# 34. Toza kod evristikalarining to'liq ro'yxati (Clean Code Heuristics)

<details>
<summary>Bu bobdagi 11 bo'lim</summary>

- [34.1 Izohlar (C1-C5)](#341-izohlar-c1-c5)
- [34.2 Muhit (E1-E2)](#342-muhit-e1-e2)
- [34.3 Funksiyalar (F1-F4)](#343-funksiyalar-f1-f4)
- [34.4 Umumiy evristikalar (G1-G12)](#344-umumiy-evristikalar-g1-g12)
- [34.5 Umumiy evristikalar (G13-G24)](#345-umumiy-evristikalar-g13-g24)
- [34.6 Umumiy evristikalar (G25-G36)](#346-umumiy-evristikalar-g25-g36)
- [34.7 Java ga xos evristikalar (J1-J3)](#347-java-ga-xos-evristikalar-j1-j3)
- [34.8 Nomlar (N1-N7)](#348-nomlar-n1-n7)
- [34.9 Testlar (T1-T9)](#349-testlar-t1-t9)
- [34.10 Evristikani review da ishlatish](#3410-evristikani-review-da-ishlatish)
- [34.11 Amalda qo'llash](#3411-amalda-qollash)

</details>


Bu bob toza kod evristikalarining klassik ro'yxatini to'liq beradi: izohlar (C), muhit (E), funksiyalar (F), umumiy (G), Java (J), nomlar (N) va testlar (T). Ro'yxat jadval shaklida, chunki uning vazifasi - review va o'z-o'zini tekshirish paytida tez ko'rib chiqish. Har bir satrda ushbu hujjatning yoki qardosh hujjatlarning tegishli bo'limiga havola bor.

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

## 34.10 Evristikani review da ishlatish

66 ta evristikani har bir review da ko'rib chiqish amalda mumkin emas. Ishlaydigan yondashuv - **kichik to'plam** bilan boshlash va vaqt o'tib ularni mashinaga topshirish.

| Bosqich | Nima qilinadi |
|---|---|
| 1 | Mashina tekshiradiganlarini CI ga ko'chirish (C5, G5, G9, G12, J1, F4) |
| 2 | Jamoaga eng ko'p tegishli 10 evristikani tanlab, review checklistiga kiritish |
| 3 | Har chorakda ro'yxatni ko'rib chiqish: qaysi evristika hech qachon ishlamadi |
| 4 | Takrorlangan review izohini qoidaga aylantirish (42.5) |
| 5 | Qolgan evristikalarni o'z-o'zini tekshirish uchun qoldirish ([49-bob](49-oz-ozini-baholash-toza-kod-yetukligi.md)) |

## 34.11 Amalda qo'llash

- [ ] 34-bobdagi 66 evristikani bir marta to'liq o'qib, kod bazasiga eng ko'p tegishli 10 tasini belgilang.
- [ ] Mashina tekshira oladigan evristikalarni Error Prone, Checkstyle va Sonar qoidalariga ko'chiring ([42-bob](42-statik-tahlil-va-avtomatik-qoidalar.md)).
- [ ] Review checklistiga tanlangan 10 evristikani qisqa shaklda kiriting (48.8).
- [ ] C1-C5 bo'yicha izohlarni bir marta to'liq ko'rib chiqib, tozalang.
- [ ] E1 va E2 ni tekshirish uchun yangi mashinada `git clone` dan keyin build va testni bir buyruq bilan ishga tushirib ko'ring.
- [ ] G25 bo'yicha kodni magic number uchun skanerlab, nomlangan konstantalar kiriting.
- [ ] N1-N7 bo'yicha eng ko'p o'zgaradigan 5 faylning nomlarini qayta ko'rib chiqing.
- [ ] T1-T9 bo'yicha test to'plamini baholab, eng sekin 10 testni ro'yxatlab tezlashtirish rejasini tuzing.

---

[&larr; 33. Kod hidlari katalogi II: sinf, ierarxiya, bog'liqlik](33-kod-hidlari-katalogi-ii-sinf-ierarxiya.md) · [Mundarija](README.md) · [35. Refaktoring harakatlari katalogi I: funksiya va o'zgaruvchi &rarr;](35-refaktoring-harakatlari-katalogi-i-funksiya.md)
