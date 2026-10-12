# Piano: FLOATING e i 5 byte del calcolatore ROM

> Stato: **IN CORSO** (2026-10-12) -- opzione A applicata a
> `lib/FP-INTERFACE.f` (`W>` arrotonda, `>W` con B = 0), **non ancora
> provata su CSpect**: codifica dei byte verificata con SjASMPlus, niente
> di piu'. Resta: provarla (`INCLUDE TEST/FLOATING-TESTS.f`, i cui
> confronti bit a bit possono cambiare esito), poi Fase 0 e seguenti.
> Decise D1, D4, D5 (sez. 10). Restano D2 (3 celle o stack separato) e D3
> (letterali): gli elementi per scegliere sono in sez. 6 e 7, la prova
> pratica che li chiude e' la Fase 0 (sez. 8). Nessuna misura ancora
> fatta: l'emulatore headless non ha il calcolatore ROM (sez. 9).

`lib/floating.f` appoggia tutta l'aritmetica al calcolatore della ROM
Spectrum (`RST $28`), che lavora su numeri di 5 byte, ma tiene i numeri
sullo stack dati in 2 celle (4 byte). Ad ogni passaggio si perde un byte
di mantissa. Questo piano quantifica il difetto e mette a confronto le
soluzioni.

## 1. Il difetto, esattamente

Formato ROM (5 byte, registri di `STK-STORE $2AB6` / `STK-FETCH $2BF1`):

    A   esponente + 128   (0 = forma "intero piccolo")
    E   bit 7 segno, bit 6..0 mantissa (il bit alto, sempre 1, e' implicito)
    D   mantissa
    C   mantissa
    B   mantissa            <-- il byte che vForth butta

Formato vForth (2 celle, `>W` / `W>` in `lib/FP-INTERFACE.f`):

    cella TOS (HL)   bit 15 segno | bit 14..7 esponente | bit 6..0 mantissa
    cella sotto (DE) mantissa (D, C della ROM)

| | ROM | vForth 2 celle |
|---|---|---|
| Mantissa (con il bit implicito) | 32 bit | 24 bit |
| Cifre decimali significative | ~9.6 | ~7.2 |
| Massimo intero esatto | 4 294 967 296 | 16 777 216 |
| Esponente | 8 bit | 8 bit (invariato) |

Il formato a 2 celle ha la stessa capienza di un IEEE-754 single (1 + 8 +
23): non e' "rotto", e' una precisione singola. I problemi veri sono tre.

1. **La perdita e' per operazione, non per espressione.** Ogni parola
   (`F+`, `FSIN`, ...) fa `>W` degli operandi, una `FOP`, `W>` del
   risultato: il byte B si perde ad ogni passo e l'errore si accumula
   lungo una catena di calcoli. Solo `F*/` e `PI` tengono l'intermedio
   sul calculator stack.
2. **`W>` tronca, non arrotonda.** Errore fino a 1 ulp (a 24 bit) e
   sempre nella stessa direzione.
3. **`>W` rientra con B = `$A2`, non 0.** Il codice e' `$06 C, $A2 C,`
   mentre il commento dice `HEX 00 N,` e `src/FP-OPT.f` (riga 75) ha
   davvero `00`. **E' una compensazione voluta** (D1, confermato
   dall'autore): bilancia in media il troncamento di `W>` (162/256
   rimessi contro 127/256 persi in media). Il prezzo: un valore esatto a
   24 bit (0.5, 70000.) non rientra esatto nel calcolatore. Il commento
   in `lib/FP-INTERFACE.f` va corretto per dirlo.

Conseguenze pratiche: `D>F` non conserva un doppio a 32 bit sopra 2^24;
un listato BASIC portato in vForth non da' gli stessi risultati cifra per
cifra (rilevante per la guida `doc/basic-to-vforth/` in corso); i test
`test/FLOATING-TESTS.f` confrontano le celle bit a bit e passano solo
dove i due rami perdono allo stesso modo.

Difetto collaterale, indipendente dal formato: `(FRAC)` in `FNUMBER`
converte i decimali con una divisione per 10 e un prodotto **per ogni
cifra**, quindi anche il letterale accumula errori (ipotesi da misurare:
`0.5` potrebbe non essere esattamente 0.5). Si cura accumulando le cifre
come intero e scalando una volta sola per 10^n. Vale per tutte le opzioni.

