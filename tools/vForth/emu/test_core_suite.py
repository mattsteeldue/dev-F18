#!/usr/bin/env python3
"""Run a test/ suite (default test/CORE-TESTS.f) in the headless emulator
and judge its output the way the author reads it on CSpect.

How the suite talks (see test/CLAUDE.md, "Reading the output"):
  - the NEEDS at the top load every dependency first, so their banners
    come before any real test;
  - every group is announced by TESTING, which just echoes the rest of its
    line (the leading backslash is decoration): "TESTING \\ F.3.1 Basic
    Assumptions" prints "\\ F.3.1 Basic Assumptions";
  - a passing T{ ... }T is silent; a failing one goes through ERROR1 of
    lib/testing.f: the source line, then message #50-#54 ("Incorrect
    result.", "Wrong number of results.", ...), then .S;
  - near the end, test/accept.f runs ACCEPT, which waits for one line of
    keyboard input and echoes it back as RECEIVED: "...";
  - "GDX has already been defined." is expected: test/_.f (F.6.1.0450)
    redefines GDX on purpose and then prints, via TESTING, two lines
    saying it is correct to see that message (the warning itself comes
    out just before them); F.3.23 in CORE-TESTS.f redefines GDX twice more
    for the same reason. Any other "has already been defined" is flagged.

Usage:  python emu/test_core_suite.py [test/OTHER-TESTS.f]
Exit 0 when the suite ran to the end with no failure.
"""
import os
import sys

EMU_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, EMU_DIR)

from repl import Repl

ACCEPT_INPUT = "ACCEPT typed by test_core_suite.py"
SYNC = "SYNC-MARK"

# messages #50-#54 of the block file, printed by ERROR1 on a failed T{ }T
TEST_FAILURES = (
    "Incorrect result.",
    "Wrong number of results.",
    "does not match ...}T spec.",
    "does not match.",
)
# core errors that abort the INCLUDE (ERROR -> QUIT)
CORE_ERRORS = ("is undefined", "Can't be executed", "Stack empty",
               "Stack full", "File not found", "Definition not finished")
EXPECTED_REDEF = "GDX"                 # the only word redefined on purpose
EXPECTED_GROUPS = ("F.6.1.0450", "F.3.23")
EXPECTED_NOTE = "It's correct seeing this message"


def feed(r, line):
    r.emu.queue_input(line)
    ok = r._run_to_prompt()
    out = r._drain()
    if not ok:
        raise SystemExit(f"[emulator stopped] on: {line}\n{out}")
    return out


def run_suite(suite):
    r = Repl()
    r.boot()
    # the ACCEPT reply is queued right behind the INCLUDE: nothing else in
    # the suite reads the keyboard, so ACCEPT is the one that consumes it
    r.emu.queue_input("INCLUDE " + suite)
    r.emu.queue_input(ACCEPT_INPUT)
    ok = r._run_to_prompt()
    out = r._drain()
    if not ok:
        raise SystemExit(f"[emulator stopped]\n{out}")
    for _ in range(40):                 # see test_nfa_contract.py: run()
        out += feed(r, f".( {SYNC})")
        if SYNC in out:
            break
    else:
        raise SystemExit(f"[no sync]\n{out}")
    return out.split(SYNC)[0]


def judge(out):
    lines = out.split(chr(10))
    bs = chr(92)                        # the decorative backslash
    sections, problems, gdx_seen, group = [], [], 0, ""
    for i, l in enumerate(lines):
        t = l.strip()
        if t.startswith("TESTING"):     # the whole line may be echoed
            t = t[len("TESTING"):].strip()
        if t.startswith(bs + " F.") or t.startswith("F."):
            group = t.lstrip(bs + " ")
            if t.startswith(bs):
                sections.append(t)
        if "has already been defined" in l and EXPECTED_NOTE not in l:
            if (l.strip().startswith(EXPECTED_REDEF + " ")
                    and any(group.startswith(g) for g in EXPECTED_GROUPS)):
                gdx_seen += 1
            elif "TESTING" not in l:
                problems.append(("warning", i, l))
        if any(k in l for k in TEST_FAILURES) or any(k in l for k in CORE_ERRORS):
            problems.append(("failure", i, l))
    received = [l.strip() for l in lines if l.strip().startswith("RECEIVED:")]
    note_seen = any(EXPECTED_NOTE in l for l in lines)
    return sections, problems, gdx_seen and note_seen, received


def main():
    suite = sys.argv[1] if len(sys.argv) > 1 else "test/CORE-TESTS.f"
    out = run_suite(suite)
    lines = out.split("\n")
    sections, problems, gdx_seen, received = judge(out)

    print(f"\n{suite}: {len(sections)} sections announced by TESTING")
    for s in sections:
        print("   ", s)
    bad = bool(problems)
    for kind, i, l in problems:
        print(f"[{kind}] {l.strip()}")
        for c in lines[max(0, i - 2):i + 2]:      # source line and .S around
            print("        |", c)
    if "CORE-TESTS" in suite.upper():
        want = f'RECEIVED: "{ACCEPT_INPUT}"'
        if not any(want in l for l in received):
            bad = True
            print(f"[failure] ACCEPT: expected {want!r}, got {received!r}")
        if not gdx_seen:
            bad = True
            print("[failure] the expected 'GDX has already been defined.' "
                  "warning did not appear")
    print("\nRESULT:", "FAILED" if bad else "all tests passed")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
