\
\ CHOMP-AI-TESTS.f
\
\ Unit tests for the ghost AI arithmetic of demo/chomp-chomp.f.
\
\ Load the game FIRST, then this file:
\     INCLUDE demo/chomp-chomp.f
\     INCLUDE test/CHOMP-AI-TESTS.f
\
\ These cover the part of the AI that a human eye cannot check: the
\ targeting arithmetic.  In particular the UP cases of Pinky and Inky are
\ exactly what a wrong row/column mapping would mirror without producing
\ any visible error, so they are tested explicitly.
\
\ Coordinates here follow the game, NOT the arcade: x-pos is the ROW and
\ y-pos is the COLUMN.  Every test is written as (r,c).
\
\ Running these scrambles the live sprite positions and the phase timer;
\ the suite calls init-all at the end to put the game back.
\

.( CHOMP-AI-TESTS )

NEEDS TESTING


\ =========================================================================
\ helpers: place an actor and set a target by hand
\ =========================================================================

: !pac  ( r c d -- )
    pacman
    sprite@ dir   c!
    sprite@ y-pos c!
    sprite@ x-pos c! ;

: !blinky ( r c -- )
    blinky
    sprite@ y-pos c!
    sprite@ x-pos c! ;

: !ted ( r c -- )
    ted
    sprite@ y-pos c!
    sprite@ x-pos c! ;

: !g ( r c d n -- )
    sprite#
    sprite@ dir   c!
    sprite@ y-pos c!
    sprite@ x-pos c! ;

: !tgt ( r c -- )  tgt-c ! tgt-r ! ;


\ =========================================================================
\ 1. geometry
\ =========================================================================

\ the four direction codes sum to 109 in pairs, which is the whole trick
T{ key-up    opposite -> key-down  }T
T{ key-down  opposite -> key-up    }T
T{ key-left  opposite -> key-right }T
T{ key-right opposite -> key-left  }T

T{ 10 12 key-up    step-cell ->  9 12 }T
T{ 10 12 key-down  step-cell -> 11 12 }T
T{ 10 12 key-left  step-cell -> 10 11 }T
T{ 10 12 key-right step-cell -> 10 13 }T

T{ 0 0 3 4 dist2 -> 25 }T
T{ 5 5 5 5 dist2 ->  0 }T
T{ 10 10 2 10 dist2 -> 64 }T
T{ 2 10 10 10 dist2 -> 64 }T          \ symmetric


\ =========================================================================
\ 2. the offset, including the arcade overflow bug
\ =========================================================================

T{ 4 key-right dir-delta ->  0  4 }T
T{ 4 key-left  dir-delta ->  0 -4 }T
T{ 4 key-down  dir-delta ->  4  0 }T

\ Facing UP the original 8080 code also picks up a LEFT offset of the
\ same size.  Kept on purpose: Pinky's ambushes depend on it.
T{ 4 key-up    dir-delta -> -4 -4 }T
T{ 2 key-up    dir-delta -> -2 -2 }T


\ =========================================================================
\ 3. scatter corners
\ =========================================================================

T{ 0 scatter-cell -> 22 23 }T         \ Inky   bottom-right
T{ 1 scatter-cell ->  0  1 }T         \ Pinky  top-left
T{ 2 scatter-cell ->  0 23 }T         \ Blinky top-right
T{ 3 scatter-cell -> 22  1 }T         \ Ted    bottom-left


\ =========================================================================
\ 4. the four personalities
\ =========================================================================

\ Blinky goes straight at Pac-Man's own cell, whichever way he faces
T{ 10 12 key-right !pac  blinky-target  tgt-r @ tgt-c @ -> 10 12 }T
T{ 10 12 key-up    !pac  blinky-target  tgt-r @ tgt-c @ -> 10 12 }T

\ Pinky aims four cells ahead
T{ 10 12 key-right !pac  pinky-target  tgt-r @ tgt-c @ -> 10 16 }T
T{ 10 12 key-left  !pac  pinky-target  tgt-r @ tgt-c @ -> 10  8 }T
T{ 10 12 key-down  !pac  pinky-target  tgt-r @ tgt-c @ -> 14 12 }T

\ ...except facing up, where the bug adds four to the left as well
T{ 10 12 key-up    !pac  pinky-target  tgt-r @ tgt-c @ ->  6  8 }T

