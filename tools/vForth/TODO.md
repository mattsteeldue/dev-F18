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

