# tutorial/ -- Guided tutorials

Guided, self-contained tutorials introducing vForth features progressively.
This file supersedes `tutorial-conventions.md` and is the authoritative reference.


## 0. Reference Documents

Two distinct documents are involved -- do not confuse them:

- **vForth manual** -- `doc/vForth1.8-core-en-<date>.odt` (the project's own manual).
  The `Reference: sec.N.NN` line in every tutorial header points to **this** document
  (e.g. sec.2.12.x = core words, sec.3.x / 7.x = hardware, sec.9 = communications).
  Its chapter numbering is being reorganised, so a stale `sec.7.x` may need updating to
  the new `sec.3.x` -- check against the current manual when revising a tutorial.

- **ZX Spectrum Next - Developer's Guide & Reference Manual (rev. 2)** --
  `C:\Zx\Next\zx-next-dev-guide-r2.pdf` (the hardware bible). This is the authoritative
  source for register/port behaviour. Cite it (with printed page numbers) when a tutorial
  touches the hardware directly -- see section 14 (AY $FFFD) for an example. When its
  prose/examples disagree with its register tables, the **register table wins** (the guide
  contains known example typos).


## 1. Language

- Interaction with the author: Italian.
- All source code, comments, and documentation: English only.
- Character encoding: 7-bit ASCII strictly.
  Allowed bytes: 0x20-0x7E, tab (0x09), LF (0x0A), CR (0x0D), 0x7F.
  No UTF-8, no BOM, no smart quotes, no em-dash (use -).
- Line width: maximum 80 columns.


## 2. File Naming

- Tutorial files: `NNN-slug.f` (three-digit zero-padded sequence number).
  Examples: `001-stack-basics.f`, `010-create-does.f`
- The prefix determines load order and reading sequence; renumbering is acceptable
  when inserting new topics.
- Stored in: `tutorial/`
- **Register every new tutorial in `lib/TUTORIAL.f`**: add its `H" tutorial/NNN-slug.f"`
  entry to `TUT-TABLE` and bump `TUT-MAX`, otherwise `NNN TUTORIAL` cannot load it.
  (Tutorial 054 shipped without this step and was unreachable until 2026-07-01.)


## 3. File Structure

Each tutorial `.f` must follow this structure:

**a) Header block (backslash comments):**
   - Filename
   - One-paragraph narrative description
   - vForth-specific notes if any
   - **Starting FORTH cross-reference line** (tutorials 001-029): the Brodie
     chapter and the parallel vForth screen range, on the line immediately above
     `Reference:`. Format:
     ```
     \ Starting FORTH (Brodie): Ch.N  |  vForth screens NNN-NNN
     ```
     The block-storage pair 028/029 maps to Brodie **Ch.3 "The Editor (and Staff)"**
     (disk/BLOCK/editor; screen 815 plus the Ch.10-completion screens 882-895).
     Use the concept map in `prompts/tutorial-vs-screens.md` (chapter table) to fill it.
     Multi-chapter tutorials list both (e.g. `Ch.2, Ch.5  |  ... 805-814, 821-825`).
     When a tutorial has no Brodie counterpart, state it explicitly instead of
     omitting the line:
       - `no Brodie counterpart (vForth extension)` -- vForth/Next-only topics
         (011 bit-ops, 024 floating, 026 catch/throw, 027 assembler; 013 case adds
         `(Brodie uses nested IF)`).
       - `no direct counterpart in screens 800-905` -- standard-Forth topics absent
         from the screen transcription (012 return stack, 025 memory).
     The screen corpus now covers Brodie Ch.1-11 (800-905): Ch.10 was completed to
     895 and Ch.11 "Extending the Compiler" added at 896-905, so the defining-word
     and compilation tutorials (010, 019, 020, and 021 partially) point at real
     screens. The hardware track (030-053) is outside Brodie's range: no such line.
   - Reference to PDF section(s): sec.N.NN
   - Load and unload instructions

