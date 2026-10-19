---
type: feedback
---
# Klient qaytargan lazy oqim: mock testlarni yashil qoldiradi

Deklarativ HTTP klient (Feign) `ResponseEntity<InputStreamResource>` yoki shunga
o'xshash lazy oqim qaytarganda, kutubxona HTTP javobini klient metodi qaytishi
bilan yopadi. Oqim metod qaytgandan **keyin** o'qilsa "stream is closed" chiqadi
va chaqiruvchi uni tashqi servis nuqsoni deb hisobot qiladi: ishlab chiqarishda
har so'rov 502, lokalda hech narsa.

- Unit testlar buni ushlamaydi: test `InputStreamResource` ni oddiy
  `ByteArrayInputStream` ustiga mock qiladi, u o'qilishi mumkin bo'lib qoladi,
  shuning uchun testlar yashil turadi. Nuqson faqat haqiqiy klientda chiqadi.
  Shuning uchun "testlar o'tdi" bu yerda dalil emas.
- Tuzatish: baytlarni kutubxona chaqiruvining ichida materializatsiya qiladigan
  metodni ishlat (`byte[]` qaytaruvchi variant). Oqimni chaqiruvchi tomonda
  o'qib bo'lmaydi, chunki yopilish vaqti chaqiruvchining qo'lida emas.
- Tuzatishdan keyin qo'riqchi qo'y: lazy oqim qaytaruvchi metod chaqirilmasligini
  tekshiradigan test (`verify(never())`). Butun kod bazasi uchun arzonrog'i
  arxitektura testi (ArchUnit), qimmatrog'i klient egasi repoda haqiqiy
  lokal HTTP server bilan shartnoma testi.
- Baytga o'tganda yo'qoladigan himoyani ayting: chunkli o'qish chegaradan
  oshganda darhol to'xtatardi, `byte[]` esa to'liq bufferlanadi. Oldingi
  darvoza (e'lon qilingan o'lcham) qoladimi, tekshir; o'lcham null kelishi
  mumkin bo'lsa bu ochiq qaror va foydalanuvchiga aytiladi.
- Xotira hisobini javadocga yozganda cho'qqini hisobla: `byte[]` dan base64
  satr yasash paytida xom baytlar, koderning massivi va satr uchalasi tirik
  (≈3.7n), barqaror holat esa ≈2.3n.
