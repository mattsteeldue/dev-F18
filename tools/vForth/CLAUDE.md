# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in
this repository.

> **Specialized context** is in subdirectory CLAUDE.md files, loaded automatically when
> working in that directory:
> - `project/CLAUDE.md` -- assembler build workflow, F18e.f<->asm mnemonic table, key files
> - `inc/CLAUDE.md` -- single-word definition conventions, CODE words, hex literals
> - `lib/CLAUDE.md` -- module conventions, heap memory facility, nextsync deployment
> - `tutorial/CLAUDE.md` -- tutorial authoring conventions (supersedes tutorial-conventions.md)
> - `help/CLAUDE.md` -- help file format and naming
> - `test/CLAUDE.md` -- test suite structure and {..}T notation

## Project Overview

**vForth Next** is a Forth compiler and runtime system for the Sinclair ZX Spectrum Next
computer. It includes a complete Forth compiler (self-bootstrapping), Z80/Z80N assembly
support, and multiple library modules for graphics, sound, file I/O, and hardware control.

**Current version**: 1.8 (build 2026-08-17)  
**License**: MIT  
**Author**: Matteo Vitturi

### Build number convention

Whenever the core binary changes (forth18e.bin / ram8.bin / the DOT
dot-command), the deliverable gets a new build number = the current date.
It appears in two encodings -- `YYYY-MM-DD` in the SPLASH banner strings
(DOES and DOT `L0.asm`), in `src/F18e.f`'s header, in this file's "Current
version" line and in the first 512-byte block of `!Blocks-64.bin`;
`YYYYMMDD` in the `main.asm` header comments. The **`/bump-build` skill**
(`.claude/skills/bump-build/SKILL.md`) updates every canonical location and
rebuilds both variants; historical copies under `version/`,
`project/*/source/version/`, `util/` and `doc/` must never be touched.
Build dates found in `.f` sources under `inc/` and `lib/` are the last-edit
date of that single file, NOT the core build number: never mass-update them
(it would only flood git) -- they change only when that file's content does.

### Reference manual (.odt/.pdf)

The manual `doc/vForth1.8-core-en-YYYYMMDD.odt` (and its exported `.pdf`)
must **never be edited automatically**. Its "Dictionary memory structure"
section contains build-specific hex addresses and SEE/DUMP transcripts for
the SWAP/DUP example: after a core rebuild, the **`/regen-doc-dict-structure`
skill** (`.claude/skills/regen-doc-dict-structure/SKILL.md`) runs
`util/gen-dict-structure.py` to regenerate that text from the current
binaries via the headless emulator; the author then pastes it into the .odt
by hand and re-exports the .pdf.

**The one sanctioned exception** is `util/odt-hygiene.py`, and only when the
author asks for it. It reports -- and with `--fix` removes -- the `_Toc*` /
`_Hlk*` bookmarks Word leaves behind on every "update TOC": they accumulate
one generation per round-trip and are inherited by every release, because
each build's manual starts as a copy of the previous one (18617 of them,
30% of `content.xml`, were removed on 2026-08-18, worth an order of
magnitude in open/save time). The fix touches `content.xml` only, asserts
the visible text is byte-identical, and re-validates the archive before
replacing the original -- so **the `.pdf` does not need re-exporting**.
Run it in report mode freely; it is read-only and exits 1 when residue is
found, which is how `/release-rebuild` gates on it (step 1c). Everything
else about the manual still goes through the author by hand.

## The Three Codebases and Their Roles

The project has three codebases in order of priority:

1. **vForth18_DOES** -- the master. All changes originate here.
2. **vForth18_DOT** -- near-identical twin. The vast majority of source is shared with
   vForth18_DOES; only startup/closedown routines and MMU7 8K page allocation differ.
3. **F18e.f** -- a historical artifact. Its primary value is **readability**: a Forth
   programmer can study it to understand how the core is implemented, in idiomatic Forth.
   The `.asm` files are the authoritative source; bootstrap recompilation from F18e.f is
   possible but not essential and is no longer part of the regular workflow.