**b) MARKER immediately after header:**
```forth
MARKER NEWTASK
```
The name `NEWTASK` is fixed across all tutorials. Rationale: the Spectrum keyboard is
cumbersome; a short, fixed name minimises mis-typing.

**c) CR before banner (for clean output when INCLUDEd):**
```forth
CR
.( --- Tutorial NNN: title loaded. ) CR
.(     Type NEWTASK to unload.   ) CR
```

**d) NEEDS lines** (if required) immediately after MARKER banner.
   NEEDS is always at interpreter level -- never inside a definition.

**e) Numbered sections with separator lines:**
```forth
\ =========================================================================
\ N. Section title
\ =========================================================================
```

**f) Interactive examples in comments using => notation:**
```forth
\   42 .    => 42
```

**g) Demonstration words** (short, named with a leading dot or descriptive name).

**h) Commented-out test block at end:**
```forth
\ NEEDS TESTING
\ T{  expr  ->  expected  }T
```

**Typical structure:**
```forth
\
\ 001-stack-basics.f
\ Introduction to the vForth stack and basic arithmetic.
\

MARKER NEWTASK

CR
.( --- Tutorial 001: stack basics loaded. ) CR
.(     Type NEWTASK to unload.           ) CR

\ =========================================================================
\ 1. Pushing values
\ =========================================================================

\ 3 4 +  leaves 7 on the stack
\   3 4 +    => ( 7 )

: .DEMO-ADD  ( a b -- )
    + . ;
```


## 4. Comment Style

- Narrative description: several lines in the file header.
- Section intro: free prose comments explaining the concept.
- Inline stack comments on non-obvious lines: `word  ( before -- after )`
- Step-by-step stack comments on complex definitions, one per line:
```forth
: SAME-STRING?    ( a1 n1 a2 n2 -- f )
    ROT           ( a1 a2 n2 n1 )
    OVER          ( a1 a2 n2 n1 n2 )
    - IF          ( a1 a2 n2 )
        2DROP     ( a1 )
        DROP      ( )
        0         ( ff )
    ELSE          ( a1 a2 n2 )
        (COMPARE) ( f )
        0=        ( f )
    THEN ;
```
- Line comments only on obscure lines, not on self-evident ones.
- Reference to PDF section in file header, not on individual words.


## 5. Stack Notation

- Standard: `( before -- after )` with TOS on the right.
- `pfa` is shown explicitly in DOES> definitions: `DOES>  ( index pfa -- addr )`
- double-cell items: `d` (signed), `ud` (unsigned), shown as two cells.
- flag: `f` (any non-zero = true), `ff` (false = 0), `tf` (true = -1 = $FFFF).


## 6. Numeric Literals

- Preferred: prefix characters in source: `$FF`  `%11111111`  `#255`
- Normal usage: global base switch for output only: `255 HEX . DECIMAL`
- Discouraged: global base switch during compilation or file loading.
- **Never use `HEX` or `DECIMAL` to switch base while a source file is being
  compiled/loaded.** Express each literal in the base you want with its prefix
  instead: `$` for hex (`$FF`), `%` for binary (`%11111111`). The `#` prefix forces
  decimal (`#255`); it is superfluous (decimal is the assumed default) but acceptable
  as a reinforcing, self-documenting marker when the surrounding code is hex-heavy.
- `NEEDS BINARY` / `NEEDS OCTAL` at interpreter level only, never inside a definition.
- Sign after prefix: `#-33` correct; `-#33` wrong.
- Double literals: any punctuation in a number makes it double (32-bit).
- **Never write `N LITERAL` to "compile a literal".** Inside a colon definition a bare
  number *already* auto-compiles as a literal, so `$E000 LITERAL` compiles `$E000` **and
  then** a second, spurious literal (`LITERAL` pops a non-existent compile-time value).
  For a constant, just write the bare number (`$E000`); `LITERAL` is only for a value
  computed at compile time inside brackets: `[ 2 3 + ] LITERAL`, `[ DECIMAL 87 ] LITERAL`
  (see `inc/MMU7@.f`, `inc/J.f`). This is a **silent** error -- it compiles without
  complaint and only corrupts the stack at run time. (Bug found and fixed in tutorial 041
  `PEEK-L2-ROW`, 2026-06-15.)


