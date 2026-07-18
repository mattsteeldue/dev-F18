\
\ vForth Tutorial / Demo / Screen-Corpus -- Three-Axis Gap Analysis
\ Snapshot: dev-F18/main, updated 2026-07-19 (through commit c4c2af3).
\ Subject to drift after Claude Code sessions.
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
| **Tutorials** | `tutorial/NNN-*.f` (001-054) | Self-contained `.f` source, INCLUDE-able | Modern, structured, authoritative teaching |
| **Brodie screens** | `!Blocks-64.bin` Scr# 800-905 | BLOCK screens, LOAD-able | Transcription/adaptation of *Starting FORTH* (Brodie) Ch.1-11; parallel reference track |
| **Example screens** | `!Blocks-64.bin` (scattered) | BLOCK screens | Working code: graphics, sound, asm, system, games |

The tutorials and the Brodie screens are **parallel but independent** tracks, not
one a rewrite of the other. They teach the same Forth concepts with **different
definitions** (`SHOW-SUM`/`CLAMP`/`SAFE-DIV` vs Brodie's `STAR`/`EGGSIZE`/`R%`),
so the overlap is **conceptual, not lexical** -- at the level of definition names
it is essentially nil. The screens are therefore not a deprecated old version but
a **second, cross-referenceable reference track**: the same concept rendered twice
in two idioms. The authoritative concept-to-concept mapping lives in the wiki page
"Tutorials vs. Starting FORTH Screens" and, at definition granularity (~58 rows
with a match-strength column), in `prompts/tutorial-vs-screens.md`. This report defers
to those for Axis-2 detail. The `demo/` `.f` files are a fourth, separate body:
large standalone programs.

---

## Axis 1 -- Language / feature coverage

### Tutorial series 001-054 (already solid)

- **Core language (001-027)**: stack, output, bases, defining words, control
  flow, loops, memory, strings, CREATE/DOES>, bit ops, return stack, CASE,
  pictured output, double, input, DEFER/IS, vocabularies, compilation, EVALUATE,
  introspection, structures, floating point, advanced memory, CATCH/THROW,
  assembler. This block is **substantially complete** for a standard Forth.
- **Block storage / editing (028-029)**: BLOCK mechanism (028) and the EDIT
  full-screen editor (029) -- the two formerly-empty slots between the core and
  hardware tracks, now filled (see gap #1 below).
- **Next hardware (030-053)**: ULA/Layer0, screen, timing, beeper, AY, keyboard,
  ULA graphics, Layer2, sprites (x2), Next registers, MMU, file I/O, filesystem,
  mouse, copper, BMP, UART, RPi0, interrupts, AFXframe, keyboard matrix, modular
  graphics.
- **Block-as-data (054)**: the BLOCK-as-binary-asset technique (LOAD2BLOCK + the
  AFX sound library), appended after the hardware track because it cross-refers
  tutorial 050 (AFXframe).
- **Dot commands (057). [CLOSED 2026-07-18]** `057-dot-commands.f` (462 lines)
  now covers standalone NextZXOS `.command` creation: what a dot command is
  (fixed $2000 origin, 8K max, esxDOS/NextZXOS ABI), the CODE-word-ends-in-RET
  vs NEXT calling-convention distinction, the DOT-RELATIVE address-translation
  technique with its three equally-correct forms (`REL-AA,`/`REL-NN,` shorthand,
  manual `DOT-RELATIVE ... AA,`, and direct post-hoc patch), the TESTER pattern
  for exercising the code in-place before relocation, and SAVE-BYTES/PAD"/
  UNLINK to write the file to `C:/DOT/`. It extracts the technique from the
  four `demo/*.dot.f` worked examples (helloworld, echo, parser, savebank)
  rather than duplicating them, and is registered in `lib/TUTORIAL.f`'s
  `TUT-TABLE` (`TUT-MAX` 56 -> 57). This closes former Axis-1 gap #3 below.
  The old placeholder slot for a DMA tutorial was renumbered `057-dma.f` ->
  `058-dma.f` to make room (still unwritten; see Open Questions).

All are dense (136-462 lines); none are stubs.

### Coverage gaps (capability present in the system, absent from tutorials)

1. **BLOCK / native Forth storage. [CLOSED 2026-06-21]** Now covered by three
   tutorials: **028-blocks** (the mechanism: BLOCK/BUFFER, UPDATE/FLUSH/
   EMPTY-BUFFERS, B/BUF B/SCR C/L L/SCR, (LINE)/LIST/INDEX, LOAD and `-->`,
   reserved blocks, the block-vs-screen unit trap, and the structure-across-
   boundary / NUL pitfalls); **029-edit** (the EDIT full-screen editor -- keys,
   the `[Edit]` command menu, PAD-based line ops, saving via FLUSH, and a note
   on LED as the upper-8K-RAM evolution of EDIT); and **054-blocks-as-assets**
   (the BLOCK-as-binary-asset technique, below). Note `THRU` is **not** a vForth
   word -- multi-screen loading uses `-->`. Worked screen examples remain a rich
   reference: besides **Scr# 880-881 (Buzzphrases Generator)** reading a word
   table via `881 (LINE)`, the **Scr# 882-895** add a `SCREENS`/`BLOCKS` lister
   (882), `CHANGE` byte-level block editing (886-887), `FORTUNE` BLOCK-as-data
   (888), and a full **virtual array on disk** (890-895). On the earlier "EDIT/LED
   are not good tutorial subjects" call: reversed by the author -- 029 now
   introduces EDIT directly, since it is the practical front-end to the BLOCK
   substrate.
2. **Layer 3 / Tilemap.** Covered only by `demo/Layer3-demo1/2/3` (sophisticated:
   40/80 col, 1-bit vs 4-bit tile defs, base address overlapping the display
   file). No tutorial. Also present as screen studies (Scr# 340, 420-436
   "TILEMAP study").
3. **`.dot` command creation. [CLOSED 2026-07-18]** Now covered by
   **057-dot-commands.f**, which extracts the pattern (assembler + relocation
   + save-bytes + `$2000`-relative addressing) shared by
   `demo/echo|helloworld|parser|savebank.dot.f`, using `helloworld.dot.f` as
   the running example and pointing to the other three for further reading.
   Screens (286, 357, 581, 940-941) remain as a cross-reference. Writing the
   tutorial also surfaced a real bug in `demo/parser.dot.f`: two call sites
   (`main`'s call to `parse`, `help`'s call to `print`) used plain `AA,`
   instead of a relocating form, embedding the live-dictionary address
   instead of the `$2000` one -- invisible to interactive testing because
   `TESTER` calls `MAIN` in place, before relocation, and would only crash
   once the saved file actually ran standalone. Fixed in both call sites;
   the three valid relocation mechanisms (`REL-AA,`/`REL-NN,` shorthand,
   manual `DOT-RELATIVE ... AA,`, direct post-hoc patch) are now named at
   every relocation point in the file via inline comments, and the general
   pattern/pitfall is documented in `tutorial/CLAUDE.md` section 17.
4. **Fixed-point (Q8.8 / 12.4).** Screens 590-595 ("Product routine for 12:4
   fixed point") exist; the Q8.8 work is not yet a tutorial. The `*/` 32-bit
   intermediate trick and `SPLIT` belong here.
5. **`ZAP` / standalone executable workflow.** Chomp-chomp documents `ZAP` as the
   simplest way to produce a standalone game; the workflow is never given tutorial
   form (related: Scr# 670 "Create standalone executable").

---

## Axis 2 -- Cross-reference structure (parallel tracks)

The screen series 800-905 is a vForth transcription/adaptation of *Starting FORTH*
(Brodie) Ch.1-11, keeping Brodie's original names. It runs **parallel** to the
tutorials, not under them: same concepts, independent definitions. It is best used
as a **cross-reference track** -- a reader can see a concept rendered twice, once
in vForth-idiom tutorial form and once in Brodie-idiom screen form.

Concept correspondence (topics present in BOTH tracks), per the wiki:

| Brodie ch. / Scr# | tutorial counterpart | shared concept |
|-------------------|----------------------|----------------|
| Ch.1 800-804 | 003, 005 | `:`, `." "`, `EMIT`, `CR`, `SPACES` |
| Ch.2 805-814 | 001, 002 | postfix arith, `DUP/SWAP/ROT/OVER`, `/MOD`, `.S` |
| Ch.3 815 (+882-895) | 028, 029 | `EDIT`/`LED`, `LIST`/`LOAD`, BLOCK/Screen storage |
| Ch.4 816-820 | 006 | `IF/ELSE/THEN`, `?DUP`, `WITHIN` |
| Ch.5 821-825 | 002, 015 | `*/`, `MIN/MAX/ABS`, percentages, conversions |
| Ch.6 826-837 | 007 | `DO/LOOP`, `+LOOP`, `?DO`, `I/J`, `LEAVE`, `BEGIN/UNTIL` |
| Ch.7 838-849 | 014, 004 | `<# # #S #> HOLD SIGN`, `.R/U.R`, `BASE`, `HEX/DECIMAL` |
| Ch.8 850-867 | 005, 008, 010, 023 | `VARIABLE/CONSTANT`, `!/@/+!`, `CREATE/ALLOT/,`, arrays |
| Ch.8 (double) | 015 | `2VARIABLE/2CONSTANT`, `2@/2!`, `D./D+/M+` |
| Ch.9 868-876 | 017, 022 | `'`/`[']`/`EXECUTE`, vectored exec, `SEE` |
| Ch.10 877-895 | 009, 016 | `TYPE`, `-TRAILING`, `TEXT`, `EXPECT`, strings, I/O, BLOCK-as-data, virtual array |
| Ch.11 896-905 | 010, 019, 020, 021 | `CREATE/DOES>` defining words, `IMMEDIATE`, `[COMPILE]`, `COMPILE`, `LITERAL`, `LOOPS` |

**Status (2026-06-21): cross-reference lines added; Ch.10 completed and Ch.11
transcribed.** Each tutorial 001-029 now carries a
`\ Starting FORTH (Brodie): Ch.N  |  vForth screens NNN-NNN` line in its header
(immediately above `Reference:`) -- including the block-storage pair 028/029, whose
Brodie counterpart is **Ch.3 "The Editor (and Staff)"** (the disk/BLOCK/editor
chapter, screen 815 plus the Ch.10-completion screens 882-895), so the
concept-to-screen mapping above is visible
at the point of use, not only in this report and `prompts/tutorial-vs-screens.md`. The
screen corpus itself was then extended: **Ch.10 was completed to Scr# 895** (TEXT
input, block editing, virtual arrays) and **Ch.11 "Extending the Compiler" added at
Scr# 896-905** (defining words, IMMEDIATE/[COMPILE]/COMPILE/LITERAL, LOOPS). The
defining-word and compilation tutorials (010, 019, 020, 021 partially) therefore now
point at real screens. Tutorials still without a Brodie counterpart state so
explicitly (`no Brodie counterpart (vForth extension)` or `no direct counterpart in
screens 800-905`). The original screens 800-881 were left untouched; the convention
is recorded in `tutorial/CLAUDE.md` section 3a. This reduces the pressure to renumber
for conceptual ordering (Open Question #1): each tutorial carries its own conceptual
coordinates regardless of file number.

Two boundary facts worth noting (both from the wiki's finer map):

- **Ch.5 IS covered**, by 002 + 015 (`*/`, MIN/MAX/ABS, percentages,
  conversions). An earlier draft of this report wrongly listed Ch.5 as an unfilled
  backbone hole; that was an artifact of coarse chapter-level mapping and is
  retracted. The **Q8.8 fixed-point gap (Axis-1 #4) still stands** as a
  *dedicated-library* gap, but it is not a Brodie-chapter hole: Brodie Ch.5 is
  introductory "philosophy of fixed point", not a Q8.8 library.
- **Brodie Ch.11 (compilation) is now transcribed** (Scr# 896-905): `CREATE/DOES>`
  defining words (896-898), `IMMEDIATE`/`[COMPILE]`/`COMPILE`/`LITERAL` (899-900),
  and the chapter problems (901-905). This closes the asymmetry an earlier draft
  noted (tutorials 019/020 once went *beyond* the screen track); the screen track
  has caught up. Ch.11 is also where Brodie actually teaches the defining-word
  technique, so tutorial 010-create-does now maps to Ch.11 (896-898) as well as the
  Ch.8 arrays it was previously pinned to.

The block-based storage teaching (`n BLOCK ... TYPE`, `LOAD`, `-->`) is now taught
in the tutorial track too (028/029/054, **Axis-1 #1 closed**), with the screens as
a worked-example reference: the Buzzphrase generator (880-881), the Ch.10-completion
screens 882-895 (block lister, `CHANGE` editing, `FORTUNE`, the 890-895 virtual
array), and the AFX banks at Scr# 2200+ that 054 draws on directly.

---

## Axis 3 -- Organisation / promotion

### `demo/` standalone programs: classify by destiny

**Promote to tutorial (light rewrite to tutorial conventions):**

| Demo | Becomes | Notes |
|------|---------|-------|
| `brot.f` | Layer2-applied tutorial | Already Next-like (layer2 + `rrrgggbb` palette). Near-ready: integer Mandelbrot. Lowest effort, high payoff. |
| `Fedora.f` | Vector + trig tutorial | Layer0 vector draw + sin-table /10000. Add note on Perl/Python table generation. |
| `*.dot.f` | Command-creation tutorial | **DONE (057-dot-commands.f, 2026-07-18)** -- closed Axis-1 gap #3; also fixed a latent relocation bug the writing surfaced (see gap #3 above). |
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

1. **Numbering [PARTLY SETTLED 2026-06-21, further precedent 2026-07-18]**: the
   hybrid was adopted -- the core BLOCK items were *inserted* in the two empty
   slots (028 BLOCK mechanism, 029 EDIT) right after the core backbone, while
   the block-as-data piece was *appended* at 054 because it cross-refers the
   hardware-track AFXframe (050). The dot-command tutorial followed the same
   append precedent: written at **057** (after 055-afx-sound-board and
   056-layer2-palette), pushing the still-unwritten DMA placeholder from
   `057-dma.f` to `058-dma.f`. Still open for the remaining gaps (tilemap,
   Q8.8, chomp-capstone): append at 059+ or insert?
2. **AFX assets [PARTLY ANSWERED]**: 054 now formally documents `LOAD2BLOCK` and
   names the Scr# 2200+ AFX banks as its worked example, pinning the `tutorial/afx/`
   tree to tutorials 050+054. The repo-inflation question (relocate under
   `work/`/`assets/` vs. keep) is still open, but the *purpose* is no longer
   ambiguous.
3. **Buzzwords/BLOCK [CLOSED]**: resolved by writing fresh tutorials rather than
   promoting a screen verbatim -- 028 teaches the mechanism, 054 teaches the
   author's original BLOCK-as-binary-asset use (`LOAD2BLOCK`). The screen examples
   (Buzzphrase 880-881, block lister 882, `CHANGE` 886-887, `FORTUNE` 888, virtual
   array 890-895) remain as a cross-reference, not the primary teaching.

---

## Summary (TL;DR)

- Dense tutorials cover core (001-027), block storage/editing (028-029), Next
  hardware (030-053), block-as-data (054), AFX sound (055), Layer2 palette (056),
  and dot commands (057). The system is far past "needs more tutorials"; it
  needs a **map** and a few **bridges**.
- The Brodie screen track (800-905) is a **parallel, independent reference**, not
  a rewrite of the tutorials and not a backbone to verify against -- same concepts,
  different definitions. Use it as a cross-reference; the wiki and
  `prompts/tutorial-vs-screens.md` hold the concept map. (An earlier draft's claim of
  an unfilled "Ch.5 Fixed Point" hole is retracted: Ch.5 is covered by 002+015.)
  It now spans Brodie Ch.1-11: Ch.10 was completed to Scr# 895 and Ch.11 added at
  896-905, so the once-missing compilation/defining-word counterparts exist.
- Axis-1 coverage gaps: **BLOCK is now closed** (028 mechanism, 029 EDIT, 054
  block-as-data), and **`.dot` commands are now closed** (057, which also
  surfaced and fixed a real relocation bug in `demo/parser.dot.f` -- see
  `tutorial/CLAUDE.md` section 17). Remaining: **Tilemap/Layer3, Q8.8 fixed
  point, ZAP/standalone workflow** -- each already has working code in `demo/`
  or the screen corpus, so promotion (not invention) is the task.
- `demo/`: promote brot/Fedora/Layer3 to tutorials (`.dot.f` already promoted,
  see above); keep cosmic-conquest, lift-challenge, raycast, term10,
  color-picker as referenced canonical examples.
- **chomp-chomp**: the legacy/Next-like split is a video *data-model* rewrite, not
  a reskin; turn it into a before/after capstone, the tutorial being the diff.
- Resolve three author decisions: numbering scheme, AFX asset placement, and
  whether to reuse Scr# 880-881 for the BLOCK tutorial.
