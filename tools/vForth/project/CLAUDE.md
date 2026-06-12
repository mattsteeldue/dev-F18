# project/ — Assembler Core (SjASMPlus)

This directory contains the Z80N assembler source for the vForth core binary.
Two variants: `vForth18_DOES/` (classic, launcher-based) and `vForth18_DOT/` (dot-command).

## Primary Development Workflow

The project master has **moved to Visual Studio Code** with a Z80N assembler (SjASMPlus).
Self-hosted compilation on the ZX Spectrum Next / CSpect emulator is too slow for daily
development.

**The representations that must stay byte-identical (for the classic variant):**

1. `src/F18e.f` — the Forth source that compiles itself on the ZX Spectrum Next
2. `project/vForth18_DOES/source/*.asm` — the same compiler in Z80N assembly for SjASMPlus

Both produce the same `forth18e.bin`. When the `.asm` files are modified, `F18e.f` must be
updated to match — and vice versa. The vForth18_DOT variant has no equivalent F18e.f
alignment path.

### Building with VS Code (primary)

**Classic variant** — `project/vForth18_DOES/`:
```
main.asm -> system.asm, L0.asm, L1.asm, L2.asm, next-opt1.asm, L3.asm
```
Outputs: `output/forth18e.bin`, `output/ram8.bin`

**Dot variant** — `project/vForth18_DOT/`:
```
main.asm -> system.asm, L0.asm, L1.asm, L2.asm, next-opt1.asm, L3.asm
```
Output: a dot-command binary deployed to `dot/`

### Building self-hosted (deprecated — not used anymore)

Screen #10 is now free for end-user use. To use the old self-hosted method, Screen #10
must first contain the line:

    include src/f18e.f

Then, within CSpect or on real hardware, execute `10 LOAD` to trigger compilation. The
system compiles itself twice (first to upper memory, then back to origin). The resulting
binary can be transferred to a PC and verified byte-by-byte against the SjASMPlus output
using a binary diff tool (e.g. AraxisMerge). This applies only to the classic
(vForth18_DOES) variant.

### Verifying alignment between .asm and F18e.f

Set `DEBUGGING equ -1` in `main.asm` for binary comparison mode (origin is adjusted to
match the Forth-compiled output for byte-by-byte diff). Applies to vForth18_DOES only.

## F18e.f <-> .asm Mnemonic Correspondence

The ASSEMBLER vocabulary in F18e.f is postfix/stack-based: each element (instruction word,
register specifier, operand commaer) is a **separate Forth word**. The full reference is
`src/Z80N-Assembler-Dictionary.txt`. Register notation:

- r|  -- source register: B| C| D| E| H| L| A| (HL)|
- r'| -- destination register: B'| C'| D'| E'| H'| L'| A'| (HL)'| (NOT the alternate
  register set -- just destination syntax), think the single-quote as a raised comma
- rr| -- register pair: BC| DE| HL| SP|  also IX| IY| AF|
- f|  -- flag for JP/CALL/RET: NZ| Z| NC| CY| PO| PE| P| M|
- f'| -- flag for JR: NZ'| Z'| NC'| CY'|
- b|  -- bit position: 0| ... 7|
- n N,  nn NN,  aa AA,  d D,  nn LH, -- operand "commaers" (push value, emit bytes)

| F18e.f (ASSEMBLER vocab) | Z80N (SjASMPlus) | Notes |
|---|---|---|
| CODE name ... C; | New_Def LABEL, "name", is_code, is_normal + code | low-level word |
| Next | next macro -> jp (ix) | inner interpreter |
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
| JRF f'\| HOLDPLACE ... HERE DISP, | jr f, label | forward jump pattern in F18e.f |
| CALL aa AA, | call aa | |
| CALLF f\| aa AA, | call f, aa | |
| PUSHN nn LH, | push nn | via ld hl,nn / push hl |
| DJNZ d D, | djnz d | |

Forward pointers in F18e.f (e.g. `HERE TO next^`, `HERE TO loop^`) mark addresses that
are then referenced by labels in the .asm (e.g. `Next_Ptr:`, `Loop_Ptr:`).

## Intentional Divergences Between vForth18_DOES and vForth18_DOT

The DOT variant has critical differences from the classic DOES variant to accommodate the
dot-command environment (banking, interrupts, exit strategy). These divergences are
**intentional and must be preserved** during maintenance.

### ROM Call Strategy (Interrupt Handling)

**vForth18_DOES:** Calls ROM routines directly via `call` or `rst $08`.

**vForth18_DOT:** Wraps ROM calls with `di`/`ei` (disable/enable interrupts) and uses
`rst $18` with a pointer, because the dot-command environment may be interrupted by the
OS and needs to protect its state. Examples:

