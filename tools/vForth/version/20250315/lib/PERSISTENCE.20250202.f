\
\ lib/persistence.f
\
\ v-Forth 1.8 - NextZXOS version - build 2025-01-01            
\ MIT License (c) 1990-2025 Matteo Vitturi     
\

.( PERSISTENCE ) 

\ save the complete current vForth status to blocks 

MARKER PERSISTENCE

\ starting block number where memory is dumped
\ User data 32063
\ Core is stored from 32000 to 32062
\ Heap is stored in blocks from 32064 to 32191
\ dot-version uses 31800-31991

#32000 0 +ORIGIN $4000 > 1+ #200 * +
CONSTANT BLOCK-NUM-CORE

#64 BLOCK-NUM-CORE + 
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
        $3E EMIT
\       2DUP 
\       CR U. U. 
        SAVE-TO-BLOCK
    ELSE
        $3C EMIT
\       2DUP 
\       CR U. U. 
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
    9 RSHIFT
    BLOCK-NUM-HEAP +
;

\ given flag f and core address, save or restore 512-bytes page
: MANAGE-CORE-PAGE ( f a -- f )
    DUP CALC-CORE-BLOCK     \ f a u
    2 PICK                  \ f a u f
    MANAGE-RW-BLOCK         \ f
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
    HERE 0 +ORIGIN              \ f a2 a1
    DO
        I MANAGE-CORE-PAGE      \ f
    B/BUF +LOOP
    \ key drop
    \ manage whole heap
    HP@ 0 DO                    \ f hp 0
        I MANAGE-HEAP-PAGE
    B/BUF +LOOP
    \ manage user data
    BLOCK-NUM-HEAP 1- BLOCK     \ f block
    $2E +ORIGIN @ ROT           \ block addr f
    IF SWAP UPDATE THEN
    #80 CMOVE 
    FLUSH \ anyway
;
    
: CLEAR-PAGES 
    -1 CALC-HEAP-BLOCK
    BLOCK-NUM-CORE
    DO 
        I BLOCK B/BUF ERASE UPDATE
    LOOP    
;

: SAVE-SYSTEM    
    1 MANAGE-PAGES 
;

: RESTORE-SYSTEM 
    0 MANAGE-PAGES 
    EMPTY-BUFFERS
    WARM
;

