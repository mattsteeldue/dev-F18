# Piano: mirror a `xt-2` che punta alla nfa invece che a lfa+2

> Stato: **APERTO** (2026-09-27) -- solo analisi, nessuna modifica al core.
> Decisione dell'autore ancora da prendere tra l'opzione A (modello
> invariato, `LFA` senza TRAVERSE) e l'opzione B (mirror -> nfa).

Segue `planners/PLAN-NFA-AMBIGUITY.md` (build 2026-09-26, `?HEAP_PTR`
rimossa). Nasce dalla domanda: se il mirror puntasse alla nfa, si
risparmierebbero chiamate a `TRAVERSE`?

## 1. I due modelli

Oggi (build 2026-09-26):

    Dizionario                          Heap
      xt-2  --> ha di lfa+2   ------->    nfa    byte-lunghezza, nome
      xt    --> codice / CALL             lfa    ha della nfa precedente
     (xt+3) --> corpo (>BODY)             lfa+2  xt in memoria principale

Ipotesi: `xt-2` contiene la **ha della nfa**; heap invariato (la cella xt a
lfa+2 resta, serve a `(FIND)` per restituire l'xt).

In pratica si sceglie quale estremo dell'header e' gratuito partendo da un
xt:

| Da un xt si ottiene... | Oggi | Ipotesi |
|---|---|---|
| cella xt / lfa | `CELL- @ FAR` (+ `CELL-`) | nfa + `1 TRAVERSE 1+` |
| nfa | lfa+2 - 3 + `-1 TRAVERSE` | `CELL- @ FAR` |

Le due scansioni costano uguale: n giri per un nome di n caratteri, 7 parole
threaded a giro (`OVER + LIT 127 OVER C@ < 0BRANCH`).

## 2. Conteggio TRAVERSE per uso

B = all'indietro, F = in avanti. Colonna "A" = modello attuale con `LFA`
riscritta senza TRAVERSE (sez. 3).

| Parola / uso | Oggi | A | B (ipotesi) |
|---|---|---|---|
| `<NAME` / `NFA` | 1B | 1B | 0 |
| `LFA` (pfa->) | 1B+1F | 0 | 1F |
| `PFA` (nfa->) | 1F | 1F | 1F |
| `ID.` | 1F | 1F | 1F |
| `WORDS`, per parola | 2F | 2F | 2F |
| `FORGET` (`NFA` + `LFA`) | 3 | 1 | 1 |
| `MARKER` compilazione (`LATEST PFA LFA`) | 3 | 1 | 2 |
| `MARKER` runtime, `(;CODE)`, `_DOES>_` | 1F | 1F | 1F |
| `CODE`, avviso ridefinizione (`<NAME ID.`) | 2 | 2 | 1 |
| `(FIND)` | 0 | 0 | 0 |
| lib `HIDE-WORD`, per giro (`PFA LFA`) | 3 | 1 | 2 |
| lib `SEE` (`DEB-NFA` + `DEB-LFA`) | 3 | 1 | 1 |
| lib `LOCALS` (`LATEST PFA LFA`) | 3 | 1 | 2 |
| lib `SET-FENCE` (`LFA`) | 2 | 0 | 1 |
| inc `.WORD`, `.VOCAB`, `RENAME` (`NFA`) | 1B | 1B | 0 |

Esito:

- rispetto a oggi, B vince o pareggia ovunque;
- rispetto ad A, **pareggio**: B vince sui percorsi xt->nome, perde sui
  percorsi xt->link;
- `WORDS` e `(FIND)`, gli unici cicli frequenti, non cambiano in nessun
  caso (partono gia' dalla nfa). Il risparmio in velocita' cade tutto su
  parole usate una volta sola: e' marginale.

`LATEST PFA LFA` (MARKER, LOCALS) e' comunque ridondante in entrambi i
modelli: `LATEST 1 TRAVERSE 1+` basta (1F).

## 3. Opzione A -- modello invariato, `LFA` diretta

    : lfa ( pfa -- lfa )
        cfa cell- @ far cell-
        ;

lfa = (cella xt) - 2. Oggi `LFA` fa `NFA` (1B) e poi `1 TRAVERSE` (1F) per
tornare quasi al punto di partenza. Costo: +1 cella (+2 byte) nel core.

Da toccare: `LFA` in L1.asm di DOES e DOT, `src/F18e.f`; eventualmente
`MARKER` e `lib/LOCALS.f` (`LATEST 1 TRAVERSE 1+`). Nessun cambio di
struttura, nessun cambio a manuale/help/strumenti oltre al codice.

## 4. Opzione B -- mirror -> nfa

### 4.1 Vantaggio principale: contratto uniforme

Dopo `PLAN-NFA-AMBIGUITY.md` il contratto e': celle memorizzate = `ha`, nfa
sullo stack = risolta. Ma il mirror e' l'unica `ha` memorizzata che **non**
punta a una nfa. Con B tutte le `ha` memorizzate (contenuto LFA, voc-cell,
`CURRENT @ @`, celle MARKER, mirror) puntano a una nfa, e
`xt CELL- @ FAR ID.` si legge come `LFA @ FAR ID.`.

### 4.2 Modifiche

- `system.asm` (DOES e DOT, byte-identici), macro `New_Def`:
  `dw mirror_Ptr - $E000 + Heap_offset` -> `dw temp_NFA - $E000 +
  Heap_offset` (e `mirror_Ptr` diventa superfluo).
- `<NAME` (L1.asm x2, F18e.f): `CELL- @ FAR` -- circa -8 byte.
- `LFA`: resta `NFA 1 TRAVERSE 1+` (ora costa 1F invece di 1B+1F).
- `CODE` (L1.asm x2, F18e.f): `HP@ CELL- ,` -> `CURRENT @ @ ,` (a quel
  punto CURRENT punta gia' alla nuova voce) -- +2 byte.
- `inc/_noname.f`: `OVER 4 + ,` -> `OVER ,`.
- Cercare ogni altro lettore del mirror (`CELL- @ FAR`, `2- @ FAR`) in
  `inc/`, `lib/`, `demo/`, `tutorial/` (censimento 2026-09-27: solo
  `<NAME` nel core e `:NONAME` come scrittore).
- Strumenti: `util/gen-dict-structure.py` (etichetta "backward-heap-pointer
  to CFA"), `util/cmp-f18e.py` (usa il mirror per lo scarto heap: verificare
  che la progressione resti leggibile), `emu/test_nfa_contract.py`.
- Documentazione: help `cfa`, `lfa`, `nfa`, `{name`, `}body` (appena
  rivisti), commento "Dictionary memory structure" in F18e.f (due copie,
  prima di `(FIND)` e prima di `CODE`), `tutorial/022-introspection.f`,
  par. 4.6 del manuale (via `/regen-doc-dict-structure` + testo in
  `products/`, incollato a mano dall'autore).
- Nuovo build: `/bump-build`, poi `/check-f18e` e CORE-TESTS su CSpect.

Saldo byte stimato: circa -6 nel core. Paging MMU7 invariato (sempre un
solo `FAR`).

### 4.3 Rischi

- Codice utente o librerie esterne che leggono il mirror come "cella xt"
  si rompono in silenzio (valore plausibile ma sbagliato).
- Il binario cambia ovunque (ogni mirror): nessun confronto byte-per-byte
  con la build precedente, solo `/check-f18e` sulla nuova.
- Si somma a una build (2026-09-26) appena fatta e non ancora pubblicata:
  valutare se accorparli in un'unica release.

### 4.4 Versione: B porta alla 1.9

Per l'autore l'opzione B e' un **cambio di paradigma** della struttura del
dizionario, non un semplice nuovo build: cambia il significato di una cella
presente in ogni definizione e letta dal codice utente. Merita quindi il
passaggio a **vForth 1.9**, non solo un nuovo build number della 1.8.

Conseguenze da pianificare prima di applicarla:

- numero di versione in tutti i punti dove oggi compare "1.8" (SPLASH di
  DOES e DOT, header di `src/F18e.f`, CLAUDE.md, loader BASIC, BLOCK 1 di
  `!Blocks-64.bin`, nome del manuale `doc/vForth1.8-core-en-*.odt`, nomi
  delle directory `project/vForth18_*` e del binario `forth18e.bin`):
  censire e decidere cosa rinominare, `/bump-build` oggi gestisce solo la
  data;
- voce nella sezione "Breaking Changes" di CLAUDE.md e nel manuale
  (`xt-2 @ FAR` restituisce la nfa, non piu' la cella xt);
- nota di migrazione per chi legge il mirror direttamente;
- l'opzione A, invece, resta compatibile e puo' uscire come build della 1.8.

## 5. A margine (vale per entrambi)

`ID.` usa `1 TRAVERSE` solo per trovare la fine del nome; `DUP C@ $1F AND`
darebbe lo stesso risultato senza scansione, ma solo se `WIDTH` resta 31:
`CODE` memorizza `MIN(len, WIDTH)` caratteri e lascia la lunghezza piena nel
byte di conteggio. Toglierebbe 1F da `ID.` e quindi da ogni giro di `WORDS`
-- l'unico risparmio che tocca un ciclo frequente. Da decidere a parte.

## 6. Raccomandazione

- Obiettivo "meno TRAVERSE": opzione A, 2 byte, nessun cambio di struttura.
- Obiettivo "chiudere l'ambiguita' del contratto `ha`": opzione B; costo in
  velocita' equivalente ad A, ma riallineamento di manuale, help e
  strumenti, e passaggio alla versione 1.9 (sez. 4.4).
