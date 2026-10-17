# Chapter 25 - Using Machine Code

[From NextBASIC to vForth](README.md)

Manual: Chapter 25, pp. 275-281.

## In short

This is where vForth is furthest ahead of BASIC. NextBASIC has no
assembler: the manual has you translate the code by hand, `POKE` the
bytes above a `CLEAR`, and call them with `USR`. vForth has an assembler
of its own, loaded with `NEEDS ASSEMBLER`, and a word for machine code,
`CODE`. The code goes into the dictionary like any other word, gets a
name, and is called by typing that name; it takes its arguments from
the stack and leaves its results there. `USR` itself survives as
`CALL#`, for code that is already in memory, and the calls to NextZXOS
that the manual sets up by hand are one word, `M_P3DOS`.

## What changes

**The code gets a name.** In BASIC the machine code is a range of
addresses that you choose, protect with `CLEAR` and remember. In vForth
`CODE name` starts a word whose body is machine code. Here is the
manual's example, written as bytes:

```forth
CODE NN99  ( -- n )
    $21 C, 99 ,                 \ ld hl,99
    $E5 C,                      \ push hl
    $DD C, $E9 C,               \ jp (ix)
    SMUDGE
NN99 .                          \ => 99
```

`C,` compiles one byte, `,` two (low byte first, as the Z80 wants), and
`SMUDGE` makes the new word visible. No `CLEAR`, no address: the
dictionary finds the room, and the word stays where it is.

**Results go on the stack, not in BC.** `USR` returns BC; a `CODE` word
pushes its results on the data stack, which is the Z80 stack, and pops
its arguments from there. So the 99 above is loaded into HL and pushed,
and there may be as many arguments and results as you like. A string,
as in `USR$`, is two cells: push the address, then the length.

**Leave through `jp (ix)`, not `ret`.** A `CODE` word is not called: it
is jumped to by the interpreter, and goes back to it with `jp (ix)`.
`NEXT` in the assembler.

**Three registers belong to Forth.** BC holds the instruction pointer,
DE the return stack pointer, IX the address of the interpreter. A
`CODE` word that needs them saves them, usually with `exx`, which swaps
BC, DE and HL with their alternate set and swaps them back at the end.
IY belongs to the ROM's interrupt, as in BASIC. SP is the data stack:
use `push` and `pop` freely, but leave it balanced as the stack comment
says.

**The assembler.** `NEEDS ASSEMBLER` loads a Z80 assembler written in
Forth, about 7K of dictionary. Its mnemonics are postfix and use `|` to
mark registers: `ld e'| l|` is `ld e,l`, `pop hl|` is `pop hl`, a
literal is followed by `N,` (one byte) or `NN,` (two). It knows the
Z80N instructions of the Next too: `NEXTREG`, `MUL`, `SWAPNIB`,
`MIRRORA`, `LDIRX`, `PIXELAD` and the others of Appendix A. This one
multiplies two bytes with `MUL`:

```forth
NEEDS ASSEMBLER
CODE TIMES  ( u1 u2 -- u )
    exx
    pop hl|  ld e'| l|
    pop hl|  ld d'| l|
    mul
    push de|
    exx
    NEXT
C;
12 11 TIMES .                   \ => 132
```

`C;` ends the word, as `;` ends a colon definition. The files in `inc/`
are written as bytes, with the instruction in a comment, so that they do
not need the assembler: tutorial `027` shows both forms, and
`util/asm2hex.py` turns one into the other.

**`USR` is `CALL#`.** For code that is already in memory, written by
someone else or loaded from a file, `CALL# ( n1 a -- n2 )` does what
`USR` does: it puts `n1` into BC (and its low byte into A), calls the
address with an ordinary `call`, so the code ends with `ret`, and gives
back BC. It saves and restores the registers of Forth itself.

```forth
NEEDS CALL#
CREATE MC  1 C, 99 C, 0 C, 201 C,     \ ld bc,99 : ret
0 MC CALL# .                    \ => 99
```

These are the manual's four bytes, unchanged; the 0 stands for the
parameter that `USR` does not have. `USR` with more parameters, which
BASIC leaves on the calculator stack, has no counterpart: give a `CODE`
word as many as it needs on the data stack.

**`BANK n USR` is `MMU7!` and `CALL#`.** Code kept in a page of your own
([Chapter 23](23-the-memory.md)) runs once the page is in the window at
`$E000`: map it, `CALL#` the address, put the old page back. The code
must have been written to run at `$E000`, and must not use the names of
the words while it runs, since their page is out of the window.

**Saving the code.** `SAVE "name" CODE a,n` and the loader that runs it
become, in vForth, simply the source file: `INCLUDE` or `NEEDS`
compiles the `CODE` words again, in a moment. `SAVE-BYTES` and
`LOAD-BYTES` ([Chapter 19](19-nextzxos-and-alternatives.md)) save and
load bytes, if you need to; and for a program that starts by itself,
`ZAP` freezes the whole running vForth into one file (tutorial `059`).

**Calling NextZXOS is one word.** The manual's example switches ROM and
RAM, moves the stack below `$BFE0`, calls the DOS, and puts everything
back, in a page of assembly. In vForth `M_P3DOS` does all that:

    n1 n2 n3 n4 a M_P3DOS ( -- n5 n6 n7 n8 f )

