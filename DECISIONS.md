# Qaror yozuvlari

Xulqni o'zgartirgan, orqaga qaytarish yo'li aniq bo'lishi kerak qarorlar.
Har yozuv bir xil shaklda: nima o'zgardi, nega, rad etilgan variantlar,
xavf, qaysi tekshiruv o'tdi, orqaga qaytarish.

Hamma o'zgarish bu yerga yozilmaydi. Yoziladigani: foydalanuvchi
muhitiga tegadigan, ma'lumot yo'qotishi mumkin bo'lgan yoki ruxsat
qarorini o'zgartiradigan o'zgarish.

## 2026-10-05: O'rnatuvchi sukut bo'yicha qo'shuvchi bo'ldi

**Nima o'zgardi.** `install/manguberdi.ps1` da `-Apply` ning sukut xulqi.
Avval u `~/.claude` dan `settings.json`, `settings.local.json`,
`CLAUDE.md`, `skills`, `agents`, `commands`, `plugins`, `hooks`, `rules`
va `output-styles` ni o'chirardi. Endi faqat o'z birliklari almashadi:
`skills\manguberdi`, olti aktyor fayli va `settings.json` dagi shu
klonga ishora qilgan hook va ruxsatlar. To'liq tozalash `-Reset` ga
o'tdi va `-Apply` bilan birga `-ConfirmReset` talab qiladi. `-Project`
va `-IncludeAuth` faqat `-Reset` bilan. Yangi `-Uninstall` o'z
yozuvlarini olib tashlaydi. Yangi `install/restore_backup.py` eski
o'rnatuvchidan keyin zaxiradan tiklaydi.

**Nega.** Bitta skill o'rnatish uchun foydalanuvchining butun Claude Code
sozlamasi ketardi: boshqa skilllar, o'z aktyorlari, global `CLAUDE.md`,
komandalar va pluginlar. Zaxira bor edi, lekin zaxirada birliklar
`<ota>--<nom>` nomi bilan yotadi, ya'ni qaytarish qo'lda va oson emas.
Zarar hajmi foyda hajmidan kattaroq edi. Qo'shuvchi birlashtirish
(`merge_settings.py`) allaqachon yozilgan va sinalgan edi, u faqat
`-Update` ortida turardi.

**Rad etilgan variantlar.**

- *Sukutni qoldirib, hujjatda ogohlantirish.* Rad etildi: ogohlantirish
  o'qilmaganda ham ma'lumot ketadi, qaytarish esa qo'lda.
- *Interaktiv tasdiq (`Read-Host`).* Rad etildi: CI va agent sessiyasi
  interaktiv emas, u yerda so'rov osilib qolardi yoki bo'sh javob olardi.
  Shuning uchun tasdiq bayroq: `-ConfirmReset`.
- *`-Update` ni sukut qilib, `-Update` bayrog'ini olib tashlash.* Rad
  etildi: eski buyruqlar, hujjatlar va CI qadamlari buzilardi. `-Update`
  qabul qilinaveradi va hech narsani o'zgartirmaydi.
- *`-Uninstall` ni butunlay PowerShell da yozish.* Rad etildi:
  PowerShell 5.1 da `ConvertFrom-Json` `PSCustomObject` beradi, uni
  o'zgartirish uchun butun daraxt qayta qurilishi kerak va bitta
  elementli massiv skalyarga aylanib ketadi; u qism agent sessiyasida
  sinalmaydi ham. JSON qismi `install/uninstall_settings.py` da,
  `tools/test_uninstall_settings.py` bilan.
- *`-Uninstall` da klon yo'lini `Resolve-Path` qilish.* Rad etildi:
  bayroq aynan klon o'chirilgan yoki ko'chirilgan holat uchun kerak.
  Yo'l satr sifatida solishtiriladi, Python skripti esa `$PSScriptRoot`
  dan olinadi, `-GeniusPath` dan emas.

