# chomp-chomp: stato della revisione (agg. 2026-08-23, sessione 4)

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
si e' tornati sugli UDG). Stadio 4 (labirinti su Screen) non iniziato.

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

| File | Stato |
|---|---|
| `demo/chomp-chomp.f` | Stadio 1+2+3 completi, **confermati su CSpect**
  (schermo, non solo compilazione). Stadio 3 nella sua forma finale:
  `UDGize` (rimessa) converte A-U *e* `.` (nuovo 22-esimo slot UDG,
  lettera `V`) a tempo di `maze-copy`; nessun font personalizzato,
  nessuna lettura di "ROM" a runtime. Banner `.( Chomp.f - X )` ->
  `.( X )` (richiesta cosmetica dell'autore, 11 occorrenze). |
| `demo/chomp-chomp/chomp-chomp.f` | **FATTO 2026-08-23**: copia del
  master, confermata byte-identica dall'autore. `chomp-chomp-0.f` (la
  vecchia copia pre-revisione, superata) rimossa dalla stessa cartella. |
| `demo/chomp-chomp/game-core.bin` / `game-heap.bin` / `game-user.bin` | **FATTO
  2026-08-23**: rigenerati con `ZAP GAME` da una sessione vForth viva
  dopo il fix di `lib/ZAP.f` sotto; lanciati via `game.bas` e
  confermati funzionanti standalone (senza `INCLUDE`). Spostati
  dall'autore anche su W: (SD CSpect), non solo in locale. |
| `lib/ZAP.f` | **Bug pre-esistente trovato e corretto dall'autore
  2026-08-23**: mancava `NEEDS [']` dopo `MARKER TASK` -- una sessione
  vForth pulita che caricava `ZAP` senza gia' avere `[']` in dizionario
  falliva. Non e' un regressione di questa sessione; scoperto solo ora
  perche' `ZAP GAME` non era mai stato riprovato dallo Stadio 3. |
| `test/CHOMP-AI-TESTS.f` | ~45 asserzioni, tutte verdi (verificato sessione 2) |
| `demo/README.txt` | riscritta per Stadio 1 (niente piu' "completely
  random"); da rivedere di nuovo a fine Stadio 3/4 per i labirinti multipli |

**Da sincronizzare**: `lib/ZAP.f` e `demo/chomp-chomp/chomp-chomp.f`
sono nuovi/modificati nel repo PC ma non ancora passati dallo skill
`/sync-cspect` -- l'autore ha spostato a mano i `.bin`/`game.bas` su
W:, ma questi due file testuali potrebbero non essere allineati sulla
SD finche' non gira un sync.

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

## Come far girare l'emulatore con questo gioco (invariato dalla sessione 2)

`emu/repl.py` non riesce a caricare chomp-chomp con le soglie di serie
(`IDLE_INSTRS`/`STEP_CAP` troppo basse, si ferma in silenzio). Serve un
driver che le alzi (`IDLE_INSTRS = 5_000_000`, `STEP_CAP = 3_000_000_000`)
e lo lanci in background: un giro completo (boot + gioco + suite) impiega
circa 41 minuti. Non aspettarlo con un `pgrep` sul nome dello script (la
riga di comando del watcher contiene il proprio nome e matcha se stessa).

## Cosa resta da validare su CSpect (Stadio 1+2, gia' confermato)

Vedi il piano, Parte 8, per la lista completa dei controlli gia' eseguiti.

**FATTO 2026-08-23**: l'Approccio B (UDG esteso) confermato su CSpect a
schermo, `ZAP GAME` confermato standalone via `game.bas`. Nessuna
verifica pendente per lo Stadio 3.

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
