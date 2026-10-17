\ 17-05.f -- the Forth side of a NextBASIC listing
\ BASIC: bas2f/txt/17-time-and-motion-05.txt
\ guide: doc/basic-to-vforth/17-time-and-motion.md
\ written by util/guide-forth.py: edit the guide, not this file
\
\   20 REG 98,0: REG 97,0
\   50 FOR x=0 TO 6
\   60 READ m,l
\   70 REG 96,m: REG 96,l
\   80 NEXT x
\   90 REG 97,0
\   100 REG 98,%@11000000
\   1000 DATA 128+(45*2),0
\   1010 DATA 64,16,65,BIN 11100000
\   1020 DATA 128+(45*2),100
\   1030 DATA 64,16,65,BIN 00000000
\   1040 DATA 128+1,128

\ --- the translation

\ 17-time-and-motion.md:507
\ no-test in the guide: it waits for keys, never ends or
\ needs hardware the emulator lacks
NEEDS COPPER
: SKY  ( -- )
    COP-STOP
      0 45 COP-WAIT   16 $40 COP-MOVE  %11100000 $41 COP-MOVE
    100 45 COP-WAIT   16 $40 COP-MOVE  %00000000 $41 COP-MOVE
    COP-HALT  COP-START ;
