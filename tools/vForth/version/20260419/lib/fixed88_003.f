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

\ Addition and subtraction work directly (same format)
: F+   ( f1 f2 -- f3 )   + ;
: F-   ( f1 f2 -- f3 )   - ;

\ Negation
: FNEGATE   ( f -- -f )   NEGATE ;

\ Multiplication: f1 * f2 = f3  (8.8 * 8.8 = 16.16 intermediate 
\ Optimized with SPLIT + FLIP to avoid slow *256 /256
: F*   ( f1 f2 -- f3 )
    2DUP XOR >R                \ save sign of result (f1 XOR f2)
    ABS SWAP ABS               \ make both positive
    UM*                        \ unsigned 32-bit (HLde) we must keep middle "Ld"
    SPLIT DROP FLIP            \ handle integer part (L)
    SWAP FLIP SPLIT DROP       \ handle fractional part (d)
    OR                         \ normalize back to 8.8
    R> +-                      \ apply sign if needed
;

    
\ Division: f1 / f2 = f3
\ To avoid precision loss we do (f1 << 8) / f2
: F/    ( f1 f2 -- q )
    2DUP XOR >R                \ save sign of result (f1 XOR f2)
    ABS SWAP ABS               \ make both positive
    SPLIT                      \ make divisor 32 bits
    SWAP FLIP #255 AND SWAP    \ handle fractional part (d)
    UM/MOD                     \ unsigned 32-bit division (remainder quotient)
    OR                         \ normalize back to 8.8
    R> +-                      \ apply sign if needed
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
    DUP SPLIT DROP IF 1+ THEN
    SPLIT 0 0 D.R 
    [CHAR] . EMIT
    #100 * SPLIT NIP 
    0 <# # # #> TYPE
    SPACE
;


CREATE SCALE
#10    ,    \ one digit after decimal point
#100   ,    \ two
#1000  ,    \ three
#10000 ,    \ four
#100   ,    \ four when double-integer exceed 65535
#1000  ,    \ five digits
#10000 ,    \ six digits
\ convert a double integer into a fixed 8.8, useful for literal input 
\ because it uses DPL as the number of digits after the decimal point, 
\ d must have less than 7 precision digits to be meaninful for f8.8 fixed points
: D>F ( d -- f8.8 )
    DUP >R DABS                 \ save high part as sign and use absolute value of d
    DPL @ IF
        DPL @ 1- CELLS SCALE +  \ get corresponding scale divisor addr
        >R                      \ save address to Return Stack
        DUP IF                  \ double-integer larger than 65535*256
            #100  UM/MOD NIP 0  \ scale down
            R> CELL+ >R         \ use next cell divisor
        THEN
        R> @ >R                 \ fetch divisor
        \ integer part
        R@
        UM/MOD FLIP             \ this is the high 8 bits of final fixed.8.8
        SWAP   
        #256 UM*                \ use two times 256 as moltiplicator
        R@ 2/ 0 D+              \ for rounding add divisor/2
        R>   UM/MOD             \ use same divisor as above
        NIP                     \ this is the lower 8 bits
        +                       \ add the two parts
    ELSE
        DROP                    \ discard high part of double-integer
        INT>8.8  
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
