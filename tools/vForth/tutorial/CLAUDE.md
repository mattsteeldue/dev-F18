# tutorial/ -- Guided tutorials

Guided, self-contained tutorials introducing vForth features progressively.
This file supersedes `tutorial-conventions.md` and is the authoritative reference.


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
