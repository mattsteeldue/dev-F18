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

# CSpect in esecuzione → lock sull'immagine SD → impossibile montare/smontare.
$cspect = Get-Process -Name 'CSpect*' -ErrorAction SilentlyContinue
if ($cspect) {
    Write-Host "ERRORE: CSpect e' in esecuzione (PID $($cspect.Id -join ', '))." -ForegroundColor Red
    Write-Host "L'immagine SD non puo' essere montata/smontata mentre CSpect la usa."
    Write-Host "Chiudi CSpect, poi rilancia lo script."
    exit 2
}

# Confronta due file per hash MD5 e copia se diversi.
function Sync-FileByHash([System.IO.FileInfo]$srcFile, [string]$destPath, [bool]$dryRun) {
    if (-not (Test-Path $destPath)) {
        Write-Host "    Hash-copy: NUOVO  $($srcFile.Name)"
        if (-not $dryRun) { Copy-Item -Path $srcFile.FullName -Destination $destPath -Force }
        return $true
    }
    $destFile = Get-Item $destPath
    if ($srcFile.Length -ne $destFile.Length) {
        Write-Host "    Hash-copy: DIVERSO (size) $($srcFile.Name)"
        if (-not $dryRun) { Copy-Item -Path $srcFile.FullName -Destination $destPath -Force }
        return $true
    }
    $h1 = (Get-FileHash $srcFile.FullName -Algorithm MD5).Hash
    $h2 = (Get-FileHash $destPath -Algorithm MD5).Hash
    if ($h1 -ne $h2) {
        Write-Host "    Hash-copy: DIVERSO (MD5) $($srcFile.Name)"
        if (-not $dryRun) { Copy-Item -Path $srcFile.FullName -Destination $destPath -Force }
        return $true
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

$xf = @() + $SyncExcludeFiles
if (-not $WithBlocks) { $xf += $SyncBlocksFile }

# Esclusioni aggiuntive: file .f (li copieremo per hash) e file in radice (idem).
$xf += '*.f'

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
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
    if (Sync-FileByHash $f $destFile $DryRun) { $copied++ }
}
Write-Host "  $copied file .f allineati"

# 3. Hash-based sync per file in radice (binari, launcher).
Write-Host ""
Write-Host "Fase 3: hash-based (file in radice)" -ForegroundColor Cyan
$rootFiles = Get-ChildItem $Source -MaxDepth 1 -File -Force |
    Where-Object { -not (Test-Excluded $_ $Source) }
$copied = 0
foreach ($f in $rootFiles) {
    $destFile = Join-Path $Dest $f.Name
    if (Sync-FileByHash $f $destFile $DryRun) { $copied++ }
}
Write-Host "  $copied file in radice allineati"

if ($DryRun) {
    Write-Host ""
    Write-Host "Dry run completato." -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "Copia completata." -ForegroundColor Green
    Write-Host "Ricorda: smonta con  imdisk -d -m w:  prima di avviare CSpect."
}
exit 0
