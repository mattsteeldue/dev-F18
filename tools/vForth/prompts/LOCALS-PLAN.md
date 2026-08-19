# LOCALS in vForth -- design consolidato

Stato: **implementato** in `lib/LOCALS.f`, verificato sull'emulatore
headless (`emu/repl.py`). Vedi sezione 9.
Ultima revisione: 2026-08-19 -- il **trampolino** (sezioni 13-14) e' stato
sostituito da un **BRANCH di scavalco** (sezione 16): un solo thread per
FOO invece di due, niente piu' corpo anonimo. Ribalta di nuovo il verdetto
della sezione 10 sul prezzo di `SEE`: torna a rompersi, ma in una forma
peggiore di quella li' descritta -- non piu' "spazzatura", un blocco che
in prova non e' mai tornato al prompt in diversi minuti. Accettato come
regressione deliberatamente rimandata. Un'ipotesi di fix (riempire lo
splice per riallinearlo) e' stata misurata e scartata; un fix diverso,
piu' mirato (far riconoscere a `SEE` il pattern "`BRANCH` come prima
cella" e saltare l'intero splice) e' stato **esplorato e verificato ad
indirizzi** ma **non implementato** -- sezione 17.
Revisione precedente: 2026-08-18 -- i **locali in uscita** studiati in
sezione 12 sono stati **implementati** (sezione 15), con la catena di
ripristino per scope che 12.4 aveva gia' previsto, invece della catena
condivisa di 11-14. Corretto insieme anche il bug di scrittura oltre
`LOCAL-PFAS` documentato in 14.5.
Revisione precedente: 2026-08-17 -- la sintassi inline `{ ... }` e' stata
**implementata** col trampolino (sezione 13) e subito dopo semplificata
togliendo la dipendenza da `:NONAME` (sezione 14). Le due sezioni
ribaltano il verdetto della sezione 10 e correggono le misure di 11.4 e
11.5: leggerle prima di fidarsi dei numeri.
Revisione precedente: 2026-08-16 -- **i locali sono ora rientranti**, vedi
sezione 11: e' la modifica piu' importante dopo il primo impianto e
cambia quello che dicono le sezioni 6 e 10.

Obiettivo: variabili locali caricabili con `NEEDS LOCALS` (nuovo `lib/LOCALS.f`),
**senza modificare il core assembly** e **senza ridefinire nessuna word del core**.

Questo documento sostituisce interamente una prima ipotesi (frame sul return
stack + rinomina degli header nell'heap), scartata: le ragioni sono in
sezione 5, che vale la pena leggere perche' spiega perche' le strade
"ovvie" non funzionano in questo sistema.

**Deviazione dichiarata dallo standard.** Non si insegue
`forth-standard.org/standard/locals`. I locali qui sono `VALUE`-like e
vivono in celle permanenti, non in un frame; la rientranza si ottiene
salvando e ripristinando quelle celle (sezione 11). Parte del costo e'
deliberatamente scaricata sul programmatore.

---

## 1. Sintassi

> **Aggiornamento 2026-08-17.** Questa sezione descrive la forma in due
> tempi, che e' quella su cui il design e' stato costruito e che resta
> supportata. La forma **preferita** e' oggi quella inline `{ ... }`,
> costruita sopra questa: vedi sezione 13.
>
> ```forth
> : FOO   { A B C }   ... A ... B ... C ... ;
> ```

```forth
3 LOCALS-FOR FOO  A B C       \ in interpretazione, PRIMA della definizione
: FOO  LOCALS  ... A ... B ... C ... ;
```

- `LOCALS-FOR` prende **il conteggio dei locali** dallo stack, poi il
  nome della definizione che seguira', poi quel numero di nomi. Gira in
  stato di interpretazione.
- `LOCALS` e' IMMEDIATE, gira dentro la definizione, non prende argomenti.
- I locali si leggono con il solo nome (`A` spinge il valore) e si scrivono
  con `TO` (`x TO A`).

**Perche' il conteggio esplicito, in stile `inc/enumerated.f`.** Terminare
la lista a fine riga non e' portabile (2.4). Il conteggio invece arriva
qui dallo stack senza problemi, perche' `LOCALS-FOR` gira in
interpretazione: l'obiezione che aveva scartato questa forma valeva solo
per una word che gira **dentro** la definizione, dove `STATE` a 1
compilerebbe il numero come letterale invece di lasciarlo sullo stack.

Tutti i nomi devono stare sulla **stessa riga** di `LOCALS-FOR`.

---

## 2. I vincoli del core che hanno prodotto questo design

Tutti verificati sul sorgente; sono le ragioni per cui il design ha la forma
che ha.

### 2.1 `CREATE` dentro una colon-definition spezza il thread

Il costruttore di header (`CODE`, `L1.asm:1565-1594`) chiude con
`hp@ cell- ,`, e `CREATE` (`L1.asm:1599-1603`) aggiunge `$CD C,` +
`Variable_Ptr ,`. Sono tutte virgole **a `HERE`** -- che dentro una
colon-definition e' il fronte di compilazione del thread. Ogni word creata
li' dentro inserisce ~7 byte non eseguibili in mezzo al codice, e a runtime
l'IP ci cammina dentro.

**Conseguenza: i locali non possono essere creati mentre si compila.** Da
qui la scelta di creare tutto in interpretazione, prima del `:`.

### 2.2 `:` azzera `CONTEXT`

`:` (`L1.asm:17-18`) fa `CURRENT @ CONTEXT !` come prima cosa. Quindi
`CONTEXT` impostato da `LOCALS-FOR` viene **cancellato** dal `:`
successivo, e nel corpo i nomi dei locali sarebbero invisibili.

**Conseguenza: serve comunque una word dentro la definizione** (`LOCALS`)
che rimetta `CONTEXT`. Non e' una scelta estetica, e' strutturale.

Nota positiva: se il programmatore dimentica `LOCALS`, i nomi non si
risolvono e la compilazione si ferma. Fallimento rumoroso, non silenzioso.

### 2.3 Il nome di un header viene sempre dall'input stream

`CODE` (`L1.asm:1553`) inizia con `-FIND`, che parsa il nome dall'input e lo
lascia come stringa contata a `HERE`; il costruttore legge da li'
(`Code_Endif:` -> `HERE DUP C@`).

**Conseguenza: non si puo' creare una word con nome calcolato** (es. `VFOO`
da `FOO`) senza reimplementare il costruttore di header in Forth. Vedi 4.2
per il modo pulito di aggirare la cosa.

### 2.4 `WORD` sceglie il buffer su `BLK`

`WORD` (`L1.asm:1199-1211`): se `BLK @` e' non-zero usa `BLK BLOCK`,
altrimenti `TIB @`.

**Conseguenza: "parsa fino a fine riga" non e' implementabile in modo
portabile.** Sotto `LOAD` il buffer e' l'intero blocco da 512 byte e le
righe sono solo visive: `WORD` proseguirebbe oltre, inghiottendo il codice
successivo. Funziona solo in interattivo (TIB) e sotto `INCLUDE`
(`BLK`=1, una riga per volta nel buffer di BLOCK 1).

Da qui la scelta di **non** basare la sintassi sulla fine riga.

### 2.5 Il return stack e' profondo 160 byte, condivisi col TIB

Da `system.asm:230-236` con `BUFFERS equ 6`:

```
LIMIT_system = $E000
FIRST_system = $E000 - 516*6      = $D3E8
USER_system  = R0_system  = $D3E8 - 80  = $D398   <- cima del return stack
TIB_system   = S0_system  = $D398 - 160 = $D2F8
```

Il TIB cresce verso l'alto da `$D2F8`, il return stack verso il basso da
`$D398`: **condividono** quei 160 byte. Con una riga di input da 80
caratteri restano ~40 celle.

**Conseguenza: nessun frame sul return stack.** Non e' un problema per il
design finale (che non ne usa), ma e' il motivo per cui l'ipotesi
precedente e' stata abbandonata, ed e' anche il tetto pre-esistente alla
ricorsione in vForth in generale.

---

## 3. Il design

### 3.1 `LOCALS-FOR` -- in interpretazione

```
1.  controlla il conteggio contro MAXLOCALS
2.  BL WORD DROP                   \ consuma il nome della definizione
3.  CURRENT @ @  ->  SCOPE-LINK     \ ancora di adiacenza (3.3)
4.  LOC-EMPTY LOC-VOC !            \ svuota il vocabolario dei locali
5.  CURRENT @ -> OLD-CURRENT ; DEFLOCALS DEFINITIONS
6.  n volte:  0 CONSTANT
        registrando LATEST PFA nell'array LOCAL-PFAS
        e incrementando #LOCALS
7.  OLD-CURRENT @ CURRENT !        <-- CRITICO, vedi 3.4
    CURRENT @ CONTEXT !
```

`CURRENT` viene salvato in una **VARIABLE**, non con `>R`/`R>`: il
salvataggio attraverserebbe il `DO..LOOP` di creazione, e incrociare il
return stack con i parametri di loop e' proprio il pattern che in questo
repo ha gia' prodotto bug (cfr. le note su `inc/PAINT.f`).

Un locale e' una `CONSTANT` a valore 0: in vForth `VALUE` **e'**
`CONSTANT` (`inc/value.f`), quindi il PFA contiene il valore ed eseguire il
nome lo spinge. Regalo che ne consegue: **`TO` funziona gia' cosi' com'e'**
-- `inc/(TO).f` fa `' >BODY` e `'` cerca via `CONTEXT`, che durante il
corpo punta al name-space dei locali.

Modello di riferimento per il ciclo di creazione: `inc/enumerated.f`
(`0 DO I CONSTANT LOOP`), dove ogni `CONSTANT` parsa il proprio nome.

### 3.2 `LOCALS` -- IMMEDIATE, dentro la definizione

```
1.  ?COMP
2.  verifica di appaiamento (3.3); errore se fallisce
3.  <name-space> CONTEXT !        \ rende visibili i nomi nel corpo
4.  per i = #LOCALS-1 .. 0:  COMPILE LIT  LOCAL-PFAS[i] ,  COMPILE (LOC-BIND)
5.  installa la catena di ripristino (11.2): COMPILE LIT <entry> , COMPILE >R
6.  consuma la traccia:  0 #LOCALS !
```

(Il passo 4 compilava `COMPILE !` e il passo 5 non esisteva, finche' i
locali non erano rientranti: sezione 11.)

Gli store si emettono **in ordine inverso** di dichiarazione: a runtime lo
stack e' `( A B C -- )` con `C` in cima, quindi si memorizza prima `C`.
Consumando l'array dall'ultimo elemento l'ordine viene giusto da solo.

`LOCALS` **non** deve essere strutturalmente la prima word della
definizione -- quel vincolo veniva dall'ipotesi col trampolino, qui assente.
Resta un requisito *semantico*: deve girare prima che il corpo tocchi lo
stack, perche' gli store consumano gli argomenti del chiamante. In pratica:
prima word per convenzione, non per necessita'.

### 3.3 Il controllo di appaiamento (non opzionale)

Senza controllo questo compila senza errori e le due word **condividono
silenziosamente le stesse celle**:

```forth
3 LOCALS-FOR FOO A B C
: FOO  LOCALS  ... ;
: BAR  LOCALS  ... ;      \ <-- riusa lo storage di FOO
```

Sono implementate **due guardie**, entrambe verificate:

**Freschezza.** `LOCALS` consuma lo scope azzerando `#LOCALS`, e rifiuta di
girare se `#LOCALS` e' zero -> *"LOCALS: no scope declared"*. Chiude
esattamente il caso qui sopra.

