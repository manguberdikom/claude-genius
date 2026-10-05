<#
.SYNOPSIS
  Claude Code sozlamalarini tozalaydi va faqat manguberdi skillini o'rnatadi.

.DESCRIPTION
  Bu skript SIZNING Windows mashinangizda ishlaydi, agent sessiyasida
  ishlamaydi. Repo qoidasi PowerShell ni agentga taqiqlaydi va tools/guard.py
  uni yurgizishga urinishni to'sadi: taqiq o'z o'rnida qoladi, bu fayl esa
  o'rnatuvchi, ish asbobi emas.

  Skript yozilgan muhitda PowerShell yo'q, shuning uchun uni CI sinaydi:
  windows-latest da powershell (5.1) va pwsh (7) bilan quruq yurish va
  -Apply. -Update ham CI da yuradi, faqat -Project yurmaydi. Baribir birinchi yurgizish quruq
  o'tadi: -Apply bermaguncha sozlamaga tegilmaydi. Quruq yurish ham
  Python ni haqiqatan chaqiradi va skillni vaqtinchalik papkada yig'ib
  sinaydi, keyin uni o'chiradi: nosozlik hech narsa o'chmasidan oldin
  chiqadi. Avval ro'yxatni o'qing.

  Nima o'chiriladi (global, $HOME\.claude; -Update da faqat manguberdi
  birliklari, pastda):
    settings.json, settings.local.json, CLAUDE.md,
    skills\, agents\, commands\, plugins\, hooks\, rules\, output-styles\
  Nima QOLADI:
    projects\ (suhbat tarixi), todos\, history.jsonl, shell-snapshots\,
    statsig\, .credentials.json (kirish tokeni; Windows da Credential
    Manager da ham turishi mumkin) va $HOME\.claude.json (user MCP
    serverlar, proyekt trust va ruxsatlari, onboarding holati).
  Tegilmaydi: managed-settings.json, proyektdagi CLAUDE.md, CLAUDE.local.md
    va .mcp.json, boshqa proyektlarning .claude\ papkasi.

.PARAMETER GeniusPath
  claude-genius klonining yo'li. Skill qo'llanmasiz ishlamaydi: doc.sh,
  index va docs\ aynan shu yerdan olinadi.

.PARAMETER Project
  Qo'shimcha: shu proyektdagi .claude\ papkasi ham tozalanadi. Klon yoki
  uy papkasi berilmaydi: skript buni rad etadi. .claude\ git da bo'lsa,
  o'chirish keyingi commit ga tushadi: git status bilan tekshiring.

.PARAMETER Apply
  Haqiqatan bajarish. Bersiz faqat ro'yxat chiqadi.

.PARAMETER Update
  Yangilash (git pull dan keyin). Hamma sozlama tozalanmaydi: faqat
  skills\manguberdi, olti aktyor fayli va settings.json dagi klon tools\
  ga ishora qilgan hook va ruxsatlar zaxiralanib almashtiriladi. Boshqa
  skill, agent, CLAUDE.md va sozlama yozuvlari joyida qoladi.
  Birlashtirishni install\merge_settings.py qiladi. -Project va
  -IncludeAuth bilan birga berilmaydi.

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
  git pull dan keyin faqat manguberdi birliklarini almashtiradi.
#>

