# Promptni normallashtirish va aktyor tanlash

Prompt ko'pincha yarim aytilgan bo'ladi: "shuni tuzat", "review qil",
"yaxshilab ber". Shunday promptni to'g'ridan-to'g'ri bajarish noto'g'ri
ishni tez bajarishga olib keladi. Avval u normallashtiriladi.

## Normallashtirish: besh maydon

Promptdan shu beshtasi chiqariladi. Chiqmasa, jadvaldagi standart
qiymat olinadi va javobda `standart: <qiymat>` deb ko'rsatiladi.
Standart yo'q maydon (Niyat) uchun bitta savol beriladi, faqat ish
boshida.

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

## Hajm: zanjir uzunligi va reja

Hajm faqat shu jadvalda ta'riflanadi. `SKILL.md`, `aktyorlar.md` va
agent fayllari unga havola qiladi, o'z shkalasini yozmaydi. Fayl soniga
tegiladigan ishlab chiqarish fayllari kiradi, ularning testlari kirmaydi.

| Hajm | Belgisi | Zanjir | Reja |
|---|---|---|---|
| S | 1-3 fayl, bitta qatlam, qaytariladi | `dasturchi` -> `review` | yo'q |
| M | 4 va undan ko'p fayl yoki bir necha qatlam, qaytarib bo'lmaydigan qaror yo'q | `dasturchi` -> `test-muhandis` va `review` parallel -> bitta tuzatish aylanasi | yo'q |
| L | qaytarib bo'lmaydigan qaror (sxema migratsiyasi, API shartnomasi, tashqi bog'liqlik, ma'lumot formati), talab hujjatdan yoki bir necha modul | `rejalashtiruvchi` -> har guruhga `dasturchi`, guruhlar parallel worktree da -> birlashgan diffga bitta `review` va `test-muhandis` | bor |

Shubha bo'lsa kichigi olinadi: S dan M ga o'tish arzon (review topilmasi
test muhandisini chaqiradi), M o'rniga L esa butun reja bosqichini
qo'shadi.

Reja qimmat: u faqat L da yoki foydalanuvchi ochiq so'raganda tuziladi.
Qolgan hammasi rejasiz: `dasturchi` toza kod va dizayn pattern
qoidalari asosida o'zi bajaradi. Bitta bug uchun reja yozish ishni
sekinlashtiradi va hech narsa qo'shmaydi.

Cheklov zanjirni qisqartiradi (`references/aktyorlar.md`, `Cheklov va testlar`):
test o'zgarishi taqiqlangan bo'lsa M da `test-muhandis` chaqirilmaydi.

## Aktyor tanlash

Niyat aktyorni belgilaydi. Bitta promptda bir nechta niyat bo'lsa, ular
ketma-ket bajariladi, aralashtirilmaydi.

| Niyat | Aktyor | Izoh |
|---|---|---|
| Holatni bilish, kamchilik topish | `review` | kod o'zgarmaydi; diff bo'lmasa doira va modul ro'yxati beriladi |
| Yo'lni belgilash | `rejalashtiruvchi` | hajm L yoki ochiq so'ralganda |
| Kodni o'zgartirish | `dasturchi` | bug, pattern, refaktoring, reja qadami; "tuzat" va "yiqildi" birga kelsa ham |
| Testlar | `test-muhandis` | qoplash so'ralganda yoki xato test kodining o'zida ekani aniq bo'lganda |
| Qoida matnini keltirish, uchtadan ko'p bo'lim | `qidiruv` | bir-uch bo'lim bo'lsa `doc.sh show` asosiy sessiyada, aktyorsiz |
| Chiqish yoki sxemani o'qish | `tahlil` | uzun log, entity, test chiqishi |

Reja tuzish zanjirda `rejalashtiruvchi` aktyoriga boradi: alohida reja
skilli yo'q.

## Hujjat berilgan bo'lsa

Rasm, PDF yoki Word berilsa, u **talab manbai**, qaror emas. Undan
chiqariladi: funksional talablar, ma'lumot modeli, chegaralar, aniq
bo'lmagan joylar. Oxirgisi rejada "aniqlanishi kerak" bo'limiga
tushadi, o'ylab to'ldirilmaydi.

Fayl bo'lib berilgan rasm, PDF yoki Word yo'li `rejalashtiruvchi` ga
beriladi va uni aktyorning o'zi o'qiydi: PDF va rasm `Read` bilan, Word
uchun buyruq agent faylida. Asosiy sessiya hujjatni oldindan o'qimaydi,
marshrut skillariga ham tayanmaydi: global o'rnatishda ular yo'q.

Rasm chatga qo'yilgan bo'lsa, aktyor uni ko'rmaydi: talablar asosiy
sessiyada matnga aylantiriladi yoki fayl yo'li beriladi, keyin
`rejalashtiruvchi` chaqiriladi.

## Ochiq qarorlar: savolsiz davom

Zanjir o'rtasida berilgan savol ishni foydalanuvchi javob berguncha
to'xtatadi va budjetni ham nolga tushiradi. Shuning uchun qaror ikki
turga bo'linadi:

| Qaror | Nima qilinadi |
|---|---|
| Qaytariladigan: nom, joy, pattern varianti, test turi, kutubxona ichidagi API tanlovi | standart tanlanadi va ish davom etadi |
| Qaytarib bo'lmaydigan: ma'lumot o'chirish yoki buzuvchi migratsiya, ommaviy API shartnomasi, yangi tashqi bog'liqlik, xavfsizlik siyosati | ish boshida, bitta xabarda, hammasi birga so'raladi |

Standart tanlash tartibi: proyekt konvensiyasi, keyin `CLAUDE.md` va
memory, keyin qo'llanma bo'limi, keyin eng tor va eng qaytariladigan
variant. Tanlangan har standart guruh kartasidagi `qarorlar:` qatoriga
va yakuniy hisobotdagi `Qabul qilingan qarorlar` ro'yxatiga yoziladi:
foydalanuvchi ularni keyin bitta xabar bilan o'zgartira oladi.

Ish boshidagi savollar ham ishni to'xtatmasligi kerak: qaytarib
bo'lmaydigan qarorga bog'liq bo'lmagan guruhlar savol bilan bir vaqtda
boshlanadi, bog'liq guruh javobni kutadi.

Aktyor ham savol bilan tugamaydi. Javobida qaror kerak bo'lsa u
shunday yoziladi va ish standart bilan davom etgan bo'ladi:

```
Ochiq qaror: <savol> | standart: <tanlangan> | qaytariladimi: ha/yo'q
```

`qaytariladimi: yo'q` bo'lsa asosiy sessiya o'sha guruhni to'xtatadi va
savolni foydalanuvchiga bir marta beradi, qolgan guruhlar davom etadi.

## Shubha bo'lsa

Ikki yo'l orasida qolganda eng tor va eng qaytariladiganini tanlang,
keyin natijani ko'rsating. Katta va qaytarib bo'lmaydigan yo'l faqat
tasdiqdan keyin.
