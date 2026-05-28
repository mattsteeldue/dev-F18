# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**vForth Next** is a Forth compiler and runtime system for the Sinclair ZX Spectrum Next computer. It includes a complete Forth compiler (self-bootstrapping), Z80/Z80N assembly support, and multiple library modules for graphics, sound, file I/O, and hardware control.

**Current version**: 1.8 (build 2026-04-19)  
**License**: MIT  
**Author**: Matteo Vitturi

## The Three Codebases and Their Roles

The project has three codebases in order of priority:

1. **vForth18_DOES** — the master. All changes originate here.
2. **vForth18_DOT** — near-identical twin. The vast majority of source is shared with vForth18_DOES; only startup/closedown routines and MMU7 8K page allocation differ. Kept in sync with the master; alignment is straightforward.
3. **F18e.f** — a historical artifact. Its primary value is **readability**: a Forth programmer can study it to understand how the core is implemented, in idiomatic Forth. The `.asm` files are the authoritative source; bootstrap recompilation from F18e.f is possible but not essential and is no longer part of the regular workflow.

| | vForth18_DOES (master) | vForth18_DOT (twin) | F18e.f (historical) |
|---|---|---|---|
| Role | Master — changes originate here | Near-identical; differs only in startup/closedown and MMU7 page allocation | Human-readable Forth form of the core — reference only, not maintained in sync |
| VS Code project | `project/vForth18_DOES/` | `project/vForth18_DOT/` | — |
| Launcher | `Forth18_loader.bas` + `forth18e.bin` + `ram8.bin` | ZX Spectrum Next dot-command (`.vforth`) | — |
| Sync path (nextsync) | `tools/vForth/` | `dot/` | — |
| Alignment cadence | — | Immediate (on each core change) | Not maintained — historical snapshot |
| Bootstrap-verifiable | Yes | No | Possible but not required |

## Primary Development Workflow

The project master has **moved to Visual Studio Code** with a Z80N assembler (SjASMPlus). Self-hosted compilation on the ZX Spectrum Next / CSpect emulator is too slow for daily development.

**The representations that must stay byte-identical (for the classic variant):**

1. `src/F18e.f` — the Forth source that compiles itself on the ZX Spectrum Next (slow, authoritative Forth representation)
2. `project/vForth18_DOES/source/*.asm` — the same compiler in Z80N assembly for SjASMPlus (fast, primary development target)

Both produce the same `forth18e.bin`. When the `.asm` files are modified, `F18e.f` must be updated to match — and vice versa. The vForth18_DOT variant has no equivalent F18e.f alignment path.

### Building with VS Code (primary)

**Classic variant** — `project/vForth18_DOES/`:
```
main.asm → system.asm, L0.asm, L1.asm, L2.asm, next-opt1.asm, L3.asm
```
Outputs: `output/forth18e.bin`, `output/ram8.bin`

**Dot variant** — `project/vForth18_DOT/`:
```
main.asm → system.asm, L0.asm, L1.asm, L2.asm, next-opt1.asm, L3.asm
```
Output: a dot-command binary deployed to `dot/`

### Building self-hosted (deprecated — not used anymore)

Screen #10 is now free for end-user use. To use the old self-hosted method, Screen #10 must first contain the line:

    include src/f18e.f

Then, within CSpect or on real hardware, execute 10 LOAD to trigger compilation. The system compiles itself twice (first to upper memory, then back to origin). The resulting binary can be transferred to a PC and verified byte-by-byte against the SjASMPlus output using a binary diff tool (e.g. AraxisMerge). This applies only to the classic (vForth18_DOES) variant.

### Verifying alignment between .asm and F18e.f

Set `DEBUGGING equ -1` in `main.asm` for binary comparison mode (origin is adjusted to match the Forth-compiled output for byte-by-byte diff). Applies to vForth18_DOES only.

### Forth-based development (inc/, lib/, demo/, tutorial/)

vForth is an extremely open system. The core (`forth18e.bin`) is now stable and changes rarely; SjASMPlus is its mainline. Everything else — `inc/`, `lib/`, `demo/`, and any future `tutorial/` content — is written in Forth and developed using Forth itself. This is the natural, incremental methodology of the language.

