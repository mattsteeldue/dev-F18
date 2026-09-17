# chomp-chomp-next: staged Next-hardware rewrite

## Context

`demo/chomp-chomp.f` (Stages 1-4 of `prompts/CHOMP-CHOMP-PLAN.md`, all confirmed
on CSpect) is explicitly the "Phase 1" / "before" half of a plan that already
named its own sequel. Two existing notes point at the same target:

- `CHOMP-CHOMP-PLAN.md` itself: *"Il gioco resta 48K-legacy: questa e' la Fase
  1. La riscrittura con Sprite hardware e grafica hires del Next e' la Fase 2,
  gia' in TODO.md"*.
- `TODO.md`, "chomp-chomp: write a 'Next-like' capstone tutorial"
  (2026-08-22): rewrite using hardware-accelerated primitives from the
  030-059 tutorial band, naming **hardware sprites (tutorial 053)** and
  **tilemap (tutorial 058)** explicitly.

This plan is that Phase 2, broken into stages small enough to build and
confirm on CSpect one at a time, per the author's usual working style
(`demo/chomp-chomp.f` itself was built the same way -- see
`prompts/CHOMP-CHOMP-STATUS.md`, four stages, each confirmed before the
next started).

**Where it lives.** `demo/chomp-chomp-next/chomp-chomp.f` -- a new directory
next to `demo/chomp-chomp.f` and `demo/chomp-chomp/` (the ZAP-packaged
standalone build), not a branch of either. `demo/chomp-chomp.f` is never
touched by this plan: it stays the 48K-legacy reference the tutorial band
053/058 already contrasts against, and the "before/after capstone tutorial"
TODO.md envisions needs both versions to exist side by side. Stage 0 below
seeds the new file as a byte-identical copy of the current
`demo/chomp-chomp.f`, so every later stage's diff is legible against a known
baseline (same convention as `demo/chomp-chomp/chomp-chomp-0.f`).

**What stays unchanged throughout.** The game rules: maze layout format,
ghost AI (personalities, scatter/chase, targets), scoring, lives, phase
progression, the four-disk-maze rotation. This plan only replaces *how*
things are drawn and paced, not what the game does -- exactly the discipline
the original four stages already followed (e.g. Stage 2's `COLORS:` changed
only *how* color cycling was written, never what colors appeared when).

