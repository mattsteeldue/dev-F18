# Fix tutorial bugs -- plan

Audit of all 67 tutorials performed 2026-09-23 (static reading + mechanical
checks + loading every file in the headless emulator + running every
`\   code  => expected` example and comparing the real output).
Nothing below has been fixed yet unless marked DONE.

Rules to respect while fixing (see root CLAUDE.md and tutorial/CLAUDE.md):
7-bit ASCII, no TAB, lines <= 80 bytes, file must not end with a space before
the final LF, minimal diff (no trailing-space cleanups), no HEX/DECIMAL
switch at load time (use `$`/`%`/`#`), `[']` inside definitions.
The author commits via GitHub Desktop: do not commit.

## 0. Already DONE by the author (verified in emulator 2026-09-23)

- 015:146 `.( (should print 3000) )` -> `."` : file now loads completely.
- 017:62  `42 DISPLAY-ITEM DROP` : stack clean after load.
- 023:69  `INIT-POINT` uses `TUCK` : prints x=10 y=20, no stray store.
- 054:36  banner uses `."` : prints fully (then stops at NEEDS DMA, known).

## 1. Runtime bugs in code (highest priority)

| File:line | Bug | Fix |
|---|---|---|
| 013:50, 100-117 | Text says "DROP n in the default section"; `DESCRIBE` consumes n with `.` then ENDCASE drops again -> `42 DESCRIBE` = "Stack is empty" (confirmed) | default must leave n: `." number " DUP .`; rewrite line 50/100 text: ENDCASE drops n, never DROP it yourself |
| 030:181 | `DROP ." ?"` in CASE default -> double drop | remove the DROP |
| 026:88-92 | `TRY-SQRT` has no `ELSE DROP`: on success leaves the CATCH 0 on top | add `ELSE DROP` like PROTECTED-DIV |
| 026:136-144 | `WITH-CLEANUP` wrong on both paths (success leaves `n3 0`, error leaves `n1 n2 0`); comment says "Square root", stack comment `( n -- )` wrong | `( n1 n2 -- n3 \| 0 )`, error: `DROP 2DROP 0`, success: `DROP`; fix comment; section says "use saved stack depth" but code doesn't |
| 057:283-340 | `.HELLO` calls PRINT, but PRINT is compiled BEFORE `HERE ORG !`, so it is outside the saved range `ORG @ HERE OVER -`; `' PRINT REL-AA,` yields an address below $2000 (ROM) -> saved dot command crashes | set ORG before PRINT and make the first bytes at ORG a `jp`/`jr` to the entry code, or inline the print loop inside .HELLO like demo/helloworld.dot.f; update section 8 text; add note to tutorial/CLAUDE.md sec.17 (new variant: target outside saved range) |
| 036:158 | `DOT-PATTERN` uses `I J PLOT` (transposed: x=row) -> right 64 columns silently clipped | `J I PLOT` |
| 038:168 | `L10-DEMO` same transposition (LAYER10 is 128x96) | `J I PLOT` |
| 038 sec.6 | PAINT example: in LAYER2 EDGE = `ATTRIB =`; outline in 224, fill in 7 -> floods whole screen | fill with the same colour as the outline (224) |
| 044 MOUSE-DRAW | `MOUSE` returns click EVENTS (cleared on read): one pixel per click, not "hold to draw"; sprite coords have origin 32px up-left of ULA screen so the pixel is not under the cursor | track down/up events in a flag; subtract 32 from both coords (and check ranges); also exit with `LAYER12 1 .PAPER` not `LAYER0 CLS` |
| 056 DIM-2ND-PALETTE | mask `%10110110` clears bits 6,3,0 (LSBs), comment says "drop msb / halved brightness" -> effect almost invisible | halve each field: e.g. `%01101101` keeps... better compute R/2,G/2,B/2 per field; at least use `%01101101` (drops MSBs) |
| 039 SPRITE-DEMO | uploads/shows slot 0 but `1 SPRITE-HIDE`; comment "slot 1" | `0 SPRITE-HIDE`, fix comment |
| 040 sec.1 / tests | example `$AA $05 REG!` ("LED reg") writes Peripheral 1 (joystick, 50/60Hz, scandoubler!) ; test `0 SPEED! 0 SPEED@ -> 0` leaves 2 cells | pick a harmless reg (e.g. $14 global transparency, save/restore) ; test `0 SPEED! SPEED@ -> 0` (also the `2` one) |
| 050 sec.6 | `4400 BLOCK <addr> 512 CMOVE UPDATE` args reversed | `<addr> 4400 BLOCK 512 CMOVE UPDATE` |
| 041 sec.5 | template WITH-PAGE: `R@ EXECUTE` executes the saved page, not the xt | `( xt page -- ) MMU7@ >R MMU7! EXECUTE R> MMU7!` |
| 037 sec.2 | typo `224 TO ATRIB` | `ATTRIB` |
| 034 sec.4 | double-division snippet broken (`1750000` without `.` is not a double; `OVER` copies wrong cell) | `freq 16 * >R 1750000. R> UM/MOD NIP` |
| 054:121, 140 | `.( to port $FE (border) )` / `(keyboard)` inside definitions: inner `)` ends the string, stray `)` compiled -> will break once lib/DMA.f exists | use `."` or remove the inner parentheses |
| 053 | after INCLUDE the user variable S0 reads 0 (was 54008): DEPTH/.S show nonsense (DEPTH=5765). Cause NOT found yet | investigate first (bisect the file in the emulator: `S0 @ U.` after each section) |

