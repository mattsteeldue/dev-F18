#!/usr/bin/env python3
r"""
Extract the Forth translations of the NextBASIC listings of
doc/basic-to-vforth/ into bas2f/f/, one file per listing, to try them under
vForth with INCLUDE.

The BASIC listing MM of chapter NN-title.md (bas2f/txt/NN-title-MM.txt) is
paired with the ```forth blocks that follow it in "Side by side", up to the
next listing or heading; the file is

    bas2f/f/NN-MM.f

When the listing has several forth blocks (alternatives, or a program built
step by step), each one gets a file of its own: NN-MM.f, NN-MMb.f,
NN-MMc.f, ...

The guide's test (emu/test_basic_guide.py) types every block in one
session, so a block may use words defined earlier, often under "What
changes". Each file is made self-contained: the blocks that define the
words it uses (and, in turn, the words those use) are copied in front of
it, in the order of the guide. They come from the same chapter, or from an
earlier one for a name neither the core nor NEEDS knows. A listing the
guide answers only in prose ("That is SHOW, in What changes") gets its
blocks the same way, from the words named in that prose (see PROSE).

What is copied is the guide's text, with these changes:

  * the BASIC listing is repeated at the top, as comments;
  * a line whose claim is an error report (\ => dup? is undefined., or
    the text of an ABORT" of the block) is commented out: the error would
    end the INCLUDE there;
  * a BASIC line longer than a source line is wrapped in the comment;
  * a block the guide marks <!-- no-test --> is preceded by a warning: it
    waits for keys, never ends or needs hardware the emulator lacks.

A ```text block after a forth block, the output of its last line, follows
it as comments. 7-bit ASCII, LF line ends, lines of 80 bytes or fewer, last
byte LF and never a space before it (the INCLUDE rule in CLAUDE.md). The
chapters are the source: edit the .md, then run this script again. A file
is rewritten only when its content changes.

    python util/guide-forth.py            # write bas2f/f/*.f
    python util/guide-forth.py --check    # exit 1 if any .f is out of date
"""
import os
import re
import sys
import glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUIDE_DIR = os.path.join(ROOT, "doc", "basic-to-vforth")
OUT_DIR = os.path.join(ROOT, "bas2f", "f")

NO_TEST = "<!-- no-test -->"
CLAIM = re.compile(r"\\ => (.*)$")
ERROR = re.compile(r"\S\? \S")          # "WORD? message." as ERROR prints it
NUMBER = re.compile(r"^-?(\$[0-9A-F]+|%[01]+|[0-9]+\.?)$")
CORE_SRC = os.path.join(ROOT, "project", "vForth18_DOES", "source")
CORE_DEF = re.compile(r'^\s*\w+_Def\s+\w+\s*,\s*"(.*)"\s*,', re.M)
FAT = str.maketrans(':?/*|\\<>"', '_^%&$_{}~')    # MAP-FN in L3.asm

# words whose next token is the name of a new word
DEFINERS = {":", "CONSTANT", "2CONSTANT", "VARIABLE", "2VARIABLE", "VALUE",
            "CREATE", "CODE", "DEFER", "MARKER", "BUFFER:",
            "FCONSTANT", "FVARIABLE", "FVALUE"}
# words whose next token is not a word to look up
SKIP_NEXT = {"NEEDS", "CHAR", "[CHAR]", "FORGET", "POSTPONE", "[COMPILE]",
             "TO", "IS", "HELP", "SEE"}
# words that parse text up to a delimiter (locals included)
STRINGS = {'."': '"', 'S"': '"', 'C"': '"', 'H"': '"', 'ABORT"': '"',
           '.(': ")", "(": ")", "{": "}"}

# listings answered only in prose: the words that prose points to
PROSE = {
    "01-05": ["TRY"],
    "12-01": ["SHOW"],
    "13-02": ["SHAPES"],
    "13-04": ["E1"],
    "25-01": ["MC", "NN99"],
    "25-03": ["TIMES"],
}


