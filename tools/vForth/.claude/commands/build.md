---
description: Assemble a vForth variant with SjASMPlus. Usage: /build <DOES|DOT|MDR>
---

Assemble the vForth variant specified in $ARGUMENTS using SjASMPlus.

Variant mapping (case-insensitive):
- DOES -> project/vForth18_DOES   (v1.8 classic, launcher-based)
- DOT  -> project/vForth18_DOT    (v1.8 dot-command, NEX output)
- MDR  -> project/vForth16_MDR_MGT (v1.6 MDR/MGT, historical)

Steps:
1. Parse $ARGUMENTS. If empty, default to DOES and tell the user.
2. Map the variant name to the project folder (see above).
3. Run the assembler with PowerShell:
   ```
   & "c:/Zx/sjasmplus/sjasmplus.exe" `
       "--sld=<folder>/list/main.sld.txt" `
       "--fullpath" `
       "--zxnext" `
       "--lst=<folder>/list/main.lst" `
       "<folder>/source/main.asm"
   ```
4. For the DOT variant only, also run after assembly:
   ```
   cmd /c "cd project\vForth18_DOT\output && copy vforth.1 /b + vforth.2 /b vforth /b"
   ```
5. Report: assembler exit code, any errors or warnings from stdout/stderr, and the
   size of the output binary (check the output/ subfolder).
6. If the build succeeds, remind the user to copy the output to the SD staging area
   (SD/tools/vForth/ for DOES, SD/dot/ for DOT) if the binary has changed.