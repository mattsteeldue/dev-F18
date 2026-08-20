## Possible improvements and Known Bugs

> Resolved entries are moved to TODO-DONE.md.

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


# ?VOCAB and .VOCAB are broken 
**2026-06-01**
Tested on real hardware; both definitions do not work correctly.
Removed from tutorial/018-vocabularies.f until fixed.


# Tutorial 054 (DMA) is a stub, not yet loadable
**2026-08-18**
`tutorial/054-dma.f` demonstrates DMA-COPY, DMA-FILL, DMA-OUT and DMA-IN via
`NEEDS DMA`, but the library it depends on, `dev/DMA.f`, has never been
promoted to `lib/DMA.f`: loading the tutorial today fails at `NEEDS DMA`
("File not found"). The slot is registered in `lib/TUTORIAL.f` (`54
TUTORIAL` resolves the file) and the header/self-references are correct, so
the numbering is reserved, but the tutorial itself cannot run yet.
Even once the library lands, the demo is unverified -- see the "NEEDS
TESTING" section at the bottom of the file: the headless emulator does not
model the zxnDMA controller, so `DEMO` needs a manual CSpect (or
real-hardware) check against the written checklist.
To close this: promote `dev/DMA.f` to `lib/DMA.f`, then run the CSpect
verification checklist already in the tutorial file.


# Several lib/ modules have little to no per-word help/ coverage
**2026-08-20**
Found while auditing `help/` for FAT-filename-mapped word names (every
`inc/` word with a mapped char now has its `help/*.txt`, plus `EXEC:`,
`ASK-Y/N`, `BMP-LOAD"`). The gap turned out to be broader than the mapped
names themselves: `lib/floating.f`, `lib/fixed88.f`, `lib/complex.f`,
`lib/testing.f`, `lib/RPi0.f`, `lib/LED.f`, `lib/ZAP.f`/`ZAP~.f`,
`lib/bleep.f`, `lib/mouse-ay-tester.f`, `lib/AFXFRAME-forth.f`,
`lib/layer3.f` and `lib/MOUSE.f` have little or no per-word `help/` entries
-- not even for their plain-named words (e.g. `F+`, `F-`, `FDUP`, `T{`,
`}T` have none; only `help/floating.txt` documents the module as a whole).
Documenting just the FAT-mapped subset of each module (`F<`, `F>`, `FP*`,
`C*`, `AFX>AY`, `TILE-MODE:`, `ZAP"`, ...) would be incoherent with their
undocumented plain-named siblings in the same file, so none of those were
added -- this needs a deliberate per-module documentation pass instead.
`?--`/`?}` in `lib/LOCALS.f` are the one confirmed exception: private
parsing helpers, intentionally undocumented like `(LOC-BIND)`/`LOC-PFA`,
not part of this gap.