class Block:
    def __init__(self, md, lineno, lines, no_test):
        self.md = md                    # chapter file
        self.lineno = lineno            # line of the opening fence
        self.lines = lines
        self.no_test = no_test
        self.output = None              # lines of a trailing ```text block
        self.defines, self.uses = scan(lines)
        self.aborts = [m.group(1) for ln in lines
                       for m in re.finditer(r'ABORT" ([^"]*)"', ln)]


def scan(lines):
    """Return the sets of names a block defines and uses."""
    defines, uses, colon = set(), set(), False
    for ln in lines:
        toks = ln.split()
        i = 0
        while i < len(toks):
            t = toks[i].upper()
            if t == "\\":
                break
            if t in STRINGS:
                j = i + 1
                while j < len(toks) and not toks[j].endswith(STRINGS[t]):
                    j += 1
                i = j + 1
                continue
            if t in (";", "C;"):
                colon = False
            elif t == ":" or (t in DEFINERS and not colon):
                if i + 1 < len(toks):
                    defines.add(toks[i + 1].upper())
                colon = colon or t in (":", "CODE")
                i += 2
                continue
            elif t in SKIP_NEXT:
                i += 2
                continue
            elif not NUMBER.match(t):
                uses.add(t)
            i += 1
    return defines, uses - defines


def known_words():
    """Names the core defines or NEEDS can load from inc/ and lib/."""
    names = set()
    for asm in glob.glob(os.path.join(CORE_SRC, "*.asm")):
        with open(asm, encoding="ascii", errors="replace") as f:
            names |= {n.upper() for n in CORE_DEF.findall(f.read())}
    files = set()
    for d in ("inc", "lib"):
        files |= {os.path.splitext(f)[0].upper()
                  for f in os.listdir(os.path.join(ROOT, d))}
    return names, files


KNOWN = None


def is_known(name):
    global KNOWN
    if KNOWN is None:
        KNOWN = known_words()
    return name in KNOWN[0] or name.translate(FAT) in KNOWN[1]


def parse(path, blocks):
    """Append the forth blocks of a chapter to `blocks`; return its listings.

    Each listing is (lines, [indices in `blocks` of its own forth blocks]).
    """
    md = os.path.basename(path)
    with open(path, encoding="utf-8") as f:
        lines = f.read().split("\n")
    listings = []
    section, pending, last, i = "", False, None, 0
    current = None                      # the listing forth blocks join
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("## "):
            section, current = ln, None
        elif ln.strip() == NO_TEST:
            pending = True
        elif ln.startswith("```"):
            tag = ln[3:].strip()
            j = i + 1
            while lines[j].strip() != "```":
                j += 1
            body = lines[i + 1:j]
            if tag == "":
                listings.append((body, []))
                current = listings[-1] if "Side by side" in section else None
                last = None
            elif tag == "forth":
                blocks.append(Block(md, i + 1, body, pending))
                last = blocks[-1]
                if current is not None:
                    current[1].append(len(blocks) - 1)
            elif tag == "text" and last is not None:
                last.output = body
            pending = False
            i = j
        elif ln.strip():
            last = None if not ln.startswith("<!--") else last
        i += 1
    return listings


def needed(blocks, own, extra, md):
    """Indices of the blocks in front of `own` that define what it uses.

    The last definition before `own` in the same chapter wins; an earlier
    chapter is searched only for a name neither the core nor NEEDS knows,
    since a chapter may redefine a standard word for its own example
    (THROW in Chapter 10).
    """
    defined_by = {}
    for k, b in enumerate(blocks):
        for name in b.defines:
            defined_by.setdefault(name, []).append(k)
    first = min(own) if own else max(k for k, b in enumerate(blocks)
                                     if b.md == md) + 1
    have = set().union(*(blocks[k].defines for k in own)) if own else set()
    want = set(extra)
    for k in own:
        want |= blocks[k].uses
    deps = set()
    while want:
        name = want.pop()
        if name in have:
            continue
        src = [k for k in defined_by.get(name, []) if k < first]
        same = [k for k in src if blocks[k].md == md]
        if same:
            k = same[-1]
        elif src and not is_known(name):
            k = src[-1]
        else:
            continue
        deps.add(k)
        have |= blocks[k].defines
        want |= blocks[k].uses
    return sorted(deps)


