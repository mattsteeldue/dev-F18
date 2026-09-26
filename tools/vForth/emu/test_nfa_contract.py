#!/usr/bin/env python3
"""Dictionary-name contract without ?HEAP_PTR / ?>HEAP (plan
planners/PLAN-NFA-AMBIGUITY.md).

Since the core stopped guessing "heap-pointer or real address" with a
numeric threshold, a heap-pointer (ha) and a resolved nfa are told apart by
position alone:

  - LFA content, vocabulary cell, mirror cell before the CFA, HP and the
    cells MARKER saves are always an ha;
  - the nfa taken or returned by ID., PFA, NFA, <NAME, LATEST is always a
    resolved address in the MMU7 window.

With the threshold gone, names can be laid down anywhere in the heap: this
script defines words with HP set well past the old $6000 limit ((FIND) used
`sub $60`) and checks name <-> xt navigation, FORGET, MARKER and the library
words that walk links (SEE, :NONAME, ?VOCAB).

Usage:  python emu/test_nfa_contract.py
"""
import os
import sys

EMU_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, EMU_DIR)

from repl import Repl


def feed(r, line):
    r.emu.queue_input(line)
    ok = r._run_to_prompt()
    out = r._drain()
    if not ok:
        raise SystemExit(f"[emulator stopped] on: {line}\n{out}")
    return out


def run(r, line):
    # a long silent run (INCLUDE, SEE) can look idle to the prompt
    # heuristic and its output then lags behind: keep going until a
    # marker typed after the line has been echoed back
    out = feed(r, line)
    for _ in range(20):
        out += feed(r, ".( SYNC-MARK)")
        if "SYNC-MARK" in out:
            return out.split("SYNC-MARK")[0]
    raise SystemExit(f"[no sync] on: {line}\n{out}")


CHECKS = [
    # (forth line, substrings expected in the output, in order)
    ("HEX ' DUP <NAME ID. ' DUP >BODY LFA @ FAR ID.", ["DUP SWAP"]),
    ("' SPLASH >BODY NFA PFA ' SPLASH >BODY = .", ["-1"]),
    ("MARKER MK HP@ U.", []),
    ("5F00 HP ! : W5 55 ; W5 .", ["55"]),
    ("6400 HP ! : W6 66 ; W6 . W5 .", ["66 55"]),
    ("' W6 <NAME DUP U. ID.", ["E400 W6"]),
    ("' W6 >BODY NFA PFA CFA ' W6 = .", ["-1"]),
    ("' W6 >BODY LFA @ FAR ID.", ["W5"]),
    ("C000 HP ! : WC 77 ; WC . ' WC <NAME ID.", ["77 WC"]),
    ("E400 HP ! : WE 88 ; WE . ' WE <NAME ID. LATEST ID.", ["88 WE WE"]),
    ("LATEST PFA ' WE >BODY = .", ["-1"]),
    ("FORGET WE HP@ U. WC .", ["E400 77"]),
    ("MK W6", ["W6? "]),
    ("NEEDS :NONAME", []),
    (":NONAME 7 . ; DUP EXECUTE <NAME DUP C@ . 1+ C@ .", ["7 81 A0"]),
    ("NEEDS SEE", []),
    ("6400 HP ! : S1 1 ; : S2 S1 2 ; SEE S2", ["Lfa:", "S1", "EXIT"]),
    ("NEEDS ?VOCAB", []),
    ("?VOCAB", ["Current", "FORTH", "Context", "FORTH"]),
    ("DECIMAL 1 2 + .", ["3"]),
]


def main():
    r = Repl()
    r.boot()
    failed = 0
    for line, want in CHECKS:
        out = run(r, line)
        pos, miss = 0, None
        for w in want:
            k = out.find(w, pos)
            if k < 0:
                miss = w
                break
            pos = k + len(w)
        status = "FAIL" if miss is not None else "ok"
        if miss is not None:
            failed += 1
        print(f"[{status}] {line}")
        if miss is not None:
            print(f"       expected {miss!r} in: {out.strip()!r}")
    print(f"\n{len(CHECKS) - failed}/{len(CHECKS)} checks passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