## 7. vForth-Specific Rules

- `,"` produces a counted-z-string: length byte + text + null byte ($00).
  The null enables direct use with NextZXOS C-style string API calls.
- `VARIABLE` initialises to 0, takes no initial value on the stack
  (standard since v1.52; old code passing a value before VARIABLE is wrong).
- `NEEDS` is interpreter-only; never call it inside a colon-definition.
- `INCLUDE` is interpreter-only; same constraint.
- `VALUE` requires `NEEDS VALUE`; `TO` requires `NEEDS TO` (separate inc/ files).
- The step-by-step stack comment style (rule 4 above) is preferred for definitions
  with more than two stack-manipulation operations.
- **Use `[']`, not `'`, to get a word's xt inside a definition.** `'` (tick) is *not*
  immediate in vForth (`: ' -find 0= 0 ?error drop ;`): it parses and looks up the next
  word at **run time**. Inside a colon definition `' FOO` therefore compiles a call to
  `'` *plus* an ordinary call to `FOO`; at run time `'` then parses whatever token follows
  in the input stream -- the wrong word, or an error (message 0) when nothing follows. To
  compile the execution token of a specific word as a literal, use the immediate `[']`:
  `: INSTALL  ['] FOO  HANDLER ! ;`. `[']` lives in `inc/['].f`, so add `NEEDS [']`.
  `'` is correct only in **interpret state** -- typed at the prompt, or as top-level code
  in a loaded source file. The same store can be right or wrong depending on context:
  `lib/MOUSE.f` ends with `' MOUSE-DELTA ISR-XT !` at interpret time (no brackets needed),
  whereas tutorial 049's `INSTALL-COUNTER` does the identical store *inside a definition*
  and so must use `[']`. Like the `LITERAL` trap above, the mistake is silent at compile
  time. (Bug found and fixed in tutorial 049 `INSTALL-COUNTER`/`REMOVE-COUNTER`,
  2026-06-15.)


## 8. CREATE...DOES> Conventions

- `DOES>` pushes PFA as the deepest new stack item.
- Caller arguments sit above PFA at DOES> entry.
- Array usage: index precedes the array name:
```forth
42  0 SCORES  !    \ not: 42 SCORES 0 !
0 SCORES  @ .
```
- Stack comment for DOES> shows pfa explicitly and rightmost:
  `DOES>  ( index pfa -- addr )`
- Never nest CREATE...DOES>.


## 9. Primitive vs Higher-Level Words

- Prefer core primitives over words requiring NEEDS when both are available and
  equally readable.
- `(COMPARE) ( a1 a2 n -- b )` is the core primitive; use it instead of
  `COMPARE ( a1 b1 a2 b2 -- n )` which requires NEEDS.
- Source of truth for core membership: `src/F18e.f` (not the PDF alone).
  When in doubt: grep for the word in F18e.f before writing NEEDS.


## 10. Self-Contained Requirement

Each tutorial must work in isolation. Use `NEEDS` for every dependency -- never assume
a word is already loaded. A reader should be able to `INCLUDE tutorial/NNN-topic.f`
from a clean vForth session and have it work.

Later tutorials may use `NEEDS` to load words introduced by earlier ones, but must not
use `INCLUDE tutorial/NNN-...f` -- they load vocabulary, not scripts. If a tutorial
concept is general enough to become a real `inc/` word, extract it following the standard
refactoring pattern.


## 11. Philosophy

- The art of stack manipulation goes hand in hand with the art of factoring: a word
  needing more than two or three shuffle operations should be split into smaller
  definitions, each taking the minimum number of parameters it actually needs.
  Readable Forth code is flat and narrow, not deep and twisted.
