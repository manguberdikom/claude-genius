<!-- doc: clean-code | chapter: 44 | part: XII. Professional intizom -->

[Barcha hujjatlar](../../README.md) / [Toza kod qoidalari](README.md)

> Holat: AI yozgan, inson tekshirmagan.

# 44. "Yo'q" va "ha" deyish: majburiyat tili (Saying No and Saying Yes)

<details>
<summary>Bu bobdagi 6 bo'lim</summary>

- [44.1 "Yo'q" ni qachon va qanday aytish](#441-yoq-ni-qachon-va-qanday-aytish)
- [44.2 "Urinib ko'raman" nega yolg'on](#442-urinib-koraman-nega-yolgon)
- [44.3 Majburiyat tili: aytaman, qilaman, qachongacha](#443-majburiyat-tili-aytaman-qilaman-qachongacha)
- [44.4 Passiv tavakkalchilik va uning narxi](#444-passiv-tavakkalchilik-va-uning-narxi)
- [44.5 Jamoa bo'lib "yo'q" deyish](#445-jamoa-bolib-yoq-deyish)
- [44.6 Amalda qo'llash](#446-amalda-qollash)

</details>


Toza kodni buzadigan eng kuchli kuch - noto'g'ri majburiyat. "Juma kuniga bo'ladi" degan gap aytilgach, sifat birinchi qurbon bo'ladi. Bu bobda majburiyat tilining aniq qoidalari.

## 44.1 "Yo'q" ni qachon va qanday aytish

Professionalizmning eng aniq belgisi - bajarilmaydigan ishga "yo'q" deyish qobiliyati. "Yo'q" deyishdan qochish qisqa muddatda ziddiyatni yo'qotadi, uzoq muddatda ishonchni yo'qotadi.

"Yo'q" aytishning ishlaydigan shakli uchta elementdan iborat: aniq javob, sabab, va muqobil taklif.

```text
Yomon: "Harakat qilaman" (majburiyat yo'q, umid bor)
Yomon: "Mumkin emas" (sabab yo'q, muqobil yo'q)

Yaxshi: "Juma kuniga to'liq xususiyat chiqmaydi: migratsiya va bank
integratsiyasi ikki hafta oladi. Juma kuniga qaytarish qismini
chiqara olaman, bank integratsiyasi keyingi sprintda. Yoki
integratsiyani sinxron qilsak juma kuniga yetadi, lekin keyin
uni qayta yozish kerak bo'ladi."
```

Muhim nuqta: "yo'q" **maqsadga** emas, aniq muddat yoki qamrovga aytiladi. Maqsad doim muhokama qilinadi; fizika muhokama qilinmaydi.

## 44.2 "Urinib ko'raman" nega yolg'on

"Urinib ko'raman" eng zararli javob, chunki tinglovchi uni "ha" deb eshitadi, aytuvchi esa "yo'q" deb o'ylaydi. Natijada reja shu "ha" ga asoslanadi va u bajarilmaydi.

"Urinib ko'raman" ning ortida uch yashirin ma'no bo'lishi mumkin va ularning har birini oshkor aytish kerak:

| Yashirin ma'no | Oshkor shakl |
|---|---|
| "Yetmaydi, lekin aytishdan qo'rqaman" | "Bu muddatda bo'lmaydi; shuni taklif qilaman..." |
| "Qo'shimcha kuch sarflashga tayyorman" | "Agar X ni olib tashlasak, yetadi" |
| "Bilmayman" | "Aniqlashim kerak; ertaga javob beraman" |
| "Boshqa ishni to'xtatsam bo'ladi" | "Y ni keyinga surib qo'ysak, bo'ladi" |

## 44.3 Majburiyat tili: aytaman, qilaman, qachongacha

Haqiqiy majburiyat uch qismdan iborat va uchtasi ham bo'lishi shart: **kim**, **nima** va **qachongacha**. Biri yo'q bo'lsa, bu majburiyat emas, niyat.

| Shakl | Majburiyatmi |
|---|---|
| "Buni qilishimiz kerak" | yo'q (kim?) |
| "Men ko'rib chiqaman" | yo'q (qachon?) |
| "Tez orada tayyor bo'ladi" | yo'q (qachon?) |
| "Agar vaqt bo'lsa qilaman" | yo'q (shart) |
| "Seshanba kuni soat 12 gacha PR ochaman" | ha |
| "Bugun kech soat 6 ga qadar javob beraman" | ha |

Majburiyat olingach, uni bajarish professionalizmning asosiy sinovidir. Bajarilmasligi aniq bo'lsa - **darhol** xabar qilish kerak (45.6), oxirgi kungacha kutmaslik.

## 44.4 Passiv tavakkalchilik va uning narxi

Passiv tavakkalchilik - "menga aytilgani shu" deb aniq xato bo'lgan yo'lni davom ettirish. Bu javobgarlikni boshqaga o'tkazishga urinish va u ishlamaydi: tizim buzilganda hamma javob beradi.

Professional xatti-harakat: xavfni **yozib** xabar qilish, muqobil taklif qilish, qaror boshqa tomondan kelsa uni qayd etish va davom etish. "Rozi emasman, lekin bajaraman" qoidasi [arxitektor hujjatidagi](../architect/README.md) "rozi emasman, lekin bajaraman" qoidasida ko'rilgan.

```markdown
## Xavf haqida xabar (qisqa shakl)
**Qaror**: bank integratsiyasini sinxron qilish (muddat sababli).
**Xavf**: bank 5 sekund javob bersa, bizning p99 5 sekunddan oshadi va
checkout to'xtaydi. O'tgan chorakda bank 3 marta sekinlashgan.
**Taklif**: asinxron + holat so'rash (2 kun qo'shimcha).
**Qabul qilingan qaror**: sinqron, timeout 2s va circuit breaker bilan.
**Qayta ko'rish**: birinchi sekinlashishdan keyin yoki 2026-Q3.
```

## 44.5 Jamoa bo'lib "yo'q" deyish

Bitta odam "yo'q" deganda u to'siq bo'lib ko'rinadi; jamoa bir ovozdan "yo'q" deganda bu texnik haqiqat bo'lib eshitiladi. Shu sababli majburiyat haqidagi suhbatga jamoa bo'lib kirish ancha samarali.

Buning sharti: jamoa ichida kelishuv bo'lishi. Agar bir odam "bo'ladi" deb aytsa, qolganlarning "yo'q" i kuchini yo'qotadi. Shuning uchun baholash jamoa bo'lib qilinadi (45.3) va muddat haqida gapirishdan oldin ichki kelishuv bo'ladi.

## 44.6 Amalda qo'llash

- [ ] Keyingi hafta "urinib ko'raman" iborasini umuman ishlatmaslikni sinab ko'ring; har safar aniq shaklga aylantiring.
- [ ] Har bir majburiyatni kim/nima/qachongacha shaklida yozib boring va bajarilishini kuzating.
- [ ] 44.1 dagi uch elementli "yo'q" shaklini keyingi muddat suhbatida qo'llang.
- [ ] Rozi bo'lmagan qarorlar uchun 44.4 dagi xavf xabari shablonini ishlating.
- [ ] Muhokama qilinmaydigan sifat me'yorlari ro'yxatini jamoa bilan yozib, menejerga taqdim eting.
- [ ] Muddat haqidagi tashqi suhbatdan oldin jamoa ichida kelishuvga erishish qoidasini kiriting.
- [ ] Bajarilmaydigan majburiyat haqida darhol xabar qilish qoidasini kelishuvga yozing.
- [ ] Oxirgi uch kechikishni ko'rib chiqib, qaysi birida majburiyat aniq bo'lmaganini aniqlang.

---

[&larr; 43. Professional mas'uliyat](43-professional-masuliyat.md) · [Mundarija](README.md) · [45. Baholash, muddat va bosim &rarr;](45-baholash-muddat-va-bosim.md)
