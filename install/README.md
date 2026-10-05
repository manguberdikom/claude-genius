# manguberdi skillini o'rnatish

Ikki yo'l bor va ular turli ish uchun. Avval qaysi biri sizga kerakligini
tanlang: noto'g'ri yo'l tanlansa skill o'rnatiladi, ko'rinishidan joyida
turadi, lekin har buyruq "No such file or directory" beradi.

| Siz nima qilasiz | Yo'l |
|---|---|
| Shu repo ichida ishlayman (qo'llanmani tahrirlash, pattern qo'shish) | **A: hech narsa o'rnatilmaydi** |
| Boshqa Java proyektda ishlayman, skill kerak | **B: global o'rnatish** |

Ikkalasi bitta mashinada bo'lishi mumkin. Lekin global o'rnatish bor
mashinada klon ichida ishlansa, repo hooklari ham, global hooklar ham
yuradi, ya'ni har hook ikki marta ishlaydi va bo'lim taklifi kontekstga
ikki marta tushadi. `budget.py` bir chaqiruvni `tool_use_id` bo'yicha
bir marta sanaydi, shuning uchun takror hook budjetni ikki baravar tez
tugatmaydi. `budget.py --tiklash <aktyor>` esa bitta qadamni qo'lda
qaytarish uchun qoladi.

## Nimaga tayanadi

Skill yakka emas. Uning ortida to'rtta narsa turadi va ular shu klonda
qoladi:

| Nima | Nega kerak |
|---|---|
| `docs/` | 6 qo'llanma, 224 bob. Qoida matni shu yerdan o'qiladi. |
| `index/` | qidiruv indeksi, git da yo'q. O'rnatuvchi `-Apply` da yasaydi. Yo'q yoki eskirgan bo'lsa `doc.sh`, `rules_for.py`, `check_code.py` va bo'lim taklifi hooki o'zi qayta yasaydi (`build_index.py`, bash shart emas). |
| `tools/` | hooklar va asboblar: bo'lim taklifi, kontekst o'lchovi, qo'riqchi, budjet, kod tekshiruvi, sarf hisobi. |
| `memory/` | sessiyalar orasida saqlanadigan bilim. |

