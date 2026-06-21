# tutorial/ vs Screen# 800-881 -- raffronto

Confronto fra i due percorsi didattici del progetto vForth:

- **tutorial/** -- corso vForth originale (file `NNN-slug.f`), organizzato per
  argomento, con nomi di esempio propri (`SHOW-SUM`, `.RANGE`, `CLAMP`,
  `SAFE-DIV`, ...).
- **Screen# 800-881** in `!Blocks-64.bin` -- trascrizione e adattamento a vForth
  dei brani di codice del libro *Starting FORTH* di Leo Brodie
  (`doc/Starting-FORTH.pdf`), organizzati per capitolo del libro (Ch.1-10) e con
  i nomi originali di Brodie (`STAR`, `GREET`, `EGGSIZE`, `R%`, `DIAMONDS`, ...).


## Sintesi

I due materiali sono **paralleli ma indipendenti**. A livello di *nome di
definizione* la sovrapposizione e' di fatto nulla: i due percorsi insegnano gli
stessi concetti Forth con definizioni diverse. La condivisione e' quindi
**concettuale**, non lessicale.

Inoltre gli Screen coprono soltanto i capitoli 1-10 di *Starting FORTH* (puro
Forth standard da libro), mentre i tutorial proseguono ben oltre, fino all'intera
traccia hardware dello ZX Spectrum Next.


## Raffronto sinottico-concettuale (argomenti presenti in ENTRAMBI)

| Capitolo Brodie / Screen#       | Tutorial/ corrispondente                                   | Concetto condiviso                                                        |
|---------------------------------|------------------------------------------------------------|--------------------------------------------------------------------------|
| Ch.1 -- 800-804                 | 003-output, 005-defining-words                             | `:` definizioni, `." "`, `EMIT`, `CR`, `SPACES`                          |
| Ch.2 -- 805-814                 | 001-stack-basics, 002-stack-ops                           | aritmetica postfix, `DUP/SWAP/ROT/OVER`, `/MOD`, `.S`, `3DUP`            |
| Ch.4 -- 816-820                 | 006-control-flow                                          | `IF/ELSE/THEN`, `?DUP`, IF annidati, `WITHIN`                            |
| Ch.5 -- 821-825                 | 002-stack-ops, 015-double-arith                           | `*/`, `MIN/MAX/ABS`, percentuali, conversioni                           |
| Ch.6 -- 826-837                 | 007-loops                                                 | `DO/LOOP`, `+LOOP`, `?DO`, `I/J`, `LEAVE`, `BEGIN/UNTIL/WHILE`           |
| Ch.7 -- 838-849                 | 014-pictured-output, 004-numeric-bases                   | `<# # #S #> HOLD SIGN`, `.R/U.R`, `BASE`, `HEX/DECIMAL/BINARY`           |
| Ch.8 -- 850-867                 | 005-defining-words, 008-memory, 010-create-does, 023-structures | `VARIABLE/CONSTANT`, `!/@/+!`, `CREATE/ALLOT/,/C,`, array, `[COMPILE] CONSTANT` |
| Ch.8 (double) -- 854-855, 864   | 015-double-arith                                          | `2VARIABLE/2CONSTANT`, `2@/2!`, `D./D+/M+`                               |
| Ch.9 -- 868-876                 | 017-defer-is, 022-introspection                          | `'`/`[']`/`EXECUTE`, esecuzione vettorizzata (`'ALOHA` <-> `DEFER`), `SEE` |
| Ch.10 -- 877-881                | 009-strings, 016-input                                   | `TYPE`, `-TRAILING`, stringhe, I/O                                       |


## Solo sugli Screen# (esempi specifici del libro Brodie)

Definizioni e interi argomenti presenti **solo** negli Screen, assenti dai
tutorial:

- **Ch.3 "The Editor" (815):** `NEEDS EDIT` / `NEEDS LED` -- nessun tutorial
  dedicato all'editor.