## 2. Wrong expected outputs in `=>` examples (confirmed in emulator)

| File:line | Written | Real / fix |
|---|---|---|
| 001:105 | `22 7 /MOD . .  => 1 3 (remainder then quotient)` | `3 1` (quotient printed first); also emu/TUTORIAL-TESTING.md repeats it |
| 003:101 | `HEX 255 . => FF` | prints 255 ($255 read in hex): write `255 HEX . DECIMAL` |
| 004:114-115 | `120,000 .S => 120000 0`, `3.14159 .S => 314159 0` | `54464 1`, `52015 4` (lo hi of the double); explain |
| 015:57 | `120,000 .S => 120000 0` | `54464 1` |
| 015:79-80 | `50,000 S>D 50,000 S>D D+` | `50,000` is already double: remove the S>D (`50,000 50,000 D+ D.`) |
| 007:79, 123, 130 | `.DOWN` => `5 4 3 2 1` | real `6 5 4 3 2 1 0` (-1 +LOOP includes the limit): `1 SWAP DO I . -1 +LOOP`; fix rule at line 120 |
| 011:165-167 | `$1234 SPLIT FLIP . => $1234` "no 8 LSHIFT OR needed" | prints 4608 and leaves $34: `SPLIT FLIP OR` |
| 014:57 | `$41 0 <# #S [CHAR] $ HOLD #> TYPE => $41` | `$65` in decimal: wrap with HEX ... DECIMAL or use 65 |
| 025:151 | `HP@ @ U.` | extra `@`: `HP@ U.` (as line 153) |
| 000:76 | `HELP NOSUCHWORD => NextZXOS Open error.` | real: `help/NOSUCHWORD.txt File not found.` |
| 008:170 | `VOWELS 2 CHARS + C@ EMIT` | CHARS is not core: add `NEEDS CHARS` note or use `2 +` |
| 030:224 | `HEX 0 3 LSHIFT 7 OR 40 OR ...` claims $7A | computes $47: `7 3 LSHIFT 2 OR 40 OR` |
| 019:158 | `UDG+` comment "A-Z -> 165-190", "~165" | A -> 144 .. Z -> 169 |

## 3. Wrong facts in prose (verified on doc/zx-next-dev-guide-r3.md or libs)

- 040 NextReg table: palette index/value are $40/$41 (not $10/$11; $10 is
  anti-brick/core boot); video timing is $11 (not $17 = Layer 2 Y offset);
  $22 = Line Interrupt Control (not LoRes); $0A = mouse config, core
  sub-minor is $0E; $12 is a 16K BANK. .NEXT-INFO prints wrong registers.
