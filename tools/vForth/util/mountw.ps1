# mountw.ps1 -- monta/smonta l'immagine SD di CSpect come unita' W: via imdisk.
#
# Uso:
#   .\mountw.ps1                  monta l'immagine (partizione 1) su W:
#   .\mountw.ps1 -Dismount        smonta W:
#   .\mountw.ps1 -Image <path>    usa un'immagine diversa da quella in config
#
# imdisk richiede privilegi di amministratore: questo script lo lancia con
# Start-Process -Verb RunAs, quindi compare il popup UAC.
#
# Exit code: 0 = ok (o gia' nello stato richiesto), 1 = errore, 2 = CSpect attivo.

param(
    [switch]$Dismount,
    [string]$Image
)

. (Join-Path $PSScriptRoot 'sd-sync.config.ps1')

if (-not $Image) { $Image = $SyncImage }

# Mai toccare l'immagine mentre CSpect la sta usando: rischio corruzione.
$cspect = Get-Process -Name 'CSpect*' -ErrorAction SilentlyContinue
if ($cspect) {
    Write-Host "ERRORE: CSpect e' in esecuzione (PID $($cspect.Id -join ', '))." -ForegroundColor Red
    Write-Host "Chiudi CSpect prima di montare o smontare l'immagine."
    exit 2
}

$mounted = Test-Path 'W:\'

if ($Dismount) {
    if (-not $mounted) {
        Write-Host "W: non e' montata: niente da fare." -ForegroundColor Green
        exit 0
    }
    Write-Host "Smonto W: (conferma il popup UAC)..."
    try {
        Start-Process imdisk -Verb RunAs -Wait -ArgumentList '-d -m w:'
    } catch {
        Write-Host "ERRORE: elevazione negata o imdisk fallito." -ForegroundColor Red
        exit 1
    }
    # Attendi che il volume sparisca (max 15 s).
    $t = 0
    while ((Test-Path 'W:\') -and ($t -lt 15)) { Start-Sleep -Seconds 1; $t++ }
    if (Test-Path 'W:\') {
        # Smontaggio gentile fallito (file aperti sul volume, es. Explorer):
        # forza il detach come fa umounty.bat (imdisk -D).
        Write-Host "W: ancora montata: forzo lo smontaggio (conferma il popup UAC)..." -ForegroundColor Yellow
        try {
            Start-Process imdisk -Verb RunAs -Wait -ArgumentList '-D -m w:'
        } catch {
            Write-Host "ERRORE: elevazione negata o imdisk fallito." -ForegroundColor Red
            exit 1
        }
        $t = 0
        while ((Test-Path 'W:\') -and ($t -lt 15)) { Start-Sleep -Seconds 1; $t++ }
        if (Test-Path 'W:\') {
            Write-Host "ERRORE: W: risulta ancora montata anche dopo il force." -ForegroundColor Red
            exit 1
        }
        Write-Host "W: smontata (forzato)." -ForegroundColor Yellow
    }
    Write-Host "W: smontata. L'immagine e' pronta per CSpect." -ForegroundColor Green
    exit 0
}

# --- Mount ---
if ($mounted) {
    Write-Host "W: e' gia' montata:" -ForegroundColor Green
    imdisk -l -m w:
    exit 0
}
if (-not (Test-Path $Image)) {
    Write-Host "ERRORE: immagine non trovata: $Image" -ForegroundColor Red
    exit 1
}
Write-Host "Monto $Image su W: (conferma il popup UAC)..."
try {
    Start-Process imdisk -Verb RunAs -Wait -ArgumentList "-a -t file -m w: -o rem -f `"$Image`" -v 1"
} catch {
    Write-Host "ERRORE: elevazione negata o imdisk fallito." -ForegroundColor Red
    exit 1
}
# Attendi che il volume compaia (max 15 s).
$t = 0
while (-not (Test-Path 'W:\') -and ($t -lt 15)) { Start-Sleep -Seconds 1; $t++ }
if (-not (Test-Path 'W:\')) {
    Write-Host "ERRORE: il mount non e' riuscito (W: non compare)." -ForegroundColor Red
    exit 1
}
Write-Host "W: montata." -ForegroundColor Green
exit 0
