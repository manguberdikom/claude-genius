---
type: feedback
---

# Egalik identifikatorga bog'langan tokenlashtirishda identifikatorni o'zgartirish

Shifrlangan maydonlarni token bilan almashtiradigan tizimlarda egalik
ko'pincha shaxsning identifikatoridan hisoblanadi (`owner_ref =
blindIndex(identifikator)`). "O'zim ko'rishim mumkin" va "qarindoshim
ko'rishim mumkin" qarorlari aynan shu `owner_ref` ga tayanadi.

Shunday tizimda identifikatorni o'zgartirish oddiy ustun tahriri emas.
Identifikatorning o'zi qayta tokenlanadi, lekin **o'sha qatorning boshqa
tokenlari eski egalik ostida qolib ketadi**. Natijada egalik tekshiruvi
jimgina buziladi: xato chiqmaydi, odam shunchaki o'z ma'lumotini
ko'rolmay qoladi.

Buni idempotent tokenizator yashiradi: "qiymati hamon mos tokenni
saqlab qol" qoidasi aynan qayta mint qilish kerak bo'lgan tokenlarni
saqlab qoladi.

**Nega:** egalik qiymatdan emas, qiymat yozilgan paytdagi identifikatordan
kelib chiqadi. Qiymat o'zgarmasa ham egalik eskiradi.

**Qanday qo'llash:**

- Identifikator o'zgarganda o'sha qatorning barcha tokenlarini qayta mint
  qil, qiymati o'zgarmagan bo'lsa ham.
- Qiymat plaintexti saqlanmaydigan bo'lsa (tokenlashtirishdan keyin
  ustun `NULL` bo'ladi), qayta mint qilish uchun uni avval ombordan
  o'qish kerak. Bu o'qish tranzaksiyadan tashqarida bo'ladi.
- Omborda token bor-u o'qish `null` qaytarsa, buni "qiymat yo'q" yoki
  "qiymat o'zgargan" deb hisoblama. Fail-closed rad et: aks holda eski
  egalikdagi token jimgina saqlanib qoladi.
- Boshqa jadvallardagi, o'sha identifikator egaligida yozilgan qatorlarni
  ham sanab chiq. Ularni ko'chirmaslik ataylab qaror bo'lishi mumkin,
  lekin u ochiq aytilishi kerak.
- Identifikator bir necha servisda kalit bo'lsa, bir joyda o'zgartirish
  qolganlarida bir odamni ikki shaxsga ajratadi. Tarqatishni ish
  qamroviga kirit yoki ochiq cheklov deb yoz.