- **Esempi-firma di Brodie** mai ripresi: la lettera `F`
  (`STAR/BAR/BLIP/MARGIN`), `GIFT/GIVER/THANKS`, le condanne penali
  (`CONVICTED-OF...WILL-SERVE`, `HOMICIDE`, `ARSON`), `EGGSIZE/CATEGORY/LABEL`,
  `DIAMONDS/TRIANGLE/\STARS//STARS`, `COMPOUND/DOUBLED` (interesse composto),
  `**` (potenza), conversioni temperatura `F>C/C>F/K>C`,
  `.PH#/.DATE/SEC/SEXTAL/.$` (output formattato), tic-tac-toe
  (`BOARD/X!/O!/DISPLAY`), pencils (`ENUMERATED/PENCILS`), histogram
  (`'SAMPLES/PLOT`), `ALOHA/SAY/COMING/GOING`, il **Buzzphrase Generator**
  (880-881), `'S`, `N-MAX`, `3BELLS`, `QUADRATIC`, `DPOLY`.
- **Uso del sistema BLOCK/Screen** come storage (`214 BLOCK ... TYPE`, `LOAD`,
  `-->`, `MARKER TASK ... LOAD`): didattica block-based che i tutorial non usano.


## Solo su tutorial/ (estensioni vForth, fuori dal raggio di Brodie Ch.1-10)

- **013-case** -- `CASE/OF/ENDOF` (Brodie usa solo IF annidati; lo Screen 876 ha
  `EXEC:` vettorizzato, non `CASE`).
- **011-bit-ops** -- operazioni bit Z80N (`.BITS`, `BIT-SET/CLEAR/TOGGLE`, hi/lo
  byte).
- **018-vocabularies** -- vocabolari come argomento autonomo (Brodie li tocca
  solo di sfuggita in 872).
- **019-compilation / 020-standard** -- `STATE`, `COMPILE`/`POSTPONE`/`COMPILE,`,
  `IMMEDIATE`, `[ ]`: corrisponde al **Ch.11 di Brodie, NON trascritto** negli
  Screen (che si fermano al Ch.10).
- **021-evaluate** -- `EVALUATE`, parsing token (`NEXT-TOKEN`, `CALC-STRING`).
- **024-floating-point** -- pacchetto floating vForth (assente in Brodie).
- **025-memory-advanced**, **026-catch-throw** (`CATCH/THROW`), **027-assembler**
  (`CODE`, `VIDEO-SYNC`, `CHECKSUM2`).
- **Intera traccia hardware ZX Spectrum Next -- 030-053** (30 tutorial):
  ULA/Layer2/sprite, AY, copper, Next-registers, MMU, file I/O, mouse, UART/RPi0,
  interrupt, keyboard-matrix, grafica modulare. **Nessun corrispettivo** negli
  Screen, che sono puro Forth standard da libro.


## Mappa riga-per-riga delle definizioni equivalenti

La mappa **non e' biiettiva**: e' many-to-many. Lo stesso esempio di Brodie fa
da controparte a piu' demo-word del tutorial (es. lo Screen 826 `DECADE` copre
sia `COUNT-UP` sia `.RANGE`; lo Screen 854 `DATE` sia `COUNTER` sia `TOTAL`; lo
Screen 829 `FALLING` sia `COUNT-DOWN` sia `.DOWN`; gli Screen 852/865/867
ricorrono piu' volte). La colonna **Forza** distingue le coincidenze concettuali
nette (`solido`, ~40 righe) da quelle solo affini (`approssimato`, ~18 righe);
totale **58 righe**.

