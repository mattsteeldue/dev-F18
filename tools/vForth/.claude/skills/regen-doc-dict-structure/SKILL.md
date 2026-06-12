---
name: regen-doc-dict-structure
description: Rigenera il testo dei due paragrafi del manuale .odt (sezione "Dictionary memory structure") che mostrano la struttura interna delle definizioni nel name-space/dizionario con indirizzi hex e dump, interrogando l'emulatore sui binari correnti. Usare dopo un rebuild del core, quando il manuale va riallineato, o quando l'utente chiede /regen-doc-dict-structure. NON modifica mai i file .odt/.pdf.
---

# regen-doc-dict-structure: rigenera i paragrafi della struttura del dizionario

Il manuale `doc/vForth1.8-core-en-YYYYMMDD.odt` (e il .pdf che ne deriva)
contiene una sezione "Dictionary memory structure" con due paragrafi pieni di
indirizzi hex legati al build corrente:

1. l'esempio di memoria delle definizioni contigue `SWAP` e `DUP`
   (tabelle "Heap memory:" NFA/LFA/CFA e "Main memory:" Mirror/xt);
2. il transcript "You can verify yourself..." con l'output reale di
   `SEE SWAP`, `SEE DUP` e dei relativi `DUMP`.

A ogni rebuild del core gli xt e i mirror cambiano (gli heap-pointer di
solito no, se SWAP/DUP non si spostano) e la correzione a mano e' error
prone. Questo skill produce il testo aggiornato; l'inserimento nel .odt
resta MANUALE.

## REGOLE INVIOLABILI

- **NON modificare mai i file `.odt` e `.pdf`**: niente edit, niente
  rigenerazione automatica del documento. L'output va consegnato come testo
  che l'utente incolla in LibreOffice.
- I binari devono essere quelli correnti: se il core e' stato appena
  modificato, prima ricompilare (vedi /bump-build) e poi rigenerare.

## Procedura

1. Da `tools/vForth/` lanciare (boot dell'emulatore ~2 minuti):

   ```
   python3 util/gen-dict-structure.py
   ```

   Lo script avvia l'emulatore headless con i binari di
   `project/vForth18_DOES/output/`, carica `SEE` e `DUMP` via NEEDS, passa
   in HEX, legge i byte reali di SWAP e DUP (heap + main memory) e cattura
   l'output reale di SEE/DUMP. Stampa su stdout i due paragrafi completi.

2. Verifica di plausibilita' sul testo generato:
   - gli heap-pointer NFA/LFA/CFA di SWAP e DUP normalmente NON cambiano
     tra build (0307/030C/030E e 0310/0314/0316); se cambiano, segnalarlo
     all'utente perche' il layout della heap si e' spostato;
   - gli `xt` e i `Mirror` cambiano quasi a ogni build: e' il motivo per
     cui si rigenera;
   - la data di build mostrata nella frase introduttiva deve coincidere con
     quella dello SPLASH corrente.

3. Confronto con la versione attuale del manuale (solo lettura!):

   ```
   cd /tmp && unzip -o -q <repo>/doc/vForth1.8-core-en-<ultima>.odt content.xml
   python3 -c "import re;print(re.sub(r'<[^>]+>','\n',open('content.xml').read()))" > doc.txt
   grep -n "Dictionary memory structure" doc.txt
   ```

   Mostrare all'utente un riassunto delle differenze (tipicamente: vecchi
   xt/mirror -> nuovi, vecchia data build -> nuova).

4. Consegnare il testo generato all'utente, indicando che va incollato a
   mano nella sezione "Dictionary memory structure" del .odt (mantenendo la
   formattazione monospace/tabella del documento), e che il .pdf va poi
   riesportato da LibreOffice.

## Note

- Lo script dipende da `emu/repl.py` e dai moduli in `emu/`; il transcript
  e' output REALE del core (compresa la colonna ASCII dei DUMP), quindi e'
  fedele a cio' che l'utente vedrebbe sull'hardware.
- Se servono parole diverse da SWAP/DUP (il manuale usa quelle), modificare
  `WORD_A`/`WORD_B` in testa a `util/gen-dict-structure.py`.
