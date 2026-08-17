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
