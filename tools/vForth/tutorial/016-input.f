\
\ 016-input.f
\ Keyboard input: KEY, ACCEPT, WAIT-KEY.
\
\ vForth reads from the keyboard through the current input device.
\ The core provides two words:
\
\   KEY    -- wait for any key and return its ASCII code
\   ACCEPT -- read a complete line into a buffer with editing
\
\ WAIT-KEY (NEEDS) is like KEY but also displays a cursor.
\
\ For interactive programs, KEY is the lowest-level entry point;
\ ACCEPT is the right choice when reading a word or number from
\ the user.  The input stream words (TIB, >IN, BLK) manage how
\ the interpreter reads from its own input; this tutorial covers
\ only the interactive keyboard words.
\
\ Common ASCII codes: 13=CR, 27=ESC, 32=SPACE, 8=backspace.
\ Printable characters: 32-126 ($20-$7E).
\ ZX Spectrum specific: DELETE=12, EDIT=..., depends on ROM.
\
\ Reference: sec.2.12.10
\
\ Load from a clean session:
\   INCLUDE tutorial/016-input.f
\ To unload and reload interactively:
\   NO-INPUT
\   INCLUDE tutorial/016-input.f
\

MARKER NO-INPUT

CR
.( --- Tutorial 016: keyboard input loaded. ) CR
.(     Type NO-INPUT to unload.            ) CR

NEEDS WAIT-KEY


\ ===========================================================================
\ 1. KEY  --  wait for a keypress
\ ===========================================================================
\
\ KEY ( -- c )   suspend execution until a key is pressed; return ASCII.
\
\ KEY does not echo the character.  The result is the ASCII code of the
\ key pressed; use EMIT to echo it manually if needed.
\
\   KEY .         => (prints ASCII code of pressed key)
\   KEY EMIT CR   => (echoes the character, then newline)
\
\ Common check patterns:
\   KEY 27 = IF  ." escape"  THEN  CR   \ test for ESC
\   KEY 13 = IF  ." enter"   THEN  CR   \ test for CR/ENTER


\ ===========================================================================
\ 2. WAIT-KEY  --  KEY with cursor
\ ===========================================================================
\
\ WAIT-KEY ( -- c )   same as KEY but displays a blinking cursor while
\ waiting.  More user-friendly for interactive programs.
\
\   WAIT-KEY .    => (ASCII code with cursor shown during wait)


\ ===========================================================================
\ 3. ACCEPT  --  read a line of text
\ ===========================================================================
\
\ ACCEPT ( addr maxlen -- len )
\   Read up to maxlen characters from the keyboard into the buffer at
\   addr.  Returns the actual number of characters read (not including
\   the terminating CR).  Provides basic line editing (backspace).
\
\   CREATE BUF  40 ALLOT
\   BUF 40 ACCEPT .         => (number of chars typed)
\   BUF OVER TYPE CR        => (prints the line just entered)
\
\ Note: the buffer is NOT null-terminated by ACCEPT.  Use TYPE with
\ the returned length to print it, not COUNT.


\ ===========================================================================
\ 4. Getting a number from the user
\ ===========================================================================
\
\ A simple approach: ACCEPT into PAD, then use NUMBER or EVALUATE.
\ This tutorial shows the EVALUATE approach (NEEDS EVALUATE separately).
\ For a simpler approach without EVALUATE:

CREATE INPUT-BUF  32 ALLOT

: ?NUMBER  ( addr len -- n f )
    \ Attempt to parse addr/len as a decimal number.
    \ Returns ( n -1 ) on success or ( 0 0 ) on failure.
    \ Uses the current BASE.
    1 0  DO          \ loop runs once
        DUP 0= IF  2DROP  0 0  LEAVE  THEN
        OVER C@ [CHAR] - = IF   \ check leading minus
            1- SWAP 1+ SWAP     \ skip minus
            NUMBER  NEGATE  -1
        ELSE
            NUMBER  -1
        THEN
    LOOP ;

: ASK-NUMBER  ( -- n )
    \ Prompt the user for a number; return it.
    ." Enter a number: "
    INPUT-BUF 20 ACCEPT
    INPUT-BUF SWAP
    ?NUMBER IF
        ." Got: " DUP . CR
    ELSE
        DROP 0
        ." (not a number)" CR
    THEN ;

.( Try: ASK-NUMBER . ) CR


\ ===========================================================================
\ 5. Simple yes/no prompt
\ ===========================================================================

: YES?  ( -- f )
    \ Ask the user yes (Y) or no (N). Return true for Y.
    BEGIN
        ." (Y/N)? "
        WAIT-KEY  DUP EMIT  CR
        DUP [CHAR] Y =  OVER [CHAR] y = OR  OVER [CHAR] N = OR
        OVER [CHAR] n = OR
    UNTIL
    [CHAR] Y =  OVER [CHAR] y = OR ;

.( Try: YES?  IF ." yes" ELSE ." no" THEN  CR ) CR


\ ===========================================================================
\ 6. Simple tests (requires NEEDS TESTING)
\ ===========================================================================
\
\ (Interactive words cannot be tested automatically; use manually.)
\
\ NEEDS TESTING
\ T{  ( interactive: press a key and check result ) }T
