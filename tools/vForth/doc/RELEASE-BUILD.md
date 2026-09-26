# Rilascio di una nuova build -- attivita' manuali

Promemoria di cio' che l'autore deve preparare **a mano** prima di far girare lo
skill `/release-rebuild YYYYMMDD`, che orchestra tutto il resto (gate sulla
documentazione, `/bump-build`, dump testuale dei blocchi, `/sync-cspect`,
`new-build.bat`, voce in `HISTORY.txt` del repo pubblico).

Nel seguito `YYYYMMDD` e' la data della nuova build (es. `20260817`) e
`YYYY-MM-DD` la sua forma con trattini. `PFX` e' il prefisso dei manuali, oggi
`vForth1.8-core-en-`.

Questo elenco vale per un rilascio **a parita' di sorgente core**. Se invece il
core cambia davvero (indirizzi, struttura del dizionario), va aggiunto un giro di
`/regen-doc-dict-structure` e il paragrafo 3.20 del manuale va riscritto: vedi
`.claude/skills/regen-doc-dict-structure/SKILL.md`.


## 1. Manuale .odt con la data nuova

Copia l'`.odt` piu' recente in `doc/PFX-YYYYMMDD.odt` e sostituisci la data
interna. **Non basta rinominare il file**: il gate dello skill estrae
`content.xml` dall'.odt e blocca se trova ancora la data della build precedente,
o se non trova quella nuova.

La data di build compare **piu' di una volta** nel testo (2 occorrenze nei
campioni recenti): vanno sostituite tutte, non solo quella di copertina.


## 2. Manuale .pdf esportato

Esporta `doc/PFX-YYYYMMDD.pdf` dall'.odt appena corretto, via menu *Stampa* ->
stampante virtuale **PDF File**.

Controlla che il file non sia di **0 byte**: se la stampa non e' andata a termine
resta un guscio vuoto che sembra presente ma non contiene nulla; il gate lo
scarta (`pdftotext` riporta "Document stream is empty").

Solo il `.pdf` viene pubblicato: l'`.odt` resta privato.


## 3. Cartella di archivio storico version/YYYYMMDD/

`new-build.bat` esige che `version/YYYYMMDD/` esista. Se manca:

    & C:\zx\forth\F18\tools\vForth\version\new-version.bat YYYYMMDD

Il **riempimento** della cartella e' archivio storico curato a mano: non e'
automatizzato per scelta. Allo script basta che la cartella ci sia.


## 4. Data di build nel BLOCK 1 e Screen editati in CSpect

La data nel primo blocco di `!Blocks-64.bin` non va piu' toccata a mano: la
aggiorna `/bump-build` (lanciato da `/release-rebuild` prima del dump dei
blocchi), e all'occorrenza la si corregge direttamente da VS Code con
l'estensione vForth.

Resta valido un solo accorgimento: `/sync-cspect` copia sempre e solo
**PC -> SD** ed esclude `!Blocks-64.bin`. Se nell'emulatore sono stati editati
Screen che devono entrare nel rilascio, chiudi CSpect e ricopia il file da SD a
PC **prima** di lanciare lo skill:

    & C:\zx\forth\F18\tools\vForth\util\mountw.ps1
    Copy-Item 'W:\tools\vForth\!Blocks-64.bin' 'C:\zx\forth\F18\tools\vForth\!Blocks-64.bin' -Force
    & C:\zx\forth\F18\tools\vForth\util\mountw.ps1 -Dismount

E' l'unico trasferimento del progetto che va nella direzione **SD -> PC**.


## 5. Chiudere tutto prima di lanciare lo skill

- **LibreOffice**, se ha ancora aperto l'`.odt`: il lock impedisce al gate di
  leggerne il `content.xml` ("il processo non puo' accedere al file").
- **CSpect e MAME**: tengono un lock esclusivo sull'immagine SD, e senza di essa
  smontabile il sync si ferma. Lo skill fa comunque montare e smontare `W:`, con
  due popup UAC da confermare.


## 6. Materiale per HISTORY.txt

La voce in `HISTORY.txt` del repo pubblico la accoda lo skill, ma il **testo**
delle novita' e' tuo: preparalo (poche righe, ~80 colonne, ASCII). Per un
rilascio a sorgente core invariato conviene dirlo esplicitamente.

**Non editare `HISTORY.txt` mentre lo skill sta lavorando:** un editing
concorrente ha gia' fatto sparire un append (2026-07-14).


## 7. Lanciare lo skill

    /release-rebuild YYYYMMDD


## 8. Commit finali

Da fare a mano (GitHub Desktop) su **due** repo distinti:

- il repo di lavoro `F18`;
- il repo pubblico `c:\Zx\GitHub\vforth-next`.
