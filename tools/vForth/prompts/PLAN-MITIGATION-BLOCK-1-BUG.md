# Piano: mitigazione strutturale del bug "block-buffer starvation"

> Stato: **PROPOSTO** (2026-09-12). Nessuna riga ancora modificata.
> Proposta dell'autore: **portare il pool a 7 buffer e specializzare il
> BLOCK 1**, rendendolo non riciclabile dalle richieste relative ad altri
> blocchi.
> Bug di riferimento: `CLAUDE.md` -> "Block-buffer starvation"; `doc/reverse.md`
> par. 2.4 e 13.3 punto 2; commento in testa a `test/CHOMP-MAZE-TESTS.f`
> (righe 20-45).


## 1. Il problema in una frase

`F_INCLUDE` tiene la riga di sorgente in corso di interpretazione nel buffer
del BLOCK 1, che vive nello stesso pool round-robin di sei buffer da cui
attinge il codice interpretato: se durante una riga si leggono sei blocchi
distinti, il buffer viene riciclato, `WORD` rilegge il BLOCK 1 da disco e
ottiene i metadati del block file invece della riga. Il sintomo e' **una
parola a caso "is undefined", diversa a ogni run**, e il file accusato e'
quasi sempre innocente.


## 2. Perche' il BLOCK 1 e' davvero un caso speciale

Non e' una scorciatoia: e' un'asimmetria strutturale.

Per **qualunque blocco diverso dall'1**, lo sfratto e' innocuo: `BLOCK` lo
rilegge da disco e riottiene gli stessi byte. Il costo e' una lettura.

Il **BLOCK 1 e' l'unico blocco il cui contenuto in RAM non e' riproducibile da
disco**: `F_INCLUDE` (e `EVALUATE`, e altri cinque moduli, vedi par. 3.2) ci
scrivono dentro senza mai chiamare `UPDATE`, quindi su disco restano i
metadati. Sfrattarlo non e' un costo: e' una distruzione di dati.

Il core **contiene gia' due precedenti** di questo caso speciale, quindi la
modifica e' coerente con il design esistente e non introduce un concetto nuovo:

- `0x00` / `NUL_WORD` -- `L1.asm:1661`: `blk @ 1 >` decide se avanzare al blocco
  successivo dello Screen; con BLK=1 (include) termina la riga invece di
  avanzare.
- `\` / `BACKSLASH` -- `L3.asm:993-995`: `blk @ 1-` con il commento esplicito
  *"BLOCK 1 is used as temp-line in INCLUDE file"*; per BLK=1 salta a
  `>IN = B/BUF-2` invece di ragionare per righe da 64 caratteri.

Questa patch aggiunge il terzo, nel punto dove serviva fin dall'inizio.


## 3. Audit: tutti i punti che toccano BLK o il BLOCK 1

### 3.1 Nel core (`project/vForth18_DOES/source/`)

| Punto | Word | Cosa fa | Impatto della patch |
|---|---|---|---|
| `L3.asm:250` | `F_INCLUDE` | `1 BLOCK B/BUF` -- prende il buffer di riga | **La vittima**: oggi qui puo' scattare una rilettura inutile dal disco |
| `L3.asm:259` | `F_INCLUDE` | `1 BLK !` -- segnala modalita' include | invariato |
| `L3.asm:225,286` | `F_INCLUDE` | salva/ripristina `BLK` per l'annidamento | invariato |
| `L1.asm:1200-1204` | `WORD` | `blk @ IF blk @ BLOCK` -- **riacquisisce l'indirizzo a ogni token** | **Dove il bug si manifesta**: e' questo `BLOCK` che rilegge i metadati |
| `L1.asm:1661-1668` | `0x00` (`NUL_WORD`) | `blk @ 1 >` -- gia' specializza BLK=1 | **precedente**, invariato |
| `L3.asm:993-1013` | `\` | `blk @ 1-` -- gia' specializza BLK=1, con commento | **precedente**, invariato |
| `L1.asm:728` | `?LOADING` | `blk @ 0=` -> msg #22 | invariato (nota: passa anche con BLK=1) |
| `L1.asm:1528` | `ERROR` | lascia `>IN BLK` sullo stack per `WHERE` | invariato |
| `L3.asm:450-458` | `LOAD` | salva/ripristina BLK, `b/scr * blk !` | invariato |
| `L3.asm:468-472` | `-->` | `b/scr blk @ over mod - blk +!` | invariato -- ma vedi par. 8 |
| `L3.asm:80-102` | `BUFFER` | **unico punto che sfratta** un buffer | **il punto della patch** |
| `L3.asm:114-150` | `BLOCK` | `+BUF` solo per *cercare*; sfratta chiamando `BUFFER` | invariato (eredita la protezione) |
| `L3.asm:67-78` | `EMPTY-BUFFERS` | `first @ limit @ over - erase` -- grezzo, non passa da `BUFFER` | **non protetto**, vedi par. 7 |
| `L3.asm:152` | `#BUFF` | `Constant_Def NBUFF, "#BUFF", BUFFERS` | **parametrico**, si aggiorna da solo |
| `L3.asm:157-166` | `FLUSH` | `#buff 1+ 0 DO 0 BUFFER DROP LOOP` | **migliorato**, vedi par. 6 |
| `L3.asm:10-30` | `R/W` | `n 1-`, range-check `0..#sec-1` | invariato; conferma che il BLOCK 1 e' l'offset 0 del file |
| `next-opt1.asm:133-140` | `BLK-SEEK` | `b/buf m*` dopo l'`1-` di `R/W` | invariato |