Two equally valid workflows exist for Forth code:

**On the machine (real or emulated).** Edit source files directly using the built-in `EDIT` word, then `INCLUDE` or `NEEDS` the file to load and test interactively. This is the classic Forth inner loop: define a word, test it at the prompt, refine, repeat.

**From a PC with a preferred editor.** Write `.f` files on the laptop, then transfer them to the corresponding directory on the ZX Spectrum Next SD card using the **sync** utility (author: Jari Komppa, aka SoL_HSA). Once synced, load the file on the machine with `INCLUDE filename.f` or `NEEDS WORDNAME`.

Both workflows converge at the same point: the canonical source lives in the root `inc/` and `lib/` directories of this repository. Since the repo root is the nextsync root, files are ready to deploy immediately after editing (see *Deployment to ZX Spectrum Next* below).

## Architecture

### Compilation Model: Direct Threading

vForth uses direct-threaded code (+25% speed vs indirect):
- Low-level definitions: CFA contains actual Z80 machine code (`jp (hl)` → executes directly)
- High-level definitions: CFA contains `call Enter_Ptr` (3 bytes)

### Z80 Register Map

```
BC  — Instruction Pointer (preserve during ROM/OS calls)
DE  — Return Stack Pointer (preserve during ROM/OS calls)
HL  — W register (working; high word for 32-bit ops)
SP  — Calculation Stack Pointer
IX  — Inner interpreter "next" pointer (jp (ix) is 2T faster than jp addr)
IY  — Reserved for ZX System interrupts
AF'/BC'/DE'/HL' — Backup/temporary
```

### Memory Layout

- **Origin**: `$6366` (binary/tape mode) or `$8080` (DeZog debug mode)
- **Heap Dictionary**: lives at `$E000–$FFFF` (MMU7 page); name-space and code-space split
- **S0/TIB/R0/USER**: below `$E000` (computed from `LIMIT_system = $E000`, 6 buffers of 516 bytes each)
- **Blocks/Screens**: 1 KB each, stored in `!Blocks.txt` on SD card

### Dictionary Structure (New_Def macro)

Each word entry:
```
[Heap @ $E000+HP]  length|END_BIT, name bytes (last byte|END_BIT), link-ptr, xt-ptr
[Dict @ origin]    mirror-ptr, [runcode CALL if HLL], actual Z80 code
```

## F18e.f ↔ .asm Mnemonic Correspondence

The ASSEMBLER vocabulary in F18e.f is postfix/stack-based: each element (instruction word, register specifier, operand commaer) is a **separate Forth word**. The full reference is `src/Z80N-Assembler-Dictionary.txt`. Register notation:

- r|  — source register: B| C| D| E| H| L| A| (HL)|
- r'| — destination register: B'| C'| D'| E'| H'| L'| A'| (HL)'|  (NOT the alternate register set — just destination syntax), think the single-quote as a raised comma
- rr| — register pair: BC| DE| HL| SP|  also IX| IY| AF|
- f|  — flag for JP/CALL/RET: NZ| Z| NC| CY| PO| PE| P| M|
- f'| — flag for JR: NZ'| Z'| NC'| CY'|
- b|  — bit position: 0| … 7|
- n N,  nn NN,  aa AA,  d D,  nn LH, — operand "commaers" (push value, emit bytes)

