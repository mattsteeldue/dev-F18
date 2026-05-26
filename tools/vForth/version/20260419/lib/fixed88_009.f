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


\ --- SQUARE ROOT (Approximated) ---

\ D<<8    ( ud -- ud*256 )
\ Shift left 8 bits (multiply by 256) for double unsigned.
\ Internal double representation in this Forth:
\   Input := "HLDE"   (HL on top of stack, DE below)
\   Output:= "LDE0"   (H is discarded, remaining LDE is shifted)
: D<<8 ( ud -- ud' ) \ DE HL 
    SPLIT            \ DE L H     (SPLIT  HL into L and H)
    DROP             \ DE  L      (discard H)   
    FLIP             \ DE L0      (L become high byte)
    SWAP             \ L0 DE
    SPLIT            \ L0  E   D
    ROT              \ E   D   L0
    OR               \ E   LD     (combine L and D)
    SWAP FLIP        \ LD  E0
    SWAP             \ E0  L0     
;              

               
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


\ Trigonometric functions - Lookup Table based 
\ Argument in radians (Q8.8), result in Q8.8 (-256..+256 represents -1.0..+1.0)

.( .)

\ Precomputed sin table: sin(x/256)*256-1   for n=0..402
\ Stored as signed 8-bit values 
CREATE SIN-TABLE 
DECIMAL 
-01 C, 000 C, 001 C, 002 C, 003 C, 004 C, 005 C, 006 C, 007 C, 008 C,  
009 C, 010 C, 011 C, 012 C, 013 C, 014 C, 015 C, 016 C, 017 C, 018 C,  
019 C, 020 C, 021 C, 022 C, 023 C, 024 C, 025 C, 026 C, 027 C, 028 C,  
029 C, 030 C, 031 C, 032 C, 033 C, 034 C, 035 C, 036 C, 037 C, 038 C,  
039 C, 040 C, 041 C, 042 C, 043 C, 044 C, 045 C, 046 C, 047 C, 048 C,  
049 C, 050 C, 051 C, 052 C, 053 C, 054 C, 055 C, 056 C, 057 C, 058 C,  
059 C, 060 C, 061 C, 062 C, 063 C, 064 C, 065 C, 066 C, 067 C, 068 C,  
069 C, 070 C, 071 C, 071 C, 072 C, 073 C, 074 C, 075 C, 076 C, 077 C,  
078 C, 079 C, 080 C, 081 C, 082 C, 083 C, 084 C, 085 C, 086 C, 087 C,  
088 C, 089 C, 090 C, 090 C, 091 C, 092 C, 093 C, 094 C, 095 C, 096 C,  .( .)
097 C, 098 C, 099 C, 100 C, 101 C, 102 C, 102 C, 103 C, 104 C, 105 C,  
106 C, 107 C, 108 C, 109 C, 110 C, 111 C, 112 C, 112 C, 113 C, 114 C,  
115 C, 116 C, 117 C, 118 C, 119 C, 120 C, 120 C, 121 C, 122 C, 123 C,  
124 C, 125 C, 126 C, 127 C, 127 C, 128 C, 129 C, 130 C, 131 C, 132 C,  
133 C, 133 C, 134 C, 135 C, 136 C, 137 C, 138 C, 138 C, 139 C, 140 C,  
141 C, 142 C, 143 C, 143 C, 144 C, 145 C, 146 C, 147 C, 148 C, 148 C,  
149 C, 150 C, 151 C, 152 C, 152 C, 153 C, 154 C, 155 C, 156 C, 156 C,  
157 C, 158 C, 159 C, 160 C, 160 C, 161 C, 162 C, 163 C, 163 C, 164 C,  
165 C, 166 C, 166 C, 167 C, 168 C, 169 C, 169 C, 170 C, 171 C, 172 C,  
172 C, 173 C, 174 C, 175 C, 175 C, 176 C, 177 C, 177 C, 178 C, 179 C,  .( .)
180 C, 180 C, 181 C, 182 C, 182 C, 183 C, 184 C, 185 C, 185 C, 186 C,  
187 C, 187 C, 188 C, 189 C, 189 C, 190 C, 191 C, 191 C, 192 C, 193 C,  
193 C, 194 C, 195 C, 195 C, 196 C, 196 C, 197 C, 198 C, 198 C, 199 C,  
200 C, 200 C, 201 C, 201 C, 202 C, 203 C, 203 C, 204 C, 204 C, 205 C,  
206 C, 206 C, 207 C, 207 C, 208 C, 209 C, 209 C, 210 C, 210 C, 211 C,  
211 C, 212 C, 213 C, 213 C, 214 C, 214 C, 215 C, 215 C, 216 C, 216 C,  
217 C, 217 C, 218 C, 218 C, 219 C, 219 C, 220 C, 220 C, 221 C, 221 C,  
222 C, 222 C, 223 C, 223 C, 224 C, 224 C, 225 C, 225 C, 226 C, 226 C,  
227 C, 227 C, 228 C, 228 C, 228 C, 229 C, 229 C, 230 C, 230 C, 231 C,  
231 C, 231 C, 232 C, 232 C, 233 C, 233 C, 234 C, 234 C, 234 C, 235 C,  .( .)
235 C, 235 C, 236 C, 236 C, 237 C, 237 C, 237 C, 238 C, 238 C, 238 C,  
239 C, 239 C, 239 C, 240 C, 240 C, 240 C, 241 C, 241 C, 241 C, 242 C,  
242 C, 242 C, 243 C, 243 C, 243 C, 244 C, 244 C, 244 C, 244 C, 245 C,  
245 C, 245 C, 246 C, 246 C, 246 C, 246 C, 247 C, 247 C, 247 C, 247 C,  
248 C, 248 C, 248 C, 248 C, 249 C, 249 C, 249 C, 249 C, 249 C, 250 C,  
250 C, 250 C, 250 C, 250 C, 251 C, 251 C, 251 C, 251 C, 251 C, 251 C,  
252 C, 252 C, 252 C, 252 C, 252 C, 252 C, 253 C, 253 C, 253 C, 253 C,  
253 C, 253 C, 253 C, 253 C, 254 C, 254 C, 254 C, 254 C, 254 C, 254 C,  
254 C, 254 C, 254 C, 254 C, 254 C, 254 C, 255 C, 255 C, 255 C, 255 C,  
255 C, 255 C, 255 C, 255 C, 255 C, 255 C, 255 C, 255 C, 255 C, 255 C,  .( .)
255 C, 255 C, 255 C,                                                   

\ Precomputed sin table:  atan(x/256)*256-1   for n=0..399
\ Stored as signed 8-bit values 
CREATE ATAN-TABLE 
DECIMAL 
-01 C, 000 C, 001 C, 002 C, 003 C, 004 C, 005 C, 006 C, 007 C, 008 C,  
009 C, 010 C, 011 C, 012 C, 013 C, 014 C, 015 C, 016 C, 017 C, 018 C,  
019 C, 020 C, 021 C, 022 C, 023 C, 024 C, 025 C, 026 C, 027 C, 028 C,  
029 C, 030 C, 031 C, 032 C, 033 C, 034 C, 035 C, 036 C, 037 C, 038 C,  
039 C, 040 C, 041 C, 042 C, 043 C, 044 C, 045 C, 046 C, 047 C, 048 C,  
049 C, 050 C, 051 C, 052 C, 053 C, 054 C, 055 C, 056 C, 057 C, 057 C,  
058 C, 059 C, 060 C, 061 C, 062 C, 063 C, 064 C, 065 C, 066 C, 067 C,  .( .)
068 C, 069 C, 070 C, 071 C, 071 C, 072 C, 073 C, 074 C, 075 C, 076 C,  
077 C, 078 C, 079 C, 080 C, 081 C, 082 C, 082 C, 083 C, 084 C, 085 C,  
086 C, 087 C, 088 C, 089 C, 090 C, 090 C, 091 C, 092 C, 093 C, 094 C,  
095 C, 096 C, 096 C, 097 C, 098 C, 099 C, 100 C, 101 C, 102 C, 102 C,  
103 C, 104 C, 105 C, 106 C, 107 C, 107 C, 108 C, 109 C, 110 C, 111 C,  
112 C, 112 C, 113 C, 114 C, 115 C, 116 C, 116 C, 117 C, 118 C, 119 C,  
120 C, 120 C, 121 C, 122 C, 123 C, 124 C, 124 C, 125 C, 126 C, 127 C,  
127 C, 128 C, 129 C, 130 C, 131 C, 131 C, 132 C, 133 C, 134 C, 134 C,  
135 C, 136 C, 137 C, 137 C, 138 C, 139 C, 139 C, 140 C, 141 C, 142 C,  .( .)
142 C, 143 C, 144 C, 145 C, 145 C, 146 C, 147 C, 147 C, 148 C, 149 C,  
149 C, 150 C, 151 C, 151 C, 152 C, 153 C, 154 C, 154 C, 155 C, 156 C,  
156 C, 157 C, 158 C, 158 C, 159 C, 160 C, 160 C, 161 C, 161 C, 162 C,  
163 C, 163 C, 164 C, 165 C, 165 C, 166 C, 167 C, 167 C, 168 C, 168 C,  
169 C, 170 C, 170 C, 171 C, 172 C, 172 C, 173 C, 173 C, 174 C, 175 C,  
175 C, 176 C, 176 C, 177 C, 178 C, 178 C, 179 C, 179 C, 180 C, 180 C,  
181 C, 182 C, 182 C, 183 C, 183 C, 184 C, 184 C, 185 C, 186 C, 186 C,  
187 C, 187 C, 188 C, 188 C, 189 C, 189 C, 190 C, 190 C, 191 C, 192 C,  
192 C, 193 C, 193 C, 194 C, 194 C, 195 C, 195 C, 196 C, 196 C, 197 C, 
197 C, 198 C, 198 C, 199 C, 199 C, 200 C, 200 C, 201 C, 201 C, 202 C, 
202 C, 203 C, 203 C, 204 C, 204 C, 205 C, 205 C, 206 C, 206 C, 207 C,  .( .)
207 C, 208 C, 208 C, 209 C, 209 C, 209 C, 210 C, 210 C, 211 C, 211 C, 
212 C, 212 C, 213 C, 213 C, 214 C, 214 C, 214 C, 215 C, 215 C, 216 C, 
216 C, 217 C, 217 C, 218 C, 218 C, 218 C, 219 C, 219 C, 220 C, 220 C, 
220 C, 221 C, 221 C, 222 C, 222 C, 223 C, 223 C, 223 C, 224 C, 224 C, 
225 C, 225 C, 225 C, 226 C, 226 C, 227 C, 227 C, 227 C, 228 C, 228 C, 
229 C, 229 C, 229 C, 230 C, 230 C, 231 C, 231 C, 231 C, 232 C, 232 C, 
232 C, 233 C, 233 C, 234 C, 234 C, 234 C, 235 C, 235 C, 235 C, 236 C, 
236 C, 236 C, 237 C, 237 C, 238 C, 238 C, 238 C, 239 C, 239 C, 239 C, 
240 C, 240 C, 240 C, 241 C, 241 C, 241 C, 242 C, 242 C, 242 C, 243 C, 
243 C, 243 C, 244 C, 244 C, 244 C, 245 C, 245 C, 245 C, 246 C, 246 C, 
246 C, 247 C, 247 C, 247 C, 248 C, 248 C, 248 C, 249 C, 249 C, 249 C, 
250 C, 250 C, 250 C, 250 C, 251 C, 251 C, 251 C, 252 C, 252 C, 252 C, 
253 C, 253 C, 253 C, 253 C, 254 C, 254 C, 254 C, 255 C, 255 C, 255 C,  .( .)


\ given argument x in suitable range and lookup-table address a, 
\ return (y+1).
\ special case when x is zero, y is zero.
\ Tipical usage:  SIN-TABLE FETCH-TABLE
: FETCH-TABLE ( x a -- y )
  OVER IF
    + C@ 1+
  ELSE
    DROP 
  THEN
;  


\ arctan for small angles
: ATAN1 ( x -- n )
  \ Lookup: argument [0.0, 1.55] maps to table index [0, 399]
  ATAN-TABLE FETCH-TABLE ;


: ATAN ( x -- angle )
  DUP IF                \ x
    DUP ABS             \ s |x|
    \ if |x| > 1, use arctan(x) = pi/2 - arctan(1/x)
    DUP [ 1.5 D>F LITERAL ] > IF     
      FP-1.0 SWAP FP/   \ s  1/x 
      ATAN1 NEGATE      \ s -arctan(1/x)
      FP-PI/2 FP+       \ 
    ELSE
      ATAN1  
    THEN            
    SWAP +-
  THEN
;

\ ATAN2     ( y x -- angle )s
\ Returns the angle in radians Q8.8 of point (x,y).
\ Range: (-PI, PI]
: ATAN2 ( y x -- angle )
    2DUP OR    IF               \ (0,0) case
        OVER ABS OVER ABS       \ |y| |x|
        2DUP < IF               \ if |y| > |x|
            SWAP                \ ensure |x| >= |y|
            FP/ ATAN            \ atan(|y|/|x|)
            FP-PI/2 SWAP FP-    \ PI/2 - atan(|y|/|x|)
        ELSE
            FP/ ATAN            \ atan(|y|/|x|)
        THEN

        \ Apply quadrant signs
        ROT SWAP                \ restore original y x (with signs)
        OVER 0< IF              \ x < 0 ?
            FP-PI FP+ 
            OVER 0< IF NEGATE THEN
        ELSE
            OVER 0< IF NEGATE THEN
        THEN

        NIP                     \ drop x
        NORMALIZE-ANGLE
    ELSE
        2DROP 0
    THEN

;


\ Sine function using lookup table with quadrant symmetry
\ Input: angle in radians (Q8.8 format), any range
\ Output: sine value (Q8.8 format, -256..+256 represents -1.0..+1.0)
\ Table: 403 entries covering [0, pi/2] with linear interpolation
: FSIN    ( radians-fp -- sin-fp )
  DUP IF
    FP-PI /MOD >R               \ R: quotient (p multiples), TOS: remainder [-p,+p]
    DUP >R                      \ R: quotient remainder, save remainder sign
    ABS                         \ Work with |remainder| [0,p]
    
    \ Reduce to first quadrant using symmetry
    DUP FP-PI/2 > IF            \ If in second quadrant [p/2, p]
        FP-PI/2 -               \ Subtract p/2
        FP-PI/2 SWAP -          \ Mirror: sin(p-x) = sin(x)
    THEN
    
    \ Lookup: angle now [0, p/2] maps to table index [0, 402]
    SIN-TABLE FETCH-TABLE
    
    R> +-                       \ Apply remainder sign
    R> -1 AND IF NEGATE THEN    \ Odd quotient means p shift ? negate
  ELSE
    0
  THEN
;

\ Cosine via phase shift: cos(x) = sin(x + p/2)
\ But implemented as: cos(x) = -sin(x - p/2) for efficiency
: FCOS  ( radians-fp -- cos-fp )
  FP-PI/2 - FSIN NEGATE
;


\ Tangent by definition tan := sin/cos
: FTAN  ( radians-fp -- tan-fp )
  DUP FSIN SWAP FCOS FP/ 
;



