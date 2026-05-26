\
\ 013-case.f
\ Multi-branch dispatch: CASE OF ENDOF ENDCASE.
\
\ CASE is a cleaner alternative to deeply nested IF...ELSE...THEN
\ when matching one value against a set of constants.  Internally it
\ compares the test value against each case constant and jumps to the
\ matching branch, or falls through to a default section.
\
\ CASE, OF, ENDOF, ENDCASE are IMMEDIATE words in vForth; they are
\ not in the core and must be loaded with NEEDS CASE.
\
\ The test value n stays on the data stack while each OF branch is
\ tested.  A matching OF consumes both the test value and the case
\ constant.  A non-matching OF drops only the case constant.  After
\ the last ENDOF, the test value is still on the stack and is
\ available in the default section.  ENDCASE always drops it.
\
\ Reference: sec.2.12.7
\
\ Load from a clean session:
\   INCLUDE tutorial/013-case.f
\ To unload and reload interactively:
\   NO-CASE
\   INCLUDE tutorial/013-case.f
\

MARKER NO-CASE

CR
.( --- Tutorial 013: CASE structure loaded. ) CR
.(     Type NO-CASE to unload.             ) CR

NEEDS CASE


\ ===========================================================================
\ 1. Syntax overview
\ ===========================================================================
\
\   n  CASE
\       c1  OF  <branch-1>  ENDOF
\       c2  OF  <branch-2>  ENDOF
\       ...
\       <default-section>   ( n is still on stack here )
\   ENDCASE                 ( n dropped by ENDCASE )
\
\ Inside each OF branch, n is gone (already matched and dropped).
\ In the default section, n is still present -- DROP it if not needed.
\
\ The comparison is always equality.  For range tests, use IF instead.


\ ===========================================================================
\ 2. Simple example: colour name
\ ===========================================================================
\
\ The ZX Spectrum color numbers 0-7 correspond to named colors.

: .COLOR-NAME  ( n -- )
    \ Print the name of a ZX Spectrum color number 0-7.
    CASE
        0 OF  ." black"   ENDOF
        1 OF  ." blue"    ENDOF
        2 OF  ." red"     ENDOF
        3 OF  ." magenta" ENDOF
        4 OF  ." green"   ENDOF
        5 OF  ." cyan"    ENDOF
        6 OF  ." yellow"  ENDOF
        7 OF  ." white"   ENDOF
        ." unknown(" DUP . ." )"    \ default: n still on stack
    ENDCASE  CR ;

.( Try: 2 .COLOR-NAME   ) CR    \ => red
.( Try: 5 .COLOR-NAME   ) CR    \ => cyan
.( Try: 9 .COLOR-NAME   ) CR    \ => unknown(9)


\ ===========================================================================
\ 3. CASE vs nested IF
\ ===========================================================================
\
\ The same logic using nested IF is harder to read:
\
\   : .COLOR-IF  ( n -- )
\       DUP 0= IF ." black" ELSE
\       DUP 1= IF ." blue"  ELSE
\       ." unknown" THEN THEN DROP CR ;
\
\ CASE is cleaner because:
\   - the test value appears only once
\   - each branch is independent and balanced
\   - the default falls through naturally


\ ===========================================================================
\ 4. Default section: using the remaining test value
\ ===========================================================================
\
\ If no OF matches, the default section runs with n on the stack.
\ You can use n there (e.g., to print it) or simply DROP it.
\
\   : DESCRIBE  ( n -- )
\       CASE
\           0 OF  ." zero"    ENDOF
\           1 OF  ." one"     ENDOF
\                 ." number " .  \ consumes n, so no DROP needed
\       ENDCASE  CR ;
\
\   0 DESCRIBE      => zero
\   1 DESCRIBE      => one
\   42 DESCRIBE     => number 42

: DESCRIBE  ( n -- )
    CASE
        0 OF  ." zero"    ENDOF
        1 OF  ." one"     ENDOF
              ." number " .
    ENDCASE  CR ;


\ ===========================================================================
\ 5. Key dispatch example
\ ===========================================================================
\
\ CASE is ideal for mapping key codes to actions.

: DO-KEY  ( c -- )
    \ Dispatch on a character code.
    CASE
        [CHAR] Q OF  ." quit"        ENDOF
        [CHAR] H OF  ." help"        ENDOF
        [CHAR] S OF  ." save"        ENDOF
        13          OF  ." enter"    ENDOF
        27          OF  ." escape"   ENDOF
        ." unknown key: " DUP EMIT
    ENDCASE  CR ;

.( Try: [CHAR] H DO-KEY ) CR
.( Try: 27 DO-KEY       ) CR


\ ===========================================================================
\ 6. Simple tests (requires NEEDS TESTING)
\ ===========================================================================
\
\ NEEDS TESTING
\ T{  0 DESCRIBE  ->       }T    \ side effect only
\ T{  1 DESCRIBE  ->       }T
\ T{  42 DESCRIBE ->       }T
