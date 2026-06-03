
# vForth Minimal Emulator -- Design Document

Goal: run `forth18e.bin` on a headless Python machine that is just big
enough to host the Forth inner interpreter and the heap paging mechanism.
The result is a fast debug loop that does not require CSpect or real ZX
Spectrum Next hardware.


## 1. The Two Binaries

| File | Load address | Size | Content |
|---|---|---|---|
| `forth18e.bin` | `$6366` | 9 999 bytes | Origin area + full Forth dictionary |
| `ram8.bin` | `$E000` | 8 192 bytes | Initial heap (name-space + code-space) |

`main.asm` saves them with these directives:

    SAVEBIN "output/forth18e.bin", ORIGIN, 9999   ; ORIGIN = $6366
    SAVEBIN "output/ram8.bin",     $E000, $2000   ; heap page


## 2. Memory Map

The emulator needs a flat 64 KB address space.  Only a subset of
addresses are actually touched at startup.

    $0000 - $6365   not used by vForth (ROM area on real hardware; not needed)
    $6366 - $8A75   forth18e.bin  (9 999 bytes, loaded verbatim)
    $8A76 - $D2F7   unused gap    (zero-initialise)
    $D2F8           S0 / TIB      (calc-stack top; TIB starts here)
    $D2F8 - $D397   TIB / calc-stack area (160 bytes)
    $D398           R0            (return-stack top; user variables start here)
    $D398 - $D3E7   user variables + return stack (80 bytes)
    $D3E8 - $DFFF   6 block buffers x 516 bytes = 3096 bytes
    $E000 - $FFFF   heap / dictionary (ram8.bin, 8 192 bytes, MMU slot 7)

Constants from `system.asm`:

    LIMIT_system  = $E000
    FIRST_system  = $E000 - 516*6 = $D3E8
    USER_system   = $D3E8 - 80   = $D398
    R0_system     = $D398
    TIB_system    = $D398 - 160  = $D2F8
    S0_system     = $D2F8


## 3. Paging Model (MMU)

The ZX Spectrum Next maps the 64 KB address space as eight 8 KB slots
(slots 0-7, addresses $0000-$1FFF each).  Slot 7 covers $E000-$FFFF.
Each slot holds a page number (0-based, 8 KB pages of physical RAM).

vForth uses **only slot 7** (the heap).  The relevant Next register is:

    Next register 87 ($57) = page number currently mapped at slot 7

The instruction `nextreg 87, a` (Z80N opcode `$ED $92 $57`) writes `A`
into register 87, swapping which physical 8 KB page appears at $E000.

### Initial heap page

`ram8.bin` is the initial content of **RAM page 32 (`$20`)**, the first
8 KB page of heap.  On a real ZX Spectrum Next, the BASIC loader does:

    LOAD "ram8.bin" BANK 32     ; loads into 8K physical page $20

At power-on, page $20 is fitted at slot 7 ($E000).  The heap variable
`HP` starts at `$0002` which encodes page $20, offset $0002 (see §3.1).

### Heap-Pointer encoding  (§6.3.1, vForth 1.8 manual)

A Heap-Pointer (`ha`) is a 16-bit integer that encodes both the physical
page and the offset within it.  The base page is 32 (`$20`).

    page   = 32 + (ha >> 13)           ; upper 3 bits select page offset from base
    offset = $E000 + (ha & $1FFF)      ; lower 13 bits = byte offset within 8K page

Examples from the manual (§6.3.2):

    ha = $0F80  ->  page $20,  physical address $EF80
    ha = $2000  ->  page $21,  physical address $E000   (start of 2nd heap page)

Conversion words:
- `>FAR  ha -- a p`  decode ha into physical offset `a` ($E000..$FFFF) and page `p`
- `<FAR  a p -- ha`  encode physical offset + page into ha
- `FAR   ha -- a`    decode AND fit the page into MMU7 (calls `>FAR` then `MMU7!`)
- `MMU7! n --`       write page number `n` into Next register 87 (slot 7)

### Minimal paging model (Phase 1 emulator)

Load `ram8.bin` as page $20.  On `nextreg 87, n`:

    if n == 32 ($20): already mapped -- do nothing
    else:             raise EmulatorError('multi-page heap not yet supported')

This is sufficient to run the cold start, inner interpreter, and any
tutorial that does not overflow the first 8 KB of heap.

### Full paging model (future)

Allocate a dictionary of `{page_number: bytearray(8192)}`.  On
`nextreg 87, n`:

    mmu7_page = n
    slot7 -> pages[n]

Read/write to $E000-$FFFF dispatches through `pages[mmu7_page]`.
New pages are allocated lazily (zeroed bytearray) when first written.


## 3a. Heap Internal Structure  (§6.3.2, vForth 1.8 manual)

The heap is a doubly-linked list of allocated chunks.  It starts at
page $20, offset $0002.  `HP` (user variable) holds the Heap-Pointer to
the next free location.

