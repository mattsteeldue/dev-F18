# ZAP-BASIC-LOADER: loader BASIC generato, a costo di memoria nullo

**Status**: Design Plan (non ancora implementato)
**Author**: Matteo Vitturi (con Claude)
**Date**: 2026-09-17 (rev. 3)

> **Decisioni gia' prese dall'autore**
> - Il template di partenza e' `Standard-Loader.bas` (radice del repo).
> - **Un deliverable = una directory**: i binari prendono nomi fissi
>   (`core.bin`, `user.bin`, `heap.bin`) dentro la cartella del gioco.
> - La direzione e' **la modalita' interpretativa**. Il motivo non e' la
>   dimensione del deliverable: e' il timore di **esaurire il dizionario** con
>   un gioco grosso, restando senza spazio di lavoro proprio quando si deve
>   salvare. Vedi sez. 2.

---

## 1. Stato attuale

`lib/ZAP.f` congela la sessione in tre binari -- `NAME-core.bin` (da `0 +ORIGIN` a
**`HERE`**), `NAME-user.bin` (da `R0 @` a `$E000`), `NAME-heap.bin` (2 pagine 8K = banco
16K 16) -- e patcha `COLD` perche' punti alla parola scelta, poi a `BYE`.

Il loader BASIC no: il manuale (sez. 2.8) dice *"You have to manually modify the basic
loader 'Standard-Loader.bas'"*. Il ciclo manuale e' *carica il template -> cambia la riga
7930 `DATA "Game"` -> `RUN` -> la riga 9800 `SAVE b$ LINE 10`*. Detokenizzato:

```
  10 ; vForth 1.7                     1210 LET a=USR 25446
  20 ; Standalone                     1220 STOP
  30 ; executable loader              7930 DATA "Game"      <-- l'unica riga da cambiare
1110 CLEAR 25087                      8000 DEFPROC filenames()
1120 PROC filenames()                 8020  RESTORE : READ f$
1150 LOAD c$ CODE 25446               8030  LET c$=f$+"-core.bin"
1160 LOAD d$ CODE 53640               8040  LET d$=f$+"-user.bin"
1170 LOAD h$ BANK 16                  8050  LET h$=f$+"-heap.bin"
                                      8060  LET b$=f$+".bas"
                                      8100 ENDPROC
                                      9800 SAVE b$ LINE 10
```

Fragilita': gli indirizzi `25446` (`ORIGIN`), `53640` (`R0 @`), `25087` (RAMTOP) e
`BANK 16` sono cablati, e **`R0` dipende dal build** -- un core ricompilato produce `.bin`
che il template carica all'indirizzo sbagliato, in silenzio. Inoltre il template conosce
un solo banco di heap (i blocchi 17/18/19 in `SAVE-HEAP` sono commentati).

---

## 2. Il vincolo vero: headroom, non dimensione del file

`SAVE-CORE` salva fino a `HERE`, quindi tutto `lib/ZAP.f` finisce dentro il binario del
gioco. Misura in emulatore headless (`emu/repl.py`, build 2026-08-20):

```
HERE U. HP@ U.   ->  33200  3360      (sessione pulita)
NEEDS ZAP
HERE U. HP@ U.   ->  33811  3594
```

**611 byte di code space, 234 di name space.** Sul deliverable e' il 3.8% di
`game-core.bin` (16023 byte): fastidioso ma tollerabile.

**Il problema serio e' un altro**: quei 611 byte ZAP li chiede **quando il gioco e' gia'
caricato**, cioe' nel momento di massima occupazione del dizionario. Un gioco che ha
quasi riempito il code space non lascia lo spazio per caricare lo strumento che deve
salvarlo -- e il fallimento arriva dopo ore di lavoro, con la sessione ormai da buttare.

### 2.1 Quanto spazio c'e' davvero

| | `HERE` | libero (tetto ~53940) |
|---|---|---|
| sessione pulita | 33200 | 20740 *(coincide col banner: "Dictionary: 20740 bytes free")* |
| core vForth da solo | -- | il core occupa 33200-25446 = 7754 byte da `ORIGIN` |
| **chomp-chomp caricato** | ~41469 *(= `ORIGIN` + 16023, dal `game-core.bin` pubblicato)* | **~12471** |
| chomp-chomp + `NEEDS ZAP` | ~42080 | ~11860 |