| | vForth18_DOES (master) | vForth18_DOT (twin) | F18e.f (historical) |
|---|---|---|---|
| Role | Master -- changes originate here | Near-identical; differs only in startup/closedown and MMU7 page allocation | Human-readable Forth form of the core -- reference only, not maintained in sync |
| VS Code project | `project/vForth18_DOES/` | `project/vForth18_DOT/` | -- |
| Launcher | `Forth18_loader.bas` + `forth18e.bin` + `ram8.bin` | ZX Spectrum Next dot-command (`.vforth`) | -- |
| Sync path (nextsync) | `tools/vForth/` | `dot/` | -- |
| Alignment cadence | -- | Immediate (on each core change) | Maintained by hand! |
| Bootstrap-verifiable | Yes | No | Possible but not required |

## Building and Testing (quick reference)

- **Assemble a variant**: `/build DOES` or `/build DOT` (SjASMPlus at
  `c:/Zx/sjasmplus/sjasmplus.exe`; full command line, the DOT two-part binary
  concatenation step and the deploy rules are in `.claude/commands/build.md`).
- **Headless emulator REPL**: `python emu/repl.py` boots the DOES binaries to the
  `ok` prompt; `printf '.quit\n' | python emu/repl.py` is the smoke test (the
  SPLASH banner must show the current build date). Docs in `emu/README.md`;
  Python regression scripts are `emu/test_*.py`. If bare `python` resolves to the
  WindowsApps stub, use the explicit `C:\Users\matteo\anaconda3\python.exe`.
- **Forth test suite**: runs inside vForth (emulator or CSpect) via
  `INCLUDE TEST/CORE-TESTS.f` etc. -- structure and `{...}T` notation in
  `test/CLAUDE.md`.

## Architecture

### Compilation Model: Direct Threading

vForth uses direct-threaded code (+25% speed vs indirect):
- Low-level definitions: CFA contains actual Z80 machine code (`jp (hl)` -> executes directly)
- High-level definitions: CFA contains `call Enter_Ptr` (3 bytes)

### Forth Virtual Machine vs Z80 Register Map

```
BC  -- Instruction Pointer (preserve during ROM/OS calls)
DE  -- Return Stack Pointer (preserve during ROM/OS calls)
HL  -- W register (working)
SP  -- Calculation Stack Pointer
IX  -- Inner interpreter "next" pointer (jp (ix) is 2T faster than jp addr)
IY  -- Reserved for ZX System interrupts
BC'/DE'/HL' -- more W's used in complex definition: it's customary using EXX to switch from Forth-Virtual-Machine scope to Machine-Code scope
```

### Memory Layout

- **BASIC RAMTOP** `$61FF` (at $6200 there is the IM-2 interrupt verctor table)
- **Origin**: `$6366` (binary/tape mode) or `$8080` (DeZog debug mode)
- **Heap Dictionary**: lives at `$E000-$FFFF` (MMU7 page); name-space and code-space split
- **S0/TIB/R0/USER**: below `$E000` (computed from `LIMIT_system = $E000`, 6 buffers of
  512 bytes each + 4 bytes each to keep track of BLOCK number and flags)
- **Blocks/Screens**: 2 Blocks forms a Screen 512 bytes each, blocks are persistently stored in `!Blocks.txt` on SD card

### Banks (16K) vs Pages (8K) -- BASIC vs vForth

Two different units name the same RAM, at two different levels. **Do not mix
them**: NextBASIC and vForth describe memory at different granularities.

- **BANK = 16K** -- the unit **NextBASIC** (and the NextZXOS allocator) works
  with. The 64K Z80 address space is four banks; `BANK n` and the OS allocate
  RAM 16K at a time. Hardware registers that count allocation units are
  bank-based too -- e.g. **NextReg `$12` (Layer 2 RAM bank)** is a 16K-bank
  number.
