# Chapter 17 - Time and Motion

[From NextBASIC to vForth](README.md)

Manual: Chapter 17, pp. 121-143.

## In short

The clock is the same machine underneath, reached by other means.
`PAUSE n` becomes a loop of `1FRAME`, a core word that waits for the
next frame, or `ms`, which counts milliseconds. `PAUSE 0` is `KEY`.
The frame counter is the same system variable, FRAMES, read with `@`.
`TIME` has no word, but it is two short lines. `TIME$` becomes
`IDE_RTC`, which leaves the date and the time on the stack as numbers.
There is no string to slice. The sprites are the same hardware, and
`NEEDS SPRITE` gives a small engine: fill a structure, then send it to
a slot. What the NextBASIC sprite system does by itself is left to the
program: remembering each sprite, moving it, testing collisions.
`LAYER AT` is a Next register, and the Copper has its own library,
whose instructions have names instead of numbers.

## What changes

**A pause is a loop of frames.** `1FRAME` waits for the next frame
interrupt, 50 or 60 times a second, as `PAUSE 1` does. A longer
pause is a loop:

```forth
: WAIT-FRAMES  ( n -- )  0 ?DO  1FRAME  LOOP ;
5 WAIT-FRAMES
```

`ms` waits for a number of milliseconds, up to 8191, whatever the CPU
speed and the frame rate:

```forth
NEEDS ms
100 ms
```

So `PAUSE 50` is `50 WAIT-FRAMES` or `1000 ms`. The first follows the
display: one second at 50 Hz, less at 60 Hz. The second is always a
second, but it is a busy loop that knows nothing of the display.

**A key does not cut the wait short.** Neither word looks at the
keyboard: a pause that a key can end, as `PAUSE` does, has to say so.
`KEY-SCAN` ([Chapter 14](14-more-about-print-and-input.md)) leaves 255
when no key is down:

```forth
NEEDS KEYBOARD
: PAUSE  ( n -- )
    0 ?DO  1FRAME  KEY-SCAN 255 - IF LEAVE THEN  LOOP ;
10 PAUSE
```

`PAUSE 0` waits for a key with no time limit, and that is `KEY DROP`.
`KEY` shows the cursor and takes the character. `NEEDS WAIT-KEY` gives
`WAIT-KEY`, which shows nothing and leaves the key where it is: like
BASIC, it waits for the keyboard to be free and then for a new key.

**The frame counter is the same.** FRAMES is the system variable at
23672, three bytes, counted up by the interrupt of the ROM. vForth
leaves that interrupt alone, so the counter runs just as it does under
BASIC. `@` reads its two lower bytes, which go round every 21 minutes
at 50 Hz. `TIME` as a command and as a function are two words:

```forth
: RESET-TIMER  ( -- )  0 23672 !  0 23674 C! ;
: TIMER  ( -- u )  23672 @ ;
RESET-TIMER
```

To measure a piece of program there is no need to reset anything: read
`TIMER` before and after, and subtract. The difference is right even
when the counter goes round in between, since `-` works modulo 65536.
As the manual warns, the counter stops whenever the interrupts are off:
during `BEEP`, a disk operation and so on.

**50 or 60 Hz.** Bit 2 of Next register 5 tells which:

```forth
: HZ  ( -- n )  5 REG@ 4 AND IF 60 ELSE 50 THEN ;
HZ .                            \ 50 or 60
```

`TIMER HZ /` is then the number of seconds, on either setting.

**The clock comes as numbers.** `TIME$` gives a string to slice with
`VAL`. vForth asks NextZXOS directly, and the answer arrives on the
stack: `NEEDS IDE_RTC` gives `IDE_RTC ( -- hs time date )`. The time
and the date are packed in the format of MS-DOS, the one of the file
dates on the SD card. The hours are in the top 5 bits of `time`, the
minutes in the middle 6, the seconds in the bottom 5, *halved*:

```forth
: HOURS    ( time -- h )  11 RSHIFT ;
: MINUTES  ( time -- m )  5 RSHIFT 63 AND ;
: SECONDS  ( time -- s )  31 AND 2* ;
34544 DUP HOURS .  DUP MINUTES .  SECONDS .   \ => 16 55 32
```

