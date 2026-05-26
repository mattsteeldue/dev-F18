\
\ Fedora.f
\

needs sqrt
needs graphics
needs .at
needs flip

marker task

( Sine Cosine Table for rad/64 )
( input between 000 and 101 )
( output is x 16384 )
CREATE SIN-TABLE
00000 , 00256 , 00512 , 00768 , 01023 , 01279 , 01534 , 
01788 , 02043 , 02296 , 02550 , 02802 , 03054 , 03305 , 
03555 , 03805 , 04053 , 04301 , 04547 , 04793 , 05037 , 
05280 , 05522 , 05762 , 06001 , 06238 , 06474 , 06709 , 
06942 , 07173 , 07402 , 07629 , 07855 , 08079 , 08300 , 
08520 , 08738 , 08953 , 09166 , 09377 , 09586 , 09793 , 
09997 , 10198 , 10397 , 10594 , 10788 , 10979 , 11168 , 
11354 , 11537 , 11717 , 11895 , 12070 , 12241 , 12410 , 
12575 , 12738 , 12897 , 13054 , 13207 , 13357 , 13503 , 
13647 , 13787 , 13923 , 14057 , 14186 , 14313 , 14435 , 
14555 , 14671 , 14783 , 14891 , 14996 , 15098 , 15195 , 
15289 , 15379 , 15466 , 15548 , 15627 , 15702 , 15773 , 
15840 , 15904 , 15964 , 16019 , 16071 , 16119 , 16163 , 
16203 , 16239 , 16271 , 16299 , 16323 , 16343 , 16359 , 
16371 , 16379 , 16383 , 16384 , 


\ argument is rad scaled / 64
\ result   is scaled / 16384
: Sin    ( rad -- n/64 )
    201 /mod >R dup >R abs              \ |q|         R: r q
    dup 101 >                           \ |q|  f        
    if 201 swap - then                  \ |q|  or  pi-|q|
    2* sin-table + @                    \ |sin|   
    R> +-                               \ |sin| with sign of q
    R> 1 and  if negate then            \ sin   with quadrant
;

\ DIM rr(320)
\ FOR i=0 TO 320
\   rr(i)=193
\ NEXT i
create rr 512 allot 

variable zi
variable xl     
variable xt
variable x1
variable y1
variable yy
variable zs 0 , \ double
variable s1
variable s3

: debug ( xi -- )
    0 0 .at
    ." zi : " zi  @         . 6 spaces cr
    ." zs : " zs 2@         . drop 6 spaces cr
    ." xl : " xl  @         . 6 spaces cr
    ." xi : "               . 6 spaces cr
    ." xt : " xt  @         . 6 spaces cr
    ." s1 : " s1  @         . 6 spaces cr
    ." s3 : " s3  @         . 6 spaces cr
    ." yy : " yy  @         . 6 spaces cr
    ." x1 : " x1  @         . 6 spaces cr
    ." y1 : " y1  @         . 6 spaces cr
;


: row-loop ( xl -- )
    cls
    2*
    dup negate                      \  xl  -xl
    ?do
        i dup um* zs 2@ D+          \            xi*xi+zs           x 65536
        DSqrt  dup xt !             \     xt=SQR(xi*xi+zs)          x 256
        2/ 2/                       \        SQR(xi*xi+zs)          x 64
        dup Sin dup s1 !            \  s1=SIN(xt)                   x 16384
        swap 768 * Sin dup s3 !     \  s3=SIN(3*xt)                 x 16384
        2 5 */ +                    \     SIN(xt)+SIN(xt*3)*0.4     x 16384
        56 16384 */      yy !       \ yy=(SIN(xt)+SIN(xt*3)*0.4)*56
        90  i + zi @ +   x1 !       \ x1=xi+zi+160
        90 yy + zi @ +   y1 !       \ y1=90-yy+zi

        \ x1 @ 0< not if              \ IF x1<0 THEN GOTO 180
        \ y1 @ rr x1 @ + c@ < if      \ IF rr(x1)<=y1 THEN GOTO 180
        \   y1 @ rr x1 @ + c!       \     rr(x1)=y1   
            192 yy @ - 
            x1 @ 
            plot                    \     PLOT 69,x1*4,850-y1*4+32
        \ then
        \ then

        i debug
        \ key drop 
        ?terminal if leave then
        
    loop \   NEXT xi
;

: fedora
    rr 512 193 fill
    -128 128 do                         \ FOR zi=64 TO -64 STEP -2  x 2
        i 2/ zi !
        0 20736                         \ 20736=144*144             x 65536

        i dup * 2*                      \     zi*zi                 x 4
        41472                           \ 5.0625                    x 8192
        um*                             \    (zi*2.25)*(zi*2.25)    x 32768 
        2dup D+                         \    (zi*2.25)*(zi*2.25)    x 65536 
        2dup zs 2!                      \ zs=(zi*2.25)*(zi*2.25)    x 65536 
        dnegate                         \ -zs
        D+ DSqrt                        \        SQR(20736-zs)      x 256 
        128 +                           \       (SQR(20736-zs)+0.5) x 256
        flip xl c!                      \ xl=int(SQR(20736-zs)+0.5) x 1
        xl c@ row-loop
        ?terminal if leave then
    -4 +loop                            \ NEXT zi
; 