**Adiacenza.** `LOCALS-FOR` registra `CURRENT @ @` (l'`ha` grezzo della
word piu' recente) in `SCOPE-LINK`; `LOCALS` verifica che
`LATEST PFA LFA @` coincida, cioe' che la definizione in corso sia
**la prima** creata dopo lo scope -> *"LOCALS: scope not adjacent"*.
La sequenza `LATEST PFA LFA @` e' l'idioma che usa gia' `MARKER`
(`L3.asm:517`), quindi e' provata dal core.

Nota sui domini di indirizzo: `LATEST` (`L1.asm:575`) e' `CURRENT @ @ FAR`,
cioe' **risolto** attraverso MMU7, mentre `LFA @` restituisce un `ha`
grezzo. L'ancora va quindi registrata come `CURRENT @ @`, non come
`LATEST`, altrimenti si confronterebbero due domini diversi.

**Il nome della definizione e' per ora solo documentativo**: viene
consumato ma non confrontato. Il confronto vero e proprio richiederebbe di
leggere i byte del nome dall'heap con il pattern di `ID.` (`?>HEAP` +
`TRAVERSE`, `L1.asm:1538`), gestendo END bit e flag nel count byte. La
guardia di adiacenza copre gia' il caso pericoloso; il confronto del nome
aggiungerebbe solo l'intercettazione del refuso
(`3 LOCALS-FOR FOO ...` seguito da `: BAR LOCALS`). Rimandato.

### 3.4 Le due trappole nell'ordine delle operazioni

**`CURRENT` va ripristinato prima che finisca `LOCALS-FOR`.** Se resta
puntato al name-space dei locali, il `: FOO` successivo crea **FOO stesso**
li' dentro, e FOO sparisce dal dizionario al prossimo azzeramento senza che
nulla lo segnali.

**`CONTEXT` non va invece mai ripristinato.** Ci pensa il `:` successivo
(2.2). E `ABORT` (`L2.asm:204`) fa `FORTH DEFINITIONS`, quindi qualunque
errore ripulisce da solo. E' questo che permette di non ridefinire `;`.

---

## 4. Dove vivono i nomi -- deciso: variante A

**Decisione presa.** Si usa un vocabolario unico riusabile (A). In pratica
il name-space dei locali e' raggiungibile solo finche' non si dichiara un
altro scope: l'ispezione a posteriori dei locali di una definizione
passata non e' possibile. E' una perdita accettata consapevolmente.

La variante B resta registrata in 4.2 perche' e' un'aggiunta pulita e
**rimandabile**: `LOCALS` trova il name-space attraverso un puntatore
registrato da `LOCALS-FOR`, non cercandolo per nome, quindi il codice di
`LOCALS` e' identico nei due casi e passare ad B non lo tocca.

### 4.1 Variante A -- un solo `DEFLOCALS` riusabile (scelta)

Un `VOCABULARY DEFLOCALS` creato una volta sola, azzerato da ogni
`LOCALS-FOR`. L'azzeramento e' **una singola `!`** sulla cella LATEST
del vocabolario (struttura in `L2.asm:84-107` e commento a `L2.asm:140-148`).

- Costo per definizione: solo le `CONSTANT` dei locali.
- Uno scope vivo per volta -- sufficiente, visto che
  `LOCALS-FOR` precede immediatamente il suo `:`.
- I locali di una definizione passata diventano irraggiungibili (e' lo
  scoping che vogliamo), ma i loro byte restano.

### 4.2 Variante B -- un vocabolario per definizione

Il prefisso `VFOO` **non e' ottenibile** (2.3). Il modo pulito e' un
vocabolario **contenitore**, cosi' il nome non va calcolato:

```forth
VOCABULARY SCOPES                 \ una volta sola
\ poi, dentro LOCALS-FOR:
CURRENT @ >R   <SCOPES DEFINITIONS>
VOCABULARY                        \ riparsa FOO e lo crea dentro SCOPES
R> CURRENT !
```

Si ottiene un vocabolario chiamato `FOO` dentro `SCOPES`, senza chirurgia e
senza mutare il buffer di input. In debug `SCOPES FOO WORDS` elenca i locali
di quella definizione.

- Costo aggiuntivo per definizione: ~11 byte di dizionario, un header
  nell'heap, e una voce in `VOC-LINK`.
- Vantaggio reale: ispezionabilita' a posteriori, e piu' scope
  contemporaneamente vivi.

Due meccaniche da conoscere prima di adottarla:

**La catena di ricerca cresce.** `VOCABULARY` (`L2.asm:88-92`) inizializza
la cella LATEST del nuovo vocabolario con `CURRENT @ @`, cioe' lo aggancia
alla word piu' recente del padre (commento a `L2.asm:142-146`). Con `SCOPES`
come padre, ogni scope si aggancia a quelli creati prima: dopo trenta
definizioni ogni lookup fallito nel corpo cammina trenta voci in piu'.
Si rimedia con **una singola `!`** subito dopo la creazione, riscrivendo
quella cella per puntare direttamente alla null-word di FORTH -- la stessa
operazione che A usa per azzerare.

