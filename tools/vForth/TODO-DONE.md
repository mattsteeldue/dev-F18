## Resolved improvements and fixed bugs

Entries moved here from TODO.md once marked **Status: Done**.


# improve (COMPARE) 
**2026-05-27**
because it uses djnz strings can be 256 bytes in length at most.
Register C seems free: modify the code to use BC instead of B as counter.
**Status: Done** 2026-05-31


# EVALUATE little bug
**2026-05-31**
I just discovered this definition has to be put on a new line to work *always*.
Tutorial 021 shows that if written on the same line of some complex evaluating 
strings it does not work well.
**2026-06-11** Root cause found and fix proposed (verified in the headless
emulator): see doc/EVALUATE-bug-analysis.md, repro in test/evaluate-bug-repro.f,
candidate fix in test/evaluate-bug-fix.f.
**Status: Done** 2026-06-11 -- inc/evaluate.f patched (commit 355851e).


# MAKEDIR / REMOVEDIR create paths with a trailing space
**2026-08-17**
`MAKEDIR example` on CSpect created a directory literally named `example ` -- with a
trailing space. Windows cannot even open such a name through a normal path (the Win32
layer trims trailing spaces), so on the mounted SD image the entry was listed but
unreachable: it broke every recursive `Get-ChildItem` over `W:\tools\vForth`, which in
turn silenced the CSpect-edited guard of `util\sync2sd.ps1` (`Get-CSpectProtectedSourcePaths`
always returned empty). The stray directory was deleted from the image via a `\\?\`
prefixed path.

Cause -- `(PARSE-PATH)` in `lib/IDE_PATH.f`. `MAKEDIR` and `REMOVEDIR` themselves were
correct: they only hand on the address `(PARSE-PATH)` returns.

    : (PARSE-PATH) ( -- a )
        BL WORD COUNT           \  a  n
        OVER + 1+  $FF SWAP C!  \  a          -- append $FF terminator
    ;

`COUNT` already returns the address of the first text character, so `a + n` is the byte
just past the last character -- exactly where the `$FF` terminator belongs. The extra
`1+` wrote it one byte further, leaving in between the blank that `WORD` appends to the
packet (`here 34 blank`, see `src/F18e.f` line 4086: "WORD ... ends the packet with two
spaces"). The pathspec handed to NextZXOS service $01B1 was therefore `example` + `$20` +
`$FF`.

A regression, not a long-standing bug. Until commit `efe06af` (2026-08-01, "filesystem
utilities" -- the same commit that split `MAKEDIR`/`REMOVEDIR`/`CD`/`PWD` into `inc/`) the
module used `PATH>PAD`, which copied the text to `PAD` and terminated it at `PAD+n`, i.e.
with no `1+`.

**Status: Done** 2026-08-17 -- the `1+` dropped from `(PARSE-PATH)`; `$FF` now lands on
`a+n`, overwriting the first of the blanks `WORD` appended. `MAKEDIR EXAMPLE` /
`REMOVEDIR EXAMPLE` verified OK on CSpect, and a recursive enumeration of the SD image
no longer trips over an unreachable name.


# F>D in FLOATING library has bug
**2026-06-01**
The example in tutorial 024:  3.7 F>D D. display 37 instead of 3
Removed from tutorial/024-floating-point.f until fixed.    
UPDATE: False positive, probably I missed typing FLOATING before testing.
**Status: Done** 2026-06-02


# Missing tutorial: fixed-point Q8.8/12.4 arithmetic
**2026-08-22**
Screen 590-595 in `!Blocks-64.bin` implement fixed-point Q8.8/12.4
arithmetic (`*/` with a 32-bit intermediate, `SPLIT`), but no tutorial/
promotes this material -- it exists only as screens. Write the dedicated
tutorial. Numbering: `030-059` is the ZX Next hardware band and is now
full (tilemap landed at 058, `063-blocks-as-assets.f` is the last slot
used); decide whether this lands past 063 (advanced-topics band, per
`tutorial/CLAUDE.md` numbering rules) or gets inserted earlier.
**Status: Done** 2026-08-22 -- tutorial/064-scaled-integer-math.f.


# Promote demo/brot.f and demo/Fedora.f to tutorial/
**2026-08-22**
`demo/brot.f` (Layer2/Mandelbrot) and `demo/Fedora.f` (vectorial/trig
graphics) have not been promoted to `tutorial/`, unlike their sibling
`demo/parser.dot.f` which became tutorial 057. Write the corresponding
tutorials following the standard tutorial/CLAUDE.md structure.
**Status: Done** 2026-08-27 -- brot.f became tutorial 064, Fedora.f
tutorial 065 (065-fedora-silhouette.f).


# .VOCAB is broken
**2026-06-01**
Split from the TODO.md entry "?VOCAB and .VOCAB are broken" (tested on real
hardware, both removed from tutorial/018-vocabularies.f). `.VOCAB` stepped
back two cells from the voc-link before calling `NFA`, one too many.
**Status: Done** 2026-09-27 (build 2026-09-26, commit 49ef116) -- one `CELL-`
dropped in `inc/.vocab.f`. On the headless emulator `CURRENT @ .VOCAB` prints
`753E FORTH` and `SHAPES CONTEXT @ .VOCAB` prints `81D7 SHAPES`. Not re-tested
on real hardware. What is left of `?VOCAB` stays in TODO.md.


# ASSEMBLER has no NO-ASSEMBLER restore word
**2026-06-03**
`ASSEMBLER` patches `;CODE` in the core by replacing the `NOOP` placeholder with the
ASSEMBLER vocabulary. There is no `NO-ASSEMBLER` word to undo this patch and restore
`;CODE` to its original state. This has never been a problem in practice because ASSEMBLER
is the only library that patches `;CODE`, so the patched state is always consistent while
ASSEMBLER is loaded. However it means ASSEMBLER cannot be cleanly unloaded and reloaded
within a session without a full restart.
Analyse whether a NO-ASSEMBLER is feasible and whether ;CODE needs a two-slot design
(stub + restore pointer) analogous to the FLOATING / NO-FLOATING pattern.
**Status: Done** 2026-10-04 -- `NO-ASSEMBLER` added to `lib/assembler.f`: it
verifies the 4th xt of `;CODE` is `ASSEMBLER` (error #14 otherwise), stores
`NOOP` back and runs the `FORGET-ASSEMBLER` marker; no two-slot design was
needed. `COLD` is redefined as `NO-ASSEMBLER COLD`, like FLOATING does.
Verified on the headless emulator only: load / unload / reload, a `CODE`
word assembled after the reload, and `COLD` with the library loaded.


# Tutorial 054 (DMA): verification still partial
**2026-10-03**
`lib/DMA.f` is promoted (it was `dev/DMA.f`), `NEEDS DMA` works and the 15
`help/dma*.txt` pages say "Available after NEEDS DMA". On a real Next
(2026-10-02) the module loads and `32 STRIPES` draws the border bands at
28 MHz (checklist item 4, `tutorial/054-stripes.png`).
Still open, see the "NEEDS TESTING" section at the bottom of
`tutorial/054-dma.f`: the DUMP checks (items 2-3), and why the transfer to
port $FE looks as if the DMA ran at 3.5 MHz (`7 REG@`, then `32 STRIPES`
after `0 SPEED!` and after `3 SPEED!`). The headless emulator does not model
the zxnDMA controller, so these need CSpect or real hardware.
**Status: Done** 2026-10-04 -- tutorial 054 created and tested by the author
on a real Next. Evidence that the DMA works: `tutorial/054-stripes.png`,
captured from the Next's video output through OBS while `32 STRIPES` was
sending 2048 bytes to port $FE. The question of the actual transfer speed
stays open as a separate entry in TODO.md.
