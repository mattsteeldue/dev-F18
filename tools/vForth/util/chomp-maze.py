#!/usr/bin/env python3
"""chomp-maze.py -- author/inspect the chomp-chomp mazes kept on Screen.

The mazes of demo/chomp-chomp.f are written with the game's own UDG
alphabet (A-N and W wall strokes, O power pill, '.' dot, '-' ghost-house
door, '/' and '\\' tunnel mouths).  A layout is unreadable as text:
the only way to tell a well-formed junction from a broken one is to look
at the 8x8 bitmaps.  This script does that headlessly -- it reads the UDG
table straight out of demo/chomp-chomp.f, so what it draws is always the
current glyph set.

    derive   resolve a layout draft: every '#' (an interior wall cell)
             becomes the wall glyph its four neighbours call for, so a
             new maze is authored as solid blocks instead of stroke
             letters -- see WALL GLYPHS below
    render   maze as ASCII art (one '#' per lit pixel) + the checks below
    check    the structural checks only (dots, pills, spawn cells,
             tunnel, connectivity, perimeter) -- the same properties the
             in-game MAZE-CHECK verifies, plus the dot count
    read     dump maze n from !Blocks-64.bin as 21 lines of 21 chars
    write    store a 21x21 layout file into maze n's Screens

The door and the two tunnel mouths are plain ROM-font characters, not
UDGs, so render leaves them blank -- what it draws is the wall, which is
the part a rule can get wrong.

Maze 0 is the copy compiled into demo/chomp-chomp.f (maze-base); mazes
1..N live on Screen MAZE-SCR0+2*(n-1) and +1, four BLOCKs each.

WALL GLYPHS.  A wall cell draws a stroke along each of its edges that
faces open floor, and the 15 letters are exactly the 15 non-empty
subsets of {N,S,W,E}:

    A N     B S     C NS    M W     J E     N WE
    E NW    D NE    I SW    H SE
    F NSW   G NSE   K NWE   L SWE   W NSWE

That is the whole alphabet -- W (a 1x1 island, closed on all four sides)
is the one this game did not have until the second batch of mazes
needed it.  The rule is exact for interior islands (it reproduces every
one of maze-base's, cell for cell); the outer silhouette is hand-drawn
art that no rule predicts, so derive leaves any glyph already spelled
out alone and refuses to guess for a '#' that touches the outside.
"""

import re
import sys
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC = os.path.join(ROOT, 'demo', 'chomp-chomp.f')
BLOCKS = os.path.join(ROOT, '!Blocks-64.bin')

MAZE_SCR0 = 740
MAZE_W = 21
MAZE_H = 21

WALK = set(' .O-/\\')          # everything ?pac-trail / ?ghost-trail accept
# hard-coded spawn geometry (see pacman-init / ghost-init / ghost-eaten);
# rows and columns here are 0-based into the 21x21 grid
PAC_START = (13, 11)
GHOST_HOME = [(11, 9), (11, 10), (11, 11)]
TED_START = (10, 10)
METADATA_ROW = '(reserved for level metadata)'