`n1` to `n4` go into HL, DE, BC and A, `a` is the address of the entry
in the jump table; on return the four registers come back in the same
order, and `f` is 0 when NextZXOS reports success, 1 when it reports an
error. `NEW-PAGE` and `FREE-PAGE` in [Chapter 23](23-the-memory.md) are
two examples. The common calls are words already: `F_OPEN`, `F_READ`,
`F_WRITE`, `F_SEEK`, `F_CLOSE`, `IDE_RTC`, `M_GETDATE`
([Chapter 19](19-nextzxos-and-alternatives.md) and
[Chapter 20](20-channels-streams-drivers-and-windows.md)), and the
catalogue of the example is `DIR`.

**Interrupts.** The manual's warnings about the I register and the
stack during paging are for an interrupt routine written by hand. `NEEDS
INTERRUPTS` sets one up for you and lets you write it in Forth
([Chapter 22](22-in-out-and-the-next-registers.md)).

## Correspondence table

| NextBASIC | vForth | Note |
|---|---|---|
| an assembler (Zeus, Odin, SPED) | `NEEDS ASSEMBLER` | Inside vForth, compiles into the dictionary. |
| `CLEAR n` to make room | -- | `CODE` takes the room in the dictionary. |
| `DATA` and `POKE` of the bytes | `CODE name ... C, ... SMUDGE` | Or the bytes in a `CREATE` table for `CALL#`. |
| `USR a` | `n a CALL#` | BC in, BC out; the code ends with `ret`. |
| `USR (a,p)` | `p a CALL#` | One parameter. |
| `USR (a,p1,p2,...)` | a `CODE` word | Arguments on the data stack. |
| `USR$ a` | a `CODE` word leaving `a n` | |
| `BANK n USR o` | `MMU7!` then `CALL#` | Code written to run at `$E000`. |
| `ret` | `jp (ix)`, `NEXT` | In a `CODE` word. |
| result in BC | `push` on the data stack | |
| `SAVE "n" CODE a,l` | the source file; `SAVE-BYTES` | `NEEDS SAVE-BYTES`. |
| `LOAD "n" CODE a,l` | `INCLUDE`; `LOAD-BYTES` | `NEEDS LOAD-BYTES`. |
| `SAVE "loader" LINE 10` | `ZAP` | Tutorial `059`. |
| calling NextZXOS, changing ROM and RAM | `M_P3DOS` | Does the switching itself. |
| `DOS_CATALOG` | `DIR` | |
| interrupt routine, register I | `NEEDS INTERRUPTS` | [Chapter 22](22-in-out-and-the-next-registers.md). |
| Z80N instructions | the assembler, or bytes with `C,` | `MUL`, `NEXTREG`, `LDIRX`... |

## Side by side

**The manual's routine, the BASIC way and the Forth way.** Four bytes
put above RAMTOP and called.

```
10 CLEAR 65267
20 LET a=65268
30 FOR n=0 TO 3: READ b: POKE a+n,b: NEXT n
40 PRINT USR a
50 DATA 1,99,0,201
```

The same bytes called with `CALL#` are `MC` above; written as a `CODE`
word they are `NN99`. The word is the usual form: it needs neither an
address nor `CALL#`.

**A parameter.** Double a number: the parameter arrives in BC, the
result goes back in BC.

```
10 CLEAR 65267
20 LET a=65268
30 FOR n=0 TO 5: READ b: POKE a+n,b: NEXT n
40 PRINT USR (a,21)
50 DATA 96,105,41,68,77,201
```

```forth
CREATE TW  96 C, 105 C, 41 C, 68 C, 77 C, 201 C,
21 TW CALL# .                   \ => 42
CODE TWICE  ( n -- 2n )
    $E1 C,                      \ pop hl
    $29 C,                      \ add hl,hl
    $E5 C,                      \ push hl
    $DD C, $E9 C,               \ jp (ix)
    SMUDGE
21 TWICE .                      \ => 42
```

The bytes of `TW` move the number from BC to HL and back (`ld h,b`,
`ld l,c`, `add hl,hl`, `ld b,h`, `ld c,l`, `ret`). `TWICE` has nothing to
move: the number is already on the stack, and so is the result.

**A Z80N instruction.** `MUL` multiplies D by E; the two bytes arrive
packed in one parameter.

```
10 CLEAR 65267
20 LET a=65268
30 FOR n=0 TO 6: READ b: POKE a+n,b: NEXT n
40 PRINT USR (a,12*256+11)
50 DATA 80,89,237,48,66,75,201
```

The bytes are `ld d,b`, `ld e,c`, `mul d,e`, `ld b,d`, `ld c,e`, `ret`.
In Forth it is `TIMES` above, which takes the two numbers as two
arguments, written with mnemonics instead of numbers.

## No equivalent

- **Calculator parameters.** `USR` with more than one parameter leaves
  them on BASIC's calculator stack; vForth has no calculator stack to
  read from, and does not need one.
- **The type flags of `USR`.** The zero and carry flags that tell a
  routine whether it got and must return a number or a string: in vForth
  the stack comment of the word says it.
- **The external assemblers.** Zeus, Odin and SPED are not needed; code
  they produce can still be loaded with `LOAD-BYTES` and called with
  `CALL#`.

## Further reading

- Tutorial `027` -- the assembler, `CODE`, `C;`, the register map.
- Tutorial `057` -- dot commands, ROM calls and `M_P3DOS`.
- Tutorial `059` -- `ZAP`, a program that starts by itself.
- Tutorial `049` -- interrupts.
- `HELP CODE`, `HELP CALL#`, `HELP M_P3DOS`.
- The vForth manual, section 3.9 -- the assembler.

<!-- nav -->
---

Previous: [Chapter 24 - The System Variables](24-the-system-variables.md) |
[Contents](README.md) |
Next: [Appendix A - Character Set, Z80N Mnemonics and Control Codes](app-a-character-set-z80n-control-codes.md)
