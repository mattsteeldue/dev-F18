#!/usr/bin/env python3
"""
Forth-word tracer for the vForth emulator.

Maps every PC to its Forth word name (parsed from list/main.lst) and logs the
sequence of words executed, *gated* so logging only starts once a chosen word is
first entered (default: AUTOEXEC). This keeps the trace focused on the part of
the boot you care about instead of the whole cold-start.

Extras:
  - silences the NEXTREG $FF MMU7 warning flood,
  - optional input queue (--keys),
  - a KEY spy: every time the KEY primitive ($6645) runs it prints LASTK, FLAGS
    and the remaining input queue, so input-delivery bugs are visible.

Usage (run from the repo root C:\\zx\\forth\\f18\\tools\\vforth):
    python emu/trace_words.py                 # gate on AUTOEXEC, no input
    python emu/trace_words.py --gate SPLASH
    python emu/trace_words.py --keys n        # answer 'n' to ASK-Y/N
    python emu/trace_words.py --keys "n" --max 8000000 --limit 400
"""
import re
import sys
import os
import time
import argparse

EMU_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(EMU_DIR)
sys.path.insert(0, EMU_DIR)

LST = os.path.join(ROOT, "project", "vForth18_DOES", "list", "main.lst")
BIN = os.path.join(ROOT, "project", "vForth18_DOES", "output", "forth18e.bin")
RAM = os.path.join(ROOT, "project", "vForth18_DOES", "output", "ram8.bin")

KEY_ADDR = 0x6645      # >KEY: in the listing
LASTK = 0x5C08
FLAGS = 0x5C3B


def build_word_map():
    """Return {code_addr: word_name} parsed from the SjASMPlus listing."""
    label2name, addr2label = {}, {}
    re_newdef = re.compile(r'New_Def\s+(\w+),\s*"([^"]*)"')
    re_lbl = re.compile(r'\b([0-9A-Fa-f]{4})\b\s+>(\w+):')
    with open(LST, "r", encoding="latin-1", errors="replace") as fh:
        for ln in fh:
            m = re_newdef.search(ln)
            if m:
                label2name.setdefault(m.group(1), m.group(2))
            m = re_lbl.search(ln)
            if m:
                addr2label[int(m.group(1), 16)] = m.group(2)
    return {a: label2name.get(l, l) for a, l in addr2label.items()}


def silence_nextreg():
    """Replace the NEXTREG handlers with quiet versions (reg 0x57 = MMU7)."""
    import z80_instructions as z

    def q_a(cpu):
        if cpu.fetch_byte() == 0x57:
            cpu.mmu7_page = cpu.A & 0xFF

    def q_nn(cpu):
        r = cpu.fetch_byte(); v = cpu.fetch_byte()
        if r == 0x57:
            cpu.mmu7_page = v & 0xFF

    z.EXTENDED_MAP[0x92] = q_a
    z.EXTENDED_MAP[0x91] = q_nn


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", default="AUTOEXEC",
                    help="word name that turns tracing on (default AUTOEXEC)")
    ap.add_argument("--keys", default="",
                    help="characters to feed as keyboard input")
    ap.add_argument("--max", type=int, default=8_000_000,
                    help="max instructions")
    ap.add_argument("--secs", type=float, default=60.0, help="wall-clock limit")
    ap.add_argument("--limit", type=int, default=300,
                    help="max word entries to print")
    args = ap.parse_args()

    silence_nextreg()
    from emulator import VForthEmulator

    addr2name = build_word_map()
    gate_addrs = {a for a, n in addr2name.items() if n == args.gate}
    if not gate_addrs:
        print(f"!! gate word {args.gate!r} not found in map"); return

    emu = VForthEmulator()
    emu.max_instructions = args.max
    emu.trace_enabled = False
    emu.input_echo = False
    emu.load_binary(BIN, 0x6366)
    emu.load_binary(RAM, 0xE000)
    emu.initialize_cold_start()

    emits = bytearray()
    emu.handle_emit = lambda: emits.append(emu.cpu.A & 0xFF)
    for ch in args.keys:
        emu.queue_input(ch)

    tracing = False
    seq = []
    key_spy = []
    last = None
    start = time.time()
    while emu.instr_count < emu.max_instructions and (time.time() - start) < args.secs:
        # Key delivery happens inside dispatch() on HALT (50Hz ISR model).
        pc = emu.cpu.PC
        if not tracing and pc in gate_addrs:
            tracing = True
        if tracing:
            nm = addr2name.get(pc)
            if nm is not None and nm != last:
                seq.append((emu.instr_count, nm))
                last = nm
            if pc == KEY_ADDR:
                key_spy.append((emu.instr_count, emu.memory[LASTK],
                                emu.memory[FLAGS], list(emu.input_queue)))
        try:
            op = emu.cpu.fetch_byte()
            emu.dispatch(op)
            emu.instr_count += 1
        except StopIteration:
            print("[StopIteration]"); break
        except Exception as e:
            print("ERR", e); break

    print(f"instr={emu.instr_count} PC=${emu.cpu.PC:04X} "
          f"traced_words={len(seq)} key_calls={len(key_spy)}")
    print(f"=== word trace from {args.gate} (first {args.limit}) ===")
    for n, w in seq[:args.limit]:
        print(f"  {n:9d}  {w}")
    if key_spy:
        print("=== KEY spy (instr, LASTK, FLAGS, queue) ===")
        for n, lk, fl, q in key_spy:
            print(f"  {n:9d}  LASTK=${lk:02X} {chr(lk) if 32<=lk<127 else '.'!r}"
                  f"  FLAGS=${fl:02X}  queue={q}")
    txt = ''.join(chr(b) if 32 <= b < 127 else ('\n' if b in (13, 10) else f'<{b:02X}>')
                  for b in emits)
    i = txt.find("Autoexec asks")
    print("=== emitted text (tail) ===")
    print(txt[i if i >= 0 else 0:][:600])


if __name__ == "__main__":
    main()
