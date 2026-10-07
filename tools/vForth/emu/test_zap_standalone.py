#!/usr/bin/env python3
"""ZAP standalone round trip (plan planners/ZAP-PLAN.md, phase 0).

Session 1 boots the normal core, defines a probe word, loads lib/ZAP.f and
runs `ZAP ZZT`: three files appear in the repo root (ZZT-core.bin,
ZZT-user.bin, ZZT-heap.bin).

Session 2 starts from blank RAM and does what the BASIC loader does:

    LOAD core CODE ORIGIN      LOAD user CODE <address>      LOAD heap BANK 16
    LET a = USR ORIGIN

then runs until the patched COLD reaches BYE (detected on entry to BASIC,
the code word BYE ends with) and compares what the probe printed with what
session 1 said the user variables hold.

The user-area address is the interesting parameter: the file is saved from
`R0 @`, so that is where it must go back. The test runs twice -- once at
`R0 @` and once at the address Standard-Loader.bas would use. Since
2026-10-07 the loader does not hold that number any more: line 1160 is
`LOAD d$ CODE DPEEK 25466`, i.e. it reads R0 from the core image it has
just loaded (ORIGIN+$14). Both runs must pass.

A second probe, ZZE, raises an error: the image must print "msg#n" (it is
saved with WARNING at 0) and leave through BYE, not fall to the prompt.
Session 1 must come out of both ZAPs unpatched: COLD, ABORT and WARNING as
before, nothing left on the stack, the heap file equal to the heap pages.

A third probe, ZZH, is defined after pushing HP into the second 16K bank:
ZAP must write ZZH-heap1.bin too, and session 2 -- which loads as many
banks as the HP found in the user file says, the way the loader does --
must find the probe's own name there.

Usage:  python emu/test_zap_standalone.py [--fill BYTE] [--keep]
"""
import argparse
import os
import re
import sys

EMU_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(EMU_DIR)
sys.path.insert(0, EMU_DIR)

from repl import Repl
from zxchars import zx_char

ORIGIN = 0x6366
HEAP_PAGE = 0x20                 # first 8K page of 16K bank 16
PROBE = "ZZT"
PROBE_ERR = "ZZE"
PROBE_HEAP = "ZZH"
HP_OFFSET = 26                   # user variable HP, in the user file


def files(probe):
    return [f"{probe}-{part}.bin" for part in ("core", "user", "heap")]


FILES = (files(PROBE) + files(PROBE_ERR) + files(PROBE_HEAP)
         + [f"{PROBE_HEAP}-heap1.bin"])
STEP_CAP = 30_000_000


def feed(r, line):
    r.emu.queue_input(line)
    ok = r._run_to_prompt()
    out = r._drain()
    if not ok:
        raise SystemExit(f"[emulator stopped] on: {line}\n{out}")
    return out


def run(r, line):
    out = feed(r, line)
    for _ in range(20):
        out += feed(r, ".( SYNC-MARK)")
        if "SYNC-MARK" in out:
            return out.split("SYNC-MARK")[0]
    raise SystemExit(f"[no sync] on: {line}\n{out}")


def numbers(text):
    return [int(n) for n in re.findall(r"(?<![\w#$-])\d+(?![\w-])", text)]


def loader_user_address():
    """Where Standard-Loader.bas loads the user file: line 1160,
    `LOAD d$ CODE n` or `LOAD d$ CODE DPEEK n`. In the second form the
    address is the cell at n of the core image written by session 1."""
    data = open(os.path.join(ROOT, "Standard-Loader.bas"), "rb").read()
    prog = data[128:128 + (data[20] | data[21] << 8)]
    i = 0
    while i < len(prog):
        line = prog[i] << 8 | prog[i + 1]
        size = prog[i + 2] | prog[i + 3] << 8
        body = prog[i + 4:i + 4 + size]
        i += 4 + size
        if line == 1160:
            code = body.index(0xAF)                 # CODE
            dpeek = body[code + 1] == 0x8A          # DPEEK
            num = body.index(0x0E, code)
            n = body[num + 3] | body[num + 4] << 8
            if dpeek:
                core = open(os.path.join(ROOT, files(PROBE)[0]), "rb").read()
                return core[n - ORIGIN] | core[n - ORIGIN + 1] << 8, f"DPEEK {n}"
            return n, "fixed"
    raise SystemExit("line 1160 not found in Standard-Loader.bas")


