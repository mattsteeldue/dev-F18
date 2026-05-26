\
\ Patrick Kaell's Fedora
\
needs J
needs GRAPHICS

marker task

\ array indexed by integer "deg" between 0 and 90
\ with the value of sin(deg) scaled /16384 for 
\ maximum precision with 16 bits integers.
CREATE sin-table
        0 ,   286 ,   572 ,   857 ,  1143 ,  1428 ,  1713 ,  
     1997 ,  2280 ,  2563 ,  2845 ,  3126 ,  3406 ,  3686 ,  
     3964 ,  4240 ,  4516 ,  4790 ,  5063 ,  5334 ,  5604 ,  
     5872 ,  6138 ,  6402 ,  6664 ,  6924 ,  7182 ,  7438 ,
     7692 ,  7943 ,  8192 ,  8438 ,  8682 ,  8923 ,  9162 ,
     9397 ,  9630 ,  9860 , 10087 , 10311 , 10531 , 10749 ,
    10963 , 11174 , 11381 , 11585 , 11786 , 11982 , 12176 , 
    12365 , 12551 , 12733 , 12911 , 13085 , 13255 , 13421 ,
    13583 , 13741 , 13894 , 14044 , 14189 , 14330 , 14466 ,
    14598 , 14726 , 14849 , 14968 , 15082 , 15191 , 15296 ,
    15396 , 15491 , 15582 , 15668 , 15749 , 15826 , 15897 , 
    15964 , 16026 , 16083 , 16135 , 16182 , 16225 , 16262 , 
    16294 , 16322 , 16344 , 16362 , 16374 , 16382 , 16384 ,


: SIN ( n1 -- n2 )
    180 /mod >R dup >R abs              \ |q|         R: r q
    dup 90 >                            \ |q|  f        
    if 180 swap - then                  \ |q|  or  pi-|q|
    2* sin-table + @                    \ |sin|   
    R> +-                               \ |sin| with sign of q
    R> 1 and if negate then             \ sin   with quadrant
;

: SQRT ( n1 -- n2 )
    DUP 1
    BEGIN 2DUP > WHILE
      + 2/ 2DUP /
    REPEAT
    ROT 2DROP
;

CREATE RR 642 ALLOT

0 VALUE ZS 
0 VALUE XL 
0 VALUE XT 
0 VALUE YY 
0 VALUE X1 
0 VALUE Y1 

160 VALUE DX 
140 VALUE DY

20736 CONSTANT 20736
27192 CONSTANT 27192
16384 CONSTANT 16384
   56 CONSTANT    56
    5 CONSTANT     5
   -2 CONSTANT    -2

: FEDORA ( -- ) 

    642 0 DO
        1000 RR I + !
    2 +LOOP
  
    -64 64  DO
        I DUP * 81 16 */ TO ZS 
        20736 ZS - 0 DSQRT TO XL 
        XL 1+ XL NEGATE DO
            I DUP * ZS + 0 DSQRT 27192 16384 */ TO XT
            XT SIN XT 3 * SIN 2 5 */ + 56 16384 */ TO YY
            DX   I   +  J +  TO X1 
            DY  YY   -  J +  TO Y1 
            X1 0 < NOT  IF
                RR X1 2* + @ Y1  >  IF
                    Y1 RR X1 2* + ! 
                    Y1  2/ 
                    X1   
                    PLOT
                THEN
            THEN
        LOOP
        ?terminal if leave then
    -2 +LOOP
;
