# sync2sd.ps1 -- copia le novita' da C:\zx\forth\F18\tools\vForth a W:\tools\vForth
#
# Uso:
#   .\sync2sd.ps1                 copia incrementale (timestamp FAT per subdir, hash per .f e radice)
#   .\sync2sd.ps1 -DryRun         mostra cosa verrebbe copiato, senza copiare
#   .\sync2sd.ps1 -Mirror         come sopra ma CANCELLA in W: i file extra
#   .\sync2sd.ps1 -WithBlocks     include anche !Blocks-64.bin (16 MB)
#
# Hash-based copy (immune da timezone FAT):
#   - tutti i file .f (sorgenti Forth)
#   - tutti i file in radice W:\tools\vForth (binari e launcher critici)
# Timestamp-based copy (veloce, FFT/DST FAT-normalized):
#   - tutto il resto (subdirectory)
#
# Prerequisito: l'immagine SD deve essere montata come W: (vedi sd-sync.config.ps1).
# Ricorda di smontarla con  imdisk -d -m w:  prima di avviare CSpect.

param(
    [string]$Source,
    [string]$Dest,
    [switch]$DryRun,
    [switch]$Mirror,
    [switch]$WithBlocks
)

. (Join-Path $PSScriptRoot 'sd-sync.config.ps1')

# CSpect o MAME in esecuzione -> lock sull'immagine SD / !Blocks-64.bin -> impossibile sincronizzare.
$blocking = Get-RunningBlockingEmulators
if ($blocking) {
    $names = ($blocking | ForEach-Object { "$($_.ProcessName) (PID $($_.Id))" }) -join ', '
    Write-Host "ERRORE: emulatore in esecuzione: $names." -ForegroundColor Red
    Write-Host "L'immagine SD non puo' essere sincronizzata mentre CSpect o MAME la usano."
    Write-Host "Chiudi l'emulatore, poi rilancia lo script."
    exit 2
}

# Confronta due file per hash MD5 e copia se diversi.
# -LiteralPath ovunque: i nomi Forth FAT-mappati possono contenere '[' (es. ['].f).
function Sync-FileByHash([System.IO.FileInfo]$srcFile, [string]$destPath, [bool]$dryRun) {
    # Guardia: se la copia su W: ha il timestamp azzerato da CSpect (1980), e' la
    # versione piu' recente (editata nell'emulatore) -- non sovrascriverla mai.
    if (Test-CSpectEdited $destPath) {
        Write-Host "    PROTETTO (editato in CSpect, ts 1980): $($srcFile.Name) -- non sovrascritto" -ForegroundColor Yellow
        return $false
    }
    if (-not (Test-Path -LiteralPath $destPath)) {
        Write-Host "    Hash-copy: NUOVO  $($srcFile.Name)"
        if (-not $dryRun) { Copy-Item -LiteralPath $srcFile.FullName -Destination $destPath -Force }
        return $true
    }
    $destFile = Get-Item -LiteralPath $destPath
    if ($srcFile.Length -ne $destFile.Length) {
        Write-Host "    Hash-copy: DIVERSO (size) $($srcFile.Name)"
        if (-not $dryRun) { Copy-Item -LiteralPath $srcFile.FullName -Destination $destPath -Force }
        return $true
    }
    $h1 = (Get-FileHash -LiteralPath $srcFile.FullName -Algorithm MD5).Hash
    $h2 = (Get-FileHash -LiteralPath $destPath -Algorithm MD5).Hash
    if ($h1 -ne $h2) {
        Write-Host "    Hash-copy: DIVERSO (MD5) $($srcFile.Name)"
        if (-not $dryRun) { Copy-Item -LiteralPath $srcFile.FullName -Destination $destPath -Force }
        return $true
    }
    # Contenuto identico: se il timestamp e' sfasato di esattamente 2h (HDFMonkey),
    # non e' una differenza reale -- correggi solo il timestamp su W:, niente ricopia.
    if (Test-HdfMonkeyShift $srcFile.LastWriteTime $destFile.LastWriteTime) {
        Write-Host "    TS-FIX (HDFMonkey 2h, contenuto identico): $($srcFile.Name)" -ForegroundColor DarkYellow
        if (-not $dryRun) { $destFile.LastWriteTime = $srcFile.LastWriteTime }
        return $true
    }
    return $false
}