- **PAGE = 8K** -- the unit the **MMU** maps. The 64K space is eight 8K slots
  (`MMU0`..`MMU7`); one 16K bank = two consecutive 8K pages. Page-level paging
  is available only at the machine-code level -- and **vForth is assimilable to
  machine code**, so vForth thinks in 8K pages.

vForth dedicates the top slot, **MMU7 (`$E000-$FFFF`)**, to page in the rest of
RAM on demand: the heap dictionary, the Layer 2 framebuffers, etc. `MMU7!`
/ `MMU7@` take/return an **8K page** number, never a 16K bank.

**Writing rule:** say "16K bank" for BASIC/NextZXOS allocation and for NextReg
`$12`; say "8K page" for anything mapped through MMU7. A size may legitimately
be quoted as both (e.g. the 80K Layer 2 320x256 framebuffer = five 16K banks =
ten 8K MMU7 pages), but never write "16K bank via MMU7" -- the MMU pages 8K.

### Hardware sprites: two classic gotchas

Full details, attribute table and history in **`tutorial/CLAUDE.md` section 16**
(bugs found in tutorial 053, fixed and CSpect-verified 2026-07-05). In short:

- **Slot vs pattern.** Attribute 3 bits 5:0 are the **pattern** a sprite shows;
  the sprite **slot** is chosen only by the write to port `$303B`. Animation
  rewrites the *same* slot with alternating patterns -- using the pattern number
  as the slot lights up extra overlapping sprites.
- **Palette offset.** Attribute 2 bits 7:4 are added to the high nibble of every
  pixel's colour index. Garbage there (typically a sprite struct `ALLOT`ed but
  never `ERASE`d) shifts all hues -- e.g. pink `$F7` turns pale blue. Shifted
  colours mean palette *offset*, not a corrupted palette.

### Blocks, Screens, and reserved ranges

A **Screen** is the unit a programmer addresses with `n LOAD`; a **Block** is the half KB
unit vForth allocates internally in `!Blocks.txt`. Two consecutive Blocks form one 1KB Screen:

    Screen# N  =  BLOCK 2*N  and  BLOCK 2*N+1

**Reserved Screens:**

| Screen# | BLOCKs | Contents |
|---------|--------|----------|
| 0 | 0 | Unused |
| 0.5 | 1 | System metadata (copyright, block usage); **F_INCLUDE internal buffer** |
| 2-3 | 4-7 | Error messages #-32 to #-1 -- the negative area, aligned with the standard THROW codes (`-1` ABORT, `-2` ABORT", `-13` undefined word, ...); Screen 3 is pre-filled with `msg# -n` placeholders |
| 4-8 | 8-17 | Standard error messages #0-#79 -- read by `?ERROR` -> `ERROR` -> `MESSAGE` |
| 9 | 18-19 | `9 LOAD` -- prints the whole message list, page by page, then FORGETs itself |
| 10 | 20-21 | Previously held `include src/f18e.f`; now free for end-user use |

**Note on BLOCK 1 and F_INCLUDE:** The first 512 bytes of `!Blocks.txt` are BLOCK 1 and
contain system metadata and copyright information. Because it can never be modified by EDIT is used as
**temporary line buffer** for the `F_INCLUDE` primitive written in Forth 
(defined in `project/vForth18_DOES/source/L3.asm` line 224
or `src/F18e.asm` line 5521). 

During file inclusion, each source line is read from the open file into this BLOCK 1 buffer 
via `F_GETLINE`, providing a maximum line length of **~511 bytes**. The `BLK` variable is set 
to 1 to signal active include mode, and `INTERPRET` processes the line. This enables 
file-based source inclusion without allocating extra heap memory and reusing the old fashion
`LOAD` technique.

**Convention:** While BLOCK 1 permits lines up to 511 bytes, vForth source style maintains 
lines at **80 bytes or fewer** for readability and adherence to Forth conventions.

### Byte offsets inside `!Blocks-64.bin` (tools that read/write the file directly)

