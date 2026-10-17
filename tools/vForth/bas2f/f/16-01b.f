\ 16-01b.f -- the Forth side of a NextBASIC listing
\ BASIC: bas2f/txt/16-graphics-01.txt
\ guide: doc/basic-to-vforth/16-graphics.md
\ written by util/guide-forth.py: edit the guide, not this file
\
\   10 FOR n=0 TO 255
\   20   PLOT n,80*SQR (n/64)
\   30 NEXT n

\ --- the translation

\ 16-graphics.md:231
\ no-test in the guide: it waits for keys, never ends or
\ needs hardware the emulator lacks
: CURVE  ( -- )
    256 0 DO  175 I 100 * SQRT -  I PLOT  LOOP ;
