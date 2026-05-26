
DECIMAL


needs value  
needs to 
needs +to
needs 2over  
needs dnegate
needs layers

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
  i sin 80 10000 */ to wx
  i cos 80 10000 */ to wy
  
  wy 95 + wx 126 + 95 126 224 draw-line
5 +loop  
;

: scrollx
  257 0 do
    i 22 reg!
    warte 
  loop

  257 0 do
    256 i - 22 reg!
    warte
  loop 
;  

: scrolly
  193 0 do
    i 23 reg!
    warte
  loop

  193 0 do
    192 i - 23 reg!
    warte
  loop 
;  

: los
 layer21
 cls
 stern
 
 scrollx
 scrolly
 ;


QUIT

 
Hi Peter,

I tryed your first example, good job ideed !

I suggest, in the four DO-LOOPs, to loop between 0 and 257 for y-direction and 0 to 193 for x-direction instead of 256 and 192.
This way you will return to ZERO scroll in both directions. This is typical in Forth in that the Loop-limit is never reached.

As far I know, in IDE_MODE NextOS call, for Layer 2 there is no sub-mode then using 0200 or 0201 should be the same.
Why did you define LAYER21 ? Did you found any difference between LAYER2 and LAYER21 ?
Anyway, I prefer to use NEEDS LAYERS that in turn loads all the other Layer related words.

For the second example, keep in mind that your ISR (ISR-TEST) scrolls Layer2 only once every 8 frame by checking "FRAMES system variable"  and doing a "7 AND" as an equivalent but faster "8 MOD". Try to reduce it to 3 or to 1 to increase the speed or remove it to achive maximum scroll speed.

To make your example suitable to run on my system I had to change your "include /fth/spriteproglayer.f" to some parts I found in "400 LOAD".

Regards.
_Matteo.

