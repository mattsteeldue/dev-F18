# vForth Minimal Emulator

A headless Z80/Z80N emulator for the vForth compiler system, targeting the Sinclair ZX Spectrum Next.

## Overview

This emulator implements the complete vForth runtime in Python with:
- **Phase 1**: Z80/Z80N CPU emulation (150+ instructions)
- **Phase 2**: Terminal I/O (KEY, EMIT, CLS)
- **Phase 3**: Complete File I/O (F_OPEN, F_CLOSE, F_READ, F_WRITE, F_SEEK, etc.)
- **Phase B**: Interactive REPL with input queue
- **Phase C**: Session recording/transcripts
- **Phase D**: Performance benchmarking

## Files

| File | Purpose |
|------|---------|
| `emulator.py` | Main emulator class (VForthEmulator, Z80CPU) |
| `z80_instructions.py` | 150+ Z80/Z80N instruction implementations |
| `interactive_test.py` | Interactive Forth REPL for manual testing |
| `test_emulator.py` | Basic startup test (1,000 instructions) |
| `test_extended.py` | Stress test (100,000 instructions) |
| `test_include_phase.py` | Phase A verification |
| `test_interactive_phase.py` | Phase B automated test |
| `test_session_recording.py` | Phase C session recording test |
| `test_benchmarking.py` | Phase D performance measurement |
| `test_include.f` | Sample Forth file for INCLUDE testing |

## Quick Start

### Interactive REPL (Phase B)

```bash
python emu/interactive_test.py
```

This launches an interactive Forth prompt where you can type Forth words:
```
forth> 1 2 + .
[Emulator executes the command and shows output]

forth> quit
```

Commands available:
- `<word> ...` — Execute Forth words
- `reset` — Reinitialize emulator
- `status` — Show CPU state (PC, registers, instruction count)
- `memory ADDR LEN` — Dump memory (both hex)
- `stack` — Show data stack contents
- `help` — Show available commands
- `quit` — Exit

### Run Tests

```bash
# Basic startup test
python emu/test_emulator.py

# Extended 100K instruction test
python emu/test_extended.py

# Phase B: Interactive input
python emu/test_interactive_phase.py

# Phase C: Session recording
python emu/test_session_recording.py

# Phase D: Performance benchmark
python emu/test_benchmarking.py
```

## Architecture

### Memory Layout
- **Origin**: $6366 (binary loaded at startup)
- **Heap**: $E000-$FFFF (MMU7 page)
- **Stack areas**: Below $E000
  - S0 (data stack): $D2F8
  - R0 (return stack): $D398
  - TIB (terminal input buffer): dynamic

### Z80 Register Map (vForth Convention)
| Register | Purpose |
|----------|---------|
| BC | Instruction Pointer (IP) |
| DE | Return Stack Pointer (RP) |
| HL | Working register (W) |
| SP | Calculation stack pointer |
| IX | Inner interpreter "next" pointer |
| IY | Reserved for system interrupts |

## Features

### Phase A: File I/O & INCLUDE Support
The emulator provides complete file I/O primitives used by vForth's `F_INCLUDE` word:
- `F_OPEN`, `F_CLOSE`, `F_READ`, `F_WRITE`
- `F_SEEK`, `F_FGETPOS`, `F_SYNC`
- `F_OPENDIR`, `F_READDIR`

F_GETLINE (used by INCLUDE) is implemented as a Forth vocabulary word that calls these primitives.

### Phase B: Interactive Input Buffer
User commands are queued for processing character-by-character:
```python
emu.queue_input("1 2 +")  # Queue command
emu.handle_key()          # KEY primitive reads from queue
```

The `interactive_test.py` REPL integrates this for interactive Forth session.

### Phase C: Session Recording
Capture full I/O transcripts for documentation:
```python
emu.start_session_recording("session.txt")
# ... run commands ...
emu.stop_session_recording()
```

Output format:
```
=== vForth Session Transcript ===
Started: <timestamp>

[0.000234] input : '1'
[0.000456] output: '3'
```

### Phase D: Performance Benchmarking
Measure emulator speed and identify bottlenecks:
```python
emu.start_benchmark()
# ... run test ...
emu.stop_benchmark()
emu.print_trace_report()  # Shows instructions/sec, hottest addresses
```

**Baseline Performance:**
- Speed: 1,224,757 instructions/second
- Per-instruction time: 0.001 ms average
- Memory: 64 KB flat address space

## Implementation Details

### Direct Threading
vForth uses direct-threaded code for ~25% speed improvement:
- Low-level words: CFA contains actual Z80 machine code
- High-level words: CFA contains `call Enter_Ptr`

### NextZXOS Syscalls
File I/O and terminal I/O are routed via NextZXOS syscalls (RST 08 + function byte):
- Terminal I/O: function 0x94
- File I/O: functions 0x9A-0xA4

### Memory Paging (MMU7)
The heap dictionary lives at $E000-$FFFF in an MMU7 page. The emulator simulates page access via memory address remapping.

## Known Limitations

1. **Interactive INCLUDE**: INCLUDE/NEEDS work in principle but require the full Forth interpreter to be active
2. **Block I/O**: Screens/blocks are not yet integrated
3. **Debugging**: Limited to instruction trace and register inspection
4. **Performance**: Emulator is fast (1.2M instr/sec) but still 50-100x slower than real hardware
5. **Directory listing (`DIR` / `WILDCARD`) is not modelled**: `handle_f_opendir`
   ignores the mode byte in `B` (so `esx_mode_use_wildcards`, the `$30` the core
   passes, has no effect) and `handle_f_readdir` ignores the pattern in `DE` and
   returns the bare entry name + NUL, not the NextZXOS record (attributes, time,
   date, size) that `lib/DIR.f`'s `DIR-LIST-ITEM` decodes. A headless
   `WILDCARD *.F` + `DIR` therefore proves nothing: the filter is a no-op and the
   listing is misparsed. **`DIR` and `WILDCARD` can only be verified on CSpect or
   real hardware** (see `test/DIR-WILDCARD-MANUAL.f`).

## Building & Maintenance

The emulator works with binaries from:
- `project/vForth18_DOES/output/forth18e.bin` (main binary)
- `project/vForth18_DOES/output/ram8.bin` (RAM initialization)

If you modify the vForth core assembler, rebuild with SjASMPlus and the emulator will automatically work with the new binary.

## Future Enhancements

- Block/Screen support for full LOAD compatibility
- Debugging UI (breakpoints, single-step)
- Profiling tools (call graph, memory allocations)
- Head-less automation (run Forth scripts from command line)
