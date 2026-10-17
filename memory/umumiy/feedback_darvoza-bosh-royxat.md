---
type: feedback
---
# Boshqa servis ro'yxatiga tayangan darvoza: bo'sh ro'yxat ochiq qiymat

- Cheklovchi qarorni (gate) boshqa servisdan kelgan ro'yxat asosida qilsangiz,
  **bo'sh ro'yxat ochiq qiymat** bo'lib qoladi: "yetishmagan narsa topilmadi"
  degani "hammasi joyida" emas, "javob yo'q" bo'lishi mumkin.
- Mijoz kutubxonalari odatda ishlatib bo'lmaydigan javobni (`success=true`,
  `data=null`, yoki noma'lum id) bo'sh ro'yxatga aylantiradi. Shuning uchun
  faqat **istisno** yo'lini yopish yetarli emas: istisno testi `catch` yo'qligini
  isbotlaydi, bo'sh javob yo'lini isbotlamaydi.
- Yechim: darvozada ro'yxat butunlay bo'sh bo'lsa rad eting va **nega bo'sh
  bo'lishi mumkin emasligini** asoslab yozing (masalan ro'yxat seed bilan
  yaratiladi va startda tekshiriladi). Zaxira qiymat cheklovchi bo'lsin.
- Kutilgan narx: bunday tekshiruv **mavjud oqim testlarini ommaviy yiqitadi**,
  chunki ular bu chaqiruvni stub qilmaydi va mock sukut bo'yicha bo'sh ro'yxat
  qaytaradi. 25 test yiqilgan holat bo'lgan. Har testga tegmang: `@BeforeEach`
  da `lenient()` bilan yaroqli sukut ro'yxat bering, darvozaning o'z testlari
  uni bosib ketadi.
