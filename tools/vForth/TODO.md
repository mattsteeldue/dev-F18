## Possible improvements and Known Bugs

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

# improve (COMPARE) 
**2026-05-27**
because it uses djnz strings can be 256 bytes in length at most.
Register C seems free: modify the code to use BC instead of B as counter.
**Status: Done** 2026-05-31


# ?VOCAB and .VOCAB are broken 
**2026-06-01**
Tested on real hardware; both definitions do not work correctly.
Removed from tutorial/018-vocabularies.f until fixed.


# EVALUATE little bug
**2026-05-31**
I just discovered this definition has to be put on a new line to work *always*.
Tutorial 021 shows that if written on the same line of some complex evaluating 
strings it does not work well.


# F>D in FLOATING library has bug
**2026-06-01**
The example in tutorial 024:  3.7 F>D D. display 37 instead of 3
Removed from tutorial/024-floating-point.f until fixed.    
UPDATE: False positive, probably I missed typing FLOATING before testing.
**Status: Done** 2026-06-02

