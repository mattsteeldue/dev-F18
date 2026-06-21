\
\ vForth Tutorial / Demo / Screen-Corpus -- Three-Axis Gap Analysis
\ Snapshot: dev-F18/main, June 2026. Subject to drift after Claude Code sessions.
\ All code/doc in English per project convention.

# vForth Teaching Material -- Gap Analysis

This report inventories three overlapping bodies of teaching material and maps
the gaps between them along three axes:

- **Axis 1 -- Language/feature coverage**: what vForth capability is taught where.
- **Axis 2 -- Pedagogical layering**: how the three corpora relate as a learning path.
- **Axis 3 -- Organisation / promotion**: what to move, promote, or retire.

Three corpora are in play, and the key realisation of this pass is that they are
**not independent** -- they are three generations of the same teaching effort:

| Corpus | Location | Form | Role |
|--------|----------|------|------|
| **Tutorials** | `tutorial/NNN-*.f` (001-053) | Self-contained `.f` source, INCLUDE-able | Modern, structured, authoritative teaching |
| **Brodie screens** | `!Blocks-64.bin` Scr# 800-881 | BLOCK screens, LOAD-able | Transcription/adaptation of *Starting FORTH* (Brodie) Ch.1-10; parallel reference track |
| **Example screens** | `!Blocks-64.bin` (scattered) | BLOCK screens | Working code: graphics, sound, asm, system, games |

