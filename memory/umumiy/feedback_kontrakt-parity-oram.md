---
type: feedback
---
# Shakl pariteti: javob o'ramini ham solishtir

Ikki servis bir xil shakldagi javob berishi talab qilinganda (frontend
ikkisini bitta parser bilan o'qiydi), DTO maydon nomlarini solishtirish
yetarli emas.

- Reviewer DTO ni maydon-maydon tasdiqladi va "parity mos" dedi, lekin
  controller javobni umumiy natija o'rovchi tipga o'ramay xom DTO
  qaytargani e'tibordan chetda qoldi. Ya'ni JSON ildizi boshqa darajada
  edi: bir tomonda `$.data.summary`, ikkinchisida `$.summary`.
- Nuqsonni kontrakt testi topdi, review emas: test JSON yo'lini ildizdan
  yozgani uchun o'ram yo'qligi darhol yiqildi.
- Shuning uchun: shakl pariteti topshirig'ida "javob o'ramini (umumiy
  natija/sahifa o'rovchi tipni) ham solishtir" bandi alohida yoziladi.
  Kontrakt testi JSON yo'lini doim to'liq ildizdan yozadi, nisbiy
  emas.
- Yo'qlikni tekshiradigan assert (`doesNotExist`) o'ram yo'q bo'lganda
  bo'sh ma'noda o'tadi: avval o'ram mavjudligi tasdiqlanadi, keyin
  ichidagi blok yo'qligi.
- Shakl bir xil bo'lib, ma'no har xil bo'lishi ham parite buzilishi.
  Bir ishda ikki servis bir xil `appliedFilter` ni qaytardi, lekin bitta
  blokni biri oraliqqa toraytirdi, ikkinchisi butun tarix bo'yicha berdi:
  bitta ekranda bir xil filtr ikki xil son ko'rsatardi. Shuning uchun
  review topshirig'ida "har bir blok filtrga ikki servisda bir xil
  javob beradimi" deb alohida so'raladi.
- Seam (internal endpoint yoki client) orqali keladigan blok alohida
  tekshiriladi: endpoint parametrni qabul qilgani uning o'sha parametrni
  ishlatishini bildirmaydi.
