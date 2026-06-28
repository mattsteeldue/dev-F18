# Piano di sviluppo: PAINT (flood fill per aree chiuse)

> Stato: **ANALISI COMPLETATA (2026-06-28). Implementazione da fare.**
> L'algoritmo attuale in `GRAPHICS-COMMON.f` e `inc/PAINT.f` e' corretto
> per regioni rettangolari ma fallisce su forme concave o non convesse.

## Diagnosi del bug nell'algoritmo attuale

Il codice attuale (`PAINT-HITX`) avanza riga per riga lungo `x` ma controlla
e semina sempre dalla **colonna `y` originale del seme**:

```forth
: PAINT-HITX ( x y d -- )
    >R
    BEGIN
        SWAP R@ + 0FF AND SWAP
        2DUP POINT EDGE NOT     \ controlla (x', y_originale)
        ?TERMINAL 0= AND
    WHILE
        2DUP PAINT-HIT2         \ semina da y_originale
    REPEAT
```

Fallisce su qualsiasi forma non rettangolare. Esempio:

```
riga 0: ..XXXXXXXX..
riga 1: ..XXXX.XXXX.   <- seme a (1, 4)   y_orig=4
riga 2: .......XXXX.   <- (2,4) = boundary -> PAINT-HITX si ferma QUI
riga 3: .......XXXX.   <- mai raggiunta, mai dipinta
```

La parte destra delle righe 2 e 3 non viene mai dipinta.

## Perche' la ricorsione 4-neighbor non va bene

```forth
: PAINT-REC ( x y -- )
    2DUP POINT EDGE NOT IF
        2DUP PLOT
        2DUP       1+ SWAP RECURSE   \ right
        2DUP       1- SWAP RECURSE   \ left
        2OVER 1+       RECURSE       \ down
        2OVER 1-       RECURSE       \ up
    THEN 2DROP ;
```

Corretto ma inutilizzabile: su un'area 100x100 la ricorsione puo' andare
10000 livelli in profondita'. Il vForth R-stack ha ~64 celle. Overflow immediato.

## Algoritmo scelto: Scanline Span Fill con stack esplicito

Metodo standard (Smith, 1979). R-stack a profondita' costante; stack esplicito
O(altezza_schermo) nel caso peggiore.

### Idea chiave

Si lavora per **campate** (span): una intera riga orizzontale di pixel colorabili
contigui. Per ogni campata dipinta, si cercano le sotto-campate adiacenti nelle
righe sopra/sotto, e si premi UN seme per ciascuna nello stack esplicito.

```
               seme
                |
riga x: ########|#######    <- trovo tutta la campata [yl..yr], la dipingo
riga x-1:  AAAA BBB CCC     <- 3 sotto-campate -> 3 semi nello stack esplicito
riga x+1: DDDDDDD EEE       <- 2 sotto-campate -> 2 semi
```

Stack esplicito: al piu' 2 x altezza_schermo voci (una per campate sopra,
una per quelle sotto, per ogni riga). Per 256 righe = ~512 voci.

### Pseudocodice

```
PAINT ( x y -- )
  EXPLICIT-STACK-INIT
  x y PUSH-SEED

  BEGIN STACK-EMPTY? 0= WHILE
    POP-SEED           ( x y )
    2DUP POINT EDGE NOT IF
      \ 1. trova la campata [yl..yr] che contiene y a riga x
      scan-left   ( x y -> yl )
      scan-right  ( x y -> yr )
      \ 2. dipinge l'intera campata
      yl yr: PLOT(x, *) per ogni y in [yl..yr]
      \ 3. per riga x-1 e x+1: cerca sotto-campate in [yl..yr]
      \    e premi UN seme per ogni sotto-campata trovata
      FOR x' IN (x-1, x+1):
        scanning := false
        FOR y = yl TO yr:
          IF POINT(x',y) non-edge AND non-painted:
            IF NOT scanning: PUSH-SEED(x', y) ; scanning := true
          ELSE:
            scanning := false
    ELSE 2DROP THEN
  REPEAT
```

## Implementazione in vForth

### Stack esplicito: dove metterlo

Opzione scelta: **array nel dizionario** (semplice, indirizzo fisso):

```forth
CREATE PAINT-STACK  1024 ALLOT   \ 256 voci x (x:1cell + y:1cell) = 512 celle = 1024 byte
VARIABLE PAINT-SP                \ stack pointer (indice in celle)
```

Nota: x e' 0..255 (1 byte) ma y e' 0..639 per L24 (10 bit), quindi servono 2 celle
per voce (x in 1 cella, y in 1 cella). 256 voci x 4 byte = 1 KB.

In caso di overflow (PAINT-SP >= 256): omettere silenziosamente il push, oppure
segnalare con `?TERMINAL`-style check (da decidere).

### Dove vive il nuovo PAINT

Rimpiazza l'attuale in `lib/GRAPHICS-COMMON.f` (e viene rimosso da `inc/PAINT.f`
o quel file viene aggiornato a richiamare GRAPHICS-COMMON). Il codice usa
`POINT`, `PLOT`, `EDGE` che sono gia' puntatori nella tabella `LAYER:`, quindi
funziona invariato su L1, L22 e L24.

## Domande di design aperte

1. **Dimensione stack esplicito**: 256 o 512 voci? (1KB o 2KB)
2. **Overflow stack**: silenzioso o segnalato?
3. **PAINT in GRAPHICS-COMMON o in inc/PAINT.f separato?**
4. **Coordinate vForth**: x=verticale (0..255), y=orizzontale (0..319 L22 / 0..639 L24).
   La convenzione e' gia' nella tabella LAYER: -- verificare che scan-left/right
   scorrano lungo y, e che le righe adiacenti cambino x.

## File da modificare / creare

- `lib/GRAPHICS-COMMON.f` -- rimpiazza `PAINT-HIT`, `PAINT-HIT2`, `PAINT-HITX`, `PAINT`
- `lib/GRAPHICS.f` -- stessa sostituzione (copia monolitica)
- `inc/PAINT.f` -- aggiornare o deprecare
