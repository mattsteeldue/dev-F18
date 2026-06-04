#!/usr/bin/env python3
"""
vForth Minimal Emulator - Phase 1
Z80/Z80N emulator for forth18e.bin on headless Python
"""

import sys
import struct
import time
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

        # Trace logging
        self.trace_enabled = False
        self.call_stack = []  # Track CALL/RET for debugging
        self.call_targets = []  # Track actual CALL targets
        self.pc_histogram = {}  # Track which addresses execute most
        self.loop_detector = {}  # Track PC -> instruction count for loop detection
        self.max_call_stack_depth = 0  # Track max depth for stats

        # File I/O (Phase 3)
        self.file_handles = {}  # Map file handle -> file object
        self.next_file_handle = 1  # Next available file handle

        # Interactive input buffer (Phase B)
        self.input_queue = []  # Queue of characters to be read by KEY
        self.input_echo = True  # Echo input to stdout

        # Session recording (Phase C)
        self.transcript_file = None  # File handle for transcript
        self.transcript_enabled = False
        self.session_start_time = None  # For timestamps

        # Performance benchmarking (Phase D)
        self.benchmark_mode = False  # Disable detailed logging for speed
        self.execution_start_time = None
        self.execution_wall_time = 0  # Wall clock time for execution

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
        self.Enter_Ptr = self.find_enter_ptr()  # For native implementation

        self.cpu.SP = S0
        self.cpu.DE = R0
        self.cpu.BC = self.find_cold_start()
        self.cpu.IX = Next_Ptr
        self.cpu.PC = Next_Ptr  # Start execution at inner interpreter

        print(f"Cold start: SP=${self.cpu.SP:04X}, DE=${self.cpu.DE:04X}, BC=${self.cpu.BC:04X}, IX=${self.cpu.IX:04X}, PC=${self.cpu.PC:04X}")
        if self.Enter_Ptr:
            print(f"Enter_Ptr found at ${self.Enter_Ptr:04X}")

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

    def handle_nextzxos_call(self):
        """Handle NextZXOS call via rst 08 / db <func>"""
        # After the RST 08 instruction, fetch the function byte
        func = self.cpu.fetch_byte()

        if func == 0x94:
            # Terminal I/O function - dispatch on C register
            c_register = self.cpu.C
            if c_register == 1:  # KEY
                self.handle_key()
            elif c_register == 2:  # EMIT / EMITC
                self.handle_emit()
            elif c_register == 7:  # CLS (clear screen)
                self.handle_cls()
            else:
                if self.instr_count < 100000:
                    print(f"[{self.instr_count:6d}] NextZXOS call C=${c_register:02X} (unimplemented)")

        elif func == 0x9A:  # F_OPEN
            self.handle_f_open()
        elif func == 0x9B:  # F_CLOSE
            self.handle_f_close()
        elif func == 0x9C:  # F_SYNC
            self.handle_f_sync()
        elif func == 0x9D:  # F_READ
            self.handle_f_read()
        elif func == 0x9E:  # F_WRITE
            self.handle_f_write()
        elif func == 0x9F:  # F_SEEK
            self.handle_f_seek()
        elif func == 0xA0:  # F_FGETPOS
            self.handle_f_fgetpos()
        elif func == 0xA3:  # F_OPENDIR
            self.handle_f_opendir()
        elif func == 0xA4:  # F_READDIR
            self.handle_f_readdir()
        else:
            if self.instr_count < 100000:
                print(f"[{self.instr_count:6d}] NextZXOS call func=${ func:02X} (unimplemented)")

    def handle_key(self):
        """KEY: read character from input queue, or stdin if queue empty"""
        # Try input queue first (for interactive REPL)
        if self.input_queue:
            char = self.input_queue.pop(0)
            self.cpu.A = ord(char) & 0xFF if isinstance(char, str) else char & 0xFF
            if self.input_echo:
                sys.stdout.write(char if isinstance(char, str) else chr(char))
                sys.stdout.flush()
            self.log_transcript("INPUT", char if isinstance(char, str) else chr(char))
            return

        # Fall back to stdin
        try:
            char = input()  # Read line from stdin
            if char:
                self.cpu.A = ord(char[0]) & 0xFF
            else:
                self.cpu.A = 0x0D  # CR if empty line
            self.log_transcript("INPUT", char if char else '\r')
        except EOFError:
            raise StopIteration()  # Exit emulator on EOF

    def queue_input(self, text):
        """Queue text input for KEY to read character-by-character"""
        for char in text:
            self.input_queue.append(char)
        # Add CR at end
        self.input_queue.append('\r')

    def start_session_recording(self, filename):
        """Start recording input/output to a transcript file"""
        try:
            self.transcript_file = open(filename, 'w', encoding='ascii')
            self.transcript_enabled = True
            self.session_start_time = time.time()
            self.transcript_file.write(f"=== vForth Session Transcript ===\n")
            self.transcript_file.write(f"Started: {self.session_start_time}\n\n")
            self.transcript_file.flush()
            print(f"[OK] Session recording started: {filename}")
        except Exception as e:
            print(f"[ERROR] Failed to start recording: {e}")

    def stop_session_recording(self):
        """Stop recording and close transcript file"""
        if self.transcript_file:
            try:
                self.transcript_file.write(f"\n=== Session ended after {self.instr_count} instructions ===\n")
                self.transcript_file.close()
                print(f"[OK] Session recording stopped")
            except Exception as e:
                print(f"[ERROR] Failed to stop recording: {e}")
            finally:
                self.transcript_file = None
                self.transcript_enabled = False

    def log_transcript(self, source, text):
        """Log input or output to transcript"""
        if self.transcript_enabled and self.transcript_file:
            try:
                # source is "input" or "output"
                elapsed = time.time() - self.session_start_time if self.session_start_time else 0
                # Escape special chars for display
                display_text = repr(text) if len(text) == 1 else text
                self.transcript_file.write(f"[{elapsed:8.2f}] {source:6s}: {display_text}\n")
                self.transcript_file.flush()
            except:
                pass  # Silently fail if transcript writing fails

    def handle_emit(self):
        """EMIT / EMITC: write character in A register to stdout"""
        # EMITC writes full byte (0-255), EMIT masks to 7-bit ASCII
        # We'll write both the same way for now
        char = chr(self.cpu.A & 0x7F) if self.cpu.A < 128 else chr(self.cpu.A)
        sys.stdout.write(char)
        sys.stdout.flush()
        self.log_transcript("OUTPUT", char)

    def handle_cls(self):
        """CLS: clear screen (stub as no-op)"""
        pass

    def handle_f_open(self):
        """F_OPEN: open file
        Input: A=mode, B=*, DE=buffer addr, IX=filename (null-terminated)
        Output: A=file handle, HL=error flag (0=success, -1=error)
        """
        # Read filename from memory at IX (null-terminated string)
        filename_addr = self.cpu.IX
        filename_bytes = []
        while True:
            byte = self.memory[filename_addr]
            if byte == 0:  # null terminator
                break
            filename_bytes.append(byte)
            filename_addr = (filename_addr + 1) & 0xFFFF

        filename = ''.join(chr(b) for b in filename_bytes if 32 <= b < 127)

        # Parse mode byte (C register contains the mode)
        mode = self.cpu.C
        read_mode = bool(mode & 0x01)
        write_mode = bool(mode & 0x02)
        create_mode = mode & 0x0C

        # Open file
        try:
            py_mode = ''
            if read_mode and write_mode:
                py_mode = 'r+b'
            elif write_mode:
                py_mode = 'w+b'
            elif read_mode:
                py_mode = 'rb'
            else:
                py_mode = 'rb'

            # Handle create modes
            if create_mode == 0x08:  # open or create
                py_mode = 'a+b'
            elif create_mode == 0x04:  # create new, error if exists
                py_mode = 'x+b'
            elif create_mode == 0x0C:  # create/truncate
                py_mode = 'w+b'

            f = open(filename, py_mode)
            handle = self.next_file_handle
            self.file_handles[handle] = f
            self.next_file_handle += 1

            self.cpu.A = handle & 0xFF
            self.cpu.HL = 0  # success
        except Exception as e:
            self.cpu.A = 0
            self.cpu.HL = 0xFFFF  # error

    def handle_f_close(self):
        """F_CLOSE: close file
        Input: A=file handle
        Output: HL=error flag (0=success, -1=error)
        """
        handle = self.cpu.A
        if handle in self.file_handles:
            try:
                self.file_handles[handle].close()
                del self.file_handles[handle]
                self.cpu.HL = 0  # success
            except:
                self.cpu.HL = 0xFFFF  # error
        else:
            self.cpu.HL = 0xFFFF  # error (file not open)

    def handle_f_read(self):
        """F_READ: read from file
        Input: A=file handle, BC=bytes to read, IX=address
        Output: DE=bytes read, HL=error flag (0=success, -1=error)
        """
        handle = self.cpu.A
        num_bytes = self.cpu.BC
        addr = self.cpu.IX

        if handle in self.file_handles:
            try:
                data = self.file_handles[handle].read(num_bytes)
                bytes_read = len(data)

                # Write data to memory
                for i, byte in enumerate(data):
                    self.memory[(addr + i) & 0xFFFF] = byte

                self.cpu.DE = bytes_read
                self.cpu.HL = 0  # success
            except:
                self.cpu.DE = 0
                self.cpu.HL = 0xFFFF  # error
        else:
            self.cpu.DE = 0
            self.cpu.HL = 0xFFFF  # error (file not open)

    def handle_f_write(self):
        """F_WRITE: write to file
        Input: A=file handle, BC=bytes to write, IX=address
        Output: DE=bytes written, HL=error flag (0=success, -1=error)
        """
        handle = self.cpu.A
        num_bytes = self.cpu.BC
        addr = self.cpu.IX

        if handle in self.file_handles:
            try:
                data = bytes(self.memory[(addr + i) & 0xFFFF] for i in range(num_bytes))
                bytes_written = self.file_handles[handle].write(data)

                self.cpu.DE = bytes_written
                self.cpu.HL = 0  # success
            except:
                self.cpu.DE = 0
                self.cpu.HL = 0xFFFF  # error
        else:
            self.cpu.DE = 0
            self.cpu.HL = 0xFFFF  # error (file not open)

    def handle_f_seek(self):
        """F_SEEK: seek in file
        Input: A=file handle, BC:DE=offset (32-bit), HL=whence (0=start)
        Output: HL=error flag (0=success, -1=error)
        """
        handle = self.cpu.A
        offset = (self.cpu.BC << 16) | self.cpu.DE

        if handle in self.file_handles:
            try:
                self.file_handles[handle].seek(offset, 0)  # 0 = SEEK_SET
                self.cpu.HL = 0  # success
            except:
                self.cpu.HL = 0xFFFF  # error
        else:
            self.cpu.HL = 0xFFFF  # error (file not open)

    def handle_f_fgetpos(self):
        """F_FGETPOS: get file position
        Input: A=file handle
        Output: BC:DE=position (32-bit), HL=error flag (0=success, -1=error)
        """
        handle = self.cpu.A

        if handle in self.file_handles:
            try:
                pos = self.file_handles[handle].tell()
                self.cpu.BC = (pos >> 16) & 0xFFFF
                self.cpu.DE = pos & 0xFFFF
                self.cpu.HL = 0  # success
            except:
                self.cpu.HL = 0xFFFF  # error
        else:
            self.cpu.HL = 0xFFFF  # error (file not open)

    def handle_f_sync(self):
        """F_SYNC: flush file to disk
        Input: A=file handle
        Output: HL=error flag (0=success, -1=error)
        """
        handle = self.cpu.A
        if handle in self.file_handles:
            try:
                self.file_handles[handle].flush()
                self.cpu.HL = 0  # success
            except:
                self.cpu.HL = 0xFFFF  # error
        else:
            self.cpu.HL = 0xFFFF  # error (file not open)

    def handle_f_opendir(self):
        """F_OPENDIR: open directory for listing
        Input: IX=directory path (null-terminated)
        Output: A=handle, HL=error flag (0=success, -1=error)
        """
        import os
        # Read directory path from memory at IX
        dir_addr = self.cpu.IX
        dir_bytes = []
        while True:
            byte = self.memory[dir_addr]
            if byte == 0:
                break
            dir_bytes.append(byte)
            dir_addr = (dir_addr + 1) & 0xFFFF

        dirname = ''.join(chr(b) for b in dir_bytes if 32 <= b < 127)

        try:
            # Emulate directory handle by storing file list
            if os.path.isdir(dirname):
                entries = os.listdir(dirname)
                handle = self.next_file_handle
                self.file_handles[handle] = {'type': 'dir', 'entries': entries, 'index': 0, 'path': dirname}
                self.next_file_handle += 1
                self.cpu.A = handle & 0xFF
                self.cpu.HL = 0  # success
            else:
                self.cpu.A = 0
                self.cpu.HL = 0xFFFF  # error (directory not found)
        except Exception as e:
            self.cpu.A = 0
            self.cpu.HL = 0xFFFF  # error

    def handle_f_readdir(self):
        """F_READDIR: read next directory entry
        Input: A=handle, DE=buffer for entry, IX=pointer
        Output: A=handle, HL=error flag (0=success, -1=error)
        """
        handle = self.cpu.A
        if handle in self.file_handles and isinstance(self.file_handles[handle], dict) and self.file_handles[handle].get('type') == 'dir':
            try:
                entries = self.file_handles[handle]['entries']
                idx = self.file_handles[handle]['index']
                if idx < len(entries):
                    entry = entries[idx]
                    # Write entry to buffer at IX
                    entry_bytes = entry.encode('ascii', errors='ignore')
                    for i, b in enumerate(entry_bytes):
                        if (self.cpu.IX + i) & 0xFFFF >= 0x10000:
                            break
                        self.memory[(self.cpu.IX + i) & 0xFFFF] = b & 0xFF
                    # Null terminator
                    self.memory[(self.cpu.IX + len(entry_bytes)) & 0xFFFF] = 0
                    self.file_handles[handle]['index'] = idx + 1
                    self.cpu.HL = 0  # success
                else:
                    # End of directory
                    self.memory[self.cpu.IX] = 0  # Empty entry
                    self.cpu.HL = 0xFFFF  # EOF marker
            except:
                self.cpu.HL = 0xFFFF  # error
        else:
            self.cpu.HL = 0xFFFF  # error (not a directory handle)

    def start_benchmark(self):
        """Start performance measurement"""
        self.benchmark_mode = True
        self.execution_start_time = time.time()
        print("[BENCHMARK] Mode enabled - detailed logging disabled for accuracy")

    def stop_benchmark(self):
        """Stop performance measurement and calculate metrics"""
        self.benchmark_mode = False
        if self.execution_start_time:
            self.execution_wall_time = time.time() - self.execution_start_time
        return self.execution_wall_time

    def print_trace_report(self):
        """Print execution trace report"""
        print("\n=== Trace Report ===")

        # Performance metrics (Phase D)
        if self.execution_wall_time > 0:
            instr_per_sec = self.instr_count / self.execution_wall_time
            print(f"\n--- Performance (Phase D) ---")
            print(f"Total instructions: {self.instr_count}")
            print(f"Wall-clock time: {self.execution_wall_time:.3f} seconds")
            print(f"Speed: {instr_per_sec:,.0f} instructions/second")
            print(f"Avg time per instruction: {1000*self.execution_wall_time/self.instr_count:.3f} ms")

        # Top executing addresses
        print("\n--- Top 20 Hottest Addresses ---")
        sorted_pcs = sorted(self.pc_histogram.items(), key=lambda x: x[1], reverse=True)
        for pc, count in sorted_pcs[:20]:
            pct = 100.0 * count / self.instr_count
            print(f"  ${pc:04X}: {count:8d} times ({pct:5.1f}%)")

        # Call stack depth
        print(f"\nMax call stack depth reached: {max(self.call_stack) if self.call_stack else 0}")
        print(f"Current CPU state:")
        print(f"  PC=${self.cpu.PC:04X}  BC=${self.cpu.BC:04X}  DE=${self.cpu.DE:04X}  HL=${self.cpu.HL:04X}")
        print(f"  SP=${self.cpu.SP:04X}  IX=${self.cpu.IX:04X}  IY=${self.cpu.IY:04X}  A=${self.cpu.A:02X}")

    def find_cold_start(self):
        """Find Cold_Start address in binary"""
        # Cold_Start is referenced from ColdRoutine
        # Look for the entry point; typically early in the code
        ORIGIN = 0x6366
        # For now, assume it's at ORIGIN + 2 (after Warm_Start entry)
        # This will be verified when we trace execution
        return ORIGIN + 2

    def find_enter_ptr(self):
        """Find Enter_Ptr address - look for PUSH BC followed by pattern"""
        ORIGIN = 0x6366
        # Enter_Ptr starts with PUSH BC (0xC5), followed by more instructions
        # and typically followed by "ld bc, hl+3" sequence
        for i in range(0x1000):
            addr = ORIGIN + i
            if addr >= 0x10000:
                break
            # Look for PUSH BC (0xC5) at address that looks like a function
            if self.memory[addr] == 0xC5:
                # Check if there's a plausible pattern afterward
                # For now, just try a few candidates
                if addr > ORIGIN + 100:  # Skip early addresses
                    return addr
        return None

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
        self.print_trace_report()

    def log_trace(self, opcode, desc=""):
        """Log instruction for tracing"""
        if self.trace_enabled:
            print(f"[{self.instr_count:7d}] PC=${self.cpu.PC-1:04X}: 0x{opcode:02X} {desc:30s} | BC=${self.cpu.BC:04X} DE=${self.cpu.DE:04X} HL=${self.cpu.HL:04X}")

    def track_pc(self):
        """Track PC for histogram and loop detection"""
        pc = self.cpu.PC
        if pc not in self.pc_histogram:
            self.pc_histogram[pc] = 0
        self.pc_histogram[pc] += 1

        # Loop detection: if same PC appears 100+ times in last 1000 instructions
        if pc not in self.loop_detector:
            self.loop_detector[pc] = self.instr_count
        else:
            delta = self.instr_count - self.loop_detector[pc]
            if delta > 0 and delta < 50:  # Tight loop
                if self.instr_count % 10000 == 0:
                    print(f"[Loop detected] PC=${pc:04X} repeats every ~{delta} instructions")

    def dispatch(self, opcode):
        """Main instruction dispatcher"""
        self.track_pc()

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

        elif opcode == 0x08:  # RST 08 -- NextZXOS call
            # NextZXOS uses C register to select function
            self.handle_nextzxos_call()
            return  # Skip normal instruction execution

        elif opcode == 0xCB:
            # Bit operations - skip for now
            self.cpu.fetch_byte()

        elif opcode == 0xFD:
            # IY instruction - skip for now
            self.cpu.fetch_byte()

        elif opcode in INSTRUCTION_MAP:
            # Special tracing and native implementation for CALL, RET, and JP
            if opcode == 0xCD:  # CALL nn
                # Look ahead to find target address (next two bytes are lo,hi)
                target_lo = self.memory[(self.cpu.PC) & 0xFFFF]
                target_hi = self.memory[(self.cpu.PC + 1) & 0xFFFF]
                target = target_lo | (target_hi << 8)

                # Check if this is a CALL to Enter_Ptr (native implementation)
                if self.Enter_Ptr and target == self.Enter_Ptr:
                    # Execute Enter_Ptr natively instead of Z80 emulation
                    if self.instr_count < 10000:
                        print(f"[{self.instr_count:6d}] CALL Enter_Ptr native: BC=${self.cpu.BC:04X}")

                    # The CALL instruction will push return address (PFA) onto hardware stack (SP)
                    # We need to execute that CALL first, then implement ENTER logic

                    # Execute the normal CALL (saves PC on SP)
                    self.cpu.SP = (self.cpu.SP - 2) & 0xFFFF
                    self.cpu.mem16_le_set(self.cpu.SP, self.cpu.PC + 2)  # PC+2 points after the 2-byte address operand

                    # Now we're at the start of ENTER_Ptr. Execute ENTER logic:
                    # 1. Save current IP (BC) on vForth return stack (via DE)
                    self.cpu.DE = (self.cpu.DE - 2) & 0xFFFF
                    self.cpu.mem16_le_set(self.cpu.DE, self.cpu.BC)

                    # 2. POP BC from hardware stack (SP) - this gets the PFA
                    pfa = self.cpu.mem16_le(self.cpu.SP)
                    self.cpu.SP = (self.cpu.SP + 2) & 0xFFFF
                    self.cpu.BC = pfa

                    # 3. Jump to Next_Ptr
                    self.cpu.PC = self.cpu.IX

                    return  # Skip normal CALL execution

                # Normal CALL
                self.call_stack.append(self.cpu.PC - 1)
                self.call_targets.append(target)

                if len(self.call_stack) > self.max_call_stack_depth:
                    self.max_call_stack_depth = len(self.call_stack)

                if self.instr_count < 1000 or len(self.call_stack) <= 5:
                    print(f"[{self.instr_count:6d}] CALL depth {len(self.call_stack):2d}: ${self.cpu.PC-1:04X} -> ${target:04X}")

            elif opcode == 0xC9:  # RET (EXIT from high-level word)
                # In vForth, RET at end of colon-definition:
                # 1. Pop IP (BC) from vForth return stack (DE)
                # 2. Jump to Next_Ptr (IX) to continue interpretation

                if self.instr_count < 100000:
                    print(f"[{self.instr_count:6d}] RET  (EXIT): BC=${self.cpu.BC:04X}, DE=${self.cpu.DE:04X}")

                # Pop BC from return stack (vForth stack at DE)
                self.cpu.BC = self.cpu.mem16_le(self.cpu.DE)
                self.cpu.DE = (self.cpu.DE + 2) & 0xFFFF

                # Jump to Next_Ptr to continue interpretation
                self.cpu.PC = self.cpu.IX

                return  # Skip normal RET execution

            elif opcode == 0xC3:  # JP nn
                jp_lo = self.memory[(self.cpu.PC) & 0xFFFF]
                jp_hi = self.memory[(self.cpu.PC + 1) & 0xFFFF]
                jp_addr = jp_lo | (jp_hi << 8)
                if self.instr_count < 100:
                    print(f"[{self.instr_count:6d}] JP    ${self.cpu.PC-1:04X} -> ${jp_addr:04X}")

            elif opcode == 0xE9:  # JP (HL)
                if self.instr_count < 200 and self.instr_count % 100 == 0:
                    print(f"[{self.instr_count:6d}] JP (HL) = ${self.cpu.HL:04X}")

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
