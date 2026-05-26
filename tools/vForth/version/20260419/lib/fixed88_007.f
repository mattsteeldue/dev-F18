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

\ --- USEFUL CONSTANTS --- 

DECIMAL    
  512 CONSTANT FP-2.0    
  256 CONSTANT FP-1.0      \ 1.0
  128 CONSTANT FP-0.5      \ 0.5 
  192 CONSTANT FP-0.75
 1608 CONSTANT FP-2PI
  804 CONSTANT FP-PI       \ Pi ~ 3.14159 ~ 804/256
  402 CONSTANT FP-PI/2
  201 CONSTANT FP-PI/4 
  696 CONSTANT FP-E        \ e ~ 2.71828 ~ 696/256
46080 CONSTANT FP-180 


\ --- BASE CONVERSIONS ---

: >FP   ( n -- fp )
  \ Convert integer to fixed-point
  \ Optimized: shift byte instead of multiply by 256
  BIT-SCALE LSHIFT ;

: FP>INT   ( fp -- n )
  \ Convert fixed-point to integer (truncation)
  DUP BIT-SCALE RSHIFT
  SWAP +- ;  


: FP>ROUND   ( fp -- n )
  \ Convert fixed-point to integer (rounding)
  FP-HALF + FP>INT ;


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


\ --- SQUARE ROOT (Approximated) ---

: FP-SQRT   ( fp -- sqrt-fp )
  \ Square root using Newton's method
  \ sqrt(x) with iterations: xn+1 = (xn + x/xn) / 2
  DUP 0> IF           \ x  
    DUP 2/            \ x  xn  Initial guess: x/2
    4 0 DO            \ 4 iterations (balance precision/speed)
      2DUP FP/        \ x  xn  x/xn
      OVER FP+        \ x  xn  xn+x/xn
      2/              \ x  xn  (xn+x/xn)/2
    LOOP
    NIP NIP                 
  ELSE 
    DROP 0    
  THEN
  ;

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

\ Print 8.8 fixed point with 2 decimal places 
: F.   ( fp -- )
    DUP 0< IF 
        [CHAR] - EMIT 
        NEGATE 
    THEN    
    DUP SPLIT DROP 
    IF 1+ THEN          \ rounding
    SPLIT S>D           \ converto to double
    0 D.R               \ emit high byte
    [CHAR] . EMIT
    100 * SPLIT NIP   \ two decimal digits
    S>D <# # # #> TYPE
    SPACE
;

\ compute d <<8, as HLDE --> LDE0, H byte is lost.
: D<<8 ( ud1 -- ud2 )
    SPLIT           \ DE 0L 0H
    DROP FLIP       \ DE L0
    SWAP            \ L0 DE
    SPLIT           \ L0 0E 0D
    ROT             \ 0E 0D L0 
    OR              \ 0E LD
    SWAP FLIP       \ LD E0
    SWAP
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

    R> +-                       \ apply sign if needed
;

\ Trigonometric functions - Lookup Table based 
\ Argument in radians (Q8.8), result in Q8.8 (-256..+256 represents -1.0..+1.0)