34544 is the 16:55:32 of the manual's example. The seconds come in
steps of two: for the exact second `NEEDS M_GETDATE` gives
`M_GETDATE ( -- date time hs f )`, where the high byte of `hs` holds the
seconds and `f` is 0 when the clock has answered. `NEEDS .NOW` gives
`.NOW`, which prints date and time as `2023-05-10 16:55`, without the
seconds. A machine with no clock module returns zeros.

**Sprites: the same hardware, a smaller library.** `NEEDS SPRITE`
gives the pieces, and the program puts them together:

- `SPRITES-ON` and `SPRITES-OFF` are `SPRITE PRINT 1` and `0`.
  `SPRITES-ON` does more: it sets the sprite palette to the identity
  (colour i is index i), the transparent colour to 227 as in BASIC,
  and writes 3 into Next register `$15`: sprites on, and over the
  border, as `SPRITE BORDER 1`. That write also resets the order of the
  layers (Chapter 22); a program that changed it sets it again after.
- A pattern is 256 bytes, put in `SPRITE-BUFFER` and sent to the
  sprite RAM with `p SPRITE-INIT`. No bank is needed: the pattern goes
  from any memory, one at a time, and there is no `SPRITE BANK`.
- `SPRITE` is not a command but a structure of 9 bytes, the one the
  library works with. Its fields are `_spriteid` (the pattern, despite
  the name), `_xcoord`, `_ycoord`, `_rotmir` (the flags) and
  `_pattern` (the palette offset, despite the name). `SPRITE s
  SPRITE-UPDATE` sends it to slot `s`:

<!-- no-test -->
```forth
NEEDS SPRITE
SPRITES-ON
152 SPRITE _xcoord !  119 SPRITE _ycoord !  0 SPRITE _spriteid !
SPRITE 0 SPRITE-UPDATE          \ SPRITE 0,152,119,0,1
```

Every `SPRITE-UPDATE` sends all the values, and always makes the
sprite visible. There is no "leave it as it was": what is not changed
in the structure is sent again as it is. The slot is the argument of
`SPRITE-UPDATE`, the pattern is a field. Mixing them up shows extra
sprites rather than an error. `s SPRITE-HIDE` makes a sprite
invisible, and `SPRITE CLEAR` is a loop:
`128 0 DO I SPRITE-HIDE LOOP`.

**The flags are the same bits.** `SPRITE-ROT`, `SPRITE-VFLIP` and
`SPRITE-HFLIP` are bits 1, 2 and 3 of the BASIC flags, ORed into
`_rotmir`:

```forth
NEEDS SPRITE
SPRITE-ROT SPRITE-HFLIP OR .    \ => 10
```

The palette offset, bits 4 to 7 of the BASIC flags, goes into the high
nibble of `_pattern`. Keep it at 0 unless you mean it: the library's
`SPRITE` starts at 0, but a structure of your own made with `ALLOT`
must be cleared with `ERASE`, or the sprite shows the wrong colours.

**The coordinates are those of BASIC.** 320 by 256, the screen
starting at 32,32, the top left corner of the sprite as its position.
`_xcoord` is a whole cell, and `SPRITE-UPDATE` sends its ninth bit.

**The sprite RAM cannot be read back**, as the manual says, and the
library keeps no copy of what it sent. The functions `SPRITE s` and
`SPRITE AT(s,c)` have no counterpart: the program knows where it put
each sprite, and keeps it in its own variables or structures.

**`LAYER AT` is a register for each layer.** BASIC moves the current
layer; vForth writes the offset register of the layer you mean:

| Layer | x | y |
|---|---|---|
| Layer 2 | `$16` | `$17` |
| ULA (Layer 0 and 1) | `$26` | `$27` |
| LoRes | `$32` | `$33` |
| tilemap (Layer 3) | `$30` (high bits `$2F`) | `$31` |

`x $16 REG!  y $17 REG!` is `LAYER AT x,y` on Layer 2, with the same
wrap-around. On Layer 2 at 320 points, the ninth bit of x goes in
`$71`.

**The Copper has a library.** `NEEDS COPPER` names the two
instructions. `v h COP-WAIT` waits for line `v` (0 to 311) and position
`h` (0 to 55); `value reg COP-MOVE` writes a value to a Next register
(0 to 127, as in BASIC). The list is written as Forth code between
`COP-STOP`, which stops the Copper and starts the list again from the
first instruction, and `COP-HALT COP-START`. `COP-START` uses the mode
that starts again at every frame, as the manual's example does with
`REG 98,%@11000000`. `COP-NOOP` is the `MOVE 0,0` of the manual, a
short delay.

