## Possible improvements and Known Bugs

> Resolved entries are moved to TODO-DONE.md.

# F_GETLINE writes outside its buffer unless used as F_INCLUDE uses it
**2026-10-16**
Found while writing chapter 20 of the BASIC-to-vForth guide; all three
reproduced on the headless emulator (`help/rnd.txt`, lines ending in LF).
`F_GETLINE ( a m fh -- n )` reads `m` bytes at `a+1`, finds the end of line
with `10 ENCLOSE` and `13 ENCLOSE` starting from `a`, then moves the line
down to `a` and blanks the rest. `F_INCLUDE` never trips on it, because it
blanks BLOCK 1 before each call and passes `a+1` and `m-2`; any other
caller does.
- **At the end of the file it writes the byte before the buffer.** In
  the `Else` branch n is 0, and `r@ + 1-` gives `a-1` as start of the
  `BLANK`. With a buffer made by `CREATE LINEBUF 82 ALLOT`, the byte
  before is part of `LINEBUF` itself: after the loop that reads the whole
  file, the next use of `LINEBUF` crashed and the dictionary was lost.
  A guard byte before the buffer went from 0 to 32.
- **The old byte at `a` changes the result.** `ENCLOSE` starts at `a`,
  where the new data is not. A 0 there (a buffer just `ERASE`d) makes it
  return 1 and split the first line (1 + 16 instead of 17); a 10 there is
  skipped as a leading delimiter.
- **No end of line within the bytes read: `ENCLOSE` goes on past them.**
  A line longer than `m`, or a last line without its end: n comes from
  whatever memory follows. With `B 10` on a 16-character line n exceeded
  `m`, `BLANK` got a negative length and the emulator hung; a last line
  `xyz` without LF gave 79. `F_INCLUDE` has the same limit for lines over
  about 508 characters.
Proposed fix, in `L3.asm` (DOES and DOT) and `src/F18e.f`; tried on the
headless emulator as `F_GETLINE2`, defined at the prompt with the same
logic. Three changes:
1. **NUL sentinel after the bytes read.** Read at most `m-2` bytes, not
   `m`, and store a 0 right after them. `ENCLOSE` always stops at a NUL
   (its comment in the core: "does not go beyond a 'nul'"), so it stays
   inside the buffer for a line longer than the maximum and for a last
   line without its end.
2. **A `BL` at `a` before the two `ENCLOSE`.** The result no longer
   depends on the byte left there (a 0 gave n = 1, a 10 was skipped).
3. **Tail rewritten.** The `BLANK` starts at `a + max(n-1,0)`, not at
   `a+n-1` (which was `a-1` for n = 0); the final 0 is one byte at
   `a+m-1`, not a cell.
Related detail: when the line is cut, n is k+1 (k = bytes read), so "n-1
is the text length" still holds, but `F_SEEK` must advance by
`min(n, k)`, or it skips a character never read.

Forth form (`src/F18e.f` style):

```forth
.( F_GETLINE )
\ Given an open filehandle read at most m-2 characters to get next line
\ terminated with $0D or $0A.
\ n is the length of line plus one (the terminator), 0 at end of file.
\ The buffer at a must be m bytes long: the line is left at a, blank
\ padded, with a trailing 0x00 at its m-th byte.
decimal
: f_getline ( a m fh -- n )
    >r tuck                                     \ m a m         R: fh
    r@ f_fgetpos [ 35 ] Literal ?error          \ m a m  d
    2swap                                       \ m  d  a m
    over 1+ swap 2-                             \ m  d  a a+1 m-2
    r@ f_read [ 35 ] Literal ?error             \ m  d  a k
    ?dup If \ at least 1 chr was read           \ m  d  a k
        2dup + 1+ 0 swap c!                     \ nul sentinel after data
        >r                                      \ m  d  a       R: fh k
        bl over c!                              \ a non-delimiter at a
        [ 10 ] Literal enclose                  \ m  d  a n1 b n3
        drop nip swap                           \ m  d  b a
        [ 13 ] Literal enclose                  \ m  d  b a n1 c n3
        drop nip rot                            \ m  d  a c b
        min                                     \ m  d  a n
        dup span !
        dup r> min >r                           \ m  d  a n     R: fh u
        2swap r>                                \ m a n  d  u   R: fh
        0 d+                                    \ m a n d+u
        r> f_seek [ 36 ] Literal ?error         \ m a n
    Else                                        \ m  d  a
        r> 2swap                                \ m a fh  d
        2drop drop
        0                                       \ m a 0
    Then
    >r                                          \ m a           R: n
    dup 1+ over r@ cmove                        \ m a
    2dup + 1- 0 swap c!                         \ m a      0 at a+m-1
    r@ 1- 0 max                                 \ m a t    t text length
    tuck + -rot - 1-                            \ a+t m-t-1
    blank
    r>                                          \ n
;
```

