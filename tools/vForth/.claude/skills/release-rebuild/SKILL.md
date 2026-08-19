---
name: release-rebuild
description: Pipeline completa di rilascio vForth a parita' di sorgente core, per timbrare una nuova build (es. introduzione di nuove librerie come LAYER22). Accetta YYYYMMDD. PRIMA di iniziare, avvisa l'utente che doc/<PFX>YYYYMMDD.odt e .pdf devono gia' esistere (preparati a mano): se mancano, lo skill si ferma al gate del passo 1 (verifica esistenza E che contengano la data nuova ma NON quella precedente, .odt via content.xml, .pdf via pdftotext), piu' il gate di igiene dell'.odt via util/odt-hygiene.py (blocca se il manuale trascina i segnalibri Word residui _Toc/_Hlk; il --fix lo lancia l'utente). Poi bump-build (compila DOES+DOT + aggiorna i riferimenti data), genera automaticamente il dump !Blocks txt via perl blocks2txt.pl, sync (sync-cspect sull'immagine CSpect), rilascio pubblico (new-version/new-build.bat) e aggiornamento di HISTORY.txt nel repo pubblico (entry separate da due righe vuote). NON tocca mai .odt/.pdf. Usare quando l'utente chiede /release-rebuild o un rilascio completo a binario sostanzialmente invariato.
---

# release-rebuild: pipeline completa di rilascio vForth

Orchestratore per pubblicare una **nuova build** quando il **sorgente core non
cambia** (o cambia in modo irrilevante): lo scopo e' distinguere il rilascio dal
precedente perche' si introducono novita' a contorno -- p.es. nuove librerie come
**LAYER22**. Poiche' la struttura del binario non cambia, **non** servono le
verifiche su indirizzi/SEE/DUMP del manuale (`regen-doc-dict-structure` NON va
lanciato).

**Argomento obbligatorio:** la data nel formato `YYYYMMDD` (es. `20260704`).
Da essa si deriva la forma con trattini `YYYY-MM-DD`. Lavorare da `tools/vForth/`.

> **Regola ferrea sul manuale:** lo skill **non modifica MAI** i file `.odt`/`.pdf`.
> La documentazione la prepara l'utente a mano (vedi gate). Lo skill si limita a
> **verificare che esista** la documentazione con la nuova data, e a fermarsi se
> manca.

> ⚠️ **AVVISO PRELIMINARE da dare all'utente prima di iniziare qualunque lavoro:**
> `doc/<PFX>YYYYMMDD.odt` e `doc/<PFX>YYYYMMDD.pdf` devono esistere **gia'** (con
> la data interna corretta, non solo rinominati) prima di invocare questo skill.
> Sono l'unica parte che l'utente prepara a mano e lo skill non puo' generarli.
> Se l'utente chiede /release-rebuild senza aver ancora preparato questi due
> file, digliele subito -- non aspettare di scoprirlo al gate del passo 1.

## 0. Validazione argomento

- Deve essere `YYYYMMDD` (8 cifre). Se assente o malformato -> ferma e chiedi la data.
- Deriva `DASH = YYYY-MM-DD`.
- Determina il prefisso e la **data vecchia** dai file `doc/vForth*-core-en-*.odt`:
  ricava il prefisso `PFX` (es. `vForth1.8-core-en-`) e `OLD` = la data piu' alta
  **strettamente minore** di `YYYYMMDD` (cioe' la build precedente; escludi il
  nuovo file se gia' presente). `OLD_DASH = forma trattini di OLD`. La condizione
  "esiste un file con la data precedente" e' proprio cio' su cui si fonda il gate
  contenuto del passo 1: se non si trova un `OLD` valido, fermati e segnalalo.

## 1. GATE iniziale -- prima di QUALUNQUE altra operazione (hard stop)

Questo passo precede compilazione, sync e copie. Se anche **una** condizione
fallisce: **fermati**, elenca cosa manca, ricorda all'utente la sua parte
manuale, e **non procedere oltre**.

Verifica l'esistenza dei **due** artefatti manuali per la nuova build (l'unica
parte che l'utente prepara a mano e' la documentazione):