- `NEEDS` is a load-time tool, not a run-time tool.
- Changing BASE for output is fine; changing BASE during source loading or compilation
  is error-prone and should be avoided.
- Unlike `inc/` files (which have minimal comments), tutorials are primarily
  documentation. Explain the *why*, show the stack effects, describe expected output.
  The target reader is a programmer new to vForth but not necessarily new to programming.


## 12. Caveats: Silent Behavioral Changes

When a word's behavior depends on internal state (NMODE, BASE, etc.), explicitly warn
readers about the consequences of forgetting to set or reset that state:

- **What the default state is** -- so readers know what to expect on entry.
- **What happens if they forget to change it** -- silent misparsing, wrong output, crashes.
- **Why this is dangerous** -- hard to debug because no error is raised.

Example: forgetting `FLOATING` before entering floating-point numbers causes the parser
to interpret them as double integers (silently), producing incorrect results or crashes.
Forgetting `INTEGER` afterwards causes subsequent integer literals with a decimal point
to be misparsed as floating-point.

Include a clear warning in the narrative or as an inline comment so readers internalize
the trap before they encounter it in practice.


## 13. Display Modes in Graphic Tutorials

vForth's default text display is **LAYER12**: the Timex HiRes mode giving 64 columns of
text. The interactive prompt expects this mode with a blue background.

Tutorials 030, 031, and 032 demonstrate the **original Spectrum ULA**, called **Layer 0**
(256x192 pixels, 8 colors, 32x24 attribute grid), activated with `LAYER0`. Any tutorial
whose `DEMO` switches the graphic mode must restore the default text mode afterwards.

### Prefer the lightweight `inc/` LAYER words, not GRAPHICS

The `LAYER` words exist in **two** places, and `NEEDS` resolves to the right one
because it searches `inc/` before `lib/`:

- **`inc/layer0.f`, `inc/layer12.f`, ...** -- standalone, lightweight. Each just
  sets the hardware display mode via `IDE_MODE!` (plus `WIDECHAR`/`PAUSEOFF` for
  LAYER12). No graphic primitives are installed.
- **`lib/GRAPHICS.f`** -- once loaded, defines *all* `LAYERx` words **and** the full
  set of vectored graphic primitives (PLOT, POINT, DRAW-LINE, ...). This is heavy.

A tutorial that only needs to flip display mode (e.g. to show ULA attributes, cursor
positioning, or timing) must pull in the **standalone** words:
```forth
NEEDS LAYER0
NEEDS LAYER12
```
Do **not** write `NEEDS GRAPHICS` just to switch layers -- that drags in the entire
graphics library when no plotting is used. Reserve `NEEDS GRAPHICS` for tutorials that
actually draw (036 and later). (`inc/layers.f` loads every `LAYERx` at once but is
likewise unnecessary for a single-mode demo.)

### DEMO pattern: switch in, restore out

- Open the demo by selecting the graphic mode and clearing the screen:
```forth
: DEMO
    LAYER0 CLS
    ...
```
- Close the demo by returning to the default text mode with a blue background
  (`.PAPER` color 1 = blue):
```forth
    LAYER12 1 .PAPER
;
```

This applies to whatever graphic mode the tutorial selects: always return to
`LAYER12 1 .PAPER` so the reader is left at the normal 64-column blue-background prompt.


## 14. AY Sound: chip-select on port $FFFD (tutorial 034)

Authoritative source: dev guide section 3.10.4, "Turbo Sound Next Control $FFFD"
(register table, printed page 113). When bit 7 = 1 the port selects the active chip:

| Bit | Meaning                                            |
|-----|----------------------------------------------------|
| 7   | 1 (chip-select mode)                               |
| 6   | 1 = enable left audio                              |
| 5   | 1 = enable right audio                             |
| 4-2 | must be 1                                          |
| 1-0 | active chip: `11`=AY1, `10`=AY2, `01`=AY3, `00`=unused |

