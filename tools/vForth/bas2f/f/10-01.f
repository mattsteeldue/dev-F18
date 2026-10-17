\ 10-01.f -- the Forth side of a NextBASIC listing
\ BASIC: bas2f/txt/10-random-numbers-01.txt
\ guide: doc/basic-to-vforth/10-random-numbers.md
\ written by util/guide-forth.py: edit the guide, not this file
\
\   10 FOR n=1 TO 2
\   20   PRINT 1+RND (6);" ";
\   30 NEXT n

\ --- words defined earlier in the guide

\ 10-random-numbers.md:23
NEEDS RND
NEEDS WITHIN
: DICE  ( -- n )  6 RND 1+ ;
DICE 1 7 WITHIN .               \ => -1

\ --- the translation

\ 10-random-numbers.md:119
: THROW  ( -- )  DICE .  DICE . ;
1 RANDOMIZE
THROW                           \ => 1 2
THROW                           \ => 6 4