1. `doc/<PFX>YYYYMMDD.odt`  -- manuale (copia dell'.odt precedente con la sola
   data interna aggiornata da `OLD_DASH` a `DASH`; replace a parita' di lunghezza).
2. `doc/<PFX>YYYYMMDD.pdf`  -- esportato dall'.odt via menu *Stampa* -> stampante
   virtuale **PDF File** (procedura dell'utente).

> Il dump `doc/txt/!Blocks-64.bin_YYYYMMDD.txt` **non** e' un prerequisito di gate:
> lo genera automaticamente lo skill al passo 2b (dopo bump-build, che aggiorna la
> data nel primo blocco di `!Blocks-64.bin`).

### 1b. Verifica CONTENUTO (bloccante) -- rete contro l'errore umano

Esistere non basta: i due file potrebbero essere stati solo **rinominati** senza
correggere la data **interna**. Quindi, dopo l'esistenza, verifica il contenuto e
**blocca** se non quadra. Il riferimento di cosa cercare e' la data della build
**precedente** `OLD_DASH`, dedotta dall'esistenza del file con timestamp anteriore
(passo 0).

Per ciascun artefatto, due condizioni bloccanti:
- **NON** deve contenere `OLD_DASH` (la data vecchia: segno di rinomina senza edit).
- **DEVE** contenere `DASH` (la data nuova: prova che la correzione c'e' stata).

Da dove si legge il testo:
- `.odt`: e' uno zip; il testo visibile sta in `content.xml`. (Non usare
  `meta.xml`: le sue date dc:date/print-date vengono riscritte al salvataggio e
  non coincidono con la data di build -> falsi positivi.)
- `.pdf`: il testo visibile e' in stream compressi, **non** nei byte grezzi;
  estrailo con **`pdftotext`** (poppler) e cerca nel testo estratto.

```powershell
$ver     = "20260704"             # = argomento YYYYMMDD
$dash    = "2026-07-04"           # = DASH
$old_dash= "2026-06-14"           # = OLD_DASH (build precedente, dal passo 0)
$pfx     = "vForth1.8-core-en-"   # = PFX rilevato
$base    = "C:\zx\forth\F18\tools\vForth"
$pdftotext = "C:\Users\matteo\Downloads\Install\poppler-26.02.0\Library\bin\pdftotext.exe"
$odt = "$base\doc\$pfx$ver.odt"; $pdf = "$base\doc\$pfx$ver.pdf"

# --- esistenza ---
$missing = @($odt,$pdf) | Where-Object { -not (Test-Path $_) }
if ($missing) {
  "GATE FALLITO -- manca la documentazione:"; $missing | ForEach-Object { "  MANCA: $_" }
  "`nPreparala a mano, poi rilancia /release-rebuild $ver :"
  "  1. Copia l'.odt piu' recente in doc\$pfx$ver.odt e sostituisci la data interna ($dash)."
  "  2. Esporta il .pdf (Stampa -> stampante 'PDF File') come doc\$pfx$ver.pdf."
  exit 1
}

$fail = @()
# --- contenuto .odt (content.xml) ---
$tmp = "$env:TEMP\rr_odt"; if (Test-Path $tmp) { Remove-Item $tmp -Recurse -Force }
Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::ExtractToDirectory($odt,$tmp)
$cx = Get-Content "$tmp\content.xml" -Raw -Encoding UTF8
if ($cx -match [regex]::Escape($old_dash)) { $fail += ".odt contiene ANCORA la data vecchia $old_dash (rinominato senza correggere la data interna)" }
if ($cx -notmatch [regex]::Escape($dash))  { $fail += ".odt NON contiene la data nuova $dash" }

# --- contenuto .pdf (pdftotext) ---
$txt = & $pdftotext $pdf -    # '-' = stdout
$ptxt = ($txt -join "`n")
if ($ptxt -match [regex]::Escape($old_dash)) { $fail += ".pdf contiene ANCORA la data vecchia $old_dash (riesportare dall'.odt corretto)" }
if ($ptxt -notmatch [regex]::Escape($dash))  { $fail += ".pdf NON contiene la data nuova $dash" }

