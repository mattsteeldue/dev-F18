# Confronto LAYER2+ (storico) vs LAYER22 (attuale)

Fonti:
- storico: `version/20250815/lib/GRAPHICS.f` (definizione `LAYER2+`, mai promossa a
  mainline, raggiungibile solo tramite un caso `SETUP` commentato "`or LAYER2+`")
- attuale: `lib/LAYER22-GRAPHICS.f` + `lib/GRAPHICS-COMMON.f`

## Identita'

Stesso modo grafico: Layer 2 320x256, 10 pagine MMU7 a partire da `L2-RAM-PAGE`,
`char-size=$04`, `layer-mode=$20`, `V-RANGE=$100`, `H-RANGE=$140`. LAYER22 e' la
versione promossa a mainline dell'esperimento LAYER2+.

## PIXELADD

Algoritmo Z80 (shift `bsrl de,b` di 5 bit, trucco `DAA` per il modulo-10, `nextreg
$57`) **identico** tra le due versioni.

Differenza reale: lo stack comment storico e' invertito -- dichiarato `( y x -- a )`
ma il primo `pop de` e' poi etichettato "horizontal y-coord" (cioe' y), il che
contraddice l'ordine dichiarato. LAYER22 corregge lo stack comment in `( x y -- a )`,
coerente con l'ordine di pop effettivo. Nessun bug funzionale nell'algoritmo di pop
stesso, solo un refuso di commento (pattern "l'autore inverte i concetti").

C'e' anche un commento fossile nel vecchio file ("uses six 8k-pages $12-$1C") che non
corrisponde piu' al codice a 10 pagine.

## INITIALIZE

Stessi NextReg (`$70=$10`, clip X 0..159, Y 0..255). Differenza sostanziale nel
colore:

- LAYER2+ derivava il PAPER per sottrazione: `#255 ATTRIB - .PAPER` -- pattern
  "NEGATE al posto di INVERT" che nel fix color-DEFER causava PAPER che non azzerava
  piu' l'INK.
- LAYER22 usa un campo `BACKGROUND` dedicato (costante `_BLUE`), lo applica sia a
  `.PAPER` che a `.BORDER`, e chiama esplicitamente `RGB-COLORS` (profilo colore
  corretto per Layer2, distinto da `ATTR-COLORS`).

## CLS / pulizia framebuffer -- la differenza piu' importante

- LAYER2+ installava `L22-CLS` come vettore `CLS`: **ogni** chiamata a CLS
  riscriveva tutte e 10 le pagine (80K), e **non** salvava/ripristinava MMU7 attorno
  al loop -- lascia la mappatura sull'ultima pagina del framebuffer, esposto allo
  stesso bug-class descritto per "Fragilita' MMU7" (risolto poi in
  `(EMITC)`/`(FIND)`/`WORDS`).
- LAYER22 chiama `L22-CLEAR` **una sola volta** dentro `INITIALIZE`, salva/ripristina
  esplicitamente `MMU7@` (`MMU7@ >R ... R> MMU7!`), e riempie con `BACKGROUND`
  invece che con l'espressione derivata per sottrazione. Nella tabella `LAYER:`
  attuale non esiste piu' un campo CLS vettorizzato per-layer: quel grado di
  liberta' e' stato eliminato dal framework comune.

## Struttura del modulo

LAYER2+ viveva inline nel monolitico `lib/GRAPHICS.f`, condiviso e mescolato con
tutti gli altri layer. LAYER22 e' un modulo a se' (`lib/LAYER22-GRAPHICS.f`), con
`NEEDS GRAPHICS-COMMON`, guard-word per `NEEDS`, `MARKER NO-LAYER22-GRAPHICS` per lo
scarico pulito, e riusa `L1-POINT`/`L1-PLOT`/`L1-XPLOT`/`L1-EDGE`/`L2-RAM-PAGE`/
`.BORDER` via `NEEDS` invece di ridefinirle -- segue la convenzione di refactoring
di `lib/CLAUDE.md`.

## In sintesi

Stesso algoritmo di indirizzamento pixel, ma LAYER22 ripulisce tre cose del
prototipo LAYER2+: lo stack comment errato, la derivazione del colore per
sottrazione, e soprattutto il bug di sicurezza MMU7 nel CLS ripetuto -- oltre a
modularizzare il codice.
