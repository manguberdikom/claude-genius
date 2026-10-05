<!-- doc: clean-code | chapter: 45 | part: XII. Professional intizom -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

# 45. Baholash, muddat va bosim (Estimation, Deadlines and Pressure)

<details>
<summary>Bu bobdagi 8 bo'lim</summary>

- [45.1 Baho va majburiyat farqi](#451-baho-va-majburiyat-farqi)
- [45.2 Uch nuqtali baho va PERT](#452-uch-nuqtali-baho-va-pert)
- [45.3 Planning poker va kattalik birligi](#453-planning-poker-va-kattalik-birligi)
- [45.4 Katta ishni baholash va noaniqlik konusi](#454-katta-ishni-baholash-va-noaniqlik-konusi)
- [45.5 Bosim ostida intizomni saqlash](#455-bosim-ostida-intizomni-saqlash)
- [45.6 Kechikishni oshkor qilish va "90% tayyor" tuzog'i](#456-kechikishni-oshkor-qilish-va-90-tayyor-tuzogi)
- [45.7 Qamrovni qisqartirish yoki sifatni qisqartirish](#457-qamrovni-qisqartirish-yoki-sifatni-qisqartirish)
- [45.8 Amalda qo'llash](#458-amalda-qollash)

</details>


Noto'g'ri baho toza kodni buzadigan ikkinchi kuch: vaqt yetmaganda test, refaktoring va hujjat birinchi qurbon bo'ladi. Bu bobda baholashning amaliy texnikalari va bosim ostida intizomni saqlash.

## 45.1 Baho va majburiyat farqi

Eng ko'p chalkashlik shu ikki tushunchani aralashtirishdan keladi. **Baho** - ehtimollik taqsimoti, u xato bo'lishi mumkin va bu normal. **Majburiyat** - bajarilishi kerak bo'lgan gap (44.3), u xato bo'lmasligi kerak.

Professional bahoni majburiyatga aylantirmasligi kerak. "Taxminan uch kun" degan baho "uch kunda qilaman" degan majburiyatga aylantirilsa, keyinchalik ayblov tug'iladi.

| Savol | To'g'ri javob turi |
|---|---|
| "Qancha vaqt oladi?" | baho (taqsimot bilan) |
| "Juma kuniga bo'ladimi?" | majburiyat (ha/yo'q) |
| "Eng tez qachon?" | optimistik baho, oshkor belgilangan |
| "Kafolat berasizmi?" | faqat majburiyat bera olgan narsaga |

## 45.2 Uch nuqtali baho va PERT

Bitta son bilan baholash ma'lumot yo'qotadi. Uch nuqtali baho noaniqlikni ham uzatadi: optimistik (O), ehtimoliy (M), pessimistik (P).

Kutilgan qiymat va standart chetlanish:

```
μ = (O + 4M + P) / 6
σ = (P - O) / 6
```

Misol: migratsiya ishi uchun O = 2 kun, M = 4 kun, P = 10 kun.
μ = (2 + 16 + 10) / 6 = 4.67 kun; σ = (10 - 2) / 6 = 1.33 kun.
Ya'ni "taxminan 5 kun, 68% ehtimol bilan 3.3-6 kun oralig'ida".

Bir necha vazifa uchun kutilgan qiymatlar qo'shiladi, chetlanishlar esa kvadratik qo'shiladi: `σ_total = √(σ₁² + σ₂² + ...)`. Natijada ko'p kichik vazifaning jami bahosi bitta katta vazifadan **aniqroq** bo'ladi - bu ishni bo'lishning matematik asosi.

## 45.3 Planning poker va kattalik birligi

Jamoa bo'lib baholashning amaliy usuli: har kim mustaqil baho beradi, keyin farqlar muhokama qilinadi. Farqning o'zi eng qimmatli ma'lumot - u kimdir boshqa narsani tushunganini ko'rsatadi.

Mutlaq vaqt o'rniga nisbiy kattalik (story point) ishlatish ikki foyda beradi: odamlar nisbatni vaqtdan yaxshiroq baholaydi, va baho odamga bog'liq bo'lmaydi.

| Kattalik | Ma'nosi |
|---|---|
| 1 | aniq, bir-ikki soat, shubha yo'q |
| 2 | aniq, yarim kun |
| 3 | tushunarli, bir kun |
| 5 | bir necha noaniq joy bor |
| 8 | bo'lish kerak |
| 13+ | bo'lish **majburiy**, hali tushunilmagan |

## 45.4 Katta ishni baholash va noaniqlik konusi

Loyiha boshida baho 4 barobar xato bo'lishi mumkin; talab aniqlashgach 2 barobar; dizayn tugagach 1.5 barobar. Bu "noaniqlik konusi" va u baholashning tabiatini ko'rsatadi: bahoni aniqlashtirishning yagona yo'li - ma'lumot to'plash.

Amaliy natija: katta ish uchun bitta son bermaslik, balki **diapazon** berish va qayta ko'rish nuqtalarini belgilash. Spike ([arxitektor hujjatidagi](../architect/README.md) spike va prototip bo'limi) noaniqlikni kamaytirishning eng arzon vositasi: ikki kunlik tajriba ikki haftalik bahoni aniqlashtiradi.

## 45.5 Bosim ostida intizomni saqlash

Bosim paytida odatiy reaksiya - intizomni tashlash: testni o'tkazib yuborish, review ni qisqartirish, kodni shoshilib yozish. Bu deyarli har doim **sekinlashtiradi**, chunki xato topilib tuzatilishi ko'proq vaqt oladi.

| Bosim ostida | To'g'ri harakat |
|---|---|
| "Test yozishga vaqt yo'q" | aynan shu paytda test eng kerak |
| "Review ni o'tkazib yuboraylik" | review eng arzon xato to'suvchi |
| "Keyin tozalaymiz" | tozalash ishning qismi (1.3) |
| "Hamma kech qolib ishlasin" | charchoq xato ko'paytiradi (43.3) |
| "Parallel qilib tezlashtiramiz" | yangi odam qo'shish dastlab sekinlashtiradi |
| "Qamrovni qisqartiramiz" | **to'g'ri yechim** (45.7) |

## 45.6 Kechikishni oshkor qilish va "90% tayyor" tuzog'i

Kechikish haqida iloji boricha ertaroq xabar berish professionalizmning asosiy belgisi: ertaroq bilingan kechikish boshqarilishi mumkin, oxirgi kunda bilingani esa yo'q.

"90% tayyor" degan hisobot eng ko'p uchraydigan yashirin kechikish shakli: qolgan 10% odatda ishning yarmini oladi (integratsiya, xato tuzatish, chegaraviy holatlar). Yechim: foiz emas, **tugallangan qismlar** bilan hisobot berish.

```
Yomon: "90% tayyor"
Yaxshi: "Qaytarish oqimi tugadi va testlari o'tyapti. Bank integratsiyasi
         yozilgan, lekin sandbox'da hali sinalmagan. Xato oqimi va
         idempotentlik qolgan: taxminan 2 kun."
```

## 45.7 Qamrovni qisqartirish yoki sifatni qisqartirish

Vaqt yetmaganda uch o'lcham bor: muddat, qamrov va sifat. Birinchisi odatda qotirilgan. Shunda tanlov ikkisi orasida qoladi va javob har doim bir xil: **qamrov qisqartiriladi, sifat qisqartirilmaydi**.

Sababi iqtisodiy: qamrovni qisqartirish bir martalik narx, sifatni qisqartirish esa doimiy foiz to'lovi. Testsiz chiqarilgan xususiyat har bir keyingi o'zgarishda qimmat tushadi.

| Qisqartirish mumkin | Qisqartirish mumkin emas |
|---|---|
| Xususiyat soni | testlar |
| Qo'llanish holatlari (edge case) | xavfsizlik tekshiruvi |
| UI silliqligi | ma'lumot butunligi |
| Avtomatlashtirish darajasi | migratsiyaning orqaga mosligi |
| Hisobot va panel | xato bilan ishlash |
| Konfiguratsiya moslashuvchanligi | monitoring |

## 45.8 Amalda qo'llash

- [ ] Keyingi uchta bahoni uch nuqtali shaklda (O/M/P) berib, PERT bilan kutilgan qiymat va chetlanishni hisoblang.
- [ ] 8 va undan katta baholangan vazifalarni majburiy bo'lish qoidasini kiriting.
- [ ] Baho va majburiyatni og'zaki suhbatda ham oshkor ajratishni odat qiling.
- [ ] Katta ish boshida ikki kunlik spike ajratib, bahoni keyin aniqlashtiring.
- [ ] "Foiz tayyor" hisobotini tugallangan qismlar ro'yxatiga almashtiring.
- [ ] Bosim paytida qisqartirilmaydigan narsalar ro'yxatini (45.7) jamoa kelishuviga kiriting.
- [ ] Oxirgi uch loyihadagi baho va haqiqiy vaqtni taqqoslab, o'z koeffitsientingizni hisoblang.
- [ ] Kechikish haqida xabar berish muddatini ("bilgan kuni") kelishuvga yozing.

---

[&larr; 44. "Yo'q" va "ha" deyish: majburiyat tili](44-yoq-va-ha-deyish-majburiyat-tili.md) · [Mundarija](README.md) · [46. Vaqt, diqqat va mashq &rarr;](46-vaqt-diqqat-va-mashq.md)
