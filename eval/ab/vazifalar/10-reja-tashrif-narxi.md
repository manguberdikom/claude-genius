# 10-vazifa: reja, tashrif narxi

**Tur:** reja (kod yozilmaydi). **Tartib:** B birinchi, A ikkinchi.

## Tayyorlash

```bash
git checkout 500158f732419217507c7656904b8e6aa1bcc0d6 -- src
```

## Prompt (ikkala holatda aynan bir xil)

```text
Tashrifga narx qo'shish kerak: veterinar tashrifni yozganda summani
kiritadi, ega ro'yxatida tashrif yonida summa va QQS bilan jami
ko'rinadi. Summalar hisobotga ham chiqadi. Kod yozmang, reja tuzing.
```

## Qabul mezoni

Rejada quyidagi yetti narsa **borligi** tekshiriladi. Har biri bor yoki
yo'q, yarim baho yo'q. `muvaffaqiyat` = 1, agar kamida beshtasi bor.

1. Pul turi ochiq tanlangan va sababi aytilgan (`BigDecimal` va
   scale/RoundingMode, yoki butun tiyin).
2. Sxema o'zgarishi: `visits` jadvaliga ustun, migratsiya fayli
   (loyihada `src/main/resources/db/` ichida) va orqaga qaytarish yo'li.
3. Mavjud ma'lumot: eski tashriflarda summa yo'q, ya'ni `NULL` yoki
   default qiymat qarori.
4. Validatsiya: manfiy summa va juda katta summa.
5. Test rejasi: qaysi daraja (unit, slice, integratsion) va qayerda.
6. Qadamlar mustaqil va har birining qabul mezoni buyruq bilan
   berilgan.
7. Qamrovdan tashqarida nima qolishi ochiq aytilgan (masalan valyuta,
   chegirma, hisobot formati).

## Tekshiruv

Qo'lda: reja faylini o'qib, yettita bandni belgilash. Reja fayli
`REJA.md` yoki `reja/*.md` bo'lishi mumkin, joyi muhim emas.

## Baholovchi uchun

Bu vazifa A uchun qasddan qulay emas: reja shabloni `rejalashtiruvchi`
aktyorida, A holatida esa u chaqirilmaydi. Shuning uchun natija
orkestratorning eng kuchli tomonini ko'rsatishi kutiladi. Agar A ham
yetti banddan beshtasini bersa, bu orkestrator foydasiga qarshi eng
kuchli dalil.