**`FORGET` non tocca `VOC-LINK`.** `FORGET` (`L3.asm:487-508`) fa `HP !`,
`DP !` e rilega la LATEST del solo vocabolario corrente; solo `MARKER`
salva e ripristina `VOC-LINK` (`L3.asm:513-517`). Quindi dimenticare
qualcosa definito prima di una serie di `LOCALS-FOR` lascia quei
vocabolari agganciati a `VOC-LINK` ma in spazio recuperato, con danno
differito alla prossima `VOCABULARY` o al prossimo `MARKER`. E' un rischio
**pre-esistente** del sistema (vale gia' per `ASSEMBLER` ed `EDITOR`), ma B
lo moltiplica di uno o due ordini di grandezza creando un vocabolario per
definizione. Lavorando con `MARKER` invece di `FORGET` il problema non si
presenta.

---

## 5. Strade scartate (e perche')

Registrate perche' sembrano tutte ragionevoli finche' non si guarda il core.

| Strada | Perche' no |
|---|---|
| Frame sul **return stack** | 160 byte condivisi col TIB (2.5). Una word con 4 locali costerebbe 12 byte per invocazione. (La rientranza di 11 usa comunque il return stack, e costa anche di piu': 20 byte. Cio' che restava impraticabile non era l'uso del return stack, ma il frame -- che avrebbe richiesto di rifare `VALUE` e `TO`.) |
| Storage su **`HERE`** con rewind a `EXIT` | Collide con qualunque compilazione a runtime, e `THROW` (`inc/throw.f`) non ripristinerebbe `HERE`. |
| Creare i locali **a compile-time** dentro la definizione | Splicing nel thread (2.1). |
| **`BRANCH` di scavalco** sopra gli header spliciati | Funziona (4 byte, offset relativo, `L0.asm:233` + `THEN` in `L3.asm:848`) ma lascia dati dentro il thread: `SEE` decodifica spazzatura. |
| **Rinomina degli header** nell'heap (pool di slot) | Tecnicamente possibile, ma il rischio e' corruzione ritardata del dizionario. Scartata come troppo pericolosa. |
| Trampolino **`NOOP`+`EXIT`** + corpo `:NONAME` (stile `inc/defer.f`) | ~~Funziona, ma `:NONAME` (`inc/_noname.f`) costa 6 byte di heap e **si aggancia alla catena di `CURRENT`** come voce fantasma; e il preambolo separato e' piu' grande e piu' lento degli store inline. Reso inutile dallo spostamento in interpretazione.~~ **RIPESCATA e adottata** per implementare `{ ... }` (sezione 13): il trampolino non serviva a `LOCALS-FOR`, ma e' l'unica cosa che libera `HERE` per i `CREATE` dei locali **dentro** la definizione. L'obiezione sui 6 byte e sulla voce fantasma e' poi caduta con la sezione 14, che costruisce a mano la CFA del corpo anonimo invece di chiamare `:NONAME`. |
| Locali come **viste sullo stack** (`PICK`) | L'offset dal TOS cambia a ogni push/pop e il compilatore non lo traccia attraverso `IF`/`LOOP`. E i valori andrebbero poi tolti **da sotto** i risultati. |
| Terminatore di lista + rewind di `>IN` | Reso inutile dal conteggio implicito di `LOCALS-FOR`. |
| Parsing **fino a fine riga** | Non portabile sotto `LOAD` (2.4). |
| Ridefinire **`EXIT`** globalmente | Romperebbe `lib/see.f:100`, `inc/;s.f:10`, `inc/exec_.f:20`, che ne catturano l'xt. |
| Ridefinire **`;`** o **`:`** | Non serve: con storage statico non c'e' niente da liberare all'uscita. |

---

## 6. Limiti accettati

**~~Niente ricorsione, niente rientranza.~~ SUPERATO -- vedi sezione 11.**
Il testo originale diceva che rimuovere il limite "richiede storage
dinamico, cioe' un design diverso". Era sbagliato in un punto: non serve
storage dinamico, basta salvare e ripristinare le celle statiche. Il
limite residuo non e' piu' semantico ma dimensionale -- la profondita' di
ricorsione consentita dal return stack (11.4).

**Costo permanente per scope**: `n` celle di dizionario piu' gli header
nell'heap (`nome+5` byte ciascuno), non recuperabili.

**Cap su `MAXLOCALS`**: `LOCALS-FOR` deve rifiutare oltre il limite
dell'array `LOCAL-PFAS`.

**Ombreggiamento**: un locale che si chiama come una word esistente la
nasconde dentro quella definizione. E' il senso dello scoping, ma va
documentato.

**Nessuna ispezione a posteriori**: col vocabolario unico (4) i locali di
una definizione passata non sono piu' raggiungibili. Perdita accettata.

**`FORGET` da' errore 23 finche' non si digita `FORTH`**. `FORGET`
(`L3.asm:489-491`) inizia con `CURRENT @ CONTEXT @ - 23 ?ERROR`, cioe'
pretende `CONTEXT` uguale a `CURRENT`. Dopo una definizione con locali
`CONTEXT` punta al name-space dei locali finche' non arriva il `:`
successivo (2.2). Ruga d'uso, non un difetto.

---

## 7. Passi di implementazione

1. Scheletro `lib/LOCALS.f`: `MARKER NO-LOCALS`, `VOCABULARY DEFLOCALS`,
   `VARIABLE #LOCALS`, `CREATE LOCAL-PFAS`, buffer `SCOPE-NAME`.
2. `LOCALS-FOR` senza il controllo di appaiamento: sbirciata con `>IN`,
   switch di `CURRENT`, ciclo `0 CONSTANT` alla `ENUMERATED`, ripristino di
   `CURRENT`. Verificare a mano che `: FOO` finisca in FORTH e non in
   `DEFLOCALS` (trappola 3.4).
3. `LOCALS`: `CONTEXT !` + compilazione degli store. Test minimo:
   `LOCALS-FOR SQ N` / `: SQ LOCALS N N * ;` / `5 SQ .`
4. Controllo di appaiamento (3.3) e azzeramento della traccia. Test
   negativo esplicito: due `LOCALS` con un solo `LOCALS-FOR` **devono**
   dare errore.
5. Verifica che `TO` funzioni sui locali senza modifiche (`NEEDS TO`).
6. Regressione: `test/CORE-TESTS.f` con e senza LOCALS caricato; nuovo
   `test/LOCALS-TESTS.f` in notazione `{...}T` (`test/CLAUDE.md`).
7. `help/LOCALS.txt`, tutorial numerato, e una riga in `lib/CLAUDE.md`.
8. Encoding: ASCII 7 bit, niente TAB, ultimo byte `0x0A`, penultimo non
   `0x20` (bug noto di `INCLUDE`).
9. Variante B (4.2) solo se serve.

Nessuna modifica al core: **non serve un nuovo build number**.

---

## 8. Questioni chiuse e rimaste

Chiuse:

- `MAXLOCALS` = **8**.
- **Niente locali non inizializzati**: `LOCALS-FOR` dichiara solo
  locali che vengono caricati dallo stack. Avrebbe richiesto di far
  elencare a `LOCALS` il sottoinsieme da caricare, reintroducendo il
  parsing dei nomi dentro la definizione e il problema di terminazione
  di 2.4.
- Name-space: **variante A** (vocabolario unico riusabile, sezione 4).

Rimaste:

- Nome definitivo delle due word: `LOCALS-FOR` e' esplicito ma lungo.
- Confronto del nome della definizione (3.3), oggi non implementato.

---

## 9. Stato e verifica

`lib/LOCALS.f` implementato e provato su `emu/repl.py` sui binari correnti
(`forth18e.bin` / `ram8.bin`, build 2026-08-01). Nessuna modifica al core,
nessuna word del core ridefinita: **non serve un nuovo build number**.

Casi verificati:

| Caso | Atteso | Esito |
|---|---|---|
| `3 LOCALS-FOR SUM3 A B C` / `: SUM3 LOCALS A B + C + ;` / `1 2 3 SUM3 .` | `6` | ok |
| `TO` su un locale (`... P Q + TO P P ;`) | `7` | ok |
| Annidamento: `OUTER` con locali che chiama `INNER` con locali | `25` | ok |
| Scoping: `FORTH` poi `P .` | non trovato | `P? is undefined.` |
| `MAXLOCALS` al limite: 8 locali | `36` | ok |
| `0 LOCALS-FOR` e `9 LOCALS-FOR` | errore | `LOCALS: bad count` |
| `LOCALS` senza scope dichiarato | errore | `LOCALS: no scope declared` |
| Definizione non adiacente allo scope | errore | `LOCALS: scope not adjacent` |
| `NO-LOCALS` (MARKER) e poi `LOCALS` | scaricato | `LOCALS? is undefined.` |

Artefatti creati e verificati sull'emulatore:

- `lib/LOCALS.f` -- il modulo.
- `test/LOCALS-TESTS.f` -- 12 asserzioni `T{ ... }T`, tutte passate
  (silenzio = pass). Registrato nella tabella di `test/CLAUDE.md`.
- `tutorial/061-locals.f` -- registrato in `lib/TUTORIAL.f` (`TUT-TABLE`
  + `TUT-MAX` portato a 61). Caricato con `061 TUTORIAL` e le sue word
  di esempio verificate: `MULADD`=26, `HYPOT2`=25, `ACCUM`=6,
  `CLAMP-ADD`=100.
- `help/locals.txt`, `help/locals-for.txt`.

- Sezione `### LOCALS (named local variables)` in `lib/CLAUDE.md`.

Non ancora fatto: la regressione completa di `test/CORE-TESTS.f` con il
modulo caricato.

La tabella qui sopra e' quella del primo impianto (locali statici). I casi
aggiunti dalla rientranza -- ricorsione, `EXIT` anticipato, `SEE`, tetto
del return stack -- sono in **11.5**.

---

## 10. Nota: quanto costerebbe la sintassi inline `{ ... }`

Domanda posta a design chiuso: quanto costa una coppia `{` / `}` che
dichiari i locali **dentro** la definizione, come nelle forme standard,
al posto di `LOCALS-FOR` esterno?

### Implementazione: poca, e il modulo si accorcia

Si riusa tutto quello che c'e' gia': `DEFLOCALS`, `LOC-VOC`, `LOC-EMPTY`,
`LOCAL-PFAS`, il ciclo che compila gli store, il salva/ripristina di
`CURRENT`. Le parti nuove sono due:

- lo **scavalco**: `COMPILE BRANCH HERE 0 ,` prima di creare i locali e
  `HERE OVER - SWAP !` dopo (offset relativo, `L0.asm:233`);
- il **ciclo di parsing con terminatore**: sbircia il token, se e' `}`
  esce, altrimenti arretra `>IN` e lascia che `0 CONSTANT` lo riparsi.

E soprattutto **spariscono le due guardie** di 3.3: `SCOPE-LINK`,
l'adiacenza e la freschezza di `#LOCALS` esistono solo perche'
dichiarazione e uso stanno in due punti diversi. Unendoli, l'intera
classe di bug di appaiamento svanisce per costruzione.

Netto: ~15 righe, il file si accorcia. Il terminatore esplicito e' anche
piu' portabile della fine riga scartata in 2.4: funziona sotto `LOAD`.

Costo a runtime: +4 byte per definizione, un `BRANCH` eseguito una volta
per chiamata. Trascurabile.

### Prezzo 1 -- `SEE` si rompe

Con lo scavalco il thread della definizione **contiene gli header dei
locali**. `lib/see.f:80` riconosce `BRANCH` e lo stampa con `DEB-B`, ma
poi riprende a decompilare dalla cella successiva, che e' in mezzo agli
header: da li' emette spazzatura fino a fine definizione, senza mai
risincronizzarsi.

Oggi `SEE` funziona perfettamente su una word con locali, perche' il suo
thread contiene solo codice ordinario. E' una regressione reale su uno
degli strumenti di debug principali del sistema, ed e' esattamente il
motivo per cui lo scavalco sta fra le strade scartate in sezione 5.

Il trampolino (`NOOP`+`EXIT` + corpo `:NONAME`) eviterebbe la spazzatura,
ma `SEE FOO` mostrerebbe solo lo stub di due celle -- inutile lo stesso --
e costa 6 byte di heap piu' una voce fantasma nella catena di FORTH per
ogni definizione.

### Prezzo 2 -- i nomi `{` e `}` sono gia' occupati

Verificato sul repo: `help/{.txt` **e' il file di help di `<`** e
`help/}.txt` e' quello di `>`, perche' nella mappatura FAT `<` diventa
`{` e `>` diventa `}`.

Le due word potrebbero esistere (vivono in `lib/LOCALS.f`, non servono
file `inc/`), ma **non potrebbero avere un file di help proprio**:
`HELP {` pescherebbe la descrizione di `<`. Vie d'uscita: un'altra grafia
(`{{ }}`, `LOCALS{ }`), oppure la nota qui sotto.

**Nota dell'autore -- sovraccaricare gli help di `<` e `>`.** Invece di
trattare la collisione come un blocco, si possono **estendere**
`help/{.txt` e `help/}.txt` perche' servano entrambe le letture: la
descrizione di `<` (risp. `>`) piu' un rimando a `LOCALS`. Chi digita
`HELP {` cercando i locali trova comunque il puntatore giusto.

Il prezzo e' che il file di `<` parla anche d'altro, quindi chi chiede
`HELP <` legge due righe che non gli servono -- costo piccolo e
accettabile. Se si adotta questa strada, **la grafia letterale `{` `}`
non e' piu' preclusa**: resta solo il Prezzo 1 (`SEE`) a decidere.

### Verdetto

> **SUPERATO il 2026-08-17 -- vedi sezione 13.** `{ ... }` e' stata
> implementata, e per la strada che questa sezione non aveva considerato:
> non lo **scavalco** con `BRANCH`, ma il **trampolino** (che la sezione 5
> aveva scartato per un'altra ragione, ormai decaduta). E' stata scelta
> proprio la "terza via" qui sotto: le due forme convivono, `{ ... }` e'
> costruita sopra `LOCALS-FOR`/`LOCALS` e non le sostituisce.
>
> Del Prezzo 1 resta la parte che riguarda il trampolino, e si e'
> avverata: `SEE FOO` mostra solo lo stub di due celle (misura in 14.4).
> Non si e' invece mai materializzata la spazzatura da scavalco descritta
> sopra, perche' lo scavalco non e' stato usato.

Con la nota dell'autore sopra, il Prezzo 2 si riduce a due righe in due
file di help gia' esistenti. **Resta quindi solo `SEE` a decidere**: se
non serve decompilare le word con locali, il cambio conviene -- meno
codice e meno modi di sbagliare. Se invece `SEE` e' uno strumento di
lavoro, la forma esterna attuale e' l'unica che lo lascia intatto.

Terza via non ancora valutata: implementare `LOCALS{ ... }` come
**variante aggiuntiva** accanto a `LOCALS-FOR`, lasciando la scelta al
singolo caso d'uso. Costo: la somma dei due, piu' la manutenzione di due
percorsi.

---

## 11. Rientranza (2026-08-16) -- implementata e verificata

Domanda posta a design chiuso: due chiamate vive della stessa word con
locali devono poter mantenere contesti distinti. Risposta: si ottiene
**senza toccare `VALUE` ne' `TO`**, e senza ridefinire `EXIT`, `;` o `:`.

### 11.1 Shallow binding, non frame

L'ipotesi di partenza -- dare ai locali uno storage dinamico e farli
leggere come `frame + offset` -- e' quella **scartata**, perche' obbliga
a tre cose insieme:

- i locali non sarebbero piu' `CONSTANT`, quindi `TO` non funzionerebbe
  piu' da solo: `inc/(TO).f` fa `' >BODY` e compila `LIT body !`, che per
  un frame slot e' l'indirizzo sbagliato. Servirebbe riconoscere la
  classe "locale" dentro `(TO)` (confronto del code field) oppure una
  `TO` ombra dentro `DEFLOCALS` con fallback -- in entrambi i casi si
  modifica una word del core, che e' esattamente cio' che il modulo ha
  evitato fin qui;
- la lettura di un locale passerebbe da un push diretto a
  `LP @ + @` con un `DOES>` di mezzo: piu' lenta a ogni singolo uso, e i
  locali si usano molte volte per definizione;
- servirebbe comunque un hook all'uscita per liberare il frame, cioe'
  lo stesso meccanismo di 11.2. Il frame non lo evita, lo aggiunge.

La strada presa e' invece lo **shallow binding** (la stessa tecnica delle
special variables Lisp): la cella resta unica e permanente, e a essere
salvato e ripristinato e' il suo **contenuto**.

```
ingresso:  per ogni locale, sul return stack finiscono (indirizzo cella,
           valore precedente); poi gli argomenti del chiamante vengono
           scritti nelle celle
uscita:    i valori precedenti tornano nelle celle
```

Mentre l'attivazione interna gira, le celle contengono i valori **suoi**;
quando esce, l'attivazione esterna ritrova i propri esattamente dove li
aveva lasciati. Poiche' i nomi dei locali sono visibili solo dentro la
definizione che li ha dichiarati, il binding dinamico e quello lessicale
qui non sono distinguibili: nessun'altra word puo' osservare la
differenza.

Il regalo di 3.1 resta intatto: un locale e' ancora una `CONSTANT`,
quindi `TO` continua a funzionare senza modifiche, e la lettura resta
un push diretto.

### 11.2 Come si aggancia l'uscita senza ridefinire `EXIT`

Il punto delicato. Il ripristino deve avvenire su **ogni** via d'uscita,
compreso un `EXIT` anticipato dentro un `IF`, e ridefinire `EXIT` e'
escluso (sezione 5: `lib/see.f`, `inc/;s.f`, `inc/exec_.f` ne catturano
l'xt).

Si sfrutta come `EXIT` e' fatto davvero (`L0.asm:1425`): preleva l'IP dal
return stack (`DE`, che cresce verso il basso) e ci salta dentro. Quindi
**basta mettere un altro indirizzo sopra a quello del chiamante**:

```
return stack all'inizio del corpo (dalla cima):
    indirizzo della catena di ripristino   <- lo trova l'EXIT del corpo
    valore precedente / cella   x n
    indirizzo di ritorno al chiamante      <- lo trova l'EXIT della catena
```

L'`EXIT` che chiude la definizione non torna al chiamante: atterra nella
catena, che ripristina le celle e termina con un `EXIT` proprio, e *quello*
torna al chiamante. Un `EXIT` anticipato fa esattamente la stessa cosa.

La catena e' un mini-thread costruito a mano una volta sola:

```forth
CREATE (LOC-EXIT)
    ' (LOC-POP) MAXLOCALS (LOC-CHAIN)   \ 8 celle (LOC-POP)
    ' EXIT ,
```

Una definizione con `n` locali entra nella catena `MAXLOCALS - n` celle
piu' avanti, cosi' esegue esattamente `n` ripristini. Nessuna catena per
definizione, nessun byte dentro il thread della definizione.

L'idioma del thread costruito a mano non e' nuovo nel repo: `inc/exec_.f`
fa gia' `HERE ' EXIT ,` e ci salta dentro caricando `bc`. E' la prova che
una cella di thread contiene proprio il valore restituito da `'`.

Le due word di supporto si passano da sole il proprio indirizzo di
ritorno, che e' in cima al return stack quando partono:

```forth
: (LOC-BIND)  ( x a -- )    R> SWAP DUP >R  DUP @ >R  ROT SWAP !  >R ;
: (LOC-POP)   ( -- )        R> R> R> !  >R ;
```

### 11.3 Cosa cambia in `LOCALS` -- diff minimo

`LOCALS-FOR` **non cambia di una riga**. In `LOCALS` cambia una parola nel
ciclo esistente (`COMPILE !` diventa `COMPILE (LOC-BIND)`) e si
aggiungono tre righe in coda:

```forth
    COMPILE LIT   #LOCALS @ LOC-ENTRY ,   COMPILE >R
```

L'installazione della catena deve essere **l'ultima cosa compilata**: se
i binding venissero dopo, sarebbe un valore salvato -- non l'indirizzo
della catena -- a trovarsi in cima quando scatta l'`EXIT`.

**La versione statica, per confronto: `lib/doc/LOCALS-static.f`.** Il primo
impianto non e' mai finito in un commit (`59d15e9` registro' solo le
tabelle in `lib/CLAUDE.md` e `test/CLAUDE.md`; i sorgenti entrano in
`c31543b` gia' rientranti), quindi non e' recuperabile da git. Quel file e'
una **ricostruzione** fatta a partire dall'attuale `lib/LOCALS.f` togliendo
esattamente quanto descritto qui sopra: niente `(LOC-BIND)`, `(LOC-POP)`,
`(LOC-CHAIN)`, `(LOC-EXIT)`, `LOC-ENTRY`, ciclo di binding con `COMPILE !`
e nessuna deviazione dell'`EXIT`. Serve a leggere il costo della rientranza
in termini di codice; non e' una libreria mantenuta, definisce gli stessi
nomi di `lib/LOCALS.f` (`MARKER NO-LOCALS` compreso) quindi le due non
convivono in una sessione, e `test/LOCALS-TESTS.f` e il tutorial 061 non
girano contro di essa perche' usano `RECURSE`.

### 11.4 Il prezzo, misurato

**Return stack.** `4+4n` byte per attivazione oltre all'indirizzo di
ritorno, su 160 byte condivisi col TIB (2.5). Misurato sull'emulatore con
`FIB` a 1 locale: `15 FIB` passa, `20 FIB` sfonda il buffer di input e
corrompe il dizionario **senza messaggio d'errore**. Regola pratica:
~15 livelli con 1 locale, ~6 con 4, ~3 con 8.

> **Da rimisurare dopo il 2026-08-17.** I numeri qui sopra sono presi su
> build 2026-08-01, quando la definizione con locali era una sola word e
> non c'era trampolino. Con `{ ... }` (13) ogni attivazione paga in piu'
> l'indirizzo di ritorno del trampolino, e dalla sezione 14 quel costo
> ricade su **ogni livello di ricorsione**, non piu' solo sull'ingresso:
> `RECURSE` rientra dalla word esterna, quindi due `Enter_Ptr` per
> livello invece di uno. Delta: **+1 cella (2 byte) per livello**, cioe'
> `6+4n` invece di `4+4n` quando la ricorsione passa da `RECURSE`. La
> regola pratica va quindi letta al ribasso finche' non si rifa' la
> misura di 11.5 sui binari correnti.

Notare che un frame vero sarebbe costato meno (2n byte invece di 4n): la
meta' della spesa e' l'indirizzo della cella, che sta li' solo perche' la
catena di ripristino e' condivisa fra tutte le definizioni. Una catena
per definizione (compilata dopo il corpo, quindi con le celle inline)
scenderebbe a `2+2n`, ma richiederebbe un terminatore al posto di `;` --
piu' veloce, e con un modo nuovo e silenzioso di sbagliare. Non fatto.

**Velocita'.** Ogni locale costa una chiamata a `(LOC-BIND)` (10
primitive) in ingresso e una a `(LOC-POP)` (5) in uscita, contro un solo
`!` prima. Se dovesse pesare, le due word sono candidate naturali a
diventare `CODE` in Z80 -- ma allora il modulo smette di essere Forth
puro.

**`ABORT` e `THROW` scavalcano la catena.** `ABORT` rifa `RP!`, e `THROW`
(`inc/throw.f`) ripristina l'RP salvato da `CATCH`: in entrambi i casi i
ripristini non vengono eseguiti e le celle restano coi valori interni.
E' innocuo **perche' ogni ingresso ri-lega tutti i locali prima che il
corpo parta** -- proprieta' gia' garantita da 8 ("niente locali non
inizializzati"). Il corollario e' che non si deve costruire nulla che
legga un locale fuori dalla propria definizione.

**Nessun overflow check.** vForth non ne ha da nessuna parte, e non ne e'
stato aggiunto uno qui: costerebbe primitive a ogni attivazione. La
conseguenza e' che il fallimento a fondo stack e' silenzioso (vedi sopra).

### 11.5 Verifica sull'emulatore

Tutto su `emu/repl.py`, binari correnti (build 2026-08-01). Nessuna
modifica al core: **non serve un nuovo build number**.

| Caso | Atteso | Esito |
|---|---|---|
| `test/LOCALS-TESTS.f` preesistente (12 asserzioni) | silenzio | passa |
| `5 FACT` (ricorsiva, `N` usato **dopo** la chiamata) | `120` | ok |
| `5 TRI` ricorsiva | `15` | ok |
| `10 FIB` / `15 FIB` (doppia ricorsione) | `55` / `610` | ok |
| `20 FIB` | -- | sfonda il return stack, sistema corrotto |
| `DEPTH` prima e dopo ogni caso | `0` | ok |
| `EXIT` anticipato dentro `IF` | `999` / `70` | ok |
| `TO` su un locale | `7` / `30` | ok |
| 8 locali (`L-EIGHT`) | `36` | ok |
| `SEE` su una word con locali | thread leggibile | ok: `LIT n (LOC-BIND) LIT n (LOC-BIND) LIT n >R U U * V V * + EXIT` |

Il caso `SEE` e' quello che decide fra questo design e la sintassi inline
`{ ... }` di sezione 10: il thread continua a contenere **solo codice**,
quindi il decompilatore resta intatto. La sezione 10 va riletta con
questo in mano -- il suo "Prezzo 1" e' ancora l'unico argomento
in gioco, e la rientranza non lo cambia.

> **Corretto il 2026-08-17.** La riga `SEE` e il paragrafo qui sopra
> valgono solo per la forma `LOCALS-FOR`/`LOCALS` **senza** trampolino.
> Da quando `LOCALS` passa anch'essa da `(LOC-OPEN)`/`(LOC-CLOSE)` (13),
> `SEE` su una word con locali mostra lo stub, non il corpo: misura in
> 14.4. Il resto della tabella e' invariato, e la ricorsione e' stata
> ri-verificata sui binari correnti dopo la sezione 14 (sempre 14.4).

---

## 12. Locali in uscita (2026-08-16) -- studio, non implementato

Domanda posta a rientranza chiusa: si possono dichiarare locali che
all'uscita **vengono spinti sullo stack come risultati**, invece di essere
soltanto ripristinati? Qui sotto: dove si aggancerebbero, che cosa
costringerebbero a cambiare nel design attuale, e che cosa si guadagna
davvero. **Nessun codice scritto**: gli schizzi Forth di questa sezione non
sono mai stati compilati ne' provati.

### 12.1 Due letture, una sola interessante

**(a) Parametro per riferimento** (l'`out`/`var` di Ada e Pascal): il
chiamante passa l'indirizzo di una cella e la definizione ci scrive dentro.
Non richiede nulla di nuovo -- si passa un indirizzo come qualunque altro
argomento, lo si tiene in un locale e si usa `!`. Non e' un problema di
locali, e non se ne parla oltre.

**(b) Risultato nominato**: un locale che non viene caricato dal chiamante
ma **consegnato al chiamante**, in modo che la definizione dichiari il
proprio effetto di uscita invece di costruirlo a mano sullo stack.

```forth
2 LOCALS-FOR /MOD2  A B -- Q R        \ sintassi ipotetica, vedi 12.5
: /MOD2  ( a b -- q r )
    LOCALS
    A B /  TO Q
    A B MOD TO R
;
```

E' la lettura studiata qui.

### 12.2 La baseline: oggi si fa gia', a mano

Va detto subito, perche' ridimensiona tutto il resto: **il risultato
nominato e' gia' ottenibile senza aggiungere niente**. Basta nominare il
locale come ultima cosa della definizione:

```forth
: /MOD2  LOCALS  A B / TO Q  A B MOD TO R   Q R ;
```

Ed e' **corretto**, non un caso fortunato: `Q R` spinge i valori mentre le
celle contengono ancora quelli dell'attivazione in corso; solo dopo l'`EXIT`
la catena di 11.2 ci rimette i valori del chiamante. L'ordine e' quello
giusto per costruzione.

La domanda quindi non e' *se si puo'*, ma se **renderlo dichiarativo** vale
la macchineria. Vedi il verdetto in 12.8.

### 12.3 Il vincolo che decide tutto: spingere prima di ripristinare

Il valore di un locale in uscita va letto dalla cella **prima** che la
catena la riscriva col valore del chiamante. Quindi non si puo' fare
"prima tutti i ripristini, poi le spinte": sarebbero i valori del
chiamante a finire sullo stack, silenziosamente e con l'aria di funzionare
(il caso peggiore -- alla prima chiamata, con le celle a 0, il bug si
maschera).

Lettura e ripristino di uno stesso locale devono stare **nella stessa
word**, cioe' serve una variante di `(LOC-POP)` che prima spinge e poi
ripristina:

```forth
: (LOC-EPOP)  ( -- x )              \ R: old a --
    R> R> R>                        \ ( ret old a )
    DUP @                           \ ( ret old a x )
    ROT ROT !                       \ ripristina: ( ret x )
    SWAP >R                         \ ( x )
;
```

Nient'altro cambia sul return stack: un locale in uscita costa le stesse
due celle (`old`, `a`) di uno in ingresso, e la coppia porta gia' con se'
l'indirizzo, quindi la catena **non ha bisogno di conoscere staticamente
quali celle siano di uscita** -- deve solo sapere, per ogni passo, se
quello e' un `(LOC-POP)` o un `(LOC-EPOP)`.

Vale la pena fissare la corrispondenza, che qui e' tutto: `LOCALS` compila
i binding **al contrario** (indice `n-1` per primo, 3.2), quindi sul return
stack la coppia dell'indice 0 finisce in cima, e la catena la incontra per
prima. **Il passo `j` della catena corrisponde al locale dichiarato in
posizione `j`.** Di conseguenza le spinte avvengono in ordine di
dichiarazione: il primo locale di uscita dichiarato finisce piu' in basso,
l'ultimo in cima -- che e' esattamente la lettura naturale di `( -- q r )`.

### 12.4 Conseguenza strutturale: la catena diventa per scope

La catena condivisa di 11.2 non regge questa forma. Oggi e' lineare --
otto `(LOC-POP)` piu' `EXIT`, e una definizione con `n` locali ci entra
`MAXLOCALS - n` celle piu' avanti. Con due tipi di passo servirebbe una
catena `[k EPOP][n-k POP][EXIT]`, e **non esiste un punto di ingresso
unico** in una tabella lineare che dia contemporaneamente il numero giusto
di passi dell'uno e dell'altro tipo: entrando a `MAXLOCALS-k` si
otterrebbero i `k` EPOP giusti e poi tutti e otto i POP. Servirebbe una
tabella bidimensionale (~64 ingressi) o un salto calcolato.

La via pulita e' **una catena per scope**, costruita da `LOCALS-FOR` --
che gira in interpretazione, quindi puo' usare `,` liberamente (dentro
`LOCALS` non si potrebbe: `,` scriverebbe nel thread della definizione,
trappola 2.1):

```forth
\ dentro LOCALS-FOR, in coda: una cella per locale, nell'ordine di
\ dichiarazione, piu' l'EXIT finale
    HERE  LOC-THREAD !
    #LOCALS @ 0 DO
        I OUT? IF  ' (LOC-EPOP) ,  ELSE  ' (LOC-POP) ,  THEN
    LOOP
    ' EXIT ,
```

e `LOCALS` compila `COMPILE LIT  LOC-THREAD @ ,  COMPILE >R` invece di
`#LOCALS @ LOC-ENTRY ,`.

Effetti collaterali, tutti buoni tranne l'ultimo:

- spariscono `(LOC-CHAIN)`, `(LOC-EXIT)`, `LOC-ENTRY` e l'aritmetica
  `MAXLOCALS SWAP - CELLS`: il modulo si accorcia;
- **i locali di uscita possono stare in qualunque posizione** della
  dichiarazione, non solo in fondo, perche' la forma della catena e'
  decisa nome per nome;
- costo permanente aggiuntivo: `2n+2` byte di dizionario per scope, contro
  i 18 byte della tabella condivisa risparmiati una volta sola. Pareggio
  intorno agli otto scope; oltre, si spende. E' coerente con il costo
  permanente per scope gia' accettato in sezione 6, ma va scritto.

**Alternativa scartata -- marcare l'indirizzo.** Si potrebbe conservare la
catena condivisa spingendo l'indirizzo della cella con il bit 0 a 1 quando
il locale e' di uscita, e far decidere a `(LOC-POP)` a runtime. Scartata
per due motivi: i PFA delle `CONSTANT` non hanno allineamento garantito
(l'heap e il code space non promettono indirizzi pari), e il test si
pagherebbe **su ogni ripristino di ogni locale**, anche nelle definizioni
che non usano uscite.

**Alternativa scartata -- tabella di indirizzi.** Un solo passo
`LIT tbl (LOC-EMIT)` in testa alla catena, che spinge i valori leggendo una
tabella statica di indirizzi, seguito dalla catena condivisa invariata.
Funziona, ma la catena condivisa non e' raggiungibile per caduta da un
altro thread: servirebbe chiudere il prologo con `LIT entry >R EXIT`, cioe'
6 celle per scope e un secondo livello di deviazione da spiegare. La catena
per scope costa uguale (`n+1` celle) ed e' leggibile.

### 12.5 Sintassi -- tre opzioni

**Opzione 1 -- due conteggi.** `ni no LOCALS-FOR nome  in... out...`.
Immediata da implementare (nessun parsing nuovo), ma rompe la sintassi
esistente: andrebbero aggiornati `test/LOCALS-TESTS.f`, `tutorial/061`,
`help/locals-for.txt` e `lib/CLAUDE.md`. E due numeri di seguito si
scambiano facilmente.

**Opzione 2 -- declaratore addizionale.** `3 LOCALS-FOR FOO A B C` seguito
da `2 OUTPUTS Q R`. Retrocompatibile, ma la catena la costruisce l'ultimo
declaratore che gira, quindi quella gia' emessa da `LOCALS-FOR` resta
abbandonata a HERE: `2n+2` byte sprecati per ogni scope che usa `OUTPUTS`.
Recuperarli richiederebbe un rewind di `DP` che non e' piu' sicuro, perche'
`OUTPUTS` ha nel frattempo creato le proprie `CONSTANT`.

**Opzione 3 -- separatore nella lista (preferita).**

```forth
4 LOCALS-FOR /MOD2   A B -- Q R
```

Il conteggio resta uno solo e conta **i nomi**, `--` escluso. Il ciclo di
creazione sbircia il token prima di ogni `0 CONSTANT`: se e' `--` lo
consuma, registra `ni = #LOCALS @` e prosegue; altrimenti arretra `>IN` e
lascia che `0 CONSTANT` riparsi il nome. E' il ciclo di parsing con
sbirciata gia' prezzato in 10 (~10 righe), qui senza nessuno dei suoi
prezzi, perche' `LOCALS-FOR` gira in interpretazione e non c'e' nessuno
scavalco nel thread.

Tre vantaggi: **e' retrocompatibile** (senza `--` si ottiene esattamente il
comportamento di oggi, zero uscite); si legge come il commento di stack che
il programmatore scriverebbe comunque; ed e' auto-verificabile -- si puo'
controllare che il numero di nomi prima di `--` corrisponda a quanto il
corpo consuma. Unico effetto: `--` diventa un token riservato dentro la
lista dei nomi, il che e' senza conseguenze pratiche.

### 12.6 Inizializzazione: azzerati, e perche' la sezione 8 resta chiusa

Un locale di uscita non viene caricato dallo stack. Lasciarlo com'e' non e'
un'opzione: con lo shallow binding la cella conterrebbe **il valore
dell'attivazione esterna**, cioe' un risultato plausibile e sbagliato
invece di spazzatura riconoscibile -- il modo peggiore di fallire.

Va quindi legato a 0 all'ingresso, con una variante del binder che non
consuma nulla dallo stack:

```forth
: (LOC-BIND0)  ( a -- )             \ R: -- old a
    R> SWAP DUP >R  DUP @ >R  0 SWAP !  >R
;
```

Nota che questo **non riapre** la questione chiusa in sezione 8 ("niente
locali non inizializzati"): l'invariante era che ogni locale sia caricato
prima che il corpo parta, e resta vera -- semplicemente, per le uscite la
sorgente e' una costante invece dello stack. E' proprio l'invariante che
rende innocuo lo scavalco della catena da parte di `ABORT`/`THROW` (11.4).

Sull'ordine di compilazione non ci sono interferenze: `LOCALS` emette i
binding dall'indice piu' alto al piu' basso, e i binding di uscita non
consumano stack, quindi gli argomenti del chiamante continuano a essere
prelevati nell'ordine giusto qualunque sia la posizione delle uscite nella
dichiarazione.

### 12.7 Il costo, sommato

| Voce | Costo |
|---|---|
| Return stack | invariato: 4 byte per locale, uscite comprese. Valgono i tetti misurati in 11.4 |
| Thread della definizione | invariato: 3 celle per locale (`LIT`, indirizzo, binder) |
| Dizionario per scope | `+2n+2` byte (catena per scope), `-18` byte una tantum (catena condivisa che sparisce) |
| Runtime, ingresso | uguale a un locale d'ingresso |
| Runtime, uscita | `(LOC-EPOP)` = `(LOC-POP)` piu' 3 primitive |
| Word nuove | `(LOC-EPOP)`, `(LOC-BIND0)`; via `(LOC-CHAIN)`, `(LOC-EXIT)`, `LOC-ENTRY` |
| Righe di modulo | circa in pari: si perde l'aritmetica della catena, si guadagna il parsing del separatore |
| `SEE` | intatto -- il thread continua a contenere solo codice |
| Core | nessuna modifica, nessuna word ridefinita: **niente nuovo build number** |

### 12.8 Verdetto

La macchineria e' modesta e non tocca nessuno dei vincoli duri del sistema.
Ma il guadagno va misurato contro la baseline di 12.2, e si riduce a tre
cose:

1. **Garanzia su ogni via d'uscita.** Con un `EXIT` anticipato dentro un
   `IF`, oggi i risultati vanno spinti a mano in ogni punto di uscita; con
   le uscite dichiarate lo fa la catena, una volta per tutte. E' l'unico
   argomento di *correttezza*, non di stile -- e va pesato sapendo che
   **lo stile di questo repo evita l'`EXIT` a meta' definizione**,
   preferendo negare la condizione e annidare il corpo sotto `IF...THEN`.
   Su definizioni scritte cosi', questo vantaggio non si presenta mai.
2. **L'effetto di stack diventa dichiarato**, e con l'opzione 3 e'
   scritto dove il programmatore scriverebbe comunque il commento.
   Documentazione che il sistema puo' verificare, invece che un commento.
3. **Simmetria concettuale**: ingressi e uscite hanno lo stesso trattamento,
   il che rende la libreria piu' facile da insegnare (tutorial 061).

Contro: `2n+2` byte permanenti per scope, due word nuove, un token
riservato, e una superficie di errore in piu' (dichiarare un'uscita e non
assegnarla mai restituisce 0 senza che nulla lo segnali -- un difetto
speculare a quello che 3.3 chiude con le guardie, ma qui non c'e' niente
da controllare in compilazione).

**Raccomandazione (2026-08-16): non implementare adesso.** Il rapporto era
meno favorevole di quello della rientranza (sezione 11), che aggiungeva una
capacita' mancante; qui si aggiungeva zucchero sintattico sopra una
capacita' che c'era gia'. La condizione posta in 12.9 -- prima adottare la
sintassi inline -- si e' avverata con la sezione 13: **implementato**,
vedi sezione 15.

### 12.9 Rapporto con la sezione 10

Se un giorno si adotta `LOCALS{ ... }` inline, le uscite dovrebbero entrare
**nello stesso momento**, non dopo: la notazione standard-simile
`{: a b | c -- r :}` ha gia' il posto dove scriverle (dopo `--`, che nello
standard e' solo commento), il separatore serve comunque per gli
uninitialized, e il ciclo di parsing con sbirciata di `>IN` -- che e' il
grosso del lavoro di 12.5 -- lo si sta scrivendo comunque. Fatte insieme,
le uscite costano quasi nulla; fatte prima, si paga due volte il parsing.

Il "Prezzo 1" di sezione 10 (`SEE` che si rompe sullo scavalco) resta
l'unico arbitro di quella scelta, e le uscite non lo spostano di un
millimetro: nessuna delle parti nuove studiate qui mette dati dentro il
thread.

### 12.10 Se si implementa: casi da verificare

Da aggiungere a `test/LOCALS-TESTS.f`, sull'emulatore, prima di
considerarlo fatto:

| Caso | Atteso |
|---|---|
| Una sola uscita, assegnata con `TO` | valore sullo stack, `DEPTH` = 1 |
| Due uscite: ordine | dichiarata per prima piu' in basso, seconda in cima |
| Uscita mai assegnata | `0`, non il valore del chiamante -- e' il test che dimostra 12.6 |
| Uscita in posizione non finale (`A -- Q B`) | ordine corretto, ingressi consumati giusti |
| Ricorsione con uscite (`RECURSE`) | ogni livello restituisce i propri valori |
| `EXIT` anticipato dentro `IF` | uscite spinte lo stesso |
| Nessuna uscita (`--` assente) | comportamento identico a oggi, retrocompatibilita' |
| `MAXLOCALS` al limite con uscite (ingressi+uscite = 8) | ok; 9 -> `LOCALS: bad count` |
| `DEPTH` prima e dopo | coerente con l'effetto dichiarato |
| `SEE` su una word con uscite | thread leggibile, solo codice |
| `NO-LOCALS` e ricarica | pulito |

---

## 13. `{ ... }` (2026-08-17) -- implementata col trampolino

La sezione 10 aveva lasciato la decisione a `SEE`, valutando **un'unica**
strada implementativa: lo scavalco con `BRANCH`, che mette gli header dei
locali dentro il thread. `{ ... }` e' stata invece implementata per la
strada che la sezione 5 aveva scartato -- il **trampolino** -- e con essa
il Prezzo 1 cambia forma: `SEE` non stampa spazzatura, stampa poco.

### 13.1 Il vincolo, ancora quello di 2.1

Il problema non e' cambiato: `CREATE` dentro una colon-definition scrive
a `HERE`, e dentro una definizione `HERE` **e'** il thread che si sta
generando. Un locale e' un `CREATE`, quindi dichiararlo dentro la
definizione e' impossibile finche' la definizione e' aperta.

Lo scavalco aggirava il problema lasciando gli header nel thread e
saltandoci sopra. Il trampolino lo **elimina**: chiude la definizione
prima di creare i locali, e riapre il corpo dopo. Fra i due momenti
`HERE` e' fuori da qualunque definizione pendente -- l'unico stato in cui
`CREATE` e' di nuovo legittimo. Questa e' la ragione per cui la riga della
tabella di sezione 5 e' stata ripescata: l'obiezione registrata li'
(":NONAME costa 6 byte e lascia una voce fantasma; reso inutile dallo
spostamento in interpretazione") era corretta **per `LOCALS-FOR`**, dove
il trampolino non serviva a niente. Per `{ ... }` e' l'abilitatore.

### 13.2 La forma

`: FOO { A B C } corpo ;` compila **due** word:

```
FOO         ( slot ) EXIT          <- la word visibile, due celle
<anonima>   binding dei locali, poi il corpo                 <- dove sta il codice
```

- `(LOC-OPEN)` chiude la word esterna dopo uno slot (`COMPILE NOOP`,
  segnaposto innocuo se non venisse mai patchato) e un `EXIT`, e registra
  l'indirizzo dello slot in `LOC-SLOT`.
- il ciclo di parsing legge i nomi con la **sbirciata di `>IN`** gia'
  descritta in sezione 10: `>IN @ BL WORD`, confronto con `}`, e se non e'
  il terminatore si riavvolge `>IN` e si lascia che `0 CONSTANT` riparsi
  lo stesso nome. Ogni nome viene quindi letto due volte.
- `(LOC-CLOSE)` apre il corpo, ne scrive l'xt nello slot, rende visibili i
  nomi (`LOC-VOC CONTEXT !`) e compila il preambolo di binding e
  l'aggancio alla catena di ripristino di 11.2.

`LOCALS` (forma vecchia) e' stata riscritta in termini delle stesse due
word, dopo le sue guardie di 3.3: le due sintassi condividono tutto tranne
il punto in cui i nomi vengono dichiarati.

### 13.3 Il ghost word di fine riga

Il ciclo di parsing incontra il quirk noto di `BL WORD`: a fine riga non
restituisce `count = 0` ma una parola fantasma lunga 1 byte il cui unico
carattere e' `0x00`. Per questo la guardia e' doppia:

```forth
DUP C@ 0=  OVER 1+ C@ 0= OR #60 ?ERROR
```

il primo termine copre la lunghezza nulla, il secondo il fantasma. Senza
il secondo, `: OOPS { A B ;` (nessun `}` sulla riga) non darebbe `#60` ma
proseguirebbe dichiarando un locale che si chiama `0x00`.

E' la stessa ragione per cui **tutti i nomi e il `}` devono stare sulla
stessa riga del `{`**: il vincolo non e' estetico, e' che il ciclo non ha
modo di chiedere la riga successiva.

### 13.4 Cosa resta e cosa cade

- Le **guardie di 3.3** (`SCOPE-LINK`, adiacenza, freschezza di
  `#LOCALS`) restano, ma servono solo alla forma `LOCALS-FOR`. Per
  `{ ... }` l'intera classe di bug di appaiamento svanisce per
  costruzione, come la sezione 10 aveva previsto.
- Il **Prezzo 2** (collisione dei nomi `{` e `}` con i file di help di
  `<` e `>` nella mappatura FAT) e' stato risolto come nella nota
  dell'autore: grafia letterale, help condivisi.
- Il **Prezzo 1** si e' avverato nella sua forma attenuata: `SEE FOO`
  mostra lo stub, non il corpo (14.4). Non c'e' spazzatura, c'e'
  reticenza.

---

## 14. Via `:NONAME` e `SMUDGE` (2026-08-17, "LOCALS v.4")

Il trampolino di 13 usava `:NONAME` (`inc/_noname.f`) per aprire il corpo
anonimo. La v.4 lo toglie, e con esso l'ultima obiezione registrata nella
tabella di sezione 5.

### 14.1 La CFA costruita a mano

Di `:NONAME` serviva una cosa sola: un code field fatto come quello di una
colon-definition, cioe' `CALL Enter_Ptr`. `(LOC-CLOSE)` se lo scrive da
solo:

```forth
    HERE                            \ xt
    $CD C,                          \ op-code CALL
    [ ' ' >BODY CELL- @ ] LITERAL , \ indirizzo di Enter_Ptr
```

`'` e' una colon-definition (`src/F18e.f:5781`), `>BODY` e' `3 +` (CFA di
3 byte), quindi `CELL-` cade esattamente sull'operando a 16 bit della sua
`CALL`, che e' `Enter_Ptr`. Le parentesi quadre fanno tutto questo **una
volta sola**, quando si compila `(LOC-CLOSE)`; a runtime resta un `,`.

Non e' un trucco nuovo: la riga e' **identica** a quella di
`inc/_noname.f:44-45`, cioe' proprio dentro il `:NONAME` che si e' smesso
di chiamare. La fragilita' implicita -- se un giorno `'` diventasse una
word `CODE`, `>BODY CELL- @` restituirebbe spazzatura in silenzio -- non
e' introdotta qui: e' preesistente e condivisa con una word di `inc/`.
Nel repo non esiste un modo piu' diretto di esporre `Enter_Ptr`.

Guadagno: spariscono i 6 byte di heap e la voce fantasma nella catena di
`CURRENT` che la sezione 5 imputava a `:NONAME`, e cade una dipendenza
(`NEEDS :NONAME`).

### 14.2 Perche' cade anche `SMUDGE`

`:` chiama `SMUDGE` su `CREATE` per **nascondere** la word mentre la si
compila; il `SMUDGE` che stava in `(LOC-OPEN)` serviva a rivelarla subito,
perche' poi `:NONAME` spostava `LATEST` sul corpo anonimo e il `;` finale
avrebbe rivelato **quello**, non la word esterna.

Senza `:NONAME` nessuno sposta piu' `LATEST`: resta la word esterna per
tutta la compilazione, quindi e' il `;` finale a rivelarla, ed e' giusto
che `(LOC-OPEN)` non tocchi piu' niente. Le due rimozioni sono la stessa
decisione vista da due lati.

### 14.3 Conseguenza: `RECURSE` ripassa dal trampolino

`RECURSE` e' `LATEST PFA CFA ,` (`inc/recurse.f`). Con `:NONAME`, `LATEST`
era il corpo e la ricorsione lo rientrava direttamente. Ora `LATEST` e' la
word esterna, quindi **`RECURSE` compila una chiamata al trampolino**: due
`Enter_Ptr` per livello invece di uno, e `Enter_Ptr` spinge sempre l'IP sul
return stack.

Funziona (14.4), ma costa: la cella del trampolino, che nella forma
precedente si pagava una volta sola all'ingresso, ora si paga **a ogni
livello**. Vedi la nota aggiunta in 11.4.

### 14.4 Verifiche sull'emulatore (build 2026-08-17)

Su `emu/repl.py`, binari correnti. Nessuna modifica al core: **non serve
un nuovo build number**.

| Caso | Atteso | Esito |
|---|---|---|
| `NEEDS LOCALS` | carica | ok |
| `: SUM2 { Q R } Q R + ;` / `3 4 SUM2 .` | `7` | ok |
| `2 LOCALS-FOR SUM2B U V` / `: SUM2B LOCALS U V + ;` / `30 40 SUM2B .` | `70` | ok |
| `111 3 4 SUM2 . .` (argomenti consumati, sotto intatto) | `7 111` | ok |
| `: FCT { N } N 1 > IF N 1- RECURSE N * ELSE 1 THEN ;` / `7 FCT .` | `5040` | ok |
| `333 5 FCT . .` | `120 333` | ok |
| `: SQ2 { N } N N * ;` / `5 SQ2 .` | `25` | ok |
| `SEE SQ2` | stub | mostra una cella senza nome (l'xt del corpo anonimo, stampato come spazzatura) e `EXIT` |

**`test/LOCALS-TESTS.f` non e' eseguibile sull'emulatore**, e non per
colpa di LOCALS: un `NEEDS` annidato dentro un file gia' `INCLUDE`d
termina in silenzio il file esterno. Ridotto al minimo:

```forth
CR .( START ) CR
NEEDS RECURSE
CR .( AFTER-NEEDS ) CR
```

stampa `START`, carica, e `AFTER-NEEDS` non compare mai. Colpisce tutte le
suite di `test/`, che iniziano tutte con un blocco di `NEEDS`. La suite va
quindi fatta girare su CSpect o su macchina vera; sull'emulatore si
possono solo precaricare le dipendenze al prompt.

### 14.5 Punti aperti

**Un `{` malformato lascia una word orfana e invisibile.** `{` chiama
`(LOC-OPEN)` **prima** del ciclo di parsing. Se il ciclo solleva `#57` o
`#60` -- casi documentati e attesi, per esempio `: OOPS { A B ;` -- si
finisce in `ERROR` -> `QUIT`, che non tocca il bit di smudge e non fa mai
eseguire il `;`. La word esterna resta nel dizionario **nascosta**, non
piu' raggiungibile da `'`, `-FIND` o `FORGET`. Prima della v.4 sopravviveva
come `NOOP EXIT` cercabile: e' una piccola regressione, e rende falso il
commento in coda a `lib/LOCALS.f` ("the error is raised after `(LOC-OPEN)`
has already revealed it"). Rimedio: rimettere un `SMUDGE` in `(LOC-OPEN)`
-- ora innocuo, perche' `LATEST` non si sposta piu' -- oppure smudgiare
esplicitamente nei rami d'errore di `{`.

**La guardia su `MAXLOCALS` in `{` scatta un nome troppo tardi.** Il ciclo
fa `(LOC-MAKE)` e **poi** `#LOCALS @ MAXLOCALS > #57 ?ERROR`, mentre
`(LOC-MAKE)` scrive in `LOCAL-PFAS` all'indice `#LOCALS @` prima di
incrementarlo. Col nono nome l'indice e' 8 e `LOCAL-PFAS` ha 8 celle: la
scrittura cade **una cella oltre l'array**, cioe' sul code field della
definizione che segue, prima che l'errore venga sollevato. `LOCALS-FOR`
non ha il problema perche' controlla il conteggio *prima* del ciclo.
Rimedio: spostare la guardia sopra `(LOC-MAKE)`, come
`#LOCALS @ MAXLOCALS = #57 ?ERROR`. Da verificare sull'emulatore col caso
`: OOPS { 9 nomi } ;` gia' elencato in `test/LOCALS-TESTS.f`.

---

## 15. Locali in uscita, implementati (2026-08-18)

Chiude lo studio di sezione 12: la condizione posta in 12.9 (prima la
sintassi inline, poi le uscite "quasi gratis" sopra di essa) si e'
avverata con la sezione 13, quindi le uscite sono state implementate
sopra `{ ... }`, con l'opzione 3 di 12.5 (separatore `--` nella lista) e
il legame a 0 di 12.6, esattamente come studiati. Corretto insieme anche
il bug di scrittura oltre `LOCAL-PFAS` di 14.5 (secondo punto), toccando
comunque il ramo che chiama `(LOC-MAKE)`; il primo punto di 14.5 (word
orfana su dichiarazione malformata) resta aperto, non toccato qui.

### 15.1 Sintassi

```forth
: SUM3    { X Y Z }        X Y + Z + ;
: SUM-TO  { N -- ACC }     N 0> IF  N 0 DO  ACC I 1+ + TO ACC  LOOP  THEN ;
: SPLIT   { N -- LO HI }   N 10 MOD TO LO  N 10 / TO HI ;
```

I nomi dopo `--` non vengono caricati dallo stack (12.6: legati a 0
all'ingresso) e **non vanno referenziati a fine corpo**: ogni via
d'uscita -- il `;` finale e un `EXIT` anticipato dentro `IF` -- li spinge
da sola, nell'ordine di dichiarazione (il primo dichiarato finisce piu'
in basso), prima di ripristinare le celle del chiamante sotto di essi.
E' la differenza reale rispetto alla baseline di 12.2 (`... Q R ;` scritto
a mano): qui la garanzia vale su **ogni** punto di uscita, non solo su
quello dove il programmatore ha ricordato di scriverla.

### 15.2 La catena per scope (12.4, come previsto)

`(LOC-CLOSE)` ora scrive **due** cose in sequenza, non una: prima la
catena di ripristino di *questo* scope (`#LOCALS` celle, una per locale,
piu' `EXIT`), poi -- come prima -- il CFA a mano e il corpo. La catena
condivisa (`(LOC-CHAIN)`, `CREATE (LOC-EXIT)`, `LOC-ENTRY`) e' sparita:
`(LOC-STEP)` decide passo per passo se compilare `(LOC-POP)` (ripristina
soltanto) o `(LOC-EPOP)` (spinge, poi ripristina), guardando `#IN-LOCALS`
-- la stessa variabile che gia' separava input da output nel ciclo di
bind. Nessuna word nuova per la sintassi: `{` non e' cambiata da 13/14,
solo `(LOC-CLOSE)` e le word di supporto.

`(LOC-BIND0)` lega un output a 0 (12.6); `(LOC-EPOP)` spinge il valore
corrente e poi ripristina quello del chiamante, nella stessa word (12.3:
lettura e ripristino devono stare insieme). La formulazione usata e'
quella gia' scritta in 12.3 (`R> R> R> DUP @ ROT ROT ! SWAP >R`),
ritracciata a mano qui perche' vale la pena fidarsi solo dopo averla
verificata di persona.

### 15.3 Due bug reali trovati implementando, non solo sulla carta

Il design di sezione 12 era corretto nella sostanza, ma **due errori di
implementazione**, non di design, hanno rotto la prima stesura -- vale la
pena registrarli perche' nessuno dei due si vede rileggendo il codice in
fretta.

**Bug 1 -- `'` al posto di `[']` dentro una definizione compilata.**
`(LOC-CLOSE)` chiudeva la catena con `' EXIT ,`. Questo idioma e' corretto
**solo interpretando** (e' esattamente come `CREATE (LOC-EXIT) ' (LOC-POP)
... ' EXIT ,` lo usava, a livello di file, prima di questa sezione): li'
`'` esegue subito e consuma "EXIT" dal testo sorgente che si sta
caricando. Dentro una definizione compilata `'` **non e' immediate**: la
parola dopo di essa nel sorgente di `(LOC-CLOSE)` non viene affatto
consumata da `'` a compile-time, ma compilata normalmente nel thread di
`(LOC-CLOSE)` **come se fosse codice** -- qui, un `EXIT` letterale, che fa
uscire `(LOC-CLOSE)` a meta'. La chiamata di `'` cade quindi a runtime,
quando (LOC-CLOSE) gira per davvero: legge il prossimo token dal flusso di
input **del chiamante** (in `: T2 LOCALS X ;`, il token e' `X`), lo cerca
-- fallisce, perche' `CONTEXT` non e' ancora stato spostato su
`DEFLOCALS` -- e da' "X? is undefined.", silenziosamente, senza mai
arrivare al resto di `(LOC-CLOSE)`. Il rimedio e' `['] EXIT ,`, lo stesso
idioma gia' corretto usato in `(LOC-STEP)` per `(LOC-POP)`/`(LOC-EPOP)`.
Diagnosticato piazzando marcatori numerici (`1111 . CR` ... `2222 . CR`)
attorno al sospetto: `2222` non compariva mai, isolando il guasto esatto.

**Bug 2 -- l'ordine di bind non e' piu' "l'inverso della dichiarazione"
quando si spezza in due cicli.** La prima stesura legava tutti gli input
in un ciclo (ultimo dichiarato per primo, correttamente) e poi tutti gli
output in un secondo ciclo (in ordine di posizione). Ma la catena si
aspetta che il passo `j` corrisponda alla posizione dichiarata `j` (12.3)
**solo se** l'ordine cronologico dei bind e' l'esatto inverso dell'ordine
della catena -- e con due cicli separati, tutti gli input finiscono
cronologicamente *dopo* tutti gli output (o viceversa), indipendentemente
dalle loro posizioni dichiarate: la corrispondenza si rompe ogni volta che
uno scope mescola i due tipi. Sintomo: non un crash, un valore sbagliato
(`T{ 47 B-SPLIT -> 7 4 }T` dava "Incorrect result."). Rimedio: **un solo
ciclo** `#LOCALS @ 0 DO ... LOOP`, con `I LOC-POS` (nuova word, `#LOCALS @
1- SWAP -`) a mappare il contatore ascendente del `DO` sulla posizione
dichiarata discendente, e con `LOC-BIND` o `LOC-BIND0` scelti posizione
per posizione in base a `#IN-LOCALS`. Uniforma i due casi (solo input,
misto) nello stesso codice, ed e' *piu' corto* della versione a due cicli.

### 15.4 Costo, confrontato con la stima di 12.7

| Voce | Stimato in 12.7 | Osservato |
|---|---|---|
| Dizionario per scope | `+2n+2` byte | `n+1` celle per la catena (2 byte l'una): stesso ordine di grandezza |
| Word nuove | `(LOC-EPOP)`, `(LOC-BIND0)` | uguale, piu' `(LOC-STEP)` e `LOC-POS` come selettori |
| Runtime, uscita | `(LOC-EPOP)` = `(LOC-POP)` + 3 primitive | confermato dal confronto diretto dei due corpi |
| `SEE` | intatto | invariato rispetto a 14 (mostra lo stub, non il corpo -- 14.4 vale ancora) |
| Core | nessuna modifica | confermato: nessun nuovo build number |

### 15.5 Verifica sull'emulatore

Tutto su `emu/repl.py`, binari correnti (build 2026-08-17). Nessuna
modifica al core. La suite `test/LOCALS-TESTS.f` gira precaricando le
`NEEDS` al prompt prima di `INCLUDE`, aggirando il limite gia' registrato
in 14.4 (NEEDS annidato dentro un file INCLUDEd).

| Caso | Atteso | Esito |
|---|---|---|
| `test/LOCALS-TESTS.f` intera (input-only + le nuove uscite, ~30 asserzioni) | silenzio | passa |
| `: SUM-TO { N -- ACC } ...` / `5 SUM-TO` / `0 SUM-TO` | `15` / `0` | ok |
| `: RESET { F -- V } F IF 99 TO V THEN ;` / `-1 RESET` / `0 RESET` | `99` / `0` -- V non assegnato resta 0, non il valore del chiamante (12.6) | ok |
| `: SPLIT { N -- LO HI } ...` / `47 SPLIT . .` | `4 7` (HI in cima, LO sotto) | ok |
| `: RFACT { N -- ACC } ... RECURSE ...` / `5 RFACT` | `120` -- ogni livello ricorsivo restituisce il proprio valore | ok |
| `{ A B C D E F G -- H }` (7 input + 1 output = 8, limite MAXLOCALS) | `28` | ok |
| `{ 9 nomi }` (nessun `--`) | errore pulito, nessuna corruzione | `I? LOCALS: bad count.` |
| `{ A -- B -- C }` (`--` duplicato) | errore pulito | `--? LOCALS: misplaced { or }.` |
| `1 2 3 SUM3` dopo i due errori sopra | `6` -- il dizionario non e' corrotto | ok |

Il caso `SPLIT` e' quello che verifica l'ordine delle uscite multiple
(12.10: "due uscite: dichiarata per prima piu' in basso, seconda in
cima") ed e' anche il caso che ha rivelato il Bug 2 di 15.3.

---

## 16. BRANCH di scavalco al posto del trampolino (2026-08-19)

Il trampolino (13-14) evitava la trappola di 2.1 (`CREATE` dentro una
colon-definition spezza il thread) chiudendo FOO su due sole celle
(`slot` + `EXIT`) e costruendo i local, la catena e il corpo vero in un
**secondo** thread anonimo, agganciato via CFA scritta a mano. Costava
un'indirezione in piu' a ogni chiamata (11.4) e la ricorsione pagava
quell'indirezione **a ogni livello** (14.3), non solo una volta.

Questa sezione sostituisce quel meccanismo con l'alternativa che la
sezione 5 aveva scartato per un'altra ragione (rompere `SEE`): un
**BRANCH di scavalco**, lo stesso idioma a riferimento in avanti che
usano `IF`/`THEN` (`COMPILE 0BRANCH HERE 0 ,` / `HERE OVER - SWAP !`),
sempre preso. FOO non viene mai chiusa: il `:` originale resta aperto per
tutta `{ ... }`, e torna a esserci **un solo thread**, non due.

### 16.1 Il design

```
(LOC-OPEN)   COMPILE BRANCH   HERE 0 ,   LOC-SLOT !
             \ FOO resta aperta. LOC-SLOT e' l'indirizzo della cella
             \ offset, non ancora risolta.

             \ { (o LOCALS-FOR/LOCALS) crea qui gli header dei local,
             \ come sempre -- ma ora dentro il thread ancora aperto di
             \ FOO: e' la trappola di 2.1, deliberatamente non evitata.

(LOC-CLOSE)  compila la catena di ripristino di questo scope (come in
             15.2, invariata)
             LOC-VOC CONTEXT !                    \ i nomi diventano visibili
             HERE LOC-SLOT @ - LOC-SLOT @ !        \ <-- il BRANCH atterra QUI
             compila il preambolo di binding (come in 15.2, invariato)
             ]                                     \ riafferma STATE compiling
             0 #LOCALS !
```

Il punto delicato e' **dove** atterra il BRANCH. Non puo' essere ne'
l'inizio della catena di ripristino ne' l'inizio del corpo utente:

- **Non l'inizio della catena.** La catena (`(LOC-POP)`/`(LOC-EPOP)` a
  ripetizione + `EXIT`) non viene mai raggiunta per caduta -- solo di
  traverso, quando l'`EXIT` del corpo trova il suo indirizzo in cima al
  return stack (messo li' dal preambolo con `>R`, sezione 11.2). Se il
  BRANCH atterrasse li', chiamare FOO eseguirebbe subito `(LOC-POP)` con
  un return stack che non contiene ancora niente da ripristinare --
  corruzione immediata.
- **Non l'inizio del corpo utente.** Salterebbe il preambolo di binding:
  i local non verrebbero mai caricati dallo stack del chiamante.

Il bersaglio giusto e' quindi **l'inizio del preambolo di binding**, cioe'
`HERE` subito dopo aver compilato la catena e prima di compilare il
preambolo -- non "come ultima operazione di `(LOC-CLOSE)`" in senso
letterale (quella sarebbe dopo il preambolo, il bersaglio sbagliato). La
formulazione iniziale data a voce ("patcha l'offset come ultima
operazione") andava quindi letta come "ultima operazione **prima del
preambolo**", non come l'ultima riga della word -- un'imprecisione
verbale simile a quella di 16.2 sotto.

### 16.2 `]`, non `[`

La prima formulazione a voce del passo finale diceva `[COMPILE] [`
("lascia aperta la compilazione"). Tracciato meccanicamente: `[` fa
`0 STATE !` -- passa a interpretazione, l'opposto dell'obiettivo
dichiarato. Corretto durante la discussione: la parola giusta e' `]`
(`192 STATE !`, la costante di compilazione), usata via `[COMPILE]`
esattamente come '`;`' stessa la usa in coda alla propria definizione
(`src/F18e.f:2971-2977`) -- necessario perche' `]`, se scritta bare
dentro `(LOC-CLOSE)`, verrebbe eseguita **quando `(LOC-CLOSE)` stessa
viene compilata** (al caricamento di `lib/LOCALS.f`) invece che quando
gira, essendo pero' `]` non-immediate questo non e' in realta' un
problema qui: si e' scelto comunque `]` bare (non `[COMPILE] ]`) per
semplicita', equivalente.

In pratica `]` qui e' un'asserzione difensiva, non una correzione: niente
fra `(LOC-OPEN)` e questo punto tocca `STATE` (`CREATE`/`CONSTANT` non lo
sfiorano), quindi resterebbe comunque a "compiling". Vale la pena
scriverla lo stesso, a beneficio di chi rilegge il codice: il `:` di FOO
e' ancora aperto, e le parole del corpo utente che seguono devono essere
**compilate**, non solo date per scontate.

**Nota per il futuro**: l'autore stesso ha segnalato di invertire talvolta
i concetti in mente quando detta un meccanismo preciso (qui, quale delle
due parole simmetriche `[`/`]` intendeva). Vale la pena tracciare la
conseguenza concreta di ogni istruzione del genere e confrontarla con
l'obiettivo dichiarato nella stessa frase, prima di implementare.

### 16.3 Cosa cade, cosa cambia

- Spariscono la CFA costruita a mano (14.1) e la `!CSP` di re-armo
  (13.2): non c'e' piu' un secondo corpo da chiudere separatamente, quindi
  il `CSP` salvato dal `:` originale di FOO resta quello giusto per il
  `;` finale dell'utente.
- `RECURSE` (compila ancora `LATEST PFA CFA ,`, invariato) rientra ora
  attraverso lo **stesso** BRANCH, con un solo salto Z80 (`JR`, nessun
  push sul return stack) invece di passare per una seconda `Enter_Ptr`:
  il costo aggiuntivo per livello di ricorsione descritto in 14.3/11.4
  (la nota "+1 cella per livello") **decade** -- non ancora rimisurato
  sui binari, ma il meccanismo che lo causava (due `Enter_Ptr` per
  livello) non c'e' piu'.
- Il "KNOWN ISSUE" di 14.5 (parola orfana e invisibile su `{` malformato)
  resta tale e quale: `(LOC-OPEN)` non smudga, `QUIT` non arriva mai alla
  `;` che lo farebbe. Non toccato da questa sezione.

### 16.4 Prezzo aggravato: `SEE`

Il "Prezzo 1" della sezione 10 torna, ma peggiore. Con lo scavalco
originale (mai implementato) la spazzatura veniva **stampata** fino a
fine definizione senza pero' bloccare il prompt. Qui, provato
sull'emulatore (`SEE` su una word con locali dopo `NEEDS SEE`), il
decompilatore ha stampato l'intestazione, poi `BRANCH 31`, poi si e'
bloccato: nessun ritorno al prompt in diversi minuti di esecuzione
reale (non un timeout di script -- il processo dell'emulatore restava
attivo, a consumare istruzioni). Non e' stato accertato se sia un loop
Forth-level genuinamente infinito o solo molto piu' lento del tetto
`STEP_CAP` di `emu/repl.py` (60 milioni di istruzioni) -- in entrambi i
casi, in pratica: **non usare `SEE` su una word con locali**. Rimandato
per esplicita richiesta dell'autore ("Tralasciamo per ora... risolveremo
questa regressione piu' avanti"), non ancora affrontato.

### 16.5 Verifica sull'emulatore (build 2026-08-17, core invariato)

Nessuna modifica al core: **non serve un nuovo build number**. Tutti i
casi gia' verificati in 14.4/15.5 ri-controllati con il nuovo meccanismo:

| Caso | Atteso | Esito |
|---|---|---|
| `test/LOCALS-TESTS.f` intera (precaricando le `NEEDS`, limite 14.4) | silenzio | passa |
| `1 2 3 SUM3` (`{ X Y Z }`) | `6` | ok |
| `5 SQ2` (`{ N }`) | `25` | ok |
| `7 9 NEST` (annidamento: chiama `SQ` due volte) | `130` | ok |
| `1 2 3 4 5 6 7 8 L8` (8 local, limite `MAXLOCALS`) | `36` | ok |
| `7 FCT` ricorsiva (`RECURSE`) | `5040` | ok |
| `0 EARLY` / `7 EARLY` (`EXIT` anticipato dentro `IF`) | `999` / `70` | ok |
| `111 1 2 3 SUM3 . .` (sotto pila intatto) | `6 111` | ok |
| `5 SUM-TO` (uscita, sezione 15) | `15` | ok |
| `47 SPLIT . .` (due uscite, ordine) | `4 7` | ok |
| `: OOPS { A B ;` (manca `}`) | errore pulito | `LOCALS: misplaced { or }.` |
| `: BAD9 { 9 nomi senza -- }` | errore pulito, guardia prima della scrittura (14.5) | `I? LOCALS: bad count.` |
| `1 2 3 SUM3` dopo i due errori sopra | `6` -- dizionario non corrotto | ok |
| `SEE` su una word con locali | -- | non torna al prompt (16.4); **non testare in script automatici** |

---

## 17. Fix di `SEE` -- ESPLORATO, NON ANCORA IMPLEMENTATO (2026-08-19)

Sezione di sola analisi: descrive un fix concreto per la regressione di 16.4, misurato
e verificato solo a livello di indirizzi/aritmetica, **non scritto in `lib/see.f`**.

### 17.1 Perche' non basta un byte di riempimento

Ipotesi discussa e scartata: siccome `0 CONSTANT <nome>` occupa **7 byte** in origin
space **sempre**, indipendentemente dalla lunghezza del nome (misurato:
`HERE 0 CONSTANT Z1 HERE SWAP -` -> `7`, uguale con nomi da 1 a 8 caratteri -- coerente
con `CODE`/`CREATE`, `L1.asm:1554-1610`: NFA/LFA/XFA vengono scritti nell'heap e poi
tolti da origin space con un `ALLOT` negativo, lasciando li' solo un mirror-ptr fisso +
la `CALL` patchata + la PFA + il codice macchina di `;CODE`), la parita' dello splice
totale dipende dalla parita' del numero di local (7 e' dispari). Un solo byte di
riempimento, condizionale al conteggio dispari, pareggerebbe la lunghezza totale.

**Misurato e scartato.** Su `SQZ  { U V }  U V + ;` (2 local, quindi gia' "pari" per
questa teoria, nessun riempimento richiesto):

| Punto | Indirizzo | Offset da PFA |
|---|---|---|
| PFA | `$853E` | 0 |
| cella offset del BRANCH | `$8540` | +2 |
| `LOC-CHAIN-START` | `$8550` | +18 |
| bersaglio patchato del BRANCH | `$8556` | +24 |
| `HERE` dopo il `;` reale (con l'`EXIT` vero) | `$8570` | +48 |

Tutti pari, esattamente come previsto -- eppure `SEE SQZ` si e' comunque bloccato per
diversi minuti. La teoria della parita' e' corretta ma **non e' la causa del blocco**:
un riempitivo (per-local o singolo condizionale) non lo risolve.

### 17.2 La causa piu' probabile

`DELOAD` (`lib/see.f:91-106`) avanza sempre di un multiplo di 2 byte da PFA (mai 1: il
suo loop fa `CELL+` a ogni giro, e i casi a 2 celle come `BRANCH`/`LIT`/`(?DO)` -- via
`DEB-B`/`DEB-L`, righe 43-45 -- consumano una cella extra, cioe' *un altro* multiplo di
2). L'allineamento a byte quindi non si rompe mai in senso stretto. Il problema e'
un altro: `(DELOAD)` (righe 72-88) confronta ogni cella con un pugno di xt noti
(`BRANCH`, `0BRANCH`, `LIT`, `(?DO)`, `(+LOOP)`, `(LOOP)`, `(LEAVE)`, `(.")`, `(H")`,
`COMPILE`). Se una cella-spazzatura dentro lo splice (header dei local, poi la catena
di ripristino) **coincide per caso numerico** con uno di questi xt, `DELOAD` crede sia
un'istruzione a 2 celle e salta una cella IN PIU' -- che puo' essere proprio quella in
cui si trova un `EXIT` vero: sia quello interno della catena (`['] EXIT ,` in coda,
sezione 15.2), sia quello reale a fine definizione. Scavalcato quello, `DELOAD`
continua a decodificare memoria non correlata, senza piu' incontrare per caso nessuno
dei cinque terminatori (`ABORT`/`QUIT`/`EXIT`/`WARM`/`(;CODE)`, righe 98-102) --
da cui il blocco osservato, non spiegabile dalla sola parita' della lunghezza.

Non e' stato individuato a byte singolo *quale* cella causi il match (richiederebbe
`NEEDS DUMP` e un confronto manuale byte-per-byte); non necessario per il fix proposto
sotto, che aggira il problema invece di correggerne la causa puntuale.

### 17.3 Il fix: riconoscere BRANCH come prima cella

Osservazione dell'autore, verificata: **nessun'altra semantica del sistema compila un
`BRANCH` come prima cella di una colon-definition.** `BRANCH` viene compilato solo da
`ELSE` e `AGAIN` (`src/F18e.f:481-483`), e in entrambi i casi sempre a meta' di una
definizione, mai come primissima cella -- un `: FOO ELSE ...` o `: FOO AGAIN ...` non ha
senso strutturalmente (`ELSE` richiede un `IF` gia' aperto, `AGAIN` un `BEGIN`) e non
compila comunque `BRANCH` per primo. Il pattern "`PFA @ = BRANCH`" e' quindi una firma
univoca e affidabile di uno scope creato da `{` o dalla vecchia `LOCALS`, che sono
oggi l'**unico** produttore di questa forma (entrambe passano da `(LOC-OPEN)`).

Invece di sperare che la decodifica cella-per-cella si riallinei da sola per caso,
`SEE` puo' **riconoscere il pattern esplicitamente** e saltare l'intero splice (header
dei local + catena di ripristino) in un colpo solo, andando dritto al bersaglio che
`(LOC-CLOSE)` ha gia' calcolato e scritto nella cella offset -- lo stesso valore che
la CPU userebbe a runtime, letto pero' a freddo da `SEE`:

```forth
\ pfa e' l'indirizzo della cella del BRANCH stesso (non ancora avanzato)
: LOC-SKIP  ( pfa -- target )
    CELL+  DUP @ +          \ (indirizzo cella offset) + (valore li' patchato)
;
```

Formula verificata in questa sessione: `LOC-SLOT @ DUP @ +` ha dato `34134` ($8556),
combaciando in modo indipendente con tutte le altre misure di 17.1 (differenza di 24
byte da PFA, coerente col preambolo di binding calcolato a mano).

Il punto di innesto e' `(SEE)` (righe 109-125), **non** il `CASE` generico di
`(DELOAD)`: quel `CASE` gestisce gia' correttamente un `BRANCH` che compare a meta' di
una definizione normale (da `ELSE`/`AGAIN`), e deve continuare a farlo -- solo un
`BRANCH` che e' **la primissima cella** deve essere trattato diversamente:

```forth
: (SEE)  ( xt -- )
    BASE @
    SWAP HEX
    >BODY
    DUP DEB-NFA
    DUP DEB-LFA
    DUP DEB-CFA
    DUP CFA @ ['] : @ =
    IF
        SWAP BASE !
        DUP @ ['] BRANCH =  IF  LOC-SKIP  THEN   \ <-- nuovo: salta lo splice
        DELOAD
        DROP
    ELSE
        HEX DEB-PFA
        BASE !
    THEN
;
```

Non tocca `lib/LOCALS.f`: `BRANCH` e' gia' una word core, quindi il controllo e'
innocuo anche quando `LOCALS` non e' caricato (nessuna word normale comincia con
`BRANCH`, quindi il ramo non scatta mai per definizioni ordinarie). Nessun accoppiamento
nuovo fra i due moduli da gestire con `NEEDS`.

### 17.4 Cosa il fix NON risolve (deliberatamente)

- **Lo splice non diventa leggibile.** `SEE` smetterebbe di bloccarsi e di stampare
  spazzatura, ma non mostrerebbe nemmeno i nomi dei local ne' la catena -- li salta e
  basta, mostrando solo il preambolo di binding (celle `LIT`/`(LOC-BIND)`/`(LOC-BIND0)`
  grezze, non "belle") seguito dal corpo utente vero e dall'`EXIT` reale. Coerente con
  quanto gia' accettato all'inizio di questa indagine: l'obiettivo e' il resync, non la
  decodifica corretta dello splice.
- **La firma non e' una garanzia assoluta.** E' vera per tutto cio' che il repository
  compila oggi, ma un utente potrebbe in teoria scrivere a mano
  `: FOO COMPILE BRANCH HERE 0 , ... ;` fuori da `LOCALS` (via `ASSEMBLER`/trucchi di
  compilazione diretta) e ottenere un falso positivo. Rischio giudicato accettabile:
  nessun costrutto del repository lo fa oggi.
- **Non copre un'eventuale futura fusione dei due thread** (l'opzione "tutto in un solo
  thread" scartata nella prima domanda di chiarimento di questa sessione, sezione 16):
  se in futuro lo scavalco venisse eliminato del tutto (nessuna word con locali
  producesse piu' questo pattern), il controllo diventerebbe silenziosamente morto --
  innocuo, ma da ricordare in un'eventuale pulizia.

### 17.5 Verifica da fare quando si implementa

Nessuna eseguita ora (solo aritmetica a freddo sugli indirizzi). Prima di considerarlo
fatto, sull'emulatore:

| Caso | Atteso |
|---|---|
| `SEE SQZ` (2 local, ex-bloccante) | termina, mostra preambolo + corpo + `EXIT`, torna al prompt |
| `SEE SUM3` (3 local, ex-bloccante) | idem |
| `SEE L8` (8 local, limite `MAXLOCALS`) | idem |
| `SEE SUM-TO` / `SEE SPLIT` (output locals, catena mista POP/EPOP) | idem |
| `SEE FCT` (ricorsiva, `RECURSE` rientra dallo stesso `BRANCH`) | idem, `RECURSE` visibile nel corpo decodificato |
| `SEE` su una word ordinaria con `ELSE`/`AGAIN` a meta' definizione (es. una gia' in `inc/`) | **invariato**: nessuna regressione sul `CASE` generico di `(DELOAD)` |
| `SEE` su una word senza locali che comincia comunque con `IF`/`0BRANCH` (mai con `BRANCH` puro) | **invariato** |
