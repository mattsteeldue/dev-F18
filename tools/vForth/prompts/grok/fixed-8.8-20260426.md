You are an expert in vForth system which repository is stored at this location: https://github.com/mattsteeldue/vforth-next/tree/master

Latest official documentation is given by the document vForth1.8-core-en-20260419.pdf available at the same location https://github.com/mattsteeldue/vforth-next/tree/master/doc

The current core v.1.8 is built using VSCode using Z80 assembly source code available in project/DIRECT_MMU7
The core is maintainded in vForth itself, the source is given in src/F18e.f

Exact stack order for double numbers in vForth (e.g.: “In vForth, an unsigned double ud is represented on the data stack with the high cell on top (high low), while in memory (2@/2!/2VARIABLE) it is stored low-cell first (low high). In registers it is often HLDE with HL = high cell.”)

In vForth system, an unsigned double ud is represented on the data stack with the high cell on top (high low), while in memory (2@/2!/2VARIABLE) it is stored low-cell first (low high). In registers it is often HLDE with HL = high cell.

Preferred result is the smallest code size





\
\ DSQRT.f
\
.( DSQRT )
\
\ Square root of d (modified Newton-Raphson method)
\ 0 <= d < 1073741824
\ n <-- ( n + d/n ) / 2
\
\
: DSQRT ( d -- n )          \ d = high low -->  n = floor(sqrt(d))
    2DUP OR IF              \ se d != 0

        [ -1 1 RSHIFT -1 XOR ] LITERAL \ number with high bit set only 
        15 0 DO 
            >R 2DUP R@      \ d d n     R: n
            UM/MOD NIP      \ d d/n
            R> +            \ d n+d/n
            1 RSHIFT        \ d (n+d/n)/2
        LOOP
        NIP NIP             \ n

    ELSE
        DROP EXIT 
    THEN
;




\
\ DSQRT.f
\
.( DSQRT )
\
\ Square root of d (modified Newton-Raphson method)
\ 0 <= d < 1073741824
\ n <-- ( n + d/n ) / 2
\
\
: DSQRT ( d -- n )          \ d = high low -->  n = floor(sqrt(d))
    2DUP OR 0= IF DROP EXIT THEN
    DUP 0< IF 2DROP -1 EXIT THEN

    OVER 8 RSHIFT 1+ DUP 4 RSHIFT +     \ initial value

    BEGIN
        >R                      \ d         R: x
        2DUP R@ UM/MOD NIP      \ d (d/x)
        R@ + 1 RSHIFT           \ d x+(d/x)
        DUP R> =                \ d x+(d/x) x=x+(d/x)
    UNTIL

    NIP NIP
;


