---
type: feedback
---
# Windows va Git Bash da jim o'tkazib yuborilgan buyruq

- `cmd /c "..."` ni **Bash toolidan chaqirmang**. Git Bash yolg'iz `/c` ni
  POSIX yo'l deb bilib `C:\` ga aylantiradi, natijada cmd `/c` ni ko'rmaydi va
  interaktiv rejimda ochiladi: buyruq **bajarilmaydi**, chiqish faqat cmd
  banneri bo'ladi va **exit kodi 0** qaytadi. Bu yolg'on yashil beradi.
- Belgi: chiqishda `Microsoft Windows [Version ...]` va prompt qatori bor,
  lekin buyruqning o'z chiqishi yo'q. Shu holatda natijani yashil deb hisoblamang.
- To'g'ri yo'llar: `./gradlew ...` (sh wrapper) yoki asbobni Pythondan chaqirish
  (`run_tests.py` shuning uchun shikastlanmaydi). Zarur bo'lsa `cmd //c` yoki
  `MSYS2_ARG_CONV_EXCL`.
- Umumiy qoida: har buyruqni **chiqish matni** bilan tasdiqlang, exit kodiga
  yolg'iz ishonmang. Tasdiqlovchi buyruq (`ls`, `grep`) natijani ko'rsatsin.
- `git worktree add` ni uzun yo'lga (sessiya temp papkasi) ochmang: Windowsda
  `Filename too long` beradi va **yarim yaratilgan** worktree qoldiradi
  (`fatal: Could not reset index file`). Qisqa yo'l ishlatiladi, masalan
  `C:/src/<nom>`. Yarim qolganini `git worktree remove --force`, so'ng
  `git worktree prune` bilan tozalang; papka o'chmasa `rmdir /s /q` yoki
  `\?\` prefiksi bilan `Remove-Item`.
