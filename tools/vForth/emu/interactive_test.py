#!/usr/bin/env python3
"""
Interactive vForth REPL emulator test
Type Forth words and see results
"""

import sys
import time
from emulator import VForthEmulator

def run_emulator_with_timeout(emu, timeout=15):
    """Run emulator for up to timeout seconds or until it halts"""
    start_time = time.time()

    try:
        while not emu.cpu.halted and emu.instr_count < emu.max_instructions:
            elapsed = time.time() - start_time
            if elapsed > timeout:
                print(f"\n[TIMEOUT] Execution took >{timeout}s, stopping")
                break

            emu.instr_count += 1

            # Fetch and execute
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
        pass

def interactive_repl():
    """Run interactive Forth REPL"""
    print("=== vForth Interactive Emulator (Phase B) ===")
    print("Loading binaries...\n")

    # Create and initialize emulator
    emu = VForthEmulator()
    emu.max_instructions = 500000
    emu.trace_enabled = False
    emu.input_echo = True

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
    print("Type Forth words and press Enter")
    print("Commands: 'quit' to exit, 'reset' to reinit, 'status' for CPU state")
    print("\nNOTE: Use forward slashes in paths (e.g. INCLUDE tutorial/001-stack-basics.f)")
    print("Execution timeout: 15 seconds per command\n")

    # Main REPL loop
    while True:
        try:
            cmd = input("forth> ").strip()

            if cmd.lower() == 'quit':
                print("Exiting...")
                break

            if cmd.lower() == 'reset':
                print("Reinitializing emulator...")
                emu.initialize_cold_start()
                continue

            if cmd.lower() == 'status':
                print(f"PC=${emu.cpu.PC:04X}  BC=${emu.cpu.BC:04X}  DE=${emu.cpu.DE:04X}  HL=${emu.cpu.HL:04X}")
                print(f"SP=${emu.cpu.SP:04X}  IX=${emu.cpu.IX:04X}  A=${emu.cpu.A:02X}")
                print(f"Instructions executed: {emu.instr_count}")
                continue

            if cmd.lower() == 'help':
                print("""
Interactive vForth REPL Emulator (Phase B)
Commands:
  <forth-word> ... -- Execute Forth words
  'reset'          -- Reinitialize emulator
  'status'         -- Show CPU state
  'memory ADDR N'  -- Dump N bytes at address (hex)
  'stack'          -- Show data stack
  'quit'           -- Exit emulator
                """)
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
                        print("Usage: memory ADDR LEN (both hex)")
                continue

            if cmd.lower() == 'stack':
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

            # Execute Forth command
            print(f"Executing: {cmd}")
            sys.stdout.flush()
            emu.queue_input(cmd)
            instr_before = emu.instr_count
            run_emulator_with_timeout(emu, timeout=15)
            instr_executed = emu.instr_count - instr_before
            if instr_executed > 0:
                print(f"\n[OK] Executed {instr_executed} instructions")
            print()  # Blank line for readability

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
