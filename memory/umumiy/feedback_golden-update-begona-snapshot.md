---
type: feedback
---

# Golden snapshotni yangilashda begona fayllarni tekshirish

Golden master testlarni yangilash rejimida (`GOLDEN_UPDATE` kabi muhit
o'zgaruvchisi) yurgizish butun suite ni qamrab olishi mumkin. Unda yangilanishi
kerak bo'lgan snapshotlar bilan birga BOSHQA snapshotlar ham qayta yoziladi.
Mazmuni o'zgarmasa ham fayl tegiladi: qator oxiri belgisi yoki yozilish tartibi
farq qilib, git ularni "o'zgargan" deb ko'rsatadi.

Tartib:

1. Yangilashdan oldin qaysi snapshot fayllar o'zgarishi KUTILAYOTGANINI aniq
   ro'yxat qilib yozib qo'y.
2. Yangilagandan keyin `git status` ni shu ro'yxat bilan solishtir. Ro'yxatda
   yo'q fayllar chiqsa, ularni `git checkout --` bilan qaytar: ular bu ishning
   o'zgarishi emas.
3. Kutilgan fayllarning diffi mazmunan tekshiriladi: o'zgarish faqat kutilgan
   joyda ekaniga dalil keltiriladi (masalan so'z to'plamini solishtirish, yoki
   o'zgargan qatorlarni sanab chiqish).
4. Keyin yangilash rejimisiz qayta yurgizib yashil ekani ko'rsatiladi.

Nima beradi: commitga tegishsiz fayl tushmaydi va "snapshot yangilandi" degan
gap dalilga aylanadi. Bog'liq: [[feedback_pdf-vizual-tekshiruv]].
