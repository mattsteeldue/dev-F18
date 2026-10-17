\ 16-01.f -- the Forth side of a NextBASIC listing
\ BASIC: bas2f/txt/16-graphics-01.txt
\ guide: doc/basic-to-vforth/16-graphics.md
\ written by util/guide-forth.py: edit the guide, not this file
\
\   10 FOR n=0 TO 255
\   20   PLOT n,80*SQR (n/64)
\   30 NEXT n

\ --- the translation

\ 16-graphics.md:225
NEEDS SQRT
64 100 * SQRT .                 \ => 80
