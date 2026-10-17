\ 17-03c.f -- the Forth side of a NextBASIC listing
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

\ 17-time-and-motion.md:440
: HIT?  ( x1 y1 x2 y2 -- flag )
    ROT - ABS 16 < >R  - ABS 16 < R> AND ;
10 10 20 25 HIT? .              \ => -1
10 10 30 10 HIT? .              \ => 0
