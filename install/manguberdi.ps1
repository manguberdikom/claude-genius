<#
.SYNOPSIS
  manguberdi skillini, olti aktyorni va hooklarni o'rnatadi. Sukut bo'yicha
  boshqa Claude Code sozlamalariga TEGMAYDI.

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

  SUKUT (qo'shuvchi). Faqat shu birliklar almashadi:
    skills\manguberdi, agents\ dagi olti aktyor fayli va settings.json
    dagi shu klonning tools\ papkasiga ishora qilgan hook va ruxsatlar.
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
  claude-genius klonining yo'li. Skill qo'llanmasiz ishlamaydi: doc.sh,
  index va docs\ aynan shu yerdan olinadi.

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
  olti aktyor fayli va eski aktyorlar. Begona yozuvlar qoladi. Klonning o'ziga bog'liq emas:
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
  Sukut bilan bir xil: git pull dan keyin faqat manguberdi birliklari.

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

# Sukut qo'shuvchi: faqat o'z birliklari almashadi. Avval sukut TO'LIQ
# TOZALASH edi va bitta skill uchun foydalanuvchining butun ~/.claude
# sozlamasi ketardi (zaxira bilan, lekin baribir). To'liq tozalash endi
# ataylab so'raladi: -Reset.
#
# -Update qabul qilinaversin va hech narsani o'zgartirmasin: eski
# buyruqlar, hujjatlar va CI qadamlari buzilmaydi. Skriptning qolgan
# qismi $Update ga qaraydi, shuning uchun u shu yerda hisoblanadi.
$Update = -not $Reset

$UserHome = [Environment]::GetFolderPath('UserProfile')
$ClaudeDir = Join-Path $UserHome '.claude'
$AuthFile = Join-Path $UserHome '.claude.json'
# Bir joyda: -Uninstall bloki ham, o'rnatish ham shunga yozadi.
$settingsPath = Join-Path $ClaudeDir 'settings.json'

# O'chiriladigan sozlama birliklari. Tarix, todo va kirish bu yerda yo'q:
# ular sozlama emas va ularni o'chirish ishni yo'qotadi.
$ConfigItems = @(
  'settings.json', 'settings.local.json', 'CLAUDE.md',
  'skills', 'agents', 'commands', 'plugins', 'hooks', 'rules', 'output-styles'
)

# O'rnatiladigan aktyorlar. Skill shu nomlar bilan chaqiradi.
$Actors = @('qidiruv', 'tahlil', 'review', 'dasturchi', 'test-muhandis',
            'rejalashtiruvchi')

# Olib tashlangan yoki qayta nomlangan aktyorlar. Qo'shuvchi o'rnatish
# begona faylga tegmaydi, shuning uchun eski nom agents\ da abadiy qolardi
# va eski ko'rsatma bilan subagent bo'lib ko'rinardi (dab9314: arxitektor
# dasturchi bo'ldi). Yangilash va -Uninstall ularni zaxira bilan oladi.
$Retired = @('arxitektor')

# O'rnatish manifesti: commit, sana, klon, Python va aktyorlar.
# tools\budget.py --holat commitni klon bilan solishtiradi. Keyingi
# yangilash avvalgi manifestdagi, lekin $Actors da yo'q aktyorni ham oladi:
# keyingi qayta nomlash $Retired ga qo'shilishini kutmaydi.
$ManifestPath = Join-Path $ClaudeDir 'skills\manguberdi\.genius.json'

# Eski aktyorlar: $Retired va avvalgi manifestdagi, $Actors da yo'q nomlar.
# Manifestdagi nom fayl yo'liga qo'shiladi, shuning uchun faqat harf, raqam,
# `_` va `-`.
function Get-StaleActors {
  $names = @($Retired)
  if (Test-Path -LiteralPath $ManifestPath -PathType Leaf) {
    try {
      $prev = [IO.File]::ReadAllText($ManifestPath) | ConvertFrom-Json
      $prop = $prev.PSObject.Properties['actors']
      if ($prop -and $prop.Value) { $names += @($prop.Value | ForEach-Object { [string]$_ }) }
    } catch {
      Write-Host "  OGOHLANTIRISH: $ManifestPath o'qilmadi, faqat `$Retired olinadi"
    }
  }
  return @($names | Where-Object { $_ -match '^[\w-]+$' -and ($Actors -notcontains $_) } |
    Select-Object -Unique)
}

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
# Pipe qilinadigan matn $OutputEncoding bilan yoziladi. Windows PowerShell
# 5.1 da u ASCII yoki BOM li UTF-8 bo'lishi mumkin: BOM dan JSON yiqiladi
# va hook jim qoladi. Shuning uchun chaqiruv davomida BOM siz UTF-8.
function Invoke-Native([string]$Exe, [string[]]$ArgList, [string]$InputText) {
  $prev = $ErrorActionPreference
  $prevEnc = $OutputEncoding
  $ErrorActionPreference = 'Continue'
  $OutputEncoding = New-Object Text.UTF8Encoding $false
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
    $OutputEncoding = $prevEnc
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

# -Project va -IncludeAuth to'liq tozalashning qismi: qo'shuvchi rejimda
# ularning ma'nosi yo'q, shuning uchun -Reset talab qiladi.
if (-not $Reset -and ($Project -or $IncludeAuth)) {
  Fail ("-Project va -IncludeAuth faqat -Reset bilan beriladi: ular to'liq " +
        "tozalashning qismi. Sukut rejim esa faqat manguberdi birliklarini " +
        "almashtiradi va boshqa hech narsaga tegmaydi.")
}

# To'liq tozalash ikkinchi marta ataylab aytilishini talab qiladi.
# Interaktiv so'rov emas: CI va agent sessiyasi interaktiv emas, Read-Host
# u yerda osilib qolardi yoki bo'sh javob olardi.
if ($Reset -and $Apply -and -not $ConfirmReset) {
  Fail ("-Reset -Apply ~/.claude dagi settings.json, settings.local.json, " +
        "CLAUDE.md, skills\, agents\, commands\, plugins\, hooks\, rules\ " +
        "va output-styles\ ni o'chiradi (zaxira bilan). Rozi bo'lsangiz " +
        "-ConfirmReset ham qo'shing. Faqat manguberdi kerak bo'lsa -Reset " +
        "bermang: sukut rejim qo'shuvchi.")
}

if ($Uninstall -and ($Project -or $IncludeAuth -or $Reset)) {
  Fail "-Uninstall bilan -Reset, -Project yoki -IncludeAuth berilmaydi."
}

if ($env:CLAUDE_CONFIG_DIR) {
  Fail ("CLAUDE_CONFIG_DIR o'rnatilgan ($env:CLAUDE_CONFIG_DIR): Claude Code " +
        "sozlamani o'sha yerdan o'qiydi, skript esa $ClaudeDir ni tozalaydi. " +
        "O'zgaruvchini olib tashlab qayta yurgizing.")
}

# -Uninstall da klon mavjud bo'lishi SHART EMAS: aynan shu holat uchun
# kerak, ya'ni klon o'chirilgan yoki ko'chirilgan va settings.json da
# uning yo'li qolgan. Shuning uchun yo'l Resolve-Path qilinmaydi, faqat
# normallanadi: u settings.json dagi yozuvlarni tanish uchun satr.
if ($Uninstall) {
  $GeniusPath = $GeniusPath.Replace('\', '/').TrimEnd('/')
  if (-not $GeniusPath.Trim('/').Trim()) {
    Fail "-GeniusPath bo'sh: olib tashlanadigan yozuvlarni tanib bo'lmaydi."
  }
} else {
  if (-not (Test-Path -LiteralPath $GeniusPath -PathType Container)) {
    Fail "GeniusPath topilmadi: $GeniusPath"
  }
  # ProviderPath: PSDrive yoki provider-qualified yo'l Python ga tushunarli
  # bo'ladi. Oxirgi slash kesiladi: bo'sh joyli yo'lda `"C:\a b\"` native
  # argumentda `\"` qo'shtirnoqni ekranlab, keyingi argumentlarni yutadi.
  $GeniusPath = (Resolve-Path -LiteralPath $GeniusPath).ProviderPath.TrimEnd('\', '/')
}

# Hook buyrug'i Git Bash da `"python" "<klon>/tools/x.py"` shaklida yuradi:
# qo'sh qo'shtirnoq ichida `$` va backtick kengayadi, `"` esa qo'shtirnoqni
# yopadi. Bunday yo'lda har hook buziladi yoki yo'ldagi matn bajariladi,
# shuning uchun o'rnatish boshlanmaydi. install\rewrite_paths.py ham xuddi
# shu belgilarda 2 qaytaradi. -Uninstall da tekshirilmaydi: u faqat eski
# yozuvni tanish uchun satr.
$UnsafeChars = [char[]]@('$', '`', '"')
function Test-SafePath([string]$what, [string]$value) {
  if ($value.IndexOfAny($UnsafeChars) -ge 0) {
    Fail ("$what yo'lida `$, backtick yoki qo'sh qo'shtirnoq bor: $value. " +
          "Hook buyrug'i bash da qo'sh qo'shtirnoq ichida yuradi va bu belgi " +
          "u yerda kengayadi yoki bajariladi. Boshqa papka tanlang.")
  }
}
if (-not $Uninstall) { Test-SafePath 'GeniusPath' $GeniusPath }
$toolsDir = Join-Path $GeniusPath 'tools'

$Required = @(
  'tools\doc.sh', 'tools\guard.py', 'tools\check_code.py', 'tools\rules_for.py',
  'tools\budget.py', 'tools\suggest_sections.py', 'tools\usage.py',
  'tools\handoff.py', 'tools\state.py', 'tools\docref.py', 'tools\hookio.py',
  'tools\build_index.py', 'tools\check_docs.py',
  'tools\review_status.py', 'tools\sonar_snapshot.py',
  'tools\run_tests.py', 'tools\parse_test_output.py', 'tools\guruh.py',
  'install\rewrite_paths.py',
  'docs\manifest.json', '.claude\skills\manguberdi\SKILL.md'
)
if ($Update) { $Required += 'install\merge_settings.py' }
# -Uninstall keyin kerak bo'ladi: klon to'liq emasligi hozir aytilsin.
$Required += 'install\uninstall_settings.py'
if (-not $Uninstall) {
  foreach ($rel in $Required) {
    if (-not (Test-Path -LiteralPath (Join-Path $GeniusPath $rel))) {
      Fail "klon to'liq emas, yo'q: $rel"
    }
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
if (-not $Uninstall) { Test-SafePath 'Python' $PythonExe }

# --- 1b. -Uninstall: o'z birliklarini olib tashlash --------------------
#
# Bu yerda, bash talabidan OLDIN va klon tekshiruvidan keyin: olib
# tashlash uchun bash ham, klon ham kerak emas. JSON jarrohligi
# install\uninstall_settings.py da, chunki PowerShell 5.1 da
# ConvertFrom-Json PSCustomObject beradi va bitta elementli massiv
# skalyarga aylanadi; Python qismi esa tools\test_uninstall_settings.py
# da sinaladi. Skript $PSScriptRoot dan olinadi, $GeniusPath dan EMAS:
# aynan shu rejimda $GeniusPath mavjud bo'lmasligi mumkin.
if ($Uninstall) {
  $uninstaller = Join-Path $PSScriptRoot 'uninstall_settings.py'
  if (-not (Test-Path -LiteralPath $uninstaller -PathType Leaf)) {
    Fail ("$uninstaller topilmadi. -Uninstall shu fayl bilan birga ishlaydi: " +
          "klonning install\ papkasidan yurgizing, yoki settings.json ni " +
          "qo'lda tahrir qiling (install\README.md, 'Klon o'chsa yoki ko'chsa').")
  }

  Say ""
  Say "manguberdi olib tashlanmoqda"
  Say "Ildiz : $GeniusPath"
  Say "Global: $ClaudeDir"
  Say ("Rejim : " + $(if ($Apply) { 'BAJARILADI' } else { 'quruq yurish (-Apply bermadingiz)' }))

  $skillDir = Join-Path $ClaudeDir 'skills\manguberdi'
  $own = @()
  if (Test-Path -LiteralPath $skillDir) { $own += $skillDir }
  # Eski aktyorlar ham: manifest skill papkasi bilan birga o'chadi,
  # shuning uchun ro'yxat o'chirishdan OLDIN olinadi.
  foreach ($actor in @($Actors) + @(Get-StaleActors)) {
    $actorFile = Join-Path $ClaudeDir "agents\$actor.md"
    if (Test-Path -LiteralPath $actorFile) { $own += $actorFile }
  }

  Say ""
  Say "1. Zaxira -> $BackupTo"
  $toBackup = @($own)
  if (Test-Path -LiteralPath $settingsPath) { $toBackup += $settingsPath }
  if ($toBackup.Count -eq 0) {
    Step "zaxiraga narsa yo'q"
  } else {
    foreach ($path in $toBackup) { Step "$path" }
    if ($Apply) {
      New-Item -ItemType Directory -Path $BackupTo -Force | Out-Null
      foreach ($path in $toBackup) {
        $leaf = Split-Path -Leaf $path
        $parent = Split-Path -Leaf (Split-Path -Parent $path)
        Copy-Item -LiteralPath $path -Destination (Join-Path $BackupTo "$parent--$leaf") -Recurse -Force
      }
      Step "zaxira yozildi: $($toBackup.Count) birlik"
    }
  }

  Say ""
  Say "2. Skill va aktyorlar"
  if ($own.Count -eq 0) { Step "manguberdi birliklari topilmadi" }
  foreach ($path in $own) {
    Step "o'chiriladi: $path"
    if ($Apply) { Remove-Item -LiteralPath $path -Recurse -Force }
  }

  Say ""
  Say "3. Sozlama -> $settingsPath"
  $uninstArgs = @($uninstaller, $settingsPath, '--root', $GeniusPath)
  if ($Apply) { $uninstArgs += '--yoz' }
  $r = Invoke-Py $uninstArgs
  if ($r.Code -ne 0) {
    Fail "settings.json o'zgarmadi: $($r.Out)"
  }
  Step $r.Out

  Say ""
  if ($Apply) {
    Say "Tayyor. manguberdi olib tashlandi, begona yozuvlar joyida."
    Say "Zaxira: $BackupTo"
    Say "Yangi sessiyada o'zgarish ko'rinadi."
  } else {
    Say "Quruq yurish tugadi. Bajarish uchun -Apply qo'shing."
  }
  exit 0
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
     $(if ($Reset) { ", TO'LIQ TOZALASH (-Reset)" } else { ", qo'shuvchi: faqat manguberdi birliklari" }))

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

# Git Bash shart. Usiz Claude Code hookni PowerShell bilan yurgizadi va
# `"python.exe" "skript.py"` shakli u yerda sintaksis xatosi: guard, budget
# va check_code jim ishlamay qolardi. tools\doc.sh ham bash skripti.
if (-not $BashExe) {
  Fail ("bash topilmadi, hech narsa o'zgarmadi. Usiz hooklar PowerShell da " +
        "yurib yiqiladi, tools\doc.sh (find, show, rule) ham ishlamaydi. " +
        "Git for Windows o'rnating (https://git-scm.com/download/win), keyin " +
        "skriptni qayta yurgizing. WSL dagi bash hisoblanmaydi.")
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

# run_tests.py global ruxsatga kirmaydi: u proyektning build kodini
# (gradlew, build.gradle, pom plaginlari) bajaradi, fork PR yoki begona
# klonda bu so'rovsiz kod bajarish bo'lardi. Ishonchli proyekt uchun tayyor
# settings.local.json bo'lagini ham rewrite_paths beradi: qoida buyruqning
# aynan boshlanishi bo'lishi shart. Oxirida ko'rsatiladi, hech qayerga
# yozilmaydi.
$r = Invoke-Py @($rewriter, $Stage, '--root', $GeniusPath,
                 '--python', $pyArg, '--bash', $bashArg, '--opt-in')
if ($r.Code -ne 0) { Fail "opt-in ruxsat bo'lagi yasalmadi, hech narsa o'chmadi: $($r.Out)" }
$OptIn = $r.Out

function Show-OptIn {
  if (-not $OptIn) { return }
  Say ""
  Say ("Ixtiyoriy: run_tests.py global ruxsatda yo'q, chunki u proyektning " +
       "build kodini bajaradi. Faqat O'ZINGIZ ishonadigan proyektda u " +
       "so'rovsiz yursin desangiz, shu bo'lakni <proyekt>\.claude\settings.local.json " +
       "ga qo'shing. Fork PR, namuna repo yoki begona klonda qo'shmang.")
  Say $OptIn
}

# Sozlama shu yerda yig'iladi, yoziladi esa 6-bo'limda: -Update da eski
# settings.json bilan birlashtirish shu yerda quruq sinaladi va buzuq fayl
# hech narsa o'chmasidan oldin chiqadi.
#
# Hook yo'llari MUTLAQ bo'ladi. Repodagi settings.json ${CLAUDE_PROJECT_DIR}
# ishlatadi, u esa faol proyektni ko'rsatadi; global o'rnatishda asboblar
# boshqa papkada turadi, shuning uchun yo'l aynan shu klonga bog'lanadi.
#
# `|| exit 1` jadvalda, shu funksiyada EMAS: handoff va usage ga argument
# qo'shiladi va u suffiksdan oldin turishi kerak. Nega kerakligi jadval
# ustidagi izohda.
function HookCmd([string]$script) {
  return ('"{0}" "{1}"' -f $PythonExe, (Join-Path $toolsDir $script))
}

# additionalDirectories da butun klon EMAS, faqat docs va memory: Read,
# Grep va Glob qo'llanma va memoryni har proyektdan so'rovsiz o'qiydi.
# Butun klon berilsa, acceptEdits rejimida aktyor tools\ dagi hook
# skriptini so'rovsiz tahrirlay olardi va o'zgarish keyingi promptda hamma
# proyektda bajarilardi (XV-Y4). Asbob buyruqlari esa $Allow dan.
# GENIUS_PYTHON: doc.sh indeksni qayta yasaganda nom bo'yicha qidirmasdan
# aynan sinalgan Python ni oladi (python3 nomi Store stub'iga tushadi).
# Hook jadvali repodagi .claude/settings.json bilan bir xil: biri
# o'zgarsa, ikkinchisi ham moslanadi: tools/test_rewrite_paths.py dagi
# case_ps1_hooklari_repoga_mos nomuvofiqlikda CI ni yiqitadi.
#
# Har buyruq oxirida `|| exit 1`. Sababi: yo'l aynan shu klonga bog'langan,
# klon o'chsa yoki ko'chsa Python "can't open file" bilan 2 kodi beradi,
# Claude Code esa hookdan kelgan 2 ni TO'SIQ deb oladi: PreToolUse da Read
# va Bash to'siladi, UserPromptSubmit da prompt modelga yetmaydi, Stop da
# sessiya tugamaydi. Ya'ni o'chgan klon Claude Code ni hamma proyektda
# ishlatmay qo'yardi. 1 esa to'smaydi, lekin Claude Code uni "hook error"
# deb ko'rsatadi: hook ishlamay qolgani jim o'tmaydi (0 da xabar faqat
# debug logga tushardi). Hooklarning o'zi to'siqni faqat JSON orqali
# beradi, shuning uchun 1 ga aylantirish hech qanday to'siqni yo'qotmaydi.
# Hook bash ichida yuradi (yuqorida $BashExe talab qilinadi), `||` esa
# PowerShell 5.1 da sintaksis xatosi bo'lardi.
$g = $GeniusPath.Replace('\', '/')
$settings = [ordered]@{
  '$schema' = 'https://json.schemastore.org/claude-code-settings.json'
  env = [ordered]@{ GENIUS_PYTHON = $pyArg }
  permissions = [ordered]@{
    additionalDirectories = @("$g/docs", "$g/memory")
    allow = $Allow
  }
  hooks = [ordered]@{
    UserPromptSubmit = @(
      [ordered]@{ hooks = @(
        [ordered]@{
          type = 'command'; command = ((HookCmd 'suggest_sections.py') + ' || exit 1')
          timeout = 10; statusMessage = "Mos bo'limlar qidirilmoqda" },
        [ordered]@{
          type = 'command'; command = ((HookCmd 'budget.py') + ' || exit 1')
          timeout = 10 },
        [ordered]@{
          type = 'command'; command = ((HookCmd 'handoff.py') + ' --hook || exit 1')
          timeout = 10; statusMessage = "Kontekst o'lchanmoqda" }) }
    )
    PreToolUse = @(
      [ordered]@{ matcher = 'Read|Bash|PowerShell'; hooks = @([ordered]@{
        type = 'command'; command = ((HookCmd 'guard.py') + ' || exit 1')
        timeout = 10; statusMessage = 'Qimmat amal tekshirilmoqda' }) },
      [ordered]@{ matcher = 'Task|Agent'; hooks = @([ordered]@{
        type = 'command'; command = ((HookCmd 'budget.py') + ' || exit 1')
        timeout = 10; statusMessage = 'Aktyor budjeti tekshirilmoqda' }) }
    )
    PostToolUse = @(
      [ordered]@{ matcher = 'Write|Edit'; hooks = @([ordered]@{
        type = 'command'; command = ((HookCmd 'check_code.py') + ' || exit 1')
        timeout = 15; statusMessage = 'Java qoidalari tekshirilmoqda' }) }
    )
    Stop = @(
      [ordered]@{ hooks = @([ordered]@{
        type = 'command'; command = ((HookCmd 'usage.py') + ' --saqlash || exit 1')
        timeout = 20; statusMessage = 'Token sarfi yozilmoqda' }) }
    )
  }
}

# Windows PowerShell 5.1 da Set-Content -Encoding UTF8 BOM yozadi, Claude
# Code va Python json.load esa BOM li faylda yiqiladi. Shuning uchun har
# JSON yozuvi BOM siz UTF-8 bilan.
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
  # Eski aktyor zaxiralanib o'chiriladi va qaytib o'rnatilmaydi. Ro'yxat
  # manifest (skill papkasi ichida) o'chishidan OLDIN olinadi.
  foreach ($actor in @(Get-StaleActors)) {
    $stalePath = Join-Path $ClaudeDir "agents\$actor.md"
    if (Test-Path -LiteralPath $stalePath) {
      Step "eski aktyor: $actor (endi o'rnatilmaydi)"
      $own += $stalePath
    }
  }
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

# Manifest skill nusxasi bilan birga yoziladi: skill o'rnatish paytidagi
# nusxa, asboblar esa klondan jonli, shuning uchun qaysi commit
# o'rnatilgani saqlanadi. git yo'q bo'lsa commit bo'sh qoladi.
Step "manifest -> $ManifestPath"
if ($Apply) {
  $commit = ''
  $g = Invoke-Native 'git' @('-C', $GeniusPath, 'rev-parse', 'HEAD')
  if ($g.Code -eq 0 -and $g.Out -match '^[0-9a-f]{40}$') { $commit = $g.Out }
  $versionFile = Join-Path $GeniusPath 'VERSION'
  $version = ''
  if (Test-Path -LiteralPath $versionFile -PathType Leaf) {
    $version = ([IO.File]::ReadAllText($versionFile)).Trim()
  }
  $manifest = [ordered]@{
    versiya = $version
    commit  = $commit
    sana    = (Get-Date).ToString('yyyy-MM-ddTHH:mm:sszzz')
    root    = $GeniusPath.Replace('\', '/')
    python  = $pyArg
    actors  = @($Actors)
  }
  [IO.File]::WriteAllText($ManifestPath, ($manifest | ConvertTo-Json -Depth 3), $Utf8NoBom)
}

# --- 6. Sozlama ----------------------------------------------------------

Say ""
Say "4. Sozlama -> $settingsPath"
Step ("yetti hook: bo'lim taklifi, budjetni nolga tushirish, kontekst o'lchovi, " +
      "qo'riqchi, aktyor budjeti, kod tekshiruvi, sarf hisobi")
Step "yo'llar mutlaq, manba: $toolsDir"
Step "ruxsat: klonning docs va memory papkalari additionalDirectories da, $($Allow.Count) ta asbob buyrug'i oldindan ruxsatli"
Step "so'raladi: run_tests.py, guruh.py birlashtir va tozala (yon ta'siri bor)"
if ($Update) { Step "birlashtiriladi: klonga ishora qilmagan hook, ruxsat (allow, ask, deny) va papkalar saqlanadi" }

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
  Show-OptIn
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

foreach ($actor in $Retired) {
  if (Test-Path -LiteralPath (Join-Path $agentsDst "$actor.md")) {
    Step "XATO: eski aktyor qoldi: $actor.md"; $ok = $false
  }
}

if (Test-Path -LiteralPath $ManifestPath -PathType Leaf) {
  Step "manifest yozildi: $ManifestPath"
} else { Step "XATO: manifest yozilmadi: $ManifestPath"; $ok = $false }

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

# GENIUS_HOOK_DEBUG: bo'sh chiqsa hook sababini stderr ga yozadi.
# CLAUDE_PROJECT_DIR ni Claude Code har hook jarayoniga beradi va hook
# faqat klonda yoki Java proyektida ishlaydi (tools/hookio.py active()).
# Shu yerda u klonga qo'yiladi, aks holda tekshiruv hookning o'rinsiz
# bo'lganini "bo'sh chiqish" deb o'qib, o'rnatishni yiqitardi.
$env:GENIUS_HOOK_DEBUG = '1'
$savedProjectDir = $env:CLAUDE_PROJECT_DIR
$env:CLAUDE_PROJECT_DIR = $GeniusPath
$r = Invoke-Py @((Join-Path $toolsDir 'suggest_sections.py')) '{"prompt":"circuit breaker"}'
Remove-Item Env:GENIUS_HOOK_DEBUG -ErrorAction SilentlyContinue
if ($null -eq $savedProjectDir) {
  Remove-Item Env:CLAUDE_PROJECT_DIR -ErrorAction SilentlyContinue
} else { $env:CLAUDE_PROJECT_DIR = $savedProjectDir }
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
  Show-OptIn
} else {
  Say "O'rnatish to'liq emas, yuqoriga qarang. Zaxira: $BackupTo"
  exit 1
}
