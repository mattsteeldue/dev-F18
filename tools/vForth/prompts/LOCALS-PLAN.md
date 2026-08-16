# LOCALS in vForth -- design consolidato

Stato: **implementato** in `lib/LOCALS.f`, verificato sull'emulatore
headless (`emu/repl.py`). Vedi sezione 9.
Ultima revisione: 2026-08-16 -- **i locali sono ora rientranti**, vedi
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
| Trampolino **`NOOP`+`EXIT`** + corpo `:NONAME` (stile `inc/defer.f`) | Funziona, ma `:NONAME` (`inc/_noname.f`) costa 6 byte di heap e **si aggancia alla catena di `CURRENT`** come voce fantasma; e il preambolo separato e' piu' grande e piu' lento degli store inline. Reso inutile dallo spostamento in interpretazione. |
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

### 11.4 Il prezzo, misurato

**Return stack.** `4+4n` byte per attivazione oltre all'indirizzo di
ritorno, su 160 byte condivisi col TIB (2.5). Misurato sull'emulatore con
`FIB` a 1 locale: `15 FIB` passa, `20 FIB` sfonda il buffer di input e
corrompe il dizionario **senza messaggio d'errore**. Regola pratica:
~15 livelli con 1 locale, ~6 con 4, ~3 con 8.

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