def udg_table():
    """{letter: [8 bytes]} read out of the UDG_1 block of chomp-chomp.f.

    Read positionally, exactly the way the print routine does: the table
    is one run of C, bytes and the glyph for code n is the eight bytes at
    (n-144)*8, so the k-th group of eight is the k-th letter from A.  Do
    not go by the comments -- only the older entries carry the hex header
    line that names their letter."""
    src = open(SRC).read()
    region = src[src.index('create UDG_1'):src.index('UDG_1 5C7B')]
    bits = re.findall(r'%([01]{8})\s+C,', region)
    if len(bits) % 8:
        sys.exit('UDG_1 holds %d bytes, not a whole number of glyphs' % len(bits))
    return {chr(ord('A') + i): bits[i * 8:i * 8 + 8]
            for i in range(len(bits) // 8)}


def compiled_maze():
    """The 21 rows of maze-base, as they end up in maze-run."""
    src = open(SRC).read()
    region = src[src.index('create maze-base'):src.index(': maze-copy')]
    rows = []
    for line in region.split('\n'):
        m = re.match(r'^,"(.*)"\s*$', line.strip())
        if m:
            # ," drops the single alignment space in front of the text and
            # keeps the one behind it, so the compiled row is the next 21
            # characters (see raw-row! in demo/chomp-chomp.f)
            rows.append(m.group(1)[1:1 + MAZE_W])
    return rows


def maze_blk0(n):
    return (n - 1) * 4 + MAZE_SCR0 * 2


def read_maze(n):
    if n == 0:
        return compiled_maze()
    data = open(BLOCKS, 'rb').read()
    rows = []
    for r in range(MAZE_H):
        blk = maze_blk0(n) + r // 8
        off = (blk - 1) * 512 + (r % 8) * 64
        rows.append(data[off:off + MAZE_W].decode('latin1'))
    return rows


def write_maze(n, rows):
    if n == 0:
        sys.exit('maze 0 is compiled into chomp-chomp.f, not on Screen')
    data = bytearray(open(BLOCKS, 'rb').read())
    size = len(data)
    for r in range(MAZE_H):
        blk = maze_blk0(n) + r // 8
        off = (blk - 1) * 512 + (r % 8) * 64
        data[off:off + 64] = rows[r].ljust(64).encode('ascii')
    # Rows 21..31 of the two Screens are the level's metadata area, unused
    # so far.  Label them rather than leaving them as they were: a raw
    # block starts out full of NULs, and a NUL is the one character that
    # stops LOAD dead without a word of explanation, should anyone ever
    # point LOAD at these Screens.
    for r in range(MAZE_H, 32):
        blk = maze_blk0(n) + r // 8
        off = (blk - 1) * 512 + (r % 8) * 64
        data[off:off + 64] = METADATA_ROW.ljust(64).encode('ascii')
    assert len(data) == size, 'block file size must never change'
    open(BLOCKS, 'wb').write(data)


# stroke set -> glyph, and the four neighbour offsets
GLYPH = {'': ' ',
         'N': 'A', 'S': 'B', 'NS': 'C', 'W': 'M', 'E': 'J', 'WE': 'N',
         'NW': 'E', 'NE': 'D', 'SW': 'I', 'SE': 'H',
         'NSW': 'F', 'NSE': 'G', 'NWE': 'K', 'SWE': 'L', 'NSWE': 'W'}
DIRS = {'N': (-1, 0), 'S': (1, 0), 'W': (0, -1), 'E': (0, 1)}


def derive(rows):
    """Replace every '#' with the wall glyph its neighbourhood calls for.

    Floor is what the game can walk on; a blank the flood-fill never
    reaches is not floor but the hollow inside of a block (or the filler
    outside the maze silhouette), which is why this has to flood-fill
    rather than just look at the characters."""
    floor = set()
    stack = [PAC_START]
    while stack:
        r, c = stack.pop()
        if (r, c) in floor or not (0 <= r < MAZE_H and 0 <= c < MAZE_W):
            continue
        if rows[r][c] not in WALK:
            continue
        floor.add((r, c))
        stack += [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]

    # the filler outside the maze's silhouette: unreachable blanks that
    # touch the edge of the grid
    outside = set()
    stack = [(r, c) for r in range(MAZE_H) for c in range(MAZE_W)
             if rows[r][c] == ' ' and (r, c) not in floor
             and (r in (0, MAZE_H - 1) or c in (0, MAZE_W - 1))]
    while stack:
        r, c = stack.pop()
        if (r, c) in outside or not (0 <= r < MAZE_H and 0 <= c < MAZE_W):
            continue
        if rows[r][c] != ' ' or (r, c) in floor:
            continue
        outside.add((r, c))
        stack += [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]

    def is_outside(r, c):
        return not (0 <= r < MAZE_H and 0 <= c < MAZE_W) or (r, c) in outside

    out, errs = [], []
    for r in range(MAZE_H):
        line = ''
        for c, ch in enumerate(rows[r]):
            if ch != '#':
                line += ch
                continue
            if any(is_outside(r + dr, c + dc) for dr, dc in DIRS.values()):
                errs.append('row %d col %d: a wall on the maze silhouette has '
                            'no derivable glyph, spell it out' % (r + 1, c + 1))
                line += '#'
                continue
            # a ghost-house door is walkable but must not be boxed in:
            # the house wall stops at it, which is what makes it read as
            # a gap (maze-base draws E/D/I/H, never K/L, beside a '-')
            strokes = ''.join(d for d in 'NSWE'
                              if (r + DIRS[d][0], c + DIRS[d][1]) in floor
                              and rows[r + DIRS[d][0]][c + DIRS[d][1]] != '-')
            line += GLYPH[strokes]
        out.append(line)
    return out, errs


def render(rows, table):
    out = []
    for row in rows:
        pix = [''] * 8
        for ch in row:
            glyph = table.get(ch.upper() if ch != '.' else 'V')
            if ch == ' ' or glyph is None:
                glyph = ['00000000'] * 8
            for i in range(8):
                pix[i] += glyph[i]
        out.extend(pix)
    return '\n'.join(l.replace('0', ' ').replace('1', '#') for l in out)


def check(rows):
    errs = []
    for r, row in enumerate(rows):
        if len(row) != MAZE_W:
            errs.append('row %d is %d chars, expected %d' % (r + 1, len(row), MAZE_W))
        for c, ch in enumerate(row):
            if ch == '\0':
                errs.append('NUL at row %d col %d' % (r + 1, c + 1))

    dots = sum(row.count('.') for row in rows)
    pills = sum(row.count('O') for row in rows)
    if pills != 4:
        errs.append('pill count %d, expected 4 (pill-n)' % pills)
    if dots == 0:
        errs.append('no dots: the level could never be completed')

    if not any('-' in row for row in rows):
        errs.append("no ghost-house door ('-')")

    srow = [r for r, row in enumerate(rows) if '/' in row]
    brow = [r for r, row in enumerate(rows) if '\\' in row]
    if len(srow) != 1 or len(brow) != 1 or srow != brow:
        errs.append("tunnel: '/' and '\\' must appear once, on the same row")
    else:
        if rows[srow[0]][0] != '/':
            errs.append("tunnel '/' must sit in column 1")
        if rows[brow[0]][MAZE_W - 1] != '\\':
            errs.append("tunnel '\\' must sit in column %d" % MAZE_W)

    # the spawn cells are hard-coded in the game, so every maze must
    # leave them exactly as maze-base does: blank where a sprite stores
    # a blank under itself, door under Ted
    for (r, c), what in ([(PAC_START, 'Pac-Man start')] +
                         [(p, 'ghost home') for p in GHOST_HOME]):
        if rows[r][c] != ' ':
            errs.append('%s at row %d col %d must be blank, found %r'
                        % (what, r + 1, c + 1, rows[r][c]))
    if rows[TED_START[0]][TED_START[1]] != '-':
        errs.append("Ted's start at row %d col %d must be a door '-'"
                    % (TED_START[0] + 1, TED_START[1] + 1))

    # connectivity: flood-fill from Pac-Man's start, exactly as
    # check-connectivity does in the game
    seen = set()
    stack = [PAC_START]
    while stack:
        r, c = stack.pop()
        if (r, c) in seen:
            continue
        if not (0 <= r < MAZE_H and 0 <= c < MAZE_W):
            continue
        if rows[r][c] not in WALK:
            continue
        seen.add((r, c))
        stack += [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]

    for r, row in enumerate(rows):
        for c, ch in enumerate(row):
            if ch in '.O-/\\' and (r, c) not in seen:
                errs.append('unreachable %r at row %d col %d' % (ch, r + 1, c + 1))

    tunnel_row = srow[0] if srow and srow == brow else -1
    for r, c in seen:
        if r in (0, MAZE_H - 1):
            errs.append('reachable cell on top/bottom border, row %d col %d'
                        % (r + 1, c + 1))
        if c in (0, MAZE_W - 1) and r != tunnel_row:
            errs.append('reachable cell on left/right border, row %d col %d'
                        % (r + 1, c + 1))

    return dots, pills, len(seen), errs


def read_layout(path):
    rows = open(path).read().split('\n')[:MAZE_H]
    rows = [r.rstrip('\n').ljust(MAZE_W)[:MAZE_W] for r in rows]
    while len(rows) < MAZE_H:
        rows.append(' ' * MAZE_W)
    return rows


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    cmd, arg = sys.argv[1], sys.argv[2]
    if cmd == 'write' and len(sys.argv) < 4:
        sys.exit('usage: chomp-maze.py write <maze-number> <layout-file>')
    if cmd == 'derive':
        rows, errs = derive(read_layout(arg))
        print('\n'.join(rows))
        if errs:
            print('\n'.join('  ! ' + e for e in errs), file=sys.stderr)
            sys.exit(1)
        return
    if cmd == 'write':
        rows, errs = derive(read_layout(sys.argv[3]))
        if errs:
            print('\n'.join('  ! ' + e for e in errs))
            sys.exit('refusing to write a maze with unresolved wall cells')
        dots, pills, reached, errs = check(rows)
        if errs:
            print('\n'.join(errs))
            sys.exit('refusing to write a maze that does not check out')
        write_maze(int(arg), rows)
        print('maze %s written: %d dots, %d pills, %d cells reachable'
              % (arg, dots, pills, reached))
        return

    rows = read_maze(int(arg))
    if cmd == 'read':
        print('\n'.join(rows))
        return
    if cmd == 'render':
        print(render(rows, udg_table()))
    dots, pills, reached, errs = check(rows)
    print('\nmaze %s: %d dots, %d pills, %d cells reachable' % (arg, dots, pills, reached))
    if errs:
        print('\n'.join('  ! ' + e for e in errs))
        sys.exit(1)
    print('  all checks pass')


if __name__ == '__main__':
    main()
