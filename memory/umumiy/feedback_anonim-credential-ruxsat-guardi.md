---
type: feedback
---
# Anonim credential bilan ochiladigan endpointga identifikatorga tayangan guard

- Ba'zi endpointlar **foydalanuvchi sessiyasi bilan emas**, bir martalik link
  yoki token bilan ochiladi (magic link, QR, taklif havolasi). So'rovda
  foydalanuvchi identifikatori (`X-Email` kabi sarlavha) **bo'lmaydi**.
- Review "bu endpoint object-level tekshiruvsiz" deb to'g'ri aytadi, lekin
  tekshiruvni **joriy foydalanuvchiga** bog'lash oqimni butunlay buzadi: egasi
  aniqlanmaydi va har so'rov rad etiladi. Guard qo'yishdan oldin endpointning
  qaysi oqimdan chaqirilishini (anonim havolami, portalmi) aniqlang.
- Yechim: **credential sifatida linkning o'zini** ishlatish. Link id so'rovdan
  olinadi, u obyektning saqlangan link id siga teng bo'lishi va link qatori
  hali faol bo'lishi tekshiriladi. Mos kelmasa oddiy egalik/ruxsat yo'liga
  tushadi, ya'ni anonim chaqiruvchi rad etiladi. Bir martalik ta'sir (yuborish,
  tasdiqlash) status matritsasi bilan himoyalanadi, shuning uchun oshkor
  bo'lgan link takror ishlatilmaydi.
- Shu bilan birga: **bo'sh identifikator bilan tashqi ruxsat servisini
  chaqirmang**. Mijoz kutubxonalari identifikatorni yo'l segmentiga qo'yadi,
  bo'sh qiymat `/has-permission//PERM_X` kabi yo'l yasaydi va servis 404/500
  qaytaradi. Kutubxona buni "ruxsat olinmadi" xatosiga o'raydi, natijada
  foydalanuvchi 403 emas, tushunarsiz 500/ichki kod ko'radi va HTTP 200 tanasida
  keladi. Tekshiruvni chaqiruvdan oldin qo'ying: identifikator bo'sh bo'lsa
  ruxsat yo'q deb hisoblang (fail-closed), chaqiruv qilinmaydi.
- Testda shu ikki holatni ajratib yozing: identifikatorsiz so'rovda ruxsat
  servisiga **umuman murojaat qilinmagani** (`never()` / `verifyNoInteractions`)
  va mavjud obyektda ham rad etilgani. Mock sukut bo'yicha `null` qaytarsa
  haqiqiy kutubxona xulqini (`success(null)`) taqlid qiling, aks holda test
  NPE ni o'lchaydi.
