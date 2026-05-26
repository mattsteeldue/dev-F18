\
\ 021-evaluate.f
\ Text interpretation: EVALUATE, WORD, FIND, NUMBER.
\
\ vForth's interpreter loop is built from a small set of words that
\ you can call directly.  This tutorial covers the key primitives:
\
\   WORD   ( c -- addr )   parse one token from the input stream
\   -FIND  ( -- cfa b f )  look up the most recently WORDed token
\   NUMBER ( -- n )        convert the most recently WORDed token to n
\   EVALUATE ( a u -- )    interpret a string as Forth source (NEEDS)
\
\ These are the building blocks of any Forth meta-interpreter, REPL
\ extension, or scripting layer.
\
\ Reference: sec.2.12.6
\
\ Load from a clean session:
\   INCLUDE tutorial/021-evaluate.f
\ To unload and reload interactively:
\   NO-EVALUATE
\   INCLUDE tutorial/021-evaluate.f
\

MARKER NO-EVALUATE

CR
.( --- Tutorial 021: evaluate loaded. ) CR
.(     Type NO-EVALUATE to unload.   ) CR

NEEDS EVALUATE


\ ===========================================================================
\ 1. WORD  --  parsing the input stream
\ ===========================================================================
\
\ WORD ( c -- addr )
\   Scan the current input for the next token delimited by character c.
\   Returns HERE, which holds a counted string (length byte + text).
\   Advances >IN past the token.
\
\ BL is the space character (32), the normal delimiter.
\
\   BL WORD  COUNT TYPE  \ read and print the next token
\
\ WORD is the same word used by the interpreter internally.
\ The result at HERE is overwritten by the next call to WORD.

: NEXT-TOKEN  ( -- addr len )
    BL WORD  COUNT ;

.( Try: NEXT-TOKEN TYPE  then type a word at the prompt ) CR


\ ===========================================================================
\ 2. -FIND  --  dictionary lookup
\ ===========================================================================
\
\ -FIND ( -- cfa b f )
\   Searches the dictionary for the word most recently parsed by WORD.
\   On success: cfa b -1  (cfa=execution token, b=NFA length byte)
\   On failure: 0
\
\ The b value's bit 6 ($40) signals IMMEDIATE.  Bit 5 ($20) is SMUDGE.
\
\   BL WORD  -FIND
\   IF  DROP  ." found: " .  ELSE  ." not found"  THEN  CR

: LOOK-UP  ( -- )
    ." Word to look up: "
    BL WORD  -FIND
    IF  NIP  ." found, CFA=" U.  ELSE  ." not found"  THEN  CR ;

.( Try: LOOK-UP DUP ) CR


\ ===========================================================================
\ 3. NUMBER  --  numeric conversion
\ ===========================================================================
\
\ NUMBER ( -- n )
\   Converts the counted string at HERE (left by WORD) to a number
\   using the current BASE.  Leaves the result on the stack.
\   If conversion fails, vForth signals an error.
\
\   BL WORD  NUMBER   \ parse the next token as a number

: PARSE-NUMBER  ( -- n )
    BL WORD  NUMBER ;

.( Try: PARSE-NUMBER 42  .  ) CR   \ type 42 at the prompt => 42


\ ===========================================================================
\ 4. EVALUATE  --  interpret a string
\ ===========================================================================
\
\ EVALUATE ( addr u -- )
\   Interprets the string at addr for u characters as Forth source.
\   Has the same effect as typing that text at the prompt.
\   Can nest: EVALUATE may call EVALUATE.
\
\   S" 2 3 + ." EVALUATE     \ interprets "2 3 + ." as Forth
\   S" : FOO  42 . ;" EVALUATE  FOO   \ define and call a word via string

: EVAL-DEMO  ( -- )
    S" 10 20 + ." EVALUATE ;

.( Try: EVAL-DEMO   ) CR          \ => 30

: EVAL-DEFINE  ( -- )
    S" : FROM-STRING  ." 1" ." 99" ." ." ." " ;" EVALUATE ;

\ Simpler direct demo:
: CALC-STRING  ( -- n )
    S" 7 6 *" EVALUATE ;

.( Try: CALC-STRING .   ) CR      \ => 42


\ ===========================================================================
\ 5. The interpreter loop in pseudocode
\ ===========================================================================
\
\ The vForth interpreter is essentially:
\
\   BEGIN
\       BL WORD
\       -FIND
\       IF
\           \ word found
\           STATE @ AND  ( immediate-flag )
\           IF  EXECUTE                   \ compile mode, not immediate
\           ELSE  EXECUTE  THEN           \ interpret or immediate: run
\       ELSE
\           NUMBER                        \ try as number
\           STATE @ IF  COMPILE LITERAL  THEN
\       THEN
\   AGAIN
\
\ Knowing this loop lets you extend the interpreter by wrapping WORD,
\ -FIND, and NUMBER.


\ ===========================================================================
\ 6. Simple tests (requires NEEDS TESTING)
\ ===========================================================================
\
\ NEEDS TESTING
\ T{  S" 2 3 +" EVALUATE  -> 5  }T
\ T{  S" 10 NEGATE" EVALUATE  -> -10  }T
