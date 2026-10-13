---
type: feedback
---
# Umumiy daraxtda boshqa sessiyaning yarim ishi kompilyatsiyani buzsa

Belgi: o'z o'zgarishingiz 6 faylda, lekin test yurgizish `cannot find symbol`
beradi va xato SIZ tegmagan faylda. `git status` da sizdan tashqari fayllar
bor: boshqa sessiya ishlab turgan, uning kodi hali izchil emas. Gradle
`testClasses` ni butun yig'adi, shuning uchun ularning yarim ishi sizning
testingizni ham yurgizmaydi.

Ularning fayliga tegmaslik kerak, `git stash` ham qilmaslik kerak (ular
build yurgizayotgan bo'lishi mumkin). Ajratilgan nusxada yurgiziladi:

```sh
git diff -- <faqat o'z fayllaring> > <scratchpad>/ish.patch
git worktree add --detach <scratchpad>/nusxa HEAD
cd <scratchpad>/nusxa && git apply <scratchpad>/ish.patch
run_tests.py --ildiz <scratchpad>/nusxa --diff --yurgiz
```

`guruh.py yarat` bu holatda yaramaydi: u asosni ishchi daraxtdan oladi,
ya'ni begona yarim ishni ham nusxaga ko'chiradi.

Yakunda `git worktree prune` registrni tozalaydi, lekin papkaning o'zi
Windows da o'chmasligi mumkin: `build/test-results/.../binary` uzun yo'l va
Gradle demoni uni ushlab turadi (`Filename too long`, `Access to the path is
denied`). Registr toza bo'lsa bu to'siq emas, papka scratchpad da qoladi.

Commit ham shu holatda aniq yo'llar bilan: `git add <o'z fayllaring>`, hech
qachon `git add -A` yoki `git commit -a`. Begona ish o'rtada commit bo'lsa
`HEAD` siljiydi, diff va patch shunda ham to'g'ri qoladi.