Shu sababli **klon o'chirilmaydi va ko'chirilmaydi**. Ko'chsa, o'rnatuvchi
yangi `-GeniusPath` bilan qayta yurgiziladi, uning oqibati
[Yangilash](#yangilash) bo'limida.

## Talablar

| Nima | Nega | Yo'q bo'lsa |
|---|---|---|
| Python 3.8+ | hooklar va asboblar Python da yozilgan | o'rnatish to'xtaydi |
| `bash` | `tools/doc.sh` bash skripti; Windows da hooklar ham Git Bash da yuradi | o'rnatish to'xtaydi |
| `git` | klonni olish va yangilash | qo'lda yuklab olinadi |

Python nomi bo'yicha emas, ishga tushirib tanlanadi: `py -3`, `python`
va `python3` shu tartibda sinaladi, Microsoft Store stub'i hisoblanmaydi.
Topilganining to'liq yo'li hook buyrug'iga va skill matniga yoziladi,
shuning uchun B yo'lida `python3` nomi `PATH` da bo'lishi shart emas.

Windows da bash odatda [Git for Windows](https://git-scm.com/download/win)
bilan keladi. O'rnatuvchi uni o'zi izlaydi: avval Git ning odatiy
papkalaridan (`Program Files\Git`, `Program Files (x86)\Git`,
`%LOCALAPPDATA%\Programs\Git`), keyin `PATH` dan. `System32` va
`WindowsApps` dagi `bash.exe` hisoblanmaydi: u WSL ishga tushirgichi va
`C:\` yo'llarini boshqa fayl tizimida ochadi. Topilmasa o'rnatuvchi hech
narsaga tegmasdan to'xtaydi: Git Bash bo'lmasa Claude Code hookni
PowerShell bilan yurgizadi, `"python.exe" "skript.py"` shakli esa u yerda
sintaksis xatosi, ya'ni guard, budget va check_code jim ishlamay qoladi.
`doc.sh` buyruqlari (`find`, `show`, `rule`, `checklist`, `outline`) ham
bashsiz yo'q.

## A yo'li: shu repo ichida ishlash

Hech narsa o'rnatilmaydi. `.claude/settings.json` allaqachon shu repoda
va hooklar proyekt papkasini `CLAUDE_PROJECT_DIR` dan oladi.

```bash
git clone -c core.autocrlf=false https://github.com/manguberdikom/claude-genius
cd claude-genius
python3 tools/check_docs.py      # hujjat butunmi
python3 tools/budget.py --holat  # asboblar ishlayaptimi
```

`-c core.autocrlf=false` Windows uchun ikkinchi himoya, sababi
[B yo'lining 0-qadamida](#0-klonni-oling-va-skriptga-ruxsat-bering).
Majburiy emas: `.gitattributes` allaqachon LF ni talab qiladi. Linux va
macOS da u hech narsani o'zgartirmaydi.

Windows da yana ikki shart bor:

- Git for Windows o'rnatilgan bo'lsin. Claude Code hookni Git Bash bilan,
  u yo'q bo'lsa PowerShell bilan yurgizadi va hook buyrug'i u yerda
  yiqiladi, `doc.sh` esa bashsiz umuman ishlamaydi.
- `python3 --version` haqiqiy Python versiyasini ko'rsatsin. Hook
  buyrug'i `python3` ni chaqiradi. python.org o'rnatuvchisi faqat
  `python` va `py` beradi, `python3` esa Microsoft Store yorlig'i bo'lib
  qolsa hooklar jim ishlamaydi.

Keyin sessiyada bir marta `/manguberdi`.

## B yo'li: global o'rnatish

Skill `~/.claude/` ga o'rnatiladi va har proyektda ishlaydi. Hook
yo'llari klonga **mutlaq** bog'lanadi.

### 0. Klonni oling va skriptga ruxsat bering

```powershell
git clone -c core.autocrlf=false https://github.com/manguberdikom/claude-genius C:\src\claude-genius
cd C:\src\claude-genius
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
```

`core.autocrlf=false` **ixtiyoriy**: repo ildizidagi `.gitattributes`
da `* text=auto eol=lf` turadi va u `core.autocrlf` dan ustun, ya'ni
`tools/doc.sh` Windows da ham LF bilan yoziladi. Bayroq zarar qilmaydi,
shuning uchun buyruqda qoldirilgan: u `.gitattributes` ga ishonmagan
yoki eski klonni ko'chirib kelgan holat uchun ikkinchi himoya.

Nega bu muhim: `tools/doc.sh` CRLF bilan yozilsa bash uni boshidayoq
to'xtatadi (`set: pipefail: invalid option name`) va qidiruv jim
ishlamay qoladi. O'rnatuvchi CRLF li `tools/doc.sh` ni o'zi ham rad
etadi, hech narsa o'chmasidan oldin, va [Muammolar](#muammolar) dagi
yechimni aytadi.

Oxirgi buyruq skript yurgizishga faqat shu oyna uchun ruxsat beradi,
tizim sozlamasi o'zgarmaydi. Windows da standart siyosat `Restricted`
va usiz `.\install\manguberdi.ps1` "running scripts is disabled" bilan
rad etiladi. Keyingi buyruqlar shu oynada, klon ildizida yurgiziladi.

### 1. Avval quruq yurgizing

```powershell
.\install\manguberdi.ps1 -GeniusPath C:\src\claude-genius
```

`-Apply` bermaguncha **sozlamaga tegilmaydi**: skript faqat `%TEMP%` dagi
sinov yig'imiga yozadi va uni o'zi o'chiradi. Chiqishda nima o'chirilishi
va nima qolishi ro'yxat bo'lib turadi. O'qing.

### 2. Bajaring

```powershell
.\install\manguberdi.ps1 -GeniusPath C:\src\claude-genius -Apply
```

**`-Reset` siz hech narsa o'chirilmaydi.** Sukut rejim qo'shuvchi: faqat
`skills\manguberdi`, olti aktyor fayli va `settings.json` dagi shu klonga
ishora qilgan hook va ruxsatlar almashadi. Boshqa skill, agent,
`CLAUDE.md`, `commands\`, `plugins\`, `hooks\`, `rules\`,
`output-styles\` va `settings.json` dagi begona yozuvlar joyida qoladi.

### Skript qadamlari

Chiqishdagi raqamlar shu tartibda keladi:

0. **Sinov yig'imi.** Zaxira va o'chirishdan OLDIN ishlaydi. Skill va
   aktyorlar `%TEMP%` da yig'iladi, yo'llari almashtiriladi va
   `--tekshir` bilan tekshiriladi, ruxsat ro'yxati yasaladi. `-Apply`
   bo'lsa klonda indeks quriladi. Biror qadam yiqilsa skript shu yerda
   to'xtaydi va hali hech narsa o'chmagan bo'ladi.
1. **Zaxira.** O'chiriladigan birliklar zaxira papkasiga ko'chiriladi.
2. **Tozalash.** O'sha birliklar o'chiriladi, qoladiganlari ro'yxatda
   aytiladi.
3. **O'rnatish.** Sinalgan nusxa `~/.claude` ga ko'chadi.
4. **Sozlama.** `settings.json` yoziladi.
5. **Tekshirish.** Faqat `-Apply` bilan: skill joyida, `settings.json`
   o'qiladi, nisbiy yo'l qolmagan, asboblar, bo'lim taklifi va `doc.sh`
   javob beradi.

`-Update` da 0-qadam `settings.json` birlashtirishni ham quruq sinaydi,
1-3 qadamlar faqat o'z birliklariga tegadi (2-qadam "Almashtirish" deb
chiqadi), 4-qadamda esa `settings.json` bosilmaydi, birlashtiriladi.
Tafsiloti [Yangilash](#yangilash) bo'limida.

### Nima o'chiriladi

Sukut rejimda **hech narsa**. Almashadigani faqat o'z birliklari:
`skills\manguberdi`, olti aktyor fayli va `settings.json` dagi shu klonga
ishora qilgan yozuvlar.

To'liq tozalash faqat `-Reset` bilan, va `-Apply` bilan birga
`-ConfirmReset` ham talab qiladi:

```powershell
.\install\manguberdi.ps1 -GeniusPath C:\src\claude-genius -Reset -Apply -ConfirmReset
```

Shundagina `~/.claude/` dan quyidagilar o'chiriladi: `settings.json`,
`settings.local.json`, `CLAUDE.md`, `skills\`, `agents\`, `commands\`,
`plugins\`, `hooks\`, `rules\`, `output-styles\`.

`-ConfirmReset` interaktiv so'rov emas: CI va agent sessiyasi interaktiv
emas, shuning uchun tasdiq bayroq bilan beriladi. `-Reset` ni `-Apply`
siz yurgizish esa odatdagidek quruq yurish: ro'yxat chiqadi, hech narsa
o'chmaydi.

### Nima qoladi

`projects\` (suhbat tarixi), `todos\`, `history.jsonl`,
`shell-snapshots\`, `statsig\`, `.credentials.json` va `~/.claude.json`.

`~/.claude.json` da user MCP serverlar, proyekt trust va ruxsatlar hamda
onboarding holati turadi. Skript uni faqat o'qiydi: undagi MCP serverlar
har proyektda ishlayveradi, shuning uchun quruq yurish ularning nomini va
olib tashlash buyrug'ini chiqaradi. Kirish tokeni unda emas, u
`~/.claude/.credentials.json` da yoki Windows Credential Manager da
turadi va skript unga tegmaydi.

`-IncludeAuth` bilan `~/.claude.json` ham zaxiralanib o'chiriladi: MCP
serverlar, trust va onboarding yo'qoladi. Login saqlanadi, chunki token
unda emas. Chiqish kerak bo'lsa Claude Code ichida `/logout`.
`-IncludeAuth` va `-Project` faqat `-Reset` bilan beriladi: qo'shuvchi
rejimda ularning ma'nosi yo'q va skript ularni rad etadi.

Tegilmaydi: `managed-settings.json`, proyektdagi `CLAUDE.md`,
`CLAUDE.local.md` va `.mcp.json`, boshqa proyektlarning `.claude\`
papkasi. Managed sozlama topilsa skript ogohlantiradi: u eng ustun, unda
`disableAllHooks` bo'lsa hooklar ishlamaydi.

`CLAUDE_CONFIG_DIR` o'rnatilgan bo'lsa skript boshidayoq to'xtaydi:
Claude Code sozlamani o'sha papkadan o'qiydi, skript esa `~/.claude` ni
tozalaydi.

### Hammasi zaxiraga olinadi

O'chirishdan oldin `~/.claude-backup-<vaqt>` ga ko'chiriladi. Boshqa joy
kerak bo'lsa `-BackupTo <yo'l>`. Bo'sh bo'lmagan papka rad etiladi:
avvalgi zaxira ustidan yozilmaydi. Har birlik `<ota>--<nom>` shaklida
turadi (masalan `.claude--settings.json`), qaytarish
[Orqaga qaytarish](#orqaga-qaytarish) bo'limida.

### Proyektning o'z sozlamasi ham tozalanishi kerak bo'lsa

```powershell
.\install\manguberdi.ps1 -GeniusPath C:\src\claude-genius -Reset -Project C:\ish\mening-proyektim -Apply -ConfirmReset
```

Klon yoki uy papkasi berilmaydi: skript buni rad etadi. `.claude\` git
da bo'lsa o'chirish keyingi commit ga tushadi, `git status` bilan
tekshiring.

## Nima o'rnatiladi

| Nima | Qayerga |
|---|---|
| `manguberdi` skilli (SKILL.md va reference fayllari) | `~/.claude/skills/manguberdi/` |
| 6 aktyor | `~/.claude/agents/` |
| Yetti hook, ruxsatlar va `env` bilan `settings.json` | `~/.claude/settings.json` |

`settings.json` da hooklardan tashqari:

| Kalit | Qiymat | Nega |
|---|---|---|
| `permissions.additionalDirectories` | klon yo'li | Read, Grep va Glob qo'llanmani har proyektdan so'rovsiz o'qiydi |
| `permissions.allow` | skill matnidagi asbob buyruqlari | skill buyruqlari har safar ruxsat so'ramaydi |
| `env.GENIUS_PYTHON` | o'rnatuvchi sinagan Python yo'li | `doc.sh` indeksni qayta yasaganda Python ni nom bo'yicha qidirmaydi |

Hooklar (hammasi tanlangan Python ning to'liq yo'li bilan):

| Hodisa | Asbob | Nima qiladi |
|---|---|---|
| `UserPromptSubmit` | `suggest_sections.py` | so'rovga mos bo'lim raqamlarini beradi |
| `UserPromptSubmit` | `budget.py` | yangi so'rovda sessiya budjetini jim nolga tushiradi |
| `UserPromptSubmit` | `handoff.py --hook` | kontekst chegaradan oshganda yangi sessiyaga uzatishni taklif qiladi |
| `PreToolUse` (Read, Bash, PowerShell) | `guard.py` | katta faylni, konteynerni, bazani, PowerShell ni to'sadi |
| `PreToolUse` (Task, Agent) | `budget.py` | aktyorning uchinchi chaqiruvini to'sadi |
| `PostToolUse` (Write, Edit) | `check_code.py` | Java qoidalarini tekshiradi |
| `Stop` | `usage.py --saqlash` | kunlik token sarfini yozib boradi |

### Hooklar qaysi proyektda ishlaydi

Global o'rnatishda hooklar har proyektda yuradi, lekin ular faqat ikki
joyda ish qiladi:

- qo'llanma klonining o'zida;
- Java proyektida, ya'ni ildizida yoki birinchi darajali papkasida
  `pom.xml`, `build.gradle`, `build.gradle.kts`, `settings.gradle` yoki
  `settings.gradle.kts` bo'lgan repoda (ko'p modulli repoda
  `backend/pom.xml` ham sanaladi).

Boshqa joyda har hook chiqishsiz 0 bilan chiqadi: Python yoki JS
proyektida `docker` va `psql` to'silmaydi, Java bo'limlari taklif
qilinmaydi va `.java` yozuvi tekshirilmaydi. Proyekt ildizi aniqlanmasa
ham hook jim o'tadi: hook o'z noaniqligi tufayli hech qachon to'smaydi.
Qoida `tools/hookio.py` dagi `active()` da, sinovlari
`tools/test_hookio.py` da.

### Hooklarni butunlay o'chirish

`GENIUS_HOOKS=off` bo'lsa har hook, klon ichida ham, darhol 0 bilan
chiqadi. `0`, `false` va `no` ham shunday ishlaydi, registr ahamiyatsiz.

```powershell
$env:GENIUS_HOOKS = 'off'     # shu sessiya uchun
setx GENIUS_HOOKS off         # doimiy
```

Bu `settings.json` ga tegmaydi, shuning uchun qaytarish uchun
o'zgaruvchini o'chirish kifoya. Skill va aktyorlar ishlashda davom
etadi: o'chadigani faqat hooklar.

## Klon o'chsa yoki ko'chsa

`settings.json` dagi hook buyruqlari aynan shu klonga mutlaq yo'l bilan
bog'langan. Klon o'chirilsa yoki boshqa nomga ko'chirilsa:

- **hooklar jim o'tadi.** Har buyruq oxirida `|| exit 0` turadi, shuning
  uchun Python ning "can't open file" xatosi 0 ga aylanadi. Bu muhim:
  Claude Code hookdan kelgan 2 kodini TO'SIQ deb oladi, ya'ni `|| exit 0`
  bo'lmasa o'chgan klon `PreToolUse` da har `Read` va `Bash` ni to'sib,
  Claude Code ni hamma proyektda ishlatmay qo'yardi. Hooklarning o'zi
  to'siqni faqat JSON orqali beradi, shuning uchun bu hech qanday
  tekshiruvni yo'qotmaydi.
- **skill ishlamaydi.** `manguberdi` matnidagi buyruqlar va qo'llanma
  yo'llari o'sha klonga qaraydi, ularni hech narsa almashtirmaydi.

Ikki yo'l bor. Klon kerak bo'lsa, yangi joyda saqlab o'rnatuvchini yangi
`-GeniusPath` bilan qayta yurgizing: hooklar va skill yangi yo'lga
bog'lanadi.

Kerak bo'lmasa, `-Uninstall` bilan olib tashlang:

```powershell
.\install\manguberdi.ps1 -GeniusPath "C:\eski\claude-genius" -Uninstall -Apply
```

`-GeniusPath` bu yerda **mavjud bo'lishi shart emas**: u faqat
`settings.json` dagi yozuvlarni tanish uchun satr sifatida
solishtiriladi, `Resolve-Path` qilinmaydi va klon tekshiruvi o'tkazib
yuboriladi. Skriptning o'zi esa kerak, shuning uchun klonning yangi
nusxasidan (yoki `git clone` dan) yurgizing. `-Apply` siz quruq yurish.

Nimalar olinadi: `settings.json` dan buyrug'ida shu ildiz bor hooklar
(shundan bo'shab qolgan guruh va hodisa ham), shu ildizga tegishli
ruxsatlar va `additionalDirectories` yozuvi, `env.GENIUS_PYTHON`, hamda
`skills\manguberdi` va olti aktyor fayli. Begona yozuvlar qoladi:
`<ildiz>-eski` kabi boshqa klonning yozuvlari ham begona hisoblanadi.
Avval zaxira olinadi.

Skript ham yo'q bo'lsa, klon yozuvlarini qo'lda oling. Zaxira bo'lsa,
[Orqaga qaytarish](#orqaga-qaytarish) dagi buyruqlar shuni qiladi.
Zaxira ham yo'q bo'lsa `~/.claude/settings.json` ni tahrir qiling va
eski klon yo'li uchragan to'rt joyni oling:

- `hooks` ichidan buyrug'ida o'sha yo'l turgan yozuvlar (hodisa guruhi
  bo'shab qolsa, guruhning o'zi ham);
- `permissions.allow` dan o'sha yo'l bilan boshlanadigan qoidalar;
- `permissions.additionalDirectories` dan o'sha yo'l;
- `env.GENIUS_PYTHON`.

Begona yozuvlarga tegilmaydi. Faylni BOM siz UTF-8 bilan saqlang: Claude
Code va Python `json.load` BOM li faylda yiqiladi.

## Yo'llar nega almashtiriladi

Skill matnida buyruqlar `python3 tools/rules_for.py` deb yozilgan. Bu
yo'l **joriy papkaga** nisbatan hal qilinadi, ya'ni klon ichida to'g'ri,
boshqa proyektda esa topilmaydi. Shuning uchun o'rnatuvchi ko'chirilgan
nusxadagi yo'llarni mutlaq qiladi:

```text
python3 tools/rules_for.py   ->  C:/Python312/python.exe C:/src/claude-genius/tools/rules_for.py
tools/doc.sh find            ->  bash C:/src/claude-genius/tools/doc.sh find
memory/<proyekt-slug>/       ->  C:/src/claude-genius/memory/<proyekt-slug>/
```

`C:/Python312/python.exe` misol: o'rnatuvchi tanlagan Python ning to'liq
yo'li yoziladi. `bash` esa nomicha qoladi: Claude Code ning Bash vositasi
Git Bash ichida yuradi va u yerda `bash` o'sha o'rnatishning bash iga
tushadi. O'rnatuvchi topgan to'liq yo'l faqat o'zining tekshiruvi uchun.

Asboblarning o'zi klonni o'z faylidan topadi, shuning uchun ularning
ichida hech narsa almashtirilmaydi. Siz bergan nisbiy fayl yo'li va
`rules_for.py --diff` dagi git o'zgarishlari esa joriy papkadan, ya'ni
ish proyektidan olinadi.

Almashtirish `install/rewrite_paths.py` da va u birlik testida sinaladi
(`tools/test_rewrite_paths.py`, CI da yuradi). PowerShell qismi faqat CI
dagi bir martalik Windows runnerda yuradi
([Ochiq aytilgan chegara](#ochiq-aytilgan-chegara)), shuning uchun mantiq
imkon qadar Python tomonda turadi.

Qo'lda tekshirish:

```bash
python3 install/rewrite_paths.py ~/.claude/skills/manguberdi \
  --root /yo/l/claude-genius --tekshir
```

Chiqishda `0 nisbiy yo'l qoldi` bo'lishi kerak.

## Token sarfini kuzatish

`Stop` hook har navbat oxirida joriy sessiyaning sarfini, subagentlari
bilan, `.claude/usage/<oy>/<proyekt-slug>/<sessiya>.json` ga yozadi.
Hook faqat joriy sessiyani o'qiydi. Aktyor nomi subagentning
`.meta.json` faylidan olinadi, workflow agentlari `workflow:<bosqich>`
bo'lib chiqadi.
Papka klon ichida turadi va git ga kirmaydi: u mashinaga tegishli,
jamoaga emas. Global o'rnatishda ham har proyektning sarfi shu klonga,
o'z proyekt papkasiga yoziladi.

```bash
python3 tools/usage.py             # bugun, aktyor bo'yicha
python3 tools/usage.py --davr 7    # oxirgi 7 kun
python3 tools/usage.py --hammasi   # butun tarix
python3 tools/usage.py --jadval    # narx jadvali
```

Hisobot joriy papkadagi proyekt uchun chiqadi. Boshqa proyektning
sarfini ko'rish uchun o'sha proyekt papkasida
`python3 <klon>/tools/usage.py` yurgiziladi.

To'rt maydon alohida sanaladi, chunki narxi boshqacha: keshdan o'qish
modelga qarab 10-20 barobar arzon, keshga yozish 5 daqiqalik keshda
chorak barobar, 1 soatlikda 2 barobar qimmat. Bitta "token" soniga
qo'shib yuborish narxni yashiradi.

Narx jadvali `tools/usage.py` ichidagi `PRICES` da ochiq turadi. Narx
o'zgarsa shu jadval tahrirlanadi. Noma'lum model nolga aylanmaydi:
tokenlari sanaladi va "narxsiz model bor" deb belgilanadi.

## O'rnatilganini tekshirish

O'rnatuvchi o'zi tekshiradi, lekin qo'lda ham ko'rish mumkin:

```bash
python3 /yo/l/claude-genius/tools/budget.py --holat
bash /yo/l/claude-genius/tools/doc.sh find "circuit breaker"
cd /yo/l/mening-proyektim && python3 /yo/l/claude-genius/tools/handoff.py
```

Uchtasi ham javob bersa, uch qatlam ishlayapti: hisoblagich, qidiruv va
kontekst o'lchovi. `handoff.py` proyekt papkasidan, unda kamida bitta
sessiya o'tgandan keyin yurgiziladi. Transkript klondan emas, sessiya ID
(`CLAUDE_CODE_SESSION_ID`) yoki proyekt papkasidan topiladi, bo'lmasa
shuni aytib chiqadi.

Keyin yangi sessiyada `/manguberdi`.

## Yangilash

`git pull` klondagi asboblarni yangilaydi va hooklar ularni darhol
oladi, chunki hook yo'li klonga bog'langan. `~/.claude` dagi skill va
aktyorlar esa o'rnatish paytidagi nusxa: ular pull bilan yangilanmaydi,
yangi hook ham `settings.json` ga o'zi qo'shilmaydi.

Ularni o'rnatuvchini qayta yurgizish yangilaydi: avval quruq, keyin
`-Apply` bilan. Sukut rejim allaqachon qo'shuvchi, shuning uchun
qo'shimcha bayroq kerak emas. Buyruqlar 0-qadamdagidek, klon ildizida va
ruxsat berilgan oynada yurgiziladi:

```powershell
git -C C:\src\claude-genius pull
.\install\manguberdi.ps1 -GeniusPath C:\src\claude-genius
.\install\manguberdi.ps1 -GeniusPath C:\src\claude-genius -Apply
```

`-Update` ham ishlayveradi va aynan shu ishni qiladi: u eski nom, sukut
xulqqa aylangan.

Faqat uch narsa zaxiralanib almashadi: `skills\manguberdi`, 6 aktyor
fayli va `settings.json` dagi o'z yozuvlari, ya'ni buyrug'i shu klonning
`tools\` papkasiga ishora qilgan hook va ruxsatlar
(`env.GENIUS_PYTHON` ham yangilanadi). Qolgani joyida turadi: boshqa
skill va agentlar, `CLAUDE.md`, `plugins\`, `settings.json` dagi begona
hook va ruxsatlar, `env` dagi boshqa o'zgaruvchilar va qolgan kalitlar.
Birlashtirishni `install/merge_settings.py` qiladi: quruq yurish nechta
hook va ruxsat almashishini bir qatorda aytadi, buzuq `settings.json` da
esa hech narsa o'chmasidan oldin to'xtaydi. Zaxirani qaytarish
[Orqaga qaytarish](#orqaga-qaytarish) bo'limida.

Klon KO'CHGAN bo'lsa qayta o'rnatish yetmaydi: eski yo'lga ishora qilgan
hooklar o'zniki deb tanilmaydi va yangilari yonida qoladi. Ikki buyruq
kerak: avval eski yo'l uchun `-Uninstall`, keyin yangi yo'l uchun
odatdagi o'rnatish.

```powershell
.\install\manguberdi.ps1 -GeniusPath C:\eski\claude-genius -Uninstall -Apply
.\install\manguberdi.ps1 -GeniusPath C:\yangi\claude-genius -Apply
```

Avval buning uchun `-Update` siz yurgizish tavsiya qilinardi, lekin u
butun sozlamani tozalardi: endi unday emas va kerak ham emas.

## Muammolar

| Belgi | Sabab | Yechim |
|---|---|---|
| `running scripts is disabled on this system` | ExecutionPolicy `Restricted` | 0-qadamdagi `Set-ExecutionPolicy -Scope Process` buyrug'i |
| `set: pipefail: invalid option name` | klon CRLF bilan olingan | `<klon>\tools\doc.sh` ni o'chirib `git -C <klon> -c core.autocrlf=false checkout -- tools/doc.sh`; doimiy yechim: klonni 0-qadamdagidek qayta olish |
| `tools/doc.sh: No such file` | yo'llar almashmagan | `rewrite_paths.py --tekshir` bilan skill matnini tekshiring; nisbiy yo'l qolgan bo'lsa o'rnatuvchini qayta yurgizing |
| `bash: command not found` | bash yo'q | Git for Windows o'rnatib skriptni qayta yurgizing |
| Hooklar ishlamaydi | `settings.json` buzuq yoki klon ko'chgan | eski yo'l uchun `-Uninstall`, keyin yangi `-GeniusPath` bilan o'rnating |
| Hooklar jim, xato ham yo'q | proyekt Java emas yoki `GENIUS_HOOKS=off` | [Hooklar qaysi proyektda ishlaydi](#hooklar-qaysi-proyektda-ishlaydi) |
| `-Reset -Apply` rad etildi | `-ConfirmReset` berilmagan, bu ataylab | rozi bo'lsangiz `-ConfirmReset` qo'shing |
| Eski o'rnatuvchi sozlamani o'chirgan | `-Update` siz `-Apply` avval to'liq tozalardi | [Eski o'rnatuvchidan keyin tiklash](#eski-ornatuvchidan-keyin-tiklash) |
| Skill ko'rinmaydi | sessiya eski sozlamada | yangi sessiya oching |
| Uchinchi aktyor chaqiruvi to'silgan | budjet tugagan, bu ataylab | aniq savol bering: javobdan keyin budjet o'zi yangilanadi |

## Orqaga qaytarish

Zaxirada har birlik `<ota>--<nom>` nomi bilan turadi:
`~/.claude/settings.json` `.claude--settings.json` bo'ladi, `skills\`
esa `.claude--skills`. Shuning uchun butun zaxirani `~/.claude` ga
ko'chirish hech narsani tiklamaydi. Quyidagi buyruqlar manguberdi
o'rnatgan narsani olib tashlaydi va har birlikni o'z nomi bilan joyiga
qaytaradi:

```powershell
$b = "$env:USERPROFILE\.claude-backup-<vaqt>"
$c = "$env:USERPROFILE\.claude"
$aktyorlar = 'qidiruv', 'tahlil', 'review', 'dasturchi', 'test-muhandis', 'rejalashtiruvchi'
$ornatilgan = @("$c\skills\manguberdi", "$c\settings.json") + ($aktyorlar | ForEach-Object { "$c\agents\$_.md" })
foreach ($x in $ornatilgan) {
  if (Test-Path -LiteralPath $x) { Remove-Item -LiteralPath $x -Recurse -Force }
}
Get-ChildItem -LiteralPath $b -Force -Filter '.claude--*' | ForEach-Object {
  $dst = Join-Path $c $_.Name.Substring(9)
  if (Test-Path -LiteralPath $dst) { Remove-Item -LiteralPath $dst -Recurse -Force }
  Copy-Item -LiteralPath $_.FullName -Destination $dst -Recurse -Force
}
```

`<foydalanuvchi>--.claude.json` (faqat `-IncludeAuth` bilan olingan
bo'lsa) `$env:USERPROFILE\.claude.json` ga, `<proyekt>--.claude` esa
`<proyekt>\.claude` ga xuddi shunday, nomidagi qo'shimchasiz
ko'chiriladi.

Skript `-Update` siz, `-Apply` bilan bir necha marta yurgizilgan
bo'lsa, **eng eski** zaxirani tanlang: keyingilarida faqat manguberdi
o'rnatgan sozlama turadi.

`-Update` zaxirasida faqat almashtirilgan birliklar turadi va ota papka
boshqa: `skills--manguberdi` `~/.claude/skills/manguberdi` ga,
`agents--<aktyor>.md` `~/.claude/agents/` ga, `.claude--settings.json`
esa `~/.claude/settings.json` ga qaytadi:

```powershell
$b = "$env:USERPROFILE\.claude-backup-<vaqt>"
$c = "$env:USERPROFILE\.claude"
if (Test-Path -LiteralPath "$b\skills--manguberdi") {
  if (Test-Path -LiteralPath "$c\skills\manguberdi") { Remove-Item -LiteralPath "$c\skills\manguberdi" -Recurse -Force }
  Copy-Item -LiteralPath "$b\skills--manguberdi" -Destination "$c\skills\manguberdi" -Recurse
}
Get-ChildItem -LiteralPath $b -Force -Filter 'agents--*.md' | ForEach-Object {
  Copy-Item -LiteralPath $_.FullName -Destination (Join-Path "$c\agents" $_.Name.Substring(8)) -Force
}
if (Test-Path -LiteralPath "$b\.claude--settings.json") {
  Copy-Item -LiteralPath "$b\.claude--settings.json" -Destination "$c\settings.json" -Force
}
```

## Eski o'rnatuvchidan keyin tiklash

O'rnatuvchining avvalgi versiyasi `-Update` siz `-Apply` berilganda
`~/.claude` dagi `settings.json`, `settings.local.json`, `CLAUDE.md`,
`skills\`, `agents\`, `commands\`, `plugins\`, `hooks\`, `rules\` va
`output-styles\` ni o'chirardi. Endi unday emas: tozalash faqat `-Reset`
bilan. Lekin eski versiyani yurgizgan bo'lsangiz, o'chirilgan narsa
zaxirada turadi.

Zaxira qayerda: `~/.claude-backup-<vaqt>` (yoki siz bergan `-BackupTo`
yo'li). O'rnatuvchi chiqishining 1-qadamida ham, oxirgi qatorida ham
aniq yo'l yozilgan. Bir nechta bo'lsa, sanasi eng eskisi birinchi
o'rnatishdan qolgani.

Qaytarish:

```powershell
python3 install\restore_backup.py $env:USERPROFILE\.claude-backup-20260101-120000
python3 install\restore_backup.py $env:USERPROFILE\.claude-backup-20260101-120000 --yoz
```

Birinchi buyruq quruq yurish: nima qaytishini va nima o'tkazib
yuborilishini ro'yxat qilib chiqaradi, hech narsa yozmaydi. `--yoz`
bilan qaytaradi.

Qoida: **faqat hozir yo'q bo'lgan narsa qaytariladi.** Hozir turgan fayl
sizning joriy holatingiz va ustidan yozilmaydi.

| Birlik | Nima bo'ladi |
|---|---|
| `CLAUDE.md`, `settings.local.json`, `commands\`, `plugins\`, `hooks\`, `rules\`, `output-styles\` | butunligicha, faqat hozir yo'q bo'lsa |
| `skills\`, `agents\` | ichidagi faqat yo'q bolalar |
| `skills\manguberdi` va olti aktyor fayli | ataylab tashlanadi: ularni o'rnatuvchi boshqaradi, zaxiradagisi eski versiya |
| `settings.json` | birlashtiriladi: zaxiradagi sizning yozuvlaringiz qaytadi, hozirgi fayldagilar ustun turadi |

`settings.json` da hozirgisi ustun turishi muhim: shunday qilinmasa
yangi o'rnatishning hooklari va ruxsatlari eski nusxasi bilan
almashinardi. `permissions` ro'yxatlarida ikkisi qo'shiladi, takrorsiz.

Zaxirani qo'lda ham qaytarish mumkin, lekin birliklar `<ota>--<nom>`
nomi bilan yotadi, shuning uchun butun papkani ko'chirish ishlamaydi:
[Orqaga qaytarish](#orqaga-qaytarish) dagi sikl har birlikni o'z nomi
bilan joyiga qo'yadi.

## Ochiq aytilgan chegara

Agent sessiyasi `manguberdi.ps1` ni yurgiza olmaydi: repo PowerShell ni
ish uchun taqiqlaydi (`tools/guard.py` uni to'sadi). Uni sinaydigan joy
CI: `.github/workflows/docs.yml` dagi `installer` job `windows-latest`
da Windows PowerShell 5.1 va pwsh 7 bilan to'rt qadam yurgizadi.

1. Quruq yurish.
2. `-Apply` (sukut, qo'shuvchi): begona `CLAUDE.md`, `skills\eski`,
   `plugins\p`, `rules\r` va `settings.json` dagi begona hook, ruxsat
   va kalit ekiladi; hammasi saqlangani, manguberdi va olti aktyor
   borligi, o'z hooki bir marta turgani va `settings.json` BOM siz
   yozilgani tekshiriladi.
3. `-Update -Apply`: eski nom bilan ham xuddi shu xulq.
4. `-Reset`: `-ConfirmReset` siz rad etilishi va hech narsa o'chmasligi,
   `-IncludeAuth` ni `-Reset` siz berish rad etilishi, tasdiq bilan esa
   o'chishi va zaxira yozilishi.
5. `-Uninstall`: klon nusxasidan o'rnatiladi, nusxa o'chiriladi, keyin
   mavjud bo'lmagan shu yo'l bilan `-Uninstall -Apply` yuradi; o'z
   yozuvlari ketgani va begonalari qolgani tekshiriladi.

`-Project` CI da yurmaydi. Yo'llarni almashtirish, `settings.json` ni
birlashtirish, olib tashlash va zaxiradan tiklash alohida birlik
testlarida: `tools/test_rewrite_paths.py`,
`tools/test_merge_settings.py`, `tools/test_uninstall_settings.py`,
`tools/test_restore_backup.py`.

ps1 yasaydigan hook jadvalining repodagi `.claude/settings.json` ga
mosligi `tools/test_rewrite_paths.py` dagi `case_ps1_hooklari_repoga_mos`
da sinaladi: hodisa, matcher, skript, argument, timeout va
statusMessage. Haqiqiy foydalanuvchi mashinasidagi holatlar (boshqa
`python3` stub'i, WSL bash) esa hali ham sinalmaydi. Shuning uchun
birinchi yurgizish `-Apply` siz bo'ladi va hammasi zaxiraga olinadi.
