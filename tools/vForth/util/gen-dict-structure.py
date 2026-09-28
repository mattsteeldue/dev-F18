#!/usr/bin/env python3
"""
gen-dict-structure.py -- regenerate the dynamic text of the manual
(vForth1.8-core-en .odt) sections that contain build-specific addresses:

  par. 4.6 "Dictionary memory structure": for the two contiguous
  definitions SWAP and DUP,
    1. the "Heap memory / Main memory" layout tables (NFA/LFA/CFA,
       mirror, xt)
    2. the "You can verify yourself" transcript (SEE + DUMP output)

  par. 3.8 "Debugger Utility": the three SEE example transcripts
  (TYPE: colon-definition, NIP: CODE word, IF: IMMEDIATE), plus the
  data for the prose note about the bytes following NIP's jp (ix).

All of these go stale on every core rebuild. This script boots the
headless emulator with the CURRENT binaries, reads the real bytes and
captures the real SEE/DUMP output, then prints the paragraphs ready to
be pasted by hand into the .odt (which must NEVER be edited
automatically). Every block of output is labelled with the manual
paragraph it belongs to.

At the end each block is compared with the text already in the manual
(the newest doc/vForth1.8-core-en-*.odt, or --odt PATH), read-only from
its content.xml: INVARIATO means nothing to paste, DA AGGIORNARE lists
the lines not found in the manual. The comparison works on whitespace-
and "|"-separated tokens, so line breaks, table cells and spacing of the
.odt do not matter; when in doubt it reports DA AGGIORNARE, never a
false INVARIATO.

Usage (from tools/vForth, takes ~2 minutes for the boot):

    python3 util/gen-dict-structure.py [--odt PATH | --no-compare]
"""
import os
import re
import sys
import contextlib
import glob
import html
import io
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "emu"))
os.chdir(ROOT)

WORD_A, WORD_B = "SWAP", "DUP"          # par. 4.6
DEBUGGER_WORDS = ["TYPE", "NIP", "IF"]  # par. 3.8

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


def heap_name(drv, nfa_addr):
    """Read a definition name from its NFA in the heap window."""
    nlen = drv.mem(nfa_addr, 1)[0] & 0x1F
    return "".join(chr(b & 0x7F) for b in drv.mem(nfa_addr + 1, nlen))


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


# --- comparison with the text already in the manual (read-only) --------

# typographic characters LibreOffice/Word may have put in the .odt
TYPO = str.maketrans({"\u2018": "'", "\u2019": "'", "\u201c": '"',
                      "\u201d": '"', "\u2013": "-", "\u2014": "-",
                      "\u00a0": " ", "\u00ad": None, "\u200b": None})


def tokens(text):
    return [t for t in re.split(r"[\s|]+", text.translate(TYPO)) if t]


def odt_tokens(path):
    """Plain-text tokens of the .odt body. Spaces, tabs, line breaks and
    paragraph/cell ends become separators; every other tag (spans,
    bookmarks) is dropped without one, so words split across styles stay
    whole."""
    x = zipfile.ZipFile(path).read("content.xml").decode("utf-8")
    x = re.sub(r"<text:s(?: [^>]*)?/>|<text:tab/>|<text:line-break/>"
               r"|</text:p>|</text:h>|</table:table-cell>", " ", x)
    return tokens(html.unescape(re.sub(r"<[^>]+>", "", x)))


def contains(hay, needle):
    if not needle:
        return True
    n, first = len(needle), needle[0]
    return any(hay[i:i + n] == needle
               for i, t in enumerate(hay) if t == first)


def default_odt():
    found = sorted(glob.glob("doc/vForth1.8-core-en-*.odt"))
    return found[-1] if found else None


def compare_with_manual(blocks, odt):
    print()
    print("=" * 72)
    print("Comparison with the manual: %s" % odt)
    print("=" * 72)
    try:
        hay = odt_tokens(odt)
    except (OSError, KeyError, zipfile.BadZipFile) as e:
        print("  not readable (%s): open in LibreOffice? Check by hand." % e)
        return
    todo = 0
    for label, text in blocks:
        if contains(hay, tokens(text)):
            print("  INVARIATO     %s" % label)
            continue
        todo += 1
        print("  DA AGGIORNARE %s" % label)
        missing = [ln.strip() for ln in text.splitlines()
                   if tokens(ln) and not contains(hay, tokens(ln))]
        for ln in missing:
            print("      ! %s" % ln)
        if not missing:
            print("      (every line is in the manual, but not in this order:"
                  " check by hand)")
    print()
    print("  %d block(s) to update, %d unchanged."
          % (todo, len(blocks) - todo))


