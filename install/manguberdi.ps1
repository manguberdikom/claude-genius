<#
.SYNOPSIS
  Claude Code sozlamalarini tozalaydi va faqat manguberdi skillini o'rnatadi.

.DESCRIPTION
  Bu skript SIZNING Windows mashinangizda ishlaydi, agent sessiyasida
  ishlamaydi. Repo qoidasi PowerShell ni agentga taqiqlaydi va tools/guard.py
  uni yurgizishga urinishni to'sadi: taqiq o'z o'rnida qoladi, bu fayl esa
  o'rnatuvchi, ish asbobi emas.

  Ochiq aytilsin: bu skript yozilgan muhitda SINALMAGAN, chunki u yerda
  PowerShell yo'q. Aynan shu sabab repo uni ish uchun taqiqlaydi. Shuning
  uchun birinchi yurgizish quruq o'tadi: -Apply bermaguncha hech narsa
  o'chirilmaydi va hech narsa yozilmaydi. Avval ro'yxatni o'qing.

  Nima o'chiriladi (global, $HOME\.claude):
    settings.json, settings.local.json, CLAUDE.md,
    skills\, agents\, commands\, plugins\, hooks\, rules\, output-styles\
  Nima QOLADI:
    projects\ (suhbat tarixi), todos\, history.jsonl, shell-snapshots\,
    statsig\ va $HOME\.claude.json (kirish ma'lumoti).
    Kirishni ham o'chirish uchun -IncludeAuth, lekin shundan keyin
    qaytadan login qilish kerak.

.PARAMETER GeniusPath
  claude-genius klonining yo'li. Skill qo'llanmasiz ishlamaydi: doc.sh,
  index va docs\ aynan shu yerdan olinadi.

.PARAMETER Project
  Qo'shimcha: shu proyektdagi .claude\ papkasi ham tozalanadi.

.PARAMETER Apply
  Haqiqatan bajarish. Bersiz faqat ro'yxat chiqadi.

.PARAMETER IncludeAuth
  $HOME\.claude.json ham o'chiriladi. Login qaytadan talab qilinadi.

.PARAMETER BackupTo
  Zaxira papkasi. Berilmasa $HOME\.claude-backup-<vaqt> ishlatiladi.

.EXAMPLE
  .\install\manguberdi.ps1 -GeniusPath C:\src\claude-genius
  Nima bo'lishini ko'rsatadi, hech narsaga tegmaydi.

.EXAMPLE
  .\install\manguberdi.ps1 -GeniusPath C:\src\claude-genius -Apply
#>

[CmdletBinding()]
param(
  [Parameter(Mandatory = $true)][string]$GeniusPath,
  [string]$Project = "",
  [switch]$Apply,
  [switch]$IncludeAuth,
  [string]$BackupTo = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$UserHome = [Environment]::GetFolderPath('UserProfile')
$ClaudeDir = Join-Path $UserHome '.claude'
$AuthFile = Join-Path $UserHome '.claude.json'

# O'chiriladigan sozlama birliklari. Tarix, todo va kirish bu yerda yo'q:
# ular sozlama emas va ularni o'chirish ishni yo'qotadi.
$ConfigItems = @(
  'settings.json', 'settings.local.json', 'CLAUDE.md',
  'skills', 'agents', 'commands', 'plugins', 'hooks', 'rules', 'output-styles'
)

# O'rnatiladigan aktyorlar. Skill shu nomlar bilan chaqiradi.
$Actors = @('qidiruv', 'tahlil', 'review', 'arxitektor', 'test-muhandis',
            'rejalashtiruvchi')

function Say([string]$text) { Write-Host $text }
function Step([string]$text) { Write-Host "  $text" }

function Fail([string]$text) {
  Write-Host "XATO: $text" -ForegroundColor Red
  exit 1
}

# --- 1. Manbani tekshirish -------------------------------------------------

if (-not (Test-Path -LiteralPath $GeniusPath -PathType Container)) {
  Fail "GeniusPath topilmadi: $GeniusPath"
}
$GeniusPath = (Resolve-Path -LiteralPath $GeniusPath).Path

$Required = @(
  'tools\doc.sh', 'tools\guard.py', 'tools\check_code.py',
  'tools\rules_for.py', 'tools\budget.py', 'tools\suggest_sections.py',
  'docs\manifest.json', '.claude\skills\manguberdi\SKILL.md'
)
foreach ($rel in $Required) {
  if (-not (Test-Path -LiteralPath (Join-Path $GeniusPath $rel))) {
    Fail "klon to'liq emas, yo'q: $rel"
  }
}

$Python = Get-Command 'python3' -ErrorAction SilentlyContinue
if (-not $Python) { $Python = Get-Command 'python' -ErrorAction SilentlyContinue }
if (-not $Python) {
  Fail "python3 topilmadi. Hooklar Python bilan ishlaydi, usiz o'rnatish ma'nosiz."
}
$PythonExe = $Python.Source

# doc.sh bash skripti va qidiruv qatlamining hammasi unga tayanadi.
# Windows da bash kafolatlanmagan: Git for Windows yoki WSL bilan keladi.
$BashCmd = Get-Command 'bash' -ErrorAction SilentlyContinue
$BashExe = if ($BashCmd) { $BashCmd.Source } else { $null }
if (-not $BashExe) {
  foreach ($candidate in @(
      "$env:ProgramFiles\Git\bin\bash.exe",
      "${env:ProgramFiles(x86)}\Git\bin\bash.exe",
      "$env:LOCALAPPDATA\Programs\Git\bin\bash.exe")) {
    if ($candidate -and (Test-Path -LiteralPath $candidate)) {
      $BashExe = $candidate
      break
    }
  }
}

Say ""
Say "Manba : $GeniusPath"
Say "Python: $PythonExe"
Say ("Bash  : " + $(if ($BashExe) { $BashExe } else { "TOPILMADI" }))
Say "Global: $ClaudeDir"
if ($Project) { Say "Proyekt: $Project" }
Say ("Rejim : " + $(if ($Apply) { 'BAJARILADI' } else { 'quruq yurish (-Apply bermadingiz)' }))

if (-not $BashExe) {
  Say ""
  Say "OGOHLANTIRISH: bash topilmadi." -ForegroundColor Yellow
  Say "  tools\doc.sh bash skripti, qidiruv qatlamining hammasi unga tayanadi:"
  Say "  find, show, rule, checklist, outline. Usiz skill qoida matnini"
  Say "  o'qiy olmaydi, faqat hooklar ishlaydi."
  Say "  Yechim: Git for Windows o'rnating (https://git-scm.com/download/win)"
  Say "  yoki WSL dan bash bering, keyin shu skriptni qayta yurgizing."
  Say ""
}

# --- 2. Zaxira ------------------------------------------------------------

if (-not $BackupTo) {
  $stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
  $BackupTo = Join-Path $UserHome ".claude-backup-$stamp"
}

Say ""
Say "1. Zaxira -> $BackupTo"

$ToRemove = @()
foreach ($name in $ConfigItems) {
  $path = Join-Path $ClaudeDir $name
  if (Test-Path -LiteralPath $path) { $ToRemove += $path }
}
if ($IncludeAuth -and (Test-Path -LiteralPath $AuthFile)) { $ToRemove += $AuthFile }
if ($Project) {
  $projClaude = Join-Path $Project '.claude'
  if (Test-Path -LiteralPath $projClaude) { $ToRemove += $projClaude }
}

if ($ToRemove.Count -eq 0) {
  Step "zaxiraga narsa yo'q, sozlama topilmadi"
} else {
  foreach ($path in $ToRemove) { Step "$path" }
  if ($Apply) {
    New-Item -ItemType Directory -Path $BackupTo -Force | Out-Null
    foreach ($path in $ToRemove) {
      $leaf = Split-Path -Leaf $path
      $parent = Split-Path -Leaf (Split-Path -Parent $path)
      $dest = Join-Path $BackupTo "$parent--$leaf"
      Copy-Item -LiteralPath $path -Destination $dest -Recurse -Force
    }
    Step "zaxira yozildi: $($ToRemove.Count) birlik"
  }
}

# --- 3. Tozalash ---------------------------------------------------------

Say ""
Say "2. Tozalash"

foreach ($path in $ToRemove) {
  Step "o'chiriladi: $path"
  if ($Apply) { Remove-Item -LiteralPath $path -Recurse -Force }
}
if (-not $IncludeAuth) {
  Step "qoladi: $AuthFile (kirish ma'lumoti; -IncludeAuth bilan o'chadi)"
}
Step "qoladi: projects\, todos\, history.jsonl (suhbat tarixi)"

# --- 4. O'rnatish --------------------------------------------------------

Say ""
Say "3. manguberdi o'rnatilmoqda"

$skillSrc = Join-Path $GeniusPath '.claude\skills\manguberdi'
$skillDst = Join-Path $ClaudeDir 'skills\manguberdi'
$agentsDst = Join-Path $ClaudeDir 'agents'

Step "skill  -> $skillDst"
if ($Apply) {
  New-Item -ItemType Directory -Path (Split-Path -Parent $skillDst) -Force | Out-Null
  Copy-Item -LiteralPath $skillSrc -Destination $skillDst -Recurse -Force
}

Step "aktyorlar -> $agentsDst"
if ($Apply) { New-Item -ItemType Directory -Path $agentsDst -Force | Out-Null }
foreach ($actor in $Actors) {
  $src = Join-Path $GeniusPath ".claude\agents\$actor.md"
  if (-not (Test-Path -LiteralPath $src)) {
    Say "  OGOHLANTIRISH: aktyor fayli yo'q: $actor.md"
    continue
  }
  Step "  $actor"
  if ($Apply) { Copy-Item -LiteralPath $src -Destination $agentsDst -Force }
}

# --- 4b. Yo'llarni mutlaq qilish -----------------------------------------

# Skill matnida buyruqlar `python3 tools/rules_for.py` ko'rinishida yozilgan
# va bu yo'l JORIY papkaga nisbatan hal qilinadi. Global o'rnatilgan skill
# boshqa proyektda ishlatilsa, ularning hammasi topilmaydi. Almashtirish
# Python da, chunki bu qism sinaladi: tools/test_rewrite_paths.py.

$rewriter = Join-Path $GeniusPath 'install\rewrite_paths.py'
$bashArg = if ($BashExe) { $BashExe.Replace('\', '/') } else { 'bash' }

Say ""
Say "3b. Yo'llar mutlaq qilinmoqda"
Step "manba: $GeniusPath"
Step "bash : $bashArg"

if ($Apply) {
  foreach ($target in @($skillDst, $agentsDst)) {
    $out = & $PythonExe $rewriter $target '--root' $GeniusPath '--bash' $bashArg 2>&1
    if ($LASTEXITCODE -ne 0) {
      Say "  XATO: yo'llarni almashtirish yiqildi: $out"
      Say "  Zaxira: $BackupTo"
      exit 1
    }
    Step "$out"
  }
}

# --- 5. Sozlama ----------------------------------------------------------

# Hook yo'llari MUTLAQ bo'ladi. Repodagi settings.json $CLAUDE_PROJECT_DIR
# ishlatadi, u esa faol proyektni ko'rsatadi; global o'rnatishda asboblar
# boshqa papkada turadi, shuning uchun yo'l aynan shu klonga bog'lanadi.
$toolsDir = Join-Path $GeniusPath 'tools'

function HookCmd([string]$script) {
  return ('"{0}" "{1}"' -f $PythonExe, (Join-Path $toolsDir $script))
}

$settings = [ordered]@{
  '$schema' = 'https://json.schemastore.org/claude-code-settings.json'
  bashOutputMaxChars = 12000
  hooks = [ordered]@{
    UserPromptSubmit = @(
      [ordered]@{ hooks = @([ordered]@{
        type = 'command'; command = (HookCmd 'suggest_sections.py')
        timeout = 10; statusMessage = "Mos bo'limlar qidirilmoqda" }) }
    )
    PreToolUse = @(
      [ordered]@{ matcher = 'Read|Bash'; hooks = @([ordered]@{
        type = 'command'; command = (HookCmd 'guard.py')
        timeout = 10; statusMessage = 'Qimmat amal tekshirilmoqda' }) },
      [ordered]@{ matcher = 'Task|Agent'; hooks = @([ordered]@{
        type = 'command'; command = (HookCmd 'budget.py')
        timeout = 10; statusMessage = 'Aktyor budjeti tekshirilmoqda' }) }
    )
    PostToolUse = @(
      [ordered]@{ matcher = 'Write|Edit'; hooks = @([ordered]@{
        type = 'command'; command = (HookCmd 'check_code.py')
        timeout = 15; statusMessage = 'Java qoidalari tekshirilmoqda' }) }
    )
    Stop = @(
      [ordered]@{ hooks = @([ordered]@{
        type = 'command'; command = ((HookCmd 'usage.py') + ' --saqlash')
        timeout = 20; statusMessage = 'Token sarfi yozilmoqda' }) }
    )
  }
}

$settingsPath = Join-Path $ClaudeDir 'settings.json'
Say ""
Say "4. Sozlama -> $settingsPath"
Step "besh hook: bo'lim taklifi, qo'riqchi, budjet, kod tekshiruvi, sarf hisobi"
Step "yo'llar mutlaq, manba: $toolsDir"

if ($Apply) {
  New-Item -ItemType Directory -Path $ClaudeDir -Force | Out-Null
  $json = $settings | ConvertTo-Json -Depth 10
  Set-Content -LiteralPath $settingsPath -Value $json -Encoding UTF8
}

# --- 6. Tekshirish -------------------------------------------------------

Say ""
Say "5. Tekshirish"

if (-not $Apply) {
  Say ""
  Say "Hech narsa o'zgarmadi. Bajarish uchun ayni buyruqqa -Apply qo'shing."
  exit 0
}

$ok = $true

if (Test-Path -LiteralPath (Join-Path $skillDst 'SKILL.md')) {
  Step "skill joyida"
} else { Step "XATO: skill ko'chmadi"; $ok = $false }

$agentFiles = Get-ChildItem -LiteralPath $agentsDst -Filter '*.md' -ErrorAction SilentlyContinue
$agentCount = @($agentFiles).Count
Step "aktyor fayli: $agentCount"
if ($agentCount -lt $Actors.Count) { $ok = $false }

try {
  $null = Get-Content -LiteralPath $settingsPath -Raw | ConvertFrom-Json
  Step "settings.json o'qiladi"
} catch { Step "XATO: settings.json buzuq"; $ok = $false }

# Nisbiy yo'l qolmaganini tasdiqlash. Qolsa, skill boshqa proyektda
# jim ishlamaydi: buyruq topilmaydi, sabab ko'rinmaydi.
foreach ($target in @($skillDst, $agentsDst)) {
  $check = & $PythonExe $rewriter $target '--root' $GeniusPath '--tekshir' 2>&1
  if ($LASTEXITCODE -eq 0) { Step "nisbiy yo'l qolmadi: $(Split-Path -Leaf $target)" }
  else { Step "XATO: $check"; $ok = $false }
}

# Asboblarning o'zi ishlayaptimi: bitta arzon chaqiruv yetadi.
try {
  $probe = & $PythonExe (Join-Path $toolsDir 'budget.py') '--holat' 2>&1
  if ($LASTEXITCODE -eq 0) { Step "asboblar ishlayapti" }
  else { Step "XATO: budget.py yiqildi: $probe"; $ok = $false }
} catch { Step "XATO: Python asbobni yurgizmadi: $_"; $ok = $false }

Say ""
if ($ok) {
  Say "Tayyor. Yangi sessiyada /manguberdi deb chaqiring."
  Say "Zaxira: $BackupTo"
  Say ""
  Say "Diqqat: skill qo'llanmani shu klondan o'qiydi."
  Say "$GeniusPath ko'chirilsa yoki o'chirilsa, hooklar ishlamay qoladi:"
  Say "skriptni yangi yo'l bilan qayta yurgizing."
} else {
  Say "O'rnatish to'liq emas, yuqoriga qarang. Zaxira: $BackupTo"
  exit 1
}
