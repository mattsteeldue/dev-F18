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


# F>D in FLOATING library has bug
**2026-06-01**
The example in tutorial 024:  3.7 F>D D. display 37 instead of 3
Removed from tutorial/024-floating-point.f until fixed.    
UPDATE: False positive, probably I missed typing FLOATING before testing.
**Status: Done** 2026-06-02
