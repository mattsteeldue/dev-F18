\ 17-03b.f -- the Forth side of a NextBASIC listing
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

\ --- the translation

\ 17-time-and-motion.md:426
\ no-test in the guide: it waits for keys, never ends or
\ needs hardware the emulator lacks
: MOVE-ALL  ( -- )
    1FRAME
    SPRITE 0 SPRITE-UPDATE  \ ... one per sprite
    ;
