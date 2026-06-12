#!/usr/bin/env python3
"""
gen-dict-structure.py -- regenerate the dynamic text of the manual section
"Dictionary memory structure" (vForth1.8-core-en .odt, ~4.6).

The section shows, for the two contiguous definitions SWAP and DUP:
  1. the "Heap memory / Main memory" layout tables (NFA/LFA/CFA, mirror, xt)
  2. the "You can verify yourself" transcript (SEE + DUMP output)

Both are full of build-specific hex addresses that go stale on every core
rebuild. This script boots the headless emulator with the CURRENT binaries,
reads the real bytes and captures the real SEE/DUMP output, then prints the
two paragraphs ready to be pasted by hand into the .odt (which must NEVER
be edited automatically).

Usage (from tools/vForth, takes ~2 minutes for the boot):

    python3 util/gen-dict-structure.py
"""
import os
import re
import sys
import contextlib
import io

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "emu"))
os.chdir(ROOT)

WORD_A, WORD_B = "SWAP", "DUP"

# minimal Z80 disassembler, enough for the tiny xt bodies shown in the doc
ONE_BYTE = {
    0xC1: "pop bc", 0xD1: "pop de", 0xE1: "pop hl", 0xF1: "pop af",
    0xC5: "push bc", 0xD5: "push de", 0xE5: "push hl", 0xF5: "push af",
    0xE3: "ex (sp),hl", 0xEB: "ex de,hl", 0xD9: "exx", 0x08: "ex af,af'",
    0xC9: "ret", 0xE9: "jp (hl)", 0x00: "nop",
}


def disasm(code):
    """Return list of (bytes, mnemonic) covering `code` (ends with DD E9)."""
    out, i = [], 0
    while i < len(code):
        b = code[i]
        if b == 0xDD and i + 1 < len(code) and code[i + 1] == 0xE9:
            out.append((code[i:i + 2], "jp (ix)"))
            i += 2
        elif b in ONE_BYTE:
            out.append((code[i:i + 1], ONE_BYTE[b]))
            i += 1
        else:
            out.append((code[i:i + 1], "db %02Xh" % b))
            i += 1
    return out


def build_date():
    src = open("project/vForth18_DOES/source/L0.asm", encoding="latin-1").read()
    m = re.search(r"build (\d{4}-\d{2}-\d{2})", src)
    return m.group(1) if m else "????-??-??"


class Driver:
    """Boot the REPL harness once and exchange lines with the core."""

    def __init__(self):
        from repl import Repl
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self.r = Repl(load_utils=False)
            self.r.boot()

    def send(self, line):
        self.r.emu.queue_input(line)
        self.r._run_to_prompt()
        return self.r._drain()

    def mem(self, addr, n):
        return bytes(self.r.emu.memory[addr:addr + n])


def parse_see(txt):
    """Extract nfa/lfa/cfa info from a SEE transcript (HEX base)."""
    nfa = int(re.search(r"Nfa:\s+([0-9A-F]+)", txt).group(1), 16)
    m = re.search(r"Lfa:\s+([0-9A-F]+)\s+([0-9A-F]+)\s*(\S*)", txt)
    lfa, prev_hp, prev_name = int(m.group(1), 16), int(m.group(2), 16), m.group(3)
    xt = int(re.search(r"Cfa:\s+([0-9A-F]+)", txt).group(1), 16)
    return dict(nfa=nfa, lfa=lfa, prev_hp=prev_hp, prev_name=prev_name, xt=xt)


def hp_of(addr):
    """heap window address $Exxx -> heap-pointer (page $20 only, the case
    of the core words shown here)."""
    return addr - 0xE000


def hx(v, w=4):
    return ("%0" + str(w) + "X") % v


def pairs(bs):
    return " ".join("%02X" % b for b in bs)


