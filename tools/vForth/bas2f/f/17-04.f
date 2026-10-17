\ 17-04.f -- the Forth side of a NextBASIC listing
\ BASIC: bas2f/txt/17-time-and-motion-04.txt
\ guide: doc/basic-to-vforth/17-time-and-motion.md
\ written by util/guide-forth.py: edit the guide, not this file
\
\   30 FOR %x=0 TO 255
\   40 LAYER AT %x,%0
\   50 NEXT %x
\   60 LAYER AT 0,0

\ --- the translation

\ 17-time-and-motion.md:478
\ no-test in the guide: it waits for keys, never ends or
\ needs hardware the emulator lacks
: ROLL-L2  ( -- )
    256 0 DO  I $16 REG!  1FRAME  LOOP
    0 $16 REG! ;