**BLOCK 0 is not stored.** The file begins with BLOCK 1, so the file offset of a block is
**`(block - 1) * 512`**, not `block * 512`. Everything else follows from it:

| Target | File offset |
|---|---|
| BLOCK `b` | `(b - 1) * 512` |
| Screen `S` (= blocks `2S`, `2S+1`) | `(2S - 1) * 512` |
| Screen `S`, line `L` (0-15, 64 bytes each) | `(2S - 1) * 512 + L * 64` |
| Error message `#n` (= Screen `4 + n/16`, line `n MOD 16`) | `(n + 32) * 64 + 3 * 512` |

Sanity checks: BLOCK 1 (metadata) is at 0; Screen 1 is at 512 -- which is exactly where
`util/blocks2txt.pl` seeks before it starts counting screens from 1; message `#0` is at
`0xE00`, the first line of Screen 4.

**The off-by-one is silent.** Using `block * 512` shifts everything by one block, i.e. by
eight lines within a screen, and the wrong text reads as perfectly plausible -- a wrong
message rather than garbage. When touching the binary, verify by reading back through the
real `BLOCK` mechanism (headless emulator) instead of trusting your own arithmetic, and
diff against a copy of the file to confirm only the intended byte ranges changed. Lines
are padded to 64 bytes with spaces (`BLANK`), and the file size must never change.

The error-message Screens (4-8) or Blocks (8-17) are a space-saving heritage from classic block-based Forth:
error text lives in the block file rather than being compiled inline into each definition.
`f n ?ERROR` checks `f`; if true it calls `n ERROR`, which calls `n MESSAGE` to display
the text from the appropriate block. Message #n is line n of Screen 4 counted straight
through, so Screen 5 starts at #16, Screen 6 at #32, Screen 7 at #48 and Screen 8 at #64 --
and the first line of each of those Screens is spent on a `( ... )` header comment.
To see the whole table on the machine, `9 LOAD`: an old auto-forgetting utility that
prints every message page by page and then `FORGET`s itself.

### Error reporting: `?ERROR` over `ABORT"` in the library

**In `inc/` and `lib/` -- the library that ships as the compendium of the vForth core --
report errors with numbered messages (`f n ?ERROR`), not with `ABORT"`.** Reasons, in
order of weight:

- `ERROR` prints the offending token (`HERE COUNT TYPE`) before the message, and when
  `BLK` is non-zero it leaves `>IN BLK` on the stack, which is exactly what `WHERE`
  (`inc/where.f`) consumes to show Screen#, row and a caret under the column. `ABORT"`
  prints its string and loses the position -- a bad trade for errors raised while
  compiling the user's source.
- `?ERROR` is a core word: no `NEEDS`. `ABORT"` pulls in `inc/abort".f` -> `S"` -> `H"`,
  i.e. the heap.
- Cost: `n ?ERROR` is a literal plus a call (~5 bytes) and no text; `ABORT"` compiles a
  branch, `(H")`, an `ha` cell, `TYPE` and `ABORT` (~12 bytes) **plus the string,
  permanently, in the scarce MMU7 heap it shares with the name-space**.
- The texts stay centralised, editable with `EDIT`, listable with `9 LOAD`, reusable
  across modules, and separated from the code.

