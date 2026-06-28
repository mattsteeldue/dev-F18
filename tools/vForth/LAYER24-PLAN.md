# Piano di sviluppo: LAYER24 (Layer 2, 640x256, 16 colori, 4bpp)

> Stato: **PIANO APPROVATO, implementazione non ancora iniziata.**
> Nome modulo deciso dall'utente: **LAYER24** (il "4" richiama 4bpp / 16 colori).
> Primitive con prefisso **L4-** (= 4bpp).
> Riferimento sorgente: `doc/zx-next-dev-guide-r3.txt` cap. 3.6 (Layer 2),
> in particolare 3.6.6 (320x256), 3.6.7 (640x256) e 3.6.8 (registri).
> Modello di partenza: `lib/LAYER22-GRAPHICS.f` (320x256, fatto il giorno prima).

## Scoperta chiave: in byte, 640x256 e' identico a 320x256

- 640x256 a 4bpp = 640*256/2 = 81920 byte = 80K = **10 pagine da 8K**, come LAYER22.
- La guida dice "8K bank = 64 colonne", ma sono 64 colonne SCHERMO = **32 colonne
  BYTE** (2 pixel/byte). Quindi 32 byte-colonne per pagina da 8K, **identico a 320**.
- Indirizzamento del byte = come L22 dividendo X per 2:
  `byteX = y>>1`, `page = byteX>>5`, `colonna = byteX&31`, riga (low byte) = `x`.

Quindi clear, init, paging, clip window e l'ossatura `LAYER:` sono quasi copia-incolla
di LAYER22.

## Differenze rispetto a LAYER22

