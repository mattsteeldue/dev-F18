\
\ dosver.f
\
.( DOSVER )
\

BASE @

NEEDS M_DOSVERSION
NEEDS SPLIT

\ Print the NextZXOS version and language code, eg "NextZXOS v2.08 en"
: DOSVER  ( -- )
    ." NextZXOS v. : "  
    BASE @ 
    M_DOSVERSION DROP
    HEX 0 <# # # [CHAR] . HOLD # #> TYPE
    BASE !
;

BASE !