| F18e.f (ASSEMBLER vocab) | Z80N (SjASMPlus) | Notes |
|---|---|---|
| CODE name … C; | New_Def LABEL, "name", is_code, is_normal + code | low-level word |
| Next | next macro → jp (ix) | inner interpreter |
| JPHL | jp (hl) | execute xt |
| LDA(X) rr\| | ld a, (rr) | e.g. LDA(X) BC\| |
| LD(X)A rr\| | ld (rr), a | |
| LD r'\| r\| | ld r, r | three separate words; r'\| = dest, r\| = source |
| LDN r'\| n N, | ld r, n | |
| INCX rr\| | inc rr | e.g. INCX BC\| |
| DECX rr\| | dec rr | |
| INC r'\| | inc r | |
| DEC r'\| | dec r | |
| PUSH rr\| | push rr | |
| POP rr\| | pop rr | |
| EXX | exx | swap register banks |
| EXDEHL | ex de, hl | |
| ADDHL rr\| | add hl, rr | |
| ADCA r\| | adc a, r | |
| ADCN n N, | adc a, n | |
| ADCHL rr\| | adc hl, rr | |
| ADDA r\| | add a, r | |
| SUBA r\| | sub r | r\| includes (HL)\| |
| SBCA r\| | sbc a, r | r\| includes (HL)\| |
| SBCHL rr\| | sbc hl, rr | |
| ANDA r\| | and r | e.g. ANDA A\| clears carry |
| ORA r\| | or r | |
| XORA r\| | xor r | |
| CPA r\| | cp r | |
| BIT b\| r\| | bit b, r | e.g. BIT 7\| B\| |
| SET b\| r\| | set b, r | |
| RES b\| r\| | res b, r | |
| CCF | ccf | |
| SCF | scf | |
| RET | ret | |
| RETF f\| | ret f | conditional return |
| JPIX | jp (ix) | |
| JP aa AA, | jp aa | |
| JPF f\| aa AA, | jp f, aa | conditional jump |
| JR d D, | jr d | relative jump |
| JRF f'\| d D, | jr f, d | |
| JRF f'\| HOLDPLACE … HERE DISP, | jr f, label | forward jump pattern in F18e.f |
| CALL aa AA, | call aa | |
| CALLF f\| aa AA, | call f, aa | |
| PUSHN nn LH, | push nn | via ld hl,nn / push hl |
| DJNZ d D, | djnz d | |

Forward pointers in F18e.f (e.g. HERE TO next^, HERE TO loop^) mark addresses that are then referenced by labels in the .asm (e.g. Next_Ptr:, Loop_Ptr:).

## Directory Structure

> **General development principle — root directories are canonical.**
> All source work happens in the root-level directories (`inc/`, `lib/`, `src/`, `test/`, `demo/`, …).
> The repo root (`C:\Zx\Forth\F18`) is the **nextsync root**: it mirrors directly to the ZX Spectrum Next
> SD card filesystem via the nextsync WiFi utility. There is no separate SD/ staging directory —
> `tools/vForth/inc/` and `tools/vForth/lib/` are simultaneously the canonical source and the
> deployment copy.

```
src/          — Forth source (F18e.f current; F15–F17 historical)
project/
  vForth18_DOES/  — Classic variant (v1.8): launcher-based, bootstrap-verifiable
    source/     — L0.asm, L1.asm, L2.asm, L3.asm, system.asm, main.asm
    output/     — forth18e.bin, ram8.bin
    list/       — Debug listings (.lst, .sld.txt)
  vForth18_DOT/     — Dot-command variant (v1.8): parallel to vForth18_DOES, not bootstrap-verifiable
    source/     — same structure as vForth18_DOES
    output/     — dot-command binary
  DIRECT/       — Historical v1.5
  DIRECT_RP/    — Variant
  INDIRECT/     — Indirect-threaded (legacy)
dot/          — Dot-command binaries at repo root (vforth, term0)
lib/          — Library modules loaded via NEEDS (GRAPHICS.f, MOUSE.f, AY.f, …)
inc/          — Single-word definitions loaded via NEEDS (256+ files)
  doc/        — Reference-only copies of core words (never loaded by NEEDS; for human reading)
test/         — Test suite (CORE-TESTS.f, FLOATING-TESTS.f, …)
demo/         — Example programs and games
tutorial/     — Guided tutorials (see conventions below)
doc/          — PDF reference manual
util/         — Perl scripts (blocks2txt.pl, putscr.pl)
```

## Character Encoding

All source files (`.f`, `.txt`, `.asm`) and all generated help files must use **7-bit ASCII only** — no UTF-8, no BOM, no extended characters.

The ZX Spectrum Next is a retro machine: it does not support Unicode or multi-byte encodings. The only exception to pure 7-bit ASCII is the character at code point **`0x7F`**, which on the ZX Spectrum represents the **© copyright symbol** and may appear in Forth source that targets the machine's display directly.

