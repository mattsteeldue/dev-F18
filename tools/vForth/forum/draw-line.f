: at. 22 emitc swap emitc emitc ;
: ink. 16 emitc emitc ;
: paper. 17 emitc emitc ;

( plot layer2 )
hex
: pixeladd ( x y -- a )  \ x: vertical  y:horizontal
  over FF and 5 rshift   \ divide x by 32
  12 reg@ 2* + mmu7!     \ fit correct 8K page
  swap 1F and            \ x mod 32
  8 lshift +             \ turn it high byte part
  E000 or
;
hex
: plot  ( x y c -- )     \ x: vertical  y:horizontal
  -rot over 8 lshift over +
  C000 U< if pixeladd c! else drop then
;

decimal

( draw-line )
\ draw a line using LAYER 2 mode
\
needs VALUE
needs TO
needs +TO
needs 2OVER
needs DNEGATE
needs LAYERS
\
0    value dx       \ x-distance between P1 and P2
0    value dy       \ y-distance between P1 and P2
0    value sx       \ x-direction from P1 to P2
0    value sy       \ y-direction from P1 to P2
0    value err      \ error at each stage
255  value color
\

: draw-line        ( x2 y2 x1 y1 c -- )
  to color   rot swap                   ( x2 x1 y2 y1 )
  \ determines sx, dx, sy, dy and err
  2over -  1 over +- to sx  abs to dx
  2dup  -  1 over +- to sy  abs negate to dy
  dx dy + to err
  swap -rot                             ( x2 y2 x1 y1 )
  begin
    2dup 256 u< swap 192 u< and  >R     \ pixel in range?
    \ plot current pixel and...
    2dup color plot 2over 2over         \ x2 y2 x1 y1 x2 y2
    \ check if final pixel is reached
    rot - -rot - or  R> AND      \ x2 y2 x1 y1 y1-y2|x2-x1|f
  while
    err dup + >R                   \ x2 y2 x1 y1  R:2err
    R@ dy < not if
      dy +to err swap sx + swap
    endif
    R> dx > not if
      dx +to err      sy +
    endif
    ?terminal if 2drop 2drop exit then
  repeat
  2drop color plot
;


( draw-line example )
LAYER2
000 255  000 000  255      draw-line
000 255  191 255  255      draw-line
191 000  191 255  255      draw-line
191 000  000 000  255      draw-line
191 255  000 000  255      draw-line
191 000  000 255  255      draw-line

15 10 at. key quit
