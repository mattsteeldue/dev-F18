\
\ LOCALS.f
\
.( LOCALS )
\
\ Re-entrant VALUE-like local variables.
\
\ Used in the form
\
\       : SUM3   { X Y Z }   X Y + Z + ;
\
\ { is IMMEDIATE and must be the first word of the definition: it declares
\ the local names, in the order in which the caller pushed them, and
\ compiles the code that pops the arguments into them. The names live as
\ VALUE-like words inside the DEFLOCALS vocabulary, invisible from
\ outside the definition that declared them.
\
\ The older two-part form is still supported, and is what { is built on:
\
\       3 LOCALS-FOR SUM3   X Y Z
\       : SUM3   LOCALS   X Y + Z + ;
\
\ LOCALS-FOR runs in interpretation state, BEFORE the colon definition,
\ and takes the count of locals, the name of the definition that follows,
\ and then that many names. LOCALS, IMMEDIATE, then makes them visible
\ inside the body and binds them. Everything { does in one place. Prefer
\ { ... } : it cannot get the count wrong, and nothing has to stay
\ adjacent to anything else.
\
\ X local pushes its value; write it with TO :
\
\       12 TO X
\
\ DELIBERATE DEVIATION from the Forth-2012 locals wordset: a local is a
\ permanent cell, not a frame slot. Re-entrancy is obtained by SHALLOW
\ BINDING: on entry each cell's previous content is pushed on the return
\ stack, and every exit path restores it. Two live activations of the
\ same word therefore see their own values, and RECURSE works.
\
\ The restore happens without redefining EXIT, ; or : . LOCALS pushes on
\ the return stack, above the caller's address, the address of a chain of
\ (LOC-POP) cells: the EXIT that ends the definition -- any EXIT, including
\ an early one inside IF -- lands there instead of returning, the chain
\ restores the cells, and its own final EXIT returns to the caller.
\
\ TRAMPOLINE. { (like LOCALS) does not compile the body into the
\ definition the user opened. It ends that definition after two cells --
\ a slot and EXIT
\ -- reveals it with SMUDGE, and then opens the body as an anonymous
\ :NONAME definition whose xt is written into the slot. So
\
\       : FOO   { X }  ... ;
\
\ compiles two words: FOO, which is just  ( call body ) EXIT , and the
\ nameless body that binds the locals and runs the code. The point of the
\ split is that between the two HERE is outside any pending definition,
\ which is the one state in which words can be CREATEd -- this is what
\ lets { ... } declare the locals in place, where LOCALS-FOR had to do it
\ before the colon. RECURSE keeps working: after :NONAME the LATEST
\ definition is the body itself, so recursion re-enters it directly,
\ re-binding the locals and skipping the trampoline.
\
\ Cost per activation: one return-stack cell for the chain address, plus
\ two per local (old value + its cell address), i.e. 4+4n bytes on top of
\ the caller's address, plus one more cell for the trampoline's own return
\ address -- paid once on entry, not on each recursion level. The return
\ stack is 160 bytes shared with the TIB, so recursion stays shallow --
\ measured on the emulator, a word with one local survives 15 levels and
\ dies at 20; with eight locals, about 3.
\ Overflowing it overwrites the input buffer, silently.
\
\ ABORT and THROW bypass the chain, so an aborted word leaves its locals
\ holding inner values. This is harmless: every entry rebinds all of them
\ from the stack before the body runs.
\
\ Every local name and cell is permanent: a scope costs n cells of
\ dictionary plus one heap header per name, none of it reclaimable.
\
\ All the local names must be on the SAME source line as the { that opens
\ them (or as LOCALS-FOR, in the older form).
\
\ Design notes and the reasoning behind this shape: prompts/LOCALS-PLAN.md
\
\ Errors are reported with ?ERROR, using four messages reserved in the
\ standard error blocks (Screen #7, lines 9-12) -- see  9 LOAD  for the
\ full list:
\
\       #57  LOCALS: bad count.
\       #58  LOCALS: no scope declared.
\       #59  LOCALS: scope not adjacent.
\       #60  LOCALS: misplaced { or }.
\

FORTH DEFINITIONS   \ Force this library as part of Forth definitions

MARKER NO-LOCALS

NEEDS TO
\ NEEDS :NONAME

  8 CONSTANT MAXLOCALS

\ The locals live in their own vocabulary so they are invisible outside
\ the definition that declared them. It is cleared by every
\ LOCALS-FOR, so only one scope is alive at a time.

VOCABULARY DEFLOCALS

DEFLOCALS
CONTEXT @   CONSTANT LOC-VOC        \ address of DEFLOCALS' LATEST cell
FORTH
LOC-VOC @   CONSTANT LOC-EMPTY      \ value of that cell when empty

VARIABLE #LOCALS        0 #LOCALS !     \ locals in the pending scope
VARIABLE SCOPE-LINK     0 SCOPE-LINK !  \ LATEST when the scope was opened
VARIABLE OLD-CURRENT    0 OLD-CURRENT !
VARIABLE LOC-SLOT       0 LOC-SLOT !     \ cell to patch with the body's xt

CREATE LOCAL-PFAS   MAXLOCALS CELLS ALLOT

\ locals are recorded in declaration order; the binding code has to be
\ emitted in reverse, because the last one declared is on top at run time.

: LOC-PFA   ( i -- a )  CELLS LOCAL-PFAS + ;

\ ----------------------------------------------------------------------
\ Run-time support: shallow binding
\
\ (LOC-BIND) binds one local to an argument, remembering on the return
\ stack what was in the cell and which cell it was. Both words juggle
\ their own return address, which is on top when they start.
\
\ (LOC-POP) undoes one binding. It is never called from a definition:
\ it is reached through the (LOC-EXIT) chain below, when the EXIT of the
\ word being unwound jumps into it.

: (LOC-BIND)  ( x a -- )            \ R: -- old a
    R> SWAP DUP >R  DUP @ >R  ROT SWAP !  >R
;

: (LOC-POP)   ( -- )                \ R: old a --
    R> R> R> !  >R
;

\ MAXLOCALS pop cells followed by EXIT. A definition with n locals is made
\ to return into this chain n cells before its end, so exactly n bindings
\ are undone and the final EXIT returns to the caller.
\ Same idiom as the hand-built thread in inc/exec_.f  ( HERE ' EXIT , ).

: (LOC-CHAIN) ( xt n -- )   0 DO  DUP ,  LOOP  DROP ;

CREATE (LOC-EXIT)
    ' (LOC-POP) MAXLOCALS (LOC-CHAIN)
    ' EXIT ,

: LOC-ENTRY  ( n -- a )             \ where to enter the chain for n locals
    MAXLOCALS SWAP - CELLS  (LOC-EXIT) +
;

\ ----------------------------------------------------------------------
\ Compile-time support: the trampoline
\
\ (LOC-OPEN) ends the definition being compiled after a slot and an EXIT,
\ then SMUDGE reveals it. HERE is now outside any pending definition, so
\ CREATE works again -- see the header note.
\
\ (LOC-CLOSE) opens the body as an anonymous definition and writes its xt
\ into the slot. :NONAME leaves that xt on the stack and makes the body
\ the LATEST definition, so the final ; un-SMUDGEs the body -- the outer
\ word was already revealed by (LOC-OPEN). Consuming the xt puts the
\ stack back where : found it, and !CSP re-arms the ?CSP check of ; on it.

: (LOC-OPEN)  ( -- )
    HERE LOC-SLOT !
    COMPILE NOOP                    \ placeholder: harmless if never patched
    COMPILE EXIT
\   SMUDGE                          \ reveal the outer word
    ;

\ (LOC-CLOSE) also makes the local names visible and compiles, at the head
\ of the body, the code that binds them: last declared first, that is the
\ one on top at run time. The chain address goes last, so that it is what
\ the EXIT of the body finds on top of the return stack.

: (LOC-CLOSE) ( -- )
    \ :NONAME                       \ ( -- xt )  the body; LATEST is now it
    HERE                            \ xt

    $CD C,                          \ compile CALL op-code
    [ ' ' >BODY CELL- @ ]   
    LITERAL ,                       \ colon-definition CFA address to jump to    
    
    LOC-SLOT @ !                    \ the outer word calls the body
    !CSP

    LOC-VOC CONTEXT !               \ local names visible in the body

    #LOCALS @ 0 DO
        COMPILE LIT
        #LOCALS @ 1- I - LOC-PFA @ ,
        COMPILE (LOC-BIND)
    LOOP

    COMPILE LIT
    #LOCALS @ LOC-ENTRY ,
    COMPILE >R

    0 #LOCALS !                     \ consume the scope
;

\ ----------------------------------------------------------------------
\ Declaring one local -- used by both forms
\
\ CURRENT must be restored before returning: if it were left on
\ DEFLOCALS, the following  :  would create the definition itself inside
\ DEFLOCALS, and it would vanish at the next scope. CONTEXT is restored
\ with it -- for LOCALS-FOR that is mere tidiness, since the following  :
\ overwrites it anyway with  CURRENT @ CONTEXT !  , but { runs after that
\ point and an error in mid-declaration must not leave the locals in the
\ search order. Nothing else will do it for us: ?ERROR ends in QUIT, which
\ resets STATE and the return stack but not CONTEXT/CURRENT -- it is ABORT,
\ not ERROR, that does FORTH DEFINITIONS.

: (LOC-MAKE)  ( -- ccc )            \ create one local, parsing its name
    CURRENT @ OLD-CURRENT !
    DEFLOCALS DEFINITIONS
    0 CONSTANT                      \ the local: a VALUE-like cell
    LATEST PFA  #LOCALS @ LOC-PFA !
    OLD-CURRENT @ CURRENT !
    CURRENT @ CONTEXT !
    1 #LOCALS +!
;

\ ----------------------------------------------------------------------
\ LOCALS-FOR  -- interpretation state, before the colon definition

: LOCALS-FOR ( n -- ccc ccc1 ... cccn )
    DUP 0=  OVER MAXLOCALS >  OR    #57 ?ERROR  \ bad count

    BL WORD DROP                    \ consume the definition name
    CURRENT @ @ SCOPE-LINK !        \ remember what LATEST was
    LOC-EMPTY LOC-VOC !             \ empty the locals vocabulary
    0 #LOCALS !
    0 DO  (LOC-MAKE)  LOOP
;

\ ----------------------------------------------------------------------
\ LOCALS  -- IMMEDIATE, inside the colon definition
\
\ The two guards catch the case that would otherwise be silent: a second
\ definition saying LOCALS without its own LOCALS-FOR would bind the SAME
\ cells and share storage with the first one.
\ The scope is consumed here, so it cannot be used twice.

: LOCALS ( -- )
    ?COMP
    #LOCALS @ 0=                    #58 ?ERROR  \ no scope declared
    LATEST PFA LFA @ SCOPE-LINK @ - #59 ?ERROR  \ scope not adjacent

    (LOC-OPEN)                      \ close the outer word on a slot
    (LOC-CLOSE)                     \ body as :NONAME, bind, divert EXIT
;
IMMEDIATE

\ ----------------------------------------------------------------------
\ {  ccc1 ... cccn  }   -- IMMEDIATE, first thing in the definition
\
\       : SUM3   { X Y Z }   X Y + Z + ;
\
\ Declaration and use in one place: no count to keep in step, no separate
\ LOCALS-FOR to keep adjacent to the definition. It is the trampoline that
\ makes this possible -- (LOC-OPEN) closes the outer word, and only then
\ is HERE free for the CREATE that each local needs.
\
\ Each name is parsed twice: >IN is rewound after the test against } so
\ that CONSTANT parses the very same name. All the names, and the } , must
\ be on the SAME source line as the { .
\
\ On a malformed declaration the outer word survives as a do-nothing
\ NOOP EXIT : the error is raised after (LOC-OPEN) has already revealed it.

: }  ( -- )
    #60 ERROR                       \ misplaced: } without {
;

: {  ( -- )
    ?COMP
    (LOC-OPEN)                      \ HERE is free from here on
    LOC-EMPTY LOC-VOC !             \ empty the locals vocabulary
    0 #LOCALS !
    BEGIN
        >IN @  BL WORD              ( in a )
        DUP C@ 0=  OVER 1+ C@ 0= OR #60 ?ERROR  \ misplaced: missing }
        DUP C@ 1 = OVER 1+ C@ [CHAR] } = AND  0=
    WHILE                           ( in a )
        DROP  >IN !                 \ rewind: CONSTANT re-parses the name
        (LOC-MAKE)
        #LOCALS @ MAXLOCALS >       #57 ?ERROR  \ bad count
    REPEAT
    2DROP                           ( in a )
    #LOCALS @ 0=                    #57 ?ERROR  \ bad count

    (LOC-CLOSE)                     \ body as :NONAME, bind, divert EXIT
;
IMMEDIATE

FORTH DEFINITIONS