**Practical rules when generating or editing files:**
- Always write files with **no BOM** (no `EF BB BF` prefix). PowerShell's default UTF-16 and UTF-8-with-BOM encodings are both wrong — use `[System.IO.File]::WriteAllBytes()` or `-Encoding ascii` / `-Encoding utf8` with explicit BOM removal.
- Do not use any character outside the range `0x20–0x7E` plus `0x09` (tab), `0x0A` (LF), `0x0D` (CR), and `0x7F` (©).
- When generating help `.txt` files: plain ASCII, no BOM, no smart quotes, no em-dashes.

## FAT Filename Character Mapping

Because Forth names use characters illegal in FAT filenames, NEEDS maps them automatically.

> **Vintage Forth perspective.** The FAT character restriction covers many characters,
> but the set actually used in Forth word names is small and well-known: `?`, `>`, `<`,
> `/`, `*`, `"` are the only special chars that appear with any frequency.
> Characters like `!`, `@`, `+`, `-`, `.`, `#` are already legal in FAT filenames.
> When working with word names (help files, NEEDS lines, documentation), always use the
> **real Forth name** with its original characters — never the FAT-mapped filename form.

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

## Library System (inc/ and lib/)

### Overview

The core (`forth18e.bin`) provides only the fundamental vocabulary. The bulk of vForth's definitions live in two complementary directories, loaded on demand at runtime:

- **`inc/`** (256+ files) — atomic, single-word definitions. Each file defines exactly one Forth word.
- **`lib/`** (~50 modules) — multi-word feature modules grouped by domain (GRAPHICS, AY, MOUSE, floating-point, …).

Neither directory has a `.asm` counterpart — these are pure Forth source files. No binary alignment requirement applies.

### NEEDS mechanism

`NEEDS` is part of the **core dictionary** — it is compiled into `forth18e.bin` (defined in `project/vForth18_DOES/source/L3.asm`). It is available immediately at startup without loading any file.

`lib/needs.f` exists in the repository but is a **documentary duplicate**: it contains the equivalent Forth-level implementation for reference and historical continuity. It is not loaded at runtime and must not be used as a substitute for the core word.

```forth
NEEDS VALUE     \ loads inc/value.f only if VALUE is not yet in the dictionary
NEEDS GRAPHICS  \ loads lib/GRAPHICS.f only if GRAPHICS is not yet in the dictionary
```

**Search order and priority.** `NEEDS NAME` always searches `inc/` first, then `lib/`. Each search step begins by checking whether `NAME` is already in the dictionary (`LFIND`); if it is, the step is skipped entirely. Consequently, if `NAME.f` (with FAT mapping applied) exists in both directories, the `inc/` copy takes effect and the `lib/` copy is never loaded.

**Exact error semantics.** The internal word `NEEDS/` that opens and executes the file is silent: if the file is not found on the filesystem, the error is discarded (`DROP`) with no message. The outer `NEEDS` performs a final `LFIND` *after* both `inc/` and `lib/` have been attempted. Only at that point, if `NAME` is still absent from the dictionary, does `NEEDS` emit the word name followed by message 43 ("File not found"). This means:

- If neither `inc/NAME.f` nor `lib/NAME.f` exists on the SD card → error.
- If the file exists and is loaded but does not actually define `NAME` → error.
- If the file exists, is loaded, and `NAME` is defined → success, no message.

### inc/ file conventions

One word per file. The filename is the FAT-mapped word name with `.f` extension.

Typical structure:
```forth
\
\ word-name.f
\
.( WORD-NAME )
\
NEEDS dependency1    \ only if needed

: WORD-NAME  ( stack-effect )
    ...
;
```

### CODE words in inc/ — development vs. release form

Low-level `CODE` definitions in `inc/` files can be written using the ASSEMBLER vocabulary during development for readability. At release, convert the mnemonics to raw hex literals using `C,` — this avoids loading the ASSEMBLER vocabulary (~7 KB) entirely, which matters when RAM is premium.