**Frames from storage or from memory.** The machinery is that of
Chapters 19 and 23: `LOAD-BYTES` reads a file into memory, and a Layer 2
screen is six 8K pages, mapped one at a time with `MMU7!`. A file name
with a number in it is built by hand, since there is no `+` for
strings: see [Chapter 7](07-strings.md). To show frames kept in memory,
a program does not need to copy 48K at all: Next register `$12`
chooses the 16K bank the Layer 2 shows, and one `REG!` flips to
another screen.

## Correspondence table

| NextBASIC | vForth | Note |
|---|---|---|
| `PAUSE n` | `n WAIT-FRAMES` above | `1FRAME` repeated. No key ends it. |
| `PAUSE n`, cut short by a key | `n PAUSE` above | `NEEDS KEYBOARD`. |
| `PAUSE 0` | `KEY DROP`, or `WAIT-KEY` | `NEEDS WAIT-KEY`: no cursor, the key stays. |
| a delay in milliseconds | `n ms` | `NEEDS ms`. Up to 8191. |
| `PEEK 23672+256*PEEK 23673` | `23672 @` | Add `23674 C@` for the third byte. |
| `TIME` (command) | `RESET-TIMER` above | |
| `TIME` (function) | `TIMER` above | |
| `REG 5&@100>>2` | `5 REG@ 4 AND` | Not zero at 60 Hz. `HZ` above. |
| `TIME$` | `IDE_RTC`; `.NOW` prints | `NEEDS IDE_RTC`, `NEEDS .NOW`. Numbers, not a string. |
| `VAL TIME$(12 TO 13)` etc. | `HOURS`, `MINUTES`, `SECONDS` above | Seconds in steps of two. |
| the exact second | `M_GETDATE` | `NEEDS M_GETDATE`. High byte of `hs`. |
| `OPEN #2,"v>t$": .TIME` | `IDE_RTC` | No dot command to capture. |
| `INKEY$` | `KEY`, `KEY-SCAN` | Chapter 14. |
| `SAVE`/`LOAD ... CODE` frames | `SAVE-BYTES`, `LOAD-BYTES` | Chapters 19 and 23. |
| `BANK n COPY TO m` frames | `MMU7!` and `CMOVE`, or `n $12 REG!` | Flipping the bank shown copies nothing. |
| `BANK n LAYER x,y,w,h TO ...` | - | |
| `BANK NEW`, `BANK POKE` for a pattern | `CREATE` and `C,` | Any memory will do. |
| `SPRITE CLEAR` | `128 0 DO I SPRITE-HIDE LOOP` | |
| `SPRITE BANK b` | `p SPRITE-INIT`, one per pattern | From `SPRITE-BUFFER`. |
| `SPRITE PRINT 1`, `0` | `SPRITES-ON`, `SPRITES-OFF` | `SPRITES-ON` also sets palette, transparency, border. |
| `SPRITE BORDER n` | bit 1 of `$15` | `SPRITES-ON` sets it. |
| `SPRITE DIM x1,y1,x2,y2` | `CLIP-SPRITES` below | |
| `SPRITE s,x,y,p,f` | fields of `SPRITE`, then `SPRITE s SPRITE-UPDATE` | Always visible. `s SPRITE-HIDE` hides. |
| flags: rotate, mirrors | `SPRITE-ROT`, `SPRITE-VFLIP`, `SPRITE-HFLIP` in `_rotmir` | |
| flags: palette offset | high nibble of `_pattern` | |
| `rf`, `mx`, `my` (relative sprites, scaling) | - | |
| `SPRITE PALETTE n,i,v` | `%00100000 $43 REG!`, `i $40 REG!`, `v $41 REG!` | 8-bit value; for 9 bits, two writes to `$44`. |
| `SPRITE STOP`, `SPRITE MOVE INT`, `SPRITE RUN` | `1FRAME`, then all the `SPRITE-UPDATE`s | |
| `SPRITE CONTINUE`, `SPRITE PAUSE` | - | The program moves the sprites. |
| `SPRITE s`, `SPRITE AT(s,c)` | - | The program knows. |
| `SPRITE OVER(s1,s2)` | `HIT?` below | |
| `LAYER AT x,y` | `x $16 REG!  y $17 REG!` (Layer 2) | One register pair per layer. |
| Copper: `REG 97`, `REG 98` | `COP-STOP`, `COP-START` | `NEEDS COPPER`. |
| Copper: `REG 96,m: REG 96,l` | `v h COP-WAIT`, `value reg COP-MOVE` | |

