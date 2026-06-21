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


## 3. File Structure

Each tutorial `.f` must follow this structure:

**a) Header block (backslash comments):**
   - Filename
   - One-paragraph narrative description
   - vForth-specific notes if any
   - **Starting FORTH cross-reference line** (tutorials 001-027 only): the Brodie
     chapter and the parallel vForth screen range, on the line immediately above
     `Reference:`. Format:
     ```
     \ Starting FORTH (Brodie): Ch.N  |  vForth screens NNN-NNN
     ```
     Use the concept map in `doc/tutorial-vs-screens.md` (chapter table) to fill it.
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

- **What the default state is** — so readers know what to expect on entry.
- **What happens if they forget to change it** — silent misparsing, wrong output, crashes.
- **Why this is dangerous** — hard to debug because no error is raised.

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
