\
\ lib/persistence.f
\
\ v-Forth 1.8 - NextZXOS version - build 2025-01-01            
\ MIT License (c) 1990-2025 Matteo Vitturi     
\

.( PERSISTENCE ) 

\ Save the complete current vForth status to blocks 

MARKER PERSISTENCE

\ Block-numbers where RAM is dumped to
\ Normal version:
\ User data: 32000
\ Core data: 32001 - 30064
\ Heap data: 32091 - 30418
\ Dot-version: 
\ User data: 32200
\ Core data: 32201 - 32216, 
\ Heap data: 32291 - 32418


0 +ORIGIN $4000 > 1+ #200 *
#32000 +
CONSTANT BLOCK-NUM-USER

BLOCK-NUM-USER 1+
CONSTANT BLOCK-NUM-CORE

#90 BLOCK-NUM-CORE + 
CONSTANT BLOCK-NUM-HEAP
 
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

\ based on flag f, save or restore 512 bytes using
\ memory address a and block number u
: MANAGE-RW-BLOCK ( a u f -- )
    IF 
        2DUP CR U. U. 
        [ CHAR > ] LITERAL EMIT
        SAVE-TO-BLOCK
    ELSE
        2DUP CR U. U. 
        [ CHAR < ] LITERAL EMIT
        RESTORE-FROM-BLOCK
    THEN
    ?TERMINAL IF ABORT THEN
;

\ given core-address compute block number
: CALC-CORE-BLOCK ( a -- u )
    0 +ORIGIN NEGATE +
    9 RSHIFT    \ as B/BUF is 512
    BLOCK-NUM-CORE +
;

\ given address compute block number
: CALC-HEAP-BLOCK ( ha -- u )
    DUP FAR DROP
    9 RSHIFT    \ as B/BUF is 512
    BLOCK-NUM-HEAP +
;

\ given flag f and core address, save or restore 512-bytes page
: MANAGE-CORE-PAGE ( f a -- f )

    $3FFF OVER <                \ f a 3FFF<a
    OVER $6300 < AND            \ f a 3FFF<a<6300
    IF
        DROP
    ELSE    
        DUP CALC-CORE-BLOCK     \ f a u
        2 PICK                  \ f a u f
        MANAGE-RW-BLOCK         \ f
    THEN
;

\ given flag f and heap address, save or restore 512-bytes page
: MANAGE-HEAP-PAGE ( f hp -- f )
    DUP CALC-HEAP-BLOCK     \ f a u
    2 PICK                  \ f a u f
    MANAGE-RW-BLOCK         \ f
;

\ based on flag f save or restore the system
: MANAGE-PAGES ( f -- )
    \ manage core lower memory
    $2000 +ORIGIN HERE MIN      \ f a2  
    0 +ORIGIN                   \ f a2 a1
    DO                          \ f 
        I MANAGE-CORE-PAGE      \ f
    B/BUF +LOOP
    $2000 +ORIGIN HERE U<
    IF
        HERE                    \ f a2
        $2000 +ORIGIN           \ f a2 a1 
        DUP 0>
        IF $4000 + THEN 
        DO                          \ f 
            I MANAGE-CORE-PAGE      \ f
        B/BUF +LOOP
    THEN
    \ manage whole heap
    HP@ 0 DO                    \ f hp 0
        I MANAGE-HEAP-PAGE
    B/BUF +LOOP

    \ manage user data
    BLOCK-NUM-USER BLOCK        \ f block
    $2E +ORIGIN @ ROT           \ block addr f
    IF SWAP UPDATE THEN
    #80 CMOVE 
    FLUSH \ anyway
;

: RESTORE-SYSTEM 
\   BLOCK-NUM-CORE BLOCK @ 
\   #8192 = 55 ?ERROR
    0 MANAGE-PAGES 
    ABORT
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