\ Precomputed sin table: sin(Pi/2/256)*256   for n=0..402
\ Stored as signed 16-bit values (but only low byte really used, high for sign)
CREATE SIN-TABLE 
DECIMAL CHAR . EMIT
000 , 001 , 002 , 003 , 004 , 005 , 006 , 007 , 008 , 009 , 
010 , 011 , 012 , 013 , 014 , 015 , 016 , 017 , 018 , 019 , 
020 , 021 , 022 , 023 , 024 , 025 , 026 , 027 , 028 , 029 , 
030 , 031 , 032 , 033 , 034 , 035 , 036 , 037 , 038 , 039 , 
040 , 041 , 042 , 043 , 044 , 045 , 046 , 047 , 048 , 049 , 
050 , 051 , 052 , 053 , 054 , 055 , 056 , 057 , 058 , 059 , 
060 , 061 , 062 , 063 , 064 , 065 , 066 , 067 , 068 , 069 , 
070 , 071 , 072 , 072 , 073 , 074 , 075 , 076 , 077 , 078 , 
079 , 080 , 081 , 082 , 083 , 084 , 085 , 086 , 087 , 088 , 
089 , 090 , 091 , 091 , 092 , 093 , 094 , 095 , 096 , 097 , CHAR . EMIT
098 , 099 , 100 , 101 , 102 , 103 , 103 , 104 , 105 , 106 , 
107 , 108 , 109 , 110 , 111 , 112 , 113 , 113 , 114 , 115 , 
116 , 117 , 118 , 119 , 120 , 121 , 121 , 122 , 123 , 124 , 
125 , 126 , 127 , 128 , 128 , 129 , 130 , 131 , 132 , 133 , 
134 , 134 , 135 , 136 , 137 , 138 , 139 , 139 , 140 , 141 , 
142 , 143 , 144 , 144 , 145 , 146 , 147 , 148 , 149 , 149 , 
150 , 151 , 152 , 153 , 153 , 154 , 155 , 156 , 157 , 157 , 
158 , 159 , 160 , 161 , 161 , 162 , 163 , 164 , 164 , 165 , 
166 , 167 , 167 , 168 , 169 , 170 , 170 , 171 , 172 , 173 , 
173 , 174 , 175 , 176 , 176 , 177 , 178 , 178 , 179 , 180 , CHAR . EMIT
181 , 181 , 182 , 183 , 183 , 184 , 185 , 186 , 186 , 187 , 
188 , 188 , 189 , 190 , 190 , 191 , 192 , 192 , 193 , 194 , 
194 , 195 , 196 , 196 , 197 , 197 , 198 , 199 , 199 , 200 , 
201 , 201 , 202 , 202 , 203 , 204 , 204 , 205 , 205 , 206 , 
207 , 207 , 208 , 208 , 209 , 210 , 210 , 211 , 211 , 212 , 
212 , 213 , 214 , 214 , 215 , 215 , 216 , 216 , 217 , 217 , 
218 , 218 , 219 , 219 , 220 , 220 , 221 , 221 , 222 , 222 , 
223 , 223 , 224 , 224 , 225 , 225 , 226 , 226 , 227 , 227 , 
228 , 228 , 229 , 229 , 229 , 230 , 230 , 231 , 231 , 232 , 
232 , 232 , 233 , 233 , 234 , 234 , 235 , 235 , 235 , 236 , CHAR . EMIT
236 , 236 , 237 , 237 , 238 , 238 , 238 , 239 , 239 , 239 , 
240 , 240 , 240 , 241 , 241 , 241 , 242 , 242 , 242 , 243 , 
243 , 243 , 244 , 244 , 244 , 245 , 245 , 245 , 245 , 246 , 
246 , 246 , 247 , 247 , 247 , 247 , 248 , 248 , 248 , 248 , 
249 , 249 , 249 , 249 , 250 , 250 , 250 , 250 , 250 , 251 , 
251 , 251 , 251 , 251 , 252 , 252 , 252 , 252 , 252 , 252 , 
253 , 253 , 253 , 253 , 253 , 253 , 254 , 254 , 254 , 254 , 
254 , 254 , 254 , 254 , 255 , 255 , 255 , 255 , 255 , 255 , 
255 , 255 , 255 , 255 , 255 , 255 , 256 , 256 , 256 , 256 , 
256 , 256 , 256 , 256 , 256 , 256 , 256 , 256 , 256 , 256 , CHAR . EMIT
256 , 256 , 256 ,                                           

DECIMAL

: *PI    ( fp -- pi*fp )
    355 113 */ 
;

: /PI    ( f -- fp/pi )
    113 355 */ 
;

: DEG>RAD   ( degrees -- radians )
  \ Convert degrees to radians: rad = deg * Pi/180
  355 20340 */ ;

: RAD>DEG   ( radians -- degrees )
  \ Convert radians to degrees: deg = rad * 180/Pi
  20340 355 */ ;

\ Sine function using lookup table with quadrant symmetry
\ Input: angle in radians (Q8.8 format), any range
\ Output: sine value (Q8.8 format, -256..+256 represents -1.0..+1.0)
\ Table: 403 entries covering [0, pi/2] with linear interpolation
: FSIN    ( radians-fp -- sin-fp )
    FP-PI /MOD >R               \ R: quotient (p multiples), TOS: remainder [-p,+p]
    DUP >R                      \ R: quotient remainder, save remainder sign
    ABS                         \ Work with |remainder| [0,p]
    
    \ Reduce to first quadrant using symmetry
    DUP FP-PI/2 > IF            \ If in second quadrant [p/2, p]
        FP-PI/2 -               \ Subtract p/2
        FP-PI/2 SWAP -          \ Mirror: sin(p-x) = sin(x)
    THEN
    
    \ Lookup: angle now [0, p/2] maps to table index [0, 402]
    CELLS SIN-TABLE + @
    
    R> +-                       \ Apply remainder sign
    R> -1 AND IF NEGATE THEN    \ Odd quotient means p shift ? negate
;

\ Cosine via phase shift: cos(x) = sin(x + p/2)
\ But implemented as: cos(x) = -sin(x - p/2) for efficiency
: FCOS  ( radians-fp -- cos-fp )
    FP-PI/2 - FSIN NEGATE
;


: FTAN  ( radians-fp -- tan-fp )
    DUP FSIN SWAP FCOS FP/ 
;

\ Test:
\ 1 >FP 2 >FP FP* F.     \ should print approx 2.00
\ 128 >FP F0.5 FP+ F.        \ 128.5

\ : t d>f .s f. ;