Adding a message means editing the block file, so keep the numbers documented in a
comment at the top of the module (see `lib/locals.f`, which reserved #57-#60), and be
aware of the two costs: the number space is global, and a module distributed on its own
against an older `!Blocks-64.bin` will print the wrong line. Also remember `ERROR` ends
in `QUIT`, which resets `STATE` and the return stack but **not** `CONTEXT`/`CURRENT` --
`FORTH DEFINITIONS` is done by `ABORT`, not by `ERROR`. Code that temporarily switches
vocabulary must restore it by itself.

Where the mechanism degrades, `ABORT"` is legitimate even in the library: with
`WARNING` at 0 `MESSAGE` prints only `msg#n`, and with `WARNING` at -1 `ERROR` aborts
silently. **End-user application sources are free to use `ABORT"` throughout** -- it is
self-contained, needs no slot in a shared table, and its cost is paid by the application
that chose it.

### Dictionary Structure (New_Def macro)

Each word entry:
```
[Heap @ $E000+HP]  length|END_BIT, name bytes (last byte|END_BIT), link-ptr, xt-ptr
[Dict @ origin]    mirror-ptr, [runcode CALL if HLL], actual Z80 code
```

There is a one-to-one correspondence between `project/vForth18_DOES/list/main.lst` and the composite contribution of `forth18e.bin` (the main memory) and `ram8.bin` (the heap): These three files are the source of truth of the working core of this Forth system.

## Boot Sequence (COLD / WARM / BLK-INIT / ABORT / AUTOEXEC)

Understanding the startup chain is essential for the emulator and for debugging a
cold start. The flow, with the `vForth18_DOES` code addresses (from `list/main.lst`):

```
entry $6366  -> ColdRoutine self-init -> COLD
COLD  $7616  -> init block buffers (EMPTY-BUFFERS, NMODE, FIRST/PREV/USE...) -> falls into WARM
WARM  $760D  -> BLK-INIT  then  ABORT
BLK-INIT $78D2 -> close any open block handle (BLK-FH), then F_OPEN the block file
ABORT $75EA  -> init data/return stacks (S0/SP!, R0/RP!), then call AUTOEXEC (first time only)
AUTOEXEC $8003 -> 11 LOAD  (Screen 11, user-configurable)
SPLASH $7FDF -> banner (called by the default Screen 11 / lib/autoexec.f)
```

Key points:

1. **BLK-INIT** opens the persistent block file `!Blocks-64.bin` (16 MB; name string in
   `BLK-FNAME` at $785F) via `F_OPEN`. If the open **fails**, vForth still returns to the
   `Ok` prompt but is left in an **inconsistent state** -- the boot must be allowed to
   continue to `ABORT` regardless.

2. **ABORT** is the word after BLK-INIT inside WARM. It (re)initialises both stacks and
   then invokes **AUTOEXEC** -- but only on the **first** execution: AUTOEXEC rewrites its
   own call site inside ABORT to a `NOOP` at run time, so every subsequent COLD/WARM/ABORT
   skips AUTOEXEC. (In the listing the slot is `dw AUTOEXEC // autoexec, patched to noop`.)

3. **AUTOEXEC** performs `11 LOAD` -- Screen 11 is user-configurable. By default Screen 11
   runs `INCLUDE lib/autoexec.f`, and that script normally calls **SPLASH** to print the
   banner (and may load utilities via `NEEDS`).

4. After AUTOEXEC (or once it is patched out), control reaches the `QUIT` loop ->
   `QUERY` / `ACCEPT` -> the interactive REPL prompt (`ok`).

**Emulator status (2026-06-05):** the headless emulator boots the full chain
COLD->WARM->BLK-INIT->ABORT->AUTOEXEC->`11 LOAD`->`INCLUDE lib/autoexec.f`->`SPLASH`
and **prints the complete banner** (version, CPU speed, dictionary/heap free, free space),
reaching `ASK-Y/N` and the utility-loading path. Three fixes were required, all in the
NextZXOS/ROM interface the headless build cannot run natively:

1. **`F_FGETPOS` (and all file syscalls) must return status in the CARRY flag**
   (`Fc=0` ok / `Fc=1` error) -- the Forth wrappers reveal it with `sbc hl,hl`.
   The handlers only set `HL`; `handle_nextzxos_call` now also translates HL->carry.
   This fixed the "F_GETLINE pos error" that aborted the autoexec include.
2. **`(CLS)` queries the active screen layer via `rst $08/$94`**; `handle_cls` now
   returns a non-zero (non-layer-0) status so (CLS) takes the portable `rst $10`
   emit-`$0E` path instead of calling ROM `$0DAF`.
3. **ROM-routine stubs**: the core `call`s real ZX ROM routines (`$1601` CHAN-OPEN via
   `SELECT`, `$0DAF` CL-ALL). These are stubbed with a `RET` (`install_rom_stubs`) so
   the CALL returns cleanly instead of derailing the PC into low memory.

A fourth fix made the **interactive REPL fully work** (boot -> banner -> `ASK-Y/N` ->
`ok` prompt -> evaluate input -> print results):

4. **Keyboard input is delivered on HALT, not on a fixed instruction interval.**
   The vForth key-wait loops (`CURS` / `ONE-FRAME`) `ei halt` each frame until a key
   appears, mirroring the 50Hz keyboard ISR. Delivering a queued key on any HALT (see
   `dispatch`) -- instead of every N instructions -- stops keys being consumed early
   during banner printing. Before this, `ASK-Y/N` read a stale CR and always took the
   "load utilities" branch; now `n` correctly makes it `QUIT` to the prompt, and
   `1 2 + .` prints `3`.

A fifth fix (2026-06-12) made the **MMU7 paging real**: `Z80CPU.mmu7_page` is now a
property that swaps the $E000-$FFFF window content per 8K page, and the NextReg
read-back ports $243B/$253B are modelled (`_bc_port_in`/`_bc_port_out` in
`z80_instructions.py` -- note `_register_ed_standard()` re-registers ED 78/79, so the
model lives in the generic `_make_in_r_c`/`_make_out_c_r`). This fixed the previously
fragile area (definitions inside INCLUDEd files derailing `(FIND)`) and was required by
the `(EMITC)` MMU7 save/restore fix, which reads the current page on every emitted
character. `emu/test_words_stream.py` covers the `13 SELECT WORDS` scenario by
simulating the +3DOS banking clobber after every `rst $10`.

The `emu/trace_words.py` tool traces Forth words (gated on entering a chosen word,
default AUTOEXEC) and spies on `KEY` (LASTK/FLAGS/queue) -- built to diagnose the above.

Remaining: utility loading via `NEEDS` (REMOUNT/WHERE/.S/EDIT/...) is heavy -- the next
area to validate.

## Directory Structure

> **General development principle -- root directories are canonical.**
> All source work happens in the root-level directories (`inc/`, `lib/`, `src/`, `test/`,
> `demo/`, ...). The repo root (`C:\Zx\Forth\F18`) is the **nextsync root**: it mirrors
> directly to the ZX Spectrum Next SD card filesystem via the nextsync WiFi utility.

```
src/          -- Forth source (F18e.f current; F15-F17 historical)
project/
  vForth18_DOES/  -- Classic variant (v1.8): launcher-based, bootstrap-verifiable
    source/     -- L0.asm, L1.asm, L2.asm, L3.asm, system.asm, main.asm
    output/     -- forth18e.bin, ram8.bin
    list/       -- Debug listings (.lst, .sld.txt)
  vForth18_DOT/   -- Dot-command variant (v1.8): parallel to vForth18_DOES
    source/     -- same structure as vForth18_DOES
    output/     -- dot-command binary
  DIRECT/       -- Historical v1.5
  DIRECT_RP/    -- Variant
  INDIRECT/     -- Indirect-threaded (legacy)
dot/          -- Dot-command binaries at repo root (vforth, term0)
emu/          -- Headless Z80/Z80N + vForth emulator in Python (see emu/README.md)
lib/          -- Library modules loaded via NEEDS (GRAPHICS.f, MOUSE.f, AY.f, ...)
inc/          -- Single-word definitions loaded via NEEDS (256+ files)
  doc/        -- Reference-only copies of core words (never loaded by NEEDS)
help/         -- Plain-text help files for the HELP command (one .txt per word)
test/         -- Test suite (CORE-TESTS.f, FLOATING-TESTS.f, ...)
demo/         -- Example programs and games
tutorial/     -- Guided tutorials
doc/          -- PDF reference manual
util/         -- Perl scripts (blocks2txt.pl, putscr.pl)
version/      -- Historical build snapshots (never modify, see build number convention)
prompts/      -- Plans, analyses, and design docs produced while discussing
```

> **Plans go in `prompts/`, never the project root.** Any plan, analysis, or
> design document we produce by discussing (e.g. `LAYER24-PLAN.md`,
> `PAINT-PLAN.md`) must be saved under `prompts/`, not at the repo root, which
> is to be kept clean. Write new plans there by default.

## Character Encoding

All source files (`.f`, `.txt`, `.asm`) and all generated help files must use **7-bit
ASCII only** -- no UTF-8, no BOM, no extended characters.

The only exception is `0x7F`, which on the ZX Spectrum represents the **copyright
symbol** and may appear in Forth source that targets the machine's display directly.

**Practical rules:**
- Always write files with **no BOM**. Use `[System.IO.File]::WriteAllBytes()` or
  `-Encoding ascii` with explicit BOM removal.
- Do not use any character outside the range `0x20-0x7E` plus `0x0A` (LF), `0x0D`
  (CR), and `0x7F` (copyright). **TAB (`0x09`) is forbidden**: it disrupts the Forth
  tokeniser and must be replaced with spaces.
- When generating help `.txt` files: plain ASCII, no BOM, no smart quotes, no em-dashes.

**EMIT vs EMITC:**
- `EMIT ( c -- )` may mask to 7-bit ASCII range (0-127).
- `EMITC ( c -- )` emits the full character code (0-255) without masking -- use for UDG or   codes and extended ZX Spectrum characters (128-255). Control characters (0-31) that target the real hardware have each a peculiar meaning.


## FAT Filename Character Mapping

Because Forth names use characters illegal in FAT filenames, NEEDS and INCLUDE maps them automatically.
When working with word names (help files, NEEDS lines, documentation), always use the
**real Forth name** -- never the FAT-mapped filename form.

| Forth char | Filename char |
|---|---|
| `:` | `_` |
| `?` | `^` |
| `/` | `%` |
| `*` | `&` |
| `\|` | `$` |
| `<` | `{` |
| `>` | `}` |
| `"` | `~` |

## NEEDS mechanism

`NEEDS` is compiled into `forth18e.bin` -- available immediately at startup.

```forth
NEEDS VALUE     \ loads inc/value.f only if VALUE is not yet in the dictionary
NEEDS GRAPHICS  \ loads lib/GRAPHICS.f only if GRAPHICS is not yet in the dictionary
```

**Search order:** `inc/` first, then `lib/`. If the word is already in the dictionary,
the file load is skipped. If neither file exists (or exists but does not define the word),
`NEEDS` emits the word name followed by message 43 ("File not found").

`NEEDS` is interpreter-only -- there is no point to call it inside a colon-definition.

## Breaking Changes Since v1.2

- `'` (tick) returns CFA, not PFA
- `-FIND` returns CFA, not PFA
- `SP!` / `RP!` require the target address
- `WORD` returns HERE address
- `CREATE` returns PFA
- `VARIABLE` now has standard behavior (since v1.52): when executed it pushes its own
  address (PFA). Old code using non-standard VARIABLE behavior must be verified.
- `DOES>` follows latest Forth standard (v1.8+)

## DOES> and PFA: stack convention

At runtime, the code following DOES> receives PFA (the Parameter Field Address of the
product word) as the top of stack item. Any arguments that the caller pushed before
invoking the product word are beneath PFA on the Forth stack.

On the Z80, the hardware stack grows downward in memory, so "top of stack" is the cell
at the lowest current stack address -- the most recently pushed item. DOES> pushes PFA
last, making it TOS at the moment the DOES> body begins executing.

The PFA holds all compile-time data stored by `,` `C,` or `ALLOT` during the CREATE
phase. The DOES> body uses PFA to access that data; caller arguments sit below TOS and
are accessed via stack manipulation.

Canonical example from `inc/2constant.f`:
```forth
: 2CONSTANT  ( d -- )
    CREATE , ,
    DOES>   ( pfa -- d )
        2@ ;
\ CREATE stores hi then lo cell at PFA.
\ DOES> pushes PFA as TOS; 2@ fetches both cells from PFA.
```

## CHAR vs [CHAR]: interpret-state vs compile-state

Same pairing as `'` (tick) vs `[']` (bracket-tick): one word for interpreted code,
one compile-only immediate word for use inside a colon-definition body.

- **`CHAR`** -- interpretive: parses the next word and pushes its first character
  code immediately. Use at the interpreter level -- outside any colon-definition,
  e.g. initializing a `VARIABLE` right after creating it.
- **`[CHAR]`** -- compile-only immediate: parses the next word at compile time and
  compiles code that pushes the character literal when the enclosing definition
  later runs. Use only inside a colon-definition body.

Using `[CHAR]` where plain `CHAR` belongs (top-level/interpreted code) is a mistake
even if it happens to not visibly misbehave in a quick check -- e.g. `lib/DIR.f` had
`VARIABLE DIR-DRIVE  [CHAR] C DIR-DRIVE C!` (top-level, interpreted) where it should
have been `CHAR C DIR-DRIVE C!`. (Historical example: `DIR-DRIVE` no longer exists --
`DIR` now leaves the drive to the NextZXOS default `'*'`, so the drive letter is
simply written in the path when needed. The `CHAR`/`[CHAR]` rule is unaffected.)

## Known Bugs

### `INCLUDE` / `NEEDS`

Crashes (usually a vertical grid on screen) if the loaded file ends with a space
immediately before its final newline. `NEEDS` inherits the bug -- it uses `INCLUDE`.

**Rule (byte-exact):** the file's last byte must be `0x0A` and the second-to-last
byte must not be `0x20`. Trailing `0x0A`s are fine (the file may end with several
blank lines); trailing spaces on *interior* lines are harmless. Only the final two
bytes matter.

**Editing note (trailing spaces):** there is **no need to strip trailing spaces**
from source files -- only the final two bytes are constrained by the rule above.
The guiding principle is the **minimal diff between commits**: do not produce changes
that flag a difference just for a space or two that "wobble". Concretely: never do
repo-wide trailing-whitespace cleanups, and when editing a line do not gratuitously
drop its trailing space. Conversely, removing an innocuous trailing space *is fine*
when the line is already being changed for a real reason and it keeps the surrounding
hunk consistent -- it is context-dependent, not a hard rule. Judge by diff noise.

### `LOAD` (block/screen interpreter)

- **Structure spanning BLOCK boundaries.** Long structured definitions (e.g. `ENUMERATED`)
  cannot straddle the boundary between the first and second half KB block of the same Screen.
  The definition must fit entirely within one Block.
- **NUL character (`0x00`) in a screen.** A NUL byte inside a screen silently stops
  interpretation mid-load with no error message. Use `EDIT` to locate it.

### `OPEN<`

Can only be used in interpretation mode. Calling it inside a colon-definition is not
supported and will produce incorrect behaviour.

### `LED`

Pressing `[BREAK]` stops any active I/O operation immediately. If `LED` is driving an
I/O sequence at the time, this may produce data loss.

### `LAYER24` (lib/LAYER24-GRAPHICS.f) -- unverified on real hardware

The Layer 2 640x256 4bpp mode works in the headless emulator but shows an
unexpected behaviour on CSpect: the image is shifted 256 px to the right
(NextReg $70=$20, clip X 0..159). The library addresses pages and coordinates
correctly, and LAYER22 works on the same emulator, so this is suspected to be
a CSpect emulation artifact -- but it has NOT yet been verified on real
hardware. Until then, treat LAYER24 as experimental. Details and 2026-06-28
findings in `prompts/LAYER24-PLAN.md`.

