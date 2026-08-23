\
\ CHOMP-MAZE-TESTS.f
\
\ Unit tests for the Stage 4 maze-on-Screen infrastructure of
\ demo/chomp-chomp.f (MAZE-SCR0, load-maze, set-maze-run, MAZE-CHECK).
\
\ Load the game FIRST, then this file:
\     INCLUDE demo/chomp-chomp.f
\     INCLUDE test/CHOMP-MAZE-TESTS.f
\
\ Requires !Blocks-64.bin with disk maze #1 written to Screen 740/741
\ (a copy of the compiled maze, put there via util/putscr.pl -- see
\ prompts/CHOMP-CHOMP-STATUS.md).
\
\ Running these changes level and rewrites maze-run; the suite restores
\ level 0 and calls set-maze-run at the end, the same way
\ CHOMP-AI-TESTS.f restores state via init-all.
\

.( CHOMP-MAZE-TESTS )

NEEDS TESTING

\ lib/testing.f ends in HEX; the game is compiled decimal.
DECIMAL


\ =========================================================================
\ 1. BLOCK arithmetic -- the kind of off-by-one this project has already
\    hit elsewhere with block offsets, so it is checked by hand here too.
\    Screen 740 -> blocks 1480/1481; Screen 741 -> blocks 1482/1483.
\ =========================================================================

T{ 1 maze-blk0 -> 1480 }T
T{ 2 maze-blk0 -> 1484 }T
T{ 3 maze-blk0 -> 1488 }T


\ =========================================================================
\ 2. the pipeline preserves the game exactly: loading disk maze #1 from
\    Screen 740/741 must reproduce maze-run byte-for-byte identical to
\    the compiled maze-base path.  This is the acceptance test for the
\    whole slice ("does the pipeline preserve the game").
\ =========================================================================

create maze-run-save  24 21 * allot

: save-maze-run ( -- )
    maze-run maze-run-save 24 21 * cmove ;

variable maze-diff

: maze-run-same? ( -- f )
    0 maze-diff !
    24 21 * 0 do
        i maze-run + c@
        i maze-run-save + c@
        <> if 1 maze-diff ! then
    loop
    maze-diff @ 0= ;

T{ 0 level ! set-maze-run  save-maze-run
   1 level ! set-maze-run  maze-run-same? -> -1 }T


\ =========================================================================
\ 3. MAZE-CHECK: both loader paths (compiled maze-base, disk Screen
\    740/741) must come back clean -- they exercise different branches
\    of maze-check-load, so both need checking, not just one.
\ =========================================================================

T{ 0 MAZE-CHECK  check-errors @ -> 0 }T
T{ 1 MAZE-CHECK  check-errors @ -> 0 }T


\ =========================================================================
\ 4. MAZE-CHECK actually catches problems.  No disk write needed: corrupt
\    maze-check-buf directly after a clean load (maze-check-load is
\    public exactly so this is possible), then re-run a check in
\    isolation.
\ =========================================================================

\ isolate an existing pellet: (5,10) is a '.' in the middle of the long
\ open corridor "M...................J" (row index 5); its down
\ neighbour (row 6, col 10) is already a wall letter, but the up
\ neighbour (row 4, col 10) is open corridor too, so wall off all three
\ of up/left/right to seal it into a 1-cell island nothing can reach.
\ Collateral damage elsewhere is fine -- the assertion only checks that
\ SOMETHING trips, not an exact count.
T{ 0 check-errors !
   0 maze-check-load
   [char] A 4 10 check^ c!
   [char] A 5  9 check^ c!
   [char] A 5 11 check^ c!
   check-connectivity
   check-errors @ 0> -> -1 }T

\ a reachable cell on the outer edge: connectivity alone would not
\ catch this (an edge cell is not a "feature"), which is exactly why
\ check-perimeter exists.  Poke the byte-1 reachability marker directly
\ instead of engineering a real leak path -- this tests check-perimeter
\ in isolation, independent of flood-fill's own correctness (already
\ covered by the previous test).
T{ 0 check-errors !
   0 maze-check-load
   1 0 12 check^ c!
   check-perimeter
   check-errors @ -> 1 }T


\ =========================================================================
\ Back to the state the game expects: level 0, maze-run rebuilt from the
\ compiled maze.
\ =========================================================================

0 level !
set-maze-run

CR .( CHOMP-MAZE-TESTS done - level 0 / maze-run restored ) CR

