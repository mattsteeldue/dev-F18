#!/usr/bin/env python3
r"""
Extract the NextBASIC listings of doc/basic-to-vforth/ into bas2f/txt/.

A BASIC listing in a chapter is a fenced block with no language tag:

    ```
    10 PRINT "Hello"
    ```

(Forth blocks are tagged ```forth, outputs ```text.) The listings of chapter
NN-title.md are numbered in order of appearance and written as

    bas2f/txt/NN-title-MM.txt

7-bit ASCII, LF line ends, headed by "#program NN-title-MM": the directive
that names the .bas both for txt2bas (Remy Sharp's NextBASIC VS Code
extension, "NextBASIC: export to binary .bas") and for .TXT2BAS on the Next.
The chapters are the source: edit the .md, then run this script again. A file
is rewritten only when its content changes.

Each listing is checked for lines without a line number and for characters
outside 0x20-0x7E.

    python util/guide-listings.py            # write bas2f/txt/*.txt
    python util/guide-listings.py --check    # exit 1 if any .txt is out of date

The .bas themselves come from txt2bas; only the listings the author has
reviewed go into git (planners/BASIC-TO-FORTH-PLAN.md, section 0).
"""
import os
import re
import sys
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUIDE_DIR = os.path.join(ROOT, "doc", "basic-to-vforth")
OUT_DIR = os.path.join(ROOT, "bas2f", "txt")


def listings(path):
    """Return the untagged fenced blocks of a chapter, as lists of lines."""
    blocks, cur, inside = [], None, False
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")
    for ln in lines:
        if not inside and ln.startswith("```"):
            inside = True
            cur = [] if ln.strip() == "```" else None
        elif inside and ln.strip() == "```":
            inside = False
            if cur is not None:
                blocks.append(cur)
        elif inside and cur is not None:
            cur.append(ln)
    return blocks


def main():
    check = "--check" in sys.argv[1:]
    stale = problems = 0
    for md in sorted(glob.glob(os.path.join(GUIDE_DIR, "[0-9][0-9]-*.md"))):
        base = os.path.splitext(os.path.basename(md))[0]
        for i, block in enumerate(listings(md), 1):
            name = "%s-%02d" % (base, i)
            text = "#program %s\n" % name + "\n".join(block) + "\n"
            for ln in block:
                if not re.match(r"^\d+ ", ln):
                    print("%s: line without a number: %r" % (name, ln))
                    problems += 1
            bad = sorted({c for c in text
                          if c != "\n" and not " " <= c <= "~"})
            if bad:
                print("%s: characters outside 7-bit ASCII: %r" % (name, bad))
                problems += 1
            out = os.path.join(OUT_DIR, name + ".txt")
            try:
                with open(out, encoding="ascii", newline="") as f:
                    old = f.read()
            except (OSError, UnicodeDecodeError):
                old = None
            if old == text:
                continue
            stale += 1
            if check:
                print("%s.txt is out of date" % name)
            elif not bad:
                os.makedirs(OUT_DIR, exist_ok=True)
                with open(out, "w", encoding="ascii", newline="\n") as f:
                    f.write(text)
                print("%s.txt written" % name)
    if check:
        sys.exit(1 if stale or problems else 0)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
