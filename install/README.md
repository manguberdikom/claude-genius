# manguberdi skillini o'rnatish

Ikki yo'l bor va ular turli ish uchun. Avval qaysi biri sizga kerakligini
tanlang: noto'g'ri yo'l tanlansa skill o'rnatiladi, ko'rinishidan joyida
turadi, lekin har buyruq "No such file or directory" beradi.

| Siz nima qilasiz | Yo'l |
|---|---|
| Shu repo ichida ishlayman (qo'llanmani tahrirlash, pattern qo'shish) | **A: hech narsa o'rnatilmaydi** |
| Boshqa Java proyektda ishlayman, skill kerak | **B: global o'rnatish** |

## Nimaga tayanadi

Skill yakka emas. Uning ortida to'rtta narsa turadi va ular shu klonda
qoladi:

| Nima | Nega kerak |
|---|---|
| `docs/` | 6 qo'llanma, 224 bob. Qoida matni shu yerdan o'qiladi. |
| `index/` | qidiruv indeksi. Yo'q bo'lsa `doc.sh` o'zi yasaydi. |
| `tools/` | hooklar va asboblar: qo'riqchi, budjet, kod tekshiruvi. |
| `memory/` | sessiyalar orasida saqlanadigan bilim. |

Shu sababli **klon o'chirilmaydi va ko'chirilmaydi**. Ko'chsa, o'rnatuvchi
qayta yurgiziladi.

## Talablar

| Nima | Nega | Yo'q bo'lsa |
|---|---|---|
| `python3` | Uch hook Python da yozilgan | o'rnatish to'xtaydi |
| `bash` | `tools/doc.sh` bash skripti | hooklar ishlaydi, **qidiruv ishlamaydi** |
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
va hooklar `$CLAUDE_PROJECT_DIR` orqali ishlaydi.

```bash
git clone https://github.com/manguberdikom/claude-genius
cd claude-genius
python3 tools/check_docs.py      # hujjat butunmi
python3 tools/budget.py --holat  # asboblar ishlayaptimi
```

Keyin sessiyada bir marta `/manguberdi`.

## B yo'li: global o'rnatish

Skill `~/.claude/` ga o'rnatiladi va har proyektda ishlaydi. Hook
yo'llari klonga **mutlaq** bog'lanadi.

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
| `manguberdi` skilli (SKILL.md va 6 reference) | `~/.claude/skills/manguberdi/` |
| 6 aktyor | `~/.claude/agents/` |
| Uch hook bilan `settings.json` | `~/.claude/settings.json` |

Hooklar:

| Hodisa | Asbob | Nima qiladi |
|---|---|---|
| `UserPromptSubmit` | `suggest_sections.py` | so'rovga mos bo'lim raqamlarini beradi |
| `PreToolUse` (Read, Bash) | `guard.py` | katta faylni, konteynerni, bazani, PowerShell ni to'sadi |
| `PreToolUse` (Task, Agent) | `budget.py` | aktyorning uchinchi chaqiruvini to'sadi |
| `PostToolUse` (Write, Edit) | `check_code.py` | Java qoidalarini tekshiradi |
| `Stop` | `usage.py --saqlash` | kunlik token sarfini yozib boradi |

## Yo'llar nega almashtiriladi

Skill matnida buyruqlar `python3 tools/rules_for.py` deb yozilgan. Bu
yo'l **joriy papkaga** nisbatan hal qilinadi, ya'ni klon ichida to'g'ri,
boshqa proyektda esa topilmaydi. Shuning uchun o'rnatuvchi ko'chirilgan
nusxadagi yo'llarni mutlaq qiladi:

```
python3 tools/rules_for.py   ->  python3 C:/src/claude-genius/tools/rules_for.py
tools/doc.sh find            ->  bash C:/src/claude-genius/tools/doc.sh find
memory/<proyekt-slug>/       ->  C:/src/claude-genius/memory/<proyekt-slug>/
```

Almashtirish `install/rewrite_paths.py` da va u sinaladi
(`tools/test_rewrite_paths.py`, 15 holat). PowerShell qismi sinalmaydi,
shuning uchun mantiq imkon qadar Python tomonda turadi.

Qo'lda tekshirish:

```bash
python3 install/rewrite_paths.py ~/.claude/skills/manguberdi \
  --root /yo/l/claude-genius --tekshir
```

Chiqishda `0 nisbiy yo'l qoldi` bo'lishi kerak.

## Token sarfini kuzatish

`Stop` hook har navbat oxirida sarfni `.claude/usage/<oy>.json` ga
yozadi. Fayl klon ichida turadi va git ga kirmaydi: u mashinaga
tegishli, jamoaga emas.

```bash
python3 tools/usage.py             # bugun, aktyor bo'yicha
python3 tools/usage.py --davr 7    # oxirgi 7 kun
python3 tools/usage.py --hammasi   # butun tarix
python3 tools/usage.py --jadval    # narx jadvali
```

To'rt maydon alohida sanaladi, chunki narxi boshqacha: keshdan o'qish
kirishdan o'n barobar arzon, keshga yozish chorak barobar qimmat. Bitta
"token" soniga qo'shib yuborish narxni yashiradi.

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
kontekst o'lchovi.

Keyin yangi sessiyada `/manguberdi`.

## Muammolar

| Belgi | Sabab | Yechim |
|---|---|---|
| `tools/doc.sh: No such file` | yo'llar almashmagan | `rewrite_paths.py` ni `--tekshir` bilan yurgizing |
| `bash: command not found` | bash yo'q | Git for Windows o'rnatib skriptni qayta yurgizing |
| Hooklar ishlamaydi | `settings.json` buzuq yoki klon ko'chgan | skriptni yangi `-GeniusPath` bilan qayta yurgizing |
| Skill ko'rinmaydi | sessiya eski sozlamada | yangi sessiya oching |
| Uchinchi aktyor chaqiruvi to'silgan | budjet tugagan, bu ataylab | `budget.py --yangi-vazifa "<nom>"` |

## Orqaga qaytarish

```powershell
Remove-Item -Recurse -Force $env:USERPROFILE\.claude\skills\manguberdi
Remove-Item -Recurse -Force $env:USERPROFILE\.claude\agents
Remove-Item -Force $env:USERPROFILE\.claude\settings.json
Copy-Item -Recurse -Force $env:USERPROFILE\.claude-backup-<vaqt>\* $env:USERPROFILE\.claude\
```

Zaxira papkasidagi nomlar `<ota>--<nom>` ko'rinishida, shuning uchun
qaytarishda ularni qo'lda joylashtirish kerak bo'ladi.

## Ochiq aytilgan chegara

`manguberdi.ps1` yozilgan muhitda **sinalmagan**: u yerda PowerShell yo'q,
va aynan shu sabab repo PowerShell ni ish uchun taqiqlaydi
(`tools/guard.py` uni to'sadi).

Sinalgan narsalar: qavs balansi, kirill harf yo'qligi, va u yasaydigan
`settings.json` hook shakli repodagiga aynan mos kelishi. Yo'llarni
almashtirish ham to'liq sinalgan, chunki u Python da.

Sinalmagan narsalar: fayl ko'chirish va o'chirish. Shuning uchun
birinchi yurgizish `-Apply` siz bo'ladi va hammasi zaxiraga olinadi.
