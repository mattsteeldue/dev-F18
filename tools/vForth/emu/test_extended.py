#!/usr/bin/env python3
"""
Extended vForth emulator test - run for 100,000 instructions and capture output
"""

import sys
import io
from emulator import VForthEmulator

class CaptureOutput:
    """Capture stdout for Forth EMIT operations"""
    def __init__(self):
        self.output = []

    def write(self, char):
        self.output.append(char)

    def flush(self):
        pass

    def get_text(self):
        return ''.join(self.output)

def test_extended():
    """Run extended test with 100,000 instructions"""
    print("=== vForth Extended Execution Test ===\n")

    # Create emulator
    emu = VForthEmulator()
    emu.max_instructions = 100000
    emu.trace_enabled = False

    print("1. Loading binaries...")
    try:
        emu.load_binary("project/vForth18_DOES/output/forth18e.bin", 0x6366)
        emu.load_binary("project/vForth18_DOES/output/ram8.bin", 0xE000)
        print("   [OK] Both binaries loaded\n")
    except FileNotFoundError as e:
        print(f"   [FAIL] {e}")
        return False

    print("2. Initializing cold start...")
    emu.initialize_cold_start()
    print(f"   PC=${emu.cpu.PC:04X}  BC=${emu.cpu.BC:04X}  DE=${emu.cpu.DE:04X}")
    print(f"   SP=${emu.cpu.SP:04X}  IX=${emu.cpu.IX:04X}\n")

    print("3. Capturing output and executing 100,000 instructions...\n")

    # Capture EMIT output
    captured = CaptureOutput()
    original_stdout = sys.stdout

    try:
        # Temporarily redirect stdout
        sys.stdout = io.StringIO()

        # Run emulator
        emu.execute(verbose=False)

        # Restore stdout
        sys.stdout = original_stdout

        print(f"   Executed {emu.instr_count} instructions\n")

    except Exception as e:
        sys.stdout = original_stdout
        print(f"   [ERROR] {e}")
        return False

    print("4. Execution Report:")
    print(f"   Total instructions: {emu.instr_count:,}")
    print(f"   Halted: {emu.cpu.halted}")
    print(f"   Final PC: ${emu.cpu.PC:04X}")
    print(f"   Final BC (IP): ${emu.cpu.BC:04X}")
    print(f"   Final DE (RP): ${emu.cpu.DE:04X}")
    print(f"   Final HL: ${emu.cpu.HL:04X}")
    print(f"   Final SP: ${emu.cpu.SP:04X}\n")

    print("5. Most-executed addresses (top 10):")
    sorted_pcs = sorted(emu.pc_histogram.items(), key=lambda x: x[1], reverse=True)[:10]
    for pc, count in sorted_pcs:
        pct = 100.0 * count / emu.instr_count
        print(f"   ${pc:04X}: {count:8d} times ({pct:5.1f}%)")

    print(f"\n[OK] Extended test completed successfully")
    return True

if __name__ == "__main__":
    success = test_extended()
    sys.exit(0 if success else 1)
