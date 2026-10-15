# NextBASIC contro vForth -- matrice di corrispondenza

> Stato: FATTO per quello che si può fare senza la macchina (2026-10-12).
> Voci di Appendice B e concetti dei capitoli: fatti per tutti e 25 i
> capitoli (scorse soltanto le parti fuori dal linguaggio: Browser, CP/M ed
> esxDOS nel cap. 19, l'elenco dei registri nel cap. 22, le strutture dati di
> BASIC nel cap. 23, la tabella del cap. 24). Prova in emulatore: fatta dove l'emulatore arriva (cap. 1-14, e
> per i cap. 17-25 tempo, file, registri, memoria, linguaggio macchina).
> Resta solo quello che si prova su CSpect o sulla macchina: l'elenco è in
> fondo, sezione "Da provare su CSpect o sulla macchina".

Strumento di lavoro della guida `doc/basic-to-vforth/`; il piano è
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
- **Comportamento: provato per i cap. 1-14** (colonna Verifica). Per gli
  altri capitoli effetto sullo stack e semantica vengono dalle intestazioni dei
  sorgenti e dai file di help, non da una prova. Le righe con "Da verificare"
  nella nota sono quelle più incerte.
- **Cosa resta senza `emu` nei cap. 1-14**: le righe C, D e N che non hanno
  uno spezzone da provare; quelle che qui non si possono provare (tutto ciò
  che passa da `FLOATING`, perché l'emulatore non ha il calcolatore della ROM,
  cioè quasi tutto il cap. 9; `EDIT` / `LED`; la posizione di stampa, i
  colori e le dimensioni dei caratteri dei cap. 13-14, perché l'emulatore
  registra i byte emessi ma non ha uno schermo; le variabili di sistema UDG,
  CHARS e FRAMES, che in emulatore valgono 0); e alcune semplicemente non
  ancora provate: `REM`, `LIST`, l'assegnazione multipla, e nel cap. 3 le
  quattro righe rimaste vuote.
- **`KEY` da solo non si prova con lo script**: senza il cursore lampeggiante
  l'emulatore non riconosce l'attesa e il giro resta fermo per minuti.
  `ACCEPT` invece funziona: la riga successiva del file fa da risposta.
- **I listati BASIC non sono provati**: i valori attesi lato BASIC vengono dal
  manuale.
- **Pagine**: per le keyword, trovate cercando la keyword in grassetto nel
  capitolo; per le righe di concetto dei cap. 8-25, ricavate dai marcatori
  `<!-- PDF page N -->` del paragrafo che tratta l'argomento. Dove non c'è un
  paragrafo preciso la riga porta solo il capitolo.
- **Cap. 15-25**: provati in emulatore `REG!` / `REG@`, `SPEED!`, `P@`,
  `C!` / `C@` / `!` / `@`, `MMU7!` / `MMU7@`, `FILL` / `CMOVE`, `UNUSED`, e
  dal secondo giro `1FRAME`, `MS`, `.FAT-DATE` / `.FAT-TIME`, il calcolo di
  `BEEP` (`BEEP-PITCH`, `BLEEP-CALC`), i file (`SAVE-BYTES`, `LOAD-BYTES`,
  `OPEN<`, `OPEN>`, `F_READ`, `F_WRITE`, `F_SEEK`, `F_FGETPOS`, `F_GETLINE`,
  `F_CLOSE`), `DUMP`, `CALL#` e una parola `CODE`. Non si provano qui:
  `NEEDS GRAPHICS` si carica ma `SETUP` e `LAYER0` finiscono in `NextZXOS DOS
  call error` (la chiamata `IDE_MODE` non è emulata); `DIR` dà `NextZXOS Read
  error`; le chiamate che passano da `M_P3DOS` (`CD`, `PWD`), il
  suono, gli sprite, il Copper e `SELECT` (la routine della ROM è uno stub).
  `IDE_RTC` invece risponde (2026-10-15: al boot `.NOW` stampa
  2045-01-07 00:14, valori senza senso ma nessun errore); FRAMES resta a 0.
  Per queste righe la colonna vForth viene dai sorgenti, letti uno per uno.
- **Registri**: i numeri dei NextReg citati nei cap. 15-25 sono stati
  ricontrollati sull'elenco del cap. 22 del manuale (pp. 234-242).
