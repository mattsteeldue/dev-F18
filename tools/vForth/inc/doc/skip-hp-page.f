\
\ skip-hp-page.f
\
\ never completely fill a page, leave alone some byte to avoid page spillover
\ reserves 257 bytes ($101) at the top of each 8K page: room for a header
\ written by CREATE past the watermark, and a buffer for stray
\ writes to BASIC's UDG area $FF58-$FFFF while MMU7 holds a heap page

HEX 1EFF CONSTANT PAGE-WATERMARK

\
\ check if  n  more bytes are available in the current 8K-page in Heap
\ otherwise skip  HP  to the beginning of next 8K-page
\
: SKIP-HP-PAGE ( n -- )
    HP@    
    1FFF  AND                   \ take only offset part of HP heap-address
    + 
    PAGE-WATERMARK
    >                           \ check if it is greater than watermark
    IF
        HP@  1FFF OR 1+ 2+ HP ! \ HP goes to the next page
    THEN
    \ HP@  0=  [ DECIMAL 12 ] LITERAL  ?ERROR  \ out of memory check
;


