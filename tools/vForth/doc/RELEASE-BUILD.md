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


## 4. Aggiornare il numero di build nel BLOCK #1 da dentro CSpect

Passo invisibile agli script -- va fatto a mano nell'emulatore, **prima** di
lanciare `/release-rebuild`, perche' lo skill genera il dump
`doc/txt/!Blocks-64.bin_YYYYMMDD.txt` dal file che trova sul PC.

Premessa: `/sync-cspect` copia sempre e solo **PC -> SD**, e per giunta esclude
`!Blocks-64.bin` (sovrascriverlo distruggerebbe gli Screen editati
nell'emulatore). Il file dei blocchi torna sul PC solo con la copia manuale del
punto 4.7 qui sotto.

La stringa da correggere e':

    \ v-Forth 1.8 - NextZXOS versione - build YYYY-MM-DD

Sta nei primi byte del file (offset 36), che sono l'inizio del **BLOCK 1**: il
file non contiene alcun BLOCK 0, ed e' proprio da qui che nasce la confusione di
questo passo. Lo Screen 0 sarebbe `BLOCK 0` + `BLOCK 1`, ma la sua prima meta'
non esiste su file -- CLAUDE.md la elenca infatti come "Screen 0.5". Nell'editor la
riga da correggere e' quindi la **riga 8**, non la riga 0.

1. **Sincronizza prima** l'immagine SD, cosi' CSpect vede le novita' di questa
   build: `/sync-cspect` (CSpect e MAME chiusi, due popup UAC).
2. Avvia CSpect e vForth.
3. **`EMPTY-BUFFERS` -- sempre, prima di qualunque altra cosa.** Scarta il
   contenuto dei buffer di blocco in RAM senza riversarlo su file. E'
   indispensabile qui piu' che altrove: lo Screen 0 comprende il BLOCK 1, che il
   sistema usa di continuo come buffer di linea per `INCLUDE`/`NEEDS`/`F_INCLUDE`,
   quindi e' facile che un buffer contenga una copia stantia o marcata `UPDATE`
   che finirebbe riscritta sopra la modifica appena fatta.
4. `NEEDS EDIT`, poi `1 LIST` per selezionare lo Screen #1 e infine `EDIT` e di 
   seguito dare la sequenza `[Edit] + B` per arretrare di uno Screen: non e' 
   possibile editare direttamente lo Screen #0.
   L'editor mostra 16 righe da 64 colonne: le righe 0-7 sono un teorico BLOCK 0 
   (che non esiste nel file) mentre le righe 8-15 il BLOCK 1.
5. Correggi la data nella riga 8, basandoti sull'indicatore di riga del pannello
   inferiore, in quanto il tentativo di visualizzazione del BLOCK 0 rende la
   schermata molto confusa per la presenza di caratteri 0x00, 
   esci dall'editor con `[Edit] + Q` e riversa con `FLUSH`.
6. Riapplica **`EMPTY-BUFFERS`** per evitare di avere il BLOCK 0 spurio.

   > **Perche' e' tricky:** questa e' l'area che il sistema considera non
   > modificabile -- il BLOCK 1 e' proprio scelto come buffer di linea di
   > `F_INCLUDE` perche' `EDIT` non lo tocca mai (vedi CLAUDE.md, "Blocks,
   > Screens, and reserved ranges"). Muoversi qui richiede attenzione e la
   > profilassi del punto 4.3.

7. **Chiudi CSpect e ricopia `!Blocks-64.bin` da SD a PC** -- e' la conclusione
   necessaria del passo, senza la quale la modifica resta solo nell'immagine:

       & C:\zx\forth\F18\tools\vForth\util\mountw.ps1
       Copy-Item 'W:\tools\vForth\!Blocks-64.bin' 'C:\zx\forth\F18\tools\vForth\!Blocks-64.bin' -Force
       & C:\zx\forth\F18\tools\vForth\util\mountw.ps1 -Dismount

   E' l'unico trasferimento del progetto che va nella direzione **SD -> PC**.
   Vale anche per qualsiasi altro Screen editato dentro CSpect che debba entrare
   nel rilascio.


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
