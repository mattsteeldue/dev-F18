# EVALUATE bug analysis -- text after EVALUATE lost on the same source line

Date: 2026-06-11
Status: analysis + proposed fix; inc/evaluate.f NOT yet modified.
TODO.md entry: "EVALUATE little bug" (2026-05-31).

## 1. Symptom

When a `.f` file loaded via `INCLUDE` / `NEEDS` executes `EVALUATE` and more
text follows on the same source line, that text is silently skipped (or
parsed mid-token, producing garbage). Putting `EVALUATE` on a line of its
own, with nothing after it, works. This is why tutorial/021-evaluate.f had
to move `EVALUATE` to its own line, and why the failure worsens with long
("complex") strings before it.

The bug only affects `EVALUATE` executed while a file include is the active
input source. Keyboard, `LOAD` (screen) and compiled-word usage are fine.

## 2. Reproduction (headless emulator, 2026-06-11)

`test/evaluate-bug-repro.f` contains:

    CR
    .( case A same line: ) TST-A COUNT EVALUATE .( tail-A) CR
    .( case B new line: ) TST-B COUNT
    EVALUATE
    .( tail-B) CR
    .( done) CR

where `TST-A` / `TST-B` are counted strings `1 2 + .` / `3 4 + .` created
beforehand from the keyboard. With the current inc/evaluate.f:

    case A same line: 3 case B new line: 7 tail-B
    done

`tail-A` is lost: the inner string was interpreted (`3` printed) but
everything after `EVALUATE` on that line vanished. Case B (own line) works.

With the proposed fix (test/evaluate-bug-fix.f) the same run prints:

    case A same line: 3 tail-A
    case B new line: 7 tail-B
    done

## 3. Background: how F_INCLUDE feeds INTERPRET

During `INCLUDE` / `NEEDS` (`F_INCLUDE`, project/vForth18_DOES/source/
L3.asm:224) each line is read into the BLOCK 1 buffer by `F_GETLINE`
(L3.asm:174), `BLK` is set to 1, `>IN` to 0, and `INTERPRET` runs on the
buffer. Facts that matter here:

- `F_GETLINE ( a m fh -- n )` records the file position at read start,
  reads up to `m` bytes, finds the first $0A/$0D terminator (offset `n`),
  stores `n` in `SPAN`, and seeks the file back to read-start + n, i.e.
  onto the terminator (L3.asm:194-198). So *while a line is being
  interpreted*, file position = read-start + SPAN.
- The F_INCLUDE loop passes `a+1, m-2` (buffer offset shifted by one) to
  F_GETLINE (L3.asm:250-255), then restarts parsing with `0 >IN !`
  (L3.asm:260). `>IN` is therefore an absolute offset into that exact
  buffer layout.
- Nested includes save `pos + (>IN - 2 - SPAN)` = read-start + >IN - 2,
  a mid-line position (L3.asm:233-239). On return they seek there and let
  the loop re-read from that point *with >IN reset to 0* (L3.asm:270-285).
  Save and restore agree: parsing resumes just after the consumed token
  (the `2-` backs up into trailing whitespace, which is harmless).

## 4. Root cause: EVALUATE copies half of that protocol

`inc/evaluate.f` reuses the F_INCLUDE nesting idiom, but only half of it.

Save side (evaluate.f, file branch):

    SOURCE-ID @ F_FGETPOS          \ pos = read-start + SPAN
    [ 36 ] LITERAL ?ERROR
    >IN @ 2-  SPAN @  -  S>D D+    \ d' = read-start + >IN - 2  (mid-line)
    >R >R

Restore side:

    R> R>  SOURCE-ID @  F_SEEK     \ seek to d' (mid-line)
    [ 35 ] LITERAL ?ERROR
    1 BLOCK B/BUF  2DUP BLANK
    SOURCE-ID @ F_GETLINE  DROP    \ re-reads only the TAIL of the line
    ...
    R> BLK !
    R> >IN !                       \ restores the OLD ABSOLUTE >IN

After the restore the buffer holds only the tail of the line: the
character that was at column `>IN - 2` now sits at the start of the
buffer. Restoring the absolute `>IN` on top of that shifted buffer makes
parsing resume at original column `2*>IN - 2`, skipping `>IN - 2`
characters -- everything after `EVALUATE` is lost or sheared mid-token.
(F_INCLUDE avoids this because its loop restarts at `>IN = 0`.)

