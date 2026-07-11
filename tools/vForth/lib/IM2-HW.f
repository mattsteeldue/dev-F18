\
\ IM2-HW.f
\
.( IM2-HW )
\
\ Hardware Interrupt Mode 2 for ZX Spectrum Next (core 3.0+).
\ Uses Next registers $C0/$C4/$C5/$C6 to give each interrupt source
\ (line, UART, CTC 0-7, ULA) its own vector-table slot with hardware
\ daisy-chain priority: the handler that runs knows which source fired.
\
\ Used in the form:
\
\   ' cccc IM2-HW-SLOT-ULA IM2-HW-HANDLER!
\   IM2-HW-ON                        \ ULA source enabled by default
\   IM2-HW-SLOT-CTC0 IM2-HW-ENABLE   \ optionally enable more sources
\   ...
\   IM2-HW-OFF
\
\ Handler contract: handlers run on the small ISR stacks shared with
\ lib/INTERRUPTS.f (about 40 cells). Keep them short: no console or
\ file I/O, no MMU7 remapping without save/restore (see tutorial 049).
\ Classic ISR-ON mode and IM2-HW-ON mode are mutually exclusive.
\

NEEDS INTERRUPTS

BASE @

HEX

MARKER NO-IM2-HW

\ ____________________________________________________________________

\ Slot numbers in hardware daisy-chain priority order (dev guide r3).
00 CONSTANT IM2-HW-SLOT-LINE
01 CONSTANT IM2-HW-SLOT-UART0RX
02 CONSTANT IM2-HW-SLOT-UART1RX
03 CONSTANT IM2-HW-SLOT-CTC0
04 CONSTANT IM2-HW-SLOT-CTC1
05 CONSTANT IM2-HW-SLOT-CTC2
06 CONSTANT IM2-HW-SLOT-CTC3
07 CONSTANT IM2-HW-SLOT-CTC4
08 CONSTANT IM2-HW-SLOT-CTC5
09 CONSTANT IM2-HW-SLOT-CTC6
0A CONSTANT IM2-HW-SLOT-CTC7
0B CONSTANT IM2-HW-SLOT-ULA
0C CONSTANT IM2-HW-SLOT-UART0TX
0D CONSTANT IM2-HW-SLOT-UART1TX