| Location | vForth18_DOES | vForth18_DOT |
|---|---|---|
| `L0.asm:904` — (EMITC) / C_Emit_Bel | `call $03B6` | `di` / `rst $18` / `defw $03B6` / `ei` |
| `L0.asm:1147` — SELECT | `call $1601` | `di` / `rst $18` / `dw $1601` / `ei` + uses TSTACK |
| `L0.asm:777-780` — (EMITC) / CLS_No_Layer_0 | `rst $10` | `di` / `rst $10` / `ei` |

### Stack and Memory Setup

**SELECT (L0.asm:1144):**
- vForth18_DOES: Uses `ld sp, Cold_origin - 5` to set up the stack for the ROM call
- vForth18_DOT: Uses `ld sp, TSTACK` (a dedicated stack space allocated during startup)

### AUTOEXEC (L3.asm:780)

**vForth18_DOES:** Loads and executes screen #11 (block-based):
```asm
dw      LIT, 11
dw      LOAD    // Executes the screen via block interpreter
dw      QUIT
```

**vForth18_DOT:** Opens and executes a file passed as a parameter from BASIC,
defaulting to `c:/tools/vforth/lib/autoexec.f`:
```asm
dw      LIT, Param_From_Basic
dw      PAD, ONE
dw      F_OPEN
dw      F_INCLUDE         // Executes the file via file-based interpreter
```

### Error Handling (BLK-INIT in next-opt1.asm:169)

**vForth18_DOES:** Raises a `QERROR` exception which stays within Forth and issues an error message:
```asm
dw  LIT, $2C, QERROR
```

**vForth18_DOT:** On file-open error, patches `Exit_with_error` and returns to BASIC:
```asm
dw  ZBRANCH
dw  Blk_Init_Endif - $
dw  LIT, $FFCF                  // PATCH op-code RST $08, $FF
dw  LIT, Exit_with_error
dw  STORE
dw  BASIC
```

### Startup and Shutdown (L2.asm)

The DOT variant performs extensive startup to save OS state and initialize banking:
- Saves CPU speed, MMU page configuration, and current layer
- Allocates 12 pages (8 HEAP, 3 MAIN, 1 BACKUP) from the OS
- Backs up MMU2 to restore on exit to BASIC
- Changes to `C:/tools/vForth/` directory
- Loads vocabulary image to `$E000` from persistent heap pages

The DOES variant is simpler: it loads directly from `forth18e.bin` and `ram8.bin` at a
fixed origin, no banking complexity.

### When Modifying Code Shared Between Variants

1. **Read-only core (no drift expected):** L1.asm, L2.asm (non-startup parts), L3.asm
2. **Carefully sync these locations** (they diverge):
   - L0.asm: ROM call patterns (EMITC, SELECT, CLS_No_Layer_0)
   - next-opt0.asm: File operations (generally share code, but audit carefully)
   - next-opt1.asm: BLK-INIT error path

After core changes, run the `/check-sync` skill to audit drift and `/sd-sync` to deploy
updated files to the SD card test image.

## Utilities

### asm2hex.py -- ASSEMBLER to hex converter

`util/asm2hex.py` converts a Forth source file that uses ASSEMBLER vocabulary mnemonics
inside `CODE...C;` blocks into release form (raw hex `C,` literals).  Use it when
finalising a new low-level word developed interactively on the ZX Spectrum Next / CSpect
before committing it to `inc/`:

```
python3 util/asm2hex.py input.f           (stdout)
python3 util/asm2hex.py input.f -o out.f  (file)
```

Lines outside `CODE...C;` blocks pass through unchanged.  Address-dependent operands
(`AA,`, `HOLDPLACE`, `DISP,`, `BACK,`) are preserved as-is.  Unrecognised patterns
pass through with a `\ WARN` comment for manual review.

## Key Files

| File | Role |
|---|---|
| `src/F18e.f` | Historical Forth form of the core -- readable reference, not maintained in sync with .asm |
| `project/vForth18_DOES/source/system.asm` | Macros, constants, `New_Def`, `next`, `psh1`, `psh2` |
| `project/vForth18_DOES/source/L0.asm` | Origin area + primitives (LIT, EXECUTE, loops, ...) |
| `project/vForth18_DOES/source/L1.asm` | Core vocabulary |
| `project/vForth18_DOES/source/L2.asm` | Mid-level vocabulary |
| `project/vForth18_DOES/source/L3.asm` | High-level vocabulary |
| `project/vForth18_DOES/source/main.asm` | Entry point, DEBUGGING flag, SAVEBIN directives |
| `HISTORY.txt` | Detailed build history since 2020 |
