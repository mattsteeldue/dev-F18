# IM2-HW: Hardware Interrupt Mode 2 Library

**Status**: Design Plan  
**Author**: Matteo Vitturi  
**Date**: 2026-07-11  
**Next Reference**: zx-next-dev-guide-r3.txt §3.12.3

---

## Overview

Create a new Forth library `lib/IM2-HW.f` that provides high-level Forth interface to the **Z80N Hardware Interrupt Mode 2** facility on ZX Spectrum Next, complementing the existing legacy `INTERRUPTS` library with a cleaner, more structured API.

**Key benefit**: Hardware IM2 mode (Next reg $C0+) properly implements Z80 IM2 daisy-chain priority, eliminating the need to poll or guess which interrupt source triggered the handler. Each interrupter gets its own vector entry and handler, with clear priority ordering.

---

## Rationale for New Library

1. **Legacy INTERRUPTS** (`lib/INTERRUPTS.f`) was written for legacy IM2:
   - Single vector table at address $xxFE0-$xxFF
   - All interrupts use same table-based lookup with random data bus LSB
   - No device priority; user must poll all sources to determine which fired
   - Works on any Z80, but fragile (odd data bus values can corrupt address calculation)

2. **Hardware IM2** (Z80N on Next, core 3.0+) improves on legacy:
   - Uses dedicated Next registers ($C0, $C4, $C5, $C6, $CC, $CD, $CE)
   - 16 dedicated vector slots (line interrupt, UART Rx/Tx, CTC channels 0-7, ULA)
   - Hardware daisy-chain priority: handler called knows exactly which source fired
   - Simpler vector table setup: 32-byte aligned table, no random LSB randomness
   - Can selectively interrupt DMA via $CC/$CD/$CE DMA interrupt enable registers

3. **Design separation**:
   - Keep `INTERRUPTS` as-is for legacy/IM1 use and educational reference
   - New `IM2-HW` targets modern Next workflow with clearer semantics
   - Both can coexist; user chooses which fits their needs

---

## Architecture

### Vector Table

```forth
.ALIGN 32              \ 32-byte boundary required
IM2-HW-TABLE:
  DW HANDLER0          \ 0 = Line interrupt (highest priority)
  DW HANDLER1          \ 1 = UART0 Rx
  DW HANDLER2          \ 2 = UART1 Rx
  DW HANDLER3          \ 3-10 = CTC Channels 0-7 (3 shown)
  ...
  DW HANDLER-ULA       \ 11 = ULA (frame interrupt, commonly used for music)
  DW HANDLER12         \ 12 = UART0 Tx
  DW HANDLER13         \ 13 = UART1 Tx (lowest priority)
  DW 0                 \ Padding to 16 entries
  DW 0
```

Each entry is a 2-byte Forth CFA address (little-endian).

### Interrupt Enable Registers

- **$C4** (Interrupt Enable 0): Bits control ULA, CTC 0-7
- **$C5** (Interrupt Enable 1): Bits control UART Rx/Tx (not used in current core)
- **$C6** (Interrupt Enable 2): Bits control CTC channels (overlap—clarify mapping)
- **$C0** (Interrupt Control): Top 3 bits of vector table LSB, bit 0 = enable HW IM2

### DMA Interrupt Enable Registers (Optional)

- **$CC, $CD, $CE** (DMA Interrupt Enable 0-2): Allow specific interrupters to interrupt ongoing DMA

---

## API Design (Sketch)

### Setup Phase

```forth
IM2-HW-INIT ( -- )
  \ Initialize vector table, enable hardware IM2 mode
  \ Steps:
  \   1. Set I register to MSB of IM2-HW-TABLE
  \   2. Configure $C0 with top 3 bits of vector table LSB + enable bit
  \   3. Disable specific interrupters via $C4/$C5/$C6 (default: ULA only)
  \   4. Enable interrupts (EI)
```

### Handler Registration

```forth
' MY-LINE-HANDLER  IM2-HW-SET-HANDLER-LINE   ( xt -- )
' MY-ULA-HANDLER   IM2-HW-SET-HANDLER-ULA    ( xt -- )
' MY-UART0RX       IM2-HW-SET-HANDLER-UART0RX ( xt -- )
```

Each `IM2-HW-SET-HANDLER-*` word updates the corresponding vector table entry.

### Enable/Disable Per-Interrupter

```forth
IM2-HW-ENABLE-ULA    ( -- )    \ Enable ULA frame interrupt
IM2-HW-DISABLE-ULA   ( -- )
IM2-HW-ENABLE-CTC0   ( -- )    \ Enable CTC channel 0
IM2-HW-ENABLE-UART0RX ( -- )
IM2-HW-DISABLE-UART0RX ( -- )
```

### Shutdown