\ ____________________________________________________________________
\
\ return-from-interrupt low-level definition: exact mirror of the
\ IM2-COMMON dispatch below. Restores SP, both register sets and IX,
\ then ei + reti (reti: daisy-chain convention for hardware IM2).
\
CODE IM2-HW-RET  ( -- )
    ED C, 7B C, ISR-SAVE-SP ,   \ ld sp,(ISR-SAVE-SP)
    D9 C,                       \ exx
    DD C, E1 C,                 \ pop ix
    C1 C, D1 C, E1 C,           \ pop bc, de, hl   (alternate set)
    D9 C,                       \ exx
    C1 C, D1 C,                 \ pop bc, de       (main set)
    F1 C, 08 C, F1 C,           \ pop af  ex af,af'  pop af
    E1 C,                       \ pop hl           (the stub's push)
    FB C,                       \ ei
    ED C, 4D C,                 \ reti
SMUDGE

\ ____________________________________________________________________

.( IM2-FRAGS )

\ 16 threaded fragments, one per slot: [ handler-xt, IM2-HW-RET ].
\ Installing a handler stores its xt in the first cell of the pair.
CREATE IM2-FRAGS
    ' NOOP , ' IM2-HW-RET ,     \ 00 LINE
    ' NOOP , ' IM2-HW-RET ,     \ 01 UART0 Rx
    ' NOOP , ' IM2-HW-RET ,     \ 02 UART1 Rx
    ' NOOP , ' IM2-HW-RET ,     \ 03 CTC0
    ' NOOP , ' IM2-HW-RET ,     \ 04 CTC1
    ' NOOP , ' IM2-HW-RET ,     \ 05 CTC2
    ' NOOP , ' IM2-HW-RET ,     \ 06 CTC3
    ' NOOP , ' IM2-HW-RET ,     \ 07 CTC4
    ' NOOP , ' IM2-HW-RET ,     \ 08 CTC5
    ' NOOP , ' IM2-HW-RET ,     \ 09 CTC6
    ' NOOP , ' IM2-HW-RET ,     \ 0A CTC7
    ' NOOP , ' IM2-HW-RET ,     \ 0B ULA
    ' NOOP , ' IM2-HW-RET ,     \ 0C UART0 Tx
    ' NOOP , ' IM2-HW-RET ,     \ 0D UART1 Tx
    ' NOOP , ' IM2-HW-RET ,     \ 0E reserved
    ' NOOP , ' IM2-HW-RET ,     \ 0F reserved

\ ____________________________________________________________________

\ 32-byte aligned vector table: 32-aligned and 32 bytes long, so it
\ can never cross a 256-byte page boundary.
HERE 1F AND NEGATE 1F AND ALLOT
HERE 20 ALLOT CONSTANT IM2-HW-TABLE

\ ____________________________________________________________________
\
\ common dispatch code: every stub jumps here with the interrupted
\ program's HL already pushed and HL = fragment address for its slot.
\ Saves the full context, moves Forth onto the ISR stacks, sets IP to
\ the fragment and enters the inner interpreter.
\
HERE
    F3 C,                       \ di  (the ULA stub's rst 38 did ei)
    F5 C, 08 C, F5 C,           \ push af  ex af,af'  push af
    D5 C, C5 C,                 \ push de, bc      (main: RSP, IP)
    D9 C,                       \ exx
    E5 C, D5 C, C5 C,           \ push hl, de, bc  (alternate set)
    DD C, E5 C,                 \ push ix
    D9 C,                       \ exx  (back: HL = fragment address)
    44 C, 4D C,                 \ ld b,h  ld c,l   (IP = fragment)
    ED C, 73 C, ISR-SAVE-SP ,   \ ld (ISR-SAVE-SP),sp
    31 C, ISR-SP0 ,             \ ld sp, ISR-SP0
    11 C, ISR-RP0 ,             \ ld de, ISR-RP0
    DD C, 21 C, (NEXT) ,        \ ld ix, next
    DD C, E9 C,                 \ jp (ix)
CONSTANT IM2-COMMON

\ ____________________________________________________________________

.( IM2-STUBS )

\ one small stub per slot; its address goes into the vector table.
\ The ULA stub is prefixed with rst 38 so the ROM 50Hz housekeeping
\ (keyboard scan, FRAMES) keeps running while hardware IM2 is active.
: IM2-STUB,  ( slot -- )
    HERE OVER 2* IM2-HW-TABLE + !
    DUP IM2-HW-SLOT-ULA = IF FF C, THEN
    E5 C,                       \ push hl
    21 C, 4 * IM2-FRAGS + ,     \ ld hl, fragment
    C3 C, IM2-COMMON ,          \ jp IM2-COMMON
;

: IM2-STUBS,  ( -- )  10 0 DO  I IM2-STUB,  LOOP ;

IM2-STUBS,

\ ____________________________________________________________________

\ slot -> (register, mask) for the Interrupt Enable 0/1/2 registers.
\ Reserved slots map to register 0 = no-op.
CREATE IM2-REGBITS
    C4 C, 02 C,                 \ 00 LINE
    C6 C, 01 C,                 \ 01 UART0 Rx
    C6 C, 10 C,                 \ 02 UART1 Rx
    C5 C, 01 C,                 \ 03 CTC0
    C5 C, 02 C,                 \ 04 CTC1
    C5 C, 04 C,                 \ 05 CTC2
    C5 C, 08 C,                 \ 06 CTC3
    C5 C, 10 C,                 \ 07 CTC4
    C5 C, 20 C,                 \ 08 CTC5
    C5 C, 40 C,                 \ 09 CTC6
    C5 C, 80 C,                 \ 0A CTC7
    C4 C, 01 C,                 \ 0B ULA
    C6 C, 04 C,                 \ 0C UART0 Tx
    C6 C, 40 C,                 \ 0D UART1 Tx
    00 C, 00 C,                 \ 0E reserved
    00 C, 00 C,                 \ 0F reserved

: IM2-REGBIT  ( slot -- reg mask )
    2* IM2-REGBITS + DUP C@ SWAP 1+ C@ ;

\ ____________________________________________________________________

.( IM2-HW API )

\ install / query a slot's handler
: IM2-HW-HANDLER!  ( xt slot -- )  4 * IM2-FRAGS + ! ;

: IM2-HW-HANDLER@  ( slot -- xt )  4 * IM2-FRAGS + @ ;

\ enable / disable one interrupt source (read-modify-write)
: IM2-HW-ENABLE  ( slot -- )
    IM2-REGBIT OVER
    IF  OVER REG@ OR SWAP REG!  ELSE  2DROP  THEN ;

: IM2-HW-DISABLE  ( slot -- )
    IM2-REGBIT OVER
    IF  FF XOR OVER REG@ AND SWAP REG!  ELSE  2DROP  THEN ;

\ ____________________________________________________________________

.( IM2-HW-ON )

\ enter hardware IM2 mode: ULA source only at first (its stub's
\ rst 38 keeps the system alive); add sources with IM2-HW-ENABLE.
: IM2-HW-ON  ( -- )
    ISR-DI
    01 C4 REG!
    00 C5 REG!
    00 C6 REG!
    IM2-HW-TABLE 8 RSHIFT SETIREG
    IM2-HW-TABLE E0 AND 01 OR C0 REG!
    ISR-IM2
    ISR-EI
;

\ ____________________________________________________________________

.( IM2-HW-OFF )

\ leave hardware IM2 mode and restore the reset defaults
: IM2-HW-OFF  ( -- )
    ISR-DI
    00 C0 REG!
    81 C4 REG!                  \ reset default: expansion bus + ULA
    00 C5 REG!
    00 C6 REG!
    ISR-OFF
;

\ ____________________________________________________________________

BASE !

: IM2-HW ;