Assembler form (`L3.asm`, DOES and DOT); the `Else` branch is unchanged,
the start, the `If` branch and the tail change:

```
                dw      TWO_SWAP, OVER          // 2swap over       ( m d a m a )
                dw      ONE_PLUS, SWAP          // 1+ swap          ( m d a a+1 m )
                dw      TWO_MINUS               // 2-               ( m d a a+1 m-2 )
                dw      R_OP, F_READ            // r f_read         ( m d a k f )
                dw      LIT, 35, QERROR         // 35 ?error        ( m d a k )
                dw      QDUP                    // ?dup
                dw      ZBRANCH
                dw      FGetline_Else - $
                dw          TWO_DUP, PLUS       //      2dup +           ( m d a k a+k )
                dw          ONE_PLUS            //      1+               ( m d a k a+k+1 )
                dw          ZERO, SWAP, CSTORE  //      0 swap c!        ( m d a k )
                dw          TO_R                //      >r               ( m d a )        \ fh k
                dw          BL, OVER, CSTORE    //      bl over c!       ( m d a )
                dw          LIT, 10, ENCLOSE    //      10 enclose       ( m d a x b x )
                dw          DROP, NIP           //      drop nip         ( m d a b )
                dw          SWAP                //      swap             ( m d b a )
                dw          LIT, 13, ENCLOSE    //      13 enclose       ( m d b a x c x )
                dw          DROP, NIP           //      drop nip         ( m d b a c )
                dw          ROT, MIN            //      rot min          ( m d a n )
                dw          DUP, SPAN, STORE    //      dup span !       ( m d a n )
                dw          DUP, R_TO, MIN      //      dup r> min       ( m d a n u )    \ fh
                dw          TO_R                //      >r               ( m d a n )      \ fh u
                dw          TWO_SWAP, R_TO      //      2swap r>         ( m a n d u )    \ fh
                dw          ZERO, DPLUS         //      0 d+             ( m a n d+u )
                dw          R_TO, F_SEEK        //      r> f_seek        ( m a n f )
                dw          LIT, 36, QERROR     //      36 ?error        ( m a n )
                dw      BRANCH
                dw      FGetline_Endif - $
FGetline_Else:
                ...                             // unchanged
FGetline_Endif:
                dw      TO_R                    // >r                   ( m a )      \ n
                dw      DUP, ONE_PLUS, OVER     // dup 1+ over          ( m a a+1 a )
                dw      R_OP, CMOVE             // r cmove              ( m a )
                dw      TWO_DUP, PLUS           // 2dup +               ( m a a+m )
                dw      ONE_SUBTRACT            // 1-                   ( m a a+m-1 )
                dw      ZERO, SWAP, CSTORE      // 0 swap c!            ( m a )
                dw      R_OP, ONE_SUBTRACT      // r 1-                 ( m a n-1 )
                dw      ZERO, MAX               // 0 max                ( m a t )
                dw      TUCK, PLUS, DASH_ROT    // tuck + -rot          ( a+t m t )
                dw      SUBTRACT, ONE_SUBTRACT  // - 1-                 ( a+t m-t-1 )
                dw      BLANK                   // blank
                dw      R_TO                    // r>                   ( n )
                dw      EXIT                    // ;
```

Tried on the headless emulator (2026-10-16):

| Case | Today | Proposed |
|---|---|---|
| `help/rnd.txt`, buffer just `ERASE`d | 1 16 1 39 ... (first line split) | 17 1 39 38 38 31 1 26 0 0 |
| bytes before and after the buffer, after the end of file | the one before blanked (0 -> 32) | both untouched |
| 16-character line, buffer of 10 | negative length, emulator hung | 9, 9, 1: two pieces of 8 plus the end, nothing lost, next buffer untouched |
| `abc` LF `xyz`, no final LF | 4, then 79 | 4, 4, 0 |

Effects:
- `F_INCLUDE` needs no change: it still passes `a+1` and `n-2` on BLOCK
  1, but now reads two bytes less per line, so the practical limit drops
  by two characters, to about 506 (the source rule is 80).
- CRLF is not addressed: a CRLF file still reads as an empty line after
  each line, because the LF is read as a line of its own. A behaviour,
  not a memory fault; it can be handled separately.
- About 13 cells (some 26 bytes) more in the dictionary.
- Then: new build (`/bump-build`), the same change in DOT and in
  `src/F18e.f`, `/check-f18e` on CSpect, and an `INCLUDE` run
  (`test/BLOCK1-PIN-TESTS.f`). Until then `help/f_getline.txt` warns, and
  chapter 20 of the guide reads lines with its own `GET-LINE` built on
  `F_READ`; once fixed, the chapter could go back to `F_GETLINE`.

