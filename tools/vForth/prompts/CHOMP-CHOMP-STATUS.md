# chomp-chomp: stato della revisione (agg. 2026-08-24, sessione 6)

Nota di ripresa per continuare il lavoro da un'altra sessione.
Piano approvato completo: `C:\Users\matteo\.claude\plans\glowing-mixing-haven.md`
(4 stadi: AI+pacing, colori ciclici, font in RAM, labirinti su Screen).

## Dove siamo

**Stadio 1 (AI dei fantasmi + pacing) — completo, confermato su CSpect.**
**Stadio 2 (colori ciclici) — completo, confermato su CSpect.**
**Stadio 3 — completo, CONFERMATO su CSpect 2026-08-23, sia
l'Approccio A (font, poi abbandonato) sia l'Approccio B (UDG esteso,
quello adottato) sia lo standalone via `ZAP`.** L'obiettivo originale
del piano (font in RAM via CHARS/`rst $10`) e' stato tentato, fatto
funzionare, poi **abbandonato e sostituito** da un approccio piu'
semplice: estendere gli UDG oltre la lettera `U` invece di introdurre
un font separato. L'Approccio B e' stato provato a schermo su CSpect:
funziona. **`ZAP GAME` provato e funzionante**: trovata e corretta al
volo una `NEEDS [']` mancante in `lib/ZAP.f` (bug pre-esistente, non
introdotto da questa sessione), poi i tre `.bin` standalone rigenerati
con successo e lanciati direttamente via `demo/chomp-chomp/game.bas`
(bypassando `INCLUDE demo/chomp-chomp.f`) -- confermato funzionante.
Vedi la sezione dedicata piu' sotto per la cronologia completa dello
Stadio 3 (perche' si e' tentato il font, cosa e' andato storto, perche'
si e' tornati sugli UDG).

**Stadio 4 (labirinti su Screen) — completo, verificato headless.**
Prima fetta 2026-08-23 (sessione 5): infrastruttura di caricamento,
contatore di livello, `MAZE-CHECK`, e il labirinto attuale convertito
come primo labirinto su disco (livello 1). Seconda fetta 2026-08-24
(sessione 6): **due tracciati nuovi** (Screen 742/743 e 744/745), il
15-esimo glifo muro `W` che mancava all'alfabeto, il conteggio dei
punti reso dinamico (era 180 fisso: un soft-lock silenzioso per
qualunque labirinto disegnato diverso) e `util/chomp-maze.py`, che
disegna e verifica un tracciato dall'host. Manca solo la conferma a
schermo su CSpect -- vedi la sezione dedicata piu' sotto.

Branch: `chomp-chomp-ghost-ai`.

| Commit | Contenuto |
|---|---|
| `44f1fc9` | Stadio 1: personalita' dei fantasmi, pacer esplicito |
| `a7a1fbf` | Suite di test dell'AI, tutta verde |
| `a9efc32` | Stadio 2: `COLORS:`, `SCARED-FLASH`, `FRUIT-CYCLE`, `PILL-FLASH`,
  fix stack leak in `ghost-catch`, fix colore `inter-hunt`; **confermato su
  CSpect**. E' anche la baseline "pre-font" a cui e' stato fatto risalire
  lo Stadio 3 (vedi sotto) -- byte-identica alla copia dell'autore
  `version/20260820/demo/chomp-chomp-1.f`. |
| `544c8e0` | Housekeeping: rinominata la copia pre-revisione in
  `demo/chomp-chomp/chomp-chomp-0.f`; bozza post Discord. Nessun cambio al
  gioco. |
| `f2ca210` | Stadio 3: UDG esteso invece del font in RAM. |
| `4bf3f16` | Stadio 4 prima fetta: infrastruttura labirinti su Screen,
  `MAZE-CHECK`, labirinto attuale convertito come livello 1 su Screen
  740/741. |
| *(non ancora committato -- l'autore usa GitHub Desktop, non la CLI)* |
  Stadio 4 seconda fetta: glifo `W`, punti dinamici, labirinti 2 e 3 su
  Screen 742-745, `util/chomp-maze.py`. |

| File | Stato |
|---|---|
| `demo/chomp-chomp.f` | Stadio 1+2+3 completi, **confermati su CSpect**
  (schermo, non solo compilazione). Stadio 3 nella sua forma finale:
  `UDGize` (rimessa) converte A-U *e* `.` (nuovo 22-esimo slot UDG,
  lettera `V`) a tempo di `maze-copy`; nessun font personalizzato,
  nessuna lettura di "ROM" a runtime. Banner `.( Chomp.f - X )` ->
  `.( X )` (richiesta cosmetica dell'autore, 11 occorrenze). Stadio 4
  prima fetta aggiunta 2026-08-23 (sessione 5): `MAZE-SCR0`/`n-mazes`/
  `level`, `maze-blk0`/`raw-row!`/`maze-line`/`load-maze-row`/
  `load-maze`, `set-maze-run` ridefinita, `MAZE-CHECK` -- **verificato
  headless** (compilazione pulita + `test/CHOMP-MAZE-TESTS.f` tutto
  verde), **non ancora confermato a schermo su CSpect**. |
| `demo/chomp-chomp/chomp-chomp.f` | **Ricopiato 2026-08-24** (sessione
  6) dal master, verificato byte-identico (`diff` + `md5sum`); include
  entrambe le fette dello Stadio 4. |
| `demo/chomp-chomp/game-core.bin` / `game-heap.bin` / `game-user.bin` | Rigenerati
  con `ZAP GAME` per lo Stadio 3 (fix `lib/ZAP.f`, confermati standalone
  via `game.bas`). **Ora superati dallo Stadio 4**: `demo/chomp-chomp.f`
  e' cambiato da allora, vanno rigenerati di nuovo dall'autore con
  `ZAP GAME` da una sessione vForth viva quando comodo (non farlo
  headless: richiede una sessione vForth interattiva). |
| `lib/ZAP.f` | **Bug pre-esistente trovato e corretto dall'autore
  2026-08-23**: mancava `NEEDS [']` dopo `MARKER TASK` -- una sessione
  vForth pulita che caricava `ZAP` senza gia' avere `[']` in dizionario
  falliva. Non e' un regressione di questa sessione; scoperto solo ora
  perche' `ZAP GAME` non era mai stato riprovato dallo Stadio 3. |
| `test/CHOMP-AI-TESTS.f` | ~45 asserzioni, tutte verdi (verificato sessione 2) |
| `test/CHOMP-MAZE-TESTS.f` | **NUOVO 2026-08-23** (sessione 5): aritmetica
  `maze-blk0`, fedelta' byte-per-byte compilato/disco, `MAZE-CHECK` pulito
  su entrambi i percorsi, due rotture deliberate (pillola isolata, fuga
  dal bordo) correttamente intercettate. **Esteso 2026-08-24** (sessione
  6): `MAZE-CHECK` pulito anche su 2 e 3, conteggio punti confrontato
  fra i due contatori indipendenti (`dot-count-check` di MAZE-CHECK e
  `maze-dots` di `find-pills`) su tutti e quattro i labirinti, ciclicita'
  di `level`, e due rotture deliberate delle celle di spawn.
  **Ristrutturato** lo stesso giorno per la starvation dei buffer blocchi
  (vedi sotto): la parte automatica tocca un solo labirinto su disco,
  i labirinti 2 e 3 stanno in `DISK-MAZE-TESTS`, da lanciare dal prompt. |
| `CLAUDE.md` | **Aggiunta 2026-08-24** alla sezione Known Bugs di
  `INCLUDE`/`NEEDS`: la starvation dei buffer blocchi che fa perdere a un
  file incluso la propria riga sorgente. Non e' specifico di chomp-chomp. |
| `!Blocks-64.bin` | **Screen 740/741 scritti 2026-08-23** (sessione 5)
  via `util/putscr.pl`, copia del labirinto compilato in formato
  labirinto-su-disco; verificato con `util/blocks2txt.pl`. **Screen
  742/743 e 744/745 scritti 2026-08-24** (sessione 6) via
  `util/chomp-maze.py write`, i due tracciati nuovi; le righe 21-31 di
  ogni Screen sono etichettate invece di restare a NUL. Screen 746-779
  (tranne 777-779, preesistenti) restano liberi. Verificato che la
  dimensione del file non cambia e che nessun byte fuori dai BLOCK
  1484-1491 e' stato toccato. |
| `util/chomp-maze.py` | **NUOVO 2026-08-24** (sessione 6): render/check/
  read/write/derive dei labirinti dall'host. Legge la tabella UDG
  direttamente da `demo/chomp-chomp.f`, quindi disegna sempre l'alfabeto
  corrente -- **posizionalmente**, come fa la routine di stampa (glifo
  del codice n = 8 byte a (n-144)*8), non seguendo i commenti: solo le
  voci piu' vecchie hanno la riga di intestazione esadecimale che le
  nomina, e la prima versione del parser, che si fidava di quella,
  saltava in silenzio proprio `V` e `W` -- cioe' rendeva invisibili i
  puntini e il glifo nuovo. |
| `demo/README.txt` | riscritta per Stadio 1 (niente piu' "completely
  random"); **aggiornata 2026-08-24** per i labirinti multipli,
  `MAZE-CHECK` e `util/chomp-maze.py` |

**Da sincronizzare**: `demo/chomp-chomp.f` e `demo/chomp-chomp/chomp-chomp.f`
sono cambiati per lo Stadio 4 (sessioni 5 e 6) e non ancora ripassati
dallo skill `/sync-cspect`. `!Blocks-64.bin` e' escluso di default dal
sync (`blocks` va passato esplicitamente) -- gli Screen 740-745 scritti
in queste due sessioni vanno quindi copiati sulla SD CSpect a parte,
quando comodo, prima di provare i livelli 1-3 su CSpect.

## Stadio 3: cronologia (font in RAM tentato, poi sostituito da UDG esteso)

**Approccio A (font in RAM via CHARS) -- funzionante, poi abbandonato.**
Obiettivo originale del piano (Parte 5): ridefinire i codici 65-79 (A-O:
14 muri + pillola grande) e 46 (`.`) con glifi propri via il meccanismo
NextZXOS `CHARS`/`rst $10` (control-code 30/31), eliminando `UDGize`.
Il test isolato del control-code 31 (`demo/charset-test.f`) e' passato
su CSpect (quirk trovato: la patch sul bitmap va scritta *prima* di
`31 EMITC 8 EMITC`, non dopo, o l'FPGA "aggancia" i vecchi glifi).
Implementato in `demo/chomp-chomp.f` (`my-font`, `install-font`,
`use-my-font`/`use-rom-font`) e confermato funzionante su CSpect, ma
con tre problemi via via risolti nella stessa sessione:

1. **Trail/pillola invalicabile, lampeggio assente** -- `maze-copy` non
   chiamava piu' `UDGize`, quindi `maze-run` conteneva la lettera ASCII
   `O` letterale, ma i controlli di movimento/incasso confrontavano
   ancora col codice UDG `[udg] O`. Fix: confronti spostati su
   `[char] O`.
2. **Testo di caricamento illeggibile** -- `install-font` accendeva il
   font subito, mescolando muri/pillola al testo delle istruzioni
   d'uso. Fix: attivazione spostata just-in-time dentro `init-display`,
   solo attorno a `maze.`.
3. **Bug architetturale DOT**: il core di `.vforth` vive in
   `$2000-$3FFF`, dove sotto dot-command la ROM classica non e' mai
   attiva. Il passo che "salvava il font ROM" (`CHARS-VAR @ 256 +
   my-font 768 cmove`) leggeva quindi garbage sotto DOT. Mitigato in
   piu' round (blank a 128 block-graphic -- poi rimosso perche'
   ridondante --, pillola/puntino spostati su UDG anche durante il
   game loop, e infine il fix vero: azzerare esplicitamente il glifo
   del codice 32 in `my-font`). Confermato funzionante su entrambe le
   varianti DOES e DOT.

**Approccio B (UDG esteso) -- quello adottato, sostituisce interamente
l'Approccio A.** Dopo la conferma su CSpect dell'Approccio A, l'autore
ha fatto un'osservazione decisiva: l'intero sforzo per un font separato
nasceva dalla scarsita' percepita degli UDG (solo 21 lettere, A-U), ma
il fix del punto 3 sopra ha dimostrato che **il codice UDG non ha
davvero un limite a 21**: la routine di stampa ROM/NextZXOS legge
semplicemente 8 byte a `(codice-144)*8` dalla tabella puntata da UDG,
senza mai controllare che il codice sia `<= 164`. Si puo' quindi
estendere la tabella con nuove lettere (`V`, `W`, ...) tanto quanto
serve. Questo elimina il bisogno di un font separato -- e con esso
*tutta* l'esposizione al bug DOT sopra, non solo la sua finestra
`maze.`, perche' gli UDG sono dati compilati nel dizionario, mai letti
dalla "ROM" a runtime.

Decisione dell'autore: **regredire `demo/chomp-chomp.f` alla baseline
pre-font** (`a9efc32`, salvata anche dall'autore come
`version/20260820/demo/chomp-chomp-1.f`, confermata byte-identica) ed
estendere `UDGize` per convertire anche `.` invece di introdurre
`my-font`. Implementato:

- `demo/chomp-chomp.f` ripristinato da `chomp-chomp-1.f` (== `a9efc32`,
  Stadio 1+2 intatti, `UDGize`/`between`/`install-font` ecc. nella loro
  forma originale).
- Nuovo 22-esimo slot in `UDG_1`, lettera `V` (codice 165 = 144+21),
  stesso bitmap piccolo-puntino gia' usato per `dot-glyph`
  nell'Approccio A.
- `UDGize` esteso: se il carattere e' `.` diventa `[udg] V` (non passa
  per la formula generica `UDG+`, che si applica solo alle vere lettere
  A-Z); altrimenti resta il comportamento originale (A-U -> UDG).
- I quattro confronti che leggevano `.` letterale da `maze@`
  (`?pac-trail`, `?ghost-trail`, `pacman-walk`, `pacman-eat-dot`)
  aggiornati da `[char] .` a `[udg] V`, simmetrici a come gia'
  funzionava `[udg] O`/`[udg] U`.
- `UDGs` (utility di debug "mostra tutti gli UDG"): bound del loop
  esteso da `[char] V` a `[char] W` per includere anche il nuovo slot.
- Tutto l'apparato dell'Approccio A (`my-font`, `CHARS-VAR`,
  `saved-chars`, `dot-glyph`, `install-font`, `use-my-font`,
  `use-rom-font`, `maze->display`, la finestra just-in-time in
  `init-display`/`game`) rimosso per intero -- non esiste piu' in
  `demo/chomp-chomp.f`.

`demo/charset-test.f` (il file di test isolato per il control-code 31)
**non e' stato toccato**: resta nel repo come documentazione della
scoperta sul meccanismo NextZXOS, anche se chomp-chomp non lo usa piu'.

## Stadio 4: cronologia della prima fetta (sessione 5, 2026-08-23)

Piano seguito: `prompts/CHOMP-CHOMP-PLAN.md` Parte 6-7, con tre
decisioni prese con l'autore prima di iniziare (via `AskUserQuestion`):
range Screen **740-779** (non 724-776 come nell'ipotesi originale del
piano -- l'autore ha preferito una zona dove tutto il non-vuoto e'
dichiaratamente superato, cioe' `777-779`); perimetro della sessione
fermato subito dopo infrastruttura + conversione del labirinto attuale
(nessun tracciato nuovo, quello resta per dopo); scrittura diretta di
`!Blocks-64.bin` via `util/putscr.pl` (headless, verificato con
`util/blocks2txt.pl`), senza passare da CSpect/EDIT.

**Scoperta chiave, trovata SOLO grazie a un `DUMP` diretto della memoria
(non fidarsi mai della sola lettura del sorgente per il formato binario
di `,"`\*\*: una riga di `maze-base` non e' `[count=21][21 char]`. `,"`
usa `WORD` con delimitatore `"`, e questo `WORD` salta gli spazi
iniziali (comportamento Forth classico) ma NON quelli finali -- quindi
lo spazio di allineamento scritto PRIMA del testo in ogni riga sorgente
(`," EAAAA...D "`) sparisce, mentre quello scritto DOPO resta. Il
conteggio compilato e' percio' **22** (21 lettere reali + 1 spazio
finale), e `,"` aggiunge poi un byte `0x00` sciolto (il suo `0 c,`
finale) subito dopo. Un blocco-riga e' quindi sempre 24 byte totali
(1 count + 22 dati + 1 NUL sciolto), esattamente lo stride che
`maze-copy` gia' usava -- ma il contenuto REALE occupa gli offset 1..21
(`maze-w` lettere), l'offset 22 e' sempre lo spazio finale, l'offset 23
e' sempre quel NUL. Il primo tentativo di `MAZE-CHECK`/`raw-row!`
assumeva un formato simmetrico a 23 colonne con spaziatura ai due lati
(letto dal *sorgente*, non dal *compilato*) e falliva con "NUL byte a
ogni riga, colonna 23" -- il `DUMP` di `maze-base`/`maze-run` lo ha
chiarito subito. Fix: `raw-row!`, `maze-line` e tutti i loop di
`MAZE-CHECK` ricalibrati su `maze-w`(21) colonne reali (1..21), niente
piu' compensazione "+2"; i dati gia' scritti su Screen 740/741 sono
stati rigenerati con l'estrazione a 21 caratteri (senza lo spazio
iniziale) e riscritti.

**Secondo bug, trovato dalla suite headless dopo il fix del formato**:
`check-perimeter` passava gli argomenti a `check^` **invertiti**
(colonna prima di riga) nella scansione riga-per-riga (bordo alto/
basso) -- `check^` si aspetta `( r c -- a )` e la chiamata era `i 1+ 0
check^` invece di `0 i 1+ check^`. Stessa categoria di errore gia'
vista con lo swap di troppo in `COLORS:` (Stadio 2): va sempre
riletta a mano la direzione, non basta che "sembri simmetrico". Fix
diretto sulle due righe (alto/basso); sinistra/destra erano gia'
nell'ordine giusto.

**Terzo problema, non un bug del gioco ma della logica del check**:
`check-perimeter` segnalava due falsi positivi sulla riga del tunnel
(colonna 1 e colonna `maze-w`), perche' `/` e `\` **devono**
raggiungere il bordo per design (e' cosi' che Pac-Man passa da un lato
all'altro). Fix: `check-perimeter` ora salta la colonna sinistra/destra
proprio sulla riga che `check-tunnel` ha gia' identificato
(`slash-row`/`bslash-row`), in ogni altra riga il bordo deve restare
non raggiungibile.

Verificato tutto **headless** (nessun accesso a CSpect in questa
sessione): compilazione pulita di `demo/chomp-chomp.f`, poi
`test/CHOMP-MAZE-TESTS.f` interamente verde -- aritmetica `maze-blk0`
(`1480 1484 1488`, confermata a mano), `maze-run` identico byte-per-
byte fra il percorso compilato e quello da Screen 740/741 dopo
`set-maze-run`, `MAZE-CHECK` pulito su entrambi i labirinti, e le due
rotture deliberate (pillola isolata via muri finti, marcatore di
raggiungibilita' piazzato a mano sul bordo) correttamente intercettate
da `check-connectivity`/`check-perimeter`. **Resta da confermare a
schermo su CSpect**: che il livello 1 (`1 level ! GAME`, o aspettando
il primo `phase-complete`) si giochi in modo indistinguibile dal
livello 0 -- criterio di successo esplicito di questa fetta.

## Stadio 4: cronologia della seconda fetta (sessione 6, 2026-08-24)

Perimetro: i tracciati nuovi lasciati fuori dalla sessione 5. Tre cose
sono emerse prima ancora di disegnarne uno, e vanno ricordate perche'
ognuna e' una trappola silenziosa.

**1. Il conteggio dei punti era hard-coded a 180, e non era una
costante di comodo: era un vincolo di progetto non scritto.** La fase e'
completa quando `score` **eguaglia** `total` (`d=`), ogni puntino vale 1,
e `total` partiva da `180.` -- il numero esatto di `.` del labirinto
compilato. Un labirinto disegnato con un numero diverso di puntini non
avrebbe dato errore: `score` avrebbe semplicemente scavalcato `total`
senza mai eguagliarlo, e il livello non sarebbe finito **mai**. Nessuno
dei controlli esistenti lo avrebbe intercettato. Risolto rendendo il
conteggio dinamico: `find-pills` gia' scandiva tutto il labirinto per
la cache delle pillole, ora conta anche i puntini in `maze-dots`, e i
tre punti che innescavano `total` (`game`, `phase-complete`,
`ghost-catch` a vite esaurite) lo leggono da li'. In `phase-complete`
il conteggio va preso **dopo** `set-maze-run`/`find-pills`, non prima
come stava il vecchio `180 total D+!`: quello che serve e' il totale
del labirinto che sta per essere giocato, non di quello appena finito.

**2. L'alfabeto dei muri e' una regola esatta, non arte a mano -- e ne
mancava esattamente un pezzo.** Una cella-muro traccia un segno lungo
ogni suo lato che confina con corridoio aperto, e le quattordici lettere
`A`-`N` sono **esattamente** i quattordici sottoinsiemi non vuoti di
{N,S,W,E} con almeno un lato libero:

    A N     B S     C NS    M W     J E     N WE
    E NW    D NE    I SW    H SE
    F NSW   G NSE   K NWE   L SWE

Il quindicesimo -- tutti e quattro i lati, cioe' l'isolotto da una cella
sola -- non c'era, e senza quello un pilastro isolato non e' disegnabile.
Aggiunto come `W`, codice UDG 166 (23-esimo slot), l'arco superiore di
`K` sopra quello inferiore di `L`. La regola e' stata **verificata**
rigenerando meccanicamente il labirinto compilato dalla sola mappa
muro/corridoio: riproduce ogni sua isola interna cella per cella. Le
uniche celle che non segue sono la silhouette esterna e il guscio della
casa dei fantasmi, che sono davvero disegnate a mano (la silhouette
traccia il lato *esterno*, non quello verso il corridoio; il muro della
casa non si chiude accanto alla porta `-`). Per questo i due tracciati
nuovi riusano quelle celle **verbatim** dal labirinto compilato.

**3. Le posizioni di partenza degli sprite sono hard-coded nel gioco,
non lette dal labirinto.** `pacman-init`/`ghost-init`/`ghost-eaten`/
`cherry-init` fissano riga e colonna, e ciascuno **memorizza uno spazio**
come cella che sta coprendo: un labirinto che ci mette un puntino lo
perde nel momento in cui lo sprite se ne va (e con lui il conteggio
torna a non tornare). Ted e' l'eccezione: parte *sulla* porta, che
quindi deve essere `-`. Ora `check-spawn` lo verifica dentro
`MAZE-CHECK`, e la stessa cosa fa `util/chomp-maze.py`.

**`util/chomp-maze.py`** e' nato da qui: un labirinto scritto con
quell'alfabeto e' illeggibile come testo, e l'unico modo per distinguere
un raccordo giusto da uno rotto e' guardare i bitmap 8x8. Lo script
legge la tabella UDG direttamente da `demo/chomp-chomp.f` (quindi disegna
sempre l'alfabeto corrente), rende il labirinto a pixel, rifa' headless
gli stessi controlli strutturali di `MAZE-CHECK` piu' il conteggio dei
puntini, e con `derive` risolve un abbozzo in cui i muri sono scritti
come blocchi `#` pieni nei glifi che il vicinato richiede -- che e' come
sono stati disegnati i due tracciati. `write` rifiuta di scrivere un
labirinto che non passa i controlli.

**I due tracciati**: maze 2 su Screen 742/743 (192 puntini, due fasce di
blocchi di forma diversa e due isolotti `W`), maze 3 su Screen 744/745
(218 puntini, pettini verticali sopra e sotto e quattro pilastri `W`
attorno alla casa). Entrambi riusano silhouette, riga del tunnel e
guscio della casa dal labirinto compilato, come sopra. `n-mazes` passa
da 2 a 4.

Un criterio non ovvio, trovato misurando il labirinto compilato invece
che a occhio: **maze-base non ha nemmeno un vicolo cieco** (nessuna
cella con una sola uscita). Le prime versioni dei due tracciati nuovi ne
avevano 8 e 4 -- tutti nati dove un blocco di progetto tappava un
corridoio contro lo scheletro fisso, cioe' esattamente dove non si
guarda. Ridisegnati fino a zero, come l'originale.

**Quarta scoperta, costata due giri di emulatore e la piu' riutilizzabile
di tutte: un file INCLUDEd puo' perdere la propria riga sorgente.**
`F_INCLUDE` legge ogni riga nel buffer di **BLOCK 1** e mette `BLK` a 1 --
quindi la riga in corso di interpretazione vive nel pool dei buffer
blocchi, e quel pool e' **sei buffer assegnati a rotazione**
(`FIRST`/`PREV`/`USE`). Un file che legge sei altri blocchi distinti
mentre interpreta ricicla percio' il buffer che contiene la propria riga:
`WORD` rilegge BLOCK 1 da disco, trova i metadati del file blocchi al
posto della riga, e l'interprete ci cammina dentro. **Quello che si vede
e' una parola a caso "is undefined"** -- una parola *diversa a ogni
esecuzione*, perche' dipende da cosa capita nel buffer riciclato: nel
primo giro `extZXOS?`, nel secondo `one?`. Niente indica la causa vera, e
il file incriminato e' innocente.

`MAZE-CHECK` legge tre blocchi per labirinto su disco, quindi la suite
che ne controllava tre ne toccava nove e perdeva la riga a meta'.
Confermato con una sonda che non conteneva altro che quattro
`MAZE-CHECK`: e' morta alla **sesta** lettura di blocco, esattamente
quando la rotazione e' tornata su BLOCK 1. La suite della sessione 5
funzionava per un pelo -- controllava solo il labirinto 1, i cui tre
blocchi erano gia' residenti dal test di fedelta'.

Ristrutturata di conseguenza: la parte automatica spende tutto il budget
su **un solo** labirinto su disco (il #1, i cui blocchi vengono poi
riusati), e tutto cio' che riguarda i labirinti 2 e 3 sta in
`DISK-MAZE-TESTS`, una parola compilata dal file e lanciata **dal prompt
`ok`** -- dove l'input viene dal TIB, `BLK` e' 0 e nessuna riga sorgente
e' a rischio. (`T{` `->` `}T` di `lib/testing.f` sono normali parole
`:`, quindi si compilano dentro una definizione senza problemi.) Il
vincolo e' annotato anche in `CLAUDE.md`, sezione Known Bugs di
`INCLUDE`/`NEEDS`: non e' specifico di chomp-chomp.

**Verificato headless**: compilazione pulita, `MAZE-CHECK` pulito su
tutti e quattro i labirinti (180/180/192/218 puntini), il contatore del
gioco (`find-pills`/`maze-dots`) d'accordo con quello indipendente di
`MAZE-CHECK` su tutti e quattro, e le quattro rotture deliberate
(pillola isolata, fuga dal bordo, muro sulla partenza di Pac-Man, porta
di Ted cancellata) tutte intercettate.

## Come far girare l'emulatore con questo gioco (invariato dalla sessione 2)

`emu/repl.py` non riesce a caricare chomp-chomp con le soglie di serie
(`IDLE_INSTRS`/`STEP_CAP` troppo basse, si ferma in silenzio). Serve un
driver che le alzi (`IDLE_INSTRS = 5_000_000`, `STEP_CAP = 3_000_000_000`)
e lo lanci in background: un giro completo (boot + gioco + suite) impiega
circa 41 minuti. Non aspettarlo con un `pgrep` sul nome dello script (la
riga di comando del watcher contiene il proprio nome e matcha se stessa).

## Cosa resta da validare su CSpect

Vedi il piano, Parte 8, per la lista completa dei controlli gia' eseguiti.

**FATTO 2026-08-23**: l'Approccio B (UDG esteso) confermato su CSpect a
schermo, `ZAP GAME` confermato standalone via `game.bas`. Nessuna
verifica pendente per lo Stadio 3.

**PENDENTE (Stadio 4, sessioni 5 e 6)**: i livelli 1-3 (labirinti
caricati dagli Screen 740-745) non sono ancora stati provati a schermo
-- solo verificati headless (vedi sopra). Prima di provarli va
rigenerata la SD CSpect: `demo/chomp-chomp.f` via `/sync-cspect`, e gli
Screen 740-745 di `!Blocks-64.bin` a parte (il sync esclude i blocchi di
default). Al tavolo:

0. Da una sessione vForth viva (anche su emulatore):
   `INCLUDE demo/chomp-chomp.f`, `INCLUDE test/CHOMP-MAZE-TESTS.f`, poi
   **`DISK-MAZE-TESTS` al prompt** -- la parte della suite che tocca i
   labirinti 2 e 3, che non puo' girare dentro un INCLUDE.
1. `1 level ! GAME` deve giocarsi indistinguibile dal livello 0.
2. `2 level ! GAME` e `3 level ! GAME`: i tracciati nuovi devono
   **apparire come li disegna `util/chomp-maze.py render`**. E' qui che
   si vede se la regola dei glifi regge anche dove il render dice di si'
   -- in particolare i raccordi dove un muro sottile si attacca al
   bordo (glifo `N` sul bordo, non `A`) e i quattro pilastri isolati
   `W` in fondo al maze 3, che sono il glifo nuovo mai visto a schermo.
3. Lasciar completare uno schema in gioco deve caricare il livello
   successivo da solo (`phase-complete` avanza `level`), e il livello
   **deve finire**: e' la conferma a schermo che il conteggio dinamico
   dei puntini funziona su un labirinto che non ne ha 180. Il maze 3
   (216 puntini) e' il caso che con il vecchio 180 fisso non sarebbe
   finito mai.
4. I `.bin` standalone in `demo/chomp-chomp/` sono superati dallo
   Stadio 4 e vanno rigenerati con `ZAP GAME` quando comodo.

## Scoperte laterali

- **RISOLTO 2026-08-23.** `tutorial/059-standalone-executables.f` e
  l'intestazione di `lib/ZAP.f` documentavano `ZAP CHOMP-CHOMP`, corretti in
  `ZAP GAME`.
- (non toccato) Esiste una terza copia del gioco residente nei blocchi
  (`600 LOAD`). Decisione presa: dichiararla superata, senza aggiornarla.
- **Nota dell'autore 2026-08-23** sul meccanismo di installazione font
  (dall'Approccio A, non piu' in uso in chomp-chomp ma valida in
  generale): su LAYER0 basta scrivere il nuovo puntatore in CHARS-VAR
  (23606, $5C36) perche' la routine ROM di stampa lo prenda subito in
  considerazione -- non serve il control-code NextZXOS `31 EMITC 8
  EMITC`. E' backward compatibility con lo Spectrum classico (il trucco
  storico "font custom via POKE 23606,..." leggeva gia' CHARS ad ogni
  carattere stampato). Su LAYER11/LAYER12 (quelli usati da chomp-chomp)
  la sequenza `31 EMITC 8 EMITC` restava invece necessaria -- e questo
  spiega perche' il quirk trovato in `demo/charset-test.f` (patch del
  bitmap prima del control-code) e' legato a quel path esplicito, non al
  caso LAYER0.
- **Scoperta chiave 2026-08-23**: il codice UDG (144-164, lettere A-U)
  non ha un limite hardware/ROM a 21 voci -- la routine di stampa legge
  semplicemente `(codice-144)*8` byte dalla tabella puntata dal
  system-variable UDG, senza upper bound. Estendere la tabella con
  lettere oltre `U` (`V`, `W`, ...) e' sicuro. Questa scoperta e' quella
  che ha reso superfluo l'intero Approccio A (font in RAM) -- vedi sopra.