Each call to `HEAP n` allocates a chunk as follows (all addresses in
`page:offset` notation, base page $20):

    page:offset   content
    ─────────────────────────────────────────────────────────────
    hp-0          forward pointer  (2 bytes)  ──┐ points to next hp
    hp+2          allocated data   (n bytes)    │
    hp+2+n        trailing NUL     (2 bytes)    │
    hp+2+n+2      backward pointer (2 bytes)  ──┼─ points to previous hp
    hp+2+n+4      new HP           (next free)◄─┘
    ─────────────────────────────────────────────────────────────

So each allocation consumes `n + 6` bytes of heap (2 forward + n data +
2 NUL trailer + 2 backward).

Concrete example from the manual (HP starts at `$0F80`, page $20):

    After `7 HEAP` (7-byte allocation, returns `$0F82`):
    20:0F80  0F8D    forward ptr  -> new HP
    20:0F82  .. x7   7 bytes (uninitialised)
    20:0F89  00 00   NUL trailer
    20:0F8B  0F80    backward ptr -> previous HP
    20:0F8D  ....    new free HP

For the emulator, `HEAP` / `HALLOT` update the in-memory HP cell and
page-map the correct page via `nextreg 87`.  The linked-list is in
memory; the emulator does not need to parse it -- it just needs the
paging to be correct.


## 4. Z80N Instruction Set

Standard Z80 instructions are well covered by existing Python emulators
(e.g. `z80` / `py80` / `z80ex`).  vForth uses a small number of Z80N
extensions.

### Extensions actually used in the binary

| Opcode | Mnemonic | Used for | Emulator action |
|---|---|---|---|
| `$ED $92 n` | `nextreg n, a` | write Next register n from A | see section 3 |
| `$ED $91 n m` | `nextreg n, m` | write Next register n immediate | not used in core |
| `$ED $36` | `add de, a` | advance RP in (LEAVE) | implement: `DE = (DE + sign_extend(A)) & 0xFFFF` |
| `$ED $23` | `push nn` | push 16-bit immediate | implement: SP-=2; mem[SP]=nn |
| `$ED $30` | `mul d, e` | multiply D*E -> DE | used in GRAPHICS lib (not in core) |

`nextreg` is the only one that interacts with hardware state.  The others
are pure arithmetic and trivially implementable.

### Z80N instruction decoding

All Z80N extensions share the `$ED` prefix.  After `$ED`, the second byte
selects the instruction:

    $91  nextreg n, m    (two more bytes: register, value)
    $92  nextreg n, a    (one more byte:  register)
    $23  swapnib         (swap nibbles of A -- not used in core)
    $24  mirror          (mirror bits of A -- not used in core)
    $30  mul d, e        (unsigned 8x8 -> 16)
    $36  add de, a       (signed add A to DE)
    $93  pixeldn         (not used in core)
    $94  ldix            (not used in core)
    $A4  ldirx           (not used in core)


## 5. Inner Interpreter

The inner interpreter lives at `Next_Ptr` (`L0.asm:86`).  Its machine
code is:

    Next_Ptr:
        ld  a, (bc)   ; fetch low byte of next CFA from IP
        inc bc
        ld  l, a
        ld  a, (bc)   ; fetch high byte
        inc bc
        ld  h, a      ; HL = CFA of next word
    Exec_Ptr:
        jp  (hl)      ; jump to code at CFA

In Python terms:

    def inner_next(cpu, mem):
        lo = mem[cpu.BC]; cpu.BC = (cpu.BC + 1) & 0xFFFF
        hi = mem[cpu.BC]; cpu.BC = (cpu.BC + 1) & 0xFFFF
        cpu.HL = (hi << 8) | lo          # HL = CFA
        cpu.PC = cpu.HL                  # jp (hl)

`IX` always holds `Next_Ptr`.  `jp (ix)` at the end of every CODE word
transfers control back here.


## 6. Threading Model

Direct threading means the CFA holds executable Z80 code:

    Low-level word:   CFA -> Z80 machine code ... jp (ix)
    High-level word:  CFA -> CALL Enter_Ptr
                      PFA -> xt_1, xt_2, ..., EXIT_xt

`Enter_Ptr` (`L1.asm`) pushes the current IP onto the return stack, then
sets BC (IP) to PFA+0:

    Enter_Ptr:
        push bc          ; save IP on return stack (via DE)
        ...              ; DE is RP, grows downward
        ld   bc, hl+3    ; PFA = CFA + 3 (CALL = 3 bytes)
        next

`EXIT` pops IP from the return stack:

    EXIT:
        pop  bc          ; (from return stack via DE)
        next

For the emulator, both can be handled as special cases in the dispatch
loop rather than executing real Z80 code, which is faster and simpler.


## 7. Cold Start Sequence

