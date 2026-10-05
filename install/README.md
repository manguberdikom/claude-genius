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
yuradi, ya'ni har hook ikki marta ishlaydi. Aktyor bir marta chaqirilgan
bo'lsa-yu, ikkinchi chaqiruvi budjet tugadi deb to'silsa, sabab shu:
`python3 tools/budget.py --tiklash <aktyor>` bitta qadamni qaytaradi.

## Nimaga tayanadi

Skill yakka emas. Uning ortida to'rtta narsa turadi va ular shu klonda
qoladi:

| Nima | Nega kerak |
|---|---|
| `docs/` | 6 qo'llanma, 224 bob. Qoida matni shu yerdan o'qiladi. |
| `index/` | qidiruv indeksi. Yo'q bo'lsa `doc.sh` o'zi yasaydi. |
| `tools/` | hooklar va asboblar: bo'lim taklifi, kontekst o'lchovi, qo'riqchi, budjet, kod tekshiruvi, sarf hisobi. |
| `memory/` | sessiyalar orasida saqlanadigan bilim. |

Shu sababli **klon o'chirilmaydi va ko'chirilmaydi**. Ko'chsa, o'rnatuvchi
yangi `-GeniusPath` bilan qayta yurgiziladi, uning oqibati
[Yangilash](#yangilash) bo'limida.

## Talablar

| Nima | Nega | Yo'q bo'lsa |
|---|---|---|
| `python3` | Hooklar Python da yozilgan | o'rnatish to'xtaydi |
| `bash` | `tools/doc.sh` bash skripti | B yo'lida hooklar ishlaydi, **qidiruv ishlamaydi** |
| `git` | klonni olish va yangilash | qo'lda yuklab olinadi |

Windows da bash odatda [Git for Windows](https://git-scm.com/download/win)
bilan keladi. O'rnatuvchi uni o'zi izlaydi: `PATH` dan, keyin Git ning
odatiy papkalaridan. Topilmasa aytadi va davom etadi, chunki hooklar
baribir ishlaydi.

Bashsiz nima yo'qoladi: `find`, `show`, `rule`, `checklist`, `outline`.
Ya'ni skill qoidani ko'rsata olmaydi, faqat mexanik tekshiruvlar qoladi.
Bu skillning yarmi, shuning uchun bashni o'rnatish tavsiya qilinadi.

## A yo'li: shu repo ichida ishlash

Hech narsa o'rnatilmaydi. `.claude/settings.json` allaqachon shu repoda
va hooklar proyekt papkasini `CLAUDE_PROJECT_DIR` dan oladi.

```bash
git clone -c core.autocrlf=false https://github.com/manguberdikom/claude-genius
cd claude-genius
python3 tools/check_docs.py      # hujjat butunmi
python3 tools/budget.py --holat  # asboblar ishlayaptimi
```

`-c core.autocrlf=false` Windows uchun, sababi
[B yo'lining 0-qadamida](#0-klonni-oling-va-skriptga-ruxsat-bering).
Linux va macOS da u hech narsani o'zgartirmaydi.

Windows da yana ikki shart bor:

- Git for Windows o'rnatilgan bo'lsin. Claude Code hookni Git Bash bilan,
  u yo'q bo'lsa PowerShell bilan yurgizadi, `doc.sh` esa bashsiz umuman
  ishlamaydi.
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

`core.autocrlf=false` shart. Git for Windows odatda uni `true` qiladi va
`tools/doc.sh` CRLF bilan yoziladi. Bash bunday faylni boshidayoq
to'xtatadi (`set: pipefail: invalid option name`), qidiruv esa jim
ishlamay qoladi.

Oxirgi buyruq skript yurgizishga faqat shu oyna uchun ruxsat beradi,
tizim sozlamasi o'zgarmaydi. Windows da standart siyosat `Restricted`
va usiz `.\install\manguberdi.ps1` "running scripts is disabled" bilan
rad etiladi. Keyingi buyruqlar shu oynada, klon ildizida yurgiziladi.

### 1. Avval quruq yurgizing

```powershell
.\install\manguberdi.ps1 -GeniusPath C:\src\claude-genius
```

`-Apply` bermaguncha **hech narsa o'chirilmaydi va yozilmaydi**. Chiqishda
nima o'chirilishi va nima qolishi ro'yxat bo'lib turadi. O'qing.

### 2. Bajaring

```powershell
.\install\manguberdi.ps1 -GeniusPath C:\src\claude-genius -Apply
```

### Nima o'chiriladi

`~/.claude/` dan: `settings.json`, `settings.local.json`, `CLAUDE.md`,
`skills\`, `agents\`, `commands\`, `plugins\`, `hooks\`, `rules\`,
`output-styles\`.

### Nima qoladi

`projects\` (suhbat tarixi), `todos\`, `history.jsonl`,
`shell-snapshots\`, `statsig\` va `~/.claude.json` (kirish ma'lumoti).

Kirishni ham o'chirish kerak bo'lsa `-IncludeAuth`, lekin shundan keyin
qaytadan login qilinadi.

### Hammasi zaxiraga olinadi

O'chirishdan oldin `~/.claude-backup-<vaqt>` ga ko'chiriladi. Boshqa joy
kerak bo'lsa `-BackupTo <yo'l>`.

### Proyektning o'z sozlamasi ham tozalanishi kerak bo'lsa

```powershell
.\install\manguberdi.ps1 -GeniusPath C:\src\claude-genius -Project C:\ish\mening-proyektim -Apply
```

## Nima o'rnatiladi

| Nima | Qayerga |
|---|---|
| `manguberdi` skilli (SKILL.md va reference fayllari) | `~/.claude/skills/manguberdi/` |
| 6 aktyor | `~/.claude/agents/` |
| Olti hook bilan `settings.json` | `~/.claude/settings.json` |

Hooklar:

| Hodisa | Asbob | Nima qiladi |
|---|---|---|
| `UserPromptSubmit` | `suggest_sections.py` | so'rovga mos bo'lim raqamlarini beradi |
| `UserPromptSubmit` | `handoff.py --hook` | kontekst chegaradan oshganda yangi sessiyaga uzatishni taklif qiladi |
| `PreToolUse` (Read, Bash) | `guard.py` | katta faylni, konteynerni, bazani, PowerShell ni to'sadi |
| `PreToolUse` (Task, Agent) | `budget.py` | aktyorning uchinchi chaqiruvini to'sadi |
| `PostToolUse` (Write, Edit) | `check_code.py` | Java qoidalarini tekshiradi |
| `Stop` | `usage.py --saqlash` | kunlik token sarfini yozib boradi |

## Yo'llar nega almashtiriladi

Skill matnida buyruqlar `python3 tools/rules_for.py` deb yozilgan. Bu
yo'l **joriy papkaga** nisbatan hal qilinadi, ya'ni klon ichida to'g'ri,
boshqa proyektda esa topilmaydi. Shuning uchun o'rnatuvchi ko'chirilgan
nusxadagi yo'llarni mutlaq qiladi:

```text
python3 tools/rules_for.py   ->  python3 C:/src/claude-genius/tools/rules_for.py
tools/doc.sh find            ->  bash C:/src/claude-genius/tools/doc.sh find
memory/<proyekt-slug>/       ->  C:/src/claude-genius/memory/<proyekt-slug>/
```

Asboblarning o'zi klonni o'z faylidan topadi, shuning uchun ularning
ichida hech narsa almashtirilmaydi. Siz bergan nisbiy fayl yo'li va
`rules_for.py --diff` dagi git o'zgarishlari esa joriy papkadan, ya'ni
ish proyektidan olinadi.

Almashtirish `install/rewrite_paths.py` da va u sinaladi
(`tools/test_rewrite_paths.py`, CI da yuradi). PowerShell qismi
sinalmaydi, shuning uchun mantiq imkon qadar Python tomonda turadi.

Qo'lda tekshirish:

```bash
python3 install/rewrite_paths.py ~/.claude/skills/manguberdi \
  --root /yo/l/claude-genius --tekshir
```

Chiqishda `0 nisbiy yo'l qoldi` bo'lishi kerak.

## Token sarfini kuzatish

`Stop` hook har navbat oxirida joriy sessiyaning sarfini, subagentlari
bilan, `.claude/usage/<oy>/<proyekt-slug>/<sessiya>.json` ga yozadi.
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
python3 /yo/l/claude-genius/tools/handoff.py
```

Uchtasi ham javob bersa, uch qatlam ishlayapti: hisoblagich, qidiruv va
kontekst o'lchovi. `handoff.py` proyekt papkasida, unda kamida bitta
sessiya o'tgandan keyin yurgiziladi: u o'sha proyektning transkriptini
o'lchaydi, transkript bo'lmasa shuni aytib chiqadi.

Keyin yangi sessiyada `/manguberdi`.

## Yangilash

`git pull` klondagi asboblarni yangilaydi va hooklar ularni darhol
oladi, chunki hook yo'li klonga bog'langan. `~/.claude` dagi skill va
aktyorlar esa o'rnatish paytidagi nusxa: ular pull bilan yangilanmaydi,
yangi hook ham `settings.json` ga o'zi qo'shilmaydi.

Hozir ularni yangilashning yagona yo'li o'rnatuvchini qayta yurgizish.
U birinchi o'rnatishdagidek ishlaydi: `~/.claude` dagi sozlamani yangi
zaxiraga olib tozalaydi. O'rnatishdan keyin qo'shilgan skill, agent yoki
`CLAUDE.md` ham zaxiraga ketadi, shuning uchun avval quruq yurgizib
ro'yxatni o'qing. Buyruqlar 0-qadamdagidek, klon ildizida va ruxsat
berilgan oynada yurgiziladi:

```powershell
git -C C:\src\claude-genius pull
.\install\manguberdi.ps1 -GeniusPath C:\src\claude-genius
.\install\manguberdi.ps1 -GeniusPath C:\src\claude-genius -Apply
```

Kerakli birlik keyin zaxiradan qaytariladi:
[Orqaga qaytarish](#orqaga-qaytarish) dagi sikl, faqat o'sha nom uchun.

## Muammolar

| Belgi | Sabab | Yechim |
|---|---|---|
| `running scripts is disabled on this system` | ExecutionPolicy `Restricted` | 0-qadamdagi `Set-ExecutionPolicy -Scope Process` buyrug'i |
| `set: pipefail: invalid option name` | klon CRLF bilan olingan | `<klon>\tools\doc.sh` ni o'chirib `git -C <klon> -c core.autocrlf=false checkout -- tools/doc.sh`; doimiy yechim: klonni 0-qadamdagidek qayta olish |
| `tools/doc.sh: No such file` | yo'llar almashmagan | `rewrite_paths.py` ni `--tekshir` bilan yurgizing |
| `bash: command not found` | bash yo'q | Git for Windows o'rnatib skriptni qayta yurgizing |
| Hooklar ishlamaydi | `settings.json` buzuq yoki klon ko'chgan | skriptni yangi `-GeniusPath` bilan qayta yurgizing |
| Skill ko'rinmaydi | sessiya eski sozlamada | yangi sessiya oching |
| Uchinchi aktyor chaqiruvi to'silgan | budjet tugagan, bu ataylab | `budget.py --yangi-vazifa "<nom>"` |

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
$aktyorlar = 'qidiruv', 'tahlil', 'review', 'arxitektor', 'test-muhandis', 'rejalashtiruvchi'
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

Skript `-Apply` bilan bir necha marta yurgizilgan bo'lsa (masalan
yangilashda), **eng eski** zaxirani tanlang: keyingilarida faqat
manguberdi o'rnatgan sozlama turadi.

## Ochiq aytilgan chegara

`manguberdi.ps1` yozilgan muhitda **sinalmagan**: u yerda PowerShell yo'q,
va aynan shu sabab repo PowerShell ni ish uchun taqiqlaydi
(`tools/guard.py` uni to'sadi). Shu qo'llanmadagi PowerShell buyruqlari
ham xuddi shunday sinalmagan.

Avtomatik sinalgani faqat yo'llarni almashtirish
(`tools/test_rewrite_paths.py`, CI da yuradi), chunki u Python da. Qavs
balansi, kirill harf yo'qligi va ps1 yasaydigan hook jadvali repodagi
`.claude/settings.json` ga mosligi bir marta qo'lda solishtirilgan,
sinov emas: biri o'zgarsa, ikkinchisi qo'lda moslanadi.

Sinalmagan narsalar: fayl ko'chirish va o'chirish. Shuning uchun
birinchi yurgizish `-Apply` siz bo'ladi va hammasi zaxiraga olinadi.
