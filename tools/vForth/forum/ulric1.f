    Arrays
: Array ( size -- )
  <BEGIN
    cells allot
  DOES> ( n -- a )
    swap cells + ;
    
    
: array ( u -- )
  create dup , cells allot \ { u x0 ... xu-1 }
  does> ( i -- addr )
    2dup @ ( i a i u )
    u< 0= -24 and throw ( invalid numeric arg )
    cell+
    swap cells + ;

    