| Aspetto          | LAYER22 (320)   | LAYER24 (640)                          |
|------------------|-----------------|----------------------------------------|
| NextReg `$70`    | `%00010000`     | `%00100000`                            |
| Clip window `$18`| X2=159, Y2=255  | **identico** (la guida usa /4-1 = 159) |
| `H-RANGE`        | 320 (`$0140`)   | 640 (`$0280`)                          |
| `V-RANGE`        | 256 (`$0100`)   | 256 (`$0100`) invariato                |
| PIXELADD         | `byteX = y`     | `byteX = y>>1` (un `bsrl de,1` in piu')|
| PLOT/POINT/XPLOT | scrive byte pieno| **read-modify-write di un nibble**    |

Convenzione coordinate ereditata da LAYER22: `x` = verticale (0..255),
`y` = orizzontale (0..639). PLOT/POINT prendono `( x y )`.

## La vera complicazione: il nibble (2 pixel per byte)

`L1-PLOT` fa `PIXELADD ATTRIB SWAP C!` -> scrive un byte intero: inservibile a 4bpp.
Convenzione nibble (da guida 3.6.7, "Colour 1 | Colour 2" = nibble alto | nibble basso):

- pixel X **pari** (sinistro) -> **nibble alto** (bit 7-4)
- pixel X **dispari**         -> **nibble basso** (bit 3-0)
- la parita' `y&1` va salvata **prima** di chiamare `PIXELADD` (che consuma `y`).

## File da creare

### Nuove parole inc/ (4bpp, nibble-aware)

1. `inc/l4-pixeladd.f` — CODE. Copia di `L22-PIXELADD` con un `bsrl de,1` iniziale per
   dimezzare `y`; ritorna l'indirizzo del **byte**. Algoritmo (stile L22):
   - `pop de` (y), `pop hl` (x, solo L)
   - `bsrl de,1`  -> de = byteX = y>>1
   - `ld c,e`     -> c = byteX low byte
   - `ld b,5 / bsrl de,b` -> de = byteX>>5 = page (0..9)
   - `ld a,e / daa / and 0F / add L2-RAM-PAGE / nextreg 57,a` -> mappa pagina su MMU7
   - `ld a,E0 / or c / ld h,a` -> H = $E0 | (byteX&31), L = x
   - `push hl / next`

2. `inc/l4-plot.f` — alto livello Forth:
   ```
   : L4-PLOT  ( x y -- )
       COORD-CHECK IF
           DUP 1 AND >R          \ parita': 0=pari/alto, 1=dispari/basso
           PIXELADD              \ a
           ATTRIB 15 AND         \ colore 0..15
           R> IF                 \ dispari -> nibble basso
               SWAP DUP C@ 240 AND ROT OR SWAP C!
           ELSE                  \ pari -> nibble alto
               4 LSHIFT SWAP DUP C@ 15 AND ROT OR SWAP C!
           THEN
       ELSE 2DROP THEN ;
   ```
   (verificare lo juggling di stack in fase di scrittura)

3. `inc/l4-point.f` — alto livello:
   ```
   : L4-POINT  ( x y -- c )
       COORD-CHECK IF
           DUP 1 AND >R
           PIXELADD C@
           R> IF 15 AND ELSE 4 RSHIFT 15 AND THEN   \ pari=alto(>>4), dispari=basso
       ELSE 2DROP -1 THEN ;
   ```

4. `inc/l4-xplot.f` — XOR del solo nibble:
   ```
   : L4-XPLOT  ( x y -- )
       COORD-CHECK IF
           DUP 1 AND >R
           PIXELADD
           R> IF 15 ELSE 240 THEN   \ maschera del nibble da invertire
           OVER C@ XOR SWAP C!
       ELSE 2DROP THEN ;
   ```

5. `inc/l4-edge.f` — `: L4-EDGE ( b -- f ) ATTRIB 15 AND = ;` (variante di L1-EDGE
   mascherata a 4 bit, perche' POINT torna un nibble 0..15).

### Nuovo modulo lib/LAYER24-GRAPHICS.f

Clone di `lib/LAYER22-GRAPHICS.f`:
- `NEEDS GRAPHICS-COMMON`, `MARKER NO-LAYER24-GRAPHICS`, word-guard `LAYER24-GRAPHICS`.
- `NEEDS L4-POINT L4-PLOT L4-XPLOT L4-EDGE L4-PIXELADD L2-RAM-PAGE MMU7@ .BORDER`.
- `L4-CLEAR` = copia identica di `L22-CLEAR` (salva/ripristina `MMU7@`, riempie le 10
  pagine da 8K con BACKGROUND).
- `L4-INITIALIZE`:
  ```
  20  70 REG!                 \ Layer 2 Control: 640x256 4bpp (%00100000)
  0   1C REG!                 \ reset clip-window index
  0   18 REG!  #159 18 REG!   \ X clip 0..159
  0   18 REG!  #255 18 REG!   \ Y clip 0..255
  RGB-COLORS                  \ INK 0..15 finisce in ATTRIB, mascherato a nibble al plot
  ATTRIB     .INK
  BACKGROUND .PAPER
  BACKGROUND .BORDER
  L4-CLEAR
  ```
- Tabella `LAYER:` come LAYER22 ma:
  - V-RANGE `0100` (256), H-RANGE `0280` (640)
  - PIXELADD = `' L4-PIXELADD`, POINT = `' L4-POINT`, PLOT = `' L4-PLOT`,
    XPLOT = `' L4-XPLOT`, PIXELATT = `' L4-PLOT` (placeholder), EDGE = `' L4-EDGE`,
    XY-RATIO = `' NOOP`, INITIALIZE = `' L4-INITIALIZE`
  - layer-mode byte = `20` (base Layer 2, come LAYER22; e' $70 a cambiare risoluzione)
  - char-size `04`, attribute mask `1 0FF`, BACKGROUND/ATTRIB come da scelta colore.
- `LAYER: LAYER24` poi attiva con `LAYER24`.

## Validazione

- **Nessun rebuild del core**: e' solo libreria.
- **Unit test emulatore headless** (`emu/`): `PLOT` di un pixel poi `POINT` deve
  restituire lo stesso colore. Caso critico: due pixel **adiacenti** pari/dispari nello
  stesso byte -> verificare che PLOT del secondo non distrugga il nibble del primo.
  L'emulatore modella MMU7 + NextReg ma NON disegna il Layer 2, quindi ci si affida al
  roundtrip PLOT/POINT, non al rendering.
- **Validazione visiva finale su CSpect**, avviata dall'utente
  (vedi memoria feedback_cspect_launch: NON avviare CSpect dal sandbox).

## Rilascio (dopo OK su CSpect)

Nuova libreria a core invariato -> pipeline `/release-rebuild` come per LAYER22
(timbro nuova build, sync), con gate manuale .odt/.pdf da aggiornare a mano
(menzione di LAYER24 nel manuale). Da fare in un secondo momento.

## Rischi da tenere a mente

- Le **5 banche da 16K** dalla banca attiva di Layer 2 (`$12`) devono essere libere:
  NextZXOS ne alloca solo 3 (48K) per il 256x192 standard; le 2 extra vanno garantite
  libere. Stesso avviso gia' in LAYER22.
- Il paging MMU7 e' la "creatura fragile" del core (vedi memoria mmu7_fragility): ogni
  `(EMITC)`/`(FIND)` durante l'uso interattivo rimappa MMU7, quindi `L4-CLEAR` deve
  salvare/ripristinare `MMU7@` esattamente come `L22-CLEAR`.

## Punto di ripresa

Tutto e' deciso. Prossimo passo concreto: scrivere `inc/l4-pixeladd.f` (il CODE,
il pezzo piu' delicato), poi le tre primitive Forth, l4-edge, infine il modulo lib.
