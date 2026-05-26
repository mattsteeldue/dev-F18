\
\ lib/persistence.f
\
\ v-Forth 1.8 - NextZXOS version - build 2025-01-01            
\ MIT License (c) 1990-2025 Matteo Vitturi     
\

( PERSISTENCE ) 

\ Save the complete current vForth status to blocks 
\ This must be the very first definition loaded just after a COLD start
\ this way these definitions are always at lower address than any subsequent 
\ loading.

CREATE PERSISTENCE .( .)

\ Block-numbers where RAM is dumped to
\ Normal version:
\ User data: 32000
\ Core data: 32001 - 32064
\ Heap data: 32091 - 32418
\ Dot-version:
\ User data: 34200
\ Core data: 34201 - 34216 
\ Heap data: 34291 - 34418

\ normal version has origin >$4000, dot version <$4000
\ and uses 200 blocks higher than normal version
0 +ORIGIN $4000 > 1+ #200 *
#32000 +
CONSTANT BLOCK-NUM-USER

BLOCK-NUM-USER 1+
CONSTANT BLOCK-NUM-CORE

#90 BLOCK-NUM-CORE + 
CONSTANT BLOCK-NUM-HEAP

' FORTH >BODY CELL+ 
CONSTANT FORTH-POINTER

$2E +ORIGIN @
CONSTANT USER-POINTER

\ given a memory address 'a' and a block number 'u'
\ compare data between block and memory
\ any FAR 8k paging must be performed beforehand
\ : COMPARE-BLOCK ( a u -- )
\     CASEON
\     BLOCK                       \ a a1
\     SWAP                        \ a1 a
\     2DUP                        \ a1 a a1 a
\     256 + SWAP 256 + SWAP       \ a1 a a3 a2
\     256                         \ a1 a a3 a2 512
\     (COMPARE) #34 ?ERROR        \ a1 a
\     [CHAR] . EMIT
\     256                         \ a1 a 512
\     (COMPARE) #34 ?ERROR
\     CASEOFF
\ ;    

.( .)
 
\ given a memory address 'a' and a block number 'u'
\ restore data from block to memory
\ any FAR 8k paging must be performed beforehand
: RESTORE-FROM-BLOCK ( a u -- )
    BLOCK                       \ a a1
    SWAP                        \ a1 a
    B/BUF                       \ a1 a 512
    CMOVE 
;    

\ given a memory address 'a' and a block number 'u'
\ save data from memory to block
\ any FAR 8k paging must be performed beforehand
: SAVE-TO-BLOCK ( a u -- )
    BLOCK                       \ a a1
    B/BUF                       \ a a1 512
    CMOVE 
    UPDATE FLUSH
;    

\ based on flag f, save (true) or restore (false) 512 bytes using
\ memory address a and block number u
: MANAGE-RW-BLOCK ( f a u -- )
    ROT IF                      \ a u f
    \   [ CHAR > ] LITERAL EMIT \ a u
    \   2DUP CR DECIMAL U. HEX U.           
        SAVE-TO-BLOCK
    ELSE
    \   [ CHAR < ] LITERAL EMIT \ a u
    \   2DUP CR DECIMAL U. HEX U.           
        RESTORE-FROM-BLOCK
        \ or COMPARE-BLOCK for test 
    THEN
    \ ?TERMINAL IF ABORT THEN
;

.( .)

\ given flag f and core address, save or restore 512-bytes page
: MANAGE-CORE-PAGE ( f a -- )
    DUP FENCE @ - 9 RSHIFT      \ f a b
    BLOCK-NUM-CORE +            \ f a u
    MANAGE-RW-BLOCK             \ f
;

\ given flag f and heap address, save or restore 512-bytes page
: MANAGE-HEAP-PAGE ( f hp -- )
    DUP 9 RSHIFT                \ f hp b
    BLOCK-NUM-HEAP +            \ f hp u
    SWAP FAR SWAP               \ f a u
    MANAGE-RW-BLOCK   
;

\ manage user data
: MANAGE-USER-DATA ( f -- )
    BLOCK-NUM-USER BLOCK        \ f blk
    USER-POINTER                \ f blk usr
    ROT DUP >R                  \   blk urs f
    IF                          \   blk usr
        SWAP                    \   usr blk
        \ save forth latest
        FORTH-POINTER @         \   usr blk latest
        USER-POINTER !          \   usr blk 
    THEN                        \   a1  a2       
    \
    #28 CMOVE   
    \
    R> IF
        UPDATE FLUSH 
    ELSE
        \ restore forth latest
        USER-POINTER @
        FORTH-POINTER !
    THEN
;

.( .)

\ based on flag f save or restore the system
: MANAGE-PAGES ( f -- )
    DUP MANAGE-USER-DATA        \ f
    \ manage whole heap
    HP@ 0                       \ f hp 0
    DO                          \ f
        DUP I MANAGE-HEAP-PAGE  \ f
    B/BUF +LOOP                 \ f
    \ manage core lower memory
    HERE FENCE @                \ f a2 a1
    DO                          \ f 
        DUP I MANAGE-CORE-PAGE  \ f
    B/BUF +LOOP
    MANAGE-USER-DATA
;

: RESTORE-SYSTEM 
\   BLOCK-NUM-CORE BLOCK @ 
\   #8192 = 55 ?ERROR
    0 MANAGE-PAGES 
\   TIB @ #34 BLANK
    HERE  #34 BLANK
    QUIT
;

: SAVE-SYSTEM    
    1 MANAGE-PAGES 
;

\ Clear blocks used by persistence
\ : CLEAR-BLOCKS
\     -1 CALC-HEAP-BLOCK
\     BLOCK-NUM-CORE
\     DO 
\         I BLOCK B/BUF ERASE UPDATE
\     LOOP    
\ ;