**Typical workflow.** New low-level words are first developed interactively on real or emulated hardware (CSpect), using the ASSEMBLER vocabulary (`NEEDS ASSEMBLER`) for readable, mnemonic-driven iteration. The ASSEMBLER vocabulary is a vForth `VOCABULARY` — it is only available on the ZX Spectrum Next / CSpect; it plays no role in SjASMPlus development.

Once a word is finalised, its `inc/` file is written using `$`-prefixed hex literals and `C,` — no ASSEMBLER dependency, ~7 KB saved at runtime:

```forth
\ wait for next interrupt, to sync video frame
CODE SYNC-VID
    $76 C,             \ halt
    $DD C, $E9 C,      \ jp (ix)
    SMUDGE
    \
```

Use `$`, `%`, `#` prefix characters for numeric literals rather than switching
BASE globally.  Rationale: changing BASE during compilation (e.g. `HEX` inside a
source file) is error-prone — a forgotten `DECIMAL` will silently misparse every
subsequent literal until the next reload.  Changing BASE for *output* (e.g.
`255 HEX . DECIMAL`) is perfectly normal and accepted practice.

Summary:
- **Preferred** — prefix characters in source: `$FF`, `%11111111`, `#255`
- **Tolerated** — global base switch for output formatting: `HEX . DECIMAL`
- **Discouraged** — global base switch during compilation or source loading

Forth code in uppercase; Z80 opcode comments in lowercase for reading fluency.

### lib/ module conventions

Each module covers a coherent feature or hardware subsystem. Conventions:

- **MARKER pattern**: place `MARKER NO-MODULENAME` near the top (after the initial comments). This lets the entire module be removed from the dictionary in one step during interactive development.
- **NEEDS for dependencies**: always use `NEEDS` to pull in prerequisites — never assume a word is already present.
- **Refactoring guideline**: if a definition inside a `lib/` module is general enough to be useful independently of that module, extract it into a new `inc/` file and replace the inline definition with a `NEEDS` call. This keeps modules focused and avoids duplication across libraries.

Example of the refactoring pattern:
```forth
\ Before — definition inline in lib/GRAPHICS.f:
: FLIP  ( n -- n' )  ... ;

\ After — definition moved to inc/flip.f; lib/GRAPHICS.f becomes:
NEEDS FLIP
```

### Deployment to ZX Spectrum Next (nextsync)

There is no separate SD/ staging directory. The repo root (`C:\Zx\Forth\F18`) is the nextsync
root and maps directly to the Next's SD card filesystem. Files edited in `inc/` or `lib/` are
ready to sync immediately — no intermediate copy step is needed.

To transfer files to the Next, run the nextsync server from the repo root:

```
cd C:\Zx\Forth\F18
python nextsync.py
```

Then on the Next, execute `.sync`. Only new or modified files are transferred.

The dot-command variant (`dot/`) contains only the compiled binaries `vforth` and `term0`.
The dot variant depends on the classic installation being present (see Directory Structure above).

## Testing

```forth
INCLUDE TEST/CORE-TESTS.f
INCLUDE TEST/FLOATING-TESTS.f
```

Tests use `{...}T` notation (defined in `lib/testing.f`).

## tutorial/ conventions

> **Full conventions reference:** `tutorial/tutorial-conventions.md` — the authoritative rules
> document for tutorial development (language, file structure, comment style, stack notation,
> numeric literals, vForth-specific rules, CREATE…DOES> conventions, philosophy). The summary
> below covers the most important points; consult that file for details.

The `tutorial/` directory contains guided, self-contained tutorials introducing vForth features progressively. Conventions:

**File naming.** Use a three-digit prefix for ordering: `001-stack-basics.f`, `002-defining-words.f`, etc. The prefix determines load order and reading sequence; renumbering is acceptable when inserting new topics.

**Self-contained.** Each tutorial must work in isolation. Use `NEEDS` for every dependency — never assume a word is already loaded. A reader should be able to `INCLUDE tutorial/NNN-topic.f` from a clean vForth session and have it work.

**Comment-heavy.** Unlike `inc/` files (which have minimal comments), tutorials are primarily documentation. Explain the *why*, show the stack effects, describe expected output. The target reader is a programmer new to vForth but not necessarily new to programming.

