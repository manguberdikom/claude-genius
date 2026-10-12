---
type: feedback
---

# Yangi saboq bo'limini hujjatga qo'yish

Bob oxiriga yangi bo'lim qo'shilganda uni **yopish bo'limidan oldin** qo'yish kerak
(`## N.x Amalda qo'llash` oxirgi bo'lim bo'lib qoladi) va navigatsiya footeri
(`---` dan keyingi `[&larr; ...]` qatori) fayl eng oxirida turishi kerak.
Mundarija qatori `<details>` bloki ichiga yoziladi, checklist ro'yxatining
oxiriga emas: u yerda markdown uni checklist elementi qilib ko'rsatadi.

Har qo'shilgan bo'lim uchun **to'rt joyda** son yangilanadi:

1. fayldagi `<summary>Bu bobdagi N bo'lim</summary>`;
2. `docs/<hujjat>/README.md` dagi shu bob qatori (`- N bo'lim`);
3. `docs/manifest.json` dagi shu bobning `"sections"`;
4. ildiz `README.md` dagi jami (`224 bob, NNNN bo'lim`) va hujjat qatori
   (`39 bob, NNN bo'lim`).

Shundan keyin `python tools/check_docs.py` yurgiziladi va "Hammasi joyida"
chiqishi kerak. Oxirgi uchta xato turi (`manifestda N`, `<summary> da N`,
`oxirgi bo'lim yopish bo'limi emas`) aynan shu tartib buzilganda chiqadi.

**Nega:** 2026-10-11 da uchta sonarqube bobiga saboq qo'shildi, lekin bo'lim
yopish bo'limidan keyin qo'shilgani va sonlar yangilanmagani uchun
`check_docs` 12 xato berdi va keyingi sessiyaga qoldi. `manifest.json` ni
qayta yozishda `json.dumps` bilan butun faylni formatlab yuborish ham kerak
emas: faqat kerakli `"sections"` qiymati matn sifatida almashtiriladi, aks
holda diff 3000 qatorga chiqadi.

**Qanday qo'llash:** bo'limni `## N.<yopish raqami> ` dan oldin joylashtir,
raqamlarni almashtir, to'rt joydagi sonni oshir, `check_docs.py` ni yurgiz.