# Headless emulator: run the 48K ROM FP calculator (option --rom)
**2026-10-16**
Idea, not started; feasibility already proved. With a real 48K ROM image
copied to `$0000` the FP calculator runs as is: `NEEDS FLOATING`,
`FLOATING`, `F.`, `F/` and the reading of `1E3`/`1.E3` all worked on the
first try (recipe in `lib/CLAUDE.md`, "Testing FLOATING in the headless
emulator"). Running the real ROM, not a Python rewrite of the calculator
(a stack machine of some 60 operations on 5-byte numbers: much work, and
never bit-exact in its rounding as the original is).
Points to take care of:
- **ROM errors**: the calculator reports an error (e.g. `Number too big`
  on overflow) with `RST $08` + error code. Today the emulator traps every
  `RST $08` as a NextZXOS call and would read the code as a function: when
  `RST $08` comes from the ROM (PC below `$4000`) it must be reported as a
  BASIC error instead.
- **System variables**: `MEM` (`$5C68`) = `$5C92`, `STKBOT` (`$5C63`) and
  `STKEND` (`$5C65`) = `$5D00`, `IY` = `$5C3A` (already set); the MEMBOT
  area must not overlap anything else.
- **Keep the `RET` stubs** of `install_rom_stubs` (`CHAN-OPEN` `$1601`,
  `CL-ALL` `$0DAF`) after copying the ROM: run for real they would need
  the BASIC channels, which are not modelled.
- **Licence**: Amstrad allows distributing the ROM with emulators, but the
  repo is public (MIT): do not commit it. An option `--rom PATH` (or an
  environment variable) in `emu/emulator.py`/`emu/repl.py`, with the FP
  tests skipped when it is absent. Local copies: `D:\zx\Fuse\roms\48.rom`,
  `D:\zx\Next\SD\machines\next\48.rom`.
- **Speed**: `FLN`, `FSIN`, `F**` run thousands of ROM instructions in the
  Python emulator; acceptable in the trial.
- **DOES only**: the DOT crash of FLOATING (entry below) depends on the ROM
  paging of a dot-command, not modelled, and is not reproduced this way.
Gains: `test/FLOATING-TESTS.f` on the emulator; the floating snippets of
the BASIC-to-vForth guide (chapters 6 and 9) moved from `<!-- no-test -->`
to a marker such as `<!-- needs-rom -->` in `emu/test_basic_guide.py`;
the `F.` powers-of-ten suspicion (entry below) checkable at once. With the
ROM present `BEEPER` (`$03B5`) would also be available for the PIP click
entry, though without a speaker it is only `OUT $FE` loops.

# FLOATING crashes the DOT variant (.vforth)
**2026-10-16**
Bug reported by the author: `NEEDS FLOATING` (`lib/floating.f`) works on
the DOES variant but crashes the dot-command `.vforth`. Not yet analysed
on the machine; the headless emulator cannot help, since it has no ROM
calculator and runs only the DOES binaries.
Likely cause, from the sources: `lib/FP-INTERFACE.f`, loaded by
`floating.f`, reaches ROM 3 directly in three places, which is right only
when ROM 3 is paged in at `$0000`, as it is in the DOES variant:
- `FOP`: `RST $28` (`$EF`), the FP calculator, followed by two inline
  bytes (the operation, patched at each call, and `$38` end-calc);
- `>W`: `CALL $2AB6` (STK-STORE);
- `W>`: `CALL $2BF1` (STK-FETCH).
In a dot-command the low 16K is the DivMMC/NextZXOS ROM, so `RST $28` and
those `CALL`s land in the wrong code. `FP-INIT` already runs some of them
at load time (`PI` and `1/2` are computed between `[` and `]`), so the
crash may happen during `NEEDS FLOATING`, before `FLOATING` is even typed.
`lib/bleep.f` shows how the DOT case is handled for a plain call: test
`0 +ORIGIN 2000 -` and compile `RST $18` + address (`$DF`) instead of
`CALL` (`$CD`). That fixes `>W` and `W>`. `FOP` is harder: through
`RST $18` the calculator would look for its inline bytes after the
`RST $18` handler's return address, not after our code. Idea to try: put
`RST $28 / op / $38 / RET` in a small routine in the dictionary (main RAM,
visible in both variants) and enter it through a ROM 3 `JP (HL)`, e.g.
`LD HL,routine` then `RST $18` / `DW $162C` (CALL-JUMP), so that ROM 3
stays paged while the calculator runs.
To do: reproduce on CSpect with `.vforth` and see whether it crashes at
load or at the first operation; fix `FP-INTERFACE.f` choosing the code at
load time like `bleep.f`; check that `NO-FLOATING` and the `COLD`
redefinition behave in DOT; then the floating parts of the tutorials and of
chapter 9 of the BASIC-to-vForth guide can be tried on both variants.
Other modules calling ROM 3 directly may share the bug: worth a grep of
`lib/` and `inc/` for `RST $28`, `$EF C,` and `$CD C,` with a ROM address.

# Headless emulator: serve ROM BEEPER, so the PIP key click can be heard
**2026-10-16**
Idea, not started. Companion of the next entry (KEY honouring PIP). Today
`emu/emulator.py` (`install_rom_stubs`) puts a bare `RET` on every ROM
entry point the core calls, and `_port_out` in `emu/z80_instructions.py`
ignores writes to the ULA port `$FE`: the emulator is silent and cannot
show whether a click happens, nor how long it is.
Proposal: instead of a `RET` stub at `BEEPER` (`$03B5`), a Python handler
(the same trap style as `handle_nextzxos_call`) that reads `DE` (cycles)
and `HL` (period, `$00C8` for the key click) and either logs the event
(enough for a regression test: "one click per key, length = PIP") or
synthesises the square wave (e.g. `winsound`/a WAV buffer). Optionally, a
port `$FE` bit 4 (speaker) trace for code that toggles the speaker by
itself -- which is exactly what the old quick'n'dirty click did: see the
commented-out `CLICK` in `src/F18e.f` (around line 1424) and in
`project/vForth18_DOES/source/L0.asm` (`New_Def CLICK`): `BORDCR` border
colour OR `$18`, `OUT ($FE)`, a 256-turn `DJNZ`, `XOR $18`, `OUT ($FE)` --
a single fixed "pop", roughly what BASIC makes with PIP = 0.
Usefulness: the handler must exist anyway as soon as `KEY` calls `$03B5`
(otherwise every key typed in `emu/repl.py` derails into low memory), so
doing it "properly" costs little more than the stub and makes the click
testable without CSpect. `BEEP`/`lib/bleep.f` would benefit from the same
handler.

# Manipulating .MDR cartridge images on the Next itself
**2026-10-16**
Idea, not started. `mdr.pl` (Perl, outside this repo: `\zx\mdr\mdr.pl`,
rev. 2022-12-01, ~1400 lines; used by `util/mdr2txt.bat`) already does
everything on the PC: catalogue (`-l`, free/bad sectors), `get=`/`put=`,
`dump`/`text`, rename/copy/erase, label, autorun on/off, bad-sector fix,
`.MDR` <-> `.TAP`. It would be nice to have the same on the Next, as
natively as possible, e.g. to recover old vForth `!Blocks` screens from
`.MDR` images (`M2.mdr`..`M8.mdr`, `Forth1.mdr`, ...) straight onto the SD.
Routes to evaluate:
- **Raspberry Pi Zero accelerator**: the Pi runs Linux with Perl, so
  `mdr.pl` could run unchanged there; the open question is the transport
  (UART between Next and Pi, the NextPi `.pisend`/`.pi*` dot-commands, and
  how files on the Next SD reach the Pi and back). Lowest porting cost.
- **A vForth `lib/` module** (e.g. `lib/MDR.f`): the `.MDR` format is
  simple (254 sectors of 543 bytes: header + record + data + checksum, plus
  the write-protect byte), so catalogue and `get` are within reach in Forth
  with `F_OPEN`/`F_READ`/`F_SEEK`; a sector buffer in heap/MMU7 page. Fully
  native, but a rewrite.
- A NextZXOS dot-command in Z80: most native, most work.
First step: decide the minimal feature set (probably catalogue + get, i.e.
read-only) and check what the NextPi distribution offers today.

# KEY could click like BASIC, honouring PIP (23609)
**2026-10-15**
Proposal, not started. Found while writing chapter 18 of the BASIC-to-vForth
guide: BASIC makes a key click whose length is the system variable PIP
(23609), so `POKE 23609,n` changes it. vForth's `KEY` makes no click at all
(the `CLICK` code in `L0.asm` near `KEY` is commented out) and never reads
PIP, so the guide says that `POKE 23609` has no effect in vForth.
Idea: in `KEY` (`project/vForth18_DOES/source/L0.asm`, `New_Def KEY`), after
`res 5,(iy+1)`, do what the ROM does when it reads a key: call `BEEPER`
(`$03B5`) with `DE` = PIP and `HL` = `$00C8`. Estimated 25-35 bytes of Z80:
- save `BC` (already done), `DE` (return stack) and `IX`, which `BEEPER`
  uses for its timing loop (`lib/bleep.f` does the same);
- `BEEPER` is timed for 3.5 MHz: drop the speed (NextReg 7) for the click
  and restore it, as `BEEP` does, or the click is 8 times shorter and
  higher at 28 MHz;
- DOT variant: `rst $18` instead of `call` (`lib/bleep.f` already picks
  one of the two).
`ACCEPT` calls `KEY` directly, so a `KEY` redefined in `inc/` would not
click at the prompt: it has to be done in the core (or `KEY` made
vectored, a larger change).
To decide first: the default behaviour. BASIC starts with PIP = 0, which
is a short click, not silence: copied as is, vForth would start clicking
on every key for everybody. Alternative: click only when PIP is not zero
(2-3 bytes more), so silence stays the default and `POKE 23609,n` turns
the click on.
Costs beyond the bytes: a new build (`/bump-build`, DOES and DOT,
`src/F18e.f` aligned and `/check-f18e` on CSpect, `/regen-doc-dict-structure`,
the boot address table in `CLAUDE.md`); a `RET` stub for `$03B5` in
`install_rom_stubs` of the headless emulator, or the first key typed in
`emu/repl.py` and in every test derails into low memory; with a large PIP
the click slows typing down. Best done together with the next core change,
not as a build of its own. When done, update chapter 18 of the guide
(`doc/basic-to-vforth/18-sound-and-music.md`, "The keyboard does not
click" and "No equivalent").


# BEEP misbehaves at the edges of its range, and from pitch 48 up
**2026-10-15**
Found while writing chapter 18 of the BASIC-to-vForth guide; measured on
the headless emulator (the arithmetic only: the sound goes through the ROM
and is not emulated). BASIC's `BEEP` stops with `B Integer out of range`
when it cannot play a pitch; `lib/bleep.f` checks nothing, and three
things go wrong silently.
- **Pitch 48 to 57: the note lasts seconds instead of the duration
  asked.** `BLEEP-CALC` computes the number of cycles as `R@ 8000 */`,
  i.e. ms * hz8 / 8000 with *signed* arithmetic. From pitch 48 (C, 4186
  Hz) `hz8` is above 32767 and `*/` takes it as negative: `500 48
  BEEP-PITCH BLEEP-CALC DROP U.` gives 63533 cycles, about 15 seconds,
  where pitch 47 gives the right 1975 (0.5 s at 3951 Hz). At pitch 57 it
  is 64960 cycles, about 9 seconds. So the useful range today is -27 to
  47, not up to 57.
  Proposed fix: unsigned arithmetic, `R@ UM* 8000 UM/MOD NIP` in place of
  `R@ 8000 */`. The cycle count must still fit in 16 bits: ms * Hz / 1000
  <= 65535, i.e. about 9 seconds at the top pitch, more below; BASIC
  limits the duration to 10 seconds.
- **Above pitch 57 the pitch folds back.** `BEEP-PITCH` starts from
  `57 SWAP - ABS`, so 58 gives the frequency of 56, 69 that of 45:
  `58 BEEP-PITCH 56 BEEP-PITCH =` is true. BASIC goes on rising (to about
  69) and then gives the error.
- **Below pitch -27 the note comes out too high.** -27 is the A at 55 Hz
  (`hz8` 440). One step lower `hz8` is 415 and `28000.000 hz8 UM/MOD`
  overflows 16 bits: `500 415 BLEEP-CALC` leaves 8162 as timing value
  where 8404 is right, and lower pitches are worse.
To do: fix the signed `*/`; then either check the pitch (-27 to 57, or a
wider table) and the duration with `?ERROR`, or state the limits in
`help/beep.txt`, `help/bleep.txt` and in the header of `lib/bleep.f`. Hear
it on CSpect or the real machine before and after (`500 47 BEEP` and
`500 48 BEEP` should last the same). Then correct chapter 18 of the guide,
which today gives the useful range as -27 to 47 and explains why.
Related: the entry on `lib/` help coverage below already notes that
tutorial 033 and the header of `lib/bleep.f` give the two `BLEEP`
arguments in the wrong order.

# +" corrupted the string it extended
**2026-10-13**
Found while writing chapter 7 of the BASIC-to-vForth guide: on the headless
emulator `H" abc" +" def" FAR COUNT TYPE` printed `bcjdef`. Two errors in
`inc/+~.f`: the new text was copied at `HP@`, i.e. four bytes past the end
of the string (after the zero cell and the back pointer that `HEAP` lays
down after every block), and the last line stored `HP` at `ha` -- on the
length byte and the first character -- instead of in the forward pointer at
`ha - 2`.

Fixed the same day: `+"` now appends right after the old text, moves `HP`
by the number of characters added, updates the length byte and lays the
tail (zero cell, back pointer) and the forward pointer down again. Checked
on the headless emulator only: `H" abc" +" def"` gives `abcdef`, length 6;
a second `+"  ghi jkl"` gives `abcdef ghi jkl`, length 14; after each step
the forward pointer equals `HP@` and the back pointer at `HP@ - 2` points
to the block; `H"` and `S"` used afterwards still work.

Still open:
- **Author's check on CSpect or the real machine**, then move this entry to
  TODO-DONE.md.
- `+"` works only on the **last** block created on the heap and checks
  neither the 8K page boundary nor the 255-character limit; it has no test
  in `test/`, and `help/+~.txt` says none of this.
- `+C` and the empty text `+" "` have entries of their own, below.


# +C leaves the tail of its heap block behind
**2026-10-13**
Found by reading `inc/+c.f` while fixing `+"` (entry above); **not yet
reproduced**, because today it has no visible effect. A block made by
`HEAP` is: forward pointer, data, a zero cell, a back pointer, and `HP`
points just after it. `+C` appends one character to the counted string at
`ha`: it adds 1 to the forward pointer at `ha - 2`, to the length byte and
to `HP`, and stores the character -- but it does not move the tail. So
after one `+C`:
- the new character lies on the first byte of the zero cell;
- the back pointer is still where it was, one byte before the place
  `HP@ - 2` where it should be, and the byte at `HP@ - 1` is whatever was
  there;
- the forward pointer and `HP` are right, so the next `HEAP` starts in
  the right place and the string itself reads back correctly.
Nothing reads the back pointer or the zero cell today (only `HEAP` writes
them), hence no symptom. It becomes a real bug the day something walks
the list backwards or relies on the zero terminator after a string.
To do: lay the tail down again after the store, as `+"` now does
(`0` at `HP@ - 4`, `ha - 2` at `HP@ - 2`); add the page-boundary and
255-character checks, or document their absence; write `help/+c.txt`
(there is none) and a test covering `H"`, `+"` and `+C` together. Like
`+"`, `+C` is valid only on the last block created.


# Empty text after S" and +" takes the rest of the line
**2026-10-13**
Seen on the headless emulator while writing chapters 7 and 8 of the
BASIC-to-vForth guide; to be looked at again before deciding it is a bug.
- `: T6  S" " VAL . ;` does not define `T6`: the next line answers
  `T6? is undefined.` The text of `S"` was not empty, it ran on past the
  closing quote.
- `+" " FAR COUNT TYPE` printed nothing: the words after the quote were
  appended to the string instead of being executed.
Likely cause, from the sources and not yet proved: both parse with
`[CHAR] " WORD` (`S"` through `H"`), and `WORD` skips leading delimiters.
In `S" "` the character after the blank that ends the name is the closing
quote itself, so it is skipped as a leading delimiter and the text runs to
the next quote, or to the end of the line.
To check, on the emulator and on the machine:
- that this is indeed what happens (dump the string that was stored);
- which other words share it: `."`, `.(`, `,"`, `H"`, `C"`, `PAD"`,
  `ABORT"`, each with an empty text;
- what the core `."` does, since it is the reference for the others.
Then decide: either parse with a word that does not skip leading
delimiters (the standard `PARSE` behaviour), so that an empty text is an
empty string, or keep it and say so in the help pages. For now the guide
warns about it (chapter 7: the empty string is `0 A$ C!`, not `S" "`).


# F. may print a two-digit mantissa at exact powers of ten (suspected)
**2026-10-13**
A suspicion from reading the code, **never observed**: the headless
emulator has no ROM calculator, so `lib/floating.f` cannot be run there.
`F>PAD` (the word behind `F.` and `F.R`) gets the decimal exponent as

    FLN 10 0 FLN F/ F>D

i.e. the logarithm in base 10, truncated towards zero. For an exact power
of ten the quotient of the two logarithms may come out a hair below the
whole number (2.9999999 for 1000): `F>D` then gives 2 instead of 3, and
the mantissa is scaled by 10^2, so `1000.0 F.` would print `10.0000e2`
instead of `1.0000e3`. The value shown would still be right; only the
form would be off. The same could happen just below a power of ten, the
other way round, if the mantissa rounds up to `10.0000` after the scaling
(e.g. 9.99996 with 4 places).
To do: on CSpect or the real machine print `F.` of 10.0, 100.0, 1000.0,
0.1, 0.01, 0.001 and of 9.99996; if any comes out wrong, correct the
exponent after the scaling (when the mantissa is >= 10 divide it by 10
and add 1 to the exponent; when it is < 1 and not zero do the opposite)
instead of trusting the logarithm. Note also that for numbers below 1
`F>D` truncates towards zero, so 0.5 prints as `0.5000e0` and 0.05 as
`0.5000e-1`, not normalised: decide whether that is wanted. Related:
`planners/FLOATING-5BYTE-PLAN.md` (option A, rounding in `W>`, applied on
2026-10-12 and not yet tried on CSpect) may change the outcome.


# VS Code extension: colorize known words in the help files too
**2026-10-05**
A small enhancement wished for the VS Code extension: highlight/colorize the
words it already knows (core and lib) also inside the `help/*.txt` files, not
only in the Forth sources. The help texts are full of word names (stack
effects, "See also" lines, examples), so the same colouring would make them
much easier to read. If possible they should also become navigable inside
VS Code itself (e.g. go to definition / follow the word to its source or to
its own help file). Mind the FAT filename mapping (`help/` names are mapped,
the words inside the text are the real Forth names).

# ?VOCAB is still incomplete
**2026-06-01**, revised **2026-10-04**
`.VOCAB` is fixed (build 2026-09-26, see TODO-DONE.md). `?VOCAB`
(`inc/^vocab.f`) now prints the right Current and Context lines, but:
- it ends with `VOC-LINK @` and nothing consumes it: one stray cell is left
  on the stack at every call, and the "Voc-Link" line prints no value;
- the `BEGIN ... UNTIL` walk of the vocabulary chain is still commented out.
Checked on the headless emulator only; the original failure was seen on real
hardware and has not been re-tested there. The `.VOCAB` examples in section 6
of `tutorial/018-vocabularies.f` are still commented out.


# DMA: at what speed does the transfer actually run?
**2026-10-04**
Left open when tutorial 054 was closed (see TODO-DONE.md). On a real Next
`32 STRIPES` works with the CPU at 28 MHz (`tutorial/054-stripes.png`), but
the transfer to port $FE looks as if the DMA ran at 3.5 MHz. Tests are needed
to settle the question: read the CPU speed with `7 REG@`, then run
`32 STRIPES` after `0 SPEED!` (3.5 MHz) and after `3 SPEED!` (28 MHz) and
compare the width of the border bands in the two captures. If the bands do
not change, the DMA rate does not follow the CPU speed. The headless emulator
does not model the zxnDMA controller, so this needs real hardware (or
CSpect, as a second opinion). Record the outcome in the status note at the
bottom of `tutorial/054-dma.f`.


# Several lib/ modules have little to no per-word help/ coverage
**2026-08-20**, revised **2026-10-04**
Found while auditing `help/` for FAT-filename-mapped word names (every
`inc/` word with a mapped char now has its `help/*.txt`, plus `EXEC:`,
`ASK-Y/N`, `BMP-LOAD"`). The gap turned out to be broader than the mapped
names themselves: `lib/floating.f`, `lib/fixed88.f`, `lib/complex.f`,
`lib/testing.f`, `lib/RPi0.f`, `lib/LED.f`, `lib/ZAP.f`/`ZAP~.f`,
`lib/bleep.f`, `lib/mouse-ay-tester.f`, `lib/AFXFRAME-forth.f`,
`lib/layer3.f` and `lib/MOUSE.f` have little or no per-word `help/` entries
-- not even for their plain-named words (e.g. `F+`, `F-`, `FDUP`, `T{`,
`}T` have none; only `help/floating.txt` documents the module as a whole).
Core words are fully covered: checked on 2026-10-04 against the RENAME
block of `src/F18e.f` (334 names), the `WORDS` listing at boot and the
definition macros of `L0.asm`-`L3.asm`; no core word lacks a page. The gap
is outside the core: `lib/` is measured below, `inc/` was not re-audited.

First pass on 2026-10-04: 65 pages written for the words used in the
compiled code of the tutorials that had none (MOUSE, RPi0/UART, AFXFRAME,
GRAPHICS, AY, beeper, BMP-LOAD, Copper, FLOATING, INTERRUPTS, LAYER3, the
`LAYERx`/`MMUn!`/`MS`/`UNLINK` words of `inc/`, ASSEMBLER). They await the
author's validation. Left out on purpose: the assembler mnemonics and
register names of tutorials 027 and 057 (about 35), and words that appear
only inside tutorial comments.
Found while writing `help/bleep.txt`: tutorial 033 and the header comment of
`lib/bleep.f` give the two `BLEEP` arguments in the opposite order to what
the code consumes (`BLEEP-CALC` leaves cycles below, pitch on top) -- to fix.

Audit of 2026-10-04 after that pass, all of `lib/*.f`: about 880 names
defined, 147 with a `help/` page of their own (74 before the pass).
Counted: every name defined with `:`, `CODE`, `CREATE`, `VARIABLE`,
`CONSTANT`, `VALUE` and the like, looked up as `help/<name>.txt` through the
FAT mapping. The figure overstates the work (constants and private helpers
are counted, and so are the several copies of AFXFRAME and GRAPHICS) and
misses names created by a module's own defining words (`F+`, `F-`, `F*` in
`floating.f`; the `TILE-*` modes of `layer3.f`, which do have pages).
Figures are "with help / defined"; "page" = a `help/<module>.txt` exists.

    Modules named above
      floating.f          7/40  page      LED.f               1/69
      fixed88.f           0/50            ZAP.f               1/19
      complex.f           0/19            ZAP~.f              0/10
      testing.f           1/36            bleep.f             3/6   page
      RPi0.f              8/42  page      mouse-ay-tester.f   0/7
      MOUSE.f             7/33  page      AFXFRAME-forth.f    2/7
      layer3.f            0/7   page (+5 TILE-* pages)

    Not named above, still no page at all
      SPRITE.f            0/18            TILE80.f            0/17
      UART-SYS.f          0/15            udg+.f              0/7
      TUTORIAL.f          0/6             mouse-tester.f      0/4
      FP-INTERFACE.f      0/3             LAYER24-GRAPHICS.f  0/3
      bsearch.f           0/3             locate.f            0/2
      IDE_PATH.f          0/2             TILE80-setup.f      0/2
      heap.f  hide-word.f  set-fence.f  used-by.f             0/1 each

    Module page plus a few words
      GRAPHICS.f         16/91  page      GRAPHICS-COMMON.f  15/56  page
      edit.f              1/32  page      see.f               2/20  page
      INTERRUPTS.f        4/18  page      DIR.f               1/14  page
      PERSISTENCE.f       1/17            editor.f            1/13
      AY.f                6/14  page      copper.f            6/12  page
      afxplay.f           6/13            bmp-load.f          3/9   page

    Partly covered
      DMA.f              16/43  page  (missing: DMA-CMD-*, DMA-WR* constants
                                       and the parenthesised helpers)
      LOCALS.f            6/32  page  (missing: private helpers only)
      needs.f             9/11  page
      assembler.f         3/3   page  (complete)

Many of the missing names are internal and need no page (`DEB-*` in `see.f`,
`LED-*`, `(LOC-*)`, port constants). The real work is deciding, module by
module, which words are public.

Documenting just the FAT-mapped subset of each module (`F<`, `F>`, `FP*`,
`C*`, `AFX>AY`, `TILE-MODE:`, `ZAP"`, ...) would be incoherent with their
undocumented plain-named siblings in the same file, so none of those were
added -- this needs a deliberate per-module documentation pass instead.
`?--`/`?}` in `lib/LOCALS.f` are the one confirmed exception: private
parsing helpers, intentionally undocumented like `(LOC-BIND)`/`LOC-PFA`,
not part of this gap.


# chomp-chomp: write a "Next-like" capstone tutorial
**2026-08-22**, revised **2026-10-04**
A Next-like rewrite of `demo/chomp-chomp` (currently a portable
sprite/tilemap game, see tutorial 059 for how it ships via ZAP) as a
before/after capstone tutorial, using the hardware-accelerated primitives
introduced across the 030-059 band (hardware sprites -- tutorial 053,
tilemap -- tutorial 058) in place of the original software model.
The rewrite is under way in `demo/chomp-chomp-next/`, following
`planners/CHOMP-CHOMP-NEXT-PLAN.md`: Stage 1 (AY sound, 2026-08-27) and
Stage 2 (hardware sprites, 2026-09-01) are implemented and both still await
CSpect confirmation; Stages 3-5 (palette effects, interrupt pacing, tilemap
maze) are not started. The tutorial itself is not started. Note that
`demo/chomp-chomp-next/README.txt` still points at the plan's old location,
`prompts/CHOMP-CHOMP-NEXT-PLAN.md`.


# ASK-Y/N as a reusable NEEDS word
**2026-09-23**
Possible evolution, deliberately not implemented: the boot path is not worth
the risk for now. `ASK-Y/N` lives only inside `lib/AUTOEXEC.f`, behind
`MARKER FORGET-THIS-TASK-3`, and forgets itself before `QUIT`; so
`help/ask-y%n.txt` documents a word the user can never call.
Idea: a new `inc/ask-y%n.f` returning a flag instead of quitting, Y default:

    : ASK-Y/N  ( -- f )  \ true unless N/n
        ." (Y/n) "  CURS KEY DUP EMIT  UPPER [CHAR] N - 0= 0= ;

and in `lib/AUTOEXEC.f` a small local word that still performs the `QUIT`
(no conditional interpretation available):

    MARKER FORGET-THIS-TASK-3
    NEEDS ASK-Y/N
    : ?UTILITIES  ." Autoexec asks: Do you wish to load utilities ? "
        ASK-Y/N  FORGET-THIS-TASK-3  0= IF ." ok " QUIT THEN ;
    CR ?UTILITIES

`lib/AUTOEXEC-DOT.f` needs no change (it only does `11 LOAD`, which includes
the same `lib/autoexec.f`).
Benefits: `help/ask-y%n.txt` becomes a regular "Available after NEEDS" entry;
a reusable prompt (tutorials 016 `YES?` and 035 `YES-OR-NO` each roll their
own). Costs: one more file open on every boot, on the most delicate path;
two files to maintain instead of one. No dictionary cost, since `NEEDS`
follows the MARKER and the word is forgotten with it.
Semantics to settle: autoexec treats any key but N as yes, the tutorials loop
until Y or N. Verify on the headless emulator (`emu/repl.py` smoke test goes
through ASK-Y/N answering `n`) and on CSpect for both DOES and DOT.
