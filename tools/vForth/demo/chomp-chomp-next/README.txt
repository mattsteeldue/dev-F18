-----------------
 chomp-chomp-next
-----------------

Staged ZX Spectrum Next hardware rewrite of demo/chomp-chomp.f, following
prompts/CHOMP-CHOMP-NEXT-PLAN.md. Game rules (maze layout, ghost AI,
scoring, phase progression) stay identical to the original at every
stage -- only how things are drawn/played/paced changes. demo/chomp-chomp.f
itself is never touched by this work; it stays the 48K-legacy reference.

To play: INCLUDE demo/chomp-chomp-next/chomp-chomp.f, then GAME.


Stage status
------------

Stage 1 -- Sound: ROM BEEP -> AY (Turbo Sound Next).
  IMPLEMENTED, awaiting CSpect confirmation.
  NEEDS AY replaces NEEDS BLEEP. bip/bleep keep their original call-site
  shape (`[ dur pitch bip ] 2lit bleep`, dur in ms, pitch as a semitone
  offset from middle C) -- only what they do changed: a local
  period-table + pitch>period converts pitch straight to an AY tone
  period (no ROM-timing double-precision math needed), and bleep plays
  it on AY channel A for the given number of 50Hz video frames. Fixed
  volume, no envelope. maze.'s decorative startup swoosh was folded
  from a two-pass queue-then-drain trick (needed to work around ROM
  BLEEP/SPEED! timing) into one straightforward per-row bip/bleep call,
  since AY has no such coupling. sound-init (AYSETUP + 1 AYSELECT) runs
  once at the top of play-level.
  Verified in isolation in the headless emulator (pitch>period against
  hand-computed periods for pitch 0/9/12/25/39; bip's two outputs
  printed and checked; bleep executed without error) -- the full game
  file itself was NOT run headless (this game needs raised
  IDLE_INSTRS/STEP_CAP thresholds and ~41 minutes for a full pass, see
  prompts/CHOMP-CHOMP-STATUS.md; out of proportion for a sound-engine
  swap that does not touch collision/AI/maze data). CSpect confirmation
  still needed: does it sound right, and does the startup swoosh still
  play alongside the maze draw.

Stage 2 -- Hardware sprites for the six mobs (Pacman, 4 ghosts, fruit).
  Not started.

Stage 3 -- Palette-driven color effects (scared flash, fruit cycle).
  Not started.

Stage 4 -- Interrupt-driven pacing (lib/INTERRUPTS.f).
  Not started.

Stage 5 -- Tilemap maze (Layer 3) -- the capstone.
  Not started.

See prompts/CHOMP-CHOMP-NEXT-PLAN.md for the full rationale and staging
order.
