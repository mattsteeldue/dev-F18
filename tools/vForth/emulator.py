#!/usr/bin/env python3
"""
vForth Minimal Emulator - Phase 1
Z80/Z80N emulator for forth18e.bin on headless Python
"""

import sys
import struct
from z80_instructions import INSTRUCTION_MAP, EXTENDED_MAP, IX_INSTRUCTION_MAP


class Z80CPU:
    """Z80 CPU state and instruction decoder"""

    def __init__(self, memory):
        self.mem = memory

        # Main registers (16-bit pairs)
        self.BC = 0  # B=high, C=low (IP on vForth)
        self.DE = 0  # D=high, E=low (RP on vForth)
        self.HL = 0  # H=high, L=low (W register)
        self.IX = 0  # Index X register
        self.IY = 0  # Index Y register

        # Stack pointer and program counter
        self.SP = 0  # Stack pointer (grows downward)
        self.PC = 0  # Program counter

        # Accumulator and flags
        self.A = 0
        self.F = 0  # Flags: S Z - H - P/V N C

        # Alternate registers (not commonly used)
        self.BC_alt = 0
        self.DE_alt = 0
        self.HL_alt = 0
        self.A_alt = 0
        self.F_alt = 0

        # Internal state
        self.halted = False
        self.cycle_count = 0

        # MMU state
        self.mmu7_page = 0x20  # Current heap page (initially page 32)

    # Register access (8-bit)
    @property
    def B(self): return (self.BC >> 8) & 0xFF
    @B.setter
    def B(self, v): self.BC = (self.BC & 0xFF) | ((v & 0xFF) << 8)

    @property
    def C(self): return self.BC & 0xFF
    @C.setter
    def C(self, v): self.BC = (self.BC & 0xFF00) | (v & 0xFF)

    @property
    def D(self): return (self.DE >> 8) & 0xFF
    @D.setter
    def D(self, v): self.DE = (self.DE & 0xFF) | ((v & 0xFF) << 8)

    @property
    def E(self): return self.DE & 0xFF
    @E.setter
    def E(self, v): self.DE = (self.DE & 0xFF00) | (v & 0xFF)

    @property
    def H(self): return (self.HL >> 8) & 0xFF
    @H.setter
    def H(self, v): self.HL = (self.HL & 0xFF) | ((v & 0xFF) << 8)

    @property
    def L(self): return self.HL & 0xFF
    @L.setter
    def L(self, v): self.HL = (self.HL & 0xFF00) | (v & 0xFF)

    @property
    def IXH(self): return (self.IX >> 8) & 0xFF
    @IXH.setter
    def IXH(self, v): self.IX = (self.IX & 0xFF) | ((v & 0xFF) << 8)

    @property
    def IXL(self): return self.IX & 0xFF
    @IXL.setter
    def IXL(self, v): self.IX = (self.IX & 0xFF00) | (v & 0xFF)

    # Memory access (16-bit little-endian)
    def mem16_le(self, addr):
        """Read 16-bit little-endian from memory"""
        return self.mem[addr] | (self.mem[(addr + 1) & 0xFFFF] << 8)

    def mem16_le_set(self, addr, val):
        """Write 16-bit little-endian to memory"""
        self.mem[addr] = val & 0xFF
        self.mem[(addr + 1) & 0xFFFF] = (val >> 8) & 0xFF

    def fetch_byte(self):
        """Fetch next instruction byte and advance PC"""
        b = self.mem[self.PC]
        self.PC = (self.PC + 1) & 0xFFFF
        return b

    def push(self, val):
        """Push 16-bit value onto stack"""
        self.SP = (self.SP - 2) & 0xFFFF
        self.mem16_le_set(self.SP, val)

    def pop(self):
        """Pop 16-bit value from stack"""
        val = self.mem16_le(self.SP)
        self.SP = (self.SP + 2) & 0xFFFF
        return val


