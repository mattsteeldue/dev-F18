\ 16-03.f -- the Forth side of a NextBASIC listing
\ BASIC: bas2f/txt/16-graphics-03.txt
\ guide: doc/basic-to-vforth/16-graphics.md
\ written by util/guide-forth.py: edit the guide, not this file
\
\   10 LAYER 1,1: BORDER 0: PAPER 0: CLS
\   20 x1=0: y1=0: c=1
\   30 FOR r=0 TO 9
\   40   x2=INT (RND*256): y2=INT (RND*192)
\   50   DRAW INK c;x2-x1,y2-y1
\   60   x1=x2: y1=y2
\   70   c=c+1: IF c=8 THEN c=1
\   80 NEXT r
\   90 PAUSE 0: LAYER 1,2

\ --- words defined earlier in the guide

\ 16-graphics.md:77
\ no-test in the guide: it waits for keys, never ends or
\ needs hardware the emulator lacks
NEEDS VALUE
NEEDS TO
0 VALUE PEN-ROW  0 VALUE PEN-COL
: MOVE-TO  ( row col -- )  TO PEN-COL  TO PEN-ROW ;
: LINE-TO  ( row col -- )  2DUP PEN-ROW PEN-COL DRAW-LINE  MOVE-TO ;
: LINE-BY  ( drow dcol -- )  PEN-COL +  SWAP PEN-ROW +  SWAP LINE-TO ;
75 0 MOVE-TO  35 80 LINE-BY     \ PLOT 0,100: DRAW 80,-35 (Layer 0)

\ --- the translation

\ 16-graphics.md:303
\ no-test in the guide: it waits for keys, never ends or
\ needs hardware the emulator lacks
NEEDS RND
: SCRIBBLE  ( -- )
    LAYER11  0 .BORDER 0 .PAPER CLS
    0 0 MOVE-TO
    10 0 DO
        I 7 MOD 1+ .INK
        192 RND  256 RND  LINE-TO
    LOOP
    KEY DROP  LAYER12 ;