### 3.2 Fuori dal core -- altri sette usi del BLOCK 1 come buffer di lavoro

Tutti guadagnano dalla patch, nessuno ne perde. **Nessuno di questi chiama
`UPDATE` sul BLOCK 1**, quindi il pin non puo' mai causare una scrittura persa.

| File | Uso | Nota |
|---|---|---|
| `inc/evaluate.f:56-64` | copia la stringa nel BLOCK 1, `1 BLK !`, `INTERPRET` | **stessa identica vulnerabilita' di `F_INCLUDE`**; `SOURCE-ID` = -1 |
| `inc/evaluate.f:84-90` | al rientro rilegge l'intera riga con `F_GETLINE` | workaround manuale dello stesso problema |
| `inc/source.f:29-30` | `1 BLOCK C/L 2*` -- commento: *"the input buffer is exploited via 1 BLOCK"* | invariato |
| `inc/VIEW-FILE-PAD.f:30-32` | commento: *"buffer address is stable: nothing in the loop calls BLOCK"* | **il pin rimuove proprio questo vincolo** |
| `inc/screen-from-file.f:8-11` | BLOCK 1 come riga, poi `LINE` + `UPDATE` | l'`UPDATE` marca `PREV` = buffer dello Screen destinazione, non il BLOCK 1: corretto |
| `lib/LED.f:146` | *"use block 1 as special buffer"* | invariato |
| `lib/RPi0.f:327-328,387` | tiene l'indirizzo in `UART-FORTH-BUF` | oggi l'indirizzo puo' essere invalidato dal riciclo: **la patch lo rende stabile** |

**Conseguenza sul gating:** `EVALUATE` mette `SOURCE-ID` a **-1**, `F_INCLUDE` a
un filehandle **positivo**. Un pin condizionato a `SOURCE-ID @ 0>` mancherebbe
`EVALUATE`. **Il pin deve essere incondizionato** -- cioe' esattamente la
proposta dell'autore, non la variante gated.

### 3.3 Fuori dal core -- chi tocca il BLOCK 1 sul file, non via `BLOCK`

Nessuno di questi passa dal pool di buffer, quindi sono **fuori scopo** ma
vanno ricordati perche' definiscono il contenuto "vero" del blocco:

- skill `/bump-build`: scrive la data di build nel primo blocco da 512 byte di
  `!Blocks-64.bin` (= BLOCK 1, offset 0).
- `util/blocks2txt.pl:39`, `util/blank-blocks.ps1:12`: offset `(n-1)*512`.

**Nessun word del core legge mai il contenuto reale del BLOCK 1.** Questo
conferma che pinnarlo non toglie nulla a nessuno.


## 4. Le due modifiche

Sono ortogonali: la (A) da' il buffer in piu', la (B) risolve il bug. La (B)
funziona anche da sola; la (A) da sola non risolve niente (sposta solo la
soglia da 6 a 7 blocchi).

### (A) `BUFFERS` 6 -> 7

Una riga per variante, tutto il resto e' derivato:

- `project/vForth18_DOES/source/system.asm:231`
- `project/vForth18_DOT/source/system.asm:225`

```
BUFFERS         equ     7      // era 6
```

`FIRST_system`, `USER_system`, `R0_system`, `TIB_system`, `S0_system` sono
calcolati da `BUFFERS` e scendono tutti di 516 byte. `#BUFF` nel core e'
`Constant_Def NBUFF, "#BUFF", BUFFERS`: si aggiorna da solo. In `F18e.f` e'
`LIMIT @ FIRST @ - 516 / constant #buff`: si aggiorna da solo.