# True se il file (FileInfo) e' escluso dalla sincronizzazione.
# (Stessa logica di verify2sd.ps1; usa $excludeFiles definito piu' sotto.)
function Test-Excluded([System.IO.FileInfo]$f, [string]$root) {
    $rel = $f.FullName.Substring($root.Length).TrimStart('\')
    $parts = $rel.Split('\')
    if ($parts.Count -gt 1) {
        if ($SyncExcludeTopDirs -contains $parts[0]) { return $true }
        foreach ($p in $parts[0..($parts.Count - 2)]) {
            if ($SyncExcludeDirNames -contains $p) { return $true }
        }
    }
    foreach ($pat in $excludeFiles) {
        if ($f.Name -like $pat) { return $true }
    }
    return $false
}

if (-not $Source) { $Source = $SyncSource }
if (-not $Dest)   { $Dest   = $SyncDest }

$driveRoot = [System.IO.Path]::GetPathRoot($Dest)
if (-not (Test-Path $driveRoot)) {
    Write-Host "ERRORE: unita' $driveRoot non trovata." -ForegroundColor Red
    Write-Host "Monta l'immagine SD con:"
    Write-Host "  imdisk -a -t file -m w: -o rem -f cspect-next-2gb.img -v 1"
    exit 1
}
if (-not (Test-Path $Source)) {
    Write-Host "ERRORE: sorgente $Source non trovata." -ForegroundColor Red
    exit 1
}

# /XD vuole percorsi completi per le esclusioni di primo livello,
# nomi semplici per le esclusioni valide ovunque.
$xd = @()
foreach ($d in $SyncExcludeTopDirs)  { $xd += (Join-Path $Source $d) }
foreach ($d in $SyncExcludeDirNames) { $xd += $d }

$excludeFiles = @() + $SyncExcludeFiles
if (-not $WithBlocks) { $excludeFiles += $SyncBlocksFile }

$xf = @() + $excludeFiles

# Esclusioni aggiuntive: file .f (li copieremo per hash) e file in radice (idem).
$xf += '*.f'

# Non sovrascrivere per timestamp i file gia' editati in CSpect (destinazione con
# ts azzerato 1980): vanno esclusi anche dal robocopy di Fase 1. (Le fasi hash
# 2-4 sono gia' protette dalla guardia in Sync-FileByHash.)
$protectedXf = @(Get-CSpectProtectedSourcePaths $Dest $Source)
if ($protectedXf.Count -gt 0) {
    Write-Host "Protetti (editati in CSpect, ts 1980, non sovrascritti): $($protectedXf.Count) file" -ForegroundColor Yellow
    $xf += $protectedXf
}

if ($DryRun) {
    Write-Host "--- DRY RUN: nessun file verra' copiato ---" -ForegroundColor Yellow
}
Write-Host "Sync: $Source  ->  $Dest"
Write-Host "  Timestamp-based (FFT/DST): subdirectory"
Write-Host "  Hash-based (MD5):           file .f + file in radice (binari/launcher)"
if ($Mirror) {
    Write-Host "ATTENZIONE: -Mirror cancella in $Dest i file assenti nella sorgente." -ForegroundColor Yellow
}
if (-not $WithBlocks) {
    Write-Host "($SyncBlocksFile escluso: usa -WithBlocks per copiarlo)"
}

# 1. Robocopy per timestamp (exclude .f e radice).
Write-Host ""
Write-Host "Fase 1: timestamp-based (subdirectory)" -ForegroundColor Cyan
$args = @($Source, $Dest, '/E', '/FFT', '/DST', '/R:2', '/W:2', '/NP', '/NDL')
if ($Mirror) { $args += '/MIR' }
if ($DryRun) { $args += '/L' }
$args += '/XD'; $args += $xd
$args += '/XF'; $args += $xf

robocopy @args | Out-Null
$rc = $LASTEXITCODE
if ($rc -ge 8) {
    Write-Host "ERRORE robocopy (codice $rc)." -ForegroundColor Red
    exit 1
}

# 2. Hash-based sync per file .f (ovunque).
Write-Host ""
Write-Host "Fase 2: hash-based (.f files)" -ForegroundColor Cyan
$fFiles = Get-ChildItem $Source -Recurse -Filter '*.f' -File -Force |
    Where-Object { -not (Test-Excluded $_ $Source) }
$copied = 0
foreach ($f in $fFiles) {
    $rel = $f.FullName.Substring($Source.Length).TrimStart('\')
    $destFile = Join-Path $Dest $rel
    $dir = [System.IO.Path]::GetDirectoryName($destFile)
    if (-not (Test-Path -LiteralPath $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
    if (Sync-FileByHash $f $destFile $DryRun) { $copied++ }
}
Write-Host "  $copied file .f allineati"

# 3. Hash-based sync per file in radice (binari, launcher).
Write-Host ""
Write-Host "Fase 3: hash-based (file in radice)" -ForegroundColor Cyan
$rootFiles = Get-ChildItem $Source -File -Force |
    Where-Object { -not (Test-Excluded $_ $Source) }
$copied = 0
foreach ($f in $rootFiles) {
    $destFile = Join-Path $Dest $f.Name
    if (Sync-FileByHash $f $destFile $DryRun) { $copied++ }
}
Write-Host "  $copied file in radice allineati"

# 4. Hash-based sync dei dot-command: dot/ -> W:\dot (radice del disco).
#    Mai mirror qui: W:\dot contiene anche i dot-command della distribuzione.
Write-Host ""
Write-Host "Fase 4: hash-based (dot-command -> $SyncDotDest)" -ForegroundColor Cyan
$dotFiles = Get-ChildItem $SyncDotSource -File -Force |
    Where-Object { -not (Test-Excluded $_ $SyncDotSource) }
$copied = 0
foreach ($f in $dotFiles) {
    if (-not (Test-Path -LiteralPath $SyncDotDest)) {
        New-Item -ItemType Directory -Path $SyncDotDest -Force | Out-Null
    }
    $destFile = Join-Path $SyncDotDest $f.Name
    if (Sync-FileByHash $f $destFile $DryRun) { $copied++ }
}
Write-Host "  $copied dot-command allineati"

if ($DryRun) {
    Write-Host ""
    Write-Host "Dry run completato." -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "Copia completata." -ForegroundColor Green
    Write-Host "Ricorda: smonta con  imdisk -d -m w:  prima di avviare CSpect."
}
exit 0
