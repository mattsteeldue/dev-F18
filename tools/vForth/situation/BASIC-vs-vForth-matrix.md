# NextBASIC contro vForth -- matrice di corrispondenza

> Stato: IN CORSO (2026-10-12). Primo giro completo sulle voci di Appendice B
> (179 righe). Restano: i concetti dei capitoli (fatti solo per il cap. 3) e la
> prova in emulatore delle righe A e B (fatta solo per il cap. 3).

Strumento di lavoro della guida `doc/BASIC-to-vForth.md`; il piano è
`planners/BASIC-TO-FORTH-PLAN.md` (fase 1). Materiale interno, in italiano.

Manuale di riferimento: `doc/zx-spectrum-next-manual-3rd-ed.md`, terza
edizione; le pagine sono quelle del PDF.

## Come leggere le tabelle

| Colonna | Contenuto |
|---|---|
| BASIC | keyword, funzione o concetto |
| Rif. manuale | capitolo e pagina della prima occorrenza nel capitolo; "App. B" se la voce è nell'elenco di Appendice B (pp. 291-295) |
| vForth | parola o idioma; dopo `--` il `NEEDS` che serve quando non è tutto nel core |
| Classe | A diretta, B idioma, C modello diverso, D-inc manca (poche righe), D-lib manca (serve una libreria), N non pertinente |
| Dove si impara | numeri dei tutorial; `-` se nessuno |
| Nota | la differenza che fa inciampare; gli omonimi sono segnalati con "Omonimo:" |
| Verifica | `emu` = spezzone provato in emulatore; vuoto = non provato |

## Cosa è verificato e cosa no

- **Esistenza delle parole: controllata.** Ogni parola Forth citata è stata
  cercata in `src/F18e.f`, `inc/` e `lib/` (file con il punto iniziale
  compresi), e il `NEEDS` è ricavato da dove sta la definizione.
- **Comportamento: provato solo per il cap. 3** (colonna Verifica). Per gli
  altri capitoli effetto sullo stack e semantica vengono dalle intestazioni dei
  sorgenti e dai file di help, non da una prova. Le righe con "Da verificare"
  nella nota sono quelle più incerte.
- **Indirizzi dei NextReg** nelle righe `REG!`: presi a memoria e dai tutorial
  040 e 056, da ricontrollare su `doc/zx-next-dev-guide-r3.md` quando si scrive
  il capitolo.
- **Pagine**: trovate cercando la keyword in grassetto nel capitolo; per le
  righe di concetto (senza keyword) la pagina manca.
