#!/usr/bin/env python3
"""
Interactive vForth REPL emulator test
Type Forth words and see results
"""

import sys
import threading
import time
from emulator import VForthEmulator

def run_emulator_thread(emu):
    """Run emulator in background thread"""
    try:
        emu.execute(verbose=False)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"\n[ERROR] {e}")

def interactive_repl():
    """Run interactive Forth REPL"""
    print("=== vForth Interactive Emulator ===")
    print("Loading binaries...\n")

    # Create and initialize emulator
    emu = VForthEmulator()
    emu.max_instructions = 500000
    emu.trace_enabled = False

    try:
        emu.load_binary("project/vForth18_DOES/output/forth18e.bin", 0x6366)
        emu.load_binary("project/vForth18_DOES/output/ram8.bin", 0xE000)
        print("[OK] Binaries loaded\n")
    except FileNotFoundError as e:
        print(f"[ERROR] {e}")
        return

    # Initialize cold start
    emu.initialize_cold_start()
    print(f"Cold start initialized at PC=${emu.cpu.PC:04X}\n")
    print("Type 'quit' to exit, 'help' for info\n")

    # Start emulator in background thread
    emu_thread = threading.Thread(target=run_emulator_thread, args=(emu,), daemon=True)
    emu_thread.start()

    # Interactive loop
    while True:
        try:
            cmd = input("forth> ").strip()

            if cmd.lower() == 'quit':
                print("Exiting...")
                break

            if cmd.lower() == 'help':
                print("""
Interactive vForth REPL Emulator
  Type Forth words and press Enter
  Type 'quit' to exit
  Type 'status' to see CPU state
  Type 'trace N' to show next N instructions
  Type 'memory ADDR LEN' to dump memory
  Type 'stack' to show stack contents
                """)
                continue

            if cmd.lower() == 'status':
                print(f"PC=${emu.cpu.PC:04X}  BC=${emu.cpu.BC:04X}  DE=${emu.cpu.DE:04X}  HL=${emu.cpu.HL:04X}")
                print(f"SP=${emu.cpu.SP:04X}  IX=${emu.cpu.IX:04X}  A=${emu.cpu.A:02X}")
                print(f"Instructions executed: {emu.instr_count}")
                continue

            if cmd.lower().startswith('memory'):
                parts = cmd.split()
                if len(parts) >= 3:
                    try:
                        addr = int(parts[1], 16)
                        length = int(parts[2])
                        print(f"Memory ${addr:04X}-${addr+length:04X}:")
                        for i in range(0, length, 16):
                            bytes_hex = ' '.join(f'{emu.memory[addr+i+j]:02X}' for j in range(min(16, length-i)))
                            ascii_str = ''.join(chr(emu.memory[addr+i+j]) if 32 <= emu.memory[addr+i+j] < 127 else '.' for j in range(min(16, length-i)))
                            print(f"  ${addr+i:04X}  {bytes_hex:47s} | {ascii_str}")
                    except:
                        print("Usage: memory ADDR LEN (hex)")
                continue

            if cmd.lower() == 'stack':
                # Forth data stack is at SP
                sp = emu.cpu.SP
                print(f"Data stack (SP=${sp:04X}):")
                for i in range(16):
                    addr = sp + i*2
                    if addr >= 0xD2F8:
                        break
                    val = emu.memory[addr] | (emu.memory[addr+1] << 8)
                    print(f"  [{i}] ${addr:04X} = ${val:04X}")
                continue

            if not cmd:
                continue

            # For now, just show that input was received
            print(f"[INPUT] {cmd} (emulator running...)")
            print("(Note: Interactive input not yet connected to emulator)")

        except KeyboardInterrupt:
            print("\nInterrupted")
            break
        except EOFError:
            break

    print("Test complete")

if __name__ == "__main__":
    try:
        interactive_repl()
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
