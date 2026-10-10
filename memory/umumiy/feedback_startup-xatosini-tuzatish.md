---
type: feedback
---
# Startup xatosini tuzatish: dalilsiz "tuzatildi" deyilmaydi

Bitta startup xatosi uch marta qaytib keldi va productiongacha chiqdi, chunki har safar
sabab taxmin qilindi va tuzatish tekshirilmay "tayyor" deyildi.

- Avval TO'LIQ stack trace so'raladi. Eng ichki kadrlar faqat qayerda yiqilganini aytadi,
  o'zgartirilishi kerak bo'lgan chaqiruvchi esa yuqoridagi kadrlarda (`afterPropertiesSet`,
  `registerJobsAndTriggers`). To'rt kadr bilan dizayn boshlanmaydi.
- "Yiqilishdan oldin ma'lumotni tozalaydigan" himoya tuzatish emas, yumshatish. Himoya
  mantiqan ishlashi kerak bo'lsa-yu xato qaytsa, ikkinchi himoya qatlami qo'shilmaydi:
  yiqiladigan chaqiruvning o'zi yo'ldan olinadi (xato log ga, ilova tirik qoladi).
- Mavjud himoya nega ishlamaganini bilmay turib yangi tuzatish "sabab topildi" deb
  yozilmaydi. Bilinmagan narsa hisobotda "bilmayman" deb aytiladi.
- Bean olib tashlansa, turi yoki nomi o'zgarsa, testlar bean NOMI bo'yicha emas, TURI
  bo'yicha ham qidiriladi: `getBean(X.class)`, `doesNotHaveBean(X.class)`, va shu
  konfiguratsiyani `withUserConfiguration` bilan yuklaydigan har sinf (yangi majburiy
  bog'liqlik ularning kontekstini yiqitadi).
- Ishlab chiqarish kodi o'zgargandan keyin test sinflari qo'lda tanlanmaydi:
  `run_tests.py --diff --yurgiz`. Qo'lda tanlangan olti sinf yashil chiqdi, to'liq suite
  da esa uchta test yiqildi.
- Foydalanuvchi "testlarni tekshirma" desa ham, build ni sindiradigan o'zgarishdan keyin
  kamida kompilyatsiya va tegishli testlar yuradi, yoki yurmagani aniq aytiladi: qizil CI
  tuzatishning prodga chiqishini to'sadi.
- Qo'llangan migratsiya fayli (Liquibase `sqlFile`, Flyway skripti) izohi bilan birga
  muzlatilgan. Sinf nomini almashtirganda `db/` ostidagi fayllar almashtirishdan
  chiqariladi, aktyorga topshiriqda ham shu yoziladi (`architect 33`).