**Xavf.** Foydalanuvchi sozlamasini o'chirish va yozish. Ikki tomoni bor.
Birinchisi: `-Reset` baribir o'chiradi, shuning uchun u ikki bayroq
ortida. Ikkinchisi: qo'shuvchi birlashtirish buzuq `settings.json`
yozsa, Claude Code sozlamasiz qoladi. Shuning uchun `merge_settings.py`
atomik yozadi (vaqtinchalik fayl va `os.replace`), BOM siz yozadi va
buzuq kirishda hech narsa yozmasdan 1 qaytaradi. `-Uninstall` ham avval
zaxira oladi.

**Qaysi tekshiruv o'tdi.**

- `tools/test_merge_settings.py` (14), `tools/test_uninstall_settings.py`
  (12), `tools/test_restore_backup.py` (12),
  `tools/test_rewrite_paths.py` (29, ichida ps1 hook jadvalining
  `.claude/settings.json` ga mosligi).
- `python3 tools/check_docs.py`, `eval_skill.py`, `eval_find.py`,
  `cost_report.py`.
- `.ps1` lokal yurgizilmadi: repo qoidasi PowerShell ni taqiqlaydi.
  Statik tekshirildi (satr va izoh hisobga olingan holda qavs balansi,
  o'zgaruvchi e'lon tartibi). Haqiqiy xulq CI da: `installer` job
  `windows-latest` da PowerShell 5.1 va pwsh 7 bilan quruq yurish,
  qo'shuvchi `-Apply`, `-Update -Apply`, `-Reset` (tasdiqsiz rad
  etilishi va tasdiq bilan o'chishi) va `-Uninstall` (klon o'chirilgan
  holatda) qadamlarini yurgizadi.

**Orqaga qaytarish.** `git revert` shu commitlar uchun. Eski sukut xulq
kerak bo'lsa `-Reset -ConfirmReset` aynan o'sha ishni qiladi, ya'ni
xulqni qaytarish uchun kodga tegish shart emas. Allaqachon o'chirilgan
sozlama `python3 install/restore_backup.py <zaxira>` bilan qaytariladi.

## 2026-10-05: Hooklar faqat Java proyektida va klonda ishlaydi

**Nima o'zgardi.** Har hook buyrug'i oxiriga ` || exit 0` qo'shildi.
`tools/hookio.py` ga `active()` qo'shildi va u olti hook kirish yo'lida
chaqiriladi: hook faqat qo'llanma klonida yoki Java proyektida
(ildizida yoki birinchi darajali papkasida Maven yoki Gradle fayli
bo'lgan repoda) ish qiladi. `GENIUS_HOOKS=off` hammasini o'chiradi.

**Nega.** Ikki nosozlik. Birinchisi: global o'rnatishda hook buyrug'i
klonga mutlaq yo'l bilan bog'langan, klon o'chsa Python 2 kodida
chiqadi, Claude Code esa hookdan kelgan 2 ni to'siq deb oladi; natijada
`PreToolUse` da har `Read` va `Bash` to'silib, Claude Code hamma
proyektda ishlamay qolardi. Ikkinchisi: hooklar har proyektda yurardi,
Python yoki JS proyektida ham: `docker` va `psql` to'silardi, Java
bo'limlari taklif qilinardi va har chaqiruvga Python ishga tushishi
qo'shilardi.

**Rad etilgan variantlar.**

- *Hooklarni faqat klonda yoqish.* Rad etildi: global o'rnatishning
  butun maqsadi boshqa Java proyektlarida ishlash.
- *`docref.in_clone()` dan foydalanish.* Rad etildi: u joriy papkaga
  qaraydi, hook jarayonining papkasi esa proyekt ildizi bo'lishi shart
  emas. Ildiz `CLAUDE_PROJECT_DIR` dan, u bo'lmasa payload dagi `cwd`
  dan olinadi.
- *`src/` yoki `.java` fayli borligini belgi qilish.* Rad etildi: boshqa
  tilli repoda ham shunday papka uchraydi. Belgi yig'uvchi fayl:
  `pom.xml`, `build.gradle`, `build.gradle.kts`, `settings.gradle`,
  `settings.gradle.kts`.
- *Ikkinchi darajali papkalarni ham qarash.* Rad etildi: unda deyarli
  har monorepo faol bo'lardi. Faqat ildiz va birinchi daraja.
- *`|| exit 0` ni `HookCmd` ichiga qo'yish.* Rad etildi: `handoff.py` va
  `usage.py` ga argument qo'shiladi va u suffiksdan oldin turishi kerak.

**Xavf.** Hook xulqi. Ildiz aniqlanmasa hook NOFAOL bo'ladi, ya'ni
noaniqlikda to'smaydi: bu ataylab, chunki to'sib qo'yish Claude Code ni
butunlay ishlatmay qo'yishi mumkin. Buning narxi: ildiz aniqlanmagan
Java proyektida qo'riqchi jim o'tadi. `|| exit 0` hech qanday
tekshiruvni yo'qotmaydi, chunki hooklarning hammasi to'siqni JSON orqali
beradi, chiqish kodi orqali emas.

**Qaysi tekshiruv o'tdi.** `tools/test_hookio.py` (28, ichida 16 gating
holati), `tools/test_guard.py` (119), `tools/test_check_code.py` (57),
`tools/test_suggest.py` (73), `test_budget`, `test_handoff`,
`test_usage`. Qo'lda:
`bash -c 'python3 /yoq/papka/guard.py </dev/null || exit 0'` 0
qaytaradi, `settings.json` dagi buyruq shakli bilan ham. CI dagi
`installer` job hook tekshiruvini `CLAUDE_PROJECT_DIR` bilan yurgizadi.

