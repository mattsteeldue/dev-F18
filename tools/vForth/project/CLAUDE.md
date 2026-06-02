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
