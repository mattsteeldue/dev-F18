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

MARKER FIXED88 
NEEDS FLIP
NEEDS SPLIT
NEEDS UD/
NEEDS DSQRT


.( .) \ show progress


DECIMAL

\ --- CONSTANTS ---

  256 CONSTANT FP-SCALE       \ 2^8 = scaling factor
  128 CONSTANT FP-HALF        \ 0.5 in fixed-point format
    8 CONSTANT BIT-SCALE
  255 CONSTANT B-MASK

  256 CONSTANT FP-1.0      \ 1.0
  128 CONSTANT FP-0.5      \ 0.5 
 1608 CONSTANT FP-2PI
  804 CONSTANT FP-PI       \ Pi ~ 3.14159 ~ 804/256
  402 CONSTANT FP-PI/2
  201 CONSTANT FP-PI/4 
  696 CONSTANT FP-E        \ e ~ 2.71828 ~ 696/256
46080 CONSTANT FP-180      \ 180.0


\ --- CONVERSIONS ---

: >FP   ( n -- fp )
  \ Convert integer to fixed-point Q8.8
  \ Optimized: shift byte instead of multiply by 256
  BIT-SCALE LSHIFT ;


: FP>INT   ( fp -- n )
  \ Convert fixed-point to integer (truncation)
  DUP BIT-SCALE RSHIFT
  SWAP +- ;  


: FP>ROUND   ( fp -- n )
  \ Convert fixed-point to integer (rounding)
  FP-HALF + FP>INT ;


DECIMAL

\ Convert degrees to radians: rad = deg * Pi/180
: DEG>RAD   ( degrees -- radians )
  355 20340 */ ;

\ Convert radians to degrees: deg = rad * 180/Pi
: RAD>DEG   ( radians -- degrees )
  20340 355 */ ;

: *PI    ( fp -- pi*fp )
    355 113 */ ;

: /PI    ( f -- fp/pi )
    113 355 */ ;



\ --- COMPONENT EXTRACTION ---

: FP-FRAC   ( fp -- n )
  \ Extract fractional part (0-255)
  B-MASK AND ;


: FP-PARTS   ( fp -- int frac )
  \ Extract both parts using SPLIT
  SPLIT SWAP ;


\ --- BASE ARITHMETIC OPERATIONS ---

: FP+   ( fp1 fp2 -- fp3 )
  \ Fixed-point addition
  + ;


: FP-   ( fp1 fp2 -- fp3 )
  \ Fixed-point subtraction
  - ;


: FP*   ( fp1 fp2 -- fp3 )
  \ Fixed-point multiplication
  \ Result needs to be scaled down by 256
  FP-SCALE */ ;  


: FP/   ( fp1 fp2 -- fp3 )
  \ Fixed-point division
  \ Numerator needs to be scaled up by 256
  FP-SCALE SWAP */ ;  


\ --- FRACTION CONVERSION ---

: N/D>FP   ( numerator denominator -- fp )
  \ Convert fraction to fixed-point
  FP/
;

\ --- ANGLE NORMALIZATION ---

: NORMALIZE-ANGLE   ( angle -- normalized-angle )
  \ Normalize angle to [0, 2Pi) range
  FP-2PI /MOD DROP 
  DUP 0< IF FP-2PI FP+ THEN 
;  


\ --- COMBINED OPERATIONS ---

: FP-SQUARE   ( fp -- fp^2 )
  \ Square
  DUP FP* ;


: FP-AVERAGE   ( fp1 fp2 -- fp-avg )
  \ Arithmetic mean
  FP+ 2 / ;


: FP-LERP   ( fp1 fp2 t -- fp-result )
  \ Linear interpolation: fp1 + t*(fp2-fp1)
  \ where t is in fixed-point format [0..1]
  >R 2DUP FP- R> FP* -ROT DROP + ;