**Precedente storico:** il blocco commentato in `system.asm:242-246` contiene
`FIRST_system: equ $D1E4`, che e' esattamente `$E000 - 516*7`. **Il layout a 7
buffer e' quello che il sistema usava in passato**, non una configurazione
inesplorata. Coerentemente, il commento in `src/F18e.f:6891-6892` dice ancora
*"There are 7 buffers (516 * 7 = 3612 bytes)"* pur riportando `FIRST = D3E8`
(che e' il valore a 6): e' un commento rimasto indietro, da correggere
(par. 5).

**Effetto sulla mappa di memoria:**

| | oggi (6) | dopo (7) |
|---|---|---|
| `LIMIT` | `$E000` | `$E000` |
| `FIRST` | `$D3E8` | `$D1E4` |
| `USER` = `R0` | `$D398` | `$D194` |
| `TIB` = `S0` | `$D2F8` | `$D0F4` |
| `HERE` al boot | `$81B0` | `$81B0` |
| spazio libero dizionario | 20808 byte | 20292 byte |

**Costo: 516 byte su ~20.8 KB liberi, il 2.5%.** Il pool utile per il codice
utente resta 6 come oggi (7 meno quello pinnato): **nessuna regressione di
capacita', in cambio della riga di sorgente protetta.**

### (B) Pin del BLOCK 1 in `BUFFER`

`BUFFER` (`L3.asm:80`) e' l'unico punto che sfratta: `BLOCK` lo attraversa,
quindi la protezione si eredita. La rotazione diventa "avanza finche' il
candidato non e' il BLOCK 1":

```asm
                Colon_Def BUFFER, "BUFFER", is_normal
Buffer_Retry:                                   // begin
                dw      USED, FETCH             //      used @
                dw      DUP, TO_R               //      dup >r
Buffer_Begin:                                   //      begin
                dw          PBUF                //          +buf
                dw      ZBRANCH                 //      until
                dw      Buffer_Begin - $
                dw      USED, STORE             //      used !
                // BLOCK 1 e' il buffer di riga di INCLUDE/EVALUATE:
                // il suo contenuto non e' rileggibile da disco. Mai riciclarlo.
                dw      R_OP, FETCH             //      r @
                dw      LIT, $7FFF, AND_OP      //      7FFF and
                dw      ONE_SUBTRACT, ZEQUAL    //      1- 0=     ( e' il blocco 1? )
                dw      DUP                     //      dup
                dw      ZBRANCH                 //      if
                dw      Buffer_Keep - $
                dw          R_TO, DROP          //          r> drop  ( scarta )
Buffer_Keep:                                    //      endif
                dw      ZEQUAL                  //      0=
                dw      ZBRANCH                 // until
                dw      Buffer_Retry - $
                dw      R_OP, FETCH, ZLESS      // r @ 0<    <-- da qui invariato
                // ... resto della definizione immutato
```

Forma Forth equivalente per `src/F18e.f:5443`:

```forth
: buffer  ( n -- a )
    Begin
        used @ dup >r
        Begin +buf Until
        used !
        r@ @ [ hex 7FFF ] Literal and  1- 0=
        dup If  r> drop  Then          \ scarta il candidato e riprova
        0=
    Until
    r@ @ 0<
    If  r@ cell+  r@ @ [ hex 7FFF ] Literal and  0 r/w  Then
    r@ !  r@ prev !  r>  cell+ ;
```

**Nessun rischio di stallo.** Quando e' `1 BLOCK` stesso a chiedere un buffer,
nessun buffer dichiara 1 (e' proprio per questo che siamo li'), quindi lo skip
non scatta. E non possono esistere due buffer che dichiarano 1, perche' `BLOCK`
verifica la residenza prima di chiamare `BUFFER`. Con 7 buffer, al massimo uno
e' pinnato: ne restano sempre almeno 6.


## 5. Punti da riallineare dopo la modifica

| File | Cosa |
|---|---|
| `src/F18e.f:5443` | `: buffer` -- stessa logica (allineamento a mano, come da convenzione) |
| `src/F18e.f:6891-6892` | commento mappa: `FIRST = D1E4`, "7 buffers" diventa finalmente vero |
| `emu/emulator.py:219` | `self.cpu.SP = 0xD2F8` -- oggi coincide con `S0`; con 7 buffer cadrebbe **dentro** il pool. Portare a `0xD0F4` (nuovo `S0`). E' transiente (`ColdRoutine` ricarica da `S0_origin`) ma e' sbagliato lasciarlo li' |
| `CLAUDE.md:124` | "6 buffers of 512 bytes each" -> 7 |
| `CLAUDE.md:545-562` | la sezione "Block-buffer starvation": da bug aperto a bug risolto, con il budget non piu' applicabile |
| `doc/reverse.md` par. 2.4 e 13.3 | idem |
| `doc/ONBOARDING.md:1254` | "competes for the same 6 buffers" |
| `test/CHOMP-MAZE-TESTS.f:20-45` | il commento diventa archeologia; vedi par. 9.1 per il test |
| `help/#buff.txt` | non cita il numero: **nessuna modifica** |

**Non toccare mai automaticamente** `doc/vForth1.8-core-en-*.odt` / `.pdf`. Se
il manuale cita la mappa di memoria o il numero di buffer, va segnalato
all'autore perche' la aggiorni a mano.

`project/vForth18_DOES/source/L0.asm:56` -- `RP_Pointer: dw $d188 // R0_system`
e' un **inizializzatore morto**: la cella e' solo lo slot di salvataggio usato
dalle macro `ldhlrp`/`ldrphl`, scritta prima di essere letta, e `$d188` e' un
residuo dell'era a 7 buffer (oggi `R0_system` = `$D398`). Non e' una dipendenza
dal layout. Va bene lasciarlo, ma il commento fuorviante andrebbe corretto.


## 6. Effetti collaterali positivi (gratis, senza codice in piu')

1. **`FLUSH` dentro un `INCLUDE` diventa sicuro.** Oggi `FLUSH` fa
   `#buff 1+ 0 DO 0 BUFFER DROP LOOP` e azzera anche l'header del buffer che
   tiene la riga corrente -> il successivo `1 BLOCK` rilegge i metadati -> stesso
   crash. E' una seconda istanza latente dello stesso bug, chiusa dalla stessa
   patch. Interessa `lib/PERSISTENCE.f` (3 punti), `inc/save.f`, `inc/bmove.f`.
2. **`EVALUATE` non ha piu' bisogno del suo workaround.** La rilettura della
   riga in `inc/evaluate.f:84-90` resta corretta ma diventa ridondante. Non
   rimuoverla in questa patch: prima si verifica, poi eventualmente si
   semplifica.
3. **`lib/RPi0.f` ottiene un indirizzo di buffer stabile** invece di uno che
   puo' essere invalidato sotto i piedi.
4. **`inc/VIEW-FILE-PAD.f` perde il suo vincolo** (*"nothing in the loop calls
   BLOCK"*).


## 7. Cosa resta fuori (non-obiettivi, da documentare)

1. **`EMPTY-BUFFERS` resta distruttivo** dentro un include: e' un
   `FIRST LIMIT OVER - ERASE` grezzo (`L3.asm:67`), non passa da `BUFFER`, e
   cancella anche il contenuto. Non toccarlo in questa patch: e' invocato da
   `COLD` prima di qualunque include, e chi lo chiama a mano sa cosa fa.
   Documentarlo come limite noto.
2. **L'annidamento di `INCLUDE` non e' risolto**: tutti i livelli condividono il
   BLOCK 1, quindi un include dentro un include sovrascrive comunque la riga
   esterna (motivo per cui `F_INCLUDE` fa il seek di riposizionamento e
   `EVALUATE` rilegge la riga). Serve un buffer di riga per livello: problema
   ortogonale, piano separato.
3. **Il BLOCK 1 diventa di fatto non persistibile**: se qualcuno lo marcasse
   `UPDATE`, non verrebbe mai riscritto (ne' dalla rotazione, ne' da `FLUSH`).
   Dato cosa contiene, e' un effetto desiderabile -- ma va scritto.
4. **Nessuna regressione sulla lettura dei metadati**: gia' oggi, dopo un
   `INCLUDE`, `1 BLOCK` restituisce l'ultima riga di sorgente invece dei
   metadati finche' il buffer non viene riciclato. Il pin rende permanente un
   comportamento che esiste gia'.


## 8. Anomalia trovata durante l'audit (fuori scopo, da tracciare)

`?LOADING` (`L1.asm:728`) passa con BLK=1, quindi `-->` **e' accettato dentro
un file incluso**: con BLK=1 calcola `b/scr - (blk mod b/scr)` = `2 - 1` = 1 e
fa `1 blk +!`, portando BLK a 2. Da quel momento `WORD` legge il BLOCK 2 come
sorgente. Non c'entra con questa patch e non e' la causa del bug in oggetto,
ma e' un modo silenzioso di far deragliare un include. Va verificato sul
target e, se confermato, o vietato (`blk @ 1 =` -> errore) o documentato.


## 9. Verifica

### 9.1 Test di accettazione primario

`test/CHOMP-MAZE-TESTS.f` e' gia' scritto attorno al bug: il corpo di
`DISK-MAZE-TESTS` (righe 189-195) tocca **9 blocchi distinti** (3 labirinti x 3
blocchi: 1480-1482, 1484-1486, 1488-1490) ed e' chiuso in una definizione
compilata **proprio per non essere eseguito durante l'`INCLUDE`**.

**Il test e': srotolare quelle righe al livello di file e verificare che
l'`INCLUDE` arrivi in fondo.**

- **Prima della patch**: fallisce con una parola non definita diversa a ogni run.
- **Dopo la patch**: deve passare tutto inline.

Nota: il file oggi tocca in tutto 4 buffer su 6 (BLOCK 1 + i 3 blocchi del
labirinto #1, letti una sola volta a riga 93-94 e riusati a 104 e 119). Il
margine apparente di 2 buffer e' ingannevole: un solo labirinto in piu' ne
chiede 3, quindi 1+3+3 = 7 > 6. Con la patch il vincolo sparisce del tutto.

### 9.2 Regressioni da controllare

- `printf '.quit\n' | python emu/repl.py` -- banner corretto, prompt `ok`.
- `emu/test_*.py` -- l'intera suite Python, in particolare
  `emu/test_words_stream.py` (tocca MMU7 e `rst $10`).
- Suite Forth sul target/emulatore: `INCLUDE TEST/CORE-TESTS.f` e le altre.
- **`EVALUATE`**: `inc/evaluate.f` annidato dentro un `INCLUDE` -- e' il secondo
  utente del BLOCK 1 e il piu' delicato.
- **`FLUSH` dentro un include**: prima della patch deve rompersi, dopo no.
- **`lib/PERSISTENCE.f`**, che usa `UPDATE FLUSH` in tre punti.
- **Stack e TIB**: `S0`/`TIB` scendono di 516 byte. Verificare `?STACK`
  (`L1.asm:1693`) e che nessuna demo con stack profondo regredisca.
- **`SPLASH`**: stampa "free space" = `S0 - HERE`; deve riportare 516 byte in
  meno. E' anche la verifica piu' rapida che la (A) abbia avuto effetto.

### 9.3 Sequenza operativa

1. Applicare (B) da sola su DOES, `/build DOES`, far girare 9.1 e 9.2.
   La (B) e' la patch che risolve: va validata in isolamento.
2. Applicare (A) su DOES, ricostruire, ripetere 9.2 con attenzione a stack,
   TIB e `SPLASH`.
3. Riportare entrambe su DOT (`system.asm:225` + `L3.asm` gemello), `/build DOT`.
4. Allineare a mano `src/F18e.f` (`: buffer` + commento mappa) -- non e'
   ricompilato dal workflow, ma e' la forma leggibile di riferimento.
5. Aggiornare `emu/emulator.py:219`.
6. `/bump-build` con la data del giorno: il binario del core cambia, quindi
   serve un nuovo build number in tutti i punti canonici.
7. `/regen-doc-dict-structure`: gli indirizzi hex del manuale cambiano
   (dizionario e mappa). L'autore incolla a mano nell'.odt e riesporta il .pdf.
8. Aggiornare la documentazione elencata al par. 5.
9. `/sync-cspect` e prova su CSpect; se possibile, prova su hardware reale --
   il layout di memoria e' la parte che l'emulatore modella meno fedelmente.


## 10. Riepilogo del delta

| | righe | rischio |
|---|---|---|
| `BUFFERS` 6 -> 7 (DOES + DOT) | 2 | basso: tutto e' derivato; costa 516 byte di dizionario |
| Pin del BLOCK 1 in `BUFFER` (DOES + DOT) | ~12 asm x2 | basso: un solo word, nessuno stallo possibile |
| Allineamento `F18e.f` | ~10 | nullo (non compilato) |
| `emu/emulator.py` | 1 | nullo |
| Documentazione | ~6 file | nullo |

In cambio: **il bug piu' insidioso del sistema diventa strutturalmente
impossibile**, il pool utile resta 6 come oggi, e tre limiti documentati
(il budget di 4-5 blocchi per file incluso, `FLUSH` dentro un include,
l'indirizzo instabile in `RPi0`/`VIEW-FILE-PAD`) cadono insieme.
