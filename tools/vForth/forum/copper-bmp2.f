NEEDS SPLIT
needs binary 
needs j
NEEDS VALUE    
NEEDS TO
NEEDS CASE
needs layer2
needs flip
NEEDS INTERRUPT
needs copper

0 value schiebe
0 value schiebe1
0 value schiebe2
0 value lire
0 value lire1
0 value lire2

: gehe
cop-stop
HEX
00   00    cop-wait 
schiebe lire + to schiebe schiebe   17    cop-MOVE 
40 0f    cop-wait 
schiebe1 lire1 + to schiebe1 schiebe1   17 cop-MOVE 
80 1e cop-wait 
schiebe2 lire2 + to schiebe2 schiebe2   17 cop-MOVE 
cop-halt ;

hex 5c08 constant last-k decimal
: keypress ( — c )
  0 last-k c!
  begin last-k c@ until
  last-k c@
;

: starte
case
  [char] a of isr-on   endof
  [char] d of isr-off  endof
  [char] e of -1 to lire  -2 to lire1 -3 to lire2 endof
  [char] q of  1 to lire   2 to lire1  3 to lire2 endof
endcase 
;

: start
  begin
  keypress
  starte
?terminal until ;

0 variable fh-BMP
HEX 12 reg@ 2* CONSTANT Layer2-Base-Page  \ 8K Base page for Layer 2
DECIMAL
: LOAD-BMP< ( a -- )  \ a is a counted z-string address, the kind created by ,"
    1+ 0 01 f_open 41 ?error fh-BMP !
    PAD 14 fh-BMP @ f_read swap 14 - or 46 ?error \ read error
    PAD 10 + 2@ swap fh-BMP @ f_seek 45 ?error  \ skip header
    6 0 DO
        5 I - LAYER2-BASE-PAGE + MMU7!  \ fit the correct page at MMU7
        32 0 DO
            31 I - FLIP [ HEX ] E000 OR [ DECIMAL ] \ destination address
            256 fh-BMP @ f_read 46 ?error drop \ ignore number of byte read
        LOOP
    LOOP
    fh-BMP @ f_close 42 ?error
;

: ISR-TEST
  23672 ( FRAMES ) @ 3 AND 0= IF
    gehe cop-start
  endif
;

INT-OFF
' ISR-TEST INT-W !
\ isr-on 
\ isr-off

create bmpname ," /fth/testbild1.bmp"
create filename ," C:/demos/bmp256converts/bitmaps/future.bmp"

: los
  layer2
  filename LOAD-BMP< 
  -1 to lire
  -2 to lire1
  -3 to lire2
  start ;