**MARKER for interactive reset.** Place `MARKER NEWTASK` near the top (after initial comments). This lets the reader unload the tutorial and reload it cleanly during interactive exploration. A fixed name is used across all tutorials to keep it short and easy to type on the Spectrum keyboard.

**Show expected output.** Document what each example prints or leaves on the stack, either inline as comments or in a trailing test block using `{...}T` notation (load `lib/testing.f` first).

**Typical structure:**
```forth
\
\ 001-stack-basics.f
\ Introduction to the vForth stack and basic arithmetic.
\

MARKER NEWTASK

\ --- example 1: pushing values ---
\ 3 4 +  leaves 7 on the stack
.( Tutorial 001: stack basics loaded. Try: 3 4 + . )

: DEMO-ADD  ( a b -- a+b )
    \ simple addition demo
    + ;

\ Expected: 7
\ 3 4 DEMO-ADD .
```

**Progression.** Later tutorials may use `NEEDS` to load words introduced by earlier ones, but must not use `INCLUDE tutorial/NNN-...f` — they load vocabulary, not scripts. If a tutorial concept is general enough to become a real `inc/` word, extract it following the standard refactoring pattern.

## Breaking Changes Since v1.2

- `'` (tick) returns CFA, not PFA
- `-FIND` returns CFA, not PFA
- `SP!` / `RP!` require the target address
- `WORD` returns HERE address
- `CREATE` returns PFA
- `VARIABLE` now has standard behavior (since v1.52): when executed it pushes its own address (PFA). Old code using non-standard VARIABLE behavior must be verified.
- `DOES>` follows latest Forth standard (v1.8+)

## DOES> and PFA: stack convention

At runtime, the code following DOES> receives PFA (the Parameter Field
Address of the product word) as the top of stack item.  Any arguments
that the caller pushed before invoking the product word are beneath PFA
on the Forth stack.

On the Z80, the hardware stack grows downward in memory, so "top of
stack" is the cell at the lowest current stack address -- the most
recently pushed item.  DOES> pushes PFA last, making it TOS at the
moment the DOES> body begins executing.

The PFA holds all compile-time data stored by , C, or ALLOT during the
CREATE phase.  The DOES> body uses PFA to access that data; caller
arguments sit below PFA and are accessed via stack manipulation.

Canonical example from inc/2constant.f:
  : 2CONSTANT  ( d -- )
      CREATE , ,
      DOES>   ( pfa -- d )
          2@ ;
  \ <BUILDS stores hi then lo cell at PFA.
  \ DOES> pushes PFA as TOS; 2@ fetches both cells from PFA.

## Heap Memory Facility

vForth provides an extended heap that lives in the MMU7 8K page ($E000–$FFFF).
It is a custom invention of the author and is separate from both the main
dictionary (code/data space) and the name-space already held in the same MMU7
page. The heap grows across multiple 8K pages; `HP@` tracks the current
allocation frontier as a **heap-pointer** (`ha`).

### Heap-pointer format (`ha`)

A heap-pointer is a single 16-bit cell encoding both the 8K page and the
offset within that page:

- **Bits 15–13** (3 MSBs): page number (relative to the base heap page)
- **Bits 12–0** (13 LSBs): byte offset from `$E000` within that page

`FAR ( ha -- a )` decodes `ha`: it extracts the page number, maps it onto
MMU7 via `MMU7!`, and returns the real address in `$E000–$FFFF`.
The page stays mapped until the next `FAR` call.

### Key heap words

| Word | Stack | Description |
|------|-------|-------------|
| `H"` | `( -- ha )` | Parse a string literal; store as counted-z-string in heap; return `ha` |
| `FAR` | `( ha -- a )` | Map heap page onto MMU7; return real address in $E000+ |
| `>FAR` | `( ha -- a page )` | Decode `ha` without mapping (low-level) |
| `MMU7!` | `( page -- )` | Map page onto MMU7 slot |
| `MMU7@` | `( -- page )` | Read current MMU7 page |
| `HP@` | `( -- ha )` | Current heap frontier (as heap-pointer) |
| `HALLOT` | `( n -- )` | Allocate n bytes in heap; advance `HP@` |
| `HEAP` | `( n -- a )` | Allocate n bytes; return real address (maps MMU7) |
| `S"` | `( -- addr len )` | Like `H"` but returns real addr+len; **volatile at interpret time** |