Il tetto del code space e' l'area user/stack subito sotto i block buffer (`R0 @` = 53640
nella build misurata). chomp-chomp -- 49 KB di sorgente Forth -- occupa **8269 byte** di
dizionario e ne lascia 12 KB: potrebbe crescere ancora della meta' prima che ZAP
diventi un problema. Ma il margine finisce davvero **intorno ai 20 KB di gioco**, e a
quel punto non c'e' rimedio a posteriori.

### 2.2 Cosa consuma, in ordine di pericolosita'

1. **La compilazione di ZAP** -- 611 byte. La elimina lo script interpretativo (sez. 4-5):
   non compila niente, quindi `HERE` non avanza di un byte.
2. **Lo scratch `PAD`** -- e' `HERE + 68` (`L1.asm:1182`), quindi **si sposta con il
   dizionario**: a dizionario pieno, `PAD` e il buffer header di `F_OPEN` finiscono
   *oltre* il tetto, dentro l'area user. Questo e' il consumo che resta anche dopo aver
   eliminato il punto 1, ed e' quello a cui nessuno pensa. Soluzione in sez. 5.1.
3. **Un eventuale buffer per il `.bas`** -- 700-1000 byte. Eliminabile del tutto
   (sez. 6.1).
4. **I dati da salvare** -- costo **zero**: `F_WRITE` scrive direttamente dall'area
   sorgente, senza copia intermedia. Verificato scrivendo 32 byte da `0 +ORIGIN` senza
   alcun buffer (sez. 4.1). Piu' il gioco e' grosso, piu' grande il file, ma
   l'operazione non chiede un byte di RAM in piu'.

**Obiettivo di progetto, da qui in avanti: ZAP deve poter girare con il dizionario a
zero byte liberi.** E' un obiettivo raggiungibile -- sez. 5.1.

---

## 3. Una directory per deliverable: cosa cambia

Con `game/core.bin`, `game/user.bin`, `game/heap.bin` **il loader non contiene piu' nulla
che dipenda dal gioco**. Niente `DATA`, niente `PROC filenames()`, niente concatenazione
di stringhe: e' lo stesso file per qualunque applicazione, a parita' di build.

```
  10 ; vForth 1.8 standalone
 100 CLEAR 25087
 110 LOAD "heap.bin" BANK 16
 120 LOAD "core.bin" CODE 25446
 130 LOAD "user.bin" CODE 53640
 200 LET a=USR 25446
 210 STOP
```

Conseguenze, tutte semplificanti:

- **Il `.bas` non si genera: si copia.** Un prototipo preparato una volta in BASIC sulla
  macchina, quindi corretto per costruzione, e copiato byte per byte accanto ai binari.
  Nessun tokenizzatore, nessun ricalcolo di lunghezze, nessun checksum da rifare.
- **Niente costruzione di nomi a runtime**: i tre nomi sono costanti, e il solo elemento
  variabile e' il prefisso di directory.
- L'autostart si ottiene dal campo 18-19 dell'header PLUS3DOS (sez. 7.1), gia' impostato
  nel prototipo: le righe 9800/9999 del template storico spariscono.
- Il prototipo resta valido finche' `ORIGIN`, `R0` e il banco heap non cambiano. Non e'
  un peggioramento (oggi sono cablati comunque), ed e' irrobustibile: vedi 6.2.

---

## 4. Modalita' interpretativa: cosa funziona davvero

Una rev. precedente di questo piano concludeva che l'interpretativo fosse impraticabile
perche' `DO`/`LOOP` sono compile-only. **Conclusione sbagliata, corretta dall'autore**:
un ciclo a estremi noti e pochi si srotola, e basta. Verificato in emulatore -- i nove
blocchi dei messaggi letti da un file incluso, srotolati, passano senza problemi:

```
8 BLOCK DROP 9 BLOCK DROP 10 BLOCK DROP ... 16 BLOCK DROP    -> ok
```

Resta vero che in interpretazione **non esistono `DO`, `IF` e le altre parole
compile-only**: ogni iterazione dev'essere scritta per esteso e ogni scelta la fa
l'operatore decidendo quali righe eseguire. Per ZAP non e' una limitazione reale: gli
unici cicli sono a estremi noti (i 9 blocchi, gli 1-4 banchi di heap).

