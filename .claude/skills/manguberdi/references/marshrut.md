# Promptni normallashtirish va aktyor tanlash

Prompt ko'pincha yarim aytilgan bo'ladi: "shuni tuzat", "review qil",
"yaxshilab ber". Shunday promptni to'g'ridan-to'g'ri bajarish noto'g'ri
ishni tez bajarishga olib keladi. Avval u normallashtiriladi.

## Normallashtirish: besh maydon

Promptdan shu beshtasi chiqariladi. Chiqmasa, **taxmin qilinmaydi**:
javobda shu maydon "aniqlanmagan" deb belgilanadi yoki bitta savol
beriladi.

| Maydon | Savol | Chiqmasa |
|---|---|---|
| Niyat | nima qilinadi: tekshirish, tuzatish, rejalashtirish, qoplash | bitta savol beriladi |
| Doira | qaysi fayl, modul yoki butun proyekt | eng tor variant olinadi |
| Artefakt | natija nima: kod, reja fayli, hisobot, test | niyatdan kelib chiqadi |
| Qabul mezoni | qachon bajarilgan hisoblanadi | tekshiruvlar toza bo'lishi olinadi |
| Cheklov | nimaga tegilmaydi | CLAUDE.md va memorydan olinadi |

Normallashtirilgan vazifa bir jumlada aytilishi kerak. Aytib bo'lmasa,
u bitta vazifa emas: bo'linadi.

## Hajm: reja kerakmi

Reja qimmat. U faqat shu uchtadan biri bo'lsa tuziladi:

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
| Holatni bilish, kamchilik topish | `review` | kod o'zgarmaydi |
| Yo'lni belgilash | `rejalashtiruvchi` | faqat yuqoridagi uch shartda |
| Kodni o'zgartirish | `arxitektor` | bug, pattern, refaktoring, reja qadami |
| Testlar | `test-muhandis` | qoplash yoki yiqilgan testni tuzatish |
| Qoida matnini keltirish | `qidiruv` | javob o'qish, qaror emas |
| Chiqish yoki sxemani o'qish | `tahlil` | uzun log, entity, test chiqishi |

## Hujjat berilgan bo'lsa

Rasm, PDF yoki Word berilsa, u **talab manbai**, qaror emas. Undan
chiqariladi: funksional talablar, ma'lumot modeli, chegaralar, aniq
bo'lmagan joylar. Oxirgisi rejada "aniqlanishi kerak" bo'limiga
tushadi, o'ylab to'ldirilmaydi.

## Shubha bo'lsa

Ikki yo'l orasida qolganda eng tor va eng qaytariladiganini tanlang,
keyin natijani ko'rsating. Katta va qaytarib bo'lmaydigan yo'l faqat
tasdiqdan keyin.
