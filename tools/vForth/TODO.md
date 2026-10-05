## Possible improvements and Known Bugs

> Resolved entries are moved to TODO-DONE.md.

# VS Code extension: colorize known words in the help files too
**2026-10-05**
A small enhancement wished for the VS Code extension: highlight/colorize the
words it already knows (core and lib) also inside the `help/*.txt` files, not
only in the Forth sources. The help texts are full of word names (stack
effects, "See also" lines, examples), so the same colouring would make them
much easier to read. If possible they should also become navigable inside
VS Code itself (e.g. go to definition / follow the word to its source or to
its own help file). Mind the FAT filename mapping (`help/` names are mapped,
the words inside the text are the real Forth names).

# ?VOCAB is still incomplete
**2026-06-01**, revised **2026-10-04**
`.VOCAB` is fixed (build 2026-09-26, see TODO-DONE.md). `?VOCAB`
(`inc/^vocab.f`) now prints the right Current and Context lines, but:
- it ends with `VOC-LINK @` and nothing consumes it: one stray cell is left
  on the stack at every call, and the "Voc-Link" line prints no value;
- the `BEGIN ... UNTIL` walk of the vocabulary chain is still commented out.
Checked on the headless emulator only; the original failure was seen on real
hardware and has not been re-tested there. The `.VOCAB` examples in section 6
of `tutorial/018-vocabularies.f` are still commented out.


# DMA: at what speed does the transfer actually run?
**2026-10-04**
Left open when tutorial 054 was closed (see TODO-DONE.md). On a real Next
`32 STRIPES` works with the CPU at 28 MHz (`tutorial/054-stripes.png`), but
the transfer to port $FE looks as if the DMA ran at 3.5 MHz. Tests are needed
to settle the question: read the CPU speed with `7 REG@`, then run
`32 STRIPES` after `0 SPEED!` (3.5 MHz) and after `3 SPEED!` (28 MHz) and
compare the width of the border bands in the two captures. If the bands do
not change, the DMA rate does not follow the CPU speed. The headless emulator
does not model the zxnDMA controller, so this needs real hardware (or
CSpect, as a second opinion). Record the outcome in the status note at the
bottom of `tutorial/054-dma.f`.


# Several lib/ modules have little to no per-word help/ coverage
**2026-08-20**, revised **2026-10-04**
Found while auditing `help/` for FAT-filename-mapped word names (every
`inc/` word with a mapped char now has its `help/*.txt`, plus `EXEC:`,
`ASK-Y/N`, `BMP-LOAD"`). The gap turned out to be broader than the mapped
names themselves: `lib/floating.f`, `lib/fixed88.f`, `lib/complex.f`,
`lib/testing.f`, `lib/RPi0.f`, `lib/LED.f`, `lib/ZAP.f`/`ZAP~.f`,
`lib/bleep.f`, `lib/mouse-ay-tester.f`, `lib/AFXFRAME-forth.f`,
`lib/layer3.f` and `lib/MOUSE.f` have little or no per-word `help/` entries
-- not even for their plain-named words (e.g. `F+`, `F-`, `FDUP`, `T{`,
`}T` have none; only `help/floating.txt` documents the module as a whole).
Core words are fully covered: checked on 2026-10-04 against the RENAME
block of `src/F18e.f` (334 names), the `WORDS` listing at boot and the
definition macros of `L0.asm`-`L3.asm`; no core word lacks a page. The gap
is outside the core: `lib/` is measured below, `inc/` was not re-audited.

First pass on 2026-10-04: 65 pages written for the words used in the
compiled code of the tutorials that had none (MOUSE, RPi0/UART, AFXFRAME,
GRAPHICS, AY, beeper, BMP-LOAD, Copper, FLOATING, INTERRUPTS, LAYER3, the
`LAYERx`/`MMUn!`/`MS`/`UNLINK` words of `inc/`, ASSEMBLER). They await the
author's validation. Left out on purpose: the assembler mnemonics and
register names of tutorials 027 and 057 (about 35), and words that appear
only inside tutorial comments.
Found while writing `help/bleep.txt`: tutorial 033 and the header comment of
`lib/bleep.f` give the two `BLEEP` arguments in the opposite order to what
the code consumes (`BLEEP-CALC` leaves cycles below, pitch on top) -- to fix.