def session1():
    """Build the snapshot; return what the probe is expected to print."""
    r = Repl()
    r.boot()
    run(r, "DECIMAL")
    run(r, f": {PROBE} 90 EMIT 90 EMIT BASE @ . 12345 U. HERE U. "
           "LATEST PFA CFA U. 90 EMIT ;")
    run(r, f": {PROBE_ERR} 90 EMIT 1 33 ?ERROR 89 EMIT ;")
    run(r, "NEEDS ZAP")
    info = numbers(run(r, "R0 @ U. ' BASIC U. HERE U. LATEST PFA CFA U."))
    r0, basic_cfa, here, latest = info[-4:]
    for probe in (PROBE, PROBE_ERR):
        out = run(r, f"ZAP {probe}")
        for name in files(probe):
            if not os.path.exists(os.path.join(ROOT, name)):
                raise SystemExit(f"ZAP did not write {name}: {out}")
    live = numbers(run(r, "?PATCHED . WARNING @ . SP@ S0 @ - ."))[-3:]
    run(r, "$0000 FAR DROP")
    pages = bytes(r.emu.memory[0xE000:0x10000])
    run(r, "$2000 FAR DROP")
    pages += bytes(r.emu.memory[0xE000:0x10000])
    heap_ok = pages == open(os.path.join(ROOT, files(PROBE_ERR)[2]),
                            "rb").read()
    run(r, "HEX 4100 HP ! DECIMAL")
    run(r, f": {PROBE_HEAP} 90 EMIT LATEST ID. 90 EMIT ;")
    run(r, f"ZAP {PROBE_HEAP}")
    for handle in list(r.emu.file_handles.values()):
        try:
            handle.close()
        except Exception:
            pass
    expected = f"ZZ10 12345 {here} {latest} Z"
    return r0, basic_cfa, expected, live, heap_ok


def session2(probe, user_addr, basic_cfa, fill):
    """Replay the BASIC loader on blank RAM; return (text, how it ended)."""
    from emulator import VForthEmulator
    emu = VForthEmulator()
    emu.max_instructions = 10 ** 12
    emu.trace_enabled = False
    emu.input_echo = False
    if fill:
        emu.memory[0x4000:0x10000] = bytes([fill]) * 0xC000

    def blob(name):
        return open(os.path.join(ROOT, name), "rb").read()

    core, user, heap = (blob(n) for n in files(probe))
    hp = user[HP_OFFSET] | user[HP_OFFSET + 1] << 8
    for bank in range(1, hp // 16384 + 1):      # what the loader works out
        more = blob(f"{probe}-heap{bank}.bin")
        emu.cpu.mmu7_pages[HEAP_PAGE + 2 * bank] = bytes(more[:0x2000])
        emu.cpu.mmu7_pages[HEAP_PAGE + 2 * bank + 1] = bytes(more[0x2000:])
    emu.memory[ORIGIN:ORIGIN + len(core)] = core
    emu.memory[user_addr:user_addr + len(user)] = user
    emu.cpu.mmu7_page = HEAP_PAGE
    emu.memory[0xE000:0x10000] = heap[:0x2000]
    emu.cpu.mmu7_pages[HEAP_PAGE + 1] = bytes(heap[0x2000:0x4000])
    emu.initialize_cold_start()

    raw = bytearray()
    emu.handle_emit = lambda: raw.append(emu.cpu.A & 0xFF)

    ending = "step cap reached (no BYE)"
    for _ in range(STEP_CAP):
        if emu.cpu.PC == basic_cfa:
            ending = "BYE"
            break
        try:
            emu.dispatch(emu.cpu.fetch_byte())
            emu.instr_count += 1
        except StopIteration:
            ending = "emulator halted"
            break
        except Exception as exc:
            ending = f"emulator error: {exc}"
            break
    text = "".join(zx_char(b) for b in raw if b >= 0x20)
    return text, ending


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fill", type=lambda s: int(s, 0), default=0,
                    help="byte RAM holds before the loader runs (default 0)")
    ap.add_argument("--keep", action="store_true",
                    help="leave the three .bin files in the repo root")
    args = ap.parse_args()

    os.chdir(ROOT)
    try:
        r0, basic_cfa, expected, live, heap_ok = session1()
        stale, how = loader_user_address()
        print()
        print(f"R0 @ = {r0}   Standard-Loader.bas loads user at {stale} ({how})"
              f"   expected output: {expected!r}")
        print()

        results = []
        for label, addr in (("R0 @", r0), ("Standard-Loader.bas", stale)):
            text, ending = session2(PROBE, addr, basic_cfa, args.fill)
            ok = text.strip() == expected and ending == "BYE"
            results.append(ok)
            print(f"user at {addr:5d} ({label}): "
                  f"{'PASS' if ok else 'FAIL'}  [{ending}]  {text[:120]!r}")

        text, ending = session2(PROBE_ERR, r0, basic_cfa, args.fill)
        err_ok = (ending == "BYE" and text.startswith("Z")
                  and "msg#33" in text.replace(" ", "") and "Y" not in text)
        print(f"error inside the image: {'PASS' if err_ok else 'FAIL'}"
              f"  [{ending}]  {text[:120]!r}")
        text, ending = session2(PROBE_HEAP, r0, basic_cfa, args.fill)
        bank_ok = ending == "BYE" and text.strip() == f"Z{PROBE_HEAP} Z"
        print(f"name in the second heap bank: {'PASS' if bank_ok else 'FAIL'}"
              f"  [{ending}]  {text[:120]!r}")
        live_ok = live == [0, 1, 0]
        print(f"live session after two ZAPs (?PATCHED WARNING depth = "
              f"{live}): {'PASS' if live_ok else 'FAIL'}")
        print(f"heap file equals heap pages: {'PASS' if heap_ok else 'FAIL'}")
    finally:
        if not args.keep:
            for name in FILES:
                if os.path.exists(os.path.join(ROOT, name)):
                    os.remove(os.path.join(ROOT, name))

    sys.exit(0 if all(results) and err_ok and bank_ok and live_ok and heap_ok else 1)


if __name__ == "__main__":
    main()