### Usage rules

**Use `H"` (not `S"`) for persistent heap strings at interpret time.**
`S"` at interpret time returns a raw `$E000+` address that becomes invalid
as soon as a subsequent `FAR` or `HEAP` call maps a different page.
`H"` returns a heap-pointer `ha` that remains valid indefinitely; decode it
with `FAR` immediately before use.

**Pattern for a string table in heap:**

```forth
\ Build: store heap-pointers in a dictionary table
CREATE MY-TABLE
    H" first string"  ,    \ ha stored in table
    H" second string" ,

\ Use: decode ha just before use
MY-TABLE CELLS + @    \ ha
FAR                   \ real address, MMU7 now mapped
1+                    \ skip count byte -> z-string
```

**`FAR` side-effect:** after `FAR`, MMU7 points to the page containing the
returned address. Do not call another `FAR` (or any word that calls `HEAP`)
while you still need the first address to remain valid.

### Design note and known limitation

The ideal would be a standard-ANS `S"` that is safe both inside definitions
and at interpret time. The current split (`S"` = volatile at interpret time,
`H"` = persistent but non-standard) is a deliberate compromise to keep the
core binary small and the heap facility self-contained.

**Future work**: find a solution that gives a fully standard `S"` without
bloating the core. Until then, use `H"` for any persistent heap string
allocation at interpret time.

### Sources
- `inc/doc/far.f` — `FAR` definition (core word — reference only)
- `inc/h~.f` — `H"` definition (FAT mapping: `"` → `~`)
- `inc/hallot.f` — `HALLOT`
- `inc/aligned.f` — `ALIGNED`
- PDF documentation: "Heap memory facility" section

## Known Bugs

### `INCLUDE` / `NEEDS`

The source file being loaded must end with a blank line. If the last line has no
trailing newline, the system crashes — typically displaying a vertical grid pattern
on screen. `NEEDS` is affected by the same bug because it uses `INCLUDE` internally.

**Workaround:** always ensure every `.f` file ends with a blank line.

### `LOAD` (block/screen interpreter)

- **Structure spanning BLOCK boundaries.** Long structured definitions (e.g.
  `ENUMERATED`) cannot straddle the boundary between the first and second 1 KB block
  of the same screen. The definition must fit entirely within one block.
- **NUL character (`0x00`) in a screen.** A NUL byte inside a screen is invisible
  in normal display but silently stops interpretation mid-load with no error message.
  Use `EDIT` (§ 2.15) to locate it: EDIT shows the ASCII code of the character under
  the cursor.
- **Screen #0.** Loading from Screen #0 (`0 LOAD`) crashes the system.

### `OPEN<`

Can only be used in interpretation mode. Calling it inside a colon-definition is
not supported and will produce incorrect behaviour.

### `LED`

Pressing `[BREAK]` stops any active I/O operation immediately. If `LED` is driving
an I/O sequence at the time, this may produce data loss. Always ensure the operation
has completed before pressing `[BREAK]`.

## Key Files

| File | Role |
|---|---|
| `src/F18e.f` | Historical Forth form of the core — readable reference, not maintained in sync with .asm |
| `project/vForth18_DOES/source/system.asm` | Macros, constants, `New_Def`, `next`, `psh1`, `psh2` |
| `project/vForth18_DOES/source/L0.asm` | Origin area + primitives (LIT, EXECUTE, loops, …) |
| `project/vForth18_DOES/source/L1.asm` | Core vocabulary |
| `project/vForth18_DOES/source/L2.asm` | Mid-level vocabulary |
| `project/vForth18_DOES/source/L3.asm` | High-level vocabulary |
| `project/vForth18_DOES/source/main.asm` | Entry point, DEBUGGING flag, SAVEBIN directives |
| `HISTORY.txt` | Detailed build history since 2020 |