### 4.1 Verifiche sperimentali

Tutte eseguite in `emu/repl.py`, riga per riga, senza compilare nulla.

**Un file si scrive interamente in interpretazione, con il file handle che sopravvive
sullo stack fra una riga e l'altra:**

```
H" zt.bin" FAR 1+ PAD 10 - $0E F_OPEN
41 ?ERROR                                  \ .S ->  14          (il fh)
DUP 0 +ORIGIN 32 ROT F_WRITE               \ .S ->  14 32 0     (fh, scritti, flag)
47 ?ERROR DROP
F_CLOSE 42 ?ERROR
```

-> `zt.bin`, 32 byte, contenuto corretto a partire da `$6366`. **Lo stack e' la variabile
globale dello script**: nessuna `VARIABLE`, nessun `CREATE`.

**Anche i nomi si compongono in interpretazione**, con `PAD` come buffer stabile
(`CMOVE` e' una primitiva: il loop e' dentro, in Z80):

```
H" zt" FAR PAD OVER C@ 2+ CMOVE                             \ counted-z-string in PAD
PAD COUNT + H" -a.bin" FAR COUNT 1+ ROT SWAP CMOVE          \ suffisso + NUL in coda
PAD 1+ PAD 70 + $0E F_OPEN 41 ?ERROR
```

