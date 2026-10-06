<#
.SYNOPSIS
  manguberdi skillini, olti aktyorni va hooklarni o'rnatadi. Sukut bo'yicha
  boshqa Claude Code sozlamalariga TEGMAYDI.

.DESCRIPTION
  Bu skript SIZNING Windows mashinangizda ishlaydi, agent sessiyasida
  ishlamaydi. Repo qoidasi PowerShell ni agentga taqiqlaydi va tools/guard.py
  uni yurgizishga urinishni to'sadi: taqiq o'z o'rnida qoladi, bu fayl esa
  o'rnatuvchi, ish asbobi emas.

  YUPQA O'RAM (R7.2). O'rnatish mantig'i BITTA joyda: install\install.py
  (Linux, macOS va Windows uchun umumiy, faqat Python standart kutubxonasi).
  Bu skript faqat Windows ga xos ishni qiladi: ishlaydigan Python 3.8+ ni
  topadi (py -3, python, python3; Microsoft Store stub'i hisoblanmaydi),
  Git Bash ni topadi (System32 va WindowsApps dagi WSL ishga tushirgichi
  hisoblanmaydi), yo'llarni to'liq yo'lga o'giradi va install.py ni
  chaqirib uning chiqish kodini qaytaradi. Hamma tekshiruv, xabar va
  settings.json yozuvi install.py da: parametrlar va chiqish kodlari avvalgidek.

  Skript yozilgan muhitda PowerShell yo'q, shuning uchun uni CI sinaydi:
  windows-latest da powershell (5.1) va pwsh (7) bilan quruq yurish va
  -Apply. -Update ham CI da yuradi, faqat -Project yurmaydi. Baribir birinchi yurgizish quruq
  o'tadi: -Apply bermaguncha sozlamaga tegilmaydi. Quruq yurish ham
  Python ni haqiqatan chaqiradi va skillni vaqtinchalik papkada yig'ib
  sinaydi, keyin uni o'chiradi: nosozlik hech narsa o'chmasidan oldin
  chiqadi. Avval ro'yxatni o'qing.

  SNAPSHOT (R7.8, XV-Y1). Hooklar klonning ishchi daraxtidan EMAS, aniq
  commit dagi snapshotdan yuradi: $HOME\.claude\genius\<sha12>\ (git
  worktree add --detach, install\snapshot.py; install.py bilan bir xil joy
  va buyruq). Aks holda git pull dan keyingi birinchi promptdayoq
  tekshirilmagan kod bajarilardi. Skill matni, hook buyruqlari, ruxsatlar
  va docs snapshotga ishora qiladi; memory va holat klonda qoladi
  (settings.json env.GENIUS_CLONE). Snapshot HEAD commitdan olinadi:
  commit qilinmagan o'zgarish unga kirmaydi. Yangi commit snapshotga
  tools\yangilash.py orqali (ro'yxat, tasdiq) yoki shu skriptni qayta
  yurgizish bilan o'tadi.

  SUKUT (qo'shuvchi). Faqat shu birliklar almashadi:
    skills\manguberdi, agents\ dagi olti aktyor fayli va settings.json
    dagi shu klonning yoki uning snapshotlarining tools\ papkasiga ishora
    qilgan hook va ruxsatlar.
  Olib tashlangan aktyor ($Retired, avvalgi .genius.json dagi, lekin
  hozirgi ro'yxatda yo'q nom) zaxira bilan o'chiriladi. O'rnatilgan
  commit, sana, klon, Python va aktyorlar
  skills\manguberdi\.genius.json ga yoziladi.
  Boshqa skill, agent, CLAUDE.md, commands\, plugins\, hooks\, rules\,
  output-styles\ va settings.json dagi begona yozuvlar JOYIDA QOLADI.
  Birlashtirishni install\merge_settings.py qiladi.

  -Reset bilan (faqat ataylab, -ConfirmReset ham kerak) global
  $HOME\.claude dan quyidagilar o'chiriladi:
    settings.json, settings.local.json, CLAUDE.md,
    skills\, agents\, commands\, plugins\, hooks\, rules\, output-styles\
  -Reset da ham nima QOLADI:
    projects\ (suhbat tarixi), todos\, history.jsonl, shell-snapshots\,
    statsig\, .credentials.json (kirish tokeni; Windows da Credential
    Manager da ham turishi mumkin) va $HOME\.claude.json (user MCP
    serverlar, proyekt trust va ruxsatlari, onboarding holati).
  Tegilmaydi: managed-settings.json, proyektdagi CLAUDE.md, CLAUDE.local.md
    va .mcp.json, boshqa proyektlarning .claude\ papkasi.

.PARAMETER GeniusPath
  claude-genius klonining yo'li. U git repo bo'lishi shart: HEAD commit dan
  snapshot olinadi ($HOME\.claude\genius\<sha12>\) va doc.sh, index, docs\
  va hooklar o'sha snapshotdan o'qiladi. Memory va holat klonda qoladi.

.PARAMETER Project
  Qo'shimcha: shu proyektdagi .claude\ papkasi ham tozalanadi. Klon yoki
  uy papkasi berilmaydi: skript buni rad etadi. .claude\ git da bo'lsa,
  o'chirish keyingi commit ga tushadi: git status bilan tekshiring.

.PARAMETER Apply
  Haqiqatan bajarish. Bersiz faqat ro'yxat chiqadi.

.PARAMETER Update
  Eski nom, endi sukut xulq. Hech narsani o'zgartirmaydi va qabul
  qilinaversin: avvalgi buyruqlar va hujjatlar buzilmaydi.

.PARAMETER Reset
  To'liq tozalash: yuqoridagi ro'yxat zaxiralanib o'chiriladi va toza
  settings.json yoziladi. -Apply bilan birga -ConfirmReset ham talab
  qiladi. -Project va -IncludeAuth faqat shu rejimda ruxsat.

.PARAMETER ConfirmReset
  -Reset -Apply uchun ikkinchi tasdiq. Interaktiv so'rov emas: CI va agent
  sessiyasi interaktiv emas.

.PARAMETER Uninstall
  manguberdi birliklarini olib tashlaydi: settings.json dan buyrug'ida shu
  ildiz bor hooklar, shu ildizga tegishli allow, ask va deny qoidalari,
  ildiz va uning ostidagi additionalDirectories yozuvlari,
  env.GENIUS_PYTHON, skills\manguberdi (.genius.json bilan),
  olti aktyor fayli, eski aktyorlar va shu klonning snapshotlari
  ($HOME\.claude\genius\ ostida, git worktree remove bilan). Begona
  yozuvlar qoladi. Klonning o'ziga bog'liq emas:
  -GeniusPath oddiy satr sifatida olinadi, shuning uchun klon allaqachon
  o'chirilgan bo'lsa ham ishlaydi.

.PARAMETER IncludeAuth
  $HOME\.claude.json ham zaxiralanib o'chiriladi: user MCP serverlar,
  proyekt trust va onboarding yo'qoladi. Login saqlanadi, chunki token
  unda emas; chiqish kerak bo'lsa Claude Code ichida /logout.

.PARAMETER BackupTo
  Zaxira papkasi. Berilmasa $HOME\.claude-backup-<vaqt> ishlatiladi.
  Bo'sh bo'lmagan papka rad etiladi: avvalgi zaxira ustidan yozilmaydi.

.EXAMPLE
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
  .\install\manguberdi.ps1 -GeniusPath C:\src\claude-genius
  Nima bo'lishini ko'rsatadi, sozlamaga tegmaydi. Birinchi qator skript
  yurgizishga faqat shu oyna uchun ruxsat beradi.

.EXAMPLE
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
  .\install\manguberdi.ps1 -GeniusPath C:\src\claude-genius -Apply

.EXAMPLE
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
  .\install\manguberdi.ps1 -GeniusPath C:\src\claude-genius -Update -Apply
  Sukut bilan bir xil: HEAD commit uchun yangi snapshot va faqat manguberdi
  birliklari. Tasdiqsiz yo'l: hook kodi o'rnatilgan commitdan farq qilsa
  o'zgarish ro'yxati chiqadi, lekin so'ralmaydi. git pull hooklarni
  o'zgartirmaydi; ro'yxat va tasdiq bilan yangilash uchun snapshotdagi
  tools\yangilash.py (o'rnatuvchi chiqishda yo'lini aytadi).

.EXAMPLE
  .\install\manguberdi.ps1 -GeniusPath C:\src\claude-genius -Reset -Apply -ConfirmReset
  Butun ~/.claude sozlamasini zaxiralab o'chiradi, keyin manguberdi ni
  o'rnatadi. -ConfirmReset siz rad etiladi.

.EXAMPLE
  .\install\manguberdi.ps1 -GeniusPath C:\eski\claude-genius -Uninstall -Apply
  manguberdi birliklarini olib tashlaydi. Klon o'chirilgan bo'lsa ham
  ishlaydi: yo'l faqat settings.json dagi yozuvlarni tanish uchun kerak.
#>

[CmdletBinding()]
param(
  [Parameter(Mandatory = $true)][string]$GeniusPath,
  [string]$Project = "",
  [switch]$Apply,
  [switch]$Update,
  [switch]$Reset,
  [switch]$ConfirmReset,
  [switch]$Uninstall,
  [switch]$IncludeAuth,
  [string]$BackupTo = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# -Update eski nom: sukut xulq allaqachon qo'shuvchi (faqat manguberdi
# birliklari almashadi), shuning uchun u hech narsani o'zgartirmaydi va
# install.py ga uzatilmaydi. Eski buyruqlar, hujjatlar va CI qadamlari
# buzilmaydi (-Reset -Update ham avvalgidek: -Reset ustun).

function Fail([string]$text) {
  Write-Host "XATO: $text" -ForegroundColor Red
  exit 1
}

# Native buyruqni chaqiradi. Windows PowerShell 5.1 da `2>&1` bilan har
# stderr qatori xato yozuviga aylanadi va 'Stop' ostida skript sababni
# aytmay to'xtaydi. Shuning uchun chaqiruv vaqtida 'Continue', chiqish
# esa matn: Out va Code. Faqat Python izlash uchun: o'rnatishning o'zi
# install.py da va uning chiqishi to'g'ridan-to'g'ri konsolga boradi.
function Invoke-Native([string]$Exe, [string[]]$ArgList) {
  $prev = $ErrorActionPreference
  $ErrorActionPreference = 'Continue'
  try {
    $lines = & $Exe @ArgList 2>&1 | ForEach-Object { "$_" }
    $code = $LASTEXITCODE
  } catch {
    $lines = @("$_")
    $code = 1
  } finally {
    $ErrorActionPreference = $prev
  }
  return [pscustomobject]@{ Out = (@($lines) -join "`n").Trim(); Code = $code }
}

# Python nomi bo'yicha emas, ishga tushirib tanlanadi. WindowsApps dagi
# python.exe va python3.exe Microsoft Store stub'i: Get-Command ularni
# topadi, lekin ular Python emas. `py -3` birinchi, chunki python.org
# o'rnatuvchisi python3.exe bermaydi. Natija sys.executable: install.py
# shu Python bilan yuradi va hook buyrug'iga aynan shu to'liq yo'lni yozadi.
function Find-Python {
  foreach ($c in @(@('py', '-3'), @('python'), @('python3'))) {
    $cmd = Get-Command $c[0] -CommandType Application -ErrorAction SilentlyContinue |
      Select-Object -First 1
    if (-not $cmd) { continue }
    $probe = @($c | Select-Object -Skip 1) +
      @('-c', 'import sys; assert sys.version_info >= (3, 8); print(sys.executable)')
    $r = Invoke-Native $cmd.Source $probe
    if ($r.Code -ne 0 -or -not $r.Out) { continue }
    $exe = ($r.Out -split "`n")[-1].Trim()
    if (Test-Path -LiteralPath $exe -PathType Leaf) { return $exe }
  }
  return $null
}

# doc.sh bash skripti va qidiruv qatlamining hammasi unga tayanadi.
# Windows da bash kafolatlanmagan: Git for Windows bilan keladi. Git ning
# odatiy papkalari PATH dan oldin qaraladi, chunki Claude Code ning Bash
# vositasi ham Git Bash. System32 dagi bash.exe WSL ishga tushirgichi
# (WindowsApps dagisi uning yorlig'i): u C:\ yo'llarini boshqa fayl
# tizimida ochadi, shuning uchun bash hisoblanmaydi. Topilmasa install.py
# o'zi xabar beradi (hech narsa o'zgarmasdan).
function Find-GitBash {
  foreach ($candidate in @(
      "$env:ProgramFiles\Git\bin\bash.exe",
      "${env:ProgramFiles(x86)}\Git\bin\bash.exe",
      "$env:LOCALAPPDATA\Programs\Git\bin\bash.exe")) {
    if (Test-Path -LiteralPath $candidate -PathType Leaf) { return $candidate }
  }
  return Get-Command 'bash' -CommandType Application -All -ErrorAction SilentlyContinue |
    Where-Object { $_.Source -notmatch '\\(System32|WindowsApps)\\bash\.exe$' } |
    Select-Object -First 1 -ExpandProperty Source
}

# Mavjud papka to'liq yo'lga (PSDrive va provider-qualified yo'l ham Python ga
# tushunarli bo'ladi). Oxirgi slash kesiladi: bo'sh joyli yo'lda `"C:\a b\"`
# native argumentda `\"` qo'shtirnoqni ekranlab, keyingi argumentlarni yutadi.
# Mavjud bo'lmagan yo'l o'zgarishsiz uzatiladi: "topilmadi" xabarini
# install.py beradi, -Uninstall esa o'chirilgan klon yo'li bilan ishlaydi.
function Resolve-Dir([string]$path) {
  if (Test-Path -LiteralPath $path -PathType Container) {
    $path = (Resolve-Path -LiteralPath $path).ProviderPath
  }
  return $path.TrimEnd('\', '/')
}

$PythonExe = Find-Python
if (-not $PythonExe) {
  Fail ("ishlaydigan Python 3.8+ topilmadi (py -3, python, python3 sinaldi; " +
        "WindowsApps dagi Microsoft Store stub'i hisoblanmaydi). Hooklar " +
        "Python bilan ishlaydi, usiz o'rnatish ma'nosiz.")
}

# Skript $PSScriptRoot dan olinadi, $GeniusPath dan EMAS: -Uninstall da
# klon allaqachon o'chirilgan bo'lishi mumkin.
$installer = Join-Path $PSScriptRoot 'install.py'
if (-not (Test-Path -LiteralPath $installer -PathType Leaf)) {
  Fail ("$installer topilmadi. Skript klonning install\ papkasidan yurishi kerak " +
        "(install.py va boshqa yordamchilar shu yerda).")
}

$GeniusPath = Resolve-Dir $GeniusPath
if (-not $GeniusPath) { Fail "-GeniusPath bo'sh: klonni tanib bo'lmaydi." }

# Bo'sh qiymat uzatilmaydi: Windows PowerShell 5.1 native chaqiruvda bo'sh
# argumentni tashlab yuboradi va keyingi bayroq qiymat bo'lib qolardi.
$pyArgs = @($installer, '--genius-path', $GeniusPath, '--ps1')
if ($Apply) { $pyArgs += '--apply' }
if ($Reset) { $pyArgs += '--reset' }
# -ConfirmReset faqat -Reset bilan ma'noli; -Reset siz avvalgidek e'tiborsiz.
if ($Reset -and $ConfirmReset) { $pyArgs += '--confirm-reset' }
if ($Uninstall) { $pyArgs += '--uninstall' }
if ($IncludeAuth) { $pyArgs += '--include-auth' }
if ($Project) { $pyArgs += @('--project', (Resolve-Dir $Project)) }
if ($BackupTo) {
  # PowerShell joriy papkasi bo'yicha: Python jarayonining papkasi bilan farq qilmasin.
  $BackupTo = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($BackupTo)
  $pyArgs += @('--backup-to', $BackupTo.TrimEnd('\', '/'))
}
if (-not $Uninstall) {
  $BashExe = Find-GitBash
  if ($BashExe) { $pyArgs += @('--bash', $BashExe) }
}

& $PythonExe @pyArgs
exit $LASTEXITCODE
