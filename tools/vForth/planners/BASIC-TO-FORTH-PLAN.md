# Da NextBASIC a vForth: guida di migrazione, capitolo per capitolo

> Stato: IN CORSO (ripresa da: fase 3, cap. 11). Fase 3 avviata il
> 2026-10-12: scritti il cap. 1 (`01-basic-programming-concepts.md`, 66
> righe Forth provate) e il cap. 2 (`02-decisions.md`, 62 righe), e il
> 2026-10-13 il cap. 4 (`04-procedures-and-subroutines.md`, 92 righe), il
> cap. 5 (`05-read-data-restore.md`, 51 righe), il cap. 6
> (`06-expressions.md`, 90 righe), il cap. 7 (`07-strings.md`, 80
> righe), il cap. 8 (`08-functions.md`, 85 righe) e il cap. 9
> (`09-mathematical-functions.md`, 29 righe: la virgola mobile è
> `no-test`) e il cap. 10 (`10-random-numbers.md`, 31 righe), tutti
> con `emu/test_basic_guide.py --chapter N`, 0 errori; i loro listati BASIC
> (5 nel cap. 1, 4 nel cap. 2, 7 nel cap. 4, 5 nel cap. 5, 5 nel cap. 6, 5 nel cap. 7, 5 nel cap. 8, 5 nel cap. 9, 4 nel cap. 10) sono da provare
> dall'autore su MAME o CSpect e da salvare in `bas2f/`: prova rinviata
> dall'autore il 2026-10-13, si fa in blocco più avanti. Fase 0 chiusa il 2026-10-11. Fase 2 (capitolo pilota, cap. 3)
> chiusa: scritta, approvata, listati BASIC provati dall'autore su MAME il
> 2026-10-12 e scaricati in `bas2f/`. **Fase 1 chiusa il 2026-10-12 per la
> parte che si fa senza la macchina**: `situation/BASIC-vs-vForth-matrix.md`
> ha voci di Appendice B, concetti e prova in emulatore per tutti e 25 i
> capitoli (537 righe; i cap. 17-25 riletti e riscritti nel secondo giro,
> più la teoria del colore del cap. 15). Resta, della fase 1, solo l'elenco
> "Da provare su CSpect o sulla macchina" in fondo alla matrice, che tocca
> all'autore (grafica, file system, stream, RTC, sprite, suono; `%RND`
> contro `RND`; `+"`). La matrice dei cap. 15-25 è chiusa: la fase 4 può
> partire. Dal 2026-10-12 la guida è una cartella, `doc/basic-to-vforth/`,
> un file per capitolo (D2 rivista).

## 1. Obiettivo

Un documento per chi conosce NextBASIC e vuole passare a vForth. Segue l'indice
del manuale `doc/zx-spectrum-next-manual-3rd-ed.md` (25 capitoli, 4 appendici) e,
per ogni semantica BASIC, indica la semantica Forth equivalente o la più vicina,
dove impararla (tutorial, help, manuale vForth) e dove invece il modello cambia.

Tre prodotti, in ordine di dipendenza:

1. **La matrice di corrispondenza** (strumento di lavoro, `situation/`): una riga
   per ogni keyword, funzione e concetto del manuale Next.
2. **La guida** (deliverable, in inglese): un capitolo per capitolo del manuale.
3. **L'elenco dei tutorial mancanti**, ricavato dalle righe della matrice senza
   un tutorial di destinazione.

## 2. Cosa c'è già

- Il manuale Next trascritto e riparato, con intestazioni `##` per capitolo e
  `###` per paragrafo, e marcatori `<!-- PDF page N -->`.
- **Appendice B, "NextBASIC Keywords and Functions"** (riga 16368 del `.md`):
  circa 150 forme di comando e 40 funzioni, in ordine alfabetico. È la lista di
  controllo di completezza: ogni voce deve avere una riga nella matrice.
- I tutorial da `000` a `066`, 597 file di help, 229 file in `inc/`,
  le librerie in `lib/`.
- Un precedente dello stesso genere: `situation/tutorial-vs-screens.md`
  (tutorial contro Screen di *Starting FORTH*, con colonna di forza della
  corrispondenza) e `situation/vForth-tutorial-gap-analysis.md`. Il formato della
  matrice riprende quello.
- 11 tutorial nominano già BASIC nel testo (001, 012, 016, 024, 041, 054, 057,
  058, 059, 060, 065): vanno riletti nella fase 1, contengono confronti già
  scritti.

## 3. Vincolo di licenza

Il manuale Next è **CC BY-NC-SA 4.0**; vForth è **MIT**. Una guida che ne copia
testo o listati diventa opera derivata e ne eredita la licenza (non commerciale,
condividi allo stesso modo), incompatibile con MIT. Quindi:

- la guida cita capitolo, titolo del paragrafo e pagina, e **non riporta testo**
  del manuale;
- i listati BASIC di confronto sono **scritti da noi**, brevi, non copiati dagli
  esempi del manuale (un `FOR`/`NEXT` di tre righe non è di nessuno, ma il
  programma di esempio di pagina N sì);