So the byte to write with both audio channels enabled is:

| Chip | bits 1-0 | byte  | binary       |
|------|----------|-------|--------------|
| AY1  | `11`     | `$FF` | `%11111111`  |
| AY2  | `10`     | `$FE` | `%11111110`  |
| AY3  | `01`     | `$FD` | `%11111101`  |

General rule: to select AY chip number `k` (k = 1,2,3) write `(-k) AND $FF` to `$FFFD`,
i.e. `$FF`/`$FE`/`$FD` (equivalently `$FF - (k-1)`). The negation `-k` is exactly the
trick `lib/AY.f AYSELECT` uses.

**The PDF uses two chip numberings.** The prose / Peripheral 4 Register $09 (printed
page 101) names the chips `AY0/AY1/AY2` (0-based), while the authoritative $FFFD table
(page 113) names the same three chips `AY1/AY2/AY3` (1-based). They map one-to-one:
AY0(prose)=AY1(table)=`$FF`, AY1(prose)=AY2(table)=`$FE`, AY2(prose)=AY3(table)=`$FD`.
**vForth follows the 1-based table** (`lib/AY.f`).

**Known PDF typo:** the example on printed page 112 writes `%11111101` and comments
"select AY1", but `%11111101` = `$FD` is the *third* chip in either naming (table AY3 /
prose AY2), not the first. Trust the register table, not the example.

**`AYSELECT` argument is 1-based:** `1 AYSELECT`=AY1, `2`=AY2, `3`=AY3. The arithmetic
only works for `k = 1,2,3`: `0 AYSELECT` writes nothing to the port (silent no-op that
leaves the previously selected chip). `AYSETUP` itself calls `1/2/3 AYSELECT`. Tutorial
code must use `1 AYSELECT` to select AY1 -- never `0 AYSELECT`. The same 1-based
convention holds for the separate `AYSELECT` in `lib/afxplay.f`, whose `1- CELLS` table
indexing bakes the 1-based assumption in.

### Mixer register 7: 0 = enabled (active low)

AY register 7 (the mixer) is **active low**: a `0` bit *enables* a source, a `1` bit
*disables* it. This is why `SHH` writes `$FF` (all ones) to silence everything. The bit
layout (dev guide page 114) is:

| Bit | 7 | 6 | 5       | 4       | 3       | 2      | 1      | 0      |
|-----|---|---|---------|---------|---------|--------|--------|--------|
|     | 0 | 0 | noise C | noise B | noise A | tone C | tone B | tone A |

So "enable tone A only" = `%00111110` (bit 0 = 0, all others 1); "enable noise A only"
= `%00110111` (bit 3 = 0, all others 1).

**Bug found and fixed in tutorial 034 `AY-NOISE` (2026-06-06):** the mixer was written
`%00101111`, which clears **bit 4 (noise B)** instead of bit 3 (noise A). It therefore
enabled noise on channel B while the volume was set only on channel A (reg 8) -- so no
sound was audible, despite the comment "enable ch A noise". Corrected to `%00110111`.
Lesson for authors: when targeting "channel A", double-check you are clearing the bit in
*column A* of the table above -- it is easy to be one bit position off, and because the
register is active-low the mistake is silent (wrong channel plays, or nothing does).


## 15. Known Issues -- Malfunctions Requiring Hardware Verification

Status as of 2026-07-05:

