\
\ wildcard^.f
\
.( WILDCARD? )
\
\ DOS-style glob match: * matches zero or more characters, ? matches
\ exactly one character. Case-insensitive. Classic iterative match with
\ backtrack to the last seen '*' (star-position in both pattern and string).
\

BASE @ DECIMAL

VARIABLE WC-PA          \ pattern base address
VARIABLE WC-PN          \ pattern length
VARIABLE WC-SA          \ string base address
VARIABLE WC-SN          \ string length
VARIABLE WC-P           \ pattern index
VARIABLE WC-S           \ string index
VARIABLE WC-STARP       \ pattern index of last '*' seen (-1 = none)
VARIABLE WC-STARS       \ string index at that '*'

: WC-PC@ ( i -- c )  WC-PA @ + C@ ;
: WC-SC@ ( i -- c )  WC-SA @ + C@ ;

\ do pattern char at pi and string char at si match (case-insensitive) ?
: WC-EQ? ( pi si -- flag )
    WC-SC@ UPPER  SWAP WC-PC@ UPPER  =
;

\ retry from the last '*' if one was seen, else fail
: WC-BACKTRACK ( -- flag )
    WC-STARP @ 0< 0= IF
        WC-STARP @ 1+ WC-P !
        WC-STARS @ 1+ DUP WC-STARS ! WC-S !
        -1
    ELSE
        0
    THEN
;

: WILDCARD?  ( pat-a pat-n str-a str-n -- flag )
    WC-SN !  WC-SA !  WC-PN !  WC-PA !
    0 WC-P !  0 WC-S !  -1 WC-STARP !  -1 WC-STARS !
    BEGIN
        WC-S @ WC-SN @ <
    WHILE
        WC-P @ WC-PN @ < IF
            WC-P @ WC-PC@ [CHAR] * = IF
                WC-P @ WC-STARP !
                WC-S @ WC-STARS !
                WC-P @ 1+ WC-P !
            ELSE
                WC-P @ WC-PC@ [CHAR] ? = IF
                    WC-P @ 1+ WC-P !
                    WC-S @ 1+ WC-S !
                ELSE
                    WC-P @ WC-S @ WC-EQ? IF
                        WC-P @ 1+ WC-P !
                        WC-S @ 1+ WC-S !
                    ELSE
                        WC-BACKTRACK NOT IF 0 EXIT THEN
                    THEN
                THEN
            THEN
        ELSE
            WC-BACKTRACK NOT IF 0 EXIT THEN
        THEN
    REPEAT
    BEGIN
        WC-P @ WC-PN @ <  WC-P @ WC-PC@ [CHAR] * =  AND
    WHILE
        WC-P @ 1+ WC-P !
    REPEAT
    WC-P @ WC-PN @ =
;

BASE !