`ColdRoutine` (= `WarmRoutine`) in `L2.asm:266`:

    ld  sp, (S0_origin)     ; SP = S0 = $D2F8
    ld  de, (R0_origin)     ; DE = R0 = $D398  (RP)
    ld  bc, Warm_Start      ; BC = IP = address of [dw WARM] or [dw COLD]
    ld  ix, Next_Ptr        ; IX = inner interpreter
    next                    ; begin execution

`Cold_Start` is a two-cell table:

    Warm_Start: dw WARM      ; BC points here for warm start
    Cold_Start: dw COLD      ; BC+2 for cold start (ColdRoutine increments BC twice)

The emulator must:
1. Load `forth18e.bin` at `$6366`.
2. Load `ram8.bin` at `$E000`.
3. Set `SP=$D2F8`, `DE=$D398`, `IX=Next_Ptr`.
4. Set `BC=Cold_Start` (= `Warm_Start + 2`).
5. Enter the fetch-decode-execute loop.


## 8. I/O and ROM Stubs

vForth calls the ZX Spectrum Next OS via `rst 08 / db $94` (esxDOS /
NextZXOS) and direct port I/O.  For the minimal emulator these need stubs.

| Mechanism | Real action | Stub strategy |
|---|---|---|
| `rst 08 / db $94` | NextZXOS call | intercept opcode; dispatch on `(IX_Echo)` / C register |
| `out (c), l` with BC=$243B | select Next register | record `selected_reg = L` |
| `in l, (c)` with BC=$253B | read Next register | return value from `next_regs[selected_reg]` |
| `out (c), l` with BC=$253B | write Next register | `next_regs[selected_reg] = L`; if reg=87 swap page |
| `nextreg 87, a` | set MMU slot 7 | see section 3 |
| `out ($FE), a` | set border colour | ignore |
| `in a, ($FE)` | read keyboard | return $BF (no key pressed) |
| ROM `PRINT` / `CLS` | character output | map to `sys.stdout.write` |

The critical one for basic operation is the NextZXOS file I/O (used by
`INCLUDE`, `NEEDS`, block read/write).  For a tutorial runner, at minimum
stub `F_OPEN`, `F_READ`, `F_CLOSE` to read files from the host filesystem.


## 9. Implementation Phases

### Phase 1 -- Inner interpreter only (no I/O)

- Flat 64 KB `bytearray`.
- Load the two binaries.
- Implement all standard Z80 instructions + `add de,a` + `nextreg`.
- Implement `Enter_Ptr` and `EXIT` natively (bypass Z80 emulation).
- Stub all I/O and OS calls as no-ops.
- Goal: execute `COLD` through to the `QUIT` loop, then stop at `KEY`.

Recommended Z80 Python library: **`z80`** (PyPI, pure Python, Z80 only)
or **`py65`**-style custom implementation targeting just the instructions
actually present in `forth18e.bin`.

### Phase 2 -- Terminal I/O

- Stub `KEY` to read from `sys.stdin`.
- Stub `EMIT` / `EMITC` to write to `sys.stdout`.
- Stub `CR` as `print()`.
- Goal: interactive Forth prompt in the terminal.

### Phase 3 -- File I/O

- Stub `F_OPEN`, `F_CLOSE`, `F_READ`, `F_WRITE`, `F_SEEK` to call Python
  `open()` / `read()` / `write()` / `seek()`.
- Goal: `INCLUDE tutorial/001-intro.f` works end-to-end.

### Phase 4 -- Block I/O

- Stub `BLK-READ` / `BLK-WRITE` to operate on a host-side `!Blocks.txt`.
- Goal: `LOAD` screens, `THRU`, all block-based tutorials.


## 10. Key Addresses (summary)

| Symbol | Address | Source |
|---|---|---|
| ORIGIN | `$6366` | `main.asm` |
| `Next_Ptr` | runtime (scan binary for pattern) | `L0.asm:86` |
| `Enter_Ptr` | runtime | `L1.asm` |
| `S0` | `$D2F8` | `system.asm` formula |
| `TIB` | `$D2F8` | `system.asm` formula |
| `R0` | `$D398` | `system.asm` formula |
| `USER` | `$D398` | `system.asm` formula |
| `FIRST` | `$D3E8` | `system.asm` formula |
| `LIMIT` | `$E000` | `system.asm` constant |
| `Warm_Start` | `Cold_Start - 2` | `L2.asm:260` |
| `Cold_Start` | `Cold_Start` | `L2.asm:261` |
| Heap (slot 7) | `$E000-$FFFF` | `main.asm` SAVEBIN |
| Heap base page | RAM page 32 (`$20`) | §6.3.2 manual; BASIC `LOAD "ram8.bin" BANK 32` |
| Heap-Pointer base | `$0002` (page $20 offset $0002) | initial `HP` value |
| HP encoding | `page = 32 + (ha>>13)`, `offset = $E000 + (ha & $1FFF)` | §6.3.1 manual |
| MMU reg slot 7 | Next register 87 (`$57`) | `L0.asm` nextreg usage |