## Side by side

**Testing the pause.** `TIME` resets the counter, and `display()` shows
it twice, read as FRAMES and as `TIME`, before and after a `PAUSE`:

```
10 INPUT "A number: ";%N
20 TIME : ;Reset timer
30 PROC display()
40 PAUSE %N
50 PROC display()
60 STOP
70 ;
100 DEFPROC display()
110 T1,T2= DPEEK 23672, TIME
120 PRINT T1,T2
130 ENDPROC
```

```forth
: DISPLAY  ( -- )  CR  23672 @ .  TIMER . ;
```

<!-- no-test -->
```forth
RESET-TIMER DISPLAY  100 WAIT-FRAMES  DISPLAY
```

```text
0 0
100 100
```

In Forth the two numbers are the same by definition, since `TIMER` is
`23672 @`. The number of frames is typed on the line, as with any word;
`INPUT` would be Chapter 14. There is no need to define the main
program: a line without loops or `IF` runs at the prompt as it is.

**Hours, minutes, seconds.** `Now()` slices `TIME$` and returns three
numbers:

```
10 T$= TIME $
20 PRINT 't$
30 PROC now() TO h,m,s
40 PRINT "It's ";h;":";m
90 STOP
100 DEFPROC Now()
110 T$= TIME $
120 PRINT 't$
130 hh= VAL (T$(12)+T$(13))
140 mi= VAL (T$(15)+T$(16))
150 ss= VAL (T$(18)+T$(19))
160 ENDPROC =hh,mi,ss
```

```forth
NEEDS IDE_RTC
: NOW  ( -- h m s )
    IDE_RTC DROP NIP
    DUP HOURS  OVER MINUTES  ROT SECONDS ;
```

`IDE_RTC` leaves three values; `DROP NIP` keeps the time only. The
three results stay on the stack, as `ENDPROC =hh,mi,ss` returns three.
To print them as `TIME$` does, with two digits each:

```forth
: .00  ( n -- )  0 <# # # #> TYPE ;
: .HMS  ( h m s -- )
    ROT .00 [CHAR] : EMIT  SWAP .00 [CHAR] : EMIT  .00 ;
16 55 32 .HMS                   \ => 16:55:32
```

`NOW .HMS` prints the time of the clock. The emulator has no
clock, so the line above gives the numbers itself.

**A sprite pattern.** The manual's spaceship is 16 `DATA` lines of 16
numbers, read with `READ` and put into a bank with `BANK POKE`. In
Forth the numbers go straight into memory as the source is read. A
row of 16 numbers is on the stack at the end of the line, and a word
stores them, the last one first:

```forth
: ROW!  ( n1 ... n16 a -- )
    15 +  16 0 DO  SWAP OVER C!  1-  LOOP  DROP ;
: ROW,  ( n1 ... n16 -- )  HERE ROW!  16 ALLOT ;
CREATE PROBE  1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 ROW,
PROBE C@ .  PROBE 15 + C@ .     \ => 1 16
```

With these the pattern reads as it does in BASIC, one row per line:

```forth
CREATE SHIP
 68  68  68  68 227 227 227 227 227 227 227 227  68  68  68  68 ROW,
 68 182 219  68 227 227 227  68  68 227 227 227  68 219 182  68 ROW,
 68  68  68  68 227 227 227  55  55 227 227 227  68  68  68  68 ROW,
182 182  68 227 227 227 227  55  55 227 227 227 227  68 182 182 ROW,
 68  68  68 227 227 227  68  68  68  68 227 227 227  68  68  68 ROW,
240  68  68 227 227 227  68 255 127  68 227 227 227  68  68 240 ROW,
227  68  68   0 227 227  68 127 127  68 227 227   0  68  68 227 ROW,
227 182 219  72   0 227 182   0  68  68 227   0  72 219 182 227 ROW,
227 182 219  72 182   0   0   0  68 182 227 182  72 219 182 227 ROW,
227 182 219  72 182  68  68   0  68  68  68 182  72 219 182 227 ROW,
227 240  68  72 182  68  68   0  68  68  68 182  72  68 240 227 ROW,
227 227 227  72 182  68 255 182 182 255  68 182  72 227 227 227 ROW,
227 227 227 227  68  68 255  68  68 255  68  68 227 227 227 227 ROW,
227 227 227 227 227  68 255 182 182 255  68 227 227 227 227 227 ROW,
227 227 227 227 227 227 236 224 236 224 227 227 227 227 227 227 ROW,
227 227 227 227 227 227 227 252 252 227 227 227 227 227 227 227 ROW,
SHIP 255 + C@ .                 \ => 227
```