- la matrice in `situation/` è materiale interno e può citare liberamente.

Deciso (D1): la guida resta sotto MIT, con listati scritti da noi.

## 4. La matrice di corrispondenza

File: `situation/BASIC-vs-vForth-matrix.md`. Una tabella per capitolo, colonne:

| Colonna | Contenuto |
|---|---|
| BASIC | keyword, funzione o concetto (`FOR ... STEP`, `DEF FN`, "numeri di riga") |
| Rif. manuale | capitolo, paragrafo, pagina PDF |
| vForth | parola o idioma (`DO ... +LOOP`), con `NEEDS` se non è nel core |
| Classe | vedi sotto |
| Dove si impara | tutorial `NNN`, `help/`, paragrafo del manuale vForth |
| Nota | la differenza che fa inciampare (ordine degli argomenti, unità, segno) |
| Verifica | `emu` (provato in emulatore), `CSpect`, `hw`, oppure vuoto |

Classi:

- **A - diretta**: stessa semantica, cambia solo la sintassi (`REG n,v` ->
  `v n REG!`).
- **B - idioma**: si ottiene lo stesso effetto con una costruzione diversa
  (`READ`/`DATA` -> tabella con `CREATE` e `,`).
- **C - modello diverso**: il concetto BASIC non si trasporta, se ne spiega il
  sostituto (numeri di riga e `GO TO` -> definizioni e strutture di controllo;
  variabili stringa -> indirizzo e lunghezza).
- **D - assente**: in vForth non c'è, e si dice se manca per scelta o è un vuoto
  da colmare (`PLAY`, finestre di NextZXOS).
- **N - non pertinente**: capitolo documentale o di installazione.

Regole di compilazione della matrice:

- prima di scrivere `NEEDS X`, controllare con `grep` in `src/F18e.f` che `X` non
  sia nel core;
- nomi Forth reali, mai la forma mappata FAT;
- "banco da 16K" per BASIC e NextReg `$12`, "pagina da 8K" per MMU7: nel
  capitolo 23 la distinzione è l'argomento stesso;
- ogni riga di classe A o B ha uno spezzone Forth provato (sez. 6).

## 5. Triage preliminare dei capitoli

Stima fatta sugli indici, da confermare nella fase 1. "Tutorial" elenca quelli
che coprono già il tema.

| Cap. | Titolo | Classe prevalente | Tutorial esistenti | Vuoti probabili |
|---|---|---|---|---|
| 1 | Basic Programming Concepts | C | 000, 001, 003, 005, 028, 029 | il capitolo ponte (vedi sotto) |
| 2 | Decisions | A/B | 006, 013 | `ON` -> `CASE` o tabella di salto |
| 3 | Looping | A/B | 007, 012 | `EXIT` dal ciclo: `LEAVE`, `UNLOOP` |
| 4 | Procedures and Subroutines | B/C | 005, 061, 026 | `REF`, valori di ritorno multipli |
| 5 | READ, DATA, RESTORE | B | 008, 010, 023 | tabelle di dati come idioma a sé |
| 6 | Expressions | C | 001, 002, 004, 011, 015 | infisso -> RPN, interi a 16 bit e segno |
| 7 | Strings | C | 009 | slicing `TO`, concatenazione, `S"` e heap |
| 8 | Functions | B | 005, 009, 014 | `DEF FN`, `VAL` -> `EVALUATE`/`NUMBER` |
| 9 | Mathematical Functions | B | 024, 064 | scelta fra virgola mobile e interi scalati |
| 10 | Random Numbers | A | nessuno dedicato | **tutorial nuovo** (`RND`, `RANDOM`, `RANDOMIZE`, `CHOOSE`) |
| 11 | Arrays | B | 008, 010, 023 | array a più dimensioni, array di stringhe |
| 12 | Conditions | A | 006, 011 | flag ben formati, `AND`/`OR` bit a bit e logici |
| 13 | The Character Set | A/B | 003, 008, 030 | UDG, set di caratteri alternativi |
| 14 | More about PRINT and INPUT | A/B | 003, 014, 016, 031, 035 | `WIDECHAR`/`NARROWCHAR` (nessun tutorial li cita), `SCREEN$` |
| 15 | Colours | A | 030, 031, 056 | `LAYER`, palette ULA |
| 16 | Graphics | A | 036, 037, 038, 052 | clipping, tiling (058 in parte) |
| 17 | Time and Motion | A/B | 032, 039, 053, 045 | **RTC** (`IDE_RTC`, `M_GETDATE`: nessun tutorial), scrolling |
| 18 | Sound and Music | A + D | 033, 034, 050, 055 | `PLAY` (D), WAV/MOD/PT3 (D) |
| 19 | NextZXOS and alternatives | B + N | 042, 043, 057, 059 | `LOAD`/`SAVE` di BASIC contro `INCLUDE`, `LOAD` di Screen, `SAVE-BYTES` |
| 20 | Channels, Streams, Drivers, Windows | B + D | 003 (`SELECT`), 047 | **tutorial nuovo** su `SELECT` e stream; finestre (D) |
| 21 | Optional Features | N + A | 047, 048 | RTC (come cap. 17) |
| 22 | IN, OUT and the Next Registers | A | 040, 049, 054 | pochi: `P@`/`P!`, `REG@`/`REG!` sono diretti |
| 23 | The Memory | A/C | 008, 025, 041 | `BANK` (16K) contro `MMU7!` (8K), `CLEAR` |
| 24 | The System Variables | A | 008 | tabella delle variabili usate da vForth |
| 25 | Using Machine Code | C | 027, 057 | `USR` -> `CODE`; chiamate a NextZXOS (`CALL#`: nessun tutorial) |
| App. A | Character Set, Z80N, Control Codes | N/A | 027, 031 | rimando |
| App. B | Reference | A | 062 | **indice inverso keyword -> parola** e codici d'errore |
| App. C | Machine Personalities | N | - | - |
| App. D | The Calculator | C | 001 | l'interprete Forth è una calcolatrice RPN |

