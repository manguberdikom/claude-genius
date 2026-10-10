---
type: feedback
---

# Chop etiladigan hujjat o'zgarishini ko'z bilan tekshirish

PDF yoki boshqa chizilgan hujjatning ko'rinishi o'zgarsa (shrift o'lchami,
ustun kengligi, joylashuv), matn snapshoti yetarli dalil emas: u kesilishni,
ustun ustiga chiqishni va sahifaga sig'masligni ko'rsatmaydi.

Tartib:

1. `src/test/` da vaqtinchalik test yoziladi. U real hajmdagi ma'lumot
   beradi: ko'p qatorli jadval, uzun ismlar, eng uzun yorliqlar, chegara
   qiymatlar. Golden fixture odatda kichik bo'ladi va sahifa uzilishini
   ko'rsatmaydi.
2. Test hujjatni scratchpad ga yozadi va o'sha yerda PNG ga render qiladi.
   `pdftoppm` (poppler) Windows da odatda yo'q, shuning uchun render test
   klasspatidagi kutubxona bilan qilinadi: PDFBox da
   `new PDFRenderer(document).renderImageWithDPI(page, 100)` va `ImageIO.write`.
   100 DPI butun sahifani ko'rish uchun yetarli, mayda joyga 200 DPI va
   `getSubimage` bilan qirqim.
3. PNG o'qiladi va ko'z bilan tekshiriladi: kesilish, ustun ustiga chiqish,
   kutilmagan o'ralish, sahifalar soni, takrorlanuvchi sarlavha.
4. Vaqtinchalik test ish oxirida o'chiriladi va commitga tushmaydi.

Nima beradi: agentlar hisobotida "vizual tekshirilmadi" degan ochiq xavf
yopiladi va sahifaga sig'ish haqidagi taxmin dalilga aylanadi.

Bog'liq: [[feedback_startup-xatosini-tuzatish]] (dalilsiz "tuzatildi" deyilmaydi).