def layout_block(d, name, drv, prev_label):
    """Render the 'Heap memory / Main memory' table for one word."""
    nfa, lfa, xt = d["nfa"], d["lfa"], d["xt"]
    nlen = drv.mem(nfa, 1)[0] & 0x1F
    name_bytes = drv.mem(nfa, 1 + nlen)
    lfa_bytes = drv.mem(lfa, 2)
    cfa_slot = lfa + 2
    cfa_bytes = drv.mem(cfa_slot, 2)
    mirror = xt - 2
    mirror_bytes = drv.mem(mirror, 2)
    code = drv.mem(xt, 16)
    end = code.find(b"\xDD\xE9")
    code = code[:end + 2] if end >= 0 else code[:6]
    ops = disasm(code)

    chars = " ".join("'%c'" % (b & 0x7F) for b in name_bytes[1:])
    backptr = mirror_bytes[0] | (mirror_bytes[1] << 8)

    lines = []
    lines.append("Heap memory:")
    lines.append("NFA    %s      | %02X | %s |             | len |  %s |"
                 % (hx(hp_of(nfa)), name_bytes[0], pairs(name_bytes[1:]), chars))
    lines.append("LFA    %s      | %s |                    | %s |  heap-pointer to previous NFA definition%s"
                 % (hx(hp_of(lfa)), pairs(lfa_bytes),
                    hx(lfa_bytes[0] | (lfa_bytes[1] << 8)), prev_label))
    lines.append("CFA    %s      | %s |                    | %s |  xt memory-address of this definition"
                 % (hx(hp_of(cfa_slot)), pairs(cfa_bytes),
                    hx(cfa_bytes[0] | (cfa_bytes[1] << 8))))
    lines.append("")
    lines.append("Main memory:")
    lines.append("Mirror %s      | %s |          | %s | backward-heap-pointer to %s's CFA"
                 % (hx(mirror), pairs(mirror_bytes), hx(backptr), name))
    lines.append(" xt    %s      | %s |"
                 % (hx(xt), " | ".join(pairs(b) for b, _ in ops)))
    lines.append("                 | %s |" % " | ".join(m for _, m in ops))
    return "\n".join(lines), nlen


def main():
    date = build_date()
    print("Booting the emulator with the current binaries (~2 min) ...",
          file=sys.stderr)
    drv = Driver()
    drv.send("NEEDS SEE")
    drv.send("NEEDS DUMP")
    drv.send("HEX")

    see_a = drv.send("SEE " + WORD_A)
    da = parse_see(see_a)
    see_b = drv.send("SEE " + WORD_B)
    db = parse_see(see_b)

    block_a, len_a = layout_block(da, WORD_A, drv, "")
    block_b, len_b = layout_block(db, WORD_B, drv, " " + WORD_A)

    dump_cmds_a = ["$%s %X DUMP" % (hx(da["nfa"]), len_a + 5),
                   "$%s 2 DUMP" % hx(da["xt"] - 2)]
    dump_cmds_b = ["$%s %X DUMP" % (hx(db["nfa"]), len_b + 5),
                   "$%s 2 DUMP" % hx(db["xt"] - 2)]

    def transcript(cmd):
        out = drv.send(cmd).strip("\n")
        out = re.sub(r" ?ok\s*$", "", out)      # drop the trailing prompt
        lines = [ln for ln in out.splitlines() if ln.strip()]
        if cmd.startswith("SEE"):
            # normalise to the manual's format (SEE itself is sloppy here):
            # - drop the stray leading line with the bare length byte
            lines = [ln for ln in lines
                     if not re.fullmatch(r"\s*[0-9A-F]{1,2}\s*", ln)]
            # - zero-pad the 16-bit heap-pointer in the Lfa: line
            lines = [re.sub(r"^(\s*Lfa: [0-9A-F]{4} )([0-9A-F]{1,3})\b",
                            lambda m: m.group(1) + m.group(2).zfill(4),
                            ln)
                     for ln in lines]
        return "        " + cmd + "\n" + "\n".join(
            "        " + ln for ln in lines)

    ver_a = "\n".join([transcript("SEE " + WORD_A)] +
                      [transcript(c) for c in dump_cmds_a])
    ver_b = "\n".join([transcript("SEE " + WORD_B)] +
                      [transcript(c) for c in dump_cmds_b])

    print("=" * 72)
    print("Section 'Dictionary memory structure' -- dynamic part,")
    print("regenerated from build %s. Paste by hand into the .odt." % date)
    print("=" * 72)
    print()
    print("For example the two contiguous definitions %s and %s appears in"
          % (WORD_A, WORD_B))
    print("memory as follow (as per build %s, since it's perfectly possible"
          % date)
    print("that a different build shows different addresses).")
    print()
    print(block_a)
    print()
    print(block_b)
    print()
    print("You can verify yourself all of that by typing some commands.")
    print()
    print(ver_a)
    print()
    print(ver_b)


if __name__ == "__main__":
    main()
