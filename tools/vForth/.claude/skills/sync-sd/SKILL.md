---
name: sync-sd
description: Sincronizza le novita' del progetto vForth sull'immagine SD di CSpect (monta W: via imdisk se serve, copia con sync2sd.ps1, verifica con verify2sd.ps1, smonta). Usare quando l'utente vuole aggiornare l'immagine SD, deployare su CSpect, o chiede /sync-sd.
---

# sync-sd: deploy su immagine SD di CSpect

Sincronizza `C:\zx\forth\F18\tools\vForth` su `W:\tools\vForth` (immagine SD montata
via imdisk). Tutta la configurazione (percorsi, esclusioni, immagine) sta in
`util\sd-sync.config.ps1` -- non duplicarla qui.

## ⚠️ Prerequisito critico

**CSpect DEVE essere chiuso.** L'emulatore ha un lock esclusivo sull'immagine SD:
se CSpect è in esecuzione, l'immagine non può essere montata né smontata su W:,
e il sync fallirà. Lo script verifica lo stato all'avvio e si ferma con un messaggio
esplicito se CSpect è attivo.

**Se lo skill aborisce con "CSpect in esecuzione":** chiudi l'emulatore, attendi 2-3 secondi,
poi rilancialo.

## Argomenti opzionali

- `dry` -- solo anteprima (dry-run), nessuna copia, nessun mount/smount automatico
- `blocks` -- include anche `!Blocks-64.bin` (di default escluso: sovrascriverlo
  distrugge gli Screen editati dentro CSpect)
- `mirror` -- cancella su W: i file assenti nella sorgente; chiedi conferma esplicita
  all'utente PRIMA di usarlo, mostrando i file che verrebbero eliminati (dry-run)

## Procedura

1. **VERIFICA CRITICA: CSpect deve essere CHIUSO** (`Get-Process -Name 'CSpect*'`).
   L'immagine SD rimane LOCKED finche' CSpect è attivo.
   Se CSpect è in esecuzione:
   - FERMATI immediatamente
   - Comunica all'utente: **"CSpect deve essere chiuso prima di sincronizzare"**
   - Exit code 2
   (Gli script sync2sd.ps1 e mountw.ps1 fanno questo controllo all'inizio.)

2. **Ricorda lo stato iniziale di W:** -- `$wasMounted = Test-Path 'W:\'`.
   Regola: lo stato trovato va ripristinato. Se W: era gia' montata, alla fine
   va lasciata montata; se la monti tu, alla fine va smontata.

3. **Mount se serve**: se W: non e' montata, avvisa l'utente che comparira' il
   popup UAC, poi:
   ```powershell
   & C:\zx\forth\F18\tools\vForth\util\mountw.ps1
   ```
   Exit 0 = ok; 1 = errore/UAC negato; 2 = CSpect attivo. Se fallisce, fermati.

4. **Sync**:
   ```powershell
   & C:\zx\forth\F18\tools\vForth\util\sync2sd.ps1
   ```
   Aggiungi `-WithBlocks` se richiesto `blocks`, `-Mirror` se confermato `mirror`,
   `-DryRun` se richiesto `dry` (in tal caso salta i passi 5-6).
   L'output robocopy puo' essere lungo: riporta all'utente solo il riepilogo
   (file copiati/ignorati/extra) e le eventuali anomalie.

5. **Verifica**:
   ```powershell
   & C:\zx\forth\F18\tools\vForth\util\verify2sd.ps1
   ```
   Stessi switch `-WithBlocks` del sync. Exit 0 = allineato. Se restano differenze
   subito dopo il sync, qualcosa non va: indaga, non rilanciare alla cieca.

6. **Smount solo se l'hai montata tu** (`-not $wasMounted`), con avviso UAC:
   ```powershell
   & C:\zx\forth\F18\tools\vForth\util\mountw.ps1 -Dismount
   ```
   Se lo smount fallisce per file aperti, suggerisci `imdisk -D -m w:` ma non
   eseguirlo senza conferma.

7. **Riepilogo finale**: quanti file copiati, esito verifica, stato di W:
   (montata/smontata). Se W: e' rimasta montata, ricorda che va smontata
   (`util\mountw.ps1 -Dismount`) prima di avviare CSpect.
