
needs J
needs GRAPHICS

\ Patrick Kaell

CREATE TRIGTABLE
    0 ,   286 ,   572 ,   857 ,  1143 ,  1428 ,  1713 ,  1997 ,
 2280 ,  2563 ,  2845 ,  3126 ,  3406 ,  3686 ,  3964 ,  4240 ,
 4516 ,  4790 ,  5063 ,  5334 ,  5604 ,  5872 ,  6138 ,  6402 ,
 6664 ,  6924 ,  7182 ,  7438 ,  7692 ,  7943 ,  8192 ,  8438 ,
 8682 ,  8923 ,  9162 ,  9397 ,  9630 ,  9860 , 10087 , 10311 ,
10531 , 10749 , 10963 , 11174 , 11381 , 11585 , 11786 , 11982 ,
12176 , 12365 , 12551 , 12733 , 12911 , 13085 , 13255 , 13421 ,
13583 , 13741 , 13894 , 14044 , 14189 , 14330 , 14466 , 14598 ,
14726 , 14849 , 14968 , 15082 , 15191 , 15296 , 15396 , 15491 ,
15582 , 15668 , 15749 , 15826 , 15897 , 15964 , 16026 , 16083 ,
16135 , 16182 , 16225 , 16262 , 16294 , 16322 , 16344 , 16362 ,
16374 , 16382 , 16384 ,

: SIN
    DUP 360 > IF
        360 MOD
    ELSE
        DUP 0< IF
            360 MOD
            360 +
        THEN
    THEN
    2* DUP 180 < IF
        TRIGTABLE + @
    ELSE
        DUP 360 < IF
            NEGATE 360 + TRIGTABLE + @
        ELSE
            DUP 540 < IF
                360 - TRIGTABLE + @ NEGATE
            ELSE
                NEGATE 720 + TRIGTABLE + @ NEGATE
            THEN
        THEN
    THEN
;

: SQR
    DUP 1
    BEGIN 2DUP > WHILE
    + 2/ 2DUP /
    REPEAT
    ROT 2DROP
;

CREATE RR 642 ALLOT

VARIABLE ZS
VARIABLE XL
VARIABLE XI
VARIABLE XT
VARIABLE YY
VARIABLE X1
VARIABLE Y1

: FEDORA
    0 MODE
    642 0 DO
        1000 RR I + !
    2 +LOOP

    -64 64 DO
        I I * 81 16 */ ZS !
        20736 ZS @ - SQR XL !
        XL @ 1+ XL @ NEGATE DO
            I I * ZS @ + SQR 27192 16384 */ XT !
            XT @ SIN XT @ 3 * SIN 2 5 */ + 56 16384 */ YY !
            I J + 160 + X1 !
            90 YY @ - J + Y1 !
            X1 @ 0 < NOT IF
                RR X1 @ 2* + @ Y1 @ > IF
                    Y1 @ RR X1 @ 2* + !
                     69 X1 @ 4 * 900 Y1 @ 4 * - PLOT
                THEN
            THEN
        LOOP
    -2 +LOOP
;