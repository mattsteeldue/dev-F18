NEEDS SPLIT
needs binary 
needs j
NEEDS VALUE    
NEEDS TO
NEEDS CASE
needs layer2
needs flip
NEEDS INTERRUPT

0 value schiebe
0 value lire
  
HEX 061 CONSTANT COP-CTRL-LO  \ Copper control Low byte
HEX 062 CONSTANT COP-CTRL-HI  \ Copper control High byte
HEX 063 CONSTANT COP-WRITE    \ Copper data 16-bit write

HEX
: UPLOAD ( n -- )
SPLIT
COP-WRITE REG!
COP-WRITE REG!
;

: STOP  ( -- )
0 COP-CTRL-LO REG!
0 COP-CTRL-HI REG!
;

: COSTART ( -- )
0  COP-CTRL-LO REG!
0C0 COP-CTRL-HI REG! 
;

HEX
: WAIT ( v h -- )   \ v-vertical (0-311) h-horizontal (0-55)
3F AND 2* FLIP SWAP \ compose horizontal part
1FF AND             \ compose vertical part
OR                  \ merge
8000 OR             \ set bit-15.
UPLOAD 
;
    
: MOVE ( v r -- )   \ v-alue and r-egister (0-127)
7F  AND  FLIP SWAP  \ force register 0-127
0FF AND             \ force value 0-255
OR                  \ merge
UPLOAD              
;

: HALT ( -- )       
0FFFF UPLOAD
;

: gehe
STOP
HEX
00   00    WAIT 
schiebe lire + to schiebe schiebe   16    MOVE 
60   00    WAIT 
00   16    MOVE
HALT
;  
  
hex 5c08 constant last-k decimal
: keypress ( — c )
  0 last-k c!
  begin last-k c@ until
  last-k c@
;

: starte
case
   97 of isr-on  endof
  100 of isr-off  endof
  101 of -1 to lire  endof
  113 of 1 to lire  endof
endcase 
;

: start
  begin
  keypress
  starte
?terminal until ;

0 variable fh-BMP
DECIMAL
: LOAD-BMP<  
    1+ 0 01 f_open 41 ?error fh-BMP !
    1162 0 fh-bmp @ f_seek 45 ?error  
    6 0 DO
        5 I - 18 + MMU7!  
        32 0 DO
            31 I - FLIP [ HEX ] E000 OR [ DECIMAL ] 
            256 fh-BMP @ f_read 46 ?error drop 
        LOOP
    LOOP
    fh-BMP @ f_close 42 ?error
;

: ISR-TEST
  23672 ( FRAMES ) @ 3 AND 0= IF
    gehe costart
  endif
;

ISR-OFF
' ISR-TEST ISR-W !
isr-on 
isr-off

create bmpname ," /tools/vforth/demo/bmp/critters.bmp"

: los
  layer2
  bmpname LOAD-BMP< 
  -1 to lire
  start ;


