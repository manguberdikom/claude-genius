---
type: feedback
---
# Filtr uchun ustun tanlashda yozuvchisini tekshir

Sana oralig'i bo'yicha filtr qo'shilganda ustun nomi mos kelgani yetarli
emas: o'sha ustunga kim yozayotganini ko'rish kerak.

- Bir ishda "sinxronizatsiya vaqti" degan ustun tabiiy nomzod edi, lekin
  mapper uni `ignore` qilgani uchun hech qachon to'lmaydi: u bilan filtr
  har doim 0 qaytarar edi. To'g'ri ustun audit yaratilish sanasi bo'lib
  chiqdi, uni retention job ham ishlatadi.
- Shuning uchun topshiriqda ustunni "tasdiqla" deb yozish kerak, "shu
  ustunni ishlat" deb emas: kim `set` qiladi, migratsiyada NOT NULL mi,
  boshqa so'rovlar unga tayanadimi.
- Nullable ustun bo'yicha filtr qatorni chiqarib tashlaydi. Filtrsiz
  yo'lda esa o'sha qator sanaladi, ya'ni ikki rejim bir-biriga mos
  kelmaydi. Buni so'rov izohida yozib qo'yish kerak.
- Statusni o'zgartiruvchi metodlar (soft delete, "ishga olindi") sanoqni
  jim o'zgartiradi: `count()` emas, status bo'yicha sanash kerak.
