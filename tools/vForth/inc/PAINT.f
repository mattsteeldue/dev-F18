\
\ paint.f
\
\ PAINT - flood fill via Scanline Span Fill (Smith 1979).
\ Replaces the old probe-from-seed-column algorithm that failed on any
\ concave shape (analysis and plan in prompts/PAINT-PLAN.md).
\
\ An explicit seed stack keeps the return-stack depth constant, so
\ large areas cannot overflow the return stack as recursion would.
\ The stack holds 256 seeds; on overflow new seeds are silently
\ dropped, which at worst leaves part of a pathological shape
\ (e.g. a fine comb) unfilled.
\
\ This file is pulled in by lib/GRAPHICS.f or lib/GRAPHICS-COMMON.f
\ via NEEDS PAINT: it compiles against the vectored primitives
\ PLOT POINT EDGE and the V-RANGE / H-RANGE values those modules
\ define. Do not load it on a bare system.
\
.( PAINT )
\
BASE @          \ save base status
HEX

\ seed stack: 256 seeds of two cells (x,y); PAINT-SP is a byte offset
CREATE PAINT-STACK 400 ALLOT
VARIABLE PAINT-SP

VARIABLE PAINT-Y1               \ span bounds on the current row
VARIABLE PAINT-Y2
VARIABLE PAINT-RUN              \ inside-a-free-run flag while seeding

: PAINT-PUSH  ( x y -- )        \ save a seed; silently drop when full
    PAINT-SP @ 400 U< IF
        PAINT-STACK PAINT-SP @ + 2!
        4 PAINT-SP +!
    ELSE
        2DROP
    THEN
;

: PAINT-POP  ( -- x y tf | ff ) \ tf with a seed, ff when empty
    PAINT-SP @ IF
        -4 PAINT-SP +!
        PAINT-STACK PAINT-SP @ + 2@
        -1
    ELSE
        0
    THEN
;

\ widen y towards 0 up to the last free pixel of the row
: (PAINT-YL)  ( x y -- yl )
    BEGIN
        DUP 0> IF
            2DUP 1- POINT EDGE NOT
        ELSE
            0
        THEN
    WHILE
        1-
    REPEAT
    SWAP DROP
;

\ widen y towards H-RANGE up to the last free pixel of the row
: (PAINT-YR)  ( x y -- yr )
    BEGIN
        DUP H-RANGE 1- < IF
            2DUP 1+ POINT EDGE NOT
        ELSE
            0
        THEN
    WHILE
        1+
    REPEAT
    SWAP DROP
;

\ plot the whole span PAINT-Y1..PAINT-Y2 of row x
: (PAINT-SPAN)  ( x -- x )
    PAINT-Y2 @ 1+  PAINT-Y1 @  DO
        DUP I PLOT
    LOOP
;

\ push one seed per free run of row nx inside the span bounds
: (PAINT-ROW)  ( nx -- nx )
    0 PAINT-RUN !
    PAINT-Y2 @ 1+  PAINT-Y1 @  DO
        DUP I POINT EDGE IF
            0 PAINT-RUN !
        ELSE
            PAINT-RUN @ 0= IF
                DUP I PAINT-PUSH
                1 PAINT-RUN !
            THEN
        THEN
    LOOP
;

\ fill the span through one seed, then queue the rows above and below
: (PAINT-SEED)  ( x y -- )
    2DUP POINT EDGE IF
        2DROP EXIT
    THEN
    2DUP (PAINT-YR) PAINT-Y2 !
    OVER >R (PAINT-YL) PAINT-Y1 ! R>
    (PAINT-SPAN)                ( x )
    DUP IF
        DUP 1- (PAINT-ROW) DROP
    THEN
    DUP 1+ V-RANGE U< IF
        DUP 1+ (PAINT-ROW) DROP
    THEN
    DROP
;

: PAINT  ( x y -- )
    0 PAINT-SP !
    PAINT-PUSH
    BEGIN
        PAINT-POP
    WHILE
        (PAINT-SEED)
        ?TERMINAL IF 0 PAINT-SP ! THEN  \ [BREAK] empties the seed stack
    REPEAT
;

BASE !