The tutorials and the Brodie screens are **parallel but independent** tracks, not
one a rewrite of the other. They teach the same Forth concepts with **different
definitions** (`SHOW-SUM`/`CLAMP`/`SAFE-DIV` vs Brodie's `STAR`/`EGGSIZE`/`R%`),
so the overlap is **conceptual, not lexical** -- at the level of definition names
it is essentially nil. The screens are therefore not a deprecated old version but
a **second, cross-referenceable reference track**: the same concept rendered twice
in two idioms. The authoritative concept-to-concept mapping lives in the wiki page
"Tutorials vs. Starting FORTH Screens" and, at definition granularity (~58 rows
with a match-strength column), in `doc/tutorial-vs-screens.md`. This report defers
to those for Axis-2 detail. The `demo/` `.f` files are a fourth, separate body:
large standalone programs.

---

## Axis 1 -- Language / feature coverage

### Tutorial series 001-053 (already solid)

- **Core language (001-027)**: stack, output, bases, defining words, control
  flow, loops, memory, strings, CREATE/DOES>, bit ops, return stack, CASE,
  pictured output, double, input, DEFER/IS, vocabularies, compilation, EVALUATE,
  introspection, structures, floating point, advanced memory, CATCH/THROW,
  assembler. This block is **substantially complete** for a standard Forth.
- **Next hardware (030-053)**: ULA/Layer0, screen, timing, beeper, AY, keyboard,
  ULA graphics, Layer2, sprites (x2), Next registers, MMU, file I/O, filesystem,
  mouse, copper, BMP, UART, RPi0, interrupts, AFXframe, keyboard matrix, modular
  graphics.

All 53 are dense (136-275 lines); none are stubs.

### Coverage gaps (capability present in the system, absent from tutorials)

1. **BLOCK / native Forth storage.** No tutorial on BLOCK, LIST, LOAD, THRU,
   UPDATE, FLUSH, buffer management -- yet this is the substrate the entire screen
   corpus runs on. A canonical teaching example already exists: **Scr# 880-881
   (Buzzphrases Generator, Brodie Ch.10)**, which reads a word table from
   Scr# 881 via `881 (LINE)` -- a clean use of BLOCK *as data*, not as code.
   Strong candidate for a new tutorial. (EDIT/LED are *not* good tutorial
   subjects -- agreed; the BLOCK *mechanism* is.)
2. **Layer 3 / Tilemap.** Covered only by `demo/Layer3-demo1/2/3` (sophisticated:
   40/80 col, 1-bit vs 4-bit tile defs, base address overlapping the display
   file). No tutorial. Also present as screen studies (Scr# 340, 420-436
   "TILEMAP study").
3. **`.dot` command creation.** The pattern for producing standalone NextZXOS
   `.command` executables (assembler + save-bytes + `$2000`-relative addressing)
   exists as `demo/echo|helloworld|parser|savebank.dot.f` and screens (286, 357,
   581, 940-941). No tutorial. High value: it is the bridge from "I write Forth"
   to "I ship a system command".
4. **Fixed-point (Q8.8 / 12.4).** Screens 590-595 ("Product routine for 12:4
   fixed point") exist; the Q8.8 work is not yet a tutorial. The `*/` 32-bit
   intermediate trick and `SPLIT` belong here.
5. **`ZAP` / standalone executable workflow.** Chomp-chomp documents `ZAP` as the
   simplest way to produce a standalone game; the workflow is never given tutorial
   form (related: Scr# 670 "Create standalone executable").

---

## Axis 2 -- Cross-reference structure (parallel tracks)

The screen series 800-881 is a vForth transcription/adaptation of *Starting FORTH*
(Brodie) Ch.1-10, keeping Brodie's original names. It runs **parallel** to the
tutorials, not under them: same concepts, independent definitions. It is best used
as a **cross-reference track** -- a reader can see a concept rendered twice, once
in vForth-idiom tutorial form and once in Brodie-idiom screen form.

Concept correspondence (topics present in BOTH tracks), per the wiki:

| Brodie ch. / Scr# | tutorial counterpart | shared concept |
|-------------------|----------------------|----------------|
| Ch.1 800-804 | 003, 005 | `:`, `." "`, `EMIT`, `CR`, `SPACES` |
| Ch.2 805-814 | 001, 002 | postfix arith, `DUP/SWAP/ROT/OVER`, `/MOD`, `.S` |
| Ch.4 816-820 | 006 | `IF/ELSE/THEN`, `?DUP`, `WITHIN` |
| Ch.5 821-825 | 002, 015 | `*/`, `MIN/MAX/ABS`, percentages, conversions |
| Ch.6 826-837 | 007 | `DO/LOOP`, `+LOOP`, `?DO`, `I/J`, `LEAVE`, `BEGIN/UNTIL` |
| Ch.7 838-849 | 014, 004 | `<# # #S #> HOLD SIGN`, `.R/U.R`, `BASE`, `HEX/DECIMAL` |
| Ch.8 850-867 | 005, 008, 010, 023 | `VARIABLE/CONSTANT`, `!/@/+!`, `CREATE/ALLOT/,`, arrays |
| Ch.8 (double) | 015 | `2VARIABLE/2CONSTANT`, `2@/2!`, `D./D+/M+` |
| Ch.9 868-876 | 017, 022 | `'`/`[']`/`EXECUTE`, vectored exec, `SEE` |
| Ch.10 877-881 | 009, 016 | `TYPE`, `-TRAILING`, strings, I/O |

**Status (2026-06-20): per-tutorial cross-reference line added.** Each tutorial
001-027 now carries a `\ Starting FORTH (Brodie): Ch.N  |  vForth screens NNN-NNN`
line in its header (immediately above `Reference:`), so the concept-to-screen
mapping above is visible at the point of use, not only in this report and
`doc/tutorial-vs-screens.md`. Tutorials without a Brodie counterpart state so
explicitly (`no Brodie counterpart (vForth extension)`, `Ch.11 -- not transcribed
in screens` for 019/020, or `no direct counterpart in screens 800-881`). The
original screens were left untouched; the convention is recorded in
`tutorial/CLAUDE.md` section 3a. This reduces the pressure to renumber for the sake
of conceptual ordering (Open Question #1): each tutorial now carries its own
conceptual coordinates regardless of file number.

Two boundary facts worth noting (both from the wiki's finer map):

- **Ch.5 IS covered**, by 002 + 015 (`*/`, MIN/MAX/ABS, percentages,
  conversions). An earlier draft of this report wrongly listed Ch.5 as an unfilled
  backbone hole; that was an artifact of coarse chapter-level mapping and is
  retracted. The **Q8.8 fixed-point gap (Axis-1 #4) still stands** as a
  *dedicated-library* gap, but it is not a Brodie-chapter hole: Brodie Ch.5 is
  introductory "philosophy of fixed point", not a Q8.8 library.
- **Brodie Ch.11 (compilation) is NOT transcribed** in the screens, yet tutorials
  019/020 cover it -- a case where the tutorials go *beyond* the screen track. The
  inverse asymmetry to keep in mind when numbering.

The wiki's "Only on the Screens" section confirms the **BLOCK gap (Axis-1 #1)**:
block-based storage teaching (`n BLOCK ... TYPE`, `LOAD`, `-->`, the Buzzphrase
generator 880-881) lives *only* on the screens. That makes Scr# 880-881 the
natural worked example for a future BLOCK tutorial -- it is the one place
BLOCK-as-data is taught.

---

## Axis 3 -- Organisation / promotion

### `demo/` standalone programs: classify by destiny

**Promote to tutorial (light rewrite to tutorial conventions):**

| Demo | Becomes | Notes |
|------|---------|-------|
| `brot.f` | Layer2-applied tutorial | Already Next-like (layer2 + `rrrgggbb` palette). Near-ready: integer Mandelbrot. Lowest effort, high payoff. |
| `Fedora.f` | Vector + trig tutorial | Layer0 vector draw + sin-table /10000. Add note on Perl/Python table generation. |
| `*.dot.f` | Command-creation tutorial | Closes Axis-1 gap #3. |
| `Layer3-demo*` | Tilemap tutorial | Closes Axis-1 gap #2. |

**Promote to "canonical example" (stays in `demo/`, referenced from tutorials):**

These are too large for tutorial form but are excellent capstones -- "now that you
know X, see how it all fits": `cosmic-conquest.f` (742 lines), `lift-challenge.f`,
`raycast.f` / `raycast_flat.f`, `term10.f`, `color-picker.f`.

### The chomp-chomp question (legacy -> Next-like)

Verified from source: `chomp-chomp.f` is **pure legacy 48K**. Its own header says
"old-fashion UDG's and standard ROM-BEEP". Its "sprites" (Inky/Pinky/Blinky/Ted)
are **software structures in arrays**, drawn as UDG characters via `.AT`/`.INK`/
`.PAPER` on LAYER12 -- the Timex attribute model. It touches **no** hardware
sprites, **no** Layer 2, **no** copper.

Making it "Next-like" is therefore **architectural, not cosmetic**: it means
rewriting the video data model -- ghosts become hardware sprites (pattern +
9-bit X/Y), the maze becomes a tilemap. This is precisely why it is pedagogically
valuable: it is the one program that can show *the same game* in both paradigms.

**Recommendation:** keep the legacy version as the "before". Write a Next version
as the "after". The tutorial *is the diff* -- a graphics capstone that teaches the
legacy->Next transition directly. (Screen-series 600-668 "Chomp.f" decompose the
game into UDG/maze/sprite/trail/ghost sections, which gives a ready scaffold for
the side-by-side.)

### The `tutorial/afx/` problem

Hundreds of `.afx` files (full sound rips of ZX/MSX games: cybernoid, nemesis,
metalgear, vampirekiller, ...) live under `tutorial/afx/`, and are loaded into
screens 2200-2344 via `tutorial/afx/zxgames.f` etc. **Open question for the
author:** are these *assets* of tutorial 050 (AFXframe), or working material that
should move out of the tutorial tree? They inflate the repo and blur the
structure. If assets, a one-line README in `afx/` pinning them to tut 050 would
fix the ambiguity; if working material, relocate under a `work/` or `assets/`
path outside `tutorial/`.

---

## Open questions for the author

1. **Numbering**: insert new tutorials (BLOCK, tilemap, dot-command, Q8.8,
   chomp-capstone) by **renumbering**, or **append 054+**? CLAUDE.md permits
   renumbering, but with 53 files it has a real cost. A hybrid -- append hardware
   items at 054+, but *insert* the BLOCK/Q8.8 core items near their Brodie-chapter
   slot -- may serve the backbone better.
2. **AFX assets**: assets-of-050 or work-material-to-relocate? (see Axis 3).
3. **Buzzwords/BLOCK**: promote Scr# 880-881 verbatim as the BLOCK tutorial's
   worked example, or write a fresh one? The screen version is clean and already
   demonstrates BLOCK-as-data.

---

## Summary (TL;DR)

- 53 dense tutorials already cover core (001-027) and Next hardware (030-053)
  well. The system is far past "needs more tutorials"; it needs a **map** and a
  few **bridges**.
- The Brodie screen track (800-881) is a **parallel, independent reference**, not
  a rewrite of the tutorials and not a backbone to verify against -- same concepts,
  different definitions. Use it as a cross-reference; the wiki and
  `doc/tutorial-vs-screens.md` hold the concept map. (An earlier draft's claim of
  an unfilled "Ch.5 Fixed Point" hole is retracted: Ch.5 is covered by 002+015.)
- Five Axis-1 coverage gaps: **BLOCK, Tilemap/Layer3, .dot commands, Q8.8 fixed
  point, ZAP/standalone workflow** -- each already has working code in `demo/` or
  the screen corpus, so promotion (not invention) is the task.
- `demo/`: promote brot/Fedora/.dot/Layer3 to tutorials; keep cosmic-conquest,
  lift-challenge, raycast, term10, color-picker as referenced canonical examples.
- **chomp-chomp**: the legacy/Next-like split is a video *data-model* rewrite, not
  a reskin; turn it into a before/after capstone, the tutorial being the diff.
- Resolve three author decisions: numbering scheme, AFX asset placement, and
  whether to reuse Scr# 880-881 for the BLOCK tutorial.
