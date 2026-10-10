---
type: project
modified: 2026-10-10T16:00:00Z
---
# check_code da hali yo'q, Sonar topgan Java qoidalari

2026-10-10 da bir Java servisida server profili (Sonar way) shu qoidalarni topdi, `check_code.py` esa yozish paytida ushlamadi. Qoida qo'shilganda shu ro'yxatdan o'chiriladi.

- `java:S1700`: maydon nomi o'z sinfi nomi bilan bir xil (`class Position { String position; }`). Mexanik ushlanadi: sinf nomi va maydon nomini kichik harfda solishtirish. Tuzatish: maydonni qayta nomlash, JSON nomi va accessor lar `@JsonProperty` va qo'lda yozilgan getter/setter bilan saqlanadi.
- `java:S6548`: singleton (`static final X INSTANCE = new X()` va private konstruktor). Mexanik ushlanadi. Holatsiz sinfda tuzatish: `INSTANCE` ni olib tashlab, fabrika metodi yangi obyekt qaytaradi.
- `java:S1141`: `try` bloki ichida yana `try`. Blok chegarasini kuzatish kerak (qavs sanash). Tuzatish: ichki `try` ni private metodga chiqarish.
- `java:S135`: bitta siklda birdan ortiq `break` yoki `continue`. Sikl tanasi chegarasini kuzatish kerak, ichki sikl va `switch` dagi `break` sanalmaydi.
- `java:S2187`: nomi `Test` bilan tugagan tashqi sinfda test metodi yo'q, testlar faqat ichki sinflarda (masalan arxitektura qoidalari guruhlari). Tuzatish: tashqi sinf nomini `Test` siz qilish (`...Rules`); test filtrlari (`--tests`) yangi nomga moslanadi.
- `java:S1075`: qattiq yozilgan URI yo'li. Mexanik ushlash tavsiya etilmaydi: protokol yo'li konstantalarida noto'g'ri musbat ko'p.

Qo'shimcha kuzatuv:
- `java:S1133` va `java:S5738` deprecated ko'prik bilan birga keladi: API ni ikki bosqichda almashtirganda birinchi bosqichda kutilgan, ko'prik olib tashlanganda yo'qoladi. Ko'prik uchun `@SuppressWarnings` yoki `NOSONAR` qo'yilmaydi.
- `java:S1130` va `java:S5778` qoidalari bor, lekin shu holatlarni o'tkazib yuborgan: test metodida tashlanmaydigan `throws Exception` va `assertThatThrownBy` lambda sida ikki chaqiruv (`job(Duration.ofDays(-1))`). Qoida kengaytirilganda shu ikki shakl manfiy/musbat testga qo'shilsin.
