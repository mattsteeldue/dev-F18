# LAYER22-GRAPHICS — Appunti

## Cos'è
Modalità grafica **Layer 2 in alta risoluzione 320×256, 256 colori, 1 colore per pixel** → **1 byte per pixel** (8bpp). Niente nibble: ogni pixel è un byte pieno. È questa la differenza sostanziale con LAYER24 (640×256, 4bpp/16 colori, mezzo byte per pixel).

Caricamento: `NEEDS LAYER22-GRAPHICS` → tira `GRAPHICS-COMMON` e **attiva subito** la modalità (riga finale `LAYER22`).

## Memoria
- Framebuffer = 320·256·1 = 81920 byte = **80K = cinque banchi da 16K = dieci pagine da 8K (MMU7)**.
- Layout a **bande verticali di 32 colonne**: una pagina da 8K per banda di 32 colonne-byte (al contrario del layout orizzontale del 256×192 standard).
- Indirizzamento del byte (in `L22-PIXELADD`):
  - `page  = y >> 5`  (quale pagina da 8K, 0..9) → mappata su MMU7 con `+ L2-RAM-PAGE`
  - `colonna = y & 31` → finisce nei bit alti di H sopra `$E0` (nessun mask necessario sul low byte)
  - `riga = x` (low byte L)
  - indirizzo = `$E000 + (y&31)*256 + x`

## Convenzione coordinate (ereditata, non standard!)
`x` = **verticale** (0..255), `y` = **orizzontale** (0..319). PLOT/POINT/… prendono `( x y )`.

## Parole usate (tutte già estratte in inc/, deduplicate via NEEDS)
`L1-POINT`, `L1-PLOT`, `L1-XPLOT`, `L1-EDGE`, `L2-RAM-PAGE`, `MMU7@`, `.BORDER`.
PLOT/POINT/XPLOT sono i **generici L1-** (scrittura/lettura di byte pieno) — non servono varianti dedicate perché in questa modalità il pixel = byte. È esattamente ciò che in LAYER24 non basta più (lì servono i nuovi `L4-*` nibble-aware).

## Definizioni proprie del modulo
- `L22-PIXELADD` (CODE): calcola page/colonna/riga, mappa la pagina su MMU7 via `nextreg $57`, ritorna l'indirizzo del **byte**.
- `L22-CLEAR`: salva `MMU7@`, riempie le 10 pagine da 8K con `BACKGROUND` (`FILL`), **ripristina MMU7** (l'heap resta consistente — punto fragile del core).
- `L22-INITIALIZE`:
  - `$70 = %00010000` (Layer 2 Control: risoluzione 320×256)
  - clip window: X 0..159 (= 0..319 in unità da 2 px), Y 0..255
  - `RGB-COLORS`, poi `.INK`/`.PAPER`/`.BORDER`, infine `L22-CLEAR`.

## Tabella `LAYER:` (build/attivazione)
- layer-mode byte = `$20` (Layer 2 base; è `$70` a commutare la risoluzione)
- char-size `04` (64 char/riga), attribute mask `1 0FF`
- **V-RANGE `$0100` (256), H-RANGE `$0140` (320)**
- PIXELADD=`L22-PIXELADD`, POINT/PLOT/XPLOT/EDGE = `L1-*`, PIXELATT=`L1-PLOT` (placeholder, mai chiamata in modalità 1-colore/pixel), XY-RATIO=`NOOP`, INITIALIZE=`L22-INITIALIZE`
- BACKGROUND=`_BLUE`, ATTRIB=`0D8`

## Avvertenze
- Servono **liberi i 5 banchi da 16K** a partire dal banco attivo di Layer 2 (`NextReg $12`). NextZXOS ne alloca solo 3 (48K) per il 256×192: i 2 extra vanno garantiti liberi. **Da validare su HW/CSpect.**
- `L22-CLEAR` salva/ripristina `MMU7@` perché ogni `(EMITC)`/`(FIND)` interattivo rimappa MMU7 (fragilità nota del paging).

## Rapporto con LAYER24
LAYER24 è il clone 640×256/4bpp: stesso footprint (80K/10 pagine), stesso indirizzamento ma con `y>>1` in più (2 px/byte) e PLOT/POINT/XPLOT riscritti **nibble-aware** (`L4-*`). Per LAYER22 il pixel = byte, quindi riusa direttamente i generici `L1-*`.