| # | Tutorial (file)                  | Screen#            | Concetto condiviso                         | Forza        |
|---|----------------------------------|--------------------|--------------------------------------------|--------------|
| 1 | `SHOW-SUM` (001)                 | `5#SUM` (807)      | combinare + stampare aritmetica            | approssimato |
| 2 | `SHOW-DIVMOD` (001)              | `QUARTERS` (809)   | `/MOD` con stampa                          | solido       |
| 3 | `SQUARE` (002)                   | `2C5` (811)        | `DUP` per quadrato / polinomio             | approssimato |
| 4 | `MIN-MAX` (002)                  | `4MAX` (823)       | `MIN`/`MAX` in catena                      | approssimato |
| 5 | `.LABELED` (003)                 | `WILL-SERVE` (814) | numero + etichetta testuale                | approssimato |
| 6 | `.HEX-AND-DEC` (003)             | `EXAMPLE` (843)    | cambio `BASE` in stampa                    | solido       |
| 7 | `.RULER` (003)                   | `RECTANGLE` (828)  | pattern stampato in loop                   | approssimato |
| 8 | `.BASES` (004)                   | `NUMS` (848)       | stesso numero in DEC/HEX/BIN               | solido       |
| 9 | `.BYTE` (004)                    | `NUMS` (848)       | formattazione in base con `.R`             | approssimato |
|10 | `SCORE`/`LIVES-LEFT` (005)       | `EGGS` (852)       | `VARIABLE` contatore                       | solido       |
|11 | `INIT-GAME` (005)                | `RESET` (852)      | azzerare una variabile (`0 X !`)           | solido       |
|12 | `AWARD-POINTS` (005)             | `EGG` (852)        | incremento con `+!`                        | solido       |
|13 | `SHOW-STATUS` (005)              | `.DATE` (851)      | stampa di stato via `?`                     | approssimato |
|14 | `.POSITIVE` (006)                | `?FULL` (816)      | `IF...THEN` semplice                       | solido       |
|15 | `.SIGN` (006)                    | `?DAY` (816)       | `IF...ELSE...THEN`                         | solido       |
|16 | `ABS-VAL` (006)                  | `DIFFERENCE` (821) | valore assoluto (`ABS`)                    | approssimato |
|17 | `.CLASSIFY` (006)                | `EGGSIZE` (817)    | `IF` annidati a cascata                    | solido       |
|18 | `COUNT-DOWN` (006)               | `FALLING` (829)    | loop discendente (`-1 +LOOP`)              | solido       |
|19 | `COUNT-UP` (006)                 | `DECADE` (826)     | `DO I . LOOP`                              | solido       |
|20 | `SAFE-DIVIDE` (006)              | `/CHECK` (817)     | guardia `0=` prima di `/`                  | solido       |
|21 | `DEMO-TYPE` (007)                | `BLOCK..TYPE`(879) | `TYPE` di un buffer                        | approssimato |
|22 | `.RANGE` (007)                   | `DECADE` (826)     | `DO I . LOOP`                              | solido       |
|23 | `.FROM-TO` (007)                 | `SAMPLE` (826)     | `DO` con estremi arbitrari                 | solido       |
|24 | `.STEP2` (007)                   | `PENTAJUMPS` (829) | `+LOOP` a passo > 1                        | solido       |
|25 | `.DOWN` (007)                    | `FALLING` (829)    | `+LOOP` a passo negativo                   | solido       |
|26 | `.SAFE-RANGE` (007)              | `**` (837)         | `?DO` (zero-trip safe)                      | approssimato |
|27 | `X`/`BUF` (008)                  | `DATE` (850)       | `VARIABLE` con `@`/`!`                      | solido       |
|28 | `COUNTER` (008)                  | `DATE` (854)       | `2VARIABLE`                                | solido       |
|29 | `MYBUF` (008)                    | `LIMITS` (856)     | `VARIABLE` + `ALLOT` (buffer)              | solido       |
|30 | `PRIMES` (008)                   | `#PENCILS` (865)   | `CREATE , , ,` (tabella di celle)          | solido       |
|31 | `VOWELS` (008)                   | `SIZES` (860)      | `CREATE C,` (tabella di byte)              | solido       |
|32 | `CELL-ARRAY@` (008)              | `PENCILS` (865)    | accesso cella `2* + @`                     | solido       |
|33 | `CELL-ARRAY!` (008)              | `LIMIT` (856)      | scrittura cella `2* + !`                   | solido       |
|34 | `BYTE-ARRAY@` (008)              | `BOARD@` (867)     | byte `+ C@`                                | solido       |
|35 | `BYTE-ARRAY!` (008)              | `BOARD!` (867)     | byte `+ C!`                                | solido       |
|36 | `.COUNTED` (009)                 | `"LABEL"` (878)    | stringa contata + `TYPE`                   | approssimato |
|37 | `MY-CONSTANT` (010)              | `LIMIT` (853)      | costante (CREATE/DOES> vs CONSTANT)        | approssimato |
|38 | `CELL-ARRAY` (010)               | `PENCILS` (865)    | array indicizzato                          | approssimato |
|39 | `BYTE-ARRAY` (010)               | `SIZES` (860)      | array di byte                              | approssimato |
|40 | `CLAMP` (012)                    | `LABEL` (878)      | `0 MAX 5 MIN` (saturazione)                | solido       |
|41 | `.COLOR-NAME`/`DESCRIBE` (013)   | `LABEL` (858)      | selezione (CASE vs IF annidati)            | solido       |
|42 | `_color` (013)                   | `DO-SOMETHING`(876)| esecuzione vettorizzata su indice          | solido       |
|43 | `.SIGNED` (014)                  | `.DEG` (846)       | `<# ... SIGN #>` con segno                 | solido       |
|44 | `.RIGHT` (014)                   | `REPORT` (859)     | incolonnare con `.R`/`U.R`                 | approssimato |
|45 | `.CENTS` (014)                   | `M.` (864)         | punto decimale con `HOLD`                  | solido       |
|46 | `TOTAL` (015)                    | `DATE` (854)       | `2VARIABLE`                                | solido       |
|47 | `RESET-TOTAL` (015)              | `DATE 2!` (854)    | store di un doppio                         | solido       |
|48 | `ADD-TO-TOTAL` (015)             | `R%` (842)         | accumulo con `M+`                          | approssimato |
|49 | `.TOTAL` (015)                   | `APPLES` (855)     | `2@ D.` (stampa doppio)                     | solido       |
|50 | `DISPLAY-ITEM`/`ALOHA` (017)     | `'ALOHA`/`ALOHA`(869)| slot eseguibile in variabile             | solido       |
|51 | `USE-NUMBERS` (017)              | `COMING` (870)     | `['] ... !` per assegnare il vettore       | solido       |
|52 | `SHOW-AS-NUMBER` (017)           | `HELLO` (869)      | handler intercambiabile                    | solido       |
|53 | `.CIRCLE`/`.SQUARE` (018)        | `DEFINITIONS` (872)| vocabolari / contesto di ricerca           | approssimato |
|54 | `.WORD-INFO` (022)               | `SEE TEST` (877)   | ispezione di una definizione               | solido       |
|55 | `WRONG` (022)                    | `/CHECK3` (819)    | errore + diagnostica (`WHERE`)             | approssimato |
|56 | `MY-POINT` (023)                 | `LIMITS` (856)     | record via `CREATE ALLOT`                  | solido       |
|57 | `INIT-POINT` (023)               | `!DATE` (851)      | store di piu' campi                        | solido       |
|58 | `.POINT` (023)                   | `.DATE` (851)      | stampa di piu' campi                       | solido       |

> Nota: le definizioni dei tutorial 011 (bit-ops), 016 (input), 019/020
> (compilation), 021 (evaluate), 024-027 e dell'intera traccia hardware 030-053
> non compaiono in tabella: non hanno controparte negli Screen (vedi le due
> sezioni precedenti).
