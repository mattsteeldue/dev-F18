# Da NextBASIC a vForth: guida di migrazione, capitolo per capitolo

> Stato: IN CORSO (ripresa da: fase 1, concetti dei capitoli). Fase 0 chiusa il
> 2026-10-11. Fase 2 (capitolo pilota, cap. 3) scritta e approvata dall'autore
> per tono e contenuto, commit 72664ae. Fase 1 avviata il 2026-10-12:
> `situation/BASIC-vs-vForth-matrix.md` ha le 179 righe delle voci di
> Appendice B e, per i cap. 1-7, anche i concetti del capitolo e la prova in
> emulatore. Resta, per la fase 1: concetti e prova dei cap. 8-25 (si riparte
> dal cap. 8); per la fase 2: la prova dei listati BASIC su CSpect. Dal 2026-10-12 la guida è una
> cartella, `doc/basic-to-vforth/`, un file per capitolo (D2 rivista).

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
  eseguirli: vanno provati dall'autore su CSpect prima della pubblicazione
  (nel cap. 3: `EXIT: EXIT 80`, `REPEAT: WHILE`, `INT (n/2)`).
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
| 1 | Matrice: prima le voci di Appendice B (FATTO 2026-10-12), poi i concetti dei cap. 1-25 e la prova in emulatore (fatti i cap. 1-7) | `situation/BASIC-vs-vForth-matrix.md` | Claude, in emulatore |
| 2 | Capitolo pilota (cap. 3, Looping): fissa forma e tono -- SCRITTO 2026-10-11 e approvato; restano da provare i listati BASIC su CSpect | un capitolo della guida | autore |
| 3 | Parte linguaggio: cap. 1-14 | guida, prima parte | emulatore |
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

Conseguenza per la matrice: la classe D si divide in **D-inc** (manca, poche
righe) e **D-lib** (manca, serve una libreria). Le D-inc sono candidate a nuovi
file in `inc/`; le D-lib vanno in `TODO.md`. (Nomi scelti per non confonderli
con le decisioni D1-D5.)
