# NextBASIC contro vForth -- matrice di corrispondenza

> Stato: IN CORSO (2026-10-12). Primo giro completo sulle voci di Appendice B
> (179 righe). Concetti dei capitoli e prova in emulatore: fatti per i cap.
> 1-7. Restano: concetti e prova dei cap. 8-25.

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
- **Comportamento: provato per i cap. 1-7** (colonna Verifica). Per gli
  altri capitoli effetto sullo stack e semantica vengono dalle intestazioni dei
  sorgenti e dai file di help, non da una prova. Le righe con "Da verificare"
  nella nota sono quelle più incerte.
- **Cosa resta senza `emu` nei cap. 1-7**: le righe C, D e N che non hanno
  uno spezzone da provare; quelle che qui non si possono provare (tutto ciò
  che passa da `FLOATING`, perché l'emulatore non ha il calcolatore della ROM;
  `EDIT` / `LED`; `?TERMINAL`); e alcune semplicemente non ancora provate:
  `INPUT` di un numero (`NUMBER` dopo `ACCEPT`), `REM`, `LIST`, l'assegnazione
  multipla, e nel cap. 3 le quattro righe rimaste vuote.
- **I listati BASIC non sono provati**: i valori attesi lato BASIC vengono dal
  manuale.
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
| 1 | Basic Programming Concepts | 30 | fatto | fatto | emu (18 righe) |
| 2 | Decisions | 13 | fatto | fatto | emu (12 righe) |
| 3 | Looping | 16 | fatto | fatto | emu (12 righe) |
| 4 | Procedures and Subroutines | 19 | fatto | fatto | emu (15 righe) |
| 5 | READ, DATA, RESTORE | 10 | fatto | fatto | emu (8 righe) |
| 6 | Expressions | 21 | nessuna voce | fatto | emu (18 righe), virgola mobile esclusa |
| 7 | Strings | 17 | nessuna voce | fatto | emu (12 righe) |
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
| `LET v=e` | cap. 1, p. 5; App. B | `e v !` (con `VARIABLE v`); `e TO v` (con `VALUE`); oppure nessun nome, il valore resta sullo stack | C | 005, 008 | `VARIABLE` non prende un valore iniziale e parte da 0. Molti valori che in BASIC hanno un nome in Forth vivono solo sullo stack. | emu |
| `PRINT` items | cap. 1, p. 10; App. B | `.` `."` `TYPE` `EMIT` `CR` `SPACE` | B | 001, 003 | Nessun a capo automatico: `CR` va scritto. `.` consuma il numero che stampa. Niente separatori `;` e `,`. | emu |
| `REM` ..., `;` ... | cap. 1, p. 10; App. B | `\ ...` fino a fine riga; `( ... )` | A | 001 | `(` vuole uno spazio dopo di sé: è una parola. |  |
| `NEW` | cap. 1, p. 9; App. B | `COLD`; `FORGET nome`; `MARKER nome` | B | 005, 022 | Non c'è un programma da cancellare: si dimenticano le definizioni fatte dopo un certo punto. | emu |
| `INPUT v` | cap. 1, p. 10; App. B | `ACCEPT` poi `NUMBER` o `(NUMBER)` | B | 016, 021 | Manca una parola unica "chiedi un numero": il tutorial 016 la costruisce (`ASK-NUMBER`). Candidata D-inc. |  |
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
| `INPUT a$` | cap. 1, p. 11 | `PAD 20 ACCEPT` (lascia la lunghezza; il testo è in `PAD`) | B | 016 | Niente virgolette e nessuna espressione in ingresso: per valutare quello che si è letto, `EVALUATE`. | emu |
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
| concatenazione `+` | cap. 7, p. 50 | accodare in un buffer: `CMOVE` e somma delle lunghezze; nello heap `+"` -- `NEEDS +"` | B | 009 | Provata solo la via del buffer. Da verificare `+"`: in emulatore `H" abc" +" def"` dà una stringa sbagliata. | emu |
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

### Candidati `inc/` (classe D-inc)

Dai cap. 1-7: `<=` e `>=`, `/STRING`, una parola che copia una stringa in una
variabile contata (il `PLACE` degli altri Forth), le minuscole, lo scarto degli
spazi iniziali, la sostituzione di caratteri.

Dalle voci di Appendice B:
un "chiedi un numero" (`INPUT`), il segno di un intero (`SGN`), `SCREEN$`,
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

`:` (cap. 1); `(`, `@`, `AND` / `OR` / `NOT` (cap. 6); `PLACE` (cap. 7);
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