- **045-copper.f**: **RESOLVED** -- confirmed working on CSpect (2026-07-10),
  all keys included. The old border/palette demo sections
  (`COPPER-RAINBOW`/`COPPER-SPLIT`/`COPPER-OFF`) were speculative and never
  confirmed working. Replaced with `SPLIT-SCROLL-DEMO`, a three-band split
  vertical-scroll effect over a loaded Layer 2 bitmap (NextReg `$17` Layer 2
  Y Offset written at three different `COP-WAIT` scanlines), ported from a
  working forum contribution (`forum/copper-bmp2.f`) and cleaned up: BMP
  loading now goes through `BMP-LOAD"` (the tutorial 046 loader) instead of
  the forum source's hand-rolled, order-reversed page loop; German-derived
  word/variable names (`gehe`/`schiebe`/`lire`/`starte`/`los`, ...)
  translated to English (`BUILD-COPPER-LIST`/`SCROLLn`/`STEPn`/
  `HANDLE-KEY`/`SPLIT-SCROLL-DEMO`); and the ISR was hooked up via `ISR-XT`
  instead of the forum source's `ISR-W`, which is not a real word in
  `lib/INTERRUPTS.f` and left the handler never actually installed.
  `SPLIT-SCROLL-DEMO` also saves/restores NextReg `$17` (Layer 2 Y Offset)
  around the effect, so it leaves that hardware register exactly as it
  found it -- the same in/out discipline as the `LAYER2`/`LAYER12` switch.
  The author confirmed on CSpect that `a` (start), `d` (pause) and `e`/`q`
  (reverse direction) all work correctly.
- **046-bmp-load.f**: **RESOLVED** -- works on CSpect (2026-07-05). The "malfunction"
  was a wrong file path: names passed to `BMP-LOAD` / `OPEN<` are **relative to the
  directory vForth was started from** (`tools/vForth` on the SD card). A PATH GOTCHA
  note was added to the tutorial's section 1, and the dead sample path
  `demos/demo.bmp` was fixed to `demo/BMP/jaws.bmp`. A second glitch: every wait
  was written `WAIT-KEY DROP`, but `WAIT-KEY ( -- )` leaves nothing on the stack
  (it is not `KEY`), so each `DROP` underflowed -- "Stack is empty" on returning
  to the prompt after `SLIDE-SHOW`. All five `DROP`s removed.
  **2026-07-10**: section 6 replaced with the double-buffered slide show ported
  from `demo/BMP-DEMO.f` (now removed -- content merged here); the fourteen
  `.bmp` assets moved from `demo/BMP/` to `tutorial/bmp/`, and every path in the
  tutorial updated accordingly. (`REG!` needs no `NEEDS` -- it is a core word,
  compiled into `forth18e.bin`; see `src/F18e.f` line 5240 and `main.lst`. An
  earlier revision of this note wrongly added `NEEDS REG!`, since removed.)
  Confirmed working on CSpect (2026-07-10), including the new slide show.
- **050-afxframe.f**: compile failure diagnosed 2026-07-05: `AFX-START`/`AFX-STOP`
  call `AYSETUP` (defined in `lib/AY.f`) but the tutorial never loaded it -- and
  `lib/AFXFRAME.f` has its own `NEEDS AY` commented out. `NEEDS AY` added to the
  tutorial header; **awaiting CSpect verification**.
- **056-layer2-palette.f (new, 2026-07-10)**: first tutorial to cover Next
  palette registers $40/$41/$43/$44 and Global Transparency $14, scoped to
  Layer 2 only (ULA/Sprites/Tilemap palettes share the mechanism but are out
  of scope). Written from `doc/zx-next-dev-guide-r3.txt` sec.3.4/3.6.4 (no
  vForth manual section exists yet for palettes). Two gotchas worth keeping
  in mind if this area is touched again: (1) auto-increment on `$40` only
  advances after a *write* to `$41`/`$44`, never after a read, and the index
  must be reset to 0 explicitly before streaming a whole palette -- relying
  on whatever `$40` happened to hold silently wrote to the wrong indexes in
  an early draft; (2) `$43` packs edit-target, active-display-bank and
  ULANext-enable in one byte, so every write in the tutorial sets the whole
  byte rather than trying to flip a single bit. Demos overwrite the Layer 2
  palette banks and restore identity colors afterwards (`RESTORE-IDENTITY`)
  rather than relying on `PAL-RESET` alone, which only resets the $43
  control byte, not the palette RAM contents. **Awaiting CSpect
  verification** -- never run outside this session.

