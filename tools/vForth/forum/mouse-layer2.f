NEEDS INTERRUPT
NEEDS VALUE     
NEEDS TO      
NEEDS +TO
NEEDS CALL#     
NEEDS FLIP
NEEDS LAYER2    
NEEDS LAYER12
NEEDS CASE
needs border.    
needs at.
needs paper.     
needs ink.
needs ms
needs 2over  
needs dnegate
 
0 value x     0 value y
 
( mouse interface )
HEX 0FFDF P@ FLIP VARIABLE mouse-x
    0FBDF P@ FLIP VARIABLE mouse-y
    0FADF P@      VARIABLE mouse-s
    0 VARIABLE mouse-dx 0 VARIABLE mouse-dy
    0 VARIABLE mouse-ds
  
: mouse-read ( -- ) \ interrupt-service-routine
  0FFDF P@ FLIP DUP mouse-x @ SWAP - mouse-dx ! mouse-x !
  0FBDF P@ FLIP DUP mouse-y @      - mouse-dy ! mouse-y !
  0FADF P@      DUP mouse-s @      - mouse-ds ! mouse-s !
  
  mouse-dy @ mouse-dx @ mouse-ds @ or or if
    5C3B C@ 20 OR 5C3B C! 0             \ set FLAGS sys-var
    mouse-ds @ 0> if 0D + then 5C08 C!  \ set LASTK sys-var
  endif
; ' mouse-read INT-W !

decimal

: mouse-dir
  mouse-dx @ ?dup if
    1 swap +- x + 0 max 256 min to x
  endif
  mouse-dy @ ?dup if
    1 swap +- y + 0 max 190 min to y
  endif
;

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
0 value wx
0 value wy

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

: mouse 
  int-on
  begin
    mouse-dir
    x y x  plot
    50 ms
  again
  int-off
;

: los
layer2
cls
mouse ;
[code]


