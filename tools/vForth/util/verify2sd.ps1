# verify2sd.ps1 -- verifica l'allineamento tra C:\zx\forth\F18\tools\vForth e W:\tools\vForth
#
# Uso:
#   .\verify2sd.ps1               verifica (timestamp FAT per subdir, hash per .f e radice)
#   .\verify2sd.ps1 -WithBlocks   include anche !Blocks-64.bin nel confronto
#
# Strategia:
#   - file .f (sorgenti Forth):       sempre hash MD5 (immune da timezone FAT)
#   - file in radice (binari):        sempre hash MD5 (immune da timezone FAT)
#   - tutto il resto:                 timestamp FFT/DST (veloce)
#
# Exit code: 0 = allineato, 1 = differenze trovate o errore.

param(
    [string]$Source,
    [string]$Dest,
    [switch]$WithBlocks
)

. (Join-Path $PSScriptRoot 'sd-sync.config.ps1')

if (-not $Source) { $Source = $SyncSource }
if (-not $Dest)   { $Dest   = $SyncDest }

if (-not (Test-Path $Dest)) {
    Write-Host "ERRORE: destinazione $Dest non trovata. Immagine SD montata?" -ForegroundColor Red
    Write-Host "  imdisk -a -t file -m w: -o rem -f cspect-next-2gb.img -v 1"
    exit 1
}

$excludeFiles = @() + $SyncExcludeFiles
if (-not $WithBlocks) { $excludeFiles += $SyncBlocksFile }

# True se il file (FileInfo) e' escluso dalla sincronizzazione.
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

$problems = 0

Write-Host "Verifica: $Source  <->  $Dest"
Write-Host "  Timestamp (FFT/DST): subdirectory"
Write-Host "  Hash (MD5):          file .f + file in radice"
Write-Host ""

# 1. Robocopy per timestamp (exclude .f e radice).
Write-Host "Fase 1: timestamp-based (subdirectory)" -ForegroundColor Cyan
$xd = @()
foreach ($d in $SyncExcludeTopDirs)  { $xd += (Join-Path $Source $d) }
foreach ($d in $SyncExcludeDirNames) { $xd += $d }

$xf = @() + $excludeFiles
$xf += '*.f'

$args = @($Source, $Dest, '/E', '/L', '/FFT', '/DST', '/NP', '/NDL', '/NJH')
$args += '/XD'; $args += $xd
$args += '/XF'; $args += $xf

robocopy @args | Out-Null
$rc = $LASTEXITCODE
if ($rc -ge 8) {
    Write-Host "ERRORE robocopy (codice $rc)." -ForegroundColor Red
    exit 1
}
if ($rc -band 1) { $problems++ }

# 2. Hash-based verify per file .f.
Write-Host ""
Write-Host "Fase 2: hash-based (.f files)" -ForegroundColor Cyan
$srcFiles = Get-ChildItem $Source -Recurse -Filter '*.f' -File -Force |
    Where-Object { -not (Test-Excluded $_ $Source) }
$hashProblems = 0
foreach ($f in $srcFiles) {
    $rel = $f.FullName.Substring($Source.Length).TrimStart('\')
    $destFile = Join-Path $Dest $rel
    if (-not (Test-Path $destFile)) {
        Write-Host "  MANCANTE: $rel" -ForegroundColor Yellow
        $hashProblems++
        continue
    }
    $df = Get-Item $destFile
    if ($df.Length -ne $f.Length) {
        Write-Host "  DIMENSIONE: $rel" -ForegroundColor Yellow
        $hashProblems++
        continue
    }
    $h1 = (Get-FileHash $f.FullName -Algorithm MD5).Hash
    $h2 = (Get-FileHash $destFile -Algorithm MD5).Hash
    if ($h1 -ne $h2) {
        Write-Host "  MD5 DIVERSO: $rel" -ForegroundColor Yellow
        $hashProblems++
    }
}
Write-Host "  Confrontati: $($srcFiles.Count), problemi: $hashProblems"
if ($hashProblems -gt 0) { $problems++ }

# 3. Hash-based verify per file in radice.
Write-Host ""
Write-Host "Fase 3: hash-based (file in radice)" -ForegroundColor Cyan
$srcRootFiles = Get-ChildItem $Source -MaxDepth 1 -File -Force |
    Where-Object { -not (Test-Excluded $_ $Source) }
$hashProblems = 0
foreach ($f in $srcRootFiles) {
    $destFile = Join-Path $Dest $f.Name
    if (-not (Test-Path $destFile)) {
        Write-Host "  MANCANTE: $($f.Name)" -ForegroundColor Yellow
        $hashProblems++
        continue
    }
    $df = Get-Item $destFile
    if ($df.Length -ne $f.Length) {
        Write-Host "  DIMENSIONE: $($f.Name)" -ForegroundColor Yellow
        $hashProblems++
        continue
    }
    $h1 = (Get-FileHash $f.FullName -Algorithm MD5).Hash
    $h2 = (Get-FileHash $destFile -Algorithm MD5).Hash
    if ($h1 -ne $h2) {
        Write-Host "  MD5 DIVERSO: $($f.Name)" -ForegroundColor Yellow
        $hashProblems++
    }
}
Write-Host "  Confrontati: $($srcRootFiles.Count), problemi: $hashProblems"
if ($hashProblems -gt 0) { $problems++ }

if ($problems -eq 0) {
    Write-Host "OK: W: allineato con la sorgente." -ForegroundColor Green
    exit 0
} else {
    Write-Host "Differenze trovate: esegui util\sync2sd.ps1 per allineare." -ForegroundColor Yellow
    exit 1
}
