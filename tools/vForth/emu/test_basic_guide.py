#!/usr/bin/env python3
r"""
Re-run the Forth snippets of doc/basic-to-vforth/*.md in the headless emulator.

The guide stays aligned with the core the same way the tests do: every fenced
```forth block is typed, line by line, at the vForth prompt and its output is
compared with what the guide claims.

The guide is one file per chapter (NN-title.md; README.md is the index). The
chapter is named by the file's first heading, "# Chapter N - Title".

Conventions the guide follows (see "How to read this guide" in README.md):

  * a line ending in   \ => text   must print `text` (blanks are collapsed,
    the match is "contains", so an error message can be claimed the same way);
  * a ```text block right after a ```forth block is the output of the LAST
    line of that forth block (used when the output spans several lines);
  * a line without a claim must not raise an error;
  * a block preceded by the line  <!-- no-test -->  is skipped (keyboard
    input, endless loops, hardware the emulator does not model);
  * lines are 80 bytes or fewer, 7-bit ASCII, no TAB;
  * links between the files keep the .md form, [text](NN-title.md), and
    must point to a file that exists.

Run from the repo root:

    python emu/test_basic_guide.py              # the whole guide
    python emu/test_basic_guide.py --chapter 3  # one chapter
    python emu/test_basic_guide.py --list       # show the snippets, do not run

Boot takes about two minutes; allow a few seconds per snippet line.
Exit status: 0 when every claim holds, 1 otherwise.
"""
import os
import re
import sys
import glob
import argparse

EMU_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(EMU_DIR)
sys.path.insert(0, EMU_DIR)

GUIDE_DIR = os.path.join(ROOT, "doc", "basic-to-vforth")
NO_TEST = "<!-- no-test -->"
CLAIM = re.compile(r"\\ => (.*)$")
CHAPTER = re.compile(r"^# (?:Chapter|Appendix) (\w+)")
LINK = re.compile(r"\]\(([^)#\s]+\.md)(?:#[^)]*)?\)")
ERROR = re.compile(r"\S\? \S")          # "WORD? message." as ERROR prints it
MAX_WAITS = 10                          # run-to-prompt retries per line


class Block:
    def __init__(self, name, chapter, lineno):
        self.name = name                # file the block comes from
        self.chapter = chapter
        self.lineno = lineno            # line of the opening fence
        self.lines = []                 # (lineno, text)
        self.output = None              # text of a trailing ```text block


def parse(path):
    """Return the testable forth blocks and the list of format complaints."""
    with open(path, "rb") as f:
        raw = f.read()
    name = os.path.basename(path)
    complaints = []
    text = raw.decode("ascii", errors="replace").replace("\r\n", "\n")
    lines = text.split("\n")
    blocks, chapter, last_text, i = [], "-", "", 0
    while i < len(lines):
        line = lines[i]
        m = CHAPTER.match(line)
        if m:
            chapter = m.group(1)
        for target in LINK.findall(line):
            if "://" not in target and not os.path.isfile(
                    os.path.join(os.path.dirname(path), target)):
                complaints.append(
                    f"{name}:{i + 1}: link to missing file {target}")
        if line.strip() == "```forth":
            skip = last_text == NO_TEST
            blk = Block(name, chapter, i + 1)
            i += 1
            while i < len(lines) and lines[i].strip() != "```":
                blk.lines.append((i + 1, lines[i]))
                i += 1
            for n, t in blk.lines:
                if len(t) > 80:
                    complaints.append(f"{name}:{n}: longer than 80 bytes")
                if "\t" in t or any(ord(c) > 126 for c in t):
                    complaints.append(f"{name}:{n}: TAB or non-ASCII byte")
            j = i + 1                   # a ```text block right after?
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines) and lines[j].strip() == "```text":
                j += 1
                out = []
                while j < len(lines) and lines[j].strip() != "```":
                    out.append(lines[j])
                    j += 1
                blk.output = "\n".join(out)
                i = j
            if not skip:
                blocks.append(blk)
            last_text = ""
        elif line.strip():
            last_text = line.strip()
        i += 1
    return blocks, complaints


def parse_guide():
    """Parse every file of the guide, chapters in order (README.md last)."""
    blocks, complaints = [], []
    for path in sorted(glob.glob(os.path.join(GUIDE_DIR, "*.md"))):
        b, c = parse(path)
        blocks += b
        complaints += c
    return blocks, complaints


def squeeze(s):
    return " ".join(s.split())


def open_definitions(depth, code):
    """Track ': ... ;' nesting: inside a definition vForth prints no 'ok'."""
    for tok in code.split():
        if tok == ":":
            depth += 1
        elif tok == ";" and depth:
            depth -= 1
    return depth


def run(blocks):
    import repl
    r = repl.Repl(load_utils=False)
    print("Booting vForth ...", flush=True)
    r.emu.queue_input("n")
    r._run_to_prompt()
    r._drain()

    failures = 0
    for blk in blocks:
        print(f"\n-- chapter {blk.chapter}, {blk.name}:{blk.lineno}",
              flush=True)
        depth = 0
        runnable = [(n, t) for n, t in blk.lines
                    if t.strip() and not t.lstrip().startswith("\\")]
        for k, (n, t) in enumerate(runnable):
            m = CLAIM.search(t)
            claim = m.group(1) if m else None
            code = CLAIM.sub("", t).rstrip()
            if claim is None and blk.output and k == len(runnable) - 1:
                claim = blk.output
            depth = open_definitions(depth, code)
            r.emu.queue_input(code)
            out = ""
            for _ in range(MAX_WAITS):
                r._run_to_prompt()
                out += r._drain()
                flat = squeeze(out)
                if depth or flat.endswith("ok") or ERROR.search(flat):
                    break
            flat = squeeze(out)
            if claim is not None:
                good = squeeze(claim) in flat
            else:
                good = not ERROR.search(flat)
            if ERROR.search(flat):
                depth = 0               # ERROR ends in QUIT: back to interpret
            if not good:
                failures += 1
            tag = "ok  " if good else "FAIL"
            print(f"{tag} {n:5d}: {code.strip()}", flush=True)
            if not good:
                if claim is not None:
                    print(f"           claimed: {squeeze(claim)}")
                print(f"           printed: {flat}", flush=True)
    return failures


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--chapter", help="run only this chapter (e.g. 3, B)")
    ap.add_argument("--list", action="store_true",
                    help="list the snippets without booting the emulator")
    args = ap.parse_args()

    blocks, complaints = parse_guide()
    if args.chapter:
        blocks = [b for b in blocks if b.chapter == args.chapter]
    for c in complaints:
        print("FORMAT", c)
    if args.list:
        for b in blocks:
            print(f"\n-- chapter {b.chapter}, {b.name}:{b.lineno}")
            for n, t in b.lines:
                print(f"{n:5d}: {t}")
            if b.output is not None:
                print("       output claimed:")
                for t in b.output.split("\n"):
                    print(f"       | {t}")
        return 1 if complaints else 0
    if not blocks:
        print("no testable forth block found")
        return 1

    failures = run(blocks)
    total = sum(1 for b in blocks for n, t in b.lines
                if t.strip() and not t.lstrip().startswith("\\"))
    print(f"\n{total} lines run, {failures} failed, "
          f"{len(complaints)} format complaints")
    return 1 if failures or complaints else 0


if __name__ == "__main__":
    sys.exit(main())
