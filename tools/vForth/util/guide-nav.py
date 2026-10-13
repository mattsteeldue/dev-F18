#!/usr/bin/env python3
r"""
Write the navigation footer of every chapter of doc/basic-to-vforth/.

Each chapter file (NN-title.md, app-*.md) ends with a footer that links the
previous chapter, the index (README.md) and the next chapter:

    <!-- nav -->
    ---

    Previous: [Chapter 5 - READ, DATA, RESTORE](05-read-data-restore.md) |
    [Contents](README.md) |
    Next: [Chapter 7 - Strings](07-strings.md)

The order is the alphabetical order of the file names, which is the order
of the chapters. Titles are taken from the first heading of each file. The
first chapter has no "Previous"; for the last one written, "Next" names the
following chapter of the index without a link, because the file is not there
yet (emu/test_basic_guide.py reports a link to a missing file).

The footer is everything from the line "<!-- nav -->" to the end of the
file: the script replaces it, or appends it when missing, so it can be run
again whenever a chapter is added.

    python util/guide-nav.py            # rewrite the footers
    python util/guide-nav.py --check    # exit 1 if any footer is out of date
"""
import os
import re
import sys
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUIDE_DIR = os.path.join(ROOT, "doc", "basic-to-vforth")
MARK = "<!-- nav -->"
HEADING = re.compile(r"^# (.+?)\s*$", re.M)
INDEX = re.compile(r"^(\d+)\. (?:\[([^\]]+)\]\([^)]*\)|(.+?))\s*$", re.M)


def title(path):
    with open(path, encoding="ascii") as f:
        m = HEADING.search(f.read())
    return m.group(1) if m else os.path.basename(path)


def index_titles():
    """Chapter number -> title, from the numbered list of README.md."""
    with open(os.path.join(GUIDE_DIR, "README.md"), encoding="ascii") as f:
        text = f.read()
    return {int(n): (a or b) for n, a, b in INDEX.findall(text)}


def footer(prev, nxt, coming):
    parts = []
    if prev:
        parts.append(f"Previous: [{title(prev)}]({os.path.basename(prev)})")
    parts.append("[Contents](README.md)")
    if nxt:
        parts.append(f"Next: [{title(nxt)}]({os.path.basename(nxt)})")
    elif coming:
        parts.append(f"Next: {coming} (not written yet)")
    return MARK + "\n---\n\n" + " |\n".join(parts) + "\n"


def main():
    check = "--check" in sys.argv[1:]
    files = sorted(p for p in glob.glob(os.path.join(GUIDE_DIR, "*.md"))
                   if os.path.basename(p) != "README.md")
    names = index_titles()
    stale = 0
    for i, path in enumerate(files):
        prev = files[i - 1] if i else None
        nxt = files[i + 1] if i + 1 < len(files) else None
        coming = None
        m = re.match(r"(\d+)-", os.path.basename(path))
        if not nxt and m and int(m.group(1)) + 1 in names:
            n = int(m.group(1)) + 1
            coming = f"Chapter {n} - {names[n]}"
        with open(path, encoding="ascii", newline="") as f:
            old = f.read()
        body = old.split(MARK)[0].rstrip("\n") + "\n\n"
        new = body + footer(prev, nxt, coming)
        if new != old:
            stale += 1
            print(("stale: " if check else "updated: ")
                  + os.path.basename(path))
            if not check:
                with open(path, "w", encoding="ascii", newline="") as f:
                    f.write(new)
    if not stale:
        print("all footers up to date")
    return 1 if check and stale else 0


if __name__ == "__main__":
    sys.exit(main())