-> `zt-a.bin` e `zt-b.bin` creati correttamente. (Con la directory per deliverable questo
passaggio diventa superfluo, ma e' utile saperlo possibile.)

**La conversione numero -> ASCII e' interpretativa**: `25446 0 <# #S #> TYPE` stampa
`25446`. Serve se un giorno si vorranno patchare gli indirizzi dentro il `.bas`.

**`F_SEEK` esiste come parola del dizionario** (`next-opt0.asm:13`): una patch a offset
noto dentro un file si fa senza buffer e senza ricerca.

**Trappola confermata -- MMU7.** Lo stesso script che scriveva `zt-a.bin` correttamente ha
prodotto un `zt-b.bin` **vuoto** scrivendo da `$E000`: l'ultimo `H"` aveva rimappato MMU7
su un'altra pagina. Con `$0000 FAR` davanti, i 16 byte vengono scritti. `F_WRITE`
**non** ha segnalato errore -- ha riportato 0 byte scritti e il flag a 0. E' esattamente
la classe di problema descritta in `lib/CLAUDE.md`: qualunque riga che scriva dalla
finestra `$E000` deve mappare la pagina **immediatamente prima**, e il fallimento e'
silenzioso.

### 4.2 Dove eseguire lo script: Screen, non file

Uno script interpretativo ha comunque bisogno di stare da qualche parte, e la scelta ha
una conseguenza tecnica precisa.

- In un **file `.f` `INCLUDE`d**, la riga in corso di interpretazione vive nel buffer del
  BLOCK 1, che e' l'unico blocco il cui contenuto in RAM **non e' riproducibile da disco**
  (`planners/PLAN-MITIGATION-BLOCK-1-BUG.md`, par. 2). Se il pool a 6 buffer lo ricicla,
  la riga e' persa.
- In uno **Screen caricato con `n LOAD`**, il buffer che contiene lo script e' un blocco
  ordinario: se viene sfrattato, `BLOCK` lo rilegge da disco e riottiene **gli stessi
  byte**. Lo sfratto costa una lettura, non una corruzione.

**Quindi lo script ZAP va in uno Screen, non in un file.** In piu' si edita con `EDIT`
direttamente sulla macchina -- che e' il punto in cui si cambia il nome della directory.

(Nota sul bug: un test mirato -- 7 blocchi distinti dentro **una sola riga** di un file
incluso -- **non** l'ha riprodotto in emulatore. Non basta a dire che non esista, il caso
di `test/CHOMP-MAZE-TESTS.f` e' documentato su hardware; ma la scelta dello Screen rende
la questione irrilevante per ZAP.)

---

## 5. Architettura proposta

**ZAP diventa uno Screen interpretativo**, non una libreria. Due Screen (32 righe da 64
colonne) sono abbondanti; `util/putscr.pl` li installa da un sorgente versionato in git,
e `EDIT` li modifica sulla macchina.

Screen 12-13 (BLOCK 24-27) sono liberi -- la scansione di `!Blocks-64.bin` segna occupati
1-11 e poi nulla fino a 35 -- e adiacenti all'area riservata 0-10 documentata nel
CLAUDE.md di root, dove andranno aggiunti.

Struttura dello script, in ordine di esecuzione:

| Righe | Operazione | Note |
|---|---|---|
| 1 | nome della directory, letto con `(LINE)` dallo Screen stesso | **l'unica riga da editare**; vedi 5.1 |
| 2 | `' NOME` + patch di `COLD` (2 store) | interpretativo, `'` funziona a prompt/sorgente |
| 3-4 | apri/scrivi/chiudi `core.bin` | `0 +ORIGIN HERE OVER -` |
| 5-7 | i 9 `BLOCK` srotolati, poi `user.bin` | `R0 @ $E000 OVER -` |
| 8-10 | `heap.bin` -- `$0000 FAR` **prima** di ogni `F_WRITE` | vedi trappola MMU7, 4.1 |
| 11-13 | copia del prototipo `.bas` | un `F_READ` + un `F_WRITE`, sez. 6 |

Nessuna definizione, nessun `NEEDS` (salvo `H"`, vedi punti aperti), quindi `HERE` non
avanza di un byte e **il binario pubblicato non contiene niente di ZAP**.

`lib/ZAP.f` resta dov'e', come alternativa comoda per chi non vuole editare uno Screen;
gli si applica semmai l'intervento della sez. 8.

### 5.1 Scratch fuori dal dizionario (il punto che chiude la sez. 2.2)

Eliminata la compilazione, l'ultimo consumo legato a `HERE` e' `PAD`. Va evitato del
tutto, e la soluzione e' gia' in mano: **lo Screen dello script e' esso stesso il
buffer**.

`(LINE) ( riga screen -- a 64 )` e' una parola core (`L2.asm:497`): restituisce
l'indirizzo della riga dentro un **block buffer**, che vive **sotto `$E000`, fuori dal
code space** (sei buffer da 512 byte piu' 4 di intestazione, fra `R0 @` e `$E000`). Quei
512 byte sono RAM gia' allocata, che il dizionario non vede e non puo' invadere.

Conseguenze pratiche:

- **Il nome della directory sta scritto in una riga dello Screen** -- che e' anche l'unica
  riga da editare. `0 12 (LINE)` lo consegna gia' in RAM scrivibile: basta sostituire con
  uno `0` il primo spazio dopo il nome per ottenere la z-string che `F_OPEN` vuole.
- **Il buffer e' auto-riparante.** Se il pool lo ricicla (i 9 `BLOCK` dei messaggi lo
  fanno), `(LINE)` lo rilegge da disco e riottiene **gli stessi byte** -- e' un blocco
  ordinario, non il BLOCK 1 (sez. 4.2). Basta richiamare `(LINE)` prima di ogni uso
  invece di conservare l'indirizzo: costa una lettura, mai una corruzione.
  L'unica cautela e' che le modifiche fatte nel buffer (il NUL) non sopravvivono al
  riciclo: vanno rifatte dopo ogni `(LINE)`, e mai `UPDATE`.
- **L'header a 8 byte di `F_OPEN`** entra nello stesso buffer, a un offset piu' avanti
  (una riga inutilizzata dello Screen, es. `15 12 (LINE)`).

Cosi' ZAP non tocca `PAD`, non tocca `HERE`, e **gira con il dizionario a zero byte
liberi**: l'obiettivo della sez. 2.2. L'unica memoria che usa e' lo stack dati e un
buffer di blocco che esisteva gia'.

---

## 6. Il `.bas`: copia, non generazione

### 6.1 Percorso base

Il prototipo (`zap-loader.bas`, preparato una volta in BASIC sulla macchina e verificato
a mano) si copia accanto ai binari:

```
apri prototipo in lettura -> F_READ in un buffer -> F_CLOSE
apri game/loader.bas in scrittura -> F_WRITE -> F_CLOSE
```

Il buffer **non** va preso sopra `HERE`: sarebbe l'unico consumo di dizionario rimasto,
proprio quello che la sez. 2.2 vuole azzerare. I file reali stanno in 653-744 byte, cioe'
**due letture da 512** in un block buffer: `F_READ` 512 -> `F_WRITE` 512 -> `F_READ` il
resto -> `F_WRITE` il resto. Quattro righe srotolate, nessun buffer nuovo. (Se un giorno
servisse un'area contigua piu' grande, l'heap ne ha 62 KB liberi -- ma va mappata con
`FAR` prima di ogni `F_READ`/`F_WRITE`, vedi la trappola MMU7 in 4.1.)

**Terza opzione, la piu' economica di tutte: non copiarlo affatto.** Con la directory per
deliverable il `.bas` e' costante a parita' di build: puo' essere messo nella cartella del
gioco dal PC, o con un `.cp` sul Next, una volta. ZAP non ha alcun obbligo di produrlo --
e se il dizionario e' davvero al limite, questa e' la via da preferire.

### 6.2 Irrobustimento facoltativo: patchare gli indirizzi

In un `.bas` tokenizzato **ogni numero compare due volte**: in ASCII (quello che si vede
in `LIST`) e subito dopo in forma binaria a 5 byte introdotta da `$0E`:

```
0x0E  00  sign  lo  hi  00        sign = 00 positivo, FF negativo
```

Verificato: `25087` -> `0E 00 00 FF 61 00` (`$61FF`); `25446` -> `0E 00 00 66 63 00`
(`$6366`); `16` -> `0E 00 00 10 00 00`.

**Il valore che il BASIC esegue e' quello binario, l'ASCII e' cosmetico -- e la forma
binaria ha lunghezza fissa.** Quindi `ORIGIN`, `R0 @`, RAMTOP e il banco heap si possono
sostituire nel buffer, prima di riscriverlo, **senza toccare nessuna lunghezza di riga,
nessun campo dell'header e nessun checksum**. Se il nuovo valore ha lo stesso numero di
cifre (tutti gli indirizzi reali ne hanno 5) si patcha anche l'ASCII e il `LIST` resta
onesto.

Serve conoscere gli offset: si ricavano una volta con `util/bas2txt.py` (sez. 10) e si
scrivono nello script come costanti. Cosi' la fragilita' "`R0` cambia col build" sparisce:
il valore arriva dalla sessione viva.

Se si preferisce non patchare, resta comunque **necessario** un controllo: confrontare i
valori del prototipo con `0 +ORIGIN` / `R0 @` e segnalare la discrepanza. Un errore
silenzioso diventa un messaggio.

---

## 7. Anatomia del `.bas` (verificata sui file del repo)

Serve a preparare il prototipo, a leggere `util/bas2txt.py` e alla patch facoltativa 6.2.

### 7.1 Header PLUS3DOS -- 128 byte

| Offset | Dim | Contenuto |
|---|---|---|
| 0-7 | 8 | `"PLUS3DOS"` |
| 8 | 1 | `$1A` |
| 9-10 | 2 | issue `1`, version `0` |
| 11-14 | 4 | lunghezza totale del file, header incluso, LE |
| 15 | 1 | tipo (0 = BASIC program) |
| 16-17 | 2 | lunghezza programma + variabili |
| 18-19 | 2 | **riga di autostart**; `>= $8000` = nessuno |
| 20-21 | 2 | offset area variabili (= lunghezza del solo programma) |
| 22-126 | 105 | zero |
| 127 | 1 | checksum = somma dei byte 0..126 mod 256 |

Verifica (checksum ricalcolato = memorizzato in tutti e tre i file):

| File | totale | prog+var | autostart | prog | checksum |
|---|---|---|---|---|---|
| `Standard-Loader.bas` | 653 | 525 | `$80FF` (nessuno) | 525 | 164 |
| `demo/chomp-chomp/game.bas` | 681 | 553 | 10 | 481 | 58 |
| `Forth18_loader.bas` | 744 | 616 | 20 | 616 | 74 |

(`game.bas` ha 72 byte di variabili in coda, residuo del `SAVE` fatto dopo aver eseguito
la PROC. Il prototipo non ne avra': `prog = prog+var`.)

Se un giorno servisse ricalcolare il checksum, `inc/checksum.f`
(`CHECKSUM ( a u -- n )`, somma a..a+u inclusi) fa esattamente questo: `hdr 126 CHECKSUM`.

### 7.2 Corpo

```
[num riga: 2 byte BIG-endian] [lunghezza corpo: 2 byte LITTLE-endian] [corpo ... 0x0D]
```

La lunghezza include il `0x0D`. Esempio reale: `00 0A | 0D 00 | "; vForth 1.7" 0D`.
Il numero di riga e' **l'unico campo big-endian del formato**.

### 7.3 Token (solo per leggere il prototipo)

`CLEAR $FD`, `LOAD $EF`, `CODE $AF`, `LET $F1`, `USR $C0`, `STOP $E2`, `SAVE $F8`,
`LINE $CA`, `DATA $E4`, `RESTORE $E5`, `READ $E3`, `PRINT $F5`, `PAUSE $F2`, `GO TO $EC`,
piu' i NextBASIC `BANK $9A`, `DEFPROC $91`, `ENDPROC $92`, `PROC $93` (questi quattro
**osservati** nei `.bas` del repo, non letti da una tabella ufficiale). Il commento si
scrive `;` ed e' ASCII puro, non un token. Con la directory per deliverable il loader usa
solo `CLEAR LOAD CODE BANK LET USR STOP`.

---

## 8. Alternativa/complemento: limitare il salvataggio (intervento Z)

Non serve allo Screen interpretativo -- che non compila nulla -- ma serve a `lib/ZAP.f`,
e vale la pena registrarlo perche' e' economico e verificato.

`SAVE-CORE` puo' fermarsi al `DP` che c'era **prima** che ZAP fosse caricato: il codice di
ZAP resta in RAM sopra quel limite, gira, e non entra nel file. Il limite e' gia'
recuperabile oggi, perche' `lib/ZAP.f` comincia con `MARKER TASK` e un `MARKER` salva nel
proprio PFA le celle che servono (`L3.asm:516`). Verificato:

```
HERE U.           ->  33200      (prima di NEEDS ZAP)
' TASK 2- U.      ->  33200      (dopo)   <-- coincidono
' TASK >BODY U.   ->  33205      (le 5 celle del marker)
```

Quindi `0 +ORIGIN  ZAP-LIMIT OVER -` al posto di `0 +ORIGIN HERE OVER -`, piu' il
ripristino di `HP`/`LATEST`/`CONTEXT`/`CURRENT`/`VOC-LINK` prima di `SAVE-HEAP` (altrimenti
l'immagine heap contiene una catena di nomi che punta a codice non piu' presente).

**`DP` non si ripristina**: `PAD` e' `HERE + 68` (`L1.asm:1182`) e `OPEN>` usa `PAD 10 -`
come buffer header per `F_OPEN` -- abbassare `DP` farebbe scrivere `F_OPEN` dentro il
codice di ZAP in esecuzione.

Effetto collaterale da chiudere con una guardia: caricare ZAP **prima** dell'applicazione
taglierebbe via l'applicazione, in silenzio. Basta verificare che l'xt del target sia
`< ZAP-LIMIT`. Regola d'uso da rendere esplicita: **`NEEDS ZAP` per ultimo**.

---

## 9. Correzioni collaterali

1. **`SAVE-HEAP` dinamico.** Banchi 16K in uso = `HP@ 13 RSHIFT 2/ 1+` (i 3 bit alti di
   `ha` sono la pagina 8K relativa alla base). Nello Screen interpretativo si traduce in
   righe srotolate per i banchi effettivamente presenti, piu' le righe `LOAD ... BANK n`
   corrispondenti nel prototipo.
2. **Bug latente nelle guardie commentate di `SAVE-HEAP`**: `$8000 HP@ <` usa il confronto
   **con segno**; oltre i 32 KB `HP@` ha il bit 15 alto ed e' negativo, quindi il test
   sbaglia. Va `U<`, o meglio sparisce sostituito dal conteggio sopra.
3. **Annotazione, fuori scope**: `SAVE-USER` fa `17 8 DO I BLOCK DROP LOOP`, ma gli Screen
   dei messaggi 4-8 sono i BLOCK 8..**17** -- l'ultimo manca; e con sei buffer
   sopravvivono comunque solo gli ultimi sei letti. I messaggi disponibili
   nell'eseguibile standalone sono meno di quanti il codice prometta.

---

## 10. Fasi

**Fase 1 -- prototipo.** L'autore prepara `zap-loader.bas` in BASIC sulla macchina (nomi
fissi, autostart nell'header) e verifica **a mano** che carichi e faccia partire un gioco
gia' esistente, copiato in una directory. Finche' questo passo non e' verde non ha senso
scrivere Forth.

**Fase 2 -- lo Screen.** Scrittura dello script interpretativo, sorgente in
`util/zap-screen.scr`, installazione su Screen 12-13 con `putscr.pl`. Prova in emulatore:
i quattro file devono comparire nella directory indicata.

**Fase 3 -- heap multi-banco.** Correzioni 9.1 e 9.2, con le righe `BANK n` nel prototipo.

**Fase 4 -- irrobustimento (facoltativa).** Patch/controllo degli indirizzi nel `.bas`
(sez. 6.2).

**Fase 5 -- documentazione.** Tutorial 059 va rivisto in profondita': sez. 2 (i nomi dei
file), sez. 6 (non piu' una procedura manuale), e la sez. 4 sul patch di `COLD` resta
valida ma va riferita allo Screen. Va aggiunta una sezione nuova su **come si scrive un
sorgente destinato al deliverable**: il budget di dizionario della sez. 2, il prologo
collaborativo della sez. 12.1, e la regola che ZAP non puo' rimediare a posteriori. Screen 12-13 nella tabella degli Screen riservati del
CLAUDE.md di root. Manuale `.odt` sez. 2.8: si segnala all'autore, mai automatico.

**Facoltativa -- intervento Z** su `lib/ZAP.f` (sez. 8), indipendente da tutto il resto.

---

## 11. Verifica

- **Emulatore headless**: `F_OPEN`/`F_WRITE`/`F_CLOSE`/`F_SEEK`/`F_READ` sono tutti
  emulati (`emu/emulator.py`), e le prove della sez. 4.1 mostrano che lo stile
  interpretativo funziona end-to-end. Il test della fase 2 e' la comparsa dei quattro
  file, con `core.bin` di dimensione pari a `HERE - ORIGIN`.
- **`util/bas2txt.py`**: detokenizzatore di controllo che stampi header, checksum,
  lunghezze di riga e listato. Gia' scritto in forma prototipale per redigere questo
  piano (tabella token completa, numeri a 5 byte, dump dell'header); va consolidato in
  `util/`. Serve a preparare il prototipo, a ricavare gli offset della 6.2 e a verificare
  che una copia patchata sia ancora un `.bas` valido.
- **CSpect**: l'unica verifica che conta e' far partire il gioco dalla sua directory.
  `demo/chomp-chomp/` e' il banco di prova ideale -- c'e' gia' il `game.bas` fatto a mano
  da confrontare.

---

## 12. Punti aperti

1. **Creare la directory.** `F_MKDIR` **non e' esposto in vForth** (verificato: nessun
   `New_Def` per `F_MKDIR`/`F_CHDIR` nel core), quindi servirebbe una `CODE` word in
   `inc/` sul modello dei wrapper esistenti (`rst $08` + il codice esxDOS, vedi
   `next-opt0.asm:190` per `F_OPEN`). Tre modi di farlo stare nel budget della sez. 2:

   - **Fuori da vForth** -- la directory si crea da NextZXOS/Browser prima di lanciare la
     sessione. Costo zero, un passo manuale in piu'. E' la via sicura quando il
     dizionario e' al limite.
   - **`MARKER` prima del gioco** (proposta dell'autore, con una precisazione sul
     momento). Caricare la `CODE` word, creare la directory e dimenticarla **all'inizio
     della sessione, prima di includere il gioco**: il picco di occupazione non coincide
     con quello del gioco, e `FORGET` riporta `HERE` esattamente dov'era -- il dizionario
     e' uno stack, non si frammenta. Il nome della directory si conosce gia' a
     quel punto.
   - **La crea il gioco stesso** -- variante collaborativa della precedente, ed e' la
     forma da preferire. Vedi 12.1.
   - **`MARKER` alla fine**, subito prima di ZAP: funziona, ma **non risolve il caso
     limite**. `FORGET` libera *dopo*: se lo spazio manca gia', la `CODE` word non si
     carica nemmeno, e il rimedio arriva troppo tardi. Utile per tenere pulita la
     sessione, non per garantire che ZAP possa girare.

### 12.1 Contratto collaborativo: la directory la crea il gioco

Il posto naturale dove creare la directory del deliverable **non e' ZAP: e' il sorgente
del gioco**, nel proprio prologo. Il ragionamento e' quello della sez. 2: **un gioco
grosso "sa" di essere grosso**, e sa quindi che al momento del deliverable non potra'
piu' permettersi di caricare `F_MKDIR`. Se ne fa carico prima, quando il dizionario e'
ancora vuoto:

```forth
\ prologo deliverable, in testa al sorgente del gioco
MARKER -PROLOGUE
NEEDS F_MKDIR
... crea la directory del deliverable ...
-PROLOGUE                 \ HERE torna esattamente dov'era: il gioco parte da zero
\ ... da qui il gioco vero e proprio
```

Perche' e' la forma migliore fra quelle elencate:

- **Il picco non coincide mai** con quello del gioco, per costruzione, senza che
  l'utente debba ricordarsi un passo manuale nell'ordine giusto.
- **Il dato sta dove nasce**: il nome della directory e' una proprieta' del gioco, non
  di ZAP. Chi scrive il gioco lo conosce; ZAP lo troverebbe solo perche' qualcuno glielo
  ha scritto in uno Screen.
- **E' riproducibile**: ricaricare il sorgente ricrea la directory, anche su un'altra
  macchina o su una SD vuota. Nessuno stato fuori dal sorgente.
- **Degrada bene**: se il gioco e' piccolo e non gliene importa, puo' non fare nulla e
  lasciare che sia ZAP (o l'utente) a creare la directory. La convenzione serve a chi ne
  ha bisogno, non obbliga nessuno.

Il corollario va scritto a chiare lettere nel tutorial 059: **ZAP non puo' rimediare a
posteriori**. Un sorgente destinato al deliverable si scrive sapendo che l'unico momento
in cui c'e' spazio per gli strumenti e' l'inizio.
2. **Path con directory in `F_OPEN`.** Non verificato: la prova `zzdir/core.bin` in
   emulatore e' fallita con "Open error", ma `resolve_fat_name` gestisce i separatori,
   quindi la causa non e' chiara (vedi anche punto 3). Da verificare su CSpect prima di
   costruirci sopra -- e' il presupposto dell'intera scelta "una directory per
   deliverable".
3. **Stringhe senza `NEEDS`.** `H"` non e' core: usarlo costa un `NEEDS H"` -- poche
   decine di byte di dizionario, che per la sez. 2 non sono zero. Due vie da verificare,
   entrambe a costo nullo: ricavare i nomi da `(LINE)` sullo Screen (sez. 5.1), che e'
   la strada principale; oppure da `BL WORD`, che scrive a `HERE` senza allocare. La
   prova di `BL WORD` in emulatore e' **fallita** e l'eco del REPL non ha permesso di
   distinguere l'errore vero dal rumore: da riprovare con calma, perche' se funziona
   anche i nomi fissi (`core.bin`, ...) si scrivono senza una sola dipendenza.
4. **`ZAP"` (`.nex`)**: fuori scope, ma stessa famiglia -- la patch di `COLD` commentata e
   il PC cablato `$7634` (tutorial 059 sez. 8) sono altri valori cablati dove basterebbe
   derivarli dalla sessione viva.

---

## 13. File toccati

| File | Natura |
|---|---|
| `util/zap-screen.scr` | nuovo -- sorgente dello script interpretativo |
| `!Blocks-64.bin` Screen 12-13 | nuovo -- lo script, installato con `putscr.pl` |
| `zap-loader.bas` | nuovo -- prototipo, **preparato a mano in BASIC** |
| `util/bas2txt.py` | nuovo -- detokenizzatore di verifica |
| `inc/` (facoltativo) | nuovo -- `CODE` word per `F_MKDIR`, vedi punto aperto 1 |
| `lib/ZAP.f` | modificato -- correzioni sez. 9, ed eventualmente intervento Z |
| `tutorial/059-standalone-executables.f` | modificato -- sez. 2, 4, 6 |
| `CLAUDE.md` (root) | modificato -- Screen riservati |
| `doc/vForth1.8-core-en-*.odt` sez. 2.8 | **a mano, dall'autore** |
| `Standard-Loader.bas` | invariato -- loader di riferimento storico |