class VForthEmulator:
    """vForth emulator with memory, CPU, and instruction dispatch"""

    def __init__(self):
        # Initialize 64 KB flat memory
        self.memory = bytearray(0x10000)
        self.cpu = Z80CPU(self.memory)

        # Instruction count for logging
        self.instr_count = 0
        self.max_instructions = 1000000  # Safety limit

    def load_binary(self, filename, address):
        """Load binary file into memory at given address"""
        with open(filename, "rb") as f:
            data = f.read()

        if address + len(data) > 0x10000:
            raise ValueError(f"Binary too large for address ${address:04X}")

        self.memory[address:address + len(data)] = data
        print(f"Loaded {len(data)} bytes from {filename} at ${address:04X}")

    def load_low_bin(self, filename):
        """Load low.bin: extract payload (skip 128-byte TAP header)"""
        with open(filename, "rb") as f:
            data = f.read()

        if len(data) < 128:
            raise ValueError("low.bin too small")

        payload = data[128:]  # Skip TAP header
        if len(payload) != 1792:
            raise ValueError(f"Expected 1792 bytes payload, got {len(payload)}")

        self.memory[0x5B00:0x5B00 + 1792] = payload
        print(f"Loaded low.bin payload (1792 bytes) at $5B00")

    def initialize_cold_start(self):
        """Set up CPU state for COLD start"""
        # From small_emulator.md section 7
        S0 = 0xD2F8
        R0 = 0xD398
        Next_Ptr = self.find_next_ptr()

        self.cpu.SP = S0
        self.cpu.DE = R0
        self.cpu.BC = self.find_cold_start()
        self.cpu.IX = Next_Ptr
        self.cpu.PC = Next_Ptr  # Start execution at inner interpreter

        print(f"Cold start: SP=${self.cpu.SP:04X}, DE=${self.cpu.DE:04X}, BC=${self.cpu.BC:04X}, IX=${self.cpu.IX:04X}, PC=${self.cpu.PC:04X}")

    def find_next_ptr(self):
        """Scan binary for Next_Ptr pattern (inner interpreter)"""
        # Pattern: 0A (ld a,(bc)) followed by 03 (inc bc)
        ORIGIN = 0x6366
        pattern = b'\x0A\x03'
        for i in range(ORIGIN, min(ORIGIN + 0x1000, 0x10000 - 1)):
            if self.memory[i:i+2] == pattern:
                return i
        print("Warning: Next_Ptr pattern not found, using default")
        return ORIGIN + 0x086

    def find_cold_start(self):
        """Find Cold_Start address in binary"""
        # Cold_Start is referenced from ColdRoutine
        # Look for the entry point; typically early in the code
        ORIGIN = 0x6366
        # For now, assume it's at ORIGIN + 2 (after Warm_Start entry)
        # This will be verified when we trace execution
        return ORIGIN + 2

    def execute(self, verbose=False):
        """Fetch-decode-execute loop"""
        print("\n=== Starting Cold Start ===\n")

        while not self.cpu.halted and self.instr_count < self.max_instructions:
            self.instr_count += 1

            # Fetch opcode
            pc_before = self.cpu.PC
            opcode = self.cpu.fetch_byte()

            if verbose:
                print(f"[{self.instr_count:6d}] ${pc_before:04X}: 0x{opcode:02X}  BC=${self.cpu.BC:04X} DE=${self.cpu.DE:04X} HL=${self.cpu.HL:04X}")

            # Decode and execute
            try:
                self.dispatch(opcode)
            except StopIteration:
                print(f"Halted at instruction {self.instr_count}")
                break
            except Exception as e:
                print(f"Error at PC ${pc_before:04X}: {e}")
                import traceback
                traceback.print_exc()
                break

        print(f"\n=== Stopped after {self.instr_count} instructions ===")

    def dispatch(self, opcode):
        """Main instruction dispatcher"""
        if opcode == 0xED:
            # Extended instruction
            ext_opcode = self.cpu.fetch_byte()
            if ext_opcode in EXTENDED_MAP:
                EXTENDED_MAP[ext_opcode](self.cpu)
            elif ext_opcode == 0xB0:  # LDIR/LDDR - skip for now
                pass
            else:
                if self.instr_count < 10:  # Only warn on early instructions
                    print(f"Unimplemented extended instruction: 0xED 0x{ext_opcode:02X}")

        elif opcode == 0xDD:
            # IX instruction
            ix_opcode = self.cpu.fetch_byte()
            if ix_opcode in IX_INSTRUCTION_MAP:
                IX_INSTRUCTION_MAP[ix_opcode](self.cpu)
            else:
                if self.instr_count < 10:
                    print(f"Unimplemented IX instruction: 0xDD 0x{ix_opcode:02X}")

        elif opcode == 0xCB:
            # Bit operations - skip for now
            self.cpu.fetch_byte()

        elif opcode == 0xFD:
            # IY instruction - skip for now
            self.cpu.fetch_byte()

        elif opcode in INSTRUCTION_MAP:
            INSTRUCTION_MAP[opcode](self.cpu)

        else:
            # Unknown instruction - try to skip operands intelligently
            if self.instr_count < 20:
                print(f"Unimplemented instruction: 0x{opcode:02X} at PC ${self.cpu.PC - 1:04X}")


def main():
    max_instr = 1000000
    verbose = False

    # Parse arguments
    for arg in sys.argv[1:]:
        if arg == "--verbose" or arg == "-v":
            verbose = True
        else:
            try:
                max_instr = int(arg)
            except ValueError:
                pass

    emulator = VForthEmulator()
    emulator.max_instructions = max_instr

    # Load binaries
    try:
        emulator.load_low_bin("low.bin")
        emulator.load_binary("project/vForth18_DOES/output/forth18e.bin", 0x6366)
        emulator.load_binary("project/vForth18_DOES/output/ram8.bin", 0xE000)
    except FileNotFoundError as e:
        print(f"Error loading binaries: {e}")
        sys.exit(1)

    # Initialize cold start
    emulator.initialize_cold_start()

    # Run
    emulator.execute(verbose=verbose)


if __name__ == "__main__":
    main()
