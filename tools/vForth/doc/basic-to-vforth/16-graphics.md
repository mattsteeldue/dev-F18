# Chapter 16 - Graphics

[From NextBASIC to vForth](README.md)

Manual: Chapter 16, pp. 113-120.

## In short

The drawing statements carry over almost one for one: `PLOT`, `CIRCLE`
and `POINT` keep their names, `DRAW` becomes `DRAW-LINE`, and there is
a `PAINT` that BASIC does not have. They live in a library,
`NEEDS GRAPHICS`, which works on every layer of
[Chapter 15](15-colours.md). Three things change, and they cause most
of the surprises: the first coordinate is the row, not the column;
the origin is always the top left corner; there is no `PLOT` position,
so a line is given both ends. Colour items inside a statement become
a value, `ATTRIB`, set before drawing. `LAYER ERASE`, `LAYER CLEAR`,
the arcs of `DRAW` and the `TILE` commands have no words.

## What changes

**Graphics is a library.** `NEEDS GRAPHICS` loads the drawing words
for all six layers at once, and sets them up for the layer the screen
is in. From then on `LAYER0`, `LAYER10`, `LAYER11`, `LAYER12`,
`LAYER13` and `LAYER2` change the layer *and* point every drawing word
at the code for that layer. A program that uses only one layer can
load less: `NEEDS LAYER11-GRAPHICS` (or any other layer's name) loads
the common part and the code of that layer only, and switches to it.
The library also redefines `.INK`, `.PAPER` and the other colour words
of Chapter 15, so that they update the drawing colour as well.
`0 GRAPHICS` goes back to `LAYER12` and takes the library out of the
dictionary.

**The row comes first.** In the library the first coordinate, called
`x`, is the *vertical* one, counted from the top, and the second, `y`,
the horizontal one, counted from the left. Both start at 0. To avoid
mixing the two conventions, this chapter calls them row and column:

<!-- no-test -->
```forth
NEEDS GRAPHICS
LAYER11
96 128 PLOT                     \ row 96, column 128: the centre
```

**The origin is always at the top left.** BASIC puts it at the bottom
left on Layer 0, with 176 rows of pixels (0 to 175) above the lower
screen, and at the top left on the other layers. vForth has no lower
screen, so Layer 0 has 192 rows like the others, and row 0 is always
the top. A `PLOT bx,by` of a Layer 0 program becomes:

```forth
: B>XY  ( bx by -- row col )  175 SWAP - SWAP ;
10 20 B>XY SWAP . .             \ => 155 10
```

On the other layers the conversion is only a `SWAP`. The good side is
that a vForth drawing does not turn upside down when the layer
changes, as the manual shows that a BASIC one does. Only the size of
the screen changes, and the library keeps it in two values: `V-RANGE`
rows and `H-RANGE` columns (512 on `LAYER12`, 128 and 96 on `LAYER10`).

**There is no `PLOT` position.** `DRAW x,y` of BASIC starts where the
last statement left off and moves *by* `x`,`y`. `DRAW-LINE` takes the
two ends, and the end comes first:

<!-- no-test -->
```forth
191 255 0 0 DRAW-LINE           \ from the top left corner (0,0)
                                \ to the bottom right (191,255)
```

A program that draws like a pen keeps the last point in two values of
its own. Then the BASIC habit of relative steps is three short words:

<!-- no-test -->
```forth
NEEDS VALUE
NEEDS TO
0 VALUE PEN-ROW  0 VALUE PEN-COL
: MOVE-TO  ( row col -- )  TO PEN-COL  TO PEN-ROW ;
: LINE-TO  ( row col -- )  2DUP PEN-ROW PEN-COL DRAW-LINE  MOVE-TO ;
: LINE-BY  ( drow dcol -- )  PEN-COL +  SWAP PEN-ROW +  SWAP LINE-TO ;
75 0 MOVE-TO  35 80 LINE-BY     \ PLOT 0,100: DRAW 80,-35 (Layer 0)
```

The `-35` of BASIC goes *down* the Layer 0 screen, so it becomes `35`
rows: in vForth a positive row step always goes down.

**Points off the screen are ignored.** BASIC stops with an error on
Layer 0 and draws off the screen elsewhere. vForth does neither: on
every layer `PLOT` checks the point with `COORD-CHECK` and skips it in
silence if it is outside. A line or a circle that leaves the screen is
drawn up to the edge, with no error. The same check is there for you:
`row col COORD-CHECK` leaves a flag above the two numbers.

**The colour is a value, not an item.** `PLOT INK 2;x,y` has no
form: set the colour first, and every drawing word uses it until you
change it. The colour is the value `ATTRIB`, and what it means depends
on the layer. On the layers with attributes (`LAYER0`, `LAYER11`,
`LAYER13`) it is a whole attribute byte, paper and ink as in Chapter 15,
and each pixel drawn writes it into its cell: paper included, not the
ink only, as BASIC does unless told otherwise. On `LAYER10` and
`LAYER2` it is the palette index of the pixel, 0 to 255. With the
library loaded, `.INK` and `.PAPER` change `ATTRIB` too, so either way
works:

<!-- no-test -->
```forth
LAYER11
2 .INK  6 .PAPER                \ red on yellow, for text and pixels
1 6 8 * + TO ATTRIB             \ blue on yellow, for pixels only
```

**`POINT` returns the pixel, not a flag.** On the layers with one bit
per pixel it returns 128 for a pixel that is set and 0 for one that is
not, where BASIC returns 1 and 0. On `LAYER10` and `LAYER2` it returns
the palette index, as `POINT ... TO` does in BASIC, and -1 for a point
off the screen. There is no `TO` form: `POINT` is an ordinary word
that leaves its result on the stack, on every layer.

<!-- no-test -->
```forth
LAYER0 CLS
175 0 POINT .  175 0 PLOT  175 0 POINT .
```

```text
0 128
```

If a program wants BASIC's 0 and 1, `0= 0= 1 AND` makes them, and
`0= 0=` alone gives a Forth flag.

**`OVER 1` and `INVERSE 1` are words, not items.** `PLOT OVER 1` is
`XPLOT`: it flips the pixel. For a whole line, the library lets you
change what `PLOT` does to the byte of the screen: it calls the
deferred word `PLOTOP`, normally `L0-SET` (OR), and `L0-XOR` makes it
flip. `DRAW OVER 1` becomes:

<!-- no-test -->
```forth
: XLINE  ( row2 col2 row1 col1 -- )
    ['] L0-XOR IS PLOTOP  DRAW-LINE  ['] L0-SET IS PLOTOP ;
```

Draw the same `XLINE` twice and it is gone, writing or no writing
under it, just as the manual describes. (On the layers with attributes
the cells it crossed keep the colour of `ATTRIB`, as in BASIC they keep
the ink.) The manual's warning holds:
draw it again with the same four numbers, in the same order, or a few
pixels stay. `PLOT INVERSE 1`, which clears the pixel, is a third
operator. `NEEDS GRAPHICS` has it as `L0-RES`; with a one-layer
module, write it:

```forth
NEEDS INVERT
: UNSET  ( pattern byte -- byte' )  SWAP INVERT AND ;
128 255 UNSET .                 \ => 127
```

and `' UNSET IS PLOTOP` before drawing, `' L0-SET IS PLOTOP` after.
`PLOTOP` works on the layers with one bit per pixel (`LAYER0`,
`LAYER11`, `LAYER12`, `LAYER13`). On `LAYER10` and `LAYER2` there is
nothing to combine: drawing with the paper colour in `ATTRIB` clears
a pixel, and `XPLOT` inverts its palette index.

**`PAINT` fills an area.** NextBASIC has no fill command, as the
manual says. vForth has one: `NEEDS PAINT`, after the graphics library,
and `row col PAINT` fills the region around that point with `ATTRIB`.
On the layers with one bit per pixel the region ends at any pixel that
is set. On `LAYER10` and `LAYER2` it ends at pixels of the `ATTRIB`
colour, so the outline must be drawn in the colour you fill with:

<!-- no-test -->
```forth
NEEDS PAINT
LAYER2  CLS
224 TO ATTRIB                   \ red
96 128 40 CIRCLE  96 128 PAINT
```

**`CIRCLE` on HiRes.** `row col r CIRCLE` draws the whole circle, as in
BASIC. On `LAYER12`, where a pixel is half as wide as it is tall, `r`
is counted in columns and the library halves it in the vertical
direction, so the circle comes out round.

## Correspondence table

| NextBASIC | vForth | Note |
|---|---|---|
| (graphics always there) | `NEEDS GRAPHICS` | Or `NEEDS LAYER11-GRAPHICS` etc., one layer only. |
| `LAYER 0`, `LAYER 1,n`, `LAYER 2,1` | `LAYER0`, `LAYER10` ... `LAYER13`, `LAYER2` | With the library loaded, they also switch the drawing words. |
| `PLOT x,y` (Layer 0) | `175 y - x PLOT` | Row first, from the top. `B>XY` above. |
| `PLOT x,y` (other layers) | `y x PLOT` | |
| `DRAW x,y` | `row2 col2 row1 col1 DRAW-LINE` | Both ends. For relative steps, `LINE-BY` above. |
| `DRAW x,y,a` | - | No arcs. See "No equivalent". |
| `CIRCLE x,y,r` | `row col r CIRCLE` | |
| `POINT (x,y)` | `row col POINT` | 128 or 0, not 1 or 0. |
| `POINT x,y TO v` | `row col POINT` | Palette index on `LAYER10`, `LAYER2`. |
| `PLOT INK c;...` | `c .INK` or `b TO ATTRIB` before | Lasts until changed. |
| `PLOT OVER 1;x,y` | `row col XPLOT` | |
| `DRAW OVER 1;...` | `XLINE` above | `PLOTOP` set to `L0-XOR`. |
| `PLOT INVERSE 1;...` | `' L0-RES IS PLOTOP` | `UNSET` above with one-layer modules. |
| errors off the screen | none | `PLOT` skips the point. `COORD-CHECK` tests it. |
| screen size | `V-RANGE`, `H-RANGE` | Rows and columns of the current layer. |
| (no fill command) | `row col PAINT` | `NEEDS PAINT`. |
| `LAYER ERASE x1,y1,x2,y2,c` | `FILL-RECT` below | With `PLOT`, so slower. |
| `LAYER DIM x1,y1,x2,y2` | `CLIP-L2` below | Registers `$1C` and `$18`; `$1A` for Layers 0 and 1. |
| `LAYER CLEAR` | - | |
| stipple UDGs | UDGs as in Chapter 13 | |
| `TILE`, `TILE BANK`, `TILE DIM` | - | Layer 3 tilemaps are another thing: tutorial `058`. |
| Layer 2 at 320x256 and 640x256 | `NEEDS LAYER22-GRAPHICS`, `NEEDS LAYER24-GRAPHICS` | BASIC has no statements for them. 640x256 is still experimental. |

## Side by side

**A parabola.** The manual's graph of `SQR`, on Layer 0.

```
10 FOR n=0 TO 255
20   PLOT n,80*SQR (n/64)
30 NEXT n
```

```forth
NEEDS SQRT
64 100 * SQRT .                 \ => 80
```

<!-- no-test -->
```forth
: CURVE  ( -- )
    256 0 DO  175 I 100 * SQRT -  I PLOT  LOOP ;
```

`SQRT` works on whole numbers, and `n/64` is a fraction. The way out
is a line of algebra: `80*SQR(n/64)` is `10*SQR(n)`, which is
`SQR(100*n)`, and `100*n` is whole. That is the integer habit of
[Chapter 9](09-mathematical-functions.md): rearrange the formula
until the fraction disappears. `175 ... -` turns the BASIC height into
a row. The same `CURVE` on `LAYER12` draws the same curve, the right
way up, in the left half of the screen.

**A sine wave.** The manual's other graph:

```
10 FOR n=0 TO 255
20   PLOT n,88+80*SIN (n/128*PI)
30 NEXT n
```

Chapter 9 took sines from a table. A wave can do without one: a point
that turns round a circle by a small step at a time has the sine as
its height, and each step needs only two multiplications. Here a step
is 1/256 of a turn, and 201/8192 is that angle in radians:

```forth
NEEDS VALUE
NEEDS TO
NEEDS +TO
0 VALUE SINE  0 VALUE COSINE
: START-WAVE  ( amplitude -- )  100 * TO COSINE  0 TO SINE ;
: TURN  ( -- )
    COSINE 201 8192 */ +TO SINE
    SINE 201 8192 */ NEGATE +TO COSINE ;
: TURNS  ( n -- )  0 ?DO  TURN  LOOP ;
80 START-WAVE  64 TURNS  SINE 100 / .   \ => 80
64 TURNS  SINE 100 / .          \ => 0
```

<!-- no-test -->
```forth
: WAVE  ( -- )
    80 START-WAVE
    256 0 DO  87 SINE 100 / -  I PLOT  TURN  LOOP ;
```

A quarter of the way round (64 steps) the height is the full 80, and
halfway it is back to 0. `SINE` and `COSINE` are kept 100 times larger
than the pixels so that the small steps do not vanish in the
integer division; `100 /` brings them back. The new `SINE` is used at
once to update `COSINE`: that order is what keeps the circle closed,
turn after turn. The heights are within two pixels of the real sine,
and no floating point is loaded.

**Random lines, in colour.** A simplified version of the manual's
program, on one layer: ten lines, each starting where the last one
ended.

```
10 LAYER 1,1: BORDER 0: PAPER 0: CLS
20 x1=0: y1=0: c=1
30 FOR r=0 TO 9
40   x2=INT (RND*256): y2=INT (RND*192)
50   DRAW INK c;x2-x1,y2-y1
60   x1=x2: y1=y2
70   c=c+1: IF c=8 THEN c=1
80 NEXT r
90 PAUSE 0: LAYER 1,2
```

<!-- no-test -->
```forth
NEEDS RND
: SCRIBBLE  ( -- )
    LAYER11  0 .BORDER 0 .PAPER CLS
    0 0 MOVE-TO
    10 0 DO
        I 7 MOD 1+ .INK
        192 RND  256 RND  LINE-TO
    LOOP
    KEY DROP  LAYER12 ;
```

`MOVE-TO` and `LINE-TO` are the pen words above, and `LINE-TO` takes
the end point itself: the BASIC `x2-x1` is there only because `DRAW`
wants a step. `I 7 MOD 1+` counts 1 to 7 and again, without the `IF`.
The lines grow thicker in colour as they cross the cells, as the
manual shows: that is the attribute clash, the same on both sides.

**A line that leaves no trace.** Draw it, and draw it again.

```
10 PLOT 0,0: DRAW OVER 1;255,175
20 PAUSE 0
30 PLOT 0,0: DRAW OVER 1;255,175
```

<!-- no-test -->
```forth
: TRACE  ( -- )
    0 255 175 0 XLINE  KEY DROP  0 255 175 0 XLINE ;
```

BASIC's bottom left corner is row 175, column 0; its top right corner
is row 0, column 255.

**Filling a rectangle.** `LAYER ERASE` fills on LoRes and Layer 2
only. Horizontal lines do it on every layer, slower:

<!-- no-test -->
```forth
: FILL-RECT  ( row1 col1 row2 col2 -- )
    ROT 2SWAP 1+ SWAP           \ col2 col1 row2+1 row1
    ?DO  I 2 PICK  I 3 PICK  DRAW-LINE  LOOP
    2DROP ;
LAYER2  28 TO ATTRIB  120 100 130 140 FILL-RECT
```

The colour is `ATTRIB`, as for every drawing word; 28 is a green on
Layer 2. For speed on Layer 2, the framebuffer can be filled a row at
a time with `FILL` once its 8K page is mapped through `MMU7!`
(Chapter 23), or with the DMA of tutorial `054`.

**A clipping window.** `LAYER DIM` on Layer 2 writes four registers,
and so does the Forth version:

```forth
: CLIP-L2  ( row1 col1 row2 col2 -- )
    ROT SWAP                    \ row1 row2 col1 col2
    1 $1C REG!                  \ start again from the first one
    SWAP $18 REG!  $18 REG!     \ columns: left, right
    SWAP $18 REG!  $18 REG! ;   \ rows: top, bottom
0 0 191 255 CLIP-L2
```

The four writes go to the same register, `$18`, one after the other;
`$1C` with bit 0 set makes the next write the first. For Layers 0 and
1 the register is `$1A`, reset with bit 2 (`4 $1C REG!`); the sprites
have `$19` and bit 1. The window is in the order of the registers:
columns first.

## No equivalent

- **Arcs (`DRAW x,y,a`).** No word draws part of a circle. The turning
  point of `TURN` above draws one: start it at the right angle, and
  stop it after the right number of steps.
- **`LAYER ERASE`** as a single fast word. `FILL-RECT` above is the
  slow form; the fast one depends on the layer.
- **`LAYER CLEAR`.** Layer, palettes, clipping windows and the order of
  the layers are separate registers (Chapters 15 and 22); there is no
  word that resets them all.
- **`TILE`, `TILE BANK`, `TILE DIM`**: drawing a Layer 2 or LoRes
  screen from a map of tiles. vForth has the hardware tilemap of
  Layer 3 instead (`lib/layer3.f`, tutorial `058`), which BASIC does
  not reach directly.
- **The `PLOT` position**, and with it `DRAW` after `CIRCLE`. The pen
  words above do the job when needed.
- **Colour items inside the statement.** `ATTRIB` and the colour words
  are set before.

## Further reading

- Tutorial `036` -- `PLOT`, `DRAW-LINE`, `CIRCLE`, `XPLOT` on the ULA
  screen.
- Tutorial `037` -- the same on Layer 2, 256 colours.
- Tutorial `038` -- all six layers, `POINT`, `COORD-CHECK`, `PAINT`.
- Tutorial `052` -- loading one layer only: `LAYER11-GRAPHICS` and the
  others.
- Tutorial `054` -- the DMA, for fast fills and copies.
- Tutorial `058` -- the Layer 3 tilemap.
- Tutorial `065` -- a drawing made with a sine table.
- `HELP GRAPHICS`, `HELP PLOT`, `HELP DRAW-LINE`, `HELP CIRCLE`,
  `HELP XPLOT`, `HELP ATTRIB`, `HELP COORD-CHECK`, `HELP H-RANGE`,
  `HELP LAYER22-GRAPHICS`.
- Chapter 22 -- the Next registers, clipping windows included.

<!-- nav -->
---

Previous: [Chapter 15 - Colours](15-colours.md) |
[Contents](README.md) |
Next: Chapter 17 - Time and Motion (not written yet)
