\
\ wildcard.f
\
.( WILDCARD )
\
\ Parses the next word in the input stream as a DOS-style wildcard pattern
\ (* / ?) and keeps it ready, null-terminated, as the "wc" argument for
\ F_OPENDIR / F_READDIR (inc/f_opendir.f, inc/f_readdir.f): NextZXOS itself
\ filters entries when the directory is opened with esx_mode_use_wildcards,
\ so no Forth-side WILDCARD? matching is needed on that path anymore.
\
\ Independent of DIR (lib/dir.f): DIR keeps parsing only the path that
\ follows it in the input stream, exactly as today. WILDCARD-SPEC defaults
\ to "*" (match all) until WILDCARD is called; call it separately, anywhere
\ earlier on the same input line, to change the pending pattern:
\
\     WILDCARD *.F  DIR MYDIR
\

BASE @ DECIMAL

CREATE WILDCARD-SPEC  32 ALLOT      \ null-terminated pattern buffer
CHAR * WILDCARD-SPEC C!             \ default: match-all
0 WILDCARD-SPEC 1+ C!

: WILDCARD  ( -- )
    BL WORD COUNT                   \ a n
    DUP 0= IF
        2DROP
        [CHAR] * WILDCARD-SPEC C!
        0 WILDCARD-SPEC 1+ C!
    ELSE
        DUP >R                       \ a n              R: n
        WILDCARD-SPEC SWAP CMOVE     \ a WILDCARD-SPEC n  copy text     R: n
        0 WILDCARD-SPEC R> + C!      \ terminate at WILDCARD-SPEC+n
    THEN
;

BASE !
