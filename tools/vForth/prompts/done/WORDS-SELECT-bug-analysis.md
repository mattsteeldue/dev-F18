# WORDS after SELECT bug analysis -- garbage written to file streams

Date: 2026-06-12
Status: FIXED in vForth18_DOES + vForth18_DOT sources, binaries rebuilt;
F18e.f aligned.

## 1. Symptom

From ZX BASIC, open an output stream to a file (`OPEN #13,"o>out.txt"`),
start vForth, then:

    13 SELECT WORDS

The file receives garbage (a repeated `CR 'F' 'i' $7F " s s s..."` pattern)
and the system appears hung -- only BREAK stops it. Meanwhile

    13 SELECT 4 LIST
    13 SELECT 1 100 INDEX

both produce a perfectly healthy out.txt.

## 2. Root cause

A `rst $10` sent to a file-attached stream is routed by NextZXOS through
+3DOS, which on exit restores the OS default banking (via ports
$7FFD/$1FFD). That re-binds MMU7 ($E000-$FFFF) to the bank-0 default page,
**unmapping the vForth heap** where the dictionary name-space lives.

`WORDS` interleaves heap reads with output: per entry it prints the name
(`ID.`) and then fetches the link from the heap (`1 TRAVERSE 1+ @`). Its
very first emitted byte is a `CR` (because `OUT` is preset to 128), so from
the second heap access onward every read hits the wrong page: garbage
names, and a garbage link chain that never reaches 0 -- hence the apparent
hang, interruptible only because the loop polls `?TERMINAL`.

`LIST` and `INDEX` are immune because they only read block buffers, which
live below $E000. Output to the screen (stream #2) is immune because the
ROM print path does not go through +3DOS.

This is not a true v1.7 -> v1.8 source regression: `WORDS`, `EMITC` and
`FAR` are identical in src/F17e.f. The exposure comes from the heap
name-space living in MMU7 pages combined with file-stream output; `(FIND)`
has always protected itself by saving/restoring MMU7 around its work, which
confirms the hazard was known to the design.

## 3. Reproduction (headless emulator)

`emu/test_words_stream.py` boots the core and re-runs `WORDS` while
resetting the MMU7 page to 1 after every emitted byte -- exactly what a
file-stream `rst $10` does on hardware. With the unfixed binary it
reproduces the repeated ` s s s...` garbage and the endless loop; with the
fixed binary both the screen and the "file stream" scenarios print the full
dictionary and return to `ok`.

Note: reproducing this required making the emulator's MMU7 banking real
(page-content swap on NextReg 87 writes) and modelling the NextReg
read-back ports $243B/$253B -- improvements now in emu/emulator.py and
emu/z80_instructions.py.

## 4. Fix

`(EMITC)` now brackets the ROM call:

    push af
    call MMU7_read          ; current page -> A  (ports $243B/$253B)
    ld   (MMU7_Saved), a    ; new one-byte buffer before the (EMITC) header
    pop  af
    rst  $10                ; may unmap MMU7 via +3DOS
    ld   a, (MMU7_Saved)
    nextreg 87, a           ; put the heap page back

`(CLS)` saves the page the same way before its `rst $08/$94` layer query,
because both of its exit paths fall into the shared restore (CLS_Layer_0).

Cost: ~60 T-states per emitted character, negligible against the ROM print
path itself.

Applied to:

- project/vForth18_DOES/source/L0.asm (master)
- project/vForth18_DOT/source/L0.asm (twin, keeps its di/ei around rst $10)
- src/F18e.f -- `(emitc)`/`(cls)` updated; the old hand-coded jr
  displacements (`$E1`/`$DD`) replaced with computed ones via the new
  `clsnol0^` / `clsl0^` forward pointers.

Binaries rebuilt with sjasmplus 1.23.1 (output byte-identical to the
previous toolchain on unmodified sources): forth18e.bin / ram8.bin and the
DOT vforth dot-command.