The manual's second pattern, for the animation, differs from the first
in two rows only: the cannons and the flame. Copy the first and change
those rows:

```forth
CREATE SHIP2  256 ALLOT
SHIP SHIP2 256 CMOVE
 68 219 182  68 227 227 227  68  68 227 227 227  68 182 219  68
SHIP2 16 + ROW!
227 227 227 227 227 227 227 224 224 227 227 227 227 227 227 227
SHIP2 240 + ROW!
```

Then both go to the sprite RAM, as patterns 0 and 1:

<!-- no-test -->
```forth
NEEDS SPRITE
: PATTERN!  ( a p -- )  SWAP SPRITE-BUFFER 256 CMOVE  SPRITE-INIT ;
SHIP 0 PATTERN!  SHIP2 1 PATTERN!
```

There is no file to save first, and no bank to reserve. Running the
program again does not use up memory as `BANK NEW` does: the patterns
are part of the program. To keep them in a file, `SAVE-BYTES` writes
the 256 bytes as they are (Chapter 19).

**A sprite on a sine wave.** The manual's last sprite program moves
the ship from the bottom of the screen to the top along a sine, and
changes pattern at every step:

```
106 PROC initXSineMov()
120 FOR %a=0 TO 255
130 %s=%1-s
140 SPRITE 0,%159+a[a],%255-a,%s,1
141 PAUSE 3
145 NEXT %a
150 GO TO 120
570 DEFPROC initXSineMov()
580 FOR f=0 TO 319:%a[INT {f}]=%INT {159*SIN (f/159*PI)}: NEXT f
590 ENDPROC
```

[Chapter 16](16-graphics.md) drew a sine wave with `START-WAVE` and `TURN`, and needed
no table. Type those definitions first; then:

<!-- no-test -->
```forth
: FLY  ( -- )
    SPRITES-ON  159 START-WAVE
    BEGIN
        256 0 DO
            159 SINE 100 / +  SPRITE _xcoord !
            255 I -           SPRITE _ycoord !
            I 1 AND           SPRITE _spriteid !
            3 WAIT-FRAMES  SPRITE 0 SPRITE-UPDATE  TURN
        LOOP
    ?TERMINAL UNTIL
    0 SPRITE-HIDE ;
```

`I 1 AND` is `%s=%1-s`: 0, 1, 0, 1 as the loop goes on. The update
comes right after the wait, at the start of a frame, so the sprite does
not change while it is being drawn. `?TERMINAL` stops it with BREAK,
which in BASIC stops the program. The step of `TURN` is 1/256 of a
turn, so the ship draws one whole wave on its way up; the manual's step
is 1/318, a little less than a wave.

**Batching.** `SPRITE STOP ... SPRITE MOVE INT` has the same shape:
wait for the frame, then send every sprite at once.

<!-- no-test -->
```forth
: MOVE-ALL  ( -- )
    1FRAME
    SPRITE 0 SPRITE-UPDATE  \ ... one per sprite
    ;
```

A program with several sprites keeps one structure for each: `CREATE
ALIEN SPRITE-OB ALLOT  ALIEN SPRITE-OB ERASE`, then `ALIEN 3
SPRITE-UPDATE`.

**A collision test.** `SPRITE OVER(s1,s2)` compares two boxes of 16 by
16. With the positions in the program's own hands, so does this:

```forth
: HIT?  ( x1 y1 x2 y2 -- flag )
    ROT - ABS 16 < >R  - ABS 16 < R> AND ;
10 10 20 25 HIT? .              \ => -1
10 10 30 10 HIT? .              \ => 0
```

Two sprites touch when they are less than 16 points apart in both
directions. The overlap that BASIC allows is a smaller number in place
of 16. For a range of sprites, loop over their structures.

**Clipping the sprites.** `SPRITE DIM` writes four values to one
register, like `LAYER DIM` in Chapter 16, and in the order of the
hardware, which is not BASIC's:

