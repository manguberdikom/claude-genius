---
type: feedback
---
# Guruh birlashtirgandan keyin commit: asosiy sessiyaning tahrirlari tushib qoladi

- `guruh.py birlashtir` faqat GURUH fayllarini indeksga qo'yadi. Asosiy sessiya o'zi qilgan
  tahrirlar (koordinator tuzatishlari, guruhlararo buzilgan test kutilmalari, build fayli)
  staged BO'LMAYDI va `git commit` (`-a` siz) ularni jimgina tashlab ketadi.
- Shuning uchun commitdan oldin har doim: `git status --short | grep -v '^??'`. Chap ustunda
  bo'sh joy bo'lgan qator (` M`) staged emas, demak commitga tushmaydi.
- Oqibati: tahrirlar ishchi daraxtda qoladi, to'liq suite ular bilan yashil chiqadi, lekin
  commit ularsiz. Keyin branch rewrite yoki alohida commit kerak bo'ladi.
- Asosiy sessiyaning tahrirlari alohida commit bo'lishi ma'qul: guruh commitlari toza qoladi.

# Bash tool da ko'p qatorli commit xabari

- Bash tool POSIX sh: PowerShell here-string (`@'...'@`) literal o'tadi va xabar boshiga `@`
  tushadi. Xabarni faylga yozib `git commit -F <fayl>` bilan ber.
