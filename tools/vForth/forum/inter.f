needs interrupt
needs value    
needs to

marker task 

: at.    22 emitc  swap  emitc emitc ;
: ink.   16 emitc   emitc ;
: paper. 17 emitc   emitc ;  

0 value wert

: isr-test
   23672 ( frames )  @ 7 and 0= if
    wert 1 + to wert
    0 0 at. wert .
  endif  ;

int-off 
' isr-test int-w ! 
int-on 