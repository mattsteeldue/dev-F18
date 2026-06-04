#!/usr/bin/env python3
"""
Test Phase D: Performance Benchmarking & Enhanced Tracing
Measure emulator speed and identify bottleneck addresses
"""

import sys
from emulator import VForthEmulator

def run_benchmark(emu, max_instructions=100000):
    """Run emulator in benchmark mode"""
    emu.start_benchmark()
    print(f"Running benchmark ({max_instructions} instructions max)...")

    try:
        while not emu.cpu.halted and emu.instr_count < max_instructions:
            emu.instr_count += 1
            pc_before = emu.cpu.PC
            opcode = emu.cpu.fetch_byte()

            try:
                emu.dispatch(opcode)
            except StopIteration:
                break
            except Exception as e:
                print(f"\n[ERROR] PC ${pc_before:04X}: {e}")
                break
    except KeyboardInterrupt:
        print("\nBenchmark interrupted")

    wall_time = emu.stop_benchmark()
    return wall_time

def test_benchmarking():
    print("=== Phase D: Performance Benchmarking Test ===\n")

    # Initialize emulator
    emu = VForthEmulator()
    emu.max_instructions = 500000
    emu.trace_enabled = False
    emu.benchmark_mode = False

    try:
        emu.load_binary("project/vForth18_DOES/output/forth18e.bin", 0x6366)
        emu.load_binary("project/vForth18_DOES/output/ram8.bin", 0xE000)
        print("[OK] Binaries loaded")
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        return False

    emu.initialize_cold_start()
    print(f"[OK] Cold start initialized\n")

    # Run benchmark with a reasonable limit
    print("--- Benchmark Run ---")
    wall_time = run_benchmark(emu, max_instructions=100000)

    # Print detailed report
    print("\n--- Performance Analysis ---")
    if wall_time > 0:
        instr_per_sec = emu.instr_count / wall_time
        print(f"\nExecution Summary:")
        print(f"  Total instructions: {emu.instr_count:,}")
        print(f"  Wall-clock time: {wall_time:.3f} seconds")
        print(f"  Speed: {instr_per_sec:,.0f} instructions/second")
        print(f"  Avg time per instruction: {1000*wall_time/emu.instr_count:.3f} ms")
    else:
        print("No timing data available")

    print(f"\n--- Hottest Addresses (Top 10) ---")
    sorted_pcs = sorted(emu.pc_histogram.items(), key=lambda x: x[1], reverse=True)
    for i, (pc, count) in enumerate(sorted_pcs[:10]):
        pct = 100.0 * count / emu.instr_count if emu.instr_count > 0 else 0
        print(f"  {i+1:2d}. ${pc:04X}: {count:8,d} times ({pct:5.1f}%)")

    print(f"\n--- Loop Detection ---")
    if emu.loop_detector:
        print(f"Potential tight loops detected:")
        for pc in list(emu.loop_detector.keys())[:5]:
            delta = emu.instr_count - emu.loop_detector[pc]
            if delta > 0:
                print(f"  PC ${pc:04X}: repeats every ~{delta} instructions")
    else:
        print("No loop patterns detected")

    print(f"\n--- Memory Usage ---")
    print(f"  Total memory: 64 KB (65,536 bytes)")
    print(f"  Memory used: {len(emu.memory)} bytes")

    # Call the built-in trace report with performance metrics
    print("\n--- Full Trace Report (with Phase D metrics) ---")
    emu.print_trace_report()

    return True

if __name__ == "__main__":
    try:
        success = test_benchmarking()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
