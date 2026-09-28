---
name: regen-doc-dict-structure
description: Rigenera il testo dei paragrafi dinamici del manuale .odt (par. 4.6 "Dictionary memory structure" e par. 3.8 "Debugger Utility") che mostrano indirizzi hex, dump e transcript SEE legati al build corrente, interrogando l'emulatore sui binari correnti; ogni blocco di output e' etichettato col paragrafo di appartenenza e confrontato (in sola lettura) col testo gia' presente nel .odt, dicendo quali blocchi sono INVARIATI e quali DA AGGIORNARE. Usare dopo un rebuild del core, quando il manuale va riallineato, o quando l'utente chiede /regen-doc-dict-structure. NON modifica mai i file .odt/.pdf.
---

# regen-doc-dict-structure: rigenera i paragrafi dinamici del manuale

Il manuale `doc/vForth1.8-core-en-YYYYMMDD.odt` (e il .pdf che ne deriva)
contiene brani pieni di indirizzi hex legati al build corrente, in DUE
paragrafi; l'output dello script etichetta ogni blocco col paragrafo di
appartenenza (`[par. 4.6 ...]` / `[par. 3.8 ...]`):

**par. 4.6 "Dictionary memory structure"**
1. l'esempio di memoria delle definizioni contigue `SWAP` e `DUP`
   (tabelle "Heap memory:" NFA/LFA/CFA e "Main memory:" Mirror/xt);
2. il transcript "You can verify yourself..." con l'output reale di
   `SEE SWAP`, `SEE DUP` e dei relativi `DUMP`.

**par. 3.8 "Debugger Utility"** (in misura minore)
3. i tre transcript d'esempio `SEE TYPE` (colon-definition), `SEE NIP`
   (CODE word) e `SEE IF` (IMMEDIATE), catturati in DECIMAL come nello
   stile di quel paragrafo (letterali come `12` e `-8`; gli indirizzi
   stampati da SEE restano hex a prescindere dalla BASE);
4. i dati per la nota in prosa dopo `SEE NIP`: i byte che seguono il
   `jp (ix)` (Mirror della definizione successiva), il NOME REALE di
   quella definizione, e la frase pronta da incollare (forma scelta
   dall'autore il 2026-09-26): il Mirror e' l'heap-pointer al CFA della
   parola successiva, quindi `$<mirror> FAR 8 DUMP` mostra il suo xt
   seguito dalla NFA della parola dopo ancora (oggi: TUCK, xt $68E0,
   poi la NFA di SWAP). Il Mirror NON punta alla NFA.

A ogni rebuild del core gli xt e i mirror cambiano (gli heap-pointer di
solito no, se le parole non si spostano) e la correzione a mano e' error
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
     quella dello SPLASH corrente;
   - par. 3.8: i letterali della decompilazione devono essere decimali
     (`12`, `-8`); nella nota su NIP controllare che il nome della
     definizione successiva sia quello reale -- la prosa storica del
     manuale citava SWAP, ma la parola adiacente puo' cambiare tra build
     (es. oggi e' TUCK; SWAP e' la NFA che si vede nel DUMP).

3. Confronto con il manuale: lo fa lo script stesso, in coda all'output
   (sezione "Comparison with the manual"). Legge in sola lettura il
   `content.xml` del `.odt` piu' recente in `doc/` (o quello passato con
   `--odt PATH`; `--no-compare` lo salta) e per ciascuno dei 9 blocchi
   (4.6: frase introduttiva, tabelle SWAP/DUP, transcript SWAP/DUP;
   3.8: SEE TYPE/NIP/IF, nota dopo SEE NIP) dice:
   - `INVARIATO`: il manuale contiene gia' quel testo, nulla da incollare;
   - `DA AGGIORNARE`: con le righe `!` non trovate nel manuale, cioe'
     quelle cambiate.

   Il confronto e' per sequenza di token (separatori: spazi e `|`), quindi
   ignora a-capo, celle di tabella e spaziature del `.odt`, e normalizza gli
   apici/trattini tipografici. Nel par. 3.8 si confronta solo l'output di
   SEE, perche' il manuale mette della prosa tra il comando e l'output.
   Nel dubbio segnala `DA AGGIORNARE`, mai un falso `INVARIATO`. Se
   l'`.odt` e' aperto in LibreOffice (lock) il confronto viene saltato con
   un avviso.

   Il confronto col manuale -- non con la build precedente -- e' voluto:
   oltre a evitare falsi positivi (una modifica che allunga una sola parola
   sposta solo le successive, ma una parola ferma puo' comunque cambiare
   transcript se chiama una parola spostata), scopre anche gli errori del
   manuale rimasto indietro di piu' build (verificato 2026-09-26: sul
   manuale 20260920 segnala 6 blocchi, tra cui i DUMP del 4.6 gia'
   sbagliati prima; sul 20260925 aggiornato dall'autore, 9 su 9 invariati).

4. Consegnare all'utente **solo i blocchi `DA AGGIORNARE`**, indicando il
   paragrafo e che vanno incollati a mano nel .odt (mantenendo la
   formattazione monospace/tabella del documento), e che il .pdf va poi
   riesportato. Se tutto e' `INVARIATO`, dirlo: non c'e' nulla da fare.
   Se il testo va salvato in `products/`, seguire la regola di `CLAUDE.md`
   ("Reference manual"): prosa un paragrafo per riga, CRLF.

## Note

- Numerazione dei paragrafi del manuale (aggiornata dall'autore il
  2026-09-26; le edizioni precedenti usavano 3.20 e 3.6.1):
  par. 4.6 "Dictionary memory structure", par. 3.8 "Debugger Utility",
  par. 2.4 "Block / Screen system" (numero dei buffer: da rivedere a mano
  quando cambia `BUFFERS` in `system.asm`). I draft vecchi in
  `products/` possono citare ancora i numeri precedenti.
- Lo script dipende da `emu/repl.py` e dai moduli in `emu/`; il transcript
  e' output REALE del core (compresa la colonna ASCII dei DUMP), quindi e'
  fedele a cio' che l'utente vedrebbe sull'hardware -- con due sole
  normalizzazioni al formato del manuale che compensano la sciatteria di
  SEE: la riga iniziale col solo length-byte viene soppressa e gli
  heap-pointer nella riga `Lfa:` sono zero-padded a 4 cifre.
- Se servono parole diverse da SWAP/DUP (il manuale usa quelle), modificare
  `WORD_A`/`WORD_B` in testa a `util/gen-dict-structure.py`.