```forth
IM2-HW-DISABLE ( -- )
  \ Disable hardware IM2 mode gracefully
  \ Steps: DI, clear $C0 enable bit, re-enable IM1 or halt
```

### Query Current State

```forth
IM2-HW-STATUS ( -- c )
  \ Read current interrupter enable mask from $C4
```

---

## Implementation Notes

### Conventions

1. **CFA vs >BODY**: Following vForth convention, all handler xt are CFAs. Direct-threaded code will jump to CFA → CALL Enter_Ptr → body. Low-level CODE words (ISR stubs) must account for this.

2. **Re-entrance**: Handlers run with interrupts *disabled* on entry (hardware behavior). If re-entrance needed, each handler must `EI` explicitly and manage stack.

3. **Register preservation**: Standard Z80 caller-save: caller (ISR frame dispatcher) preserves all registers. Handlers don't need to save/restore unless they use non-vForth low-level code.

4. **Error handling**: Invalid handler index (> 15) or attempt to enable a handler before setting it → no-op or emit error message. Punt for v1.

### File Structure

```
lib/IM2-HW.f
├─ MARKER IM2-HW                    \ Optional clear point
├─ Data (vector table, state vars)
│  ├─ IM2-HW-TABLE (32-aligned)
│  ├─ IM2-HW-I-REGISTER (computed)
│  └─ IM2-HW-ENABLED-MASK (current $C4 state, cached)
├─ Low-level CODE words
│  ├─ IM2-HW-INIT
│  ├─ IM2-HW-DISABLE
│  └─ Register read/write helpers (SetReg, GetReg)
└─ High-level API
   ├─ IM2-HW-SET-HANDLER-*
   ├─ IM2-HW-ENABLE-*
   ├─ IM2-HW-DISABLE-*
   └─ IM2-HW-STATUS
```

Naming: all public words use `IM2-HW-` prefix to avoid collision with `INTERRUPTS`.

### Phased Rollout

**Phase 1 (MVP)**:
- Vector table setup
- Basic `IM2-HW-INIT`, `IM2-HW-DISABLE`
- Handler slots for ULA (most common) and one CTC (for testing)
- No DMA interrupt enable (out of scope for v1)

**Phase 2**:
- Extend handler slots for all 16 interrupters
- Add `IM2-HW-ENABLE-*` / `IM2-HW-DISABLE-*` for each
- Query and status words

**Phase 3** (optional):
- DMA interrupt enable register support ($CC/$CD/$CE)
- Tutorial with music playback example
- Help file entries

---

## Testing Strategy

### Emulator (Headless)

1. **Setup verification**: Call `IM2-HW-INIT`, read back $C0 register (via `NEXTREG` read), verify IM2 enabled bit is set
2. **Handler dispatch**: Install a test handler at ULA slot, trigger interrupt via `HALT`, verify handler was called (counter incremented)
3. **Enable/disable**: Toggle ULA enable, verify register state reflects changes
4. **Multiple handlers**: Set distinct handlers for CTC0 and ULA, verify each fires correctly

### CSpect / Real Hardware (Defer to User Testing)

- Music playback: load a tune driver, verify smooth playback via ULA interrupt
- Multi-device: ULA + CTC timer for lower-latency audio synthesis
- Priority: fire multiple interrupts in sequence, verify daisy-chain priority

---

## Design Questions & Decisions

1. **Handler naming convention**:
   - ✓ Decided: `IM2-HW-SET-HANDLER-ULA`, `IM2-HW-ENABLE-ULA` etc (explicit, self-documenting)
   - Alternative: `HANDLER-ULA!`, `HANDLER-ULA?` (terse, Forth style)

2. **Default handlers**:
   - ✓ Decided: All slots point to `NOOP` or `ISR-RET` on init; user must explicitly set handlers
   - Alternative: Pre-populate with stub that just returns (less safe, but fewer setup steps)

3. **Vector table location**:
   - ✓ Decided: Allocate at compile time in `lib/IM2-HW.f` using `HERE $00FF AND ...` technique from legacy `INTERRUPTS`
   - Rationale: Predictable, no heap fragmentation, user doesn't need to worry about alignment

4. **Separate namespace for register I/O**:
   - ✓ Decided: Use inline `NEXTREG` in Forth words; no wrapper layer
   - Rationale: Direct and clear; matches existing vForth style

---

## Example Usage (Sketch)

```forth
\ Define ULA handler (plays music)
: MUSIC-ISR ( -- )
  MUSIC-PLAYER-TICK
  \ (assumes MUSIC-PLAYER-TICK does not re-enable interrupts)
;

\ Define CTC0 handler (timer-driven synthesis)
: CTC0-ISR ( -- )
  SYNTH-NEXT-SAMPLE
;

\ Initialize and start
IM2-HW-INIT
' MUSIC-ISR IM2-HW-SET-HANDLER-ULA
' CTC0-ISR  IM2-HW-SET-HANDLER-CTC0
IM2-HW-ENABLE-ULA
IM2-HW-ENABLE-CTC0
```

