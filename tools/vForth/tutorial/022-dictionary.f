\
\ 022-dictionary.f
\ Dictionary introspection: WORDS, SEE, WHERE, '.
\
\ vForth exposes the dictionary at runtime.  You can list all words,
\ disassemble any word, and inspect name/link/code fields directly.
\
\ Core words (no NEEDS):
\   '   ( -- cfa )    look up the next token; return its CFA
\   NFA ( cfa -- nfa ) CFA to Name Field Address
\   LFA ( cfa -- lfa ) CFA to Link Field Address
\   ID. ( nfa -- )    print the name at NFA
\
\ Words requiring NEEDS:
\   WORDS   ( -- )       list all words in CONTEXT vocabulary
\   SEE     ( -- cccc )  disassemble a word
\   WHERE   ( n n -- )   show the source line after a LOAD error
\
\ Reference: sec.2.12.4
\
\ Load from a clean session:
\   NEEDS TUTORIAL
\   022 TUTORIAL
\ To unload and reload interactively:
\   NEWTASK 022 TUTORIAL
\

MARKER NEWTASK

CR
.( --- Tutorial 022: dictionary loaded. ) CR
.(     Type NEWTASK to unload.   ) CR

NEEDS WORDS
NEEDS SEE


\ ===========================================================================
\ 1.  '  (tick)  --  get the CFA of a word
\ ===========================================================================
\
\ ' name ( -- cfa )
\   Returns the CFA (execution token) of name.  Unlike ['] (which is
\   immediate and works inside definitions), ' runs at interpret time.
\
\   ' DUP .         => (prints CFA address of DUP)
\   ' DUP EXECUTE   => same as DUP (duplicates TOS)
\
\ Inside a definition, use ['] (NEEDS [']) to compile the CFA as a literal:
\   : GET-DUP-XT  ( -- xt )  ['] DUP ;

.( ' DUP CFA: ) ' DUP U. CR
.( ' + CFA:   ) ' + U. CR


\ ===========================================================================
\ 2. NFA, LFA, ID.  --  walking the dictionary
\ ===========================================================================
\
\ Each dictionary entry has three fields relative to its CFA:
\   NFA ( cfa -- nfa )  Name Field Address: length+flags byte then name
\   LFA ( cfa -- lfa )  Link Field Address: points to the previous entry
\   ID. ( nfa -- )      print the name stored at nfa
\
\ Walk two entries back from DUP:
\
\   ' DUP  NFA  ID. CR              \ => DUP
\   ' DUP  LFA  @                   \ address of previous entry
\   NFA    ID. CR                   \ print its name

.( DUP name: ) ' DUP NFA ID. CR


\ ===========================================================================
\ 3. WORDS  --  list all words in the current vocabulary
\ ===========================================================================
\
\ WORDS ( -- )
\   Lists every word in the CONTEXT vocabulary (FORTH by default),
\   wrapping at the screen width.  Press BREAK to stop early.
\
\   WORDS              \ list all words
\   DEMO-VOC WORDS     \ list words of a specific vocabulary
\
.( Try: WORDS ) CR


\ ===========================================================================
\ 4. SEE  --  disassemble a word
\ ===========================================================================
\
\ SEE name ( -- )
\   Disassembles the word named by the next token.  For high-level
\   words it shows the compiled word addresses; for CODE words it
\   shows the hex bytes of the machine code.
\
\   SEE DUP         \ show DUP's code
\   SEE +           \ show +'s code
\   SEE SWAP        \ show SWAP's code
\
.( Try: SEE SWAP ) CR


\ ===========================================================================
\ 5. Inspecting a word manually
\ ===========================================================================
\
\ Example: print name and link of the word before SWAP in the dictionary.

: .WORD-INFO  ( cfa -- )
    DUP  NFA ID.  SPACE
    LFA  @  DUP IF  NFA ID.  ELSE  DROP ." (end)"  THEN  CR ;

.( DUP info: ) ' DUP .WORD-INFO


\ ===========================================================================
\ 6. WHERE  --  locate an error in a LOAD
\ ===========================================================================
\
\ WHERE is used after a compilation error during LOAD or INCLUDE.
\ It displays the screen and line number where the error occurred.
\ Normally called automatically by the error handler; use manually with:
\
\   >IN @  BLK @  WHERE

.( WHERE is called automatically after LOAD errors. ) CR


\ ===========================================================================
\ 7. Simple tests (requires NEEDS TESTING)
\ ===========================================================================
\
\ NEEDS TESTING
\ T{  ' DUP  NFA  C@  $3F AND  -> 3  }T   \ "DUP" is 3 chars
\ T{  ' +    NFA  C@  $3F AND  -> 1  }T   \ "+" is 1 char