I capitoli 1, 6 e 7 sono quelli da curare di più: lì il lettore incontra le tre
differenze che non hanno riga nella tabella -- niente numeri di riga, notazione
postfissa, stringhe come indirizzo e lunghezza. Sbagliati quelli, le tabelle dei
capitoli successivi non servono.

## 6. La guida

Forma di ogni capitolo, sempre nello stesso ordine:

1. **In breve**: due o tre frasi su quanto del capitolo si trasporta.
2. **Cosa cambia**: il cambio di modello, se c'è (classe C).
3. **Tabella di corrispondenza**: estratta dalla matrice (BASIC, vForth, nota).
4. **Fianco a fianco**: due o tre esempi, listato BASIC e sorgente Forth.
5. **Senza equivalente**: le voci D, con il motivo.
6. **Per approfondire**: tutorial, help, paragrafo del manuale vForth.

In coda alla guida: l'indice inverso alfabetico keyword BASIC -> parola Forth
(da Appendice B), che è la pagina che l'utente terrà aperta.

Convenzioni: Markdown in inglese (D2, D3); i blocchi di codice Forth seguono le
regole dei sorgenti (7-bit ASCII, nessun TAB, 80 colonne). Ogni spezzone Forth si prova in `emu/repl.py`;
quelli che toccano hardware non emulato (sprite, copper, AY, RTC) li prova
l'autore su CSpect o sulla macchina, e la colonna "Verifica" della matrice lo
registra. Uno script `emu/test_basic_guide.py` estrae i blocchi di codice della
guida e li riesegue: la guida resta allineata al core come i test.

**Un file per capitolo** (deciso il 2026-10-12, vedi D2). La guida sta in
`doc/basic-to-vforth/`:

- `README.md`: titolo, "How to read this guide" e l'indice dei capitoli (un
  capitolo senza link non è ancora scritto);
- `NN-titolo.md`, due cifre e titolo in minuscolo (`03-looping.md`): apre con
  `# Chapter N - Title`, poi il link di ritorno a `README.md`; le sei parti
  sono intestazioni `##`;
