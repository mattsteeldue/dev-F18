#!/usr/bin/env python3
r"""
Interactive vForth REPL over the headless emulator.

Boots the core to the `ok` prompt (auto-answering the ASK-Y/N utility question),
then forwards each line you type to the running Forth system and prints what it
emits. Input is delivered the way the real machine sees it (on HALT / frame
wait), so the REPL behaves like the Spectrum Next console.

Run from the repo root  C:\zx\forth\f18\tools\vforth :

    python emu/repl.py            # skip utility loading (answers 'n')
    python emu/repl.py --load     # answer 'y' (load REMOUNT/WHERE/.S/... ; slow)

Type Forth at the `vforth>` prompt. Commands:  .quit  exits,  .stack  not provided
(use Forth's own words). Ctrl-C also exits.
"""
import os
import re
import sys
import argparse

EMU_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(EMU_DIR)
sys.path.insert(0, EMU_DIR)

BIN = os.path.join(ROOT, "project", "vForth18_DOES", "output", "forth18e.bin")
RAM = os.path.join(ROOT, "project", "vForth18_DOES", "output", "ram8.bin")

CURSOR_GLYPHS = (0x8F, 0x8C)          # the two blinking-cursor characters
IDLE_INSTRS = 250_000                 # quiet instrs (after real output) => at prompt
STEP_CAP = 60_000_000                 # safety cap per run-until-prompt


class Repl:
    def __init__(self, load_utils=False):
        from emulator import VForthEmulator
        self.emu = VForthEmulator()
        self.emu.max_instructions = 10 ** 12
        self.emu.trace_enabled = False
        self.emu.input_echo = False
        self.emu.load_binary(BIN, 0x6366)
        self.emu.load_binary(RAM, 0xE000)
        self.emu.initialize_cold_start()

        self.out_raw = bytearray()      # every emitted byte, rendered at display
        self._saw_cursor = False
        self._last_real_instr = 0
        self.emu.handle_emit = self._emit
        self.load_utils = load_utils

    def _emit(self):
        b = self.emu.cpu.A & 0xFF
        self.out_raw.append(b)
        if b in CURSOR_GLYPHS:
            self._saw_cursor = True
        elif b != 0x08:                  # backspace alone isn't "real" output
            self._last_real_instr = self.emu.instr_count

    def _run_to_prompt(self):
        """Execute until the core sits in its blinking-cursor input wait."""
        emu = self.emu
        self._saw_cursor = False
        self._last_real_instr = emu.instr_count
        start_instr = emu.instr_count
        while emu.instr_count - start_instr < STEP_CAP:
            try:
                op = emu.cpu.fetch_byte()
                emu.dispatch(op)
                emu.instr_count += 1
            except StopIteration:
                return False
            except Exception as e:
                self.out_raw.extend(f"\n[emulator error: {e}]\n".encode("latin-1"))
                return False
            # At the prompt: queue drained, the cursor has blinked, and no real
            # (non-cursor) byte has been emitted for a while.
            if (not emu.input_queue and self._saw_cursor
                    and emu.instr_count - self._last_real_instr > IDLE_INSTRS):
                return True
        return True

    def _drain(self):
        """Render the raw byte stream like a terminal: apply CR/backspace,
        drop the blinking-cursor glyphs, map the ZX copyright glyph."""
        line, col, lines = [], 0, []
        for b in self.out_raw:
            if b in (0x0D, 0x0A):
                lines.append("".join(line)); line, col = [], 0
            elif b == 0x08:
                col = max(0, col - 1)
            elif b in CURSOR_GLYPHS or b < 0x20:
                continue
            else:
                ch = "(c)" if b == 0x7F else chr(b)
                if col < len(line):
                    line[col] = ch
                else:
                    line.append(ch)
                col += 1
        lines.append("".join(line))
        self.out_raw.clear()
        return "\n".join(lines)

    @staticmethod
    def _show(text):
        sys.stdout.write(text)
        sys.stdout.flush()

    def boot(self):
        self.emu.queue_input("y" if self.load_utils else "n")
        self._run_to_prompt()
        self._show(self._drain())

    def repl(self):
        print("\n[vforth REPL ready -- type Forth, '.quit' to exit]\n")
        while True:
            try:
                line = input("vforth> ")
            except (EOFError, KeyboardInterrupt):
                print("\nbye")
                return
            if line.strip() in (".quit", ".q", "bye"):
                print("bye")
                return
            self.emu.queue_input(line)
            ok = self._run_to_prompt()
            self._show(self._drain())
            if not ok:
                print("\n[emulator stopped]")
                return


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--load", action="store_true",
                    help="answer 'y' to load utilities (slow)")
    args = ap.parse_args()
    r = Repl(load_utils=args.load)
    print("Booting vForth ...")
    r.boot()
    r.repl()


if __name__ == "__main__":
    main()