---

## Open Questions for Refinement

1. **Interaction with existing ROM/BIOS**: Can we safely leave IM1 vector at $0038 while running IM2? (Ans: yes, once IM2 is set, IM1 handler is bypassed. But MMU7/paging may interact.)

2. **MMU7 paging in interrupts**: If handler pages in/out MMU7 (e.g., to access heap dictionary), must save/restore MMU7 register. Gotcha from project memory noted; design guidance needed.

3. **F_INCLUDE + interrupt context**: If a file include handler triggers during ISR (edge case), are there re-entrance issues with BLOCK 1 buffer? Probably defer.

4. **DMA precedence**: If DMA is running and interrupt fires, does hardware IM2 pause DMA or skip interrupt? Spec says configurable via $CC/$CD/$CE; defer full implementation.

---

## References

- **zx-next-dev-guide-r3.txt** §3.12.3 "Hardware Interrupt Mode 2", p. 123-124
- **lib/INTERRUPTS.f** (legacy IM2 reference implementation)
- **project/CLAUDE.md** MMU7 paging gotchas (section "Fragilità MMU7")
- **project/vForth18_DOES/source/L0.asm** (check ISR/COLD boot chain if relevant)

---

## Success Criteria

- [ ] Library compiles without errors via `NEEDS IM2-HW`
- [ ] Emulator boots, ULA interrupt fires a handler, counter increments
- [ ] Multiple handlers coexist and fire at correct priority
- [ ] Handlers can be swapped at runtime without crashing
- [ ] Tutorial or help written (Phase 2+)
- [ ] Confirmed on CSpect with music playback (user validation)

---

## REDESIGN 2026-07-11 (post-review) - the committed lib is broken

The Phase 1+2 implementation (commit 1b196c5) never loaded and cannot
work: full findings in `prompts/REVIEW-2026-07-11.md`. Summary: DI/EI do
not exist as words; `CONSTANT IM2-HW-TABLE` pops garbage (missing HERE)
and the 32 table bytes are never ALLOTed; raw Forth xts in the vector
table cannot serve as ISRs; ULA/CTC0 enable bits target the wrong
registers. The API bulk (56 per-slot words) also duplicates itself.
This section is the verified design for the rewrite.

### Reuse lib/INTERRUPTS.f (NEEDS INTERRUPTS)

Its trampoline is the proven pattern to copy, and its helpers solve the
missing pieces directly:

- `ISR-DI` / `ISR-EI` / `ISR-IM2` / `SETIREG` - the CODE words IM2-HW
  referenced as DI/EI (which do not exist anywhere).
- `ISR-OFF` - the correct disable path: di, I=$3F, im 1, ei. The old
  `IM2-HW-DISABLE` only wrote $C0=0, leaving the CPU in im 2 with our
  I register -> first legacy-IM2 ULA interrupt reads table[$FF] beyond
  our 32-byte table and derails.
- `ISR-SAVE-SP`, `ISR-SP0`, `ISR-RP0` - register-save cell and the small
  data/return stacks for the handler's Forth context. Sharing is safe:
  classic ISR-ON mode and hw-IM2 mode are mutually exclusive, and hw IM2
  cannot nest (ints stay disabled until the final ei/reti).
- `(NEXT)` is core: pushes the inner-interpreter address (used by
  ISR-SUB via `ld ix, nn`).

### Dispatch design: per-slot stub + threaded fragment

Mirrors ISR-SUB/ISR-XT/ISR-RET exactly, but per slot.

- `IM2-FRAGS`: 16 entries x 2 cells: `[ handler-xt , ' IM2-HW-RET ]`.
  Handler install = store xt at `IM2-FRAGS + slot*4`. Default `' NOOP`.
- Vector table: `HERE $1F AND ?DUP IF $20 SWAP - ALLOT THEN` then
  `HERE CONSTANT IM2-HW-TABLE  $20 ALLOT` (both fixes: HERE before
  CONSTANT, and the 32 bytes actually reserved). 32-aligned + 32 bytes
  long means it can never cross a 256-byte page.
- Per-slot stub (8 bytes, built with C, via a helper word run 16 times;
  entry address stored into `IM2-HW-TABLE + slot*2`):

      E5              push hl
      21 nn nn        ld hl, IM2-FRAGS + slot*4
      C3 nn nn        jp IM2-COMMON

  Slot 11 (ULA) only: prefix `FF` (rst $38) so the ROM 50Hz housekeeping
  (keyboard scan, FRAMES) keeps running while hw IM2 is active -
  otherwise KEY dies. Same trick as ISR-SUB's first byte.
