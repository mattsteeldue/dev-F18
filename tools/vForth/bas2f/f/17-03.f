\ 17-03.f -- the Forth side of a NextBASIC listing
\ BASIC: bas2f/txt/17-time-and-motion-03.txt
\ guide: doc/basic-to-vforth/17-time-and-motion.md
\ written by util/guide-forth.py: edit the guide, not this file
\
\   106 PROC initXSineMov()
\   120 FOR %a=0 TO 255
\   130 %s=%1-s
\   140 SPRITE 0,%159+a[a],%255-a,%s,1
\   141 PAUSE 3
\   145 NEXT %a
\   150 GO TO 120
\   570 DEFPROC initXSineMov()
\   580 FOR f=0 TO 319:%a[INT {f}]=%INT {159*SIN (f/159*PI)}: NEXT f
\   590 ENDPROC

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

\ 17-time-and-motion.md:28
: WAIT-FRAMES  ( n -- )  0 ?DO  1FRAME  LOOP ;
5 WAIT-FRAMES

\ --- the translation

\ 17-time-and-motion.md:401
\ no-test in the guide: it waits for keys, never ends or
\ needs hardware the emulator lacks
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