\ Inky doubles the vector from Blinky to the cell two ahead of Pac-Man.
\ Pac-Man (10,12) facing right -> O = (10,14); Blinky (10,10)
\ target = ( 2*10-10 , 2*14-10 ) = (10,18)
T{ 10 12 key-right !pac  10 10 !blinky
   inky-target  tgt-r @ tgt-c @ -> 10 18 }T

\ With Blinky far away the doubled vector runs off the maze.  A negative
\ target is correct and harmless: it is only ever an operand of a
\ subtraction, never an index into the maze.
\ Pac-Man (5,5) facing up -> O = (3,3); Blinky (10,20)
\ target = ( 2*3-10 , 2*3-20 ) = (-4,-14)
T{ 5 5 key-up !pac  10 20 !blinky
   inky-target  tgt-r @ tgt-c @ -> -4 -14 }T

\ Ted chases while 8 or more cells away and peels off when closer.
\ Exactly on the ring: dist2 = 64 -> still chasing
T{ 10 10 !ted  10 18 key-right !pac  ted
   ted-target  tgt-r @ tgt-c @ -> 10 18 }T

\ Just outside: dist2 = 1 + 64 = 65 -> chasing
T{ 10 10 !ted  11 18 key-right !pac  ted
   ted-target  tgt-r @ tgt-c @ -> 11 18 }T

\ Just inside: dist2 = 49 -> runs for his own corner instead
T{ 10 10 !ted  10 17 key-right !pac  ted
   ted-target  tgt-r @ tgt-c @ -> 22  1 }T


\ =========================================================================
\ 5. choosing a direction
\ =========================================================================
\ Row 6 of the maze is a long open corridor; (5,10) and (7,10) are walls,
\ so at (6,10) only left and right are available.

\ heading up (so down is the forbidden reversal): picks the nearer side
T{ 6 10 key-up 0 !g   6  2 !tgt  choose-dir -> key-left  }T
T{ 6 10 key-up 0 !g   6 20 !tgt  choose-dir -> key-right }T

\ A genuine tie: (6,9) and (6,11) are both 26 away from (1,10).  The
\ scan order up > left > down > right with a strict < hands it to left.
T{ 6 10 key-up 0 !g   1 10 !tgt  choose-dir -> key-left }T

\ Heading right with the target behind him: a ghost never volunteers to
\ reverse, so he keeps going right even though left is closer.
T{ 6 10 key-right 0 !g  6 2 !tgt  choose-dir -> key-right }T

\ (4,5) is a sealed pocket of this maze: no legal exit at all.  Rather
\ than freeze, the chooser falls back to turning round.
T{ 4 5 key-right 0 !g   4 20 !tgt  choose-dir -> key-left }T


\ =========================================================================
\ 6. speed accumulator
\ =========================================================================

\ 192/256 = 75%: three steps in four ticks
T{ 0 sprite#  0 sprite@ accum c!  192 sprite@ speed c!
   ghost-step? ghost-step? ghost-step? ghost-step?
   + + + -> 3 }T

\ 128/256 = 50%: two steps in four ticks, the frightened rate
T{ 0 sprite#  0 sprite@ accum c!  128 sprite@ speed c!
   ghost-step? ghost-step? ghost-step? ghost-step?
   + + + -> 2 }T


\ =========================================================================
\ 7. forced reversal
\ =========================================================================

T{ 0 sprite#  key-right sprite@ dir c!  1 sprite@ rev? c!
   apply-reverse
   sprite@ dir c@  sprite@ rev? c@ -> key-left 0 }T

T{ 0 sprite#  key-right sprite@ dir c!  0 sprite@ rev? c!
   apply-reverse
   sprite@ dir c@ -> key-right }T


\ =========================================================================
\ 8. scatter / chase phases
\ =========================================================================

\ a level begins in scatter, for 70 ticks
T{ reset-phases  phase-t @ -> 70 }T
T{ reset-phases  scatter? @ 0= -> 0 }T

\ when the phase runs out the mode flips to chase for 200 ticks and every
\ ghost is told to turn round
T{ reset-phases  1 hunt !
   70 0 do tick-phase loop
   scatter? @ 0=  phase-t @ -> -1 200 }T
T{ 0 sprite# sprite@ rev? c@ -> 1 }T

\ the timer is suspended while the ghosts are frightened
T{ reset-phases  -1 hunt !
   30 0 do tick-phase loop
   phase-t @ -> 70 }T
1 hunt !


\ =========================================================================

CR .( CHOMP-AI-TESTS done - put the game back with: init-all ) CR

