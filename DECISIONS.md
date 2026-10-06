# Qaror yozuvlari

Xulqni o'zgartirgan, orqaga qaytarish yo'li aniq bo'lishi kerak qarorlar.
Har yozuv bir xil shaklda: nima o'zgardi, nega, rad etilgan variantlar,
xavf, qaysi tekshiruv o'tdi, orqaga qaytarish.

Hamma o'zgarish bu yerga yozilmaydi. Yoziladigani: foydalanuvchi
muhitiga tegadigan, ma'lumot yo'qotishi mumkin bo'lgan yoki ruxsat
qarorini o'zgartiradigan o'zgarish.

## 2026-10-06: Global o'rnatishda hooklar pin qilingan snapshotdan yuradi, yangilash tasdiq bilan

**Nima o'zgardi.** Hook buyruqlari, `permissions.allow`, `<docs>`
`additionalDirectories` yozuvi va skill matnidagi `tools/` yo'llari klonning
ishchi daraxtiga emas, `~/.claude/genius/<sha12>/` ga ishora qiladi. U
`git worktree add --detach` bilan HEAD commitdan yasaladi (butun daraxt,
`install/snapshot.py`; `install.py` va `manguberdi.ps1` bir xil joy va bir
xil buyruqni undan oladi), indeks unda bir marta quriladi. Yoziladigan
narsa snapshotga emas, klonga ketadi: o'rnatuvchi `settings.json` `env` ga
`GENIUS_CLONE` yozadi va `geniuslib.clone_root` / `state_dir` shuni
o'qiydi, faqat ROOT `~/.claude/genius/<12 hex>` bo'lsa (klonning o'zi va
`.claude/worktrees/genius-x` o'z daraxtiga yozadi). `<klon>/memory` `additionalDirectories` da qoladi. Yangi
`tools/yangilash.py`: `git fetch`, `git log --oneline` va hookka tegadigan
yo'llar (`tools install .claude .github`) uchun `git diff --stat`, so'rov
(`--ha` so'ramaydi, `--faqat-korsat` hech narsa qilmaydi), tasdiqdan
keyin `merge --ff-only` va o'rnatuvchining mavjud yo'li bilan yangi
snapshot; eski snapshot bittasi qoladi, qolgani `git worktree remove`
bilan ketadi. `yangilash.py` ning o'zi ham pin qilingan: snapshotdagi
nusxa bilan yuradi (klondagi nusxa manifest bor bo'lsa to'xtaydi,
`--klondan` bilan ataylab), klon manifestdagi `clone` dan olinadi va
env yoki skript joyi undan farq qilsa xato. O'rnatuvchi o'rnatilgan
commitdan farqli sha ga o'tayotganda `log --oneline` ro'yxatini
ko'rsatadi (tasdiqsiz qo'lda yo'l ochiq qoldirilgan, SECURITY.md). `--uninstall` snapshotlarni ham olib tashlaydi (faqat
`~/.claude/genius/<12 hex>`). `merge_settings.py` va
`uninstall_settings.py` `--root` ni takroran qabul qiladi (klon va uning
snapshotlari o'zniki). Klon `.claude/settings.json` (A yo'li) o'zgarmadi.

**Nega.** Audit XV-Y1: hook yo'li klonning `tools/` iga bog'langan edi,
shuning uchun `main` ga tushgan bitta yomon commit `git pull` dan keyingi
birinchi promptdayoq, hech kim ko'rmasdan, har Java proyektda
foydalanuvchi huquqi bilan bajarilardi (34 soatda 40 commit hook
fayllariga tekkan, tashqi PR 74 daqiqada merge qilingan, tag va imzo yo'q).
Hook yangilash siyosati (audit 9-bo'lim, 12-savol): faqat tasdiq bilan.
`<asos>` sifatida klon HEAD emas, hozir ishlayotgan snapshot commiti
olinadi: aks holda qo'lda `git pull` qilingan commitlar ro'yxatda
ko'rinmay hookka o'tardi.

**Rad etilgan variantlar.**

- *Faqat `tools/` ni nusxalash.* Rad etildi: asboblar `ROOT` ni `tools/` ning
  ota papkasidan oladi va `index/`, `docs/`, `GLOSSARY.md`, `.claude/.state`
  ni shu yerdan o'qiydi, nusxa hooklarni buzardi.
- *Memory uchun `git checkout origin/main -- memory/`.* Rad etildi: lokal
  `main` origin dan orqada qolsa push rad etiladi, baribir pull kerak
  bo'ladi. Memory klonda, push shu yerdan.
- *`git archive` nusxasi worktree o'rniga.* Rad etildi: git bilan aloqasiz
  papka o'chirishda `worktree remove` qilmaydi, reestr eskirgan yozuv
  qoldiradi va doctor commitni solishtira olmaydi. (Archive faqat
  quruq yurishda, git ga yozmaslik uchun ishlatiladi.)
- *Barqaror `~/.claude/genius/current` symlinki.* Rad etildi: hook yo'li
  o'zgarmasa o'zgarish `settings.json` da ko'rinmaydi, almashtirish esa
  tasdiqsiz bo'lib qolishi mumkin; sha yo'li o'zi tasdiq izi. Narxi: `run_tests.py`
  opt-in qoidasi har yangilashdan keyin qayta qo'shiladi.
- *Avtomatik yangilash.* Rad etildi (12-savol qarori: faqat tasdiq bilan).
- *Klondan yurgan `yangilash.py` ni snapshotdan qayta exec qilish.* Rad
  etildi: stdin va argumentlarni ko'chirish nozik, to'xtatib yo'lni
  aytish soddaroq va xavfsizroq.
- *Ikki klon uchun sha ga klon identifikatori qo'shish (`<sha12>-<klon>`).*
  Rad etildi: spetsifikatsiya joyi `<sha12>`; boshqa klon yasagan snapshotga
  `yarat` xato beradi.
- *`GENIUS_CLONE` o'rniga `GENIUS_STATE_DIR` va `GENIUS_MEMORY_DIR` ni
  alohida yozish.* Rad etildi: memory yo'li (`umumiy`, `claude-genius`)
  klondan olinadi, uchta o'zgaruvchi esa har yangilashda uch joyda
  mos kelishi kerak bo'lardi. `GENIUS_STATE_DIR` baribir ustun.

**Xavf.** Yozuvchilar ro'yxati: holat papkasi (`budget.py`, `state.py`,
`usage.py` ham `.claude/usage`, `handoff.py`, `hookio.py`, `actor_check.py`,
`run_tests.py`), memory (`docref.py`, `rules_for.py`, `guard.py` ning git
tekshiruvi, `handoff.py`), `hookio.active()`. Shulardan biri `ROOT` ga
tushib qolsa snapshotga yozilardi: `tools/test_yangilash.py` snapshotda
`.claude/.state`, `usage` va memory yo'qligini tekshiradi. Klon o'chsa
`GENIUS_CLONE` e'tiborsiz qolib yozuv snapshotga tushadi (doctor
ogohlantiradi). Snapshot HEAD dan olinadi, commit qilinmagan o'zgarish
kirmaydi (o'rnatuvchi ogohlantiradi). Ikki klon bir sha da bitta
snapshotni ulasha olmaydi: ikkinchisining `yarat` i xato beradi. Tasdiq odam o'qishiga tayanadi: `--ha`
himoyani olib tashlaydi. ps1 va Windows dagi `yangilash.py` yo'li agent
sessiyasida yurmaydi, faqat CI va matn paritet testlari.

**Qaysi tekshiruv o'tdi.** `tools/test_yangilash.py` 64/64 (o'rnatish
snapshot yasaydi, `git pull` dan keyin `sha256sum snapshot/tools/*.py`
o'zgarmaydi, `--faqat-korsat` va rad etish hech narsa o'zgartirmaydi,
tasdiqda ff-merge va yangi snapshot va settings, eski bittasi qoladi va
keyingisida tozalanadi, iflos klon, detached HEAD va ajralgan tarixda
to'xtaydi, memory va holat klonga tushadi, snapshot o'zgartirilgan yoki
qo'lda o'chirilgan holat), `tools/test_install.py` 126/126 (snapshot,
paritet snapshot joyi, eski o'rnatishdan o'tish, yetim snapshot,
`--uninstall`), `tools/test_rewrite_paths.py` 39/39 (ps1 hook yo'li
snapshotga, `--clone` va `--root-keyin`), `test_merge_settings` 19/19,
`test_uninstall_settings` 14/14, `test_doctor` 12/12, `test_budget` 40/40,
`run_all_tests.py` (32 suite), `check_docs.py`, `eval_skill.py`. CI
`-Uninstall` qadamlari snapshot yozuvi qolmaganini ham tekshiradi.

**Orqaga qaytarish.** Avval joriy kod bilan `python3 install/install.py
--uninstall --apply` (u snapshot yozuvlari va worktree larni oladi:
eski kod ularni o'zniki deb tanimaydi), so'ng `git revert` va o'rnatuvchini
qayta yurgizish: hook yo'llari klonga qaytadi. Faqat shu yangilanishdan
keyin nimadir buzilsa: o'rnatuvchi zaxirasidagi `.claude--settings.json`
ni qaytaring, u qoldirilgan eski snapshotga ishora qiladi.

## 2026-10-06: Aktyor javobi SubagentStop hooki bilan tekshiriladi

**Nima o'zgardi.** Yangi `tools/actor_check.py` `SubagentStop` hookiga
ulandi (`.claude/settings.json` va `install/manguberdi.ps1`, matcher
siz). Aktyor turi `dasturchi` yoki `test-muhandis` bo'lsa va u kod
fayliga Edit/Write qilgan bo'lsa, ikki narsa talab qilinadi: javobda
`run_tests exit=<kod>` qatori va oxirgi tahrirdan keyin `run_tests.py`
jurnalida (`<holat>/run_tests.jsonl`) tahrirlangan fayl turgan ildiz
uchun yozuv (guruhda worktree papkasi; `isitish` sanalmaydi). Biri
bo'lmasa `{"decision": "block", "reason": ...}`: aktyor shu chaqiruv
ichida davom etadi. Shu bilan PreToolUse budjet matcheri
`Task|Agent|SendMessage` bo'ldi (PL-CC7 qolgani).

**Nega.** Aktyor ish oxirida test yurgizishi va javob shakli faqat
matnda yozilgan edi. Test yurgizmay "bajarildi" degan aktyorning xatosi
partiya oxiridagi to'liq suite gacha ko'rinmasdi, u yerda esa egasining
budjeti tugagan bo'lishi mumkin (OK-O14). `block` yangi Agent chaqiruvi
emas, ya'ni budjetga tushmaydi. SendMessage tugagan aktyorni yangi Agent
chaqiruvisiz qayta yurgizadi, matcher uni ushlamasa budget.py dagi
SendMessage qismi hech qachon ishga tushmasdi.

**Rad etilgan variantlar.**

- *Matcher `dasturchi|test-muhandis`.* Rad etildi: payloadda
  `agent_type` bo'lmagan versiyada hook umuman chaqirilmasligi mumkin
  edi, skript esa turni `agent-<id>.meta.json` va asosiy transkriptdagi
  oxirgi Agent chaqiruvidan ham oladi. Narxi: har subagent to'xtashida
  ~40 ms Python.
- *Budjetni PostToolUseFailure bilan avtomatik qaytarish.* Rad etildi:
  yomon natija qaytargan aktyor asbob nuqtai nazaridan muvaffaqiyatli,
  foydalanuvchi to'xtatgan holatni ham qamramaydi; `--tiklash` qo'lda
  qoladi.
- *Faqat javob qatorini tekshirish.* Rad etildi: qatorni yozish arzon,
  jurnal yozuvi esa `run_tests.py` haqiqatan yurganini ko'rsatadi.

**Xavf.** Yolg'on to'siq bitta qo'shimcha navbat narxida:
`stop_hook_active` bo'lsa hook jim, ikkinchi to'xtash o'tadi. Faqat
hujjat (`.md`, `.txt`, `.rst`, `.adoc`) tegilgan, tahrir yo'q,
transkript o'qilmagan yoki `run_tests` "Ta'sirlangan test yo'q" degan
(jurnalga yozuv tushmaydi) holatlarda jim. `hookio.active()` false
bo'lsa, ya'ni Java proyekti emas, jim. Jurnal klon holat papkasida:
`GENIUS_STATE_DIR` hook va aktyor Bash ida bir xil bo'lishi kerak.

**Qaysi tekshiruv o'tdi.** `tools/test_actor_check.py` 31/31 (block,
o'tish, eski va begona ildiz yozuvi, isitish, worktree ildizi,
test-muhandis, boshqa aktyor, prefiks, `stop_hook_active`, nofaol,
hujjat, tahrirsiz, fail-open, maydon zaxiralari, jarayon chegarasi),
`tools/test_skill.py` (SubagentStop matcheri agent nomi, actor_check
ulangan, budget matcherida SendMessage), `tools/test_rewrite_paths.py`
(ps1 paritet), `tools/doctor.py` (yangi `SubagentStop.json` namunasi).

**Orqaga qaytarish.** Ikkala fayldan `SubagentStop` blokini olib
tashlash (paritet testi ikkalasini birga talab qiladi); `test_skill.py`
dagi `EVENT_MUST_WIRE` yozuvi ham. Vaqtincha: `GENIUS_HOOKS=off`.

## 2026-10-06: Guruh joriy holatdan, worktree loyiha ichida

**Nima o'zgardi.** `guruh.py yarat` asos sifatida HEAD o'rniga joriy
holatning vaqtinchalik commitini oladi: alohida `GIT_INDEX_FILE` (asosiy
indeks nusxasi) bilan `git add -A`, `write-tree`, `commit-tree <tree> -p
HEAD`. Asosiy branch, indeks va ishchi daraxt o'zgarmaydi; daraxt HEAD
niki bilan bir xil bo'lsa HEAD ning o'zi asos. Iflos daraxt endi rad
etilmaydi. Sukut worktree joyi `<root>/.claude/worktrees/genius-<id>`;
`yarat` birinchi marta `<git-common-dir>/info/exclude` ga
`.claude/worktrees/` qatorini qo'shadi. `GENIUS_GURUH_DIR` berilsa eski
`<papka>/<repo>.guruh-<id>` nomi. `birlashtir` qo'llagan fayllarini holat
faylida `files` sifatida saqlaydi, `royxat --fayllar` har guruh ostida
fayllarini beradi. `parallel.md` tartibi: birlashtir, to'liq suite
(fonda), egani `royxat --fayllar` bo'yicha topish, keyin tozala.

**Nega.** Rejalashtiruvchi REJA.md ni commit qilmaydi va birlashtirish
commit qilmaydi, ya'ni L zanjirida va har ikkinchi partiyada daraxt
iflos edi va `yarat` rad etardi: parallel rejim amalda hech qachon
yoqilmasdi (OK-T-K4). Qo'shni papkadagi worktree ga Edit va Write
ishchi papkadan tashqarida, Claude Code ruxsat so'raydi va "savolsiz
zanjir" to'xtaydi (OK-O13). `royxat` fayl nomini bermasdi, yiqilgan
testni guruhga bog'lab bo'lmasdi (OK-T-K1).

**Rad etilgan variantlar.**

- *`.gitignore` ga `.claude/worktrees/`.* Rad etildi: proyekt faylini
  o'zgartirish daraxtni o'zi iflos qiladi va foydalanuvchi reposiga
  tushadi. `info/exclude` lokal va commit qilinmaydi.
- *Asosiy daraxtda `git stash` yoki vaqtinchalik commit.* Rad etildi:
  foydalanuvchi branchi va stash steki o'zgaradi, parallel sessiyalar
  bilan to'qnashadi.
- *`additionalDirectories` ga qo'shni papka.* Rad etildi: o'rnatuvchi va
  har proyekt sozlamasiga tegadi, loyiha ichidagi joy bunga hojat
  qoldirmaydi.

**Xavf.** Vaqtinchalik commit `genius/<id>` branchida; `tozala` dan
keyin u yetim va `git gc` uni oladi. Asosiy daraxtda untracked bo'lgan
faylni guruh o'zgartirsa `apply --index` uni qo'llay olmaydi va kesishish
deb aytadi (`--3way` yo'li). Katta repoda `add -A` asosiy indeks
nusxasidan boshlanadi, shuning uchun faqat o'zgargan fayllar xeshlanadi.
Ichki worktree papkasini `.claude/worktrees/` ni bilmaydigan boshqa
vosita (masalan IDE indeksi) ko'rishi mumkin.

**Qaysi tekshiruv o'tdi.** `tools/test_guruh.py` 29/29, yangi: untracked
REJA.md va commit qilinmagan tahrir bilan `yarat` (asosiy HEAD va indeks
o'zgarmaydi), birlashtirilgan partiyadan keyingi ikkinchi partiya, ikki
guruh ichki papkada (`info/exclude` bir marta, `.gitignore` yo'q),
`royxat --fayllar`.

**Orqaga qaytarish.** `git revert`. Vaqtincha eski joy:
`GENIUS_GURUH_DIR=<repo ota papkasi>`.

## 2026-10-06: Boshqa proyekt memorysi klondan tashqarida, handoff lokal

**Nima o'zgardi.** Global o'rnatishda (joriy proyekt klonning o'zi
bo'lmasa) proyekt memorysi `GENIUS_MEMORY_DIR` da, sukut bo'yicha
`~/.claude/genius-memory/<slug>/`, push siz. Klonga faqat
`memory/umumiy/` va `memory/claude-genius/` yoziladi. Joyni
`docref.memory_dir` hal qiladi, `rules_for.past_mistakes` va `handoff`
shu funksiyani ishlatadi. `guard.py`: klondagi begona `memory/<slug>/`
ga tegadigan `git add` yoki `git commit` (`add -A`, `add .`,
`commit -a` ham, klonda begona papka bo'lsa) `ask`. `handoff.py
--prompt` fakt qismini o'zi yig'adi (`git diff --stat HEAD`, git da yo'q
fayllar, REJA.md `[x]` va `[ ]`); `--vazifa <nom>` topshiriqni lokal
sessiyada `.claude/.state/handoff/<nom>.md` ga git siz yozadi, bulut
sessiyasida (`CLAUDE_CODE_REMOTE`) proyekt memorysiga. `--memory` ikki
indeksni bitta chaqiruvda beradi, manguberdi uni ish boshida o'qiydi.
`memory/README.md` dagi git buyruqlari `git -C <memory ildizi>` bilan.
Mayda: handoff holati `GENIUS_STATE_DIR` ni hurmat qiladi, tmp nomida
pid; `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` chegarani siqish nuqtasiga
tushiradi.

**Nega.** Klon ochiq GitHub repo, global o'rnatishda esa hamma Java
proyekt shu klonni ishlatadi. Eski qoida topshiriqning Maqsad, Qarorlar
maydonlarini `memory/<proyekt-slug>/` ga yozib push qilardi: xususiy
proyekt nomi, qarorlari va fayl yo'llari ochiq tarixga tushardi va
o'chirish qimmat (JR-J6, OC-K4, OK-T-K3, XV-Y3). Git buyruqlari `-C`
siz edi, ya'ni ish proyektida yurardi (OC-T-Q2). Handoff har uzatishda
memory fayl, indeks, commit, push va o'chirishga 4-6 navbat sarflardi
(OK-O17).

**Rad etilgan variantlar.**

- *`.gitignore` da `memory/*/`.* Rad etildi: yozuv jim lokal qolardi,
  foydalanuvchi buni bilmasdi, `umumiy/` uchun istisno ham mo'rt.
- *Proyekt memorysini proyektning o'zida (`<proyekt>/.claude/memory/`)
  saqlash.* Rad etildi: u proyekt reposiga tushishi mumkin, jamoa
  reposida esa shaxsiy eslatma begona.
- *Push ni butunlay olib tashlash.* Rad etildi: cloud sessiyasida klon
  memorysi yo'qolardi. Push klondagi ikki papka uchun qoladi.
- *Handoff ni har doim memoryga yozish.* Rad etildi: bu bir martalik
  vazifa tafsiloti, memory darvozasining 1-savoliga zid.

**Xavf.** Ma'lumot joyi o'zgaradi. Oldin klonda `memory/<slug>/` bo'lsa,
endi u boshqa proyektdan o'qilmaydi: uni qo'lda
`~/.claude/genius-memory/` ga ko'chirish kerak. Bulut sessiyasida
`GENIUS_MEMORY_DIR` git da bo'lmasa yozuv konteyner bilan yo'qoladi,
asbob buni aytadi. `GENIUS_MEMORY_DIR` dagi topic faylni Read bilan
ochish ruxsat so'rashi mumkin (`additionalDirectories` da emas).
Guard to'sig'i odatga qarshi: `bash -c` ichini ko'rmaydi.

**Qaysi tekshiruv o'tdi.** `tools/test_handoff.py` 29/29 (8 yangi:
PCT, GENIUS_STATE_DIR va pid, fakt qismi, lokal va bulut topshirig'i,
memory joyi), `tools/test_rules_for.py` 84/84 (GENIUS_MEMORY_DIR),
`tools/test_guard.py` 209/209 (begona slug `add` va `commit` -> `ask`,
umumiy va claude-genius -> o'tadi). O'rnatilgan `manguberdi` skill
matnida `<klon>/memory/<proyekt-slug>` yo'q (`rewrite_paths` bilan
sinaldi). Aktyor fayli `rejalashtiruvchi.md` dagi o'qish qatori bu
o'zgarishga kirmadi.

**Orqaga qaytarish.** `git revert`. Vaqtincha: `GENIUS_MEMORY_DIR` ni
`<klon>/memory` ga qo'yish eski joyni qaytaradi (push qoidasisiz).

## 2026-10-05: Gradle yurishiga init skript: jacoco, XML, kompilyatsiya keshi

**Nima o'zgardi.** `run_tests.py` har Gradle buyrug'iga `-I <init skript>`
qo'shadi. Skript build fayllariga tegmaydi va faqat shu yurishga ta'sir
qiladi.

1. Maqsadli yurishda (va qayta yurishda) jacoco agenti, `JacocoReport`
   va `JacocoCoverageVerification` vazifalari o'chadi, HTML test
   hisoboti yozilmaydi.
2. Har yurishda JUnit XML majburiy.
3. Loyiha `org.gradle.caching` ni tanlamagan bo'lsa asbob `--build-cache`
   ni yoqadi. Faqat kompilyatsiya vazifalari (`AbstractCompile`, Kotlin
   compile) cache lanadi va faqat lokal. Remote cache shu yurish uchun
   `beforeSettings` ichidan o'chiriladi, shuning uchun
   `GRADLE_USER_HOME/init.d` sozlagan remote ham o'chadi.
4. `--isit` skript ro'yxatga olgan `geniusIsit` vazifasini chaqiradi. U
   har Test vazifasining test sinflarini (va ular talab qilgan main ni)
   quradi. Nom papkadan taxmin qilinmaydi; jmh yoki Spring AOT kabi test
   emas source set qurilmaydi.

Skript loyihaning `.gradle/genius/` papkasida turadi va nisbiy yo'l bilan
beriladi. Init qo'shilmaydigan holatlar:

- `GENIUS_GRADLE_INIT=0`;
- wrapper Gradle 6.1 dan eski;
- isolated projects yoqilgan.

Wrapper versiyasi o'qilmasa init qo'shiladi, lekin cache yoqilmaydi.

Yo'l-yo'lakay tuzatilganlar:

- Kesh tanlovi `-Dorg.gradle.caching` ni (GENIUS_TEST_FLAGS, GRADLE_OPTS,
  JAVA_OPTS) ham ko'radi.
- `gradle.properties` da `:` va bo'shliq ajratgichi o'qiladi;
  `GRADLE_USER_HOME` dagi qiymat loyihanikidan ustun.
- Versiya faqat `distributionUrl` dan olinadi, izohdagi eski URL dan
  emas.
- `includeBuild` papkasi modul sifatida `:<nom>:test` ga bog'lanadi.
  Avval u ildizning `:test` iga tushardi: ildizda java bo'lsa yurish
  testsiz "yashil" chiqardi. Nom papka nomidan (Gradle shunday chaqiradi,
  `rootProject.name` dan emas) yoki `{ name = '...' }` dan olinadi.
  Included build ichidagi included build ham hisobga olinadi, uning ildiz
  fayllari (`settings.gradle`, `build.gradle`, `gradle.properties`)
  o'zgarsa reja to'liq suite bo'ladi. Faqat included build li ildizda
  `test` va `geniusIsit` selektori ishlatilmaydi. Gradle 6.8 dan eski
  bo'lsa bog'lash yo'q.
- Ildiz include lari dinamik bo'lsa (`listOf(...).forEach { include(it) }`)
  modul avvalgidek eng yaqin build fayli bo'yicha topiladi.
- `src/integration-test/java` kabi papkaning vazifa nomi build
  skriptidagi `srcDir` ni o'rab turgan blokdan, topilmasa camelCase
  dan olinadi (`integrationTest`). Avval `:orders:integration-test`
  "Task not found" bilan yiqilardi.
- Test emas vazifa (coverage, lint) yiqilgan bo'lsa, qayta yurishda
  o'tgan test natijani `4` qilmaydi: `exit=1` va `Boshqa yiqilish:`
  qatori. Maven da: surefire va failsafe dan boshqa goal; yiqilgan
  sinfi yo'q moduldagi surefire yiqilishi (fork qulashi); `-fae` da
  SKIPPED modul. Formatlash qadami yiqilishi hisobga olinmaydi.
- `--tashxis` ga Gradle bandlari qo'shildi. Build scan bandi faqat
  yuklash haqiqatan yoqilganda chiqadi.

**Nega.** Maven maqsadli yurishi `-Djacoco.skip=true` bilan tezlashgan
edi, Gradle da bunday xossa yo'q. Ko'p loyihada `test` ga
`finalizedBy jacocoTestCoverageVerification` bog'langan. Shunda maqsadli
yurish bir nechta test bilan coverage chegarasiga yetmay yolg'on
yiqiladi. Buni Gradle 7.6, 8.14 va 9.8 da qayta hosil qildim. Eski exec
fayli qolgan bo'lsa hisobot vazifasi agentsiz ham yiqitardi, shuning
uchun vazifalarning o'zi o'chiriladi.

Yangi worktree birinchi yurishda hamma modulni noldan kompilyatsiya
qilardi. Endi boshqa daraxt kompilyatsiya qilgan modul cache dan
olinadi. Sintetik 2500 sinfli loyihada:

- yangi worktree kompilyatsiyasi 5.3 s dan 2.8 s ga tushdi;
- maqsadli yurish 3.0 s dan 1.7 s ga tushdi.

Qayta yurish va beqarorni ajratish JUnit XML ga tayanadi, shuning uchun
XML majburiy.

**Rad etilgan variantlar.**

- *To'liq `--build-cache` (test vazifasi bilan).* Rad etildi: test
  vazifasi kirish sifatida muhit o'zgaruvchisi va tashqi holatni
  bilmaydi, cache dan olingan "yashil" haqiqiy yurish emas. Oldingi
  yozuvdagi rad etish shu sabab bilan qoladi. Qabul qilingani torroq:
  kirish va chiqishini Gradle va JetBrains e'lon qilgan kompilyatsiya
  vazifalari. Ularning cache kaliti UP-TO-DATE tekshiruvi bilan bir xil
  kirishlardan olinadi.
- *Build fayliga `jacoco { enabled = false }` yozish.* Rad etildi: asbob
  foydalanuvchi kodini o'zgartirmaydi.
- *`-x jacocoTestReport -x jacocoTestCoverageVerification`.* Rad etildi:
  vazifa yo'q loyihada `-x` "Task not found" bilan yiqiladi, agentni esa
  o'chirmaydi.
- *Skript umumiy `/tmp` da.* Rad etildi:
  - oldindan ma'lum nomli faylni boshqa lokal foydalanuvchi oldindan
    qo'yib, Gradle orqali kod bajartirishi mumkin;
  - Windows da TEMP dagi `&` yoki `^` `cmd /c` buyrug'ini bo'ladi.
- *`--parallel`, `--configuration-cache` standart.* Rad etildi, oldingi
  yozuvdagi sabab bilan: to'g'riligi build ga bog'liq. `--tashxis` ularni
  tavsiya qiladi, yoqish `GENIUS_TEST_FLAGS` bilan.
- *`--no-scan` standart.* Rad etildi: build scan tashkilot tanlovi.
  `--tashxis` aytadi, yoqish `GENIUS_TEST_FLAGS=--no-scan` bilan.

**Xavf.**

- Kompilyatsiya cache i `.java` dan tashqari faylni (masalan
  `lombok.config`) o'qiydigan annotation processor da eskirgan sinf
  qaytarishi mumkin. Bu xavf UP-TO-DATE tekshiruvida ham bor, cache uni
  worktree lar orasiga yoyadi. Loyihaning `org.gradle.caching=false`
  qiymati uni to'liq o'chiradi.
- Loyiha `org.gradle.caching=true` qilgan bo'lsa uning sozlamasi amal
  qiladi: o'zgarmagan test natijasi ham cache dan keladi.
- `.gradle/` gitignore da bo'lmasa skript fayli untracked ko'rinadi.
  Gradle bu papkaga baribir yozadi.
- Kotlin compile cache i faqat qo'lda tekshirildi (review agenti, KGP
  2.0.21, Gradle 8.14.3: ikkinchi worktree da `compileKotlin FROM-CACHE`).
  Avtomatik sinov yo'q.

**Qaysi tekshiruv o'tdi.**

- `tools/test_run_tests.py`: 54/54.
- `python3 tools/test_run_tests.py --gradle <gradle>` haqiqiy Gradle
  7.6.4 (JDK 17), 8.14.3 va 9.8.0 (JDK 21) da 12/12:
  - init siz maqsadli yurish yiqiladi (nazorat);
  - init bilan, eski exec turganda ham, yashil: agent va HTML yo'q,
    XML bor;
  - to'liq suite da coverage tekshiruvi qoladi;
  - yangi worktree kompilyatsiyani cache dan oladi, testni esa cache dan
    olmaydi;
  - build XML ni o'chirgan bo'lsa ham yiqilgan test qayta yuradi;
  - lokal HTTP server bilan sanalganda remote ga murojaat yo'q, init.d
    sozlagan remote ham o'chadi, nazoratda esa murojaat bor;
  - loyiha cache ni o'zi tanlaganda asbob unga tegmaydi;
  - `--isit` source set nomi papka nomidan farq qilganda ham ishlaydi;
  - `src/integration-test` dagi test `:orders:integrationTest` bilan
    yuradi;
  - included build testi `:money:test` bilan yuradi, ildizda testsiz
    composite da `--isit` va `--hammasi` ham.
- `geniusIsit` configuration cache bilan: entry saqlanadi va qayta
  ishlatiladi (8.14, 9.8).
- Mustaqil review ikki bosqichda o'tdi:
  - birinchisi (5 yo'nalish, har topilmaga rad etuvchi tekshiruvchi)
    29 topilmani tasdiqladi;
  - tuzatishlarning qayta review i yana 19 tasini tasdiqladi.

  Hammasi shu yozuvdagi tuzatishlarda.
- Mutatsiya: remote o'chirish, `beforeSettings`, hisobot vazifasini
  o'chirish va XML majburiyligi olib tashlansa e2e yiqiladi.

**Orqaga qaytarish.**

- `GENIUS_GRADLE_INIT=0` init skriptni butunlay o'chiradi.
- Faqat cache ni o'chirish uchun: `org.gradle.caching=false` yoki
  `GENIUS_TEST_FLAGS=--no-build-cache`.

## 2026-10-05: Beqaror test ajratiladi, Spring orqali ta'sir tanlanadi

**Nima o'zgardi.** `run_tests.py`: (1) yiqilgan sinflar JUnit XML dan
olinadi va bir marta qayta yurgiziladi; qayta o'tsa natija `exit=4`
(beqaror), kompilyatsiya xatosida qayta yurish yo'q. (2) `@Configuration`,
filter, `@ControllerAdvice` kabi sinf o'zgarsa modulning barcha Spring
testlari, `@Entity` o'zgarsa baza testlari tanlanadi; abstrakt bazaviy
sinfdagi `@SpringBootTest` hisobga olinadi. (3) Maven maqsadli yurishida
`-Djacoco.skip=true`, verify da javadoc va source jar o'chadi. (4)
`--isit`: guruh ochilgach fonda kompilyatsiya, ildiz qulfi bilan. (5) Har
yurish jurnalga, `--hisobot` uni jamlaydi. (6) `--tashxis` Spring
kontekst ishga tushishini logdagi `Started X in N seconds` dan sanaydi.
(7) `GENIUS_TEST_FLAGS`: build ga tegmaydigan ixtiyoriy bayroqlar.

**Nega.** Tezlik va to'g'rilik bir-biriga bog'liq. Flaky test o'zgarishga
yopishtirilsa dasturchi yo'q xatoni qidiradi: bu ham sekin, ham noto'g'ri.
SecurityConfig kabi sinf hech qaysi testda nomi bilan uchramaydi, lekin
har Spring testining kontekstiga kiradi: tanlov uni o'tkazib yuborsa xato
partiya oxirida chiqadi va qo'shimcha aylana ochadi. Verify ga bog'langan
`jacoco:check` bir nechta test bilan coverage chegarasiga yetmay yolg'on
yiqilardi. Kontekst sonini taxminiy kalitdan emas, Spring Boot ning o'z
qatoridan olish aniqroq.

**Rad etilgan variantlar.**

- *Surefire `rerunFailingTestsCount`.* Rad etildi: faqat Maven da bor,
  Gradle da esa test-retry plaginini build ga qo'shish kerak. XML orqali
  ikkala asbobda bir xil xulq.
- *Beqarorni yashil deb qaytarish.* Rad etildi: o'zgargan kodga tegadigan
  beqaror test poyga xatosi bo'lishi mumkin. Kod 4 ko'rinib turadi.
- *Gradle `--build-cache`, `--configuration-cache`, `--parallel` ni
  standart yoqish.* Rad etildi: to'g'riligi build dagi vazifalar
  kirish-chiqishni to'g'ri e'lon qilganiga bog'liq, bu foydalanuvchi
  qarori. `GENIUS_TEST_FLAGS` bilan bir qatorda yoqiladi. (Keyingi
  yozuvda torroq shakli qabul qilindi: kesh faqat kompilyatsiya uchun.)
- *pmd va spotbugs ni ham o'chirish.* Rad etildi: skip kalitlarini
  manbadan tasdiqlay olmadim. Checkstyle va enforcer ataylab qoladi:
  ular arzon va xatoni erta ko'rsatadi.

**Xavf.** Qayta yurish flaky ni tasniflaydi, lekin tuzatmaydi: egasi
test-muhandis. Spring tanlovi kengroq: Spring testi ko'p modulda maqsadli
yurish modul yurishiga yaqinlashadi (filtr cheklovi uni butun vazifaga
o'tkazadi).

**Qaysi tekshiruv o'tdi.** `tools/test_run_tests.py` 42/42, beshta
mutatsiya tutildi (Spring tanlovi, ota sinf, kompilyatsiya to'sig'i,
qayta yurish doirasi, symlink yo'li). Gradle 8.14 da qo'lda: beqaror
test `exit=4`, doimiy yiqilish `exit=1` va xulosa takrorsiz, `--isit`,
`--hisobot`.

**Orqaga qaytarish.** `--qayta 0` qayta yurishni o'chiradi; qolganlari
`run_tests.py` dagi tegishli funksiyani olib tashlash bilan.

## 2026-10-05: Testlar maqsadli, to'liq suite partiyada bir marta

**Nima o'zgardi.** `tools/run_tests.py` qo'shildi: o'zgarishga ta'sir
qilgan test sinflarini tanlaydi (o'zgargan test, nomi mos, murojaat, bir
qadam narida ishlatuvchi, sozlama va migratsiya), modulga bog'langan
buyruq yasaydi va uni o'zi yurgizadi, log faylga, ekranga birinchi
sabab. `guard.py` xom to'liq suite (`./gradlew test`, `mvn verify`),
`clean`, `--rerun-tasks` va `--no-daemon` ni `deny` qiladi va shu
asbobni ko'rsatadi. To'liq suite partiyada bir marta, asosiy sessiyada.

**Nega.** Suite 5-8 daqiqa, aktyor uni 2-4 marta, guruhda 3-5 aktyor
yurgizardi. Sabab faqat odat emas, tajribada tasdiqlandi: ko'p modulli
Gradle da `test --tests X` X yo'q modulda "No tests found for given
includes" bilan yiqiladi (`failOnNoMatchingTests` standarti true), Maven
da `-Dtest=X` "No tests matching pattern" bilan. Aktyor shundan keyin
filtrsiz suite ga qaytardi. Asbob modulni o'zi qo'yadi
(`:orders:test --tests X`, `-pl orders -am -Dsurefire.failIfNoSpecifiedTests=false`),
IT ni failsafe ga beradi (`-Dit.test`, `-Dfailsafe.failIfNoSpecifiedTests=false`),
`--continue`/`-fae` bilan hamma modul yiqilishini bitta yurishda
ko'rsatadi va Maven da validate fazasidagi spring-javaformat ni oldin
qo'llaydi.

**Rad etilgan variantlar.**

- *Faqat ko'rsatma yozish ("to'liq suite yurgizmang").* Rad etildi:
  test-muhandis agentida bu allaqachon yozilgan edi va baribir
  yurgizilardi, chunki to'g'ri buyruqni yasash ko'p modulda qiyin.
- *To'siqni `ask` qilish.* Rad etildi: `ask` zanjirni odam javobini
  kutib to'xtatadi, holbuki arzon yo'l har doim bir xil.
- *Build tool plaginiga asoslangan tanlash (Gradle test impact).*
  Rad etildi: foydalanuvchi build iga tegadi. Asbob faqat manbani
  o'qiydi; xatosini partiya oxiridagi to'liq suite tutadi.

**Xavf.** Ikki. Birinchisi: tanlash taxminiy (nom va murojaat bo'yicha),
uzoq bog'liqlik o'tkazib yuborilishi mumkin; xavfsizlik to'ri partiya
oxiridagi to'liq suite. Ikkinchisi, ruxsat: o'rnatuvchi ruxsat
ro'yxatini skill matnidagi asboblardan yasaydi, shuning uchun
`run_tests.py` ham unga tushadi va u loyihaning build ini (ya'ni loyiha
kodini) har yurishda ruxsat so'ramasdan ishga tushiradi. Bu ataylab:
test yurishidagi har ruxsat so'rovi zanjirni to'xtatardi. Asbob faqat
test vazifalarini yurgizadi, ixtiyoriy Gradle yoki Maven vazifasini
emas. Testcontainers testlari konteyner ko'taradi va `guard.py` ularni
ko'rmaydi: bu avval ham shunday edi, endi esa to'liq suite partiyada
bir marta.

**Qaysi tekshiruv o'tdi.** `tools/test_run_tests.py` 26/26 (to'rtta
mutatsiya ham tutildi), `tools/test_guard.py` 138/138, haqiqiy Gradle
8.14 va Maven 3.9 fixture larida qo'lda: maqsadli yurish, bir qadam
tanlovi, ikki modul yiqilishi bitta yurishda, IT failsafe da.

**Orqaga qaytarish.** `guard.py` dagi `check_build` chaqiruvini olib
tashlash; ruxsatni olib tashlash uchun `~/.claude/settings.json` dagi
`run_tests.py` qoidasini o'chirish yoki `GENIUS_HOOKS=off`.

## 2026-10-05: Zanjir hajmga qarab, guruhlar parallel worktree da

**Nima o'zgardi.** Zanjir hajmga bog'landi: S da dasturchi o'zi
regressiya testini yozadi va review keladi; M da test muhandisi va
review parallel; L da reja va guruhlar parallel. Ikkinchi aylana faqat
`yuqori` topilmada, review to'liq qayta yurmaydi. Fayllari kesishmaydigan
guruhlar o'z git worktree sida ishlaydi (`tools/guruh.py`), budjet
`guruh: <id>` qatori bo'yicha guruhga ajratildi (`budget.py`). Zanjir
o'rtasida savol berilmaydi: qaytariladigan qarorda standart tanlanadi va
yoziladi, qaytarib bo'lmaydigani ish boshida bitta xabarda so'raladi.

**Nega.** Bitta guruh dasturchi, test muhandisi, review, keyin ikkalasi
yana bilan 40-70 daqiqa olardi va guruhlar bitta ishchi papka tufayli
ketma-ket yurardi. Budjet sessiya bo'yicha sanalardi: ikki guruh parallel
ishlasa, birinchisining ikkinchi aylanasi ikkinchisining birinchi
chaqiruvi tufayli to'silardi. Savol esa ishni javobgacha to'xtatardi
va har yangi so'rovda budjetni ham nolga tushirardi.

**Rad etilgan variantlar.**

- *Agent asbobining `isolation: worktree` i.* Rad etildi: u har
  chaqiruvga alohida worktree beradi, guruhning dasturchisi va test
  muhandisi esa bitta daraxtda ishlashi kerak.
- *Guruh branchini `git merge` bilan birlashtirish.* Rad etildi: merge
  commit foydalanuvchi branchiga tushadi. Patch (`git apply --index`)
  ish bitta daraxtda bajarilgandek natija beradi, commit qilmaydi va
  kesishganda asosiy daraxtga tegmaydi.
- *Har qanday holatda parallel.* Rad etildi: asosiy daraxt iflos bo'lsa
  guruh uni ko'rmaydi, mashina chegarasidan ortiq guruh esa hammani
  sekinlashtiradi. Shunda ketma-ket ishlanadi, savolsiz.

**Xavf.** Parallel testlar umumiy port yoki lokal bazaga tegsa bir-birini
buzadi: `run_tests.py --navbat` ularni ketma-ket qiladi, `--tashxis`
belgini ko'rsatadi. Standart bilan qabul qilingan qaror noto'g'ri
bo'lishi mumkin: shuning uchun har biri hisobotda ro'yxat bo'lib
chiqadi.

**Qaysi tekshiruv o'tdi.** `tools/test_guruh.py` 9/9, `tools/test_budget.py`
26/26, ikki worktree da parallel Gradle qo'lda.

**Orqaga qaytarish.** `references/aktyorlar.md` dagi hajm jadvalini
eski to'liq zanjirga qaytarish; guruh qatorisiz chaqiruv budjetni eski
xulqda sanaydi.

## 2026-10-05: Qidiruv dvigateli qayta yozilmaydi

**Nima o'zgardi.** Hech narsa. Bu yozuv ataylab: qaror "tegmaslik".

**Nega.** Soddalashtirish bo'yicha ko'rib chiqishda qidiruv qatlamini
SQLite yoki FTS ga ko'chirish varianti ham bor edi. Rad etildi: mavjud
dvigatel ishlaydi va o'lchangan (`eval_find.py`: taxallus bo'yicha
top-3 98%, matn bo'yicha top-10 95%, median 24 ms). Ishlayotgan va
o'lchangan qatlamni qayta yozish xavf keltiradi, foyda esa o'lchanmagan.

**Rad etilgan variantlar.**

- *SQLite FTS5 ga ko'chirish.* Rad etildi: indeks hozir TSV va u grep
  qilinadi, ya'ni hech qanday bog'liqlik talab qilmaydi. SQLite Windows
  da ham bor, lekin yangi sxema, migratsiya va yangi nosozlik turlari
  qo'shiladi.
- *`doc.sh show` chegarasini olib tashlash.* Rad etildi: 200 KB bobni
  butun o'qish ~50k token turadi, chegara aynan shuni to'xtatadi.
- *Katta bobni o'qish to'sig'ini `ask` ga o'tkazish.* Rad etildi: arzon
  yo'l (`doc.sh show`) har doim bir xil, odam qarori kerak emas.

**Xavf.** Yo'q: kod o'zgarmadi.

**Qaysi tekshiruv o'tdi.** `eval_find.py` (A, B, C va yangi D sinovi),
`eval_skill.py` 100%.

**Orqaga qaytarish.** Mavzu emas: o'zgarish yo'q.

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

## 2026-10-06: Hook xatosi jim o'tmaydi: `|| exit 0` o'rniga `|| exit 1`

**Nima o'zgardi.** `.claude/settings.json` va `install/manguberdi.ps1`
dagi yetti hook buyrug'ining oxiri ` || exit 0` dan ` || exit 1` ga
almashdi. "Hooklar faqat Java proyektida va klonda ishlaydi" yozuvidagi
qolgan qism (`active()`, `GENIUS_HOOKS=off`) o'zgarmaydi.

**Nega.** `|| exit 0` hook ishga tushmaganini butunlay yashirardi: klon
ko'chsa, Python almashsa yoki import xatosi bo'lsa guard, budget,
check_code va usage birga jim o'chardi, foydalanuvchi esa himoya bor deb
ishlardi. Claude Code 0 dagi stderr ni ko'p eventlarda faqat debug logga
yozadi. 2 dan boshqa nol bo'lmagan kod to'smaydi, lekin transkriptda
"hook error" bo'lib ko'rinadi (PL-CC11). Avvalgi yozuvdagi asos, ya'ni
Python ning "can't open file" kodi 2 to'siq bo'lmasin, 1 bilan ham
saqlanadi.

**Rad etilgan variantlar.**

- *`hookio` ichida `run_hook` o'rami va xato logi.* Rad etildi: skript
  umuman ishga tushmasa (yo'l yo'q, Python yo'q) o'ram ham yurmaydi, ya'ni
  aynan shu holatni ushlay olmaydi; uchta faylga tegadi.
- *`|| exit 0` ni qoldirib, faqat `doctor` tekshiruvi.* Rad etildi:
  tekshiruv qo'lda yurgiziladi, xato esa har sessiyada ko'rinishi kerak.

**Xavf.** Hook xulqi. O'chgan yoki ko'chgan klon endi har chaqiruvda
"hook error" xabarini beradi (to'smaydi). Hookning o'zi kutilmagan
istisno bilan yiqilsa Python 1 qaytaradi va bu ham ko'rinadi; ichida
istisnoni ushlab 0 qaytaradigan hooklar (`suggest_sections`, `handoff`)
avvalgidek jim. To'siq faqat JSON orqali beriladi: hook rejimida hamma
skript 0 qaytaradi, shuning uchun normal ishda xabar chiqmaydi.

**Qaysi tekshiruv o'tdi.** `tools/test_rewrite_paths.py` (ps1 va
settings.json hook jadvali paritet holati bilan), `tools/test_skill.py`.
Qo'lda: `CLAUDE_PROJECT_DIR=/yoq` bilan `settings.json` dagi yetti
buyruqning har biri rc=1 va bo'sh stdout.

**Orqaga qaytarish.** `git revert`, yoki ikkala fayldagi ` || exit 1` ni
` || exit 0` ga qaytarish (paritet testi ikkalasini birga talab qiladi).
Global o'rnatishda `-Update` eski buyruqni yo'l bo'yicha almashtiradi.

## 2026-10-06: guard o'qishni o'lchaydi, yagona clean va budjet tiklash so'raladi

**Nima o'zgardi.** `tools/guard.py`:

- Bash va PowerShell dagi o'qish bayt bilan o'lchanadi, Read dagi
  `slice_bytes` kabi: `head -n N`, `head -c N`, `tail -n +K`,
  `sed -n 'A,Bp'`, `awk 'NR>=A && NR<=B'`, `Get-Content -TotalCount N`.
  `grep ''`, `awk '1'`, `sed ''`, `sed -n p` butun fayl. Quvurda oxirgi
  bosqich hal qiladi: `cat BIG | wc -l`, `| head`, `| grep naqsh`,
  `| tail -n N`, `| Select-Object -First N` va `> fayl` o'tadi. Bitta
  chaqiruvdagi bo'laklar qo'shiladi (HK-H3).
- Yagona vazifa sifatidagi `clean` (`./gradlew clean`, `mvn clean`)
  `deny` emas `ask`. Test sharti undan oldin tekshiriladi, shuning uchun
  `mvn clean install`, `./gradlew clean test` va `clean build` `deny`
  qoladi. `clean` boshqa vazifa bilan birga ham `deny` (HK-H12).
- `budget.py --tiklash` asosiy oqimda `ask`, subagentda `deny`.
  `--holat` va `--yangi-vazifa` erkin (XV-O3).
- Tekshiruv tartibi: avval hamma `deny`, keyin `ask`. Ruxsat berilgan
  so'rov endi shu buyruqdagi to'liq suite yoki katta o'qishni ochmaydi.

**Nega.** O'qish to'sig'i tasodifiy edi: `sed -n '1,400p' BIG` 54 KB
o'tardi, `cat BIG | head -40` esa to'silardi va butun zanjirli buyruq
qayta yuborilardi. `./gradlew clean` foydalanuvchi aniq so'raganda ham
bajarilmasdi, lekin umumiy `ask` `mvn clean install` ni ham ochardi
(tekshiruvchi varianti). `--tiklash` chegarani bitta buyruq bilan
ochardi.

**Rad etilgan variantlar.**

- *`clean` ni umumiy `ask`.* Rad etildi: yuqoridagi sabab.
- *Satr soni bilan o'lchash.* Rad etildi: zich bobda 300 satr 40 KB.
- *`--yangi-vazifa` ni ham `ask`.* Rad etildi: SKILL.md dagi qonuniy
  oqim zanjir o'rtasida to'xtardi.

**Xavf.** Ruxsat qarori. Oddiy `grep naqsh` va `sed -n '/re/p'` filtr
deb o'tadi: natija katta bo'lishi mumkin, lekin bu avval ham shunday
edi. Noma'lum buyruq (`sort`, `tee`) oqimni kesmaydi deb olinadi, ya'ni
`cat BIG | sort` avvalgidek `deny`.

**Qaysi tekshiruv o'tdi.** `tools/test_guard.py` 272/272: 31 yangi
o'lchov va quvur holati, Read va Bash ning chegaraning ikki yonida bir
xil qarori, 8 clean, 8 budjet holati, yangi regexlar 10 KB patologik
kirishda 0.2 s dan tez.

**Orqaga qaytarish.** `git revert`.