if ($fail) {
  "GATE CONTENUTO FALLITO:"; $fail | ForEach-Object { "  X $_" }
  "`nCorreggi la data INTERNA di .odt/.pdf (non basta rinominare), poi rilancia."
  exit 1
}
"GATE OK -- esistenza + contenuto verificati (data nuova $dash presente, vecchia $old_dash assente)"
```

(Adatta `$ver`/`$dash`/`$old_dash`/`$pfx` ai valori reali del run. Se `pdftotext`
non e' al percorso indicato, cercalo in PATH: `Get-Command pdftotext`.)

### 1c. Igiene dell'.odt (bloccante) -- segnalibri Word residui

Il manuale di ogni build nasce come **copia** di quello della build precedente,
quindi la zavorra si eredita all'infinito se nessuno la ferma. Il residuo tipico
sono i segnalibri `_Toc*`/`_Hlk*` che Word posa a ogni "aggiorna sommario" e non
rimuove mai: nel manuale `20260817` erano 18617, in 18 generazioni sovrapposte,
pari al 30% di `content.xml`. Sono invisibili in pagina e rallentano solo
apertura e salvataggio (ripulendoli, un ordine di grandezza guadagnato).

`util/odt-hygiene.py` in sola lettura: esce 0 se pulito, **1 se c'e' residuo**.

```powershell
$python = "C:\Users\matteo\AppData\Local\Python\pythoncore-3.14-64\python.exe"
& $python "$base\util\odt-hygiene.py" $odt
if ($LASTEXITCODE -ne 0) {
  "GATE IGIENE FALLITO -- l'.odt trascina segnalibri Word residui."
  "Ripulisci (in place, con validazione e .bak) e poi rilancia:"
  "  & `"$python`" util\odt-hygiene.py --fix doc\$pfx$ver.odt"
  exit 1
}
"IGIENE OK -- nessun segnalibro Word residuo"
```

> **Il --fix lo lancia l'utente, non lo skill.** Vale la regola ferrea: lo skill
> non modifica mai l'.odt. Qui si limita a misurare e a fermarsi.
>
> Dopo un `--fix` **il `.pdf` NON va riesportato**: la rimozione non tocca il
> testo visibile (lo script lo verifica byte per byte) ne' l'impaginazione, e il
> gate contenuto del passo 1b resta soddisfatto. Il `.pdf` gia' esportato e'
> ancora valido.

Nel report compare anche il conteggio degli `<text:span>` ridondanti
(`Default_20_Paragraph_20_Font`, altro residuo dell'import da Word, ~1 MB):
e' **informativo e non bloccante** -- rimuoverli tocca la formattazione e non
e' un intervento da fare dentro un rilascio.

## 2. bump-build YYYYMMDD (compila DOES + DOT, aggiorna i riferimenti)

Invoca lo skill **`/bump-build YYYYMMDD`**. Aggiorna i punti canonici della data
(SPLASH DOES/DOT, header dei due `main.asm`, `src/F18e.f`, `CLAUDE.md`, primo
blocco di `!Blocks-64.bin`, i due `.bas`), **ricompila entrambe le varianti** e
copia i binari in radice (`forth18e.bin`, `ram8.bin`) e il dot-command in `dot/`.
Vedi `.claude/skills/bump-build/SKILL.md` per i dettagli -- non duplicarli qui.

Verifica rapida a fine bump (gia' parte di bump-build): nessuna data vecchia
residua nei punti canonici; la nuova data e' nei binari.

## 2b. Genera il dump testuale dei blocchi (automatico)

Va **dopo** il bump: bump-build ha appena aggiornato la stringa `build YYYY-MM-DD`
nel primo blocco di `!Blocks-64.bin`, e il dump ne riporta l'header -- quindi
deve riflettere la data nuova. Replica meccanicamente cio' che l'utente fa con
`util\blk2txt.bat` (`perl blocks2txt.pl`), ma scrive direttamente il file datato
in `doc/txt/` (l'arg `16383` = numero massimo di Screen, come nel .bat):

```powershell
$ver  = "20260704"                       # = YYYYMMDD
$base = "C:\zx\forth\F18\tools\vForth"
& perl "$base\util\blocks2txt.pl" "$base\!Blocks-64.bin" 16383
# blocks2txt.pl scrive accanto al sorgente: <file>.txt
Copy-Item "$base\!Blocks-64.bin.txt" "$base\doc\txt\!Blocks-64.bin_$ver.txt" -Force
Remove-Item "$base\!Blocks-64.bin.txt" -Force   # come il 'move' del .bat: non lasciarlo in radice
if (Test-Path "$base\doc\txt\!Blocks-64.bin_$ver.txt") { "dump OK -> doc\txt\!Blocks-64.bin_$ver.txt" } else { "ERRORE: dump non creato"; exit 1 }
```

Prerequisiti: `perl` in PATH (Strawberry: `C:\Strawberry\perl\bin\perl.exe`) e
`!Blocks-64.bin` presente in radice. Questo `.txt` serve a `new-build.bat`
(passo 4, copia in SD e zip).

## 3. Sync

**`/sync-cspect`** -- deploy sull'immagine SD di CSpect (`W:\tools\vForth` <-
`cspect-next-2gb.img`). Sincronizza anche le nuove librerie (es.
`lib/LAYER22-GRAPHICS.f`).
**Prerequisito critico: CSpect deve essere CHIUSO** (lock esclusivo
sull'immagine). Se e' aperto, lo skill sync-cspect si ferma: avvisa l'utente,
non forzare. Comporta due popup UAC (mount/dismount di `W:`).

> Nota: **non** usare `/sd-sync` qui. In questo repo non esiste (ne' esistera')
> una cartella di staging `SD/`: l'unica sync verso l'ambiente di test e'
> `/sync-cspect`.

## 4. Rilascio pubblico (i .bat)

Repo pubblico: `c:\Zx\GitHub\vforth-next`. I `.bat` stanno in
`tools\vForth\version\`. **Gotcha sandbox:** con
`NoDefaultCurrentDirectoryInExePath=1` i `.bat` vanno invocati con path assoluto
(un `call nome.bat` nudo fallisce qui).

1. **Alberatura archivio storico** -- `new-build.bat` esige che esista
   `version\YYYYMMDD\`. Se manca, creala con:
   ```powershell
   & C:\zx\forth\F18\tools\vForth\version\new-version.bat YYYYMMDD
   ```
   Il **riempimento** di `version\YYYYMMDD\` e' archivio storico che l'utente cura
   **a mano**: non automatizzarlo (scelta dell'utente). A `new-build.bat` basta
   che la cartella esista.

2. **Copia + zip pubblico**:
   ```powershell
   & C:\zx\forth\F18\tools\vForth\version\new-build.bat YYYYMMDD
   ```
   Copia selettiva verso `vforth-next\SD\tools\vForth` e la radice, copia `dot\*`,
   pulisce la SD (zip leggero: `doc\previous` svuotata, un solo `!Blocks` txt =
   quello della build), crea `download\vForth_18_NextZXOS_YYYYMMDD.zip`, aggiorna
   i project pubblici `MMU7_DOT` / `DIRECT_MMU7`. Usa
   `doc\txt\!Blocks-64.bin_YYYYMMDD.txt` (verificato al gate).
   Due messaggi `Nome duplicato o impossibile trovare il file` durante "Moving
   older docs to previous" sono **benigni**: il `move` cerca anche pattern non
   presenti sulla SD (es. il `.odt`, che resta privato -- si pubblica solo il
   `.pdf`).

3. **Aggiorna `HISTORY.txt` del repo pubblico** (`c:\Zx\GitHub\vforth-next\HISTORY.txt`).
   `new-build.bat` **non** lo tocca: va accodato a mano la voce di questo build,
   rispettando la formattazione del file. Convenzioni: **LF (Unix)** -- il blob
   in `HEAD` e' salvato a soli LF, anche se il working tree del clone locale
   puo' apparire in CRLF per conto suo (vecchio checkout, `core.autocrlf`
   pregresso: irrilevante, cio' che conta e' non introdurre CR nuovi) -- solo
   ASCII 7-bit, entry separate da **due righe vuote** (non una -- confermato
   dall'utente 2026-07-14), header `\ build YYYYMMDD` seguito da testo libero
   (poche righe ~80 col). Per un rilascio a sorgente invariato conviene dire
   esplicitamente che il core-binary non cambia (come la entry `20260419`).

   > ⚠️ **NON usare `` `r`n `` (CRLF) come separatore di riga, MAI.** Il file e'
   > Unix (LF). Un append con `` $nl="`r`n" `` scrive correttamente le righe
   > nuove ma, unito al fatto che .NET `AppendAllText` non tocca i byte
   > preesistenti, lascia il file con newline **miste**: le righe vecchie
   > restano LF, quelle nuove sono CRLF. Se poi qualcosa (editor, un comando
   > successivo) normalizza l'intero file su quel CRLF "vincente", l'intero
   > file passa a DOS -- il tipo di modifica silenziosa e diffusa che si nota
   > solo con `file HISTORY.txt` (dice `CRLF line terminators` quando non
   > dovrebbe) o con un diff a sorpresa enorme (vedi sotto). Capitato e
   > corretto il 2026-08-01: causa era `$nl="`r`n"` nello script di questo
   > stesso passo. Usa **sempre** `$nl="`n"`.

   Esempio di append (preserva LF/ASCII, non sovrascrive):
   ```powershell
   $f='C:\Zx\GitHub\vforth-next\HISTORY.txt'; $nl="`n"
   $lines=@('', '', '\ build YYYYMMDD', '<riga 1 delle novita''>', '<riga 2>', '...')
   [System.IO.File]::AppendAllText($f, ($lines -join $nl)+$nl, [System.Text.Encoding]::ASCII)
   ```
   Le novita' descrivono cosa cambia in QUESTO build (es. la famiglia
   `LAYERxx-GRAPHICS` e il nuovo `LAYER22`).

   **Verifica sempre con `git diff -- HISTORY.txt` subito dopo l'append.**
   Due possibili cause, entrambe da escludere prima di considerare l'append
   riuscito:
   - **Editing concorrente dell'utente.** Il 2026-07-14 un append e' apparso
     scritto correttamente (verificato con `tail`), ma un secondo controllo
     poco dopo mostrava la voce sparita e righe vuote raddoppiate in punti
     vecchi del file -- causato dall'utente che stava editando HISTORY.txt in
     parallelo (sua "cleansing" di righe precedenti), non da un bug dello
     script.
   - **Mismatch di line-ending (CRLF vs LF).** Se il diff mostra l'INTERO file
     come cambiato (non solo le righe nuove in coda), prima di allarmarsi
     verifica se e' solo un problema di `\r`: confronta le versioni
     normalizzate, `git show HEAD:HISTORY.txt | tr -d '\r'` contro
     `cat HISTORY.txt | tr -d '\r'` (o l'equivalente PowerShell). Se il diff
     normalizzato mostra ESATTAMENTE le righe nuove attese, il contenuto e'
     giusto ma il file ha newline miste/sbagliate: **non lasciarlo cosi'**,
     fai ripristinare il file all'utente (`git checkout -- HISTORY.txt` /
     discard) e ripeti l'append con `$nl="`n"`.

   In ogni caso, se il diff dopo l'append non mostra ESATTAMENTE le righe
   attese (nient'altro sopra o sotto, stesso line-ending del resto del file),
   non fidarsi e ricontrollare con `Read`/`git diff` prima di andare avanti.

## 5. Riepilogo finale

Riferisci: data build, esito gate, esito bump (binari ricompilati/copiati),
esito sync (file copiati, eventuali `PROTETTO`/`TS-FIX`, stato di W:), esito
rilascio (zip creato, project copiati) e voce aggiunta a `HISTORY.txt`.
Commit/push **solo se l'utente lo chiede** (l'utente committa via GitHub
Desktop, non da CLI): ricorda che i commit da fare sono **due** -- il repo di
lavoro `F18` e il repo pubblico `vforth-next`.
