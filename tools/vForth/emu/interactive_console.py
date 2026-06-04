#!/usr/bin/env python3
"""
Interactive vForth Console - Real Display Emulation
Captures EMIT output and shows it on console, input via keyboard
"""

import sys
import time
from emulator import VForthEmulator

class ConsoleDisplay:
    """Emulate vForth console display (output buffer)"""

    def __init__(self, width=80, height=25):
        self.width = width
        self.height = height
        self.output_buffer = ""
        self.line_count = 0

    def emit(self, char):
        """Handle EMIT output"""
        if char == '\r':  # CR - carriage return
            self.output_buffer += '\n'
            self.line_count += 1
        elif char == '\n':  # LF - line feed (vForth usually uses CR)
            pass  # Skip extra LF
        elif 32 <= ord(char) < 127 or char == '\t':  # Printable ASCII + tab
            self.output_buffer += char
        else:
            # Non-printable, show as [XX]
            self.output_buffer += f"[{ord(char):02X}]"

    def get_output(self):
        """Get and clear output buffer"""
        result = self.output_buffer
        self.output_buffer = ""
        return result

    def display(self):
        """Show current output"""
        output = self.get_output()
        if output:
            sys.stdout.write(output)
            sys.stdout.flush()

def run_emulator_steps(emu, display, max_steps=500000):
    """Run emulator and display output in real-time"""
    step = 0
    try:
        while step < max_steps and not emu.cpu.halted:
            emu.instr_count += 1
            step += 1

            opcode = emu.cpu.fetch_byte()

            try:
                emu.dispatch(opcode)
            except StopIteration:
                display.display()
                return True
            except Exception as e:
                display.display()
                print(f"\n[ERROR] {e}")
                return False

            # Show output every 100 instructions (more responsive)
            if step % 100 == 0:
                display.display()

    except KeyboardInterrupt:
        display.display()
        print("\n[Interrupted by user]")
        return False

    display.display()
    return False

def main():
    print("=== vForth Console Emulator ===\n")
    print("Loading binaries...", end="", flush=True)

    # Initialize emulator
    emu = VForthEmulator()
    emu.max_instructions = 5000000
    emu.trace_enabled = False
    emu.input_echo = False  # We'll handle display ourselves
    emu.benchmark_mode = False

    # Create console display
    display = ConsoleDisplay()

    # Override EMIT to capture output
    original_emit = emu.handle_emit
    def emit_with_display():
        char = chr(emu.cpu.A & 0xFF)
        display.emit(char)
        original_emit()
    emu.handle_emit = emit_with_display

    try:
        emu.load_binary("project/vForth18_DOES/output/forth18e.bin", 0x6366)
        emu.load_binary("project/vForth18_DOES/output/ram8.bin", 0xE000)
        print(" OK\n")
    except FileNotFoundError as e:
        print(f" FAILED\n[ERROR] {e}")
        return

    # Initialize cold start
    emu.initialize_cold_start()
    print("vForth initialized.\n")
    print("=" * 60)
    print()

    # Run cold start sequence to let vForth show its banner
    print("Starting vForth...\n", end="", flush=True)
    run_emulator_steps(emu, display, max_steps=50000)

    print("\n" + "=" * 60)
    print("\nCommands:")
    print("  Type Forth words (e.g. '42 .')")
    print("  Type 'quit' to exit")
    print("  Type 'reset' to reinit")
    print("  Type 'status' for CPU state")
    print("\nUse forward slashes in paths: INCLUDE tutorial/001-stack-basics.f\n")

    # Main REPL loop
    while True:
        try:
            cmd = input(">>> ").strip()

            if cmd.lower() == 'quit':
                print("Exiting vForth Console.")
                break

            if cmd.lower() == 'reset':
                print("Reinitializing...")
                emu.initialize_cold_start()
                continue

            if cmd.lower() == 'status':
                print(f"\nCPU State:")
                print(f"  PC=${emu.cpu.PC:04X}  BC=${emu.cpu.BC:04X}  DE=${emu.cpu.DE:04X}  HL=${emu.cpu.HL:04X}")
                print(f"  SP=${emu.cpu.SP:04X}  IX=${emu.cpu.IX:04X}  A=${emu.cpu.A:02X}")
                print(f"  Instructions: {emu.instr_count}\n")
                continue

            if not cmd:
                continue

            # Queue input command
            emu.queue_input(cmd)

            # Run emulator
            print(f"\n[Executing: {cmd}]")
            start_time = time.time()
            instr_before = emu.instr_count
            run_emulator_steps(emu, display, max_steps=500000)
            elapsed = time.time() - start_time
            instr_count = emu.instr_count - instr_before

            if elapsed > 0.1:  # Only show timing for longer operations
                print(f"\n[{instr_count} instructions in {elapsed:.2f}s]\n")

        except KeyboardInterrupt:
            print("\n[Interrupted]")
            break
        except EOFError:
            break
        except Exception as e:
            print(f"[ERROR] {e}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
