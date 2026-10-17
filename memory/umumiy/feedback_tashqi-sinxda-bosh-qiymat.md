---
type: feedback
---

# Tashqi manbadan sinxronizatsiyada bo'sh qiymat mavjudini o'chirmasin

Tashqi registr yoki xizmatdan ma'lumot tortib, uni mavjud qatorga
yozadigan kod odatda shunday yoziladi:

```java
target.setName(incoming.name());
target.setBirthDate(incoming.birthDate());
```

Tashqi manba biror maydonni bermasa (`null` yoki bo'sh), bu kod qo'lda
kiritilgan qiymatni o'chirib yuboradi. Foydalanuvchi uchun bu "yangilash
tugmasini bosdim, ma'lumotim yo'qoldi" bo'lib ko'rinadi, log da esa
hech qanday xato yo'q.

Eng yashirin ko'rinishi: ko'rsatish ustuni uchun qo'yilgan placeholder
("Noma'lum", "N/A"). U yangi qator uchun o'ylanadi, lekin moslashgan
mavjud qatorga ham qo'llanib, haqiqiy ismni placeholder bilan
almashtiradi.

**Nega:** "manba bermadi" va "manba bo'sh deb aytdi" ikki xil narsa,
lekin `null` ikkalasini bir xil ko'rsatadi. Sinxronizatsiya kodi
birinchisini ikkinchisi deb o'qiydi.

**Qanday qo'llash:**

- Qoidani bitta joyda ifoda qil: manba bermagan qiymat saqlanganni
  o'chirmaydi. Uchta `if` ni uch joyga tarqatib yuborma.
- Placeholder faqat saqlangan qiymat ham bo'sh bo'lganda yoziladi.
- Tekshirishda eng xavfli holat shifrlash yoki token o'chirilgan
  muhitdir: tokeni bor maydon token orqali tiklanadi, token yo'q
  bo'lganda qiymat butunlay yo'qoladi. Testni shu muhitda ham yoz.
- Qiymatni ataylab o'chirish kerak bo'lsa, u alohida amal bo'ladi, "bo'sh
  yuborish" emas.
- Alohida masala: moslik topilmasa sinxronizatsiya ikkinchi qator
  yaratadi. Bu yo'qolish emas, lekin bir xil tuguncha ichida yuradi va
  foydalanuvchiga baribir nuqson bo'lib ko'rinadi. Qamrovga kiritilmasa
  ochiq ayt.