Flag: 045 confirmed on CSpect (2026-07-10); 046 (including its new slide
show) confirmed on CSpect (2026-07-10); 050 until its fix is confirmed on
CSpect; 056 until confirmed on CSpect.


## 16. Hardware Sprites: slot vs pattern, palette offset (tutorial 053)

Working reference: Screens 399-413 in `!Blocks-64.bin` (Derek Bolli's Sprite Lib
port); test sprite file `tutorial/DKSprite.spr` (64 patterns; skin pixels use
colour indexes `$F7`/`$FB` = pink with the default identity palette, `$E3` is the
transparency index). Both bugs below were found by diffing tutorial 053 against
those screens and confirmed fixed on CSpect (2026-07-05).

Sprite attribute bytes (written to port `$57` after selecting a slot on `$303B`):

| Byte | Content                                                              |
|------|----------------------------------------------------------------------|
| 0    | X low 8 bits                                                         |
| 1    | Y low 8 bits                                                         |
| 2    | palette offset (7:4), X mirror (3), Y mirror (2), rotate (1), X8 (0) |
| 3    | visible (7), attr-4 enable (6), **pattern number (5:0)**             |

### Slot vs pattern -- never conflate them

Attribute 3 bits 5:0 are the **PATTERN** the sprite displays, *not* the sprite
slot. The slot (which of the 64 hardware sprites is being programmed) is chosen
only by the write to port `$303B`. Frame animation rewrites **the same slot**
with alternating pattern numbers (`SPRITE 0 SPRITE-UPDATE`, Screens 406/411).

**Bug found and fixed in tutorial 053 (2026-07-05):** `SPRITE-UPDATE` used the
`_spriteid` field both for the `$303B` slot select and for attribute 3. The walk
animation (`I 1 AND`) then alternated the *slot* too: it lit hardware sprites 0
and 1 on alternate steps, both left visible -- a pair of half-overlapped sprites
walking together instead of one animated character (and the final `0 SPRITE-HIDE`
left sprite 1 on screen). Fix: `SPRITE-UPDATE ( a n -- )` takes the slot as a
separate argument, as the screens' version always did.

### Palette offset: uninitialised struct = shifted hues

Attribute 2 bits 7:4 are a **palette offset** the hardware adds to the high
nibble of *every pixel's* colour index. A sprite struct allocated with
`CREATE ... ALLOT` and never `ERASE`d leaves heap garbage in the fields the demo
does not store (`_pattern`, `_rotmir`, `_anchor`); a non-zero `_pattern` shifts
every colour (pink `$F7` -> e.g. offset 4 -> `$37` = pale blue), and a dirty
`_rotmir` can silently mirror/rotate the sprite. The symptom "all hues shifted /
pinks turned pale blue" means **palette offset**, not a corrupted palette.
Rule: always `ERASE` a struct right after `ALLOT` unless every field is stored.

### Palette notes

- The sprite palette defaults to the identity mapping (colour i = i, RRRGGGBB);
  `.spr` files drawn for it (like DKSprite.spr) need no palette programming.
  NextReg `$40/$41/$43` are shared state though: tutorial 053's
  `SPRITE-PALETTE-INIT` rewrites the identity defensively. Careful with `$43`:
  bits 3:1 select the displayed palette per layer and bit 0 enables ULANext;
  `%00100000` restores the power-on defaults LAYER12 expects.
- Screen 409's palette write (`18 40 REG!` + `E3 41 REG!`) is Derek Bolli's ULA
  "paper bright 0" background tweak (see `forum/next-sprite-test.f`) -- it has
  nothing to do with sprite colours.


## 17. Dot-command relocation discipline: three correct forms, and how a
    missing one hides (demo/parser.dot.f)

