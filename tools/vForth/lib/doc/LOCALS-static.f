\
\ LOCALS-static.f
\
\ RECONSTRUCTION of the first implementation of lib/LOCALS.f -- the one
\ with STATIC storage, before shallow binding made the locals re-entrant.
\ It was never committed (59d15e9 recorded only the CLAUDE.md tables), so
\ this file is rebuilt from the current lib/LOCALS.f minus the re-entrancy
\ machinery, following prompts/LOCALS-PLAN.md section 3.2:
\
\     "Il passo 4 compilava COMPILE ! e il passo 5 non esisteva,
\      finche' i locali non erano rientranti: sezione 11."
\
\ Reference only, like inc/doc/ : never loaded by NEEDS, kept for
\ comparison. The live library is lib/LOCALS.f.
\
.( LOCALS )
\
\ VALUE-like local variables.
\
\ Used in the form
\
\       3 LOCALS-FOR SUM3   A B C
\       : SUM3   LOCALS   A B + C + ;
\
\ LOCALS-FOR runs in interpretation state, BEFORE the colon definition.
\ It takes the count of locals, the name of the definition that follows,
\ and then that many local names. It creates the locals as VALUE-like
\ words inside the DEFLOCALS vocabulary, invisible from outside.
\
\ LOCALS is IMMEDIATE and takes no arguments. Inside the definition it
\ makes the local names visible again and compiles the code that pops the
\ caller arguments into them. It must run before the body touches the
\ stack, so in practice it is the first word of the definition.
\
\ A local pushes its value; write it with TO :
\
\       12 TO A
\
\ Storage is STATIC: a local is one permanent cell, written on entry and
\ never restored. A word with locals is therefore neither recursive nor
\ re-entrant -- and that includes being called from an interrupt handler
\ while it is already running. The inner activation overwrites the cells
\ the outer one is still using.
\
\ Every local name and cell is permanent: a scope costs n cells of
\ dictionary plus one heap header per name, none of it reclaimable.
\
\ All the local names must be on the SAME source line as LOCALS-FOR.
\
\ Design notes and the reasoning behind this shape: prompts/LOCALS-PLAN.md
\
MARKER NO-LOCALS

NEEDS TO

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

CREATE LOCAL-PFAS   MAXLOCALS CELLS ALLOT

\ locals are recorded in declaration order; the binding code has to be
\ emitted in reverse, because the last one declared is on top at run time.

: LOC-PFA   ( i -- a )  CELLS LOCAL-PFAS + ;

\ ----------------------------------------------------------------------
\ LOCALS-FOR  -- interpretation state, before the colon definition
\
\ CURRENT must be restored before returning: if it were left on
\ DEFLOCALS, the following  :  would create the definition itself inside
\ DEFLOCALS, and it would vanish at the next LOCALS-FOR.
\ CONTEXT is restored too, but only for tidiness -- the following  :
\ overwrites it anyway with  CURRENT @ CONTEXT !

: LOCALS-FOR ( n -- ccc ccc1 ... cccn )
    DUP 0=  OVER MAXLOCALS >  OR    #57 ?ERROR  \ bad count

    BL WORD DROP                    \ consume the definition name
    CURRENT @ @ SCOPE-LINK !        \ remember what LATEST was
    LOC-EMPTY LOC-VOC !             \ empty the locals vocabulary
    0 #LOCALS !

    CURRENT @ OLD-CURRENT !
    DEFLOCALS DEFINITIONS
    0 DO
        0 CONSTANT                  \ the local: a VALUE-like cell
        LATEST PFA  #LOCALS @ LOC-PFA !
        1 #LOCALS +!
    LOOP
    OLD-CURRENT @ CURRENT !
    CURRENT @ CONTEXT !
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

    LOC-VOC CONTEXT !               \ local names visible in the body

    \ store the arguments, last declared first: it is the one on top.

    #LOCALS @ 0 DO
        COMPILE LIT
        #LOCALS @ 1- I - LOC-PFA @ ,
        COMPILE !
    LOOP

    0 #LOCALS !                     \ consume the scope
;
IMMEDIATE
