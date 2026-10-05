<!-- doc: clean-code | chapter: 43 | part: XII. Professional intizom -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

# 43. Professional mas'uliyat (Professionalism)

<details>
<summary>Bu bobdagi 6 bo'lim</summary>

- [43.1 "Zarar qilmaslik": funksiyaga va tuzilishga](#431-zarar-qilmaslik-funksiyaga-va-tuzilishga)
- [43.2 O'z xatosi uchun javob berish](#432-oz-xatosi-uchun-javob-berish)
- [43.3 Ishga layoqat: charchagan holda kod yozmaslik](#433-ishga-layoqat-charchagan-holda-kod-yozmaslik)
- [43.4 Mijoz va ishlab chiquvchi maqsadlari to'qnashuvi](#434-mijoz-va-ishlab-chiquvchi-maqsadlari-toqnashuvi)
- [43.5 Kasbiy etika: sir, ma'lumot, xavfsizlik](#435-kasbiy-etika-sir-malumot-xavfsizlik)
- [43.6 Amalda qo'llash](#436-amalda-qollash)

</details>


Toza kod texnik qoidalar to'plami emas, kasbiy munosabat natijasi. Bu va keyingi to'rt bob shu munosabatni ko'rib chiqadi: javobgarlik, majburiyat, baholash, vaqt va birgalikda ishlash. Texnik yetakchilik va jamoada qaror tarqatish [arxitektor hujjatidagi](../architect/README.md) code review va texnik yetakchilik bo'limida, o'rganish va texnologiya tanlash esa [38-bobda](38-refaktoringni-xavfsiz-bajarish.md).

## 43.1 "Zarar qilmaslik": funksiyaga va tuzilishga

Professional ikki xil zarar qilmasligi kerak. **Funksiyaga zarar** - ishlaydigan narsani buzish: xato kiritish, regressiya, ma'lumot yo'qotish. **Tuzilishga zarar** - kod bazasini o'zgartirishga qarshilik qiladigan holga keltirish.

Birinchi zarar ko'rinadi va u haqida gapiradilar. Ikkinchi zarar ko'rinmaydi va shu sababli ko'proq uchraydi: har bir shoshilib yozilgan, testsiz, chalkash o'zgarish tuzilishga qarz qo'shadi. Oqibati keyin keladi - har bir yangi xususiyat sekinlashadi.

"Xato qilmayman" degan da'vo haqiqatga mos emas; to'g'ri da'vo boshqa: **xatolarim uchun javob beraman va ularni tez topadigan tizim quraman**. Shu tizimning qismlari: testlar, statik tahlil, monitoring, kichik qadamlar.

## 43.2 O'z xatosi uchun javob berish

Professionalizmning amaliy belgisi: xato chiqqanda uni tan olish, oqibatini bartaraf etish va takrorlanmasligi uchun tizim o'zgartirish. Uchinchi qism eng ko'p e'tibordan chetda qoladi.

| Xato turi | Noto'g'ri javob | To'g'ri javob |
|---|---|---|
| Production da xato | "test muhiti boshqa edi" | tuzatish + shu holatga test |
| Regressiya | "men bilmagan edim" | tuzatish + qamrovni oshirish |
| Noto'g'ri baho | "talab o'zgardi" | bahoni qayta ko'rish, sababni yozish |
| Noto'g'ri qaror | himoyalanish | qarorni qayta ko'rish (ADR yangilanishi) |
| Review da o'tkazib yuborilgan xato | "u yozgan" | jamoaviy javobgarlik, qoida qo'shish |

Incident tahlili va post-mortem mexanikasi [arxitektor hujjatidagi](../architect/README.md) incident va post-mortem bo'limida; bu yerda muhim nuqta: ayblov emas, tizim o'zgarishi.

## 43.3 Ishga layoqat: charchagan holda kod yozmaslik

Kod yozish aqliy diqqat talab qiladi va charchoq uning sifatini keskin pasaytiradi. Charchagan holda yozilgan kod odatda ikki marta qimmat tushadi: bir marta yozilganda, bir marta tuzatilganda.

Amaliy qoidalar: charchagan holda murakkab mantiq yozmaslik (o'rniga hujjat, review, oddiy vazifa); uzun kun oxirida muhim o'zgarishni merge qilmaslik; va juma kuni kech production ga chiqarmaslik (xato topilsa, hech kim yo'q).

## 43.4 Mijoz va ishlab chiquvchi maqsadlari to'qnashuvi

Mijoz tez va arzon natija xohlaydi; ishlab chiquvchi uzoq muddatli sifat uchun javob beradi. Bu to'qnashuv tabiiy va uni yashirish zarar keltiradi.

To'g'ri yondashuv: tanlovni **oshkor** qilish va qarorni narx bilan ifodalash. "Buni bir kunda qilish mumkin, lekin testsiz va keyin har bir o'zgarish ikki barobar sekin bo'ladi" - bu qaror mijoz bilan birga qabul qilinadi. Yashirin qaror esa (jim testsiz yozish) professionalizm emas.

Bir narsa muhokama qilinmaydi: **sifat me'yori**. Testsiz kod, tekshirilmagan xavfsizlik, ma'lumot yo'qotish xavfi - bular tanlov emas (44.1).

## 43.5 Kasbiy etika: sir, ma'lumot, xavfsizlik

Toza kodning etik o'lchovi bor va u uchta amaliy qoidaga qisqaradi.

**Ma'lumot**: foydalanuvchi ma'lumotiga faqat kerakli darajada tegish, log ga sezgir ma'lumot yozmaslik (29.8), production bazasidan ma'lumotni test muhitiga nusxalashdan oldin anonimlashtirish.

**Xavfsizlik**: topilgan zaiflikni yashirmaslik, hatto o'zingiz kiritgan bo'lsangiz ham; xavfsizlik tekshiruvini "vaqt yo'q" sababi bilan o'tkazib yubormaslik.

**Sir**: mijoz ma'lumoti, ichki arxitektura va kod - ular haqida tashqarida gapirmaslik; lekin texnik bilimni (pattern, yondashuv) ulashish normal.

## 43.6 Amalda qo'llash

- [ ] Oxirgi uch incidentni ko'rib chiqib, har biri uchun tizim o'zgarishi kiritilganini tekshiring.
- [ ] "Sifat me'yori muhokama qilinmaydi" ro'yxatini yozib, jamoa va menejer bilan kelishib oling.
- [ ] Charchagan holda merge va reliz qilmaslik qoidasini jamoa kelishuviga kiriting.
- [ ] Texnik qarz haqidagi suhbatni narx tilida olib borish uchun bitta misol tayyorlang (45.7).
- [ ] Production ma'lumotini test muhitiga ko'chirish tartibini (anonimlashtirish bilan) hujjatlashtiring.
- [ ] Log va `toString` larda sezgir ma'lumot yo'qligini bir marta to'liq audit qiling (29.8).
- [ ] Topilgan zaifliklarni xabar qilish kanalini (kimga, qanday) aniq belgilang.
- [ ] O'z xatolaringizni yozib boradigan shaxsiy jurnal yuritib, har chorakda naqshlarni ko'rib chiqing.

---

[&larr; 42. Statik tahlil va avtomatik qoidalar](42-statik-tahlil-va-avtomatik-qoidalar.md) · [Mundarija](README.md) · [44. "Yo'q" va "ha" deyish: majburiyat tili &rarr;](44-yoq-va-ha-deyish-majburiyat-tili.md)