**Orqaga qaytarish.** `git revert`. Yoki vaqtincha: `active()` har doim
`True` qaytarsa eski xulq qaytadi, `|| exit 0` esa alohida va zararsiz.

## 2026-10-05: Qimmat amal to'silmaydi, foydalanuvchi qaroriga qo'yiladi

**Nima o'zgardi.** `tools/guard.py` da konteyner ko'tarish/yig'ish, baza
klienti va PowerShell skripti uchun `permissionDecision` `deny` emas
`ask`. `COST_OK=1` qochish yo'li olib tashlandi. Katta `docs/` bo'lagini
butun o'qish `deny` bo'lib qoldi.

**Nega.** `COST_OK=1` prefiksini modelning o'zi qo'yardi, ya'ni to'siq
o'zini-o'zi ochadigan to'siq edi. Qaysi chaqiruv haqiqatan kerakligini
faqat odam biladi, shuning uchun qaror egasi almashdi. Katta bo'lakni
o'qish esa boshqa toifa: u kontekstni himoya qiladi, odam qarorini
talab qilmaydi va arzon yo'l (`doc.sh show`) har doim bir xil.

**Rad etilgan variantlar.**

- *`deny` ni qoldirib, `COST_OK` ni saqlash.* Rad etildi: yuqoridagi
  sabab.
- *Hammasini `ask` qilish, o'qish to'sig'i ham.* Rad etildi: bob o'qish
  har sessiyada o'nlab marta uchraydi, har biriga so'rov chiqarish
  foydalanuvchini so'rov bosqichiga aylantiradi, arzon yo'l esa aniq.
- *`allow` qilib, faqat eslatma berish.* Rad etildi: eslatma
  bajarilgandan keyin keladi, pul va vaqt allaqachon ketgan bo'ladi.

**Xavf.** Ruxsat qarori (permission gate). `ask` ko'proq so'rov
chiqaradi, ya'ni ishni sekinlashtiradi. Buning o'rniga sabab matni
qisqartirildi: nega qimmat va arzon yo'l qaysi, ikki-uch qatorda.
Tashxis buyruqlari (`docker ps`, `docker logs`, `psql --version`)
avvalgidek so'ralmaydi.

**Qaysi tekshiruv o'tdi.** `tools/test_guard.py` 119/119 (45 holat `ask`
ga o'tdi, 21 ta `deny` bo'lib qoldi). Mezonlar qo'lda tekshirildi:
`docker run x`, `psql db`, `./x.ps1`, `pwsh -File x` -> `ask`;
`docker ps`, `docker logs x` -> chiqish yo'q; `COST_OK=1 docker run x`
-> `ask`; katta bobni butun o'qish -> `deny`.

**Orqaga qaytarish.** `git revert`. Qarorni qaytarish uchun `ask()`
chaqiruvlarini `deny()` ga almashtirish ham yetadi, lekin unda `COST_OK`
ham qaytarilishi kerak, aks holda yo'l butunlay yopiladi.
