\ 25-02.f -- the Forth side of a NextBASIC listing
\ BASIC: bas2f/txt/25-using-machine-code-02.txt
\ guide: doc/basic-to-vforth/25-using-machine-code.md
\ written by util/guide-forth.py: edit the guide, not this file
\
\   10 CLEAR 65267
\   20 LET a=65268
\   30 FOR n=0 TO 5: READ b: POKE a+n,b: NEXT n
\   40 PRINT USR (a,21)
\   50 DATA 96,105,41,68,77,201

\ --- the translation

\ 25-using-machine-code.md:185
CREATE TW  96 C, 105 C, 41 C, 68 C, 77 C, 201 C,
21 TW CALL# .                   \ => 42
CODE TWICE  ( n -- 2n )
    $E1 C,                      \ pop hl
    $29 C,                      \ add hl,hl
    $E5 C,                      \ push hl
    $DD C, $E9 C,               \ jp (ix)
    SMUDGE
21 TWICE .                      \ => 42