A secondary inconsistency: the restore calls F_GETLINE with `a, m`
(`1 BLOCK B/BUF`) while the F_INCLUDE loop uses `a+1, m-2`, so even the
tail lands one byte off relative to the normal buffer layout.

Why "EVALUATE alone on its line" works: the saved `>IN` then points at
the end of the line, the re-read tail is empty/whitespace, INTERPRET
finds nothing, and the F_INCLUDE loop simply fetches the next line. The
mis-positioning lands in blanks, so nothing visible is lost.

## 5. Proposed fix

Restore the *exact* pre-EVALUATE state instead of a shifted one. Two
changes, both in the file branch (full code: test/evaluate-bug-fix.f):

1. Save the true read-start of the current line -- drop the `>IN` term:

       SOURCE-ID @ F_FGETPOS
       [ 36 ] LITERAL ?ERROR
       SPAN @ NEGATE S>D D+        \ d' = read-start of current line
       >R >R

2. Re-read the whole line with the same call shape as the F_INCLUDE loop
   so the buffer layout is reproduced exactly:

       R> R>  SOURCE-ID @  F_SEEK
       [ 35 ] LITERAL ?ERROR
       1 BLOCK B/BUF               \ a m
       2DUP BLANK                  \ a m
       SWAP 1+ SWAP CELL-          \ a+1 m-2   (same as F_INCLUDE loop)
       SOURCE-ID @ F_GETLINE
       DROP

Everything else, including the final `R> BLK !  R> >IN !`, stays as is.
After the restore: buffer content, `SPAN`, file position (back to exactly
the saved F_FGETPOS value, since read-start + n = pos) and the absolute
`>IN` are all mutually consistent, so parsing resumes right after the
`EVALUATE` token. A further benefit: `SPAN` is correct again afterwards,
so a *second* EVALUATE later on the same line also works.

Assumption (unchanged from the current code and from F_INCLUDE itself):
`SPAN` still holds the current line length when EVALUATE runs, i.e.
nothing on the line before EVALUATE ran EXPECT or another F_GETLINE.

Verified in the headless emulator (section 2). `NEGATE` and `CELL-` are
core words, so no new dependency is introduced.

## 6. Related latent issue (not the reported bug): nested EVALUATE

The `SOURCE-ID @ 0<` branch (EVALUATE called while another EVALUATE is
the input source) has its own problems, untouched by the fix above:

- On exit it adjusts the saved pointers with `R> >IN @ + SOURCE-P !` and
  `R> >IN @ - SOURCE-L !`, but at that point `>IN` still holds the
  *inner* string's final offset -- the outer `>IN` is restored only two
  lines later. The arithmetic mixes the two scopes.
- The outer string living in BLOCK 1 was overwritten by the inner one
  and is never copied back, so the outer INTERPRET resumes over the
  inner string's remains.

Suggested direction (to be tested separately): mirror the file-branch
fix -- restore SOURCE-P / SOURCE-L verbatim, re-CMOVE the outer string
(`SOURCE-P @ FAR`, `SOURCE-L @`, clipped to B/BUF) back into BLOCK 1,
then let the shared `R> BLK !  R> >IN !` epilogue stand. Cost is one
CMOVE of at most 511 bytes.

## 7. Testing notes

Emulator (from tools/vForth):

    printf 'NEEDS EVALUATE
    CREATE TST-A ," 1 2 + ."
    CREATE TST-B ," 3 4 + ."
    INCLUDE test/evaluate-bug-fix.f
    INCLUDE test/evaluate-bug-repro.f
    .quit
    ' | python3 emu/repl.py

Omit the evaluate-bug-fix.f line to see the bug; with it, `tail-A`
appears. Note: the CREATEs must be typed at the keyboard -- creating
definitions inside an included file currently derails the *emulator*
((FIND) loops in the heap during the third vocabulary probe); that is an
emulator limitation to investigate separately, not a vForth bug.

On real hardware: run the same five lines, then re-test tutorial 021
after moving `EVALUATE` back onto the `S" ..."` line in EVAL-DEFINE.
Regression checks: a plain `INCLUDE` chain (NEEDS of a few utilities),
`EVALUATE` from keyboard, `EVALUATE` inside a colon definition, and two
EVALUATE calls on the same included source line.
