---
type: feedback
modified: 2026-10-28T00:00:00Z
---
# Commitsiz asosiy daraxtga guruhni birlashtirish

- Asosiy daraxtda oldingi bosqich commitsiz tursa, `guruh.py yarat` uni snapshot qilib guruhga beradi. `guruh.py birlashtir` esa shu commitsiz o'zgarishni kesishma deb hisoblaydi va hech narsani qo'llamaydi: guruh diffi asosga nisbatan toza bo'lsa ham.
- Yo'l:
  1. Guruh worktree sida `git add -A -N .`, keyin `git diff --binary <asos>` (yangi fayllar ham kiradi).
  2. Asosiy daraxtda `git apply --check`, keyin `git apply --exclude=<kesishgan fayl>`.
  3. Kesishgan fayl uchun asosni `git show <asos>:<fayl>` bilan oling. Asos va guruh nusxasini maqsad faylning qator oxiriga (CRLF/LF) keltiring va `git merge-file <joriy> <asos> <guruh>` ni joyida yurgizing. Hook `.java` ga shell yo'naltirish (`>`) ni to'sadi. Qolgan ziddiyat Edit bilan hal qilinadi.
  4. Har faylni `diff --strip-trailing-cr` bilan guruh nusxasiga solishtiring: farq faqat ikkinchi guruh qo'shgan qism bo'lishi kerak.
- Qo'lda birlashtirilgan guruh `guruh.py` uchun birlashmagan bo'lib qoladi: tozalash `tozala <id> --majburiy`, keyin branch nomi bilan `git branch -D`.
- Registrdagi yetim yozuvlar (papkasi va branchi yo'q) `GENIUS_GURUH_MAX` chegarasini to'ldiradi. Boshqa sessiyalar yozgan bo'lishi mumkin, shuning uchun registrga tegilmaydi: chegara faqat o'z buyruqlari uchun `GENIUS_GURUH_MAX=<son>` bilan ko'tariladi.
- Teskari holat ham bor: asosiy daraxt toza va asos `dev` tarixida bo'lsa `birlashtir` cherry-pick yo'lini tanlaydi va guruhning commitsiz qoldig'ini o'zi `genius: <id> qolgan o'zgarish` xabari bilan commit qilib `dev` ga qo'yadi. "Commit yo'q" rejimida `birlashtir` ishlatilmaydi: yuqoridagi qo'lda yo'l (worktree da `git add -A && git diff --cached --binary <asos>`, asosiy daraxtda `git apply --3way`). Tushib qolgan commit `git reset --mixed <asos>` bilan qaytariladi.
