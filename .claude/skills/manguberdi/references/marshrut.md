# Promptni normallashtirish va aktyor tanlash

Prompt ko'pincha yarim aytilgan bo'ladi: "shuni tuzat", "review qil",
"yaxshilab ber". Shunday promptni to'g'ridan-to'g'ri bajarish noto'g'ri
ishni tez bajarishga olib keladi. Avval u normallashtiriladi.

## Normallashtirish: besh maydon

Promptdan shu beshtasi chiqariladi. Chiqmasa, jadvaldagi standart
qiymat olinadi va javobda `standart: <qiymat>` deb ko'rsatiladi.
Standart yo'q maydon (Niyat) uchun bitta savol beriladi.

| Maydon | Savol | Chiqmasa |
|---|---|---|
| Niyat | nima qilinadi: tekshirish, tuzatish, rejalashtirish, qoplash | bitta savol beriladi |
| Doira | qaysi fayl, modul yoki butun proyekt | eng tor variant olinadi |
| Artefakt | natija nima: kod, reja fayli, hisobot, test | niyatdan kelib chiqadi |
| Qabul mezoni | qachon bajarilgan hisoblanadi | tekshiruvlar toza bo'lishi olinadi |
| Cheklov | nimaga tegilmaydi | CLAUDE.md va memorydan olinadi |

Normallashtirilgan vazifa bir jumlada aytilishi kerak. Aytib bo'lmasa,
u bitta vazifa emas: bo'linadi. Doira bitta aktyor chaqiruviga
sig'maydigan darajada katta bo'lsa (bir necha modul), u ham bo'linadi:
har modul alohida vazifa va alohida budjet.

## Hajm: reja kerakmi

Reja qimmat. U faqat shu uchtadan biri bo'lsa yoki foydalanuvchi ochiq
so'rasa tuziladi:

- O'zgarish **uch fayldan ko'proq** yoki bir necha qatlamga tegadi.
- Qaror **qaytarib bo'lmaydi**: sxema migratsiyasi, API shartnomasi,
  tashqi bog'liqlik, ma'lumot formati.
- Talab **hujjatdan keladi**: spetsifikatsiya, dizayn rasmi, PDF, Word.

Qolgan hammasi rejasiz: `arxitektor` toza kod va dizayn pattern
qoidalari asosida o'zi bajaradi. Bitta bug uchun reja yozish ishni
sekinlashtiradi va hech narsa qo'shmaydi.

## Aktyor tanlash

Niyat aktyorni belgilaydi. Bitta promptda bir nechta niyat bo'lsa, ular
ketma-ket bajariladi, aralashtirilmaydi.

| Niyat | Aktyor | Izoh |
|---|---|---|
| Holatni bilish, kamchilik topish | `review` | kod o'zgarmaydi; diff bo'lmasa doira va modul ro'yxati beriladi |
| Yo'lni belgilash | `rejalashtiruvchi` | yuqoridagi uch shartda yoki ochiq so'ralganda |
| Kodni o'zgartirish | `arxitektor` | bug, pattern, refaktoring, reja qadami |
| Testlar | `test-muhandis` | qoplash yoki yiqilgan testni tuzatish |
| Qoida matnini keltirish, uchtadan ko'p bo'lim | `qidiruv` | bir-uch bo'lim bo'lsa `doc.sh show` asosiy sessiyada, aktyorsiz |
| Chiqish yoki sxemani o'qish | `tahlil` | uzun log, entity, test chiqishi |

`reja` skilli zanjirda chaqirilmaydi, uning o'rnini `rejalashtiruvchi` bosadi.

## Hujjat berilgan bo'lsa

Rasm, PDF yoki Word berilsa, u **talab manbai**, qaror emas. Undan
chiqariladi: funksional talablar, ma'lumot modeli, chegaralar, aniq
bo'lmagan joylar. Oxirgisi rejada "aniqlanishi kerak" bo'limiga
tushadi, o'ylab to'ldirilmaydi.

Fayl bo'lib berilgan rasm, PDF yoki Word yo'li `rejalashtiruvchi` ga
beriladi va uni aktyorning o'zi o'qiydi: PDF va rasm `Read` bilan, Word
uchun buyruq agent faylida. Asosiy sessiya hujjatni oldindan o'qimaydi,
`reja` skilliga ham tayanmaydi: global o'rnatishda u yo'q.

Rasm chatga qo'yilgan bo'lsa, aktyor uni ko'rmaydi: talablar asosiy
sessiyada matnga aylantiriladi yoki fayl yo'li beriladi, keyin
`rejalashtiruvchi` chaqiriladi.

## Shubha bo'lsa

Ikki yo'l orasida qolganda eng tor va eng qaytariladiganini tanlang,
keyin natijani ko'rsating. Katta va qaytarib bo'lmaydigan yo'l faqat
tasdiqdan keyin.
