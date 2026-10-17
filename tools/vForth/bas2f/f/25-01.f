\ 25-01.f -- the Forth side of a NextBASIC listing
\ BASIC: bas2f/txt/25-using-machine-code-01.txt
\ guide: doc/basic-to-vforth/25-using-machine-code.md
\ written by util/guide-forth.py: edit the guide, not this file
\
\   10 CLEAR 65267
\   20 LET a=65268
\   30 FOR n=0 TO 3: READ b: POKE a+n,b: NEXT n
\   40 PRINT USR a
\   50 DATA 1,99,0,201

\ --- the translation

\ 25-using-machine-code.md:26
CODE NN99  ( -- n )
    $21 C, 99 ,                 \ ld hl,99
    $E5 C,                      \ push hl
    $DD C, $E9 C,               \ jp (ix)
    SMUDGE
NN99 .                          \ => 99

\ 25-using-machine-code.md:90
NEEDS CALL#
CREATE MC  1 C, 99 C, 0 C, 201 C,     \ ld bc,99 : ret
0 MC CALL# .                    \ => 99