## 2. Vincoli e proprieta' da non perdere per distrazione

- La cella e' 16 bit: 5 byte sono 2 celle e mezza.
- Oggi un float e' un doppio: `2DUP 2SWAP 2DROP 2@ 2! 2CONSTANT`
  (`FCONSTANT` e' `2CONSTANT`), `DLITERAL` per i letterali, `.S` li mostra.
- Il segno si legge "da intero" sul TOS (`F0<` e' `NIP 0<`).
- Un intero positivo 0..65535 scritto `n 0` e' gia' un float valido (forma
  intero piccolo della ROM): `1 0 >W`, `180 0 F*/`, `10 0 FLN`.
- `FLOATING` rattoppa la cella 32 di `INTERPRET` (`NUMBER` -> `FNUMBER`);
  `INTERPRET` poi fa `DPL @ 1+ IF DLITERAL ELSE DROP LITERAL THEN`, cioe'
  si aspetta comunque un doppio da `NUMBER`.
- `NMODE`, `PLACE`, `EXP` sono variabili utente del core e restano.
- Il calculator stack sta nella memoria BASIC (STKBOT..STKEND, sotto
  RAMTOP `$61FF`). La `TEST-ROOM` della ROM confronta con SP, ma SP e' lo
  stack dati Forth (~`$D0xx`): **nessuna protezione** se il calculator
  stack cresce oltre RAMTOP dentro la tabella IM2 e il core. Oggi non
  succede perche' la profondita' e' al massimo 2-3.

## 3. Le opzioni

### A. Restare a 2 celle, arrotondare (correttivo minimo)

`W>` arrotonda al piu' vicino usando il bit 7 di B; `>W` rientra con
B = 0. L'arrotondamento si fa dopo l'impacchettamento: se il bit 7 di B e'
1, incremento a 32 bit di HL:DE -- il riporto dalla mantissa entra da solo
nell'esponente, come in IEEE. Da saltare quando A = 0 (intero piccolo).
Circa 10 byte in `W>`, uno cambiato in `>W`.

- Pro: nessuna modifica di API, niente da riscrivere, errore massimo
  dimezzato (0.5 ulp) e senza deriva, valori esatti che restano esatti.
- Contro: restano 24 bit e la perdita per operazione. Non risolve: rende
  onesto il nome "precisione singola".
- Rischio: i risultati cambiano sull'ultimo bit; i test bit a bit e
  qualche output del tutorial 024 vanno ricontrollati.

### B. 3 celle sullo stack dati

Il float diventa una tripla (6 byte, uno sprecato). Servono `FDUP FSWAP
FOVER FROT FDROP` in CODE, `F@ F!`, `FVARIABLE`, `FCONSTANT` proprie.
Letterali senza toccare il core: in compilazione `FNUMBER` compila da se'
la cella piu' profonda con `LITERAL` e restituisce le altre due, che
`INTERPRET` compila con `DLITERAL`.

- Pro: un solo stack, `.S` continua a mostrare tutto, segno ancora
  leggibile sul TOS se il layout lo mette li'.
- Contro: ogni operazione fa ancora due `>W` e un `W>` (ora di 5 byte):
  veloce come oggi o poco meno, mai di piu'. Rompe comunque
  `2DUP`/`2CONSTANT`/`n 0`. Stack dati piu' affollato.

### C. Stack FP separato = il calculator stack della ROM

I float vivono sul calculator stack, a 5 byte, e non lo lasciano mai. E'
il modello di default di Forth-2012 (stack floating-point separato).

    F+ F- F* F/ FSIN ...   una sola FOP, nessun trasferimento
    FDUP FSWAP FDROP       opcode calcolatore $31 $01 $02
    FOVER FROT             CODE (copia di 5 byte su STKEND)
    F@ F! FVARIABLE        5 byte in memoria;  1 FLOATS = 5
    FCONSTANT FLITERAL     5 byte in linea + runtime (FLIT)
    F0< F0= F<             lasciano un flag sullo stack DATI
    S>F F>S D>F F>D        ponte con lo stack dati (STACK-BC, FP-TO-BC)
    FDEPTH F.S FCLEAR      diagnostica e pulizia

- Pro: precisione ROM piena, nessuna perdita ne' per operazione ne' in
  memoria; piu' veloce di oggi (spariscono 3 trasferimenti per
  operazione); `D>F` esatto su 32 bit; stessi risultati del BASIC.
- Contro: API incompatibile (niente `2DUP` sui float, niente `n 0`,
  segno non piu' leggibile sul TOS, `.S` non li vede). Da riscrivere:
  libreria, test, tutorial 024, help, paragrafo del manuale.
- Rischi specifici:
  - **Overflow del calculator stack verso `$6200`** (sez. 2): la libreria
    deve controllare da se' STKEND contro RAMTOP nelle parole che fanno
    crescere lo stack (letterali, `FDUP`, `FOVER`, `F@`, `S>F`), con un
    margine per i temporanei della ROM. Da misurare lo spazio reale in
    DOES e in DOT (STKBOT, STKEND, RAMTOP a prompt).
  - **Errori**: `ABORT`/`QUIT` non svuotano il calculator stack. Serve
    `FCLEAR` e una regola su chi lo chiama. Un errore ROM (ritorno al
    BASIC) invece lo svuota da solo.
  - **Letterali**: un float non deve lasciare nulla sullo stack dati, ma
    `INTERPRET` vuole un doppio da `NUMBER`. Quattro vie, sez. 7.

### D. Ibrido: 2 celle come formato di scambio, calcolo sul calculator stack

Lasciare `lib/floating.f` com'e' e documentare/estendere `>W FOP W>` come
"modo calcolatore" (piu' `W@`/`W!` a 5 byte): la perdita diventa per
espressione invece che per operazione. E' di fatto la C sotto altri nomi,
con due vocabolari da spiegare. Utile solo come tappa, non come arrivo.

### Scartate

- Aritmetica FP propria (IEEE single o 48 bit) senza ROM: single non
  guadagna nulla, 48 bit costa qualche KB di Z80 nuovo da validare.
- Stringere l'esponente per rubare bit alla mantissa: 1-2 bit, e si
  perde range.
- Float "in scatola" nell'heap con un handle di una cella: serve una
  gestione della vita degli oggetti, e l'heap MMU7 e' gia' scarso.

## 4. Confronto

| | A | B | C | D |
|---|---|---|---|---|
| Mantissa in memoria | 24 | 32 | 32 | 24 / 32 |
| Perdita per operazione | si', meta' | no | no | solo a fine espr. |
| Velocita' rispetto a oggi | = | = o poco peggio | meglio | meglio in catena |
| Compatibilita' sorgenti | piena | rotta | rotta | piena |
| Modifiche al core | no | no | no (o hook, D3) | no |
| Lavoro | ore | giorni | giorni | 1-2 giorni |

## 5. Raccomandazione

**Arrivo a 5 byte (C preferita, B da confrontare: sez. 6) nel modulo che
si chiamera' `FLOATING`; il 2 celle di oggi rinominato e congelato (D4).**

C e' l'unica che elimina la perdita e in piu' accelera; B paga la stessa
rottura di API senza il guadagno di velocita', ma e' piu' robusta e non
ha lo stack nascosto. La scelta si fa dopo la Fase 0, sui numeri e su due
esempi scritti in tutti e due gli stili.

L'opzione A e' il miglioramento intermedio mentre D2/D3 maturano, ed e'
**applicata** (2026-10-12, da provare): arrotondamento in `W>` e B = 0
in `>W` insieme, perche' con l'arrotondamento la compensazione `$A2` non
serve piu'. In `W>` l'arrotondamento e' saltato quando l'esponente e' 0
(intero piccolo) o `$FF` (il riporto uscirebbe nel bit di segno). Non
fatti, di proposito, finche' la A non e' provata: `(FRAC)` a scala unica
e la revisione dei test. `src/FP-OPT.f` non e' referenziato da nessuna
parte ed e' rimasto com'era. Nota: in `test/FLOATING-TESTS.f` la riga 36
(`1. FATAN 2. F*`) non ha il `}T` di chiusura.

## 6. Elementi per D2: 3 celle (B) o stack separato (C)

**Il sorgente FP puro e' identico.** In tutti e due i casi le parole di
stack sono le `F`:

    oggi   : HYP  2DUP F*  2SWAP 2DUP F*  F+ FSQRT ;
    B e C  : HYP  FDUP F*  FSWAP FDUP F*  F+ FSQRT ;

La differenza si vede solo dove float e interi si incontrano.

| Aspetto | B (3 celle, stack dati) | C (calculator stack) |
|---|---|---|
| Interi e float mescolati | l'intero finisce sotto una tripla: `ROT`/`-ROT` di gruppi, o variabili | stack distinti: `( n -- ) ( F: x -- y )`, nessun rimescolamento |
| Indici di `DO`, indirizzi, contatori | convivono con le triple | non vedono i float |
| Costo di una operazione | 2 depositi + `FOP` + 1 prelievo | solo `FOP` |
| `FDUP` `FSWAP` | CODE nuovo, 6-12 byte mossi | opcode ROM, gia' pronti |
| `.S` | mostra 3 celle hex per float (illeggibili) | non li mostra: serve `F.S`, che pero' stampa i valori |
| `ABORT` / errore | lo stack si svuota da solo (`SP!`) | resta sporco: serve `FCLEAR` (sez. 3) |
| Capienza | quella dello stack dati | zona libera BASIC sotto `$6200`, **senza protezione ROM** |
| Dimenticare un vecchio `2DUP` | lavora su 2 celle di 3: errore silenzioso | lo stack dati e' vuoto: errore subito |
| Float sul return stack | possibile (3 `>R`) | no |
| Standard Forth-2012 | ammesso, ma con 3 celle e' insolito | il modello di default: codice e testi altrui portabili |
| Dipendenza dallo stato della ROM | solo durante la singola `FOP` | permanente: tutto cio' che azzera STKEND azzera i float |

Cosa pesa davvero, in ordine:

1. **Robustezza contro comodita'.** B non puo' corrompere il core e si
   ripulisce da sola; C richiede un controllo di profondita' scritto
   bene e una regola per `FCLEAR`. E' l'unico vero argomento per B.
2. **Codice misto.** La guida BASIC -> vForth e i demo grafici mescolano
   coordinate intere e calcolo FP: e' il caso in cui C si scrive molto
   meglio.
3. **Velocita'.** Da misurare, non da stimare (Fase 0): se il guadagno
   di C fosse piccolo l'argomento 1 peserebbe di piu'.

Domande a cui la Fase 0 deve rispondere prima di scegliere:

- Quanti float stanno tra STKEND e RAMTOP, in DOES e in DOT?
- Qualcosa nel sistema tocca il calculator stack mentre vForth gira
  (ROM BEEP, NextZXOS, l'uscita su stream file)? Lo lascia bilanciato?
- Quanto vale il rapporto di tempo del banco di prova (sez. 8)?

## 7. Elementi per D3: i letterali

Il punto: `INTERPRET` dopo `NUMBER` esegue sempre, per 10 celle,
`DPL @ 1+ IF DLITERAL ELSE DROP LITERAL THEN` (`L2.asm` righe 44-63), e
poi `?STACK`. Per B non c'e' problema (sez. 3). Per C il float non deve
lasciare celle sullo stack dati. Quattro vie:

| Via | Come | Core | Fragilita' |
|---|---|---|---|
| a1 | `FNUMBER` sposta il proprio indirizzo di ritorno di 20 byte e atterra su `?STACK` | intatto | dipende dalla forma esatta di `INTERPRET` |
| a2 | due rattoppi dello stesso tipo di oggi: `NUMBER` -> `FNUMBER` e la cella `DLITERAL` -> una parola che, se il numero era un float, fa `2DROP` e altrimenti `DLITERAL` | intatto | due celle da verificare al caricamento invece di una |
| b | aggancio nel core: `NUMBER` segnala "gia' gestito" | cambia | nessuna, ma nuovo build |
| c | parola-prefisso `F# 3.14`, nessun rattoppo | intatto | nessuna |

Elementi:

- **a2 e' la piu' vicina a quello che gia' c'e'**: `FP-INIT` oggi
  verifica e rattoppa la cella 32 del corpo di `INTERPRET`; la seconda
  cella sta a un offset fisso da quella. `FNUMBER` mette il float sul
  calculator stack (o in compilazione compila `(FLIT)` + 5 byte),
  restituisce un doppio fittizio con `DPL` >= 0 e alza un flag; la
  parola al posto di `DLITERAL` lo legge. `NO-FLOATING` ripristina due
  celle. Nessun gioco sul return stack.
- **a1** risparmia un rattoppo ma manipola il return stack dentro una
  parola chiamata da `INTERPRET`: meno leggibile, stessa dipendenza.
- **b** costa una release intera: `/bump-build` (9 file), DOT allineato,
  `src/F18e.f` allineato e `/check-f18e` su CSpect, rigenerazione dei
  paragrafi dinamici del manuale. Ha senso solo se l'aggancio serve
  anche ad altro (un "recognizer" generale); per i soli float a2 da' lo
  stesso risultato. Nota: in `INTERPRET` c'e' ancora, commentato, un
  vecchio tentativo `NMODE @ IF ...` proprio in quel punto.
- **c** e' l'unica che elimina alla radice la trappola
  `FLOATING`/`INTEGER` (tutorial 060 sez. 8), ma `F# 0.5 F# 2.0 F*` e'
  pesante da scrivere e da leggere. Buona come rete di sicurezza: puo'
  esistere comunque, accanto a una delle altre.

Sintassi, indipendente dalla via:

| | `3.14` | `3.14E0` / `1E3` | Modo |
|---|---|---|---|
| Oggi | float se `NMODE` = 1, doppio se 0 | float solo con `NMODE` = 1 | necessario |
| Standard Forth-2012 | doppio, sempre | float, sempre (in base 10) | nessuno |
| Mista | float se `NMODE` = 1, doppio se 0 | float sempre (in base 10) | facoltativo |

- Lo standard toglie del tutto il modo, e con lui la trappola del
  misparsing silenzioso; ma `0.5E0` e' scomodo e i sorgenti esistenti
  (tutorial 024, test, guida BASIC) usano tutti `3.14`.
- La mista e' compatibile con tutti e due: chi scrive con la `E` non ha
  bisogno di `FLOATING`/`INTEGER`, chi vuole `3.14` accende il modo come
  oggi. Con `NMODE` = 0 oggi `1E3` in base 10 non e' un numero valido,
  quindi riconoscerlo non rompe nulla.
- La `E` vale solo in base 10: in `HEX` e' una cifra (`1E3` = 483).

## 8. Fasi

**Fase 0 -- misure e prova pratica (CSpect, a mano).** Non impegna a
nulla e chiude D2. Tre cose, tutte fattibili con il modulo di oggi:

1. Numeri "prima": errore di `PI`, `0.1 10. F* 1. F-`, `0.5 2. F* 1.
   F-`, una catena di 20 `FSQRT`/quadrati, `16777217. D>F F>D`.
2. Spazio e banco di prova: STKBOT (`$5C63`), STKEND (`$5C65`), RAMTOP
   (`$5CB2`) a prompt in DOES e in DOT; poi il tempo di

       : T-OGGI  1000 0 DO  2DUP FSQRT 2DROP  LOOP ;
       : T-C     >W  1000 0 DO  49 FOP 40 FOP 2 FOP  LOOP  W> ;

   (49, 40, 2 = duplicate, sqr, delete del calcolatore). `T-C` e' il
   costo di una operazione nel modello C; `T-OGGI` vale anche per B.
3. Mini-prototipo di C in una decina di righe, sopra `FOP` `>W` `W>`
   esistenti (`: FDUP 49 FOP ;` `: F+ 15 FOP ;` `: S>F 0 >W ;` ...), per
   riscrivere due o tre esempi veri -- quelli del tutorial 024 e un
   listato della guida BASIC -- e guardarli accanto alla versione a
   celle sullo stack dati.

Prova di D5 nella stessa seduta (non provato, da verificare):

    INTEGER
    CODE W.  ( F: r -- )
        $C5 C, $D5 C,       \ push bc, push de
        $DD C, $E5 C,       \ push ix
        $CD C, $2DE3 ,      \ call PRINT-FP
        $DD C, $E1 C,       \ pop ix
        $D1 C, $C1 C,       \ pop de, pop bc
        $DD C, $E9 C,       \ jp (ix)
        SMUDGE
    FLOATING  3.14 >W W.

`PRINT-FP` consuma il numero in cima al calculator stack e stampa fino
a 8 cifre significative: con il modulo di oggi dovrebbe mostrare a occhio
proprio il byte perso (un `3.14` che non esce `3.14`). Da osservare:

- formato (niente zeri finali, notazione E fuori intervallo), nessun
  controllo di larghezza: `F.R` e `PLACES` restano a `F>PAD`, o spariscono;
- la stampa passa da `RST $10` dentro la ROM, **non** da `(EMITC)`:
  niente salvataggio di MMU7 (regola in `lib/CLAUDE.md`, caso `13 SELECT
  WORDS`), quindi provarla anche con l'uscita rediretta su file;
- va definita in modo `INTEGER`: sotto `FLOATING` i letterali `$C5` non
  passano da `NUMBER`.

**Fase 1 -- il modulo nuovo.** Nell'ordine: primitive di stack e ponte
(`FDUP`.. `S>F` `F>D`), controllo di overflow (solo C), memoria (`F@ F!
FVARIABLE FCONSTANT`), letterali (D3) con `(FRAC)` a scala unica, output
(D5), poi le funzioni (una riga ciascuna). Suite di test propria, con
tolleranza invece del confronto bit a bit. Si sviluppa sotto un nome
provvisorio, senza toccare `lib/floating.f`.

**Fase 2 -- scambio dei nomi (D4), in un solo commit.** Il 2 celle
diventa `lib/<nome-legacy>.f` (nome da scegliere, es. `FLOATING4`: 4 byte
contro 5) e continua a definire `FLOATING` `INTEGER` `NO-FLOATING`, cosi'
i sorgenti che lo usano cambiano solo la riga `NEEDS`. Il nuovo diventa
`lib/floating.f`. I due si escludono a vicenda. Nello stesso commit:
`test/FLOATING-TESTS.f`, tutorial 024 e 060 sez. 8, `help/`, cosi'
`NEEDS FLOATING` non resta mai rotto. Correggere qui anche il commento
`$A2` in `lib/FP-INTERFACE.f`.

**Fase 3 -- documentazione.** Voce in `lib/CLAUDE.md`, capitolo numerico
della guida BASIC, testo per il paragrafo 3.7 del manuale in `products/`
(lo incolla l'autore).

## 9. Verifica

L'emulatore headless ha solo stub `RET` per la ROM (`ROM_STUBS` in
`emu/emulator.py`): `RST $28` non funziona, quindi oggi ogni prova FP
passa da CSpect e dall'autore. Da valutare in Fase 0: mappare un'immagine
della ROM 48K in `$0000-$3FFF` nell'emulatore tenendo le intercettazioni
esistenti; se regge, i test FP diventano automatici (`emu/test_*.py`).

## 10. Decisioni

Prese (autore, 2026-10-12):

- **D1.** `$A2` in `>W` e' una compensazione voluta del troncamento. Il
  modulo a 2 celle la conserva.
- **D4.** `FLOATING` sara' il modulo nuovo; il 2 celle viene rinominato.
  Resta da scegliere il nome legacy (Fase 2).
- **D5.** `F.` prova la `PRINT-FP` della ROM (`$2DE3`), mai usata finora:
  prova in Fase 0; cosa fare di `F.R`/`PLACES` si decide dopo averla vista.

Aperte:

- **D2.** B o C: elementi in sez. 6, si chiude dopo la Fase 0.
  Orientamento del piano: C, salvo che le misure diano poco spazio sotto
  `$6200` o un guadagno di velocita' trascurabile.
- **D3.** Letterali: elementi in sez. 7. Orientamento del piano: via a2
  con sintassi mista. Riguarda solo C; con B i letterali non pongono
  problemi.
