\
\ 032-timing.f
\ Timing: ms delays and frame-synchronised animation.
\
\ vForth provides the ms word for millisecond delays.  The ZX Next
\ runs at 50 Hz (PAL) or 60 Hz (NTSC), giving one video frame every
\ 20 ms or 16.7 ms.  Frame-synchronised animation avoids tearing by
\ waiting for the vertical blank before updating the display.  The
\ ms CODE word reads the CPU speed register automatically so it gives
\ correct delays at any clock rate (3.5-28 MHz).
\
\ Reference: sec.7.5
\
\ Load from a clean session:
\   INCLUDE tutorial/032-timing.f
\ To unload and reload interactively:
\   NO-TIMING
\   INCLUDE tutorial/032-timing.f
\

MARKER NO-TIMING

CR
.( --- Tutorial 032: Timing and delays loaded. ) CR
.(     Type NO-TIMING to unload.               ) CR

NEEDS ms
NEEDS .BORDER

\ ===========================================================================
\ 1. ms -- millisecond delay
\ ===========================================================================
\
\   ms ( n -- )   delay n milliseconds (n must be < 8192)
\
\ ms is a CODE word that auto-detects the current CPU speed
\ (register $07) and adjusts its inner loop accordingly.
\ Valid speeds: 0=3.5 MHz  1=7 MHz  2=14 MHz  3=28 MHz.
\
\ Examples:
\   500 ms     \ wait half a second
\   1000 ms    \ wait one second
\   20 ms      \ wait one PAL video frame
\
\ Maximum safe value: 8191 ms (~8 seconds).
\ For longer delays, call ms repeatedly.
\
\ Example: 3-second delay
\   3000 ms
\   ( or: 3 0 DO 1000 ms LOOP )

\ ===========================================================================
\ 2. Video frame timing
\ ===========================================================================
\
\ The ZX Next video system generates interrupts at 50 Hz (PAL) or
\ 60 Hz (NTSC) -- one interrupt per video frame.
\
\ One PAL frame  = 20 ms
\ One NTSC frame = approximately 16 ms
\
\ ISR-SYNC is a CODE word (from lib/INTERRUPTS.f) that executes a
\ Z80 HALT instruction.  HALT suspends the CPU until the next
\ interrupt fires, giving exact frame synchronisation.
\
\ Usage pattern for frame-synchronised animation:
\
\   NEEDS INTERRUPTS
\   BEGIN
\       \ ... update display ...
\       ISR-SYNC    \ wait for next vertical blank
\   ?TERMINAL UNTIL
\
\ Alternatively, use 20 ms for an approximate PAL frame delay:
\
\   BEGIN
\       \ ... update display ...
\       20 ms
\   ?TERMINAL UNTIL
\
\ ?TERMINAL ( -- f ): returns true when BREAK (CAPS SHIFT + SPACE)
\ is pressed.  Use it as the loop exit condition.

\ ===========================================================================
\ 3. Demo: simple counting animation using ms
\ ===========================================================================

NEEDS .AT

: COUNT-DEMO  ( -- )
    CLS
    0 0 .AT  ." Press BREAK to stop." CR
    0
    BEGIN
        1+
        1 0 .AT
        DUP .
        100 ms
        ?TERMINAL
    UNTIL
    DROP  CR
;

\ ===========================================================================
\ 4. Demo: stopwatch -- count elapsed seconds
\ ===========================================================================

: STOPWATCH  ( -- )
    CLS
    0 0 .AT  ." Stopwatch (BREAK to stop)" CR
    0
    BEGIN
        1+
        1 0 .AT  DUP .  ."  seconds"
        1000 ms
        ?TERMINAL
    UNTIL
    DROP CR
;

\ ===========================================================================
\ 5. Demo: frame-synchronised flash using ISR-SYNC
\ ===========================================================================
\
\ The following demo uses ISR-SYNC for exact 50 Hz frame timing.
\ Load INTERRUPTS before using ISR-SYNC.

NEEDS INTERRUPTS

: FRAME-FLASH  ( -- )
    CLS
    0 0 .AT  ." Frame-sync flash demo.  BREAK=stop." CR
    0
    BEGIN
        1+
        DUP 25 MOD 12 < IF  7  ELSE  0  THEN
        .BORDER
        ISR-SYNC        \ wait for vertical blank
        ?TERMINAL
    UNTIL
    DROP
    0 .BORDER
    CLS
;

\ ===========================================================================
\ 6. Demo: longer delay using a loop
\ ===========================================================================

: WAIT-SECONDS  ( n -- )
    0 DO  1000 ms  LOOP
;

\ ===========================================================================
\ 7. Simple tests (requires NEEDS TESTING)
\ ===========================================================================
\
\ ms has no return value and cannot be verified automatically.
\ The following are structural tests only.
\
\ NEEDS TESTING
\ T{  0 ms  ->  }T     \ zero ms does nothing
\ T{  1 ms  ->  }T     \ 1 ms delay
