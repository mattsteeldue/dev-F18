\
\ 011-vocabularies.f
\ Vocabularies: namespaces in the Forth dictionary.
\
\ In vForth the dictionary is organised as a chain of vocabularies.
\ Two user variables control word search and definition placement:
\
\   CONTEXT  ( -- addr )  vocabulary searched first during lookup.
\   CURRENT  ( -- addr )  vocabulary where new definitions are inserted.
\
\ At startup both point to FORTH, the root vocabulary.  Creating a new
\ vocabulary with VOCABULARY cccc does not change either pointer; you
\ have to execute cccc and/or cccc DEFINITIONS explicitly.
\
\ The search order is: CONTEXT first, then CURRENT (if different).
\ Only two vocabularies are searched at a time -- vForth is not ANS
\ search-order Forth.  This is intentional and matches the classic
\ Forth-79 / Forth-83 model.
\
\ A key use case on vForth/Next: isolating the ASSEMBLER vocabulary so
\ that Z80 mnemonics do not pollute the FORTH namespace.
\
\ Reference: sec.2.12.9, sec.2.12.12
\
\ Load from a clean session:
\   INCLUDE tutorial/011-vocabularies.f
\ To unload and reload interactively:
\   NO-VOCABULARIES
\   INCLUDE tutorial/011-vocabularies.f
\

MARKER NO-VOCABULARIES

CR
.( --- Tutorial 011: vocabularies loaded. ) CR
.(     Type NO-VOCABULARIES to unload.   ) CR


\ ===========================================================================
\ 1. The two control variables: CONTEXT and CURRENT
\ ===========================================================================
\
\ CONTEXT and CURRENT are user variables holding the address of the latest
\ word in the respective vocabulary (i.e. a pointer into the NFA chain).
\
\   CONTEXT @  .    => (address of FORTH vocabulary header)
\   CURRENT @  .    => (same at startup)
\
\ Executing a vocabulary name sets CONTEXT to that vocabulary:
\   ASSEMBLER       ( CONTEXT now points to ASSEMBLER )
\   FORTH           ( CONTEXT back to FORTH )
\
\ DEFINITIONS sets CURRENT to whatever CONTEXT currently is:
\   ASSEMBLER DEFINITIONS   ( new words go into ASSEMBLER )
\   FORTH DEFINITIONS       ( restore: new words go into FORTH )
\
\ Always restore FORTH DEFINITIONS after working in another vocabulary.


\ ===========================================================================
\ 2. VOCABULARY -- creating a new namespace
\ ===========================================================================
\
\ VOCABULARY name  ( -- )
\   Creates a new vocabulary word called name.  Executing name sets
\   CONTEXT to the new vocabulary.  The new vocabulary is initially
\   empty (it inherits no words from FORTH automatically).
\
\ Pattern for a self-contained module:
\
\   VOCABULARY MYMODULE
\   MYMODULE DEFINITIONS    \ new words go into MYMODULE
\
\   : HELPER  ( -- )  ... ;   \ private to MYMODULE
\   : API     ( -- )  ... ;   \ also in MYMODULE
\
\   FORTH DEFINITIONS         \ restore: new words back to FORTH
\
\ Words in MYMODULE are accessible only when CONTEXT = MYMODULE.
\ From FORTH, call them as:  MYMODULE  API

VOCABULARY SHAPES
SHAPES DEFINITIONS

: .CIRCLE   ( -- )  ." O"  CR ;
: .SQUARE   ( -- )  ." []" CR ;
: .TRIANGLE ( -- )  ." /\" CR ;

FORTH DEFINITIONS   \ always restore before continuing

.( Try: SHAPES .CIRCLE   ) CR
.( Try: SHAPES .SQUARE   ) CR


\ ===========================================================================
\ 3. WORDS -- inspecting a vocabulary
\ ===========================================================================
\
\ WORDS  ( -- )
\   Lists all words in the CONTEXT vocabulary, newest first.
\   Output wraps at the screen edge automatically.
\
\   WORDS               ( list FORTH vocabulary )
\   SHAPES WORDS        ( list SHAPES vocabulary )
\
\ WORDS scans the NFA chain from CONTEXT @ @ backward to the beginning.
\ It respects ?TERMINAL: press [BREAK] to interrupt a long listing.


\ ===========================================================================
\ 4. Hiding words with SMUDGE
\ ===========================================================================
\
\ During compilation of a colon-definition, the word being defined is
\ temporarily "smudged" -- invisible to the dictionary search.  This
\ prevents a definition from accidentally calling itself before it is
\ complete.  SMUDGE toggles the smudge bit in the NFA.
\
\ Normally you never call SMUDGE directly.  It is mentioned here because
\ understanding it clarifies why a word is not found during its own
\ compilation and why a recursive word needs RECURSE (or an explicit
\ forward reference).
\
\   : FACTORIAL  ( n -- n! )
\       DUP 1 > IF  DUP 1-  RECURSE  *  ELSE  DROP 1  THEN ;
\
\   5 FACTORIAL .   => 120


\ ===========================================================================
\ 5. FORGET -- removing words from the dictionary
\ ===========================================================================
\
\ FORGET name  ( -- )
\   Removes name and every word defined after it from the CURRENT
\   vocabulary.  The dictionary pointer (DP) is reset to just before
\   name's NFA.
\
\ Use carefully: FORGET is permanent and cannot be undone.
\ MARKER is safer for temporary definitions (see tutorial 005).
\
\   : TEMP  ( -- )  ." temporary" CR ;
\   TEMP                    => temporary
\   FORGET TEMP
\   TEMP                    => error: word not found


\ ===========================================================================
\ 6. The ASSEMBLER vocabulary
\ ===========================================================================
\
\ ASSEMBLER is a pre-defined vocabulary containing the Z80 mnemonic words
\ (ld, add, push, pop, ...).  It is kept separate from FORTH so that
\ mnemonic names do not shadow ordinary Forth words.
\
\ Inside a CODE definition the system automatically switches to ASSEMBLER;
\ C; switches back to FORTH.  You should not need to manage
\ the ASSEMBLER vocabulary manually unless you are writing your own CODE
\ words or extending the assembler.
\
\   CODE MY-WORD  ( -- )
\       \ assembler mnemonics available here
\       halt
\       Next            \ standard vForth exit from a CODE word
\   C;
\
\ See the assembler tutorial for a full treatment.


\ ===========================================================================
\ 7. Demonstration
\ ===========================================================================

: .CONTEXT  ( -- )
    ." CONTEXT = " CONTEXT @ @ U. CR ;

: .CURRENT  ( -- )
    ." CURRENT = " CURRENT @ @ U. CR ;

.( Try: .CONTEXT  ) CR
.( Try: .CURRENT  ) CR
.( Try: SHAPES WORDS  ) CR


\ ===========================================================================
\ 8. Simple tests (requires NEEDS TESTING)
\ ===========================================================================
\
\ (Vocabulary state is hard to test automatically; use interactive checks.)
\
\ NEEDS TESTING
\ T{  CONTEXT @  CURRENT @  =  -> -1  }T   \ both FORTH at startup