- `IM2-COMMON` (one raw code blob, address in a CONSTANT):

      F3              di            (rst $38 re-enabled ints; also safe)
      F5 08 F5        push af / ex af,af' / push af
      D5 C5           push de / push bc          (main DE=RSP, BC=IP)
      D9              exx
      E5 D5 C5        push hl / de / bc          (alt set)
      DD E5           push ix
      D9              exx                        (back: HL = fragment)
      44 4D           ld b,h / ld c,l            (IP = fragment)
      ED 73 nn nn     ld (ISR-SAVE-SP), sp
      31 nn nn        ld sp, ISR-SP0
      11 nn nn        ld de, ISR-RP0
      DD 21 nn nn     ld ix, <(NEXT) value>
      DD E9           jp (ix)

- `CODE IM2-HW-RET` (second xt of every fragment) - exact mirror:

      ED 7B nn nn     ld sp, (ISR-SAVE-SP)
      D9              exx
      DD E1           pop ix
      C1 D1 E1        pop bc / de / hl           (alt set)
      D9              exx
      C1 D1           pop bc / de                (main)
      F1 08 F1        pop af / ex af,af' / pop af
      E1              pop hl                     (the stub's push)
      FB              ei
      ED 4D           reti

  reti (not ret): daisy-chain convention for hw IM2.

### Register map (verified on dev guide r3, "Interrupt Enable 0/1/2")

| Slot | Source   | Reg | Bit  | Note                                |
|------|----------|-----|------|-------------------------------------|
| 0    | LINE     | $C4 | 1    |                                     |
| 1    | UART0 Rx | $C6 | 0    | (bit 1 = Rx half full, not used)    |
| 2    | UART1 Rx | $C6 | 4    | (bit 5 = Rx half full, not used)    |
| 3-10 | CTC 0-7  | $C5 | 0-7  | CTC n -> bit n (NOT $C4 $08!)       |
| 11   | ULA      | $C4 | 0    | NOT $80: $C4 bit 7 = expansion bus  |
| 12   | UART0 Tx | $C6 | 2    |                                     |
| 13   | UART1 Tx | $C6 | 6    |                                     |

The old Phase-2 $C6 bits (0,4,2,6) were already correct; Phase-1's ULA
($80) and CTC0 ($C4 $08) were wrong.

$C0 write: `IM2-HW-TABLE $E0 AND 1 OR` - the three top bits of the
table LSB stay AT bits 7:5 (guide: "supplying the top 3 bits of LSB of
the vector table to bits 7-5"), bit 0 = 1 enables hw IM2. The old
`5 RSHIFT` moved them to bits 2:0.

### API (replaces the 56 per-slot words with a slot-map table)

- Keep the `IM2-HW-SLOT-*` constants (0-15, guide priority order).
- `IM2-HW-HANDLER!` ( xt slot -- ) / `IM2-HW-HANDLER@` ( slot -- xt )
- `IM2-HW-ENABLE` / `IM2-HW-DISABLE` ( slot -- ): read-modify-write the
  real register via core REG@/REG! (no shadow caches needed) through a
  16-entry slot->(reg,mask) table; reserved slots map to 0 = no-op.
- `IM2-HW-ON`: ISR-DI; $C4=$01 (ULA only, keeps system alive via the
  rst $38 stub), $C5=0, $C6=0; table MSB SETIREG;
  `IM2-HW-TABLE $E0 AND 1 OR $C0 REG!`; ISR-IM2; ISR-EI.
- `IM2-HW-OFF`: ISR-DI; 0 $C0 REG!; $81 $C4 REG! (reset default:
  expansion bus + ULA); 0 $C5 / 0 $C6; ISR-OFF.
- REG!/REG@ are CORE words - do not redefine them in the lib.
- `MARKER NO-IM2-HW` at top + guard `: IM2-HW ;` as the LAST definition
  (lib/INTERRUPTS.f pattern) so `NEEDS IM2-HW` succeeds only on a full
  load.

### Handler contract (document in lib header)

Handlers run on ISR-SP0/ISR-RP0 (~40 cells): keep them short, no
console I/O, no file access, no MMU7 remapping without save/restore.
Same rules as ISR-XT handlers (tutorial 049).

### Verification plan

Emulator (load-path + structure): table 32-aligned, 16 distinct stub
addresses in the vector table, HANDLER!/HANDLER@ round-trip, REG@
read-back of $C4/$C5/$C6 after ENABLE/DISABLE. `1 $C4 REG! $C4 REG@ .`
confirms the emu NextReg model first. Do NOT call IM2-HW-ON in the
headless emu until its im2/HALT interaction is understood - risk of
killing the REPL keyboard path. Real dispatch (handler fires, counter
increments) only on CSpect, with the tutorial-049-style counter demo.

