\
\ fixed88.f
\ ______________________________________________________________________ 
\
\ v-Forth 1.8 - NextZXOS version - build 2026-04-19
\ MIT License (c) 1990-2026 Matteo Vitturi     
\ ______________________________________________________________________ 
\
\ Fixed-point 8.8 arithmetic library for vForth (16-bit cells)
\ Signed Q8.8 format: 8 integer bits, 8 fractional bits (range -128.0 to +127.996)

.( FIXED88 )

NEEDS FLIP
NEEDS SPLIT
NEEDS UD/
NEEDS DSQRT

MARKER FIXED88 


\ ================================================================
\ Basic conversion words
\ ================================================================

\ Convert integer to 8.8 fixed-point (n -- f8.8)
: INT>8.8   ( n -- f )
    8 LSHIFT            \ multiply by 256 (left shift by 8)
;


\ Convert 8.8 fixed-point to integer (truncated towards zero)
: 8.8>INT0  ( f -- n )
    8 RSHIFT 
;


\ Convert 8.8 fixed-point to integer (rounded) (f8.8 -- n)
: 8.8>INT   ( f -- n )
    #128 + 8.8>INT0     \ add 0.5 and shift right (standard rounding)
;   


\ ================================================================
\ Optimized arithmetic using FLIP and SPLIT
\ ================================================================

\ Addition, subtraction and Negation work directly (same format)
: F+   ( f1 f2 -- f3 )   + ;
: F-   ( f1 f2 -- f3 )   - ;
: FNEGATE   ( f -- -f )   NEGATE ;

\ Multiplication: f1 * f2 = f3  (8.8 * 8.8 = 16.16 intermediate 
: F*   ( f1 f2 -- f3 )
    #256 */        
;
    
\ Division: f1 / f2 = f3
\ To avoid precision loss we do (f1 << 8) / f2
: F/    ( f1 f2 -- q )
    #256 SWAP */
;

\ ================================================================
\ I/O
\ ================================================================

\ Print 8.8 fixed point with 2 decimal places 
: F.   ( f -- )
    DUP 0< IF 
        [CHAR] - EMIT 
        FNEGATE 
    THEN    
    DUP SPLIT DROP 
    IF 1+ THEN          \ rounding
    SPLIT 0 0 D.R       \ emit high byte
    [CHAR] . EMIT
    #100 * SPLIT NIP    \ two decimal digits
    0 <# # # #> TYPE
    SPACE
;

: UD/10 ( ud1 -- ud2 )
    0 #10 UM/MOD >R             \ de 00  r      R: q1
    #10 UM/MOD NIP R>           \ q2 q1
;


CREATE SCALE
    0 #10    ,    \ one digit after decimal point
    0 #100   ,    \ two digits after decimal point
    0 #1000  ,    \ three digits
    0 #10000 ,    \ four digits
  #10 #10000 ,    \ five digits
 #100 #10000 ,    \ six digits
#1000 #10000 ,    \ seven digits
\ convert a double integer into a fixed 8.8, useful for literal input. 
\ It uses DPL as the number of digits after the decimal point, 
\ d must have less than 7 precision digits to be meaninful for f8.8 fixed points
: D>F ( d -- f8.8 )

    \ save high part as sign and use absolute value of d
    DUP >R DABS                 

    \ compute d <<8, as HLDE --> LDE0, high byte is lost.
    SPLIT NIP FLIP              \ de l0
    >R SPLIT R> +               \ e0 ld

    \ if there is any digit after decimal point
    DPL @ ?DUP IF
        \ get corresponding TWO scale divisors addreses
        1- CELLS 2* 
        SCALE +
        DUP @ >R 
        
        \ apply first divisor
        CELL+ @ UD/
        
        \ apply second divisor if non zero.
        R> ?DUP IF
            UD/
        THEN
    THEN

    R> +-                       \ apply sign if needed
;


\ ================================================================
\ Useful constants
\ ================================================================


#512  CONSTANT F2.0    
#256  CONSTANT F1.0      \ 1.0
#128  CONSTANT F0.5      \ 0.5 in 8.8


\ ================================================================
\ Square Root - FSQRT (f8.8 -- f8.8)
\ Uses binary search on the result. Input must be >= 0.
\ ================================================================

: FSQRT   ( f -- sqrt_f )
    0 DSQRT #16 *
;


\ ================================================================
\ Comparison words
\ ================================================================

: F0<   ( f -- flag )   0< ;
: F0=   ( f -- flag )   0= ;
: F=    ( f1 f2 -- flag )   = ;
: F<    ( f1 f2 -- flag )   < ;
: F>    ( f1 f2 -- flag )   > ;

\ ================================================================
\ Example usage (for testing)
\ ================================================================

\ Test:
\ 1 INT>8.8 2 INT>8.8 F* F.     \ should print approx 2.00
\ 128 INT>8.8 F0.5 F+ F.        \ 128.5

: t d>f .s f. ;
