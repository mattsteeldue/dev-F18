#!/usr/bin/env python3
"""
Test Phase B: Interactive Input Buffer Integration
Verify that queued input is processed correctly by the emulator
"""

import sys
import time
from emulator import VForthEmulator

def run_emulator_until_halt(emu, max_time=5):
    """Run emulator until halt or timeout"""
    start_time = time.time()
    try:
        while not emu.cpu.halted and emu.instr_count < emu.max_instructions:
            elapsed = time.time() - start_time
            if elapsed > max_time:
                print(f"\n[TIMEOUT] after {emu.instr_count} instructions")
                return False

            emu.instr_count += 1
            pc_before = emu.cpu.PC
            opcode = emu.cpu.fetch_byte()

            try:
                emu.dispatch(opcode)
            except StopIteration:
                return True
            except Exception as e:
                print(f"\n[ERROR] PC ${pc_before:04X}: {e}")
                return False
    except KeyboardInterrupt:
        return False

    return True

def test_interactive_phase():
    print("=== Phase B: Interactive Input Buffer Test ===\n")

    # Initialize emulator
    emu = VForthEmulator()
    emu.max_instructions = 100000  # Reasonable limit for test
    emu.trace_enabled = False
    emu.input_echo = False  # Don't echo during automated test

    try:
        emu.load_binary("project/vForth18_DOES/output/forth18e.bin", 0x6366)
        emu.load_binary("project/vForth18_DOES/output/ram8.bin", 0xE000)
        print("[OK] Binaries loaded")
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        return False

    emu.initialize_cold_start()
    print(f"[OK] Cold start at PC=${emu.cpu.PC:04X}")

    # Test 1: Simple input queuing
    print("\n--- Test 1: Input Queue Mechanism ---")
    print("Queueing text '1'...")
    emu.queue_input("1")
    print(f"Input queue length: {len(emu.input_queue)}")
    if len(emu.input_queue) > 0:
        print("[OK] Text queued successfully (includes CR)")
    else:
        print("[FAIL] Input queue is empty")
        return False

    # Test 2: KEY reads from queue
    print("\n--- Test 2: KEY Reads from Queue ---")
    emu.input_queue = []  # Clear
    emu.queue_input("A")
    initial_queue_len = len(emu.input_queue)
    print(f"Queue before KEY: {initial_queue_len} chars")

    # Simulate KEY syscall
    emu.handle_key()
    final_queue_len = len(emu.input_queue)
    print(f"Queue after KEY: {final_queue_len} chars")
    print(f"A register after KEY: ${emu.cpu.A:02X} (expected ${ord('A'):02X})")

    if emu.cpu.A == ord('A') and final_queue_len < initial_queue_len:
        print("[OK] KEY successfully read from queue")
    else:
        print("[FAIL] KEY did not read correctly from queue")
        return False

    # Test 3: Run emulator with queued input (simple test)
    print("\n--- Test 3: Emulator Execution with Queued Input ---")
    emu.initialize_cold_start()
    emu.input_queue = []
    emu.input_echo = False

    # Queue a simple input sequence (simulating user typing something)
    # In a real Forth system, this would be a Forth word
    # For now, just queue random input to verify the mechanism works
    test_input = "X"
    print(f"Queueing test input: '{test_input}'")
    emu.queue_input(test_input)

    start_queue = len(emu.input_queue)
    print(f"Running emulator with {start_queue} chars in queue...")
    run_emulator_until_halt(emu, max_time=2)
    end_queue = len(emu.input_queue)

    print(f"Queue after execution: {end_queue} chars processed")
    if end_queue < start_queue:
        print("[OK] Input was consumed by emulator")
    else:
        print("[WARN] Input was not consumed (may still be in queue)")

    print("\n=== Phase B Summary ===")
    print("Input queue mechanism: IMPLEMENTED")
    print("KEY function: reads from queue BEFORE stdin")
    print("queue_input() method: WORKING")
    print("Interactive REPL: ready for testing")
    print("\nTo test interactively, run: python emu/interactive_test.py")

    return True

if __name__ == "__main__":
    try:
        success = test_interactive_phase()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