- 047: "video timing mode (reg $17)" -> $11 (lib/RPi0.f:64 reads $11).
- 039 sec.1: attribute layout wrong -- attr2 = palette offset 7:4, X
  mirror 3, Y mirror 2, rotate 1, X8 0; attr3 = visible 7, attr4-enable 6,
  pattern 5:0 (tutorial/CLAUDE.md sec.16). Left edge is X=32 (guide: origin
  32px up-left of ULA), not 8. Transparency is $E3, not 0.
- 045 sec.1: copper WAIT = horizontal bits 14-9, vertical bits 8-0 (as
  lib/copper.f). Side note (library bug): COP-WAIT does `$FF AND` on the
  line -> lines 256-311 unreachable.
- 058 sec.1/3: TILE-80 ($6B=%11001001) HAS the attribute byte and is text
  mode; TILE-TXT (%11101001) is the one without attribute.
- 041 sec.1 slot table: slot 3 ($6000) is not ULA screen, vForth code starts
  at $6366 (RAMTOP $61FF, IM2 table $6200).
- 043 sec.4: install dir is tools/vForth, launcher Forth18_loader.bas (plus
  dot command .vforth); fix C:/NextZXOS/vForth examples.
- 033 sec.2: `$07A7 $00DC BLEEP` is A3 220 Hz for 1 s (n1 1959); for 440 Hz:
  n1=964 ($03C4), n2=440 ($01B8). Remove the HEX in the example.
- 034 sec.5 and 050 sec.9: AYSETUP does NOT call ENABLE-TURBOSOUND.
- 028:42,96 and 063:113: "nothing reaches SD until FLUSH" is false -- dirty
  buffers are written when recycled (055 sec.7(c) is right).
- 042 sec.7 error codes: #44 = DOS call error, #45 = Pos error, #39 =
  Opendir error, #48 is a header line (no rename error). 046 sec.1 lists
  39 as "wrong dimensions": lib/bmp-load.f:61 uses #39, whose text is
  "NextZXOS Opendir error." (library message-number bug).
- 037: gradient comments red/green swapped; sec.3 "may wrap" stale (L2-PLOT
  skips out-of-range since June). 038 sec.5 stale for the same reason.
- 031 COLOR-GRID: paper cycles by column (I), comment says rows.
- 060 sec.5: EMIT masks only codes >= $90; 128-143 print, control codes
  not in the table print nothing -> "first two glyphs match" compares two
  empty outputs. Rewrite the explanation/demo.
- 056: PAL-RESET-BYTE $20 selects the SPRITES first palette as edit target
  (bits 6-4 = %010), comment says Layer 2.
- 052 sec.7: NEWTASK also forgets the graphics modules (loaded after MARKER).
- 029 EDIT-SCREEN guard `8 <` still allows editing Screen 8 (messages), 9
  and 11 (AUTOEXEC).
