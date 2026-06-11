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
$SyncBlocksFile = '!Blocks-64.bin'