Audit of 2026-10-04 after that pass, all of `lib/*.f`: about 880 names
defined, 147 with a `help/` page of their own (74 before the pass).
Counted: every name defined with `:`, `CODE`, `CREATE`, `VARIABLE`,
`CONSTANT`, `VALUE` and the like, looked up as `help/<name>.txt` through the
FAT mapping. The figure overstates the work (constants and private helpers
are counted, and so are the several copies of AFXFRAME and GRAPHICS) and
misses names created by a module's own defining words (`F+`, `F-`, `F*` in
`floating.f`; the `TILE-*` modes of `layer3.f`, which do have pages).
Figures are "with help / defined"; "page" = a `help/<module>.txt` exists.

    Modules named above
      floating.f          7/40  page      LED.f               1/69
      fixed88.f           0/50            ZAP.f               1/19
      complex.f           0/19            ZAP~.f              0/10
      testing.f           1/36            bleep.f             3/6   page
      RPi0.f              8/42  page      mouse-ay-tester.f   0/7
      MOUSE.f             7/33  page      AFXFRAME-forth.f    2/7
      layer3.f            0/7   page (+5 TILE-* pages)

    Not named above, still no page at all
      SPRITE.f            0/18            TILE80.f            0/17
      UART-SYS.f          0/15            udg+.f              0/7
      TUTORIAL.f          0/6             mouse-tester.f      0/4
      FP-INTERFACE.f      0/3             LAYER24-GRAPHICS.f  0/3
      bsearch.f           0/3             locate.f            0/2
      IDE_PATH.f          0/2             TILE80-setup.f      0/2
      heap.f  hide-word.f  set-fence.f  used-by.f             0/1 each

    Module page plus a few words
      GRAPHICS.f         16/91  page      GRAPHICS-COMMON.f  15/56  page
      edit.f              1/32  page      see.f               2/20  page
      INTERRUPTS.f        4/18  page      DIR.f               1/14  page
      PERSISTENCE.f       1/17            editor.f            1/13
      AY.f                6/14  page      copper.f            6/12  page
      afxplay.f           6/13            bmp-load.f          3/9   page

    Partly covered
      DMA.f              16/43  page  (missing: DMA-CMD-*, DMA-WR* constants
                                       and the parenthesised helpers)
      LOCALS.f            6/32  page  (missing: private helpers only)
      needs.f             9/11  page
      assembler.f         3/3   page  (complete)

Many of the missing names are internal and need no page (`DEB-*` in `see.f`,
`LED-*`, `(LOC-*)`, port constants). The real work is deciding, module by
module, which words are public.

Documenting just the FAT-mapped subset of each module (`F<`, `F>`, `FP*`,
`C*`, `AFX>AY`, `TILE-MODE:`, `ZAP"`, ...) would be incoherent with their
undocumented plain-named siblings in the same file, so none of those were
added -- this needs a deliberate per-module documentation pass instead.
`?--`/`?}` in `lib/LOCALS.f` are the one confirmed exception: private
parsing helpers, intentionally undocumented like `(LOC-BIND)`/`LOC-PFA`,
not part of this gap.


# chomp-chomp: write a "Next-like" capstone tutorial
**2026-08-22**, revised **2026-10-04**
A Next-like rewrite of `demo/chomp-chomp` (currently a portable
sprite/tilemap game, see tutorial 059 for how it ships via ZAP) as a
before/after capstone tutorial, using the hardware-accelerated primitives
introduced across the 030-059 band (hardware sprites -- tutorial 053,
tilemap -- tutorial 058) in place of the original software model.
The rewrite is under way in `demo/chomp-chomp-next/`, following
`planners/CHOMP-CHOMP-NEXT-PLAN.md`: Stage 1 (AY sound, 2026-08-27) and
Stage 2 (hardware sprites, 2026-09-01) are implemented and both still await
CSpect confirmation; Stages 3-5 (palette effects, interrupt pacing, tilemap
maze) are not started. The tutorial itself is not started. Note that
`demo/chomp-chomp-next/README.txt` still points at the plan's old location,
`prompts/CHOMP-CHOMP-NEXT-PLAN.md`.


# ASK-Y/N as a reusable NEEDS word
**2026-09-23**
Possible evolution, deliberately not implemented: the boot path is not worth
the risk for now. `ASK-Y/N` lives only inside `lib/AUTOEXEC.f`, behind
`MARKER FORGET-THIS-TASK-3`, and forgets itself before `QUIT`; so
`help/ask-y%n.txt` documents a word the user can never call.
Idea: a new `inc/ask-y%n.f` returning a flag instead of quitting, Y default:

    : ASK-Y/N  ( -- f )  \ true unless N/n
        ." (Y/n) "  CURS KEY DUP EMIT  UPPER [CHAR] N - 0= 0= ;

and in `lib/AUTOEXEC.f` a small local word that still performs the `QUIT`
(no conditional interpretation available):

    MARKER FORGET-THIS-TASK-3
    NEEDS ASK-Y/N
    : ?UTILITIES  ." Autoexec asks: Do you wish to load utilities ? "
        ASK-Y/N  FORGET-THIS-TASK-3  0= IF ." ok " QUIT THEN ;
    CR ?UTILITIES

`lib/AUTOEXEC-DOT.f` needs no change (it only does `11 LOAD`, which includes
the same `lib/autoexec.f`).
Benefits: `help/ask-y%n.txt` becomes a regular "Available after NEEDS" entry;
a reusable prompt (tutorials 016 `YES?` and 035 `YES-OR-NO` each roll their
own). Costs: one more file open on every boot, on the most delicate path;
two files to maintain instead of one. No dictionary cost, since `NEEDS`
follows the MARKER and the word is forgotten with it.
Semantics to settle: autoexec treats any key but N as yes, the tutorials loop
until Y or N. Verify on the headless emulator (`emu/repl.py` smoke test goes
through ASK-Y/N answering `n`) and on CSpect for both DOES and DOT.
