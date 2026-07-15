# sd-sync.config.ps1 -- configurazione condivisa per sync2sd.ps1 / verify2sd.ps1
# Sincronizzazione PC -> immagine SD di CSpect montata come unita' W: via imdisk:
#   imdisk -a -t file -m w: -o rem -f cspect-next-2gb.img -v 1

$SyncSource = 'C:\zx\forth\F18\tools\vForth'
$SyncDest   = 'W:\tools\vForth'

# Immagine SD di CSpect (quella effettivamente usata; esiste una copia in CSpect.2.19).
$SyncImage  = 'C:\Zx\CSpect\cspect-next-2gb.img'

# Directory escluse SOLO al primo livello (percorso completo):
# materiale di sviluppo PC che non serve sulla SD.
# - dot:   i dot-command si deployano in W:\dot, non sotto tools\vForth
# - doc:   ~15 MB di PDF/ODT/shortcut; il doc/ sulla SD e' statico
$SyncExcludeTopDirs = @(
    'dev'
    'doc'
    'dot'
    'emu'
    'forum'
    'project'
    'prompts'
    'tools'
    'version'
)

# Directory escluse OVUNQUE nell'albero (per nome).
$SyncExcludeDirNames = @(
    '.claude'
    '.git'
    '__pycache__'
    'afx'
)

# File esclusi OVUNQUE (per nome o wildcard).
$SyncExcludeFiles = @(
    'CLAUDE.md'
    'TODO.md'
    '*.ps1'
    'out.txt'
    'transcript.txt'
    '.gitattributes'
    '.gitignore'
    '*.pyc'
    '*.lnk'
    '!Blocks-64.bin_*.txt'
    'Thumbs.db'
    'desktop.ini'
)

# Il file dei Block (16 MB) si copia solo con lo switch -WithBlocks:
# sovrascriverlo distrugge gli Screen eventualmente editati dentro CSpect.
# Anche con -WithBlocks vale la guardia generale Test-CSpectEdited (vedi sotto):
# se la copia su W: ha ts 1980 non viene sovrascritta.
$SyncBlocksFile = '!Blocks-64.bin'

# I dot-command locali (dot/) si deployano nella radice del disco W:,
# non sotto tools\vForth: e' la directory \dot standard di NextZXOS.
# Solo copia/aggiornamento dei file presenti in sorgente: W:\dot contiene
# anche i dot-command della distribuzione, che non vanno toccati.
$SyncDotSource = Join-Path $SyncSource 'dot'
$SyncDotDest   = 'W:\dot'

# --- Guardia "emulatore in esecuzione" ---------------------------------------
# Sia CSpect che MAME (core Next) possono avere in uso la medesima immagine SD /
# lo stesso file !Blocks-64.bin: non devono MAI essere in esecuzione insieme, ne'
# individualmente durante mount/smount/sync dell'immagine.
$SyncBlockingProcessNames = @('CSpect*', 'mame*')

# Elenco dei processi bloccanti attualmente in esecuzione (CSpect e/o MAME).
# Vuoto se nessuno e' attivo.
function Get-RunningBlockingEmulators() {
    $found = @()
    foreach ($pattern in $SyncBlockingProcessNames) {
        $found += @(Get-Process -Name $pattern -ErrorAction SilentlyContinue)
    }
    return $found
}

# --- Guardia "timestamp azzerato da CSpect" ----------------------------------
# Quando si editano i BLOCK (o altri file) da dentro CSpect, l'emulatore riscrive
# il file sull'immagine SD ma ne AZZERA il timestamp FAT, che diventa 1980-01-01.
# Un file di destinazione (W:) con quel timestamp contiene quindi la versione PIU'
# RECENTE -- quella editata nell'emulatore -- e NON deve mai essere sovrascritto
# dalla sorgente PC. La regola e' generale: vale per qualunque file, non solo
# !Blocks-64.bin.
$SyncCSpectZeroYear = 1980

# True se $destPath esiste e ha il timestamp azzerato da CSpect (anno 1980):
# in tal caso il file va lasciato com'e' sull'immagine SD.
function Test-CSpectEdited([string]$destPath) {
    if (-not (Test-Path -LiteralPath $destPath)) { return $false }
    return ((Get-Item -LiteralPath $destPath).LastWriteTime.Year -eq $SyncCSpectZeroYear)
}

# Elenco dei path SORGENTE corrispondenti a file di destinazione protetti
# (timestamp azzerato) sotto $destRoot: da passare a robocopy /XF perche' la
# copia per timestamp (Fase 1) non li sovrascriva. Vuoto se $destRoot non esiste.
function Get-CSpectProtectedSourcePaths([string]$destRoot, [string]$srcRoot) {
    if (-not (Test-Path -LiteralPath $destRoot)) { return @() }
    Get-ChildItem -LiteralPath $destRoot -Recurse -File -Force -ErrorAction SilentlyContinue |
        Where-Object { $_.LastWriteTime.Year -eq $SyncCSpectZeroYear } |
        ForEach-Object { $srcRoot + $_.FullName.Substring($destRoot.Length) }
}

# --- Guardia "sfasamento HDFMonkey" (2 ore) ----------------------------------
# Copiando un file sull'immagine SD con HDFMonkey, il tool sfasa il timestamp di
# ESATTAMENTE 2 ore (suo comportamento bizzarro). Se il contenuto e' identico
# (stesso MD5) ma il timestamp e' sfasato di 2h, NON e' una differenza reale: la
# versione PC e quella su SD sono lo stesso file. In tal caso e' corretto allineare
# (= "sovrascrivere") il timestamp su W: a quello della sorgente.
$SyncHdfMonkeyOffsetSeconds = 2 * 3600   # sfasamento tipico di HDFMonkey
$SyncFatToleranceSeconds    = 2          # granularita' FAT (timestamp a passi di 2 s)

# True se la differenza (in valore assoluto, in entrambe le direzioni) tra i due
# timestamp e' lo sfasamento di 2 ore di HDFMonkey, entro la tolleranza FAT.
# Il chiamante deve aver GIA' verificato che il contenuto (MD5) e' identico.
function Test-HdfMonkeyShift([datetime]$srcTime, [datetime]$destTime) {
    $delta = [Math]::Abs(($srcTime - $destTime).TotalSeconds)
    return ([Math]::Abs($delta - $SyncHdfMonkeyOffsetSeconds) -le $SyncFatToleranceSeconds)
}
