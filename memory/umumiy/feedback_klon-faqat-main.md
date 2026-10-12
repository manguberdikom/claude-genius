---
type: feedback
---
# Genius klonida faqat `main`: boshqa branch ochilmaydi va push qilinmaydi

- Klonda ish `main` da bajariladi. Saboq commiti `main` ga qo'yiladi va `main` ga push
  qilinadi. Yangi branch ochilmaydi, boshqa branchga push qilinmaydi.
- Sabab: bilim bo'linib qolgan edi. `sonar-boyitish` branchida 35 commit to'planib,
  `main` 35 commit orqada yurdi; `main` dan o'rnatilgan snapshot esa saboqlarni
  ko'rmasdi. 2026-10-12 da hammasi `main` ga fast-forward bilan birlashtirildi va
  qolgan branchlar o'chirildi.
- Push foydalanuvchining proyekt repolariga tegishli qoidadan farq qiladi: proyekt
  repolarida push foydalanuvchida qoladi, KLONDA esa push saboq bosqichining o'z qismi.
- Tekshirish: `git branch --show-current` `main` bo'lishi kerak. Lokal `pre-push` hook
  (`.git/hooks/pre-push`) `main` dan boshqa ref ga pushni rad etadi.