- le appendici come `app-a-...md`, l'indice inverso come `keyword-index.md`.
- **piede di navigazione** (chiesto dall'autore il 2026-10-13): ogni
  capitolo finisce con la riga `<!-- nav -->`, una linea e i link a
  capitolo precedente, indice e capitolo successivo. Lo scrive
  `python util/guide-nav.py` (ordine dei nomi di file, titoli dalla prima
  intestazione); va rilanciato a ogni capitolo nuovo, perché cambia anche
  il piede del precedente. L'ultimo capitolo scritto nomina il successivo
  senza link ("not written yet"). `--check` esce con 1 se un piede è
  vecchio; `emu/test_basic_guide.py` segnala il capitolo che non ce l'ha.

I link fra i file restano nella forma `.md` (`[Looping](03-looping.md)`), che
è quella che funziona nel repo; l'eventuale conversione per la wiki è compito
del passo di pubblicazione, non dei sorgenti. Lo script di test segnala come
errore di formato un link verso un file che non esiste. La matrice in
`situation/` resta invece un file solo.

### 6.1 Cosa ha fissato il capitolo pilota (2026-10-11)

Convenzioni nate scrivendo il cap. 3, da confermare o correggere nella
revisione; valgono per tutti i capitoli successivi.

- **Spezzoni verificabili.** In un blocco ` ```forth ` la riga che termina con
  `\ => testo` dichiara cosa stampa; un blocco ` ```text ` subito dopo è
  l'uscita dell'ultima riga del blocco Forth (uscite su più righe); una riga
  senza dichiarazione non deve dare errore. Anche un messaggio d'errore si
  dichiara così (`\ => DO? Can't be executed.`). Il blocco preceduto da
  `<!-- no-test -->` è saltato (attesa di un tasto, cicli senza fine, hardware
  non emulato).
- **Lo script.** `python emu/test_basic_guide.py [--chapter N] [--list]`:
  circa 7 minuti per il cap. 3 sul Raspberry Pi (2 di boot). Aspetta `ok` o un
  errore dopo ogni riga, perché il rilevamento del prompt di `repl.py` torna
  troppo presto quando una riga compila a lungo senza stampare.
- **Righe corte.** Una riga oltre gli 80 caratteri digitata nel REPL viene
  spezzata e il resto è interpretato come riga nuova (`OLO? is undefined`):
  gli spezzoni restano entro 72 colonne, definizioni su più righe.
- **Listati BASIC non provati.** Sono scritti da noi ma qui non c'è modo di
  eseguirli: vanno provati dall'autore su CSpect o MAME prima della
  pubblicazione (nel cap. 3: `EXIT: EXIT 80`, `REPEAT: WHILE`, `INT (n/2)`;
  provati tutti su MAME il 2026-10-12).
- **Il fianco a fianco mostra anche l'idioma.** Dopo la traduzione letterale
  (cicli annidati con `J`) viene la versione fattorizzata (`ROW` + `TABLE`):
  è il punto in cui il lettore vede che Forth non si scrive come BASIC.
- **Omonimi che ingannano** vanno in "What changes", non in tabella: nel
  cap. 3 `EXIT` (esce dalla definizione, non dal ciclo) e `REPEAT` (chiude
  il ciclo, non lo apre).

Per strada: la voce `help/^do.txt` (`?DO`) è stata ampliata il 2026-10-12
(effetto sullo stack, caso dell'indice oltre il limite); `UNLOOP`, `J` e `K` stanno in `inc/`, tutto il resto del capitolo
è nel core.

## 7. Fasi

| Fase | Lavoro | Esce | Chi verifica |
|---|---|---|---|
| 0 | Decisioni D1-D5 -- FATTA 2026-10-11 | questo piano aggiornato | autore |
| 1 | Matrice: voci di Appendice B, concetti dei cap. 1-25 e prova in emulatore -- FATTA 2026-10-12; restano le prove su CSpect elencate in fondo alla matrice (autore) | `situation/BASIC-vs-vForth-matrix.md` | Claude, in emulatore |
| 2 | Capitolo pilota (cap. 3, Looping): fissa forma e tono -- FATTA: scritto 2026-10-11 e approvato; listati BASIC provati dall'autore su MAME il 2026-10-12 | un capitolo della guida | autore |
| 3 | Parte linguaggio: cap. 1-14 -- IN CORSO: fatti i cap. 1, 2 e 3 (2026-10-12) e i cap. 4, 5, 6, 7, 8, 9 e 10 (2026-10-13), si riparte dal cap. 11 | guida, prima parte | emulatore |
| 4 | Parte macchina: cap. 15-25 | guida, seconda parte | emulatore + CSpect |
| 5 | Appendici e indice inverso | guida completa | Claude |
| 6 | Vuoti: elenco ordinato dei tutorial da scrivere, uno per volta con `/new-tutorial` | `TODO.md`, tutorial nuovi | autore |
| 7 | Rimandi: una riga "Coming from BASIC" nei tutorial 001-029 | tutorial ritoccati (solo commenti) | - |

La fase 1 è il grosso del lavoro e si può spezzare per capitolo in sessioni
diverse: la matrice porta in testa una riga di stato per capitolo (fatto, in
corso, da fare), così si riprende da qualsiasi postazione.

La fase 2 viene prima delle altre perché cambiare forma dopo dieci capitoli
costa: si sceglie un capitolo facile, di classe A/B, con tutorial già solidi.

## 8. Decisioni (prese dall'autore il 2026-10-11)

- **D1 - Licenza e listati.** La guida resta sotto **MIT**; i listati BASIC di
  confronto sono scritti da noi, nessun testo né listato copiato dal manuale.
- **D2 - Formato e posto.** Markdown in `doc/` (che non va sulla SD) e
  pubblicazione sulla wiki di `vforth-next`. Scartati: capitolo del manuale
  `.odt`, serie di tutorial `.f`. **Rivista il 2026-10-12:** non più il file
  unico `doc/BASIC-to-vForth.md` ma la cartella `doc/basic-to-vforth/`, un file
  per capitolo, con i link fra i file nella forma `.md` (sez. 6).
- **D3 - Lingua.** Inglese.
- **D4 - Profondità sui capitoli tecnici.** Per i capitoli di installazione e
  documentali (parti dei cap. 19 e 21, Appendice C): un breve rimando, più
  l'indicazione esplicita di non-copertura dove vForth non offre nulla.
- **D5 - Edizione di riferimento.** Solo la terza edizione, con i numeri di
  pagina del PDF. Nessun rimando alle edizioni precedenti.

## 9. Candidati a tutorial nuovo (elenco provvisorio)

Ricavati dal triage, da confermare con la matrice. Banda `000-029` per il
linguaggio, `030-059` per l'hardware, `060-...` per il resto.

1. **Numeri casuali** (cap. 10): `RND`, `RANDOM`, `RANDOMIZE`, `CHOOSE`. Oggi
   compaiono solo di passaggio in 051, 056, 062, 063.
2. **Orologio in tempo reale** (cap. 17 e 21): `IDE_RTC`, `M_GETDATE`. Nessun
   tutorial li nomina.
3. **Stream e canali** (cap. 20): `SELECT`, `OPEN<`, stampa su stream diversi.
   `SELECT` è usato in 23 tutorial ma spiegato in nessuno.
4. **Tabelle di dati** (cap. 5 e 11): l'idioma che sostituisce `DATA`/`READ` e
   `DIM`, oggi sparso fra 008, 010 e 023.
5. **Caratteri larghi e stretti, UDG** (cap. 13 e 14): `WIDECHAR`, `NARROWCHAR`,
   `udg+`.
6. **Chiamare la ROM e NextZXOS** (cap. 25): `CALL#`, `M_P3DOS`, il confine con
   `CODE`.
7. **"Coming from BASIC"** (cap. 1): un tutorial ponte, breve, che apre la serie
   per chi arriva dalla guida. Potrebbe essere il primo da scrivere.

Per `PLAY` (cap. 18) la domanda è diversa: non un tutorial ma una libreria che
oggi non esiste. Va in `TODO.md` come proposta, fuori da questo piano.

## 10. Vuoti di funzionalità: prima ricognizione (2026-10-11)

Ricerca per nome in `src/F18e.f`, `inc/` e `lib/`, a partire da Appendice B. È
una ricognizione, non la matrice: un nome non trovato può esistere sotto un
altro nome, e va riconfermato nella fase 1.

**Nessuna parola, servirebbe una libreria nuova**

- `PLAY` e l'audio digitale (WAV, MOD, PT3): nessuna traccia.
- Finestre di NextZXOS, `OPEN #`/`CLOSE #` verso canali, `DRIVER`: c'è solo
  `SELECT` per scegliere lo stream.
- `TILE` / `TILE BANK` / `TILE DIM` (tiling software su Layer 1/2):
  `lib/TILE80.f` e `lib/layer3.f` sono la tilemap hardware, un'altra cosa.
- Sprite oltre il minimo: `lib/SPRITE.f` ha init, update, hide, palette, on/off.
  Mancano movimento automatico, sprite relativi/compositi, batching, funzioni
  di collisione.
- `COPY` da file a file.

**Nessuna parola, ma bastano poche righe o un `REG!`**

- `BANK NEW`: l'allocazione via `IDE_BANK` esiste solo dentro `inc/PAINT.f`,
  non come parola pubblica. Le altre forme di `BANK` (`COPY`, `ERASE`, `POKE`,
  `PEEK`) si fanno con `MMU7!` più `CMOVE`/`FILL`/`C!`.
- `LAYER AT` (scroll), `LAYER OVER` (priorità), `LAYER BANK` (doppio buffer),
  `SPRITE DIM`, `SPRITE BORDER`, `PALETTE ...`: solo `REG!` diretto, come nel
  tutorial 056. `LAYER DIM` (clip) esiste solo in LAYER22/LAYER24.
- `LAYER ERASE` (riempimento di un rettangolo), `DRAW x,y,z` (arco),
  `PRINT POINT` (testo a coordinate pixel), stippling: non trovati.
- `SCREEN$ (x,y)`: non trovata. `ATTR (x,y)` si ricava da `PIXELATT`.
- `PAUSE n`: non c'è una parola con quel nome; c'è `MS` in `inc/ms.f`.
- `TIME$`: `IDE_RTC` e `M_GETDATE` danno i valori grezzi, manca la formattazione.
- Slicing di stringhe: `/STRING` non c'è; `+"` e `-TRAILING` sì.

**Presenti** (controllati): `BEEP` (`lib/bleep.f`), `.BORDER`, `.INK`/`.PAPER`/
`.BRIGHT`/`.FLASH`/`.INVERSE`/`.OVER`, `.AT`, `TAB`, `INKEY`, `PLOT`, `POINT`,
`CIRCLE`, `DRAW-LINE`, `PAINT`, `RND`/`RANDOMIZE`, `REG!`/`REG@`, `SPEED!`,
`REMOUNT`, `CD`, `PWD`, `MAKEDIR`, `REMOVEDIR`, `RENAME`, `UNLINK`, `F_CHMOD`,
`DIR`, `SAVE-BYTES`/`LOAD-BYTES`, `SAVE-BANK`, `SCREEN-FROM-FILE`, e in
`lib/floating.f` trigonometria, `FEXP`, `FLN`, `FSQRT`, `PI`.

**Correzioni emerse compilando la matrice (2026-10-12).** Tre voci di
"Presenti" qui sopra erano sbagliate: `INKEY` non esiste (nel core è
commentata), `RENAME` rinomina una parola del dizionario e non un file (per i
file c'è `F_RENAME`), `SAVE-BANK` è una parola di `lib/ZAP.f` limitata ai
banchi 16-19. La matrice riporta le forme giuste e, in coda, l'elenco dei file
di help da rivedere trovati per strada.

**Emerso dai cap. 8-25 (2026-10-12).** Il dettaglio è nella matrice, sezione
"Cosa esce dalla matrice"; qui solo ciò che tocca il piano.

- Tre trappole da mettere in "What changes" dei rispettivi capitoli: `ACCEPT`
  restituisce i caratteri letti più uno (cap. 14); `COMPARE` non distingue
  maiuscole e minuscole finché non si dà `CASEON` (cap. 13); `MMU7!` dal
  prompt nasconde lo heap con i nomi, quindi va usata dentro una definizione
  che rimette la pagina (cap. 23).
- `SQRT` prende una cella, non un doppio: la voce di "Presenti" va letta così.
- `RND` segue la sequenza di `RND` in virgola mobile di BASIC; se anche
  `%RND` la segua è da vedere su CSpect (il manuale dà un altro primo valore).
- Candidati `inc/` nuovi: ricerca in una stringa (`SCAN`, `SEARCH`), potenza
  fra interi, `UDG!`, una `PAUSE` interrompibile, `TIME`, e le definizioni
  provate nella matrice (`SGN`, `INPUT#`, `ARRAY`, `MATRIX`, `SARRAY`).
- Lo script di prova non regge `KEY` da solo (nessun cursore: il giro resta
  fermo per minuti): negli spezzoni della guida `KEY` va sotto `no-test`.
- `NEEDS GRAPHICS` in emulatore si carica ma non si inizializza (`IDE_MODE`
  non emulata): tutti gli spezzoni grafici dei cap. 15-17 sono `no-test` e
  vanno all'autore, come previsto dalla sez. 6.

**Emerso dalla rilettura dei cap. 17-25 (2026-10-12).** Il dettaglio è nella
matrice, sezione "Trovato rileggendo i cap. 15 e 17-25".

- Altre due voci di "Presenti" da leggere con cautela: `SCREEN-FROM-FILE`
  copia un file di testo in uno Screen (non carica un'immagine), e `DIR` dà
  già dimensione, data e ora.
- `COPY` da file a file non chiede una libreria: tre righe con `F_READ` e
  `F_WRITE`, provate. Passa a D-inc; `LPRINT` e `LLIST` passano a idioma
  (`3 SELECT`), da provare con una stampante.
- Trappole per "What changes": `CD` rompe `NEEDS` (cap. 19); `F_GETLINE`
  conta anche il fine riga (cap. 20); `SPRITE` è una struttura e
  `SPRITES-ON` riscrive il NextReg `$15` (cap. 17); nel registro 7 del chip
  AY il bit a 0 accende (cap. 18).
- Candidati `inc/` nuovi: `PAUSE` e `FRAMES`, `TIME`, `TIME$` con i
  secondi, `HIT?` (collisione fra sprite), `FCOPY`, `ZLEN`.
- In emulatore non si provano `DIR`, `CD`, `PWD`, `IDE_RTC` (chiamate non
  emulate): negli spezzoni dei cap. 17 e 19 vanno sotto `no-test`.

**Emerso scrivendo il cap. 4 (2026-10-13).**

- `3 AREA .` con un argomento in meno non si ferma in `AREA`: moltiplica
  per quello che sta sotto lo stack e l'errore lo dà la parola dopo
  (`.? Stack is empty.`). Usato in "What changes".
- `GCD` esiste già in `lib/GCD.f` (stessa definizione, con `TUCK`): il
  capitolo la cita.
- Trappola dei locali, provata in emulatore: dopo il `;` di una parola con
  `{ }` `CONTEXT` resta su `DEFLOCALS` fino al prossimo `:`, quindi un locale
  con lo stesso nome di una parola la nasconde anche dal prompt (con un
  locale `AREA`, `3 4 AREA .` stampa 0 e lascia 3 e 4 sullo stack; dopo un
  `:` qualsiasi torna a dare 12). `lib/LOCALS.f` la chiama "harmless", ma
  vale solo se i nomi non coincidono. Nel capitolo i locali di `RECT` si
  chiamano `SURFACE` e `PERIM`, e la trappola è in "What changes".
- Un locale di lavoro che non sia né argomento né risultato non ha forma
  con `{ }`: la riga della matrice `LOCAL v=valore` -> locale di uscita vale
  solo quando il valore è anche il risultato. Messo in "No equivalent".

**Emerso scrivendo il cap. 5 (2026-10-13).**

- Il conteggio `HERE tab - 2 /` vale solo subito dopo l'ultima virgola: la
  prima stesura lo metteva dopo altre definizioni e dava 58 invece di 6.
  Il capitolo lo dice.
- Per l'elenco di stringhe il capitolo usa una tabella di indirizzi (una
  `CREATE` con `,"` per stringa), non lo heap con `H"`: resta tutto nel
  core, senza `NEEDS`.

**Emerso scrivendo il cap. 6 (2026-10-13).**

- `3.5 .` non stampa solo 0: lascia 35 sullo stack, e il `.` successivo lo
  trova. Il capitolo lo mostra così (due `.` di fila), ed è il modo più
  breve di far vedere che un doppio occupa due celle.
- `0<>` non esiste (`0<>? is undefined.`): il flag ben formato si ottiene
  con `0= 0=`. `NOT` del core è il NOT logico, uguale a `0=`.
- `1 0 /` e `7 0 MOD` danno -1. Anche un quoziente che non sta in una cella
  dà -1 senza avviso (`1000000. 7 M/`, `1000000. 7 UM/MOD`): non è nel
  capitolo, va nel cap. 9 o nel tutorial 015.
- La virgola mobile nel cap. 6 è solo prosa (`NEEDS FLOATING`, `FLOATING`,
  `INTEGER`, le quattro operazioni): nessuno spezzone, perché in emulatore
  non si prova. Gli spezzoni, `no-test`, vanno nel cap. 9.
- Il decimale senza virgola mobile è mostrato con un intero scalato e
  `<# # 46 HOLD #S #>` (`.TENTHS`, 98.6 da 37 gradi): è la risposta
  consigliata prima della libreria.
- Nei listati BASIC del cap. 6 è da controllare sulla macchina soprattutto
  `PRINT %(f<<7)|(b<<6)|(p<<3)|i` (atteso 79) e `PRINT % SGN {a/2}` con
  `%a=50000` (atteso -7768); il testo afferma anche che
  `PRINT %30000*20/100` dà 101 come in Forth.

**Emerso scrivendo il cap. 7 (2026-10-13).**

- Il capitolo definisce da sé le parole che mancano, tutte provate:
  `$!` (assegna a una stringa contata), `$+!` (accoda), `/STRING`,
  `SLICE`, `-LEADING`, `UPCASE`, `LOWER` e `LOWCASE`, `TIMES`,
  `BACKWARDS`. Sono le prime candidate D-inc da promuovere in `inc/`
  (`/STRING` per prima, poi `$!` e `$+!` con il nome da decidere: `PLACE`
  nel core è già una variabile utente).
- `+"` resta fuori dal capitolo: in emulatore `H" abc" +" def"` seguito da
  `FAR COUNT TYPE` stampava `bcjdef`. Era un difetto di `inc/+~.f`,
  corretto lo stesso giorno e provato in emulatore (voce in `TODO.md`, con
  quel che resta: prova dell'autore, `+C`, test). Il capitolo la nomina
  soltanto, in "No equivalent": estende solo l'ultima stringa dello heap.
- `S"` funziona anche dal prompt e lascia un indirizzo nella finestra
  MMU7 (`$ED29` nella prova). Il capitolo dice di usare la coppia subito
  o di copiarla, e di non scriverci dentro; gli esempi tengono i
  letterali dentro una definizione (`: PLANET S" Spectrum" ;`).
- `COMPARE` all'avvio non distingue maiuscole e minuscole
  (`S" next" S" NEXT" COMPARE` dà 0): mostrato qui, con rimando al cap. 13
  per `CASEON`.
- `a$( TO n)` è solo `n MIN` sulla lunghezza, e l'assegnazione a una
  sottostringa è `CMOVE` (o `FILL`): la regola "procustea" di BASIC è il
  comportamento naturale.

**Emerso scrivendo il cap. 8 (2026-10-13).**

- `S" "` non dà la stringa vuota: `WORD` salta il delimitatore iniziale e
  si prende il resto della riga (`: T6 S" " VAL . ;` non definisce `T6`).
  È lo stesso comportamento di `+" "` annotato in `TODO.md`. Aggiunto un
  avviso al cap. 7.
- `SQRT` prende una cella senza segno, non un doppio: `help/sqrt.txt` e il
  commento di `inc/SQRT.f` dicevano `d -- n`, corretti in `u -- n`.
  `-4 SQRT` dà 255, senza errore.
- `>NUMBER` non riconosce il segno (`S" -5"` dà 0): la `VAL` del capitolo
  vale per i numeri senza segno, e il testo lo dice. Per il resto c'è
  `EVALUATE`.
- La stringa di `<# ... #>` dura fino alla prossima conversione:
  `12 STR$ 34 STR$ TYPE TYPE` stampa `3434`. Mostrato nel capitolo.
- Definite e provate nel capitolo: `SGN`, `STR$`, `BASE$`, `VAL`,
  `ROUND/`, `POS` (ricerca di un carattere), `LEFT$`, `RIGHT$`, `MID$`,
  `TL$`. `/STRING` è ridefinita qui perché ogni capitolo si prova da
  solo: un motivo in più per portarla in `inc/`.
- `7 REG@` in emulatore dà 3 (28 MHz): la riga è nel capitolo senza
  uscita dichiarata, perché sulla macchina dipende dalla velocità.

**Emerso scrivendo il cap. 9 (2026-10-13).**

- Il capitolo ha due metà. La virgola mobile (`lib/floating.f`) è
  descritta dal sorgente e dal tutorial 024, in otto spezzoni `no-test`:
  l'emulatore non ha il calcolatore della ROM. Le alternative intere
  (`**`, `YEARS` con `*/`, 355/113, `DSQRT` riscalata, tabella di seni)
  sono provate: 29 righe, 0 errori.
- **Da provare dall'autore su CSpect o sulla macchina**, perché scritto
  senza poterlo eseguire: (a) le uscite di `F.` dichiarate negli spezzoni
  (`3.5000e0`, `3.1416e0`, `1.4142e0`, `2.7183e0`, `0.5000e0`, `6.3000e1`,
  `1.0240e3`, `1.5708e1`, `1.9635e1`), ricavate dalla forma di `F>PAD`;
  (b) che fra `FLOATING` e `INTEGER` un numero senza punto resti un
  intero a una cella (dedotto da `FNUMBER`, che lascia `DPL` a -1, e dal
  tutorial 024 che dà `2 PLACES` in quel modo); (c) la forma `1.5E3`;
  (d) le definizioni `SAVINGS`, `CIRC`, `AREA`, `HEIGHT` con letterali in
  virgola mobile compilati.
- `F>PAD` ricava l'esponente da `FLN 10 FLN F/ F>D`: per le potenze
  esatte di 10 un logaritmo appena sotto l'intero darebbe una mantissa
  `10.0000`. Gli esempi del capitolo le evitano; è da guardare quando si
  prova la libreria.
- `FIX` in `lib/floating.f` aveva il commento `( fp -- a n )` ma è
  `F>D DROP`, cioè `( fp -- n )`; lo ripeteva il tutorial 024 (due
  righe). Corretti il 2026-10-13. Il sospetto su `F.` qui sopra è
  tracciato in `TODO.md`.
- **Il capitolo va riletto quando `FLOATING` passa a 5 byte**
  (`planners/FLOATING-5BYTE-PLAN.md`): "due celle", `2DUP`/`2SWAP`,
  `2VARIABLE` e "circa sette cifre" descrivono il modulo di oggi.
- `1000 10 YEARS` dà 1623 contro 1628,89; con la somma in decimi
  (`10000 10 YEARS`) 16284: l'esempio mostra il rimedio di portarsi dietro
  una cifra in più.

**Emerso scrivendo il cap. 10 (2026-10-13).**

- `RND` non aveva una pagina di help: scritta `help/rnd.txt`.
- `RND` non passa dalla ROM: `inc/RND.f` rifà in Z80N la formula di BASIC
  (`75*(n+1) MOD 65537 - 1`) sulla stessa variabile SEED (23670). Dopo
  `1 RANDOMIZE`, `100 RND` dà 0 17 87 58 53.
- `NEEDS RND` non carica `WITHIN`: gli spezzoni che la usano danno
  `NEEDS WITHIN`.
- Gli esempi cominciano con `1 RANDOMIZE` per avere uscite dichiarabili
  (`THROW` 1 2 e 6 4; `100 HEADS` 45; `600 THROWS` 88 94 112 88 114 104).
- `23672 @ RANDOMIZE` (seme da FRAMES) è `no-test`: in emulatore FRAMES
  resta a 0. Resta da vedere su CSpect se `%RND` e `RND (n)` di BASIC
  seguono la stessa sequenza: il capitolo afferma solo formula e variabile
  comuni con `RND`.
- Il candidato 1 della sez. 9 (tutorial sui numeri casuali) resta valido:
  "Further reading" dice che non ce n'è ancora uno.

**Rilettura dell'autore (2026-10-13).** Nel core c'è `NOT`, uguale a
`0=`: aggiunto al cap. 2 (paragrafo, tabella, rimandi) e al cap. 6.

**Le due direzioni di lettura (autore, 2026-10-14).** Concetto che vale
per ogni Forth e che la guida usava senza dirlo: il sorgente si esegue da
sinistra a destra, ma una parola prende i valori da sinistra (lo stack) e
i nomi da destra (il testo che segue), quindi certe frasi si leggono al
contrario dell'inglese. L'esempio emblematico è `DEFER PONG` (guarda a
destra) contro `' PONG2 IS PONG` (si legge da destra: "PONG is PONG2").
Messo in quattro punti: paragrafo "Left for the value, right for the
name" nel cap. 1, dopo `VALUE`/`TO`/`CONSTANT`; commento a `DEFER`/`IS`
nel cap. 4; rimando nel cap. 6; una riga in "How to read this guide" del
`README.md`. Da riprendere dove torna utile: cap. 11 (`CREATE nome`),
cap. 13 (`CHAR c`, `[CHAR] c`), cap. 19 (`INCLUDE file`, `NEEDS nome`).

Conseguenza per la matrice: la classe D si divide in **D-inc** (manca, poche
righe) e **D-lib** (manca, serve una libreria). Le D-inc sono candidate a nuovi
file in `inc/`; le D-lib vanno in `TODO.md`. (Nomi scelti per non confonderli
con le decisioni D1-D5.)
