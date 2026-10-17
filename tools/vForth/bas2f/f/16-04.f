\ 16-04.f -- the Forth side of a NextBASIC listing
\ BASIC: bas2f/txt/16-graphics-04.txt
\ guide: doc/basic-to-vforth/16-graphics.md
\ written by util/guide-forth.py: edit the guide, not this file
\
\   10 PLOT 0,0: DRAW OVER 1;255,175
\   20 PAUSE 0
\   30 PLOT 0,0: DRAW OVER 1;255,175

\ --- words defined earlier in the guide

\ 16-graphics.md:142
\ no-test in the guide: it waits for keys, never ends or
\ needs hardware the emulator lacks
: XLINE  ( row2 col2 row1 col1 -- )
    ['] L0-XOR IS PLOTOP  DRAW-LINE  ['] L0-SET IS PLOTOP ;

\ --- the translation

\ 16-graphics.md:330
\ no-test in the guide: it waits for keys, never ends or
\ needs hardware the emulator lacks
: TRACE  ( -- )
    0 255 175 0 XLINE  KEY DROP  0 255 175 0 XLINE ;
