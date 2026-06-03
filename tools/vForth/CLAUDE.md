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

**Current version**: 1.8 (build 2026-05-31)  
**License**: MIT  
**Author**: Matteo Vitturi

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
| Alignment cadence | -- | Immediate (on each core change) | Not maintained -- historical snapshot |
| Bootstrap-verifiable | Yes | No | Possible but not required |

## Architecture

### Compilation Model: Direct Threading

vForth uses direct-threaded code (+25% speed vs indirect):
- Low-level definitions: CFA contains actual Z80 machine code (`jp (hl)` -> executes directly)
- High-level definitions: CFA contains `call Enter_Ptr` (3 bytes)

### Z80 Register Map

```
BC  -- Instruction Pointer (preserve during ROM/OS calls)
DE  -- Return Stack Pointer (preserve during ROM/OS calls)
HL  -- W register (working; high word for 32-bit ops)
SP  -- Calculation Stack Pointer
IX  -- Inner interpreter "next" pointer (jp (ix) is 2T faster than jp addr)
IY  -- Reserved for ZX System interrupts
AF'/BC'/DE'/HL' -- Backup/temporary
```

### Memory Layout

- **Origin**: `$6366` (binary/tape mode) or `$8080` (DeZog debug mode)
- **Heap Dictionary**: lives at `$E000-$FFFF` (MMU7 page); name-space and code-space split
- **S0/TIB/R0/USER**: below `$E000` (computed from `LIMIT_system = $E000`, 6 buffers of
  516 bytes each)
- **Blocks/Screens**: 1 KB each, stored in `!Blocks.txt` on SD card

### Blocks, Screens, and reserved ranges

A **Screen** is the unit a programmer addresses with `n LOAD`; a **Block** is the 1 KB
unit vForth allocates internally in `!Blocks.txt`. Two consecutive Blocks form one Screen:

    Screen# N  =  BLOCK 2*N  and  BLOCK 2*N+1

**Reserved Screens:**

| Screen# | BLOCKs | Contents |
|---------|--------|----------|
| 0 | 0-1 | Unused -- loading Screen# 0 crashes the system (see Known Bugs) |
| 4-7 | 8-15 | Standard error messages -- read by `?ERROR` -> `ERROR` -> `MESSAGE` |
| 10 | 20-21 | Previously held `include src/f18e.f`; now free for end-user use |

The error-message Screens (4-7) are a space-saving heritage from classic block-based Forth:
error text lives in the block file rather than being compiled inline into each definition.
`f n ?ERROR` checks `f`; if true it calls `ERROR n`, which calls `MESSAGE n` to display
the text from the appropriate block.

### Dictionary Structure (New_Def macro)

Each word entry:
```
[Heap @ $E000+HP]  length|END_BIT, name bytes (last byte|END_BIT), link-ptr, xt-ptr
[Dict @ origin]    mirror-ptr, [runcode CALL if HLL], actual Z80 code
```

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
lib/          -- Library modules loaded via NEEDS (GRAPHICS.f, MOUSE.f, AY.f, ...)
inc/          -- Single-word definitions loaded via NEEDS (256+ files)
  doc/        -- Reference-only copies of core words (never loaded by NEEDS)
help/         -- Plain-text help files for the HELP command (one .txt per word)
test/         -- Test suite (CORE-TESTS.f, FLOATING-TESTS.f, ...)
demo/         -- Example programs and games
tutorial/     -- Guided tutorials
doc/          -- PDF reference manual
util/         -- Perl scripts (blocks2txt.pl, putscr.pl)
```

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
- `EMITC ( c -- )` emits the full character code (0-255) without masking -- use for UDG
  codes and extended ZX Spectrum characters (128-255).

## FAT Filename Character Mapping

Because Forth names use characters illegal in FAT filenames, NEEDS maps them automatically.
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

`NEEDS` is interpreter-only -- never call it inside a colon-definition.

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
phase. The DOES> body uses PFA to access that data; caller arguments sit below PFA and
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

## Known Bugs

### `INCLUDE` / `NEEDS`

The system crashes -- typically displaying a vertical grid pattern on screen -- if the
last line of the loaded file ends with one or more trailing spaces before the newline.
The crash occurs regardless of what non-space content precedes the trailing spaces.
`NEEDS` is affected by the same bug because it uses `INCLUDE` internally.

**Workaround:** ensure the last line of every `.f` file has no trailing spaces.

### `LOAD` (block/screen interpreter)

- **Structure spanning BLOCK boundaries.** Long structured definitions (e.g. `ENUMERATED`)
  cannot straddle the boundary between the first and second 1 KB block of the same screen.
  The definition must fit entirely within one block.
- **NUL character (`0x00`) in a screen.** A NUL byte inside a screen silently stops
  interpretation mid-load with no error message. Use `EDIT` to locate it.
- **Screen #0.** Loading from Screen #0 (`0 LOAD`) crashes the system.

### `OPEN<`

Can only be used in interpretation mode. Calling it inside a colon-definition is not
supported and will produce incorrect behaviour.

### `LED`

Pressing `[BREAK]` stops any active I/O operation immediately. If `LED` is driving an
I/O sequence at the time, this may produce data loss.