def render_block(b):
    out = ["", "\\ %s:%d" % (b.md, b.lineno)]
    if b.no_test:
        out.append("\\ no-test in the guide: it waits for keys, never ends or")
        out.append("\\ needs hardware the emulator lacks")
    for ln in b.lines:
        m = CLAIM.search(ln)
        if m and (ERROR.search(m.group(1))
                  or any(a and a in m.group(1) for a in b.aborts)):
            out.append("\\ an error in the guide, it would end the INCLUDE:")
            ln = "\\ " + ln
        out.append(ln)
    if b.output:
        out.append("\\ output of the last line:")
        out.extend(("\\ " + ln).rstrip() for ln in b.output)
    return out


def render(name, txt, md, listing, blocks, deps, own):
    out = ["\\ %s.f -- the Forth side of a NextBASIC listing" % name,
           "\\ BASIC: bas2f/txt/%s.txt" % txt,
           "\\ guide: doc/basic-to-vforth/%s" % md,
           "\\ written by util/guide-forth.py: edit the guide, not this file",
           "\\"]
    for ln in listing:
        # a BASIC line may be longer than a source line: wrap the comment
        while len(ln) > 76:
            cut = ln.rfind(" ", 0, 76)
            cut = cut if cut > 4 else 76
            out.append("\\   " + ln[:cut])
            ln = "    " + ln[cut:].lstrip()
        out.append(("\\   " + ln).rstrip())
    if deps:
        out.append("")
        out.append("\\ --- words defined earlier in the guide")
        for k in deps:
            out.extend(render_block(blocks[k]))
    if own:
        out.append("")
        out.append("\\ --- the translation")
        for k in own:
            out.extend(render_block(blocks[k]))
    while out and not out[-1].strip():
        out.pop()
    return "\n".join(ln.rstrip() for ln in out) + "\n"


def main():
    check = "--check" in sys.argv[1:]
    stale = problems = 0
    blocks, chapters = [], []
    for path in sorted(glob.glob(os.path.join(GUIDE_DIR, "[0-9][0-9]-*.md"))):
        chapters.append((os.path.basename(path), parse(path, blocks)))
    for md, listings in chapters:
        base = os.path.splitext(md)[0]
        for i, (listing, own) in enumerate(listings, 1):
            name = "%s-%02d" % (base[:2], i)
            txt = "%s-%02d" % (base, i)
            extra = PROSE.get(name, [])
            if not own and not extra:
                print("%s: no forth block and no entry in PROSE" % name)
                problems += 1
            if own:
                parts = [[k] for k in own]
            else:
                parts = [needed(blocks, [], extra, md)]
            for n, part in enumerate(parts):
                fname = name + ("" if n == 0 else chr(ord("a") + n))
                deps = needed(blocks, part, extra, md) if own else []
                s, p = write(fname, txt, md, listing, blocks, deps, part,
                             check)
                stale += s
                problems += p
    if check:
        sys.exit(1 if stale or problems else 0)
    sys.exit(1 if problems else 0)


def write(name, txt, md, listing, blocks, deps, own, check):
    """Write one .f; return (1 if it was out of date, problems found)."""
    stale = problems = 0
    text = render(name, txt, md, listing, blocks, deps, own)
    for n, ln in enumerate(text.split("\n"), 1):
        if len(ln) > 80:
            print("%s.f:%d: longer than 80 bytes" % (name, n))
            problems += 1
    bad = sorted({c for c in text
                  if c != "\n" and not " " <= c <= "~"})
    if bad:
        print("%s.f: characters outside 7-bit ASCII: %r" % (name, bad))
        problems += 1
    out = os.path.join(OUT_DIR, name + ".f")
    try:
        with open(out, encoding="ascii", newline="") as f:
            old = f.read()
    except (OSError, UnicodeDecodeError):
        old = None
    if old == text:
        return 0, problems
    stale += 1
    if check:
        print("%s.f is out of date" % name)
    elif not bad:
        os.makedirs(OUT_DIR, exist_ok=True)
        with open(out, "w", encoding="ascii", newline="\n") as f:
            f.write(text)
        print("%s.f written" % name)
    return stale, problems


if __name__ == "__main__":
    main()
