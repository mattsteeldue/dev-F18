#!/usr/bin/env python3
"""
Test vForth emulator with basic startup sequence
"""

import sys
from emulator import VForthEmulator

def test_emulator():
    """Test emulator initialization and execution"""
    print("=== vForth Emulator Test ===\n")

    # Create emulator
    emu = VForthEmulator()

    # Load binaries
    print("1. Loading binaries...")
    try:
        emu.load_binary("project/vForth18_DOES/output/forth18e.bin", 0x6366)
        print("   [OK] forth18e.bin loaded")
    except FileNotFoundError as e:
        print(f"   [FAIL] forth18e.bin not found: {e}")
        return False

    try:
        emu.load_binary("project/vForth18_DOES/output/ram8.bin", 0xE000)
        print("   [OK] ram8.bin loaded")
    except FileNotFoundError as e:
        print(f"   [FAIL] ram8.bin not found: {e}")
        return False

    try:
        emu.load_low_bin("tools/low.bin")
        print("   [OK] low.bin loaded")
    except FileNotFoundError as e:
        print(f"   [INFO] low.bin not found (optional): {e}")
        print("   Using default system variables...")

    # Initialize cold start
    print("\n2. Initializing cold start...")
    emu.initialize_cold_start()
    print(f"   PC=${emu.cpu.PC:04X}  BC=${emu.cpu.BC:04X}  DE=${emu.cpu.DE:04X}")
    print(f"   SP=${emu.cpu.SP:04X}  IX=${emu.cpu.IX:04X}")

    # Execute for a limited number of instructions
    print("\n3. Executing for 1000 instructions...")
    emu.max_instructions = 1000

    try:
        emu.execute(verbose=False)
        print(f"\n[OK] Emulator executed {emu.instr_count} instructions without crash")
        return True
    except KeyboardInterrupt:
        print(f"\n[INFO] Interrupted after {emu.instr_count} instructions")
        return True
    except Exception as e:
        print(f"\n[FAIL] Emulator error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_emulator()
    sys.exit(0 if success else 1)
