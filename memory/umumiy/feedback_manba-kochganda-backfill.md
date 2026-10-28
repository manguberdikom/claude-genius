---
type: feedback
modified: 2026-10-28T00:00:00Z
---
# Fakt manbasi ko'chganda ma'lumot ham ko'chadi

- Ustun hosila qiymatga aylantirilsa (getter, `@Formula`, boshqa jadvaldan JOIN), eski ustundagi qiymat yangi manbada bormi, deploydan oldin sanash kerak. Bir ishda xodim sanalari "joriy hujjat" dan o'qiladigan bo'ldi, lekin xodimlarning 90% ida bunday hujjat yo'q edi: ekranda sana yo'qolardi, contract esa ustunni DROP qilib yo'qotishni qaytarilmas qilardi.
- Kartada uchta narsa majburiy: (1) SELECT: eski manbada qiymat bor, yangisida yo'q qatorlar soni; (2) expand changeset da backfill (idempotent, kichik bo'laklar); (3) contract DROP ga ma'lumot darvozasi: shu son 0 bo'lmasa DROP yo'q.
- Ikki manba farq qilsa qaysi biri yutishi foydalanuvchi qarori bilan yoziladi, backfill farqli qatorlarga tegmaydi.
