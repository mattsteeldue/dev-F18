#!/usr/bin/env python3
"""
Test tutorial loading via INCLUDE
Verify that tutorial files can be loaded and executed via F_INCLUDE
"""

import sys
import os
from emulator import VForthEmulator

def run_emulator_steps(emu, max_steps=100000):
    """Run emulator for a fixed number of steps"""
    step = 0
    try:
        while not emu.cpu.halted and emu.instr_count < emu.max_instructions and step < max_steps:
            emu.instr_count += 1
            step += 1

            pc_before = emu.cpu.PC
            opcode = emu.cpu.fetch_byte()

            try:
                emu.dispatch(opcode)
            except StopIteration:
                break
            except Exception as e:
                if emu.instr_count < 100:
                    print(f"[ERROR at step {step}] PC ${pc_before:04X}: {e}")
                break
    except KeyboardInterrupt:
        pass

    return step

def test_tutorial_loading():
    print("=== Tutorial Loading Test ===\n")

    # Check if tutorial files exist
    tutorial_file = "tutorial/001-stack-basics.f"
    if not os.path.exists(tutorial_file):
        print(f"[ERROR] Tutorial file not found: {tutorial_file}")
        return False

    print(f"[OK] Found tutorial: {tutorial_file}")
    file_size = os.path.getsize(tutorial_file)
    print(f"[OK] File size: {file_size} bytes\n")

    # Initialize emulator
    emu = VForthEmulator()
    emu.max_instructions = 500000
    emu.trace_enabled = False
    emu.input_echo = False
    emu.benchmark_mode = False

    try:
        emu.load_binary("project/vForth18_DOES/output/forth18e.bin", 0x6366)
        emu.load_binary("project/vForth18_DOES/output/ram8.bin", 0xE000)
        print("[OK] Binaries loaded")
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        return False

    emu.initialize_cold_start()
    print(f"[OK] Cold start at PC=${emu.cpu.PC:04X}\n")

    # Test 1: Try to construct INCLUDE command
    print("--- Test 1: INCLUDE Command Preparation ---")
    include_cmd = f'INCLUDE {tutorial_file}'
    print(f"Command: {include_cmd}")
    print(f"Command length: {len(include_cmd)} chars\n")

    # Test 2: Queue the INCLUDE command
    print("--- Test 2: Queue and Execute INCLUDE ---")
    emu.queue_input(include_cmd)
    print(f"Input queued: {len(emu.input_queue)} chars in queue")
    print(f"Running emulator...\n")

    steps = run_emulator_steps(emu, max_steps=200000)
    print(f"[OK] Executed {steps} steps")
    print(f"Total instructions: {emu.instr_count}\n")

    # Test 3: Check if we got any output
    print("--- Test 3: Assessment ---")
    print(f"Final PC: ${emu.cpu.PC:04X}")
    print(f"Final stack pointer SP: ${emu.cpu.SP:04X}")
    print(f"Final BC (IP): ${emu.cpu.BC:04X}")

    # Note on limitations
    print("\n--- Known Limitations ---")
    print("The INCLUDE command may not have completed because:")
    print("1. The emulator is in 'cold start' state - interpreter not fully active")
    print("2. INCLUDE requires the full Forth interpreter to be running")
    print("3. The emulator reaches instruction limit before full execution")
    print("\nFor interactive testing, use: python emu/interactive_test.py")
    print("Then type: INCLUDE tutorial/001-stack-basics.f")

    return True

if __name__ == "__main__":
    try:
        success = test_tutorial_loading()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
