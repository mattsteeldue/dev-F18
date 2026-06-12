#!/usr/bin/env python3
"""Reproduce the `13 SELECT WORDS` corruption.

On real NextZXOS, `rst $10` to a file-attached stream goes through +3DOS,
which restores the OS default banking on exit and so unmaps the vForth heap
page from MMU7 (slot 7 is left at the bank-0 default, page 1).  The flat-memory
emulator never actually swaps $E000-$FFFF, so this script installs a real
MMU7 page swap (heap pages are preserved per page number; foreign pages read
as OS-looking garbage), then resets the page to 1 after every emitted byte,
exactly like a file-stream rst $10 does on hardware.

Usage:  python emu/test_words_stream.py
"""
import os
import sys

EMU_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(EMU_DIR)
sys.path.insert(0, EMU_DIR)

from emulator import VForthEmulator

BIN = os.path.join(ROOT, "project", "vForth18_DOES", "output", "forth18e.bin")
RAM = os.path.join(ROOT, "project", "vForth18_DOES", "output", "ram8.bin")

STEP_CAP = 40_000_000
CURSOR_GLYPHS = (0x8F, 0x8C)
GARBAGE = (b"\x73\x81" * 0x1000)[:0x2000]   # what a foreign page "contains"


def install_mmu7_banking(cpu):
    """Make nextreg-87 writes really swap the $E000-$FFFF window."""
    pages = {}
    cpu._mmu7_real = cpu.mmu7_page

    def fget(self):
        return getattr(self, "_mmu7_real", 0x20)

    def fset(self, v):
        v &= 0xFF
        if not hasattr(self, "_mmu7_real"):   # fresh CPU (property is class-wide)
            self._mmu7_real = v
            return
        cur = self._mmu7_real
        if v == cur:
            return
        pages[cur] = bytes(self.mem[0xE000:0x10000])
        self.mem[0xE000:0x10000] = pages.get(v, GARBAGE)
        self._mmu7_real = v

    type(cpu).mmu7_page = property(fget, fset)


def install_nextreg_ports(cpu):
    """Model reading back NextReg 87 via ports $243B/$253B (MMU7_read)."""
    import z80_instructions as zi
    sel = [0]

    def out_c_a(c):
        if c.BC == 0x243B:
            sel[0] = c.A

    def in_a_c(c):
        if c.BC == 0x253B and sel[0] == 87:
            c.A = c.mmu7_page & 0xFF
        else:
            c.A = 0xFF

    zi.EXTENDED_MAP[0x79] = out_c_a
    zi.EXTENDED_MAP[0x78] = in_a_c


CAVE = 0x5B00          # scratch RAM, unused by the headless core
SAVED = 0x5BFE         # one-byte MMU7 save slot


def apply_fix_patch(mem):
    """Binary-patch the loaded core with the same fix now in L0.asm:
    save the MMU7 page before the rst $10 ROM call, restore it after.
    Returns False when the loaded core already contains the fix (the
    bare push ix / rst $10 / pop ix sequence is gone after reassembly)."""
    pat = bytes([0xDD, 0xE5, 0xD7, 0xDD, 0xE1])   # push ix / rst $10 / pop ix
    base = bytes(mem).find(pat)
    if base < 0:
        return False
    rst_at = base + 2                              # the D7 byte (CLS_No_Layer_0)
    back = base + 5                                # the pop de that follows
    # rst $10 / pop ix  ->  jp CAVE
    mem[rst_at:rst_at + 3] = bytes([0xC3, CAVE & 0xFF, CAVE >> 8])
    cave = bytes([
        0xF5,                          # push af          (keep the char)
        0x3E, 0x57,                    # ld a, $57        (MMU7_read inline)
        0x01, 0x3B, 0x24,              # ld bc, $243B
        0xED, 0x79,                    # out (c), a
        0x04,                          # inc b
        0xED, 0x78,                    # in a, (c)
        0x32, SAVED & 0xFF, SAVED >> 8,  # ld (SAVED), a
        0xF1,                          # pop af
        0xD7,                          # rst $10
        0x3A, SAVED & 0xFF, SAVED >> 8,  # ld a, (SAVED)
        0xED, 0x92, 0x57,              # nextreg $57, a
        0xDD, 0xE1,                    # pop ix
        0xC3, back & 0xFF, back >> 8,  # jp back
    ])
    mem[CAVE:CAVE + len(cave)] = cave
    return True


def core_is_unfixed(path=BIN):
    pat = bytes([0xDD, 0xE5, 0xD7, 0xDD, 0xE1])
    with open(path, "rb") as fh:
        return fh.read().find(pat) >= 0


def run_words(clobber_mmu7, patched=False):
    emu = VForthEmulator()
    emu.max_instructions = 10 ** 12
    emu.trace_enabled = False
    emu.input_echo = False
    emu.load_binary(BIN, 0x6366)
    emu.load_binary(RAM, 0xE000)
    emu.initialize_cold_start()
    install_mmu7_banking(emu.cpu)
    install_nextreg_ports(emu.cpu)
    if patched:
        apply_fix_patch(emu.memory)

    out = bytearray()
    last_real = [0]
    saw_cursor = [False]
    clobber = [False]

    def emit():
        b = emu.cpu.A & 0xFF
        out.append(b)
        if b in CURSOR_GLYPHS:
            saw_cursor[0] = True
        elif b != 0x08:
            last_real[0] = emu.instr_count
        if clobber[0]:
            # what +3DOS leaves behind after a file-stream rst $10
            emu.cpu.mmu7_page = 1

    emu.handle_emit = emit

    def run_to_prompt(max_out=None):
        saw_cursor[0] = False
        last_real[0] = emu.instr_count
        start = emu.instr_count
        while emu.instr_count - start < STEP_CAP:
            op = emu.cpu.fetch_byte()
            emu.dispatch(op)
            emu.instr_count += 1
            if max_out is not None and len(out) > max_out:
                return False          # runaway output: the real-HW "hang"
            if (not emu.input_queue and saw_cursor[0]
                    and emu.instr_count - last_real[0] > 250_000):
                return True
        return False

    emu.queue_input("n")          # skip utility loading
    run_to_prompt()
    out.clear()

    clobber[0] = clobber_mmu7     # 13 SELECT: from now on emits go "to file"
    emu.queue_input("WORDS")
    finished = run_to_prompt(max_out=6000)
    return finished, bytes(out)


def render(raw):
    return "".join(chr(b) if 0x20 <= b < 0x7F else ("\n" if b == 0x0D else "")
                   for b in raw)


failures = 0
unfixed = core_is_unfixed()
print(f"core binary contains the fix: {not unfixed}\n")
modes = [("as-built, normal rst $10 (screen)", False, False),
         ("as-built, clobbering rst $10 (file stream)"
          + (" -- expect garbage" if unfixed else ""), True, False)]
if unfixed:
    modes += [("patched, clobbering rst $10 (file stream)", True, True),
              ("patched, normal rst $10 (screen)", False, True)]
for mode, clobber, patched in modes:
    finished, raw = run_words(clobber, patched)
    txt = render(raw)
    names = txt.split()
    sane = ("WORDS" in names and "EMIT" in names and "LIST" in names
            and finished)
    print(f"=== {mode} ===")
    print(f"finished: {finished}   bytes: {len(raw)}   sane: {sane}")
    print(txt[:280])
    print("--- tail ---")
    print(txt[-160:])
    print()
    expected_garbage = clobber and not patched and unfixed
    if sane == expected_garbage:
        failures += 1

sys.exit(failures)
