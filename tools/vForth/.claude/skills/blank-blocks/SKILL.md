---
name: blank-blocks
description: Riempie di BLANK (0x20, come la parola Forth BLANK = BL FILL) uno o piu' intervalli di Screen/BLOCK in !Blocks-64.bin, preservando la dimensione del file. Screen N corrisponde a BLOCK 2N e 2N+1. Include il preset "persistence" per gli intervalli usati da lib/PERSISTENCE.f (32000-32040, 32048-32175, 32200-32240, 32248-32375). Usare quando l'utente chiede di ripulire/azzerare uno o piu' Screen o BLOCK nel file dei blocchi, o quando chiede /blank-blocks.
---

# blank-blocks: ripulisce Screen/BLOCK in !Blocks-64.bin

Riempie i BLOCK richiesti con lo spazio (`0x20`), cioe' lo stesso riempimento
della parola Forth `BLANK ( a n -- )` (`inc/doc/blank.f`: `BL FILL`) usata
dall'editor di blocchi -- **non** azzeramento a `0x00`. La dimensione del
file non cambia mai (16 MB = 32768 BLOCK).

## ⚠️ Operazione distruttiva -- conferma prima di eseguire

Sovrascrive contenuto reale (Screen utente, dati di persistenza). Prima di
lanciare lo script, riepiloga all'utente ESATTAMENTE quali Screen/BLOCK
verranno azzerati e attendi conferma esplicita, a meno che l'utente non li
abbia gia' indicati in modo inequivocabile nella richiesta.

Mitigazione: `!Blocks-64.bin` e' **tracciato in git** (verificare con
`git ls-files | grep -i "Blocks-64.bin"` -- deve comparire il file in radice,
non le copie storiche sotto `version/`/`doc/`), quindi l'operazione e'
recuperabile con `git diff -- "!Blocks-64.bin"` / `git checkout --
"!Blocks-64.bin"` finche' non viene committata. Non fare mai il commit
automaticamente: lascialo decidere all'utente dopo aver verificato il
risultato.

## ⚠️ Prerequisito: CSpect e MAME chiusi

Come nello skill sync-cspect, se CSpect o MAME hanno il file (o l'immagine SD
che lo contiene) aperto, la scrittura puo' fallire per lock o essere
sovrascritta al successivo save dell'emulatore. Verificare che nessuno dei
due sia in esecuzione prima di procedere.

## Conversione Screen -> BLOCK

Screen N occupa **BLOCK 2N e 2N+1**. Un intervallo di Screen [S1, S2]
corrisponde quindi a BLOCK [2*S1, 2*S2+1]:

```
Screen 12 .. 98  ->  BLOCK 24 .. 197
```

**Il numero di BLOCK e' 1-based sul file.** Confermato nel core
(`project/vForth18_DOES/source/L3.asm`, parola `R/W`: fa `1-` sul numero di
blocco prima di chiamare `BLK-SEEK`, che poi calcola `n * B/BUF`): BLOCK n
vive a byte-offset **`(n-1)*512`**, non `n*512`. BLOCK 1 sono quindi i primi
512 byte del file (coerente con la nota di CLAUDE.md: "The first 512 bytes
of !Blocks.txt are BLOCK 1"). `util/blank-blocks.ps1` applica gia' questa
formula -- non riscriverla altrove con `n*512`, e' un bug gia' commesso una
volta (Screen successivo intaccato, primo BLOCK dell'intervallo mancato).

## Preset "persistence"

Gli intervalli usati da `lib/PERSISTENCE.f` (vedi commento in testa al file
e parola `PERSISTENCE`/`CLEAR-BLOCKS`), variante normale e dot-command:

| Intervallo BLOCK | Contenuto |
|---|---|
| 32000-32040 | User data (32000) + Core data (32001-32040), variante normale |
| 32048-32175 | Heap data, variante normale |
| 32200-32240 | User data (32200) + Core data (32201-32240), variante dot |
| 32248-32375 | Heap data, variante dot |

## Procedura

1. **Calcolare** gli intervalli BLOCK richiesti (Screen->BLOCK come sopra;
   il preset persistence e' gia' in BLOCK).
2. **Verificare git status pulito** su `!Blocks-64.bin` prima di iniziare
   (`git status -- "!Blocks-64.bin"`), cosi' un eventuale `git diff` dopo
   riflette solo questa operazione.
3. **Controllo preliminare (obbligatorio, non scrive nulla)**: eseguire lo
   script con `-CheckOnly` PRIMA di qualunque scrittura, per sapere quali
   BLOCK tra quelli richiesti sono gia' blank e quali contengono dati reali
   che verrebbero distrutti:
   ```powershell
   powershell -File util/blank-blocks.ps1 -File "!Blocks-64.bin" -Ranges "24-197,32000-32040,32048-32175,32200-32240,32248-32375" -CheckOnly
   ```
   Un BLOCK conta come "gia' blank" se ogni byte e' `0x20` (spazio) **o**
   `0x00` (NUL) -- e' ammissibile che ci siano caratteri `0x00` inerti
   mescolati tra gli spazi, non invalida il fatto che il BLOCK sia blank.
   Riportare all'utente l'elenco dei BLOCK NON gia' blank (se presenti)
   prima di procedere: sono quelli che l'operazione modifichera' davvero.
4. **Eseguire la scrittura**, stessi intervalli in un colpo solo (uno
   script singolo, non uno per intervallo), senza `-CheckOnly`, da
   `tools/vForth/` (lo script ristampa comunque il pre-check come log,
   poi scrive):
   ```powershell
   powershell -File util/blank-blocks.ps1 -File "!Blocks-64.bin" -Ranges "24-197,32000-32040,32048-32175,32200-32240,32248-32375"
   ```
   (adattare il primo intervallo se l'utente chiede uno Screen range diverso;
   omettere gli intervalli persistence se l'utente non li ha richiesti). Lo
   script e' PowerShell nativo (`[System.IO.File]`) apposta: **non usare
   python3** per questa operazione -- in questo ambiente non e' installato
   (solo lo stub Windows Store che fallisce).
5. **Verificare**:
   - Dimensione file invariata: `ls -la "!Blocks-64.bin"` deve mostrare
     ancora 16777216 byte.
   - Un campione dei BLOCK toccati e' tutto spazi: ad es. per BLOCK 24
     (BLOCK 1-based, offset `(n-1)*512` -- vedi sopra),
     ```powershell
     $fs=[System.IO.File]::OpenRead("!Blocks-64.bin"); $fs.Seek((24-1)*512,'Begin')|Out-Null
     $buf=New-Object byte[] 512; $fs.Read($buf,0,512)|Out-Null; $fs.Close()
     ($buf | Sort-Object -Unique)
     ```
     deve stampare solo `32` (0x20 decimale).
   - Ripetere lo `-CheckOnly` del passo 3: ora deve riportare 0 BLOCK non
     blank sull'intero intervallo.
   - `git diff --stat -- "!Blocks-64.bin"` per confermare che solo questo
     file e' cambiato.
6. **Non committare** automaticamente: riportare all'utente l'esito e
   lasciare a lui la decisione di commit (l'utente committa tramite GitHub
   Desktop, non da CLI).

## Nota implementativa

`util/blank-blocks.ps1` e' generico: accetta `-Ranges` come lista di
intervalli `start-end` separati da virgola e riempie ciascun BLOCK con
`0x20`, verificando prima che il file sia abbastanza grande per il BLOCK
massimo richiesto. Non serve modificarlo per richieste future con
intervalli diversi -- basta ricalcolare gli intervalli e richiamarlo.
