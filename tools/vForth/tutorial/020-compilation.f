\
\ 020-compilation.f
\ Compilation internals: STATE, [ ], IMMEDIATE, POSTPONE, COMPILE,.
\
\ Forth blurs the boundary between interpretation and compilation.
\ Understanding STATE, immediate words, and POSTPONE lets you write
\ words that behave differently depending on whether they run at
\ compile time or interpret time.
\
\ Core words (no NEEDS):
\   STATE    -- user variable: 0=interpreting, nonzero=compiling
\   [        -- switch to interpret state (immediate)
\   ]        -- switch to compile state
\   IMMEDIATE -- mark the last-defined word as immediate
\   COMPILE,  -- compile the CFA at TOS into the current definition
\   COMPILE   -- compile a literal CFA into the definition (old-style)
\   [COMPILE] -- force-compile an immediate word (old-style)
\
\ POSTPONE requires NEEDS (in inc/postpone.f).
\ ['] requires NEEDS (in inc/['].f).
\
\ Reference: sec.2.12.4
\
\ Load from a clean session:
\   NEEDS TUTORIAL
\   020 TUTORIAL
\ To unload and reload interactively:
\   NEWTASK 020 TUTORIAL
\

MARKER NEWTASK

CR
.( --- Tutorial 020: compilation loaded. ) CR
.(     Type NEWTASK to unload.   ) CR

NEEDS POSTPONE
NEEDS [']


\ ===========================================================================
\ 1. STATE -- what mode are we in?
\ ===========================================================================
\
\ STATE ( -- a )  returns the address of the state flag.
\   STATE @   => 0       (interpreting)
\   STATE @   => nonzero (compiling, inside : ... ; )
\
\ The interpreter reads STATE to decide whether to execute or compile
\ each word it encounters.

: .STATE  ( -- )
    STATE @ IF  ." compiling"  ELSE  ." interpreting"  THEN  CR ;

.( Try: .STATE   ) CR        \ => interpreting
.( Try: : FOO  .STATE ;  FOO  ) CR  \ => interpreting (runs at runtime)


\ ===========================================================================
\ 2. [ and ]  --  escape hatch from compilation
\ ===========================================================================
\
\ Inside a colon definition, [ ... ] switches temporarily to interpret
\ mode.  The words between [ and ] are executed immediately at compile
\ time, not compiled.
\
\ Common use: compute a constant at compile time:
\
\   : DAYS-IN-YEAR   [ 7 52 * ] LITERAL ;
\                      ^^^^^^^
\                    executed at compile time; result compiled as literal
\
\   : LIMIT   [ BL 1+ ] LITERAL ;   \ BL+1 = 33 = !

: COMPILE-TIME-DEMO  ( -- n )
    [ 2 3 + ] LITERAL ;     \ 5 is compiled as a literal

.( Try: COMPILE-TIME-DEMO .  ) CR   \ => 5


\ ===========================================================================
\ 3. IMMEDIATE -- words that run at compile time
\ ===========================================================================
\
\ A word marked IMMEDIATE is always executed, even inside : ... ; .
\ Control-flow words (IF ELSE THEN DO LOOP) and [ are all immediate.
\
\ Pattern for a dual-mode word:
\
\   : MY-WORD  ( ... -- ... )
\       STATE @ IF
\           \ compile-time behaviour
\       ELSE
\           \ interpret-time behaviour
\       THEN  ;
\   IMMEDIATE

: ?COMPILING  ( -- )
    STATE @ IF
        ." (inside a definition)"
    ELSE
        ." (at the prompt)"
    THEN  CR ;
IMMEDIATE

.( Try: ?COMPILING                ) CR  \ runs at prompt => at the prompt
.( Try: : TEST-IMMED  ?COMPILING ; ) CR \ runs at compile time


\ ===========================================================================
\ 4. COMPILE,  --  compiling an xt
\ ===========================================================================
\
\ COMPILE, ( xt -- )  appends xt to the current definition.
\ This is the low-level operation behind all compilation.
\
\ Example: a word that compiles DUP into the current definition:
\
\   : COMPILE-DUP  ( -- )   ['] DUP  COMPILE, ;  IMMEDIATE
\
\ Then:   : TRIPLE  ( n -- n n n )  COMPILE-DUP  COMPILE-DUP ;
\ is equivalent to:   : TRIPLE  DUP DUP ;

: COMPILE-DUP  ( -- )   ['] DUP  COMPILE, ;  IMMEDIATE

: TRIPLE  ( n -- n n n )   COMPILE-DUP  COMPILE-DUP ;

.( Try: 5 TRIPLE .S 2DROP .  ) CR   \ => 5 5 5


\ ===========================================================================
\ 5. POSTPONE  --  the modern way to compile immediate words
\ ===========================================================================
\
\ POSTPONE name  compiles the compilation-semantics of name, whether or
\ not name is immediate.  It replaces both COMPILE and [COMPILE].
\
\ If name is NOT immediate: same as [ ' name ] LITERAL COMPILE,
\ If name IS immediate:      same as [COMPILE] name
\
\ Example: a word that conditionally compiles a SWAP:
\
\   : ?SWAP  ( f -- )
\       IF  POSTPONE SWAP  THEN ;  IMMEDIATE

: COMPILE-SWAP-IF  ( f -- )
    IF  POSTPONE SWAP  THEN ;  IMMEDIATE

: TEST-POSTPONE  ( -- )
    [ -1 ] LITERAL  COMPILE-SWAP-IF
    1 2 ;   \ if flag was true, stack becomes 2 1

.( Try: TEST-POSTPONE . .  ) CR   \ => 2 1


\ ===========================================================================
\ 6. Summary: compile-time vs runtime dispatch
\ ===========================================================================
\
\ Technique         When to use
\ -----------------------------------------------
\ [ ... ]           Compute constants at compile time
\ IMMEDIATE         Word runs at compile time (and at prompt)
\ STATE @           Query mode to write dual-behaviour words
\ COMPILE,          Low-level: append xt to current definition
\ POSTPONE          High-level: compile semantics of any word


\ ===========================================================================
\ 7. Simple tests (requires NEEDS TESTING)
\ ===========================================================================
\
\ NEEDS TESTING
\ T{  COMPILE-TIME-DEMO  -> 5    }T
\ T{  5 TRIPLE           -> 5 5 5 }T