```forth
: CLIP-SPRITES  ( x1 y1 x2 y2 -- )
    ROT SWAP                    \ x1 x2 y1 y2
    2 $1C REG!                  \ start again from the first one
    2SWAP SWAP $19 REG! $19 REG!  SWAP $19 REG! $19 REG! ;
0 0 255 191 CLIP-SPRITES
```

The window is counted inside the screen, not in the 320 by 256 of the
sprite positions, and it has no effect while the sprites are over the
border: `SPRITES-ON` puts them there. To use it, write 1 into `$15`
after `SPRITES-ON`: sprites on, under the border.

**Scrolling.** The manual rolls a Layer 2 picture to the left:

```
30 FOR %x=0 TO 255
40 LAYER AT %x,%0
50 NEXT %x
60 LAYER AT 0,0
```

<!-- no-test -->
```forth
: ROLL-L2  ( -- )
    256 0 DO  I $16 REG!  1FRAME  LOOP
    0 $16 REG! ;
```

The `1FRAME` is not in the BASIC loop. Without it the Forth loop is
over long before the picture can be seen: 256 writes to a register take
no time at all.

**The Copper.** The manual paints the top 100 lines of the screen red
with a list of numbers:

```
20 REG 98,0: REG 97,0
50 FOR x=0 TO 6
60 READ m,l
70 REG 96,m: REG 96,l
80 NEXT x
90 REG 97,0
100 REG 98,%@11000000
1000 DATA 128+(45*2),0
1010 DATA 64,16,65,BIN 11100000
1020 DATA 128+(45*2),100
1030 DATA 64,16,65,BIN 00000000
1040 DATA 128+1,128
```

<!-- no-test -->
```forth
NEEDS COPPER
: SKY  ( -- )
    COP-STOP
      0 45 COP-WAIT   16 $40 COP-MOVE  %11100000 $41 COP-MOVE
    100 45 COP-WAIT   16 $40 COP-MOVE  %00000000 $41 COP-MOVE
    COP-HALT  COP-START ;
```

The list is code, with the names of the operations: `128+(45*2)` is
written by `COP-WAIT`, which also puts the line in the right bits.
`COP-HALT` ends the list as the manual's wait for line 384 does. As in
BASIC, the list writes palette index 16 (paper and border) through
registers `$40` and `$41`. These write the palette that register `$43`
selects, and `SPRITES-ON` points it at the sprites: after it,
`0 $43 REG!` brings back the first ULA palette.

## No equivalent

- **Automatic sprite movement**: `SPRITE CONTINUE`, `SPRITE PAUSE`
  and the function `SPRITE CONTINUE s`. Limits, steps, bouncing and
  animation are the program's own loop, as in `FLY` above.
- **Relative, composite and unified sprites**, and **scaling** (`rf`,
  `mx`, `my`). They use a fifth attribute byte that the library does
  not send; the structure has an `_anchor` field, unused.
- **Reading a sprite back**: `SPRITE s`, `SPRITE AT(s,c)`.
- **`SPRITE OVER` on a range**: `HIT?` above tests two sprites, and a
  loop does the rest.
- **4-bit sprites**, which BASIC does not use either. The hardware can
  be reached with ports and registers, but the library has no words.
- **`BANK n LAYER`**, copying a rectangle between the screen and a
  bank (Chapter 23).
- **A clock string** with the seconds: `.NOW` prints without them, and
  nothing leaves the time as a string. `.HMS` above prints it.
- **`PAUSE` interrupted by a key** as a ready word: `PAUSE` above.

## Further reading

- Tutorial `032` -- `ms`, frame-synchronised loops, a stopwatch.
- Tutorial `039` -- the first sprites, with the registers written by
  hand.
- Tutorial `053` -- the sprite engine that became `NEEDS SPRITE`: slot
  and pattern, the palette offset.
- Tutorial `045` -- the Copper.
- Tutorial `046` -- loading pictures from files.
- `HELP 1FRAME`, `HELP ms`, `HELP WAIT-KEY`, `HELP KEY-SCAN`,
  `HELP M_GETDATE`, `HELP COPPER`, `HELP COP-WAIT`, `HELP COP-MOVE`,
  `HELP REG!`.
- Chapter 22 -- the Next registers, sprite ports included.
- Chapter 23 -- memory pages, for frames kept in memory.

<!-- nav -->
---

Previous: [Chapter 16 - Graphics](16-graphics.md) |
[Contents](README.md) |
Next: [Chapter 18 - Sound and Music](18-sound-and-music.md)
