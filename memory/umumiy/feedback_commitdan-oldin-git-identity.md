---
type: feedback
---
# Commitdan oldin git identity tekshiriladi

Global `~/.gitconfig` dagi identity foydalanuvchinikidan boshqa hisob
bo'lishi mumkin. Repo darajasida `user.name` va `user.email` o'rnatilmagan
bo'lsa commit jim o'sha begona nom bilan ketadi va bu faqat remote da,
push dan keyin ko'rinadi.

- Foydalanuvchi buni push qilingan commitni ko'rib aytdi: muallif noto'g'ri
  hisobdan chiqqan. Bir repoda repo darajasidagi identity bor edi, qo'shni
  repoda esa yo'q, shuning uchun bir xil ishning commitlari ikki xil nom
  bilan ketgan.
- Qoida: proyekt repoda birinchi commitdan oldin
  `git config --local user.email` tekshiriladi. Bo'sh bo'lsa, to'g'ri qiymat
  qo'shni repodan olinadi (`git -C <qo'shni repo> config --local user.name`
  va `user.email`), global qiymat ishonchli emas.
- Qiymatning o'zi memoryga yozilmaydi, u shaxsiy ma'lumot. Faqat qayerdan
  olinishi yoziladi.
- Noto'g'ri muallif bilan commit allaqachon push qilingan bo'lsa, tuzatish
  tarixni qayta yozadi va `--force-with-lease` talab qiladi: bu
  foydalanuvchining qarori, o'z-o'zidan qilinmaydi.