- **Capitolo di appartenenza**: dove la keyword non compare nel capitolo
  atteso, la riga è stata messa nel capitolo che la tratta di più (es. `LINE`,
  `ERASE` di righe e `LIST` stanno nel cap. 19 con l'editor).

## Stato per capitolo

| Cap. | Titolo | Righe | Voci di App. B | Concetti del capitolo | Verifica |
|---|---|---|---|---|---|
| 1 | Basic Programming Concepts | 12 | fatto | da fare | da fare |
| 2 | Decisions | 3 | fatto | da fare | da fare |
| 3 | Looping | 16 | fatto | fatto | emu (tutto) |
| 4 | Procedures and Subroutines | 8 | fatto | da fare | da fare |
| 5 | READ, DATA, RESTORE | 3 | fatto | da fare | da fare |
| 6 | Expressions | 0 | nessuna voce | da fare | da fare |
| 7 | Strings | 0 | nessuna voce | da fare | da fare |
| 8 | Functions | 11 | fatto | da fare | da fare |
| 9 | Mathematical Functions | 7 | fatto | da fare | da fare |
| 10 | Random Numbers | 3 | fatto | da fare | da fare |
| 11 | Arrays | 3 | fatto | da fare | da fare |
| 12 | Conditions | 0 | nessuna voce | da fare | da fare |
| 13 | The Character Set | 3 | fatto | da fare | da fare |
| 14 | More about PRINT and INPUT | 8 | fatto | da fare | da fare |
| 15 | Colours | 16 | fatto | da fare | da fare |
| 16 | Graphics | 10 | fatto | da fare | da fare |
| 17 | Time and Motion | 11 | fatto | da fare | da fare |
| 18 | Sound and Music | 2 | fatto | da fare | da fare |
| 19 | NextZXOS and alternatives | 28 | fatto | da fare | da fare |
| 20 | Channels, Streams, Drivers and Windows | 11 | fatto | da fare | da fare |
| 21 | Optional Features | 0 | nessuna voce | da fare | da fare |
| 22 | IN, OUT and the Next Registers | 5 | fatto | da fare | da fare |
| 23 | The Memory | 16 | fatto | da fare | da fare |
| 24 | The System Variables | 0 | nessuna voce | da fare | da fare |
| 25 | Using Machine Code | 3 | fatto | da fare | da fare |

## Capitolo 1 - Basic Programming Concepts

| BASIC | Rif. manuale | vForth | Classe | Dove si impara | Nota | Verifica |
|---|---|---|---|---|---|---|
| `LET v=e` | cap. 1, p. 5; App. B | `e v !` (con `VARIABLE v`); `e TO v` (con `VALUE`); oppure nessun nome, il valore resta sullo stack | C | 005, 008 | `VARIABLE` non prende un valore iniziale e parte da 0. Molti valori che in BASIC hanno un nome in Forth vivono solo sullo stack. |  |
| `PRINT` items | cap. 1, p. 10; App. B | `.` `."` `TYPE` `EMIT` `CR` `SPACE` | B | 001, 003 | Nessun a capo automatico: `CR` va scritto. `.` consuma il numero che stampa. Niente separatori `;` e `,`. |  |
| `REM` ..., `;` ... | cap. 1, p. 10; App. B | `\ ...` fino a fine riga; `( ... )` | A | 001 | `(` vuole uno spazio dopo di sé: è una parola. |  |
| `NEW` | cap. 1, p. 9; App. B | `COLD`; `FORGET nome`; `MARKER nome` | B | 005, 022 | Non c'è un programma da cancellare: si dimenticano le definizioni fatte dopo un certo punto. |  |
| `INPUT v` | cap. 1, p. 10; App. B | `ACCEPT` poi `NUMBER` o `(NUMBER)` | B | 016, 021 | Manca una parola unica "chiedi un numero": il tutorial 016 la costruisce (`ASK-NUMBER`). Candidata D-inc. |  |
| `GO TO n` | cap. 1, p. 8; App. B | - | C | 006, 007 | Niente numeri di riga e niente salto: `IF`, cicli e definizioni. Le etichette (`@label`) seguono la stessa sorte. |  |
| `STOP` | cap. 1, p. 13; App. B | `QUIT`; `ABORT` | B | 026 | Tornano al prompt. `ABORT` svuota anche lo stack dei dati. |  |
| `CONTINUE` | cap. 1, p. 10; App. B | - | D (scelta) | - | Una parola interrotta non si riprende: la si richiama. |  |
| `LIST [n]` | cap. 1, p. 8; App. B | `n LIST` (Screen); `SEE nome`; `VIEW file`; `WORDS` -- `NEEDS SEE`, `NEEDS VIEW` | C | 022, 028 | Il sorgente sta in un file o in uno Screen, non in memoria. `SEE` decompila una parola; omonimo: `LIST` in Forth elenca uno Screen. |  |
| `RUN [n]` | cap. 1, p. 9; App. B | si digita il nome della parola | C | 005 | Ogni definizione è un comando. Non c'è `CLEAR` implicito. |  |
| `ERROR [TO e,l,s,b]` | cap. 1, p. 14; App. B | `n THROW`; `n ERROR` -- `NEEDS THROW` | B | 026, 062 | Omonimo: `ERROR ( n -- )` stampa il messaggio n e torna al prompt. Il codice arriva sullo stack da `CATCH`. |  |
| `ON ERROR` statementlist | cap. 1, p. 13; App. B | `['] parola CATCH` -- `NEEDS CATCH`, `NEEDS [']` | B | 026 | La trappola vale per l'esecuzione di una parola, non per il resto del programma; `CATCH` restituisce 0 o il codice. |  |

## Capitolo 2 - Decisions

| BASIC | Rif. manuale | vForth | Classe | Dove si impara | Nota | Verifica |
|---|---|---|---|---|---|---|
| `IF x THEN y [: ELSE z]` | cap. 2, p. 16; App. B | `x IF y ELSE z THEN` | A | 006 | La condizione viene prima di `IF`; `THEN` chiude la struttura (in BASIC la apre). Solo dentro una definizione. |  |
| `ELSE` | cap. 2, p. 16; App. B | `ELSE` | A | 006 | Vedi `IF`. |  |
| `ON x: stmt1: stmt2 ...` (selezione) | cap. 2 | `CASE n OF ... ENDOF ... ENDCASE`; `EXEC:` -- `NEEDS CASE`, `NEEDS EXEC:` | B | 013 | Non è in App. B (cap. 2, "Case selection with ON"). `EXEC:` è la tabella di salto. |  |

## Capitolo 3 - Looping

| BASIC | Rif. manuale | vForth | Classe | Dove si impara | Nota | Verifica |
|---|---|---|---|---|---|---|
| `FOR v=a TO b` ... `NEXT v` | cap. 3, p. 21; App. B | `b 1+ a DO` ... `LOOP` | A | 007 | Prima il limite, poi l'inizio; il limite è escluso. Solo dentro una definizione. | emu |
| idem, quando può girare zero volte | cap. 3 | `b 1+ a ?DO` ... `LOOP` | A | 007 | `DO` gira sempre almeno una volta (65536 giri se inizio = limite). `?DO` salta solo il caso "uguali". | emu |
| `STEP s` (s > 0) | cap. 3, p. 22; App. B | `b 1+ a DO` ... `s +LOOP` | A | 007 | Il passo sta in fondo e può cambiare a ogni giro. Solo interi. | emu |
| `STEP -s` | cap. 3 | `b a DO` ... `-s +LOOP` | A | 007 | In discesa il limite è incluso: niente `1+`. | emu |
| `STEP` frazionario | cap. 3 | contatore riscalato a interi | C | 064, 024 | Es. `101 0 DO ... 25 +LOOP` conta in centesimi. |  |
| `NEXT v` | cap. 3, p. 21; App. B | `LOOP` / `+LOOP` | A | 007 | Senza nome: chiude il `DO` più vicino. `NEXT` da comando diretto non ha equivalente. | emu |
| variabile di controllo `v` | cap. 3 | `I`; ciclo esterno `J`, `K` -- `NEEDS J`, `NEEDS K` | C | 007, 012 | Non è una variabile: vive sul return stack e dopo il ciclo non esiste più. `I'` dà il limite. | emu |
| `EXIT` (da `FOR`) | cap. 3, p. 23; App. B | `LEAVE` | A | 007 | Omonimo: `EXIT` in Forth esce dalla definizione, non dal ciclo. | emu |
| `EXIT: EXIT n` (cicli annidati) | cap. 3 | `UNLOOP UNLOOP EXIT` -- `NEEDS UNLOOP` | B | - | Un `UNLOOP` per ogni ciclo abbandonato, poi `EXIT` lascia la parola. Senza `UNLOOP` la macchina va in crash. `UNLOOP` non compare in nessun tutorial. | emu |
| `EXIT n` (esci e salta alla riga n) | cap. 3 | - | C | - | Niente righe: `EXIT` dalla parola, o un `IF` dopo il ciclo. |  |
| `REPEAT` ... `REPEAT UNTIL c` | cap. 3, p. 24; App. B | `BEGIN` ... `c UNTIL` | A | 006 | Omonimo: `REPEAT` in Forth chiude `BEGIN ... WHILE ... REPEAT`. | emu |
| `REPEAT: WHILE c` ... `REPEAT UNTIL 0` | cap. 3, p. 25; App. B | `BEGIN c WHILE` ... `REPEAT` | A | 006 | Un solo costrutto; `WHILE` può stare ovunque fra `BEGIN` e `REPEAT`. Due `WHILE` nello stesso ciclo: funziona, chiudendo con `REPEAT ... THEN`. | emu |
| `REPEAT` ... `REPEAT UNTIL 0` | cap. 3 | `BEGIN` ... `AGAIN` | A | 006 | Senza un test proprio non si ferma più. |  |
| tasto BREAK | cap. 3 | `?TERMINAL` | B | 006, 032 | BREAK non è automatico: il ciclo deve interrogare `?TERMINAL`. |  |
| `FOR` da comando diretto | cap. 3 | - | C | 005 | I cicli esistono solo in compilazione: `DO? Can't be executed.` | emu |
| cicli sovrapposti | cap. 3 | - | C | - | Rifiutati in compilazione: `LOOP? Syntax error.` | emu |

## Capitolo 4 - Procedures and Subroutines

| BASIC | Rif. manuale | vForth | Classe | Dove si impara | Nota | Verifica |
|---|---|---|---|---|---|---|
| `GO SUB n` ... `RETURN` | cap. 4, p. 27; App. B | `: nome ... ;` e poi `nome`; uscita anticipata `EXIT` | B | 005 | La subroutine ha un nome, non una riga. App. B la scrive `GOSUB`. |  |
| `RETURN` | cap. 4, p. 27; App. B | `;` oppure `EXIT` | B | 005 |  |  |
| `DEFPROC nome(par)` ... `ENDPROC [=lista]` | cap. 4, p. 29; App. B | `: nome ( par -- ris ) ... ;` | B | 005, 002 | Parametri e risultati passano sullo stack, in qualsiasi numero; il commento di stack è la dichiarazione. |  |
| `ENDPROC [= lista]` | cap. 4, p. 30; App. B | `;`; i risultati restano sullo stack | B | 005 |  |  |
| `PROC nome(expr) [TO lista]` | cap. 4, p. 30; App. B | `expr nome` | A | 005 | Gli argomenti prima del nome; nessun controllo di numero o tipo. |  |
| `LOCAL lista` | cap. 4, p. 28; App. B | `{ a b -- }` ; oppure `>R` ... `R>` -- `NEEDS LOCALS` | B | 061, 012 | I locali con nome stanno in `lib/LOCALS.f`. L'abitudine Forth è farne a meno fattorizzando. |  |
| `PRIVATE` / `PRIVATE CLEAR` | cap. 4 | - | C | 018 | Non è in App. B (cap. 4). Il sostituto più vicino sono i vocabolari. |  |
| parametri per riferimento (`REF`) | cap. 4 | si passa l'indirizzo: `v` invece di `v @` | B | 008 | Non è in App. B (cap. 4). |  |

## Capitolo 5 - READ, DATA, RESTORE

| BASIC | Rif. manuale | vForth | Classe | Dove si impara | Nota | Verifica |
|---|---|---|---|---|---|---|
| `DATA` lista | cap. 5, p. 35; App. B | `CREATE tab  n1 , n2 , ...` | B | 008, 010, 023 | I dati sono una tabella con un nome, non un flusso sparso nel programma. |  |
| `READ v1,v2,...` | cap. 5, p. 35; App. B | `tab i CELLS + @` | B | 008, 010 | Accesso per indice, in qualsiasi ordine; con `DOES>` la tabella diventa una parola che prende l'indice. |  |
| `RESTORE [n]` | cap. 5, p. 35; App. B | si azzera l'indice | B | 008 | Non c'è un puntatore DATA nascosto. |  |

## Capitolo 8 - Functions

| BASIC | Rif. manuale | vForth | Classe | Dove si impara | Nota | Verifica |
|---|---|---|---|---|---|---|
| `ABS x` | cap. 8, p. 54; App. B | `ABS`; virgola mobile `FABS` -- `NEEDS FLOATING` | A | 001, 024 |  |  |
| `DEF FN f(x)=e` | cap. 8, p. 57; App. B | `: f ( x -- y ) e ;` | B | 005 | Una funzione è una definizione come le altre. |  |
| `FN f(x)` | cap. 8, p. 57; App. B | `x f` | A | 005 |  |  |
| `INT x` | cap. 8, p. 57; App. B | interi: nessuna; virgola mobile `FINT` -- `NEEDS FLOATING` | B | 024, 015 | La divisione fra interi tronca già (`/`, `/MOD`, `FM/MOD`, `SM/REM` per scegliere l'arrotondamento). |  |
| `INT {x}` | cap. 8 | `F>D`, `FIX` -- `NEEDS FLOATING` | B | 024 | Da virgola mobile a intero (doppio). |  |
| `LEN stringa` | cap. 8, p. 53; App. B | la lunghezza è già sullo stack (`a n`); stringa contata: `COUNT` | C | 009 | Una stringa è una coppia indirizzo-lunghezza. |  |
| `SGN x` | cap. 8, p. 55; App. B | interi: `DUP 0< SWAP 0> -`; virgola mobile `FSGN` -- `NEEDS FLOATING` | B | 006 | Manca una parola per il segno di un intero: candidata D-inc. |  |
| `SGN {i}` | cap. 8 | `.` invece di `U.` | C | 001, 015 | Segno o no è una scelta di chi stampa o confronta (`<` contro `U<`), non del dato. |  |
| `STR$ x` | cap. 8, p. 53; App. B | `S>D <# #S #>` dà `a n` | B | 014 | L'uscita formattata produce una stringa; `.` la stampa soltanto. |  |
| `VAL f` | cap. 8, p. 52; App. B | numero: `NUMBER` / `>NUMBER`; espressione: `EVALUATE` -- `NEEDS >NUMBER`, `NEEDS EVALUATE` | B | 021 | `EVALUATE` interpreta testo Forth, non un'espressione infissa. |  |
| `VAL$ f` | cap. 8, p. 55; App. B | `EVALUATE` -- `NEEDS EVALUATE` | C | 021 |  |  |

## Capitolo 9 - Mathematical Functions

| BASIC | Rif. manuale | vForth | Classe | Dove si impara | Nota | Verifica |
|---|---|---|---|---|---|---|
| `SIN x`, `COS x`, `TAN x` | cap. 9, p. 60; App. B | `FSIN` `FCOS` `FTAN` -- `NEEDS FLOATING` | A | 024 | Dopo `FLOATING`; i numeri in virgola mobile occupano due celle. Radianti; `DEG>RAD`, `RAD>DEG`. |  |
| `ASN x`, `ACS x`, `ATN x` | cap. 9, p. 60; App. B | `FASIN` `FACOS` `FATAN` -- `NEEDS FLOATING` | A | - | Il tutorial 024 non le nomina. |  |
| `EXP x` | cap. 9, p. 60; App. B | `FEXP` -- `NEEDS FLOATING` | A | 024 | Omonimo: `EXP` nel core è una variabile utente dell'interprete numerico. |  |
| `LN x` | cap. 9, p. 60; App. B | `FLN` -- `NEEDS FLOATING` | A | - | Il tutorial 024 non la nomina. |  |
| `SQR x` | cap. 9, p. 60; App. B | `FSQRT`; interi: `SQRT ( d -- n )` -- `NEEDS FLOATING`, `NEEDS SQRT` | A | 024, 065 | `SQRT` vuole un doppio. |  |
| `PI` | cap. 9, p. 62; App. B | `PI` -- `NEEDS FLOATING` | A | 024 |  |  |
| `x ^ y` (potenza) | cap. 9 | `F**` -- `NEEDS FLOATING` | A | 024 | Non è in App. B (cap. 9). Fra interi non c'è. |  |

## Capitolo 10 - Random Numbers

| BASIC | Rif. manuale | vForth | Classe | Dove si impara | Nota | Verifica |
|---|---|---|---|---|---|---|
| `RANDOMIZE [n]` | cap. 10, p. 64; App. B | `n RANDOMIZE` -- `NEEDS RANDOMIZE` | A | - | Scrive la stessa variabile di sistema SEED (23670) di BASIC. Senza argomento non c'è: usare FRAMES a mano. |  |
| `RND` (fra 0 e 1) | cap. 10, p. 64; App. B | - | D-inc | 064 | Nessun casuale in virgola mobile: si scala l'intero. |  |
| `% RND i` (intero fra 0 e i-1) | cap. 10 | `i RND`; in alternativa `i CHOOSE`, `RANDOM` -- `NEEDS RND`, `NEEDS CHOOSE`, `NEEDS RANDOM` | A | - | `RND ( u -- u2 )` segue la stessa sequenza della ROM. `CHOOSE`/`RANDOM` sono quelle di Brodie. Nessun tutorial dedicato. |  |

## Capitolo 11 - Arrays

| BASIC | Rif. manuale | vForth | Classe | Dove si impara | Nota | Verifica |
|---|---|---|---|---|---|---|
| `DIM a(n)` | cap. 11, p. 67; App. B | `CREATE a  n CELLS ALLOT`; accesso `a i CELLS + @` | B | 008, 010, 023 | Indici da 0, nessun controllo dei limiti, memoria non azzerata (`ERASE`). |  |
| `DIM a(n1,...,nk)` | cap. 11 | `CREATE` ... `DOES>` con il calcolo dell'indice | B | 010 | Più dimensioni: la parola definente fa il prodotto degli indici. |  |
| `DIM a$(n,len)` | cap. 11 | `CREATE a  n len * ALLOT` | B | 009, 010 | Array di stringhe a lunghezza fissa: nessun tutorial lo mostra. |  |

## Capitolo 13 - The Character Set

| BASIC | Rif. manuale | vForth | Classe | Dove si impara | Nota | Verifica |
|---|---|---|---|---|---|---|
| `CHR$ n` | cap. 13, p. 74; App. B | `n EMIT`; `n EMITC` per i codici >= 128 | C | 003, 060 | Un carattere è il suo codice: non c'è conversione, solo stampa. |  |
| `CODE f` | cap. 13, p. 74; App. B | `a C@`; letterale: `CHAR x`, `[CHAR] x` | B | 003, 009 | Omonimo: `CODE` in Forth apre una definizione in linguaggio macchina. |  |
| `USR "a"` (indirizzo di un UDG) | cap. 13, p. 76; App. B | `c UDG@` -- `NEEDS UDG+` | B | - | In `lib/udg+.f`, con `UDG+` e `.UDG`. Nessun tutorial. |  |

## Capitolo 14 - More about PRINT and INPUT

| BASIC | Rif. manuale | vForth | Classe | Dove si impara | Nota | Verifica |
|---|---|---|---|---|---|---|
| `PRINT AT r,c;` | cap. 14, p. 82; App. B | `r c .AT` -- `NEEDS .AT` | A | 030, 031 | Stesso ordine: riga, colonna. |  |
| `PRINT TAB n;` | cap. 14, p. 82; App. B | `n .TAB` -- `NEEDS .TAB` | A | - | Nessun tutorial. |  |
| `PRINT #n, ...` | cap. 14 | `n SELECT` ... `VIDEO` | B | 003 | `SELECT` cambia lo stream corrente per tutta l'uscita successiva; `VIDEO` torna allo schermo. |  |
| `PRINT POINT x,y` | cap. 14, p. 85; App. B | - | D-inc | - | Testo a coordinate pixel: non trovato. |  |
| `INPUT LINE a$` | cap. 14, p. 91; App. B | `buf len ACCEPT` | A | 016 | Restituisce il numero di caratteri letti. |  |
| `SCREEN$ (r,c)` | cap. 14, p. 88; App. B | - | D-inc | - | Non trovata. |  |
| `INKEY$` | cap. 14, p. 93; App. B | `KEY` (aspetta); senza attesa: `?TERMINAL`, `?ESCAPE`, `KEY-DOWN?` -- `NEEDS ?ESCAPE`, `NEEDS KEYBOARD` | B | 016, 035, 051 | Non c'è `INKEY`: nel core è commentata. La lettura senza attesa passa dalla matrice (`NEEDS KEYBOARD`). |  |
| `CLS` | cap. 14, p. 89; App. B | `CLS` | A | 003, 031 |  |  |

## Capitolo 15 - Colours

| BASIC | Rif. manuale | vForth | Classe | Dove si impara | Nota | Verifica |
|---|---|---|---|---|---|---|
| `INK n` | cap. 15, p. 105; App. B | `n .INK` -- `NEEDS .INK` | A | 030 | Con `GRAPHICS` caricata la parola segue il modo grafico attivo. |  |
| `PAPER n` | cap. 15, p. 105; App. B | `n .PAPER` -- `NEEDS .PAPER` | A | 030 |  |  |
| `FLASH n` | cap. 15, p. 106; App. B | `n .FLASH` -- `NEEDS .FLASH` | A | 030 |  |  |
| `BRIGHT n` | cap. 15, p. 105; App. B | `n .BRIGHT` -- `NEEDS .BRIGHT` | A | 030 |  |  |
| `INVERSE n` | cap. 15, p. 107; App. B | `n .INVERSE` -- `NEEDS .INVERSE` | A | 031 |  |  |
| `OVER n` | cap. 15, p. 107; App. B | `n .OVER` -- `NEEDS .OVER` | A | 031 | Omonimo: `OVER` in Forth copia il secondo elemento dello stack. |  |
| `BORDER m` | cap. 15, p. 107; App. B | `m .BORDER` -- `NEEDS .BORDER` | A | 030 |  |  |
| colori permanenti (comando diretto) | cap. 15 | `.PERM` -- `NEEDS .PERM` | B | - | I colori dati con `.INK` ecc. sono temporanei finché non si chiama `.PERM`. |  |
| `ATTR (r,c)` | cap. 15, p. 108; App. B | `PIXELATT` poi `C@`; oppure `$5800 r 32 * + c + C@` -- `NEEDS GRAPHICS` | B | 031 | Solo Layer 0. |  |
| `LAYER m[,n]` | cap. 15, p. 98; App. B | `LAYER0` `LAYER10` `LAYER11` `LAYER12` `LAYER13` `LAYER2` -- `NEEDS LAYER0`, `NEEDS LAYER10`, `NEEDS LAYER11`, `NEEDS LAYER12`, `NEEDS LAYER13`, `NEEDS LAYER2` | A | 030, 037, 052 | Una parola per modo. Il modo testo di vForth è `LAYER12`: va ripristinato a fine programma. |  |
| `LAYER OVER n` | cap. 15, p. 103; App. B | `n $15 REG!` (bit 4:2) | B | 040 | Solo `REG!` diretto. |  |
| `LAYER PALETTE ...` | cap. 15, p. 103; App. B | `REG!` su `$40` `$41` `$43` `$44` | B | 056 | Solo Layer 2 nel tutorial. |  |
| `PALETTE CLEAR` | cap. 15, p. 109; App. B | - | D-inc | 056 | Il tutorial 056 riscrive la palette identità a mano. |  |
| `PALETTE DIM n` | cap. 15, p. 108; App. B | `REG!` su `$41` (8 bit) o `$44` (9 bit) | B | 056 |  |  |
| `PALETTE FORMAT n` | cap. 15, p. 108; App. B | `REG!` su `$42`, `$43` | B | 056 | Da verificare: non coperto dai tutorial. |  |
| `PALETTE OVER n` | cap. 15, p. 109; App. B | `n $14 REG!` | A | 056 |  |  |

## Capitolo 16 - Graphics

| BASIC | Rif. manuale | vForth | Classe | Dove si impara | Nota | Verifica |
|---|---|---|---|---|---|---|
| `LAYER CLEAR` | cap. 16, p. 119; App. B | - | D-inc | - | Non trovata. |  |
| `PLOT x,y` | cap. 16, p. 113; App. B | `x y PLOT` -- `NEEDS GRAPHICS` | A | 036, 038 | Attenzione alle coordinate: in vForth x è verticale (dall'alto) e y orizzontale; colore in `ATTRIB`. |  |
| `DRAW x,y` | cap. 16, p. 113; App. B | `x2 y2 x1 y1 DRAW-LINE` -- `NEEDS GRAPHICS` | B | 036 | Coordinate assolute dei due estremi: non c'è una "posizione corrente". |  |
| `DRAW x,y,z` (arco) | cap. 16 | - | D-inc | - | Non trovato. |  |
| `CIRCLE x,y,r` | cap. 16, p. 113; App. B | `x y r CIRCLE` -- `NEEDS GRAPHICS` | A | 036 |  |  |
| `POINT (x,y)`, `POINT x,y TO v` | cap. 16, p. 113; App. B | `x y POINT` -- `NEEDS GRAPHICS` | A | 038 | Restituisce il colore, non solo 0/1. |  |
| riempimento di un'area | cap. 16 | `x y PAINT` -- `NEEDS GRAPHICS` | B | 038 | Non è una keyword di BASIC: in più rispetto al manuale. |  |
| `LAYER DIM x1,y1,x2,y2` | cap. 16, p. 119; App. B | `REG!` su `$18` (Layer 2), `$1A` (ULA) | B | - | Esiste solo dentro LAYER22/LAYER24. |  |
| `LAYER ERASE x,y,w,h[,f]` | cap. 16, p. 118; App. B | - | D-inc | - | Riempimento di un rettangolo: non trovato. |  |
| `TILE ...`, `TILE BANK n`, `TILE DIM ...` | cap. 16, p. 113; App. B | - | D-lib | 058 | Tiling software su Layer 1/2: non c'è. `lib/layer3.f` e `lib/TILE80.f` sono la tilemap hardware, un'altra cosa. |  |

## Capitolo 17 - Time and Motion

| BASIC | Rif. manuale | vForth | Classe | Dove si impara | Nota | Verifica |
|---|---|---|---|---|---|---|
| `LAYER AT x,y` | cap. 17, p. 140; App. B | `REG!` su `$16`/`$17` (Layer 2), `$26`/`$27` (ULA) | B | 045 | Solo `REG!` diretto. |  |
| `PAUSE n` | cap. 17, p. 121; App. B | `n 20 * MS`; un quadro: `1FRAME` -- `NEEDS MS`, `NEEDS WAIT-KEY` | B | 032 | `MS` conta millisecondi (n < 8192) e non si interrompe con un tasto. `PAUSE 0`: `KEY DROP` o `WAIT-KEY`. |  |
| orologio (`TIME$`, RTC) | cap. 17 | `IDE_RTC`, `M_GETDATE`, `.NOW` -- `NEEDS IDE_RTC`, `NEEDS M_GETDATE`, `NEEDS .NOW` | B | - | Valori grezzi in formato MS-DOS; nessun tutorial. |  |
| `SPRITE s,x,y,i,f` | cap. 17, p. 130; App. B | `a n SPRITE-UPDATE` -- `NEEDS SPRITE` | B | 053 | Gli attributi stanno in una struttura all'indirizzo a; n è lo slot. Slot e pattern non vanno confusi. |  |
| `SPRITE BANK b[,o,p,n]` | cap. 17, p. 130; App. B | `a SPRITE-DATA>` -- `NEEDS SPRITE` | B | 053 | I pattern si caricano da memoria, non da un banco. |  |
| `SPRITE PRINT n` | cap. 17, p. 130; App. B | `SPRITES-ON` / `SPRITES-OFF` -- `NEEDS SPRITE` | A | 039 |  |  |
| `SPRITE CLEAR` | cap. 17, p. 130; App. B | `n SPRITE-HIDE` per ogni slot -- `NEEDS SPRITE` | B | 039 | Non c'è il reset globale. |  |
| `SPRITE BORDER n` | cap. 17, p. 130; App. B | `REG!` su `$15` (bit 1) | B | 040 |  |  |
| `SPRITE DIM x1,y1,x2,y2` | cap. 17, p. 132; App. B | `REG!` su `$19` | B | - |  |  |
| `SPRITE PALETTE ...` | cap. 17, p. 135; App. B | `SPRITE-PALETTE-INIT`; `REG!` su `$40`-`$44` -- `NEEDS SPRITE` | B | 053, 056 |  |  |
| movimento automatico, sprite compositi, collisioni | cap. 17 | - | D-lib | - | `lib/SPRITE.f` copre solo il minimo. |  |

## Capitolo 18 - Sound and Music

| BASIC | Rif. manuale | vForth | Classe | Dove si impara | Nota | Verifica |
|---|---|---|---|---|---|---|
| `BEEP x,y` | cap. 18, p. 144; App. B | `ms nota BEEP` -- `NEEDS BLEEP` | A | 033 | Durata in millisecondi, non in secondi; nota in semitoni dal do centrale come in BASIC. `BLEEP` è la forma grezza. |  |
| `PLAY f1[,...]` | cap. 18, p. 145; App. B | - | D-lib | 034, 050, 055 | Nessun interprete di stringhe musicali. `lib/AY.f` scrive i registri; AFX suona effetti e musiche preparati. |  |

## Capitolo 19 - NextZXOS and alternatives

| BASIC | Rif. manuale | vForth | Classe | Dove si impara | Nota | Verifica |
|---|---|---|---|---|---|---|
| `LINE start,step`, `LINE m,n TO mm,nn` | cap. 19, p. 164; App. B | - | N | - | Rinumerazione: niente numeri di riga. |  |
| `LINE MERGE first,last` | cap. 19, p. 192; App. B | - | N | - | Come sopra. |  |
| `ERASE [m,n]` | cap. 19, p. 159; App. B | `FORGET nome` | B | 004, 028 | Omonimo: `ERASE ( a n -- )` in Forth azzera n byte di memoria. |  |
| `CAT [filespec]` | cap. 19, p. 159; App. B | `DIR percorso` -- `NEEDS DIR` | A | 043 |  |  |
| `CD filespec` | cap. 19, p. 179; App. B | `CD percorso` -- `NEEDS CD` | A | 043 | Il percorso segue la parola, senza virgolette. |  |
| `PWD` | cap. 19, p. 180; App. B | `PWD` -- `NEEDS PWD` | A | 043 |  |  |
| `MKDIR filespec` | cap. 19, p. 178; App. B | `MAKEDIR percorso` -- `NEEDS MAKEDIR` | A | - | Nessun tutorial. |  |
| `RMDIR filespec` | cap. 19, p. 178; App. B | `REMOVEDIR percorso` -- `NEEDS REMOVEDIR` | A | - | Nessun tutorial. |  |
| `ERASE filespec` | cap. 19, p. 159; App. B | `UNLINK nomefile` -- `NEEDS UNLINK` | A | - | Niente caratteri jolly; nessun tutorial. |  |
| `MOVE f1,f2` | cap. 19, p. 159; App. B | `F_RENAME ( src dest -- f )` -- `NEEDS F_RENAME` | B | - | Primitiva con due z-string. Omonimo: `RENAME` in vForth rinomina una parola del dizionario, non un file. |  |
| `MOVE filespec TO attributo` | cap. 19 | `F_CHMOD` -- `NEEDS F_CHMOD` | B | - | Primitiva. |  |
| `COPY u1 TO u2` | cap. 19, p. 159; App. B | - | D-lib | - | Copia da file a file: non c'è. |  |
| `COPY u TO SCREEN$` | cap. 19 | `VIEW nomefile` -- `NEEDS VIEW` | A | 064 | Il tutorial 064 la usa di passaggio. |  |
| `LOAD f` (programma) | cap. 19, p. 158; App. B | `INCLUDE file`; `NEEDS parola`; `n LOAD` (Screen) | C | 028, 043 | Si carica sorgente, che viene compilato. Omonimo: `LOAD` in Forth interpreta uno Screen. |  |
| `LOAD f CODE m[,n]` | cap. 19 | `PAD" f" m n LOAD-BYTES` -- `NEEDS PAD"`, `NEEDS LOAD-BYTES` | A | 042 | Il nome va prima in PAD. |  |
| `LOAD f SCREEN$` | cap. 19 | `PAD" f" $4000 6912 LOAD-BYTES` -- `NEEDS LOAD-BYTES` | B | 042 |  |  |
| `LOAD f LAYER` | cap. 19 | `BMP-LOAD"`; oppure `MMU7!` + `LOAD-BYTES` pagina per pagina -- `NEEDS BMP-LOAD`, `NEEDS LOAD-BYTES` | B | 046 |  |  |
| `LOAD f BANK m` | cap. 19 | `MMU7!` + `LOAD-BYTES` (due pagine da 8K per banco) -- `NEEDS LOAD-BYTES` | B | 041, 042 |  |  |
| `LOAD f DATA a()` | cap. 19 | `LOAD-BYTES` sull'indirizzo della tabella -- `NEEDS LOAD-BYTES` | B | 042 |  |  |
| `SAVE f` (programma) | cap. 19, p. 158; App. B | - | C | 028, 059 | Il sorgente è già un file. Omonimo: `SAVE` in vForth scarica gli Screen modificati. Per congelare il sistema: `ZAP`. |  |
| `SAVE f CODE m,n` | cap. 19 | `PAD" f" m n SAVE-BYTES` -- `NEEDS SAVE-BYTES` | A | 042 | Errore se il file esiste già (`SAVE-BYTES-FORCE`). |  |
| `SAVE f SCREEN$` | cap. 19 | `PAD" f" $4000 6912 SAVE-BYTES` -- `NEEDS SAVE-BYTES` | B | 042 |  |  |
| `SAVE f BANK m` | cap. 19 | `MMU7!` + `SAVE-BYTES` -- `NEEDS SAVE-BYTES` | B | 041, 042 | `SAVE-BANK` di `lib/ZAP.f` è un'altra cosa (salva i banchi 16-19 dello heap). |  |
| `MERGE f` | cap. 19, p. 169; App. B | `INCLUDE file` | A | 043 | `INCLUDE` aggiunge sempre al dizionario. |  |
| `VERIFY f` | cap. 19, p. 168; App. B | - | N | - | Solo nastro. |  |
| `REMOUNT` | cap. 19, p. 186; App. B | `REMOUNT` -- `NEEDS REMOUNT` | A | - | Chiude anche il file dei blocchi. |  |
| `SPECTRUM ...` | cap. 19, p. 189; App. B | - | N | - | Modo 48K e snapshot. |  |
| uscita dal sistema | cap. 19 | `BYE`; `BASIC` | B | - | Da BASIC, `RUN` riprende vForth. |  |

## Capitolo 20 - Channels, Streams, Drivers and Windows

| BASIC | Rif. manuale | vForth | Classe | Dove si impara | Nota | Verifica |
|---|---|---|---|---|---|---|
| `LLIST [m]` | cap. 20, p. 207; App. B | - | D-inc | - | Da verificare se `3 SELECT` instrada l'uscita sulla stampante come lo stream 3 di BASIC. |  |
| `OPEN #n,canale` | cap. 20, p. 208; App. B | `OPEN< nomefile` (lettura), `OPEN> nomefile`; primitiva `F_OPEN` -- `NEEDS OPEN>` | B | 053, 060 | Restituiscono un handle di file, non un numero di stream. Solo in interpretazione. Finestre e canali di NextZXOS: D-lib. |  |
| `CLOSE #n` | cap. 20, p. 207; App. B | `fh F_CLOSE` | A | 042 |  |  |
| `INPUT #n` | cap. 20 | `F_GETLINE`, `F_READ` | B | 053 |  |  |
| `NEXT #n,v` | cap. 20 | `a 1 fh F_READ` | B | 053 | Un byte alla volta. |  |
| `GO TO #n,m` | cap. 20 | `d fh F_SEEK` | A | - | Posizione in doppia precisione. |  |
| `RETURN #n,v` | cap. 20 | `fh F_FGETPOS` | A | - |  |  |
| `DIM #n,v` | cap. 20 | `F_FSTAT` -- `NEEDS F_FSTAT` | B | - | Primitiva. |  |
| `LPRINT` | cap. 20, p. 206; App. B | - | D-inc | - | Come `LLIST`: da verificare `3 SELECT`. |  |
| `COPY` (stampante) | cap. 20 | - | N | - | ZX Printer. |  |
| `DRIVER drid,callid ...` | cap. 20, p. 213; App. B | - | D-inc | - | Nessuna parola per `M_DRVAPI`. |  |

## Capitolo 22 - IN, OUT and the Next Registers

| BASIC | Rif. manuale | vForth | Classe | Dove si impara | Nota | Verifica |
|---|---|---|---|---|---|---|
| `OUT m,n` | cap. 22, p. 229; App. B | `n m P!` | A | 039, 053 | Prima il valore, poi la porta. Omonimo: `OUT` nel core è una variabile utente (colonna di stampa). |  |
| `IN n` | cap. 22, p. 229; App. B | `n P@` | A | 066 |  |  |
| `REG n,v` | cap. 22, p. 229; App. B | `v n REG!` | A | 040 | Prima il valore, poi il registro. |  |
| `REG n` (funzione) | cap. 22 | `n REG@` | A | 040 |  |  |
| `RUN AT speed` | cap. 22, p. 233; App. B | `n SPEED!` (0-3); lettura `SPEED@` -- `NEEDS SPEED!`, `NEEDS SPEED@` | A | 040 |  |  |

## Capitolo 23 - The Memory

| BASIC | Rif. manuale | vForth | Classe | Dove si impara | Nota | Verifica |
|---|---|---|---|---|---|---|
| `CLEAR [n]` | cap. 23, p. 251; App. B | `FORGET nome` / `MARKER`; stack: `ABORT` | C | 005, 025 | Non ci sono variabili da azzerare in blocco. RAMTOP non si sposta: la mappa di memoria di vForth è fissa. |  |
| `LAYER BANK n,m` | cap. 23, p. 251; App. B | `REG!` su `$12`, `$13` -- `NEEDS L2-RAM-PAGE` | B | 046 | NextReg `$12` conta in banchi da 16K; `L2-RAM-PAGE` dà la prima pagina da 8K per `MMU7!`. |  |
| `POKE a,lista` | cap. 23, p. 250; App. B | `b a C!`; più valori: `C,` in una tabella e `CMOVE` | A | 008 | Prima il valore, poi l'indirizzo. |  |
| `DPOKE a,lista` | cap. 23, p. 257; App. B | `n a !` | A | 008 |  |  |
| `PEEK a` | cap. 23, p. 250; App. B | `a C@` | A | 008 |  |  |
| `DPEEK a` | cap. 23; App. B | `a @` | A | 008 |  |  |
| `PEEK$ (a,len)` | cap. 23, p. 249; App. B | `a len` è già una stringa: `TYPE`, `CMOVE` | C | 009 |  |  |
| `BANK m POKE o,lista` / `BANK m PEEK o` | cap. 23, p. 248; App. B | `pagina MMU7!` poi `C!` / `C@` a `$E000 + o` | C | 041 | BASIC conta in banchi da 16K; `MMU7!` vuole una pagina da 8K: banco m = pagine 2m e 2m+1. |  |
| `BANK m DPOKE` / `BANK m DPEEK` | cap. 23 | `MMU7!` poi `!` / `@` | C | 041 |  |  |
| `BANK m ERASE [o,l,][v]` | cap. 23 | `MMU7!` poi `FILL` | B | 041 | Due pagine per banco. |  |
| `BANK m COPY TO n`, `BANK m COPY o,l TO n,o2` | cap. 23 | `MMU7!` + `CMOVE` passando da un buffer -- `NEEDS MMU0!`, `NEEDS MMU1!` | B | 041, 054 | MMU7 mostra una pagina alla volta. `MMU0!`/`MMU1!` esistono in `inc/`; per blocchi grandi il DMA. |  |
| `BANK NEW v` | cap. 23 | - | D-inc | - | L'allocazione via `IDE_BANK` esiste solo dentro `inc/PAINT.f`. |  |
| `BANK m CLEAR` | cap. 23 | - | D-inc | - | Come sopra. |  |
| `BANK m LAYER ...` | cap. 23 | - | D-inc | - | Copia fra schermo e banco: non trovata. |  |
| `BANK 1346 FORMAT` / `USR` | cap. 23 | - | N | - | Gestione del RAMdisk. |  |
| `BANK m GOSUB/GOTO/LINE/LIST/MERGE/PROC/RESTORE` | cap. 23 | - | N | 025 | Programmi BASIC in banchi. In vForth il codice sta nel dizionario e i nomi nello heap (MMU7). |  |

## Capitolo 25 - Using Machine Code

| BASIC | Rif. manuale | vForth | Classe | Dove si impara | Nota | Verifica |
|---|---|---|---|---|---|---|
| `USR a` | cap. 25, p. 276; App. B | `n a CALL#`; codice proprio: `CODE nome ... C;` -- `NEEDS CALL#` | C | 027, 057 | `CALL#` passa n in BC e A e restituisce BC. Di norma il linguaggio macchina si scrive come parola `CODE`. Nessun tutorial su `CALL#`. |  |
| `BANK n USR o` | cap. 25 | `MMU7!` poi `CALL#` -- `NEEDS CALL#` | B | 041 |  |  |
| chiamate a NextZXOS | cap. 25 | `M_P3DOS` | B | - | Primitiva del core; nessun tutorial. |  |

## Cosa esce dalla matrice

### Correzioni alla ricognizione del piano (sez. 10)

- **`INKEY` non esiste.** In `src/F18e.f` la definizione è commentata. La
  lettura senza attesa passa da `?TERMINAL`, `?ESCAPE` o dalla matrice dei
  tasti (`KEY-DOWN?`).
- **`RENAME` non rinomina un file**: rinomina una parola del dizionario. Per i
  file c'è la primitiva `F_RENAME`.
- **`SAVE-BANK` non è un `SAVE ... BANK` generico**: fa parte di `lib/ZAP.f` e
  accetta solo i banchi 16-19 dello heap.

### Candidati `inc/` (classe D-inc)

Un "chiedi un numero" (`INPUT`), il segno di un intero (`SGN`), `SCREEN$`,
`PRINT POINT`, `LAYER ERASE`, `LAYER CLEAR`, `PALETTE CLEAR`, l'arco di `DRAW`,
`BANK NEW` / `BANK CLEAR` (allocazione di banchi), `BANK ... LAYER`, `DRIVER`,
l'uscita su stampante (`LPRINT`, `LLIST`), un casuale fra 0 e 1.

### Mancano e servirebbe una libreria (classe D-lib)

`PLAY`, il tiling software (`TILE`), la copia da file a file (`COPY`), gli
sprite oltre il minimo. A queste si aggiungono finestre e canali di NextZXOS
(riga `OPEN #`).

### Righe senza tutorial

`RANDOMIZE` / `RND` / `CHOOSE`, `UNLOOP`, `.PERM`, `.TAB`, le funzioni
trigonometriche inverse e `FLN`, `MAKEDIR` / `REMOVEDIR` / `UNLINK`, UDG (`lib/udg+.f`), orologio
(`IDE_RTC`, `M_GETDATE`, `.NOW`), `F_RENAME` / `F_CHMOD` / `F_FSTAT`,
`F_SEEK` / `F_FGETPOS`, `REMOUNT`, `CALL#` e `M_P3DOS`, `BYE` / `BASIC`,
array di stringhe. Coincidono in buona parte con l'elenco dei tutorial nuovi
del piano (sez. 9).

### Omonimi da mettere in "What changes"

`EXIT`, `REPEAT` (cap. 3); `LIST`, `ERROR`, `ERASE` (cap. 1 e 19); `LOAD`,
`SAVE`, `RENAME` (cap. 19); `OVER` (cap. 15); `CODE` (cap. 13); `EXP`
(cap. 9); `OUT` (cap. 22).

### File di help da rivedere

Trovati leggendo gli help per compilare la colonna vForth; non corretti.

- Testo che non corrisponde alla parola: `p!.txt` e `p@.txt` ("paged byte":
  sono le porte di I/O), `select.txt` ("layer or memory page": sceglie lo
  stream di uscita), `reg!.txt` e `reg@.txt` ("NextZXOS system register":
  sono i NextReg), `video.txt` ("Set video mode": riporta l'uscita
  sullo schermo, `2 SELECT`).
- Senza voce di help: `RND`, `PAINT`, `DRAW`, `DRAW-CIRCLE`, `POINT`,
  `PIXELADD`, `PIXELATT`, `IDE_RTC`, `.NOW`, `CALL#`, `UDG+`, `F_CHMOD`,
  `F_FSTAT`, `REMOUNT`, `VIEW`, `IDE_MODE!`, `PAUSEOFF`, `LAYER13`, `ZAP`, le
  parole di `lib/SPRITE.f`.