- **Capitolo di appartenenza**: dove la keyword non compare nel capitolo
  atteso, la riga è stata messa nel capitolo che la tratta di più (es. `LINE`,
  `ERASE` di righe e `LIST` stanno nel cap. 19 con l'editor).

## Stato per capitolo

| Cap. | Titolo | Righe | Voci di App. B | Concetti del capitolo | Verifica |
|---|---|---|---|---|---|
| 1 | Basic Programming Concepts | 30 | fatto | fatto | emu (19 righe) |
| 2 | Decisions | 13 | fatto | fatto | emu (12 righe) |
| 3 | Looping | 16 | fatto | fatto | emu (12 righe) |
| 4 | Procedures and Subroutines | 19 | fatto | fatto | emu (15 righe) |
| 5 | READ, DATA, RESTORE | 10 | fatto | fatto | emu (8 righe) |
| 6 | Expressions | 21 | nessuna voce | fatto | emu (18 righe), virgola mobile esclusa |
| 7 | Strings | 17 | nessuna voce | fatto | emu (12 righe) |
| 8 | Functions | 21 | fatto | fatto | emu (16 righe) |
| 9 | Mathematical Functions | 15 | fatto | fatto | emu (4 righe), virgola mobile esclusa |
| 10 | Random Numbers | 9 | fatto | fatto | emu (5 righe) |
| 11 | Arrays | 16 | fatto | fatto | emu (11 righe) |
| 12 | Conditions | 15 | nessuna voce | fatto | emu (14 righe) |
| 13 | The Character Set | 17 | fatto | fatto | emu (11 righe) |
| 14 | More about PRINT and INPUT | 21 | fatto | fatto | emu (4 righe); posizione e colori solo sulla macchina |
| 15 | Colours | 35 | fatto | fatto, teoria del colore compresa (pp. 95-103) | non provabile in emulatore: da fare su CSpect |
| 16 | Graphics | 19 | fatto | fatto | non provabile in emulatore (`GRAPHICS` non si inizializza): da fare su CSpect |
| 17 | Time and Motion | 44 | fatto | fatto | emu (5 righe: tempo e orologio); guida: 68 righe (2026-10-15); sprite, Copper e RTC su CSpect |
| 18 | Sound and Music | 21 | fatto | fatto | emu (2 righe: solo il calcolo); il suono su CSpect |
| 19 | NextZXOS and alternatives | 61 | fatto | fatto (Browser, menu NMI, CP/M ed esxDOS solo scorsi: fuori dal linguaggio) | emu (3 righe: salvare, caricare, copiare); catalogo e cartelle su CSpect |
| 20 | Channels, Streams, Drivers and Windows | 29 | fatto | fatto | emu (9 righe: file con handle); `SELECT` e finestre sulla macchina |
| 21 | Optional Features | 10 | nessuna voce | fatto | da fare sulla macchina (RTC, WiFi, acceleratore) |
| 22 | IN, OUT and the Next Registers | 20 | fatto | fatto (elenco dei registri scorso, non riga per riga) | emu (7 righe) |
| 23 | The Memory | 36 | fatto | fatto | emu (13 righe) |
| 24 | The System Variables | 8 | nessuna voce | fatto | emu (1 riga); i valori sulla macchina |
| 25 | Using Machine Code | 14 | fatto | fatto | emu (2 righe) |

## Capitolo 1 - Basic Programming Concepts

| BASIC | Rif. manuale | vForth | Classe | Dove si impara | Nota | Verifica |
|---|---|---|---|---|---|---|
| `LET v=e` | cap. 1, p. 5; App. B | `e v !` (con `VARIABLE v`); `e TO v` (con `VALUE`); oppure nessun nome, il valore resta sullo stack | C | 005, 008 | `VARIABLE` non prende un valore iniziale e parte da 0. Molti valori che in BASIC hanno un nome in Forth vivono solo sullo stack. | emu |
| `PRINT` items | cap. 1, p. 10; App. B | `.` `."` `TYPE` `EMIT` `CR` `SPACE` | B | 001, 003 | Nessun a capo automatico: `CR` va scritto. `.` consuma il numero che stampa. Niente separatori `;` e `,`. | emu |
| `REM` ..., `;` ... | cap. 1, p. 10; App. B | `\ ...` fino a fine riga; `( ... )` | A | 001 | `(` vuole uno spazio dopo di sé: è una parola. |  |
| `NEW` | cap. 1, p. 9; App. B | `COLD`; `FORGET nome`; `MARKER nome` | B | 005, 022 | Non c'è un programma da cancellare: si dimenticano le definizioni fatte dopo un certo punto. | emu |
| `INPUT v` | cap. 1, p. 10; App. B | `ACCEPT` poi `NUMBER` o `(NUMBER)` | B | 016, 021 | Manca una parola unica "chiedi un numero": il tutorial 016 la costruisce (`ASK-NUMBER`). Candidata D-inc. Una forma provata è nel cap. 14 (`INPUT#`). | emu |
| `GO TO n` | cap. 1, p. 8; App. B | - | C | 006, 007 | Niente numeri di riga e niente salto: `IF`, cicli e definizioni. Le etichette (`@label`) seguono la stessa sorte. |  |
| `STOP` | cap. 1, p. 13; App. B | `QUIT`; `ABORT` | B | 026 | Tornano al prompt. `ABORT` svuota anche lo stack dei dati. | emu |
| `CONTINUE` | cap. 1, p. 10; App. B | - | D (scelta) | - | Una parola interrotta non si riprende: la si richiama. |  |
| `LIST [n]` | cap. 1, p. 8; App. B | `n LIST` (Screen); `SEE nome`; `VIEW file`; `WORDS` -- `NEEDS SEE`, `NEEDS VIEW` | C | 022, 028 | Il sorgente sta in un file o in uno Screen, non in memoria. `SEE` decompila una parola; omonimo: `LIST` in Forth elenca uno Screen. |  |
| `RUN [n]` | cap. 1, p. 9; App. B | si digita il nome della parola | C | 005 | Ogni definizione è un comando. Non c'è `CLEAR` implicito. |  |
| `ERROR [TO e,l,s,b]` | cap. 1, p. 14; App. B | `n THROW`; `n ERROR` -- `NEEDS THROW` | B | 026, 062 | Omonimo: `ERROR ( n -- )` stampa il messaggio n e torna al prompt. Il codice arriva sullo stack da `CATCH`. | emu |
| `ON ERROR` statementlist | cap. 1, p. 13; App. B | `['] parola CATCH` -- `NEEDS CATCH`, `NEEDS [']` | B | 026 | La trappola vale per l'esecuzione di una parola, non per il resto del programma; `CATCH` restituisce 0 o il codice. | emu |
| numeri di riga, programma in memoria | cap. 1, p. 5 | sorgente in un file (`INCLUDE file`) o in uno Screen; conta l'ordine di definizione | C | 005, 028 | Una parola si usa solo dopo averla definita. Niente righe da inserire "in mezzo", niente rinumerazione. |  |
| comando diretto / riga di programma | cap. 1, p. 5 | interpretazione / compilazione fra `:` e `;` | C | 005, 019 | Quello che si digita è eseguito subito; `:` passa a compilare. Le strutture di controllo esistono solo in compilazione. | emu |
| `:` fra due istruzioni | cap. 1, p. 10 | lo spazio | C | 001 | Le parole si separano con spazi, l'a capo non conta. Omonimo: `:` apre una definizione. | emu |
| variabili numeriche globali | cap. 1, p. 6 | `VARIABLE v`; `n VALUE v`; `n CONSTANT c` -- `NEEDS VALUE`, `NEEDS TO` | B | 005, 008 | Vanno dichiarate prima dell'uso. `v` lascia l'indirizzo e serve `@`; un `VALUE` lascia il valore. | emu |
| tipi di variabile (virgola mobile, intero `%`, stringa `$`) | cap. 1, p. 6 | cella da 16 bit senza tipo; doppio e virgola mobile su 2 celle; stringa = indirizzo e lunghezza | C | 001, 015, 024, 009 | Il tipo non sta nel nome né nel dato: lo decide la parola che si applica (`.` o `U.`, `+` o `D+`). L'intero è il caso normale, non l'eccezione. |  |
| `PRINT v` | cap. 1, p. 5 | `v @ .` oppure `v ?` | A | 008 |  | emu |
| `LET a,b=10,20` (assegnazione multipla) | cap. 1, p. 6 | `10 a !  20 b !` | B | 008 | Nessuna forma multipla. |  |
| `v += e` | cap. 1, p. 7 | `e v +!`; per un `VALUE`: `e +TO v` -- `NEEDS +TO` | A | 005, 008 |  | emu |
| `-=` `*=` `/=` e gli altri | cap. 1, p. 7 | `e NEGATE v +!`; in generale `v @ e op v !` | B | 008 | Solo la somma ha una parola propria. | emu |
| etichette `@nome` | cap. 1, p. 8 | il nome di una definizione | C | 005 | Vedi `GO TO`. |  |
| editor di righe, Renumber | cap. 1, p. 8 | editor sul PC e `INCLUDE`; sulla macchina `EDIT` (Screen) e `LED` (file) -- `NEEDS EDIT`, `NEEDS LED` | C | 028, 029 |  |  |
| sostituire una riga (stesso numero) | cap. 1, p. 8 | ridefinire la parola | C | 005 | Avviso `nome has already been defined.`; la definizione vecchia resta e chi la usava continua a usarla. Per sostituirla davvero: `FORGET nome` e ricaricare il sorgente. | emu |
| le variabili restano dopo `RUN` | cap. 1, p. 9 | dizionario e stack restano fra un comando e l'altro | A | 001, 005 | `QUIT` conserva lo stack, `ABORT` lo svuota. | emu |
| `PRINT`: i separatori `;` `,` `'` | cap. 1, p. 11 | `;` nulla; `'` `CR`; `,` `n .TAB` -- `NEEDS .TAB` | B | 003 | `.` mette uno spazio dopo il numero; `n w .R` allinea a destra in w colonne, senza spazio. La colonna a metà riga non è automatica. | emu |
| `INPUT a$` | cap. 1, p. 11 | `PAD 20 ACCEPT` (il testo è in `PAD`; lascia la lunghezza più uno, vedi cap. 14) | B | 016 | Niente virgolette e nessuna espressione in ingresso: per valutare quello che si è letto, `EVALUATE`. | emu |
| tasto BREAK | cap. 1, p. 12 | `?TERMINAL` | B | 006, 032 | Vedi cap. 3: un ciclo senza test proprio si ferma solo con il reset. |  |
| rapporti (`0 OK`, `9 STOP statement, 130:1`) | cap. 1, p. 10 | `ok`; in errore `parola? messaggio.` | C | 022, 062 | Niente riga e istruzione: il rapporto nomina la parola in corso. Per un errore durante un `LOAD`, `WHERE` mostra Screen e riga -- `NEEDS WHERE`. | emu |
| `ERROR$` | cap. 1, p. 14 | `n MESSAGE` | B | 059, 062 | I testi stanno nel file dei blocchi (Screen 4-8). | emu |

## Capitolo 2 - Decisions

| BASIC | Rif. manuale | vForth | Classe | Dove si impara | Nota | Verifica |
|---|---|---|---|---|---|---|
| `IF x THEN y [: ELSE z]` | cap. 2, p. 16; App. B | `x IF y ELSE z THEN` | A | 006 | La condizione viene prima di `IF`; `THEN` chiude la struttura (in BASIC la apre). Solo dentro una definizione. | emu |
| `ELSE` | cap. 2, p. 16; App. B | `ELSE` | A | 006 | Vedi `IF`. | emu |
| `ON x: stmt1: stmt2 ...` (selezione) | cap. 2 | `CASE n OF ... ENDOF ... ENDCASE`; `EXEC:` -- `NEEDS CASE`, `NEEDS EXEC:` | B | 013 | Non è in App. B (cap. 2, "Case selection with ON"). `EXEC:` è la tabella di salto. | emu |
| relazioni `=` `<` `>` `<>` | cap. 2, p. 16 | `=` `<` `>` `<>` -- `NEEDS <>` | A | 006, 011 | Postfisse: `a b <`. Vero è -1, non 1 (cap. 6). | emu |
| `<=`, `>=` | cap. 2, p. 17 | `> 0=`, `< 0=` | B | 006 | Non ci sono come parole: candidate D-inc. | emu |
| confronto con zero | cap. 2 | `0=` `0<` `0>` | A | 006 | In più rispetto a BASIC: più corte e più veloci di `0 =`. | emu |
| `IF c THEN GO TO n` | cap. 2, p. 17 | - | C | 006 | Niente righe: il ramo si scrive fra `IF` e `THEN`. |  |
| `IF` lungo ... `END IF` (su più righe) | cap. 2, p. 18 | `IF ... ELSE ... THEN`, su quante righe si vuole | A | 006 | In Forth la forma è una sola. | emu |
| `ELSE IF` in catena | cap. 2, p. 17 | `IF` annidati, un `THEN` per ogni `IF`; oppure `EXIT` alla fine di ogni caso; oppure `CASE` -- `NEEDS CASE` | B | 006, 013 |  | emu |
| confronto fra stringhe | cap. 2, p. 16 | `a1 n1 a2 n2 COMPARE` -- `NEEDS COMPARE` | B | 009 | Dà -1, 0 o 1: 0 vuol dire "uguali", il contrario di un flag. | emu |
| operatore di selezione `n?(e0,e1,...)` | cap. 2, p. 19 | tabella: `CREATE t e0 , e1 , ...` e `n max MIN CELLS t + @` | B | 010 | Non è in App. B. Il `MIN` riproduce "oltre la fine vale l'ultima". | emu |
| `GO TO n?(...)` (salto calcolato) | cap. 2, p. 20 | `EXEC:` -- `NEEDS EXEC:` | B | 013 | Nessun controllo su n. | emu |
| `IF` da comando diretto | cap. 2, p. 16 | - | C | 005 | `IF? Can't be executed.` | emu |

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
| `GO SUB n` ... `RETURN` | cap. 4, p. 27; App. B | `: nome ... ;` e poi `nome`; uscita anticipata `EXIT` | B | 005 | La subroutine ha un nome, non una riga. App. B la scrive `GOSUB`. | emu |
| `RETURN` | cap. 4, p. 27; App. B | `;` oppure `EXIT` | B | 005 |  | emu |
| `DEFPROC nome(par)` ... `ENDPROC [=lista]` | cap. 4, p. 29; App. B | `: nome ( par -- ris ) ... ;` | B | 005, 002 | Parametri e risultati passano sullo stack, in qualsiasi numero; il commento di stack è la dichiarazione. | emu |
| `ENDPROC [= lista]` | cap. 4, p. 30; App. B | `;`; i risultati restano sullo stack | B | 005 |  | emu |
| `PROC nome(expr) [TO lista]` | cap. 4, p. 30; App. B | `expr nome` | A | 005 | Gli argomenti prima del nome; nessun controllo di numero o tipo. | emu |
| `LOCAL lista` | cap. 4, p. 28; App. B | `{ a b -- }` ; oppure `>R` ... `R>` -- `NEEDS LOCALS` | B | 061, 012 | I locali con nome stanno in `lib/LOCALS.f`. L'abitudine Forth è farne a meno fattorizzando. | emu |
| `PRIVATE` / `PRIVATE CLEAR` | cap. 4, p. 29 | `VARIABLE v` definita subito prima della parola; azzerare: `0 v !` | B | 005, 018 | Non è in App. B. La variabile resta visibile a tutti: per nasconderla servono i vocabolari (018). | emu |
| parametri per riferimento (`REF`) | cap. 4 | si passa l'indirizzo: `v` invece di `v @` | B | 008 | Non è in App. B (cap. 4). | emu |
| scavalcare le subroutine (`GO TO` prima di `DEFPROC`) | cap. 4, p. 27 | - | C | 005 | Una definizione non viene eseguita quando è letta: non c'è niente da scavalcare. |  |
| ricorsione | cap. 4, p. 28 | `RECURSE` -- `NEEDS RECURSE` | A | 061 | Il nome della parola non è ancora visibile dentro la sua definizione. Con 16 bit `8 FACT` è già oltre 32767. | emu |
| stack dei ritorni di `GO SUB` | cap. 4, p. 27 | return stack: `>R` `R>` `R@` | C | 012 | È visibile e usabile come deposito temporaneo, ma va lasciato com'era prima di `;`. |  |
| `LOCAL v=valore` (valore iniziale) | cap. 4, p. 28 | locale di uscita `{ a -- v }` (parte da 0), poi `valore TO v` -- `NEEDS LOCALS` | B | 061 | I locali dopo `--` vengono restituiti all'uscita. | emu |
| valori predefiniti dei parametri | cap. 4, p. 30 | una seconda parola che mette il valore: `: nome0  0 nome ;` | B | 005 | Il numero di argomenti di una parola è fisso. |  |
| più punti di uscita (`ENDPROC` ripetuto) | cap. 4, p. 30 | `EXIT` | A | 006 | Dentro un `DO` serve prima `UNLOOP` (cap. 3). | emu |
| più risultati: `ENDPROC =a,b` e `PROC ... TO x,y` | cap. 4, p. 30 | restano sullo stack: `17 5 /MOD` ne lascia due | A | 002, 005 | Chi chiama li consuma o li memorizza (`v !`). | emu |
| controllo dei parametri (`Q Parameter error`) | cap. 4, p. 31 | - | C | 002 | Nessun controllo: un argomento in più o in meno sbilancia lo stack senza avviso. `.S` e `DEPTH` per guardare -- `NEEDS .S`, `NEEDS DEPTH`. |  |
| parametri in numero variabile (`DATA` in `DEFPROC`) | cap. 4, p. 33 | il conteggio come ultimo argomento: `1 2 3 4 4 SUMN` | B | - |  | emu |
| `ON ERROR` locale, annidato | cap. 4, p. 33 | `CATCH` annidati -- `NEEDS CATCH`, `NEEDS THROW` | B | 026 | `THROW` risale al `CATCH` più vicino, che può rilanciare. | emu |
| `DEFPROC` solo in un programma | cap. 4, p. 31 | `:` funziona anche dal prompt | C | 005 | Al contrario di BASIC: è `IF` a non funzionare dal prompt, non la definizione. | emu |

## Capitolo 5 - READ, DATA, RESTORE

| BASIC | Rif. manuale | vForth | Classe | Dove si impara | Nota | Verifica |
|---|---|---|---|---|---|---|
| `DATA` lista | cap. 5, p. 35; App. B | `CREATE tab  n1 , n2 , ...` | B | 008, 010, 023 | I dati sono una tabella con un nome, non un flusso sparso nel programma. | emu |
| `READ v1,v2,...` | cap. 5, p. 35; App. B | `tab i CELLS + @` | B | 008, 010 | Accesso per indice, in qualsiasi ordine; con `DOES>` la tabella diventa una parola che prende l'indice. | emu |
| `RESTORE [n]` | cap. 5, p. 35; App. B | si azzera l'indice | B | 008 | Non c'è un puntatore DATA nascosto. | emu |
| `DATA` di stringhe | cap. 5, p. 35 | `CREATE t ," testo"` e poi `t COUNT TYPE` | B | 009, 010 | Stringa contata, al massimo 255 caratteri. | emu |
| `READ` dentro un `FOR` | cap. 5, p. 35 | `t n CELLS BOUNDS DO I @ ... 2 +LOOP` | B | 007, 010 |  | emu |
| `READ` in sequenza | cap. 5, p. 35 | un indice in una variabile: `t p @ CELLS + @  1 p +!` | B | 008 | Quando serve davvero il flusso di BASIC: due definizioni di una riga. | emu |
| fine dei dati (`E Out of DATA`) | cap. 5, p. 35 | - | C | 010 | Nessun controllo: oltre la fine si legge memoria qualsiasi. Il numero di elementi lo tiene il programma. |  |
| `DATA` come funzione (tipo del prossimo dato) | cap. 5, p. 36 | - | C | - | Una tabella non ha tipi: la sua struttura la conosce il programma. |  |
| dati a byte | cap. 5 | `C,` e `C@` | A | 008 | In più rispetto a BASIC: metà memoria per valori fino a 255. | emu |
| tabella che si indicizza da sola | cap. 5 | `: TABLE: CREATE DOES> SWAP CELLS + @ ;` | B | 010, 023 | Dopo `TABLE: SQ 0 , 1 , 4 , 9 ,` si scrive `3 SQ`. | emu |

## Capitolo 6 - Expressions

| BASIC | Rif. manuale | vForth | Classe | Dove si impara | Nota | Verifica |
|---|---|---|---|---|---|---|
| notazione infissa, precedenze, parentesi | cap. 6, p. 37 | notazione postfissa: `2 3 4 * +` | C | 001, 002 | Nessuna precedenza e nessuna parentesi: l'ordine di scrittura è l'ordine di calcolo. Omonimo: `(` apre un commento. | emu |
| `+` `-` `*` `/` | cap. 6, p. 37 | `+` `-` `*` `/` | A | 001 | Fra interi a 16 bit. `/` tronca verso lo zero: `-7 2 /` dà -3. | emu |
| `MOD` | cap. 6, p. 37 | `MOD`; quoziente e resto insieme: `/MOD` | A | 001 | Il resto ha il segno del dividendo: `-7 2 MOD` dà -1. | emu |
| `x*20/100` (percentuali, scalature) | cap. 6, p. 37 | `x 20 100 */` | B | 064, 065 | Prodotto intermedio a 32 bit: `30000 20 100 */` dà 6000, `30000 20 * 100 /` dà 101. | emu |
| espressioni intere `%` | cap. 6, p. 37 | il caso normale | A | 001, 015 | Stesse regole: 16 bit, da sinistra a destra, nessun controllo di overflow (`65535 1+` dà 0). | emu |
| espressioni in virgola mobile (il default di BASIC) | cap. 6, p. 37 | `F+` `F-` `F*` `F/` dopo `FLOATING` -- `NEEDS FLOATING` | C | 024 | Qui è una libreria, non il default. Mantissa a 24 bit (circa 7 cifre) contro le 9 e mezza di BASIC: i risultati non coincidono cifra per cifra (`planners/FLOATING-5BYTE-PLAN.md`). Non provabile in emulatore: manca il calcolatore della ROM. |  |
| `!` (NOT bit a bit) | cap. 6, p. 38 | `INVERT` -- `NEEDS INVERT` | A | 011 | `15 INVERT U.` dà 65520. | emu |
| `<<`, `>>` | cap. 6, p. 38 | `LSHIFT`, `RSHIFT`; di un bit `2*`, `2/` | A | 011 | `RSHIFT` è logico; `2/` conserva il segno. | emu |
| AND, OR, XOR bit a bit (`&` e simili) | cap. 6, p. 38 | `AND`, `OR`, `XOR` | A | 011 |  | emu |
| `AND`, `OR`, `NOT` logici | cap. 6, p. 38 | `AND`, `OR`, `0=` | B | 006, 011 | Omonimi: in Forth `AND` e `OR` lavorano bit a bit e danno il risultato logico solo su flag ben formati (`1 2 AND` dà 0). `NOT` qui è `0=`, non l'inversione dei bit. | emu |
| vero = 1 | cap. 6, p. 39 | vero = -1 (tutti i bit a 1) | C | 006 | Chi fa aritmetica con il risultato di un confronto deve cambiare segno (`NEGATE`) o usare `AND` come maschera. | emu |
| nomi di variabile | cap. 6, p. 39 | qualsiasi carattere tranne lo spazio; maiuscole e minuscole equivalenti | C | 005 | Anche `2001` è un nome valido: il dizionario viene consultato prima di provare a leggere un numero. Nessuna keyword riservata. `CASEON` distingue maiuscole e minuscole. | emu |
| notazione scientifica (`2.34e2`) | cap. 6, p. 40 | solo dopo `FLOATING` -- `NEEDS FLOATING` | C | 024 | Senza: `1E3? is undefined.` Da verificare la forma accettata. |  |
| il punto in un numero | cap. 6, p. 40 | `3.5` è l'intero doppio 35 | C | 015, 024 | Trappola: senza `FLOATING` il punto segna un numero a 32 bit (`DPL` ricorda dove stava). `3.5 .` stampa 0, la cella alta; `3.5 D.` stampa 35. | emu |
| interi grandi (fino a 2^32-1) | cap. 6, p. 41 | interi doppi: `100000.` `D+` `D.` `M*` `S>D` | B | 015 | Senza punto un numero oltre 65535 è troncato senza avviso: `70000 .` dà 4464. | emu |
| virgolette dentro una stringa (`""`) | cap. 6, p. 41 | `34 EMIT` | B | 003 | `."` finisce alla prima virgoletta. | emu |
| letterali `$` esadecimale e `@` binario | cap. 6, p. 41 | `$E3`, `%11100011`; oppure `HEX`, `DECIMAL`, `BINARY` -- `NEEDS BINARY` | A | 004 | Il prefisso del binario è `%`, non `@` (omonimo: `@` legge una cella di memoria). `HEX` cambia la base anche in uscita, finché non si torna a `DECIMAL`. Niente parte frazionaria. | emu |
| `INT { }`: da virgola mobile a intero e viceversa | cap. 6, p. 42 | `F>D`, `D>F`; da cella a doppio `S>D` -- `NEEDS FLOATING` | B | 024 | Le conversioni sono sempre esplicite: non c'è il "casting" automatico. |  |
| con segno e senza segno (`SGN { }`) | cap. 6, p. 45 | il dato è lo stesso, sceglie la parola: `.` o `U.`, `<` o `U<`, `/` o `UM/MOD` | C | 001, 015 | Il default è rovesciato: BASIC senza segno, Forth con segno. `-32448 U.` dà 33088, `33088 .` dà -32448. `+` `-` `*` valgono per entrambi. | emu |
| complemento a due | cap. 6, p. 46 | `NEGATE`; a mano `INVERT 1+` | A | 011 |  | emu |
| divisione per zero (`6 Number too big`) | cap. 6, p. 39 | nessun errore | C | - | `1 0 /` non segnala nulla e lascia un risultato senza senso: il controllo spetta al programma. | emu |

## Capitolo 7 - Strings

| BASIC | Rif. manuale | vForth | Classe | Dove si impara | Nota | Verifica |
|---|---|---|---|---|---|---|
| stringa letterale | cap. 7, p. 49 | `." testo"` (stampa); `S" testo"` (lascia `a n`) -- `NEEDS S"` | B | 003, 009, 021 | `S"` conserva il testo nello heap (MMU7). | emu |
| variabile stringa `a$` | cap. 7, p. 49 | `CREATE a$ ," testo"` (contata); oppure `CREATE buf n ALLOT` | C | 009 | La lunghezza massima si decide alla creazione; il primo byte è la lunghezza e `COUNT` dà `a n`. Nessuna gestione automatica della memoria. | emu |
| `LEN a$`, stringa vuota | cap. 7, p. 41 | la lunghezza è il secondo elemento di `a n`; vuota: `a 0` | C | 009 | Vedi cap. 8. | emu |
| `a$(m TO n)` | cap. 7, p. 49 | aritmetica su `a n`: `: SLICE ( a n m k -- a2 n2 ) OVER - 1+ >R 1- ROT + NIP R> ;` | B | 009 | Manca `/STRING`: candidata D-inc. Non copia: è una vista sugli stessi byte. Nessun controllo (niente `3 Subscript wrong`). | emu |
| `a$(n)` (un carattere) | cap. 7, p. 49 | `a$ n + C@` | A | 009 | In una stringa contata l'indice da 1 coincide con l'offset, perché il byte 0 è la lunghezza. | emu |
| assegnare a una sottostringa | cap. 7, p. 50 | `CMOVE` sulla zona | B | 009 | È sempre "procustea": si copiano esattamente i byte chiesti, la lunghezza non cambia. | emu |
| `a$ = "..."` con lunghezza diversa | cap. 7, p. 50 | `CMOVE` e poi riscrivere il byte di lunghezza | B | 009 | Manca una parola che lo faccia in un colpo (omonimo: `PLACE` nel core è una variabile utente). Candidata D-inc. | emu |
| concatenazione `+` | cap. 7, p. 50 | accodare in un buffer: `CMOVE` e somma delle lunghezze; nello heap `+"` -- `NEEDS +"` | B | 009 | La guida usa la via del buffer (`$+!`, cap. 7). `+"` estende solo l'ultima stringa creata nello heap; il difetto che dava una stringa sbagliata è stato corretto il 2026-10-13 (`TODO.md`). | emu |
| `a$*n` (ripetizione) | cap. 7, p. 50 | ciclo: `0 ?DO 2DUP TYPE LOOP 2DROP` | B | - | Si stampa n volte, non si costruisce una stringa nuova. | emu |
| `a$*-1` (rovesciata) | cap. 7, p. 51 | ciclo all'indietro con `C@ EMIT` | B | - |  | emu |
| `[+]` (maiuscole) | cap. 7, p. 51 | `UPPER ( c -- c2 )` su ogni carattere | B | 016 | Solo un carattere alla volta. | emu |
| `[-]` (minuscole) | cap. 7, p. 51 | - | D-inc | - | Non trovata. |  |
| `[>]` (via gli spazi finali) | cap. 7, p. 51 | `-TRAILING` | A | 009 |  | emu |
| `[<]` (via gli spazi iniziali) | cap. 7, p. 51 | - | D-inc | - | `WORD` li salta in lettura, ma non c'è una parola su `a n`. |  |
| `[(f$,r$)]` (sostituzione di caratteri) | cap. 7, p. 51 | - | D-inc | - |  |  |
| `[~]`, `[^]` (terminatore sul bit 7) | cap. 7, p. 51 | - | N | - |  |  |
| tokenizzazione `{a$}` | cap. 7, p. 51 | - | N | - | Niente token. |  |

## Capitolo 8 - Functions

| BASIC | Rif. manuale | vForth | Classe | Dove si impara | Nota | Verifica |
|---|---|---|---|---|---|---|
| `ABS x` | cap. 8, p. 56; App. B | `ABS`; virgola mobile `FABS` -- `NEEDS FLOATING` | A | 001, 024 |  | emu |
| `DEF FN f(x)=e` | cap. 8, p. 57; App. B | `: f ( x -- y ) e ;` | B | 005 | Una funzione è una definizione come le altre: `: SQ ( x -- y ) DUP * ;`. Si può definire anche dal prompt (in BASIC solo dentro un programma). | emu |
| `FN f(x)` | cap. 8, p. 57; App. B | `x f` | A | 005 | L'argomento prima del nome, senza parentesi; si compongono mettendole in fila: `2 SQ SQ` dà 16. | emu |
| `INT x` | cap. 8, p. 56; App. B | interi: nessuna; virgola mobile `FINT` -- `NEEDS FLOATING` | B | 024, 015 | La divisione fra interi tronca già, ma verso lo zero: `-7 2 /` dà -3. `INT` arrotonda verso il basso: per quello `FM/MOD` (`-7 S>D 2 FM/MOD` dà quoziente -4, resto 1); `SM/REM` è la forma che tronca. | emu |
| `INT {x}` | cap. 8, p. 58 | `F>D`, `FIX` -- `NEEDS FLOATING` | B | 024 | Da virgola mobile a intero (doppio). |  |
| `LEN stringa` | cap. 8, p. 53; App. B | la lunghezza è già sullo stack (`a n`); stringa contata: `COUNT`, o solo la lunghezza `C@` | C | 009 | Una stringa è una coppia indirizzo-lunghezza. | emu |
| `SGN x` | cap. 8, p. 55; App. B | interi: `DUP 0< SWAP 0> -`; virgola mobile `FSGN` -- `NEEDS FLOATING` | B | 006 | Manca una parola per il segno di un intero: candidata D-inc. Provato: -7, 0, 9 danno -1, 0, 1. | emu |
| `SGN {i}` | cap. 8 | `.` invece di `U.` | C | 001, 015 | Segno o no è una scelta di chi stampa o confronta (`<` contro `U<`), non del dato. |  |
| `STR$ x` | cap. 8, p. 53; App. B | `S>D <# #S #>` dà `a n`; con il segno: `DUP ABS 0 <# #S ROT SIGN #>` | B | 014 | L'uscita formattata produce una stringa; `.` la stampa soltanto. La stringa sta in un'area di lavoro sotto `PAD`: va usata o copiata subito. | emu |
| `VAL f` | cap. 8, p. 55; App. B | numero: `0 0 a u >NUMBER`, `a NUMBER`; espressione: `EVALUATE` -- `NEEDS >NUMBER`, `NEEDS EVALUATE` | B | 021 | `>NUMBER ( d a u -- d2 a2 u2 )` si ferma al primo carattere che non è una cifra e dice quanti ne restano (`12AB`: 12, restano 2). `NUMBER ( a -- d )` vuole una stringa contata seguita da uno spazio e dà errore se non è tutta un numero (`NUMBER? is undefined.`). | emu |
| `VAL$ f` | cap. 8, p. 55; App. B | `EVALUATE` -- `NEEDS EVALUATE` | C | 021 | Il testo valutato lascia sullo stack quello che vuole, anche una stringa. |  |
| ordine di calcolo fra funzioni e operatori | cap. 8, p. 52 | notazione postfissa | C | 001, 002 | Le funzioni non hanno una priorità più alta degli operatori: sono parole come le altre e si applicano nell'ordine in cui sono scritte. |  |
| `STR$ (x,base[,cifre])` | cap. 8, p. 53 | cambiare `BASE` per il tempo che serve: `: BASE$ ( u base -- a u ) BASE @ >R BASE ! 0 <# #S #> R> BASE ! ;` | B | 004, 014 | `100 16 BASE$ TYPE` dà 64, `201 16 BASE$` C9, `3 2 BASE$` 11. Solo per stampare basta `HEX .` e poi `DECIMAL`. Niente parte frazionaria. | emu |
| `IN (s$,m$[,inizio[,jolly$]])` (ricerca in una stringa) | cap. 8, p. 54 | - | D-inc | - | Non ci sono `SEARCH` né `SCAN`. Un carattere si cerca con un ciclo di due righe (provato: lo spazio in `Harry is awesome` è in posizione 6, 0 se manca); sottostringa, ricerca all'indietro e jolly sono da scrivere. Omonimo: `IN n` è la lettura di una porta (cap. 22). | emu |
| `VAL "2*3"` (espressione in una stringa) | cap. 8, p. 55 | `S" 2 3 *" EVALUATE` -- `NEEDS S"`, `NEEDS EVALUATE` | B | 021 | Il testo è Forth, quindi postfisso; può contenere qualsiasi parola, anche definizioni. | emu |
| `DEF FN` con più argomenti o senza | cap. 8, p. 57 | `: P ( x y -- n ) * 10 + ;`  `: Q ( -- n ) A @ ;` | A | 005 | Nessuna parentesi vuota da ricordare: una parola senza argomenti si scrive da sola. | emu |
| gli argomenti sono locali alla funzione | cap. 8, p. 57 | gli argomenti sono valori sullo stack, senza nome | C | 002, 061 | Non c'è niente da nascondere: l'argomento non ha un nome che possa coincidere con quello di una variabile. Chi vuole i nomi usa i locali di `lib/LOCALS.f` (cap. 4). |  |
| `DEF FN` ricorsiva | cap. 8, p. 56 | `RECURSE` -- `NEEDS RECURSE` | A | 061 | `: FACTOR ( n -- n! ) DUP 2 < IF DROP 1 ELSE DUP 1- RECURSE * THEN ;` e `5 FACTOR` dà 120. | emu |
| `LEFT$`, `RIGHT$`, `MID$`, `TL$` (da definire con `DEF FN`) | cap. 8, p. 58 | aritmetica su `a u`: `LEFT$` è `MIN`; `TL$` è `1- SWAP 1+ SWAP`; `RIGHT$ ( a u n -- a2 u2 )` è `1- OVER MIN >R R@ - SWAP R> + SWAP` | B | 009 | Come lo slicing del cap. 7: viste sugli stessi byte, senza copia. Con `/STRING` sarebbero una parola ciascuna (candidata D-inc). Provate anche sulla stringa vuota. | emu |
| funzioni in espressioni intere (`%ABS`, `%IN`, `%REG`, `%PEEK`, `%DPEEK`, `%RND`, `BIN`) | cap. 8, p. 58 | `ABS`, `P@`, `REG@`, `C@`, `@`, `RND`, prefisso `%` -- `NEEDS RND` | A | 008, 040 | In Forth sono la forma normale, non una variante veloce. `PRINT %REG 7 & BIN 00000011` diventa `7 REG@ %00000011 AND .`. Dettagli nei cap. 10, 22, 23. | emu |
| `INT (x+0.5)` (arrotondare al più vicino) | cap. 8, p. 57 | fra interi, sommare metà del divisore prima di dividere: `: ROUND/ ( n d -- q ) DUP 2/ ROT + SWAP / ;` | B | 064 | `29 10 ROUND/` dà 3, `24 10 ROUND/` dà 2. In virgola mobile `1/2 F+ FINT` (da verificare). | emu |

## Capitolo 9 - Mathematical Functions

| BASIC | Rif. manuale | vForth | Classe | Dove si impara | Nota | Verifica |
|---|---|---|---|---|---|---|
| `SIN x`, `COS x`, `TAN x` | cap. 9, p. 62; App. B | `FSIN` `FCOS` `FTAN` -- `NEEDS FLOATING` | A | 024 | Dopo `FLOATING`; i numeri in virgola mobile occupano due celle. Radianti, come in BASIC. |  |
| `ASN x`, `ACS x`, `ATN x` | cap. 9, p. 62; App. B | `FASIN` `FACOS` `FATAN` -- `NEEDS FLOATING` | A | - | Il tutorial 024 non le nomina. |  |
| `EXP x` | cap. 9, p. 61; App. B | `FEXP` -- `NEEDS FLOATING` | A | 024 | Omonimo: `EXP` nel core è una variabile utente dell'interprete numerico. |  |
| `LN x` | cap. 9, p. 61; App. B | `FLN` -- `NEEDS FLOATING` | A | - | Il tutorial 024 non la nomina. |  |
| `SQR x` | cap. 8, p. 56; App. B | `FSQRT` -- `NEEDS FLOATING` | A | 024 | Il manuale la presenta nel cap. 8. Fra interi vedi la riga `SQRT`. |  |
| `PI` | cap. 9, p. 62; App. B | `PI` -- `NEEDS FLOATING` | A | 024 |  |  |
| `x ^ y` (potenza) | cap. 9, p. 60 | `F**` -- `NEEDS FLOATING` | A | 024 | Non è in App. B. Fra interi vedi la riga sotto. |  |
| `x ^ n` con esponente intero | cap. 9, p. 60 | `: ** ( n u -- n^u ) 1 SWAP 0 ?DO OVER * LOOP NIP ;` | B | 007 | Non c'è né nel core né in `inc/`: candidata D-inc. `2 10 **` dà 1024, `2 0 **` dà 1; l'overflow è silenzioso (`2 16 **` dà 0). | emu |
| `SQR x` fra interi | cap. 8, p. 56 | `n SQRT`; da un doppio `d DSQRT` -- `NEEDS SQRT` | A | 065 | Dà la parte intera: `2 SQRT` dà 1. Per avere decimali si riscala prima: `2000000. DSQRT` dà 1414. `SQRT` prende una cella, non un doppio (`16. SQRT` dà 0): il commento `( d -- n )` in `inc/SQRT.f` è sbagliato. | emu |
| crescita esponenziale (`10*1.15^y`) | cap. 9, p. 61 | `*/` ripetuto: `: YEARS ( n y -- n2 ) 0 ?DO 115 100 */ LOOP ;` | B | 064 | `1000 5 YEARS` dà 2010 contro 2011,36: ogni giro tronca e l'errore si accumula. Per restare precisi si riscala il capitale (centesimi). | emu |
| `PI` fra interi | cap. 9, p. 62 | il rapporto 355/113 dentro `*/`: `100 355 113 */` dà 314 | B | 064 |  | emu |
| `LN x/LN a` (logaritmo in un'altra base) | cap. 9, p. 61 | `x FLN a FLN F/` -- `NEEDS FLOATING` | A | - |  |  |
| gradi e radianti | cap. 9, p. 63 | `DEG>RAD`, `RAD>DEG` -- `NEEDS FLOATING` | A | 024 | Sono l'esercizio 1 del capitolo, già pronto. |  |
| trigonometria senza virgola mobile | cap. 9 | tabella di seni (`CREATE` e `,`) e `*/`; oppure `lib/fixed88.f` -- `NEEDS FIXED88` | B | 065, 064 | È il modo normale in un gioco: la virgola mobile passa dal calcolatore della ROM ed è lenta. `FIXED88` (virgola fissa 8.8) non è provata qui. |  |
| argomento fuori dominio (`A Invalid argument`) | cap. 8, p. 56 | virgola mobile: errore #11 da `FSQRT` di un negativo, `FLN` di un numero non positivo, `FASIN`/`FACOS` fuori da -1..1; interi: nessun controllo | B | - | Dal sorgente di `lib/floating.f` (`11 ?ERROR`), non provato. |  |

## Capitolo 10 - Random Numbers

| BASIC | Rif. manuale | vForth | Classe | Dove si impara | Nota | Verifica |
|---|---|---|---|---|---|---|
| `RANDOMIZE n` | cap. 10, p. 65; App. B | `n RANDOMIZE` -- `NEEDS RANDOMIZE` | A | - | Scrive la stessa variabile di sistema SEED (23670) di BASIC: la sequenza riparte uguale, utile per il debug. | emu |
| `RANDOMIZE` (senza argomento, o 0) | cap. 10, p. 65 | `23672 @ RANDOMIZE` | B | - | L'argomento è obbligatorio: il seme "dal tempo" si prende a mano da FRAMES (23672). In emulatore FRAMES resta a 0: da provare su CSpect. |  |
| `RND` (fra 0 e 1) | cap. 10, p. 64; App. B | - | D (scelta) | 064 | Nessun casuale in virgola mobile: si chiede direttamente l'intero nell'intervallo che serve (`10000 RND` per quattro decimali). |  |
| `INT (RND*n)`, `RND (n)` | cap. 10, p. 64 | `n RND` -- `NEEDS RND` | A | - | `RND ( u -- u2 )` dà un intero fra 0 e u-1 con il generatore della ROM. Dopo `1 RANDOMIZE`, `100 RND` ripetuto dà 0 17 87 58 53 e SEED passa a 149: è la sequenza di `RND` di BASIC (0.0022735596 = 149/65536). `0 RND` dà 0. | emu |
| `% RND n` | cap. 10, p. 64 | `n RND` -- `NEEDS RND` | A | - | Stesso intervallo. Da verificare su CSpect se anche la sequenza coincide: il manuale dice che dopo `RANDOMIZE 1` `%RND 100` comincia con 97, qui il primo valore è 0. |  |
| dado: `1+INT (RND*6)` | cap. 10, p. 64 | `: DICE ( -- n ) 6 RND 1+ ;` | A | - |  | emu |
| testa o croce: `coin=%RND 2` e `ON coin` | cap. 10, p. 65 | `2 RND IF ... ELSE ... THEN` | A | 006 | 100 lanci provati: 49 e 51. | emu |
| altri generatori | cap. 10 | `RANDOM ( -- u )`, `n CHOOSE` -- `NEEDS RANDOM`, `NEEDS CHOOSE` | B | 051, 056, 062, 063 | Quelli di *Starting FORTH* (Brodie): formula diversa, stessa variabile SEED, quindi `RANDOMIZE` vale anche per loro. Non c'è in BASIC. | emu |
| `RAND` (abbreviazione di `RANDOMIZE`) | cap. 10, p. 65 | - | N | - | Niente abbreviazioni: chi la vuole definisce `: RAND RANDOMIZE ;`. |  |

## Capitolo 11 - Arrays

| BASIC | Rif. manuale | vForth | Classe | Dove si impara | Nota | Verifica |
|---|---|---|---|---|---|---|
| `DIM a(n)` | cap. 11, p. 67; App. B | `CREATE a  n CELLS ALLOT`; accesso `a i CELLS + @` | B | 008, 010, 023 | Indici da 0 (in BASIC da 1): si toglie 1 nell'accesso o si riserva un elemento in più. Nessun controllo dei limiti. | emu |
| l'array parte azzerato | cap. 11, p. 67 | `a n CELLS ERASE`; stringhe: `BLANK` | A | 008 | `ALLOT` riserva soltanto: la memoria contiene quello che c'era. | emu |
| `a(i)` come parola | cap. 11, p. 67 | parola definente: `: ARRAY ( n -- ) CREATE CELLS HERE OVER ERASE ALLOT DOES> SWAP CELLS + ;` | B | 010, 023 | `10 ARRAY M` e poi `43 3 M !`, `3 M @`: l'array prende l'indice e lascia l'indirizzo dell'elemento, buono sia per leggere sia per scrivere. | emu |
| `DIM a(n1,n2)` | cap. 11, p. 68 | `: MATRIX ( righe col -- ) CREATE DUP , * CELLS HERE OVER ERASE ALLOT DOES> >R SWAP R@ @ * + CELLS R> + 2 + ;` | B | 010 | `3 6 MATRIX C`, `7 2 5 C !`, `2 5 C @`. Il numero di colonne sta nella prima cella; più dimensioni: stesso schema, un prodotto in più. | emu |
| `DIM a$(n,len)` | cap. 11, p. 69 | `: SARRAY ( n len -- ) CREATE DUP , * HERE OVER BLANK ALLOT DOES> DUP @ >R 2 + SWAP R@ * + R> ;` | B | 009, 010 | `3 10 SARRAY A$` e `1 A$` lascia `a len` della riga. Nessun tutorial lo mostra. | emu |
| `a$(i)="..."` (assegnazione procustea) | cap. 11, p. 69 | `: S! ( a1 u1 a2 len -- ) 2DUP BLANK ROT MIN CMOVE ;` | B | 009 | Riempie di spazi e copia al massimo `len` caratteri: una stringa di 16 in una riga da 10 viene troncata senza toccare la riga accanto. | emu |
| `a$(i,k)`, `a$(i)(m TO n)` | cap. 11, p. 69 | `i A$ DROP k 1- + C@`; `i A$ DROP m 1- + n m - 1+` | B | 009 | Come lo slicing del cap. 7, su una riga dell'array. | emu |
| spazi in coda agli elementi (esercizio 2) | cap. 11, p. 70 | `-TRAILING` | A | 009 | `2 A$ -TRAILING TYPE ." ing"` stampa `maying`. | emu |
| `DIM a$(len)` (stringa a lunghezza fissa) | cap. 11, p. 69 | `CREATE a$ len ALLOT` | A | 009 | In Forth è il caso normale di una variabile stringa (cap. 7). |  |
| array interi `%a(n)` già dimensionati a 64 | cap. 11, p. 67 | - | C | 008 | Niente array predefiniti: ognuno si dichiara, della misura che serve, a celle (`CELLS`) o a byte. |  |
| `%a[n]` oltre 64 elementi, `%c[x][y]` | cap. 11, p. 68 | - | N | - | Espediente di BASIC (un array "mangia" i successivi): qui la dimensione è libera. |  |
| array di byte | cap. 11 | `CREATE b n ALLOT`; `b i + C@`, `C!` | A | 008 | In più rispetto a BASIC: metà memoria per valori fino a 255. | emu |
| indice fuori dai limiti (`3 Subscript wrong`) | cap. 11 | nessun controllo | C | 010 | `99 M @` legge memoria qualsiasi e `!` la sovrascrive, senza avviso. Chi vuole il controllo lo mette nel `DOES>`. | emu |
| `DIM` ripetuto cancella l'array | cap. 11, p. 67 | `ERASE` per azzerarlo; per cambiarne la misura `FORGET` e ridefinire | C | 005 | Una seconda `CREATE` con lo stesso nome ne fa uno nuovo e lascia il vecchio dov'è. |  |
| array e variabile con lo stesso nome | cap. 11, p. 67 | - | C | 005 | Un nome è una parola sola: l'ultima definita nasconde le precedenti. |  |
| funzione `DIM (a()[,k])` | cap. 11, p. 70 | la misura la tiene il programma: una `CONSTANT`, o una cella in testa all'array (`' C >BODY @` dà 6) | B | 010 |  | emu |

## Capitolo 12 - Conditions

| BASIC | Rif. manuale | vForth | Classe | Dove si impara | Nota | Verifica |
|---|---|---|---|---|---|---|
| relazioni unite da `AND`, `OR` | cap. 12, p. 71 | `AND`, `OR` dopo i due confronti: `x 0> y 0> AND` | A | 006, 011 | Lavorano bit a bit, ma sui flag dei confronti (0 e -1) danno il risultato logico. | emu |
| `NOT` | cap. 12, p. 71 | `0=`; `NOT` è lo stesso | A | 006 | Qui `NOT` è logico: `5 NOT` dà 0. Per invertire i bit c'è `INVERT`. | emu |
| `NOT a=b` | cap. 12, p. 71 | `a b = 0=`, oppure `a b <>` -- `NEEDS <>` | A | 006 | `>=` e `<=` come negazioni: `< 0=`, `> 0=` (cap. 2). | emu |
| leggi di De Morgan | cap. 12, p. 71 | valgono allo stesso modo | A | 011 | `a b AND 0=` equivale a `a 0= b 0= OR`. | emu |
| priorità (`OR` < `AND` < `NOT` < relazioni) | cap. 12, p. 71 | - | C | 001 | Nessuna priorità: l'ordine di scrittura. |  |
| vero vale 1 | cap. 12, p. 72 | vero vale -1 | C | 006 | `1 2 <> .` stampa -1. Per avere 1: `NEGATE`, oppure `1 AND`. Vedi cap. 6. | emu |
| `IF` accetta qualsiasi numero | cap. 12, p. 72 | lo stesso: 0 è falso, tutto il resto è vero | A | 006 |  | emu |
| `x AND y` (x se y, altrimenti 0) | cap. 12, p. 72 | `x f AND`, con f flag di un confronto | A | 011 | Più diretto che in BASIC: il flag -1 è una maschera di tutti 1. `7 5 3 > AND` dà 7, `7 3 5 > AND` dà 0. | emu |
| `x OR y` (1 se y, altrimenti x) | cap. 12, p. 72 | `IF DROP 1 THEN` | B | 006 | `OR` bit a bit non fa questo: `115 -1 OR` dà -1. | emu |
| `AND`, `OR` fra numeri che non sono flag | cap. 12, p. 72 | prima si normalizza: `0= 0=` | C | 011 | Trappola: `1 2 AND` dà 0 anche se entrambi sono "veri"; `1 0= 0= 2 0= 0= AND` dà -1. | emu |
| il maggiore di due: `(a AND a>=b)+(b AND a<b)` | cap. 12, p. 72 | `MAX`; il minore `MIN` | A | 001 |  | emu |
| `x$ AND y` (la stringa se y, altrimenti vuota) | cap. 12, p. 73 | `a u f AND` | A | 009 | Il flag maschera la lunghezza: resta `a 0`, la stringa vuota. | emu |
| ordinare due stringhe (`a$>b$`) | cap. 12, p. 73 | `COMPARE 0>` -- `NEEDS COMPARE` | B | 009 | `COMPARE` dà -1, 0 o 1 (cap. 2). | emu |
| "a diverso sia da b sia da c" (esercizio) | cap. 12, p. 73 | `a b <> a c <> AND` | A | 006 | Stessa logica di BASIC. | emu |
| appartenenza a un intervallo (`a<=x AND x<=b`) | cap. 12 | `x a b BETWEEN`; `x a b WITHIN` -- `NEEDS BETWEEN`, `NEEDS WITHIN` | A | - | In più rispetto a BASIC. `BETWEEN` include i due estremi, `WITHIN` esclude quello alto. Nessun tutorial le spiega. | emu |

## Capitolo 13 - The Character Set

| BASIC | Rif. manuale | vForth | Classe | Dove si impara | Nota | Verifica |
|---|---|---|---|---|---|---|
| `CHR$ n` | cap. 13, p. 74; App. B | `n EMIT`; `n EMITC` per i codici >= 128 e per i codici di controllo | C | 003, 060 | Un carattere è il suo codice: non c'è conversione, solo stampa. Nessun controllo sull'intervallo: `300 EMIT` stampa `,` (300 modulo 256 fa 44), niente `B Integer out of range`. | emu |
| `CODE f` | cap. 13, p. 74; App. B | `a C@`; letterale: `CHAR x`, in una definizione `[CHAR] x` | B | 003, 009 | Omonimo: `CODE` in Forth apre una definizione in linguaggio macchina. Per una stringa contata il primo carattere è `a$ 1+ C@`. | emu |
| l'insieme dei caratteri (codici 32-127) | cap. 13, p. 74 | `: CHARSET 128 32 DO I EMIT LOOP ;` | A | 003 | Stessi codici: è la ROM a disegnarli. 127 è il simbolo di copyright. | emu |
| simboli grafici (128-143) | cap. 13, p. 74 | `n EMITC` | A | 003, 060 | `EMIT` può mascherare a 7 bit: per questi codici serve `EMITC`. | emu |
| token (codici 165-255) | cap. 13, p. 75 | - | N | - | Il sorgente Forth è testo, senza token. `EMITC` di un codice di token passa dalla ROM, che lo espande come farebbe `PRINT`: da verificare sulla macchina. |  |
| `BIN 01111100` | cap. 13, p. 75 | `%01111100`; oppure `BINARY` ... `DECIMAL` -- `NEEDS BINARY` | A | 004 | Vedi cap. 6. | emu |
| `USR "a"` (indirizzo di un UDG) | cap. 13, p. 76; App. B | `CHAR S UDG@` -- `NEEDS UDG+` | B | - | In `lib/udg+.f`. `UDG@ ( c -- a )` parte dalla variabile di sistema UDG (23675), come BASIC. In emulatore la variabile vale 0: l'indirizzo vero va visto sulla macchina. Nessun tutorial. | emu |
| definire un UDG (`POKE USR "S"+n,riga`) | cap. 13, p. 76 | le otto righe in una tabella, poi una copia: `CREATE SIGMA %00000000 C, %01111100 C, ...` e `SIGMA CHAR S UDG@ 8 CMOVE` | B | 008 | `DATA` e il ciclo di `POKE` diventano `C,` e `CMOVE` (cap. 5). Manca una parola `UDG!`: una riga, candidata D-inc. | emu |
| stampare un UDG | cap. 13, p. 75 | `CHAR S UDG+ EMITC`; in una definizione `[UDG] S EMITC`; `UDGs` li mostra tutti, `c .UDG` ne disegna la matrice -- `NEEDS UDG+` | B | - | `UDG+ ( c -- c2 )` dà il codice 144-164 (`S` dà 162). `UDGize` e `Gtype` convertono e stampano una stringa intera. | emu |
| `CHR$ 8` (indietro di un posto) | cap. 13, p. 77 | `8 EMITC` | A | 031 | `." 1234" 8 EMITC ." 5"` mostra 1235. | emu |
| `CHR$ 13` (a capo) | cap. 13, p. 77 | `CR`; oppure `13 EMITC` | A | 003 |  | emu |
| `CHR$ 6` (come la virgola di `PRINT`) | cap. 13, p. 77 | `6 EMITC` | A | - | Non provato sulla macchina. |  |
| codici di controllo 16-23 | cap. 13, p. 77 | `EMITC` del codice e poi dei suoi argomenti; di norma le parole `.INK`, `.PAPER`, `.AT`, `.TAB` | A | 030, 031 | Un argomento fuori intervallo è un errore della ROM (`K Invalid colour`): si esce a BASIC, e `RUN` riprende vForth. Le parole pronte tengono gli argomenti in riga. |  |
| ordine alfabetico delle stringhe (`<`, `>`, `=`) | cap. 13, p. 78 | `COMPARE` -- `NEEDS COMPARE` | B | 009 | Trappola: di default `COMPARE` non distingue maiuscole e minuscole (`EVIL` e `evil` danno 0), mentre in BASIC `"EVIL"<"evil"`. Segue l'opzione `CASEON` / `CASEOFF` del sistema: dopo `CASEON` lo stesso confronto dà -1. La stringa più corta viene prima (`zoo` contro `zoology` dà -1). | emu |
| scambio `a$,b$=b$,a$` | cap. 13, p. 78 | `2SWAP` | A | 002 | Si scambiano le due coppie `a u` sullo stack: nessun carattere viene copiato. |  |
| set di caratteri alternativo (variabile CHARS) | cap. 13, p. 79 | `a 23606 !` | A | 008 | La stessa `POKE` di BASIC: 768 byte per i codici 32-127, e CHARS punta 256 byte prima. In emulatore la variabile vale 0. Da verificare sulla macchina. |  |
| modo grafico a caratteri (Layer 3) | cap. 13, p. 80 | `lib/layer3.f`, `lib/TILE80.f` -- `NEEDS LAYER3`, `NEEDS TILE80` | B | 058 | In BASIC il Layer 3 si raggiunge solo con `POKE` e `REG`; vForth ha una libreria. |  |

## Capitolo 14 - More about PRINT and INPUT

| BASIC | Rif. manuale | vForth | Classe | Dove si impara | Nota | Verifica |
|---|---|---|---|---|---|---|
| `PRINT AT r,c;` | cap. 14, p. 82; App. B | `r c .AT` -- `NEEDS .AT` | A | 030, 031 | Stesso ordine: riga, colonna. In emulatore si vede solo che la parola gira: la posizione va vista sulla macchina. |  |
| `PRINT TAB n;` | cap. 14, p. 88; App. B | `n .TAB` -- `NEEDS .TAB` | A | - | Nessun tutorial. Come sopra per la verifica. |  |
| `PRINT #n, ...` | cap. 14 | `n SELECT` ... `VIDEO` | B | 003 | `SELECT` cambia lo stream corrente per tutta l'uscita successiva; `VIDEO` torna allo schermo. Vedi cap. 20. |  |
| `PRINT POINT x,y` | cap. 14, p. 85; App. B | - | D-inc | - | Testo a coordinate pixel: non trovato. |  |
| `INPUT LINE a$` | cap. 14, p. 91; App. B | `buf len ACCEPT` | A | 016 | Trappola: il numero restituito è quello dei caratteri più uno (`Simon` dà 6), perché conta anche il terminatore. La lunghezza della stringa è `ACCEPT 1-`. | emu |
| `SCREEN$ (r,c)` | cap. 14, p. 88; App. B | - | D-inc | - | Non trovata. |  |
| `INKEY$` | cap. 14, p. 93; App. B | `KEY` (aspetta); senza attesa: `?TERMINAL`, `?ESCAPE`, `KEY-SCAN` -- `NEEDS ?ESCAPE`, `NEEDS KEYBOARD` | B | 016, 035, 051 | Non c'è `INKEY`: nel core è commentata. `KEY-SCAN ( -- n )` legge la matrice e dà l'indice del tasto (0-39) o 255 se nessuno è premuto: un indice, non il carattere. `?TERMINAL` dice solo se è premuto BREAK. | emu |
| `CLS` | cap. 14, p. 89; App. B | `CLS` | A | 003, 031 |  | emu |
| righe e colonne secondo il layer | cap. 14, p. 81 | lo stesso: il testo esce dalla routine della ROM (`rst $10`), quindi righe e colonne sono quelle del layer attivo | A | 030, 052 | Il modo testo normale di vForth è `LAYER12` (cap. 15). |  |
| larghezza dei caratteri (`CHR$ 30;CHR$ n`) | cap. 14, p. 82 | `30 EMITC n EMITC`; già pronte `WIDECHAR` (8) e `NARROWCHAR` (4) -- `NEEDS WIDECHAR`, `NEEDS NARROWCHAR` | A | - | Nessun tutorial le nomina. |  |
| altezza dei caratteri (`CHR$ 29;CHR$ n`) | cap. 14, p. 82 | `29 EMITC n EMITC` | A | - | Nessuna parola pronta. |  |
| `CHR$ 22`, `CHR$ 23` (AT e TAB come codici) | cap. 14, p. 92 | `22 EMITC r EMITC c EMITC` | A | 031 | È la definizione stessa di `.AT`; `.TAB` manda 23 e i due byte della colonna. |  |
| `PRINT AT` fuori schermo (`5 Out of screen`) | cap. 14, p. 83 | - | C | 031 | L'errore lo dà la ROM: si esce a BASIC e `RUN` riprende vForth. Da verificare sulla macchina. |  |
| `scroll?` e `POKE 23692,n` | cap. 14, p. 89 | `n 23692 C!` | A | 008 | Stessa variabile di sistema (SCR CT). Il comportamento di vForth a fine schermo è da verificare sulla macchina. |  |
| `CHR$ 26;CHR$ n` (inibire la richiesta di scroll) | cap. 14, p. 92 | `26 EMITC n EMITC` | A | - |  |  |
| `INPUT "testo", v` | cap. 14, p. 90 | `." testo"` e poi la lettura | B | 016 | Il messaggio è una stampa normale, dove sta il cursore. |  |
| `INPUT v` (un numero) | cap. 14, p. 90 | `: INPUT# ( -- d ) PAD 1+ 20 ACCEPT 1- PAD C! BL PAD COUNT + C! PAD NUMBER ;` | B | 016 | Manca una parola unica, candidata D-inc. `NUMBER` vuole la stringa contata chiusa da uno spazio e lascia un doppio (`DROP` per la cella singola); accetta il segno e i prefissi `$` `%`. Provata con 42 e -17. Su un testo che non è un numero dà errore e torna al prompt. | emu |
| espressioni in risposta a `INPUT` (`a+2`) | cap. 14, p. 91 | `PAD 80 ACCEPT 1- PAD SWAP EVALUATE` -- `NEEDS EVALUATE` | B | 021 | Si valuta testo Forth: `A @ 2 +`. Non provata in questa forma. |  |
| `INPUT AT`, la parte bassa dello schermo | cap. 14, p. 90 | - | C | 016 | Non c'è una zona di input separata: `ACCEPT` legge dove si trova il cursore; prima si posiziona con `.AT`. |  |
| `INPUT n` (joystick) | cap. 14, p. 93 | `31 P@` (Kempston 1), `55 P@` (Kempston 2) | B | 066 | Stessi bit: destra, sinistra, giù, su, fuoco. In emulatore la porta dà 255. |  |
| `INPUT -n` (ridefinire i tasti) | cap. 14, p. 94 | `GET-KEY KEY#>RM` e poi `KEY-PRESSED?` -- `NEEDS KEYBOARD` | B | 051 | Il "joystick di tastiera" di NextZXOS non c'è: i tasti scelti si leggono dalla matrice. |  |

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
| `ATTR (r,c)` | cap. 15, p. 108; App. B | `$5800 r 32 * + c + C@` | B | 031 | Solo Layer 0. `PIXELATT ( b a -- )` di `GRAPHICS` fa il contrario: scrive l'attributo b nella cella del pixel di indirizzo a. |  |
| `LAYER m[,n]` | cap. 15, p. 98; App. B | `LAYER0` `LAYER10` `LAYER11` `LAYER12` `LAYER13` `LAYER2` -- `NEEDS LAYER0`, `NEEDS LAYER10`, `NEEDS LAYER11`, `NEEDS LAYER12`, `NEEDS LAYER13`, `NEEDS LAYER2` | A | 030, 037, 052 | Una parola per modo. Il modo testo di vForth è `LAYER12`: va ripristinato a fine programma. |  |
| `LAYER OVER n` | cap. 15, p. 103; App. B | `$15 REG@ %11100011 AND n 2 LSHIFT OR $15 REG!` | B | 040 | Solo `REG!` diretto: gli otto ordini (0-7) stanno nei bit 4:2 del NextReg `$15`, nello stesso ordine di BASIC; gli altri bit accendono gli sprite e vanno lasciati. `SPRITES-ON` riscrive tutto il registro e riporta l'ordine a 0. |  |
| `LAYER PALETTE ...` | cap. 15, p. 103; App. B | `REG!` su `$40` `$41` `$43` `$44` | B | 056 | Solo Layer 2 nel tutorial. |  |
| `PALETTE CLEAR` | cap. 15, p. 109; App. B | - | D-inc | 056 | Il tutorial 056 riscrive la palette identità a mano. |  |
| `PALETTE DIM n` | cap. 15, p. 108; App. B | `REG!` su `$41` (8 bit) o `$44` (9 bit) | B | 056 |  |  |
| `PALETTE FORMAT n` | cap. 15, p. 108; App. B | `REG!` su `$42`, `$43` | B | 056 | Da verificare: non coperto dai tutorial. |  |
| `PALETTE OVER n` | cap. 15, p. 109; App. B | `n $14 REG!` | A | 056 |  |  |
| attributi per cella 8x8 (INK, PAPER, BRIGHT, FLASH) | cap. 15, p. 98 | lo stesso: è l'hardware; l'area degli attributi è a `$5800` | A | 030 | Il capitolo descrive la macchina, non il linguaggio: vale tale e quale. |  |
| gli otto colori di base | cap. 15, p. 105 | `_BLACK` `_BLUE` `_RED` `_MAGENTA` `_GREEN` `_CYAN` `_YELLOW` `_WHITE` -- `NEEDS GRAPHICS` | A | 036 | Costanti con il trattino basso davanti; senza `GRAPHICS` si usano i numeri 0-7. |  |
| `INK 8` (trasparente), `INK 9` (contrasto) | cap. 15, p. 106 | `8 .INK`, `9 .INK` | A | - | Da verificare: `.INK` passa l'argomento da `ATTRIB-MASK` prima di mandarlo alla ROM. |  |
| colore dentro un `PRINT` (`PRINT PAPER 6;"x"`) | cap. 15, p. 106 | `6 .PAPER ." x"` | C | 030 | Non c'è la differenza fra istruzione e elemento di `PRINT`: `.PAPER` manda il codice di controllo e vale da lì in avanti come colore temporaneo della ROM; `.PERM` lo rende permanente. Da verificare sulla macchina quando la ROM lo riporta al permanente. |  |
| codici di controllo 16-21 (`CHR$ 16+CHR$ n`) | cap. 15, p. 107 | `16 EMITC n EMITC` | A | 031 | È la definizione stessa di `.INK`. Un argomento fuori intervallo fa uscire a BASIC con `K Invalid colour` (cap. 13). |  |
| caratteri composti con `OVER 1` e `CHR$ 8` | cap. 15, p. 107 | `1 .OVER ." o" 8 EMITC 34 EMIT 0 .OVER` -- `NEEDS .OVER` | A | 031 | Non provato sulla macchina. |  |
| `INK` / `PAPER` da 0 a 255 (LoRes, Layer 2) | cap. 15, p. 106 | con `GRAPHICS` caricata: `.INK`, `.PAPER` per il testo e `c TO ATTRIB` per i pixel -- `NEEDS GRAPHICS` | B | 037, 052 | Il colore dei pixel è un `VALUE`, non un comando. |  |
| `LAYER 2,0` / `LAYER 2,1` (nascondere e mostrare il Layer 2) | cap. 15, p. 105 | bit 7 del NextReg `$69`: `$69 REG@ $80 OR $69 REG!` | B | 037 | Da verificare se `LAYER2` e `LAYER12` lo fanno già da sole. |  |
| i modi che BASIC non raggiunge (Layer 2 a 320x256 e 640x256) | cap. 14, p. 81; cap. 16, p. 120 | `LAYER22-GRAPHICS`; `LAYER24-GRAPHICS` -- `NEEDS LAYER22-GRAPHICS` | A | 052 | In più rispetto a BASIC, che li ottiene solo con `REG` e `BANK POKE`. Il 640x256 (`LAYER24`) è sperimentale: non verificato su hardware. |  |
| formato dei colori di palette (RRRGGGBB, 9 bit su due byte) | cap. 15, p. 109 | lo stesso: è l'hardware | A | 056 |  |  |
| la parte bassa dello schermo prende il colore del bordo | cap. 15, p. 106 | - | C | 030 | Non c'è una parte bassa riservata. |  |
| 512 colori, a 8 bit (RRRGGGBB) o a 9 | cap. 15, p. 95 | lo stesso: è l'hardware | A | 056 | Il colore a 8 bit va nel NextReg `$41`, quello a 9 in due scritture su `$44`. |  |
| memoria video a terzi interlacciati (`BANK 5 POKE m,v`) | cap. 15, p. 96 | `v $4000 m + C!`; l'indirizzo di un pixel: `x y PIXELADD` -- `NEEDS GRAPHICS` | A | 030, 036 | Il banco 5 di BASIC è la memoria da `$4000`: i primi 6144 byte sono i pixel, i 768 seguenti gli attributi. |  |
| il secondo file video (`BANK 5 POKE 8192+m`: HiRes, HiColour, schermo ombra) | cap. 15, p. 97 | `11 MMU7!` e poi `$E000 m +` | C | 041, 052 | Trappola: la seconda metà del banco 5 (pagina 11) non si raggiunge a `$6000`, perché lì gira vForth (origine `$6366`): va mappata in MMU7. Da verificare su CSpect; le librerie `LAYER12` e `LAYER13` lo fanno da sole. |  |
| un byte per pixel, senza attributi (LoRes, Layer 2) | cap. 15, p. 102 | `PLOT` con il colore in `ATTRIB`; a mano: `MMU7!` sulla pagina e `C!` -- `NEEDS GRAPHICS` | B | 037, 041 | Il Layer 2 a 256x192 sono sei pagine da 8K a partire da `L2-RAM-PAGE` (di norma 18). Niente FLASH né BRIGHT, come in BASIC. |  |
| le otto palette (due per ULA, Layer 2, Layer 3, sprite) | cap. 15, p. 101 | NextReg `$43`: sceglie la palette da scrivere e quella mostrata | B | 056 | Il tutorial tratta solo quella del Layer 2. |  |
| palette identità (indice = colore) | cap. 15, p. 101 | `0 $40 REG!` e `256 0 DO I $41 REG! LOOP` | B | 056 | È quello che fa `SPRITE-PALETTE-INIT` per gli sprite. Con la palette identità il byte del pixel è il colore. |  |
| colori prioritari del Layer 2 | cap. 15, p. 102 | il bit 7 del secondo byte scritto su `$44` | B | 056 | Solo `REG!` diretto. Non provato. |  |
| EnhancedULA (INK e PAPER come indici di palette) | cap. 15, p. 100 | `REG!` su `$42` e `$43` | B | 056 | Vedi `PALETTE FORMAT`. |  |

## Capitolo 16 - Graphics

| BASIC | Rif. manuale | vForth | Classe | Dove si impara | Nota | Verifica |
|---|---|---|---|---|---|---|
| `LAYER CLEAR` | cap. 15, p. 105; App. B | - | D-inc | - | Riporta ai valori iniziali banchi, modo, scorrimento e ordine dei layer: non trovata. Il manuale la presenta nel cap. 15. |  |
| `PLOT x,y` | cap. 16, p. 113; App. B | `x y PLOT` -- `NEEDS GRAPHICS` | A | 036, 038 | Attenzione alle coordinate: in vForth x è verticale (dall'alto) e y orizzontale; colore in `ATTRIB`. | emu (2026-10-15, `LAYER0` degradato) |
| `DRAW x,y` | cap. 16, p. 113; App. B | `x2 y2 x1 y1 DRAW-LINE` -- `NEEDS GRAPHICS` | B | 036 | Coordinate assolute dei due estremi: non c'è una "posizione corrente". | emu (2026-10-15, `LAYER0` degradato) |
| `DRAW x,y,z` (arco) | cap. 16 | - | D-inc | - | Non trovato. |  |
| `CIRCLE x,y,r` | cap. 16, p. 113; App. B | `x y r CIRCLE` -- `NEEDS GRAPHICS` | A | 036 |  | emu (2026-10-15, `LAYER0` degradato) |
| `POINT (x,y)`, `POINT x,y TO v` | cap. 16, p. 113; App. B | `x y POINT` -- `NEEDS GRAPHICS` | A | 038 | Sui layer a un bit dà 128 o 0 (non 1 o 0); su LoRes e Layer 2 l'indice di palette, -1 fuori schermo. | emu (2026-10-15, `LAYER0` degradato) |
| riempimento di un'area | cap. 16 | `x y PAINT` -- `NEEDS PAINT` (dopo `GRAPHICS`) | B | 038 | Non è una keyword di BASIC: in più rispetto al manuale. `GRAPHICS` non la carica (riga commentata). |  |
| `LAYER DIM x1,y1,x2,y2` | cap. 16, p. 119; App. B | `REG!` su `$18` (Layer 2), `$1A` (ULA) | B | - | Esiste solo dentro LAYER22/LAYER24. |  |
| `LAYER ERASE x,y,w,h[,f]` | cap. 16, p. 118; App. B | - | D-inc | - | Riempimento di un rettangolo: non trovato. |  |
| `TILE ...`, `TILE BANK n`, `TILE DIM ...` | cap. 16, p. 113; App. B | - | D-lib | 058 | Tiling software su Layer 1/2: non c'è. `lib/layer3.f` e `lib/TILE80.f` sono la tilemap hardware, un'altra cosa. |  |
| origine delle coordinate (in basso a sinistra su Layer 0, in alto altrove) | cap. 16, p. 113 | sempre in alto a sinistra, e il primo numero è la verticale | C | 036 | Trappola doppia: in `lib/GRAPHICS.f` x è la coordinata verticale (dall'alto) e y l'orizzontale. `PLOT bx,by` di BASIC su Layer 0 diventa `175 by - bx PLOT`. |  |
| posizione corrente (`PLOT` position) | cap. 16, p. 114 | - | C | 036 | Non esiste: `DRAW-LINE` prende i due estremi. Per il tracciato "a penna" si tiene l'ultimo punto in due `VALUE`. |  |
| colore dentro l'istruzione (`PLOT INK c;x,y`) | cap. 16, p. 115 | `c TO ATTRIB` prima di disegnare -- `NEEDS GRAPHICS` | B | 036, 038 | Resta in vigore finché non si cambia. |  |
| `PLOT OVER 1` (inverte il pixel) | cap. 16, p. 117 | `x y XPLOT` -- `NEEDS GRAPHICS` | A | 038 | Su LoRes e Layer 2 inverte il valore del pixel. |  |
| `PLOT INVERSE 1` (cancella il pixel) | cap. 16, p. 117 | `' L0-RES IS PLOTOP` prima di `PLOT`, poi `' L0-SET IS PLOTOP` -- `NEEDS GRAPHICS` | B | - | L'operatore di `PLOT` è la parola differita `PLOTOP` (di norma `L0-SET`). Vale per Layer 0 e Layer 1 a un bit per pixel; nessun tutorial lo mostra. `L0-RES` c'è solo in `lib/GRAPHICS.f`; il cap. 16 della guida definisce `UNSET` (`SWAP INVERT AND`), provata. | emu (2026-10-15) |
| punti fuori schermo (errore su Layer 0, ammessi altrove) | cap. 16, p. 114 | nessun errore: `PLOT` chiama da sé `COORD-CHECK ( x y -- x y f )` e scarta il punto | C | - | Un punto fuori dallo schermo viene ignorato in silenzio, su tutti i layer. Dai sorgenti (`L0-PLOT` in `lib/GRAPHICS.f`). |  |
| grafico di una funzione (`PLOT n,88+80*SIN (n/128*PI)`) | cap. 16, p. 113 | tabella di seni e `*/`, oppure `FLOATING` -- `NEEDS GRAPHICS` | B | 065 | Vedi cap. 9: in virgola mobile è lento. |  |
| tratteggi con un UDG a scacchiera | cap. 16, p. 118 | UDG come nel cap. 13 | B | - |  |  |
| riempire o copiare in fretta la memoria video | cap. 16, p. 118 | `FILL`, `CMOVE`; a blocchi grandi `DMA-FILL`, `DMA-COPY` -- `NEEDS DMA` | B | 054 | Per il Layer 2 la pagina da 8K va prima mappata con `MMU7!` (cap. 23). |  |

## Capitolo 17 - Time and Motion

| BASIC | Rif. manuale | vForth | Classe | Dove si impara | Nota | Verifica |
|---|---|---|---|---|---|---|
| `PAUSE n` | cap. 17, p. 121; App. B | a quadri: `: FRAMES ( n -- ) 0 ?DO 1FRAME LOOP ;`; a millisecondi: `n 20 * MS` -- `NEEDS MS` | B | 032 | `1FRAME` è nel core e aspetta l'interrupt di quadro: segue i 50 o 60 Hz come `PAUSE`. `MS` conta millisecondi (al massimo 8191, otto secondi) e tiene conto della velocità della CPU. Nessuna delle due si interrompe con un tasto. | emu |
| `PAUSE 0` (finché non si preme un tasto) | cap. 17, p. 121 | `KEY DROP`; oppure `WAIT-KEY` -- `NEEDS WAIT-KEY` | A | 016, 032 | `WAIT-KEY` aspetta prima che la tastiera sia libera e poi un tasto nuovo, senza cursore e senza consumare il carattere. |  |
| pausa che un tasto interrompe | cap. 17, p. 121 | ciclo: `: PAUSE ( n -- ) 0 ?DO 1FRAME ?TERMINAL IF LEAVE THEN LOOP ;` | B | 032, 051 | Per "un tasto qualsiasi" si interroga `KEY-SCAN` al posto di `?TERMINAL` (che vede solo BREAK). Candidata D-inc. | emu |
| tarare la pausa sul tempo di calcolo (l'orologio con `PAUSE wait`) | cap. 17, p. 121 | un `1FRAME` per giro | B | 032 | Chi aspetta il quadro è già agganciato al quadro: il tempo di calcolo non si somma, finché sta dentro i 20 ms. |  |
| 50 o 60 Hz (`REG 5`, bit 2) | cap. 17, p. 123 | `5 REG@ 4 AND` | A | 040 | Diverso da zero a 60 Hz. Serve a chi converte quadri in secondi. | emu |
| contatore dei quadri (`PEEK 23672` e seguenti) | cap. 17, p. 122 | `23672 @` (i 16 bit bassi di FRAMES) | A | 032 | Circa 21 minuti a 50 Hz prima di ripartire da 0; per i 24 bit si aggiunge `23674 C@`. In emulatore resta a 0. |  |
| `TIME` (azzera) e `TIME` (legge) | cap. 17, p. 122 | `0 23672 !  0 23674 C!` e `23672 @` | B | 032 | Nessuna parola pronta: candidata D-inc. Per misurare un tratto basta la differenza fra due letture, senza azzerare. Non è in App. B. |  |
| il contatore perde colpi (durante `BEEP`, disco, stampante) | cap. 17, p. 125 | lo stesso | A | 032 | FRAMES lo aggiorna l'interrupt della ROM: si ferma quando gli interrupt sono disabilitati, in BASIC come in vForth. Per il tempo vero c'è l'RTC. |  |
| `TIME$` | cap. 17, p. 123 | `.NOW` -- `NEEDS .NOW` | B | - | Stampa `aaaa-mm-gg hh:mm`: i secondi mancano (in `inc/.FAT-TIME.f` la riga è commentata) e non c'è una forma che lasci la stringa (`a u`): candidata D-inc. Nessun tutorial. Senza modulo RTC i valori sono 0. Non è in App. B. |  |
| ore, minuti e secondi (`VAL` su pezzi di `TIME$`) | cap. 17, p. 124 | `IDE_RTC ( -- 100mi ora data )`; dall'ora: `11 RSHIFT` (ore), `5 RSHIFT 63 AND` (minuti), `31 AND 2*` (secondi, a coppie) -- `NEEDS IDE_RTC` | B | - | Niente stringa da affettare: data e ora arrivano come campi di bit in formato MS-DOS (anno dal 1980 nei 7 bit alti della data). `.FAT-DATE` e `.FAT-TIME` li stampano (provate con valori fissi: `22186 .FAT-DATE` dà 2023-05-10, `34544 .FAT-TIME` dà 16:55). | emu |
| il secondo esatto | cap. 17, p. 124 | `M_GETDATE ( -- data ora hs f )` -- `NEEDS M_GETDATE` | B | - | Il byte alto di `hs` sono i secondi (precisione di un secondo), il basso i centesimi o `$FF`; f è 0 se l'RTC ha risposto. Da provare sulla macchina. |  |
| `.time` e `.date` catturati con `OPEN #2,"v>t$"` | cap. 17, p. 122 | `.NOW` -- `NEEDS .NOW` | C | - | Da vForth non si lancia un comando punto e non serve catturarne l'uscita: si chiama NextZXOS (`IDE_RTC`) e i valori arrivano sullo stack. |  |
| `INKEY$` (macchina da scrivere, ciclo di controllo) | cap. 17, p. 125 | con attesa: `BEGIN KEY DUP EMIT 13 = UNTIL`; senza attesa: `KEY-SCAN`, `n KEY-DOWN?` -- `NEEDS KEYBOARD` | B | 016, 035, 051 | Vedi cap. 14. In un gioco si legge la matrice dei tasti a ogni quadro, non il carattere. |  |
| fotogrammi letti da disco (`SAVE` / `LOAD ... CODE`, `LOAD ... LAYER`) | cap. 17, p. 125 | `PAD" nome" a n LOAD-BYTES`; BMP `BMP-LOAD"` -- `NEEDS LOAD-BYTES`, `NEEDS BMP-LOAD` | B | 042, 046 | Il nome con il numero del fotogramma si compone a mano (`<# #S #>` e `CMOVE` in `PAD`): non c'è la concatenazione di BASIC. Un Layer 2 da 48K sono sei pagine da 8K, una `LOAD-BYTES` ciascuna dopo `MMU7!`. Anche il RAMdisk (`m:`) è un'unità come le altre. |  |
| fotogrammi tenuti in memoria (`BANK 9 COPY TO n`) | cap. 17, p. 127 | `MMU7!` e `CMOVE` (o `DMA-COPY`); doppio buffer con `REG!` su `$12` e `$13` -- `NEEDS DMA` | B | 041, 054 | Il banco 9 di BASIC sono le pagine 18 e 19. Invece di copiare 48K si può cambiare il banco mostrato (NextReg `$12`, in banchi da 16K): è un `REG!` solo. |  |
| `BANK n LAYER x,y,w,h TO ...` (rettangolo fra schermo e banco) | cap. 17, p. 128 | - | D-inc | - | Vedi cap. 23. |  |
| il sistema degli sprite (128 sprite, 64 pattern a 8 bit, 16x16) | cap. 17, p. 128 | lo stesso: è l'hardware | A | 039, 053 | I pattern a 4 bit, che BASIC non usa, da vForth sono raggiungibili (porte e NextReg), ma `lib/SPRITE.f` non li tratta. |  |
| creare un pattern (`DATA`, `BANK NEW`, `BANK POKE`) | cap. 17, p. 128 | 256 byte in una tabella (`CREATE` e `C,`), poi `tab SPRITE-BUFFER 256 CMOVE` e `p SPRITE-INIT` -- `NEEDS SPRITE` | B | 053 | Non serve un banco: il pattern va dalla memoria principale alla RAM degli sprite. 227 (`$E3`) è il trasparente, come in BASIC. |  |
| pattern in un file (`SAVE "x.spr" BANK a,0,256`) | cap. 17, p. 130 | `SAVE-BYTES` / `LOAD-BYTES` su `SPRITE-BUFFER` -- `NEEDS SAVE-BYTES`, `NEEDS LOAD-BYTES` | B | 053 | Il tutorial 053 mostra una `SPRITE-LOAD<` che legge un file `.spr` di 64 pattern; non fa parte della libreria. |  |
| `SPRITE CLEAR` | cap. 17, p. 130; App. B | `n SPRITE-HIDE` per ogni slot -- `NEEDS SPRITE` | B | 039 | Non c'è il reset globale. |  |
| `SPRITE BANK b[,o,p,n]` | cap. 17, p. 131; App. B | `p SPRITE-INIT` per ogni pattern (manda `SPRITE-BUFFER`); la primitiva è `a SPRITE-DATA>` -- `NEEDS SPRITE` | B | 053 | I pattern si caricano da memoria, uno alla volta, non da un banco intero. |  |
| `SPRITE PRINT n` | cap. 17, p. 131; App. B | `SPRITES-ON` / `SPRITES-OFF` -- `NEEDS SPRITE` | A | 039, 053 | `SPRITES-ON` fa di più: palette identità, trasparente `$E3`, e scrive 3 nel NextReg `$15` (sprite accesi e sopra il bordo), azzerando i bit di priorità dei layer. |  |
| `SPRITE s,x,y,p,f` | cap. 17, p. 131; App. B | si riempie la struttura e si manda: `x SPRITE _xcoord !  y SPRITE _ycoord !  p SPRITE _spriteid !  SPRITE s SPRITE-UPDATE` -- `NEEDS SPRITE` | B | 053 | Omonimo: `SPRITE` in `lib/SPRITE.f` è la struttura di lavoro, non un comando. `_spriteid` è il pattern, lo slot è l'argomento di `SPRITE-UPDATE`: non vanno confusi. Ogni volta partono tutti gli attributi: non c'è il "parametro omesso resta com'era". |  |
| flag di `SPRITE`: visibile, rotazione, specchi | cap. 17, p. 131 | `SPRITE-ROT SPRITE-HFLIP OR SPRITE _rotmir C!`; nascondere: `s SPRITE-HIDE` -- `NEEDS SPRITE` | A | 053 | Stessi bit di BASIC (1 rotazione, 2 specchio Y, 3 specchio X). `SPRITE-UPDATE` accende sempre il bit di visibilità. |  |
| flag di `SPRITE`: scostamento di palette (bit 4-7) | cap. 17, p. 131, 136 | il nibble alto del campo `_pattern` | B | 053 | Il nome inganna: `_pattern` è lo scostamento di palette. La struttura va azzerata con `ERASE` dopo `ALLOT`: un nibble sporco sposta tutti i colori. |  |
| `SPRITE ...,rf,mx,my` (ingrandimento 2x, 4x, 8x) | cap. 17, p. 131 | - | D-inc | - | `SPRITE-UPDATE` manda quattro attributi; ingrandimento e sprite relativi stanno nel quinto. Da verificare sulla macchina: il bit 6 dell'attributo 3 (`$C0`) annuncia un quinto byte che poi non parte. |  |
| coordinate degli sprite (320x256, lo schermo comincia a 32,32) | cap. 17, p. 132 | lo stesso: è l'hardware | A | 053 | La x è a 9 bit: `_xcoord` è una cella e `SPRITE-UPDATE` mette il bit alto nell'attributo 2. |  |
| `SPRITE BORDER n` | cap. 17, p. 132; App. B | bit 1 del NextReg `$15` | B | 040 | `SPRITES-ON` lo accende già. |  |
| `SPRITE DIM x1,y1,x2,y2` | cap. 17, p. 132; App. B | quattro `REG!` di fila su `$19`, nell'ordine x1, x2, y1, y2 | B | - | L'ordine dell'hardware non è quello di BASIC. Non ha effetto con gli sprite sopra il bordo, come in BASIC. Non provato. |  |
| animare uno sprite (alternare i pattern) | cap. 17, p. 132 | stesso slot, pattern diverso in `_spriteid`, poi `SPRITE-UPDATE` | B | 053 | Lo slot si sceglie con la porta `$303B`, il pattern sta nei bit 5:0 dell'attributo 3: scambiarli accende sprite in più. |  |
| muovere uno sprite | cap. 17, p. 134 | aggiornare `_xcoord` e `_ycoord` e chiamare `SPRITE-UPDATE` a ogni quadro (`1FRAME`) | B | 039, 053 |  |  |
| traiettoria a seno precalcolata (`%a[f]=...SIN...`) | cap. 17, p. 135 | tabella di seni con `CREATE` e `,` | B | 065, 010 | Stessa tecnica: in BASIC la tabella si calcola all'avvio, in Forth si può anche scriverla già calcolata nel sorgente. Vedi cap. 9. |  |
| `SPRITE PALETTE n[,i,v]`, `SPRITE PALETTE n BANK b,o` | cap. 17, p. 135; App. B | `SPRITE-PALETTE-INIT` (identità); a mano: `%00100000 $43 REG!` (prima palette degli sprite), `i $40 REG!`, `v $41 REG!` -- `NEEDS SPRITE` | B | 053, 056 | Il valore a 9 bit va in due scritture su `$44`. Una palette intera è un ciclo di `REG!` da una tabella. |  |
| sprite relativi, compositi e unificati (`SPRITE -1,...`) | cap. 17, p. 136 | - | D-lib | - | Servono il quinto attributo e la gestione dell'ancora: nella struttura c'è un campo `_anchor`, non usato. |  |
| batching (`SPRITE STOP`, `SPRITE MOVE`, `SPRITE MOVE INT`, `SPRITE RUN`) | cap. 17, p. 137 | `1FRAME` e subito dopo tutte le `SPRITE-UPDATE` | B | 039, 053 | Gli aggiornamenti sono sempre immediati: è il programma a raggrupparli dopo l'interrupt di quadro. L'attesa di una riga di scansione (`SPRITE MOVE INT y`) si fa con l'interrupt di linea (`lib/INTERRUPTS.f`) o con il Copper. Non sono in App. B. |  |
| movimento automatico (`SPRITE CONTINUE`, `SPRITE PAUSE`) | cap. 17, p. 137 | - | D-lib | - | Limiti, passo, rimbalzo e animazione li tiene il programma. Non sono in App. B. |  |
| funzioni `SPRITE s`, `SPRITE AT (s,c)`, `SPRITE CONTINUE s` | cap. 17, p. 139 | - | C | 053 | La RAM degli sprite non si rilegge: posizione, pattern e visibilità stanno nelle strutture del programma, che le conosce già. |  |
| `SPRITE OVER (s1,s2 [TO s3])` (collisioni) | cap. 17, p. 139 | `: HIT? ( x1 y1 x2 y2 -- f ) ROT - ABS 16 < >R - ABS 16 < R> AND ;` | D-inc | - | Riquadri di 16x16 che si toccano; il margine di tolleranza di BASIC si ottiene abbassando il 16. Il giro su un intervallo di sprite è un `DO ... LOOP` sulle strutture. | emu |
| `LAYER AT x,y` | cap. 17, p. 140; App. B | Layer 2: `x $16 REG!  y $17 REG!`; ULA: `$26`, `$27`; LoRes: `$32`, `$33`; tilemap: `$30` (e `$2F`), `$31` | B | 045 | Solo `REG!` diretto, e un registro per layer invece del "layer corrente". Per il Layer 2 a 320 punti il nono bit della x sta in `$71`. L'immagine rientra dal lato opposto, come in BASIC. |  |
| scorrimento di paesaggi grandi (finestra di clip e schermo ombra) | cap. 17, p. 140 | `REG!` su `$18` (clip del Layer 2) e `$13` (banco ombra) | B | 046 | Vedi cap. 16 e 23. |  |
| il Copper | cap. 17, p. 140 | `COP-STOP`, `v h COP-WAIT`, `valore reg COP-MOVE`, `COP-HALT`, `COP-START` -- `NEEDS COPPER` | A | 045 | In BASIC si programma a colpi di `REG 96`; qui c'è una libreria, che scrive l'istruzione intera nel NextReg `$63`. `COP-WAIT ( v h -- )` vuole prima la riga (0-311) e poi la posizione orizzontale (0-55). `COP-START` usa il modo che riparte a ogni quadro, come l'esempio del manuale. |  |
| la lista del Copper in `DATA` | cap. 17, p. 141 | una definizione: `: SKY COP-STOP 0 45 COP-WAIT 16 $40 COP-MOVE $E0 $41 COP-MOVE 100 45 COP-WAIT 16 $40 COP-MOVE 0 $41 COP-MOVE COP-HALT COP-START ;` | B | 045 | La lista è codice con i nomi delle operazioni, non numeri da comporre (`128+(45*2)`). Solo i NextReg 0-127, come in BASIC. Da provare su CSpect. |  |
| `MOVE 0,0` come ritardo breve | cap. 17, p. 143 | `COP-NOOP` | A | 045 |  |  |
| Copper e `REG` che scrivono insieme | cap. 17, p. 143 | lo stesso: `COP-STOP` prima dei `REG!` | A | 045 | È l'hardware. L'esercizio 1 (fermare due volte) è `COP-STOP COP-STOP`. |  |

## Capitolo 18 - Sound and Music

| BASIC | Rif. manuale | vForth | Classe | Dove si impara | Nota | Verifica |
|---|---|---|---|---|---|---|
| `BEEP durata,nota` | cap. 18, p. 144; App. B | `ms nota BEEP` -- `NEEDS BLEEP` | A | 033 | Durata in millisecondi, non in secondi (`BEEP .5,7` è `500 7 BEEP`); nota in semitoni dal do centrale come in BASIC, anche negativa. Sta in `lib/bleep.f`. Per la durata della nota la CPU scende a 3,5 MHz e poi torna com'era. In emulatore si prova solo il calcolo (`0 BEEP-PITCH` dà 2093, otto volte i 261,6 Hz del do): il suono passa dalla ROM. | emu |
| una melodia (`BEEP` in fila, battuta ripetuta) | cap. 18, p. 144 | una definizione per battuta: `: BAR1 1000 0 BEEP 1000 2 BEEP 500 3 BEEP 500 2 BEEP 1000 0 BEEP ;` e poi `BAR1 BAR1` | B | 033, 005 | La battuta che si ripete ha un nome: è l'esercizio 1 del capitolo, senza `FOR`. In alternativa una tabella di coppie durata-nota e un ciclo (cap. 5). |  |
| trasporto e tempo (variabili `key` e `crotchet`) | cap. 18, p. 145 | `0 VALUE KEY#  1000 VALUE CROTCHET` e `: N ( frazione nota -- ) KEY# + SWAP CROTCHET SWAP / SWAP BEEP ;` -- `NEEDS VALUE`, `NEEDS BLEEP` | B | 033 | La durata si dà come divisore della semiminima (1, 2, 4): niente frazioni. Omonimo: `KEY` in Forth legge un tasto, quindi la variabile cambia nome. | emu |
| note frazionarie (scala naturale, quarti di tono) | cap. 18, p. 146 | `ms hz8 BLEEP-CALC BLEEP`, con la frequenza in ottavi di Hz -- `NEEDS BLEEP` | B | 033 | `BEEP` accetta solo semitoni interi; la frequenza si dà direttamente, moltiplicata per 8 (il la a 440 Hz è 3520). |  |
| una nota per volta, e il programma aspetta | cap. 18, p. 145 | lo stesso | A | 033 | Il suono lo fa la CPU, come in BASIC. Per suonare mentre il programma gira: il chip AY, pilotato da un interrupt (riga AFX). |  |
| nota fuori intervallo (`B Integer out of range`) | cap. 18, p. 146 | nessun controllo | C | - | Da verificare sulla macchina cosa succede agli estremi: `BEEP-PITCH` non controlla l'argomento. |  |
| `POKE 23609,n` (il clic dei tasti) | cap. 18, p. 147 | `n 23609 C!` | A | 008 | Stessa variabile di sistema (PIP). Da verificare sulla macchina se la lettura dei tasti di vForth fa il clic. |  |
| `PLAY f1[,...]` | cap. 18, p. 147; App. B | - | D-lib | 034, 050, 055 | Nessun interprete di stringhe musicali. `lib/AY.f` scrive i registri del chip; AFX suona effetti e musiche preparati. Le righe che seguono dicono dove va a finire ogni comando della stringa. |  |
| `PLAY`: nota e ottava (`c`-`B`, `#`, `$`, `O`) | cap. 18, p. 148 | il periodo del tono, 12 bit: `periodo 0 AY!!` (canale A; 2 per B, 4 per C) -- `NEEDS AY` | B | 034 | Si scrive un periodo, non il nome di una nota: la tabella delle note la costruisce il programma. |  |
| `PLAY`: durata, pausa `&`, tempo `T`, ripetizioni `( )` | cap. 18, p. 149 | il ciclo del programma: `MS` o `1FRAME` fra una nota e l'altra, `DO ... LOOP` per ripetere -- `NEEDS MS` | B | 032, 034 | Il chip tiene la nota finché non gli si dice altro: il tempo lo scandisce il programma (o un interrupt). |  |
| `PLAY`: volume `V` | cap. 18, p. 151 | registri 8, 9, 10: `v 8 AY!` (0-15) -- `NEEDS AY` | A | 034 |  |  |
| `PLAY`: effetti di volume `W`, `U`, `X` | cap. 18, p. 151 | inviluppo: forma nel registro 13, periodo nei registri 11 e 12; il canale lo usa con volume 16 -- `NEEDS AY` | B | 034 | Le otto forme di `W` corrispondono alle forme dell'inviluppo del chip. |  |
| `PLAY`: scelta dei canali `M` (tono o rumore) | cap. 18, p. 153 | registro 7 (mixer); periodo del rumore nel registro 6; `SHH` spegne tutto -- `NEEDS AY` | B | 034 | Trappola: nel registro 7 il bit a 0 accende, al contrario di `M`. `M7` (tre toni) è `%00111000 7 AY!`. |  |
| nove canali su tre chip | cap. 18, p. 147 | `ENABLE-TURBOSOUND` e poi `n AYSELECT` (1-3) prima di scrivere i registri -- `NEEDS AY` | A | 034 | `AYSETUP` zittisce i tre chip e li mette in mono. |  |
| stereo (`L`, `R`, `S`) | cap. 18, p. 153 | `ENABLE-MONO`, `DISABLE-MONO`; canale sinistro o destro: bit 6 e 5 del byte scritto sulla porta `$FFFD` -- `NEEDS AY` | B | 034 | `AYSELECT` accende sempre entrambi i lati: per uno solo si scrive la porta a mano con `P!`. |  |
| `PLAY`: MIDI (`Y`, `Z`) | cap. 18, p. 148 | - | D (scelta) | - |  |  |
| `PLAY`: `H`, `N`, commenti `! !` | cap. 18, p. 151 | - | N | - | Sintassi della stringa: senza stringa non servono. |  |
| effetti e musiche già pronti | cap. 18 | lettore AFX: `AFXFRAME`, `lib/afxplay.f` -- `NEEDS AFXFRAME` | B | 050, 055 | In più rispetto a BASIC: suona nell'interrupt mentre il programma continua. |  |
| audio digitale (`.wavplay32`, `.nxmod`, `.playpt3`) | cap. 18, p. 153 | - | D-lib | - | In BASIC sono comandi punto, e da vForth non si lancia un comando punto. I DAC si raggiungono con `REG!` (NextReg `$2C`-`$2E`), ma un lettore non c'è. |  |
| audio con l'acceleratore Raspberry Pi (`.pisend`) | cap. 18, p. 154 | `lib/RPi0.f`: `RPI0`, `TERM`; `SH` -- `NEEDS RPi0`, `NEEDS SH` | B | 048 | La libreria parla con il Pi sulla UART e gli manda righe di comando; il trasferimento di un file audio (`.pisend`) non c'è. |  |
| uscita audio esterna, file TZX | cap. 18, p. 155 | - | N | - | Hardware, fuori dal linguaggio. |  |

## Capitolo 19 - NextZXOS and alternatives

| BASIC | Rif. manuale | vForth | Classe | Dove si impara | Nota | Verifica |
|---|---|---|---|---|---|---|
| nomi di file, unità e percorsi | cap. 19, p. 159 | gli stessi di NextZXOS; il nome segue la parola (`INCLUDE lib/x.f`) oppure va messo in PAD (`PAD" nome"`) | A | 042, 043 | Senza virgolette, tranne `PAD"`. Le parole che leggono il nome dal testo (`INCLUDE`, `UNLINK`, `VIEW`, `OPEN>`) si fermano al primo spazio: un nome con gli spazi passa solo da `PAD"`. I nomi delle parole con caratteri vietati nei file sono mappati da `NEEDS` (`?` diventa `^`, e così via). |  |
| il tipo del file (`.bas`, `.bin`) | cap. 19, p. 159 | per convenzione `.f` per i sorgenti | A | 028, 043 | `NEEDS parola` cerca `inc/parola.f` e poi `lib/parola.f`; `INCLUDE` vuole il nome completo. |  |
| unità predefinita (`LOAD "m:"`, `SAVE "c:"`) | cap. 19, p. 161 | la lettera dell'unità nel percorso; primitiva `M_GETSETDRV` -- `NEEDS M_GETSETDRV` | B | - | Senza lettera vale l'unità predefinita di NextZXOS. `M_GETSETDRV` non tocca le unità di `LOAD` / `SAVE` di BASIC. Nessuna parola pronta, nessun tutorial. |  |
| `LOAD f` (programma) | cap. 19, p. 160; App. B | `INCLUDE file`; `NEEDS parola`; `n LOAD` (Screen) | C | 028, 043 | Si carica sorgente, che viene compilato. Omonimo: `LOAD` in Forth interpreta uno Screen. |  |
| `LOAD ""`, `LOAD "*"`, `LOAD "d*"` (nastro, dischi virtuali, primo file che comincia per d) | cap. 19, p. 161 | - | N | - |  |  |
| `LOAD f CODE m[,n]` | cap. 19, p. 162 | `PAD" f" m n LOAD-BYTES` -- `NEEDS PAD"`, `NEEDS LOAD-BYTES` | A | 042 | Indirizzo e lunghezza sono obbligatori: n è il massimo, e un file più corto si carica senza errore. Meglio sotto `$E000` (sopra c'è MMU7). Da verificare su CSpect: un file scritto da BASIC con `SAVE ... CODE` comincia con l'intestazione +3DOS, che `LOAD-BYTES` caricherebbe come dati; `SAVE-BYTES` scrive i byte nudi. | emu |
| `LOAD f SCREEN$` | cap. 19, p. 161 | `PAD" f" $4000 6912 LOAD-BYTES` -- `NEEDS LOAD-BYTES` | B | 042 | 6144 byte per i soli pixel, senza attributi, come `CODE 16384,6144`. |  |
| `LOAD f LAYER` | cap. 19, p. 162 | secondo il layer: `LOAD-BYTES` a `$4000`, oppure `MMU7!` + `LOAD-BYTES` pagina per pagina (Layer 2: sei pagine da 8K); BMP: `BMP-LOAD"` -- `NEEDS LOAD-BYTES`, `NEEDS BMP-LOAD` | B | 046 | Non c'è una parola che segua il "layer corrente". |  |
| la palette non viene salvata con lo schermo | cap. 19, p. 162 | lo stesso | A | 056 | Si legge con `REG@` (`$40`, `$41`) e si salva a parte. |  |
| `LOAD f BANK m[,o,n]` | cap. 19, p. 163 | `MMU7!` + `LOAD-BYTES` a `$E000` (due pagine da 8K per banco) -- `NEEDS LOAD-BYTES` | B | 041, 042 | Dentro una definizione che rimette la pagina di prima (cap. 23). |  |
| `LOAD f DATA a()` | cap. 19, p. 163 | `PAD" f" tab n LOAD-BYTES` -- `NEEDS LOAD-BYTES` | B | 042 | La tabella va già riservata con `ALLOT`: il caricamento non la dimensiona. Nessun controllo del tipo. |  |
| `LOAD f INT`, `LOAD f INPUT` | cap. 19, p. 163 | - | N | - | Non c'è un insieme fisso di variabili intere, né il joystick di tastiera. Le variabili che servono si salvano come una zona di memoria. |  |
| `SAVE f` (programma) | cap. 19, p. 164; App. B | - | C | 028, 059 | Il sorgente è già un file. Omonimo: `SAVE` in vForth scarica gli Screen modificati. Per congelare il sistema: `ZAP`. |  |
| copia di riserva automatica (`.bak`) | cap. 19, p. 164 | - | C | 042 | `SAVE-BYTES` rifiuta di scrivere su un file che esiste; `SAVE-BYTES-FORCE` lo sovrascrive senza copia. |  |
| `SAVE f LINE n` (avvio automatico) | cap. 19, p. 165 | l'ultima riga del sorgente chiama la parola principale | B | 028 | `INCLUDE gioco.f` compila e, arrivato in fondo, esegue quello che trova. |  |
| `SAVE f CODE m,n` | cap. 19, p. 166 | `PAD" f" m n SAVE-BYTES` -- `NEEDS PAD"`, `NEEDS SAVE-BYTES` | A | 042 | Se il file esiste già: `SAVE-BYTES? NextZXOS Open error.`; per sovrascrivere c'è `SAVE-BYTES-FORCE`. | emu |
| `SAVE f SCREEN$`, `SAVE f LAYER` | cap. 19, p. 166 | `PAD" f" $4000 6912 SAVE-BYTES`; altri layer: `MMU7!` + `SAVE-BYTES` -- `NEEDS SAVE-BYTES` | B | 042 | I tipi `.SCR`, `.SL2` e gli altri sono una convenzione del Browser: valgono anche qui. |  |
| `SAVE f BANK m[,o,l]` | cap. 19, p. 167 | `MMU7!` + `SAVE-BYTES` -- `NEEDS SAVE-BYTES` | B | 041, 042 | `SAVE-BANK` di `lib/ZAP.f` è un'altra cosa (salva i banchi 16-19 dello heap). |  |
| `SAVE f DATA a()` | cap. 19, p. 167 | `PAD" f" tab n SAVE-BYTES` -- `NEEDS SAVE-BYTES` | B | 042 | Una tabella è una zona di memoria come le altre. |  |
| `VERIFY f` | cap. 19, p. 168; App. B | - | N | - | Solo nastro. |  |
| `MERGE f` | cap. 19, p. 169; App. B | `INCLUDE file`; per le librerie `NEEDS parola` | B | 043 | `INCLUDE` aggiunge sempre al dizionario. Una parola ridefinita non sostituisce la vecchia per chi la usava già (cap. 1). `NEEDS` carica una volta sola: è il modo normale di tenere una libreria di routine. |  |
| caratteri jolly | cap. 19, p. 170 | `WILDCARD *.F` e poi `DIR` -- `NEEDS WILDCARD`, `NEEDS DIR` | B | - | Valgono solo per `DIR`. Il filtro resta attivo finché non si dà un `WILDCARD` da solo. Nessun tutorial. |  |
| filesystem, partizioni, dispositivi, montaggio | cap. 19, p. 171 | - | N | - | Ambiente della macchina. |  |
| `CAT [filespec]` (anche `DIR`, `LS`) | cap. 19, p. 173; App. B | `DIR percorso` -- `NEEDS DIR` | A | 042, 043 | Stesso nome dell'alias di BASIC. L'elenco è ordinato e ha già dimensione, data e ora, con il totale in fondo: è più vicino a `CAT EXP`. Il percorso segue la parola, senza virgolette. In emulatore si carica ma dà `NextZXOS Read error` (limite dell'emulatore): da provare su CSpect. |  |
| `CAT EXP` | cap. 19, p. 173 | `DIR`; gli attributi con `F_STAT` -- `NEEDS DIR`, `NEEDS F_STAT` | B | 043 | `DIR` non mostra gli attributi; `F_STAT ( a buf -- f )` li mette in un buffer di 11 byte con ora, data e dimensione. |  |
| `CAT -` (nomi corti 8+3) | cap. 19, p. 175 | - | D (scelta) | - |  |  |
| `MKDIR filespec` | cap. 19, p. 178; App. B | `MAKEDIR percorso` -- `NEEDS MAKEDIR` | A | - | Nessun tutorial. |  |
| `RMDIR filespec` | cap. 19, p. 178; App. B | `REMOVEDIR percorso` -- `NEEDS REMOVEDIR` | A | - | Nessun tutorial. |  |
| `CD filespec` | cap. 19, p. 179; App. B | `CD percorso` -- `NEEDS CD` | A | 043 | Trappola: `NEEDS` e `INCLUDE lib/...` usano percorsi relativi alla cartella di vForth, quindi dopo un `CD` non trovano più niente finché non si torna indietro. `..` e `/` valgono come in BASIC: li interpreta NextZXOS. |  |
| `PWD` | cap. 19, p. 180; App. B | `PWD` -- `NEEDS PWD` | A | 043 |  |  |
| `PWD #n` in una stringa (`OPEN #2,"v>d$"`) | cap. 19, p. 180 | `buf F_GETCWD` -- `NEEDS F_GETCWD` | B | - | Lascia in `buf` il percorso terminato da uno zero. Non serve catturare l'uscita di un comando. |  |
| `COPY f1 TO f2` | cap. 19, p. 181; App. B | - | D-inc | 042 | Non c'è, ma sono poche righe: due file aperti e un ciclo `F_READ` / `F_WRITE` su un buffer (provato, vedi "Cosa esce dalla matrice"). Con i caratteri jolly diventa un lavoro da libreria. | emu |
| `COPY f TO SCREEN$` | cap. 19, p. 182 | `VIEW nomefile` -- `NEEDS VIEW` | A | 064 | Mostra il file a 85 colonne. |  |
| `COPY f TO LPRINT` | cap. 19, p. 182 | - | D-inc | - | Vedi cap. 20: da verificare `3 SELECT`. |  |
| `ERASE filespec` | cap. 19, p. 182; App. B | `UNLINK nomefile` -- `NEEDS UNLINK` | A | 057 | Niente caratteri jolly e nessuna richiesta di conferma. Se il file non c'è stampa il messaggio 43 e suggerisce di mettere l'unità. |  |
| `MOVE f1 TO f2` (spostare e rinominare) | cap. 19, p. 183; App. B | `F_RENAME ( src dest -- f )` -- `NEEDS F_RENAME` | B | - | Primitiva con due nomi terminati da zero (`CREATE N1 ," vecchio" 0 C,` e poi `N1 1+`). Come in BASIC, non fra unità diverse. Omonimo: `RENAME` in vForth rinomina una parola del dizionario, non un file. |  |
| `MOVE f TO "+p"` (attributi) | cap. 19, p. 184 | `F_CHMOD ( a attr maschera -- f )` -- `NEEDS F_CHMOD` | B | - | Primitiva: la maschera dice quali bit cambiare. Da verificare su CSpect la corrispondenza con `+p`, `+s`, `+a`. |  |
| il RAMdisk (`m:`) | cap. 19, p. 186 | lo stesso: un'unità come le altre | A | 042 |  |  |
| `CAT TAB`, `CAT ASN`, `MOVE ... IN`, `MOVE ... OUT` | cap. 19, p. 186 | - | D (scelta) | - | Dispositivi, partizioni e montaggio si gestiscono da BASIC prima di lanciare vForth. |  |
| `REMOUNT` | cap. 19, p. 188; App. B | `REMOUNT` -- `NEEDS REMOUNT` | A | - | Chiude anche il file dei blocchi. |  |
| `.mkdata`, `.mkswap` (dischi virtuali) | cap. 19, p. 188 | - | N | - |  |  |
| stampa (`LLIST`, `LPRINT`, `COPY`) | cap. 19, p. 189 | - | D-inc | - | Vedi cap. 20. |  |
| `SPECTRUM`, `SPECTRUM f`, `SPECTRUM LOAD`, `SPECTRUM 48` | cap. 19, p. 189; App. B | - | N | - | Modo 48K e snapshot. |  |
| `SPECTRUM INK` / `PAPER` / `ATTR` (colori dell'editor) | cap. 19, p. 190 | i colori del prompt: `.INK`, `.PAPER` e `.PERM` nello Screen 11 o in `lib/autoexec.f` -- `NEEDS .PERM` | B | 030 | Lo Screen 11 imposta i colori a ogni avvio. |  |
| `SPECTRUM CHR$ n` (32, 64, 85 colonne) | cap. 19, p. 191 | `NARROWCHAR`, `WIDECHAR`; in generale `30 EMITC n EMITC` -- `NEEDS NARROWCHAR`, `NEEDS WIDECHAR` | B | - | Vedi cap. 14. |  |
| `SPECTRUM SCREEN$ n,t` (salvaschermo) | cap. 19, p. 191 | - | N | - |  |  |
| `RUN AT s` | cap. 19, p. 191 | `s SPEED!` -- `NEEDS SPEED!` | A | 040 | Vedi cap. 22. |  |
| `ERASE [m,n]` | cap. 19, p. 192; App. B | `FORGET nome` | B | 004, 028 | Omonimo: `ERASE ( a n -- )` in Forth azzera n byte di memoria. |  |
| `LINE start,step`, `LINE m,n TO mm,nn` | cap. 19, p. 192; App. B | - | N | - | Rinumerazione: niente numeri di riga. |  |
| `LINE MERGE first,last` | cap. 19, p. 192; App. B | - | N | - | Come sopra. |  |
| `LIST [#c] [PROC nome()]` | cap. 19, p. 193 | `SEE nome`; il sorgente: `VIEW file`, `n LIST` -- `NEEDS SEE`, `NEEDS VIEW` | B | 022, 028 | `SEE` decompila una parola sola: è il `LIST PROC` di Forth. Vedi cap. 1. |  |
| `%CODE` (bit 1: BREAK disabilitato) | cap. 19, p. 193 | - | C | 006 | BREAK non è mai automatico: lo sente solo il programma che interroga `?TERMINAL`. Il bit 0 riguarda `RND` (cap. 10). |  |
| Browser, menu NMI, riga di comando, cartucce, CP/M, esxDOS | cap. 19, p. 193 | - | N | - | Ambiente della macchina, fuori dal linguaggio. |  |
| comandi punto | cap. 19, p. 199 | - | C | 057 | vForth stesso può essere un comando punto (`.vforth`, variante DOT), ma da dentro non ne lancia altri. |  |
| `.browse` (finestra di scelta di un file) | cap. 19, p. 200 | - | D-lib | - | Servirebbe la chiamata `IDE_BROWSER` attraverso `M_P3DOS`. |  |
| `.mem`, `.nextver` | cap. 19, p. 200 | `UNUSED`; `DOSVER` -- `NEEDS UNUSED`, `NEEDS DOSVER` | B | 025 | `UNUSED` è lo spazio libero nel dizionario di vForth, non la memoria di NextZXOS. `DOSVER` stampa la versione. |  |
| avvio automatico (`autoexec.bas`) | cap. 19, p. 200 | Screen 11 del file dei blocchi, che include `lib/autoexec.f` | B | 028 | Si modifica con `EDIT` o cambiando `lib/autoexec.f`. |  |
| uscita dal sistema | cap. 19 | `BYE`; `n BASIC` | B | 035, 051, 059 | `BYE` scarica i blocchi, chiude il file e torna a BASIC; `BASIC ( n -- )` torna subito, passando n come risultato di `USR`. Da BASIC, `RUN` riprende vForth. |  |
| spazio libero, dimensione e data di un file | cap. 19, p. 173 | `.FREE-SIZE`, `.FILE-SIZE`, `.DATE-TIME`; primitive `F_GETFREE`, `F_STAT`, `F_FSTAT` -- `NEEDS .FREE-SIZE`, `NEEDS .FILE-SIZE` | B | - | `CHAR * F_GETFREE` dà lo spazio libero in settori da 512 byte, come doppio. Non provate. |  |
| dati che restano fra una sessione e l'altra | cap. 19 | il file dei blocchi: `n BLOCK`, `UPDATE`, `FLUSH`; `LIST`, `LOAD` | C | 028, 063 | In più rispetto a BASIC: 16 MB di blocchi da 512 byte sempre aperti, senza `OPEN` né nomi di file. |  |
| sorgente fra file di testo e Screen | cap. 19 | `n SCREEN-TO-FILE nome`, `n SCREEN-FROM-FILE nome` -- `NEEDS SCREEN-TO-FILE`, `NEEDS SCREEN-FROM-FILE` | B | 063 | In più rispetto a BASIC. Attenzione al nome: `SCREEN-FROM-FILE` copia un file di testo nello Screen n del file dei blocchi, non carica un'immagine. |  |

## Capitolo 20 - Channels, Streams, Drivers and Windows

| BASIC | Rif. manuale | vForth | Classe | Dove si impara | Nota | Verifica |
|---|---|---|---|---|---|---|
| canali e stream (il modello) | cap. 20, p. 206 | due meccanismi distinti: l'uscita a caratteri segue lo stream scelto con `n SELECT`; i file si usano con un handle (`F_OPEN`, `F_READ`, `F_WRITE`, `F_CLOSE`) | C | 003, 042 | Un handle è un numero sullo stack dato da NextZXOS, non uno stream da 0 a 15: lo tiene il programma, di solito in una `VALUE`. `OPEN #` come comando non c'è. |  |
| stream già aperti (tastiera, schermo, stampante) | cap. 20, p. 206 | `2 SELECT` (o `VIDEO`), `3 SELECT`, `4 SELECT` | B | 003 | `SELECT` chiama la routine della ROM che attiva uno stream: sceglie uno stream che esiste già. Il 3 è la stampante, come in BASIC; dal 4 in su dipendono da un `OPEN #` fatto in BASIC prima di lanciare vForth. Nessun tutorial spiega `SELECT`, anche se 20 lo usano. |  |
| `PRINT #n; ...` | cap. 20, p. 211 | `n SELECT` ... `VIDEO` | B | 003 | `SELECT` vale per tutta l'uscita che segue (`.`, `."`, `TYPE`, `EMIT`), finché `VIDEO` non torna allo schermo. Verso un file aperto in BASIC funziona (è il caso di `13 SELECT WORDS`). In emulatore la routine della ROM è uno stub: da provare sulla macchina. |  |
| `LPRINT` | cap. 20, p. 206; App. B | `3 SELECT` ... `VIDEO` | B | - | Da provare con una stampante: nessuna parola dedicata. |  |
| `LLIST [m]` | cap. 20, p. 207; App. B | `3 SELECT n LIST VIDEO` | B | - | Elenca uno Screen sulla stampante; un file sorgente: `3 SELECT VIEW file VIDEO`. Da provare. |  |
| `COPY` (schermo sulla stampante) | cap. 19, p. 189 | - | N | - | ZX Printer. |  |
| `INPUT #0`, `INPUT #1` (tastiera, parte bassa dello schermo) | cap. 20, p. 207 | `ACCEPT`, `KEY` | C | 016 | Non c'è una parte bassa dello schermo: vedi cap. 14. |  |
| `OPEN #n,"i>file"` (lettura) | cap. 20, p. 208; App. B | dal prompt: `OPEN< nomefile` (lascia l'handle); in una definizione: `PAD" nome" PAD DUP 10 - 1 F_OPEN` -- `NEEDS PAD"` | B | 042, 053, 060 | `OPEN<` funziona solo in interpretazione. `F_OPEN ( a1 a2 modo -- fh f )`: f diverso da zero vuol dire errore, e va controllato (`41 ?ERROR`). | emu |
| `OPEN #n,"o>file"` (scrittura, file nuovo) | cap. 20, p. 208 | `OPEN> nomefile`; in una definizione `F_OPEN` con modo `%1110` -- `NEEDS OPEN>` | B | 042, 059 | `%1110` crea il file e cancella quello che c'era; `%0110` dà errore se esiste già. Nessun tutorial usa `OPEN>`. | emu |
| `OPEN #n,"u>file"` (aggiornamento) | cap. 20, p. 209 | `F_OPEN` con modo `%0011` (lettura e scrittura, file esistente) | B | 042 | Non provato. |  |
| `OPEN #n,"k"`, `"s"`, `"p"` | cap. 20, p. 208 | - | N | - | Sono già aperti: `SELECT`. |  |
| `CLOSE #n` | cap. 20, p. 209; App. B | `fh F_CLOSE` (lascia un flag) | A | 042 | Trappola: un errore (`ERROR`, `ABORT`) non chiude i file aperti; un file in scrittura lasciato aperto può perdere dati, come in BASIC. | emu |
| `POINT #n`, `RETURN #n TO v` (posizione) | cap. 20, p. 209 | `fh F_FGETPOS ( -- d f )` | A | - | Posizione in doppia precisione: nessun limite a 65535. | emu |
| `DIM #n`, `DIM #n TO v` (lunghezza) | cap. 20, p. 210 | `buf fh F_FSTAT` e poi i quattro byte a `buf 7 +` -- `NEEDS F_FSTAT` | B | - | Primitiva: riempie un buffer di 11 byte (attributi, ora, data, dimensione). Da verificare su CSpect l'ordine delle due celle della dimensione. |  |
| `GO TO #n,pos` | cap. 20, p. 210 | `d fh F_SEEK` (lascia un flag) | A | - | Posizione in doppia precisione: `100. fh F_SEEK DROP`. | emu |
| `NEXT #n TO v` (un carattere) | cap. 20, p. 210 | da un file: `PAD 1 fh F_READ` e poi `PAD C@`; dalla tastiera: `KEY` | B | 042, 053 | `F_READ ( a n fh -- n2 f )`. La macchina da scrivere del manuale è `BEGIN KEY EMIT AGAIN`. | emu |
| `INPUT #n; LINE a$` (una riga da un file) | cap. 20, p. 211 | `buf max fh F_GETLINE ( -- n )` | B | 053 | Legge fino al fine riga. Trappola: il numero lasciato conta anche il fine riga (`Hello` dà 6), come `ACCEPT`. È la parola con cui `INCLUDE` legge i sorgenti; nessun tutorial la spiega. | emu |
| `PRINT #n` su un file | cap. 20, p. 208 | `a n fh F_WRITE` | B | 042, 059 | `F_WRITE ( a n fh -- n2 f )` scrive byte: i numeri vanno prima convertiti in testo con `<# ... #>`, e il fine riga si scrive a mano. | emu |
| fine del file (`8 End of file`) | cap. 20, p. 212 | `F_READ` dice quanti byte ha letto davvero | B | 042 | Meno di quelli chiesti vuol dire fine del file: nessun errore. | emu |
| `ON ERROR` attorno alle operazioni sugli stream | cap. 20, p. 212 | il flag di ogni primitiva, con `n ?ERROR`; oppure `CATCH` -- `NEEDS CATCH` | B | 026, 042 | Le primitive `F_...` non si fermano da sole: lasciano un flag. |  |
| `COPY f TO #n`, `CAT #n`, `PWD #n` (uscita di un comando su uno stream) | cap. 20, p. 211 | `n SELECT` prima della parola, `VIDEO` dopo | B | 003 | Da verificare: `DIR`, `PWD` e `VIEW` stampano con `EMIT`, quindi dovrebbero seguire lo stream scelto. |  |
| canale variabile (`v>`) e canale memoria (`m>`) | cap. 20, p. 211 | - | N | - | Servono a BASIC per catturare l'uscita in una stringa: in Forth l'uscita formattata è già una stringa (`<# #>`), e le chiamate a NextZXOS lasciano i valori sullo stack (`F_GETCWD`, `IDE_RTC`). |  |
| `.install`, `.uninstall` (driver) | cap. 20, p. 213 | - | N | - | Si installano da BASIC prima di lanciare vForth. |  |
| `DRIVER drid,callid ...` | cap. 20, p. 213; App. B | - | D-inc | - | Nessuna parola per la chiamata `M_DRVAPI`. |  |
| `OPEN #n,"d>X..."` (canali driver: rete, seriale) | cap. 20, p. 213 | `lib/UART-SYS.f` -- `NEEDS UART-SYS` | B | 047 | Si parla con la UART direttamente, non attraverso un driver di NextZXOS. |  |
| finestre di sistema e i loro codici di controllo | cap. 20, p. 214 | `EMITC` del codice e dei suoi argomenti | A | 031 | Il testo di vForth esce dalla ROM nella finestra di sistema del layer attivo, quindi valgono i codici della colonna SW: 14 pulisce (è `CLS`), 24 imposta l'attributo, 26 la pausa automatica (`PAUSEOFF` la toglie), 28 la larghezza doppia, 29 l'altezza, 30 la larghezza del carattere. Sul Layer 0 valgono solo i codici classici (cap. 13). Da provare sulla macchina. |  |
| finestre utente (`OPEN #n,"w>riga,col,alt,larg"`) | cap. 20, p. 214 | - | D-lib | - | Finestre con posizione e misura proprie, giustificazione, salvataggio e ripristino del contenuto: niente di tutto questo. |  |
| set di caratteri di una finestra | cap. 20, p. 216 | la variabile CHARS (`a 23606 !`) e poi `2 EMITC` | B | - | Vedi cap. 13. Da provare sulla macchina. |  |
| `INPUT #` in una finestra | cap. 20, p. 217 | - | D-lib | - | Come le finestre utente. |  |

## Capitolo 21 - Optional Features

| BASIC | Rif. manuale | vForth | Classe | Dove si impara | Nota | Verifica |
|---|---|---|---|---|---|---|
| installazione di memoria, WiFi, RTC e acceleratore | cap. 21, p. 220 | - | N | - | Capitolo di installazione. |  |
| prova della memoria (1792K nel menu, `2MBTEST`) | cap. 21, p. 223 | - | N | 041 | La memoria in più vForth la vede come pagine da 8K oltre la 95 (banchi da 16K oltre il 47), da mappare con `MMU7!`. |  |
| prova del WiFi (`.uart`, comandi `AT`) | cap. 21, p. 223 | `lib/UART-SYS.f` -- `NEEDS UART-SYS` | B | 047 | Il tutorial 047 dialoga con il modulo ESP dalla UART, senza passare dal comando punto. |  |
| prova dell'RTC (`.time`) | cap. 21, p. 225 | `M_GETDATE ( -- data ora hs f )` -- `NEEDS M_GETDATE` | B | - | f diverso da zero vuol dire che l'RTC non ha risposto: è la prova più diretta. Da provare sulla macchina. |  |
| prova dell'acceleratore (`terminex`, prompt `SUP>`) | cap. 21, p. 226 | `RPI0`, `TERM` -- `NEEDS RPi0` | B | 048 | `lib/RPi0.f` è un terminale verso il Pi: aspetta lo stesso prompt `SUP>`. |  |
| leggere l'orologio (`TIME$`, `.time`, `.date`) | cap. 21, p. 227 | `.NOW`; valori grezzi `IDE_RTC`, `M_GETDATE` -- `NEEDS .NOW`, `NEEDS IDE_RTC`, `NEEDS M_GETDATE` | B | - | Vedi cap. 17. Data e ora in formato MS-DOS; `.FAT-DATE` e `.FAT-TIME` le stampano. Nessun tutorial. |  |
| impostare l'orologio (`.time "hh:mm:ss"`, `.date "gg/mm/aaaa"`) | cap. 21, p. 227 | - | D (scelta) | - | Si fa una volta, da BASIC o dal menu di NextZXOS. |  |
| data e ora sui file salvati | cap. 21, p. 227 | lo stesso | A | 043 | Le mette NextZXOS: valgono anche per i file scritti da vForth, e `DIR` le mostra. |  |
| ora da Internet (`.nxtp`) | cap. 21, p. 228 | - | N | - | Comando punto, da mettere in `autoexec.bas`. |  |
| acceleratore Raspberry Pi Zero | cap. 21, p. 228 | `lib/RPi0.f`; `ASK`, `SH` -- `NEEDS RPi0`, `NEEDS ASK`, `NEEDS SH` | B | 048 | `SH comando` manda una riga al Pi; `ASK comando` raccoglie anche la risposta in `PAD` (fino a 1024 byte) e ne lascia la lunghezza. |  |

## Capitolo 22 - IN, OUT and the Next Registers

| BASIC | Rif. manuale | vForth | Classe | Dove si impara | Nota | Verifica |
|---|---|---|---|---|---|---|
| `OUT m,n` | cap. 22, p. 229; App. B | `n m P!` | A | 039, 053 | Prima il valore, poi la porta. Omonimo: `OUT` nel core è una variabile utente, un contatore dei caratteri emessi (in emulatore vale qualche migliaio dopo poche righe: non è la colonna). |  |
| `IN n` | cap. 22, p. 229; App. B | `n P@` | A | 066 | Omonimo: in BASIC `IN` è anche la ricerca in una stringa (cap. 8). | emu |
| indirizzi di porta a 16 bit, decodifica parziale | cap. 22, p. 229 | `P@` e `P!` prendono la porta intera: `$FEFE P@` | A | 051 | È l'hardware: ogni porta pari risponde la ULA, e la mezza riga della tastiera sta nel byte alto. |  |
| la tabella delle porte | cap. 22, p. 230 | la stessa: è l'hardware | N | 040 | La guida rimanda al manuale Next. |  |
| NextREG attraverso le porte `$243B` e `$253B` (`OUT 9275,n: OUT 9531,v`) | cap. 22, p. 232 | è quello che fanno `REG@` e `REG!` | A | 040 | Le due scritture stanno dentro una parola sola, senza niente in mezzo: l'avvertenza di BASIC ("sulla stessa riga") non serve. Vale invece per una routine di interrupt che usi i NextReg: deve rimettere a posto il registro selezionato. |  |
| `REG n,v` | cap. 22, p. 232; App. B | `v n REG!` | A | 040 | Prima il valore, poi il registro. | emu |
| `REG n` (funzione) | cap. 22, p. 232 | `n REG@` | A | 040 |  | emu |
| `RUN AT speed` | cap. 22, p. 232; App. B | `n SPEED!` (0-3); lettura `SPEED@` -- `NEEDS SPEED!`, `NEEDS SPEED@` | A | 040 | `2 SPEED! SPEED@ .` dà 2. È il NextReg 7: `7 REG@ 3 AND` legge la stessa cosa. Il manuale ne parla anche nel cap. 19 (p. 191). | emu |
| un bit di un registro (`REG 5&@100>>2`) | cap. 22, p. 233 | `5 REG@ 4 AND 2 RSHIFT`; come flag basta `5 REG@ 4 AND` | A | 011, 040 | Maschera e scorrimento, postfissi. | emu |
| cambiare alcuni bit lasciando gli altri | cap. 22, p. 233 | `reg REG@ maschera AND nuovi OR reg REG!` | A | 011, 040 | Per accendere un bit: `$69 REG@ $80 OR $69 REG!`. Provato sul registro utente `$7F`. | emu |
| l'elenco dei NextReg | cap. 22, p. 234 | lo stesso: è l'hardware | N | 040 | La guida rimanda al manuale Next; i tutorial coprono solo i registri usati. |  |
| registri delle MMU (`$50`-`$57`) | cap. 22, p. 238 | `MMU7!`, `MMU7@`; `MMU0!`, `MMU1!` -- `NEEDS MMU0!`, `NEEDS MMU1!` | A | 041 | Solo MMU7 è libera: negli altri slot ci sono vForth, i suoi stack e lo schermo. Vedi cap. 23. |  |
| interrupt (NextReg `$C0` e seguenti) | cap. 22, p. 241 | `ISR-SETUP`, `ISR-ON`, `ISR-OFF`, `ISR-SYNC` -- `NEEDS INTERRUPTS` | B | 049 | In più rispetto a BASIC, che non può scrivere una routine di interrupt. |  |
| tastiera (`IN 65278` e le altre mezze righe) | cap. 22, p. 243 | `$FEFE P@ 1 AND` (0 se CAPS SHIFT è premuto); libreria `KEYBOARD` -- `NEEDS KEYBOARD` | A | 051 | Bit a 0 vuol dire tasto premuto, come in BASIC. L'indirizzo di una mezza riga: `: HALF-ROW ( n -- porta ) 1 SWAP LSHIFT 255 SWAP - 256 * 254 + ;` (0 dà 65278). In emulatore la porta dà sempre "nessun tasto". | emu |
| `OUT 254,n` (bordo, altoparlante) | cap. 22, p. 243 | `n 254 P!`; il bordo: `n .BORDER` -- `NEEDS .BORDER` | A | 030, 033 | `.BORDER` passa dalla ROM e aggiorna anche la variabile di sistema; la scrittura sulla porta no. |  |
| porte della paginazione (`$7FFD`, `$1FFD`, `$DFFD`) | cap. 22, p. 243 | - | N | 041 | Da non toccare: vForth usa le MMU (cap. 23). |  |
| porte del chip AY (`$FFFD`, `$BFFD`) | cap. 22, p. 243 | `v r AY!` -- `NEEDS AY` | A | 034 | Vedi cap. 18. |  |
| mouse Kempston | cap. 22, p. 244 | `lib/MOUSE.f` -- `NEEDS MOUSE` | B | 044 |  |  |
| joystick Kempston (porte 31 e 55) | cap. 22, p. 244 | `31 P@`, `55 P@` | A | 066 | In emulatore la porta dà 255. |  |
| DMA, UART, sprite, Layer 2, DAC (porte dedicate) | cap. 22, p. 244 | `lib/DMA.f`, `lib/UART-SYS.f`, `lib/SPRITE.f`, `LAYER2`; per le altre `P!` | B | 054, 047, 039, 037 | Ogni gruppo di porte ha la sua libreria; DAC, SPI, I2C e CTC si pilotano a mano. |  |

## Capitolo 23 - The Memory

| BASIC | Rif. manuale | vForth | Classe | Dove si impara | Nota | Verifica |
|---|---|---|---|---|---|---|
| la mappa di memoria (64K visibili, il resto a banchi) | cap. 23, p. 247 | la stessa fino a RAMTOP (`$61FF`); vForth parte da `$6366`; stack e buffer dei blocchi stanno sotto `$E000`; `$E000-$FFFF` è lo slot MMU7 | C | 025, 041 | vForth vive sopra RAMTOP, come un programma in linguaggio macchina lanciato da BASIC. |  |
| banco da 16K e pagina da 8K (i due schemi di paginazione) | cap. 23, p. 248 | `: BANK>PAGES ( banco -- p1 p2 ) 2* DUP 1+ ;` | C | 041 | BASIC conta in banchi da 16K, `MMU7!` in pagine da 8K: il banco 20 sono le pagine 40 e 41. Provato: un byte scritto nella pagina 40 non si vede nella 41 e si ritrova tornando alla 40. | emu |
| `POKE a,v` | cap. 23, p. 249; App. B | `v a C!` | A | 008 | Prima il valore, poi l'indirizzo. Si scrive il byte basso di qualsiasi numero: nessun controllo sull'intervallo. | emu |
| `DPOKE a,v` | cap. 23, p. 249; App. B | `n a !` | A | 008 |  | emu |
| `PEEK a` | cap. 23, p. 249; App. B | `a C@` | A | 008 |  | emu |
| `DPEEK a` | cap. 23, p. 249; App. B | `a @` | A | 008 | Byte basso per primo, come in BASIC: `@` e `!` fanno già la conversione. | emu |
| meglio le forme `BANK` che `PEEK` / `POKE` diretti | cap. 23, p. 249 | - | C | 008, 025 | Al contrario: in Forth `C@` e `C!` su indirizzi assoluti sono il modo normale, perché il dizionario non si sposta. La memoria propria si prende con `CREATE` e `ALLOT`; sotto `$6200` c'è BASIC con lo schermo. |  |
| scrivere nello schermo (`POKE 16384,...` e poi `CLS`) | cap. 23, p. 250 | `255 $4000 C!` | A | 030 | Stessa memoria video del Layer 0, e `CLS` la cancella allo stesso modo. |  |
| esaminare una zona di memoria (ciclo di `PEEK`) | cap. 23, p. 256 | `a n DUMP`; oppure `: PEEKS ( a n -- ) BOUNDS DO I C@ . LOOP ;` -- `NEEDS DUMP` | A | 008, 022 | `DUMP` mostra esadecimale e caratteri. | emu |
| `PEEK$ (a,len)` | cap. 23, p. 256; App. B | `a len` è già una stringa: `TYPE`, `CMOVE` | C | 009 | Nessuna copia: la coppia indirizzo-lunghezza è la stringa. |  |
| `PEEK$ (a,~0)` (stringa con terminatore) | cap. 23, p. 256 | `: ZLEN ( a -- n ) DUP BEGIN DUP C@ WHILE 1+ REPEAT SWAP - ;` e poi `a DUP ZLEN` | B | 009 | Per un altro terminatore si cambia il test. Le chiamate a NextZXOS usano stringhe chiuse da zero o da `$FF`. | emu |
| cercare un testo in memoria (`PEEK$` in un ciclo) | cap. 23, p. 256 | ciclo con `(COMPARE)` | D-inc | - | Manca `SEARCH` (cap. 8). |  |
| `POKE a,lista` (byte, parole con `~`, stringhe) | cap. 23, p. 257 | una scrittura per valore: `C!`, `!`; una stringa: `S" test" a SWAP CMOVE`; molti valori: tabella con `C,` e `,` e poi `CMOVE` -- `NEEDS S"` | B | 008, 009 | Non c'è la lista: dati fissi si compilano in una tabella (cap. 5). | emu |
| `POKE` nella ROM non ha effetto | cap. 23, p. 258 | lo stesso | A | - | È l'hardware. |  |
| `CLEAR [n]` | cap. 23, p. 259; App. B | `FORGET nome` / `MARKER`; stack: `ABORT` | C | 005, 025 | Non ci sono variabili da azzerare in blocco. RAMTOP non si sposta: la mappa di memoria di vForth è fissa. |  |
| fare posto con `CLEAR n`, memoria esaurita | cap. 23, p. 259 | lo spazio si prende dal dizionario: `CREATE buf n ALLOT`; `UNUSED` dice quanto ne resta -- `NEEDS UNUSED` | C | 008, 025 | Niente RAMTOP da spostare. I nomi stanno a parte, nello heap (MMU7). | emu |
| quali banchi sono liberi | cap. 23, p. 251 | - | C | 041 | vForth tiene lo heap nei banchi 16-19 (pagine 32-39); il Layer 2 sta dove dice il NextReg `$12` (di norma banchi 9-11, pagine 18-23). I banchi 0, 2 e 5 sono la memoria in cui vForth gira, 7 e 8 sono di NextZXOS. Non c'è un allocatore pubblico (vedi `BANK NEW`). |  |
| `BANK NEW v` | cap. 23, p. 260 | - | D-inc | - | L'allocazione via `IDE_BANK` esiste solo dentro `inc/PAINT.f`. Senza, il programma sceglie le pagine a mano e NextZXOS non lo sa. |  |
| `BANK m CLEAR` | cap. 23, p. 260 | - | D-inc | - | Come sopra. |  |
| `BANK 1346 USR` / `FORMAT` | cap. 23, p. 261 | - | N | - | Gestione del RAMdisk. |  |
| `BANK m POKE o,lista` / `BANK m PEEK o` | cap. 23, p. 249; App. B | `pagina MMU7!` poi `C!` / `C@` a `$E000 + o` | C | 041 | BASIC conta in banchi da 16K; `MMU7!` vuole una pagina da 8K: banco m = pagine 2m e 2m+1, e un offset oltre 8191 cade nella seconda. | emu |
| `BANK m DPOKE` / `BANK m DPEEK` | cap. 23, p. 249 | `MMU7!` poi `!` / `@` | C | 041 | Una cella a cavallo dell'offset 8191 sta su due pagine. |  |
| `BANK m PEEK$ (o,len)` | cap. 23, p. 249 | `MMU7!` poi `$E000 o + len`, da copiare sotto `$E000` prima di rimettere la pagina | C | 041 | La stringa vale finché la pagina resta mappata. |  |
| `BANK m COPY TO n`, `BANK m COPY o,l TO n,o2` | cap. 23, p. 261 | `MMU7!` + `CMOVE` passando da un buffer; `DMA-COPY` -- `NEEDS DMA` | B | 041, 054 | MMU7 mostra una pagina alla volta: fra due banchi si passa da un buffer nel dizionario, 8K per volta al massimo. |  |
| `BANK m ERASE [o,l,][v]` | cap. 23, p. 261 | `MMU7!` poi `$E000 8192 v FILL` | B | 041 | Due pagine per banco. | emu |
| `BANK m LAYER x,y,w,h TO ...` (rettangolo fra schermo e banco) | cap. 23, p. 262 | - | D-inc | - | Per il solo Layer 2 è un ciclo di `CMOVE`, una riga di pixel per volta; con i formati di tutti i layer e le operazioni `&`, `\|`, `^`, `~` è un lavoro da libreria. |  |
| `LAYER BANK n,m` | cap. 23, p. 263; App. B | `n $12 REG!`, `m $13 REG!` -- `NEEDS L2-RAM-PAGE` | B | 046 | I NextReg `$12` e `$13` contano in banchi da 16K; `L2-RAM-PAGE` dà la prima pagina da 8K per `MMU7!`, ma è una costante calcolata al caricamento: se il Layer 2 viene spostato dopo, non lo segue. |  |
| `LAYER PALETTE n BANK b,o`, `SPRITE PALETTE n BANK b,o` | cap. 23, p. 263 | ciclo di `REG!` su `$41` (o `$44`) da una tabella | B | 056 | Vedi cap. 15 e 17. |  |
| `SPRITE BANK`, `TILE BANK`, `TILE DIM` | cap. 23, p. 264 | - | - | - | Vedi cap. 17 (`SPRITE-INIT`) e cap. 16 (D-lib). |  |
| `BANK m GO TO` / `GOSUB` / `PROC` / `LINE` / `LIST` / `MERGE` / `RESTORE` | cap. 23, p. 265 | - | N | 025 | Programmi BASIC in banchi. In vForth il codice sta nel dizionario e i nomi nello heap (MMU7). |  |
| come BASIC tiene programma e variabili | cap. 23, p. 253 | - | N | 022, 025 | Il corrispettivo è la struttura del dizionario (manuale vForth, "Dictionary memory structure"). |  |
| cambiare pagina dal prompt | cap. 23 | sempre dentro una definizione che rimette la pagina di prima: `MMU7@ >R ... R> MMU7!` | C | 041 | Trappola: in MMU7 sta lo heap con i nomi delle parole. Cambiando pagina dal prompt l'interprete non trova più niente. | emu |
| copiare e riempire memoria | cap. 23 | `CMOVE`, `FILL`, `ERASE`, `BLANK`; blocchi grandi `DMA-COPY`, `DMA-FILL` -- `NEEDS DMA` | A | 008, 054 |  | emu |
| paginazione con le MMU (NextReg `$50`-`$57`) | cap. 23, p. 269 | `n MMU7!`, `MMU7@` | A | 041 | È lo schema che vForth usa. Negli altri slot ci sono la ROM, lo schermo e vForth stesso. |  |
| Layer 2 mappato sulla ROM (porta `$123B`) | cap. 23, p. 269 | `n $123B P!`; di norma `MMU7!` sulle pagine del Layer 2 | B | 037, 041 | Le librerie grafiche di vForth passano da MMU7. La mappatura in sola scrittura sui 16K bassi lascia leggere la ROM; quella a 48K coprirebbe vForth. |  |
| i modi di paginazione di NextZXOS (porte `$7FFD`, `$1FFD`, allRAM), togliere la ROM | cap. 23, p. 265 | - | N | 041 | vForth usa solo le MMU; il resto va lasciato com'è. La ROM serve: stampa e tastiera passano di lì. |  |

## Capitolo 24 - The System Variables

| BASIC | Rif. manuale | vForth | Classe | Dove si impara | Nota | Verifica |
|---|---|---|---|---|---|---|
| le variabili di sistema (23296-23733) | cap. 24, p. 271 | agli stessi indirizzi: `a C@`, `a @`, `C!`, `!` | A | 008 | Valgono perché vForth stampa e legge la tastiera attraverso la ROM. In emulatore valgono quasi tutte 0 (fa eccezione LAST K, 23560): da vedere sulla macchina. |  |
| variabili a due byte (`PEEK n+256*PEEK (n+1)`) | cap. 24, p. 271 | `n @`, `v n !` | A | 008 | Come `DPEEK` e `DPOKE`: la cella è già nell'ordine giusto. | emu |
| le sigle X, N, R (da non toccare, senza effetto, routine) | cap. 24, p. 271 | lo stesso | A | - | Le routine di paginazione (23296 e seguenti) e BANKM non vanno toccate da vForth. |  |
| quelle che usa il core di vForth | cap. 24 | FLAGS 23611, LAST K 23560, FLAGS2 23658 (tastiera), FRAMES 23672, BORDCR 23624, SCR CT 23692, RAMTOP 23730 | A | - | Dai sorgenti in `project/vForth18_DOES/source/`. Scriverci a mano cambia il comportamento del prompt. |  |
| quelle che usano le librerie | cap. 24 | SEED 23670 (`RND`, `RANDOM`, `RANDOMIZE`), UDG 23675 (`UDG@`) | A | - | Trovate cercando gli indirizzi in `src/`, `inc/` e `lib/`. Sono le stesse di BASIC: un seme o un UDG impostati da BASIC valgono anche qui. |  |
| FRAMES 23672 | cap. 24, p. 272 | `23672 @` | A | 032 | Vedi cap. 17. |  |
| SCR CT 23692, ATTR P 23693, BORDCR 23624, CHARS 23606, PIP 23609, RASP 23608 | cap. 24, p. 272 | `C@` / `C!`; CHARS con `@` / `!` | A | - | Vedi cap. 13, 14, 15 e 18. RASP (il ronzio dell'editor di BASIC) in vForth non ha effetto. |  |
| le "variabili di sistema" di Forth | cap. 24 | variabili utente: `BASE`, `STATE`, `DP`, `>IN`, `BLK`, `SPAN`, `OUT`, `WARNING` | C | 022 | Sono parole, non indirizzi da ricordare: `BASE @`, `HEX`. |  |

## Capitolo 25 - Using Machine Code

| BASIC | Rif. manuale | vForth | Classe | Dove si impara | Nota | Verifica |
|---|---|---|---|---|---|---|
| linguaggio macchina e assembler | cap. 25, p. 275 | `lib/assembler.f`: mnemonici in notazione postfissa dentro `CODE nome ... C;` -- `NEEDS ASSEMBLER` | B | 027 | In più rispetto a BASIC, che non ha un assembler: quello di vForth sta nel sistema e compila direttamente nel dizionario. |  |
| dove mettere il codice (`CLEAR n` e sopra RAMTOP) | cap. 25, p. 275 | nel dizionario: una parola `CODE nome ... C;` | C | 027 | Il codice ha un nome e si chiama come ogni altra parola; niente indirizzi da ricordare. |  |
| scrivere il codice (byte in `DATA` e `POKE`) | cap. 25, p. 275 | i byte in esadecimale con `C,` dentro `CODE nome` ... `SMUDGE` | B | 027 | I file di `inc/` usano l'esadecimale per non dover caricare l'assembler. |  |
| `USR a` | cap. 25, p. 276; App. B | `n a CALL#`; codice proprio: `CODE nome ... C;` -- `NEEDS CALL#` | C | 027, 057 | `CALL# ( n1 a -- n2 )` passa n1 in BC e in A, chiama l'indirizzo e restituisce BC, come `USR`; conserva lei i registri di Forth. Di norma il linguaggio macchina si scrive come parola `CODE`. Nessun tutorial su `CALL#`. In emulatore: `0 a CALL#` sui quattro byte del manuale dà 99. | emu |
| `ld bc,99: ret` come esempio | cap. 25, p. 275 | `CODE NN99 HEX 21 C, 63 C, 0 C, E5 C, DD C, E9 C, SMUDGE DECIMAL` | B | 027 | Il risultato non torna in BC ma sullo stack (`ld hl,99: push hl`), e si esce con `jp (ix)` invece di `ret`. | emu |
| passare e ricevere valori (BC, parametri di `USR`) | cap. 25, p. 276 | lo stack dei dati: `POP HL` ... `PUSH HL` | C | 027 | Quanti parametri si vuole, in entrata e in uscita. Vanno conservati BC (puntatore di istruzione), DE (return stack) e IX; IY resta alla ROM, come in BASIC. |  |
| `USR$ a` (codice che restituisce una stringa) | cap. 25, p. 276 | la parola `CODE` lascia indirizzo e lunghezza sullo stack | C | 027 | Una stringa è `a u` anche per il linguaggio macchina. |  |
| `BANK n USR o` | cap. 25, p. 276 | `MMU7!` poi `CALL#` -- `NEEDS CALL#` | B | 041 | Il codice deve essere scritto per girare a `$E000`. |  |
| salvare e ricaricare il codice (`SAVE` / `LOAD ... CODE`) | cap. 25, p. 277 | `SAVE-BYTES`; `LOAD-BYTES` in una zona riservata con `ALLOT`, poi `CALL#` -- `NEEDS SAVE-BYTES`, `NEEDS LOAD-BYTES`, `NEEDS CALL#` | B | 042 | Più naturale tenere il sorgente e ricompilarlo con `INCLUDE`. |  |
| caricatore BASIC che lancia il codice (`SAVE "loader" LINE 10`) | cap. 25, p. 277 | - | N | 059 | È quello che fa `Forth18_loader.bas` per avviare vForth. Per un eseguibile autonomo: `ZAP`. |  |
| interrupt, registro I, stack durante la paginazione | cap. 25, p. 277 | `lib/INTERRUPTS.f` -- `NEEDS INTERRUPTS` | B | 049 | La libreria imposta il modo IM 2 (la tabella dei vettori è a `$6200`). Le avvertenze del manuale valgono per chi scrive una routine di interrupt a mano. |  |
| chiamare NextZXOS (cambio di ROM e RAM, stack sotto `$BFE0`) | cap. 25, p. 278 | `hl de bc a indirizzo M_P3DOS ( -- hl de bc a f )` | B | 057 | La primitiva del core fa da sola il cambio di ROM, banco e stack che l'esempio del manuale scrive a mano; restano da preparare i registri e controllare il flag. Il catalogo dell'esempio (`DOS_CATALOG`, `$011E`) è già `DIR`. |  |
| le chiamate di NextZXOS già pronte | cap. 25, p. 278 | `F_OPEN`, `F_READ`, `F_WRITE`, `F_SEEK`, `IDE_RTC`, `M_GETDATE` e le altre `F_...` | A | 042, 057 | Le più comuni sono già parole (cap. 19 e 20); per le altre `M_P3DOS`. |  |
| istruzioni Z80N e prefissi dei codici operativi | cap. 25, p. 281 | in esadecimale (`ED C, 30 C,` è `MUL`); l'assembler ha `NEXTREG` e `NEXTREGA` | A | 027 | Esempi in `inc/RND.f`. Da verificare quali altre istruzioni Z80N conosce `lib/assembler.f`. |  |

## Cosa esce dalla matrice

### Correzioni alla ricognizione del piano (sez. 10)

- **`INKEY` non esiste.** In `src/F18e.f` la definizione è commentata. La
  lettura senza attesa passa da `?TERMINAL`, `?ESCAPE` o dalla matrice dei
  tasti (`KEY-DOWN?`).
- **`RENAME` non rinomina un file**: rinomina una parola del dizionario. Per i
  file c'è la primitiva `F_RENAME`.
- **`SAVE-BANK` non è un `SAVE ... BANK` generico**: fa parte di `lib/ZAP.f` e
  accetta solo i banchi 16-19 dello heap.

### Trovato provando i cap. 1-7 in emulatore (2026-10-12)

- **`+"` dà una stringa sbagliata.** `H" abc" +" def" FAR COUNT TYPE` stampa
  `bc!def` (o `bcw def`), e la lunghezza letta subito dopo è 145 invece di 6.
  `H" abc" FAR COUNT TYPE` da solo funziona. Da capire se è un difetto di
  `inc/+~.f`, un uso sbagliato (l'help dice solo "Appends string to Heap") o
  un limite dell'emulatore: va riprovato su CSpect.
- **`1 0 /` non dà errore**: nessun messaggio, resta un valore sullo stack.
- **Il punto in un numero non è la virgola**: `3.5 .` stampa 0. È la trappola
  più probabile per chi arriva da BASIC, da mettere in "What changes" del
  cap. 6.
- **Un intero oltre 65535 è troncato senza avviso**: `70000 .` dà 4464.
- **`FORGET nome` porta via anche tutto ciò che è stato definito dopo**,
  comprese le parole caricate con `NEEDS` nel frattempo.
- **Vero è -1**, e la divisione tronca verso lo zero (`-7 2 /` dà -3,
  `-7 2 MOD` dà -1).
- `OUT @` dopo aver stampato un solo numero vale qualche migliaio: sembra un
  contatore dei caratteri emessi, non la colonna. La nota della riga `OUT`
  (cap. 22) dice "colonna di stampa" ed è da ricontrollare.

### Trovato provando i cap. 8-14 in emulatore (2026-10-12)

- **`ACCEPT` restituisce i caratteri letti più uno.** `PAD 20 ACCEPT .` con
  `Simon` stampa 6: il conteggio comprende il terminatore. Il tutorial 016 lo
  sa (`?NUMBER` comincia con `1-`), ma l'intestazione nel core dice "n2 is the
  string length". È la trappola del cap. 14: chi usa il numero come lunghezza
  si porta dietro un byte a zero.
- **`COMPARE` non distingue maiuscole e minuscole**: `EVIL` contro `evil` dà
  0. Passa da `(COMPARE)`, che segue `CASEON` / `CASEOFF`; l'help dice solo
  "0 if equal". In BASIC `"EVIL"<"evil"`. Con `CASEON` torna -1 (provato).
- **`SQRT` prende una cella, non un doppio**: `16 SQRT .` dà 4, `16. SQRT .`
  dà 0. Il commento `( d -- n )` in `inc/SQRT.f` è sbagliato (il doppio lo
  costruisce lei con `0 DSQRT`); la riga del cap. 9 diceva "vuole un doppio"
  ed è stata corretta.
- **`RND` segue la sequenza di `RND` in virgola mobile di BASIC**, non quella
  che il manuale dà per `%RND`: dopo `1 RANDOMIZE` SEED diventa 149 (cioè
  0.0022735596, il valore del manuale) e `100 RND` dà 0, mentre il manuale
  dice che `%RND 100` comincia con 97. Da chiarire su CSpect quale delle due
  cose fa davvero NextBASIC.
- **`NUMBER` vuole lo spazio in fondo**: su una stringa creata con `,"` dà
  `is undefined` anche se il testo è un numero valido, perché dopo l'ultima
  cifra non trova lo spazio. `>NUMBER` e `(NUMBER)` non hanno il problema.
- **Nessun controllo, come previsto**: `300 EMIT` stampa `,`; `99 M @` su un
  array di 10 elementi legge e basta; `2 16 **` dà 0.
- **I nomi non distinguono maiuscole e minuscole**: `CREATE evil` dopo
  `CREATE EVIL` avvisa `EVIL has already been defined.` e da lì entrambi i
  nomi trovano la seconda.
- **Non ci sono `SEARCH`, `SCAN`, `/STRING`, `**`, `<=`, `>=`**: i primi tre
  pesano su tutto quello che nei cap. 7, 8 e 11 riguarda le stringhe.

### Trovato nel primo giro sui cap. 15-25 (2026-10-12)

- **`OUT` non è la colonna di stampa**: `OUT @` vale 14804 dopo una trentina
  di righe. È un contatore dei caratteri emessi; la riga del cap. 22 è stata
  corretta.
- **MMU7 dal prompt**: la pagina corrente è la 32 (lo heap con i nomi). Le
  prove di `MMU7!` sono fatte dentro definizioni che rimettono la pagina di
  prima; è la forma da mostrare nel cap. 23 della guida.
- **`L2-RAM-PAGE` è una costante calcolata al caricamento** (da NextReg
  `$12`): se il Layer 2 viene spostato dopo, non lo segue.
- **Vuoti nuovi**: una `PAUSE` che un tasto interrompe, `TIME` (azzerare e
  leggere FRAMES), una parola per mostrare e nascondere il Layer 2.

### Trovato rileggendo i cap. 15 e 17-25 (2026-10-12)

Correzioni a righe del primo giro:

- **`SCREEN-FROM-FILE` non carica un'immagine**: copia un file di testo in
  uno Screen del file dei blocchi (`SCREEN-TO-FILE` fa il contrario). Era
  citata nei cap. 17 e 19 come caricatore di schermate.
- **`PIXELATT ( b a -- )` scrive un attributo, non lo legge**: la riga `ATTR`
  del cap. 15 la dava come lettura.
- **`DIR` non dà "solo l'elenco"**: è ordinato e mostra dimensione, data e
  ora, con il totale. Corrisponde a `CAT EXP` senza gli attributi.
- **`COPY` da file a file passa da D-lib a D-inc**: provata in emulatore una
  `FCOPY ( fh1 fh2 -- )` di tre righe (`F_READ` / `F_WRITE` su un buffer di
  256 byte). Resta da libreria la forma con i caratteri jolly.
- **`LPRINT` e `LLIST` passano da D-inc a B**: `SELECT` chiama la routine
  della ROM che attiva uno stream, e il commento nel core dice che il 3 è la
  stampante. Resta da provare con una stampante.
- **`PLOT` controlla da sé le coordinate** (`COORD-CHECK` dentro `L0-PLOT`) e
  scarta in silenzio il punto fuori schermo; `PLOT INVERSE` è `' L0-RES IS
  PLOTOP`. Le due righe del cap. 16 dicevano "da verificare".

Trappole e particolarità nuove:

- **`CD` rompe `NEEDS`**: i percorsi `inc/` e `lib/` sono relativi alla
  cartella corrente. È scritto nell'intestazione di `inc/CD.f`; va in "What
  changes" del cap. 19.
- **`F_GETLINE` conta anche il fine riga**: su `Hello` seguito da a capo
  lascia 6. È la stessa sorpresa di `ACCEPT` (cap. 14).
- **`LOAD-BYTES` non dà errore su un file più corto**: carica quello che
  c'è. `SAVE-BYTES` su un file che esiste dà `NextZXOS Open error`.
- **Intestazione +3DOS**: `SAVE-BYTES` scrive byte nudi; un file fatto da
  BASIC con `SAVE ... CODE` ha davanti l'intestazione. Da provare su CSpect
  in tutti e due i versi prima di scrivere il cap. 19 della guida.
- **Un errore non chiude i file**: gli handle restano aperti dopo `ERROR`.
- **`.NOW` stampa data, ore e minuti ma non i secondi**: in
  `inc/.FAT-TIME.f` la riga dei secondi è commentata. I secondi esatti li dà
  solo `M_GETDATE`.
- **`SPRITE` è un omonimo**: in `lib/SPRITE.f` è la struttura di lavoro. Il
  campo `_spriteid` è il pattern, `_pattern` è lo scostamento di palette, e
  `SPRITES-ON` riscrive tutto il NextReg `$15` (sprite sopra il bordo, ordine
  dei layer a 0).
- **`SPRITE-UPDATE` manda quattro attributi ma accende il bit 6
  dell'attributo 3** (`$C0`), che annuncia un quinto byte: funziona su CSpect
  (tutorial 053), ma è da capire se è voluto.
- **Il Copper**: la libreria scrive l'istruzione a 16 bit nel NextReg `$63`,
  il manuale usa `$60` un byte per volta; `COP-WAIT` vuole prima la riga.
- **`BEEP` accetta solo semitoni interi**; per le altre frequenze
  `BLEEP-CALC`. `0 BEEP-PITCH` dà 2093 (261,6 Hz per 8).
- **Registro 7 del chip AY**: il bit a 0 accende, al contrario di `M` in
  `PLAY`.
- **La seconda metà del banco 5 (pagina 11) non è a `$6000`**: lì gira
  vForth. `L12-PIXELADD` mappa le pagine 10 e 11 in MMU7.
- **`M_P3DOS` fa da sola il cambio di ROM, banco e stack** che il cap. 25
  del manuale scrive a mano in una pagina di assembler.
- **`CALL#` è `USR`**: sui quattro byte dell'esempio del manuale (`ld bc,99:
  ret`) dà 99.

### Candidati `inc/` (classe D-inc)

Dai cap. 1-7: `<=` e `>=`, `/STRING`, una parola che copia una stringa in una
variabile contata (il `PLACE` degli altri Forth), le minuscole, lo scarto degli
spazi iniziali, la sostituzione di caratteri.

Dai cap. 8-14: la ricerca in una stringa (`IN`: `SCAN` per un carattere,
`SEARCH` per una sottostringa), la potenza fra interi (`**`), `UDG!` (copia di
otto byte nella matrice di un UDG), e le definizioni provate qui che si
possono promuovere così come sono: `SGN`, `INPUT#`, `ARRAY`, `MATRIX`,
`SARRAY` con `S!`.

Dalle voci di Appendice B:
un "chiedi un numero" (`INPUT`), il segno di un intero (`SGN`), `SCREEN$`,
`PRINT POINT`, `LAYER ERASE`, `LAYER CLEAR`, `PALETTE CLEAR`, l'arco di `DRAW`,
`BANK NEW` / `BANK CLEAR` (allocazione di banchi), `BANK ... LAYER`, `DRIVER`,
un casuale fra 0 e 1.

Dai cap. 17-25: `PAUSE` (a quadri, interrompibile da un tasto) e `FRAMES`,
`TIME` (azzerare e leggere il contatore dei quadri), `TIME$` come stringa e
con i secondi, la collisione fra due sprite (`HIT?`), il quinto attributo
degli sprite (ingrandimento), la copia di un file (`FCOPY`), la lunghezza di
una stringa chiusa da zero (`ZLEN`), una parola per mostrare e nascondere il
Layer 2, `LAYER OVER`, `LAYER AT` e `SPRITE DIM` come parole invece di
`REG!` a mano.

### Mancano e servirebbe una libreria (classe D-lib)

`PLAY`, il tiling software (`TILE`), gli sprite oltre il minimo (relativi,
compositi, movimento automatico), l'audio digitale (WAV, MOD, PT3), le
finestre utente di NextZXOS con il loro `INPUT`, la finestra di scelta di un
file (`.browse`), la copia di file con i caratteri jolly.

### Righe senza tutorial

`RANDOMIZE` / `RND` / `CHOOSE`, `UNLOOP`, `.PERM`, `.TAB`, le funzioni
trigonometriche inverse e `FLN`, `MAKEDIR` / `REMOVEDIR` / `UNLINK`, UDG (`lib/udg+.f`), orologio
(`IDE_RTC`, `M_GETDATE`, `.NOW`), `F_RENAME` / `F_CHMOD` / `F_FSTAT`,
`F_SEEK` / `F_FGETPOS`, `REMOUNT`, `CALL#` e `M_P3DOS`, `BYE` / `BASIC`,
array di stringhe, `BETWEEN` / `WITHIN`, `WIDECHAR` / `NARROWCHAR` e i
codici di controllo 29 e 30, `RND` (i tutorial usano solo `CHOOSE` e
`RANDOM`). Coincidono in buona parte con l'elenco dei tutorial nuovi
del piano (sez. 9).

Dai cap. 17-25 si aggiungono: `SELECT` (usato in 20 tutorial, spiegato in
nessuno), `OPEN>`, `F_GETLINE`, `F_GETCWD`, `M_GETSETDRV`, `WILDCARD`,
`DOSVER`, `WAIT-KEY`, `.FREE-SIZE` / `.FILE-SIZE`, la finestra di clip degli
sprite, i codici di controllo delle finestre di sistema e `PAUSEOFF`.

### Omonimi da mettere in "What changes"

`:` (cap. 1); `(`, `@`, `AND` / `OR` / `NOT` (cap. 6); `PLACE` (cap. 7);
`EXIT`, `REPEAT` (cap. 3); `LIST`, `ERROR`, `ERASE` (cap. 1 e 19); `LOAD`,
`SAVE`, `RENAME` (cap. 19); `OVER` (cap. 15); `CODE` (cap. 13); `EXP`
(cap. 9); `OUT` (cap. 22); `IN` (cap. 8: in BASIC è anche la ricerca in
una stringa, oltre alla lettura di una porta); `SPRITE` (cap. 17: in
`lib/SPRITE.f` è una struttura); `KEY` (cap. 18: il manuale chiama `key` la
variabile del trasporto); `DIR` (cap. 19: stesso nome, uscita più ricca).

### File di help da rivedere

Trovati leggendo gli help per compilare la colonna vForth; non corretti.

- Testo che non corrisponde alla parola: `p!.txt` e `p@.txt` ("paged byte":
  sono le porte di I/O), `select.txt` ("layer or memory page": sceglie lo
  stream di uscita), `reg!.txt` e `reg@.txt` ("NextZXOS system register":
  sono i NextReg), `video.txt` ("Set video mode": riporta l'uscita
  sullo schermo, `2 SELECT`).
- Commenti nei sorgenti che non corrispondono: `inc/SQRT.f` (`( d -- n )`,
  ma prende una cella), `ACCEPT` in `src/F18e.f` ("n2 is the string length":
  è la lunghezza più uno), `help/compare.txt` (non dice che il confronto
  segue `CASEON` / `CASEOFF`).
- Nomi che ingannano: `SCREEN-FROM-FILE` / `SCREEN-TO-FILE` (lo "screen" è
  uno Screen del file dei blocchi, non lo schermo), i campi `_spriteid` e
  `_pattern` di `lib/SPRITE.f`.
- Senza voce di help: `RND`, `PAINT`, `DRAW`, `DRAW-CIRCLE`, `POINT`,
  `PIXELADD`, `PIXELATT`, `IDE_RTC`, `.NOW`, `CALL#`, `UDG+`, `F_CHMOD`,
  `F_FSTAT`, `REMOUNT`, `VIEW`, `IDE_MODE!`, `PAUSEOFF`, `LAYER13`, `ZAP`, le
  parole di `lib/SPRITE.f`.

## Da provare su CSpect o sulla macchina

È quello che resta della fase 1: righe la cui colonna vForth viene dai
sorgenti e non da una prova. In ordine di peso per la guida.

1. **Grafica e colori (cap. 15-16)**: `PLOT`, `DRAW-LINE`, `CIRCLE`, `POINT`,
   `PAINT`, `XPLOT`; `.INK` 8 e 9; quando la ROM riporta il colore temporaneo
   al permanente; `' L0-RES IS PLOTOP`; la pagina 11 in MMU7 per il secondo
   file video; `LAYER 2,0` / `2,1` con il bit 7 del NextReg `$69`.
2. **File (cap. 19)**: `DIR` con e senza `WILDCARD`; `CD` e `PWD`, e `NEEDS`
   dopo un `CD`; `MAKEDIR`, `REMOVEDIR`, `UNLINK`; `F_RENAME`; `F_CHMOD`
   contro `MOVE ... TO "+p"`; l'intestazione +3DOS fra `SAVE ... CODE` di
   BASIC e `LOAD-BYTES`, e fra `SAVE-BYTES` e `LOAD ... CODE`.
3. **Stream (cap. 20)**: `3 SELECT` verso la stampante; `SELECT` verso un
   file aperto in BASIC; `DIR`, `PWD` e `VIEW` dopo `SELECT`; `F_FSTAT` e
   l'ordine delle due celle della dimensione; i codici di controllo delle
   finestre di sistema (24, 26, 28, 29, 30) in `LAYER12`.
4. **Tempo (cap. 17 e 21)**: `23672 @` che avanza; `.NOW`, `IDE_RTC` e
   `M_GETDATE` con e senza modulo RTC; la `PAUSE` interrompibile con un
   tasto vero.
5. **Sprite e Copper (cap. 17)**: `SPRITE DIM` su `$19`; lo scorrimento con
   `$16` / `$17`; la definizione `SKY` del Copper; il bit 6 dell'attributo 3.
6. **Suono (cap. 18)**: `BEEP` agli estremi dell'intervallo; il clic dei
   tasti con `23609`; i registri del chip AY.
7. **Dai cap. 1-14, già in elenco**: `%RND` contro `RND` dopo `RANDOMIZE 1`;
   `+"`; `RANDOMIZE` con FRAMES; UDG e CHARS; `PRINT AT` fuori schermo;
   lo scroll a fine schermo; i token con `EMITC`.
