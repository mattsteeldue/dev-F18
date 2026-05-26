needs value  
needs to 
needs +to
needs 2over  
needs dnegate
needs layers
NEEDS CASE
NEEDS INTERRUPT

\ include /fth/spriteproglayer.f
\ SPRITE-LOAD< ../../fth/sprite1.spr 
400 load

100 value wx 100 value wy
0 value wx1
0 value wy1

: ISR-TEST
\ 23672 ( FRAMES ) @ 3 AND 0= IF
    wx1 1 - to wx1
    wx1 22 reg!
\ endif
;

INT-OFF
' ISR-TEST INT-W !
int-on 
int-off

  0  SPRITE  _spriteid   !
100  SPRITE  _xcoord     !
100  SPRITE  _ycoord     !
  0  SPRITE  _pattern    c!
  0  SPRITE  _rotmir     c!
  0  SPRITE  _anchor     c!

hex
: pixeladd ( x y -- a )  
  over ff and 5 rshift   
  12 reg@ 2* + mmu7!     
  swap 1f and            
  8 lshift +             
  e000 or
;

: plot  ( x y c -- )    
  -rot over 8 lshift over +
  C000 U< if 
      pixeladd c! 
   else 
       drop  2drop  
   then
;
decimal

0    value dx       
0    value dy       
0    value sx       
0    value sy       
0    value err      
255  value color

471 load

2 constant cell
: sinus@ cell * sine-table + @ ;

: sin 
  dup >r 
  abs 360 mod
  dup 180 > if 180 - -1 else 0 then >r
  dup 90 > if 180 swap - then
  sinus@
  r> +- 
  r> +-  ;

: cos 90 + sin ;

: draw-line ( x2 y2 x1 y1 c -- )
  to color rot swap                   
  
  2over -  1 over +- to sx  abs to dx
  2dup  -  1 over +- to sy  abs negate to dy
  dx dy + to err
  swap -rot 
  
  begin
    2dup 256 u< swap 192 u< and  >r      
    2dup color plot 2over 2over          
    rot - -rot - or  r> and      
  while
    err dup + >r                   
    r@ dy < not if
      dy +to err swap sx + swap
    endif
    r> dx > not if
      dx +to err sy +
    endif
    ?terminal if 2drop 2drop exit then
  repeat
  2drop color plot
;

: warte
  1000 0 do loop ;

: stern
360 0 do 
  i sin 80 10000 */ to wx1
  i cos 80 10000 */ to wy1
  
  wy1 95 + wx1 126 + 95 126 224 draw-line
5 +loop  
;

hex 5c08 constant last-k decimal
: keypress ( — c )
  0 last-k c!
  begin last-k c@ until
  last-k c@
;

: oben
  wy 2 - to wy
  wy SPRITE _ycoord !
  0 SPRITE _spriteid !
  SPRITE  0  SPRITE-UPDATE
  ;
  
: unten
  wy 2 + to wy
  wy SPRITE _ycoord !
  0 SPRITE _spriteid !
  SPRITE  0  SPRITE-UPDATE
  ;
  
: rechts
  wx 2 + to wx
  wx SPRITE _xcoord !
  0 SPRITE _spriteid !
  SPRITE  0  SPRITE-UPDATE
  ;
  
: links
  wx 2 - to wx
  wx SPRITE _xcoord !
  0 SPRITE _spriteid !
  SPRITE  0  SPRITE-UPDATE
  ;

: starte
case
  97 of int-on  endof
  100 of int-off  endof
  119 of oben   endof
  101 of rechts endof
  113 of links  endof
  115 of unten  endof 
endcase ; 

: start
  begin
  keypress
  starte
?terminal until 
int-off
0 22 reg!
;

: los
 layer2
 cls
 stern
 
 SPRITE  0  SPRITE-UPDATE
 
 start
;


