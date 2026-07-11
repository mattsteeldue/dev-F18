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