\ D<<8    ( ud -- ud*256 )
\ Shift left 8 bits (multiply by 256) for double unsigned.
\ Internal double representation in this Forth:
\   Input := "HLDE"   (HL on top of stack, DE below)
\   Output:= "LDE0"   (H is discarded, remaining LDE is shifted)
CODE D<<8 ( ud -- ud' ) 
    $D9 C,          \ EXX
    $E1 C,          \ POP     HL|     
    $D1 C,          \ POP     DE|     
    $65 C,          \ LD      H'|    L|    
    $6A C,          \ LD      L'|    D|    
    $53 C,          \ LD      D'|    E|    
    $1E C, $00 C,   \ LDN     E'|    HEX 00 N,  
    $D5 C,          \ PUSH DE
    $E5 C,          \ PUSH HL
    $D9 C,          \ EXX
    $DD C, $E9 C,   \ NEXT
    SMUDGE          \ C;


\ --- SQUARE ROOT (Approximated) ---

               
\ FP-SQRT   ( ufp -- sqrt-fp )
\ Fixed-point square root using Newton's method.
\ Returns 0 for negative or zero input.
\ Uses early exit via LEAVE when convergence is reached.
: FP-SQRT   ( uf -- sqrt_f )
    DUP 0> IF
        0 D<<8 DSQRT 
    ELSE
        DROP 0
    THEN ;


\ --- PRACTICAL APPLICATIONS ---

\ Calculate distance between two points (positive part only)
: FP-DIST   ( x1 y1 x2 y2 -- dist )
  \ dist = sqrt((x2-x1)^2 + (y2-y1)^2)
  ROT  FP- FP-SQUARE    \ (y2-y1)^2
  -ROT FP- FP-SQUARE    \ (x2-x1)^2
  FP+ FP-SQRT ;


\ Temperature conversion Celsius → Fahrenheit
: C>F   ( celsius-fp -- fahrenheit-fp )
  \ F = C * 9/5 + 32
  9 5 */ 32 >FP FP+ ;


\ Temperature conversion Fahrenheit → Celsius
: F>C   ( fahrenheit-fp -- celsius-fp )
  \ C = (F - 32) * 5/9
  32 >FP FP- 5 9 */ ;


\ Compound interest calculation
: FP-INTEREST   ( capital rate% years -- amount )
  \ M = C * (1 + r)^n (approximated for small n)
  >R >R           \ Save years and capital
  100 N/D>FP FP-1.0 FP+  \ (1 + r/100)
  R> FP*          \ capital * (1+r)
  R> 1- 0 DO 
    OVER FP* 
  LOOP
  NIP ;


\ --- 2D VECTOR OPERATIONS ---

\ Vector addition
: VEC2-ADD   ( x1 y1 x2 y2 -- x3 y3 )
  ROT FP+ -ROT FP+ SWAP ;


\ Dot product
: VEC2-DOT   ( x1 y1 x2 y2 -- dot-product )
  ROT FP* -ROT FP* FP+ ;


\ Vector length
: VEC2-LEN   ( x y -- length )
  FP-SQUARE SWAP FP-SQUARE FP+ FP-SQRT ;


\ Vector normalization
: VEC2-NORMALIZE   ( x y -- x-norm y-norm )
  2DUP VEC2-LEN      \ x y len
  DUP 0= IF 
    DROP 2DROP 0 0   \ Null vector
  ELSE
    >R 2DUP R> 
    DUP >R FP/ -ROT R> FP/ SWAP
  THEN ;


\ --- I/O --- 

\ Print Q8.8 fixed point with 2 decimal places 
: F.   ( fp -- )
    DUP 0< IF 
        [CHAR] - EMIT 
        NEGATE 
    THEN    
    \ simple rounding, only if fractional part is non-zero
    DUP SPLIT DROP IF 1+ THEN     
    \ Integer part and dot
    SPLIT 0 .R [CHAR] . EMIT
    \ Fractional (2 decimal places)
    100 * SPLIT NIP   \ 100 means 2 decimal digits
    0 <# # # #> TYPE
    SPACE
;


CREATE FPSCALE   
DECIMAL        
\ Each entry: ( divisor-hi divisor-lo )
\ Index by (DPL-1)*2*CELLS
    0 , 10    ,    \ one digit after decimal point
    0 , 100   ,    \ two digits after decimal point
    0 , 1000  ,    \ three digits
    0 , 10000 ,    \ four digits
   10 , 10000 ,    \ five digits
  100 , 10000 ,    \ six digits
 1000 , 10000 ,    \ seven digits

\ convert a double integer into a fixed 8.8, useful for literal input. 
\ It uses DPL as the number of digits after the decimal point, 
\ d must have less than 8 precision digits to be meaninful for f8.8 fixed points
: D>F ( d -- f8.8 )
    \ save high part as sign and use absolute value of d
    DUP >R DABS   
    D<<8              
    \ if there is any digit after decimal point
    DPL @ ?DUP IF
        \ get corresponding TWO scale divisors addreses
        1- CELLS 2* 
        FPSCALE +
        DUP @ >R 
        \ apply first divisor
        CELL+ @ UD/
        \ apply second divisor if non zero.
        R> ?DUP IF
            UD/
        THEN
    THEN
    DROP
    \ apply sign 
    R> +- ;

.( .)


\ Floating-Point Calculator Interface
\ A floating point number is stored in Spectrum's calculator stack as 5 bytes.
\ Exponent in A, sign in msb of E, mantissa in the rest of E and DCB.

\ FOP    ( n -- )
\ Floating-Point-Operation.
\ it calls the FP calculator which is a small Stack-Machine
CODE FOP 
    $E1 C,          \ POP     HL|     
    $C5 C,          \ PUSH    BC|
    $D5 C,          \ PUSH    DE|
    $7D C,          \ LD      A'|    L|
    $32 C, HERE 0 , \ LD()A   HERE 0 AA,   
    $EF C,          \ RST     28|
    HERE SWAP !     \         HERE SWAP !  *THIS BYTE IS PATCHED*
    $38 C,          \         HEX 38 C, \ this location is patched each time
    $38 C,          \         HEX 38 C, \ end of calculation
    $D1 C,          \ POP     DE|
    $C1 C,          \ POP     BC|
    $DD C, $E9 C,   \ NEXT
    SMUDGE          \ C;

\ FP>W    ( fp -- )
\ pop number from calculator stack and push it to floating-pointer stack 
CODE FP>W
    $D9 C,          \ EXX
    $E1 C,          \ POP     HL|     
    $5C C,          \ LD      E'|    H|    
    $55 C,          \ LD      D'|    L|    
    $01 C, 0 ,      \ LDX     BC|    HEX 0000 NN,  
    $3E C, $8C C,   \ LDN     A'|    HEX $8C N,  
    $CD C, $2AB6 ,  \ CALL    HEX 2AB6 AA,
    $D9 C,          \ EXX
    $DD C, $E9 C,   \ NEXT
    SMUDGE          \ C;

\ W>FP    (  -- man-tissa exponent )
\ pop a number from floating-pointer stack and push it to top of calculator stack 
CODE W>FP3
    $D9 C,          \ EXX
    $CD C, $2BF1 ,  \ CALL    HEX 2BF1 AA,
    $6B C,          \ LD      L'|    E|    
    $5A C,          \ LD      E'|    D|    
    $55 C,          \ LD      D'|    L|    
    $69 C,          \ LD      L'|    C|    
    $48 C,          \ LD      C'|    B|    
    $45 C,          \ LD      B'|    L|    
    $6F C,          \ LD      L'|    A|    
    $26 C, $00 C,   \ LDN     H'|    0 N,
    $C5 C,          \ PUSH BC
    $D5 C,          \ PUSH DE
    $E5 C,          \ PUSH HL
    $D9 C,          \ EXX
    $DD C, $E9 C,   \ NEXT
    SMUDGE          \ C;
   
: W>FP ( -- fp )
    dup 128 < if
        
    else
        128 ?do
            2*
        loop
    then
    nip
;
        
\ Trigonometric functions - Lookup Table based 
\ Argument in radians (Q8.8), result in Q8.8 (-256..+256 represents -1.0..+1.0)



