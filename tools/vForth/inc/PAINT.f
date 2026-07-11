\
\ paint.f - Scanline Span Fill (Smith 1979)
\
.( PAINT )
\
NEEDS GRAPHICS
NEEDS FLIP

HEX

\ Explicit stack: ~256 seeds (x,y pairs); avoids R-stack overflow
CREATE PAINT-STACK 1024 ALLOT
VARIABLE PAINT-SP

: PAINT-CLEAR  0 PAINT-SP ! ;

: PAINT-PUSH ( x y -- )
    PAINT-SP @ 4 + DUP PAINT-STACK 1024 + > IF
        2DROP
    ELSE
        PAINT-STACK + 2!
        PAINT-SP !
    THEN
;

: PAINT-POP ( -- x y f )
    PAINT-SP @ 4 < IF  0 EXIT  THEN
    PAINT-SP @ 4 - PAINT-SP !
    PAINT-STACK PAINT-SP @ + 2@  -1
;

\ Find left boundary of span at (x,y), scanning leftward until edge
: (PAINT-SCAN-LEFT) ( x y -- x_left )
    >R
    BEGIN
        DUP 0 > IF
            DUP 1 - R@ 2DUP POINT EDGE NOT
        ELSE
            0
        THEN
    WHILE
        1 -
    REPEAT
    R> DROP
;

\ Find right boundary of span at (x,y), scanning rightward until edge
: (PAINT-SCAN-RIGHT) ( x y -- x_right )
    >R
    BEGIN
        DUP 1FF < IF
            DUP 1 + R@ 2DUP POINT EDGE NOT
        ELSE
            0
        THEN
    WHILE
        1 +
    REPEAT
    R> DROP
;

\ Fill span and push new seeds from adjacent rows
: (PAINT-FILL-SPAN) ( x_left x_right y -- )
    >R
    \ Fill the span
    R@ SWAP DO
        I R@ PLOT
    LOOP

    \ Check row y-1 for new seeds
    R@ 1 - 0 >= IF
        R@ 1 - >R
        R@ SWAP DO
            I R@ POINT EDGE NOT IF
                I R@ PAINT-PUSH
            THEN
        LOOP
        R> DROP
    THEN

    \ Check row y+1 for new seeds
    R@ 1 + 1FF < IF
        R@ 1 + >R
        R@ SWAP DO
            I R@ POINT EDGE NOT IF
                I R@ PAINT-PUSH
            THEN
        LOOP
        R> DROP
    THEN

    R> DROP
;

: PAINT  ( x y -- )
    PAINT-CLEAR  PAINT-PUSH

    BEGIN
        PAINT-POP
    WHILE
        2DUP POINT EDGE NOT IF
            \ Unfilled seed: find span bounds and fill
            2DUP (PAINT-SCAN-LEFT) >R  \ x_left
            ROT ROT (PAINT-SCAN-RIGHT) \ x_left x_right
            R> SWAP ROT               \ x_left x_right y
            (PAINT-FILL-SPAN)
        ELSE
            2DROP
        THEN
    REPEAT
;