def main():
    args = sys.argv[1:]
    odt = None
    if "--no-compare" not in args:
        odt = args[args.index("--odt") + 1] if "--odt" in args else default_odt()
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

    def transcript(cmd, pad_lfa=True, raw=None):
        out = raw if raw is not None else drv.send(cmd)
        out = re.sub(r" ?ok\s*$", "", out.strip("\n"))  # drop trailing prompt
        # keep printable ASCII only (SEE may emit attribute control codes
        # for the inverse-video literals)
        out = "".join(c for c in out if 32 <= ord(c) < 127 or c == "\n")
        lines = [ln for ln in out.splitlines() if ln.strip()]
        if cmd.startswith("SEE"):
            # normalise (SEE itself is sloppy here):
            # - drop the stray leading line with the bare length byte
            #   (2 hex digits in HEX base, up to 3 digits in DECIMAL)
            lines = [ln for ln in lines
                     if not re.fullmatch(r"\s*[0-9A-F]{1,3}\s*", ln)]
            # - zero-pad the 16-bit heap-pointer in the Lfa: line; the
            #   manual does this in par. 4.6 but keeps SEE's raw output
            #   in par. 3.8
            if pad_lfa:
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

    # --- par. 3.8 Debugger Utility: SEE example transcripts -----------
    # The manual shows these in DECIMAL (e.g. the literal 12 in TYPE's
    # body); SEE prints addresses in hex regardless of BASE.
    drv.send("DECIMAL")
    dbg = {}
    for w in DEBUGGER_WORDS:
        dbg[w] = drv.send("SEE " + w)
    drv.send("HEX")

    # data for the prose note after SEE NIP: the bytes that follow
    # jp (ix) are the Mirror of the subsequent definition
    dnip = parse_see(dbg["NIP"])
    nip_code = drv.mem(dnip["xt"], 16)
    nip_end = nip_code.find(b"\xDD\xE9") + 2
    trail = nip_code[nip_end:nip_end + 4]
    next_cfa_hp = trail[0] | (trail[1] << 8)
    next_nfa = dnip["lfa"] + 4          # heap entries are contiguous
    next_name = heap_name(drv, next_nfa)
    # what "$<mirror> FAR 8 DUMP" shows: the next word's xt (its CFA
    # slot), then the NFA of the word after it
    next_cfa = 0xE000 + next_cfa_hp
    next_xt_bytes = drv.mem(next_cfa, 2)
    next_xt = next_xt_bytes[0] | (next_xt_bytes[1] << 8)
    after_name = heap_name(drv, next_cfa + 2)

    print("=" * 72)
    print("Manual dynamic parts regenerated from build %s." % date)
    print("Paste by hand into the .odt; every block is labelled with the")
    print("manual paragraph it belongs to.")
    print("=" * 72)
    print()
    print("-" * 72)
    print("[par. 4.6 -- Dictionary memory structure]")
    print("-" * 72)
    blocks = []                 # (label, text) compared with the manual

    def emit(label, text, compare=None):
        print(text)
        blocks.append((label, text if compare is None else compare))

    print()
    emit("par. 4.6 intro sentence",
         "For example the two contiguous definitions %s and %s appears in\n"
         "memory as follow (as per build %s, since it's perfectly possible\n"
         "that a different build shows different addresses)."
         % (WORD_A, WORD_B, date))
    print()
    emit("par. 4.6 table %s" % WORD_A, block_a)
    print()
    emit("par. 4.6 table %s" % WORD_B, block_b)
    print()
    print("You can verify yourself all of that by typing some commands.")
    print()
    emit("par. 4.6 transcript %s" % WORD_A, ver_a)
    print()
    emit("par. 4.6 transcript %s" % WORD_B, ver_b)
    print()
    print("-" * 72)
    print("[par. 3.8 -- Debugger Utility]")
    print("-" * 72)
    for w in DEBUGGER_WORDS:
        print()
        print("[par. 3.8 -- transcript: SEE %s]" % w)
        print()
        t = transcript("SEE " + w, pad_lfa=False, raw=dbg[w])
        # the manual puts prose between the command and its output
        # ("the system will show ..."): compare the output only
        output = t.split(chr(10), 1)[1]
        emit("par. 3.8 SEE %s" % w, t, compare=output)
    print()
    print("[par. 3.8 -- data for the prose note after SEE NIP]")
    print()
    print("  bytes following NIP's jp (ix): %s" % pairs(trail))
    print("  $%s FAR 8 DUMP shows: %s (%s's xt $%s) + %s's NFA"
          % (hx(next_cfa_hp), pairs(drv.mem(next_cfa, 8)), next_name,
             hx(next_xt), after_name))
    print()
    emit("par. 3.8 note after SEE NIP",
         "The bytes that follow  - %s - are the beginning of the subsequent\n"
         "definition compiled in dictionary (%s in this case): %s is %s's\n"
         "Mirror, i.e. the heap-pointer $%s to its CFA. Try $%s FAR 8 DUMP to\n"
         "inspect the HEAP: you'll see %s's xt $%s followed by %s's NFA."
         % (pairs(trail), next_name, pairs(trail[:2]), next_name,
            hx(next_cfa_hp), hx(next_cfa_hp), next_name, hx(next_xt),
            after_name))

    if odt:
        compare_with_manual(blocks, odt)


if __name__ == "__main__":
    main()