- 032 STOPWATCH comment "auto-detect once at load time": it is run time.
- 050 sec.2: AFX-CH-DESC description inconsistent (48 bytes vs "6 channels,
  2 words"); 055 says 9 voices x 4 bytes. Reconcile with lib/AFXFRAME.f.
- 047: NEEDS RPI0 runs RPI0-INIT at load (lib/RPi0.f:473): side effect
  28 MHz + RPi0 UART selected just by loading the tutorial -- mention it.

## 4. Broken references / housekeeping

- 064:43 -> `tutorial/064-scaled-integer-math.png` does not exist (files are
  064-brot.png, 064-brot-bulb.png); tutorial/CLAUDE.md sec.15 same.
- 027:216 -> `inc/VIDEO-SYNC.f` does not exist.
- 061:32 -> `prompts/LOCALS-PLAN.md` moved to `planners/archive/`.
- 054:18, 056:23 -> `doc/zx-next-dev-guide-r3.txt` is now `.md`
  (tutorial/CLAUDE.md sec.15 too).
- TODO.md: "Missing tutorial: fixed-point" and "Promote brot/Fedora" are
  done (064/065) -> move to TODO-DONE.md.
- Root CLAUDE.md says plans go in `prompts/`, repo now uses `planners/`.

## 5. Conventions (low priority)

- HEX/DECIMAL at load time: 030:228-232, 031:106-108, 050:146-151.
- 039: 25 lines with CRLF (lines 91-119).
- NEEDS REG!/REG@ (core words) in 039, 040, 041.
- tutorial/CLAUDE.md sec.1 allows TAB, root CLAUDE.md forbids it.
- 035 test block uses `[CHAR]` at interpret level (works, but CHAR is the
  documented idiom).

## 6. Not verifiable headless (need CSpect)

024 (ROM calculator), all GRAPHICS tutorials (036-038, 044, 052, 056, 065:
"SETUP? NextZXOS DOS call error"), 047/048 (UART), 057 relocation, sprites,
copper, palette, mouse.

## How to verify (headless emulator)

Python: `C:\Users\matteo\AppData\Local\Python\pythoncore-3.14-64\python.exe`
(set `PYTHONIOENCODING=utf-8`). Run from `tools/vforth`. A minimal driver:

```python
import sys, time; sys.path.insert(0, 'emu'); import repl
r = repl.Repl(); r.emu.queue_input("n"); r._run_to_prompt(); r._drain()
for c in sys.argv[1:] + [".( @@END@@)"]: r.emu.queue_input(c)
buf = ""
while "@@END@@" not in buf:
    ok = r._run_to_prompt(); buf += r._drain()
    if not ok: break
print(buf)
```

e.g. `python drv.py "INCLUDE tutorial/013-case.f" "42 DESCRIBE" "S0 @ SP@ - 2/ ."`
(empty stack prints 1). Each boot+load takes 20-300 s. The emulator writes
real files: back up `!Blocks-64.bin` before running tutorials that UPDATE
blocks (028, 055, 063) and check `git diff --quiet -- '!Blocks-64.bin'`.
Remember `.(` and `[CHAR]` are state-smart in vForth (not bugs inside
definitions); LOCALS outputs after `--` are pushed automatically.

## Status 2026-09-24 -- plan carried out

Every item of sections 1-5 has been applied (not committed), except 053
(below). Beyond the plan:
- 040 sec.7 REG-ROUNDTRIP wrote $55/$AA into $06 (Peripheral 2: PS/2
  mouse/keyboard, DivMMC, F8/F3 keys): moved to $7F (user storage).
  Machine ID: $0A on a real Next, $08 on emulators.
- lib/copper.f COP-WAIT `$FF AND` -> `$1FF AND` (lines 256-311).
- lib/bmp-load.f height check #39 -> #38 (message text "Not a BMP file").
- 026 WITH-CLEANUP now really restores a saved DEPTH (NEEDS DEPTH).
- 057: new CODE DOT-START (sets ORG, `jp` placeholder patched after
  .HELLO); tutorial/CLAUDE.md sec.17 documents the new bug variant.
- 044 MOUSE-DRAW: pen flag from down/up events, -32 offset, COORD-CHECK,
  exit with `LAYER12 1 .PAPER`.

053 "S0 reads 0": NOT a tutorial bug. Probes after every section show
S0 = 54008 until the end of the file and after it. What breaks is the
first command typed after the INCLUDE, which loses its first character
(`SP@ U.` became `P@ U.` and printed 255; `S0 @ U.` printed 0): the
section 12 session runs TEST -> PAUSE -> 1FRAME, 240 HALTs, and the
headless emulator delivers queued keys on HALT. Emulator/driver artifact
of queueing input ahead of time; not reproducible by a user typing.
Confirmed: with the TEST line commented out, the command after the
INCLUDE survives intact (S0 = 54008).

Verified in the headless emulator (2026-09-24): 013 `42 DESCRIBE` ->
"number 42", stack clean; 026 `4 TRY-SQRT .` -> 2, `-4 TRY-SQRT .` ->
error + 0, `10 2 WITH-CLEANUP .` -> 5, `10 0 WITH-CLEANUP .` -> 0, stack
clean; 007 `5 .DOWN` -> 5 4 3 2 1; 057 loads, `GREETING 1+ TESTER`
prints Hello, World!, byte at ORG = $C3 and its operand = relocated
.HELLO ($2039). Graphics/sprites/mouse/copper/palette/UART changes
still need CSpect (section 6).
