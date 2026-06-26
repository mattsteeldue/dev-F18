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
6. Deploy (DOES only). After a successful DOES build, verified by tests (at minimum
   the headless-emulator smoke test: boot to the SPLASH banner, e.g.
   `printf '.quit\n' | python3 emu/repl.py | grep build` shows the expected build date),
   copy the two binaries to the repo base directory -- the same directory that holds
   `!Blocks-64.bin` -- so that /sync-cspect will carry them onto the SD image:
   ```
   project/vForth18_DOES/output/forth18e.bin  ->  ./forth18e.bin
   project/vForth18_DOES/output/ram8.bin      ->  ./ram8.bin
   ```
   Copy only if content differs (compare MD5). If the tests fail, do NOT deploy:
   report the failure and leave the base directory untouched.
7. Deploy (DOT only). After a successful DOT build, verified by tests, copy the
   concatenated 16KB binary to the repo dot/ directory:
   ```
   project/vForth18_DOT/output/vforth  ->  ./dot/vforth
   ```
   Copy only if content differs (compare MD5). Note the two-leg path: this first
   leg lands in the repo; the second leg is handled by /sync-cspect, whose phase 4
   copies dot/ to `W:\dot` (the NextZXOS dot-command directory at the ROOT of the
   SD image, NOT under W:\tools\vForth).