**What is explicitly deferred.** `lib/IM2-HW.f` (modern hardware IM2,
`prompts/IM2-HW-PLAN.md`) is still only a design plan -- not implemented.
Stage 4 below uses the existing, working legacy `lib/INTERRUPTS.f` instead
(already proven in tutorial 045's copper demo via `ISR-XT`). Building
IM2-HW.f for real is a separate project this plan does not depend on.

---

## Staging rationale

Ordered by two criteria: **blast radius** (does it touch collision/AI/maze
data, or only how a frame is drawn?) and **dependency** (does a later stage
need an earlier one's machinery?). Sound and hardware sprites are both
self-contained swaps behind existing call sites and can be built and
confirmed independently of everything else; the palette-driven color stage
is a light follow-on that only makes sense once sprites exist; interrupt
pacing is an architectural cleanup worth doing before the heaviest, riskiest
stage (the tilemap maze) rather than after. The tilemap maze is last because
it is the one stage that touches the collision/maze-data model
(`maze@`/`maze!`/`MAZE-CHECK`/the disk-maze loader) that every other system
in the game reads.

---

## Stage 0 -- Scaffolding (done)

`demo/chomp-chomp-next/chomp-chomp.f` created as a byte-identical copy of
`demo/chomp-chomp.f`. No behavior change. This is the baseline every later
stage's diff is measured against.

---

## Stage 1 -- Sound: ROM BEEP -> AY (Turbo Sound Next)

Swap the sound engine only. `bip`/`bleep`/`beep-pitch`/`bleep-calc`
(`NEEDS BLEEP`, ROM `BEEP`) get replaced by `lib/AY.f` tone/envelope calls at
the exact same call sites: `pacman-eat-pill`, `pacman-eat-cherry`,
`ghost-eaten`, and the `interlude`/`inter-hunt`/`inter-flee` sound-effect
words. No change to game logic, timing, or the `2lit`/`[ ... ] 2lit bleep`
call shape at each site -- only what `bleep` ultimately does. A real "waka-
waka" via one AY channel's envelope generator (arcade-style, continuous
while Pac-Man is eating) is a natural stretch goal here, since AY gives
sustained tones the ROM beeper cannot.

**Why first**: lowest risk (does not touch `maze@`, sprites, or AI), fastest
to confirm (audible on CSpect in seconds), and does not block or get blocked
by any other stage.

**Depends on**: nothing.

**Status (2026-08-27): implemented, awaiting CSpect confirmation.**
`demo/chomp-chomp-next/chomp-chomp.f` now loads `NEEDS AY` instead of
`NEEDS BLEEP`; `bip`/`bleep` keep their original call-site shape
(`[ dur pitch bip ] 2lit bleep`) and semantics (dur in ms, pitch as a
semitone offset from middle C) -- only the implementation changed. A
local `period-table` (one octave of AY 12-bit tone periods, computed
from `period = 1750000/(16*freq)`, the same clock/formula tutorial 034
documents) plus `pitch>period` replace `lib/bleep.f`'s
`BEEP-PITCH`/`BLEEP-CALC`/`12/MOD`/`FREQ-TABLE` chain -- no ROM-timing
double-precision math needed, since an AY period is already a small
12-bit value. `bleep` plays the period on AY channel A (fixed volume,
no envelope -- a sustained envelope-driven tone is a natural follow-up,
not required to match the original feel) for the requested number of
50Hz video frames via `sync-vid`, then silences it. `sound-init`
(`AYSETUP 1 AYSELECT`) runs once at the top of `play-level`.

One call site needed more than a drop-in swap: `maze.` (the startup
maze-print swoosh) bypassed `bip` entirely and called
`beep-pitch`/`bleep-calc` directly, queuing 21 rows' worth of BLEEP
args on the data stack in a silent first pass, then draining them
during the drawing pass via `>R bleep R>` (protecting the `maze-run`
pointer on the return stack while BLEEP's args sat on top of the data
stack). That two-pass queuing existed to work around ROM
`BLEEP`/`SPEED!` timing coupling that AY does not have, so it was
folded into one straightforward loop instead: compute pitch from `i`,
`bip swap bleep` it, then draw the row -- `bleep` fully resolves before
the `maze-run` pointer is touched, so no return-stack shuffle is
needed. Every other `bip`/`bleep` call site (`pacman-eat-pill`,
`pacman-eat-cherry`, `ghost-eaten`, `inter-sound`/`inter-flee`/
`inter-hunt`) was left untouched.

Verified in the headless emulator, but only in isolation: a standalone
snippet (`period-table`/`pitch>period`/`bip`/`bleep`/`sound-init`,
copied verbatim) loaded cleanly and `pitch>period` matched hand-computed
periods for pitch 0/9/12/25/39 (418/249/209/98/44 -- 12 and 25 and 39
cross-checked against the octave-shift arithmetic by hand); `bip`'s two
outputs printed as expected (`50 25 bip . .` -> `2 98`, i.e. frames=2
period=98, confirming the output order `2lit`/the direct-call sites
both rely on); `bleep` executed without error. The full game file was
**not** run headless -- this game needs raised
`IDLE_INSTRS`/`STEP_CAP` thresholds and ~41 minutes for a full pass
(`prompts/CHOMP-CHOMP-STATUS.md`), disproportionate for a sound-engine
swap that touches no collision/AI/maze-data code. **Needs CSpect**:
does it sound right, and does the startup swoosh still play alongside
the maze draw.

**2026-09-01 -- follow-on decided, deferred to Stage 4.** The raw-AY
`bip`/`bleep` here still block the game loop for the sound's whole
duration (`0 do sync-vid loop`) and are functionally "the same beep,
just on a different chip" -- no envelope, no background playback.
`lib/afxplay.f`/`AFXFRAME` (tutorial 050/055) is the natural next step:
same audible tones, but driven from a `.afx`-format frame buffer through
the interrupt-driven player, so a sound effect no longer has to freeze
gameplay while it plays. Doing this now would mean hand-rolling an ISR
just for sound, ahead of and separate from Stage 4's own ISR work; doing
it as *part* of Stage 4 means the interrupt plumbing is built once and
carries both the game-tick clock and `AFXFRAME`. See Stage 4 below for
the design questions this still needs to settle (blocking drop-in vs.
background/fire-and-forget; generated-on-the-fly vs. hand-authored
envelopes).

---

## Stage 2 -- Hardware sprites for the six mobs

Rewrite `sprite-put` to program real ZX Spectrum Next hardware sprites
(tutorial 053: slot select on port `$303B`, attribute bytes on `$57`)
instead of `sync-emit`-ing 12 UDG characters. Applies to Pac-Man, the four
ghosts, and the fruit -- **the maze itself (walls/dots/pills) stays exactly
as it is today**: UDG text cells on LAYER12, read by `maze@`/`maze!` exactly
as now. Only the moving mobs change medium.

Mechanics:

- Each mob gets a small sprite pattern set (a handful of 16x16 frames --
  Pac-Man's R/P/Q/S facings, one or two ghost frames, fruit) uploaded once
  at `init-display`/`play-level` time, the same place `UDG_1` is installed
  today.
- Sprite pixel position = cell coordinate * 8 (LAYER12's cell size), so all
  existing position math (`xy-pos@`, `x-pos`/`y-pos` fields, `.at`-style
  cell arithmetic) is reused unchanged -- only the final "draw" step differs.
- `sprite-color`/`Array`'s `color` field maps to the sprite's palette-offset
  attribute byte instead of an `.ink` call. Mind the tutorial/CLAUDE.md
  section 16 gotcha: `ERASE` every sprite struct after allocation, or a
  stale `_pattern`/`_rotmir` field shifts hues or mirrors the sprite
  silently.
- `sprite-put`'s two responsibilities split: the maze-glyph half (still text,
  for `V`/pill/fruit-under-mob bookkeeping) stays as-is; only the mob-glyph
  half moves to hardware sprites.

Also removes the "12 EMITC per sprite" cost from the draw path entirely --
already decoupled from game pacing by the earlier `pace`/`tick-frames`
refactor (Stage 1 of the original plan), but this stage is what actually
makes redraws cheap, which is what later stages (smoother motion, more
on-screen effects) need headroom for.

**Why second**: the visually defining upgrade, explicitly named in
`TODO.md`, and self-contained -- confirmable on CSpect (six sprites moving
correctly, right colors, right facing) without touching AI, scoring, or the
maze loader.

**Depends on**: nothing (sound in Stage 1 is unrelated). Blocks Stage 3.

**Status (2026-09-01): implemented, awaiting CSpect confirmation.** A new
reusable module, `lib/SPRITE.f` (`NEEDS SPRITE`), extracts the hardware
sprite engine from tutorial 053 (ports, the `SPRITE-OB` struct,
`SPRITE-INIT`/`SPRITE-UPDATE`/`SPRITE-HIDE`, `SPRITES-ON`/`SPRITES-OFF`) into
a loadable library, leaving the tutorial itself untouched; only
`SPRITE-LOAD<` (reading a whole `.spr` file) stayed tutorial-only, since
chomp-chomp-next builds its patterns programmatically instead.
`demo/chomp-chomp-next/chomp-chomp.f` adds a "hw sprites" section right
before `sprite-put` (which it replaces) with:

- **Patterns generated from the existing UDG bitmaps**, not new art:
  `mob-pattern-from-udg` unpacks each 8x8 1-bit UDG letter (R/P/Q/S for
  Pac-Man's four facings, T for the ghost body -- shared by all four ghosts,
  since they differ only by colour -- and U/X/Y/Z for the four fruit types,
  9 patterns total) into the top-left 8x8 of an otherwise-transparent 16x16
  sprite pattern, unscaled, so mobs stay the same on-screen size as before.
- **Colour via the palette-offset attribute, not per-colour patterns**:
  `mob-palette` programs 8 palette banks (offset 0-7, one per classic
  Spectrum ink number) so a pattern's foreground pixel (value 1) reads that
  bank's RGB332 ink colour and its background (value 0) reads a sentinel
  `MOB-TRANSPARENT` ($01). This is deliberately NOT the identity-palette
  shortcut tutorial 053 uses for its own demo: identity maps ink 3
  (magenta, Pinky's colour) to RGB332 $E3, which is also the *default*
  transparency key -- reusing it here would make Pinky invisible. `sprite-put`
  just stores `sprite-color` (an ink 0-7, unchanged from before) into the
  `_pattern` attribute field each draw.
- **Hardware slot = `Sprite-no`** (0-3 ghosts, 4 Pac-Man, 5 fruit) -- the
  same numbering `name-of` already assigned, so `sprite-put` needs no new
  slot-allocation logic.
- **Position**: `cell * 8 + origin`, unscaled (LAYER11 is the plain 256x192
  ULA mode this game runs in, 32x24 cells of 8x8 -- confirmed by reading
  `inc/layer11.f`, not assumed). `MOB-X-ORIGIN`/`MOB-Y-ORIGIN` (32,32) are
  the documented Next "border compensation" default for aligning sprite
  (0,0) with the paper area's top-left corner (dev guide sec.3.4) -- this
  is the one number in the whole stage that is a guess, not derived from
  reading this game's own code, and the first thing to adjust if mobs land
  off-grid on CSpect.

**A hardware sprite is an overlay, not a text overwrite -- this changes
more than the drawing call.** The old `sprite-put` had a second half,
invisible in the plan text above: `sprite@ maze c@`/`c!` bookkeeping that
redrew whatever dot/pill/blank was under a mob's *previous* cell, because
overwriting a text cell to draw a mob destroyed whatever was there before.
A hardware sprite never touches the text layer, so that bookkeeping is now
dead code (left in place, e.g. in `move-four-ghosts`, rather than risk
deleting something not fully traced) and nothing needs restoring -- but the
flip side is that nothing erases a mob's *own* sprite either when it should
disappear. The one place this bit for real: the fruit. `put-cherry` used to
rely on Pac-Man's glyph implicitly overdrawing the fruit's text cell when he
ate it; with independent hardware sprites that overdraw never happens, so
`put-cherry` now calls `5 SPRITE-HIDE` explicitly whenever the fruit is
neither visible nor freshly spawning. `init-display` also hides the fruit
slot defensively (no stale sprite from a previous level) and `interlude`
calls `SPRITES-OFF` before its text splash, so mobs don't appear frozen
behind it between levels/lives.

Verified only in isolation (same caveat as Stage 1: the full game file is
impractical to run headless -- and this session found piping it through
`emu/repl.py` via `INCLUDE`/`cat | repl.py` is not just slow but unreliable,
losing its place partway with no error surfaced, matching the documented
`INCLUDE`/`NEEDS` block-buffer-starvation bug when nested `NEEDS` calls
share `BLOCK 1`; a short snippet piped directly as top-level REPL input,
Stage 1's own method, avoids that and is what was used here). `lib/SPRITE.f`
loads cleanly stand-alone. A standalone copy of `mob-palette`,
`mob-pattern-from-udg`, `mob-upload-patterns` and `face>patid` (against a
minimal stand-in UDG table) ran without error, and `face>patid` returned the
expected pattern ids (R->0, T->4, Z->8) for all three glyph classes
(Pac-Man facing, ghost body, fruit). **Not verified even in isolation**: the
`sprite-put` coordinate/attribute arithmetic itself (traced by hand against
`SPRITE-UPDATE`'s stack comments, not executed), and everything that can
only be judged visually -- pattern shapes, the eight ink colours, the
`MOB-X-ORIGIN`/`MOB-Y-ORIGIN` alignment, six sprites moving/overlapping
correctly, and the fruit-hide behaviour. **Needs CSpect**, more than Stage 1
did.

---

## Stage 3 -- Palette-driven color effects

Once ghosts are hardware sprites, `COLORS:` (a cyclic redraw-with-different-
ink word) becomes unnecessary for the ghosts: `SCARED-FLASH` (frightened
blue/white) and the per-level fruit cycle (`FRUIT-CYCLE`) become NextReg
palette pokes (tutorial 056: `$40`/`$41`/`$43`/`$44`) on the sprite palette,
changing color with zero redraw cost and no flicker from the redraw itself.

`PILL-FLASH` (the power pill) stays a maze-text glyph in this stage (the
maze is still UDG/LAYER12 until Stage 5), so it keeps using `COLORS:`/`.ink`
as today -- this stage only migrates the sprite-side cycles.

**Why third**: a light refinement that only pays off once Stage 2 exists;
doing it before Stage 2 would mean writing the palette plumbing twice.

**Depends on**: Stage 2.

---

## Stage 4 -- Interrupt-driven pacing (legacy IM2, `lib/INTERRUPTS.f`)

Replace the `halt`-based `sync-vid`/`pace` (a busy loop, `ei halt` x
`tick-frames`) with a real ISR installed via `ISR-XT` that increments
`ticks` at 50 Hz in the background. `heart-beat`'s own execution time (now
lighter thanks to Stage 2's hardware-sprite redraws) stops competing with
the frame clock: the game tick becomes a property of the interrupt, not of
how long drawing took.

This uses the **existing, working** `lib/INTERRUPTS.f` (confirmed on CSpect
via tutorial 045's copper split-scroll demo) -- not `lib/IM2-HW.f`, which
remains an unimplemented design plan (`prompts/IM2-HW-PLAN.md`). If the
author later wants proper hardware-IM2 daisy-chain priority, that is a
separate prerequisite project, not a blocker here.

**Also folds in the Stage 1 sound follow-on (decided 2026-09-01):**
migrate `bip`/`bleep` off raw AY register writes and onto
`lib/afxplay.f`'s `AFXFRAME` (tutorial 050/055), sharing the ISR this
stage installs for the game clock. Two design questions to settle when
this stage is picked up:
- **Blocking drop-in vs. background/fire-and-forget.** Either `bip`/
  `bleep` build a small `.afx` buffer and still play it with a blocking
  loop (same feel as today, only the mechanism changes), or sound
  becomes a `AFX-CH-DESC` store (tutorial 055's `FIRE`/`SFX-START`
  pattern) and plays in the background while the game keeps moving --
  a real gameplay change, not just a mechanism swap.
- **Generated-on-the-fly vs. hand-authored envelopes.** Either a helper
  synthesises N identical frames from the current `(period frames)`
  pair (reproduces exactly today's flat-volume tone through the new
  engine), or each event (pill/cherry/ghost-eaten/swoosh) gets a
  hand-written frame sequence with a real attack/decay envelope --
  closer to an arcade effect, but no longer "the same sound".

**Why fourth**: an architectural cleanup best done once the draw path is
cheap (Stage 2) and before the heaviest stage (Stage 5), where a stable,
CPU-decoupled clock matters most. Purely internal -- should be
indistinguishable from Stage 3 in play (game pacing), confirmed by the
game feeling identical in pace on CSpect; the sound engine swap is the one
part of this stage that IS meant to be user-visible/audible, per the two
questions above.

**Depends on**: Stage 2 (for the pacing headroom to matter). Not required by
Stage 3.

---

## Stage 5 -- Tilemap maze (Layer 3, tutorial 058) -- the capstone

Redraw the maze itself -- walls, dots, power pills -- as tiles on the
dedicated Layer 3 tilemap hardware layer instead of UDG text cells on
LAYER12. This is the stage `TODO.md` names explicitly and the highest-effort,
highest-risk one: it touches the collision/maze-data model every other
system reads (`maze@`/`maze!`, `MAZE-CHECK`, `maze-line`/`load-maze-row`,
the four-disk-maze rotation on Screen 740-745). It also removes the UDG
budget pressure that drove the original Stage 3 (14 wall letters is a hard
ceiling for LAYER12 text; a tilemap has no such 21/26-glyph limit).

Deliberately **not broken into sub-parts yet** -- this deserves its own
planning pass once Stages 1-4 are solid and confirmed, the same way the
original plan's Stage 4 (mazes on Screen) got its own two-session breakdown
after Stages 1-3 landed. Candidate follow-on, once Stage 5 exists: **smooth
sub-cell pixel movement** for the sprites (no longer glued to an 8x8 text
cell), the single biggest remaining "feel" difference from the arcade --
but only viable after both Stage 2 (sprites) and Stage 5 (a maze whose
walls are pixel-addressable) are in place.

**Depends on**: Stage 2 (sprites already moved off the text grid, so the
maze can follow without a double transition). Should follow Stage 4 (a
stable clock before the biggest rewrite), though not strictly blocked by it.

---

## Toolbox, not dedicated stages

Two more Next-specific techniques are useful *inside* the stages above
rather than as stages of their own -- naming them now so they are not
forgotten, without forcing a slot in the sequence:

- **Copper** (`lib/copper.f`, confirmed working via tutorial 045): a
  zero-CPU alternative to a palette poke for a per-scanline effect (e.g. a
  split status-bar look), or an alternative mechanism for Stage 3's color
  cycling. Optional, evaluate when Stage 3 is underway.
- **DMA** (`lib/DMA.f`/tutorial 054): candidate for fast tile-grid fills or
  bulk copies once Stage 5's tilemap exists (e.g. redrawing a whole maze on
  level transition). Optional, evaluate when Stage 5 is underway.

Keyboard-matrix direct scan (tutorial 051) was also considered and set
aside: current input (`LASTK`/Kempston `31 p@`) is not a limitation for a
single-direction game like this one, so it stays a backlog idea, not part
of this plan.

---

## Verification discipline (carried over from the original plan)

Same rules `CHOMP-CHOMP-STATUS.md` already established for this codebase:

- `emu/repl.py` cannot run this game with default thresholds (silently
  stalls) -- raised `IDLE_INSTRS`/`STEP_CAP` and a background run take ~41
  minutes for a full pass, so headless verification here is for compile-
  cleanliness and isolated logic, not full playthroughs.
- Every stage needs an actual CSpect confirmation before being marked done
  -- hardware sprites, palette pokes, interrupts and tilemap all live in
  territory the headless emulator does not model reliably (or at all).
  `demo/chomp-chomp-next/README.txt` (to be written alongside Stage 1)
  should track stage-by-stage status the same way `demo/README.txt` does
  for the original.
