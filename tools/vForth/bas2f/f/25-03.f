\ 25-03.f -- the Forth side of a NextBASIC listing
\ BASIC: bas2f/txt/25-using-machine-code-03.txt
\ guide: doc/basic-to-vforth/25-using-machine-code.md
\ written by util/guide-forth.py: edit the guide, not this file
\
\   10 CLEAR 65267
\   20 LET a=65268
\   30 FOR n=0 TO 6: READ b: POKE a+n,b: NEXT n
\   40 PRINT USR (a,12*256+11)
\   50 DATA 80,89,237,48,66,75,201

\ --- the translation

\ 25-using-machine-code.md:65
NEEDS ASSEMBLER
CODE TIMES  ( u1 u2 -- u )
    exx
    pop hl|  ld e'| l|
    pop hl|  ld d'| l|
    mul
    push de|
    exx
    NEXT
C;
12 11 TIMES .                   \ => 132
