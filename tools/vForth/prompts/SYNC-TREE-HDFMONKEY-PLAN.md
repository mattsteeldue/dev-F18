# Piano: sync/verify massivo dell'albero vForth via hdfmonkey (estensione VS Code)

Destinatario: team di manutenzione di `vscode-vforth`
(<https://github.com/mattsteeldue/vscode-vforth>, locale `C:\Zx\GitHub\vscode-vforth\`).
Data: 2026-09-19. Origine: progetto vForth (`tools/vForth`).

## 1. Obiettivo

Portare nell'estensione la funzione oggi svolta da `/sync-cspect`
(`util/sync2sd.ps1` + `util/verify2sd.ps1`): allineare in blocco l'albero
vForth sull'immagine SD di CSpect e verificarne l'allineamento, **con CSpect
aperto e senza mount imdisk / UAC**, usando `hdfmonkey` come gia' fa
`vforth.pushToSD`.

Il canale W:/imdisk resta per chi lo vuole (richiede CSpect e MAME chiusi).
Il nuovo canale non lo sostituisce: lo affianca.

## 2. Perche' (fatti verificati il 2026-09-19)

- Il lock esclusivo su W: e' una proprieta' di imdisk/hdfm-gooey, non di CSpect:
  `hdfmonkey` scrive nella FAT dell'immagine direttamente e funziona a
  CSpect acceso (gia' documentato nel README dell'estensione).
- **`hdfmonkey ls` restituisce solo `<size>\t<nome>` (e `[DIR]\t<nome>`), senza
  timestamp. `hdfmonkey get` non preserva il timestamp** (il file locale
  riceve l'ora corrente). Conseguenza: sul canale hdfmonkey NON si puo'
  applicare la guardia storica "ts 1980 = file editato in CSpect, non
  sovrascrivere" ne' la normalizzazione "sfasamento HDFMonkey 2h". Il confronto
  e' solo per **contenuto** (dimensione, poi MD5). La sezione 4 sostituisce la
  guardia 1980 con un manifest.
- Il percorso sull'immagine non distingue maiuscole (`/tools/vForth` ==
  `/tools/vforth`).
- Da Git Bash i percorsi che iniziano con `/` vengono convertiti in percorsi
  Windows (`/tools` -> `C:/Program Files/Git/tools`) e `hdfmonkey` risponde
  "File / directory name is invalid". Da `execFile` di Node non succede; vale
  solo per chi prova a mano da Git Bash (usare PowerShell o
  `MSYS_NO_PATHCONV=1`).

## 3. Cosa deve fare la funzione

Due comandi nuovi, piu' un'estensione di `pushToSD`:

| Comando | Effetto |
|---|---|
| `vForth: Sync tree to SD image` | Confronta e spinge nuovi/diversi. Prima mostra il piano (contatori + lista) e chiede conferma. |
| `vForth: Verify tree against SD image` | Sola lettura: stesso confronto, nessuna scrittura. Ritorna il riepilogo. |
| `vForth: Push file to SD image` (esistente) | In piu': aggiorna il manifest (par. 4). |

Opzioni del sync (QuickPick o impostazioni): *dry run*, *include
`!Blocks-64.bin`* (default no, conferma esplicita, vedi 7), *mirror* (v2, vedi 9).

### Algoritmo

1. **Enumerazione locale** sotto `vforth.root`, applicando le esclusioni
   (par. 5). Percorso relativo `rel` con `/`.
2. **Enumerazione SD**: `hdfmonkey ls <img> <dir>` ricorsivo a partire da
   `sdDestPrefix`; una `ls` per directory, risultato in cache per la durata del
   comando. Distinguere le directory dal prefisso `[DIR]`.
3. **Classificazione** di ogni file locale:
   - assente sulla SD -> `NEW`;
   - dimensione diversa -> `DIFF`;
   - dimensione uguale -> `get` su file temporaneo e confronto MD5 con il
     locale: uguale -> `SAME`, altrimenti `DIFF`. (Ottimizzazione: nessun `get`
     se la dimensione differisce.)
4. **Per ogni `DIFF`** consultare il manifest (par. 4): `UPDATE` (sicuro) oppure
   `PROTECTED` (non toccare).
5. **Esecuzione** (solo dopo conferma, non in dry-run/verify):
   - creare con `mkdir` le directory mancanti, dal genitore al figlio;
   - `put` raggruppato **per directory di destinazione** (il comando accetta piu'
     sorgenti: `put <img> <src...> <destdir>`), per ridurre gli spawn;
   - dopo ogni `put`, `get` + MD5 del file appena scritto (verifica di
     scrittura) e aggiornamento del manifest.
6. **Report**: Output channel "vForth" + riepilogo (NEW / UPDATE / SAME /
   PROTECTED / SKIPPED / errori), con esito sintetico come exit-code
   (0 = allineato, 1 = differenze o errori) per il verify.
7. **dot-command**: la cartella locale `dot/` va nella **radice** `/dot` dell'immagine (non sotto `sdDestPrefix`),
   solo copia/aggiornamento dei file presenti in sorgente, mai cancellazione:
   `/dot` contiene anche i dot-command della distribuzione.

## 4. Sostituto della guardia 1980: manifest MD5

Problema: con la sola differenza di contenuto, un file `DIFF` puo' essere sia
"vecchio" (la SD e' indietro, si puo' spingere) sia "editato in CSpect" (la SD
e' avanti, spingere distrugge lavoro). Il timestamp non e' leggibile.

Soluzione: **manifest** delle ultime versioni spinte.

- Posizione: `context.storageUri` (o `globalStorageUri`) dell'estensione, MAI
  nel repo vForth. Un file JSON per immagine SD, chiave = `sdImage` + `sdDestPrefix`.
- Schema:
  ```json
  { "version": 1,
    "image": "C:\\Zx\\CSpect\\cspect-next-2gb.img",
    "prefix": "tools/vforth",
    "files": { "inc/2constant.f": { "md5": "...", "size": 147, "pushed": "2026-09-19T18:42:44Z" } } }
  ```
- Regola per un `DIFF` con `md5SD`:
  - `md5SD == manifest.md5` -> la SD non e' cambiata dall'ultimo push:
    **UPDATE** (sovrascrivi);
  - `md5SD != manifest.md5` oppure nessuna voce -> la SD e' stata modificata
    altrove (CSpect) o e' di origine ignota: **PROTECTED**, non sovrascrivere.
- `PROTECTED` non e' un errore: e' una scelta da fare. Per ciascuno offrire
  *Skip* / *Overwrite (PC wins)* / *Pull (SD wins)* -- il pull e' il
  `vforth.pullFromSD` gia' esistente -- / *Show diff* (`vscode.diff` tra il file
  locale e la copia scaricata in temporaneo).
- **Aggiornare il manifest in tutti i punti che scrivono o leggono la SD**:
  `pushToSD` (dopo il `put`), `pullFromSD` (dopo il `get`: md5 uguale al locale),
  sync massivo, e ogni "Overwrite"/"Pull" deciso dall'utente. Questo elimina
  i falsi allarmi che nascerebbero da push fatti con l'estensione.
- Dopo un `SAME` (contenuto identico) scrivere/aggiornare la voce: la SD e' nota.
- Bootstrap: al primo uso il manifest e' vuoto, quindi ogni `DIFF` e' `PROTECTED`
  e viene proposto file per file. Offrire *Overwrite all remaining* con conferma
  esplicita per chi e' certo che la SD sia indietro.
- I Screen/Block editati dall'estensione (`openScreen`/`openBlock`) NON
  passano dal manifest: il file dei Block e' escluso dal sync (par. 7).

## 5. Esclusioni (portare tale e quale da `util/sd-sync.config.ps1`)

- Directory di primo livello (`vforth.sdExcludeTopDirs`, gia' presente):
  `dev doc dot emu forum project prompts tools version`. `dot` e' escluso
  perche' va in `/dot` (par. 3.7).
- Nomi di directory esclusi ovunque (nuova impostazione
  `vforth.sdExcludeDirNames`): `.claude .git __pycache__ afx`.
- File esclusi ovunque (nuova impostazione `vforth.sdExcludeFiles`, glob):
  `CLAUDE.md TODO.md *.ps1 out.txt transcript.txt .gitattributes .gitignore
  *.pyc *.lnk !Blocks-64.bin_*.txt Thumbs.db desktop.ini`.
- `!Blocks-64.bin`: escluso, vedi 7.

I default coincidono con quelli attuali del progetto: nessuno deve
configurare nulla per ottenere lo stesso insieme di file di `sync2sd.ps1`.

## 6. Nomi dei file

- I nomi sul disco locale sono gia' quelli FAT-mappati (es. `^layer2.f`,
  `[']`.f -> attenzione al carattere `[`). Nessuna mappatura da fare.
- Verificare che `hdfmonkey` gestisca i nomi lunghi (LFN) e i caratteri `[ ] ^ $ & { } ~ !`
  in `put`/`get`/`ls`. `pushToSD` gia' spinge file come `^layer2.f`; il caso
  `[`...`]` non e' verificato.
- Confronto dei nomi sulla SD **case-insensitive**.
- `execFile` con array di argomenti (mai stringa di shell): niente escape.

## 7. `!Blocks-64.bin`

- Escluso dal sync di default (sovrascriverlo distrugge gli Screen editati in
  CSpect: e' la fonte piu' probabile di perdita dati).
- Se richiesto: conferma modale con testo esplicito, `PROTECTED` di default
  anche se `md5SD != manifest`, e mai senza aver mostrato la dimensione (16 777 216
  byte; deve restare invariata).
- Nota: i `get`/`put` di 16 MB da parte di `openScreen`/`openBlock` gia' pongono
  il problema della finestra di race documentato nel README; il sync massivo
  non lo aggrava se il file dei Block resta escluso.

## 8. Rischio di concorrenza (da validare prima di rilasciare)

Il sync massivo scrive per piu' tempo di un push singolo. Se CSpect scrive
sulla stessa FAT nello stesso istante (per esempio vForth che salva un Block,
o un `F_OPEN` in scrittura), la FAT puo' diventare incoerente.

Mitigazioni proposte:
- comandi eseguiti **in serie**, mai spawn paralleli di `hdfmonkey`;
- se `tasklist` mostra `CSpect*` in esecuzione, avvertire ("CSpect e' aperto: non
  usarlo (ne' salvare Block) mentre il sync e' in corso") e chiedere conferma;
- protocollo di validazione prima del rilascio (test d'accettazione 3 e 4).

## 9. Fuori scope della v1 (voci per la v2)

- **Mirror** (cancellare sulla SD i file assenti in locale): richiede `rm`,
  lista dei candidati e conferma esplicita, mai su `/dot`. Non necessario per
  il ciclo di lavoro; lasciarlo al canale W:.
- Sync bidirezionale automatico.
- Sincronizzazione dei timestamp (non leggibili, vedi 2).

## 10. Struttura del codice (coerente con l'architettura attuale)

Seguire la separazione gia' in uso: logica pura senza dipendenze da `vscode`,
adattatore sottile in `extension.js`.

- **`src/sdsync.js`** (nuovo, puro): enumerazione locale con esclusioni,
  parsing dell'output di `ls`, classificazione, gestione manifest, costruzione
  del piano. Il runner di `hdfmonkey` e' **iniettato** (`run(cmd, args) ->
  {stdout}`) cosi' i test usano un finto `hdfmonkey` su una directory temporanea.
- **`extension.js`**: registra i comandi, `withProgress`, Output channel,
  QuickPick per `PROTECTED`, `context.storageUri` per il manifest.
- **`package.json`**: comandi `vforth.syncTreeToSD` e `vforth.verifyTreeVsSD`;
  impostazioni `vforth.sdExcludeDirNames`, `vforth.sdExcludeFiles`.
- **`test/sdsync.js`**: test di logica pura (non c'e' un framework: stessa
  convenzione di `test/selftest.js` e `test/sweep.js`).
- **`README.md` / `CHANGELOG.md`**: nuova sezione "Sync tree", con la tabella
  "quale canale usare" del par. 11.

## 11. Quale canale usare (testo per il README)

| Situazione | Canale |
|---|---|
| Modifico un file e lo provo in CSpect | `Push file to SD image` |
| Modifico uno Screen | `Open Screen #` |
| Ho toccato molti file, CSpect e' aperto | `Sync tree to SD image` (nuovo) |
| Voglio solo controllare l'allineamento | `Verify tree against SD image` (nuovo) |
| Deploy completo con `-Mirror`, `!Blocks-64.bin`, `dot/`, protezione timestamp 1980 | `/sync-cspect` (imdisk, emulatori chiusi) |

## 12. Test d'accettazione

1. **Logica pura**: albero finto con file nuovi/uguali/diversi; manifest vuoto ->
   tutti i `DIFF` sono `PROTECTED`; manifest uguale a `md5SD` -> `UPDATE`.
2. **Esclusioni**: l'insieme locale coincide con quello di
   `util/sync2sd.ps1 -DryRun` (confronto dell'elenco file).
3. **Immagine reale, CSpect chiuso**: sync completo dopo un clone; poi
   `Verify` -> nessuna differenza; poi `util/verify2sd.ps1` (canale W:) -> nessuna
   differenza di contenuto (le differenze di timestamp di 2 h sono attese).
4. **Immagine reale, CSpect aperto e fermo al prompt `ok`**: sync completo, poi
   in CSpect `NEEDS` di una parola appena spinta e `INCLUDE test/CORE-TESTS.f`
   senza errori; nessun `REMOUNT`.
5. **Guardia**: modificare un file dentro CSpect (il ts diventa 1980), rilanciare
   il sync -> il file risulta `PROTECTED` e resta intatto.
6. **Nomi difficili**: `^layer2.f`, un nome con `[`, un nome lungo, `!` iniziale.
7. **Interruzione**: annullare a meta' (`CancellationToken`) -> il manifest
   contiene solo i file davvero scritti e verificati.
8. `hdfmonkey` assente o `sdImage` errato: messaggi gia' in uso, invariati.

## 13. Ricadute lato progetto vForth (a carico nostro, non del team)

- Riscrivere la skill `.claude/skills/sync-cspect/SKILL.md`: il prerequisito
  "CSpect e MAME chiusi" vale solo per la strada W:/imdisk; aggiungere la
  scelta del canale e rimandare all'estensione.
- `util/sd-sync.config.ps1`: nessun cambiamento necessario finche' lo script resta.
  Il guard su MAME resta per il solo canale W: (non e' stato verificato che MAME
  tolleri `hdfmonkey` in parallelo).
- CLAUDE.md: richiamare l'estensione nella sezione dei percorsi di build/deploy e
  aggiornare la memoria di lavoro (workflow di sync SD).
- Dopo un push con `hdfmonkey` i file hanno un timestamp sfasato di 2 h: se poi si
  usa il canale W:, la Fase 1 (robocopy per timestamp) ricopiera' i file non `.f`
  di sottocartella; per i `.f` interviene il `TS-FIX`. Atteso, innocuo.

## 14. Domande aperte per il team

1. `hdfmonkey ls` e' affidabile su directory con centinaia di file (`inc/` ne ha
   piu' di 256)? Verificare paginazione/limiti.
2. Il manifest per immagine va in `storageUri` (per workspace) o in
   `globalStorageUri` (condiviso tra workspace)? Consigliato `globalStorageUri`
   con chiave `sdImage`+`prefix`, perche' l'immagine e' una sola per tutti.
3. `put` con piu' sorgenti verso una directory: conferma del comportamento su
   nomi con caratteri speciali e su sovrascrittura (rimuove/riscrive la voce o
   fallisce?).
4. Un file cancellato in CSpect (non solo modificato) e' `NEW` per il sync: va
   bene ripristinarlo o deve risultare `PROTECTED`? Proposta: `NEW` sempre.