[CmdletBinding()]
param(
  [Parameter(Mandatory = $true)][string]$GeniusPath,
  [string]$Project = "",
  [switch]$Apply,
  [switch]$Update,
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

# Sinov yig'imi papkasi. Fail uni tozalaydi, shuning uchun oldindan e'lon.
$Stage = $null

function Say([string]$text, [string]$Color) {
  if ($Color) { Write-Host $text -ForegroundColor $Color } else { Write-Host $text }
}
function Step([string]$text) { Write-Host "  $text" }

function Fail([string]$text) {
  Write-Host "XATO: $text" -ForegroundColor Red
  if ($script:Stage -and (Test-Path -LiteralPath $script:Stage)) {
    Remove-Item -LiteralPath $script:Stage -Recurse -Force -ErrorAction SilentlyContinue
  }
  exit 1
}

# Native buyruqni chaqiradi. Windows PowerShell 5.1 da `2>&1` bilan har
# stderr qatori xato yozuviga aylanadi va 'Stop' ostida skript sababni
# aytmay to'xtaydi. Shuning uchun chaqiruv vaqtida 'Continue', chiqish
# esa matn: Out va Code.
function Invoke-Native([string]$Exe, [string[]]$ArgList, [string]$InputText) {
  $prev = $ErrorActionPreference
  $ErrorActionPreference = 'Continue'
  try {
    if ($InputText) {
      $lines = $InputText | & $Exe @ArgList 2>&1 | ForEach-Object { "$_" }
    } else {
      $lines = & $Exe @ArgList 2>&1 | ForEach-Object { "$_" }
    }
    $code = $LASTEXITCODE
  } catch {
    $lines = @("$_")
    $code = 1
  } finally {
    $ErrorActionPreference = $prev
  }
  return [pscustomobject]@{ Out = (@($lines) -join "`n").Trim(); Code = $code }
}

function Invoke-Py([string[]]$ArgList, [string]$InputText) {
  return Invoke-Native $script:PythonExe $ArgList $InputText
}

# Python nomi bo'yicha emas, ishga tushirib tanlanadi. WindowsApps dagi
# python.exe va python3.exe Microsoft Store stub'i: Get-Command ularni
# topadi, lekin ular Python emas. `py -3` birinchi, chunki python.org
# o'rnatuvchisi python3.exe bermaydi. Natija sys.executable: hook va skill
# matniga aynan shu to'liq yo'l yoziladi.
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

# --- 1. Manbani tekshirish -------------------------------------------------

# -Update faqat o'z birliklarini almashtiradi, -Project va -IncludeAuth esa
# to'liq tozalashning qismi: birga berilsa qaysi biri ustun ekani noaniq.
if ($Update -and ($Project -or $IncludeAuth)) {
  Fail "-Update bilan -Project yoki -IncludeAuth berilmaydi: ular to'liq tozalash uchun."
}

if ($env:CLAUDE_CONFIG_DIR) {
  Fail ("CLAUDE_CONFIG_DIR o'rnatilgan ($env:CLAUDE_CONFIG_DIR): Claude Code " +
        "sozlamani o'sha yerdan o'qiydi, skript esa $ClaudeDir ni tozalaydi. " +
        "O'zgaruvchini olib tashlab qayta yurgizing.")
}

if (-not (Test-Path -LiteralPath $GeniusPath -PathType Container)) {
  Fail "GeniusPath topilmadi: $GeniusPath"
}
# ProviderPath: PSDrive yoki provider-qualified yo'l Python ga tushunarli
# bo'ladi. Oxirgi slash kesiladi: bo'sh joyli yo'lda `"C:\a b\"` native
# argumentda `\"` qo'shtirnoqni ekranlab, keyingi argumentlarni yutadi.
$GeniusPath = (Resolve-Path -LiteralPath $GeniusPath).ProviderPath.TrimEnd('\', '/')
$toolsDir = Join-Path $GeniusPath 'tools'

$Required = @(
  'tools\doc.sh', 'tools\guard.py', 'tools\check_code.py', 'tools\rules_for.py',
  'tools\budget.py', 'tools\suggest_sections.py', 'tools\usage.py',
  'tools\handoff.py', 'tools\state.py', 'tools\docref.py',
  'tools\build_index.py', 'tools\check_docs.py', 'install\rewrite_paths.py',
  'docs\manifest.json', '.claude\skills\manguberdi\SKILL.md'
)
if ($Update) { $Required += 'install\merge_settings.py' }
foreach ($rel in $Required) {
  if (-not (Test-Path -LiteralPath (Join-Path $GeniusPath $rel))) {
    Fail "klon to'liq emas, yo'q: $rel"
  }
}

# -Project ning .claude\ papkasi o'chiriladi. Uy papkasi berilsa bu global
# papkaning o'zi (tarix va kirish ketadi), klon berilsa o'rnatish manbasi.
# Shuning uchun bu hech narsa boshlanmasidan, quruq yurishda ham rad etiladi.
$projClaude = $null
if ($Project) {
  if (-not (Test-Path -LiteralPath $Project -PathType Container)) {
    Fail "Project topilmadi: $Project"
  }
  $Project = (Resolve-Path -LiteralPath $Project).ProviderPath.TrimEnd('\', '/')
  $projClaude = Join-Path $Project '.claude'
  $himoya = @($ClaudeDir, (Join-Path $GeniusPath '.claude'))
  if ($himoya | Where-Object { $_.TrimEnd('\') -ieq $projClaude.TrimEnd('\') }) {
    Fail "-Project klon yoki uy papkasi bo'la olmaydi: $Project"
  }
}

# Zaxira hech qachon avvalgisi ustidan yozilmaydi: qayta yurgizishda bir
# xil -BackupTo asl settings.json nusxasini o'rnatilgani bilan bosardi.
if (-not $BackupTo) {
  $BackupTo = Join-Path $UserHome (".claude-backup-" + (Get-Date -Format 'yyyyMMdd-HHmmss'))
}
if ((Test-Path -LiteralPath $BackupTo) -and
    @(Get-ChildItem -LiteralPath $BackupTo -Force).Count -gt 0) {
  Fail ("zaxira papkasi bo'sh emas: $BackupTo. Avvalgi zaxira ustidan " +
        "yozilmaydi: yangi yo'l bering yoki -BackupTo ni olib tashlang.")
}

$PythonExe = Find-Python
if (-not $PythonExe) {
  Fail ("ishlaydigan Python 3.8+ topilmadi (py -3, python, python3 sinaldi; " +
        "WindowsApps dagi Microsoft Store stub'i hisoblanmaydi). Hooklar " +
        "Python bilan ishlaydi, usiz o'rnatish ma'nosiz.")
}

# doc.sh bash skripti va qidiruv qatlamining hammasi unga tayanadi.
# Windows da bash kafolatlanmagan: Git for Windows bilan keladi. Git ning
# odatiy papkalari PATH dan oldin qaraladi, chunki Claude Code ning Bash
# vositasi ham Git Bash. System32 dagi bash.exe WSL ishga tushirgichi
# (WindowsApps dagisi uning yorlig'i): u C:\ yo'llarini boshqa fayl
# tizimida ochadi, shuning uchun bash hisoblanmaydi.
$BashExe = $null
foreach ($candidate in @(
    "$env:ProgramFiles\Git\bin\bash.exe",
    "${env:ProgramFiles(x86)}\Git\bin\bash.exe",
    "$env:LOCALAPPDATA\Programs\Git\bin\bash.exe")) {
  if (Test-Path -LiteralPath $candidate -PathType Leaf) {
    $BashExe = $candidate
    break
  }
}
if (-not $BashExe) {
  $BashExe = Get-Command 'bash' -CommandType Application -All -ErrorAction SilentlyContinue |
    Where-Object { $_.Source -notmatch '\\(System32|WindowsApps)\\bash\.exe$' } |
    Select-Object -First 1 -ExpandProperty Source
}

# Git for Windows odatda core.autocrlf=true bilan klonlaydi va doc.sh CRLF
# bilan yoziladi. Bash uni birinchi qatordayoq to'xtatadi (set: pipefail:
# invalid option name) va qidiruv jim ishlamay qoladi. Bash hali yo'q
# bo'lsa ham rad etiladi: keyin o'rnatilganda xuddi shu yiqiladi.
$docSh = Join-Path $toolsDir 'doc.sh'
if ([IO.File]::ReadAllText($docSh).Contains("`r`n")) {
  Fail ("tools\doc.sh CRLF bilan olingan, bash uni yurgizmaydi. Yechim: " +
        "$docSh ni o'chirib 'git -C `"$GeniusPath`" -c core.autocrlf=false " +
        "checkout -- tools/doc.sh', yoki klonni 'git clone -c " +
        "core.autocrlf=false' bilan qayta oling. Hech narsa o'chmadi.")
}

# ~/.claude.json dagi user scope MCP serverlar har proyektda ishlaydi va
# skript ularga tegmaydi, shuning uchun nomlari ochiq aytiladi. Fayl faqat
# o'qiladi, joyida tahrirlanmaydi.
$UserMcp = @()
if (Test-Path -LiteralPath $AuthFile) {
  try {
    $cfg = Get-Content -LiteralPath $AuthFile -Raw | ConvertFrom-Json
    $prop = $cfg.PSObject.Properties['mcpServers']
    if ($prop -and $prop.Value) {
      $UserMcp = @($prop.Value.PSObject.Properties | ForEach-Object { $_.Name })
    }
  } catch { $UserMcp = @() }
}

Say ""
Say "Manba : $GeniusPath"
Say "Python: $PythonExe"
Say ("Bash  : " + $(if ($BashExe) { $BashExe } else { "TOPILMADI" }))
Say "Global: $ClaudeDir"
if ($Project) { Say "Proyekt: $Project" }
Say ("Rejim : " + $(if ($Apply) { 'BAJARILADI' } else { 'quruq yurish (-Apply bermadingiz)' }) +
     $(if ($Update) { ', yangilash (-Update)' } else { '' }))

# Managed sozlama hammadan ustun: skript unga tegmaydi, lekin u hooklarni
# o'chirib qo'ysa o'rnatish jim ishlamaydi.
foreach ($m in @("$env:ProgramFiles\ClaudeCode\managed-settings.json",
                 "$env:ProgramData\ClaudeCode\managed-settings.json")) {
  if (Test-Path -LiteralPath $m) {
    Say ""
    Say ("DIQQAT: $m topildi. U eng ustun sozlama, skript unga tegmaydi; " +
         "disableAllHooks yoki allowManagedHooksOnly bo'lsa hooklar ishlamaydi.") Yellow
  }
}

if (-not $BashExe) {
  Say ""
  Say "OGOHLANTIRISH: bash topilmadi." Yellow
  Say "  tools\doc.sh bash skripti, qidiruv qatlamining hammasi unga tayanadi:"
  Say "  find, show, rule, checklist, outline. Usiz skill qoida matnini"
  Say "  o'qiy olmaydi, faqat hooklar ishlaydi."
  Say "  Yechim: Git for Windows o'rnating (https://git-scm.com/download/win),"
  Say "  keyin shu skriptni qayta yurgizing. WSL dagi bash hisoblanmaydi."
  Say ""
}

# --- 2. Sinov yig'imi ----------------------------------------------------

# Skill avval vaqtinchalik papkada yig'iladi va sinaladi, keyin o'rniga
# ko'chadi. Yo'l almashtirish yoki indeks yiqilsa, hali hech narsa
# o'chmagan bo'ladi. Quruq yurishda ham ishlaydi: faqat %TEMP% ga yozadi.
#
# Skill matnida buyruqlar `python3 tools/rules_for.py` ko'rinishida yozilgan
# va bu yo'l JORIY papkaga nisbatan hal qilinadi. Global o'rnatilgan skill
# boshqa proyektda ishlatilsa, ularning hammasi topilmaydi. Almashtirish
# Python da, chunki bu qism sinaladi: tools/test_rewrite_paths.py.

$skillSrc = Join-Path $GeniusPath '.claude\skills\manguberdi'
$rewriter = Join-Path $GeniusPath 'install\rewrite_paths.py'
$merger = Join-Path $GeniusPath 'install\merge_settings.py'
# Skill matniga topilgan to'liq yo'l emas, `bash` nomi yoziladi: Claude
# Code ning Bash vositasi Git Bash ichida yuradi va u yerda `bash` o'sha
# o'rnatishning /usr/bin/bash ga tushadi. $BashExe faqat shu skriptning
# o'z ogohlantirishi va tekshiruvi uchun.
$bashArg = 'bash'
$pyArg = $PythonExe.Replace('\', '/')
$Utf8NoBom = New-Object Text.UTF8Encoding $false

$Stage = Join-Path ([IO.Path]::GetTempPath()) ("manguberdi-" + [guid]::NewGuid().ToString('N').Substring(0, 8))
$stageSkill = Join-Path $Stage 'skills\manguberdi'
$stageAgents = Join-Path $Stage 'agents'

Say ""
Say "0. Sinov yig'imi -> $Stage"
Step "python: $pyArg"
Step "bash  : $bashArg (skill matnida shu nom)"

New-Item -ItemType Directory -Path (Split-Path -Parent $stageSkill) -Force | Out-Null
New-Item -ItemType Directory -Path $stageAgents -Force | Out-Null
Copy-Item -LiteralPath $skillSrc -Destination $stageSkill -Recurse -Force
foreach ($actor in $Actors) {
  $src = Join-Path $GeniusPath ".claude\agents\$actor.md"
  if (-not (Test-Path -LiteralPath $src)) {
    Say "  OGOHLANTIRISH: aktyor fayli yo'q: $actor.md"
    continue
  }
  Copy-Item -LiteralPath $src -Destination $stageAgents -Force
}

foreach ($target in @($stageSkill, $stageAgents)) {
  $r = Invoke-Py @($rewriter, $target, '--root', $GeniusPath,
                   '--python', $pyArg, '--bash', $bashArg)
  if ($r.Code -ne 0) { Fail "yo'llarni almashtirish yiqildi, hech narsa o'chmadi: $($r.Out)" }
  Step $r.Out
  $r = Invoke-Py @($rewriter, $target, '--root', $GeniusPath, '--tekshir')
  if ($r.Code -ne 0) { Fail "nisbiy yo'l qoldi, hech narsa o'chmadi: $($r.Out)" }
}

# Global ruxsat ro'yxati. Qoida buyruq matnining aynan boshlanishi bo'lishi
# shart, aks holda mos kelmaydi; shuning uchun uni yo'llarni yozgan asbob
# o'zi beradi, bu yerda qo'lda yig'ilmaydi.
$r = Invoke-Py @($rewriter, $Stage, '--root', $GeniusPath,
                 '--python', $pyArg, '--bash', $bashArg, '--allow')
if ($r.Code -ne 0) { Fail "ruxsat ro'yxati yasalmadi, hech narsa o'chmadi: $($r.Out)" }
$Allow = @()
try {
  foreach ($rule in ($r.Out | ConvertFrom-Json)) { $Allow += [string]$rule }
} catch { Fail "ruxsat ro'yxati o'qilmadi: $($r.Out)" }
Step "ruxsat qoidasi: $($Allow.Count) ta"

# Sozlama shu yerda yig'iladi, yoziladi esa 6-bo'limda: -Update da eski
# settings.json bilan birlashtirish shu yerda quruq sinaladi va buzuq fayl
# hech narsa o'chmasidan oldin chiqadi.
#
# Hook yo'llari MUTLAQ bo'ladi. Repodagi settings.json ${CLAUDE_PROJECT_DIR}
# ishlatadi, u esa faol proyektni ko'rsatadi; global o'rnatishda asboblar
# boshqa papkada turadi, shuning uchun yo'l aynan shu klonga bog'lanadi.
function HookCmd([string]$script) {
  return ('"{0}" "{1}"' -f $PythonExe, (Join-Path $toolsDir $script))
}

# Klon additionalDirectories da: Read, Grep va Glob qo'llanmani har
# proyektdan so'rovsiz o'qiydi. Asbob buyruqlari esa $Allow dan.
# GENIUS_PYTHON: doc.sh indeksni qayta yasaganda nom bo'yicha qidirmasdan
# aynan sinalgan Python ni oladi (python3 nomi Store stub'iga tushadi).
# Hook jadvali repodagi .claude/settings.json bilan bir xil: biri
# o'zgarsa, ikkinchisi ham moslanadi: tools/test_rewrite_paths.py dagi
# case_ps1_hooklari_repoga_mos nomuvofiqlikda CI ni yiqitadi.
$settings = [ordered]@{
  '$schema' = 'https://json.schemastore.org/claude-code-settings.json'
  bashOutputMaxChars = 12000
  env = [ordered]@{ GENIUS_PYTHON = $pyArg }
  permissions = [ordered]@{
    additionalDirectories = @($GeniusPath.Replace('\', '/'))
    allow = $Allow
  }
  hooks = [ordered]@{
    UserPromptSubmit = @(
      [ordered]@{ hooks = @(
        [ordered]@{
          type = 'command'; command = (HookCmd 'suggest_sections.py')
          timeout = 10; statusMessage = "Mos bo'limlar qidirilmoqda" },
        [ordered]@{ type = 'command'; command = (HookCmd 'budget.py'); timeout = 10 },
        [ordered]@{
          type = 'command'; command = ((HookCmd 'handoff.py') + ' --hook')
          timeout = 10; statusMessage = "Kontekst o'lchanmoqda" }) }
    )
    PreToolUse = @(
      [ordered]@{ matcher = 'Read|Bash|PowerShell'; hooks = @([ordered]@{
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

# Windows PowerShell 5.1 da Set-Content -Encoding UTF8 BOM yozadi, Claude
# Code va Python json.load esa BOM li faylda yiqiladi. Shuning uchun har
# JSON yozuvi BOM siz UTF-8 bilan.
$settingsPath = Join-Path $ClaudeDir 'settings.json'
$stageSettings = Join-Path $Stage 'settings.json'
$json = $settings | ConvertTo-Json -Depth 10
[IO.File]::WriteAllText($stageSettings, $json, $Utf8NoBom)

# -Update: settings.json ga yozmasdan, nima almashishini aytadi. Faqat
# buyrug'i shu klonning tools\ papkasiga ishora qilgan yozuvlar almashadi.
if ($Update) {
  $r = Invoke-Py @($merger, $settingsPath, $stageSettings, '--root', $GeniusPath)
  if ($r.Code -ne 0) { Fail "settings.json birlashtirilmadi, hech narsa o'chmadi: $($r.Out)" }
  Step $r.Out
}

# Indeks git da yo'q: toza klonda bo'lim taklifi hooki usiz jim bo'sh.
# U klonga yoziladi, shuning uchun faqat -Apply bilan.
$sections = Join-Path $GeniusPath 'index\sections.tsv'
if ($Apply) {
  $r = Invoke-Py @((Join-Path $toolsDir 'build_index.py'))
  if ($r.Code -ne 0 -or -not (Test-Path -LiteralPath $sections)) {
    Fail "indeks yasalmadi, hech narsa o'chmadi: $($r.Out)"
  }
  Step "indeks yasaldi: $(Split-Path -Parent $sections)"
} else {
  Step "indeks: $(Split-Path -Parent $sections) (-Apply bilan yasaladi)"
}

# --- 3. Zaxira ------------------------------------------------------------

Say ""
Say "1. Zaxira -> $BackupTo"

# $ToRemove o'chiriladi, $ToBackup zaxiraga olinadi. -Update da ular farq
# qiladi: settings.json zaxiralanadi, lekin o'chmaydi, 6-bo'limda joyida
# birlashtiriladi.
$ToRemove = @()
if ($Update) {
  $own = @(Join-Path $ClaudeDir 'skills\manguberdi')
  foreach ($actor in $Actors) { $own += (Join-Path $ClaudeDir "agents\$actor.md") }
  foreach ($path in $own) {
    if (Test-Path -LiteralPath $path) { $ToRemove += $path }
  }
  $ToBackup = @($ToRemove)
  if (Test-Path -LiteralPath $settingsPath) { $ToBackup += $settingsPath }
} else {
  foreach ($name in $ConfigItems) {
    $path = Join-Path $ClaudeDir $name
    if (Test-Path -LiteralPath $path) { $ToRemove += $path }
  }
  if ($IncludeAuth -and (Test-Path -LiteralPath $AuthFile)) { $ToRemove += $AuthFile }
  if ($projClaude) {
    if (Test-Path -LiteralPath $projClaude) { $ToRemove += $projClaude }
    else { Step "proyektda .claude yo'q: $Project" }
  }
  $ToBackup = @($ToRemove)
}

if ($ToBackup.Count -eq 0) {
  Step "zaxiraga narsa yo'q, sozlama topilmadi"
} else {
  foreach ($path in $ToBackup) { Step "$path" }
  if ($Apply) {
    New-Item -ItemType Directory -Path $BackupTo -Force | Out-Null
    foreach ($path in $ToBackup) {
      $leaf = Split-Path -Leaf $path
      $parent = Split-Path -Leaf (Split-Path -Parent $path)
      $dest = Join-Path $BackupTo "$parent--$leaf"
      Copy-Item -LiteralPath $path -Destination $dest -Recurse -Force
    }
    Step "zaxira yozildi: $($ToBackup.Count) birlik"
  }
}

# --- 4. Tozalash ---------------------------------------------------------

Say ""
if ($Update) { Say "2. Almashtirish" } else { Say "2. Tozalash" }

foreach ($path in $ToRemove) {
  if ($Update) { Step "almashtiriladi: $path" } else { Step "o'chiriladi: $path" }
  if ($Apply) { Remove-Item -LiteralPath $path -Recurse -Force }
}
if ($Update) {
  Step "qoladi: boshqa skill va agentlar, CLAUDE.md, plugins\, settings.json dagi boshqa yozuvlar"
}
if (-not $IncludeAuth) {
  Step "qoladi: $AuthFile (user MCP serverlar, proyekt trust, onboarding; -IncludeAuth bilan o'chadi)"
  foreach ($n in $UserMcp) {
    Step "qoladi: user MCP server $n (olib tashlash: claude mcp remove $n -s user)"
  }
}
Step "qoladi: .credentials.json (kirish tokeni), projects\, todos\, history.jsonl (suhbat tarixi)"

# --- 5. O'rnatish --------------------------------------------------------

Say ""
Say "3. manguberdi o'rnatilmoqda"

$skillDst = Join-Path $ClaudeDir 'skills\manguberdi'
$agentsDst = Join-Path $ClaudeDir 'agents'

Step "skill  -> $skillDst"
Step "aktyorlar -> $agentsDst"
foreach ($file in @(Get-ChildItem -LiteralPath $stageAgents -Filter '*.md')) {
  Step "  $($file.BaseName)"
}
if ($Apply) {
  # Copy-Item mavjud papkaga ko'chirsa ichida ikkinchi manguberdi\ ochadi.
  # Shuning uchun eski skill avval o'chiriladi, keyin nusxalanadi.
  if (Test-Path -LiteralPath $skillDst) { Remove-Item -LiteralPath $skillDst -Recurse -Force }
  New-Item -ItemType Directory -Path (Split-Path -Parent $skillDst) -Force | Out-Null
  Copy-Item -LiteralPath $stageSkill -Destination $skillDst -Recurse -Force
  New-Item -ItemType Directory -Path $agentsDst -Force | Out-Null
  foreach ($file in @(Get-ChildItem -LiteralPath $stageAgents -Filter '*.md')) {
    Copy-Item -LiteralPath $file.FullName -Destination $agentsDst -Force
  }
}

# --- 6. Sozlama ----------------------------------------------------------

Say ""
Say "4. Sozlama -> $settingsPath"
Step ("yetti hook: bo'lim taklifi, budjetni nolga tushirish, kontekst o'lchovi, " +
      "qo'riqchi, aktyor budjeti, kod tekshiruvi, sarf hisobi")
Step "yo'llar mutlaq, manba: $toolsDir"
Step "ruxsat: klon additionalDirectories da, $($Allow.Count) ta asbob buyrug'i oldindan ruxsatli"
if ($Update) { Step "birlashtiriladi: klon tools\ papkasiga ishora qilmagan hook va ruxsatlar saqlanadi" }

if ($Apply) {
  New-Item -ItemType Directory -Path $ClaudeDir -Force | Out-Null
  if ($Update) {
    $r = Invoke-Py @($merger, $settingsPath, $stageSettings, '--root', $GeniusPath, '--yoz')
    if ($r.Code -ne 0) {
      Fail ("settings.json birlashtirilmadi va o'zgarmadi, skill va aktyorlar esa " +
            "yangilandi. Zaxira: $BackupTo. $($r.Out)")
    }
    Step $r.Out
  } else {
    [IO.File]::WriteAllText($settingsPath, $json, $Utf8NoBom)
  }
}
Remove-Item -LiteralPath $Stage -Recurse -Force
$Stage = $null

# --- 7. Tekshirish -------------------------------------------------------

Say ""
Say "5. Tekshirish"

if (-not $Apply) {
  Say ""
  Say "Sozlama o'zgarmadi. Bajarish uchun ayni buyruqqa -Apply qo'shing."
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
  $r = Invoke-Py @($rewriter, $target, '--root', $GeniusPath, '--tekshir')
  if ($r.Code -eq 0) { Step "nisbiy yo'l qolmadi: $(Split-Path -Leaf $target)" }
  else { Step "XATO: $($r.Out)"; $ok = $false }
}

# Asboblarning o'zi ishlayaptimi: har qatlamdan bitta arzon chaqiruv.
$r = Invoke-Py @((Join-Path $toolsDir 'budget.py'), '--holat')
if ($r.Code -eq 0) { Step "asboblar ishlayapti" }
else { Step "XATO: budget.py yiqildi: $($r.Out)"; $ok = $false }

$r = Invoke-Py @((Join-Path $toolsDir 'suggest_sections.py')) '{"prompt":"circuit breaker"}'
if ($r.Code -eq 0 -and $r.Out -match 'patterns') { Step "bo'lim taklifi ishlayapti" }
else { Step "XATO: bo'lim taklifi bo'sh: $($r.Out)"; $ok = $false }

if ($BashExe) {
  $r = Invoke-Native $BashExe @((Join-Path $toolsDir 'doc.sh').Replace('\', '/'), 'find', 'circuit breaker')
  if ($r.Code -eq 0) { Step "doc.sh ishlayapti" }
  else { Step "XATO: doc.sh ishlamadi (bash ichida python3 yo'qmi?): $($r.Out)"; $ok = $false }
}

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
