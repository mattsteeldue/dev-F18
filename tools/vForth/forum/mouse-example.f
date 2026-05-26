( mouse interface via interrupt )
NEEDS INTERRUPT
NEEDS FLIP  \ swaps hi and low byte of the integer number

HEX 0FFDF P@ FLIP VARIABLE mouse-x
    0FBDF P@ FLIP VARIABLE mouse-y
    0FADF P@      VARIABLE mouse-s
    
  0 VARIABLE mouse-dx
  0 VARIABLE mouse-dy 
  0 VARIABLE mouse-ds
  
\ this definition is the interrupt-service-routine that reads the three mouse ports and 
\ keep track of current state and current "delta" compared with the previous mouse state 
\ that was read during the previous interrupt.
: mouse-read ( -- ) 
  0FFDF P@ FLIP DUP mouse-x @ SWAP - mouse-dx ! mouse-x !
  0FBDF P@ FLIP DUP mouse-y @      - mouse-dy ! mouse-y !
  0FADF P@      DUP mouse-s @      - mouse-ds ! mouse-s !
  mouse-dy @ mouse-dx @ mouse-ds @ or or if
    5C3B C@ 20 OR 5C3B C! 0             \ set FLAGS sys-var
    mouse-ds @ 0> if 0D + then 5C08 C!  \ set LASTK sys-var
  endif
; ' mouse-read INT-W !

