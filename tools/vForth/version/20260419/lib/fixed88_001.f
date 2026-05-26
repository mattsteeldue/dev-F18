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

CREATE SCALE
#1     ,    \ no decimal digits 
#20    ,    \ one digit after decimal point
#200   ,    \ two
#2000  ,    \ three
#20000 ,    \ four
#195   ,    \ four when double-integer exceed 65535
#1953  ,    \ five digits
#19531 ,    \ six digits
\ convert a double integer into a fixed 8.8, useful for literal input 
\ because it uses DPL as the number of digits after the decimal point, 
: D>F ( d -- f )
    DUP >R DABS                 \ save high part as sign and use absolute value of d
    DPL @ IF
        DPL @ CELLS SCALE + @   \ get suitable divisor
        DUP >R 2/               \ and save for later
        UM/MOD                  \ get integer part and remainder
        FLIP                    \ this is the high 8 bits of final fixed.8.8
        SWAP                    \ now work on lower 8 bit
        512 UM*                 \ use two times 256 as moltiplicator
        R@ 2/ 0 D+              \ add some rounding
        R> UM/MOD               \ use same divisor as above
        NIP                     \ this is the lower 8 bits
        +                       \ add the two parts
    ELSE
        DROP                    \ discard high part of double-integer
        INT>8.8  
    THEN
    R> +-                       \ apply sign if needed
;

    \   2 LSHIFT DUP IF 1+ THEN 64 \ but first allow some rounding
    \    SWAP 2 LSHIFT 1+ 64 R> @ */   \ this is the lower 8 bits
\   DPL @ CELLS SCALE + >R      \ save DPL pointer to SCALE table
\   DUP IF                      \ rshift 8 for 32 bits.
\       SPLIT                   \ stack is DE 0L 0H
\       SWAP FLIP               \ stack is DE 0H L0 
\       ROT  SPLIT NIP          \ stack is 0H L0 0D
\       OR SWAP                 \ stack is LD 0H that is 0HLD      
\       R> 2+ >R                \ increment DPL to point next entry
\   THEN


\ Print 8.8 fixed point with 2 decimal places 
: F.   ( f -- )
    DUP 0< IF [CHAR] - EMIT FNEGATE THEN    
    1+ SPLIT 0 0 D.R 
    [CHAR] . EMIT
    100 * SPLIT NIP 
    0 <# # # #> TYPE
    SPACE
;


\ ================================================================
\ Square Root - FSQRT (f8.8 -- f8.8)
\ Uses binary search on the result. Input must be >= 0.
\ ================================================================

: FSQRT   ( f -- sqrt_f )
    DUP 0< IF DROP 0 EXIT THEN          \ negative ? return 0 (or error)
    DUP 0= IF EXIT THEN                 \ sqrt(0) = 0

    \ Binary search: low = 0, high = f (safe upper bound)
    0 SWAP                              \ low high
    BEGIN
        2DUP - 2 RSHIFT +               \ mid = low + (high - low)/4   (faster convergence)
        DUP DUP F*                      \ mid^2
        2OVER ROT                       \ mid^2 low high
        > IF                            \ if mid^2 > f then high = mid
            NIP                         \ high = mid
        ELSE
            DROP                        \ low = mid
        THEN
        2DUP 1- =                       \ if high <= low + 1
    UNTIL
    DROP ;                              \ leave the lower value (good enough for 8.8)

\ ================================================================
\ Comparison words
\ ================================================================

: F0<   ( f -- flag )   0< ;
: F0=   ( f -- flag )   0= ;
: F=    ( f1 f2 -- flag )   = ;
: F<    ( f1 f2 -- flag )   < ;
: F>    ( f1 f2 -- flag )   > ;

\ ================================================================
\ Useful constants
\ ================================================================

: F0.5     128 ;          \ 0.5 in 8.8
: F1.0     256 ;          \ 1.0
: F2.0     512 ;
: F0.25     64 ;
: F0.125    32 ;

\ ================================================================
\ Example usage (for testing)
\ ================================================================

\ Test:
\ 1 INT>8.8 2 INT>8.8 F* F.     \ should print approx 2.00
\ 128 INT>8.8 F0.5 F+ F.        \ 128.5

