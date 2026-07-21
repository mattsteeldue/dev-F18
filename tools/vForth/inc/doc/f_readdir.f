\
\ f_readdir.f
\
.( F_READDIR )
\
\ EXPERIMENTAL redefinition -- shadows the core F_READDIR. Must be loaded
\ with INCLUDE, never NEEDS (see f_opendir.f header). Pairs with the new
\ F_OPENDIR: when the directory handle was opened with esx_mode_use_wildcards,
\ pass the SAME wildcard z-string as a2 on every call, and NextZXOS returns
\ only matching entries.
\
\ Behaviourally identical to the core F_READDIR -- the core already threads
\ a2 into DE correctly for the syscall, no logic change was needed. Rewritten
\ here only so the experimental pair is self-contained under inc/ (own inline
\ exit sequence, verified against project/vForth18_DOES/source/next-opt0.asm,
\ instead of jr-ing into the core's internal F_Open_Exit/F_Read_Exit labels).
\

BASE @
HEX

\ given a pad address a1, a wildcard z-string a2 and a file-handle fh,
\ fetch the next available (and, if opened with wildcards, matching) entry
\ of the directory. Return 1 as ok or 0 to signal end of data, then
\ return 0 on success, True flag on error.
CODE F_READDIR  ( a1 a2 fh -- n f )

    D9 C,               \ exx
    E1 C,               \ pop     hl          hl' = fh
    7D C,               \ ld      a,l         a = fh
    D1 C,               \ pop     de          de' = a2 (wildcard)
    DD C, E3 C,         \ ex      (sp),ix     ix = a1  (buffer)
    D9 C,               \ exx
    D5 C,               \ push    de          save real RSP
    C5 C,               \ push    bc          save real IP
    D9 C,               \ exx                 de = a2 again, for syscall
    F3 C,               \ di
    CF C, A4 C,         \ rst     $08 / $A4   F_READDIR syscall
    5F C,               \ ld      e,a         e = n (entries returned)
    16 C, 00 C,         \ ld      d,$00
    FB C,               \ ei
    D9 C,               \ exx
    C1 C,               \ pop     bc
    D1 C,               \ pop     de
    DD C, E1 C,         \ pop     ix
    D9 C,               \ exx
    D5 C,               \ push    de          n
    ED C, 62 C,         \ sbc     hl,hl       flag
    E5 C,               \ push    hl
    D9 C,               \ exx
    DD C, E9 C,         \ jp      (ix)        NEXT

    SMUDGE

BASE !
