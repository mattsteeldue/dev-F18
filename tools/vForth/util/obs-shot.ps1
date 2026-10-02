# obs-shot.ps1 -- cattura in PNG la finestra di OBS, che mostra l'uscita video
# della ZX Spectrum Next reale (scheda di acquisizione HDMI).
#
# Uso:
#   .\obs-shot.ps1                  salva in $env:TEMP\obs-shot.png
#   .\obs-shot.ps1 -Out <path>      salva nel file indicato
#
# Usa GetWindowRect + PrintWindow (PW_RENDERFULLCONTENT) di user32: la finestra
# viene disegnata in una bitmap anche se coperta da altre, ma NON deve essere
# ridotta a icona. Cattura l'intera finestra (titolo e menu compresi), non il
# solo segnale video: se l'anteprima e' piu' alta della finestra il bordo
# inferiore resta tagliato. Via preferita, quando il server WebSocket di OBS e'
# attivo: util/obs-ws-shot.py (solo la sorgente, risoluzione nativa).
#
# Stampa il percorso del PNG salvato.
# Exit code: 0 = ok, 1 = OBS non avviato o finestra ridotta a icona.

param(
    [string]$Out = (Join-Path $env:TEMP 'obs-shot.png')
)

Add-Type -AssemblyName System.Drawing
Add-Type @'
using System;
using System.Runtime.InteropServices;
public class ObsShotW {
    [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
    [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr dc, uint f);
    [DllImport("user32.dll")] public static extern bool IsIconic(IntPtr h);
    public struct RECT { public int Left, Top, Right, Bottom; }
}
'@

$proc = Get-Process obs64 -ErrorAction SilentlyContinue |
    Where-Object { $_.MainWindowHandle -ne [IntPtr]::Zero } | Select-Object -First 1
if (-not $proc) { Write-Error 'OBS (obs64) non e'' avviato'; exit 1 }
$h = $proc.MainWindowHandle
if ([ObsShotW]::IsIconic($h)) { Write-Error 'la finestra di OBS e'' ridotta a icona'; exit 1 }

$r = New-Object ObsShotW+RECT
[ObsShotW]::GetWindowRect($h, [ref]$r) | Out-Null
$bmp = New-Object System.Drawing.Bitmap ($r.Right - $r.Left), ($r.Bottom - $r.Top)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$dc = $g.GetHdc()
[ObsShotW]::PrintWindow($h, $dc, 2) | Out-Null    # 2 = PW_RENDERFULLCONTENT
$g.ReleaseHdc($dc)
$g.Dispose()
$Out = [System.IO.Path]::GetFullPath($Out)
$bmp.Save($Out, [System.Drawing.Imaging.ImageFormat]::Png)
$bmp.Dispose()
$Out
exit 0
