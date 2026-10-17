\ 03-08.f -- the Forth side of a NextBASIC listing
\ BASIC: bas2f/txt/03-looping-08.txt
\ guide: doc/basic-to-vforth/03-looping.md
\ written by util/guide-forth.py: edit the guide, not this file
\
\   10 REPEAT
\   20   PRINT "Hello ";
\   30 REPEAT UNTIL 0

\ --- the translation

\ 03-looping.md:356
\ no-test in the guide: it waits for keys, never ends or
\ needs hardware the emulator lacks
: HELLO  ( -- )
    BEGIN
        ." Hello "
        ?TERMINAL
    UNTIL ;
