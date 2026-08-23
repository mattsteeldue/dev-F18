# chomp-chomp: stato della revisione (agg. 2026-08-23, sessione 5)

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

**Stadio 4 (labirinti su Screen) — prima fetta completa e verificata
headless 2026-08-23 (sessione 5): infrastruttura di caricamento,
contatore di livello, `MAZE-CHECK`, e il labirinto attuale convertito
come primo labirinto su disco (livello 1).** Nuovi tracciati (che
sfruttino eventualmente altri UDG per incroci a T) restano fuori
perimetro, per una sessione successiva -- vedi la sezione dedicata piu'
sotto.

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
| *(non ancora committato -- l'autore usa GitHub Desktop, non la CLI)* |
  Stadio 4 prima fetta: infrastruttura labirinti su Screen, `MAZE-CHECK`,
  labirinto attuale convertito come livello 1 su Screen 740/741. |

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
| `demo/chomp-chomp/chomp-chomp.f` | **FATTO 2026-08-23** (sessione 5):
  ricopiato dal master, verificato byte-identico (`diff`), include ora
  anche lo Stadio 4. |
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
  dal bordo) correttamente intercettate. Tutto verde headless. |
| `!Blocks-64.bin` | **Screen 740/741 scritti 2026-08-23** (sessione 5)
  via `util/putscr.pl`, copia del labirinto compilato in formato
  labirinto-su-disco; verificato con `util/blocks2txt.pl`. Screen
  742-779 (tranne 777-779, preesistenti) restano liberi. |
| `demo/README.txt` | riscritta per Stadio 1 (niente piu' "completely
  random"); da rivedere di nuovo a fine Stadio 4 per i labirinti multipli |

**Da sincronizzare**: `demo/chomp-chomp.f` e `demo/chomp-chomp/chomp-chomp.f`
sono cambiati per lo Stadio 4 (sessione 5) e non ancora ripassati dallo
skill `/sync-cspect`. `!Blocks-64.bin` e' escluso di default dal sync
(`blocks` va passato esplicitamente) -- lo Screen 740/741 scritto in
questa sessione va quindi copiato sulla SD CSpect a parte, quando
comodo, prima di provare il livello 1 su CSpect.

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

**PENDENTE (Stadio 4, sessione 5)**: il livello 1 (labirinto caricato
da Screen 740/741) non e' ancora stato provato a schermo -- solo
verificato headless (vedi sopra). Prima di provarlo va rigenerata la SD
CSpect: `demo/chomp-chomp.f` via `/sync-cspect`, e lo Screen 740/741 di
`!Blocks-64.bin` a parte (il sync esclude i blocchi di default). Al
tavolo: 1) `1 level ! GAME` deve giocarsi indistinguibile dal livello 0;
2) lasciar completare uno schema in gioco deve caricare il livello 1 da
solo (`phase-complete` avanza `level`); 3) i `.bin` standalone in
`demo/chomp-chomp/` sono superati dallo Stadio 4 e vanno rigenerati con
`ZAP GAME` quando comodo.

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
