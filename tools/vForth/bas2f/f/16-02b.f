\ 16-02b.f -- the Forth side of a NextBASIC listing
\ BASIC: bas2f/txt/16-graphics-02.txt
\ guide: doc/basic-to-vforth/16-graphics.md
\ written by util/guide-forth.py: edit the guide, not this file
\
\   10 FOR n=0 TO 255
\   20   PLOT n,88+80*SIN (n/128*PI)
\   30 NEXT n

\ --- words defined earlier in the guide

\ 16-graphics.md:257
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

\ --- the translation

\ 16-graphics.md:272
\ no-test in the guide: it waits for keys, never ends or
\ needs hardware the emulator lacks
: WAVE  ( -- )
    80 START-WAVE
    256 0 DO  87 SINE 100 / -  I PLOT  TURN  LOOP ;