Analysis performed 2026-07-18 while writing tutorial 057 section 11's gotcha,
then used to fix the demo itself (comments now in the file point back here).
Every CALL/JP target embedded inside a dot command's own code must be
translated from "wherever it sits in the live dictionary right now" to
"where it will actually run at $2000" (tutorial 057 section 3). Auditing
`demo/parser.dot.f` turned up **three different, equally correct mechanisms**
for doing that translation, plus **two call sites where none of them had
been used** -- a real, silent bug.

**The three correct mechanisms**, all present in the same file:

1. **`rel-AA,` / `rel-NN,` shorthand** -- applies `DOT-RELATIVE` and the
   matching commaer in one step. Used by `parse`'s call to `parse-string`
   and by `help`'s `ldx hl| ... rel-NN,` load of its message address.
2. **Manual `dot-relative ... AA,`** -- the identical translation, spelled
   out in two words instead of the shorthand. Used by `main`'s conditional
   jump to `help`. Functionally identical to (1), just a different style.
3. **Direct post-hoc patch** -- `entry-point`'s placeholder `jp 0 AA,` is
   fixed up after the fact by poking the translated address straight into
   dictionary memory (`' main dot-relative org @ 1+ !`), bypassing the
   assembler's `AA,` emission entirely.

**The bug this hid (found and fixed 2026-07-18):** two CALLs used plain
`AA,` with none of the three mechanisms above -- `main`'s
`call ' parse AA,` and `help`'s `call ' print AA,`. Plain `AA,` embeds the
address the target word has *right now, in the live dictionary*. That
address is meaningless once vForth is gone and the saved file is running
standalone at `$2000` (tutorial 057 section 1): **both** of the file's two
runtime branches (with-arguments -> `parse`, no-arguments -> `help` ->
`print`) would crash once genuinely relocated, even though every CODE
definition compiled cleanly and every interactive test passed.

**Why interactive testing never caught it:** the file's own `tester` word
(tutorial 057 section 6's TESTER pattern) calls `main` in place, before any
relocation has happened -- at that moment the "wrong" addresses embedded by
plain `AA,` still happen to equal the real ones, so `TESTER` reports
success. The failure exists only in the copy written to `C:/DOT/`, running
at `$2000`, which -- per tutorial 057 section 10 -- can only be verified on
CSpect or real hardware, never from inside the vForth session that built
it. General lesson: a missing `REL-AA,`/`REL-NN,` is invisible at every
stage of in-session testing and manifests only after the file leaves
vForth.

**Rule of thumb when auditing a dot command for this class of bug:** grep
every `AA,`/`NN,` between the `VARIABLE ORG` capture and the `SAVE-BYTES`
call; each one must be either operating on a value that is already
position-independent (rare) or be one of the three mechanisms above --
never plain. `demo/parser.dot.f` now carries an inline comment at every
relocation point naming which of the three it uses, plus one at `tester`'s
`call ' main AA,` explaining why plain `AA,` is *correct* there (it runs
in place, never relocated).

**Audit of the other three `demo/*.dot.f` files (2026-07-19):** applying the
same grep found no bug elsewhere.

- `demo/echo.dot.f` has zero `AA,`/`NN,` in the whole file -- its single
  `CODE echo` never embeds a CALL/JP or a stored address, only a PC-relative
  `Back,` loop and immediate byte constants, so there is nothing to
  relocate. Now says so in an inline comment.
- `demo/savebank.dot.f` was already fully correct: every CALL/JP to another
  word and every reference to its `v-*` variables (which live inside the
  relocated `[org, Here)` span, so they need translating too) already used
  `rel-AA,`/`rel-NN,`. The only plain `AA,` occurrences are the same two
  legitimate exceptions as `parser.dot.f` -- `entry-point`'s placeholder
  (direct post-hoc patch) and `tester`'s in-place call to `main`. Inline
  comments matching `parser.dot.f`'s style were added purely for
  documentation consistency; no logic changed.
