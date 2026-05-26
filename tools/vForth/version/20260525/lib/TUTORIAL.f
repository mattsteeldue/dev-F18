\
\ tutorial.f
\ TUTORIAL  --  launch a tutorial by its sequence number.
\
\ Usage:
\   NEEDS TUTORIAL
\   3 TUTORIAL     ( loads ./tutorial/003-output.f )
\
\ The word opens the tutorial/ directory, finds the first entry whose
\ name matches the wildcard NNN-* (zero-padded number), builds the
\ full path "tutorial/<name>", and calls F_INCLUDE.
\
\ The filename in a NextZXOS dirent buffer is a z-string at offset 0.
\ Wildcard matching NNN-* is handled by the OS via F_READDIR.
\
\ All dependencies are core: F_OPENDIR F_READDIR F_INCLUDE F_CLOSE.
\
\ Reference: sec.2.12.14
\

.( TUTORIAL )

\ ---------------------------------------------------------------------------
\ Scratch buffers -- allocated once, never relocated.
\ ---------------------------------------------------------------------------

\ "tutorial/" as counted-z-string; 1+ yields the z-string for OS calls.
CREATE tut-pfx    ," tutorial/"

\ wildcard buffer: "NNN-*" + null (6 bytes used, 16 allotted).
CREATE tut-wcard  16 ALLOT
tut-wcard 16 ERASE

\ dirent buffer filled by F_READDIR; filename is z-string at offset 0.
CREATE tut-dirent 64 ALLOT
tut-dirent 64 ERASE

\ full path buffer: "tutorial/" (9) + filename (up to 32) + null.
CREATE tut-path   48 ALLOT
tut-path 48 ERASE


\ ---------------------------------------------------------------------------
\ (3DIGITS)  ( n addr -- )
\ Write the decimal representation of n (0..999) as exactly three ASCII
\ digits at addr.  No null terminator written.
\ ---------------------------------------------------------------------------
: (3DIGITS)  ( n addr -- )
    OVER  #100  /             #48  +  OVER  C!  1+  \ hundreds digit
    OVER  #10   MOD  #10  /   #48  +  OVER  C!  1+  \ tens digit
    SWAP  #10   MOD           #48  +  SWAP  C!  ;    \ units digit


\ ---------------------------------------------------------------------------
\ (BUILD-WCARD)  ( n -- )
\ Fill tut-wcard with the z-string "NNN-*\0".
\ ---------------------------------------------------------------------------
: (BUILD-WCARD)  ( n -- )
    tut-wcard  16  ERASE            \ zero the buffer
    DUP  tut-wcard  (3DIGITS)       \ write "NNN" at bytes 0-2
    [CHAR] -  tut-wcard  3  +  C!   \ byte 3 = '-'
    [CHAR] *  tut-wcard  4  +  C! ; \ byte 4 = '*'; byte 5 = 0 from ERASE


\ ---------------------------------------------------------------------------
\ (ZLEN)  ( addr -- n )
\ Return the length of the null-terminated string at addr (null excluded).
\ ---------------------------------------------------------------------------
: (ZLEN)  ( addr -- n )
    DUP  BEGIN  DUP C@  WHILE  1+  REPEAT  SWAP  - ;


\ ---------------------------------------------------------------------------
\ (BUILD-PATH)  ( -- )
\ Compose "tutorial/<dirent-filename>" as a z-string in tut-path.
\ ---------------------------------------------------------------------------
: (BUILD-PATH)  ( -- )
    tut-path  48  ERASE
    tut-pfx COUNT  tut-path  SWAP  CMOVE  \ copy "tutorial/" (9 bytes)
    tut-dirent  (ZLEN)                    \ length of filename in dirent
    tut-dirent  tut-path  tut-pfx C@ +   \ src  dst (after prefix)
    SWAP  CMOVE ;                         \ copy filename; null from ERASE


\ ---------------------------------------------------------------------------
\ TUTORIAL  ( n -- )
\ ---------------------------------------------------------------------------
: TUTORIAL  ( n -- )
    (BUILD-WCARD)
    \ Open tutorial/ directory; 1+ skips the count byte of counted string.
    tut-pfx  1+  F_OPENDIR
    IF  DROP
        ." TUTORIAL: cannot open tutorial/" CR  EXIT
    THEN                                    \ fh
    tut-dirent  tut-wcard  OVER  F_READDIR  \ fh n err
    IF  DROP  F_CLOSE  DROP
        ." TUTORIAL: F_READDIR error" CR  EXIT
    THEN                                    \ fh n
    0=  IF  F_CLOSE  DROP
        ." TUTORIAL: no matching tutorial" CR  EXIT
    THEN                                    \ fh (dirent is populated)
    F_CLOSE  DROP
    (BUILD-PATH)
    tut-path  PAD  1  F_OPEN               \ open the file read-only
    IF  DROP
        ." TUTORIAL: cannot open file" CR  EXIT
    THEN                                    \ fh
    F_INCLUDE ;
